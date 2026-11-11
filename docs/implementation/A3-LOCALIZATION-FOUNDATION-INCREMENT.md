# EKHC OS — A3 Localization Foundation Increment

**Status:** IMPLEMENTED — exact-head verification pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/localization-foundation`  
**Parent baseline:** `ebe25ab828812c9b0b76fc18423b66e3e6c31d37`

## 1. Purpose

Establish a small, authority-independent localization foundation while institutional documents and the original UI source remain pending. This increment implements request-scoped language negotiation only; it does not recreate, replace, or modify an existing UI.

## 2. Implemented behavior

- Amharic (`am`) is the default language.
- English (`en`) is supported when requested through the standard `Accept-Language` header.
- Unsupported language preferences fall back to Amharic.
- Django's built-in `LocaleMiddleware` performs request-scoped negotiation.
- The selected language is not persisted to an account, session, cookie, database, or profile by this increment.

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

- `config/settings.py` — Amharic default, supported Amharic/English language list, and locale middleware.
- `tests/test_health.py` — tests for default Amharic, English selection, and unsupported-language fallback.
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
| LOC-04 | Existing health response remains minimal and non-sensitive | Existing health tests |
| LOC-05 | No database, persistence, UI, translation catalogue, or institutional authority model is introduced | Change review |
| LOC-06 | Exact-head Django checks/tests, Ruff, and dependency audit pass | GitHub Actions |

## 6. Verification and governance

Exact-head CI evidence will be added after the workflow completes. This increment remains on its own A3 branch. The accepted prior A3/A4 baseline remains unchanged; `main` remains unchanged. A4 verification for this increment is not yet claimed. A2 remains PARTIAL / OPEN. A5, merge, deployment, signing, and publication remain separately gated.
