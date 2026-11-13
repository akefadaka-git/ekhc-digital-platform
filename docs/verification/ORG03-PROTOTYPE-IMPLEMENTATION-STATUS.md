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
