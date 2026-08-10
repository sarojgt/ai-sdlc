#!/usr/bin/env python3
"""Discover context documents and safely synchronize their catalog metadata."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_context_pack import sources  # noqa: E402
from context_selection import parse_index, words  # noqa: E402


STOPWORDS = {"context", "consistent", "guardrails", "architecture", "platform", "technology", "business", "product", "security", "principles", "and"}


def frontmatter_value(text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}:\s*([^\n]+)", text, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def inferred_class(path: Path) -> str:
    parts = set(path.parts)
    if "guardrails" in parts:
        return "guardrail"
    if "business" in parts:
        return "domain"
    if "technology" in parts:
        return "technology"
    if "architecture" in parts or "platform" in parts:
        return "enterprise"
    return "product"


def discover_local_sources(repo_root: Path, configured: list[dict[str, str]]) -> list[dict[str, str]]:
    """Find human-authored context documents not yet present in the registry."""
    known = {entry["id"] for entry in configured}
    context_root = repo_root / "ai-sdlc" / "context"
    discovered: list[dict[str, str]] = []
    if not context_root.is_dir():
        return discovered
    for path in sorted(context_root.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        context_id = frontmatter_value(text, "context_id")
        if not context_id or context_id in known:
            continue
        relative = path.relative_to(repo_root).as_posix()
        discovered.append({
            "id": context_id,
            "class": inferred_class(path.relative_to(context_root)),
            "source": relative,
            "authority": frontmatter_value(text, "authority") or "context-owner-review-required",
            "freshness": "90d",
        })
    return discovered


def append_registry_entries(path: Path, entries: list[dict[str, str]]) -> None:
    if not entries:
        return
    block = "\n".join(
        "\n".join([
            f"  - id: {entry['id']}",
            f"    class: {entry['class']}",
            f"    source: \"{entry['source']}\"",
            f"    authority: {entry['authority']}",
            f"    freshness: {entry['freshness']}",
        ]) for entry in entries
    )
    text = path.read_text(encoding="utf-8").rstrip() + "\n"
    marker = "\nselection:"
    if marker in text:
        text = text.replace(marker, f"\n{block}{marker}", 1)
    else:
        text += block + "\n"
    path.write_text(text, encoding="utf-8")


def heading_titles(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, re.MULTILINE)]


def suggestion(repo_root: Path, entry: dict[str, str]) -> str:
    source = entry.get("source", "")
    path = repo_root / source
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    title_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else entry["id"].replace("-", " ").title()
    terms = sorted(words(entry["id"].replace("-", " ") + " " + title) - STOPWORDS)[:12]
    headings = heading_titles(text)
    selected = [heading for heading in headings if re.search(r"hld|requirement|implication|decision|guardrail|boundary|design", heading, re.I)][:4]
    if not selected:
        selected = headings[:2] or ["all"]
    summary = f"Review and describe {title.lower()} for HLD context selection."
    quote = lambda value: '"' + value.replace('"', "'") + '"'
    return "\n".join([
        f"    - id: {entry['id']}",
        f"      summary: {quote(summary)}",
        f"      keywords: [{', '.join(terms)}]",
        f"      selected_sections: [{', '.join(quote(item) for item in selected)}]",
        "      priority: review-required",
        "      applies_to: [review-required]",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--update", action="store_true", help="Append stubs for missing entries; never delete or overwrite entries")
    args = parser.parse_args()
    repo_root = args.root.resolve()
    registry = repo_root / "ai-sdlc" / "config" / "context-sources.yaml"
    index_path = repo_root / "ai-sdlc" / "config" / "context-index.yaml"
    source_entries = sources(registry)
    discovered = discover_local_sources(repo_root, source_entries)
    if discovered:
        print("Unregistered local context documents: " + ", ".join(entry["id"] for entry in discovered))
    _, _, index_entries = parse_index(index_path)
    missing = [entry for entry in source_entries if entry["id"] not in index_entries]
    if args.update and discovered:
        append_registry_entries(registry, discovered)
        source_entries.extend(discovered)
        missing.extend(discovered)
    if not missing:
        print(f"Context catalog is up to date: {len(source_entries)} sources indexed.")
        return 0

    local = [entry for entry in missing if (repo_root / entry.get("source", "")).is_file()]
    provider = [entry for entry in missing if entry not in local]
    print(f"Missing context catalog entries: {len(missing)}")
    if local:
        print("Local sources: " + ", ".join(entry["id"] for entry in local))
    if provider:
        print("Provider-backed sources: " + ", ".join(entry["id"] for entry in provider))
    if not args.update:
        print("Run with --update to append review-required stubs.", file=sys.stderr)
        return 1

    text = index_path.read_text(encoding="utf-8").rstrip() + "\n"
    text += "\n# Entries below were generated by sync_context_catalog.py and require human refinement.\n"
    text += "\n\n".join(suggestion(repo_root, entry) for entry in missing) + "\n"
    index_path.write_text(text, encoding="utf-8")
    print(f"Appended {len(missing)} review-required catalog stubs to {index_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
