# EKHC OS — A4 Security Headers and Deployment Configuration Verification Record

**Verification status:** TECHNICAL PASS — Owner acceptance pending  
**Date:** 2026-11-11  
**Repository:** ake fadaka-git/ekhc-digital-platform  
**Implementation branch:** a3/security-deployment-configuration  
**Implementation SHA tested by CI:** 6ae339305641ace35232981f175d6fe416a12df7  
**Verification branch:** a4/security-deployment-configuration-verification  
**A3 documentation commit:** 9faa2483a04a8591a31ad2366671cf1e6a5c6acc  
**A3 parent baseline:** 65499e3cf949c8b69fa165958cdd47d35b46d388

## 1. Verification scope

A4 reviewed the security middleware ordering, response-header policy, environment parsing and production guards, TLS/HSTS defaults, proxy trust boundaries, regression tests, CI required-file gate, and exact-head workflow evidence.

This is a scoped technical verification. It is not a production deployment test, external security audit, penetration test, certificate/TLS validation, institutional approval, or production-readiness assessment.

## 2. Review findings and dispositions

| ID | Review area | Finding | Disposition |
|---|---|---|---|
| A4-SEC-01 | Security middleware | Django security and clickjacking middleware must run before application middleware | PASS — both middleware classes are registered first; response-header tests verify the expected values |
| A4-SEC-02 | Content/frame/referrer/opener headers | Baseline headers must be explicit and restrictive without inventing resource origins | PASS — nosniff, DENY, same-origin referrer policy, and same-origin COOP are configured and tested |
| A4-SEC-03 | HTTPS/HSTS defaults | Development must not redirect or emit HSTS; production must not start with weak/ambiguous HTTPS settings | PASS — development defaults are redirect-off/HSTS-zero; production requires explicit hosts, HTTPS redirect, and positive HSTS duration |
| A4-SEC-04 | Configuration parsing | Invalid environment names, booleans, and HSTS durations must fail startup | PASS — strict accepted values and bounds are covered by regression tests |
| A4-SEC-05 | Proxy trust boundary | Caller-controlled forwarded headers must not be trusted without a verified proxy chain | PASS — SECURE_PROXY_SSL_HEADER remains None; USE_X_FORWARDED_HOST remains false; regression test verifies forwarded host/proto are ignored |
| A4-SEC-06 | Production cookie flags | Secure cookie transport should be enabled for production mode | PASS — session and CSRF secure flags are true in production mode; no session/authentication product flow is claimed |
| A4-SEC-07 | Regression and scope control | Existing health, localization, and observability behavior must remain intact | PASS — 31 Django tests pass; no database, identity, role, institutional hierarchy, external integration, or production data added |

## 3. Exact-head CI evidence

- Workflow: A3 quality checks
- Run: #80
- Run ID: 43023827925
- Tested SHA: 6ae339305641ace35232981f175d6fe416a12df7
- Result: SUCCESS
- URL: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/43023827925

Verified steps:

| Check | Result |
|---|---|
| Required-file gate | PASS |
| Python 3.14.10 setup | PASS |
| Hash-locked dependency installation | PASS |
| Django system check | PASS |
| Django test suite | PASS — 31 tests |
| Ruff lint | PASS |
| Ruff format | PASS |
| pip-audit | PASS |

Earlier attempts exposed a missing X-frame middleware assertion and import/format issues. Those were corrected. Earlier failed/cancelled attempts are not treated as passing evidence; run #80 is the final exact implementation-head evidence.

## 4. Security boundaries and limitations

- Production-mode settings assume TLS is terminated directly at the Django-facing server. Reverse-proxy TLS termination is not supported by this increment.
- No forwarded host/proto header is trusted. Do not enable proxy trust until the real proxy chain, network restrictions, and header-stripping/rewriting behavior are verified.
- HSTS is disabled in development/test defaults. Production requires a positive duration, but subdomain coverage and preload remain disabled by default. Operators must verify all affected hostnames are HTTPS-ready before enabling production mode.
- No production hostname, certificate, TLS topology, CORS origin, CSP source allowlist, CDN, static asset host, or secret is supplied or assumed.
- Content Security Policy is intentionally deferred until actual UI/resource origins and integrations are verified.
- No production environment, live endpoint, reverse proxy, certificate, browser HSTS persistence, or external service was tested.
- No merge, deployment, signing, publication, or production-data access occurred.

## 5. Governance and conclusion

**A4 technical conclusion: PASS for the restricted security headers and deployment configuration increment.**

The final implementation SHA passed the exact-head quality workflow, including 31 tests, Django system check, Ruff lint/format, and dependency audit. The implementation remains isolated from main.

**Owner acceptance remains pending.** This technical PASS does not close A2, validate institutional authority or legal requirements, authorize production proxy trust, or authorize A5. A5 remains NOT STARTED and separately gated.
