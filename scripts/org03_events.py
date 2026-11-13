"""Pure, append-only ORG-03 acknowledgement and escalation transitions.

This state machine records synthetic event facts only. It does not deliver
notifications, identify real responders, or authorize operational actions.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any


INITIAL_STATE = "RECEIVED"
VALID_PRIORITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
VALID_DISPOSITIONS = {"ACCEPTED", "UNABLE_TO_ACCEPT"}
VALID_ROLES = {"PRIMARY_SECURITY_OPERATIONS", "BACKUP_SECURITY_OPERATIONS", "OWNER_OR_DELEGATE"}


class TransitionError(ValueError):
    """Raised when an event is unauthorized, malformed, or out of sequence."""


def _valid_utc(value: Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def new_alert(alert_id: str, priority: str, received_at_utc: str) -> dict[str, Any]:
    """Create an immutable-by-convention alert state with an initial event."""
    if not alert_id or priority not in VALID_PRIORITIES or not _valid_utc(received_at_utc):
        raise TransitionError("alert ID, priority or UTC timestamp is invalid")
    return {
        "alert_id": alert_id,
        "priority": priority,
        "status": INITIAL_STATE,
        "next_sequence": 2,
        "history": [{
            "sequence": 1,
            "event": "RECEIVED",
            "at_utc": received_at_utc,
            "actor_role": "SYSTEM",
            "actor_ref": "SYNTHETIC-SYSTEM",
        }],
    }


def apply_event(
    state: dict[str, Any],
    event: dict[str, Any],
    *,
    authorized_responder_refs: dict[str, str],
) -> dict[str, Any]:
    """Validate one event and return a new state with an appended history row."""
    if not isinstance(state, dict) or not isinstance(event, dict):
        raise TransitionError("state and event must be objects")
    if not _valid_utc(event.get("at_utc")):
        raise TransitionError("event timestamp must be ISO-8601 UTC ending in Z")
    if event.get("sequence") != state.get("next_sequence"):
        raise TransitionError("event sequence must be the next monotonic sequence")
    actor_role = event.get("actor_role")
    actor_ref = event.get("actor_ref")
    if not isinstance(actor_role, str) or not isinstance(actor_ref, str):
        raise TransitionError("actor role and opaque actor reference are required")

    current = state.get("status")
    name = event.get("event")
    next_status: str

    if name == "DELIVERY_CONFIRMED":
        if current not in {"RECEIVED", "DELIVERY_PENDING"} or actor_role != "SYSTEM":
            raise TransitionError("delivery confirmation is not valid from this state")
        next_status = "AWAITING_HUMAN_ACK"
    elif name == "DELIVERY_FAILED":
        if current not in {"RECEIVED", "DELIVERY_PENDING"} or actor_role != "SYSTEM":
            raise TransitionError("delivery failure is not valid from this state")
        next_status = "DELIVERY_UNCONFIRMED"
    elif name in {"HUMAN_ACKNOWLEDGED", "HUMAN_UNABLE_TO_ACCEPT"}:
        if current != "AWAITING_HUMAN_ACK":
            raise TransitionError("human acknowledgement requires confirmed delivery")
        expected = {
            "PRIMARY_SECURITY_OPERATIONS": "primary",
            "BACKUP_SECURITY_OPERATIONS": "backup",
            "OWNER_OR_DELEGATE": "owner_or_delegate",
        }.get(actor_role)
        if expected is None or authorized_responder_refs.get(expected) != actor_ref:
            raise TransitionError("actor is not the currently authorized responder for this role")
        if name == "HUMAN_ACKNOWLEDGED":
            if event.get("disposition") != "ACCEPTED":
                raise TransitionError("acknowledgement must explicitly be ACCEPTED")
            next_status = "ACKNOWLEDGED"
        else:
            if event.get("disposition") != "UNABLE_TO_ACCEPT":
                raise TransitionError("decline must explicitly be UNABLE_TO_ACCEPT")
            if actor_role == "PRIMARY_SECURITY_OPERATIONS":
                next_status = "BACKUP_ROUTED"
            elif actor_role == "BACKUP_SECURITY_OPERATIONS":
                next_status = "AUTHORITY_ESCALATED"
            else:
                raise TransitionError("Owner/delegate cannot decline into another escalation tier")
    elif name == "PRIMARY_ACK_DEADLINE_MISSED":
        if current != "AWAITING_HUMAN_ACK" or actor_role != "SYSTEM":
            raise TransitionError("primary deadline event is invalid from this state")
        next_status = "BACKUP_ROUTED"
    elif name == "BACKUP_ACK_DEADLINE_MISSED":
        if current != "BACKUP_ROUTED" or actor_role != "SYSTEM":
            raise TransitionError("backup deadline event is invalid from this state")
        next_status = "AUTHORITY_ESCALATED"
    elif name == "OWNER_AUTHORITY_ACKNOWLEDGED":
        if current != "AUTHORITY_ESCALATED" or actor_role != "OWNER_OR_DELEGATE":
            raise TransitionError("authority acknowledgement requires escalation state")
        if authorized_responder_refs.get("owner_or_delegate") != actor_ref:
            raise TransitionError("actor is not the current Owner/delegate")
        if event.get("disposition") != "ACCEPTED":
            raise TransitionError("authority acknowledgement must be ACCEPTED")
        next_status = "ACKNOWLEDGED"
    else:
        raise TransitionError("unsupported ORG-03 event")

    result = deepcopy(state)
    result["history"].append(deepcopy(event))
    result["status"] = next_status
    result["next_sequence"] += 1
    return result
