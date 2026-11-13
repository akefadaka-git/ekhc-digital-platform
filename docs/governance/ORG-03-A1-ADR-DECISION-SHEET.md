# ORG-03 A1 — ADR Decision Sheet

**Document ID:** EKHC-ORG03-A1-ADR-SHEET-001  
**Status:** WORKING DECISION SHEET — PROPOSALS ONLY; NO ADR APPROVED  
**Approval model selected by Owner:** Owner approval plus relevant, formally authorized EKHC institutional approval/concurrence (`owner_and_institution`)  
**Owner additional instruction:** None  
**Related records:** [Architecture Decision Register](../architecture/ORG-03-ARCHITECTURE-DECISION-REGISTER.md); [Owner Decision Record](ORG-03-A1-OWNER-DECISION-RECORD.md)  
**Synthetic reference baseline:** `225daf65eaa27182ec20749adf469436fec1f654`

## 1. Purpose and decision rules

This sheet converts ADR-001 through ADR-020 into decision-ready proposals. It is a preparation aid, not an institutional decision, procurement instruction, architecture approval, or authorization to implement.

The Owner selected a joint approval model. For each ADR:
1. The Owner's approval is required for the Owner-governed project baseline.
2. The relevant EKHC institutional authority must be identified from authoritative governance instruments and must approve or concur within its actual mandate.
3. The named decision-maker, authority instrument, decision evidence, effective date and review trigger must be recorded.
4. Where legal/privacy/security implications apply, the appropriate institutional Legal/Privacy/Security review must be evidenced; technical preference cannot replace that review.
5. No option in this sheet is selected or approved merely because it is recommended here.

**Evidence limitation:** No authoritative EKHC internal constitution/bylaws, delegation schedule, signed resolutions, appointments, policies, contracts, data-processing records, service-provider commitments or operational runbooks have been evidenced in the reviewed project materials. Functional authorities below are role-level routing suggestions, not verified office-holders or a claim that those roles possess formal delegated power.

## 2. ADR decision matrix

| ADR | Decision topic | Working recommendation for review (NOT APPROVED) | Required institutional evidence before decision | Functional authority to identify and verify | Status |
|---|---|---|---|---|---|
| ADR-001 | Identity authority | Prefer an institution-controlled IdP with MFA, lifecycle controls, auditable federation and fail-closed behavior; defer provider selection. | Identity/security standard; IdP ownership; MFA and account lifecycle policy; outage and revocation procedures. | IT/Security + Governance/HR/Secretariat | UNRESOLVED |
| ADR-002 | Institutional subject and appointment source | Use an authoritative institutional subject and appointment register; bind roles to verified appointments/delegations, not self-asserted profiles. | Approved subject source; appointment register; signed appointment, delegation, expiry and revocation records; update SLA. | Governance/Secretariat + HR + IT | UNRESOLVED |
| ADR-003 | Authorization model | Use least-privilege, deny-by-default authorization with explicit role/action matrix and organization/record scope; evaluate RBAC plus constrained ABAC. | Approved role catalogue; authority matrix; delegation rules; restricted-record access matrix; privacy/security review. | Governance + Data Owners + Security/Privacy | UNRESOLVED |
| ADR-004 | Persistence platform | Retain a transactional relational database as the candidate architecture; select a product/topology only after hosting, support, residency and recovery evidence. | Hosting/residency approval; data ownership; transaction/availability needs; support and processor terms; backup evidence. | IT Architecture/Operations + Data Owner + Legal | UNRESOLVED |
| ADR-005 | Event and aggregate consistency | Require explicit aggregate boundaries, optimistic concurrency or row locking as justified, idempotent commands and transactionally consistent state changes. | Business invariants; concurrency/load profile; isolation requirements; failure and recovery tests; data-owner acceptance. | Architecture/DB Authority + Process Owner | UNRESOLVED |
| ADR-006 | Outbox and delivery processing | Prefer transactional outbox with idempotent workers, bounded retries, deduplication and observable dead-letter handling; queue/provider remains undecided. | Delivery/ordering requirements; provider contracts; retry and escalation policy; payload and disclosure rules. | IT Operations + Communications + Privacy | UNRESOLVED |
| ADR-007 | Trusted time | Define an institutional time-source hierarchy, synchronization monitoring, drift limits and outage behavior; use a legally recognized timestamp service only where evidence/legal analysis shows it is required. | Time-service ownership; approved sources; drift/outage policy; evidentiary and legal requirements; timestamp-provider terms if applicable. | IT Time-Service Owner + Legal/Governance | UNRESOLVED |
| ADR-008 | Business calendar and SLA | Use a versioned, institution-approved calendar/timezone and explicit business-hours/SLA rules; do not infer holidays or deadlines from device-local time. | Official calendar source; timezone; holiday/closure authority; operating hours; SLA policy and exception rules. | Operations + Governance/Secretariat | UNRESOLVED |
| ADR-009 | Key custody | Require institution-approved KMS/HSM or equivalent controlled custody, separation of duties, rotation, revocation, audit and tested recovery; no production keys in application configuration. | Crypto/key-management policy; named custodians; dual-control mandate; service assurance and location; compromise/recovery procedures. | Information Security + Appointed Key Custodian | UNRESOLVED |
| ADR-010 | Cryptographic evidence | Use MACs for service-to-service integrity where shared trust is appropriate; require attributable digital signatures or other independent-verifier evidence where non-repudiation/approval proof is required. | Threat model; assurance level per action; identity binding; signature/timestamp legal analysis; key lifecycle and verifier requirements. | Security + Governance + Legal | UNRESOLVED |
| ADR-011 | Independent checkpoint | Require a checkpoint/anchor in a separate administrative and failure domain with independently controlled anti-rollback evidence and tested restore. | Independent service/storage owner; administrator separation; retention; anti-rollback design; restore and compromise tests. | Security + IT Operations + Independent Custodian | UNRESOLVED |
| ADR-012 | Restricted records | Keep restricted-record content outside ORG-03 unless a lawful, minimized, explicitly governed integration is approved; use references and scoped access where feasible. | Record inventory/classification; controller/processor roles; lawful basis; custodian; access matrix; retention/legal hold; DPIA/prior consultation if applicable. | Data Owners/Records Custodians + Privacy/Legal | UNRESOLVED |
| ADR-013 | Notifications | Use only institution-approved channels/providers with verified recipient authority, minimal payloads, delivery receipts and fallback/escalation controls. | Provider contracts; approved sender/recipient sources; consent/authority basis; payload policy; delivery/failure and coverage procedures. | Communications + Privacy + Procurement/Legal | UNRESOLVED |
| ADR-014 | Audit and monitoring | Require tamper-resistant, access-controlled audit records, security monitoring, alert ownership and retention tied to approved records schedules. | Audit policy; event taxonomy; log access; retention/legal hold; SIEM/monitoring ownership; alert response roster. | Security + Internal Audit + IT Operations | UNRESOLVED |
| ADR-015 | Hosting and residency | Do not choose a host until actual data location, administrator access, subprocessors, cross-border transfers, contracts and safeguards are reviewed. | Hosting/data-location statement; processor/subprocessor list; admin/support model; contracts; legal transfer assessment and approval. | IT/Security + Legal/Privacy + Data Owner | UNRESOLVED |
| ADR-016 | Backup and disaster recovery | Require encrypted, access-separated backups, point-in-time recovery where supported, independent copies and demonstrated restore; RPO/RTO must be approved, not invented. | Approved RPO/RTO; backup custody; retention; restore evidence; disaster roles; service dependencies. | IT Operations + Data Owners + Security | UNRESOLVED |
| ADR-017 | Retention and disposal | Establish category-specific retention and legal-hold schedules; do not assign a generic retention period without records/legal authority. | Records classification; statutory/contractual requirements; approved schedule; legal-hold and deletion authorization; disposal evidence. | Records Management + Legal + Data Owners | UNRESOLVED |
| ADR-018 | Environment and release controls | Separate development, test, staging and production; promote immutable reviewed artifacts with protected approvals, secrets separation and rollback controls. | SDLC/change policy; environment ownership; access matrix; CI/CD controls; migration/rollback policy; release authority. | IT/Security + Change/Release Authority | UNRESOLVED |
| ADR-019 | Operational coverage | Require named primary/backup responders, accepted coverage windows, verified escalation routes and delegated authority before any operational service. | Approved roster; acceptance by responders; coverage calendar; contact verification; escalation mandate and fallback. | Designated Operational Owner + Secretariat | UNRESOLVED |
| ADR-020 | Incident response | Adopt institution-owned security/privacy incident playbooks with evidence preservation, severity, containment, notification decision authority and recovery exercises. | Incident/breach playbooks; response authority; contact tree; legal notification analysis; exercise records; post-incident review process. | Security Leadership + IT Operations + Legal/Privacy | UNRESOLVED |

## 3. Cross-cutting evidence bundles

The following eight evidence bundles are prerequisites for defensible ADR decisions. They are evidence requests, not assumptions that the documents exist.

| Bundle | Evidence requested | Functional routing |
|---|---|---|
| G-01 Governance mandate and decision authority | Constitution/bylaws; ORG-03 mandate; signed resolutions; delegation schedule; decision and escalation authority. | Governing body / Secretariat |
| G-02 Identity and institutional authority | Identity standard; IdP ownership; lifecycle; authoritative appointment/role register; signed appointment/delegation/revocation records. | IT/Security + Governance/HR/Secretariat |
| G-03 Data protection, records and restricted-record custody | Inventory/classification; controller/processor determination; lawful basis; system-of-record map; access matrix; retention/legal hold; DPIA/prior consultation if applicable. | Data owners / Records Custodians + Privacy/Legal |
| G-04 Hosting, persistence and service architecture | Hosting/data-location; database architecture; processor/subprocessor contracts; administrator model; support ownership; transaction/availability requirements. | IT Architecture/Operations + Data Owner |
| G-05 Time, calendar and SLA | Time source/configuration/drift/outage policy; official calendar/holiday source; timezone; operating hours; SLA policy. | IT time-service owner + Operations/Governance |
| G-06 Cryptographic custody and independent integrity | Crypto policy; KMS/HSM evidence; custodian appointments; dual control; key lifecycle/compromise plan; independent checkpoint ownership; anti-rollback and recovery tests. | Information Security + appointed key custodian |
| G-07 Notifications and responder coverage | Provider contracts; recipient source; payload/disclosure policy; accepted roster; verified routes; coverage calendar; delivery/fallback and escalation mandate. | Communications + designated Operational Owner |
| G-08 Audit, resilience, release and incident response | Audit/retention; monitoring; backup/DR; RPO/RTO; restore evidence; incident/breach playbooks; SDLC/change policy; exercise and independent review. | Security/Audit + IT Operations + Legal/Privacy |

## 4. Legal and regulatory review boundary

Legal requirements must be assessed for applicability by qualified institutional counsel. The existence of a legal rule does not by itself choose a technical product or establish an EKHC internal policy.

- Personal-data processing, security, accountability, breach handling, retention and cross-border transfer require applicability analysis under the relevant Ethiopian data-protection framework.
- Electronic signatures and legally recognized timestamp services must be distinguished from ordinary application authentication, HMAC integrity checks and system clock synchronization.
- Do not assume every workflow requires a qualified/regulated trust service; do not treat HMAC as proof of non-repudiation.
- Hosting location, retention periods, RPO/RTO, RBAC/ABAC details, providers and operational rosters remain institutional decisions requiring evidence.

## 5. Per-ADR approval record template

Complete one record for each ADR only after evidence is received:

- **ADR ID / title:**
- **Status:** PROPOSED / APPROVED / REJECTED / DEFERRED / SUPERSEDED
- **Owner decision reference:**
- **Institutional decision authority (office/person):**
- **Authority instrument and exact reference:**
- **Subject-matter concurrence(s):**
- **Decision date/effective time and timestamp assurance:**
- **Context and constraints:**
- **Options considered (including do-nothing):**
- **Selected option and rationale:**
- **Evidence references, provenance and integrity:**
- **Legal/privacy/security review:**
- **Consequences and accepted residual risks:**
- **Implementation stage permitted (if any):**
- **Review trigger / expiry:**

## 6. Current gate status

- Owner approval model: **RECORDED**.
- Formal EKHC approving offices/persons and authority instruments: **MISSING / UNVERIFIED**.
- Institutional evidence bundles G-01–G-08: **MISSING**.
- ADR-001–ADR-020: **20/20 UNRESOLVED; 0 APPROVED**.
- A1: **PARTIAL — NOT CLOSED**.
- A2: **NOT AUTHORIZED**.
- Production A3, live rehearsal, operational activation and A5: **NOT AUTHORIZED**.

## 7. Immediate next step

Issue the G-01–G-08 evidence request through the institution's verified official channels. Once authoritative responses are received, reconcile each document's issuer, authority, date, scope, approval status and integrity; then prepare ADR-specific options for Owner and institutional decision. No implementation or merge follows automatically.
