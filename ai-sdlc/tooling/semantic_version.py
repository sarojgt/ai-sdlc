#!/usr/bin/env python3
"""Calculate the next semantic release tag from the merged PR title."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conventional_commits import Commit, highest_bump  # noqa: E402


SEMVER_TAG = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def latest_tag() -> str | None:
    tags = [tag for tag in run("git", "tag", "--list", "v*", "--sort=-version:refname").splitlines() if SEMVER_TAG.match(tag)]
    return tags[0] if tags else None


def commits_since(tag: str | None) -> list[Commit]:
    revision = f"{tag}..HEAD" if tag else "HEAD"
    output = run("git", "log", "--format=%s%x1f%b%x1e", revision)
    commits = []
    for record in output.split("\x1e"):
        if not record.strip():
            continue
        subject, _, body = record.partition("\x1f")
        commits.append(Commit(subject.strip(), body.strip()))
    return commits


def next_version(tag: str | None, bump: str) -> str:
    current = [int(part) for part in (SEMVER_TAG.match(tag).groups() if tag else (0, 0, 0))]
    if bump == "major":
        current = [current[0] + 1, 0, 0]
    elif bump == "minor":
        current = [current[0], current[1] + 1, 0]
    else:
        current = [current[0], current[1], current[2] + 1]
    return "v" + ".".join(str(part) for part in current)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--pr-title", help="Merged PR title used as the release intent")
    args = parser.parse_args()

    tag = latest_tag()
    commits = [Commit(args.pr_title)] if args.pr_title else commits_since(tag)
    bump = highest_bump(commits)
    if args.explain:
        print(f"latest_tag={tag or 'none'}")
        print(f"commits={len(commits)}")
        print(f"release_bump={bump}")
    if bump == "none":
        return 0
    print(next_version(tag, bump))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
