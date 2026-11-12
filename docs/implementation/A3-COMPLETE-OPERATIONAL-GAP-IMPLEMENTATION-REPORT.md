# A3 Technical Gap Implementation — Hard Deadline and Durable Mock Ledger

**Status:** IMPLEMENTED — EXACT-HEAD CI PASS  
**Date:** 2026-11-12  
**Branch:** `a3/complete-operational-gap-implementation`  
**Base:** Monitoring A3 corrective source `1a3946284c819b7004d4a652a4bbcb02396f3389`

## 1. Scope

This increment addresses software-side limitations that can be implemented without institutional service provisioning:

1. Enforce a hard end-to-end OSV request deadline.
2. Persist mock notification receipts and redacted audit events in SQLite.
3. Preserve destination-bound idempotency across process restarts and serialize concurrent writers.
4. Preserve atomic multi-channel behavior for persisted mock requests.
5. Keep mock acknowledgement events explicitly synthetic.
6. Include the new notification tests in the required CI file gate.

This increment does not create live email/SMS providers, send real messages, assign responders, establish institutional custody, or authorize a rehearsal or production operation.

## 2. Hard OSV wall-clock deadline

The existing 20-second urllib timeout remains a per-socket inactivity timeout and is not treated as a total request deadline.

The main monitor now delegates the complete OSV operation to a child process. The parent supervises that process with a 63-second timeout. The bound includes:
- process startup;
- request connection and response handling;
- response streaming and size validation;
- all retry attempts;
- 1-second and 2-second retry backoff;
- result serialization.

If the worker exceeds the deadline, the parent terminates it and raises a timeout error. The monitor reports INCOMPLETE and exits non-zero. The worker emits structured JSON only on stdout; errors are returned as a non-sensitive error class on stderr.

The existing maximum of three attempts and retry eligibility rules are unchanged. A hard deadline does not convert a timeout into a clean result.

## 3. Durable mock notification ledger

The optional `SQLiteNotificationLedger` stores only:
- synthetic event IDs;
- channel names;
- synthetic destination references;
- simulated outcome and attempt count;
- fixed simulated/not-delivered flags;
- redacted audit metadata.

It does not store message bodies, real addresses, phone numbers, credentials, provider responses, or restricted exception content.

Configuration:
- `EKHC_NOTIFICATION_MODE=mock`
- `EKHC_EMAIL_MODE=mock`
- `EKHC_SMS_MODE=mock`
- Optional `EKHC_NOTIFICATION_LEDGER_PATH` set to a local filesystem path.

If no ledger path is configured, the adapter retains its in-memory behavior. When configured, the SQLite database is created locally, the database file is restricted to owner read/write permissions where supported, WAL and FULL synchronous durability are enabled, and SQLite writer transactions serialize processes.

### Idempotency and transaction behavior

- The ledger uses `(event_id, channel)` as its unique key.
- The stored destination is bound to that key; a different destination is rejected.
- The orchestrator obtains a SQLite `BEGIN IMMEDIATE` transaction and refreshes persisted receipts after acquiring the writer lock.
- Same-destination replays return the original simulated receipt without a second mock attempt.
- A conflicting destination is rejected before any request audit or attempt.
- All channels in a request are processed within one database transaction; an unexpected processing failure rolls back all receipts and audit events from that request.
- Simulated acknowledgement events are durably recorded with `simulated=true` and `SIMULATED — NOT DELIVERED`.

This is durable mock evidence, not a real notification delivery ledger. It provides no provider delivery, human acknowledgement, exactly-once external delivery, or live-service guarantee. The ledger must not be connected to a live provider.

## 4. Tests added

- Hard OSV worker deadline is passed to the process supervisor.
- Deadline expiration becomes a fail-closed timeout.
- Worker JSON output is validated; malformed/non-zero worker results fail closed.
- SQLite receipt persistence survives orchestrator recreation.
- Duplicate suppression survives process restart.
- Changed-destination replay remains rejected after restart.
- Multi-channel failures roll back persisted receipts and audit entries atomically.
- Simulated acknowledgement persists with an explicit simulated label.
- Non-simulated receipts are rejected by the ledger.
- SQLite file permissions are checked on the CI filesystem.
- The CI required-file gate includes the notification module and test suite.

## 5. Remaining institutional / operational gates

These cannot be truthfully completed by repository code in the absence of institutional inputs:

| Gate | Required external evidence | Status |
|---|---|---|
| ORG-02 email | Provisioned institutional tenant/mailbox, sender control, authorized recipients, delivery test | NOT AVAILABLE / NOT VERIFIED |
| ORG-02 SMS | Provisioned SMS provider/account/sender, authorized recipients, delivery test | NOT AVAILABLE / NOT VERIFIED |
| ORG-03 responders | Accepted primary/backup roster, coverage and authority, acknowledgement/escalation evidence | NOT ESTABLISHED |
| ORG-04 custody | Selected restricted records system, custodians, access/MFA/encryption/audit/retention/recovery evidence | NOT IDENTIFIED |
| ORG-05 rehearsal | Separate Owner authorization after ORG-02–04 evidence is accepted | NOT AUTHORIZED / NOT RUN |
| A5 | Separate Owner authorization after operational and technical gates | NOT AUTHORIZED |

No provider, person, contact route, system, custodian, or service guarantee is inferred.

## 6. Security and governance boundaries

- No third-party dependency added.
- No provider SDK, SMTP client, HTTP delivery client, or external notification route added to the mock module.
- No secret, repository variable, credential, or permission change.
- No real contact or production data used.
- SQLite state is local and synthetic-only; database files are gitignored.
- No exception register mutation.
- No schedule activation, merge, default-branch integration, deployment, publication, signing, rehearsal, or A5.

## 7. Exact-head CI evidence

**Validated branch head:** `37b907a7caaa2e4bfcbaaa53c6152e9d25507037`

Both workflows completed successfully on this exact commit:

- **A3 quality run #263**, run ID `43215780859`: SUCCESS.
  - Required-file gate: PASS.
  - Django system check: PASS.
  - Django test suite: **100 tests PASS**.
  - Ruff lint: PASS.
  - Ruff format: PASS.
  - pip-audit: PASS.
  - [Workflow run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43215780859)
- **Security Monitor run #148**, run ID `43215780854`: SUCCESS.
  - OSV query and exception-register monitoring workflow: PASS.
  - [Workflow run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43215780854)

The final branch read-back and comparison must still be recorded after this report commit; the implementation source/test head above is the CI-validated code head. The report-only commit does not change implementation or test files.

## 8. Acceptance and status

- Hard OSV wall-clock deadline: IMPLEMENTED; exact-head tests and CI PASS.
- Durable SQLite mock ledger: IMPLEMENTED; persistence, restart replay, destination conflict, transaction rollback, and concurrent orchestrator tests PASS.
- CI quality and dependency audit: PASS.
- Security monitor workflow: PASS.
- External email/SMS services, recipients, responders, restricted-record custody: NOT AVAILABLE / NOT VERIFIED.
- Controlled rehearsal: NOT AUTHORIZED / NOT RUN.
- Operational readiness: NOT VERIFIED.
- Production readiness: NOT READY.
- Merge, deployment, schedule activation, publication, signing, and A5: NOT AUTHORIZED.
