"""Read-only OSV dependency monitoring and exception-expiry reminders.

Uses only the Python standard library. It never edits repository files, creates
issues, changes dependencies, approves exceptions, or changes exception status.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import re
import socket
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from html import escape as escape_html
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OSV_QUERYBATCH_URL = "https://api.osv.dev/v1/querybatch"
MAX_OSV_RESPONSE_BYTES = 2 * 1024 * 1024
OSV_REQUEST_TIMEOUT_SECONDS = 20
OSV_MAX_ATTEMPTS = 3
OSV_RETRY_BACKOFF_SECONDS = (1, 2)
# The subprocess supervisor enforces this as a hard end-to-end deadline.
OSV_RETRY_BUDGET_SECONDS = OSV_MAX_ATTEMPTS * OSV_REQUEST_TIMEOUT_SECONDS + sum(
    OSV_RETRY_BACKOFF_SECONDS
)
TRANSIENT_OSV_ERRNOS = {
    errno.ECONNABORTED,
    errno.ECONNREFUSED,
    errno.ECONNRESET,
    errno.EHOSTUNREACH,
    errno.ENETUNREACH,
    errno.EPIPE,
    errno.ETIMEDOUT,
    socket.EAI_AGAIN,
}
PINNED_REQUIREMENT = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s;\\]+)$")
SHA256_HASH_OPTION = re.compile(r"^--hash=sha256:[0-9a-fA-F]{64}$")
REMINDER_DAYS = (30, 14, 7, 3, 1)
VALID_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
VALID_STATUSES = {"PROPOSED", "APPROVED", "REJECTED", "REVOKED", "EXPIRED"}


def is_transient_transport_error(error: OSError) -> bool:
    """Return true only for known transient socket/transport failures."""
    reason = error.reason if isinstance(error, URLError) else error
    if isinstance(reason, (TimeoutError, ConnectionError)):
        return True
    return isinstance(reason, OSError) and reason.errno in TRANSIENT_OSV_ERRNOS


def parse_lockfile(text: str) -> list[dict[str, str]]:
    """Parse the repository's pinned PyPI requirements lock format strictly."""
    packages: list[dict[str, str]] = []
    seen: set[str] = set()
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        tokens = line.split()
        match = PINNED_REQUIREMENT.fullmatch(tokens[0]) if tokens else None
        if not match:
            raise ValueError(
                f"Unsupported lock entry at line {number}; expected name==version"
            )
        for option in tokens[1:]:
            if not SHA256_HASH_OPTION.fullmatch(option):
                raise ValueError(
                    f"Unsupported lock option at line {number}; "
                    "expected --hash=sha256:<64 hex>"
                )
        name, version = match.groups()
        normalized = re.sub(r"[-_.]+", "-", name).lower()
        if normalized in seen:
            raise ValueError(
                f"Duplicate normalized package name at line {number}: {name}"
            )
        seen.add(normalized)
        packages.append({"name": name, "version": version})
    if not packages:
        raise ValueError("Lockfile contains no pinned packages")
    return packages


def parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("expires_at_utc must use an explicit UTC Z suffix")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("expires_at_utc must be UTC")
    return parsed


def evaluate_exceptions(document: dict, now: datetime) -> list[dict[str, object]]:
    if not isinstance(document, dict):
        raise ValueError("Exception register must be a JSON object")
    if document.get("schema_version") != 1 or not isinstance(
        document.get("exceptions"), list
    ):
        raise ValueError(
            "Exception register must use schema_version 1 and an exceptions array"
        )
    if now.tzinfo is None or now.utcoffset() != timedelta(0):
        raise ValueError("Evaluation time must be timezone-aware UTC")
    reminders: list[dict[str, object]] = []
    identifiers: set[str] = set()
    for entry in document["exceptions"]:
        if not isinstance(entry, dict):
            raise ValueError("Each exception register entry must be an object")
        required = {
            "exception_id",
            "severity",
            "status",
            "expires_at_utc",
            "record_reference",
        }
        if not required.issubset(entry):
            raise ValueError("Exception register entry is missing required metadata")
        identifier = entry["exception_id"]
        if (
            not isinstance(identifier, str)
            or not identifier.strip()
            or identifier in identifiers
        ):
            raise ValueError("Exception IDs must be non-empty and unique")
        identifiers.add(identifier)
        severity = entry["severity"]
        status = entry["status"]
        if (
            not isinstance(severity, str)
            or severity not in VALID_SEVERITIES
            or not isinstance(status, str)
            or status not in VALID_STATUSES
        ):
            raise ValueError(f"Invalid severity or status for {identifier}")
        reference = entry["record_reference"]
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError(f"Missing non-sensitive record reference for {identifier}")
        expiry = parse_utc(entry["expires_at_utc"])
        if status != "APPROVED":
            continue
        days_left = (expiry.date() - now.date()).days
        if days_left < 0:
            reminders.append(
                {"id": identifier, "kind": "EXPIRED", "days_left": days_left}
            )
        elif days_left == 0:
            reminders.append(
                {
                    "id": identifier,
                    "kind": "EXPIRY_REMINDER",
                    "days_left": days_left,
                }
            )
        elif days_left in REMINDER_DAYS:
            reminders.append(
                {
                    "id": identifier,
                    "kind": "EXPIRY_REMINDER",
                    "days_left": days_left,
                }
            )
        elif days_left > 0:
            missed_thresholds = [
                threshold for threshold in REMINDER_DAYS if threshold > days_left
            ]
            if missed_thresholds:
                threshold = min(missed_thresholds)
                reminders.append(
                    {
                        "id": identifier,
                        "kind": "EXPIRY_REMINDER_OVERDUE",
                        "days_left": days_left,
                        "threshold_days": threshold,
                        "days_overdue": threshold - days_left,
                    }
                )
    return reminders


def query_osv(packages: list[dict[str, str]]) -> list[dict]:
    queries = [
        {
            "package": {
                "name": re.sub(r"[-_.]+", "-", package["name"]).lower(),
                "ecosystem": "PyPI",
            },
            "version": package["version"],
        }
        for package in packages
    ]
    payload = json.dumps({"queries": queries}).encode("utf-8")
    request = Request(
        OSV_QUERYBATCH_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ekhc-security-monitor/1.0",
        },
        method="POST",
    )
    raw_response = None
    for attempt in range(1, OSV_MAX_ATTEMPTS + 1):
        try:
            with urlopen(request, timeout=OSV_REQUEST_TIMEOUT_SECONDS) as response:
                raw_response = response.read(MAX_OSV_RESPONSE_BYTES + 1)
            break
        except HTTPError as error:
            retryable = error.code == 429 or 500 <= error.code <= 599
            if not retryable or attempt == OSV_MAX_ATTEMPTS:
                raise
        except OSError as error:
            if not is_transient_transport_error(error) or attempt == OSV_MAX_ATTEMPTS:
                raise
        sleep(OSV_RETRY_BACKOFF_SECONDS[attempt - 1])
    if raw_response is None:
        raise ValueError("OSV request completed without a response")
    if len(raw_response) > MAX_OSV_RESPONSE_BYTES:
        raise ValueError("OSV response exceeded the 2 MiB safety limit")
    data = json.loads(raw_response.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("OSV returned a non-object response")
    results = data.get("results")
    if not isinstance(results, list) or len(results) != len(packages):
        raise ValueError("OSV returned an incomplete or malformed batch response")
    findings = []
    for package, result in zip(packages, results, strict=True):
        if not isinstance(result, dict):
            raise ValueError("OSV returned a malformed package result")
        advisories = result.get("vulns", [])
        if not isinstance(advisories, list):
            raise ValueError("OSV returned a malformed advisory list")
        for advisory in advisories:
            if not isinstance(advisory, dict):
                raise ValueError("OSV returned a malformed advisory entry")
            findings.append(
                {
                    "package": package["name"],
                    "version": package["version"],
                    "id": advisory.get("id", "UNKNOWN-ID"),
                    "modified": advisory.get("modified", "UNKNOWN"),
                    "summary": advisory.get("summary", "No summary supplied"),
                }
            )
    return findings


def query_osv_with_deadline(packages: list[dict[str, str]]) -> list[dict]:
    """Run OSV lookup in a killable worker with a hard wall-clock deadline.

    urllib's socket timeout is an inactivity timeout. A separate process lets
    the parent terminate a worker even if a peer continuously streams bytes.
    """
    command = [sys.executable, str(Path(__file__).resolve()), "--osv-worker"]
    try:
        completed = subprocess.run(
            command,
            input=json.dumps(packages),
            capture_output=True,
            check=False,
            text=True,
            timeout=OSV_RETRY_BUDGET_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise TimeoutError(
            f"OSV worker exceeded the {OSV_RETRY_BUDGET_SECONDS}-second hard deadline"
        ) from error
    if completed.returncode != 0:
        worker_error = completed.stderr.strip() or "unspecified worker error"
        raise ValueError(f"OSV worker failed: {worker_error}")
    try:
        findings = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError("OSV worker returned malformed output") from error
    if not isinstance(findings, list) or any(
        not isinstance(item, dict) for item in findings
    ):
        raise ValueError("OSV worker returned an invalid findings collection")
    return findings


def osv_worker_main() -> int:
    """Private subprocess entry point; emits JSON only on stdout."""
    try:
        packages = json.load(sys.stdin)
        if not isinstance(packages, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get("name"), str)
            or not isinstance(item.get("version"), str)
            for item in packages
        ):
            raise ValueError("Worker input must be a list of pinned package objects")
        findings = query_osv(packages)
    except (OSError, ValueError, TypeError) as error:
        print(type(error).__name__, file=sys.stderr)
        return 1
    sys.stdout.write(json.dumps(findings, separators=(",", ":")))
    return 0


def escape_table_cell(value: object) -> str:
    escaped = escape_html(str(value).replace("\\", "\\\\"), quote=True)
    for character in ("|", "`", "[", "]", "*", "_"):
        escaped = escaped.replace(character, "\\" + character)
    return escaped.replace("\r", " ").replace("\n", " ")


def write_summary(markdown: str) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write(markdown + "\n")
    print(markdown)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", default="requirements-lock.txt")
    parser.add_argument("--exceptions", default="docs/security/exception-register.json")
    args = parser.parse_args()
    now = datetime.now(UTC)
    try:
        packages = parse_lockfile(Path(args.lock).read_text(encoding="utf-8"))
        register = json.loads(Path(args.exceptions).read_text(encoding="utf-8"))
        reminders = evaluate_exceptions(register, now)
        findings = query_osv_with_deadline(packages)
    except (OSError, ValueError) as error:
        message = (
            "## Security monitoring — INCOMPLETE\n\n"
            f"Monitoring could not complete: {type(error).__name__}. See job logs."
        )
        write_summary(message)
        return 2

    lines = [
        "## Read-only security monitoring",
        f"- Evaluation time: {now.isoformat()}",
        f"- Locked PyPI packages queried: {len(packages)}",
        f"- OSV advisories returned: {len(findings)}",
        f"- Approved exception reminders/expiries: {len(reminders)}",
        "",
    ]
    if findings:
        lines.extend(
            [
                "### Advisory findings",
                "| Package | Locked version | Advisory | Modified | Summary |",
                "|---|---:|---|---|---|",
            ]
        )
        for item in findings:
            cells = [
                escape_table_cell(item[field])
                for field in ("package", "version", "id", "modified", "summary")
            ]
            lines.append("| " + " | ".join(cells) + " |")
    else:
        lines.append(
            "No matching OSV advisories were returned for the "
            "locked PyPI package versions."
        )
    if reminders:
        lines.extend(
            [
                "",
                "### Exception expiry signals",
                "| Exception | Signal | Days remaining | "
                "Overdue threshold | Days overdue |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for item in reminders:
            identifier = escape_table_cell(item["id"])
            threshold = item.get("threshold_days", "")
            overdue = item.get("days_overdue", "")
            lines.append(
                f"| {identifier} | {item['kind']} | {item['days_left']} "
                f"| {threshold} | {overdue} |"
            )
    else:
        lines.extend(
            [
                "",
                "No approved exception is at, past, or overdue for a configured "
                "reminder threshold.",
            ]
        )
    lines.extend(
        [
            "",
            (
                "> This workflow reports signals only. It does not assign severity, "
                "create tickets, modify dependencies, "
                "approve/revoke/expire exceptions, "
                "or deliver a guaranteed out-of-band notification. "
                "Overdue reminders may repeat on subsequent runs because no "
                "delivery state or acknowledgement is stored."
            ),
        ]
    )
    write_summary("\n".join(lines))
    return 1 if findings or reminders else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--osv-worker"]:
        sys.exit(osv_worker_main())
    sys.exit(main())
