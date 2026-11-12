# EKHC OS — A2 Monitoring Operational-Readiness Read-Only Reconciliation

**Status:** VERIFIED-CLOSED WITH BLOCKERS RECORDED  
**Date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A2 branch:** `a2/monitoring-operational-readiness-reconciliation`  
**A2 source head:** `677a97b18782f5eee2be1b87890fcd11aae0ac83`  
**A1 assessment branch:** `a1/monitoring-operational-readiness-assessment`  
**A1 assessment commit:** `677a97b18782f5eee2be1b87890fcd11aae0ac83`  
**Monitoring code baseline:** `b4ed07262b1366e49f566cfadc9af3f892abfa14`  
**Accepted A4 branch head:** `9d77f91dbdbca0b220b5e0d0d735caa525a0c9ec`  
**Accepted A4 record blob:** `dc2f37885472775b86496708d19d31a8ba9d124f`  
**Main observed:** `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`

## 1. Purpose and governance

This A2 activity is a read-only reconciliation of the approved A1 assessment against the current monitoring implementation, tests, workflow, exception register, governance policy, and Owner-accepted A4 evidence.

The Owner approved the A1 assessment and its two technical decisions on 2026-11-12:
1. OSV retry policy: at most three total attempts, bounded exponential backoff, retry only transient transport failures and HTTP 429/5xx; do not retry malformed/incomplete/oversized responses, other 4xx, or local input errors.
2. Reminder catch-up: on the next successful run, surface the nearest missed configured threshold with an overdue indicator. Repeated signals may occur; no persistent delivery state or exactly-once claim is introduced.

This record closes only the bounded A2 reconciliation activity. It does not certify operational readiness, implement the approved design, or authorize A3.

## 2. Reconciliation method and integrity

Read-only GitHub source/evidence inspection was performed. No tests were re-run, no external OSV requests were made, and no source/workflow/configuration/register changes were made.

### Branch and commit comparisons

- A1 branch versus code base: **1 commit ahead, 0 behind**; exactly one added file, the A1 assessment document. No code or workflow files changed.
- A4 branch compared with its accepted closure commit: **identical**, 0 ahead / 0 behind / 0 changed files.
- Main remained at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823` during this reconciliation.
- The A2 branch was created from the approved A1 assessment commit; this A2 record is the only intended A2-branch addition.

### Existing exact-head CI evidence rechecked

- Quality run #147, ID `43122480532`, completed SUCCESS on exact code SHA `b4ed07262b1366e49f566cfadc9af3f892abfa14`: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43122480532
- Monitoring run #32, ID `43122480518`, completed SUCCESS on the same exact code SHA; the single monitor job completed SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43122480518
- The historical monitor result queried 32 locked PyPI packages and returned zero OSV advisories. The exception register was empty, so this run did not demonstrate a real exception reminder/expiry.
- These are historical A3-head results, not CI evidence for the A2 documentation commit or a future A3 implementation.

## 3. Current implementation reconciliation

### OR-01 — Positive advisory simulation

**Status: PARTIAL.**

The current test suite mocks an OSV response containing a synthetic advisory and verifies that `query_osv` extracts its identifier and package. It does not exercise the full `main()` report-generation path, the GitHub step summary output, safe rendering of all advisory fields in the report, or the final process exit status for a finding.

**A2 conclusion:** add an end-to-end mocked test around the command/report path in A3. Keep the advisory synthetic; no live vulnerability or public disclosure is required.

### OR-02 — Bounded OSV retry

**Status: MISSING.**

The current `query_osv` performs one `urlopen` call with a 20-second timeout. No retry/backoff exists. Oversized responses (2 MiB bound), malformed/non-object payloads, incomplete batch lengths, malformed package results, and malformed advisory entries are rejected. The monitor catches transport/time-out/value/JSON errors in `main()`, emits an INCOMPLETE summary, and returns exit code 2.

**A2-approved design contract:**
- Maximum three total attempts (one initial attempt plus at most two retries).
- Retry transient transport failures and HTTP 429/5xx only.
- Do not retry malformed JSON/schema, incomplete batch, oversized response, local file/input errors, or other 4xx.
- Preserve the 20-second per-attempt timeout and 2 MiB response cap.
- Use bounded exponential backoff; exact delay constants and total wall-clock bound must be made explicit in A3 implementation/tests.
- Exhaustion must emit INCOMPLETE and return non-zero; never convert failure into a clean zero-findings result.

### OR-03 — Missed-run reminder semantics

**Status: PARTIAL.**

The current monitor reports reminders only when `days_left` is exactly one of 30, 14, 7, 3, or 1, or is 0. A missed threshold is not surfaced on a later run. An approved exception past expiry (`days_left < 0`) is reported as EXPIRED on every successful run. The monitor does not mutate exception status.

**A2-approved design contract:**
- For a non-expired approved exception, if one or more reminder thresholds have passed since the last possible run, surface the nearest missed threshold on the next successful run and label it overdue.
- Interpret nearest as the smallest configured threshold strictly greater than current positive `days_left`; report how many days past that threshold the run is.
- At `days_left == 0`, retain the expiry-day signal.
- At `days_left < 0`, continue to surface EXPIRED on every successful run.
- With no persistent delivery state, duplicate/repeated overdue signals are expected and must be documented. Do not claim exactly-once delivery or human acknowledgement.
- Only APPROVED records are eligible. No status, approval, expiry, renewal, revocation, or register mutation is permitted.

### OR-04 — Operator runbook and escalation

**Status: MISSING / OPERATIONAL INPUTS UNRESOLVED.**

The workflow supports manual `workflow_dispatch`; the monitor emits a GitHub Actions job summary/stdout and uses exit codes 0 (no findings/signals), 1 (findings/reminders), and 2 (incomplete/error). The governance policy defines Owner accountability and response SLAs but explicitly does not establish that private vulnerability reporting is enabled or that a human responder is continuously staffed.

No verified out-of-band channel, recipient, acknowledgement path, escalation coverage, responder rota, holiday calendar, or operational record custody was found in the reviewed evidence. Do not infer these from repository permissions or labels.

**A2 conclusion:** A3 may document a truthful manual runbook and Owner escalation boundary without inventing responders or channels. Human coverage and notification delivery remain operational blockers.

### OR-05 — Production activation gate

**Status: PARTIAL / NOT AUTHORIZED.**

The workflow contains a daily `06:15 UTC` schedule, manual dispatch, push triggers for `a3/**`, and pull-request triggers targeting `main`. GitHub scheduled workflows run only from the default branch; because this workflow is not integrated into the default branch, its daily schedule is not active. The workflow grants read-only contents permissions, has a 10-minute job timeout, and does not configure an external notification channel.

A future activation checklist must require separate Owner authorization, default-branch integration approval, verified notification/acknowledgement path where required, actual responder coverage, exception-register custody, alert-handling procedure, and a controlled rehearsal. This A2 activity does not activate or move the workflow.

## 4. Cross-cutting findings and limitations

1. **Exception demonstration:** `docs/security/exception-register.json` has schema version 1 and an empty `exceptions` array. Synthetic test fixtures exist, but there is no real exception entry and none should be invented for testing.
2. **Lock parsing:** the monitor uses a purpose-built regular expression for the repository's pinned `name==version` lock format. It is not a complete pip requirements parser and does not establish support for all pip syntax (includes, continuations, direct references, extras/markers, or alternate requirement forms). Preserve the existing lockfile and dependencies in this increment; define and test the exact accepted lock grammar or use an already-locked parser only after a separate compatibility review.
3. **External dependency:** OSV is an external service. No service availability, SLA, rate-limit, live positive-advisory, or network-path guarantee is established by the mocked tests or the successful zero-finding run.
4. **Human operations:** job success is not human acknowledgement. Job summary/stdout is not guaranteed out-of-band notification. No recipient or response coverage is verified.
5. **Governance:** the vulnerability policy reserves exception approval/risk acceptance to the Owner. This monitoring improvement must not alter that authority or create institutional roles.
6. **Security posture:** preserve least-privilege read-only workflow permissions, checkout with persisted credentials disabled, bounded response size, no secrets, no protected/production data, and no automated dependency or exception mutation.

## 5. A2 disposition

| Work package | A2 status | A3 implementation direction |
|---|---|---|
| OR-01 positive-advisory report simulation | PARTIAL | Implement mocked end-to-end report/exit test |
| OR-02 transient retry/backoff | MISSING | Implement approved max-three-attempt bounded retry |
| OR-03 missed reminder catch-up | PARTIAL | Implement approved nearest-missed-threshold semantics |
| OR-04 operator runbook | MISSING | Document manual run and Owner escalation; no invented channel/person |
| OR-05 activation gate | PARTIAL | Complete documentation only; keep schedule inactive |

**A2 bounded read-only reconciliation: VERIFIED-CLOSED WITH BLOCKERS RECORDED.**

**Operational readiness: NOT VERIFIED.** The unresolved notification, acknowledgement, responder coverage, exception custody, live positive advisory, and rehearsal gaps remain explicit.

## 6. Authorization boundary

- A1 assessment and the two design decisions: OWNER-APPROVED.
- A2 bounded read-only reconciliation: VERIFIED-CLOSED WITH BLOCKERS RECORDED.
- A3 implementation: **NOT AUTHORIZED by this A2 closure**.
- Default-branch integration, merge, deployment, publication, signing, production operation, scheduled monitoring activation, and A5: **NOT AUTHORIZED**.
- A4 automated advisory monitoring verification remains separately Owner-accepted and VERIFIED-CLOSED WITH LIMITATIONS. This A2 record does not reopen, amend, or replace it.

No code, workflow, lockfile, dependency, exception register, application, production data, A4 closure record, or default-branch file was changed by this reconciliation.
