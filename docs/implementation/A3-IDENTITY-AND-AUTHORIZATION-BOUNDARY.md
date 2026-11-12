# A3 — Identity and Authorization Boundary Increment

**Status:** Implemented on an Owner-approved A3 work branch; exact-head CI pending.  
**Scope:** Non-persistent, authority-independent primitives only.

## Implemented

- Added distinct immutable PersonReference and AccountReference value types.
- Added an explicit typed IdentityLink; it does not infer a relationship from matching identifiers.
- Added an authorization request envelope using opaque resource and optional scope references.
- Added a fail-closed authorization evaluator that denies every request while no approved policy is configured.
- Added negative tests for type confusion, malformed references, malformed requests, and default denial.

## Deliberate exclusions

This increment does not implement credentials, authentication, sessions, account recovery, person verification, membership status, roles, positions, office assignments, organizational hierarchy, permission grants, policy configuration, persistence, database models, migrations, APIs, or UI. It does not establish institutional identity or authority. The reference values are synthetic in tests and have no production data semantics.

The prior approved technical baseline defers database/schema work and requires unresolved institutional authority to remain unmodeled. This increment respects those restrictions. A real authentication provider and any authorization grants require separate security and institutional decisions.

## Verification

The Django test runner discovers the added tests. Exact-head GitHub Actions quality verification is required before this increment can be marked verified. No merge, deployment, signing, publication, or production-data use is included.
