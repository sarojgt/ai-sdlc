#!/usr/bin/env python3
"""Small dependency-free helpers for deterministic context selection."""

from __future__ import annotations

import re
from pathlib import Path


WORD_RE = re.compile(r"[a-z][a-z0-9-]{2,}")


def words(text: str) -> set[str]:
    return set(WORD_RE.findall(text.lower()))


def parse_index(path: Path) -> tuple[int, list[str], dict[str, dict[str, object]]]:
    version = 1
    budget = 30000
    default_sections: list[str] = []
    entries: dict[str, dict[str, object]] = {}
    current: dict[str, object] | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("version:"):
            version = int(re.search(r"\d+", line).group())
        elif line.startswith("advisory_token_budget:"):
            budget = int(re.search(r"\d+", line).group())
        elif line.startswith("- ") and "id:" in line:
            if current and "id" in current:
                entries[str(current["id"])] = current
            current = {"id": line.split("id:", 1)[1].strip().strip('"')}
        elif line.startswith("id:") and current is not None:
            current["id"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("summary:") and current is not None:
            current["summary"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("keywords:") and current is not None:
            value = line.split(":", 1)[1].strip().strip("[]")
            current["keywords"] = [item.strip().strip('"') for item in value.split(",") if item.strip()]
        elif line.startswith("selected_sections:") and current is not None:
            value = line.split(":", 1)[1].strip().strip("[]")
            current["selected_sections"] = [item.strip().strip('"') for item in value.split(",") if item.strip()]
        elif line.startswith("priority:") and current is not None:
            current["priority"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("applies_to:") and current is not None:
            value = line.split(":", 1)[1].strip().strip("[]")
            current["applies_to"] = [item.strip().strip('"') for item in value.split(",") if item.strip()]
        elif line.startswith("requires:") and current is not None:
            value = line.split(":", 1)[1].strip().strip("[]")
            current["requires"] = [item.strip().strip('"') for item in value.split(",") if item.strip()]
        elif line.startswith("- ") and current is None:
            default_sections.append(line[2:].strip().strip('"'))
    if current and "id" in current:
        entries[str(current["id"])] = current
    return budget, default_sections, entries


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group(2).strip()
        sections[title] = text[match.end():end].strip()
    return sections


def select_section_names(text: str, preferred: list[str], requirement_words: set[str], defaults: list[str]) -> list[str]:
    sections = markdown_sections(text)
    selected: list[str] = []
    for candidate in preferred + defaults:
        for title in sections:
            if title.casefold() == candidate.casefold() or candidate.casefold() in title.casefold():
                if title not in selected:
                    selected.append(title)
    if selected:
        return selected
    ranked = sorted(
        sections,
        key=lambda title: len(requirement_words.intersection(words(title + " " + sections[title]))),
        reverse=True,
    )
    return ranked[:2] if ranked else []


def excerpt(text: str, selected: list[str]) -> str:
    sections = markdown_sections(text)
    return "\n\n".join(f"## {title}\n\n{sections[title]}" for title in selected if sections.get(title))
