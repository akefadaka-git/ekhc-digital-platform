"""Security tests for the non-persistent session evaluation contract."""

from datetime import UTC, datetime, timedelta

from django.test import SimpleTestCase

from identity.references import AccountReference
from security.sessions import (
    SessionDecision,
    SessionObservation,
    SessionPolicy,
    evaluate_session,
)

NOW = datetime(2026, 11, 12, 12, 0, tzinfo=UTC)


class SessionPolicyTests(SimpleTestCase):
    def setUp(self):
        self.policy = SessionPolicy(
            idle_timeout=timedelta(minutes=15),
            absolute_timeout=timedelta(hours=8),
        )
        self.observation = SessionObservation(
            account=AccountReference("account-test-01"),
            issued_at=NOW - timedelta(minutes=5),
            last_activity_at=NOW - timedelta(minutes=2),
            absolute_expires_at=NOW + timedelta(hours=7),
            authenticated=True,
        )

    def test_valid_observation_is_accepted(self):
        result = evaluate_session(self.observation, self.policy, now=NOW)
        self.assertEqual(result.decision, SessionDecision.ACCEPT)
        self.assertEqual(result.reason_code, "SESSION_VALID")

    def test_revoked_session_is_denied(self):
        observation = SessionObservation(
            **{**self.observation.__dict__, "revoked": True}
        )
        result = evaluate_session(observation, self.policy, now=NOW)
        self.assertEqual(result.decision, SessionDecision.DENY)
        self.assertEqual(result.reason_code, "SESSION_REVOKED")

    def test_unauthenticated_observation_is_denied(self):
        observation = SessionObservation(
            account=self.observation.account,
            issued_at=self.observation.issued_at,
            last_activity_at=self.observation.last_activity_at,
            absolute_expires_at=self.observation.absolute_expires_at,
            authenticated=False,
        )
        self.assertEqual(
            evaluate_session(observation, self.policy, now=NOW).reason_code,
            "SESSION_NOT_AUTHENTICATED",
        )

    def test_idle_timeout_is_enforced_at_boundary(self):
        observation = SessionObservation(
            account=self.observation.account,
            issued_at=NOW - timedelta(minutes=20),
            last_activity_at=NOW - timedelta(minutes=15),
            absolute_expires_at=NOW + timedelta(hours=1),
            authenticated=True,
        )
        result = evaluate_session(observation, self.policy, now=NOW)
        self.assertEqual(result.reason_code, "SESSION_IDLE_TIMEOUT")

    def test_absolute_timeout_is_enforced_at_boundary(self):
        observation = SessionObservation(
            account=self.observation.account,
            issued_at=NOW - timedelta(hours=8),
            last_activity_at=NOW - timedelta(minutes=1),
            absolute_expires_at=NOW,
            authenticated=True,
        )
        result = evaluate_session(observation, self.policy, now=NOW)
        self.assertEqual(result.reason_code, "SESSION_ABSOLUTE_TIMEOUT")

    def test_future_activity_fails_closed(self):
        observation = SessionObservation(
            account=self.observation.account,
            issued_at=NOW - timedelta(minutes=1),
            last_activity_at=NOW + timedelta(seconds=1),
            absolute_expires_at=NOW + timedelta(hours=1),
            authenticated=True,
        )
        self.assertEqual(
            evaluate_session(observation, self.policy, now=NOW).reason_code,
            "SESSION_TIME_OBSERVATION_INVALID",
        )

    def test_naive_timestamps_are_rejected(self):
        with self.assertRaisesMessage(ValueError, "timezone-aware"):
            SessionObservation(
                account=AccountReference("account-test-02"),
                issued_at=datetime(2026, 11, 12),
                last_activity_at=NOW,
                absolute_expires_at=NOW + timedelta(hours=1),
                authenticated=True,
            )

    def test_policy_cannot_disable_session_rotation(self):
        with self.assertRaisesMessage(ValueError, "rotation after authentication"):
            SessionPolicy(
                idle_timeout=timedelta(minutes=10),
                absolute_timeout=timedelta(hours=1),
                rotate_on_authentication=False,
            )
