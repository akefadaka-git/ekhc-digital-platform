# EKHC OS — A1 Monitoring Operational-Readiness Assessment

**Status:** DRAFT — Owner review required before A2  
**Date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Assessment branch:** `a1/monitoring-operational-readiness-assessment`  
**Code baseline:** `b4ed07262b1366e49f566cfadc9af3f892abfa14` (`a3/security-monitor-corrections`)  
**A4 acceptance baseline:** `9d77f91dbdbca0b220b5e0d0d735caa525a0c9ec` (`a4/automated-advisory-monitoring-verification`)  
**Main baseline observed:** `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`

## 1. Purpose

Assess a separate, bounded improvement increment for operational readiness of the read-only OSV advisory and exception-expiry monitor. This assessment does not reopen or modify the Owner-accepted A4 technical verification baseline. A4 remains VERIFIED-CLOSED WITH LIMITATIONS.

This is an A1 assessment and proposed specification only. It does not authorize implementation, default-branch integration, scheduled production operation, notification delivery, or A5.

## 2. Existing verified baseline

The Owner-accepted A4 record documents:
- Exact-head quality run #147 and monitor run #32 succeeded on A3 code head `b4ed07262b1366e49f566cfadc9af3f892abfa14`.
- 64 tests, Django system check, Ruff lint, Ruff format, and pip-audit passed on that exact A3 head.
- The monitor queried 32 pinned PyPI packages; OSV returned zero advisories.
- The exception register was empty, so no real exception reminders or expiries were demonstrated.
- The workflow has a 06:15 UTC daily schedule, but schedule execution is inactive while the workflow is not on the default branch.
- The monitor emits GitHub Actions job summary/stdout and exit status; guaranteed out-of-band delivery is not implemented or verified.
- There is no retry/backoff for OSV service errors.
- A positive advisory is covered by a mocked parser test, not by a live positive OSV match.
- Reminder thresholds are exact-day checks; missed threshold-day executions are not replayed later as those particular reminders.
- The lock parser is purpose-built for the repository's pinned requirements format, not a complete pip requirements parser.
- Operational acknowledgement, escalation, responder coverage, and delivery are not verified.

## 3. Proposed objective

Improve deterministic signal correctness, failure handling, missed-run visibility, and operator readiness while retaining a strictly read-only monitor and keeping production activation disabled.

## 4. Proposed bounded work packages

### OR-01 — Deterministic positive-advisory simulation
- Add an end-to-end test of the report-generation path using a synthetic, mocked OSV response.
- Verify package/version/advisory fields are rendered safely and the process returns the expected finding exit status.
- Do not depend on a live vulnerability being present in OSV.
- Do not create a real advisory, issue, or public disclosure.

### OR-02 — Bounded OSV transient-failure handling
- Assess and, if approved, implement bounded retry/backoff for transient transport failures and retryable server responses.
- Keep a strict total time budget and bounded response size.
- Do not retry malformed responses as though they were transient.
- Emit INCOMPLETE and a non-zero exit after retry exhaustion.
- Tests must use mocks; no external service is required for CI.

### OR-03 — Missed-run and reminder-boundary semantics
- Specify catch-up behavior for reminders whose exact threshold date was missed.
- Keep expiry signals visible on every run after expiry.
- Prevent the monitor from mutating exception status or approving, renewing, revoking, or extending an exception.
- Do not introduce persistent delivery state or claim exactly-once notification without an approved state store and delivery contract.
- Use synthetic exception entries only; do not add a real exception to the register.

### OR-04 — Operator runbook and escalation contract
- Document manual dispatch, interpretation of SUCCESS/INCOMPLETE/finding exit states, evidence retention, response steps, and escalation to the Owner.
- State explicitly that GitHub job summaries/stdout are not guaranteed out-of-band notification.
- Do not invent responder identities, contact addresses, rota coverage, or institutional roles.

### OR-05 — Production activation gate (documentation only)
- Record prerequisites for any future schedule activation: separate Owner authorization, default-branch integration approval, verified notification/acknowledgement path if required, responder coverage, exception-register custody, alert handling procedure, and successful controlled rehearsal.
- The current work must not enable or activate scheduled production monitoring.
- Do not merge the workflow to the default branch.

## 5. Explicit exclusions and controls

The following are outside this increment:
- merge, deployment, publication, signing, release, production operation, or A5;
- activation of the existing daily schedule or any other production schedule;
- adding email, mobile, webhook, chat, ticketing, or other out-of-band notification delivery;
- adding secrets, tokens, external credentials, or notification recipients;
- adding/updating dependencies or changing the lockfile;
- creating real exception records or accessing protected/production data;
- changing exception approval or risk-acceptance authority;
- changing application behavior, database schema, migrations, authentication, authorization, or institutional roles;
- weakening CI, lint, audit, or security controls.

Any future notification integration requires a separately approved destination, recipient/owner, credential-handling model, privacy review, delivery/retry semantics, and verification plan. None is assumed here.

## 6. Proposed acceptance criteria

1. Positive advisory behavior is reproducibly tested using synthetic mocked data, including safe rendering and exit status.
2. Transient OSV failures follow a documented, bounded retry policy; malformed/incomplete/oversized responses fail closed.
3. Reminder catch-up semantics are explicit, deterministic, and covered by tests, without mutating exception records or claiming delivery.
4. Operator runbook accurately distinguishes monitor execution status from human acknowledgement and notification delivery.
5. Production activation checklist is explicit and remains NOT AUTHORIZED.
6. All tests and repository quality checks pass on the exact implementation head.
7. No dependency, application, schema, production-data, or default-branch changes occur.
8. A4 record and branch remain unchanged.

## 7. Open decisions requiring Owner direction

- **Reminder catch-up:** proposed behavior is to surface the nearest missed configured threshold on the next successful run, together with an overdue indicator, rather than silently dropping all missed thresholds. This may repeat on later runs unless a separately authorized delivery-state mechanism is introduced. Confirm or revise this behavior before A3.
- **Retry policy:** proposed maximum is three total attempts with bounded exponential backoff for transient network errors and retryable HTTP 5xx/429 responses; no retry for malformed JSON/schema responses, 4xx other than 429, or local input errors. Confirm or revise before A3.
- **Notification channel:** no external channel is proposed for implementation in this increment. GitHub job summary/stdout remains the only output unless a separate channel is explicitly selected and authorized.
- **Operator identity/coverage:** remain Owner-directed and UNRESOLVED until actual named responders and availability are supplied through an authorized process. Do not infer them.

## 8. Stage and governance status

- A1 assessment: DRAFT / OWNER REVIEW REQUIRED.
- A2 read-only reconciliation: NOT STARTED.
- A3 implementation: NOT AUTHORIZED.
- A4 verification: not part of this new increment; prior A4 remains VERIFIED-CLOSED WITH LIMITATIONS.
- A5: NOT AUTHORIZED.

No changes were made to the A3 code, A4 closure record, default branch, application, dependency manifests, lockfile, workflow schedule, exception register, or production systems.
