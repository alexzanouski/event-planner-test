#!/usr/bin/env python3
"""Workflow state helper.

Usage:
  state.py init <run-dir>                    create workflow-state.json
  state.py write <run-dir> <artifact-file>   record that an artifact was written
  state.py set <run-dir> <stage> <status>    set a stage status by hand
  state.py confirm <run-dir>                 record that the user confirmed the requirements
  state.py gate <run-dir> <G> <pass|fail|retry> [owner]
                                             record a gate result, or count a retry
  state.py show <run-dir>                    print stage statuses

The state file is runs/<run-id>/workflow-state.json, see docs/state.md.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "workflow-state.json"
STATUSES = {"pending", "running", "done", "failed", "stale"}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def state_path(run_dir):
    return Path(run_dir) / "workflow-state.json"


def load(run_dir):
    return json.loads(state_path(run_dir).read_text())


def save(run_dir, state):
    state["updated_at"] = now()
    state_path(run_dir).write_text(json.dumps(state, indent=2) + "\n")


def init(run_dir):
    run_dir = Path(run_dir)
    if state_path(run_dir).exists():
        sys.exit(f"state already exists: {state_path(run_dir)}")
    run_dir.mkdir(parents=True, exist_ok=True)
    state = json.loads(TEMPLATE.read_text())
    state["run_id"] = run_dir.name
    state["created_at"] = now()
    save(run_dir, state)


def dependents(stages, name):
    """All stages that depend on `name`, directly or through other stages."""
    found = set()
    todo = [name]
    while todo:
        current = todo.pop()
        for other, info in stages.items():
            if current in info["depends_on"] and other not in found:
                found.add(other)
                todo.append(other)
    return found


def write(run_dir, artifact_file):
    """Called after an artifact was written. Returns the stage name or None."""
    state = load(run_dir)
    path = Path(artifact_file)
    stage = next(
        (n for n, i in state["stages"].items() if i["artifact"] == path.name), None
    )
    if stage is None or not path.exists():
        return None

    text = path.read_text()
    digest = hashlib.sha256(text.encode()).hexdigest()
    info = state["stages"][stage]
    changed = info["hash"] is not None and info["hash"] != digest

    info["hash"] = digest
    info["attempts"] += 1
    # HTML has no Status line, writing it is the end of that stage.
    final = path.suffix == ".html" or "Status: final" in text
    info["status"] = "done" if final else "running"
    info["updated_at"] = now()

    # Downstream work was built from the old content, mark it for a re-run.
    if changed:
        for name in dependents(state["stages"], stage):
            if state["stages"][name]["status"] == "done":
                state["stages"][name]["status"] = "stale"
                state["stages"][name]["updated_at"] = now()
    save(run_dir, state)
    return stage


def set_status(run_dir, stage, status):
    if status not in STATUSES:
        sys.exit(f"unknown status: {status}")
    state = load(run_dir)
    if stage not in state["stages"]:
        sys.exit(f"unknown stage: {stage}")
    state["stages"][stage]["status"] = status
    state["stages"][stage]["updated_at"] = now()
    save(run_dir, state)


def gate(run_dir, name, result, owner=None):
    """`retry` counts one more re-run caused by the gate and prints the total."""
    if result not in ("pass", "fail", "retry"):
        sys.exit(f"unknown gate result: {result}")
    state = load(run_dir)
    if name not in state["gates"]:
        sys.exit(f"unknown gate: {name}")
    entry = state["gates"][name]
    if result == "retry":
        entry["retries"] += 1
    else:
        entry["status"] = result
        entry["owner"] = owner if result == "fail" else None
    save(run_dir, state)
    print(f"{name}: {entry['status']}, retries={entry['retries']}")


def confirm(run_dir):
    state = load(run_dir)
    state["requirements_confirmed"] = True
    save(run_dir, state)


def show(run_dir):
    state = load(run_dir)
    for name, info in state["stages"].items():
        print(f"{info['group']:>2} {name:<26} {info['status']:<8} attempts={info['attempts']}")
    for name, info in state["gates"].items():
        print(f"{name} {info['status']:<7} retries={info['retries']} owner={info['owner']}")
    print(f"requirements confirmed: {state['requirements_confirmed']}")
    print(f"approval: {state['approval']['status']}")


def main(argv):
    commands = {"init": (init, 1, 1), "write": (write, 2, 2), "set": (set_status, 3, 3),
                "gate": (gate, 3, 4), "confirm": (confirm, 1, 1), "show": (show, 1, 1)}
    if len(argv) < 2 or argv[1] not in commands:
        sys.exit(__doc__)
    func, low, high = commands[argv[1]]
    if not low <= len(argv) - 2 <= high:
        sys.exit(__doc__)
    func(*argv[2:])


if __name__ == "__main__":
    main(sys.argv)
