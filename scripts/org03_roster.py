"""Fail-closed validation for the public, synthetic ORG-03 roster template.

This module validates structure and operational readiness separately. It never
loads restricted identity/contact records and never sends notifications.
"""

import datetime
import typing

ACTIVE = "ACTIVE"


def _is_utc_timestamp(value: typing.Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def validate_roster(document: dict[str, typing.Any]) -> dict[str, list[str]]:
    """Return deterministic schema errors and readiness blockers."""
    errors: list[str] = []
    blockers: list[str] = []

    if document.get("classification") != "SYNTHETIC_TEMPLATE_NO_PERSONAL_DATA":
        errors.append(
            "classification must identify a synthetic, no-personal-data record"
        )

    policy = document.get("policy")
    roster = document.get("roster")
    routing = document.get("routing")
    activation = document.get("activation")
    sections = (policy, roster, routing, activation)
    if not all(isinstance(item, dict) for item in sections):
        return {
            "errors": errors
            + ["policy, roster, routing and activation must be objects"],
            "blockers": ["roster cannot be evaluated until its structure is valid"],
        }

    targets = policy.get("acknowledgement_targets", {})
    expected_targets = {
        "critical_elapsed_hours": 4,
        "high_business_days": 1,
        "medium_business_days": 2,
        "low_informational_business_days": 3,
    }
    if targets != expected_targets:
        errors.append("acknowledgement targets differ from the Owner-approved policy")

    primary = roster.get("primary")
    backup = roster.get("backup")
    authority = roster.get("owner_or_delegate")
    assignments = (primary, backup, authority)
    if not all(isinstance(item, dict) for item in assignments):
        return {
            "errors": errors
            + ["primary, backup and owner_or_delegate must be objects"],
            "blockers": ["all three authority slots must be structurally present"],
        }

    for role in ("primary", "backup"):
        entry = roster[role]
        required_fields = (
            "responder_ref",
            "authorization_ref",
            "restricted_contact_ref",
            "accepted_at_utc",
            "effective_from_utc",
            "effective_until_utc",
            "coverage_ref",
        )
        for field in required_fields:
            if not entry.get(field):
                blockers.append(f"{role}.{field} is not evidenced")
        if entry.get("status") != ACTIVE:
            blockers.append(f"{role} assignment is not ACTIVE")
        timestamp_fields = (
            "accepted_at_utc",
            "effective_from_utc",
            "effective_until_utc",
        )
        for field in timestamp_fields:
            value = entry.get(field)
            if value and not _is_utc_timestamp(value):
                errors.append(
                    f"{role}.{field} must be an ISO-8601 UTC timestamp ending in Z"
                )

    primary_ref = primary.get("responder_ref")
    backup_ref = backup.get("responder_ref")
    if primary_ref and backup_ref and primary_ref == backup_ref:
        errors.append("primary and backup must be distinct individuals")

    authority_fields = (
        "authority_ref",
        "delegation_scope_ref",
        "restricted_contact_ref",
    )
    for field in authority_fields:
        if not authority.get(field):
            blockers.append(f"owner_or_delegate.{field} is not evidenced")
    if authority.get("status") != ACTIVE:
        blockers.append("Owner/delegate escalation assignment is not ACTIVE")
    authority_accepted = authority.get("accepted_at_utc")
    if authority_accepted and not _is_utc_timestamp(authority_accepted):
        errors.append(
            "owner_or_delegate.accepted_at_utc must be an ISO-8601 UTC "
            "timestamp ending in Z"
        )

    if policy.get("business_time_convention") != "APPROVED":
        blockers.append("business-time convention is not approved")
    if not policy.get("timezone") or policy.get("timezone") == "NOT_APPROVED":
        blockers.append("coverage timezone is not approved")
    if not policy.get("working_days"):
        blockers.append("working days are not configured")
    if not policy.get("coverage_window"):
        blockers.append("daily coverage window is not configured")
    if not policy.get("holiday_calendar_ref"):
        blockers.append("holiday calendar evidence is absent")

    route_fields = ("primary_route_ref", "backup_route_ref", "escalation_route_ref")
    for field in route_fields:
        if not routing.get(field):
            blockers.append(f"routing.{field} is not configured")
    if routing.get("status") != "CONFIGURED":
        blockers.append("notification routing is not CONFIGURED")

    activation_fields = (
        "rehearsal_authorized",
        "production_notifications_authorized",
        "production_operation_authorized",
        "merge_authorized",
        "deployment_authorized",
    )
    for field in activation_fields:
        if activation.get(field) is not False:
            errors.append(
                f"activation.{field} must remain false in this synthetic-only increment"
            )

    if errors:
        blockers.append("structural validation failed; routing must remain disabled")

    return {"errors": sorted(set(errors)), "blockers": sorted(set(blockers))}


def is_operationally_ready(result: dict[str, list[str]]) -> bool:
    """Only an error-free roster with no missing evidence is ready."""
    return not result["errors"] and not result["blockers"]
