"""Durability, concurrency, replay and rollback tests using temporary SQLite."""

import concurrent.futures
import json
import multiprocessing
import os
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path

from scripts.org03_event_store import (
    AuthorityError,
    CheckpointError,
    EventLogIntegrityError,
    EventStoreBusy,
    IdempotencyConflict,
    IntegrityKeyError,
    Org03EventStore,
    StaleAggregateVersion,
    _digest,
)

TEST_INTEGRITY_KEYS = {
    "synthetic-test-v1": b"ORG03-TEST-ONLY-KEY-NOT-FOR-PRODUCTION-32"
}

AUTH = {
    "primary": "SYNTHETIC-PRIMARY-01",
    "backup": "SYNTHETIC-BACKUP-01",
    "owner_or_delegate": "SYNTHETIC-OWNER-01",
}


def make_store(path, **kwargs):
    kwargs.setdefault("integrity_keys", TEST_INTEGRITY_KEYS)
    return Org03EventStore(path, **kwargs)


def make_event(sequence, name, role="SYSTEM", actor="SYNTHETIC-SYSTEM", **extra):
    return {
        "sequence": sequence,
        "event": name,
        "at_utc": f"2026-11-13T07:{sequence:02d}:00Z",
        "actor_role": role,
        "actor_ref": actor,
        **extra,
    }


def _process_append(path, barrier, queue, event, event_id, idempotency_key):
    store = make_store(path)
    barrier.wait(timeout=10)
    try:
        state = store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            event,
            expected_version=2,
            event_id=event_id,
            idempotency_key=idempotency_key,
            authorized_responder_refs=AUTH,
        )
        queue.put(("committed", state["status"]))
    except StaleAggregateVersion:
        queue.put(("stale", None))


def _crash_with_uncommitted_event(path):
    connection = sqlite3.connect(path, isolation_level=None)
    connection.execute("BEGIN IMMEDIATE")
    connection.execute(
        "INSERT INTO org03_events(event_id, alert_id, sequence, "
        "idempotency_key, event_json, previous_hash, event_hash) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            "SYNTHETIC-CRASH-UNCOMMITTED",
            "SYNTHETIC-ALERT-STORE-01",
            3,
            "SYNTHETIC-CRASH-IDEM",
            "{}",
            "uncommitted",
            "uncommitted",
        ),
    )
    os._exit(17)


class Org03DurableEventStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "org03-test.sqlite3"
        self.store = make_store(self.path)
        self.store.create_alert(
            "SYNTHETIC-ALERT-STORE-01", "HIGH", "2026-11-13T07:00:00Z"
        )
        self.store.register_authority(
            AUTH["primary"],
            "PRIMARY_SECURITY_OPERATIONS",
            "2026-11-13T06:00:00Z",
            scope_ref="SYNTHETIC-ALERT-STORE-01",
        )
        self.store.register_authority(
            AUTH["backup"],
            "BACKUP_SECURITY_OPERATIONS",
            "2026-11-13T06:00:00Z",
            scope_ref="SYNTHETIC-ALERT-STORE-01",
        )
        self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(2, "DELIVERY_CONFIRMED"),
            expected_version=1,
            event_id="SYNTHETIC-EVENT-02",
            idempotency_key="SYNTHETIC-IDEM-02",
            authorized_responder_refs=AUTH,
        )

    def tearDown(self):
        self.temp.cleanup()

    def append_primary(self, event_id="SYNTHETIC-EVENT-03", key="SYNTHETIC-IDEM-03"):
        return self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(
                3,
                "HUMAN_ACKNOWLEDGED",
                "PRIMARY_SECURITY_OPERATIONS",
                AUTH["primary"],
                disposition="ACCEPTED",
            ),
            expected_version=2,
            event_id=event_id,
            idempotency_key=key,
            authorized_responder_refs=AUTH,
        )

    def _race_two_events(self, first_event, second_event, *, expected_version):
        barrier = threading.Barrier(2)

        def attempt(event, event_id, key):
            barrier.wait()
            try:
                result = self.store.append_event(
                    "SYNTHETIC-ALERT-STORE-01",
                    event,
                    expected_version=expected_version,
                    event_id=event_id,
                    idempotency_key=key,
                    authorized_responder_refs=AUTH,
                )
                return ("committed", result["status"])
            except StaleAggregateVersion:
                return ("stale", None)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(
                pool.map(
                    lambda args: attempt(*args),
                    [
                        (
                            first_event,
                            "SYNTHETIC-RACE-EVENT-A",
                            "SYNTHETIC-RACE-IDEM-A",
                        ),
                        (
                            second_event,
                            "SYNTHETIC-RACE-EVENT-B",
                            "SYNTHETIC-RACE-IDEM-B",
                        ),
                    ],
                )
            )
        self.assertEqual(1, sum(item[0] == "committed" for item in outcomes))
        self.assertEqual(1, sum(item[0] == "stale" for item in outcomes))
        return outcomes

    def test_committed_events_survive_new_store_instance(self):
        self.append_primary()
        reopened = make_store(self.path)
        state = reopened.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual("ACKNOWLEDGED", state["status"])
        self.assertEqual(3, len(state["history"]))
        self.assertEqual(3, reopened.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_primary_ack_racing_primary_deadline_has_one_winner(self):
        self._race_two_events(
            make_event(
                3,
                "HUMAN_ACKNOWLEDGED",
                "PRIMARY_SECURITY_OPERATIONS",
                AUTH["primary"],
                disposition="ACCEPTED",
            ),
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
        )
        state = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertIn(state["status"], {"ACKNOWLEDGED", "BACKUP_ROUTED"})
        self.assertEqual(3, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_backup_ack_racing_backup_deadline_has_one_winner(self):
        self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
            event_id="SYNTHETIC-EVENT-03",
            idempotency_key="SYNTHETIC-IDEM-03",
            authorized_responder_refs=AUTH,
        )
        self._race_two_events(
            make_event(
                4,
                "HUMAN_ACKNOWLEDGED",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="ACCEPTED",
            ),
            make_event(4, "BACKUP_ACK_DEADLINE_MISSED"),
            expected_version=3,
        )
        state = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertIn(state["status"], {"ACKNOWLEDGED", "AUTHORITY_ESCALATED"})
        self.assertEqual(4, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_concurrent_same_version_backup_ack_attempts_only_one_wins(self):
        self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
            event_id="SYNTHETIC-EVENT-03",
            idempotency_key="SYNTHETIC-IDEM-03",
            authorized_responder_refs=AUTH,
        )
        self._race_two_events(
            make_event(
                4,
                "HUMAN_ACKNOWLEDGED",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="ACCEPTED",
            ),
            make_event(
                4,
                "HUMAN_ACKNOWLEDGED",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="ACCEPTED",
            ),
            expected_version=3,
        )
        self.assertEqual(4, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_duplicate_idempotent_retry_returns_committed_state(self):
        first = self.append_primary()
        retry = self.append_primary()
        self.assertEqual(first, retry)
        self.assertEqual(3, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_reusing_idempotency_key_for_different_event_is_rejected(self):
        self.append_primary()
        with self.assertRaises(IdempotencyConflict):
            self.store.append_event(
                "SYNTHETIC-ALERT-STORE-01",
                make_event(4, "PRIMARY_ACK_DEADLINE_MISSED"),
                expected_version=3,
                event_id="SYNTHETIC-EVENT-04",
                idempotency_key="SYNTHETIC-IDEM-03",
                authorized_responder_refs=AUTH,
            )

    def test_stale_version_cannot_overwrite_committed_transition(self):
        self.append_primary()
        with self.assertRaises(StaleAggregateVersion):
            self.store.append_event(
                "SYNTHETIC-ALERT-STORE-01",
                make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
                expected_version=2,
                event_id="SYNTHETIC-EVENT-STALE",
                idempotency_key="SYNTHETIC-IDEM-STALE",
                authorized_responder_refs=AUTH,
            )
        self.assertEqual(3, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_failure_before_commit_leaves_no_partial_event(self):
        with (
            self.assertRaises(sqlite3.IntegrityError),
            self.store._connect() as connection,
        ):
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "INSERT INTO org03_events(event_id, alert_id, sequence, "
                "idempotency_key, event_json, previous_hash, event_hash) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    "SYNTHETIC-EVENT-BAD",
                    "SYNTHETIC-ALERT-STORE-01",
                    2,
                    "SYNTHETIC-IDEM-BAD",
                    "{}",
                    "bad",
                    "bad",
                ),
            )
            connection.commit()
        self.assertEqual(2, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))
        state = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual("AWAITING_HUMAN_ACK", state["status"])

    def test_corrupted_event_hash_fails_closed(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET event_hash = ? "
                "WHERE alert_id = ? AND sequence = 2",
                ("f" * 64, "SYNTHETIC-ALERT-STORE-01"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_separate_processes_arbitrate_same_aggregate_version(self):
        context = multiprocessing.get_context("fork")
        barrier = context.Barrier(2)
        queue = context.Queue()
        events = [
            (
                make_event(
                    3,
                    "HUMAN_ACKNOWLEDGED",
                    "PRIMARY_SECURITY_OPERATIONS",
                    AUTH["primary"],
                    disposition="ACCEPTED",
                ),
                "SYNTHETIC-MP-EVENT-A",
                "SYNTHETIC-MP-IDEM-A",
            ),
            (
                make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
                "SYNTHETIC-MP-EVENT-B",
                "SYNTHETIC-MP-IDEM-B",
            ),
        ]
        processes = [
            context.Process(
                target=_process_append,
                args=(str(self.path), barrier, queue, event, event_id, key),
            )
            for event, event_id, key in events
        ]
        for process in processes:
            process.start()
        for process in processes:
            process.join(timeout=20)
            self.assertFalse(process.is_alive(), "worker process did not exit")
            self.assertEqual(0, process.exitcode)
        outcomes = [queue.get(timeout=5), queue.get(timeout=5)]
        self.assertEqual(1, sum(item[0] == "committed" for item in outcomes))
        self.assertEqual(1, sum(item[0] == "stale" for item in outcomes))
        self.assertEqual(3, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_uncommitted_write_is_rolled_back_after_abrupt_process_exit(self):
        context = multiprocessing.get_context("fork")
        process = context.Process(
            target=_crash_with_uncommitted_event, args=(str(self.path),)
        )
        process.start()
        process.join(timeout=20)
        self.assertFalse(process.is_alive(), "crash worker did not exit")
        self.assertEqual(17, process.exitcode)
        reopened = make_store(self.path)
        state = reopened.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual("AWAITING_HUMAN_ACK", state["status"])
        self.assertEqual(2, reopened.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_replay_is_repeatable_and_aggregate_matches_log(self):
        first = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        second = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual(first, second)
        self.assertEqual("AWAITING_HUMAN_ACK", second["status"])

    def test_load_state_uses_one_snapshot_during_concurrent_commit(self):
        reader = make_store(self.path)
        writer = make_store(self.path)
        aggregate_read = threading.Event()
        allow_replay = threading.Event()
        original_replay = reader._replay_in_transaction
        observed = {}

        def paused_replay(*args, **kwargs):
            aggregate_read.set()
            self.assertTrue(allow_replay.wait(timeout=5))
            return original_replay(*args, **kwargs)

        reader._replay_in_transaction = paused_replay

        def read():
            observed["state"] = reader.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

        thread = threading.Thread(target=read)
        thread.start()
        self.assertTrue(aggregate_read.wait(timeout=5))
        writer.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
            event_id="SYNTHETIC-SNAPSHOT-EVENT-03",
            idempotency_key="SYNTHETIC-SNAPSHOT-IDEM-03",
            authorized_responder_refs=AUTH,
        )
        allow_replay.set()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual("AWAITING_HUMAN_ACK", observed["state"]["status"])
        self.assertEqual(
            "BACKUP_ROUTED",
            reader.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )["status"],
        )

    def test_writer_contention_expires_with_typed_error(self):
        store = make_store(self.path, timeout_seconds=0.15)
        blocker = sqlite3.connect(self.path, isolation_level=None)
        blocker.execute("BEGIN IMMEDIATE")
        started = time.monotonic()
        try:
            with self.assertRaises(EventStoreBusy):
                store.create_alert(
                    "SYNTHETIC-LOCKED-ALERT", "LOW", "2026-11-13T08:00:00Z"
                )
        finally:
            blocker.rollback()
            blocker.close()
        self.assertLess(time.monotonic() - started, 1.5)

    def test_owned_connection_is_closed_on_context_exit(self):
        with self.store._connection() as connection:
            connection.execute("SELECT 1")
        with self.assertRaises(sqlite3.ProgrammingError):
            connection.execute("SELECT 1")

    def test_same_idempotency_key_with_different_event_id_is_rejected(self):
        self.append_primary()
        with self.assertRaises(IdempotencyConflict):
            self.append_primary(
                event_id="SYNTHETIC-ALTERNATE-EVENT-ID",
                key="SYNTHETIC-IDEM-03",
            )

    def test_full_database_rewrite_with_recomputed_public_hashes_fails_hmac(self):
        with self.store._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM org03_events WHERE alert_id = ? ORDER BY sequence",
                ("SYNTHETIC-ALERT-STORE-01",),
            ).fetchall()
            previous = self.store.GENESIS_HASH
            for row in rows:
                event = __import__("json").loads(row["event_json"])
                if row["sequence"] == 2:
                    event["at_utc"] = "2026-11-13T07:59:59Z"
                event_json = __import__("json").dumps(
                    event, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                )
                digest = _digest(
                    previous,
                    row["alert_id"],
                    row["event_id"],
                    row["sequence"],
                    row["idempotency_key"],
                    event_json,
                )
                connection.execute(
                    "UPDATE org03_events SET event_json = ?, previous_hash = ?, "
                    "event_hash = ? WHERE event_id = ?",
                    (event_json, previous, digest, row["event_id"]),
                )
                previous = digest
        with self.assertRaises(EventLogIntegrityError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_event_identifier_substitution_fails_hmac(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET event_id = ? WHERE sequence = 2",
                ("SYNTHETIC-SUBSTITUTED-EVENT",),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_event_truncation_is_detected_by_checkpoint(self):
        with self.store._connect() as connection:
            connection.execute(
                "DELETE FROM org03_events WHERE alert_id = ? AND sequence = 2",
                ("SYNTHETIC-ALERT-STORE-01",),
            )
            connection.execute(
                "UPDATE org03_aggregates SET version = 1 WHERE alert_id = ?",
                ("SYNTHETIC-ALERT-STORE-01",),
            )
        with self.assertRaises((CheckpointError, EventLogIntegrityError)):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_unknown_integrity_key_fails_closed(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET key_id = ? WHERE sequence = 2",
                ("unknown-key",),
            )
        with self.assertRaises(IntegrityKeyError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_revoked_integrity_key_fails_closed(self):
        reopened = make_store(
            self.path,
            revoked_key_ids=frozenset({"synthetic-test-v1"}),
        )
        with self.assertRaises(IntegrityKeyError):
            reopened.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_checkpoint_rollback_is_detected(self):
        import shutil

        checkpoint = self.store._checkpoint_path("SYNTHETIC-ALERT-STORE-01")
        old_checkpoint = Path(self.temp.name) / "checkpoint-before-append.json"
        shutil.copyfile(checkpoint, old_checkpoint)
        self.append_primary()
        shutil.copyfile(old_checkpoint, checkpoint)
        with self.assertRaises(CheckpointError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_key_rotation_keeps_old_events_verifiable_and_signs_new_events(self):
        rotated = make_store(
            self.path,
            integrity_keys={
                "synthetic-test-v1": TEST_INTEGRITY_KEYS["synthetic-test-v1"],
                "synthetic-test-v2": b"ORG03-ROTATED-TEST-KEY-NOT-FOR-PRODUCTION-32",
            },
            active_key_id="synthetic-test-v2",
        )
        event = make_event(3, "PRIMARY_ACK_DEADLINE_MISSED")
        rotated.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            event,
            expected_version=2,
            event_id="SYNTHETIC-ROTATED-EVENT",
            idempotency_key="SYNTHETIC-ROTATED-IDEM",
            authorized_responder_refs=AUTH,
        )
        state = rotated.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual("BACKUP_ROUTED", state["status"])

    def test_concurrent_identical_retries_commit_one_event(self):
        event = make_event(
            3,
            "HUMAN_ACKNOWLEDGED",
            "PRIMARY_SECURITY_OPERATIONS",
            AUTH["primary"],
            disposition="ACCEPTED",
        )
        barrier = threading.Barrier(2)

        def attempt():
            barrier.wait()
            return self.store.append_event(
                "SYNTHETIC-ALERT-STORE-01",
                event,
                expected_version=2,
                event_id="SYNTHETIC-CONCURRENT-DUPLICATE",
                idempotency_key="SYNTHETIC-CONCURRENT-DUPLICATE-IDEM",
                authorized_responder_refs=AUTH,
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: attempt(), range(2)))
        self.assertEqual(results[0], results[1])
        self.assertEqual(3, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))

    def test_historical_event_before_revocation_remains_valid(self):
        self.append_primary()
        self.store.revoke_authority(AUTH["primary"], "2026-11-13T07:04:00Z")
        state = self.store.load_state(
            "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
        )
        self.assertEqual("ACKNOWLEDGED", state["status"])

    def test_new_event_after_effective_revocation_is_rejected(self):
        self.store.revoke_authority(AUTH["primary"], "2026-11-13T07:02:00Z")
        event = make_event(
            3,
            "HUMAN_ACKNOWLEDGED",
            "PRIMARY_SECURITY_OPERATIONS",
            AUTH["primary"],
            disposition="ACCEPTED",
        )
        with self.assertRaises(AuthorityError):
            self.store.append_event(
                "SYNTHETIC-ALERT-STORE-01",
                event,
                expected_version=2,
                event_id="SYNTHETIC-REVOKED-EVENT",
                idempotency_key="SYNTHETIC-REVOKED-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_authority_registry_tampering_fails_replay(self):
        self.append_primary()
        with self.store._connect() as connection:
            connection.execute("DROP TRIGGER org03_authority_no_update")
            connection.execute(
                "UPDATE org03_authority_versions SET evidence_mac = ? "
                "WHERE principal_ref = ?",
                ("0" * 64, AUTH["primary"]),
            )
        with self.assertRaises(AuthorityError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_cross_principal_authority_evidence_substitution_is_rejected(self):
        self.append_primary()
        with self.store._connect() as connection:
            row = connection.execute(
                "SELECT event_json FROM org03_events WHERE sequence = 3"
            ).fetchone()
            event = __import__("json").loads(row["event_json"])
            event["actor_ref"] = AUTH["backup"]
            connection.execute(
                "UPDATE org03_events SET event_json = ? WHERE sequence = 3",
                (
                    __import__("json").dumps(
                        event, sort_keys=True, separators=(",", ":"), ensure_ascii=False
                    ),
                ),
            )
        with self.assertRaises(AuthorityError):
            self.store.load_state(
                "SYNTHETIC-ALERT-STORE-01", authorized_responder_refs=AUTH
            )

    def test_authority_versions_cannot_be_mutated_or_deleted(self):
        with (
            self.assertRaises(sqlite3.IntegrityError),
            self.store._connect() as connection,
        ):
            connection.execute(
                "UPDATE org03_authority_versions SET role = ? WHERE principal_ref = ?",
                ("SYNTHETIC_ADMIN", AUTH["primary"]),
            )

    def test_idempotent_retry_returns_original_result_after_later_transition(self):
        first_event = make_event(
            3,
            "HUMAN_UNABLE_TO_ACCEPT",
            "PRIMARY_SECURITY_OPERATIONS",
            AUTH["primary"],
            disposition="UNABLE_TO_ACCEPT",
        )
        original = self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            first_event,
            expected_version=2,
            event_id="SYNTHETIC-ORIGINAL-DECLINE",
            idempotency_key="SYNTHETIC-ORIGINAL-DECLINE-IDEM",
            authorized_responder_refs=AUTH,
        )
        self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            make_event(
                4,
                "HUMAN_ACKNOWLEDGED",
                "BACKUP_SECURITY_OPERATIONS",
                AUTH["backup"],
                disposition="ACCEPTED",
            ),
            expected_version=3,
            event_id="SYNTHETIC-LATER-EVENT",
            idempotency_key="SYNTHETIC-LATER-IDEM",
            authorized_responder_refs=AUTH,
        )
        retry = self.store.append_event(
            "SYNTHETIC-ALERT-STORE-01",
            first_event,
            expected_version=2,
            event_id="SYNTHETIC-ORIGINAL-DECLINE",
            idempotency_key="SYNTHETIC-ORIGINAL-DECLINE-IDEM",
            authorized_responder_refs=AUTH,
        )
        self.assertEqual(original, retry)
        self.assertEqual("BACKUP_ROUTED", retry["status"])
        self.assertEqual(4, self.store.event_count("SYNTHETIC-ALERT-STORE-01"))


class Org03R1R3NegativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "org03-integrity.sqlite3"
        self.store = make_store(self.path)
        self.store.create_alert("SYNTHETIC-R1-ALERT", "HIGH", "2026-11-13T07:00:00Z")
        self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            make_event(2, "DELIVERY_CONFIRMED"),
            expected_version=1,
            event_id="SYNTHETIC-R1-EVENT-02",
            idempotency_key="SYNTHETIC-R1-IDEM-02",
            authorized_responder_refs=AUTH,
        )

    def tearDown(self):
        self.temp.cleanup()

    def load(self):
        return self.store.load_state(
            "SYNTHETIC-R1-ALERT", authorized_responder_refs=AUTH
        )

    def register_primary(self):
        self.store.register_authority(
            AUTH["primary"],
            "PRIMARY_SECURITY_OPERATIONS",
            "2026-11-13T07:00:00Z",
            scope_ref="SYNTHETIC-R1-ALERT",
        )

    def human_ack(self, at):
        return {
            "sequence": 3,
            "event": "HUMAN_ACKNOWLEDGED",
            "at_utc": at,
            "actor_role": "PRIMARY_SECURITY_OPERATIONS",
            "actor_ref": AUTH["primary"],
            "disposition": "ACCEPTED",
        }

    def test_full_database_rewrite_with_recomputed_hash_fails_hmac(self):
        with self.store._connect() as connection:
            row = connection.execute(
                "SELECT * FROM org03_events WHERE alert_id=? AND sequence=2",
                ("SYNTHETIC-R1-ALERT",),
            ).fetchone()
            changed = json.loads(row["event_json"])
            changed["event"] = "DELIVERY_FAILED"
            encoded = json.dumps(
                changed, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            )
            digest = _digest(
                row["previous_hash"],
                row["alert_id"],
                row["event_id"],
                row["sequence"],
                row["idempotency_key"],
                encoded,
            )
            connection.execute(
                "UPDATE org03_events SET event_json=?,event_hash=? WHERE event_id=?",
                (encoded, digest, row["event_id"]),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.load()

    def test_event_id_substitution_fails_hmac(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET event_id=? WHERE alert_id=? AND sequence=2",
                ("SYNTHETIC-SUBSTITUTED-EVENT", "SYNTHETIC-R1-ALERT"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.load()

    def test_truncation_with_matching_aggregate_rewrite_fails_checkpoint(self):
        with self.store._connect() as connection:
            connection.execute(
                "DELETE FROM org03_events WHERE alert_id=? AND sequence=2",
                ("SYNTHETIC-R1-ALERT",),
            )
            connection.execute(
                "UPDATE org03_aggregates SET version=1, "
                "status='AWAITING_HUMAN_ACK' WHERE alert_id=?",
                ("SYNTHETIC-R1-ALERT",),
            )
        with self.assertRaises(CheckpointError):
            self.load()

    def test_unknown_event_key_fails_closed(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET key_id='unknown-key' "
                "WHERE alert_id=? AND sequence=2",
                ("SYNTHETIC-R1-ALERT",),
            )
        with self.assertRaises(IntegrityKeyError):
            self.load()

    def test_revoked_key_fails_closed(self):
        revoked = make_store(
            self.path, revoked_key_ids=frozenset({"synthetic-test-v1"})
        )
        with self.assertRaises(IntegrityKeyError):
            revoked.load_state("SYNTHETIC-R1-ALERT", authorized_responder_refs=AUTH)

    def test_checkpoint_rollback_is_detected(self):
        path = self.store._checkpoint_path("SYNTHETIC-R1-ALERT")
        old = path.read_text(encoding="utf-8")
        self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
            event_id="SYNTHETIC-R1-EVENT-03",
            idempotency_key="SYNTHETIC-R1-IDEM-03",
            authorized_responder_refs=AUTH,
        )
        path.write_text(old, encoding="utf-8")
        with self.assertRaises(CheckpointError):
            self.load()

    def test_idempotent_result_snapshot_tampering_fails_hmac(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET result_json = ? "
                "WHERE alert_id = ? AND sequence = 2",
                ('{"status":"FORGED"}', "SYNTHETIC-R1-ALERT"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.load()

    def test_idempotency_request_fingerprint_tampering_fails_hmac(self):
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET request_json = ? "
                "WHERE alert_id = ? AND sequence = 2",
                ('{"event_type":"FORGED"}', "SYNTHETIC-R1-ALERT"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.load()

    def test_idempotent_retry_rejects_tampered_result_snapshot(self):
        event = make_event(3, "PRIMARY_ACK_DEADLINE_MISSED")
        self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            event,
            expected_version=2,
            event_id="SYNTHETIC-R1-IDEMPOTENT-RESULT",
            idempotency_key="SYNTHETIC-R1-IDEMPOTENT-RESULT-IDEM",
            authorized_responder_refs=AUTH,
        )
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET result_json = ? "
                "WHERE alert_id = ? AND sequence = 3",
                ('{"status":"FORGED"}', "SYNTHETIC-R1-ALERT"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.store.append_event(
                "SYNTHETIC-R1-ALERT",
                event,
                expected_version=2,
                event_id="SYNTHETIC-R1-IDEMPOTENT-RESULT",
                idempotency_key="SYNTHETIC-R1-IDEMPOTENT-RESULT-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_idempotent_retry_rejects_tampered_request_fingerprint(self):
        event = make_event(3, "PRIMARY_ACK_DEADLINE_MISSED")
        self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            event,
            expected_version=2,
            event_id="SYNTHETIC-R1-IDEMPOTENT-REQUEST",
            idempotency_key="SYNTHETIC-R1-IDEMPOTENT-REQUEST-IDEM",
            authorized_responder_refs=AUTH,
        )
        with self.store._connect() as connection:
            connection.execute(
                "UPDATE org03_events SET request_json = ? "
                "WHERE alert_id = ? AND sequence = 3",
                ('{"event_type":"FORGED"}', "SYNTHETIC-R1-ALERT"),
            )
        with self.assertRaises(EventLogIntegrityError):
            self.store.append_event(
                "SYNTHETIC-R1-ALERT",
                event,
                expected_version=2,
                event_id="SYNTHETIC-R1-IDEMPOTENT-REQUEST",
                idempotency_key="SYNTHETIC-R1-IDEMPOTENT-REQUEST-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_checkpoint_mac_tampering_fails_closed(self):
        checkpoint = self.store._checkpoint_path("SYNTHETIC-R1-ALERT")
        record = json.loads(checkpoint.read_text(encoding="utf-8"))
        record["event_hash"] = "f" * 64
        checkpoint.write_text(
            json.dumps(record, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
        with self.assertRaises(CheckpointError):
            self.load()

    def test_concurrent_revocation_and_acknowledgement_fail_closed(self):
        self.register_primary()
        barrier = threading.Barrier(2)

        def append_ack():
            barrier.wait()
            return self.store.append_event(
                "SYNTHETIC-R1-ALERT",
                self.human_ack("2026-11-13T07:04:00Z"),
                expected_version=2,
                event_id="SYNTHETIC-R3-CONCURRENT-ACK",
                idempotency_key="SYNTHETIC-R3-CONCURRENT-ACK-IDEM",
                authorized_responder_refs=AUTH,
            )

        def revoke():
            barrier.wait()
            return self.store.revoke_authority(AUTH["primary"], "2026-11-13T07:04:00Z")

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            ack_future = pool.submit(append_ack)
            revoke_future = pool.submit(revoke)
            try:
                ack_future.result()
                append_won = True
            except AuthorityError:
                append_won = False
            revoke_future.result()

        if append_won:
            with self.assertRaises(AuthorityError):
                self.load()
        else:
            self.assertEqual("AWAITING_HUMAN_ACK", self.load()["status"])

    def test_key_rotation_verifies_old_and_new_events(self):
        keys = {
            "synthetic-test-v1": b"ORG03-TEST-ONLY-KEY-NOT-FOR-PRODUCTION-32",
            "synthetic-test-v2": b"synthetic-org03-rotated-test-key-000000000000",
        }
        rotated = make_store(
            self.path, integrity_keys=keys, active_key_id="synthetic-test-v2"
        )
        rotated.append_event(
            "SYNTHETIC-R1-ALERT",
            make_event(3, "PRIMARY_ACK_DEADLINE_MISSED"),
            expected_version=2,
            event_id="SYNTHETIC-R1-ROTATED",
            idempotency_key="SYNTHETIC-R1-ROTATED-IDEM",
            authorized_responder_refs=AUTH,
        )
        self.assertEqual(
            "BACKUP_ROUTED",
            rotated.load_state("SYNTHETIC-R1-ALERT", authorized_responder_refs=AUTH)[
                "status"
            ],
        )
        with rotated._connection() as connection:
            ids = [
                r["key_id"]
                for r in connection.execute(
                    "SELECT key_id FROM org03_events "
                    "WHERE alert_id=? ORDER BY sequence",
                    ("SYNTHETIC-R1-ALERT",),
                )
            ]
        self.assertEqual(
            [
                "synthetic-test-v1",
                "synthetic-test-v1",
                "synthetic-test-v2",
            ],
            ids,
        )

    def test_empty_keyring_is_rejected(self):
        with self.assertRaises(IntegrityKeyError):
            Org03EventStore(Path(self.temp.name) / "empty.sqlite3", integrity_keys={})

    def test_system_event_cannot_claim_responder_authority(self):
        event = make_event(3, "PRIMARY_ACK_DEADLINE_MISSED")
        event["authority_evidence"] = {"principal_ref": AUTH["primary"]}
        with self.assertRaises(AuthorityError):
            self.store.append_event(
                "SYNTHETIC-R1-ALERT",
                event,
                expected_version=2,
                event_id="SYNTHETIC-R1-SYSTEM-AUTHORITY",
                idempotency_key="SYNTHETIC-R1-SYSTEM-AUTHORITY-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_historical_authority_before_revocation_remains_valid(self):
        self.register_primary()
        self.store.revoke_authority(AUTH["primary"], "2026-11-13T07:04:00Z")
        result = self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            self.human_ack("2026-11-13T07:03:00Z"),
            expected_version=2,
            event_id="SYNTHETIC-R3-HISTORICAL",
            idempotency_key="SYNTHETIC-R3-HISTORICAL-IDEM",
            authorized_responder_refs=AUTH,
        )
        self.assertEqual("ACKNOWLEDGED", result["status"])
        self.assertEqual("ACKNOWLEDGED", self.load()["status"])

    def test_authority_is_rejected_at_exact_revocation_time(self):
        self.register_primary()
        self.store.revoke_authority(AUTH["primary"], "2026-11-13T07:04:00Z")
        with self.assertRaises(AuthorityError):
            self.store.append_event(
                "SYNTHETIC-R1-ALERT",
                self.human_ack("2026-11-13T07:04:00Z"),
                expected_version=2,
                event_id="SYNTHETIC-R3-REVOKED",
                idempotency_key="SYNTHETIC-R3-REVOKED-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_altered_authority_evidence_is_rejected(self):
        self.register_primary()
        with self.store._connection() as connection:
            event = self.store._authority_for_event(
                connection, self.human_ack("2026-11-13T07:03:00Z"), "SYNTHETIC-R1-ALERT"
            )
            event["authority_evidence"]["role"] = "OWNER_OR_DELEGATE"
            with self.assertRaises(AuthorityError):
                self.store._verify_authority_event(
                    connection, event, "SYNTHETIC-R1-ALERT"
                )

    def test_cross_principal_evidence_substitution_is_rejected(self):
        self.register_primary()
        self.store.register_authority(
            AUTH["backup"],
            "PRIMARY_SECURITY_OPERATIONS",
            "2026-11-13T07:00:00Z",
            scope_ref="SYNTHETIC-R1-ALERT",
        )
        with self.store._connection() as connection:
            event = self.store._authority_for_event(
                connection, self.human_ack("2026-11-13T07:03:00Z"), "SYNTHETIC-R1-ALERT"
            )
            event["actor_ref"] = AUTH["backup"]
            with self.assertRaises(AuthorityError):
                self.store._verify_authority_event(
                    connection, event, "SYNTHETIC-R1-ALERT"
                )

    def test_historical_replay_ignores_mutated_current_responder_mapping(self):
        self.register_primary()
        self.store.append_event(
            "SYNTHETIC-R1-ALERT",
            self.human_ack("2026-11-13T07:03:00Z"),
            expected_version=2,
            event_id="SYNTHETIC-R3-HISTORICAL-MAPPING",
            idempotency_key="SYNTHETIC-R3-HISTORICAL-MAPPING-IDEM",
            authorized_responder_refs=AUTH,
        )
        state = self.store.load_state(
            "SYNTHETIC-R1-ALERT",
            authorized_responder_refs={"primary": "SYNTHETIC-REPLACED-RESPONDER"},
        )
        self.assertEqual("ACKNOWLEDGED", state["status"])

    def test_authority_grant_cannot_be_reused_for_another_alert_scope(self):
        self.register_primary()
        self.store.create_alert("SYNTHETIC-OTHER-ALERT", "HIGH", "2026-11-13T07:00:00Z")
        self.store.append_event(
            "SYNTHETIC-OTHER-ALERT",
            make_event(2, "DELIVERY_CONFIRMED"),
            expected_version=1,
            event_id="SYNTHETIC-OTHER-DELIVERY",
            idempotency_key="SYNTHETIC-OTHER-DELIVERY-IDEM",
            authorized_responder_refs=AUTH,
        )
        with self.assertRaises(AuthorityError):
            self.store.append_event(
                "SYNTHETIC-OTHER-ALERT",
                self.human_ack("2026-11-13T07:03:00Z"),
                expected_version=2,
                event_id="SYNTHETIC-OTHER-HUMAN-ACK",
                idempotency_key="SYNTHETIC-OTHER-HUMAN-ACK-IDEM",
                authorized_responder_refs=AUTH,
            )

    def test_authority_registry_versions_are_immutable(self):
        self.register_primary()
        with (
            self.store._connection() as connection,
            self.assertRaises(sqlite3.IntegrityError),
        ):
            connection.execute(
                "UPDATE org03_authority_versions SET role='OWNER_OR_DELEGATE' "
                "WHERE principal_ref=?",
                (AUTH["primary"],),
            )


if __name__ == "__main__":
    unittest.main()
