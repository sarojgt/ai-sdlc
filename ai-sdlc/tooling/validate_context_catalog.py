#!/usr/bin/env python3
"""Validate that every configured context source has catalog metadata."""

from __future__ import annotations

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_context_pack import sources  # noqa: E402
from context_selection import parse_index  # noqa: E402


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = root / "config" / "context-sources.yaml"
    index = root / "config" / "context-index.yaml"
    source_ids = {entry["id"] for entry in sources(registry)}
    _, _, entries = parse_index(index)
    index_ids = set(entries)
    missing = sorted(source_ids - index_ids)
    extra = sorted(index_ids - source_ids)
    if missing or extra:
        if missing:
            print(f"Context catalog is missing metadata for: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"Context catalog contains unknown entries: {', '.join(extra)}", file=sys.stderr)
        return 1
    mismatches = []
    missing_metadata = []
    required_fields = ("context_id", "context_type", "authority", "status", "owner", "review_cadence")
    for entry in sources(registry):
        source = entry.get("source", "")
        path = root.parent / source
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^context_id:\s*([^\n]+)", text, re.MULTILINE)
        if match and match.group(1).strip().strip('"') != entry["id"]:
            mismatches.append(f"{entry['id']} -> {match.group(1).strip()}")
        missing = [field for field in required_fields if not re.search(rf"^{field}:\s*", text, re.MULTILINE)]
        if missing:
            missing_metadata.append(f"{entry['id']} ({', '.join(missing)})")
    if mismatches:
        print(f"Context document IDs do not match the source registry: {', '.join(mismatches)}", file=sys.stderr)
        return 1
    if missing_metadata:
        print(f"Context documents are missing front matter: {', '.join(missing_metadata)}", file=sys.stderr)
        return 1
    print(f"Context catalog is valid: {len(source_ids)} sources indexed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
