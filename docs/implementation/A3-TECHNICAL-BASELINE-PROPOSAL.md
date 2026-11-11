# EKHC OS — A3 Technical Baseline Decision Proposal

**Status:** PROPOSAL ONLY — Owner decision required  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Related authorization:** `docs/implementation/A3-RESTRICTED-FOUNDATION-SCOPE.md`

## 1. Decision requested

Approve a technical baseline for a first, authority-independent implementation increment, or return the proposal for revision.

This proposal does not approve constitutional or organizational modeling, production data, an existing UI replacement, deployment, or any paid service. No framework or database is selected by this document.

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
| Backend | Laravel/PHP; Django/Python; FastAPI/Python | No selection. Compare maintainability, security defaults, team capability, testability, and hosting constraints before approval. |
| Frontend | Existing UI if recovered; otherwise Vue/TypeScript or React/TypeScript | No selection. Existing UI provenance must be resolved before any replacement or new shell is considered. |
| Persistence | PostgreSQL; SQLite for isolated local tests only if compatible with chosen runtime | PostgreSQL remains an A1 candidate, not an approved production choice. Do not create schema yet. |
| API | Framework-native API or documented REST boundary | No endpoint contract or API surface approved. |
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

Each item needs a separate acceptance criterion and focused tests before implementation. This list is not blanket approval to choose dependencies or create product features.

## 6. Explicitly deferred

- Organization, church, office, ministry, membership, and hierarchy schemas.
- Roles, permissions, delegated authority, scope resolution, and identity-to-office assignment.
- Governance meetings, approvals, minutes, resolutions, and official records workflows.
- Live personal, pastoral, membership, child, or financial data.
- Offline caching or synchronization of sensitive records.
- UI recreation, redesign, or replacement.
- Production migration, hosting, monitoring service purchase, deployment, release signing, or publication.

## 7. Required decisions before executable work

The Owner should approve or revise the following:

1. Backend framework and supported runtime.
2. Frontend disposition: continue existing UI if recovered, or authorize a new UI only after provenance review.
3. Persistence choice and whether any database is needed in the first increment.
4. API approach and whether an API is in the first increment.
5. Test, lint, static-analysis, and dependency-audit tools.
6. CI approach constrained to public/free execution and local fallback.
7. Whether the proposed first increment is the intended A3 implementation sequence.

If any decision is deferred, keep the related implementation item out of scope.

## 8. Acceptance and governance

After Owner approval, create a separate implementation checklist with file-level scope and testable acceptance criteria. Implement only that checklist on the authorized A3 branch. Record exact dependency versions, changed files, commit SHAs, test commands/results, CI run links, and limitations.

A4 remains a separate verification gate. A2 remains PARTIAL / OPEN until its evidence and closure conditions are separately reconciled and accepted. Merge, deployment, signing, publication, and production data remain separately gated.

## 9. Current disposition

- Technical baseline: PROPOSED / NOT APPROVED.
- Executable application implementation: NOT STARTED.
- Existing UI: PRESERVE; provenance unresolved.
- Main branch: MUST REMAIN UNCHANGED.
- Paid services: NOT ASSUMED.
- Organizational authority and hierarchy: EXCLUDED / BLOCKED.
