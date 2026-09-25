from __future__ import annotations

from typing import Any, Iterable

from .models import Observation
from .outliers import ClassificationPolicy, enrich_observation


def _require_text(name: str, value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{name} must not be blank")
    return cleaned


def _require_items(name: str, values: Iterable[str]) -> list[str]:
    cleaned = [value.strip() for value in values if value and value.strip()]
    if not cleaned:
        raise ValueError(f"{name} must contain at least one non-blank item")
    return cleaned


def build_opportunity_record(
    *,
    opportunity_id: str,
    market: str,
    topic: str,
    observations: Iterable[Observation],
    original_contribution: str,
    titles: Iterable[str],
    thumbnails: Iterable[str],
    core_promise: str,
    audience: str | None = None,
    desired_outcome: str | None = None,
    perceived_problem: str | None = None,
    mechanism: str | None = None,
    awareness: str | None = None,
    curiosity_gap: str | None = None,
    expected_payoff: str | None = None,
    source_dependency_pass: bool | None = None,
    policy: ClassificationPolicy | None = None,
) -> dict[str, Any]:
    enriched = [enrich_observation(item, policy) for item in observations]

    counts = {key: 0 for key in ("winner", "failure", "comparator", "context")}
    for item in enriched:
        counts[item.classification or "context"] += 1

    winner_channels = {
        item.channel_id or item.channel
        for item in enriched
        if item.classification == "winner" and (item.channel_id or item.channel)
    }
    known_outliers = [
        item.outlier_multiple
        for item in enriched
        if item.outlier_multiple is not None
    ]
    missing_baseline = sum(
        1
        for item in enriched
        if item.channel_baseline_views in (None, 0)
    )

    evidence = [
        {
            "source_url": item.source_url,
            "platform": item.platform,
            "video_id": item.video_id,
            "channel": item.channel,
            "views": item.views,
            "channel_baseline_views": item.channel_baseline_views,
            "outlier_multiple": item.outlier_multiple,
            "classification": item.classification,
            "confidence": item.confidence,
            "notes": item.notes,
        }
        for item in enriched
    ]

    return {
        "id": _require_text("opportunity_id", opportunity_id),
        "market": _require_text("market", market),
        "topic": _require_text("topic", topic),
        "audience": audience,
        "desired_outcome": desired_outcome,
        "perceived_problem": perceived_problem,
        "mechanism": mechanism,
        "awareness": awareness,
        "status": "AWAITING_PRODUCTION_DECISION",
        "evidence": evidence,
        "evidence_summary": {
            "total": len(enriched),
            "winners": counts["winner"],
            "failures": counts["failure"],
            "comparators": counts["comparator"],
            "context": counts["context"],
            "unique_winner_channels": len(winner_channels),
            "observations_missing_baseline": missing_baseline,
            "max_outlier_multiple": max(known_outliers) if known_outliers else None,
        },
        "original_contribution": _require_text(
            "original_contribution",
            original_contribution,
        ),
        "source_dependency_pass": source_dependency_pass,
        "scores": {},
        "packaging": {
            "titles": _require_items("titles", titles),
            "thumbnails": _require_items("thumbnails", thumbnails),
            "core_promise": _require_text("core_promise", core_promise),
            "curiosity_gap": curiosity_gap,
            "expected_payoff": expected_payoff,
        },
        "gate0": {
            "decision": "RESEARCH_MORE",
            "decided_by": None,
            "decided_at": None,
            "notes": "Default state until a human reviews the decision packet.",
        },
    }
