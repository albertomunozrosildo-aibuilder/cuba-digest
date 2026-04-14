"""
YouTube Collector — no API key required.

Resolution strategy (tried in order):
  1. channel_id   → direct RSS feed
  2. handle       → fetch youtube.com/@handle, extract channel_id from HTML
  3. channel_url  → parse /channel/UC..., or resolve /@handle inside URL

If none resolve, the channel is skipped with a warning.
"""

import logging
import re
import time
from datetime import datetime, timedelta, timezone

import feedparser
import requests
from bs4 import BeautifulSoup

from src.utils import clean_html, extract_keywords, first_sentences, make_item_id, now_utc, parse_date

logger = logging.getLogger(__name__)

_RSS_BASE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
_RESOLVE_CACHE: dict[str, str | None] = {}   # handle/url → channel_id

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-US,es;q=0.9,en;q=0.8",
}


class YouTubeCollector:
    def __init__(self, config: dict):
        self.lookback_hours = config.get("lookback_hours", 48)
        self.max_per_channel = config.get("max_videos_per_channel", 5)
        self.channels = config.get("channels", [])

    # ── Public API ────────────────────────────────────────────────────────────

    def collect(self) -> list[dict]:
        all_items: list[dict] = []
        date_str = now_utc().strftime("%Y%m%d")
        cutoff = now_utc() - timedelta(hours=self.lookback_hours)

        for ch in self.channels:
            if not ch.get("enabled", True):
                continue
            name = ch.get("name", "unknown")
            try:
                items = self._collect_channel(ch, date_str, cutoff)
                if items:
                    logger.info(f"  YouTube [{name}]: {len(items)} videos")
                else:
                    logger.debug(f"  YouTube [{name}]: 0 videos (no recent content or unresolved)")
                all_items.extend(items)
            except Exception as exc:
                logger.warning(f"  YouTube [{name}]: error — {exc}")

        return all_items

    # ── Channel resolution ────────────────────────────────────────────────────

    def _resolve_channel_id(self, ch: dict) -> str | None:
        """Return a UC... channel_id or None."""
        # 1. Direct channel_id
        cid = ch.get("channel_id")
        if cid and _looks_like_channel_id(cid):
            return cid

        # 2. Handle
        handle = ch.get("handle")
        if handle:
            handle = handle.lstrip("@")
            resolved = self._resolve_handle(handle)
            if resolved:
                return resolved

        # 3. channel_url
        url = ch.get("channel_url")
        if url:
            resolved = self._resolve_from_url(url)
            if resolved:
                return resolved

        return None

    def _resolve_handle(self, handle: str) -> str | None:
        cache_key = f"handle:{handle}"
        if cache_key in _RESOLVE_CACHE:
            return _RESOLVE_CACHE[cache_key]

        url = f"https://www.youtube.com/@{handle}"
        result = self._extract_channel_id_from_page(url)
        _RESOLVE_CACHE[cache_key] = result
        return result

    def _resolve_from_url(self, url: str) -> str | None:
        cache_key = f"url:{url}"
        if cache_key in _RESOLVE_CACHE:
            return _RESOLVE_CACHE[cache_key]

        # Direct /channel/UC...
        m = re.search(r"/channel/(UC[\w-]+)", url)
        if m:
            _RESOLVE_CACHE[cache_key] = m.group(1)
            return m.group(1)

        # /@handle in URL
        m = re.search(r"/@([\w-]+)", url)
        if m:
            result = self._resolve_handle(m.group(1))
            _RESOLVE_CACHE[cache_key] = result
            return result

        # /c/name or /user/name — fetch the page
        if "/c/" in url or "/user/" in url or "youtube.com/" in url:
            result = self._extract_channel_id_from_page(url)
            _RESOLVE_CACHE[cache_key] = result
            return result

        _RESOLVE_CACHE[cache_key] = None
        return None

    def _extract_channel_id_from_page(self, url: str) -> str | None:
        """Fetch a YouTube page and extract the channel ID."""
        try:
            resp = requests.get(url, headers=_HEADERS, timeout=12)
            if resp.status_code != 200:
                logger.debug(f"    resolve {url}: HTTP {resp.status_code}")
                return None

            html = resp.text

            # Strategy 1: <link rel="canonical" href=".../channel/UCxxx">
            m = re.search(
                r'<link\s+rel="canonical"\s+href="https://www\.youtube\.com/channel/(UC[\w-]+)"',
                html,
            )
            if m:
                return m.group(1)

            # Strategy 2: "channelId":"UCxxx" in JSON blobs
            m = re.search(r'"channelId"\s*:\s*"(UC[\w-]+)"', html)
            if m:
                return m.group(1)

            # Strategy 3: "externalId":"UCxxx"
            m = re.search(r'"externalId"\s*:\s*"(UC[\w-]+)"', html)
            if m:
                return m.group(1)

            # Strategy 4: browseId
            m = re.search(r'"browseId"\s*:\s*"(UC[\w-]+)"', html)
            if m:
                return m.group(1)

            logger.debug(f"    resolve {url}: no channel_id pattern found")
            return None

        except requests.RequestException as exc:
            logger.debug(f"    resolve {url}: request error — {exc}")
            return None

    # ── Feed parsing ──────────────────────────────────────────────────────────

    def _collect_channel(
        self, ch: dict, date_str: str, cutoff: datetime
    ) -> list[dict]:
        channel_id = self._resolve_channel_id(ch)
        if not channel_id:
            logger.debug(f"  YouTube [{ch.get('name')}]: cannot resolve identifier, skipping")
            return []

        rss_url = _RSS_BASE.format(channel_id=channel_id)
        feed = feedparser.parse(rss_url)

        if feed.bozo and not feed.entries:
            logger.debug(f"  YouTube [{ch.get('name')}]: feed parse error — {feed.get('bozo_exception')}")
            return []

        items: list[dict] = []
        for entry in feed.entries:
            item = self._parse_entry(entry, ch, date_str)
            if item is None:
                continue
            pub = parse_date(item["content"]["published_date"])
            if pub and pub < cutoff:
                continue
            items.append(item)
            if len(items) >= self.max_per_channel:
                break

        return items

    def _parse_entry(self, entry, ch: dict, date_str: str) -> dict | None:
        try:
            url = entry.get("link", "")
            if not url:
                return None

            title = entry.get("title", "").strip()
            if not title:
                return None

            # Published date
            pub_date = parse_date(entry.get("published_parsed") or entry.get("published"))

            # Description — from media:description or summary
            description = ""
            media_group = entry.get("media_group") or {}
            if isinstance(media_group, dict):
                description = media_group.get("media_description", "") or ""
            if not description:
                description = clean_html(entry.get("summary", ""))

            # View count
            view_count = 0
            try:
                stats = entry.get("media_statistics") or {}
                if isinstance(stats, dict):
                    view_count = int(stats.get("views", 0) or 0)
            except (ValueError, TypeError):
                view_count = 0

            # Thumbnail
            thumbnail_url = ""
            try:
                thumbs = entry.get("media_thumbnail") or []
                if thumbs and isinstance(thumbs, list):
                    thumbnail_url = thumbs[0].get("url", "")
            except (IndexError, AttributeError):
                thumbnail_url = ""

            return {
                "id": make_item_id(date_str, url),
                "type": "video",
                "source": {
                    "name": ch["name"],
                    "tier": ch.get("tier", "diaspora"),
                    "weight": ch.get("weight", 0.5),
                    "url": f"https://www.youtube.com/channel/{ch.get('channel_id', '')}",
                    "description": ch.get("description", ""),
                },
                "content": {
                    "title": title,
                    "url": url,
                    "published_date": pub_date.isoformat() if pub_date else None,
                    "description": description,
                },
                "enrichment": {
                    "summary": "",
                    "insight": "",
                    "keywords": extract_keywords(f"{title} {description}"),
                },
                "metadata": {
                    "view_count": view_count,
                    "thumbnail_url": thumbnail_url,
                    "has_captions": False,
                },
                "processing": {
                    "collected_at": now_utc().isoformat(),
                    "enriched_at": None,
                    "topic_assigned": None,
                },
                "scoring": {
                    "editorial_score": 0.0,
                    "engagement_score": 0.0,
                    "recency_score": 0.0,
                    "source_tier_score": 0.0,
                    "total_score": 0.0,
                },
            }
        except Exception as exc:
            logger.debug(f"    parse entry error: {exc}")
            return None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _looks_like_channel_id(value: str) -> bool:
    return bool(value and re.match(r"^UC[\w-]{20,}$", value))
