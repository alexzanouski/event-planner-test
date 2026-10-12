# Event Planner Workflow

An agentic workflow for Claude Code that turns a free-form event request
into a validated, human-approved event plan delivered as a standalone HTML page.

Invoked with a custom slash command: `/plan-event <request>`.

> Status: work in progress. Setup, run and resume instructions are added
> as the workflow components land.

## Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) with a logged-in
  account or `ANTHROPIC_API_KEY`
- Node.js 22 or later (the Open-Meteo MCP server runs through `npx`)
- Python 3 (helper scripts, added in later commits)

## MCP servers

`.mcp.json` registers one server:

| Server | Used by | Notes |
|---|---|---|
| [open-meteo](https://github.com/cmer81/open-meteo-mcp) | `weather` agent | No API key. Pinned to `2.5.2` |

On the first run Claude Code asks to approve the project MCP server.

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
