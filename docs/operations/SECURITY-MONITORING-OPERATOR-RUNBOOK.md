# EKHC OS — Security Monitoring Operator Runbook

**Status:** A3 operational procedure; human notification and responder coverage remain unverified  
**Scope:** read-only OSV dependency advisory checks and approved exception-expiry signals

## 1. Purpose and limits

This procedure describes how an authorized repository operator can run and inspect the security monitor. The monitor reads the pinned PyPI lockfile and non-sensitive exception metadata, queries OSV, and writes a GitHub Actions job summary and log output.

It does not provide guaranteed email, mobile, webhook, ticket, or other out-of-band delivery. A successful workflow run is not human acknowledgement. No responder rota, alternate contact, recipient list, acknowledgement SLA, holiday coverage, or restricted-record custodian is established by this runbook. Do not infer or invent any of those operational inputs.

## 2. Manual execution

1. Open the repository's Actions tab.
2. Select Read-only security advisory and exception monitor.
3. Use Run workflow on the reviewed A3 branch.
4. Wait for the monitor job to complete; inspect the job summary and logs.
5. Record the run URL and exact commit SHA in the applicable internal operational record. Do not copy confidential exception rationales, exploit evidence, credentials, or restricted records into this public repository.

The workflow is also configured with a daily 06:15 UTC schedule, but GitHub scheduled workflows run only from the default branch. This A3 branch is not the default branch; the schedule remains inactive unless separately approved and integrated.

## 3. Exit status and response

| Exit status | Meaning | Operator action |
|---|---|---|
| 0 | Query completed; no advisory findings or reminder signals | Record the run URL/SHA if operational recordkeeping is required. This is not proof that dependencies are vulnerability-free. |
| 1 | Query completed and at least one advisory finding or exception reminder/expiry signal was reported | Review the complete job summary and logs. Preserve the signal; refer exception approval, renewal, or risk acceptance to the Owner. Do not change dependencies or exception status as an automated response. |
| 2 | Monitoring is INCOMPLETE or encountered an input/API/transport error | Treat the result as unknown, not clean. Inspect the error class and run logs; correct a confirmed non-sensitive input problem or rerun after a transient external-service failure. Do not suppress the failure or record it as zero findings. |

OSV retries only transient transport failures and HTTP 429/5xx, with at most three total attempts and 1-second then 2-second backoff. Other HTTP statuses and malformed, incomplete, or oversized responses are not retried. Each attempt uses a 20-second urllib socket-inactivity timeout. This is not a hard per-attempt wall-clock limit or a hard total request deadline: a response that continuously streams data can keep socket reads active beyond 20 seconds, and total elapsed time can exceed the nominal 63-second timeout/backoff calculation. The implementation makes no hard end-to-end wall-clock guarantee. The three-attempt limit and bounded backoff still apply.

## 4. Exception reminder handling

Only APPROVED register entries are evaluated. A missed threshold is surfaced as EXPIRY_REMINDER_OVERDUE using the nearest higher configured threshold and the number of days overdue. The expiry date retains its expiry-day signal; an expired approved entry remains EXPIRED.

The monitor stores no delivery/acknowledgement state. An overdue or expired signal may therefore repeat on later successful runs. Repetition is intentional and is not an exactly-once delivery claim. The monitor never approves, renews, revokes, expires, or otherwise mutates an exception.

The committed exception register is empty. Do not add a real exception merely to test the monitor. Synthetic records belong only in isolated tests and must not be committed to the register.

## 5. Escalation and unresolved operations

The Owner retains authority for exception approval, renewal, revocation, and risk acceptance. This runbook does not assign authority to an unverified role or name a responder. Where a finding or exception signal requires a decision, preserve the evidence and seek Owner direction through an independently established and authorized communication route.

Before claiming operational readiness, the Owner must separately establish and verify:
- the notification channel and intended recipients;
- acknowledgement expectations and escalation coverage;
- responder availability and backup/holiday coverage;
- custody and access controls for full exception records;
- an evidence-retention location and handling procedure;
- a controlled rehearsal proving that the intended people receive and act on signals.

Until those inputs are verified, the monitor is a repository-visible advisory mechanism only.
