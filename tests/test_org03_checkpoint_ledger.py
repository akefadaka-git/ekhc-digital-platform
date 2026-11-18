"""Contract tests for the synthetic ORG-03 checkpoint ledger adapter."""

import multiprocessing
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.org03_checkpoint_ledger import (
    GENESIS_HASH,
    AsymmetricCheckpointSigner,
    Checkpoint,
    CheckpointAuthenticationError,
    CheckpointConflict,
    CheckpointProviderUnavailable,
    HMACCheckpointSigner,
    SQLiteCheckpointLedger,
    canonical_json,
)

KEYS = {"test-v1": b"ORG03-SYNTHETIC-CHECKPOINT-KEY-MATERIAL-32-BYTES"}


def make_signer():
    return HMACCheckpointSigner(KEYS, "test-v1")


def make_checkpoint(sequence, previous_hash, event_hash, previous_sequence=None):
    return Checkpoint(
        alert_id="SYNTHETIC-ALERT-01",
        sequence=sequence,
        event_hash=event_hash,
        previous_sequence=(
            sequence - 1 if previous_sequence is None else previous_sequence
        ),
        previous_hash=previous_hash,
        checkpoint_version=1,
        key_id="test-v1",
        published_at_utc=f"2026-11-18T10:00:{sequence:02d}Z",
    )


def _advance_worker(path, barrier, queue, event_hash):
    signer = make_signer()
    ledger = SQLiteCheckpointLedger(path, signer)
    checkpoint = make_checkpoint(1, GENESIS_HASH, event_hash)
    _, signature = signer.sign(checkpoint.payload())
    barrier.wait(timeout=10)
    try:
        created = ledger.compare_and_set(checkpoint, signature)
        queue.put(("ok", created))
    except CheckpointConflict:
        queue.put(("conflict", False))


class CheckpointLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.temp.name) / "checkpoint-ledger.sqlite3")
        self.signer = make_signer()
        self.ledger = SQLiteCheckpointLedger(self.path, self.signer)

    def tearDown(self):
        self.temp.cleanup()

    def advance(self, sequence, previous_hash, event_hash):
        checkpoint = make_checkpoint(sequence, previous_hash, event_hash)
        _, signature = self.signer.sign(checkpoint.payload())
        return self.ledger.compare_and_set(checkpoint, signature)

    def test_genesis_advancement_and_head_read(self):
        self.assertTrue(self.advance(1, GENESIS_HASH, "a" * 64))
        head = self.ledger.head("SYNTHETIC-ALERT-01")
        self.assertEqual(1, head.sequence)
        self.assertEqual("a" * 64, head.event_hash)

    def test_exact_repeat_is_idempotent(self):
        self.advance(1, GENESIS_HASH, "a" * 64)
        self.assertFalse(self.advance(1, GENESIS_HASH, "a" * 64))

    def test_same_sequence_different_hash_is_conflict(self):
        self.advance(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointConflict):
            self.advance(1, GENESIS_HASH, "b" * 64)

    def test_wrong_predecessor_is_rejected(self):
        self.advance(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointConflict):
            self.advance(2, "f" * 64, "b" * 64)

    def test_sequence_skip_is_rejected(self):
        with self.assertRaises(CheckpointConflict):
            self.advance(2, "a" * 64, "b" * 64)

    def test_signature_tampering_is_rejected(self):
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointAuthenticationError):
            self.ledger.compare_and_set(checkpoint, "invalid")

    def test_history_is_ordered_and_authenticated(self):
        self.advance(1, GENESIS_HASH, "a" * 64)
        self.advance(2, "a" * 64, "b" * 64)
        history = self.ledger.history("SYNTHETIC-ALERT-01", 1, 2)
        self.assertEqual([1, 2], [item.sequence for item in history])

    def test_asymmetric_provider_adapter_keeps_signing_provider_side(self):
        provider = Mock()
        provider.sign.return_value = b"provider-signature"
        provider.verify.return_value = True
        signer = AsymmetricCheckpointSigner(
            provider,
            trusted_key_ids=frozenset({"kms-key-v1"}),
            active_key_id="kms-key-v1",
        )
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        key_id, signature = signer.sign(checkpoint.payload())
        self.assertEqual("kms-key-v1", key_id)
        self.assertTrue(signer.verify(key_id, checkpoint.payload(), signature))
        provider.sign.assert_called_once()
        provider.verify.assert_called_once_with(
            "kms-key-v1",
            canonical_json(checkpoint.payload()).encode("utf-8"),
            b"provider-signature",
        )

    def test_asymmetric_provider_adapter_fails_closed_for_revoked_key(self):
        provider = Mock()
        signer = AsymmetricCheckpointSigner(
            provider,
            trusted_key_ids=frozenset({"kms-key-v1"}),
            active_key_id="kms-key-v1",
            revoked_key_ids=frozenset({"kms-key-v1"}),
        )
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointAuthenticationError):
            signer.sign(checkpoint.payload())
        self.assertFalse(signer.verify("kms-key-v1", checkpoint.payload(), "c2ln"))
        provider.sign.assert_not_called()
        provider.verify.assert_not_called()

    def test_asymmetric_provider_outage_is_retriable_not_authentication_failure(self):
        provider = Mock()
        provider.sign.side_effect = TimeoutError("synthetic KMS timeout")
        provider.verify.side_effect = TimeoutError("synthetic KMS timeout")
        signer = AsymmetricCheckpointSigner(
            provider,
            trusted_key_ids=frozenset({"kms-key-v1"}),
            active_key_id="kms-key-v1",
        )
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointProviderUnavailable):
            signer.sign(checkpoint.payload())
        with self.assertRaises(CheckpointProviderUnavailable):
            signer.verify("kms-key-v1", checkpoint.payload(), "c2ln")

    def test_checkpoint_key_rotation_verifies_old_and_new_signatures(self):
        keys = {
            "test-v1": KEYS["test-v1"],
            "test-v2": b"ORG03-SECOND-SYNTHETIC-KEY-MATERIAL-32-BYTES",
        }
        signer_v1 = HMACCheckpointSigner(keys, "test-v1")
        ledger_v1 = SQLiteCheckpointLedger(self.path, signer_v1)
        first = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        _, first_signature = signer_v1.sign(first.payload())
        ledger_v1.compare_and_set(first, first_signature)

        signer_v2 = HMACCheckpointSigner(keys, "test-v2")
        ledger_v2 = SQLiteCheckpointLedger(self.path, signer_v2)
        self.assertEqual("test-v1", ledger_v2.head(first.alert_id).key_id)
        second = Checkpoint(
            alert_id=first.alert_id,
            sequence=2,
            event_hash="b" * 64,
            previous_sequence=1,
            previous_hash="a" * 64,
            checkpoint_version=1,
            key_id="test-v2",
            published_at_utc="2026-11-18T10:00:02Z",
        )
        _, second_signature = signer_v2.sign(second.payload())
        ledger_v2.compare_and_set(second, second_signature)
        history = ledger_v2.history(first.alert_id, 1, 2)
        self.assertEqual(["test-v1", "test-v2"], [item.key_id for item in history])

    def test_revoked_checkpoint_signing_key_cannot_advance_ledger(self):
        signer = HMACCheckpointSigner(
            KEYS, "test-v1", revoked_key_ids=frozenset({"test-v1"})
        )
        ledger = SQLiteCheckpointLedger(self.path, signer)
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        with self.assertRaises(CheckpointAuthenticationError):
            signer.sign(checkpoint.payload())
        self.assertIsNone(ledger.head(checkpoint.alert_id))

    def test_missing_historical_checkpoint_key_fails_closed(self):
        original = HMACCheckpointSigner(KEYS, "test-v1")
        ledger = SQLiteCheckpointLedger(self.path, original)
        checkpoint = make_checkpoint(1, GENESIS_HASH, "a" * 64)
        _, signature = original.sign(checkpoint.payload())
        ledger.compare_and_set(checkpoint, signature)

        replacement = HMACCheckpointSigner(
            {"test-v2": b"ORG03-SECOND-SYNTHETIC-KEY-MATERIAL-32-BYTES"},
            "test-v2",
        )
        reopened = SQLiteCheckpointLedger(self.path, replacement)
        with self.assertRaises(CheckpointAuthenticationError):
            reopened.head(checkpoint.alert_id)

    def test_two_processes_cannot_publish_conflicting_genesis_heads(self):
        context = multiprocessing.get_context("fork")
        barrier = context.Barrier(2)
        queue = context.Queue()
        processes = [
            context.Process(
                target=_advance_worker, args=(self.path, barrier, queue, value)
            )
            for value in ("a" * 64, "b" * 64)
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=20)
            self.assertFalse(process.is_alive(), "ledger worker did not exit")
            self.assertEqual(0, process.exitcode)
        outcomes = [queue.get(timeout=5)[0] for _ in processes]
        self.assertEqual(1, outcomes.count("ok"))
        self.assertEqual(1, outcomes.count("conflict"))
        self.assertEqual(1, self.ledger.head("SYNTHETIC-ALERT-01").sequence)


if __name__ == "__main__":
    unittest.main()
