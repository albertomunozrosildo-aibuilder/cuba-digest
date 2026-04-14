"""
RSS / News Collector — uses feedparser, no API keys required.
"""

import logging
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from src.utils import clean_html, extract_keywords, make_item_id, now_utc, parse_date

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "es-US,es;q=0.9,en;q=0.8",
}


class RSSCollector:
    def __init__(self, config: dict):
        self.lookback_hours = config.get("lookback_hours", 48)
        self.max_per_feed = config.get("max_items_per_feed", 10)
        self.timeout = config.get("request_timeout", 10)
        self.feeds = config.get("feeds", [])

    # ── Public API ────────────────────────────────────────────────────────────

    def collect(self) -> list[dict]:
        all_items: list[dict] = []
        date_str = now_utc().strftime("%Y%m%d")
        cutoff = now_utc() - timedelta(hours=self.lookback_hours)

        for feed_cfg in self.feeds:
            if not feed_cfg.get("enabled", True):
                continue
            name = feed_cfg.get("name", "unknown")
            url = feed_cfg.get("url", "")
            if not url:
                continue
            try:
                items = self._collect_feed(feed_cfg, date_str, cutoff)
                logger.info(f"  RSS [{name}]: {len(items)} articles")
                all_items.extend(items)
            except Exception as exc:
                logger.warning(f"  RSS [{name}]: error — {exc}")

        return all_items

    # ── Feed parsing ──────────────────────────────────────────────────────────

    def _collect_feed(
        self, feed_cfg: dict, date_str: str, cutoff: datetime
    ) -> list[dict]:
        url = feed_cfg["url"]

        # Always fetch via requests first to enforce timeout
        feed = self._fetch_with_requests(url)
        if not feed or not feed.entries:
            logger.debug(f"  RSS [{feed_cfg['name']}]: empty or unreachable")
            return []

        items: list[dict] = []
        for entry in feed.entries:
            item = self._parse_entry(entry, feed_cfg, date_str)
            if item is None:
                continue
            pub = parse_date(item["content"]["published_date"])
            if pub and pub < cutoff:
                continue
            items.append(item)
            if len(items) >= self.max_per_feed:
                break

        return items

    def _fetch_with_requests(self, url: str):
        """Fetch RSS with timeout then parse with feedparser."""
        try:
            resp = requests.get(url, headers=_HEADERS, timeout=self.timeout)
            if resp.status_code == 200:
                return feedparser.parse(resp.content)
            logger.debug(f"    HTTP {resp.status_code} for {url}")
        except requests.exceptions.Timeout:
            logger.warning(f"    Timeout fetching {url}")
        except requests.RequestException as exc:
            logger.debug(f"    Request error {url}: {exc}")
        return None

    def _parse_entry(self, entry, feed_cfg: dict, date_str: str) -> dict | None:
        try:
            # URL
            url = entry.get("link", "")
            if not url:
                return None

            # Title
            title = entry.get("title", "").strip()
            title = clean_html(title)
            if not title:
                return None

            # Published date — try multiple fields
            pub_date = parse_date(
                entry.get("published_parsed")
                or entry.get("updated_parsed")
                or entry.get("published")
                or entry.get("updated")
            )

            # Description — prefer summary, fallback to content
            description = ""
            if entry.get("summary"):
                description = clean_html(entry.get("summary", ""))
            elif entry.get("content"):
                for c in entry.get("content", []):
                    description = clean_html(c.get("value", ""))
                    if description:
                        break

            return {
                "id": make_item_id(date_str, url),
                "type": "article",
                "source": {
                    "name": feed_cfg["name"],
                    "tier": feed_cfg.get("tier", "independiente"),
                    "weight": feed_cfg.get("weight", 1.0),
                    "url": _base_url(url),
                    "cuba_filter": feed_cfg.get("cuba_filter", False),
                    "description": feed_cfg.get("description", ""),
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
                    "view_count": 0,
                    "thumbnail_url": _extract_thumbnail(entry),
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

def _base_url(url: str) -> str:
    from urllib.parse import urlparse
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def _extract_thumbnail(entry) -> str:
    """Try to find a thumbnail URL from various feed fields."""
    # media:thumbnail
    thumbs = entry.get("media_thumbnail") or []
    if thumbs and isinstance(thumbs, list):
        return thumbs[0].get("url", "")
    # enclosures (podcast-style)
    for enc in entry.get("enclosures", []):
        if "image" in enc.get("type", ""):
            return enc.get("href", "")
    return ""
