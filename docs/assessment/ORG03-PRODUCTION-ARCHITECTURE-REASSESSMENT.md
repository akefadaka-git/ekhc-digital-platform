# ORG-03 Production Architecture Reassessment

**Assessment date:** 2026-11-13  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Assessment branch:** `a3/org-03-responder-operations`  
**Baseline head assessed:** `225daf65eaa27182ec20749adf469436fec1f654`  
**Assessment type:** Architecture assessment and decision record only  
**Implementation status:** NOT AUTHORIZED / NOT PERFORMED  
**Production status:** NOT READY  
**A5:** NOT AUTHORIZED

## 1. Executive decision

The ORG-03 R1–R6 work establishes a substantially stronger synthetic prototype, with exact-head automated verification. It does not establish a production trust, persistence, identity, key-custody, checkpoint-administration, or operational architecture.

**Recommendation:** retain the current prototype as a synthetic reference implementation. Before any production implementation is authorized, adopt a separately governed production architecture built around:

1. A transactional, highly available relational persistence service for authoritative alert state, event records, idempotency records, and transactional outbox entries.
2. Server-generated, trusted UTC acceptance timestamps, with separately preserved untrusted client/event-occurrence times.
3. Institutional identity federation plus an authoritative, versioned authority registry and explicit delegation/revocation lifecycle.
4. Centralized KMS/HSM-backed key custody with separation of duties and documented compromise recovery.
5. An independently administered remote monotonic checkpoint/attestation service or equivalent tamper-resistant external anchor.
6. Operational controls covering monitoring, incident response, backup/restore, disaster recovery, notification delivery, human acknowledgement, privacy, audit, and periodic access review.

These are target architecture recommendations, not selected vendors, approved technologies, procurement decisions, or permission to implement.

## 2. Scope, evidence and limitations

### 2.1 Included

This assessment covers:
- persistence and transaction boundaries;
- trusted timestamps and deadline calculation;
- identity, institutional authority and delegation;
- cryptographic key custody and lifecycle;
- checkpoint administration and tamper evidence;
- operational security, resilience, monitoring and governance.

### 2.2 Excluded

No code, configuration, migrations, database schemas, identity integration, credentials, keys, infrastructure, production data, restricted records, notifications, rehearsal, deployment, merge, publication or activation is authorized or performed.

No live institutional system, infrastructure, identity provider, custodian process, or service-level agreement was inspected. No legal, privacy, procurement, or regulatory compliance certification is made.

### 2.3 Evidence baseline

The assessment uses the current branch documentation and recorded synthetic test evidence:
- R1–R6 synthetic remediation and acceptance specification;
- internal R1/R3 security re-review;
- earlier durability, concurrency, recovery and restricted-access architecture review;
- ORG-03 acknowledgement/escalation acceptance matrix;
- final exact-head CI run #43408303800.

The CI result establishes only the behavior exercised by the synthetic test suite on its recorded runner and commit. It is not production assurance.

## 3. Target architecture and trust boundaries

### 3.1 Logical components

A production design should separate these trust domains:

1. **User and operator access layer:** authenticated web/mobile clients; no direct database access.
2. **ORG-03 application/API:** validates requests, applies authorization, creates trusted acceptance timestamps, enforces state transitions and idempotency.
3. **Transactional persistence:** authoritative relational database for alert state, append-only event records, authority references, idempotency records and outbox.
4. **Identity and authority services:** institutional identity provider and independently governed role/delegation registry.
5. **Cryptographic services:** KMS/HSM for key generation, signing/MAC operations, access policy, rotation and revocation.
6. **External integrity anchor:** remote checkpoint service or independently administered immutable evidence store.
7. **Notification adapters:** approved email/SMS/provider integrations, with delivery receipts kept distinct from human acknowledgement.
8. **Audit, monitoring and recovery services:** protected security logs, alerting, backup, restore, incident response and disaster recovery.

Trust boundaries must be explicit. Compromise of the application process, database administrator, identity administrator, key administrator, or checkpoint administrator must not silently grant all powers.

### 3.2 Recommended event/state model

Prefer a transactional state-plus-append-only-event model for the initial production service:
- update authoritative alert aggregate and append the corresponding event in one database transaction;
- enforce unique event ID, per-alert sequence, idempotency key and request fingerprint constraints;
- use optimistic concurrency or row-level serialization so competing acknowledgements have one deterministic winner;
- write a transactional outbox record in the same transaction;
- dispatch notifications asynchronously and record provider delivery separately;
- never treat provider acceptance/delivery as human acknowledgement;
- preserve the original accepted result for exact idempotent retries.

Full event sourcing should be selected only if replay, temporal reconstruction, multiple projections, and event-driven integration justify its additional operational complexity. This assessment does not mandate full event sourcing.

## 4. Persistence architecture

### 4.1 Recommendation

Use a supported transactional relational database service as the authoritative store. PostgreSQL is a candidate for evaluation, not an approved selection. The final choice must follow hosting availability, data residency, supportability, recovery objectives, security administration, cost and institutional ownership review.

Do not use a local SQLite file or a database colocated with the application host as the production system of record.

### 4.2 Required transactional guarantees

A single logical acknowledgement/transition transaction must atomically:
- verify current aggregate version and state;
- verify the authenticated actor and authority reference;
- apply the valid transition;
- append the immutable event;
- persist idempotency/request fingerprint and committed response;
- append an outbox item where notification is required.

Required constraints:
- unique event identifiers;
- unique alert/sequence pair;
- unique idempotency scope/key;
- foreign-key integrity for alert, event, authority reference and outbox relationships;
- immutable event history through application permissions and controlled database administration;
- explicit transaction isolation and bounded retry semantics;
- no success response before commit confirmation.

A retry with the same idempotency key and same canonical request returns the original committed result. Reuse with a different request fingerprint must be rejected.

### 4.3 Concurrency

The service must define a linearization point for competing primary, backup, escalation, expiry and closure actions. Use database-enforced concurrency control; do not rely on in-process locks.

Acceptance evidence must include:
- multi-process and multi-host races;
- duplicate and delayed retries;
- acknowledgement versus deadline/escalation races;
- transaction timeout and deadlock handling;
- exactly one accepted state transition per aggregate version;
- deterministic recovery after a losing transaction or retried request.

### 4.4 Durability, backup and restore

Required controls:
- encrypted backups with separately controlled backup keys;
- point-in-time recovery where supported;
- defined retention and immutable/offline backup copies;
- documented RPO and RTO approved by the institution;
- periodic restore exercises in an isolated environment;
- verification of event-chain, aggregate, authority and outbox consistency after restore;
- documented recovery when database state and external integrity checkpoints disagree.

A backup job reporting success is not proof of recoverability. Only a witnessed restore test with recorded recovery-point and recovery-time evidence can support that claim.

## 5. Trusted timestamp and deadline architecture

### 5.1 Separate time concepts

Production records must distinguish:
- **accepted_at:** server-generated UTC time when the service accepted and durably committed the request;
- **occurred_at:** asserted time an external or human event allegedly occurred; untrusted unless independently attested;
- **received_at:** time an external provider or integration delivered the message to ORG-03;
- **effective_at:** institutionally approved time a grant, revocation, assignment or policy takes effect;
- **due_at:** deadline derived from the approved SLA and business calendar.

Never accept a client-supplied timestamp as the authoritative acceptance or revocation time. Preserve it only as an explicitly untrusted claim with provenance.

### 5.2 Time source and integrity

Required:
- server-side time synchronization to approved, monitored time sources;
- UTC storage and unambiguous RFC 3339/ISO 8601 representation;
- monitoring for clock offset, synchronization loss and clock jumps;
- trusted server-side timestamp creation at the acceptance boundary;
- monotonic elapsed-time measurement for in-process duration/timeouts, not wall-clock comparisons;
- immutable preservation of the timestamp and source metadata used for each decision;
- documented behavior when time synchronization is degraded or unavailable.

A conventional synchronized server clock is not automatically a legally trusted timestamp authority. If non-repudiation or evidentiary timestamp certification is required, that requirement needs a separate legal/security assessment and a qualified trusted timestamping service.

### 5.3 SLA and business calendar

The current target acknowledgement intervals (Critical 4 elapsed hours; High 1 business day; Medium 2 business days; Low/informational 3 business days) must remain policy proposals until institutionally ratified.

Before implementation, the institution must approve:
- authoritative timezone;
- working days and working hours;
- holiday calendar and exceptional closures;
- 24/7 coverage rules for critical incidents;
- daylight-saving/time-zone rule handling if applicable;
- pause/suspension rules, if any;
- deadline recalculation policy after severity changes;
- treatment of late, delayed, duplicated or out-of-order messages.

Persist the calendar/policy version and the computed due_at value used for each alert. Do not recalculate historical deadlines silently when a calendar changes.

## 6. Identity, authority and delegation

### 6.1 Authentication

Use an institution-approved identity provider supporting:
- unique individual identities;
- MFA, preferably phishing-resistant for privileged and restricted actions;
- lifecycle disablement and session revocation;
- strong session protection and step-up authentication for sensitive actions;
- audit correlation between authenticated identity, session and action.

OIDC or SAML federation are candidate integration patterns, not selections. The institution must identify the authoritative identity provider and owner.

Shared responder accounts are not acceptable for human acknowledgement evidence.

### 6.2 Authorization and authority registry

Authentication proves which account authenticated; it does not prove that the person holds a particular institutional office or has authority for a specific alert.

Create a separately governed, versioned authority registry whose source of truth is institutionally designated. Each grant must bind:
- unique principal identity;
- institutional role/office and scope;
- permitted actions and resource scope;
- grantor and approval evidence;
- valid-from and expiry times;
- delegation chain and limits, if delegated;
- revocation decision, actor and effective time;
- immutable version/reference.

Enforce least privilege, deny by default, server-side record/action/field scope, separation of duties, and explicit conflict-of-interest handling. The application must not allow a user to grant authority to themselves.

### 6.3 Delegation and revocation

Institutional policy must define who may appoint primary/backup responders, who may delegate Owner/delegate authority, approval requirements, emergency revocation, and how authority is verified when the identity provider or registry is unavailable.

Events must preserve the authority version/evidence actually evaluated at acceptance. Revocation must not rewrite historical evidence; it must block new actions from the effective revocation time onward according to the approved policy.

### 6.4 Unresolved institutional decisions

No actual EKHC office mapping, authority issuer, role owner, delegate chain, identity provider, roster or approval evidence is established by the synthetic prototype. These are mandatory inputs, not values to infer in code.

## 7. Cryptographic key custody and lifecycle

### 7.1 Recommendation

Use a centrally governed KMS or HSM-backed key service, selected after institutional threat-model and hosting review. Private signing keys or MAC keys must not be stored in application source, repository secrets as long-lived raw values, the application database, local configuration files, or the same administrative domain as the event database.

Use asymmetric signatures for independently verifiable attestations where third-party verification or separation of signing authority is required. Use HMAC only where shared-secret verification is appropriate and the verifier trust boundary is explicitly accepted.

### 7.2 Required controls

- key generation in an approved cryptographic boundary;
- non-exportable keys where supported and justified;
- least-privilege service identities and operation-level permissions;
- separation of key administrators from application/database administrators;
- dual control for high-impact key operations;
- key identifiers and algorithm/version metadata in signed records;
- scheduled rotation and emergency rotation procedures;
- historical verification policy and archival verification capability;
- revocation, compromise containment, forensic preservation and recovery;
- audit of every key administration and cryptographic operation;
- backup/escrow and disaster recovery consistent with the selected HSM/KMS model;
- tested behavior during KMS outage, throttling, permission loss and key retirement.

A key-revocation design must not make all historical evidence unverifiable without a controlled migration/re-attestation or archival verification strategy. Define how a compromised key affects the trust status of records signed before and after the suspected compromise window.

No production key material is to be generated or provisioned during this assessment.

## 8. Independent checkpoint administration and event integrity

### 8.1 Current limitation

The synthetic prototype stores an authenticated checkpoint in a local sidecar separate from SQLite. This improves the database-only-writer threat model but does not protect against an attacker who can modify both the database and checkpoint directory or compromise the process/key. The database commit and filesystem checkpoint replacement are not one atomic transaction; a crash between them can cause fail-closed unavailability.

### 8.2 Production target

Use a remote, independently administered monotonic anchor for checkpoint commitments. Candidate patterns include:
- a separate security-account service with append-only checkpoint API;
- immutable object storage with retention lock plus independently controlled signing;
- an independently administered transparency log;
- a managed ledger/attestation service, subject to vendor and jurisdiction review.

The checkpoint should bind at least:
- repository/service/environment identity;
- alert or partition identifier;
- highest committed sequence and event-chain head;
- checkpoint generation/version;
- signing key identifier and algorithm;
- trusted checkpoint creation time;
- previous checkpoint reference;
- policy/schema version.

The checkpoint administrator must be separate from routine application and database administration. Application operators must not be able to delete, rewrite or roll back the authoritative external checkpoint.

### 8.3 Consistency and recovery protocol

Design explicitly for the dual-write problem between the database transaction and external checkpoint service. Do not assume a database commit and remote checkpoint update are atomic.

A proposed pattern for evaluation:
1. Commit the event and a durable checkpoint-outbox record in the database transaction.
2. An independent checkpoint publisher submits the committed head to the remote anchor.
3. The remote anchor enforces monotonic sequence/generation and returns a signed receipt.
4. Persist the receipt reference and verify it asynchronously.
5. Expose an explicit integrity state: VERIFIED, PENDING_ANCHOR, DEGRADED, or QUARANTINED.
6. For high-risk actions, define whether a remote anchor receipt is required before the action is treated as fully committed or before downstream notification occurs.
7. On mismatch, missing receipt, rollback or unavailable anchor, fail closed for protected operations, quarantine affected partitions and invoke a documented reconciliation procedure.

The exact consistency model, availability trade-off, maximum anchoring delay and fail-closed scope require Owner and institutional risk approval. Never silently re-anchor to a lower sequence.

## 9. Operational security and service controls

### 9.1 Monitoring and alerting

Monitor at minimum:
- application/API availability and error rates;
- database availability, replication lag, locks, deadlocks and storage capacity;
- transaction retries and idempotency conflicts;
- event sequence/hash/MAC verification failures;
- checkpoint lag, mismatch, rollback and anchor unavailability;
- KMS/HSM errors, denied operations, key rotation and revocation;
- identity-provider and authority-registry outages;
- clock synchronization offset and time-source failures;
- notification provider acceptance, delivery failure and retry backlog;
- overdue acknowledgements and escalation queue age;
- backup completion and restore-test outcomes;
- privileged access, policy changes and audit-log integrity.

Alerts must have an approved human owner and fallback route. A monitoring alert is not proof of human receipt.

### 9.2 Notification and acknowledgement semantics

Keep distinct states for:
- queued;
- provider accepted;
- delivered/failed/unknown (where provider evidence supports it);
- human acknowledged;
- escalation initiated;
- resolved/closed by an authorized actor.

Email/SMS provider callbacks must be authenticated and deduplicated. A delivery receipt must never be promoted to human acknowledgement. If all channels fail, preserve the alert and raise an operational control failure; never claim receipt.

### 9.3 Audit, privacy and restricted data

Define a data classification and minimization policy before storing actual responder identities or contact details. Apply encryption in transit and at rest, restricted access, audited export, retention/deletion controls, legal hold, backup protection, and privacy-approved log redaction.

Audit records should capture actor, action, resource, decision, authority version, timestamp, request correlation and outcome, without unnecessarily duplicating sensitive payloads or credentials.

### 9.4 Incident response and operations

Approve runbooks for:
- suspected identity compromise;
- responder authority revocation;
- signing/MAC key compromise;
- event-chain or checkpoint mismatch;
- database corruption or rollback;
- KMS/HSM or identity-provider outage;
- notification provider outage;
- clock synchronization failure;
- backup/restore and disaster recovery;
- privacy/security incident and evidence preservation.

Define on-call ownership, escalation, change control, patching, vulnerability management, dependency review, security testing, access recertification, and periodic operational exercises.

### 9.5 Resilience objectives

Institutional owners must set service availability, RTO, RPO, maximum checkpoint lag, notification latency and acknowledgement coverage objectives. These values must be based on operational risk and service capability; this assessment does not invent numeric production SLAs.

## 10. Architecture decisions and options

| Decision area | Recommended direction | Alternatives / trade-off | Decision owner |
|---|---|---|---|
| System of record | Transactional relational database service | Managed PostgreSQL candidate; other supported relational service subject to evidence | Owner + institutional IT |
| Event model | State + append-only events + transactional outbox | Full event sourcing adds replay/projection complexity | Owner + architecture |
| Trusted time | Server-generated UTC acceptance time and monitored time sync | Qualified timestamp authority if evidentiary certification is required | Owner + security/legal |
| Identity | Institutional IdP federation | OIDC/SAML based on actual IdP capability | Institutional identity owner |
| Authority | Versioned institutional authority registry | Integrate with existing HR/governance source if authoritative | Governing authority |
| Key custody | KMS/HSM with separated administration | Self-managed HSM only with staffing and recovery capability | Security/key custodian |
| Checkpoint | Remote monotonic anchor under separate administration | Transparency log or immutable retention-locked store | Security owner + audit |
| Notification | Approved provider adapters and durable outbox | Multiple providers/fallback route; cost and coverage trade-offs | Operations owner |
| Recovery | Encrypted backups, PITR and tested restore | Secondary site/region based on approved RTO/RPO | Institutional IT |

No row is a final vendor, product, procurement, or implementation decision.

## 11. Production acceptance gates

Production implementation must not begin until the following are documented and approved:

| Gate | Required evidence | Current disposition |
|---|---|---|
| P-01 Persistence | Selected platform, ownership, data location, transaction and concurrency design, backup/restore plan | OPEN |
| P-02 Time | Trusted time source, timestamp semantics, timezone, SLA calendar and failure policy | OPEN |
| P-03 Identity | Named institutional IdP owner, MFA/session policy and lifecycle integration | OPEN |
| P-04 Authority | Approved role/office matrix, grantor, delegation and revocation rules | OPEN |
| P-05 Keys | KMS/HSM selection, custodians, separation of duties, rotation and compromise runbook | OPEN |
| P-06 Checkpoint | Independent administrator, remote anchor, consistency protocol and restore/reconciliation tests | OPEN |
| P-07 Operations | Monitoring owners, incident response, on-call, notification routes and support model | OPEN |
| P-08 Resilience | Approved RTO/RPO, backup retention, restore evidence and disaster recovery exercise | OPEN |
| P-09 Privacy | Data classification, minimization, retention, access, export and legal review | OPEN |
| P-10 Independent assurance | External security review, threat model, penetration test plan and findings disposition | OPEN |
| P-11 Operational readiness | Accepted primary/backup roster, coverage calendar, authority route and controlled rehearsal approval | OPEN |
| P-12 Owner scope approval | Explicit staged authorization for any production-bound implementation | OPEN |

A4 cannot be declared fully closed for production architecture based on synthetic CI alone. A5 remains a separate authorization.

## 12. Risk register

| ID | Risk | Severity | Required treatment |
|---|---|---|---|
| AR-01 | Local database/checkpoint compromise permits coordinated rollback or rewrite | Critical | Independent remote monotonic anchor and separated administration |
| AR-02 | Database commit and checkpoint update are not atomic | High | Durable outbox, explicit pending-anchor state and tested reconciliation |
| AR-03 | Caller-controlled timestamps permit backdating | Critical | Trusted server acceptance time and authoritative time governance |
| AR-04 | Synthetic principal/role evidence is not institutional authority | Critical | Institutional IdP plus versioned authority registry |
| AR-05 | Process-held synthetic keys do not provide production custody | Critical | KMS/HSM and separated key administration |
| AR-06 | Unknown recovery behavior after key compromise/revocation | High | Compromise window policy, archival verification and recovery exercise |
| AR-07 | Unapproved business calendar can produce incorrect escalation | High | Ratified timezone, coverage and holiday calendar |
| AR-08 | Provider delivery can be mistaken for human acknowledgement | High | Separate delivery and acknowledgement states with authenticated callbacks |
| AR-09 | Backup success may not produce recoverable service | High | Periodic witnessed restore and DR tests |
| AR-10 | No assigned operational owners or accepted responder roster | Critical | Institutional appointment, acceptance, coverage and escalation evidence |

Severity ratings are architecture risk assessments, not evidence that an incident has occurred.

## 13. Required institutional input register

The following inputs remain unresolved and must be provided by authorized institutional owners:
1. System/data owner and service sponsor.
2. Approved hosting jurisdiction and data-residency constraints.
3. Database/platform operations owner and support model.
4. Institutional identity provider and identity lifecycle owner.
5. Authority issuer, office/role matrix, delegation rules and revocation approver.
6. Security officer and independent key custodian(s).
7. Independent checkpoint/log administrator.
8. Approved time source, timezone, working calendar and SLA policy owner.
9. Primary/backup responder appointments, acceptance, coverage and fallback routes.
10. Approved email/SMS providers and evidence/retention requirements.
11. Privacy/data classification, retention and incident notification requirements.
12. RTO, RPO, availability and checkpoint-lag objectives.
13. Independent security reviewer and penetration-test authority.

Do not infer these values from test fixtures, repository usernames, informal chat, or the current synthetic roster.

## 14. Final disposition

- R1–R6 synthetic prototype implementation: **IMPLEMENTED**.
- Exact-head synthetic CI evidence: **PASS** at the recorded baseline.
- Production persistence architecture: **ASSESSED — NOT SELECTED / NOT IMPLEMENTED**.
- Trusted timestamps: **REQUIREMENTS IDENTIFIED — NOT IMPLEMENTED**.
- Institutional identity and authority: **REQUIREMENTS IDENTIFIED — UNRESOLVED**.
- Production key custody: **REQUIREMENTS IDENTIFIED — NOT IMPLEMENTED**.
- Independent checkpoint administration: **REQUIREMENTS IDENTIFIED — NOT IMPLEMENTED**.
- Operational controls: **REQUIREMENTS IDENTIFIED — NOT VERIFIED**.
- Independent external security review: **NOT OBTAINED**.
- Operational readiness: **NOT VERIFIED**.
- Production readiness: **NOT READY**.
- Merge, deployment, production activation, live notification, real identity/data use and A5: **NOT AUTHORIZED**.

**Assessment conclusion:** ORG-03 has a useful synthetic integrity/concurrency prototype, but production use requires institutional trust anchors and operational controls that do not exist in the current evidence. The recommended target architecture is suitable as a basis for further Owner and institutional decisions. It is not an implementation baseline until each open gate is resolved and a separate scope authorization is issued.

---
**Governance statement:** This document records architecture findings and recommendations only. It does not authorize implementation, procurement, infrastructure provisioning, merge, deployment, signing, publication, production operation or institutional rehearsal.
