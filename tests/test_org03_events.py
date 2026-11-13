"""Synthetic-only acknowledgement and escalation state-machine tests."""
from __future__ import annotations

import unittest
from copy import deepcopy

from scripts.org03_events import TransitionError, apply_event, new_alert


AUTH = {
    "primary": "SYNTHETIC-PRIMARY-01",
    "backup": "SYNTHETIC-BACKUP-01",
    "owner_or_delegate": "SYNTHETIC-OWNER-01",
}


def event(sequence, name, role="SYSTEM", actor="SYNTHETIC-SYSTEM", **extra):
    return {
        "sequence": sequence,
        "event": name,
        "at_utc": f"2026-11-13T07:0{sequence}:00Z",
        "actor_role": role,
        "actor_ref": actor,
        **extra,
    }


class Org03AcknowledgementTransitionTests(unittest.TestCase):
    def setUp(self):
        self.state = new_alert("SYNTHETIC-ALERT-01", "HIGH", "2026-11-13T07:00:00Z")
        self.state = apply_event(
            self.state,
            event(2, "DELIVERY_CONFIRMED"),
            authorized_responder_refs=AUTH,
        )

    def test_primary_acceptance_records_acknowledged_state(self):
        result = apply_event(
            self.state,
            event(
                3,
                "HUMAN_ACKNOWLEDGED",
                "PRIMARY_SECURITY_OPERATIONS",
                AUTH["primary"],
                disposition="ACCEPTED",
            ),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("ACKNOWLEDGED", result["status"])
        self.assertEqual(3, len(result["history"]))
        self.assertEqual("AWAITING_HUMAN_ACK", self.state["status"])

    def test_primary_decline_routes_to_backup(self):
        result = apply_event(
            self.state,
            event(
                3,
                "HUMAN_UNABLE_TO_ACCEPT",
                "PRIMARY_SECURITY_OPERATIONS",
                AUTH["primary"],
                disposition="UNABLE_TO_ACCEPT",
            ),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("BACKUP_ROUTED", result["status"])

    def test_backup_acceptance_acknowledges_after_routing(self):
        backup_routed = apply_event(
            self.state,
            event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        result = apply_event(
            backup_routed,
            event(
                4,
                "HUMAN_ACKNOWLEDGED",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="ACCEPTED",
            ),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("ACKNOWLEDGED", result["status"])

    def test_missed_primary_deadline_routes_to_backup(self):
        result = apply_event(
            self.state,
            event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("BACKUP_ROUTED", result["status"])

    def test_backup_decline_escalates_to_owner(self):
        backup_routed = apply_event(
            self.state,
            event(
                3,
                "HUMAN_UNABLE_TO_ACCEPT",
                "PRIMARY_SECURITY_OPERATIONS",
                AUTH["primary"],
                disposition="UNABLE_TO_ACCEPT",
            ),
            authorized_responder_refs=AUTH,
        )
        result = apply_event(
            backup_routed,
            event(
                4,
                "HUMAN_UNABLE_TO_ACCEPT",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="UNABLE_TO_ACCEPT",
            ),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("AUTHORITY_ESCALATED", result["status"])

    def test_missed_backup_deadline_escalates_to_owner(self):
        backup_routed = apply_event(
            self.state,
            event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        result = apply_event(
            backup_routed,
            event(4, "BACKUP_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("AUTHORITY_ESCALATED", result["status"])

    def test_owner_acknowledgement_completes_acknowledgement_not_closure(self):
        escalated = apply_event(
            apply_event(
                self.state,
                event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
                authorized_responder_refs=AUTH,
            ),
            event(4, "BACKUP_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        result = apply_event(
            escalated,
            event(
                5,
                "OWNER_AUTHORITY_ACKNOWLEDGED",
                "OWNER_OR_DELEGATE",
                AUTH["owner_or_delegate"],
                disposition="ACCEPTED",
            ),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("ACKNOWLEDGED", result["status"])
        self.assertNotEqual("CLOSED", result["status"])

    def test_unauthorized_responder_cannot_acknowledge(self):
        with self.assertRaises(TransitionError):
            apply_event(
                self.state,
                event(
                    3,
                    "HUMAN_ACKNOWLEDGED",
                    "PRIMARY_SECURITY_OPERATIONS",
                    "SYNTHETIC-UNAUTHORIZED",
                    disposition="ACCEPTED",
                ),
                authorized_responder_refs=AUTH,
            )

    def test_bot_delivery_receipt_cannot_be_human_ack(self):
        with self.assertRaises(TransitionError):
            apply_event(
                self.state,
                event(
                    3,
                    "HUMAN_ACKNOWLEDGED",
                    "SYSTEM",
                    "SYNTHETIC-SYSTEM",
                    disposition="ACCEPTED",
                ),
                authorized_responder_refs=AUTH,
            )

    def test_ack_before_confirmed_delivery_is_rejected(self):
        initial = new_alert(
            "SYNTHETIC-ALERT-02", "CRITICAL", "2026-11-13T07:00:00Z"
        )
        with self.assertRaises(TransitionError):
            apply_event(
                initial,
                event(
                    2,
                    "HUMAN_ACKNOWLEDGED",
                    "PRIMARY_SECURITY_OPERATIONS",
                    AUTH["primary"],
                    disposition="ACCEPTED",
                ),
                authorized_responder_refs=AUTH,
            )

    def test_duplicate_or_out_of_order_sequence_is_rejected(self):
        bad = event(4, "PRIMARY_ACK_DEADLINE_MISSED")
        with self.assertRaises(TransitionError):
            apply_event(self.state, bad, authorized_responder_refs=AUTH)

    def test_failed_delivery_never_claims_human_acknowledgement(self):
        initial = new_alert(
            "SYNTHETIC-ALERT-03", "MEDIUM", "2026-11-13T07:00:00Z"
        )
        result = apply_event(
            initial,
            event(2, "DELIVERY_FAILED"),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("DELIVERY_UNCONFIRMED", result["status"])
        with self.assertRaises(TransitionError):
            apply_event(
                result,
                event(
                    3,
                    "HUMAN_ACKNOWLEDGED",
                    "PRIMARY_SECURITY_OPERATIONS",
                    AUTH["primary"],
                    disposition="ACCEPTED",
                ),
                authorized_responder_refs=AUTH,
            )

    def test_history_is_append_only_and_prior_state_is_unchanged(self):
        original = deepcopy(self.state)
        result = apply_event(
            self.state,
            event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            authorized_responder_refs=AUTH,
        )
        self.assertEqual(original, self.state)
        self.assertEqual(2, len(self.state["history"]))
        self.assertEqual(3, len(result["history"]))


if __name__ == "__main__":
    unittest.main()
