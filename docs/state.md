# Workflow state

Each run keeps its progress in `runs/<run-id>/workflow-state.json`.
The file is updated by `scripts/` helpers and the post-write hook, never
by hand. It lets a run continue after an interruption without redoing
finished work.

## Fields

| Field | Meaning |
|---|---|
| `run_id` | Folder name of the run, `<date>-<slug>`, for example `2026-10-25-birthday-warsaw` |
| `created_at`, `updated_at` | ISO timestamps |
| `requirements_confirmed` | `true` after the user confirmed the requirements, set with `state.py confirm`. Resume does not ask again |
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
  "hash": "sha256 of the artifact file",
  "depends_on": ["requirements-formalizer"],
  "updated_at": "2026-10-12T10:15:00Z"
}
```

`status` is one of `pending`, `running`, `done`, `failed`, `stale`.
`stale` means the artifact exists but an upstream artifact changed after
it was written, so it must be regenerated.

The post-write hook sets the stage to `done` when the written artifact has
`Status: final` (or is the final HTML) and to `running` otherwise. It stores the file `hash` and
counts `attempts`. If the hash of an existing artifact changes, every
`done` stage that depends on it, directly or not, becomes `stale`.

### gates

```json
"G3": { "status": "fail", "owner": "catering-planner", "retries": 1 }
```

`owner` comes from the validator's finding. G1, G6 and G7 have no fixed
owner: a budget overrun is fixed by whoever owns the expensive line, a
duplicate by the artifact that repeats the vendor, a broken link by the
artifact that cites it.

`status` is `pending`, `pass` or `fail`. `retries` counts re-runs caused
by this gate and is changed with `scripts/state.py gate`. At 3 the run
stops and the failure is reported.

### approval

```json
"approval": {
  "status": "approved",
  "plan_hash": "sha256 of event-plan.md",
  "approved_at": "2026-10-12T11:02:00Z",
  "feedback": null
}
```

`status` is `none`, `approved` or `rejected`. `scripts/approve.py` records
the decision and refuses to approve while a gate has not passed.
Approval is only valid while `plan_hash` matches the current
`event-plan.md`. When the plan is rewritten the post-write hook resets the
approval to `none`, so a revised plan always needs a new approval. A
rejection keeps the user's `feedback` until the plan is rewritten.

## Resume

1. Read `workflow-state.json`.
2. Skip stages with `done`.
3. Run stages with `pending`, `failed` or `stale`, in group order.
4. Stages that depend on a re-run stage are marked `stale` first.
