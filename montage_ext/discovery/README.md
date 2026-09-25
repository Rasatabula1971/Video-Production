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
- YouTube Data API v3 evidence ingestion
- channel-baseline estimation using recent same-duration uploads when possible
- in-process caching for repeated video/channel/playlist evidence
- bounded retry/backoff for transient API failures
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

Collect live YouTube evidence for one seed topic:

```bash
# PowerShell
$env:YOUTUBE_API_KEY="your-key"

python -m montage_ext.discovery youtube-collect \
  --seed "turbo lag explained" \
  --output projects/discovery-automotive-performance/observations-turbo-lag.json
```

The API key is read only from the local environment and is never written to the observation file.

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
- Do not paginate YouTube search automatically in v1; search calls are the scarce quota bucket.
- Do not interpret the outlier multiple as causal proof. It is a discovery signal.

## Next step

Run the automotive-performance live trial under `projects/discovery-automotive-performance/`. Start with one seed, inspect the baseline and classifications, then expand across the seed list only after the evidence looks sane.

See `docs/DEMAND_VALIDATED_SYSTEM_v2_2.md`.


## YouTube baseline policy

For each search result, v1 retrieves the channel's recent upload IDs and computes a median baseline.

Preference order:

1. recent uploads in the same duration class as the candidate, when at least 5 are available;
2. otherwise, recent mature uploads across the channel;
3. if no defensible sample exists, baseline remains unknown and the observation is classified as context.

Defaults:

- short-form boundary: 180 seconds (configurable)
- recent-upload baseline pool: 25 videos
- exclude uploads younger than 7 days
- minimum same-duration sample: 5 videos

These are testable defaults, not permanent platform truths.

## YouTube quota design

The collector deliberately uses one `search.list` call per seed and then relies on lower-cost read calls plus in-process caches. Repeating the same seed/channel within one process reuses cached evidence instead of spending quota again.
