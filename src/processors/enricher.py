"""
Enricher — heuristic summaries, insights, and category classification.

No external APIs. All enrichment is rule-based and keyword-driven.
"""

import logging

from src.utils import (
    category_label_es,
    classify_category,
    first_sentences,
    now_utc,
    parse_date,
)

logger = logging.getLogger(__name__)

_TIER_LABELS = {
    "independiente": "medio independiente cubano",
    "diaspora":      "medio de la diáspora cubana",
    "internacional": "medio internacional",
    "estatal":       "medio estatal cubano",
}


class Enricher:
    def __init__(self, config: dict):
        self.summary_sentences = config.get("summary_sentences", 2)
        self.summary_max_chars = config.get("summary_max_chars", 220)

    def enrich_all(self, items: list[dict]) -> list[dict]:
        now = now_utc()
        for item in items:
            self._enrich(item, now)
        logger.info(f"  Enriched {len(items)} items (heuristic)")
        return items

    def _enrich(self, item: dict, now) -> None:
        content = item["content"]
        desc   = content.get("description") or ""
        title  = content.get("title") or ""
        tier   = item["source"].get("tier", "independiente")
        is_vid = item["type"] == "video"

        # ── Category classification ───────────────────────────────────────────
        combined = f"{title} {desc}"
        category = classify_category(combined)
        item["enrichment"]["category"] = category

        # ── Summary ───────────────────────────────────────────────────────────
        if desc:
            summary = first_sentences(
                desc,
                n=self.summary_sentences,
                max_chars=self.summary_max_chars,
            )
        else:
            summary = ""
        # For videos with no description, fall back to title
        if not summary and is_vid:
            summary = title[:self.summary_max_chars]
        item["enrichment"]["summary"] = summary

        # ── Insight ───────────────────────────────────────────────────────────
        parts: list[str] = []

        # Recency signal
        pub = parse_date(content.get("published_date"))
        if pub:
            hours = (now - pub).total_seconds() / 3600
            if hours < 3:
                parts.append("Publicado hace menos de 3 horas.")
            elif hours < 8:
                parts.append("Cobertura reciente.")

        # Category label
        cat_label = category_label_es(category)
        if cat_label != "General":
            parts.append(f"Tema: {cat_label}.")

        # Source tier
        tier_label = _TIER_LABELS.get(tier, "")
        if tier_label:
            parts.append(f"Fuente: {tier_label.capitalize()}.")

        # Estatal warning
        if tier == "estatal":
            parts.append("Se recomienda contrastar con fuentes independientes.")

        item["enrichment"]["insight"] = " ".join(parts)
        item["processing"]["enriched_at"] = now.isoformat()
