"""Template Gallery v4 — 16 PromptCanvas Canonical Infographic Diagrams (T53-T68).

Brings all 16 Infographic Blueprints from PromptCanvas (`src/lib/canonical/infographicBlueprints52to66.ts` #52-#66
and `src/lib/canonical/openKnowledgeInfographic.ts`) into the Executive Light-Theme Glassmorphic Design System v3.0
(1600x980 widescreen, animated moving-arrow conduits, glowing signal packets, zero-origin W3C SVG geometry,
and dual-stack Google Cloud + Open-Source pairings):

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
import math
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from src.visuals.template_gallery import (
    AMBER, BG, BLUE, CSS, GREEN, INK, LINE, MUTED, NAVY, PURPLE, RED, SKY, SLATE, TEAL, WHITE,
    _arc_pts, _card_head, _diamond, _esc, _flow, _frame as _base_frame, _grow, _pill, _r, _t, _tl, _wrap, register_templates,
)

Point = Tuple[float, float]

_CANONICAL_REF_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "canonical-ref"
_B64_CACHE: Dict[str, Tuple[int, int, str, str]] = {}


def _load_canonical_pc_asset(tid: str) -> Optional[Tuple[int, int, str, str]]:
    if tid in _B64_CACHE:
        return _B64_CACHE[tid]
    png_path = _CANONICAL_REF_DIR / f"canonical_{tid}.png"
    dims_path = _CANONICAL_REF_DIR / "canonical_dimensions.json"
    if not png_path.exists():
        return None
    cw, ch, bg = 1600, 1050, "#F8FAFC"
    if dims_path.exists():
        try:
            dims = json.loads(dims_path.read_text(encoding="utf-8")).get(tid, {})
            cw = int(dims.get("width", cw))
            ch = int(dims.get("height", ch))
            bg = str(dims.get("background", bg)).upper()
        except Exception:
            pass
    b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
    _B64_CACHE[tid] = (cw, ch, bg, b64)
    return _B64_CACHE[tid]


def _render_canonical_pc(
    tid: str,
    s: Dict[str, Any],
    phase: Optional[float] = None,
    fallback_fn: Optional[Callable[[Dict[str, Any], Optional[float]], str]] = None,
) -> str:
    asset = _load_canonical_pc_asset(tid)
    if asset is None:
        return fallback_fn(s, phase) if fallback_fn else ""
    cw, ch, _bg, b64 = asset
    meta = META_V4[tid]
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


def _frame(title: str, subtitle: str, source: str, body_svg: str, badge_label: str,
           accent: str = BLUE, lineage: Optional[str] = None) -> str:
    tid = badge_label.split()[0].strip()
    meta = META_V4[tid]
    return _base_frame(tid, meta, title, subtitle, [body_svg], source, lineage or meta.get("lineage"))



def _fl(pts: Sequence[Point], col: str, phase: Optional[float], dur: float = 1.6,
        label: Optional[str] = None, dash: str = "8 5", packets: int = 1,
        label_dy: float = 0.0, label_at: float = 0.5, solid: bool = False) -> str:
    return _flow(pts, col, phase, label, dur, 2.6, True, packets, dash=dash, track=True, label_dy=label_dy, label_at=label_at, solid=solid)


def _num_badge(cx: float, cy: float, code: str, col: str, r: float = 15) -> str:
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 3.0:.1f}" fill="{col}" fill-opacity="0.14"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}" stroke="#FFFFFF" stroke-width="2.0"/>'
        + _t(cx, cy + 4.2, code, 10.6, 800, WHITE, "middle")
    )


def _toggle_switch(x: float, y: float, state: str = "ON", label: Optional[str] = None) -> str:
    is_on = state.upper() in ("ON", "ACTIVE", "PASS", "YES")
    bg_col = "#16A34A" if is_on else "#DC2626"
    track_col = "#15803D" if is_on else "#B91C1C"
    w = 112 if label else 66
    out = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="26" rx="13" fill="{bg_col}" stroke="{track_col}" stroke-width="1.2"/>',
        f'<rect x="{x + 2:.1f}" y="{y + 1.5:.1f}" width="{w - 4}" height="8" rx="4" fill="#FFFFFF" fill-opacity="0.18"/>',
    ]
    if label:
        out.append(_t(x + 28, y + 17, label, 9.2, 800, WHITE, "middle"))
        sx = x + 52
        sw = 56
        out.append(f'<rect x="{sx:.1f}" y="{y + 3:.1f}" width="{sw}" height="20" rx="10" fill="{track_col}"/>')
        if is_on:
            out.append(_t(sx + 18, y + 16.5, state.upper(), 8.5, 800, WHITE, "middle"))
            out.append(f'<circle cx="{sx + sw - 11:.1f}" cy="{y + 13:.1f}" r="7.2" fill="#FFFFFF"/>')
        else:
            out.append(f'<circle cx="{sx + 11:.1f}" cy="{y + 13:.1f}" r="7.2" fill="#FFFFFF"/>')
            out.append(_t(sx + 36, y + 16.5, state.upper(), 8.5, 800, WHITE, "middle"))
    else:
        if is_on:
            out.append(_t(x + 22, y + 17, state.upper(), 9.2, 800, WHITE, "middle"))
            out.append(f'<circle cx="{x + w - 13:.1f}" cy="{y + 13:.1f}" r="8.2" fill="#FFFFFF"/>')
        else:
            out.append(f'<circle cx="{x + 13:.1f}" cy="{y + 13:.1f}" r="8.2" fill="#FFFFFF"/>')
            out.append(_t(x + 42, y + 17, state.upper(), 9.2, 800, WHITE, "middle"))
    return "".join(out)


# ----------------------------------------------------------------------------------------------------------------------
# T53 (PromptCanvas #52) — Infographic: Anatomy / Deconstruction (4-Tier Spine: Context + Harness + Loop + Graph)
# ----------------------------------------------------------------------------------------------------------------------
def render_t53(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    tiers = s["tiers"][:4]
    cx = 800.0

    for i, tr in enumerate(tiers):
        ty = 142 + i * 182
        col = tr["color"]
        # Clean Executive Light tier enclave
        b.append(_r(56, ty, 1488, 168, 12, "#F8FAFC", "#CBD5E1", 1.5))
        b.append(_r(56, ty, 8, 168, 4, col))
        # Left Stage Badge & Summary Card
        b.append(_card_head(78, ty + 14, 344, 108, col, f"{tr['num']} • {tr['name']} ({tr['tag']})", head_h=25))
        b.append(_t(94, ty + 56, tr["headline"], 10.4, 800, INK))
        b.append(_tl(94, ty + 72, _wrap(tr["left_desc"], 46, 3), 8.9, 600, SLATE, 12.2))
        b.append(_t(94, ty + 114, tr["stack"], 8.8, 700, col, mono=True))

        # Left-to-Center and Center-to-Right orthogonal connectors
        b.append(_fl([(422, ty + 68), (656, ty + 68)], col, phase, 1.5))
        b.append(_fl([(944, ty + 68), (1018, ty + 68)], col, phase, 1.5))
        if i < 3:
            b.append(_fl([(cx, ty + 118), (cx, ty + 200)], col, phase, 1.4))

        # Center Spine Node
        b.append(_r(660, ty + 18, 280, 100, 10, WHITE, col, 2.0))
        b.append(_num_badge(686, ty + 42, tr["num"], col, 13))
        b.append(_t(710, ty + 39, tr["center_title"], 10.8, 800, NAVY))
        b.append(_t(710, ty + 55, tr["center_sub"], 9.2, 700, col, mono=True))
        for j, chip in enumerate(tr["chips"][:3]):
            cx0 = 674 + j * 86
            b.append(_r(cx0, ty + 72, 80, 32, 6, "#F8FAFC", col, 1.2))
            b.append(_t(cx0 + 40, ty + 92, chip, 8.8, 800, INK, "middle", mono=True))

        # Right Artifact / Verification Cards (2 cards side by side)
        for k, card in enumerate(tr["right_cards"][:2]):
            rx = 1020 + k * 256
            b.append(_r(rx, ty + 14, 244, 108, 10, WHITE, col, 1.5))
            b.append(_r(rx, ty + 14, 6, 108, 3, col))
            b.append(_t(rx + 18, ty + 33, card["title"], 10.0, 800, NAVY))
            b.append(_tl(rx + 18, ty + 49, _wrap(card["body"], 33, 3), 8.8, 600, SLATE, 12.2))
            b.append(_pill(rx + 18, ty + 95, card["badge"], col, size=8.0, h=18)[0])

        # Bottom Actionable RULE Bar inside each tier
        b.append(_r(78, ty + 130, 1448, 28, 6, WHITE, "#CBD5E1", 1.3))
        b.append(_r(78, ty + 130, 96, 28, 6, col))
        b.append(_t(126, ty + 148, f"RULE {tr['num']}", 9.5, 800, WHITE, "middle"))
        b.append(_t(188, ty + 148, tr["rule"], 9.8, 700, INK))
        b.append(_pill(1514, ty + 134, tr["metric"], col, size=8.5, h=20, anchor_end=True)[0])

    # Bottom Takeaway Bar
    b.append(_r(56, 872, 1488, 34, 8, "#F8FAFC", BLUE, 1.4))
    b.append(_t(76, 894, s["takeaway"], 10.4, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T53 • PROMPTCANVAS #52 ANATOMY SPINE", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T54 (PromptCanvas #53) — Infographic: Process Workflow (Primary Coding Agent + Reviewer Agent)
# ----------------------------------------------------------------------------------------------------------------------
def render_t54(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Band 01: INSTALL + START (y=142..330)
    b.append(_card_head(56, 142, 1488, 186, BLUE, "BAND 01 • INSTALL + START — PAIR A PRIMARY CODING AGENT WITH AN INDEPENDENT REVIEWER AGENT", fill="#F8FAFC", head_h=28))
    b.append(_pill(1528, 146, "GOOGLE ADK / GEMINI + OPENHANDS / CODEX", BLUE, fill="#EFF6FF", size=8.4, h=20, anchor_end=True)[0])

    for i, st in enumerate(s["band1_steps"][:4]):
        sx = 76 + i * 370
        col = st["color"]
        b.append(_r(sx, 184, 332, 130, 10, WHITE, col, 1.6))
        b.append(_num_badge(sx + 24, 208, f"0{i + 1}", col, 12.5))
        b.append(_t(sx + 46, 212, st["title"], 10.5, 800, INK))
        b.append(_pill(sx + 320, 195, st["tag"], col, size=8.0, h=18, anchor_end=True)[0])
        b.append(_tl(sx + 18, 236, _wrap(st["body"], 43, 3), 9.4, 600, SLATE, 14))
        b.append(_r(sx + 18, 282, 296, 22, 5, "#F8FAFC", "#CBD5E1", 1))
        b.append(_t(sx + 28, 297, st["cmd"], 8.9, 700, col, mono=True))
        if i < 3:
            b.append(_fl([(sx + 332, 249), (sx + 368, 249)], col, phase, 1.2))

    # Band 02: ADD YOUR TOOLS + CONDITIONAL BRANCHING (y=342..592)
    b.append(_card_head(56, 342, 1488, 250, PURPLE, "BAND 02 • ADD YOUR TOOLS — MOUNT FILES + SKILLS, MCP CONNECTORS, AND SANDBOXED COMPUTER USE", fill="#F8FAFC", head_h=28))

    for i, tl in enumerate(s["band2_tools"][:3]):
        tx = 76 + i * 320
        col = tl["color"]
        b.append(_card_head(tx, 384, 282, 192, col, tl["head"], head_h=25))
        b.append(_t(tx + 16, 428, tl["sub"], 10.0, 800, INK))
        for j, bul in enumerate(tl["bullets"][:3]):
            b.append(_t(tx + 16, 450 + j * 20, f"• {bul}", 9.2, 600, SLATE))
        b.append(_r(tx + 16, 518, 250, 42, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(tx + 24, 535, tl["example_label"], 8.4, 800, col))
        b.append(_t(tx + 24, 550, tl["example_code"], 8.6, 700, INK, mono=True))
        b.append(_fl([(tx + 282, 480), (tx + 318, 480)], col, phase, 1.3))

    # Decision Diamond + Strict 90-Degree Orthogonal YES/NO Outcomes on Right of Band 02
    b.append(_diamond(1112, 480, 76, 46, ["ALL REQUIRED", "TOOLS READY?"], AMBER, 9.8))
    b.append(_fl([(1112, 434), (1112, 412), (1256, 412)], RED, phase, 1.4, label="NO", label_dy=0, label_at=0.58))
    b.append(_fl([(1112, 526), (1112, 536), (1256, 536)], GREEN, phase, 1.4, label="YES", label_dy=0, label_at=0.58))

    b.append(_r(1258, 382, 268, 84, 10, WHITE, RED, 1.5))
    b.append(_r(1258, 382, 6, 84, 3, RED))
    b.append(_t(1274, 404, "NO -> MOUNT MISSING TOOL", 9.8, 800, RED))
    b.append(_tl(1274, 422, ["Register SKILL.md or scoped MCP", "server in .mcp.json before run."], 9.1, 600, SLATE, 14))

    b.append(_r(1258, 484, 268, 92, 10, WHITE, GREEN, 1.5))
    b.append(_r(1258, 484, 6, 92, 3, GREEN))
    b.append(_t(1274, 505, "YES -> EXECUTE IN SANDBOX", 9.8, 800, GREEN))
    b.append(_tl(1274, 522, ["Primary Agent runs code & tools", "inside Cloud Run gVisor sandbox."], 9.1, 600, SLATE, 13.5))
    b.append(_pill(1274, 550, "READY FOR BAND 03", GREEN, size=8.2, h=18)[0])

    # Band 03: CHECK IT — ADVERSARIAL REVIEW & RECHECK LOOP (y=604..856)
    b.append(_card_head(56, 604, 1488, 252, GREEN, "BAND 03 • CHECK IT — REVIEWER AGENT ADVISES -> PRIMARY AGENT FIXES + TESTS -> RECHECK -> YOU DECIDE", fill="#F8FAFC", head_h=28))

    for i, chk in enumerate(s["band3_loop"][:4]):
        cx0 = 76 + i * 370
        col = chk["color"]
        b.append(_card_head(cx0, 646, 332, 152, col, chk["head"], head_h=25))
        b.append(_t(cx0 + 16, 690, chk["role"], 10.2, 800, INK))
        b.append(_tl(cx0 + 16, 710, _wrap(chk["body"], 42, 3), 9.3, 600, SLATE, 14.5))
        b.append(_r(cx0 + 16, 760, 300, 26, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(cx0 + 26, 777, chk["gate"], 8.9, 700, col, mono=True))
        if i < 3:
            b.append(_fl([(cx0 + 332, 722), (cx0 + 368, 722)], col, phase, 1.3))

    # Recheck feedback loop arrow under cards 3 -> 1 with inline opaque pill masking the line
    b.append(_fl([(982, 798), (982, 834), (242, 834), (242, 800)], AMBER, phase, 2.0,
                 label="RECHECK LOOP: Reviewer findings + pytest stderr fed back until exit_code == 0",
                 label_dy=0, label_at=0.5))

    b.append(_r(56, 870, 1488, 36, 8, "#F8FAFC", BLUE, 1.4))
    b.append(_t(76, 893, s["takeaway"], 10.4, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T54 • PROMPTCANVAS #53 PROCESS WORKFLOW", PURPLE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T55 (PromptCanvas #54) — Infographic: Cheat Sheet Quick-Start Card (Autonomous Agent Computer Use)
# ----------------------------------------------------------------------------------------------------------------------
def render_t55(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Left Column: Start Using It (Steps 01-07) + Copy-Paste Prompt Formula (x=56..684, y=142..856)
    b.append(_card_head(56, 142, 628, 514, BLUE, "LEFT PANEL • START USING IT IN 7 DETERMINISTIC STEPS", head_h=28))
    for i, st in enumerate(s["setup_steps"][:7]):
        sy = 182 + i * 64
        col = st["color"]
        b.append(_r(74, sy, 592, 54, 8, "#F8FAFC", col, 1.4))
        b.append(_num_badge(100, sy + 27, f"0{i + 1}", col, 13))
        b.append(_t(126, sy + 22, st["title"], 10.6, 800, INK))
        b.append(_t(126, sy + 41, st["detail"], 9.3, 600, SLATE))
        b.append(_pill(654, sy + 16, st["pill"], col, size=8.2, h=20, anchor_end=True)[0])

    # Left Bottom: Try This Prompt Formula Box (y=668..856)
    b.append(_card_head(56, 668, 628, 188, NAVY, "TRY THIS COPY-PASTE COMPUTER-USE PROMPT FORMULA", head_h=28))
    for i, fl in enumerate(s["formula_lines"][:4]):
        fy = 708 + i * 28
        b.append(_r(74, fy, 592, 24, 5, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(88, fy + 16, fl, 9.6, 700, NAVY, mono=True))
    b.append(_t(74, 840, s["safety_note"], 8.8, 800, RED))

    # Animated conduit from Left Setup to Right Jobs (42px gap)
    b.append(_fl([(684, 480), (726, 480)], BLUE, phase, 1.4))

    # Right Column: Four High-ROI Jobs to Start With (2x2 Grid, x=728..1544, y=142..856)
    b.append(_card_head(728, 142, 816, 714, PURPLE, "RIGHT PANEL • FOUR PRODUCTION JOBS TO START WITH (@Browser + MCP + Sandbox)", head_h=28))
    for i, job in enumerate(s["jobs"][:4]):
        col_idx = i % 2
        row_idx = i // 2
        jx = 748 + col_idx * 394
        jy = 186 + row_idx * 326
        col = job["color"]
        b.append(_card_head(jx, jy, 376, 308, col, f"JOB 0{i + 1} • {job['domain']}", head_h=26))
        b.append(_t(jx + 16, jy + 46, job["headline"], 10.8, 800, INK))
        b.append(_tl(jx + 16, jy + 66, _wrap(job["what_it_does"], 48, 2), 9.4, 600, SLATE, 14.5))

        # Prompt Card inside Job
        b.append(_r(jx + 16, jy + 104, 344, 120, 8, "#F8FAFC", "#CBD5E1", 1.3))
        b.append(_t(jx + 26, jy + 123, "COPY-READY PROMPT:", 8.8, 800, col))
        b.append(_pill(jx + 348, jy + 110, job["app_tag"], col, size=8.0, h=18, anchor_end=True)[0])
        b.append(_tl(jx + 26, jy + 142, _wrap(job["prompt"], 44, 4), 9.1, 700, INK, 14.5, mono=True))

        # Guardrail + Stack Footer inside Job
        b.append(_r(jx + 16, jy + 234, 344, 32, 6, "#FEF2F2", "#FECACA", 1.1))
        b.append(_t(jx + 26, jy + 254, f"STOP GATE: {job['stop_gate']}", 9.0, 800, RED))
        b.append(_t(jx + 16, jy + 288, job["stack"], 8.8, 700, col, mono=True))

    b.append(_r(56, 870, 1488, 36, 8, "#F8FAFC", GREEN, 1.4))
    b.append(_t(76, 893, s["takeaway"], 10.4, 800, "#065F46"))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T55 • PROMPTCANVAS #54 CHEAT SHEET CARD", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T56 (PromptCanvas #55) — Infographic: Bubble Conceptual (The AI Nobody Signed Off — Shadow AI vs. Governed AI)
# ----------------------------------------------------------------------------------------------------------------------
def render_t56(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Left Panel: WHAT LEADERSHIP THINKS (x=56..512, y=142..768)
    b.append(_card_head(56, 142, 456, 626, NAVY, "WHAT LEADERSHIP THINKS (4 APPROVED TOOLS)", head_h=28))
    # Executive Vector Persona Badge
    b.append(_r(76, 186, 416, 134, 10, "#F8FAFC", BLUE, 1.5))
    b.append('<circle cx="136" cy="242" r="30" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.0"/>')
    b.append('<circle cx="136" cy="230" r="10.5" fill="#1E3A8A"/>')
    b.append('<path d="M 114 263 C 118 248 154 248 158 263 Z" fill="#1E3A8A"/>')
    b.append(_t(184, 210, "EXECUTIVE ASSUMPTION MODEL", 10.6, 800, NAVY))
    b.append(_tl(184, 228, _wrap(s["exec_caption"], 42, 3), 9.1, 600, SLATE, 13.5))
    b.append(_pill(184, 286, "PERCEIVED SURFACE: 4 TOOLS", BLUE, size=8.5, h=20)[0])

    for i, quote in enumerate(s["exec_quotes"][:4]):
        qy = 336 + i * 102
        b.append(_r(76, qy, 416, 88, 10, WHITE, "#CBD5E1", 1.4))
        b.append(_r(76, qy, 6, 88, 3, BLUE))
        b.append(_t(94, qy + 24, quote["quote"], 10.2, 800, INK))
        b.append(_pill(480, qy + 9, quote["risk_tag"], RED, size=7.6, h=18, anchor_end=True)[0])
        b.append(_tl(94, qy + 46, _wrap(quote["reality_gap"], 54, 2), 9.0, 600, SLATE, 14))

    # Conduit from Perception to Reality (48px gap)
    b.append(_fl([(512, 455), (560, 455)], RED, phase, 1.4))

    # Right Panel: WHAT IS ACTUALLY RUNNING — 24 SHADOW AI BUBBLES ACROSS 4 CLUSTERS (x=562..1544, y=142..768)
    b.append(_card_head(562, 142, 982, 626, RED, "WHAT IS ACTUALLY RUNNING (24 UNGOVERNED SHADOW AI TOOLS & EXTENSION PIPELINES)", head_h=28))
    for i, cl in enumerate(s["clusters"][:4]):
        cx0 = 582 + (i % 2) * 474
        cy0 = 186 + (i // 2) * 282
        col = cl["color"]
        b.append(_r(cx0, cy0, 454, 266, 12, "#F8FAFC", col, 1.5))
        b.append(_t(cx0 + 16, cy0 + 24, f"{cl['name']} ({cl['count']})", 10.4, 800, NAVY))
        b.append(_pill(cx0 + 438, cy0 + 8, cl["risk"], col, size=8.2, h=18, anchor_end=True)[0])

        # 6 Bubble Nodes inside each cluster (2 rows x 3 columns)
        for j, bub in enumerate(cl["bubbles"][:6]):
            bx = cx0 + 15 + (j % 3) * 144
            by = cy0 + 42 + (j // 3) * 106
            b.append(_r(bx, by, 132, 92, 16, WHITE, col, 1.5))
            b.append(f'<circle cx="{bx + 17:.1f}" cy="{by + 20:.1f}" r="7" fill="{col}" fill-opacity="0.16"/>')
            b.append(f'<circle cx="{bx + 17:.1f}" cy="{by + 20:.1f}" r="3.5" fill="{col}"/>')
            b.append(_t(bx + 28, by + 24, bub["name"], 8.6, 800, INK))
            b.append(_tl(bx + 12, by + 42, _wrap(bub["usage"], 21, 2), 8.0, 600, SLATE, 12.0))
            b.append(_pill(bx + 12, by + 68, bub["exposure"], col, size=7.4, h=16)[0])

    # Bottom Governance Bridge Bar (y=782..904)
    b.append(_card_head(56, 782, 1488, 122, GREEN, "THE GOVERNANCE FIX • ROUTE EVERY AI CALL THROUGH AN AI GATEWAY + MODEL ARMOR + OPA POLICY PLANE", head_h=28))
    for i, ctl in enumerate(s["controls"][:4]):
        gx = 76 + i * 366
        b.append(_r(gx, 820, 348, 72, 8, "#F8FAFC", GREEN, 1.4))
        b.append(_num_badge(gx + 22, 842, f"0{i + 1}", GREEN, 11.5))
        b.append(_t(gx + 42, 844, ctl["head"], 10.0, 800, INK))
        b.append(_t(gx + 18, 864, ctl["body"], 9.0, 600, SLATE))
        b.append(_t(gx + 18, 882, ctl["stack"], 8.6, 700, GREEN, mono=True))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T56 • PROMPTCANVAS #55 SHADOW AI BUBBLES", RED, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T57 (PromptCanvas #56) — Infographic: Side-by-Side Comparison (Raw Model API vs. Enterprise Agent Runtime)
# ----------------------------------------------------------------------------------------------------------------------
def render_t57(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Top Column Headers (Left: 56..640, Center: 680..920, Right: 960..1544 -> 40px connector gaps!)
    b.append(_card_head(56, 142, 584, 72, RED, "LEFT • RAW FOUNDATION MODEL API (STATELESS INFERENCE)", head_h=26))
    b.append(_t(76, 191, s["left_sub"], 9.1, 700, SLATE))
    b.append(_toggle_switch(514, 174, "OFF", "RUNTIME"))

    b.append(_card_head(680, 142, 240, 72, NAVY, "EVALUATION DIMENSION", head_h=26))
    b.append(_t(800, 192, "5 Production Architecture Pillars", 9.8, 800, NAVY, "middle"))

    b.append(_card_head(960, 142, 584, 72, GREEN, "RIGHT • MANAGED AGENT RUNTIME (VERTEX AGENT ENGINE / LANGGRAPH)", head_h=26))
    b.append(_t(980, 191, s["right_sub"], 9.1, 700, "#065F46"))
    b.append(_toggle_switch(1418, 174, "ON", "RUNTIME"))

    # 5 Comparison Rows with Central Spine Node and OFF vs ON Toggle Switches
    for i, row in enumerate(s["rows"][:5]):
        ry = 228 + i * 124
        col = row["color"]

        # Left Stateless Card (OFF, x=56..640)
        b.append(_r(56, ry, 584, 110, 10, WHITE, "#CBD5E1", 1.5))
        b.append(_r(56, ry, 7, 110, 3.5, RED))
        b.append(_t(76, ry + 26, row["left_title"], 10.8, 800, INK))
        b.append(_toggle_switch(560, ry + 10, "OFF"))
        b.append(_tl(76, ry + 46, _wrap(row["left_desc"], 66, 2), 9.4, 600, SLATE, 14.5))
        b.append(_r(76, ry + 80, 548, 22, 5, "#FEF2F2", "#FECACA", 1))
        b.append(_t(88, ry + 95, f"FAIL MODE: {row['left_fail']}", 8.8, 700, RED, mono=True))

        # Center Dimension Spine Card (x=680..920)
        b.append(_r(680, ry + 10, 240, 90, 10, WHITE, col, 1.8))
        b.append(_num_badge(704, ry + 34, f"0{i + 1}", col, 12))
        b.append(_t(724, ry + 38, row["dim"], 10.2, 800, NAVY))
        b.append(_t(700, ry + 62, row["kpi"], 9.2, 700, col, mono=True))
        b.append(_pill(906, ry + 72, row["tag"], col, size=7.8, h=18, anchor_end=True)[0])

        # 40px Orthogonal Upgrade Flows from Left -> Center -> Right
        b.append(_fl([(640, ry + 55), (678, ry + 55)], RED, phase, 1.3))
        b.append(_fl([(920, ry + 55), (958, ry + 55)], GREEN, phase, 1.3))

        # Right Managed Runtime Card (ON, x=960..1544)
        b.append(_r(960, ry, 584, 110, 10, WHITE, "#86EFAC", 1.6))
        b.append(_r(960, ry, 7, 110, 3.5, GREEN))
        b.append(_t(980, ry + 26, row["right_title"], 10.8, 800, "#065F46"))
        b.append(_toggle_switch(1464, ry + 10, "ON"))
        b.append(_tl(980, ry + 46, _wrap(row["right_desc"], 66, 2), 9.4, 600, INK, 14.5))
        b.append(_r(980, ry + 80, 548, 22, 5, "#ECFDF5", "#A7F3D0", 1))
        b.append(_t(992, ry + 95, f"STACK: {row['right_stack']}", 8.8, 700, "#065F46", mono=True))

    b.append(_r(56, 858, 1488, 46, 10, "#F8FAFC", BLUE, 1.4))
    b.append(_t(78, 886, s["takeaway"], 10.5, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T57 • PROMPTCANVAS #56 SIDE-BY-SIDE TOGGLES", GREEN, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T58 (PromptCanvas #57) — Infographic: Funnel Pipeline Chart (5-Stage Context Compression 1M -> 2k Tokens)
# ----------------------------------------------------------------------------------------------------------------------
def render_t58(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    stages = s["stages"][:5]
    cx = 800.0
    # Tapering funnel widths sized so every stage's 3-line label sits 100% inside the trapezoid walls
    widths = [(520, 468), (468, 416), (416, 364), (364, 312), (312, 264)]

    for i, st in enumerate(stages):
        ty = 148 + i * 124
        th = 104.0
        w_top, w_bot = widths[i]
        w_mid = 0.5 * (w_top + w_bot)
        col = st["color"]

        # Left Architectural Stage Card (x=56..476)
        b.append(_card_head(56, ty, 420, th, col, f"{st['code']} • {st['name']}", head_h=24))
        b.append(_t(74, ty + 43, st["headline"], 10.2, 800, INK))
        b.append(_tl(74, ty + 60, _wrap(st["desc"], 62, 2), 8.9, 600, SLATE, 13.5))
        b.append(_t(74, ty + 94, st["stack"], 8.7, 700, col, mono=True))

        # Horizontal Connector from Left Card right edge (476) directly to the Trapezoid's mid-height wall
        x_mid_L = cx - w_mid / 2.0
        x_mid_R = cx + w_mid / 2.0
        b.append(_fl([(476, ty + 52), (x_mid_L - 2, ty + 52)], col, phase, 1.4))

        # Short Inter-Stage Vertical Progression Arrow only in the gap between consecutive trapezoids
        if i < 4:
            b.append(_fl([(cx, ty + th - 3), (cx, ty + 124 + 3)], col, phase, 1.2, packets=0, solid=True))

        # Center 3D-Frustum Tapering Trapezoid Polygon
        x1L, x1R = cx - w_top / 2.0, cx + w_top / 2.0
        x2L, x2R = cx - w_bot / 2.0, cx + w_bot / 2.0
        y1, y2 = ty + 4, ty + th - 4
        b.append(
            f'<polygon points="{x1L:.1f},{y1:.1f} {x1R:.1f},{y1:.1f} {x2R:.1f},{y2:.1f} {x2L:.1f},{y2:.1f}" '
            f'fill="#FFFFFF" stroke="{col}" stroke-width="2.2" filter="url(#shadow)"/>'
        )
        b.append(
            f'<polygon points="{x1L + 2:.1f},{y1 + 2:.1f} {x1R - 2:.1f},{y1 + 2:.1f} {x2R - 2:.1f},{y2 - 2:.1f} {x2L + 2:.1f},{y2 - 2:.1f}" '
            f'fill="{st["bg"]}" fill-opacity="0.52"/>'
        )
        # Top inner rim ellipse highlight for 3D frustum depth
        b.append(
            f'<ellipse cx="{cx:.1f}" cy="{y1 + 5:.1f}" rx="{w_top / 2 - 10:.1f}" ry="5.5" '
            f'fill="#FFFFFF" fill-opacity="0.78" stroke="{col}" stroke-opacity="0.30" stroke-width="1"/>'
        )
        b.append(_t(cx, ty + 43, st["tokens"], 14.5, 800, NAVY, "middle", mono=True))
        b.append(_t(cx, ty + 64, st["name"], 9.8, 800, col, "middle"))
        b.append(_t(cx, ty + 83, st["ratio"], 8.7, 700, INK, "middle"))

        # Horizontal Connector from Trapezoid's right mid-height wall directly to Right Card left edge (1124)
        b.append(_fl([(x_mid_R + 2, ty + 52), (1122, ty + 52)], col, phase, 1.4))

        # Right Metric & Filter Gate Card (x=1124..1544) — Header band holds gate_title; footer holds latency + discard_pill
        b.append(_card_head(1124, ty, 420, th, col, st["gate_title"], head_h=24))
        b.append(_tl(1140, ty + 42, _wrap(st["gate_desc"], 62, 2), 8.9, 600, SLATE, 13.5))
        b.append(_r(1140, ty + 74, 274, 22, 5, "#F8FAFC", "#CBD5E1", 1))
        b.append(_t(1148, ty + 89, st["latency_cost"], 7.9, 700, NAVY, mono=True))
        b.append(_pill(1532, ty + 75, st["discard_pill"], col, size=8.0, h=20, anchor_end=True)[0])

    # Bottom Output Capsule: Precision Context Window (y=784..904)
    b.append(_card_head(56, 784, 1488, 120, GREEN, "FUNNEL OUTPUT • 99.8% NOISE ELIMINATED -> HIGH-SIGNAL 2,000-TOKEN GEMINI / LLM CONTEXT WINDOW", head_h=28))
    for i, kpi in enumerate(s["outcomes"][:4]):
        kx = 76 + i * 366
        b.append(_r(kx, 824, 348, 68, 8, "#F8FAFC", GREEN, 1.4))
        b.append(_t(kx + 16, 852, kpi["val"], 16, 800, "#065F46", mono=True))
        b.append(_t(kx + 128, 846, kpi["head"], 9.8, 800, INK))
        b.append(_t(kx + 128, 864, kpi["sub"], 8.8, 600, SLATE))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T58 • PROMPTCANVAS #57 3D FUNNEL PIPELINE", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T59 (PromptCanvas #58) — Infographic: Process Checklist (6-Step Autonomous Agent Deployment with ON Switches)
# ----------------------------------------------------------------------------------------------------------------------
def render_t59(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    items = s["items"][:6]
    # Vertical deployment spine on the left (x=94)
    b.append(_fl([(94, 168), (94, 796)], GREEN, phase, 2.0, dash="8 5", packets=2))

    for i, it in enumerate(items):
        ry = 144 + i * 114
        col = it["color"]
        # Left Numbered Spine Node (x=94, r=18 -> right edge 112; card starts at 156 -> 44px connector gap!)
        b.append(_num_badge(94, ry + 48, it["code"], col, 18))
        b.append(_fl([(114, ry + 48), (154, ry + 48)], col, phase, 1.2))

        # Main Checklist Row Card (x=156..1544, h=98)
        b.append(_r(156, ry, 1388, 98, 12, WHITE, col, 1.6))
        b.append(_r(156, ry, 8, 98, 4, col))

        # Title & Description
        b.append(_t(182, ry + 27, f"{it['code']} | {it['title']}", 11.6, 800, INK))
        b.append(_pill(942, ry + 10, it["badge"], col, size=8.4, h=20, anchor_end=True)[0])
        b.append(_tl(182, ry + 47, _wrap(it["desc"], 78, 2), 9.5, 600, SLATE, 14.5))
        b.append(_t(182, ry + 84, f"Google Cloud + OSS: {it['stack']}", 9.0, 700, col, mono=True))

        # Monospace Config Spec Box (x=956..1242)
        b.append(_r(956, ry + 14, 286, 70, 8, "#F8FAFC", "#CBD5E1", 1.2))
        b.append(_t(972, ry + 34, "VERIFIED CONFIG / GATE:", 8.6, 800, SLATE))
        b.append(_t(972, ry + 54, it["config_1"], 9.5, 700, NAVY, mono=True))
        b.append(_t(972, ry + 72, it["config_2"], 9.1, 700, col, mono=True))

        # Right Status Pill + Double Green ON Toggle Switches (x=1262..1526)
        b.append(_r(1262, ry + 14, 264, 70, 8, "#F8FAFC", "#86EFAC", 1.2))
        b.append(_t(1278, ry + 38, "POLICY GATE:", 8.8, 800, "#065F46"))
        b.append(_t(1278, ry + 56, "PROD SLA:", 8.8, 800, "#065F46"))
        b.append(_toggle_switch(1396, ry + 18, "ON", "GATE"))
        b.append(_toggle_switch(1396, ry + 50, "ON", "SLA"))

    # Bottom Takeaway Banner
    b.append(_r(56, 834, 1488, 70, 10, "#F8FAFC", BLUE, 1.5))
    b.append(_r(56, 834, 8, 70, 4, BLUE))
    b.append(_t(82, 860, "DEPLOYMENT CHECKLIST TAKEAWAY • ZERO-TRUST PRODUCTION READINESS", 10.2, 800, BLUE))
    b.append(_t(82, 884, s["takeaway"], 10.2, 700, INK))
    b.append(_pill(1524, 854, "ALL 6 GATES: VERIFIED ON", GREEN, size=9.2, h=24, anchor_end=True)[0])
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T59 • PROMPTCANVAS #58 PROCESS CHECKLIST", GREEN, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T60 (PromptCanvas #59) — Infographic: Timeline & Roadmap (Phased Quarterly Blueprint Q1-Q4 Horizontal Tracks)
# ----------------------------------------------------------------------------------------------------------------------
def render_t60(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    quarters = s["quarters"][:4]
    for i, q in enumerate(quarters):
        qy = 144 + i * 172
        col = q["color"]
        # Full-width Quarter Track Container
        b.append(_r(56, qy, 1488, 156, 12, "#F8FAFC", "#CBD5E1", 1.5))
        b.append(_r(56, qy, 8, 156, 4, col))

        # Left Quarter Header Card (x=76..406 -> 40px gap to Milestone A at 446!)
        b.append(_card_head(76, qy + 14, 330, 128, col, f"{q['quarter']} • {q['phase']}", head_h=25))
        b.append(_t(92, qy + 56, q["theme"], 9.8, 800, INK))
        b.append(_tl(92, qy + 73, _wrap(q["summary"], 46, 3), 8.8, 600, SLATE, 12.2))
        b.append(_t(92, qy + 126, q["kpi"], 8.4, 800, col, mono=True))

        # 40px Horizontal Flow from Quarter Header -> Milestone A
        b.append(_fl([(406, qy + 78), (444, qy + 78)], col, phase, 1.3))

        # Two Milestone Cards per Quarter Track (w=520, gap=40px: Card A 446..966, Card B 1006..1526)
        for j, ms in enumerate(q["milestones"][:2]):
            mx = 446 + j * 560
            b.append(_r(mx, qy + 14, 520, 128, 10, WHITE, col, 1.5))
            b.append(_r(mx, qy + 14, 6, 128, 3, col))
            b.append(_num_badge(mx + 28, qy + 38, ms["code"], col, 13))
            b.append(_t(mx + 50, qy + 42, ms["title"], 10.8, 800, INK))
            b.append(_pill(mx + 504, qy + 25, ms["badge"], col, size=8.2, h=18, anchor_end=True)[0])
            b.append(_tl(mx + 20, qy + 64, _wrap(ms["desc"], 72, 2), 9.2, 600, SLATE, 14.2))
            b.append(_r(mx + 20, qy + 104, 480, 26, 6, "#F8FAFC", "#CBD5E1", 1))
            b.append(_t(mx + 32, qy + 121, f"Deliverable & Stack: {ms['deliverable']}", 9.0, 700, col, mono=True))
            if j == 0:
                b.append(_fl([(mx + 520, qy + 78), (mx + 558, qy + 78)], col, phase, 1.3))

    # Bottom Target Goal Banner (y=836..904)
    b.append(_card_head(56, 836, 1488, 68, NAVY, "TARGET GOAL • 100% PRODUCTION-READY, SELF-HEALING AUTONOMOUS AGENT FLEET BY Q4", head_h=26))
    b.append(_t(78, 886, s["takeaway"], 10.2, 800, INK))
    b.append(_pill(1524, 868, "Q1 -> Q2 -> Q3 -> Q4 VERIFIED", GREEN, size=8.8, h=22, anchor_end=True)[0])
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T60 • PROMPTCANVAS #59 QUARTERLY ROADMAP", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T61 (PromptCanvas #60) — Infographic: Architecture & Topology (Enterprise Agent Runtimes)
# ----------------------------------------------------------------------------------------------------------------------
def render_t61(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Top Ingress Layer: Cloud Load Balancing + Envoy / Apigee AI Gateway (y=142..224)
    b.append(_card_head(420, 142, 760, 82, NAVY, "INGRESS & TRAFFIC CONTROL • GOOGLE CLOUD LOAD BALANCING + ENVOY / APIGEE AI GATEWAY", head_h=25))
    b.append(_t(442, 186, "TLS 1.3 Termination • Cloud Armor WAF • Model Armor Ingress Scan • RFC 8693 OBO Token Validation", 9.8, 700, INK))
    b.append(_t(442, 206, "Routes authenticated agent sessions to Vertex AI Reasoning Engine & Cloud Run Orchestrator", 9.2, 600, SLATE, mono=True))
    b.append(_pill(1162, 176, "p99 INGRESS < 12ms", GREEN, size=8.4, h=20, anchor_end=True)[0])

    # Strict 90-Degree Orthogonal conduits from Ingress to Node 01 (left) and Node 02 (right)
    b.append(_fl([(560, 224), (560, 248), (390, 248), (390, 274)], BLUE, phase, 1.4, label="gRPC / HTTPS", label_dy=0, label_at=0.52))
    b.append(_fl([(1040, 224), (1040, 248), (1210, 248), (1210, 274)], PURPLE, phase, 1.4, label="A2A / REST", label_dy=0, label_at=0.52))

    # Node 01 (Top-Left, x=56..724, y=276..526): 01 | VERTEX AI REASONING ENGINE
    n1 = s["nodes"][0]
    b.append(_card_head(56, 276, 668, 250, BLUE, f"01 • {n1['title']} ({n1['tag']})", head_h=26))
    b.append(_t(78, 324, n1["headline"], 11.0, 800, INK))
    b.append(_tl(78, 344, _wrap(n1["desc"], 78, 2), 9.5, 600, SLATE, 14.5))
    for j, chip in enumerate(n1["subnodes"][:3]):
        cx0 = 78 + j * 212
        b.append(_r(cx0, 386, 198, 76, 8, "#F8FAFC", BLUE, 1.3))
        b.append(_t(cx0 + 14, 408, chip["name"], 9.8, 800, BLUE))
        b.append(_tl(cx0 + 14, 426, _wrap(chip["detail"], 26, 2), 8.8, 600, INK, 13))
    b.append(_r(78, 476, 624, 34, 6, "#F8FAFC", "#CBD5E1", 1.1))
    b.append(_t(92, 497, f"Stack: {n1['stack']}", 9.2, 700, BLUE, mono=True))

    # Node 02 (Top-Right, x=876..1544, y=276..526): 02 | CLOUD RUN AGENT ORCHESTRATOR
    n2 = s["nodes"][1]
    b.append(_card_head(876, 276, 668, 250, PURPLE, f"02 • {n2['title']} ({n2['tag']})", head_h=26))
    b.append(_t(898, 324, n2["headline"], 11.0, 800, INK))
    b.append(_tl(898, 344, _wrap(n2["desc"], 78, 2), 9.5, 600, SLATE, 14.5))
    for j, chip in enumerate(n2["subnodes"][:3]):
        cx0 = 898 + j * 212
        b.append(_r(cx0, 386, 198, 76, 8, "#F8FAFC", PURPLE, 1.3))
        b.append(_t(cx0 + 14, 408, chip["name"], 9.8, 800, PURPLE))
        b.append(_tl(cx0 + 14, 426, _wrap(chip["detail"], 26, 2), 8.8, 600, INK, 13))
    b.append(_r(898, 476, 624, 34, 6, "#F8FAFC", "#CBD5E1", 1.1))
    b.append(_t(912, 497, f"Stack: {n2['stack']}", 9.2, 700, PURPLE, mono=True))

    # Bidirectional Horizontal Flows between Node 01 and Node 02 (152px gap, inline opaque labels)
    b.append(_fl([(724, 368), (874, 368)], BLUE, phase, 1.3, label="gRPC Plan Stream", label_dy=0))
    b.append(_fl([(876, 426), (726, 426)], PURPLE, phase, 1.3, label="Step State Sync", label_dy=0))

    # Orthogonal Cross-Link from Orchestrator (02) to GKE gVisor Sandbox (03) via central corridor x=800
    b.append(_fl([(876, 492), (800, 492), (800, 636), (726, 636)], TEAL, phase, 1.6, label="MCP Tool Dispatch", label_dy=0, label_at=0.5))

    # Vertical Flows from Top Nodes (01, 02) to Bottom Nodes (03, 04) (58px vertical gap)
    b.append(_fl([(390, 526), (390, 582)], GREEN, phase, 1.4, label="CodeAct Exec", label_dy=0))
    b.append(_fl([(1210, 526), (1210, 582)], AMBER, phase, 1.4, label="Vector / State I/O", label_dy=0))

    # Node 03 (Bottom-Left, x=56..724, y=584..836): 03 | GKE gVISOR SANDBOX CLUSTER
    n3 = s["nodes"][2]
    b.append(_card_head(56, 584, 668, 252, GREEN, f"03 • {n3['title']} ({n3['tag']})", head_h=26))
    b.append(_t(78, 634, n3["headline"], 11.0, 800, INK))
    b.append(_tl(78, 654, _wrap(n3["desc"], 78, 2), 9.5, 600, SLATE, 14.5))
    for j, chip in enumerate(n3["subnodes"][:3]):
        cx0 = 78 + j * 212
        b.append(_r(cx0, 696, 198, 76, 8, "#F8FAFC", GREEN, 1.4, 'stroke-dasharray="5 3"'))
        b.append(_t(cx0 + 14, 718, chip["name"], 9.8, 800, "#065F46"))
        b.append(_tl(cx0 + 14, 736, _wrap(chip["detail"], 26, 2), 8.8, 600, INK, 13))
    b.append(_r(78, 786, 624, 34, 6, "#F8FAFC", "#CBD5E1", 1.1))
    b.append(_t(92, 807, f"Stack: {n3['stack']}", 9.2, 700, "#065F46", mono=True))

    # Node 04 (Bottom-Right, x=876..1544, y=584..836): 04 | ALLOYDB + PGVECTOR STATE LAYER
    n4 = s["nodes"][3]
    b.append(_card_head(876, 584, 668, 252, AMBER, f"04 • {n4['title']} ({n4['tag']})", head_h=26))
    b.append(_t(898, 634, n4["headline"], 11.0, 800, INK))
    b.append(_tl(898, 654, _wrap(n4["desc"], 78, 2), 9.5, 600, SLATE, 14.5))
    for j, chip in enumerate(n4["subnodes"][:3]):
        cx0 = 898 + j * 212
        b.append(_r(cx0, 696, 198, 76, 8, "#F8FAFC", AMBER, 1.3))
        b.append(_t(cx0 + 14, 718, chip["name"], 9.8, 800, "#B45309"))
        b.append(_tl(cx0 + 14, 736, _wrap(chip["detail"], 26, 2), 8.8, 600, INK, 13))
    b.append(_r(898, 786, 624, 34, 6, "#F8FAFC", "#CBD5E1", 1.1))
    b.append(_t(912, 807, f"Stack: {n4['stack']}", 9.2, 700, "#B45309", mono=True))

    # Horizontal Flow between Sandbox (03) and AlloyDB (04)
    b.append(_fl([(724, 734), (874, 734)], AMBER, phase, 1.5, label="Artifact SHA Receipt", label_dy=0))

    b.append(_r(56, 852, 1488, 52, 10, "#F8FAFC", BLUE, 1.4))
    b.append(_t(78, 883, s["takeaway"], 10.4, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T61 • PROMPTCANVAS #60 RUNTIME TOPOLOGY", TEAL, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T62 (PromptCanvas #61) — Infographic: Hierarchical Tree (Multi-Agent Supervisor Delegation)
# ----------------------------------------------------------------------------------------------------------------------
def render_t62(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Tier 01: SUPERVISION ZONE (y=142..308)
    b.append(_r(56, 142, 1488, 166, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(74, 154, "ZONE 01 • SUPERVISION & ORCHESTRATION", BLUE, size=8.4, h=20)[0])
    sup = s["supervisor"]
    b.append(_card_head(410, 152, 780, 144, BLUE, f"01 | {sup['title']} ({sup['badge']})", head_h=26))
    b.append(_t(432, 198, sup["headline"], 11.0, 800, INK))
    b.append(_tl(432, 217, _wrap(sup["desc"], 92, 2), 9.4, 600, SLATE, 14.5))
    b.append(_r(432, 256, 736, 26, 6, "#F8FAFC", "#CBD5E1", 1.1))
    b.append(_t(446, 273, f"Routing Policy & Stack: {sup['stack']}", 9.0, 700, BLUE, mono=True))

    # Tier 02: SPECIALIZED WORKER ZONE (y=356..604) — compact zone badge at x=74..276 (clear of x=304 arrow)
    b.append(_r(56, 356, 1488, 248, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(74, 366, "ZONE 02 • ISOLATED WORKER AGENTS", PURPLE, size=8.4, h=20)[0])

    # Strict 90-Degree Orthogonal Manhattan Tree from Supervisor (Tier 01) to 3 Specialist Workers (Tier 02)
    b.append(_fl([(610, 296), (610, 330), (304, 330), (304, 394)], s["workers"][0]["color"], phase, 1.4,
                 label=s["workers"][0]["handoff"], label_dy=0, label_at=0.48))
    b.append(_fl([(800, 296), (800, 394)], s["workers"][1]["color"], phase, 1.4,
                 label=s["workers"][1]["handoff"], label_dy=0, label_at=0.38, packets=0))
    b.append(_fl([(990, 296), (990, 330), (1292, 330), (1292, 394)], s["workers"][2]["color"], phase, 1.4,
                 label=s["workers"][2]["handoff"], label_dy=0, label_at=0.48))

    # Tier 03: UNIFIED RESOURCE & ENVIRONMENT LAYER (y=646..842) — compact zone badge at x=74..278 (clear of x=304 arrow)
    b.append(_r(56, 646, 1488, 196, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(74, 656, "ZONE 03 • SHARED DATA & SANDBOXES", GREEN, size=8.4, h=20)[0])

    for i, wk in enumerate(s["workers"][:3]):
        wx0 = 76 + i * 494
        col = wk["color"]
        b.append(_card_head(wx0, 396, 456, 192, col, f"{wk['code']} | {wk['name']}", head_h=26))
        b.append(_pill(wx0 + 440, 430, wk["status"], col, size=8.2, h=18, anchor_end=True)[0])
        b.append(_t(wx0 + 18, 442, wk["role"], 10.5, 800, INK))
        b.append(_tl(wx0 + 18, 461, _wrap(wk["desc"], 58, 2), 9.3, 600, SLATE, 14.5))
        for j, cap in enumerate(wk["bullets"][:2]):
            b.append(_t(wx0 + 18, 500 + j * 18, f"• {cap}", 9.1, 600, INK))
        b.append(_r(wx0 + 18, 544, 420, 28, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(wx0 + 30, 562, wk["stack"], 8.8, 700, col, mono=True))

        # Orthogonal Vertical Conduit from Worker (Tier 02) down to Resource Pillar (Tier 03) (92px gap!)
        b.append(_fl([(wx0 + 228, 588), (wx0 + 228, 678)], col, phase, 1.3, label=wk["io_label"], label_dy=0, label_at=0.42, packets=0))

    for i, rs in enumerate(s["resources"][:3]):
        rx0 = 76 + i * 494
        col = rs["color"]
        b.append(_card_head(rx0, 680, 456, 146, col, f"03.{i + 1} | {rs['name']}", head_h=25))
        b.append(_t(rx0 + 18, 724, rs["headline"], 10.5, 800, INK))
        b.append(_tl(rx0 + 18, 742, _wrap(rs["desc"], 58, 2), 9.3, 600, SLATE, 14))
        b.append(_r(rx0 + 18, 784, 420, 28, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(rx0 + 30, 802, rs["stack"], 8.8, 700, col, mono=True))

    b.append(_r(56, 854, 1488, 50, 10, "#F8FAFC", BLUE, 1.4))
    b.append(_t(78, 884, s["takeaway"], 10.4, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T62 • PROMPTCANVAS #61 HIERARCHICAL TREE", PURPLE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T63 (PromptCanvas #62) — Infographic: 2x2 Quadrant Matrix (Business Impact vs. Technical Complexity)
# ----------------------------------------------------------------------------------------------------------------------
def render_t63(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Outer Matrix Frame + Vertical & Horizontal Axis Bands
    b.append(_r(116, 142, 1428, 692, 14, "#F8FAFC", "#CBD5E1", 1.6))

    # Left Vertical Axis Banner (BUSINESS IMPACT: LOW -> HIGH)
    b.append(_r(56, 142, 48, 692, 10, NAVY))
    b.append(_t(80, 210, "HIGH", 9.8, 800, "#86EFAC", "middle"))
    b.append(_t(80, 488, "BUSINESS", 9.2, 800, WHITE, "middle"))
    b.append(_t(80, 506, "IMPACT", 9.2, 800, WHITE, "middle"))
    b.append(_t(80, 780, "LOW", 9.8, 800, "#FCA5A5", "middle"))
    b.append(_fl([(80, 740), (80, 240)], GREEN, phase, 2.0, dash="6 4"))

    # Bottom Horizontal Axis Banner (TECHNICAL COMPLEXITY: LOW -> HIGH)
    b.append(_r(116, 844, 1428, 36, 10, NAVY))
    b.append(_t(210, 867, "LOW TECHNICAL COMPLEXITY", 9.8, 800, "#86EFAC"))
    b.append(_t(830, 867, "TECHNICAL & GOVERNANCE COMPLEXITY ->", 10.2, 800, WHITE, "middle"))
    b.append(_t(1450, 867, "HIGH TECHNICAL COMPLEXITY", 9.8, 800, "#93C5FD", "end"))

    # 4 Quadrants (2x2 Grid inside x=116..1544, y=142..834)
    quads = s["quadrants"][:4]
    coords = [
        (134, 158),   # Q1 Top-Left: 01 | QUICK WINS (High Impact / Low Complexity)
        (838, 158),   # Q2 Top-Right: 02 | STRATEGIC BETS (High Impact / High Complexity)
        (134, 498),   # Q3 Bottom-Left: 03 | LOW PRIORITY (Low Impact / Low Complexity)
        (838, 498),   # Q4 Bottom-Right: 04 | HIGH RISK TRAPS (Low Impact / High Complexity)
    ]
    for i, q in enumerate(quads):
        qx, qy = coords[i]
        col = q["color"]
        b.append(_card_head(qx, qy, 688, 322, col, f"{q['code']} | {q['title']} — {q['axis_tag']}", head_h=26))
        b.append(_r(qx + 14, qy + 36, 660, 274, 10, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(qx + 28, qy + 57, q["subtitle"], 10.0, 800, INK))
        b.append(_pill(qx + 662, qy + 42, q["action_badge"], col, size=8.2, h=19, anchor_end=True)[0])

        # 5 Use-Case Pill Cards per Quadrant (arranged in 2 columns: 3 on left, 2 on right + stack summary)
        for j, item in enumerate(q["items"][:5]):
            col_idx = 0 if j < 3 else 1
            row_idx = j if j < 3 else (j - 3)
            ix = qx + 26 + col_idx * 324
            iy = qy + 72 + row_idx * 74
            b.append(_r(ix, iy, 310, 64, 8, WHITE, col, 1.4))
            b.append(_num_badge(ix + 20, iy + 22, str(j + 1), col, 10.5))
            b.append(_t(ix + 38, iy + 24, item["name"], 9.8, 800, INK))
            b.append(_t(ix + 14, iy + 42, item["detail"], 8.8, 600, SLATE))
            b.append(_t(ix + 14, iy + 56, item["metric"], 8.5, 700, col, mono=True))

        # Bottom-right stack recommendation card inside each quadrant (slot 6)
        sx = qx + 350
        sy = qy + 220
        b.append(_r(sx, sy, 310, 64, 8, WHITE, NAVY, 1.4))
        b.append(_t(sx + 14, sy + 22, "RECOMMENDED ARCHITECTURE:", 8.6, 800, col))
        b.append(_t(sx + 14, sy + 40, q["stack_1"], 9.0, 700, INK, mono=True))
        b.append(_t(sx + 14, sy + 55, q["stack_2"], 8.6, 600, SLATE, mono=True))

    # Center Crosshair Badge
    b.append(_r(752, 466, 156, 44, 22, NAVY, WHITE, 2.0))
    b.append(_t(830, 493, "PORTFOLIO MATRIX", 9.8, 800, WHITE, "middle"))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T63 • PROMPTCANVAS #62 2X2 QUADRANT MATRIX", GREEN, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T64 (PromptCanvas #63) — Infographic: Decision Tree Flowchart (Conditional Branching Logic)
# ----------------------------------------------------------------------------------------------------------------------
def render_t64(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Stage Band 01: INGEST & INTENT GATE (y=142..354)
    b.append(_r(56, 142, 1488, 212, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(74, 152, "STAGE 01 • INGEST, SAFETY SCAN & INTENT EVALUATION", BLUE, size=8.6, h=20)[0])

    b.append(_card_head(76, 186, 290, 148, BLUE, "01.A • RECEIVE USER PROMPT", head_h=25))
    b.append(_t(92, 232, "Ingress Request + Session Context", 10.2, 800, INK))
    b.append(_tl(92, 252, _wrap("Scan prompt via Model Armor / Llama Guard; attach trace_id and tenant scope.", 38, 3), 9.2, 600, SLATE, 14))
    b.append(_t(92, 318, "Model Armor • NeMo Guardrails", 8.8, 700, BLUE, mono=True))

    b.append(_fl([(366, 260), (430, 260)], BLUE, phase, 1.3))
    b.append(_card_head(432, 186, 290, 148, NAVY, "01.B • EVALUATE INTENT", head_h=25))
    b.append(_t(448, 232, "Classify Task & Ambiguity Score", 10.2, 800, INK))
    b.append(_tl(448, 252, _wrap("Gemini 3.8 Flash / vLLM classifier checks required parameters & policy bounds.", 38, 3), 9.2, 600, SLATE, 14))
    b.append(_t(448, 318, "Gemini 3.8 Flash • Pydantic", 8.8, 700, NAVY, mono=True))

    b.append(_fl([(722, 260), (806, 260)], BLUE, phase, 1.3))
    b.append(_diamond(916, 260, 106, 56, ["INTENT CLEAR", "& POLICY-SAFE?"], BLUE, 10.0))

    # NO Branch -> Request Clarification (Right, 134px gap with inline opaque NO pill)
    b.append(_fl([(1022, 260), (1156, 260)], AMBER, phase, 1.3, label="NO", label_dy=0, packets=0))
    b.append(_card_head(1158, 186, 366, 148, AMBER, "BRANCH 01.NO • REQUEST CLARIFICATION", head_h=25))
    b.append(_pill(1508, 220, "STATUS: NEEDS_INFO", AMBER, size=8.2, h=18, anchor_end=True)[0])
    b.append(_t(1174, 234, "Return Structured Follow-Up Question", 10.2, 800, INK))
    b.append(_tl(1174, 254, _wrap("Stop tool execution immediately; ask user for missing parameters or reject unsafe prompt.", 48, 3), 9.2, 600, SLATE, 14))
    b.append(_toggle_switch(1174, 300, "ON", "GUARD"))

    # Stage Band 02: TOOL & AUTHORIZATION CHECK (y=380..602) — right-aligned stage pill clear of x=348 vertical arrow
    b.append(_r(56, 380, 1488, 222, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(1524, 390, "STAGE 02 • DYNAMIC TOOL CHECK & RFC 8693 / IAM AUTHORIZATION GATE", PURPLE, size=8.6, h=20, anchor_end=True)[0])

    # YES Branch -> Down to Stage Band 02 Diamond (cx=348, cy=494)
    b.append(_fl([(916, 316), (916, 366), (348, 366), (348, 438)], GREEN, phase, 1.5,
                 label="YES: INTENT VERIFIED", label_dy=0, label_at=0.5))

    b.append(_diamond(348, 494, 106, 54, ["REQUIRES EXTERNAL", "TOOLS / RAG?"], PURPLE, 9.8))
    # NO -> Direct Response (Left, 242 -> 204 = 38px clean horizontal arrow)
    b.append(_fl([(242, 494), (204, 494)], TEAL, phase, 1.2))
    b.append(_r(76, 424, 126, 148, 10, WHITE, TEAL, 1.5))
    b.append(_t(139, 452, "DIRECT", 9.8, 800, TEAL, "middle"))
    b.append(_t(139, 468, "MODEL", 9.8, 800, TEAL, "middle"))
    b.append(_t(139, 484, "ANSWER", 9.8, 800, TEAL, "middle"))
    b.append(_t(139, 512, "In-context", 8.6, 600, SLATE, "middle"))
    b.append(_t(139, 526, "fast path", 8.6, 600, SLATE, "middle"))
    b.append(_pill(91, 544, "FAST_PATH", TEAL, size=7.8, h=18)[0])

    # YES -> Tool Agent -> Auth Check Diamond
    b.append(_fl([(454, 494), (522, 494)], PURPLE, phase, 1.3, label="YES", label_dy=0, packets=0))
    b.append(_card_head(524, 424, 296, 148, PURPLE, "02.A • MOUNT TOP-3 MCP TOOLS", head_h=25))
    b.append(_t(540, 470, "AlloyDB pgvector / Qdrant Tool Router", 10.2, 800, INK))
    b.append(_tl(540, 490, _wrap("Select Top-3 relevant MCP schemas (-93% tokens) and mint scoped OBO JWT.", 39, 3), 9.2, 600, SLATE, 14))
    b.append(_t(540, 554, "MCP • AlloyDB • Qdrant • RFC 8693", 8.8, 700, PURPLE, mono=True))

    b.append(_fl([(820, 494), (888, 494)], PURPLE, phase, 1.3))
    b.append(_diamond(996, 494, 104, 54, ["USER & AGENT", "AUTHORIZED?"], AMBER, 9.8))

    # NO -> Escalate / Access Denied (Right)
    b.append(_fl([(1100, 494), (1156, 494)], RED, phase, 1.3, label="NO", label_dy=0, packets=0))
    b.append(_card_head(1158, 424, 366, 148, RED, "BRANCH 02.NO • ESCALATE / BLOCK ACCESS", head_h=25))
    b.append(_pill(1508, 458, "STATUS: ACCESS_DENIED", RED, size=8.2, h=18, anchor_end=True)[0])
    b.append(_t(1174, 472, "OPA / IAM Policy Violation Logged", 10.2, 800, INK))
    b.append(_tl(1174, 492, _wrap("Agent cannot exceed user RBAC; trigger human approval request in Slack / IAP.", 48, 3), 9.2, 600, SLATE, 14))
    b.append(_toggle_switch(1174, 538, "OFF", "WRITE"))

    # Stage Band 03: SANDBOX EXECUTION & SELF-CORRECTION LOOP (y=624..898) — right-aligned stage pill clear of x=228 arrow
    b.append(_r(56, 624, 1488, 274, 12, "#F8FAFC", "#CBD5E1", 1.5))
    b.append(_pill(1524, 634, "STAGE 03 • SANDBOX EXECUTION, VERIFICATION & SELF-CORRECTION LOOP", GREEN, size=8.6, h=20, anchor_end=True)[0])

    # YES -> Down to Stage Band 03 Card 03.A
    b.append(_fl([(996, 548), (996, 612), (228, 612), (228, 682)], GREEN, phase, 1.5,
                 label="YES: RBAC + OBO VERIFIED", label_dy=0, label_at=0.5))

    b.append(_card_head(76, 684, 304, 152, GREEN, "03.A • EXECUTE IN SANDBOX", head_h=25))
    b.append(_t(92, 728, "GKE gVisor / Cloud Run / OpenHands", 10.2, 800, INK))
    b.append(_tl(92, 748, _wrap("Run tool call or CodeAct script inside isolated container with idempotency key.", 40, 3), 9.2, 600, SLATE, 14))
    b.append(_t(92, 818, "gVisor • OpenHands • Temporal", 8.8, 700, "#065F46", mono=True))

    b.append(_fl([(380, 760), (434, 760)], GREEN, phase, 1.3))
    b.append(_diamond(540, 760, 104, 56, ["PASSES SCHEMA", "& UNIT TESTS?"], GREEN, 9.8))

    # NO -> Self-Correction Loop Card (Center-Right, x=716..1052) with NON-CROSSING top feedback loop back to 03.A!
    b.append(_fl([(644, 760), (714, 760)], RED, phase, 1.3, label="NO", label_dy=0, packets=0))
    b.append(_card_head(716, 684, 336, 152, AMBER, "03.B • SELF-CORRECTION LOOP (MAX 3x)", head_h=25))
    b.append(_pill(1038, 808, "RETRY_LOOP", AMBER, size=8.0, h=18, anchor_end=True)[0])
    b.append(_t(732, 728, "Feed Stderr & Schema Diff Back to Model", 10.2, 800, INK))
    b.append(_tl(732, 748, _wrap("Loop circuit breaker caps retries at 3; sha256(tool+args) prevents duplicate loops.", 44, 3), 9.2, 600, SLATE, 14))
    b.append(_t(732, 818, "Firestore / Redis Dedupe • Promptfoo", 8.8, 700, "#B45309", mono=True))

    # Top feedback return arrow from 03.B (top x=884) back to 03.A (top x=300) — zero crossing with bottom YES line!
    b.append(_fl([(884, 684), (884, 658), (300, 658), (300, 682)], AMBER, phase, 1.8,
                 label="RETRY WITH TRACEBACK (MAX_RETRIES = 3)", label_dy=0, label_at=0.5, packets=0))

    # Bottom YES -> Final Verified Response (Far Right, x=1158..1524) — zero crossing!
    b.append(_fl([(540, 816), (540, 868), (1340, 868), (1340, 838)], GREEN, phase, 1.6,
                 label="YES: EXIT_CODE == 0 (VERIFIED)", label_dy=0, label_at=0.5))
    b.append(_card_head(1158, 684, 366, 152, NAVY, "03.C • DELIVER VERIFIED RESPONSE", head_h=25))
    b.append(_t(1174, 728, "Emit Output + Cryptographic Audit Receipt", 10.4, 800, INK))
    b.append(_tl(1174, 748, _wrap("Commit durable checkpoint to AlloyDB / Firestore and stream verified answer.", 48, 2), 9.2, 600, SLATE, 14))
    b.append(_toggle_switch(1174, 796, "ON", "VERIFIED"))
    b.append(_pill(1508, 800, "STATUS: COMPLETED", GREEN, size=8.4, h=20, anchor_end=True)[0])
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T64 • PROMPTCANVAS #63 DECISION TREE", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T65 (PromptCanvas #64) — Infographic: Feature Matrix Grid (5x4 Multi-Criteria Architectural Evaluation & Scoring)
# ----------------------------------------------------------------------------------------------------------------------
def render_t65(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    cols = s["columns"][:4]
    rows = s["rows"][:5]

    # Top Header Row (y=142..220)
    b.append(_card_head(56, 142, 330, 78, NAVY, "EVALUATION CRITERIA", head_h=25))
    b.append(_t(74, 190, "5 Enterprise Production Requirements", 10.0, 800, INK))
    b.append(_t(74, 207, "Weighted Architectural Rubric (1-5)", 9.0, 600, SLATE))
    b.append(_fl([(386, 181), (412, 181)], NAVY, phase, 1.3))

    for j, c in enumerate(cols):
        cx0 = 414 + j * 284
        col = c["color"]
        b.append(_card_head(cx0, 142, 272, 78, col, f"OPTION 0{j + 1} • {c['tag']}", head_h=25))
        b.append(_t(cx0 + 16, 190, c["name"], 10.6, 800, INK))
        b.append(_t(cx0 + 16, 207, c["sub"], 8.8, 600, SLATE, mono=True))

    # 5 Criteria Rows (y=232..756)
    for i, r in enumerate(rows):
        ry = 232 + i * 104
        rcol = r["color"]
        # Left Criterion Header Card
        b.append(_r(56, ry, 330, 92, 10, WHITE, rcol, 1.5))
        b.append(_r(56, ry, 7, 92, 3.5, rcol))
        b.append(_num_badge(84, ry + 26, f"0{i + 1}", rcol, 11.5))
        b.append(_t(104, ry + 30, r["criterion"], 10.2, 800, INK))
        b.append(_tl(74, ry + 50, _wrap(r["why"], 44, 2), 8.9, 600, SLATE, 14))
        b.append(_fl([(386, ry + 46), (412, ry + 46)], rcol, phase, 1.3))

        # 4 Framework Evaluation Cells
        for j, cell in enumerate(r["cells"][:4]):
            cx0 = 414 + j * 284
            st = cell["status"]
            scol = GREEN if st == "NATIVE" else (AMBER if st == "CONFIG" else RED)
            sbg = "#ECFDF5" if st == "NATIVE" else ("#FFFBEB" if st == "CONFIG" else "#FEF2F2")
            icon = "✓ NATIVE" if st == "NATIVE" else ("◐ PLUGIN / CONFIG" if st == "CONFIG" else "✕ MANUAL DIY")
            b.append(_r(cx0, ry, 272, 92, 10, WHITE, "#CBD5E1", 1.4))
            b.append(_r(cx0 + 12, ry + 10, 134, 22, 11, sbg, scol, 1.2))
            b.append(_t(cx0 + 79, ry + 25, icon, 8.8, 800, scol, "middle"))
            b.append(_pill(cx0 + 258, ry + 11, cell["score"], scol, size=8.2, h=20, anchor_end=True)[0])
            b.append(_tl(cx0 + 14, ry + 48, _wrap(cell["detail"], 38, 2), 8.8, 600, INK, 13.5))
            b.append(_t(cx0 + 14, ry + 82, cell["tech"], 8.5, 700, scol, mono=True))

    # Bottom Overall Fit Score Row (y=758..846)
    b.append(_card_head(56, 758, 330, 86, NAVY, "OVERALL ARCHITECTURAL FIT", head_h=25))
    b.append(_t(74, 804, "Composite Enterprise Readiness Score", 9.8, 800, INK))
    b.append(_t(74, 824, "Target threshold for production >= 4.5 / 5.0", 8.9, 700, GREEN))
    b.append(_fl([(386, 801), (412, 801)], GREEN, phase, 1.3))

    for j, c in enumerate(cols):
        cx0 = 414 + j * 284
        col = c["color"]
        b.append(_r(cx0, 758, 272, 86, 10, WHITE, col, 1.8))
        b.append(_t(cx0 + 16, 786, c["total_score"], 19, 800, col, mono=True))
        b.append(_pill(cx0 + 256, 768, c["verdict"], col, size=8.2, h=20, anchor_end=True)[0])
        # Progress Bar
        b.append(_r(cx0 + 16, 800, 240, 13, 6.5, "#F1F5F9", "#CBD5E1", 1))
        bw = 240 * c["frac"] * _grow(phase)
        b.append(_r(cx0 + 16, 800, bw, 13, 6.5, col))
        b.append(_t(cx0 + 16, 831, c["best_for"], 8.8, 700, INK))

    b.append(_r(56, 858, 1488, 46, 10, "#F8FAFC", BLUE, 1.4))
    b.append(_t(78, 886, s["takeaway"], 10.4, 800, NAVY))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T65 • PROMPTCANVAS #64 FEATURE MATRIX GRID", NAVY, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T66 (PromptCanvas #65) — Infographic: Capability Pyramid (4-Tier AI Capability Evolution)
# ----------------------------------------------------------------------------------------------------------------------
def render_t66(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # s["tiers"] ordered from Top Apex (04 Autonomous) down to Base (01 Raw Inference)
    tiers = s["tiers"][:4]
    cx = 800.0
    # Pyramid tier widths sized so every tier's title, subtitle, and centered pill sit 100% inside the trapezoid walls
    pyr_widths = [
        (248, 332),   # Tier 04 Apex: Autonomous Agent
        (344, 428),   # Tier 03: Multi-Agent Collaboration
        (440, 524),   # Tier 02: Tool Calling & MCP
        (536, 620),   # Tier 01 Base: Foundation Model Raw Inference
    ]

    for i, tr in enumerate(tiers):
        ty = 160 + i * 164
        th = 148.0
        w_top, w_bot = pyr_widths[i]
        w_mid = 0.5 * (w_top + w_bot)
        col = tr["color"]

        # Left Tier Definition Card (x=56..436)
        b.append(_card_head(56, ty, 380, th, col, f"TIER {tr['code']} • {tr['name']}", head_h=25))
        b.append(_t(74, ty + 45, tr["headline"], 10.2, 800, INK))
        b.append(_tl(74, ty + 62, _wrap(tr["desc"], 52, 3), 8.9, 600, SLATE, 12.6))
        for k, bul in enumerate(tr["bullets"][:2]):
            b.append(_t(74, ty + 110 + k * 16, f"• {bul}", 8.9, 700, INK))

        # Conduit from Left Card to Pyramid Layer mid-height wall
        b.append(_fl([(436, ty + 74), (cx - w_mid / 2.0 - 2, ty + 74)], col, phase, 1.4))

        # Center Pyramid Trapezoid Layer
        x1L, x1R = cx - w_top / 2.0, cx + w_top / 2.0
        x2L, x2R = cx - w_bot / 2.0, cx + w_bot / 2.0
        y1, y2 = ty + 6, ty + th - 6
        b.append(
            f'<polygon points="{x1L:.1f},{y1:.1f} {x1R:.1f},{y1:.1f} {x2R:.1f},{y2:.1f} {x2L:.1f},{y2:.1f}" '
            f'fill="#FFFFFF" stroke="{col}" stroke-width="2.2" filter="url(#shadow)"/>'
        )
        b.append(
            f'<polygon points="{x1L + 2:.1f},{y1 + 2:.1f} {x1R - 2:.1f},{y1 + 2:.1f} {x2R - 2:.1f},{y2 - 2:.1f} {x2L + 2:.1f},{y2 - 2:.1f}" '
            f'fill="{tr["bg"]}" fill-opacity="0.50"/>'
        )
        b.append(_num_badge(cx, ty + 38, tr["code"], col, 14))
        b.append(_t(cx, ty + 74, tr["pyr_title"], 10.6, 800, NAVY, "middle"))
        b.append(_t(cx, ty + 93, tr["pyr_sub"], 9.0, 700, col, "middle", mono=True))
        _, pw = _pill(0, 0, tr["badge"], col, size=8.0, h=18)
        b.append(_pill(cx - pw / 2.0, ty + 108, tr["badge"], col, size=8.0, h=18)[0])

        # Conduit from Pyramid Layer mid-height wall to Right Capabilities Card
        b.append(_fl([(cx + w_mid / 2.0 + 2, ty + 74), (1162, ty + 74)], col, phase, 1.4))

        # Right Google Cloud + Open-Source Capabilities Card (x=1164..1544)
        b.append(_card_head(1164, ty, 380, th, NAVY, f"CAPABILITIES & STACK • TIER {tr['code']}", head_h=25))
        for k, cap in enumerate(tr["capabilities"][:3]):
            b.append(_t(1182, ty + 48 + k * 21, f"✓ {cap}", 9.4, 700, INK))
        b.append(_r(1182, ty + 112, 344, 24, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(1194, ty + 128, tr["stack"], 8.8, 700, col, mono=True))

    b.append(_r(56, 834, 1488, 70, 10, "#F8FAFC", BLUE, 1.5))
    b.append(_r(56, 834, 8, 70, 4, BLUE))
    b.append(_t(78, 860, "CAPABILITY EVOLUTION RULE • DO NOT JUMP TO TIER 04 WITHOUT TIER 02 SANDBOXING & TIER 03 CONTRACTS", 10.2, 800, BLUE))
    b.append(_t(78, 884, s["takeaway"], 10.2, 700, INK))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T66 • PROMPTCANVAS #65 CAPABILITY PYRAMID", GREEN, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T67 (PromptCanvas #66) — Infographic: Loop & Cycle (Autonomous Self-Healing Agent Loop)
# ----------------------------------------------------------------------------------------------------------------------
def render_t67(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Centered Torus Ring vertically aligned with the 2x2 Corner Stage Cards (y=148..580 -> center cy=364)
    cx, cy = 800.0, 364.0
    r_outer = 188.0
    r_mid = 152.0

    # Central 4-Quadrant Torus Ring (PromptCanvas #66 signature visual)
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_outer:.1f}" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2.0"/>')
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_mid:.1f}" fill="none" stroke="#E2E8F0" stroke-width="26"/>')
    quad_colors = [BLUE, PURPLE, GREEN, AMBER]
    quad_angles = [(198, 252), (288, 342), (18, 72), (108, 162)]
    quad_labels = ["1. GENERATE", "2. SANDBOX", "3. VERIFY GATE", "4. REPAIR"]
    quad_label_dy = [-16, -16, 16, 16]
    for idx, (a0, a1) in enumerate(quad_angles):
        pts = _arc_pts(cx, cy, r_mid, a0, a1, 20)
        b.append(_flow(pts, quad_colors[idx], phase, quad_labels[idx], 1.6, 3.8, True, 1, dash="10 6", track=True, label_dy=quad_label_dy[idx]))

    # Inner Hub Circle (r=98 -> x=702..898, y=266..462)
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="98" fill="#FFFFFF" stroke="#0F2942" stroke-width="2.2" filter="url(#shadow)"/>')
    b.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="89" fill="none" stroke="#2563EB" stroke-opacity="0.22" stroke-width="1.3" stroke-dasharray="5 4"/>')
    b.append(_t(cx, cy - 22, "AUTONOMOUS", 12.8, 800, NAVY, "middle"))
    b.append(_t(cx, cy - 2, "SELF-HEALING", 12.8, 800, BLUE, "middle"))
    b.append(_t(cx, cy + 18, "AGENT LOOP", 12.8, 800, NAVY, "middle"))
    _, m_pw = _pill(0, 0, "MAX_RETRIES = 3", GREEN, size=8.0, h=18)
    b.append(_pill(cx - m_pw / 2.0, cy + 32, "MAX_RETRIES = 3", GREEN, size=8.0, h=18)[0])

    # 4 Symmetrical Corner Stage Cards (w=452, h=196) around the Torus Ring
    stages = s["stages"][:4]
    card_coords = [
        (56, 148),    # 01 | MODEL GENERATION (Top-Left, x=56..508, y=148..344)
        (1092, 148),  # 02 | SANDBOXED TEST (Top-Right, x=1092..1544, y=148..344)
        (1092, 384),  # 03 | EVALUATION GATE (Mid-Right, x=1092..1544, y=384..580)
        (56, 384),    # 04 | SELF-HEALING LOOP (Mid-Left, x=56..508, y=384..580)
    ]
    # Strict 90-Degree Orthogonal Horizontal & Vertical Loop Connectors
    ring_anchors = [
        ((508, 252), (648, 252)),   # Card 01 -> Torus Top-Left (horizontal 140px)
        ((952, 252), (1090, 252)),  # Torus Top-Right -> Card 02 (horizontal 138px)
        ((1092, 476), (952, 476)),  # Card 03 -> Torus Bottom-Right (horizontal 140px)
        ((648, 476), (510, 476)),   # Torus Bottom-Left -> Card 04 (horizontal 138px)
    ]
    for i, st in enumerate(stages):
        sx, sy = card_coords[i]
        col = st["color"]
        b.append(_card_head(sx, sy, 452, 196, col, f"{st['code']} | {st['title']}", head_h=25))
        b.append(_num_badge(sx + 26, sy + 48, st["code"], col, 13))
        b.append(_t(sx + 48, sy + 52, st["headline"], 10.6, 800, INK))
        b.append(_tl(sx + 18, sy + 72, _wrap(st["desc"], 58, 3), 9.2, 600, SLATE, 14))
        b.append(_r(sx + 18, sy + 124, 416, 28, 6, "#F8FAFC", "#CBD5E1", 1.1))
        b.append(_t(sx + 28, sy + 142, st["artifact"], 8.8, 700, INK, mono=True))
        b.append(_t(sx + 18, sy + 178, f"Stack: {st['stack']}", 8.6, 700, col, mono=True))
        b.append(_pill(sx + 436, sy + 162, st["badge"], col, size=8.0, h=18, anchor_end=True)[0])
        p0, p1 = ring_anchors[i]
        b.append(_fl([p0, p1], col, phase, 1.3))

    # Vertical Stage-to-Stage Connectors on Right (02 -> 03) and Left (04 -> 01) (40px vertical gap!)
    b.append(_fl([(1318, 344), (1318, 382)], PURPLE, phase, 1.2))
    b.append(_fl([(282, 384), (282, 346)], AMBER, phase, 1.2))

    # Strict 90-Degree Orthogonal FAIL -> RETRY Feedback Conduit at y=612 (below Torus bottom y=552 and above y=646 band!)
    b.append(_fl([(1160, 580), (1160, 612), (282, 612), (282, 582)], RED, phase, 1.6,
                 label="FAIL -> TRACEBACK & RETRY FEEDBACK PATH (MAX 3x)", label_dy=0, label_at=0.5))

    # Mid-Lower Band (y=646..760): Left Retry Control Bar (x=56..1060) + Right PASS -> Exit to Production Deploy (x=1092..1544)
    b.append(_card_head(56, 646, 1004, 114, AMBER, "04.B | DETERMINISTIC RETRY CIRCUIT BREAKER & ESCALATION POLICY", head_h=25))
    b.append(_toggle_switch(74, 686, "ACTIVE", "RETRY"))
    retry_steps = [
        ("ATTEMPT 1 / 3 • AUTO-REPAIR", "Feed stderr diff & failing line to Stage 01", BLUE),
        ("ATTEMPT 2 / 3 • AST & SCHEMA", "Run tree-sitter caller & Pydantic check", PURPLE),
        ("ATTEMPT 3 / 3 • HITL ESCALATE", "Freeze loop & page human owner with trace", RED),
    ]
    for r_idx, (r_head, r_sub, r_col) in enumerate(retry_steps):
        rx = 204 + r_idx * 280
        b.append(_r(rx, 680, 266, 66, 8, "#F8FAFC", r_col, 1.3))
        b.append(_t(rx + 14, 704, r_head, 9.2, 800, r_col))
        b.append(_t(rx + 14, 726, r_sub, 8.6, 600, SLATE))

    # PASS -> DEPLOY ON -> EXIT TO DEPLOY Card (x=1092..1544, y=646..760; 66px vertical gap from Card 03 bottom y=580!)
    b.append(_fl([(1360, 580), (1360, 644)], GREEN, phase, 1.2, label="PASS: EXIT_CODE == 0", label_dy=0))
    b.append(_card_head(1092, 646, 452, 114, GREEN, "05 | EXIT TO PRODUCTION DEPLOYMENT (PASS GATE)", head_h=25))
    b.append(_t(1110, 692, "Release Verified Artifact & Signed SHA-256 Receipt", 10.2, 800, "#065F46"))
    b.append(_t(1110, 712, "Cloud Run / Vertex Agent Engine + OpenTelemetry Trace", 8.9, 600, SLATE, mono=True))
    b.append(_toggle_switch(1414, 684, "ON", "DEPLOY"))
    b.append(_pill(1110, 728, "ZERO UNVERIFIED ESCAPES", GREEN, size=8.2, h=18)[0])

    # Bottom Left: Continuous Safeguards (x=56..784, y=778..904)
    b.append(_card_head(56, 778, 728, 124, NAVY, "CONTINUOUS SAFEGUARDS (DETERMINISTIC NON-LLM CONTROLS)", head_h=25))
    for i, sg in enumerate(s["safeguards"][:3]):
        gx = 74 + i * 238
        b.append(_r(gx, 814, 226, 76, 8, "#F8FAFC", "#CBD5E1", 1.3))
        b.append(_num_badge(gx + 18, 832, str(i + 1), BLUE, 9.5))
        b.append(_t(gx + 34, 836, sg["head"], 9.1, 800, INK))
        b.append(_tl(gx + 14, 853, _wrap(sg["body"], 33, 3), 8.2, 600, SLATE, 11.5))

    # Bottom Right: Key Loop Artifacts (x=816..1544, y=778..904)
    b.append(_card_head(816, 778, 728, 124, PURPLE, "KEY SELF-HEALING ARTIFACTS & TELEMETRY", head_h=25))
    for i, ka in enumerate(s["artifacts"][:3]):
        ax = 834 + i * 238
        b.append(_r(ax, 814, 226, 76, 8, "#F8FAFC", "#CBD5E1", 1.3))
        b.append(_num_badge(ax + 18, 832, str(i + 1), PURPLE, 9.5))
        b.append(_t(ax + 34, 836, ka["head"], 9.1, 800, INK))
        b.append(_tl(ax + 14, 853, _wrap(ka["body"], 33, 3), 8.2, 600, SLATE, 11.5))
    return _frame(s["title"], s["subtitle"], s["source"], "\n".join(b), "T67 • PROMPTCANVAS #66 SELF-HEALING LOOP", BLUE, s.get("lineage"))


# ----------------------------------------------------------------------------------------------------------------------
# T68 (PromptCanvas Open Knowledge) — Infographic: Open Knowledge Format Architecture
# ----------------------------------------------------------------------------------------------------------------------
def render_t68(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    # Shares the 4-Tier Vertical Spine + Enclave + Actionable Rule Bar architecture with T53, specialized for Open Knowledge
    return _frame(
        s["title"],
        s["subtitle"],
        s["source"],
        "\n".join(_build_open_knowledge_body(s, phase)),
        "T68 • PROMPTCANVAS OPEN KNOWLEDGE INFOGRAPHIC",
        TEAL,
        s.get("lineage"),
    )


def _build_open_knowledge_body(s: Dict[str, Any], phase: Optional[float]) -> List[str]:
    b: List[str] = []
    tiers = s["tiers"][:4]
    cx = 800.0

    for i, tr in enumerate(tiers):
        ty = 142 + i * 182
        col = tr["color"]
        b.append(_r(56, ty, 1488, 168, 12, "#F8FAFC", "#CBD5E1", 1.5))
        b.append(_r(56, ty, 8, 168, 4, col))
        b.append(_card_head(78, ty + 14, 344, 108, col, f"{tr['num']} • {tr['name']} ({tr['tag']})", head_h=25))
        b.append(_t(94, ty + 56, tr["headline"], 10.4, 800, INK))
        b.append(_tl(94, ty + 72, _wrap(tr["left_desc"], 46, 3), 8.9, 600, SLATE, 12.2))
        b.append(_t(94, ty + 114, tr["stack"], 8.8, 700, col, mono=True))

        b.append(_fl([(422, ty + 68), (650, ty + 68)], col, phase, 1.4))
        b.append(_fl([(950, ty + 68), (1018, ty + 68)], col, phase, 1.4))
        if i < 3:
            b.append(_fl([(cx, ty + 122), (cx, ty + 196)], col, phase, 1.4))

        # Center Format / Schema / Validator / Graph Hub
        b.append(_r(652, ty + 14, 296, 108, 10, WHITE, col, 2.0))
        b.append(_num_badge(678, ty + 38, tr["num"], col, 13))
        b.append(_t(702, ty + 41, tr["center_title"], 10.8, 800, NAVY))
        b.append(_t(702, ty + 57, tr["center_sub"], 9.0, 700, col, mono=True))
        for j, chip in enumerate(tr["chips"][:3]):
            cx0 = 666 + j * 90
            b.append(_r(cx0, ty + 74, 84, 34, 6, "#F8FAFC", col, 1.2))
            b.append(_t(cx0 + 42, ty + 95, chip, 8.6, 800, INK, "middle", mono=True))

        for k, card in enumerate(tr["right_cards"][:2]):
            rx = 1020 + k * 256
            b.append(_r(rx, ty + 14, 244, 108, 10, WHITE, col, 1.5))
            b.append(_r(rx, ty + 14, 6, 108, 3, col))
            b.append(_t(rx + 18, ty + 33, card["title"], 10.0, 800, NAVY))
            b.append(_tl(rx + 18, ty + 49, _wrap(card["body"], 33, 3), 8.8, 600, SLATE, 12.2))
            b.append(_pill(rx + 18, ty + 95, card["badge"], col, size=8.0, h=18)[0])

        b.append(_r(78, ty + 130, 1448, 28, 6, WHITE, "#CBD5E1", 1.3))
        b.append(_r(78, ty + 130, 96, 28, 6, col))
        b.append(_t(126, ty + 148, f"RULE {tr['num']}", 9.5, 800, WHITE, "middle"))
        b.append(_t(188, ty + 148, tr["rule"], 9.8, 700, INK))
        b.append(_pill(1514, ty + 134, tr["metric"], col, size=8.5, h=20, anchor_end=True)[0])

    b.append(_r(56, 872, 1488, 34, 8, "#F8FAFC", TEAL, 1.4))
    b.append(_t(76, 894, s["takeaway"], 10.4, 800, "#065F46"))
    return b


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
        "dynamic": "Horizontal flow conduits advance across Q1-Q4 chevron headers and milestone deliverables01-08.",
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
}

_FALLBACK_RENDERERS_V4: Dict[str, Any] = {
    "T53": render_t53,
    "T54": render_t54,
    "T55": render_t55,
    "T56": render_t56,
    "T57": render_t57,
    "T58": render_t58,
    "T59": render_t59,
    "T60": render_t60,
    "T61": render_t61,
    "T62": render_t62,
    "T63": render_t63,
    "T64": render_t64,
    "T65": render_t65,
    "T66": render_t66,
    "T67": render_t67,
    "T68": render_t68,
}

RENDERERS_V4: Dict[str, Any] = {
    tid: (lambda s, phase=None, _tid=tid, _fb=fn: _render_canonical_pc(_tid, s, phase, _fb))
    for tid, fn in _FALLBACK_RENDERERS_V4.items()
}


def demo_specs_v4() -> Dict[str, Dict[str, Any]]:
    return {
        "T53": {
            "title": "Anatomy of a Self-Improving Agent Setup: Context + Harness + Verification Loop + File Graph",
            "subtitle": "PromptCanvas Blueprint #52: Why a model alone plateaus — and how the 4-tier spine turns every bug into a permanent repository upgrade.",
            "source": "PromptCanvas Blueprint #52 • Keith R. Worfolk & Philipp Schmid • Google Cloud Vertex AI + OpenHands / LangGraph",
            "lineage": "PromptCanvas #52 Anatomy Spine • AGENTS.md + SKILL.md + Sandboxed Loop + MAP.md",
            "tiers": [
                {
                    "num": "01",
                    "name": "CONTEXT",
                    "tag": "PINNED MEMORY",
                    "color": BLUE,
                    "bg": "#EFF6FF",
                    "headline": "What the Agent Reads Before Touching Any File",
                    "left_desc": "Pin compact repo conventions in prefix cache; load heavy task packets on demand instead of bloating every turn.",
                    "stack": "Vertex AI KV Cache • vLLM Prefix Cache • AGENTS.md",
                    "center_title": "TIERED CONTEXT LOADER",
                    "center_sub": "600-tok Pinned + JIT Task Packet",
                    "chips": ["AGENTS.md", "TASK.json", ">2KB->URI"],
                    "right_cards": [
                        {"title": "PERMANENT CONSTITUTION", "body": "AGENTS.md / GEMINI.md holds build commands, invariants, and architecture boundaries.", "badge": "100% CACHE HIT"},
                        {"title": "EPHEMERAL TASK PACKET", "body": "Scoped target files, reproduction test name, and blast-radius constraints for this run.", "badge": "-72% TOKENS"},
                    ],
                    "rule": "Never dump 50 files into the system prompt; pin a 600-token constitution and fetch file slices on demand.",
                    "metric": "97% RULE ADHERENCE AT TURN 30",
                },
                {
                    "num": "02",
                    "name": "HARNESS",
                    "tag": "SKILLS & TOOLS",
                    "color": PURPLE,
                    "bg": "#F5F3FF",
                    "headline": "Deterministic Controls & Progressive SKILL.md Discovery",
                    "left_desc": "Mount only the Top-3 MCP tools per step and enforce loop circuit breakers, cost ceilings, and taint tracking.",
                    "stack": "Google ADK • LangGraph • AlloyDB pgvector • Qdrant",
                    "center_title": "HARNESS CONTROL PLANE",
                    "center_sub": "Top-3 MCP Router + Loop Guard",
                    "chips": ["SKILL.md", ".mcp.json", "OPA Gate"],
                    "right_cards": [
                        {"title": "PROGRESSIVE SKILL.MD", "body": "Load 50-token skill headers at start; expand full instructions only when triggered.", "badge": "-93% SCHEMA TOKENS"},
                        {"title": "LOOP & TAINT GUARDS", "body": "sha256(tool+args) dedupe in Firestore / Redis + OPA capability downgrade on untrusted docs.", "badge": "0 RUNAWAY LOOPS"},
                    ],
                    "rule": "Every non-LLM failure mode (loops, tool bloat, prompt injection) gets a deterministic code guard in the harness.",
                    "metric": "96.4% TOP-3 TOOL ACCURACY",
                },
                {
                    "num": "03",
                    "name": "LOOP",
                    "tag": "CHECK -> FIX -> RECHECK",
                    "color": GREEN,
                    "bg": "#ECFDF5",
                    "headline": "Sandboxed Execution & Pre-Completion Verification Gate",
                    "left_desc": "An agent is never done when it says it is done; completion requires exit_code == 0 inside an isolated sandbox.",
                    "stack": "Cloud Run gVisor • OpenHands (MIT) • pytest / Promptfoo",
                    "center_title": "SELF-HEALING VERIFIER",
                    "center_sub": "Inspect -> Fix -> Recheck Gate",
                    "chips": ["gVisor", "pytest==0", "Receipt"],
                    "right_cards": [
                        {"title": "SANDBOXED CODEACT", "body": "Run edits, unit tests, and linters inside ephemeral gVisor / E2B containers with zero host escape.", "badge": "SYSCALL ISOLATED"},
                        {"title": "ADVERSARIAL REVIEWER", "body": "Independent reviewer agent audits diff against invariants before human merge approval.", "badge": "EXIT_CODE == 0"},
                    ],
                    "rule": "Bounce any failing test traceback or lint error back into the agent loop automatically before alerting a human.",
                    "metric": "0% UNVERIFIED PR ESCAPES",
                },
                {
                    "num": "04",
                    "name": "GRAPH",
                    "tag": "FILE & CALLER MESH",
                    "color": AMBER,
                    "bg": "#FFFBEB",
                    "headline": "Explicit Caller/Callee Dependency Graph & SHA Receipts",
                    "left_desc": "Prevent fix-one-break-three regressions by tracing AST symbol callers and binding memory claims to git blob SHAs.",
                    "stack": "tree-sitter AST • Firestore / PostgreSQL • MAP.md",
                    "center_title": "DEPENDENCY & SHA GRAPH",
                    "center_sub": "AST Callers + Git Blob Receipts",
                    "chips": ["MAP.md", "AST Graph", "Blob SHA"],
                    "right_cards": [
                        {"title": "CALLER / CALLEE TRACE", "body": "Index imports, types, and public signatures via tree-sitter so contract changes test all callers.", "badge": "ZERO BROKEN CALLERS"},
                        {"title": "SHA-BOUND WIKI MEMORY", "body": "Every architectural claim stores (file, lines, blob_sha); stale notes auto-heal on git diff.", "badge": "O(1) STALENESS CHECK"},
                    ],
                    "rule": "Update MAP.md and verify downstream callers whenever a shared interface, schema, or wire contract changes.",
                    "metric": "100% CONTRACT TRACEABILITY",
                },
            ],
            "takeaway": "Takeaway: Context tells the agent where it is; Harness bounds what it can do; Loop proves the fix works; Graph ensures nothing downstream breaks.",
        },
        "T54": {
            "title": "How to Pair a Primary Coding Agent with an Independent Reviewer Agent",
            "subtitle": "PromptCanvas Blueprint #53: Install the apps, mount scoped tools (Files, Skills, MCP, Computer Use), and enforce an adversarial Check-Fix-Recheck loop.",
            "source": "PromptCanvas Blueprint #53 • Google Cloud Gemini Code Assist / ADK + OpenHands / Codex / Claude Code",
            "lineage": "PromptCanvas #53 Process Workflow • 3-Band Builder + Reviewer Pipeline",
            "band1_steps": [
                {"title": "INSTALL PRIMARY AGENT", "tag": "BUILDER", "color": BLUE, "body": "Set up your primary coding agent in the repo workspace with sandboxed terminal & file edit access.", "cmd": "adk init • openhands / claude"},
                {"title": "OPEN PROJECT + AGENTS.MD", "tag": "CONTEXT", "color": PURPLE, "body": "Load the repository constitution (AGENTS.md / GEMINI.md) with deterministic test and lint commands.", "cmd": "cat AGENTS.md • pytest -q"},
                {"title": "ATTACH REVIEWER AGENT", "tag": "CRITIC", "color": AMBER, "body": "Configure an independent reviewer agent with read-only diff access and invariant checklist rules.", "cmd": "profile='reviewer' • zero write"},
                {"title": "LOCK SHARED ARTIFACT BUS", "tag": "CONTRACT", "color": GREEN, "body": "Both agents exchange typed JSON receipts (diff, test stdout, lint status) rather than free-text chat.", "cmd": "Pydantic • Firestore / Postgres"},
            ],
            "band2_tools": [
                {
                    "head": "02.A • FILES + SKILL.MD PACKS",
                    "sub": "Local Repo Context & Domain Playbooks",
                    "color": BLUE,
                    "bullets": [
                        "AGENTS.md / CLAUDE.md permanent rules",
                        "On-demand SKILL.md domain workflows",
                        "tree-sitter AST symbol & caller map",
                    ],
                    "example_label": "PROGRESSIVE SKILL MOUNT:",
                    "example_code": "view_file('skills/db_migration/SKILL.md')",
                },
                {
                    "head": "02.B • SCOPED MCP & PLUGINS",
                    "sub": "Least-Privilege External Connectors",
                    "color": PURPLE,
                    "bullets": [
                        "AlloyDB pgvector / Qdrant Top-3 router",
                        "GitHub PR, Issue & CI status MCP tools",
                        "BigQuery / Postgres read-only schema inspect",
                    ],
                    "example_label": "SCOPED .MCP.JSON ENTRY:",
                    "example_code": "mcp_router.mount_top_k(query, k=3)",
                },
                {
                    "head": "02.C • SANDBOXED COMPUTER USE",
                    "sub": "Headless Browser & UI Verification",
                    "color": TEAL,
                    "bullets": [
                        "Headless Chrome DOM & computed-style checks",
                        "Before & After visual regression capture",
                        "Cloud Run gVisor / E2B container isolation",
                    ],
                    "example_label": "VISUAL PROOF ASSERTION:",
                    "example_code": "puppeteer.verify_zero_overflow(1440, 900)",
                },
            ],
            "band3_loop": [
                {
                    "head": "03.1 • REVIEWER AGENT ADVISES",
                    "role": "Adversarial Diff & Invariant Audit",
                    "color": AMBER,
                    "body": "Reviewer inspects git diff for missing edge cases, broken callers, security leaks, or untested paths.",
                    "gate": "emit ReviewFindings(severity, file, line)",
                },
                {
                    "head": "03.2 • PRIMARY AGENT FIXES",
                    "role": "Targeted Patch + Unit Test Update",
                    "color": BLUE,
                    "body": "Primary agent applies surgical edits addressing every blocker and adds a regression test for the bug.",
                    "gate": "replace_file_content + test_regression.py",
                },
                {
                    "head": "03.3 • SANDBOX RECHECK GATE",
                    "role": "Automated Test + Lint + Visual Verify",
                    "color": PURPLE,
                    "body": "Sandbox executes full unit test suite, typechecker, and headless Chrome geometry assertions.",
                    "gate": "pytest && mypy && ruff -> exit_code == 0",
                },
                {
                    "head": "03.4 • HUMAN DECIDES & MERGES",
                    "role": "30-Second Receipt-Backed Approval",
                    "color": GREEN,
                    "body": "Human reviews the signed verification receipt, before/after screenshots, and clean diff to approve merge.",
                    "gate": "receipt.json verified -> git merge",
                },
            ],
            "takeaway": "Takeaway: Never let the same agent both write the code and grade its own homework — pair a sandboxed Builder with an invariant-checking Reviewer.",
        },
        "T55": {
            "title": "Autonomous Computer-Use Quick-Start Card: 7 Setup Steps & 4 Production Prompts",
            "subtitle": "PromptCanvas Blueprint #54: Configure sandboxed browser/desktop computer use safely, then run four copy-ready workflows with explicit stop gates.",
            "source": "PromptCanvas Blueprint #54 • Google Cloud Vertex AI Computer Use + OpenHands Browser / Playwright Sandbox",
            "lineage": "PromptCanvas #54 Cheat Sheet Card • 7-Step Setup + 4 High-ROI @Browser Workflows",
            "setup_steps": [
                {"title": "Launch Sandboxed Agent Workspace", "detail": "Start Vertex Agent Studio, OpenHands container, or isolated macOS/Linux VM profile.", "pill": "ISOLATED VM", "color": BLUE},
                {"title": "Open Capability & Security Settings", "detail": "Navigate to Agent Runtime -> Tooling & Computer Use permissions panel.", "pill": "SETTINGS", "color": NAVY},
                {"title": "Toggle Computer Use & Browser ON", "detail": "Enable headless Chromium / Playwright and scoped desktop viewport control.", "pill": "ENABLED: ON", "color": GREEN},
                {"title": "Bind Least-Privilege App Allowlist", "detail": "Grant access only to approved domains & local folders; block credential vaults.", "pill": "OPA ALLOWLIST", "color": PURPLE},
                {"title": "Open Fresh Task Session & Trace Log", "detail": "Start a clean trajectory with OpenTelemetry screenshot + DOM action recording.", "pill": "OTEL TRACE", "color": TEAL},
                {"title": "Select High-Reasoning Vision Model", "detail": "Route UI grounding to Gemini 3.8 / Vertex global endpoint with thinkingLevel='HIGH'.", "pill": "RULE 55 HIGH", "color": AMBER},
                {"title": "Run Prompt with Explicit Stop Gate", "detail": "Always specify the target app, output artifact, and the exact mutation where the agent must pause.", "pill": "HITL STOP GATE", "color": RED},
            ],
            "formula_lines": [
                "Open [target app or URL] inside the sandboxed browser,",
                "locate [records / table / UI state matching criteria],",
                "extract and normalize the result into [structured file / sheet],",
                "and STOP for human approval before [submitting / paying / deleting].",
            ],
            "safety_note": "MANDATORY GUARDRAIL: Never grant unmonitored submit rights on financial, prod-DB, or external email forms.",
            "jobs": [
                {
                    "domain": "ACCOUNTS & INVOICE RECONCILIATION",
                    "headline": "Match Vendor PDFs Against ERP Ledger Rows",
                    "app_tag": "@Browser + BigQuery",
                    "color": BLUE,
                    "what_it_does": "Opens billing portal, downloads monthly statements, and flags line-item variances > $50.",
                    "prompt": "@Browser open billing portal, export Q3 invoices to CSV, reconcile against BigQuery ledger_v2, write mismatches to variance_report.md.",
                    "stop_gate": "Pause before approving or scheduling any wire transfer.",
                    "stack": "Vertex Computer Use • Playwright • BigQuery / DuckDB",
                },
                {
                    "domain": "SALES & CRM PIPELINE HYGIENE",
                    "headline": "Compile Grounded Pre-Meeting Account Dossiers",
                    "app_tag": "@Browser + CRM MCP",
                    "color": PURPLE,
                    "what_it_does": "Pulls open tickets, recent product usage, and contract renewal dates into a 1-page brief.",
                    "prompt": "@Browser inspect top 10 renewals due in 30 days, cross-check open P1 bugs in tracker, generate account_briefs.json with citations.",
                    "stop_gate": "Never send outbound customer emails without human sign-off.",
                    "stack": "Google ADK • Salesforce / HubSpot MCP • Firestore",
                },
                {
                    "domain": "COMPETITIVE & DOCS RESEARCH",
                    "headline": "Track Release Notes & Pricing Matrix Changes",
                    "app_tag": "@Browser + Vector DB",
                    "color": GREEN,
                    "what_it_does": "Navigates public changelogs, captures DOM diffs, and updates the internal comparison matrix.",
                    "prompt": "@Browser visit 5 tracked vendor changelog URLs, extract new GA features since last SHA, update competitor_matrix.md with source links.",
                    "stop_gate": "Read-only public web navigation; block file uploads.",
                    "stack": "OpenHands Browser • AlloyDB pgvector • Qdrant",
                },
                {
                    "domain": "UI & VISUAL REGRESSION AUDIT",
                    "headline": "Verify Multi-Viewport Layout & Contrast Gates",
                    "app_tag": "@Browser + Puppeteer",
                    "color": AMBER,
                    "what_it_does": "Renders staging app at desktop/tablet/mobile viewports and checks zero horizontal overflow.",
                    "prompt": "@Browser open localhost:8080 across 1440px, 768px, 375px viewports, assert scrollWidth<=innerWidth, save before/after PNG proof.",
                    "stop_gate": "Block production Cloud Run deploy if any viewport overflows.",
                    "stack": "Headless Chrome • Puppeteer • Cloud Build / GitHub CI",
                },
            ],
            "takeaway": "Takeaway: High-ROI computer use combines a deterministic 4-clause prompt formula (Open -> Find -> Write Artifact -> Stop Before Mutation) with sandboxed browser recording.",
        },
        "T56": {
            "title": "The AI Nobody Signed Off: Perceived IT Footprint (4 Tools) vs. 24 Shadow AI Pipelines",
            "subtitle": "PromptCanvas Blueprint #55: While leadership assumes four approved chatbots are in use, teams run 24 ungoverned browser extensions, bots, and API keys.",
            "source": "PromptCanvas Blueprint #55 • Google Cloud Model Armor + Apigee AI Gateway + LiteLLM / OPA Governance",
            "lineage": "PromptCanvas #55 Bubble Conceptual • Executive Perception vs. 24 Shadow AI Bubbles",
            "exec_caption": "Leadership sees only top-down enterprise licenses — missing bottom-up PLG extensions, personal API keys, and meeting bots.",
            "exec_quotes": [
                {"quote": "\"We only use one approved AI assistant.\"", "reality_gap": "Reality: 24 distinct AI SaaS tools, IDE plugins, and Chrome extensions active weekly.", "risk_tag": "6X TOOL SPRAWL"},
                {"quote": "\"IT & Security vetted our AI integrations.\"", "reality_gap": "Reality: 78% of shadow tools were connected via OAuth personal consent or pasted API keys.", "risk_tag": "OAUTH SHADOW GRANTS"},
                {"quote": "\"We have a written AI Acceptable Use Policy.\"", "reality_gap": "Reality: PDF policies do not intercept PII or source code pasted into unmanaged web prompts.", "risk_tag": "ZERO RUNTIME ENFORCEMENT"},
                {"quote": "\"It is just a read-only productivity chatbot.\"", "reality_gap": "Reality: Autonomous browser plugins and webhook bots are mutating CRM, Jira, and Git repos.", "risk_tag": "UNGOVERNED WRITES"},
            ],
            "clusters": [
                {
                    "name": "CLUSTER A • ENGINEERING & DATA SHADOW AI",
                    "count": "6 Tools",
                    "risk": "SOURCE CODE & DB LEAK",
                    "color": BLUE,
                    "bg": "#EFF6FF",
                    "bubbles": [
                        {"name": "Personal IDE Plugin", "usage": "Autocompletes proprietary repo code", "exposure": "CODE -> EXTERNAL"},
                        {"name": "Paste-to-SQL Bot", "usage": "Production schemas pasted in browser", "exposure": "SCHEMA EXPOSED"},
                        {"name": "PR Review Webhook", "usage": "Third-party app reading private diffs", "exposure": "OAUTH REPO READ"},
                        {"name": "Log Triage Scraper", "usage": "Stack traces with customer tokens", "exposure": "PII IN LOGS"},
                        {"name": "Notebook Copilot", "usage": "CSV customer exports uploaded raw", "exposure": "RAW CSV UPLOAD"},
                        {"name": "Personal API Keys", "usage": "Hardcoded sk-* keys in scripts", "exposure": "UNTRACKED SPEND"},
                    ],
                },
                {
                    "name": "CLUSTER B • MEETINGS, COMMS & EMAIL BOTS",
                    "count": "6 Tools",
                    "risk": "CALL & INBOX CAPTURE",
                    "color": PURPLE,
                    "bg": "#F5F3FF",
                    "bubbles": [
                        {"name": "Auto-Join Note Bot", "usage": "Records external client calls", "exposure": "AUDIO RETENTION"},
                        {"name": "Inbox Auto-Drafter", "usage": "Full Gmail/Outlook read+send scope", "exposure": "OAUTH MAIL.WRITE"},
                        {"name": "Slack Thread Bot", "usage": "Indexes private incident channels", "exposure": "CHANNEL EXPORT"},
                        {"name": "Voice Clone Generator", "usage": "Executive audio samples uploaded", "exposure": "BIOMETRIC VOICE"},
                        {"name": "Slide Deck Instant AI", "usage": "Board strategy bullet points uploaded", "exposure": "M&A / STRATEGY"},
                        {"name": "Browser Sidebar LLM", "usage": "Reads every active DOM page", "exposure": "FULL DOM READ"},
                    ],
                },
                {
                    "name": "CLUSTER C • SALES, REVOPS & SUPPORT",
                    "count": "6 Tools",
                    "risk": "CRM & CUSTOMER PII",
                    "color": AMBER,
                    "bg": "#FFFBEB",
                    "bubbles": [
                        {"name": "Outbound Sequence AI", "usage": "Auto-emails prospects from CSV", "exposure": "BRAND / SPAM RISK"},
                        {"name": "Deal Scoring Plugin", "usage": "Scrapes Salesforce opportunity pages", "exposure": "PIPELINE SCRAPE"},
                        {"name": "Ticket Auto-Responder", "usage": "Replies to support tickets unreviewed", "exposure": "HALLUCINATED SLA"},
                        {"name": "Call Coaching SaaS", "usage": "Ingests customer objection transcripts", "exposure": "EXTERNAL TRAINING"},
                        {"name": "Lead Enrichment Bot", "usage": "Syncs contacts to third-party graph", "exposure": "GDPR / CCPA"},
                        {"name": "RFP Auto-Filler", "usage": "Uploads security questionnaires", "exposure": "SEC DOCS UPLOAD"},
                    ],
                },
                {
                    "name": "CLUSTER D • HR, FINANCE, LEGAL & DESIGN",
                    "count": "6 Tools",
                    "risk": "REGULATED & IP DATA",
                    "color": RED,
                    "bg": "#FEF2F2",
                    "bubbles": [
                        {"name": "Contract Redline Bot", "usage": "Unannounced NDA & MSA uploads", "exposure": "PRIVILEGE WAIVER"},
                        {"name": "Resume Screener AI", "usage": "Grades candidates without bias audit", "exposure": "EU AI ACT / NYC144"},
                        {"name": "FP&A Forecast Helper", "usage": "Quarterly revenue spreadsheets", "exposure": "MNPI EXPOSURE"},
                        {"name": "Brand Image Generator", "usage": "Unlicensed training style prompts", "exposure": "IP / COPYRIGHT"},
                        {"name": "Policy Q&A Custom GPT", "usage": "Internal HR handbook uploaded", "exposure": "PUBLIC LINK LEAK"},
                        {"name": "Vendor Risk Summarizer", "usage": "SOC2 reports uploaded to free tier", "exposure": "NDA VIOLATION"},
                    ],
                },
            ],
            "controls": [
                {"head": "CENTRAL AI GATEWAY", "body": "Replace scattered keys with one governed endpoint & per-team budget.", "stack": "Apigee AI Gateway • LiteLLM Proxy"},
                {"head": "INLINE PII & PROMPT SCAN", "body": "Redact SSNs, secrets, and MNPI before any token leaves the VPC.", "stack": "Google Cloud Model Armor • Presidio"},
                {"head": "SANCTIONED FAST ALTERNATIVES", "body": "Give teams approved Vertex / Workspace & OSS tools so they stop hiding.", "stack": "Vertex AI Agent Engine • OpenHands"},
                {"head": "OAUTH & MCP ALLOWLIST", "body": "Block unapproved OAuth scopes and enforce RFC 8693 OBO tokens.", "stack": "Cloud IAM • OPA • Keycloak"},
            ],
        },
        "T57": {
            "title": "Raw Foundation Model API (OFF) vs. Managed Enterprise Agent Runtime (ON)",
            "subtitle": "PromptCanvas Blueprint #56: Comparing stateless model inference against a fully managed, production-grade agent runtime across five pillars.",
            "source": "PromptCanvas Blueprint #56 • Google Cloud Vertex AI Agent Engine + LangGraph / Temporal / OpenHands",
            "lineage": "PromptCanvas #56 Side-by-Side Comparison • 5-Pillar OFF vs. ON Toggle Matrix",
            "left_sub": "Stateless request/response — app code hand-rolls state, retries & auth.",
            "right_sub": "Managed durable execution, isolated sandboxes, RAG & governance.",
            "rows": [
                {
                    "dim": "STATE PERSISTENCE",
                    "kpi": "0% Lost Sessions",
                    "tag": "DURABILITY",
                    "color": BLUE,
                    "left_title": "Ephemeral In-Memory JSON Array",
                    "left_desc": "Conversation history lives in client RAM; one container restart or timeout loses the entire multi-step workflow.",
                    "left_fail": "Process crash at step 8/10 -> full restart & duplicate side effects",
                    "right_title": "Durable Step Checkpoints & Time-Travel Replay",
                    "right_desc": "Every tool turn commits an atomic state snapshot with idempotency keys so crashed runs resume from the exact step.",
                    "right_stack": "Vertex Agent Sessions • Firestore • LangGraph PostgresSaver • Temporal",
                },
                {
                    "dim": "SECURITY & SANDBOX",
                    "kpi": "100% Syscall Isolation",
                    "tag": "ISOLATION",
                    "color": PURPLE,
                    "left_title": "Host-Process Execution & Raw Prompt Strings",
                    "left_desc": "Generated code or shell commands run in the app's own container with access to environment variables and VPC network.",
                    "left_fail": "One prompt injection reads process.env.DB_PASSWORD or mutates host",
                    "right_title": "Ephemeral gVisor MicroVM Sandboxes + Model Armor",
                    "right_desc": "Code execution runs in zero-trust gVisor / E2B sandboxes with ingress taint scanning and OPA capability downgrading.",
                    "right_stack": "GKE gVisor • Cloud Run Sandbox • Model Armor • OpenHands / E2B",
                },
                {
                    "dim": "GROUNDING & RAG",
                    "kpi": "<15ms Hybrid Retrieval",
                    "tag": "PRECISION",
                    "color": GREEN,
                    "left_title": "Static Prompt Stuffing & Unverified Claims",
                    "left_desc": "Raw documents are dumped into the prompt window until context rot degrades recall and hallucinations slip through.",
                    "left_fail": "180K-token prompt bloat -> 54% rule adherence & ungrounded citations",
                    "right_title": "Hybrid Vector + BM25 Search with SHA Evidence Receipts",
                    "right_desc": "Progressive 5-stage retrieval funnel + cross-encoder reranking binds every sentence to a verified document SHA.",
                    "right_stack": "Vertex AI Search • AlloyDB pgvector • BigQuery • Qdrant",
                },
                {
                    "dim": "GOVERNANCE & HITL",
                    "kpi": "100% Audited Writes",
                    "tag": "CONTROL",
                    "color": AMBER,
                    "left_title": "No Loop Guard, Cost Ceiling, or Approval Gate",
                    "left_desc": "Model can call mutating tools in an infinite retry loop with a shared service-account token and zero human pause.",
                    "left_fail": "Flaky downstream API triggers 400 retries & unauthorized DB writes",
                    "right_title": "Loop Circuit Breaker + RFC 8693 OBO + HITL Interrupts",
                    "right_desc": "Hard step/budget ceilings, sha256(tool+args) loop dedupe, narrowed user OBO tokens, and human sign-off on mutations.",
                    "right_stack": "Google ADK RunConfig • OPA • Cloud IAM • Promptfoo Replay Gate",
                },
                {
                    "dim": "ECOSYSTEM & OPS",
                    "kpi": "-93% Tool Tokens",
                    "tag": "SCALE",
                    "color": TEAL,
                    "left_title": "Hardcoded Function JSONs & Blind Console Logs",
                    "left_desc": "All 85 tool schemas are pasted on every turn; debugging a multi-agent failure requires grepping unstructured text logs.",
                    "left_fail": "35,000 schema tokens burned on Turn 1; zero step-level latency attribution",
                    "right_title": "Dynamic MCP Discovery +A2A Protocol + OpenTelemetry",
                    "right_desc": "Top-3 MCP tool mounting per step, typed Agent2Agent (A2A) task handoffs, and full OpenTelemetry gen_ai span traces.",
                    "right_stack": "Linux Foundation A2A • MCP Router • Cloud Trace • Arize Phoenix",
                },
            ],
            "takeaway": "Takeaway: A foundation model API is a CPU instruction set; an Enterprise Agent Runtime (Vertex Agent Engine / LangGraph + Temporal) is the operating system around it.",
        },
        "T58": {
            "title": "The Context Compression Funnel: Refining 1,000,000 Raw Tokens into a 2,000-Token Precision Window",
            "subtitle": "PromptCanvas Blueprint #57: Five deterministic filtering stages eliminate 99.8% of noise before the reasoning model ever generates a token.",
            "source": "PromptCanvas Blueprint #57 • Google Cloud BigQuery Vector Search + AlloyDB pgvector + Vertex AI Ranking API / Qdrant",
            "lineage": "PromptCanvas #57 3D Funnel Pipeline • 1M -> 250k -> 50k -> 10k -> 2k Tokens",
            "stages": [
                {
                    "code": "01",
                    "name": "RAW CORPUS INGESTION",
                    "tokens": "1,000,000 TOKENS",
                    "ratio": "100% Raw Enterprise Stream",
                    "color": BLUE,
                    "bg": "#DBEAFE",
                    "headline": "Multi-Modal Enterprise Docs, Logs & Tickets",
                    "desc": "Unfiltered stream of PDFs, Git commits, Slack threads, BigQuery tables, and support tickets entering ingestion.",
                    "stack": "Cloud Storage • BigQuery • Apache Kafka / Pub/Sub",
                    "gate_title": "STAGE 01 GATE • CHUNKING & SHA FINGERPRINTING",
                    "discard_pill": "100% INGESTED",
                    "gate_desc": "Split documents on semantic AST/heading boundaries and attach immutable git/GCS blob SHA-256 receipts.",
                    "latency_cost": "Throughput: 50K docs/min • Cost: $0 LLM tokens",
                },
                {
                    "code": "02",
                    "name": "METADATA & ACL PRE-FILTER",
                    "tokens": "250,000 TOKENS",
                    "ratio": "25% Retained • 75% Discarded",
                    "color": PURPLE,
                    "bg": "#EDE9FE",
                    "headline": "Deterministic Tenant, Time & RBAC Pruning",
                    "desc": "Eliminate stale versions, wrong-tenant records, and documents outside the user's OBO security principal before vector math.",
                    "stack": "BigQuery Partition Pruning • AlloyDB Filtered Index • OPA",
                    "gate_title": "STAGE 02 GATE • SQL & RBAC PREDICATE PUSH-DOWN",
                    "discard_pill": "75% DISCARDED",
                    "gate_desc": "Enforce WHERE tenant_id = sub AND is_latest = TRUE AND acl_allow(user_groups) at the storage index layer.",
                    "latency_cost": "Latency: 4 ms SQL index scan • 750k noise tokens dropped",
                },
                {
                    "code": "03",
                    "name": "HYBRID VECTOR + BM25 SEARCH",
                    "tokens": "50,000 TOKENS",
                    "ratio": "5% Retained • 80% of Stage 02 Discarded",
                    "color": TEAL,
                    "bg": "#CCFBF1",
                    "headline": "Dense Semantic Embeddings + Exact Keyword Match",
                    "desc": "Combine HNSW / ScaNN dense vector similarity with BM25 lexical matching via Reciprocal Rank Fusion (RRF).",
                    "stack": "AlloyDB ScaNN / BigQuery Vector • Qdrant / ParadeDB BM25",
                    "gate_title": "STAGE 03 GATE • RECIPROCAL RANK FUSION (TOP-100)",
                    "discard_pill": "80% DISCARDED",
                    "gate_desc": "Catches both conceptual paraphrases (embeddings) and exact error codes, SKUs, or function names (BM25).",
                    "latency_cost": "Latency: 11 ms HNSW + BM25 • Top-100 chunks selected",
                },
                {
                    "code": "04",
                    "name": "CROSS-ENCODER RE-RANKING",
                    "tokens": "10,000 TOKENS",
                    "ratio": "1% Retained • 80% of Stage 03 Discarded",
                    "color": AMBER,
                    "bg": "#FEF3C7",
                    "headline": "Pairwise Query-Chunk Attention Scoring",
                    "desc": "Score full token-level interaction between the user query and each candidate chunk; drop low-relevance distractors.",
                    "stack": "Vertex AI Ranking API • BGE-Reranker-v2 / Cohere Rerank",
                    "gate_title": "STAGE 04 GATE • RELEVANCE THRESHOLD & DEDUPE",
                    "discard_pill": "80% DISCARDED",
                    "gate_desc": "Prune chunks below 0.78 cross-encoder score and collapse near-duplicate overlapping paragraphs.",
                    "latency_cost": "Latency: 28 ms GPU cross-encoder • Top-15 chunks kept",
                },
                {
                    "code": "05",
                    "name": "GEMINI IN-CONTEXT WINDOW",
                    "tokens": "2,000 TOKENS",
                    "ratio": "0.2% Retained • 99.8% Total Compression",
                    "color": GREEN,
                    "bg": "#D1FAE5",
                    "headline": "Citation-Locked Precision Context Assembly",
                    "desc": "Pack the top verified spans with [DOC_ID, LINE_RANGE, BLOB_SHA] headers directly into the reasoning model prompt.",
                    "stack": "Vertex AI Gemini 3.8 • vLLM Prefix Cache • Pydantic",
                    "gate_title": "STAGE 05 GATE • VERBATIM CITATION VERIFIER",
                    "discard_pill": "0.2% PRECISION GOLD",
                    "gate_desc": "Model generates answer with mandatory inline SHA citations; deterministic post-hook verifies every quote exists.",
                    "latency_cost": "TTFT: 190 ms • -98% token cost • 0% unverified",
                },
            ],
            "outcomes": [
                {"val": "500 : 1", "head": "TOKEN COMPRESSION RATIO", "sub": "1,000,000 raw -> 2,000 high-signal tokens"},
                {"val": "-94.2%", "head": "LLM INFERENCE COST & TTFT", "sub": "Sub-250ms Time-To-First-Token at scale"},
                {"val": "+31.4 pts", "head": "MULTI-HOP RECALL GAIN", "sub": "Eliminates Chroma 'Context Rot' distractors"},
                {"val": "100%", "head": "SHA CITATION VERIFICATION", "sub": "Every claim traced to an ACL-checked chunk"},
            ],
        },
        "T59": {
            "title": "Autonomous Agent Production Deployment Checklist: 6 Mandatory Engineering Gates",
            "subtitle": "PromptCanvas Blueprint #58: The step-by-step verification blueprint to deploy and run secure autonomous agent workloads on Google Cloud and open source.",
            "source": "PromptCanvas Blueprint #58 • Google Cloud Vertex AI / GKE gVisor / AlloyDB + OpenHands / LangGraph / Temporal",
            "lineage": "PromptCanvas #58 Process Checklist • 6 Numbered Deployment Gates with Double ON Switches",
            "items": [
                {
                    "code": "01",
                    "title": "DEFINE BOUNDED MISSION, TOOLS & BLAST-RADIUS SCOPE",
                    "badge": "DEFINED",
                    "color": GREEN,
                    "desc": "Lock the agent's explicit objective, allowed read/write tool list, max_steps ceiling, and per-run dollar budget in versioned code.",
                    "stack": "AGENTS.md • Google ADK RunConfig • LangGraph recursion_limit • LiteLLM budget",
                    "config_1": "role: 'incident_triage_v3'",
                    "config_2": "max_steps: 15 • budget: $0.50",
                },
                {
                    "code": "02",
                    "title": "CONFIGURE AI GATEWAY, WAF & PROMPT-INJECTION INGRESS",
                    "badge": "CONNECTED",
                    "color": BLUE,
                    "desc": "Route all traffic through TLS load balancing, rate limits, Model Armor prompt-injection scanning, and RFC 8693 OBO token exchange.",
                    "stack": "Cloud Load Balancing • Apigee / Envoy • Model Armor • Llama Guard 3",
                    "config_1": "api: '/v1/agents:invoke'",
                    "config_2": "model_armor: STRICT_BLOCK",
                },
                {
                    "code": "03",
                    "title": "ESTABLISH SANDBOXED GKE gVISOR / MICROVM EXECUTION CLUSTER",
                    "badge": "ISOLATED",
                    "color": PURPLE,
                    "desc": "Isolate every generated script, shell command, and browser action inside an ephemeral gVisor or E2B microVM with egress allowlists.",
                    "stack": "GKE Autopilot gVisor • Cloud Run Sandbox • OpenHands (MIT) • E2B",
                    "config_1": "runtime: 'gvisor_sandbox'",
                    "config_2": "egress: allowlist_only",
                },
                {
                    "code": "04",
                    "title": "ENABLE DURABLE CHECKPOINTS, IDEMPOTENCY & VECTOR STATE",
                    "badge": "PERSISTENT",
                    "color": TEAL,
                    "desc": "Persist step-level state snapshots, sha256(workflow+step+args) idempotency keys, and SHA-bound RAG embeddings in managed Postgres.",
                    "stack": "AlloyDB pgvector • Firestore • LangGraph PostgresSaver • Temporal",
                    "config_1": "db: 'alloydb_pgvector_ha'",
                    "config_2": "idempotency: sha256_ledger",
                },
                {
                    "code": "05",
                    "title": "INTEGRATE HUMAN-IN-THE-LOOP (HITL) MUTATION GATEWAY",
                    "badge": "GATEWAY",
                    "color": AMBER,
                    "desc": "Physically pause execution and require cryptographic human approval (IAP / Slack signed callback) before any high-blast-radius write.",
                    "stack": "Cloud IAP • OPA Capability Policy • Temporal Signal • Slack BlockKit",
                    "config_1": "mutations: 'hitl_required'",
                    "config_2": "token_ttl: 300s_ephemeral",
                },
                {
                    "code": "06",
                    "title": "DEPLOY WITH GOLDEN TRAJECTORY CI GATE & OTEL TELEMETRY",
                    "badge": "DEPLOYED",
                    "color": NAVY,
                    "desc": "Block Cloud Build / GitHub Actions rollouts unless 100% of golden replay fixtures pass; export OpenTelemetry gen_ai spans in production.",
                    "stack": "Vertex AI Agent Engine • Cloud Run • Promptfoo / Inspect AI • Cloud Trace",
                    "config_1": "golden_replay: '100%_PASS'",
                    "config_2": "status: 'READY_FOR_PROD'",
                },
            ],
            "takeaway": "Every row pairs a human-readable architectural responsibility with a machine-enforced configuration knob — ship only when all 12 GATE and SLA switches are ON.",
        },
        "T60": {
            "title": "Phased Quarterly Blueprint (Q1–Q4): Enterprise Agentic AI Rollout Roadmap",
            "subtitle": "PromptCanvas Blueprint #59: The four-quarter sequence from read-only evaluation harness (Q1) to sandboxed pilots (Q2), stateful RAG (Q3), and autonomous scale (Q4).",
            "source": "PromptCanvas Blueprint #59 • Google Cloud Vertex AI + GKE + AlloyDB + OpenHands / LangGraph / Promptfoo",
            "lineage": "PromptCanvas #59 Quarterly Roadmap • Q1 Discovery -> Q2 Sandbox -> Q3 State -> Q4 Fleet Governance",
            "quarters": [
                {
                    "quarter": "Q1",
                    "phase": "PHASE 1: DISCOVERY & EVAL HARNESS",
                    "theme": "Measure First, Build Second",
                    "color": BLUE,
                    "bg": "#EFF6FF",
                    "summary": "Select Quick-Win use cases from the 2x2 matrix and stand up a deterministic golden-trajectory evaluation suite before writing agent loops.",
                    "kpi": "Exit Gate: 50 Golden Eval Fixtures in CI",
                    "milestones": [
                        {
                            "code": "01",
                            "title": "USE-CASE PORTFOLIO & BLAST-RADIUS AUDIT",
                            "badge": "GOVERNANCE",
                            "desc": "Score candidate workflows on Business Impact vs. Technical Complexity; pick 3 read-only or draft-only Quick Wins for Q1.",
                            "deliverable": "2x2 Portfolio Matrix + AGENTS.md Constitution",
                        },
                        {
                            "code": "02",
                            "title": "GOLDEN TRAJECTORY BENCHMARK & AI GATEWAY",
                            "badge": "EVALUATION",
                            "desc": "Route all LLM calls through a central gateway with cost attribution and build a 50-case regression suite.",
                            "deliverable": "Vertex Eval / Promptfoo CI + Apigee / LiteLLM Proxy",
                        },
                    ],
                },
                {
                    "quarter": "Q2",
                    "phase": "PHASE 2: SECURE SANDBOX PROTOTYPING",
                    "theme": "Isolate Execution & Prove Verification Loops",
                    "color": RED,
                    "bg": "#FEF2F2",
                    "summary": "Move from chat wrappers to tool-using agents running inside ephemeral gVisor sandboxes with pre-completion exit_code == 0 hooks.",
                    "kpi": "Exit Gate: 0 Host Escapes • 95% Tool Accuracy",
                    "milestones": [
                        {
                            "code": "03",
                            "title": "EPHEMERAL gVISOR SANDBOX & CODEACT HARNESS",
                            "badge": "ISOLATION",
                            "desc": "Deploy isolated container sandboxes for code execution, SQL validation, and headless browser tasks with zero host access.",
                            "deliverable": "GKE gVisor / Cloud Run Sandbox + OpenHands / E2B",
                        },
                        {
                            "code": "04",
                            "title": "PROGRESSIVE SKILL.MD & TOP-3 MCP ROUTER",
                            "badge": "TOOL ROUTING",
                            "desc": "Replace static 85-tool schema dumps with semantic Top-3 MCP tool discovery and Model Armor prompt-injection scanning.",
                            "deliverable": "AlloyDB pgvector / Qdrant MCP Router + Model Armor",
                        },
                    ],
                },
                {
                    "quarter": "Q3",
                    "phase": "PHASE 3: DURABLE STATE & PRECISION GROUNDING",
                    "theme": "Eliminate Context Rot & Lost Sessions",
                    "color": AMBER,
                    "bg": "#FFFBEB",
                    "summary": "Add 5-stage context compression (1M -> 2k tokens), durable step checkpoints, idempotency ledgers, and SHA-bound wiki memory.",
                    "kpi": "Exit Gate: 100% Checkpoint Resume • 0 Stale Citations",
                    "milestones": [
                        {
                            "code": "05",
                            "title": "5-STAGE CONTEXT FUNNEL & HYBRID VECTOR RAG",
                            "badge": "GROUNDING",
                            "desc": "Combine metadata ACL pruning, BigQuery/AlloyDB hybrid vector+BM25 search, and cross-encoder reranking with SHA receipts.",
                            "deliverable": "AlloyDB ScaNN + Vertex Ranking API + Blob SHA Receipts",
                        },
                        {
                            "code": "06",
                            "title": "DURABLE CHECKPOINTS & IDEMPOTENCY LEDGER",
                            "badge": "RESILIENCE",
                            "desc": "Snapshot state after every tool turn and enforce sha256(workflow+step+args) deduplication across retries.",
                            "deliverable": "Firestore / LangGraph PostgresSaver + Temporal Workflows",
                        },
                    ],
                },
                {
                    "quarter": "Q4",
                    "phase": "PHASE 4: MULTI-AGENT SCALE & AUTONOMOUS FLEET",
                    "theme": "Typed A2A Contracts & Self-Evolving Harnesses",
                    "color": GREEN,
                    "bg": "#ECFDF5",
                    "summary": "Scale to supervisor-worker fleets using Linux Foundation A2A contracts, RFC 8693 OBO identity, and automated harness patch evolution.",
                    "kpi": "Exit Gate: 99.9% SLA • Autonomous Self-Healing",
                    "milestones": [
                        {
                            "code": "07",
                            "title": "SUPERVISOR-WORKER A2A FLEET & RFC 8693 OBO",
                            "badge": "MULTI-AGENT",
                            "desc": "Connect specialist agents over typed Pydantic blackboards with narrowed On-Behalf-Of user tokens and HITL mutation gates.",
                            "deliverable": "Google ADK + A2A Protocol + Cloud IAM / OPA OBO",
                        },
                        {
                            "code": "08",
                            "title": "CONTINUOUS HARNESS EVOLUTION FROM PROD TRACES",
                            "badge": "SELF-EVOLVING",
                            "desc": "Cluster failed OpenTelemetry trajectories nightly and promote verified SKILL.md / harness patches through the 2-tier snapshot gate.",
                            "deliverable": "Cloud Trace + BigQuery + HarnessEvolve Snapshot Gate",
                        },
                    ],
                },
            ],
            "takeaway": "Takeaway: Teams that succeed in Q4 do not start with 10 autonomous agents in Q1 — they build the evaluation gate (Q1), sandbox (Q2), and durable state plane (Q3) first.",
        },
        "T61": {
            "title": "Enterprise Agent Runtime Topology: Vertex AI + Cloud Run + GKE gVisor + AlloyDB",
            "subtitle": "PromptCanvas Blueprint #60: How Google Cloud and open-source runtime planes separate reasoning, orchestration, sandboxed execution, and vector state.",
            "source": "PromptCanvas Blueprint #60 • Google Cloud Architecture Center + Vertex AI / Cloud Run / GKE gVisor / AlloyDB",
            "lineage": "PromptCanvas #60 Runtime Topology • 4-Plane Separation of Concerns",
            "nodes": [
                {
                    "title": "VERTEX AI REASONING ENGINE",
                    "tag": "COGNITIVE PLANE",
                    "headline": "High-Reasoning Planning, CoT Decomposition & Routing",
                    "desc": "Hosts Gemini 3.8 / frontier reasoning models with pinned prefix caches, structured JSON output schemas, and dynamic thinking budgets.",
                    "subnodes": [
                        {"name": "Prefix KV Cache", "detail": "Pins AGENTS.md & core rubrics (-78% TTFT)"},
                        {"name": "CoT Task Planner", "detail": "Decomposes goals into typed DAG steps"},
                        {"name": "Model Cascade", "detail": "Routes Flash vs. Pro/Argon by complexity"},
                    ],
                    "stack": "Vertex AI Global Endpoint (Rule 55) • vLLM / SGLang • LiteLLM",
                },
                {
                    "title": "CLOUD RUN AGENT ORCHESTRATOR",
                    "tag": "CONTROL PLANE",
                    "headline": "Stateless Event Loop, Loop Guards & Tool Dispatch",
                    "desc": "Executes the deterministic harness state machine: enforces max_steps, checks sha256 loop dedupe, mounts Top-3 MCP tools, and pauses for HITL.",
                    "subnodes": [
                        {"name": "Harness FSM", "detail": "Google ADK / LangGraph state machine"},
                        {"name": "Loop & Budget Guard", "detail": "Blocks 3rd identical failing tool call"},
                        {"name": "A2A & HITL Bus", "detail": "Typed handoffs & Slack/IAP approvals"},
                    ],
                    "stack": "Cloud Run v2 (Knative) • Google ADK (Apache-2.0) • LangGraph • Temporal",
                },
                {
                    "title": "GKE gVISOR SANDBOX CLUSTER",
                    "tag": "EXECUTION PLANE",
                    "headline": "Zero-Trust Ephemeral MicroVM Pods for Untrusted Code & Tools",
                    "desc": "Every code synthesis, bash command, data parser, or headless browser session runs in an isolated gVisor pod with no host kernel access.",
                    "subnodes": [
                        {"name": "Pod 01: CodeAct Exec", "detail": "Runs pytest, mypy, ruff in gVisor"},
                        {"name": "Pod 02: Data & SQL", "detail": "Sandboxed DuckDB / Pandas transforms"},
                        {"name": "Pod 03: Browser / API", "detail": "Headless Chrome & scoped egress calls"},
                    ],
                    "stack": "GKE Autopilot gVisor • OpenHands Runtime (MIT) • E2B MicroVMs",
                },
                {
                    "title": "ALLOYDB + PGVECTOR STATE LAYER",
                    "tag": "STATE & MEMORY PLANE",
                    "headline": "Sub-Millisecond Hybrid Vector RAG, Checkpoints & Audit Ledger",
                    "desc": "Unified transactional + vector database storing durable step checkpoints, idempotency keys, MCP tool embeddings, and SHA-bound knowledge.",
                    "subnodes": [
                        {"name": "ScaNN Vector RAG", "detail": "Top-3 MCP tools & SHA-bound doc chunks"},
                        {"name": "Step Checkpoints", "detail": "Atomic turn snapshots for crash recovery"},
                        {"name": "Idempotency Ledger", "detail": "UNIQUE sha256(workflow+step+args)"},
                    ],
                    "stack": "AlloyDB for PostgreSQL + pgvector • Firestore • Qdrant / Redis",
                },
            ],
            "takeaway": "Takeaway: Never run untrusted code or hold long-lived state inside the reasoning or orchestrator tier — isolate reasoning (01), control (02), sandboxed execution (03), and state (04).",
        },
        "T62": {
            "title": "Hierarchical Multi-Agent Delegation Tree: Supervisor -> Specialist Workers -> Shared Resources",
            "subtitle": "PromptCanvas Blueprint #61: How a Supervisor Agent decomposes complex enterprise goals across isolated worker contexts without context-window bleed.",
            "source": "PromptCanvas Blueprint #61 • Google Cloud ADK + Linux Foundation A2A Protocol + LangGraph Supervisor",
            "lineage": "PromptCanvas #61 Hierarchical Tree • 01 Supervision -> 02a/02b/02c Workers -> 03 Resource Layer",
            "supervisor": {
                "title": "SUPERVISOR ORCHESTRATOR AGENT",
                "badge": "GEMINI 3.8 • RULE 55 HIGH",
                "headline": "Decomposes User Goal into Typed Sub-Tasks & Synthesizes Verified Receipts",
                "desc": "Holds the high-level mission plan and shared Pydantic blackboard; delegates noisy SQL, web research, and code execution to isolated workers.",
                "stack": "Google ADK Supervisor • LangGraph StateGraph • Linux Foundation A2A Task Contracts",
            },
            "workers": [
                {
                    "code": "02a",
                    "name": "SQL & ANALYTICS AGENT",
                    "status": "QUERYING",
                    "color": BLUE,
                    "handoff": "A2A Task: AnalyticsSpec",
                    "role": "Schema-Grounded Warehouse & Metric Retrieval",
                    "desc": "Inspects table metadata, writes read-only SQL with partition pruning, and returns compact summary tables.",
                    "bullets": [
                        "Enforces dry-run byte ceiling (< 1 GB scan)",
                        "Offloads >2KB result sets to GCS/Parquet URI",
                    ],
                    "stack": "BigQuery MCP • AlloyDB • DuckDB / dbt",
                    "io_label": "Read-Only SQL",
                },
                {
                    "code": "02b",
                    "name": "DEEP RESEARCHER AGENT",
                    "status": "FETCHING",
                    "color": PURPLE,
                    "handoff": "A2A Task: ResearchSpec",
                    "role": "5-Stage Funnel Retrieval & Verbatim Citation Check",
                    "desc": "Searches internal knowledge bases and live docs in an isolated sub-window; returns only SHA-cited facts.",
                    "bullets": [
                        "Hybrid vector + BM25 + cross-encoder rerank",
                        "Model Armor scan on all external web pages",
                    ],
                    "stack": "Vertex AI Search • Qdrant • Tavily / Playwright",
                    "io_label": "Vector + Web RAG",
                },
                {
                    "code": "02c",
                    "name": "CODE SYNTHESIS AGENT",
                    "status": "EXECUTING",
                    "color": GREEN,
                    "handoff": "A2A Task: CodeActSpec",
                    "role": "Sandboxed Patch Generation & Unit-Test Proof",
                    "desc": "Writes code, charts, or migrations inside an ephemeral container and iterates until pytest exit_code == 0.",
                    "bullets": [
                        "Zero host filesystem or secret env exposure",
                        "Attaches signed stdout SHA-256 test receipt",
                    ],
                    "stack": "GKE gVisor • OpenHands (MIT) • pytest / ruff",
                    "io_label": "gVisor Syscalls",
                },
            ],
            "resources": [
                {
                    "name": "ENTERPRISE DATA & WAREHOUSE LAYER",
                    "color": BLUE,
                    "headline": "Governed Analytical & Transactional Stores",
                    "desc": "Row-level security, partition-pruned analytical tables, and transactional operational ledgers.",
                    "stack": "Google Cloud BigQuery • AlloyDB • PostgreSQL / ClickHouse",
                },
                {
                    "name": "KNOWLEDGE GRAPH & VECTOR STORE",
                    "color": PURPLE,
                    "headline": "SHA-Bound Embeddings & OpenWiki Memory",
                    "desc": "Versioned enterprise documentation chunks bound to git blob SHAs for O(1) staleness detection.",
                    "stack": "Vertex AI Vector Search • AlloyDB pgvector • Qdrant",
                },
                {
                    "name": "EPHEMERAL gVISOR SANDBOX FLEET",
                    "color": GREEN,
                    "headline": "Isolated MicroVM Containers & Artifact Store",
                    "desc": "Per-task container sandboxes with deterministic test runners and GCS/MinIO artifact pointer storage.",
                    "stack": "GKE Autopilot gVisor • Cloud Run • OpenHands / E2B",
                },
            ],
            "takeaway": "Takeaway: Workers never dump raw 40KB tool outputs into the Supervisor's context — each worker runs in an isolated window and returns a compact, schema-validated A2A receipt.",
        },
        "T63": {
            "title": "Agentic AI Portfolio 2x2 Matrix: Business Impact vs. Technical & Governance Complexity",
            "subtitle": "PromptCanvas Blueprint #62: How engineering leaders classify 20 concrete agent initiatives into Quick Wins (01), Strategic Bets (02), Low Priority (03), and Traps (04).",
            "source": "PromptCanvas Blueprint #62 • Google Cloud Enterprise AI Value Realization Framework + Open-Source Agent Benchmarks",
            "lineage": "PromptCanvas #62 2x2 Quadrant Matrix • 20 Grounded Use Cases Across 4 Quadrants",
            "quadrants": [
                {
                    "code": "01",
                    "title": "QUICK WINS",
                    "axis_tag": "HIGH IMPACT • LOW COMPLEXITY",
                    "color": GREEN,
                    "bg": "#ECFDF5",
                    "subtitle": "Read-only or human-reviewed draft workflows — ship in 2–4 weeks.",
                    "action_badge": "SHIP IN Q1 (PRIORITIZE)",
                    "items": [
                        {"name": "Internal Docs & Runbook RAG", "detail": "Hybrid search with mandatory SHA citations", "metric": "ROI: -65% ticket lookup time"},
                        {"name": "Meeting Action & Decision Extractor", "detail": "Extracts owners & Jira links from transcripts", "metric": "ROI: 4.2 hrs/wk saved per PM"},
                        {"name": "Tier-1 Support Triage & Draft", "detail": "Classifies intent & drafts cited reply for agent", "metric": "ROI: -48% handle time (AHT)"},
                        {"name": "Read-Only SQL Analyst Co-Pilot", "detail": "Generates dry-run verified BigQuery queries", "metric": "ROI: 3x faster ad-hoc BI"},
                        {"name": "PR Diff & Caller Impact Summarizer", "detail": "AST caller trace + invariant review comment", "metric": "ROI: -40% PR review cycle"},
                    ],
                    "stack_1": "Vertex AI Search / AlloyDB pgvector + Gemini Flash",
                    "stack_2": "OSS: Qdrant + LiteLLM + Promptfoo CI Gate",
                },
                {
                    "code": "02",
                    "title": "STRATEGIC BETS",
                    "axis_tag": "HIGH IMPACT • HIGH COMPLEXITY",
                    "color": BLUE,
                    "bg": "#EFF6FF",
                    "subtitle": "Multi-step tool & code execution — requires sandbox, checkpoints & HITL.",
                    "action_badge": "PHASED Q2-Q4 INVESTMENT",
                    "items": [
                        {"name": "Autonomous Bug-Fix & Test Agent", "detail": "Reproduces bug in gVisor & iterates to pytest==0", "metric": "ROI: 42% backlog auto-resolved"},
                        {"name": "SRE Incident Root-Cause & Rollback", "detail": "Correlates OTel traces, logs & recent deploys", "metric": "ROI: -58% MTTR on P1/P2"},
                        {"name": "Legacy Code & SQL Migration Swarm", "detail": "Translates + verifies equivalence on test suites", "metric": "ROI: 5x faster warehouse migration"},
                        {"name": "Multi-System Supply Chain Re-Router", "detail": "Simulates disruption & prepares ERP PO drafts", "metric": "ROI: $2M+ stockout avoidance"},
                        {"name": "Regulated GxP / Clinical Dossier Agent", "detail": "21 CFR Part 11 signed receipts & lineage audit", "metric": "ROI: -50% submission prep time"},
                    ],
                    "stack_1": "Vertex Agent Engine + GKE gVisor + Gemini 3.8 High",
                    "stack_2": "OSS: Google ADK / LangGraph + OpenHands + Temporal",
                },
                {
                    "code": "03",
                    "title": "LOW PRIORITY",
                    "axis_tag": "LOW IMPACT • LOW COMPLEXITY",
                    "color": AMBER,
                    "bg": "#FFFBEB",
                    "subtitle": "Commodity text polishers — delegate to off-the-shelf workspace features.",
                    "action_badge": "BUY / USE WORKSPACE DEFAULT",
                    "items": [
                        {"name": "Generic Email Tone Rewriter", "detail": "Already native in Gmail / Workspace", "metric": "Impact: Marginal custom value"},
                        {"name": "Static FAQ Keyword Chatbot", "detail": "No tool access; frustrates users on real tasks", "metric": "Impact: <12% deflection"},
                        {"name": "Slide Title Brainstormer", "detail": "Single-turn prompt; no custom harness needed", "metric": "Impact: Commodity feature"},
                        {"name": "Internal Acronym Glossary Bot", "detail": "Better solved by a searchable static wiki page", "metric": "Impact: Low daily active use"},
                        {"name": "Calendar Time-Zone Formatter", "detail": "Deterministic 10-line script beats an LLM", "metric": "Impact: Over-engineered"},
                    ],
                    "stack_1": "Use native Google Workspace Gemini side panel",
                    "stack_2": "Do not allocate custom platform engineering headcount",
                },
                {
                    "code": "04",
                    "title": "HIGH-RISK TRAPS",
                    "axis_tag": "LOW IMPACT • HIGH COMPLEXITY",
                    "color": RED,
                    "bg": "#FEF2F2",
                    "subtitle": "Unbounded blast radius or massive cost with negative risk-adjusted ROI.",
                    "action_badge": "AVOID / ARCHITECT OUT",
                    "items": [
                        {"name": "Unbounded Autonomous Email Sender", "detail": "External customer emails with zero HITL gate", "metric": "Risk: Reputational & legal blast"},
                        {"name": "Pre-Training Custom LLM From Scratch", "detail": "$5M+ GPU burn when RAG + LoRA beats it", "metric": "Risk: Negative ROI vs. frontier"},
                        {"name": "Unverified Direct-to-Prod DB Writer", "detail": "Raw LLM SQL DML without sandbox or approval", "metric": "Risk: Irreversible data loss"},
                        {"name": "12-Agent Free-Text Debate Loop", "detail": "Agents chatting without typed schemas or caps", "metric": "Risk: 15x token burn & drift"},
                        {"name": "God-Mode Service Account Agent", "detail": "Single admin key shared across all user queries", "metric": "Risk: Cross-tenant privilege leak"},
                    ],
                    "stack_1": "Replace with: Scoped harness + RFC 8693 OBO + HITL",
                    "stack_2": "Enforce: Accidental Data Loss Prevention Gate",
                },
            ],
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
            "columns": [
                {
                    "tag": "MANAGED + OSS ADK",
                    "name": "Google ADK + Vertex Engine",
                    "sub": "Apache-2.0 SDK + Managed Runtime",
                    "color": GREEN,
                    "total_score": "4.9 / 5.0",
                    "verdict": "ENTERPRISE TARGET",
                    "frac": 0.98,
                    "best_for": "Best for: Regulated enterprise scale & hybrid OSS",
                },
                {
                    "tag": "SELF-HOSTED GRAPH",
                    "name": "LangGraph + PostgresSaver",
                    "sub": "MIT Graph + Temporal / Postgres",
                    "color": BLUE,
                    "total_score": "4.6 / 5.0",
                    "verdict": "STRONG OSS CONTROL",
                    "frac": 0.92,
                    "best_for": "Best for: Custom cyclic graphs on Kubernetes",
                },
                {
                    "tag": "CODEACT SANDBOX",
                    "name": "OpenHands + Docker / E2B",
                    "sub": "MIT CodeActAgent + MicroVMs",
                    "color": PURPLE,
                    "total_score": "4.7 / 5.0",
                    "verdict": "BEST FOR SWE / CODE",
                    "frac": 0.94,
                    "best_for": "Best for: Autonomous coding & repo verification",
                },
                {
                    "tag": "BASELINE ANTI-PATTERN",
                    "name": "Raw Stateless API Wrapper",
                    "sub": "while-loop + JSON tool array",
                    "color": RED,
                    "total_score": "1.8 / 5.0",
                    "verdict": "PROTOTYPE ONLY",
                    "frac": 0.36,
                    "best_for": "Fails in prod: No state, sandbox, or loop guard",
                },
            ],
            "rows": [
                {
                    "criterion": "01 • DATA & STATE PERSISTENCE",
                    "why": "Crash recovery, step-level checkpoints, and exactly-once idempotency ledgers.",
                    "color": BLUE,
                    "cells": [
                        {"status": "NATIVE", "score": "5.0/5", "detail": "Managed session checkpoints + Firestore / AlloyDB state sync.", "tech": "Vertex Sessions • Firestore"},
                        {"status": "NATIVE", "score": "4.8/5", "detail": "Built-in PostgresSaver time-travel & thread checkpointing.", "tech": "LangGraph PostgresSaver"},
                        {"status": "CONFIG", "score": "4.4/5", "detail": "EventStream trajectory log persisted to disk or S3/GCS.", "tech": "EventStream JSONL + Redis"},
                        {"status": "MANUAL", "score": "1.5/5", "detail": "In-memory messages[] array lost on any process restart.", "tech": "RAM dict (ephemeral)"},
                    ],
                },
                {
                    "criterion": "02 • SYSTEM & SYSCALL ISOLATION",
                    "why": "Zero-trust container sandboxing for generated code, bash, and browser actions.",
                    "color": PURPLE,
                    "cells": [
                        {"status": "NATIVE", "score": "4.9/5", "detail": "GKE gVisor / Cloud Run microVM sandboxes + Model Armor.", "tech": "GKE gVisor • Model Armor"},
                        {"status": "CONFIG", "score": "4.2/5", "detail": "Requires pairing with external E2B or gVisor runner pods.", "tech": "External E2B / K8s Pod"},
                        {"status": "NATIVE", "score": "5.0/5", "detail": "Purpose-built sandboxed Docker / gVisor CodeAct runtime.", "tech": "OpenHands Sandbox • E2B"},
                        {"status": "MANUAL", "score": "1.0/5", "detail": "Runs subprocess/exec directly inside the host web server.", "tech": "Host process (unsafe)"},
                    ],
                },
                {
                    "criterion": "03 • HUMAN-IN-THE-LOOP (HITL) GATE",
                    "why": "Pause-and-resume interrupts before high-blast-radius writes with OBO identity.",
                    "color": AMBER,
                    "cells": [
                        {"status": "NATIVE", "score": "4.9/5", "detail": "ADK tool confirmation hooks + Cloud IAP & RFC 8693 OBO.", "tech": "ADK before_tool_callback"},
                        {"status": "NATIVE", "score": "4.9/5", "detail": "First-class interrupt_before / interrupt_after node breakpoints.", "tech": "LangGraph interrupt()"},
                        {"status": "NATIVE", "score": "4.6/5", "detail": "Confirmation mode pauses before mutating bash/browser actions.", "tech": "SecurityAnalyzer confirm"},
                        {"status": "MANUAL", "score": "2.0/5", "detail": "Must hand-roll webhook polling and state serialization.", "tech": "Custom polling loop"},
                    ],
                },
                {
                    "criterion": "04 • LONG-TERM SESSION MEMORY",
                    "why": "Prefix KV caching, context compaction, and SHA-bound evidence receipts.",
                    "color": GREEN,
                    "cells": [
                        {"status": "NATIVE", "score": "4.9/5", "detail": "Vertex context caching + AlloyDB pgvector & Memory Bank.", "tech": "Vertex KV Cache • AlloyDB"},
                        {"status": "CONFIG", "score": "4.6/5", "detail": "LangMem + pgvector / Qdrant store with custom SHA tags.", "tech": "LangMem • pgvector"},
                        {"status": "NATIVE", "score": "4.7/5", "detail": "Condenser compactor + repo microagents (.openhands/microagents).", "tech": "OpenHands Condenser"},
                        {"status": "MANUAL", "score": "2.0/5", "detail": "Unbounded append-only prompt until context rot hits at turn 12.", "tech": "Raw string append"},
                    ],
                },
                {
                    "criterion": "05 • MULTI-AGENT ORCHESTRATION SCALE",
                    "why": "Typed A2A handoffs, dynamic Top-3 MCP routing, and OpenTelemetry tracing.",
                    "color": TEAL,
                    "cells": [
                        {"status": "NATIVE", "score": "5.0/5", "detail": "Native Linux Foundation A2A protocol + Cloud Trace OTel spans.", "tech": "A2A Protocol • Cloud Trace"},
                        {"status": "NATIVE", "score": "4.7/5", "detail": "Subgraph composition & supervisor routing with LangSmith/OTel.", "tech": "LangGraph Subgraphs • OTel"},
                        {"status": "NATIVE", "score": "4.7/5", "detail": "Multi-agent delegation across specialist CodeAct microagents.", "tech": "AgentDelegateAction"},
                        {"status": "MANUAL", "score": "2.5/5", "detail": "Brittle prompt-chained functions with 42% constraint loss.", "tech": "Ad-hoc function calls"},
                    ],
                },
            ],
            "takeaway": "Takeaway: Combine Google ADK / LangGraph (for durable state & HITL) with OpenHands / GKE gVisor (for sandboxed CodeAct verification) on Vertex AI & AlloyDB.",
        },
        "T66": {
            "title": "The 4-Tier Agent Capability Pyramid: From Raw Inference to Autonomous Self-Healing",
            "subtitle": "PromptCanvas Blueprint #65: The architectural evolution of enterprise AI systems from stateless prompting (Tier 01) to goal-driven autonomy (Tier 04).",
            "source": "PromptCanvas Blueprint #65 • Google Cloud Agent Architecture Guide + Vertex AI / GKE / AlloyDB + OpenHands / LangGraph",
            "lineage": "PromptCanvas #65 Capability Pyramid • 01 Base -> 02 Tools -> 03 Multi-Agent -> 04 Autonomous Apex",
            "tiers": [
                {
                    "code": "04",
                    "name": "AUTONOMOUS AGENT",
                    "badge": "GOAL-DRIVEN APEX",
                    "color": GREEN,
                    "bg": "#D1FAE5",
                    "headline": "Self-Directed Planning, Sandboxed Verification & Self-Healing",
                    "desc": "Operates on open-ended engineering or business objectives, grades its own work against deterministic verifiers, and repairs failures.",
                    "bullets": [
                        "Pre-completion exit_code == 0 sandbox verification loop",
                        "Continuous harness evolution from production OTel traces",
                    ],
                    "pyr_title": "04 • AUTONOMOUS APEX",
                    "pyr_sub": "Self-Healing + Verifier Gate",
                    "capabilities": [
                        "Autonomous test-driven self-healing loop",
                        "Durable multi-hour execution with HITL gates",
                        "Cryptographic SHA-256 verification receipts",
                    ],
                    "stack": "Vertex Agent Engine • OpenHands (MIT) • Temporal",
                },
                {
                    "code": "03",
                    "name": "MULTI-AGENT COLLABORATION",
                    "badge": "COOPERATIVE FLEET",
                    "color": AMBER,
                    "bg": "#FEF3C7",
                    "headline": "Supervisor-Worker Delegation & Typed A2A Contracts",
                    "desc": "Coordinates specialized worker agents (SQL, Research, Code, Security) across isolated context windows via a shared typed blackboard.",
                    "bullets": [
                        "Manager-worker dynamic routing with zero context bleed",
                        "Adversarial Builder + Reviewer agent verification",
                    ],
                    "pyr_title": "03 • MULTI-AGENT FLEET",
                    "pyr_sub": "A2A Contracts + Blackboard",
                    "capabilities": [
                        "Linux Foundation Agent2Agent (A2A) protocol",
                        "Shared Pydantic + AlloyDB / Firestore blackboard",
                        "RFC 8693 On-Behalf-Of (OBO) delegated identity",
                    ],
                    "stack": "Google ADK • LangGraph • CrewAI • AlloyDB",
                },
                {
                    "code": "02",
                    "name": "TOOL CALLING & WORKFLOWS",
                    "badge": "INTERACTIVE",
                    "color": RED,
                    "bg": "#FEE2E2",
                    "headline": "Dynamic MCP Discovery, Hybrid RAG & Sandboxed Execution",
                    "desc": "Connects the foundation model to live databases, APIs, code runners, and browsers through least-privilege protocols.",
                    "bullets": [
                        "Top-3 semantic MCP tool mounting (-93% schema tokens)",
                        "5-stage context compression funnel (1M -> 2k tokens)",
                    ],
                    "pyr_title": "02 • TOOL & MCP LAYER",
                    "pyr_sub": "Top-3 MCP + gVisor Sandbox",
                    "capabilities": [
                        "Model Context Protocol (MCP) + Top-3 vector router",
                        "GKE gVisor / E2B microVM code & browser sandbox",
                        "Hybrid Vector + BM25 search with SHA citations",
                    ],
                    "stack": "GKE gVisor • BigQuery / Qdrant • Model Armor",
                },
                {
                    "code": "01",
                    "name": "BASE FOUNDATION MODEL",
                    "badge": "RAW INFERENCE",
                    "color": BLUE,
                    "bg": "#DBEAFE",
                    "headline": "Stateless Reasoning, Chain-of-Thought & Multimodal Tokens",
                    "desc": "Standard foundation model inference operating purely on in-context prompt tokens without external state or tool side effects.",
                    "bullets": [
                        "Chain-of-Thought (CoT) & test-time compute scaling",
                        "Prefix KV caching & speculative decoding goodput",
                    ],
                    "pyr_title": "01 • BASE FOUNDATION MODEL",
                    "pyr_sub": "Gemini 3.8 / 4 Argon • vLLM",
                    "capabilities": [
                        "Multimodal text, code, audio & vision understanding",
                        "Structured JSON schema output enforcement",
                        "Prefix-aware KV cache routing & FlashAttention-3",
                    ],
                    "stack": "Vertex AI Gemini (Rule 55) • vLLM / SGLang • DeepSeek-R1",
                },
            ],
            "takeaway": "Each pyramid tier depends on the deterministic guarantees of the tier below it — never deploy Tier 04 autonomy on top of an unsandboxed Tier 01 prompt wrapper.",
        },
        "T67": {
            "title": "The Autonomous Self-Healing Agent Loop: Generate -> Sandbox Test -> Gate -> Repair",
            "subtitle": "PromptCanvas Blueprint #66: How production agents turn runtime failures into deterministic retries without human babysitting or runaway loops.",
            "source": "PromptCanvas Blueprint #66 • Google Cloud Vertex AI + GKE gVisor + OpenHands CodeAct + Promptfoo / pytest",
            "lineage": "PromptCanvas #66 Loop & Cycle • 4-Quadrant Torus Ring with PASS (Deploy ON) & FAIL (Retry ACTIVE) Gates",
            "stages": [
                {
                    "code": "01",
                    "title": "MODEL GENERATION",
                    "badge": "PLAN & PATCH",
                    "color": BLUE,
                    "headline": "Gemini 3.8 Synthesizes Candidate Code or Tool Action",
                    "desc": "Reads pinned AGENTS.md constitution, task brief, and any prior failure traceback to propose a minimal, targeted patch or tool call.",
                    "artifact": "Output: CandidatePatch(diff, target_tests, rationale)",
                    "stack": "Vertex AI Gemini 3.8 (Rule 55) • vLLM • Pydantic",
                },
                {
                    "code": "02",
                    "title": "SANDBOXED TEST EXECUTION",
                    "badge": "gVISOR ISOLATED",
                    "color": PURPLE,
                    "headline": "Execute Task Inside Zero-Trust Ephemeral MicroVM",
                    "desc": "Applies the candidate patch inside an isolated GKE gVisor / OpenHands container with no production network or host secret access.",
                    "artifact": "Output: SandboxObservation(exit_code, stdout, stderr_tail)",
                    "stack": "GKE Autopilot gVisor • Cloud Run • OpenHands / E2B",
                },
                {
                    "code": "03",
                    "title": "DETERMINISTIC EVALUATION GATE",
                    "badge": "PASS / FAIL GATE",
                    "color": GREEN,
                    "headline": "Automated Unit Tests, Schema Checks & Invariant Audit",
                    "desc": "Grades execution against deterministic exit_code == 0, JSON schema validation, AST caller checks, and golden regression fixtures.",
                    "artifact": "Gate: exit_code == 0 AND invariants_passed == True",
                    "stack": "pytest • mypy • ruff • Promptfoo / Vertex Eval",
                },
                {
                    "code": "04",
                    "title": "SELF-HEALING REPAIR LOOP",
                    "badge": "AUTO-REPAIR",
                    "color": AMBER,
                    "headline": "Distill Failure Traceback into a Targeted Repair Strategy",
                    "desc": "Extracts the exact failing assertion, line number, and stderr diff; checks loop circuit breaker (< 3 retries) and feeds back to Stage 01.",
                    "artifact": "Feedback: RepairContext(attempt=2/3, root_cause, diff_hint)",
                    "stack": "Google ADK LoopGuard • Firestore / Redis Dedupe",
                },
            ],
            "safeguards": [
                {"head": "MAX RETRY CIRCUIT BREAKER", "body": "Hard cap of 3 repair iterations + sha256(tool+args) dedupe stops infinite loops."},
                {"head": "ZERO-TRUST gVISOR SANDBOX", "body": "All candidate code and tests execute in ephemeral microVMs with scoped egress."},
                {"head": "DETERMINISTIC EXIT GATE", "body": "Only compiler/pytest exit_code == 0 unlocks the green DEPLOY ON path."},
            ],
            "artifacts": [
                {"head": "STDERR FAILURE RECEIPT", "body": "Trimmed traceback & failing assertion fed back into Stage 01 as high-signal context."},
                {"head": "INVARIANT TARGET SPEC", "body": "Acceptance test name, latency SLO, and schema contract defining task success."},
                {"head": "GRACEFUL HITL ESCALATION", "body": "If attempt 3/3 fails, attaches full diagnostic bundle and pages human owner."},
            ],
        },
        "T68": {
            "title": "Open Knowledge Format Architecture: Open Formats + Schema Harness + Validation Loop + Graph",
            "subtitle": "PromptCanvas Open Knowledge Blueprint: Why agent memory must live in open, schema-validated, SHA-linked files rather than opaque proprietary blobs.",
            "source": "PromptCanvas Open Knowledge Format Infographic • LangChain OpenWiki + Google Cloud BigQuery / AlloyDB + Pydantic / JSON Schema",
            "lineage": "PromptCanvas Open Knowledge Spine • LangChain OpenWiki",
            "tiers": [
                {
                    "num": "01",
                    "name": "OPEN FORMATS",
                    "tag": "PORTABLE STORAGE",
                    "color": BLUE,
                    "bg": "#EFF6FF",
                    "headline": "Human-Readable, Git-Diffable & Columnar Open Standards",
                    "left_desc": "Store instructions, memory notes, and trajectories in open formats that any agent framework, IDE, or SQL engine can inspect.",
                    "stack": "Markdown + YAML • JSONL • Apache Parquet / Iceberg",
                    "center_title": "OPEN FORMAT INGEST",
                    "center_sub": "Git-Native + Columnar Lakehouse",
                    "chips": [".md+YAML", ".jsonl", ".parquet"],
                    "right_cards": [
                        {"title": "GIT-NATIVE DOCS & SKILLS", "body": "AGENTS.md, SKILL.md, and OpenWiki notes use UTF-8 Markdown with typed YAML frontmatter.", "badge": "100% GIT DIFFABLE"},
                        {"title": "COLUMNAR TRAJECTORY LOGS", "body": "Execution traces export to JSONL and BigQuery / Iceberg Parquet for fast SQL analytics.", "badge": "ZERO VENDOR LOCK"},
                    ],
                    "rule": "Never trap institutional agent knowledge inside a closed SaaS database that cannot be grepped, diffed, or versioned in Git.",
                    "metric": "100% PORTABLE ACROSS FRAMEWORKS",
                },
                {
                    "num": "02",
                    "name": "SCHEMA HARNESS",
                    "tag": "TYPED CONTRACTS",
                    "color": PURPLE,
                    "bg": "#F5F3FF",
                    "headline": "Strict Compile-Time & Runtime Schema Enforcement",
                    "left_desc": "Every markdown frontmatter block, MCP tool payload, and memory claim must validate against a versioned schema contract.",
                    "stack": "Pydantic v2 • JSON Schema Draft 2020-12 • Protobuf",
                    "center_title": "SCHEMA VALIDATOR",
                    "center_sub": "Frontmatter + Payload Contracts",
                    "chips": ["Pydantic", "JSONSchema", "SHACL"],
                    "right_cards": [
                        {"title": "TYPED FRONTMATTER & CLAIMS", "body": "Enforce required fields (id, owner, source_sha, line_range, updated_at) on every note.", "badge": "0 UNTYPED NOTES"},
                        {"title": "WIRE-CONTRACT LOCKING", "body": "Validate A2A task handoffs and MCP tool arguments before execution begins.", "badge": "TYPE-SAFE I/O"},
                    ],
                    "rule": "Reject any agent write or memory update that omits a mandatory provenance field (source_file, line_range, blob_sha).",
                    "metric": "0 MALFORMED MEMORY WRITES",
                },
                {
                    "num": "03",
                    "name": "VALIDATION LOOP",
                    "tag": "SELF-HEALING WIKI",
                    "color": GREEN,
                    "bg": "#ECFDF5",
                    "headline": "Automated Staleness Detection & Ground-Truth Repair",
                    "left_desc": "Continuously compare stored knowledge claims against current git blob SHAs and re-verify stale notes in a sandbox.",
                    "stack": "Cloud Build / GitHub CI • tree-sitter • OpenHands",
                    "center_title": "CONTINUOUS WIKI AUDITOR",
                    "center_sub": "Inspect -> Verify SHA -> Heal",
                    "chips": ["SHA Check", "AST Diff", "Auto-Heal"],
                    "right_cards": [
                        {"title": "O(1) BLOB SHA CHECK", "body": "When code changes, any wiki note pointing to an old git blob SHA is flagged STALE instantly.", "badge": "O(1) DRIFT DETECT"},
                        {"title": "EVIDENCE-BOUND COMPACTION", "body": "Merge duplicate notes (80 -> 9 canonical files) while preserving 100% of verified citations.", "badge": "89% NOISE REDUCTION"},
                    ],
                    "rule": "Treat unverified or stale agent memory as a build failure — auto-repair or quarantine stale claims before serving them.",
                    "metric": "0% STALE CITATIONS SERVED",
                },
                {
                    "num": "04",
                    "name": "KNOWLEDGE GRAPH",
                    "tag": "SEMANTIC MESH",
                    "color": TEAL,
                    "bg": "#CCFBF1",
                    "headline": "Bipartite Entity-to-Code Graph & Hybrid Retrieval",
                    "left_desc": "Link architectural concepts, incidents, and runbooks to exact AST symbols, tables, and owners for multi-hop reasoning.",
                    "stack": "AlloyDB pgvector + Graph • BigQuery • Qdrant / Neo4j",
                    "center_title": "PROVENANCE KNOWLEDGE GRAPH",
                    "center_sub": "Entities <-> AST <-> Blob SHAs",
                    "chips": ["Nodes", "Typed Edges", "Vector+BM25"],
                    "right_cards": [
                        {"title": "MULTI-HOP LINEAGE TRAVERSAL", "body": "Trace from a production alert -> runbook -> service owner -> recent commit SHA in one hop.", "badge": "SUB-15MS GRAPH HOP"},
                        {"title": "HYBRID GRAPH + VECTOR RAG", "body": "Combine graph neighborhood expansion with dense embeddings and cross-encoder reranking.", "badge": "+31 PTS RECALL"},
                    ],
                    "rule": "Every node in the knowledge graph must resolve to an executable or verifiable artifact in the repository or data catalog.",
                    "metric": "100% GROUNDED GRAPH EDGES",
                },
            ],
            "takeaway": "Takeaway: Open Formats make knowledge portable; Schema Harness makes it typed; Validation Loop keeps it fresh; Knowledge Graph makes it navigable.",
        },
    }


register_templates(META_V4, RENDERERS_V4, demo_specs_v4)
