# EKHC OS — A4 Runtime Secret and Host Configuration Hardening Verification Record

**Verification status:** TECHNICAL PASS — Owner acceptance pending  
**Date:** 2026-11-11  
**Repository:** akefadaka-git/ekhc-digital-platform  
**Implementation branch:** a3/runtime-security-hardening  
**Implementation SHA tested by CI:** 5c5e347fbb6a74d9ae226fbb38f1f5093c073e0b  
**Verification branch:** a4/runtime-security-hardening-verification  
**A3 base:** bb082a8705db011f3ae83320fe72fed13da7d246  
**Main SHA observed during verification:** adfa62eccda93c8b261e5abd3cbdb22cf28c8823

## 1. Verification scope and change inventory

A4 independently reviewed the A3 diff from the Owner-accepted security/deployment A4 baseline. The comparison reports eight commits ahead, zero behind, and exactly five changed files:

| File | Change |
|---|---|
| `.github/workflows/quality.yml` | Required-file gate includes runtime validator and its tests |
| `config/runtime.py` | New startup validation for secrets and explicit host entries |
| `config/settings.py` | Uses the centralized runtime validation result |
| `tests/test_runtime.py` | New runtime secret and host regression coverage |
| `docs/implementation/A3-RUNTIME-SECRET-HOST-HARDENING.md` | A3 scope and operational boundaries |

No application routes, health behavior, localization, observability, identity, authorization, institutional hierarchy, database, migration, or production-data files changed.

## 2. Verification findings

| ID | Review area | Disposition |
|---|---|---|
| A4-RSH-01 | Required runtime secret | PASS — missing secret fails startup; the exception message does not echo the supplied secret |
| A4-RSH-02 | Production secret floor | PASS — production rejects fewer than 50 characters, internal whitespace, and explicit placeholder markers |
| A4-RSH-03 | Allowed-host parsing | PASS — explicit DNS names, IP addresses, and leading-dot subdomain patterns accepted; wildcard, malformed URL/port/path, whitespace, empty entries, and case-insensitive duplicates rejected |
| A4-RSH-04 | Existing settings compatibility | PASS — local development defaults remain; DEBUG remains false; security/deployment settings remain loaded and unchanged in behavior |
| A4-RSH-05 | Regression and scope control | PASS — all 42 Django tests pass; existing wildcard-host error wording is preserved; no unrelated product or institutional functionality added |
| A4-RSH-06 | CI enforcement | PASS — required-file gate includes both new files and all quality steps passed on the exact implementation SHA |

## 3. Exact-head CI evidence

- Workflow: A3 quality checks
- Run: #90
- Run ID: 43053231878
- Tested SHA: 5c5e347fbb6a74d9ae226fbb38f1f5093c073e0b
- Result: SUCCESS
- URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43053231878

All workflow steps passed:

| Check | Result |
|---|---|
| Required-file gate | PASS |
| Python 3.14.10 setup | PASS |
| Hash-locked dependency installation | PASS |
| Django system check | PASS |
| Django test suite | PASS — 42 tests |
| Ruff lint | PASS |
| Ruff format | PASS |
| pip-audit | PASS |

An earlier exact-head attempt failed because the new wildcard parser changed an existing settings-import error message. The implementation was corrected to preserve the established error contract, the new regression test was aligned to the explicit wildcard error, and run #90 is the final passing exact-head evidence. The failed run is not counted as passing evidence.

## 4. Security limitations and operational notes

- The 50-character minimum is only a configuration floor, not proof of cryptographic entropy. Operators must generate a high-entropy secret and inject it through a protected secret manager or equivalent environment mechanism.
- No production secret, hostname, certificate, TLS topology, proxy, or deployment environment was supplied or tested.
- The previously verified direct-TLS contract remains unchanged. Forwarded proxy headers remain untrusted; reverse-proxy TLS termination is not enabled.
- This increment does not establish CSP, CORS, CSRF trusted origins, authentication, session flows, role/permission controls, external security review, or production readiness.
- Hostname parsing is intentionally conservative; internationalized domain names should be supplied in ASCII IDNA form after environment-specific review.
- No merge, deployment, signing, publication, or production-data access occurred.

## 5. Governance and conclusion

**A4 technical conclusion: PASS for the restricted runtime secret and allowed-host configuration increment.**

The final implementation SHA passed exact-head CI, including 42 tests, Django system check, Ruff lint/format, and dependency audit. The implementation remains isolated on its A3 branch. The A4 verification record is prepared for Owner acceptance; it is not yet marked VERIFIED-CLOSED.

This verification does not close A2, resolve institutional authority/provenance blockers, or authorize A5. A5 remains NOT STARTED and separately gated.
