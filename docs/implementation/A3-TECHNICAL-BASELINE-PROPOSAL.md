# EKHC OS — A3 Technical Baseline Decision Proposal

**Status:** PARTIALLY APPROVED — backend and database deferral decisions recorded; remaining baseline decisions pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Related authorization:** `docs/implementation/A3-RESTRICTED-FOUNDATION-SCOPE.md`

## 1. Decision requested

Approve a technical baseline for a first, authority-independent implementation increment, or return the proposal for revision.

This proposal does not approve constitutional or organizational modeling, production data, an existing UI replacement, deployment, or any paid service. No production database or schema is approved.

## 2. Verified current repository condition

The inspected `main` tree contains project documentation and assessment artifacts. It does not contain an identifiable application source tree, package manifest, lockfile, established test suite, or build pipeline. The prior UI paths recorded in the A2 report were not present on the inspected main ref. UI provenance remains unresolved.

The A1 architecture document explicitly leaves framework, database, API, authentication/session model, offline protocol, storage, hosting, and deployment topology undecided. Therefore, this proposal treats those as decisions, not inherited facts.

## 3. Recommended technical principles

1. **Preserve existing work:** do not create a replacement UI or assume the absent UI paths are disposable.
2. **One deployable application initially:** evaluate a modular monolith with explicit internal boundaries; do not introduce microservices without measured need.
3. **Server-authoritative security:** no client-supplied role, office, organization, or scope value may grant access.
4. **Fail closed:** until constitutional and institutional authority is verified, no organizational hierarchy, role catalogue, or authority-bearing workflow is implemented.
5. **Synthetic-only development:** fixtures must be fictional and contain no real member, pastoral, child, or governance data.
6. **No paid dependency:** local development and automated checks must be usable without a paid account, deposit, billing activation, or paid hosted service.
7. **Reproducibility:** pin supported runtime and dependency versions; commit lockfiles; document deterministic setup and test commands.
8. **Accessibility and localization by design:** preserve Unicode, test Amharic text rendering, and avoid hard-coded Gregorian-only assumptions. Do not invent translations or calendar conversion behavior.
9. **No production claims:** successful unit tests or public CI do not constitute security certification, accessibility conformance, operational readiness, or production acceptance.

## 4. Technology options to evaluate

| Concern | Candidate options | Current disposition |
|---|---|---|
| Backend | Laravel/PHP; Django/Python; FastAPI/Python | Django/Python selected as preferred backend by Owner; runtime version and exact dependency set remain to be specified. |
| Frontend | Existing UI if recovered; otherwise Vue/TypeScript or React/TypeScript | No selection. Existing UI provenance must be resolved before any replacement or new shell is considered. |
| Persistence | PostgreSQL; SQLite for isolated local tests only if compatible with chosen runtime | Owner approved deferring database and schema implementation from the first A3 increment. No database dependency, migration, schema, or persistence layer is to be added in that increment. Revisit persistence only when an approved requirement demonstrates the need. |
| API | Django-native minimal endpoint for the first increment; Django REST Framework (DRF) deferred | Owner approved Django-native endpoints only for the minimal health/readiness check in the first increment. No general REST API or resource endpoints are approved. DRF is deferred. |
| Tests | Framework-native unit/integration tests; static analysis; dependency audit; accessibility checks where UI exists | Tooling depends on approved runtimes. Tests must include negative authorization cases before any access-control feature is accepted. |
| CI | Public-repository GitHub Actions or documented local commands | Candidate only. Verify actual free-tier availability and workflow permissions; no billing/top-up assumptions. |
| Delivery | Local development and CI verification only | No hosting, deployment, release signing, or publication in this increment. |

## 5. Proposed first implementation increment (after technical approval)

The first increment should remain deliberately narrow and must not encode institutional authority:

- Establish the approved repository layout and reproducible local developer setup.
- Add a minimal health/readiness check that exposes no secrets or sensitive data.
- Add centralized configuration validation and safe error handling.
- Add structured logging conventions with secret and personal-data redaction.
- Add a test harness and CI checks that run without paid services.
- Add a generic audit-event envelope only if its fields do not imply an authority model or unapproved retention policy.
- Add Unicode and Amharic rendering test fixtures only in an approved UI location; do not create a replacement UI.
- Add calendar conversion only after selecting a reviewed implementation and authoritative test vectors for Ethiopian and Gregorian dates.

**Database boundary:** no database server, ORM persistence integration, migration, schema, model, or database-backed feature is included in this first increment. Tests should use in-memory or framework-supported non-persistent mechanisms where practical. This does not select SQLite or authorize a hidden substitute database.

Each item needs a separate acceptance criterion and focused tests before implementation. This list is not blanket approval to choose dependencies or create product features.

## 6. Explicitly deferred

- Database selection for production, persistence integration, migrations, and all schemas.
- Organization, church, office, ministry, membership, and hierarchy schemas.
- Roles, permissions, delegated authority, scope resolution, and identity-to-office assignment.
- Governance meetings, approvals, minutes, resolutions, and official records workflows.
- Live personal, pastoral, membership, child, or financial data.
- Offline caching or synchronization of sensitive records.
- UI recreation, redesign, or replacement.
- Production migration, hosting, monitoring service purchase, deployment, release signing, or publication.

## 7. Remaining decisions before executable work

1. Frontend disposition: continue existing UI if recovered; no replacement is authorized by default.
2. API approach: resolved by Owner Decision 3 below; no general API surface is approved.
3. Test, lint, static-analysis, and dependency-audit tools.
4. CI approach constrained to public/free execution and local fallback.
5. Supported Python and Django versions, pinned only after compatibility and support-lifecycle review.
6. Whether the proposed first increment is the intended A3 implementation sequence.
7. File-level scope and measurable acceptance criteria for each included item.

If any decision is deferred, keep the related implementation item out of scope.

## 8. Acceptance and governance

After the remaining decisions are resolved, create a separate implementation checklist with file-level scope and testable acceptance criteria. Implement only that checklist on the authorized A3 branch. Record exact dependency versions, changed files, commit SHAs, test commands/results, CI run links, and limitations.

A4 remains a separate verification gate. A2 remains PARTIAL / OPEN until its evidence and closure conditions are separately reconciled and accepted. Merge, deployment, signing, publication, and production data remain separately gated.

## 9. Owner decision record — 2026-11-11

### Decision 1 — backend

**Decision:** APPROVED — Django/Python as the preferred EKHC OS backend candidate.

**Decision scope:** This approval selects Django/Python as the preferred backend for the technical baseline. It does not select an exact Python or Django version, approve dependencies, database/schema, API contracts, frontend technology, authentication/authorization model, or implementation file list.

### Decision 2 — database deferral

**Decision:** APPROVED — defer database and schema implementation from the first A3 increment.

**Decision scope:** The first increment must not add a database server dependency, ORM persistence integration, migrations, schemas, or database-backed product features. Use non-persistent test mechanisms where practical. This is a deferral, not a selection of SQLite or any other database. Reconsider persistence only after a concrete, approved requirement justifies it.

### Decision 3 — first-increment API approach

**Decision:** APPROVED — use Django-native endpoints for the first increment; defer Django REST Framework (DRF).

**Decision scope:** Django-native routing/views may be used only to implement and test the minimal health/readiness check described in Section 5. The endpoint must not expose secrets, personal data, organizational data, or internal configuration values. This decision does not approve a general REST API, resource endpoints, authentication API, data endpoints, API contracts, or DRF dependency. Any broader API surface requires a separate Owner decision.

**Implementation authorization:** These decisions record technical direction only. Executable implementation remains NOT STARTED pending the remaining technical decisions and a file-level acceptance checklist.

**Constraints retained:** synthetic data only; preserve existing UI; no invented organizational hierarchy, offices, mandates, roles, permissions, or governance workflows; no paid services; no main-branch changes; no merge, deployment, signing, or publication without separate approval.

## 10. Current disposition

- Backend preference: **OWNER-APPROVED — Django/Python**.
- First-increment API: **OWNER-APPROVED — Django-native health/readiness endpoint only; DRF DEFERRED**.
- First-increment database/schema work: **OWNER-APPROVED — DEFERRED**.
- Complete technical baseline: PARTIAL / OPEN.
- Exact runtime and dependencies: NOT SELECTED.
- Executable application implementation: NOT STARTED.
- Existing UI: PRESERVE; provenance unresolved.
- Main branch: MUST REMAIN UNCHANGED.
- Paid services: NOT ASSUMED.
- Organizational authority and hierarchy: EXCLUDED / BLOCKED.
