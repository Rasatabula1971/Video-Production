from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import Observation
from .outliers import ClassificationPolicy, enrich_observation


@dataclass(frozen=True, slots=True)
class ComparisonRecord:
    winner_id: str
    failure_id: str
    topic_match: bool
    format_match: bool
    same_channel: bool
    outlier_gap: float | None
    views_ratio: float | None


def _norm(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.casefold().split())
    return normalized or None


def _views_ratio(winner: Observation, failure: Observation) -> float | None:
    if winner.views is None or failure.views is None or failure.views == 0:
        return None
    return winner.views / failure.views


def _outlier_gap(winner: Observation, failure: Observation) -> float | None:
    if winner.outlier_multiple is None or failure.outlier_multiple is None:
        return None
    return winner.outlier_multiple - failure.outlier_multiple


def build_comparisons(
    observations: Iterable[Observation],
    policy: ClassificationPolicy | None = None,
) -> list[ComparisonRecord]:
    enriched = [enrich_observation(item, policy) for item in observations]
    winners = [item for item in enriched if item.classification == "winner"]
    failures = [item for item in enriched if item.classification == "failure"]

    records: list[ComparisonRecord] = []
    for winner in winners:
        winner_topic = _norm(winner.topic)
        if winner_topic is None:
            continue

        candidates = [
            failure
            for failure in failures
            if _norm(failure.topic) == winner_topic
        ]
        candidates.sort(
            key=lambda failure: (
                _norm(failure.format) != _norm(winner.format),
                failure.id,
            )
        )

        for failure in candidates:
            records.append(
                ComparisonRecord(
                    winner_id=winner.id,
                    failure_id=failure.id,
                    topic_match=True,
                    format_match=_norm(winner.format) == _norm(failure.format),
                    same_channel=bool(
                        winner.channel_id
                        and failure.channel_id
                        and winner.channel_id == failure.channel_id
                    ),
                    outlier_gap=_outlier_gap(winner, failure),
                    views_ratio=_views_ratio(winner, failure),
                )
            )
    return records
