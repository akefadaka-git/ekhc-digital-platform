# A1 Requirements-to-Evidence Traceability Matrix

**Status:** Draft traceability baseline — not an approval or verification report  
**Requirements source:** `REQUIREMENTS.md` at the same branch revision  
**Scope:** Current Owner constraints, repository documents, source register, workflow discovery and risk register  
**Rule:** A trace link means that evidence is relevant to a requirement. It does not mean the requirement is validated, accepted, implemented or tested.

## 1. Traceability status definitions

| Status | Meaning |
|---|---|
| OWNER-DIRECTED | Requirement direction is present in recovered Owner decisions; detailed acceptance still needs validation |
| PARTIAL | Some relevant evidence exists, but authoritative, complete or stakeholder evidence is missing |
| UNVERIFIED | Requirement is a candidate with no sufficient validating evidence yet |
| BLOCKED | Required authoritative source or decision is missing; do not freeze the requirement or dependent design |
| PROPOSED | Quality target or architecture control is proposed for review, not yet approved |
| NOT TESTED | No implementation or test evidence exists in this A1 documentation-only stage |

## 2. Functional requirement traceability

| Requirement | Priority | Evidence references | Evidence currently available | Missing evidence / validation action | Current status |
|---|---|---|---|---|---|
| FR-001 Organizational structure and official terminology | MUST | EV-001; SRC-001–004; R-001, R-004 | Owner-provided eight-step discovery chain and terminology constraints in `docs/organization/HIERARCHY-AND-TERMINOLOGY.md` | Obtain seventh-edition Constitution, current bylaws, approved structure and office mandates; cite exact articles/pages; reconcile every level, relationship, exception and authority | BLOCKED |
| FR-002 Distinct person, membership and login identity | MUST | GAP-002; R-005, R-014; WF-02 | Requirement catalogue states the separation; workflow discovery identifies people/membership registration and transfer as candidate processes | Approved definitions, lifecycle states, identifiers, source registers, duplicate/correction process, lawful purpose and data owner | UNVERIFIED |
| FR-003 Effective-dated office, ministry and leadership assignments | MUST | EV-001; SRC-001–004; GAP-001, GAP-003; R-001, R-004, R-013; WF-03 | Owner hierarchy constraints and candidate appointment/election/delegation workflow | Constitutional/bylaw authority, approved position/office definitions, appointment evidence, terms, delegation, revocation and conflict rules | BLOCKED |
| FR-004 Governance meetings, agendas, minutes, resolutions and decisions | MUST | GAP-003; R-005, R-013; WF-13 | Candidate meeting and decision workflow documented | Official meeting types, convening authority, quorum, voting, approval, signatures, correction, retention and publication rules | PARTIAL |
| FR-005 Controlled document and records management | MUST | SRC-002, SRC-004; GAP-005; R-005, R-014; WF-12 | Candidate communication/literature and record workflow; source register identifies legal-document publication/archive context | Records classification, authoritative record status, versioning, access, retention, archival, legal hold, export and deletion policy | PARTIAL |
| FR-006 Scoped communication and announcements | SHOULD | EV-001; GAP-006; R-003, R-005; WF-12, WF-15 | Public communication/literature context; requirement proposes authorized audience scoping | Approved publication authority, consent basis, audience rules, moderation, correction/takedown and delivery-channel policies | PARTIAL |
| FR-007 Education, training and ministry workflows | SHOULD | PUB-001–004; GAP-004; R-006; WF-07–WF-11 | Public ministry/service-area labels and candidate education, discipleship, youth, children and ministry workflows | Current mandates, program-specific processes, safeguarding, learner/participant data rules and process-owner approval | PARTIAL |
| FR-008 Amharic-first multilingual UX | MUST | EV-001, EV-004; SRC-003–004; R-010; UI-005 | Owner language direction; historical UI notes indicate Amharic-first shell; public Amharic pages provide terminology context | Approved glossary, language list, translation reviewers, fallback rules, content ownership and cross-channel localization tests | OWNER-DIRECTED |
| FR-009 Ethiopian calendar default | MUST | EV-001, EV-004; R-010; UI-005 | Owner direction and historical UI notes identify Ethiopian-calendar-first behavior | Calendar conversion rules, time-zone policy, date input/display/sort/export requirements, dual-calendar policy and test vectors | OWNER-DIRECTED |
| FR-010 Offline-capable workflows and controlled synchronization | MUST | EV-001; GAP-007; R-007, R-008, R-011 | Owner offline-first direction; risk register identifies device exposure and synchronization conflicts | Field connectivity/device evidence; per-workflow offline eligibility; local data classification, encryption, expiry, revocation, idempotency and conflict rules | OWNER-DIRECTED |
| FR-011 Web, Android, iOS and PWA access | SHOULD | EV-001; GAP-009; R-011, R-012 | Owner target channel direction | User/device research, accessibility and offline parity, platform support matrix, delivery/maintenance cost and release strategy | OWNER-DIRECTED |
| FR-012 Audit trails for sensitive reads and state changes | MUST | EV-001; R-005, R-009, R-013; WF-01–WF-15 | Auditability is a stated requirement; security baseline and risk register identify privileged and sensitive actions | Audit event catalogue, actor attribution, immutable/tamper-evident storage, access review, retention, monitoring and evidence export requirements | PARTIAL |

## 3. Non-functional requirement traceability

| Requirement | Evidence references | Evidence currently available | Missing evidence / validation action | Current status |
|---|---|---|---|---|
| NFR-001 Security and authorization | EV-001; R-004, R-009; GAP-001 | Draft deny-by-default, server-side and scope-aware security direction in `SECURITY.md` and `REQUIREMENTS.md` | Constitution/bylaws-backed authority matrix; threat model; data/resource/action matrix; negative authorization tests; privileged-access and revocation policy | PROPOSED |
| NFR-002 Privacy and data protection | R-005, R-006, R-014; GAP-002, GAP-004, GAP-005 | Draft minimization and sensitive-data handling principles; identified child/safeguarding and personal-data risks | Data inventory/classification; purpose and legal-basis review; privacy impact assessment; retention/deletion schedule; consent/guardian and disclosure rules | PARTIAL |
| NFR-003 Reliability and recoverability | R-007, R-008, R-012; GAP-009 | Recovery, backup and restore are listed as quality needs; offline failure modes identified | Service objectives, backup ownership/frequency, recovery point/time objectives, restore drills, outage and sync recovery scenarios | PROPOSED |
| NFR-004 Performance | R-011, R-012; GAP-007, GAP-009 | Requirement explicitly defers targets until field conditions are known | Representative device/network measurements, workload model, latency percentiles, throughput, offline sync size/time and load-test criteria | UNVERIFIED |
| NFR-005 Accessibility | EV-004; R-010 | Accessibility target of WCAG 2.2 AA appears in current requirements; no audit evidence | Confirm target and scope; test critical Amharic journeys with automated and manual keyboard, screen-reader, contrast, focus and mobile checks | PROPOSED |
| NFR-006 Localization | EV-001, EV-004; R-010; UI-005 | Amharic-first and Ethiopian-calendar-first Owner direction; historical UI shell references | Approved terminology glossary; Unicode/input/font tests; locale-aware numbers/dates; search/sort/export/notification tests; reviewed translations | OWNER-DIRECTED |
| NFR-007 Interoperability | GAP-009; R-014 | API-driven integration direction is present in candidate architecture; no interface inventory | System/interface inventory, data owners, API contracts, identity/trust model, consent/data-sharing basis, error/retry and versioning rules | PROPOSED |
| NFR-008 Maintainability | EV-001; GAP-009; R-002, R-012, R-014 | Modular architecture and testability are proposed; existing UI preservation risk recorded | Existing source inventory; approved architecture boundaries; supported stack and lifecycle; test strategy, CI constraints, runbooks and ownership model | PROPOSED |

## 4. Elicitation-gap traceability

These gaps must be resolved before dependent requirements can be baselined.

| Gap | Affected requirements | Required evidence / decision | Current dependency |
|---|---|---|---|
| GAP-001 Verified roles and workflows by organizational level | FR-001, FR-003, FR-006, FR-012, NFR-001 | Seventh-edition Constitution, current bylaws, mandates, role/authority matrix and process-owner validation | SRC-001–004 |
| GAP-002 Membership lifecycle and identity data | FR-002, NFR-002 | Approved membership forms/registers, data dictionary, lifecycle and correction rules, privacy review | SRC-004; authorized membership process owner |
| GAP-003 Governance and meeting processes | FR-003, FR-004, FR-012 | Governing clauses, bylaws, approved meeting/voting/decision rules and templates | SRC-001–003 |
| GAP-004 Ministry and safeguarding boundaries | FR-007, NFR-002 | Ministry mandates, safeguarding policies, restricted-data rules and authorized validation | SRC-004; ministry and safeguarding owners |
| GAP-005 Records and retention | FR-005, NFR-002, NFR-003 | Records policy, retention schedule, archival and disclosure rules | SRC-002, SRC-004 |
| GAP-006 Communication consent and audience | FR-006, FR-012, NFR-002 | Publication authority, consent/notice policy, audience rules and moderation procedures | SRC-004; communications owner |
| GAP-007 Offline operation | FR-010, NFR-003, NFR-004, NFR-006 | Field survey, device/connectivity profile and per-workflow sync decisions | R-007, R-008, R-011 |
| GAP-008 Reporting and aggregation | FR-004–FR-007, FR-012, NFR-002, NFR-007 | Approved report catalogue, metric definitions, data ownership, aggregation and disclosure rules | Authorized domain owners |
| GAP-009 Integration, migration and operations | FR-011, NFR-003, NFR-004, NFR-007, NFR-008 | System inventory, data quality, interface owners, hosting/support/cost and migration assessment | SRC-005; R-011, R-012, R-014 |

## 5. Evidence register cross-reference

| Evidence ID | Evidence item | Traceability use | Reliability boundary |
|---|---|---|---|
| EV-001 | Recovered Owner decisions and constraints | Product identity, independence, language, calendar, offline/channel direction, terminology | Owner direction; not a substitute for institutional constitutional evidence |
| EV-002 / SRC-001 | EKHC 7th-edition Constitution | Organizational structure, authority, governance and role boundaries | REQUIRED; not yet supplied or verified |
| EV-003 / SRC-002 | Current bylaws | Operational rules, governance and delegated authority | REQUIRED; not yet supplied or verified |
| EV-004 / SRC-005 | Existing EKHC UI and design artifacts | UX, localization, shell and design continuity | PARTIAL; historical paths were not found on current `main`; source repository/branch unresolved |
| EV-005 | Authorized stakeholder and workflow evidence | Validated actors, processes, data and acceptance criteria | NOT YET PROVIDED |
| EV-006 / PUB-001–004 | Official public EKHC websites/pages | Public-facing identity and ministry/service-area discovery | CORROBORATIVE ONLY; cannot prove constitutional hierarchy or authority |
| R-001–R-014 | A1 risk and dependency register | Security, privacy, offline, continuity and delivery risk trace | Preliminary planning assessment; no accepted residual risks |
| WF-01–WF-15 | Candidate workflow areas in stakeholder discovery | Candidate business processes for elicitation | Not validated by authorized process owners |

## 6. Coverage summary

| Measure | Current result |
|---|---:|
| Functional requirements with at least one relevant evidence link | 12 / 12 |
| Functional requirements with authoritative or stakeholder validation complete | 0 / 12 |
| Non-functional requirements with at least one relevant risk/decision link | 8 / 8 |
| Non-functional requirements with measured/test evidence | 0 / 8 |
| Elicitation gaps explicitly tracked | 9 |
| Constitutional dependencies verified | 0 |
| Existing UI source fully reconciled | No |

**Interpretation:** 100% of the currently catalogued requirements have at least one trace reference, but this is only reference coverage. Validation coverage is not complete. No requirement is approved, implemented or tested by this matrix.

## 7. A1 exit and change-control rules

A requirement may move to **VALIDATED** only when:
1. Its source evidence is identified, current and authoritative for the claim being made.
2. The relevant authorized process owner confirms the workflow and terminology.
3. Acceptance criteria are specific, observable and testable.
4. Conflicts, assumptions, dependencies and privacy implications are recorded.
5. The Owner approves the requirement baseline at the appropriate stage gate.

A requirement may move to **APPROVED/FROZEN** only through explicit Owner approval; inclusion in this matrix is not approval. Requirements affected by SRC-001 or SRC-002 remain blocked until those sources are verified.

Implementation and test evidence must be added later without rewriting the historical A1 evidence record. Any changed requirement must retain its ID and have its revision, rationale, approver and affected trace links recorded.
