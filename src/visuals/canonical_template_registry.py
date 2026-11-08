"""Canonical Template Registry — 128 Certified Unique `Best` + `High` Visual Templates.

Consolidates the entire visual catalog with zero legacy Gen-1 raw Python SVG box approximations (`Law 18` / `Rule 57B`):
- 15 PromptCanvas Canonical `Best` Blueprints:
    `T54`–`T67` (PromptCanvas `#53`–`#66` Infographics) + `T79` (Canonical 4-Tier Spine Archetype, hosting `23` Topic Posts `T01, T53, T68–T78, T80–T89` on disk and in `T79.topic_posts`).
- 24 Kept Session `Best` Blueprints (`Gen-4` Sculptural Posters):
    `T90, T91, T94, T98, T100, T101, T103, T105, T110, T111, T115, T125, T129, T131, T150, T152, T159, T175, T176, T178, T188, T190, T191, T195`.
- 33 Refactored Session `Best` Blueprints (`Gen-5` Open-Drafting-Grid Sculptural Posters):
    `T95, T102, T104, T106, T107, T108, T118, T124, T128, T130, T142, T145, T148, T153, T155, T158, T163, T165, T167, T168, T169, T171, T181, T183, T185, T186, T192, T194, T197, T198, T199, T203, T207`.
- 44 Kept Session `High` Blueprints (`Gen-4` Certified High):
    `T92, T93, T96, T97, T99, T109, T112, T117, T119, T120, T121, T122, T123, T127, T133, T136, T137, T140, T146, T151, T154, T157, T160, T161, T162, T164, T170, T172, T173, T174, T177, T179, T184, T187, T193, T196, T200, T201, T202, T204, T205, T206, T208, T209`.

Total Certified Gallery Templates = `128` (`84 Best` + `44 High`, `0 Medium/Low/Worst`).
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


from src.visuals.generative_template_synthesizer import (
    GENERATIVE_GRAMMAR_TEMPLATE_META,
    synthesize_generative_template_svg,
)


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
    for tid in sorted(GENERATIVE_GRAMMAR_TEMPLATE_META.keys(), key=lambda k: int(k[1:])):
        meta[tid] = dict(GENERATIVE_GRAMMAR_TEMPLATE_META[tid])
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


def _parse_mx_style(style_str: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in str(style_str or "").split(";"):
        t = part.strip()
        if not t:
            continue
        if "=" in t:
            k, v = t.split("=", 1)
            out[k.strip()] = v.strip()
        else:
            out[t] = "1"
    return out


def _resolve_mx_edge_points(
    sbox: Optional[Tuple[float, float, float, float]],
    tbox: Optional[Tuple[float, float, float, float]],
    style: Dict[str, str],
    waypoints: Sequence[Point],
    source_pt: Optional[Point],
    target_pt: Optional[Point],
) -> List[Point]:
    """Resolve exact orthogonal Draw.io edge polyline from exitX/Y, waypoints, and entryX/Y."""
    pts: List[Point] = []
    if sbox is not None:
        sx, sy, sw, sh = sbox
        if "exitX" in style and "exitY" in style:
            pts.append((sx + sw * float(style["exitX"]), sy + sh * float(style["exitY"])))
        elif waypoints:
            wx, wy = waypoints[0]
            scx, scy = sx + sw / 2.0, sy + sh / 2.0
            if abs(wx - scx) <= sw * 0.48:
                pts.append((wx, sy + sh if wy >= scy else sy))
            elif abs(wy - scy) <= sh * 0.48:
                pts.append((sx + sw if wx >= scx else sx, wy))
            else:
                pts.append((scx, sy + sh if wy >= scy else sy))
        elif tbox is not None:
            tx, ty, tw, th = tbox
            scx, scy = sx + sw / 2.0, sy + sh / 2.0
            tcx, tcy = tx + tw / 2.0, ty + th / 2.0
            if abs(scy - tcy) <= max(sh, th) * 0.75:
                pts.append((sx + sw if tcx >= scx else sx, scy))
            else:
                pts.append((scx, sy + sh if tcy >= scy else sy))
    elif source_pt is not None:
        pts.append(source_pt)

    for wp in waypoints:
        pts.append(wp)

    if tbox is not None:
        tx, ty, tw, th = tbox
        if "entryX" in style and "entryY" in style:
            pts.append((tx + tw * float(style["entryX"]), ty + th * float(style["entryY"])))
        elif pts:
            lx, ly = pts[-1]
            tcx, tcy = tx + tw / 2.0, ty + th / 2.0
            if tx - 4.0 <= lx <= tx + tw + 4.0:
                pts.append((lx, ty if ly <= tcy else ty + th))
            elif ty - 4.0 <= ly <= ty + th + 4.0:
                pts.append((tx if lx <= tcx else tx + tw, ly))
            elif abs(ly - tcy) <= abs(lx - tcx):
                pts.append((tx if lx <= tcx else tx + tw, tcy))
            else:
                pts.append((tcx, ty if ly <= tcy else ty + th))
    elif target_pt is not None:
        pts.append(target_pt)

    # Orthogonalize micro-slants (<= 3px) so vertical/horizontal shafts stay 100% collinear
    ortho: List[Point] = []
    for p in pts:
        if not ortho:
            ortho.append(p)
            continue
        px, py = ortho[-1]
        nx, ny = p
        if abs(nx - px) <= 3.0 and abs(ny - py) > 3.0:
            nx = px
        elif abs(ny - py) <= 3.0 and abs(nx - px) > 3.0:
            ny = py
        if abs(nx - px) > 1.0 or abs(ny - py) > 1.0:
            ortho.append((nx, ny))
    return ortho


def _clip_segment_outside_boxes(
    p1: Point,
    p2: Point,
    boxes: Sequence[Tuple[float, float, float, float]],
) -> List[Tuple[Point, Point]]:
    """Liang-Barsky 1D interval subtraction: return sub-segments of (p1, p2) strictly outside all boxes."""
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    seg_len = (dx * dx + dy * dy) ** 0.5
    if seg_len < 2.0:
        return []

    intervals: List[Tuple[float, float]] = [(0.0, 1.0)]
    for bx0, by0, bx1, by1 in boxes:
        if max(x1, x2) <= bx0 or min(x1, x2) >= bx1 or max(y1, y2) <= by0 or min(y1, y2) >= by1:
            continue
        t0, t1 = 0.0, 1.0
        inside = True
        for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
            if abs(p) < 1e-9:
                if q < 0.0:
                    inside = False
                    break
            else:
                r = q / p
                if p < 0.0:
                    if r > t1:
                        inside = False
                        break
                    if r > t0:
                        t0 = r
                else:
                    if r < t0:
                        inside = False
                        break
                    if r < t1:
                        t1 = r
        if inside and t1 > t0 + 1e-6:
            next_intervals: List[Tuple[float, float]] = []
            for a, b in intervals:
                if t1 <= a or t0 >= b:
                    next_intervals.append((a, b))
                else:
                    if t0 > a + 1e-4:
                        next_intervals.append((a, t0))
                    if t1 < b - 1e-4:
                        next_intervals.append((t1, b))
            intervals = next_intervals
            if not intervals:
                return []

    out: List[Tuple[Point, Point]] = []
    for a, b in intervals:
        if (b - a) * seg_len >= 10.0:
            out.append(((x1 + a * dx, y1 + a * dy), (x1 + b * dx, y1 + b * dy)))
    return out


def _clip_polyline_outside_boxes(
    pts: Sequence[Point],
    boxes: Sequence[Tuple[float, float, float, float]],
    min_len: float = 16.0,
) -> List[List[Point]]:
    """Split and clip a polyline against forbidden boxes so 0.0px ever touches any card, pill, or text."""
    if len(pts) < 2:
        return []
    chains: List[List[Point]] = []
    for i in range(len(pts) - 1):
        sub_segs = _clip_segment_outside_boxes(pts[i], pts[i + 1], boxes)
        for sp1, sp2 in sub_segs:
            if chains and abs(chains[-1][-1][0] - sp1[0]) <= 2.0 and abs(chains[-1][-1][1] - sp1[1]) <= 2.0:
                chains[-1].append(sp2)
            else:
                chains.append([sp1, sp2])
    valid: List[List[Point]] = []
    for ch_pts in chains:
        total = sum(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5 for p1, p2 in zip(ch_pts, ch_pts[1:]))
        if total >= min_len:
            valid.append(ch_pts)
    return valid


def _extract_drawio_topology(tid: str, cw: int, ch: int) -> Dict[str, Any]:
    """Extract internal connector lines, stage rects, circles, mxGraph edges, and forbidden card/text boxes from {tid}.drawio."""
    cached = _DRAWIO_TOPOLOGY_CACHE.get(tid)
    if cached is not None:
        return cached

    import xml.etree.ElementTree as ET

    drawio_path = _TEMPLATE_GALLERY_DIR / f"{tid}.drawio"
    if not drawio_path.exists() and tid.startswith("T79_"):
        drawio_path = _TEMPLATE_GALLERY_DIR / "T79.drawio"

    mx_verts: Dict[str, Tuple[float, float, float, float, str]] = {}
    raw_edges: List[Dict[str, Any]] = []
    bg_lines: List[List[Point]] = []
    bg_circles: List[Tuple[float, float, float]] = []
    bg_rects: List[Tuple[float, float, float, float]] = []
    forbidden_boxes: List[Tuple[float, float, float, float]] = [
        (0.0, 0.0, float(cw), 115.0),
        (0.0, float(ch - 52), float(cw), float(ch)),
    ]

    if drawio_path.exists():
        try:
            root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
            bg_svg = ""
            has_poster_bg = False
            for c in root.findall(".//mxCell"):
                cid = c.attrib.get("id", "")
                val = c.attrib.get("value", "")
                if "<svg" in val and cid.startswith(("bg", "poster_bg")):
                    bg_svg = val
                    has_poster_bg = True
                elif c.attrib.get("edge") == "1":
                    src = c.attrib.get("source", "")
                    tgt = c.attrib.get("target", "")
                    style = _parse_mx_style(c.attrib.get("style", ""))
                    g = c.find("mxGeometry")
                    wps: List[Point] = []
                    sp: Optional[Point] = None
                    tp: Optional[Point] = None
                    if g is not None:
                        for pt in g.findall("mxPoint"):
                            role = pt.attrib.get("as", "")
                            if role == "sourcePoint":
                                sp = (float(pt.attrib.get("x", 0.0)), float(pt.attrib.get("y", 0.0)))
                            elif role == "targetPoint":
                                tp = (float(pt.attrib.get("x", 0.0)), float(pt.attrib.get("y", 0.0)))
                        arr = g.find("Array[@as='points']")
                        if arr is not None:
                            for pt in arr.findall("mxPoint"):
                                wps.append((float(pt.attrib.get("x", 0.0)), float(pt.attrib.get("y", 0.0))))
                    clean_lbl = re.sub(r"<[^>]+>", " ", val).strip()
                    clean_lbl = re.sub(r"\s+", " ", clean_lbl)
                    raw_edges.append(
                        {
                            "id": cid,
                            "src": src,
                            "tgt": tgt,
                            "style": style,
                            "waypoints": wps,
                            "source_pt": sp,
                            "target_pt": tp,
                            "label": clean_lbl,
                        }
                    )
                elif c.attrib.get("vertex") == "1":
                    g = c.find("mxGeometry")
                    if g is not None and g.attrib.get("x") is not None and g.attrib.get("y") is not None and g.attrib.get("relative") != "1":
                        vx = float(g.attrib.get("x", 0.0))
                        vy = float(g.attrib.get("y", 0.0))
                        vw = float(g.attrib.get("width", 0.0))
                        vh = float(g.attrib.get("height", 0.0))
                        clean_txt = re.sub(r"<[^>]+>", " ", val).strip()
                        clean_txt = re.sub(r"\s+", " ", clean_txt)
                        mx_verts[cid] = (vx, vy, vw, vh, clean_txt)

            # GraphViewer translates ONLY graphs that lack a (0,0) poster_bg backdrop (i.e. T01, T53, T68-T89)
            offset_x, offset_y = 0.0, 0.0
            if mx_verts and not has_poster_bg:
                min_vx = min(v[0] for v in mx_verts.values())
                min_vy = min(v[1] for v in mx_verts.values())
                if min_vx > 2.0 or min_vy > 2.0:
                    offset_x, offset_y = min_vx, min_vy
                    mx_verts = {
                        k: (vx - offset_x, vy - offset_y, vw, vh, txt)
                        for k, (vx, vy, vw, vh, txt) in mx_verts.items()
                    }

            # Register opaque leaf content vertices as forbidden boxes so no conduit ever crosses a card or pill
            container_prefixes = (
                "band",
                "t1_card",
                "t2_card",
                "t3_card",
                "t4_card",
                "t1_left",
                "t1_right",
                "t2_sub",
                "t4_left",
                "t4_right",
                "col54_L",
                "tr59_",
                "z61_",
                "hdr_cols",
                "grid",
                "left_hdr",
                "right_hdr",
                "div_line",
                "stage_frame",
            )
            for cid, (vx, vy, vw, vh, txt) in mx_verts.items():
                if cid.startswith(container_prefixes):
                    continue
                if vw * vh >= float(cw * ch) * 0.20 and not txt:
                    continue
                is_parent_container = False
                for ocid, (ox, oy, ow, oh, _) in mx_verts.items():
                    if ocid != cid and ow * oh < vw * vh * 0.75:
                        ocx, ocy = ox + ow / 2.0, oy + oh / 2.0
                        if vx <= ocx <= vx + vw and vy <= ocy <= vy + vh:
                            is_parent_container = True
                            break
                if is_parent_container:
                    continue
                pad = 0.5
                forbidden_boxes.append((vx - pad, vy - pad, vx + vw + pad, vy + vh + pad))

            mx_edges: List[Tuple[str, str, str, List[Point], Dict[str, str]]] = []
            for e in raw_edges:
                cid = e["id"]
                src = e["src"]
                tgt = e["tgt"]
                sbox = mx_verts[src][:4] if src in mx_verts else None
                tbox = mx_verts[tgt][:4] if tgt in mx_verts else None
                wps = [(wx - offset_x, wy - offset_y) for wx, wy in e["waypoints"]]
                sp = (e["source_pt"][0] - offset_x, e["source_pt"][1] - offset_y) if e["source_pt"] else None
                tp = (e["target_pt"][0] - offset_x, e["target_pt"][1] - offset_y) if e["target_pt"] else None
                pts = _resolve_mx_edge_points(sbox, tbox, e["style"], wps, sp, tp)
                if len(pts) >= 2:
                    mx_edges.append((cid, src, tgt, pts, e["style"]))
                    if e["label"] and len(pts) >= 2:
                        # Protect midpoint edge label text (e.g., 'retries', 'check', 'yes', 'no', 'win')
                        mx_pt, my_pt = _pat(pts, 0.5)
                        lw = max(28.0, len(e["label"]) * 6.2 + 8.0)
                        lh = 16.0
                        forbidden_boxes.append((mx_pt - lw / 2.0, my_pt - lh / 2.0, mx_pt + lw / 2.0, my_pt + lh / 2.0))

            if bg_svg:
                body = re.sub(r"<defs>.*?</defs>", "", bg_svg, flags=re.DOTALL)
                body = re.sub(
                    r'<g transform="translate\(\s*(?:30|644|696|788)\s*,\s*(?:18|22)\s*\)"[^>]*>.*?</g>',
                    "",
                    body,
                    flags=re.DOTALL,
                )
                for m in re.finditer(r"<(line|circle|rect|text)\b([^>]*)>(.*?)</\1>|<(line|circle|rect)\b([^>]*)/?>", body, flags=re.DOTALL):
                    tag = m.group(1) or m.group(4)
                    attr_str = m.group(2) if m.group(1) else m.group(5)
                    inner_txt = (m.group(3) or "").strip() if m.group(1) else ""
                    attrs = dict(re.findall(r'([a-zA-Z0-9_:-]+)="([^"]*)"', attr_str or ""))
                    if tag == "line":
                        try:
                            x1, y1 = float(attrs["x1"]), float(attrs["y1"])
                            x2, y2 = float(attrs["x2"]), float(attrs["y2"])
                            seg_len = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                            is_ortho = abs(x1 - x2) <= 3.0 or abs(y1 - y2) <= 3.0
                            has_marker_or_dash = bool(attrs.get("marker-end") or attrs.get("stroke-dasharray"))
                            if 135.0 <= min(y1, y2) and max(y1, y2) <= ch - 60.0 and 18.0 <= seg_len <= 780.0:
                                if is_ortho or has_marker_or_dash:
                                    bg_lines.append([(x1, y1), (x2, y2)])
                        except (KeyError, ValueError):
                            pass
                    elif tag == "circle":
                        try:
                            cx, cy, r = float(attrs["cx"]), float(attrs["cy"]), float(attrs["r"])
                            if 16.0 <= r <= 185.0 and 175.0 <= cy <= ch - 75.0:
                                bg_circles.append((cx, cy, r))
                                if r <= 52.0:
                                    forbidden_boxes.append((cx - r - 2.0, cy - r - 2.0, cx + r + 2.0, cy + r + 2.0))
                        except (KeyError, ValueError):
                            pass
                    elif tag == "rect":
                        try:
                            rx, ry = float(attrs["x"]), float(attrs["y"])
                            rw, rh = float(attrs["width"]), float(attrs["height"])
                            if 180.0 <= ry <= ch - 85.0 and 44.0 <= rw <= cw - 85.0 and 18.0 <= rh <= 420.0:
                                bg_rects.append((rx, ry, rw, rh))
                                if rw <= 320.0 and rh <= 95.0:
                                    forbidden_boxes.append((rx - 2.0, ry - 2.0, rx + rw + 2.0, ry + rh + 2.0))
                        except (KeyError, ValueError):
                            pass
                    elif tag == "text" and inner_txt:
                        try:
                            tx = float(attrs.get("x", 0.0))
                            ty = float(attrs.get("y", 0.0))
                            fs = float(re.sub(r"[^0-9.]", "", attrs.get("font-size", "11")) or 11.0)
                            clean_t = re.sub(r"<[^>]+>", "", inner_txt).strip()
                            if clean_t and ty >= 120.0:
                                tw = len(clean_t) * fs * 0.56 + 8.0
                                anchor = attrs.get("text-anchor", "start")
                                if anchor == "middle":
                                    tx0, tx1 = tx - tw / 2.0, tx + tw / 2.0
                                elif anchor == "end":
                                    tx0, tx1 = tx - tw, tx
                                else:
                                    tx0, tx1 = tx, tx + tw
                                forbidden_boxes.append((tx0 - 3.0, ty - fs - 2.0, tx1 + 3.0, ty + 4.0))
                        except (ValueError, KeyError):
                            pass
        except Exception:
            mx_edges = []

    if tid == "T56":
        # Protect the executive portrait illustration in T56
        forbidden_boxes.append((28.0, 200.0, 305.0, 560.0))

    topo = {
        "mx_verts": mx_verts,
        "mx_edges": mx_edges,
        "bg_lines": bg_lines,
        "bg_circles": bg_circles,
        "bg_rects": bg_rects,
        "forbidden_boxes": forbidden_boxes,
    }
    _DRAWIO_TOPOLOGY_CACHE[tid] = topo
    return topo


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
    """Render a clean, non-dashed 4-phase outer perimeter glow around a diagram zone or card."""
    cls = f' class="phase-glow-{phase_idx}"' if phase is None else ""
    if phase is not None:
        active = int((phase * 4.0) % 4) + 1 == phase_idx
        op = 0.82 if active else 0.16
        sw = 2.6 if active else 1.2
    else:
        op = 0.72
        sw = 2.2
    return (
        f'<rect x="{x - 2.0:.1f}" y="{y - 2.0:.1f}" width="{w + 4.0:.1f}" height="{h + 4.0:.1f}" rx="{rx:.1f}"'
        f'{cls} fill="none" stroke="{color}" stroke-width="{sw:.1f}" stroke-opacity="{op:.2f}"/>'
    )


def _render_spot_circle(
    cx: float,
    cy: float,
    r: float,
    color: str,
    phase_idx: int,
    phase: Optional[float],
) -> str:
    """Render a clean, non-dashed 4-phase outer perimeter ring around a circular lens or bubble."""
    cls = f' class="phase-glow-{phase_idx}"' if phase is None else ""
    if phase is not None:
        active = int((phase * 4.0) % 4) + 1 == phase_idx
        op = 0.84 if active else 0.18
        sw = 2.8 if active else 1.3
    else:
        op = 0.74
        sw = 2.4
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 3.0:.1f}"{cls} fill="none" '
        f'stroke="{color}" stroke-width="{sw:.1f}" stroke-opacity="{op:.2f}"/>'
    )


def _conduit_pulse(
    pts: Sequence[Point],
    color: str,
    phase: Optional[float],
    forbidden_boxes: Sequence[Tuple[float, float, float, float]] = (),
    dur: float = 1.4,
    width: float = 2.2,
    packets: int = 1,
) -> str:
    """Render a zero-track, zero-occlusion animated signal conduit strictly outside all card/text boxes."""
    chains = _clip_polyline_outside_boxes(pts, forbidden_boxes, min_len=14.0) if forbidden_boxes else [list(pts)]
    out: List[str] = []
    for ch_pts in chains:
        out.append(
            _flow(
                ch_pts,
                color,
                phase=phase,
                dur=dur,
                width=width,
                head=False,
                packets=packets,
                dash="7 5",
                track=False,
            )
        )
    return "\n".join(s for s in out if s)


def _render_master_packet(pts: Sequence[Point], color: str, phase: Optional[float], dur: float = 4.8) -> str:
    """Render a high-visibility multi-ring master signal packet traversing the end-to-end gutter route."""
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
            f'<circle r="9.0" fill="{color}" fill-opacity="0.16"/>'
            f'<circle r="5.8" fill="{color}" fill-opacity="0.30"/>'
            f'<circle r="4.0" fill="#FFFFFF" stroke="{color}" stroke-width="2.2"/>'
            f'<circle r="1.8" fill="{color}"/>'
            f'<animateMotion dur="{dur:.2f}s" begin="0s" repeatCount="indefinite" path="{d}"/>'
            f"</g>"
        )
    px, py = _pat(clean, phase % 1.0)
    return (
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9.0" fill="{color}" fill-opacity="0.16"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.8" fill="{color}" fill-opacity="0.30"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.0" fill="#FFFFFF" stroke="{color}" stroke-width="2.2"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.8" fill="{color}"/>'
    )


def _build_template_flow_overlay(
    tid: str,
    cw: int,
    ch: int,
    accent: str,
    meta: Dict[str, Any],
    phase: Optional[float] = None,
) -> str:
    """Compile clean, zero-occlusion, gutter-only multi-phase signal animations for {tid}."""
    out: List[str] = []
    phase_colors = [BLUE, GREEN, AMBER, PURPLE]
    topo = _extract_drawio_topology(tid, cw, ch)
    mx_verts = topo["mx_verts"]
    mx_edges = topo["mx_edges"]
    bg_lines = topo["bg_lines"]
    bg_circles = topo["bg_circles"]
    bg_rects = topo["bg_rects"]
    forbidden_boxes = topo["forbidden_boxes"]

    # 1. Bespoke Flagship Exemplar: T160 (C4 Model 3-Lens Telescopic AI Architecture Zoom, 920x1150)
    if tid == "T160":
        out.append(_render_spot_circle(156.0, 446.0, 86.0, BLUE, 1, phase))
        out.append(_render_spot_circle(438.0, 540.0, 108.0, GREEN, 2, phase))
        out.append(_render_spot_circle(734.0, 632.0, 122.0, AMBER, 3, phase))
        out.append(_render_spot_rect(42.0, 788.0, 836.0, 122.0, PURPLE, 4, phase, rx=16.0))

        t160_routes = [
            ([(242.0, 446.0), (330.0, 505.0)], BLUE, 1.4, 2),
            ([(184.0, 362.0), (426.0, 430.0)], BLUE, 1.6, 1),
            ([(156.0, 532.0), (388.0, 646.0)], GREEN, 1.6, 1),
            ([(546.0, 540.0), (612.0, 595.0)], AMBER, 1.4, 2),
            ([(488.0, 434.0), (734.0, 508.0)], AMBER, 1.6, 1),
            ([(456.0, 648.0), (698.0, 752.0)], AMBER, 1.6, 1),
            ([(734.0, 756.0), (734.0, 786.0)], PURPLE, 1.3, 1),
            ([(163.0, 912.0), (163.0, 982.0)], BLUE, 1.4, 1),
            ([(460.0, 912.0), (460.0, 982.0)], GREEN, 1.4, 1),
            ([(757.0, 912.0), (757.0, 982.0)], AMBER, 1.4, 1),
        ]
        for r_pts, col, dur, pkts in t160_routes:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=dur, packets=pkts))

        out.append(
            _render_master_packet(
                [
                    (242.0, 446.0),
                    (330.0, 505.0),
                    (438.0, 430.0),
                    (546.0, 540.0),
                    (612.0, 595.0),
                    (734.0, 508.0),
                    (734.0, 756.0),
                    (734.0, 786.0),
                ],
                BLUE,
                phase,
                dur=4.8,
            )
        )
        return "\n".join(s for s in out if s)

    # 2. Bespoke PromptCanvas Infographics (T55-T67) with exact inter-card gutter coordinates
    if tid == "T55":
        out.append(_render_spot_rect(20.0, 122.0, 414.0, 716.0, BLUE, 1, phase, rx=14.0))
        out.append(_render_spot_rect(20.0, 882.0, 414.0, 128.0, PURPLE, 2, phase, rx=12.0))
        out.append(_render_spot_rect(452.0, 280.0, 418.0, 350.0, GREEN, 3, phase, rx=14.0))
        out.append(_render_spot_rect(452.0, 644.0, 418.0, 366.0, AMBER, 4, phase, rx=14.0))
        for r_pts, col in [
            ([(443.0, 186.0), (443.0, 918.0)], BLUE),
            ([(227.0, 840.0), (227.0, 880.0)], PURPLE),
            ([(434.0, 364.0), (452.0, 364.0)], GREEN),
            ([(878.0, 364.0), (878.0, 546.0)], GREEN),
            ([(878.0, 546.0), (878.0, 728.0)], AMBER),
            ([(878.0, 728.0), (878.0, 918.0)], PURPLE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.5, packets=1))
        out.append(_render_master_packet([(443.0, 186.0), (443.0, 364.0), (443.0, 546.0), (443.0, 728.0), (443.0, 918.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T56":
        out.append(_render_spot_rect(152.0, 218.0, 140.0, 68.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_circle(116.0, 642.0, 56.0, GREEN, 2, phase))
        out.append(_render_spot_circle(198.0, 800.0, 58.0, AMBER, 3, phase))
        out.append(_render_spot_circle(138.0, 938.0, 58.0, PURPLE, 4, phase))
        # Conduits flow strictly along the vertical divider (x=312) and horizontal inter-row bubble gutters (y=295, 428, 561, 698, 830)
        for r_pts, col in [
            ([(294.0, 252.0), (312.0, 252.0), (312.0, 295.0), (836.0, 295.0)], BLUE),
            ([(312.0, 295.0), (312.0, 428.0), (836.0, 428.0)], PURPLE),
            ([(174.0, 642.0), (312.0, 642.0), (312.0, 561.0), (836.0, 561.0)], GREEN),
            ([(312.0, 642.0), (312.0, 698.0), (836.0, 698.0)], AMBER),
            ([(258.0, 800.0), (312.0, 800.0), (312.0, 830.0), (836.0, 830.0)], RED),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.6, packets=1))
        out.append(
            _render_master_packet(
                [(312.0, 252.0), (312.0, 295.0), (836.0, 295.0), (836.0, 561.0), (312.0, 561.0), (312.0, 830.0), (836.0, 830.0)],
                RED,
                phase,
            )
        )
        return "\n".join(s for s in out if s)

    if tid == "T57":
        out.append(_render_spot_rect(414.0, 280.0, 306.0, 106.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(414.0, 425.0, 306.0, 106.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(414.0, 570.0, 306.0, 106.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(414.0, 860.0, 306.0, 106.0, PURPLE, 4, phase, rx=12.0))
        # Conduits connect consecutive cards vertically in the 39px inter-row gutters + outer column spine
        for r_pts, col in [
            ([(198.0, 238.0), (198.0, 278.0)], RED),
            ([(198.0, 388.0), (198.0, 423.0)], RED),
            ([(198.0, 533.0), (198.0, 568.0)], AMBER),
            ([(198.0, 678.0), (198.0, 713.0)], AMBER),
            ([(198.0, 823.0), (198.0, 858.0)], RED),
            ([(567.0, 238.0), (567.0, 278.0)], BLUE),
            ([(567.0, 388.0), (567.0, 423.0)], GREEN),
            ([(567.0, 533.0), (567.0, 568.0)], TEAL),
            ([(567.0, 678.0), (567.0, 713.0)], PURPLE),
            ([(567.0, 823.0), (567.0, 858.0)], GREEN),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(
            _render_master_packet(
                [(738.0, 280.0), (738.0, 478.0), (738.0, 623.0), (738.0, 768.0), (738.0, 960.0)],
                GREEN,
                phase,
            )
        )
        return "\n".join(s for s in out if s)

    if tid == "T58":
        out.append(_render_spot_rect(130.0, 266.0, 505.0, 82.0, BLUE, 1, phase, rx=10.0))
        out.append(_render_spot_rect(170.0, 394.0, 425.0, 82.0, GREEN, 2, phase, rx=10.0))
        out.append(_render_spot_rect(260.0, 646.0, 245.0, 92.0, AMBER, 3, phase, rx=10.0))
        out.append(_render_spot_rect(160.0, 904.0, 445.0, 50.0, PURPLE, 4, phase, rx=10.0))
        for r_pts, col in [
            ([(382.5, 350.0), (382.5, 392.0)], BLUE),
            ([(382.5, 478.0), (382.5, 518.0)], GREEN),
            ([(382.5, 608.0), (382.5, 644.0)], AMBER),
            ([(382.5, 740.0), (382.5, 774.0)], PURPLE),
            ([(382.5, 868.0), (382.5, 902.0)], GREEN),
            ([(88.0, 307.0), (128.0, 435.0), (172.0, 563.0), (216.0, 692.0)], BLUE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(88.0, 307.0), (128.0, 435.0), (172.0, 563.0), (216.0, 692.0), (260.0, 821.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T59":
        out.append(_render_spot_rect(130.0, 180.0, 586.0, 102.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(130.0, 428.0, 586.0, 102.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(130.0, 676.0, 586.0, 102.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(50.0, 916.0, 666.0, 48.0, PURPLE, 4, phase, rx=10.0))
        for r_pts, col in [
            ([(84.0, 267.0), (84.0, 319.0)], BLUE),
            ([(84.0, 391.0), (84.0, 443.0)], GREEN),
            ([(84.0, 515.0), (84.0, 567.0)], AMBER),
            ([(84.0, 639.0), (84.0, 691.0)], PURPLE),
            ([(84.0, 763.0), (84.0, 815.0)], BLUE),
            ([(734.0, 231.0), (734.0, 851.0)], GREEN),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(734.0, 231.0), (734.0, 479.0), (734.0, 727.0), (734.0, 851.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T60":
        out.append(_render_spot_rect(38.0, 192.0, 689.0, 160.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(38.0, 366.0, 689.0, 160.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(38.0, 540.0, 689.0, 160.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(38.0, 714.0, 689.0, 160.0, PURPLE, 4, phase, rx=12.0))
        for r_pts, col in [
            ([(22.0, 272.0), (22.0, 896.0)], BLUE),
            ([(38.0, 359.0), (727.0, 359.0)], BLUE),
            ([(38.0, 533.0), (727.0, 533.0)], GREEN),
            ([(38.0, 707.0), (727.0, 707.0)], AMBER),
            ([(38.0, 885.0), (727.0, 885.0)], PURPLE),
            ([(742.0, 272.0), (742.0, 896.0)], GREEN),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(22.0, 272.0), (22.0, 446.0), (22.0, 620.0), (22.0, 794.0), (22.0, 920.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T61":
        out.append(_render_spot_rect(180.0, 492.0, 224.0, 160.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(180.0, 240.0, 280.0, 180.0, PURPLE, 2, phase, rx=12.0))
        out.append(_render_spot_rect(492.0, 392.0, 228.0, 204.0, GREEN, 3, phase, rx=12.0))
        out.append(_render_spot_rect(423.0, 638.0, 297.0, 288.0, AMBER, 4, phase, rx=12.0))
        for r_pts, col in [
            ([(88.0, 572.0), (178.0, 572.0)], BLUE),
            ([(291.0, 490.0), (291.0, 422.0)], PURPLE),
            ([(311.0, 422.0), (311.0, 490.0)], PURPLE),
            ([(462.0, 324.0), (613.0, 324.0), (613.0, 390.0)], GREEN),
            ([(406.0, 556.0), (490.0, 556.0)], TEAL),
            ([(490.0, 540.0), (406.0, 540.0)], TEAL),
            ([(291.0, 654.0), (291.0, 795.0), (421.0, 795.0)], AMBER),
            ([(421.0, 779.0), (307.0, 779.0), (307.0, 654.0)], GREEN),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(
            _render_master_packet(
                [(88.0, 572.0), (178.0, 572.0), (291.0, 490.0), (291.0, 422.0), (462.0, 324.0), (613.0, 324.0), (613.0, 390.0)],
                TEAL,
                phase,
            )
        )
        return "\n".join(s for s in out if s)

    if tid == "T62":
        out.append(_render_spot_rect(275.0, 196.0, 215.0, 170.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(275.0, 445.0, 215.0, 189.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(40.0, 688.0, 685.0, 84.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(40.0, 848.0, 685.0, 72.0, PURPLE, 4, phase, rx=12.0))
        for r_pts, col in [
            ([(382.5, 368.0), (382.5, 412.0), (147.5, 412.0), (147.5, 443.0)], BLUE),
            ([(382.5, 368.0), (382.5, 443.0)], GREEN),
            ([(382.5, 412.0), (617.5, 412.0), (617.5, 443.0)], PURPLE),
            ([(191.0, 622.0), (191.0, 643.0), (382.5, 643.0)], BLUE),
            ([(382.5, 622.0), (382.5, 668.0)], GREEN),
            ([(574.0, 622.0), (574.0, 643.0), (382.5, 643.0)], AMBER),
            ([(382.5, 800.0), (382.5, 826.0)], PURPLE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(382.5, 368.0), (382.5, 443.0), (382.5, 622.0), (382.5, 668.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T63":
        out.append(_render_spot_rect(116.0, 262.0, 284.0, 260.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(415.0, 262.0, 292.0, 260.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(116.0, 536.0, 284.0, 260.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(415.0, 536.0, 292.0, 260.0, PURPLE, 4, phase, rx=12.0))
        for r_pts, col in [
            ([(407.5, 262.0), (407.5, 529.0)], BLUE),
            ([(407.5, 529.0), (407.5, 796.0)], GREEN),
            ([(116.0, 529.0), (407.5, 529.0)], AMBER),
            ([(407.5, 529.0), (707.0, 529.0)], PURPLE),
            ([(724.0, 262.0), (724.0, 878.0)], BLUE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.5, packets=1))
        out.append(_render_master_packet([(116.0, 529.0), (407.5, 529.0), (707.0, 529.0), (407.5, 529.0), (407.5, 796.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T64":
        out.append(_render_spot_rect(311.0, 164.0, 143.0, 70.0, BLUE, 1, phase, rx=10.0))
        out.append(_render_spot_rect(311.0, 384.0, 143.0, 50.0, GREEN, 2, phase, rx=10.0))
        out.append(_render_spot_rect(424.0, 606.0, 134.0, 54.0, AMBER, 3, phase, rx=10.0))
        out.append(_render_spot_rect(310.0, 870.0, 145.0, 60.0, PURPLE, 4, phase, rx=10.0))
        for r_pts, col in [
            ([(382.5, 236.0), (382.5, 256.0)], BLUE),
            ([(382.5, 356.0), (382.5, 382.0)], GREEN),
            ([(382.5, 436.0), (382.5, 454.0)], AMBER),
            ([(255.0, 566.0), (255.0, 658.0), (382.5, 658.0), (382.5, 678.0)], BLUE),
            ([(382.5, 578.0), (382.5, 658.0)], GREEN),
            ([(382.5, 730.0), (382.5, 750.0)], AMBER),
            ([(382.5, 834.0), (382.5, 846.0)], PURPLE),
            ([(103.0, 848.0), (88.0, 848.0), (88.0, 704.0), (304.0, 704.0)], RED),
            ([(744.0, 199.0), (744.0, 900.0)], BLUE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(744.0, 199.0), (744.0, 480.0), (744.0, 721.0), (744.0, 900.0)], BLUE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T65":
        out.append(_render_spot_rect(170.0, 168.0, 140.0, 54.0, BLUE, 1, phase, rx=8.0))
        out.append(_render_spot_rect(312.0, 168.0, 140.0, 54.0, GREEN, 2, phase, rx=8.0))
        out.append(_render_spot_rect(596.0, 820.0, 140.0, 92.0, AMBER, 3, phase, rx=10.0))
        out.append(_render_spot_rect(26.0, 928.0, 713.0, 64.0, PURPLE, 4, phase, rx=10.0))
        for r_pts, col in [
            ([(169.0, 168.0), (169.0, 912.0)], BLUE),
            ([(311.0, 168.0), (311.0, 912.0)], GREEN),
            ([(453.0, 168.0), (453.0, 912.0)], AMBER),
            ([(595.0, 168.0), (595.0, 912.0)], PURPLE),
            ([(746.0, 168.0), (746.0, 960.0)], GREEN),
            ([(169.0, 920.0), (738.0, 920.0)], BLUE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.5, packets=1))
        out.append(_render_master_packet([(746.0, 168.0), (746.0, 540.0), (746.0, 920.0), (169.0, 920.0)], GREEN, phase))
        return "\n".join(s for s in out if s)

    if tid == "T66":
        out.append(_render_spot_rect(82.0, 750.0, 202.0, 154.0, BLUE, 1, phase, rx=10.0))
        out.append(_render_spot_rect(82.0, 568.0, 202.0, 160.0, GREEN, 2, phase, rx=10.0))
        out.append(_render_spot_rect(82.0, 388.0, 202.0, 160.0, AMBER, 3, phase, rx=10.0))
        out.append(_render_spot_rect(82.0, 214.0, 202.0, 158.0, PURPLE, 4, phase, rx=10.0))
        for r_pts, col in [
            ([(56.0, 900.0), (56.0, 214.0)], BLUE),
            ([(286.0, 819.0), (528.0, 819.0)], BLUE),
            ([(286.0, 644.0), (518.0, 644.0)], GREEN),
            ([(286.0, 471.0), (506.0, 471.0)], AMBER),
            ([(286.0, 302.0), (498.0, 302.0)], PURPLE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(_render_master_packet([(56.0, 900.0), (56.0, 644.0), (56.0, 302.0), (498.0, 302.0)], PURPLE, phase))
        return "\n".join(s for s in out if s)

    if tid == "T67":
        out.append(_render_spot_rect(39.0, 168.0, 263.0, 118.0, BLUE, 1, phase, rx=12.0))
        out.append(_render_spot_rect(464.0, 168.0, 263.0, 118.0, GREEN, 2, phase, rx=12.0))
        out.append(_render_spot_rect(487.0, 428.0, 240.0, 125.0, AMBER, 3, phase, rx=12.0))
        out.append(_render_spot_rect(39.0, 585.0, 253.0, 118.0, PURPLE, 4, phase, rx=12.0))
        for r_pts, col in [
            ([(304.0, 227.0), (462.0, 227.0)], BLUE),
            ([(595.0, 288.0), (595.0, 394.0)], GREEN),
            ([(607.0, 555.0), (607.0, 578.0)], AMBER),
            ([(529.0, 734.0), (382.0, 734.0), (382.0, 808.0)], PURPLE),
            ([(175.0, 548.0), (175.0, 322.0)], BLUE),
        ]:
            out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4, packets=1))
        out.append(
            _render_master_packet(
                [(304.0, 227.0), (462.0, 227.0), (595.0, 288.0), (595.0, 394.0), (175.0, 548.0), (175.0, 322.0)],
                BLUE,
                phase,
            )
        )
        return "\n".join(s for s in out if s)

    # 3. Case A: Templates with explicit Draw.io mxGraph edges (T54, T01, T53, T68-T89, T79_P01-P23)
    if mx_edges:
        if tid == "T54":
            out.append(_render_spot_rect(26.0, 122.0, 1023.0, 316.0, BLUE, 1, phase, rx=16.0))
            out.append(_render_spot_rect(26.0, 458.0, 1023.0, 432.0, PURPLE, 2, phase, rx=16.0))
            out.append(_render_spot_rect(392.0, 704.0, 306.0, 154.0, GREEN, 3, phase, rx=12.0))
            out.append(_render_spot_rect(26.0, 910.0, 1023.0, 352.0, AMBER, 4, phase, rx=16.0))
        else:
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
            if all(b in mx_verts for b in ("badge_01", "badge_02", "badge_03", "badge_04")):
                for b1, b2, col in [
                    ("badge_01", "badge_02", RED),
                    ("badge_02", "badge_03", BLUE),
                    ("badge_03", "badge_04", GREEN),
                ]:
                    x1, y1, w1, h1, _ = mx_verts[b1]
                    x2, y2, w2, _h2, _ = mx_verts[b2]
                    out.append(
                        _conduit_pulse(
                            [(x1 + w1 / 2.0, y1 + h1 + 2.0), (x2 + w2 / 2.0, y2 - 2.0)],
                            col,
                            phase,
                            forbidden_boxes,
                            dur=1.4,
                            packets=1,
                        )
                    )

        master_pts: List[Point] = []
        for idx, (cid, _src, tgt, pts, _st) in enumerate(mx_edges):
            if cid.startswith("t4_m") or cid == "spine_line":
                continue
            ymid = sum(p[1] for p in pts) / len(pts)
            if tid == "T54":
                col = BLUE if ymid < 450.0 else (PURPLE if ymid < 865.0 else (GREEN if "yes" in cid or "dec" in tgt else AMBER))
            else:
                col = RED if ymid < 300.0 else (BLUE if ymid < 520.0 else (GREEN if "yes1" in cid or "loop" in cid or "map" in cid else AMBER))
            out.append(_conduit_pulse(pts, col, phase, forbidden_boxes, dur=1.35 + (idx % 3) * 0.15, packets=1))
            if tid == "T54" and cid in ("e53_1a", "e53_p2q", "e53_q1_yes", "e53_q2_yes", "e53_m_C", "e53_b_no", "e53_af", "e53_recheck"):
                master_pts.extend(pts)
            elif tid != "T54" and cid in ("t1_edge_1", "t1_edge_2", "t2_edge_calls", "t2_edge_checks", "t3_e1", "t3_e2", "t3_e_yes1", "t4_edge_maps"):
                master_pts.extend(pts)

        if len(master_pts) >= 2:
            out.append(_render_master_packet(master_pts[:10], BLUE, phase, dur=4.8))
        return "\n".join(s for s in out if s)

    # 4. Case B: Sculptural Architecture Posters (T90-T209, 920x1150)
    stage_nodes: List[Tuple[float, float, float, float, str]] = []
    for cid, (vx, vy, vw, vh, _) in sorted(mx_verts.items(), key=lambda kv: (round(kv[1][1] / 95.0), kv[1][0])):
        if cid.startswith(("bg", "poster_bg", "hdr", "brand", "ftr", "an_bad", "an_good")):
            continue
        if 195.0 <= vy <= ch - 95.0 and 48.0 <= vw <= cw - 40.0 and 24.0 <= vh <= 420.0:
            kind = "circle" if abs(vw - vh) <= 6.0 and vw <= 125.0 else "rect"
            stage_nodes.append((vx, vy, vw, vh, kind))

    for cx, cy, r in sorted(bg_circles, key=lambda c: (round(c[1] / 90.0), c[0])):
        if r >= 26.0 and 330.0 <= cy <= 780.0:
            stage_nodes.append((cx - r, cy - r, 2.0 * r, 2.0 * r, "circle"))

    if len(stage_nodes) >= 4:
        idxs = [
            0,
            1 if len(stage_nodes) > 2 else 0,
            max(2, len(stage_nodes) // 2),
            len(stage_nodes) - 1,
        ]
        seen_idx = set()
        phase_num = 1
        for i in idxs:
            if i in seen_idx or phase_num > 4:
                continue
            seen_idx.add(i)
            nx, ny, nw, nh, kind = stage_nodes[i]
            col = phase_colors[(phase_num - 1) % 4]
            if kind == "circle":
                out.append(_render_spot_circle(nx + nw / 2.0, ny + nh / 2.0, nw / 2.0, col, phase_num, phase))
            else:
                out.append(_render_spot_rect(nx, ny, nw, nh, col, phase_num, phase, rx=12.0))
            phase_num += 1

    # Gutter-only conduits: top Bad->Good bridge, clipped stage lines, left/right margin bus, and bottom outcome gutter bridges
    sculptural_routes: List[Tuple[List[Point], str]] = [
        ([(450.0, 163.0), (462.0, 163.0)], GREEN),
        ([(18.0, 272.0), (18.0, 848.0)], BLUE),
        ([(902.0, 272.0), (902.0, 848.0)], GREEN),
        ([(163.0, 914.0), (163.0, 980.0)], BLUE),
        ([(460.0, 914.0), (460.0, 980.0)], GREEN),
        ([(757.0, 914.0), (757.0, 980.0)], AMBER),
    ]
    for idx, seg in enumerate(bg_lines[:8]):
        sculptural_routes.append((seg, phase_colors[idx % len(phase_colors)]))

    for idx, (r_pts, col) in enumerate(sculptural_routes):
        out.append(_conduit_pulse(r_pts, col, phase, forbidden_boxes, dur=1.4 + (idx % 3) * 0.15, packets=1))

    out.append(
        _render_master_packet(
            [(18.0, 272.0), (18.0, 560.0), (18.0, 848.0), (18.0, 948.0), (902.0, 948.0), (902.0, 560.0), (902.0, 272.0)],
            accent or BLUE,
            phase,
            dur=4.8,
        )
    )
    return "\n".join(s for s in out if s)


def render_template(tid: str, spec: Optional[Dict[str, Any]] = None, phase: Optional[float] = None) -> str:
    """Render any certified gallery template (`128`) or preserved `T79` topic post (`23`) into a Zero-Origin W3C SVG."""
    if tid not in TEMPLATE_META and tid not in TOPIC_POST_IDS:
        raise KeyError(f"Unknown or purged template ID: {tid}")
    if tid in GENERATIVE_GRAMMAR_TEMPLATE_META:
        return synthesize_generative_template_svg({"tid": tid, **(spec or {})}, phase=phase)
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
    """Return the ordered list of 128 Certified Unique Visual Templates (`84 Best` + `44 High`)."""
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
