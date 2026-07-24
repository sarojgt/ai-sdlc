#!/usr/bin/env python3
"""Shared Conventional Commit parsing for policy and release automation."""

from __future__ import annotations

import re
from dataclasses import dataclass


TYPES = {
    "feat": "minor",
    "fix": "patch",
    "perf": "patch",
    "refactor": "patch",
    "revert": "patch",
    "docs": "none",
    "test": "none",
    "chore": "none",
    "ci": "none",
    "build": "none",
    "style": "none",
}

HEADER = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[A-Za-z0-9._/-]+)\))?(?P<breaking>!)?:\s+(?P<description>\S.*)$"
)


@dataclass(frozen=True)
class Commit:
    subject: str
    body: str = ""

    @property
    def breaking(self) -> bool:
        return bool(HEADER.match(self.subject) and HEADER.match(self.subject).group("breaking")) or bool(
            re.search(r"^BREAKING CHANGE(?:\s*\([^)]*\))?:", self.body, flags=re.MULTILINE)
        )

    @property
    def commit_type(self) -> str | None:
        match = HEADER.match(self.subject)
        return match.group("type") if match else None

    def release_bump(self) -> str:
        if self.breaking:
            return "major"
        return TYPES.get(self.commit_type or "", "none")


def validate_commit(commit: Commit) -> str | None:
    match = HEADER.match(commit.subject)
    if not match:
        return "must match `type(scope)!: description` with a supported type"
    if match.group("type") not in TYPES:
        return f"uses unsupported type `{match.group('type')}`"
    return None


def highest_bump(commits: list[Commit]) -> str:
    priority = {"none": 0, "patch": 1, "minor": 2, "major": 3}
    return max((commit.release_bump() for commit in commits), key=lambda value: priority[value], default="none")
