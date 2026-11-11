# EKHC OS — Security Trust-Boundary and Data-Flow Architecture

**Status:** A3 documentation-only security architecture increment  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/security-trust-boundary-architecture`  
**Base:** `9c1267b83edebfdd8ddf18811d22de542edfa1a6` — Owner-accepted A4 security regression verification closure

## 1. Purpose and disposition

This document establishes a technology-neutral security architecture baseline for trust boundaries, data-flow review, threat analysis, and future control decisions while the A2 institutional authority and provenance blockers remain unresolved.

**Disposition: DOCUMENTATION ONLY — no runtime architecture or access capability is added.**

This increment does not select an identity provider, authentication protocol, authorization model, database, hosting topology, external integration, institutional hierarchy, office, role, membership, mandate, delegation, or reporting relationship. It does not authorize authentication or authorization implementation.

The architecture distinguishes:
- **Observed current state:** the deliberately minimal Django foundation described in the existing A3 assessment and A4 verification record.
- **Conditional future state:** conceptual boundaries that may apply only after the relevant product, institutional, privacy, and operational decisions are approved.
- **Unresolved decisions:** choices that must not be filled by engineering assumptions.

## 2. Security objectives and invariants

The following invariants apply to all future design work:

1. **No implicit trust:** data crossing a client, process, service, storage, identity, or operator boundary is untrusted until validated for its specific use.
2. **Authentication is not authority:** proof of account control does not prove institutional membership, office, appointment, mandate, jurisdiction, eligibility, or delegation.
3. **No client-granted access:** client state, URL parameters, headers, cookies, hidden controls, or self-asserted claims cannot independently authorize an operation.
4. **Deny on uncertainty:** absent, stale, malformed, conflicting, unverifiable, or unavailable authorization evidence must not produce an allow decision.
5. **Least privilege and explicit purpose:** any future access must be limited to an approved action, resource, scope, and purpose; broad access is not a default.
6. **No data before policy:** protected resources must not be queried, serialized, exported, cached, or disclosed before server-side authorization succeeds.
7. **Revocation must propagate:** future designs must define freshness, revocation, session invalidation, and cache invalidation semantics before persistent grants or decisions are used.
8. **Minimize sensitive data:** collect and retain only data with an approved purpose, access policy, retention period, and accountable owner.
9. **Safe failure:** security-control failures must fail closed without leaking secrets, sensitive records, or implementation details.
10. **Evidence before assertion:** architecture, authority, operational readiness, and security claims must be traceable to inspectable evidence.

## 3. Observed current system boundary

The current reviewed repository baseline is intentionally non-persistent:
- Django foundation with no registered product/authentication applications.
- One non-sensitive health route.
- No configured usable application database, user model, identity provider, token issuer, session workflow, authorization policy, protected business-resource endpoint, or institutional role catalogue.
- Existing runtime secret/host validation, conservative security headers, request correlation/log minimization, Amharic/English language negotiation, and current-boundary regression tests.
- No verified frontend/client provenance or approved deployment topology.

These are repository-state observations from the prior A3/A4 reviews, not a guarantee about an external hosting environment or systems outside this repository. The current health route is not a general-purpose API gateway or evidence of production readiness.

## 4. Trust-boundary register

| Boundary | Current state | Future design questions | Required security posture |
|---|---|---|---|
| Browser/mobile client ↔ application | No verified product client or authenticated flow | Which clients are real, supported, and source-verified? | Treat every client field and claim as untrusted; enforce controls server-side |
| Application process ↔ persistent storage | No usable application database configured | What data is necessary, where may it reside, who operates it, and how is it backed up/deleted? | No storage until data classification, access, retention, encryption, backup, and recovery are approved |
| Application ↔ identity provider | No provider or integration | First-party identity or external OIDC? Who controls issuer, keys, account lifecycle, and outages? | Validate issuer, audience, signature, expiry, nonce/state and key lifecycle if applicable; never trust decoded claims alone |
| Application ↔ session/token store | No session/token store | Session or token model, expiry, rotation, revocation, isolation and recovery? | Protect secrets in transit/at rest; no identifiers in URLs or logs; define revocation and replay controls |
| Principal ↔ authorization decision | No principal or policy engine | What approved evidence can support each action/resource decision? | Server-side, resource/action-specific, deny-by-default decisions |
| Authorization policy ↔ institutional evidence | No verified authority source integrated | Which authoritative documents, decisions, effective dates, and revocations are valid? | No software-created authority; trace every authority-bearing entitlement to verified evidence |
| Application ↔ recovery/notification channel | No integration | Which channels are available, verified, accessible, and supportable? | Recovery no weaker than enrollment; prevent account enumeration and channel substitution |
| Application ↔ audit/log pipeline | Request-scoped minimal observability exists; no external sink verified | Audit event schema, privacy basis, access, retention, integrity and review? | Separate operational logs from authority/audit records; minimize identifiers and prohibit credential capture |
| CI/build ↔ repository and artifacts | Read-only CI pattern established for current tests | Artifact provenance, dependency updates, signing and release controls? | Least-privilege workflow permissions, pinned/locked dependencies, inspectable exact-head evidence |
| Operator/deployment environment ↔ application | No production topology validated | TLS termination, proxy trust, secrets, backups, monitoring, incident response and recovery? | Explicit environment inventory; do not trust forwarded headers or assume proxy topology |

A boundary becomes applicable only when the corresponding component is approved and introduced. This register is not evidence that any future component exists.

## 5. Conditional data-flow model

The following is a conceptual review sequence, not an implemented request path:

1. A client submits a request over an approved transport.
2. The application validates request shape, size, encoding, origin/CSRF conditions where applicable, and protocol-specific protections.
3. If authentication is selected and implemented, the application validates the credential/session with the approved trust source.
4. The application resolves a server-side principal reference; client-supplied identity, role, office, organization, membership, scope, and permission claims remain untrusted.
5. If the request targets a protected resource, the application obtains current, authoritative policy evidence and evaluates the exact action/resource/scope.
6. If any required evidence is missing, stale, conflicting, revoked, malformed, or unavailable, the operation is denied before data retrieval or serialization.
7. Only after an allow decision may the application retrieve the minimum authorized data and apply field-level controls.
8. The application emits a minimized security event and a safe response; secrets and protected payloads are excluded from logs.
9. Any change to credentials, authority evidence, policy, or resource scope triggers the approved revocation/freshness contract.

No step above should be interpreted as a feature currently implemented or as approval to implement it.

## 6. Threat and control analysis

| Threat scenario | Failure mode | Architecture control to require | Verification evidence |
|---|---|---|---|
| Spoofed client identity or claims | Client fabricates identity, office, role, scope, or permission | Derive principal from validated server-side authentication; ignore client authority claims | Negative request tests; claim-tampering tests |
| Credential/session theft or replay | Stolen credential is reused | Approved MFA/session/token lifecycle, secure storage, rotation, expiry and revocation | Replay, expiry, rotation and revocation tests |
| Account recovery takeover | Weak recovery bypasses normal authentication | Recovery assurance at least equivalent to enrollment; independent verification and notification | Recovery abuse and channel-substitution tests |
| Broken object-level authorization | Valid principal reads another resource by changing an identifier | Authorize each action against each target resource before retrieval | Cross-resource ID substitution tests |
| Scope confusion / bulk disclosure | List/export crosses permitted boundary | Server-derived scope and per-object filtering; fail closed on unresolved scope | List, search, export and pagination negative tests |
| Stale authority or delayed revocation | Former entitlement continues to work | Explicit effective-time, expiry, revocation and cache invalidation contract | Concurrent revocation and stale-cache tests |
| Policy service failure | Timeout or malformed response becomes implicit allow | Fail closed; no permissive fallback | Fault injection and adapter-failure tests |
| Field-level overexposure | Serializer returns hidden/sensitive fields | Explicit field-level policy and safe serialization defaults | Field enumeration and schema-diff tests |
| Sensitive data in logs/errors | Tokens, session IDs, personal or protected payloads leak | Allowlisted structured events; redaction and output minimization | Log/error inspection and secret canary tests |
| Cross-principal cache leakage | Cached decision/data reused for another principal or policy version | Cache key includes all security-relevant dimensions; disable cache until proven | Principal/resource/policy-version cache isolation tests |
| Dependency/build compromise | Malicious or vulnerable dependency enters artifact | Locked dependencies, audit, provenance and controlled updates | Dependency audit, lock diff and build provenance |
| Operator or deployment misconfiguration | Incorrect proxy, host, secret, TLS or access settings weaken boundary | Explicit environment contract and deployment checklist | Environment-specific configuration tests and independent review |
| Unicode normalization collision | Distinct identifiers collapse or bypass checks | Define canonicalization per identifier type; preserve original display value | Amharic/Unicode normalization and collision tests |
| Excessive data collection/retention | Unnecessary sensitive data persists or spreads | Data classification, purpose limitation, retention/deletion and access review | Data inventory, retention tests and audit evidence |

## 7. Data classification and handling gates

Before any business or personal data is introduced, classify each data category using an approved institutional/privacy review. At minimum record:
- data category and purpose;
- source and provenance;
- sensitivity and affected-person considerations;
- minimum fields required;
- lawful/institutional basis and accountable decision owner;
- permitted readers and operations, based on verified authority rather than inferred labels;
- storage location, encryption and key custody;
- retention, archival, correction, export and deletion rules;
- audit requirements and incident response;
- backup, restore and disaster-recovery requirements.

Do not populate this register with assumed institutional records or sensitive examples. Synthetic test descriptors remain non-identifying and must not be derived from production records.

## 8. Security architecture decisions — explicitly deferred

| Decision | Current disposition | Evidence required before selection |
|---|---|---|
| Frontend/client architecture | UNRESOLVED | Original UI repository/branch/commit provenance and client inventory |
| Authentication protocol/provider | NOT SELECTED | Identity/account requirements, client inventory, provider trust and operational review |
| Account identifier and proofing | UNRESOLVED | Approved identity-proofing, uniqueness, correction and recovery process |
| Session/token lifecycle | NOT SELECTED | Client topology, threat model, expiry/revocation, storage and recovery contract |
| Authorization model and policy engine | NOT SELECTED | Verified constitutional/bylaw sources, approved mandates/delegations, resource/action inventory |
| Institutional role/office catalogue | PROHIBITED TO INFER | Authoritative current organogram, mandates, appointment and delegation evidence |
| Data store and classification | NOT SELECTED | Data inventory, privacy review, hosting/residency and operational ownership |
| Audit record and retention | PARTIAL | Privacy-approved schema, retention, access and integrity controls |
| Deployment/proxy topology | UNRESOLVED | Verified hosting architecture, TLS termination, operator procedures and environment evidence |
| External integrations | NOT APPROVED | Named business purpose, data-sharing basis, provider review, credentials and failure model |

## 9. A2 blockers and governance dependency

This architecture increment does not resolve or bypass the A2 blockers. In particular:
- the current seventh-edition Constitution and adoption/amendment evidence remain unverified;
- current consolidated bylaws and amendments remain unverified;
- the constitutional-source conflict in the main README remains open;
- hierarchy, entity types, parentage, jurisdiction, mandates, and reporting relationships remain unresolved;
- approved organogram, office mandates, appointments, delegation and reporting evidence remain unverified;
- UI/client provenance, process-owner validation, legal/institutional review, privacy/safeguarding review, and product requirements remain open.

Public website labels, ministry names, familiar church structures, common software patterns, or engineering convenience are not substitutes for authoritative evidence. No institutional role or access entitlement may be inferred from them.

## 10. Verification plan for a later implementation

When a separately approved component is introduced, its A3/A4 plan must include:
- updated architecture and data-flow diagrams based on verified deployed components;
- threat-model review covering spoofing, tampering, repudiation, information disclosure, denial of service and privilege escalation;
- negative tests at policy, request, object, field, bulk/export, cache, and concurrency boundaries;
- synthetic-only fixtures and isolated test services;
- secret/log leakage checks and dependency/build provenance;
- explicit failure semantics for unavailable identity, policy, storage, and audit services;
- independent reviewer who did not author the implementation;
- exact-head CI, failed/cancelled/skipped job reconciliation, changed-file inventory, and documented residual risks.

Tests that cannot run because a feature does not exist must be labelled **NOT RUN / NOT APPLICABLE**, never PASS. CI success is not a penetration test or production security certification.

## 11. Scope and acceptance checklist

- [x] Documentation-only architecture baseline.
- [x] Current and conditional future states explicitly separated.
- [x] Trust boundaries and conditional data-flow sequence recorded.
- [x] Threat scenarios paired with required controls and verification evidence.
- [x] Data-classification gates defined without introducing actual data.
- [x] Authentication, authorization, roles, provider, storage and deployment choices remain unselected.
- [x] A2 authority/provenance blockers preserved as unresolved.
- [x] No application source, settings, routes, dependencies, migrations, database, secrets, test identities, roles, or protected resources changed.
- [x] No merge, deployment, signing, publication, or production-data access performed.

**Conclusion:** this increment supplies a reviewable security architecture baseline without creating an access path or asserting institutional authority. It is a design artifact only; production readiness and implementation authorization remain NOT ESTABLISHED.
