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
| weather | `weather.md` | requirements |
| catering-planner | `catering.md` | requirements, venue, weather |
| program-planner | `program.md` | requirements, venue, weather |
| services-planner | `services.md` | requirements, venue, weather |
| guest-checklist-planner | `checklist.md` | requirements, venue, weather, catering, program |
| budget-aggregator | `budget.md` | requirements, venue, catering, program, services |
| validator | `validation.md` | all artifacts |
| plan-builder | `event-plan.md` | all validated artifacts |
| html-builder | `event-plan.html` | approved `event-plan.md`, skill `event-html-theme-builder` |

## Execution rules

The coordinator is `.claude/commands/plan-event.md`. It follows these
steps and the rules below.

1. Create the run (`scripts/state.py init runs/<run-id>`), or resume an
   existing one.
2. Requirements: run `requirements-formalizer`. If it reports missing
   fields, ask them in one batch, then run it again. Planning does not
   start until the user confirmed the requirements.
3. Groups A, B and C in order. Agents inside a group run in parallel,
   groups run sequentially.
4. After each group check every new artifact with the `artifact-validator`
   skill (`.claude/skills/artifact-validator/`). A failed artifact is
   re-run by its owner, not skipped, up to 3 attempts.
5. Run `validator`. Map each failed gate to its owner and re-run only
   the owners and the stages that became `stale` because of it, in group
   order, then validate again. Max 3 retries per gate. If a gate still
   fails, stop, mark the stage `failed` and report it. Nothing that
   depends on it runs.
6. Run `plan-builder`, ask the user to approve the plan, then
   `html-builder`. Approval is recorded by `scripts/approve.py` and
   verified by a hook, not by the model's own judgement. If the user
   rejects, the feedback goes to `plan-builder` (presentation) or to the
   owning agents (content), the stale stages are re-run, gates are
   checked again and the new plan is submitted for approval.

Rules:

- The coordinator writes no event content, it only delegates, validates
  and tracks state.
- Every claim about venues, prices or vendors needs a source URL found via
  web search or fetch. Weather data comes from the Open-Meteo MCP server
  (`.mcp.json`; tools `geocoding`, `weather_forecast`, `weather_archive`).
  Do not rely on model memory for facts.
- Internal names must not reach the user. A leak is any artifact file
  name (`venue.md`, `budget.md`, ...), `workflow-state.json` or a
  `runs/<run-id>/artifacts` path. Refer to artifacts in plain words
  ("the venue shortlist"). `no-leak-guard` blocks `AskUserQuestion`
  calls and writes of `event-plan.html` that contain such names.
- `approval-gate-guard` blocks writing `runs/<run-id>/event-plan.html`
  unless the state says `approved` and the approved hash matches the
  current plan. The hash is computed from the plan file, so editing the
  state by hand does not help.

## Failure mapping

| Failed gate | Owner (from the validator's finding) | Re-generated afterwards |
|---|---|---|
| G1 budget over limit | owner of the largest cost line, usually catering or venue | budget, checklist, validator |
| G2 capacity | venue-planner | everything in groups B and C |
| G3 dietary | catering-planner | budget, checklist |
| G4 time window | program-planner | checklist, budget |
| G5 rain fallback | program-planner | checklist |
| G6 duplicates | the artifact that repeats the vendor | budget |
| G7 sources | the artifact that cites the bad link | its dependents |

Dependents are not listed by hand: when an artifact is rewritten its hash
changes, the hook marks `done` stages that depend on it as `stale`, and
the coordinator re-runs every `stale` stage.

## Quality gates

- G1 Budget total is within the user's limit.
- G2 Venue capacity covers the guest count.
- G3 Dietary restrictions are covered by the catering plan.
- G4 Program fits into the event time window.
- G5 Outdoor events have a rain fallback.
- G6 No duplicate vendors or venues.
- G7 Every recommendation links to a real source page.

The `validator` agent runs all gates and names the owning agent for every
failure. For G1, G6 and G7 the owner depends on the finding, for example
the artifact with the largest cost line.

## State and runs

Each run lives in `runs/<run-id>/`:

- `input.md` the original request
- `artifacts/` the markdown artifacts listed above
- `workflow-state.json` stage statuses, retries, approval

State is updated automatically whenever an artifact is written. On resume
the coordinator reads the state, skips completed stages and continues
with the first stage that is pending or failed.

Artifact layout is described in `docs/artifacts.md`, state format in `docs/state.md`.
