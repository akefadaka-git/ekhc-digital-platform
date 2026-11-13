# ORG-03 Production Architecture Decision Register

**Document ID:** EKHC-ORG03-A1-ADR-001  
**Status:** Proposed decisions — none approved by this register  
**Baseline:** Synthetic A3 commit `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`

## Decision protocol

Each decision requires: stable ID; accountable institutional decision owner; options considered; authoritative evidence; selected option and rationale; security/privacy impact; consequences; approval identity and timestamp; effective date; review trigger. A blank or unavailable owner/evidence field means UNRESOLVED, not implicitly approved.

| ID | Decision | Options to evaluate | Accountable decision authority | Required evidence | Status |
|---|---|---|---|---|---|
| ADR-001 | Identity authority | Existing institutional IdP; federation; institution-managed identity | Institutional IT/security authority | Identity ownership, MFA, lifecycle, outage and revocation policies | UNRESOLVED |
| ADR-002 | Institutional subject and appointment source | HR/directory/governance register or approved authoritative combination | Institutional governance and IT | Authoritative source, update latency, appointment and revocation process | UNRESOLVED |
| ADR-003 | Authorization model | RBAC with organization-scoped ABAC; policy engine; hybrid | Governance/security owners | Role catalogue, scope hierarchy, action matrix, delegation rules | UNRESOLVED |
| ADR-004 | Persistence platform | Supported relational DB and HA topology | IT operations and data owner | Hosting, sovereignty, support, transaction and backup evidence | UNRESOLVED |
| ADR-005 | Event and aggregate consistency | Optimistic versioning; row locking; serializable aggregate boundary | Architecture/DB authority | Concurrency model, isolation and failure test plan | UNRESOLVED |
| ADR-006 | Outbox and delivery processing | DB outbox plus worker; approved queue integration | IT operations and communications | Retry, dedupe, ordering, provider semantics and failure policy | UNRESOLVED |
| ADR-007 | Trusted time | Institutional NTP/PTP or approved authenticated time service; independent timestamp authority if needed | IT operations, governance/legal | Source hierarchy, drift, outage and evidentiary requirements | UNRESOLVED |
| ADR-008 | Business calendar and SLA | Official calendar/timezone source and versioning approach | Operations/governance | Business hours, holidays, local zone, SLA interpretation | UNRESOLVED |
| ADR-009 | Key custody | Institutional KMS/HSM or approved managed custody | Security/key custodian | Custodian roles, dual control, audit, backup and compromise process | UNRESOLVED |
| ADR-010 | Cryptographic evidence | MAC for service integrity; signatures where verifier separation/evidence requires | Security authority | Threat model, algorithm policy, identity binding and verification needs | UNRESOLVED |
| ADR-011 | Independent checkpoint | Separate trust service/storage/administrator failure domain | Security and operations | Anti-rollback, retention, consistency and restore evidence | UNRESOLVED |
| ADR-012 | Restricted records | Existing system adapter or separately governed service | Records custodians/data owner | Classification, legal basis, minimization and access matrix | UNRESOLVED |
| ADR-013 | Notifications | Institution-approved SMS/email/push/telephony routes | Communications, privacy and procurement | Provider terms, destinations, consent/authority and payload policy | UNRESOLVED |
| ADR-014 | Audit and monitoring | Institutional SIEM/log platform and protected retention | Security/audit owner | Event taxonomy, access, retention, alert response | UNRESOLVED |
| ADR-015 | Hosting and residency | Institution-operated or institution-approved hosting | IT/security and legal | Data location, administrator model, contracts and sovereignty | UNRESOLVED |
| ADR-016 | Backup and disaster recovery | Independent backup domain, immutable copy, PITR and restore | Operations/data owners | Approved RPO/RTO, restore test and custody | UNRESOLVED |
| ADR-017 | Retention and disposal | Per-record-class schedule, legal hold and authorized deletion | Records/legal/privacy authority | Retention schedule and evidence preservation rules | UNRESOLVED |
| ADR-018 | Environment and release controls | Segregated dev/test/stage/prod with signed artifact promotion | IT/security/change authority | Environment access, CI/CD, migration and rollback policy | UNRESOLVED |
| ADR-019 | Operational coverage | Primary/backup roster, coverage calendar and delegated escalation | Operational Owner | Accepted assignments, verified routes and on-call evidence | UNRESOLVED |
| ADR-020 | Incident response | Institutional playbooks and response authority | Security/operations leadership | Severity, notification, containment and recovery runbooks | UNRESOLVED |

## Required decision record template

For each ADR, record:

- **Decision ID and title:**
- **Status:** PROPOSED / APPROVED / REJECTED / DEFERRED / SUPERSEDED
- **Decision owner and approving authority:**
- **Date and effective time (with timestamp assurance):**
- **Context and constraints:**
- **Options considered, including do-nothing:**
- **Selected option and rationale:**
- **Evidence references and source authority:**
- **Security, privacy, legal and operational impact:**
- **Consequences and residual risks:**
- **Implementation stage permitted (if any):**
- **Review trigger / expiry:**

## A1 exit rule

No ADR becomes APPROVED by editing this file or by repository authorship alone. Approval must be evidenced by the institutionally authorized decision-maker and recorded in the Owner decision record. Vendor choices and procurement remain outside the scope of this draft.

**Current disposition:** all 20 decisions UNRESOLVED. A1 NOT CLOSED; A2 NOT AUTHORIZED.
