"""Durability, concurrency, replay and rollback tests using temporary SQLite."""

import concurrent.futures
import multiprocessing
import os
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

from scripts.org03_event_store import (
    EventLogIntegrityError,
    IdempotencyConflict,
    Org03EventStore,
    StaleAggregateVersion,
)

AUTH = {
    "primary": "SYNTHETIC-PRIMARY-01",
    "backup": "SYNTHETIC-BACKUP-01",
    "owner_or_delegate": "SYNTHETIC-OWNER-01",
}


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
    store = Org03EventStore(path)
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
        self.store = Org03EventStore(self.path)
        self.store.create_alert(
            "SYNTHETIC-ALERT-STORE-01", "HIGH", "2026-11-13T07:00:00Z"
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
        reopened = Org03EventStore(self.path)
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
        with self.assertRaises(sqlite3.IntegrityError):
            with self.store._connect() as connection:
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
        reopened = Org03EventStore(self.path)
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


if __name__ == "__main__":
    unittest.main()
