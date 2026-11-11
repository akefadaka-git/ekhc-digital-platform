# A3 — Security Headers and Deployment Configuration Foundation

**Status:** IMPLEMENTATION IN PROGRESS — verification pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/security-deployment-configuration`  
**Base:** `65499e3cf949c8b69fa165958cdd47d35b46d388` (Owner-approved secure observability A4 closure)

## 1. Objective

Establish conservative Django security response headers, explicit and validated deployment-mode settings, and a fail-closed boundary around TLS/proxy assumptions. This increment is authority-independent and does not introduce institutional data, identity, or application features.

## 2. Scope

- Enable Django `SecurityMiddleware` before application middleware.
- Preserve `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.
- Set a restrictive same-origin referrer policy and cross-origin opener policy.
- Validate environment mode, HTTPS redirect, HSTS duration, and HSTS subdomain configuration.
- Require explicit allowed hosts, HTTPS redirect, and positive HSTS duration in production mode.
- Enable secure session/CSRF cookie flags in production mode.
- Keep wildcard hosts rejected and `DEBUG=False`.
- Keep `SECURE_PROXY_SSL_HEADER=None` and `USE_X_FORWARDED_HOST=False`; do not trust forwarded headers without an independently verified proxy chain and header-stripping contract.
- Add regression tests for response headers, default behavior, malformed configuration, and production guards.

## 3. Deployment contract and limitations

The production-mode settings assume TLS is terminated directly at the Django-facing server, so Django can determine HTTPS from the connection scheme. Reverse-proxy TLS termination is **not supported by this increment**. Do not set or infer `SECURE_PROXY_SSL_HEADER`, `USE_X_FORWARDED_HOST`, proxy IP ranges, forwarded host/proto trust, or a proxy chain. A later increment must verify the actual infrastructure and ensure the trusted proxy strips and sets forwarding headers before enabling any proxy trust.

HSTS is disabled in development/test defaults. Production mode requires an explicit positive HSTS duration, but this code does not enable subdomain coverage or browser preload by default. Operators must confirm that every affected hostname is permanently HTTPS before production configuration is supplied; HSTS can persist in browsers and cause access failures if enabled prematurely.

No hostname, certificate, TLS topology, reverse proxy, CORS origin, CSP source allowlist, CDN, static asset host, or secret value is invented. Content Security Policy is intentionally not added until actual UI/resource origins and required integrations are verified. No production environment is configured by this repository change.

## 4. Configuration variables

| Variable | Development/test default | Production requirement |
|---|---|---|
| `DJANGO_ENVIRONMENT` | `development` | `production` |
| `DJANGO_ALLOWED_HOSTS` | Existing explicit local/test hosts | Explicit deployment hostnames; wildcard forbidden |
| `DJANGO_SECURE_SSL_REDIRECT` | `false` | `true` |
| `DJANGO_SECURE_HSTS_SECONDS` | `0` | Positive whole number, at most 63072000 |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | `false` | Optional; requires positive HSTS duration |
| `DJANGO_SECRET_KEY` | Required as before | Required as before; secret manager/environment only |

Boolean values accept only `true`/`false` or `1`/`0`. Invalid or ambiguous values fail startup. Production also enables secure session and CSRF cookie flags. The app currently has no session or CSRF-backed product flows; these flags are preventive defaults, not proof of a complete authentication design.

## 5. Verification criteria

- Security headers appear on normal responses.
- HSTS is absent on plain HTTP development responses.
- Development defaults do not redirect or trust proxy headers.
- Invalid booleans, HSTS values, environment names, and unsafe production omissions fail closed.
- Existing health, localization, and observability behavior remains intact.
- Django checks, all tests, Ruff lint/format, dependency audit, and exact-head CI pass.
- A4 verifies the exact implementation head and records deployment limitations.

## 6. Explicit exclusions

No proxy trust, CORS policy, CSP allowlist, hostname, certificate, secret, production data, database, authentication, authorization, institutional hierarchy, external service, merge, deployment, signing, or publication is introduced. A2 remains open and A5 remains separately gated.
