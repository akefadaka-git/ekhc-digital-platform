# EKHC Organizational Hierarchy and Terminology Register

**Status:** Recovered Owner constraints; constitutional reconciliation required  
**Use:** A1 assessment only. Do not implement or encode this register as a production schema until approved.

## 1. Product identity

The application identity is:

**የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን**

Maale Hibret is contextual information, not the product identity.

## 2. Recovered organizational chain

The following chain was explicitly supplied by the Owner in prior project discussions and must be preserved for source reconciliation:

1. Church
2. ዋ/ጽ/ቤት
3. ቀጣና
4. ቀጣና ጽ/ቤት
5. አጥቢያ ቤተ ክርስቲያናት ኅብረት
6. ኅብረት ጽ/ቤት
7. አጥቢያ ቃለ ሕይወት ቤተ ክርስቲያን
8. አጥቢያ ጽ/ቤት

This is a recovered Owner-provided chain, not yet a verified constitutional schema. Exact names, parent-child relationships, scope, delegated authority, and any exceptions must be checked against the applicable official constitution and bylaws.

## 3. Binding terminology constraints

- `ቀጣና` is a genuine organizational level above `ኅብረት`; do not collapse the two.
- Retain `ኅብረት` as the EKHC term. Do not translate or relabel it as “Union”.
- Do not create a `ChurchUnion` or `Union` domain entity.
- Two prohibited legacy organizational labels are excluded throughout the repository and product: documentation, source code, database schemas, APIs, UI, reporting, analytics, and tests.
- Do not substitute generic labels such as “zone/union/local church” unless the mapping is explicitly supported by an authoritative EKHC source and approved.
- Office labels and seal-name composition do not, by themselves, prove organizational parentage or authority.

## 4. Required source reconciliation

Before A1 closure, record:

- Exact constitutional edition, revision date, articles, and relevant clauses.
- Official names and definitions for each organizational level and office.
- Parent-child relationships and permitted organizational exceptions.
- Governance and appointment/election authority at each level.
- Whether committees, departments, positions, and assignments are constitutional entities, administrative structures, or merely operational constructs.
- Whether the same individual may hold multiple positions and how delegated authority is represented.
- Required Amharic spelling, abbreviations, and approved multilingual display labels.

## 5. Implementation guardrail

No hierarchy table, enum, foreign key, route, permission scope, or UI navigation tree is approved by this draft. A2 must reconcile this register against authoritative documents before any schema or implementation is proposed for approval.
