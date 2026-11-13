"""Run the ORG-03 synthetic suites and emit a JUnit XML report.

This runner uses only the Python standard library so the Linux CI job remains
compatible with the repository's hash-locked dependency set.
"""

from __future__ import annotations

import argparse
import sys
import time
import traceback
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


class JUnitResult(unittest.TextTestResult):
    """Text test result that also records portable JUnit testcase data."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cases: list[dict[str, object]] = []
        self.started_at: dict[unittest.case.TestCase, float] = {}
        self.current: dict[str, object] | None = None

    def startTest(self, test):
        super().startTest(test)
        self.started_at[test] = time.monotonic()
        self.current = {
            "test": test,
            "status": "passed",
            "message": "",
            "details": "",
        }

    def addSuccess(self, test):
        super().addSuccess(test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._set_problem("failure", err)

    def addError(self, test, err):
        super().addError(test, err)
        self._set_problem("error", err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.current is not None:
            self.current["status"] = "skipped"
            self.current["message"] = reason

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        self._set_problem("skipped", err)

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        if self.current is not None:
            self.current["status"] = "failure"
            self.current["message"] = "unexpected success"

    def _set_problem(self, status, err):
        if self.current is None:
            return
        self.current["status"] = status
        self.current["message"] = str(err[1])
        self.current["details"] = "".join(traceback.format_exception(*err))

    def stopTest(self, test):
        if self.current is not None:
            self.current["duration"] = time.monotonic() - self.started_at[test]
            self.cases.append(self.current)
            self.current = None
        super().stopTest(test)


class JUnitRunner(unittest.TextTestRunner):
    resultclass = JUnitResult


def write_junit(result: JUnitResult, destination: Path) -> None:
    failures = sum(case["status"] == "failure" for case in result.cases)
    errors = sum(case["status"] == "error" for case in result.cases)
    skipped = sum(case["status"] == "skipped" for case in result.cases)
    total_time = sum(float(case.get("duration", 0.0)) for case in result.cases)
    suite = ET.Element(
        "testsuite",
        {
            "name": "ORG-03 synthetic verification",
            "tests": str(len(result.cases)),
            "failures": str(failures),
            "errors": str(errors),
            "skipped": str(skipped),
            "time": f"{total_time:.6f}",
        },
    )
    for case in result.cases:
        test = case["test"]
        testcase = ET.SubElement(
            suite,
            "testcase",
            {
                "classname": test.__class__.__module__,
                "name": test._testMethodName,
                "time": f"{float(case.get('duration', 0.0)):.6f}",
            },
        )
        status = case["status"]
        if status in {"failure", "error"}:
            node = ET.SubElement(
                testcase,
                status,
                {"message": str(case.get("message", ""))},
            )
            node.text = str(case.get("details", ""))
        elif status == "skipped":
            ET.SubElement(
                testcase,
                "skipped",
                {"message": str(case.get("message", "skipped"))},
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(suite, space="  ")
    ET.ElementTree(suite).write(destination, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--xml",
        type=Path,
        default=Path("artifacts/org03-junit.xml"),
        help="JUnit XML output path (default: artifacts/org03-junit.xml)",
    )
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repository_root))

    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite(
        [
            loader.loadTestsFromName("tests.test_org03_event_store"),
            loader.loadTestsFromName("tests.test_org03_synthetic_access_policy"),
            loader.loadTestsFromName("tests.test_org03_events"),
            loader.loadTestsFromName("tests.test_org03_roster"),
        ]
    )
    result = JUnitRunner(verbosity=2).run(suite)
    write_junit(result, args.xml)
    print(f"JUnit XML written to {args.xml}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
