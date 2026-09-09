# ledger

A thin **append-only** SQLite record across production runs. Not a state machine
— a durable paper trail, per the v3.0 DOC-02 / DOC-08 intent.

## Records

| Event | Fields (indicative) |
|---|---|
| `run_started` | run_id, subject_id, pipeline, timestamp |
| `checkpoint` | run_id, gate (1/2), stage, decision (approve / revise / reject), note, who |
| `cost` | run_id, provider, tool, units, usd, running_total |
| `provider_call` | run_id, provider, model, purpose, outcome |
| `artifact` | run_id, stage, artifact_type, path, schema_valid |
| `published` | run_id, platform, platform_id, url, timestamp |
| `metric_pull` | run_id, platform, metric, value, pulled_at  — or `METRICS_MISSING` |

## Rules

- Append only. No row is ever updated or deleted.
- Every openmontage run gets a `run_started` and, on completion, a terminal event.
- A failed metrics pull writes `METRICS_MISSING`, never a silent blank (v3.0 invariant).
- The DB file (`*.sqlite`) is gitignored — it holds run history, not structure.
  The schema lives here in version control.
