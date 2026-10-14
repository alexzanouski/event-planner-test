#!/usr/bin/env python3
"""Build the static site from approved runs.

Usage: build_site.py [output-dir]      (default: site)

A run is included when its state says `approved`, the approved hash still
matches artifacts/event-plan.md and event-plan.html exists. Output:

  <out>/index.html            list of planned events
  <out>/<run-id>/index.html   the guide of one event, copied unchanged
"""
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"


def overview_field(plan_text, label):
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", plan_text, re.M)
    return match.group(1).strip() if match else ""


def read_run(run_dir):
    """Return the metadata of an approved run, or None."""
    state_file = run_dir / "workflow-state.json"
    plan_file = run_dir / "artifacts" / "event-plan.md"
    page = run_dir / "event-plan.html"
    if not (state_file.exists() and plan_file.exists() and page.exists()):
        return None
    approval = json.loads(state_file.read_text()).get("approval", {})
    current = hashlib.sha256(plan_file.read_bytes()).hexdigest()
    if approval.get("status") != "approved" or approval.get("plan_hash") != current:
        return None

    text = plan_file.read_text()
    date = re.search(r"\d{4}-\d{2}-\d{2}", overview_field(text, "Date"))
    kind = overview_field(text, "Event type").split(",")[0] or "Event"
    city = overview_field(text, "City")
    return {
        "id": run_dir.name,
        "title": f"{kind} in {city}" if city else kind,
        "date": date.group(0) if date else "",
        "guests": overview_field(text, "Guests").split(".")[0].split(",")[0],
        "cost": overview_field(text, "Total cost"),
        "page": page,
    }


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Planned events</title>
<style>
  :root {{ --bg: #fbf8f3; --card: #ffffff; --text: #2b2622; --muted: #7a6f66;
          --accent: #b5532f; --line: #e8dfd4; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #1c1917; --card: #26211e; --text: #f1ebe4; --muted: #a79b90;
            --accent: #e0825c; --line: #3a322d; }}
  }}
  body {{ margin: 0; background: var(--bg); color: var(--text);
         font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width: 760px; margin: 0 auto; padding: 40px 16px 48px; }}
  h1 {{ color: var(--accent); margin: 0 0 4px; }}
  p.lead {{ color: var(--muted); margin: 0 0 24px; }}
  ul {{ list-style: none; padding: 0; margin: 0; }}
  li a {{ display: block; background: var(--card); border: 1px solid var(--line);
         border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
         color: var(--text); text-decoration: none; }}
  li a:hover {{ border-color: var(--accent); }}
  .title {{ font-weight: 600; color: var(--accent); }}
  .meta {{ color: var(--muted); font-size: .9rem; }}
</style>
</head>
<body>
<main>
  <h1>Planned events</h1>
  <p class="lead">{count} event guides created by the event planner workflow.</p>
  <ul>
{items}
  </ul>
</main>
</body>
</html>
"""


def item(run):
    meta = " · ".join(
        html.escape(part) for part in (run["date"], run["guests"], run["cost"]) if part
    )
    return (
        f'    <li><a href="{html.escape(run["id"])}/">'
        f'<div class="title">{html.escape(run["title"])}</div>'
        f'<div class="meta">{meta}</div></a></li>'
    )


def main(argv):
    out = Path(argv[1]) if len(argv) > 1 else ROOT / "site"
    runs = [r for r in (read_run(d) for d in sorted(RUNS.glob("*/"))) if r]
    runs.sort(key=lambda r: (r["date"], r["id"]), reverse=True)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for run in runs:
        target = out / run["id"]
        target.mkdir()
        shutil.copyfile(run["page"], target / "index.html")
    (out / "index.html").write_text(
        INDEX.format(count=len(runs), items="\n".join(item(r) for r in runs))
    )
    print(f"built {out} with {len(runs)} event(s)")
    for run in runs:
        print(f"  {run['id']}: {run['title']} {run['date']}")


if __name__ == "__main__":
    main(sys.argv)
