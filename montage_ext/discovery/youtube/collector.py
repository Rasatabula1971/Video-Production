from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from ..models import Observation
from .baseline import BaselineVideo, compute_channel_baseline
from .client import YouTubeDataClient
from .duration import parse_iso8601_duration_seconds


def _int_or_none(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _video_map(items: Iterable[dict]) -> dict[str, dict]:
    return {item.get("id"): item for item in items if item.get("id")}


def collect_seed_observations(
    *,
    client: YouTubeDataClient,
    seed_topic: str,
    max_results: int = 25,
    baseline_pool_size: int = 25,
    baseline_min_age_days: int = 7,
    min_same_bucket_samples: int = 5,
    short_max_seconds: float = 180.0,
) -> list[Observation]:
    if not seed_topic.strip():
        raise ValueError("seed_topic must not be blank")

    search_items = client.search_videos(seed_topic, max_results=max_results)
    candidate_ids = [
        item.get("id", {}).get("videoId")
        for item in search_items
        if item.get("id", {}).get("videoId")
    ]
    candidates = client.videos(candidate_ids)
    candidate_map = _video_map(candidates)

    channel_ids = [
        item.get("snippet", {}).get("channelId")
        for item in candidates
        if item.get("snippet", {}).get("channelId")
    ]
    channels = {
        item.get("id"): item
        for item in client.channels(channel_ids)
        if item.get("id")
    }

    uploads_by_channel: dict[str, list[str]] = {}
    all_baseline_ids: list[str] = []
    for channel_id, channel in channels.items():
        uploads = (
            channel.get("contentDetails", {})
            .get("relatedPlaylists", {})
            .get("uploads")
        )
        ids = client.playlist_video_ids(uploads, max_results=baseline_pool_size) if uploads else []
        uploads_by_channel[channel_id] = ids
        all_baseline_ids.extend(ids)

    baseline_details = _video_map(client.videos(all_baseline_ids))
    collected_at = datetime.now(timezone.utc).isoformat()

    observations: list[Observation] = []
    for candidate_id in candidate_ids:
        item = candidate_map.get(candidate_id)
        if not item:
            continue

        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        content = item.get("contentDetails", {})
        channel_id = snippet.get("channelId")
        channel = channels.get(channel_id, {})

        duration_seconds = parse_iso8601_duration_seconds(content.get("duration"))
        baseline_videos: list[BaselineVideo] = []
        for baseline_id in uploads_by_channel.get(channel_id, []):
            baseline_item = baseline_details.get(baseline_id)
            if not baseline_item:
                continue
            base_snippet = baseline_item.get("snippet", {})
            base_stats = baseline_item.get("statistics", {})
            views = _int_or_none(base_stats.get("viewCount"))
            if views is None:
                continue
            baseline_videos.append(
                BaselineVideo(
                    video_id=baseline_id,
                    views=views,
                    duration_seconds=parse_iso8601_duration_seconds(
                        baseline_item.get("contentDetails", {}).get("duration")
                    ),
                    published_at=base_snippet.get("publishedAt"),
                )
            )

        baseline = compute_channel_baseline(
            candidate_video_id=candidate_id,
            candidate_duration_seconds=duration_seconds,
            videos=baseline_videos,
            min_age_days=baseline_min_age_days,
            min_same_bucket_samples=min_same_bucket_samples,
            short_max_seconds=short_max_seconds,
        )

        channel_title = snippet.get("channelTitle") or channel.get("snippet", {}).get("title")
        observations.append(
            Observation(
                id=f"youtube:{candidate_id}",
                source_url=f"https://www.youtube.com/watch?v={candidate_id}",
                platform="youtube",
                title=snippet.get("title") or candidate_id,
                video_id=candidate_id,
                channel_id=channel_id,
                channel=channel_title,
                published_at=snippet.get("publishedAt"),
                views=_int_or_none(statistics.get("viewCount")),
                channel_baseline_views=baseline.median_views,
                channel_baseline_sample_size=baseline.sample_size,
                channel_baseline_method=baseline.method,
                duration_seconds=duration_seconds,
                topic=seed_topic,
                collected_at=collected_at,
                notes=(
                    f"baseline_bucket={baseline.candidate_bucket or 'unknown'}; "
                    f"baseline_pool={len(baseline_videos)}"
                ),
            )
        )

    return observations
