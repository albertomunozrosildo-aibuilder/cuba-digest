"""Filter items by age, title quality, description length, URL validity, and Cuba relevance."""

import logging
import re
from datetime import timedelta
from urllib.parse import urlparse

from src.utils import now_utc, parse_date

logger = logging.getLogger(__name__)

# Terms that confirm an item is about Cuba / Cuban affairs.
# Used to filter international sources that cover many topics.
_CUBA_TERMS = re.compile(
    r"\b(cuba|cubano|cubana|cubanos|cubanas|habanero|habanera"
    r"|la\s+habana|díaz[- ]canel|diaz[- ]canel|castrismo"
    r"|embargo\s+a\s+cuba|granma|varadero|santiago\s+de\s+cuba"
    r"|régimen\s+cubano|gobierno\s+cubano|isla\s+de\s+cuba)\b",
    re.IGNORECASE,
)


class ItemFilter:
    def __init__(self, config: dict):
        self.min_description_length = config.get("min_description_length", 50)
        self.max_age_hours = config.get("max_age_hours", 48)
        self.min_title_length = config.get("min_title_length", 10)

    def filter(self, items: list[dict]) -> list[dict]:
        cutoff = now_utc() - timedelta(hours=self.max_age_hours)
        seen_urls: set[str] = set()
        kept, dropped = [], 0

        for item in items:
            reason = self._should_drop(item, cutoff, seen_urls)
            if reason:
                logger.debug(
                    f"  drop [{item['source']['name']}] "
                    f"{item['content']['title'][:60]}: {reason}"
                )
                dropped += 1
            else:
                seen_urls.add(item["content"].get("url", ""))
                kept.append(item)

        logger.info(f"  Filter: {len(kept)} kept, {dropped} dropped")
        return kept

    def _should_drop(self, item: dict, cutoff, seen_urls: set) -> str | None:
        content = item["content"]
        is_video = item["type"] == "video"

        # URL validity
        url = content.get("url", "")
        if not url:
            return "missing URL"
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return "invalid URL scheme"

        # Duplicate URL
        if url in seen_urls:
            return "duplicate URL"

        # Title quality
        title = (content.get("title") or "").strip()
        if len(title) < self.min_title_length:
            return f"title too short ({len(title)} chars)"

        # Age — only applied when date is known
        pub = parse_date(content.get("published_date"))
        if pub and pub < cutoff:
            return "too old"

        # Description length — videos are exempt (often have no description)
        if not is_video:
            desc = (content.get("description") or "").strip()
            if len(desc) < self.min_description_length:
                return f"description too short ({len(desc)} chars)"

        # Cuba relevance — applied to sources flagged with cuba_filter
        if item["source"].get("cuba_filter"):
            combined = f"{title} {content.get('description', '') or ''}"
            if not _CUBA_TERMS.search(combined):
                return "not Cuba-relevant"

        return None
