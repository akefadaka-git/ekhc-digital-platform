# EKHC OS — A1 Master Evidence and Decision Register

**Status:** Consolidated working register — A1 OPEN; not Owner-approved or closed  
**Stage:** A1 assessment/specification only  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Register branch:** `docs/a1-master-evidence-decision-register`  
**Register baseline commit:** `6dfd1755a9a6461306cf107823249151cf2457d4`  
**Purpose:** Provide one navigable index of the A1 evidence, decisions, source gaps, document overlaps, conflicts, dependencies, and closure conditions.

## 1. Executive status

A1 has a substantial set of assessment documents, but evidence coverage must not be confused with validation or approval.

| Measure | Current result | Interpretation |
|---|---:|---|
| Functional requirements with at least one evidence reference | 12/12 | Traceability coverage only |
| Functional requirements fully validated | 0/12 | No authoritative and stakeholder validation completed |
| Non-functional requirements with at least one risk/decision reference | 8/8 | Traceability coverage only |
| Non-functional requirements with measured/test evidence | 0/8 | No performance, accessibility, security or operational test evidence |
| Elicitation gaps recorded | 9 | Open discovery areas |
| Constitutional dependencies verified | 0 | Seventh-edition Constitution remains missing |
| Current bylaws verified | 0 | Current bylaws remain missing |
| Historical UI source fully reconciled | No | Source repository/branch/commit unresolved |
| Legal and institutional-policy review | Not completed | Dependency domains documented; qualified review absent |
| Owner A1 approval | Pending | No closure authorization |

**Overall disposition: PARTIAL / OPEN.** The register improves navigation and consistency of A1 evidence. It does not increase validation status merely because more documents have been created.

## 2. Scope and evidence rules

1. This register indexes the current A1 working documents and their reported branch/blob identifiers.
2. The underlying assessment documents currently reside on separate branches. This register does not merge or integrate those branches.
3. Each referenced file must be re-fetched at its listed branch/ref before a future reconciliation or merge decision; the blob SHA identifies the observed file content.
4. Owner-stated constraints are valid project directions, but they are not substitutes for constitutional, legal, policy, or process-owner evidence.
5. Public institutional websites are corroborative context only.
6. Historical constitutional editions are historical research only and cannot validate current governance.
7. No real personal, pastoral, child, financial, personnel, or confidential institutional data may be used in assessment examples or test fixtures; synthetic-only remains in force.
8. No organizational hierarchy, official role, permission, retention period, lawful basis, consent rule, schema, API, or production control is approved by inclusion in this register.
9. A missing source remains MISSING; an unlocated artifact remains UNRESOLVED. A 404 or unsuccessful search does not prove that an artifact never existed.
10. No A2, A3, A4, or A5 work is authorized by this register.

## 3. A1 document inventory

The following is a cross-branch inventory. It is not a claim that all documents are present together on one branch.

| ID | Document | Branch | Observed blob SHA | Status / purpose |
|---|---|---|---|---|
| DOC-01 | `PROJECT_CHARTER.md` | `docs/a1-assessment-foundation` | `b5451115294b356487a222194210d4d09ce4790a` | Draft scope and governance |
| DOC-02 | `REQUIREMENTS.md` | `docs/a1-assessment-foundation` | `a1ddfdf3f8de8d3480ee4b9b4ee4b0d26349ad5d` | Provisional FR/NFR catalogue |
| DOC-03 | `docs/assessment/REQUIREMENTS-TRACEABILITY-MATRIX.md` | `docs/a1-assessment-foundation` | `2af477ee0d2dc217e78f7fb7f6e3309bb97fb0b5` | Requirements-to-evidence mapping |
| DOC-04 | `docs/assessment/SOURCE-REGISTER.md` | `docs/a1-assessment-foundation` | `ad77bad452a4b42b47daf7507a57aa9cde0d30c0` | Governing source inventory |
| DOC-05 | `docs/assessment/UI-RECONCILIATION-REGISTER.md` | `docs/a1-assessment-foundation` | `4b75b2adf5f2fe0d1e1d55237c8020ade5a7aebf` | Preserve and locate existing UI |
| DOC-06 | `docs/assessment/RISK-AND-DEPENDENCY-REGISTER.md` | `docs/a1-assessment-foundation` | `30c64e5b1bb51912e4cfa353301ed6df38ce1206` | Initial risks R-001..R-014 |
| DOC-07 | `docs/decisions/DECISION-LOG.md` | `docs/a1-assessment-foundation` | `35f53ad01f227086db2486b21a84fc641cf8780e` | Owner constraints and decisions |
| DOC-08 | `docs/assessment/DATA-CLASSIFICATION-AND-PRIVACY-ASSESSMENT.md` | `docs/a1-data-classification-privacy` | `b2c3f45f6f46b7f2e9b9bd6978426ba99c737b3a` | Draft C0–C3 data handling assessment |
| DOC-09 | `docs/assessment/DATA-INVENTORY-AND-STAKEHOLDER-VALIDATION-WORKBOOK.md` | `docs/a1-data-inventory-workbook` | `b5f253d2f3b9ef4c64298dac3c35c25d78e53548` | Workflow/data discovery instrument |
| DOC-10 | `docs/assessment/A1-ARCHITECTURE-OPTIONS-AND-DECISION-ASSESSMENT.md` | `docs/a1-architecture-options-assessment` | `aaa01d5f1e49f869e0e57359a8f06c26d0307b75` | Architecture alternatives and preliminary ADRs |
| DOC-11 | `docs/assessment/A1-HOSTING-SUSTAINABILITY-AND-TCO-ASSESSMENT.md` | `docs/a1-hosting-sustainability-cost-assessment` | `2141a6a45675418b892dcb57c52e4514bc3aa475` | Hosting models, TCO and continuity |
| DOC-12 | `docs/assessment/A1-LEGAL-REGULATORY-AND-INSTITUTIONAL-POLICY-ASSESSMENT.md` | `docs/a1-legal-regulatory-policy-assessment` | `c546bd1373c1d59751758f3b057af84388775811` | Legal/institutional dependency map |

**Important:** DOC-01 through DOC-07 are identified from the A1 foundation branch; DOC-08 through DOC-12 are on separate assessment branches. Their observed blob SHAs do not establish that those files are integrated into main or into the A1 foundation branch.

## 4. Canonical evidence and authority register

| Evidence ID | Evidence / source | Current status | What it can establish |
|---|---|---|---|
| EV-001 | Owner-provided project scope, stage gates and constraints | OWNER-DIRECTED | Project boundaries and operating constraints |
| EV-002 / SRC-001 | EKHC seventh-edition Constitution, authoritative Amharic edition | MISSING — BLOCKING | Current institutional authority, structure and source terminology |
| EV-003 / SRC-002 | Current bylaws and amendments | MISSING — BLOCKING | Current detailed governance rules |
| EV-004 / SRC-003..004 | Approved structure and office mandates | NOT VERIFIED | Operational structure and delegated responsibilities |
| EV-005 / SRC-005 | Existing UI source/design repository, branch and commit | UNRESOLVED | Provenance and preservation of historic UI work |
| EV-006 | Authorized process-owner and stakeholder evidence | MISSING | Actual workflows, exceptions and data purposes |
| EV-007 | Current privacy, safeguarding, pastoral, records and security policies | MISSING | Institutional data-handling controls |
| EV-008 | Applicable Ethiopian legal instruments and qualified legal review | NOT REVIEWED | Legal applicability and obligations |
| EV-009 | Content ownership/licence/permission records | MISSING | Rights to store, reproduce, distribute or adapt content |
| EV-010 | Hosting contracts, location, processor terms and operating capacity | NOT VERIFIED | Production hosting suitability and continuity |
| EV-011 | Finance, procurement, audit and entity-specific policies | MISSING | Financial controls and accountability |
| EV-012 | Accessibility, language and translation policies | NOT VERIFIED | Formal acceptance criteria beyond Owner direction |
| EV-013 | Measured technical tests and representative device/network evidence | NOT TESTED | Performance, reliability, accessibility and offline feasibility |

### Authority rule

The seventh-edition Constitution and current bylaws are the required governing baseline. Historical editions and public websites cannot replace them. Public web content may corroborate institutional context but cannot independently authorize product hierarchy, roles, or permissions.

## 5. Decision register consolidation

The following decisions are safe to carry forward as project constraints or explicit unresolved boundaries. They do not authorize implementation.

| Decision ID | Decision / constraint | Status | Evidence / dependency |
|---|---|---|---|
| D-001 | Canonical repository is `akefadaka-git/ekhc-digital-platform` | CONFIRMED | Owner direction and repository identity |
| D-002 | EKHC OS is independent of ARNA/MASES, MaaleNex and IROKA | OWNER-DIRECTED | Project scope |
| D-003 | Work remains A1 until explicit Owner approval | OWNER-DIRECTED | Stage-gate governance |
| D-004 | No merge, deployment, signing, publication or production implementation without separate authorization | OWNER-DIRECTED | Approval boundary |
| D-005 | Seventh-edition Constitution is the required governing baseline | OWNER-DIRECTED / SOURCE MISSING | SRC-001 |
| D-006 | Older constitutional editions are historical only | OWNER-DIRECTED | Source authority rule |
| D-007 | Official websites are corroborative, not constitutional proof | OWNER-DIRECTED | Source register |
| D-008 | Preserve existing UI; do not recreate or overwrite it | OWNER-DIRECTED | UI reconciliation register |
| D-009 | `ቀጣና` and `ኅብረት` are distinct; do not collapse or translate them by assumption | OWNER-DIRECTED | Authoritative source confirmation still required |
| D-010 | Amharic-first and Ethiopian-calendar-first are product directions | OWNER-DIRECTED | Formal acceptance criteria remain open |
| D-011 | Use synthetic-only information during assessment and validation | OWNER-DIRECTED | Privacy and workbook controls |
| D-012 | No real sensitive institutional or personal data until lawful authority and controls are verified | INTERIM FAIL-CLOSED CONTROL | Legal/privacy assessment |
| D-013 | Architecture alternatives remain proposals; no architecture option is frozen | PROPOSED / OPEN | Architecture options assessment |
| D-014 | Hosting must be sustainable without depending on unavailable paid top-ups or deposits | OWNER CONSTRAINT / OPTIONS OPEN | Hosting assessment |
| D-015 | No vendor, provider, or data location has been approved | UNRESOLVED | Hosting and legal evidence |
| D-016 | No production schema, role model, permission scope, API contract, retention period or hierarchy tree is approved | OPEN / NOT AUTHORIZED | Constitution, policy and stakeholder dependencies |

## 6. Overlap and consolidation map

Overlaps are intentional where one document defines a control and another records its evidence. They should be cross-linked, not blindly duplicated or deleted.

| Topic | Primary document | Related documents | Consolidation treatment |
|---|---|---|---|
| Requirement definition | DOC-02 | DOC-03, DOC-01 | Keep catalogue as source; matrix references it |
| Evidence and validation | DOC-03 | DOC-04, DOC-05, DOC-09, DOC-12 | Matrix is traceability index; source/workbook/legal docs remain evidence instruments |
| Organizational authority | DOC-04 | DOC-01, DOC-05, DOC-09, DOC-12 | Constitution and bylaws remain authoritative; do not resolve from proposals |
| UI preservation | DOC-05 | DOC-01, DOC-03 | One canonical UI evidence register; no recreation |
| Risk management | DOC-06 | DOC-03, DOC-08, DOC-10, DOC-11, DOC-12 | DOC-06 remains risk ID source; specialist documents provide treatment detail |
| Data classification | DOC-08 | DOC-09, DOC-03, DOC-06, DOC-12 | Privacy assessment defines provisional classes; workbook captures dataset-level evidence |
| Workflow and dataset discovery | DOC-09 | DOC-02, DOC-03, DOC-08 | Workbook is a collection template, not stakeholder validation |
| Architecture | DOC-10 | DOC-02, DOC-03, DOC-06, DOC-08, DOC-11 | Alternatives and ADRs remain provisional pending evidence |
| Hosting/TCO | DOC-11 | DOC-06, DOC-08, DOC-10, DOC-12 | No price/provider assumptions; use institutionally verified cost and capacity evidence |
| Legal and policy | DOC-12 | DOC-03, DOC-04, DOC-06, DOC-08, DOC-09, DOC-11 | Dependency register, not legal opinion or compliance certificate |

## 7. Contradictions, material conflicts and unresolved interpretations

| ID | Issue | Evidence / observed conflict | Required disposition | Status |
|---|---|---|---|---|
| CON-01 | Main README describes the sixth revision as the current governing baseline | Earlier A1 review found main README blob `d94349c8a4050a745ce8bb229a2823c671bf4d3a` describing sixth revision as current; A1 source register requires seventh edition | Owner-directed correction or reconciliation after fresh main re-fetch; do not edit main automatically | UNRESOLVED — MATERIAL |
| CON-02 | Main contains historical sixth-revision research while A1 requires seventh edition | Historical index/analysis and third-party sixth-revision copy are not current constitutional authority | Label historical-only; do not use to freeze hierarchy | UNRESOLVED |
| CON-03 | UI references exist in prior project history, but current source path/repository is unknown | Historical paths returned 404 on checked refs; checked branches did not expose the UI implementation | Continue provenance search without recreating or overwriting | UNRESOLVED |
| CON-04 | Architecture proposals may be mistaken for approved decisions | Architecture and hosting options documents are explicitly preliminary | Mark all architecture/hosting choices PROPOSED until evidence and Owner approval | CONTROL REQUIRED |
| CON-05 | Provisional data classes may be mistaken for an approved classification policy | Privacy assessment defines C0–C3 as provisional | Keep as assessment vocabulary; do not implement access rules from it | CONTROL REQUIRED |
| CON-06 | Candidate workflows may be mistaken for confirmed offices or functions | Workbook and discovery list candidate workflows only | Require authorized process-owner validation and authority basis | CONTROL REQUIRED |
| CON-07 | Legal domains may be mistaken for confirmed statutory applicability | Legal assessment maps questions but has no qualified legal review | Record law-by-law applicability only after verified sources and counsel review | OPEN |
| CON-08 | Project progress estimates may imply validation | Document creation/coverage is not validation evidence | Report planning progress separately from validated requirement coverage | CONTROL REQUIRED |

**No conflict is resolved by this register.** In particular, it does not correct the main README or modify the A1 foundation branch.

## 8. Dependency graph and blocking sequence

| Dependency | Blocks | Required evidence / action |
|---|---|---|
| Seventh-edition Constitution | Hierarchy, office authority, terminology, governance workflows | Obtain and verify authoritative complete edition |
| Current bylaws and amendments | Detailed governance and institutional procedure | Verify current instrument and constitutional consistency |
| Approved structure and office mandates | Role/assignment workflows and accountability | Authorized institutional records |
| Stakeholder/process-owner validation | Functional workflows, exceptions and acceptance criteria | Authorized, documented sessions; synthetic examples only |
| UI source provenance | Existing UI reconciliation and preservation | Repository, branch, commit, ownership and source files |
| Legal review | Privacy, safeguarding, records, finance, communications, hosting and content rights | Qualified review of current authoritative instruments |
| Approved institutional policies | Retention, disclosure, consent, access and safeguarding controls | Current policy versions and approving authority |
| Hosting evidence | TCO, provider choice, continuity and operational readiness | Actual quotes, payment/renewal path, staffing, backup/DR evidence |
| Owner A1 decision | A2 authorization | Explicit Owner approval after review of the complete A1 package |

## 9. A1 completion checklist

- [ ] Verify the complete seventh-edition Constitution and record relevant provisions.
- [ ] Verify current bylaws and amendments.
- [ ] Verify current structure, office mandates and delegated authority.
- [ ] Resolve the main README historical-edition conflict through an Owner-directed decision.
- [ ] Locate and reconcile the existing UI source without recreating it.
- [ ] Validate each candidate workflow with an authorized process owner.
- [ ] Validate all 12 functional requirements against authoritative and stakeholder evidence.
- [ ] Validate all 8 non-functional requirements with testable criteria and evidence plans.
- [ ] Complete qualified legal review of applicable laws and regulatory instruments.
- [ ] Verify institutional privacy, safeguarding, pastoral, records, finance, personnel, communications, security and content-rights policies.
- [ ] Validate data inventory and classification using synthetic examples; approve no real data processing until lawful authority and controls are confirmed.
- [ ] Reconcile architecture and hosting options against verified constraints, operating capacity and cost evidence.
- [ ] Resolve or explicitly accept each material risk and contradiction with authority recorded.
- [ ] Review the consolidated A1 baseline and approve it explicitly as Owner.

## 10. Work deliberately not performed

- No main-branch edits.
- No changes to existing assessment documents on their source branches.
- No branch merges or PR creation.
- No A2 read-only reconciliation stage started.
- No A3 implementation, migrations, schemas, APIs, permissions or production code.
- No A4 verification or A5 deployment readiness.
- No real data collection, procurement, account creation, hosting selection or deployment.
- No constitutional, legal or institutional policy conclusion invented.

## 11. Next authorized decision point

The next decision point is **A1 package review**, not implementation. The Owner may review this register alongside the source documents and decide whether to:
- direct specific corrections to the assessment documents;
- resolve the main-branch historical-edition conflict;
- commission or record authoritative constitutional, legal and stakeholder evidence; or
- approve the A1 baseline only after the blocking criteria are satisfied.

**Current conclusion:** A1 documentation is consolidated at index level. A1 evidence validation remains PARTIAL; constitutional authority, legal applicability, stakeholder validation and UI provenance remain unresolved. A1 is OPEN and NOT APPROVED.
