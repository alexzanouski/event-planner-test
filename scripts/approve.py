#!/usr/bin/env python3
"""Record the user's decision on the event plan.

Usage:
  approve.py <run-dir> approve
  approve.py <run-dir> reject "<feedback>"

Approval stores the sha256 of artifacts/event-plan.md. approval-gate-guard
compares it with the current plan before the HTML may be written, so a
plan changed after approval needs a new approval. Approval is refused
while a quality gate has not passed.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main(argv):
    if len(argv) < 3 or argv[2] not in ("approve", "reject"):
        sys.exit(__doc__)
    run_dir = Path(argv[1])
    state_file = run_dir / "workflow-state.json"
    plan_file = run_dir / "artifacts" / "event-plan.md"
    if not state_file.exists() or not plan_file.exists():
        sys.exit("no state or no plan in this run")

    state = json.loads(state_file.read_text())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if argv[2] == "approve":
        open_gates = [g for g, i in state["gates"].items() if i["status"] != "pass"]
        if open_gates:
            sys.exit(f"cannot approve, gates not passed: {', '.join(open_gates)}")
        state["approval"] = {
            "status": "approved",
            "plan_hash": hashlib.sha256(plan_file.read_bytes()).hexdigest(),
            "approved_at": now,
            "feedback": None,
        }
    else:
        if len(argv) != 4 or not argv[3].strip():
            sys.exit("reject needs the user's feedback")
        state["approval"] = {
            "status": "rejected",
            "plan_hash": None,
            "approved_at": None,
            "feedback": argv[3],
        }
    state["updated_at"] = now
    state_file.write_text(json.dumps(state, indent=2) + "\n")
    print(f"approval: {state['approval']['status']}")


if __name__ == "__main__":
    main(sys.argv)
