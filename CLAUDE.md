# Event Planner Workflow

Agentic workflow for planning an event. The user runs `/plan-event <request>`,
the coordinator gathers missing requirements, runs specialised subagents,
validates their artifacts, asks for approval and only then renders the
final HTML page.

Domain: events (birthdays, corporate parties, small weddings, meetups).

## Architecture

Hub-and-spoke. The coordinator (`/plan-event`) is the only orchestrator.
It never writes event content itself, it only plans, delegates, validates
and tracks state. Every subagent has one job and owns one artifact.

```
requirements-formalizer
  -> [venue-planner, weather]                                  group A
  -> [catering-planner, program-planner, services-planner]     group B
  -> [guest-checklist-planner, budget-aggregator]              group C
  -> validator          (targeted retry on fail, max 3)
  -> plan-builder
  -> human approval     (revision loop on reject)
  -> html-builder
```

Agents inside a group run in parallel. Groups run one after another because
each group reads the artifacts of the previous ones.

## Agents

| Agent | Owns | Reads |
|---|---|---|
| requirements-formalizer | `requirements.md` | user request, Q&A |
| venue-planner | `venue.md` | requirements |
| weather | `weather.md` | requirements, venue |
| catering-planner | `catering.md` | requirements, venue, weather |
| program-planner | `program.md` | requirements, venue, weather |
| services-planner | `services.md` | requirements, venue, weather |
| guest-checklist-planner | `checklist.md` | requirements, venue, program, weather |
| budget-aggregator | `budget.md` | all domain artifacts |
| validator | `validation.md` | all artifacts |
| plan-builder | `event-plan.md` | all validated artifacts |
| html-builder | `event-plan.html` | approved `event-plan.md` |

## Execution rules

1. Do not start planning until `requirements.md` is confirmed by the user.
   Ask all missing questions in one batch, not one by one.
2. Every artifact is checked with the `artifact-validator` skill before the
   next group starts. A failed artifact is re-run, not skipped.
3. The `validator` agent checks the quality gates below. On a failure the
   coordinator finds the owning agent, re-runs only that agent and the
   artifacts that depend on it, then validates again. Max 3 retries per
   gate. After that dependent work stops and the failure is reported.
4. `html-builder` runs only after the plan was approved by the user.
   Approval is recorded by a script and verified by a hook, not by the
   model's own judgement. If the user rejects, the feedback goes to the
   affected agents and the plan is approved again.
5. Every claim about venues, prices or vendors needs a source URL found via
   web search or fetch. Weather data comes from the Open-Meteo MCP server.
   Do not rely on model memory for facts.
6. Internal artifact names (`venue.md`, `workflow-state.json`, ...) must not
   appear in text shown to the user.

## Quality gates

- G1 Budget total is within the user's limit.
- G2 Venue capacity covers the guest count.
- G3 Dietary restrictions are covered by the catering plan.
- G4 Program fits into the event time window.
- G5 Outdoor events have a rain fallback.
- G6 No duplicate vendors or venues.
- G7 Every recommendation links to a real source page.

## State and runs

Each run lives in `runs/<run-id>/`:

- `input.md` the original request
- `artifacts/` the markdown artifacts listed above
- `workflow-state.json` stage statuses, retries, approval

State is updated automatically whenever an artifact is written. On resume
the coordinator reads the state, skips completed stages and continues
with the first stage that is pending or failed.

Artifact layout is described in `docs/artifacts.md`, state format in `docs/state.md`.
