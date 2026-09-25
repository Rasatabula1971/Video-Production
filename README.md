# Video-Production

Subject-neutral video intelligence + production control plane. Market/topic in → evidence-backed production decision → published video → performance evidence out.

The system now has **three human decision points**:

- **Gate 0 — should we make this?** Demand, opportunity, originality and package are reviewed before the idea enters production.
- **Gate 1 — approve before spend.** Existing OpenMontage proposal/script controls remain in place before expensive asset generation.
- **Gate 2 — approve before publish.** Final human review remains mandatory before publication.

The subject varies. Steelpan is subject #1, not the only one. Everything subject-specific lives in `subjects/<id>/`; the engine and `montage_ext/` stay generic.

## Operating architecture

```text
DISCOVER -> PROVE -> PACKAGE -> GATE 0
        -> RESEARCH -> STORY -> GATE 1
        -> PRODUCE -> VERIFY -> GATE 2
        -> PUBLISH -> MEASURE -> LEARN
        -> next opportunity
```

The production engine is still OpenMontage. The demand-validation and learning layers are built beside it; `vendor/openmontage/` is not modified for product-specific intelligence.

## How this repo is put together

| Path | What it is |
|---|---|
| `docs/PLAN_v1.md` | Original build plan and adopted OpenMontage strategy. |
| `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md` | Current demand-validation, packaging and learning architecture. |
| `vendor/openmontage/` | Vendored production engine (AGPL-3.0). See `vendor/VENDORED.md`. |
| `subjects/steelpan/` | First Subject Package: audience, copyright rules and vetted fact corpus. |
| `brands/` | Reusable brand packages, separate from subjects. |
| `montage_ext/discovery/` | Pre-production demand evidence, opportunity records and Gate 0 contracts. |
| `montage_ext/hook_scorer/` | Hook/script quality scoring before production spend. |
| `montage_ext/ledger/` | Append-only cross-run event/decision record. |
| `montage_ext/publishers/` | Platform publishing and metrics adapters. |
| `montage_ext/learning/` | Joins opportunity hypotheses to real audience outcomes. |
| `BUILD_STATUS.md` | What is done and what is next. |

## First subject

The history of the Trinidad steelpan — its pioneers and how the instrument evolved. Culture-first launch for YouTube Shorts.

The existing steelpan dry run and free render chain remain valid. Demand validation is an additional upstream decision layer, not a replacement for the production pipeline.

## Design principles

- Evidence before production.
- Copy demonstrated demand, not another creator's video.
- Collect failures as well as winners.
- Separate topic, promise, format, hook, structure and payoff.
- Package before expensive production.
- Keep observations separate from interpretations.
- Never invent missing platform metrics.
- Human approval controls production and publishing.
- Every published video should improve the next production decision.

## Governing specs

Repository-tracked specs are the preferred source of truth for implementation. Historical local documents may contain additional background, but new architecture changes should be captured under `docs/` so the repo is self-describing.

## Licensing

This project vendors AGPL-3.0 code under `vendor/openmontage/`. See `NOTICE`.
Free / open-source components are preferred throughout; paid services are a fallback only where a free or local tool cannot do the job.
