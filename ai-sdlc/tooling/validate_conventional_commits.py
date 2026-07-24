#!/usr/bin/env python3
"""Validate a PR title and all commits introduced by its base/head range."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conventional_commits import Commit, validate_commit  # noqa: E402

# Legacy Copilot progress commits were created before this repository enforced
# Conventional Commits. Keep this exemption narrow and remove it after all open
# branches with these subjects are merged or closed.
EXEMPT_COMMIT_SUBJECTS = {
    "Initial plan",
}


def git_commits(base: str, head: str) -> list[Commit]:
    result = subprocess.run(
        ["git", "log", "--format=%s%x1f%b%x1e", f"{base}..{head}"],
        check=True,
        capture_output=True,
        text=True,
    )
    commits = []
    for record in result.stdout.split("\x1e"):
        if not record.strip():
            continue
        subject, _, body = record.partition("\x1f")
        commits.append(Commit(subject.strip(), body.strip()))
    return commits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-title", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()

    errors = []
    title_error = validate_commit(Commit(args.pr_title))
    if title_error:
        errors.append(f"PR title `{args.pr_title}` {title_error}")

    commits = git_commits(args.base, args.head)
    if not commits:
        errors.append("PR contains no commits in the base/head range")
    for commit in commits:
        if commit.subject in EXEMPT_COMMIT_SUBJECTS:
            # Emit to stderr so CI logs preserve visibility without changing the
            # normal success output contract on stdout.
            print(f"Skipping exempt legacy commit subject: `{commit.subject}`", file=sys.stderr)
            continue
        error = validate_commit(commit)
        if error:
            errors.append(f"commit `{commit.subject}` {error}")

    if errors:
        print("Conventional Commit policy failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Conventional Commit policy passed for {len(commits)} commit(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
