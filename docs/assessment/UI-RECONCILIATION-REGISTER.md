# Existing EKHC UI Reconciliation Register

**Status:** OPEN — historical UI work is acknowledged, but its authoritative source location is not yet verified.  
**Purpose:** Protect prior work from accidental replacement and define the evidence needed for a safe, read-only reconciliation.

## 1. Recovered historical UI evidence

Prior EKHC project discussions describe an existing UI foundation with the following references:

| Evidence ID | Artifact / area | Recovered information | Current remote verification |
|---|---|---|---|
| UI-001 | `resources/js/layouts/Header.vue` | Existing header component; a prior incremental UI-SHELL-3b change was described | NOT FOUND on current `main` at this exact path (GitHub 404) |
| UI-002 | `resources/js/styles/tokens.css` | Design-token file; prior UI-SHELL-3a work described a header surface token | NOT FOUND on current `main` at this exact path (GitHub 404) |
| UI-003 | `tailwind.config.js` | Prior note described a token-to-Tailwind mapping | NOT FOUND on current `main` at this exact path (GitHub 404) |
| UI-004 | Shared application shell | Historical design scope included header, active context, sidebar, footer, layouts, cards/KPI, tables/charts/widgets and interface states | DESIGN CONTEXT RECOVERED; source files not located |
| UI-005 | Localization and responsive behavior | Amharic-first, Ethiopian-calendar-first and mobile-first direction | DESIGN CONTEXT RECOVERED; current implementation not verified |

The historical header note described a blue header surface, a separately preserved accent stripe, a larger EKHC logo, white identity/tagline text, and an Ethiopian date shown at medium-and-larger breakpoints. These are historical implementation notes, not current visual acceptance criteria.

## 2. Verification performed for this A1 pass

The exact paths in UI-001 through UI-003 were queried against the current repository `main` branch and returned GitHub 404 responses. The available evidence therefore does not establish whether the artifacts were moved, exist on another branch, belong to a different repository, or were never committed to the current repository.

No files were modified in order to recreate or replace the historical UI. No UI package, component, route, backend endpoint, or schema was introduced by this register.

## 3. Required read-only reconciliation procedure

When the source location is established:

1. Record repository full name, default branch, candidate branch, and exact commit SHA.
2. Inventory the complete UI tree, package manifests, build configuration, route definitions, layouts, shared components, design tokens, localization files and tests.
3. Capture the existing build/test state and any known failing checks without changing the source.
4. Compare each artifact with the recovered design context and current A1 requirements.
5. Identify preserved, reusable, conflicting, incomplete, obsolete and unknown elements.
6. Record dependencies and integration boundaries; do not assume that visual similarity means architectural compatibility.
7. Produce a file-by-file reconciliation matrix and proposed change plan for Owner review.
8. Do not copy, overwrite, rebase, merge, install packages or implement changes during read-only reconciliation unless separately authorized.

## 4. Reconciliation decision rules

- Preserve existing work by default.
- Do not treat a historical conversation note as proof that a file currently exists.
- Do not recreate missing paths merely to make the repository resemble a historical description.
- Do not change the existing hierarchy, access model, or navigation based on unverified constitutional assumptions.
- Separate visual design findings from route, data, authorization and workflow findings.
- Any proposed redesign or replacement must identify the exact existing artifact and explain why reuse is not viable.

## 5. Closure criteria

This register can be marked VERIFIED only when the authoritative source repository/branch and commit are identified, the relevant files are inspected, the complete inventory is recorded, and a read-only reconciliation report is reviewed. Until then, UI reconciliation remains PARTIAL / UNRESOLVED.


## 6. Supplemental provenance findings — 2026-11-26

The follow-up repository inventory did not identify an exact original UI repository, branch, or commit that can be tied to UI-001 through UI-005. The historical paths remain unverified. The current EKHC project repository is not presumed to be the original UI source merely because it is the active project repository.

**Current status:** SRC-005 remains PARTIAL / UNRESOLVED. This is a provenance gap, not proof that the historical UI work is lost or never existed.

## 7. Minimum evidence required to recover the original UI

Accept one of the following as a starting lead, then independently verify provenance:

1. Exact GitHub/GitLab repository URL and owner/organization.
2. Exact branch name plus a commit SHA from the original implementation.
3. A source archive that includes verifiable Git metadata, commit history, or a signed/reproducible provenance record.
4. An existing deployment/source-control record that identifies the repository and immutable commit used for the deployed UI.

A screenshot, exported design image, copied component, local folder name, or recollection of a branch label may help locate the work but does not by itself prove the original commit or source ownership.

## 8. Read-only recovery checklist

When a candidate source is supplied or located:

- Verify repository identity and access scope.
- Resolve the branch to its current commit SHA and record the timestamp of inspection.
- Verify that the candidate commit contains the historical paths or clearly corresponding renamed artifacts.
- Inspect commit history around the claimed UI-SHELL changes and record exact commit SHAs.
- Inventory package manifests, framework/build versions, routes, shared shell components, design tokens, localization and calendar code, assets, tests and CI.
- Compare the candidate source against the current project without copying or modifying either repository.
- Record provenance confidence and unresolved ownership/licensing questions.
- Produce a file-by-file preserve/reuse/conflict/missing/unknown matrix for Owner review.

Do not install dependencies, execute untrusted build scripts, copy source files, change branches, open a PR, or implement a replacement as part of this read-only recovery.

## 9. Source intake record

| Required field | Value |
|---|---|
| Original repository URL / owner | NOT PROVIDED / NOT VERIFIED |
| Original default branch | UNKNOWN |
| Claimed UI branch | UNKNOWN |
| Claimed implementation commit SHA | UNKNOWN |
| Source archive / provenance record | NOT PROVIDED |
| Historical UI-SHELL commit mapping | NOT VERIFIED |
| Repository ownership / reuse permission | NOT VERIFIED |
| Reconciliation disposition | BLOCKED — source provenance required |

No UI replacement, redesign, route, component, package, backend endpoint or schema is approved by this register. Existing UI preservation remains the default.
