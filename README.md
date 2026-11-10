# Ethiopian Kale Heywot Church Operating System (EKHC OS)

A national, Amharic-first, multilingual digital platform intended to support church governance, administration, membership, ministries, communication, education, and organizational operations across Ethiopia.

## Project status

**Stage:** A1 — Assessment, specification, and architecture (draft; not approved or frozen)

This repository is the independent home of EKHC OS. It is not part of ARNA, MASES, MaaleNex, or IROKA.

## Governance and delivery gates

Work is Owner-governed and stage-gated:

1. **A1 — Assessment and specification:** establish authoritative requirements, validate organizational terminology and hierarchy, assess risks, and prepare the architecture for review.
2. **A2 — Read-only reconciliation:** compare the approved baseline with authoritative source material and existing work without implementation changes.
3. **A3 — Implementation:** begin only after A1 approval and A2 reconciliation authorization.
4. **A4 — Verification:** validate implementation, security, quality, and acceptance criteria.
5. **A5 — Deployment readiness:** assess separately; deployment requires separate authorization.

No production features, production data migrations, deployment, signing, or publication are authorized by this initial repository foundation.

## Foundational constraints

- Amharic-first and multilingual experience.
- Ethiopian calendar as the default calendar, with Gregorian preference support where required.
- Web, Android, iOS, and offline-capable PWA are target delivery channels, subject to A1 validation.
- Offline-first behavior with controlled synchronization is a design requirement to validate.
- Organization-scoped authorization, role/permission controls, and auditable actions are mandatory design concerns.
- The authoritative church hierarchy and terminology must be verified against official EKHC constitutional and governance documents before being encoded.
- Two prohibited legacy organizational labels must not appear in the application, documentation, code, database schemas, APIs, UI, reports, or analytics.
- Existing EKHC UI and related work must be discovered and assessed before any replacement or integration; do not overwrite it blindly.

## Initial documentation

A1 assessment and specification documents will be added as drafts for Owner review. Drafts are not approved policy or frozen architecture.

## Scope discipline

This repository starts with governance, assessment, and specification. Do not introduce production application code or broaden scope without an approved stage gate.
