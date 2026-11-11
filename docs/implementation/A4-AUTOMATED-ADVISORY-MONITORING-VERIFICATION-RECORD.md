# A4 Independent Verification — Automated Advisory Monitoring and Exception Expiry

**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 branch:** `a3/automated-security-advisory-monitoring`  
**A3 implementation head reviewed:** `585555868fc3fcea8a925cd8148e9b859401f122`  
**A3 base:** `974ca3c05af5cb024ee7ed45e099a9461a9a69b8`  
**A4 review date:** 2026-11-11  
**Owner acceptance:** PENDING  
**Exact-head CI:** NOT CONFIRMED  
**Technical disposition:** PASS WITH MATERIAL LIMITATIONS  
**Closure status:** NOT YET OWNER-CLOSED

## 1. Scope and method

Read-only independent review of the exact A3 head and these files:
- `.github/workflows/security-monitor.yml`
- `scripts/security_monitor.py`
- `tests/test_security_monitor.py`
- `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md`
- `docs/security/exception-register.json`
- `.github/workflows/quality.yml`

The A3 compare from base `974ca3c05af5cb024ee7ed45e099a9461a9a69b8` to reviewed head reports 18 commits ahead, 0 behind. The compare lists seven changed paths: one workflow modified and six files added. The earlier progress message stated 19 commits ahead and eight changed files; that summary does not match the current GitHub compare response and is superseded by the exact compare evidence above.

No source, workflow, test, lockfile, dependency, or runtime files were modified during this A4 review. This record is documentation-only.

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

No evidence was available that the workflow has executed successfully at the reviewed head.

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
- Response body size is not bounded before `read()`; oversized responses can consume runner memory.
- No retry/backoff or independent OSV availability check is implemented.
- Advisory field types and semantic completeness (for example, a meaningful ID and timestamp) are not validated; fallback display values are used.
- A successful empty OSV response means only that OSV returned no matching records for these queried package identities/versions at that time. It does not prove absence of vulnerabilities or completeness/freshness of OSV coverage.
- No exact-head live OSV query or returned-advisory integration test is evidenced.

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

**Result: FAIL — test suite contains a deterministic defect**

Seven test methods are present. In `test_rejects_duplicate_exception_ids_and_non_utc_time`, the test constructs a datetime using `timezone.utc`, but the module imports only `UTC` and `datetime`. The name `timezone` is undefined and this test raises `NameError` when executed.

The same undefined name is expected to be reported by Ruff's undefined-name rule if the test file is included in linting. The quality workflow's required-file gate includes the test file and its Ruff command runs `ruff check .`; therefore the defect is a likely CI blocker. This conclusion is source inspection, not a claim that CI actually ran.

The tests cover pinned parsing, duplicate normalization, empty lock, explicit UTC, approved exception reminders/expiry, and Markdown escaping. Missing test cases include malformed OSV top-level/result payloads, oversized response handling, OSV HTTP/network failures, every reminder boundary, missed-run behavior, and end-to-end workflow output/exit codes.

**Required correction before A4 technical re-review:** replace the stale `timezone.utc` reference with imported `UTC` (or import `timezone`), then run tests and Ruff at the exact corrected head.

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

- Exact-head workflow lookup returned no runs.
- **Exact-head CI: NOT CONFIRMED.** No pass, failure, or cancellation is inferred.
- The current lookup wrapper is limited to pull-request-triggered runs; its empty result does not establish that no push or manual run exists.
- `main` was fetched at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823` and remains unchanged in this review.
- No merge, deployment, signing, publication, dependency update, production-data access, or exception approval was performed.

## 9. Required follow-up

1. Fix the undefined `timezone` test reference on a separate A3 correction commit.
2. Run exact-head quality workflow and preserve full run/job evidence; do not mark CI passed until verified.
3. Add bounded OSV response reads and tests for malformed/oversized responses and network failures.
4. Add deterministic tests for all reminder boundaries, missed-run behavior, and exit-code/reporting semantics.
5. Validate notification delivery and escalation with a controlled, non-sensitive test before operational adoption.
6. Keep the schedule inactive until a separately approved default-branch integration.
7. Conduct a focused A4 re-review against the corrected exact head.

## 10. Disposition

**Technical result: PASS WITH MATERIAL LIMITATIONS; test defect identified.**  
**Test readiness: FAIL pending correction.**  
**Exact-head CI: NOT CONFIRMED.**  
**Operational adoption: PARTIAL / NOT VERIFIED.**  
**Owner acceptance: PENDING.**  
**Closure: NOT YET OWNER-CLOSED.**

This A4 record does not authorize merge, deployment, publication, signing, automatic dependency changes, exception approval, or A5.