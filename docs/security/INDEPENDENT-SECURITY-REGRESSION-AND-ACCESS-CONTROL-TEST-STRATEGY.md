# EKHC OS — Independent Security Regression and Access-Control Test Strategy

**Status:** A3 strategy and current-boundary regression guard implemented; future authorization tests specified but intentionally not executable until an approved authorization feature exists  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/security-access-control-regression-strategy`  
**Base:** `98cdfbd861047dcc0b8742c153d52abab751b8e3` — A3 authentication/authorization security assessment

## 1. Objective and hard safety boundary

Establish a repeatable, independently reviewable security regression strategy that protects the current authority-independent foundation and defines how future access-control behavior must be tested.

This increment does **not** create authentication, authorize a principal, protect or expose business data, or introduce institutional roles, offices, hierarchy, memberships, scopes, entitlements, or permissions.

The present application has no authentication feature and no protected business resources. Consequently, it is unsafe and misleading to claim that access-control behavior is already tested. The executable tests added here protect the current *absence* of an access-control surface. The future test matrix is a specification, not a claim that a policy engine exists.

**Invariant:** no business data, personal data, membership records, pastoral records, governance records, or protected resource endpoints are created, loaded, queried, or exposed by this test suite.

## 2. Test architecture and independence

Use four distinct layers when features are separately authorized:

1. **Current-boundary regression tests (executable now):** inspect the Django settings and URL configuration to ensure the minimal no-auth foundation has not silently grown an application, database, login route, or protected route.
2. **Pure policy unit tests (future):** exercise a separately approved authorization decision function using synthetic principal/resource/action descriptors and explicit policy fixtures. No Django request, database, or live identity provider is needed for the core policy truth table.
3. **Request-boundary integration tests (future):** exercise middleware, views, and service boundaries with synthetic requests and a fake policy adapter. Verify every protected operation is denied unless a deliberately constructed, approved test policy returns an allow decision.
4. **Independent adversarial verification (future A4):** a reviewer who did not implement the policy inspects the threat model and tests, then runs negative tests for bypass, stale entitlement, scope confusion, object references, and data leakage.

The test suite must not depend on a production identity provider, production credentials, live email/SMS, external member data, production database, or paid service. CI must use synthetic fixtures and read-only repository permissions.

## 3. Executable regression scope in this increment

The new current-boundary test verifies:

- The Django installed-app registry remains empty.
- The URL configuration remains limited to the single non-sensitive health route.
- No login, logout, token, account, member, organization, or other application route has been introduced.
- No database configuration has been enabled.

This is a regression guard for the current foundation, not an authentication test and not evidence that a future authorization policy is correct. When a later Owner-approved increment adds an application component, the guard must be revised only with an explicit scope decision and an equivalent test proving that no protected route or data access is accidentally exposed.

Existing health, runtime, security-header, localization, and observability tests remain in force. This increment must not weaken or replace them.

## 4. Future access-control test model — synthetic only

Use neutral technical fixtures, not institutional titles or roles:

- **anonymous request:** no authenticated principal.
- **synthetic principal A / B:** opaque test identities with no real-person mapping.
- **unentitled principal:** authenticated synthetic principal with no grant in the test policy.
- **synthetic resource A / B:** inert in-memory resource descriptors, not database rows or real records.
- **synthetic action:** a fixed test operation such as `read`, `update`, or `export`.
- **policy evidence:** a test-only, explicit allow/deny fixture with version and effective-time metadata; it must not model an EKHC appointment, office, authority, or hierarchy.

Do not create a production role catalogue. A test fixture must not use institutional labels or imply that a synthetic grant corresponds to real-world authority.

## 5. Required future security regression matrix

| ID | Scenario | Expected result | Test layer |
|---|---|---|---|
| AC-01 | Anonymous request to a future protected endpoint | Deny; no resource data returned | Request integration |
| AC-02 | Authenticated synthetic principal with no grant | Deny | Policy + integration |
| AC-03 | Missing policy evidence | Deny by default | Pure policy |
| AC-04 | Malformed, conflicting, or unverifiable policy evidence | Deny; safe error; no partial disclosure | Pure policy + integration |
| AC-05 | Client submits a claimed permission, scope, office, or organization value | Ignore client claim; server-side decision remains authoritative | Integration |
| AC-06 | Principal A substitutes resource B's identifier | Deny unless independently authorized for B | Object-level integration |
| AC-07 | Bulk list/export attempts to cross the permitted resource set | Return only independently authorized objects; default deny on unresolved scope | Integration |
| AC-08 | Expired or revoked synthetic grant | Deny immediately after policy freshness/revocation contract | Policy + integration |
| AC-09 | Stale session or revoked authentication credential | Reject or require re-authentication; no protected response | Authentication integration (future) |
| AC-10 | Privilege escalation by modifying request payload, headers, cookies, or client state | No change to server-side decision | Integration |
| AC-11 | Field-level sensitive attribute requested without explicit policy | Omit/deny according to approved field policy; never serialize by default | Serializer/service |
| AC-12 | Error, debug response, or audit log on denial | No credential, token, cookie, session ID, raw payload, or unnecessary personal data | Integration + log inspection |
| AC-13 | Concurrent revocation and protected operation | Behavior matches an explicitly approved consistency contract; no stale grant beyond bound | Concurrency integration |
| AC-14 | Policy adapter unavailable or times out | Fail closed; no fallback allow | Integration |
| AC-15 | Cache key omits principal/resource/policy version or reuses stale decision | Test detects cross-principal or stale-decision reuse | Policy/cache integration |
| AC-16 | Unicode/Amharic identifiers and normalization edge cases | No identity collision or authorization bypass; canonicalization rules explicit | Unit + integration |

No AC-01–AC-16 execution claim is made in this increment. They become executable only when an approved feature and policy contract exist.

## 6. Authentication regression matrix — future feature gate

When authentication is separately authorized, add independent tests for:

- login and recovery account-enumeration resistance;
- credential verification and modern password-hash configuration, if passwords are selected;
- rate limiting and abuse throttling;
- MFA enrollment, challenge, recovery, and removal controls;
- session rotation on authentication and security-sensitive changes;
- secure, HttpOnly, SameSite cookie flags and CSRF enforcement for cookie sessions;
- idle/absolute expiry and server-side session revocation;
- token issuer, audience, expiry, signature/key rotation, replay and revocation, if a token architecture is selected;
- recovery workflow strength and notification integrity;
- secrets, passwords, tokens, cookies and session identifiers absent from logs and error output.

Do not test against real identities or contact channels. Use synthetic credentials and in-memory/fake adapters.

## 7. Test data and environment controls

- Synthetic-only data; opaque identifiers such as `principal-a` and `resource-a`.
- No production dump, anonymized production dump, real names, phone numbers, email addresses, pastoral notes, child data, or governance records.
- No production credentials, signing keys, identity-provider secrets, or real session cookies.
- No external identity, SMS, email, analytics, storage, or production network integration.
- No database is introduced by this increment.
- Test policy fixtures are deterministic, local, explicit, and isolated per test.
- Tests must not make outbound network calls.
- Use fresh test clients and reset state between tests.
- CI artifacts and logs must not contain secrets or personal data.
- Time-dependent tests must freeze/inject a test clock; do not rely on wall-clock sleeps.

## 8. CI and independent verification protocol

For every implementation commit:

1. Confirm the exact branch head SHA.
2. Run the required-file gate.
3. Install dependencies from the committed hash lock.
4. Run Django system checks.
5. Run the full Django test suite, including current-boundary regression tests.
6. Run Ruff lint and format checks.
7. Run pip-audit.
8. Inspect every failed, cancelled, skipped, or missing job; a green summary cannot conceal an unexamined job.
9. Confirm the workflow's tested head SHA equals the proposed commit SHA.
10. Review changed-file inventory and confirm no protected data, roles, auth routes, migrations, or unrelated changes were introduced.

A4 independent verification must repeat the exact-head checks and review negative tests separately from the implementation author. A passing CI run is evidence of automated checks only, not a penetration test or security certification.

## 9. Failure semantics and release gates

- Any unexpected route, app, database configuration, or protected-data path in the current foundation is a regression failure.
- Missing, malformed, stale, conflicting, or unavailable authorization evidence must never produce an allow decision.
- A skipped or unexecuted test is NOT RUN, not PASS.
- A test with no implemented feature is SPECIFIED / NOT APPLICABLE, not PASS.
- A CI run on a different SHA is not exact-head evidence.
- Security test results do not establish institutional authority or legal compliance.
- A4 must not close access-control security until the approved policy contract, complete negative matrix, independent review, and exact-head evidence exist.
- A5 deployment remains a separate gate and requires separate authorization.

## 10. Current disposition

- Strategy document: established in this A3 increment.
- Current-boundary regression guard: implemented.
- Future policy and access-control matrix: specified, NOT RUN because no such feature exists.
- Authentication tests: specified as a future feature gate, NOT RUN.
- Institutional roles/authority: not created or inferred.
- Protected data/resources: none introduced or accessed.
- Database/schema/migrations: none introduced.
- Production identity or external integrations: none.
- Merge, deployment, signing, publication: not authorized or performed.

**Conclusion:** the repository now has an executable guard against accidental introduction of an authentication/data-access surface, plus a future independent access-control regression matrix. It does not claim to provide authorization before an authorization feature exists.
