# Artifact conventions

Artifacts are plain markdown files. They are read by people and by other
agents, so there is no JSON schema, only a fixed layout that every agent
follows. The same input should always produce the same set of sections in
the same order.

## Location and names

`runs/<run-id>/artifacts/<name>.md`, one file per owning agent:

`requirements`, `venue`, `weather`, `catering`, `program`, `services`,
`checklist`, `budget`, `validation`, `event-plan`.

An agent writes only its own artifact and never edits another one.

## Layout

Every domain artifact (everything except `requirements`, `validation`
and `event-plan`) has these sections in this order:

```
# <Title>

Owner: <agent name>
Run: <run-id>
Status: draft | final
Inputs: <artifacts this one was built from>

## Summary
Two or three sentences with the main recommendation.

## Details
The actual content. Tables for options, lists for steps.

## Costs
Table with item, quantity, unit price, total. Amounts carry the currency code (`400 EUR`).
Write "No costs" if the artifact has none.

## Sources
One line per source: `- [title](url) - what it was used for`.

## Open issues
Anything the next agent or the user should know. "None" if empty.
```

Rules:

- Costs use the currency fixed in `requirements.md`.
- Every venue, vendor, price or opening hour in Details must have a
  matching entry in Sources.
- Dates are ISO (`2026-08-01`), times are 24h (`18:30`).
- No placeholders such as `TBD` or `lorem ipsum` in a final artifact.

## Required sections

The `artifact-validator` skill checks these before the next group starts.

| Artifact | Header | Required sections, in order |
|---|---|---|
| venue, weather, catering, program, services, checklist, budget | yes | Summary, Details, Costs, Sources, Open issues |
| requirements | yes | Request, Confirmed requirements, Constraints, Assumptions, Q&A |
| validation | yes | one section per gate G1..G7 |
| event-plan | yes | Overview, Timeline, Budget, Checklist, Sources |

`Header` means the `Owner`, `Run`, `Status` lines under the title.

## Special artifacts

- `requirements.md` has `Request`, `Confirmed requirements`, `Constraints`,
  `Assumptions` and `Q&A`. It is the only artifact the user confirms.
- `validation.md` has one section per gate (G1..G7) with `PASS` or `FAIL`,
  findings and the name of the owning agent for each failure.
- `event-plan.md` is the merged timeline: `Overview`, `Timeline`,
  `Budget`, `Checklist`, `Sources`.
