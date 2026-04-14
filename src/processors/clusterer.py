"""
Clusterer — groups items into topics using keyword overlap.

Strategy:
  1. Extract discriminating keywords (generic Cuban/geographic words excluded).
  2. Items share a topic if they share ≥ min_keyword_overlap SEED keywords
     (founding item's keywords only — prevents chain-growth false matches).
  3. After clustering, single-item orphans in the same category are grouped
     into a "Otras noticias de [category]" catch-all topic.
  4. Topic name = category label + best item title for multi-item topics;
     raw title for singletons.
  5. Topic synthesis = joined summaries, no redundant "Según X:" prefix when
     the article text already attributes the source.
"""

import logging
import re

from src.utils import category_label_es, make_topic_id, now_utc

logger = logging.getLogger(__name__)

# Minimum items to keep a standalone topic; smaller clusters get merged
# into the category catch-all bucket.
_MIN_STANDALONE = 2


class Clusterer:
    def __init__(self, config: dict):
        self.min_overlap   = config.get("min_keyword_overlap", 3)
        self.max_topics    = config.get("max_topics", 15)
        self.min_synthesis = config.get("min_items_for_synthesis", 2)

    def cluster(self, items: list[dict]) -> list[dict]:
        date_str = now_utc().strftime("%Y%m%d")
        topics: list[dict] = []

        for item in items:
            assigned = self._find_topic(item, topics)
            if assigned:
                self._add_to_topic(assigned, item)
            else:
                topics.append(self._new_topic(item, date_str))

        # ── Merge single-item orphans by category ──────────────────────────
        topics = self._merge_orphans(topics, items, date_str)

        # Sort by score, trim to max
        topics.sort(key=lambda t: t["scoring"]["total_score"], reverse=True)
        topics = topics[: self.max_topics]

        # ── Finalise each topic ────────────────────────────────────────────
        item_map = {i["id"]: i for i in items}
        for topic in topics:
            all_ids = (
                topic["items"]["featured"]
                + topic["items"]["additional"]
                + topic["items"]["videos"]
            )
            if len(all_ids) >= self.min_synthesis:
                self._synthesize(topic, item_map)
            # Assign topic back to items
            for iid in all_ids:
                if iid in item_map:
                    item_map[iid]["processing"]["topic_assigned"] = topic["id"]
            # Refine readable name
            topic["name"] = self._derive_name(topic, item_map)

        logger.info(f"  Clustered into {len(topics)} topics")
        return topics

    # ── Matching ──────────────────────────────────────────────────────────────

    def _find_topic(self, item: dict, topics: list[dict]) -> dict | None:
        kw_set = set(item["enrichment"].get("keywords", []))
        if len(kw_set) < self.min_overlap:
            return None
        for topic in topics:
            # Use frozen seed keywords to prevent chain-growth false matches
            if len(kw_set & topic["_seed_keywords"]) >= self.min_overlap:
                return topic
        return None

    def _add_to_topic(self, topic: dict, item: dict) -> None:
        topic["_keywords"] |= set(item["enrichment"].get("keywords", []))

        iid  = item["id"]
        tier = item["source"]["tier"]
        if item["type"] == "video":
            if iid not in topic["items"]["videos"]:
                topic["items"]["videos"].append(iid)
        elif tier == "estatal":
            if iid not in topic["items"]["state_coverage"]:
                topic["items"]["state_coverage"].append(iid)
        elif len(topic["items"]["featured"]) < 3:
            if iid not in topic["items"]["featured"]:
                topic["items"]["featured"].append(iid)
        else:
            if iid not in topic["items"]["additional"]:
                topic["items"]["additional"].append(iid)

        topic["coverage"]["total_items"] += 1
        topic["coverage"][tier] = topic["coverage"].get(tier, 0) + 1
        self._update_topic_score(topic)

    # ── New topic creation ────────────────────────────────────────────────────

    def _new_topic(self, item: dict, date_str: str) -> dict:
        tier     = item["source"].get("tier", "independiente")
        category = item["enrichment"].get("category", "general")
        seed_kw  = set(item["enrichment"].get("keywords", []))
        topic_id = make_topic_id(date_str, item["content"]["title"])

        items_init: dict[str, list] = {
            "featured":       [],
            "additional":     [],
            "videos":         [],
            "state_coverage": [],
        }
        if item["type"] == "video":
            items_init["videos"].append(item["id"])
        elif tier == "estatal":
            items_init["state_coverage"].append(item["id"])
        else:
            items_init["featured"].append(item["id"])

        importance = item["scoring"]["total_score"]
        return {
            "id": topic_id,
            "name": _truncate(item["content"]["title"], 80),
            "category": category,
            "created_at": now_utc().isoformat(),
            "_seed_keywords": seed_kw,
            "_keywords": set(seed_kw),
            "synthesis": {
                "narrative": item["enrichment"].get("summary", ""),
                "key_points": [],
            },
            "items": items_init,
            "coverage": {
                "total_items": 1,
                tier: 1,
            },
            "scoring": {
                "importance_score": importance,
                "coverage_breadth": 0.2,
                # Single-item topics start at 50% of their item score so they
                # still appear meaningfully in the digest, but multi-source
                # topics (which use the full 0.6+0.4 formula) rank higher.
                "total_score": round(importance * 0.5, 4),
            },
        }

    # ── Orphan merging ────────────────────────────────────────────────────────

    def _merge_orphans(
        self, topics: list[dict], items: list[dict], date_str: str
    ) -> list[dict]:
        """
        Collect single-item topics that share a category and merge them
        into a "Otras noticias de [category]" bucket.
        Only merge categories that have ≥ 2 orphan topics.
        """
        from collections import defaultdict

        standalone = [t for t in topics if t["coverage"]["total_items"] < _MIN_STANDALONE]
        multi      = [t for t in topics if t["coverage"]["total_items"] >= _MIN_STANDALONE]

        if not standalone:
            return topics

        # Group orphans by category
        by_cat: dict[str, list] = defaultdict(list)
        for t in standalone:
            by_cat[t.get("category", "general")].append(t)

        kept_standalone: list[dict] = []
        merged_topics: list[dict] = []

        item_map = {i["id"]: i for i in items}

        for cat, orphans in by_cat.items():
            if len(orphans) < 2:
                # Only 1 orphan in this category — keep standalone
                kept_standalone.extend(orphans)
                continue

            # Build merged topic
            label  = category_label_es(cat)
            name   = f"Otras noticias: {label}"
            merged = {
                "id": make_topic_id(date_str, name),
                "name": name,
                "category": cat,
                "created_at": now_utc().isoformat(),
                "_seed_keywords": set(),
                "_keywords": set(),
                "synthesis": {"narrative": "", "key_points": []},
                "items": {
                    "featured":       [],
                    "additional":     [],
                    "videos":         [],
                    "state_coverage": [],
                },
                "coverage": {"total_items": 0},
                "scoring": {"importance_score": 0.0, "coverage_breadth": 0.0, "total_score": 0.0},
            }

            # Sort orphans by item score (best first) and add them
            orphans_sorted = sorted(
                orphans,
                key=lambda t: t["scoring"]["importance_score"],
                reverse=True,
            )
            for orphan in orphans_sorted:
                for slot in ("featured", "additional", "videos", "state_coverage"):
                    for iid in orphan["items"].get(slot, []):
                        item = item_map.get(iid)
                        if item:
                            self._add_to_topic(merged, item)

            self._update_topic_score(merged)
            merged_topics.append(merged)

        return multi + kept_standalone + merged_topics

    # ── Scoring ───────────────────────────────────────────────────────────────

    def _update_topic_score(self, topic: dict) -> None:
        n = topic["coverage"]["total_items"]
        breadth = min(n / 5.0, 1.0)
        importance = topic["scoring"]["importance_score"]
        topic["scoring"]["coverage_breadth"] = round(breadth, 4)
        topic["scoring"]["total_score"] = round(
            0.6 * importance + 0.4 * breadth, 4
        )

    # ── Synthesis ─────────────────────────────────────────────────────────────

    def _synthesize(self, topic: dict, item_map: dict) -> None:
        """Build narrative from the best featured items' summaries.

        Strips the 'Según X: ' attribution prefix that the enricher adds to
        summaries, since the topic card already shows source name and the
        double-attribution looks redundant ('Según Cubanet: Según informó…').
        """
        featured_ids = topic["items"]["featured"][:3]
        parts: list[str] = []
        for iid in featured_ids:
            item = item_map.get(iid)
            if not item:
                continue
            summary = item["enrichment"].get("summary", "")
            source  = item["source"]["name"]
            if not summary:
                continue
            # Clean up double-attribution pattern
            clean = _strip_segun_prefix(summary)
            parts.append(f"{source}: {clean}" if clean else "")

        narrative = " · ".join(p for p in parts if p)
        if narrative:
            topic["synthesis"]["narrative"] = narrative
            topic["synthesis"]["key_points"] = [
                item_map[iid]["content"]["title"]
                for iid in featured_ids
                if iid in item_map
            ]

    # ── Name derivation ───────────────────────────────────────────────────────

    def _derive_name(self, topic: dict, item_map: dict) -> str:
        category = topic.get("category", "general")
        n = topic["coverage"]["total_items"]

        # For already-named catch-all topics, keep the name
        if topic["name"].startswith("Otras noticias:"):
            return topic["name"]

        # Find highest-scored featured/video item
        best = None
        best_score = -1.0
        for iid in (topic["items"]["featured"] or topic["items"]["videos"]):
            item = item_map.get(iid)
            if item:
                s = item["scoring"]["total_score"]
                if s > best_score:
                    best_score, best = s, item

        if not best:
            return topic["name"]

        title = _truncate(best["content"]["title"], 70)
        if n >= 2:
            label = category_label_es(category)
            return f"[{label}] {title}"
        return title


# ── Helpers ───────────────────────────────────────────────────────────────────

_SEGUN_PREFIX = re.compile(r"^según\s+\w[\w\s]*:\s*", re.IGNORECASE)


def _strip_segun_prefix(text: str) -> str:
    """Remove leading 'Según [Source]: ' attribution from a summary string."""
    return _SEGUN_PREFIX.sub("", text).strip()


def _truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len - 1] + "…"
