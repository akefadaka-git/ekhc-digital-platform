"""Static guards for dependency and CI supply-chain invariants."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def normalized_name(value):
    return re.sub(r"[-_.]+", "-", value).lower()


class DependencyLockIntegrityTests(unittest.TestCase):
    def test_every_lock_entry_is_exactly_pinned_and_sha256_hashed(self):
        lock = read_text("requirements-lock.txt")
        entries = [
            line.strip()
            for line in lock.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertGreater(len(entries), 0)

        for entry in entries:
            with self.subTest(entry=entry.split()[0]):
                self.assertRegex(entry, r"^[A-Za-z0-9_.-]+==[^\s]+")
                hashes = re.findall(r"--hash=sha256:([0-9a-f]{64})", entry)
                self.assertGreaterEqual(len(hashes), 1)
                self.assertEqual(len(hashes), len(re.findall(r"--hash=", entry)))

    def test_direct_runtime_and_development_pins_are_present_in_lock(self):
        lock_lines = [
            line.strip()
            for line in read_text("requirements-lock.txt").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        locked = {}
        for line in lock_lines:
            match = re.match(r"^([A-Za-z0-9_.-]+)==([^\s]+)", line)
            self.assertIsNotNone(match, line)
            locked[normalized_name(match.group(1))] = match.group(2)

        for manifest in ("requirements.txt", "requirements-dev.txt"):
            for raw in read_text(manifest).splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or line.startswith("-r "):
                    continue
                self.assertNotRegex(line, r"(https?://|git\+|^-e\s)")
                match = re.match(r"^([A-Za-z0-9_.-]+)==([^\s;]+)$", line)
                self.assertIsNotNone(match, f"{manifest}: {line}")
                name, version = match.groups()
                self.assertEqual(locked.get(normalized_name(name)), version)

    def test_runtime_dependency_set_remains_django_only(self):
        requirements = [
            line.strip()
            for line in read_text("requirements.txt").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(requirements, ["Django==5.2.19"])


class CiSupplyChainBoundaryTests(unittest.TestCase):
    def test_ci_uses_read_only_repository_permissions(self):
        workflow = read_text(".github/workflows/quality.yml")
        self.assertRegex(workflow, r"(?m)^permissions:\s*\n\s+contents:\s+read\s*$")
        self.assertRegex(workflow, r"(?m)^\s{4}permissions:\s*\n\s{6}contents:\s+read\s*$")
        self.assertNotRegex(
            workflow,
            r"(?mi)^\s+(contents|packages|id-token|attestations):\s+write\s*$",
        )

    def test_actions_are_pinned_to_full_commit_shas(self):
        workflow = read_text(".github/workflows/quality.yml")
        action_refs = re.findall(r"(?m)^\s+uses:\s+[^@\s]+@([^\s#]+)", workflow)
        self.assertGreaterEqual(len(action_refs), 2)
        for ref in action_refs:
            with self.subTest(ref=ref):
                self.assertRegex(ref, r"^[0-9a-f]{40}$")

    def test_checkout_does_not_persist_repository_credentials(self):
        workflow = read_text(".github/workflows/quality.yml")
        self.assertRegex(workflow, r"(?m)^\s+persist-credentials:\s+false\s*$")

    def test_ci_installs_only_from_hash_locked_manifest_and_audits_it(self):
        workflow = read_text(".github/workflows/quality.yml")
        self.assertIn("pip install --require-hashes -r requirements-lock.txt", workflow)
        self.assertIn("pip-audit -r requirements-lock.txt", workflow)

    def test_artifact_attestation_is_not_claimed_or_enabled(self):
        workflow = read_text(".github/workflows/quality.yml")
        self.assertNotRegex(
            workflow,
            r"(?mi)^\s+(id-token|attestations):\s+write\s*$",
        )
        self.assertNotRegex(
            workflow,
            r"(?mi)^\s+uses:\s+actions/(upload-artifact|attest-build-provenance)@",
        )


if __name__ == "__main__":
    unittest.main()
