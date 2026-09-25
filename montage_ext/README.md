# montage_ext — what we build on top of OpenMontage

OpenMontage (`vendor/openmontage/`) is the production engine. It already covers research → proposal → script → scene → asset → edit → compose → publish bundle, with checkpoints, decision logging, cost tracking and asset provenance.

`montage_ext/` contains the intelligence and connective tissue that are specific to this control plane. We do not edit `vendor/openmontage/` for these features.

| Module | Role | Status |
|---|---|---|
| `discovery/` | Demand validation before production: seed research, outlier evidence, winner/failure comparison, demand clusters, opportunity record, package hypotheses and Gate 0. | contract + schema added |
| `hook_scorer/` | Hook & script scoring before production spend. | not started |
| `ledger/` | Append-only cross-run decisions, cost, provider, publish and metric events. | not started |
| `publishers/youtube_shorts/` | YouTube publish handoff + metrics retrieval. TikTok/Reels later behind the same interface. | not started |
| `learning/` | Joins discovery hypotheses, published package/content choices and measured outcomes to guide future opportunities. | contract added |
| `brand_intake/` | Conversational brand-kit builder writing `brands/<id>/`. | spec written |

## Gate model

- **Gate 0:** should we make this? Human reviews demand, originality, package, value and feasibility.
- **Gate 1:** approve before spend. Existing production approval remains authoritative.
- **Gate 2:** approve before publish. Existing final human approval remains authoritative.

Gate 0 does not replace Gate 1.

## Architecture boundary

```text
montage_ext/discovery
        |
        v
     Gate 0
        |
        v
OpenMontage production pipeline
        |
        v
publishers -> metrics -> montage_ext/learning
        ^                         |
        |_________________________|
```

See `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md` for the current architecture and `docs/PLAN_v1.md` for the original adoption/build plan.
