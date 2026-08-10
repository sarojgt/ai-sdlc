#!/usr/bin/env python3
"""Build a deterministic, section-aware context manifest and advisory pack."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from context_selection import excerpt, select_section_names, words, parse_index  # noqa: E402
from context_versions import latest_tag, package_for, tag_commit  # noqa: E402

BASELINE_IDS = {"enterprise-architecture", "security-baseline", "api-standards", "arb-governance"}
GENERIC_CONTEXT_WORDS = {
    "context", "consistent", "guardrails", "architecture", "platform", "technology",
    "business", "product", "security", "principles", "source", "sources", "and",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(path: Path) -> list[dict[str, str]]:
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
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: build_context_pack.py <initiative-dir> [--check|--explain]", file=sys.stderr)
        return 2
    initiative = Path(sys.argv[1]).resolve()
    mode = sys.argv[2] if len(sys.argv) == 3 else ""
    if mode not in {"", "--check", "--explain"}:
        print("Unknown mode; expected --check or --explain", file=sys.stderr)
        return 2
    check = mode == "--check"
    root = Path(__file__).resolve().parents[1]
    requirement = initiative / "requirement.md"
    if not requirement.is_file():
        print(f"Missing requirement: {requirement}", file=sys.stderr)
        return 1

    requirement_text = requirement.read_text(encoding="utf-8")
    requirement_words = words(requirement_text)
    index_path = root / "config" / "context-index.yaml"
    budget, default_sections, index = parse_index(index_path) if index_path.exists() else (30000, [], {})
    items: list[dict[str, object]] = []
    excerpts: list[str] = [f"# Context pack: {initiative.name}", "", "This generated pack is advisory input assembled from the allowlisted context manifest.", ""]

    source_entries = sources(root / "config" / "context-sources.yaml")
    selected_ids: set[str] = set()
    selected_reasons: dict[str, str] = {}
    for entry in source_entries:
        source = entry.get("source", "")
        path = root.parent / source
        if not path.is_file():
            continue
        metadata = index.get(entry["id"], {})
        keywords = set(metadata.get("keywords", [])) if isinstance(metadata.get("keywords"), list) else set()
        fallback_terms = words(entry["id"].replace("-", " ")) - GENERIC_CONTEXT_WORDS
        matches = len(requirement_words.intersection(keywords | fallback_terms))
        if entry.get("id") in BASELINE_IDS or matches >= 2:
            selected_ids.add(entry["id"])
            selected_reasons[entry["id"]] = "baseline policy" if entry.get("id") in BASELINE_IDS else f"{matches} requirement terms matched indexed vocabulary"
    changed = True
    while changed:
        changed = False
        for source_id in list(selected_ids):
            metadata = index.get(source_id, {})
            requires = metadata.get("requires", []) if isinstance(metadata.get("requires"), list) else []
            for dependency in requires:
                if dependency not in selected_ids and any(item.get("id") == dependency for item in source_entries):
                    selected_ids.add(dependency)
                    selected_reasons[dependency] = f"required by selected context: {source_id}"
                    changed = True

    for entry in source_entries:
        source = entry.get("source", "")
        path = root.parent / source
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        metadata = index.get(entry["id"], {})
        keywords = set(metadata.get("keywords", [])) if isinstance(metadata.get("keywords"), list) else set()
        fallback_terms = words(entry["id"].replace("-", " ")) - GENERIC_CONTEXT_WORDS
        matches = len(requirement_words.intersection(keywords | fallback_terms))
        always = entry.get("id") in BASELINE_IDS
        if entry["id"] not in selected_ids:
            continue
        preferred = metadata.get("selected_sections", []) if isinstance(metadata.get("selected_sections"), list) else []
        selected_sections = select_section_names(text, [str(item) for item in preferred], requirement_words, default_sections)
        selected_text = excerpt(text, selected_sections) or text[:4000]
        token_estimate = max(1, len(selected_text) // 4)
        package = package_for(source)
        item = {
            **entry,
            "path": source,
            "package": package or "unversioned",
            "version_tag": latest_tag(package) if package else "unversioned",
            "version_commit": tag_commit(latest_tag(package)) if package else "",
            "content_sha256": digest(path),
            "selection": "baseline" if always else ("dependency" if entry["id"] in selected_reasons and selected_reasons[entry["id"]].startswith("required") else f"metadata-keyword-match:{matches}"),
            "selection_score": 100 if always else matches,
            "selection_reasons": selected_reasons.get(entry["id"], f"{matches} requirement terms matched indexed vocabulary"),
            "selected_sections": ", ".join(selected_sections),
            "estimated_tokens": str(token_estimate),
            "summary": str(metadata.get("summary", "")),
            "priority": str(metadata.get("priority", "optional")),
            "applies_to": ", ".join(str(item) for item in metadata.get("applies_to", [])) if isinstance(metadata.get("applies_to"), list) else "",
            "requires": ", ".join(str(item) for item in metadata.get("requires", [])) if isinstance(metadata.get("requires"), list) else "",
        }
        items.append(item)
        excerpts.extend([f"## {entry['id']}", "", f"Source: `{source}`", "", selected_text, ""])

    relative_dir = initiative / "context" / "relative"
    for path in sorted(relative_dir.rglob("*")) if relative_dir.is_dir() else []:
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            selected_text = text
            item = {"id": f"relative-{path.stem}", "class": "relative", "authority": "initiative-owner", "freshness": "initiative", "path": str(path.relative_to(initiative)), "package": "relative", "version_tag": "unreleased", "version_commit": "", "content_sha256": digest(path), "selection": "explicit-relative-context", "selection_score": 100, "selection_reasons": "explicit initiative context", "summary": "Initiative-specific context supplied with the requirement.", "priority": "required", "applies_to": "initiative", "requires": "", "selected_sections": "all", "estimated_tokens": str(max(1, len(selected_text) // 4))}
            items.append(item)
            excerpts.extend([f"## {item['id']}", "", f"Source: `{item['path']}`", "", selected_text, ""])

    pack_path = initiative / "evidence" / "context-pack.md"
    pack_path.parent.mkdir(parents=True, exist_ok=True)
    pack_text = "\n".join(excerpts).rstrip() + "\n"
    pack_path.write_text(pack_text, encoding="utf-8")
    total_tokens = sum(int(str(item["estimated_tokens"])) for item in items)
    budget_status = "within-advisory-budget" if total_tokens <= budget else "over-advisory-budget"
    combined = hashlib.sha256("\n".join(f"{item['path']}:{item['content_sha256']}:{item['selected_sections']}" for item in items).encode()).hexdigest()
    pack_hash = digest(pack_path)
    output = initiative / "context-manifest.yaml"
    if check:
        existing = output.read_text(encoding="utf-8") if output.exists() else ""
        if f'content_sha256: "{combined}"' not in existing or not pack_path.exists():
            print("Context manifest or generated context pack is missing or stale; run build_context_pack.py", file=sys.stderr)
            return 1
        print(f"Context selection check passed: {len(items)} items, approximately {total_tokens} tokens ({budget_status}).")
        return 0

    lines = ["das_version: \"0.1\"", f"initiative: {yaml_quote(initiative.name)}", "context_pack:", f"  id: {yaml_quote('CTX-' + initiative.name + '-v1')}", "  version: 1", "  status: assembled", "  selection_policy_version: \"1\"", f"  advisory_token_budget: {budget}", f"  estimated_tokens: {total_tokens}", f"  budget_status: {yaml_quote(budget_status)}", f"  generated_pack: {yaml_quote('evidence/context-pack.md')}", f"  generated_pack_sha256: {yaml_quote(pack_hash)}", "  items:"]
    for item in items:
        lines.extend([f"    - id: {yaml_quote(str(item['id']))}", f"      class: {yaml_quote(str(item['class']))}", f"      package: {yaml_quote(str(item['package']))}", f"      version_tag: {yaml_quote(str(item['version_tag']))}", f"      version_commit: {yaml_quote(str(item['version_commit']))}", f"      path: {yaml_quote(str(item['path']))}", f"      authority: {yaml_quote(str(item['authority']))}", f"      freshness: {yaml_quote(str(item['freshness']))}", f"      selection: {yaml_quote(str(item['selection']))}", f"      selection_score: {item['selection_score']}", f"      selection_reasons: {yaml_quote(str(item['selection_reasons']))}", f"      summary: {yaml_quote(str(item['summary']))}", f"      priority: {yaml_quote(str(item['priority']))}", f"      applies_to: {yaml_quote(str(item['applies_to']))}", f"      requires: {yaml_quote(str(item['requires']))}", f"      selected_sections: {yaml_quote(str(item['selected_sections']))}", f"      estimated_tokens: {item['estimated_tokens']}", f"      content_sha256: {yaml_quote(str(item['content_sha256']))}"])
    lines.extend(["  exclusions:", "    - \"configured secret and build patterns\"", f"  content_sha256: {yaml_quote(combined)}", ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    status_message = "within advisory budget" if budget_status == "within-advisory-budget" else "over advisory budget; continuing without blocking"
    print(f"Context pack assembled: {output} ({len(items)} items, approximately {total_tokens} tokens; {status_message}).")
    if mode == "--explain":
        print("\nSelected context:")
        for item in items:
            print(f"- {item['id']}: {item['selection_reasons']}; sections={item['selected_sections']}")
        print("\nExcluded sources are not copied into the generated pack unless explicitly added as relative context.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
