from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from statistics import median
from typing import Iterable

from .duration import duration_bucket


@dataclass(frozen=True, slots=True)
class BaselineVideo:
    video_id: str
    views: int
    duration_seconds: float | None
    published_at: str | None


@dataclass(frozen=True, slots=True)
class BaselineResult:
    median_views: float | None
    sample_size: int
    method: str
    candidate_bucket: str | None


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def compute_channel_baseline(
    *,
    candidate_video_id: str,
    candidate_duration_seconds: float | None,
    videos: Iterable[BaselineVideo],
    min_age_days: int = 7,
    min_same_bucket_samples: int = 5,
    short_max_seconds: float = 180.0,
    now: datetime | None = None,
) -> BaselineResult:
    if min_age_days < 0:
        raise ValueError("min_age_days must be >= 0")
    if min_same_bucket_samples < 1:
        raise ValueError("min_same_bucket_samples must be >= 1")

    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    candidate_bucket = duration_bucket(candidate_duration_seconds, short_max_seconds)

    eligible: list[BaselineVideo] = []
    for video in videos:
        if video.video_id == candidate_video_id or video.views < 0:
            continue
        published = _parse_datetime(video.published_at)
        if published is not None:
            age_days = (now - published).total_seconds() / 86400
            if age_days < min_age_days:
                continue
        eligible.append(video)

    if not eligible:
        return BaselineResult(None, 0, "insufficient_data", candidate_bucket)

    same_bucket = [
        video
        for video in eligible
        if candidate_bucket is not None
        and duration_bucket(video.duration_seconds, short_max_seconds) == candidate_bucket
    ]

    chosen = same_bucket if len(same_bucket) >= min_same_bucket_samples else eligible
    method = "recent_same_duration_median" if chosen is same_bucket else "recent_channel_median"
    values = [video.views for video in chosen]

    return BaselineResult(
        median_views=float(median(values)) if values else None,
        sample_size=len(values),
        method=method,
        candidate_bucket=candidate_bucket,
    )
