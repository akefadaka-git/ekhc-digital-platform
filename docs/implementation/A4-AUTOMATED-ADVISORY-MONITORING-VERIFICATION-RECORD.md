# A4 Independent Verification — Automated Advisory Monitoring and Exception Expiry

**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 branch:** `a3/security-monitor-corrections` (correction branch for `a3/automated-security-advisory-monitoring`)  
**A3 implementation head reviewed:** `b4ed07262b1366e49f566cfadc9af3f892abfa14`  
**A3 base:** `974ca3c05af5cb024ee7ed45e099a9461a9a69b8`  
**A4 review date:** 2026-11-12  
**Owner acceptance:** PENDING  
**Exact-head CI:** QUALITY RUN #147 SUCCESS; MONITOR RUN #32 SUCCESS  
**Technical disposition:** A4 TECHNICAL VERIFICATION PASS WITH LIMITATIONS; AWAITING OWNER ACCEPTANCE  
**Closure status:** NOT YET OWNER-CLOSED

## 1. Scope and method

Read-only independent review of the exact A3 head and these files:
- `.github/workflows/security-monitor.yml`
- `scripts/security_monitor.py`
- `tests/test_security_monitor.py`
- `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md`
- `docs/security/exception-register.json`
- `.github/workflows/quality.yml`

The A3 correction branch now points to `b4ed07262b1366e49f566cfadc9af3f892abfa14`. The correction scope remains limited to the A3 correction report, scripts/security_monitor.py, tests/test_security_monitor.py, and pre-existing tests/test_supply_chain_baseline.py. The lockfile, dependency manifests, quality workflow, runtime application configuration, and application behavior remain unchanged. The latest correction applies only Ruff-reported formatting changes to the three files; lint rules, lint scope, tests, dependencies, and runtime behavior are unchanged.

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

**Current exact-head execution:** security monitor run #32 / ID `43122480518` on `b4ed07262b1366e49f566cfadc9af3f892abfa14` completed **SUCCESS**. It queried 32 locked PyPI packages, returned zero OSV advisories, and emitted zero exception-expiry signals because the exception register is empty. This is a successful point-in-time query, not proof of no vulnerabilities or complete OSV coverage. Earlier run #23 / ID `43099104462` was cancelled with zero jobs returned and has no execution result.

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

**Current exact-head result: PASS — quality run #147 / ID `43122480532` completed successfully on `b4ed07262b1366e49f566cfadc9af3f892abfa14`.** Django system check passed; all 64 tests passed; `ruff check .` passed with “All checks passed!”; `ruff format --check .` passed with 51 files already formatted; `pip-audit -r requirements-lock.txt` passed with “No known vulnerabilities found”. All five workflow quality stages completed successfully on Python 3.14.10 using the hash-locked requirements.

The deterministic timezone.utc defect was corrected to use imported UTC. The test module includes regression cases for oversized OSV responses, incomplete batch responses, and a valid matching advisory.

Quality history:
- Run #138 / ID 43099104469, head 23f4b3efba9cca99179eae14445ea1138e35b3aa: retry completed with system check PASS and 64 tests PASS, but Ruff lint failed with five findings (three E501 in scripts/security_monitor.py, one I001 and one E501 in tests/test_supply_chain_baseline.py). Ruff format and pip-audit were skipped.
- Runs #140, #141, and #142 each passed system check and all 64 tests but failed Ruff lint on the remaining I001 in the pre-existing supply-chain test file. Ruff format and pip-audit were skipped.
- Run #143 / ID 43122251234, head a33e1907964397c7ab3a0837dc5c3db00324cb94: system check PASS, 64 tests PASS, Ruff lint PASS; Ruff format failed and identified three files: scripts/security_monitor.py, tests/test_security_monitor.py, tests/test_supply_chain_baseline.py. pip-audit was skipped.
- Run #144 / ID 43122390947, head d426c3fba4d9513b36b1fb0b489df71e16402e72: system check PASS, 64 tests PASS, Ruff lint PASS; Ruff format failed with the same three files. pip-audit was skipped.
- Formatter-reported changes were applied to those three files, using the exact Ruff output: module-docstring spacing and one wrapped expression in the monitor script; quote and expression layout in its tests; and one assertion layout in the supply-chain test.
- Intermediate quality run #145 / ID 43122470468 targeted 86b5cf9e35d73a71c4400aa6587924318079e2ee and was IN PROGRESS with no steps reported at the time of the earlier inspection. It is not the final head.
- Run #146 / ID 43122475763 on 3ae70be144992dfde196108bab04733aaf47da7a was cancelled before jobs were returned.
- Final-head quality run #147 / ID 43122480532 targets b4ed07262b1366e49f566cfadc9af3f892abfa14 and completed SUCCESS. Its inspected logs confirm Django system check PASS, 64 tests PASS, Ruff lint PASS, Ruff format PASS (51 files already formatted), and pip-audit PASS (no known vulnerabilities found). Do not infer quality results from prior heads; this result is specific to the recorded final SHA.

The final exact-head run must complete and its test, Ruff lint, Ruff format, and pip-audit steps/logs must be inspected before A4 can close.

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

- Quality run #143 passed system check, 64 tests, and Ruff lint, but failed Ruff format; pip-audit was skipped.
- Quality run #144 passed system check, 64 tests, and Ruff lint, but failed Ruff format; pip-audit was skipped.
- Formatter changes were committed in the final A3 correction sequence. Intermediate run #145 remains in progress on a non-final SHA; run #146 was cancelled.
- Final-head A3 quality run #147 / ID 43122480532 targets exact SHA b4ed07262b1366e49f566cfadc9af3f892abfa14 and completed SUCCESS. All five quality workflow stages completed successfully. [Run #147](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43122480532)
- Security monitor run #32 / ID 43122480518 on the final A3 head b4ed07262b1366e49f566cfadc9af3f892abfa14 completed SUCCESS. The job and logs were inspected: 32 locked PyPI packages queried; zero OSV advisories returned; zero exception reminders/expiries; exception register empty. [Run #32](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43122480518)
- Earlier monitor runs #28–#31 succeeded on their respective heads; #32 is the current-head evidence.
- The exact current A3 branch head is b4ed07262b1366e49f566cfadc9af3f892abfa14. main was fetched and remains adfa62eccda93c8b261e5abd3cbdb22cf28c8823.
- No merge, deployment, signing, publication, dependency update, production-data access, or exception approval was performed.

## 9. Required follow-up

1. Preserve the successful exact-head quality and monitor run evidence; no further CI correction is currently indicated.
2. Retain successful final-head monitoring evidence from run #32, with its zero-result and empty-register limitations.
3. Add further coverage for OSV HTTP/network failures, every reminder boundary, missed-run behavior, and end-to-end exit-code/reporting semantics.
4. Validate notification delivery and escalation with a controlled, non-sensitive test before operational adoption.
5. Keep the daily schedule inactive until the workflow is present on the default branch following separate approval and integration.
6. Preserve the empty exception register as an honest state; no exception approval or risk acceptance is implied.

## 10. Disposition

**Source corrections: COMMITTED — the six A3-owned Ruff findings and two pre-existing repository-wide Ruff findings were addressed without weakening lint rules or coverage.**  
**Final-head test execution: PASS — 64 tests on run #147.**  
**Final-head Ruff lint/format: PASS — full-repository Ruff lint and format checks on run #147.**  
**Final-head dependency audit: PASS — pip-audit reported no known vulnerabilities on run #147.**  
**Final-head security monitor: PASS — run #32; 32 packages queried, zero advisories returned, zero exception signals, empty register.**  
**Exact-head CI: PASS — quality run #147 and monitor run #32 both succeeded on the same A3 head.**  
**Operational adoption: PARTIAL / NOT VERIFIED.**  
**Owner acceptance: PENDING.**  
**Closure: NOT YET OWNER-CLOSED; technical evidence is complete with limitations, and explicit Owner acceptance remains pending.**

This A4 record does not authorize merge, deployment, publication, signing, automatic dependency changes, exception approval, or A5.