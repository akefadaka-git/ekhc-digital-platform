# EKHC OS — Automated Advisory Monitoring and Exception-Expiry Signals

**Status:** A3 implementation baseline; operational notification delivery not yet verified  
**Date:** 2026-11-11  
**Scope:** read-only daily monitoring of locked PyPI package versions and non-sensitive exception expiry metadata

## 1. Controls and boundaries

The scheduled workflow queries the public OSV batch API for each exact PyPI name/version in `requirements-lock.txt`. It validates and reads the exception metadata register, then reports approved exceptions at the 30-, 14-, 7-, 3-, and 1-day thresholds, on the expiry date, and after expiry. If a run misses a threshold, the next successful run reports the nearest passed threshold as EXPIRY_REMINDER_OVERDUE, including the threshold and days overdue. Only APPROVED records are eligible. No delivery state is stored, so overdue/expired signals can repeat on later runs; no exactly-once delivery or human acknowledgement is claimed.

The OSV client makes at most three total attempts. It retries transient transport failures and HTTP 429/5xx only, with a 20-second per-attempt timeout and bounded 1-second then 2-second backoff. It does not retry other 4xx responses, malformed JSON/schema, incomplete batches, oversized responses, or local input errors. The configured request/backoff budget is 63 seconds (three 20-second attempts plus three seconds of backoff), excluding runner and local-processing overhead. Exhaustion is reported as INCOMPLETE with a non-zero exit status.\n\nThe workflow is deliberately read-only:
- workflow and job permissions are `contents: read` only;
- no issue, pull request, repository, package, deployment, or OIDC write permissions;
- no dependency installation or update;
- no application runtime changes or new third-party dependencies;
- no automatic severity assignment, risk acceptance, approval, revocation, expiry-status mutation, merge, or deployment;
- no artifact upload or publication.

A due reminder, overdue reminder, expiry signal, or advisory finding produces a non-zero workflow result and a job summary. Exit status 0 means no findings/signals, 1 means findings/reminders, and 2 means INCOMPLETE/error. A query, parsing, or API failure is reported as INCOMPLETE and fails closed. The workflow does not guarantee email, mobile push, or out-of-band delivery; GitHub notification settings and recipient subscription must be verified separately.

## 2. Exception metadata and confidentiality

The committed `exception-register.json` is intentionally empty and is limited to non-sensitive metadata. Full exception records, risk rationales, exploit evidence, compensating-control details, and approval evidence must remain in an access-restricted location under the governance policy. Do not place confidential exception records or secrets in this public repository.

When a real exception is separately approved, a maintainer may add only its non-sensitive identifier, severity, status, UTC expiry, and a non-sensitive record reference to the register. The monitor treats only `APPROVED` entries as active. Proposed, rejected, revoked, and expired entries are not treated as active approvals. The monitor never changes the status; an overdue entry remains visible as overdue until a human updates the record and metadata.

Expiry reminders are signals to obtain Owner review before the deadline. They do not extend, renew, revoke, or accept risk. The Owner's explicit approval remains mandatory for any exception or renewal.

## 3. Cadence and execution

- Scheduled cadence: daily at 06:15 UTC.
- Manual execution: `workflow_dispatch`.
- Push validation: A3 branches.
- Pull-request validation: pull requests targeting `main`.
- GitHub scheduled workflows run only from the repository's default branch. Until this branch is separately reviewed and merged, the schedule is not active; manual dispatch on this branch can validate it.

The OSV API is an external dependency. Results depend on OSV coverage, package identity normalization, network availability, and advisory freshness. No result is not proof that a package is safe. The current parser intentionally supports the repository's pinned PyPI lock format; it rejects unsupported entries rather than silently skipping them.

## 4. Acceptance and remaining operational work

Acceptance requires:
1. exact-head workflow validation with a successful OSV response;
2. unit tests for lock parsing, malformed input, UTC validation, reminder thresholds, and non-approved statuses;
3. independent review of workflow permissions, API handling, and failure behavior;
4. confirmation that the Owner's GitHub notification preferences surface failed scheduled runs;
5. a controlled test with a synthetic, non-sensitive exception entry, followed by removal of that test entry;
6. explicit review/approval before any merge to the default branch.

No real exception currently exists in the committed register. No real advisory intake, exception approval, or notification delivery is claimed. The manual operator procedure is documented in docs/operations/SECURITY-MONITORING-OPERATOR-RUNBOOK.md; production activation prerequisites and the separate Owner gate are documented in docs/operations/SECURITY-MONITORING-PRODUCTION-ACTIVATION-GATE.md. The daily schedule remains inactive while this workflow is not on the default branch.
