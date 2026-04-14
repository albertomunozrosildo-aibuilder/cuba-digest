#!/usr/bin/env python3
"""
Cuba Digest — main entrypoint.

Usage:
  python3 main.py --mode digest          # Full pipeline → HTML output
  python3 main.py --mode collect         # Collect only, save raw JSON
  python3 main.py --mode render          # Render from existing processed data
  python3 main.py --date 2026-04-12      # Run for a specific date
  python3 main.py --dry-run              # Collect + process, skip HTML write
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.collectors.rss_collector import RSSCollector
from src.collectors.youtube_collector import YouTubeCollector
from src.processors.clusterer import Clusterer
from src.processors.deduplicator import Deduplicator
from src.processors.enricher import Enricher
from src.processors.filter import ItemFilter
from src.processors.scorer import Scorer
from src.renderers.html_renderer import HTMLRenderer
from src.utils import load_yaml, setup_logging

# ── Config paths ──────────────────────────────────────────────────────────────

BASE_DIR     = Path(__file__).parent
SOURCES_FILE = BASE_DIR / "config" / "sources.yaml"
SETTINGS_FILE = BASE_DIR / "config" / "settings.yaml"


def load_config():
    sources  = load_yaml(SOURCES_FILE)
    settings = load_yaml(SETTINGS_FILE)
    return sources, settings


# ── Pipeline steps ────────────────────────────────────────────────────────────

def step_collect(sources: dict) -> list[dict]:
    all_items: list[dict] = []

    logging.info("📥 Collecting YouTube channels…")
    yt_cfg = sources.get("youtube", {})
    if yt_cfg:
        yt = YouTubeCollector(yt_cfg)
        yt_items = yt.collect()
        logging.info(f"   → {len(yt_items)} YouTube videos collected")
        all_items.extend(yt_items)

    logging.info("📰 Collecting RSS feeds…")
    rss_cfg = sources.get("rss", {})
    if rss_cfg:
        rss = RSSCollector(rss_cfg)
        rss_items = rss.collect()
        logging.info(f"   → {len(rss_items)} RSS articles collected")
        all_items.extend(rss_items)

    logging.info(f"✅ Total collected: {len(all_items)} items")
    return all_items


def step_process(items: list[dict], settings: dict) -> tuple[list[dict], list[dict]]:
    proc = settings.get("processing", {})

    logging.info("🔍 Filtering…")
    items = ItemFilter(proc.get("filtering", {})).filter(items)

    logging.info("🔄 Deduplicating…")
    items = Deduplicator(proc.get("deduplication", {})).deduplicate(items)

    logging.info("📊 Scoring…")
    scorer = Scorer(proc.get("scoring", {}))
    items  = scorer.score_all(items)

    logging.info("✨ Enriching…")
    items = Enricher(proc.get("enrichment", {})).enrich_all(items)

    logging.info("🗂  Clustering into topics…")
    topics = Clusterer(proc.get("clustering", {})).cluster(items)

    logging.info("📈 Re-scoring with coverage signal…")
    items = scorer.rescore_with_coverage(items, topics)

    return items, topics


def step_render(
    items: list[dict],
    topics: list[dict],
    settings: dict,
    date_str: str,
    dry_run: bool,
) -> Path | None:
    if dry_run:
        logging.info("⏭  Dry-run: skipping HTML write")
        return None

    logging.info("🎨 Rendering HTML…")
    output_cfg = settings.get("output", {})
    renderer = HTMLRenderer(output_cfg)
    return renderer.render(topics, items, date_str)


def save_raw(items: list[dict], date_str: str):
    raw_dir = BASE_DIR / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{date_str}_items.json"
    path.write_text(
        json.dumps(items, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    logging.debug(f"  Raw data saved → {path}")


def save_processed(items: list[dict], topics: list[dict], date_str: str):
    proc_dir = BASE_DIR / "data" / "processed"
    proc_dir.mkdir(parents=True, exist_ok=True)

    # Strip internal _keywords set (not JSON-serialisable)
    clean_topics = []
    for t in topics:
        ct = {k: v for k, v in t.items() if k != "_keywords"}
        clean_topics.append(ct)

    payload = {
        "date": date_str,
        "metadata": {
            "total_items": len(items),
            "videos": sum(1 for i in items if i["type"] == "video"),
            "articles": sum(1 for i in items if i["type"] == "article"),
            "topics": len(clean_topics),
        },
        "items": items,
        "topics": clean_topics,
    }
    path = proc_dir / f"{date_str}_processed.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    logging.info(f"  Processed data saved → {path}")
    return payload


def load_processed(date_str: str) -> tuple[list[dict], list[dict]]:
    path = BASE_DIR / "data" / "processed" / f"{date_str}_processed.json"
    if not path.exists():
        logging.error(f"No processed data found for {date_str}: {path}")
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("items", []), data.get("topics", [])


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Cuba Digest Generator")
    parser.add_argument(
        "--mode",
        choices=["digest", "collect", "render"],
        default="digest",
        help="Pipeline mode (default: digest = full run)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Target date YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run pipeline without writing HTML output",
    )
    args = parser.parse_args()

    # Determine date string
    if args.date:
        date_str = args.date.replace("-", "")
    else:
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    # Load config
    sources, settings = load_config()

    # Setup logging
    log_cfg = settings.get("logging", {})
    setup_logging(
        level=log_cfg.get("level", "INFO"),
        log_file=log_cfg.get("file"),
    )

    logger = logging.getLogger(__name__)
    logger.info(f"🇨🇺 Cuba Digest — mode={args.mode}  date={date_str}")

    # ── Modes ─────────────────────────────────────────────────────────────────

    if args.mode == "collect":
        items = step_collect(sources)
        save_raw(items, date_str)
        logger.info(f"Done. {len(items)} items saved to data/raw/{date_str}_items.json")

    elif args.mode == "render":
        items, topics = load_processed(date_str)
        out = step_render(items, topics, settings, date_str, dry_run=False)
        if out:
            logger.info(f"✅ Digest → {out}")

    else:  # digest (full pipeline)
        items = step_collect(sources)

        if not items:
            logger.warning("⚠️  No items collected. Check sources and network.")
            # Still produce an empty digest rather than crashing
            items, topics = [], []
        else:
            items, topics = step_process(items, settings)

        payload = save_processed(items, topics, date_str)

        out = step_render(items, topics, settings, date_str, dry_run=args.dry_run)

        # ── Summary ───────────────────────────────────────────────────────────
        meta = payload["metadata"]
        logger.info("")
        logger.info("─" * 50)
        logger.info(f"  Articles : {meta['articles']}")
        logger.info(f"  Videos   : {meta['videos']}")
        logger.info(f"  Topics   : {meta['topics']}")
        if out:
            logger.info(f"  Output   : {out}")
        logger.info("─" * 50)
        if out:
            logger.info(f"✅ Done — open {out} in your browser")


if __name__ == "__main__":
    main()
