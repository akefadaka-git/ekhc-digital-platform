"""Boundary tests for the synthetic-only restricted-record policy harness."""

import unittest

from scripts.org03_synthetic_access_policy import (
    AccessDenied,
    SyntheticPrincipal,
    SyntheticRecord,
    authorize,
)


class Org03SyntheticAccessPolicyTests(unittest.TestCase):
    def setUp(self):
        self.record = SyntheticRecord(
            "SYNTHETIC-RECORD-01",
            "SYNTHETIC_RESTRICTED_TEST_RECORD",
            frozenset({"summary", "status"}),
        )
        self.custodian = SyntheticPrincipal(
            "SYNTHETIC-PRINCIPAL-01",
            "SYNTHETIC_CUSTODIAN",
            frozenset({"SYNTHETIC-RECORD-01"}),
        )

    def test_anonymous_access_is_denied(self):
        with self.assertRaises(AccessDenied):
            authorize(None, self.record, "record.read")

    def test_unknown_role_is_denied_by_default(self):
        unknown = SyntheticPrincipal(
            "SYNTHETIC-UNKNOWN-01", "UNDEFINED_ROLE", frozenset({"SYNTHETIC-RECORD-01"})
        )
        with self.assertRaises(AccessDenied):
            authorize(unknown, self.record, "record.read")

    def test_inactive_or_revoked_principal_is_denied(self):
        revoked = SyntheticPrincipal(
            self.custodian.principal_ref,
            self.custodian.role,
            self.custodian.allowed_record_refs,
            active=False,
        )
        with self.assertRaises(AccessDenied):
            authorize(revoked, self.record, "record.read")

    def test_cross_record_reference_is_denied(self):
        other = SyntheticRecord(
            "SYNTHETIC-RECORD-02",
            "SYNTHETIC_RESTRICTED_TEST_RECORD",
            frozenset({"summary"}),
        )
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, other, "record.read")

    def test_least_privilege_denies_unassigned_action(self):
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, self.record, "record.export")

    def test_field_level_disclosure_is_limited(self):
        with self.assertRaises(AccessDenied):
            authorize(
                self.custodian,
                self.record,
                "record.read",
                requested_fields={"summary", "private_contact"},
            )

    def test_auditor_is_read_only(self):
        auditor = SyntheticPrincipal(
            "SYNTHETIC-AUDITOR-01",
            "SYNTHETIC_AUDITOR",
            frozenset({"SYNTHETIC-RECORD-01"}),
        )
        authorize(auditor, self.record, "record.read", requested_fields={"summary"})
        with self.assertRaises(AccessDenied):
            authorize(auditor, self.record, "record.update", requested_fields={"status"})

    def test_non_synthetic_principal_is_rejected(self):
        external = SyntheticPrincipal(
            "EXTERNAL-IDENTITY",
            "SYNTHETIC_CUSTODIAN",
            frozenset({"SYNTHETIC-RECORD-01"}),
            synthetic=False,
        )
        with self.assertRaises(AccessDenied):
            authorize(external, self.record, "record.read")

    def test_omitted_or_empty_field_scope_is_denied(self):
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, self.record, "record.read")
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, self.record, "record.read", requested_fields=set())

    def test_read_permission_does_not_grant_update_fields(self):
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, self.record, "record.update", requested_fields={"summary"})

    def test_update_projection_is_limited_to_status(self):
        self.assertEqual(
            frozenset({"status"}),
            authorize(self.custodian, self.record, "record.update", requested_fields={"status"}),
        )

    def test_unknown_fields_fail_closed(self):
        with self.assertRaises(AccessDenied):
            authorize(self.custodian, self.record, "record.read", requested_fields={"unknown"})


if __name__ == "__main__":
    unittest.main()
