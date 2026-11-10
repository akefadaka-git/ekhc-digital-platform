# A1 Assessment Plan

**Status:** Draft  
**Purpose:** Define the evidence and decisions required before EKHC OS architecture and scope can be frozen.

## Workstreams

### A1.1 — Institutional and governance assessment
- Identify authoritative EKHC constitutional, governance, administrative, and policy documents.
- Establish the official organizational hierarchy, level names, responsibilities, and reporting relationships from those sources.
- Verify role names, appointment/delegation rules, approval paths, and decision rights.
- Do not infer or invent organizational levels.

### A1.2 — Existing digital work reconciliation inventory
- Locate existing EKHC UI designs, prototypes, repositories, documents, and operational tools.
- Record ownership, technology, current status, source links, and reuse constraints.
- Preserve existing work; no replacement or destructive changes during assessment.

### A1.3 — Stakeholder and workflow assessment
- Map stakeholder groups and their responsibilities.
- Identify core workflows across governance, organization, membership, ministries, communications, education, and administration.
- Capture exceptions, approvals, records, and audit requirements.

### A1.4 — Context and operating constraints
- Assess connectivity, device capability, power reliability, language, accessibility, and support capacity across target operating contexts.
- Validate offline requirements, synchronization expectations, and data-loss tolerance.
- Validate Ethiopian calendar behavior and Gregorian preference requirements.

### A1.5 — Security, privacy, and risk assessment
- Identify data classes, lawful/organizational purpose, retention, access, disclosure, and incident handling requirements.
- Define organization-scoped access principles and audit expectations.
- Threat-model account compromise, privilege escalation, device loss, synchronization abuse, and insider misuse.

### A1.6 — Technical options assessment
- Compare modular monolith and other viable architectures against team capability, maintainability, cost, hosting constraints, and scale.
- Validate candidate frontend, backend, database, mobile, and offline approaches.
- Avoid selecting technology solely because it was used in an unrelated project.

## Required outputs

1. Source register with document title, issuing authority, date/version, location, and verification status.
2. Confirmed organizational hierarchy and terminology matrix.
3. Stakeholder and workflow catalogue.
4. Functional and non-functional requirements with priorities and acceptance criteria.
5. Existing-work inventory and preservation/reconciliation plan.
6. Proposed architecture and technology decision record.
7. Security/privacy threat and risk register.
8. Dependency, assumption, constraint, and open-decision register.
9. A1 review package and explicit Owner approval record.

## Exit criteria

A1 cannot be marked complete or frozen while authoritative hierarchy, core scope, data stewardship, security boundaries, or material operating assumptions remain unresolved.
