#!/usr/bin/env python3
"""PreToolUse hook: keep internal file names out of user-facing output.

Checked calls: Write/Edit of event-plan.html and AskUserQuestion.
Exit code 2 blocks the call and tells the model what to reword.
"""
import json
import re
import sys

LEAK = re.compile(
    r"\b(requirements|venue|weather|catering|program|services|checklist|"
    r"budget|validation|event-plan)\.md\b"
    r"|workflow-state\.json"
    r"|runs/[\w.-]+/artifacts"
)


def user_facing_text(event):
    tool = event.get("tool_name")
    data = event.get("tool_input", {})
    if tool in ("Write", "Edit"):
        if not str(data.get("file_path", "")).endswith("event-plan.html"):
            return ""
        return data.get("content") or data.get("new_string") or ""
    if tool == "AskUserQuestion":
        return json.dumps(data, ensure_ascii=False)
    return ""


def main():
    event = json.load(sys.stdin)
    found = sorted(set(m.group(0) for m in LEAK.finditer(user_facing_text(event))))
    if found:
        print(
            "no-leak-guard: internal names in user-facing output: "
            + ", ".join(found)
            + ". Describe the content in plain words instead.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
