# EKHC OS — Dependency and Software Supply-Chain Assurance Baseline

**Status:** A3 baseline established; current controls partially verified; artifact provenance not implemented  
**Date:** 2026-11-11  
**Repository:** `akefadaka-git/ekhc-digital-platform`  
**Base:** `399bb07ac5ba386907e363e963a9a036ab19d135` — Owner-accepted A4 trust-boundary architecture closure  
**Scope:** dependency provenance, lock integrity, vulnerability handling, CI permissions, build-artifact provenance

## 1. Objective and safety boundary

Establish a reviewable minimum assurance baseline for the Python dependency and GitHub Actions supply chain. Preserve application behavior and the existing runtime dependency set.

This increment is deliberately limited to documentation and static regression guards. It must not add runtime or development packages, change package versions or lock hashes, alter application code/configuration, introduce build or release artifacts, enable artifact publishing, grant CI write permissions, or change deployment behavior.

**Non-goals:** production deployment, containerization, package publication, signing, attestations, SBOM generation, dependency auto-updates, runtime dependency changes, and changes to authentication/authorization or institutional authority.

## 2. Current inventory and evidence

### 2.1 Dependency manifests

| File | Current purpose | Observed content |
|---|---|---|
| `requirements.txt` | Runtime dependency manifest | `Django==5.2.19` only |
| `requirements-dev.txt` | Development/test tools | Includes runtime manifest; pins `ruff==0.17.4` and `pip-audit==2.10.1` |
| `requirements-lock.txt` | Complete CI install lock | Exact versions and SHA-256 hashes for the resolved dependency set |
| `.python-version` | Python toolchain selection | `3.14.10` |

The lock comments state that the file was resolved on Python 3.14.10 / Ubuntu 24.04 x86_64 and that release-file hashes were sourced from PyPI. The manifest is consumed by CI with `pip install --require-hashes -r requirements-lock.txt`.

**Important distinction:** hash checking constrains downloaded bytes to the committed digest. It does not independently prove package publisher identity, source repository ownership, build provenance, or that the committed digest was originally obtained from a trustworthy publisher channel. The current workflow does not set an explicit package index URL; the effective pip index may be influenced by runner or environment configuration. Source identity therefore remains PARTIAL.

### 2.2 Vulnerability handling

The current workflow runs:

```sh
pip-audit -r requirements-lock.txt
```

This checks the locked dependency set against the vulnerability data available to the audit service at run time. A clean result is point-in-time evidence, not a guarantee that a dependency is safe or that no undisclosed vulnerability exists.

No suppression/ignore policy, exception register, severity-based remediation SLA, security advisory owner, or automated update bot is established by this baseline. Findings must not be silently suppressed or fixed by an unreviewed version bump.

### 2.3 CI workflow permissions and action provenance

The current `.github/workflows/quality.yml` was inspected:

- Workflow-level permission: `contents: read`.
- Job-level permission: `contents: read`.
- Checkout action pinned to a full 40-character commit SHA; checkout uses `persist-credentials: false`.
- Python setup action pinned to a full 40-character commit SHA.
- Dependency installation uses the committed hash lock.
- Vulnerability audit runs against that same lock.
- No `contents: write`, `packages: write`, `id-token: write`, or `attestations: write` grant is present.
- No artifact upload or provenance-attestation step is present.

This is a useful least-privilege CI baseline for quality checks. It does not establish repository branch-protection settings, required-reviewer rules, GitHub organization policy, runner isolation, or administrator bypass controls; those settings have not been independently verified here.

### 2.4 Build artifacts and provenance

The inspected quality workflow runs checks and does not build or publish a release artifact. No build-artifact provenance or signed attestation is currently generated or verified.

Disposition: **NOT IMPLEMENTED / NOT APPLICABLE TO CURRENT QUALITY-ONLY WORKFLOW**. Do not describe the current workflow as SLSA-compliant, attested, reproducible, or artifact-verified.

## 3. Required baseline controls

### DEP-01 — Dependency declaration and provenance

1. Runtime and development dependencies remain separated.
2. Direct dependencies use exact version pins; no floating ranges, editable installs, VCS references, or unreviewed direct URLs.
3. Each new direct or transitive dependency requires a recorded purpose, upstream project, licence review, maintenance/release health review, and vulnerability review before approval.
4. Record the canonical upstream project and package index/source for each dependency during future dependency review.
5. Prefer the canonical public package index and verify upstream release metadata/digests independently before refreshing the lock.
6. Treat a package-name collision, unexpected maintainer/repository change, unexplained release, or unexpected dependency-tree expansion as a supply-chain risk requiring investigation.
7. Do not add runtime packages as part of this assurance baseline.

Current status: **PARTIAL** — exact pins and lock hashes exist; upstream identity/source policy and independent provenance verification are not yet automated.

### DEP-02 — Lockfile integrity and reproducibility

1. CI installs only from `requirements-lock.txt` with `--require-hashes`.
2. Every resolved package entry must be exactly pinned and carry one or more valid SHA-256 hashes.
3. Every direct runtime and development pin must exist at the same version in the lock.
4. Lock refreshes are explicit, reviewable changes; no CI-time resolution or unpinned installation.
5. A lock refresh must include the reason, old/new dependency inventory, upstream source, hash provenance, vulnerability audit result, and test result.
6. Lock regeneration must not be combined with unrelated application changes.
7. Platform-specific wheel/source distributions and Python version compatibility must be considered before claiming cross-platform reproducibility.

Current status: **BASELINE PRESENT; STATIC GUARDS ADDED IN THIS INCREMENT**. The existing lock is platform-scoped by its own comment; cross-platform reproducibility is not claimed.

### DEP-03 — Vulnerability handling

1. Run `pip-audit` against the exact committed lock on every quality workflow run.
2. A newly detected vulnerability fails the quality gate until investigated.
3. Record the advisory identifier, affected package/version, fixed version if available, severity/source, exploitability context, exposure, owner, disposition, and target remediation date.
4. Remediate by a separately reviewed lock refresh; do not patch installed packages in CI or bypass hash checking.
5. Any exception must be explicit, time-bounded, justified, risk-accepted by the Owner, and revalidated on expiry or material advisory change.
6. Never treat “no known vulnerabilities reported” as proof of safety.
7. Define formal severity-based remediation SLAs and exception authority before production use.

Current status: **PARTIAL** — automated audit exists; durable finding/exception workflow and Owner-approved remediation SLAs are not yet established.

### DEP-04 — CI workflow and action permissions

1. Keep workflow and job permissions explicitly minimal; quality checks remain `contents: read`.
2. Pin every third-party action to a full commit SHA. A version comment is informational and must not replace the SHA pin.
3. Keep checkout credentials disabled unless a separately approved job demonstrably requires them.
4. Do not expose production secrets to pull-request workflows.
5. Do not grant package publishing, repository write, deployment, OIDC token, or attestation permissions to ordinary quality jobs.
6. Review action updates as dependency changes: verify upstream repository, release tag/commit correspondence, maintainer history, permissions, and diff before changing the pin.
7. Inspect workflow triggers, fork/PR behavior, reusable workflows, and transitive actions before increasing permissions.
8. Branch protection, CODEOWNERS, required reviews, runner isolation, and administrator bypass policy require separate verification.

Current status: **PARTIAL PASS** — the inspected workflow is read-only and its two actions are full-SHA pinned; repository-level controls and runner isolation are UNKNOWN / NOT VERIFIED.

### DEP-05 — Build-artifact provenance and release gate

No artifact is currently built or published by the quality workflow. Before any future package, container, mobile bundle, or deployable artifact is produced or distributed, require a separately approved design that includes:

1. A deterministic artifact subject and cryptographic digest (at minimum SHA-256).
2. Source repository identity and exact source commit SHA.
3. Workflow path/ref, workflow run identifier, builder identity, invocation parameters, and build environment/toolchain.
4. Resolved dependency materials and lockfile digest.
5. An SBOM in a selected, versioned format (for example SPDX or CycloneDX), tied to the artifact digest.
6. Signed provenance/attestation generated by a trusted builder and stored immutably with the artifact.
7. Verification of attestation signature, issuer, subject digest, source repository, source ref, workflow identity, and expected builder before promotion or deployment.
8. A policy preventing deployment of artifacts with missing, invalid, mismatched, or untrusted provenance.
9. Retention, access-control, and incident-response procedures for artifacts and attestations.

Grant `id-token: write` and `attestations: write` only to a dedicated, narrowly scoped attestation job after an explicit security design and Owner approval. Never add those permissions to the general quality job. Do not introduce artifact generation, upload, signing, or deployment in this increment.

Current status: **NOT IMPLEMENTED**. No artifact provenance or SBOM claim is made.

## 4. Regression guard added in this increment

A static test module, `tests/test_supply_chain_baseline.py`, is intended to protect these present-tense invariants:

- every lock entry is exactly pinned and contains valid SHA-256 digest syntax;
- direct runtime/development pins are represented at the same versions in the lock;
- runtime dependencies remain Django-only;
- CI workflow and job permissions remain read-only;
- GitHub Actions references remain full 40-character commit SHAs;
- checkout credentials remain disabled;
- CI uses hash-checked installation and runs `pip-audit`;
- artifact attestation permissions and artifact-upload/provenance steps are not silently introduced.

These are static configuration checks, not proof that an upstream publisher is authentic, a package is non-malicious, a runner is uncompromised, or a future artifact is reproducible. Any deliberate change to these invariants requires an explicit scope review and corresponding test update.

## 5. Acceptance criteria

- [ ] No runtime dependency, package version, application behavior, schema, route, or deployment setting changes.
- [ ] Lockfile remains unchanged and all current direct pins match it.
- [ ] CI permission model remains read-only.
- [ ] All third-party actions in the quality workflow remain full-SHA pinned.
- [ ] Checkout credentials remain disabled.
- [ ] Hash-checked installation and vulnerability audit remain mandatory.
- [ ] Static supply-chain regression tests pass on the exact A3 head.
- [ ] No artifact publication, signing, attestation, SBOM upload, or deployment is enabled.
- [ ] Changed-file inventory is limited to this baseline, its static test, and the workflow required-file gate.
- [ ] A4 independently verifies the exact head, test quality, and unchanged runtime dependency/application surface.

## 6. Open risks and explicit limitations

- PyPI/source provenance is not independently attested or enforced by an explicit index configuration.
- Hashes protect artifact integrity relative to the committed lock, not the trustworthiness of the original digest source.
- No automated dependency update bot or advisory intake/triage register is configured.
- No formal Owner-approved vulnerability remediation SLA or exception process exists.
- No repository branch-protection/CODEOWNERS/required-review configuration has been verified.
- Runner image, isolation, cache trust, network egress, and administrative bypass are not independently assessed.
- No SBOM, build artifact, signed provenance, or attestation exists in this increment.
- No external supply-chain security review or penetration test has been performed.

## 7. Disposition

- Dependency declaration: **PARTIAL**.
- Lock integrity: **BASELINE PRESENT; REGRESSION GUARDS ADDED**.
- Vulnerability scanning: **PRESENT; governance workflow PARTIAL**.
- CI permissions/action pinning: **PARTIAL PASS**.
- Build-artifact provenance: **NOT IMPLEMENTED**.
- Runtime dependency changes: **NONE**.
- Application behavior/configuration changes: **NONE**.
- Merge/deployment/signing/publication: **NOT AUTHORIZED / NOT PERFORMED**.

**Conclusion:** this increment establishes a bounded, testable dependency and CI supply-chain baseline without adding runtime dependencies or changing application behavior. It deliberately does not claim complete package provenance or build-artifact assurance. Artifact attestation remains a future, separately authorized release capability.
