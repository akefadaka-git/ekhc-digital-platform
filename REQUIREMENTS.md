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

- **Security:** deny by default; server-side authorization; least privilege; organization-scoped data access.
- **Privacy:** data minimization, purpose limitation, retention rules, and protected handling of sensitive personal and pastoral information.
- **Reliability:** recoverable operations, backup/restore procedures, and defined service objectives.
- **Performance:** measurable response-time and synchronization targets to be established from field conditions.
- **Accessibility:** target WCAG 2.2 AA for applicable web interfaces, subject to validation.
- **Localization:** Amharic-first content, Unicode correctness, locale-aware dates/numbers, and reviewed translations.
- **Interoperability:** documented APIs and controlled integrations; no implicit trust across systems.
- **Maintainability:** modular boundaries, automated tests, documented operations, and supported upgrade paths.

## 3. Authorization model — proposal for evaluation

Evaluate a model in which an authenticated user acts through explicit assignments to positions and authorized organizational scopes; permissions and policies determine access to resources and actions. The backend remains authoritative. The active scope must be visible to the user, and search, exports, dashboards, and background jobs must enforce the same scope rules.

This is an architecture proposal, not an approved schema. Its relationship to EKHC constitutional authority must be validated.

## 4. Requirements still to elicit

- Detailed workflows and role catalogues by verified organizational level.
- Membership lifecycle, family/household relationships, transfers and duplicate resolution.
- Governance and meeting approval paths.
- Ministry-specific workflows and safeguarding boundaries.
- Document classification, retention, archival and access rules.
- Communication consent and audience rules.
- Offline use cases, device sharing, conflict resolution and data expiry.
- Reporting definitions, data ownership and permitted aggregation.
- Integration, migration, hosting, support and sustainability requirements.

## 5. Out of scope for A1

Production code, live member data, production migrations, payment processing, autonomous decisions, deployment, signing and publication.
