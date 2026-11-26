# A1 Baseline Consistency Review

**Status:** READ-ONLY REVIEW COMPLETE — findings recorded; no source specification approved or frozen  
**Review date:** 2026-11-26  
**Reviewed branch snapshot:** `docs/a1-assessment-foundation` at `608409645f63544fed44e5430c258cd5dcbe36b7`  
**Review scope:** `REQUIREMENTS.md`, `ARCHITECTURE.md`, `SECURITY.md`, and their A1 evidence/traceability dependencies  
**Change boundary:** This memo is additive documentation only. The three source specifications and existing evidence records were not edited.

## 1. Executive result

The three baseline documents are directionally consistent in describing an A1 proposal rather than an approved implementation baseline. They repeatedly defer constitutional structure, domain ownership, technology choices, data models and deployment decisions pending authoritative evidence and explicit Owner approval.

The main issue is not a demonstrated contradiction in the proposed system shape. It is **normative ambiguity and insufficiently testable detail**: some requirement priorities and security controls read like mandatory commitments even though their approval status is provisional; several acceptance directions are not yet observable tests; and important dependencies are not yet translated into concrete evidence/decision records.

**Disposition:** Keep all three documents provisional. Do not freeze architecture, schema, roles, permissions, workflows, hosting, or security controls on the strength of these drafts.

## 2. Findings requiring attention

### F-01 — Draft priorities can be mistaken for approved obligations
- **Severity:** HIGH
- **Locations:** `REQUIREMENTS.md` sections 1–2 and 6; `docs/assessment/REQUIREMENTS-TRACEABILITY-MATRIX.md`
- **Finding:** The catalogue marks FR-001–FR-005, FR-008–FR-010 and FR-012 as MUST, and labels several non-functional requirements as quality requirements. The document does say the catalogue is provisional, while the traceability matrix correctly records 0/12 functional requirements as authoritatively/stakeholder validated and 0/8 non-functional requirements as measured/tested.
- **Risk:** Readers may treat MUST as an approved scope commitment despite the explicit A1 draft status.
- **Recommended disposition:** In a future controlled revision, define MUST/SHOULD as *proposed prioritization for elicitation*, not approved delivery commitments, until the Owner approves the requirements baseline. Keep current traceability statuses unchanged.

### F-02 — Acceptance directions are not yet testable acceptance criteria
- **Severity:** HIGH
- **Locations:** `REQUIREMENTS.md` FR-001–FR-012 and NFR-001–NFR-008
- **Finding:** Several acceptance directions use broad terms such as “verified,” “authorized,” “controlled,” “traceable,” “recoverable,” and “consistent” without defining measurable outcomes, actors, preconditions, exception paths or evidence. For example, FR-001 does not yet define how each organizational relationship is tested; FR-004 does not specify the distinct meeting/decision states and approval evidence; FR-005 does not specify records lifecycle outcomes.
- **Risk:** Requirements could be declared complete based on subjective interpretation, or implementation could encode unverified institutional practice.
- **Recommended disposition:** After source and stakeholder validation, split broad requirements into workflow-level acceptance scenarios with actor, trigger, preconditions, normal path, exceptions, authorization source, records produced and observable pass/fail criteria. Do not invent those scenarios now.

### F-03 — Constitutional and mandate dependencies correctly block hierarchy-dependent design
- **Severity:** CRITICAL
- **Locations:** `REQUIREMENTS.md` FR-001, FR-003 and GAP-001; `ARCHITECTURE.md` sections 1–4 and 6–7; `docs/organization/HIERARCHY-AND-TERMINOLOGY.md`; `docs/assessment/SOURCE-REGISTER.md`
- **Finding:** The source register still records the seventh-edition Constitution as missing from accessible public sources, current bylaws as unresolved, and approved structure/office mandates as unverified. The Owner-provided eight-step chain is explicitly a discovery baseline, not a constitutional schema.
- **Risk:** Prematurely turning candidate domains, organizational scopes, assignments or navigation into tables, enums, permissions or application behavior would hard-code unverified authority.
- **Recommended disposition:** Maintain the current block. A later read-only reconciliation must cite exact authoritative clauses and current mandate instruments. Preserve the distinction between `ቀጣና` and `ኅብረት`; neither public ministry labels nor the unauthenticated historical bylaws candidate can close this dependency.

### F-04 — Candidate architecture boundaries need ownership and boundary tests
- **Severity:** MEDIUM
- **Locations:** `ARCHITECTURE.md` sections 2–3 and 6
- **Finding:** The candidate logical domains and modular-monolith/API-driven shape are explicitly provisional. However, no domain ownership, source-of-truth rules, cross-domain invariants, transaction boundaries, event contracts or integration trust boundaries are defined.
- **Risk:** Domain names may be mistaken for an approved module inventory, and future implementation may duplicate ownership or create unsafe cross-domain coupling.
- **Recommended disposition:** Retain the candidate list as a discussion aid only. Once process owners and systems are known, produce a domain/context map with accountable owner, authoritative records, invariants, interfaces, data classification and failure behavior. No technology or deployment choice is implied by this review.

### F-05 — Security baseline mixes control objectives with underspecified implementation choices
- **Severity:** HIGH
- **Locations:** `SECURITY.md` “Minimum design requirements”; `REQUIREMENTS.md` NFR-001–NFR-002; `ARCHITECTURE.md` section 4
- **Finding:** The draft lists encryption at rest, tamper-evident audit, multi-factor authentication options, effective-dated assignments, secure recovery and other controls, but does not yet define threat coverage, assurance level, key custody/rotation, audit integrity/verification, privileged-access lifecycle, emergency access, or measurable control tests.
- **Risk:** A checklist could be mistaken for a complete threat model or proof of security; controls may be implemented without a coherent threat and data-classification basis.
- **Recommended disposition:** Treat these as proposed control objectives pending a threat model and data classification. For each control, record threat, asset/data class, trust boundary, control owner, verification method, residual risk and exception path. No security certification or production readiness should be inferred.

### F-06 — Privacy and safeguarding dependencies need to precede collection and feature design
- **Severity:** CRITICAL
- **Locations:** `SECURITY.md` threat scenarios/A1 work required; `REQUIREMENTS.md` NFR-002 and GAP-002/GAP-004/GAP-005/GAP-006; risk register R-005/R-006
- **Finding:** The documents correctly recognize personal, pastoral, child/safeguarding, personnel and governance information as sensitive. The required data inventory, purpose/legal-basis review, classification, retention, guardian/consent, disclosure and incident rules remain unassessed.
- **Risk:** Data fields, analytics, notifications, exports, offline caches or access patterns could be designed before lawful purpose and handling constraints are known.
- **Recommended disposition:** Do not ingest live sensitive records or define detailed collection fields. Complete the approved data inventory/classification and privacy/safeguarding review before feature-level data design. Continue using synthetic or properly anonymized examples only.

### F-07 — Offline architecture has sound principles but lacks workflow-level eligibility decisions
- **Severity:** HIGH
- **Locations:** `REQUIREMENTS.md` FR-010; `ARCHITECTURE.md` section 5; `SECURITY.md` threat scenarios
- **Finding:** The architecture identifies read-only cache, queued drafts and connectivity-required sensitive actions, and rejects silent last-write-wins for high-integrity records. It does not yet specify which real workflows fit each class, conflict ownership, revocation timing, shared-device controls, local key management, replay/idempotency semantics or recovery evidence.
- **Risk:** “Offline-first” could be interpreted as permission to cache or mutate sensitive governance/member data without a validated threat and process model.
- **Recommended disposition:** Keep offline support as an Owner-directed requirement but do not authorize data caching or offline state changes until field evidence, data classification and per-workflow decisions exist. Define negative tests for revoked devices, replay, stale versions, duplicate submissions, lost devices and conflicting approvals.

### F-08 — Localization, calendar and accessibility targets need scoped conformance criteria
- **Severity:** MEDIUM
- **Locations:** `REQUIREMENTS.md` FR-008–FR-009, NFR-005–NFR-006; `ARCHITECTURE.md` section 1
- **Finding:** Amharic-first and Ethiopian-calendar-first directions are recorded as Owner-directed, but the glossary, fallback language, Unicode/font behavior, conversion/time-zone rules, dual-calendar behavior and channel-specific acceptance tests remain open. WCAG 2.2 AA is described as a target subject to validation, not as audited conformance.
- **Risk:** Different clients may implement inconsistent date, search, sort, export or translated-content behavior; the accessibility target could be overstated.
- **Recommended disposition:** Develop reviewed language/date test vectors and define the applicable accessibility scope and critical journeys before claiming conformance. Preserve Owner-directed intent without treating implementation behavior as validated.

### F-09 — Channel scope is grouped too broadly for cost and support decisions
- **Severity:** MEDIUM
- **Locations:** `REQUIREMENTS.md` FR-011; `ARCHITECTURE.md` sections 3 and 6
- **Finding:** Web, Android, iOS and PWA are grouped into one SHOULD requirement, while the architecture says clients share governed application services. There is no channel-by-channel user evidence, device coverage, offline parity, support model, release/upgrade model or cost assessment.
- **Risk:** The grouped requirement may be read as a commitment to deliver and support all four channels, even though the catalogue says the channel scope must be validated.
- **Recommended disposition:** In a future revision, assess each channel separately against users, devices, connectivity, security, accessibility, operating cost and support capacity. Do not infer a delivery commitment from the candidate list.

### F-10 — Security and operational acceptance evidence is not yet represented as a verification plan
- **Severity:** HIGH
- **Locations:** `SECURITY.md` A1 work required; `REQUIREMENTS.md` NFR-001–NFR-008; `ARCHITECTURE.md` sections 4–6
- **Finding:** The documents call for threat modelling, privacy impact assessment, backup/restore, incident response, revocation, dependency management and CI/release controls, but do not define evidence artefacts, responsible reviewers, pass/fail thresholds or test environments.
- **Risk:** Future readiness claims could be based on design statements rather than verified controls.
- **Recommended disposition:** Before any A3 implementation proposal, create a control-to-evidence matrix and test strategy covering positive and negative authorization, cross-scope isolation, audit integrity, account recovery, offline/device-loss, backup restore, incident response, dependency/security scanning and release provenance. Tests must use synthetic data and approved test identities.

## 3. Cross-document consistency check

| Area | Consistency result | Review note |
|---|---|---|
| Provisional status | PASS | All three source documents label themselves draft/proposal; none claims approval or production readiness. |
| Governance dependency | PASS WITH BLOCKER | Requirements and architecture defer hierarchy/authority; source register confirms governing evidence remains unresolved. |
| Owner terminology constraints | PASS WITH CONTROL | Hierarchy register explicitly preserves `ቀጣና` and `ኅብረት` as distinct; architecture says not to freeze hierarchy. |
| Identity and authorization | PARTIAL | Person/account separation and server-side authorization are consistently proposed, but no approved authority matrix, threat model or schema exists. |
| Offline behavior | PARTIAL | High-integrity conflict principles align; workflow eligibility, device controls and sync semantics remain undefined. |
| Security/privacy | PARTIAL | Risk themes align across documents; the security list is not yet a complete threat model or testable assurance baseline. |
| Localization/accessibility | PARTIAL | Owner direction and target are recorded; acceptance scope and conformance evidence remain open. |
| Technology/deployment | PASS | Architecture explicitly leaves framework, database, hosting and topology unfrozen. |
| Traceability | PASS WITH LIMITATION | 12/12 FR and 8/8 NFR have relevant references; validation remains 0/12 FR and measured/test evidence 0/8 NFR. Trace presence is not validation. |
| Existing UI provenance | BLOCKED | Historical source remains unidentified; no UI replacement or reuse decision is supported. |

## 4. Evidence and scope boundaries retained

This review relies on the A1 evidence records as they stood at the reviewed branch snapshot:
- `docs/assessment/SOURCE-REGISTER.md`
- `docs/assessment/REQUIREMENTS-TRACEABILITY-MATRIX.md`
- `docs/assessment/RISK-AND-DEPENDENCY-REGISTER.md`
- `docs/assessment/STAKEHOLDER-WORKFLOW-DISCOVERY.md`
- `docs/assessment/UI-RECONCILIATION-REGISTER.md`
- `docs/organization/HIERARCHY-AND-TERMINOLOGY.md`

The seventh-edition Constitution was not located in accessible public sources; this does not establish that it does not exist. The third-party sixth-revision bylaws transcription remains unauthenticated and cannot establish current bylaws. Public ministry/service descriptions are corroborative only. The original UI repository/branch/commit remains unresolved. No institutional contact was made.

## 5. Recommended sequencing

1. **A1 evidence completion:** obtain and authenticate governing instruments; identify approved structure/mandates; recover original UI source provenance; identify authorized process owners and approved workflow evidence.
2. **A1 requirements refinement:** convert validated workflows into observable acceptance scenarios; separate Owner-directed requirements from proposed priorities and quality targets.
3. **A1 security/privacy assessment:** complete data classification, threat model, privacy/safeguarding review, privileged-access model, retention and incident-response requirements.
4. **A1 architecture review:** only after the above, validate domain ownership, trust boundaries, offline eligibility, integration contracts and operational model.
5. **Owner gate:** submit a reconciled A1 package for explicit review/approval. No A2, A3, merge or deployment status is implied by this memo.

## 6. Review conclusion

**A1 remains OPEN.** This review is a documentation consistency assessment, not an architecture approval, requirements validation, security audit, A2 reconciliation, implementation, or production-readiness assessment.

No source specification was edited. No requirement was promoted to VALIDATED, APPROVED, FROZEN, IMPLEMENTED or TESTED. No schema, code, workflow, permission, UI, hosting or deployment change is authorized by this memo.
