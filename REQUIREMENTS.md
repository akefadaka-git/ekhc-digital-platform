# EKHC OS Requirements Catalogue

**Status:** A1 draft; requirements are provisional and require stakeholder validation.

## 1. Product requirements

| ID | Requirement | Priority | Acceptance direction |
|---|---|---|---|
| FR-001 | Support EKHC's verified organizational structure and official terminology | MUST | Every organization record and navigation path maps to approved constitutional definitions |
| FR-002 | Support people, membership and authorized user identities as distinct concepts | MUST | Membership and login identity are not conflated |
| FR-003 | Support office, ministry and leadership assignments with effective dates and scope | MUST | Assignment history is traceable and authority is scope-bound |
| FR-004 | Support governance meetings, agendas, minutes, resolutions and decisions | MUST | Records have provenance, authorization and audit history |
| FR-005 | Support controlled document and records management | MUST | Access, version, retention and download are policy-controlled |
| FR-006 | Support communication and announcements by authorized organizational scope | SHOULD | Audience is resolved from approved scope and permissions |
| FR-007 | Support education, training and ministry workflows | SHOULD | Content and participation are permissioned and attributable |
| FR-008 | Support multilingual content with Amharic-first UX | MUST | Core workflows have Amharic labels and locale-aware rendering |
| FR-009 | Support Ethiopian calendar dates as the default | MUST | Date input, display, sorting and export are calendar-consistent |
| FR-010 | Support offline-capable workflows and controlled synchronization | MUST | Approved offline use cases work without connectivity and reconcile safely |
| FR-011 | Support web, Android, iOS and PWA access | SHOULD | Channel scope is validated against user needs and delivery cost |
| FR-012 | Provide audit trails for sensitive reads and state-changing actions | MUST | Audit records are attributable, tamper-resistant and reviewable |

## 2. Non-functional requirements

| ID | Quality attribute | Requirement | Acceptance direction |
|---|---|---|---|
| NFR-001 | Security | Deny by default; server-side authorization; least privilege; organization-scoped data access | Every protected request is authorized server-side against the verified actor, action, resource and scope; negative tests demonstrate denial |
| NFR-002 | Privacy | Data minimization, purpose limitation, retention rules, and protected handling of sensitive personal and pastoral information | Approved data inventory, purpose/basis, access, retention and deletion rules exist before live sensitive data is processed |
| NFR-003 | Reliability | Recoverable operations, backup/restore procedures, and defined service objectives | Approved service objectives and tested backup/restore and recovery procedures |
| NFR-004 | Performance | Measurable response-time and synchronization targets to be established from field conditions | Baselines and percentile targets agreed after representative field/device/connectivity measurement |
| NFR-005 | Accessibility | Target WCAG 2.2 AA for applicable web interfaces, subject to validation | Accessibility review and automated/manual test evidence for agreed critical journeys |
| NFR-006 | Localization | Amharic-first content, Unicode correctness, locale-aware dates/numbers, and reviewed translations | Reviewed language glossary and test coverage for input, display, search, sort, notifications and exports |
| NFR-007 | Interoperability | Documented APIs and controlled integrations; no implicit trust across systems | Approved interface contracts, authentication, authorization, data-sharing and error-handling rules |
| NFR-008 | Maintainability | Modular boundaries, automated tests, documented operations, and supported upgrade paths | Approved architecture boundaries, CI/test strategy, operational runbooks and dependency lifecycle policy |

## 3. Authorization model — proposal for evaluation

Evaluate a model in which an authenticated user acts through explicit assignments to positions and authorized organizational scopes; permissions and policies determine access to resources and actions. The backend remains authoritative. The active scope must be visible to the user, and search, exports, dashboards, and background jobs must enforce the same scope rules.

This is an architecture proposal, not an approved schema. Its relationship to EKHC constitutional authority must be validated.

## 4. Requirements still to elicit

The following are discovery gaps, not approved functional requirements:

| Gap ID | Topic requiring elicitation | Evidence needed |
|---|---|---|
| GAP-001 | Detailed workflows and role catalogues by verified organizational level | Constitution/bylaws, process-owner interviews, approved process documents |
| GAP-002 | Membership lifecycle, household relationships, transfers and duplicate resolution | Approved registers, data dictionary, process-owner validation and privacy review |
| GAP-003 | Governance and meeting approval paths | Constitutional clauses, bylaws, approved meeting rules, minutes templates |
| GAP-004 | Ministry-specific workflows and safeguarding boundaries | Ministry mandates, safeguarding policies and authorized stakeholder validation |
| GAP-005 | Document classification, retention, archival and access rules | Records policy, legal requirements, approved retention schedule |
| GAP-006 | Communication consent and audience rules | Communication policy, consent basis, approved audience and publication rules |
| GAP-007 | Offline use cases, device sharing, conflict resolution and data expiry | Field studies, device/connectivity profile, workflow-level sync decisions |
| GAP-008 | Reporting definitions, data ownership and permitted aggregation | Approved report templates, metric definitions, data owners and disclosure rules |
| GAP-009 | Integration, migration, hosting, support and sustainability requirements | System inventory, interface owners, data quality review, hosting and operating-cost assessment |

## 5. Out of scope for A1

Production code, live member data, production migrations, payment processing, autonomous decisions, deployment, signing and publication.

## 6. Baseline control

Requirement IDs are stable traceability identifiers. Changes to requirement wording, priority or acceptance direction must be recorded in the decision log and reflected in `docs/assessment/REQUIREMENTS-TRACEABILITY-MATRIX.md`. A requirement is not approved merely because it has an ID or appears in the matrix.
