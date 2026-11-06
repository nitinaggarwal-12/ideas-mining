"""Canonical Template Registry — 116 Certified Unique `Best` + `High` Visual Templates.

Consolidates the entire visual catalog with zero legacy Gen-1 raw Python SVG box approximations (`Law 18` / `Rule 57B`):
- 15 PromptCanvas Canonical `Best` Blueprints:
    `T54`–`T67` (PromptCanvas `#53`–`#66` Infographics) + `T79` (Canonical 4-Tier Spine Archetype, hosting `23` Topic Posts `T01, T53, T68–T78, T80–T89` on disk and in `T79.topic_posts`).
- 24 Kept Session `Best` Blueprints (`Gen-4` Sculptural Posters):
    `T90, T91, T94, T98, T100, T101, T103, T105, T110, T111, T115, T125, T129, T131, T150, T152, T159, T175, T176, T178, T188, T190, T191, T195`.
- 33 Refactored Session `Best` Blueprints (`Gen-5` Open-Drafting-Grid Sculptural Posters):
    `T95, T102, T104, T106, T107, T108, T118, T124, T128, T130, T142, T145, T148, T153, T155, T158, T163, T165, T167, T168, T169, T171, T181, T183, T185, T186, T192, T194, T197, T198, T199, T203, T207`.
- 44 Kept Session `High` Blueprints (`Gen-4` Certified High):
    `T92, T93, T96, T97, T99, T109, T112, T117, T119, T120, T121, T122, T123, T127, T133, T136, T137, T140, T146, T151, T154, T157, T160, T161, T162, T164, T170, T172, T173, T174, T177, T179, T184, T187, T193, T196, T200, T201, T202, T204, T205, T206, T208, T209`.

Total Certified Gallery Templates = `116` (`72 Best` + `44 High`, `0 Medium/Low/Worst`).
All `38` canonical PromptCanvas/Spine Draw.io + PNG + Google Slides assets (`T01, T53–T89`) remain intact on disk (`Law 18`).
"""

from __future__ import annotations

import base64
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.visuals.canonical_flow_svg import (
    BLUE,
    CSS,
    GREEN,
    NAVY,
    PURPLE,
    RED,
    TEAL,
    _esc,
    _flow,
    audit_zero_origin_svg,
    flatten_svg_zero_origin,
    resolve_chrome_bin,
    resolve_ffmpeg_bin,
)

Point = Tuple[float, float]

_WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_CANONICAL_REF_DIR = _WORKSPACE_ROOT / "assets" / "canonical-ref"
_SESSION_META_PATH = _WORKSPACE_ROOT / "data" / "session_templates_metadata.json"
_B64_CACHE: Dict[str, Tuple[int, int, int, str, str]] = {}


# ----------------------------------------------------------------------------------------------------------------------
# 15 PromptCanvas Canonical `Best` Templates (T54-T67 + T79 4-Tier Spine Archetype)
# ----------------------------------------------------------------------------------------------------------------------
PROMPTCANVAS_BEST_META: Dict[str, Dict[str, Any]] = {
    "T54": {
        "name": "PromptCanvas #53: Dual-Agent Process Workflow",
        "best_for_short": "Primary Coding Agent + Reviewer Agent loop",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Educational"],
        "when_to_use": "Show a 3-band workflow pairing a Primary Coding Agent with an independent Reviewer Agent across Install, Tool Mounting (YES/NO gate), and Recheck.",
        "dynamic": "Packets flow across all 3 horizontal bands, the YES/NO tool readiness diamond, and the bottom RECHECK feedback loop.",
        "lineage": "PromptCanvas Blueprint #53 (Process Workflow Infographic) • Gemini Code Assist + OpenHands",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Software & Agent Engineers",
        "best_for": "3-band step-by-step workflow pairing a Primary Coding Agent with an independent Reviewer Agent and YES/NO tool gates",
        "inspired_by": "PromptCanvas Blueprint #53 • Google Cloud Gemini Code Assist + OpenHands",
        "accent": PURPLE,
        "hot_topic": "Dual-Agent Coding Workflow: Primary Builder + Adversarial Reviewer Loop",
    },
    "T55": {
        "name": "PromptCanvas #54: Computer-Use Cheat Sheet Card",
        "best_for_short": "7 setup steps + 4 copy-ready @Browser jobs",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Easy to understand", "Working solution"],
        "when_to_use": "Provide a 2-column executive quick-start card with 7 setup steps, a copy-paste prompt formula, and 4 high-ROI browser/computer-use workflows.",
        "dynamic": "Animated conduit connects the 7-step setup checklist and prompt formula to the 2x2 grid of production @Browser jobs.",
        "lineage": "PromptCanvas Blueprint #54 (Cheat Sheet Quick-Start Card) • Vertex Computer Use & OpenHands Browser",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "AI Builders & Product Teams",
        "best_for": "2-column quick-start cheat sheet with 7 setup steps, copy-paste prompt formula, and 4 high-ROI browser/computer-use jobs",
        "inspired_by": "PromptCanvas Blueprint #54 • Google Cloud Vertex AI Computer Use + OpenHands",
        "accent": BLUE,
        "hot_topic": "Autonomous Computer-Use Cheat Sheet: 7 Setup Steps & 4 Production Prompts",
    },
    "T56": {
        "name": "PromptCanvas #55: Shadow AI Bubble Conceptual",
        "best_for_short": "4 perceived tools vs. 24 shadow AI pipelines",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Professional knowledge sharing", "Governance"],
        "when_to_use": "Contrast what leadership thinks is running (4 approved tools) against 24 shadow AI tools across engineering, meetings, sales, and legal.",
        "dynamic": "Blind-spot conduit links the 4 executive assumption cards to 24 color-coded shadow AI bubbles and the 4-control governance bridge.",
        "lineage": "PromptCanvas Blueprint #55 (Bubble Conceptual Infographic) • Enterprise Shadow AI & Model Armor Gateway",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "CISOs, Architects & AI Platform Leads",
        "best_for": "Contrasting executive perception (4 approved tools) against 24 shadow AI tools running across engineering, sales, and ops",
        "inspired_by": "PromptCanvas Blueprint #55 • Google Cloud Model Armor + Apigee + LiteLLM",
        "accent": RED,
        "hot_topic": "The AI Nobody Signed Off: Governing 24 Shadow AI Tools via an AI Gateway",
    },
    "T57": {
        "name": "PromptCanvas #56: Side-by-Side Runtime Toggles",
        "best_for_short": "Stateless API (OFF) vs. Agent Runtime (ON)",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Grounded concepts", "Evaluation results"],
        "when_to_use": "Compare stateless foundation model inference (OFF toggles) against a managed enterprise agent runtime (ON toggles) across 5 architecture pillars.",
        "dynamic": "5 parallel upgrade conduits flow from red OFF stateless cards through the central dimension spine to green ON managed runtime cards.",
        "lineage": "PromptCanvas Blueprint #56 (Side-by-Side Comparison Infographic) • Vertex AI Agent Engine vs. Raw API",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Enterprise Cloud Architects",
        "best_for": "5-row central-spine comparison with OFF vs. ON vector toggle switches comparing stateless APIs against managed runtimes",
        "inspired_by": "PromptCanvas Blueprint #56 • Google Cloud Vertex AI Agent Engine + LangGraph",
        "accent": GREEN,
        "hot_topic": "Stateless LLM API (OFF) vs. Managed Enterprise Agent Runtime (ON)",
    },
    "T58": {
        "name": "PromptCanvas #57: 3D Context Compression Funnel",
        "best_for_short": "5-stage token refinement: 1M -> 2k tokens",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Grounded concepts", "Research topics"],
        "when_to_use": "Visualize progressive token refinement across 5 tapering 3D-frustum funnel stages from 1,000,000 raw tokens down to 2,000 precision context tokens.",
        "dynamic": "3 glowing signal packets stream down the 5-stage 3D frustum funnel while side conduits link stage architectures to discard gates.",
        "lineage": "PromptCanvas Blueprint #57 (Funnel Pipeline Chart) • BigQuery Vector Search & Cross-Encoder Re-Ranking",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "RAG & Retrieval Systems Engineers",
        "best_for": "5-stage 3D-frustum tapering vector funnel showing progressive token refinement from 1M raw tokens to 2k precision context",
        "inspired_by": "PromptCanvas Blueprint #57 • Google Cloud BigQuery Vector Search + pgvector",
        "accent": BLUE,
        "hot_topic": "Progressive Context Compression Funnel: 1,000,000 -> 2,000 High-Signal Tokens",
    },
    "T59": {
        "name": "PromptCanvas #58: 6-Gate Deployment Checklist",
        "best_for_short": "6-step autonomous agent prod checklist (ON)",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Proof of concept"],
        "when_to_use": "Present a 6-row numbered production deployment checklist with status badges, monospace config specs, and double green ON toggle switches.",
        "dynamic": "Vertical deployment spine feeds 6 numbered checklist rows, each equipped with verified config boxes and dual ON switches.",
        "lineage": "PromptCanvas Blueprint #58 (Process Checklist Infographic) • Google Cloud GKE gVisor & AlloyDB",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "SRE, DevSecOps & Platform Engineers",
        "best_for": "6-step numbered production deployment checklist with status badges, monospace config specs, and double ON toggle switches",
        "inspired_by": "PromptCanvas Blueprint #58 • Google Cloud GKE gVisor + AlloyDB + OpenHands",
        "accent": GREEN,
        "hot_topic": "6-Step Autonomous Agent Production Deployment Checklist",
    },
    "T60": {
        "name": "PromptCanvas #59: Q1-Q4 Quarterly Roadmap Tracks",
        "best_for_short": "Phased Q1-Q4 enterprise agent rollout plan",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Professional knowledge sharing", "Roadmap"],
        "when_to_use": "Lay out a 4-quarter enterprise rollout roadmap (Q1 Discovery -> Q2 Sandbox -> Q3 State -> Q4 Fleet) with 8 numbered milestones and ACTIVE toggles.",
        "dynamic": "Horizontal flow conduits advance across Q1-Q4 chevron headers and milestone deliverables 01-08.",
        "lineage": "PromptCanvas Blueprint #59 (Timeline & Roadmap Infographic) • Enterprise Agentic AI Rollout Plan",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Engineering Directors & AI Program Leads",
        "best_for": "4 horizontal quarterly roadmap tracks (Q1-Q4) with chevron headers, ACTIVE switches, and 8 numbered milestone deliverables",
        "inspired_by": "PromptCanvas Blueprint #59 • Google Cloud Vertex AI + OpenHands",
        "accent": BLUE,
        "hot_topic": "Phased Q1-Q4 Enterprise Agentic AI Architecture Roadmap",
    },
    "T61": {
        "name": "PromptCanvas #60: 4-Plane Runtime Topology",
        "best_for_short": "Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Grounded concepts"],
        "when_to_use": "Show the 4-node enterprise runtime topology separating reasoning (Vertex AI), orchestration (Cloud Run), sandbox (GKE gVisor), and state (AlloyDB).",
        "dynamic": "Bidirectional gRPC, MCP, CodeAct, and vector state packets flow between Load Balancing ingress and the 4 runtime planes.",
        "lineage": "PromptCanvas Blueprint #60 (Architecture & Topology Infographic) • Google Cloud Agent Reference Topology",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Cloud & Distributed Systems Architects",
        "best_for": "4-node interconnected runtime topology linking Cloud Load Balancing, Vertex Reasoning Engine, Cloud Run, GKE gVisor, and AlloyDB",
        "inspired_by": "PromptCanvas Blueprint #60 • Google Cloud Vertex AI + Cloud Run + pgvector",
        "accent": TEAL,
        "hot_topic": "Enterprise Agent Runtime Topology: Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
    },
    "T62": {
        "name": "PromptCanvas #61: Multi-Agent Supervisor Tree",
        "best_for_short": "Supervisor (01) -> Workers (02a-c) -> Data (03)",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Grounded concepts", "Working solution"],
        "when_to_use": "Illustrate a 3-tier hierarchical delegation tree from Supervisor Agent (01) to 3 Specialized Worker Agents (02a/02b/02c) to Shared Resources (03).",
        "dynamic": "A2A task packets fan out from the Supervisor to SQL, Research, and Code workers and down into BigQuery, Vector Search, and gVisor.",
        "lineage": "PromptCanvas Blueprint #61 (Hierarchical Tree Infographic) • Google ADK & LangGraph Supervisor Pattern",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Multi-Agent Systems Builders",
        "best_for": "3-tier delegation tree from Supervisor Agent (01) to Specialized Worker Agents (02a/02b/02c) to Unified Resource Layer (03)",
        "inspired_by": "PromptCanvas Blueprint #61 • Google Cloud ADK + LangGraph Supervisor",
        "accent": PURPLE,
        "hot_topic": "3-Tier Multi-Agent Supervisor Delegation Tree & Shared Resource Plane",
    },
    "T63": {
        "name": "PromptCanvas #62: 2x2 Impact vs. Complexity Matrix",
        "best_for_short": "20 use cases across Quick Wins, Bets & Traps",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Professional knowledge sharing", "Easy to understand"],
        "when_to_use": "Prioritize 20 concrete agent use cases across a 2x2 matrix of Business Impact vs. Technical Complexity (Quick Wins, Strategic Bets, Low Priority, Traps).",
        "dynamic": "4 color-coded quadrants with 20 numbered use-case cards, ROI metrics, and recommended Google Cloud + OSS stacks.",
        "lineage": "PromptCanvas Blueprint #62 (2x2 Quadrant Matrix Infographic) • AI Portfolio Prioritization",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Product Executives & Principal Architects",
        "best_for": "4-quadrant executive prioritization matrix mapping 20 concrete agent use-cases across Quick Wins, Strategic Bets, Low Priority, and Traps",
        "inspired_by": "PromptCanvas Blueprint #62 • Google Cloud Vertex AI + OpenHands",
        "accent": GREEN,
        "hot_topic": "Agentic AI Portfolio 2x2 Matrix: Quick Wins vs. Strategic Bets vs. Traps",
    },
    "T64": {
        "name": "PromptCanvas #63: Conditional Decision Tree",
        "best_for_short": "3-stage YES/NO branching & self-correction",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Educational"],
        "when_to_use": "Map deterministic YES/NO branching logic across Stage 01 Ingest, Stage 02 Tool & RBAC Check, and Stage 03 Sandboxed Execution & Self-Correction.",
        "dynamic": "Packets traverse 4 decision diamonds with YES/NO branches and an animated self-correction retry loop in Stage 03.",
        "lineage": "PromptCanvas Blueprint #63 (Decision Tree Flowchart) • Deterministic Agent Routing & Self-Correction",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Backend & Agent Workflow Engineers",
        "best_for": "3-stage conditional decision tree across Ingest, Tool/RBAC Check, and Sandboxed Execution with YES/NO diamonds and retry loops",
        "inspired_by": "PromptCanvas Blueprint #63 • Google Cloud ADK + Temporal / LangGraph",
        "accent": BLUE,
        "hot_topic": "Deterministic Agent Decision Tree: Intent Gate -> RBAC Check -> Sandbox Loop",
    },
    "T65": {
        "name": "PromptCanvas #64: 5x4 Feature Evaluation Matrix",
        "best_for_short": "Score 4 agent stacks across 5 prod criteria",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Evaluation results", "Grounded concepts"],
        "when_to_use": "Evaluate 4 agent architectures (Google ADK + Vertex, LangGraph + Postgres, OpenHands + Docker, Raw API) across 5 weighted production criteria.",
        "dynamic": "5x4 matrix of NATIVE / CONFIG / MANUAL capability badges plus animated overall architectural fit score bars (4.9/5 to 1.8/5).",
        "lineage": "PromptCanvas Blueprint #64 (Feature Matrix Grid) • Google ADK vs. LangGraph vs. OpenHands vs. Raw API",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Staff Engineers & Platform Evaluators",
        "best_for": "5x4 multi-criteria evaluation matrix scoring 4 agent stacks across persistence, isolation, HITL, memory, and scale",
        "inspired_by": "PromptCanvas Blueprint #64 • Google Cloud ADK + LangGraph + OpenHands",
        "accent": NAVY,
        "hot_topic": "5x4 Agent Stack Evaluation Matrix: Persistence, Isolation, HITL, Memory & Scale",
    },
    "T66": {
        "name": "PromptCanvas #65: 4-Tier Capability Pyramid",
        "best_for_short": "Raw Inference → Tools → Multi-Agent → Apex",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Educational", "Grounded concepts"],
        "when_to_use": "Show the 4-tier evolution of AI systems from Base Foundation Model (01) to Tool Calling (02) to Multi-Agent (03) to Autonomous Self-Healing Apex (04).",
        "dynamic": "Upward evolution spine climbs the 4-tier 3D trapezoid pyramid while side conduits link tier definitions to Google Cloud + OSS capabilities.",
        "lineage": "PromptCanvas Blueprint #65 (Capability Pyramid Infographic) • Google Cloud Agent Evolution Tiers",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Engineering Leaders & Enablement Architects",
        "best_for": "4-tier ascending capability pyramid from Base Foundation Model (01) to Tool Calling (02) to Multi-Agent (03) to Autonomous Apex (04)",
        "inspired_by": "PromptCanvas Blueprint #65 • Google Cloud Vertex AI + MCP + OpenHands",
        "accent": GREEN,
        "hot_topic": "The 4-Tier Agent Capability Pyramid: Raw Inference → Tools → Multi-Agent → Autonomous",
    },
    "T67": {
        "name": "PromptCanvas #66: Self-Healing Torus Loop",
        "best_for_short": "4-stage circular autonomous repair cycle",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Proof of concept"],
        "when_to_use": "Visualize the circular 4-stage autonomous agent loop (01 Generate → 02 Sandbox Test → 03 Eval Gate → 04 Self-Healing Retry or PASS Deploy).",
        "dynamic": "Packets orbit the 4-quadrant central torus ring, branching on FAIL to the RETRY ACTIVE feedback path or on PASS to DEPLOY ON.",
        "lineage": "PromptCanvas Blueprint #66 (Loop & Cycle Infographic) • Autonomous Self-Healing Evaluation Cycle",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina)",
        "audience": "Autonomous Coding & Verification Engineers",
        "best_for": "Circular 4-quadrant torus loop connecting Model Generation, Sandboxed Test, Evaluation Gate (PASS/FAIL), and Self-Healing Retry",
        "inspired_by": "PromptCanvas Blueprint #66 • Google Cloud Vertex AI + OpenHands",
        "accent": BLUE,
        "hot_topic": "Autonomous Self-Healing Agent Loop: Generate → Sandbox Test → Gate → Repair",
    },
    "T79": {
        "name": "PromptCanvas #52: 4-Tier Spine Archetype (24 Variants)",
        "best_for_short": "4-Tier Spine: Context/Problem → Mechanism → Gate Loop → Scoreboard",
        "content_types": ["PromptCanvas Infographic", "Best Tier", "Working solution", "Grounded concepts"],
        "when_to_use": "Canonical 4-tier vertical spine (1020×1040) contrasting naive patterns against deterministic gates, check-fix-recheck loops, and 4×4 scoreboards — exemplified by Constrained Decoding (T79) plus 23 topic posts (T01, T53, T68–T78, T80–T89).",
        "dynamic": "Packets flow down the 4-tier spine with inked-pixel-centered arrow labels (≤ 0.5px x-height offset) and 842px full-width RULE bars.",
        "lineage": "PromptCanvas Blueprint #52 / Open Knowledge 4-Tier Spine Archetype • Google Cloud Vertex AI + vLLM Outlines",
        "category": "PromptCanvas Infographic",
        "quality_tier": "Best",
        "rendering_tech": "Canonical Draw.io mxGraph + viewer-static.min.js (@2x Retina 2040x2080)",
        "audience": "Principal AI Systems Architects & Researchers",
        "best_for": "4-tier vertical engineering spine with inked-pixel-centered connectors, check-fix-recheck loop, and 4-column production matrix",
        "inspired_by": "PromptCanvas #52 Spine Archetype • Google Cloud Vertex AI Controlled Generation + vLLM Outlines + OpenHands",
        "accent": BLUE,
        "hot_topic": "Prompt-Based JSON vs. Constrained Decoding: Why 99/100 Valid Replies Still Break Pipelines",
    },
}

# 23 Topic Posts preserved on disk (Law 18) and nested under T79.topic_posts so gallery_manifest.json exposes 116 unique visual templates
TOPIC_POSTS_T79: List[Dict[str, str]] = [
    {"id": "T01", "name": "3-Breaker Loop Guard Spine (Agent Stuck Loops)"},
    {"id": "T53", "name": "Anatomy of a Production Coding Agent: Context + Harness + Loop + Graph"},
    {"id": "T68", "name": "Open Knowledge Format Architecture: Formats + Schema + Validation + Graph"},
    {"id": "T69", "name": "Harness² Recursive Agent Harnessing Spine (+22pp NoveltyBench)"},
    {"id": "T70", "name": "5 Open-Source Agent Repos Stack Spine (gstack + Paperclip + rowboat)"},
    {"id": "T71", "name": "3-Track Data Modeling & Medallion Map Spine"},
    {"id": "T72", "name": "TokenEconomizer Black-Box Cost Controller Spine (-30.9% SWE-Bench)"},
    {"id": "T73", "name": "11-Zone Production Agentic AI Reference Spine"},
    {"id": "T74", "name": "6-Vendor AI Agent Sandbox Isolation Spine (gVisor / microVM)"},
    {"id": "T75", "name": "Anatomy of an AI Agent: 5 Building Blocks Spine"},
    {"id": "T76", "name": "12 Google Cloud Concepts for AI Engineers Spine"},
    {"id": "T77", "name": "2026 Pharma R&D & Life Sciences Bio-AI Spine"},
    {"id": "T78", "name": "Ultimate 6-Stage Agentic Coding Workflow Spine"},
    {"id": "T80", "name": "9 Typed Micro-Decisions in the Agent Loop Spine"},
    {"id": "T81", "name": "8-Phase Harness Engineering Curriculum Spine"},
    {"id": "T82", "name": "Agent Code Review Replay-Set & Missed-Defects Spine"},
    {"id": "T83", "name": "Multi-Trial Agent Evals & pass^k Reliability Spine"},
    {"id": "T84", "name": "Inference Engineering Roofline & SLO Goodput Spine"},
    {"id": "T85", "name": "Zero-Bloat MCP Gateway & OAuth 2.1 OBO Spine (MINT-01)"},
    {"id": "T86", "name": "Durable Saga Checkpointing & Idempotent Compensation Spine (MINT-04)"},
    {"id": "T87", "name": "Indirect Prompt Injection & Lethal Trifecta Armor Spine (MINT-06)"},
    {"id": "T88", "name": "Agentic Hybrid GraphRAG & Query-Plan Verifier Spine (MINT-09)"},
    {"id": "T89", "name": "Sub-300ms Multimodal Voice & Barge-In State Machine Spine (MINT-11)"},
]


def _load_session_meta() -> Dict[str, Dict[str, Any]]:
    if not _SESSION_META_PATH.exists():
        return {}
    raw = json.loads(_SESSION_META_PATH.read_text(encoding="utf-8"))
    ordered_keys = sorted(raw.keys(), key=lambda k: int(k[1:]))
    return {k: raw[k] for k in ordered_keys}


def _build_template_meta() -> Dict[str, Dict[str, Any]]:
    meta: Dict[str, Dict[str, Any]] = {}
    for tid in sorted(PROMPTCANVAS_BEST_META.keys(), key=lambda k: int(k[1:])):
        entry = dict(PROMPTCANVAS_BEST_META[tid])
        if tid == "T79":
            entry["topic_posts"] = list(TOPIC_POSTS_T79)
        meta[tid] = entry
    meta.update(_load_session_meta())
    return meta


TEMPLATE_META: Dict[str, Dict[str, Any]] = _build_template_meta()
TOPIC_POST_IDS = {tp["id"] for tp in TOPIC_POSTS_T79}


def _load_canonical_asset(tid: str) -> Tuple[int, int, str, str]:
    """Fail-closed canonical Draw.io-rendered PNG loader with st_mtime_ns cache invalidation (Rule 57B)."""
    png_path = _CANONICAL_REF_DIR / f"canonical_{tid}.png"
    dims_path = _CANONICAL_REF_DIR / "canonical_dimensions.json"
    if not png_path.exists():
        raise FileNotFoundError(
            f"[Rule 57B Violation] Missing canonical asset {png_path}. "
            "All templates must render from verified Draw.io @2x Retina assets."
        )
    mtime_ns = png_path.stat().st_mtime_ns
    cached = _B64_CACHE.get(tid)
    if cached is not None and cached[0] == mtime_ns:
        return cached[1], cached[2], cached[3], cached[4]
    cw, ch, bg = (920, 1150, "#FAF8F2") if int(tid[1:]) >= 90 else (1020, 1040, "#F8FAFC")
    if dims_path.exists():
        try:
            dims = json.loads(dims_path.read_text(encoding="utf-8")).get(tid, {})
            cw = int(dims.get("width", cw))
            ch = int(dims.get("height", ch))
            bg = str(dims.get("background", bg)).upper()
        except Exception:
            pass
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    _B64_CACHE[tid] = (mtime_ns, cw, ch, bg, b64)
    return cw, ch, bg, b64


def render_template(tid: str, spec: Optional[Dict[str, Any]] = None, phase: Optional[float] = None) -> str:
    """Render any certified gallery template (`116`) or preserved `T79` topic post (`22`) into a Zero-Origin W3C SVG."""
    if tid not in TEMPLATE_META and tid not in TOPIC_POST_IDS:
        raise KeyError(f"Unknown or purged template ID: {tid}")
    s = spec or {}
    meta = TEMPLATE_META.get(tid) or {
        "accent": BLUE,
        "lineage": f"PromptCanvas 4-Tier Spine Topic Variant ({tid})",
        "inspired_by": f"PromptCanvas 4-Tier Spine ({tid}) • Google Cloud Vertex AI + OpenHands + LangGraph",
    }
    cw, ch, bg, b64 = _load_canonical_asset(tid)
    accent = meta.get("accent", BLUE)
    lineage = str(s.get("lineage") or meta.get("lineage") or "Canonical Draw.io Blueprint").replace(" GCP ", " Google Cloud ")
    source_note = str(s.get("source") or meta.get("inspired_by") or "Google Cloud Vertex AI + OpenHands").replace(" GCP ", " Google Cloud ")
    if not any(m in source_note for m in ("LangGraph", "OpenHands", "vLLM", "PostgreSQL", "OpenTelemetry", "Llama Guard", "Temporal", "Promptfoo", "MCP", "Knative", "pgvector", "Redis", "Qdrant", "LiteLLM")):
        source_note = f"{source_note} • OpenHands + LangGraph + pgvector"
    if not any(m in source_note for m in ("Google", "Vertex", "Gemini", "Firestore", "Cloud Run", "ADK", "Model Armor", "BigQuery", "AlloyDB", "Cloud Trace")):
        source_note = f"{source_note} • Google Cloud Vertex AI"

    conduit = _flow(
        [(20.0, 2.0), (float(cw - 20), 2.0)],
        accent,
        phase=phase,
        dur=2.4,
        width=2.6,
        head=True,
        packets=3,
        dash="8 5",
        track=True,
    )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="{cw}" height="{ch}">',
        f"<title>{_esc(f'{tid} • NITIN AGGARWAL • NOVEMBER 2026 • FORMAT LINEAGE: {lineage} • Proprietary + Confidential')}</title>",
        f"<desc>{_esc(f'Author: Nitin Aggarwal • November 2026 • {source_note}')}</desc>",
        "<defs>",
        '<linearGradient id="glassCardGrad" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.98"/>'
        '<stop offset="100%" stop-color="#F8FAFC" stop-opacity="0.94"/>'
        "</linearGradient>",
        '<linearGradient id="glassSheen" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.72"/>'
        '<stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0"/>'
        "</linearGradient>",
        '<pattern id="archGrid" width="24" height="24" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="1" fill="#94A3B8" fill-opacity="0.18"/>'
        "</pattern>",
        f"<style>{CSS}</style>",
        "</defs>",
        f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="{bg if bg.startswith("#") and len(bg) == 7 else "#F8FAFC"}"/>',
        f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="#F8FAFC" fill-opacity="0.01"/>',
        f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="url(#archGrid)"/>',
        f'<image x="0" y="0" width="{cw}" height="{ch}" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{b64}"/>',
        conduit,
        "</svg>",
    ]
    return flatten_svg_zero_origin("\n".join(parts))


def render_template_gif(
    tid: str,
    gif_path: Path,
    png_path: Optional[Path] = None,
    frames: int = 6,
    spec: Optional[Dict[str, Any]] = None,
) -> bool:
    """Compile a looping Animated GIF from canonical 2x Retina PNG + animated phase packets via FFmpeg/Chrome."""
    ffmpeg = resolve_ffmpeg_bin()
    chrome = resolve_chrome_bin()
    src_png = _CANONICAL_REF_DIR / f"canonical_{tid}.png"
    if png_path is not None and src_png.exists():
        png_path.parent.mkdir(parents=True, exist_ok=True)
        png_path.write_bytes(src_png.read_bytes())
    if ffmpeg is None:
        return False
    gif_path.parent.mkdir(parents=True, exist_ok=True)

    # Fast, crisp native FFmpeg pulse-conduit GIF directly from the canonical @2x PNG when available
    if src_png.exists() and frames <= 6:
        subprocess.run(
            [
                str(ffmpeg),
                "-y",
                "-loop",
                "1",
                "-t",
                "1.5",
                "-i",
                str(src_png),
                "-vf",
                "fps=4,scale=920:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
                "-loop",
                "0",
                str(gif_path),
            ],
            check=False,
            capture_output=True,
        )
        if gif_path.exists() and gif_path.stat().st_size > 1024:
            return True

    if chrome is None:
        return False
    with tempfile.TemporaryDirectory(prefix=f"tpl_{tid}_") as tmp:
        tmp_path = Path(tmp)
        for i in range(frames):
            phase = i / float(frames)
            frame_svg = tmp_path / f"frame_{i:02d}.svg"
            frame_png = tmp_path / f"frame_{i:02d}.png"
            svg_text = render_template(tid, spec, phase)
            frame_svg.write_text(svg_text, encoding="utf-8")
            mw = re.search(r'<svg[^>]*\bwidth="(\d+)"', svg_text)
            mh = re.search(r'<svg[^>]*\bheight="(\d+)"', svg_text)
            win_w = int(mw.group(1)) if mw else 920
            win_h = int(mh.group(1)) if mh else 1150
            subprocess.run(
                [
                    str(chrome),
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    f"--window-size={win_w},{win_h}",
                    f"--screenshot={frame_png}",
                    f"file://{frame_svg}",
                ],
                check=False,
                capture_output=True,
            )
        subprocess.run(
            [
                str(ffmpeg),
                "-y",
                "-framerate",
                "4",
                "-i",
                str(tmp_path / "frame_%02d.png"),
                "-vf",
                "split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
                "-loop",
                "0",
                str(gif_path),
            ],
            check=False,
            capture_output=True,
        )
    return gif_path.exists()


def list_templates() -> List[Dict[str, Any]]:
    """Return the ordered list of 116 Certified Unique Visual Templates (`72 Best` + `44 High`)."""
    return [{"id": tid, **meta} for tid, meta in TEMPLATE_META.items()]


def get_gallery_summary() -> Dict[str, Any]:
    """Return tier breakdown and catalog statistics for Studio UI and tests."""
    items = list_templates()
    best_count = sum(1 for t in items if t.get("quality_tier") == "Best")
    high_count = sum(1 for t in items if t.get("quality_tier") == "High")
    return {
        "template_count": len(items),
        "best_count": best_count,
        "high_count": high_count,
        "medium_low_worst_count": len(items) - best_count - high_count,
        "t79_topic_posts_count": len(TOPIC_POSTS_T79),
    }
