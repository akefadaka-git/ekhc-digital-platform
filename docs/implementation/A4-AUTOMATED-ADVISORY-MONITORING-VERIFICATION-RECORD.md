# A4 Independent Verification — Automated Advisory Monitoring and Exception Expiry

**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 branch:** `a3/security-monitor-corrections` (correction branch for `a3/automated-security-advisory-monitoring`)  
**A3 implementation head reviewed:** `23f4b3efba9cca99179eae14445ea1138e35b3aa`  
**A3 base:** `974ca3c05af5cb024ee7ed45e099a9461a9a69b8`  
**A4 review date:** 2026-11-11  
**Owner acceptance:** PENDING  
**Exact-head CI:** RUNS QUEUED — quality and monitor workflows triggered, results pending  
**Technical disposition:** A4 RE-REVIEW IN PROGRESS; no closure until exact-head quality evidence is complete  
**Closure status:** NOT YET OWNER-CLOSED

## 1. Scope and method

Read-only independent review of the exact A3 head and these files:
- `.github/workflows/security-monitor.yml`
- `scripts/security_monitor.py`
- `tests/test_security_monitor.py`
- `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md`
- `docs/security/exception-register.json`
- `.github/workflows/quality.yml`

The A3 correction branch has advanced to `23f4b3efba9cca99179eae14445ea1138e35b3aa`. The comparison from prior corrected head `32812969c1ad13eccc681721d58c79a1d58dfa36` reports **4 commits ahead, 0 behind, exactly four changed paths**: the A3 correction report added, `scripts/security_monitor.py` modified, `tests/test_security_monitor.py` modified, and pre-existing `tests/test_supply_chain_baseline.py` modified to resolve two repository-wide lint findings. The lockfile, dependency manifests, workflow, runtime application configuration, and application behavior were not changed in this correction increment.

The A3-owned files received import-order and line-length corrections; the existing supply-chain test file received its two lint corrections. Ruff rules and the full-repository `ruff check .` command remain unchanged. This is a source-level correction only until the exact-head workflow finishes.

## 2. Monitoring workflow review

**Result: PASS WITH LIMITATIONS**

- Workflow/job permissions are explicitly `contents: read`.
- Checkout uses a full 40-character action SHA and `persist-credentials: false`.
- Python setup action is pinned to a full 40-character SHA.
- No secrets, write token, package publishing, artifact upload, deployment, OIDC permission, or repository mutation step is present.
- The workflow has a 10-minute job timeout and invokes the monitor script directly.
- Schedule is `15 6 * * *` (06:15 UTC daily); manual dispatch is available.
- Push validation is limited to `a3/**`; pull-request validation targets `main`.
- GitHub scheduled workflows run only from the default branch. Since this workflow is on a non-default A3 branch and has not been merged, scheduled execution is not active. Manual dispatch or branch-triggered validation is distinct from scheduled operation.
- The PR workflow executes repository code with read-only token permissions and no configured secrets in this job. This reduces credential impact but is not a sandbox or network-egress isolation control.

**Prior exact-head execution evidence:** security monitor run #19 / ID `43074972062` on prior corrected head `32812969c1ad13eccc681721d58c79a1d58dfa36` completed SUCCESS (32 packages queried; zero advisories; empty exception register). This is historical evidence for that prior SHA, not evidence for the new head.

**Current exact-head execution:** security monitor run #23 / ID `43099104462` on `23f4b3efba9cca99179eae14445ea1138e35b3aa` is **QUEUED**. No current-head monitoring result is claimed.

## 3. Lock parser review

**Result: PASS WITH LIMITATIONS**

- Parser rejects unpinned entries, duplicate normalized names, unsupported lines, and empty lockfiles.
- It accepts the repository's current pinned requirements format with hash options.
- It is a purpose-built line parser, not a complete pip requirements parser.
- It does not validate hash-option syntax, prove that every lock entry has a hash, or independently establish lockfile integrity/provenance. Those controls remain the responsibility of the hash-required installation and separate supply-chain assurance process.
- The parser's acceptance of arbitrary trailing text after whitespace should not be treated as validation of the full lock grammar.

## 4. OSV response handling

**Result: PASS WITH LIMITATIONS**

Positive controls:
- Uses HTTPS OSV querybatch endpoint, POST JSON, and a 20-second urllib timeout.
- Checks that response is an object, `results` is a list with exactly one result per package, each result is an object, `vulns` is a list, and each advisory is an object.
- Uses strict zip length checking and fails incomplete/malformed batches rather than silently treating them as clean.
- Network, JSON, and input errors produce an INCOMPLETE summary and non-zero exit.
- Untrusted advisory fields are escaped before inclusion in Markdown table cells.

Limitations:
- Response body is now bounded to 2 MiB by reading at most `MAX_OSV_RESPONSE_BYTES + 1` and rejecting an oversized response through the INCOMPLETE/non-zero path. A mocked regression test covers the oversized-response case.
- No retry/backoff or independent OSV availability check is implemented.
- Advisory field types and semantic completeness (for example, a meaningful ID and timestamp) are not validated; fallback display values are used.
- A successful empty OSV response means only that OSV returned no matching records for these queried package identities/versions at that time. It does not prove absence of vulnerabilities or completeness/freshness of OSV coverage.
- The exact-head live OSV workflow run is evidenced (32 packages; zero advisories returned). A mocked valid-advisory parser test and malformed/incomplete-batch and oversized-response tests are present. No real positive advisory match was returned, so end-to-end rendering of a live advisory remains unverified.

## 5. Exception-expiry logic

**Result: PASS WITH LIMITATIONS**

- Requires schema version 1, an exceptions array, unique non-empty identifiers, valid severity/status enums, a non-empty record reference, and an explicit UTC `Z` expiry timestamp.
- Only `APPROVED` entries generate signals.
- Emits configured reminders at 30, 14, 7, 3, and 1 calendar days, on the expiry date, and an EXPIRED signal on every run after expiry.
- Does not modify status, approve, renew, revoke, extend, or accept risk.
- The committed register is empty; no real exception record or real notification is demonstrated.
- Reminder thresholds are exact-day matches. A missed scheduled run on a threshold day is not replayed as that specific reminder later, although expiry-day and overdue signals remain available.
- This is a reminder evaluator, not an enforcement mechanism. It does not automatically disable a dependency or make an exception invalid in another system.

## 6. Test review and concrete defect

**Prior-head result: SOURCE DEFECT CORRECTED; 64 TESTS PASS; LINT FAILS. Current-head validation pending.**

The prior undefined `timezone.utc` reference is corrected to the imported `UTC`. The corrected test module contains ten test methods, including mocked tests for oversized OSV responses, incomplete batch responses, and a valid matching advisory. The prior deterministic NameError is no longer present in the fetched exact-head source.

Prior exact-head A3 quality run #134 / ID `43074971731` (job `130712307471`) completed FAILURE on SHA `32812969c1ad13eccc681721d58c79a1d58dfa36`. The Django system check passed and the complete Django suite passed: **64 tests, 0 failures**. Ruff lint then failed with **8 findings**:
- `scripts/security_monitor.py`: one import-order finding and three line-length findings;
- `tests/test_security_monitor.py`: one import-order finding and one line-length finding;
- existing `tests/test_supply_chain_baseline.py`: one import-order finding and one line-length finding.

The last two findings are in a file outside the seven paths changed by this A3 increment; they are existing repository-wide lint debt surfaced by the full-repository Ruff command, not changes introduced by this branch. Ruff format check and dependency vulnerability audit were skipped because the lint step failed.

Those eight findings were corrected in the current increment: six in the two A3-owned files and two in the pre-existing supply-chain test file. The full lint command and configured Ruff rule set were retained. **Current-head test and lint results are pending** the exact-head quality run.

## 7. Notification and operational limitations

**Result: PARTIAL / NOT VERIFIED**

- The monitor appends a GitHub Actions job summary and prints to stdout.
- Non-zero exit codes make findings/reminders and incomplete monitoring visible as failed runs.
- No explicit email, mobile push, webhook, issue, or out-of-band notification delivery is implemented.
- GitHub notification preferences, watch settings, recipient subscriptions, and delivery were not verified.
- A workflow failure is not proof that an accountable person received or acknowledged an alert.
- Daily schedule remains inactive until the workflow is present on the default branch and separately approved/merged.
- The exception register is empty and contains no real approved exceptions.
- No production adoption, operational rota, response acknowledgement, or escalation exercise is evidenced.

## 8. CI and repository evidence

- Prior-head workflow evidence is retained above for audit history. Current exact-head push runs are:
  - A3 quality run #138, ID `43099104469`, exact SHA `23f4b3efba9cca99179eae14445ea1138e35b3aa`: **QUEUED**. [Run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43099104469)
  - Security monitor run #23, ID `43099104462`, same exact SHA: **QUEUED**. [Run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43099104462)
- Three intermediate push commits also generated queued runs (#136/#137 and #137/#22); these are not substitutes for the final exact-head run. The latest exact-head quality job ID is `130784772500` and has not started (no steps reported).
- **Current exact-head CI: QUEUED / NOT YET VERIFIED.** The earlier test/lint outcome applies only to the prior SHA and is not projected onto this head.
- `main` was fetched at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823` and remains unchanged in this review.
- No merge, deployment, signing, publication, dependency update, production-data access, or exception approval was performed.

## 9. Required follow-up

1. Obtain completion evidence for quality run #138 at exact head `23f4b3efba9cca99179eae14445ea1138e35b3aa`; inspect test, Ruff lint, Ruff format, and pip-audit steps/logs. If any fail, correct and rerun on the new exact head.
2. Obtain completion evidence for security-monitor run #23 at the same exact head.
3. Add coverage for OSV HTTP/network failures, all reminder boundaries, missed-run behavior, and end-to-end exit-code/reporting semantics.
4. Validate notification delivery and escalation with a controlled, non-sensitive test before operational adoption.
5. Keep the daily schedule inactive until the workflow is present on the default branch following separate approval and integration.
6. Preserve the empty exception register as an honest state; no exception approval or risk acceptance is implied.

## 10. Disposition

**Source correction: COMMITTED — six A3-owned Ruff findings and two pre-existing repository-wide Ruff findings addressed; no lint rules or coverage weakened.**  
**Current-head test execution: NOT YET RUN — quality run queued.**  
**Current-head Ruff lint/format: NOT YET RUN — quality run queued.**  
**Current-head dependency audit: NOT YET RUN — quality run queued.**  
**Current-head security monitor: QUEUED.**  
**Exact-head CI: QUEUED / NOT YET VERIFIED.**  
**Operational adoption: PARTIAL / NOT VERIFIED.**  
**Owner acceptance: PENDING.**  
**Closure: NOT YET OWNER-CLOSED; await exact-head workflow evidence before A4 closure.

This A4 record does not authorize merge, deployment, publication, signing, automatic dependency changes, exception approval, or A5.