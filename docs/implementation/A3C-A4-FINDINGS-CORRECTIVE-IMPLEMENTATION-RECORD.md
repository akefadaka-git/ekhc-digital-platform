# EKHC OS — A3 corrective implementation record for A4-F01–F04

**Base:** `a8042051824ddb50592492ee75d5aad24d1bb03a`  
**Corrective branch:** `a3/monitoring-operational-readiness-a4-corrections`  
**Scope:** Owner-authorized A3 corrective work only; no merge, deployment, schedule activation, or A5.

## Corrections

- **A4-F01:** Removed the misleading hard-wall-clock interpretation. The implementation now names the 63-second figure a nominal configured socket-timeout plus backoff budget. Documentation explicitly states that urllib's timeout is an inactivity timeout and a continuously streaming response can exceed the nominal budget. No hard end-to-end deadline is claimed.
- **A4-F02:** Replaced the literal escaped newline sequence between the retry explanation and read-only controls with actual Markdown paragraph breaks.
- **A4-F03:** Corrected report evidence references to be reconciled against the exact corrective implementation commit and its workflow run metadata after CI completes.
- **A4-F04:** Added tests proving HTTP 429/5xx exhaustion stops after exactly three attempts and exactly two backoff sleeps, and that `main()` returns exit code 2 with an INCOMPLETE summary on OSV transport failure.

## Boundaries

The response-size cap, retry classification, three-attempt maximum, 1s/2s backoff, read-only permissions, empty exception register, inactive schedule, and operational-notification limitations remain unchanged. The accepted A4 branch and `main` are not modified.

## Corrective CI evidence

**Corrective code/test source head:** `35c6cad2bae0cf7dd7400b3605e315f71c476f4b`  
**Validation PR:** [#8](https://github.com/akefadaka-git/ekhc-digital-platform/pull/8), draft, retargeted to the A3 implementation branch; not merged.

- **Quality run #198**, ID `43157775745`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43157775745
  - Django system check: PASS
  - Django test suite: PASS — 74 tests
  - Ruff lint: PASS
  - Ruff format: PASS — 57 files already formatted
  - pip-audit: PASS — no known vulnerabilities found
- **Security monitor run #83**, ID `43157775696`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43157775696
  - Read-only OSV monitor job: PASS
  - The run remains a point-in-time query; it does not establish OSV SLA, live positive-advisory coverage, or notification delivery.

These workflows were triggered for the corrective PR with the source head above. The PR workflow validates the PR merge ref; this evidence is not described as a standalone push-triggered exact-head run.

## Corrective disposition

- A4-F01: **CORRECTED IN IMPLEMENTATION / A4 RE-VERIFICATION REQUIRED** — hard 63-second deadline claim removed; socket inactivity timeout and slow-stream limitation are explicit.
- A4-F02: **CORRECTED / DOCUMENT CHECK REQUIRED** — actual Markdown paragraph breaks restored.
- A4-F03: **CORRECTED / EVIDENCE REFERENCES UPDATED** — original A3 report now identifies A3 final head `a8042051824ddb50592492ee75d5aad24d1bb03a`, quality run #179 / ID `43130314519`, and security run #64 / ID `43130314540`, with matching URLs.
- A4-F04: **TESTS ADDED / CI PASS** — HTTP 429/5xx exhaustion asserts three total attempts and exactly two sleeps; OSV failure path asserts `main()` exit 2 and an INCOMPLETE summary.

**Overall A3 corrective implementation:** IMPLEMENTED — corrective CI PASS on the source head above.  
**A4 closure:** NOT YET VERIFIED; repeat independent A4 review is required.  
**Operational readiness:** NOT VERIFIED.  
**Production readiness:** NOT READY.  
**Merge, deployment, schedule activation, and A5:** NOT AUTHORIZED.
