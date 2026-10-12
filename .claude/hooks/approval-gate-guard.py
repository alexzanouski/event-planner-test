#!/usr/bin/env python3
"""PreToolUse hook: block the final HTML until the plan is approved.

Writing runs/<run-id>/event-plan.html is allowed only if workflow-state.json
has approval.status == "approved" and approval.plan_hash equals the sha256
of the current artifacts/event-plan.md. Exit code 2 blocks the tool call.
"""
import hashlib
import json
import sys
from pathlib import Path


def block(message):
    print(f"approval-gate-guard: {message}", file=sys.stderr)
    sys.exit(2)


def main():
    event = json.load(sys.stdin)
    file_path = event.get("tool_input", {}).get("file_path")
    if not file_path:
        return
    path = Path(file_path)
    if path.name != "event-plan.html" or "runs" not in path.parts:
        return

    run_dir = path.parent
    state_file = run_dir / "workflow-state.json"
    plan_file = run_dir / "artifacts" / "event-plan.md"
    if not state_file.exists() or not plan_file.exists():
        block("no workflow state or no plan for this run, nothing was approved")

    approval = json.loads(state_file.read_text()).get("approval", {})
    if approval.get("status") != "approved":
        block(f"plan is not approved (status: {approval.get('status')})")
    current = hashlib.sha256(plan_file.read_bytes()).hexdigest()
    if approval.get("plan_hash") != current:
        block("plan changed after approval, ask the user to approve it again")


if __name__ == "__main__":
    main()
