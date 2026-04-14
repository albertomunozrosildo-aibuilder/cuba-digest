"""
HTML Renderer — Jinja2-based Phase 2 implementation.
"""

import logging
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"


class HTMLRenderer:
    def __init__(self, config: dict):
        self.output_dir = Path(config.get("output_dir", "./output"))
        self.filename_pattern = config.get("digest_filename", "digest_{date}.html")

        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html"]),
        )
        self.env.filters["timeago"] = _filter_timeago
        self.env.filters["views"] = _filter_views

    def render(self, topics: list[dict], items: list[dict], date_str: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.output_dir / self.filename_pattern.format(date=date_str)

        context = _build_context(topics, items, date_str)
        template = self.env.get_template("digest.html.j2")
        html = template.render(**context)

        out_path.write_text(html, encoding="utf-8")
        logger.info(f"  HTML written → {out_path}")
        return out_path


# ── Template context builder ──────────────────────────────────────────────────

def _build_context(topics: list[dict], items: list[dict], date_str: str) -> dict:
    # Build fast lookup: item_id → item dict
    item_map = {item["id"]: item for item in items}

    def _resolve(ids: list) -> list[dict]:
        return [item_map[iid] for iid in ids if iid in item_map]

    # items_by_topic: topic_id → {featured, additional, videos, state_coverage}
    # Topic items lists hold IDs; resolve them to full item dicts for the template.
    items_by_topic: dict[str, dict] = {}
    for topic in topics:
        topic_items = topic.get("items", {})
        items_by_topic[topic["id"]] = {
            "featured": _resolve(topic_items.get("featured", [])),
            "additional": _resolve(topic_items.get("additional", [])),
            "videos": _resolve(topic_items.get("videos", [])),
            "state_coverage": _resolve(topic_items.get("state_coverage", [])),
        }

    # items_by_source: tier → {source_name → [items]}
    items_by_source: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for item in items:
        tier = item["source"].get("tier", "independiente")
        name = item["source"].get("name", "Desconocido")
        items_by_source[tier][name].append(item)
    # Convert defaultdicts to plain dicts for Jinja2 compatibility
    items_by_source = {t: dict(sources) for t, sources in items_by_source.items()}

    # core_del_dia: top topic names + article count context
    core_del_dia = _build_core_del_dia(topics, items)

    # Date display
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        date_display = dt.strftime("%-d de %B de %Y").replace(
            dt.strftime("%B"), _month_es(dt.month)
        )
    except ValueError:
        date_display = date_str

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sources_set = {item["source"]["name"] for item in items}
    stats = {
        "total": len(items),
        "articles": sum(1 for i in items if i["type"] == "article"),
        "videos": sum(1 for i in items if i["type"] == "video"),
        "topics": len(topics),
        "sources": len(sources_set),
    }

    return {
        "topics": topics,
        "items": items,
        "items_by_topic": items_by_topic,
        "items_by_source": items_by_source,
        "core_del_dia": core_del_dia,
        "date_display": date_display,
        "generated_at": generated_at,
        "stats": stats,
    }


def _build_core_del_dia(topics: list[dict], items: list[dict]) -> list[dict]:
    """
    Generate 5 headline entries for the Core del Día section.

    Returns list of dicts:
      { text, url, source_name, source_count, source_links }
    where source_links is a list of {name, url} for all items in the topic.
    """
    entries: list[dict] = []
    used_item_ids: set[str] = set()

    sorted_topics = sorted(
        topics,
        key=lambda t: t.get("scoring", {}).get("total_score", 0),
        reverse=True,
    )

    item_map = {i["id"]: i for i in items}

    for topic in sorted_topics:
        if len(entries) >= 5:
            break

        n = topic.get("coverage", {}).get("total_items", 0)
        featured_ids = topic.get("items", {}).get("featured", [])
        video_ids = topic.get("items", {}).get("videos", [])
        additional_ids = topic.get("items", {}).get("additional", [])
        candidate_ids = featured_ids + video_ids
        all_ids = featured_ids + video_ids + additional_ids

        if not candidate_ids:
            continue

        # Pick the highest-scored item in this topic
        best_item = None
        best_score = -1.0
        for iid in candidate_ids:
            it = item_map.get(iid)
            if it:
                s = it.get("scoring", {}).get("total_score", 0)
                if s > best_score:
                    best_score, best_item = s, it

        if not best_item:
            continue

        title = best_item["content"].get("title", "").strip()
        if len(title) > 120:
            title = title[:117] + "…"

        real_words = re.findall(r"[a-záéíóúüñA-Z]{3,}", title)
        if not title or len(real_words) < 4:
            continue

        # Collect source links (deduplicated by source name, keeping best-scored)
        seen_sources: dict[str, dict] = {}
        for iid in all_ids:
            it = item_map.get(iid)
            if not it:
                continue
            sname = it["source"].get("name", "")
            surl = it["content"].get("url", "")
            if sname and surl:
                existing = seen_sources.get(sname)
                if not existing or it.get("scoring", {}).get("total_score", 0) > existing.get("_score", 0):
                    seen_sources[sname] = {"name": sname, "url": surl, "_score": it.get("scoring", {}).get("total_score", 0)}

        source_links = [{"name": v["name"], "url": v["url"]} for v in seen_sources.values()]

        entries.append({
            "text": title,
            "url": best_item["content"].get("url", ""),
            "source_name": best_item["source"].get("name", ""),
            "source_count": n,
            "source_links": source_links,
        })

        for iid in all_ids:
            used_item_ids.add(iid)

    # Fill remaining slots from top-scored items not yet used
    if len(entries) < 5:
        sorted_items = sorted(
            items,
            key=lambda i: i.get("scoring", {}).get("total_score", 0),
            reverse=True,
        )
        for item in sorted_items:
            if len(entries) >= 5:
                break
            if item["id"] in used_item_ids:
                continue
            title = item["content"].get("title", "").strip()
            if len(title) > 120:
                title = title[:117] + "…"
            real_words = re.findall(r"[a-záéíóúüñA-Z]{3,}", title)
            if title and len(real_words) >= 4:
                source = item["source"].get("name", "")
                url = item["content"].get("url", "")
                entries.append({
                    "text": title,
                    "url": url,
                    "source_name": source,
                    "source_count": 1,
                    "source_links": [{"name": source, "url": url}] if source and url else [],
                })
                used_item_ids.add(item["id"])

    return entries


# ── Jinja2 custom filters ─────────────────────────────────────────────────────

def _filter_timeago(value: str | None) -> str:
    """Convert ISO datetime string to human-readable time-ago."""
    if not value:
        return ""
    try:
        if isinstance(value, str):
            # Handle both naive and timezone-aware ISO strings
            value = value.rstrip("Z")
            if "+" in value:
                value = value.split("+")[0]
            dt = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        else:
            return ""
        now = datetime.now(timezone.utc)
        diff = now - dt
        secs = int(diff.total_seconds())
        if secs < 0:
            return "justo ahora"
        if secs < 60:
            return "hace un momento"
        mins = secs // 60
        if mins < 60:
            return f"hace {mins} min"
        hours = mins // 60
        if hours < 24:
            return f"hace {hours}h"
        days = hours // 24
        if days == 1:
            return "ayer"
        if days < 7:
            return f"hace {days} días"
        return dt.strftime("%-d %b")
    except Exception:
        return str(value)[:10] if value else ""


def _filter_views(value: int | None) -> str:
    """Format view count: 1234567 → '1.2M', 45000 → '45K'."""
    if not value:
        return ""
    try:
        n = int(value)
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M vistas"
        if n >= 1_000:
            return f"{n//1_000}K vistas"
        return f"{n} vistas"
    except (ValueError, TypeError):
        return ""


# ── Month names in Spanish ────────────────────────────────────────────────────

_MONTHS_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}

def _month_es(month: int) -> str:
    return _MONTHS_ES.get(month, "")
