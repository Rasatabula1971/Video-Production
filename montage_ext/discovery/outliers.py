from __future__ import annotations

from dataclasses import dataclass, replace

from .models import Classification, Observation


@dataclass(frozen=True, slots=True)
class ClassificationPolicy:
    winner_outlier_min: float = 10.0
    failure_outlier_max: float = 0.5

    def __post_init__(self) -> None:
        if self.winner_outlier_min <= 0:
            raise ValueError("winner_outlier_min must be > 0")
        if self.failure_outlier_max < 0:
            raise ValueError("failure_outlier_max must be >= 0")
        if self.failure_outlier_max >= self.winner_outlier_min:
            raise ValueError("failure_outlier_max must be less than winner_outlier_min")


def calculate_outlier_multiple(
    video_views: int | float | None,
    channel_baseline_views: int | float | None,
) -> float | None:
    if video_views is None or channel_baseline_views is None:
        return None
    if video_views < 0:
        raise ValueError("video_views must be >= 0")
    if channel_baseline_views < 0:
        raise ValueError("channel_baseline_views must be >= 0")
    if channel_baseline_views == 0:
        return None
    return float(video_views) / float(channel_baseline_views)


def classify_observation(
    observation: Observation,
    policy: ClassificationPolicy | None = None,
) -> Classification:
    if observation.classification is not None:
        return observation.classification

    policy = policy or ClassificationPolicy()
    multiple = observation.outlier_multiple
    if multiple is None:
        multiple = calculate_outlier_multiple(
            observation.views,
            observation.channel_baseline_views,
        )

    if multiple is None:
        return "context"
    if multiple >= policy.winner_outlier_min:
        return "winner"
    if multiple <= policy.failure_outlier_max:
        return "failure"
    return "comparator"


def enrich_observation(
    observation: Observation,
    policy: ClassificationPolicy | None = None,
) -> Observation:
    multiple = observation.outlier_multiple
    if multiple is None:
        multiple = calculate_outlier_multiple(
            observation.views,
            observation.channel_baseline_views,
        )
    classification = classify_observation(observation, policy)
    return replace(
        observation,
        outlier_multiple=multiple,
        classification=classification,
    )
