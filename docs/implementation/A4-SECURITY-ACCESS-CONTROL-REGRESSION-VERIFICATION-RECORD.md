# EKHC OS — A4 Independent Verification Record
## Security regression guard and access-control test strategy

**Verification disposition:** PASS — independent A4 technical review complete; Owner acceptance pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 subject branch:** `a3/security-access-control-regression-strategy`  
**A3 exact head reviewed:** `5c6b07a80ed7fdf7a96433f1542d357cb392fade`  
**A4 record branch:** `a4/security-access-control-regression-verification`  
**A3 base:** `98cdfbd861047dcc0b8742c153d52abab751b8e3`

## 1. Verification scope

Independently reviewed the A3 security strategy, current-boundary regression test, CI workflow, exact-head commit/diff, URL configuration, health view, Django settings, and the exact-head GitHub Actions run.

The verification asks whether this increment:
- preserves the deliberate absence of authentication and protected business-data surfaces;
- introduces no institutional roles, grants, resource records, migrations, or database-backed behavior;
- uses negative tests that fail when the current minimal boundary expands unexpectedly;
- can itself create a protected-data access path; and
- accurately distinguishes executable current-boundary checks from future access-control tests that are only specified.

This is a source-and-CI review, not a penetration test, production test, or security certification.

## 2. Exact-head and change-inventory verification

The GitHub commit comparison from A3 base `98cdfbd861047dcc0b8742c153d52abab751b8e3` to reviewed head `5c6b07a80ed7fdf7a96433f1542d357cb392fade` reports:
- 4 commits ahead, 0 behind;
- exactly 3 changed files;
- no application source, URL configuration, settings, models, migrations, or data files changed.

Changed files:
1. `.github/workflows/quality.yml` — required-file gate adds the new regression test.
2. `docs/security/INDEPENDENT-SECURITY-REGRESSION-AND-ACCESS-CONTROL-TEST-STRATEGY.md` — strategy and future test matrix.
3. `tests/test_access_control_boundary.py` — four current-boundary assertions.

No application route, view, model, migration, authentication package, authorization package, policy engine, identity provider, resource store, or role catalogue was added.

## 3. Adversarial review of executable negative tests

The executable test class uses Django `SimpleTestCase` and performs configuration and URL-resolution assertions only.

| Negative guard | Adversarial assessment | Result |
|---|---|---|
| `INSTALLED_APPS == []` | Detects accidental registration of product/auth apps in the current configuration. It does not claim to detect arbitrary Python modules that are imported without app registration. | PASS |
| Default DB engine is Django dummy and DB name is empty | Confirms there is no usable configured Django database. Django ORM access through this configured backend cannot provide a working persistence path. | PASS |
| Exactly one root URL pattern, named `health`, at `health/`, callback module `health.views` | A newly added root route, changed route, or nested URL resolver fails the assertion/attribute checks rather than being silently accepted. | PASS |
| Common login/logout/token/accounts/members/organizations/API paths raise `Resolver404` | Confirms those representative paths are not resolvable. The exact root-pattern assertion is stronger for this current minimal URL tree than this finite path list alone. | PASS |

### Test-side non-interference

The new test:
- imports only Django settings, `SimpleTestCase`, and URL resolver utilities;
- does not instantiate a Django test client;
- does not create users, principals, permissions, grants, resources, fixtures, or sessions;
- does not issue ORM queries, raw SQL, migrations, transactions, or writes;
- does not call external services, identity providers, email/SMS, or network clients;
- does not read environment secrets or production data.

The CI job runs with `contents: read`, checkout uses `persist-credentials: false`, and the job has no repository write permission. Its secret key is explicitly CI-only and must not be reused in any deployed environment.

### Independent source-path inspection

At the reviewed SHA:
- `config/urls.py` registers only `health/` and imports only the health view.
- `health/views.py` returns a fixed `{"status":"ok"}` JSON body, sets no-store and nosniff headers, and is GET-only. It does not query a database or return business data.
- `config/settings.py` sets `INSTALLED_APPS = []`, leaves Django on the dummy database backend, and configures only the existing security, observability, and localization middleware.
- Runtime dependencies contain Django only; no database driver, authentication framework, authorization framework, or ORM-backed product app was introduced.

**Conclusion on the requested safety property:** the reviewed test code does not create a protected-data access path. The application source at this exact head exposes only the fixed health response; there is no configured Django database or registered application route through which protected business data could be retrieved. This conclusion is bounded to the reviewed repository state and configured Django request path; it is not a claim that arbitrary future Python code, a future external service, or a changed deployment environment is inherently unable to access data.

## 4. Strategy and future negative-test coverage review

The strategy correctly separates:
1. executable current-boundary guards;
2. future pure policy tests;
3. future request-boundary integration tests; and
4. independent adversarial A4 review for a future authorization implementation.

The 16 future AC cases are appropriately labelled specified / NOT RUN because no authorization feature or policy contract exists. They cover anonymous denial, unentitled principals, missing/malformed evidence, client-claim tampering, object-reference substitution, bulk/export scope, revocation/expiry, stale credentials, request-state privilege escalation, field-level disclosure, log/error leakage, concurrent revocation, policy-adapter failure, cache isolation, and Unicode/Amharic normalization.

No future AC case is counted as passed. Authentication cases are also correctly deferred until an authentication architecture is separately approved.

### Coverage limitations retained as explicit future work

- The current test does not statically scan the repository for arbitrary raw network clients, direct socket use, raw SQL, or import-time side effects. The reviewed current source has no such data-access route, but this test is not a general static taint-analysis control.
- The finite list of forbidden paths is not intended to be a complete route dictionary; the exact single-root-pattern assertion provides the principal current-route guard.
- No adversarial policy tests can run until there is an approved policy contract and a feature to test.
- No concurrency, cache, revocation, field-level authorization, or real request-boundary protected-resource tests have run.
- CI does not constitute network-egress isolation, production environment validation, penetration testing, or independent external security review.

These limitations do not invalidate the narrow current-boundary guard. They prevent overstating it as a complete access-control security test suite.

## 5. Exact-head CI evidence

Workflow: **A3 quality checks**  
Run: **#97**  
Run ID: `43063351008`  
URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43063351008  
Tested head: `5c6b07a80ed7fdf7a96433f1542d357cb392fade`

GitHub Actions job ID: `130671579312`  
Job: `Django, Ruff, and dependency audit`  
Conclusion: **completed / success**

Independently inspected job steps and decoded logs:
- checkout exact A3 SHA: PASS;
- required-file gate: PASS;
- Python 3.14.10 setup: PASS;
- hash-locked dependency installation: PASS;
- Django system check: PASS;
- Django tests: **46 passed**, 0 failures;
- Ruff lint: PASS;
- Ruff format check: PASS;
- pip-audit: **no known vulnerabilities found**.

The workflow log shows the checked-out commit and `git log -1` both equal the reviewed A3 SHA. The latest-attempt job list contains one job, completed successfully, with all listed steps successful.

Earlier failed/cancelled attempts are not counted as successful evidence: run #96 failed due to an incorrect database-settings assumption and was corrected; runs #94 and #95 were cancelled during rapid commits. The successful exact-head run #97 supersedes those attempts for this reviewed SHA.

## 6. Findings and disposition

| Area | Result |
|---|---|
| Exact A3 SHA and change inventory | PASS |
| Current-boundary negative-test logic | PASS |
| Test non-interference / no data creation | PASS |
| Current application URL and view path | PASS |
| No usable Django database / no registered product apps | PASS |
| CI permissions and credential persistence | PASS |
| Exact-head CI and 46 tests | PASS |
| Future AC-01–AC-16 execution | NOT RUN — correctly deferred |
| Future authentication regression execution | NOT RUN — correctly deferred |
| Production penetration / external security review | NOT RUN |
| Protected-data authorization correctness | NOT APPLICABLE — no authorization feature exists |

**A4 technical verification: PASS.** The A3 increment meets its narrowly stated purpose: an executable guard for the current absence of authentication and protected-data routes, plus a clearly separated future access-control test strategy. The test code itself does not add a protected-data access path.

**Closure status:** Owner acceptance pending. This record does not self-authorize a VERIFIED-CLOSED governance disposition. Upon Owner acceptance, this A4 increment may be recorded as VERIFIED-CLOSED within the limited scope above.

## 7. Governance and deployment boundaries

- `main` was not modified; its previously verified SHA remains `adfa62eccda93c8b261e5abd3cbdb22cf28c8823`.
- No merge, deployment, signing, publication, production-data access, institutional role creation, or protected-data access was performed.
- A2 authority/provenance blockers remain open as previously recorded.
- A5 remains a separate gate requiring separate explicit authorization.
