"""Tests for fail-closed synthetic notification behavior and durable ledger."""

import socket
import stat
import tempfile
import unittest
from pathlib import Path
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
    SQLiteNotificationLedger,
)


def config(fixture_set=ALLOWED_FIXTURE_SET, ledger_path=None):
    env = {
        "EKHC_NOTIFICATION_MODE": "mock",
        "EKHC_EMAIL_MODE": "mock",
        "EKHC_SMS_MODE": "mock",
    }
    if fixture_set is not None:
        env["EKHC_NOTIFICATION_FIXTURE_SET"] = fixture_set
    if ledger_path is not None:
        env["EKHC_NOTIFICATION_LEDGER_PATH"] = str(ledger_path)
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

    def test_ledger_path_must_be_local(self):
        with self.assertRaises(NotificationConfigurationError):
            config(ledger_path="https://provider.example.invalid/ledger")

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

    def test_duplicate_event_with_changed_destination_is_rejected(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        orchestrator.notify(event(), {Channel.EMAIL: "synthetic-email-recipient-01"})
        with self.assertRaisesRegex(ValueError, "Idempotency conflict"):
            orchestrator.notify(
                event(), {Channel.EMAIL: "synthetic-email-recipient-02"}
            )
        self.assertEqual(len(orchestrator._receipts), 1)
        receipt = orchestrator._receipts[(event().event_id, Channel.EMAIL)]
        self.assertEqual(receipt.destination_reference, "synthetic-email-recipient-01")

    def test_destination_mapping_is_preflighted_before_any_attempt(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        with self.assertRaisesRegex(ValueError, "channel-matched synthetic reference"):
            orchestrator.notify(
                event(),
                {
                    Channel.EMAIL: "synthetic-email-recipient-01",
                    Channel.SMS: "synthetic-email-recipient-02",
                },
            )
        self.assertEqual(orchestrator._receipts, {})
        self.assertEqual(orchestrator.audit_events, [])

    def test_existing_destination_conflict_is_preflighted_atomically(self):
        orchestrator = NotificationOrchestrator(config(), FixtureSet.accepted())
        orchestrator.notify(event(), {Channel.SMS: "synthetic-sms-recipient-01"})
        prior_receipts = dict(orchestrator._receipts)
        prior_audit = list(orchestrator.audit_events)
        with self.assertRaisesRegex(ValueError, "Idempotency conflict"):
            orchestrator.notify(
                event(),
                {
                    Channel.EMAIL: "synthetic-email-recipient-01",
                    Channel.SMS: "synthetic-sms-recipient-02",
                },
            )
        self.assertEqual(orchestrator._receipts, prior_receipts)
        self.assertEqual(orchestrator.audit_events, prior_audit)

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

    def test_sqlite_ledger_persists_receipts_and_suppresses_restart_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state" / "mock-ledger.sqlite3"
            first = NotificationOrchestrator(
                config(ledger_path=path), FixtureSet.accepted()
            )
            first_receipts = first.notify(
                event(), {Channel.EMAIL: "synthetic-email-recipient-01"}
            )
            first.ledger.close()

            second = NotificationOrchestrator(
                config(ledger_path=path), FixtureSet.accepted()
            )
            second_receipts = second.notify(
                event(), {Channel.EMAIL: "synthetic-email-recipient-01"}
            )
            self.assertEqual(second_receipts, first_receipts)
            self.assertEqual(
                [item["event"] for item in second.ledger.load_audit_events()].count(
                    "mock_attempted"
                ),
                1,
            )
            self.assertIn(
                "duplicate_suppressed",
                [item["event"] for item in second.ledger.load_audit_events()],
            )
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            second.ledger.close()

    def test_sqlite_ledger_rejects_changed_destination_after_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mock-ledger.sqlite3"
            first = NotificationOrchestrator(
                config(ledger_path=path), FixtureSet.accepted()
            )
            first.notify(event(), {Channel.EMAIL: "synthetic-email-recipient-01"})
            first.ledger.close()

            second = NotificationOrchestrator(
                config(ledger_path=path), FixtureSet.accepted()
            )
            with self.assertRaisesRegex(ValueError, "Idempotency conflict"):
                second.notify(event(), {Channel.EMAIL: "synthetic-email-recipient-02"})
            self.assertEqual(len(second._receipts), 1)
            second.ledger.close()

    def test_sqlite_ledger_rolls_back_all_channels_on_processing_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mock-ledger.sqlite3"
            fixtures = FixtureSet(outcomes={Channel.EMAIL: (MockOutcome.ACCEPTED,)})
            orchestrator = NotificationOrchestrator(config(ledger_path=path), fixtures)
            with self.assertRaisesRegex(ValueError, "No synthetic outcomes"):
                orchestrator.notify(
                    event(),
                    {
                        Channel.EMAIL: "synthetic-email-recipient-01",
                        Channel.SMS: "synthetic-sms-recipient-01",
                    },
                )
            self.assertEqual(orchestrator._receipts, {})
            self.assertEqual(orchestrator.audit_events, [])
            self.assertEqual(orchestrator.ledger.load_receipts(), {})
            self.assertEqual(orchestrator.ledger.load_audit_events(), [])
            orchestrator.ledger.close()

    def test_sqlite_ledger_persists_simulated_acknowledgement_as_simulated(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mock-ledger.sqlite3"
            orchestrator = NotificationOrchestrator(config(ledger_path=path))
            orchestrator.record_simulated_acknowledgement(
                "SYNTH-EVENT-0001", "synthetic-primary-responder"
            )
            stored = orchestrator.ledger.load_audit_events()
            self.assertEqual(len(stored), 1)
            self.assertIs(stored[0]["simulated"], True)
            self.assertEqual(stored[0]["display_label"], "SIMULATED — NOT DELIVERED")
            orchestrator.ledger.close()

    def test_sqlite_ledger_rejects_non_simulated_receipts(self):
        from notifications.mock import DeliveryReceipt

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mock-ledger.sqlite3"
            with SQLiteNotificationLedger(str(path)) as ledger:
                with ledger.transaction():
                    receipt = DeliveryReceipt(
                        event_id="SYNTH-EVENT-0001",
                        channel=Channel.EMAIL,
                        destination_reference="synthetic-email-recipient-01",
                        status=MockOutcome.ACCEPTED,
                        attempts=1,
                        delivery_claim=True,
                    )
                    with self.assertRaisesRegex(
                        ValueError, "Only explicitly simulated receipts"
                    ):
                        ledger.save_receipt(receipt)


if __name__ == "__main__":
    unittest.main()
