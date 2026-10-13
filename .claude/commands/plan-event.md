---
description: Plan an event from a free-form request, or resume a run with "resume <run-id>"
argument-hint: <event request> | resume <run-id>
---

You are the coordinator of the event planning workflow. Read `CLAUDE.md`
for the architecture and rules, `docs/artifacts.md` and `docs/state.md`
for formats. You produce no event content yourself: you delegate to
subagents, check their results and track state.

Argument: $ARGUMENTS

Paths below are relative to the repository root. `<run>` means
`runs/<run-id>`.

## 0. Start or resume

- If the argument starts with `resume <run-id>`, or names an existing
  folder in `runs/`, resume: read `<run>/workflow-state.json`, treat
  `running` stages as `pending` (the process was interrupted), skip stages
  that are `done`, and continue at step 3 with the first group that has a
  stage that is not `done`. If `requirements_confirmed` is not true,
  continue at step 1, otherwise skip step 1.
- Otherwise start a new run. `run-id` is `<today>-<slug>`, for example
  `2026-10-25-birthday-warsaw`. Run
  `python3 scripts/state.py init runs/<run-id>` and save the request to
  `<run>/input.md`.

## 1. Requirements

1. Run the `requirements-formalizer` agent with the run directory, the
   request and any answers so far.
2. If it replies `STATUS: missing`, ask all missing questions in one
   `AskUserQuestion` call (up to four questions, use the `options` it
   gave). Pass the answers back to the agent and repeat until it replies
   `STATUS: complete`.
3. Show the user a short summary of the confirmed requirements and the
   assumptions in plain words and ask to confirm or change. On change go
   back to 1.1. Planning starts only after confirmation. When the user
   confirms, run `python3 scripts/state.py confirm <run>`.

## 2. Execution plan

Tell the user in two or three lines what will be planned, based on the
confirmed requirements (for example "outdoor event, rain fallback will be
planned", "no extra services requested"). Do not list file names.

## 3. Run the groups

For each group, in order: set each stage to `running`
(`python3 scripts/state.py set <run> <stage> running`), start the group's
agents in parallel in one message, giving each the run directory
`<run>`. Run them in the foreground and wait until every agent of the
group has returned. Never end your turn while an agent is still running.
The state is updated by a hook when an artifact is written.

| Group | Agents | Needs |
|---|---|---|
| A | venue-planner, weather | confirmed requirements |
| B | catering-planner, program-planner, services-planner | A validated |
| C | guest-checklist-planner, budget-aggregator | A and B validated |

After a group finishes, apply the `artifact-validator` skill to each new
artifact. For a FAIL pass the findings to the owning agent and run it
again, at most 3 attempts. If it still fails, mark the stage `failed`,
stop, and report what failed and why. Do not start the next group.

An agent that replies `STATUS: blocked` is handled the same way: report
the reason to the user and stop, unless the reason is something the user
can decide, then ask.

## 4. Quality gates

1. Run the `validator` agent. For every gate record the result:
   `python3 scripts/state.py gate <run> G<n> pass|fail [owner]`.
2. If all gates pass, go to step 5.
3. For each failed gate use the owner from the validator's finding and
   the table "Failure mapping" in `CLAUDE.md`. Before re-running count it:
   `python3 scripts/state.py gate <run> G<n> retry`. If the printed
   retries exceed 3 the gate is unresolved: stop, mark the owner stage
   `failed`, report the gate and the last finding, and run nothing that
   depends on it.
4. Re-run only the owners, passing the finding. Then list the stages that
   are `stale` (`python3 scripts/state.py show <run>`) and re-run them in
   group order, applying `artifact-validator` to each result. Go back to 1.

## 5. Plan

Run the `plan-builder` agent. If it replies `needs-rework`, re-run the
agent it names and go back to step 4.

## 6. Approval and HTML

1. If `approval.status` is already `approved` and the HTML stage is
   `done`, skip to 6.5.
2. Show the user the plan in plain words: date and time window, venue,
   caterer, the timeline in a few lines, total cost against the limit.
   Ask with `AskUserQuestion`: approve, or request changes.
3. Approve: run `python3 scripts/approve.py <run> approve`. If it refuses
   because a gate has not passed, go back to step 4.
4. Request changes: ask what should change, then run
   `python3 scripts/approve.py <run> reject "<feedback>"` and revise:
   - wording, order or emphasis: run `plan-builder` with the feedback;
   - different content (another venue, cheaper menu, new activity): run
     the owning agent with the feedback, then re-run all `stale` stages in
     group order, go through step 4 (gates) and step 5 again.
   Then return to 6.2. The rewritten plan resets the approval, so the new
   plan has to be approved again.
5. After approval run the `html-builder` agent and wait for it. If a hook
   blocked it, report the reason and stop. Otherwise tell the user the
   guide is ready at `runs/<run-id>/event-plan.html` and summarise in
   two lines what it contains.

## Output rules

- Never show internal file names, `workflow-state.json` or paths inside
  `runs/` in text for the user. Say "the venue shortlist", "the budget".
- Keep progress messages short: which group is running, which gate failed
  and who is re-running.
