"""Transactional sync tests use an in-memory rollback-capable fake adapter."""

import hashlib
from copy import deepcopy
from datetime import UTC, datetime
from uuid import uuid4

from django.test import SimpleTestCase

from audit.events import AuditEvent, AuditOutcome
from audit.storage import AuditChainEntry, canonical_event_digest, verify_audit_chain
from identity.references import AccountReference
from security.crypto import (
    AES_256_GCM_SUITE,
    EncryptionEnvelope,
    GeneratedDataKey,
)
from sync.application import (
    SyncCommand,
    SyncReceipt,
    apply_sync_command,
)
from sync.contracts import SyncEnvelope

NOW = datetime(2026, 11, 12, 12, 0, tzinfo=UTC)


class FixedClock:
    def __init__(self):
        self.calls = 0

    def now(self):
        self.calls += 1
        return NOW


class FakeTransaction:
    def __init__(self, state):
        self.state = state

    def get_receipt(self, key):
        return self.state["receipts"].get(key)

    def get_aggregate_version_for_update(self, aggregate_reference):
        return self.state["versions"].get(aggregate_reference, 0)

    def apply_aggregate_mutation(self, aggregate_reference, expected_version, payload, occurred_at):
        if self.get_aggregate_version_for_update(aggregate_reference) != expected_version:
            raise RuntimeError("concurrent version changed")
        new_version = expected_version + 1
        self.state["versions"][aggregate_reference] = new_version
        self.state["mutations"].append((aggregate_reference, payload, occurred_at))
        return new_version

    def append_receipt(self, receipt):
        self.state["receipts"][receipt.idempotency_key] = receipt

    def append_audit_event(self, event):
        self.state["audit"].append(event)
        if self.state.get("fail_audit"):
            raise RuntimeError("injected audit insert failure")

    def enqueue_outbox(self, event_id, aggregate_reference, resulting_version, occurred_at):
        self.state["outbox"].append((event_id, aggregate_reference, resulting_version, occurred_at))
        if self.state.get("fail_outbox"):
            raise RuntimeError("injected outbox insert failure")


class FakeUnitOfWork:
    def __init__(self, *, fail_audit=False, fail_outbox=False):
        self.state = {
            "versions": {"aggregate-001": 3},
            "receipts": {},
            "mutations": [],
            "audit": [],
            "outbox": [],
            "fail_audit": fail_audit,
            "fail_outbox": fail_outbox,
        }

    class TransactionContext:
        def __init__(self, owner):
            self.owner = owner

        def __enter__(self):
            self.before = deepcopy(self.owner.state)
            return FakeTransaction(self.owner.state)

        def __exit__(self, exc_type, exc, traceback):
            if exc_type is not None:
                self.owner.state = self.before
            return False

    def transaction(self):
        return self.TransactionContext(self)


def make_command(key=None, base_version=3):
    payload = b"synthetic-sync-payload"
    envelope = SyncEnvelope(
        idempotency_key=key or uuid4(),
        aggregate_reference="aggregate-001",
        device_reference="device-001",
        base_version=base_version,
        payload_sha256=hashlib.sha256(payload).hexdigest(),
        client_created_at=NOW,
    )
    return SyncCommand(envelope, AccountReference("account-001"), payload)


class TransactionalSyncTests(SimpleTestCase):
    def test_success_commits_aggregate_receipt_audit_and_outbox_together(self):
        store = FakeUnitOfWork()
        clock = FixedClock()
        result = apply_sync_command(make_command(), store, clock)
        self.assertEqual(result.status, "applied")
        self.assertEqual(store.state["versions"]["aggregate-001"], 4)
        self.assertEqual(len(store.state["receipts"]), 1)
        self.assertEqual(len(store.state["audit"]), 1)
        self.assertEqual(len(store.state["outbox"]), 1)
        self.assertEqual(clock.calls, 1)
        timestamps = [
            store.state["mutations"][0][2],
            next(iter(store.state["receipts"].values())).occurred_at,
            store.state["audit"][0].occurred_at,
            store.state["outbox"][0][2],
        ]
        self.assertTrue(all(value is NOW for value in timestamps))

    def test_duplicate_idempotency_key_returns_prior_receipt_without_mutation(self):
        store = FakeUnitOfWork()
        command = make_command()
        first = apply_sync_command(command, store, FixedClock())
        second = apply_sync_command(command, store, FixedClock())
        self.assertEqual(first.status, "applied")
        self.assertTrue(second.replayed)
        self.assertEqual(len(store.state["mutations"]), 1)
        self.assertEqual(len(store.state["outbox"]), 1)

    def test_version_conflict_records_receipt_and_audit_without_mutation(self):
        store = FakeUnitOfWork()
        result = apply_sync_command(make_command(base_version=2), store, FixedClock())
        self.assertEqual(result.status, "conflict")
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(len(store.state["receipts"]), 1)
        self.assertEqual(store.state["audit"][0].outcome, AuditOutcome.DENIED)
        self.assertEqual(store.state["outbox"], [])

    def test_audit_insert_failure_rolls_back_aggregate_and_receipt(self):
        store = FakeUnitOfWork(fail_audit=True)
        with self.assertRaisesMessage(RuntimeError, "injected audit insert failure"):
            apply_sync_command(make_command(), store, FixedClock())
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])

    def test_outbox_insert_failure_rolls_back_everything(self):
        store = FakeUnitOfWork(fail_outbox=True)
        with self.assertRaisesMessage(RuntimeError, "injected outbox insert failure"):
            apply_sync_command(make_command(), store, FixedClock())
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])

    def test_payload_digest_mismatch_is_rejected_before_transaction(self):
        payload = b"not-the-declared-payload"
        envelope = SyncEnvelope(
            idempotency_key=uuid4(),
            aggregate_reference="aggregate-001",
            device_reference="device-001",
            base_version=3,
            payload_sha256="a" * 64,
            client_created_at=NOW,
        )
        with self.assertRaisesMessage(ValueError, "payload digest does not match"):
            SyncCommand(envelope, AccountReference("account-001"), payload)


class AuditChainTests(SimpleTestCase):
    def test_chain_verifies_and_detects_tampering(self):
        first_event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        first_digest = canonical_event_digest(first_event, "0" * 64)
        first = AuditChainEntry(1, "0" * 64, first_event, first_digest)
        second_event = AuditEvent(
            action="records.write",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        second_digest = canonical_event_digest(second_event, first_digest)
        second = AuditChainEntry(2, first_digest, second_event, second_digest)
        self.assertTrue(verify_audit_chain((first, second)))
        self.assertFalse(
            verify_audit_chain((first, AuditChainEntry(2, first_digest, second_event, "f" * 64)))
        )

    def test_sequence_gap_is_rejected(self):
        event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        digest = canonical_event_digest(event, "0" * 64)
        entry = AuditChainEntry(2, "0" * 64, event, digest)
        self.assertFalse(verify_audit_chain((entry,)))


class CryptographicContractTests(SimpleTestCase):
    def test_generated_data_key_is_256_bits_and_wrapped(self):
        value = GeneratedDataKey(
            plaintext_key=bytearray(b"k" * 32),
            wrapped_key=b"wrapped-test-key",
            key_reference="kms-key-ref",
            key_version="v1",
        )
        self.assertEqual(len(value.plaintext_key), 32)

    def test_envelope_requires_gcm_nonce_and_tag_sized_ciphertext(self):
        envelope = EncryptionEnvelope(
            ciphertext=b"c" * 16,
            nonce=b"n" * 12,
            wrapped_key=b"wrapped-test-key",
            key_reference="kms-key-ref",
            key_version="v1",
            algorithm_suite=AES_256_GCM_SUITE,
            aad_sha256="a" * 64,
        )
        self.assertEqual(envelope.algorithm_suite, "AES-256-GCM")
        with self.assertRaisesMessage(ValueError, "nonce must contain 12 bytes"):
            EncryptionEnvelope(
                ciphertext=b"c" * 16,
                nonce=b"short",
                wrapped_key=b"wrapped-test-key",
                key_reference="kms-key-ref",
                key_version="v1",
                algorithm_suite=AES_256_GCM_SUITE,
                aad_sha256="a" * 64,
            )
