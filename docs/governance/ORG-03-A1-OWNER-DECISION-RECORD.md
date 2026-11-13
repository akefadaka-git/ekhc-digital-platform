# ORG-03 A1 Owner Decision Record

**Document ID:** EKHC-ORG03-A1-DEC-001  
**Status:** OWNER DECISION RECORDED — INSTITUTIONAL CONCURRENCE PENDING  
**Decision authority:** Owner and applicable institutional authorities  
**Review PR:** #24  
**Review branch:** `a1/org03-production-architecture-review`  
**Synthetic A3 baseline:** `225daf65eaa27182ec20749adf469436fec1f654`

## 1. Owner decision recorded

**Owner selection:** `owner_and_institution`.

The Owner has explicitly selected a joint approval model: the Owner's approval together with approval/concurrence from the relevant EKHC institutional authorities who are formally empowered for the subject matter. This governs the approval model for the ORG-03 A1 architecture package and its ADRs.

**Additional Owner instruction:** None.

This is an attributable record of the Owner's selection in this conversation. It is not evidence that any EKHC governing body, office or individual has approved the architecture. The institution's governing instruments, delegation schedule, named decision-makers and subject-matter concurrence remain outstanding. The identities and legal authority of the institutional approvers must be verified from authoritative institutional records before A1 can close.

The Owner's selection does not approve individual ADR options, select vendors or platforms, accept residual risks, authorize A2, or authorize implementation, merge, live rehearsal, activation or deployment.

## 2. Proposed disposition

**Recommendation: CONDITIONAL RETURN FOR COMPLETION; production NO-GO.**

Accept the revised documents as a structured architecture proposal, but do not close A1 until the institutional decisions and evidence listed below are supplied, reviewed and approved by their actual authorities.

## 3. Package under consideration

1. `ORG-03-PRODUCTION-INTEGRATION-A1-ARCHITECTURE-REVIEW.md`
2. `ORG-03-PRODUCTION-ARCHITECTURE-ANNEX.md`
3. `ORG-03-ARCHITECTURE-DIAGRAMS.md`
4. `ORG-03-ARCHITECTURE-DECISION-REGISTER.md`
5. `ORG-03-PRODUCTION-THREAT-REGISTER.md`

All are documentation-only proposals. No provider, institutional identity service, database, hosting platform, key service or records integration is selected.

## 4. Decisions proposed for Owner consideration

| ID | Proposed decision | Current proposed disposition |
|---|---|---|
| O-01 | Accept the package as the revised A1 working draft | ACCEPT AS DRAFT ONLY |
| O-02 | Preserve synthetic A3 baseline and its regression protections | REQUIRED |
| O-03 | Require authoritative institutional evidence for all governance/security decisions | REQUIRED |
| O-04 | Require trusted-time and persistence specifications before A1 closure | REQUIRED |
| O-05 | Require identity/authority and key-custody specifications before A1 closure | REQUIRED |
| O-06 | Require operational architecture, diagrams and threat treatment before A1 closure | REQUIRED |
| O-07 | Keep production integration NO-GO pending formal A1/A2 and later implementation approvals | REQUIRED |
| O-08 | Keep live rehearsal, operational activation and A5 separately gated | REQUIRED |

## 5. Institutional evidence register

The following evidence is not established by this repository package. Each item requires an authoritative source, named owner, approver and review date.

- Institutional identity provider and subject lifecycle.
- Appointment, role, delegation and revocation authority.
- Data classification, privacy/legal basis and records custodianship.
- Restricted-record system, access matrix and break-glass policy.
- Approved hosting location, residency and administrator model.
- Database platform and operational support.
- Official time source, drift policy, calendar and SLA semantics.
- KMS/HSM custody, custodians, dual-control and recovery.
- Independent checkpoint and backup trust domain.
- Approved notification channels, providers, recipients and processing terms.
- Audit ownership, retention, legal hold and disposal.
- RPO/RTO, restore evidence and incident response.
- Responder roster, accepted primary/backup coverage and escalation authority.

Until evidenced, each remains UNRESOLVED. No institution, office, person, vendor or service is presumed to have approved the design.

## 6. Stage-gate decision

| Stage | Status | Permitted scope |
|---|---|---|
| A1 architecture assessment | IN PROGRESS | Documentation and decision preparation only |
| A1 formal approval | NOT GRANTED | Requires explicit Owner/institution decision |
| A2 reconciliation | NOT AUTHORIZED | Read-only only after A1 approval |
| A3 production implementation | NOT AUTHORIZED | Separate scope and approval required |
| A4 production verification | NOT AUTHORIZED | Requires approved implementation and test plan |
| Live rehearsal | NOT AUTHORIZED | Separate explicit Owner authorization |
| Operational activation | NOT AUTHORIZED | Separate written go/no-go |
| A5 deployment | NOT AUTHORIZED | Separate release authorization |

## 7. Immutable scope restrictions

This decision record does not authorize:
- changes to the synthetic A3 branch or baseline;
- runtime code, Django apps, ORM models, migrations or production routes;
- institutional identity integration or real user/role ingestion;
- restricted-record connection or real personal data processing;
- production keys, secrets, notification credentials or outbound messages;
- live rehearsal, operational activation, merge or deployment.

## 8. Approval and authority record

**Owner decision on final institutional approving-authority model:** RECORDED — `owner_and_institution`  
**Owner decision meaning:** Owner approval plus concurrence/approval by relevant, formally authorized EKHC institutional authorities.  
**Additional Owner instruction:** None.  
**Owner decision date/time:** Conversation record date 2026-11-14; exact decision time and independently trusted timestamp NOT ESTABLISHED.  
**Named institutional approving authority/office:** NOT VERIFIED.  
**Authority source (constitution/bylaws/resolution/delegation):** NOT PROVIDED.  
**Institutional concurrence references:** NOT PROVIDED.  
**Individual ADR approvals:** NONE RECORDED.  
**Conditions / dissent / accepted residual risks:** NOT RECORDED.

The Owner's authority-model selection is recorded, but it must not be represented as institutional approval. Repository authorship, a commit, PR approval, review comment or automated check does not substitute for institutional authority evidence or explicit stage authorization.

A repository commit, PR approval, review comment or automated check does not substitute for the Owner's explicit stage authorization unless the Owner expressly designates that mechanism and the approval is attributable and unambiguous.

## 9. Current disposition

**A1: PARTIAL — OWNER AUTHORITY-MODEL DECISION RECORDED; INSTITUTIONAL AUTHORITY AND CONCURRENCE EVIDENCE PENDING.**  
**A2: NOT AUTHORIZED.**  
**Production A3: NOT AUTHORIZED.**  
**Live rehearsal / operational activation: NOT AUTHORIZED.**  
**A5: NOT AUTHORIZED.**

The next permissible step is review of this package and provision of missing institutional evidence. No merge or implementation follows automatically from this record.
