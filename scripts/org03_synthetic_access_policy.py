"""Synthetic-only deny-by-default policy harness; not production authentication.

The caller-supplied principal is a test fixture, not a verified identity.
This module intentionally has no integration with Django, sessions, tokens,
institutional directories, or restricted records.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SyntheticPrincipal:
    principal_ref: str
    role: str
    allowed_record_refs: frozenset[str]
    active: bool = True
    synthetic: bool = True


@dataclass(frozen=True)
class SyntheticRecord:
    record_ref: str
    classification: str
    fields: frozenset[str]


ROLE_ACTIONS = {
    "SYNTHETIC_CUSTODIAN": frozenset({"record.read", "record.update"}),
    "SYNTHETIC_AUDITOR": frozenset({"record.read", "audit.read"}),
}


class AccessDenied(PermissionError):
    """Raised whenever a synthetic access request is not explicitly allowed."""


def authorize(
    principal: SyntheticPrincipal | None,
    record: SyntheticRecord,
    action: str,
    *,
    requested_fields: set[str] | None = None,
) -> None:
    """Apply explicit synthetic role, record-scope and field-scope checks."""
    if principal is None:
        raise AccessDenied("anonymous access denied")
    if not principal.synthetic or not principal.active or not principal.principal_ref:
        raise AccessDenied("principal is absent, inactive, or not synthetic")
    allowed_actions = ROLE_ACTIONS.get(principal.role, frozenset())
    if action not in allowed_actions:
        raise AccessDenied("role is not authorized for this action")
    if record.classification != "SYNTHETIC_RESTRICTED_TEST_RECORD":
        raise AccessDenied("record classification is not in the test boundary")
    if record.record_ref not in principal.allowed_record_refs:
        raise AccessDenied("principal is not scoped to this record")
    if requested_fields is not None and not requested_fields.issubset(record.fields):
        raise AccessDenied("requested fields exceed the record field allow-list")
