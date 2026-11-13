# ORG-03 A1 Institutional Evidence Reconciliation

**Document ID:** EKHC-ORG03-A1-EVID-001  
**Review date:** 2026-11-13  
**Status:** EVIDENCE REVIEW — A1 NOT CLOSED  
**PR:** #24 — `a1/org03-production-architecture-review`  
**Reviewed package HEAD:** `902e56a4cdaef03e8fd7ed38d59766a945a04921`  
**Synthetic A3 reference:** `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`

## 1. Executive finding

The revised PR #24 package is a coherent architecture proposal, but the 20 ADRs cannot be approved or resolved from the evidence presently available.

The repository package contains proposed controls and decision templates, not institutional approvals. The publicly accessible Ethiopian legal sources establish certain mandatory legal constraints for personal-data processing and electronic-signature/timestamp services. The public EKHC website provides organizational and ministry context, but it is not an approved identity directory, appointment register, IT/security policy, records schedule, hosting approval, provider agreement, or signed governance resolution.

A search of the accessible project Library did not surface authoritative EKHC internal policies, signed resolutions, appointment/delegation instruments, IT/security standards, contracts, data-processing records, or operational runbooks for these ADRs. Unrelated MASES/ARNA documents were excluded as evidence.

**Result:** 0 of 20 decisions can be marked institutionally APPROVED on the evidence reviewed. Several decisions have relevant legal constraints that must be incorporated, but those constraints do not select EKHC's implementation or substitute for an institutional decision.

## 2. Evidence standard

Evidence is sufficient only when it is:
1. issued by the legally or institutionally competent authority;
2. current and operative for the relevant entity, system and jurisdiction;
3. attributable and verifiable (signed resolution, approved policy, official register, contract, certificate, or authoritative system record);
4. specific enough to support the exact decision, including scope and effective date; and
5. approved by the authority empowered to make that decision.

Public legal sources can establish legal requirements. They cannot, by themselves, prove which EKHC identity service, hosting provider, database, time source, key custodian, notification provider, operational roster, or recovery objective EKHC has approved.

The website's published leadership and ministry descriptions are contextual evidence only. They do not establish delegated authority for any of the 20 technical decisions.

## 3. Authoritative public-source findings

### E-01 — Ethiopian Personal Data Protection Proclamation No. 1321/2024

The Federal Negarit Gazette text establishes, among other requirements:
- personal data processing principles including lawfulness, purpose limitation, minimization, accuracy, storage limitation, security and data sovereignty;
- registration obligations for data controllers and processors before processing;
- appropriate technical and organizational measures, records of processing, data protection impact assessment and data protection officer obligations as applicable;
- records of processing operations; and
- personal-data breach notification obligations, including the statutory 72-hour notification requirement for a controller after becoming aware of a breach.

Sources:
- Ministry of Justice law record: https://justice.gov.et/en/law/personal-data-protection-proclamation/
- Federal Negarit Gazette PDF, Proclamation No. 1321/2024: https://pdp.eca.et/files/pdfs/pdp-proclamation/pdp_personal_data_protection_proclamation_No_1321_2024.pdf

Relevant provisions located in the Gazette text include Articles 6–7 (principles/lawfulness), Article 33 (registration), Articles 40–42 (DPO and technical/organizational measures), Article 43 (breach notification), Article 45 (prior security check), and Article 46 (records of processing operations). Applicability, controller/processor roles, exemptions and any subsequent directives must be confirmed by qualified Ethiopian counsel and the competent data-protection authority for the actual EKHC processing.

### E-02 — Electronic Signature Proclamation No. 1072/2018, as amended by Proclamation No. 1358/2024

The federal electronic-signature framework recognizes electronic signatures and timestamp services. The original Proclamation provides a legal framework for licensed/recognized certificate and timestamp services; it is not a blanket approval of an internal application clock or a locally generated timestamp.

Sources:
- INSA-hosted Proclamation: https://www.insa.gov.et/pdf/electronic-signature-proclamation-no1072-2018
- Ministry of Justice amendment record: https://justice.gov.et/en/law/proclamation-to-provide-for-the-amendment-of-the-electronic-signature-proclamation-no-1358-2024/

### E-03 — Council of Ministers Electronic Signature Regulation No. 582/2025

The Ministry of Justice lists Regulation No. 582/2025 as in force and issued under the amended Electronic Signature Proclamation.

Source: https://justice.gov.et/en/law/regulation-no-582-2025-electronic-signature-regulation/

### E-04 — INSA Electronic Signature Implementation Directive No. 1157/2026

The Ministry of Justice hosts the INSA directive. It defines timestamp service providers and prescribes licensing requirements for timestamp services, including secure systems, operational procedures, primary/disaster-recovery data centers, information-security and personal-data-protection policies, and business-continuity/disaster-recovery plans. It also addresses registration and identity-verification service providers and audit requirements.

Sources:
- Official directive PDF: https://justice.gov.et/wp-content/uploads/2026/11/1157-Electronic-Signature-Directive-No.-1157-2026.pdf
- Ministry of Justice directive record: https://justice.gov.et/am/directives/

This is directly relevant if ORG-03 requires legally recognized electronic signature, certificate, identity-verification or timestamp services. It does not identify which provider EKHC has contracted or approve a provider for EKHC.

### E-05 — EKHC public website

The publicly accessible EKHC website describes the church's ministries and publishes general organizational information. It does not provide the operative constitution/bylaws, signed delegations, authoritative staff/appointment directory, technology policies, data-retention schedule, infrastructure inventory, service contracts, security standards, or approved operational rosters needed to decide the ADRs.

Source: https://www.ekhc.net/

## 4. Twenty-decision reconciliation

Status vocabulary:
- **LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN:** authoritative law constrains the design, but EKHC's actual choice/approval is missing.
- **UNRESOLVED — NO SUFFICIENT EVIDENCE:** no authoritative evidence supports a decision.
- No ADR is marked APPROVED.

| ADR | Decision | Evidence finding | Required institutional evidence / decision | Status |
|---|---|---|---|---|
| ADR-001 | Identity authority | E-04 regulates identity-verification service providers where such regulated services are used. EKHC's IdP, federation, subject identifiers, MFA and lifecycle are not evidenced. | IT/security-approved identity architecture; IdP owner; account lifecycle, MFA, service identity, revocation and outage policy; provider contract/certification where applicable. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-002 | Institutional subject and appointment source | Public website leadership information is not a live authoritative staff/appointment register and does not evidence appointment/delegation rules. | Operative constitution/bylaws and signed appointment/delegation/revocation instruments; authoritative directory/register owner; update and effective-date rules. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-003 | Authorization model | E-01 requires lawful, purpose-limited, secure processing and appropriate organizational/technical controls. It does not prescribe EKHC's RBAC/ABAC model. | Approved role catalogue, organization hierarchy, record/action matrix, delegation model, separation-of-duties policy, break-glass policy and data-owner approval. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-004 | Persistence platform | No EKHC-approved database, hosting or support standard found. E-01 imposes data-security, storage-limitation and sovereignty requirements for personal data. | IT architecture approval; hosting/data-location evidence; database support and licensing; data classification; processor contracts; backup and operations ownership. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-005 | Event and aggregate consistency | No institutional database architecture or transaction/isolation standard found. | Approved data model, aggregate/transaction boundaries, isolation and locking policy, concurrency/retry requirements, integrity and migration review. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-006 | Outbox and delivery processing | No approved messaging architecture, queue, provider contract, delivery semantics or retry policy found. | Communications/IT approval; provider API/contract and webhook evidence; payload classification; delivery receipt semantics; retry, rate-limit and failure escalation policy. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-007 | Trusted time | E-02/E-04 establish a regulated framework for legally recognized timestamp services and provider licensing. They do not establish EKHC's operational NTP/PTP source, clock hierarchy, drift tolerance or selected licensed timestamp provider. | IT time-service standard; approved source hierarchy and synchronization configuration; monitoring/drift limits; outage policy; if legal timestamp evidence is required, verify provider license/accreditation and service terms. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-008 | Business calendar and SLA | No EKHC-approved calendar, time zone, holiday authority or SLA interpretation found. | Signed operations policy defining response targets, business hours, official calendar/holiday source, IANA time zone, after-hours coverage and rule/version owner. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-009 | Key custody | E-02/E-04 provide relevant requirements if certificate/signature/timestamp services are used; no EKHC KMS/HSM, custodian roster, key ceremony or internal integrity-key policy found. | Security-approved cryptographic policy; KMS/HSM evidence and contract; named custodians; dual-control ceremonies; key inventory, backup, rotation, revocation, compromise and recovery procedures. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-010 | Cryptographic evidence | E-02/E-03/E-04 constrain legally recognized electronic signatures and regulated trust services. They do not decide whether internal event integrity uses MAC, signatures, or both, nor support a non-repudiation claim by default. | Security/legal decision on assurance claims; algorithms and key lifecycle; signer identity/intent binding; certificate and timestamp validation policy; verifier separation; independent security review. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-011 | Independent checkpoint | No independent checkpoint service, administrator separation, anti-rollback service, retention contract or recovery evidence found. | Security architecture approval; named independent trust-domain owner; service/storage topology; monotonicity and verification protocol; retention, backup and restore test evidence. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-012 | Restricted records | E-01 establishes data-protection requirements, controller/processor registration, processing records, security measures and DPO obligations as applicable. No EKHC records inventory, classification, custodians, controller/processor determination, access matrix or legal basis was provided. | Counsel/privacy review; controller/processor role analysis and registration evidence; data inventory/classification; records custodians and system-of-record owners; lawful basis; access and break-glass matrix; DPIA/prior consultation where required. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-013 | Notifications | E-01 constrains personal-data disclosure and processing; no approved provider, destination, recipient/contact source, contract, consent/authority or channel policy found. | Communications, privacy and procurement approval; provider agreement and subprocessors; approved channels/recipients; minimal payload and disclosure rules; webhook verification; delivery failure and wrong-recipient response. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-014 | Audit and monitoring | E-01 requires processing records and appropriate technical/organizational measures, including breach documentation/notification. It does not select EKHC's SIEM, log platform, audit owner or retention period. | Security/audit-approved event taxonomy, log custody, access/export controls, tamper protection, monitoring platform, alert ownership, processing records and retention policy. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-015 | Hosting and residency | E-01 includes data-sovereignty principles and requires accounting for foreign recipients/transfers in processing records; specific transfer conditions and current directives need counsel review. No hosting location, processor, administrator model or transfer approval found. | Data-location and subprocessor inventory; hosting contract; data sovereignty/transfer legal assessment; security and administrator model; processor agreement; regulator approval/consultation where required. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-016 | Backup and disaster recovery | E-01 requires appropriate security/resilience and timely restoration capabilities. E-04 imposes primary/DR facilities and continuity controls on regulated trust-service providers, not automatically on an ordinary ORG-03 deployment. No EKHC RPO/RTO, backup system or restore evidence found. | Approved RPO/RTO; backup architecture, encryption and independent custody; recovery owner; retention; clean restore and integrity test evidence; determine whether any selected service is subject to E-04. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-017 | Retention and disposal | E-01 requires personal data not be kept longer than necessary and establishes data-processing accountability. It does not provide an EKHC-specific schedule for all workflow, audit, church, legal or operational records. | Records/legal authority-approved retention schedule by record class; legal-hold and archival policy; deletion/redaction authority; backup expiry; evidentiary preservation and disposal records. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-018 | Environment and release controls | E-01 imposes appropriate security and organizational measures. E-04 includes security/DR obligations for regulated trust-service providers. No EKHC SDLC, environment, CI/CD, release approval, artifact provenance or change-control policy found. | IT/security-approved SDLC and change policy; environment inventory and segregation; CI/CD and secret access model; artifact/SBOM/provenance rules; migration/rollback approvals; emergency change audit. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |
| ADR-019 | Operational coverage | Public ministry descriptions do not establish ORG-03 responder appointments, accepted assignments, contact verification, leave/holiday coverage or escalation authority. | Signed operating mandate; named primary/backup roster with acceptance; verified routes; coverage calendar; escalation authority; on-call/incident responsibility and review cycle. | UNRESOLVED — NO SUFFICIENT EVIDENCE |
| ADR-020 | Incident response | E-01 includes data-breach notification and documentation requirements, including 72-hour controller notification after awareness. No EKHC incident commander, security runbook, severity matrix, internal notification path or tested response plan found. | Approved incident response and breach playbooks; named incident authority and deputies; 24/7 detection/notification path; legal/privacy escalation; evidence preservation; regulator/data-subject notification decision process; exercise evidence. | LEGAL CONSTRAINT FOUND / INSTITUTIONAL DECISION OPEN |

## 5. Critical legal corrections to the architecture package

1. **Timestamp assurance:** distinguish ordinary system time from a legally recognized timestamp service. If ORG-03 requires trusted evidentiary timestamping under the electronic-signature framework, verify that the provider is licensed/recognized and that its service evidence meets the applicable policy. Do not label NTP synchronization alone a legally trusted timestamp.
2. **Personal-data governance:** do not assume that EKHC's ORG-03 role is controller or processor. Determine the legal entity and purposes/means of processing, then document the applicable registration, lawful basis, processing records, DPO, DPIA/prior consultation and breach obligations.
3. **Data sovereignty and hosting:** do not infer a blanket domestic-only hosting rule or unrestricted foreign transfer. Obtain legal advice on the Proclamation's sovereignty and transfer provisions, actual processing locations, recipients, subprocessors and safeguards before selecting hosting.
4. **Retention:** storage limitation is a binding principle, but a single generic retention period cannot be inferred from the Proclamation. The records/legal authority must approve category-specific schedules and legal-hold exceptions.
5. **Electronic signatures:** the legal framework does not mean every workflow acknowledgement requires a qualified electronic signature. Determine the legal effect required for each action and use the appropriate assurance level.
6. **Regulated-service scope:** the detailed INSA timestamp/certificate/identity-verification provider requirements apply to entities providing those regulated services. Do not automatically impose them on ORG-03 as if it were itself a certificate authority or timestamp service provider.

## 6. Evidence gaps blocking A1 closure

The following primary-source documents are still required from EKHC or the competent authority:

- Operative EKHC constitution/bylaws and current governance/authority delegation schedule.
- Signed resolution or mandate establishing ORG-03 purpose, accountable business owner and decision authorities.
- Current institutional IT/security architecture and identity-provider/identity lifecycle standards.
- Staff/role/appointment authority source and service-account governance.
- Data inventory, classification, controller/processor determination, registration evidence and lawful-basis analysis.
- Records custody, restricted-record access, retention, legal-hold and disposal policies.
- Approved hosting, data-location, processor/subprocessor and administrator evidence.
- Database, messaging, time, audit, backup and disaster-recovery service decisions/contracts.
- Cryptographic/key-management policy, KMS/HSM evidence, key custodian appointments and independent checkpoint design.
- Business calendar, response SLA, roster acceptance, primary/backup coverage and escalation mandate.
- Incident response, privacy-breach response, monitoring, change/release and continuity runbooks.
- Written institutional approvals and evidence references for each ADR, including approver authority and effective date.

## 7. Required next evidence submission

For each ADR, the institutional evidence owner should provide:
- document title and document/control number;
- issuing institution/office and source-of-authority;
- signed/approved version and effective date;
- relevant clause/page/record identifier;
- named decision owner and approving authority;
- decision selected and options rejected;
- conditions, expiry/review date and accepted residual risk;
- immutable evidence location or verifiable official URL.

Sensitive policies, personnel records, contact lists, keys and credentials must not be placed in a public repository. Provide sanitized decision extracts or controlled evidence references instead.

## 8. A1 disposition

**Package review:** COMPLETE for the available PR contents and public-source evidence.  
**Authoritative institutional evidence collection:** INCOMPLETE.  
**ADR decisions approved:** 0 / 20.  
**ADR decisions with relevant public legal constraints identified:** 12 / 20 (ADR-003, 007, 009, 010, 012–018, 020). These are not approvals.  
**ADR decisions without sufficient supporting evidence:** 8 / 20 (ADR-001, 002, 004, 005, 006, 008, 011, 019).  
**A1 closure:** NOT PERMITTED.  
**A2:** NOT AUTHORIZED.  
**Production A3, live rehearsal, activation, merge and A5:** NOT AUTHORIZED.

This is an evidence reconciliation, not legal advice, institutional approval, or a substitute for Owner decision. No ADR is resolved by inference. A1 may be reconsidered only after the missing authoritative evidence is supplied and each competent authority's decision is recorded.
