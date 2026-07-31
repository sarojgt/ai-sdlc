#!/usr/bin/env python3
"""Run the deterministic lifecycle hooks implemented for the HLD stage."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(*command: str) -> None:
    subprocess.run(command, check=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: run_lifecycle_hooks.py <before_hld|after_hld> <initiative-dir>", file=sys.stderr)
        return 2
    phase, raw = sys.argv[1:]
    initiative = Path(raw).resolve()
    tooling = Path(__file__).resolve().parent
    if phase == "before_hld":
        run(sys.executable, str(tooling / "approval_gate.py"), "requirements", str(initiative))
        run(sys.executable, str(tooling / "build_context_pack.py"), str(initiative))
        completed = ["validate_initiative_exists", "validate_required_parent_artifact", "validate_context_pack", "create_agent_run_record"]
    elif phase == "after_hld":
        run(sys.executable, str(tooling / "validate_hld_artifacts.py"), str(initiative))
        completed = ["validate_agent_response", "validate_das_artifacts", "calculate_content_hashes", "attach_run_evidence"]
    else:
        print(f"Unsupported hook phase: {phase}", file=sys.stderr)
        return 2
    evidence = initiative / "evidence" / f"hooks-{phase}.yaml"
    evidence.parent.mkdir(exist_ok=True)
    evidence.write_text("hooks:\n  phase: \"%s\"\n  completed_at: \"%s\"\n  completed:\n%s" % (phase, datetime.now(timezone.utc).isoformat(), "".join(f"    - {hook}\n" for hook in completed)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
