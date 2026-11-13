# ORG-03 Production Architecture Annex

**Document ID:** EKHC-ORG03-A1-ARCH-002  
**Status:** Draft for Owner/institution decision — not implementation authorization  
**Applies to:** Proposed future production architecture only  
**Synthetic baseline:** `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`

## 1. Normative interpretation

This annex defines design constraints and acceptance questions. It does not select vendors, assert that institutional services exist, or authorize runtime changes. Terms such as MUST and MUST NOT express proposed production requirements, subject to formal A1 approval.

## 2. Trusted time and timestamp assurance

### 2.1 Separate time concepts

The design MUST distinguish:
- **Observed event time:** UTC wall-clock time recorded by the service at event acceptance.
- **Monotonic elapsed time:** process/host monotonic source used for local duration measurement and timeout handling; never treated as a portable calendar timestamp.
- **Authoritative time source:** institution-approved source(s), synchronization method, operators and monitoring.
- **Business-time interpretation:** approved IANA time-zone identifier, calendar version, holiday/working-hour source and SLA calculation version.
- **Independent timestamp evidence:** optional cryptographic or external timestamp evidence where legal, evidentiary or risk requirements demand stronger assurance than a server timestamp.

A client-supplied timestamp MUST be retained only as untrusted claimed metadata, never as the authoritative event time.

### 2.2 Clock trust and failure

Before A1 closure, the institution must decide the authoritative time source, authenticated synchronization protocol, redundancy, source hierarchy, maximum permitted offset, drift alert threshold, holdover behavior, leap-second handling, and accountable operator. No numeric tolerance is assumed in this draft.

Services MUST monitor synchronization state and record source identity, observed offset/uncertainty where available, and clock-health status with security-relevant events. A clock outside approved tolerance, a rollback, an unexplained jump, or disagreement between sources MUST trigger a defined degraded mode. The workflow MUST NOT silently recalculate historical deadlines or rewrite event times.

If trustworthy time is unavailable, the system must preserve sequence and monotonic observations, mark time assurance as degraded, and apply a separately approved fail-closed or restricted-operation policy. It must not claim an SLA result whose time basis is unknown.

### 2.3 Event timestamp evidence

Each accepted event should bind:
- event identifier and aggregate identifier;
- aggregate sequence/version and prior-event digest;
- authoritative UTC timestamp and time-source/assurance metadata;
- actor/service identity and authority-evidence reference;
- event schema/version and canonical payload digest;
- correlation/idempotency identifier;
- applicable SLA/calendar/time-zone rule version;
- integrity key identifier and independent checkpoint reference where applicable.

A cryptographic MAC/signature authenticates a statement relative to a key; it does not independently prove when the statement existed. If independent timestamping is required, specify the trusted timestamp authority, request/response evidence, verification policy, retention, outage behavior and long-term validation process.

### 2.4 SLA computation

SLA calculation MUST be deterministic and reproducible from the recorded event, approved calendar version, time zone, holiday data and policy version. Store the original deadline and calculation inputs. Calendar corrections apply prospectively unless a formally authorized correction event records the reason, authority, affected records and before/after interpretation. Late acknowledgement never erases a breach.

## 3. Persistence, transaction and distributed-concurrency architecture

### 3.1 Logical data model

At minimum, define separate durable concepts for:
- alert/workflow aggregate and current version;
- append-only domain event;
- idempotency request/result record;
- transactional outbox message;
- provider delivery attempt/receipt;
- human acknowledgement and responsibility acceptance;
- authority/assignment evidence reference;
- audit/security event;
- schema, policy, calendar and migration versions.

Restricted source records remain in their authoritative records system unless a documented classification and custody decision approves another arrangement. ORG-03 should persist the minimum reference and workflow metadata necessary for its purpose.

### 3.2 Atomic command boundary

A successful command MUST atomically commit:
1. aggregate version transition;
2. append-only event(s);
3. idempotency key, authenticated request fingerprint and deterministic result reference;
4. outbox intent for any required asynchronous side effect.

No provider call occurs inside the database transaction. A command either commits all durable intent or none. The caller receives a stable result only after commit is confirmed. Ambiguous commit outcomes are resolved by querying the durable idempotency record, not by blindly repeating a non-idempotent operation.

### 3.3 Concurrency and ordering

The final database design must select and document transaction isolation, locking/optimistic version checks, uniqueness constraints, serialization/retry behavior and deadlock policy. Concurrent commands against one aggregate MUST use compare-and-swap/version enforcement or an equivalent serializable aggregate boundary. The system must reject stale transitions and preserve a single authoritative event order per aggregate.

Multi-instance workers MUST claim outbox work with a database-supported lease/claim mechanism that is safe under process death and lease expiry. Duplicate delivery attempts are expected; provider adapters require idempotency where supported, and downstream effects must be deduplicated. Exactly-once external delivery must not be claimed.

### 3.4 Outbox, inbox and poison messages

Outbox state should distinguish pending, leased, attempted, provider-accepted, provider-rejected, retry-scheduled, exhausted and administratively quarantined. Provider delivery receipts remain separate evidence. Inbound webhooks require signature/authenticity verification, replay protection, event identity validation and durable inbox deduplication.

Retries require bounded backoff, jitter, maximum age/attempt policy, provider rate limits and alerting. Poison messages enter a quarantine workflow with controlled inspection and re-drive authorization; they must not block unrelated aggregates.

### 3.5 Failure and recovery matrix

| Failure | Required behavior/evidence |
|---|---|
| Process termination before commit | No partial command; safe retry via idempotency |
| Process termination after commit, before response | Resolve prior result from durable idempotency record |
| Worker termination after provider acceptance | Reconcile receipt/deduplicate; do not assume unsent |
| Database unavailable | No false success; bounded retry and explicit degraded state |
| Disk full / write failure | Transaction rollback, alert, protect existing evidence |
| Network partition | No split-brain aggregate ownership; reject uncertain writes |
| Key service unavailable | Fail closed for integrity-critical writes; read policy explicitly defined |
| Clock source unavailable | Mark time assurance degraded; apply approved SLA policy |
| Backup restore | Restore DB, outbox and integrity metadata consistently; verify chain/checkpoints |
| Regional/host loss | Follow approved RPO/RTO and independent recovery-domain plan |

### 3.6 Data lifecycle

A1 must identify retention classes and authority for event history, personal data, contact details, provider payloads, audit records, idempotency data, backups and legal holds. Deletion must respect legal retention and evidence-preservation rules. Crypto-erasure, anonymization or redaction must not silently invalidate event-chain verification; design explicit tombstone/redaction events and key-retention policy.

## 4. Identity, institutional authority and authorization

### 4.1 Distinct trust assertions

The system must not collapse these assertions:
1. **Authentication:** who controls the current authenticated credential/session?
2. **Institutional identity:** which authoritative subject does that credential represent?
3. **Appointment/role:** what institutionally recorded position or role is effective at the relevant time?
4. **Delegation:** who granted a bounded authority to whom, for which scope and period?
5. **Authorization:** may this subject perform this action on this organization/record/field now?
6. **Evidence attribution:** what verifiable evidence supports the actor and authority claims for a historical event?

A successful login is not proof of appointment or authority.

### 4.2 Authority evidence

Institution-approved authority records should include stable subject and organization identifiers, authority type, scope, source system/reference, issuer, approval evidence, effective-from and effective-until instants, recorded-at time, revocation effective time, version, and integrity evidence. Corrections create new versions or revocation events; historical evidence is not overwritten.

The institution must define which body or office can appoint, suspend, revoke and delegate each authority class. Conflicting appointments, unknown issuers, stale synchronization, missing approvals and ambiguous effective times fail closed for privileged actions.

### 4.3 Delegation and separation of duties

Delegation must be explicit, purpose-limited, scope-limited, time-bounded, non-transitive by default and independently revocable. The record must identify delegator, delegate, authority basis, scope, restrictions, start/end and approval evidence. The delegate cannot grant broader authority than the delegator holds.

High-impact actions may require dual control: one actor proposes and a separate authorized actor approves. Define incompatible role combinations, administrator break-glass controls, emergency authority and post-event review.

### 4.4 Service identities

Every service identity must have an owner, purpose, least-privilege scope, credential/certificate lifecycle, rotation and revocation path, environment restriction, audit trail and expiry/review date. Human accounts must not be used as shared service credentials. Service-to-service trust must be mutually authenticated and bound to workload identity where supported.

### 4.5 Authorization evaluation

Authorization must be server-side, deny-by-default and evaluated against current authoritative status plus historical event-time authority as required. Policy inputs and policy version should be auditable without copying unnecessary personal data. Define cache TTL/invalidation and emergency revocation latency. The UI is never an enforcement boundary.

## 5. Key custody and cryptographic operations

### 5.1 Trust separation

The production design must separate application runtime administration, key-custodian authority, security audit and backup administration. Application operators must not be able to export or silently replace root integrity keys. No production key may be committed to source, issue text, CI logs, ordinary application config or synthetic fixtures.

### 5.2 Key hierarchy and lifecycle

Document key purpose, algorithm, size, owner, custodian, key identifier, permitted operation, environment, creation/activation/retirement/revocation times, rotation overlap, backup/recovery method and destruction authorization. Separate keys by purpose and environment. Define root/intermediate/data-signing or MAC key hierarchy only after security authority review.

Rotation must preserve historical verification without permitting revoked keys to authorize new events. Compromise response must specify containment, revocation effective time, trust-anchor replacement, event-range impact analysis, re-attestation/checkpoint strategy and notification obligations.

### 5.3 MAC, signatures and non-repudiation

Choose MAC or digital signatures based on threat model and evidence requirements. A MAC is appropriate for integrity among trusted services sharing a secret, but any holder of the MAC key can generate valid tags. A signature can support verifier separation but does not automatically prove human intent, identity or time. If non-repudiation is claimed, specify identity binding, signing ceremony, key custody, intent confirmation, audit and legal acceptance.

### 5.4 Independent checkpoints

The checkpoint trust domain must be independent of the primary database and application administrator threat domain. Specify authenticated write protocol, monotonic sequence/epoch, retention, anti-rollback, replication, recovery and verification. A local file on the same host is not an independent trust anchor. Loss or disagreement of the external checkpoint must enter a documented fail-closed reconciliation procedure.

### 5.5 Key ceremonies and outage

Define dual-control key generation/import, activation, backup, rotation, revocation, destruction and recovery ceremonies. Record participants, approvals, device/service identity, time evidence, key IDs and audit references without recording secret material. KMS/HSM outage policy must distinguish read-only verification from integrity-critical writes and must not silently downgrade to local keys.

## 6. Operational, deployment and service architecture

### 6.1 Environment separation

Production, staging, development and test must have separate identities, keys, data stores, provider destinations and access roles. Synthetic test data only in non-production. Production data must not be copied into developer environments without a separately approved lawful and secure process. CI must not receive production secrets.

### 6.2 Deployment and change control

Define immutable build provenance, dependency/SBOM generation, vulnerability policy, artifact signing/verification, environment promotion, migration review, approval separation, rollback/roll-forward strategy and emergency change audit. Database migrations require compatibility and recovery plans. Feature flags for identity, restricted records and outbound notifications default OFF and require separately authorized activation.

### 6.3 Availability and service objectives

Institution owners must set availability, latency, capacity, RPO and RTO objectives. Define service dependency map, health/readiness checks, overload behavior, queue depth limits, rate limits, graceful degradation and maintenance windows. A health endpoint must not disclose sensitive state.

### 6.4 Monitoring and incident response

Log security-relevant actions with actor/service, authority decision reference, correlation ID, outcome, timestamp assurance and policy version. Avoid credentials, full restricted content and unnecessary personal data. Protect logs against alteration and unauthorized search/export.

Define severity, detection source, on-call ownership, escalation, evidence preservation, containment, communication, recovery and post-incident review for identity compromise, key compromise, data exposure, event-integrity failure, wrong-recipient notification, clock failure and unavailable dependencies.

### 6.5 Operational readiness evidence

Before live rehearsal, require named primary/backup operators, accepted assignments, verified contact routes, approved calendar and time zone, runbooks, stop/rollback controls, tested recovery, provider test environment, privacy-approved payloads, incident contacts and written go/no-go authorization. This annex does not authorize rehearsal.

## 7. A1 acceptance checklist

| Domain | Required A1 artifact / decision | Status |
|---|---|---|
| Trusted time | Source hierarchy, synchronization, drift policy, outage/degraded mode, evidence model | OPEN |
| SLA semantics | Calendar authority, timezone, deadline versioning and correction policy | OPEN |
| Persistence | Data model, transaction boundary, isolation and concurrency contract | OPEN |
| Outbox/inbox | Delivery state machine, deduplication, retry and quarantine | OPEN |
| Recovery | Approved RPO/RTO, backup trust domain, restore verification | OPEN |
| Identity | Authoritative IdP/subject lifecycle and service identity | OPEN |
| Authority | Appointment, delegation, revocation, historical evidence | OPEN |
| Authorization | RBAC/ABAC policy, scope, break-glass, separation of duties | OPEN |
| Key custody | KMS/HSM, custodians, ceremonies, compromise and recovery | OPEN |
| Operations | Environment, deployment, monitoring, incident and readiness model | OPEN |
| Governance | Classification, privacy, retention, legal hold and data residency | OPEN |

**Disposition:** requirements specified as a design proposal; all institution-specific selections and evidence remain unresolved. No production implementation is authorized.
