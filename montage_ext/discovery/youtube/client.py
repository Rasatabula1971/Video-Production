from __future__ import annotations

import json
import time
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

FetchJSON = Callable[[str], dict[str, Any]]


class YouTubeAPIError(RuntimeError):
    pass


def _default_fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "Video-Production/DiscoveryEngine-v1"})
    retriable = {429, 500, 502, 503, 504}

    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8")
            try:
                return json.loads(payload)
            except json.JSONDecodeError as exc:
                raise YouTubeAPIError("YouTube API returned invalid JSON") from exc
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in retriable and attempt < 2:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt
                time.sleep(delay)
                continue
            raise YouTubeAPIError(f"YouTube API HTTP {exc.code}: {detail[:500]}") from exc
        except URLError as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise YouTubeAPIError(f"YouTube API network error: {exc.reason}") from exc

    raise YouTubeAPIError("YouTube API request failed after retries")


class YouTubeDataClient:
    base_url = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str, fetch_json: FetchJSON | None = None) -> None:
        if not api_key.strip():
            raise ValueError("api_key must not be blank")
        self.api_key = api_key
        self._fetch_json = fetch_json or _default_fetch_json
        self.call_counts: dict[str, int] = {}
        self._search_cache: dict[tuple[str, int], list[dict[str, Any]]] = {}
        self._video_cache: dict[str, dict[str, Any]] = {}
        self._channel_cache: dict[str, dict[str, Any]] = {}
        self._playlist_cache: dict[tuple[str, int], list[str]] = {}

    def _get(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        clean = {key: value for key, value in params.items() if value is not None}
        clean["key"] = self.api_key
        url = f"{self.base_url}/{method}?{urlencode(clean, doseq=True)}"
        self.call_counts[method] = self.call_counts.get(method, 0) + 1
        return self._fetch_json(url)

    def search_videos(self, query: str, max_results: int = 25) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            raise ValueError("query must not be blank")
        max_results = min(max(int(max_results), 1), 50)
        key = (query, max_results)
        if key not in self._search_cache:
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
            self._search_cache[key] = list(payload.get("items", []))
        return list(self._search_cache[key])

    def videos(self, video_ids: list[str]) -> list[dict[str, Any]]:
        unique = list(dict.fromkeys(item for item in video_ids if item))
        missing = [item for item in unique if item not in self._video_cache]
        for start in range(0, len(missing), 50):
            batch = missing[start : start + 50]
            payload = self._get(
                "videos",
                {
                    "part": "snippet,statistics,contentDetails",
                    "id": ",".join(batch),
                    "maxResults": 50,
                },
            )
            for item in payload.get("items", []):
                if item.get("id"):
                    self._video_cache[item["id"]] = item
        return [self._video_cache[item] for item in unique if item in self._video_cache]

    def channels(self, channel_ids: list[str]) -> list[dict[str, Any]]:
        unique = list(dict.fromkeys(item for item in channel_ids if item))
        missing = [item for item in unique if item not in self._channel_cache]
        for start in range(0, len(missing), 50):
            batch = missing[start : start + 50]
            payload = self._get(
                "channels",
                {
                    "part": "snippet,contentDetails,statistics",
                    "id": ",".join(batch),
                    "maxResults": 50,
                },
            )
            for item in payload.get("items", []):
                if item.get("id"):
                    self._channel_cache[item["id"]] = item
        return [self._channel_cache[item] for item in unique if item in self._channel_cache]

    def playlist_video_ids(self, playlist_id: str, max_results: int = 25) -> list[str]:
        if not playlist_id:
            return []
        max_results = min(max(int(max_results), 1), 50)
        key = (playlist_id, max_results)
        if key not in self._playlist_cache:
            payload = self._get(
                "playlistItems",
                {
                    "part": "contentDetails",
                    "playlistId": playlist_id,
                    "maxResults": max_results,
                },
            )
            self._playlist_cache[key] = [
                item.get("contentDetails", {}).get("videoId")
                for item in payload.get("items", [])
                if item.get("contentDetails", {}).get("videoId")
            ]
        return list(self._playlist_cache[key])
