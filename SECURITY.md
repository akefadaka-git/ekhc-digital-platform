# EKHC OS Security and Privacy Baseline

**Status:** A1 draft; threat model and controls require review.

## Security objectives

- Confidentiality of personal, pastoral, membership and governance information.
- Integrity of membership, office assignments, minutes, resolutions and records.
- Availability and recoverability under intermittent connectivity.
- Accountability for privileged access and sensitive actions.

## Minimum design requirements

1. Deny-by-default authorization enforced on the server.
2. Explicit organization scope and effective-dated assignments.
3. Separation of authentication identity, person record, role, position and permission.
4. Strong session management, secure account recovery and multi-factor authentication options for privileged users.
5. Encryption in transit and at rest, including offline device stores and backups.
6. Tamper-evident audit records for privileged changes and sensitive access.
7. Data minimization, classification, retention and secure deletion rules.
8. Rate limiting, input validation, output encoding, CSRF protection where applicable, and secure file handling.
9. Dependency and vulnerability management, secret handling, and reproducible release controls.
10. Tested backup, restore, incident response and access-revocation procedures.

## Threat scenarios to assess

- Cross-organization data exposure through an incorrect scope check.
- Stolen or shared mobile device exposing cached personal records.
- Unauthorized elevation through manipulated client role/scope values.
- Replay or duplicate submission during offline synchronization.
- Unauthorized changes to governance minutes or resolutions.
- Compromised privileged account or insecure recovery process.
- Data leakage through exports, search, notifications, logs or analytics.
- Insider misuse and insufficient audit review.

## A1 work required

Create a data classification matrix, threat model, privacy impact assessment, privileged-access model, audit and retention policy, offline-device control specification, and incident response outline. No security certification or production readiness is claimed by this draft.
