"""Tests for non-persistent separation of person and account references."""

from dataclasses import FrozenInstanceError

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

    def test_identity_link_rejects_account_in_person_slot(self):
        with self.assertRaisesMessage(TypeError, "person must be a PersonReference"):
            IdentityLink(
                person=AccountReference("same-opaque-value"),
                account=AccountReference("account-001"),
            )

    def test_identity_link_rejects_person_in_account_slot(self):
        with self.assertRaisesMessage(TypeError, "account must be an AccountReference"):
            IdentityLink(
                person=PersonReference("person-001"),
                account=PersonReference("same-opaque-value"),
            )

    def test_matching_string_values_do_not_create_a_link(self):
        person = PersonReference("same-value")
        account = AccountReference("same-value")
        self.assertIsNone(getattr(person, "account", None))
        self.assertIsNone(getattr(account, "person", None))

    def test_references_are_immutable(self):
        person = PersonReference("person-001")
        with self.assertRaises(FrozenInstanceError):
            person.value = "person-002"

    def test_reference_rejects_empty_value(self):
        with self.assertRaisesMessage(ValueError, "must be non-empty"):
            PersonReference("")

    def test_reference_rejects_whitespace(self):
        with self.assertRaisesMessage(ValueError, "must not contain whitespace"):
            AccountReference("account 001")

    def test_reference_rejects_overlong_value(self):
        with self.assertRaisesMessage(ValueError, "must not exceed 128 characters"):
            PersonReference("p" * 129)
