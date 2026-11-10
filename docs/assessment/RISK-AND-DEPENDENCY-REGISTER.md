# A1 Risk and Dependency Register

**Status:** Initial assessment draft — ratings are preliminary and require Owner/stakeholder review.  
**Scope:** Risks identifiable from currently available project constraints and public institutional context. This is not a completed security assessment or production risk acceptance.

| ID | Risk / dependency | Initial impact | Likelihood | Required treatment / evidence | Status |
|---|---|---|---|---|---|
| R-001 | Required 7th-edition Constitution and current bylaws are not yet available for verification | CRITICAL | UNKNOWN | Obtain complete authoritative documents; reconcile exact clauses, amendments and authority before freezing hierarchy or permissions | OPEN — BLOCKS GOVERNANCE FREEZE |
| R-002 | Existing UI source location is unresolved | HIGH | UNKNOWN | Identify exact repository, branch and commit; inspect read-only and produce file-by-file reconciliation before any UI changes | OPEN |
| R-003 | Public EKHC pages may differ in freshness, naming or scope | HIGH | MEDIUM | Use only as corroboration; verify current names and mandates with authorized records and process owners | OPEN |
| R-004 | Organizational scope and authority could be modeled incorrectly before source reconciliation | CRITICAL | MEDIUM | Keep hierarchy, roles, assignments, permission scopes and navigation provisional; no schema or policy freeze | CONTROL IN PLACE |
| R-005 | Sensitive member, pastoral, personnel, finance and governance data could be over-collected or exposed | CRITICAL | MEDIUM | Complete data inventory, purpose/legal-basis review, minimization, access matrix, retention schedule and privacy impact assessment | OPEN |
| R-006 | Children and safeguarding-related information may require stricter handling | CRITICAL | UNKNOWN | Identify applicable safeguarding policies, guardian/consent rules, restricted access, disclosure and incident processes before defining features | OPEN |
| R-007 | Offline storage on shared or lost devices could expose cached information | HIGH | MEDIUM | Classify offline-eligible data, minimize cache, encrypt local storage, expire data, support revocation and test device-loss scenarios | OPEN |
| R-008 | Offline submissions may create duplicate, stale or conflicting records | HIGH | MEDIUM | Define per-workflow idempotency, version checks, conflict resolution, audit and connectivity-required actions | OPEN |
| R-009 | A client-controlled role or active scope could be manipulated | CRITICAL | MEDIUM | Enforce authorization server-side for every read, write, export, search, background job and synchronization operation | DESIGN REQUIREMENT |
| R-010 | Amharic, Ethiopian calendar and multilingual rendering may be inconsistent across channels | HIGH | MEDIUM | Define localization, date conversion, Unicode, search/sort/export and translation review test cases | OPEN |
| R-011 | Connectivity, device capability and support conditions across locations are not yet evidenced | HIGH | UNKNOWN | Conduct field assessment; define minimum supported devices, offline needs, service objectives, support and recovery model | OPEN |
| R-012 | Hosting, backup, disaster recovery and long-term operating costs are not established | HIGH | UNKNOWN | Compare viable operating models and cost scenarios; define ownership, support capacity, backups and recovery objectives | OPEN |
| R-013 | Financial workflows may lack sufficient segregation of duties or traceable approvals | CRITICAL | UNKNOWN | Validate actual finance controls, approval thresholds, account structures, reconciliations and audit requirements with authorized finance owners | OPEN |
| R-014 | Existing records and systems may contain duplicates, inconsistent identifiers or undocumented integrations | HIGH | UNKNOWN | Inventory source systems and data owners; assess quality and migration only after source authority and lawful basis are established | OPEN |

## Assessment rules

- Initial severity is a planning signal, not a quantified risk score or accepted residual risk.
- UNKNOWN likelihood must not be interpreted as low likelihood.
- No risk is accepted or closed by this draft.
- Mitigations that depend on constitutional authority remain provisional until source verification.
- Do not use real sensitive records in discovery without approved handling controls; prefer synthetic or properly anonymized samples.

## A1 exit evidence

Before A1 closure, each material risk must have an accountable owner, evidence-based likelihood and impact assessment, mitigation plan, residual rating, and explicit acceptance or treatment decision. Critical governance and privacy dependencies must not be waived by a schedule target.
