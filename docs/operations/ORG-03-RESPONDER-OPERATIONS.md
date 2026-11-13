# EKHC OS — ORG-03 Responder Operations, Acknowledgement and Escalation

**Implementation status:** PROCESS DESIGN IMPLEMENTED — INSTITUTIONAL ASSIGNMENTS AND LIVE OPERATION NOT VERIFIED  
**Owner policy basis:** Owner-approved ORG-03 decision, 2026-11-12  
**Scope:** Security / operations advisory response only; synthetic records for validation.

## 1. Purpose and control boundary

This procedure operationalizes the approved role-based primary/backup responder model, acknowledgement targets, and escalation to the Owner or explicitly delegated authority.

It does not appoint a person, create institutional authority, grant production privileges, establish 24×7 coverage, authorize remediation, or prove that a notification was delivered. Actual identities, contact routes, signed acceptance and duty schedules must remain in the approved restricted institutional system. This public repository stores role labels, opaque evidence references and non-sensitive status only.

## 2. Approved roles and separation of duties

| Role key | Responsibility | Minimum control |
|---|---|---|
| PRIMARY_SECURITY_OPERATIONS | First-line duty response and human acknowledgement | Named individual assigned in restricted roster; acceptance recorded |
| BACKUP_SECURITY_OPERATIONS | Alternate when primary is unavailable, conflicted or misses the routing handoff | Different individual from primary; acceptance recorded |
| OWNER_OR_DELEGATE | Escalation authority for coverage failure, overdue acknowledgement and decisions outside responder authority | Delegation must be explicit, scoped, current and evidenced |
| ROSTER_CUSTODIAN | Maintains restricted identities, contact routes, schedule and acceptance evidence | Restricted access; periodic review and change history |

The primary and backup must be distinct people. The roster custodian may not silently self-assign responder authority. Role assignment does not itself grant repository administration, production access, exception approval, deployment authority or permission to change monitoring policy.

## 3. Acknowledgement targets

The clock starts at the timestamp when the alert is successfully recorded as delivered to the designated institutional notification channel. If delivery cannot be established, record DELIVERY_UNCONFIRMED and route through the documented alternate channel; do not start or claim a human acknowledgement clock based solely on a successful GitHub workflow.

| Priority | Target |
|---|---|
| CRITICAL / actively exploitable | 4 elapsed hours |
| HIGH | 1 business day |
| MEDIUM | 2 business days |
| LOW / informational | 3 business days |

Acknowledgement is a human receipt confirmation containing the alert/evidence reference, responder role, acknowledgement timestamp and an explicit ACCEPTED or UNABLE_TO_ACCEPT disposition. An automated email receipt, SMS delivery receipt, workflow success, page view or bot response is not human acknowledgement. Acknowledgement does not mean investigation, containment or remediation is complete.

**Business-time calculation remains a deployment prerequisite:** the institution must approve the business timezone, working days, daily coverage window, public-holiday calendar, and treatment of alerts outside coverage. Until approved, business-day targets cannot be converted into authoritative due timestamps. The four-hour Critical target is elapsed time, not business time.

## 4. Routing and escalation state machine

1. **RECEIVED:** alert has a unique opaque alert ID, priority, source reference and trusted timestamp.
2. **DELIVERY_PENDING:** attempt primary institutional channel. Persist provider delivery result and event ID without sensitive payload.
3. **DELIVERY_UNCONFIRMED:** provider failure, timeout or absent delivery evidence. Record failure and use only an institution-approved alternate route. Never represent this state as delivered.
4. **AWAITING_HUMAN_ACK:** delivery is confirmed. Record the target due time using the approved priority clock.
5. **PRIMARY_ACKNOWLEDGED:** primary provides a human ACCEPTED or UNABLE_TO_ACCEPT response. Record identity reference, role, time and disposition in the restricted record.
6. **BACKUP_ROUTED:** primary is unavailable, explicitly unable to accept, or the acknowledgement deadline is reached without acknowledgement. Route to backup and record the trigger and time.
7. **AUTHORITY_ESCALATED:** backup is unavailable/unable to accept, the deadline is missed after backup routing, or a decision exceeds the responder's approved authority. Escalate to Owner or current explicitly delegated authority.
8. **ACKNOWLEDGED:** a human with an authorized role has accepted receipt. Preserve whether acceptance came from primary, backup or escalation authority.
9. **CLOSED:** only after the incident/alert handling record separately documents disposition and closure authority. Acknowledgement alone never closes an alert.

A routing transition must be append-only in the restricted event record. Corrections are new events referencing the superseded event; never rewrite the historical acknowledgement or escalation timeline.

## 5. Mandatory routing behavior

- Primary and backup are separate, accepted assignments. If either is absent or expired, coverage is INCOMPLETE.
- If primary is unavailable or declines, route to backup immediately; do not wait for the acknowledgement target.
- If primary does not acknowledge by its due time, route to backup and record SLA_BREACH_PRIMARY.
- If backup cannot accept or does not acknowledge within the applicable target, escalate to Owner/delegate and record SLA_BREACH_BACKUP.
- If no current Owner/delegate assignment exists, mark AUTHORITY_ROUTE_UNAVAILABLE, preserve the alert, and report operational readiness NOT VERIFIED. Do not invent an escalation contact.
- If all channels fail, retain DELIVERY_UNCONFIRMED, record each failed attempt, and raise an operational control failure through the last approved institutional route. Do not claim receipt.
- Conflicts of interest, leave, shift change and handover must be recorded; the outgoing responder remains responsible until the incoming responder explicitly accepts handover or the backup/authority route takes over.
- Responders may acknowledge and triage within their written authority. Destructive remediation, access changes, public disclosure, exception approval, production activation, merge and deployment require their separate applicable approvals.

## 6. Coverage roster requirements (restricted system only)

Each roster entry must contain:
- opaque responder reference (not a name in this public repository);
- role key and organizational authorization reference;
- restricted identity/contact reference;
- primary/backup designation and distinct-person check;
- effective-from and effective-until timestamps;
- timezone, coverage days/hours, holiday and absence coverage;
- explicit acceptance reference and timestamp;
- permitted actions and prohibited actions;
- current status: PENDING_ACCEPTANCE, ACTIVE, SUSPENDED or EXPIRED;
- last review timestamp and next review due date;
- change history and approving authority reference.

Activation requires both primary and backup ACTIVE, accepted, distinct, and covered by an approved schedule, plus a current Owner/delegate escalation route. No default identity, contact or 24×7 schedule is assumed.

## 7. Required acknowledgement / escalation event fields

Store in the restricted system:
- opaque alert ID and opaque evidence reference;
- priority and source workflow/advisory reference;
- event type and monotonic event sequence;
- event timestamp in UTC and original source timestamp;
- delivery channel, provider event reference and delivery outcome;
- responder opaque reference and role key;
- ACCEPTED / UNABLE_TO_ACCEPT disposition;
- acknowledgement target policy version and due timestamp;
- routing/escalation trigger, previous state and next state;
- authority/delegation reference where used;
- append-only audit event reference.

Never store credentials, access tokens, confidential exception details or restricted-record contents in GitHub logs, workflow artifacts or this public repository.

## 8. Monitoring and management controls

The roster custodian reviews roster validity, acceptance, distinctness, coverage gaps and expired assignments before each coverage period and at the institution-approved review cadence. Every roster change requires an approval reference and an append-only change record. Missed acknowledgement targets, failed delivery, missing coverage and unavailable escalation authority are control failures; they must remain visible and cannot be silently waived.

No automatic remediation or production action is triggered by acknowledgement state. The system may record, route and escalate only after the relevant channels and human assignments are actually provisioned and separately authorized.

## 9. Evidence required to mark ORG-03 operational

The following evidence must be supplied through an approved restricted channel and represented here only by opaque references:
1. accepted, distinct primary and backup roster entries with role authorization;
2. current Owner/delegate escalation assignment and delegation scope;
3. approved coverage timezone, working hours, days, holiday calendar and handover rules;
4. approved business-day calculation convention;
5. configured routing and acknowledgement policy version;
6. synthetic delivery evidence for primary, backup and escalation routes;
7. redacted human acknowledgement evidence for ACCEPTED and UNABLE_TO_ACCEPT;
8. evidence of missed-deadline, unavailable-primary, unavailable-backup, failed-channel and unavailable-authority handling;
9. access review and roster-custodian accountability evidence.

Until these are evidenced, ORG-03 remains POLICY APPROVED / PROCESS DESIGN IMPLEMENTED / OPERATIONAL READINESS NOT VERIFIED.

## 10. Activation gate

This document does not authorize rehearsal, sending real notifications, activating scheduled workflows, external integration, production operation, merge, deployment, publication, signing or A5. A controlled synthetic rehearsal requires separate explicit Owner authorization after institutional services and responder assignments are evidenced.
