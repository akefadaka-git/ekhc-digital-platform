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



## 12. Final provenance and authority reconciliation — 2026-11-11

### 12.1 UI provenance search — expanded

The search was extended beyond the initial main-branch inspection:

- Re-fetched the three historical paths from main; all three returned 404:
  - resources/js/layouts/Header.vue
  - resources/js/styles/tokens.css
  - tailwind.config.js
- Rechecked the visible branch inventory. It contains the A1 documentation branches, the A2 report branch, and main; no UI-specific branch is present.
- Searched the EKHC repository's default-branch code index for the historical file names and references. No matching files were returned.
- Searched the accessible current Owner GitHub repository inventory and the accessible legacy-account repository inventory for a separate EKHC UI repository. No separately identifiable Owner-controlled EKHC UI repository was surfaced.
- Rechecked prior project records. They preserve the same three paths and describe the former UI as an Amharic-first, Ethiopian-calendar-first, mobile-first shell, but do not identify a verifiable repository, branch, commit, or source artifact.

**Result:** UI provenance remains UNRESOLVED. The search is exhaustive only across the accessible Owner repository inventories, visible branches, available indexed code results, and retained project records. It cannot establish absence from private, unindexed, deleted, transferred, or otherwise inaccessible repositories. No candidate was found that can safely be declared the source of truth. No UI code was copied, recreated, replaced, or changed.

### 12.2 Hierarchy and authority reconciliation

The Owner-provided eight-entry sequence is retained exactly as a discovery input:

| Sequence | Owner-provided label | Evidence currently available | A2 disposition |
|---:|---|---|---|
| 1 | Church | Official EKHC public pages confirm institutional identity; the main README also quotes a historical constitutional source | Identity corroborated; constitutional authority and full hierarchy unresolved |
| 2 | ዋ/ጽ/ቤት | A historical transcription in the repository includes a main-office label | Exact current name, scope, authority, and relationship unresolved |
| 3 | ቀጣና | The historical transcription contains a corresponding assembly/office category; official public pages do not establish its constitutional authority | Preserve as distinct Owner term; current powers and parentage unresolved |
| 4 | ቀጣና ጽ/ቤት | Historical transcription includes a corresponding office label | Current mandate, reporting line, and relationship unresolved |
| 5 | አጥቢያ ቤተ ክርስቲያናት ኅብረት | Historical transcription includes a corresponding assembly/office category | Preserve ኅብረት as a distinct term; current scope and parentage unresolved |
| 6 | ኅብረት ጽ/ቤት | Historical transcription includes a corresponding office label | Current mandate, reporting line, and relationship unresolved |
| 7 | አጥቢያ ቃለ ሕይወት ቤተ ክርስቲያን | Historical transcription contains local-church provisions and categories | Current legal/organizational definition and relationship unresolved |
| 8 | አጥቢያ ጽ/ቤት | Historical transcription includes a local-church office label | Current mandate, reporting line, and relationship unresolved |

The historical material above is the sixth-revision text identified in the main README and a third-party-hosted copy. It is not the required seventh-edition governing source, and its authenticity, completeness, amendment status, and continued effect have not been established. It may be used only as historical comparison material. The official public websites provide corroborative institutional and ministry information, not constitutional proof of parentage or delegated authority.

**Binding reconciliation controls:**
- Keep ቀጣና and ኅብረት distinct; do not merge, rename, or translate one into the other.
- Preserve the eight labels as Owner-provided discovery terminology only.
- Do not infer that the numbered list proves a complete parent-child path, reporting line, jurisdiction, delegation, or authority chain.
- Do not infer that an office is the parent of the corresponding assembly or entity from a shared name.
- Do not derive current roles, permissions, hierarchy enums, database relationships, API scopes, or navigation from the historical sixth-revision material or public website structure.
- The seventh-edition Constitution and current bylaws remain blocking sources for authority reconciliation.

**Result:** The terminology constraints are reconciled as binding design constraints. The current constitutional hierarchy and every unsupported relationship remain UNRESOLVED.

### 12.3 Final A2 gap matrix

| Gap | Evidence / current state | Severity | Required disposition before hierarchy or implementation approval |
|---|---|---|---|
| G-01 — Seventh-edition Constitution | Complete authoritative edition, adoption evidence, amendment history, and relevant clauses not obtained or verified | BLOCKING / CRITICAL | Obtain and authenticate the complete current edition; record exact articles, clauses, and pages |
| G-02 — Current bylaws | Current edition, amendments, legal status, and relationship to the Constitution not verified | BLOCKING / CRITICAL | Obtain and verify the current bylaws and all effective amendments |
| G-03 — Constitutional source conflict | Main README describes the sixth revision as the current baseline; A1 source register requires the seventh edition | BLOCKING / MATERIAL | Resolve through authoritative source evidence and a separately approved correction; main remains unchanged in A2 |
| G-04 — Eight-entry hierarchy | Owner-provided labels preserved; historical sixth-revision text offers limited comparison only | BLOCKING / CRITICAL | Validate exact labels, entity types, scope, authority, exceptions, and every parent-child edge against current sources |
| G-05 — Office mandates and reporting | Current organizational chart and approved office/department mandate records not verified | BLOCKING / HIGH | Obtain dated, authorized structure and mandate evidence; reconcile conflicts with constitutional text |
| G-06 — UI provenance | Historical paths known; no source repository, branch, commit, or recoverable artifact established | UNRESOLVED / HIGH | Identify the authoritative source location and ownership, then perform file-by-file read-only comparison |
| G-07 — Stakeholder validation | Authorized process-owner and stakeholder evidence unavailable | OPEN / HIGH | Validate workflows, roles, acceptance criteria, and exceptions with authorized owners |
| G-08 — Legal and policy review | Applicability and current institutional policy not reviewed by qualified reviewers | OPEN / HIGH | Obtain qualified legal/institutional review before compliance claims or sensitive workflows |
| G-09 — Privacy and safeguarding requirements | A1 risks and data classes are proposals; no authorized operational validation | OPEN / HIGH | Validate purpose, lawful basis, minimization, access, retention, safeguarding, and incident procedures |
| G-10 — Technical acceptance evidence | No measured security, accessibility, performance, offline/sync, recovery, or operational results | NOT TESTED | Define approved acceptance criteria and test only after the relevant implementation gate |
| G-11 — Requirements validation | 12/12 functional and 8/8 non-functional requirements have references; 0/12 functional requirements fully validated; 0/8 non-functional requirements measured/tested | OPEN / HIGH | Keep requirements provisional until authoritative and stakeholder evidence plus acceptance evidence exists |
| G-12 — A1 stage register | A1 approval and A2 authorization statements in the master register are stale | VERIFIED / DOCUMENTATION | Carry the 2026-11-11 Owner decision in this controlled A2 record; do not rewrite the A1 source register during read-only reconciliation |
| G-13 — Branch topology | Cumulative A1 branch history verified; master-register topology description inaccurate | VERIFIED / DOCUMENTATION | Correct only through a separately controlled documentation update; do not merge branches as a shortcut |
| G-14 — Main-branch terminology conflict | Main README conflicts with Owner terminology constraints | VERIFIED / MATERIAL | Preserve exact Owner constraints; defer any main correction to a separately authorized change |
| G-15 — Public-source limitations | Official public pages provide institutional/ministry corroboration but do not prove current constitutional hierarchy or office authority | VERIFIED / LIMITATION | Use only for discovery/corroboration; never substitute for the governing source |

### 12.4 A2 closure recommendation

**Recommendation to the Owner: do not declare a clean or fully reconciled A2 closure.** The read-only repository, branch, historical-reference, and public-source searches available to this review are complete to the extent accessible. The remaining material gaps are explicitly identified above, but the two governing-source dependencies and UI provenance remain unresolved.

The Owner may consider closing the *read-only evidence-review activity* as **VERIFIED-CLOSED WITH BLOCKERS RECORDED**, provided the closure record expressly preserves all of the following:

1. G-01 and G-02 remain BLOCKING / CRITICAL. No hierarchy or authority model is certified.
2. G-04 remains unresolved at the relationship and authority level. The eight labels remain discovery terminology only.
3. G-06 remains unresolved. Existing UI must be preserved; no recreation or replacement is authorized.
4. G-07 through G-11 remain open or not tested; no requirements, legal compliance, privacy readiness, or technical acceptance claims are implied.
5. The main-branch constitutional and terminology conflicts are recorded but not changed.
6. A2 closure does not authorize A3, source edits, schema/API/UI implementation, merge, deployment, signing, or publication.

**Current stage status pending Owner decision:** A1 = OWNER APPROVED; A2 = PARTIAL / OPEN, closure recommendation prepared; A3 = NOT AUTHORIZED / NOT STARTED; A4 = NOT STARTED; A5 = NOT STARTED.

If the Owner accepts the bounded evidence-review closure, the next permitted activity remains separately gated. Any A3 proposal must first be based on authenticated current governing sources and explicit scope approval. No automatic transition is implied by this recommendation.


## 13. Additional public bylaw candidate located — 2026-11-11

A further public-source search located a Scribd-hosted scan/transcription titled in Amharic as the EKHC bylaw, marked as a sixth revision and dated 2012 E.C. The page also contains a separate EKHC Constitution title/copyright notice dated 2020 and identifies the Communication and Literature Department as publisher. Its table of contents includes sections for local churches, አጥቢያ ቤተ ክርስቲያናት ኅብረት, ቀጣና, national church structures, and the national head office. The page states that it was uploaded by an individual Scribd account and displays an all-rights-reserved notice.

**Source locator:** https://www.scribd.com/document/943135783/የቃለ-ህይወት-መተዳደሪያ-ደንብ

**Evidence quality and limitations:**
- This is a third-party user-uploaded copy, not a verified EKHC-controlled publication endpoint.
- The page metadata and extracted contents do not authenticate the scan against an original signed/approved edition.
- The displayed sixth-revision date does not establish that it remains current or unamended.
- The co-present Constitution copyright notice dated 2020 does not establish a seventh edition, adoption date, or constitutional approval.
- The document's table of contents is a useful source-discovery lead, not authority to freeze the hierarchy or office mandates.
- Copyright is expressly reserved; no source text has been copied into project files.

**Updated disposition:** A potential historical/current-at-publication sixth-revision bylaw candidate is now LOCATED, but current bylaws remain MISSING / UNVERIFIED for A2 exit purposes. The seventh-edition Constitution remains MISSING / BLOCKING. The hierarchy remains unapproved. The candidate may be authenticated by comparing a complete copy against an official EKHC-issued original, adoption record, amendments, and confirmation of current force.

This finding updates G-02 from “no candidate located” to “historical sixth-revision candidate located; current authoritative edition and amendments not verified.” It does not remove the blocker.


## 14. A2 evidence refresh and gate reconciliation — 2026-11-11

**Refresh branch:** `a2/authority-provenance-refresh`  
**Parent A2 evidence branch head:** `30bcadc1367fa4dad4fd78032f68a1baf7287335`  
**Method:** Read-only repository and historical-path inspection; public-source discovery; this section records evidence and does not amend `main`, A1 source documents, or application code.

### 14.1 Repository topology and stage-state correction

A fresh repository branch listing now shows the following visible refs:

- `main`
- `a1/assessment-specification`
- `docs/a1-architecture-options-assessment`
- `docs/a1-assessment-foundation`
- `docs/a1-data-classification-privacy`
- `docs/a1-data-inventory-workbook`
- `docs/a1-hosting-sustainability-cost-assessment`
- `docs/a1-legal-regulatory-policy-assessment`
- `docs/a1-master-evidence-decision-register`
- `docs/a2-read-only-reconciliation`
- `a2/authority-provenance-refresh` (this refresh branch)
- `a3/restricted-foundation-scope`

The A3 branch now contains the Owner-accepted restricted first increment and the A4 closure record. The A4 closure-record commit is `ebe25ab828812c9b0b76fc18423b66e3e6c31d37`. Its exact-head quality workflow run #40 (ID `42971789834`) completed with conclusion SUCCESS on that SHA. Run URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42971789834

This supersedes older A2-report statements that A3 was unauthorized/not started and A4 had not started. Current gate status is: A1 OWNER-APPROVED; A2 PARTIAL / OPEN; A3 OWNER-ACCEPTED for the restricted first increment; A4 OWNER-ACCEPTED / VERIFIED-CLOSED; A5 NOT STARTED. This status correction does not close A2 or authorize A5.

### 14.2 Current official public-site corroboration — terminology only

A fresh review of the current English and Amharic pages at `https://ekhc.et/` and `https://ekhc.et/amh/` found public-facing ministry/service labels including Missions, Theological Education, Finance, Human Resource/Properties/Logistics, Communication and Literature, Discipleship/Church Education, Women, Youth, Children, Social Security Commission, Professionals, National Mobile Leadership Training, Church and Community Empowerment, and Christian Marriage/National Prayer services.

These are current public website labels as displayed during this review. They are discovery and terminology evidence only. They do not prove that each label is a constitutional department, its administrative tier, legal status, mandate, approval authority, reporting line, or relationship to another body. Website cards and English renderings must not be copied into canonical organization enums or permission scopes without approved institutional evidence.

The legacy `ekhc.net` pages remain a distinct historical/legacy source set. Their older organizational descriptions and numerical claims differ from the current `ekhc.et` presentation. The discrepancy is retained as source-version/freshness risk; no numerical organization counts or hierarchy claims are accepted.

### 14.3 Historical UI path and repository-history check

The three previously identified UI paths were checked against repository commit history using path-scoped commit queries:

- `resources/js/layouts/Header.vue`: no commits returned.
- `resources/js/styles/tokens.css`: no commits returned.
- `tailwind.config.js`: no commits returned.

The A2 evidence branch tree and the current A3 branch tree contain no frontend/UI source files. This strengthens the finding that the identified files are not present in the inspected repository history and current branch snapshots. It does not establish that the UI never existed or cannot exist in another private, deleted, transferred, unindexed, or inaccessible repository. No original UI repository, branch, commit, or owner-verified artifact has been identified.

**Disposition:** G-06 remains UNRESOLVED / HIGH. Preserve the existing UI direction; do not recreate, replace, or infer its implementation from current website appearance.

### 14.4 Additional historical structure lead — 2002

A publicly accessible academic repository document includes an appendix titled “EKHC Central Office Structure (August, 2002)”. The appendix depicts a historical central-office arrangement with General Secretary and spiritual/development leadership groupings, departments, and programs.

This is a dated secondary academic source reproducing a 2002 diagram. It is useful only as a historical lead and cannot establish current structure, current office names, current reporting lines, or current delegated authority. Its labels must not be treated as a seventh-edition constitutional interpretation or imported into the application.

**Disposition:** Historical evidence candidate recorded; no hierarchy gap closed.

### 14.5 Updated gap disposition

| Gap | Refresh evidence | Current status |
|---|---|---|
| G-01 — Seventh-edition Constitution | No authoritative seventh-edition copy or adoption/amendment record located in this refresh | BLOCKING / CRITICAL — MISSING |
| G-02 — Current bylaws and amendments | Sixth-revision third-party copy remains the only located public candidate; current force and amendment history unverified | BLOCKING / CRITICAL — UNVERIFIED |
| G-03 — Main constitutional-source conflict | Main README still requires separate controlled reconciliation against Owner-directed seventh-edition baseline | BLOCKING / MATERIAL — OPEN |
| G-04 — Hierarchy and relationships | 2002 academic diagram and sixth-revision copy are historical only; current parentage/authority cannot be inferred | BLOCKING / CRITICAL — UNRESOLVED |
| G-05 — Office mandates/reporting | Current website service labels corroborate public terminology only; no approved mandate schedule or current organogram located | BLOCKING / HIGH — UNVERIFIED |
| G-06 — UI provenance | No path-scoped commits for the three historical UI paths; no UI files in inspected A2/A3 trees; no source repo identified | UNRESOLVED / HIGH |
| G-07 — Stakeholder validation | No authorized process-owner validation evidence added | OPEN / HIGH |
| G-08 — Legal/institutional review | No qualified legal or institutional review evidence added | OPEN / HIGH |
| G-09 — Privacy/safeguarding | No current approved institutional policy or authorized operational validation added | OPEN / HIGH |
| G-10 — Technical acceptance | A3/A4 checks verify only the restricted Django foundation, not product-wide security, accessibility, offline, performance, recovery or operations | NOT TESTED / OPEN |
| G-11 — Requirements validation | Public site discovery does not validate workflows; functional and non-functional requirements remain unvalidated/unmeasured | OPEN / HIGH |

### 14.6 A2 disposition and next evidence requests

A2 remains PARTIAL / OPEN. The expanded search improved the public-source and repository-history record but did not resolve the blocking constitutional or UI dependencies. The existing recommendation for bounded evidence-review closure with blockers recorded remains an Owner decision, not an automatic status.

The following primary evidence is still required from authorized EKHC custodians:

1. Complete seventh-edition Constitution in authoritative Amharic, with cover/title page, adoption/approval record, effective date, complete articles, and amendment history.
2. Current consolidated bylaws and every effective amendment/directive, with issuing body and effective dates.
3. Current approved organizational chart and office/department mandate documents, including reporting/accountability and appointment/delegation authority.
4. Original UI source repository or archive location, exact branch/commit or release archive, and confirmation of ownership/source-of-truth.
5. Authorized process-owner contacts and approved forms/manuals for workflow validation.
6. Current privacy, safeguarding, pastoral-care, records-retention, HR, finance, communications, and security policies.
7. Qualified legal/institutional review of applicable Ethiopian legal instruments and the institution's governing documents.

Until these arrive, keep the seven governance/provenance dependencies open. Do not implement hierarchy, role/permission scopes, governance workflows, sensitive-data processing, or UI replacement based on historical or public-web evidence.

**A2 status:** PARTIAL / OPEN — evidence refresh recorded; closure not recommended as fully reconciled.  
**A3:** OWNER-ACCEPTED restricted first increment only.  
**A4:** OWNER-ACCEPTED / VERIFIED-CLOSED; exact closure-record head CI run #40 passed.  
**A5:** NOT STARTED; separate Owner authorization required.  
**Main:** unchanged. No merge, deployment, signing, publication, or production-data activity performed.
