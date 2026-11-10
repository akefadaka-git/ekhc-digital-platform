# EKHC OS Delivery Roadmap

**Status:** Planning baseline; all later stages remain gated.

| Stage | Purpose | Entry condition | Exit evidence |
|---|---|---|---|
| A1 | Assessment, requirements, architecture and risk baseline | Repository established; Owner mandate | Reviewed specification, source register, architecture and explicit Owner approval |
| A2 | Read-only reconciliation | A1 approved; reconciliation scope authorized | Evidence-backed gap matrix; no implementation changes |
| A3 | Implementation | A2 closed; A3 scope and acceptance criteria authorized | Scoped implementation, review evidence and traceability |
| A4 | Verification | A3 implementation candidate available | Test, security, accessibility, integration and acceptance evidence |
| A5 | Deployment readiness | A4 accepted; separate A5 authorization | Environment-specific readiness decision; deployment separately authorized |

## Delivery principles

- Prefer small, reviewable, traceable changes.
- Preserve unrelated repository work.
- Keep CI and tooling compatible with free/public-repository constraints where practical.
- Do not make paid-service, billing, deployment or publication commitments without explicit approval.
- Report exact commit SHAs, changed paths, test evidence, unresolved items and gate status.
