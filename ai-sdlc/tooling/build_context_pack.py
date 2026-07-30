#!/usr/bin/env python3
"""Build a deterministic, hashed context manifest from repository context."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

BASELINE_IDS = {"enterprise-architecture", "security-baseline", "api-standards", "arb-governance"}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(path: Path) -> list[dict[str, str]]:
    """Read the intentionally flat source registry without a runtime dependency."""
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        item = re.match(r"^  - id: (.+)$", line)
        field = re.match(r"^    (class|source|authority|freshness): \"?(.*?)\"?$", line)
        if item:
            if current:
                entries.append(current)
            current = {"id": item.group(1)}
        elif field and current is not None:
            current[field.group(1)] = field.group(2)
    if current:
        entries.append(current)
    return entries


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: build_context_pack.py <initiative-dir> [--check]", file=sys.stderr)
        return 2
    initiative = Path(sys.argv[1]).resolve()
    check = len(sys.argv) == 3 and sys.argv[2] == "--check"
    root = Path(__file__).resolve().parents[1]
    requirement = initiative / "requirement.md"
    if not requirement.is_file():
        print(f"Missing requirement: {requirement}", file=sys.stderr)
        return 1
    words = set(re.findall(r"[a-z][a-z0-9-]{3,}", requirement.read_text(encoding="utf-8").lower()))
    items: list[dict[str, str]] = []
    for entry in sources(root / "config" / "context-sources.yaml"):
        source = entry.get("source", "")
        path = root.parent / source
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        matches = len(words.intersection(re.findall(r"[a-z][a-z0-9-]{3,}", text)))
        always = entry.get("id") in BASELINE_IDS
        if always or matches >= 2:
            items.append({**entry, "path": source, "content_sha256": digest(path), "selection": "baseline" if always else f"keyword-match:{matches}"})
    for path in sorted((initiative / "context" / "relative").rglob("*") if (initiative / "context" / "relative").is_dir() else []):
        if path.is_file():
            items.append({"id": f"relative-{path.stem}", "class": "relative", "authority": "initiative-owner", "freshness": "initiative", "path": str(path.relative_to(initiative)), "content_sha256": digest(path), "selection": "explicit-relative-context"})
    combined = hashlib.sha256("\n".join(f"{item['path']}:{item['content_sha256']}" for item in items).encode()).hexdigest()
    output = initiative / "context-manifest.yaml"
    if check:
        existing = output.read_text(encoding="utf-8") if output.exists() else ""
        if f'content_sha256: "{combined}"' not in existing:
            print("Context manifest is missing or stale; run build_context_pack.py", file=sys.stderr)
            return 1
        return 0
    lines = ["das_version: \"0.1\"", f'initiative: {yaml_quote(initiative.name)}', "context_pack:", f'  id: {yaml_quote("CTX-" + initiative.name + "-v1")}', "  version: 1", "  status: assembled", "  items:"]
    for item in items:
        lines.extend([f'    - id: {yaml_quote(item["id"])}', f'      class: {yaml_quote(item["class"])}', f'      path: {yaml_quote(item["path"])}', f'      authority: {yaml_quote(item["authority"])}', f'      freshness: {yaml_quote(item["freshness"])}', f'      selection: {yaml_quote(item["selection"])}', f'      content_sha256: {yaml_quote(item["content_sha256"])}'])
    lines.extend(["  exclusions:", "    - \"configured secret and build patterns\"", f'  content_sha256: {yaml_quote(combined)}', ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Context pack assembled: {output} ({len(items)} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
