#!/usr/bin/env python3
"""Validate the human HLD contract and machine evidence consistency."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from shutil import which

VALID_PROFILES = {"small", "medium", "large"}


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(name)}\s*:\s*[\"']?([^\"'\n#]+)", text, re.I | re.M)
    return match.group(1).strip().lower() if match else None


def mermaid_blocks(text: str) -> list[str]:
    return re.findall(r"```mermaid\s*\n(.*?)```", text, re.I | re.S)


def validate_mermaid(blocks: list[str]) -> None:
    mmdc = which("mmdc")
    skip_render = os.environ.get("AI_SDLC_SKIP_MERMAID_RENDER", "").lower() in {
        "1",
        "true",
        "yes",
    }
    if skip_render and mmdc:
        print(
            "Mermaid browser rendering skipped; structural Mermaid checks remain enabled.",
            file=sys.stderr,
        )
    for index, block in enumerate(blocks, 1):
        if "<br" in block.lower():
            raise ValueError(f"Mermaid diagram {index} uses HTML; use portable Mermaid labels")
        first = next((line.strip().lower() for line in block.splitlines() if line.strip()), "")
        if not first.startswith(("flowchart", "graph", "sequencediagram", "classdiagram", "statediagram", "erdiagram", "journey", "gantt", "pie", "mindmap", "timeline")):
            raise ValueError(f"Mermaid diagram {index} has unsupported or missing diagram declaration")

        if mmdc and not skip_render:
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "diagram.mmd"
                output = Path(directory) / "diagram.svg"
                source.write_text(block, encoding="utf-8")
                result = subprocess.run([mmdc, "-i", str(source), "-o", str(output), "-q"], capture_output=True, text=True)
                if result.returncode:
                    raise ValueError(f"Mermaid diagram {index} failed to render: {result.stderr.strip()}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_hld_artifacts.py <initiative-directory>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    hld = target / "hld" / "hld.md"
    assessment = target / "evidence" / "hld-assessment.yaml"
    loop = target / "evidence" / "hld-loop.yaml"
    if not hld.exists():
        print(f"Missing HLD: {hld}", file=sys.stderr)
        return 1

    hld_text = hld.read_text(encoding="utf-8")
    profile = field(hld_text, "change_size")
    if profile not in VALID_PROFILES:
        print("HLD change_size must be small, medium, or large", file=sys.stderr)
        return 1
    if assessment.exists():
        assessment_text = assessment.read_text(encoding="utf-8")
        assessed = field(assessment_text, "recommended_profile")
        if assessed != profile:
            print(f"HLD profile mismatch: assessment={assessed}, HLD={profile}", file=sys.stderr)
            return 1
    if loop.exists():
        loop_profile = field(loop.read_text(encoding="utf-8"), "profile")
        if loop_profile and loop_profile != profile:
            print(f"HLD loop profile mismatch: loop={loop_profile}, HLD={profile}", file=sys.stderr)
            return 1

    headings = re.findall(r"^##\s+(.+)$", hld_text, re.M)
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    if duplicates:
        print(f"Duplicate HLD section headings: {', '.join(duplicates)}", file=sys.stderr)
        return 1
    gap_headings = [heading for heading in headings if "context" in heading.lower() and "gap" in heading.lower()]
    if len(gap_headings) != 1:
        print("HLD must contain exactly one canonical context-gap register", file=sys.stderr)
        return 1
    risk_headings = [heading for heading in headings if "risk" in heading.lower()]
    if len(risk_headings) != 1:
        print("HLD must contain exactly one canonical risk register", file=sys.stderr)
        return 1

    try:
        validate_mermaid(mermaid_blocks(hld_text))
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    print(f"HLD artifact validation passed: profile={profile}, diagrams={len(mermaid_blocks(hld_text))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
