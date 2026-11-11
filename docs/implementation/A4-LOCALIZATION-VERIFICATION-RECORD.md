# EKHC OS — A4 Localization Foundation Verification Record

**Verification status:** TECHNICAL PASS — OWNER ACCEPTED / VERIFIED-CLOSED  
**Owner acceptance date:** 2026-11-11  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Implementation branch:** `a3/localization-foundation`  
**Implementation SHA:** `96198cad6b3e2731a7bfedf8511c2be85409c8bd`  
**Verification branch:** `a4/localization-verification`  
**A3 parent baseline:** `ebe25ab828812c9b0b76fc18423b66e3e6c31d37`

## 1. Verification scope

A4 reviewed the Amharic-first request-language negotiation increment, its integration with the existing minimal Django foundation, its regression tests, and its exact-head CI evidence.

This is a scoped technical verification. It is not a third-party penetration test, external security certification, institutional/legal approval, or production-readiness assessment.

## 2. Review findings and dispositions

| ID | Review area | Finding | Disposition |
|---|---|---|---|
| A4-LOC-01 | HTTP cache correctness | Responses depend on `Accept-Language`, but the original middleware did not declare the request-header variation to caches | FIXED — middleware now merges `Accept-Language` into `Vary` using Django's `patch_vary_headers` |
| A4-LOC-02 | Default behavior | Missing or unsupported preferences must resolve to the Amharic platform default | PASS — covered by tests |
| A4-LOC-03 | Language preference handling | Supported English, regional tags, quality ordering, zero quality, and invalid quality values require deterministic handling | PASS — covered by tests |
| A4-LOC-04 | Regression safety | Existing health endpoint and fail-closed settings must remain intact | PASS — existing tests pass |
| A4-LOC-05 | Scope control | No persistence, user identity, role/authority model, UI replacement, or invented institutional terminology may be introduced | PASS — reviewed changed-file diff contains only middleware and tests after the A3 baseline |

## 3. Corrective implementation

The A4 cache finding was corrected on the A3 implementation branch:

- `config/localization.py` now adds `Vary: Accept-Language` while preserving any existing `Vary` values.
- `tests/test_health.py` adds tests for regional language tags, invalid quality values, and the `Vary` response header.

The correction changed only two files. Comparison from the pre-correction implementation SHA `4fb63080236501aaaaae610f6cf73e2558f46555` to verified implementation SHA `96198cad6b3e2731a7bfedf8511c2be85409c8bd` reports two commits, two modified files, 18 additions, and no deletions.

## 4. Exact-head CI evidence

- Workflow: **A3 quality checks**
- Run: **#52**
- Run ID: `42985668861`
- Tested SHA: `96198cad6b3e2731a7bfedf8511c2be85409c8bd`
- Result: **SUCCESS**
- URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42985668861

Verified steps:

| Check | Result |
|---|---|
| Python 3.14.10 setup | PASS |
| Hash-locked dependency installation | PASS |
| Django system check | PASS |
| Django test suite | PASS — 14 tests |
| Ruff lint | PASS |
| Ruff format | PASS |
| pip-audit | PASS — no known vulnerabilities found |

## 5. Remaining limitations

1. This increment negotiates language metadata; it does not provide translated UI or product content.
2. Django's internal `LANGUAGE_CODE` remains English because the framework distribution used here does not include an Amharic translation catalogue. The platform language is exposed separately as `request.LANGUAGE_CODE` and `Content-Language`; this must not be misrepresented as activated Django Amharic translations.
3. No user preference persistence, account settings, cookie, session, or database behavior has been implemented.
4. No production reverse-proxy/CDN cache configuration or end-to-end deployment behavior has been tested.
5. No external third-party security reviewer or penetration test has been engaged.

These are explicit scope boundaries or later verification needs, not silently accepted production capabilities.

## 6. Governance and conclusion

**A4 technical conclusion: PASS for the restricted localization increment.**

**Owner acceptance: APPROVED.** The Owner explicitly approved A4 closure in the project conversation on 2026-11-11. This increment is therefore **VERIFIED-CLOSED** at A4 for its restricted technical scope.

The cache correctness finding was fixed and the final implementation head passed the complete existing quality workflow. The implementation remains isolated from `main`; no PR merge, deployment, signing, publication, or production-data access occurred.

This closure does not close A2, satisfy missing constitutional/bylaw/UI-provenance dependencies, or authorize A5. A5 remains **NOT STARTED** and separately gated.
