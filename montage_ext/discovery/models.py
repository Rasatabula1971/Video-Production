from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Classification = Literal["winner", "failure", "comparator", "context"]


@dataclass(frozen=True, slots=True)
class Observation:
    id: str
    source_url: str
    platform: str
    title: str
    video_id: str | None = None
    channel_id: str | None = None
    channel: str | None = None
    published_at: str | None = None
    views: int | None = None
    channel_baseline_views: float | None = None
    outlier_multiple: float | None = None
    duration_seconds: float | None = None
    topic: str | None = None
    format: str | None = None
    promise: str | None = None
    hook: str | None = None
    classification: Classification | None = None
    confidence: float | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id must not be blank")
        if not self.source_url.strip():
            raise ValueError("source_url must not be blank")
        if not self.platform.strip():
            raise ValueError("platform must not be blank")
        if not self.title.strip():
            raise ValueError("title must not be blank")

        for name in ("views", "channel_baseline_views", "outlier_multiple", "duration_seconds"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be >= 0")

        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Observation":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
