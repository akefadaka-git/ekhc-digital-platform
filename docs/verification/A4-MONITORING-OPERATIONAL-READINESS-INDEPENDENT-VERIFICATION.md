# EKHC OS — A4 Independent Verification Record
## Monitoring Operational-Readiness A3

**Disposition:** PARTIAL — INDEPENDENT REVIEW FINDINGS RECORDED  
**Verification date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A4 verification branch:** `a4/monitoring-operational-readiness-verification`  
**Verified A3 branch:** `a3/monitoring-operational-readiness`  
**Exact A3 branch head under review:** `a8042051824ddb50592492ee75d5aad24d1bb03a`  
**A2 governing record:** `15c971ce703d51adf1db83a340c5dc3c2a987058`  
**Main observed unchanged:** `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`  
**Previously accepted A4 baseline observed unchanged:** `9d77f91dbdbca0b220b5e0d0d735caa525a0c9ec`

## 1. Scope, independence, and governance

This A4 review independently inspected the final A3 branch tree, implementation source, tests, workflow definitions, operational runbook, production activation gate, exception register, A3 implementation report, and exact-head GitHub Actions metadata/logs.

The review branch was created from the exact A3 head above. No A3 source, workflow, lockfile, dependency, exception-register, or operational document was changed during this verification. This A4 record does not modify or reopen the earlier Owner-accepted A4 baseline for the original advisory-monitoring workstream.

No merge, default-branch integration, deployment, publication, signing, production operation, schedule activation, dependency update, exception mutation, secret addition, or A5 action was performed. The schedule remains inactive while the workflow is off the default branch.

## 2. Exact-head automated evidence — PASS

Both GitHub Actions runs were confirmed to reference the exact A3 head `a8042051824ddb50592492ee75d5aad24d1bb03a` and completed successfully:

| Workflow | Run | Exact-head result | Evidence |
|---|---:|---|---|
| A3 quality checks | #179; ID `43130314519` | SUCCESS | https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43130314519 |
| Read-only security monitor | #64; ID `43130314540` | SUCCESS | https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43130314540 |

Quality job steps verified successful:
- Required-file gate
- Approved Python setup and pinned dependency installation
- Django system check
- Django test suite — 72 tests
- Ruff lint
- Ruff format check
- pip-audit

Security-monitor job steps verified successful:
- Python setup
- Read-only monitor execution
- 32 locked PyPI packages queried
- 0 OSV advisories returned
- 0 approved exception reminders/expiries (the committed register is empty)

These results establish that the configured checks passed on the exact A3 head. They do not establish a live positive advisory, a real exception reminder, OSV availability/SLA, absence of vulnerabilities, human acknowledgement, or out-of-band notification delivery.

## 3. Independent technical review

| Area | A4 result | Review notes |
|---|---|---|
| Retry classification | PASS WITH FINDING | HTTP 429/5xx and recognized transient transport errors are retried; non-retryable HTTP, permanent URL/TLS errors and malformed response paths are not retried. Three total attempts and 1s/2s backoff are present. |
| Response bounds/schema | PASS | Response is read with a 2 MiB + 1 byte sentinel; oversized, malformed, non-object and incomplete batch responses fail closed. |
| Reminder semantics | PASS | Only APPROVED records produce signals. Exact thresholds, missed-threshold catch-up, expiry day and expired state are represented. Repeated overdue/expired signals are possible; no delivery state or exactly-once claim is made. |
| Read-only boundary | PASS | Workflow/job permissions are contents: read; checkout credentials persistence is disabled; no dependency/exception mutation or external notification integration is present. |
| Lock parser | PASS WITH LIMITATION | Strict repository-specific pinned name==version grammar with optional SHA-256 hash options; intentionally not a full pip requirements parser. |
| Positive advisory simulation | PASS | Mocked `main()` path verifies synthetic finding output, Markdown escaping and finding exit status. |
| Failure-path coverage | PARTIAL | Tests cover non-retryable HTTP, malformed response, transient transport exhaustion and retryable HTTP recovery. No direct test asserts HTTP 429/5xx exhaustion behavior through all three attempts or `main()` INCOMPLETE exit status. |
| Operator runbook | PASS WITH LIMITATIONS | Correctly states manual execution, exit meanings, Owner escalation boundary, and absence of guaranteed delivery or responder coverage. |
| Production activation gate | PASS | Explicitly keeps default-branch integration, schedule activation, production operation and A5 separately gated. |

## 4. A4 findings requiring correction or explicit disposition

### A4-F01 — Configured timeout budget is not a hard wall-clock deadline
**Severity:** HIGH  
**Status:** UNRESOLVED / A3 CORRECTION REQUIRED

The implementation defines `OSV_MAX_WALL_CLOCK_SECONDS = 63`, but this value is not enforced by a monotonic deadline. `urlopen(..., timeout=20)` configures socket-operation timeout behavior; it does not by itself guarantee that the complete request and response-read sequence finishes within 20 seconds of wall-clock time if data continues arriving. Therefore three attempts plus two sleeps do not prove a hard 63-second total wall-clock ceiling.

A3's documented 63-second figure must not be represented as a guaranteed maximum elapsed runtime. Correct the implementation to enforce a genuine total deadline across connection and response reading, or explicitly revise the approved requirement/record to a bounded per-operation timeout plus bounded retry sleeps and accurately describe the remaining slow-stream limitation. Do not claim a hard wall-clock cap without enforceable evidence.

### A4-F02 — Literal escape sequences in security implementation documentation
**Severity:** MEDIUM  
**Status:** UNRESOLVED / DOCUMENTATION CORRECTION REQUIRED

`docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md` contains literal backslash-n text (`\\n\\n`) between the retry-budget paragraph and the read-only controls list. This renders as visible escape characters rather than paragraph separation. Correct the document formatting in a separately authorized A3 correction.

### A4-F03 — A3 implementation report contains stale/mismatched evidence metadata
**Severity:** HIGH  
**Status:** UNRESOLVED / EVIDENCE RECORD CORRECTION REQUIRED

The A3 report currently states:
- tested source head `f91cbca5c20cd21b7a55551cad23f5495d903e9c`, while the verified branch head and both successful exact-head workflow runs are `a8042051824ddb50592492ee75d5aad24d1bb03a`;
- quality run #178 and monitor run #63, while verified runs are #179 and #64;
- run IDs in the report's link destinations do not match the run IDs named in the same report.

Correct the A3 report to identify the final verified head and the actual run numbers, IDs and matching URLs. Preserve the historical code-head SHA only if it is separately labelled as an earlier implementation commit, not as the final exact-head verification SHA.

### A4-F04 — Missing direct regression assertions for two failure outcomes
**Severity:** MEDIUM  
**Status:** PARTIAL

Add focused tests for:
1. retryable HTTP 429/5xx exhaustion after exactly three total attempts, including the expected two backoff sleeps and propagated INCOMPLETE outcome;
2. `main()` returning exit status 2 and rendering an INCOMPLETE summary for an OSV transport/API failure.

Current tests exercise retryable HTTP recovery and transient transport exhaustion, but do not directly assert these two end-to-end outcomes.

## 5. Operational limitations preserved

The following remain explicit and are not treated as A4 defects that can be closed by code-only evidence:

- External notification channel and recipient identities: UNRESOLVED.
- Human acknowledgement and escalation coverage: NOT VERIFIED.
- Responder, backup and holiday coverage: NOT VERIFIED.
- Restricted exception-record custody and access controls: NOT VERIFIED.
- Controlled human-response rehearsal: NOT RUN.
- Committed exception register: empty; no real exception was added or tested.
- Live positive OSV advisory: NOT OBSERVED; only synthetic mocked positive coverage exists.
- OSV service availability, SLA, rate-limit guarantees and network path: NOT ESTABLISHED.
- Scheduled workflow: INACTIVE off default branch.
- Successful GitHub workflow: not evidence of human acknowledgement or guaranteed out-of-band delivery.

No recipients, roles, communication channels, responder identities, or operational commitments have been invented.

## 6. Integrity checks and boundaries

- A3 branch head reviewed: `a8042051824ddb50592492ee75d5aad24d1bb03a`.
- A3 versus A2 reconciliation: 31 commits ahead, 0 behind; seven changed paths in the A3 branch comparison.
- `main` remained `adfa62eccda93c8b261e5abd3cbdb22cf28c8823` at verification.
- Previously accepted A4 baseline remained `9d77f91dbdbca0b220b5e0d0d735caa525a0c9ec`.
- No source or workflow modifications were made during A4 review.
- This record is created on a separate A4 verification branch rooted at the exact A3 head.

## 7. A4 disposition and required next step

**A4 technical verification:** PARTIAL — FINDINGS RECORDED.  
**Exact-head CI evidence:** PASS.  
**Implementation review:** PARTIAL pending A4-F01 and A4-F04 disposition/correction.  
**A3 evidence report integrity:** PARTIAL pending A4-F03 correction.  
**Documentation integrity:** PARTIAL pending A4-F02 correction.  
**Operational readiness:** NOT VERIFIED.  
**Production readiness:** NOT READY.  
**A4 closure:** NOT APPROVED / NOT CLOSED.  
**A5, merge, deployment, default-branch integration and schedule activation:** NOT AUTHORIZED.

Immediate next step: address A4-F01 through A4-F04 in a separately authorized A3 corrective change, obtain fresh exact-head quality and monitoring evidence, then repeat A4 verification. Preserve all operational limitations above; do not activate the schedule or merge.
