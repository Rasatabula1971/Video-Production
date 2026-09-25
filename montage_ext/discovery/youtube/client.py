from __future__ import annotations

import json
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

FetchJSON = Callable[[str], dict[str, Any]]


class YouTubeAPIError(RuntimeError):
    pass


def _default_fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "Video-Production/DiscoveryEngine-v1"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise YouTubeAPIError(f"YouTube API HTTP {exc.code}: {detail[:500]}") from exc
    except URLError as exc:
        raise YouTubeAPIError(f"YouTube API network error: {exc.reason}") from exc
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError("YouTube API returned invalid JSON") from exc


class YouTubeDataClient:
    base_url = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str, fetch_json: FetchJSON | None = None) -> None:
        if not api_key.strip():
            raise ValueError("api_key must not be blank")
        self.api_key = api_key
        self._fetch_json = fetch_json or _default_fetch_json
        self.call_counts: dict[str, int] = {}

    def _get(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        clean = {key: value for key, value in params.items() if value is not None}
        clean["key"] = self.api_key
        url = f"{self.base_url}/{method}?{urlencode(clean, doseq=True)}"
        self.call_counts[method] = self.call_counts.get(method, 0) + 1
        return self._fetch_json(url)

    def search_videos(self, query: str, max_results: int = 25) -> list[dict[str, Any]]:
        if not query.strip():
            raise ValueError("query must not be blank")
        max_results = min(max(int(max_results), 1), 50)
        payload = self._get(
            "search",
            {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": "relevance",
                "safeSearch": "none",
            },
        )
        return list(payload.get("items", []))

    def videos(self, video_ids: list[str]) -> list[dict[str, Any]]:
        unique = list(dict.fromkeys(item for item in video_ids if item))
        results: list[dict[str, Any]] = []
        for start in range(0, len(unique), 50):
            batch = unique[start : start + 50]
            payload = self._get(
                "videos",
                {
                    "part": "snippet,statistics,contentDetails",
                    "id": ",".join(batch),
                    "maxResults": 50,
                },
            )
            results.extend(payload.get("items", []))
        return results

    def channels(self, channel_ids: list[str]) -> list[dict[str, Any]]:
        unique = list(dict.fromkeys(item for item in channel_ids if item))
        results: list[dict[str, Any]] = []
        for start in range(0, len(unique), 50):
            batch = unique[start : start + 50]
            payload = self._get(
                "channels",
                {
                    "part": "snippet,contentDetails,statistics",
                    "id": ",".join(batch),
                    "maxResults": 50,
                },
            )
            results.extend(payload.get("items", []))
        return results

    def playlist_video_ids(self, playlist_id: str, max_results: int = 25) -> list[str]:
        if not playlist_id:
            return []
        max_results = min(max(int(max_results), 1), 50)
        payload = self._get(
            "playlistItems",
            {
                "part": "contentDetails",
                "playlistId": playlist_id,
                "maxResults": max_results,
            },
        )
        return [
            item.get("contentDetails", {}).get("videoId")
            for item in payload.get("items", [])
            if item.get("contentDetails", {}).get("videoId")
        ]
