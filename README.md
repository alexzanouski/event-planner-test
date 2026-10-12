# Event Planner Workflow

An agentic workflow for Claude Code that turns a free-form event request
into a validated, human-approved event plan delivered as a standalone HTML page.

Invoked with a custom slash command: `/plan-event <request>`.

> Status: work in progress. Setup, run and resume instructions are added
> as the workflow components land.

## Repository layout

| Path | Purpose |
|---|---|
| `.claude/agents/` | Subagent definitions |
| `.claude/skills/` | Reusable skills |
| `.claude/commands/` | Slash commands (coordinator) |
| `.claude/hooks/` | PreToolUse / PostToolUse hook scripts |
| `scripts/` | Helper scripts (state, approval) |
| `docs/` | Artifact and state conventions |
| `templates/` | Artifact and HTML templates |
| `runs/` | Persisted sample runs: inputs, artifacts, state |

## Secrets

No secrets are committed. See `.env.example` for the variables the workflow
may use; copy it to `.env` locally (ignored by git).
