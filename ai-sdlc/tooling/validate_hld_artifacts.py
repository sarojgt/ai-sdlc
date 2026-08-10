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
CORE_HEADING_ALTERNATIVES = {
    "problem or motivation": ("motivation", "problem", "outcome"),
    "solution or recommendation": ("solution overview", "recommendation"),
    "solution design": ("solution design",),
    "risks": ("risks",),
}
PLACEHOLDER_PATTERNS = (
    r"\bTBD\b",
    r"\bTODO\b",
    r"<(?:insert|replace|describe|name|value)[^>]*>",
    r"small\s*/\s*medium\s*/\s*large",
)


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(name)}\s*:\s*[\"']?([^\"'\n#]+)", text, re.I | re.M)
    return match.group(1).strip().lower() if match else None


def mermaid_blocks(text: str) -> list[str]:
    return re.findall(r"```mermaid\s*\n(.*?)```", text, re.I | re.S)


def visible_headings(text: str) -> list[str]:
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.findall(r"^##\s+(.+)$", without_comments, re.M)


def normalized_heading(heading: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*[.)]?\s*", "", heading.strip()).lower()


def validate_core_headings(headings: list[str]) -> None:
    normalized = [normalized_heading(heading) for heading in headings]
    missing = [
        label
        for label, alternatives in CORE_HEADING_ALTERNATIVES.items()
        if not any(any(option in heading for option in alternatives) for heading in normalized)
    ]
    if missing:
        raise ValueError(f"HLD is missing mandatory core sections: {', '.join(missing)}")


def sections(text: str) -> list[tuple[int, str, str]]:
    """Return visible sections, including content in their nested subsections."""
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    matches = list(re.finditer(r"^(#{2,4})\s+(.+)$", without_comments, re.M))
    result = []
    for index, match in enumerate(matches):
        level = len(match.group(1))
        end = len(without_comments)
        for candidate in matches[index + 1:]:
            if len(candidate.group(1)) <= level:
                end = candidate.start()
                break
        result.append((level, match.group(2).strip(), without_comments[match.end():end]))
    return result


def has_meaningful_content(body: str) -> bool:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    prose = [
        line for line in lines
        if not line.startswith("|")
        and not line.startswith("#")
        and line not in {"---"}
    ]
    if any(not re.fullmatch(r"[-: ]+", line) for line in prose):
        return True
    table_lines = [line for line in lines if line.startswith("|")]
    separator = next(
        (index for index, line in enumerate(table_lines) if re.fullmatch(r"\|?[|:\- ]+\|?", line)),
        None,
    )
    return separator is not None and len(table_lines) > separator + 1


def validate_core_content(text: str) -> None:
    parsed = sections(text)
    for label, alternatives in CORE_HEADING_ALTERNATIVES.items():
        bodies = [
            body
            for level, heading, body in parsed
            if level == 2
            if any(option in normalized_heading(heading) for option in alternatives)
        ]
        if not bodies or not any(has_meaningful_content(body) for body in bodies):
            raise ValueError(f"HLD mandatory section has no substantive content: {label}")
    for level, heading, body in parsed:
        if level != 2:
            continue
        if any(token in normalized_heading(heading) for token in ("risk", "context gap")):
            if not has_meaningful_content(body):
                raise ValueError(f"HLD register has no substantive content: {heading}")
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, re.sub(r"<!--.*?-->", "", text, flags=re.S), re.I):
            raise ValueError(f"HLD contains unresolved placeholder content matching: {pattern}")


def validate_mermaid(blocks: list[str]) -> None:
    """Run advisory diagram checks without making Mermaid a lifecycle gate."""
    mmdc = which("mmdc")
    parser = Path(__file__).with_name("mermaid") / "validate.mjs"
    node = which("node")
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
            print(f"Warning: Mermaid diagram {index} uses HTML; prefer portable labels", file=sys.stderr)
        first = next((line.strip().lower() for line in block.splitlines() if line.strip()), "")
        if not first.startswith(("flowchart", "graph", "sequencediagram", "classdiagram", "statediagram", "erdiagram", "journey", "gantt", "pie", "mindmap", "timeline")):
            print(f"Warning: Mermaid diagram {index} has an unsupported or missing declaration", file=sys.stderr)

        if mmdc and not skip_render:
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "diagram.mmd"
                output = Path(directory) / "diagram.svg"
                source.write_text(block, encoding="utf-8")
                result = subprocess.run([mmdc, "-i", str(source), "-o", str(output), "-q"], capture_output=True, text=True)
                if result.returncode:
                    print(f"Warning: Mermaid diagram {index} failed optional rendering: {result.stderr.strip()}", file=sys.stderr)

    if blocks and node and parser.is_file() and (parser.parent / "node_modules").is_dir():
        hld_file = os.environ.get("AI_SDLC_MERMAID_SOURCE_FILE")
        if hld_file:
            result = subprocess.run([node, str(parser), hld_file], capture_output=True, text=True)
            if result.returncode:
                print(f"Warning: optional Mermaid parser reported issues:\n{result.stdout}{result.stderr}", file=sys.stderr)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_hld_artifacts.py <initiative-directory>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    hld = target / "hld" / "hld.md"
    assessment = target / "evidence" / "hld-assessment.yaml"
    loop = target / "evidence" / "hld-loop.yaml"
    baseline = target / "evidence" / "design-baseline.yaml"
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

    # Any HLD produced by the governed lifecycle must carry one consistent,
    # hashable provenance chain. Legacy examples without lifecycle evidence are
    # left untouched, but a partially-created evidence set is rejected.
    if loop.exists() or baseline.exists() or assessment.exists():
        consistency = target / "evidence" / "hld-assessment.yaml"
        required = (assessment, loop, baseline, target / "context-manifest.yaml", target / "requirement.md")
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            print(f"HLD evidence is incomplete; missing: {', '.join(missing)}", file=sys.stderr)
            return 1
        from validate_hld_consistency import validate_consistency

        try:
            validate_consistency(target)
        except ValueError as error:
            print(str(error), file=sys.stderr)
            return 1

    headings = visible_headings(hld_text)
    try:
        validate_core_headings(headings)
        validate_core_content(hld_text)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    normalized_headings = [normalized_heading(heading) for heading in headings]
    duplicates = sorted({heading for heading in normalized_headings if normalized_headings.count(heading) > 1})
    if duplicates:
        print(f"Duplicate HLD section headings: {', '.join(duplicates)}", file=sys.stderr)
        return 1
    gap_headings = [heading for heading in headings if "context" in normalized_heading(heading) and "gap" in normalized_heading(heading)]
    if len(gap_headings) != 1:
        print("HLD must contain exactly one canonical context-gap register", file=sys.stderr)
        return 1
    risk_headings = [heading for heading in headings if "risk" in normalized_heading(heading)]
    if len(risk_headings) != 1:
        print("HLD must contain exactly one canonical risk register", file=sys.stderr)
        return 1

    try:
        os.environ.setdefault("AI_SDLC_MERMAID_SOURCE_FILE", str(hld))
        validate_mermaid(mermaid_blocks(hld_text))
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    print(f"HLD artifact validation passed: profile={profile}, diagrams={len(mermaid_blocks(hld_text))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
