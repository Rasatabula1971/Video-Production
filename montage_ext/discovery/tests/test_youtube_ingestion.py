from __future__ import annotations

from datetime import datetime, timezone
import unittest
from urllib.parse import parse_qs, urlparse

from montage_ext.discovery.youtube.baseline import BaselineVideo, compute_channel_baseline
from montage_ext.discovery.youtube.client import YouTubeDataClient
from montage_ext.discovery.youtube.collector import collect_seed_observations
from montage_ext.discovery.youtube.duration import (
    duration_bucket,
    parse_iso8601_duration_seconds,
)


class DurationTests(unittest.TestCase):
    def test_parses_iso_duration(self) -> None:
        self.assertEqual(parse_iso8601_duration_seconds("PT2M30S"), 150.0)
        self.assertEqual(parse_iso8601_duration_seconds("PT1H2M3S"), 3723.0)

    def test_duration_bucket(self) -> None:
        self.assertEqual(duration_bucket(180), "short")
        self.assertEqual(duration_bucket(181), "long")
        self.assertIsNone(duration_bucket(None))


class BaselineTests(unittest.TestCase):
    def test_prefers_same_duration_bucket(self) -> None:
        now = datetime(2026, 9, 25, tzinfo=timezone.utc)
        videos = [
            BaselineVideo(f"s{i}", views, 60, "2026-09-01T00:00:00Z")
            for i, views in enumerate([100, 200, 300, 400, 500], start=1)
        ] + [
            BaselineVideo("long1", 10000, 1200, "2026-09-01T00:00:00Z")
        ]
        result = compute_channel_baseline(
            candidate_video_id="candidate",
            candidate_duration_seconds=45,
            videos=videos,
            now=now,
        )
        self.assertEqual(result.median_views, 300.0)
        self.assertEqual(result.sample_size, 5)
        self.assertEqual(result.method, "recent_same_duration_median")

    def test_falls_back_to_channel_median(self) -> None:
        now = datetime(2026, 9, 25, tzinfo=timezone.utc)
        videos = [
            BaselineVideo("s1", 100, 60, "2026-09-01T00:00:00Z"),
            BaselineVideo("long1", 1000, 1200, "2026-09-01T00:00:00Z"),
        ]
        result = compute_channel_baseline(
            candidate_video_id="candidate",
            candidate_duration_seconds=45,
            videos=videos,
            now=now,
        )
        self.assertEqual(result.median_views, 550.0)
        self.assertEqual(result.method, "recent_channel_median")

    def test_excludes_recent_uploads(self) -> None:
        now = datetime(2026, 9, 25, tzinfo=timezone.utc)
        videos = [
            BaselineVideo("recent", 999999, 60, "2026-09-24T00:00:00Z"),
            BaselineVideo("old", 100, 60, "2026-09-01T00:00:00Z"),
        ]
        result = compute_channel_baseline(
            candidate_video_id="candidate",
            candidate_duration_seconds=60,
            videos=videos,
            min_same_bucket_samples=1,
            now=now,
        )
        self.assertEqual(result.median_views, 100.0)


class FakeAPI:
    def __call__(self, url: str) -> dict:
        parsed = urlparse(url)
        method = parsed.path.rsplit("/", 1)[-1]
        params = parse_qs(parsed.query)

        if method == "search":
            return {
                "items": [
                    {
                        "id": {"videoId": "candidate"},
                        "snippet": {"title": "Ignored search title"},
                    }
                ]
            }

        if method == "channels":
            return {
                "items": [
                    {
                        "id": "chan1",
                        "snippet": {"title": "Test Channel"},
                        "contentDetails": {"relatedPlaylists": {"uploads": "uploads1"}},
                        "statistics": {"subscriberCount": "1000"},
                    }
                ]
            }

        if method == "playlistItems":
            return {
                "items": [
                    {"contentDetails": {"videoId": f"base{i}"}}
                    for i in range(1, 6)
                ]
            }

        if method == "videos":
            ids = params.get("id", [""])[0].split(",")
            items = []
            for video_id in ids:
                if video_id == "candidate":
                    items.append(
                        {
                            "id": "candidate",
                            "snippet": {
                                "title": "Turbo Lag Explained",
                                "channelId": "chan1",
                                "channelTitle": "Test Channel",
                                "publishedAt": "2026-09-20T00:00:00Z",
                            },
                            "statistics": {"viewCount": "3000"},
                            "contentDetails": {"duration": "PT1M"},
                        }
                    )
                elif video_id.startswith("base"):
                    view_count = int(video_id.removeprefix("base")) * 100
                    items.append(
                        {
                            "id": video_id,
                            "snippet": {
                                "channelId": "chan1",
                                "publishedAt": "2026-09-01T00:00:00Z",
                            },
                            "statistics": {"viewCount": str(view_count)},
                            "contentDetails": {"duration": "PT1M"},
                        }
                    )
            return {"items": items}

        raise AssertionError(f"unexpected method {method}")


class CollectorTests(unittest.TestCase):
    def test_collects_normalized_observation_with_baseline(self) -> None:
        client = YouTubeDataClient("fake-key", fetch_json=FakeAPI())
        observations = collect_seed_observations(
            client=client,
            seed_topic="turbo lag",
            max_results=1,
            baseline_pool_size=5,
            min_same_bucket_samples=5,
        )
        self.assertEqual(len(observations), 1)
        item = observations[0]
        self.assertEqual(item.video_id, "candidate")
        self.assertEqual(item.views, 3000)
        self.assertEqual(item.channel_baseline_views, 300.0)
        self.assertEqual(item.channel_baseline_sample_size, 5)
        self.assertEqual(item.channel_baseline_method, "recent_same_duration_median")
        self.assertEqual(item.topic, "turbo lag")
        self.assertEqual(client.call_counts["search"], 1)

    def test_reuses_cached_channel_and_baseline_evidence(self) -> None:
        client = YouTubeDataClient("fake-key", fetch_json=FakeAPI())
        kwargs = {
            "client": client,
            "seed_topic": "turbo lag",
            "max_results": 1,
            "baseline_pool_size": 5,
            "min_same_bucket_samples": 5,
        }
        collect_seed_observations(**kwargs)
        first_counts = dict(client.call_counts)
        collect_seed_observations(**kwargs)
        self.assertEqual(client.call_counts, first_counts)


if __name__ == "__main__":
    unittest.main()
