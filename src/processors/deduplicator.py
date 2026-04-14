"""
Deduplicator — detects near-duplicate items by title similarity.

Same source + similar title → keep most recent.
Different sources + similar title → keep both but link as additional coverage.
"""

import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class Deduplicator:
    def __init__(self, config: dict):
        self.threshold = config.get("title_similarity_threshold", 0.82)
        self.enabled = config.get("enabled", True)

    def deduplicate(self, items: list[dict]) -> list[dict]:
        if not self.enabled:
            return items

        unique: list[dict] = []
        dropped = 0

        for item in items:
            duplicate_of = self._find_duplicate(item, unique)
            if duplicate_of is None:
                unique.append(item)
            else:
                # Different source: add as additional_coverage reference
                if item["source"]["name"] != duplicate_of["source"]["name"]:
                    refs = duplicate_of.setdefault("additional_coverage", [])
                    refs.append({
                        "source": item["source"]["name"],
                        "url": item["content"]["url"],
                        "title": item["content"]["title"],
                    })
                dropped += 1

        logger.info(f"  Dedup: {len(unique)} unique, {dropped} duplicates merged")
        return unique

    def _find_duplicate(self, item: dict, existing: list[dict]) -> dict | None:
        title = item["content"]["title"].lower()
        for candidate in existing:
            sim = SequenceMatcher(
                None, title, candidate["content"]["title"].lower()
            ).ratio()
            if sim >= self.threshold:
                return candidate
        return None
