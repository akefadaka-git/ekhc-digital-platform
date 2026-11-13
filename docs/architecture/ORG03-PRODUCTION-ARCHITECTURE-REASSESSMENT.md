# ORG-03 Production Architecture Reassessment

**Assessment date:** 2026-11-13  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Assessment base:** `225daf65eaa27182ec20749adf469436fec1f654`  
**Assessment branch:** `docs/org03-production-architecture-reassessment`  
**System:** ORG-03 responder operations  
**Classification:** Architecture assessment and production-readiness requirements; not an implementation specification or deployment approval

## 1. Executive decision

**Decision: DO NOT PROMOTE THE CURRENT PROTOTYPE TO PRODUCTION.**

The current ORG-03 implementation is a synthetic-only SQLite event-store and access-policy prototype. Its R1–R6 remediation has passed the recorded exact-head Linux verification, including 158 Django tests, 84 dedicated ORG-03 tests, Ruff lint and formatting, and dependency audit on workflow run [43408303800](https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43408303800), for head `225daf65eaa27182ec20749adf469436fec1f654`.

That evidence supports the tested prototype scope only. It does not establish production availability, multi-host behavior, institutional authority, identity assurance, trusted time, production key custody, independently administered checkpoints, disaster recovery, privacy compliance, or operational responder readiness.

The recommended direction is a service-backed architecture with:
1. a supported transactional relational database and explicit data ownership;
2. server-generated trusted acceptance timestamps and monitored time synchronization;
3. institutional identity federation plus a separately governed, versioned authority service;
4. KMS/HSM-backed cryptographic key custody and documented rotation/compromise procedures;
5. a checkpoint/anchor service administered outside the database and application trust boundary;
6. controlled operations, monitoring, backup/restore, incident response, and continuity procedures.

These are target requirements, not selected products or approved infrastructure. Database vendor, hosting, identity provider, KMS/HSM, timestamping mechanism, and checkpoint technology remain undecided pending institutional requirements, threat modelling, cost and capability assessment, and Owner approval.

## 2. Scope and explicit exclusions

### In scope

- Production persistence and transaction boundaries.
- Trusted event time and authority-effective time.
- Authentication, identity binding, authorization and delegated authority.
- Cryptographic key lifecycle and custody.
- Checkpoint administration and rollback/fork detection.
- Availability, monitoring, backup, recovery, incident response and operational governance.
- Migration and acceptance gates from the synthetic prototype to a separately approved production design.

### Out of scope

This document does not authorize or perform:
- Django runtime integration or production database selection/configuration;
- ORM models, migrations, APIs, services, background workers or provider integrations;
- real identity-provider configuration, user onboarding, credentials or role assignments;
- production key generation, import, storage or KMS/HSM provisioning;
- real institutional data, restricted records, or live notifications;
- operational activation, institutional rehearsal, merge, deployment or A5.

The current prototype remains isolated and synthetic. No real EKHC roster, office, identity, authority, alert, or restricted record is represented by its fixtures.

## 3. Current baseline and assurance boundary

### Verified prototype characteristics

- Standalone Python/SQLite event-store adapter, not wired into Django.
- Synthetic-only HMAC-SHA-256 event authentication, key identifiers and key rotation.
- Authenticated checkpoint file stored in a local sibling directory outside the SQLite database.
- Append-only synthetic authority versions, event-bound evidence and effective-time revocation semantics.
- Transactional event append/replay, idempotency, bounded SQLite lock retry and deterministic connection closure.
- Synthetic deny-by-default policy harness and field-level projections.
- Dedicated Linux CI verification and JUnit evidence on the stated exact head.

### Material residual limitations

1. **Persistence/checkpoint atomicity:** SQLite commit and filesystem checkpoint replacement are separate resource operations. A crash between them can produce fail-closed unavailability. A trusted reconciliation/re-anchoring protocol is absent.
2. **Checkpoint trust:** the checkpoint is local. An attacker controlling both the database and checkpoint directory, or process memory and integrity keys, may defeat the current trust boundary.
3. **Key custody:** keys are supplied to the process and held in memory. There is no production KMS/HSM, independent key administration, attested workload identity, or compromise recovery.
4. **Trusted time:** event timestamps are synthetic caller-supplied values. Production must not rely on a client-provided timestamp for acceptance or authority decisions.
5. **Authority source:** the authority registry is local SQLite synthetic state. It is not an institutional appointment, delegation, or revocation system.
6. **Identity and access:** the prototype does not authenticate real people, bind identities to institutional accounts, or enforce a production authorization service.
7. **Operations:** production backup/restore, multi-host failover, capacity, monitoring, alerting, on-call, service-level objectives, and disaster recovery have not been demonstrated.

## 4. Target architecture (logical, vendor-neutral)

The recommended logical separation is:

1. **Identity provider (IdP):** authenticates individual users using institution-approved accounts and strong authentication.
2. **Authority and policy service:** resolves current and historical appointments, role grants, delegation, scope, validity and revocation. It must be independently auditable and must not infer authority merely from successful authentication.
3. **ORG-03 application/API:** validates each command, derives actor identity from a verified authentication context, asks the authority/policy service for a decision, and applies workflow rules.
4. **Transactional event store:** commits the event, aggregate state/version, idempotency record and durable publication/outbox record in one database transaction.
5. **Integrity and checkpoint service:** anchors committed event-stream heads in a separate administrative/security boundary and supports monotonic verification and controlled recovery.
6. **Key management service:** controls cryptographic keys, access policy, rotation, revocation and audit; private key material is not stored in application tables or source control.
7. **Notification adapters:** send email/SMS through approved providers, record provider delivery receipts separately from human acknowledgement, and use retry/dead-letter handling.
8. **Operations and audit plane:** centralized logs/metrics/traces, security monitoring, backup/restore, incident handling and controlled administrative access.

The application must not be the sole authority for its own identity assertions, signing keys, trusted time, checkpoint state, and audit evidence. These trust functions require explicit separation of duties and independently controlled evidence.

## 5. Production requirements by domain

### 5.1 Persistence and transaction design

**Required decision:** select a supported production relational database only after data classification, hosting, recovery, concurrency, jurisdiction, support and institutional ownership requirements are approved. PostgreSQL is a candidate for evaluation, not an approved selection.

Required capabilities:

- ACID transactions with documented isolation semantics.
- Atomic commit of event append, aggregate version/state transition, idempotency outcome and outbox record.
- Unique constraints for event identity, per-stream sequence and idempotency scope.
- Optimistic version checks or equivalent concurrency control; no last-write-wins for acknowledgement or escalation transitions.
- Append-only event history enforced through database permissions and controlled write paths, not merely application convention.
- Database roles separated between application writer, read-only auditor, migration operator and platform administrator.
- Explicit schema versioning, migration review, tested rollback/forward-recovery strategy and compatibility policy.
- Encryption in transit and at rest, protected backups, retention and deletion policy consistent with legal/institutional requirements.
- Connection pooling limits, query/lock timeouts, bounded retries and observable contention.
- Transactional outbox or equivalent to avoid claiming a notification was sent merely because an event committed.
- Reconciliation for event-store, aggregate, outbox and checkpoint divergence.

Acceptance evidence must include multi-process and multi-host concurrency tests, isolation tests, failover tests, load/soak tests at an institution-approved capacity target, and restore tests from independently protected backups.

**Unresolved decisions:** database engine and version, hosting location, data residency, RPO/RTO, retention, backup ownership, HA topology, capacity, operational support, and whether event history and personal data require separate stores.

### 5.2 Trusted timestamps and time semantics

Production event time must be generated by a trusted server-side component after authentication and before authorization/commit. Client-supplied time may be retained only as explicitly labelled, untrusted metadata; it must never establish event acceptance or backdate authority.

Requirements:

- Use UTC timestamps with explicit precision and unambiguous serialization.
- Synchronize hosts to institution-approved, monitored time sources; monitor offset, drift, synchronization loss and clock-step events.
- Record distinct times where needed: client-observed time, server-received time, authorization decision time, database commit time, provider delivery time, and human acknowledgement time.
- Define which timestamp is authoritative for each state transition and legal/audit question.
- Ensure monotonic ordering uses stream sequence/transaction order, not wall-clock ordering alone.
- Store authority validity intervals and revocation-effective times with explicit semantics, including how delayed, corrected or disputed revocations are handled.
- Define behavior when time synchronization is unhealthy: fail closed for high-risk authority-sensitive actions or route to an explicitly approved contingency process.
- Consider an external trusted timestamping or signed time-attestation mechanism for audit evidence where threat model and legal requirements justify it.

Acceptance: clock skew, source outage, backward/forward clock step, delayed message, concurrent event and revocation, and timestamp replay tests; operational evidence of time-source monitoring and alert response.

**Unresolved decisions:** authoritative time source, allowed drift, timestamp precision, time attestation requirement, and institutional policy for effective-time disputes.

### 5.3 Identity, authentication and authority

Authentication and institutional authority are separate controls. A valid login proves control of an account under the IdP's assurance; it does not prove that the person currently holds a particular office or may act on a particular alert.

Requirements:

- Use an institution-approved IdP and federation protocol (for example OIDC or SAML, subject to the IdP's actual capabilities).
- Unique human identities; no shared responder accounts for attributable actions.
- MFA proportionate to action risk, with phishing-resistant methods preferred for privileged or high-impact operations where supported.
- Verified issuer, audience, signature, expiry, nonce/state and session properties; short-lived access tokens and controlled refresh/revocation.
- Lifecycle controls for onboarding, role changes, suspension, departure, lost credentials and emergency access.
- A separate authority registry/service for office, appointment, role, scope, delegation, start/end time, approving authority, evidence reference and revocation.
- Versioned, immutable authority decisions; each event stores a verifiable reference or signed evidence snapshot sufficient to reconstruct why the action was authorized at that time.
- Explicit delegated authority chain and limits; delegation cannot exceed the delegator's authority and must have scope and expiry.
- Separation of duties for grant issuance, revocation, policy administration and security administration.
- Deny by default, least privilege, record/alert scoping and field/action-specific authorization.
- Re-evaluate authority at the defined commit boundary for sensitive actions; document race handling when revocation and action are concurrent.
- Emergency/break-glass access requires time limits, reason, additional approval where practicable, enhanced logging and post-event review.

Acceptance: account lifecycle, compromised account, token replay, privilege escalation, stale grant, cross-scope, delegation-chain, concurrent revocation/action, and emergency-access tests. Institutional governance must identify who is authorized to appoint, delegate, approve, revoke and audit.

**Unresolved decisions:** IdP, identity proofing standard, MFA policy, authoritative office/appointment source, authority approvers, delegation rules, emergency authority, and evidence retention.

### 5.4 Cryptographic key custody and lifecycle

Application-held synthetic test keys are not a production key-management design.

Requirements:

- Use institution-approved KMS/HSM-backed key custody, selected through security and procurement review.
- Separate keys by purpose: event authentication/signing, checkpoint signing, transport, database/storage encryption and backup encryption. Avoid cross-purpose key reuse.
- Prefer asymmetric signatures for independently verifiable audit evidence where the architecture requires third-party verification; use HMAC only where shared-secret verification and trust boundaries are explicitly justified.
- Bind key use to workload identity and least-privilege service policy; application operators must not be able to export root/private key material.
- Define key generation, activation, versioning, rotation, overlap, retirement, revocation, backup/escrow if permitted, destruction and emergency compromise response.
- Preserve historical verification after normal rotation without retaining compromised keys as trusted indefinitely.
- Establish how compromised signatures/checkpoints are quarantined and how a new trust epoch is anchored.
- Log key administration and signing operations to a separately protected audit stream.
- Prohibit secrets in source code, repository files, CI logs, SQLite records, ordinary environment dumps or developer workstations.
- Require two-person control or equivalent for root-key and trust-policy changes where feasible.

Acceptance: rotation with historical verification, unauthorized key-use denial, service identity compromise, key revocation, KMS/HSM outage, restore, compromise response and trust-root rollover exercises.

**Unresolved decisions:** KMS/HSM provider and ownership, key algorithms/parameters, signer topology, administrative quorum, escrow policy, recovery objectives, and key retention/retirement policy.

### 5.5 Checkpoint administration and independent integrity anchoring

A local sidecar file is not an independent production checkpoint.

Requirements:

- Store checkpoints in a separate security/administrative boundary from the event database and application host.
- Anchor stream identity, sequence, event-head digest, schema/version, signing-key identity, and trusted anchor time.
- Enforce monotonic sequence/epoch progression and detect rollback, fork, deletion, stale replay and unauthorized re-anchoring.
- Use a signing service or independently controlled witness/anchor service; application database administrators must not be able to silently rewrite both event history and its trust anchor.
- Define checkpoint frequency and maximum unanchored event window; high-risk events may require synchronous anchoring before acknowledgement is reported complete.
- Make checkpoint writes idempotent and support safe retries after timeout.
- Specify failure behavior: reject or quarantine integrity-sensitive reads/writes when the trusted anchor cannot be checked; do not silently fall back to a local checkpoint.
- Provide a controlled reconciliation procedure for a database commit that succeeds but whose checkpoint operation fails, and the inverse failure case.
- Require dual authorization, evidence capture and immutable audit record for re-anchoring or trust-epoch reset.
- Test backup restoration against the latest externally held anchor before restored data is made available.

Acceptance: database-only rewrite, checkpoint-only rewrite, joint administrative compromise assumptions, rollback/fork, missing anchor, delayed anchor, partial commit, network partition, witness outage, restore-to-old-backup and authorized re-anchor tests.

**Unresolved decisions:** independent administrator, anchor technology, witness count/quorum, anchor cadence, maximum unanchored window, retention, and disaster recovery ownership.

### 5.6 Operational controls and service readiness

Production readiness requires a named service owner and operational capability, not only passing unit tests.

Minimum control set:

- Approved service owner, data owner, security owner, database owner and on-call escalation path.
- Documented operating hours, coverage model, business calendar, holidays, time zone and after-hours authority.
- Approved primary/backup responder roster, acceptance evidence, role scopes and periodic recertification.
- Separate notification delivery, provider receipt, human acknowledgement and escalation states.
- Provider retry/backoff, deduplication, dead-letter queue, delivery reconciliation and manual fallback procedure.
- Health checks and monitoring for database, event lag, checkpoint age, signature failures, time drift, queue depth, delivery failures, lock contention, authentication anomalies and authority changes.
- Actionable alert thresholds, runbooks, paging ownership and tested escalation.
- Centralized structured logs, metrics and traces with correlation IDs; avoid logging secrets or unnecessary restricted data.
- Tamper-resistant audit export and retention schedule; audit access itself is logged.
- Vulnerability management, dependency/SBOM review, patch windows, secure configuration and periodic penetration/security review.
- Threat model, data-flow inventory, privacy impact assessment and records classification before real data is introduced.
- Backup encryption, immutable/offline or independently protected copies, regular restore tests and documented RPO/RTO.
- Disaster recovery and business continuity exercises, including identity, KMS, checkpoint, database and notification-provider outages.
- Change management, release approvals, rollback/forward-fix criteria and separation of duties.
- Incident response covering account compromise, key compromise, event-integrity failure, unauthorized access, data exposure and service outage.

Acceptance requires evidence from tabletop and technical exercises, not policy documents alone. No live institutional rehearsal is implied by this assessment.

## 6. Recommended trust and transaction flows

### 6.1 Human acknowledgement

1. Client authenticates with institutional IdP.
2. API validates identity/session and obtains a server-side identity subject.
3. API requests authority decision for actor, action, alert scope and current time.
4. API validates expected aggregate version and idempotency semantics.
5. Database transaction atomically commits event, aggregate update, idempotency result and outbox record.
6. Integrity anchor is advanced according to the approved checkpoint policy.
7. Only after the required commit/anchor condition is met does the API report the defined acknowledgement outcome.
8. Notification/outbox processing and provider delivery are recorded independently; provider delivery is never treated as human acknowledgement.
9. Audit records preserve identity, authority evidence reference, trusted timestamps, decision, event sequence and correlation IDs.

The final design must explicitly choose whether anchoring is synchronous for every event, synchronous only for high-risk events, or asynchronous with a documented exposure window. That choice is a risk decision, not an implementation convenience.

### 6.2 Revocation race

Authority revocation and a sensitive responder action must have a deterministic ordering rule. The design must identify the authoritative decision/commit point and produce one auditable outcome when the two operations race. A client timestamp must not decide the winner. A revoked or expired authority must not be resurrected by replaying an older grant or event.

### 6.3 Recovery after partial failure

The design must distinguish:
- event transaction did not commit;
- event committed but external checkpoint did not advance;
- checkpoint advanced but client did not receive response;
- outbox record committed but notification delivery is pending;
- provider delivered but receipt callback was delayed or duplicated.

Every case needs a deterministic retry/reconciliation procedure, no duplicate human acknowledgement, no silent history rewrite, and a durable audit trail.

## 7. Architecture decisions register

| ID | Decision | Recommendation | Status |
|---|---|---|---|
| ADR-01 | Production database | Evaluate supported transactional relational DB; PostgreSQL may be assessed | OPEN |
| ADR-02 | Event/aggregate transaction | Atomic event, aggregate, idempotency and outbox commit | REQUIRED |
| ADR-03 | Trusted time | Server-generated UTC plus monitored trusted time source | REQUIRED |
| ADR-04 | Identity | Institution-approved federated IdP with unique human identities and MFA | OPEN |
| ADR-05 | Authority | Separate governed, versioned appointment/delegation/revocation authority | REQUIRED |
| ADR-06 | Key custody | Institution-approved KMS/HSM with separated key purposes and duties | OPEN |
| ADR-07 | Checkpoint | Independent monotonic anchor outside DB/application administration | REQUIRED |
| ADR-08 | Checkpoint cadence | Risk-based; define maximum unanchored exposure and synchronous cases | OPEN |
| ADR-09 | Notification | Transactional outbox; provider receipt distinct from human acknowledgement | REQUIRED |
| ADR-10 | Recovery | Approved RPO/RTO, immutable backups, restore and reconciliation drills | OPEN |
| ADR-11 | Operations | Named owners, coverage, runbooks, monitoring and incident response | REQUIRED |
| ADR-12 | Data governance | Classification, residency, retention, privacy and audit access policy | OPEN |

## 8. Threat model and minimum assurance cases

The production threat model must include at least:

- malicious or compromised application process;
- database administrator or database credential compromise;
- checkpoint administrator compromise;
- KMS/HSM operator or workload identity compromise;
- stolen/replayed user session or compromised IdP account;
- malicious or stale authority grant/delegation;
- concurrent acknowledgement, escalation and revocation;
- time-source manipulation, clock drift and delayed events;
- partial network partition between database, KMS and checkpoint service;
- malicious insider with access to multiple administrative planes;
- ransomware, backup deletion, rollback to stale backup and regional outage;
- notification provider outage, duplication or delayed delivery;
- unauthorized access to restricted records and audit logs.

For each threat, the final security case must identify preventive, detective and recovery controls, owner, evidence, residual risk and acceptance authority. The threat model must explicitly state which colluding-administrator scenarios are in and out of scope.

## 9. Migration strategy and gates

No migration is authorized by this assessment. If a later production implementation is proposed, use separate Owner-approved stages:

- **P0 — Institutional discovery:** confirm legal/records obligations, data classification, office/authority model, service owner, operating model, residency, RPO/RTO and budget/support constraints.
- **P1 — Architecture freeze:** approve database, IdP, authority service, KMS/HSM, checkpoint administration, time source, notification boundaries, threat model and trust assumptions.
- **P2 — Detailed security design:** data flows, schemas, transaction contracts, cryptographic protocols, failure semantics, threat model, audit and recovery plans; independent review before implementation.
- **P3 — Controlled implementation:** separate authorization required; synthetic test environment first; no production identities or restricted records until explicit gates pass.
- **P4 — Verification and operational acceptance:** independent security review, multi-process/multi-host/fault-injection tests, restore/DR evidence, privacy/security approvals, operational runbooks and named responders.
- **P5 — Deployment:** separate explicit Owner approval. This is not authorized.

The existing A1–A5 governance remains controlling. This P0–P5 outline is a production-specific planning aid, not a replacement for or automatic advancement of those stages.

## 10. Production acceptance matrix

| Domain | Required evidence | Current status |
|---|---|---|
| Persistence | Approved DB architecture; atomicity/isolation; multi-host concurrency; backup/restore | NOT MET |
| Trusted time | Approved time source; drift monitoring; timestamp semantics; failure tests | NOT MET |
| Identity | IdP integration design, assurance/MFA and lifecycle controls | NOT MET |
| Authority | Institutionally approved grants/delegations/revocations and immutable evidence | NOT MET |
| Key custody | KMS/HSM design, ownership, rotation and compromise recovery evidence | NOT MET |
| Checkpoint | Independent anchor, monotonicity, dual control and recovery tests | NOT MET |
| Operational controls | Named owners, roster, coverage, runbooks, monitoring and incident response | NOT MET |
| Privacy/data governance | Classification, lawful basis, retention, residency and access policy | NOT MET |
| Independent security review | Independent review of production design and implementation | NOT OBTAINED |
| Prototype CI | Exact-head synthetic test and quality evidence | PASS — prototype scope only |
| Operational readiness | Institutional evidence and rehearsed controls | NOT VERIFIED |
| Production readiness | All production gates | NOT READY |
| A5 | Separate Owner authorization | NOT AUTHORIZED |

## 11. Decisions required from institutional governance

Before architecture freeze, the institution must identify and approve:

1. The accountable service owner and data controller/owner.
2. Which offices may appoint, delegate, suspend and revoke ORG-03 responder authority.
3. The authoritative identity source and required identity assurance/MFA level.
4. The operating calendar, time zone, business hours, holiday rules and emergency coverage.
5. Data classification, retention, audit access, residency and privacy obligations.
6. Service availability targets, RPO/RTO, expected concurrency and support capability.
7. Who administers the database, keys, checkpoint anchors and audit evidence, including separation of duties.
8. Approved notification channels/providers and manual fallback.
9. The independent security reviewer and acceptance authority for residual risk.

No institutional names, office holders, vendors, budgets, calendars or legal conclusions are assumed in this assessment.

## 12. Final disposition

- **Assessment:** PREPARED.
- **Prototype R1–R6 implementation:** recorded as complete for the synthetic prototype.
- **Prototype exact-head CI:** PASS for the recorded workflow/head.
- **Production architecture:** NOT FROZEN.
- **Production persistence/identity/authority/key/checkpoint services:** NOT SELECTED OR IMPLEMENTED.
- **Independent external security review:** NOT OBTAINED.
- **Operational readiness:** NOT VERIFIED.
- **Production readiness:** NOT READY.
- **A5 / deployment:** NOT AUTHORIZED.

The next valid step is institutional P0 discovery and Owner review of this architecture assessment. Any subsequent architecture freeze or implementation must be separately approved. No code, configuration, database, identity integration, keys, providers, or production data were changed as part of this assessment.
