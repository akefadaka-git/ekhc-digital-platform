# A4 Independent Verification — Automated Advisory Monitoring and Exception Expiry

**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 branch:** `a3/security-monitor-corrections` (correction branch for `a3/automated-security-advisory-monitoring`)  
**A3 implementation head reviewed:** `32812969c1ad13eccc681721d58c79a1d58dfa36`  
**A3 base:** `974ca3c05af5cb024ee7ed45e099a9461a9a69b8`  
**A4 review date:** 2026-11-11  
**Owner acceptance:** PENDING  
**Exact-head CI:** CONFIRMED — MIXED (monitor SUCCESS; quality FAILURE)  
**Technical disposition:** PASS WITH MATERIAL LIMITATIONS; quality gate remains failed  
**Closure status:** NOT YET OWNER-CLOSED

## 1. Scope and method

Read-only independent review of the exact A3 head and these files:
- `.github/workflows/security-monitor.yml`
- `scripts/security_monitor.py`
- `tests/test_security_monitor.py`
- `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md`
- `docs/security/exception-register.json`
- `.github/workflows/quality.yml`

The A3 compare from base `974ca3c05af5cb024ee7ed45e099a9461a9a69b8` to corrected head `32812969c1ad13eccc681721d58c79a1d58dfa36` reports **22 commits ahead, 0 behind, and seven changed paths**: `.github/workflows/quality.yml` modified and six files added. The correction sub-compare from initial implementation head `585555868fc3fcea8a925cd8148e9b859401f122` to corrected head reports **4 commits ahead, 0 behind, exactly two changed code paths**: `scripts/security_monitor.py` and `tests/test_security_monitor.py`.

The A4 review inspected the corrected script and test source, exact-head Actions run metadata, job steps, and job logs. Only this A4 verification record is changed by the present A4 update; no A3 source, workflow, test, lockfile, dependency, or runtime file is modified.

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

**Exact-head execution evidence:** the security monitor workflow ran on corrected head `32812969c1ad13eccc681721d58c79a1d58dfa36`, run #19 / ID `43074972062`, job ID `130712305036`, and completed SUCCESS. It ran at `2026-11-11T18:09:05Z` on Ubuntu 24.04 / Python 3.14.10. The job log records 32 locked PyPI packages queried, zero OSV advisories returned, and zero approved-exception reminders/expiries (the committed register is empty). This confirms one live run, not continuous scheduled operation or complete advisory-source coverage.

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

**Result: SOURCE DEFECT CORRECTED; TESTS PASS; LINT FAILS**

The prior undefined `timezone.utc` reference is corrected to the imported `UTC`. The corrected test module contains ten test methods, including mocked tests for oversized OSV responses, incomplete batch responses, and a valid matching advisory. The prior deterministic NameError is no longer present in the fetched exact-head source.

Exact-head A3 quality run #134 / ID `43074971731` (job `130712307471`) completed FAILURE on the corrected SHA. The Django system check passed and the complete Django suite passed: **64 tests, 0 failures**. Ruff lint then failed with **8 findings**:
- `scripts/security_monitor.py`: one import-order finding and three line-length findings;
- `tests/test_security_monitor.py`: one import-order finding and one line-length finding;
- existing `tests/test_supply_chain_baseline.py`: one import-order finding and one line-length finding.

The last two findings are in a file outside the seven paths changed by this A3 increment; they are existing repository-wide lint debt surfaced by the full-repository Ruff command, not changes introduced by this branch. Ruff format check and dependency vulnerability audit were skipped because the lint step failed.

**Required correction before A4 closure:** fix all six findings in the two A3-owned files, decide separately whether to repair or explicitly scope the two pre-existing findings without weakening lint coverage, then rerun the exact-head quality workflow. Do not treat the passing test step as a passing quality gate.

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

- Direct GitHub Actions API lookup confirmed two push-triggered runs on exact head `32812969c1ad13eccc681721d58c79a1d58dfa36`:
  - Security monitor run #19, ID `43074972062`, job `130712305036`: **SUCCESS**. [Run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43074972062)
  - A3 quality run #134, ID `43074971731`, job `130712307471`: **FAILURE** at Ruff lint. [Run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43074971731)
- Quality steps: checkout, required-file gate, Python 3.14.10 setup, hash-locked requirements install, Django system check, and Django tests all PASS; Ruff lint FAIL; Ruff format and pip-audit SKIPPED.
- The security monitor log confirms the live OSV query outcome and empty exception register as recorded in Section 2.
- **Exact-head CI: CONFIRMED — MIXED.** No claim of overall CI success is made.
- `main` was fetched at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823` and remains unchanged in this review.
- No merge, deployment, signing, publication, dependency update, production-data access, or exception approval was performed.

## 9. Required follow-up

1. Correct the six Ruff findings in the two A3-owned files and rerun the exact-head quality workflow; address the two pre-existing repository-wide Ruff findings without weakening lint enforcement.
2. Add coverage for OSV HTTP/network failures, all reminder boundaries, missed-run behavior, and end-to-end exit-code/reporting semantics.
3. Validate notification delivery and escalation with a controlled, non-sensitive test before operational adoption.
4. Keep the daily schedule inactive until the workflow is present on the default branch following separate approval and integration.
5. Preserve the empty exception register as an honest state; no exception approval or risk acceptance is implied.

## 10. Disposition

**Technical result: PASS WITH MATERIAL LIMITATIONS; source defect corrected, but repository quality gate remains failed.**  
**Test execution: PASS — 64 tests.**  
**Ruff lint: FAIL — 8 findings; format and dependency audit SKIPPED.**  
**Security monitor execution: PASS — exact-head run confirmed; 32 packages queried, zero advisories returned, empty exception register.**  
**Exact-head CI: CONFIRMED — MIXED, NOT GREEN.**  
**Operational adoption: PARTIAL / NOT VERIFIED.**  
**Owner acceptance: PENDING.**  
**Closure: NOT YET OWNER-CLOSED; A3 lint corrections and a green exact-head quality run remain required.

This A4 record does not authorize merge, deployment, publication, signing, automatic dependency changes, exception approval, or A5.