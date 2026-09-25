# Discovery engine

Pre-production demand validation for the Video-Production control plane.

This module sits **before** the existing OpenMontage research/proposal pipeline. It answers a different question: *is this opportunity strong enough to justify entering production?*

## Inputs

- market / niche
- target audience hypothesis
- seed topics
- collected platform evidence

## Outputs

- `discovery_record.json` - normalized observations
- `opportunity_record.json` - evidence-backed opportunity hypothesis
- `package_record.json` - title/thumbnail/promise candidates
- Gate 0 decision: `PRODUCE | RESEARCH_MORE | REFRAME | REJECT`

## Non-goals

- Do not copy successful videos.
- Do not infer unavailable platform metrics.
- Do not treat view count alone as proof of demand.
- Do not automatically approve production from a score.
- Do not modify `vendor/openmontage/`.

## Initial deterministic metric

```text
outlier_multiple = video_views / channel_baseline_views
```

Return null when a defensible baseline is unavailable or zero.

## Evidence quality

Every derived conclusion should retain links to the observations that support it. Missing data and uncertainty are first-class fields.

See `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md`.
