# EKHC OS — Mock Notification Architecture and Configuration Specification

**Status:** PHASE 1.2 SPECIFICATION — PROPOSED FOR OWNER REVIEW  
**Date:** 2026-11-12  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Specification branch:** `ops/mock-notification-architecture-spec`  
**Parent baseline:** `cd65178b09bec76353ea49cc3d4046b972e44671`

## 1. Purpose and scope

Define a safe interim notification architecture while institutional email and SMS services are not yet available. The interim system is mock-only: it exercises application behavior and produces synthetic evidence without contacting external providers or real people.

This is a specification only. It does not implement adapters, modify workflows, create GitHub secrets, configure providers, activate notifications, or authorize a rehearsal, production operation, merge, deployment, or A5.

## 2. Confirmed constraints and policy alignment

- Institutional email is the future primary channel; SMS is the future secondary channel, per the Owner-approved ORG-02 policy.
- Neither institutional service is currently available.
- Recipient identities, responder assignments, and restricted-record custody are not established.
- No real names, email addresses, phone numbers, credentials, private endpoints, or confidential exception details may be stored in public repository files or test fixtures.
- The mock implementation must make no outbound network calls.
- A simulated delivery receipt is not provider delivery, human receipt, acknowledgement, or remediation.
- The existing monitoring workflow remains read-only. Existing permissions, triggers, secrets, exception register, schedule state, and production boundaries must not be expanded by this specification.
- Production notification integration and controlled operational rehearsal require separate Owner authorization.

## 3. Proposed logical architecture

```text
Security monitor event
        |
        v
Notification policy / severity mapper
        |
        v
Notification orchestrator
        |
        +---- Email adapter interface ---- Mock email adapter (MOCK only)
        |
        +---- SMS adapter interface ------ Mock SMS adapter (MOCK only)
        |
        v
Synthetic event / receipt recorder
        |
        v
Test assertions and redacted CI summary
```

The orchestrator should be provider-neutral. Adapter interfaces should be stable so a future provider implementation can be added without changing severity mapping, notification policy, or the monitoring engine.

The mock adapters must not import or instantiate live provider SDKs. The mock-only build/test path must not contain a hidden fallback to a live adapter.

## 4. Configuration contract

Recommended non-secret configuration:

| Key | Allowed interim value | Default / failure behavior |
|---|---|---|
| `EKHC_NOTIFICATION_MODE` | `mock` | Missing, blank, or unknown value: fail closed |
| `EKHC_EMAIL_MODE` | `mock` | Missing or unknown: disabled / fail closed |
| `EKHC_SMS_MODE` | `mock` | Missing or unknown: disabled / fail closed |
| `EKHC_NOTIFICATION_FIXTURE_SET` | A named synthetic fixture set | Missing: use no recipients; never infer real recipients |
| `EKHC_NOTIFICATION_LOG_LEVEL` | `summary` or `debug` | Default to redacted summary |

For this interim phase, only `mock` is an accepted mode. Values such as `live`, `production`, `smtp`, `http`, `provider`, or arbitrary mode strings must be rejected. Do not introduce a live mode until a separately approved design and implementation change.

Configuration validation must:
1. Validate enumerated values exactly.
2. Reject unexpected configuration keys where practical.
3. Avoid printing environment values in logs.
4. Avoid logging recipient-like values or payload contents.
5. Ensure the mock adapter cannot perform DNS resolution, socket creation, HTTP requests, SMTP, SMS API calls, or other external I/O.
6. Treat any attempted real endpoint or credential configuration as a configuration error, not a reason to fall back.

## 5. Adapter interface and behavior

Each adapter should implement a narrow interface conceptually equivalent to:

- `send(notification, destination_reference) -> DeliveryReceipt`
- `validate_configuration() -> ConfigurationStatus`

The interface accepts only:
- a normalized notification event;
- a synthetic destination reference, such as `synthetic-email-recipient-01` or `synthetic-sms-recipient-01`;
- a generated correlation/event ID.

It must not accept raw real email addresses or phone numbers in the mock implementation.

Mock adapter outcomes must be deterministic and fixture-driven:
- `SIMULATED_ACCEPTED`: mock adapter accepted the fixture for simulation only;
- `SIMULATED_REJECTED`: fixture represents a deterministic rejection;
- `SIMULATED_TIMEOUT`: fixture represents a timeout;
- `SIMULATED_UNAVAILABLE`: fixture represents an unavailable provider;
- `SIMULATED_RETRY_EXHAUSTED`: all configured mock attempts exhausted.

Every receipt must include `simulated=true` and `delivery_claim=false`. The UI, logs, tests, and reports must display the phrase **SIMULATED — NOT DELIVERED** for mock outcomes. Never use statuses such as `DELIVERED`, `SENT`, `PROVIDER_ACCEPTED`, or `ACKNOWLEDGED` for mock results.

## 6. Synthetic fixture model

Use only obviously synthetic identifiers and reserved example values. Suggested fixture identifiers:

- Email destination: `synthetic-email-recipient-01`
- SMS destination: `synthetic-sms-recipient-01`
- Primary responder: `synthetic-primary-responder`
- Backup responder: `synthetic-backup-responder`
- Escalation authority: `synthetic-owner-escalation-role`
- Evidence record: `SYNTH-EVIDENCE-0001`

Do not use real or routable contact details. Do not use personal data belonging to staff, shareholders, board members, or any other person, even if temporarily available.

A synthetic notification payload may contain:
- synthetic event/correlation ID;
- severity enum;
- package or component name from a synthetic test;
- synthetic advisory reference;
- timestamp;
- workflow/test run reference;
- required-action code.

It must exclude:
- credentials, tokens, API keys, or private endpoints;
- private contact details;
- confidential exception rationale or restricted-record contents;
- personal or sensitive data.

## 7. Delivery, retry, idempotency, and audit semantics

- Mock outcomes must be deterministic for a given fixture and test case.
- Retry tests must use a bounded attempt count and bounded backoff; no real waiting is required if a fake clock/sleeper is used.
- Retry only outcomes explicitly classified as transient by the test fixture.
- Permanent configuration or validation errors must fail closed without retry.
- Each notification must carry an idempotency/correlation key so tests can assert duplicate suppression.
- A repeated monitor signal may produce a repeated notification according to policy; do not claim exactly-once delivery.
- Record separate events for `notification_requested`, `mock_attempted`, `mock_result`, `mock_retry_exhausted`, and `human_acknowledgement_simulated`.
- The mock acknowledgement fixture is not evidence of real human acknowledgement and must always be labeled simulated.
- Logs and CI summaries must contain only opaque IDs, status, severity, timestamps, and test/run references.

## 8. Required automated test matrix

| Test | Expected result |
|---|---|
| Mock email success fixture | Synthetic receipt; `simulated=true`; not delivered |
| Mock SMS success fixture | Synthetic receipt; `simulated=true`; not delivered |
| Mock email/SMS rejection | Deterministic simulated failure |
| Transient mock failure | Bounded retries and expected backoff |
| Retry exhaustion | Explicit simulated failure; no live fallback |
| Invalid/missing mode | Fail closed |
| Attempt to configure live mode | Rejected before adapter initialization |
| Real-looking destination input | Rejected by mock interface |
| Duplicate event/idempotency key | Expected duplicate behavior; no false delivery claim |
| Payload redaction | No secrets, contact details, or confidential content in logs |
| External I/O guard | No network/DNS/socket/SMTP/provider calls |
| Mock acknowledgement | Explicitly simulated; never counted as human acknowledgement |
| CI summary | Shows simulated status and does not claim delivery |

Tests should use injected clocks, deterministic fixtures, and network-call guards. Do not create real exception records or contact actual recipients to test this matrix.

## 9. Future live-service transition gate

A future live adapter is out of scope. Before any live integration is proposed, all of the following must be evidenced in restricted records:

1. Institutional email tenant, mailbox, sender identity, account owner, administrator, and approved authentication method.
2. Institutional SMS provider, account owner, sender identity, API/service configuration, and approved authentication method.
3. Owner-authorized recipient roster, role mapping, authorization basis, recipient acceptance, and joiner/leaver process.
4. Accepted primary/backup responder assignments, coverage calendar, timezone, holiday and absence handling, escalation authority, and acknowledgement evidence source.
5. Restricted records system, system owner, primary/backup custodians, access groups, MFA, encryption, audit logging, retention, backup/recovery, and disposal evidence.
6. Credential custody and rotation plan; secrets must be stored in the approved secret manager, never in source, fixtures, logs, or public documentation.
7. Separate threat review, implementation plan, test plan, and explicit Owner authorization for the live integration and any controlled rehearsal.

A future live adapter must be separately reviewed and must not be enabled merely by changing an environment variable in an existing deployment.

## 10. GitHub Actions variables and secrets guidance

- Mock selectors and non-sensitive fixture-set names are configuration, not secrets. If repository-level storage is needed, use GitHub Actions Variables, not Secrets.
- Real provider credentials, API tokens, and private authentication material belong in GitHub Actions Secrets only after the corresponding institutional service exists and the Owner approves the integration.
- Secret names are identifiers, not evidence that secrets exist. Suggested future names:
  - `EKHC_EMAIL_PROVIDER_CREDENTIAL`
  - `EKHC_EMAIL_SENDER_IDENTITY`
  - `EKHC_SMS_PROVIDER_CREDENTIAL`
  - `EKHC_SMS_SENDER_IDENTITY`
- No secret values are specified in this document. No secret or variable is created by this specification.
- Never echo secret values. If later workflows need to verify configuration, check only whether required values are present, without printing them.
- Do not place dummy values in secrets as a substitute for a mock adapter. A mock adapter should be testable without any secret configured.

## 11. Operational and governance limitations

This design can validate software behavior, formatting, routing, retry logic, redaction, and audit-event generation. It cannot validate:
- actual email/SMS provider availability or delivery;
- sender reputation, carrier routing, spam filtering, or provider rate limits;
- recipient authorization or acceptance;
- real responder coverage or human acknowledgement;
- restricted-record custody controls;
- operational readiness or production readiness.

The existing A4 technical verification remains VERIFIED-CLOSED WITH EXPLICIT LIMITATIONS. This specification does not reopen A4 or change its closure.

## 12. Phase 1.2 acceptance criteria

Phase 1.2 is ready for Owner review when:
- mock-only architecture and configuration are documented;
- live delivery is explicitly excluded;
- fail-closed behavior is specified;
- synthetic identifiers and data boundaries are explicit;
- receipt semantics cannot be confused with delivery or acknowledgement;
- retry, idempotency, redaction, and no-network tests are specified;
- future live-service prerequisites and governance gates are documented;
- no secrets, variables, provider accounts, recipients, or production controls are created or changed.

**Phase 1.2 status:** SPECIFICATION WRITTEN — OWNER REVIEW REQUIRED.  
**A3 mock-adapter implementation:** NOT STARTED — requires separate explicit Owner authorization.  
**Operational rehearsal:** NOT AUTHORIZED / NOT RUN.  
**Production readiness:** NOT READY.

## 13. Change-control boundary

Only this specification document is added by this branch. No application code, test code, workflow, permissions, dependencies, secret, variable, exception register, schedule, or production configuration is changed. No merge, deployment, publication, signing, or A5 is performed or authorized.
