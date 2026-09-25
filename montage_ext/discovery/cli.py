from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .decision_packet import render_gate0_packet
from .models import Observation
from .outliers import enrich_observation


def _load_json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m montage_ext.discovery",
        description="Deterministic Discovery Engine v1 utilities.",
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

    args = parser.parse_args(argv)
    if args.command == "classify":
        return _cmd_classify(args.path)
    if args.command == "packet":
        return _cmd_packet(args.path)

    parser.error("unknown command")
    return 2
