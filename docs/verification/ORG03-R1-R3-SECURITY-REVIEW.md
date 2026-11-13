# ORG-03 R1/R3 Security Re-review Report

**Review type:** Internal second-pass technical review  
**Implementation branch:** `a3/org-03-responder-operations`  
**Implementation SHA reviewed:** `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`  
**Exact-head CI:** [Run 43408089840](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43408089840) — SUCCESS  
**Scope:** Synthetic-only SQLite event-store prototype and synthetic authority policy. No production integration.

## Executive disposition

R1 authenticated event integrity and R3 historical authority/revocation controls are implemented and passed the exact-head automated test suite. The internal second-pass review found no additional reproducible bypass in the tested synthetic boundary. This is not an independent external assessment and does not establish production readiness.

**A4 remains PARTIAL / OPEN** until a designated independent reviewer completes review and the institutional evidence gates are satisfied.

## R1 — authenticated event integrity

### Controls inspected

- HMAC-SHA-256 uses caller-supplied key material held by the process; the keyring is not stored in SQLite.
- Event authentication binds alert/event IDs, sequence, idempotency key, canonical event payload, request fingerprint, committed result snapshot, previous hash, algorithm identifier and key ID.
- Key rotation permits retained historical keys to verify old records while newly appended events use the active key. Unknown or revoked keys fail closed.
- The separate checkpoint file authenticates the alert head and is stored outside the SQLite database in a restricted sibling directory.
- Checkpoint writes use temporary-file replacement, fsync and monotonic sequence checks. Read verification captures the checkpoint before the SQLite snapshot transaction.
- Append retries verify the complete authenticated event history before returning an idempotent result.

### Tests inspected

Full database rewrite with recomputed unkeyed hashes; event-ID substitution; truncation with aggregate rewrite; unknown key; revoked key; old/new key rotation; checkpoint MAC tampering; checkpoint rollback; request fingerprint tampering; result snapshot tampering; concurrent duplicate retries; concurrent SQLite reader/writer snapshot.

### Residual R1 risks

1. The checkpoint is a local sidecar, not a remote or independently administered monotonic anchor. Compromise of both database and checkpoint directory, or process memory/key access, is outside the prototype boundary.
2. SQLite commit and filesystem checkpoint replacement are not one atomic transaction. A crash between them can leave a stale checkpoint and cause fail-closed unavailability. Trusted reconciliation/re-anchoring is not implemented.
3. Revoking a key makes all records authenticated by that key unverifiable. Production key compromise recovery and external trust-root governance are not implemented.
4. Production key provisioning, KMS/HSM custody, and checkpoint separation across administrative/security boundaries are not implemented.

## R3 — historical authority and revocation

### Controls inspected

- Authority grants are synthetic, versioned, append-only records with HMAC-authenticated principal, role, alert scope, version, valid-from UTC, effective revocation UTC and key ID.
- SQLite triggers reject update/delete. Replay independently verifies registry record MACs and event-bound authority evidence.
- Human events carry the historical evidence in the event payload; the event HMAC covers it.
- Replay derives the responder principal and role from authenticated event evidence, not from the caller's current responder mapping.
- Revocation creates a new immutable version with an explicit effective UTC timestamp. Replay accepts historical events before that time and rejects events at/after it.
- Authority is scoped to the synthetic alert reference. A grant cannot be replayed against another alert.

### Tests inspected

Historical acceptance before revocation; rejection at/after effective revocation; altered authority evidence; authority registry tampering; cross-principal substitution; cross-alert scope reuse; mutable current responder-map substitution; system-event authority injection; concurrent acknowledgement/revocation boundary race; immutable authority record mutation rejection.

### Residual R3 risks

1. Event timestamps are synthetic caller-supplied UTC values. Production must use a trusted server acceptance timestamp and an authenticated institutional authority source; otherwise caller-controlled backdating is outside the assurance boundary.
2. The registry is local SQLite state. Production needs institutionally governed grant issuance, revocation approval, identity binding, audit retention and independent evidence custody.
3. The synthetic prototype does not implement a real identity provider, delegated authority chain, institutional role lifecycle, or production ACL service.

## Exact-head verification evidence

Run [43408089840](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43408089840), exact implementation SHA `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`, completed SUCCESS on Ubuntu 24.04:

- Django system check: PASS.
- Django tests: 158 passed.
- Dedicated ORG-03 tests: 84 passed.
- JUnit XML: 84 tests, 0 failures, 0 errors, 0 skipped.
- Ruff lint: PASS.
- Ruff format: PASS (76 files already formatted).
- Dependency audit: PASS (no known vulnerabilities).
- Evidence artifact: [14027659042](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43408089840/artifacts/14027659042).

## Independence and gate status

- Internal second-pass review: COMPLETE.
- Independent external security reviewer: NOT OBTAINED.
- A4: PARTIAL / OPEN.
- Operational readiness: NOT VERIFIED.
- Production readiness: NOT READY.
- A5: NOT AUTHORIZED.

An independent review cannot be truthfully claimed from this internal pass. A reviewer must be nominated or a security-review team identified before the independent gate can close. No merge, deployment, production key provisioning, real identity/data processing, live notification, or institutional rehearsal is authorized by this report.
