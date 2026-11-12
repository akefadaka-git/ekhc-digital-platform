# A3 — Identity, Authentication, and Authorization Boundary

**Status:** Contract-level implementation completed on the Owner-approved A3 branch; exact-head CI and A4 verification pending.  
**Scope:** Authority-independent and non-persistent primitives only.

## A3.2 — Authentication/session security design

- A provider-neutral `AuthenticationProvider` protocol defines the verification boundary without selecting a provider or storing credentials.
- Session observations use typed account references and trusted server-side timestamps.
- Session evaluation uses one injected, timezone-aware clock observation and fails closed for revocation, unauthenticated state, future timestamps, idle expiry, and absolute expiry.
- Session policy requires idle/absolute timeouts and rotation after authentication or security-boundary changes.
- Browser cookie policy requires Secure, HttpOnly, host-only cookies with SameSite Strict/Lax.

No authentication endpoints, credential verification, MFA, recovery, session persistence, session issuance, cookie middleware, or identity-provider integration is enabled. The current application has no active session backend. Provider, account lifecycle owner, and persistence/security design remain unresolved.

## A3.3 — Person/account separation

- Immutable `PersonReference` and `AccountReference` values are distinct types.
- `IdentityLink` requires explicit typed references; matching values never infer a relationship.
- Negative tests cover cross-type substitution, untyped values, immutability, malformed references, and absent inferred links.

No persistent schemas, person verification, membership lifecycle, roles, offices, hierarchy, permission grants, or institutional authority are implemented.

## Authorization default

The authorization evaluator remains deny-by-default until an independently approved policy is configured. This branch introduces no policy grants or institutional role model.

## Verification boundary

Exact-head CI must pass before technical verification can be claimed. No merge, deployment, signing, publication, or production-data use is included.
