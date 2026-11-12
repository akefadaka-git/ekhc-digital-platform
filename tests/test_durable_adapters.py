"""Durable adapter contract tests with rollback and crypto test doubles."""

import hashlib
from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from django.test import SimpleTestCase

from audit.events import AuditEvent, AuditOutcome
from audit.storage import (
    AuditChainEntry,
    canonical_event_digest,
    verify_audit_chain,
)
from identity.references import AccountReference
from security.crypto import (
    AES_256_GCM_SUITE,
    EncryptionEnvelope,
    GeneratedDataKey,
    decrypt_payload,
    encrypt_payload,
)
from sync.application import (
    SyncCommand,
    apply_sync_command,
    sync_associated_data,
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

    def apply_aggregate_mutation(
        self, aggregate_reference, expected_version, encrypted_payload, occurred_at
    ):
        if (
            self.get_aggregate_version_for_update(aggregate_reference)
            != expected_version
        ):
            raise RuntimeError("concurrent version changed")
        new_version = expected_version + 1
        self.state["versions"][aggregate_reference] = new_version
        self.state["mutations"].append(
            (aggregate_reference, encrypted_payload, occurred_at)
        )
        return new_version

    def append_receipt(self, receipt):
        self.state["receipts"][receipt.idempotency_key] = receipt

    def append_audit_event(self, event):
        self.state["audit"].append(event)
        if self.state.get("fail_audit"):
            raise RuntimeError("injected audit insert failure")

    def enqueue_outbox(
        self, event_id, aggregate_reference, resulting_version, occurred_at
    ):
        self.state["outbox"].append(
            (event_id, aggregate_reference, resulting_version, occurred_at)
        )
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


def make_command(key=None, base_version=3, *, aad_override=None):
    idempotency_key = key or uuid4()
    ciphertext = b"synthetic-encrypted-payload" + (b"t" * 16)
    envelope = SyncEnvelope(
        idempotency_key=idempotency_key,
        aggregate_reference="aggregate-001",
        device_reference="device-001",
        base_version=base_version,
        payload_sha256=hashlib.sha256(ciphertext).hexdigest(),
        client_created_at=NOW,
    )
    aad = sync_associated_data(envelope)
    encrypted_payload = EncryptionEnvelope(
        ciphertext=ciphertext,
        nonce=b"n" * 12,
        wrapped_key=b"wrapped-test-key",
        key_reference="kms-test-key",
        key_version="v1",
        algorithm_suite=AES_256_GCM_SUITE,
        aad_sha256=aad_override or hashlib.sha256(aad).hexdigest(),
    )
    return SyncCommand(envelope, AccountReference("account-001"), encrypted_payload)


class TransactionalSyncTests(SimpleTestCase):
    def test_success_commits_aggregate_receipt_audit_and_outbox_together(self):
        store = FakeUnitOfWork()
        clock = FixedClock()
        command = make_command()
        result = apply_sync_command(command, store, clock)
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
            store.state["outbox"][0][3],
        ]
        self.assertTrue(all(value is NOW for value in timestamps))
        self.assertIs(store.state["mutations"][0][1], command.encrypted_payload)
        self.assertNotIn(command.encrypted_payload.ciphertext, store.state["outbox"])

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

    def test_ciphertext_digest_mismatch_is_rejected_before_transaction(self):
        command = make_command()
        bad_envelope = EncryptionEnvelope(
            ciphertext=b"tampered-ciphertext" + (b"t" * 16),
            nonce=command.encrypted_payload.nonce,
            wrapped_key=command.encrypted_payload.wrapped_key,
            key_reference=command.encrypted_payload.key_reference,
            key_version=command.encrypted_payload.key_version,
            algorithm_suite=command.encrypted_payload.algorithm_suite,
            aad_sha256=command.encrypted_payload.aad_sha256,
        )
        with self.assertRaisesMessage(ValueError, "ciphertext digest"):
            SyncCommand(command.envelope, command.actor, bad_envelope)

    def test_aad_must_bind_the_sync_operation(self):
        with self.assertRaisesMessage(ValueError, "AAD does not bind"):
            make_command(aad_override="f" * 64)


class FakeKeyProvider:
    def __init__(self):
        self.generated = None

    def generate_data_key(self, key_reference):
        self.generated = GeneratedDataKey(
            bytearray(b"k" * 32), b"wrapped-key", key_reference, "v1"
        )
        return self.generated

    def unwrap_data_key(self, wrapped_key, key_reference):
        return bytearray(b"k" * 32)

    def rewrap_data_key(self, wrapped_key, old_key_reference, new_key_reference):
        return b"rewrapped-key", "v2"


class ReversibleTestCipher:
    """Test-only reversible stand-in; never use as a production cipher."""

    def encrypt(self, plaintext, key, nonce, associated_data):
        transformed = bytes(
            value ^ key[index % len(key)] for index, value in enumerate(plaintext)
        )
        return transformed + (b"t" * 16)

    def decrypt(self, ciphertext, key, nonce, associated_data):
        transformed = ciphertext[:-16]
        return bytes(
            value ^ key[index % len(key)] for index, value in enumerate(transformed)
        )


class EnvelopeEncryptionTests(SimpleTestCase):
    def setUp(self):
        self.provider = FakeKeyProvider()
        self.cipher = ReversibleTestCipher()
        self.aad = b"document:doc-001:version:1"

    def test_encrypt_creates_envelope_and_zeroizes_transient_data_key(self):
        envelope = encrypt_payload(
            b"synthetic document bytes",
            self.provider,
            self.cipher,
            key_reference="kms-test-key",
            associated_data=self.aad,
        )
        self.assertEqual(envelope.algorithm_suite, AES_256_GCM_SUITE)
        self.assertEqual(len(envelope.nonce), 12)
        self.assertEqual(self.provider.generated.plaintext_key, bytearray(32))

    def test_decrypt_requires_exact_authenticated_data(self):
        envelope = encrypt_payload(
            b"synthetic document bytes",
            self.provider,
            self.cipher,
            key_reference="kms-test-key",
            associated_data=self.aad,
        )
        plaintext = decrypt_payload(
            envelope, self.provider, self.cipher, associated_data=self.aad
        )
        self.assertEqual(plaintext, b"synthetic document bytes")

    def test_decrypt_rejects_aad_substitution(self):
        envelope = encrypt_payload(
            b"synthetic document bytes",
            self.provider,
            self.cipher,
            key_reference="kms-test-key",
            associated_data=self.aad,
        )
        with self.assertRaisesMessage(ValueError, "does not match"):
            decrypt_payload(
                envelope,
                self.provider,
                self.cipher,
                associated_data=b"document:other:version:1",
            )


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
            verify_audit_chain(
                (
                    first,
                    AuditChainEntry(2, first_digest, second_event, "f" * 64),
                )
            )
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

    def test_changed_event_field_is_detected_as_tampering(self):
        event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        digest = canonical_event_digest(event, "0" * 64)
        original = AuditChainEntry(1, "0" * 64, event, digest)
        altered_event = replace(event, action="records.delete")
        altered = AuditChainEntry(1, "0" * 64, altered_event, digest)
        self.assertTrue(verify_audit_chain((original,)))
        self.assertFalse(verify_audit_chain((altered,)))

    def test_predecessor_digest_substitution_is_detected(self):
        first_event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        first_digest = canonical_event_digest(first_event, "0" * 64)
        second_event = AuditEvent(
            action="records.write",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        second_digest = canonical_event_digest(second_event, first_digest)
        first = AuditChainEntry(1, "0" * 64, first_event, first_digest)
        tampered_second = AuditChainEntry(2, "f" * 64, second_event, second_digest)
        self.assertFalse(verify_audit_chain((first, tampered_second)))

    def test_reordered_audit_entries_are_rejected(self):
        events = []
        previous = "0" * 64
        for action, sequence in (("records.read", 1), ("records.write", 2)):
            event = AuditEvent(
                action=action,
                resource_type="document",
                resource_reference="doc-001",
                occurred_at=NOW,
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
            )
            digest = canonical_event_digest(event, previous)
            events.append(AuditChainEntry(sequence, previous, event, digest))
            previous = digest
        self.assertFalse(verify_audit_chain(tuple(reversed(events))))

    def test_invalid_previous_digest_is_rejected(self):
        event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        with self.assertRaisesMessage(ValueError, "lowercase SHA-256"):
            canonical_event_digest(event, "Z" * 64)


class SyncFailureEdgeTests(SimpleTestCase):
    def test_naive_clock_is_rejected_before_transaction(self):
        class NaiveClock:
            def now(self):
                return datetime(2026, 11, 12, 12, 0)

        store = FakeUnitOfWork()
        with self.assertRaisesMessage(ValueError, "timezone-aware"):
            apply_sync_command(make_command(), store, NaiveClock())
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])

    def test_aggregate_adapter_wrong_version_rolls_back(self):
        class WrongVersionTransaction(FakeTransaction):
            def apply_aggregate_mutation(
                self,
                aggregate_reference,
                expected_version,
                encrypted_payload,
                occurred_at,
            ):
                super().apply_aggregate_mutation(
                    aggregate_reference,
                    expected_version,
                    encrypted_payload,
                    occurred_at,
                )
                return expected_version

        class WrongVersionUnitOfWork(FakeUnitOfWork):
            class TransactionContext(FakeUnitOfWork.TransactionContext):
                def __enter__(self):
                    self.before = deepcopy(self.owner.state)
                    return WrongVersionTransaction(self.owner.state)

        store = WrongVersionUnitOfWork()
        with self.assertRaisesMessage(RuntimeError, "advance exactly one version"):
            apply_sync_command(make_command(), store, FixedClock())
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])

    def test_conflict_replay_does_not_create_duplicate_audit_or_receipt(self):
        store = FakeUnitOfWork()
        command = make_command(base_version=1)
        first = apply_sync_command(command, store, FixedClock())
        second = apply_sync_command(command, store, FixedClock())
        self.assertEqual(first.status, "conflict")
        self.assertTrue(second.replayed)
        self.assertEqual(len(store.state["receipts"]), 1)
        self.assertEqual(len(store.state["audit"]), 1)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["outbox"], [])


class AuditAndSyncInvariantExtensionTests(SimpleTestCase):
    def test_chain_rejects_non_hex_digest_even_when_length_is_valid(self):
        event = AuditEvent(
            action="records.read",
            resource_type="document",
            resource_reference="doc-001",
            occurred_at=NOW,
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        entry = AuditChainEntry(1, "0" * 64, event, "g" * 64)
        self.assertFalse(verify_audit_chain((entry,)))

    def test_conflict_audit_failure_rolls_back_conflict_receipt(self):
        store = FakeUnitOfWork(fail_audit=True)
        with self.assertRaisesMessage(RuntimeError, "injected audit insert failure"):
            apply_sync_command(make_command(base_version=2), store, FixedClock())
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])

    def test_outbox_reference_matches_audit_event_and_excludes_payload(self):
        store = FakeUnitOfWork()
        command = make_command()
        result = apply_sync_command(command, store, FixedClock())
        event = store.state["audit"][0]
        outbox = store.state["outbox"][0]
        self.assertEqual(result.status, "applied")
        self.assertEqual(outbox[0], event.event_id)
        self.assertEqual(outbox[1], command.envelope.aggregate_reference)
        self.assertEqual(outbox[2], result.resulting_version)
        self.assertEqual(outbox[3], event.occurred_at)
        self.assertNotIn(command.encrypted_payload.ciphertext, outbox)
        self.assertNotIn(command.encrypted_payload.wrapped_key, outbox)


class AuditTruncationAndSequenceTests(SimpleTestCase):
    def make_chain(self):
        entries = []
        previous = "0" * 64
        for sequence in range(1, 4):
            event = AuditEvent(
                action=f"records.event_{sequence}",
                resource_type="document",
                resource_reference="doc-001",
                occurred_at=NOW,
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
            )
            digest = canonical_event_digest(event, previous)
            entries.append(AuditChainEntry(sequence, previous, event, digest))
            previous = digest
        return tuple(entries)

    def test_interior_truncation_is_rejected(self):
        chain = self.make_chain()
        self.assertFalse(verify_audit_chain((chain[0], chain[2])))

    def test_duplicate_sequence_is_rejected(self):
        chain = self.make_chain()
        duplicate = replace(chain[1], sequence=1)
        self.assertFalse(verify_audit_chain((chain[0], duplicate, chain[2])))

    def test_tail_truncation_requires_independently_trusted_checkpoint(self):
        chain = self.make_chain()
        truncated = chain[:2]
        # A valid prefix alone cannot prove that later entries were removed.
        self.assertTrue(verify_audit_chain(truncated))
        self.assertFalse(
            verify_audit_chain(
                truncated,
                expected_head_sequence=3,
                expected_head_digest=chain[-1].digest,
            )
        )
        self.assertTrue(
            verify_audit_chain(
                chain,
                expected_head_sequence=3,
                expected_head_digest=chain[-1].digest,
            )
        )

    def test_checkpoint_arguments_must_be_paired_and_well_formed(self):
        chain = self.make_chain()
        with self.assertRaisesMessage(ValueError, "supplied together"):
            verify_audit_chain(chain, expected_head_sequence=3)
        with self.assertRaisesMessage(ValueError, "non-negative integer"):
            verify_audit_chain(
                chain,
                expected_head_sequence=True,
                expected_head_digest=chain[-1].digest,
            )


class SyncRetryAndInterruptionTests(SimpleTestCase):
    def assert_single_success(self, store, command):
        self.assertEqual(store.state["versions"]["aggregate-001"], 4)
        self.assertEqual(len(store.state["mutations"]), 1)
        self.assertEqual(len(store.state["receipts"]), 1)
        self.assertEqual(len(store.state["audit"]), 1)
        self.assertEqual(len(store.state["outbox"]), 1)
        replay = apply_sync_command(command, store, FixedClock())
        self.assertTrue(replay.replayed)
        self.assertEqual(len(store.state["mutations"]), 1)
        self.assertEqual(len(store.state["audit"]), 1)
        self.assertEqual(len(store.state["outbox"]), 1)

    def test_retry_after_audit_append_failure_applies_once(self):
        store = FakeUnitOfWork(fail_audit=True)
        command = make_command()
        with self.assertRaisesMessage(RuntimeError, "injected audit insert failure"):
            apply_sync_command(command, store, FixedClock())
        store.state["fail_audit"] = False
        result = apply_sync_command(command, store, FixedClock())
        self.assertEqual(result.status, "applied")
        self.assert_single_success(store, command)

    def test_retry_after_outbox_append_failure_applies_once(self):
        store = FakeUnitOfWork(fail_outbox=True)
        command = make_command()
        with self.assertRaisesMessage(RuntimeError, "injected outbox insert failure"):
            apply_sync_command(command, store, FixedClock())
        store.state["fail_outbox"] = False
        result = apply_sync_command(command, store, FixedClock())
        self.assertEqual(result.status, "applied")
        self.assert_single_success(store, command)

    def test_interruption_after_aggregate_mutation_rolls_back_then_retries(self):
        class InterruptingTransaction(FakeTransaction):
            def apply_aggregate_mutation(
                self,
                aggregate_reference,
                expected_version,
                encrypted_payload,
                occurred_at,
            ):
                version = super().apply_aggregate_mutation(
                    aggregate_reference,
                    expected_version,
                    encrypted_payload,
                    occurred_at,
                )
                if self.state.get("interrupt_after_mutation"):
                    self.state["interrupt_after_mutation"] = False
                    raise RuntimeError("injected interruption after aggregate mutation")
                return version

        class InterruptingUnitOfWork(FakeUnitOfWork):
            def __init__(self):
                super().__init__()
                self.state["interrupt_after_mutation"] = True

            class TransactionContext(FakeUnitOfWork.TransactionContext):
                def __enter__(self):
                    self.before = deepcopy(self.owner.state)
                    return InterruptingTransaction(self.owner.state)

        store = InterruptingUnitOfWork()
        command = make_command()
        with self.assertRaisesMessage(
            RuntimeError, "injected interruption after aggregate mutation"
        ):
            apply_sync_command(command, store, FixedClock())
        self.assertEqual(store.state["versions"]["aggregate-001"], 3)
        self.assertEqual(store.state["mutations"], [])
        self.assertEqual(store.state["receipts"], {})
        self.assertEqual(store.state["audit"], [])
        self.assertEqual(store.state["outbox"], [])
        store.state["interrupt_after_mutation"] = False
        result = apply_sync_command(command, store, FixedClock())
        self.assertEqual(result.status, "applied")
        self.assert_single_success(store, command)

    def test_lost_commit_acknowledgement_retries_as_idempotent_replay(self):
        class LostAcknowledgementUnitOfWork(FakeUnitOfWork):
            def __init__(self):
                super().__init__()
                self.lose_acknowledgement = True

            class TransactionContext(FakeUnitOfWork.TransactionContext):
                def __exit__(self, exc_type, exc, traceback):
                    result = super().__exit__(exc_type, exc, traceback)
                    if exc_type is None and self.owner.lose_acknowledgement:
                        self.owner.lose_acknowledgement = False
                        raise RuntimeError("simulated commit acknowledgement loss")
                    return result

        store = LostAcknowledgementUnitOfWork()
        command = make_command()
        with self.assertRaisesMessage(RuntimeError, "commit acknowledgement loss"):
            apply_sync_command(command, store, FixedClock())
        # The synthetic context committed its state before simulating lost acknowledgement.
        replay = apply_sync_command(command, store, FixedClock())
        self.assertTrue(replay.replayed)
        self.assertEqual(replay.status, "applied")
        self.assertEqual(len(store.state["mutations"]), 1)
        self.assertEqual(len(store.state["receipts"]), 1)
        self.assertEqual(len(store.state["audit"]), 1)
        self.assertEqual(len(store.state["outbox"]), 1)

    def test_genesis_checkpoint_accepts_empty_chain(self):
        self.assertTrue(
            verify_audit_chain(
                (),
                expected_head_sequence=0,
                expected_head_digest="0" * 64,
            )
        )
