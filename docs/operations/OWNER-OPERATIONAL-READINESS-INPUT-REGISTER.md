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
