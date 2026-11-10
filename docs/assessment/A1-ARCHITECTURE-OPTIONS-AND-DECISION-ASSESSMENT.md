# A1 Architecture Options and Decision Assessment

**Status:** Preliminary options assessment — not approved or frozen  
**Stage:** A1 only  
**Baseline:** Existing A1 architecture proposal, requirements catalogue, risk register, privacy assessment, and data-inventory workbook  
**Decision authority:** Owner approval after authoritative evidence and stakeholder validation  
**Scope:** Logical architecture, application shape, client channels, offline operation, hosting/operations, security boundaries, and decision dependencies

## 1. Purpose and decision boundary

This assessment compares architecture options to make A1 decisions evidence-ready. It is not a technical design specification, procurement decision, implementation authorization, or production deployment plan.

No programming language, framework, database, hosting provider, cloud vendor, mobile packaging approach, network topology, or service-level objective is selected by this document. Options and provisional preferences are hypotheses to validate.

The platform remains independent of ARNA/MASES, MaaleNex, IROKA, and unrelated systems. No code, schema, credentials, designs, or infrastructure from those projects are assumed reusable.

Organizational hierarchy, authority, and scope remain blocked on verification of the seventh-edition Constitution, current applicable bylaws, amendments, and approved mandates. Preserve exact Amharic terminology. Keep ቀጣና and ኅብረት distinct; do not infer relationships or unapproved translations.

## 2. Architecture drivers and evidence status

| Driver | Current direction | Evidence status | Consequence |
|---|---|---|---|
| Institutional fit | Reflect verified EKHC governance and operations | MISSING — governing sources | Avoid hierarchy-dependent schema and authorization design |
| Language and calendar | Amharic-first; Ethiopian calendar default; multilingual support | OWNER-DIRECTED; detailed glossary and workflow validation pending | Treat localization as a cross-cutting platform capability |
| Connectivity | Offline-capable operation | OWNER-DIRECTED direction; actual field profiles missing | Define offline behavior per workflow, not as blanket data replication |
| Channels | Web, Android, iOS, and PWA target direction | OWNER-DIRECTED target; user/device research missing | Compare channel strategies and capability limits |
| Security | Server-side, deny-by-default, least privilege | Proposed requirement; authority model unverified | Do not freeze roles, scopes, or permission tables |
| Privacy | Data minimization and protected sensitive information | Provisional assessment only; legal/policy validation missing | No live sensitive data or broad offline cache |
| Scale and performance | Suitable for institution-wide use | Workload and usage estimates missing | Do not over-engineer or claim capacity |
| Operations | Sustainable hosting, backup, recovery, support | Hosting and operating constraints unknown | Compare operating models before vendor selection |
| Interoperability | Controlled integrations and documented interfaces | System inventory missing | Avoid premature provider-specific coupling |
| Accessibility | Accessible user journeys | Target requires validation | Include in design and acceptance planning; no compliance claim |
| Maintainability | Understandable modular boundaries and supportable operations | Team capacity and support model unknown | Prefer low operational complexity unless evidence justifies more |

## 3. Candidate application architecture options

### Option A — Modular monolith with API boundary

A single deployable application organized into explicit internal domains and modules, with controlled module interfaces and a documented API for clients and integrations.

**Potential advantages**
- Lower operational and deployment complexity than a distributed system.
- Easier transactional consistency for related workflows.
- Clear domain boundaries can be enforced without operating many services.
- A practical starting point when workload, team size, and operational capacity are unknown.
- Can support web and mobile clients through governed application services.

**Risks and constraints**
- Poor module boundaries can create a tightly coupled monolith.
- Scaling individual workloads independently is limited.
- A single deployment may increase the impact of some failures.
- Requires architecture tests and dependency rules to prevent cross-domain coupling.

**Evidence needed**
- Candidate domain ownership and workflows.
- Expected transaction boundaries and workload profile.
- Team skills, deployment capability, and support model.
- Security review of module boundaries and API enforcement.

**Preliminary assessment:** Strong candidate for further evaluation because it limits operational complexity while preserving internal modularity. Not selected.

### Option B — Distributed services / microservices

Multiple independently deployable services organized around bounded contexts and communicating through APIs or asynchronous messaging.

**Potential advantages**
- Independent deployment and scaling where genuine workload differences exist.
- Stronger isolation for selected services when correctly designed.
- Separate teams can own service lifecycles where staffing supports it.

**Risks and constraints**
- Adds service discovery, network failure, distributed tracing, message delivery, versioning, and cross-service consistency concerns.
- Increases operational, security, monitoring, and deployment burden.
- Offline synchronization becomes harder when one user action spans multiple services.
- Requires mature service ownership, incident response, and automated delivery.

**Evidence needed**
- Demonstrated independent scaling or release needs.
- Sufficient engineering and operations capacity.
- Clear service boundaries and data ownership.
- Measured reasons why a modular monolith is insufficient.

**Preliminary assessment:** Do not select as the initial architecture without concrete evidence. Reconsider only if measured needs justify the added complexity.

### Option C — Serverless / managed function-oriented architecture

Application behavior split across managed functions and provider-managed services, with platform-specific event, identity, storage, and database integrations.

**Potential advantages**
- Reduced management of some infrastructure components.
- Elastic execution for suitable event-driven workloads.
- Potentially useful for discrete background jobs or integration adapters.

**Risks and constraints**
- Provider dependence, runtime limits, cold-start behavior, observability differences, and cost variability.
- Offline synchronization and long-running domain workflows still require deliberate application design.
- Vendor service availability, account access, data location, pricing, and contractual terms are unknown.
- A large function estate can fragment domain logic.

**Evidence needed**
- Provider and contract suitability.
- Data location and legal assessment.
- Workload and cost model.
- Portability, monitoring, support, and incident response assessment.

**Preliminary assessment:** Possible hosting/execution option for selected workloads, not a default platform architecture decision.

## 4. Candidate client and channel strategies

| Option | Description | Benefits | Risks / limitations | Evidence required |
|---|---|---|---|---|
| Responsive web + PWA | One web application installable where supported | Broad reach, shared release path, offline capability for carefully selected workflows | Browser/device differences; background sync, storage, and OS integration vary | Target devices, browser support, field connectivity, offline journeys |
| Web + cross-platform mobile application | Shared domain services/API with dedicated Android/iOS clients, potentially sharing selected UI/business logic | Better native integration and control over device capabilities | More build, signing, testing, release, and support work | Device inventory, team skills, app-store constraints, device APIs needed |
| Separate native Android and iOS applications | Independent native clients consuming shared APIs | Maximum platform-specific control | Highest implementation and maintenance burden; duplicated client work | Demonstrated native requirements, funding, staffing, support model |
| PWA first, native clients later | Progressive web baseline with staged native delivery if evidence justifies | Lower initial channel complexity while preserving API-driven expansion | Must avoid assuming PWA can meet every offline/device need | Critical journeys, device capability tests, stakeholder priorities |

**Provisional direction for evaluation:** validate a responsive Amharic-first web/PWA experience against actual target devices and workflows first, while maintaining an API boundary that does not prevent future Android/iOS clients. This is a sequencing hypothesis, not a reduction of the stated multi-channel target or a final product decision.

## 5. Offline architecture options

Offline support must be specified by workflow, data classification, and action risk. “Offline-first” does not mean every record is copied to every device.

### Pattern 1 — Read-only offline content

Approved content is cached for a limited period and refreshed when connectivity returns.

- Suitable candidates may include approved public or low-sensitivity reference content.
- Requires content versioning, expiry, cache deletion, and integrity checks.
- Must not silently retain withdrawn or superseded content indefinitely.

### Pattern 2 — Local drafts and queued submissions

A client records a draft or queued command locally and submits it after connectivity returns.

- Requires authenticated user and device context.
- Every command needs an idempotency key, schema/version compatibility, authorization re-check at submission, and clear status.
- A queued action must be rejected if the user's authority has expired or been revoked.
- User-visible states must distinguish saved locally, submitted, accepted, rejected, and requiring attention.
- Conflicts require workflow-specific resolution; never silently overwrite high-integrity governance or financial records.

### Pattern 3 — Connectivity-required sensitive actions

High-risk approvals, sensitive disclosures, privileged administration, and actions requiring current authority may require live connectivity and additional approval.

- Offline client state must not be treated as proof of current authority.
- No queued action may bypass approval or segregation-of-duties checks.
- Emergency exceptions must come from verified policy, not software invention.

### Offline control requirements to assess

- Minimize data by field and workflow.
- Apply the provisional privacy classes from the A1 privacy assessment; no C3 routine offline cache.
- Encrypt local data and protect encryption keys.
- Use device/session controls appropriate to shared-device realities.
- Set cache expiry and logout/revocation deletion behavior.
- Protect notification previews, local search indexes, attachments, and app-switcher snapshots.
- Authenticate synchronization and protect transport.
- Use idempotency, version checks, replay protection, and attributable audit events.
- Define conflict ownership and user resolution for each workflow.
- Test device loss, prolonged disconnection, account revocation, duplicate submission, clock drift, partial upload, and application upgrade.
- Define safe behavior when server-side policy changes while a device is offline.

**A1 decision status:** no offline workflow, data class, retention period, or synchronization protocol is approved.

## 6. Data and persistence options

| Option | Strengths | Constraints / questions |
|---|---|---|
| Relational database | Strong transactional model, constraints, structured reporting, mature backup practices | Schema must not encode unverified hierarchy; operations, capacity, backup and restore need validation |
| Document-oriented database | Flexible records and some evolving document shapes | Cross-record integrity, reporting, transaction needs, and consistency must be tested against real workflows |
| Hybrid persistence | Can fit specialized workloads with different storage needs | More operational complexity, duplication, consistency and backup concerns |

A relational database remains a candidate, not a frozen decision. A1 must first establish record authority, domain ownership, retention, reporting, and transaction requirements.

**Data architecture principles for assessment**
- Separate human/person records from login credentials and sessions.
- Preserve authoritative source, provenance, version, and correction history.
- Avoid duplicating the same authoritative fact across modules without clear ownership.
- Model effective dates and historical changes only where verified workflows require them.
- Define data export, backup, restore, archival, and deletion behavior.
- Do not create hierarchy tables, enums, foreign keys, or permission scopes before constitutional reconciliation.
- Do not migrate legacy records until provenance, lawful authority, quality, and minimization are established.

## 7. Security and trust boundaries

The following are architecture requirements to evaluate, not an approved security design.

1. Clients are untrusted. The server independently authenticates and authorizes every protected operation.
2. Organization scope and role claims from the client are never authoritative.
3. Authorization covers direct reads, search, reports, exports, attachments, background jobs, notifications, and synchronization.
4. Identity, authentication, assignments, and institutional authority remain conceptually distinct.
5. Privileged actions require attributable identities, least privilege, and appropriate approval separation.
6. Secrets are not stored in source code, ordinary logs, or client bundles.
7. Administrative and security events require protected, reviewable audit records.
8. File upload and download require classification-aware access and malware/content controls.
9. Integrations use explicit trust boundaries, scoped credentials, and revocation.
10. Threat modeling must include shared devices, lost devices, compromised accounts, insider misuse, network interception, replay, and data leakage through exports.

Authentication technology, session model, identity proofing, account recovery, and privileged-access approach remain undecided.

## 8. Hosting and operational models

| Model | Potential advantages | Main constraints | Required evidence |
|---|---|---|---|
| Locally managed infrastructure | Direct operational control and potential local hosting | Requires capable staff, physical/network resilience, power, backups, security and maintenance | Site capability, staffing, connectivity, recovery plan, full cost |
| Managed hosting / cloud platform | Managed infrastructure capabilities and elastic resources | Data location, contracts, connectivity, recurring cost, vendor dependence, account and payment availability | Provider terms, jurisdiction, price model, support, service limits, export and exit plan |
| Hybrid | Can place selected workloads or data components in different environments | More complex identity, networking, synchronization, monitoring, backup and responsibility boundaries | Clear data classification, threat model, ownership and tested recovery |
| Institution-operated shared hosting | Potential control over institutional service environment | Capacity, security, redundancy, staffing, procurement and lifecycle support | Confirmed institutional capability, policy, service ownership and operating budget |

No hosting provider or deployment topology is recommended as selected. No assumption is made that paid cloud services, billing methods, local facilities, or operational support are available.

### Minimum operational questions

- Who owns the service and is accountable for incidents?
- Who can administer infrastructure and review privileged activity?
- Where are primary data, backups, logs, and attachments stored?
- What are the recurring and one-time costs, including connectivity, support, domains, certificates, storage, messaging, and backups?
- What happens if payment, provider access, connectivity, or a key administrator becomes unavailable?
- How are backups encrypted, tested, retained, and restored?
- What recovery time and recovery point objectives are required and affordable?
- How are upgrades, security patches, monitoring, vulnerability reports, and incident response handled?
- Can data and attachments be exported in documented formats if the provider relationship ends?
- What minimum staffing and training are required for sustainable operation?

## 9. API, integration, and interoperability options

A documented API boundary is a candidate regardless of internal application shape.

A1 should discover:
- Existing authoritative systems, spreadsheets, paper registers, and external service dependencies.
- Which system is authoritative for each data category.
- Whether integration is legally and operationally permitted.
- Data-sharing purpose, minimum fields, recipient, security, error handling, and revocation.
- Whether integration is synchronous, asynchronous, or manual.
- Duplicate handling, retries, idempotency, reconciliation, and audit.
- Provider exit and data portability.

Do not create API contracts, external integrations, or migration pipelines during A1. Do not assume social media or public website content is a trusted source of institutional records.

## 10. Preliminary option comparison

Qualitative assessment only; no numeric scores are assigned because workload, team capacity, hosting, and field evidence are missing.

| Criterion | Modular monolith | Distributed services | Serverless functions |
|---|---|---|---|
| Initial operational complexity | Lower | High | Medium; provider-dependent |
| Internal domain separation | Strong if enforced | Strong if boundaries are well designed | Depends on function/domain discipline |
| Cross-domain transactions | Simpler within one application boundary | More complex | Depends on backing services and orchestration |
| Independent scaling | Limited by deployable unit | Strong | Potentially strong for suitable workloads |
| Offline workflow complexity | Manageable with explicit sync service | Higher across service boundaries | Still requires explicit sync architecture |
| Team/operations demands | Moderate | High | Provider/platform expertise required |
| Vendor portability | Depends on framework and dependencies | Depends on service infrastructure | Often lower with proprietary managed services |
| Fit with currently unknown scale/team | Plausible candidate | Not yet evidenced | Not yet evidenced |

The comparison is not a decision. Actual selection requires representative workflow and workload evidence, operational capability, cost, and security review.

## 11. Architecture decision register

| ADR ID | Decision topic | Candidate direction | Current status | Evidence required before decision |
|---|---|---|---|---|
| ADR-A1-001 | Overall application shape | Modular monolith vs distributed vs serverless | OPEN — PROPOSED | Domain/workflow map, workload, team and operations evidence |
| ADR-A1-002 | Client strategy | PWA-first evaluation with API boundary vs dedicated mobile clients | OPEN — PROPOSED | Device inventory, user journeys, offline capability tests |
| ADR-A1-003 | Offline synchronization | Read-only cache, queued commands, connectivity-required actions | OPEN — PROPOSED | Workflow risk and data-classification decisions |
| ADR-A1-004 | Persistence | Relational vs document vs hybrid | OPEN — PROPOSED | Record integrity, transaction, reporting and operational requirements |
| ADR-A1-005 | Identity and authorization | Server-side policy enforcement | DESIGN PRINCIPLE — DETAILS OPEN | Verified authority, mandates, role and assignment workflows |
| ADR-A1-006 | Hosting | Local, managed, hybrid, institution-operated | OPEN — UNASSESSED | Legal, data-location, cost, support, connectivity and recovery evidence |
| ADR-A1-007 | File and object storage | Managed or institution-operated storage | OPEN — UNASSESSED | File classification, volume, retention, backup, access and cost |
| ADR-A1-008 | Search and analytics | Governed indexing and aggregate reporting | OPEN — UNASSESSED | Privacy, access, language search, data ownership and reporting needs |
| ADR-A1-009 | Notifications | In-app, email, SMS, push or combinations | OPEN — UNASSESSED | Consent, reach, cost, provider availability, privacy and language needs |
| ADR-A1-010 | Integration strategy | Explicit API and controlled adapters | PRINCIPLE PROPOSED | System inventory, source ownership, legal basis, provider contracts |
| ADR-A1-011 | Observability and recovery | Centralized monitoring, audit, backup and restore | OPEN — UNASSESSED | Operations ownership, incident requirements, recovery objectives and cost |

An ADR becomes accepted only after alternatives, evidence, consequences, security/privacy impact, reversibility, owner, and explicit approval are recorded. No ADR is accepted by this assessment.

## 12. Requirements and risk traceability

Relevant requirements:
- FR-008 and FR-009 — localization and Ethiopian calendar.
- FR-010 and FR-011 — offline workflows and client channels.
- FR-012 — auditability.
- NFR-001 through NFR-008 — security, privacy, reliability, performance, accessibility, localization, interoperability, maintainability.

Relevant risks:
- R-004 — incorrect organizational scope or authority.
- R-007 and R-008 — offline cache and synchronization conflicts.
- R-009 — client-controlled authorization.
- R-010 — localization and calendar inconsistency.
- R-011 — unknown connectivity and device conditions.
- R-012 — hosting, backup, disaster recovery, and cost.
- R-014 — legacy data and integration quality.

These references indicate relevance only. This assessment does not validate or close requirements or risks.

## 13. Evidence gaps and next research actions

| ID | Missing evidence | Why it matters | Safe A1 action without unavailable documents |
|---|---|---|---|
| ARCH-G01 | Seventh-edition Constitution, bylaws, approved amendments and mandates | Blocks authority-dependent domains, scope and authorization | Keep hierarchy-dependent decisions open; prepare source-to-domain questions |
| ARCH-G02 | Existing UI repository, branch and commit | Prevents duplicate or destructive redesign | Continue read-only repository/branch/history discovery; preserve all existing UI |
| ARCH-G03 | Authorized workflow and process-owner evidence | Establishes actual domain boundaries and transaction needs | Use the stakeholder workbook as a blank instrument; mark all unconfirmed workflows |
| ARCH-G04 | Device, browser and connectivity profile | Determines feasible offline and client strategy | Prepare device test plan; do not claim compatibility |
| ARCH-G05 | Hosting, support, budget and payment constraints | Determines sustainable operating model | Prepare total-cost template and provider-neutral criteria |
| ARCH-G06 | Legal, privacy, safeguarding and records policies | Determines data location, retention, processing and controls | Maintain privacy controls as provisional; no real data |
| ARCH-G07 | Workload, user count, transaction and reporting profile | Determines scaling and performance requirements | Define measurement plan; do not invent targets |
| ARCH-G08 | Existing systems and integration inventory | Prevents unsafe duplication and migration | Prepare inventory template; do not connect or import |

## 14. A1 exit criteria for architecture assessment

Before architecture can be frozen:
- Governing sources and current mandates are authenticated and reconciled.
- Candidate workflows and domain ownership are validated by authorized stakeholders.
- Existing UI source and current design are located and reconciled without destructive replacement.
- Field devices, connectivity, and offline workflows are evidenced.
- Privacy, safeguarding, legal, records, and security requirements are reviewed.
- Hosting, operational ownership, support, cost, backup, and recovery are feasible and documented.
- Options are evaluated against agreed measurable requirements.
- Each selected decision has alternatives, evidence, consequences, owner, and explicit approval.
- Architecture choices are traceable to validated requirements and accepted risks.
- The Owner explicitly approves the A1 baseline.

## 15. Explicit exclusions

This assessment does not authorize:
- Production code, schemas, migrations, API contracts, infrastructure provisioning, or vendor purchase.
- Selection of a programming language, framework, database, cloud, hosting provider, or mobile stack.
- Organizational hierarchy, office, role, permission, or navigation design based on unverified authority.
- Real-data import, migration, processing, or external disclosure.
- AI services, autonomous decisions, payments, or production integrations.
- Merge, deployment, signing, publication, or operational launch.
- A2 reconciliation, A3 implementation, or closure of A1.

**Assessment outcome:** PARTIAL — options and evidence dependencies documented; no architecture decision frozen; authoritative, stakeholder, field, legal, and operating evidence remain outstanding.
