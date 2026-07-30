#!/usr/bin/env python3
"""Render the latest framework and scoped artifact tags as a human view."""

from __future__ import annotations

import re
import subprocess


FRAMEWORK_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
SCOPED_TAG = re.compile(
    r"^(?P<track>initiative/[^/]+(?:/(?:hld|lld|context))?|context/[a-z-]+)/(?P<version>v\d+\.\d+\.\d+)$"
)


def main() -> int:
    latest: dict[str, tuple[tuple[int, int, int], str]] = {}
    tags = subprocess.run(["git", "tag", "--list"], check=True, capture_output=True, text=True).stdout.splitlines()
    for tag in tags:
        if FRAMEWORK_TAG.match(tag):
            track = "framework"
            version = tag
        else:
            match = SCOPED_TAG.match(tag)
            if not match:
                continue
            track = match.group("track")
            version = match.group("version")
        key = tuple(int(part) for part in version[1:].split("."))
        if track not in latest or key > latest[track][0]:
            latest[track] = (key, tag)

    print("# AI-SDLC Version Matrix\n")
    print("This view is derived from Git tags. Each HLD also records its exact design baseline.\n")
    print("| Track | Latest version tag | Git commit |")
    print("|---|---|---|")
    if not latest:
        print("| framework | unreleased | - |")
    for track in sorted(latest):
        tag = latest[track][1]
        commit = subprocess.run(["git", "rev-list", "-n", "1", tag], check=True, capture_output=True, text=True).stdout.strip()
        print(f"| `{track}` | `{tag}` | `{commit[:12]}` |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
