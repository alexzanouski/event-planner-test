---
name: event-html-theme-builder
description: Rules and the predefined template for rendering an approved event-plan.md as a standalone HTML page. Use when building the final event guide.
---

# event-html-theme-builder

Turns `event-plan.md` into one standalone HTML file using
`template.html` in this folder. The same plan always gives the same page
structure.

## Steps

1. Read `template.html` and the approved `event-plan.md`.
2. Replace each placeholder with HTML made from the matching section:

   | Placeholder | Source |
   |---|---|
   | `{{TITLE}}` | event type and city, for example `Birthday in Warsaw` |
   | `{{SUBTITLE}}` | date and time window |
   | `{{OVERVIEW}}` | section `Overview` |
   | `{{TIMELINE}}` | section `Timeline` |
   | `{{BUDGET}}` | section `Budget` |
   | `{{CHECKLIST}}` | section `Checklist` |
   | `{{SOURCES}}` | section `Sources` |

3. Write the result to `runs/<run-id>/event-plan.html`.

## Rendering rules

- Markdown tables become `<table>`, lists become `<ul>`, in the same
  order as in the plan. Do not reorder, merge or drop rows.
- Escape `&`, `<` and `>` in text. Links are `<a href target="_blank"
  rel="noopener">` with the URL from the plan.
- In the timeline wrap the `Rain fallback` row in
  `<tr class="fallback">`.
- Do not add text that is not in the plan: no intro, no tips, no
  decorative copy.
- Do not change the template's CSS, structure or section ids. No external
  scripts, fonts or images, the page must work offline.
- Never print internal names (artifact file names, `workflow-state.json`,
  run paths) in the page. Refer to content by its section title.
