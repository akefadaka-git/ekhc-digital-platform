# EKHC OS — A3 Automated Advisory Monitoring and Exception-Expiry Implementation Report

**Status:** IMPLEMENTED — A3 evidence recorded; exact-head CI and A4 verification remain pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/automated-security-advisory-monitoring`  
**A3 implementation code head:** `585555868fc3fcea8a925cd8148e9b859401f122`  
**Base:** `974ca3c05af5cb024ee7ed45e099a9461a9a69b8` — Owner-accepted A4 vulnerability-governance closure

## 1. Scope delivered

The implementation adds read-only daily advisory matching for the exact PyPI name/version pairs in `requirements-lock.txt`, using the public OSV batch API, and expiry signals for explicitly APPROVED exceptions in a minimal non-sensitive metadata register.

The exception reminder thresholds are 30, 14, 7, 3, and 1 days, the expiry date, and overdue dates. The monitor does not change the exception status or make a risk decision.

## 2. Exact change set

GitHub compare from the A3 base to implementation code head: **18 commits ahead, 0 behind; exactly 7 files changed**.

| File | Change |
|---|---|
| `.github/workflows/security-monitor.yml` | New daily scheduled, manual, A3-push and PR monitor workflow |
| `.github/workflows/quality.yml` | Required-file gate includes the new monitor module, register, and regression tests |
| `scripts/security_monitor.py` | Standard-library-only lock parser, OSV batch query, exception metadata validation, expiry evaluation and safe job summary |
| `scripts/__init__.py` | Python package marker |
| `tests/test_security_monitor.py` | Seven unit tests for lock parsing, duplicate/unpinned entries, UTC validation, expiry status/thresholds, duplicate IDs, and advisory-text escaping |
| `docs/security/exception-register.json` | Empty, non-sensitive metadata register (`exceptions: []`) |
| `docs/security/AUTOMATED-ADVISORY-MONITORING-AND-EXCEPTION-EXPIRY.md` | Operating model, cadence, confidentiality, limitations and acceptance criteria |

The lockfile was inspected: 32 non-comment entries, all matched the supported pinned PyPI requirement syntax. No lockfile or dependency manifest was changed.

## 3. Security and behavior boundaries

- Workflow and job permissions are `contents: read` only.
- Checkout action credentials are not persisted.
- GitHub Actions used are pinned to full commit SHAs already present in the repository's quality workflow.
- No repository write, issue, pull-request, deployment, package, OIDC, artifact-upload, or attestation permission was added.
- No runtime or development dependency, lockfile, application source, Django settings, route, migration, database, or production behavior changed.
- The monitor makes no severity determination and does not create or update advisories, issues, exceptions, or dependencies.
- Full exception records and sensitive evidence remain outside this public repository. Only non-sensitive metadata may be placed in the committed register.
- Advisory text is escaped before inclusion in the Markdown job summary.
- Invalid lock/register/API responses fail closed as INCOMPLETE; matching advisories or due/overdue exceptions return a non-zero job result.

## 4. Verification evidence and limitations

| Check | Result |
|---|---|
| GitHub base-to-head scope comparison | PASS — 7 files, no unrelated application files |
| Lockfile syntax coverage | PASS — 32/32 entries match pinned PyPI format |
| Read-only workflow permission inspection | PASS — `contents: read` only at workflow and job |
| Action pin inspection | PASS — full 40-character SHAs |
| Unit test suite authored | PASS — 7 focused tests present |
| Exact-head CI run/result | **NOT CONFIRMED** |
| Live OSV API query | **NOT RUN / NOT CONFIRMED** |
| GitHub email/mobile notification delivery | **NOT VERIFIED** |
| Scheduled execution on default branch | **NOT ACTIVE until separately merged to default branch** |
| Real exception reminder exercise | **NOT RUN — committed register is empty** |
| A4 independent verification | **NOT RUN** |

The available workflow-run lookup used for this report exposes only pull-request-triggered runs and returned no associated run for this push head. This is insufficient to conclude that GitHub Actions did not run; neither success, failure, nor cancellation is inferred. Exact-head CI therefore remains NOT CONFIRMED.

The schedule is daily at 06:15 UTC, but GitHub scheduled workflows execute only from the default branch. The branch can be tested by push or manual dispatch; scheduled monitoring will not become active until a separately approved merge to the default branch. A non-zero workflow result provides a GitHub Actions failure signal, but email/mobile delivery depends on repository/user notification settings and is not guaranteed or verified here.

## 5. Phase disposition

- A3 implementation: **IMPLEMENTED — PARTIAL pending exact-head CI evidence**.
- A4 independent verification: **NOT RUN**.
- A5 merge/deployment: **NOT AUTHORIZED**.
- Main: verified unchanged at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.

No merge, deployment, dependency update, exception approval, risk acceptance, exception-status mutation, artifact publication, signing, or protected-data access occurred.

## 6. Immediate next step

Obtain exact-head CI evidence for both the existing quality workflow and the new security-monitor workflow, including the live OSV API result; then conduct independent A4 review of permissions, parser/API failure handling, reminder semantics, and notification limitations. Keep the schedule inactive on the default branch until a separate merge approval is granted.
