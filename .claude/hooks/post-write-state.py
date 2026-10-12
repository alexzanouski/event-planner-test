#!/usr/bin/env python3
"""PostToolUse hook: keep workflow-state.json in sync with written artifacts.

Fires after Write and Edit. If the file lives in runs/<run-id>/ and the run
has a state file, the matching stage is updated by scripts/state.py.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import state  # noqa: E402


def run_dir_of(path):
    """Return runs/<run-id> for a file inside a run, else None."""
    parts = path.resolve().parts
    if "runs" not in parts:
        return None
    i = len(parts) - 1 - parts[::-1].index("runs")
    if i + 2 >= len(parts):
        return None
    return Path(*parts[: i + 2])


def main():
    event = json.load(sys.stdin)
    file_path = event.get("tool_input", {}).get("file_path")
    if not file_path:
        return
    path = Path(file_path)
    run_dir = run_dir_of(path)
    if run_dir is None or not (run_dir / "workflow-state.json").exists():
        return
    stage = state.write(run_dir, path)
    if stage:
        print(f"workflow-state: {stage} updated", file=sys.stderr)


if __name__ == "__main__":
    main()
