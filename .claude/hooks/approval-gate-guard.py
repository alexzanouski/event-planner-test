#!/usr/bin/env python3
"""PreToolUse hook: block the final HTML until the plan is approved.

- Write/Edit of runs/<run-id>/event-plan.html is allowed only if
  workflow-state.json has approval.status == "approved" and
  approval.plan_hash equals the sha256 of the current artifacts/event-plan.md.
- Write/Edit of workflow-state.json is always blocked: the state is changed
  only by the scripts and hooks, so approval cannot be written by hand.
- Bash commands that would write either file (redirects, cp, mv, scripts
  and so on) are blocked, so the checks above cannot be bypassed.

Exit code 2 blocks the tool call.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROTECTED = re.compile(r"event-plan\.html|workflow-state\.json")
WRITES = re.compile(
    r">|\btee\b|\bcp\b|\bmv\b|\brm\b|\bsed\s+-i|\bdd\b|\bln\b|\btouch\b|\btruncate\b"
    r"|\binstall\b|\bpython3?\b|\bnode\b|\bperl\b|\bruby\b|\bjq\b"
)


def block(message):
    print(f"approval-gate-guard: {message}", file=sys.stderr)
    sys.exit(2)


def check_bash(command):
    if PROTECTED.search(command) and WRITES.search(command):
        block("the plan HTML and the run state are written only by html-builder "
              "and the workflow scripts, not by shell commands")


def check_html(path):
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


def main():
    event = json.load(sys.stdin)
    data = event.get("tool_input", {})
    if event.get("tool_name") == "Bash":
        check_bash(data.get("command", ""))
        return

    file_path = data.get("file_path")
    if not file_path:
        return
    path = Path(file_path)
    if "runs" not in path.parts:
        return
    if path.name == "workflow-state.json":
        block("the run state is changed only by the workflow scripts and hooks")
    if path.name == "event-plan.html":
        check_html(path)


if __name__ == "__main__":
    main()
