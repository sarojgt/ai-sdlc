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

SCOPES = {
    "initiative",
    "requirement",
    "context",
    "hld",
    "lld",
    "approval",
    "traceability",
    "workflow",
    "policy",
    "release",
    "ai-sdlc",
    "repo",
}

ARTIFACT_ONLY_SCOPES = {
    "initiative",
    "requirement",
    "context",
    "hld",
    "lld",
    "approval",
    "traceability",
}

HEADER = re.compile(
    r"^(?P<type>[a-z]+)\((?P<scope>[A-Za-z0-9._/-]+)\)(?P<breaking>!)?:\s+(?P<description>\S.*)$"
)

BRANCH = re.compile(
    r"^(?P<type>[a-z]+)\/(?P<scope>ai-sdlc|initiative|requirement|context|hld|lld|approval|traceability|workflow|policy|release|repo)-(?P<description>[a-z0-9]+(?:-[a-z0-9]+)*)$"
)

PROHIBITED_BRANCH_PREFIXES = {"agent", "copilot", "codex", "claude", "gemini", "qwen", "ai"}


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
        if self.scope in ARTIFACT_ONLY_SCOPES:
            return "none"
        return TYPES.get(self.commit_type or "", "none")

    @property
    def scope(self) -> str | None:
        match = HEADER.match(self.subject)
        return match.group("scope") if match else None


def validate_commit(commit: Commit) -> str | None:
    match = HEADER.match(commit.subject)
    if not match:
        return "must match `type(scope)!: description` with a supported type"
    if match.group("type") not in TYPES:
        return f"uses unsupported type `{match.group('type')}`"
    if match.group("scope") not in SCOPES:
        return f"uses unsupported scope `{match.group('scope')}`"
    return None


def validate_branch_name(branch: str) -> str | None:
    match = BRANCH.match(branch)
    if not match:
        return "must match `type/scope-short-description` using lowercase kebab-case"
    if match.group("type") not in TYPES:
        return f"uses unsupported type `{match.group('type')}`"
    if match.group("scope") not in SCOPES:
        return f"uses unsupported scope `{match.group('scope')}`"
    if match.group("type") in PROHIBITED_BRANCH_PREFIXES:
        return f"uses prohibited provider-oriented prefix `{match.group('type')}`"
    return None


def highest_bump(commits: list[Commit]) -> str:
    priority = {"none": 0, "patch": 1, "minor": 2, "major": 3}
    return max((commit.release_bump() for commit in commits), key=lambda value: priority[value], default="none")
