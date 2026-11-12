"""Tests for the authorization boundary's fail-closed default."""

from django.test import SimpleTestCase

from identity.references import AccountReference
from security.policy import (
    AuthorizationRequest,
    Decision,
    evaluate_authorization,
)


class AuthorizationBoundaryTests(SimpleTestCase):
    def test_unconfigured_policy_denies_access(self):
        request = AuthorizationRequest(
            actor=AccountReference("account-001"),
            action="read",
            resource_type="document",
            resource_reference="document-001",
        )

        result = evaluate_authorization(request)

        self.assertEqual(result.decision, Decision.DENY)
        self.assertEqual(
            result.reason_code,
            "AUTHORIZATION_POLICY_NOT_CONFIGURED",
        )

    def test_unconfigured_policy_also_denies_scoped_request(self):
        request = AuthorizationRequest(
            actor=AccountReference("account-001"),
            action="update",
            resource_type="record",
            resource_reference="record-001",
            scope_reference="opaque-scope-001",
        )

        self.assertEqual(evaluate_authorization(request).decision, Decision.DENY)

    def test_request_rejects_missing_action(self):
        with self.assertRaisesMessage(ValueError, "action must be a non-empty string"):
            AuthorizationRequest(
                actor=AccountReference("account-001"),
                action="",
                resource_type="document",
                resource_reference="document-001",
            )

    def test_request_rejects_wrong_actor_type(self):
        with self.assertRaisesMessage(TypeError, "actor must be an AccountReference"):
            AuthorizationRequest(
                actor="account-001",
                action="read",
                resource_type="document",
                resource_reference="document-001",
            )

    def test_request_rejects_blank_scope(self):
        with self.assertRaisesMessage(ValueError, "scope_reference must be absent"):
            AuthorizationRequest(
                actor=AccountReference("account-001"),
                action="read",
                resource_type="document",
                resource_reference="document-001",
                scope_reference=" ",
            )

    def test_evaluator_rejects_untyped_request(self):
        with self.assertRaisesMessage(TypeError, "request must be an AuthorizationRequest"):
            evaluate_authorization(object())
