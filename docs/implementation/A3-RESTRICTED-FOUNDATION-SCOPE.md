# EKHC OS — A3 Restricted Foundation Scope and Authorization Record

**Status:** OWNER-AUTHORIZED SCOPE; implementation entry constraints remain open  
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
- A3 restricted scope is OWNER-AUTHORIZED, but executable implementation is subject to the technical and source prerequisites in this record.
- A4 and A5 remain NOT STARTED.
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

## 5. Technical prerequisites — unresolved

The A1 architecture proposal explicitly leaves framework, backend/frontend technology, database, migration strategy, mobile/PWA delivery, authentication/session model, offline protocol, storage, hosting, and deployment topology undecided.

The repository's current `main` tree contains documentation and historical research artifacts, but no application source tree or established build/test pipeline. Therefore, selecting a runtime or creating executable application code now would silently convert an unapproved architecture proposal into an implementation decision.

Before executable A3 work begins, record an Owner-approved technical baseline covering at minimum:

- Backend and frontend/runtime selection, including supported versions.
- Package/build/test tooling and repository layout.
- Database and migration approach, if any.
- API boundary and authentication/session approach, if any.
- Test strategy and free/public-repository CI constraints.
- Localization and Ethiopian-calendar implementation/test references.
- Security baseline and dependency-update policy.

This is a technical prerequisite, not a request to resolve constitutional authority by assumption.

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
- G-10 — technical acceptance evidence: NOT TESTED.
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
**Executable implementation: BLOCKED pending technical baseline and acceptance criteria.**  
**A2: PARTIAL / OPEN.**  
**Main branch: UNCHANGED.**  
**Merge/deployment/signing/publication: NOT AUTHORIZED.**
