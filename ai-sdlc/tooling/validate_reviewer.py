#!/usr/bin/env python3
"""Validate a reviewer against the repository's explicit POC allowlist."""

from __future__ import annotations

import re
import sys
import os
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_reviewer.py <role> <github-login>", file=sys.stderr)
        return 2
    role, login = sys.argv[1:]
    policy = Path(os.environ.get("AI_SDLC_GOVERNANCE_FILE", Path(__file__).resolve().parents[1] / "config" / "github-governance.yaml"))
    text = policy.read_text(encoding="utf-8")
    section = re.search(rf"(?ms)^  {re.escape(role)}:\s*$\n(.*?)(?=^  \w|\Z)", text)
    allowed = set(re.findall(r"^    -\s+([A-Za-z0-9-]+)\s*$", section.group(1) if section else ""))
    if login in allowed:
        return 0
    print(f"Reviewer `{login}` is not permitted for role `{role}` by {policy.name}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
