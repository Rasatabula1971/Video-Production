# Discovery engine

Pre-production demand validation for the Video-Production control plane.

This module sits **before** the existing OpenMontage research/proposal pipeline. It answers: *is this opportunity strong enough to justify entering production?*

## Current v1 implementation

Discovery Engine v1 is deliberately deterministic. It does not crawl platforms or let an LLM approve production.

Implemented:

- normalized `Observation` model
- `observation.schema.json`
- null-safe outlier calculation
- deterministic evidence classification
- winner/failure comparison records
- opportunity record builder
- Gate 0 Markdown decision packet
- CLI utilities
- unit tests + GitHub Actions workflow

## Inputs

- market / niche
- target audience hypothesis
- seed topics
- collected platform evidence

## Outputs

- normalized observations
- evidence classifications: `winner | failure | comparator | context`
- winner/failure comparison records
- `opportunity_record.json`
- human-readable Gate 0 packet
- Gate 0 decision: `PRODUCE | RESEARCH_MORE | REFRAME | REJECT`

## Classification policy

Default deterministic thresholds:

```text
winner:    outlier_multiple >= 10.0
failure:   outlier_multiple <= 0.5
comparator: between those thresholds
context:   no defensible baseline / insufficient relative-performance data
```

```text
outlier_multiple = video_views / channel_baseline_views
```

If the baseline is missing or zero, the outlier is unknown rather than invented.

These thresholds are configurable heuristics, not claims that a video will succeed.

## CLI

Classify a JSON array of observations:

```bash
python -m montage_ext.discovery classify observations.json
```

Render a Gate 0 packet from an opportunity record:

```bash
python -m montage_ext.discovery packet opportunity.json
```

## Tests

```bash
python -m unittest discover -s montage_ext/discovery/tests -v
```

GitHub Actions runs the same deterministic tests whenever Discovery Engine files change.

## Non-goals

- Do not copy successful videos.
- Do not infer unavailable platform metrics.
- Do not treat view count alone as proof of demand.
- Do not automatically approve production from a score.
- Do not modify `vendor/openmontage/`.
- Do not add autonomous crawling until the evidence model proves useful on real data.

## Next step

Feed real YouTube observations into v1 and inspect whether the winner/failure comparisons and Gate 0 packets are decision-useful. Only after that should we automate discovery collection.

See `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md`.
