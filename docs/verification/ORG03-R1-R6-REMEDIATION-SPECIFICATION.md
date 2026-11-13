# ORG-03 R1–R6 Remediation Specification and Acceptance-Test Plan

**Status:** DRAFT — OWNER REVIEW REQUIRED  
**Prepared:** 2026-11-13  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/org-03-responder-operations`  
**Baseline reviewed:** `ab4f35f0f1839d22b0e07cce60ed0a9f6921d815`  
**Scope:** Isolated, synthetic-only ORG-03 prototype  
**Implementation status:** NOT AUTHORIZED / NOT STARTED

## 1. Purpose and governing constraints

This document converts the independent source review findings into six bounded remediation work packages and a testable acceptance plan. It is a specification, not an implementation authorization.

The work remains confined to the standalone SQLite prototype and synthetic policy harness. It does not authorize wiring either module into Django or another runtime, selecting a production database, adding authentication or institutional identity integrations, processing real identities or restricted data, enabling notifications, or conducting operational rehearsal.

No merge, deployment, production activation, signing-key provisioning, external service integration, or A5 work is authorized by this document. Preserve `main` and unrelated changes.

## 2. Design principles

1. **Fail closed:** integrity, authority, scope, or consistency uncertainty must reject the operation.
2. **No caller-created trust:** caller-supplied fixtures may remain useful for unit tests, but must never be represented as authenticated identity or authoritative role assignment.
3. **Historical verifiability:** an event must remain verifiable against the authority context that applied when it was accepted.
4. **Atomic state:** aggregate state and its corresponding event must commit or roll back together.
5. **Stable request identity:** an idempotent retry must identify the same logical request, not merely a similar payload.
6. **Bounded resource use:** database contention must have a documented, bounded outcome; connections and transactions must have deterministic lifetimes.
7. **Synthetic-only evidence:** all new fixtures and test databases must use synthetic identifiers and temporary storage.

## 3. R1 — Authenticated event-chain integrity

**Finding addressed:** The existing unkeyed SHA-256 chain is tamper-evident against accidental or unsophisticated changes, but a database writer can rewrite the history and recompute the chain.

### Required behavior

- Define an authenticated event-integrity envelope covering, at minimum: schema/version identifier, alert ID, event ID, sequence, idempotency key, canonical event payload, predecessor digest, algorithm identifier, and key identifier.
- Verification must reject altered, missing, reordered, duplicated, truncated, or cross-alert substituted events.
- A database-only attacker must not be able to forge a valid new history merely by recomputing public hashes.
- The integrity key must not be stored alongside the event database in a form that grants the same writer signing capability.
- Define key rotation, retired-key verification, compromise response, and verification behavior when a key is unavailable.
- Define a separately protected checkpoint/chain-head mechanism. The checkpoint must detect whole-database rewrite or rollback, not merely validate an internally consistent rewritten chain.
- Keep key material synthetic/test-only in this prototype. Do not create or provision production keys.

### Design decision required before implementation

Choose and document one design:
- HMAC with protected key custody and externally protected checkpoints; or
- digital signatures with a protected signing key and independently verifiable public key; or
- another explicitly reviewed construction with equivalent integrity and operational properties.

The design must state the threat model, algorithm and parameters, key custody boundary, checkpoint storage/trust boundary, rotation/revocation model, and recovery behavior. Do not silently choose a production key-management service.

### Acceptance tests

- **R1-AT-01:** Modify one stored payload byte; verification fails closed.
- **R1-AT-02:** Modify event ID, alert ID, sequence, idempotency key, predecessor digest, or algorithm/key identifier; verification fails.
- **R1-AT-03:** Recompute every unkeyed digest after rewriting the complete database; authenticated verification still fails.
- **R1-AT-04:** Delete, reorder, duplicate, truncate, or transplant an event between alerts; verification fails.
- **R1-AT-05:** Present an unknown, revoked, or unavailable key identifier; verification fails closed with a typed, non-sensitive error.
- **R1-AT-06:** Verify historical events across a supported key rotation; valid old events remain verifiable while newly revoked/compromised key use is rejected according to the approved policy.
- **R1-AT-07:** Roll back the database to an earlier internally valid checkpoint; comparison with the independently protected latest checkpoint detects rollback.
- **R1-AT-08:** A test process with database write access but no integrity key cannot create an accepted forged event.

**Evidence:** design decision record, negative-test output, key-rotation test evidence, and checkpoint rollback test evidence.

## 4. R2 — Consistent read snapshots

**Finding addressed:** `load_state()` reads the aggregate and event log in separate autocommit SELECT statements, allowing a concurrent commit between reads.

### Required behavior

- Read aggregate metadata and its event history within one explicit SQLite read transaction/snapshot.
- Ensure the snapshot is consistently released on success and every exception path.
- Preserve existing fail-closed aggregate/log consistency checks.
- Do not weaken writer serialization or compare-and-update behavior.
- Document SQLite journal and transaction assumptions used by the test adapter.

### Acceptance tests

- **R2-AT-01:** Coordinate a reader after its aggregate SELECT and a writer before its commit; prove the reader sees one coherent snapshot rather than a mixed aggregate/log view.
- **R2-AT-02:** After the reader completes, a subsequent read sees the writer's committed version and event.
- **R2-AT-03:** Force replay/integrity failure during the read; the read transaction is rolled back/closed and a later read succeeds.
- **R2-AT-04:** Run repeated reader/writer interleavings; no false aggregate/log mismatch occurs for valid committed histories.
- **R2-AT-05:** Genuine aggregate/event divergence still fails closed.

**Evidence:** deterministic synchronization-based tests, not sleep-only race tests, plus exact-head Linux JUnit output.

## 5. R3 — Historical authority evidence

**Finding addressed:** replay uses the caller's current `authorized_responder_refs`, so historical event validity depends on mutable caller-supplied data.

### Required behavior

- Each human-originated event must reference an immutable authority-context identifier/version applicable at event acceptance.
- The event must carry the minimum authority evidence reference needed to verify who/what was authorized, for which role/scope, and during which validity interval.
- Replay must resolve that historical authority context from a controlled, immutable test fixture/registry; it must not trust an arbitrary current mapping supplied with each replay call.
- Revocation must have explicit effective-time semantics: distinguish events validly accepted before revocation from attempts after revocation.
- Missing, ambiguous, altered, or unverifiable historical authority evidence must fail closed.
- This prototype remains synthetic. It does not establish actual EKHC office, Owner, delegate, staff, or responder authority.

### Acceptance tests

- **R3-AT-01:** A valid synthetic responder event replays against its recorded authority-context version.
- **R3-AT-02:** Changing the caller's current responder mapping does not rewrite the historical validity of an already accepted event.
- **R3-AT-03:** A new event using a revoked authority context after its effective revocation time is rejected.
- **R3-AT-04:** A valid event accepted before revocation remains verifiable under the documented historical policy.
- **R3-AT-05:** Unknown, missing, altered, expired, or mismatched authority-context references fail closed.
- **R3-AT-06:** Cross-alert or cross-principal substitution of authority evidence is rejected.
- **R3-AT-07:** Replay results are deterministic when the same immutable event and authority evidence are supplied.

**Evidence:** versioned synthetic authority fixtures, revocation-time boundary tests, and replay consistency results.

## 6. R4 — Mandatory field scope and explicit synthetic policy boundary

**Finding addressed:** `requested_fields=None` skips field-level authorization, and `authorize()` returns no filtered projection. The principal and record objects are caller-constructed fixtures.

### Required behavior

- For synthetic read operations, require an explicit, non-empty requested field set; omission must fail closed.
- Reject unknown fields and actions; do not treat a missing field list as unrestricted access.
- Separate read-field scope from update-field scope. An update must specify exactly which fields it intends to change and must not inherit read permission.
- Provide a pure policy decision/projection interface that returns the permitted field set or a typed decision; callers must not infer permission from a successful call with no output.
- Keep synthetic fixture construction visibly separate from identity verification. The module must continue to state that it is not authentication.
- Do not claim production ACL coverage. A real boundary would require trusted identity/role resolution and enforcement at the actual data-access layer, which remains out of scope.

### Acceptance tests

- **R4-AT-01:** A read request with omitted fields is denied.
- **R4-AT-02:** An empty field set is denied unless an explicitly approved no-disclosure operation is defined.
- **R4-AT-03:** A request containing any unknown or disallowed field is denied as a whole.
- **R4-AT-04:** A permitted read returns only the explicitly allowed projection; disallowed fields are absent.
- **R4-AT-05:** Read permission does not imply update permission; update field scope is independently enforced.
- **R4-AT-06:** Anonymous, inactive, non-synthetic, unknown-role, cross-record, and unassigned-action cases remain denied.
- **R4-AT-07:** A forged caller-created fixture is explicitly classified as a unit-test input, not accepted as evidence of authenticated identity.
- **R4-AT-08:** Unknown classification and malformed scope data fail closed.

**Evidence:** synthetic policy unit tests and proof that the returned projection excludes unauthorized fields. No production authorization claim.

## 7. R5 — Complete idempotency request identity

**Finding addressed:** duplicate-key handling compares event payload but does not bind the retry to the original event ID.

### Required behavior

- Define a canonical immutable request envelope containing alert ID, event ID, idempotency key, expected aggregate version, event type, and canonical payload. Include any other field that changes operation semantics.
- Persist a request fingerprint derived from that complete envelope.
- A retry with the same idempotency key and identical request envelope returns the original committed result without appending a second event.
- Reuse of an idempotency key with any different identity or semantic field raises a typed conflict.
- A retry must not silently return a different later aggregate state as though it were the original response. Define and preserve the original committed result/version semantics.
- Ensure the unique database constraint and transaction ordering preserve behavior under simultaneous duplicate requests.

### Acceptance tests

- **R5-AT-01:** Exact retry returns the original committed outcome and creates no new event.
- **R5-AT-02:** Same key with a different event ID is rejected.
- **R5-AT-03:** Same key with a different alert ID is rejected.
- **R5-AT-04:** Same key with a different expected version is rejected.
- **R5-AT-05:** Same key with a changed event type or payload is rejected.
- **R5-AT-06:** Concurrent identical retries create exactly one event and return equivalent original outcomes.
- **R5-AT-07:** Concurrent conflicting retries produce one accepted request and a typed conflict for the other; no partial event is left behind.
- **R5-AT-08:** A retry after later aggregate transitions still returns the defined original operation result, not an ambiguous current-state substitute.

**Evidence:** deterministic duplicate/concurrent retry tests, event-count assertions, and persisted request-fingerprint inspection.

## 8. R6 — Deterministic connection lifecycle and bounded contention

**Finding addressed:** SQLite connection context-manager use does not itself close connections, and lock contention has no explicit bounded retry/caller outcome contract.

### Required behavior

- Guarantee connection closure on success, exceptions, rollback, and initialization failure.
- Make transaction ownership explicit; no helper may unexpectedly commit or close a transaction owned by its caller.
- Define which SQLite errors are retryable (for example, bounded lock/busy contention) and which are terminal (integrity, schema, malformed SQL, corruption).
- Use bounded retries with capped backoff and an overall deadline. Do not retry indefinitely or retry non-transient failures.
- Preserve idempotency and optimistic-version semantics across retries.
- Surface exhausted contention as a typed error that callers can safely handle.
- Do not add a background worker, distributed lock, or production database dependency in this work package.

### Acceptance tests

- **R6-AT-01:** Connections close after successful reads/writes.
- **R6-AT-02:** Connections close after injected exceptions and rollback paths.
- **R6-AT-03:** Initialization failure does not leak an open connection.
- **R6-AT-04:** A transient lock is retried within the configured bound and succeeds when the lock is released in time.
- **R6-AT-05:** A lock held beyond the deadline returns the documented typed contention error within the time bound.
- **R6-AT-06:** Non-retryable database errors are not retried.
- **R6-AT-07:** Retry exhaustion does not duplicate an event or bypass expected-version checks.
- **R6-AT-08:** Repeated open/close cycles do not cause file-handle growth or prevent temporary database cleanup on the Linux runner.

**Evidence:** injected lock tests, connection lifecycle tests, bounded-duration assertions, and exact-head Linux JUnit output.

## 9. Cross-work-package regression and verification

The following existing behavior must remain covered after remediation:

- one winner for same-version acknowledgement/deadline races;
- stale aggregate versions cannot overwrite committed transitions;
- atomic event + aggregate commit/rollback;
- sequence uniqueness and replay consistency;
- duplicate idempotent retry does not append a duplicate;
- abrupt process termination before commit leaves no partial committed event;
- synthetic policy denies anonymous, inactive, unknown-role, cross-record, and unassigned-action access;
- no real identity, production record, external notification, Django runtime, or production database is introduced.

### Required verification sequence

1. Unit tests for each R1–R6 work package.
2. Combined ORG-03 synthetic suite with JUnit XML and console log.
3. Full repository Django test suite and system checks.
4. Ruff lint and format checks.
5. Dependency audit.
6. Inspect the exact GitHub Actions run SHA and retrieve/parse the JUnit artifact.
7. Review changed-file list to confirm scope containment.
8. Record unresolved limitations and evidence links; do not infer production readiness from passing synthetic tests.

## 10. Proposed implementation order and dependencies

| Order | Work package | Dependency / gate |
|---|---|---|
| 1 | R1 authenticated integrity design | Owner selects and approves cryptographic/key/checkpoint design before code |
| 2 | R2 consistent read snapshots | Independent; can be implemented after this specification is approved |
| 3 | R5 complete idempotency identity | Coordinate schema/envelope with R1 |
| 4 | R3 historical authority evidence | Depends on approved immutable event envelope and authority-context format |
| 5 | R4 mandatory field scope | Synthetic harness only; no real identity integration |
| 6 | R6 connection lifecycle/contention | Independent, but regression-tested with transaction and idempotency behavior |

Implementation may be split into separate commits so each work package can be reviewed and reverted independently. R1 key/checkpoint architecture must be decided before implementation; R3 and R5 data-envelope decisions must be reconciled before their code changes.

## 11. Owner review and approval checklist

Please review these explicit decisions before implementation:

- [ ] Approve the R1 threat model and select HMAC, digital signatures, or request a revised design.
- [ ] Approve the independently protected checkpoint concept and its trust boundary.
- [ ] Approve R2 single-snapshot read semantics.
- [ ] Approve immutable, versioned synthetic authority evidence and revocation-time semantics for R3.
- [ ] Approve R4 fail-closed behavior when requested fields are omitted or empty.
- [ ] Approve R5 binding idempotency to the complete request envelope and returning the original operation result.
- [ ] Approve R6 bounded retry/deadline behavior and typed contention failure.
- [ ] Confirm that implementation remains limited to synthetic fixtures, temporary SQLite files, scripts, tests, and verification documentation.

**Implementation gate:** No R1–R6 source-code or test-code implementation begins until the Owner has reviewed this specification and explicitly approved it. A review request, comment, or request for clarification is not implementation approval.

## 12. Current status

| Item | Status |
|---|---|
| Independent source review | COMPLETED |
| R1–R6 specification | DRAFTED |
| Acceptance-test plan | DRAFTED — 43 named acceptance cases |
| Specification reviewed by Owner | PENDING |
| Implementation | NOT STARTED — approval gate |
| Exact-head tests for remediation | NOT RUN |
| A4 verification | OPEN |
| Operational readiness | NOT VERIFIED |
| Production readiness | NOT READY |
| A5 | NOT AUTHORIZED |
