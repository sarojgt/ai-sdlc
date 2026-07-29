#!/usr/bin/env python3
"""Calculate scoped artifact tags from the merged PR title and changed paths."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conventional_commits import Commit  # noqa: E402


SEMVER = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
PRIORITY = {"none": 0, "patch": 1, "minor": 2, "major": 3}


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def commits(revision: str = "HEAD") -> list[tuple[Commit, list[str]]]:
    hashes = run(
        "git", "log", "--format=%H", revision, "--", "ai-sdlc/initiatives", "ai-sdlc/context"
    ).splitlines()
    result = []
    for commit_hash in hashes:
        metadata = run("git", "show", "-s", "--format=%s%x1f%b", commit_hash)
        subject, _, body = metadata.partition("\x1f")
        paths = run(
            "git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-m", commit_hash
        ).splitlines()
        result.append((Commit(subject.strip(), body.strip()), paths))
    return result


def merged_change(title: str) -> list[tuple[Commit, list[str]]]:
    paths = run(
        "git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-m", "HEAD"
    ).splitlines()
    return [(Commit(title), paths)]


def tracks(paths: list[str], commit: Commit) -> set[str]:
    result = set()
    for path in paths:
        parts = path.split("/")
        if len(parts) >= 3 and parts[:2] == ["ai-sdlc", "initiatives"]:
            initiative = parts[2]
            area = parts[3] if len(parts) > 3 else ""
            if area == "hld" and commit.scope == "hld":
                result.add(f"initiative/{initiative}/hld")
            elif area == "lld" and commit.scope == "lld":
                result.add(f"initiative/{initiative}/lld")
            elif area == "context" and len(parts) > 4 and parts[4] == "relative" and commit.scope == "context":
                result.add(f"initiative/{initiative}/context")
            elif area not in {"hld", "lld", "context"} and commit.scope in {
                "initiative", "requirement", "approval", "traceability"
            }:
                result.add(f"initiative/{initiative}")
        elif path.startswith("ai-sdlc/context/consistent/") and commit.scope == "context":
            result.add("context/consistent")
        elif path.startswith("ai-sdlc/context/guardrails/") and commit.scope == "context":
            result.add("context/guardrails")
    return result


def latest_tag(track: str) -> str | None:
    tags = run("git", "tag", "--list", f"{track}/v*").splitlines()
    versions = []
    for tag in tags:
        version = tag.rsplit("/", 1)[-1]
        if SEMVER.match(version):
            versions.append((tuple(int(part) for part in SEMVER.match(version).groups()), tag))
    return max(versions)[1] if versions else None


def next_tag(track: str, tag: str | None, bump: str) -> str:
    current = [int(part) for part in (SEMVER.match(tag.rsplit("/", 1)[-1]).groups() if tag else (0, 0, 0))]
    if bump == "major":
        current = [current[0] + 1, 0, 0]
    elif bump == "minor":
        current = [current[0], current[1] + 1, 0]
    else:
        current = [current[0], current[1], current[2] + 1]
    return f"{track}/v{'.'.join(str(part) for part in current)}"


def main() -> int:
    all_entries = commits()
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-title", help="Merged PR title used as the release intent")
    args = parser.parse_args()
    if args.pr_title:
        all_entries = merged_change(args.pr_title)
    discovered_tracks: set[str] = set()
    for commit, paths in all_entries:
        discovered_tracks.update(tracks(paths, commit))

    for track in sorted(discovered_tracks):
        previous = latest_tag(track)
        entries = commits(f"{previous}..HEAD") if previous else all_entries
        applicable = []
        for commit, paths in entries:
            if track in tracks(paths, commit):
                applicable.append(commit)
        bump = max(
            (commit.artifact_release_bump() for commit in applicable),
            key=lambda value: PRIORITY[value],
            default="none",
        )
        if bump != "none":
            print(f"{track}|{next_tag(track, previous, bump)}|{bump}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
