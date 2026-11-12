# EKHC OS — Owner Operational-Readiness Input Register

**Status:** OWNER-APPROVED POLICY DECISIONS RECORDED — IMPLEMENTATION EVIDENCE INCOMPLETE  
**Decision date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Related reconciliation:** `docs/operations/MONITORING-OPERATIONAL-READINESS-GAP-RECONCILIATION.md`

> **Decision scope:** On 2026-11-12, the Owner approved ORG-02, ORG-03, and ORG-04 proposals with no amendments or conditions, and explicitly directed that SMS also be included for notifications. This records policy decisions only. It does not claim that channels, accounts, recipients, responders, systems, custodians, or controls have been provisioned, configured, accepted, or tested.

> **Confidentiality:** This public file must not contain personal names, email addresses, telephone numbers, account identifiers, private URLs, credentials, confidential exception rationales, or restricted-record contents. Keep those details in the approved restricted system. Public records may contain generic roles and opaque evidence references only.

## 1. Owner decision record

- Owner decision reference: **CHAT OWNER DECISION — 2026-11-12**
- Approving authority: **OWNER**
- ORG-02: **APPROVED — institutional email primary; SMS included as a notification channel**
- ORG-03: **APPROVED — role-based primary/backup coverage and acknowledgement targets as written below**
- ORG-04: **APPROVED — controlled institutional records and custody/access-control policy as written below**
- Amendments / conditions: **NONE SPECIFIED**, except the explicit SMS inclusion for ORG-02.
- Supporting decision evidence: **Owner's explicit chat decisions dated 2026-11-12**
- Implementation/control evidence: **NOT PROVIDED; unresolved items remain open**

Approval is evidence of the policy decisions, not proof of implementation or operational effectiveness.

## 2. ORG-02 — Notification destination and recipients

**Owner decision: APPROVED. Institutional email is the primary notification channel; SMS is also approved for notifications as the secondary channel.**

Approved policy:
- Primary: designated institutional security / operations email mailbox.
- Secondary: SMS notification to authorized duty responders.
- Recipients: role-based authorized distribution; actual identities and contact routes must be held in a restricted record.
- Notification content: severity, affected package, advisory reference, workflow run link, timestamp, and required action.
- Prohibited content: credentials, secrets, and confidential exception details.
- Delivery failure, bounce, or unavailable channel must be recorded as a notification failure. A successful GitHub workflow is not proof of notification delivery.

Implementation and evidence:
- Actual email service, tenant, and mailbox: **NOT PROVIDED — UNRESOLVED**
- Actual SMS provider, sender/service configuration, and endpoint: **NOT PROVIDED — UNRESOLVED**
- Account / tenant owner and channel administrators: **NOT PROVIDED — UNRESOLVED**
- Authorized recipient roster and authorization basis: **NOT PROVIDED — RESTRICTED EVIDENCE REQUIRED**
- Credential / sender-ID custody and rotation procedure: **NOT PROVIDED — RESTRICTED EVIDENCE REQUIRED**
- Recipient acceptance and roster review / joiner-leaver process: **NOT PROVIDED — UNRESOLVED**
- Email and SMS channel control and successful synthetic delivery evidence: **NOT PROVIDED — NOT VERIFIED**

**ORG-02 disposition: POLICY APPROVED (EMAIL PRIMARY + SMS); IMPLEMENTATION PARTIAL / NOT VERIFIED.** SMS is an approved channel choice, but no SMS provider, sender identity, recipient number, account, or delivery test is evidenced.

## 3. ORG-03 — Responders, acknowledgement, and escalation

**Owner decision: APPROVED — role-based primary and backup coverage, with Owner or explicitly delegated escalation authority.**

Approved coverage policy:
- Primary responder: designated security / operations duty role.
- Backup responder: separately designated alternate role.
- Escalation authority: Owner or explicitly delegated authority.
- Coverage must account for approved operating hours, non-working days, holidays, unavailability, and handover.
- Responders must operate within expressly approved authority limits; this approval does not grant unbounded remediation or production privileges.

Approved acknowledgement targets:

| Finding priority | Acknowledgement target |
|---|---|
| Critical / actively exploitable | **4 hours** |
| High | **1 business day** |
| Medium | **2 business days** |
| Low / informational | **3 business days** |

Acknowledgement means a human confirms receipt; it does not mean investigation or remediation is complete.

Implementation and evidence:
- Actual primary and backup responder identities: **NOT PROVIDED — RESTRICTED EVIDENCE REQUIRED**
- Responder acceptance of responsibility: **NOT PROVIDED — NOT VERIFIED**
- Coverage hours, timezone, holiday rota, handover, and unavailability procedure: **NOT PROVIDED — UNRESOLVED**
- Responder authority boundaries and prohibited actions: **NOT PROVIDED — UNRESOLVED**
- Operational acknowledgement definition and evidence source: **NOT CONFIGURED / NOT VERIFIED**
- Escalation triggers, routes, and failure-to-acknowledge handling: **NOT CONFIGURED / NOT VERIFIED**
- Restricted incident / decision record location: **NOT PROVIDED**
- Delivery and human acknowledgement test evidence: **NOT PROVIDED — NOT RUN**

**ORG-03 disposition: POLICY AND TARGETS APPROVED; RESPONDER ASSIGNMENT, COVERAGE, ROUTING, AND OPERATIONAL EVIDENCE NOT VERIFIED.** GitHub workflow success is not proof of human receipt or acknowledgement.

## 4. ORG-04 — Restricted exception-record custody

**Owner decision: APPROVED — controlled institutional records system and the proposed custody, access-control, audit, retention, and confidentiality policy.**

Approved policy requirements:
- Use a controlled institutional system of record separate from the public repository.
- Designate primary and backup custodians.
- Enforce least-privilege access and MFA.
- Require Owner or explicitly delegated-authority approval for access.
- Maintain audit trails for viewing, creation, modification, export, and deletion where supported.
- Encrypt records in transit and at rest.
- Provide controlled backup and recovery.
- Establish documented retention and secure disposal.
- Conduct periodic access reviews.
- Keep only opaque evidence references and non-sensitive status in the public repository.

Implementation and evidence:
- Actual restricted system / tenant: **NOT SELECTED — UNRESOLVED**
- System owner and primary / backup custodians: **NOT PROVIDED — RESTRICTED EVIDENCE REQUIRED**
- Authorized access groups and access-approval configuration: **NOT PROVIDED — NOT VERIFIED**
- MFA, encryption, audit logging, backup / recovery configuration: **NOT PROVIDED — NOT VERIFIED**
- Retention and secure disposal schedule: **NOT PROVIDED — UNRESOLVED**
- Access-review cadence and completed review evidence: **NOT PROVIDED — UNRESOLVED**
- Confidential evidence-handling procedure and opaque-reference convention: **NOT PROVIDED — UNRESOLVED**

**ORG-04 disposition: POLICY APPROVED; SYSTEM SELECTION, CUSTODIAN ASSIGNMENT, CONTROL CONFIGURATION, AND EVIDENCE NOT VERIFIED.**

## 5. Rehearsal and activation boundary

- Controlled synthetic rehearsal: **NOT AUTHORIZED / NOT RUN**
- Production notification integration: **NOT AUTHORIZED**
- Scheduled workflow activation: **NOT AUTHORIZED**
- Production operation: **NOT AUTHORIZED**
- Merge / default-branch integration: **NOT AUTHORIZED**
- Deployment, publication, or signing: **NOT AUTHORIZED**
- A5: **NOT AUTHORIZED**

Any future rehearsal requires a separate explicit Owner authorization after the implementation evidence is assembled. Use synthetic, non-sensitive fixtures only; do not create or modify a real exception to test the process.

## 6. Current gate status

| Gate | Owner decision | Implementation / evidence status |
|---|---|---|
| ORG-02 email + SMS notification policy | **APPROVED** | **PARTIAL / NOT VERIFIED** — services, account control, recipients, and delivery tests missing |
| ORG-03 responder coverage and acknowledgement targets | **APPROVED** | **NOT VERIFIED** — actual roster, accepted coverage, routing, and acknowledgement evidence missing |
| ORG-04 restricted-record custody policy | **APPROVED** | **NOT VERIFIED** — system, custodians, configured controls, and audit/retention evidence missing |
| Controlled synthetic rehearsal | Not approved | **NOT AUTHORIZED / NOT RUN** |
| Operational readiness | — | **NOT VERIFIED** |
| Production readiness | — | **NOT READY** |

## 7. Governance

This register records the Owner's approved policy decisions and preserves outstanding implementation evidence as unresolved. It does not itself provision accounts, authorize people, configure controls, or demonstrate delivery, acknowledgement, or custody.

No credentials, secrets, private contact details, or restricted records may be copied into this public repository. No external integration, secret creation, permission expansion, workflow-trigger change, exception-register mutation, schedule activation, production operation, merge, deployment, publication, signing, or A5 is authorized by these decisions.

A4 technical verification remains **VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS**. Operational readiness remains **NOT VERIFIED** until the implementation evidence above is supplied and assessed.


## 8. Evidence reconciliation against approved policies — 2026-11-12

**Method and scope:** Read-only inspection of the current Owner register, operational gap reconciliation, security-monitor operator runbook, A3 monitoring design, and committed exception register in the repository. This pass did not access an external institutional email tenant, SMS gateway/provider console, private recipient directory, HR/duty roster, or restricted records system because no such source or approved access reference is identified in the repository evidence. No identities or services are inferred.

### 8.1 ORG-02 — Email and SMS services, recipient authorization, delivery

| Required evidence | Evidence observed | Reconciliation |
|---|---|---|
| Institutional email service, tenant, designated mailbox, ownership/admin | The operator runbook says the monitor currently writes GitHub Actions job summary and logs; it explicitly does not provide guaranteed email or other out-of-band delivery. No institutional email service or mailbox is identified in the reviewed records. | **MISSING / UNRESOLVED** |
| SMS service/provider, sender identity, configuration and account ownership | Owner approved SMS as a secondary notification channel. No SMS provider, sender ID/number, gateway, account, configuration, or delivery evidence appears in the reviewed records. | **MISSING / UNRESOLVED** |
| Authorized recipient roster and authorization basis | No actual recipient roster, restricted roster reference, role-to-person authorization record, or recipient acceptance evidence is present in the reviewed records. | **MISSING / UNRESOLVED** |
| Email and SMS delivery controls and test evidence | No channel-control proof, synthetic email/SMS delivery receipt, bounce/failure record, or delivery audit evidence is present. | **MISSING / NOT VERIFIED** |

**Finding:** The approved design is email-primary plus SMS-secondary, but neither channel is established operationally. GitHub job summary/stdout remains the only repository-evidenced output. No notification integration or test was performed.

### 8.2 ORG-03 — Responder coverage and acknowledgement / escalation

| Required evidence | Evidence observed | Reconciliation |
|---|---|---|
| Primary and backup responder identities and role authorization | No accepted primary/backup roster or restricted identity reference is present. | **MISSING / UNRESOLVED** |
| Coverage hours, timezone, holiday rota, handover and absence coverage | No approved duty schedule or acceptance/availability evidence is present. | **MISSING / UNRESOLVED** |
| Approved acknowledgement targets | Owner approved Critical/actively exploitable: 4 hours; High: 1 business day; Medium: 2 business days; Low/informational: 3 business days. | **POLICY EVIDENCE PRESENT; OPERATIONAL ENFORCEMENT NOT VERIFIED** |
| Acknowledgement event, evidence source, escalation triggers and routes | No configured acknowledgement mechanism, escalation destination, timeout behavior, or delivery/acknowledgement records are present. | **MISSING / NOT VERIFIED** |
| Responder acceptance and authority boundaries | No signed/recorded acceptance or role authority definition is present. | **MISSING / UNRESOLVED** |

**Finding:** The role-based coverage model and acknowledgement targets are approved policy, not an assigned or accepted rota. No human acknowledgement or escalation path is demonstrated.

### 8.3 ORG-04 — Restricted exception-record custody

| Required evidence | Evidence observed | Reconciliation |
|---|---|---|
| Selected restricted system / tenant and accountable system owner | No named or opaque-referenced restricted system, tenant, or system owner is identified. | **MISSING / UNRESOLVED** |
| Primary/backup custodians and authorized access groups | No custodian assignment, access group, or restricted authorization record is present. | **MISSING / UNRESOLVED** |
| Least privilege, MFA, encryption and audit logging configuration | Policy is approved, but no configuration export, control attestation, or audit sample is provided. | **POLICY APPROVED; CONTROL IMPLEMENTATION NOT VERIFIED** |
| Retention, secure disposal, backup and recovery | No approved schedule, procedure, configuration, or recovery evidence is present. | **MISSING / UNRESOLVED** |
| Access review and evidence-handling procedure | No review cadence, completed review evidence, or controlled evidence-handling record is present. | **MISSING / UNRESOLVED** |

**Finding:** The committed public exception register is schema version 1 with an empty `exceptions` array. This confirms there are no committed exception entries; it does not establish custody of any external or future restricted records. No real exception or restricted record was created or changed.

### 8.4 Consolidated reconciliation status

| Area | Owner policy decision | Evidence status | Readiness disposition |
|---|---|---|---|
| ORG-02 email + SMS and recipients | **APPROVED** | Actual services, owners, roster, and delivery tests absent | **PARTIAL / NOT VERIFIED** |
| ORG-03 responder coverage | **APPROVED** | Targets approved; actual responders, accepted coverage, escalation and acknowledgement evidence absent | **NOT VERIFIED** |
| ORG-04 restricted-record custody | **APPROVED** | System, custodians, configured controls, retention and audit evidence absent | **NOT VERIFIED** |
| Operational readiness | — | Material controls remain unevidenced | **NOT VERIFIED** |
| Production readiness | — | Production gates remain unmet | **NOT READY** |

### 8.5 Required evidence to resolve the gaps

Provide evidence through an approved restricted channel; do not put private details or confidential records in this public repository:

1. **ORG-02:** email provider/tenant/mailbox ownership evidence; SMS provider/account/sender configuration evidence; authorized recipient roster and authorization/acceptance reference; synthetic email and SMS delivery receipts including failure-path handling.
2. **ORG-03:** accepted primary/backup responder roster; coverage calendar including timezone and holidays; role authority boundaries; configured acknowledgement and escalation rules; redacted delivery and human-acknowledgement evidence.
3. **ORG-04:** selected restricted system and accountable owner; primary/backup custodian assignments; access-group and MFA/least-privilege evidence; encryption/audit configuration evidence; retention/disposal policy; backup/recovery evidence; periodic access-review record.

Use only opaque evidence IDs and non-sensitive status in this register. Actual identities, addresses, telephone numbers, credentials, and restricted records must remain in the restricted system.

### 8.6 Scope and authorization boundary

This was a repository evidence reconciliation and documentation update only. It did not access external mail/SMS services or restricted systems, contact recipients/responders, configure integrations, create secrets, change permissions or workflows, modify the exception register, or run delivery tests or rehearsal.

No production activation, schedule activation, merge, default-branch integration, deployment, publication, signing, or A5 is authorized or performed. A controlled rehearsal remains **NOT AUTHORIZED / NOT RUN** and requires separate Owner authorization after the required evidence is supplied and reviewed.
