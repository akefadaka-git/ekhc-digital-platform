"""Tests for offline sync idempotency, versioning, and encrypted-store contracts."""

from datetime import UTC, datetime
from uuid import uuid4

from django.test import SimpleTestCase

from sync.contracts import (
    EncryptedLocalRecord,
    SyncDecision,
    SyncEnvelope,
    SyncState,
    can_transition_sync_state,
    evaluate_sync,
)


class SyncEvaluationTests(SimpleTestCase):
    def setUp(self):
        self.key = uuid4()
        self.envelope = SyncEnvelope(
            idempotency_key=self.key,
            aggregate_reference="aggregate-ref-001",
            device_reference="device-ref-001",
            base_version=4,
            payload_sha256="a" * 64,
            client_created_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
        )

    def test_matching_version_is_ready_without_applying(self):
        result = evaluate_sync(self.envelope, current_server_version=4)
        self.assertEqual(result.decision, SyncDecision.READY)
        self.assertEqual(result.reason_code, "VERSION_MATCH")

    def test_replayed_idempotency_key_is_not_applied_twice(self):
        result = evaluate_sync(
            self.envelope,
            current_server_version=5,
            applied_idempotency_keys=[self.key],
        )
        self.assertEqual(result.decision, SyncDecision.IDEMPOTENT_REPLAY)
        self.assertEqual(result.reason_code, "ALREADY_APPLIED")

    def test_version_mismatch_is_a_conflict(self):
        result = evaluate_sync(self.envelope, current_server_version=5)
        self.assertEqual(result.decision, SyncDecision.VERSION_CONFLICT)
        self.assertEqual(result.reason_code, "BASE_VERSION_MISMATCH")

    def test_payload_digest_must_be_sha256_hex(self):
        with self.assertRaisesMessage(ValueError, "SHA-256 hex digest"):
            SyncEnvelope(
                idempotency_key=self.key,
                aggregate_reference="aggregate-ref-001",
                device_reference="device-ref-001",
                base_version=4,
                payload_sha256="not-a-digest",
                client_created_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
            )

    def test_boolean_version_is_not_accepted_as_integer(self):
        with self.assertRaisesMessage(TypeError, "base_version must be an integer"):
            SyncEnvelope(
                idempotency_key=self.key,
                aggregate_reference="aggregate-ref-001",
                device_reference="device-ref-001",
                base_version=True,
                payload_sha256="a" * 64,
                client_created_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
            )


class SyncStateTransitionTests(SimpleTestCase):
    def test_normal_queue_and_retry_recovery_transitions(self):
        self.assertTrue(can_transition_sync_state(SyncState.QUEUED, SyncState.IN_FLIGHT))
        self.assertTrue(
            can_transition_sync_state(
                SyncState.IN_FLIGHT, SyncState.RETRYABLE_FAILURE
            )
        )
        self.assertTrue(
            can_transition_sync_state(
                SyncState.RETRYABLE_FAILURE, SyncState.QUEUED
            )
        )

    def test_acknowledged_and_permanent_failure_are_terminal(self):
        self.assertFalse(
            can_transition_sync_state(SyncState.ACKNOWLEDGED, SyncState.QUEUED)
        )
        self.assertFalse(
            can_transition_sync_state(
                SyncState.PERMANENT_FAILURE, SyncState.QUEUED
            )
        )

    def test_conflict_requires_explicit_resolution_before_requeue(self):
        self.assertFalse(
            can_transition_sync_state(SyncState.IN_FLIGHT, SyncState.QUEUED)
        )
        self.assertTrue(
            can_transition_sync_state(SyncState.CONFLICT, SyncState.QUEUED)
        )


class EncryptedLocalRecordTests(SimpleTestCase):
    def test_only_nonempty_ciphertext_is_accepted(self):
        record = EncryptedLocalRecord(
            ciphertext=b"synthetic-ciphertext",
            key_reference="test-key-reference",
            algorithm_suite="test-reviewed-suite",
        )
        self.assertEqual(record.ciphertext, b"synthetic-ciphertext")

    def test_empty_ciphertext_is_rejected(self):
        with self.assertRaisesMessage(ValueError, "ciphertext must be non-empty"):
            EncryptedLocalRecord(
                ciphertext=b"",
                key_reference="test-key-reference",
                algorithm_suite="test-reviewed-suite",
            )
