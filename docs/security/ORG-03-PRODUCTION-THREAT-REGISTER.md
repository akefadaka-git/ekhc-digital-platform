# ORG-03 Production Security Threat Register

**Document ID:** EKHC-ORG03-A1-SEC-001  
**Status:** Initial architecture threat register — draft, not independently reviewed  
**Scope:** Proposed production integration; synthetic A3 remains unchanged

## Rating method

Severity and likelihood are not scored numerically until institutional impact criteria and threat intelligence are available. Priority labels below are provisional architecture review judgments, not a completed risk assessment. No risk is accepted by this document.

| ID | Threat / abuse case | Boundary and impact | Required preventive controls | Detection / evidence | Residual risk owner | Status |
|---|---|---|---|---|---|---|
| T-01 | Stolen session or compromised IdP account | Identity → API; unauthorized workflow action | MFA policy, short-lived sessions, secure token handling, revocation and reauthentication for sensitive actions | IdP alerts, session revocation logs, anomalous access | Institutional identity authority | OPEN |
| T-02 | False or stale appointment/role assertion | Governance source → policy; unauthorized responder/admin | Authoritative appointment source, signed/versioned authority evidence, expiry and revocation | Authority provenance and sync-lag monitoring | Governance authority | OPEN |
| T-03 | Delegation abuse or privilege escalation | Authority boundary; action outside delegated scope | Non-transitive scoped delegation, expiry, independent approval and separation of duties | Delegation issuance/revocation audit | Governance/security | OPEN |
| T-04 | Cross-organization or record authorization bypass | API → records; restricted disclosure or modification | Deny-by-default server policy, record-level checks, field minimization and independent records authorization | Policy decision logs, access review and negative tests | Records custodian/security | OPEN |
| T-05 | Administrator abuses privilege | Operations/admin boundary; silent data or policy changes | Least privilege, dual control, immutable audit, break-glass reason/expiry and independent review | Privileged-action alerts and periodic access review | Security/audit owner | OPEN |
| T-06 | Event replay, substitution, truncation or reordering | API/event store; false workflow history | Authenticated event binding, sequence/version constraints, idempotency, independent checkpoint | Replay verification and tamper alarms | Security/key custodian | OPEN |
| T-07 | Application and key/checkpoint compromise together | App ↔ key trust boundary; forged history | Separate admin domains, HSM/KMS policy, external checkpoint, independent verification | Key-use anomaly, checkpoint mismatch and incident evidence | Security authority | OPEN |
| T-08 | Key leakage, unauthorized rotation or lost historical verification | Key boundary; forged events or unverifiable history | Dual control, key purpose separation, rotation/revocation protocol, protected metadata and recovery | KMS audit, key inventory reconciliation | Key custodian | OPEN |
| T-09 | Clock skew, rollback or false time source | Time boundary; SLA miscalculation and disputed evidence | Authenticated redundant time, drift policy, time-assurance metadata and degraded mode | Clock offset alarms and time-source audit | IT operations/governance | OPEN |
| T-10 | Calendar/time-zone or holiday error | SLA engine; missed escalation or false breach | Authoritative calendar, versioned rules, test vectors and recorded calculation inputs | Boundary-case tests and calendar change audit | Operations/governance | OPEN |
| T-11 | Concurrent commands create conflicting transitions | Application ↔ DB; lost update or duplicate escalation | Aggregate version check, transaction constraints, idempotency and concurrency control | Conflict metrics, invariant checks and race tests | Application/DB owner | OPEN |
| T-12 | Outbox retry or worker crash duplicates/misses delivery | DB ↔ provider; missed/duplicate notification | Durable outbox, lease recovery, dedupe, bounded retry and explicit uncertain state | Queue age, retry/dead-letter and provider reconciliation | Operations/communications | OPEN |
| T-13 | Spoofed provider webhook or delivery receipt | Provider → API; false delivery evidence | Authenticated webhook, replay protection, provider event ID and inbox dedupe | Signature failure, replay and receipt anomaly logs | Communications/security | OPEN |
| T-14 | Wrong recipient, SIM swap or compromised contact route | Notification destination; confidentiality and missed response | Authoritative verified contacts, change verification, minimal payload and alternate escalation | Contact change audit and delivery anomaly | Communications/data owner | OPEN |
| T-15 | Restricted data leaks through logs, exports or notification | App/audit/provider; privacy/legal impact | Data minimization, redaction, export controls, DLP where approved and access segmentation | Sensitive-data scanning and export alerts | Privacy/records owner | OPEN |
| T-16 | Backup theft or restore to stale/forged state | Backup/recovery boundary; disclosure or integrity loss | Encryption, separate custody, immutable retention, independent checkpoint and clean restore | Restore drills and integrity attestations | Operations/records owner | OPEN |
| T-17 | Database/network/key-service outage or partition | Service dependency; unavailable or uncertain workflow | Explicit degraded modes, fail-closed writes, HA and recovery objectives | Dependency health and outage alerts | IT operations | OPEN |
| T-18 | Ransomware, host loss or destructive insider | Infrastructure boundary; loss of service/evidence | Segmentation, least privilege, protected backups, recovery isolation and incident plan | EDR/SIEM and restore evidence | Security/operations | OPEN |
| T-19 | Supply-chain compromise or vulnerable dependency | Build/release boundary; code execution or data exposure | Pinned dependencies, SBOM, provenance, vulnerability response and signed artifacts | CI audit, dependency scan and provenance verification | Engineering/security | OPEN |
| T-20 | Notification/queue denial of service or retry storm | API/provider boundary; delayed escalation | Rate limits, quotas, circuit breakers, bounded retries and priority queues | Queue saturation and provider error alerts | Operations | OPEN |
| T-21 | Insider changes policy/calendar without authority | Governance/configuration boundary; altered SLA or routing | Versioned config, dual approval, signed change evidence and rollback | Config-diff alerts and approval audit | Governance/audit owner | OPEN |
| T-22 | Emergency/break-glass access persists | Privileged access boundary; prolonged excessive access | Just-in-time grant, strict scope/expiry, reason and retrospective review | Immediate alert and expiry reconciliation | Security owner | OPEN |

## Required threat treatment

For each threat before A1 closure, record attack preconditions, likelihood rationale, impact classification, preventive control, detection control, response playbook, test evidence, residual risk, named risk owner and authorized acceptance or blocking disposition.

Threats involving legal/privacy impact require review by the institution's authorized privacy/legal function. Risk acceptance cannot be inferred from technical mitigation or project-owner authorship.

## Mandatory negative scenarios for later A4 planning

- revoked identity/appointment with stale session;
- cross-organization and cross-record ID substitution;
- delegation expiry and revocation race;
- clock rollback, time-source disagreement and calendar version change;
- simultaneous conflicting aggregate transitions;
- process crash at every transaction/outbox boundary;
- duplicate, delayed, forged and out-of-order provider receipts;
- KMS/HSM outage, key rotation and compromised key;
- checkpoint rollback and restore from stale backup;
- log/export/notification payload data-leak attempt;
- privilege escalation through break-glass and administrator functions.

These are future test-planning requirements only. No test implementation or production integration is authorized here.

**Disposition:** 22 threats catalogued; risk ratings, institutional owners, independent review and acceptance remain OPEN.
