# ORG-03 A1 Owner Decision Record

**Document ID:** EKHC-ORG03-A1-DEC-001  
**Status:** PROPOSED — NOT APPROVED  
**Decision authority:** Owner and applicable institutional authorities  
**Review PR:** #24  
**Review branch:** `a1/org03-production-architecture-review`  
**Synthetic A3 baseline:** `225daf65eaa27182ec20749adf469436fec1f654`

## 1. Decision requested

The Owner is asked to decide whether the revised A1 architecture package is accepted as a complete-enough specification for a later read-only A2 reconciliation. This document does not presume approval and must not be treated as an approval signature.

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

## 8. Approval record — intentionally blank

**Owner decision:** NOT RECORDED  
**Approving authority:** NOT RECORDED  
**Decision date/time and timestamp assurance:** NOT RECORDED  
**Institutional concurrence references:** NOT PROVIDED  
**Conditions / dissent / accepted residual risks:** NOT RECORDED

A repository commit, PR approval, review comment or automated check does not substitute for the Owner's explicit stage authorization unless the Owner expressly designates that mechanism and the approval is attributable and unambiguous.

## 9. Current disposition

**A1: PARTIAL — REVISED PACKAGE PREPARED, OWNER DECISION PENDING.**  
**A2: NOT AUTHORIZED.**  
**Production A3: NOT AUTHORIZED.**  
**Live rehearsal / operational activation: NOT AUTHORIZED.**  
**A5: NOT AUTHORIZED.**

The next permissible step is review of this package and provision of missing institutional evidence. No merge or implementation follows automatically from this record.
