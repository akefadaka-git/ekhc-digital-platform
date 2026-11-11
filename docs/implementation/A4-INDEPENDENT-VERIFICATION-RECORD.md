# EKHC OS — A4 Independent Verification Record

**Status:** IN PROGRESS — corrective increment committed; A4 exact-head CI evidence verified on commit `48e6da85d4cc32a3d8da654d5cb2beca64377e31`  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Working branch:** `a3/restricted-foundation-scope`  
**A3 accepted implementation baseline:** `bf3443b288bcc78d7479630ffa92f0af7c88cd77`  
**A3 Owner decision:** A3 first-increment closure accepted; A4 independent verification authorized.

## 1. Verification boundary

A4 verifies only the Owner-accepted restricted A3 foundation and its acceptance evidence. It does not expand product scope or resolve A2 constitutional, institutional, UI-provenance, legal, privacy, or stakeholder dependencies.

No changes to `main`, merge, deployment, signing, publication, production data, or A5 activity are authorized by this A4 work.

## 2. Independent baseline findings

The A4 review inspected the branch tree, file-level implementation, workflow definition, commit comparison, and the completed job logs for the prior final-head run.

- The A3 baseline branch was 51 commits ahead of `main` and 0 behind; its merge base was `main` at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.
- The restricted implementation consisted of 20 changed paths at the A3 baseline.
- Runtime and dependencies: Python 3.14.10, Django 5.2.19, Ruff 0.17.4, pip-audit 2.10.1; 32 exact dependency versions and 402 SHA-256 hashes in `requirements-lock.txt`.
- Workflow: standard `ubuntu-24.04` runner, read-only contents permissions, checkout/setup actions pinned to immutable commit SHAs, `persist-credentials: false`, hash-locked installation, Django check/tests, Ruff lint/format, and pip-audit.
- The prior final-head workflow was **A3 quality checks run #26**, ID `42968545687`, tested commit `bf3443b288bcc78d7479630ffa92f0af7c88cd77`. All 10 job steps completed successfully. Logs showed 3 tests passing, Ruff checks passing, and pip-audit reporting “No known vulnerabilities found”.
- Earlier run #22 remains valid historical evidence for the lock-file integration at its own commit, but it is not the final-head evidence for the A3 baseline. Run #26 superseded it for that baseline.

Run #26: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42968545687

## 3. A4 findings and corrective actions

### A4-F01 — historical CI evidence was described as current exact-head evidence

**Finding:** Several A3 records highlighted run #22 and commit `628dccda9d12fa78a29cecfe9520452f930b5df3`. That run passed, but the branch subsequently advanced.

**Disposition:** Reconciled here. The authoritative A3 final-head evidence is run #26 at `bf3443b288bcc78d7479630ffa92f0af7c88cd77`. Run #22 is retained as historical lock-integration evidence, not the final-head run.

### A4-F02 — README stage status was stale

**Finding:** README described A3 as under implementation and A4 as not started, despite Owner acceptance of A3 and authorization of A4.

**Disposition:** Corrected. README now identifies A3 as Owner-accepted, A4 as in progress, and A5 as not started. It links this A4 record and preserves A2 as PARTIAL / OPEN.

### A4-F03 — fail-closed configuration branches lacked regression tests

**Finding:** `config/settings.py` rejects missing `DJANGO_SECRET_KEY`, empty `DJANGO_ALLOWED_HOSTS`, and wildcard hosts, but the existing tests did not exercise these rejection paths.

**Disposition:** Corrective tests added in `tests/test_health.py`. They launch an isolated Python subprocess for each invalid configuration and assert that importing settings fails with the expected configuration error. Cases cover:
- Missing secret key.
- Empty allowed-host list.
- Wildcard allowed-host list.

These tests do not require a database, network access, live data, or new runtime dependencies.

## 4. Corrective change inventory

The A4 corrective increment is limited to:
- `tests/test_health.py` — three negative configuration regression tests and a small subprocess helper.
- `README.md` — corrected stage status and A4 record reference.
- `docs/implementation/A4-INDEPENDENT-VERIFICATION-RECORD.md` — this verification record.

No product endpoint, schema, persistence, identity, role, authority, hierarchy, governance workflow, UI, or external integration is added.

## 5. Required final exact-head verification

A4 corrective verification is accepted only after a successful GitHub Actions run on the final corrective branch head, with all of the following:
- Required-file check: PASS.
- Python 3.14.10 setup: PASS.
- `python -m pip install --require-hashes -r requirements-lock.txt`: PASS.
- `python manage.py check`: PASS.
- `python manage.py test`: PASS, including the three new fail-closed configuration tests.
- `ruff check .`: PASS.
- `ruff format --check .`: PASS.
- `pip-audit -r requirements-lock.txt`: PASS; findings, if any, must be triaged and recorded.
- Workflow conclusion: SUCCESS.
- Run URL and exact tested SHA recorded below.

### Final corrective CI evidence — first A4 verification head

- Workflow: **A3 quality checks**, run **#29**, ID `42969284013`.
- Tested commit: `48e6da85d4cc32a3d8da654d5cb2beca64377e31`.
- Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42969284013
- Workflow/job conclusion: **SUCCESS**; all 10 job steps completed successfully.
- Python 3.14.10 setup and hash-locked installation: PASS.
- Django system check: PASS.
- Django tests: PASS — **6 tests**, including all three new fail-closed settings regression tests.
- Ruff lint: PASS; Ruff format: PASS (18 files already formatted).
- pip-audit: PASS — no known vulnerabilities found.

This run verified the corrective implementation and A4 record at its tested commit. The subsequent governance-record reconciliation is documentation-only and requires its own exact-head CI confirmation before A4 closure.

## 6. A2 blockers retained

The following remain outside A4 and continue to block broader product acceptance:
- Authoritative seventh-edition Constitution.
- Current bylaws and amendments.
- Authoritative hierarchy and office mandates.
- Existing UI provenance and integration requirements.
- Stakeholder and requirements validation.
- Qualified legal/institutional review.
- Privacy and safeguarding review.
- Broader product/requirements technical acceptance.

No unsupported organizational relationship, office mandate, role, permission, or governance workflow is inferred or implemented.

## 7. Current disposition

- A3 first-increment closure: **OWNER-ACCEPTED**.
- A4 corrective implementation: **COMMITTED; corrective code and initial A4 record CI verified by run #29; final governance-head confirmation pending**.
- A4 independent verification: **IN PROGRESS; NOT CLOSED**.
- A2: **PARTIAL / OPEN**.
- A5: **NOT STARTED**.
- `main`: **MUST REMAIN UNCHANGED**.
- Merge, deployment, signing, publication, production data: **NOT AUTHORIZED**.

A4 closure recommendation may be prepared only after final exact-head CI succeeds and the resulting branch/file inventory is reconciled. A4 closure does not imply A2 closure, production readiness, or A5 authorization.
