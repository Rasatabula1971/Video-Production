# Automotive performance — Discovery Engine live trial

This project is the first live-data validation of the generic Discovery Engine.

The system should **discover** the strongest opportunities. The seed list is intentionally broad and does not preselect a final video.

## Market

Car performance / automotive engineering explained.

## Initial seeds

See `seeds.json`.

## Run

Set a YouTube Data API v3 key locally:

```text
YOUTUBE_API_KEY=...
```

Then collect one seed first:

```bash
python -m montage_ext.discovery youtube-collect \
  --seed "turbo lag explained" \
  --output projects/discovery-automotive-performance/observations-turbo-lag.json
```

After validating one seed, batch the seed list. Keep raw observations and derived classifications separate so we can audit how Gate 0 conclusions were reached.

## Success criterion

The trial is useful only if the final Gate 0 packet gives a human reviewer better evidence for choosing a video opportunity than simply browsing high-view videos manually.
