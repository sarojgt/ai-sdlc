from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLING = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLING))
from context_versions import package_for  # noqa: E402
from release_context_notes import main as render_context_notes  # noqa: E402
from validate_hld_consistency import validate_consistency  # noqa: E402
from validate_hld_readiness import has_blocking_gap  # noqa: E402


class LifecycleToolTests(unittest.TestCase):
    def initiative(self, root: Path) -> Path:
        initiative = root / "TEST-INITIATIVE"
        (initiative / "context" / "relative").mkdir(parents=True)
        (initiative / "requirement.md").write_text(
            "---\nartifact:\n  status: approved\n---\n# Requirement\n", encoding="utf-8"
        )
        digest = hashlib.sha256()
        digest.update(b"requirement.md\0")
        digest.update((initiative / "requirement.md").read_bytes())
        (initiative / "approvals.yaml").write_text(
            "records:\n"
            "  - gate: requirements\n"
            "    decision: approved\n"
            "    principal: \"architect\"\n"
            f"    content_sha256: \"{digest.hexdigest()}\"\n"
            "    review_commit: \"abc\"\n",
            encoding="utf-8",
        )
        return initiative

    def run_tool(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, *args], text=True, capture_output=True, check=False, env=env)

    def test_requirement_gate_requires_matching_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = self.initiative(Path(directory))
            result = self.run_tool(str(TOOLING / "approval_gate.py"), "requirements", str(initiative))
            self.assertEqual(result.returncode, 0, result.stderr)
            (initiative / "requirement.md").write_text("---\nartifact:\n  status: approved\n---\n# Changed\n", encoding="utf-8")
            result = self.run_tool(str(TOOLING / "approval_gate.py"), "requirements", str(initiative))
            self.assertEqual(result.returncode, 10)
            self.assertIn("content hash", result.stderr)

    def test_feedback_batch_preserves_submitted_review_comments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initiative = root / "TEST-INITIATIVE"
            (initiative / "hld").mkdir(parents=True)
            (initiative / "hld" / "hld.md").write_text("# HLD\n", encoding="utf-8")
            body = root / "review.md"
            comments = root / "comments.json"
            body.write_text("Please address the API contract.\n", encoding="utf-8")
            comments.write_text(json.dumps([{"path": f"ai-sdlc/initiatives/{initiative.name}/hld/hld.md", "line": 12, "body": "Clarify pagination."}]), encoding="utf-8")
            result = self.run_tool(
                str(TOOLING / "create_feedback_batch.py"), str(initiative), "--review-id", "42",
                "--reviewer", "architect", "--review-commit", "abc", "--review-body-file", str(body),
                "--comments-file", str(comments),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            batch = initiative / "feedback" / "batches" / "review-42.md"
            self.assertIn("Please address", batch.read_text(encoding="utf-8"))
            self.assertIn("Clarify pagination", batch.read_text(encoding="utf-8"))

    def test_hld_gate_requires_matching_approved_hld(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = self.initiative(Path(directory))
            hld = initiative / "hld" / "hld.md"
            hld.parent.mkdir()
            hld.write_text("---\nartifact:\n  status: approved\n---\n# HLD\n", encoding="utf-8")
            digest = hashlib.sha256(hld.read_bytes()).hexdigest()
            (initiative / "approvals.yaml").write_text(
                (initiative / "approvals.yaml").read_text(encoding="utf-8")
                + "  - gate: hld\n"
                + "    decision: approved\n"
                + "    principal: \"architect\"\n"
                + f"    content_sha256: \"{digest}\"\n"
                + "    review_commit: \"def\"\n",
                encoding="utf-8",
            )
            result = self.run_tool(str(TOOLING / "approval_gate.py"), "hld", str(initiative))
            self.assertEqual(result.returncode, 0, result.stderr)
            hld.write_text("---\nartifact:\n  status: approved\n---\n# Changed HLD\n", encoding="utf-8")
            result = self.run_tool(str(TOOLING / "approval_gate.py"), "hld", str(initiative))
            self.assertEqual(result.returncode, 10)
            self.assertIn("content hash", result.stderr)

    def test_review_validator_requires_front_matter_and_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            review = Path(directory) / "ai-review.md"
            review.write_text(
                "---\nreviewer: codex\nmodel: review\niteration: 1\ndecision: ready_for_human_review\n---\n\n"
                "## Findings\nNone.\n\n## Required actions\nNone.\n\n## Validation\n- Valid.\n",
                encoding="utf-8",
            )
            result = self.run_tool(str(TOOLING / "validate_ai_review.py"), str(review))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_context_pack_is_deterministic_and_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = Path(directory) / "TEST-INITIATIVE"
            relative = initiative / "context" / "relative"
            relative.mkdir(parents=True)
            (initiative / "requirement.md").write_text("# Secure card API\n", encoding="utf-8")
            (relative / "api.md").write_text("# Existing contract\n", encoding="utf-8")
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative))
            self.assertEqual(result.returncode, 0, result.stderr)
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative), "--check")
            self.assertEqual(result.returncode, 0, result.stderr)
            (relative / "api.md").write_text("# Changed contract\n", encoding="utf-8")
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative), "--check")
            self.assertEqual(result.returncode, 1)

    def test_reviewer_allowlist_rejects_untrusted_login(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / "governance.yaml"
            policy.write_text("github_reviewers:\n  solution_architect:\n    - test-architect\n", encoding="utf-8")
            environment = {**os.environ, "AI_SDLC_GOVERNANCE_FILE": str(policy)}
            allowed = self.run_tool(str(TOOLING / "validate_reviewer.py"), "solution_architect", "test-architect", env=environment)
            denied = self.run_tool(str(TOOLING / "validate_reviewer.py"), "solution_architect", "untrusted", env=environment)
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(denied.returncode, 1)

    def test_context_paths_map_to_stable_version_packages(self) -> None:
        self.assertEqual(package_for("ai-sdlc/context/consistent/architecture/api-standards.md"), "architecture")
        self.assertEqual(package_for("ai-sdlc/context/guardrails/security/secure-logging.md"), "security")
        self.assertEqual(package_for("ai-sdlc/context/consistent/technology/tech-radar.md"), "technology")

    def test_context_release_notes_renderer_is_available(self) -> None:
        self.assertEqual(render_context_notes(), 0)

    def test_hld_readiness_detects_blocking_context_gaps(self) -> None:
        hld = """## Context gaps

| Gap ID | Missing fact | Blocks decision? |
|---|---|---|
| GAP-001 | Service owner | Yes |
"""
        self.assertTrue(has_blocking_gap(hld))
        self.assertFalse(has_blocking_gap(hld.replace("| Yes |", "| No |")))

    def test_hld_provenance_chain_is_consistent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "TEST-INITIATIVE"
            (target / "evidence").mkdir(parents=True)
            (target / "hld").mkdir()
            (target / "requirement.md").write_text("# Requirement\n", encoding="utf-8")
            (target / "context-manifest.yaml").write_text(
                'initiative: "TEST-INITIATIVE"\ncontext_pack:\n  content_sha256: "pack"\n',
                encoding="utf-8",
            )
            requirement_hash = hashlib.sha256((target / "requirement.md").read_bytes()).hexdigest()
            manifest_hash = hashlib.sha256((target / "context-manifest.yaml").read_bytes()).hexdigest()
            (target / "evidence" / "hld-assessment.yaml").write_text(
                f'recommended_profile: "medium"\nrequirement_sha256: "{requirement_hash}"\n'
                f'context_manifest_sha256: "{manifest_hash}"\n', encoding="utf-8"
            )
            (target / "evidence" / "design-baseline.yaml").write_text(
                'initiative:\n  id: "TEST-INITIATIVE"\n'
                f'requirement:\n  content_sha256: "{requirement_hash}"\n'
                f'context:\n  manifest_sha256: "{manifest_hash}"\n', encoding="utf-8"
            )
            (target / "evidence" / "hld-loop.yaml").write_text(
                'hld_loop:\n  status: running\n  profile: "medium"\n'
                f'  requirement_sha256: "{requirement_hash}"\n'
                f'  context_manifest_sha256: "{manifest_hash}"\n', encoding="utf-8"
            )
            validate_consistency(target)


if __name__ == "__main__":
    unittest.main()
