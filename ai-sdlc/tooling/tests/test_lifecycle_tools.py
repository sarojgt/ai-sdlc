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
from validate_hld_artifacts import (  # noqa: E402
    validate_core_content,
    validate_core_headings,
    visible_headings,
)


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

    def test_feedback_batch_accepts_explicit_pull_request_comment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            initiative = root / "TEST-INITIATIVE"
            (initiative / "hld").mkdir(parents=True)
            (initiative / "hld" / "hld.md").write_text("# HLD\n", encoding="utf-8")
            body = root / "comment.md"
            comments = root / "comments.json"
            body.write_text("/ai-sdlc revise-hld Please clarify the migration risk.\n", encoding="utf-8")
            comments.write_text(json.dumps([{
                "body": body.read_text(encoding="utf-8"),
                "html_url": "https://github.com/example/review",
            }]), encoding="utf-8")
            result = self.run_tool(
                str(TOOLING / "create_feedback_batch.py"), str(initiative), "--review-id", "comment-7",
                "--reviewer", "architect", "--review-commit", "abc", "--review-body-file", str(body),
                "--comments-file", str(comments),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            batch = initiative / "feedback" / "batches" / "review-comment-7.md"
            self.assertIn("migration risk", batch.read_text(encoding="utf-8"))

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

    def test_context_pack_records_selected_sections_and_advisory_budget(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = Path(directory) / "TEST-INITIATIVE"
            relative = initiative / "context" / "relative"
            relative.mkdir(parents=True)
            (initiative / "requirement.md").write_text(
                "# API requirement\n\nAdd an authenticated portal API with observability.\n",
                encoding="utf-8",
            )
            (relative / "api.md").write_text(
                "# Existing API\n\nCurrent route.\n\n## HLD implications\n\nReuse the gateway.\n",
                encoding="utf-8",
            )
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative), "--explain")
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = (initiative / "context-manifest.yaml").read_text(encoding="utf-8")
            pack = (initiative / "evidence" / "context-pack.md").read_text(encoding="utf-8")
            self.assertIn("selection_policy_version", manifest)
            self.assertIn("advisory_token_budget", manifest)
            self.assertIn("selected_sections", manifest)
            self.assertIn("Existing API", pack)
            self.assertIn("explicit initiative context", result.stdout)

    def test_context_budget_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = Path(directory) / "TEST-INITIATIVE"
            relative = initiative / "context" / "relative"
            relative.mkdir(parents=True)
            (initiative / "requirement.md").write_text("# API\n\n" + ("important context " * 5000), encoding="utf-8")
            (relative / "large.md").write_text("# Large context\n\n" + ("detail " * 20000), encoding="utf-8")
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("continuing without blocking", result.stdout)

    def test_context_selection_ignores_generic_repository_path_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            initiative = Path(directory) / "TEST-INITIATIVE"
            relative = initiative / "context" / "relative"
            relative.mkdir(parents=True)
            (initiative / "requirement.md").write_text("# Unrelated capability\n\nA unique ledger capability.\n", encoding="utf-8")
            (relative / "ledger.md").write_text("# Ledger\n\nThe current ledger owner.\n", encoding="utf-8")
            result = self.run_tool(str(TOOLING / "build_context_pack.py"), str(initiative), "--explain")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("enterprise-architecture", result.stdout)
            self.assertNotIn("portal-atlas", result.stdout)

    def test_context_catalog_covers_configured_sources(self) -> None:
        result = self.run_tool(str(TOOLING / "validate_context_catalog.py"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sources indexed", result.stdout)

    def test_context_catalog_sync_appends_only_missing_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "ai-sdlc" / "config"
            source = root / "ai-sdlc" / "context" / "new.md"
            config.mkdir(parents=True)
            source.parent.mkdir(parents=True)
            source.write_text("# New Context\n\n## HLD implications\n\nUse this context.\n", encoding="utf-8")
            (config / "context-sources.yaml").write_text(
                "context_sources:\n"
                "  - id: new-context\n"
                "    class: enterprise\n"
                "    source: \"ai-sdlc/context/new.md\"\n"
                "    authority: architecture\n"
                "    freshness: 90d\n",
                encoding="utf-8",
            )
            (config / "context-index.yaml").write_text(
                "context_index:\n  version: \"1\"\n  entries:\n",
                encoding="utf-8",
            )
            check = self.run_tool(str(TOOLING / "sync_context_catalog.py"), "--root", str(root))
            self.assertEqual(check.returncode, 1)
            update = self.run_tool(str(TOOLING / "sync_context_catalog.py"), "--root", str(root), "--update")
            self.assertEqual(update.returncode, 0, update.stderr)
            updated = (config / "context-index.yaml").read_text(encoding="utf-8")
            self.assertIn("id: new-context", updated)
            again = self.run_tool(str(TOOLING / "sync_context_catalog.py"), "--root", str(root), "--update")
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(updated, (config / "context-index.yaml").read_text(encoding="utf-8"))

    def test_context_catalog_sync_discovers_markdown_after_merge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "ai-sdlc" / "config"
            context = root / "ai-sdlc" / "context" / "consistent" / "product" / "services"
            config.mkdir(parents=True)
            context.mkdir(parents=True)
            (context / "new-service.md").write_text(
                "---\ncontext_id: service-new\nauthority: service-owner\n"
                "context_type: consistent\nstatus: imported-snapshot\n"
                "owner: service-team\nreview_cadence: 90d\n---\n"
                "# New Service\n\n## HLD implications\nUse this service.\n",
                encoding="utf-8",
            )
            (config / "context-sources.yaml").write_text("context_sources:\n", encoding="utf-8")
            (config / "context-index.yaml").write_text("context_index:\n  version: \"1\"\n  entries:\n", encoding="utf-8")
            update = self.run_tool(str(TOOLING / "sync_context_catalog.py"), "--root", str(root), "--update")
            self.assertEqual(update.returncode, 0, update.stderr)
            registry = (config / "context-sources.yaml").read_text(encoding="utf-8")
            catalog = (config / "context-index.yaml").read_text(encoding="utf-8")
            self.assertIn("id: service-new", registry)
            self.assertIn("id: service-new", catalog)

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

    def test_prompt_profiles_are_rendered_from_authoritative_config(self) -> None:
        result = self.run_tool(
            str(TOOLING / "render_prompt.py"), "--name", "hld-generation",
            "--initiative-id", "TEST-INITIATIVE", "--profile", "small",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Omit Pending Items from ARB, Traceability", result.stdout)
        self.assertIn("A concise architecture decision record", result.stdout)
        self.assertIn("Usually none", result.stdout)
        self.assertNotIn("{{", result.stdout)

    def test_assessment_rubric_is_rendered_from_profiles(self) -> None:
        result = self.run_tool(
            str(TOOLING / "render_prompt.py"), "--name", "hld-assessment",
            "--initiative-id", "TEST-INITIATIVE", "--profile", "auto",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("One bounded capability or service", result.stdout)
        self.assertIn("Multiple components or one material boundary", result.stdout)
        self.assertIn("new architectural boundary", result.stdout)
        self.assertNotIn("{{", result.stdout)

    def test_review_prompt_omits_invalid_none_condition(self) -> None:
        result = self.run_tool(
            str(TOOLING / "render_prompt.py"), "--name", "hld-review",
            "--initiative-id", "TEST-INITIATIVE", "--profile", "small",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("There is no submitted feedback batch", result.stdout)
        self.assertNotIn("If `None`", result.stdout)

    def test_revision_prompt_preserves_unaffected_sections(self) -> None:
        result = self.run_tool(
            str(TOOLING / "render_prompt.py"), "--name", "hld-generation",
            "--initiative-id", "TEST-INITIATIVE", "--profile", "medium",
            "--mode", "revision", "--feedback-file", "feedback/batches/review-1.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("preserve unaffected approved content", result.stdout)
        self.assertIn("feedback/batches/review-1.md", result.stdout)

    def test_hld_core_accepts_numbered_headings_with_content(self) -> None:
        hld = """## 1. Motivation
Needed outcome.
## 2. Solution Overview
Use the existing service.
## 3. Solution Design
The existing API owns the change.
## 4. Risks
No material initiative-specific risks are known.
## 5. Context Gaps
No decision-blocking context gaps are known.
"""
        headings = visible_headings(hld)
        validate_core_headings(headings)
        validate_core_content(hld)

    def test_hld_core_rejects_empty_template_registers(self) -> None:
        hld = """## Motivation
Needed outcome.
## Solution Overview
Use the existing service.
## Solution Design
The existing API owns the change.
## Risks
| ID | Risk |
|---|---|
## Context Gaps
| ID | Gap |
|---|---|
"""
        with self.assertRaisesRegex(ValueError, "no substantive content"):
            validate_core_content(hld)

    def test_solution_design_content_may_live_in_selected_subsection(self) -> None:
        hld = """## Motivation
Needed outcome.
## Solution Overview
Use the existing service.
## Solution Design
### API and Integration Design
The existing API owns the change.
## Risks
No material initiative-specific risks are known.
## Context Gaps
No decision-blocking context gaps are known.
"""
        validate_core_content(hld)

    def test_review_artifact_names_are_not_reused_by_a_new_run(self) -> None:
        loop = (TOOLING / "hld_loop.sh").read_text(encoding="utf-8")
        self.assertIn('export AI_SDLC_HLD_REVIEW_FILE="$review_file_relative"', loop)
        self.assertIn('if [ -e "$target/$review_file_relative" ]; then', loop)
        self.assertIn('ai-review-iteration-$iteration-run-$started_at.md', loop)


if __name__ == "__main__":
    unittest.main()
