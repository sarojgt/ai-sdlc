#!/usr/bin/env python3
"""Validate the requirement/context/design provenance chain for an HLD."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*\n(.*?)(?=^[A-Za-z0-9_-]+:\s|\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def scalar(text: str, key: str, indent: str = "") -> str:
    match = re.search(rf"^{re.escape(indent)}{re.escape(key)}:\s*[\"']?([^\"'\n#]+)", text, re.M)
    return match.group(1).strip() if match else ""


def normalize(value: str) -> str:
    return value.strip().strip('"\'').lower()


def validate_consistency(target: Path) -> None:
    requirement = target / "requirement.md"
    manifest = target / "context-manifest.yaml"
    assessment_path = target / "evidence" / "hld-assessment.yaml"
    loop_path = target / "evidence" / "hld-loop.yaml"
    baseline_path = target / "evidence" / "design-baseline.yaml"
    for path in (requirement, manifest, assessment_path, loop_path, baseline_path):
        if not path.is_file():
            raise ValueError(f"Missing HLD provenance file: {path}")

    assessment = assessment_path.read_text(encoding="utf-8")
    loop = loop_path.read_text(encoding="utf-8")
    baseline = baseline_path.read_text(encoding="utf-8")
    manifest_text = manifest.read_text(encoding="utf-8")
    expected_requirement = digest(requirement)
    expected_manifest = digest(manifest)

    baseline_requirement = scalar(section(baseline, "requirement"), "content_sha256", "  ")
    baseline_manifest = scalar(section(baseline, "context"), "manifest_sha256", "  ")
    assessment_requirement = scalar(assessment, "requirement_sha256")
    assessment_manifest = scalar(assessment, "context_manifest_sha256")
    loop_requirement = scalar(loop, "requirement_sha256", "  ")
    loop_manifest = scalar(loop, "context_manifest_sha256", "  ")
    comparisons = {
        "design baseline requirement hash": (baseline_requirement, expected_requirement),
        "assessment requirement hash": (assessment_requirement, expected_requirement),
        "loop requirement hash": (loop_requirement, expected_requirement),
        "design baseline context hash": (baseline_manifest, expected_manifest),
        "assessment context hash": (assessment_manifest, expected_manifest),
        "loop context hash": (loop_manifest, expected_manifest),
    }
    for label, (actual, expected) in comparisons.items():
        if not actual or actual != expected:
            raise ValueError(f"HLD provenance mismatch: {label}={actual or '<missing>'}, expected {expected}")

    initiative_id = target.name
    if normalize(scalar(baseline, "id", "  ")) != normalize(initiative_id):
        raise ValueError("HLD provenance mismatch: design baseline initiative id")
    if normalize(scalar(manifest_text, "initiative")) != normalize(initiative_id):
        raise ValueError("HLD provenance mismatch: context manifest initiative id")
    context_pack = section(manifest_text, "context_pack")
    if not scalar(context_pack, "content_sha256", "  "):
        raise ValueError("HLD provenance mismatch: context manifest content hash is missing")

    loop_status = normalize(scalar(loop, "status", "  "))
    decision = normalize(scalar(loop, "latest_decision", "  "))
    review_file = scalar(loop, "latest_review_file", "  ")
    if loop_status == "ai_review_passed" and decision not in {"pass", "ready_for_human_review"}:
        raise ValueError("HLD loop cannot be ai_review_passed unless the latest review passed")
    if loop_status == "changes_requested" and decision != "changes_requested":
        raise ValueError("HLD loop changes_requested status must reference a changes_requested review")
    if review_file:
        review_path = target / review_file.strip('"\'')
        if not review_path.is_file():
            raise ValueError(f"HLD loop latest review file does not exist: {review_file}")
        review_text = review_path.read_text(encoding="utf-8")
        review_decision = normalize(scalar(review_text, "decision"))
        if decision and review_decision != decision:
            raise ValueError(
                f"HLD loop latest decision={decision} disagrees with {review_file} decision={review_decision}"
            )
