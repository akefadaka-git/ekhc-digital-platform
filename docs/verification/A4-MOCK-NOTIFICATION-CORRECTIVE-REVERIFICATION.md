# A4 Corrective Re-verification — Mock Notification

**Status:** VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS  
**Verification branch:** `a4/mock-notification-corrective-reverification`  
**Initial verification baseline:** `12971f893c50419152e8de2c4b97cc0caad92641`  
**Corrective source/test head inspected:** `5878462a00630da53133d32b43d09d961013520f`  
**Parent A3 implementation head:** `b3c417f011d9e484683b875d80e839f60ab771c5`

## 1. Scope and governance

This A4 increment independently re-verifies A4-MN-F01 and A4-MN-F02 after the Owner-authorized A3 corrective increment. Scope is limited to source/test inspection, behavior verification, and this verification record. It does not authorize merge, deployment, publication, signing, schedule activation, rehearsal, production operation, or A5.

## 2. Source and provenance inspected

The complete files were successfully retrieved from branch `a3/mock-notification-a4-corrections`, which resolves to the corrective implementation branch:

- `notifications/mock.py`
  - Blob SHA: `753647ef82f99490619143d65bd9e13cdb0bd9ff`
- `tests/test_mock_notifications.py`
  - Blob SHA: `40c04460345b72ed3de34e97b2d054694136144f`

The source and tests were read in full. The implementation/test source head is `5878462a00630da53133d32b43d09d961013520f`.

GitHub compare from original A3 final head `b3c417f011d9e484683b875d80e839f60ab771c5` to corrective source/test head `5878462a00630da53133d32b43d09d961013520f` reports four commits ahead, zero behind, and exactly two changed paths:
- `notifications/mock.py` — 30 additions, 9 deletions
- `tests/test_mock_notifications.py` — 40 additions

The final A3 corrective branch head is `12971f893c50419152e8de2c4b97cc0caad92641`; its difference from tested source/test head is a documentation-only implementation-report update.

## 3. Finding-by-finding independent disposition

### A4-MN-F01 — MEDIUM — Destination mismatch during duplicate replay

**Implementation inspected:** `NotificationOrchestrator.notify()` preflight retrieves any existing receipt using `(notification.event_id, channel)`. If a prior receipt exists and its `destination_reference` differs from the newly requested destination, the method raises `ValueError("Idempotency conflict: ...")` before appending request audit events or processing channels. A same-destination replay reaches the duplicate-suppression path, appends a duplicate-suppressed audit event, and returns the original stored receipt without another adapter attempt.

**Regression tests inspected:**
- `test_duplicate_event_is_suppressed_per_channel` checks same-destination replay returns equal receipts, records exactly one `mock_attempted` event, and records duplicate suppression.
- `test_duplicate_event_with_changed_destination_is_rejected` checks a changed destination raises the idempotency-conflict error, preserves exactly one receipt, and confirms the stored receipt remains bound to the original destination.

**Disposition: CORRECTED — PASS.** The destination binding is enforced before any request-side processing. No exactly-once or durable cross-process idempotency guarantee is inferred.

### A4-MN-F02 — LOW — Destination map not validated atomically

**Implementation inspected:** Before appending `notification_requested`, the method iterates over the complete supplied destination mapping and validates every channel type, synthetic destination format/channel prefix, and existing event/channel destination binding. Only after this preflight loop succeeds does it append the request audit event and begin channel processing. Thus a later invalid entry or later existing-destination conflict cannot leave earlier channels partially processed.

**Regression tests inspected:**
- `test_destination_mapping_is_preflighted_before_any_attempt` supplies a valid first destination and invalid later destination, expects rejection, and asserts both the receipt map and audit event list remain empty. Since attempt events are written to that audit list, this also verifies no attempt was recorded.
- `test_existing_destination_conflict_is_preflighted_atomically` establishes an existing SMS receipt, snapshots receipts and audit events, then submits a multi-channel request with a new valid email destination followed by a conflicting SMS destination. It expects an idempotency conflict and asserts both receipts and audit events remain exactly unchanged.

**Disposition: CORRECTED — PASS.** Full mapping validation and existing binding checks precede all processing-side effects.

## 4. Four required behavioral conditions

| Required condition | Inspected implementation/test evidence | Result |
|---|---|---|
| Same event/channel/same destination returns original receipt without a second attempt | Stored receipt lookup and duplicate-suppression test; one attempt asserted | PASS |
| Same event/channel/different destination is rejected and does not return the old receipt as a successful result | Destination binding conflict raises before return; changed-destination test asserts exception and original binding remains | PASS |
| Every channel and destination is validated before processing-side effects | Complete preflight loop precedes request audit and channel processing; valid-first/invalid-later test asserts no receipts or audit events | PASS |
| Existing destination conflicts in a multi-channel request are detected before any new receipt, attempt, or audit event | Existing binding checked in preflight; regression test snapshots and asserts unchanged receipts and audit events | PASS |

The regression tests assert side-effect absence for invalid later entries and multi-channel binding conflicts, not merely the exception. The changed-destination test verifies rejection and preservation of the original receipt binding; the implementation's ordering confirms that this rejection occurs before new audit/attempt side effects.

## 5. CI evidence

The A3 corrective report and PR #11 record successful checks on exact source/test head `5878462a00630da53133d32b43d09d961013520f`:

- Quality run #232 / ID `43202521961`: SUCCESS — 90 tests, Django system check, Ruff lint/format, and pip-audit passed.
  https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43202521961
- Security Monitor run #117 / ID `43202521980`: SUCCESS.
  https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43202521980

These CI results are treated as recorded exact-head evidence. No claim is made that CI proves real provider delivery or human acknowledgement.

## 6. Additional controls observed in inspected source

- Notification configuration requires all three selectors to be explicitly `mock`.
- Unsupported provider/email/SMS/notification environment settings are rejected.
- The module imports no network, SMTP, provider, or SDK clients.
- Adapter destinations must be channel-matched synthetic references.
- Retry behavior remains fixed at three attempts with 1s/2s backoff; only simulated timeout/unavailable outcomes retry.
- Receipts remain `simulated=True`, `delivery_claim=False`, and display `SIMULATED — NOT DELIVERED`.
- Audit and summary output do not expose destination references or payload contents.
- In-memory receipts/audit do not provide durable delivery ledger, cross-process deduplication, or exactly-once delivery.

## 7. Verification outcome

| Item | Result |
|---|---|
| Corrective branch ancestry / compare | PASS — four commits ahead, zero behind |
| Changed-path scope | PASS — implementation and test paths only |
| Full corrective source retrieval and inspection | PASS |
| Full regression-test retrieval and inspection | PASS |
| A4-MN-F01 independent verification | PASS — CORRECTED |
| A4-MN-F02 independent verification | PASS — CORRECTED |
| Exact-head CI evidence | PASS — recorded for source/test head |
| A4 technical verification | VERIFIED-CLOSED |
| Operational readiness | NOT VERIFIED |
| Production readiness | NOT READY |

## 8. Explicit limitations and remaining gates

A4 closes only the two identified mock-notification technical findings. Institutional email and SMS services remain unavailable; actual recipients, responders, responder acceptance/coverage, and restricted-record custody evidence remain unresolved. No real provider delivery, human acknowledgement, external notification, operational rehearsal, or production ingress has been verified. In-memory idempotency/audit remains process-local. The OSV monitoring and operational-readiness limitations recorded in earlier A4 and operational gap records remain unchanged.

PR #11 remains draft and unmerged; PR #10 remains draft and unmerged. The repository default branch was not changed by this verification. No merge, deployment, publication, signing, schedule activation, rehearsal, production operation, or A5 is authorized.

## 9. Closure statement

A4-MN-F01 and A4-MN-F02 are independently VERIFIED-CLOSED based on direct inspection of the complete corrective implementation and regression tests, supported by the recorded exact-head CI evidence. This closure is technical and bounded; it is not operational or production readiness approval.
