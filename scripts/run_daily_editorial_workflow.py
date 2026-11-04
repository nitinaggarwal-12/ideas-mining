#!/usr/bin/env python3
"""Automated Daily Top-5 Editorial & Multi-Platform Staging CLI (`ideas-minting`).

Executes end-to-end:
1. Harvests & deduplicates Top 5 Unique In-Demand Agentic AI Ideas (30-day rolling ledger).
2. Pairs each idea with 5 Orthogonal Certified Templates (from the 116 Best+High pool).
3. Computes Recommended Mode + 3-Part Mode/Platform Content-Length Budgets.
4. Transcodes 4:5 & 9:16 Multi-JPEG Carousels + 9:16 Safe-Zone Short Video for the lead idea.
5. Stages compliant multi-platform packages into the HITL Publishing Outbox (`data/publishing_outbox_ledger.json`).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

from src.harvester.daily_top5_editorial_engine import DailyTop5EditorialEngine
from src.publisher.multi_platform_publisher import MultiPlatformOutboxManager
from src.video.multi_platform_transcoder import (
    compile_carousel_jpegs,
    compile_vertical_9x16_short_video,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Daily Top-5 Editorial & Multi-Platform Auto-Publishing Workflow.")
    parser.add_argument("--date", default="", help="Optional YYYY-MM-DD edition date")
    parser.add_argument("--query", default="", help="Optional focus query")
    parser.add_argument("--offline", action="store_true", help="Skip live network polling and use curated signal floor")
    parser.add_argument("--transcode-lead", action="store_true", help="Transcode 4:5/9:16 Carousel JPEGs + 9:16 Short MP4 for #1 idea")
    parser.add_argument(
        "--stage-platforms",
        default="linkedin,telegram,youtube_shorts,instagram,tiktok,devto,whatsapp",
        help="Comma-separated platforms to stage into the HITL Outbox for Idea #1",
    )
    parser.add_argument("--auto-approve-tier1", action="store_true", help="Dispatch/validate staged items immediately")
    args = parser.parse_args()

    engine = DailyTop5EditorialEngine()
    briefing = engine.generate_daily_top5_briefing(
        edition_date=args.date or None,
        topic_query=args.query,
        use_live_network=not args.offline,
    )

    lead_idea = briefing["ideas"][0]
    lead_tpl = lead_idea["matching_templates"][0]

    transcode_summary = {}
    if args.transcode_lead:
        spec = {
            "id": lead_idea["id"],
            "title": lead_idea["title"],
            "summary": lead_idea["summary"],
            "template_id": lead_tpl["template_id"],
            "cluster_label": lead_idea.get("cluster_label", ""),
            "metrics_hint": lead_idea["metrics_hint"],
            "source_channel": lead_idea["source_channel"],
        }
        transcode_summary["carousel"] = compile_carousel_jpegs(spec, force=True)
        transcode_summary["short_video"] = compile_vertical_9x16_short_video(spec, force=True)

    platforms = [p.strip() for p in args.stage_platforms.split(",") if p.strip()]
    outbox = MultiPlatformOutboxManager()
    staged = outbox.stage_packages(
        idea=lead_idea,
        template=lead_tpl,
        mode=lead_idea["default_recommended_mode"],
        platforms=platforms,
    )
    dispatched = None
    if args.auto_approve_tier1:
        ids = [r["outbox_id"] for r in staged["staged"]]
        dispatched = outbox.approve_and_publish(ids)

    print(
        json.dumps(
            {
                "edition_date": briefing["edition_date"],
                "ideas_count": briefing["ideas_count"],
                "lead_idea_id": lead_idea["id"],
                "lead_template_id": lead_tpl["template_id"],
                "recommended_mode": lead_idea["default_recommended_mode"],
                "staged_platforms": [r["platform_id"] for r in staged["staged"]],
                "auto_approved_count": len(dispatched["processed"]) if dispatched else 0,
                "transcoded_lead": bool(transcode_summary),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
