# EKHC OS — Initial Architecture Proposal

**Status:** Conceptual proposal only; subject to A1 assessment and Owner approval.

## 1. Architectural direction to evaluate

A modular monolith with explicit domain boundaries and API-driven integration is a candidate starting point. It may reduce operational complexity while preserving separation of concerns. This is not yet a final technology or architecture decision.

## 2. Candidate capability domains

- Governance and decision records
- Organization and administrative structure
- People and membership
- Ministries and service groups
- Communication and announcements
- Documents and records
- Education and training
- Operational workflows and reporting

Domain boundaries, ownership, and sequencing must be validated through stakeholder and workflow assessment.

## 3. Cross-cutting capabilities

- Identity and authentication
- Authorization and policy evaluation
- Organization-scoped context
- Audit and event history
- Search with permission filtering
- Notifications
- Offline data handling and synchronization
- Localization and calendar services
- API contracts and integration boundaries

## 4. Candidate platform characteristics

- Relational database, with PostgreSQL as a candidate requiring validation.
- Web application and installable PWA.
- Android and iOS delivery, with the implementation approach to be assessed.
- Offline-capable workflows with explicit sync state, retry, idempotency, and conflict resolution.
- Server-side authorization as the authoritative control; client-side checks are not security boundaries.
- Encryption in transit and at rest, secrets management, backup, restore, and audit controls.

## 5. Authorization model — design question

A possible conceptual relationship is:

`Person → Account → Assignment → Position → Organizational Scope → Permission → Policy → Resource → Action`

This model must be validated against official EKHC governance and delegation rules. It must not be implemented until approved. Access should be deny-by-default, least-privilege, auditable, and scoped to the user's authorized organizational responsibilities.

## 6. Non-negotiable terminology constraint

The terms **ወረዳ** and **District** must not appear as organizational concepts or labels anywhere in application surfaces, documentation, source code, schemas, APIs, reports, or analytics. The official alternative terminology and hierarchy must be derived from authoritative EKHC sources.

## 7. Open architecture decisions

- Authoritative hierarchy and scope model
- Identity proofing and account lifecycle
- Membership record ownership and duplicate resolution
- Offline data minimization and device protection
- Synchronization conflict policy
- Data residency, hosting, backup, and disaster recovery
- Language and translation governance
- Accessibility baseline and supported device matrix
- Integration requirements and API governance
- Technology stack and delivery sequencing

No architecture decision is frozen by this proposal.
