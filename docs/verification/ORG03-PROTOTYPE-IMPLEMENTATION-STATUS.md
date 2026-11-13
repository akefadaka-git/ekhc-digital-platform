# ORG-03 Isolated Durability and Access-Boundary Prototype — Status

**Date:** 2026-11-13  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/org-03-responder-operations`  
**Implementation head at document creation:** `10195cac0ccf8075d585d680a6d9d04940d18c98`  
**Scope:** Synthetic-only prototype; no production runtime integration

## 1. Owner authorization applied

The implementation is limited to:
- a standalone SQLite event-store adapter using Python's standard library;
- temporary test databases only;
- transaction-level acknowledgement arbitration and event replay checks;
- a synthetic-only, deny-by-default record access policy harness;
- unit tests using synthetic identifiers and test records.

The Django settings, application registry, database configuration, URL surface, dependencies, migrations, and production runtime have not been changed. No production database or storage path has been selected.

## 2. Files added

| File | Purpose |
|---|---|
| `scripts/org03_event_store.py` | Isolated SQLite transaction/event-log prototype; event IDs, idempotency keys, per-alert sequence constraints, aggregate version compare-and-update, SHA-256 hash chain, replay |
| `tests/test_org03_event_store.py` | Temporary-database tests for reopen/replay, concurrent same-version requests, stale versions, idempotent retries, rollback, and hash corruption |
| `scripts/org03_synthetic_access_policy.py` | Synthetic-only policy harness; explicit role/action and record/field scopes; deny-by-default |
| `tests/test_org03_synthetic_access_policy.py` | Synthetic tests for anonymous denial, unknown role, inactive/revoked principal, cross-record access, action and field restrictions, and non-synthetic principal denial |

No external dependency was added.

## 3. Verification status

**Implementation present: YES.**  
**Tests authored: YES.**  
**Tests executed locally: NOT RUN.**  
**Exact-head GitHub Actions: NOT RUN / NOT VERIFIED.**  
**Operational readiness: NOT VERIFIED.**  
**Production readiness: NOT READY.**

The GitHub connector returned no combined status checks for the implementation head. A browser-based attempt to dispatch the existing quality workflow did not start because the browser automation wallet was below zero. No payment or top-up is requested; the user's no-paid-services constraint remains in force. A direct local Git clone was also unavailable because the execution environment could not resolve github.com.

Prior CI runs `43384771796` and `43384771790` apply only to the earlier source head `04e0c1c38e5e2c885e582ab9b15d38f47863595e`; they are not evidence for this prototype head.

## 4. Important limits — do not overstate these results

### Event store
- SQLite is a local test adapter, not an approved production database.
- The hash chain detects accidental or unsophisticated record changes when replayed, but plain SHA-256 is not a keyed signature and does not prevent an attacker with write access from rewriting the database and recomputing the chain.
- The authored concurrency test uses two threads and separate SQLite connections in one process. Multi-process, multi-host, high-load, and production database behavior remain untested.
- Reopening a new store instance verifies committed-data replay. Hard process termination at every commit boundary, filesystem/power-loss behavior, backup restoration, and corruption recovery remain untested.
- The event-store adapter is not wired into Django or any production service.

### Restricted-record boundary
- The policy harness receives a synthetic principal object from its caller. It does not authenticate that principal.
- Its role labels are test fixtures, not EKHC offices, constitutional authority, or actual staff assignments.
- No restricted personal data, real identity provider, MFA, encryption/key custody, audit service, retention policy, backup, or production authorization endpoint exists.
- Therefore, this is a policy-unit-test harness, not a deployed restricted-record access-control system.

## 5. Acceptance matrix

| Requirement | Current evidence | Status |
|---|---|---|
| PERSIST-01 atomic append and aggregate update | Transaction and uniqueness constraints implemented; authored rollback test | PARTIAL — test execution pending |
| PERSIST-02 idempotent retry | Idempotency key and payload conflict handling implemented; authored tests | PARTIAL — test execution pending |
| CONC-01 competing acknowledgement requests | Same-version arbitration uses SQLite write transaction; two-thread test authored | PARTIAL — test execution pending; multi-process not tested |
| REC-01 restart/replay | New store instance replays event log and checks sequence/hash/aggregate | PARTIAL — test execution pending; hard-crash and backup recovery not tested |
| ACL-01 synthetic policy boundary | Anonymous/default-deny, role/action, record scope, field allow-list tests authored | PARTIAL — test execution pending; no real authentication or deployed ACL |
| Production security controls | Not in this authorization | NOT IMPLEMENTED |
| Operational responder readiness | Institutional appointments, authority, calendars and routes unresolved | NOT VERIFIED |

## 6. Governance

- Main branch remains unchanged at the previously verified `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.
- No merge, deployment, production integration, live notification, rehearsal, production data, real identities, or restricted-system access occurred.
- A5 remains separate and unauthorized.
- No claim of operational or production readiness is made.

## 7. Next verification step

Run the repository's existing quality workflow against the exact implementation head `10195cac0ccf8075d585d680a6d9d04940d18c98` using an available no-cost GitHub Actions route. Resolve any syntax, formatting, lint, or test failures, then repeat exact-head verification. Only after the unit tests pass should the prototype be extended to multi-process concurrency and controlled crash-injection tests.

## 8. Verification refinement after initial implementation

Two follow-up commits refined the prototype:
- `c0659d26fcca09314f35d141824b9447f6e043fe`: bind alert ID, event ID, sequence, idempotency key, and canonical event payload into the event hash chain; use the aggregate update row count for compare-and-update validation.
- `c8f516e1ed07110c63bc7f368b472ee87254b4c3`: add separate concurrent primary-ack/deadline and backup-ack/deadline races, plus same-version duplicate backup acknowledgement arbitration.

The final implementation head for this increment is `c8f516e1ed07110c63bc7f368b472ee87254b4c3`.

The race tests are still **AUTHORED / NOT RUN**. The hash chain remains tamper-evident rather than authenticated: a database writer able to rewrite the full log can recompute an unkeyed SHA-256 chain. Independent process-level crash injection and multi-process stress testing remain outstanding.


## 9. Additional process-level tests authored

Commit `73c7c35814689a035e3c45b19985beb3d53e5a86` adds two more synthetic tests:
- Separate OS processes racing an acknowledgement and the primary deadline against the same aggregate version; expected result is one committed event and one stale-version rejection.
- A child process terminated abruptly with an uncommitted SQLite write; a fresh store instance must reopen, replay, and confirm the uncommitted event was rolled back.

These tests are **AUTHORED / NOT RUN**. They use the POSIX `fork` multiprocessing context and therefore target the repository's Linux CI runner; portability to non-POSIX environments is not claimed. The event-store test module now contains 12 test methods. The full repository test suite and exact-head CI remain outstanding.


## 10. Exact-head Linux verification and JUnit evidence — 2026-11-13

This section supersedes the earlier pending-test statements in Sections 3, 5, 7, and 9 for the isolated synthetic prototype only.

**Verified branch head:** `14916f23f6fc1ad7c2bed7968169b944e2780772`  
**Workflow:** [A3 quality checks — run 43395710793](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43395710793)  
**Runner:** Ubuntu 24.04  
**Run conclusion:** SUCCESS  
**Exact-head match:** the workflow `head_sha` matched the branch head at verification.

### 10.1 Test evidence

- Full Django repository suite: 114 tests passed; system check reported no issues.
- Dedicated ORG-03 prototype suite: 20 tests passed.
- JUnit report: `artifacts/org03-junit.xml`.
- Dedicated console log: `artifacts/org03-tests.log`.
- Uploaded artifact: `org03-linux-test-evidence`, artifact ID `14023160981`, 14-day retention.
- Ruff lint: PASS.
- Ruff format check: PASS.
- Dependency audit: PASS; no known vulnerabilities reported.

The uploaded JUnit XML was retrieved and inspected. It reports 20 ORG-03 test cases with zero failures, errors, or skipped tests. The tests cover the synthetic persistence, concurrency, process-level race, abrupt uncommitted-write recovery, replay/integrity, and synthetic access-policy scenarios.

### 10.2 Updated acceptance status

| Requirement | Current evidence | Status |
|---|---|---|
| PERSIST-01 isolated synthetic append/replay and rollback | SQLite test adapter and passing JUnit cases | PASS — isolated prototype only |
| PERSIST-02 idempotent retry | Passing JUnit cases | PASS — isolated prototype only |
| CONC-01 thread/process acknowledgement arbitration | Passing thread and POSIX process tests | PASS — tested Linux prototype scope |
| REC-01 reopen/replay and abrupt uncommitted-write recovery | Passing JUnit cases | PASS — tested SQLite process scope; not power-loss or backup restoration |
| ACL-01 synthetic policy boundary | Passing synthetic policy tests | PASS — policy harness only; no authentication or deployed ACL |
| Full repository quality checks | Exact-head Linux workflow | PASS |
| Operational responder readiness | Actual roster, acceptance, authority, coverage, calendar and routing still absent | NOT VERIFIED |
| Production security controls and service integration | Not part of this prototype | NOT IMPLEMENTED |

### 10.3 Evidence limits and governance

The JUnit result establishes only that the authored tests passed on the specified Linux runner and exact source head. It does not establish multi-host/high-load database behavior, filesystem or power-loss durability, backup restoration, cryptographic authenticity of the unkeyed hash chain, production authentication/authorization, institutional readiness, or deployed restricted-record protection.

No Django runtime integration, production database selection, real identity, provider integration, live notification, operational rehearsal, merge, deployment, or A5 action occurred. A4 remains open pending independent technical/security review and the outstanding institutional evidence. Production readiness remains NOT READY.

## 11. R1–R6 remediation implementation increment — 2026-11-13

Owner approval to implement was received on 2026-11-13. The approved synthetic-only specification and implementation decisions are recorded in `docs/verification/ORG03-R1-R6-REMEDIATION-SPECIFICATION.md`.

### 11.1 Changes in this increment

- **R2:** `load_state()` now starts an explicit read transaction before loading aggregate metadata and replaying event history, so both reads use one SQLite snapshot.
- **R4:** synthetic policy checks now require an explicit non-empty field set, apply role-specific read/update field scopes, and return the exact permitted field projection. Read permission does not imply update permission.
- **R5:** event rows now retain a canonical request envelope including alert ID, event ID, idempotency key, expected version, event type, and payload. Exact retries return the originally committed result snapshot; changed event IDs or other request semantics conflict.
- **R6:** internal store connections are deterministically closed. Writer reservation uses bounded lock/busy retries and raises a typed `EventStoreBusy` when the deadline expires.

### 11.2 New acceptance coverage authored

- A coordinated WAL reader/writer test checks that an in-flight read returns a coherent pre-commit snapshot and a subsequent read sees the committed update.
- A held-writer-lock test checks bounded timeout and typed contention failure.
- A connection-lifecycle test checks closure after context exit.
- Synthetic policy tests cover omitted/empty fields, role-specific update scope, and unknown fields.
- Idempotency tests cover event-ID substitution and replay of the original result after a later valid transition.

**Current implementation head at report update:** `686e26cc4e494c82884942a4ddd2ed37bddc5496`.

### 11.3 Remaining R1/R3 work

- **R1 — NOT IMPLEMENTED:** keyed HMAC-SHA-256 event authenticity, protected checkpoint trust boundary, key identification/rotation and rollback detection are still outstanding.
- **R3 — NOT IMPLEMENTED:** immutable versioned synthetic authority registry, event-bound authority context and effective-time revocation semantics are still outstanding.

### 11.4 Verification

Workflow run for prior exact head `dee411f7c0ac4a2f24b19044ae9b85cfe91791c5` exposed one failure in the new original-result test scenario (the test attempted an invalid deadline transition after acknowledgement). That test was corrected on `bafd014c1bd9444cbb1e2a386e7e433974aaa6c2`. The corrected test scenario passed on `bafd014c1bd9444cbb1e2a386e7e433974aaa6c2` (123 Django tests and 29 ORG-03 tests), but Ruff lint failed on line-length/import-format findings. Those findings were corrected in commits `cf598abed933d2fc034bbdb6e07e1b9dd311c08e` and `686e26cc4e494c82884942a4ddd2ed37bddc5496`. Exact-head workflow `43401866233` is running on `686e26cc4e494c82884942a4ddd2ed37bddc5496`; JUnit, logs, Ruff, formatting and dependency audit remain pending inspection.

A4 remains OPEN. Production readiness remains NOT READY. No merge, deployment, production runtime integration, real identities/data, live notifications, institutional rehearsal or A5 action occurred.
