# A4 Independent Verification — Dependency and Software Supply-Chain Assurance Baseline

**Verification date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**A3 implementation branch:** `a3/dependency-supply-chain-assurance`  
**Exact A3 implementation head:** `4e0172e5c01e0c865057762c2a0202ca1d959f57`  
**A3 base:** `399bb07ac5ba386907e363e963a9a036ab19d135`  
**A4 branch:** `a4/dependency-supply-chain-assurance-verification`

## 1. Verification disposition

**Technical result: PASS WITH LIMITATIONS.**  
**Owner acceptance: PENDING.**  
**Exact-head CI: NOT CONFIRMED.**  
**Closure status: NOT YET OWNER-CLOSED.**

The A3 increment is narrowly scoped and the inspected source supports the claim that it does not add runtime dependencies or alter application behavior. The static guard is useful for the current lock/workflow conventions, but it is not a semantic YAML policy engine or independent package provenance verifier. No CI success is claimed because the available commit-run lookup did not return push-triggered runs for the exact A3 head.

## 2. Exact-head and scope verification

The A3 compare from `399bb07ac5ba386907e363e963a9a036ab19d135` to `4e0172e5c01e0c865057762c2a0202ca1d959f57` returned:

- 4 commits ahead, 0 behind.
- Exactly 3 changed paths:
  1. `.github/workflows/quality.yml` — one-line required-file gate update.
  2. `docs/security/DEPENDENCY-AND-SUPPLY-CHAIN-ASSURANCE-BASELINE.md` — 184 lines added.
  3. `tests/test_supply_chain_baseline.py` — 108 lines added.
- No application source, settings, runtime dependency manifest, development dependency manifest, lockfile, database, migration, route, or deployment file changed.

Fetched blob identities at the A3 head:

| File | Blob SHA |
|---|---|
| `requirements.txt` | `6cce32a72870adb42a0879c0b5ab7b7421868962` |
| `requirements-dev.txt` | `641bd305c8ad4b81d3dc23a4b790dfbb7f4cd644` |
| `requirements-lock.txt` | `db79c9e58aa6cd6f0798aba30edeeb8f5af20f85` |
| `tests/test_supply_chain_baseline.py` | `4c061bb770dcc79b18906d9e8c0a144dda0ade30` |
| `.github/workflows/quality.yml` | `84b4d4b7d451ef161edaf07c68797924bd3b24b1` |
| Assurance baseline | `2218b28fc92d1b827137acb12d7e124dfe5c3e1c` |

The runtime manifest contains only `Django==5.2.19`. The development manifest includes the runtime manifest and exact pins for Ruff and pip-audit. The lockfile blob is unchanged from the inspected A3 base. This confirms no dependency or lock refresh was part of this increment.

## 3. Independent adversarial review

### 3.1 Dependency and lockfile guards

**PASS WITH LIMITATIONS**

The eight static tests cover:

- non-empty lockfile;
- exact package-version syntax on each non-comment lock entry;
- at least one syntactically valid 64-hex SHA-256 hash per entry;
- rejection of malformed hash tokens;
- direct runtime/development manifest pins matching locked versions;
- Django-only runtime dependency set;
- CI workflow/job read-only `contents: read` permission declarations;
- full 40-character commit-SHA action references;
- checkout credential persistence disabled;
- hash-required install and pip-audit command presence;
- absence of selected artifact upload/attestation patterns and attestation token grants.

The implementation's eight test methods are static source/configuration checks. They do not install packages, execute the application, access a database, or create a data-access path.

**Limitations found:**

1. Lock parsing is line-oriented and tailored to the current generated lock format. It is not a full requirements-file parser and does not independently resolve the dependency graph.
2. Duplicate normalized package names are not explicitly rejected by the test. Pip's hash-checked install remains a separate operational check.
3. The manifest-to-lock test checks direct pins but does not prove the transitive closure is complete. The hash-required CI install is the operational completeness check.
4. SHA-256 syntax and committed digest presence do not prove that the original digest was obtained from an authentic upstream publisher or that the package source is trustworthy.
5. The lock is explicitly scoped by its comments to Python 3.14.10 / Ubuntu 24.04 x86_64. Cross-platform reproducibility is not established.

### 3.2 CI permissions and action references

**PASS WITH LIMITATIONS**

The inspected workflow has workflow-level and job-level `contents: read`; both actions are pinned to full 40-character commit SHAs; checkout sets `persist-credentials: false`; the quality job does not grant repository write, package write, OIDC, or attestation permissions. It uses the hash-checked lock and invokes `pip-audit` against that lock.

**Limitations found:**

1. Permission assertions are regular-expression checks against the current YAML text, not parsed YAML or GitHub's effective permission evaluation. YAML restructuring or alternative permission syntax could evade these guards.
2. The tests do not validate the action SHA against its claimed upstream release tag or independently inspect action source/transitive dependencies.
3. Workflow text inspection does not prove GitHub repository settings: branch protection, required reviewers/status checks, CODEOWNERS enforcement, administrator bypass, organization policy, runner isolation, or cache trust remain UNKNOWN / NOT VERIFIED.
4. A workflow-level static assertion cannot prove that external organization/enterprise policy has not modified the effective token capability.

### 3.3 Vulnerability handling

**PARTIAL**

The workflow invokes `pip-audit -r requirements-lock.txt`. The baseline correctly records that this is point-in-time advisory intelligence and does not imply absence of undisclosed vulnerabilities.

No persistent advisory triage register, severity-based remediation SLA, Owner-approved exception process, or automated advisory intake was evidenced. Those remain open controls.

### 3.4 Artifact provenance

**NOT IMPLEMENTED — correctly bounded**

The current quality workflow does not upload artifacts, publish packages, sign outputs, generate SBOMs, or attest build provenance. No artifact trust claim is made. The regression test protects against selected accidental additions of artifact/attestation steps and privileged token grants.

The test does not provide artifact provenance; no artifact exists in this workflow to verify. A dedicated, Owner-approved release design remains required before any future artifact publication or deployment.

## 4. Security boundary and behavior preservation

Source review confirms the increment changes only the required-file list in the existing quality workflow and adds documentation plus a static test. It does not add application packages, alter Django settings, change URLs, create models/migrations, configure authentication/authorization, introduce secrets, or enable protected-data access.

No production secrets, institutional roles, identity records, protected data, or production integrations were introduced.

## 5. CI evidence

The commit-associated workflow lookup returned no workflow runs for the exact A3 head. That lookup is limited to pull-request-triggered runs and does not establish that a push-triggered run did not occur.

Therefore:

- Exact-head workflow execution: **NOT CONFIRMED**.
- Django test execution on this head: **NOT CONFIRMED**.
- Ruff lint/format on this head: **NOT CONFIRMED**.
- pip-audit result on this head: **NOT CONFIRMED**.

No workflow success, failure, or cancellation is inferred from the empty lookup response. The A4 review does not count CI as passing.

## 6. Acceptance matrix

| Control | A4 result |
|---|---|
| Exact-head changed-file scope | PASS |
| Runtime dependency set unchanged | PASS |
| Development dependency manifest unchanged | PASS |
| Lockfile unchanged | PASS |
| Lock entry/hash static guard | PASS WITH LIMITATIONS |
| Direct pin/lock consistency guard | PASS WITH LIMITATIONS |
| CI least-privilege declarations | PASS WITH LIMITATIONS |
| Full-SHA action pin guard | PASS WITH LIMITATIONS |
| Checkout credential guard | PASS |
| Hash-check install and pip-audit presence | PASS |
| Vulnerability exception/remediation governance | PARTIAL |
| Upstream package provenance | PARTIAL |
| Repository protection / runner controls | UNKNOWN / NOT VERIFIED |
| Build-artifact provenance / SBOM / attestation | NOT IMPLEMENTED |
| Exact-head CI | NOT CONFIRMED |
| Runtime/application behavior change | NONE OBSERVED |

## 7. Required follow-up before stronger assurance claims

1. Run and inspect the complete quality workflow at the exact A3 head; retain the run ID, head SHA, conclusion, and job-step evidence.
2. Strengthen the lock guard to reject duplicate normalized package names and, if the lock format evolves, use a parser aligned with pip requirements syntax.
3. Parse workflow YAML and assert the effective workflow/job permission maps, rather than relying solely on regular expressions.
4. Independently validate action commit SHAs against upstream release/source evidence.
5. Establish a vulnerability advisory register, remediation SLAs, and explicit time-bounded exception governance.
6. Verify repository protection, required reviews, runner isolation, cache trust, and administrator bypass settings.
7. Design SBOM and signed provenance only as a separately approved release-stage increment.

## 8. Governance and final boundary

This record verifies the A3 increment as a technical baseline with limitations. It does not close the broader A2 institutional authority/provenance blockers, authorize authentication/authorization implementation, authorize A5, or certify production readiness.

- Merge: **NOT AUTHORIZED / NOT PERFORMED**.
- Deployment: **NOT AUTHORIZED / NOT PERFORMED**.
- Package publication, signing, SBOM upload, attestation: **NOT AUTHORIZED / NOT PERFORMED**.
- Production-data access: **NOT PERFORMED**.
- Owner acceptance: **PENDING**.

**Final technical disposition: PASS WITH LIMITATIONS; exact-head CI NOT CONFIRMED; Owner acceptance pending.**
