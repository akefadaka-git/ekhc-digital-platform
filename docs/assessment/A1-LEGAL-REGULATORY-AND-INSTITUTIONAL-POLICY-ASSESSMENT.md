# A1 Legal, Regulatory and Institutional-Policy Dependency Assessment

**Status:** Preliminary dependency register — not legal advice, not compliance certification, and not Owner-approved  
**Stage:** A1 assessment only  
**Baseline commit:** `359b46f0a3b4e2e4b99c8d40c4434546401de1f6`  
**Authority boundary:** No legal interpretation, institutional authority, policy, retention period, permission, or production data-processing basis is approved by this document.

## 1. Purpose

This assessment identifies legal, regulatory, constitutional, and institutional-policy questions that must be resolved before EKHC OS requirements, data governance, architecture, or operational procedures can be treated as approved.

It is designed to proceed without requiring the Owner to provide unavailable documents immediately. Missing instruments remain explicitly MISSING or UNVERIFIED; no law, policy, authority, or hierarchy is inferred from product conventions or public web pages.

This document is a requirements and evidence map, not a legal opinion. A qualified Ethiopian legal reviewer and authorized EKHC reviewers must verify applicability, current text, amendments, interpretation, and institutional decisions before implementation involving real data.

## 2. Governing principles

1. **Constitutional authority first:** the EKHC seventh-edition Constitution (Amharic authoritative text) is the required governing baseline for institutional mandate, structure, offices, authority and terminology.
2. **Current instruments only:** bylaws, policies, directives, and delegated mandates must be checked for current validity, adoption, amendment, and consistency with the Constitution.
3. **No invented hierarchy:** the platform must not create organizational levels, offices, reporting relationships, or delegated powers based on assumptions or historical practice.
4. **Legal applicability requires review:** a law's existence does not by itself establish how it applies to EKHC OS, a particular data flow, or a particular institutional activity.
5. **Purpose limitation and minimization:** collect only information necessary for a verified, authorized purpose.
6. **Safeguarding by design:** children, pastoral care, complaints, and vulnerable-person information require heightened review and restricted handling.
7. **Evidence before controls:** retention, disclosure, consent, access, data residency, and reporting rules must trace to applicable law or approved institutional policy.
8. **No real data during unresolved assessment:** use synthetic-only information in development and validation.
9. **Separation of approval gates:** documenting a dependency does not approve a policy, legal interpretation, production schema, implementation, or deployment.

## 3. Authority and source hierarchy

Use the following evidence order when validating requirements:

| Priority | Source class | How it may be used | Current project status |
|---|---|---|---|
| 1 | EKHC seventh-edition Constitution, authoritative Amharic edition | Governing institutional authority and source-defined terminology | MISSING — REQUIRED |
| 2 | Current EKHC bylaws and duly adopted amendments | Detailed institutional governance, where consistent with Constitution | MISSING — REQUIRED |
| 3 | Approved policies, regulations, directives, resolutions and office mandates | Operational rules within delegated authority | MISSING / NOT VERIFIED |
| 4 | Applicable Ethiopian legislation and binding regulatory instruments | Legal obligations, subject to qualified applicability review | NOT YET REVIEWED |
| 5 | Authorized stakeholder/process-owner confirmation | Current workflow evidence within documented authority | MISSING |
| 6 | Official EKHC website and publications | Corroborative context only; not a substitute for governing instruments | PARTIAL |
| 7 | Historical editions, informal copies, third-party descriptions | Historical research leads only | HISTORICAL / NON-AUTHORITATIVE |

A source is not VERIFIED until its issuer, authority, title, version, adoption/effective date, amendment history, completeness, authenticity, and relevant provisions have been recorded.

## 4. Legal and regulatory domains requiring qualified review

This section identifies subject areas for legal review. It does not assert that a particular provision applies or prescribe a legal interpretation.

### 4.1 Personal information and privacy

Questions to resolve:
- Which Ethiopian personal-information and privacy instruments apply to EKHC and the proposed platform?
- What are the lawful grounds and institutional authority for each processing purpose?
- Which notices, rights-handling processes, correction mechanisms, and complaint channels are required?
- What rules apply to sensitive information, children, pastoral care, employee/personnel records, financial records, and identity credentials?
- Are impact assessments, registration, notification, or designated responsible persons required?
- What restrictions apply to processors, subcontractors, cloud hosting, cross-border access, and international transfers?
- What breach assessment, notification, evidence preservation, and response duties apply?
- What deletion, retention, archival, and legal-hold rules are mandatory?

**Evidence status:** MISSING — legal applicability and institutionally approved privacy policy not reviewed.

### 4.2 Electronic records, signatures and transactions

Questions to resolve:
- What legal recognition and evidentiary requirements apply to electronic records, approvals, signatures, timestamps, and decision registers?
- When is a handwritten, witnessed, sealed, or otherwise formal record still required?
- What identity proofing, signature assurance, non-repudiation, and record-integrity requirements apply?
- What rules govern electronic notices and delivery evidence?
- Which record formats, metadata, and audit evidence must be retained?

**Evidence status:** MISSING — no legal review or institutional electronic-records policy supplied.

### 4.3 Cybersecurity, computer misuse and incident response

Questions to resolve:
- Which cybersecurity and computer-misuse obligations apply to the service and its operators?
- What security controls and incident reporting duties are legally required?
- What rules apply to access logs, monitoring, investigations, evidence preservation, and disclosure?
- What restrictions apply to security testing, vulnerability disclosure, and third-party access?
- Which government or sectoral reporting channels, if any, are applicable?

**Evidence status:** MISSING — legal applicability and incident-response policy not verified.

### 4.4 Child protection and safeguarding

Questions to resolve:
- Which child-protection and safeguarding laws, policies, and institutional procedures apply?
- Who may access child-related records and under what authority?
- What rules govern consent/assent, guardian involvement, referrals, disclosure, complaints, and escalation?
- Which information must never be collected in routine workflows?
- What are the mandatory reporting, referral, retention, and deletion obligations?
- How are safeguarding cases kept separate from ordinary membership, education, communication, or analytics features?

**Evidence status:** CRITICAL / MISSING — no approved safeguarding policy or legal assessment supplied.

### 4.5 Employment, volunteer and personnel records

Questions to resolve:
- Which employment, volunteer, occupational safety, and personnel-record rules apply?
- What is the authority for collecting identity, family, payroll, performance, disciplinary, and assignment information?
- What separation-of-duty, confidentiality, access, correction, retention, and disclosure rules are required?
- How are volunteers distinguished from employees and office holders for legal and operational purposes?

**Evidence status:** MISSING — no personnel policy or legal applicability review supplied.

### 4.6 Finance, donations, procurement and audit

Questions to resolve:
- Which accounting, tax, donation, financial reporting, procurement, audit, and anti-fraud obligations apply to the relevant EKHC entities and activities?
- Which entity is legally responsible for each financial record and transaction?
- What approval thresholds, dual controls, reconciliation, receipt, audit-trail, and record-retention requirements are authorized?
- What restrictions apply to donor information, giving records, beneficiary support, and financial disclosure?
- Are payment processing, digital wallets, or financial integrations in scope, and if so, what separate regulatory review is required?

**Evidence status:** MISSING — entity-specific legal and finance governance review not supplied.

### 4.7 Copyright, publications and digital content

Questions to resolve:
- Who owns or controls each publication, translation, image, recording, teaching resource, logo, and document?
- Which licence or written permission permits storage, reproduction, distribution, adaptation, streaming, export, or public display?
- What attribution, share-alike, territorial, language, term, and takedown conditions apply?
- What user-generated content, moderation, complaint, and removal policies are required?
- Which materials may be used offline or included in downloadable packages?

**Evidence status:** MISSING — no content-rights register or approved digital-publication policy supplied.

### 4.8 Communications, consent and public notices

Questions to resolve:
- Which channels may be used for announcements, SMS, email, push notifications, and group communication?
- What consent, opt-out, audience, confidentiality, and message-retention rules apply?
- Which notices are official, who may issue them, and what proof of authorization is required?
- What protections prevent accidental disclosure of recipients, pastoral matters, children, or sensitive groups?

**Evidence status:** MISSING — no approved communications and consent policy supplied.

### 4.9 Accessibility, language and records accessibility

Questions to resolve:
- Which accessibility obligations apply to public and internal digital services?
- What institutional requirements govern Amharic-first content, terminology, translation approval, and accessible alternatives?
- Which language version controls where translated legal or governance text differs?
- What record-access, correction, and format requirements apply?

**Evidence status:** PARTIAL — Amharic-first direction is Owner-stated; formal accessibility and translation policy remain unverified.

### 4.10 Hosting, data location and third-party processors

Questions to resolve:
- Are there restrictions on hosting or accessing institutional or personal information outside Ethiopia?
- Which contracts, processor terms, security commitments, and subcontractor disclosures are required?
- Who owns accounts, encryption keys, backups, and export rights?
- What audit, incident notice, deletion, data return, and termination clauses are mandatory?
- Which payment and procurement approvals are required before a service is used?

**Evidence status:** MISSING — no provider, legal review, contract, or institutional procurement policy supplied.

## 5. Institutional governance instruments required

| ID | Instrument / evidence | Why it matters | Status |
|---|---|---|---|
| GOV-01 | Seventh-edition Constitution, complete authoritative Amharic edition | Mandate, authority, hierarchy and terminology | MISSING — REQUIRED |
| GOV-02 | Current bylaws and amendments | Current governance and implementation details | MISSING — REQUIRED |
| GOV-03 | Approved organizational structure and office mandates | Validates accountable offices and reporting authority | NOT VERIFIED |
| GOV-04 | Data protection / confidentiality policy | Processing purpose, access, disclosure and rights | MISSING |
| GOV-05 | Records management and archives policy | Retention, preservation, legal holds and disposal | MISSING |
| GOV-06 | Child safeguarding policy and escalation procedure | Child-related data and case handling | MISSING — CRITICAL |
| GOV-07 | Pastoral care confidentiality policy | Highly sensitive pastoral information | MISSING |
| GOV-08 | Finance, donations, procurement and audit policies | Financial controls and record integrity | MISSING |
| GOV-09 | Personnel and volunteer policy | Employment, assignment and personnel records | MISSING |
| GOV-10 | Communications, publication and consent policy | Audience, notices, messaging and media | MISSING |
| GOV-11 | IT/security, access and incident response policies | Technical and operational controls | MISSING |
| GOV-12 | Delegation, signature and approval authority matrix | Digital approvals and valid decision evidence | MISSING |
| GOV-13 | Data sharing and third-party processor agreements | External disclosure and hosting controls | MISSING |
| GOV-14 | Accessibility, language and translation policy | Amharic-first and accessible service obligations | NOT VERIFIED |

No office or responsible person is named here because authoritative assignments have not been provided.

## 6. Legal-source verification worksheet

For each potentially applicable legal instrument, record:

| Field | Required entry |
|---|---|
| Source ID | Unique identifier |
| Official title | Exact title in authoritative language |
| Issuer | Legislature, regulator, court, or authorized institution |
| Instrument number | Exact number, if applicable |
| Publication source | Official gazette or authoritative issuer location |
| Adoption / publication / effective dates | Record separately |
| Amendment / repeal status | Verify current status as of review date |
| Relevant provisions | Article, section, clause and page |
| Authoritative language | Identify controlling text and translation status |
| Applicability question | Specific EKHC OS activity, data, entity, or role affected |
| Reviewer | Qualified reviewer and institutional authority |
| Review date | Date of review |
| Conclusion | Applies / does not apply / further advice required |
| Implementation implication | Requirement, control, evidence, and owner |
| Confidence | Verified / partial / unresolved |

Search snippets, unofficial translations, summaries, and third-party copies may identify leads but cannot alone support a final legal conclusion.

## 7. Requirement and risk traceability

| Project requirement / risk | Legal or institutional dependency | Gate |
|---|---|---|
| FR-001 organizational structure and terminology | GOV-01 to GOV-03 | No hierarchy schema or role tree freeze |
| FR-002 people, membership and login identity | Privacy, membership authority, identity and retention rules | No real-person data |
| FR-003 assignments and leadership | Constitution, office mandates, delegation and effective-date authority | No authority model freeze |
| FR-004 meetings, decisions and resolutions | Governance procedure, records and signature rules | No formal digital approval claim |
| FR-005 documents and records | Copyright, records, retention, access and legal hold | No real document ingestion |
| FR-006 communications | Consent, confidentiality, publication and notice rules | No real audience messaging |
| FR-007 education and ministry workflows | Safeguarding, content rights and ministry policy | Synthetic-only validation |
| FR-008 multilingual UX | Authoritative terminology and translation policy | No unapproved translations |
| FR-009 Ethiopian calendar | Official records and date interpretation requirements | Calendar default remains Owner-directed proposal |
| FR-010 offline and synchronization | Privacy, device security, revocation and retention | No sensitive offline cache |
| FR-011 web/mobile/PWA | Accessibility, security, platform and privacy obligations | Platform scope not frozen |
| FR-012 audit trails | Evidence, retention, access and incident requirements | No retention duration approved |
| NFR-001 security | Applicable security obligations and approved policy | Draft only |
| NFR-002 privacy | Legal basis, rights, retention, processor and disclosure rules | Draft only |
| NFR-003 reliability/recovery | Records continuity and service obligations | No RPO/RTO approved |
| NFR-005 accessibility | Applicable standards and institutional policy | WCAG target remains proposed |
| NFR-006 localization | Authoritative language and terminology policy | Owner direction only |
| R-005 / R-006 | Privacy, child protection and safeguarding | Critical dependency |
| R-009 | Authorized roles, delegated authority and server-side enforcement | No role model freeze |
| R-012 | Procurement, payment, hosting and continuity obligations | No vendor selection |
| R-014 | Lawful migration, source authority and record provenance | No migration |

## 8. Interim fail-closed controls

Until the relevant legal and institutional evidence is verified:
- Use synthetic-only data in development, testing, demonstrations, and validation.
- Do not import membership lists, child records, pastoral notes, personnel files, donor information, financial records, complaints, or confidential governance documents.
- Do not infer consent, lawful basis, authority, retention period, disclosure permission, or data ownership.
- Do not create production permissions, roles, access scopes, database fields, or API contracts from unverified policy assumptions.
- Do not enable AI summarization, profiling, automated recommendations, or external processing of real institutional information.
- Do not send real messages or notifications to institutional audiences.
- Do not choose a hosting location or third-party processor for real data.
- Do not treat public website content or historical constitutional material as a substitute for current governing authority.
- Record each unresolved dependency with an owner to be assigned only by authorized decision.

These are conservative project controls pending verification, not a statement of legal obligations.

## 9. A1 dependency status

| Area | Status | Reason |
|---|---|---|
| Constitutional authority | MISSING — BLOCKING | Seventh-edition authoritative text unavailable |
| Current bylaws | MISSING — BLOCKING | Current version and amendments unavailable |
| Organizational mandates | NOT VERIFIED | No approved structure or mandate documents |
| Personal-information law applicability | NOT REVIEWED | Qualified legal review required |
| Child safeguarding | MISSING — CRITICAL | No current policy or legal assessment |
| Pastoral confidentiality | MISSING | No approved policy |
| Finance and audit | MISSING | No entity-specific review or policy |
| Electronic records/signatures | NOT REVIEWED | Legal and institutional validity not established |
| Copyright and publication rights | MISSING | No content rights register |
| Communications consent | MISSING | No approved policy |
| Hosting and processors | MISSING | No legal review or contract evidence |
| Accessibility and language | PARTIAL | Product direction exists; formal policy absent |

## 10. Actions possible without additional documents

The project can continue safely at A1 by:
1. Maintaining this dependency register and linking each dependency to affected requirements and risks.
2. Preparing source-verification templates for a future legal reviewer.
3. Keeping all product examples and test fixtures synthetic.
4. Avoiding hard-coded retention, consent, legal-basis, and disclosure assumptions.
5. Keeping institutional hierarchy and approval flows unresolved until authoritative sources are available.
6. Separating legal review from technical implementation and deployment approval.

No additional document upload or screenshot is required to complete these preparatory tasks.

## 11. A1 exit criteria for this assessment

This workstream can be marked VERIFIED only when:
1. The authoritative seventh-edition Constitution is obtained and reviewed in full.
2. Current bylaws and amendments are verified.
3. Relevant institutional policies and delegated mandates are identified and authenticated.
4. Qualified legal review records the applicable legal instruments and provisions for each relevant processing activity.
5. Safeguarding, pastoral confidentiality, records, finance, personnel, communications, copyright, and security requirements are validated by authorized reviewers.
6. Requirements, risks, data classes, and workflow controls are updated with source citations and traceable decisions.
7. Unresolved conflicts and residual risks have documented dispositions.
8. The Owner explicitly approves the resulting A1 baseline.

## 12. Explicit exclusions

This document does not:
- Provide legal advice or certify compliance.
- Assert that any specific law or provision applies without qualified review.
- Approve EKHC policy, office mandates, hierarchy, roles, or delegated authority.
- Approve a lawful basis, consent mechanism, retention schedule, disclosure rule, or data residency.
- Authorize collection, import, processing, hosting, or disclosure of real personal or institutional data.
- Approve production schemas, APIs, permissions, integrations, AI features, or architecture.
- Start A2 reconciliation, A3 implementation, A4 verification, or A5 deployment readiness.
- Authorize merge, signing, publication, procurement, or deployment.

**Assessment outcome:** PARTIAL — legal and institutional dependency domains, source hierarchy, evidence worksheet, interim controls, and traceability documented. Authoritative constitutional and policy evidence, qualified legal review, and institutional validation remain MISSING / NOT VERIFIED.
