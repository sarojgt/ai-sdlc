#!/usr/bin/env python3
"""Run an agent command with a portable process timeout."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: with_timeout.py <seconds> <command> [args...]", file=sys.stderr)
        return 2
    seconds = int(sys.argv[1])
    command = sys.argv[2:]
    process = subprocess.Popen(command, start_new_session=True)
    try:
        return process.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        print(f"Agent command timed out after {seconds} seconds: {Path(command[0]).name}", file=sys.stderr)
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
