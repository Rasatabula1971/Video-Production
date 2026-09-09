# publishers/youtube_shorts

The v2.2 measurement loop that openmontage lacks. openmontage's `publish` stage
only writes an export bundle; this takes it the rest of the way.

## 1. Publish handoff
- Input: openmontage export bundle (video, metadata, thumbnail concept).
- YouTube Data API v3 upload (**free**). Shorts metadata: title, description,
  hashtags, chapters, required CC attributions from `montage_ext` provenance.
- Human confirms at Gate 2 before the upload call. Scheduled or immediate.
- Idempotency key per bundle — a timed-out upload reconciles, never double-posts.

## 2. Metrics retrieval
- Scheduled pulls, YouTube Analytics API (**free**): impressions, stop-rate
  proxy (swipe-away first 3s), average % viewed, completion, rewatches, shares,
  saves, comments, followers gained, non-follower reach, estimated target-market %.
- A failed pull → `METRICS_MISSING` in the ledger, never a silent blank.

## 3. Learning store
- Each published item's `hook_type`, `structure`, `pillar`, `duration` → outcome.
- Feeds the next run's decision engine: which hooks and structures actually reach
  the target audience, not which get the most raw views.

## Later
TikTok and Instagram Reels adapters implement the same three-part interface.
Auth tokens (`.youtube-token.json` etc.) are gitignored.
