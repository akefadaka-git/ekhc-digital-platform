# EKHC OS — A3 Restricted Foundation Scope and Authorization Record

**Status:** OWNER-AUTHORIZED SCOPE; restricted first-increment implementation and exact-head hash-locked CI verified; A3 closure awaits Owner review  
**Authorization date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Base:** `main` at `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`

## 1. Owner decision

On 2026-11-11, the Owner answered “yes” to the proposed restricted A3 basis: implement only components that do not depend on unresolved constitutional or organizational authority.

This authorization is narrow. It does not approve the constitutional hierarchy, office mandates, parent-child relationships, roles, permissions, authority scopes, or workflows derived from those matters.

## 2. Preserved stage and repository boundaries

- A1 remains OWNER APPROVED.
- A2 remains PARTIAL / OPEN. This record does not declare A2 closed or represent that its formal roadmap exit condition has been met.
- A3 restricted scope is OWNER-AUTHORIZED. The approved technical baseline and file-level checklist have been implemented; exact-head hash-locked CI has passed. The first-increment closure recommendation is ready for Owner review.
- A4 independent verification is IN PROGRESS; A5 remains NOT STARTED.
- Work stays on this branch. Do not modify `main`, merge, deploy, sign, or publish.
- Preserve existing UI and unrelated repository work. No UI recreation or replacement is authorized.
- Use synthetic fixtures only; do not introduce production data.
- No paid service, billing, or deposit is assumed.

## 3. Explicitly excluded from this A3 scope

Until authoritative current sources and separate approval resolve them, do not implement or encode:

1. The organizational hierarchy or any parent-child relationship among the Owner-provided labels.
2. Organizational entity types, tiers, jurisdictions, reporting lines, or office mandates.
3. Roles, positions, delegated authority, permission matrices, or organization-scoped authorization rules.
4. Membership lifecycle or governance approval workflows whose rules depend on constitutional or bylaw provisions.
5. Navigation, dashboards, routing, or reports that imply an unverified organizational structure.
6. Any use of the historical sixth-revision material as current authority.
7. Any UI source replacement, migration, or recreation while provenance remains unresolved.

Keep `ቀጣና` and `ኅብረት` distinct in all future work. Preserve the Owner's established Amharic terminology and do not introduce prohibited legacy organizational labels.

## 4. Candidate authority-independent work areas

These are candidates for subsequent implementation only after the technical prerequisites below are resolved and acceptance criteria are recorded:

- Repository/build/test automation that does not assume a product framework or paid CI service.
- General input validation, error handling, and secure configuration patterns.
- Audit-event envelope and correlation metadata that do not define institutional authority or sensitive-data retention.
- Localization infrastructure and Unicode-safe rendering primitives, without inventing translations or replacing existing UI.
- Ethiopian/Gregorian calendar conversion utilities, only after a library/algorithm and test oracle are selected and verified.
- Accessibility and security test harnesses that do not require live user data.
- Synthetic fixtures and negative tests for fail-closed behavior, without inventing roles or organizational scopes.

No candidate above is yet an approved framework, database, API, schema, hosting, or deployment decision.

## 5. Approved technical baseline and implementation status

The Owner-approved first-increment technical baseline is:

- Backend: Django/Python.
- Runtime: Python 3.14.10 and Django 5.2.19.
- API: Django-native `GET /health/` only; DRF and general resource endpoints are deferred.
- Persistence: no database server, ORM persistence, migrations, schemas, models, or database-backed features.
- Quality: Django built-in test runner, Ruff 0.17.4, and pip-audit 2.10.1.
- CI: standard public GitHub Actions Linux runner, least-privilege read-only permissions, immutable action SHAs, and local fallback.
- Dependencies: direct pins in `requirements.txt` and `requirements-dev.txt`; transitive lock in `requirements-lock.txt` with 32 exact package versions and 402 SHA-256 hashes.

The approved first-increment files are implemented on `a3/restricted-foundation-scope`. Earlier run #22 verified hash-lock integration at its own commit. Final A3 exact-head workflow run #26 passed hash-locked installation, Django system check, three tests, Ruff lint/format, and pip-audit. The audit reported no known vulnerabilities at the time of the run. Exact tested SHA: `bf3443b288bcc78d7479630ffa92f0af7c88cd77`. Evidence: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42968545687

This technical baseline is limited to the authority-independent foundation. Frontend selection, database/persistence architecture, authentication/authorization, identity, institutional hierarchy, office mandates, governance workflows, localization product behavior, hosting, and deployment remain unselected, deferred, or blocked. Preserve existing UI; do not replace it.

## 6. Blocking evidence retained

The following A2 gaps remain open and must not be represented as fixed by this A3 authorization:

- G-01 — authoritative seventh-edition Constitution: BLOCKING / CRITICAL.
- G-02 — current bylaws and amendments: BLOCKING / CRITICAL; a third-party sixth-revision candidate is historical/unverified.
- G-03 — main-branch constitutional-source conflict: BLOCKING / MATERIAL.
- G-04 — hierarchy and relationships: BLOCKING / CRITICAL.
- G-05 — office mandates/reporting: BLOCKING / HIGH.
- G-06 — existing UI provenance: UNRESOLVED / HIGH.
- G-07 — stakeholder validation: OPEN / HIGH.
- G-08 — qualified legal/institutional review: OPEN / HIGH.
- G-09 — privacy and safeguarding validation: OPEN / HIGH.
- G-10 — broader product/requirements technical acceptance: NOT TESTED; the restricted A3 foundation has separate passing CI evidence.
- G-11 — requirements validation: OPEN / HIGH.

## 7. Change-control and verification requirements

Every implementation change must:
- Be confined to this A3 branch or a later explicitly authorized A3 work branch.
- Map to a named, authority-independent acceptance criterion.
- Include focused automated tests and negative tests where applicable.
- Avoid secrets, live personal/pastoral/member data, and paid dependencies.
- Preserve existing UI and unrelated work.
- Report exact changed paths, commit SHA, test commands/results, CI evidence, and unresolved limitations.

A3 completion requires a reconciled change inventory and review evidence. A4 verification remains a separate stage. Merge, deployment, signing, publication, and production-data use require separate Owner authorization.

## 8. Current disposition

**A3 scope authorization: VERIFIED.**  
**Restricted first-increment implementation: COMPLETE.**  
**Final A3 exact-head hash-locked CI: PASS — run #26, SHA `bf3443b288bcc78d7479630ffa92f0af7c88cd77`.**  
**A3 first-increment closure: OWNER-ACCEPTED before A4 authorization.**  
**A2: PARTIAL / OPEN.**  
**A4: IN PROGRESS. A5: NOT STARTED.**  
**Main branch: UNCHANGED.**  
**Merge/deployment/signing/publication: NOT AUTHORIZED.**
