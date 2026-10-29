#!/usr/bin/env python3
"""CLI & Daily Cron Entrypoint for the Latest-Topic LinkedIn Post & Visual Generator.

Usage:
  python3 scripts/generate_daily_posts.py --count 6
  python3 scripts/generate_daily_posts.py --topic "speculative decoding KV cache" --style STYLE-06 --count 3
  python3 scripts/generate_daily_posts.py --date 2026-10-29 --offline --count 6
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from src.harvester.daily_post_generator import CREATOR_STYLE_ARCHETYPES, DailyLinkedInPostEngine


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Harvest daily latest AI/systems topics and generate publication-ready LinkedIn posts + custom 2D SVGs."
    )
    parser.add_argument("--date", default="", help="Edition date (YYYY-MM-DD); defaults to today UTC")
    parser.add_argument("--count", type=int, default=6, help="Number of daily posts to generate (1..12, default: 6)")
    parser.add_argument("--topic", default="", help="Optional topic focus query (e.g., 'agent evals pass^k')")
    parser.add_argument(
        "--style",
        default="AUTO",
        choices=["AUTO"] + list(CREATOR_STYLE_ARCHETYPES.keys()),
        help="Creator style archetype code (AUTO or STYLE-01..STYLE-06)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use curated ground-truth signals without live network calls",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON edition payload to stdout")
    args = parser.parse_args()

    engine = DailyLinkedInPostEngine()
    edition = engine.generate_daily_edition(
        edition_date=args.date or None,
        count=args.count,
        topic_query=args.topic,
        creator_style=args.style,
        use_live_network=not args.offline,
    )

    if args.json:
        print(json.dumps(edition, indent=2, ensure_ascii=False))
        return 0

    print(
        f"✅ Generated Daily LinkedIn Edition [{edition['edition_date']}] — "
        f"{edition['post_count']} posts persisted to {engine.store_path.relative_to(WORKSPACE_ROOT)}"
    )
    for p in edition["posts"]:
        print(
            f"  [{p['rank']:02d}] {p['id']} | Score {p['scores']['composite_score']}/100 | "
            f"{p['style_code']} ({p['creator_inspiration']} • {p['canonical_template_id']}) | "
            f"{p['topic_title'][:72]}"
        )
        print(f"       SVG: {p['custom_dynamic_svg_url']} | Source: {p['primary_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
