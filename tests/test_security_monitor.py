import unittest
from datetime import UTC, datetime

from scripts.security_monitor import (
    escape_table_cell,
    evaluate_exceptions,
    parse_lockfile,
    parse_utc,
)


class SecurityMonitorTests(unittest.TestCase):
    def test_parses_pinned_lock_entries_and_ignores_hash_options(self):
        lock_text = (
            "# lock\n"
            + "Django==5.2.19 --hash=sha256:"
            + "a" * 64
            + "\nruff==0.17.4 --hash=sha256:"
            + "b" * 64
        )
        packages = parse_lockfile(lock_text)
        self.assertEqual(
            packages,
            [
                {"name": "Django", "version": "5.2.19"},
                {"name": "ruff", "version": "0.17.4"},
            ],
        )

    def test_escapes_untrusted_advisory_text_for_markdown_tables(self):
        escaped = escape_table_cell('<img>|[link](javascript:alert(1))')
        self.assertIn("&lt;img&gt;", escaped)
        self.assertIn("\\|", escaped)
        self.assertIn("\\[link\\]", escaped)

    def test_rejects_unpinned_and_duplicate_normalized_entries(self):
        with self.assertRaises(ValueError):
            parse_lockfile("Django>=5.2")
        with self.assertRaises(ValueError):
            parse_lockfile("some_pkg==1.0\nsome-pkg==2.0")

    def test_rejects_empty_lock(self):
        with self.assertRaises(ValueError):
            parse_lockfile("# comments only")

    def test_requires_explicit_utc_expiry(self):
        with self.assertRaises(ValueError):
            parse_utc("2026-12-01T00:00:00")
        self.assertEqual(
            parse_utc("2026-12-01T00:00:00Z").utcoffset().total_seconds(),
            0,
        )

    def test_reports_due_and_expired_approved_exceptions_only(self):
        now = datetime(2026, 11, 11, 12, tzinfo=UTC)
        register = {
            "schema_version": 1,
            "exceptions": [
                {
                    "exception_id": "EX-1",
                    "severity": "HIGH",
                    "status": "APPROVED",
                    "expires_at_utc": "2026-11-25T00:00:00Z",
                    "record_reference": "restricted-record-1",
                },
                {
                    "exception_id": "EX-2",
                    "severity": "LOW",
                    "status": "APPROVED",
                    "expires_at_utc": "2026-11-10T00:00:00Z",
                    "record_reference": "restricted-record-2",
                },
                {
                    "exception_id": "EX-3",
                    "severity": "MEDIUM",
                    "status": "PROPOSED",
                    "expires_at_utc": "2026-11-12T00:00:00Z",
                    "record_reference": "restricted-record-3",
                },
            ],
        }
        self.assertEqual(
            evaluate_exceptions(register, now),
            [
                {"id": "EX-1", "kind": "EXPIRY_REMINDER", "days_left": 14},
                {"id": "EX-2", "kind": "EXPIRED", "days_left": -1},
            ],
        )

    def test_rejects_duplicate_exception_ids_and_non_utc_time(self):
        now = datetime(2026, 11, 11, tzinfo=timezone.utc)
        entry = {
            "exception_id": "EX-1",
            "severity": "HIGH",
            "status": "APPROVED",
            "expires_at_utc": "2026-11-12T00:00:00Z",
            "record_reference": "restricted-ref",
        }
        with self.assertRaises(ValueError):
            evaluate_exceptions(
                {"schema_version": 1, "exceptions": [entry, entry]}, now
            )
        with self.assertRaises(ValueError):
            evaluate_exceptions(
                {"schema_version": 1, "exceptions": []}, datetime(2026, 11, 11)
            )


if __name__ == "__main__":
    unittest.main()
