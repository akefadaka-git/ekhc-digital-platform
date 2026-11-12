# A4 Independent Verification — Mock Notification Increment

**Verification status:** PARTIAL — CORRECTIVE ACTION REQUIRED  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Verification branch:** `a4/mock-notification-independent-verification`  
**Verified implementation branch:** `a3/mock-notification-implementation`  
**Exact implementation branch head reviewed:** `b3c417f011d9e484683b875d80e839f60ab771c5`  
**Implementation/test source SHA:** `0609ee826ea7a0c44810213d406af7d6925230d4`  
**Specification baseline:** `03ae65da832906db2cad890d22af6caca49ed0ec`

## 1. Verification scope and independence

This A4 review independently inspected the implementation, tests, approved Phase 1.2 architecture specification, implementation report, branch ancestry, pull-request metadata, and exact-head GitHub Actions evidence. It is a bounded technical review of the mock-only notification increment; it does not verify live notification delivery or operational readiness.

No implementation code, test, workflow, dependency, permission, secret, variable, exception register, or production configuration was changed during A4. This branch adds only this verification record.

## 2. Exact-head CI evidence

Both configured workflows completed successfully on the exact implementation branch head `b3c417f011d9e484683b875d80e839f60ab771c5`. GitHub's commit check-runs endpoint reported both checks completed with conclusion `success`.

1. **A3 quality checks — run #227, ID `43199714346`, SUCCESS**  
   [GitHub Actions run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43199714346)
   - Django system check: PASS
   - Django test suite: PASS — 87 tests
   - Ruff lint: PASS
   - Ruff format: PASS — 65 files already formatted
   - pip-audit: PASS — no known vulnerabilities found

2. **Read-only security monitor — run #112, ID `43199714370`, SUCCESS**  
   [GitHub Actions run](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43199714370)
   - OSV advisory query: PASS; zero matching advisories returned for locked PyPI package versions.
   - Exception register query: PASS; no committed exception entries were reported.

The comparison from implementation/test source SHA `0609ee826ea7a0c44810213d406af7d6925230d4` to exact final branch head `b3c417f011d9e484683b875d80e839f60ab771c5` is one commit ahead, zero behind, with only the implementation report modified. The tested implementation and test files are unchanged.

CI success proves configured automated checks passed. It does not prove provider delivery, external service availability, human acknowledgement, or operational readiness.

## 3. Independent findings

### A4-MN-F01 — MEDIUM — Idempotency key does not bind the destination

**Evidence:** In `notifications/mock.py`, `NotificationOrchestrator.notify()` uses `(notification.event_id, channel)` as the receipt/deduplication key. The destination reference is not part of the key, and a duplicate request returns the prior receipt without checking that the requested destination matches the destination recorded in that receipt.

**Reproduction path:** Submit event `SYNTH-EVENT-0001` to `synthetic-email-recipient-01`; submit the same event/channel again to `synthetic-email-recipient-02`. The second call is classified as a duplicate and returns the first receipt, whose destination reference is still `synthetic-email-recipient-01`.

**Impact:** The caller can receive a receipt that does not correspond to the destination in its current request. In a future provider-backed implementation, this ambiguity could conceal a routing change or cause incorrect delivery accounting. Current implementation remains mock-only and makes no external delivery.

**Required correction:** Define the idempotency contract explicitly. At minimum, reject a repeated event/channel request when its destination differs from the original; alternatively, use a destination-bound idempotency key if the approved notification policy permits multiple destination-specific sends. Add tests for changed-destination replay and same-destination duplicate replay. Do not claim exactly-once behavior.

**Disposition:** OPEN — A3 corrective change required.

### A4-MN-F02 — LOW — Destination map is not validated atomically before processing

**Evidence:** `notify()` validates each channel/destination inside the processing loop. With a mapping containing a valid first channel followed by an invalid channel or destination, the earlier channel may already have produced a receipt and audit events before the later invalid entry raises an exception.

**Impact:** A rejected multi-channel request can leave partial in-memory results and audit state. This is not external delivery, but makes the operation's all-or-nothing validation semantics unclear.

**Required correction:** Validate all supplied channel keys and synthetic destination references before processing any channel; add a test with a valid first entry and invalid later entry that proves no attempt or receipt is recorded.

**Disposition:** OPEN — recommended A3 correction before A4 closure.

## 4. Verified controls

- All three mode selectors must be explicitly `mock`; unsupported notification/email/SMS-prefixed environment settings are rejected by the environment loader.
- No network, SMTP, provider, or SDK client is imported by the mock module.
- Synthetic destination references are channel-matched and validated when processed.
- Mock outcomes are deterministic; transient outcomes are bounded to three attempts with 1s/2s backoff; permanent rejection is not retried.
- Receipts carry `simulated=true`, `delivery_claim=false`, and `SIMULATED — NOT DELIVERED`.
- Summary output omits destination references and payload data.
- Simulated acknowledgement is explicitly labeled as simulated and uses only synthetic responder-role references.
- Retry/idempotency/audit state is in-memory only; there is no durable delivery ledger, cross-process deduplication, or exactly-once guarantee.
- No real provider delivery, actual human acknowledgement, recipient routing policy, or operational service has been established.

## 5. Repository and governance checks

- Implementation branch head reviewed: `b3c417f011d9e484683b875d80e839f60ab771c5`.
- Approved specification baseline: `03ae65da832906db2cad890d22af6caca49ed0ec`.
- Implementation branch comparison against specification: 23 commits ahead, 0 behind; four added paths (implementation report, package initializer, mock implementation, test module).
- Draft PR #10 remains open, draft, unmerged, and targets `ops/mock-notification-architecture-spec`: [PR #10](https://github.com/akefadaka-git/ekhc-digital-platform/pull/10).
- `main` remains at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.
- No merge, deployment, schedule activation, publication, signing, production operation, rehearsal, or A5 was performed or authorized.

## 6. A4 disposition and next gate

**A4 technical verification:** PARTIAL — NOT CLOSED.  
**Findings:** 2 open (1 MEDIUM, 1 LOW).  
**A3 implementation:** CI PASS; corrective changes required for the findings above.  
**Operational readiness:** NOT VERIFIED.  
**Production readiness:** NOT READY.

A4 cannot close until the two findings are corrected on a dedicated A3 corrective branch and independently re-verified against the resulting exact branch head. A4 closure does not itself authorize merge, deployment, schedule activation, rehearsal, or A5; each remains separately gated.

**Change-control boundary:** This verification branch contains only this A4 record. No source-code or workflow changes were made during verification.
