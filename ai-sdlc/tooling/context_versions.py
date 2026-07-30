#!/usr/bin/env python3
"""Shared context-package ownership and Git-tag resolution."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


PACKAGE_PATHS = {
    "ai-sdlc/context/consistent/architecture/": "architecture",
    "ai-sdlc/context/guardrails/architecture/": "architecture",
    "ai-sdlc/context/consistent/security/": "security",
    "ai-sdlc/context/guardrails/security/": "security",
    "ai-sdlc/context/guardrails/security-baseline.md": "security",
    "ai-sdlc/context/consistent/technology/": "technology",
    "ai-sdlc/context/consistent/platform/": "platform",
    "ai-sdlc/context/consistent/business/": "domain",
    "ai-sdlc/context/consistent/product/": "product",
}
SEMVER = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def package_for(path: str) -> str | None:
    matches = [(len(prefix), package) for prefix, package in PACKAGE_PATHS.items() if path.startswith(prefix)]
    return max(matches)[1] if matches else None


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def latest_tag(package: str) -> str:
    track = f"context/{package}"
    tags = run("git", "tag", "--merged", "HEAD", "--list", f"{track}/v*").splitlines()
    versions = [(tuple(int(part) for part in SEMVER.match(tag.rsplit("/", 1)[-1]).groups()), tag) for tag in tags if SEMVER.match(tag.rsplit("/", 1)[-1])]
    return max(versions)[1] if versions else "unreleased"


def tag_commit(tag: str) -> str:
    return run("git", "rev-list", "-n", "1", tag) if tag != "unreleased" else run("git", "rev-parse", "HEAD")
