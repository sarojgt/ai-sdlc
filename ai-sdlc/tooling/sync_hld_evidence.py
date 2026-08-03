#!/usr/bin/env python3
"""Synchronize deterministic provenance into HLD assessment evidence."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_top_level(text: str, key: str, value: str) -> str:
    line = f'{key}: "{value}"'
    pattern = rf"^{re.escape(key)}:.*$"
    updated, count = re.subn(pattern, line, text, count=1, flags=re.MULTILINE)
    if count:
        return updated
    lines = text.splitlines()
    insert_at = 0
    for index, current in enumerate(lines):
        if current.startswith("---"):
            insert_at = index + 1
            continue
        if current and not current.startswith((" ", "\t")):
            insert_at = index
            break
    lines.insert(insert_at, line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: sync_hld_evidence.py <initiative-directory>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1]).resolve()
    requirement = target / "requirement.md"
    manifest = target / "context-manifest.yaml"
    assessment = target / "evidence" / "hld-assessment.yaml"
    for path in (requirement, manifest, assessment):
        if not path.is_file():
            print(f"Missing HLD provenance file: {path}", file=sys.stderr)
            return 1

    text = assessment.read_text(encoding="utf-8")
    text = set_top_level(text, "requirement_sha256", digest(requirement))
    text = set_top_level(text, "context_manifest_sha256", digest(manifest))
    assessment.write_text(text, encoding="utf-8")
    print(f"Synchronized HLD evidence provenance for {target.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
