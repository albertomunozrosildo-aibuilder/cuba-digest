"""
Scorer — calculates composite relevance score for each item.

Score components (weights from settings.yaml):
  editorial   (0.40): based on source tier
  recency     (0.30): exponential decay by age
  engagement  (0.20): view count for videos, neutral for articles
  source_tier (0.10): direct tier weight
"""

import logging
import math
from datetime import timedelta

from src.utils import now_utc, parse_date

logger = logging.getLogger(__name__)


class Scorer:
    def __init__(self, config: dict):
        weights = config.get("weights", {})
        self.w_editorial   = weights.get("editorial", 0.40)
        self.w_recency     = weights.get("recency", 0.30)
        self.w_engagement  = weights.get("engagement", 0.20)
        self.w_tier        = weights.get("source_tier", 0.10)

        self.tier_scores = config.get("tier_scores", {
            "independiente": 1.0,
            "diaspora":      0.8,
            "internacional": 0.6,
            "estatal":       0.0,
        })

        recency = config.get("recency_buckets", {})
        self.r_6h  = recency.get("under_6h", 1.0)
        self.r_12h = recency.get("under_12h", 0.8)
        self.r_24h = recency.get("under_24h", 0.5)
        self.r_old = recency.get("older", 0.2)

    def score_all(self, items: list[dict]) -> list[dict]:
        now = now_utc()
        for item in items:
            self._score_item(item, now)
        items.sort(key=lambda x: x["scoring"]["total_score"], reverse=True)
        return items

    def rescore_with_coverage(self, items: list[dict], topics: list[dict]) -> list[dict]:
        """
        Optional second pass after clustering.
        Items that belong to a multi-source topic receive a small coverage
        bonus so they rise in the Trending tab relative to isolated items.
        """
        # Build map: item_id → topic coverage_breadth
        id_to_breadth: dict[str, float] = {}
        for topic in topics:
            breadth = topic["scoring"].get("coverage_breadth", 0.0)
            if breadth <= 0.2:
                continue  # single-item topics — no bonus
            for slot in ("featured", "additional", "videos"):
                for iid in topic["items"].get(slot, []):
                    id_to_breadth[iid] = max(id_to_breadth.get(iid, 0.0), breadth)

        for item in items:
            breadth = id_to_breadth.get(item["id"], 0.0)
            if breadth > 0.2:
                # Bonus: up to +0.10 for items in full-coverage topics
                bonus = round(breadth * 0.10, 4)
                item["scoring"]["total_score"] = round(
                    min(item["scoring"]["total_score"] + bonus, 1.0), 4
                )

        items.sort(key=lambda x: x["scoring"]["total_score"], reverse=True)
        return items

    def _score_item(self, item: dict, now) -> None:
        tier = item["source"].get("tier", "independiente")
        s = item["scoring"]

        s["editorial_score"]    = self._editorial(item, tier)
        s["recency_score"]      = self._recency(item, now)
        s["engagement_score"]   = self._engagement(item)
        s["source_tier_score"]  = self.tier_scores.get(tier, 0.5)

        s["total_score"] = round(
            self.w_editorial  * s["editorial_score"]
            + self.w_recency  * s["recency_score"]
            + self.w_engagement * s["engagement_score"]
            + self.w_tier     * s["source_tier_score"],
            4,
        )

    def _editorial(self, item: dict, tier: str) -> float:
        base = 0.5
        tier_bonus = {
            "independiente": 0.3,
            "diaspora":      0.25,
            "internacional": 0.15,
            "estatal":       0.0,
        }
        score = base + tier_bonus.get(tier, 0.0)
        # Penalty for very short description
        desc = item["content"].get("description", "") or ""
        if len(desc) < 100:
            score *= 0.7
        return min(round(score, 4), 1.0)

    def _recency(self, item: dict, now) -> float:
        pub = parse_date(item["content"].get("published_date"))
        if not pub:
            return self.r_old
        hours = (now - pub).total_seconds() / 3600
        if hours < 6:
            return self.r_6h
        elif hours < 12:
            return self.r_12h
        elif hours < 24:
            return self.r_24h
        return self.r_old

    def _engagement(self, item: dict) -> float:
        if item["type"] != "video":
            return 0.5   # neutral for articles
        views = item["metadata"].get("view_count", 0) or 0
        if views <= 0:
            return 0.1
        # log10 scale: 1K→0.6, 10K→0.8, 50K→0.93, 100K→1.0
        score = math.log10(views + 1) / 5.0
        return min(round(score, 4), 1.0)
