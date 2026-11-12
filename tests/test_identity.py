"""Tests for non-persistent separation of person and account references."""

from django.test import SimpleTestCase

from identity.references import AccountReference, IdentityLink, PersonReference


class IdentityReferenceTests(SimpleTestCase):
    def test_person_and_account_are_distinct_types(self):
        person = PersonReference("person-ref-001")
        account = AccountReference("person-ref-001")

        self.assertNotEqual(type(person), type(account))
        self.assertNotEqual(person, account)

    def test_identity_link_requires_explicit_typed_references(self):
        link = IdentityLink(
            person=PersonReference("person-001"),
            account=AccountReference("account-001"),
        )

        self.assertEqual(link.person.value, "person-001")
        self.assertEqual(link.account.value, "account-001")

    def test_identity_link_rejects_untyped_values(self):
        with self.assertRaisesMessage(TypeError, "person must be a PersonReference"):
            IdentityLink(person="person-001", account=AccountReference("account-001"))

    def test_reference_rejects_empty_value(self):
        with self.assertRaisesMessage(ValueError, "must be non-empty"):
            PersonReference("")

    def test_reference_rejects_whitespace(self):
        with self.assertRaisesMessage(ValueError, "must not contain whitespace"):
            AccountReference("account 001")

    def test_reference_rejects_overlong_value(self):
        with self.assertRaisesMessage(ValueError, "must not exceed 128 characters"):
            PersonReference("p" * 129)
