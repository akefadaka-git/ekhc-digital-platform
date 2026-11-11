# EKHC OS — A3 Localization Foundation Increment

**Status:** IMPLEMENTED — corrective exact-head verification pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/localization-foundation`  
**Parent baseline:** `ebe25ab828812c9b0b76fc18423b66e3e6c31d37`

## 1. Purpose

Establish a small, authority-independent localization foundation while institutional documents and the original UI source remain pending. This increment implements request-scoped language negotiation only; it does not recreate, replace, or modify an existing UI.

## 2. Implemented behavior

- Amharic (`am`) is the platform default.
- English (`en`) is supported when requested through the standard `Accept-Language` header.
- Regional tags such as `en-US` and `am-ET` are reduced to their supported primary language.
- Quality weights are respected; zero-quality and unsupported languages are ignored.
- Unsupported or absent preferences fall back to Amharic.
- The middleware sets `request.LANGUAGE_CODE` and the response `Content-Language` header.
- Selection is request-scoped and is not persisted to an account, session, cookie, database, or profile.

Django's own `LANGUAGE_CODE` remains `en` for its internal translation fallback because Django 5.2.19 does not ship an Amharic translation catalogue. The platform middleware deliberately separates platform language negotiation from Django's catalogue-based translation machinery. No translated UI copy is claimed.

## 3. Explicit boundaries

This increment does not:
- Add or choose a database, ORM, migration, schema, or persistence layer.
- Add authentication, accounts, roles, permissions, or institutional authority.
- Create translations, message catalogues, official terminology, or institutional labels.
- Add or replace frontend/UI files.
- Modify the existing UI or claim that the original UI provenance has been resolved.
- Introduce production data, external integrations, paid dependencies, deployment, signing, or publication.

Amharic-first behavior is a platform default, not a substitute for Owner-approved translations or authoritative EKHC terminology.

## 4. Changed paths

- `config/localization.py` — dependency-free, request-scoped language negotiation middleware.
- `config/settings.py` — Amharic platform default, supported platform language list, and middleware registration.
- `tests/test_health.py` — default, English, unsupported fallback, quality-order, and zero-quality regression tests.
- `.github/workflows/quality.yml` — run the existing read-only quality workflow for A3 implementation branches.
- `README.md` — current incremental implementation and verification status.
- This record.

No dependency or lockfile changes are required.

## 5. Acceptance criteria

| ID | Acceptance criterion | Verification |
|---|---|---|
| LOC-01 | Requests without a language preference resolve to Amharic | Automated test |
| LOC-02 | Supported English preference resolves to English | Automated test |
| LOC-03 | Unsupported preference falls back to Amharic | Automated test |
| LOC-04 | Quality weights are respected and q=0 is ignored | Automated tests |
| LOC-05 | Existing health response remains minimal and non-sensitive | Existing health tests |
| LOC-06 | No database, persistence, UI, translation catalogue, or institutional authority model is introduced | Change review |
| LOC-07 | Exact-head Django checks/tests, Ruff, and dependency audit pass | GitHub Actions |

## 6. Verification and governance

Initial run #41 failed at Django system checks because the framework's built-in locale catalogue does not include Amharic. The implementation was corrected to use a dedicated platform negotiation middleware rather than falsely treating Amharic as a Django translation catalogue. Corrective exact-head CI evidence will be added after the workflow completes.

This increment remains on its own A3 branch. The accepted prior A3/A4 baseline remains unchanged; `main` remains unchanged. A4 verification for this increment is not yet claimed. A2 remains PARTIAL / OPEN. A5, merge, deployment, signing, and publication remain separately gated.


Corrective implementation commit: `2fb8e5d07afc7b0db90c7e484e9e1c7253f9c83d`. The failed initial check is retained above as evidence of the catalogue compatibility issue and its resolution.

Formatting correction: Ruff's exact formatting changes were applied to `config/localization.py` and `tests/test_health.py` after run #42 identified those two style-only issues. The next exact-head workflow must verify the corrected tree.
