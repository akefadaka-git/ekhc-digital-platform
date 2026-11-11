# EKHC OS — A2 Read-only Reconciliation Report

**Status:** PARTIAL — reconciliation in progress; not closed  
**Stage authorization:** Owner approved A1 and authorized A2 on 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Report branch:** `docs/a2-read-only-reconciliation`  
**Report baseline:** `aad86d638ba9dd791de09f32784f49d3e43aba84`  
**Main snapshot inspected:** `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`  
**Method:** Read-only inspection of repository refs and source files; this report is a separate evidence artifact.

## 1. Executive result

A2 has started. Repository inventory and an initial cross-document comparison are complete. The review found material source-baseline and terminology conflicts, stale stage-status statements, and an inaccurate description of the assessment-branch topology. The governing seventh-edition Constitution and current bylaws remain unavailable, so current constitutional authority cannot be reconciled or certified.

**Disposition: PARTIAL / OPEN.** No implementation, source correction, merge, deployment, signing, publication, or production-data activity was performed.

## 2. Owner authorization and boundaries

The Owner selected option 2: approve A1 and authorize A2 read-only reconciliation. This supersedes earlier draft statements that A1 approval was pending and A2 was not authorized.

A2 scope:
- Compare the approved Owner directions and A1 assessment package with current repository content and available historical work.
- Record evidence, conflicts, provenance, and unresolved dependencies.
- Do not change `main` or modify existing A1 source documents.
- Do not infer missing constitutional provisions, institutional authority, or UI provenance.
- Keep all examples and test data synthetic.
- No A3 implementation, A4 verification, A5 deployment-readiness work, merge, deployment, signing, or publication.

## 3. Repository and branch inventory

The repository branch search returned these nine visible branches:
- `main`
- `a1/assessment-specification`
- `docs/a1-assessment-foundation`
- `docs/a1-data-classification-privacy`
- `docs/a1-data-inventory-workbook`
- `docs/a1-architecture-options-assessment`
- `docs/a1-hosting-sustainability-cost-assessment`
- `docs/a1-legal-regulatory-policy-assessment`
- `docs/a1-master-evidence-decision-register`

The inspected main snapshot is `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.

Commit comparisons against main show the A1 documentation branches are cumulative descendants with five commits of divergence behind main:
- Foundation: 26 ahead / 5 behind.
- Privacy: 28 ahead / 5 behind.
- Data inventory: 29 ahead / 5 behind.
- Architecture assessment: 30 ahead / 5 behind.
- Hosting assessment: 31 ahead / 5 behind.
- Legal/policy assessment: 33 ahead / 5 behind.
- Master register: 34 ahead / 5 behind.
- Earlier assessment specification: 3 ahead / 5 behind.

This confirms the later assessment branches carry forward earlier assessment documents. The master register's claim that the assessment documents are separate branch-only files and are not present together on the later assessment branch is inaccurate. This is an inventory correction, not permission to merge branches.

## 4. Main-branch source conflict

The current main README blob is `d94349c8a4050a745ce8bb229a2823c671bf4d3a`. It identifies the sixth-revision Constitution/bylaw as the current A1 governing baseline and includes a third-party public copy as the working source.

The A1 source register blob `ad77bad452a4b42b47daf7507a57aa9cde0d30c0` identifies the seventh-edition Constitution as the required governing baseline and marks it missing. The master register also records the seventh edition as required and missing.

Main additionally contains:
- `docs/constitution/sixth-revision-article-index.md`, blob `a671d8d2307fcd26a2709f0e55ae9ceefa57021c`.
- `docs/constitution/articles-25-41-analysis.md`, blob `907a040734b3f237d71b5b3c56d775c215bdfa07`.

The index explicitly describes itself as a contents-page extraction and not a full interpretation. The Articles 25–41 note records an incomplete third-party text extraction. These are historical research artifacts only. They do not establish the current governing edition, complete article wording, or current institutional hierarchy.

**Disposition:** Material conflict confirmed; unresolved because the authoritative seventh-edition source and current bylaws have not been verified. Do not use the historical edition to freeze current hierarchy, roles, permissions, or system relationships. Do not silently amend main.

## 5. Owner terminology and hierarchy constraints

The A1 decision log and hierarchy register preserve these Owner constraints:
- `ቀጣና` and `ኅብረት` are distinct; do not collapse them.
- Preserve the established Amharic terminology; do not introduce an unapproved English organizational equivalent.
- The recovered eight-step organizational chain is a discovery input only, not a verified constitutional schema.
- Do not invent offices, tiers, reporting lines, role authorities, or parent-child relationships.
- Two Owner-prohibited legacy organizational labels must remain absent throughout project artifacts and product surfaces.

The current main README contains wording that conflicts with these terminology constraints. Exact prohibited strings are intentionally not reproduced in this report.

**Disposition:** Conflict confirmed; no source edits made. Any correction to main requires a separately controlled change after this A2 reconciliation identifies the full impact.

## 6. Assessment package reconciliation

The later A1 master-register branch was re-fetched and contains the assessment package, including:
- Project charter, requirements, architecture proposal, security baseline and roadmap.
- A1 assessment plan, source register, UI reconciliation register, stakeholder workflow discovery, risk register and requirements traceability matrix.
- Data classification/privacy assessment and data-inventory/stakeholder workbook.
- Architecture options assessment, hosting/TCO assessment and legal/regulatory/institutional-policy assessment.
- Master evidence and decision register.

The fetched file blobs matched the previously recorded identifiers for the master register and principal assessment documents. The requirements catalogue remains provisional; the traceability matrix itself states that trace links are not validation, acceptance, implementation, or test evidence.

### Reconciliation findings

| ID | Finding | Status |
|---|---|---|
| A2-01 | Main README uses the historical constitutional edition as current baseline, conflicting with Owner-directed seventh-edition requirement | CONFLICT — BLOCKING |
| A2-02 | Seventh-edition Constitution not available or verified | MISSING — BLOCKING |
| A2-03 | Current bylaws and amendments not available or verified | MISSING — BLOCKING |
| A2-04 | Assessment branches are cumulative; master register's topology description is inaccurate | VERIFIED — DOCUMENTATION CORRECTION REQUIRED |
| A2-05 | Master register still says A1 unapproved and A2 unauthorized, now superseded by Owner decision | STALE — UPDATE REQUIRED IN CONTROLLED A2 RECORD |
| A2-06 | Master register checklist still places Owner A1 approval as pending | STALE — SUPERSEDED |
| A2-07 | Historical UI source repository/branch/commit remains unresolved | UNRESOLVED |
| A2-08 | Authorized stakeholder/process-owner validation remains unavailable | MISSING |
| A2-09 | Legal and institutional policy applicability remains unreviewed by qualified reviewers | NOT REVIEWED |
| A2-10 | Architecture, hosting, data classes and authorization model remain proposals | NOT APPROVED FOR IMPLEMENTATION |
| A2-11 | No measured technical, accessibility, security, performance, offline or operational test evidence is present in the A1 documentation baseline | NOT TESTED |

## 7. UI provenance

The historical UI register identifies the prior paths:
- `resources/js/layouts/Header.vue`
- `resources/js/styles/tokens.css`
- `tailwind.config.js`

The prior A1 inspection recorded 404 responses for these exact paths on main. Current GitHub code searches for those identifiers returned no matches in the default-branch search. The visible branch inventory contains no UI-named branch. This does not prove the artifacts never existed or are absent from every repository/account.

**Disposition:** UNRESOLVED. Do not recreate, overwrite, copy, or replace the UI until its source repository, branch, commit and ownership are established.

## 8. Requirements and validation status

The requirements catalogue contains 12 functional requirements, 8 non-functional requirements, and 9 elicitation gaps. The traceability matrix reports reference coverage of 12/12 functional and 8/8 non-functional requirements, while reporting zero fully validated functional requirements and zero measured/tested non-functional requirements.

A2 does not upgrade any requirement to validated merely because its source document exists. Validation still requires current authoritative evidence, authorized process-owner confirmation, observable acceptance criteria, documented conflicts/dependencies/privacy implications, and Owner approval at the relevant gate.

## 9. A2 control and change register

No repository source document or main-branch file was changed during this read-only pass. This report is a separate A2 evidence artifact on its own branch. No PR was opened and no branch was merged.

Proposed documentation corrections for a later controlled A2 update:
1. Correct the master register's branch-topology description using the observed cumulative branch comparisons.
2. Replace stale A1/A2 gate status with the Owner's 2026-11-11 decision, preserving the distinction between stage approval and evidence validation.
3. Record the main README constitutional-baseline and terminology conflict without modifying main.
4. Reconcile source references and blob identifiers against current branch tips before any integration decision.

These are documentation reconciliation actions only. They do not authorize changes to main or implementation.

## 10. Remaining A2 work and exit conditions

A2 remains open until the following are addressed or explicitly recorded as blocked:
- Obtain and verify the complete authoritative seventh-edition Constitution, including edition, approval/adoption date, amendments, completeness and exact relevant clauses.
- Verify current bylaws and amendments and their relationship to the Constitution.
- Reconcile organizational terms, entities, parentage, authority and exceptions against those sources.
- Locate the historical UI source repository/branch/commit and perform file-by-file read-only inspection.
- Reconcile all A1 documents and decision records against the Owner's current approval and constraints.
- Record authorized stakeholder evidence when available; until then, retain workflow requirements as unvalidated.
- Record legal/policy review dependencies as open; do not claim compliance.
- Produce a final A2 gap matrix and closure recommendation.

**Current conclusion:** A2 inventory and initial conflict reconciliation are verified. Full constitutional, UI, stakeholder, and legal/policy reconciliation is blocked or unresolved. A2 is PARTIAL / OPEN. A3 implementation remains unauthorized.


## 11. Official public-site corroboration (not constitutional authority)

Public official EKHC pages were checked as corroborative evidence only on 2026-11-11:

- The newer Amharic homepage at `https://ekhc.et/amh/` presents public ministry/service labels, including missions, theological education, finance, human resources/properties/logistics, communication/literature, discipleship/church education, women, youth, children, social security, professionals, leadership training, community empowerment, and marriage/prayer services.
- The English homepage at `https://ekhc.et/` presents a substantially similar set of public ministry/service labels.
- The older `https://ekhc.net/about_us` page reports a different public organizational snapshot, including numerical counts for zonal administrations, subordinate offices and special centres. The page does not establish the constitutional authority, approved terminology, or current validity of those counts.
- The `https://ekhc.net/literature_and_communication` page describes publication and circulation of church legal documents and archive work. It does not expose the required seventh-edition Constitution.

**Reconciliation result:** Official public pages are useful for discovery and corroboration, but their different content, freshness and level of detail prevent them from resolving constitutional hierarchy, office mandates, approved terminology, or current reporting relationships. No public-page label or translation has been adopted as a canonical application term.

**Status:** CORROBORATIVE EVIDENCE RECORDED; GOVERNANCE AUTHORITY UNRESOLVED.

