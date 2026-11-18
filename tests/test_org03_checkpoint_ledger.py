"""Contract tests for the synthetic ORG-03 checkpoint ledger adapter."""
import multiprocessing
import tempfile
import unittest
from pathlib import Path

from scripts.org03_checkpoint_ledger import (
    GENESIS_HASH,
    Checkpoint,
    CheckpointAuthenticationError,
    CheckpointConflict,
    HMACCheckpointSigner,
    SQLiteCheckpointLedger,
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
