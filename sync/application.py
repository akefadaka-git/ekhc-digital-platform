"""Transactional synchronization application service and database adapter ports."""

import hashlib
import json
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from audit.events import AuditEvent, AuditOutcome
from identity.references import AccountReference
from security.crypto import EncryptionEnvelope
from sync.contracts import SyncEnvelope


class TrustedClock(Protocol):
    def now(self) -> datetime: ...


@dataclass(frozen=True, slots=True)
class SyncCommand:
    envelope: SyncEnvelope
    actor: AccountReference
    encrypted_payload: EncryptionEnvelope

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, SyncEnvelope):
            raise TypeError("envelope must be a SyncEnvelope.")
        if not isinstance(self.actor, AccountReference):
            raise TypeError("actor must be an AccountReference.")
        if not isinstance(self.encrypted_payload, EncryptionEnvelope):
            raise TypeError("encrypted_payload must be an EncryptionEnvelope.")
        actual_digest = hashlib.sha256(self.encrypted_payload.ciphertext).hexdigest()
        if actual_digest != self.envelope.payload_sha256:
            raise ValueError("ciphertext digest does not match the sync envelope.")
        aad = sync_associated_data(self.envelope)
        if hashlib.sha256(aad).hexdigest() != self.encrypted_payload.aad_sha256:
            raise ValueError(
                "encryption envelope AAD does not bind this sync operation."
            )


@dataclass(frozen=True, slots=True)
class SyncReceipt:
    idempotency_key: UUID
    status: str
    aggregate_reference: str
    resulting_version: int
    reason_code: str
    occurred_at: datetime


class SyncTransaction(Protocol):
    def get_receipt(self, idempotency_key: UUID) -> SyncReceipt | None: ...

    def get_aggregate_version_for_update(self, aggregate_reference: str) -> int: ...

    def apply_aggregate_mutation(
        self,
        aggregate_reference: str,
        expected_version: int,
        encrypted_payload: EncryptionEnvelope,
        occurred_at: datetime,
    ) -> int: ...

    def append_receipt(self, receipt: SyncReceipt) -> None: ...

    def append_audit_event(self, event: AuditEvent) -> None: ...

    def enqueue_outbox(
        self,
        event_id: UUID,
        aggregate_reference: str,
        resulting_version: int,
        occurred_at: datetime,
    ) -> None: ...


class SyncUnitOfWork(Protocol):
    def transaction(self) -> AbstractContextManager[SyncTransaction]: ...


@dataclass(frozen=True, slots=True)
class SyncResult:
    status: str
    resulting_version: int
    reason_code: str
    replayed: bool = False


def apply_sync_command(
    command: SyncCommand, unit_of_work: SyncUnitOfWork, clock: TrustedClock
) -> SyncResult:
    """Apply aggregate, receipt, audit, and outbox changes in one transaction.

    Exactly one trusted time observation is captured for this operation and reused
    for every timestamp written by the transaction.
    """
    if not isinstance(command, SyncCommand):
        raise TypeError("command must be a SyncCommand.")
    occurred_at = clock.now()
    if not isinstance(occurred_at, datetime) or occurred_at.tzinfo is None:
        raise ValueError("trusted clock must return a timezone-aware datetime.")

    envelope = command.envelope
    with unit_of_work.transaction() as transaction:
        existing = transaction.get_receipt(envelope.idempotency_key)
        if existing is not None:
            return SyncResult(
                existing.status,
                existing.resulting_version,
                existing.reason_code,
                replayed=True,
            )

        current_version = transaction.get_aggregate_version_for_update(
            envelope.aggregate_reference
        )
        if current_version != envelope.base_version:
            receipt = SyncReceipt(
                envelope.idempotency_key,
                "conflict",
                envelope.aggregate_reference,
                current_version,
                "BASE_VERSION_MISMATCH",
                occurred_at,
            )
            transaction.append_receipt(receipt)
            transaction.append_audit_event(
                AuditEvent(
                    action="sync.conflict",
                    resource_type="aggregate",
                    resource_reference=envelope.aggregate_reference,
                    occurred_at=occurred_at,
                    correlation_id=envelope.idempotency_key,
                    outcome=AuditOutcome.DENIED,
                    actor=command.actor,
                )
            )
            return SyncResult("conflict", current_version, "BASE_VERSION_MISMATCH")

        new_version = transaction.apply_aggregate_mutation(
            envelope.aggregate_reference,
            current_version,
            command.encrypted_payload,
            occurred_at,
        )
        if new_version != current_version + 1:
            raise RuntimeError("aggregate adapter must advance exactly one version.")

        event = AuditEvent(
            action="sync.applied",
            resource_type="aggregate",
            resource_reference=envelope.aggregate_reference,
            occurred_at=occurred_at,
            correlation_id=envelope.idempotency_key,
            outcome=AuditOutcome.SUCCEEDED,
            actor=command.actor,
        )
        receipt = SyncReceipt(
            envelope.idempotency_key,
            "applied",
            envelope.aggregate_reference,
            new_version,
            "APPLIED",
            occurred_at,
        )
        transaction.append_receipt(receipt)
        transaction.append_audit_event(event)
        transaction.enqueue_outbox(
            event.event_id, envelope.aggregate_reference, new_version, occurred_at
        )
        return SyncResult("applied", new_version, "APPLIED")


def sync_associated_data(envelope: SyncEnvelope) -> bytes:
    """Bind ciphertext to one idempotency key, device, aggregate, and base version."""
    if not isinstance(envelope, SyncEnvelope):
        raise TypeError("envelope must be a SyncEnvelope.")
    fields = [
        "ekhc-sync-v1",
        envelope.aggregate_reference,
        envelope.device_reference,
        str(envelope.base_version),
        str(envelope.idempotency_key),
    ]
    return json.dumps(fields, separators=(",", ":")).encode("utf-8")
