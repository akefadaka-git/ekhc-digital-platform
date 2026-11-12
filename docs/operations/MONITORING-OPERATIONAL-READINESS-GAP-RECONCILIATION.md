# EKHC OS — Monitoring Operational-Readiness Gap Reconciliation

**Date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Reconciliation branch:** `ops/monitoring-operational-readiness-gap-reconciliation`  
**Starting A4 closure commit:** `42db0eb6c3eb778af8acd9f9fe5d71ef3307cadc`  
**A4 technical baseline:** `0a845253fda11614828b71eb78446e062e394c1f`  
**Scope:** documentation-only operational-readiness reconciliation; no production activation

## 1. Disposition

**RESULT: PARTIAL — DOCUMENTATION CONSISTENCY CORRECTED; OPERATIONAL INPUTS AND CONTROL EVIDENCE REMAIN UNRESOLVED.**

A4 technical verification remains VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS. This reconciliation does not reopen A4 and does not authorize implementation of external notification, responder assignment, default-branch integration, scheduled activation, production operation, or A5.

A stale timeout description was found in the operator runbook. It described the nominal 63-second calculation as an upper bound excluding local processing and runner overhead, while the corrected security-monitor design explicitly states that urllib's socket-inactivity timeout does not impose a hard wall-clock deadline when a response continuously streams data. The operator runbook has been corrected to state the same limitation.

## 2. Reconciled evidence and gaps

| ID | Control area | Repository evidence | Reconciliation result |
|---|---|---|---|
| ORG-01 | OSV request deadline | `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md` describes a 20-second socket-inactivity timeout, at most three attempts, 1s/2s backoff, and no hard total wall-clock deadline. The prior operator runbook's 63-second upper-bound wording was inconsistent. | **CORRECTED IN THIS BRANCH** — operator runbook now accurately says streaming reads can exceed 20 seconds and total elapsed time can exceed 63 seconds. No hard wall-clock guarantee is claimed. |
| ORG-02 | Notification channel and recipients | Operator runbook and activation gate state that GitHub job summary/stdout are the only verified output; no external destination or recipients are established. | **UNRESOLVED** — requires Owner-selected channel and actual authorized recipient identities; none inferred. |
| ORG-03 | Human acknowledgement and escalation | No acknowledgement SLA, primary/backup responders, escalation route, or holiday coverage is established in the reviewed documents. | **NOT VERIFIED** — requires explicit Owner-approved assignments and evidence of availability/acceptance. |
| ORG-04 | Restricted exception-record custody | Public register is intentionally limited to non-sensitive metadata; full exception records are expected to remain in a restricted location, but no concrete custodian, access list, or tested custody control is evidenced in the reviewed repository material. | **NOT VERIFIED** — requires an identified restricted repository/system, authorized custodians, access review, and handling procedure. |
| ORG-05 | Controlled operational rehearsal | Activation gate requires synthetic positive-advisory, retry-exhaustion, overdue-reminder, and INCOMPLETE rehearsal, including receipt and understanding by authorized responders. No such human-response rehearsal evidence is present. | **NOT RUN** — cannot be completed until ORG-02 through ORG-04 are established. |
| ORG-06 | Exception register positive-path operations | `docs/security/exception-register.json` is schema version 1 with an empty `exceptions` array. | **PASS FOR EMPTY BASELINE; POSITIVE OPERATION NOT DEMONSTRATED** — no real exception is to be created for testing. Synthetic fixtures remain isolated to tests/rehearsal and must not be committed to the public register. |
| ORG-07 | Live OSV positive advisory | Exact-head Security Monitor workflow completed successfully and reported zero OSV advisories. Synthetic positive-advisory behavior is covered by mocked tests. | **NOT OBSERVED LIVE** — no live positive advisory is claimed or fabricated. |
| ORG-08 | OSV availability and service guarantees | Repository code calls the public OSV API; no SLA, rate-limit commitment, or guaranteed network path is evidenced. | **UNRESOLVED EXTERNAL DEPENDENCY** — retain fail-closed INCOMPLETE semantics and do not infer a service guarantee. |
| ORG-09 | Scheduled execution | Workflow is configured for 06:15 UTC daily but scheduled workflows run only from the default branch. Corrective branch is not the default branch. | **INACTIVE OFF DEFAULT BRANCH** — activation remains separately unauthorized. |
| ORG-10 | GitHub run visibility | Quality and Security Monitor checks passed on exact validation head `0a845253fda11614828b71eb78446e062e394c1f`. | **TECHNICAL CI PASS; HUMAN DELIVERY NOT PROVEN** — a green run is not an acknowledgement or notification guarantee. |

## 3. Corrective documentation change

Updated:

- `docs/operations/SECURITY-MONITORING-OPERATOR-RUNBOOK.md`

The timeout paragraph now accurately distinguishes:
- 20-second urllib socket-inactivity timeout per attempt;
- maximum three total attempts;
- bounded 1-second and 2-second backoff;
- absence of a hard per-attempt or total wall-clock deadline;
- possible elapsed time beyond the nominal 63-second calculation when a response continues streaming.

This is a documentation correction only. No Python source, tests, workflow, permissions, secrets, dependency manifest, lockfile, exception register, or application code was changed.

## 4. Owner decisions and external evidence required

The following are prerequisites for any claim of operational readiness. They must be supplied or approved through an explicit Owner-governed process:

1. **Notification destination:** select an approved delivery channel and establish its account/tenant ownership, credential custody, privacy constraints, delivery failure behavior, and recipient list. This reconciliation does not connect or configure a channel.
2. **Named responders:** identify primary and backup responders, their authority boundaries, availability windows, holiday coverage, and acknowledgement expectations. No role or person is inferred from repository labels.
3. **Escalation route:** define how an unacknowledged alert is escalated to the Owner, including a measurable response interval and evidence of delivery/acknowledgement.
4. **Exception-record custody:** identify the restricted system of record, authorized custodians, access-control evidence, retention policy, and non-sensitive reference convention. Do not move confidential exception rationales or evidence into this public repository.
5. **Rehearsal authorization:** separately authorize a controlled rehearsal using synthetic, non-sensitive fixtures after the people and delivery path are established. The rehearsal must test positive finding, retry exhaustion, overdue reminder, and INCOMPLETE handling, and record actual receipt, acknowledgement, and response.
6. **External service assumptions:** keep OSV availability and rate limits as external dependencies unless independently supported service terms or monitoring evidence are obtained.

No actual notification recipient, responder, custodian, service SLA, or response commitment is recorded in this document.

## 5. Remaining implementation and governance boundaries

- No hard total wall-clock deadline has been implemented. If a strict deadline is later required, it needs a separately scoped technical design and tests; this documentation correction does not implement one.
- No external notification integration has been implemented.
- No secrets, credentials, expanded GitHub permissions, dependencies, or third-party services were added.
- No real exception was added or modified.
- No production or protected data was accessed.
- The daily schedule remains inactive off the default branch.
- The A4 closure branch and record are preserved and unchanged by this branch.
- No merge, deployment, publication, signing, default-branch integration, schedule activation, production operation, or A5 action was performed or authorized.

## 6. Status

- A4 technical verification: **VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS** (preserved).
- Operator runbook timeout wording: **CORRECTED IN THIS BRANCH; A4 baseline not rewritten**.
- Documentation-only operational gap reconciliation: **PARTIAL**.
- Notification and recipient identity: **UNRESOLVED**.
- Human acknowledgement and responder coverage: **NOT VERIFIED**.
- Restricted exception-record custody: **NOT VERIFIED**.
- Controlled human-response rehearsal: **NOT RUN**.
- Live positive OSV advisory: **NOT OBSERVED**.
- OSV SLA/rate-limit guarantee: **NOT ESTABLISHED**.
- Production readiness: **NOT READY**.
- Merge/default-branch integration/schedule activation/deployment/A5: **NOT AUTHORIZED**.

## 7. Immediate next action

Obtain Owner-approved operational inputs for ORG-02 through ORG-04 (notification destination and recipients, responder/backup/holiday coverage and acknowledgement/escalation rules, and restricted exception-record custody). Only after those inputs are evidenced should a controlled synthetic rehearsal be proposed for separate authorization.
