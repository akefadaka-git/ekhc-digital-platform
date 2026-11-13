"""Isolated SQLite event-store prototype for synthetic ORG-03 verification.

This module is not wired into Django or any runtime service. Callers must
provide synthetic responder references. SQLite files should be temporary test
artifacts; this module does not configure production storage.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
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

    def __init__(self, path: str | Path, *, timeout_seconds: float = 10.0):
        self.path = str(path)
        self.timeout_seconds = timeout_seconds
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path,
            timeout=self.timeout_seconds,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(f"PRAGMA busy_timeout = {int(self.timeout_seconds * 1000)}")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
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
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL,
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
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                connection.execute(
                    "INSERT INTO org03_aggregates(alert_id, priority, version, status) "
                    "VALUES (?, ?, 1, ?)",
                    (alert_id, priority, state["status"]),
                )
                connection.execute(
                    "INSERT INTO org03_events(event_id, alert_id, sequence, "
                    "idempotency_key, event_json, previous_hash, event_hash) "
                    "VALUES (?, ?, 1, ?, ?, ?, ?)",
                    (
                        event_id,
                        alert_id,
                        idempotency_key,
                        event_json,
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
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                prior = connection.execute(
                    "SELECT event_json FROM org03_events "
                    "WHERE alert_id = ? AND idempotency_key = ?",
                    (alert_id, idempotency_key),
                ).fetchone()
                if prior is not None:
                    if prior["event_json"] != event_json:
                        raise IdempotencyConflict(
                            "idempotency key was already used for a different event"
                        )
                    connection.commit()
                    return self.load_state(
                        alert_id,
                        authorized_responder_refs=authorized_responder_refs,
                    )

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
                    "idempotency_key, event_json, previous_hash, event_hash) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        event_id,
                        alert_id,
                        sequence,
                        idempotency_key,
                        event_json,
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
            if event.get("sequence") != expected_sequence or row["sequence"] != expected_sequence:
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
        with self._connect() as connection:
            aggregate = connection.execute(
                "SELECT priority, version, status FROM org03_aggregates WHERE alert_id = ?",
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
                raise EventLogIntegrityError("aggregate version differs from event log")
            if aggregate["status"] != state["status"]:
                raise EventLogIntegrityError("aggregate status differs from event log")
            return state

    def event_count(self, alert_id: str) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM org03_events WHERE alert_id = ?",
                (alert_id,),
            ).fetchone()
            return row["count"]
