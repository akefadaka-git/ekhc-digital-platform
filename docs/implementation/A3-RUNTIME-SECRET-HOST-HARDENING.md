# A3 — Runtime Secret and Host Configuration Hardening

**Status:** IMPLEMENTED — awaiting exact-head CI verification  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/runtime-security-hardening`  
**Base:** `bb082a8705db011f3ae83320fe72fed13da7d246` (Owner-accepted A4 security/deployment verification closure)

## 1. Objective

Harden startup-time validation of the Django runtime secret and allowed-host configuration. The increment is authority-independent and does not add institutional data, identity, database persistence, or product workflows.

## 2. Implemented controls

- Centralize runtime configuration loading in `config/runtime.py`.
- Require `DJANGO_SECRET_KEY` without printing or echoing its value in configuration errors.
- In production mode, reject keys shorter than 50 characters, keys containing whitespace, and obvious placeholder markers.
- Parse `DJANGO_ALLOWED_HOSTS` into explicit DNS names, IP addresses, or Django-style leading-dot subdomain patterns.
- Reject wildcard entries, URL schemes, ports, paths, whitespace, empty list entries, malformed DNS labels, and case-insensitive duplicates.
- Preserve local development defaults and keep `DEBUG=False`.
- Wire validated values into `config/settings.py`.
- Extend the CI required-file gate to include the new runtime module and regression tests.

## 3. Verification coverage

New regression tests cover:
- explicit DNS/IP/subdomain host entries;
- wildcard, malformed, URL/port/path, whitespace, empty, and duplicate host rejection;
- required secret handling without secret disclosure;
- development compatibility;
- production short, placeholder, and whitespace-containing secret rejection;
- acceptance of a sufficiently long non-placeholder production secret.

The full suite, lint, formatting, Django system check, dependency audit, and exact-head GitHub Actions workflow remain required for A4 verification.

## 4. Operational boundaries

- A 50-character minimum is a configuration floor, not proof of cryptographic entropy. Operators must generate a high-entropy secret and inject it through a protected secret manager or equivalent environment mechanism.
- No production secret, hostname, certificate, proxy, or deployment environment is supplied or assumed.
- The existing production TLS contract remains unchanged: direct TLS termination at Django-facing server; reverse-proxy forwarded-header trust remains disabled.
- No CSP/CORS policy is guessed, no external service is configured, and no authentication/session product flow is introduced.
- No merge to `main`, deployment, signing, publication, or production-data access is included.

## 5. A4 exit criteria

- Exact-head CI succeeds on the final implementation SHA.
- Django system check, all tests, Ruff lint/format, and pip-audit pass.
- Runtime host/secret controls are independently reviewed against the implementation.
- A4 records exact tested SHA, workflow run evidence, findings, limitations, and Owner acceptance status.

A4 and A5 remain separate gates. This A3 record does not claim production readiness.
