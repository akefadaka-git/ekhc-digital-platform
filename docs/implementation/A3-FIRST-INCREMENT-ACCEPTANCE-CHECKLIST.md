# EKHC OS — A3 First-Increment File-Level Acceptance Checklist

**Status:** PREPARED — pending Owner approval before executable implementation  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Baseline:** Owner-approved Django/Python; Python 3.14.10 + Django 5.2.19; no database/schema; Django-native health/readiness endpoint only; Django test runner, Ruff, pip-audit; public GitHub Actions standard runners plus local fallback.

## 1. Scope boundary

This checklist defines only the first authority-independent technical foundation. It does not authorize implementation until the Owner approves this checklist.

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
| `requirements-dev.txt` | Development tool pins | Includes the runtime requirements and exact reviewed pins for Ruff and pip-audit; installation works in a clean Python 3.14.10 virtual environment. |
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
| `.github/workflows/quality.yml` | No-cost CI workflow | Pull-request and authorized-branch push triggers plus manual dispatch; standard public Linux runner only; least-privilege permissions; third-party actions pinned to immutable reviewed SHAs; setup uses exact Python patch; installs pinned requirements; runs Django tests, Ruff check, Ruff format check, and pip-audit; no secrets, artifacts, deployment, release, or write permissions. |
| `README.md` | Developer setup and local fallback | Documents Python version, virtual environment, dependency install, test/lint/format/audit commands, scope restrictions, and no-cost local fallback. |

## 3. Required verification commands

Run from a clean environment after the files exist:

```bash
python --version
python -m pip install -r requirements-dev.txt
python manage.py check
python manage.py test
ruff check .
ruff format --check .
pip-audit
```

Acceptance requires:
- Runtime reports the exact approved Python patch.
- Dependency installation is reproducible and does not install database drivers or undeclared product dependencies.
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

The approved CI approach is standard GitHub-hosted runners for the public repository, with local execution as fallback. The workflow file must be authored only after this checklist is approved and its action dependencies are reviewed and pinned to immutable SHAs. No workflow run or passing status is claimed at checklist-preparation time.

## 6. Approval gate

**Requested Owner decision:** Approve this exact file-level checklist for the first A3 implementation increment, or return it for revision.

Until approval:
- Checklist: PREPARED / NOT APPROVED.
- Executable implementation: NOT STARTED.
- CI workflow file: NOT CREATED.
- CI run: NOT RUN.
- A2: PARTIAL / OPEN.
- A4/A5: NOT STARTED.
- Merge/deployment/signing/publication: NOT AUTHORIZED.
