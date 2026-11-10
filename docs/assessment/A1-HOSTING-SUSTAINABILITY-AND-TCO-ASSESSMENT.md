# A1 Hosting, Sustainability and Total-Cost Assessment

**Status:** Preliminary assessment framework — not procurement-approved, priced, or Owner-approved  
**Stage:** A1 only  
**Baseline:** A1 requirements, risk register, privacy assessment, data inventory workbook, and architecture options assessment  
**Decision boundary:** No hosting provider, payment commitment, infrastructure purchase, contract, or deployment is authorized

## 1. Purpose and constraints

This assessment defines how EKHC OS hosting and long-term operating options should be compared before a platform architecture is frozen. It provides a provider-neutral cost model, operating-capability checklist, and evidence register.

No current vendor quotation, hosting account, institutional infrastructure inventory, confirmed budget, support roster, data-location approval, or recovery target has been supplied. Therefore this document deliberately contains no fabricated prices, savings, service guarantees, or vendor rankings.

A known project constraint is that the Owner cannot fund account top-ups, deposits, or paid CI/service prerequisites at this stage. The assessment must therefore distinguish:
- **Zero-cost validation:** documentation, local/synthetic tests, public repository workflows, and free-tier evaluation where terms permit.
- **Recurring operating cost:** services that may become payable when real users, storage, messaging, traffic, backups, or support are introduced.
- **One-time setup cost:** equipment, migration, configuration, training, and procurement.
- **Deferred/conditional cost:** costs that arise only after scale, retention, integrations, or service-level requirements are approved.

A free tier is not automatically sustainable, contractually suitable, secure, or production-ready. A design that depends on a payment method or paid service unavailable to the institution is not a viable baseline until an alternative is evidenced.

This is an A1 assessment only. It does not authorize deployment, procurement, real-data processing, account creation, or paid subscriptions.

## 2. Decision principles

1. **Institutional ownership:** identify who owns the service, data, domains, accounts, encryption keys, backups, and vendor relationships.
2. **Affordability over headline price:** include staffing, connectivity, support, backups, recovery, upgrades, and exit costs.
3. **No hidden payment dependency:** record payment method, billing country, currency, tax, deposit, top-up, and renewal requirements before selecting a provider.
4. **Data protection first:** storage location, access, encryption, backup, retention, and deletion must match verified legal and institutional requirements.
5. **Operational capability:** select only an operating model that named, trained people can sustain.
6. **Resilience:** backups must be independently recoverable; a provider's availability claim is not a backup strategy.
7. **Portability:** data, attachments, logs, configuration, and documentation must be exportable in usable formats.
8. **Incremental commitment:** validate using synthetic data and free tools before any procurement decision.
9. **Transparent cost horizon:** compare one-time and recurring costs over at least three years, with assumptions and uncertainty visible.
10. **No unsupported production claims:** a prototype, free deployment, or successful CI run does not establish production readiness.

## 3. Candidate operating models

### Model A — Institution-operated infrastructure

The institution operates servers and associated infrastructure in an approved facility or data center.

**Potential advantages**
- Direct control over infrastructure and administrative access.
- Greater ability to align physical operations and data custody with institutional policy.
- Potentially predictable recurring cash costs after equipment and staffing are funded.

**Cost components**
- Server and storage equipment; warranty and replacement.
- Power, backup power, cooling, physical security, rack/space, and connectivity.
- Firewall, network equipment, certificates, monitoring, and security tooling.
- Administrator and support staff time, training, and succession coverage.
- Off-site or otherwise independent backup storage and periodic restore tests.
- Spare parts, upgrades, vulnerability remediation, and incident response.

**Principal constraints**
- Requires reliable facility, power, connectivity, physical security, technical staff, and after-hours response.
- Hardware failure, theft, fire, power disruption, or local connectivity failure may affect the whole service.
- Capital cost and staff availability may be underestimated.
- Institutional ownership does not itself prove secure configuration or recovery capability.

**Evidence required**
- Facility and power assessment.
- Named operational owner and at least one trained backup administrator.
- Network and connectivity measurements.
- Hardware inventory, warranty, replacement and lifecycle plan.
- Independent backup location and tested restore evidence.
- Three-year staffing and replacement cost.

**Current assessment:** UNVERIFIED — no institutional infrastructure or staffing evidence available.

### Model B — Managed hosting / cloud service

Infrastructure and some operational functions are provided by an external hosting provider.

**Potential advantages**
- Less physical infrastructure to operate directly.
- Managed backups, monitoring, databases, or scaling may be available depending on contract.
- Potentially faster initial setup.

**Cost components**
- Compute/runtime, database, storage, bandwidth/egress, and request volume.
- Backup retention, snapshots, recovery, monitoring, logs, and support tiers.
- Domain registration, DNS, certificates, email/SMS/push services.
- Data transfer, attachment delivery, search, and third-party integrations.
- Taxes, currency conversion, payment processing, deposits, minimum balances, and renewal.
- Migration, configuration, security review, and vendor exit.

**Principal constraints**
- Data location, subcontractors, legal terms, account ownership, and support access may be unclear.
- Billing/payment restrictions can block service creation, renewal, or recovery.
- Free tiers may have quotas, suspension rules, or unsuitable data terms.
- Provider lock-in and sudden price changes may affect sustainability.
- Managed services do not remove the institution's responsibility for identity, access, data governance, and incident handling.

**Evidence required**
- Written terms, service limits, data location and subprocessors.
- Confirmed account owner and recovery contacts.
- Actual payment route available to the institution; no assumed card or foreign-currency access.
- Price estimate for realistic workloads and backups.
- Export and termination process.
- Support response commitments and incident notification terms.

**Current assessment:** UNVERIFIED — no provider selected or quoted.

### Model C — Hybrid operation

A deliberate combination of institution-operated and managed components, with explicit trust boundaries.

**Potential advantages**
- Can place selected workloads or data components where institutional policy and operational capability support them.
- May provide a fallback or staged migration path.
- Can combine managed infrastructure with institution-controlled backup or selected services.

**Cost components**
- All applicable institution-operated and managed-hosting costs.
- Secure network connectivity, VPN/private links where needed, identity federation, monitoring, and cross-environment backup.
- Data synchronization, replication, duplicate storage, and incident coordination.
- Additional staff training and vendor/institution responsibility management.

**Principal constraints**
- More complex security, monitoring, identity, backup, and incident response.
- Split responsibility can create gaps in patching, access review, and recovery.
- Replication may move data into an unapproved location.
- Connectivity loss between environments can interrupt workflows.

**Evidence required**
- Data classification and approved location requirements.
- Clear system-of-record boundaries.
- Network threat model and access controls.
- End-to-end restore and failover test.
- Named responsibility matrix and full cost model.

**Current assessment:** UNVERIFIED — no validated requirement currently justifies hybrid complexity.

### Model D — Staged low-cost validation, then approved operating model

Use public/free development tools and synthetic data for requirements validation, prototypes, and automated checks. Select a production operating model only after costs, policy, staffing, and recovery are evidenced.

**Potential advantages**
- Avoids premature financial commitments.
- Supports A1/A2 evidence gathering without real personal data.
- Makes payment and provider constraints visible before architecture freeze.
- Keeps production procurement and deployment as separate approvals.

**Principal constraints**
- Free development environments are not production infrastructure.
- Quotas, ephemeral storage, build minutes, availability, and terms may change.
- A later migration is required if the prototype relies on provider-specific services.

**Evidence required**
- Reproducible build and test process.
- Synthetic-only data controls.
- Explicit separation of development, test, staging, and production.
- Documented transition criteria and portability test.

**Current assessment:** RECOMMENDED FOR CURRENT A1/A2 VALIDATION WORK ONLY — not a production hosting selection.

## 4. Comparative assessment

| Criterion | Institution-operated | Managed hosting | Hybrid | Staged validation |
|---|---|---|---|---|
| Upfront cash requirement | Potentially high | Often lower, provider-dependent | Medium to high | Lowest for documentation/synthetic tests |
| Recurring cash cost | Power, connectivity, staff, replacement | Usage, storage, support, backups, renewals | Both environments plus integration | Free-tier limits; future production costs remain |
| Payment dependency | Procurement and local operating costs | Provider payment route may be a blocker | Both | Can minimize during validation |
| Operational staffing | High direct responsibility | Shared, not eliminated | High coordination | Low for limited validation |
| Data-location control | Potentially direct | Contract/provider dependent | Split and complex | Synthetic data only |
| Availability responsibility | Institution | Shared under contract | Shared across parties | No production guarantee |
| Backup/recovery burden | Institution must provide and test | Contract and configuration dependent | Cross-environment | Test process only; no production backup |
| Portability | Depends on open formats and operations | Must verify export and exit | More complex | Should be designed into prototypes |
| Current evidence | Missing | Missing | Missing | Feasible for A1 work |

No numerical winner is declared. Scores require comparable quotes, operational evidence, and agreed priorities.

## 5. Total-cost-of-ownership model

Use a three-year planning horizon. Record all amounts in ETB where possible; if a quote is in another currency, record the original currency, quote date, exchange-rate source/date, taxes, and conversion assumptions separately.

### 5.1 One-time setup costs

| Cost ID | Cost item | Quantity / basis | Unit cost | One-time total | Evidence / quote |
|---|---|---|---:|---:|---|
| SET-01 | Infrastructure equipment or initial hosting setup | TBD | TBD | TBD | Vendor/institution inventory |
| SET-02 | Network, power protection, physical setup | TBD | TBD | TBD | Site assessment |
| SET-03 | Domain and initial configuration | TBD | TBD | TBD | Registrar quote |
| SET-04 | Security architecture and configuration review | TBD | TBD | TBD | Qualified reviewer estimate |
| SET-05 | Data migration and cleansing (only if later authorized) | TBD | TBD | TBD | Source inventory and effort estimate |
| SET-06 | Initial backup and recovery configuration | TBD | TBD | TBD | Tested design and quote |
| SET-07 | Staff training and documentation | TBD | TBD | TBD | Training plan |
| SET-08 | Accessibility and localization review | TBD | TBD | TBD | Review scope |
| SET-09 | Contingency | Explicit percentage and basis TBD | TBD | TBD | Owner-approved assumption |

### 5.2 Recurring monthly / annual costs

| Cost ID | Cost item | Billing basis | Monthly ETB | Annual ETB | Evidence / quote |
|---|---|---|---:|---:|---|
| REC-01 | Application compute/runtime | Instance, usage or contract | TBD | TBD | Provider quote |
| REC-02 | Database service / storage | Capacity, IOPS, usage | TBD | TBD | Provider quote |
| REC-03 | File/object storage | GB-month and operations | TBD | TBD | Provider quote |
| REC-04 | Bandwidth / data transfer | GB or plan | TBD | TBD | Provider quote |
| REC-05 | Backup and snapshot retention | Capacity and frequency | TBD | TBD | Provider quote |
| REC-06 | Monitoring, logging and alerting | Usage / retention | TBD | TBD | Provider quote |
| REC-07 | Domain, DNS and certificates | Annual renewal | TBD | TBD | Registrar/provider quote |
| REC-08 | Email, SMS and push notifications | Message / subscription | TBD | TBD | Provider quote |
| REC-09 | Connectivity and power | Site / plan | TBD | TBD | Local quote |
| REC-10 | Technical operations and support | Staff hours / contract | TBD | TBD | Approved staffing estimate |
| REC-11 | Security patching and periodic review | Hours / engagement | TBD | TBD | Review plan |
| REC-12 | Hardware maintenance and replacement reserve | Lifecycle reserve | TBD | TBD | Asset lifecycle |
| REC-13 | Taxes, currency conversion and payment fees | Actual terms | TBD | TBD | Provider/payment terms |
| REC-14 | Training and staff turnover | Annual plan | TBD | TBD | Training plan |
| REC-15 | Incident response and recovery reserve | Approved provision | TBD | TBD | Risk assessment |

### 5.3 Three-year calculation

For each option:
- One-time total = sum of SET-01 through SET-09.
- Annual recurring total = sum of annualized recurring cost items.
- Three-year TCO = one-time total + (3 × annual recurring total) + separately identified one-off renewals/migrations.
- Cost per active user-month = annual recurring total ÷ (12 × evidenced average active users).
- Cost per transaction = attributable annual operating cost ÷ evidenced annual transaction count.

Do not calculate unit costs until user counts and transaction volumes are measured or explicitly scenario-based. Do not omit staff time because it is unpaid or contributed in-kind; show cash cost and in-kind resource cost separately.

### 5.4 Required scenario assumptions

Create low, expected, and high scenarios for:
- Active users and concurrent sessions.
- Monthly requests and API workload.
- File upload volume, average file size, and retention.
- Backup frequency and retention period.
- Data transfer and geographic distribution.
- Notification volumes and delivery channel.
- Support hours and incident frequency.
- Currency conversion, tax, and price changes.
- Growth, hardware replacement, and migration.

Every assumption must have a source, owner, date, confidence rating, and sensitivity note. Do not present a scenario as a forecast without supporting evidence.

## 6. Affordability and payment-access gate

Before a managed service is shortlisted, record:
- Legal entity or institutional account holder.
- Who can create and recover the account.
- Supported billing country and institution's available payment methods.
- Whether card, bank transfer, prepaid balance, deposit, top-up, or foreign-currency payment is required.
- Currency, conversion charges, tax, invoice availability, and renewal rules.
- Whether a free tier can be used without payment details and whether it can be suspended or deleted unexpectedly.
- Whether the institution can maintain service for at least 12 months without relying on an individual's personal account.
- What happens if the payment method fails or the account owner becomes unavailable.

**Fail-closed rule:** if the institution cannot reliably create, pay for, recover, and renew a required service, that service cannot be a production dependency. Do not ask the Owner to top up or deposit funds as a workaround. Identify an institutionally supportable alternative or leave the decision unresolved.

## 7. Operational sustainability and responsibility

A sustainable service requires named responsibility, documented procedures, and backup coverage.

| Responsibility | Required capability | Current evidence |
|---|---|---|
| Service ownership | Accountable institutional owner and decision route | MISSING |
| Technical administration | Secure configuration, patching, access review | MISSING |
| Application maintenance | Supported releases, dependency updates, incident fixes | MISSING |
| Data stewardship | Source authority, correction, retention and disclosure control | MISSING |
| Security operations | Monitoring, vulnerability response, incident handling | MISSING |
| Backup/recovery | Independent backups and witnessed restore tests | MISSING |
| User support | Amharic-first support process and escalation | MISSING |
| Continuity | Alternate administrator, key/account recovery and succession | MISSING |
| Vendor management | Contract, renewal, exit, data return and deletion oversight | MISSING |

No named staff or office is inferred. Roles must be assigned only through authorized institutional decisions.

## 8. Backup, disaster recovery and continuity

Before production approval, define and test:
- Recovery Point Objective (RPO): maximum acceptable data loss, determined by workflow and institutional risk.
- Recovery Time Objective (RTO): maximum acceptable restoration time, determined by service criticality.
- Backup frequency, encryption, retention, immutability or separation, and access control.
- Independent backup location and protection against the same account, site, or credential failure.
- Database, uploaded files, application configuration, keys, and required metadata coverage.
- Restore procedure, integrity checks, and periodic test schedule.
- Emergency access, key recovery, administrator succession, and provider outage process.
- Communication and decision authority during service interruption.

No RPO, RTO, retention duration, or availability percentage is set here. A backup job showing success is not proof of recoverability; a restore test is required.

## 9. Security, privacy and legal dependencies

Hosting selection is blocked pending review of:
- Applicable Ethiopian legal and regulatory requirements for personal information, records, telecommunications, cross-border processing, and relevant institutional obligations.
- EKHC policies governing confidentiality, safeguarding, records, pastoral care, finance, and disclosure.
- Data location, provider subprocessors, administrative access, backup location, and incident notification.
- Encryption in transit and at rest, key ownership and rotation, privileged access, audit, and deletion.
- Data subject correction/access requests and lawful disclosure processes where applicable.
- Contractual exit, data export, secure deletion, and evidence of deletion.

This assessment is not a legal opinion. No claim is made that any provider or location is legally compliant.

The provisional data classes in the A1 privacy assessment are not yet approved policy. Until approved, use synthetic data only for platform development and validation. Do not place real child, pastoral, membership, personnel, financial, or sensitive governance information in test services.

## 10. Provider-neutral procurement and exit checklist

For every candidate provider or facility, collect:
- Legal provider name, jurisdiction, service description and service owner.
- Data center or processing location, subprocessors, and cross-border access.
- Service terms, SLA, support hours, maintenance notice, incident notice, and suspension rules.
- Current price sheet, usage limits, overage charges, taxes, currency and payment requirements.
- Security attestations and independently reviewable controls, without treating marketing claims as proof.
- Backup options, restore procedure, retention, and separate failure-domain details.
- Network access controls, encryption, key management, administrative access logs.
- Export format, API access, data egress charges, termination window, and secure deletion.
- Account ownership, multi-person recovery, administrator succession, and credential custody.
- Portability test and estimated migration/exit cost.

Do not select a vendor based only on a free trial, introductory discount, regional proximity, or marketing statement.

## 11. Risk and dependency traceability

| Existing risk | Hosting/sustainability relevance | Required evidence |
|---|---|---|
| R-005 / R-006 | Sensitive and child-related data exposure | Legal/policy review, classification, access and location decisions |
| R-007 / R-008 | Offline cache and synchronization | Device profile, cache rules, synchronization and revocation tests |
| R-009 | Authorization manipulation | Server-side policy enforcement and security test plan |
| R-011 | Connectivity and device limitations | Field measurements and support profile |
| R-012 | Hosting, backup, recovery and operating cost | Comparable quotes, operating model, tested restore, three-year TCO |
| R-014 | Legacy systems and migration | Source inventory, authority, data quality and lawful migration basis |

New assessment risks to track:
- HST-01: service unavailable because payment route, billing account, or renewal cannot be maintained.
- HST-02: single administrator/account owner prevents recovery or continuity.
- HST-03: free-tier limits or terms change and interrupt service.
- HST-04: backup exists but cannot be restored independently.
- HST-05: provider data location or subcontractor access is incompatible with approved policy.
- HST-06: unbudgeted support, bandwidth, storage, messaging, or egress cost causes service degradation.
- HST-07: vendor lock-in prevents timely export or affordable exit.
- HST-08: operational responsibilities are assumed but no trained owner is assigned.

These are assessment risks, not quantified or accepted risks. They should be reconciled into the risk register during a separately reviewed A1 update.

## 12. A1 evidence register and next actions

| ID | Evidence item | Status | Action |
|---|---|---|---|
| HST-E01 | Institutional infrastructure/facility inventory | MISSING | Keep institution-operated option unverified |
| HST-E02 | Hosting provider quotations and service terms | MISSING | Do not name a preferred vendor |
| HST-E03 | Confirmed institutional payment and renewal route | MISSING | Apply fail-closed payment gate |
| HST-E04 | Named technical operations and support capacity | MISSING | Do not claim operational readiness |
| HST-E05 | Workload, active users, storage and traffic estimates | MISSING | Build scenarios only after discovery |
| HST-E06 | Data-location, privacy and legal review | MISSING | No real data or hosting commitment |
| HST-E07 | Backup/restore and continuity requirements | MISSING | Do not set RPO/RTO or availability targets |
| HST-E08 | Vendor export, deletion and exit evidence | MISSING | Keep portability as mandatory evaluation criterion |
| HST-E09 | Three-year comparable cost scenarios | NOT CALCULATED | Populate only from verified quotes and assumptions |
| HST-E10 | Institution-approved operating owner and budget | MISSING | No procurement or production deployment |

Safe A1 work that can continue without missing evidence:
- Keep the cost model and provider-neutral checklist ready for later completion.
- Use synthetic-only development and free tooling where terms allow.
- Document build/test workflows without relying on paid CI or service deposits.
- Keep all production dependencies explicitly unresolved until affordability and institutional ownership are verified.

## 13. A1 exit criteria for hosting and sustainability

This assessment may be considered complete only when:
1. At least two viable operating models have comparable, dated cost evidence, or a documented reason why comparison is not possible.
2. Three-year TCO includes setup, recurring, staff/in-kind, security, backup, connectivity, renewal, and exit costs.
3. Payment and renewal routes are verified for the institution, not assumed from an individual's account.
4. Data location, provider terms, legal review, privacy and safeguarding requirements are approved.
5. Named service, technical, security, data, and support responsibilities are assigned through authorized decisions.
6. Backup, restore, continuity, RPO/RTO, and incident procedures are defined and tested at the appropriate stage.
7. Portability and vendor exit are evidenced.
8. Residual risks have owners and explicit treatment/acceptance decisions.
9. The Owner explicitly approves the selected operating model.

## 14. Explicit exclusions

This document does not authorize:
- Vendor selection, procurement, subscription, payment, account top-up, or contract signature.
- Infrastructure provisioning, domain purchase, production configuration, or deployment.
- Real-data import, processing, backup, or hosting.
- A production budget commitment or unsupported price estimate.
- RPO, RTO, uptime, retention, or support SLA approval.
- A2 reconciliation, A3 implementation, A4 verification, A5 deployment readiness, merge, signing, or publication.

**Assessment outcome:** PARTIAL — operating models, cost categories, payment constraints, and evidence requirements documented; actual costs, institutional capability, legal approval, and production operating ownership remain MISSING/UNVERIFIED.
