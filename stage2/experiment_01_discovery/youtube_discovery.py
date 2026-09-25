"""Stage 2 Experiment 01: discover proven YouTube content.

Standard library only. Requires a YouTube Data API v3 key in YOUTUBE_API_KEY.
This is a research tool, not production architecture.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE = "https://www.googleapis.com/youtube/v3"
HERE = Path(__file__).resolve().parent
LONG_MIN = 1_000_000
SHORT_MIN = 5_000_000
EMERGING_MIN = 500_000
EMERGING_OUTLIER = 10.0


def api_get(resource: str, key: str, **params: Any) -> dict[str, Any]:
    params["key"] = key
    url = f"{BASE}/{resource}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Video-Production-Stage2/1.0"})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(last_error)


def parse_duration_seconds(value: str) -> int:
    # ISO-8601 subset used by YouTube durations: PT#H#M#S.
    import re
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not match:
        return 0
    h, m, s = (int(x or 0) for x in match.groups())
    return h * 3600 + m * 60 + s


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def days_old(published_at: str) -> float:
    delta = datetime.now(timezone.utc) - parse_time(published_at)
    return max(delta.total_seconds() / 86400.0, 1 / 24)


def chunks(values: list[str], size: int = 50):
    for i in range(0, len(values), size):
        yield values[i:i + size]


def video_details(ids: list[str], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for batch in chunks(list(dict.fromkeys(ids))):
        data = api_get("videos", key, part="snippet,statistics,contentDetails", id=",".join(batch), maxResults=50)
        for item in data.get("items", []):
            out[item["id"]] = item
    return out


def channel_details(ids: list[str], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for batch in chunks(list(dict.fromkeys(ids))):
        data = api_get("channels", key, part="snippet,statistics,contentDetails", id=",".join(batch), maxResults=50)
        for item in data.get("items", []):
            out[item["id"]] = item
    return out


def recent_upload_ids(channel: dict[str, Any], key: str, max_results: int = 25) -> list[str]:
    uploads = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if not uploads:
        return []
    data = api_get("playlistItems", key, part="contentDetails", playlistId=uploads, maxResults=min(max_results, 50))
    return [x["contentDetails"]["videoId"] for x in data.get("items", []) if x.get("contentDetails", {}).get("videoId")]


def classify_format(seconds: int) -> str:
    # Research heuristic only. Duration alone does not prove a video is a Short.
    return "short_candidate" if 0 < seconds <= 180 else "long_form"


def comparable_baseline(candidate: dict[str, Any], history: list[dict[str, Any]]) -> tuple[float | None, int]:
    cand_id = candidate["video_id"]
    cand_format = candidate["format"]
    comparable = [
        int(v["statistics"].get("viewCount", 0))
        for v in history
        if v["id"] != cand_id
        and classify_format(parse_duration_seconds(v.get("contentDetails", {}).get("duration", ""))) == cand_format
        and int(v["statistics"].get("viewCount", 0)) >= 0
    ][:10]
    if not comparable:
        return None, 0
    return float(statistics.median(comparable)), len(comparable)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-searches", type=int, default=60, help="Safety cap; default YouTube search quota is 100/day.")
    parser.add_argument("--published-after", help="RFC3339, e.g. 2024-01-01T00:00:00Z")
    parser.add_argument("--region-code", default=None)
    parser.add_argument("--language", default=None)
    args = parser.parse_args()

    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        raise SystemExit("Set YOUTUBE_API_KEY in the environment. Do not commit API keys.")

    config = json.loads((HERE / "niches.json").read_text(encoding="utf-8"))
    discovered: dict[str, set[str]] = {}
    search_calls = 0

    for niche in config["niches"]:
        for query in niche["queries"]:
            if search_calls >= args.max_searches:
                break
            params: dict[str, Any] = {
                "part": "snippet", "q": query, "type": "video",
                "order": "viewCount", "maxResults": 50,
            }
            if args.published_after:
                params["publishedAfter"] = args.published_after
            if args.region_code:
                params["regionCode"] = args.region_code
            if args.language:
                params["relevanceLanguage"] = args.language
            data = api_get("search", key, **params)
            search_calls += 1
            for item in data.get("items", []):
                vid = item.get("id", {}).get("videoId")
                if vid:
                    discovered.setdefault(vid, set()).add(niche["name"])
        if search_calls >= args.max_searches:
            break

    details = video_details(list(discovered), key)
    channel_ids = list({v["snippet"]["channelId"] for v in details.values()})
    channels = channel_details(channel_ids, key)

    rows: list[dict[str, Any]] = []
    for vid, item in details.items():
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        views = int(stats.get("viewCount", 0))
        seconds = parse_duration_seconds(item.get("contentDetails", {}).get("duration", ""))
        fmt = classify_format(seconds)
        primary = views >= (SHORT_MIN if fmt == "short_candidate" else LONG_MIN)
        if views < EMERGING_MIN and not primary:
            continue
        age = days_old(snippet["publishedAt"])
        likes = int(stats.get("likeCount", 0)) if "likeCount" in stats else None
        rows.append({
            "video_id": vid,
            "title": snippet.get("title", ""),
            "channel_id": snippet.get("channelId", ""),
            "channel_title": snippet.get("channelTitle", ""),
            "published_at": snippet.get("publishedAt", ""),
            "age_days": round(age, 2),
            "duration_seconds": seconds,
            "format": fmt,
            "views": views,
            "views_per_day": round(views / age, 2),
            "likes": likes,
            "like_rate": round(likes / views, 6) if likes is not None and views else None,
            "niches": sorted(discovered.get(vid, set())),
            "primary_pool": primary,
            "channel_subscribers": int(channels.get(snippet.get("channelId", ""), {}).get("statistics", {}).get("subscriberCount", 0) or 0),
            "channel_baseline_median": None,
            "baseline_sample_size": 0,
            "outlier_ratio": None,
            "emerging_pool": False,
        })

    # Only spend channel-history calls on >=500k candidates that need outlier evaluation.
    history_cache: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["primary_pool"]:
            continue
        cid = row["channel_id"]
        channel = channels.get(cid)
        if not channel:
            continue
        if cid not in history_cache:
            ids = recent_upload_ids(channel, key, 25)
            history_cache[cid] = list(video_details(ids, key).values())
        baseline, n = comparable_baseline(row, history_cache[cid])
        row["channel_baseline_median"] = baseline
        row["baseline_sample_size"] = n
        if baseline and baseline > 0:
            ratio = row["views"] / baseline
            row["outlier_ratio"] = round(ratio, 2)
            row["emerging_pool"] = row["views"] >= EMERGING_MIN and ratio >= EMERGING_OUTLIER

    # Primary pool + emerging outliers are the review set. Keep all >=500k rows in raw output for threshold analysis.
    rows.sort(key=lambda r: (bool(r["primary_pool"] or r["emerging_pool"]), r["views_per_day"], r["views"]), reverse=True)

    output = HERE / "output"
    output.mkdir(exist_ok=True)
    (output / "raw_results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    fields = [
        "video_id","title","channel_id","channel_title","published_at","age_days",
        "duration_seconds","format","views","views_per_day","likes","like_rate",
        "channel_subscribers","channel_baseline_median","baseline_sample_size",
        "outlier_ratio","primary_pool","emerging_pool","niches"
    ]
    with (output / "candidates.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            flat["niches"] = "|".join(row["niches"])
            writer.writerow({k: flat.get(k) for k in fields})

    summary = {
        "search_calls": search_calls,
        "unique_search_hits": len(discovered),
        "videos_at_least_500k": len(rows),
        "primary_pool": sum(bool(r["primary_pool"]) for r in rows),
        "emerging_pool": sum(bool(r["emerging_pool"]) for r in rows),
        "thresholds": {
            "long_form_primary_views": LONG_MIN,
            "short_candidate_primary_views": SHORT_MIN,
            "emerging_min_views": EMERGING_MIN,
            "emerging_outlier_ratio": EMERGING_OUTLIER,
        },
        "note": "Strong velocity is intentionally collected as views_per_day but not thresholded until the distribution is reviewed."
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
