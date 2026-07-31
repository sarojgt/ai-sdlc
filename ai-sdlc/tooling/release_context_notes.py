#!/usr/bin/env python3
"""Render the context package versions available at the current Git commit."""

from __future__ import annotations

from context_versions import PACKAGE_PATHS, latest_tag, tag_commit


def main() -> int:
    packages = sorted(set(PACKAGE_PATHS.values()))
    print("## Context versions\n")
    print("These context package versions were available at the release commit.\n")
    print("| Package | Version tag | Source commit |")
    print("|---|---|---|")
    for package in packages:
        tag = latest_tag(package)
        commit = tag_commit(tag)[:12] if tag != "unreleased" else "-"
        print(f"| `{package}` | `{tag}` | `{commit}` |")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
