from __future__ import annotations

import re

_DURATION_RE = re.compile(
    r"^P"
    r"(?:(?P<days>\d+)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+)H)?"
    r"(?:(?P<minutes>\d+)M)?"
    r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?"
    r")?$"
)


def parse_iso8601_duration_seconds(value: str | None) -> float | None:
    if not value:
        return None
    match = _DURATION_RE.match(value)
    if not match:
        return None
    parts = {name: float(number or 0) for name, number in match.groupdict().items()}
    return (
        parts["days"] * 86400
        + parts["hours"] * 3600
        + parts["minutes"] * 60
        + parts["seconds"]
    )


def duration_bucket(seconds: float | None, short_max_seconds: float = 180.0) -> str | None:
    if seconds is None:
        return None
    if seconds < 0:
        raise ValueError("seconds must be >= 0")
    return "short" if seconds <= short_max_seconds else "long"
