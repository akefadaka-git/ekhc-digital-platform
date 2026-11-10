# A1 Data Classification and Privacy Assessment

**Status:** Draft assessment — not legally reviewed, stakeholder-validated, or Owner-approved  
**Stage:** A1 only  
**Scope:** Information governance, privacy, and data-handling requirements for the proposed EKHC OS  
**Baseline:** Existing A1 requirements and risk register; no organizational authority or hierarchy is inferred here

## 1. Purpose and decision boundary

This assessment establishes a provisional method for classifying information and identifying privacy risks before functional requirements and architecture are frozen.

It is an assessment instrument, not a data policy, legal opinion, production security design, or authorization to collect or process real personal information.

The classification levels and handling rules below are proposals for review. They do not establish who within EKHC may access a record. Access authority must be derived from verified governing documents, approved policies, and authorized process-owner decisions.

No production database schema, role catalogue, permission scope, retention period, data export entitlement, or offline synchronization policy is approved by this document.

Where organizational scope is referenced in future assessment records, preserve ቀጣና and ኅብረት as distinct source-defined terms. Do not collapse them, infer a parent-child relationship beyond verified constitutional provisions, or introduce unverified translations.

## 2. Assessment principles

1. **Purpose limitation:** collect information only for a defined, authorized church or operational purpose.
2. **Data minimization:** collect the least information necessary for that purpose.
3. **Source accountability:** identify the authoritative source, record owner, and responsible process for each information set.
4. **Need-to-know access:** access must be justified by an authorized task, not merely by seniority, convenience, or possession of a device.
5. **Separation of duties:** sensitive approvals and financial controls must not depend on one unrestricted account.
6. **Confidentiality by default:** personal, pastoral, personnel, child-related, safeguarding, and sensitive governance information must not be treated as ordinary internal content.
7. **Lifecycle control:** creation, correction, access, disclosure, export, retention, archival, and disposal must be governed and auditable.
8. **Offline minimization:** local devices should hold only the minimum data needed for an approved offline workflow.
9. **Accountability:** access and material changes must be attributable to an authenticated actor and recorded in an audit trail.
10. **No inference:** do not infer consent, authority, membership status, family relationships, pastoral status, or eligibility from incomplete data.

## 3. Provisional information classification

The following four classes are proposed for assessment. They are not yet approved policy labels.

| Class | Description | Illustrative examples | Provisional handling |
|---|---|---|---|
| C0 — Public | Information explicitly approved for unrestricted public release | Public service times, approved public announcements, published contact channels | Public distribution may be permitted after publication approval; preserve source and publication status |
| C1 — Internal | Routine non-public operational information whose disclosure would cause limited harm | General internal notices, non-sensitive schedules, approved operational guidance | Authenticated access; limit distribution to the relevant work context |
| C2 — Confidential | Personal or organizational information whose disclosure could cause meaningful harm, embarrassment, financial loss, or unfair treatment | Member contact details, ordinary membership records, staff records, internal meeting minutes, non-public financial records | Restricted access by approved purpose; controlled export; access and changes logged |
| C3 — Highly restricted | Information whose exposure could create serious personal, safeguarding, pastoral, legal, financial, or institutional harm | Child-related records, safeguarding reports, pastoral-care notes, sensitive allegations, identity evidence, credentials, security secrets, high-risk personnel matters | Explicitly authorized access; strong authentication; tightly limited disclosure; no general offline caching; enhanced audit and incident handling |

### Classification rules

- Classify each dataset and, where necessary, individual fields; a record may contain fields at different levels.
- When classification is uncertain, apply the more protective class until an authorized review resolves the uncertainty.
- Public availability of one field does not make the complete record public.
- A user's church membership or organizational affiliation does not by itself authorize access to another person's information.
- Combining individually low-risk fields may create a higher-risk profile; assess re-identification and inference risk.
- C3 examples are risk indicators, not a claim that every such record is currently collected or that a specific EKHC department owns it.

## 4. Candidate information inventory for discovery

This inventory identifies information categories to investigate. It does not confirm that EKHC currently maintains each category or authorize importing it.

| Information area | Candidate information | Initial classification assumption | Evidence required |
|---|---|---|---|
| People and membership | Names, contact details, membership status, dates, transfers, household links | C2; selected identity or sensitive fields may be C3 | Official record sources, purpose, correction process, access authority |
| Leadership and assignments | Appointments, terms, election evidence, delegations, handovers | C2; disputed or sensitive matters may be C3 | Governing provisions, approved records, authorized custodians |
| Governance | Agendas, minutes, resolutions, votes, deliberations, attendance | C1–C3 depending on content | Meeting rules, publication status, record custodian, disclosure rules |
| Finance | Budgets, receipts, payments, bank details, payroll, audit records | C2–C3 | Finance policy, approval matrix, segregation of duties, retention and audit rules |
| Personnel | Recruitment, employment, compensation, performance, leave | C2–C3 | HR authority, employment requirements, access and retention rules |
| Pastoral care | Care requests, counselling notes, referrals, prayer requests | C3 by default pending policy review | Pastoral confidentiality policy, disclosure exceptions, responsible care authority |
| Children and youth | Identity, guardian details, attendance, health or safeguarding information | C3 by default | Safeguarding policy, guardian/consent requirements, access and incident procedures |
| Education and training | Enrollment, attendance, assessment, credentials | C1–C2; minors' or sensitive records may be C3 | Recognized institutions, credential authority, learner privacy and retention |
| Property and assets | Asset registers, custody, location, procurement, security details | C1–C2; security-sensitive details may be C3 | Asset custodian, financial controls, disclosure and retention rules |
| Communication | Announcements, recipient lists, subscriptions, messages | C0–C2; private messages may be C3 | Publication approval, consent/preferences, audience and retention rules |
| Technical identity and audit | Account identifiers, authentication events, device/session data, security logs | C2–C3 | Security purpose, access restrictions, retention, incident response |
| Public content | Approved public documents, public service information | C0 only after publication approval | Publisher, approval evidence, version and withdrawal process |

For each confirmed dataset, A1 discovery must record: source system or document, data owner/custodian, purpose, data subjects, fields, classification, authority, collection method, recipients, access basis, retention rule, correction route, export needs, offline need, integration, and evidence reference.

## 5. Special handling requirements

### 5.1 Children and safeguarding

- Treat child-related and safeguarding records as C3 by default.
- Do not include such records in general membership search, bulk export, broad reports, or routine notifications.
- Establish verified safeguarding policies and authorized roles before defining workflows.
- Confirm guardian/consent requirements, age-related rules, disclosure exceptions, referral processes, incident escalation, and record retention with authorized EKHC representatives and qualified legal/safeguarding reviewers.
- Do not use identifiable child records in demonstrations, testing, or discovery samples.

### 5.2 Pastoral and care information

- Treat counselling, pastoral-care notes, sensitive prayer requests, allegations, and care referrals as C3 by default.
- Separate care records from general membership profiles unless a documented, authorized purpose requires a minimal reference.
- Do not expose sensitive care details in general notifications, dashboards, search indexes, analytics, or exports.
- Define emergency disclosure and safeguarding escalation only from approved policy and legal review; do not invent exceptions.

### 5.3 Finance and personnel

- Treat personal compensation, payroll, bank/payment details, disciplinary records, and sensitive personnel matters as C3 or C2 according to a documented field-level assessment.
- Validate maker/checker controls, approval thresholds, reconciliations, conflict-of-interest handling, and audit access with authorized finance and personnel process owners.
- Do not treat an audit role as blanket permission to view unrelated personal or pastoral records.

### 5.4 Identity, credentials, and security records

- Never store plaintext passwords, recovery secrets, private keys, or authentication tokens in ordinary business records, logs, exports, or analytics.
- Keep authentication secrets separate from profile and membership information.
- Restrict security logs and incident evidence; redact secrets and unnecessary personal information.
- Define account recovery, identity verification, revocation, and privileged-access review before production authorization.

## 6. Access and disclosure assessment

The following are proposed control requirements, not a role or permission model.

- Every access decision must be enforced server-side and evaluated against an approved actor, purpose, record scope, action, and current assignment.
- The client must not be trusted to declare its own role, organization scope, or permission.
- Read, create, update, correct, approve, delete, search, export, print, share, synchronize, and administer are distinct actions to assess.
- Bulk access and export require a separate justification and approval path proportionate to the classification.
- Privileged access must be limited, attributable, periodically reviewed, and revocable.
- Delegation and temporary access must have an approver, reason, scope, start/end time, and audit record.
- Access to C3 information must be individually justified and reviewed; shared accounts are not acceptable for attributable access.
- Reports and analytics must aggregate or de-identify data where individual-level detail is not necessary.
- Record correction must preserve accountability and required history; do not silently overwrite authoritative records.
- Disclosure to external organizations or service providers requires documented purpose, authority, safeguards, and agreement review.

The exact actors, offices, authority chains, and scopes remain UNVERIFIED until the seventh-edition Constitution, applicable bylaws, approved policies, and current mandates are reconciled.

## 7. Offline, synchronization, and device handling

Offline-first is a target requirement, not permission to cache every dataset.

Provisional handling proposal:

| Class | Offline proposal | Conditions |
|---|---|---|
| C0 | May be available offline | Approved public content only |
| C1 | Limited offline use may be considered | Device protection, user authentication, expiry, and controlled synchronization |
| C2 | Disabled by default; exception requires explicit assessment | Minimum fields, encrypted storage, short retention, device binding where feasible, remote revocation and audit |
| C3 | No routine offline cache | Any exceptional offline workflow requires a separate documented threat assessment and explicit authorization |

Required assessment topics:

- Shared-device and device-loss scenarios.
- Local database encryption and key protection.
- Screen lock, session expiry, re-authentication, and app-switcher exposure.
- Local notification content and preview privacy.
- Cache minimization, expiry, deletion, and logout behavior.
- Remote revocation and lost-device response.
- Sync authentication, transport protection, idempotency, conflict handling, and audit.
- Whether a workflow can safely be read-only offline.
- Whether queued writes could cause harm if delayed, duplicated, or submitted by a revoked user.

No offline eligibility is approved for any real personal or sensitive dataset by this document.

## 8. Retention, correction, archival, and disposal

No retention periods are assigned here. They must be derived from verified legal requirements, governing documents, approved EKHC records policy, operational necessity, and any applicable safeguarding or financial obligations.

For each dataset, determine:

1. The event that starts the retention period.
2. The authorized retention owner and approved duration.
3. Whether legal hold, investigation, audit, or safeguarding rules suspend disposal.
4. What is retained in the primary system, backups, exports, attachments, logs, and offline devices.
5. How correction requests are received, verified, approved, and recorded.
6. How archival preserves authenticity, provenance, access restrictions, and retrieval.
7. How disposal is securely performed and evidenced.
8. How deletion from active systems interacts with backup expiry and legal obligations.

Do not promise erasure or retention periods until the applicable rules are confirmed.

## 9. Privacy impact and risk review triggers

A documented privacy impact assessment should be required before any proposed workflow:

- Processes C3 information or large volumes of C2 personal information.
- Involves children, safeguarding, pastoral care, allegations, health, or other highly sensitive matters.
- Introduces identity matching, profiling, automated scoring, biometrics, location tracking, or consequential automated decisions.
- Shares information across organizational boundaries or with external providers.
- Adds bulk search, export, analytics, public directories, or broad reporting.
- Introduces offline storage on personal or shared devices.
- Migrates legacy records or links datasets that were previously separate.
- Uses a new integration, hosting provider, AI service, or cross-border processing arrangement.
- Changes the purpose, audience, retention, or access model of an existing dataset.

Each review must identify necessity, proportionality, risks to data subjects, mitigations, residual risks, approvers, and unresolved issues. High-risk processing must not proceed while material safeguards or authority remain unresolved.

## 10. Legal and policy verification required

This document does not provide a legal conclusion about Ethiopian data protection, electronic transactions, employment, child protection, financial records, telecommunications, or cross-border data processing.

Before requirements are frozen, qualified reviewers must identify and verify:

- Applicable Ethiopian laws, regulations, directives, and effective dates.
- Whether and how each rule applies to EKHC and the proposed processing purpose.
- Lawful grounds or other required authority for each processing activity.
- Notice, consent, objection, access, correction, complaint, and disclosure obligations where applicable.
- Requirements for children and safeguarding information.
- Hosting location, international transfers, service-provider contracts, and breach notification.
- Record retention, financial audit, employment, and institutional record obligations.

Record the exact instrument, provision, source, effective date, reviewer, and applicability rationale. Do not treat a general website summary as legal advice or authoritative interpretation.

## 11. A1 evidence and decision register

| ID | Required evidence or decision | Current status | A1 action |
|---|---|---|---|
| PRIV-01 | Authoritative seventh-edition Constitution | MISSING | Obtain complete authorized copy and reconcile governance-related authority |
| PRIV-02 | Current applicable bylaws and amendments | MISSING | Verify applicability, adoption, and precedence |
| PRIV-03 | Current privacy, records, safeguarding, finance, and personnel policies | NOT VERIFIED | Obtain approved versions and responsible custodians |
| PRIV-04 | Applicable Ethiopian legal requirements and applicability review | NOT ASSESSED | Obtain qualified legal review with provision-level references |
| PRIV-05 | Authorized data owners and process owners | NOT PROVIDED | Identify through approved EKHC channels |
| PRIV-06 | Dataset and field-level inventory | NOT ASSESSED | Conduct structured discovery without real sensitive data |
| PRIV-07 | Approved classification policy | PROPOSED | Review provisional classes with authorized stakeholders |
| PRIV-08 | Retention and disposal schedule | MISSING | Derive from verified law and approved records policy |
| PRIV-09 | Access and disclosure authority matrix | BLOCKED | Do not define until governance and process authority are verified |
| PRIV-10 | Safeguarding and child-data handling rules | MISSING | Obtain current policy and qualified review |
| PRIV-11 | Offline data eligibility and device threat assessment | NOT ASSESSED | Validate actual devices, connectivity, and workflows |
| PRIV-12 | Hosting, processor, backup, and transfer assessment | NOT ASSESSED | Identify proposed providers and operating model before approval |
| PRIV-13 | Privacy incident and breach response process | NOT VERIFIED | Confirm accountable contacts, escalation, evidence preservation, and notification rules |
| PRIV-14 | Data-subject correction and complaint workflow | NOT ASSESSED | Validate applicable rights and authorized handling process |

## 12. Requirements and risk traceability

This assessment contributes evidence and proposed controls for:

- FR-002 — people and membership information.
- FR-003 — leadership and assignment records.
- FR-004 — governance records.
- FR-005 — controlled documents and records.
- FR-006 — communication and audience control.
- FR-007 — education and ministry workflows.
- FR-010 — offline workflows and synchronization.
- FR-012 — audit trails.
- NFR-001 — security and authorization.
- NFR-002 — privacy and data protection.
- NFR-003 — reliability and recoverability.
- NFR-006 — localization where notices, consent, and records require multilingual handling.
- NFR-007 — interoperability and controlled disclosure.

Related risks: R-005 (sensitive information), R-006 (children and safeguarding), R-007 (offline cache exposure), R-008 (sync conflicts), R-009 (authorization manipulation), R-012 (hosting and recovery), R-013 (financial controls), and R-014 (legacy data and integration quality).

These links demonstrate relevance only. They do not validate or close any requirement or risk.

## 13. A1 acceptance criteria for this assessment

This assessment may be considered ready for Owner review only when:

- Authoritative governance and policy sources are identified and provenance-checked.
- Applicable legal requirements have been reviewed by a qualified person.
- Authorized data and process owners have validated the candidate inventory.
- Classification criteria and exceptions are explicitly approved.
- Sensitive and child-related handling requirements are grounded in approved policies.
- Retention, correction, archival, and disposal requirements are evidenced.
- Access authority is derived from verified governance and process mandates.
- Offline eligibility is supported by a device and threat assessment.
- Residual risks, accountable owners, and treatment decisions are documented.
- Requirements and traceability records accurately reflect evidence status.
- The Owner explicitly approves the A1 baseline.

Until then, all classifications and handling proposals in this document remain DRAFT.

## 14. Explicit exclusions

This A1 document does not authorize:

- Collection, import, migration, or use of real member, child, pastoral, personnel, or financial records.
- Production database tables, migrations, API contracts, role catalogues, permission scopes, or UI implementation.
- Live AI processing, automated eligibility decisions, identity profiling, or third-party disclosure.
- Routine offline caching of confidential or highly restricted records.
- Publication, deployment, signing, external integrations, or operational use.
- A2 reconciliation, A3 implementation, or closure of A1.

**Assessment outcome:** PARTIAL — useful provisional controls documented; authoritative policy, legal, stakeholder, and Owner validation remain outstanding.
