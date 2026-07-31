#!/usr/bin/env python3
"""Validate the machine-readable decision contract of an AI HLD review."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DECISIONS = {"ready_for_human_review", "changes_requested", "escalate"}


def field(text: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}:\s*([^\n#]+)", text, re.M)
    return match.group(1).strip().strip('"\'') if match else ""


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_ai_review.py <review-file>", file=sys.stderr)
        return 2
    review = Path(sys.argv[1])
    text = review.read_text(encoding="utf-8") if review.is_file() else ""
    front_matter = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    if not front_matter:
        print("AI review must begin with YAML front matter", file=sys.stderr)
        return 1
    metadata = front_matter.group(1)
    missing = [name for name in ("reviewer", "model", "iteration", "decision") if not field(metadata, name)]
    if missing:
        print(f"AI review missing front-matter fields: {', '.join(missing)}", file=sys.stderr)
        return 1
    if field(metadata, "decision") not in DECISIONS:
        print("AI review has an unsupported decision", file=sys.stderr)
        return 1
    for heading in ("Findings", "Required actions", "Validation"):
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.M):
            print(f"AI review missing section: {heading}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
