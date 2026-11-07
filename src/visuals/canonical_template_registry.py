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
    AMBER,
    BLUE,
    CSS,
    GREEN,
    NAVY,
    PURPLE,
    RED,
    SKY,
    TEAL,
    _esc,
    _flow,
    _pat,
    _t,
    audit_zero_origin_svg,
    flatten_svg_zero_origin,
    resolve_chrome_bin,
    resolve_ffmpeg_bin,
)

Point = Tuple[float, float]

_WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_CANONICAL_REF_DIR = _WORKSPACE_ROOT / "assets" / "canonical-ref"
_TEMPLATE_GALLERY_DIR = _WORKSPACE_ROOT / "assets" / "template-gallery"
_SESSION_META_PATH = _WORKSPACE_ROOT / "data" / "session_templates_metadata.json"
_B64_CACHE: Dict[str, Tuple[int, int, int, str, str]] = {}
_DRAWIO_TOPOLOGY_CACHE: Dict[str, Dict[str, Any]] = {}


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


def _parse_svg_path_points(d_str: str) -> List[Point]:
    """Convert an SVG path d attribute (M/L/H/V/Q/C) into polyline coordinates."""
    tokens = re.findall(r"[MLHVQCZmlhvqcz]|[-+]?(?:\d+\.?\d*|\.\d+)", d_str or "")
    pts: List[Point] = []
    cx, cy = 0.0, 0.0
    cmd = ""
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if re.match(r"^[A-Za-z]$", tok):
            cmd = tok
            i += 1
            if cmd in ("Z", "z"):
                if pts:
                    pts.append(pts[0])
            continue
        try:
            if cmd in ("M", "L"):
                cx, cy = float(tokens[i]), float(tokens[i + 1])
                pts.append((cx, cy))
                i += 2
            elif cmd in ("m", "l"):
                cx += float(tokens[i])
                cy += float(tokens[i + 1])
                pts.append((cx, cy))
                i += 2
            elif cmd == "H":
                cx = float(tokens[i])
                pts.append((cx, cy))
                i += 1
            elif cmd == "h":
                cx += float(tokens[i])
                pts.append((cx, cy))
                i += 1
            elif cmd == "V":
                cy = float(tokens[i])
                pts.append((cx, cy))
                i += 1
            elif cmd == "v":
                cy += float(tokens[i])
                pts.append((cx, cy))
                i += 1
            elif cmd == "Q":
                qx, qy = float(tokens[i]), float(tokens[i + 1])
                ex, ey = float(tokens[i + 2]), float(tokens[i + 3])
                mx = 0.25 * cx + 0.5 * qx + 0.25 * ex
                my = 0.25 * cy + 0.5 * qy + 0.25 * ey
                pts.append((mx, my))
                cx, cy = ex, ey
                pts.append((cx, cy))
                i += 4
            elif cmd == "C":
                c1x, c1y = float(tokens[i]), float(tokens[i + 1])
                c2x, c2y = float(tokens[i + 2]), float(tokens[i + 3])
                ex, ey = float(tokens[i + 4]), float(tokens[i + 5])
                mx = 0.125 * cx + 0.375 * c1x + 0.375 * c2x + 0.125 * ex
                my = 0.125 * cy + 0.375 * c1y + 0.375 * c2y + 0.125 * ey
                pts.append((mx, my))
                cx, cy = ex, ey
                pts.append((cx, cy))
                i += 6
            else:
                i += 1
        except (ValueError, IndexError):
            break
    dedup: List[Point] = []
    for p in pts:
        if not dedup or abs(p[0] - dedup[-1][0]) > 1.5 or abs(p[1] - dedup[-1][1]) > 1.5:
            dedup.append(p)
    return dedup


def _extract_drawio_topology(tid: str, cw: int, ch: int) -> Dict[str, Any]:
    """Extract internal connector lines, paths, stage rects, circles, and mxGraph edges from {tid}.drawio."""
    cached = _DRAWIO_TOPOLOGY_CACHE.get(tid)
    if cached is not None:
        return cached

    import xml.etree.ElementTree as ET

    drawio_path = _TEMPLATE_GALLERY_DIR / f"{tid}.drawio"
    if not drawio_path.exists() and tid.startswith("T79_"):
        drawio_path = _TEMPLATE_GALLERY_DIR / "T79.drawio"

    mx_verts: Dict[str, Tuple[float, float, float, float, str]] = {}
    mx_edges: List[Tuple[str, str, str]] = []
    bg_lines: List[List[Point]] = []
    bg_paths: List[List[Point]] = []
    bg_circles: List[Tuple[float, float, float]] = []
    bg_rects: List[Tuple[float, float, float, float]] = []

    if drawio_path.exists():
        try:
            root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
            bg_svg = ""
            for c in root.findall(".//mxCell"):
                cid = c.attrib.get("id", "")
                val = c.attrib.get("value", "")
                if "<svg" in val and cid.startswith(("bg", "poster_bg")):
                    bg_svg = val
                elif c.attrib.get("edge") == "1":
                    src = c.attrib.get("source", "")
                    tgt = c.attrib.get("target", "")
                    if src and tgt:
                        mx_edges.append((cid, src, tgt))
                elif c.attrib.get("vertex") == "1":
                    g = c.find("mxGeometry")
                    if g is not None and g.attrib.get("x") is not None and g.attrib.get("y") is not None:
                        vx = float(g.attrib.get("x", 0.0))
                        vy = float(g.attrib.get("y", 0.0))
                        vw = float(g.attrib.get("width", 0.0))
                        vh = float(g.attrib.get("height", 0.0))
                        clean_txt = re.sub(r"<[^>]+>", " ", val).strip()
                        clean_txt = re.sub(r"\s+", " ", clean_txt)
                        mx_verts[cid] = (vx, vy, vw, vh, clean_txt)

            # GraphViewer (border: 0) translates graphs without a (0,0) backdrop by (-min_vx, -min_vy)
            if mx_verts:
                min_vx = min(v[0] for v in mx_verts.values())
                min_vy = min(v[1] for v in mx_verts.values())
                if min_vx > 2.0 or min_vy > 2.0:
                    mx_verts = {
                        k: (vx - min_vx, vy - min_vy, vw, vh, txt)
                        for k, (vx, vy, vw, vh, txt) in mx_verts.items()
                    }

            if bg_svg:
                body = re.sub(r"<defs>.*?</defs>", "", bg_svg, flags=re.DOTALL)
                body = re.sub(
                    r'<g transform="translate\(\s*(?:30|644|696|788)\s*,\s*(?:18|22)\s*\)"[^>]*>.*?</g>',
                    "",
                    body,
                    flags=re.DOTALL,
                )
                for m in re.finditer(r"<(line|path|circle|rect)\b([^>]*)/?>", body):
                    tag = m.group(1)
                    attrs = dict(re.findall(r'([a-zA-Z0-9_:-]+)="([^"]*)"', m.group(2)))
                    if tag == "line":
                        try:
                            x1, y1 = float(attrs["x1"]), float(attrs["y1"])
                            x2, y2 = float(attrs["x2"]), float(attrs["y2"])
                            seg_len = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                            if 125.0 <= min(y1, y2) and max(y1, y2) <= ch - 55.0 and 14.0 <= seg_len <= 820.0:
                                bg_lines.append([(x1, y1), (x2, y2)])
                        except (KeyError, ValueError):
                            pass
                    elif tag == "path":
                        pts = _parse_svg_path_points(attrs.get("d", ""))
                        if len(pts) >= 2:
                            xs = [p[0] for p in pts]
                            ys = [p[1] for p in pts]
                            bw, bh = max(xs) - min(xs), max(ys) - min(ys)
                            if (
                                min(ys) >= 135.0
                                and max(ys) <= ch - 55.0
                                and (bw >= 22.0 or bh >= 22.0)
                                and bw <= cw - 90.0
                            ):
                                bg_paths.append(pts[:8])
                    elif tag == "circle":
                        try:
                            cx, cy, r = float(attrs["cx"]), float(attrs["cy"]), float(attrs["r"])
                            if 16.0 <= r <= 185.0 and 175.0 <= cy <= ch - 75.0:
                                bg_circles.append((cx, cy, r))
                        except (KeyError, ValueError):
                            pass
                    elif tag == "rect":
                        try:
                            rx, ry = float(attrs["x"]), float(attrs["y"])
                            rw, rh = float(attrs["width"]), float(attrs["height"])
                            if 180.0 <= ry <= ch - 85.0 and 44.0 <= rw <= cw - 85.0 and 18.0 <= rh <= 420.0:
                                bg_rects.append((rx, ry, rw, rh))
                        except (KeyError, ValueError):
                            pass
        except Exception:
            pass

    topo = {
        "mx_verts": mx_verts,
        "mx_edges": mx_edges,
        "bg_lines": bg_lines,
        "bg_paths": bg_paths,
        "bg_circles": bg_circles,
        "bg_rects": bg_rects,
    }
    _DRAWIO_TOPOLOGY_CACHE[tid] = topo
    return topo


def _edge_port_points(
    sbox: Tuple[float, float, float, float],
    tbox: Tuple[float, float, float, float],
) -> List[Point]:
    """Compute clean port-to-port polyline between two vertex bounding boxes."""
    sx, sy, sw, sh = sbox
    tx, ty, tw, th = tbox
    scx, scy = sx + sw / 2.0, sy + sh / 2.0
    tcx, tcy = tx + tw / 2.0, ty + th / 2.0

    # Horizontal right-to-left or left-to-right when vertically overlapping
    if abs(scy - tcy) <= max(sh, th) * 0.85:
        if sx + sw <= tx + 6.0:
            y_mid = (scy + tcy) / 2.0
            return [(sx + sw, y_mid), (tx, y_mid)]
        if tx + tw <= sx + 6.0:
            y_mid = (scy + tcy) / 2.0
            return [(sx, y_mid), (tx + tw, y_mid)]

    # Vertical top-to-bottom or bottom-to-top
    if sy + sh <= ty + 8.0:
        p1 = (scx, sy + sh)
        p2 = (tcx, ty)
        if abs(scx - tcx) <= 18.0:
            return [p1, (scx, ty)]
        ym = (p1[1] + p2[1]) / 2.0
        return [p1, (scx, ym), (tcx, ym), p2]

    if ty + th <= sy + 8.0:
        # Feedback / replan loop going upward (e.g., t3_fix_box -> t3_model_circle)
        return [(sx, scy), (tcx, scy), (tcx, ty + th)]

    return [(scx, scy), (tcx, tcy)]


def _render_spot_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    color: str,
    phase_idx: int,
    phase: Optional[float],
    rx: float = 12.0,
) -> str:
    """Render a 4-phase spotlight frame around a diagram zone or card."""
    cls = f' class="phase-glow-{phase_idx}"' if phase is None else ""
    if phase is not None:
        active = int((phase * 4.0) % 4) + 1 == phase_idx
        op = 0.95 if active else 0.22
        sw = 3.2 if active else 1.4
    else:
        op = 0.88
        sw = 2.8
    return (
        f'<rect x="{x - 3.0:.1f}" y="{y - 3.0:.1f}" width="{w + 6.0:.1f}" height="{h + 6.0:.1f}" rx="{rx:.1f}"'
        f'{cls} fill="none" stroke="{color}" stroke-width="{sw:.1f}" stroke-opacity="{op:.2f}" stroke-dasharray="8 4"/>'
    )


def _render_spot_circle(
    cx: float,
    cy: float,
    r: float,
    color: str,
    phase_idx: int,
    phase: Optional[float],
) -> str:
    """Render a 4-phase spotlight ring around a circular lens or hub."""
    cls = f' class="phase-glow-{phase_idx}"' if phase is None else ""
    if phase is not None:
        active = int((phase * 4.0) % 4) + 1 == phase_idx
        op = 0.95 if active else 0.24
        sw = 3.4 if active else 1.5
    else:
        op = 0.90
        sw = 3.0
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 4.5:.1f}"{cls} fill="none" '
        f'stroke="{color}" stroke-width="{sw:.1f}" stroke-opacity="{op:.2f}" stroke-dasharray="9 5"/>'
    )


def _render_master_packet(pts: Sequence[Point], color: str, phase: Optional[float], dur: float = 4.8) -> str:
    """Render a high-visibility multi-ring master signal packet traversing the entire end-to-end architecture path."""
    clean: List[Point] = []
    for p in pts:
        pt = (float(p[0]), float(p[1]))
        if not clean or abs(pt[0] - clean[-1][0]) > 1.5 or abs(pt[1] - clean[-1][1]) > 1.5:
            clean.append(pt)
    if len(clean) < 2:
        return ""
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in clean)
    if phase is None:
        return (
            f"<g>"
            f'<circle r="11.0" fill="{color}" fill-opacity="0.18"/>'
            f'<circle r="7.2" fill="{color}" fill-opacity="0.34"/>'
            f'<circle r="4.8" fill="#FFFFFF" stroke="{color}" stroke-width="2.4"/>'
            f'<circle r="2.2" fill="{color}"/>'
            f'<animateMotion dur="{dur:.2f}s" begin="0s" repeatCount="indefinite" path="{d}"/>'
            f"</g>"
        )
    px, py = _pat(clean, phase % 1.0)
    return (
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="11.0" fill="{color}" fill-opacity="0.18"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7.2" fill="{color}" fill-opacity="0.34"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.8" fill="#FFFFFF" stroke="{color}" stroke-width="2.4"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.2" fill="{color}"/>'
    )


def _render_phase_telemetry_strip(
    cw: int,
    strip_y: float,
    labels: Sequence[str],
    colors: Sequence[str],
    phase: Optional[float],
) -> str:
    """Render a 4-phase synchronized WHEN · WHERE · WHY telemetry strip with zero text bbox overlaps."""
    margin_x = 24.0
    gap = 8.0
    avail_w = float(cw) - 2.0 * margin_x - 3.0 * gap
    pill_w = avail_w / 4.0
    pill_h = 20.0
    out: List[str] = []
    centers: List[Point] = []
    font_sz = 7.9 if cw < 860 else 8.3
    max_chars = max(24, int(pill_w / 4.2))

    for idx in range(4):
        px = margin_x + idx * (pill_w + gap)
        col = colors[idx % len(colors)]
        raw_lbl = str(labels[idx] if idx < len(labels) else f"Phase 0{idx + 1}").replace(" GCP ", " Google Cloud ")
        if len(raw_lbl) > max_chars:
            raw_lbl = raw_lbl[:max_chars].rstrip()
        cls = f' class="phase-pill-{idx + 1}"' if phase is None else ""
        if phase is not None:
            active = int((phase * 4.0) % 4) == idx
            op = "1.0" if active else "0.55"
            sw = "2.2" if active else "1.2"
        else:
            op = "0.96"
            sw = "1.6"
        out.append(
            f'<g{cls} opacity="{op}">'
            f'<rect x="{px:.1f}" y="{strip_y:.1f}" width="{pill_w:.1f}" height="{pill_h:.1f}" rx="10.0" '
            f'fill="#FFFFFF" fill-opacity="0.96" stroke="{col}" stroke-width="{sw}"/>'
            f'{_t(px + pill_w / 2.0, strip_y + 13.4, raw_lbl, font_sz, 800, col, "middle")}'
            f"</g>"
        )
        centers.append((px + pill_w / 2.0, strip_y + pill_h / 2.0))

    # Synchronized time-cursor orb gliding across the 4 phase pills
    out.append(
        _flow(
            [(margin_x + 12.0, strip_y - 2.0), (float(cw) - margin_x - 12.0, strip_y - 2.0)],
            colors[0],
            phase=phase,
            dur=4.8,
            width=1.8,
            head=True,
            packets=1,
            dash="6 4",
            track=False,
        )
    )
    return "\n".join(out)


def _build_template_flow_overlay(
    tid: str,
    cw: int,
    ch: int,
    accent: str,
    meta: Dict[str, Any],
    phase: Optional[float] = None,
) -> str:
    """Compile true end-to-end multi-phase signal, bit-stream, and causal spotlight animations for {tid}."""
    out: List[str] = []
    phase_colors = [BLUE, GREEN, AMBER, PURPLE]

    # 1. Bespoke Flagship Exemplar: T160 (C4 Model 3-Lens Telescopic AI Architecture Zoom, 920x1150)
    if tid == "T160":
        # Top Bad-vs-Good comparison transformation bridge
        out.append(
            _flow(
                [(442.0, 272.0), (478.0, 272.0)],
                GREEN,
                phase=phase,
                dur=1.4,
                width=2.6,
                head=True,
                packets=1,
            )
        )
        # 4-Phase Stage Spotlights (Lens 1 C1 -> Lens 2 C2 -> Lens 3 C3 -> LENSES Takeaway)
        out.append(_render_spot_circle(156.0, 446.0, 86.0, BLUE, 1, phase))
        out.append(_render_spot_rect(90.0, 434.0, 132.0, 24.0, BLUE, 1, phase, rx=8.0))
        out.append(_render_spot_circle(438.0, 540.0, 108.0, GREEN, 2, phase))
        out.append(_render_spot_rect(359.0, 506.0, 158.0, 24.0, GREEN, 2, phase, rx=8.0))
        out.append(_render_spot_circle(734.0, 632.0, 122.0, AMBER, 3, phase))
        out.append(_render_spot_rect(642.0, 580.0, 184.0, 66.0, AMBER, 3, phase, rx=10.0))
        out.append(_render_spot_rect(42.0, 788.0, 836.0, 122.0, PURPLE, 4, phase, rx=16.0))

        # Phase 1: C1 System Context Internal Signal Flow (Enterprise User -> AI Support System -> Spanner + Billing)
        out.append(_flow([(156.0, 372.0), (156.0, 392.0)], BLUE, phase=phase, dur=1.2, width=2.4, packets=1))
        out.append(_flow([(156.0, 416.0), (156.0, 434.0)], BLUE, phase=phase, dur=1.1, width=2.8, packets=1))
        out.append(_flow([(156.0, 458.0), (156.0, 476.0)], BLUE, phase=phase, dur=1.1, width=2.8, packets=1))
        out.append(
            _flow(
                [(217.0, 488.0), (232.0, 488.0), (232.0, 446.0), (222.0, 446.0)],
                SKY,
                phase=phase,
                dur=1.5,
                width=2.2,
                packets=1,
            )
        )

        # Optical Zoom Bridge 1 (C1 AI Support System -> C2 Envoy OIDC Gateway)
        out.append(
            _flow(
                [(184.0, 386.0), (426.0, 430.0)],
                BLUE,
                phase=phase,
                label="①→② ZOOM: JWT → OIDC mTLS",
                label_dy=-18.0,
                label_at=0.48,
                dur=1.8,
                width=2.0,
                head=True,
                packets=1,
                dash="7 5",
                track=False,
            )
        )
        out.append(
            _flow(
                [(222.0, 446.0), (294.0, 460.0), (365.0, 474.0)],
                BLUE,
                phase=phase,
                dur=1.4,
                width=3.2,
                head=True,
                packets=2,
            )
        )
        out.append(
            _flow(
                [(156.0, 506.0), (388.0, 634.0)],
                GREEN,
                phase=phase,
                dur=1.8,
                width=2.0,
                head=True,
                packets=1,
                dash="7 5",
                track=False,
            )
        )

        # Phase 2: C2 Container Mesh Flow (Envoy OIDC -> ADK Orchestrator Pod -> IAM STS OBO & FastMCP Svc)
        out.append(_flow([(438.0, 486.0), (438.0, 506.0)], GREEN, phase=phase, dur=1.1, width=2.8, packets=1))
        out.append(_flow([(406.0, 530.0), (388.0, 564.0)], GREEN, phase=phase, dur=1.2, width=2.8, packets=1))
        out.append(_flow([(470.0, 530.0), (488.0, 564.0)], GREEN, phase=phase, dur=1.2, width=2.8, packets=1))
        out.append(
            _flow(
                [(388.0, 588.0), (438.0, 604.0), (488.0, 588.0)],
                TEAL,
                phase=phase,
                dur=1.5,
                width=2.2,
                packets=1,
            )
        )

        # Optical Zoom Bridge 2 (C2 ADK Orchestrator Pod -> C3 4-Hook Harness Pipeline)
        out.append(
            _flow(
                [(488.0, 464.0), (734.0, 512.0)],
                AMBER,
                phase=phase,
                label="②→③ ZOOM: POD → 4 ADK HOOKS",
                label_dy=-18.0,
                label_at=0.45,
                dur=1.8,
                width=2.0,
                head=True,
                packets=1,
                dash="7 5",
                track=False,
            )
        )
        out.append(
            _flow(
                [(517.0, 518.0), (582.0, 534.0), (647.0, 550.0)],
                AMBER,
                phase=phase,
                dur=1.4,
                width=3.2,
                head=True,
                packets=2,
            )
        )
        out.append(
            _flow(
                [(456.0, 628.0), (698.0, 748.0)],
                AMBER,
                phase=phase,
                dur=1.8,
                width=2.0,
                head=True,
                packets=1,
                dash="7 5",
                track=False,
            )
        )

        # Phase 3: C3 In-Process ADK Runner 4-Hook Sequential Bit-Stream Cascade
        out.append(
            _flow(
                [(821.0, 550.0), (842.0, 550.0), (842.0, 592.0), (826.0, 592.0)],
                AMBER,
                phase=phase,
                dur=1.2,
                width=2.5,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(642.0, 592.0), (624.0, 592.0), (624.0, 634.0), (642.0, 634.0)],
                AMBER,
                phase=phase,
                dur=1.2,
                width=2.5,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(826.0, 634.0), (842.0, 634.0), (842.0, 676.0), (820.0, 676.0)],
                AMBER,
                phase=phase,
                dur=1.2,
                width=2.5,
                packets=1,
            )
        )

        # Phase 4: OTel GenAI Span Commit -> L·E·N·S·E·S Takeaway & 3 Executive Outcome Cards
        out.append(
            _flow(
                [(734.0, 688.0), (734.0, 772.0), (540.0, 772.0), (540.0, 788.0)],
                PURPLE,
                phase=phase,
                label="④ OTel SPAN → L·E·N·S·E·S",
                label_dy=-14.0,
                label_at=0.58,
                dur=1.4,
                width=3.0,
                packets=2,
            )
        )
        out.append(
            _flow(
                [(163.0, 910.0), (163.0, 948.0)],
                BLUE,
                phase=phase,
                dur=1.6,
                width=2.2,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(460.0, 910.0), (460.0, 948.0)],
                GREEN,
                phase=phase,
                dur=1.6,
                width=2.2,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(757.0, 910.0), (757.0, 948.0)],
                AMBER,
                phase=phase,
                dur=1.6,
                width=2.2,
                packets=1,
            )
        )

        # Continuous Master End-to-End Telemetry Packet across all 3 Lenses + Takeaway
        out.append(
            _render_master_packet(
                [
                    (156.0, 392.0),
                    (156.0, 446.0),
                    (156.0, 488.0),
                    (156.0, 446.0),
                    (222.0, 446.0),
                    (365.0, 474.0),
                    (438.0, 474.0),
                    (438.0, 518.0),
                    (388.0, 576.0),
                    (488.0, 576.0),
                    (517.0, 518.0),
                    (647.0, 550.0),
                    (734.0, 550.0),
                    (734.0, 592.0),
                    (734.0, 634.0),
                    (734.0, 676.0),
                    (734.0, 788.0),
                    (460.0, 848.0),
                ],
                BLUE,
                phase,
                dur=4.8,
            )
        )

        out.append(
            _render_phase_telemetry_strip(
                cw,
                954.0,
                [
                    "① 0–1.2s · C1 User → AI → Spanner",
                    "② 1.2–2.4s · C2 OIDC → ADK → OBO/MCP",
                    "③ 2.4–3.6s · C3 KV → Breaker → Armor",
                    "④ 3.6–4.8s · OTel Span → L·E·N·S·E·S",
                ],
                phase_colors,
                phase,
            )
        )
        return "\n".join(out)

    # 2. Bespoke Flagship Exemplar: T61 (PromptCanvas #60: 4-Plane Runtime Topology, 765x1024)
    if tid == "T61":
        out.append(_render_spot_rect(180.0, 492.0, 224.0, 160.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(180.0, 240.0, 280.0, 180.0, PURPLE, 2, phase, rx=12.0))
        out.append(_render_spot_rect(492.0, 392.0, 228.0, 204.0, GREEN, 3, phase, rx=12.0))
        out.append(_render_spot_rect(423.0, 638.0, 297.0, 288.0, AMBER, 4, phase, rx=12.0))

        # Phase 1: HTTPS Ingress -> Cloud Load Balancing -> 02 Cloud Run Orchestrator
        out.append(
            _flow(
                [(22.0, 572.0), (92.0, 572.0), (178.0, 572.0)],
                BLUE,
                phase=phase,
                label="① HTTPS → CLB → Cloud Run",
                label_dy=-56.0,
                dur=1.3,
                width=3.0,
                packets=2,
            )
        )
        # Phase 2: 02 Cloud Run <-> 01 Vertex AI Reasoning Engine (Gemini)
        out.append(
            _flow(
                [(291.0, 492.0), (291.0, 422.0)],
                PURPLE,
                phase=phase,
                dur=1.2,
                width=2.8,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(311.0, 422.0), (311.0, 490.0)],
                PURPLE,
                phase=phase,
                dur=1.2,
                width=2.8,
                packets=1,
            )
        )
        # Phase 3: 01 Vertex AI & 02 Cloud Run <-> 04 AlloyDB State & Knowledge (pgvector)
        out.append(
            _flow(
                [(460.0, 324.0), (613.0, 324.0), (613.0, 390.0)],
                GREEN,
                phase=phase,
                label="③ pgvector RAG Grounding",
                label_dy=-16.0,
                dur=1.5,
                width=3.0,
                packets=2,
            )
        )
        out.append(
            _flow(
                [(406.0, 556.0), (490.0, 556.0)],
                TEAL,
                phase=phase,
                dur=1.3,
                width=2.8,
                packets=1,
            )
        )
        out.append(
            _flow(
                [(490.0, 540.0), (406.0, 540.0)],
                TEAL,
                phase=phase,
                dur=1.3,
                width=2.4,
                packets=1,
            )
        )
        # Phase 4: 02 Cloud Run <-> 03 GKE gVisor Sandbox Secure Execution
        out.append(
            _flow(
                [(291.0, 654.0), (291.0, 795.0), (423.0, 795.0)],
                AMBER,
                phase=phase,
                dur=1.5,
                width=3.0,
                packets=2,
            )
        )
        out.append(
            _flow(
                [(423.0, 779.0), (307.0, 779.0), (307.0, 654.0)],
                GREEN,
                phase=phase,
                dur=1.5,
                width=2.8,
                packets=2,
            )
        )

        # Continuous Master End-to-End Signal Packet across all 4 Runtime Planes
        out.append(
            _render_master_packet(
                [
                    (22.0, 572.0),
                    (180.0, 572.0),
                    (291.0, 540.0),
                    (291.0, 340.0),
                    (460.0, 324.0),
                    (613.0, 324.0),
                    (613.0, 490.0),
                    (490.0, 556.0),
                    (291.0, 556.0),
                    (291.0, 795.0),
                    (560.0, 795.0),
                    (423.0, 779.0),
                    (307.0, 779.0),
                    (307.0, 572.0),
                ],
                TEAL,
                phase,
                dur=4.8,
            )
        )
        out.append(
            _render_phase_telemetry_strip(
                cw,
                942.0,
                [
                    "① 0–1.2s · HTTPS → Cloud Run",
                    "② 1.2–2.4s · Vertex AI Plan Loop",
                    "③ 2.4–3.6s · AlloyDB pgvector RAG",
                    "④ 3.6–4.8s · GKE gVisor Sandbox",
                ],
                [BLUE, PURPLE, GREEN, AMBER],
                phase,
            )
        )
        return "\n".join(out)

    # 3. Universal .drawio Topology Compiler for all remaining 137 templates
    topo = _extract_drawio_topology(tid, cw, ch)
    mx_verts = topo["mx_verts"]
    mx_edges = topo["mx_edges"]
    bg_lines = topo["bg_lines"]
    bg_paths = topo["bg_paths"]
    bg_circles = topo["bg_circles"]
    bg_rects = topo["bg_rects"]

    # Case A: 4-Tier Spine & Process Templates with explicit mxGraph edges (T01, T53, T54, T68-T89, T79_P01-P23)
    if mx_edges:
        for idx, card_id in enumerate(("t1_card", "t2_card", "t3_card", "t4_card"), start=1):
            if card_id in mx_verts:
                vx, vy, vw, vh, _ = mx_verts[card_id]
                out.append(
                    _render_spot_rect(
                        vx,
                        vy,
                        vw,
                        vh,
                        [RED, BLUE, AMBER, GREEN][idx - 1],
                        idx,
                        phase,
                        rx=14.0,
                    )
                )
        # Vertical spine progression across 01 -> 02 -> 03 -> 04 badges
        if all(b in mx_verts for b in ("badge_01", "badge_02", "badge_03", "badge_04")):
            spine_pts: List[Point] = []
            for b in ("badge_01", "badge_02", "badge_03", "badge_04"):
                bx, by, bw, bh, _ = mx_verts[b]
                spine_pts.append((bx + bw / 2.0, by + bh / 2.0))
            out.append(
                _flow(
                    spine_pts,
                    BLUE,
                    phase=phase,
                    dur=3.2,
                    width=3.0,
                    head=True,
                    packets=3,
                )
            )

        master_pts: List[Point] = []
        for cid, src, tgt in mx_edges:
            if cid in ("t4_m2", "t4_m4", "t4_m5", "t4_m6"):
                continue
            if src not in mx_verts or tgt not in mx_verts:
                continue
            sbox = mx_verts[src][:4]
            tbox = mx_verts[tgt][:4]
            pts = _edge_port_points(sbox, tbox)
            ymid = (sbox[1] + tbox[1]) / 2.0
            if ymid < 300.0:
                col = RED
            elif ymid < 520.0:
                col = BLUE
            elif ymid < 740.0:
                col = GREEN if "yes1" in cid or "done" in tgt else AMBER
            else:
                col = GREEN if "map" in cid or "map" in tgt else RED
            out.append(
                _flow(
                    pts,
                    col,
                    phase=phase,
                    dur=1.4,
                    width=2.6,
                    head=True,
                    packets=1,
                )
            )
            if cid in ("t1_edge_1", "t1_edge_2", "t2_edge_in", "t2_edge_calls", "t2_edge_checks", "t3_e1", "t3_e2", "t3_e_yes1", "t4_edge_maps"):
                master_pts.extend(pts)

        if len(master_pts) >= 2:
            out.append(_render_master_packet(master_pts, BLUE, phase, dur=4.8))

        strip_y = float(ch - 26) if ch >= 1030 else 892.0
        out.append(
            _render_phase_telemetry_strip(
                cw,
                strip_y,
                [
                    "① 0–1.2s · Tier 01 Trigger & Failure",
                    "② 1.2–2.4s · Tier 02 Pre-Tool Gate",
                    "③ 2.4–3.6s · Tier 03 Check-Fix Loop",
                    "④ 3.6–4.8s · Tier 04 Verified Metrics",
                ],
                [RED, BLUE, AMBER, GREEN],
                phase,
            )
        )
        return "\n".join(out)

    # Case B: Infographics & Sculptural Architecture Posters (T55-T67, T90-T209)
    # Collect stage nodes from circles, stage rects, and interior mxCell vertices
    stage_nodes: List[Tuple[float, float, float, float, str]] = []
    for cx, cy, r in sorted(bg_circles, key=lambda c: (round(c[1] / 90.0), c[0])):
        if r >= 22.0:
            stage_nodes.append((cx - r, cy - r, 2.0 * r, 2.0 * r, "circle"))

    for rx, ry, rw, rh in sorted(bg_rects, key=lambda b: (round(b[1] / 90.0), b[0])):
        if 210.0 <= ry <= 780.0 and rw <= 720.0 and rh <= 360.0:
            stage_nodes.append((rx, ry, rw, rh, "rect"))

    for cid, (vx, vy, vw, vh, _) in sorted(mx_verts.items(), key=lambda kv: (round(kv[1][1] / 95.0), kv[1][0])):
        if cid.startswith(("bg", "poster_bg", "hdr", "brand", "ftr")):
            continue
        if 165.0 <= vy <= ch - 95.0 and 48.0 <= vw <= cw - 40.0 and 24.0 <= vh <= 420.0:
            stage_nodes.append((vx, vy, vw, vh, "mx"))

    # Select 4 representative stage nodes across the diagram's reading order for 4-phase spotlighting
    spot_candidates = [n for n in stage_nodes if 170.0 <= n[1] <= 915.0]
    if len(spot_candidates) >= 4:
        idxs = [
            0,
            max(1, len(spot_candidates) // 3),
            max(2, (2 * len(spot_candidates)) // 3),
            len(spot_candidates) - 1,
        ]
        seen_idx = set()
        phase_num = 1
        for i in idxs:
            if i in seen_idx or phase_num > 4:
                continue
            seen_idx.add(i)
            nx, ny, nw, nh, kind = spot_candidates[i]
            col = phase_colors[(phase_num - 1) % 4]
            if kind == "circle":
                out.append(_render_spot_circle(nx + nw / 2.0, ny + nh / 2.0, nw / 2.0, col, phase_num, phase))
            else:
                out.append(_render_spot_rect(nx, ny, nw, nh, col, phase_num, phase, rx=12.0))
            phase_num += 1

    # Animate all internal connector lines and paths extracted from the .drawio SVG stage
    conduit_paths: List[List[Point]] = []
    for seg in bg_lines[:14]:
        conduit_paths.append(seg)
    for ppts in bg_paths[:10]:
        conduit_paths.append(ppts)

    # Also build causal stage-to-stage bridges across the diagram's interior nodes so every stage is connected end-to-end
    interior_centers: List[Point] = []
    for nx, ny, nw, nh, kind in spot_candidates[:12]:
        pt = (nx + nw / 2.0, ny + nh / 2.0)
        if not interior_centers or ((pt[0] - interior_centers[-1][0]) ** 2 + (pt[1] - interior_centers[-1][1]) ** 2) ** 0.5 >= 58.0:
            interior_centers.append(pt)

    for idx, pts in enumerate(conduit_paths):
        col = phase_colors[idx % len(phase_colors)]
        out.append(
            _flow(
                pts,
                col,
                phase=phase,
                dur=1.35 + (idx % 3) * 0.2,
                width=2.6,
                head=True,
                packets=1,
            )
        )

    for idx in range(len(interior_centers) - 1):
        p1, p2 = interior_centers[idx], interior_centers[idx + 1]
        col = phase_colors[idx % len(phase_colors)]
        if abs(p1[0] - p2[0]) > 45.0 and abs(p1[1] - p2[1]) > 45.0:
            mid = (p2[0], p1[1]) if idx % 2 == 0 else (p1[0], p2[1])
            bridge_pts = [p1, mid, p2]
        else:
            bridge_pts = [p1, p2]
        out.append(
            _flow(
                bridge_pts,
                col,
                phase=phase,
                dur=1.5,
                width=2.5,
                head=True,
                packets=1,
            )
        )

    # Master end-to-end packet route across interior centers (or conduit endpoints)
    master_route: List[Point] = list(interior_centers)
    if len(master_route) < 3 and conduit_paths:
        for seg in conduit_paths[:6]:
            master_route.extend(seg)
    if len(master_route) >= 2:
        out.append(_render_master_packet(master_route, accent or BLUE, phase, dur=4.8))

    # Compute verified clear horizontal gutter for the 4-Phase Telemetry Strip
    if ch >= 1140:
        strip_y = 955.0
    elif tid in ("T61", "T62", "T63", "T64", "T66"):
        strip_y = 940.0
    elif tid in ("T58", "T60", "T67"):
        strip_y = 958.0
    elif tid == "T65":
        strip_y = 148.0
    elif tid == "T59":
        strip_y = 283.0
    else:
        strip_y = float(ch - 24)

    out.append(
        _render_phase_telemetry_strip(
            cw,
            strip_y,
            [
                "① 0–1.2s · Signal Ingress & Context",
                "② 1.2–2.4s · Policy Gate & Routing",
                "③ 2.4–3.6s · Core Agent Execution",
                "④ 3.6–4.8s · Telemetry & Verified ACK",
            ],
            phase_colors,
            phase,
        )
    )
    return "\n".join(out)


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

    conduit = _build_template_flow_overlay(tid, cw, ch, accent, meta, phase=phase)
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

    # Fast fallback only when Chrome is unavailable or single-frame requested
    if src_png.exists() and (frames <= 1 or chrome is None):
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
