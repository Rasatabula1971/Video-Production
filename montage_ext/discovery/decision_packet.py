from __future__ import annotations

from typing import Any


def _fmt(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def render_gate0_packet(record: dict[str, Any]) -> str:
    summary = record.get("evidence_summary", {})
    packaging = record.get("packaging", {})
    evidence = list(record.get("evidence", []))

    lines = [
        f"# Gate 0 Decision Packet — {record.get('topic', 'Untitled opportunity')}",
        "",
        f"**Opportunity ID:** {record.get('id', 'unknown')}",
        f"**Market:** {record.get('market', 'unknown')}",
        f"**Audience:** {record.get('audience') or 'not specified'}",
        "",
        "## Evidence summary",
        "",
        f"- Observations: {_fmt(summary.get('total'))}",
        f"- Winners: {_fmt(summary.get('winners'))}",
        f"- Failures: {_fmt(summary.get('failures'))}",
        f"- Comparators: {_fmt(summary.get('comparators'))}",
        f"- Context-only: {_fmt(summary.get('context'))}",
        f"- Unique winner channels: {_fmt(summary.get('unique_winner_channels'))}",
        f"- Missing/zero channel baselines: {_fmt(summary.get('observations_missing_baseline'))}",
        f"- Maximum observed outlier multiple: {_fmt(summary.get('max_outlier_multiple'))}",
        "",
        "## Original contribution",
        "",
        record.get("original_contribution") or "Not supplied.",
        "",
        "## Source dependency test",
        "",
        (
            "PASS"
            if record.get("source_dependency_pass") is True
            else "FAIL"
            if record.get("source_dependency_pass") is False
            else "NOT YET REVIEWED"
        ),
        "",
        "## Packaging hypotheses",
        "",
        f"**Core promise:** {packaging.get('core_promise') or 'not supplied'}",
        "",
        "**Titles**",
    ]

    for title in packaging.get("titles", []):
        lines.append(f"- {title}")

    lines.extend(["", "**Thumbnail concepts**"])
    for thumbnail in packaging.get("thumbnails", []):
        lines.append(f"- {thumbnail}")

    lines.extend(["", "## Strongest evidence", ""])
    ranked = sorted(
        evidence,
        key=lambda item: (
            item.get("outlier_multiple") is not None,
            item.get("outlier_multiple") or 0,
        ),
        reverse=True,
    )[:10]

    if not ranked:
        lines.append("- No evidence attached.")
    else:
        for item in ranked:
            lines.append(
                "- "
                f"[{item.get('classification', 'context')}] "
                f"{item.get('channel') or 'unknown channel'} — "
                f"views={_fmt(item.get('views'))}, "
                f"outlier={_fmt(item.get('outlier_multiple'))}x — "
                f"{item.get('source_url')}"
            )

    lines.extend(
        [
            "",
            "## Human decision",
            "",
            "Choose exactly one: **PRODUCE / RESEARCH_MORE / REFRAME / REJECT**",
            "",
            f"Current stored decision: **{record.get('gate0', {}).get('decision', 'RESEARCH_MORE')}**",
        ]
    )
    return "\n".join(lines) + "\n"
