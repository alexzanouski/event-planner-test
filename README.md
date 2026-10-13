# Event Planner Workflow

An agentic workflow for Claude Code that turns a free-form event request
into a validated, human-approved event plan delivered as a standalone HTML page.

Invoked with a custom slash command: `/plan-event <request>`.

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) with a logged-in
  account or `ANTHROPIC_API_KEY`
- Node.js 22 or later (the Open-Meteo MCP server runs through `npx`)
- Python 3 (state script and hooks, standard library only)

## MCP servers

`.mcp.json` registers one server:

| Server | Used by | Notes |
|---|---|---|
| [open-meteo](https://github.com/cmer81/open-meteo-mcp) | `weather` agent | No API key. Pinned to `2.5.2` |

On the first run Claude Code asks to approve the project MCP server.

## Run

Start Claude Code in the repository root and approve the project MCP
server and hooks on first start:

```bash
claude
```

Then:

```
/plan-event Birthday party for 20 guests in Warsaw on 2026-10-25, 16:00-22:00, budget 2000 EUR, 3 vegetarians, photographer needed
```

The command asks the missing questions in one batch, confirms the
requirements, runs the agents and creates `runs/<run-id>/`. Resume and
approval are described below once they land.

## Repository layout

| Path | Purpose |
|---|---|
| `.claude/agents/` | Subagent definitions |
| `.claude/skills/` | Reusable skills |
| `.claude/commands/` | Slash commands (coordinator) |
| `.claude/hooks/` | PreToolUse / PostToolUse hook scripts |
| `.claude/settings.json` | Hook registration |
| `scripts/` | `state.py` (init, show, update run state), approval script later |
| `docs/` | Artifact and state conventions |
| `templates/` | Artifact and HTML templates |
| `runs/` | Persisted sample runs: inputs, artifacts, state |

## Secrets

No secrets are committed. See `.env.example` for the variables the workflow
may use; copy it to `.env` locally (ignored by git).
