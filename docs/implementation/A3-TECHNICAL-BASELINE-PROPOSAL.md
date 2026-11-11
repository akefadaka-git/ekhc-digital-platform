# EKHC OS — A3 Technical Baseline Decision Proposal

**Status:** PARTIALLY APPROVED — technical choices 1–6 and the first-increment checklist are Owner-approved; broader product and frontend baseline decisions remain open  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Branch:** `a3/restricted-foundation-scope`  
**Related authorization:** `docs/implementation/A3-RESTRICTED-FOUNDATION-SCOPE.md`

## 1. Decision requested

Approve a technical baseline for a first, authority-independent implementation increment, or return the proposal for revision.

This proposal does not approve constitutional or organizational modeling, production data, an existing UI replacement, deployment, or any paid service. No production database or schema is approved.

## 2. Verified current repository condition

The inspected `main` tree contains project documentation and assessment artifacts. It does not contain an identifiable application source tree, package manifest, lockfile, established test suite, or build pipeline. The prior UI paths recorded in the A2 report were not present on the inspected main ref. UI provenance remains unresolved.

The A1 architecture document explicitly leaves framework, database, API, authentication/session model, offline protocol, storage, hosting, and deployment topology undecided. Therefore, this proposal treats those as decisions, not inherited facts.

## 3. Recommended technical principles

1. **Preserve existing work:** do not create a replacement UI or assume the absent UI paths are disposable.
2. **One deployable application initially:** evaluate a modular monolith with explicit internal boundaries; do not introduce microservices without measured need.
3. **Server-authoritative security:** no client-supplied role, office, organization, or scope value may grant access.
4. **Fail closed:** until constitutional and institutional authority is verified, no organizational hierarchy, role catalogue, or authority-bearing workflow is implemented.
5. **Synthetic-only development:** fixtures must be fictional and contain no real member, pastoral, child, or governance data.
6. **No paid dependency:** local development and automated checks must be usable without a paid account, deposit, billing activation, or paid hosted service.
7. **Reproducibility:** pin supported runtime and dependency versions; commit lockfiles; document deterministic setup and test commands.
8. **Accessibility and localization by design:** preserve Unicode, test Amharic text rendering, and avoid hard-coded Gregorian-only assumptions. Do not invent translations or calendar conversion behavior.
9. **No production claims:** successful unit tests or public CI do not constitute security certification, accessibility conformance, operational readiness, or production acceptance.

## 4. Technology options to evaluate

| Concern | Candidate options | Current disposition |
|---|---|---|
| Backend | Laravel/PHP; Django/Python; FastAPI/Python | Django/Python approved; Python 3.14.10, Django 5.2.19, direct development pins, and the transitive hash lock are recorded. |
| Frontend | Existing UI if recovered; otherwise Vue/TypeScript or React/TypeScript | No selection. Existing UI provenance must be resolved before any replacement or new shell is considered. |
| Persistence | PostgreSQL; SQLite for isolated local tests only if compatible with chosen runtime | Owner approved deferring database and schema implementation from the first A3 increment. No database dependency, migration, schema, or persistence layer is to be added in that increment. Revisit persistence only when an approved requirement demonstrates the need. |
| API | Django-native minimal endpoint for the first increment; Django REST Framework (DRF) deferred | Owner approved Django-native endpoints only for the minimal health/readiness check in the first increment. No general REST API or resource endpoints are approved. DRF is deferred. |
| Tests | Framework-native unit/integration tests; static analysis; dependency audit; accessibility checks where UI exists | First-increment tooling approved and verified: Django test runner, Ruff, and pip-audit. Product/access-control tests remain deferred until those features are separately approved. |
| CI | Public-repository GitHub Actions or documented local commands | Owner-approved and implemented on standard public GitHub-hosted Linux runners with read-only permissions, immutable action SHAs, and a local hash-locked fallback. |
| Delivery | Local development and CI verification only | No hosting, deployment, release signing, or publication in this increment. |

## 5. Proposed first implementation increment (after technical approval)

The first increment should remain deliberately narrow and must not encode institutional authority:

- Establish the approved repository layout and reproducible local developer setup.
- Add a minimal health/readiness check that exposes no secrets or sensitive data.
- Add centralized configuration validation and safe error handling.
- Add structured logging conventions with secret and personal-data redaction.
- Add a test harness and CI checks that run without paid services.
- Add a generic audit-event envelope only if its fields do not imply an authority model or unapproved retention policy.
- Add Unicode and Amharic rendering test fixtures only in an approved UI location; do not create a replacement UI.
- Add calendar conversion only after selecting a reviewed implementation and authoritative test vectors for Ethiopian and Gregorian dates.

**Database boundary:** no database server, ORM persistence integration, migration, schema, model, or database-backed feature is included in this first increment. Tests should use in-memory or framework-supported non-persistent mechanisms where practical. This does not select SQLite or authorize a hidden substitute database.

Each item needs a separate acceptance criterion and focused tests before implementation. This list is not blanket approval to choose dependencies or create product features.

## 6. Explicitly deferred

- Database selection for production, persistence integration, migrations, and all schemas.
- Organization, church, office, ministry, membership, and hierarchy schemas.
- Roles, permissions, delegated authority, scope resolution, and identity-to-office assignment.
- Governance meetings, approvals, minutes, resolutions, and official records workflows.
- Live personal, pastoral, membership, child, or financial data.
- Offline caching or synchronization of sensitive records.
- UI recreation, redesign, or replacement.
- Production migration, hosting, monitoring service purchase, deployment, release signing, or publication.

## 7. Remaining decisions and deferred items

1. **Frontend disposition — UNRESOLVED / DEFERRED:** preserve existing UI if recovered; no replacement is authorized by default.
2. **API approach — RESOLVED:** Django-native minimal health/readiness endpoint only; no general API or DRF.
3. **Test and quality tools — RESOLVED:** Django test runner, Ruff, and pip-audit.
4. **CI approach — RESOLVED:** standard public GitHub Actions runner with local fallback and least privilege.
5. **Runtime — RESOLVED:** Python 3.14.10 and Django 5.2.19, subject to future upstream security re-checks.
6. **First-increment sequence and file-level acceptance checklist — OWNER APPROVED:** exact checklist approved on 2026-11-11 and implementation started on the authorized branch.
7. **First-increment verification and dependency reproducibility — PASS:** the final A3 exact-head CI, tests, Ruff, pip-audit, and transitive SHA-256 hash lock are verified in run #26 at `bf3443b288bcc78d7479630ffa92f0af7c88cd77`; run #22 is retained as historical lock-integration evidence. Broader product and independent A4 acceptance remain open.

Keep all deferred or unresolved items out of executable scope until separately approved.

## 8. Acceptance and governance

The file-level checklist has been created and Owner-approved. The first-increment files and transitive hash lock have been implemented on the authorized A3 branch. Final A3 exact-head workflow run #26 passed hash-locked installation, Django checks/tests, Ruff lint/format, and pip-audit. Run #22 remains historical lock-integration evidence. The Owner accepted A3 first-increment closure before separately authorizing A4 verification. Broader product requirements and A4 independent verification remain separate.

A4 remains a separate verification gate. A2 remains PARTIAL / OPEN until its evidence and closure conditions are separately reconciled and accepted. Merge, deployment, signing, publication, and production data remain separately gated.

## 9. Owner decision record — 2026-11-11

### Decision 1 — backend

**Decision:** APPROVED — Django/Python as the preferred EKHC OS backend candidate.

**Decision scope:** This approval selects Django/Python as the preferred backend for the technical baseline. It does not select an exact Python or Django version, approve dependencies, database/schema, API contracts, frontend technology, authentication/authorization model, or implementation file list.

### Decision 2 — database deferral

**Decision:** APPROVED — defer database and schema implementation from the first A3 increment.

**Decision scope:** The first increment must not add a database server dependency, ORM persistence integration, migrations, schemas, or database-backed product features. Use non-persistent test mechanisms where practical. This is a deferral, not a selection of SQLite or any other database. Reconsider persistence only after a concrete, approved requirement justifies it.

### Decision 3 — first-increment API approach

**Decision:** APPROVED — use Django-native endpoints for the first increment; defer Django REST Framework (DRF).

**Decision scope:** Django-native routing/views may be used only to implement and test the minimal health/readiness check described in Section 5. The endpoint must not expose secrets, personal data, organizational data, or internal configuration values. This decision does not approve a general REST API, resource endpoints, authentication API, data endpoints, API contracts, or DRF dependency. Any broader API surface requires a separate Owner decision.

### Decision 4 — Python and Django runtime versions

**Decision:** APPROVED — Python 3.14.x with Django 5.2 LTS for the first increment, with exact patch versions pinned in project files.

**Verified patch baseline on 2026-11-11:** Python **3.14.10** and Django **5.2.19**. Python.org lists 3.14.10 as the latest 3.14 maintenance release and Python 3.14 remains in bugfix support through October 2030. Django's official download page lists 5.2.19 as the latest 5.2 LTS patch and extended support through April 2028. Django 5.2 supports Python 3.14 from 5.2.8 onward. Sources: https://www.python.org/downloads/release/python-31410/ ; https://www.djangoproject.com/download/ ; https://docs.djangoproject.com/en/5.2/releases/5.2/

**Decision scope:** Pin Python 3.14.10 and Django 5.2.19 when the first-increment project files are created. This does not approve additional runtime packages, database integration, production hosting, or deployment. Re-check upstream security releases immediately before implementation and use a newer compatible patch if one has superseded these versions; record the exact change and evidence.

**Implementation authorization:** These decisions record technical direction only. Executable implementation remains NOT STARTED pending the remaining technical decisions and a file-level acceptance checklist.

**Constraints retained:** synthetic data only; preserve existing UI; no invented organizational hierarchy, offices, mandates, roles, permissions, or governance workflows; no paid services; no main-branch changes; no merge, deployment, signing, or publication without separate approval.



### Decision 5 — first-increment test and quality toolchain

**Decision:** APPROVED — use Django's built-in test runner for unit and integration tests, Ruff for Python linting and formatting, and pip-audit for dependency vulnerability checks. Defer additional static type checking until the first increment establishes meaningful interfaces.

**Decision scope:** These tools are approved for the narrowly scoped first increment. Their configuration must be reproducible and usable locally without paid services. Dependency-audit results must be recorded; a clean audit is not a security certification. Do not add unrelated quality platforms or paid services. Any additional tool or materially broader check requires a separate justification and approval.



## 11. CI and local verification approach — Owner-approved

**Recommendation:** Use one minimal GitHub Actions workflow on the public repository, on standard GitHub-hosted Linux runners only (for example, `ubuntu-24.04`). Do not use larger runners, paid hosted services, deployment jobs, or workflows that require secrets.

**Cost evidence checked 2026-11-11:** GitHub's current documentation states that standard GitHub-hosted runners are free and unlimited for public repositories. Larger runners are billed even for public repositories. This proposal therefore excludes larger runners and any service that could incur a charge. Sources:
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners

**Approved workflow behavior:**
- Trigger on pull requests and pushes to the authorized A3 working branch; optionally support manual dispatch.
- Use least-privilege workflow permissions; no write permissions unless a later, separately approved job requires them.
- Set up the approved Python patch version, install only pinned project dependencies, then run Django tests, Ruff checks, and pip-audit.
- Do not run on `main` as a development target or change branch protection/settings.
- Do not upload artifacts, publish packages, deploy, sign releases, or access production credentials.
- Pin third-party actions to immutable commit SHAs when the workflow is eventually authored; document the reviewed action versions.

**Local fallback:** Provide a documented, reproducible sequence using the same Python version and dependency lock:
1. Create/activate a virtual environment.
2. Install the pinned development requirements.
3. Run `python manage.py test`.
4. Run `ruff check .` and `ruff format --check .`.
5. Run `pip-audit`.

The local commands are illustrative until the project files and dependency lock exist. Do not claim the commands pass before implementation and execution evidence exists.

**Owner decision:** APPROVED on 2026-11-11. The workflow file has been created on the authorized A3 branch. A passing CI run is not claimed until its exact run and commit status are observed.



### Decision 6 — CI and local verification approach

**Decision:** APPROVED — use a minimal GitHub Actions workflow on standard GitHub-hosted Linux runners for this public repository, subject to the safeguards in Section 11, with documented local commands as the fallback.

**Decision scope:** Standard public-repository runners only; no larger runners, paid hosted services, billing activation, secrets, deployment, release signing, publication, or production access. Workflow permissions must be least-privilege. Third-party actions must be pinned to reviewed immutable commit SHAs when the workflow is authored. Local and CI checks must use the same pinned Python/dependency baseline. No CI success is claimed until an actual run is observed.

**Implementation boundary:** This approves preparation of the workflow specification and file-level acceptance checklist. It does not by itself approve merging, deployment, or expansion beyond the first increment. Create the executable workflow only with the approved checklist and ensure it does not report success when required application files are absent.


## 10. Current disposition

- Backend: **OWNER-APPROVED — Django/Python**.
- Runtime: **OWNER-APPROVED — Python 3.14.10 + Django 5.2.19**.
- First-increment API: **OWNER-APPROVED — Django-native health/readiness endpoint only; DRF DEFERRED**.
- Database/schema: **OWNER-APPROVED — DEFERRED**.
- Test runner: **OWNER-APPROVED — Django built-in test runner**.
- Lint/format: **OWNER-APPROVED — Ruff 0.17.4**.
- Dependency audit: **OWNER-APPROVED — pip-audit 2.10.1**.
- Direct dependency inputs: `requirements.txt` and `requirements-dev.txt`.
- Transitive dependency lock: `requirements-lock.txt`, 32 exact package versions and 402 SHA-256 hashes.
- Final A3 exact-head hash-locked CI: **PASS — run #26 at `bf3443b288bcc78d7479630ffa92f0af7c88cd77`**, including `pip install --require-hashes`, Django check/tests, Ruff, and pip-audit; no known vulnerabilities found in that audit.
- First-increment A3 closure recommendation: **READY FOR OWNER REVIEW**; not automatically closed.
- Frontend: **UNRESOLVED / DEFERRED**; preserve existing UI and do not replace it.
- Database, authentication, authorization, hierarchy, roles, governance workflows, production data, hosting, deployment: **DEFERRED / EXCLUDED**.
- A2: **PARTIAL / OPEN**.
- A4: **IN PROGRESS**; see `docs/implementation/A4-INDEPENDENT-VERIFICATION-RECORD.md`.
- A5: **NOT STARTED**.
- Main branch: **MUST REMAIN UNCHANGED**.
- Merge/deployment/signing/publication: **NOT AUTHORIZED**.

## 12. First-increment checklist approval and implementation record — 2026-11-11

The Owner-approved checklist at `docs/implementation/A3-FIRST-INCREMENT-ACCEPTANCE-CHECKLIST.md` governs the restricted first increment. The Django foundation, minimal health endpoint, tests, Ruff configuration, public-runner CI workflow, local setup instructions, and transitive hash lock have been created on `a3/restricted-foundation-scope`.

**Dependency reproducibility:** direct pins remain in `requirements.txt` and `requirements-dev.txt`. The committed `requirements-lock.txt` pins 32 resolved runtime/development packages and carries 402 SHA-256 hashes for the published release files of those exact versions. It is installed with pip `--require-hashes`.

**Historical lock-integration verification:** A3 quality workflow run #22 at commit `628dccda9d12fa78a29cecfe9520452f930b5df3` succeeded. **Final A3 exact-head verification:** run #26 at `bf3443b288bcc78d7479630ffa92f0af7c88cd77` succeeded, including hash-locked installation, Django check, three tests, Ruff lint/format, and pip-audit. The audit reported no known vulnerabilities. Run #26: https://github.com/akefadaka-git/ekhc-digital-platform/actions/runs/42968545687

The A3 first-increment closure was accepted by the Owner before A4 authorization. This does not imply and does not authorize merge, deployment, signing, publication, production data, or any A2-dependent feature. No database, UI, organizational authority model, or product workflow is included.
