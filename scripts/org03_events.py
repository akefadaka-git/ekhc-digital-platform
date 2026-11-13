"""Pure, append-only ORG-03 acknowledgement and escalation transitions.

This state machine records synthetic event facts only. It does not deliver
notifications, identify real responders, or authorize operational actions.
"""

import copy
import datetime
import typing


INITIAL_STATE = "RECEIVED"
VALID_PRIORITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}


class TransitionError(ValueError):
    """Raised when an event is unauthorized, malformed, or out of sequence."""


def _valid_utc(value: typing.Any) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return True


def new_alert(
    alert_id: str, priority: str, received_at_utc: str
) -> dict[str, typing.Any]:
    """Create an immutable-by-convention alert state with an initial event."""
    if (
        not alert_id
        or priority not in VALID_PRIORITIES
        or not _valid_utc(received_at_utc)
    ):
        raise TransitionError("alert ID, priority or UTC timestamp is invalid")
    return {
        "alert_id": alert_id,
        "priority": priority,
        "status": INITIAL_STATE,
        "next_sequence": 2,
        "history": [
            {
                "sequence": 1,
                "event": "RECEIVED",
                "at_utc": received_at_utc,
                "actor_role": "SYSTEM",
                "actor_ref": "SYNTHETIC-SYSTEM",
            }
        ],
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

    if name in {
        "DELIVERY_CONFIRMED",
        "DELIVERY_FAILED",
        "PRIMARY_ACK_DEADLINE_MISSED",
        "BACKUP_ACK_DEADLINE_MISSED",
    }:
        if actor_role != "SYSTEM" or actor_ref != "SYNTHETIC-SYSTEM":
            raise TransitionError(
                "system transition requires the synthetic system actor"
            )

    if name == "DELIVERY_CONFIRMED":
        if current not in {"RECEIVED", "DELIVERY_PENDING"}:
            raise TransitionError("delivery confirmation is not valid from this state")
        next_status = "AWAITING_HUMAN_ACK"
    elif name == "DELIVERY_FAILED":
        if current not in {"RECEIVED", "DELIVERY_PENDING"}:
            raise TransitionError("delivery failure is not valid from this state")
        next_status = "DELIVERY_UNCONFIRMED"
    elif name == "HUMAN_ACKNOWLEDGED" or name == "HUMAN_UNABLE_TO_ACCEPT":
        expected = {
            "PRIMARY_SECURITY_OPERATIONS": ("primary", "AWAITING_HUMAN_ACK"),
            "BACKUP_SECURITY_OPERATIONS": ("backup", "BACKUP_ROUTED"),
        }.get(actor_role)
        if expected is None or current != expected[1]:
            raise TransitionError(
                "human acknowledgement is invalid for this role or state"
            )
        if authorized_responder_refs.get(expected[0]) != actor_ref:
            raise TransitionError(
                "actor is not the currently authorized responder for this role"
            )
        if name == "HUMAN_ACKNOWLEDGED":
            if event.get("disposition") != "ACCEPTED":
                raise TransitionError("acknowledgement must explicitly be ACCEPTED")
            next_status = "ACKNOWLEDGED"
        else:
            if event.get("disposition") != "UNABLE_TO_ACCEPT":
                raise TransitionError("decline must explicitly be UNABLE_TO_ACCEPT")
            if actor_role == "PRIMARY_SECURITY_OPERATIONS":
                next_status = "BACKUP_ROUTED"
            else:
                next_status = "AUTHORITY_ESCALATED"
    elif name == "PRIMARY_ACK_DEADLINE_MISSED":
        if current != "AWAITING_HUMAN_ACK":
            raise TransitionError("primary deadline event is invalid from this state")
        next_status = "BACKUP_ROUTED"
    elif name == "BACKUP_ACK_DEADLINE_MISSED":
        if current != "BACKUP_ROUTED":
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

    result = copy.deepcopy(state)
    result["history"].append(copy.deepcopy(event))
    result["status"] = next_status
    result["next_sequence"] += 1
    return result
