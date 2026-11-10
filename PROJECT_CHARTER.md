# EKHC OS — Project Charter (A1 Draft)

**Status:** Draft for Owner review; not approved or frozen  
**Stage:** A1 — Assessment, specification, and architecture  
**Repository:** `akefadaka-git/ekhc-digital-platform`

## 1. Purpose

EKHC OS is an independent, national digital operating platform intended to support the Ethiopian Kale Heywot Church's governance, organizational administration, people and membership services, ministries, communication, education, records, and operational coordination.

The platform must reflect EKHC's actual constitutional structure, terminology, authority, and operating practices. It must not impose a generic church hierarchy.

## 2. Governance

The project is Owner-governed and stage-gated:

- **A1:** assessment, requirements discovery, formal specification, architecture proposal, risk assessment, and baseline review.
- **A2:** read-only reconciliation against authoritative source material and existing EKHC work.
- **A3:** implementation, only after the required approvals.
- **A4:** verification and acceptance.
- **A5:** deployment-readiness assessment, handled separately. Deployment requires separate authorization.

A stage is not complete merely because draft documents or code exist. Closure requires explicit review evidence and Owner approval.

## 3. Independence and exclusions

- EKHC OS is independent of ARNA/MASES, MaaleNex, IROKA, and other unrelated systems.
- Do not reuse another project's foundation, identity, data model, code, or branding without explicit authorization.
- Do not introduce production features, production data migrations, deployment, signing, or publication during A1.
- Do not replace or overwrite existing EKHC UI or project work before discovery and reconciliation.
- Do not introduce the prohibited organizational terms `ወረዳ` or `District` anywhere in product or project artifacts.

## 4. Foundational product direction

- Amharic-first, multilingual experience.
- Ethiopian calendar as the default, with Gregorian display/preference support where needed.
- Target channels: web, Android, iOS, and offline-capable PWA; final delivery scope is subject to A1 validation.
- Offline-first workflows with controlled synchronization.
- Organization-scoped access, role/permission controls, traceable assignments, and auditability.
- Secure handling of personal, pastoral, governance, and organizational records.

## 5. A1 deliverables

1. Current-state and stakeholder assessment.
2. Source-backed organizational hierarchy and terminology register.
3. Functional and non-functional requirements with priorities and acceptance criteria.
4. Domain and system architecture proposal with alternatives and trade-offs.
5. Security, privacy, data governance, offline synchronization, and operational risk assessments.
6. Existing-work inventory and compatibility/reconciliation plan.
7. Phased roadmap, decision log, and A1 approval package.

## 6. Approval criteria

A1 may be submitted for approval when every material requirement is either source-backed or explicitly marked unresolved; hierarchy and terminology are reconciled against authoritative documents; architecture decisions and trade-offs are documented; risks have owners and mitigations; and no production implementation has been introduced.
