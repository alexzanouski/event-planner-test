# Workflow state

Each run keeps its progress in `runs/<run-id>/workflow-state.json`.
The file is updated by `scripts/` helpers and the post-write hook, never
by hand. It lets a run continue after an interruption without redoing
finished work.

## Fields

| Field | Meaning |
|---|---|
| `run_id` | Folder name of the run |
| `created_at`, `updated_at` | ISO timestamps |
| `stages` | One entry per agent, see below |
| `gates` | Result and retry count per quality gate |
| `approval` | Human approval of the event plan |

### stages

Keyed by agent name:

```json
"venue-planner": {
  "group": "A",
  "status": "done",
  "artifact": "venue.md",
  "attempts": 1,
  "depends_on": ["requirements-formalizer"],
  "updated_at": "2026-10-12T10:15:00Z"
}
```

`status` is one of `pending`, `running`, `done`, `failed`, `stale`.
`stale` means the artifact exists but an upstream artifact changed after
it was written, so it must be regenerated.

### gates

```json
"G1": { "status": "fail", "owner": "budget-aggregator", "retries": 1 }
```

`status` is `pending`, `pass` or `fail`. `retries` counts re-runs caused
by this gate. At 3 the run stops and the failure is reported.

### approval

```json
"approval": {
  "status": "approved",
  "plan_hash": "sha256 of event-plan.md",
  "approved_at": "2026-10-12T11:02:00Z",
  "feedback": null
}
```

`status` is `none`, `pending`, `approved` or `rejected`. Approval is only
valid while `plan_hash` matches the current `event-plan.md`. Any edit to
the plan invalidates it.

## Resume

1. Read `workflow-state.json`.
2. Skip stages with `done`.
3. Run stages with `pending`, `failed` or `stale`, in group order.
4. Stages that depend on a re-run stage are marked `stale` first.
