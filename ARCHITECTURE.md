# EKHC OS — Architecture Proposal

**Status:** A1 proposal; not approved or frozen.

## 1. Design principles

1. Model EKHC's verified governance and organizational reality rather than imposing generic structures.
2. Keep the platform independent and API-driven.
3. Prefer clear domain boundaries and a modular starting architecture over premature distributed services.
4. Make authorization server-enforced, deny-by-default, and organization-scope aware.
5. Design offline workflows explicitly, including conflict, revocation and device-loss behavior.
6. Treat localization, Ethiopian calendar support, accessibility and low-connectivity operation as core requirements.
7. Preserve auditability and data provenance for governance records.

## 2. Candidate logical domains

- Organization and governance
- People and membership
- Identity, assignments and access policy
- Ministries and service operations
- Meetings, decisions and resolutions
- Documents and records
- Communication and notifications
- Education and training
- Reporting and analytics
- Shared platform services: audit, search, localization, synchronization, API and integrations

These are candidate boundaries. A1 stakeholder and source analysis must validate ownership, dependencies and scope.

## 3. Candidate system shape

A modular monolith with explicit domain boundaries and a documented API is the initial candidate. A relational database such as PostgreSQL is a candidate persistence layer. Web/PWA and mobile clients consume the same governed application services. Offline data is minimized and encrypted; synchronization uses authenticated, authorized, version-aware operations.

No framework, hosting provider, database schema, or deployment topology is frozen by this document.

## 4. Identity and authorization

Evaluate separation between a person record and an authentication account. A user's active authority should derive from approved, effective-dated assignments and policies, not from client-supplied role labels. Every request, export, search result, report, synchronization operation and background job must enforce server-side authorization.

Revocation, reassignment, account recovery, shared-device use, and emergency access require explicit design and audit controls.

## 5. Offline and synchronization architecture

A1 must classify workflows into:
- Read-only cached content.
- Draft creation and queued submissions.
- Sensitive actions that require connectivity or additional approval.

Define conflict policy per aggregate; do not use silent last-write-wins for governance decisions or other high-integrity records. Define device registration, encryption, local data expiry, remote revocation, replay protection, idempotency, audit and recovery.

## 6. Architecture decisions pending

- Backend and frontend technology selection.
- Modular monolith packaging and domain ownership.
- Database and migration strategy.
- Mobile delivery strategy and PWA capability boundaries.
- Authentication, session and device trust model.
- Offline sync protocol and conflict policy.
- File storage, search and notification providers.
- Hosting, backup, disaster recovery and operational support.
- Integration and data migration boundaries.

## 7. Explicit non-goals

No microservice decomposition without evidence; no production feature implementation during A1; no reuse of ARNA/MASES foundations; no hierarchy schema before authoritative reconciliation; no deployment design treated as approved merely because it appears here.
