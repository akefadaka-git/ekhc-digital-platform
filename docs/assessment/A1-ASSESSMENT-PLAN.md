# A1 Assessment Plan

**Status:** Draft — assessment in progress  
**Baseline:** Repository initialization on `main`; A1 documentation work on `docs/a1-assessment-foundation`

## Assessment workstreams

| ID | Workstream | Required evidence | Current status |
|---|---|---|---|
| A1-01 | Governance and mandate | Official mandate, governance decisions, approval authority | PARTIAL |
| A1-02 | Organizational model | Current constitution/bylaws, authoritative hierarchy and office definitions | PARTIAL — user-provided hierarchy recovered; source reconciliation pending |
| A1-03 | Stakeholders and workflows | National, zone, local, ministry, office and member workflows | NOT ASSESSED |
| A1-04 | Functional requirements | Validated use cases, actors, priorities and acceptance criteria | DRAFT |
| A1-05 | Non-functional requirements | Availability, performance, accessibility, localization, resilience | DRAFT |
| A1-06 | Existing systems and UI | Inventory of prior EKHC UI, data, integrations and ownership | NOT ASSESSED |
| A1-07 | Architecture | Domain boundaries, deployment model, data architecture and integration contracts | PROPOSED |
| A1-08 | Security and privacy | Threat model, data classification, authorization, audit and retention | DRAFT |
| A1-09 | Offline operations | Offline use cases, conflict rules, sync security and recovery | DRAFT |
| A1-10 | Delivery and sustainability | Hosting, operating model, support, cost and connectivity assumptions | NOT ASSESSED |

## Known constraints to carry into assessment

- EKHC-only product identity: `የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን`.
- `ቀጣና` is a distinct organizational level above `ኅብረት`.
- `ኅብረት` is the established EKHC term; do not relabel it as “Union”.
- The user's prescribed hierarchy chain is recorded in `docs/organization/HIERARCHY-AND-TERMINOLOGY.md`; official source reconciliation remains required.
- Two prohibited legacy organizational labels are excluded from all project artifacts and product surfaces.
- Do not infer office parentage, governance powers, or data scope from seal wording or display composition alone.
- Preserve existing EKHC UI/work until it has been inventoried and assessed.

## A1 evidence register

| Evidence ID | Evidence item | Source / owner | Status |
|---|---|---|---|
| EV-001 | User-confirmed product identity and terminology constraints | Prior Owner decisions, October 2026 | RECOVERED |
| EV-002 | Sixth-revised EKHC Constitution (2012 E.C.) | Official constitutional source; obtain and verify exact edition | REQUIRED |
| EV-003 | Applicable bylaws / መተዳደሪያ ደንብ | Official EKHC source; edition and amendments to verify | REQUIRED |
| EV-004 | Existing EKHC UI and related project artifacts | Existing project locations / Owner-provided materials | REQUIRED |
| EV-005 | Stakeholder workflow and role evidence | EKHC offices and authorized stakeholders | REQUIRED |

## Exit gate

A1 remains OPEN until evidence gaps are resolved or formally accepted as explicit assumptions, the requirements and architecture are reviewed, and the Owner records approval. This plan is not itself A1 approval.
