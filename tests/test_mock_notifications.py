"""Tests for fail-closed synthetic notification behavior."""

import socket
import unittest
from unittest.mock import patch

from notifications.mock import (
    ALLOWED_FIXTURE_SET,
    Channel,
    FixtureSet,
    MockOutcome,
    Notification,
    NotificationConfig,
    NotificationConfigurationError,
    NotificationOrchestrator,
)


def config(fixture_set=ALLOWED_FIXTURE_SET):
    env = {
        "EKHC_NOTIFICATION_MODE": "mock",
        "EKHC_EMAIL_MODE": "mock",
        "EKHC_SMS_MODE": "mock",
    }
    if fixture_set is not None:
        env["EKHC_NOTIFICATION_FIXTURE_SET"] = fixture_set
    return NotificationConfig.from_environment(env)


def event():
    return Notification(
        event_id="SYNTH-EVENT-0001",
        severity="HIGH",
        event_code="DEPENDENCY_ADVISORY",
    )


class MockNotificationTests(unittest.TestCase):
    def test_configuration_requires_all_modes_explicitly_mock(self):
        with self.assertRaises(NotificationConfigurationError):
            NotificationConfig.from_environment({})
        with self.assertRaises(NotificationConfigurationError):
            NotificationConfig.from_environment(
                {
                    "EKHC_NOTIFICATION_MODE": "live",
                    "EKHC_EMAIL_MODE": "mock",
                    "EKHC_SMS_MODE": "mock",
                }
            )

    def test_live_provider_credentials_and_unknown_fixtures_are_rejected(self):
        env = {
            "EKHC_NOTIFICATION_MODE": "mock",
            "EKHC_EMAIL_MODE": "mock",
            "EKHC_SMS_MODE": "mock",
            "EKHC_EMAIL_PROVIDER_CREDENTIAL": "must-not-be-used",
        }
        with self.assertRaises(NotificationConfigurationError):
            NotificationConfig.from_environment(env)
        for key in ("EKHC_EMAIL_HOST", "EKHC_SMS_API_URL"):
            unsafe_env = {
                "EKHC_NOTIFICATION_MODE": "mock",
                "EKHC_EMAIL_MODE": "mock",
                "EKHC_SMS_MODE": "mock",
                key: "provider.example.invalid",
            }
            with (
                self.subTest(key=key),
                self.assertRaises(NotificationConfigurationError),
            ):
                NotificationConfig.from_environment(unsafe_env)
        with self.assertRaises(NotificationConfigurationError):
            config("unapproved-fixture")

    def test_missing_fixture_set_has_no_implicit_recipients(self):
        orchestrator = NotificationOrchestrator(config(fixture_set=None))
        self.assertEqual(orchestrator.notify(event()), [])
        self.assertEqual(
            orchestrator.audit_events[-1]["event"], "no_synthetic_recipients"
        )

    def test_email_and_sms_success_are_explicitly_simulated(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        receipts = orchestrator.notify(
            event(),
            {
                Channel.EMAIL: "synthetic-email-recipient-01",
                Channel.SMS: "synthetic-sms-recipient-01",
            },
        )
        self.assertEqual(len(receipts), 2)
        for receipt in receipts:
            self.assertEqual(receipt.status, MockOutcome.ACCEPTED)
            self.assertTrue(receipt.simulated)
            self.assertFalse(receipt.delivery_claim)
            self.assertEqual(receipt.display_label, "SIMULATED — NOT DELIVERED")

    def test_real_or_wrong_channel_destination_is_rejected(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        with self.assertRaises(ValueError):
            orchestrator.notify(event(), {Channel.EMAIL: "person@example.com"})
        with self.assertRaises(ValueError):
            orchestrator.notify(event(), {Channel.SMS: "synthetic-email-recipient-01"})

    def test_transient_outcomes_retry_with_bounded_backoff(self):
        sleeps = []
        fixtures = FixtureSet(
            outcomes={
                Channel.EMAIL: (
                    MockOutcome.TIMEOUT,
                    MockOutcome.UNAVAILABLE,
                    MockOutcome.ACCEPTED,
                )
            }
        )
        orchestrator = NotificationOrchestrator(
            config(), fixtures, sleeper=sleeps.append
        )
        receipt = orchestrator.notify(
            event(), {Channel.EMAIL: "synthetic-email-recipient-01"}
        )[0]
        self.assertEqual(receipt.status, MockOutcome.ACCEPTED)
        self.assertEqual(receipt.attempts, 3)
        self.assertEqual(sleeps, [1, 2])

    def test_retry_exhaustion_is_explicit_and_bounded(self):
        sleeps = []
        fixtures = FixtureSet(outcomes={Channel.SMS: (MockOutcome.UNAVAILABLE,)})
        orchestrator = NotificationOrchestrator(
            config(), fixtures, sleeper=sleeps.append
        )
        receipt = orchestrator.notify(
            event(), {Channel.SMS: "synthetic-sms-recipient-01"}
        )[0]
        self.assertEqual(receipt.status, MockOutcome.RETRY_EXHAUSTED)
        self.assertEqual(receipt.attempts, 3)
        self.assertEqual(sleeps, [1, 2])

    def test_permanent_rejection_is_not_retried(self):
        sleeps = []
        fixtures = FixtureSet(outcomes={Channel.EMAIL: (MockOutcome.REJECTED,)})
        orchestrator = NotificationOrchestrator(
            config(), fixtures, sleeper=sleeps.append
        )
        receipt = orchestrator.notify(
            event(), {Channel.EMAIL: "synthetic-email-recipient-01"}
        )[0]
        self.assertEqual(receipt.status, MockOutcome.REJECTED)
        self.assertEqual(receipt.attempts, 1)
        self.assertEqual(sleeps, [])

    def test_duplicate_event_is_suppressed_per_channel(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        destination = {Channel.EMAIL: "synthetic-email-recipient-01"}
        first = orchestrator.notify(event(), destination)
        second = orchestrator.notify(event(), destination)
        self.assertEqual(first, second)
        attempted = [
            record
            for record in orchestrator.audit_events
            if record["event"] == "mock_attempted"
        ]
        self.assertEqual(len(attempted), 1)
        self.assertIn(
            "duplicate_suppressed",
            [item["event"] for item in orchestrator.audit_events],
        )

    def test_simulated_acknowledgement_is_never_human_acknowledgement(self):
        orchestrator = NotificationOrchestrator(config())
        orchestrator.record_simulated_acknowledgement(
            "SYNTH-EVENT-0001", "synthetic-primary-responder"
        )
        event_record = orchestrator.audit_events[-1]
        self.assertEqual(event_record["event"], "human_acknowledgement_simulated")
        self.assertIs(event_record["simulated"], True)
        self.assertEqual(event_record["display_label"], "SIMULATED — NOT DELIVERED")
        with self.assertRaises(ValueError):
            orchestrator.record_simulated_acknowledgement(
                "SYNTH-EVENT-0001", "real-person"
            )

    def test_summary_and_audit_do_not_include_destination_or_payload(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        orchestrator.notify(event(), {Channel.EMAIL: "synthetic-email-recipient-01"})
        summary = orchestrator.redacted_summary()
        self.assertIn("SIMULATED — NOT DELIVERED", summary)
        self.assertNotIn("synthetic-email-recipient-01", summary)
        self.assertNotIn("person@", str(orchestrator.audit_events))

    def test_retry_policy_cannot_be_expanded(self):
        with self.assertRaises(ValueError):
            NotificationOrchestrator(config(), max_attempts=4)
        with self.assertRaises(ValueError):
            NotificationOrchestrator(config(), backoff_seconds=(1, 2, 3))

    def test_mock_execution_performs_no_network_or_dns_calls(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        with (
            patch.object(
                socket, "socket", side_effect=AssertionError("network blocked")
            ),
            patch.object(
                socket, "getaddrinfo", side_effect=AssertionError("DNS blocked")
            ),
        ):
            receipts = orchestrator.notify(
                event(),
                {
                    Channel.EMAIL: "synthetic-email-recipient-01",
                    Channel.SMS: "synthetic-sms-recipient-01",
                },
            )
        self.assertEqual(len(receipts), 2)


if __name__ == "__main__":
    unittest.main()
