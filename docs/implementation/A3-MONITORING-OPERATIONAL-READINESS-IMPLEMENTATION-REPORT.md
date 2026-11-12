# EKHC OS — A3 Monitoring Operational-Readiness Implementation Report

**Status:** IMPLEMENTED — EXACT-HEAD CI VERIFIED  
**Date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 branch:** `a3/monitoring-operational-readiness`  
**A2 governing baseline:** `15c971ce703d51adf1db83a340c5dc3c2a987058`  
**Implementation/tested source head:** `1126bcad218a0391efea1c3ac22bdb29c87a0017`  
**Main observed unchanged:** `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`  
**Accepted A4 branch observed unchanged:** `9d77f91dbdbca0b220b5e0d0d735caa525a0c9ec`

## 1. Scope and governance

This implementation executes the Owner-authorized A3 work packages OR-01 through OR-05 under the approved A2 reconciliation. The two approved design decisions were preserved: at most three OSV attempts with bounded backoff and narrowly classified retries; nearest missed exception reminder threshold surfaced on the next successful run, with repeated signals allowed and no delivery state.

The implementation is confined to the separate A3 branch. No merge, default-branch integration, deployment, publication, signing, production operation, schedule activation, dependency update, secret addition, production-data access, or A5 activity was performed. The accepted A4 closure record was not modified.

## 2. Work-package results

| Work package | Result | Implementation/evidence |
|---|---|---|
| OR-01 Positive advisory simulation | PASS | Added a mocked end-to-end `main()` test covering synthetic advisory rendering, Markdown escaping, and finding exit status 1. No live vulnerability or public disclosure was used. |
| OR-02 Bounded OSV retry | PASS | At most 3 total attempts; retry only transient transport `OSError` and HTTP 429/5xx; 20-second per-attempt timeout; 1-second then 2-second backoff; configured request/backoff budget 63 seconds. Exhaustion remains INCOMPLETE/non-zero. |
| OR-03 Missed reminder catch-up | PASS | For positive days remaining, report the smallest configured threshold strictly greater than current days remaining, with threshold and days overdue. Preserve exact-threshold reminders, expiry-day signal, and repeated EXPIRED signals after expiry. Only APPROVED entries are eligible; no register mutation or delivery state. |
| OR-04 Operator runbook | PASS — DOCUMENTED | Added manual execution, exit-code interpretation, INCOMPLETE handling, Owner escalation boundary, and explicit notification/coverage limitations. No responder, channel, rota, or acknowledgement path was invented. |
| OR-05 Production activation gate | PASS — DOCUMENTED / ACTIVATION BLOCKED | Added mandatory separate approval/evidence checklist. Daily schedule remains on the workflow but inactive off the default branch. No schedule or trigger activation was performed. |

## 3. Cross-cutting implementation controls

- Preserved the 2 MiB OSV response cap and existing malformed/incomplete response rejection.
- Added explicit accepted lock grammar: one pinned `name==version` per line, optionally followed only by one or more `--hash=sha256:<64 hex>` tokens; blank lines and full-line comments are ignored. Unsupported pip syntax/options are rejected.
- Kept standard-library-only OSV handling; no dependency or lockfile changes.
- Kept workflow permissions read-only (`contents: read`) and checkout credentials persistence disabled.
- Kept the exception register unchanged and empty.
- Sanitized synthetic advisory content and exception identifiers for Markdown table output.
- No ticket creation, dependency mutation, exception approval/revocation/renewal/expiry mutation, or guaranteed external notification was added.

## 4. Exact-head GitHub Actions evidence

Both workflows completed successfully on the implementation/tested source head `1126bcad218a0391efea1c3ac22bdb29c87a0017`:

- Quality run #162, ID `43129406546`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43129406546
  - Django system check: PASS
  - Django test suite: PASS — 71 tests
  - Ruff lint: PASS
  - Ruff format check: PASS
  - pip-audit: PASS
- Security monitor run #47, ID `43129406350`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43129406350
  - 32 locked PyPI packages queried
  - 0 OSV advisories returned
  - 0 approved exception reminders/expiries (register remains empty)

The successful zero-advisory run is not evidence of a live positive advisory, OSV SLA, or guaranteed external notification. Positive advisory behavior is covered by synthetic mocked tests.

## 5. Files changed

1. `.github/workflows/quality.yml` — require the two new operational documents.
2. `scripts/security_monitor.py` — retry/backoff, strict lock grammar, overdue reminders, report rendering.
3. `tests/test_security_monitor.py` — retry classification/exhaustion, malformed response no-retry, reminder catch-up, strict lock grammar, positive report/exit path.
4. `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md` — implementation semantics and limitations.
5. `docs/operations/SECURITY-MONITORING-OPERATOR-RUNBOOK.md` — manual run and response procedure.
6. `docs/operations/SECURITY-MONITORING-PRODUCTION-ACTIVATION-GATE.md` — separate activation prerequisites and prohibitions.

No changes to `requirements-lock.txt`, `requirements.txt`, `requirements-dev.txt`, `docs/security/exception-register.json`, the monitoring workflow schedule, the accepted A4 record, or `main`.

## 6. Remaining blockers and limitations

- External notification delivery, recipient identities, acknowledgement, responder/backup coverage, holiday coverage, and restricted exception-record custody remain UNRESOLVED / NOT VERIFIED.
- No real exception entry exists; no real exception reminder was exercised.
- No live positive OSV advisory was returned; only synthetic test coverage exists.
- OSV availability, SLA, rate-limit behavior beyond the tested HTTP responses, and network-path guarantees are not established.
- The 63-second figure is the configured per-attempt-timeout plus backoff budget, excluding runner and local-processing overhead; it is not an OS-level hard real-time guarantee.
- A successful GitHub run is not human acknowledgement or guaranteed out-of-band delivery.

## 7. Disposition and next stage

**A3 implementation scope:** 100% complete for OR-01 through OR-05.  
**A3 exact-head automated verification:** PASS on the implementation/tested source head.  
**Operational readiness:** NOT VERIFIED — unresolved human notification and response controls remain.  
**Production readiness:** NOT READY.  
**A4:** NOT STARTED; requires separate verification against the final A3 branch head and review of the evidence record.  
**Merge/default-branch integration, deployment, production operation, schedule activation, and A5:** NOT AUTHORIZED.

Immediate next step: perform A4 independent verification of the final A3 branch head, preserving all listed operational limitations and keeping the production schedule inactive.
