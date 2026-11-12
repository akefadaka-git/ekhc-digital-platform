"""Fail-closed, mock-only notification adapters for EKHC OS.

This module deliberately imports no network, SMTP, provider, or SDK clients.
Mock receipts are synthetic test evidence, never evidence of delivery.
An optional SQLite ledger persists only synthetic identifiers and redacted
status metadata. It is not a live-delivery ledger.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from collections.abc import Iterator, Mapping
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from threading import RLock


class NotificationConfigurationError(ValueError):
    """Raised when notification configuration is missing or unsafe."""


class Channel(StrEnum):
    EMAIL = "email"
    SMS = "sms"


class MockOutcome(StrEnum):
    ACCEPTED = "SIMULATED_ACCEPTED"
    REJECTED = "SIMULATED_REJECTED"
    TIMEOUT = "SIMULATED_TIMEOUT"
    UNAVAILABLE = "SIMULATED_UNAVAILABLE"
    RETRY_EXHAUSTED = "SIMULATED_RETRY_EXHAUSTED"


TRANSIENT_OUTCOMES = {MockOutcome.TIMEOUT, MockOutcome.UNAVAILABLE}
ALLOWED_FIXTURE_SET = "synthetic-default-v1"
DESTINATION_PATTERN = re.compile(r"^synthetic-(email|sms)-recipient-[0-9]{2}$")
EVENT_ID_PATTERN = re.compile(r"^SYNTH-[A-Z0-9-]{1,48}$")
EVENT_CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")
LIVE_CONFIGURATION_KEYS = {
    "EKHC_EMAIL_PROVIDER_CREDENTIAL",
    "EKHC_EMAIL_SENDER_IDENTITY",
    "EKHC_SMS_PROVIDER_CREDENTIAL",
    "EKHC_SMS_SENDER_IDENTITY",
}


@dataclass(frozen=True)
class NotificationConfig:
    mode: str
    email_mode: str
    sms_mode: str
    fixture_set: str | None = None
    log_level: str = "summary"
    ledger_path: str | None = None

    @classmethod
    def from_environment(cls, environ: Mapping[str, str]) -> NotificationConfig:
        """Load only the explicitly supported mock configuration contract."""
        unsafe_keys = LIVE_CONFIGURATION_KEYS.intersection(environ)
        unsafe_keys.update(
            key
            for key in environ
            if key.startswith("EKHC_NOTIFICATION_")
            and key
            not in {
                "EKHC_NOTIFICATION_MODE",
                "EKHC_NOTIFICATION_FIXTURE_SET",
                "EKHC_NOTIFICATION_LOG_LEVEL",
                "EKHC_NOTIFICATION_LEDGER_PATH",
            }
        )
        unsafe_keys.update(
            key
            for key in environ
            if key.startswith(("EKHC_EMAIL_", "EKHC_SMS_"))
            and key not in {"EKHC_EMAIL_MODE", "EKHC_SMS_MODE"}
        )
        unsafe_keys.update(
            key
            for key in environ
            if key.startswith("EKHC_")
            and re.search(r"(CREDENTIAL|TOKEN|API_KEY|ENDPOINT|SENDER_IDENTITY)$", key)
        )
        if unsafe_keys:
            raise NotificationConfigurationError(
                "Live-provider or unsupported notification configuration "
                "is not permitted"
            )
        values = {
            "EKHC_NOTIFICATION_MODE": environ.get("EKHC_NOTIFICATION_MODE"),
            "EKHC_EMAIL_MODE": environ.get("EKHC_EMAIL_MODE"),
            "EKHC_SMS_MODE": environ.get("EKHC_SMS_MODE"),
        }
        for key, value in values.items():
            if value != "mock":
                raise NotificationConfigurationError(
                    f"{key} must be explicitly set to mock"
                )
        fixture_set = environ.get("EKHC_NOTIFICATION_FIXTURE_SET") or None
        if fixture_set not in (None, ALLOWED_FIXTURE_SET):
            raise NotificationConfigurationError(
                "Unknown synthetic notification fixture set"
            )
        log_level = environ.get("EKHC_NOTIFICATION_LOG_LEVEL", "summary")
        if log_level not in {"summary", "debug"}:
            raise NotificationConfigurationError(
                "EKHC_NOTIFICATION_LOG_LEVEL must be summary or debug"
            )
        ledger_path = environ.get("EKHC_NOTIFICATION_LEDGER_PATH") or None
        if ledger_path is not None and (
            not ledger_path.strip() or "://" in ledger_path
        ):
            raise NotificationConfigurationError(
                "Notification ledger path must be a local filesystem path"
            )
        return cls(
            mode="mock",
            email_mode="mock",
            sms_mode="mock",
            fixture_set=fixture_set,
            log_level=log_level,
            ledger_path=ledger_path,
        )


@dataclass(frozen=True)
class Notification:
    event_id: str
    severity: str
    event_code: str

    def __post_init__(self) -> None:
        if not EVENT_ID_PATTERN.fullmatch(self.event_id):
            raise ValueError("event_id must be a synthetic opaque identifier")
        if self.severity not in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
            raise ValueError("Unsupported notification severity")
        if not EVENT_CODE_PATTERN.fullmatch(self.event_code):
            raise ValueError("event_code must be a normalized action code")


@dataclass(frozen=True)
class FixtureSet:
    """Deterministic outcomes keyed by channel; no real recipient data."""

    outcomes: Mapping[Channel, tuple[MockOutcome, ...]]

    @classmethod
    def accepted(cls) -> FixtureSet:
        return cls(
            outcomes={
                Channel.EMAIL: (MockOutcome.ACCEPTED,),
                Channel.SMS: (MockOutcome.ACCEPTED,),
            }
        )


@dataclass(frozen=True)
class DeliveryReceipt:
    event_id: str
    channel: Channel
    destination_reference: str
    status: MockOutcome
    attempts: int
    simulated: bool = True
    delivery_claim: bool = False
    display_label: str = "SIMULATED — NOT DELIVERED"


class SQLiteNotificationLedger:
    """Durable, transactional storage for synthetic mock receipts and audit.

    The database contains opaque synthetic references only. A BEGIN IMMEDIATE
    transaction serializes writers across processes, so a duplicate event
    cannot race past the idempotency check. The transaction is intentionally
    held only while mock adapters execute; this class must never wrap live I/O.
    """

    def __init__(self, path: str) -> None:
        if not isinstance(path, str) or not path.strip():
            raise ValueError("A local SQLite ledger path is required")
        self.path = path
        if path != ":memory:":
            database_path = Path(path)
            database_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            if database_path.exists() and database_path.is_symlink():
                raise ValueError("Notification ledger must not be a symlink")
        self._lock = RLock()
        self._connection = sqlite3.connect(
            path, timeout=30, isolation_level=None, check_same_thread=False
        )
        self._connection.execute("PRAGMA busy_timeout = 30000")
        self._connection.execute("PRAGMA synchronous = FULL")
        if path != ":memory:":
            self._connection.execute("PRAGMA journal_mode = WAL")
            os.chmod(path, 0o600)
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS notification_receipts (
                event_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                destination_reference TEXT NOT NULL,
                status TEXT NOT NULL,
                attempts INTEGER NOT NULL CHECK (attempts BETWEEN 1 AND 3),
                simulated INTEGER NOT NULL CHECK (simulated = 1),
                delivery_claim INTEGER NOT NULL CHECK (delivery_claim = 0),
                display_label TEXT NOT NULL
                    CHECK (display_label = 'SIMULATED — NOT DELIVERED'),
                PRIMARY KEY (event_id, channel)
            );
            CREATE TABLE IF NOT EXISTS notification_audit (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                event_json TEXT NOT NULL
            );
            """
        )

    @contextmanager
    def transaction(self) -> Iterator[SQLiteNotificationLedger]:
        """Acquire a cross-process write lock and commit or roll back atomically."""
        with self._lock:
            self._connection.execute("BEGIN IMMEDIATE")
            try:
                yield self
            except BaseException:
                self._connection.rollback()
                raise
            else:
                self._connection.commit()

    def load_receipts(self) -> dict[tuple[str, Channel], DeliveryReceipt]:
        rows = self._connection.execute(
            "SELECT event_id, channel, destination_reference, status, attempts, "
            "simulated, delivery_claim, display_label FROM notification_receipts"
        ).fetchall()
        return {
            (row[0], Channel(row[1])): DeliveryReceipt(
                event_id=row[0],
                channel=Channel(row[1]),
                destination_reference=row[2],
                status=MockOutcome(row[3]),
                attempts=row[4],
                simulated=bool(row[5]),
                delivery_claim=bool(row[6]),
                display_label=row[7],
            )
            for row in rows
        }

    def save_receipt(self, receipt: DeliveryReceipt) -> None:
        if not receipt.simulated or receipt.delivery_claim:
            raise ValueError("Only explicitly simulated receipts may be persisted")
        self._connection.execute(
            "INSERT INTO notification_receipts "
            "(event_id, channel, destination_reference, status, attempts, "
            "simulated, delivery_claim, display_label) "
            "VALUES (?, ?, ?, ?, ?, 1, 0, ?)",
            (
                receipt.event_id,
                receipt.channel.value,
                receipt.destination_reference,
                receipt.status.value,
                receipt.attempts,
                receipt.display_label,
            ),
        )

    def record_audit(self, events: list[dict[str, object]]) -> None:
        for event in events:
            event_id = event.get("event_id")
            if not isinstance(event_id, str) or not EVENT_ID_PATTERN.fullmatch(
                event_id
            ):
                raise ValueError("Only synthetic event IDs may enter the audit ledger")
            self._connection.execute(
                "INSERT INTO notification_audit (event_id, event_json) VALUES (?, ?)",
                (event_id, json.dumps(event, sort_keys=True, separators=(",", ":"))),
            )

    def load_audit_events(self) -> list[dict[str, object]]:
        rows = self._connection.execute(
            "SELECT event_json FROM notification_audit ORDER BY audit_id"
        ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def __enter__(self) -> SQLiteNotificationLedger:
        return self

    def __exit__(self, _type, _value, _traceback) -> None:
        self.close()


@dataclass
class MockNotificationAdapter:
    channel: Channel
    fixtures: FixtureSet

    def attempt(
        self, notification: Notification, destination_reference: str, number: int
    ) -> MockOutcome:
        """Return a deterministic fixture result without external I/O."""
        expected_prefix = f"synthetic-{self.channel.value}-recipient-"
        if (
            not isinstance(destination_reference, str)
            or not DESTINATION_PATTERN.fullmatch(destination_reference)
            or not destination_reference.startswith(expected_prefix)
        ):
            raise ValueError(
                "Destination must be a channel-matched synthetic reference"
            )
        outcomes = self.fixtures.outcomes.get(self.channel, ())
        if not outcomes:
            raise ValueError("No synthetic outcomes are configured for this channel")
        return outcomes[min(number - 1, len(outcomes) - 1)]


@dataclass
class NotificationOrchestrator:
    config: NotificationConfig
    fixtures: FixtureSet | None = None
    max_attempts: int = 3
    backoff_seconds: tuple[int, ...] = (1, 2)
    sleeper: object = lambda _seconds: None
    audit_events: list[dict[str, object]] = field(default_factory=list)
    ledger: SQLiteNotificationLedger | None = field(default=None, repr=False)
    _receipts: dict[tuple[str, Channel], DeliveryReceipt] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if any(
            value != "mock"
            for value in (
                self.config.mode,
                self.config.email_mode,
                self.config.sms_mode,
            )
        ):
            raise NotificationConfigurationError("Only mock mode is permitted")
        if self.max_attempts != 3 or self.backoff_seconds != (1, 2):
            raise ValueError(
                "Mock retry policy is fixed at three attempts with 1s/2s backoff"
            )
        if not callable(self.sleeper):
            raise ValueError("Mock sleeper must be an injected callable")
        if self.ledger is None and self.config.ledger_path:
            self.ledger = SQLiteNotificationLedger(self.config.ledger_path)
        if self.ledger is not None:
            self._receipts.update(self.ledger.load_receipts())

    def notify(
        self,
        notification: Notification,
        destinations: Mapping[Channel, str] | None = None,
    ) -> list[DeliveryReceipt]:
        """Process only explicit synthetic destinations, atomically if persisted."""
        if not destinations or self.fixtures is None:
            self.audit_events.append(
                {
                    "event": "notification_requested",
                    "event_id": notification.event_id,
                    "severity": notification.severity,
                    "event_code": notification.event_code,
                }
            )
            self.audit_events.append(
                {"event": "no_synthetic_recipients", "event_id": notification.event_id}
            )
            if self.ledger is not None:
                with self.ledger.transaction():
                    self.ledger.record_audit(self.audit_events[-2:])
            return []

        prior_memory = dict(self._receipts)
        prior_audit_count = len(self.audit_events)
        transaction = (
            self.ledger.transaction() if self.ledger is not None else nullcontext()
        )
        try:
            with transaction:
                if self.ledger is not None:
                    # Refresh after obtaining SQLite's writer lock. This is the
                    # cross-process idempotency check, not just an in-memory cache.
                    self._receipts.update(self.ledger.load_receipts())

                for channel, destination in destinations.items():
                    if not isinstance(channel, Channel):
                        raise ValueError("Unsupported notification channel")
                    expected_prefix = f"synthetic-{channel.value}-recipient-"
                    if (
                        not isinstance(destination, str)
                        or not DESTINATION_PATTERN.fullmatch(destination)
                        or not destination.startswith(expected_prefix)
                    ):
                        raise ValueError(
                            "Destination must be a channel-matched synthetic reference"
                        )
                    prior_receipt = self._receipts.get((notification.event_id, channel))
                    if (
                        prior_receipt is not None
                        and prior_receipt.destination_reference != destination
                    ):
                        raise ValueError(
                            "Idempotency conflict: event/channel is already bound "
                            "to a different destination"
                        )

                self.audit_events.append(
                    {
                        "event": "notification_requested",
                        "event_id": notification.event_id,
                        "severity": notification.severity,
                        "event_code": notification.event_code,
                    }
                )
                receipts: list[DeliveryReceipt] = []
                for channel, destination in destinations.items():
                    key = (notification.event_id, channel)
                    if key in self._receipts:
                        self.audit_events.append(
                            {
                                "event": "duplicate_suppressed",
                                "event_id": notification.event_id,
                                "channel": channel.value,
                            }
                        )
                        receipts.append(self._receipts[key])
                        continue

                    adapter = MockNotificationAdapter(channel, self.fixtures)
                    final_outcome: MockOutcome | None = None
                    attempts = 0
                    for attempt_number in range(1, self.max_attempts + 1):
                        attempts = attempt_number
                        self.audit_events.append(
                            {
                                "event": "mock_attempted",
                                "event_id": notification.event_id,
                                "channel": channel.value,
                                "attempt": attempt_number,
                            }
                        )
                        final_outcome = adapter.attempt(
                            notification, destination, attempt_number
                        )
                        self.audit_events.append(
                            {
                                "event": "mock_result",
                                "event_id": notification.event_id,
                                "channel": channel.value,
                                "outcome": final_outcome.value,
                            }
                        )
                        if final_outcome not in TRANSIENT_OUTCOMES:
                            break
                        if attempt_number < self.max_attempts:
                            self.sleeper(self.backoff_seconds[attempt_number - 1])
                    if final_outcome in TRANSIENT_OUTCOMES:
                        final_outcome = MockOutcome.RETRY_EXHAUSTED
                        self.audit_events.append(
                            {
                                "event": "mock_retry_exhausted",
                                "event_id": notification.event_id,
                                "channel": channel.value,
                                "attempts": attempts,
                            }
                        )
                    receipt = DeliveryReceipt(
                        event_id=notification.event_id,
                        channel=channel,
                        destination_reference=destination,
                        status=final_outcome or MockOutcome.REJECTED,
                        attempts=attempts,
                    )
                    self._receipts[key] = receipt
                    if self.ledger is not None:
                        self.ledger.save_receipt(receipt)
                    receipts.append(receipt)

                if self.ledger is not None:
                    self.ledger.record_audit(self.audit_events[prior_audit_count:])
            return receipts
        except BaseException:
            if self.ledger is not None:
                self._receipts = self.ledger.load_receipts()
            else:
                self._receipts = prior_memory
            del self.audit_events[prior_audit_count:]
            raise

    def record_simulated_acknowledgement(
        self, event_id: str, responder_reference: str
    ) -> None:
        """Record a test-only acknowledgement that is never human acknowledgement."""
        if not EVENT_ID_PATTERN.fullmatch(event_id):
            raise ValueError("event_id must be synthetic")
        if responder_reference not in {
            "synthetic-primary-responder",
            "synthetic-backup-responder",
            "synthetic-owner-escalation-role",
        }:
            raise ValueError("Responder must be a known synthetic role")
        event = {
            "event": "human_acknowledgement_simulated",
            "event_id": event_id,
            "responder_reference": responder_reference,
            "simulated": True,
            "display_label": "SIMULATED — NOT DELIVERED",
        }
        if self.ledger is not None:
            with self.ledger.transaction():
                self.ledger.record_audit([event])
        self.audit_events.append(event)

    def redacted_summary(self) -> str:
        """Return status-only output; never render payloads or destination values."""
        counts: dict[str, int] = {}
        for receipt in self._receipts.values():
            counts[receipt.status.value] = counts.get(receipt.status.value, 0) + 1
        details = ", ".join(
            f"{status}={count}" for status, count in sorted(counts.items())
        )
        if not details:
            details = "no synthetic receipts"
        return f"SIMULATED — NOT DELIVERED; {details}"
