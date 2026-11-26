# A1 Authoritative Source Register

**Status:** OPEN — seventh-edition constitutional source not yet obtained or verified  
**Authority rule:** The EKHC 7th-edition Constitution is the required governing baseline for this project. Older editions are historical references only where superseded. Public website and social-media material may corroborate institutional context but cannot override constitutional evidence.

## 1. Governing source required

| ID | Source | Required verification | Current status |
|---|---|---|---|
| SRC-001 | EKHC 7th-edition Constitution (Amharic authoritative edition) | Obtain complete copy; verify title page, edition, approval/adoption date, amendments, completeness, and relevant articles | MISSING — REQUIRED |
| SRC-002 | Current EKHC bylaws / መተዳደሪያ ደንብ | Verify current edition, amendments, legal status and relationship to Constitution | MISSING — REQUIRED |
| SRC-003 | Official organizational chart / approved structure | Confirm current administrative implementation against constitutional authority | NOT VERIFIED |
| SRC-004 | Official office/department mandate documents | Confirm names, responsibilities, reporting lines and delegated authority | NOT VERIFIED |
| SRC-005 | Existing UI source and design records | Identify authoritative repository, branches, commits, design files and ownership | PARTIAL — historical references recovered; current source location not established |

## 2. Public institutional corroboration (not constitutional proof)

| ID | Public source | What it can corroborate | Limitation |
|---|---|---|---|
| PUB-001 | [EKHC official Amharic website](https://ekhc.et/amh/) | Public-facing institutional identity, ministry/service labels and Amharic terminology | Does not establish constitutional hierarchy or delegated authority |
| PUB-002 | [EKHC official website](https://ekhc.et/) | Public-facing ministry/service areas and institutional context | Does not establish constitutional hierarchy or delegated authority |
| PUB-003 | [EKHC website](https://www.ekhc.net/) | Public institutional context and ministry descriptions | Must be checked for currency; not a substitute for the Constitution |
| PUB-004 | [EKHC Literature and Communication page](https://ekhc.net/literature_and_communication) | Public description of publication/circulation of church legal documents and archive work | Does not itself provide the required seventh-edition Constitution |

The public pages currently expose ministry/service labels including missions, theological education, finance, human resources/properties/logistics, communication/literature, discipleship/church education, women, youth, children, social security, professionals, leadership training, community empowerment, and marriage/prayer services. These labels are discovery inputs only. They are not approved application domains, a complete inventory, or proof of reporting lines.

Public pages on different EKHC web properties do not always present identical descriptions or counts. Treat such differences as a source-freshness and reconciliation issue; do not choose one page as the definitive organizational record.

## 3. Historical material — not governing evidence

A publicly indexed copy describes itself as the sixth-revised EKHC constitution/bylaw, 2012 E.C. It is not the required seventh edition and is not being used to approve or freeze current hierarchy, office names, or authority. Any use is limited to historical comparison after the seventh edition is obtained.

## 4. Source verification protocol

For every constitutional or bylaw claim, record:

- Exact source title and edition.
- Publisher/issuing authority and evidence of authenticity.
- Adoption/approval date and effective date.
- Amendment history and supersession status.
- Article, section, clause and printed page.
- Exact Amharic wording; translations are secondary and must be reviewed.
- The claim supported and any ambiguity or conflict.
- Reviewer and verification date.

Do not infer constitutional parentage, powers, or office hierarchy from website layout, leadership lists, seals, social posts, or historical editions.

## 5. Existing UI evidence

Prior project history identifies an existing EKHC UI foundation with references to:

- `resources/js/layouts/Header.vue`
- `resources/js/styles/tokens.css`
- `tailwind.config.js`

The earlier UI work described an Amharic-first, Ethiopian-calendar-first, mobile-first shell and shared elements such as header, active context, sidebar, footer, layouts and reusable interface components. A prior implementation note specifically referred to a header-surface token and a Header component adjustment.

**Current verification result:** attempts to fetch those exact paths from the current repository `main` branch returned GitHub 404 responses. This does not prove the work never existed; it means its current branch, commit, repository location and file contents are not established by the available remote evidence. Do not recreate, overwrite, or declare this work reconciled until its source is located and compared.

## 6. Current A1 findings

- The Owner-provided eight-step organizational chain is preserved as a discovery baseline only.
- The chain is **not verified** against the required seventh-edition Constitution.
- Public EKHC websites are useful corroborative references, not authority for constitutional structure.
- Public ministry/service labels can guide stakeholder discovery but do not prove internal organizational structure or approved software domains.
- Existing UI work is acknowledged and protected; its exact current source location remains unresolved.
- No hierarchy schema, authorization scope, database enum, API contract, or navigation tree is approved.
- A1 remains OPEN. A2 read-only reconciliation cannot be declared complete until governing sources and existing artifacts are located and reconciled.

## 7. Supplemental source verification — 2026-11-26

This section records a follow-up public-source check. It does not change the governing-source requirements above.

| Evidence ID | Candidate / observation | Verification result | Permitted use |
|---|---|---|---|
| SRC-002-CAND-001 | Third-party Scribd transcription titled `የቃለ ህይወት መተዳደሪያ ደንብ`, whose description identifies it as the EKHC bylaws revised for the sixth time in 2012 E.C. ([public transcription](https://www.scribd.com/document/943135783/የቃለ-ህይወት-መተዳደሪያ-ደንብ)) | PARTIAL — candidate located; not EKHC-hosted or independently authenticated; no evidence establishes that it is the current version or has not been superseded | Historical research lead only. Do not treat as operative bylaws or use to approve current roles, hierarchy, authority, or workflows. |
| PUB-005 | Current public English-facing EKHC page ([ekhc.et](https://ekhc.et/)) | Public page currently lists ministry/service areas and gives short descriptions for selected ministry areas | Corroborative public-facing terminology only; not an approved organogram or mandate instrument |
| PUB-006 | Current public Amharic-facing EKHC page ([ekhc.et/amh/](https://ekhc.et/amh/)) | Public page presents Amharic names for ministry/service areas and selected descriptions | Corroborative terminology only; preserve source wording and do not infer reporting lines or delegated authority |

**Constitution status:** SRC-001 remains MISSING / NOT OBTAINED from accessible public sources. No authenticated seventh-edition text, adoption record, or effective-date record was located in this check. This is not a finding that such an edition does not exist.

**Bylaws status:** SRC-002 remains REQUIRED / CURRENT VERSION UNRESOLVED. SRC-002-CAND-001 is a historical candidate only and does not satisfy the source requirement.

**Organizational mandates:** SRC-003 and SRC-004 remain NOT VERIFIED. Public website ministry/service descriptions do not establish an approved organizational chart, formal mandates, reporting lines, or delegated authority.

**UI provenance:** SRC-005 remains PARTIAL / UNRESOLVED. No exact original UI repository, branch, or commit was identified in the available repository inventory. The historical paths above remain unverified; do not reconstruct them from descriptions.

**Verification boundary:** No institutional contact was made. No source was represented as institutionally authenticated. No organizational data, hierarchy, permissions, workflow, schema, or UI implementation is approved by this supplemental note.
