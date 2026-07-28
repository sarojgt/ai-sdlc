#!/usr/bin/env python3
"""Create design artifacts only when their lifecycle stage begins."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DESIGN_READMES = {
    "hld": """# High-Level Design

Create and review this content only after the requirement is approved and the
relevant context has been assembled. Architecture approval is recorded only by
a human Solution Architect or ARB.
""",
    "lld": """# Engineering Design

Create this content only after the HLD approval gate has passed. The LLD may
contain detailed APIs, schemas, classes, implementation sequencing, testing,
migration, and observability design.
""",
}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def values(initiative_dir: Path) -> dict[str, str]:
    initiative_yaml = initiative_dir / "initiative.yaml"
    requirement = initiative_dir / "requirement.md"
    text = initiative_yaml.read_text() if initiative_yaml.exists() else requirement.read_text()
    result: dict[str, str] = {}
    for key, pattern in {
        "id": r'^\s+(?:initiative|id):\s*"([^"]+)"\s*$',
        "title": r'^\s+title:\s*"([^"]*)"\s*$',
    }.items():
        match = re.search(pattern, text, flags=re.MULTILINE)
        if match:
            result[key] = match.group(1)
    return result


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[2] not in DESIGN_READMES:
        fail("Usage: initialize_design_artifacts.py <initiative-dir> <hld|lld>")

    initiative_dir = Path(sys.argv[1]).resolve()
    artifact = sys.argv[2]
    if not initiative_dir.is_dir():
        fail(f"Initiative directory not found: {initiative_dir}")

    template = initiative_dir.parent.parent / "templates" / "initiative" / artifact / f"{artifact}.md"
    if not template.exists():
        fail(f"Design template not found: {template}")

    data = values(initiative_dir)
    target_dir = initiative_dir / artifact
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{artifact}.md"
    if not target.exists():
        text = template.read_text()
        text = text.replace("{{ initiative.id }}", data.get("id", initiative_dir.name))
        text = text.replace("{{ initiative.title }}", data.get("title", "Untitled initiative"))
        target.write_text(text)

    readme = target_dir / "README.md"
    if not readme.exists():
        readme.write_text(DESIGN_READMES[artifact])

    print(f"Initialized {artifact.upper()} artifacts for {initiative_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
