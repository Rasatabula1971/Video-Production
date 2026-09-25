from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Sequence

from .decision_packet import render_gate0_packet
from .models import Observation
from .outliers import enrich_observation
from .youtube.client import YouTubeDataClient
from .youtube.collector import collect_seed_observations


def _load_json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str, payload: object) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _cmd_classify(path: str) -> int:
    payload = _load_json(path)
    if not isinstance(payload, list):
        raise ValueError("classify input must be a JSON array of observations")

    enriched = [
        enrich_observation(Observation.from_dict(item)).to_dict()
        for item in payload
    ]
    print(json.dumps(enriched, indent=2, ensure_ascii=False))
    return 0


def _cmd_packet(path: str) -> int:
    payload = _load_json(path)
    if not isinstance(payload, dict):
        raise ValueError("packet input must be a JSON object")
    print(render_gate0_packet(payload), end="")
    return 0


def _cmd_youtube_collect(args: argparse.Namespace) -> int:
    api_key = os.environ.get(args.api_key_env, "").strip()
    if not api_key:
        raise RuntimeError(
            f"{args.api_key_env} is not set; provide a YouTube Data API v3 key locally"
        )

    client = YouTubeDataClient(api_key)
    observations = collect_seed_observations(
        client=client,
        seed_topic=args.seed,
        max_results=args.max_results,
        baseline_pool_size=args.baseline_pool_size,
        baseline_min_age_days=args.baseline_min_age_days,
        min_same_bucket_samples=args.min_same_bucket_samples,
        short_max_seconds=args.short_max_seconds,
    )
    enriched = [enrich_observation(item).to_dict() for item in observations]
    _write_json(args.output, enriched)

    print(
        "Collected "
        f"{len(enriched)} observations to {args.output}; "
        f"API calls={dict(sorted(client.call_counts.items()))}"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m montage_ext.discovery",
        description="Deterministic Discovery Engine utilities.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    classify = sub.add_parser(
        "classify",
        help="derive outlier multiples and evidence classifications",
    )
    classify.add_argument("path")

    packet = sub.add_parser(
        "packet",
        help="render a Gate 0 Markdown decision packet",
    )
    packet.add_argument("path")

    youtube = sub.add_parser(
        "youtube-collect",
        help="collect live YouTube evidence for one seed topic",
    )
    youtube.add_argument("--seed", required=True)
    youtube.add_argument("--output", required=True)
    youtube.add_argument("--max-results", type=int, default=25)
    youtube.add_argument("--baseline-pool-size", type=int, default=25)
    youtube.add_argument("--baseline-min-age-days", type=int, default=7)
    youtube.add_argument("--min-same-bucket-samples", type=int, default=5)
    youtube.add_argument("--short-max-seconds", type=float, default=180.0)
    youtube.add_argument("--api-key-env", default="YOUTUBE_API_KEY")

    args = parser.parse_args(argv)
    if args.command == "classify":
        return _cmd_classify(args.path)
    if args.command == "packet":
        return _cmd_packet(args.path)
    if args.command == "youtube-collect":
        return _cmd_youtube_collect(args)

    parser.error("unknown command")
    return 2
