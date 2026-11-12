"""Provider-neutral offline synchronization contracts; no local persistence."""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID

_HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class SyncDecision(StrEnum):
    READY = "ready"
    IDEMPOTENT_REPLAY = "idempotent_replay"
    VERSION_CONFLICT = "version_conflict"


@dataclass(frozen=True, slots=True)
class SyncEnvelope:
    """Metadata-only envelope; the business payload is not stored in this object."""

    idempotency_key: UUID
    aggregate_reference: str
    device_reference: str
    base_version: int
    payload_sha256: str
    client_created_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.idempotency_key, UUID):
            raise TypeError("idempotency_key must be a UUID.")
        for name in ("aggregate_reference", "device_reference"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(f"{name} must be non-empty and normalized.")
        if isinstance(self.base_version, bool) or not isinstance(
            self.base_version, int
        ):
            raise TypeError("base_version must be an integer.")
        if self.base_version < 0:
            raise ValueError("base_version must not be negative.")
        if not isinstance(self.payload_sha256, str) or not _HEX_SHA256.fullmatch(
            self.payload_sha256
        ):
            raise ValueError("payload_sha256 must be a lowercase SHA-256 hex digest.")
        if (
            not isinstance(self.client_created_at, datetime)
            or self.client_created_at.tzinfo is None
        ):
            raise ValueError("client_created_at must be timezone-aware.")


@dataclass(frozen=True, slots=True)
class SyncEvaluation:
    decision: SyncDecision
    reason_code: str


def evaluate_sync(
    envelope: SyncEnvelope,
    *,
    current_server_version: int,
    applied_idempotency_keys: Iterable[UUID] = (),
) -> SyncEvaluation:
    """Classify a sync request without applying it or mutating server state."""
    if not isinstance(envelope, SyncEnvelope):
        raise TypeError("envelope must be a SyncEnvelope.")
    if (
        isinstance(current_server_version, bool)
        or not isinstance(current_server_version, int)
        or current_server_version < 0
    ):
        raise ValueError("current_server_version must be a non-negative integer.")
    if envelope.idempotency_key in set(applied_idempotency_keys):
        return SyncEvaluation(SyncDecision.IDEMPOTENT_REPLAY, "ALREADY_APPLIED")
    if envelope.base_version != current_server_version:
        return SyncEvaluation(SyncDecision.VERSION_CONFLICT, "BASE_VERSION_MISMATCH")
    return SyncEvaluation(SyncDecision.READY, "VERSION_MATCH")


class SyncState(StrEnum):
    QUEUED = "queued"
    IN_FLIGHT = "in_flight"
    ACKNOWLEDGED = "acknowledged"
    CONFLICT = "conflict"
    RETRYABLE_FAILURE = "retryable_failure"
    PERMANENT_FAILURE = "permanent_failure"


_ALLOWED_TRANSITIONS = {
    SyncState.QUEUED: {SyncState.IN_FLIGHT},
    SyncState.IN_FLIGHT: {
        SyncState.ACKNOWLEDGED,
        SyncState.CONFLICT,
        SyncState.RETRYABLE_FAILURE,
        SyncState.PERMANENT_FAILURE,
    },
    SyncState.RETRYABLE_FAILURE: {SyncState.QUEUED},
    SyncState.CONFLICT: {SyncState.QUEUED},
    SyncState.ACKNOWLEDGED: set(),
    SyncState.PERMANENT_FAILURE: set(),
}


def can_transition_sync_state(current: SyncState, target: SyncState) -> bool:
    """Return whether a state transition is permitted; performs no mutation."""
    if not isinstance(current, SyncState) or not isinstance(target, SyncState):
        raise TypeError("current and target must be SyncState values.")
    return target in _ALLOWED_TRANSITIONS[current]


@dataclass(frozen=True, slots=True)
class EncryptedLocalRecord:
    """Ciphertext-only storage contract; plaintext and key material are excluded."""

    ciphertext: bytes
    key_reference: str
    algorithm_suite: str

    def __post_init__(self) -> None:
        if not isinstance(self.ciphertext, bytes) or not self.ciphertext:
            raise ValueError("ciphertext must be non-empty bytes.")
        if (
            not isinstance(self.key_reference, str)
            or not self.key_reference
            or self.key_reference != self.key_reference.strip()
        ):
            raise ValueError("key_reference must be a non-empty opaque reference.")
        if (
            not isinstance(self.algorithm_suite, str)
            or not self.algorithm_suite
            or self.algorithm_suite != self.algorithm_suite.strip()
        ):
            raise ValueError("algorithm_suite must identify a reviewed suite.")


class EncryptedLocalStore(Protocol):
    """Local adapter accepts ciphertext records only; key management is external."""

    def put(self, record_reference: str, record: EncryptedLocalRecord) -> None: ...

    def get(self, record_reference: str) -> EncryptedLocalRecord | None: ...

    def delete(self, record_reference: str) -> None: ...
