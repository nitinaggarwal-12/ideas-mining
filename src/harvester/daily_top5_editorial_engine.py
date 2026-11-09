"""Daily Top-5 Unique In-Demand Ideas, 5-Angle Template Matcher & Mode/Length Contract Engine.

Implements the complete editorial decision pipeline:
  Daily Signal Harvest + 30-Day Rolling Dedupe Ledger
    -> Top 5 Unique Most In-Demand Ideas (diversified across 5 engineering clusters)
    -> Top 5 Orthogonal Certified Templates per Idea (drawn strictly from the 128 Best+High pool)
    -> Recommended Mode of Presentation (Carousel, Image, Short_Video, Video, Slidedeck, Slide, Doc, Text)
    -> 3-Part Mode & Platform Content-Length Budgets (Hook Fold, Per-Unit Density, Total Deliverable)
"""

from __future__ import annotations
from src.catalog.post_distribution_directory import resolve_distribution_directory_for_post

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from src.catalog.career_minting_catalog import CAREER_MINTING_TOPICS
from src.harvester.daily_post_generator import CURATED_LATEST_TOPICS, DailyLinkedInPostEngine
from src.visuals.canonical_blueprint_minter import (
    BANNED_LEGACY_GEN1_IDS,
    validate_non_legacy_template_id,
)
from src.visuals.canonical_template_registry import TEMPLATE_META, TOPIC_POSTS_T79

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
HISTORY_LEDGER_JSON = DATA_DIR / "daily_idea_history_ledger.json"
DAILY_TOP5_BRIEFING_JSON = DATA_DIR / "daily_top5_editorial_briefing.json"
SLIDES_MANIFEST_JSON = DATA_DIR / "template_google_slides_manifest.json"


# ---------------------------------------------------------------------------
# 1. Canonical 8 Presentation Modes & 3-Part Structural Length Contracts
# ---------------------------------------------------------------------------
PRESENTATION_MODE_CONTRACTS: Dict[str, Dict[str, Any]] = {
    "Carousel": {
        "mode_id": "Carousel",
        "label": "Swipeable Carousel (8–10 Slides)",
        "short_label": "Carousel",
        "primary_aspect_ratios": ["4:5 (1080×1350)", "9:16 (1080×1920)"],
        "length_budget": {
            "hook_above_fold": "Slide 1 Headline ≤ 10 words + Caption Hook ≤ 125–210 chars before '…more'",
            "per_unit_density": "25–40 words per slide (1 bold header + ≤ 3 concise bullets)",
            "total_deliverable_size": "8–10 slides (240–360 slide words) + 150–240 word post caption",
            "estimated_consumption_time": "45–60 sec swipe",
        },
        "file_formats_by_platform": {
            "linkedin": "4:5 PDF Document (≤ 100 MB, ≤ 300 pages)",
            "instagram": "2–20 individual 4:5 JPEG images (≤ 8 MB/img, zero PDF)",
            "tiktok": "2–35 individual 9:16 JPEG/WebP Photo Mode slides (≤ 20 MB/img)",
            "telegram": "4:5 PDF Document or 2–10 image album (caption ≤ 1,024 chars)",
            "facebook": "Multi-image 4:5 Page post",
        },
        "compatible_platforms": ["linkedin", "instagram", "tiktok", "telegram", "facebook"],
    },
    "Image": {
        "mode_id": "Image",
        "label": "Single @2x Infographic Poster",
        "short_label": "Image",
        "primary_aspect_ratios": ["4:5 (1840×2300 @2x)", "1:1 (2040×2080 @2x)"],
        "length_budget": {
            "hook_above_fold": "Caption Hook ≤ 180 chars (2 punchy lines above fold) + Poster Header ≤ 9 words",
            "per_unit_density": "≤ 12 words per diagram node • ≥ 11pt crisp vector labels",
            "total_deliverable_size": "1 @2x PNG/SVG poster + 160–220 word companion narrative (950–1,400 chars)",
            "estimated_consumption_time": "30 sec scan",
        },
        "file_formats_by_platform": {
            "linkedin": "PNG/JPG single image post + Comment #1 source link",
            "telegram": "PNG photo + ≤ 1,024-char executive digest",
            "instagram": "4:5 JPEG single feed poster (zero raw URLs in caption)",
            "facebook": "4:5 PNG/JPEG Page post",
            "bluesky": "PNG/JPEG (≤ 1 MB compressed) + ≤ 300 grapheme summary",
            "x": "PNG/JPEG + ≤ 280 char post (link in Reply #2)",
            "whatsapp": "1:1 or 4:5 PNG (≤ 5 MB) + ≤ 700 char executive brief",
        },
        "compatible_platforms": ["linkedin", "telegram", "instagram", "facebook", "bluesky", "x", "whatsapp"],
    },
    "Short_Video": {
        "mode_id": "Short_Video",
        "label": "Vertical 9:16 Short / Reel / TikTok",
        "short_label": "9:16 Short Video",
        "primary_aspect_ratios": ["9:16 (1080×1920 @ 30fps)"],
        "length_budget": {
            "hook_above_fold": "First 2.5 sec spoken pattern-interrupt (≤ 12 words) + Caption ≤ 90 chars",
            "per_unit_density": "5 vertical tier-zoom scenes × 8.5–9.0s (20–24 spoken words/scene)",
            "total_deliverable_size": "40–55 sec MP4 (≤ 180s YT Shorts / ≤ 90s IG Reels API) • ~110–135 spoken words",
            "estimated_consumption_time": "43 sec watch",
        },
        "file_formats_by_platform": {
            "youtube_shorts": "9:16 H.264 MP4 ≤ 180s via videos.insert + Related Video link",
            "instagram": "9:16 H.264 MP4 Reel (3s–90s, ≤ 300 MB, captions y ≤ 1490px)",
            "tiktok": "9:16 H.264 MP4 (SEND_TO_USER_INBOX or Direct Post post-audit)",
            "facebook": "9:16 H.264 MP4 Page Reel (3s–90s)",
            "telegram": "9:16 MP4 ≤ 50 MB + ≤ 1,024-char caption",
        },
        "compatible_platforms": ["youtube_shorts", "instagram", "tiktok", "facebook", "telegram"],
    },
    "Video": {
        "mode_id": "Video",
        "label": "Widescreen 16:9 Architecture Walkthrough",
        "short_label": "16:9 Video",
        "primary_aspect_ratios": ["16:9 (1920×1080 @ 30fps)"],
        "length_budget": {
            "hook_above_fold": "Title ≤ 70 chars (front-load keywords in first 50) + First 8s CLI/Metric Proof",
            "per_unit_density": "6 scenes × 7–15s (Architecture Spotlight + Live CLI Benchmark + Non-Occluding Twin)",
            "total_deliverable_size": "45s–4m MP4 (120–550 spoken words) + Timestamped Description (1,000–2,200 chars)",
            "estimated_consumption_time": "45 sec – 3 min watch",
        },
        "file_formats_by_platform": {
            "youtube": "16:9 1080p30 MP4 + 1280×720 thumbnail + timestamp chapters",
            "linkedin": "16:9 Native Video MP4 (≤ 200 MB) + 140–200 word post",
            "telegram": "16:9 MP4 (≤ 50 MB cloud Bot API) + ≤ 1,024-char summary",
            "facebook": "16:9 Native Page Video MP4",
        },
        "compatible_platforms": ["youtube", "linkedin", "telegram", "facebook"],
    },
    "Slidedeck": {
        "mode_id": "Slidedeck",
        "label": "12 / 24-Slide Executive & Technical Deck",
        "short_label": "Slidedeck",
        "primary_aspect_ratios": ["16:9 Widescreen (13.333\" × 7.5\")"],
        "length_budget": {
            "hook_above_fold": "Slide 1 Title + Slide 2 Executive BLUF Scorecard (3 quantified KPIs)",
            "per_unit_density": "45–65 on-slide words + 90–130 spoken presenter-note words per slide",
            "total_deliverable_size": "12-Slide 3-Act Deck (~650 slide words) or 24-Slide Cloudstyle 2.0 Master (~1,400 words)",
            "estimated_consumption_time": "15–30 min briefing",
        },
        "file_formats_by_platform": {
            "google_slides": "100% Native Editable Google Slides + Linked Sheets Charts (Rule 47)",
            "linkedin": "Exported 12-Slide PDF via Documents API (≤ 100 MB)",
            "telegram": "Editable .pptx + .pdf attachment (≤ 50 MB)",
        },
        "compatible_platforms": ["linkedin", "telegram"],
    },
    "Slide": {
        "mode_id": "Slide",
        "label": "Single 16:9 Executive BLUF One-Pager Slide",
        "short_label": "1-Slide BLUF",
        "primary_aspect_ratios": ["16:9 (1920×1080)"],
        "length_budget": {
            "hook_above_fold": "1 Action-Verb Assertion Title (≤ 12 words) + 3-Metric KPI Strip",
            "per_unit_density": "≤ 75 total words across 1 diagram + 3 executive design rail cards",
            "total_deliverable_size": "1 Native Editable Slide + 120–160 word executive post",
            "estimated_consumption_time": "20 sec executive read",
        },
        "file_formats_by_platform": {
            "linkedin": "16:9 PNG/PDF single-slide executive card",
            "telegram": "16:9 PNG + ≤ 900-char executive takeaway",
            "x": "16:9 crisp PNG + ≤ 280-char thesis",
            "bluesky": "16:9 PNG + ≤ 300-grapheme thesis",
            "whatsapp": "16:9 PNG + ≤ 600-char C-suite brief",
        },
        "compatible_platforms": ["linkedin", "telegram", "x", "bluesky", "whatsapp"],
    },
    "Doc": {
        "mode_id": "Doc",
        "label": "Deep-Dive Technical Blueprint Article",
        "short_label": "Technical Doc",
        "primary_aspect_ratios": ["1.91:1 Cover (1600×840) + Inline @2x Diagrams"],
        "length_budget": {
            "hook_above_fold": "TL;DR Architecture Box in first 120 words + Problem Benchmark Table",
            "per_unit_density": "4–6 H2 sections × 220–320 words + 1 runnable ADK/OSS code block + 1 #78 diagram",
            "total_deliverable_size": "1,250–1,900 words (6–9 min read) with canonical_url SEO attribution",
            "estimated_consumption_time": "7 min deep read",
        },
        "file_formats_by_platform": {
            "devto": "GFM Markdown via POST /api/articles (≤ 4 tags + canonical_url)",
            "hashnode": "GFM Markdown via GraphQL publishPost mutation",
            "substack": "Clean Rich-HTML Copy Packet + RSS 2.0 Feed import",
            "linkedin": "Long-Form LinkedIn Article (~1,500 words) or Repo README link",
        },
        "compatible_platforms": ["devto", "hashnode", "substack", "linkedin"],
    },
    "Text": {
        "mode_id": "Text",
        "label": "High-Signal Contrarian Text / Thread",
        "short_label": "Text / Thread",
        "primary_aspect_ratios": ["Pure Typography (Zero Media Container)"],
        "length_budget": {
            "hook_above_fold": "First 2 lines ≤ 190 chars (contrarian failure observation + hard metric)",
            "per_unit_density": "Short 1–2 sentence paragraphs • 4 numbered architectural rules",
            "total_deliverable_size": "LinkedIn: 140–210 words (900–1,350 chars) • X/Bluesky: 4–5 post thread • Telegram: ≤ 1,800 chars",
            "estimated_consumption_time": "35 sec read",
        },
        "file_formats_by_platform": {
            "linkedin": "Text-only REST /rest/posts + 1st-comment source URL",
            "telegram": "sendMessage Markdown/HTML (≤ 4,096 chars)",
            "bluesky": "AT-Protocol post/thread (≤ 300 graphemes/post)",
            "x": "280-char Hook Post #1 + Link in Reply #2",
            "whatsapp": "Formatted WhatsApp bold/bullet digest (≤ 800 chars)",
        },
        "compatible_platforms": ["linkedin", "telegram", "bluesky", "x", "whatsapp"],
    },
}


# ---------------------------------------------------------------------------
# 2. Sub-Domain Cluster Classifier & 5-Angle Certified Template Router
# ---------------------------------------------------------------------------
SUBDOMAIN_CLUSTERS: List[Tuple[str, str, Tuple[str, ...]]] = [
    (
        "CLUSTER_MCP_IDENTITY",
        "MCP, Tool Routing & Zero-Trust Identity",
        ("mcp", "oauth", "obo", "token", "tool", "schema", "auth", "rbac", "identity", "deputy"),
    ),
    (
        "CLUSTER_INFERENCE_KV",
        "LLM Serving, KV-Cache & Inference Goodput",
        ("kv", "prefill", "decode", "fp8", "vllm", "speculative", "goodput", "ttft", "latency", "roofline"),
    ),
    (
        "CLUSTER_CODING_EVALS",
        "Autonomous Coding Harnesses & Sandbox Evals",
        ("code", "sandbox", "openhands", "eval", "pass^k", "replay", "review", "diff", "test", "gvisor"),
    ),
    (
        "CLUSTER_MULTIAGENT_MEMORY",
        "Multi-Agent Orchestration, GraphRAG & Memory",
        ("supervisor", "multi-agent", "a2a", "memory", "rag", "graph", "episodic", "context", "funnel", "skill"),
    ),
    (
        "CLUSTER_GOVERNANCE_FINOPS",
        "Enterprise AI Governance, FinOps & SRE Reliability",
        ("shadow", "finops", "cost", "circuit", "breaker", "loop", "slo", "sre", "armor", "policy", "audit"),
    ),
]


ORTHOGONAL_TEMPLATE_ANGLES: List[Dict[str, Any]] = [
    {
        "angle_id": "ANGLE_1_ARCHITECTURE",
        "angle_label": "Architecture & Runtime Topology",
        "preferred_ids": ["T85", "T61", "T62", "T64", "T79", "T86", "T87", "T212", "T217", "T220", "T131", "T153"],
        "keywords": ("topology", "runtime", "supervisor", "tree", "hub", "gateway", "plane", "sequence", "flow"),
    },
    {
        "angle_id": "ANGLE_2_CONTRAST",
        "angle_label": "Before/After & OFF-vs-ON Contrast",
        "preferred_ids": ["T57", "T56", "T90", "T215", "T218", "T101", "T125", "T150", "T175", "T188"],
        "keywords": ("vs", "comparison", "contrast", "toggle", "shadow", "naive", "before", "blindspot", "trap"),
    },
    {
        "angle_id": "ANGLE_3_QUANTITATIVE",
        "angle_label": "Funnel, Roofline & Benchmark Matrix",
        "preferred_ids": ["T58", "T65", "T83", "T84", "T88", "T89", "T211", "T216", "T155", "T157", "T181"],
        "keywords": ("funnel", "matrix", "eval", "benchmark", "score", "metric", "budget", "latency", "compression"),
    },
    {
        "angle_id": "ANGLE_4_CHECKLIST",
        "angle_label": "Deployment Checklist & Cheat Sheet",
        "preferred_ids": ["T59", "T54", "T55", "T80", "T82", "T210", "T214", "T219", "T95", "T104", "T148"],
        "keywords": ("checklist", "cheat sheet", "workflow", "setup", "step", "review", "gate", "guide"),
    },
    {
        "angle_id": "ANGLE_5_EXECUTIVE",
        "angle_label": "Executive 2×2 Matrix, Pyramid & Roadmap",
        "preferred_ids": ["T63", "T60", "T66", "T67", "T81", "T213", "T221", "T154", "T156", "T167"],
        "keywords": ("roadmap", "quadrant", "2x2", "pyramid", "portfolio", "executive", "maturity", "curriculum"),
    },
]


CURATED_HIGH_DEMAND_SIGNALS: List[Dict[str, Any]] = [
    {
        "source_channel": "MCP & Cloud IAM • Enterprise Security",
        "title": "Zero-Bloat MCP Tool Search with Per-Turn RFC 8693 OAuth 2.1 On-Behalf-Of Exchange",
        "summary": "Replaces 55K-token static MCP tool dumps and shared service keys with hybrid BM25+Dense Top-4 tool search, frozen system prefixes (94.2% KV hit), and 5-minute narrow-audience OBO JWTs.",
        "primary_url": "https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization",
        "published_at": "2026-11-04",
        "metrics_hint": "55,240 → 1,380 schema tokens (-97.5%) • 4.09x faster p95 • 0 cross-tenant OBO leaks",
        "corroborating_sources": ["MCP Spec", "Google Cloud IAM STS", "GitHub Breakout"],
    },
    {
        "source_channel": "LLM Inference Systems • GPU Serving",
        "title": "Disaggregated Prefill-Decode Pools with FP8 KV-Cache & Speculative Goodput Routing",
        "summary": "Splits compute-bound prefill workers (TTFT) from memory-bandwidth-bound decode workers (TPOT) over RDMA/NVLink with prefix-aware routing and quantized FP8 KV blocks.",
        "primary_url": "https://docs.vllm.ai/en/latest/",
        "published_at": "2026-11-04",
        "metrics_hint": "-50% KV HBM footprint • +2.6x p99 SLO-compliant Goodput • <4% block fragmentation",
        "corroborating_sources": ["vLLM Docs", "arXiv cs.DC", "Hacker News Frontpage"],
    },
    {
        "source_channel": "Autonomous SWE • Sandbox Verification",
        "title": "Orthogonal Builder-vs-Judge Coding Agents Inside Isolated gVisor Replay Sandboxes",
        "summary": "Eliminates circular self-approval in coding agents by pairing a fast Builder model with an orthogonal Judge model gated on seeded defect replay suites, DOM geometry checks, and git SHA receipts.",
        "primary_url": "https://docs.all-hands.dev/usage/architecture/runtime",
        "published_at": "2026-11-04",
        "metrics_hint": "pass^5 stability 41% → 89% • 0 unverified commits • 100% deterministic test gate",
        "corroborating_sources": ["OpenHands Runtime", "SWE-bench Verified", "arXiv cs.SE"],
    },
    {
        "source_channel": "Multi-Agent Systems • Context Engineering",
        "title": "Hierarchical Supervisor Delegation with 5-Stage Progressive Context Compression (1M → 2K)",
        "summary": "Prevents context rot across multi-agent A2A workflows by isolating noisy worker tool traces inside sub-sessions and returning only schema-validated artifacts to the root supervisor.",
        "primary_url": "https://google.github.io/adk-docs/",
        "published_at": "2026-11-04",
        "metrics_hint": "1,000,000 → 2,000 precision tokens • -78% multi-hop hallucination rate • 3.1x lower cost",
        "corroborating_sources": ["Google ADK Docs", "Linux Foundation A2A", "HuggingFace Papers"],
    },
    {
        "source_channel": "AI Platform FinOps & CISO Governance",
        "title": "Shadow AI Discovery & 3-Tier Semantic Model Cascade with Circuit-Breaker Loop Guards",
        "summary": "Brings unsanctioned departmental AI pipelines behind a unified AI Gateway enforcing Model Armor PII/prompt shields, semantic step deduplication, and Flash-to-Argon complexity routing.",
        "primary_url": "https://cloud.google.com/security-command-center/docs/model-armor-overview",
        "published_at": "2026-11-04",
        "metrics_hint": "24 shadow pipelines governed • -68% blended inference spend • 0 runaway retry loops",
        "corroborating_sources": ["Google Cloud Model Armor", "FinOps Foundation", "Enterprise CISO Brief"],
    },
]


def _classify_cluster(text: str) -> Tuple[str, str]:
    lowered = text.lower()
    best_id, best_label = SUBDOMAIN_CLUSTERS[0][0], SUBDOMAIN_CLUSTERS[0][1]
    best_hits = -1
    for cid, clabel, kws in SUBDOMAIN_CLUSTERS:
        hits = sum(1 for kw in kws if kw in lowered)
        if hits > best_hits:
            best_hits = hits
            best_id, best_label = cid, clabel
    return best_id, best_label


def _fingerprint_topic(title: str, primary_url: str) -> str:
    norm_title = re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()
    core_words = " ".join(norm_title.split()[:8])
    norm_url = (primary_url or "").strip().rstrip("/").lower()
    raw = f"{core_words}|{norm_url}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _load_slides_map() -> Dict[str, Dict[str, Any]]:
    if SLIDES_MANIFEST_JSON.exists():
        try:
            return json.loads(SLIDES_MANIFEST_JSON.read_text(encoding="utf-8")).get("slides", {})
        except Exception:
            return {}
    return {}


def _build_full_certified_catalog_index() -> Dict[str, Dict[str, Any]]:
    """Index all 128 certified Best+High templates + 23 T79 spine variants (zero legacy T02-T52)."""
    slides_map = _load_slides_map()
    catalog: Dict[str, Dict[str, Any]] = {}
    for tid, meta in TEMPLATE_META.items():
        validate_non_legacy_template_id(tid)
        slide_entry = slides_map.get(tid) or {}
        catalog[tid] = {
            "id": tid,
            "name": meta.get("name", tid),
            "best_for_short": meta.get("best_for_short", ""),
            "when_to_use": str(meta.get("when_to_use", "")).replace("`", ""),
            "quality_tier": meta.get("quality_tier", "Best"),
            "category": meta.get("category", "Certified Infographic"),
            "svg_url": f"/assets/template-gallery/{tid}.svg",
            "png_url": f"/assets/template-gallery/{tid}.png",
            "gif_url": f"/assets/template-gallery/{tid}.gif",
            "pptx_url": f"/assets/template-gallery/{tid}.pptx" if (WORKSPACE_ROOT / "assets" / "template-gallery" / f"{tid}.pptx").exists() else "",
            "drawio_url": f"/assets/template-gallery/{tid}.drawio" if (WORKSPACE_ROOT / "assets" / "template-gallery" / f"{tid}.drawio").exists() else "",
            "google_slides_url": slide_entry.get("googleSlidesEditUrl", ""),
        }
    for tp in TOPIC_POSTS_T79:
        tid = tp["id"]
        validate_non_legacy_template_id(tid)
        if tid not in catalog:
            slide_entry = slides_map.get(tid) or {}
            catalog[tid] = {
                "id": tid,
                "name": tp.get("name", tid),
                "best_for_short": tp.get("hot_topic", "4-Tier Canonical Spine"),
                "when_to_use": tp.get("when_to_use", "4-tier vertical architectural spine with quantitative footer."),
                "quality_tier": "Best",
                "category": "Canonical 4-Tier Spine",
                "svg_url": f"/assets/template-gallery/{tid}.svg",
                "png_url": f"/assets/template-gallery/{tid}.png",
                "gif_url": f"/assets/template-gallery/{tid}.gif",
                "pptx_url": f"/assets/template-gallery/{tid}.pptx" if (WORKSPACE_ROOT / "assets" / "template-gallery" / f"{tid}.pptx").exists() else "",
                "drawio_url": f"/assets/template-gallery/{tid}.drawio" if (WORKSPACE_ROOT / "assets" / "template-gallery" / f"{tid}.drawio").exists() else "",
                "google_slides_url": slide_entry.get("googleSlidesEditUrl", ""),
            }
    return catalog


def recommend_mode_for_idea_and_template(idea: Dict[str, Any], template: Dict[str, Any], angle_id: str) -> Dict[str, Any]:
    """Deterministically recommend the #1 highest-leverage presentation mode for (idea, template)."""
    tid = template["id"]
    text = f"{idea.get('title', '')} {idea.get('summary', '')} {template.get('name', '')}".lower()

    if tid in ("T85", "T86", "T87", "T88", "T89") or "walkthrough" in text or "mcp" in text:
        primary_mode = "Carousel"
        secondary_modes = ["Short_Video", "Video", "Slidedeck", "Image", "Doc"]
        rationale = (
            f"{tid} packs a 4-tier architecture spine + benchmark bar: an 8-slide 4:5 Carousel maximizes "
            "LinkedIn/Instagram swipe dwell time while pairing directly with a 43s 9:16 Vertical Short."
        )
    elif angle_id == "ANGLE_2_CONTRAST":
        primary_mode = "Image"
        secondary_modes = ["Carousel", "Short_Video", "Text", "Slide"]
        rationale = (
            f"{tid} is an instant A-vs-B visual contrast poster: a single @2x 4:5 Infographic stops feed scroll "
            "in <2 seconds on LinkedIn, Telegram, Instagram, and X."
        )
    elif angle_id == "ANGLE_3_QUANTITATIVE":
        primary_mode = "Doc" if ("benchmark" in text or "goodput" in text or "prefill" in text) else "Carousel"
        secondary_modes = ["Carousel", "Image", "Slidedeck", "Video"]
        rationale = (
            f"{tid} carries high quantitative telemetry density: {primary_mode} mode gives practitioners "
            "both the visual roofline/funnel and reproducible configuration thresholds."
        )
    elif angle_id == "ANGLE_4_CHECKLIST":
        primary_mode = "Carousel"
        secondary_modes = ["Image", "Doc", "Short_Video", "Text"]
        rationale = (
            f"{tid} structures sequential implementation gates: 1 gate per slide in Carousel mode drives "
            "high bookmark/save rates across LinkedIn, Instagram, and TikTok Photo Mode."
        )
    else:
        primary_mode = "Slidedeck" if template.get("google_slides_url") else "Image"
        secondary_modes = ["Image", "Carousel", "Slide", "Doc"]
        rationale = (
            f"{tid} frames executive portfolio/roadmap trade-offs: {primary_mode} mode equips Principal Architects "
            "for leadership reviews and C-suite stakeholder alignment."
        )

    return {
        "recommended_mode": primary_mode,
        "secondary_modes": secondary_modes,
        "rationale": rationale,
        "length_budget": PRESENTATION_MODE_CONTRACTS[primary_mode]["length_budget"],
    }


class DailyTop5EditorialEngine:
    """Generates Daily Top-5 Unique In-Demand Ideas x 5 Orthogonal Templates x 8 Mode/Length Contracts."""

    def __init__(self) -> None:
        self.legacy_post_engine = DailyLinkedInPostEngine()
        self.template_catalog = _build_full_certified_catalog_index()

    def _load_history_ledger(self) -> Dict[str, Any]:
        if HISTORY_LEDGER_JSON.exists():
            try:
                return json.loads(HISTORY_LEDGER_JSON.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"window_days": 30, "entries": []}

    def _save_history_ledger(self, edition_date: str, selected_ideas: List[Dict[str, Any]]) -> Dict[str, Any]:
        ledger = self._load_history_ledger()
        try:
            ref_dt = datetime.strptime(edition_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            ref_dt = datetime.now(timezone.utc)
        cutoff_str = (ref_dt - timedelta(days=30)).strftime("%Y-%m-%d")

        # Keep entries within rolling 30-day window from OTHER dates, then upsert today's 5 ideas
        kept = [
            e
            for e in ledger.get("entries", [])
            if str(e.get("edition_date", "")) >= cutoff_str and e.get("edition_date") != edition_date
        ]
        for idea in selected_ideas:
            kept.append(
                {
                    "edition_date": edition_date,
                    "fingerprint": idea["fingerprint"],
                    "idea_id": idea["id"],
                    "title": idea["title"],
                    "primary_url": idea["primary_url"],
                    "cluster_id": idea["cluster_id"],
                }
            )
        updated = {
            "window_days": 30,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "active_ledger_count": len(kept),
            "entries": kept,
        }
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        HISTORY_LEDGER_JSON.write_text(json.dumps(updated, indent=2), encoding="utf-8")
        return updated

    def _score_demand(self, raw_topic: Dict[str, Any]) -> Dict[str, Any]:
        base_scores = self.legacy_post_engine.score_topic_candidate(raw_topic)
        corroborators = list(raw_topic.get("corroborating_sources") or [])
        if not corroborators:
            ch = str(raw_topic.get("source_channel") or "Primary Signal")
            corroborators = [s.strip() for s in ch.split("•") if s.strip()]
            if "arxiv.org" in str(raw_topic.get("primary_url", "")):
                corroborators.append("arXiv Preprint")
            elif "github.com" in str(raw_topic.get("primary_url", "")):
                corroborators.append("GitHub Velocity")
        corroboration_bonus = min(6.0, len(corroborators) * 1.8)
        demand_score = min(
            99.5,
            round(
                0.35 * base_scores["practitioner_utility"]
                + 0.25 * base_scores["novelty"]
                + 0.25 * base_scores["quantitative_density"]
                + 0.15 * base_scores["visualizability"]
                + corroboration_bonus,
                1,
            ),
        )
        return {
            **base_scores,
            "demand_score": demand_score,
            "corroborating_sources": corroborators[:4],
        }

    def match_top5_orthogonal_templates(self, idea: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select 5 distinct certified templates spanning the 5 orthogonal visual storytelling angles."""
        idea_text = f"{idea.get('title', '')} {idea.get('summary', '')} {idea.get('metrics_hint', '')}".lower()
        idea_tokens = set(re.findall(r"[a-z0-9]{3,}", idea_text))
        used_ids: Set[str] = set()
        ranked_matches: List[Dict[str, Any]] = []

        for angle in ORTHOGONAL_TEMPLATE_ANGLES:
            best_tid: Optional[str] = None
            best_score = -1.0

            # Score all 128+23 certified templates for this specific orthogonal angle
            for tid, tmeta in self.template_catalog.items():
                if tid in used_ids or tid in BANNED_LEGACY_GEN1_IDS:
                    continue
                hay = f"{tmeta['name']} {tmeta['best_for_short']} {tmeta['when_to_use']}".lower()
                hay_tokens = set(re.findall(r"[a-z0-9]{3,}", hay))

                overlap = len(idea_tokens & hay_tokens)
                angle_kw_hits = sum(1 for kw in angle["keywords"] if kw in hay)
                pref_bonus = 0.0
                if tid in angle["preferred_ids"]:
                    pref_idx = angle["preferred_ids"].index(tid)
                    pref_bonus = 18.0 - pref_idx * 1.1
                tier_bonus = 5.0 if tmeta["quality_tier"] == "Best" else 2.0
                slides_bonus = 2.5 if tmeta.get("google_slides_url") else 0.0

                score = 68.0 + overlap * 2.6 + angle_kw_hits * 2.4 + pref_bonus + tier_bonus + slides_bonus
                if score > best_score:
                    best_score = score
                    best_tid = tid

            if not best_tid:
                continue
            used_ids.add(best_tid)
            tmeta = self.template_catalog[best_tid]
            fit_score = min(99.2, round(best_score, 1))
            mode_rec = recommend_mode_for_idea_and_template(idea, tmeta, angle["angle_id"])
            ranked_matches.append(
                {
                    "template_id": best_tid,
                    "name": tmeta["name"],
                    "quality_tier": tmeta["quality_tier"],
                    "angle_id": angle["angle_id"],
                    "angle_label": angle["angle_label"],
                    "fit_score": fit_score,
                    "best_for_short": tmeta["best_for_short"],
                    "when_to_use": tmeta["when_to_use"],
                    "svg_url": tmeta["svg_url"],
                    "png_url": tmeta["png_url"],
                    "gif_url": tmeta["gif_url"],
                    "pptx_url": tmeta["pptx_url"],
                    "drawio_url": tmeta["drawio_url"],
                    "google_slides_url": tmeta["google_slides_url"],
                    "recommended_mode": mode_rec["recommended_mode"],
                    "secondary_modes": mode_rec["secondary_modes"],
                    "mode_rationale": mode_rec["rationale"],
                    "mode_length_budget": mode_rec["length_budget"],
                }
            )

        ranked_matches.sort(key=lambda item: item["fit_score"], reverse=True)
        for idx, m in enumerate(ranked_matches, start=1):
            m["rank"] = idx
            m["is_primary_recommended"] = idx == 1
        return ranked_matches[:5]

    def generate_daily_top5_briefing(
        self,
        edition_date: Optional[str] = None,
        topic_query: str = "",
        use_live_network: bool = True,
    ) -> Dict[str, Any]:
        ed_date = edition_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ledger = self._load_history_ledger()
        prior_fingerprints: Set[str] = {
            str(e.get("fingerprint"))
            for e in ledger.get("entries", [])
            if e.get("edition_date") != ed_date
        }

        from src.harvester.autonomous_omnichannel_miner import (
            fetch_creator_syndicate_rss_live,
            fetch_devto_practitioner_pulse_live,
            fetch_reddit_practitioner_json_live,
            prescribe_format_duration_channels_and_groups,
        )

        raw_candidates: List[Dict[str, Any]] = []
        if use_live_network:
            raw_candidates.extend(fetch_creator_syndicate_rss_live(limit_per_feed=2))
            raw_candidates.extend(fetch_devto_practitioner_pulse_live(limit=3))
            raw_candidates.extend(fetch_reddit_practitioner_json_live(limit_per_sub=2))
        if use_live_network or topic_query.strip():
            raw_candidates.extend(
                self.legacy_post_engine.harvest_latest_topics(
                    topic_query=topic_query, use_live_network=use_live_network
                )
            )
        for sig in CURATED_HIGH_DEMAND_SIGNALS:
            raw_candidates.append(dict(sig))
        for cur in CURATED_LATEST_TOPICS:
            raw_candidates.append(dict(cur))
        for mint in CAREER_MINTING_TOPICS:
            raw_candidates.append(
                {
                    "source_channel": "Google Cloud ADK • 2026 Career-Minting Signal",
                    "title": mint["title"],
                    "summary": f"{mint['analogy']} {mint['golden_rule']}",
                    "primary_url": mint.get("primary_source_url") or "https://github.com/nitinaggarwal-12/ideas-mining",
                    "published_at": ed_date,
                    "metrics_hint": mint["promo_impact"],
                }
            )

        enriched: List[Dict[str, Any]] = []
        seen_batch_fps: Set[str] = set()
        for cand in raw_candidates:
            title = str(cand.get("title") or "").strip()
            url = str(cand.get("primary_url") or "").strip()
            if not title:
                continue
            fp = _fingerprint_topic(title, url)
            if fp in seen_batch_fps:
                continue
            seen_batch_fps.add(fp)
            is_fresh_30d = fp not in prior_fingerprints
            cid, clabel = _classify_cluster(f"{title} {cand.get('summary', '')}")
            scores = self._score_demand(cand)
            enriched.append(
                {
                    **cand,
                    "fingerprint": fp,
                    "unique_30d": is_fresh_30d,
                    "cluster_id": cid,
                    "cluster_label": clabel,
                    "scores": scores,
                }
            )

        # Prioritize 30-day unseen topics first, then highest demand_score
        enriched.sort(
            key=lambda x: (1 if x["unique_30d"] else 0, x["scores"]["demand_score"]),
            reverse=True,
        )

        # Pass 1: 1 unseen (30-day unique) top idea per distinct engineering cluster for maximum breadth
        selected: List[Dict[str, Any]] = []
        used_clusters: Set[str] = set()
        for item in enriched:
            if item["unique_30d"] and item["cluster_id"] not in used_clusters:
                selected.append(item)
                used_clusters.add(item["cluster_id"])
                if len(selected) == 5:
                    break
        # Pass 2: fill any remaining slots from 30-day unseen candidates first
        if len(selected) < 5:
            selected_fps = {s["fingerprint"] for s in selected}
            for item in enriched:
                if item["unique_30d"] and item["fingerprint"] not in selected_fps:
                    selected.append(item)
                    selected_fps.add(item["fingerprint"])
                    if len(selected) == 5:
                        break
        # Pass 3: emergency fallback only if < 5 unseen candidates exist across all sources
        if len(selected) < 5:
            selected_fps = {s["fingerprint"] for s in selected}
            for item in enriched:
                if item["fingerprint"] not in selected_fps:
                    selected.append(item)
                    selected_fps.add(item["fingerprint"])
                    if len(selected) == 5:
                        break

        ideas_payload: List[Dict[str, Any]] = []
        for rank_idx, idea in enumerate(selected[:5], start=1):
            idea_id = f"TOP5-{ed_date.replace('-', '')}-{rank_idx:02d}"
            top5_templates = self.match_top5_orthogonal_templates(idea)
            lead_tpl = top5_templates[0]
            ideas_payload.append(
                {
                    "id": idea_id,
                    "rank": rank_idx,
                    "edition_date": ed_date,
                    "fingerprint": idea["fingerprint"],
                    "unique_30d_verified": bool(idea["unique_30d"]),
                    "cluster_id": idea["cluster_id"],
                    "cluster_label": idea["cluster_label"],
                    "title": idea["title"],
                    "summary": idea["summary"],
                    "primary_url": idea["primary_url"],
                    "source_channel": idea.get("source_channel", "Verified Signal"),
                    "published_at": idea.get("published_at", ed_date),
                    "metrics_hint": idea.get("metrics_hint", "Verified production architecture telemetry"),
                    "scores": idea["scores"],
                    "default_template_id": lead_tpl["template_id"],
                    "default_recommended_mode": lead_tpl["recommended_mode"],
                    "omnichannel_prescription": prescribe_format_duration_channels_and_groups(idea),
                    "distribution_directory": resolve_distribution_directory_for_post(
                        post_id=idea_id,
                        title=idea["title"],
                        cluster_id=idea["cluster_id"],
                        primary_url=idea["primary_url"],
                        source_channel=idea.get("source_channel", "Verified Signal"),
                    ),
                    "matching_templates": top5_templates,
                }
            )

        updated_ledger = self._save_history_ledger(ed_date, ideas_payload)
        briefing = {
            "status": "READY",
            "edition_date": ed_date,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "topic_query": topic_query,
            "ideas_count": len(ideas_payload),
            "templates_per_idea": 5,
            "certified_pool_size": len(TEMPLATE_META),
            "dedupe_ledger_window_days": updated_ledger["window_days"],
            "dedupe_ledger_entries": updated_ledger["active_ledger_count"],
            "mode_contracts": PRESENTATION_MODE_CONTRACTS,
            "ideas": ideas_payload,
        }
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_TOP5_BRIEFING_JSON.write_text(json.dumps(briefing, indent=2), encoding="utf-8")
        return briefing

    def get_or_create_briefing(self, edition_date: str = "") -> Dict[str, Any]:
        if DAILY_TOP5_BRIEFING_JSON.exists():
            try:
                cached = json.loads(DAILY_TOP5_BRIEFING_JSON.read_text(encoding="utf-8"))
                if cached.get("certified_pool_size") != len(TEMPLATE_META):
                    cached["certified_pool_size"] = len(TEMPLATE_META)
                    DAILY_TOP5_BRIEFING_JSON.write_text(json.dumps(cached, indent=2), encoding="utf-8")
                for _it in cached.get("ideas", []):
                    if "distribution_directory" not in _it:
                        _it["distribution_directory"] = resolve_distribution_directory_for_post(
                            post_id=_it.get("id", ""),
                            title=_it.get("title", ""),
                            cluster_id=_it.get("cluster_id", ""),
                            primary_url=_it.get("primary_url", ""),
                            source_channel=_it.get("source_channel", "Verified Signal"),
                        )
                if not edition_date or cached.get("edition_date") == edition_date:
                    return cached
            except Exception:
                pass
        return self.generate_daily_top5_briefing(edition_date=edition_date or None, use_live_network=False)
