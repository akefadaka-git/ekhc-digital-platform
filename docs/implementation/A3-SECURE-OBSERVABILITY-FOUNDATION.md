# A3 — Secure Request Observability Foundation

**Status:** IMPLEMENTED — exact-head CI pending  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/secure-observability-foundation`  
**Base implementation:** `96198cad6b3e2731a7bfedf8511c2be85409c8bd`

## 1. Objective

Add a narrow, authority-independent observability foundation to the existing Django skeleton: server-generated request correlation IDs and structured operational request logs with strict data minimization.

## 2. Implemented behavior

- Generate a fresh UUIDv4 request ID for every request; do not trust or reflect caller-supplied `X-Request-ID` values.
- Attach the ID to the request as `request.request_id` and return it as `X-Request-ID` on successful responses.
- Use a `ContextVar` and logging filter to correlate log records emitted during the active request.
- Emit one JSON request-completion event with a fixed event name, timestamp, log level, request ID, normalized HTTP method, response status, elapsed milliseconds, and exception class name when applicable.
- Serialize only an explicit allowlist. Raw log messages, arbitrary `extra` fields, paths, query strings, headers, request bodies, user identifiers, credentials, tokens, and personal data are not serialized.
- Reset request context in a `finally` block to prevent request ID leakage across reused execution contexts.
- Extend CI's required-file check to include the new middleware and tests.

## 3. Security and privacy boundaries

This is data minimization, not a claim that arbitrary application logging is automatically safe. The configured request logger uses the safe JSON formatter and does not include request-controlled content. Future application loggers must not bypass this policy or emit secrets.

No request or response bodies, authorization headers, cookies, query strings, URL paths, IP addresses, user identities, or institution-specific data are collected by this middleware. No retention period, external log sink, monitoring vendor, SIEM integration, or privacy-policy assumption is introduced.

The request ID is a correlation identifier, not an authentication credential, authorization token, or trusted identity assertion. Incoming request IDs are intentionally ignored to prevent spoofing and log correlation injection.

## 4. Files changed

- `config/observability.py` — request correlation, context filter, safe JSON formatter, completion logging.
- `config/settings.py` — middleware registration and dedicated logger configuration.
- `tests/test_observability.py` — UUID response header, caller-ID non-reflection, allowlist privacy, and method normalization tests.
- `.github/workflows/quality.yml` — require observability source and tests in CI.

## 5. Verification criteria

- Django system check passes.
- Existing tests remain green.
- New observability tests pass.
- Ruff lint and format pass.
- pip-audit reports no known vulnerabilities.
- CI runs against the exact implementation head.
- A4 review verifies request-ID generation, context reset, safe field allowlisting, and scope boundaries.

## 6. Explicit exclusions

No database, migrations, authentication, user identity, roles, authorization, institutional hierarchy, retention policy, log shipping, monitoring vendor, frontend/UI, production credentials, production data, deployment, merge, signing, or publication is introduced. A2 remains open and A5 remains separately gated.
