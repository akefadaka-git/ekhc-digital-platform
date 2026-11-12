# EKHC OS — A4 Independent Re-verification and Technical Closure Record: Monitoring Operational Readiness

**Verification date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Corrective source branch:** `a3/monitoring-operational-readiness-a4-corrections`  
**Final validation head:** `0a845253fda11614828b71eb78446e062e394c1f`  
**Pre-validation corrective head:** `1a3946284c819b7004d4a652a4bbcb02396f3389`  
**Source tree SHA (identical at both heads):** `627b50edd588d7a163111e41acba02493b6c203e`  
**A3 implementation baseline:** `a8042051824ddb50592492ee75d5aad24d1bb03a`  
**A4 verification branch:** `a4/monitoring-operational-readiness-reverification`

## 1. A4 disposition

**A4 TECHNICAL VERIFICATION: VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS.**

All four A4 corrective findings have been independently re-verified, and both required GitHub Actions workflows have now completed successfully on validation head `0a845253fda11614828b71eb78446e062e394c1f`. The validation commit has the exact same Git tree as pre-validation corrective head `1a3946284c819b7004d4a652a4bbcb02396f3389`; comparison reports one commit ahead, zero behind, and zero changed files. Thus the validation commit changes no source, tests, workflow, or documentation file and provides final-tree CI evidence without altering the tested implementation.

The technical verification is closed only for the documented, read-only advisory and exception-expiry monitoring scope and its stated limitations. This does **not** close operational readiness or production readiness.

## 2. Re-verification of A4 findings

| Finding | Independent check | Final result |
|---|---|---|
| A4-F01 — OSV wall-clock bound | Maximum three attempts; 20-second urllib socket-inactivity timeout per attempt; bounded 1s/2s sleeps. No hard total wall-clock deadline is implemented. Runbook explicitly states a continuously streaming response can exceed 20 seconds and total elapsed time can exceed 63 seconds. | **CORRECTED — PASS WITH EXPLICIT LIMITATION** |
| A4-F02 — literal newline rendering | Corrected monitoring runbook uses real Markdown paragraph breaks; literal backslash-n sequence is absent. | **CORRECTED — PASS** |
| A4-F03 — evidence integrity | A3 report identifies A3 final head `a8042051824ddb50592492ee75d5aad24d1bb03a`, quality run #179 / ID `43130314519`, and monitor run #64 / ID `43130314540`. Corrective record identifies tested source SHA `35c6cad2bae0cf7dd7400b3605e315f71c476f4b`, quality run #198 / ID `43157775745`, and monitor run #83 / ID `43157775696`, with the PR merge-ref provenance qualification. | **CORRECTED — PASS** |
| A4-F04 — failure-path tests | Tests cover HTTP 429/5xx exhaustion (exactly three attempts and two sleeps) and `main()` OSV failure (exit 2 and INCOMPLETE summary). The tests are included in the identical validation tree and were exercised by the successful exact-tree Quality workflow. | **CORRECTED — PASS** |

## 3. Exact-tree CI evidence

Both workflows were triggered by a push to the corrective branch and completed on exact head `0a845253fda11614828b71eb78446e062e394c1f`.

- **Quality workflow #203**, run ID `43191960075`, **SUCCESS**: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43191960075
  - Required-file gate: PASS
  - Approved Python setup and pinned dependency installation: PASS
  - Django system check: PASS
  - Django tests: PASS
  - Ruff lint: PASS
  - Ruff format check: PASS
  - pip-audit dependency vulnerability audit: PASS
- **Security monitor workflow #88**, run ID `43191960042`, **SUCCESS**: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43191960042
  - Read-only OSV advisory and exception-expiry monitor job: PASS

The exact-head check-runs endpoint reports both checks completed with conclusion `success`. The prior corrective CI runs #198/#83 remain supplementary evidence; the final-tree runs #203/#88 now satisfy the previously open exact-head CI gate.

## 4. Corrective source and branch integrity

- Validation commit: `0a845253fda11614828b71eb78446e062e394c1f`.
- Parent: `1a3946284c819b7004d4a652a4bbcb02396f3389`.
- Tree SHA is identical at parent and validation commit: `627b50edd588d7a163111e41acba02493b6c203e`.
- Commit comparison: one commit ahead, zero behind, zero changed files.
- Corrective branch remains separate from original A3 implementation branch.
- PR #8 remains open and draft, targeting `a3/monitoring-operational-readiness`; it has not been merged.
- Main remains outside this A4 verification action; no default-branch integration was performed.
- No merge, deployment, publication, signing, production-data access, scheduled activation, or A5 action was performed.

## 5. Explicit technical and operational limitations

The following limitations remain binding and are not waived by A4 technical closure:

1. **No hard total OSV wall-clock deadline.** The 20-second urllib timeout is a socket inactivity timeout for each attempt, not a strict cap on the entire response/read. A continuously streaming response can exceed 20 seconds; total elapsed time can exceed the nominal 63-second budget. Retry behavior remains a maximum of three total attempts with 1s/2s bounded backoff for transient transport failures and HTTP 429/5xx only.
2. **No guaranteed out-of-band notification.** Output remains GitHub workflow summary/stdout. No external notification channel or recipient identities have been established.
3. **No human acknowledgement or response coverage verification.** Responder, backup, holiday coverage, escalation ownership, and acknowledgement evidence remain NOT VERIFIED.
4. **No restricted exception-record custody verification.** Access and custody controls for exception records remain NOT VERIFIED.
5. **No controlled human-response rehearsal.** NOT RUN.
6. **No real approved exception reminder demonstrated.** The committed exception register is empty; zero exception reminders/expiries in the workflow is not proof of positive expiry handling against a real approved record.
7. **No live positive OSV advisory observed.** Positive-advisory behavior is covered by synthetic/mocked tests only.
8. **No OSV service SLA, rate-limit guarantee, or uninterrupted network-path guarantee established.**
9. **Scheduled workflow remains inactive off the default branch.** No schedule activation is authorized or implied.

A successful workflow run is evidence that the configured job completed; it is not proof of human acknowledgement, external notification delivery, institutional response readiness, or production operational coverage.

## 6. Closure boundary and remaining status

- **A4 technical verification:** **VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS**.
- **A4-F01 through A4-F04:** **PASS**, with the F01 timeout limitation preserved.
- **Operational readiness:** **NOT VERIFIED**.
- **Production readiness:** **NOT READY**.
- **External notification / responder coverage / custody / rehearsal:** **UNRESOLVED or NOT RUN**, as itemized above.
- **Merge PR #8 / default-branch integration:** **NOT AUTHORIZED**.
- **Deployment / publication / signing / production operation:** **NOT AUTHORIZED**.
- **Scheduled workflow activation:** **NOT AUTHORIZED**.
- **A5:** **NOT AUTHORIZED**.

A4 technical closure does not imply approval of any of these separate actions. Further work must remain within a separately approved scope and must preserve the limitations above.
