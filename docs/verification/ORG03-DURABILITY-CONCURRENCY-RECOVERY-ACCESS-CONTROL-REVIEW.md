# EKHC OS — ORG-03 Durability, Concurrency, Recovery and Restricted-Access Review

**Review date:** 2026-11-13  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Reviewed branch:** `a3/org-03-responder-operations`  
**Reviewed source head:** `04e0c1c38e5e2c885e582ab9b15d38f47863595e`  
**Review type:** Repository architecture and source inspection; no live systems or restricted data accessed

## 1. Disposition

**ORG-03 event-transition unit behavior: VERIFIED AT THE REVIEWED SOURCE HEAD.**  
**Durable event persistence: NOT IMPLEMENTED / NOT TESTED.**  
**Concurrent acknowledgement safety: NOT IMPLEMENTED / NOT TESTED.**  
**Restart and crash recovery: NOT IMPLEMENTED / NOT TESTED.**  
**Restricted-record access controls: NOT IMPLEMENTED / NOT TESTED.**  
**Operational readiness: NOT VERIFIED. Production readiness: NOT READY.**

This review does not certify the implementation as operationally safe. It records the precise gap between the existing synthetic state-machine tests and the controls required for an operational service.

## 2. Evidence inspected

The following files were inspected at the reviewed branch head:

- `scripts/org03_events.py`
- `tests/test_org03_events.py`
- `scripts/org03_roster.py`
- `tests/test_org03_roster.py`
- `config/settings.py`
- `tests/test_access_control_boundary.py`
- `config/security.py`
- `config/urls.py`
- `docs/implementation/A3-RESTRICTED-FOUNDATION-SCOPE.md`
- `docs/implementation/A3-TECHNICAL-BASELINE-PROPOSAL.md`
- `docs/assessment/A3-AUTHENTICATION-AUTHORIZATION-SECURITY-FOUNDATION-ASSESSMENT.md`
- `docs/operations/OWNER-OPERATIONAL-READINESS-INPUT-REGISTER.md`

The previously recorded exact-head CI evidence at `04e0c1c38e5e2c885e582ab9b15d38f47863595e` is:
- Quality run `43384771796`: SUCCESS; 94 Django tests, Ruff lint/format and dependency audit passed.
- Security monitor run `43384771790`: SUCCESS.

These runs predate this review document and do not test the four missing capabilities below.

## 3. Technical findings

### 3.1 Event persistence

`scripts/org03_events.py` accepts a Python dictionary, deep-copies it, appends an event to an in-memory list, and returns a new dictionary. No event repository, database connection, durable write, transaction, database constraint, or persistent audit log is configured.

Consequences:
- Process exit loses the event history unless an external caller separately persists it; no such caller or persistence contract is present in the inspected implementation.
- Append-only behavior is a property of the returned Python value, not a tamper-resistant or durable storage guarantee.
- There is no demonstrated event identity, durable idempotency key, or atomic state-and-event commit.

**Result: NOT IMPLEMENTED.** No persistence or durability claim is permitted.

### 3.2 Concurrent acknowledgement handling

The state machine checks a caller-supplied sequence number against `next_sequence`. This protects a single in-memory state transition from a stale sequence only when the caller uses the returned state serially.

There is no shared transactional store, row-level lock, compare-and-swap operation, uniqueness constraint, or multi-process coordination. The test suite does not run competing acknowledgement requests against shared storage.

**Result: NOT IMPLEMENTED / NOT TESTED.** The current code does not establish that only one concurrent primary/backup/Owner acknowledgement wins.

### 3.3 Restart and crash recovery

No durable event replay, checkpoint, transaction recovery, partial-write detection, restart test, or corrupted-log handling exists in the reviewed code.

**Result: NOT IMPLEMENTED / NOT TESTED.** A restart-safe reconstructed alert state cannot be claimed.

### 3.4 Restricted-record access controls

The reviewed roster module explicitly validates a synthetic public template and does not load restricted identity/contact records. Django settings install no product/authentication apps and configure no usable database; the access-boundary regression test explicitly asserts those properties. The approved security assessment also defers authentication and authorization implementation pending authoritative identity, institutional authority, privacy, and client decisions.

No restricted-record store, principal authentication, least-privilege enforcement, MFA integration, custodian access group, object-level authorization, encryption/key management, audit trail, retention, or backup/recovery control is implemented or evidenced.

**Result: NOT IMPLEMENTED / NOT TESTED.** The public synthetic roster validator must not be treated as a restricted-record security boundary.

## 4. Binding architecture constraint — persistence is not currently authorized

The reviewed A3 scope and technical baseline expressly defer:
- database selection and production persistence architecture;
- ORM integration, migrations, schemas, models, and database-backed features;
- authentication and authorization;
- restricted identity or production data;
- general resource APIs.

The approved first-increment baseline intentionally has no database, ORM persistence, migrations, or product apps. The access-control boundary tests enforce that baseline.

Therefore, adding a database, persistence layer, migrations, authentication, authorization, or a restricted-record service now would contradict the recorded Owner-approved technical baseline. This review does **not** silently expand that authorization.

A separate Owner decision is required before implementation can proceed beyond non-persistent synthetic tests. That decision should explicitly define:
1. Whether to reopen the database/persistence deferral for an isolated ORG-03 technical increment.
2. Permitted storage technology and test-only versus production scope.
3. Whether any schema or migration is allowed, and whether it may contain synthetic data only.
4. Whether authentication/access-control implementation is in scope, given the unresolved institutional identity and authority decisions.
5. Whether the work must remain an isolated technical prototype with no production data, credentials, live integrations, or deployment.

## 5. Required acceptance criteria after separate scope approval

### PERSIST-01 — Durable append and atomic commit
- Persist each event and the corresponding aggregate version in one transaction.
- Enforce unique event ID and unique per-alert sequence at the storage layer.
- Reject mutation/deletion of committed history through the application interface.
- Verify committed events remain available after a new process opens the store.
- Verify transaction rollback leaves neither a partial event nor a falsely advanced aggregate version.

### CONC-01 — Concurrent acknowledgement arbitration
- Execute simultaneous primary and backup acknowledgement attempts against the same aggregate version.
- Execute duplicate retries with the same idempotency key.
- Execute stale-version and out-of-order submissions.
- Race an acknowledgement against a deadline/escalation transition.
- Assert exactly one valid state transition is committed; losing requests return a conflict/retry-safe result and cannot overwrite the winner.
- Verify the event log contains no duplicate accepted sequence.

### REC-01 — Crash and replay recovery
- Simulate termination before commit, during commit, and immediately after commit.
- Reopen the store and reconstruct the aggregate from committed events.
- Verify uncommitted work is absent, committed work is present exactly once, and aggregate version matches the log.
- Detect invalid sequence, duplicate ID, invalid transition, and tampered/corrupt record; fail closed rather than silently repair history.
- Verify recovery is repeatable and idempotent.

### ACL-01 — Restricted-record boundary
Only after an approved identity/access-control scope:
- Deny anonymous access by default.
- Enforce server-side least privilege at both record and action level.
- Deny access when authorization evidence is absent, stale, conflicting, or revoked.
- Test direct object reference, cross-record, bulk export, and field-level disclosure attempts.
- Require MFA through the selected approved identity architecture; do not invent institutional roles or entitlements.
- Audit view, create, change, export, and delete attempts using privacy-approved minimal metadata.
- Verify encryption in transit/at rest, key custody/rotation, retention, backup, and recovery through configuration evidence and controlled tests.

## 6. Safe work permitted before the scope decision

Until a separate decision is recorded:
- Preserve the current in-memory transition implementation and its existing tests.
- Add only documentation and synthetic, non-persistent test specifications that do not imply an approved database, schema, identity model, or institutional authority.
- Keep the public roster template empty and synthetic.
- Do not add database dependencies, migrations, models, authentication packages, restricted-record APIs, secrets, live integrations, or real identities.
- Do not run a real responder rehearsal or send notifications.

## 7. Current readiness and governance

| Area | Status |
|---|---|
| Existing synthetic transition behavior | VERIFIED by prior exact-head CI, with stated in-memory limitation |
| Durable event persistence | NOT IMPLEMENTED |
| Concurrent acknowledgement arbitration | NOT IMPLEMENTED |
| Crash/restart recovery | NOT IMPLEMENTED |
| Restricted-record access control | NOT IMPLEMENTED |
| Institutional primary/backup appointments and acceptance | UNRESOLVED |
| Owner/delegate authority evidence | UNRESOLVED |
| Coverage timezone, working days and holiday calendar | UNRESOLVED |
| Institutional email/SMS services | NOT AVAILABLE YET; mock-only direction |
| Restricted system and custodians | UNRESOLVED |
| Operational readiness | NOT VERIFIED |
| Production readiness | NOT READY |
| Merge, deployment, rehearsal, activation and A5 | NOT AUTHORIZED |

No main-branch changes, merge, deployment, external integration, live notification, rehearsal, production-data access, or restricted-system access were performed in this review.

## 8. Decision required to proceed with implementation

The immediate blocker is not a failing unit test. It is the explicit architecture boundary that database persistence and authentication/authorization were deferred. The next implementation step requires a separate Owner scope decision reopening only the specific technical capabilities required for synthetic ORG-03 verification, while preserving all institutional authority and production-use restrictions.
