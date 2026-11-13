# ORG-03 Production Integration — A1 Architecture Review

**Document ID:** EKHC-ORG03-A1-ARCH-001  
**Date:** 2026-11-13  
**Status:** DRAFT FOR OWNER DECISION — NOT APPROVED FOR IMPLEMENTATION  
**Baseline:** Synthetic A3 branch head `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`  
**Scope:** Architecture assessment only. No runtime, database, identity, notification, or restricted-record implementation is authorized by this document.

## 1. Executive decision

**Recommendation: NO-GO for production integration until the prerequisites and decisions in this review are resolved and separately approved.**

The current ORG-03 implementation is a synthetic event-store and policy prototype. Its successful synthetic integrity, authority, transition, roster, and access-policy tests do not establish institutional identity assurance, production data custody, legal/records compliance, real notification delivery, operational coverage, or disaster recovery.

This review proposes a bounded target architecture and an ordered decision process for a future A1 specification. It does not approve A2 reconciliation, A3 production implementation, live rehearsal, operational activation, or A5 deployment.

## 2. Verified current boundary

The existing implementation and regression tests deliberately establish these limits:

- No Django product apps, ORM-backed ORG-03 persistence, or production migrations are enabled.
- Django uses a dummy database backend; the health endpoint is the only registered application route.
- No real institutional authentication, sessions, access tokens, identity-provider integration, or staff directory is connected.
- Restricted records, real responder identities, contact details, and institutional channels are not loaded by the synthetic roster or access-policy harness.
- The synthetic event store uses process-held test keys and a local independently authenticated checkpoint file. That checkpoint is not an external trust anchor or a separate disaster-recovery failure domain.
- No real email, SMS, push, telephony, messaging provider, or institutional notification route is configured.
- The acknowledgement/escalation acceptance matrix records live rehearsal as NOT RUN pending separate Owner authorization.

These constraints are intentional. They must remain regression-protected until a later architecture and implementation stage is explicitly approved.

## 3. Goals and non-goals

### 3.1 Goals for a future production design

1. Preserve append-only, attributable, time-stamped workflow evidence.
2. Authenticate every human and service actor through an institution-approved identity boundary.
3. Enforce organization-, record-, action-, and field-level authorization on the server.
4. Protect restricted information throughout storage, processing, transport, backup, export, and deletion.
5. Make notification delivery, human receipt, acknowledgement, escalation, and closure distinct auditable states.
6. Provide tested recovery, key rotation, revocation, retention, and incident-response procedures.
7. Support explicit organizational coverage calendars, holidays, time zones, accepted primary/backup assignments, and delegated authority.
8. Keep operational activation and deployment separately gated.

### 3.2 Non-goals

- No production implementation in this A1 review.
- No selection or procurement of a specific identity provider, database, cloud, KMS/HSM, or notification vendor.
- No assumption that a particular institutional directory, API, legal basis, policy, or data classification already exists.
- No conversion of synthetic authority fixtures into real institutional authority.
- No real recipient contact, message sending, rehearsal, or operational activation.
- No change to the approved synthetic A3 baseline.

## 4. Proposed logical architecture (subject to approval)

The recommended shape is a modular, server-side architecture with explicit trust boundaries. Technology selection is deferred until institutional constraints and hosting/security requirements are evidenced.

### 4.1 Trust zones and components

1. **Client zone:** web/mobile clients. Treat all client-provided identity, role, scope, timestamps, event payloads, and record identifiers as untrusted.
2. **Identity boundary:** institution-approved identity provider or federation, with strong authentication, session/token lifecycle, MFA policy, account disablement, and authoritative subject identifiers.
3. **Application/API boundary:** server-side authentication, authorization, input validation, rate limits, CSRF/session protections as applicable, and centralized policy enforcement. No direct client-to-database access.
4. **ORG-03 workflow service:** explicit state machine and SLA/coverage calculation. Domain transitions must be deterministic, versioned, and independently tested.
5. **Persistence boundary:** transactional relational persistence for workflow state and append-only event history. Event append, aggregate version update, idempotency record, and outbox insertion must commit atomically.
6. **Integrity/key boundary:** managed key service or HSM-backed key custody, key identifiers, rotation and revocation, narrowly scoped signing/MAC operations, and independent checkpoint/backup trust anchors. Do not place production secrets in source code, ordinary application configuration, or process-only test fixtures.
7. **Restricted-record boundary:** separate service or controlled repository adapter with its own authorization checks, classification, minimization, audit, retention, and export policy. ORG-03 should reference only the minimum necessary record identifier/metadata; avoid copying restricted content into notification payloads or general event logs.
8. **Notification adapter boundary:** asynchronous transactional outbox and provider adapters. Provider acceptance/delivery receipts must never be represented as human acknowledgement. Provider credentials and destinations are separately governed.
9. **Audit/monitoring boundary:** tamper-evident security and operational audit, alerting on policy denial, key events, delivery failure, clock anomalies, unusual exports, and administrative changes.
10. **Recovery boundary:** encrypted backups, independently protected integrity metadata, tested restoration, recovery objectives, and documented incident procedures.

### 4.2 Core workflow invariants

- Delivery requested, provider accepted, provider delivered, human acknowledged, accepted responsibility, escalation, disposition, and closure are distinct events.
- A provider receipt is not proof that a human saw or accepted an alert.
- Acknowledgement does not close an alert.
- Late acknowledgement records the actual timestamp and preserves the SLA breach; it must not rewrite the deadline.
- Missing/expired authority, unaccepted roster assignments, unknown coverage, failed delivery, invalid evidence, and uncertain state fail closed.
- Retries are idempotent only when the same authenticated request identity and event binding are proven.
- Event history is append-only; corrections are compensating events, never silent mutation.
- Time source, UTC event time, local display zone, business calendar, holiday calendar, and deadline calculation version are recorded.
- Primary-to-backup-to-Owner/delegate escalation requires explicit, current, independently verifiable authority and route evidence.

## 5. Production security requirements

### 5.1 Identity and authentication

Before implementation, identify the institutionally authoritative identity source, accountable owner, subject identifier lifecycle, joiner/mover/leaver process, MFA requirements, session/token standards, emergency access, service identities, and account revocation latency.

Authentication must not itself grant access. No authorization decision may rely on caller-constructed role claims without server-side validation and authoritative provenance. Delegation must be scoped, time-bounded, non-transitive unless explicitly approved, and revocable with a defined effective time.

### 5.2 Authorization and restricted records

Adopt deny-by-default authorization. Define policy dimensions at minimum for:
- subject and verified institutional status;
- organization scope and hierarchy;
- role, duty, and delegated authority;
- record classification and ownership/custody;
- action (read, create, acknowledge, route, amend, export, close, administer);
- field-level disclosure and purpose;
- time-bounded assignments and separation of duties.

Every restricted-record access must be checked at the service boundary, not merely in the UI or a caller-supplied object. Define break-glass access, approval, reason capture, alerting, retrospective review, and expiry. Keep secrets, credentials, personal contact data, and restricted content out of public artifacts, generic logs, and notification bodies.

### 5.3 Event integrity and key management

The synthetic HMAC implementation is a prototype, not a production key-management design. Production design must specify:
- approved cryptographic algorithms and key sizes;
- KMS/HSM custody, key ownership, separation of duties, access policy and audit;
- rotation, overlap, revocation, compromise response and historical verification;
- external/independent checkpoint storage and anti-rollback strategy;
- database, backup, and checkpoint consistency protocol;
- canonical serialization and schema/version migration;
- trusted time and clock rollback detection;
- restore validation and independent integrity verification.

A MAC proves integrity relative to a secret key; it does not by itself provide non-repudiation, trusted time, or protection if an attacker controls both the application and key service. Threat-model those claims explicitly.

### 5.4 Persistence, concurrency and recovery

Select the database only after hosting, sovereignty, support, backup, and operational constraints are known. Specify transaction isolation, uniqueness constraints, optimistic concurrency, idempotency retention, event ordering, outbox atomicity, retry semantics, and multi-instance locking.

Define and test:
- RPO/RTO approved by the accountable institution;
- encrypted, access-controlled, immutable or separately protected backups;
- restoration to a clean environment;
- point-in-time recovery and integrity verification;
- partial-write, crash, disk-full, network-partition, clock-skew, and key-service outage behavior;
- retention, legal hold, archival, deletion, and evidence-preservation rules.

The existing SQLite tests do not prove distributed database behavior, power-loss recovery, host compromise resistance, or disaster recovery.

### 5.5 Notifications and operational routing

Before any provider is selected, approve the authorized channels, destinations, provider data processing terms, message minimization, delivery receipt semantics, retries, rate limits, quiet hours, fallback rules, and failure escalation.

A roster must be based on an authoritative and maintained source, with primary and backup assignments accepted by the assigned people, verified contact routes, start/end times, time zone, holiday/leave coverage, and a documented Owner/delegate escalation route. A schema-valid roster is not proof of operational coverage.

No notification adapter may be enabled by default. Production sending must be separately feature-gated and disabled until authorized rehearsal and operational sign-off.

## 6. Data governance and institutional prerequisites

The following evidence is required before a production design can be frozen:

| Prerequisite | Required evidence | Current status |
|---|---|---|
| Institutional data classification | Approved classification and handling policy | NOT PROVIDED |
| Record ownership/custodianship | Named accountable roles and systems of record | NOT PROVIDED |
| Privacy/legal basis | Applicable legal, privacy, retention and cross-border requirements reviewed by institution | NOT PROVIDED |
| Identity authority | Approved identity source, MFA and lifecycle policy | NOT PROVIDED |
| Restricted-record access | Approved access matrix, field rules and break-glass process | NOT PROVIDED |
| Key custody | Approved KMS/HSM or equivalent custody model and key owners | NOT PROVIDED |
| Hosting/data residency | Approved hosting environment, location and administrator model | NOT PROVIDED |
| Responder roster | Verified assignments, accepted primary/backup, contacts and coverage calendar | NOT PROVIDED |
| SLA calendar | Approved business hours, holidays, timezone and clock semantics | NOT PROVIDED |
| Notification destinations | Approved providers, routes, recipient consent/authority and data terms | NOT PROVIDED |
| Audit/retention | Approved audit owner, retention, legal hold and disposal policy | NOT PROVIDED |
| Recovery | Approved RPO/RTO, backup custody and restoration test evidence | NOT PROVIDED |
| Incident response | Security incident, credential compromise and notification-failure playbooks | NOT PROVIDED |

Do not infer that missing evidence exists. Keep each item UNRESOLVED until an authoritative artifact and accountable approver are recorded.

## 7. Architecture decisions required from the Owner/institution

No option below is selected by this document.

| Decision | Options to assess | Required decision owner/evidence |
|---|---|---|
| Identity federation | Existing institutional IdP, approved federation, or institution-managed identity service | Institutional IT/security authority |
| Authorization model | RBAC plus organization-scoped ABAC/policy engine; delegated authority model | Governance and security owners |
| Persistence | Supported relational DB and hosting topology | IT operations, data owner |
| Restricted records | Existing records system integration vs separately governed service | Records custodians |
| Key custody | Institution KMS/HSM or approved managed service | Security/key custodian |
| Notifications | Institution-approved SMS/email/push/telephony providers | Communications and procurement |
| Audit | Central SIEM/log platform and immutable retention | Security/audit owner |
| Hosting | Institution-operated or approved hosted environment | IT/security and legal |
| Recovery | RPO/RTO, backup provider and independent trust domain | Operations and records owners |
| Time/SLA | Official time source, business calendar and holiday authority | Operations/governance |

## 8. Threat model to complete before A2

At minimum, assess:
- compromised or malicious responder, administrator, delegate, or service account;
- stolen session/token, MFA fatigue, identity-provider compromise and stale account;
- cross-organization and cross-record authorization bypass;
- replay, event substitution, truncation, deletion, reordering and database rewrite;
- compromise or rollback of both application and integrity key/checkpoint;
- key leakage, unauthorized rotation, premature revocation or loss of historical verification;
- malicious or compromised notification provider, spoofed delivery receipts, SIM swap and wrong recipient;
- concurrency races, retry storms, duplicate messages, out-of-order delivery and stale roster assignment;
- clock skew/rollback, calendar mistakes, missed SLA, holiday and timezone boundary;
- backup theft, restore to stale state, ransomware, host loss and insider tampering;
- restricted-data leakage through logs, analytics, exports, attachments, notifications and public repositories;
- denial of service and failure of identity, key, database, network or notification dependencies.

For each threat, document trust boundary, attack preconditions, impact, mitigations, detection, residual risk, test evidence and accountable risk acceptance.

## 9. Proposed stage gates

1. **A1 completion:** obtain authoritative institutional inputs; finalize data classification, trust boundaries, threat model, identity, record custody, hosting, key, persistence, notification, audit and recovery decisions. Record unresolved items and accountable owners. Submit this review and its companion decision register for explicit Owner/institution approval.
2. **A2 read-only reconciliation:** compare the approved architecture against actual institutional identity, records, hosting, policies, providers, legal requirements and current systems. No implementation changes.
3. **A3 production integration:** only after separate approval of the A1/A2 baseline and a bounded implementation plan. Production credentials and real personal/restricted data require their own authorization and secure test plan.
4. **A4 verification:** independent security review, integration tests, failure injection, access-control testing, backup restore, key rotation/revocation, audit verification, privacy review and approved acceptance evidence.
5. **Live rehearsal / operational activation:** separate explicit Owner authorization, named accountable operators, approved real destinations, rehearsed rollback/stop controls and written go/no-go decision.
6. **A5 deployment:** separate authorization after operational readiness and release controls pass.

## 10. Explicit prohibitions until separately authorized

- Do not add Django product apps, ORM models, migrations, database persistence, or production routes for ORG-03.
- Do not connect an institutional identity provider, create real authentication/session/token flows, or ingest institutional user/role data.
- Do not connect restricted-record systems, import real records, or process real personal/contact data.
- Do not configure real notification credentials, recipients, provider webhooks, or outbound delivery.
- Do not create production keys, use real secrets in tests, or claim production key custody from the synthetic HMAC design.
- Do not conduct live notification rehearsal, operational activation, deployment, merge, or A5.
- Do not weaken the existing synthetic-only boundary tests to make integration easier.

## 11. A1 review checklist and disposition

| Review item | Disposition |
|---|---|
| Current A3 boundary documented | VERIFIED from repository baseline |
| Synthetic-to-production gaps identified | DOCUMENTED |
| Proposed trust boundaries and logical architecture | DRAFT |
| Identity and authorization design | OPEN — institutional evidence required |
| Restricted-record architecture | OPEN — custodianship and classification required |
| Persistence and recovery design | OPEN — hosting and RPO/RTO decisions required |
| Key custody and independent checkpoint | OPEN — security authority decision required |
| Notification and roster architecture | OPEN — provider and operational evidence required |
| Threat model and risk ownership | DRAFT — independent review required |
| A1 Owner approval | NOT GRANTED |
| A2 authorization | NOT GRANTED |
| A3 production implementation | NOT AUTHORIZED |
| Live rehearsal / operational activation | NOT AUTHORIZED |
| A5 deployment | NOT AUTHORIZED |

**A1 disposition: PARTIAL / DRAFT FOR OWNER DECISION.** This document is a structured architecture review, not evidence that institutional prerequisites have been met. It must not be represented as an approved production architecture.

## 12. Revised A1 package map and completion criteria

This review is accompanied by the following documentation-only architecture artifacts on this branch:

- `docs/architecture/ORG-03-PRODUCTION-ARCHITECTURE-ANNEX.md` — normative design requirements for trusted time, persistence/concurrency, identity/authority, key custody, and operations.
- `docs/architecture/ORG-03-ARCHITECTURE-DIAGRAMS.md` — system context, trust-boundary/data-flow, deployment zones, and workflow sequence diagrams.
- `docs/architecture/ORG-03-ARCHITECTURE-DECISION-REGISTER.md` — decision records, decision owners, options, evidence, and explicit unresolved status.
- `docs/security/ORG-03-PRODUCTION-THREAT-REGISTER.md` — threat scenarios, controls, detection, residual risks, and acceptance ownership.
- `docs/governance/ORG-03-A1-OWNER-DECISION-RECORD.md` — Owner decision proposal and stage-gate disposition.

### 12.1 A1 completion criteria

A1 cannot be closed solely by completing repository documentation. Closure requires:

1. Each architecture decision has an identified institutional decision owner, approved option or explicit accepted deferral, supporting authoritative evidence, and recorded approval.
2. Trusted time, persistence semantics, institutional authority, key custody, operational topology, data governance, and recovery are specified to the level required by the annex.
3. Diagrams are reconciled with the written architecture and threat register.
4. Every threat has a disposition: mitigated with evidence, accepted by an authorized risk owner, or explicitly blocking.
5. Every missing institutional prerequisite has an accountable owner and evidence due condition; no missing item is silently treated as satisfied.
6. The synthetic A3 baseline and its regression protections remain unchanged.
7. The Owner explicitly approves the frozen A1 package before A2 can begin.

### 12.2 Status of this revision

The companion documents improve architectural completeness but do not supply missing institutional evidence. All vendor, institution, legal, identity, records, hosting, key-custody, roster, and operational decisions remain UNRESOLVED unless supported by an authoritative artifact. The package remains a proposal for Owner decision, not an approved architecture.

## 13. Related repository evidence

- Synthetic implementation: `scripts/org03_event_store.py`
- Synthetic access policy: `scripts/org03_synthetic_access_policy.py`
- Synthetic roster validation: `scripts/org03_roster.py`
- Synthetic transition model: `scripts/org03_events.py`
- Acknowledgement/escalation acceptance matrix: `docs/verification/ORG-03-ACKNOWLEDGEMENT-ESCALATION-ACCEPTANCE-MATRIX.md`
- Runtime boundary regression: `tests/test_access_control_boundary.py`

**Final control statement:** this A1 artifact is documentation-only. The production integration boundary, live rehearsal prohibition, operational activation prohibition, and separate A5 gate remain unchanged.
