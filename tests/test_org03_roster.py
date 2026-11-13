"""Synthetic-only tests for ORG-03 roster validation."""

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.org03_roster import is_operationally_ready, validate_roster


TEMPLATE = (
    Path(__file__).parents[1]
    / "docs"
    / "operations"
    / "org-03-roster-template.synthetic.json"
)


class Org03RosterValidationTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    def test_published_template_is_structurally_valid_but_not_ready(self):
        result = validate_roster(self.document)
        self.assertEqual([], result["errors"])
        self.assertTrue(result["blockers"])
        self.assertFalse(is_operationally_ready(result))

    def test_same_person_cannot_be_primary_and_backup(self):
        document = deepcopy(self.document)
        document["roster"]["primary"]["responder_ref"] = "SYNTHETIC-RESPONDER-1"
        document["roster"]["backup"]["responder_ref"] = "SYNTHETIC-RESPONDER-1"
        result = validate_roster(document)
        self.assertIn(
            "primary and backup must be distinct individuals", result["errors"]
        )
        self.assertFalse(is_operationally_ready(result))

    def test_approved_policy_targets_are_immutable(self):
        document = deepcopy(self.document)
        document["policy"]["acknowledgement_targets"]["critical_elapsed_hours"] = 1
        result = validate_roster(document)
        self.assertIn(
            "acknowledgement targets differ from the Owner-approved policy",
            result["errors"],
        )

    def test_invalid_timestamp_is_rejected(self):
        document = deepcopy(self.document)
        document["roster"]["primary"]["accepted_at_utc"] = "tomorrow"
        result = validate_roster(document)
        self.assertIn(
            "primary.accepted_at_utc must be an ISO-8601 UTC timestamp ending in Z",
            result["errors"],
        )

    def test_active_status_without_evidence_does_not_enable_readiness(self):
        document = deepcopy(self.document)
        document["roster"]["primary"]["status"] = "ACTIVE"
        document["roster"]["backup"]["status"] = "ACTIVE"
        document["roster"]["owner_or_delegate"]["status"] = "ACTIVE"
        result = validate_roster(document)
        self.assertTrue(result["blockers"])
        self.assertFalse(is_operationally_ready(result))

    def test_activation_flags_must_remain_false(self):
        document = deepcopy(self.document)
        document["activation"]["production_operation_authorized"] = True
        result = validate_roster(document)
        self.assertIn(
            "activation.production_operation_authorized must remain false "
            "in this synthetic-only increment",
            result["errors"],
        )

    def test_missing_roster_object_fails_closed(self):
        document = deepcopy(self.document)
        document["roster"] = None
        result = validate_roster(document)
        self.assertTrue(result["errors"])
        self.assertFalse(is_operationally_ready(result))


if __name__ == "__main__":
    unittest.main()
