# Stage 2 — Experiment 01: Proven-Content Discovery

## Question
Can YouTube Data API v3 reliably produce a useful pool of already-proven videos for later transformation into original, value-added videos?

## Working hypothesis
Primary pool:
- long-form: >= 1,000,000 views
- Shorts: >= 5,000,000 views

Emerging exception:
- >= 500,000 views
- >= 10x the channel's recent comparable-video median
- strong current velocity

The thresholds are hypotheses for Stage 2, not frozen product rules.

## What this experiment does
1. Searches YouTube by niche/query using `search.list`, ordered by view count.
2. Hydrates candidates with `videos.list`.
3. Classifies Short vs long-form using duration as a practical first-pass heuristic.
4. Keeps primary-pool videos immediately.
5. For candidates >=500k that do not meet the primary threshold, fetches the channel's uploads playlist and recent uploads.
6. Calculates a median baseline from up to 10 prior comparable uploads.
7. Calculates outlier ratio, views/day and like rate.
8. Exports raw JSON plus a flat CSV for analysis.

## Important limitations
- YouTube does not expose a minimum-view search filter. The script searches first and filters locally.
- Duration is only a first-pass format classifier. Shorts identification should be validated in later research because vertical format is not directly exposed by the Data API.
- Public API statistics do not expose retention, CTR or watch time for other creators' videos.
- `viewCount` semantics changed in 2026, so raw view comparisons across periods/formats need care.
- "Strong velocity" is deliberately not hard-coded as a pass/fail rule yet. We collect views/day and will set the threshold after examining the real distribution.
- Channel baseline uses recent public uploads and excludes the candidate. It is a research proxy, not YouTube's internal recommendation baseline.

## Setup
Set `YOUTUBE_API_KEY` in your environment. No OAuth is required for these public reads.

Run:
```
python stage2/experiment_01_discovery/youtube_discovery.py --max-searches 60
```

Outputs are written to:
- `stage2/experiment_01_discovery/output/raw_results.json`
- `stage2/experiment_01_discovery/output/candidates.csv`
- `stage2/experiment_01_discovery/output/summary.json`

The output directory should remain uncommitted when it contains experiment data.

## Stage-2 decision
Do not freeze ranking weights from this experiment's code. First inspect the collected distribution and manually review a sample of candidates. The next decision is whether the 1M/5M primary thresholds and 500k+10x emerging exception actually produce commercially interesting source ideas.
