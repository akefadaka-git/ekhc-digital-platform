"""Durable audit storage ports and verifiable event-chain primitives."""

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from audit.events import AuditEvent
from audit.records import DocumentVersion

_GENESIS_DIGEST = "0" * 64


@dataclass(frozen=True, slots=True)
class AuditChainEntry:
    sequence: int
    previous_digest: str
    event: AuditEvent
    digest: str

    def __post_init__(self) -> None:
        if isinstance(self.sequence, bool) or not isinstance(self.sequence, int):
            raise TypeError("sequence must be an integer.")
        if self.sequence < 1:
            raise ValueError("sequence must be positive.")
        for name in ("previous_digest", "digest"):
            value = getattr(self, name)
            if not isinstance(value, str) or len(value) != 64:
                raise ValueError(f"{name} must be a 64-character digest.")


def canonical_event_digest(event: AuditEvent, previous_digest: str) -> str:
    """Hash canonical event fields and predecessor digest for tamper evidence."""
    if not isinstance(event, AuditEvent):
        raise TypeError("event must be an AuditEvent.")
    if (
        not isinstance(previous_digest, str)
        or len(previous_digest) != 64
        or any(character not in "0123456789abcdef" for character in previous_digest)
    ):
        raise ValueError("previous_digest must be lowercase SHA-256 hex.")
    payload = {
        "event_id": str(event.event_id),
        "actor": event.actor.value if event.actor else None,
        "action": event.action,
        "resource_type": event.resource_type,
        "resource_reference": event.resource_reference,
        "occurred_at": event.occurred_at.isoformat(),
        "correlation_id": str(event.correlation_id),
        "outcome": event.outcome.value,
        "previous_digest": previous_digest,
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def verify_audit_chain(
    entries: tuple[AuditChainEntry, ...],
    *,
    expected_head_sequence: int | None = None,
    expected_head_digest: str | None = None,
) -> bool:
    """Verify the chain, optionally against an independently trusted head checkpoint.

    A checkpoint detects tail truncation. Without one, a valid prefix is
    indistinguishable from a complete chain using hash links alone.
    """
    if (expected_head_sequence is None) != (expected_head_digest is None):
        raise ValueError("head sequence and digest must be supplied together.")
    if expected_head_sequence is not None:
        if (
            isinstance(expected_head_sequence, bool)
            or not isinstance(expected_head_sequence, int)
            or expected_head_sequence < 0
        ):
            raise ValueError("expected head sequence must be a non-negative integer.")
        if (
            not isinstance(expected_head_digest, str)
            or len(expected_head_digest) != 64
            or any(
                character not in "0123456789abcdef"
                for character in expected_head_digest
            )
        ):
            raise ValueError("expected head digest must be lowercase SHA-256 hex.")

    previous = _GENESIS_DIGEST
    for expected_sequence, entry in enumerate(entries, start=1):
        if entry.sequence != expected_sequence or entry.previous_digest != previous:
            return False
        if canonical_event_digest(entry.event, previous) != entry.digest:
            return False
        previous = entry.digest

    if expected_head_sequence is not None:
        return len(entries) == expected_head_sequence and previous == expected_head_digest
    return True


class AuditEventRepository(Protocol):
    """Transactional append/read port; application adapters expose no mutation."""

    def append(self, event: AuditEvent, occurred_at: datetime) -> AuditChainEntry: ...

    def read_after(self, sequence: int, limit: int) -> tuple[AuditChainEntry, ...]: ...

    def verify_chain(self) -> bool: ...


class DocumentMetadataRepository(Protocol):
    """Append-only versions and compare-and-swap manifest updates."""

    def append_version(
        self, document_reference: str, version: DocumentVersion
    ) -> None: ...

    def compare_and_swap_current_version(
        self, document_reference: str, expected_version: int, new_version: int
    ) -> bool: ...

    def get_current_version(self, document_reference: str) -> int | None: ...
