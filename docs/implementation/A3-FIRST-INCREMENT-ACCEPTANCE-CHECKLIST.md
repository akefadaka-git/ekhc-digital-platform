# EKHC OS — A3 First-Increment File-Level Acceptance Checklist

**Status:** OWNER APPROVED — implementation authorized within this exact checklist  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Baseline:** Owner-approved Django/Python; Python 3.14.10 + Django 5.2.19; no database/schema; Django-native health/readiness endpoint only; Django test runner, Ruff, pip-audit; public GitHub Actions standard runners plus local fallback.

## 1. Scope boundary

This checklist defines only the first authority-independent technical foundation. The Owner approved this exact checklist on 2026-11-11; implementation is authorized only within the listed files and acceptance criteria.

- Preserve any existing UI; do not create, replace, or redesign UI.
- Synthetic data only; no live member, pastoral, child, governance, or financial data.
- No database server, ORM persistence, migrations, schema, models, or hidden substitute database.
- No authentication, authorization, role, office, hierarchy, membership, governance, approval, or records workflow.
- No general REST API; only a minimal non-sensitive health/readiness endpoint.
- No paid services, paid runners, billing activation, production credentials, deployment, signing, or publication.
- Do not modify `main`; work only on `a3/restricted-foundation-scope`.

## 2. Proposed file-level scope and acceptance criteria

| File | Purpose | Acceptance criteria |
|---|---|---|
| `.python-version` | Runtime declaration | Contains exactly the approved Python patch version; setup documentation agrees. |
| `requirements.txt` | Runtime dependency pins | Django is pinned to the approved 5.2.19 patch unless a newer compatible security patch is verified and recorded before implementation; no database driver or unapproved runtime package. |
| `requirements-dev.txt` | Direct development inputs | Includes the runtime requirements and exact reviewed pins for Ruff and pip-audit; acts as the reviewed direct-input set for lock generation. |
| `requirements-lock.txt` | Transitive dependency lock | Pins every resolved runtime/development package and lists SHA-256 hashes for all published files for each exact package version; installs successfully with pip `--require-hashes` on the approved Python 3.14.10 / Ubuntu 24.04 runner. |
| `manage.py` | Django command entry point | Uses the documented project settings module and runs without requiring a database service. |
| `config/__init__.py` | Project package marker | Present; no import-time side effects. |
| `config/settings.py` | Minimal settings and configuration validation | Reads environment configuration safely; rejects invalid required configuration; contains no secrets; disables unnecessary apps/middleware; no database configuration or persistence integration. |
| `config/urls.py` | Minimal URL routing | Exposes only the approved health/readiness route; no product/resource endpoints. |
| `config/wsgi.py` and `config/asgi.py` | Standard Django entry points | Import successfully using the pinned environment; no deployment configuration or credentials. |
| `health/__init__.py` | Health package marker | Present; no import-time side effects. |
| `health/views.py` | Health/readiness view | Returns a minimal status response; does not disclose settings, versions, environment variables, paths, secrets, personal data, or organizational data; does not query a database. |
| `tests/__init__.py` | Test package marker | Present. |
| `tests/test_health.py` | Health endpoint tests | Tests success response, expected content type/schema, and absence of sensitive/internal values; tests do not require network or database services. |
| `pyproject.toml` | Ruff configuration | Pins or constrains the approved Ruff behavior consistently with the dev dependency; deterministic lint and format checks. |
| `.github/workflows/quality.yml` | No-cost CI workflow | Pull-request and authorized-branch push triggers plus manual dispatch; standard public Linux runner only; least-privilege permissions; third-party actions pinned to immutable reviewed SHAs; setup uses exact Python patch; installs `requirements-lock.txt` with `--require-hashes`; runs Django tests, Ruff check, Ruff format check, and pip-audit against the same lock; no secrets, artifacts, deployment, release, or write permissions. |
| `README.md` | Developer setup and local fallback | Documents Python version, virtual environment, dependency install, test/lint/format/audit commands, scope restrictions, and no-cost local fallback. |

## 3. Required verification commands

Run from a clean environment after the files exist:

```bash
python --version
python -m pip install --require-hashes -r requirements-lock.txt
python manage.py check
python manage.py test
ruff check .
ruff format --check .
pip-audit -r requirements-lock.txt
```

Acceptance requires:
- Runtime reports the exact approved Python patch.
- Dependency installation is reproducible: every runtime/development and transitive package is pinned and hash-verified with pip `--require-hashes`; no database drivers or undeclared product dependencies are installed.
- Django system check and test suite complete successfully without a database service.
- Ruff lint and format checks pass.
- pip-audit completes; every finding is triaged and recorded. A clean audit is not security certification.
- The same checks run in the GitHub Actions workflow on a standard public runner.
- The workflow fails clearly if required source or dependency files are missing; it must not silently skip checks or produce a false green result.
- Exact CI run URL, commit SHA, command outputs/status, and dependency-audit summary are recorded.

## 4. Explicit exclusions

No UI source files, UI framework, design system, localization catalogue, calendar conversion, audit-event retention policy, database, schema, user model, authentication, authorization, organizational hierarchy, role catalogue, governance workflow, API resource endpoint, production settings, deployment workflow, secrets, or production data.

Any item in this exclusion list requires separate evidence, scope definition, and Owner approval.

## 5. Workflow preparation note

The approved CI approach is standard GitHub-hosted runners for the public repository, with local execution as fallback. The workflow file was authored after checklist approval and its third-party actions are pinned to immutable SHAs. Workflow evidence is recorded in Section 7.

## 6. Owner approval record

**Decision:** APPROVED on 2026-11-11.

**Approval scope:** Implement only the exact first-increment files and acceptance criteria in Section 2. All exclusions in Sections 1 and 4 remain binding. No merge, deployment, signing, publication, or production-data authorization is implied.

- Checklist: OWNER APPROVED.
- Executable implementation: AUTHORIZED within this checklist.
- CI workflow file: CREATED on the authorized A3 branch.
- A2: PARTIAL / OPEN.
- A4: IN PROGRESS. A5: NOT STARTED.
- Merge/deployment/signing/publication: NOT AUTHORIZED.

## 7. Implementation and verification record — 2026-11-11

**Implementation state:** ALL FIRST-INCREMENT FILES CREATED. The approved runtime, minimal health endpoint, test suite, lint/format checks, dependency audit, hash-locked dependency installation, and public-runner CI have passed. A3 closure recommendation is ready for Owner review; this document does not itself declare A3 closed.

Created on `a3/restricted-foundation-scope`:
- Runtime and direct dependency declarations: `.python-version`, `requirements.txt`, `requirements-dev.txt`.
- Transitive dependency lock: `requirements-lock.txt` — 32 exact package versions and 402 SHA-256 hashes covering the published release files for those versions.
- Django entry point/configuration: `manage.py`, `config/__init__.py`, `config/settings.py`, `config/urls.py`, `config/wsgi.py`, `config/asgi.py`.
- Minimal endpoint: `health/__init__.py`, `health/views.py`.
- Tests and lint configuration: `tests/__init__.py`, `tests/test_health.py`, `pyproject.toml`.
- CI and developer instructions: `.github/workflows/quality.yml`, `README.md` (existing README content preserved and updated to use the hash lock).

**A3 lock-integration verification evidence (historical):
- Workflow: **A3 quality checks**, run **#22**; commit `628dccda9d12fa78a29cecfe9520452f930b5df3`.
- Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42968364171

**Final A3 exact-head verification evidence:**
- Workflow: **A3 quality checks**, run **#26**; exact tested commit `bf3443b288bcc78d7479630ffa92f0af7c88cd77`.
- Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42968545687.
- All 10 job steps succeeded: required files, Python 3.14.10, hash-locked install, Django check, 3 tests, Ruff lint/format, and pip-audit. Audit: no known vulnerabilities found.
- Event: push on `a3/restricted-foundation-scope`.
- Overall workflow conclusion: **SUCCESS**.
- Required-file check, including `requirements-lock.txt`: PASS.
- Python 3.14.10 setup: PASS.
- `python -m pip install --require-hashes -r requirements-lock.txt`: PASS.
- Django system check: PASS.
- Django tests: PASS — 3 tests.
- Ruff lint: PASS.
- Ruff format check: PASS.
- `pip-audit -r requirements-lock.txt`: PASS — **No known vulnerabilities found** at the time of this run.
- Job conclusion: SUCCESS.

**Lock-generation method and boundaries:**
- Direct input pins remain in `requirements.txt` and `requirements-dev.txt`.
- The resolved dependency graph was obtained using pip's built-in `--dry-run --ignore-installed --report` on Python 3.14.10 / Ubuntu 24.04 x86_64.
- SHA-256 digests were read from PyPI release metadata for each exact resolved package version; all published release-file hashes were included in the lock.
- The generated lock was then installed using pip's `--require-hashes` and audited by the successful exact-head workflow.
- Regenerate and review the lock whenever a direct dependency or supported runtime/platform changes. The lock does not replace ongoing dependency updates or security review.

**Earlier failure and correction record:**
- Run #11 at `f84cfc81459091784dbcaf8309f20621f6e8a067` failed at Ruff import sorting.
- The CI diagnostic isolated one extra blank line between the import block and first module setting; it was corrected in `config/settings.py`.
- Run #18 verified the corrected code and all checks with direct pins.
- Run #20 successfully generated the dependency-lock preview.
- Run #22 verified the committed hash lock and all required checks.

**Acceptance disposition:**
- Required files: PRESENT.
- Python 3.14.10 setup: PASS.
- Hash-locked dependency installation: PASS.
- Django system check: PASS.
- Django tests: PASS — 3 tests.
- Ruff lint: PASS.
- Ruff format: PASS.
- pip-audit: PASS — no known vulnerabilities found in run #22.
- Exact-head GitHub Actions: PASS for the tested commit above.
- Dependency reproducibility: PASS for the approved Python 3.14.10 / Ubuntu 24.04 x86_64 CI environment; re-lock and re-verify when the approved runtime/platform or direct inputs change.
- A3 implementation acceptance: OWNER-ACCEPTED; A3 closure approved before A4 authorization.
- Independent A4 review: IN PROGRESS; see `A4-INDEPENDENT-VERIFICATION-RECORD.md`.
- A2 constitutional and organizational blockers: remain PARTIAL / OPEN.

**Closure record:** The Owner accepted A3 first-increment closure and separately authorized A4 independent verification. A4 is in progress; see `A4-INDEPENDENT-VERIFICATION-RECORD.md`. A3 acceptance does not authorize merge, deployment, signing, publication, production data, or any A2-dependent feature.
