"""Template Gallery v4 — 16 PromptCanvas Canonical Infographic Diagrams (T53-T68).

Renders all 16 Infographic Blueprints directly from the canonical PromptCanvas source assets
(`src/lib/canonical/infographicBlueprints52to66.ts` #52-#66 and `src/lib/canonical/openKnowledgeInfographic.ts`,
exported via `viewer-static.min.js` at 2x Retina into `assets/canonical-ref/canonical_T53.png..canonical_T68.png`
per Rule 57B — zero hand-rolled SVG box-approximation fallbacks):

  T53 (PromptCanvas #52) — Infographic: Anatomy / Deconstruction (4-Tier Spine: Context + Harness + Loop + Graph)
  T54 (PromptCanvas #53) — Infographic: Process Workflow (Primary Coding Agent + Reviewer Agent)
  T55 (PromptCanvas #54) — Infographic: Cheat Sheet Quick-Start Card (Autonomous Agent Computer Use)
  T56 (PromptCanvas #55) — Infographic: Bubble Conceptual (The AI Nobody Signed Off — Shadow AI vs. Governed AI)
  T57 (PromptCanvas #56) — Infographic: Side-by-Side Comparison (Raw Model API vs. Enterprise Agent Runtime)
  T58 (PromptCanvas #57) — Infographic: Funnel Pipeline Chart (5-Stage Context Compression 1M -> 2k Tokens)
  T59 (PromptCanvas #58) — Infographic: Process Checklist (6-Step Autonomous Agent Deployment with ON Switches)
  T60 (PromptCanvas #59) — Infographic: Timeline & Roadmap (Phased Quarterly Blueprint Q1-Q4 Horizontal Tracks)
  T61 (PromptCanvas #60) — Infographic: Architecture & Topology (Enterprise Agent Runtimes: Vertex, Cloud Run, GKE, AlloyDB)
  T62 (PromptCanvas #61) — Infographic: Hierarchical Tree (Multi-Agent Supervisor Delegation 01 -> 02a/02b/02c -> 03)
  T63 (PromptCanvas #62) — Infographic: 2x2 Quadrant Matrix (Business Impact vs. Technical Complexity)
  T64 (PromptCanvas #63) — Infographic: Decision Tree Flowchart (Conditional Branching Logic: Ingest / Tool Check / Execute)
  T65 (PromptCanvas #64) — Infographic: Feature Matrix Grid (5x4 Multi-Criteria Architectural Evaluation & Scoring)
  T66 (PromptCanvas #65) — Infographic: Capability Pyramid (4-Tier AI Capability Evolution: Base -> Tools -> Multi-Agent -> Apex)
  T67 (PromptCanvas #66) — Infographic: Loop & Cycle (Circular 4-Stage Autonomous Self-Healing Agent Loop)
  T68 (PromptCanvas Open Knowledge) — Infographic: Open Knowledge Format Architecture (Formats + Schema + Validation + Graph)
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

from src.visuals.template_gallery import (
    BLUE, CSS, GREEN, NAVY, PURPLE, RED, TEAL,
    _esc, _flow, register_templates,
)

Point = Tuple[float, float]

_CANONICAL_REF_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "canonical-ref"
_B64_CACHE: Dict[str, Tuple[int, int, int, str, str]] = {}


def _load_canonical_pc_asset(tid: str) -> Tuple[int, int, str, str]:
    """Fail-closed canonical PromptCanvas asset loader with mtime cache invalidation (Rule 57B)."""
    png_path = _CANONICAL_REF_DIR / f"canonical_{tid}.png"
    dims_path = _CANONICAL_REF_DIR / "canonical_dimensions.json"
    if not png_path.exists():
        raise FileNotFoundError(
            f"[Rule 57B Violation] Missing canonical PromptCanvas asset {png_path}. "
            "Run `node scripts/sync_canonical_promptcanvas_infographics.mjs` first."
        )
    mtime_ns = png_path.stat().st_mtime_ns
    cached = _B64_CACHE.get(tid)
    if cached is not None and cached[0] == mtime_ns:
        return cached[1], cached[2], cached[3], cached[4]
    cw, ch, bg = 1020, 1040, "#F8FAFC"
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


def _fl(
    pts: Sequence[Point],
    col: str,
    phase: Optional[float],
    dur: float = 1.6,
    label: Optional[str] = None,
    dash: str = "8 5",
    packets: int = 1,
    label_dy: float = 0.0,
    label_at: float = 0.5,
    solid: bool = False,
) -> str:
    return _flow(
        pts, col, phase, label, dur, 2.6, True, packets,
        dash=dash, track=True, label_dy=label_dy, label_at=label_at, solid=solid,
    )


def _render_canonical_pc(tid: str, s: Dict[str, Any], phase: Optional[float] = None) -> str:
    cw, ch, _bg, b64 = _load_canonical_pc_asset(tid)
    meta = META_V4.get(tid, {})
    accent = meta.get("accent", BLUE)
    lineage = s.get("lineage") or meta.get("lineage") or "PromptCanvas Canonical Infographic"
    source_note = str(s.get("source") or meta.get("inspired_by") or "Google Cloud Vertex AI + OpenHands").replace(" GCP ", " Google Cloud ")
    if not any(m in source_note for m in ("LangGraph", "OpenHands", "vLLM", "PostgreSQL", "OpenTelemetry", "Llama Guard", "Temporal", "Promptfoo", "MCP", "Knative", "pgvector", "Redis", "Qdrant", "LiteLLM")):
        source_note = f"{source_note} • OpenHands + LangGraph + pgvector"
    if not any(m in source_note for m in ("Google", "Vertex", "Gemini", "Firestore", "Cloud Run", "ADK", "Model Armor", "BigQuery", "AlloyDB", "Cloud Trace")):
        source_note = f"{source_note} • Google Cloud Vertex AI"
    total_h = ch
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {total_h}" width="{cw}" height="{total_h}">',
        f"<title>{_esc(f'{tid} • FORMAT LINEAGE: {lineage} • Proprietary + Confidential')}</title>",
        f"<desc>{_esc(source_note)}</desc>",
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
        f'<rect x="0" y="0" width="{cw}" height="{total_h}" fill="#F8FAFC"/>',
        f'<rect x="0" y="0" width="{cw}" height="{total_h}" fill="url(#archGrid)"/>',
        f'<image x="0" y="0" width="{cw}" height="{ch}" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{b64}"/>',
        _fl([(20.0, 2.0), (float(cw - 20), 2.0)], accent, phase, 2.4, packets=3),
        "</svg>",
    ]
    return "\n".join(parts)


# ----------------------------------------------------------------------------------------------------------------------
# Metadata & Grounded Demo Specs for T53-T68
# ----------------------------------------------------------------------------------------------------------------------
META_V4: Dict[str, Dict[str, Any]] = {
    "T53": {
        "name": "PromptCanvas #52: Anatomy / Deconstruction Spine",
        "best_for_short": "Context + Harness + Loop + Graph 4-tier spine",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Educational", "Working solution"],
        "when_to_use": "Deconstruct a self-improving AI agent setup across 01 Context, 02 Harness (AGENTS.md & Skills), 03 Loop (Check/Fix/Recheck), and 04 Graph (MAP.md).",
        "dynamic": "Packets travel down the 4-tier central spine and across left-to-right verification enclaves with RULE 01-04 bars.",
        "lineage": "PromptCanvas Blueprint #52 (Anatomy / Deconstruction Infographic) • Keith R. Worfolk & Philipp Schmid",
        "category": "PromptCanvas Infographic",
        "best_for": "4-part structural breakdown of a self-improving AI agent setup (Context, Harness, Loop, Graph) with RULE bars",
        "inspired_by": "PromptCanvas Blueprint #52 (Anatomy / Deconstruction Infographic) • Keith R. Worfolk & Philipp Schmid",
        "accent": BLUE,
        "hot_topic": "Anatomy of a Production Coding Agent: Context + Harness + Loop + Graph",
    },
    "T54": {
        "name": "PromptCanvas #53: Dual-Agent Process Workflow",
        "best_for_short": "Primary Coding Agent + Reviewer Agent loop",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Educational", "Proof of concept"],
        "when_to_use": "Show a 3-band workflow pairing a Primary Coding Agent with an independent Reviewer Agent across Install, Tool Mounting (YES/NO gate), and Recheck.",
        "dynamic": "Packets flow across all 3 horizontal bands, the YES/NO tool readiness diamond, and the bottom RECHECK feedback loop.",
        "lineage": "PromptCanvas Blueprint #53 (Process Workflow Infographic) • Gemini Code Assist + OpenHands / Codex",
        "category": "PromptCanvas Infographic",
        "best_for": "3-band step-by-step workflow pairing a Primary Coding Agent with an independent Reviewer Agent and YES/NO tool gates",
        "inspired_by": "PromptCanvas Blueprint #53 (Process Workflow Infographic) • Gemini Code Assist + OpenHands / Codex",
        "accent": PURPLE,
        "hot_topic": "Dual-Agent Coding Workflow: Primary Builder + Adversarial Reviewer Loop",
    },
    "T55": {
        "name": "PromptCanvas #54: Computer-Use Cheat Sheet Card",
        "best_for_short": "7 setup steps + 4 copy-ready @Browser jobs",
        "content_types": ["PromptCanvas Infographic", "Easy to understand", "Educational", "Working solution"],
        "when_to_use": "Provide a 2-column executive quick-start card with 7 setup steps, a copy-paste prompt formula, and 4 high-ROI browser/computer-use workflows.",
        "dynamic": "Animated conduit connects the 7-step setup checklist and prompt formula to the 2x2 grid of production @Browser jobs.",
        "lineage": "PromptCanvas Blueprint #54 (Cheat Sheet Quick-Start Card) • Vertex Computer Use & OpenHands Browser",
        "category": "PromptCanvas Infographic",
        "best_for": "2-column quick-start cheat sheet with 7 setup steps, copy-paste prompt formula, and 4 high-ROI browser/computer-use jobs",
        "inspired_by": "PromptCanvas Blueprint #54 (Cheat Sheet Quick-Start Card) • Vertex Computer Use & OpenHands Browser",
        "accent": BLUE,
        "hot_topic": "Autonomous Computer-Use Cheat Sheet: 7 Setup Steps & 4 Production Prompts",
    },
    "T56": {
        "name": "PromptCanvas #55: Shadow AI Bubble Conceptual",
        "best_for_short": "4 perceived tools vs. 24 shadow AI pipelines",
        "content_types": ["PromptCanvas Infographic", "Professional knowledge sharing", "Ideas", "Information"],
        "when_to_use": "Contrast what leadership thinks is running (4 approved tools) against 24 shadow AI tools across engineering, meetings, sales, and legal.",
        "dynamic": "Blind-spot conduit links the 4 executive assumption cards to 24 color-coded shadow AI bubbles and the 4-control governance bridge.",
        "lineage": "PromptCanvas Blueprint #55 (Bubble Conceptual Infographic) • Enterprise Shadow AI & Model Armor Gateway",
        "category": "PromptCanvas Infographic",
        "best_for": "Contrasting executive perception (4 approved tools) against 24 shadow AI tools running across engineering, sales, and ops",
        "inspired_by": "PromptCanvas Blueprint #55 (Bubble Conceptual Infographic) • Enterprise Shadow AI & Model Armor Gateway",
        "accent": RED,
        "hot_topic": "The AI Nobody Signed Off: Governing 24 Shadow AI Tools via an AI Gateway",
    },
    "T57": {
        "name": "PromptCanvas #56: Side-by-Side Runtime Toggles",
        "best_for_short": "Stateless API (OFF) vs. Agent Runtime (ON)",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Evaluation results", "Professional knowledge sharing"],
        "when_to_use": "Compare stateless foundation model inference (OFF toggles) against a managed enterprise agent runtime (ON toggles) across 5 architecture pillars.",
        "dynamic": "5 parallel upgrade conduits flow from red OFF stateless cards through the central dimension spine to green ON managed runtime cards.",
        "lineage": "PromptCanvas Blueprint #56 (Side-by-Side Comparison Infographic) • Vertex AI Agent Engine vs. Raw API",
        "category": "PromptCanvas Infographic",
        "best_for": "5-row central-spine comparison with OFF vs. ON vector toggle switches comparing stateless APIs against managed runtimes",
        "inspired_by": "PromptCanvas Blueprint #56 (Side-by-Side Comparison Infographic) • Vertex AI Agent Engine vs. Raw API",
        "accent": GREEN,
        "hot_topic": "Stateless LLM API (OFF) vs. Managed Enterprise Agent Runtime (ON)",
    },
    "T58": {
        "name": "PromptCanvas #57: 3D Context Compression Funnel",
        "best_for_short": "5-stage token refinement: 1M -> 2k tokens",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Evaluation results", "Research topics"],
        "when_to_use": "Visualize progressive token refinement across 5 tapering 3D-frustum funnel stages from 1,000,000 raw tokens down to 2,000 precision context tokens.",
        "dynamic": "3 glowing signal packets stream down the 5-stage 3D frustum funnel while side conduits link stage architectures to discard gates.",
        "lineage": "PromptCanvas Blueprint #57 (Funnel Pipeline Chart) • BigQuery Vector Search & Cross-Encoder Re-Ranking",
        "category": "PromptCanvas Infographic",
        "best_for": "5-stage 3D-frustum tapering vector funnel showing progressive token refinement from 1M raw tokens to 2k precision context",
        "inspired_by": "PromptCanvas Blueprint #57 (Funnel Pipeline Chart) • BigQuery Vector Search & Cross-Encoder Re-Ranking",
        "accent": BLUE,
        "hot_topic": "Progressive Context Compression Funnel: 1,000,000 -> 2,000 High-Signal Tokens",
    },
    "T59": {
        "name": "PromptCanvas #58: 6-Gate Deployment Checklist",
        "best_for_short": "6-step autonomous agent prod checklist (ON)",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Professional knowledge sharing", "Proof of concept"],
        "when_to_use": "Present a 6-row numbered production deployment checklist with status badges, monospace config specs, and double green ON toggle switches.",
        "dynamic": "Vertical deployment spine feeds 6 numbered checklist rows, each equipped with verified config boxes and dual ON switches.",
        "lineage": "PromptCanvas Blueprint #58 (Process Checklist Infographic) • Google Cloud GKE gVisor & AlloyDB",
        "category": "PromptCanvas Infographic",
        "best_for": "6-step numbered production deployment checklist with status badges, monospace config specs, and double ON toggle switches",
        "inspired_by": "PromptCanvas Blueprint #58 (Process Checklist Infographic) • Google Cloud GKE gVisor & AlloyDB",
        "accent": GREEN,
        "hot_topic": "6-Step Autonomous Agent Production Deployment Checklist",
    },
    "T60": {
        "name": "PromptCanvas #59: Q1-Q4 Quarterly Roadmap Tracks",
        "best_for_short": "Phased Q1-Q4 enterprise agent rollout plan",
        "content_types": ["PromptCanvas Infographic", "Professional knowledge sharing", "Ideas", "Information"],
        "when_to_use": "Lay out a 4-quarter enterprise rollout roadmap (Q1 Discovery -> Q2 Sandbox -> Q3 State -> Q4 Fleet) with 8 numbered milestones and ACTIVE toggles.",
        "dynamic": "Horizontal flow conduits advance across Q1-Q4 chevron headers and milestone deliverables 01-08.",
        "lineage": "PromptCanvas Blueprint #59 (Timeline & Roadmap Infographic) • Enterprise Agentic AI Rollout Plan",
        "category": "PromptCanvas Infographic",
        "best_for": "4 horizontal quarterly roadmap tracks (Q1-Q4) with chevron headers, ACTIVE switches, and 8 numbered milestone deliverables",
        "inspired_by": "PromptCanvas Blueprint #59 (Timeline & Roadmap Infographic) • Enterprise Agentic AI Rollout Plan",
        "accent": BLUE,
        "hot_topic": "Phased Q1-Q4 Enterprise Agentic AI Architecture Roadmap",
    },
    "T61": {
        "name": "PromptCanvas #60: 4-Plane Runtime Topology",
        "best_for_short": "Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Grounded concepts", "Educational"],
        "when_to_use": "Show the 4-node enterprise runtime topology separating reasoning (Vertex AI), orchestration (Cloud Run), sandbox (GKE gVisor), and state (AlloyDB).",
        "dynamic": "Bidirectional gRPC, MCP, CodeAct, and vector state packets flow between Load Balancing ingress and the 4 runtime planes.",
        "lineage": "PromptCanvas Blueprint #60 (Architecture & Topology Infographic) • Google Cloud Agent Reference Topology",
        "category": "PromptCanvas Infographic",
        "best_for": "4-node interconnected runtime topology linking Cloud Load Balancing, Vertex Reasoning Engine, Cloud Run, GKE gVisor, and AlloyDB",
        "inspired_by": "PromptCanvas Blueprint #60 (Architecture & Topology Infographic) • Google Cloud Agent Reference Topology",
        "accent": TEAL,
        "hot_topic": "Enterprise Agent Runtime Topology: Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
    },
    "T62": {
        "name": "PromptCanvas #61: Multi-Agent Supervisor Tree",
        "best_for_short": "Supervisor (01) -> Workers (02a-c) -> Data (03)",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Working solution", "Educational"],
        "when_to_use": "Illustrate a 3-tier hierarchical delegation tree from Supervisor Agent (01) to 3 Specialized Worker Agents (02a/02b/02c) to Shared Resources (03).",
        "dynamic": "A2A task packets fan out from the Supervisor to SQL, Research, and Code workers and down into BigQuery, Vector Search, and gVisor.",
        "lineage": "PromptCanvas Blueprint #61 (Hierarchical Tree Infographic) • Google ADK & LangGraph Supervisor Pattern",
        "category": "PromptCanvas Infographic",
        "best_for": "3-tier delegation tree from Supervisor Agent (01) to Specialized Worker Agents (02a/02b/02c) to Unified Resource Layer (03)",
        "inspired_by": "PromptCanvas Blueprint #61 (Hierarchical Tree Infographic) • Google ADK & LangGraph Supervisor Pattern",
        "accent": PURPLE,
        "hot_topic": "3-Tier Multi-Agent Supervisor Delegation Tree & Shared Resource Plane",
    },
    "T63": {
        "name": "PromptCanvas #62: 2x2 Impact vs. Complexity Matrix",
        "best_for_short": "20 use cases across Quick Wins, Bets & Traps",
        "content_types": ["PromptCanvas Infographic", "Professional knowledge sharing", "Easy to understand", "Ideas"],
        "when_to_use": "Prioritize 20 concrete agent use cases across a 2x2 matrix of Business Impact vs. Technical Complexity (Quick Wins, Strategic Bets, Low Priority, Traps).",
        "dynamic": "4 color-coded quadrants with 20 numbered use-case cards, ROI metrics, and recommended Google Cloud + OSS stacks.",
        "lineage": "PromptCanvas Blueprint #62 (2x2 Quadrant Matrix Infographic) • AI Portfolio Prioritization",
        "category": "PromptCanvas Infographic",
        "best_for": "4-quadrant executive prioritization matrix mapping 20 concrete agent use-cases across Quick Wins, Strategic Bets, Low Priority, and Traps",
        "inspired_by": "PromptCanvas Blueprint #62 (2x2 Quadrant Matrix Infographic) • AI Portfolio Prioritization",
        "accent": GREEN,
        "hot_topic": "Agentic AI Portfolio 2x2 Matrix: Quick Wins vs. Strategic Bets vs. Traps",
    },
    "T64": {
        "name": "PromptCanvas #63: Conditional Decision Tree",
        "best_for_short": "3-stage YES/NO branching & self-correction",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Educational", "Grounded concepts"],
        "when_to_use": "Map deterministic YES/NO branching logic across Stage 01 Ingest, Stage 02 Tool & RBAC Check, and Stage 03 Sandboxed Execution & Self-Correction.",
        "dynamic": "Packets traverse 4 decision diamonds with YES/NO branches and an animated self-correction retry loop in Stage 03.",
        "lineage": "PromptCanvas Blueprint #63 (Decision Tree Flowchart) • Deterministic Agent Routing & Self-Correction",
        "category": "PromptCanvas Infographic",
        "best_for": "3-stage conditional decision tree across Ingest, Tool/RBAC Check, and Sandboxed Execution with YES/NO diamonds and retry loops",
        "inspired_by": "PromptCanvas Blueprint #63 (Decision Tree Flowchart) • Deterministic Agent Routing & Self-Correction",
        "accent": BLUE,
        "hot_topic": "Deterministic Agent Decision Tree: Intent Gate -> RBAC Check -> Sandbox Loop",
    },
    "T65": {
        "name": "PromptCanvas #64: 5x4 Feature Evaluation Matrix",
        "best_for_short": "Score 4 agent stacks across 5 prod criteria",
        "content_types": ["PromptCanvas Infographic", "Evaluation results", "Professional knowledge sharing", "Grounded concepts"],
        "when_to_use": "Evaluate 4 agent architectures (Google ADK + Vertex, LangGraph + Postgres, OpenHands + Docker, Raw API) across 5 weighted production criteria.",
        "dynamic": "5x4 matrix of NATIVE / CONFIG / MANUAL capability badges plus animated overall architectural fit score bars (4.9/5 to 1.8/5).",
        "lineage": "PromptCanvas Blueprint #64 (Feature Matrix Grid) • Google ADK vs. LangGraph vs. OpenHands vs. Raw API",
        "category": "PromptCanvas Infographic",
        "best_for": "5x4 multi-criteria evaluation matrix scoring 4 agent stacks across persistence, isolation, HITL, memory, and scale",
        "inspired_by": "PromptCanvas Blueprint #64 (Feature Matrix Grid) • Google ADK vs. LangGraph vs. OpenHands vs. Raw API",
        "accent": NAVY,
        "hot_topic": "5x4 Agent Stack Evaluation Matrix: Persistence, Isolation, HITL, Memory & Scale",
    },
    "T66": {
        "name": "PromptCanvas #65: 4-Tier Capability Pyramid",
        "best_for_short": "Raw Inference -> Tools -> Multi-Agent -> Apex",
        "content_types": ["PromptCanvas Infographic", "Educational", "Grounded concepts", "Professional knowledge sharing"],
        "when_to_use": "Show the 4-tier evolution of AI systems from Base Foundation Model (01) to Tool Calling (02) to Multi-Agent (03) to Autonomous Self-Healing Apex (04).",
        "dynamic": "Upward evolution spine climbs the 4-tier 3D trapezoid pyramid while side conduits link tier definitions to Google Cloud + OSS capabilities.",
        "lineage": "PromptCanvas Blueprint #65 (Capability Pyramid Infographic) • Google Cloud Agent Evolution Tiers",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier ascending capability pyramid from Base Foundation Model (01) to Tool Calling (02) to Multi-Agent (03) to Autonomous Apex (04)",
        "inspired_by": "PromptCanvas Blueprint #65 (Capability Pyramid Infographic) • Google Cloud Agent Evolution Tiers",
        "accent": GREEN,
        "hot_topic": "The 4-Tier Agent Capability Pyramid: Raw Inference -> Tools -> Multi-Agent -> Autonomous",
    },
    "T67": {
        "name": "PromptCanvas #66: Self-Healing Torus Loop",
        "best_for_short": "4-stage circular autonomous repair cycle",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Grounded concepts", "Proof of concept"],
        "when_to_use": "Visualize the circular 4-stage autonomous agent loop (01 Generate -> 02 Sandbox Test -> 03 Eval Gate -> 04 Self-Healing Retry or PASS Deploy).",
        "dynamic": "Packets orbit the 4-quadrant central torus ring, branching on FAIL to the RETRY ACTIVE feedback path or on PASS to DEPLOY ON.",
        "lineage": "PromptCanvas Blueprint #66 (Loop & Cycle Infographic) • Autonomous Self-Healing Evaluation Cycle",
        "category": "PromptCanvas Infographic",
        "best_for": "Circular 4-quadrant torus loop connecting Model Generation, Sandboxed Test, Evaluation Gate (PASS/FAIL), and Self-Healing Retry",
        "inspired_by": "PromptCanvas Blueprint #66 (Loop & Cycle Infographic) • Autonomous Self-Healing Evaluation Cycle",
        "accent": BLUE,
        "hot_topic": "Autonomous Self-Healing Agent Loop: Generate -> Sandbox Test -> Gate -> Repair",
    },
    "T68": {
        "name": "PromptCanvas Open Knowledge: 4-Tier Format Spine",
        "best_for_short": "Open Formats + Schema + Validation + Graph",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Research topics", "Working solution"],
        "when_to_use": "Explain why agent knowledge should live in Open Formats (01), validated by a Schema Harness (02), healed by a Validation Loop (03), and linked in a Graph (04).",
        "dynamic": "Packets flow down the 4-tier Open Knowledge vertical spine and across format/schema/validator/graph hubs with RULE 01-04 bars.",
        "lineage": "PromptCanvas Open Knowledge Spine • LangChain OpenWiki",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier vertical spine illustrating Open Formats (01), Schema Harness (02), Validation Loop (03), and Knowledge Graph (04)",
        "inspired_by": "PromptCanvas Open Knowledge Format Infographic • LangChain OpenWiki & Deterministic Knowledge Graphs",
        "accent": TEAL,
        "hot_topic": "Open Knowledge Architecture: Formats + Schema Harness + Validation Loop + Graph",
    },
    "T69": {
        "name": "Harness² Recursive Agent Harnessing Spine",
        "best_for_short": "Static Trap + Dynamic Synthesis + Critic Loop + +22pp Gain",
        "content_types": ["PromptCanvas Infographic", "Research topics", "Grounded concepts", "Evaluation results"],
        "when_to_use": "Deconstruct Google's Harness² paper (arXiv:2604.08523): why static hand-built harnesses fail in open worlds and how recursive meta-harness synthesis adds +22pp on NoveltyBench.",
        "dynamic": "Packets traverse the 4-tier recursive Harness² spine from open-world task distribution shift to dynamic tool synthesis, verification loop, and +22pp benchmark gains.",
        "lineage": "Google Harness² (arXiv:2604.08523) • Aishwarya Naresh Reganti",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier recursive agent harness breakdown (Static Trap, Dynamic Synthesis, Verification Loop, +22pp Benchmark Gains)",
        "inspired_by": "Google Harness² Paper (arXiv:2604.08523) • Aishwarya Naresh Reganti • Vertex AI ADK + OpenHands",
        "accent": BLUE,
        "hot_topic": "Harness²: Recursive Agent Harnessing for an Open World (+22pp NoveltyBench)",
    },
    "T70": {
        "name": "5 Open-Source Agent Repos Stack Spine",
        "best_for_short": "gstack + Paperclip + agency-agents + rowboat + multica",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Professional knowledge sharing", "Easy to understand"],
        "when_to_use": "Map the 5 open-source agent repositories (gstack, Paperclip, agency-agents, rowboat, multica) across Role Skills, Org Orchestration, Memory Graph, and CI/CD Coding.",
        "dynamic": "Packets flow across the 5-repo architectural spine from Garry Tan's 23 gstack role skills to Paperclip + agency-agents orchestration, rowboat graph memory, and multica CI/CD.",
        "lineage": "5 Agent Repos Stack • Vaibhav Sisinty (112K+ Combined GitHub Stars)",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier open-source agent repository stack covering role skills, multi-agent orgs, persistent memory graphs, and CI/CD coding",
        "inspired_by": "Vaibhav Sisinty • gstack + Paperclip + agency-agents + rowboat + multica • Google Cloud ADK + OpenHands",
        "accent": PURPLE,
        "hot_topic": "The 5-Repo Agent Engineering Stack: Skills, Orchestration, Memory & CI/CD",
    },
    "T71": {
        "name": "3-Track Data Modeling & Medallion Map Spine",
        "best_for_short": "Design Track + Meaning Track + Consumption Track + 3x3 Matrix",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Educational", "Professional knowledge sharing"],
        "when_to_use": "Align data architecture across Track 1 Design (Conceptual/Logical/Physical -> Bronze/Silver/Gold), Track 2 Meaning (Glossary/Ontology/Knowledge Graph), and Track 3 Consumption (Semantic Layer).",
        "dynamic": "Packets flow from Conceptual/Logical/Physical Medallion design into Domain Ontology grounding, Semantic Layer KPI validation, and the 3x3 Data Modeling Matrix.",
        "lineage": "The Data Modeling Map: 3 Questions, 3 Tracks • Nan Li",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier data modeling and Medallion architecture spine uniting physical schema design, semantic ontology, and governed consumption",
        "inspired_by": "Nan Li • 3-Track Data Modeling Map • Google Cloud BigQuery + Dataplex + dbt / Looker + pgvector",
        "accent": TEAL,
        "hot_topic": "The Data Modeling Map: Design, Meaning & Semantic Consumption Tracks",
    },
    "T72": {
        "name": "TokenEconomizer Black-Box Cost Controller Spine",
        "best_for_short": "Trace Loop + Micro-Skills + Tool Pruning + SWE-Bench (-30.9%)",
        "content_types": ["PromptCanvas Infographic", "Evaluation results", "Research topics", "Working solution"],
        "when_to_use": "Show how UC Berkeley & Microsoft's TokenEconomizer cuts coding agent cost by 18.4%-30.9% across 30/30 SWE-Bench Verified configs via micro-skills, tool pruning (23->3), and loop intervention.",
        "dynamic": "Packets circulate through the closed-loop trace analyzer, pre-task schema pruner, 3-turn stall breaker, and SWE-Bench Verified cost/solve-rate scoreboard.",
        "lineage": "UC Berkeley & Microsoft TokenEconomizer • Alena Panshina",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier black-box coding agent cost controller combining trace analysis, 3-line micro-skills, schema pruning, and loop intervention",
        "inspired_by": "Alena Panshina • UC Berkeley & Microsoft TokenEconomizer • Vertex AI Gemini + OpenHands",
        "accent": GREEN,
        "hot_topic": "TokenEconomizer: Experience-Driven Black-Box Coding Agent Cost Control (-30.9%)",
    },
    "T73": {
        "name": "11-Zone Production Agentic AI Reference Spine",
        "best_for_short": "Perimeter + AgentCore Gateway + Approval Gate + AgentOps",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Grounded concepts", "Professional knowledge sharing"],
        "when_to_use": "Architect an 11-zone production enterprise agent covering Perimeter & Channels (Zones 1-2), Supervisor Runtime (3, 9, 10), AgentCore Gateway + RAG (4, 6, 7), Approval Gate (5), and AgentOps (8, 11).",
        "dynamic": "Packets traverse zero-trust ingress, OAuth identity-propagating AgentCore Gateway, risk-tiered HITL approval gates, and OpenTelemetry AgentOps observability.",
        "lineage": "11-Zone Production Agentic AI Reference Architecture • Rajesh Kumar",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier synthesis of the 11-zone enterprise agent reference architecture with identity propagation, risk-tiered approvals, and AgentOps",
        "inspired_by": "Rajesh Kumar • 11-Zone Production Agentic AI Architecture • Google Cloud GKE + Apigee + LangGraph",
        "accent": BLUE,
        "hot_topic": "11-Zone Production Agentic AI Reference Architecture: Gateway, Approvals & AgentOps",
    },
    "T74": {
        "name": "6-Vendor AI Agent Sandbox Isolation Spine",
        "best_for_short": "Kernel Isolation + Secret Proxy + Sandbox Loop + 6-Vendor Matrix",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Evaluation results", "Working solution"],
        "when_to_use": "Compare how Google (GKE Agent Sandbox gVisor), AWS (Bedrock AgentCore + Strands), Microsoft (Windows Agent Workspace), NVIDIA (OpenShell DPU), Perplexity (SPACE), and OpenAI isolate agent code.",
        "dynamic": "Packets flow through microVM kernel isolation, externalized secret broker injection, syscall/egress interception loops, and the 6-vendor sandbox comparison matrix.",
        "lineage": "The AI Agent Sandbox Landscape (6 Vendors) • Rakesh Gohel",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier security architecture comparing kernel isolation, externalized credential proxies, syscall loops, and 6 cloud/AI sandbox stacks",
        "inspired_by": "Rakesh Gohel • 6-Vendor AI Agent Sandbox Landscape • Google Cloud GKE gVisor + OpenHands",
        "accent": RED,
        "hot_topic": "The AI Agent Sandbox Landscape: How Google, AWS, MSFT & NVIDIA Isolate Agent Code",
    },
    "T75": {
        "name": "Anatomy of an AI Agent: 5 Building Blocks Spine",
        "best_for_short": "Brain (LLM) + Library (RAG) + Nerves (MCP) + Memory (Skills) + Hands",
        "content_types": ["PromptCanvas Infographic", "Easy to understand", "Educational", "Grounded concepts"],
        "when_to_use": "Explain the 5 building blocks of a modern AI agent using crisp human-body analogies: 1. LLM = Brain, 2. RAG = Library, 3. MCP = Nervous System, 4. Skills = Muscle Memory, 5. Agent = Brain + Hands.",
        "dynamic": "Packets connect the reasoning LLM Brain and RAG Library through the MCP Nervous System and SKILL.md Muscle Memory into self-verifying Agent Hands.",
        "lineage": "Anatomy of an AI Agent: 5 Building Blocks • Harish Kumar",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier intuitive breakdown of LLM, RAG, MCP, Skills, and AI Agents with concrete production prompts",
        "inspired_by": "Harish Kumar • Anatomy of an AI Agent (5 Building Blocks) • Vertex AI Gemini + MCP + OpenHands",
        "accent": PURPLE,
        "hot_topic": "Anatomy of an AI Agent: Brain (LLM), Library (RAG), Nerves (MCP), Memory (Skills) & Hands",
    },
    "T76": {
        "name": "12 Google Cloud Concepts for AI Engineers Spine",
        "best_for_short": "AI Core (1-3) + Compute/Vector (4-7) + Streams (8-10) + IAM/Monitoring (11-12)",
        "content_types": ["PromptCanvas Infographic", "Educational", "Easy to understand", "Working solution"],
        "when_to_use": "Teach how the 12 core Google Cloud services (Vertex AI, Gemini API, TPUs/GPUs, Cloud Run, GKE, Vector Search, GCS, Pub/Sub, Dataflow, BigQuery, IAM/Secrets, Monitoring) fit together.",
        "dynamic": "Packets flow from Vertex AI + Gemini + TPUs through Cloud Run/GKE + Vector Search + GCS, across Pub/Sub + Dataflow -> BigQuery, under IAM & Cloud Monitoring.",
        "lineage": "12 Google Cloud Concepts Every AI Engineer Must Know • Gautami Nadkarni",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier end-to-end map of the 12 essential Google Cloud AI, compute, vector memory, streaming, and security services",
        "inspired_by": "Gautami Nadkarni • 12 Google Cloud AI Concepts • Vertex AI + Cloud Run + GKE + BigQuery + OpenTelemetry",
        "accent": BLUE,
        "hot_topic": "12 Google Cloud Concepts Every AI Engineer Must Know: From Vertex AI to BigQuery",
    },
    "T77": {
        "name": "2026 Pharma R&D & Life Sciences Bio-AI Spine",
        "best_for_short": "Hypothesis Copilots + Virtual Cells + 4 R&D Gates + 2026 Scorecard",
        "content_types": ["PromptCanvas Infographic", "Research topics", "Evaluation results", "Domain application"],
        "when_to_use": "Synthesize the 6 landmark 2026 Pharma R&D AI systems (Gemini Co-Scientist KIRA6 10nM AML hit, Robin RBM24 2.27x AMD hit, MAMMAL 2B samples, MolGenBench, Virtual Screening, VirtualCell) and 4 GxP gates.",
        "dynamic": "Packets link literature/omics hypothesis copilots to robotic wet-lab assays, MAMMAL + VirtualCell perturbation twins, 21 CFR Part 11 GxP gates, and preclinical readouts.",
        "lineage": "2026 Signals from AI in Pharma R&D & Life Sciences • Himanshu Jain",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier life-sciences AI architecture connecting wet-lab closed loops, multimodal foundation models, virtual cells, and GxP release gates",
        "inspired_by": "Himanshu Jain • 2026 Signals from AI in Pharma R&D • Google Co-Scientist + Vertex AI + MAMMAL + OpenHands",
        "accent": GREEN,
        "hot_topic": "2026 Signals from AI in Pharma R&D: Closed-Loop Wet Labs, MAMMAL & Virtual Cells",
    },
    "T78": {
        "name": "Ultimate 6-Stage Agentic Coding Workflow Spine",
        "best_for_short": "6-Stage Flow + Rules/Skills/Subagents + Deterministic Hooks + Power Patterns",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Easy to understand", "Professional knowledge sharing"],
        "when_to_use": "codify the 6-stage agentic coding workflow (Explore -> Plan -> Implement -> Verify -> Review -> Commit), modular AGENTS.md + SKILL.md rules, isolated subagents, and deterministic post-edit hooks.",
        "dynamic": "Packets progress through Explore & Plan, delegate to isolated Explorer/QA/Security subagents via MCP, validate diffs in the post-edit hook loop, and score PR quality.",
        "lineage": "Ultimate Agentic Coding Guide (6-Stage Workflow) • Matt Village",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier agentic coding engineering guide covering the 6-stage workflow, modular rules/skills, isolated subagents, and post-edit hooks",
        "inspired_by": "Matt Village • Ultimate Agentic Coding Guide • Google Antigravity / Gemini CLI + OpenHands + MCP",
        "accent": NAVY,
        "hot_topic": "Ultimate 6-Stage Agentic Coding Guide: Explore, Plan, Subagents & Deterministic Hooks",
    },
    "T79": {
        "name": "Constrained Decoding & Semantic Gate Spine",
        "best_for_short": "Prompt JSON + Grammar Mask + Semantic Gate + Zero Retry",
        "content_types": ["PromptCanvas Infographic", "Working solution", "Grounded concepts", "Evaluation results"],
        "when_to_use": "Contrast prompt-based JSON ('return only JSON', 99/100 trap) against FSM/CFG Constrained Decoding (100% valid shape) plus a deterministic Semantic Gate verifying foreign-key meaning.",
        "dynamic": "Packets flow through FSM/CFG token masking, Pydantic schema compilation, CRM foreign-key semantic checks, and zero-retry production scorecards.",
        "lineage": "Prompt-Based JSON vs. Constrained Decoding (CDM) • Sivasankar Natarajan",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier structured-output engineering breakdown contrasting prose JSON prompts against FSM grammar masks and semantic verification",
        "inspired_by": "Sivasankar Natarajan • Constrained Decoding & Semantic Verification • Google Cloud Vertex AI Controlled Generation + vLLM Outlines",
        "accent": BLUE,
        "hot_topic": "Prompt-Based JSON vs. Constrained Decoding: Why 99/100 Valid Replies Still Break Pipelines",
    },
    "T80": {
        "name": "9 Typed Micro-Decisions in the Agent Loop Spine",
        "best_for_short": "Before Call (01-03) + Inside Loop (04-06) + After Answer (07-09)",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Working solution", "Professional knowledge sharing"],
        "when_to_use": "Map the 9 bounded micro-decisions (input screening, retrieval gate, risk score, tool gate, stop check, model router, grounding audit, memory filter, handoff) to calibrated System-1 classifiers.",
        "dynamic": "Packets route through <15ms single-pass bool/choice/score gates before, inside, and after the main LLM call, cutting full LLM invocations by 60%-75%.",
        "lineage": "Where TypeSafe Jev Fits in the Agent Loop (9 Micro-Decisions) • Rathnakumar Udayakumar",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier System-1 vs. System-2 agent loop map offloading 9 bounded bool/choice/score decisions from full frontier LLM calls",
        "inspired_by": "Rathnakumar Udayakumar • 9 Typed Micro-Decisions in the Agent Loop • Google Cloud Model Armor + Vertex AI + vLLM / LiteLLM",
        "accent": PURPLE,
        "hot_topic": "9 Micro-Decisions Inside Your Agent Loop That Should Not Be Full LLM Calls",
    },
    "T81": {
        "name": "8-Phase Harness Engineering Curriculum Spine",
        "best_for_short": "Repo Rules + Continuity + Maker-Checker + Graph Rollback",
        "content_types": ["PromptCanvas Infographic", "Educational", "Working solution", "Easy to understand"],
        "when_to_use": "Present a step-by-step 8-phase harness engineering curriculum (repo rules, context/memory, session continuity, verification/traces, Maker-Checker loops, parallel DAG rollback).",
        "dynamic": "Packets progress across 14 lectures and 8 real-app projects from AGENTS.md repo structure to trace-verified loops, Maker-Checker gates, and checkpointed graph rollback.",
        "lineage": "Harness Engineering from Scratch (walkinglabs, 21K+ Stars) • Mayank A.",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier open-source engineering curriculum map evolving one real application across 8 progressive agent-harness phases",
        "inspired_by": "Mayank A. • walkinglabs/learn-harness-engineering • Google Cloud ADK + OpenHands + OpenTelemetry",
        "accent": GREEN,
        "hot_topic": "Harness Engineering from Scratch: 8 Phases Beyond Prompt-Only Agent Demos",
    },
    "T82": {
        "name": "Agent Code Review Replay-Set & Misses Spine",
        "best_for_short": "Replay Set + Causal Triage + Dual Timers + SHA Revision Gate",
        "content_types": ["PromptCanvas Infographic", "Evaluation results", "Working solution", "Professional knowledge sharing"],
        "when_to_use": "Design an independent evaluation harness for AI code reviewers using seeded defects, unusual valid PRs, clean baselines, dual timers (run vs. assess), and commit-SHA pinning.",
        "dynamic": "Packets test seeded auth/race bugs and clean PRs, separate bot latency from human triage cost, and bind review sign-off to the exact Git commit SHA.",
        "lineage": "Agent Code Review: Measure What It Missed • Bally S Kehal",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier engineering evaluation harness measuring missed defects, false-alarm triage tax, and commit-SHA revision pinning",
        "inspired_by": "Bally S Kehal • Agent Code Review Evaluation Design • Google Cloud Gemini Code Assist + ADK + OpenHands",
        "accent": TEAL,
        "hot_topic": "Agent Code Review: Why Teams Must Measure Missed Defects & Human Triage Time",
    },
    "T83": {
        "name": "Multi-Trial Agent Evals & pass^k Reliability Spine",
        "best_for_short": "Real Tasks + Isolated Trials + Code/Judge + pass^k (42.2%) Gate",
        "content_types": ["PromptCanvas Infographic", "Evaluation results", "Grounded concepts", "Educational"],
        "when_to_use": "Explain why a 75% per-run agent passes 3 consecutive runs (pass^3) only 42.2% of the time, and how to grade Outcome, Trajectory, Restraint, and calibrated 'unknown' rubrics.",
        "dynamic": "Packets run k=5 isolated env.reset() trials across failure + restraint tasks, run deterministic DB assertions before calibrated judges, and gate shipping on pass^k.",
        "lineage": "Evaluating AI Agents Properly: Outcome, Trajectory & pass^k • Shivani Virdi",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier agent evaluation guide contrasting optimistic pass@k against customer-facing pass^k reliability and restraint checks",
        "inspired_by": "Shivani Virdi • Multi-Turn Agent Evaluation & pass^k Reliability • Google Cloud Vertex AI Eval + Promptfoo + OpenHands",
        "accent": RED,
        "hot_topic": "Why a 75% Agent Fails 57.8% of 3-Run Workflows: Evaluating Outcome, Trajectory & pass^k",
    },
    "T84": {
        "name": "Inference Engineering Roofline & Goodput Spine",
        "best_for_short": "Prefill vs Decode + KV-Cache Math + Batching + SLO Goodput",
        "content_types": ["PromptCanvas Infographic", "Grounded concepts", "Evaluation results", "Research topics"],
        "when_to_use": "Deconstruct LLM serving from first principles: compute-bound Prefill (TTFT) vs. HBM-bandwidth-bound Decode (ITL/TPOT), KV-cache byte math, PagedAttention/FP8, and SLO Goodput.",
        "dynamic": "Packets split across compute-bound prefill and HBM-bound decode pools, apply PagedAttention + chunked prefill + speculative decoding, and optimize p99 SLO Goodput.",
        "lineage": "Inference Engineering Reference Sheet: Roofline, KV-Cache & Goodput • Pallavi Ahuja",
        "category": "PromptCanvas Infographic",
        "best_for": "4-tier systems reference sheet linking Roofline hardware regimes, KV-cache byte math, continuous batching, and SLO Goodput diagnosis",
        "inspired_by": "Pallavi Ahuja • Inference Engineering Reference Sheet • Google Cloud GKE TPU/GPU + Vertex AI + vLLM",
        "accent": BLUE,
        "hot_topic": "Inference Engineering Reference Sheet: Prefill vs. Decode, KV-Cache Math & SLO Goodput",
    },
}

RENDERERS_V4: Dict[str, Any] = {
    tid: (lambda s, phase=None, _tid=tid: _render_canonical_pc(_tid, s, phase))
    for tid in META_V4
}


def demo_specs_v4() -> Dict[str, Dict[str, Any]]:
    return {
        "T53": {
            "title": "Anatomy of a Self-Improving Agent Setup: Context + Harness + Verification Loop + File Graph",
            "subtitle": "PromptCanvas Blueprint #52: Why a model alone plateaus — and how the 4-tier spine turns every bug into a permanent repository upgrade.",
            "source": "PromptCanvas Blueprint #52 • Keith R. Worfolk & Philipp Schmid • Google Cloud Vertex AI + OpenHands / LangGraph",
            "lineage": "PromptCanvas #52 Anatomy Spine • AGENTS.md + SKILL.md + Sandboxed Loop + MAP.md",
        },
        "T54": {
            "title": "How to Pair a Primary Coding Agent with an Independent Reviewer Agent",
            "subtitle": "PromptCanvas Blueprint #53: Install the apps, mount scoped tools (Files, Skills, MCP, Computer Use), and enforce an adversarial Check-Fix-Recheck loop.",
            "source": "PromptCanvas Blueprint #53 • Google Cloud Gemini Code Assist / ADK + OpenHands / Codex / Gemini CLI",
            "lineage": "PromptCanvas #53 Process Workflow • 3-Band Builder + Reviewer Pipeline",
        },
        "T55": {
            "title": "Autonomous Computer-Use Quick-Start Card: 7 Setup Steps & 4 Production Prompts",
            "subtitle": "PromptCanvas Blueprint #54: Configure sandboxed browser/desktop computer use safely, then run four copy-ready workflows with explicit stop gates.",
            "source": "PromptCanvas Blueprint #54 • Google Cloud Vertex AI Computer Use + OpenHands Browser / Playwright Sandbox",
            "lineage": "PromptCanvas #54 Cheat Sheet Card • 7-Step Setup + 4 High-ROI @Browser Workflows",
        },
        "T56": {
            "title": "The AI Nobody Signed Off: Perceived IT Footprint (4 Tools) vs. 24 Shadow AI Pipelines",
            "subtitle": "PromptCanvas Blueprint #55: While leadership assumes four approved chatbots are in use, teams run 24 ungoverned browser extensions, bots, and API keys.",
            "source": "PromptCanvas Blueprint #55 • Google Cloud Model Armor + Apigee AI Gateway + LiteLLM / OPA Governance",
            "lineage": "PromptCanvas #55 Bubble Conceptual • Executive Perception vs. 24 Shadow AI Bubbles",
        },
        "T57": {
            "title": "Raw Foundation Model API (OFF) vs. Managed Enterprise Agent Runtime (ON)",
            "subtitle": "PromptCanvas Blueprint #56: Comparing stateless model inference against a fully managed, production-grade agent runtime across five pillars.",
            "source": "PromptCanvas Blueprint #56 • Google Cloud Vertex AI Agent Engine + LangGraph / Temporal / OpenHands",
            "lineage": "PromptCanvas #56 Side-by-Side Comparison • 5-Pillar OFF vs. ON Toggle Matrix",
        },
        "T58": {
            "title": "The Context Compression Funnel: Refining 1,000,000 Raw Tokens into a 2,000-Token Precision Window",
            "subtitle": "PromptCanvas Blueprint #57: Five deterministic filtering stages eliminate 99.8% of noise before the reasoning model ever generates a token.",
            "source": "PromptCanvas Blueprint #57 • Google Cloud BigQuery Vector Search + AlloyDB pgvector + Vertex AI Ranking API / Qdrant",
            "lineage": "PromptCanvas #57 3D Funnel Pipeline • 1M -> 250k -> 50k -> 10k -> 2k Tokens",
        },
        "T59": {
            "title": "Autonomous Agent Production Deployment Checklist: 6 Mandatory Engineering Gates",
            "subtitle": "PromptCanvas Blueprint #58: The step-by-step verification blueprint to deploy and run secure autonomous agent workloads on Google Cloud and open source.",
            "source": "PromptCanvas Blueprint #58 • Google Cloud Vertex AI / GKE gVisor / AlloyDB + OpenHands / LangGraph / Temporal",
            "lineage": "PromptCanvas #58 Process Checklist • 6 Numbered Deployment Gates with Double ON Switches",
        },
        "T60": {
            "title": "Phased Quarterly Blueprint (Q1–Q4): Enterprise Agentic AI Rollout Roadmap",
            "subtitle": "PromptCanvas Blueprint #59: The four-quarter sequence from read-only evaluation harness (Q1) to sandboxed pilots (Q2), stateful RAG (Q3), and autonomous scale (Q4).",
            "source": "PromptCanvas Blueprint #59 • Google Cloud Vertex AI + GKE + AlloyDB + OpenHands / LangGraph / Promptfoo",
            "lineage": "PromptCanvas #59 Quarterly Roadmap • Q1 Discovery -> Q2 Sandbox -> Q3 State -> Q4 Fleet Governance",
        },
        "T61": {
            "title": "Enterprise Agent Runtime Topology: Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
            "subtitle": "PromptCanvas Blueprint #60: How Google Cloud and open-source runtime planes separate reasoning, orchestration, sandboxed execution, and vector state.",
            "source": "PromptCanvas Blueprint #60 • Google Cloud Architecture Center + Vertex AI / Cloud Run / GKE gVisor / AlloyDB",
            "lineage": "PromptCanvas #60 Runtime Topology • 4-Plane Separation of Concerns",
        },
        "T62": {
            "title": "Hierarchical Multi-Agent Delegation Tree: Supervisor -> Specialist Workers -> Shared Resources",
            "subtitle": "PromptCanvas Blueprint #61: How a Supervisor Agent decomposes complex enterprise goals across isolated worker contexts without context-window bleed.",
            "source": "PromptCanvas Blueprint #61 • Google Cloud ADK + Linux Foundation A2A Protocol + LangGraph Supervisor",
            "lineage": "PromptCanvas #61 Hierarchical Tree • 01 Supervision -> 02a/02b/02c Workers -> 03 Resource Layer",
        },
        "T63": {
            "title": "Agentic AI Portfolio 2x2 Matrix: Business Impact vs. Technical & Governance Complexity",
            "subtitle": "PromptCanvas Blueprint #62: How engineering leaders classify 20 concrete agent initiatives into Quick Wins (01), Strategic Bets (02), Low Priority (03), and Traps (04).",
            "source": "PromptCanvas Blueprint #62 • Google Cloud Enterprise AI Value Realization Framework + Open-Source Agent Benchmarks",
            "lineage": "PromptCanvas #62 2x2 Quadrant Matrix • 20 Grounded Use Cases Across 4 Quadrants",
        },
        "T64": {
            "title": "Deterministic Agent Decision Tree: Conditional Branching Across Ingest, RBAC & Sandbox",
            "subtitle": "PromptCanvas Blueprint #63: Why production agents never rely on free-form LLM judgment for safety, authorization, or completion.",
            "source": "PromptCanvas Blueprint #63 • Google Cloud ADK + Model Armor + OPA / Cloud IAM + GKE gVisor / OpenHands",
            "lineage": "PromptCanvas #63 Decision Tree Flowchart • 3 Stages, 4 Decision Diamonds, Self-Correction Loop",
        },
        "T65": {
            "title": "Multi-Criteria Agent Stack Evaluation Matrix: Scoring 4 Architectures Across 5 Pillars",
            "subtitle": "PromptCanvas Blueprint #64: Side-by-side capability and scoring matrix comparing managed, open-source graph, sandbox-first, and raw wrapper patterns.",
            "source": "PromptCanvas Blueprint #64 • Google Cloud Vertex AI Agent Engine + Google ADK + LangGraph + OpenHands",
            "lineage": "PromptCanvas #64 Feature Matrix Grid • 5 Criteria x 4 Architectural Patterns",
        },
        "T66": {
            "title": "The 4-Tier Agent Capability Pyramid: From Raw Inference to Autonomous Self-Healing",
            "subtitle": "PromptCanvas Blueprint #65: The architectural evolution of enterprise AI systems from stateless prompting (Tier 01) to goal-driven autonomy (Tier 04).",
            "source": "PromptCanvas Blueprint #65 • Google Cloud Agent Architecture Guide + Vertex AI / GKE / AlloyDB + OpenHands / LangGraph",
            "lineage": "PromptCanvas #65 Capability Pyramid • 01 Base -> 02 Tools -> 03 Multi-Agent -> 04 Autonomous Apex",
        },
        "T67": {
            "title": "The Autonomous Self-Healing Agent Loop: Generate -> Sandbox Test -> Gate -> Repair",
            "subtitle": "PromptCanvas Blueprint #66: How production agents turn runtime failures into deterministic retries without human babysitting or runaway loops.",
            "source": "PromptCanvas Blueprint #66 • Google Cloud Vertex AI + GKE gVisor + OpenHands CodeAct + Promptfoo / pytest",
            "lineage": "PromptCanvas #66 Loop & Cycle • 4-Quadrant Torus Ring with PASS (Deploy ON) & FAIL (Retry ACTIVE) Gates",
        },
        "T68": {
            "title": "Open Knowledge Format Architecture: Open Formats + Schema Harness + Validation Loop + Graph",
            "subtitle": "PromptCanvas Open Knowledge Blueprint: Why agent memory must live in open, schema-validated, SHA-linked files rather than opaque proprietary blobs.",
            "source": "PromptCanvas Open Knowledge Format Infographic • LangChain OpenWiki + Google Cloud BigQuery / AlloyDB + Pydantic / JSON Schema",
            "lineage": "PromptCanvas Open Knowledge Spine • LangChain OpenWiki",
        },
        "T69": {
            "title": "Harness²: Recursive Agent Harnessing for an Open World (+22pp NoveltyBench)",
            "subtitle": "Google Harness² (arXiv:2604.08523): Why static hand-crafted harnesses fail on out-of-distribution tasks and how a meta-harness synthesizes custom tools and critics.",
            "source": "Google Harness² Paper (arXiv:2604.08523) • Aishwarya Naresh Reganti • Google Cloud Vertex AI ADK + GKE gVisor + OpenHands / LangGraph",
            "lineage": "Google Harness² Recursive Spine • Static Trap + Dynamic Synthesis + Critic Loop + +22pp Gain",
        },
        "T70": {
            "title": "The 5-Repo Agent Engineering Stack: Skills + Org Orchestration + Memory Graph + CI/CD",
            "subtitle": "How gstack (Garry Tan), Paperclip, agency-agents, rowboat, and multica combine into a complete multi-agent engineering organization.",
            "source": "Vaibhav Sisinty • gstack + Paperclip + agency-agents + rowboat + multica • Google Cloud Vertex AI / ADK + OpenHands / MCP",
            "lineage": "5-Repo Agent Stack Spine • Role Skills + Org Chart + Knowledge Graph + Autonomous CI/CD",
        },
        "T71": {
            "title": "The 3-Track Data Modeling & Medallion Architecture Map: Design, Meaning & Consumption",
            "subtitle": "How Conceptual/Logical/Physical schemas (Track 1), Glossary/Ontology/Knowledge Graphs (Track 2), and Semantic Layer KPIs (Track 3) align across Bronze, Silver, and Gold.",
            "source": "Nan Li • The Data Modeling Map • Google Cloud BigQuery + Dataplex + AlloyDB pgvector + dbt / Looker / OpenTelemetry",
            "lineage": "3-Track Data Modeling Spine • Medallion Design + Semantic Ontology + Governed Consumption",
        },
        "T72": {
            "title": "TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents (-30.9%)",
            "subtitle": "UC Berkeley & Microsoft research: How trace-driven micro-skills, tool schema pruning (23 -> 3 tools), and loop intervention save 18.4%-30.9% across 30/30 SWE-Bench Verified configs.",
            "source": "Alena Panshina • UC Berkeley & Microsoft TokenEconomizer • Google Cloud Vertex AI Gemini + OpenHands / LangGraph",
            "lineage": "TokenEconomizer Spine • Trace Loop + 3-Line Micro-Skills + Tool Pruning + SWE-Bench Gains",
        },
        "T73": {
            "title": "11-Zone Production-Grade Agentic AI Reference Architecture: Gateway, Approvals & AgentOps",
            "subtitle": "How enterprise agents move from fragile demos to governed production across Perimeter, Supervisor Runtime, AgentCore Gateway, Risk-Tiered HITL Approvals, and AgentOps.",
            "source": "Rajesh Kumar • 11-Zone Production Agentic AI Architecture • Google Cloud GKE + Apigee + Vertex AI + LangGraph / OpenTelemetry",
            "lineage": "11-Zone Production Agentic Spine • Perimeter + AgentCore Gateway + Approval Gate + AgentOps",
        },
        "T74": {
            "title": "The AI Agent Sandbox Landscape Across 6 Vendors: Kernel Isolation & Secret Proxies",
            "subtitle": "Comparing Google Cloud GKE Agent Sandbox (gVisor), AWS Bedrock AgentCore + Strands, Microsoft Agent Workspace, NVIDIA OpenShell DPU, Perplexity SPACE, and OpenAI.",
            "source": "Rakesh Gohel • 6-Vendor AI Agent Sandbox Landscape • Google Cloud GKE Agent Sandbox (gVisor) + Vertex AI + OpenHands",
            "lineage": "6-Vendor Sandbox Spine • microVM Isolation + External Secret Proxy + Egress Loop + 6-Vendor Matrix",
        },
        "T75": {
            "title": "Anatomy of an AI Agent: How LLM, RAG, MCP, and Skills Combine Into One System",
            "subtitle": "Five intuitive building blocks: 1. LLM = The Brain, 2. RAG = The Library, 3. MCP = The Nervous System, 4. Skills = Muscle Memory, 5. AI Agent = Brain + Hands.",
            "source": "Harish Kumar • Anatomy of an AI Agent (5 Building Blocks) • Google Cloud Vertex AI Gemini + Vertex Search + MCP + OpenHands",
            "lineage": "5-Block Agent Anatomy Spine • Brain (LLM) + Library (RAG) + Nerves (MCP) + Memory (Skills) + Hands",
        },
        "T76": {
            "title": "12 Google Cloud Concepts Every AI Engineer Must Know: From Vertex AI to BigQuery",
            "subtitle": "How Vertex AI, Gemini API, TPUs/GPUs, Cloud Run, GKE, Vector Search, Cloud Storage, Pub/Sub, Dataflow, BigQuery, IAM/Secret Manager, and Cloud Monitoring connect.",
            "source": "Gautami Nadkarni • 12 Google Cloud AI Concepts • Google Cloud Vertex AI + Cloud Run + GKE + BigQuery + OpenTelemetry / MCP",
            "lineage": "12 Google Cloud AI Concepts Spine • AI Core + Compute/Vector Memory + Streaming ETL + IAM/Monitoring",
        },
        "T77": {
            "title": "2026 Signals from AI in Pharma R&D & Life Sciences: Closed-Loop Wet Labs & Virtual Cells",
            "subtitle": "Six landmark bio-AI breakthroughs (Gemini Co-Scientist KIRA6 10nM AML hit, Robin RBM24 AMD hit, MAMMAL 2B samples, MolGenBench, Virtual Screening, VirtualCell) and 4 GxP gates.",
            "source": "Himanshu Jain • 2026 Signals from AI in Pharma R&D • Google Co-Scientist + Vertex AI + AlphaFold + OpenHands / LangGraph",
            "lineage": "2026 Pharma R&D Bio-AI Spine • Hypothesis Copilots + Wet-Lab Loops + Virtual Cells + GxP Gates",
        },
        "T78": {
            "title": "Ultimate 6-Stage Agentic Coding Guide: Explore, Plan, Subagents & Deterministic Hooks",
            "subtitle": "How high-velocity engineers pair a 6-stage workflow (Explore -> Plan -> Implement -> Verify -> Review -> Commit) with modular AGENTS.md/SKILL.md rules, subagents, and hooks.",
            "source": "Matt Village • Ultimate Agentic Coding Guide • Google Antigravity + Gemini CLI + Vertex AI + OpenHands / MCP",
            "lineage": "6-Stage Agentic Coding Spine • Explore/Plan + Modular Rules/Skills + Isolated Subagents + Hooks",
        },
        "T79": {
            "title": "Prompt-Based JSON vs. Constrained Decoding: Enforcing Schema Shape & Semantic Meaning",
            "subtitle": "Why 'return only valid JSON' works 99 times and breaks your parser on the 100th — and why FSM grammar masks still need a foreign-key semantic gate.",
            "source": "Sivasankar Natarajan • Constrained Decoding & Semantic Gate • Google Cloud Vertex AI Controlled Generation + vLLM Outlines / Pydantic",
            "lineage": "Constrained Decoding Spine • Prompt JSON Trap + FSM Grammar Mask + Semantic Gate + Zero Retry",
        },
        "T80": {
            "title": "9 Typed Micro-Decisions Inside the Agent Loop Without Full LLM Calls",
            "subtitle": "How to offload bounded bool, choice, and score gates Before, Inside, and After the main LLM call to calibrated <15ms System-1 classifiers.",
            "source": "Rathnakumar Udayakumar • TypeSafe Jev 9-Decision Agent Loop • Google Cloud Model Armor + Vertex AI + vLLM / LiteLLM",
            "lineage": "9-Decision Agent Loop Spine • Before Call (01-03) + Inside Loop (04-06) + After Answer (07-09)",
        },
        "T81": {
            "title": "Harness Engineering from Scratch: 14 Lectures & 8 Projects Evolving One Real App",
            "subtitle": "How walkinglabs/learn-harness-engineering moves beyond prompt-only tutorials across repository rules, continuity ledgers, Maker-Checker loops, and DAG rollback.",
            "source": "Mayank A. • walkinglabs/learn-harness-engineering (21K+ Stars) • Google Cloud ADK + OpenHands + OpenTelemetry",
            "lineage": "8-Phase Harness Engineering Spine • Repo Rules + Continuity + Maker-Checker + Graph Rollback",
        },
        "T82": {
            "title": "Agent Code Review Evaluation Design: Measure Missed Defects & Human Triage Cost",
            "subtitle": "Why engineering teams must test AI reviewers against seeded defects, unusual valid PRs, dual timers (run vs. assess), and commit-SHA revision pinning.",
            "source": "Bally S Kehal • Agent Code Review Replay-Set Design • Google Cloud Gemini Code Assist + ADK + OpenHands",
            "lineage": "Code Review Eval Spine • Seeded Replay Set + Causal Triage + Dual Timers + Commit-SHA Pinning",
        },
        "T83": {
            "title": "Evaluating AI Agents Properly: Outcome, Trajectory, Restraint & pass^k Reliability",
            "subtitle": "Why a 75% per-run agent passes 3 consecutive runs (pass^3) only 42.2% of the time — and how to combine code assertions with calibrated 'unknown'-capable judges.",
            "source": "Shivani Virdi • Multi-Turn Agent Evaluation Guide • Google Cloud Vertex AI Eval + Promptfoo + OpenHands / pytest",
            "lineage": "Multi-Trial Agent Eval Spine • Failure + Restraint Tasks + Isolated env.reset() + pass^k Gate",
        },
        "T84": {
            "title": "Inference Engineering Reference Sheet: Prefill vs. Decode, KV-Cache Math & SLO Goodput",
            "subtitle": "First-principles LLM serving across compute-bound Prefill (TTFT), HBM-bandwidth-bound Decode (ITL/TPOT), PagedAttention, FP8 KV quantization, and p99 Goodput.",
            "source": "Pallavi Ahuja • Inference Engineering Reference Sheet • Google Cloud GKE TPU/GPU + Vertex AI + vLLM / SGLang",
            "lineage": "Inference Engineering Spine • Roofline Split + KV-Cache Math + Batching + SLO Goodput",
        },
    }


register_templates(META_V4, RENDERERS_V4, demo_specs_v4)
