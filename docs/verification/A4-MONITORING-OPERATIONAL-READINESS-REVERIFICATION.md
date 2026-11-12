# EKHC OS — A4 Independent Re-verification Record: Monitoring Operational Readiness

**Verification date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Verified corrective source branch:** `a3/monitoring-operational-readiness-a4-corrections`  
**Corrective source SHA:** `1a3946284c819b7004d4a652a4bbcb02396f3389`  
**A3 implementation baseline:** `a8042051824ddb50592492ee75d5aad24d1bb03a`  
**A4 verification branch:** `a4/monitoring-operational-readiness-reverification`

## 1. A4 disposition

**A4 result: PARTIAL — FOUR CORRECTIVE FINDINGS RE-VERIFIED; FINAL-HEAD CI EVIDENCE GATE REMAINS OPEN.**

The independent source review confirms that the four prior findings have been addressed in the corrective source. The prior corrective CI runs passed on source SHA `35c6cad2bae0cf7dd7400b3605e315f71c476f4b`. A direct comparison from that tested source SHA to the corrective source SHA above reports exactly two commits ahead and one changed path: the corrective implementation evidence record. The security-monitor Python source and test source are byte-for-byte identical at those two SHAs. The corrected runbook and A3 implementation report are included in the final corrective source.

The final corrective source SHA itself has no associated workflow runs or combined status checks returned by the available GitHub evidence interface. Therefore this record does not claim final-head CI. The prior CI is strong evidence for the unchanged code/tests, but it does not satisfy a strict final-head workflow-evidence gate.

## 2. Re-verification of A4 findings

| Finding | Independent check | Result |
|---|---|---|
| A4-F01 — OSV wall-clock bound | Inspected `query_osv`: maximum three attempts; 20-second urllib socket-inactivity timeout per attempt; bounded 1s/2s sleeps; no hard total wall-clock deadline. Runbook explicitly states a continuously streaming response can exceed 20 seconds and total elapsed time can exceed 63 seconds. | **CORRECTED — PASS WITH EXPLICIT LIMITATION** |
| A4-F02 — literal newline rendering | Inspected corrected monitoring runbook. The retry-budget paragraph is followed by real Markdown paragraph breaks; literal backslash-n sequence is absent. | **CORRECTED — PASS** |
| A4-F03 — evidence integrity | Inspected A3 report: it identifies A3 final head `a8042051824ddb50592492ee75d5aad24d1bb03a`, quality run #179 / ID `43130314519`, and monitor run #64 / ID `43130314540`. The corrective record identifies source SHA `35c6cad2bae0cf7dd7400b3605e315f71c476f4b`, quality run #198 / ID `43157775745`, and monitor run #83 / ID `43157775696`; links and run IDs agree. The corrective record accurately explains that those runs were triggered while PR #8 targeted main and are not standalone exact-head runs. | **CORRECTED — PASS** |
| A4-F04 — failure-path tests | Inspected tests for HTTP 429/5xx exhaustion (three attempts, two sleeps) and `main()` OSV failure (exit 2 and INCOMPLETE summary). Both tests are present. Quality run #198 reports 74 tests passed and successful Ruff lint/format and pip-audit. | **CORRECTED — PASS; FINAL-HEAD CI PENDING** |

## 3. Corrective CI evidence inspected

- Quality workflow #198, run ID `43157775745`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43157775745
  - Django system check: PASS
  - Django tests: PASS — 74 tests
  - Ruff lint: PASS
  - Ruff format: PASS — 57 files already formatted
  - pip-audit: PASS — no known vulnerabilities found
- Security monitor workflow #83, run ID `43157775696`, SUCCESS: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43157775696
  - 32 locked PyPI packages queried
  - 0 OSV advisories returned
  - 0 approved exception reminders/expiries; committed register remains empty

The successful OSV query is a point-in-time result, not proof of a live positive advisory, OSV SLA, or notification delivery. Synthetic positive-advisory behavior remains mocked test coverage.

## 4. Branch and repository integrity

- Corrective branch versus original A3 branch: 13 commits ahead, 0 behind; five changed paths.
- Corrective source SHA `1a3946284c819b7004d4a652a4bbcb02396f3389` versus CI-tested corrective source SHA `35c6cad2bae0cf7dd7400b3605e315f71c476f4b`: two commits ahead, 0 behind; only `docs/implementation/A3C-A4-FINDINGS-CORRECTIVE-IMPLEMENTATION-RECORD.md` changed.
- `scripts/security_monitor.py` and `tests/test_security_monitor.py` are identical at the CI-tested and final corrective source SHAs.
- Main observed at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`; no merge or default-branch integration performed by this verification.
- PR #8 remains the corrective PR; it has not been merged.
- Temporary validation PR #9 was closed unmerged after discovering it would present 62 files / 225 commits relative to main; it is not used as verification evidence.
- The accepted prior A4 verification branch/record was not changed by this review.

## 5. Operational and production gates remain open

The following remain NOT VERIFIED or NOT RUN: external notification channel and recipient identities; human acknowledgement; responder/backup/holiday coverage; restricted exception-record custody; controlled human-response rehearsal; real approved exception reminder; live positive OSV advisory; OSV service SLA/rate-limit guarantees. The scheduled workflow remains inactive off the default branch.

## 6. Required next action

Obtain fresh successful Quality and Security Monitor workflow runs on the final corrective branch head `1a3946284c819b7004d4a652a4bbcb02396f3389` (or on a validation commit whose code and test tree is demonstrably identical and whose evidence provenance is explicit), then update this A4 record with the run IDs and job outcomes.

**A4 closure:** NOT CLOSED — final-head CI evidence gate open.  
**Operational readiness:** NOT VERIFIED.  
**Production readiness:** NOT READY.  
**Merge, deployment, default-branch integration, schedule activation, and A5:** NOT AUTHORIZED.
