# montage_ext — what we build on top of openmontage

openmontage (`vendor/openmontage/`) is the production engine. It already does
research → proposal (cost + Gate 1) → script → scene → asset → edit → compose →
publish-bundle, with checkpoints, a decision log, a cost tracker, and asset
provenance.

`montage_ext/` is the four things it does **not** do (see `docs/PLAN_v1.md` §2).
We do not edit `vendor/openmontage/` — we layer here and call into it.

| Module | Fills | Status |
|---|---|---|
| `hook_scorer/` | The hook & script scoring loop — the make-or-break gate. Scores every candidate hook + script against the v2.2 stop-rate / retention / customer-reach model + an LLM-judge panel, regenerates until it clears a bar, attaches a `hook_scorecard` to the proposal. | not started |
| `ledger/` | A thin append-only SQLite record across runs: run id, subject, every checkpoint decision, cost, provider calls, publish + metric events. Not a state machine — a durable paper trail (v3.0 DOC-02/DOC-08 intent). | not started |
| `publishers/youtube_shorts/` | Publish handoff (YouTube Data API v3, free) + scheduled metrics retrieval (YouTube Analytics API, free) + a learning store that feeds the next run's decisions. TikTok / Reels added after Shorts works, same interface. | not started |
| `brand_intake/` | The conversational brand-kit builder. Walks the 14-step Brand Building Kit sequence and writes `brands/<id>/`. See `brands/README.md`. | spec written |

Also here (later): the loader that reads `brands/<id>/` + `subjects/<id>/` and
injects the brand kit, profile, copyright rules, and fact corpus into
openmontage's `creative-intake` and `research-director` stages.

See also `docs/APP_IMPROVEMENTS.md` for the quality backlog from the first dry run.
