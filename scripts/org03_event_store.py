"""Isolated SQLite event-store prototype for synthetic ORG-03 verification.

This module is not wired into Django or any runtime service. Callers must
provide synthetic responder references. SQLite files should be temporary test
artifacts; this module does not configure production storage.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from scripts.org03_events import TransitionError, apply_event, new_alert


class EventStoreError(RuntimeError):
    """Base class for durable event-store failures."""


class StaleAggregateVersion(EventStoreError):
    """The caller's expected aggregate version is no longer current."""


class IdempotencyConflict(EventStoreError):
    """An idempotency key was reused for a different event."""


class EventLogIntegrityError(EventStoreError):
    """Stored event history failed its integrity or replay checks."""


class EventStoreBusy(EventStoreError):
    """SQLite remained busy beyond the configured bounded retry deadline."""


class IntegrityKeyError(EventLogIntegrityError):
    """An integrity key is unknown, unavailable, or revoked."""


class CheckpointError(EventLogIntegrityError):
    """The independent authenticated checkpoint is invalid or stale."""


class AuthorityError(EventStoreError):
    """Synthetic historical authority evidence is invalid."""


DEFAULT_SYNTHETIC_KEYS = {"synthetic-test-v1": b"ORG03-TEST-ONLY-KEY-NOT-FOR-PRODUCTION-32"}


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(
    previous_hash: str,
    alert_id: str,
    event_id: str,
    sequence: int,
    idempotency_key: str,
    event_json: str,
) -> str:
    envelope = _canonical(
        {
            "alert_id": alert_id,
            "event_id": event_id,
            "sequence": sequence,
            "idempotency_key": idempotency_key,
            "event_json": event_json,
        }
    )
    return hashlib.sha256((previous_hash + "\n" + envelope).encode("utf-8")).hexdigest()


class Org03EventStore:
    """Transactional, append-only-by-interface SQLite adapter for tests."""

    GENESIS_HASH = "0" * 64

    def __init__(self, path: str | Path, *, timeout_seconds: float = 10.0, integrity_keys: dict[str, bytes] | None = None, active_key_id: str = "synthetic-test-v1", revoked_key_ids: frozenset[str] = frozenset(), checkpoint_dir: str | Path | None = None):
        self.path = str(path)
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.timeout_seconds = timeout_seconds
        self._integrity_keys = dict(integrity_keys or DEFAULT_SYNTHETIC_KEYS)
        self.active_key_id = active_key_id
        self.revoked_key_ids = frozenset(revoked_key_ids)
        if active_key_id not in self._integrity_keys or active_key_id in self.revoked_key_ids:
            raise IntegrityKeyError("active integrity key is unavailable")
        if any(not isinstance(key, bytes) or len(key) < 32 for key in self._integrity_keys.values()):
            raise ValueError("integrity keys must contain at least 32 bytes")
        self.checkpoint_dir = Path(checkpoint_dir or (self.path + ".org03-checkpoints"))
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=min(self.timeout_seconds, 0.1),
            isolation_level=None,
        )
        try:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            busy_timeout_ms = int(min(self.timeout_seconds, 0.1) * 1000)
            connection.execute(f"PRAGMA busy_timeout = {busy_timeout_ms}")
            return connection
        except Exception:
            connection.close()
            raise

    @contextmanager
    def _connection(self):
        """Own and deterministically close one SQLite connection."""
        connection = self._connect()
        try:
            yield connection
        finally:
            connection.close()

    def _begin_immediate(self, connection: sqlite3.Connection) -> None:
        """Acquire the writer reservation with bounded lock/busy retries."""
        deadline = time.monotonic() + self.timeout_seconds
        delay = 0.01
        while True:
            try:
                connection.execute("BEGIN IMMEDIATE")
                return
            except sqlite3.OperationalError as exc:
                message = str(exc).lower()
                if "locked" not in message and "busy" not in message:
                    raise
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise EventStoreBusy(
                        "SQLite remained busy past the retry deadline"
                    ) from exc
                time.sleep(min(delay, remaining))
                delay = min(delay * 2, 0.1)

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS org03_aggregates (
                    alert_id TEXT PRIMARY KEY,
                    priority TEXT NOT NULL,
                    version INTEGER NOT NULL CHECK (version >= 1),
                    status TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS org03_events (
                    event_id TEXT PRIMARY KEY,
                    alert_id TEXT NOT NULL REFERENCES org03_aggregates(alert_id),
                    sequence INTEGER NOT NULL CHECK (sequence >= 1),
                    idempotency_key TEXT NOT NULL,
                    event_json TEXT NOT NULL,
                    request_json TEXT,
                    result_json TEXT,
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL,
                    key_id TEXT NOT NULL DEFAULT 'synthetic-test-v1',
                    event_mac TEXT NOT NULL DEFAULT '',
                    UNIQUE(alert_id, sequence),
                    UNIQUE(alert_id, idempotency_key)
                );
                """
            )

    def create_alert(self, alert_id: str, priority: str, received_at_utc: str) -> dict:
        state = new_alert(alert_id, priority, received_at_utc)
        initial_event = state["history"][0]
        event_json = _canonical(initial_event)
        event_id = f"{alert_id}:1"
        idempotency_key = f"{alert_id}:initial"
        event_hash = _digest(
            self.GENESIS_HASH, alert_id, event_id, 1, idempotency_key, event_json
        )
        with self._connection() as connection:
            self._begin_immediate(connection)
            try:
                connection.execute(
                    "INSERT INTO org03_aggregates(alert_id, priority, version, status) "
                    "VALUES (?, ?, 1, ?)",
                    (alert_id, priority, state["status"]),
                )
                connection.execute(
                    "INSERT INTO org03_events(event_id, alert_id, sequence, "
                    "idempotency_key, event_json, request_json, result_json, "
                    "previous_hash, event_hash) "
                    "VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?)",
                    (
                        event_id,
                        alert_id,
                        idempotency_key,
                        event_json,
                        _canonical(
                            {
                                "alert_id": alert_id,
                                "event_id": event_id,
                                "idempotency_key": idempotency_key,
                                "expected_version": 0,
                                "event_type": "RECEIVED",
                                "event_json": event_json,
                            }
                        ),
                        _canonical(state),
                        self.GENESIS_HASH,
                        event_hash,
                    ),
                )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
        return state

    def append_event(
        self,
        alert_id: str,
        event: dict,
        *,
        expected_version: int,
        event_id: str,
        idempotency_key: str,
        authorized_responder_refs: dict[str, str],
    ) -> dict:
        if not event_id or not idempotency_key:
            raise EventStoreError("event_id and idempotency_key are required")
        event_json = _canonical(event)
        request_json = _canonical(
            {
                "alert_id": alert_id,
                "event_id": event_id,
                "idempotency_key": idempotency_key,
                "expected_version": expected_version,
                "event_type": event.get("event"),
                "event_json": event_json,
            }
        )
        with self._connection() as connection:
            self._begin_immediate(connection)
            try:
                prior = connection.execute(
                    "SELECT event_id, event_json, request_json, result_json "
                    "FROM org03_events "
                    "WHERE alert_id = ? AND idempotency_key = ?",
                    (alert_id, idempotency_key),
                ).fetchone()
                if prior is not None:
                    if (
                        prior["request_json"] != request_json
                        or prior["event_id"] != event_id
                    ):
                        raise IdempotencyConflict(
                            "idempotency key was already used for a different request"
                        )
                    if prior["result_json"] is None:
                        raise EventLogIntegrityError(
                            "idempotent result snapshot is missing"
                        )
                    original_result = json.loads(prior["result_json"])
                    connection.commit()
                    return original_result

                aggregate = connection.execute(
                    "SELECT priority, version FROM org03_aggregates WHERE alert_id = ?",
                    (alert_id,),
                ).fetchone()
                if aggregate is None:
                    raise EventStoreError("alert does not exist")
                if aggregate["version"] != expected_version:
                    raise StaleAggregateVersion(
                        f"expected version {expected_version}; current version is "
                        f"{aggregate['version']}"
                    )

                state = self._replay_in_transaction(
                    connection,
                    alert_id,
                    aggregate["priority"],
                    authorized_responder_refs,
                )
                if state["next_sequence"] != expected_version + 1:
                    raise EventLogIntegrityError(
                        "aggregate version does not match event log"
                    )

                updated = apply_event(
                    state,
                    event,
                    authorized_responder_refs=authorized_responder_refs,
                )
                previous = connection.execute(
                    "SELECT event_hash FROM org03_events "
                    "WHERE alert_id = ? ORDER BY sequence DESC LIMIT 1",
                    (alert_id,),
                ).fetchone()
                previous_hash = previous["event_hash"]
                sequence = event["sequence"]
                event_hash = _digest(
                    previous_hash,
                    alert_id,
                    event_id,
                    sequence,
                    idempotency_key,
                    event_json,
                )
                connection.execute(
                    "INSERT INTO org03_events(event_id, alert_id, sequence, "
                    "idempotency_key, event_json, request_json, result_json, "
                    "previous_hash, event_hash) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        event_id,
                        alert_id,
                        sequence,
                        idempotency_key,
                        event_json,
                        request_json,
                        _canonical(updated),
                        previous_hash,
                        event_hash,
                    ),
                )
                cursor = connection.execute(
                    "UPDATE org03_aggregates SET version = ?, status = ? "
                    "WHERE alert_id = ? AND version = ?",
                    (sequence, updated["status"], alert_id, expected_version),
                )
                if cursor.rowcount != 1:
                    raise StaleAggregateVersion("aggregate compare-and-update lost")
                connection.commit()
                return updated
            except Exception:
                connection.rollback()
                raise

    def _replay_in_transaction(
        self,
        connection: sqlite3.Connection,
        alert_id: str,
        priority: str,
        authorized_responder_refs: dict[str, str],
    ) -> dict:
        rows = connection.execute(
            "SELECT * FROM org03_events WHERE alert_id = ? ORDER BY sequence",
            (alert_id,),
        ).fetchall()
        if not rows:
            raise EventLogIntegrityError("event log is empty")
        first = json.loads(rows[0]["event_json"])
        if first.get("sequence") != 1 or first.get("event") != "RECEIVED":
            raise EventLogIntegrityError("invalid initial event")
        state = new_alert(alert_id, priority, first["at_utc"])
        previous_hash = self.GENESIS_HASH
        for index, row in enumerate(rows):
            event = json.loads(row["event_json"])
            expected_sequence = index + 1
            if (
                event.get("sequence") != expected_sequence
                or row["sequence"] != expected_sequence
            ):
                raise EventLogIntegrityError("event sequence gap or duplicate")
            if row["previous_hash"] != previous_hash:
                raise EventLogIntegrityError("event hash-chain predecessor mismatch")
            calculated = _digest(
                previous_hash,
                row["alert_id"],
                row["event_id"],
                row["sequence"],
                row["idempotency_key"],
                row["event_json"],
            )
            if calculated != row["event_hash"]:
                raise EventLogIntegrityError("event hash mismatch")
            if index:
                try:
                    state = apply_event(
                        state,
                        event,
                        authorized_responder_refs=authorized_responder_refs,
                    )
                except TransitionError as exc:
                    raise EventLogIntegrityError(
                        "stored event cannot be replayed"
                    ) from exc
            previous_hash = calculated
        return state

    def load_state(
        self, alert_id: str, *, authorized_responder_refs: dict[str, str]
    ) -> dict:
        with self._connection() as connection:
            connection.execute("BEGIN")
            try:
                aggregate = connection.execute(
                    "SELECT priority, version, status FROM org03_aggregates "
                    "WHERE alert_id = ?",
                    (alert_id,),
                ).fetchone()
                if aggregate is None:
                    raise EventStoreError("alert does not exist")
                state = self._replay_in_transaction(
                    connection,
                    alert_id,
                    aggregate["priority"],
                    authorized_responder_refs,
                )
                if aggregate["version"] != state["next_sequence"] - 1:
                    raise EventLogIntegrityError(
                        "aggregate version differs from event log"
                    )
                if aggregate["status"] != state["status"]:
                    raise EventLogIntegrityError(
                        "aggregate status differs from event log"
                    )
                connection.commit()
                return state
            except Exception:
                connection.rollback()
                raise

    def event_count(self, alert_id: str) -> int:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM org03_events WHERE alert_id = ?",
                (alert_id,),
            ).fetchone()
            return row["count"]
