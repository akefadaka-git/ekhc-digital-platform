# EKHC OS — A3 Authentication and Authorization Security Foundation Assessment

**Status:** A3 assessment completed — implementation intentionally blocked pending authority, product, and architecture decisions  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/authn-authz-security-assessment`  
**Base:** Owner-accepted A4 runtime-hardening closure `bfc1ed40694018b4b11fdbaa02087f5cb4e69bb0`

## 1. Executive disposition

The current repository is a deliberately non-persistent Django foundation. It has no installed Django applications, database, user model, authentication endpoints, session workflows, authorization policy, role catalogue, or organization model. The only route is a non-sensitive health check.

**Assessment result: AUTHENTICATION/AUTHORIZATION IMPLEMENTATION MUST NOT START YET.**

A secure identity and access-control foundation can be specified now, but a functioning sign-in system or authorization model would require unresolved decisions about the recovered UI/client architecture, identity proofing, account ownership, institutional authority, office/role assignment, privacy, safeguarding, and operational support.

This assessment therefore records security requirements, threat boundaries, architecture options, decision dependencies, and future verification criteria. It does not add an authentication or authorization feature and does not infer any institutional role, office, hierarchy, mandate, delegation, or reporting relationship.

## 2. Verified current technical baseline

The reviewed base is `a4/runtime-security-hardening-verification`, at `bfc1ed40694018b4b11fdbaa02087f5cb4e69bb0`.

Observed repository state:

- Django 5.2.19 and Python 3.14.10 are the approved first-increment runtime.
- `INSTALLED_APPS = []`; there is no configured Django authentication app or custom user model.
- `config/urls.py` exposes only `GET /health/`.
- No database engine, ORM persistence, migration, user table, identity provider, token issuer, session store, or password-reset flow is configured.
- Runtime secret and allowed-host validation are implemented and passed exact-head CI.
- Secure response headers and conservative TLS/proxy trust boundaries are implemented.
- Request observability deliberately excludes request paths, query strings, headers, bodies, cookies, IP addresses, user identifiers, and arbitrary log extras.
- No verified frontend source or client integration has been recovered in this assessment branch.

The repository's A2 evidence review remains closed with blockers recorded; substantive institutional authority/provenance gaps remain unresolved. A3 work does not cure those blockers.

## 3. Security objectives and trust boundaries

The future system must preserve these distinctions:

1. **Identity proofing:** evidence that a real person is who they claim to be. This is not the same as creating a username.
2. **Authentication:** establishing control of an account for a particular session or credential.
3. **Account lifecycle:** invitation, activation, credential enrollment, recovery, suspension, deactivation, and deletion/retention handling.
4. **Authorization:** deciding whether an authenticated principal may perform a specific action on a specific resource under an approved policy.
5. **Institutional authority:** evidence that an individual has a current, valid mandate or delegation. Software roles must never manufacture this authority.
6. **Auditability:** recording security-relevant outcomes without leaking credentials, session secrets, or unnecessary personal information.

Trust boundaries to model explicitly before implementation:

- Browser/mobile client ↔ application server.
- Application server ↔ identity provider, if one is selected.
- Application server ↔ session/token store, if one is selected.
- Authenticated principal ↔ server-side authorization policy.
- Server-side authorization policy ↔ authoritative assignment/mandate evidence.
- Application ↔ email/SMS/other recovery channel, if any is approved.
- Application ↔ audit/logging pipeline.

Client-supplied role, office, organization, membership status, permission, delegation, or scope claims are untrusted input. A request parameter, hidden UI control, JWT custom claim, or client-side route guard must never grant access by itself.

## 4. Authentication requirements (design baseline, not implementation approval)

### AUTH-01 — Account identity and uniqueness
Define the canonical account identifier only after the institution's identity-proofing and account lifecycle requirements are approved. Do not assume that email address or telephone number is universally available, unique, stable, or suitable as a legal identity.

### AUTH-02 — Identity proofing and enrollment
Document acceptable evidence, who may verify it, duplicate-account resolution, correction/appeal paths, and the minimum data retained. These are institutional and privacy decisions, not technical defaults.

### AUTH-03 — Credential security
If passwords are selected, use a maintained password-hashing implementation with a modern memory-hard algorithm and reviewed parameters. Never store plaintext or reversibly encrypted passwords. Do not build a custom cryptographic scheme.

### AUTH-04 — Multi-factor authentication
Evaluate MFA for all accounts and require stronger, phishing-resistant authentication for privileged or sensitive operations once the privileged actor classes are authoritatively defined. Do not invent a privileged role list in this assessment.

### AUTH-05 — Session lifecycle
If first-party browser sessions are selected, use server-managed sessions, secure/HttpOnly/SameSite cookies, CSRF protection for state-changing requests, session rotation after authentication and privilege changes, idle and absolute expiry, and server-side revocation. Never put session identifiers in URLs or logs.

### AUTH-06 — API/mobile authentication
Do not select bearer tokens, JWT, refresh-token rotation, OAuth/OIDC, or a mobile token profile until the existing UI/client provenance, supported clients, identity provider, threat model, and revocation requirements are reconciled. If tokens are later used, define audience, issuer, expiry, signing-key rotation, revocation, storage, and replay controls explicitly.

### AUTH-07 — Recovery and account support
Recovery must not be weaker than enrollment/authentication. Define independent verification, notification, throttling, recovery-code handling, support-agent controls, and appeal paths. No staff member should be able to silently assume a user's identity.

### AUTH-08 — Abuse resistance
Design rate limits and abuse monitoring for login, enrollment, verification, recovery, and MFA challenges. Avoid account-enumeration responses. Do not use IP address as the sole identity or abuse signal.

### AUTH-09 — Security notifications
Define user notifications for credential changes, new-device/session events, recovery, MFA changes, and account suspension. Do not disclose sensitive details to an unverified channel.

### AUTH-10 — Accessibility and localization
Authentication and recovery must support Unicode and Amharic-first presentation, accessible error handling, keyboard and assistive-technology use, and low-connectivity constraints. Do not translate security-critical terms without review.

## 5. Authorization requirements (no institutional policy inferred)

### AUTHZ-01 — Deny by default
No authenticated state alone grants access to business data. Every protected operation must have an explicit server-side authorization decision. Missing, malformed, stale, conflicting, or unverifiable policy evidence results in denial.

### AUTHZ-02 — Separate authentication from authorization
A valid login proves control of an account, not membership, office, appointment, eligibility, jurisdiction, or delegated authority.

### AUTHZ-03 — Server-side policy evaluation
Authorization must be enforced at the server/service boundary for every request and object operation. Client-side navigation guards are usability controls only.

### AUTHZ-04 — Resource and action specificity
Future policy decisions must identify the requested action and target resource, and must verify the resource's scope and the principal's current approved entitlement. Do not rely on broad UI-level permissions.

### AUTHZ-05 — No client-selected scope
Never accept a client-provided organization, church, office, ministry, committee, or geographic scope as proof of entitlement. Resolve permitted scope from trusted, current, server-side evidence after the institutional model is approved.

### AUTHZ-06 — Authority provenance and effective dates
Any future entitlement that represents institutional authority must trace to an authoritative source, approving body/person, decision reference, effective date, expiry/review date, revocation state, and any documented delegation chain. This assessment does not define those sources or approvers.

### AUTHZ-07 — Separation of duties
Do not permit one actor to approve their own authority-bearing appointment, privilege escalation, or sensitive transaction unless an authoritative rule explicitly allows it and a separately approved control mitigates the conflict.

### AUTHZ-08 — Revocation and stale access
Define prompt revocation, session invalidation, cache invalidation, and re-evaluation after account or entitlement changes before enabling persistent authorization caches.

### AUTHZ-09 — Object-level and field-level controls
Future APIs must test direct-object-reference attacks, cross-scope access, bulk export, attachment access, and field-level disclosure. Hiding a button or field is not authorization.

### AUTHZ-10 — Auditable decisions
Record allow/deny outcomes with a stable event correlation reference, policy version, action/resource category, and minimal actor reference only after a privacy-approved audit schema and retention policy exist. Never log credentials, raw tokens, session IDs, full request bodies, or unnecessary sensitive personal data.

## 6. Architecture options — decision deferred

| Option | Appropriate conditions | Risks / dependencies | Current disposition |
|---|---|---|---|
| Django server-side session authentication | Recovered first-party browser UI; same-site deployment; server-managed session lifecycle | CSRF, session store, cookie domain, deployment topology, account recovery and MFA still require design | CANDIDATE — NOT SELECTED |
| External OpenID Connect identity provider | Approved identity provider and multiple clients; provider supports required MFA and lifecycle | Provider trust, account linking, claims validation, outages, key rotation, licensing/data residency and exit strategy | CANDIDATE — NOT SELECTED |
| Native mobile authorization-code flow with PKCE | Verified native clients and an approved OIDC provider | Secure OS credential storage, redirect URI control, refresh rotation, device compromise and revocation | DEFERRED — client provenance unresolved |
| Self-hosted identity service | Demonstrated requirement for independent control and operational capacity | High patching, availability, backup, recovery, monitoring and security-review burden | DEFERRED — no operational capacity evidence |

Do not add Django authentication packages, an identity provider, OAuth/OIDC library, token package, database, user model, or authentication route based solely on this assessment.

## 7. Institutional and product blockers

The following blockers prohibit implementation of authority-bearing access control:

- Current seventh-edition Constitution and adoption/amendment evidence are not verified.
- Current consolidated bylaws and amendments are not verified.
- The constitutional-source conflict recorded in the main README remains unresolved.
- Institutional hierarchy, entity types, parentage, jurisdiction, mandates, and reporting lines remain unresolved.
- Approved organogram, office mandates, appointments, delegation, and reporting evidence remain unverified.
- Existing UI/client source provenance remains unresolved.
- Identity proofing, account ownership, account recovery, member/non-member access, and user support workflows have not been validated by process owners.
- Privacy, safeguarding, data minimization, retention, and qualified legal/institutional review remain open.
- Stakeholder and operational validation remains open.

The Owner's eight hierarchy labels remain discovery terms only. Preserve `ቀጣና` and `ኅብረት` as distinct. Do not create role names or map either term to an assumed English organizational level.

## 8. Threat assessment and required mitigations

| Threat | Potential impact | Required control before release |
|---|---|---|
| Account takeover through weak recovery | Unauthorized access and sensitive disclosure | Independently verified recovery, MFA, throttling, alerts, recovery audit |
| Credential stuffing / brute force | Account compromise or service exhaustion | Rate limits, abuse detection, safe responses, MFA |
| Session theft or fixation | Impersonation | Secure cookies or secure token storage, rotation, expiry, revocation, TLS |
| CSRF / cross-site request abuse | Unauthorized state changes | CSRF protections and origin policy appropriate to selected client architecture |
| Broken object-level authorization | Cross-church/cross-scope disclosure or modification | Server-side object checks and adversarial cross-scope tests |
| Client-supplied role/scope escalation | Privilege escalation | Ignore client entitlement claims; resolve only from trusted server-side policy |
| Stale or revoked appointment | Continued unauthorized access | Effective-dated assignments, revocation propagation, session/cache invalidation |
| Privilege conflict / self-approval | Fraud or governance bypass | Approved separation-of-duties policy and independent approval |
| Sensitive audit/log leakage | Privacy and credential exposure | Allowlisted event schema, redaction, retention/access controls |
| Identity-provider compromise/outage | Broad account compromise or loss of access | Provider assessment, key rotation, recovery, availability and exit plan |

Risk ratings cannot be finalized without the real user population, data classification, threat actors, deployment topology, and approved workflows.

## 9. Future implementation sequence and acceptance criteria

Implementation must be separately authorized after the blockers and decisions below are resolved.

1. **Identity and client decision:** recover/verify UI source and client inventory; decide account identifier, identity proofing, and authentication architecture.
2. **Account lifecycle specification:** approve invitation, enrollment, recovery, suspension, deactivation, and support workflows with privacy/safeguarding review.
3. **Authentication implementation:** add only the selected maintained framework/provider integration; test secure sessions or token lifecycle, MFA, CSRF, abuse limits, recovery, and revocation.
4. **Authorization policy specification:** reconcile authoritative institutional sources and model only evidenced actors, entitlements, scopes, delegations, and effective dates.
5. **Authorization implementation:** central server-side policy enforcement, deny-by-default, object/field-level checks, separation of duties, and revocation.
6. **Independent verification:** test privilege escalation, IDOR, cross-scope access, stale sessions, recovery abuse, CSRF, token replay, audit leakage, and accessibility.
7. **Operational readiness:** secrets, keys, backups, monitoring, support, incident response, retention, and recovery tests. Deployment remains A5 and separately authorized.

Minimum test acceptance before any release:
- anonymous requests cannot reach protected resources;
- authenticated but unentitled principals are denied;
- a user cannot grant themselves or another user an entitlement;
- cross-scope object identifiers cannot bypass policy;
- expired/revoked entitlements and sessions stop authorizing requests;
- state-changing browser requests are CSRF-protected when cookie sessions are used;
- recovery and login endpoints resist enumeration and automated abuse;
- logs and errors contain no passwords, tokens, cookies, session IDs, or sensitive request payloads;
- all negative tests fail closed when policy evidence is absent, malformed, conflicting, or stale.

## 10. A3 change-control disposition

This branch is a documentation-only assessment increment. It does not add code, dependencies, endpoints, models, migrations, credentials, secrets, test fixtures containing personal data, or production integrations.

No merge to `main`, deployment, signing, publication, or production-data access is authorized or performed. The existing UI and all unrelated work are preserved.

**Assessment conclusion:** Authentication and authorization are security-critical prerequisites, but implementation is currently **BLOCKED** by unresolved identity/client, institutional authority, privacy, and operational decisions. The safe next action is to obtain and reconcile the missing authoritative evidence and approve the identity/client lifecycle decisions before implementing authentication; authorization must remain deny-by-default and unconfigured until authoritative entitlement rules exist.

A4 verification of this assessment is a separate gate. A5 remains NOT STARTED.
