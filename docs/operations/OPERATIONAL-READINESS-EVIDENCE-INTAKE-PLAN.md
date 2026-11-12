# EKHC OS — Operational-Readiness Evidence Intake Plan

**Status:** PREPARATION COMPLETE — EXTERNAL EVIDENCE NOT YET AVAILABLE  
**Date:** 2026-11-12  
**Baseline:** A4 corrective re-verification commit `85f110c734aa348edf19d8163186f0906b8a6485`  
**Scope:** Documentation-only preparation for future ORG-02, ORG-03, and ORG-04 evidence intake.

## 1. Purpose and current position

This plan defines how evidence will be received, checked, referenced, and reconciled when institutional services and responsible personnel become available.

The Owner has confirmed that institutional email and SMS services are not yet available and are expected in the future. Actual recipients, responder assignments, responder acceptance/coverage, and a restricted records system/custodians are also not yet established in the repository evidence.

Accordingly, this is an intake plan, not an assertion that any service or control exists. No external service was contacted, no person was assigned, and no restricted evidence was requested or accessed in this documentation-only step.

## 2. Evidence handling rules

1. Obtain evidence only through an Owner-approved restricted channel or system.
2. Do not put names, email addresses, phone numbers, tenant/account identifiers, private URLs, credentials, message bodies, confidential exception rationales, or restricted records in this public repository.
3. Public documentation may record only an opaque evidence reference, evidence type, non-sensitive status, verification date, and responsible role where approved.
4. Never request secret values. For credentials, verify authorized custody, rotation, and configuration through redacted attestations or control evidence; do not copy credentials into this repository or report.
5. Distinguish policy approval, service provisioning, configuration, provider acceptance, recipient delivery, and human acknowledgement. These are separate evidence claims.
6. A screenshot or declaration alone is not proof of an end-to-end operational control when configuration exports, audit events, or controlled test evidence are reasonably available.
7. Mark missing, inaccessible, stale, conflicting, or unverified evidence explicitly. Do not infer a PASS.
8. Do not create a real exception, contact a real recipient, or send an actual notification merely to test the workflow.

## 3. ORG-02 — Institutional email and SMS

### 3.1 Email-primary service evidence

Collect, when available:
- Opaque evidence reference for the institutional email service/tenant and designated operational mailbox.
- Attestation of the service owner and authorized administrator roles.
- Evidence that the designated mailbox exists and is controlled by the institution.
- Sender identity and credential custody/rotation evidence, redacted to exclude secret values.
- Configuration/control evidence for authentication, transport security, delivery failure/bounce handling, and audit visibility where supported.
- Approved role-based recipient roster reference, authorization basis, recipient acceptance, and roster review/joiner-leaver process.
- Synthetic test evidence for accepted, rejected, unavailable, and retry-exhausted paths, with a clear distinction between simulated and provider-confirmed results.

### 3.2 SMS-secondary service evidence

Collect, when available:
- Opaque evidence reference for the institutional SMS provider/account/gateway and sender identity.
- Attestation of service owner and authorized administrator roles.
- Redacted configuration evidence for sender identity, credentials custody/rotation, endpoint security, and delivery failure handling.
- Approved role-based recipient roster reference and authorization/acceptance evidence.
- Provider-side or controlled test evidence distinguishing provider acceptance, delivery status if supplied, and human acknowledgement. Do not treat these as interchangeable.

### 3.3 Channel acceptance criteria

ORG-02 remains **NOT VERIFIED** until:
- Institutional email service and designated mailbox are evidenced.
- Institutional SMS service and sender configuration are evidenced.
- Recipient authorization and acceptance are evidenced through restricted records.
- Both channel paths have controlled test evidence, including failure handling.
- Public records contain only opaque evidence references and non-sensitive status.

The approved policy remains email primary and SMS secondary. This plan does not authorize choosing a provider, configuring an integration, creating credentials/secrets, or sending real messages.

## 4. ORG-03 — Responders, coverage, acknowledgement, escalation

Collect, when available:
- Restricted reference to the accepted primary security/operations duty responder.
- Restricted reference to a separately accepted backup responder.
- Owner or explicitly delegated escalation-authority reference and the delegation evidence.
- Accepted coverage schedule with timezone, business hours, weekends/holidays, leave/unavailability, handover, and backup substitution.
- Written authority boundaries and prohibited actions for each duty role.
- Defined acknowledgement event and approved evidence source. Acknowledgement means a human confirms receipt; it is not remediation completion.
- Configured escalation triggers, route, fallback when primary/backup is unavailable, and failure-to-acknowledge handling.
- Redacted test evidence demonstrating delivery, actual human acknowledgement, and escalation routing under an explicitly authorized controlled test.

Approved acknowledgement targets remain:
- Critical / actively exploitable: 4 hours.
- High: 1 business day.
- Medium: 2 business days.
- Low / informational: 3 business days.

ORG-03 remains **NOT VERIFIED** until accepted responder assignments, complete coverage, authority, acknowledgement mechanism, and escalation evidence are reviewed. Do not infer any individual or role assignment from repository access or project labels.

## 5. ORG-04 — Restricted exception-record custody

Collect, when available:
- Opaque reference to the selected institutional restricted records system/tenant and its accountable system owner.
- Primary and backup custodian role references, with acceptance and authorization evidence.
- Access-group design and least-privilege review evidence.
- MFA and encryption-in-transit/at-rest configuration attestations or exports.
- Audit logging evidence for view, create, modify, export, and delete events where supported.
- Approved retention schedule, legal/records policy reference, secure disposal procedure, and evidence of enforcement.
- Backup and recovery design plus a redacted recovery-test result.
- Access-review cadence, last completed review reference, and remediation tracking.
- Evidence-handling procedure defining how restricted artifacts receive opaque public references.

ORG-04 remains **NOT VERIFIED** until the system, owner, custodians, access controls, audit, encryption, retention, disposal, backup/recovery, and periodic review are evidenced. Do not transfer restricted records into the public repository.

## 6. Evidence intake register template

Use one row per evidence artifact in the restricted evidence system. The public repository should contain only the opaque reference and non-sensitive reconciliation status.

| Field | Required content |
|---|---|
| Evidence ID | Opaque, non-identifying reference |
| Control | ORG-02 / ORG-03 / ORG-04 and specific sub-control |
| Evidence type | Attestation, configuration export, audit sample, acceptance, test record, policy, recovery record |
| Issuer / accountable role | Restricted record; public copy only if non-sensitive and approved |
| Evidence date | Date evidence was generated or attested |
| Validity / review date | Expiry or next review date, if applicable |
| Integrity / provenance | Restricted-system source and integrity metadata |
| Verification method | What was checked, by whom/role, and against which acceptance criterion |
| Result | PASS / PARTIAL / MISSING / UNRESOLVED / STALE / CONFLICTING / NOT RUN |
| Public opaque reference | Reference only; no private URL or record contents |
| Follow-up | Gap owner role and required evidence, without private details |

Do not fill the register with invented sample services, recipients, responders, custodians, or evidence IDs that could be mistaken for real operational records. Synthetic fixtures remain confined to test code and clearly labeled mock evidence.

## 7. Intake and reconciliation sequence

1. **Receive:** Owner or authorized custodian supplies an opaque reference and confirms that the evidence is shared through an approved restricted channel.
2. **Classify:** Map it to ORG-02, ORG-03, or ORG-04 and a specific acceptance criterion.
3. **Validate provenance:** Check issuer authority, source system, evidence date, integrity, and whether the artifact is current.
4. **Inspect securely:** Review the artifact only in its approved restricted environment. Do not export sensitive contents into this public repository or chat.
5. **Assess:** Record PASS only when the evidence directly satisfies the criterion; otherwise record PARTIAL, MISSING, UNRESOLVED, STALE, CONFLICTING, or NOT RUN.
6. **Cross-check:** Verify dependencies between service ownership, recipient authorization, responder acceptance, and restricted-record custody.
7. **Update public status:** Commit only opaque references and non-sensitive findings to a dedicated operational evidence reconciliation branch. Preserve prior baselines and unrelated work.
8. **Escalate gaps:** Return missing evidence requests through the approved Owner-governed channel. Do not contact unverified people or providers.
9. **Rehearsal gate:** After ORG-02 through ORG-04 are evidenced and independently assessed, prepare a separate synthetic rehearsal plan for explicit Owner authorization. This plan itself does not authorize rehearsal.

## 8. Current intake readiness

| Evidence area | Current state | Intake action |
|---|---|---|
| Institutional email service | NOT YET AVAILABLE | Await Owner-provided service evidence |
| Institutional SMS service | NOT YET AVAILABLE | Await Owner-provided service evidence |
| Recipient authorization / acceptance | NOT YET ESTABLISHED | Await restricted roster evidence |
| Primary / backup responder acceptance | NOT YET ESTABLISHED | Await restricted role and coverage evidence |
| Acknowledgement / escalation configuration | NOT VERIFIED | Await configuration and controlled test evidence |
| Restricted records system | NOT YET IDENTIFIED | Await Owner selection and system-owner evidence |
| Custodians / access controls | NOT ESTABLISHED | Await restricted assignments and control evidence |
| Controlled rehearsal | NOT AUTHORIZED / NOT RUN | Separate authorization required after evidence review |

**Current disposition:** Preparation is complete; operational evidence intake is blocked pending future service provisioning and Owner-supplied evidence. Operational readiness remains **NOT VERIFIED** and production readiness remains **NOT READY**.

## 9. Scope and governance boundaries

This document is a preparation artifact only. It does not:
- Provision or select email/SMS services.
- Configure providers, recipients, responders, credentials, secrets, or repository variables.
- Contact any institution, provider, recipient, responder, or custodian.
- Access or create restricted records.
- Create or modify exception entries.
- Run external delivery tests or a human-response rehearsal.
- Activate the scheduled workflow or production operation.
- Authorize merge, default-branch integration, deployment, publication, signing, or A5.

A4 technical verification remains **VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS**. This separate operational preparation branch does not modify or reopen that A4 record.
