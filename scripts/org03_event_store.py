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
from datetime import UTC, datetime
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


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _utc_timestamp(value: str) -> datetime:
    """Parse one explicit UTC timestamp; reject local or ambiguous clock values."""
    if not isinstance(value, str) or not value.endswith("Z"):
        raise AuthorityError(
            "authority timestamps must be explicit UTC ISO-8601 values"
        )
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise AuthorityError("authority timestamp is invalid") from exc
    if parsed.tzinfo != UTC:
        raise AuthorityError("authority timestamp must use UTC")
    return parsed


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

    def __init__(
        self,
        path: str | Path,
        *,
        timeout_seconds: float = 10.0,
        integrity_keys: dict[str, bytes] | None = None,
        active_key_id: str = "synthetic-test-v1",
        revoked_key_ids: frozenset[str] = frozenset(),
        checkpoint_dir: str | Path | None = None,
    ):
        self.path = str(path)
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.timeout_seconds = timeout_seconds
        self._integrity_keys = dict(integrity_keys or {})
        self.active_key_id = active_key_id
        self.revoked_key_ids = frozenset(revoked_key_ids)
        if any(
            not isinstance(key_id, str)
            or not key_id
            or not isinstance(key, bytes)
            or len(key) < 32
            for key_id, key in self._integrity_keys.items()
        ):
            raise ValueError(
                "integrity keys require non-empty IDs and at least 32 bytes"
            )
        if active_key_id not in self._integrity_keys:
            raise IntegrityKeyError("active integrity key is unavailable")
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
                    algorithm TEXT NOT NULL DEFAULT 'HMAC-SHA-256',
                    key_id TEXT NOT NULL DEFAULT 'synthetic-test-v1',
                    event_mac TEXT NOT NULL DEFAULT '',
                    UNIQUE(alert_id, sequence),
                    UNIQUE(alert_id, idempotency_key)
                );
                """
            )
            event_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(org03_events)")
            }
            if "algorithm" not in event_columns:
                connection.execute(
                    "ALTER TABLE org03_events ADD COLUMN algorithm "
                    "TEXT NOT NULL DEFAULT 'HMAC-SHA-256'"
                )
            authority_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(org03_authority_versions)"
                )
            }
            if "scope_ref" not in authority_columns:
                connection.execute(
                    "ALTER TABLE org03_authority_versions "
                    "ADD COLUMN scope_ref TEXT NOT NULL DEFAULT 'UNSCOPED'"
                )
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS org03_authority_versions (
                    principal_ref TEXT NOT NULL,
                    role TEXT NOT NULL,
                    scope_ref TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    valid_from_utc TEXT NOT NULL,
                    revoked_at_utc TEXT,
                    key_id TEXT NOT NULL,
                    evidence_mac TEXT NOT NULL,
                    PRIMARY KEY(principal_ref, version)
                );
                CREATE TRIGGER IF NOT EXISTS org03_authority_no_update
                BEFORE UPDATE ON org03_authority_versions
                BEGIN SELECT RAISE(ABORT, 'authority versions are immutable'); END;
                CREATE TRIGGER IF NOT EXISTS org03_authority_no_delete
                BEFORE DELETE ON org03_authority_versions
                BEGIN SELECT RAISE(ABORT, 'authority versions are immutable'); END;
            """)

    def _key(self, key_id: str) -> bytes:
        if key_id in self.revoked_key_ids or key_id not in self._integrity_keys:
            raise IntegrityKeyError("integrity key is unknown, unavailable, or revoked")
        return self._integrity_keys[key_id]

    def _event_envelope(
        self,
        alert_id,
        event_id,
        sequence,
        idempotency_key,
        event_json,
        previous_hash,
        key_id,
    ):
        return {
            "schema": "ORG03-EVENT-INTEGRITY-V1",
            "algorithm": "HMAC-SHA-256",
            "key_id": key_id,
            "alert_id": alert_id,
            "event_id": event_id,
            "sequence": sequence,
            "idempotency_key": idempotency_key,
            "event_json": event_json,
            "previous_hash": previous_hash,
        }

    def _mac(self, key_id: str, payload: dict) -> str:
        return hmac.new(
            self._key(key_id), _canonical(payload).encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def _checkpoint_path(self, alert_id: str) -> Path:
        return self.checkpoint_dir / (
            hashlib.sha256(alert_id.encode("utf-8")).hexdigest() + ".json"
        )

    def _write_checkpoint(self, alert_id: str, sequence: int, event_hash: str) -> None:
        key_id = self.active_key_id
        payload = {
            "schema": "ORG03-CHECKPOINT-V1",
            "algorithm": "HMAC-SHA-256",
            "alert_id": alert_id,
            "sequence": sequence,
            "event_hash": event_hash,
            "key_id": key_id,
        }
        checkpoint = {**payload, "mac": self._mac(key_id, payload)}
        self.checkpoint_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        try:
            os.chmod(self.checkpoint_dir, 0o700)
        except OSError:
            pass
        path = self._checkpoint_path(alert_id)
        if path.exists():
            current = json.loads(path.read_text(encoding="utf-8"))
            old_payload = {k: v for k, v in current.items() if k != "mac"}
            if not hmac.compare_digest(
                current.get("mac", ""), self._mac(old_payload["key_id"], old_payload)
            ):
                raise CheckpointError("existing checkpoint authentication failed")
            if old_payload["sequence"] > sequence:
                return
            if old_payload["sequence"] == sequence:
                if old_payload["event_hash"] != event_hash:
                    raise CheckpointError("checkpoint fork detected")
                return
        fd, temporary = tempfile.mkstemp(prefix=".checkpoint-", dir=self.checkpoint_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(_canonical(checkpoint))
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temporary, 0o600)
            os.replace(temporary, path)
            dir_fd = os.open(self.checkpoint_dir, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def _read_checkpoint(self, alert_id: str) -> dict:
        path = self._checkpoint_path(alert_id)
        if not path.exists():
            raise CheckpointError("independent checkpoint is missing")
        try:
            checkpoint = json.loads(path.read_text(encoding="utf-8"))
            payload = {k: v for k, v in checkpoint.items() if k != "mac"}
            expected = self._mac(payload["key_id"], payload)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise CheckpointError("checkpoint cannot be verified") from exc
        if not hmac.compare_digest(checkpoint.get("mac", ""), expected):
            raise CheckpointError("checkpoint authentication failed")
        return payload

    def _verify_checkpoint(
        self, alert_id: str, sequence: int, event_hash: str, payload: dict | None = None
    ) -> None:
        payload = payload or self._read_checkpoint(alert_id)
        if (
            payload.get("schema") != "ORG03-CHECKPOINT-V1"
            or payload.get("algorithm") != "HMAC-SHA-256"
            or payload.get("alert_id") != alert_id
        ):
            raise CheckpointError("checkpoint identity mismatch")
        if (
            payload.get("sequence") != sequence
            or payload.get("event_hash") != event_hash
        ):
            raise CheckpointError("database head differs from independent checkpoint")

    def _authority_payload(
        self, principal_ref, role, version, valid_from, revoked_at, key_id
    ):
        return {
            "schema": "ORG03-AUTHORITY-V1",
            "principal_ref": principal_ref,
            "role": role,
            "version": version,
            "valid_from_utc": valid_from,
            "revoked_at_utc": revoked_at,
            "key_id": key_id,
        }

    def register_authority(
        self, principal_ref: str, role: str, valid_from_utc: str
    ) -> int:
        if (
            not isinstance(principal_ref, str)
            or not principal_ref.startswith("SYNTHETIC-")
            or not role
            or role == "SYSTEM"
        ):
            raise AuthorityError(
                "only synthetic human principals and roles can be registered"
            )
        _utc_timestamp(valid_from_utc)
        key_id = self.active_key_id
        with self._connection() as connection:
            self._begin_immediate(connection)
            try:
                if connection.execute(
                    "SELECT 1 FROM org03_authority_versions WHERE principal_ref = ?",
                    (principal_ref,),
                ).fetchone():
                    raise AuthorityError("authority registration is immutable")
                payload = self._authority_payload(
                    principal_ref, role, 1, valid_from_utc, None, key_id
                )
                signature = self._mac(key_id, payload)
                connection.execute(
                    "INSERT INTO org03_authority_versions VALUES (?, ?, 1, ?, NULL, ?, ?)",
                    (principal_ref, role, valid_from_utc, key_id, signature),
                )
                connection.commit()
                return 1
            except Exception:
                connection.rollback()
                raise

    def revoke_authority(self, principal_ref: str, effective_at_utc: str) -> int:
        effective_at = _utc_timestamp(effective_at_utc)
        with self._connection() as connection:
            self._begin_immediate(connection)
            try:
                latest = connection.execute(
                    "SELECT * FROM org03_authority_versions "
                    "WHERE principal_ref = ? ORDER BY version DESC LIMIT 1",
                    (principal_ref,),
                ).fetchone()
                if latest is None or latest["revoked_at_utc"] is not None:
                    raise AuthorityError("authority is missing or already revoked")
                if effective_at < _utc_timestamp(latest["valid_from_utc"]):
                    raise AuthorityError("revocation cannot precede authority validity")
                version = latest["version"] + 1
                key_id = self.active_key_id
                payload = self._authority_payload(
                    principal_ref,
                    latest["role"],
                    version,
                    latest["valid_from_utc"],
                    effective_at_utc,
                    key_id,
                )
                signature = self._mac(key_id, payload)
                connection.execute(
                    "INSERT INTO org03_authority_versions VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        principal_ref,
                        latest["role"],
                        version,
                        latest["valid_from_utc"],
                        effective_at_utc,
                        key_id,
                        signature,
                    ),
                )
                connection.commit()
                return version
            except Exception:
                connection.rollback()
                raise

    def _authority_for_event(self, connection, event):
        role = event.get("actor_role", "SYSTEM")
        if role == "SYSTEM":
            return event
        principal_ref = event.get("actor_ref")
        rows = connection.execute(
            "SELECT * FROM org03_authority_versions "
            "WHERE principal_ref = ? ORDER BY version",
            (principal_ref,),
        ).fetchall()
        if not rows:
            raise AuthorityError("human event has no registered synthetic authority")
        latest = rows[-1]
        for row in rows:
            payload = self._authority_payload(
                row["principal_ref"],
                row["role"],
                row["version"],
                row["valid_from_utc"],
                row["revoked_at_utc"],
                row["key_id"],
            )
            if not hmac.compare_digest(
                row["evidence_mac"], self._mac(row["key_id"], payload)
            ):
                raise AuthorityError("stored authority version authentication failed")
        at_utc = event.get("at_utc", "")
        if latest["role"] != role or at_utc < latest["valid_from_utc"]:
            raise AuthorityError("principal or role is not authorized at event time")
        if latest["revoked_at_utc"] is not None and at_utc >= latest["revoked_at_utc"]:
            raise AuthorityError("authority is revoked at event time")
        payload = self._authority_payload(
            latest["principal_ref"],
            latest["role"],
            latest["version"],
            latest["valid_from_utc"],
            latest["revoked_at_utc"],
            latest["key_id"],
        )
        event = dict(event)
        event["authority_evidence"] = {
            **payload,
            "evidence_mac": latest["evidence_mac"],
        }
        return event

    def _verify_authority_event(self, connection, event):
        role = event.get("actor_role", "SYSTEM")
        evidence = event.get("authority_evidence")
        if role == "SYSTEM":
            if evidence is not None:
                raise AuthorityError("system event carries responder authority")
            return
        if not isinstance(evidence, dict):
            raise AuthorityError("human event lacks historical authority evidence")
        principal_ref = event.get("actor_ref")
        if (
            evidence.get("principal_ref") != principal_ref
            or evidence.get("role") != role
        ):
            raise AuthorityError(
                "authority evidence is bound to a different principal or role"
            )
        at_utc = _utc_timestamp(event.get("at_utc", ""))
        valid_from = _utc_timestamp(evidence.get("valid_from_utc", ""))
        revoked_at_value = evidence.get("revoked_at_utc")
        revoked_at = _utc_timestamp(revoked_at_value) if revoked_at_value else None
        if at_utc < valid_from or (revoked_at is not None and at_utc >= revoked_at):
            raise AuthorityError("historical authority is not valid at event time")
        payload = {
            key: value for key, value in evidence.items() if key != "evidence_mac"
        }
        if evidence.get("schema") != "ORG03-AUTHORITY-V1":
            raise AuthorityError("authority evidence schema is invalid")
        if not hmac.compare_digest(
            evidence.get("evidence_mac", ""),
            self._mac(evidence.get("key_id", ""), payload),
        ):
            raise AuthorityError("historical authority evidence authentication failed")
        rows = connection.execute(
            "SELECT * FROM org03_authority_versions "
            "WHERE principal_ref = ? ORDER BY version",
            (principal_ref,),
        ).fetchall()
        if not rows:
            raise AuthorityError("historical authority registry entry is missing")
        version = evidence.get("version")
        if not isinstance(version, int) or version < 1 or version > len(rows):
            raise AuthorityError("historical authority version is unavailable")
        registered = rows[version - 1]
        expected_payload = self._authority_payload(
            registered["principal_ref"],
            registered["role"],
            registered["version"],
            registered["valid_from_utc"],
            registered["revoked_at_utc"],
            registered["key_id"],
        )
        if payload != expected_payload or registered["version"] != version:
            raise AuthorityError(
                "event evidence does not match its immutable registry version"
            )
        for row in rows:
            signed = self._authority_payload(
                row["principal_ref"],
                row["role"],
                row["version"],
                row["valid_from_utc"],
                row["revoked_at_utc"],
                row["key_id"],
            )
            if not hmac.compare_digest(
                row["evidence_mac"], self._mac(row["key_id"], signed)
            ):
                raise AuthorityError("authority registry tampering detected")
        latest_revocation = rows[-1]["revoked_at_utc"]
        if latest_revocation and at_utc >= _utc_timestamp(latest_revocation):
            raise AuthorityError("event timestamp is at or after authority revocation")

    def create_alert(self, alert_id: str, priority: str, received_at_utc: str) -> dict:
        state = new_alert(alert_id, priority, received_at_utc)
        initial_event = state["history"][0]
        event_json = _canonical(initial_event)
        event_id = f"{alert_id}:1"
        idempotency_key = f"{alert_id}:initial"
        event_hash = _digest(
            self.GENESIS_HASH, alert_id, event_id, 1, idempotency_key, event_json
        )
        key_id = self.active_key_id
        event_mac = self._mac(
            key_id,
            self._event_envelope(
                alert_id,
                event_id,
                1,
                idempotency_key,
                event_json,
                self.GENESIS_HASH,
                key_id,
            ),
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
                    "previous_hash, event_hash, algorithm, key_id, event_mac) "
                    "VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                        "HMAC-SHA-256",
                        key_id,
                        event_mac,
                    ),
                )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
        self._write_checkpoint(alert_id, 1, event_hash)
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
        with self._connection() as connection:
            self._begin_immediate(connection)
            try:
                request_json = _canonical(
                    {
                        "alert_id": alert_id,
                        "event_id": event_id,
                        "idempotency_key": idempotency_key,
                        "expected_version": expected_version,
                        "event_type": event.get("event"),
                        "event_json": _canonical(event),
                    }
                )
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

                event = self._authority_for_event(connection, event)
                event_json = _canonical(event)
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
                    "SELECT sequence, event_hash FROM org03_events "
                    "WHERE alert_id = ? ORDER BY sequence DESC LIMIT 1",
                    (alert_id,),
                ).fetchone()
                self._verify_checkpoint(
                    alert_id, previous["sequence"], previous["event_hash"]
                )
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
                key_id = self.active_key_id
                event_mac = self._mac(
                    key_id,
                    self._event_envelope(
                        alert_id,
                        event_id,
                        sequence,
                        idempotency_key,
                        event_json,
                        previous_hash,
                        key_id,
                    ),
                )
                connection.execute(
                    "INSERT INTO org03_events(event_id, alert_id, sequence, "
                    "idempotency_key, event_json, request_json, result_json, "
                    "previous_hash, event_hash, algorithm, key_id, event_mac) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                        "HMAC-SHA-256",
                        key_id,
                        event_mac,
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
                self._write_checkpoint(alert_id, sequence, event_hash)
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
            self._verify_authority_event(connection, event)
            if row["algorithm"] != "HMAC-SHA-256":
                raise EventLogIntegrityError(
                    "unsupported event authentication algorithm"
                )
            key_id = row["key_id"]
            calculated_mac = self._mac(
                key_id,
                self._event_envelope(
                    row["alert_id"],
                    row["event_id"],
                    row["sequence"],
                    row["idempotency_key"],
                    row["event_json"],
                    previous_hash,
                    key_id,
                ),
            )
            if not hmac.compare_digest(row["event_mac"], calculated_mac):
                raise EventLogIntegrityError("event HMAC verification failed")
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
        checkpoint_snapshot = self._read_checkpoint(alert_id)
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
                last_event = connection.execute(
                    "SELECT sequence, event_hash FROM org03_events "
                    "WHERE alert_id = ? ORDER BY sequence DESC LIMIT 1",
                    (alert_id,),
                ).fetchone()
                self._verify_checkpoint(
                    alert_id,
                    last_event["sequence"],
                    last_event["event_hash"],
                    checkpoint_snapshot,
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
