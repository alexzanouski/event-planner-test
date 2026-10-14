#!/usr/bin/env python3
"""Approval records for the event plan.

Approval is written only by the approval-recorder hook, from the user's
own answer to the approval question. The model can record a rejection
with feedback, but it cannot approve:

  approve.py <run-dir> reject "<feedback>"

Approval stores the sha256 of artifacts/event-plan.md. approval-gate-guard
compares it with the current plan before the HTML may be written. Approval
is refused while a quality gate has not passed.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def record(run_dir, decision, feedback=None):
    """Write the decision into the run state. Returns an error text or None."""
    run_dir = Path(run_dir)
    state_file = run_dir / "workflow-state.json"
    plan_file = run_dir / "artifacts" / "event-plan.md"
    if not state_file.exists() or not plan_file.exists():
        return "no state or no plan in this run"

    state = json.loads(state_file.read_text())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if decision == "approved":
        open_gates = [g for g, i in state["gates"].items() if i["status"] != "pass"]
        if open_gates:
            return f"cannot approve, gates not passed: {', '.join(open_gates)}"
        state["approval"] = {
            "status": "approved",
            "plan_hash": hashlib.sha256(plan_file.read_bytes()).hexdigest(),
            "approved_at": now,
            "feedback": None,
        }
    else:
        state["approval"] = {
            "status": "rejected",
            "plan_hash": None,
            "approved_at": None,
            "feedback": feedback,
        }
    state["updated_at"] = now
    state_file.write_text(json.dumps(state, indent=2) + "\n")
    return None


def main(argv):
    if len(argv) != 4 or argv[2] != "reject" or not argv[3].strip():
        sys.exit(__doc__)
    error = record(argv[1], "rejected", argv[3])
    if error:
        sys.exit(error)
    print("approval: rejected")


if __name__ == "__main__":
    main(sys.argv)
