import io
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from scripts.security_monitor import (
    MAX_OSV_RESPONSE_BYTES,
    OSV_MAX_ATTEMPTS,
    OSV_REQUEST_TIMEOUT_SECONDS,
    OSV_RETRY_BACKOFF_SECONDS,
    OSV_RETRY_BUDGET_SECONDS,
    escape_table_cell,
    evaluate_exceptions,
    main,
    parse_lockfile,
    parse_utc,
    query_osv,
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
        escaped = escape_table_cell("<img>|[link](javascript:alert(1))")
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

    @patch("scripts.security_monitor.urlopen")
    def test_osv_rejects_oversized_response(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = b"x" * (
            MAX_OSV_RESPONSE_BYTES + 1
        )
        with self.assertRaisesRegex(ValueError, "2 MiB safety limit"):
            query_osv([{"name": "Django", "version": "5.2.19"}])

    @patch("scripts.security_monitor.urlopen")
    def test_osv_rejects_incomplete_batch_response(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = (
            b'{"results":[]}'
        )
        with self.assertRaisesRegex(ValueError, "incomplete or malformed"):
            query_osv([{"name": "Django", "version": "5.2.19"}])

    @patch("scripts.security_monitor.urlopen")
    def test_osv_parses_matching_advisory(self, mocked_urlopen):
        payload = (
            b'{"results":[{"vulns":[{"id":"GHSA-test",'
            b'"modified":"2026-01-01T00:00:00Z","summary":"test"}]}]}'
        )
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = payload
        result = query_osv([{"name": "Django", "version": "5.2.19"}])
        self.assertEqual(result[0]["id"], "GHSA-test")
        self.assertEqual(result[0]["package"], "Django")

    def test_rejects_duplicate_exception_ids_and_non_utc_time(self):
        now = datetime(2026, 11, 11, tzinfo=UTC)
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

    def test_missed_reminder_reports_nearest_threshold_and_overdue_days(self):
        now = datetime(2026, 11, 11, 12, tzinfo=UTC)
        register = {
            "schema_version": 1,
            "exceptions": [
                {
                    "exception_id": "EX-OVERDUE",
                    "severity": "HIGH",
                    "status": "APPROVED",
                    "expires_at_utc": "2026-11-21T00:00:00Z",
                    "record_reference": "restricted-ref",
                },
                {
                    "exception_id": "EX-NOT-APPROVED",
                    "severity": "LOW",
                    "status": "PROPOSED",
                    "expires_at_utc": "2026-11-21T00:00:00Z",
                    "record_reference": "restricted-ref-2",
                },
            ],
        }
        self.assertEqual(
            evaluate_exceptions(register, now),
            [
                {
                    "id": "EX-OVERDUE",
                    "kind": "EXPIRY_REMINDER_OVERDUE",
                    "days_left": 10,
                    "threshold_days": 14,
                    "days_overdue": 4,
                }
            ],
        )

    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_retries_only_retryable_statuses_with_bounded_backoff(
        self, mocked_urlopen, mocked_sleep
    ):
        successful_response = io.BytesIO(b'{"results":[{"vulns":[]}]}')
        mocked_urlopen.side_effect = [
            HTTPError(
                "https://api.osv.dev/v1/querybatch", 503, "Unavailable", {}, None
            ),
            HTTPError(
                "https://api.osv.dev/v1/querybatch", 429, "Rate limited", {}, None
            ),
            successful_response,
        ]
        self.assertEqual(query_osv([{"name": "Django", "version": "5.2.19"}]), [])
        self.assertEqual(mocked_urlopen.call_count, OSV_MAX_ATTEMPTS)
        self.assertEqual(
            [call.args[0] for call in mocked_sleep.call_args_list],
            list(OSV_RETRY_BACKOFF_SECONDS),
        )
        self.assertTrue(
            all(
                call.kwargs["timeout"] == OSV_REQUEST_TIMEOUT_SECONDS
                for call in mocked_urlopen.call_args_list
            )
        )
        self.assertEqual(OSV_RETRY_BUDGET_SECONDS, 63)  # Nominal, not a hard deadline.

    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_does_not_retry_non_retryable_http_status(
        self, mocked_urlopen, mocked_sleep
    ):
        mocked_urlopen.side_effect = HTTPError(
            "https://api.osv.dev/v1/querybatch", 404, "Not found", {}, None
        )
        with self.assertRaises(HTTPError):
            query_osv([{"name": "Django", "version": "5.2.19"}])
        mocked_urlopen.assert_called_once()
        mocked_sleep.assert_not_called()

    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_retries_transient_transport_errors_at_most_three_times(
        self, mocked_urlopen, mocked_sleep
    ):
        mocked_urlopen.side_effect = URLError(
            ConnectionResetError("temporary connection failure")
        )
        with self.assertRaises(URLError):
            query_osv([{"name": "Django", "version": "5.2.19"}])
        self.assertEqual(mocked_urlopen.call_count, OSV_MAX_ATTEMPTS)
        self.assertEqual(mocked_sleep.call_count, OSV_MAX_ATTEMPTS - 1)

    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_does_not_retry_non_transient_url_error(
        self, mocked_urlopen, mocked_sleep
    ):
        mocked_urlopen.side_effect = URLError("certificate verification failed")
        with self.assertRaises(URLError):
            query_osv([{"name": "Django", "version": "5.2.19"}])
        mocked_urlopen.assert_called_once()
        mocked_sleep.assert_not_called()

    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_does_not_retry_malformed_response(self, mocked_urlopen, mocked_sleep):
        mocked_urlopen.return_value = io.BytesIO(b"not-json")
        with self.assertRaises(ValueError):
            query_osv([{"name": "Django", "version": "5.2.19"}])
        mocked_urlopen.assert_called_once()
        mocked_sleep.assert_not_called()

    @patch("scripts.security_monitor.write_summary")
    @patch("scripts.security_monitor.query_osv")
    def test_main_renders_synthetic_positive_advisory_and_returns_finding_status(
        self, mocked_query, mocked_summary
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lockfile = root / "requirements-lock.txt"
            register = root / "exception-register.json"
            lockfile.write_text("Django==5.2.19\n", encoding="utf-8")
            register.write_text(
                '{"schema_version":1,"exceptions":[]}', encoding="utf-8"
            )
            mocked_query.return_value = [
                {
                    "package": "Django",
                    "version": "5.2.19",
                    "id": "GHSA-SYNTHETIC",
                    "modified": "2026-01-01T00:00:00Z",
                    "summary": "<script>|synthetic advisory</script>",
                }
            ]
            with patch(
                "sys.argv",
                [
                    "security_monitor.py",
                    "--lock",
                    str(lockfile),
                    "--exceptions",
                    str(register),
                ],
            ):
                result = main()
        self.assertEqual(result, 1)
        report = mocked_summary.call_args.args[0]
        self.assertIn("GHSA-SYNTHETIC", report)
        self.assertIn("Django", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertNotIn("<script>", report)


    @patch("scripts.security_monitor.sleep")
    @patch("scripts.security_monitor.urlopen")
    def test_osv_http_429_and_5xx_exhaustion_uses_exactly_three_attempts(
        self, mocked_urlopen, mocked_sleep
    ):
        mocked_urlopen.side_effect = [
            HTTPError(
                "https://api.osv.dev/v1/querybatch", 429, "Rate limited", {}, None
            ),
            HTTPError(
                "https://api.osv.dev/v1/querybatch", 503, "Unavailable", {}, None
            ),
            HTTPError(
                "https://api.osv.dev/v1/querybatch", 500, "Server error", {}, None
            ),
        ]
        with self.assertRaises(HTTPError):
            query_osv([{"name": "Django", "version": "5.2.19"}])
        self.assertEqual(mocked_urlopen.call_count, 3)
        self.assertEqual(
            [call.args[0] for call in mocked_sleep.call_args_list], [1, 2]
        )

    @patch("scripts.security_monitor.write_summary")
    @patch(
        "scripts.security_monitor.query_osv",
        side_effect=URLError("temporary network failure"),
    )
    @patch(
        "scripts.security_monitor.parse_lockfile",
        return_value=[{"name": "Django", "version": "5.2.19"}],
    )
    @patch("scripts.security_monitor.evaluate_exceptions", return_value=[])
    def test_main_reports_incomplete_and_returns_two_on_osv_failure(
        self, mocked_evaluate, mocked_parse, mocked_query, mocked_summary
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lockfile = root / "requirements-lock.txt"
            register = root / "exception-register.json"
            lockfile.write_text("Django==5.2.19", encoding="utf-8")
            register.write_text(
                '{"schema_version":1,"exceptions":[]}', encoding="utf-8"
            )
            with patch(
                "sys.argv",
                [
                    "security_monitor.py",
                    "--lock",
                    str(lockfile),
                    "--exceptions",
                    str(register),
                ],
            ):
                result = main()
        self.assertEqual(result, 2)
        report = mocked_summary.call_args.args[0]
        self.assertIn("Security monitoring — INCOMPLETE", report)
        self.assertIn("Monitoring could not complete", report)
        mocked_parse.assert_called_once()
        mocked_evaluate.assert_called_once()
        mocked_query.assert_called_once()

    def test_lock_parser_accepts_only_sha256_hash_options(self):
        valid_hash = "a" * 64
        parsed = parse_lockfile(f"Django==5.2.19 --hash=sha256:{valid_hash}")
        self.assertEqual(parsed, [{"name": "Django", "version": "5.2.19"}])
        for invalid in (
            "Django==5.2.19 --index-url=https://example.invalid",
            "Django==5.2.19 --hash=sha256:abcd",
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                parse_lockfile(invalid)


if __name__ == "__main__":
    unittest.main()
