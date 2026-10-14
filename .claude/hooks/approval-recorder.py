#!/usr/bin/env python3
"""PostToolUse hook: record the user's answer to the approval question.

The coordinator asks exactly "Approve the event plan for run <run-id>?"
with the options "Approve" and "Request changes". This hook reads the
answer the user gave, not anything the model says, and writes it to the
run state through scripts/approve.py. Only an exact "Approve" approves.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import approve  # noqa: E402

QUESTION = re.compile(r"^Approve the event plan for run ([\w.-]+)\?$")


def find_answers(obj):
    """Collect question -> answer pairs from the tool input and response."""
    found = {}
    if isinstance(obj, dict):
        answers = obj.get("answers")
        if isinstance(answers, dict):
            found.update({str(k): str(v) for k, v in answers.items()})
        for value in obj.values():
            found.update(find_answers(value))
    elif isinstance(obj, list):
        for value in obj:
            found.update(find_answers(value))
    elif isinstance(obj, str):
        # Text form: "question"="answer"
        found.update(dict(re.findall(r'"([^"]+)"="([^"]*)"', obj)))
    return found


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "AskUserQuestion":
        return
    questions = [q.get("question", "") for q in event.get("tool_input", {}).get("questions", [])]
    asked = [(q, QUESTION.match(q)) for q in questions]
    asked = [(q, m.group(1)) for q, m in asked if m]
    if not asked:
        return

    answers = find_answers(event.get("tool_input", {}))
    answers.update(find_answers(event.get("tool_response")))
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ROOT))
    for question, run_id in asked:
        answer = answers.get(question)
        if answer is None:
            print(f"approval-recorder: no answer found for run {run_id}, nothing recorded", file=sys.stderr)
            sys.exit(2)
        decision = "approved" if answer.strip() == "Approve" else "rejected"
        feedback = None if decision == "approved" else answer
        error = approve.record(project / "runs" / run_id, decision, feedback)
        if error:
            print(f"approval-recorder: {error}", file=sys.stderr)
            sys.exit(2)
        print(f"approval-recorder: run {run_id} {decision} by the user", file=sys.stderr)


if __name__ == "__main__":
    main()
