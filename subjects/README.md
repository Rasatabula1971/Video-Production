# subjects/

One folder per subject. **The subject varies** — steelpan is subject #1, not the
only one. Nothing outside these folders knows what any subject is.

## Adding a subject

Create `subjects/<id>/` with:

| File | What it holds |
|---|---|
| `profile.yaml` | Brand, audience, platform targets, content pillars, cadence, the metrics to pull. |
| `copyright-rules.md` | Hard rules — what may and may not appear on screen. Enforced at Gate 2, not advisory. |
| `fact-corpus/` | Vetted facts the research stage cites before the open web. |

`montage_ext/` reads the active subject folder. The engine (`vendor/openmontage/`)
and the glue code never hard-code a subject's facts, rules, or audience.

## Current subjects

- `steelpan/` — history of the Trinidad steelpan and its pioneers. Series 1.
