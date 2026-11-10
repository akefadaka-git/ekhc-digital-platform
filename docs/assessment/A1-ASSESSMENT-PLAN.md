# A1 Assessment Plan

**Status:** Draft — assessment in progress  
**Baseline:** Repository initialization on `main`; A1 documentation work on `docs/a1-assessment-foundation`

## Assessment workstreams

| ID | Workstream | Required evidence | Current status |
|---|---|---|---|
| A1-01 | Governance and mandate | Official mandate, governance decisions, approval authority | PARTIAL |
| A1-02 | Organizational model | Current 7th-edition Constitution, applicable bylaws, authoritative hierarchy and office definitions | PARTIAL — Owner-provided discovery chain recovered; constitutional reconciliation pending |
| A1-03 | Stakeholders and workflows | National, ቀጣና, ኅብረት, local, ministry, office and member workflows | PARTIAL — public ministry/service areas inventoried; stakeholder validation not yet available |
| A1-04 | Functional requirements | Validated use cases, actors, priorities and acceptance criteria | DRAFT — candidate capability areas only |
| A1-05 | Non-functional requirements | Availability, performance, accessibility, localization, resilience | DRAFT |
| A1-06 | Existing systems and UI | Inventory of prior EKHC UI, source repository/branch, data, integrations and ownership | PARTIAL — historical UI design/implementation references recovered; exact files not found on current main; reconciliation open |
| A1-07 | Architecture | Domain boundaries, deployment model, data architecture and integration contracts | PROPOSED |
| A1-08 | Security and privacy | Threat model, data classification, authorization, audit and retention | DRAFT |
| A1-09 | Offline operations | Offline use cases, conflict rules, sync security and recovery | DRAFT |
| A1-10 | Delivery and sustainability | Hosting, operating model, support, cost and connectivity assumptions | NOT ASSESSED |

## Known constraints to carry into assessment

- EKHC-only product identity: `የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን`.
- `ቀጣና` is a distinct organizational level above `ኅብረት`.
- Retain `ኅብረት` as the established EKHC term; do not substitute an unapproved English organizational label.
- The Owner-provided hierarchy chain is recorded in `docs/organization/HIERARCHY-AND-TERMINOLOGY.md`; it is a discovery baseline only and is not constitutionally verified.
- Two prohibited legacy organizational labels are excluded from all project artifacts and product surfaces.
- Do not infer office parentage, governance powers, or data scope from seal wording or display composition alone.
- Preserve existing EKHC UI/work until it has been inventoried and assessed. The historical UI references are recorded in `docs/assessment/UI-RECONCILIATION-REGISTER.md`; exact current remote files remain unverified.
- The EKHC 7th-edition Constitution is the required governing source. Older editions are historical references only where superseded.

## A1 evidence register

| Evidence ID | Evidence item | Source / owner | Status |
|---|---|---|---|
| EV-001 | Owner-confirmed product identity and terminology constraints | Prior Owner decisions, October–November 2026 | RECOVERED |
| EV-002 | EKHC 7th-edition Constitution (Amharic authoritative edition) | Official EKHC source; complete copy and authenticity to verify | REQUIRED — NOT PROVIDED YET |
| EV-003 | Current applicable bylaws / መተዳደሪያ ደንብ | Official EKHC source; edition and amendments to verify | REQUIRED |
| EV-004 | Existing EKHC UI and related project artifacts | Historical project references plus current repository inspection | PARTIAL — exact files/branch not located on current main |
| EV-005 | Stakeholder workflow and role evidence | EKHC offices and authorized stakeholders | REQUIRED — not yet validated |
| EV-006 | Public institutional/service-area evidence | Official EKHC public websites | CORROBORATIVE ONLY |

## A1 work completed with currently available evidence

1. Repository-level governance, independence and stage gates documented.
2. Owner-provided organizational chain preserved as an unverified discovery baseline.
3. Public EKHC ministry/service-area labels inventoried as context, not constitutional structure.
4. Existing UI references recovered from prior project history and recorded without assuming the files are present in the current default branch.
5. Candidate workflows and evidence questions documented for later stakeholder validation.
6. Candidate architecture and security concerns documented without freezing technology or data models.
7. Initial risk and dependency register created; ratings remain preliminary and unaccepted.

## Exit gate

A1 remains OPEN until authoritative sources are reconciled, existing UI and systems are located and assessed, stakeholder workflows are validated, requirements and architecture are reviewed, and the Owner records explicit approval. Missing evidence must remain visible; it must not be silently converted into assumptions or closure.
