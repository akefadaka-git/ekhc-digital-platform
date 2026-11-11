# EKHC OS — A4 Independent Verification Record

**Status:** VERIFIED — A4 closure recommendation ready for Owner review; formal A4 closure not yet accepted  
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

Run #37 verified the corrective implementation and the reconciled A3/A4 governance records at its tested commit. The final A4 record update was then committed as a documentation-only change. Run #38 below confirms the resulting final branch head.


### Final A4 corrective verification — run #37

- Workflow: **A3 quality checks**, run **#37**, ID `42969700818`.
- Tested commit: `6d2ccc1116d9c95955e36ccba9bc54724073ff95`.
- Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42969700818
- Workflow/job conclusion: **SUCCESS**; all 10 job steps completed successfully.
- Required-file check, Python 3.14.10 setup, and hash-locked dependency installation: PASS.
- Django system check: PASS.
- Django tests: PASS — **6 tests**, including all three fail-closed settings regression tests.
- Ruff lint: PASS; Ruff format: PASS (18 files already formatted).
- pip-audit: PASS — no known vulnerabilities found.

### Final record-head CI confirmation — run #38

- Workflow: **A3 quality checks**, run **#38**, ID `42969850685`.
- Exact tested branch head: `8b94f27ff84ad97e4adb38a2ddc8b723adc9c542`.
- Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42969850685
- Workflow/job conclusion: **SUCCESS**; all 10 job steps completed successfully.
- Required-file check: PASS.
- Python 3.14.10 setup and hash-locked dependency installation: PASS.
- Django system check: PASS.
- Django tests: PASS — **6 tests**.
- Ruff lint: PASS; Ruff format: PASS (18 files already formatted).
- pip-audit: PASS — no known vulnerabilities found.

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
- A4 corrective implementation: **VERIFIED; six tests, Ruff, and pip-audit passed on the final branch head in run #38**.
- A4 independent verification: **VERIFIED; closure recommendation READY FOR OWNER REVIEW; formal closure awaits Owner acceptance**.
- A2: **PARTIAL / OPEN**.
- A5: **NOT STARTED**.
- `main`: **MUST REMAIN UNCHANGED**.
- Merge, deployment, signing, publication, production data: **NOT AUTHORIZED**.

A4 verification is complete and its closure recommendation is ready for Owner review. This record does not itself close A4. A4 closure does not imply A2 closure, production readiness, or A5 authorization.
