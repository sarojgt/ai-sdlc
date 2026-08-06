#!/usr/bin/env python3
"""Determine whether an HLD is ready for human review or needs discovery."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def context_gap_section(text: str) -> str:
    match = re.search(r"^##\s+[^\n]*context\s+gaps[^\n]*\n(.*?)(?=^##\s+|\Z)", text, re.I | re.M | re.S)
    return match.group(1) if match else ""


def has_blocking_gap(text: str) -> bool:
    section = context_gap_section(text)
    if not section:
        return False
    for line in section.splitlines():
        if line.lstrip().startswith("|") and re.search(r"\|\s*yes\s*\|", line, re.I):
            if not re.search(r"blocks\s+decision", line, re.I):
                return True
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_hld_readiness.py <initiative-directory>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1]).resolve()
    hld = target / "hld" / "hld.md"
    if not hld.is_file():
        print(f"Missing HLD: {hld}", file=sys.stderr)
        return 1
    if has_blocking_gap(hld.read_text(encoding="utf-8")):
        print("discovery_required")
        print("HLD has unresolved context gaps that block an architectural decision.", file=sys.stderr)
        return 10
    print("ready_for_human_review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
