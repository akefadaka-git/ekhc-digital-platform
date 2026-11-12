"""Append-only audit event contracts; no storage or retention is configured."""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol
from uuid import UUID, uuid4

from identity.references import AccountReference

_EVENT_NAME = re.compile(r"^[a-z][a-z0-9_.-]{0,95}$")
_RESOURCE_TYPE = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")


class AuditOutcome(StrEnum):
    SUCCEEDED = "succeeded"
    DENIED = "denied"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """Minimal event facts; payloads, credentials, and arbitrary metadata excluded."""

    action: str
    resource_type: str
    resource_reference: str
    occurred_at: datetime
    correlation_id: UUID
    outcome: AuditOutcome
    actor: AccountReference | None = None
    event_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.action, str) or not _EVENT_NAME.fullmatch(self.action):
            raise ValueError("action must be a normalized event identifier.")
        if not isinstance(self.resource_type, str) or not _RESOURCE_TYPE.fullmatch(
            self.resource_type
        ):
            raise ValueError("resource_type must be a normalized identifier.")
        if (
            not isinstance(self.resource_reference, str)
            or not self.resource_reference
            or self.resource_reference != self.resource_reference.strip()
        ):
            raise ValueError("resource_reference must be non-empty and normalized.")
        if not isinstance(self.occurred_at, datetime) or self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware.")
        if not isinstance(self.correlation_id, UUID) or not isinstance(
            self.event_id, UUID
        ):
            raise TypeError("event_id and correlation_id must be UUID values.")
        if not isinstance(self.outcome, AuditOutcome):
            raise TypeError("outcome must be an AuditOutcome.")
        if self.actor is not None and not isinstance(self.actor, AccountReference):
            raise TypeError("actor must be an AccountReference or None.")


class AppendOnlyAuditSink(Protocol):
    """Write-only contract: no update, delete, query, or retention semantics."""

    def append(self, event: AuditEvent) -> None: ...
