"""Checkpoint-ledger contract and synthetic SQLite adapter for ORG-03.

The SQLite adapter is for deterministic tests only. It shares the host and
filesystem failure domain with an event store and MUST NOT be represented as
the production independent checkpoint authority. Production must inject an
independently administered ledger and protected asymmetric signer.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


GENESIS_HASH = "0" * 64


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class CheckpointLedgerError(RuntimeError):
    """Base error for checkpoint ledger operations."""


class CheckpointConflict(CheckpointLedgerError):
    """The ledger head or an existing sequence conflicts with the request."""


class CheckpointAuthenticationError(CheckpointLedgerError):
    """A checkpoint signature or stored record is invalid."""


@dataclass(frozen=True)
class Checkpoint:
    alert_id: str
    sequence: int
    event_hash: str
    previous_sequence: int
    previous_hash: str
    checkpoint_version: int
    key_id: str
    published_at_utc: str

    def payload(self) -> dict[str, object]:
        return asdict(self)


class CheckpointSigner(Protocol):
    def sign(self, payload: dict[str, object]) -> tuple[str, str]: ...
    def verify(self, key_id: str, payload: dict[str, object], signature: str) -> bool: ...


class CheckpointLedger(Protocol):
    def head(self, alert_id: str) -> Checkpoint | None: ...
    def get(self, alert_id: str, sequence: int) -> Checkpoint | None: ...
    def compare_and_set(self, checkpoint: Checkpoint, signature: str) -> bool: ...


class HMACCheckpointSigner:
    """Synthetic-only signer. Never use this as production key custody."""

    def __init__(
        self,
        keys: dict[str, bytes],
        active_key_id: str,
        revoked_key_ids: frozenset[str] = frozenset(),
    ):
        if not keys or active_key_id not in keys:
            raise ValueError("active checkpoint signing key is unavailable")
        if any(not key_id or not isinstance(key, bytes) or len(key) < 32
               for key_id, key in keys.items()):
            raise ValueError("checkpoint test keys must contain at least 32 bytes")
        self._keys = dict(keys)
        self.active_key_id = active_key_id
        self.revoked_key_ids = frozenset(revoked_key_ids)

    def sign(self, payload: dict[str, object]) -> tuple[str, str]:
        if self.active_key_id in self.revoked_key_ids:
            raise CheckpointAuthenticationError("active signing key is revoked")
        signature = hmac.new(
            self._keys[self.active_key_id],
            canonical_json(payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return self.active_key_id, signature

    def verify(self, key_id: str, payload: dict[str, object], signature: str) -> bool:
        key = self._keys.get(key_id)
        if key is None or key_id in self.revoked_key_ids:
            return False
        expected = hmac.new(
            key, canonical_json(payload).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)


class SQLiteCheckpointLedger:
    """Independent-file ledger simulator for tests; not a production trust anchor."""

    def __init__(self, path: str | Path, signer: CheckpointSigner, timeout: float = 10.0):
        self.path = str(path)
        self.signer = signer
        self.timeout = timeout
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=self.timeout, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            mode = connection.execute("PRAGMA journal_mode = WAL").fetchone()[0]
            if str(mode).lower() != "wal":
                raise CheckpointLedgerError("checkpoint ledger WAL mode unavailable")
            synchronous = connection.execute("PRAGMA synchronous").fetchone()[0]
            if synchronous != 2:
                raise CheckpointLedgerError("checkpoint ledger requires synchronous=FULL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS org03_checkpoint_records (
                    alert_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL CHECK(sequence >= 1),
                    event_hash TEXT NOT NULL,
                    previous_sequence INTEGER NOT NULL CHECK(previous_sequence >= 0),
                    previous_hash TEXT NOT NULL,
                    checkpoint_version INTEGER NOT NULL CHECK(checkpoint_version >= 1),
                    key_id TEXT NOT NULL,
                    published_at_utc TEXT NOT NULL,
                    signature TEXT NOT NULL,
                    PRIMARY KEY(alert_id, sequence)
                );
                CREATE TRIGGER IF NOT EXISTS org03_checkpoint_no_update
                BEFORE UPDATE ON org03_checkpoint_records
                BEGIN SELECT RAISE(ABORT, 'checkpoint records are immutable'); END;
                CREATE TRIGGER IF NOT EXISTS org03_checkpoint_no_delete
                BEFORE DELETE ON org03_checkpoint_records
                BEGIN SELECT RAISE(ABORT, 'checkpoint records are immutable'); END;
                """
            )

    @staticmethod
    def _record(row: sqlite3.Row) -> Checkpoint:
        record = Checkpoint(
            alert_id=row["alert_id"],
            sequence=row["sequence"],
            event_hash=row["event_hash"],
            previous_sequence=row["previous_sequence"],
            previous_hash=row["previous_hash"],
            checkpoint_version=row["checkpoint_version"],
            key_id=row["key_id"],
            published_at_utc=row["published_at_utc"],
        )
        return record

    def _verified_record(self, row: sqlite3.Row | None) -> Checkpoint | None:
        if row is None:
            return None
        record = self._record(row)
        if not self.signer.verify(record.key_id, record.payload(), row["signature"]):
            raise CheckpointAuthenticationError("stored checkpoint authentication failed")
        return record

    def head(self, alert_id: str) -> Checkpoint | None:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM org03_checkpoint_records WHERE alert_id=? ORDER BY sequence",
                (alert_id,),
            ).fetchall()
        records = [self._verified_record(row) for row in rows]
        previous_hash = GENESIS_HASH
        for expected_sequence, record in enumerate(records, start=1):
            if (
                record.sequence != expected_sequence
                or record.previous_sequence != expected_sequence - 1
                or record.previous_hash != previous_hash
            ):
                raise CheckpointAuthenticationError("checkpoint history is not contiguous")
            previous_hash = record.event_hash
        return records[-1] if records else None

    def get(self, alert_id: str, sequence: int) -> Checkpoint | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM org03_checkpoint_records WHERE alert_id=? AND sequence=?",
                (alert_id, sequence),
            ).fetchone()
        return self._verified_record(row)

    def history(self, alert_id: str, start: int, end: int) -> list[Checkpoint]:
        if start < 1 or end < start:
            raise ValueError("invalid checkpoint history range")
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM org03_checkpoint_records WHERE alert_id=? "
                "AND sequence BETWEEN ? AND ? ORDER BY sequence",
                (alert_id, start, end),
            ).fetchall()
        records = [self._verified_record(row) for row in rows]
        previous = self.get(alert_id, start - 1) if start > 1 else None
        previous_hash = previous.event_hash if previous else GENESIS_HASH
        expected_sequence = start
        for record in records:
            if (
                record.sequence != expected_sequence
                or record.previous_sequence != expected_sequence - 1
                or record.previous_hash != previous_hash
            ):
                raise CheckpointAuthenticationError("checkpoint history is not contiguous")
            previous_hash = record.event_hash
            expected_sequence += 1
        if expected_sequence != end + 1:
            raise CheckpointAuthenticationError("checkpoint history contains a sequence gap")
        return records

    def compare_and_set(self, checkpoint: Checkpoint, signature: str) -> bool:
        """Advance exactly one sequence; return False for an exact idempotent repeat."""
        try:
            timestamp = datetime.fromisoformat(checkpoint.published_at_utc.replace("Z", "+00:00"))
        except (TypeError, ValueError) as exc:
            raise CheckpointConflict("checkpoint timestamp is invalid") from exc
        if timestamp.tzinfo != UTC or not checkpoint.published_at_utc.endswith("Z"):
            raise CheckpointConflict("checkpoint timestamp must be explicit UTC")
        if checkpoint.sequence < 1 or checkpoint.checkpoint_version < 1:
            raise CheckpointConflict("checkpoint sequence and version must be positive")
        if checkpoint.sequence != checkpoint.previous_sequence + 1:
            raise CheckpointConflict("checkpoint must advance exactly one sequence")
        if checkpoint.previous_sequence == 0 and checkpoint.previous_hash != GENESIS_HASH:
            raise CheckpointConflict("genesis predecessor hash is invalid")
        if not self.signer.verify(checkpoint.key_id, checkpoint.payload(), signature):
            raise CheckpointAuthenticationError("checkpoint signature is invalid")
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                row = connection.execute(
                    "SELECT * FROM org03_checkpoint_records WHERE alert_id=? "
                    "ORDER BY sequence DESC LIMIT 1", (checkpoint.alert_id,)
                ).fetchone()
                current = self._verified_record(row)
                if current and current.sequence == checkpoint.sequence:
                    if (
                        current.event_hash == checkpoint.event_hash
                        and current.previous_sequence == checkpoint.previous_sequence
                        and current.previous_hash == checkpoint.previous_hash
                        and current.checkpoint_version == checkpoint.checkpoint_version
                    ):
                        connection.commit()
                        return False
                    raise CheckpointConflict("same sequence has a different checkpoint")
                current_sequence = current.sequence if current else 0
                current_hash = current.event_hash if current else GENESIS_HASH
                if (current_sequence, current_hash) != (
                    checkpoint.previous_sequence, checkpoint.previous_hash
                ):
                    raise CheckpointConflict("checkpoint compare-and-set predecessor mismatch")
                connection.execute(
                    "INSERT INTO org03_checkpoint_records "
                    "(alert_id, sequence, event_hash, previous_sequence, previous_hash, "
                    "checkpoint_version, key_id, published_at_utc, signature) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        checkpoint.alert_id, checkpoint.sequence, checkpoint.event_hash,
                        checkpoint.previous_sequence, checkpoint.previous_hash,
                        checkpoint.checkpoint_version, checkpoint.key_id,
                        checkpoint.published_at_utc, signature,
                    ),
                )
                connection.commit()
                return True
            except Exception:
                connection.rollback()
                raise
