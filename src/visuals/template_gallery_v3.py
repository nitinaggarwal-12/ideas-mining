"""Template Gallery v3 — 12 net-new, zero-overlap dynamic templates (T41-T52).

Completes the 52-template Zero-Redundancy Gallery by incorporating the highest-engagement visual archetypes
and topics from the 14 evaluated viral LinkedIn posts and the 31 top Agentic AI / LLM / Systems creators:

  T41 Kavi Priyan (#01, 607 likes) & Sahn Lam — Systems Deep-Dive Engraving (LLM Inference Load Balancing & KV Routing)
  T42 Gurisa Roy (#02, 201 likes) & Keith R. Worfolk (#03) — Google Harness² Dual-Loop Recursive Self-Improving Agent
  T43 Ravena O & Rakesh Gohel (#05, 88 likes) — LangChain OpenWiki Self-Correcting Memory & SHA Evidence Receipts
  T44 Sumanth P (#04, 124 likes) — Deep Research Agent + Deterministic Citation Check + JEV Review Loop
  T45 Jonny Tooze (#11, 141 likes, 144 comments) — Executive ROI Crossover Chart & 6-Stage Agentic Value Funnel
  T46 Alok Sharan (#14, 63 likes) & Matthew Coombs (#08, 51 likes) — 4-Circle Cloverleaf C-Suite AI Governance Venn
  T47 Prashant Rathi (#09, 203 likes, 68 comments) — 4x5 Global AI Regulatory & Engineering Compliance Matrix
  T48 Prashant Rathi (#12, 53 likes) & Jonathan Parsons (#10, 71 likes) — 8-Tier Production AI Maturity Pyramid & 10-Step Order
  T49 Prem Natarajan (#13, 59 likes, 53 comments) & Chip Huyen — 3-Column Automation vs. Workflows vs. Agents Triptych
  T50 Alex Xu / ByteByteGo (#07) & Shalini Goyal (#06) — Stacked OAuth 2.0 + PKCE vs. OIDC + RFC 8693 Agent Delegation
  T51 Sahn Lam & Umar Jamil — GPU Memory Hierarchy (SRAM vs. HBM) & Speculative Decoding Token-Tree Verifier
  T52 Sebastian Raschka & Maxime Labonne — Reasoning Model Post-Training Pipeline (SFT -> GRPO -> RLVR -> Test-Time Compute)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.visuals.template_gallery import (
    AMBER, BG, BLUE, GREEN, INK, LINE, MUTED, NAVY, PURPLE, RED, SKY, SLATE, TEAL, WHITE,
    _card_head, _diamond, _esc, _flow, _frame, _grow, _pill, _r, _t, _tl, _wrap, register_templates,
)

Point = Tuple[float, float]


def _reveal(phase: Optional[float], n: int) -> int:
    return n if (phase is None or phase >= 0.8) else max(1, min(n, int(phase * (n + 1)) + 1))


def _fl(pts: Sequence[Point], col: str, phase: Optional[float], dur: float = 1.6,
        label: Optional[str] = None, dash: str = "7 5") -> str:
    return _flow(pts, col, phase, label, dur, 2.4, True, 1, dash=dash, track=True, label_dy=-12)


def _num(cx: float, cy: float, n: Any, col: str, r: float = 12) -> str:
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 3.0:.1f}" fill="{col}" fill-opacity="0.16"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{col}" stroke="#FFFFFF" stroke-width="1.2"/>'
        + _t(cx, cy + 4, str(n), 10, 800, WHITE, "middle")
    )


# ----------------------------------------------------------------------------------------------------------------------
# T41 — Systems Deep-Dive Engraving (LLM Inference Load Balancing & Prefix-Aware KV Routing)
# ----------------------------------------------------------------------------------------------------------------------
def render_t41(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    # Warm editorial paper backdrop (Kavi Priyan / Sahn Lam systems deep-dive style)
    b.append(_r(56, 136, 1508, 738, 12, "#F6F2E8", "#D6CFC0", 1.8))

    # Top Row: 2-column problem framing
    b.append(_r(72, 150, 728, 124, 10, WHITE, "#CBD5E1", 1.5))
    b.append(_r(72, 150, 8, 124, 4, RED))
    b.append(_t(94, 174, "01 • WHY NAIVE ROUND-ROBIN BREAKS FOR LLM INFERENCE", 11, 800, RED))
    b.append(_tl(94, 196, _wrap(s["problem_left"], 96, 4), 10.5, 600, INK, 16))

    b.append(_r(816, 150, 732, 124, 10, WHITE, "#CBD5E1", 1.5))
    b.append(_r(816, 150, 8, 124, 4, BLUE))
    b.append(_t(838, 174, "02 • PREFILL (COMPUTE-BOUND) VS. DECODE (MEMORY-BANDWIDTH-BOUND)", 11, 800, BLUE))
    for i, cmp_row in enumerate(s["compare_bars"][:2]):
        ry = 194 + i * 38
        b.append(_t(838, ry + 14, cmp_row["label"], 10, 800, cmp_row["color"]))
        b.append(_r(1070, ry, 280, 20, 5, "#F1F5F9", "#CBD5E1", 1))
        bw = 280 * cmp_row["frac"] * _grow(phase)
        b.append(_r(1070, ry, bw, 20, 5, cmp_row["color"]))
        b.append(_t(1362, ry + 14, cmp_row["metrics"], 9.8, 800, INK, mono=True))

    # Middle Left: Router-to-4-GPU-Workers Schematic (x=72..1032, y=288..672)
    b.append(_r(72, 288, 960, 384, 10, WHITE, "#CBD5E1", 1.6))
    b.append(_t(92, 314, "LIVE REQUEST ROUTING: RADIX PREFIX TREE + LEAST-KV-PRESSURE LOAD BALANCER", 11, 800, NAVY))

    # Incoming request cards on the left
    for i, req in enumerate(s["requests"][:3]):
        ry = 336 + i * 106
        b.append(_r(88, ry, 212, 88, 8, "#F8FAFC", req["color"], 1.5))
        b.append(_t(102, ry + 20, req["id"], 10, 800, req["color"]))
        b.append(_t(102, ry + 38, req["prefix"], 9.5, 700, INK, mono=True))
        b.append(_t(102, ry + 56, req["tokens"], 9.5, 600, SLATE))
        b.append(_pill(102, ry + 64, req["route_tag"], req["color"], size=8.5, h=18)[0])
        b.append(_fl([(300, ry + 44), (336, 480)], req["color"], phase, 1.4))

    # Central Router Box
    b.append(_card_head(338, 356, 232, 252, NAVY, "PREFIX + KV ROUTER", head_h=28))
    b.append(_t(352, 404, "Radix Prefix Cache Table:", 9.5, 800, BLUE))
    for i, rt in enumerate(s["radix_table"][:3]):
        b.append(_r(352, 414 + i * 26, 204, 22, 4, "#EFF6FF", "#BFDBFE", 1))
        b.append(_t(360, 429 + i * 26, rt, 9, 700, INK, mono=True))
    b.append(_t(352, 512, "Composite Score:", 9.5, 800, PURPLE))
    b.append(_r(352, 520, 204, 42, 6, "#F5F3FF", "#DDD6FE", 1))
    b.append(_t(360, 536, "+ PrefixOverlap(req, w)", 9, 700, "#5B21B6", mono=True))
    b.append(_t(360, 552, "- KV_HBM(w) - Queue(w)", 9, 700, "#5B21B6", mono=True))
    b.append(_t(352, 586, "vLLM • SGLang • Vertex / GKE", 9, 700, GREEN))

    # 4 GPU Worker Nodes (complete bars, zero clipped orphan arcs)
    for i, w in enumerate(s["workers"][:4]):
        wy = 330 + i * 84
        col = w["color"]
        b.append(_fl([(570, 480), (624, wy + 36)], col, phase, 1.5, dash="6 4"))
        b.append(_r(628, wy, 388, 72, 8, w["fill"], col, 1.6))
        b.append(_r(628, wy, 8, 72, 4, col))
        b.append(_t(646, wy + 20, w["name"], 10.5, 800, INK))
        b.append(_pill(864, wy + 6, w["status"], col, size=8.5, h=18)[0])
        # KV Cache Fill Bar
        b.append(_t(646, wy + 40, f"KV HBM: {w['kv_pct']}%", 9.5, 700, SLATE, mono=True))
        b.append(_r(740, wy + 29, 130, 14, 4, WHITE, "#CBD5E1", 1))
        b.append(_r(740, wy + 29, 130 * (w["kv_pct"] / 100.0), 14, 4, col))
        b.append(_t(880, wy + 40, w["prefix_held"], 9, 700, col, mono=True))
        b.append(_t(646, wy + 59, w["detail"], 9.5, 700, "#1E293B"))

    # Middle Right: 2 Magnifier Callouts (x=1048..1548, y=288..672)
    b.append(_card_head(1048, 288, 500, 184, PURPLE, "ZOOM A • CHUNKED PREFILL STOPS DECODE STALLS", head_h=28))
    b.append(_t(1066, 336, "Without chunking (32K prefill blocks decode for 850 ms):", 9.5, 700, RED))
    b.append(_r(1066, 344, 340, 20, 4, RED))
    b.append(_t(1236, 358, "32K PREFILL MONOLITH (850 ms)", 9, 800, WHITE, "middle"))
    b.append(_r(1412, 344, 118, 20, 4, "#94A3B8"))
    b.append(_t(1471, 358, "DECODE STALLED", 8.5, 800, WHITE, "middle"))

    b.append(_t(1066, 386, "With chunked prefill (2K chunks interleaved with active decode):", 9.5, 700, GREEN))
    for k in range(4):
        cx = 1066 + k * 118
        b.append(_r(cx, 394, 64, 20, 4, BLUE))
        b.append(_t(cx + 32, 408, f"Prefill {k+1}", 8.5, 800, WHITE, "middle"))
        b.append(_r(cx + 68, 394, 44, 20, 4, GREEN))
        b.append(_t(cx + 90, 408, "Dec", 8.5, 800, WHITE, "middle"))
    b.append(_tl(1066, 434, _wrap(s["zoom_a_note"], 68, 2), 9.5, 600, INK, 14))

    b.append(_card_head(1048, 488, 500, 184, TEAL, "ZOOM B • DISAGGREGATED PREFILL & DECODE POOLS", head_h=28))
    b.append(_r(1066, 530, 210, 74, 8, "#EFF6FF", BLUE, 1.5))
    b.append(_t(1171, 552, "PREFILL POOL (COMPUTE)", 9.5, 800, BLUE, "middle"))
    b.append(_t(1171, 570, "High FLOP utilization", 9, 600, INK, "middle"))
    b.append(_t(1171, 588, "Optimizes TTFT (<185 ms)", 9, 700, BLUE, "middle"))
    b.append(_fl([(1276, 567), (1320, 567)], TEAL, phase, 1.2, "KV DMA"))
    b.append(_r(1322, 530, 210, 74, 8, "#ECFDF5", GREEN, 1.5))
    b.append(_t(1427, 552, "DECODE POOL (HBM BW)", 9.5, 800, GREEN, "middle"))
    b.append(_t(1427, 570, "High HBM3e bandwidth", 9, 600, INK, "middle"))
    b.append(_t(1427, 588, "Optimizes ITL (11.4 ms)", 9, 700, GREEN, "middle"))
    b.append(_tl(1066, 624, _wrap(s["zoom_b_note"], 68, 3), 9.5, 600, INK, 14))

    # Bottom Row: 01..03 Strategy Cards (y=684..862)
    for i, st in enumerate(s["strategies"][:3]):
        sx = 72 + i * 494
        col = st["color"]
        b.append(_r(sx, 684, 488, 176, 10, WHITE, col, 1.8))
        b.append(_r(sx, 684, 488, 30, 10, col))
        b.append(_t(sx + 16, 704, f"0{i + 1} • {st['title']}", 10.5, 800, WHITE))
        b.append(_t(sx + 472, 704, st["gain"], 10, 800, "#FEF08A", "end", mono=True))
        b.append(_tl(sx + 16, 734, _wrap(st["how"], 64, 4), 10, 600, INK, 15))
        b.append(_t(sx + 16, 814, "WHEN TO USE:", 9, 800, col))
        b.append(_t(sx + 104, 814, st["when"], 9.5, 700, "#1E293B"))
        b.append(_pill(sx + 16, 828, st["stack"], col, size=8.5, h=20)[0])

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T41", META["T41"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T42 — Recursive Agent Harness (Google Harness²: Task-Level & Harness-Level Self-Improvement)
# ----------------------------------------------------------------------------------------------------------------------
def render_t42(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Left Column: Loop 1 — Task-Level Recursion (Propose -> Probe -> Compose)
    b.append(_card_head(56, 136, 464, 734, BLUE, "LOOP 1 • TASK-LEVEL RECURSION (SKILL GRAPH)"))
    for i, st in enumerate(s["task_loop"][:3]):
        sy = 184 + i * 168
        col = st["color"]
        b.append(_r(74, sy, 428, 142, 10, "#F8FAFC", col, 1.6))
        b.append(_r(74, sy, 8, 142, 4, col))
        b.append(_num(102, sy + 24, i + 1, col, 12))
        b.append(_t(122, sy + 28, st["name"], 11.5, 800, col))
        b.append(_pill(370, sy + 12, st["tag"], col, size=8.5, h=20)[0])
        b.append(_tl(94, sy + 52, _wrap(st["body"], 58, 4), 10, 600, INK, 15))
        b.append(_t(94, sy + 124, st["artifact"], 9.5, 700, SLATE, mono=True))
        if i < 2:
            b.append(_fl([(288, sy + 142), (288, sy + 168)], col, phase, 1.2))
    # Feedback loop arrow from Compose back to Propose
    b.append(_fl([(74, 590), (62, 590), (62, 240), (74, 240)], PURPLE, phase, 2.0))
    b.append(_r(74, 690, 428, 162, 10, "#FEF2F2", RED, 1.5))
    b.append(_t(92, 714, "WHY STATIC HARNESSES PLATEAU", 10, 800, RED))
    b.append(_tl(92, 736, _wrap(s["why_static_fails"], 58, 6), 10, 600, "#7F1D1D", 15))

    # Center Column: 5 Concentric Operating Rings + Complete 6-Step Closed Execution Loop
    b.append(_card_head(536, 136, 548, 734, NAVY, "5 CONCENTRIC HARNESS RINGS + 6-STEP CLOSED LOOP"))
    cx, cy = 810, 398
    rings = [
        (230, 178, "#ECFDF5", GREEN, "RING 5 • GOVERNANCE & SNAPSHOT GATE (Promptfoo / Vertex)"),
        (190, 146, "#EFF6FF", BLUE, "RING 4 • PROTOCOLS & SANDBOX (MCP • A2A • OpenHands)"),
        (150, 114, "#F5F3FF", PURPLE, "RING 3 • MEMORY & ARTIFACT RECEIPTS (Firestore • SHA)"),
        (110, 82, "#FFFBEB", AMBER, "RING 2 • DYNAMIC SKILL GRAPH (Composed SKILL.md)"),
        (72, 52, "#F0FDFA", TEAL, "RING 1 • RUNTIME HARNESS (ADK • LangGraph • Budgets)"),
    ]
    for rx, ry, fill, col, label in rings:
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{col}" stroke-width="1.8"/>')
        pw = len(label) * 5.1 + 16
        b.append(_r(cx - pw / 2.0, cy - ry + 2, pw, 17, 8, WHITE, col, 1.2))
        b.append(_t(cx, cy - ry + 14, label, 8.6, 800, col, "middle"))
    b.append(_r(cx - 56, cy - 22, 112, 44, 22, NAVY, WHITE, 2))
    b.append(_t(cx, cy - 3, "FOUNDATION LLM", 9.2, 800, WHITE, "middle"))
    b.append(_t(cx, cy + 12, "Gemini 3.8 / GLM-5", 8.5, 700, "#93C5FD", "middle"))

    # Complete 6-Step Execution Loop (01..06 — fixes Keith Worfolk's missing Step 05!)
    b.append(_t(810, 604, "COMPLETE 6-STEP HARNESS EXECUTION LOOP (01 -> 06, ZERO SKIPPED STEPS)", 10, 800, NAVY, "middle"))
    for i, step in enumerate(s["six_steps"][:6]):
        col_i = i % 3
        row_i = i // 3
        sx = 554 + col_i * 174
        sy = 618 + row_i * 116
        col = step["color"]
        b.append(_r(sx, sy, 164, 100, 8, "#F8FAFC", col, 1.6))
        b.append(_r(sx, sy, 164, 24, 8, col))
        b.append(_t(sx + 10, sy + 16, f"0{i + 1} • {step['name']}", 9.5, 800, WHITE))
        b.append(_tl(sx + 10, sy + 40, _wrap(step["desc"], 25, 4), 9.0, 600, INK, 12.5))

    # Right Column: Loop 2 — Harness-Level Recursion & Verified Benchmark Gains
    b.append(_card_head(1100, 136, 464, 734, GREEN, "LOOP 2 • HARNESS-LEVEL RECURSION & BENCHMARKS"))
    b.append(_r(1118, 184, 428, 232, 10, "#F8FAFC", GREEN, 1.6))
    b.append(_t(1134, 208, "CROSS-TASK HARNESS EVOLUTION PIPELINE", 10.5, 800, GREEN))
    for i, hstep in enumerate(s["harness_loop"][:4]):
        hy = 224 + i * 46
        b.append(_num(1144, hy + 12, i + 1, GREEN, 10))
        b.append(_t(1162, hy + 10, hstep["head"], 10, 800, INK))
        b.append(_t(1162, hy + 26, hstep["sub"], 9.2, 600, SLATE))

    # Verified Benchmark Bars (Harness² Paper)
    b.append(_r(1118, 432, 428, 242, 10, WHITE, LINE, 1.6))
    b.append(_t(1134, 456, "VERIFIED HARNESS² BENCHMARK GAINS (SAME BASE MODEL)", 10.2, 800, NAVY))
    for i, bm in enumerate(s["benchmarks"][:3]):
        by = 478 + i * 64
        b.append(_t(1134, by + 12, bm["name"], 10.5, 800, INK))
        b.append(_t(1528, by + 12, bm["delta"], 10.5, 800, GREEN, "end", mono=True))
        # Baseline bar
        b.append(_r(1134, by + 20, 260 * (bm["base"] / 100.0), 14, 4, "#94A3B8"))
        b.append(_t(1140 + 260 * (bm["base"] / 100.0), by + 31, f"Static: {bm['base']}%", 8.8, 700, SLATE, mono=True))
        # Harness2 bar
        hw = 260 * (bm["after"] / 100.0) * _grow(phase)
        b.append(_r(1134, by + 37, hw, 16, 4, bm["color"]))
        b.append(_t(1140 + 260 * (bm["after"] / 100.0), by + 49, f"Harness²: {bm['after']}%", 9.2, 800, bm["color"], mono=True))

    b.append(_r(1118, 690, 428, 162, 10, "#ECFDF5", GREEN, 1.6))
    b.append(_t(1134, 714, "THE ARCHITECTURAL SHIFT (GURISA ROY & HARNESS²)", 10, 800, "#065F46"))
    b.append(_tl(1134, 736, _wrap(s["core_insight"], 58, 6), 10, 700, "#064E3B", 15))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T42", META["T42"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T43 — Self-Correcting Memory (LangChain OpenWiki: Teaching AI Agents How to Forget)
# ----------------------------------------------------------------------------------------------------------------------
def render_t43(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Top Problem vs. Fix Banner (y=136..244)
    b.append(_r(56, 136, 742, 108, 10, "#FEF2F2", RED, 1.6))
    b.append(_t(76, 162, "THE SILENT FAILURE: MEMORY ROT IN LONG-LIVED AGENTS", 10.5, 800, RED))
    b.append(_tl(76, 184, _wrap(s["problem_banner"], 98, 3), 10.2, 600, "#7F1D1D", 16))

    b.append(_r(822, 136, 742, 108, 10, "#ECFDF5", GREEN, 1.6))
    b.append(_t(842, 162, "THE LANGCHAIN OPENWIKI FIX: EVIDENCE RECEIPTS + O(1) STALENESS", 10.5, 800, "#065F46"))
    b.append(_tl(842, 184, _wrap(s["solution_banner"], 98, 3), 10.2, 600, "#064E3B", 16))

    # Main 4-Stage Pipeline (y=260..716)
    for i, st in enumerate(s["stages"][:4]):
        sx = 56 + i * 382
        col = st["color"]
        b.append(_card_head(sx, 260, 362, 456, col, f"0{i + 1} • {st['title']}", head_h=32))
        b.append(_t(sx + 16, 316, st["subtitle"], 10.5, 800, col))
        b.append(_tl(sx + 16, 338, _wrap(st["body"], 48, 4), 10, 600, INK, 15))

        # Concrete artifact box inside each stage
        b.append(_r(sx + 16, 408, 330, 196, 8, "#0F172A", col, 1.5))
        b.append(_t(sx + 28, 430, st["code_head"], 9.5, 800, "#93C5FD", mono=True))
        for k, ln in enumerate(st["code_lines"][:7]):
            lcol = "#86EFAC" if ln.startswith("+") else ("#FCA5A5" if ln.startswith("!") else "#E2E8F0")
            b.append(_t(sx + 28, 452 + k * 20, ln, 9.2, 600, lcol, mono=True))

        # Bottom mini-rule inside each card
        b.append(_r(sx + 16, 618, 330, 82, 8, st["note_fill"], col, 1.4))
        b.append(_t(sx + 28, 638, st["note_head"], 9.5, 800, col))
        b.append(_tl(sx + 28, 656, _wrap(st["note_body"], 46, 3), 9.5, 600, INK, 14))

        if i < 3:
            b.append(_fl([(sx + 362, 488), (sx + 382, 488)], col, phase, 1.2))

    # Bottom Verified Results Bar (y=732..868)
    b.append(_r(56, 732, 1508, 136, 12, WHITE, LINE, 1.8))
    b.append(_t(76, 758, "VERIFIED BENCHMARK OUTCOMES (LANGCHAIN OPENWIKI • FIRESTORE ⇄ POSTGRESQL + GIT)", 10.5, 800, NAVY))
    for i, m in enumerate(s["metrics"][:4]):
        mx = 76 + i * 368
        b.append(_r(mx, 770, 352, 82, 8, "#F8FAFC", m["color"], 1.6))
        b.append(_r(mx, 770, 8, 82, 4, m["color"]))
        b.append(_t(mx + 22, 802, m["value"], 22, 800, m["color"], mono=True))
        b.append(_t(mx + 22, 824, m["label"], 10, 800, INK))
        b.append(_t(mx + 22, 842, m["sub"], 9, 600, SLATE))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T43", META["T43"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T44 — Deep Research Verifier (Deterministic Citation Check + JEV Review Loop)
# ----------------------------------------------------------------------------------------------------------------------
def render_t44(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Top Pipeline Container (y=136..522)
    b.append(_r(56, 136, 1508, 386, 12, WHITE, LINE, 1.8))
    b.append(_t(76, 162, "END-TO-END DEEP RESEARCH & DETERMINISTIC + JEV VERIFICATION ARCHITECTURE", 11, 800, NAVY))

    # 6 Pipeline Stages across y=182..354
    xs = [74, 314, 562, 810, 1066, 1322]
    ws = [216, 224, 224, 232, 232, 222]
    for i, st in enumerate(s["pipeline"][:6]):
        sx, sw = xs[i], ws[i]
        col = st["color"]
        b.append(_card_head(sx, 182, sw, 174, col, f"0{i + 1} • {st['name']}", head_h=28))
        b.append(_t(sx + 12, 230, st["role"], 10, 800, col))
        b.append(_tl(sx + 12, 248, _wrap(st["desc"], int(sw / 7.2), 4), 9.5, 600, INK, 14))
        b.append(_pill(sx + 12, 322, st["stack"], col, size=8.2, h=20)[0])
        if i < 5:
            nx = xs[i + 1]
            b.append(_fl([(sx + sw, 268), (nx, 268)], col, phase, 1.2))

    # Conditional JEV Retry Loop Band (y=372..504)
    b.append(_r(314, 384, 984, 118, 10, "#FFFBEB", AMBER, 1.6))
    b.append(_diamond(1182, 442, 66, 38, ["JEV GATE", "Pass / Retry?"], AMBER, 9))
    # Down arrow from Stage 05 to Diamond
    b.append(_fl([(1182, 356), (1182, 404)], AMBER, phase, 1.0))
    # Approve path to Stage 06
    b.append(_fl([(1248, 442), (1433, 442), (1433, 356)], GREEN, phase, 1.3, "APPROVE"))
    # Research_Again loop back to Stage 02
    b.append(_fl([(1116, 442), (426, 442), (426, 356)], RED, phase, 2.2))
    b.append(_t(760, 412, "RESEARCH_AGAIN (MAX 1 TARGETED RETRY WITH MISSING-EVIDENCE QUERIES)", 10, 800, RED, "middle"))
    b.append(_t(760, 468, "Passes exact unsupported claims + failed URL spans back to Stage 02 so the agent repairs only what failed.", 9.8, 700, "#92400E", "middle"))

    # Bottom 3 Deep-Dive Cards (y=538..868)
    for i, p in enumerate(s["panels"][:3]):
        px = 56 + i * 510
        col = p["color"]
        b.append(_card_head(px, 538, 488, 330, col, p["title"], head_h=30))
        for k, item in enumerate(p["items"][:4]):
            iy = 582 + k * 68
            b.append(_r(px + 16, iy, 456, 58, 8, "#F8FAFC", col, 1.2))
            b.append(_num(px + 34, iy + 20, k + 1, col, 10))
            b.append(_t(px + 52, iy + 22, item["head"], 10, 800, INK))
            b.append(_tl(px + 52, iy + 38, _wrap(item["body"], 60, 2), 9.2, 600, SLATE, 13))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T44", META["T44"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T45 — Executive ROI Crossover Funnel (The Agentic AI Value Funnel: First Run to P&L)
# ----------------------------------------------------------------------------------------------------------------------
def render_t45(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Top Left: Crossover Chart (x=56..1076, y=136..498)
    b.append(_r(56, 136, 1020, 362, 12, WHITE, LINE, 1.8))
    b.append(_t(78, 162, "THE AGENTIC CROSSOVER: HUMAN TOUCHES PER OUTCOME VS. NET VALUE DELIVERED", 11, 800, NAVY))
    x0, y0, x1, y1 = 128, 194, 1024, 440

    # Grid lines & Pilot Ceiling
    for k in range(5):
        gy = y1 - (y1 - y0) * k / 4.0
        b.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="#E2E8F0" stroke-width="1"/>')
        b.append(_t(x0 - 10, gy + 4, f"{k * 25}%", 9, 700, SLATE, "end"))

    # Pilot Ceiling Line
    pcy = y1 - (y1 - y0) * 0.42
    b.append(f'<line x1="{x0}" y1="{pcy:.1f}" x2="{x1}" y2="{pcy:.1f}" stroke="{AMBER}" stroke-width="2" stroke-dasharray="8 6"/>')
    b.append(_r(140, pcy - 22, 276, 20, 4, "#FFFBEB", AMBER, 1))
    b.append(_t(278, pcy - 8, "PILOT CEILING (80% of teams stall here)", 8.8, 800, "#92400E", "middle"))

    stages = s["funnel"][:6]
    human_pts: List[Point] = []
    value_pts: List[Point] = []
    for i, st in enumerate(stages):
        px = x0 + (x1 - x0) * i / 5.0
        hy = y1 - (y1 - y0) * (st["human_pct"] / 100.0)
        vy = y1 - (y1 - y0) * (st["value_pct"] / 100.0)
        human_pts.append((px, hy))
        value_pts.append((px, vy))
        b.append(_t(px, y1 + 20, f"0{i+1} {st['short']}", 9.5, 800, INK, "middle"))

    # Draw curves
    b.append(_flow(human_pts, BLUE, phase, None, 3.0, 3.0, False, 1, dash="8 5", track=False))
    b.append(_flow(value_pts, GREEN, phase, None, 3.0, 3.5, False, 1, track=False, solid=True))
    for i in range(6):
        hx, hy = human_pts[i]
        vx, vy = value_pts[i]
        b.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="5" fill="{BLUE}" stroke="{WHITE}" stroke-width="1.5"/>')
        htx = hx + (24 if i == 0 else (-20 if i == 5 else 0))
        hty = (hy + 18) if i == 2 else (hy - 10)
        b.append(_t(htx, hty, f"{stages[i]['human_pct']}% touch", 8.8, 800, BLUE, "middle"))
        b.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="5.5" fill="{GREEN}" stroke="{WHITE}" stroke-width="1.5"/>')
        vtx = vx + (22 if i == 0 else (-18 if i == 5 else 0))
        vty = (vy - 10) if i == 2 else (vy + 18)
        b.append(_t(vtx, vty, f"{stages[i]['value_pct']}% val", 8.8, 800, GREEN, "middle"))

    # Crossover Callout Box
    cx_cross = (human_pts[2][0] + human_pts[3][0]) / 2.0
    cy_cross = (human_pts[2][1] + value_pts[3][1]) / 2.0
    b.append(f'<circle cx="{cx_cross:.1f}" cy="{cy_cross:.1f}" r="9" fill="{PURPLE}" fill-opacity="0.25" stroke="{PURPLE}" stroke-width="2"/>')
    b.append(_r(cx_cross - 140, 200, 280, 44, 8, "#F5F3FF", PURPLE, 1.6))
    b.append(_t(cx_cross, 218, "THE CROSSOVER POINT", 9.5, 800, PURPLE, "middle"))
    b.append(_t(cx_cross, 234, "Humans step back from the work to the gates", 9, 700, INK, "middle"))
    b.append(f'<line x1="{cx_cross:.1f}" y1="244" x2="{cx_cross:.1f}" y2="{cy_cross - 10:.1f}" stroke="{PURPLE}" stroke-width="1.6" stroke-dasharray="4 3"/>')

    # Legend at bottom of chart
    b.append(_t(130, 484, "— — Blue: Human touches per outcome (100% -> 4%) • Vertex AI / Cloud Trace ⇄ OpenHands / LangGraph", 9.2, 800, BLUE))
    b.append(_t(730, 484, "─── Green: Net P&L value delivered (crosses Pilot Ceiling at Stage 03->04)", 9.2, 800, GREEN))

    # Top Right: Executive Unlock Card (x=1092..1564, y=136..498)
    b.append(_card_head(1092, 136, 472, 362, NAVY, "HOW TO BREAK THROUGH THE PILOT CEILING"))
    for i, g in enumerate(s["unlock_gates"][:3]):
        gy = 182 + i * 102
        b.append(_r(1110, gy, 436, 90, 8, "#F8FAFC", g["color"], 1.5))
        b.append(_r(1110, gy, 8, 90, 4, g["color"]))
        b.append(_t(1128, gy + 22, f"GATE {i + 1} • {g['head']}", 10, 800, g["color"]))
        b.append(_tl(1128, gy + 40, _wrap(g["body"], 60, 3), 9.5, 600, INK, 14))

    # Bottom Half: 6-Stage Value Funnel Cards (y=514..868)
    for i, st in enumerate(stages):
        sx = 56 + i * 254
        col = st["color"]
        b.append(_card_head(sx, 514, 238, 354, col, f"0{i + 1} • {st['name']}", head_h=30))
        b.append(_pill(sx + 14, 556, f"OWNER: {st['owner']}", col, size=8.5, h=20)[0])
        b.append(_t(sx + 14, 602, st["kpi_value"], 20, 800, col, mono=True))
        b.append(_t(sx + 14, 622, st["kpi_label"], 9.5, 800, INK))
        b.append(_tl(sx + 14, 646, _wrap(st["question"], 32, 3), 9.5, 700, "#1E293B", 14))
        b.append(_r(sx + 14, 706, 210, 146, 8, "#F8FAFC", "#CBD5E1", 1.2))
        b.append(_t(sx + 24, 726, "WHAT PROVES IT:", 8.8, 800, col))
        b.append(_tl(sx + 24, 744, _wrap(st["proof"], 29, 5), 9.2, 600, SLATE, 14))
        if i < 5:
            b.append(_fl([(sx + 238, 690), (sx + 254, 690)], col, phase, 1.0))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T45", META["T45"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T46 — 4-Circle Cloverleaf Governance Venn (C-Suite AI Governance: CEO vs. CIO vs. CTO vs. CISO)
# ----------------------------------------------------------------------------------------------------------------------
def render_t46(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Left Panel: 4-Circle Cloverleaf Venn Diagram (x=56..836, y=136..868)
    b.append(_card_head(56, 136, 780, 732, NAVY, "C-SUITE CLOVERLEAF GOVERNANCE VENN (CEO • CTO • CIO • CISO)"))
    # 4 overlapping circles around center (446, 476)
    circles = [
        (334, 364, 172, BLUE, "#EFF6FF", "CEO", "STRATEGY & P&L", 276, 302,
         ["• Competitive AI moat", "• Capital & ROI targets", "• Board risk appetite"]),
        (558, 364, 172, PURPLE, "#F5F3FF", "CTO", "MODEL & HARNESS", 616, 302,
         ["• Vertex / ADK & LangGraph", "• Eval & latency SLOs", "• MCP / A2A architecture"]),
        (334, 588, 172, TEAL, "#F0FDFA", "CIO", "ENTERPRISE IT & DATA", 276, 614,
         ["• BigQuery / Postgres lineage", "• Workforce adoption", "• Vendor SaaS sprawl"]),
        (558, 588, 172, RED, "#FEF2F2", "CISO", "SECURITY & RISK", 616, 614,
         ["• Model Armor / Llama Guard", "• Least-privilege IAM/OPA", "• EU AI Act / NIST RMF"]),
    ]
    for cx, cy, rad, col, fill, _role, _sub, _tx, _ty, _bullets in circles:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{fill}" fill-opacity="0.68" stroke="{col}" stroke-width="2.4"/>')
    for _cx, _cy, _rad, col, _fill, role, sub, tx, ty, bullets in circles:
        b.append(_t(tx, ty, f"{role} • {sub}", 10.2, 800, col, "middle"))
        for k, bul in enumerate(bullets):
            b.append(_t(tx, ty + 18 + k * 15, bul, 9.0, 700, INK, "middle"))

    # 4 Pairwise Overlap Pills inside the cloverleaf
    overlaps = [
        (446, 256, "CEO ∩ CTO: Build vs. Buy", BLUE),
        (446, 696, "CIO ∩ CISO: Data DLP & IAM", RED),
        (218, 476, "CEO ∩ CIO: Workflow ROI", TEAL),
        (674, 476, "CTO ∩ CISO: Secure Harness", PURPLE),
    ]
    for ox, oy, olabel, ocol in overlaps:
        b.append(_r(ox - 86, oy - 14, 172, 28, 14, WHITE, ocol, 1.8))
        b.append(_t(ox, oy + 4, olabel, 8.8, 800, ocol, "middle"))

    # Center Core Badge
    b.append(_r(356, 444, 180, 64, 12, NAVY, WHITE, 2.2))
    b.append(_t(446, 470, "ENTERPRISE AI", 10.5, 800, "#93C5FD", "middle"))
    b.append(_t(446, 488, "OPERATING MODEL", 10.5, 800, WHITE, "middle"))

    # Lifecycle Progression Bar at bottom of Left Panel (y=778..852)
    b.append(_r(74, 780, 744, 72, 10, "#F8FAFC", LINE, 1.5))
    b.append(_t(92, 800, "LIFECYCLE HANDOFFS (MATTHEW COOMBS & ALOK SHARAN):", 9.5, 800, NAVY))
    lsteps = [
        ("1. DEMO", "CTO Sandbox", PURPLE),
        ("2. PILOT", "CTO + CIO Data", BLUE),
        ("3. PRODUCTION", "+ CISO Guardrails", RED),
        ("4. ENTERPRISE", "+ CEO P&L Scale", GREEN),
    ]
    for i, (lh, ls, lcol) in enumerate(lsteps):
        lx = 92 + i * 182
        b.append(_r(lx, 810, 160, 32, 6, WHITE, lcol, 1.5))
        b.append(_t(lx + 80, 824, lh, 9, 800, lcol, "middle"))
        b.append(_t(lx + 80, 837, ls, 8.5, 600, SLATE, "middle"))
        if i < 3:
            b.append(_fl([(lx + 160, 826), (lx + 182, 826)], lcol, phase, 1.1))

    # Right Panel: 6 Shared Accountability Cards (x=852..1564, y=136..868)
    b.append(_card_head(852, 136, 712, 732, NAVY, "6 SHARED ACCOUNTABILITY CHARTERS (ZERO OVERLAPPING BULLETS)"))
    for i, card in enumerate(s["charters"][:6]):
        col_i = i % 2
        row_i = i // 2
        cx = 870 + col_i * 344
        cy = 182 + row_i * 224
        col = card["color"]
        b.append(_r(cx, cy, 332, 208, 10, "#F8FAFC", col, 1.6))
        b.append(_r(cx, cy, 332, 28, 10, col))
        b.append(_t(cx + 12, cy + 19, card["pair"], 9.8, 800, WHITE))
        b.append(_t(cx + 12, cy + 48, card["title"], 10.5, 800, INK))
        for k, item in enumerate(card["bullets"][:3]):
            b.append(_tl(cx + 12, cy + 68 + k * 36, _wrap(f"• {item}", 46, 2), 9.2, 600, "#1E293B", 13))
        b.append(_pill(cx + 12, cy + 178, card["artifact"], col, size=8.2, h=20)[0])

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T46", META["T46"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T47 — Global AI Regulatory Matrix (4x5 Grid: 20 Cross-Border AI Policies & Standards Explained)
# ----------------------------------------------------------------------------------------------------------------------
def render_t47(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    for r_idx, row in enumerate(s["rows"][:4]):
        ry = 138 + r_idx * 184
        rcol = row["color"]
        # Left Region Header Pill
        b.append(_r(56, ry, 146, 172, 10, rcol))
        b.append(_t(129, ry + 50, row["region"], 10.5, 800, WHITE, "middle"))
        b.append(_tl(129, ry + 70, _wrap(row["sub"], 19, 4), 9.0, 700, "#E2E8F0", 12.5, "middle"))
        b.append(_t(129, ry + 152, row["count_tag"], 8.8, 800, "#FEF08A", "middle", mono=True))
        if r_idx < 3:
            b.append(_fl([(129, ry + 172), (129, ry + 184)], rcol, phase, 1.2))

        # 5 Policy Cards across the row
        for c_idx, card in enumerate(row["cards"][:5]):
            cx = 212 + c_idx * 270
            num = r_idx * 5 + c_idx + 1
            b.append(_r(cx, ry, 260, 172, 10, WHITE, rcol, 1.5))
            b.append(_r(cx, ry, 260, 26, 10, row["fill"]))
            b.append(_t(cx + 10, ry + 18, f"{num:02d} • {card['name']}", 9.8, 800, rcol))
            b.append(_t(cx + 250, ry + 18, card["jurisdiction"], 8.5, 800, SLATE, "end", mono=True))

            b.append(_t(cx + 10, ry + 44, "SCOPE:", 8.5, 800, SLATE))
            b.append(_t(cx + 56, ry + 44, card["scope"], 9, 700, INK))

            b.append(_t(cx + 10, ry + 62, "ENGINEERING REQUIREMENT:", 8.5, 800, rcol))
            b.append(_tl(cx + 10, ry + 78, _wrap(card["control"], 37, 3), 9.2, 600, "#1E293B", 13))

            b.append(_r(cx + 10, ry + 124, 240, 38, 6, "#F8FAFC", "#CBD5E1", 1))
            b.append(_t(cx + 18, ry + 139, f"STATUS: {card['status']}", 8.5, 800, INK))
            b.append(_t(cx + 18, ry + 154, f"GATE: {card['gate']}", 8.5, 700, rcol, mono=True))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 11.5, 800, WHITE, "middle"))
    return _frame("T47", META["T47"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T48 — 8-Tier Production AI Maturity Pyramid (From Prototype Demo to Elite Autonomous Systems)
# ----------------------------------------------------------------------------------------------------------------------
def render_t48(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Left Column: Jonathan Parsons's 10-Step Correct Build Order (x=56..446, y=136..868)
    b.append(_card_head(56, 136, 390, 732, BLUE, "THE 10-STEP BUILD ORDER (DON'T START AT #10)"))
    for i, step in enumerate(s["build_order"][:10]):
        sy = 178 + i * 67
        col = step["color"]
        b.append(_r(72, sy, 358, 59, 8, "#F8FAFC", col, 1.4))
        b.append(_num(92, sy + 20, i + 1, col, 11))
        b.append(_t(112, sy + 22, step["head"], 10, 800, INK))
        b.append(_t(418, sy + 22, step["phase"], 8.5, 800, col, "end", mono=True))
        b.append(_t(112, sy + 42, step["sub"], 9.2, 600, SLATE))

    # Center Column: 8-Tier Ascending Pyramid (x=462..1158, y=136..868)
    b.append(_card_head(462, 136, 696, 732, NAVY, "8-TIER PRODUCTION AI MATURITY PYRAMID (PRASHANT RATHI)"))
    cx = 810.0
    tiers = s["tiers"][:8]  # Ordered L8 (top apex) -> L1 (wide base)
    for i, t_item in enumerate(tiers):
        ty0 = 186 + i * 82
        ty1 = ty0 + 72
        # Top width minimum 390px -> base width 656px so all text fits inside with generous margins
        w_top = 380 + i * 34
        w_bot = 380 + (i + 1) * 34
        pts = f"{cx - w_top/2:.1f},{ty0} {cx + w_top/2:.1f},{ty0} {cx + w_bot/2:.1f},{ty1} {cx - w_bot/2:.1f},{ty1}"
        b.append(f'<polygon points="{pts}" fill="{t_item["color"]}" stroke="{WHITE}" stroke-width="2"/>')
        b.append(_t(cx, ty0 + 26, f"{t_item['level']} • {t_item['name']}", 11, 800, WHITE, "middle"))
        b.append(_t(cx, ty0 + 45, t_item["controls"], 9.5, 700, "#F1F5F9", "middle"))
        b.append(_t(cx, ty0 + 61, t_item["stack"], 8.8, 700, "#FEF08A", "middle", mono=True))
    # Ascending animated flow arrow along the left edge of the pyramid
    b.append(_fl([(478, 826), (478, 200)], GREEN, phase, 2.2))

    # Right Column: What Breaks When You Skip a Tier (x=1174..1564, y=136..868)
    b.append(_card_head(1174, 136, 390, 732, RED, "WHAT BREAKS IF YOU SKIP A TIER"))
    for i, fl in enumerate(s["skip_failures"][:4]):
        fy = 182 + i * 168
        col = fl["color"]
        b.append(_r(1190, fy, 358, 152, 10, "#FEF2F2" if col == RED else "#FFFBEB", col, 1.6))
        b.append(_r(1190, fy, 8, 152, 4, col))
        b.append(_t(1208, fy + 24, fl["skip"], 10.5, 800, col))
        b.append(_t(1208, fy + 44, f"SYMPTOM: {fl['symptom']}", 9.8, 800, INK))
        b.append(_tl(1208, fy + 64, _wrap(fl["why"], 48, 3), 9.5, 600, "#1E293B", 14))
        b.append(_pill(1208, fy + 120, f"FIX: {fl['fix']}", GREEN, size=8.5, h=20)[0])

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T48", META["T48"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T49 — 3-Column Automation Decision Triptych (Traditional Automation vs. Workflows vs. AI Agents)
# ----------------------------------------------------------------------------------------------------------------------
def render_t49(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    for i, col_spec in enumerate(s["columns"][:3]):
        cx = 56 + i * 510
        col = col_spec["color"]
        b.append(_card_head(cx, 136, 488, 672, col, f"0{i + 1} • {col_spec['title']}", head_h=34))
        b.append(_t(cx + 18, 194, col_spec["tagline"], 11, 800, col))

        # Mini 3-Step Architecture Flow inside each column (y=208..296)
        b.append(_r(cx + 18, 208, 452, 88, 8, "#F8FAFC", col, 1.4))
        for k, node in enumerate(col_spec["nodes"][:3]):
            nx = cx + 30 + k * 148
            b.append(_r(nx, 224, 128, 56, 6, WHITE, col, 1.5))
            b.append(_t(nx + 64, 246, f"0{k+1} {node['head']}", 9.2, 800, col, "middle"))
            b.append(_t(nx + 64, 264, node["sub"], 8.5, 600, INK, "middle"))
            if k < 2:
                b.append(_fl([(nx + 128, 252), (nx + 148, 252)], col, phase, 1.1))

        # Comparison Attributes
        rows = [
            ("CONTROL FLOW OWNER", col_spec["owner"]),
            ("BEST FOR (USE CASES)", col_spec["best_for"]),
            ("LATENCY & COST / RUN", col_spec["cost"]),
            ("PRIMARY FAILURE MODE", col_spec["failure"]),
            ("VERIFICATION MECHANISM", col_spec["verify"]),
            ("GOOGLE ⇄ OSS STACK", col_spec["stack"]),
        ]
        for r_i, (rhead, rbody) in enumerate(rows):
            ry = 312 + r_i * 72
            b.append(_r(cx + 18, ry, 452, 62, 8, WHITE if r_i % 2 == 0 else "#F8FAFC", "#CBD5E1", 1.2))
            b.append(_t(cx + 30, ry + 18, rhead, 8.8, 800, col))
            b.append(_tl(cx + 30, ry + 35, _wrap(rbody, 62, 2), 9.6, 600, INK, 13))

        # Bottom Verdict Badge inside column
        b.append(_r(cx + 18, 748, 452, 44, 8, col))
        b.append(_t(cx + 244, 775, col_spec["verdict"], 10.5, 800, WHITE, "middle"))

    # Decision Rule Bar above footer (y=820..872)
    b.append(_r(56, 820, 1508, 52, 10, "#FFFBEB", AMBER, 1.8))
    b.append(_t(76, 842, "THE DECISION RULE (PREM NATARAJAN & CHIP HUYEN):", 9.8, 800, "#92400E"))
    b.append(_t(76, 860, s["decision_bar"], 11, 700, INK))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T49", META["T49"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T50 — Stacked Dual-Protocol Sequence (OAuth 2.0 + PKCE Authorization vs. OIDC + Agent Delegation)
# ----------------------------------------------------------------------------------------------------------------------
def render_t50(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    for p_idx, panel in enumerate(s["panels"][:2]):
        py = 136 + p_idx * 372
        pcol = panel["color"]
        b.append(_card_head(56, py, 1508, 358, pcol, panel["title"], head_h=30))

        # 4 Actor Headers + Vertical Lifelines (x=76..1100)
        actor_xs = [156, 426, 706, 986]
        for a_idx, actor in enumerate(panel["actors"][:4]):
            ax = actor_xs[a_idx]
            b.append(_r(ax - 82, py + 40, 164, 42, 8, panel["fill"], pcol, 1.6))
            b.append(_t(ax, py + 58, actor["name"], 9.8, 800, pcol, "middle"))
            b.append(_t(ax, py + 73, actor["sub"], 8.5, 600, SLATE, "middle"))
            b.append(f'<line x1="{ax}" y1="{py + 82}" x2="{ax}" y2="{py + 344}" stroke="#CBD5E1" stroke-width="1.8" stroke-dasharray="5 5"/>')

        # 7 Numbered Opaque-Pill Messages (zero lifeline collisions!)
        for m_idx, msg in enumerate(panel["messages"][:7]):
            my = py + 102 + m_idx * 34
            x_from = actor_xs[msg["from"]]
            x_to = actor_xs[msg["to"]]
            mcol = msg["color"]
            b.append(_fl([(x_from, my), (x_to, my)], mcol, phase, 1.1, dash="6 4"))
            mx = (x_from + x_to) / 2.0
            label_txt = msg["text"]
            pw = min(380, max(168, len(label_txt) * 5.8 + 38))
            px0 = mx - pw / 2.0
            b.append(_r(px0, my - 11, pw, 22, 11, WHITE, mcol, 1.4))
            b.append(_num(px0 + 13, my, m_idx + 1, mcol, 8.5))
            b.append(_t(px0 + 26, my + 3.5, label_txt, 9.0, 800, INK))

        # Right Summary & Token Payload Card (x=1112..1548)
        b.append(_r(1112, py + 40, 436, 304, 10, "#F8FAFC", pcol, 1.6))
        b.append(_t(1128, py + 64, panel["card_title"], 10.2, 800, pcol))
        for k, bul in enumerate(panel["bullets"][:3]):
            b.append(_tl(1128, py + 84 + k * 34, _wrap(f"• {bul}", 60, 2), 9.2, 600, INK, 13))
        b.append(_r(1128, py + 190, 404, 140, 8, "#0F172A", pcol, 1.4))
        b.append(_t(1140, py + 210, panel["token_head"], 9.2, 800, "#93C5FD", mono=True))
        for k, tln in enumerate(panel["token_lines"][:5]):
            b.append(_t(1140, py + 230 + k * 19, tln, 8.8, 600, "#86EFAC" if "act" in tln or "code_verifier" in tln else "#E2E8F0", mono=True))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T50", META["T50"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T51 — Speculative Decoding Token-Tree & GPU Memory Hierarchy (SRAM vs. HBM + Draft-Verify Loop)
# ----------------------------------------------------------------------------------------------------------------------
def render_t51(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Left Panel: GPU Memory Bandwidth Pyramid & Arithmetic Intensity (x=56..736, y=136..868)
    b.append(_card_head(56, 136, 680, 732, NAVY, "WHY DECODE IS MEMORY-BOUND: H100 GPU MEMORY PYRAMID"))
    cx_p = 396.0
    mem_tiers = [
        (280, 360, "#ECFDF5", GREEN, "ON-CHIP SRAM (L1 + SHARED)", "19.0 TB/s Bandwidth • 50 MB Capacity", "FlashAttention-3 tiles & Tensor Core registers live here"),
        (370, 460, "#EFF6FF", BLUE, "OFF-CHIP HBM3e (VRAM)", "3.35 TB/s Bandwidth • 80 GB Capacity", "70B FP8 weights (70 GB) + Paged KV Cache live here"),
        (470, 570, "#FFFBEB", AMBER, "NVLINK / PCIe INTERCONNECT", "900 GB/s NVLink • 128 GB/s PCIe Gen5", "Cross-GPU Tensor Parallelism & Disaggregated KV DMA"),
    ]
    for idx, (w_top, w_bot, fill, col, name, bw, note) in enumerate(mem_tiers):
        ty0 = 192 + idx * 116
        ty1 = ty0 + 104
        pts = f"{cx_p - w_top/2},{ty0} {cx_p + w_top/2},{ty0} {cx_p + w_bot/2},{ty1} {cx_p - w_bot/2},{ty1}"
        b.append(f'<polygon points="{pts}" fill="{fill}" stroke="{col}" stroke-width="2.2"/>')
        b.append(_t(cx_p, ty0 + 32, name, 11, 800, col, "middle"))
        b.append(_t(cx_p, ty0 + 54, bw, 10.5, 800, INK, "middle", mono=True))
        b.append(_t(cx_p, ty0 + 76, note, 9.2, 600, SLATE, "middle"))

    # Worked Roofline Math Box (y=552..852)
    b.append(_r(74, 552, 644, 298, 10, "#0F172A", BLUE, 1.6))
    b.append(_t(94, 578, "THE ROOFLINE BOTTLENECK (WORKED H100 CALCULATION)", 10.5, 800, "#93C5FD", mono=True))
    for i, mln in enumerate(s["roofline_lines"][:10]):
        col_ln = "#FCA5A5" if "IDLE" in mln else ("#86EFAC" if "FIX:" in mln else "#E2E8F0")
        b.append(_t(94, 604 + i * 23, mln, 9.5, 700 if "FIX:" in mln or "IDLE" in mln else 600, col_ln, mono=True))

    # Right Panel: Speculative Decoding Token-Tree Verifier (x=752..1564, y=136..868)
    b.append(_card_head(752, 136, 812, 732, PURPLE, "SPECULATIVE DECODING TOKEN-TREE (DRAFT K=5 -> VERIFY IN 1 PASS)"))

    # Top comparison inside Right Panel: Standard Autoregressive vs Speculative
    b.append(_r(770, 182, 776, 136, 10, "#FEF2F2", RED, 1.5))
    b.append(_t(788, 204, "STANDARD AUTOREGRESSIVE DECODE: 5 SEQUENTIAL 70B HBM READS = 160 ms", 10, 800, RED))
    for k, tok in enumerate(["sha256", "(", "raw", ".encode()", ")[:8]"]):
        tx = 788 + k * 150
        b.append(_r(tx, 218, 132, 46, 6, WHITE, RED, 1.4))
        b.append(_t(tx + 66, 238, f"Pass {k+1} (70 GB HBM)", 8.5, 700, RED, "middle"))
        b.append(_t(tx + 66, 254, f"-> '{tok}'", 9.5, 800, INK, "middle", mono=True))
        if k < 4:
            b.append(_fl([(tx + 132, 241), (tx + 150, 241)], RED, phase, 1.0))
    b.append(_t(788, 294, "Bottleneck: Streaming 70 GB of weights 5 separate times = 350 GB moved from HBM to SRAM.", 9.5, 700, "#7F1D1D"))

    # Middle: Speculative Token-Tree Verification (y=332..674)
    b.append(_r(770, 332, 776, 342, 10, "#ECFDF5", GREEN, 1.6))
    b.append(_t(788, 356, "SPECULATIVE DRAFT-VERIFY LOOP (EAGLE-2 / MEDUSA): 1 SINGLE 70B HBM READ = 58 ms (2.7x FASTER)", 10, 800, "#065F46"))

    # Step A: Fast Draft Tree
    b.append(_r(788, 372, 220, 132, 8, WHITE, PURPLE, 1.6))
    b.append(_t(898, 394, "1. DRAFT HEAD / 1B MODEL", 9.8, 800, PURPLE, "middle"))
    b.append(_t(898, 414, "Fits in SRAM / fast cache", 9, 600, SLATE, "middle"))
    b.append(_t(898, 434, "Proposes K=5 token tree", 9.5, 700, INK, "middle"))
    b.append(_t(898, 454, "in just 6 ms total", 9.5, 800, PURPLE, "middle", mono=True))
    b.append(_pill(818, 470, "Prompt: 'return hashlib.'", PURPLE, size=8.5, h=20)[0])

    b.append(_fl([(1008, 438), (1046, 438)], PURPLE, phase, 1.2))

    # Step B: Candidate Token Tree + Parallel 70B Verifier Pass
    b.append(_r(1048, 372, 480, 192, 8, WHITE, GREEN, 1.6))
    b.append(_t(1064, 394, "2. TARGET 70B MODEL SCORES ALL 5 CANDIDATES IN 1 PARALLEL PASS", 9.5, 800, "#065F46"))
    tree_nodes = [
        ("t1: 'sha256'", "ACCEPT (p=0.99)", GREEN, 1064, 412),
        ("t2: '('", "ACCEPT (p=0.98)", GREEN, 1220, 412),
        ("t3: 'raw'", "ACCEPT (p=0.95)", GREEN, 1376, 412),
        ("t4: '.encode()'", "ACCEPT (p=0.94)", GREEN, 1064, 484),
        ("t5a: '.digest()'", "REJECT (p=0.11)", RED, 1220, 484),
        ("t5b: ').hexdigest()'", "CORRECTED BY 70B", BLUE, 1376, 484),
    ]
    for t_tok, t_stat, t_col, nx, ny in tree_nodes:
        b.append(_r(nx, ny, 140, 56, 6, "#F8FAFC", t_col, 1.5))
        b.append(_t(nx + 70, ny + 22, t_tok, 9.2, 800, INK, "middle", mono=True))
        b.append(_t(nx + 70, ny + 42, t_stat, 8.2, 800, t_col, "middle"))

    b.append(_r(788, 576, 740, 86, 8, WHITE, TEAL, 1.5))
    b.append(_t(804, 596, "3. WHY IT IS MATHEMATICALLY LOSSLESS (EXACT TARGET DISTRIBUTION)", 9.8, 800, TEAL))
    b.append(_tl(804, 614, _wrap(s["lossless_note"], 108, 3), 9.2, 600, INK, 13.5))

    # Bottom Stack & Takeaway Card inside Right Panel (y=688..852)
    b.append(_r(770, 688, 776, 164, 10, "#F8FAFC", LINE, 1.5))
    b.append(_t(788, 712, "THREE SPECULATIVE DECODING ARCHITECTURES IN PRODUCTION", 10, 800, NAVY))
    for i, arch in enumerate(s["spec_archs"][:3]):
        ax = 788 + i * 252
        b.append(_r(ax, 726, 240, 112, 8, WHITE, arch["color"], 1.4))
        b.append(_t(ax + 12, 746, arch["name"], 9.8, 800, arch["color"]))
        b.append(_tl(ax + 12, 764, _wrap(arch["how"], 33, 3), 9, 600, INK, 13))
        b.append(_t(ax + 12, 822, arch["speedup"], 9, 800, arch["color"], mono=True))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T51", META["T51"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T52 — Reasoning Model Post-Training Pipeline (Base Pre-Train -> SFT -> GRPO / RLVR -> Test-Time Compute)
# ----------------------------------------------------------------------------------------------------------------------
def render_t52(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []

    # Top 4-Stage Post-Training & Test-Time Scaling Pipeline (y=136..546)
    for i, st in enumerate(s["stages"][:4]):
        sx = 56 + i * 382
        col = st["color"]
        b.append(_card_head(sx, 136, 362, 410, col, f"STAGE 0{i + 1} • {st['name']}", head_h=32))
        b.append(_t(sx + 16, 192, st["goal"], 10.5, 800, col))
        b.append(_tl(sx + 16, 212, _wrap(st["how"], 48, 4), 9.8, 600, INK, 14))

        # Formula / Mechanism Box
        b.append(_r(sx + 16, 276, 330, 136, 8, "#0F172A", col, 1.5))
        b.append(_t(sx + 28, 298, st["box_head"], 9.2, 800, "#93C5FD", mono=True))
        for k, fln in enumerate(st["box_lines"][:5]):
            b.append(_t(sx + 28, 318 + k * 18, fln, 9, 600, "#86EFAC" if k == len(st["box_lines"]) - 1 else "#E2E8F0", mono=True))

        # Data / Compute Footprint
        b.append(_r(sx + 16, 424, 330, 106, 8, "#F8FAFC", col, 1.3))
        b.append(_t(sx + 28, 444, f"DATA / COMPUTE: {st['scale']}", 9.2, 800, col))
        b.append(_tl(sx + 28, 462, _wrap(st["takeaway"], 46, 3), 9.2, 600, "#1E293B", 13))
        b.append(_pill(sx + 28, 504, st["stack"], col, size=8.2, h=18)[0])

        if i < 3:
            b.append(_fl([(sx + 362, 340), (sx + 382, 340)], col, phase, 1.2))

    # Bottom Left: PPO vs. GRPO Architecture & Memory Comparison (x=56..796, y=562..868)
    b.append(_card_head(56, 562, 740, 306, PURPLE, "WHY GRPO REPLACED PPO FOR REASONING MODELS (~50% LESS RL VRAM)"))
    b.append(_r(74, 604, 340, 184, 8, "#FEF2F2", RED, 1.5))
    b.append(_t(90, 626, "TRADITIONAL PPO (4 MODELS IN VRAM)", 9.8, 800, RED))
    for k, mname in enumerate(["1. Policy Model (Trainable 70B)", "2. Reference Model (Frozen 70B)", "3. Reward Model (Frozen 70B)", "4. Value / Critic Model (Trainable 70B)"]):
        b.append(_r(90, 638 + k * 34, 308, 28, 5, WHITE, RED if k >= 2 else "#94A3B8", 1.2))
        b.append(_t(102, 656 + k * 34, mname, 9.2, 700, INK))

    b.append(_r(436, 604, 342, 184, 8, "#ECFDF5", GREEN, 1.5))
    b.append(_t(452, 626, "DEEPSEEK-R1 GRPO + RLVR (NO CRITIC MODEL)", 9.8, 800, "#065F46"))
    for k, mname in enumerate(["1. Policy Model (Trainable — samples G=8 outputs)", "2. Reference Model (Frozen — KL divergence guard)", "3. Deterministic Sandbox Verifier (pytest / math)", "4. Group Advantage: A_i = (r_i - mean(r)) / std(r)"]):
        b.append(_r(452, 638 + k * 34, 310, 28, 5, WHITE, GREEN, 1.4))
        b.append(_t(464, 656 + k * 34, mname, 9.0, 700, "#064E3B"))

    b.append(_r(74, 798, 704, 58, 8, "#F5F3FF", PURPLE, 1.4))
    b.append(_t(90, 816, "KEY INSIGHT (SEBASTIAN RASCHKA):", 9.2, 800, PURPLE))
    b.append(_tl(90, 833, _wrap(s["ppo_vs_grpo_note"], 114, 2), 9.0, 700, INK, 12.5))

    # Bottom Right: Enterprise Decision Matrix — Prompt Harness vs. SFT vs. RLVR (x=816..1564, y=562..868)
    b.append(_card_head(816, 562, 748, 306, NAVY, "ENTERPRISE PLAYBOOK: WHEN TO USE HARNESS VS. SFT VS. GRPO / RLVR"))
    for i, opt in enumerate(s["playbook"][:3]):
        oy = 608 + i * 82
        col = opt["color"]
        b.append(_r(834, oy, 712, 72, 8, "#F8FAFC", col, 1.5))
        b.append(_r(834, oy, 8, 72, 4, col))
        b.append(_t(852, oy + 22, opt["level"], 10.5, 800, col))
        b.append(_t(1530, oy + 22, opt["cost"], 9.5, 800, col, "end", mono=True))
        b.append(_tl(852, oy + 40, _wrap(opt["when"], 96, 2), 9.5, 600, INK, 14))

    b.append(_r(56, 884, 1508, 44, 10, NAVY))
    b.append(_t(810, 911, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T52", META["T52"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# Metadata + Demo Specs for T41-T52
# ----------------------------------------------------------------------------------------------------------------------
META: Dict[str, Dict[str, Any]] = {
    "T41": {
        "name": "Systems Deep-Dive Engraving",
        "best_for_short": "LLM inference load balancing & KV routing",
        "content_types": ["Grounded concepts", "Educational", "Working solution"],
        "when_to_use": "Explain low-level GPU serving mechanics (prefill vs decode, Radix prefix-cache affinity, least-KV-pressure routing, chunked prefill).",
        "dynamic": "Requests flow through the Radix Prefix Router to 4 GPU workers; KV HBM bars fill dynamically.",
        "lineage": "Kavi Priyan (#01, 607 likes) • Sahn Lam • SGLang RadixAttention / vLLM",
    },
    "T42": {
        "name": "Recursive Agent Harness",
        "best_for_short": "Harness² dual-loop self-improving agents",
        "content_types": ["Research topics", "Grounded concepts", "Evaluation results"],
        "when_to_use": "Show how agents improve at both task-level (Propose->Probe->Compose skill graphs) and harness-level without retraining model weights.",
        "dynamic": "Packets traverse Loop 1 (Propose->Probe->Compose), the 5 concentric rings, and Loop 2 benchmark bars.",
        "lineage": "Gurisa Roy (#02, 201 likes) • Keith R. Worfolk (#03) • Google & Northwestern Harness²",
    },
    "T43": {
        "name": "Self-Correcting Memory",
        "best_for_short": "LangChain OpenWiki SHA evidence receipts",
        "content_types": ["Working solution", "Evaluation results", "Grounded concepts"],
        "when_to_use": "Show how to stop agent memory rot by binding claims to Git blob SHAs, running O(1) staleness checks, and self-correcting in the flow of work.",
        "dynamic": "Packets flow across the 4-stage OpenWiki pipeline from SHA receipt storage to in-flow self-correction.",
        "lineage": "Ravena O & Rakesh Gohel (#05, 88 likes) • LangChain OpenWiki",
    },
    "T44": {
        "name": "Deep Research Verifier",
        "best_for_short": "Deterministic citation check + JEV loop",
        "content_types": ["Working solution", "Evaluation results", "Proof of concept"],
        "when_to_use": "Architect a deep research agent that verifies every URL and quote span deterministically before running a bounded JEV judge retry loop.",
        "dynamic": "Packets traverse stages 01->06 with an animated conditional RESEARCH_AGAIN loop from Stage 05 back to Stage 02.",
        "lineage": "Sumanth P (#04, 124 likes) • LangChain Deep Agents + JEV + Tavily + LangSmith",
    },
    "T45": {
        "name": "Executive ROI Crossover Funnel",
        "best_for_short": "Agentic AI value funnel: First run to P&L",
        "content_types": ["Professional knowledge sharing", "Ideas", "Evaluation results"],
        "when_to_use": "Show executives how falling human touches cross rising business value above the Pilot Ceiling across 6 stages from Work Done to P&L.",
        "dynamic": "Dual crossover curves draw across the Pilot Ceiling while packets advance through the 6 C-suite value stages.",
        "lineage": "Jonny Tooze (#11, 141 likes, 144 comments) • Executive AI Value Realization",
    },
    "T46": {
        "name": "Cloverleaf Governance Venn",
        "best_for_short": "CEO vs. CTO vs. CIO vs. CISO AI charter",
        "content_types": ["Professional knowledge sharing", "Grounded concepts", "Easy to understand"],
        "when_to_use": "Clarify C-suite AI responsibilities and the 6 pairwise overlap charters across Demo -> Pilot -> Production -> Enterprise scale.",
        "dynamic": "4-circle cloverleaf Venn diagram with pairwise intersection pills and 6 structured charter cards.",
        "lineage": "Alok Sharan (#14, 63 likes) & Matthew Coombs (#08, 51 likes)",
    },
    "T47": {
        "name": "Global AI Regulatory Matrix",
        "best_for_short": "4x5 cheat sheet of 20 global AI laws",
        "content_types": ["Information", "Professional knowledge sharing", "Educational"],
        "when_to_use": "Give engineering and legal leaders a one-page 4x5 reference of 20 global AI laws, standards, and the exact technical gate each requires.",
        "dynamic": "20 color-coded regulatory cards across Europe, Global Standards, US Federal/State, and APAC.",
        "lineage": "Prashant Rathi (#09, 203 likes, 68 comments) • Global AI Policy Matrix",
    },
    "T48": {
        "name": "8-Tier AI Maturity Pyramid",
        "best_for_short": "8 maturity tiers + 10-step build order",
        "content_types": ["Educational", "Grounded concepts", "Professional knowledge sharing"],
        "when_to_use": "Pair an 8-tier ascending production AI pyramid with the 10-step prerequisite build order and what breaks when teams skip tiers.",
        "dynamic": "8 ascending pyramid tiers flanked by the 10-step build sequence and 4 skipped-tier failure cards.",
        "lineage": "Prashant Rathi (#12, 53 likes) & Jonathan Parsons (#10, 71 likes)",
    },
    "T49": {
        "name": "Automation Decision Triptych",
        "best_for_short": "Rules vs. AI Workflows vs. AI Agents",
        "content_types": ["Easy to understand", "Educational", "Grounded concepts"],
        "when_to_use": "Help teams choose between deterministic automation, code-orchestrated AI workflows, and autonomous AI agents side by side.",
        "dynamic": "3 parallel decision columns with live 3-node mini-flows, latency/cost profiles, and a bottom rule bar.",
        "lineage": "Prem Natarajan (#13, 59 likes, 53 comments) & Chip Huyen",
    },
    "T50": {
        "name": "Stacked Dual-Protocol Sequence",
        "best_for_short": "OAuth 2.0 + PKCE vs. OIDC + Agent OBO",
        "content_types": ["Educational", "Grounded concepts", "Working solution"],
        "when_to_use": "Compare two related security protocols vertically: OAuth 2.0 + PKCE delegated access vs. OIDC + RFC 8693 On-Behalf-Of agent token exchange.",
        "dynamic": "14 numbered opaque-pill messages travel across 4 actor lifelines in two stacked protocol panels.",
        "lineage": "Alex Xu / ByteByteGo (#07) & Shalini Goyal (#06) • RFC 8693 Agent Identity",
    },
    "T51": {
        "name": "GPU Memory & Speculative Tree",
        "best_for_short": "SRAM vs. HBM + Speculative Decode 2.7x",
        "content_types": ["Grounded concepts", "Educational", "Research topics"],
        "when_to_use": "Show why autoregressive LLM decoding is memory-bandwidth-bound on HBM and how speculative decoding verifies 5 draft tokens in 1 pass.",
        "dynamic": "3-tier GPU memory pyramid + worked roofline math on the left; live draft-verify token tree on the right.",
        "lineage": "Sahn Lam & Umar Jamil • EAGLE-2 / Medusa / FlashAttention-3",
    },
    "T52": {
        "name": "Reasoning Post-Training Pipeline",
        "best_for_short": "SFT -> GRPO -> RLVR -> Test-Time Compute",
        "content_types": ["Research topics", "Educational", "Grounded concepts"],
        "when_to_use": "Explain how modern reasoning models are trained (Cold-start SFT -> GRPO without a critic model -> RLVR deterministic rewards -> Test-Time scaling).",
        "dynamic": "4-stage horizontal post-training pipeline + PPO vs. GRPO VRAM comparison + enterprise customization playbook.",
        "lineage": "Sebastian Raschka & Maxime Labonne • DeepSeek-R1 GRPO & RLVR",
    },
}

RENDERERS_V3 = {
    "T41": render_t41, "T42": render_t42, "T43": render_t43, "T44": render_t44,
    "T45": render_t45, "T46": render_t46, "T47": render_t47, "T48": render_t48,
    "T49": render_t49, "T50": render_t50, "T51": render_t51, "T52": render_t52,
}


def demo_specs_v3() -> Dict[str, Dict[str, Any]]:
    return {
        "T41": {
            "title": "Load Balancing for LLM Inference: Why Round-Robin Fails and How Prefix-Aware KV Routing Fixes It",
            "subtitle": "LLM requests are stateful and asymmetric: a 32K prefill saturates compute while a 200-token decode starves on HBM bandwidth.",
            "source": "Kavi Priyan, 'Load Balancing for LLM Inference' • SGLang RadixAttention (Zheng et al.) • vLLM PagedAttention • GKE Inference Gateway",
            "lineage": "Kavi Priyan (#01, 607 likes) • Sahn Lam • SGLang RadixAttention / vLLM",
            "problem_left": "Traditional HTTP load balancers treat every request as equal and stateless. In multi-turn agent loops, Turn 12 shares 92% of its prompt prefix with Turns 1-11. Round-robin scatters Turn 12 to a cold GPU worker, forcing it to recompute 28,000 prefill tokens from scratch while stalling active decode batches.",
            "compare_bars": [
                {"label": "Naive Round-Robin", "frac": 0.92, "color": RED, "metrics": "TTFT: 850ms | KV Hit: 12.0%"},
                {"label": "Prefix + KV Router", "frac": 0.24, "color": GREEN, "metrics": "TTFT: 185ms | KV Hit: 84.6%"},
            ],
            "requests": [
                {"id": "REQ #401 • Turn 12 Coding Agent", "prefix": "prefix_sha: 9f3a (24K tok)", "tokens": "+ 600 new diff tokens", "route_tag": "AFFINITY -> WORKER 02", "color": BLUE},
                {"id": "REQ #402 • Turn 6 Support Agent", "prefix": "prefix_sha: c41e (8K tok)", "tokens": "+ 350 new tool tokens", "route_tag": "AFFINITY -> WORKER 01", "color": GREEN},
                {"id": "REQ #403 • Cold Document Summary", "prefix": "prefix_sha: 7b12 (new)", "tokens": "14K cold prefill tokens", "route_tag": "LEAST KV -> WORKER 04", "color": TEAL},
            ],
            "radix_table": [
                "9f3a (24K) -> Worker 02 [HOT]",
                "c41e (8K)  -> Worker 01 [HOT]",
                "e801 (64K) -> Worker 03 [94% FULL]",
            ],
            "workers": [
                {"name": "GPU Worker 01 (H100 80GB)", "status": "ACTIVE • 18 REQS", "kv_pct": 62, "prefix_held": "Radix: [c41e, a12b]", "detail": "ITL: 11.2 ms • Serves REQ #402 with 8K cached KV blocks", "color": GREEN, "fill": "#F8FAFC"},
                {"name": "GPU Worker 02 (H100 80GB)", "status": "PREFIX HIT • 14 REQS", "kv_pct": 48, "prefix_held": "Radix: [9f3a (24K)]", "detail": "TTFT: 185 ms (-78%) • Reuses 24K KV tokens for REQ #401", "color": BLUE, "fill": "#EFF6FF"},
                {"name": "GPU Worker 03 (H100 80GB)", "status": "BYPASSED • KV 94%", "kv_pct": 94, "prefix_held": "Radix: [e801 (64K)]", "detail": "Saturated HBM + long prefill running -> router diverts new traffic", "color": RED, "fill": "#FEF2F2"},
                {"name": "GPU Worker 04 (H100 80GB)", "status": "LOWEST KV • 6 REQS", "kv_pct": 24, "prefix_held": "Radix: [cold pool]", "detail": "76% free HBM -> absorbs cold 14K prefill (REQ #403) cleanly", "color": TEAL, "fill": "#F0FDFA"},
            ],
            "zoom_a_note": "Splitting long prompts into 2,048-token prefill chunks lets decode tokens piggyback on every iteration — keeping P95 ITL under 15 ms.",
            "zoom_b_note": "Separating Prefill GPUs from Decode GPUs (DistServe / Mooncake / vLLM Disaggregated) stops compute-heavy prompts from starving token streaming.",
            "strategies": [
                {"title": "LEAST-KV-PRESSURE ROUTING", "gain": "-94% OOM / Evictions", "color": BLUE, "how": "Route based on live GPU HBM KV-cache block utilization and waiting prefill tokens — never by raw active HTTP connection count.", "when": "Variable-length prompts (1K to 128K tokens)", "stack": "GKE Inference Gateway ⇄ Envoy + vLLM metrics"},
                {"title": "PREFIX-AWARE RADIX AFFINITY", "gain": "84.6% KV Hit Rate", "color": PURPLE, "how": "Maintain a distributed Radix tree of prompt prefixes across workers; route multi-turn agent calls to the GPU holding their system+tool+history KV blocks.", "when": "Multi-turn agents & shared 20K+ system prompts", "stack": "SGLang RadixAttention ⇄ llm-d / AIBrix router"},
                {"title": "CHUNKED PREFILL + DISAGGREGATION", "gain": "3.1x SLA Goodput", "color": GREEN, "how": "Cap prefill batch chunks to 2K tokens on mixed pools, or disaggregate Prefill and Decode onto dedicated GPU pools connected via NVLink/RDMA.", "when": "Strict dual SLOs: TTFT < 250ms and ITL < 15ms", "stack": "vLLM --enable-chunked-prefill ⇄ Mooncake / DistServe"},
            ],
            "rule": "Rule: Route LLM traffic by (Prefix Overlap − HBM KV Pressure − Queued Prefill Tokens), never by round-robin request count.",
        },
        "T42": {
            "title": "Google Harness²: How Recursive Self-Improving Harnesses Beat Static Agents Without Retraining Weights",
            "subtitle": "Most 'agent failures' are harness failures. Harness² adds two recursive loops around a frozen model: Task-Level Skill Graphs and Harness-Level Evolution.",
            "source": "Harness² (Northwestern University & Google Cloud AI Research, harness2.github.io) • Gurisa Roy (#02) • Keith R. Worfolk (#03)",
            "lineage": "Gurisa Roy (#02, 201 likes) • Keith R. Worfolk (#03) • Google & Northwestern Harness²",
            "task_loop": [
                {"name": "PROPOSE (Decompose Skill Graph)", "tag": "STEP 1", "color": BLUE, "body": "Analyze the user goal and current workspace state; propose a candidate DAG of modular skills and explicit verification assertions.", "artifact": "Artifact: candidate_skill_dag.json"},
                {"name": "PROBE (Execute & Observe in Sandbox)", "tag": "STEP 2", "color": PURPLE, "body": "Run candidate sub-skills inside an isolated gVisor / E2B container; capture deterministic exit codes, stderr tracebacks, and state diffs.", "artifact": "Artifact: probe_trace + exit_code"},
                {"name": "COMPOSE (Prune & Lock Verified Graph)", "tag": "STEP 3", "color": GREEN, "body": "Discard failing branches, repair broken tool arguments from probe feedback, and compose the verified sub-skills into the active execution path.", "artifact": "Artifact: verified_skill_chain.md"},
            ],
            "why_static_fails": "Static harnesses hardcode one prompt template, one tool list, and one retry rule for every task. When an enterprise workflow hits an unfamiliar schema or multi-step edge case, a static harness repeats the same broken call until max_steps expires.",
            "six_steps": [
                {"name": "OBSERVE", "color": BLUE, "desc": "Load pinned rules, SHA memory receipts, and Top-3 routed MCP tools."},
                {"name": "PLAN", "color": PURPLE, "desc": "Propose skill DAG and deterministic test assertions before mutating state."},
                {"name": "ACT", "color": AMBER, "desc": "Execute CodeAct / tool call with idempotency key in gVisor sandbox."},
                {"name": "VERIFY", "color": GREEN, "desc": "Run deterministic exit_code==0 test + schema check on output."},
                {"name": "REFINE SKILL", "color": TEAL, "desc": "On failure, diff reference trace and patch the local skill node."},
                {"name": "PROMOTE", "color": NAVY, "desc": "If snapshot pool improves with 0 regressions, commit to harness."},
            ],
            "harness_loop": [
                {"head": "Mine Cross-Task Divergences", "sub": "Cluster failed steps across production trajectories by error signature."},
                {"head": "Synthesize Harness Patch", "sub": "Generate targeted edit to SKILL.md, tool schema, or guardrail code."},
                {"head": "Tier-1 Anti-Bloat & Leak Gate", "sub": "Reject patches that grow prompt >15% or hardcode benchmark answers."},
                {"head": "Tier-2 Snapshot Pool Promotion", "sub": "Promote only if peak score rises AND 100% of golden fixtures pass."},
            ],
            "benchmarks": [
                {"name": "WorkBuddy-Bench (Enterprise Workflows)", "base": 47.5, "after": 59.0, "delta": "+11.5 pts", "color": BLUE},
                {"name": "JobBench (Multi-Step Tool Tasks)", "base": 59.4, "after": 63.9, "delta": "+4.5 pts", "color": PURPLE},
                {"name": "LAB Benchmark (Long-Horizon Agents)", "base": 51.8, "after": 63.6, "delta": "+11.8 pts", "color": GREEN},
            ],
            "core_insight": "Upgrading the model while keeping a brittle harness yields diminishing returns. Making the harness itself recursive — proposing, probing, and composing skills per task while evolving instructions across tasks — unlocks +4.5 to +11.8 points on the exact same frozen model.",
            "rule": "Rule: Freeze the model weights, evolve the harness — Loop 1 adapts the skill graph per task; Loop 2 promotes verified patches across tasks.",
        },
        "T43": {
            "title": "Teaching AI Agents How to Forget: LangChain OpenWiki's Self-Correcting Memory Architecture",
            "subtitle": "Long-lived agents rot when yesterday's true memory becomes today's hallucination. Bind every stored claim to a Git blob SHA receipt.",
            "source": "LangChain OpenWiki case study • Ravena O & Rakesh Gohel, 'Teaching AI Agents How to Forget' (#05) • Firestore / PostgreSQL + Git",
            "lineage": "Ravena O & Rakesh Gohel (#05, 88 likes) • LangChain OpenWiki",
            "problem_banner": "Most agent memory layers (vector DBs, summary notes) only know how to append. When an engineer renames a function or updates an API contract, the agent retrieves last month's memory note and confidently writes broken code.",
            "solution_banner": "Never store a naked text summary. Store an Evidence Receipt (file_path, line_span, git_blob_sha). On retrieval, run a 0-token O(1) hash comparison against current Git HEAD and self-correct stale claims in the flow of work.",
            "stages": [
                {
                    "title": "STORE EVIDENCE RECEIPTS",
                    "subtitle": "Bind every memory claim to a cryptographic source SHA",
                    "color": BLUE,
                    "body": "When the agent learns an architectural fact, persist the exact file path, line range, and Git blob SHA alongside the claim.",
                    "code_head": "memory_record.json (Firestore / Postgres)",
                    "code_lines": [
                        "{",
                        "  \"claim\": \"refresh_token grace is 60s\",",
                        "+ \"file\": \"src/auth/refresh.py\",",
                        "+ \"lines\": \"L42-L68\",",
                        "+ \"git_blob_sha\": \"a94f21c8\",",
                        "  \"verified_at\": \"2026-10-18T09:15Z\"",
                        "}",
                    ],
                    "note_fill": "#EFF6FF",
                    "note_head": "RULE 01 • NO NAKED SUMMARIES",
                    "note_body": "A claim without a verifiable pointer (blob_sha, doc_version, row_etag) is banned from long-term semantic memory.",
                },
                {
                    "title": "O(1) STALENESS CHECK",
                    "subtitle": "Deterministic version check on read (0 LLM tokens)",
                    "color": PURPLE,
                    "body": "Before injecting any retrieved memory into the prompt, compare its stored git_blob_sha against the current repository tree in <2 ms.",
                    "code_head": "staleness_gate.py (Deterministic Hook)",
                    "code_lines": [
                        "def check_receipt(rec, git_tree):",
                        "    cur_sha = git_tree.get_sha(rec.file)",
                        "    if cur_sha is None:",
                        "!       return 'MOVED_OR_DELETED'",
                        "    if cur_sha != rec.git_blob_sha:",
                        "!       return 'STALE_SHA_MISMATCH'",
                        "+   return 'TRUSTED_FRESH'",
                    ],
                    "note_fill": "#F5F3FF",
                    "note_head": "RULE 02 • DETERMINISTIC FRESHNESS",
                    "note_body": "Never ask an LLM 'is this memory still true?' — hash comparison + git rename detection costs $0.00 and never hallucinates.",
                },
                {
                    "title": "FLAG, DON'T AUTO-DELETE",
                    "subtitle": "Preserve historical context while preventing blind trust",
                    "color": AMBER,
                    "body": "Auto-deleting on mismatch loses valuable architectural intent. Instead, tag the memory as STALE_REVERIFY with the diff commit.",
                    "code_head": "context_injection_banner.txt",
                    "code_lines": [
                        "[MEMORY #104 • STATUS: STALE_REVERIFY]",
                        "! Warning: src/auth/refresh.py changed",
                        "! Stored SHA: a94f21c8 != HEAD: f31d90e2",
                        "  Prior claim: 'grace window is 60s'",
                        "+ Action required: Read L42-L75 of",
                        "+ src/auth/refresh.py before answering.",
                        "",
                    ],
                    "note_fill": "#FFFBEB",
                    "note_head": "RULE 03 • GRACEFUL DEGRADATION",
                    "note_body": "The stale claim tells the agent *where* to look; the warning flag stops the agent from quoting the old number as fact.",
                },
                {
                    "title": "SELF-CORRECT IN FLOW",
                    "subtitle": "Re-read changed span and mint a fresh SHA receipt",
                    "color": GREEN,
                    "body": "During its normal task turn, the agent reads only the modified lines, updates the memory claim, and writes the new Git blob SHA.",
                    "code_head": "updated_memory_record.json",
                    "code_lines": [
                        "{",
                        "+ \"claim\": \"refresh_token grace is 120s\",",
                        "  \"file\": \"src/auth/refresh.py\",",
                        "  \"lines\": \"L42-L75\",",
                        "+ \"git_blob_sha\": \"f31d90e2\",",
                        "+ \"prev_sha\": \"a94f21c8\",",
                        "  \"status\": \"TRUSTED_FRESH\"",
                        "}",
                    ],
                    "note_fill": "#ECFDF5",
                    "note_head": "RULE 04 • ZERO BACKGROUND CRON DRIFT",
                    "note_body": "Memory heals itself on the exact hot paths engineers actually query, keeping active knowledge 98% supported.",
                },
            ],
            "metrics": [
                {"value": "80 -> 9", "label": "Stale claims remaining (-88.8%)", "sub": "After 1 self-correcting checkpoint pass", "color": GREEN},
                {"value": "15 -> 0", "label": "Hallucinated claims (-100%)", "sub": "Eliminated by mandatory span + SHA receipts", "color": BLUE},
                {"value": "98.0%", "label": "Claims supported at next checkpoint", "sub": "Verified against live repository HEAD", "color": PURPLE},
                {"value": "0 tok", "label": "LLM tokens spent on staleness detection", "sub": "100% deterministic O(1) Git blob SHA lookup", "color": TEAL},
            ],
            "rule": "Rule: An agent memory without a source SHA receipt is a future hallucination waiting for the next code commit.",
        },
        "T44": {
            "title": "Deep Research Agent with Deterministic Citation Verification and a Bounded JEV Review Loop",
            "subtitle": "Never ship a research report just because an LLM formatted citations nicely — verify URLs & quote spans in Python, then run a 1-retry JEV gate.",
            "source": "Sumanth P (#04, 124 likes) • LangChain Deep Agents + JEV (Judge-Evaluator-Verifier) + Tavily + Vertex AI / Nebius + LangSmith",
            "lineage": "Sumanth P (#04, 124 likes) • LangChain Deep Agents + JEV + Tavily + LangSmith",
            "pipeline": [
                {"name": "RESEARCH QUERY", "role": "Scope & Rubric", "color": "#334155", "desc": "Decompose open question into sub-questions, required source tiers, and freshness cutoff.", "stack": "Pydantic ResearchBrief"},
                {"name": "DEEP AGENT", "role": "Parallel Search", "color": BLUE, "desc": "Fan out parallel sub-queries, fetch full page markdown, and store raw source snapshots.", "stack": "LangGraph + Tavily / Vertex"},
                {"name": "CITED DRAFT", "role": "Inline Receipts", "color": PURPLE, "desc": "Synthesize report where every claim binds to [source_id, url, exact_quote_span].", "stack": "Gemini 3.8 / DeepSeek-R1"},
                {"name": "CITATION CHECK", "role": "Deterministic Python", "color": TEAL, "desc": "Verify URL exists in fetched cache, HTTP 200, and exact_quote_span matches source text.", "stack": "Zero-LLM Python Gate"},
                {"name": "JEV VERIFIER", "role": "Judge-Evaluator", "color": AMBER, "desc": "Grade coverage, cross-source contradictions, and whether citations actually prove the claim.", "stack": "JEV Binary Rubric"},
                {"name": "VERIFIED REPORT", "role": "Ship + Audit Trace", "color": GREEN, "desc": "Emit final markdown report + verifiable citation ledger + full trace link.", "stack": "LangSmith / Cloud Trace"},
            ],
            "panels": [
                {
                    "title": "WHY NAIVE RESEARCH AGENTS FAIL IN PRODUCTION",
                    "color": RED,
                    "items": [
                        {"head": "Plausible but fabricated URLs", "body": "Models synthesize realistic-looking paths (/blog/2025-ai-report) that return HTTP 404."},
                        {"head": "Citation laundering (unrelated quote)", "body": "The URL is real, but the linked paragraph says nothing about the number claimed in the sentence."},
                        {"head": "Silent contradiction dropping", "body": "When Source A says 14% and Source B says 42%, naive prompts pick one and hide the conflict."},
                        {"head": "Unbounded research loops", "body": "Without a hard retry cap (max_retries=1), self-reflecting agents burn $4+ searching forever."},
                    ],
                },
                {
                    "title": "STAGE 04: DETERMINISTIC CITATION CHECK (PYTHON)",
                    "color": TEAL,
                    "items": [
                        {"head": "Cache-provenance check", "body": "Every cited URL must exist in the session's fetched_sources[] table — zero unvisited links allowed."},
                        {"head": "Normalized substring / fuzzy span match", "body": "Verify exact_quote_span appears in the cached document text (token overlap >= 0.95)."},
                        {"head": "Numeric & entity grounding check", "body": "Every percentage, dollar figure, or benchmark score in prose must appear in its linked span."},
                        {"head": "Domain & date policy enforcement", "body": "Block denylisted low-trust domains and flag sources older than max_age_days."},
                    ],
                },
                {
                    "title": "STAGE 05: JEV GATE & BOUNDED RETRY CONTRACT",
                    "color": GREEN,
                    "items": [
                        {"head": "Structured JEV verdict schema", "body": "Outputs {\"decision\": \"APPROVE | RESEARCH_AGAIN\", \"failed_claims\": [...], \"queries\": [...]}."},
                        {"head": "Targeted delta search (not a full restart)", "body": "On RESEARCH_AGAIN, Stage 02 runs only the 2-3 missing-evidence queries keeping valid sections intact."},
                        {"head": "Hard ceiling: max_retries = 1", "body": "If a claim still lacks evidence after 1 targeted retry, label it [UNVERIFIED IN SOURCES] explicitly."},
                        {"head": "Full observability trace", "body": "Every search query, deterministic span check, and JEV verdict is logged to LangSmith / OpenTelemetry."},
                    ],
                },
            ],
            "rule": "Rule: Verify URLs and quote spans with deterministic code first; use the LLM judge (JEV) only to grade semantic support and trigger at most 1 retry.",
        },
        "T45": {
            "title": "The Agentic AI Value Funnel: How to Cross the Pilot Ceiling From 'Work Done' to Real P&L",
            "subtitle": "Most AI projects die at Stage 02 ('it ran fast in a demo') because humans still check every output. Real ROI starts at the Crossover.",
            "source": "Jonny Tooze, 'The Agentic AI Value Funnel' (#11, 141 likes, 144 comments) • ScoreX CFO Value Realization Framework",
            "lineage": "Jonny Tooze (#11, 141 likes, 144 comments) • Executive AI Value Realization",
            "unlock_gates": [
                {"head": "DETERMINISTIC PRE-COMPLETION VERIFICATION", "body": "Humans stop reviewing 100% of outputs only when a sandboxed test, schema check, or citation verifier guarantees exit_code == 0.", "color": BLUE},
                {"head": "CONFIDENCE-ROUTED EXCEPTION QUEUES", "body": "Auto-commit the 85% of runs that pass all deterministic gates; route only the 15% flagged anomalies to human reviewers.", "color": PURPLE},
                {"head": "OUTCOME-BASED FINOPS ($ / RESOLVED TASK)", "body": "Stop reporting 'tokens consumed' or 'hours saved on a survey'; track fully loaded cost per verified business outcome.", "color": GREEN},
            ],
            "funnel": [
                {"short": "Work Done", "name": "WORK DONE", "owner": "ENG LEAD", "color": "#475569", "human_pct": 95, "value_pct": 12, "kpi_value": "94.2%", "kpi_label": "First-pass task completion", "question": "Can the agent actually complete the workflow end-to-end?", "proof": "Golden eval suite pass rate >= 90% on 100 real production traces."},
                {"short": "Speed", "name": "SPEED", "owner": "CTO / VP ENG", "color": BLUE, "human_pct": 78, "value_pct": 28, "kpi_value": "4h -> 6m", "kpi_label": "End-to-end cycle time (-97%)", "question": "Does it compress turnaround time from hours to minutes?", "proof": "P95 turn latency & time-to-resolution logged in Cloud Trace / Langfuse."},
                {"short": "Human Load", "name": "HUMAN LOAD", "owner": "OPS LEAD", "color": PURPLE, "human_pct": 42, "value_pct": 48, "kpi_value": "8.4 -> 0.4", "kpi_label": "Human touches per outcome", "question": "Did humans step back from doing the work to governing the gates?", "proof": "% of runs requiring zero manual edits (Straight-Through Processing)."},
                {"short": "Capacity", "name": "CAPACITY", "owner": "COO", "color": TEAL, "human_pct": 18, "value_pct": 72, "kpi_value": "3.8x", "kpi_label": "Volume handled per team", "question": "Can the same team absorb 3-4x demand without adding headcount?", "proof": "Verified completed outcomes / week per FTE before vs. after rollout."},
                {"short": "Cost", "name": "UNIT COST", "owner": "CFO / FINOPS", "color": AMBER, "human_pct": 9, "value_pct": 88, "kpi_value": "-68%", "kpi_label": "Cost per resolved outcome", "question": "Is (LLM + tool + human review cost) lower than the legacy baseline?", "proof": "All-in unit economics ledger: ($1.40 agent+gate vs. $4.40 manual)."},
                {"short": "P&L", "name": "P&L IMPACT", "owner": "CEO / BOARD", "color": GREEN, "human_pct": 4, "value_pct": 98, "kpi_value": "+$4.2M", "kpi_label": "Net annualized EBITDA / revenue", "question": "Where does the freed capacity show up on the income statement?", "proof": "Audited P&L line item: margin expansion, SLA retention, or new revenue."},
            ],
            "rule": "Rule: Speed without reducing Human Load hits the Pilot Ceiling. You only reach Capacity, Cost, and P&L when humans move from the work to the gates.",
        },
        "T46": {
            "title": "C-Suite AI Governance Cloverleaf: How CEO, CTO, CIO, and CISO Divide and Share the Operating Model",
            "subtitle": "Enterprise AI stalls when four executives either duplicate the same review or assume someone else owns the kill switch.",
            "source": "Alok Sharan, 'Information Governance vs AI Governance' (#14) • Matthew Coombs, 'Key Roles in Enterprise AI' (#08)",
            "lineage": "Alok Sharan (#14, 63 likes) & Matthew Coombs (#08, 51 likes)",
            "charters": [
                {
                    "pair": "01 • CEO ∩ CTO CHARTER",
                    "title": "Strategic Architecture & Build-vs-Buy Moat",
                    "color": BLUE,
                    "bullets": [
                        "Decide which workflows are core IP (custom harness + domain evals) vs. commodity SaaS.",
                        "Set model-routing budget guardrails tied directly to unit margin targets.",
                        "Review quarterly capability frontier shifts before committing multi-year contracts.",
                    ],
                    "artifact": "Artifact: AI Portfolio & Moat Matrix",
                },
                {
                    "pair": "02 • CEO ∩ CIO CHARTER",
                    "title": "Enterprise Workflow Adoption & Value Realization",
                    "color": TEAL,
                    "bullets": [
                        "Prioritize deployments by Straight-Through Processing (STP) impact, not demo flashiness.",
                        "Redesign human operating procedures so freed hours convert into measurable capacity.",
                        "sunset redundant point-solution AI tools across business units.",
                    ],
                    "artifact": "Artifact: 6-Stage Value Funnel Ledger",
                },
                {
                    "pair": "03 • CTO ∩ CISO CHARTER",
                    "title": "Secure Agent Harness Engineering (AgentSecOps)",
                    "color": PURPLE,
                    "bullets": [
                        "Enforce ingress prompt-injection scanning (Model Armor / Llama Guard) + taint tracking.",
                        "Physically unmount write tools via OPA policy when untrusted content enters context.",
                        "Mandate RFC 8693 On-Behalf-Of user+agent tokens and gVisor sandbox execution.",
                    ],
                    "artifact": "Artifact: Harness Security Gate Suite",
                },
                {
                    "pair": "04 • CIO ∩ CISO CHARTER",
                    "title": "Information Governance, DLP & Regulatory Compliance",
                    "color": RED,
                    "bullets": [
                        "Classify enterprise data tiers; block PII/PHI from unapproved external endpoints.",
                        "Maintain immutable 10-field agent action audit logs for EU AI Act / ISO 42001 / SOC 2.",
                        "Enforce data residency, CMEK encryption, and VPC Service Controls across clouds.",
                    ],
                    "artifact": "Artifact: Data Lineage & Compliance Dossier",
                },
                {
                    "pair": "05 • CTO ∩ CIO CHARTER",
                    "title": "Platform Integration, MCP Registry & FinOps",
                    "color": AMBER,
                    "bullets": [
                        "Operate a curated internal MCP server & SKILL.md registry over ERP/CRM systems.",
                        "Standardize telemetry (OpenTelemetry gen_ai spans) and per-tenant cost attribution.",
                        "Guarantee idempotent writes and durable checkpoints across enterprise databases.",
                    ],
                    "artifact": "Artifact: Enterprise MCP & Telemetry Catalog",
                },
                {
                    "pair": "06 • ALL 4 EXECUTIVES (CORE)",
                    "title": "Production Go/No-Go & Kill-Switch Charter",
                    "color": GREEN,
                    "bullets": [
                        "No agent ships without passing CTO evals, CIO data sign-off, and CISO red-team.",
                        "Every autonomous workflow has an assigned human owner, cost ceiling, and kill switch.",
                        "Monthly board review tracks the crossover from human touches to audited P&L impact.",
                    ],
                    "artifact": "Artifact: Production Agent Launch Receipt",
                },
            ],
            "rule": "Rule: Information governance (CIO/CISO) secures what data goes in; AI harness governance (CTO/CISO/CEO) controls what actions come out.",
        },
        "T47": {
            "title": "Global AI Regulatory & Standards Matrix: 20 Policies Every AI Architect Needs on One Page",
            "subtitle": "Don't build 20 separate compliance forks. Map global laws across 4 regions to the concrete engineering controls that satisfy all of them.",
            "source": "Prashant Rathi, 'Global AI Policies Explained' (#09, 203 likes, 68 comments) • EU AI Act • NIST AI RMF • ISO/IEC 42001",
            "lineage": "Prashant Rathi (#09, 203 likes, 68 comments) • Global AI Policy Matrix",
            "rows": [
                {
                    "region": "EUROPE & TREATIES",
                    "sub": "Risk-tiered statutory regimes & binding human-rights treaties",
                    "count_tag": "CARDS 01-05",
                    "color": BLUE,
                    "fill": "#EFF6FF",
                    "cards": [
                        {"name": "EU AI Act", "jurisdiction": "EU 2024/1689", "scope": "Prohibited, High-Risk & GPAI models", "control": "Risk tiering, technical dossier, human oversight gate, and conformity assessment.", "status": "Phased 2025-2027", "gate": " up to 7% global turnover"},
                        {"name": "GDPR Art. 22 & AI", "jurisdiction": "EU / EEA", "scope": "Automated decisions on individuals", "control": "Right to human intervention, explanation of logic, and DPIA before launch.", "status": "Enforced", "gate": "up to 4% global turnover"},
                        {"name": "CoE AI Convention", "jurisdiction": "Treaty (US/EU/UK)", "scope": "Public & private lifecycle rights", "control": "Documented risk impact assessments and contestability for affected persons.", "status": "Signed Sep 2024", "gate": "Binding signatory law"},
                        {"name": "OECD AI Principles", "jurisdiction": "47+ Nations", "scope": "Trustworthy & robust AI systems", "control": "Traceability of datasets, processes, and decisions across the AI lifecycle.", "status": "Updated May 2024", "gate": "Baseline for G7 / national laws"},
                        {"name": "UNESCO AI Ethics", "jurisdiction": "193 States", "scope": "Human rights & environmental impact", "control": "Ethical Impact Assessment (EIA) and gender/diversity bias audits.", "status": "Active global norm", "gate": "Procurement mandate"},
                    ],
                },
                {
                    "region": "GLOBAL STANDARDS",
                    "sub": "Certifiable engineering & security frameworks used in enterprise audits",
                    "count_tag": "CARDS 06-10",
                    "color": PURPLE,
                    "fill": "#F5F3FF",
                    "cards": [
                        {"name": "NIST AI RMF 1.0", "jurisdiction": "NIST AI 600-1", "scope": "Govern, Map, Measure, Manage", "control": "Continuous TEVV (Testing, Evaluation, Verification, Validation) + GenAI profile.", "status": "De facto US/Global", "gate": "Required in enterprise RFPs"},
                        {"name": "ISO/IEC 42001", "jurisdiction": "ISO Standard", "scope": "AI Management System (AIMS)", "control": "Auditable AI risk register, supplier controls, and incident postmortem loop.", "status": "Certifiable today", "gate": "Third-party ISO audit"},
                        {"name": "OWASP LLM Top 10", "jurisdiction": "OWASP 2025", "scope": "AppSec for LLMs & AI Agents", "control": "Prompt-injection taint guards, output encoding, and excessive-agency caps.", "status": "Industry baseline", "gate": "CI/CD red-team gate"},
                        {"name": "G7 Hiroshima Code", "jurisdiction": "G7 Leaders", "scope": "Frontier & foundation AI systems", "control": "Red-teaming before release, content provenance watermarks, vulnerability sharing.", "status": "Voluntary / Procurement", "gate": "Frontier model reporting"},
                        {"name": "SOC 2 + FDA 21CFR11", "jurisdiction": "Enterprise / GxP", "scope": "SaaS security & regulated life sciences", "control": "HMAC-SHA256 signed state tokens, immutable audit trails, RBAC isolation.", "status": "Enforced", "gate": "Blocks enterprise go-live"},
                    ],
                },
                {
                    "region": "UNITED STATES",
                    "sub": "Federal agency procurement rules & high-impact state statutes",
                    "count_tag": "CARDS 11-15",
                    "color": AMBER,
                    "fill": "#FFFBEB",
                    "cards": [
                        {"name": "US Federal AI Policy", "jurisdiction": "White House / EO", "scope": "Federal AI innovation & safety", "control": "National security evaluations, compute reporting, and federal AI testbeds.", "status": "Active Federal directive", "gate": "Federal contractor gate"},
                        {"name": "OMB Memo M-24-10", "jurisdiction": "US Agencies", "scope": "Safety-impacting & rights-impacting AI", "control": "Chief AI Officer sign-off, real-world testing, and opt-out fallback.", "status": "Enforced Dec 2024", "gate": "Agency authority to operate"},
                        {"name": "California AI Laws", "jurisdiction": "AB 2013 / SB 942", "scope": "Training data & AI provenance", "control": "Publish training-data lineage summaries and provide latent/manifest AI watermarks.", "status": "Enacted (2026 eff.)", "gate": "CA civil penalties"},
                        {"name": "Colorado AI Act", "jurisdiction": "CO SB 24-205", "scope": "High-risk consequential decisions", "control": "Annual algorithmic discrimination audit, consumer notice, and appeal path.", "status": "Enacted (2026 eff.)", "gate": "CO AG enforcement"},
                        {"name": "Texas & NYC LL 144", "jurisdiction": "TX TRAIGA / NYC", "scope": "State ethics & automated hiring tools", "control": "Independent bias audit published publicly before using AI in employment.", "status": "NYC enforced / TX active", "gate": "$500-$1,500/day per violation"},
                    ],
                },
                {
                    "region": "APAC & EMERGING",
                    "sub": "Mandatory algorithm registries, labeling laws, and national acts",
                    "count_tag": "CARDS 16-20",
                    "color": TEAL,
                    "fill": "#F0FDFA",
                    "cards": [
                        {"name": "China GenAI Rules", "jurisdiction": "CAC Measures", "scope": "Public-facing generative AI services", "control": "Algorithm registry filing, training-data legality audit, content moderation.", "status": "Enforced Aug 2023", "gate": "Mandatory CAC license"},
                        {"name": "China AI Labeling", "jurisdiction": "CAC / MIIT 2025", "scope": "All synthetic text, audio, image, video", "control": "Visible user disclosure label + immutable metadata watermark in file headers.", "status": "Enforced Sep 2025", "gate": "App store removal / fines"},
                        {"name": "South Korea AI Act", "jurisdiction": "KR Basic Act", "scope": "High-impact AI & generative watermarks", "control": "Prior user notification, safety impact documentation, and local representative.", "status": "Passed Dec 2024", "gate": "Effective Jan 2026"},
                        {"name": "Japan AI Promotion", "jurisdiction": "METI / AISI JP", "scope": "Innovation-first agile governance", "control": "Alignment with AISI safety evals; disclosure of severe incidents to ministry.", "status": "Enacted 2025", "gate": "Guidance + public naming"},
                        {"name": "India DPDP & Brazil", "jurisdiction": "IN / BR Bill 2338", "scope": "Personal data & risk-tiered AI rights", "control": "Explicit consent ledger, data localization options, and high-risk sandbox testing.", "status": "DPDP active / BR Senate", "gate": "Up to ₹250 Cr / R$50M"},
                    ],
                },
            ],
            "rule": "Rule: Architect once for the strictest superset — Risk Tiering (EU) + Continuous Evals (NIST/ISO 42001) + Provenance Labels (CA/China) + Bias Audits (CO/NYC).",
        },
        "T48": {
            "title": "The 8-Tier Production AI Maturity Pyramid — and the 10-Step Order to Build It Without Skipping Tiers",
            "subtitle": "Teams fail when they jump straight from Tier 1 (a notebook demo) to Tier 6 (multi-agent swarms) without building Tiers 2-5 first.",
            "source": "Prashant Rathi, 'Production AI Stack 8 Tiers' (#12) • Jonathan Parsons, 'Correct Order to Build AI Agents' (#10)",
            "lineage": "Prashant Rathi (#12, 53 likes) & Jonathan Parsons (#10, 71 likes)",
            "build_order": [
                {"head": "Map the human workflow first", "phase": "STEP 01", "sub": "Document inputs, edge cases, and failure cost before touching an LLM.", "color": "#475569"},
                {"head": "Extract deterministic code rules", "phase": "STEP 02", "sub": "If IF/THEN or regex solves 60% of cases, write Python — not a prompt.", "color": "#475569"},
                {"head": "Clean data contracts & schemas", "phase": "STEP 03", "sub": "Define strict Pydantic / JSON schemas for inputs and outputs.", "color": BLUE},
                {"head": "Build 50+ golden eval fixtures", "phase": "STEP 04", "sub": "You cannot improve what you cannot grade automatically in CI.", "color": BLUE},
                {"head": "Single LLM call + structured output", "phase": "STEP 05", "sub": "Benchmark one well-prompted call before adding chains or loops.", "color": PURPLE},
                {"head": "Grounded RAG + citation verification", "phase": "STEP 06", "sub": "Hybrid search + reranking + deterministic quote-span checks.", "color": PURPLE},
                {"head": "Multi-step deterministic workflow", "phase": "STEP 07", "sub": "Code owns the DAG; LLM handles bounded extraction/drafting nodes.", "color": TEAL},
                {"head": "Scoped read-only tool calls (MCP)", "phase": "STEP 08", "sub": "Mount Top-3 read tools dynamically; enforce loop & token ceilings.", "color": AMBER},
                {"head": "Guarded write tools + HITL gates", "phase": "STEP 09", "sub": "Idempotency keys, taint downgrade, and human sign-off on mutations.", "color": GREEN},
                {"head": "Multi-agent / self-evolving harness", "phase": "STEP 10", "sub": "Add subagents & Harness² recursion only when one window saturates.", "color": NAVY},
            ],
            "tiers": [
                {"level": "TIER 8", "name": "ELITE AUTONOMOUS OS", "controls": "Recursive skill evolution (Harness²) + automated canary rollback", "stack": "Harness² • OpenTelemetry • Canary Gate", "color": "#0F172A"},
                {"level": "TIER 7", "name": "SELF-CORRECTING MEMORY & CI", "controls": "Git blob SHA evidence receipts + 100% golden trajectory CI gate", "stack": "OpenWiki SHA • Promptfoo / Inspect AI", "color": "#1E3A8A"},
                {"level": "TIER 6", "name": "MULTI-AGENT & SANDBOX VERIFY", "controls": "Typed blackboard handoffs + gVisor sandbox exit_code == 0 hook", "stack": "A2A Protocol • OpenHands / E2B • Firestore", "color": PURPLE},
                {"level": "TIER 5", "name": "CORE PRODUCTION HARNESS", "controls": "Loop circuit breaker + hard cost ceiling + durable step checkpoints", "stack": "Google ADK / LangGraph • Temporal • LiteLLM", "color": GREEN},
                {"level": "TIER 4", "name": "SCOPED TOOL USE & SECURITY", "controls": "Top-3 dynamic MCP routing + prompt-injection taint capability downgrade", "stack": "MCP • AlloyDB pgvector / Qdrant • Model Armor / OPA", "color": TEAL},
                {"level": "TIER 3", "name": "GROUNDED RAG & CONTEXT HYGIENE", "controls": "Contextual hybrid retrieval + CRAG + 60% window compaction + URI pointers", "stack": "Vertex RAG / Qdrant • BM25 + Reranker • GCS / MinIO", "color": AMBER},
                {"level": "TIER 2", "name": "STRUCTURED PROMPTING & EVALS", "controls": "Pydantic schema enforcement + trace error taxonomy + binary judges", "stack": "Pydantic • Vertex Eval / DeepEval • Langfuse", "color": BLUE},
                {"level": "TIER 1", "name": "PROTOTYPE / NOTEBOOK DEMO", "controls": "Single raw prompt, static tool dump, happy-path screenshot, zero guards", "stack": "Raw SDK call • 0 evals • Not production-safe", "color": "#64748B"},
            ],
            "skip_failures": [
                {"skip": "SKIP TIER 2 (Evals & Schemas)", "symptom": "Silent prompt regressions on every edit", "why": "Without a 50-trace golden eval suite and Pydantic contracts, fixing bug A quietly breaks workflows B and C.", "fix": "Build Step 03-04 before adding tools", "color": RED},
                {"skip": "SKIP TIER 3 (Context & RAG Hygiene)", "symptom": "Context rot & 67% missed retrieval", "why": "Dumping 85 tools and raw PDFs into a 200K window dilutes attention and serves unverified chunks.", "fix": "Add Contextual Hybrid RAG + 60% compaction", "color": AMBER},
                {"skip": "SKIP TIER 4-5 (Security & Harness)", "symptom": "$400 retry storms & data exfiltration", "why": "Giving an unguarded loop write tools lets one flaky API or poisoned document trigger runaway damage.", "fix": "Enforce loop guard, OPA taint, & idempotency", "color": RED},
                {"skip": "SKIP TIER 6-7 (Sandbox & SHA Memory)", "symptom": "38% broken 'done' claims & memory rot", "why": "Agents declare victory without running tests and quote stale architectural facts weeks after code changes.", "fix": "Require exit_code==0 & SHA memory receipts", "color": AMBER},
            ],
            "rule": "Rule: Earn each tier from the bottom up — never deploy Tier 6 multi-agent autonomy on top of a Tier 1 unverified harness.",
        },
        "T49": {
            "title": "Traditional Automation vs. AI Workflows vs. Autonomous Agents: The 3-Column Decision Triptych",
            "subtitle": "Don't use an autonomous agent for a deterministic cron job, and don't force an IF/THEN script to parse messy unstructured edge cases.",
            "source": "Prem Natarajan, 'Automation vs AI Workflows vs AI Agents' (#13, 59 likes, 53 comments) • Anthropic 'Building Effective Agents' • Chip Huyen",
            "lineage": "Prem Natarajan (#13, 59 likes, 53 comments) & Chip Huyen",
            "columns": [
                {
                    "title": "TRADITIONAL AUTOMATION",
                    "tagline": "Deterministic code & fixed rules (Zero LLM)",
                    "color": "#334155",
                    "nodes": [
                        {"head": "Trigger", "sub": "Webhook / Cron"},
                        {"head": "IF / THEN", "sub": "Exact code rules"},
                        {"head": "Action", "sub": "100% predictable"},
                    ],
                    "owner": "100% Application Code — every branch, retry, and field mapping is explicitly programmed.",
                    "best_for": "Schema validation, billing calculations, idempotency ledgers, database ETL, and compliance gates.",
                    "cost": "< 10 ms latency • ~$0.00001 / run • 100% reproducible",
                    "failure": "Brittle on unstructured inputs: fails immediately if a vendor changes a PDF layout or column name.",
                    "verify": "Standard unit & integration tests (pytest / CI) with 100% deterministic coverage.",
                    "stack": "Cloud Workflows / Cloud Run ⇄ Temporal / Python / Airflow",
                    "verdict": "USE FIRST whenever the rules and inputs are structured",
                },
                {
                    "title": "AI WORKFLOWS (DAG)",
                    "tagline": "Code-orchestrated steps with bounded LLM nodes",
                    "color": BLUE,
                    "nodes": [
                        {"head": "Ingest", "sub": "Messy doc / ticket"},
                        {"head": "LLM Node", "sub": "Extract / classify"},
                        {"head": "Code Gate", "sub": "Validate & route"},
                    ],
                    "owner": "Code owns the control flow (the DAG); the LLM is called inside specific nodes to parse, classify, or draft.",
                    "best_for": "80% of enterprise AI: invoice extraction, support triage, grounded RAG Q&A, PR summarization.",
                    "cost": "1 – 4 sec latency • $0.002 – $0.02 / run • Bounded token budget",
                    "failure": "Node-level extraction errors — easily caught by Pydantic validation and a single evaluator-optimizer retry.",
                    "verify": "Per-node golden dataset evals (Promptfoo / Vertex Eval) + deterministic schema assertions.",
                    "stack": "Vertex AI Pipelines / ADK Workflow ⇄ LangGraph DAG / Instructor",
                    "verdict": "DEFAULT CHOICE when steps are known but data is messy",
                },
                {
                    "title": "AUTONOMOUS AI AGENTS",
                    "tagline": "Model-directed planning & tool use inside a harness",
                    "color": GREEN,
                    "nodes": [
                        {"head": "Open Goal", "sub": "Fix bug / research"},
                        {"head": "Act-Verify", "sub": "Dynamic tool loop"},
                        {"head": "Receipt", "sub": "exit_code == 0"},
                    ],
                    "owner": "The LLM dynamically decides which tools to call and how many steps to take, bounded by a deterministic harness.",
                    "best_for": "Open-ended coding (SWE-bench), multi-source deep research, root-cause debugging across unknown files.",
                    "cost": "10 – 120 sec latency • $0.05 – $0.80 / run • Requires hard budget ceiling",
                    "failure": "Compounding multi-step drift, retry storms, or tool misuse unless gated by loop guards and sandboxes.",
                    "verify": "Trajectory precision/recall + sandboxed pre-completion test (exit_code == 0) + human gate on writes.",
                    "stack": "Google ADK + Cloud Run gVisor ⇄ OpenHands / LangGraph + Temporal",
                    "verdict": "EARN THIS ONLY when the step sequence cannot be predicted",
                },
            ],
            "decision_bar": "Start at Column 01 (Code). Move to Column 02 (AI Workflow) when inputs are unstructured. Move to Column 03 (Agent) only when the path itself cannot be scripted — and wrap Column 03 in Column 01 gates.",
            "rule": "Rule: The best production AI systems are hybrids — an Autonomous Agent (Col 3) running inside an AI Workflow (Col 2) guarded by Traditional Automation (Col 1).",
        },
        "T50": {
            "title": "OAuth 2.0 + PKCE vs. OpenID Connect (OIDC) + RFC 8693 Agent Delegation: The Protocol Sequence Diff",
            "subtitle": "OAuth 2.0 grants delegated API permission; OIDC proves user identity; RFC 8693 'act' claims bind an AI agent to the human it acts for.",
            "source": "Alex Xu / ByteByteGo, 'OAuth 2.0 vs OIDC' (#07) • Shalini Goyal (#06) • RFC 6749 / RFC 7636 (PKCE) / OIDC Core / RFC 8693 Token Exchange",
            "lineage": "Alex Xu / ByteByteGo (#07) & Shalini Goyal (#06) • RFC 8693 Agent Identity",
            "panels": [
                {
                    "title": "PANEL A • OAUTH 2.0 AUTHORIZATION CODE + PKCE (DELEGATED PERMISSION — NOT IDENTITY)",
                    "color": BLUE,
                    "fill": "#EFF6FF",
                    "actors": [
                        {"name": "USER / BROWSER", "sub": "Resource Owner"},
                        {"name": "CLIENT / AGENT APP", "sub": "Generates PKCE verifier"},
                        {"name": "AUTH SERVER", "sub": "OAuth 2.0 /authorize & /token"},
                        {"name": "RESOURCE / MCP API", "sub": "Checks scopes (scp)"},
                    ],
                    "messages": [
                        {"from": 0, "to": 1, "text": "Click 'Connect GitHub' (app generates code_verifier)", "color": "#334155"},
                        {"from": 1, "to": 2, "text": "GET /authorize?code_challenge=SHA256(verifier)&scope=repo:read", "color": BLUE},
                        {"from": 2, "to": 0, "text": "Prompt user login & scope consent screen", "color": PURPLE},
                        {"from": 2, "to": 1, "text": "Redirect callback with short-lived authorization_code", "color": PURPLE},
                        {"from": 1, "to": 2, "text": "POST /token (authorization_code + plaintext code_verifier)", "color": BLUE},
                        {"from": 2, "to": 1, "text": "Verify SHA256(verifier) -> issue scoped access_token", "color": GREEN},
                        {"from": 1, "to": 3, "text": "Call MCP / API with Authorization: Bearer <access_token>", "color": TEAL},
                    ],
                    "card_title": "OAUTH 2.0 + PKCE TAKEAWAYS",
                    "bullets": [
                        "Answers 'What is this app allowed to access?' — never use an opaque access_token as proof of who logged in.",
                        "PKCE (RFC 7636) binds the authorization code to the exact client that started the flow via code_verifier.",
                        "Scope ceiling: the access_token only carries the consented scopes (e.g., repo:read, never admin:org).",
                    ],
                    "token_head": "OAuth 2.0 Access Token (API Authorization)",
                    "token_lines": [
                        "{",
                        "  \"iss\": \"https://auth.example.com\",",
                        "  \"aud\": \"https://mcp.github.internal\",",
                        "  \"scp\": [\"repo:read\", \"pull_request:read\"],",
                        "  \"code_verifier_checked\": true",
                        "}",
                    ],
                },
                {
                    "title": "PANEL B • OPENID CONNECT (OIDC) + RFC 8693 ON-BEHALF-OF (OBO) AGENT DELEGATION",
                    "color": GREEN,
                    "fill": "#ECFDF5",
                    "actors": [
                        {"name": "HUMAN USER", "sub": "Authenticated Principal"},
                        {"name": "ORCHESTRATOR AGENT", "sub": "Holds user id_token"},
                        {"name": "OIDC IdP & RFC 8693 STS", "sub": "Identity + Token Exchange"},
                        {"name": "DOWNSTREAM MCP TOOL", "sub": "Enforces sub + act OPA"},
                    ],
                    "messages": [
                        {"from": 0, "to": 1, "text": "Sign in with OIDC (scope=openid profile email)", "color": "#334155"},
                        {"from": 2, "to": 1, "text": "Issue signed id_token (JWT proving user identity) + access_token", "color": BLUE},
                        {"from": 1, "to": 1, "text": "Verify id_token signature, iss, aud, exp (sub = 'alice@corp')", "color": PURPLE},
                        {"from": 1, "to": 2, "text": "POST /token (RFC 8693 exchange: subject=alice, actor=triage_agent)", "color": AMBER},
                        {"from": 2, "to": 1, "text": "Mint narrowed OBO JWT with both sub='alice' and act={'sub':'agent'}", "color": GREEN},
                        {"from": 1, "to": 3, "text": "tools/call with Bearer <OBO_JWT> (5-min TTL, single-task scope)", "color": TEAL},
                        {"from": 3, "to": 1, "text": "OPA verifies BOTH alice's RBAC and agent's allowlist -> execute & log", "color": GREEN},
                    ],
                    "card_title": "OIDC + RFC 8693 AGENT IDENTITY TAKEAWAYS",
                    "bullets": [
                        "OIDC adds the signed id_token so the app knows *who* the human user is (sub, email, groups).",
                        "Never give an agent a god-mode service account! Exchange the user token via RFC 8693 for a narrowed OBO token.",
                        "Downstream tools authorize the intersection of (Human User RBAC ∩ Agent Capability Policy) and log both IDs.",
                    ],
                    "token_head": "OIDC + RFC 8693 Agent OBO JWT (Dual Identity)",
                    "token_lines": [
                        "{",
                        "  \"sub\": \"user:alice@corp.com\",",
                        "  \"act\": { \"sub\": \"agent:pr-reviewer-v2\" },",
                        "  \"scp\": [\"jira:comment:create\"],",
                        "  \"exp\": 1761003000  // 300s ephemeral TTL",
                        "}",
                    ],
                },
            ],
            "rule": "Rule: OAuth 2.0 authorizes APIs; OIDC authenticates humans; RFC 8693 'act' tokens ensure an AI agent never exceeds the human's permissions.",
        },
        "T51": {
            "title": "Why LLM Decoding Is Memory-Bound — and How Speculative Decoding Verifies 5 Tokens in 1 HBM Read",
            "subtitle": "During decode, an H100 spends >95% of its time moving 70 GB of weights from HBM3e to SRAM for a single token. Draft-and-verify fixes the arithmetic intensity.",
            "source": "Sahn Lam & Umar Jamil • Leviathan et al. (Speculative Decoding) • Medusa (Cai et al.) • EAGLE-2 (Li et al.) • FlashAttention-3",
            "lineage": "Sahn Lam & Umar Jamil • EAGLE-2 / Medusa / FlashAttention-3",
            "roofline_lines": [
                "Model: Llama-3.3-70B in FP8 (70 GB weights in HBM3e)",
                "H100 SXM5 Peak FP8 Compute: 1,979 TFLOPS",
                "H100 SXM5 HBM3e Bandwidth:  3.35 TB/s",
                "Ridge Point (Compute / BW): ~590 FLOPs / Byte",
                "----------------------------------------------------",
                "Standard Decode (Batch=1, generating 1 token):",
                "  Must stream all 70 GB weights from HBM -> SRAM",
                "  Min HBM transfer time = 70 GB / 3.35 TB/s = 20.9 ms",
                "  Arithmetic Intensity  = ~2 FLOPs / Byte (! 98% Tensor Cores IDLE !)",
                "FIX: Verify K=5 draft tokens in 1 weight read -> 5x arithmetic intensity!",
            ],
            "lossless_note": "Target 70B computes logits for all K=5 draft positions in parallel. Using rejection sampling p_accept = min(1, p_target(x) / p_draft(x)), any rejected token is resampled directly from the residual distribution — guaranteeing 100% identical output quality to greedy or temperature sampling.",
            "spec_archs": [
                {"name": "TWO-MODEL DRAFT (70B + 1B)", "how": "Pair a small 1B-3B model from the same tokenizer family to draft K=5 tokens; 70B verifies.", "speedup": "1.9x - 2.3x speedup", "color": BLUE},
                {"name": "MEDUSA (PARALLEL HEADS)", "how": "Attach K lightweight FFN heads onto the 70B model's last hidden state — no separate draft model.", "speedup": "2.2x - 2.5x speedup", "color": PURPLE},
                {"name": "EAGLE-2 (DYNAMIC DRAFT TREE)", "how": "Autoregressive feature-level draft head builds a confidence-pruned token tree per step.", "speedup": "2.5x - 2.8x speedup", "color": GREEN},
            ],
            "rule": "Rule: Prefill is compute-bound (optimize FLOPs with FlashAttention-3); Decode is HBM-bandwidth-bound (optimize tokens-per-weight-read with Speculative Decoding).",
        },
        "T52": {
            "title": "How Reasoning Models Are Built: Cold-Start SFT -> GRPO -> Verifiable Rewards (RLVR) -> Test-Time Compute",
            "subtitle": "Sebastian Raschka & DeepSeek-R1 post-training breakdown: why dropping the PPO critic model and training against deterministic compilers unlocked reasoning.",
            "source": "Sebastian Raschka, 'Understanding Reasoning LLMs' • DeepSeek-R1 (arXiv:2501.12948) • Maxime Labonne •Lambert et al. (TÜLU 3 RLVR)",
            "lineage": "Sebastian Raschka & Maxime Labonne • DeepSeek-R1 GRPO & RLVR",
            "stages": [
                {
                    "name": "COLD-START SFT",
                    "goal": "Instill readable <think> structure",
                    "color": BLUE,
                    "how": "Fine-tune the base pre-trained model on a small, high-quality set of curated Chain-of-Thought traces so RL starts from coherent formatting.",
                    "box_head": "Cold-Start Format Template",
                    "box_lines": [
                        "<think>",
                        "  1. Decompose constraints...",
                        "  2. Check edge case x=0...",
                        "</think>",
                        "<answer>Final verified solution</answer>",
                    ],
                    "scale": "5K – 50K curated traces",
                    "takeaway": "Prevents language-mixing and unreadable gibberish that pure RL-from-base (R1-Zero) suffers from.",
                    "stack": "TRL SFTTrainer • Axolotl • LoRA / QLoRA",
                },
                {
                    "name": "GRPO OPTIMIZATION",
                    "goal": "Eliminate the 70B Value Critic model",
                    "color": PURPLE,
                    "how": "Sample a group of G=8 outputs per prompt from the current policy; compute baseline advantage from the group's own mean and std reward.",
                    "box_head": "Group Relative Advantage (GRPO)",
                    "box_lines": [
                        "Prompt q -> sample {o_1, ..., o_G}",
                        "Score each: {r_1, ..., r_G}",
                        "mean_r = mean(r), std_r = std(r)",
                        "Advantage A_i = (r_i - mean_r) / std_r",
                        "Update policy with KL penalty to ref",
                    ],
                    "scale": "~50% less RL GPU memory vs. PPO",
                    "takeaway": "No separate Value/Critic network to train or hold in HBM — the group of G completions acts as its own baseline.",
                    "stack": "DeepSeek GRPO • HuggingFace TRL • VeRL",
                },
                {
                    "name": "RLVR (VERIFIABLE REWARDS)",
                    "goal": "Replace hackable neural reward models",
                    "color": GREEN,
                    "how": "Grade each sampled completion with a deterministic ground-truth verifier (unit test suite, compiler, SQL engine, or exact math solver).",
                    "box_head": "Deterministic Reward Function",
                    "box_lines": [
                        "def verify_reward(completion, test_suite):",
                        "    fmt_ok = has_think_and_answer(completion)",
                        "    code   = extract_code(completion)",
                        "    passed = sandbox.run_pytest(code) == 0",
                        "    return (1.0 if passed else 0.0) + 0.1*fmt_ok",
                    ],
                    "scale": "Zero reward-model hacking",
                    "takeaway": "Neural reward models get gamed by verbose phrasing; a compiler or pytest exit_code == 0 cannot be sweet-talked.",
                    "stack": "OpenHands / E2B Sandbox • SymPy • pytest",
                },
                {
                    "name": "TEST-TIME COMPUTE",
                    "goal": "Trade inference tokens for accuracy",
                    "color": AMBER,
                    "how": "At deployment, scale reasoning budget dynamically per query complexity and verify parallel candidates before returning the final answer.",
                    "box_head": "Inference Scaling Levers",
                    "box_lines": [
                        "1. Dynamic thinking budget (LOW/HIGH)",
                        "2. Parallel Best-of-N sampling (N=4..16)",
                        "3. Sandbox verifier filters N -> valid",
                        "4. Majority vote / Process Reward Judge",
                        "Result: 27B + verifier beats 405B zero-shot",
                    ],
                    "scale": "1K – 32K thinking tokens on hard tasks",
                    "takeaway": "Spend extra test-time compute only when router complexity > 0.75 or when a deterministic check fails on Turn 1.",
                    "stack": "Vertex thinkingLevel='HIGH' • vLLM Best-of-N",
                },
            ],
            "ppo_vs_grpo_note": "PPO requires training a Value Critic model as large as the Policy model just to estimate baseline variance. GRPO replaces that entire 70B network with a 5-line z-score across G=8 sampled completions.",
            "playbook": [
                {"level": "LEVEL 1 • PROMPT + DETERMINISTIC HARNESS (90% OF ENTERPRISE TEAMS)", "cost": "$0 training • Ship in days", "when": "Start here: wrap a frontier or reasoning model (Gemini 3.8 / Claude / DeepSeek-R1) in a loop guard, Contextual RAG, and a sandboxed pre-completion verifier.", "color": BLUE},
                {"level": "LEVEL 2 • COLD-START LoRA SFT / DISTILLATION (LATENCY & COST COMPRESSION)", "cost": "$200 – $2K GPU • 5K traces", "when": "Use when your Level 1 harness works, and you want to distill verified trajectories from a large model into a fast 7B-14B model for 10x cheaper serving.", "color": PURPLE},
                {"level": "LEVEL 3 • GRPO + RLVR ON DOMAIN VERIFIERS (PROPRIETARY REASONING MOAT)", "cost": "$5K – $25K GPU • Verifier required", "when": "Use when you have a deterministic domain verifier (SQL query execution, Terraform validate, formal policy prover, chip layout DRC) and want superhuman domain accuracy.", "color": GREEN},
            ],
            "rule": "Rule: If you can write a deterministic verifier (exit_code == 0), you can use it today as a runtime harness gate — and tomorrow as an RLVR training reward.",
        },
    }


register_templates(META, RENDERERS_V3, demo_specs_v3)
