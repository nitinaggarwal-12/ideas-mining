"""Template Gallery v2 — 20 more unique dynamic templates (T21-T40).

Each template reproduces the *signature format* of a top-followed Agentic AI / GenAI / LLM / Evaluation / Claude creator or
primary source, and delivers one concrete artifact a reader can use today: a pattern picker, a copy-paste prompt, a token
budget, a worked calculation, runnable code, a scorecard, a security test, a cost waterfall, an incident timeline.

Lineage (format inspiration + primary source) is printed on every template so attribution stays explicit:
  T21 Anthropic "Building effective agents" (Schluntz & Zhang, Dec 2024)     T31 Shubham Saboo / Nir Diamant demo-repo format
  T22 Anthropic "Claude Code: best practices for agentic coding" (Apr 2025)  T32 Andrew Ng, Sequoia AI Ascent (Mar 2024)
  T23 Anthropic "Effective context engineering for AI agents" (Sep 2025)     T33 Ethan Mollick, "jagged frontier" (Dell'Acqua et al. 2023)
  T24 Hamel Husain & Shreya Shankar, AI Evals error-analysis method          T34 Simon Willison, "The lethal trifecta" (Jun 2025)
  T25 Eugene Yan / Shreya Shankar / MT-Bench (Zheng et al. 2023)             T35 Anthropic "How we built our multi-agent research system" (Jun 2025)
  T26 Google "Agents Companion" whitepaper (Feb 2025)                        T36 Chip Huyen-style practical AI economics
  T27 Alex Xu / ByteByteGo "how it works" + MCP specification                T37 Google SRE postmortem format applied to AgentOps
  T28 Avi Chawla & Akshay Pachaar sketch explainers + Anthropic Contextual Retrieval (Sep 2024)   T38 Anthropic "Writing effective tools for agents" (Sep 2025)
  T29 Tom Yeh "AI by Hand" worked examples                                   T39 CoALA (Sumers et al. 2023) + Lilian Weng (2023) + Aishwarya Reganti memory infographics
  T30 Pascal Biese (LLM Watch) & Elvis Saravia (DAIR.AI) paper digests       T40 Nate B. Jones "one chart" / Santiago Valdarrama build-in-public
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.visuals.template_gallery import (
    AMBER, BG, BLUE, GREEN, INK, LINE, MUTED, NAVY, PURPLE, RED, SKY, SLATE, TEAL, WHITE,
    _arc_pts, _card_head, _diamond, _esc, _flow, _frame, _grow, _pill, _qbez_pts, _r, _t, _tl, _wrap, register_templates,
)

HAND = "'Chalkboard SE', 'Marker Felt', 'Comic Sans MS', cursive"
Point = Tuple[float, float]


def _ht(x: float, y: float, s: Any, size: float = 13, weight: int = 700, fill: str = INK, anchor: str = "start", extra: str = "") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{HAND}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{_esc(s)}</text>')


def _htl(x: float, y: float, lines: Sequence[str], size: float = 13, weight: int = 700, fill: str = INK, lh: float = 18, anchor: str = "start") -> str:
    return "\n".join(_ht(x, y + i * lh, ln, size, weight, fill, anchor) for i, ln in enumerate(lines))


def _reveal(phase: Optional[float], n: int) -> int:
    return n if (phase is None or phase >= 0.8) else max(1, min(n, int(phase * (n + 1)) + 1))


def _mb(x: float, y: float, w: float, h: float, label: str, col: str, fill: str = WHITE, size: float = 9.5) -> str:
    lines = _wrap(label, max(6, int(w / 6.2)), 2)
    ty = y + h / 2 + (4 if len(lines) == 1 else -2)
    return _r(x, y, w, h, 6, fill, col, 1.6) + _tl(x + w / 2, ty, lines, size, 800, INK if fill == WHITE else WHITE, 11, "middle")


def _fl(pts: Sequence[Point], col: str, phase: Optional[float], dur: float = 1.6, label: Optional[str] = None, dash: str = "7 5") -> str:
    return _flow(pts, col, phase, label, dur, 2.4, True, 1, dash=dash, track=False, label_dy=-14)


def _num(cx: float, cy: float, n: Any, col: str, r: float = 13) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{col}"/>' + _t(cx, cy + 4, str(n), 10.5, 800, WHITE, "middle")


# ----------------------------------------------------------------------------------------------------------------------
# T21 — Pattern Picker: Anthropic's 5 workflows + the agent loop, each with use/avoid/example
# ----------------------------------------------------------------------------------------------------------------------
def _schematic(kind: str, x: float, y: float, w: float, h: float, col: str, phase: Optional[float]) -> List[str]:
    o: List[str] = []
    cy = y + h / 2
    if kind == "chain":
        o.append(_mb(x, cy - 15, 46, 30, "In", SLATE))
        o.append(_fl([(x + 46, cy), (x + 70, cy)], col, phase))
        o.append(_mb(x + 72, cy - 15, 74, 30, "LLM call 1", col))
        o.append(_fl([(x + 146, cy), (x + 168, cy)], col, phase))
        o.append(_diamond(x + 196, cy, 26, 22, ["gate"], AMBER, 9))
        o.append(_fl([(x + 222, cy), (x + 246, cy)], col, phase))
        o.append(_mb(x + 248, cy - 15, 74, 30, "LLM call 2", col))
        o.append(_fl([(x + 322, cy), (x + 346, cy)], col, phase))
        o.append(_mb(x + 348, cy - 15, 74, 30, "LLM call 3", col))
        o.append(_fl([(x + 422, cy), (x + 444, cy)], GREEN, phase))
        o.append(_t(x + 196, cy + 44, "gate = programmatic check between steps (e.g. 'is the outline on-brief?')", 9, 700, SLATE, "middle"))
    elif kind == "route":
        o.append(_mb(x, cy - 15, 42, 30, "In", SLATE))
        o.append(_fl([(x + 42, cy), (x + 76, cy)], col, phase))
        o.append(_mb(x + 78, cy - 17, 92, 34, "Router (LLM or classifier)", col))
        for j, lbl in enumerate(["Cheap model: FAQ", "Strong model: hard", "Refund specialist"]):
            yy = y + 8 + j * 39
            o.append(_fl([(x + 170, cy), (x + 202, yy + 14), (x + 234, yy + 14)], col, phase))
            o.append(_mb(x + 236, yy, 126, 28, lbl, col))
            o.append(_fl([(x + 362, yy + 14), (x + 388, cy), (x + 402, cy)], GREEN, phase))
        o.append(_mb(x + 404, cy - 15, 40, 30, "Out", GREEN))
    elif kind == "parallel":
        o.append(_mb(x, cy - 15, 46, 30, "In", SLATE))
        for j, lbl in enumerate(["LLM: section A", "LLM: section B", "LLM: vote / guardrail"]):
            yy = y + 8 + j * 39
            o.append(_fl([(x + 46, cy), (x + 80, yy + 14), (x + 118, yy + 14)], col, phase))
            o.append(_mb(x + 120, yy, 130, 28, lbl, col))
            o.append(_fl([(x + 250, yy + 14), (x + 290, cy), (x + 316, cy)], col, phase))
        o.append(_mb(x + 318, cy - 15, 92, 30, "Aggregate", col))
        o.append(_fl([(x + 410, cy), (x + 444, cy)], GREEN, phase))
    elif kind == "orchestrator":
        o.append(_mb(x, cy - 22, 112, 34, "Orchestrator LLM decides subtasks", col))
        for j, lbl in enumerate(["Worker: file A", "Worker: file B", "Worker: tests"]):
            yy = y + 2 + j * 35
            o.append(_fl([(x + 112, cy - 5), (x + 150, yy + 13), (x + 178, yy + 13)], col, phase, dash="3 4"))
            o.append(_mb(x + 180, yy, 120, 26, lbl, col))
            o.append(_fl([(x + 300, yy + 13), (x + 332, cy - 5), (x + 352, cy - 5)], col, phase))
        o.append(_mb(x + 354, cy - 20, 60, 30, "Merge", col))
        o.append(_fl([(x + 414, cy - 5), (x + 444, cy - 5)], GREEN, phase))
        o.append(_t(x + 224, y + h - 1, "dashed = subtasks are decided at run time, not hard-coded", 8.8, 700, SLATE, "middle"))
    elif kind == "evaluator":
        o.append(_mb(x + 40, cy - 17, 120, 34, "Generator LLM", col))
        o.append(_fl([(x + 160, cy - 8), (x + 300, cy - 8)], col, phase, label="draft"))
        o.append(_mb(x + 300, cy - 17, 120, 34, "Evaluator LLM", AMBER))
        o.append(_fl([(x + 300, cy + 10), (x + 160, cy + 10)], AMBER, phase, label="feedback", dash="4 4"))
        o.append(_fl([(x + 360, cy + 17), (x + 360, cy + 48), (x + 444, cy + 48)], GREEN, phase, label="accepted"))
        o.append(_t(x + 230, y + 10, "loop until the evaluator says 'meets the bar' (or max rounds)", 8.8, 700, SLATE, "middle"))
    else:  # agent
        o.append(_mb(x, cy - 15, 50, 30, "Human", SLATE))
        o.append(_fl([(x + 50, cy), (x + 84, cy)], col, phase, label="task"))
        o.append(_mb(x + 86, cy - 17, 102, 34, "LLM plans next step", col))
        o.append(_fl([(x + 188, cy - 8), (x + 272, cy - 8)], col, phase, label="action"))
        o.append(_mb(x + 274, cy - 17, 104, 34, "Environment / tools", TEAL))
        o.append(_fl([(x + 274, cy + 10), (x + 188, cy + 10)], TEAL, phase, label="result", dash="4 4"))
        o.append(_fl([(x + 378, cy), (x + 394, cy)], GREEN, phase))
        o.append(_diamond(x + 416, cy, 22, 20, ["done?"], GREEN, 8.5))
        o.append(_t(x + 220, y + 10, "stop on: task complete, max steps, or a human checkpoint", 8.8, 700, SLATE, "middle"))
    return o


def render_t21(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    for i, p in enumerate(s["patterns"][:6]):
        x, y = 56 + (i % 3) * 500, 136 + (i // 3) * 372
        w, h = 488, 356
        b.append(_r(x, y, w, h, 12, WHITE, p["color"], 2))
        b.append(_r(x, y, w, 30, 10, p["color"]))
        b.append(_t(x + 14, y + 20, f"{i + 1}. {p['name'].upper()}  •  {p['tag']}", 11, 800, WHITE))
        b.append(_r(x + 10, y + 38, w - 20, 146, 8, "#F8FAFC", "#E2E8F0", 1))
        b += _schematic(p["kind"], x + 24, y + 48, w - 48, 128, p["color"], phase)
        b.append(_t(x + 14, y + 204, "USE WHEN", 9.5, 800, GREEN))
        b.append(_tl(x + 14, y + 220, _wrap(p["use"], 66, 2), 11, 600, "#1E293B", 15))
        b.append(_t(x + 14, y + 256, "AVOID WHEN", 9.5, 800, RED))
        b.append(_tl(x + 14, y + 272, _wrap(p["avoid"], 66, 2), 11, 600, "#1E293B", 15))
        b.append(_t(x + 14, y + 308, "REAL EXAMPLE", 9.5, 800, BLUE))
        b.append(_tl(x + 14, y + 324, _wrap(p["example"], 66, 2), 11, 700, INK, 15))
    b.append(_r(56, 890, 1508, 42, 10, NAVY))
    b.append(_t(810, 916, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T21", META["T21"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T22 — Claude Code playbook: Explore -> Plan -> Code -> Commit with copy-paste prompts
# ----------------------------------------------------------------------------------------------------------------------
def render_t22(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    for i, ph in enumerate(s["phases"][:4]):
        x, y = 56 + i * 380, 136
        b.append(_card_head(x, y, 364, 246, ph["color"], ph["badge"], head_h=26))
        b.append(_t(x + 14, y + 50, ph["title"], 13.5, 800, INK))
        b.append(_t(x + 14, y + 70, "WHAT YOU TYPE", 9, 800, ph["color"]))
        b.append(_r(x + 14, y + 78, 336, 84, 6, "#0F172A"))
        b.append(_tl(x + 24, y + 98, _wrap(ph["prompt"], 50, 4), 10, 700, "#A7F3D0", 15, mono=True))
        b.append(_t(x + 14, y + 184, "WHY IT WORKS", 9, 800, ph["color"]))
        b.append(_tl(x + 14, y + 200, _wrap(ph["why"], 52, 3), 10.5, 600, "#1E293B", 14))
        if i < 3:
            b.append(_flow([(x + 366, y + 123), (x + 434, y + 123)], ph["color"], phase, None, 1.4, 3.2, True, 1))
    b.append(_r(56, 402, 680, 136, 12, WHITE, LINE, 1.6))
    b.append(_t(74, 424, s["dial_title"], 11, 800, INK))
    for i, (kw, hgt) in enumerate(zip(s["dial_keywords"], (16, 30, 46, 62))):
        bx = 90 + i * 160
        g = _grow(phase)
        b.append(_r(bx, 510 - hgt * g, 92, hgt * g, 5, [SKY, BLUE, PURPLE, NAVY][i]))
        b.append(_t(bx + 46, 506 - hgt * g - 4, kw, 10, 800, INK, "middle", mono=True))
    b.append(_t(74, 528, s["dial_note"], 9.2, 700, SLATE))
    b.append(_r(760, 402, 804, 136, 12, WHITE, LINE, 1.6))
    b.append(_t(778, 426, s["claude_md_title"], 11, 800, INK))
    for i, item in enumerate(s["claude_md_items"][:8]):
        cx_, cy_ = 778 + (i % 2) * 400, 450 + (i // 2) * 22
        b.append(f'<rect x="{cx_}" y="{cy_ - 11}" width="14" height="14" rx="3" fill="#ECFDF5" stroke="{GREEN}" stroke-width="1.4"/>')
        b.append(_t(cx_ + 7, cy_, "✓", 9.5, 800, GREEN, "middle"))
        b.append(_t(cx_ + 22, cy_, item, 10.5, 600, "#1E293B"))
    for i, v in enumerate(s["variants"][:3]):
        x, y = 56 + i * 504, 556
        b.append(_card_head(x, y, 480, 304, v["color"], v["badge"], head_h=26))
        b.append(_t(x + 14, y + 50, v["title"], 13, 800, INK))
        steps = v["steps"][:5]
        for j, st in enumerate(steps):
            sx = x + 14 + j * 92
            b.append(_mb(sx, y + 64, 84, 42, st, v["color"]))
            if j < len(steps) - 1:
                b.append(_fl([(sx + 84, y + 85), (sx + 92, y + 85)], v["color"], phase))
        if v.get("loop_back"):
            b.append(_flow([(x + 14 + 3 * 92 + 42, y + 106), (x + 14 + 3 * 92 + 42, y + 120), (x + 14 + 1 * 92 + 42, y + 120), (x + 14 + 1 * 92 + 42, y + 108)], v["color"], phase, v["loop_back"], 2.0, 2.4, True, 1, dash="5 4", track=False, label_dy=12))
        b.append(_tl(x + 14, y + 168, _wrap(v["detail"], 68, 4), 10.2, 600, "#1E293B", 14.5))
        b.append(_r(x + 14, y + 242, 452, 46, 6, "#0F172A"))
        b.append(_tl(x + 24, y + 260, _wrap(v["command"], 66, 2), 9.5, 700, "#A7F3D0", 14, mono=True))
    b.append(_r(56, 880, 1508, 50, 10, NAVY))
    b.append(_t(810, 910, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T22", META["T22"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T23 — Context window budget ledger: before vs after compaction + just-in-time retrieval
# ----------------------------------------------------------------------------------------------------------------------
def render_t23(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    scale = 1488 / s["window_tokens"]
    g = _grow(phase)

    def ledger(y: float, header_y: float, label: str, segs: List[Dict[str, Any]], note: str) -> List[Point]:
        out_pts: List[Point] = []
        x = 56
        total = sum(sg["tokens"] for sg in segs)
        b.append(_t(56, header_y, label, 11, 800, INK))
        b.append(_t(1544, header_y, f"= {total // 1000}K tokens  {note}", 11, 800, INK, "end"))
        for sg in segs:
            w = sg["tokens"] * scale * g
            b.append(_r(x, y, max(2, w), 54, 4, sg["color"]))
            if w > 64:
                max_ch = max(4, int((w - 14) / 6.0))
                lbl = sg["name"] if len(sg["name"]) <= max_ch else sg["name"][: max_ch - 1].rstrip() + "…"
                b.append(_t(x + 7, y + 22, lbl, 9.8, 800, WHITE))
                b.append(_t(x + 7, y + 42, f"{sg['tokens'] // 1000}K • {int(100 * sg['tokens'] / total)}%", 9.2, 700, "#F1F5F9"))
            out_pts.append((x + w / 2, y + 54))
            x += sg["tokens"] * scale * g
        return out_pts

    before_pts = ledger(172, 160, s["before_label"], s["before"], s["before_note"])
    after_pts = ledger(314, 388, s["after_label"], s["after"], s["after_note"])
    after_w = sum(sg["tokens"] for sg in s["after"]) * scale * g
    freed_x = 56 + after_w + 14
    freed_w = max(40, 1488 - after_w - 14)
    b.append(_r(freed_x, 314, freed_w, 54, 4, "#F0FDF4", GREEN, 1.6, 'stroke-dasharray="6 6"'))
    b.append(_t(freed_x + freed_w / 2, 345, s["freed_label"], 11, 800, GREEN, "middle"))
    for i, (p0, p1) in enumerate(zip(before_pts, after_pts)):
        if i >= len(after_pts):
            break
        mid_y = 240 + i * 9
        b.append(_flow([(p0[0], p0[1] + 2), (p0[0], mid_y), (p1[0], mid_y), (p1[0], 310)], s["before"][i]["color"], phase, None, 2.2, 2.2, True, 1, dash="5 5", track=False))
    for i, pr in enumerate(s["principles"][:5]):
        x = 56 + i * 302
        b.append(_r(x, 420, 290, 216, 10, WHITE, pr["color"], 1.8))
        b.append(_r(x, 420, 290, 28, 8, pr["color"]))
        b.append(_t(x + 12, 439, f"{i + 1}. {pr['name']}", 10.5, 800, WHITE))
        b.append(_tl(x + 12, 470, _wrap(pr["how"], 40, 6), 10.5, 600, "#1E293B", 15))
        b.append(_pill(x + 12, 604, pr["stack"], pr["color"], size=9)[0])
    b.append(_r(56, 656, 740, 216, 12, "#FFF5F5", "#FCA5A5", 1.8))
    b.append(_t(74, 682, s["rot_title"], 11, 800, "#991B1B"))
    b.append(_tl(74, 706, _wrap(s["rot_body"], 92, 6), 11, 600, "#1E293B", 16))
    b.append(_r(820, 656, 744, 216, 12, "#ECFDF5", "#6EE7B7", 1.8))
    b.append(_t(838, 682, s["signals_title"], 11, 800, "#065F46"))
    for i, sig in enumerate(s["signals"][:5]):
        b.append(_t(838, 708 + i * 26, "→", 12, 800, GREEN))
        b.append(_t(858, 708 + i * 26, sig, 11, 700, "#064E3B"))
    b.append(_r(56, 888, 1508, 42, 10, NAVY))
    b.append(_t(810, 914, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T23", META["T23"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T24 — Error analysis -> failure taxonomy -> Pareto -> binary judge (Hamel Husain & Shreya Shankar method)
# ----------------------------------------------------------------------------------------------------------------------
def render_t24(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_card_head(56, 136, 470, 560, BLUE, "STEP 1 • READ 100 REAL TRACES AND WRITE WHAT WENT WRONG (OPEN CODING)"))
    for i, tr in enumerate(s["traces"][:6]):
        y = 176 + i * 84
        b.append(_r(72, y, 438, 72, 8, "#F8FAFC", LINE, 1.2))
        b.append(_t(84, y + 18, f"trace #{tr['id']}  •  {tr['user']}", 9.5, 800, SLATE, mono=True))
        b.append(_tl(84, y + 36, _wrap(tr["agent"], 66, 1), 10.5, 600, "#1E293B", 13))
        b.append(_ht(84, y + 60, f"note: {tr['note']}", 11.5, 700, "#B45309"))
    buckets = s["buckets"]
    total = sum(bk["count"] for bk in buckets) + s["pass_count"]
    b.append(_card_head(560, 136, 440, 560, PURPLE, "STEP 2 • GROUP NOTES INTO A FAILURE TAXONOMY (AXIAL CODING)"))
    for i, bk in enumerate(buckets[:5]):
        y = 180 + i * 98
        b.append(_r(576, y, 408, 84, 8, WHITE, bk["color"], 1.6))
        b.append(_r(576, y, 8, 84, 4, bk["color"]))
        b.append(_t(596, y + 22, bk["name"], 12, 800, INK))
        b.append(_t(970, y + 22, f"{bk['count']} / {total}", 12, 800, bk["color"], "end"))
        b.append(_tl(596, y + 42, _wrap(bk["definition"], 56, 2), 10, 600, "#1E293B", 13))
        b.append(_t(596, y + 76, f"example: {bk['example']}", 9.5, 700, SLATE, mono=True))
        src_y = 176 + min(i, 5) * 84 + 36
        b.append(_flow([(510, src_y), (540, src_y), (540, y + 42), (574, y + 42)], bk["color"], phase, None, 2.0, 2.2, True, 1, dash="5 5", track=False))
    b.append(_card_head(1034, 136, 530, 300, AMBER, "STEP 3 • PARETO: WHICH FAILURES ARE WORTH FIXING FIRST?"))
    ordered = sorted(buckets, key=lambda k: -k["count"])
    mx = max(k["count"] for k in ordered)
    g = _grow(phase)
    cum = 0
    for i, bk in enumerate(ordered[:5]):
        y = 184 + i * 46
        w = 216 * bk["count"] / mx * g
        cum += bk["count"]
        b.append(_t(1048, y + 18, bk["name"], 9.6, 800, INK))
        b.append(_r(1232, y, 216, 26, 4, "#F1F5F9"))
        b.append(_r(1232, y, max(3, w), 26, 4, bk["color"]))
        b.append(_t(1548, y + 18, f"{bk['count']}  (cum {int(100 * cum / max(1, total - s['pass_count']))}%)", 9.5, 800, SLATE, "end"))
    b.append(_t(1050, 420, s["pareto_note"], 10, 700, "#92400E"))
    b.append(_card_head(1034, 452, 530, 244, GREEN, "STEP 4 • ONE BINARY JUDGE PER TOP FAILURE MODE"))
    b.append(_r(1050, 492, 498, 112, 6, "#0F172A"))
    b.append(_tl(1062, 512, _wrap(s["judge_prompt"], 74, 6), 9.5, 700, "#A7F3D0", 14, mono=True))
    b.append(_t(1050, 630, "STEP 5 • CHECK THE JUDGE AGAINST HUMANS BEFORE TRUSTING IT", 9.5, 800, GREEN))
    b.append(_tl(1050, 650, _wrap(s["validation"], 76, 3), 10.5, 700, "#064E3B", 15))
    b.append(_r(56, 716, 1508, 56, 10, "#FFFBEB", "#F59E0B", 1.6))
    b.append(_t(74, 740, "WHY BINARY PASS / FAIL INSTEAD OF 1-5 SCORES", 10, 800, "#92400E"))
    b.append(_t(74, 760, s["why_binary"], 11, 700, "#1E293B"))
    b.append(_r(56, 790, 1508, 92, 12, NAVY))
    b.append(_t(78, 818, "DO THIS TODAY (90 MINUTES)", 10.5, 800, "#93C5FD"))
    for i, step in enumerate(s["today"][:3]):
        b.append(_t(78 + i * 500, 846, f"{i + 1}. {step}", 11.5, 800, WHITE))
    b.append(_t(810, 916, s["rule"], 12, 800, SLATE, "middle"))
    return _frame("T24", META["T24"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T25 — LLM-as-a-judge calibration card: confusion matrix, known biases -> fixes, judge prompt skeleton
# ----------------------------------------------------------------------------------------------------------------------
def render_t25(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    tp, fp, fn, tn = s["tp"], s["fp"], s["fn"], s["tn"]
    n = tp + fp + fn + tn
    tpr, tnr, acc = tp / (tp + fn), tn / (tn + fp), (tp + tn) / n
    p_pass_h, p_pass_j = (tp + fn) / n, (tp + fp) / n
    pe = p_pass_h * p_pass_j + (1 - p_pass_h) * (1 - p_pass_j)
    kappa = (acc - pe) / (1 - pe)
    b.append(_card_head(56, 136, 470, 520, BLUE, f"JUDGE VS. {n} HUMAN-LABELED TRACES (CONFUSION MATRIX)"))
    b.append(_t(290, 190, "HUMAN SAYS →", 9.5, 800, SLATE, "middle"))
    b.append(_t(230, 210, "PASS", 10.5, 800, GREEN, "middle"))
    b.append(_t(400, 210, "FAIL", 10.5, 800, RED, "middle"))
    b.append(_t(92, 300, "JUDGE", 9.5, 800, SLATE, "middle", extra='transform="rotate(-90 92 300)"'))
    b.append(_t(126, 282, "PASS", 10.5, 800, GREEN, "middle"))
    b.append(_t(126, 392, "FAIL", 10.5, 800, RED, "middle"))
    cells = [(150, 224, tp, "#DCFCE7", GREEN, "true pass"), (320, 224, fp, "#FEE2E2", RED, "judge too lenient"),
             (150, 334, fn, "#FEE2E2", RED, "judge too strict"), (320, 334, tn, "#DCFCE7", GREEN, "true fail")]
    show = _reveal(phase, 4)
    for i, (cx_, cy_, v, fill, col, lbl) in enumerate(cells):
        b.append(_r(cx_, cy_, 160, 100, 8, fill if i < show else "#F8FAFC", col, 1.6))
        if i < show:
            b.append(_t(cx_ + 80, cy_ + 50, str(v), 30, 800, col, "middle"))
            b.append(_t(cx_ + 80, cy_ + 80, lbl, 9.5, 800, SLATE, "middle"))
    b.append(_flow([(230, 436), (230, 462)], GREEN, phase, None, 1.2, 2.4, True, 1, track=False))
    b.append(_flow([(400, 436), (400, 462)], RED, phase, None, 1.2, 2.4, True, 1, track=False))
    metrics = [("TPR (catches real passes)", f"{tpr:.2f}", GREEN), ("TNR (catches real fails)", f"{tnr:.2f}", GREEN),
               ("Agreement", f"{int(acc * 100)}%", BLUE), ("Cohen's κ", f"{kappa:.2f}", PURPLE)]
    for i, (name, val, col) in enumerate(metrics):
        mx, my = 72 + (i % 2) * 222, 470 + (i // 2) * 84
        b.append(_r(mx, my, 210, 72, 8, "#F8FAFC", col, 1.4))
        b.append(_t(mx + 12, my + 24, name, 9.5, 800, SLATE))
        b.append(_t(mx + 12, my + 56, val, 22, 800, col))
    b.append(_t(74, 640, s["matrix_note"], 9.5, 700, "#1E293B"))
    b.append(_card_head(560, 136, 480, 520, AMBER, "5 KNOWN JUDGE BIASES → THE FIX THAT ACTUALLY WORKS"))
    for i, bias in enumerate(s["biases"][:5]):
        y = 178 + i * 94
        b.append(_r(576, y, 200, 80, 8, "#FFF7ED", "#FDBA74", 1.4))
        b.append(_t(588, y + 20, bias["name"], 10.5, 800, "#9A3412"))
        b.append(_tl(588, y + 38, _wrap(bias["symptom"], 30, 3), 9.5, 600, "#1E293B", 13))
        b.append(_fl([(778, y + 40), (820, y + 40)], AMBER, phase))
        b.append(_r(824, y, 200, 80, 8, "#ECFDF5", "#6EE7B7", 1.4))
        b.append(_t(836, y + 20, "FIX", 9.5, 800, GREEN))
        b.append(_tl(836, y + 38, _wrap(bias["fix"], 30, 3), 9.5, 700, "#064E3B", 13))
    b.append(_card_head(1074, 136, 490, 520, GREEN, "JUDGE PROMPT SKELETON (COPY, THEN FILL THE RUBRIC)"))
    b.append(_r(1090, 176, 458, 330, 6, "#0F172A"))
    b.append(_tl(1102, 196, s["prompt_lines"][:21], 9.5, 700, "#A7F3D0", 15, mono=True))
    b.append(_t(1090, 532, "CALIBRATION ROUTINE", 9.5, 800, GREEN))
    b.append(_tl(1090, 552, _wrap(s["routine"], 66, 6), 10.5, 700, "#064E3B", 15))
    b.append(_r(56, 676, 1508, 60, 10, "#FFFBEB", "#F59E0B", 1.6))
    b.append(_t(74, 700, "THE ONE NUMBER TO WATCH", 10, 800, "#92400E"))
    b.append(_t(74, 722, s["watch"], 11.5, 700, "#1E293B"))
    b.append(_r(56, 752, 1508, 120, 12, NAVY))
    b.append(_t(78, 780, "WHERE THESE RULES COME FROM", 10.5, 800, "#93C5FD"))
    for i, src in enumerate(s["sources"][:3]):
        b.append(_tl(78 + i * 500, 806, _wrap(src, 70, 3), 10.5, 700, WHITE, 15))
    b.append(_t(810, 914, s["rule"], 12, 800, SLATE, "middle"))
    return _frame("T25", META["T25"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T26 — Agent trajectory scorecard: expected vs actual tool calls, six metrics computed live
# ----------------------------------------------------------------------------------------------------------------------
def render_t26(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    exp, act = s["expected"], s["actual"]
    step = _reveal(phase, len(act))

    def row(y: float, label: str, calls: List[str], col: str, flags: Optional[List[str]] = None, highlight_upto: Optional[int] = None) -> None:
        b.append(_t(56, y - 10, label, 11, 800, INK))
        cw = min(236, int((1488 - (len(calls) - 1) * 18) / len(calls)))
        for i, c in enumerate(calls):
            x = 56 + i * (cw + 18)
            flag = flags[i] if flags else None
            fill = "#FEE2E2" if flag == "extra" else ("#DCFCE7" if flag == "ok" else WHITE)
            stroke = RED if flag == "extra" else col
            active = highlight_upto is not None and i < highlight_upto
            b.append(_r(x, y, cw, 54, 8, fill, stroke, 3 if active and i == highlight_upto - 1 else 1.6))
            b.append(_num(x + 18, y + 27, i + 1, stroke, 11))
            b.append(_t(x + 36, y + 24, c, 11, 800, INK, mono=True))
            b.append(_t(x + 36, y + 42, flag.upper() if flag else "expected", 8.5, 800, stroke))
            if i < len(calls) - 1:
                b.append(_flow([(x + cw, y + 27), (x + cw + 18, y + 27)], stroke, phase, None, 1.3, 2.4, True, 1, track=False, dash="5 4"))

    row(170, "EXPECTED TRAJECTORY (what a correct run calls, in order)", exp, BLUE)
    row(270, "ACTUAL TRAJECTORY (what the agent really called)", act, GREEN, s["actual_flags"], step)
    b.append(_card_head(56, 360, 1000, 392, NAVY, "SIX TRAJECTORY METRICS FROM THE GOOGLE 'AGENTS COMPANION' WHITEPAPER — COMPUTED FOR THIS RUN"))
    hdr = [("METRIC", 72), ("WHAT IT ASKS", 262), ("RESULT", 760), ("VERDICT", 900)]
    for name, x in hdr:
        b.append(_t(x, 404, name, 9.5, 800, SLATE))
    for i, m in enumerate(s["metrics"][:6]):
        y = 416 + i * 54
        b.append(_r(72, y, 968, 46, 6, "#F8FAFC" if i % 2 == 0 else WHITE, LINE, 1))
        b.append(_t(84, y + 28, m["name"], 11, 800, INK))
        b.append(_tl(262, y + 20, _wrap(m["asks"], 78, 2), 9.5, 600, "#1E293B", 13))
        b.append(_t(760, y + 28, m["value"], 14, 800, m["color"], mono=True))
        b.append(_pill(900, y + 12, m["verdict"], m["color"], size=9)[0])
    b.append(_card_head(1080, 360, 484, 392, PURPLE, "WHICH METRIC TO REPORT, WHEN"))
    for i, w in enumerate(s["when"][:5]):
        y = 404 + i * 66
        b.append(_r(1096, y, 452, 56, 8, "#F5F3FF", "#C4B5FD", 1.2))
        b.append(_t(1108, y + 20, w["head"], 10.5, 800, PURPLE))
        b.append(_tl(1108, y + 38, _wrap(w["body"], 62, 2), 9.5, 600, "#1E293B", 13))
    b.append(_r(56, 772, 1508, 72, 12, "#ECFDF5", "#6EE7B7", 1.8))
    b.append(_t(74, 798, "FINAL-RESPONSE CHECK (SEPARATE FROM THE TRAJECTORY)", 10, 800, "#065F46"))
    b.append(_t(74, 822, s["final_response"], 11.5, 700, "#064E3B"))
    b.append(_r(56, 862, 1508, 56, 12, NAVY))
    b.append(_t(810, 896, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T26", META["T26"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T27 — "How MCP works" 9-Step Sequence & Architecture Walkthrough (ByteByteGo + Brij Kishore Pandey format)
# ----------------------------------------------------------------------------------------------------------------------
def render_t27(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    lanes = s["lanes"][:3]
    lx = [56, 606, 1156]
    lw = 408
    cx = [x + lw / 2 for x in lx]  # [260, 810, 1360] -> 550px between adjacent lifelines!
    b.append(_r(56, 222, 1508, 562, 14, "#F8FAFC", LINE, 1.5))
    for i, ln in enumerate(lanes):
        # Subtle vertical column band & lifeline so there are zero giant empty boxes
        b.append(_r(cx[i] - 92, 228, 184, 550, 10, ln["fill"], ln["color"], 1.0, 'stroke-opacity="0.35"'))
        b.append(f'<line x1="{cx[i]:.1f}" y1="216" x2="{cx[i]:.1f}" y2="776" stroke="{ln["color"]}" stroke-width="2.2" stroke-dasharray="6 6" stroke-opacity="0.65"/>')
        # Top Actor Header Card (80px tall)
        b.append(_r(lx[i], 136, lw, 80, 12, WHITE, ln["color"], 2))
        b.append(_r(lx[i], 136, lw, 42, 10, ln["color"]))
        b.append(_t(cx[i], 155, ln["name"], 12.5, 800, WHITE, "middle"))
        b.append(_t(cx[i], 171, ln["sub"], 9.2, 700, "#F1F5F9", "middle"))
        # Center the 3 capability pills cleanly inside the 408px actor card
        chip_svgs: List[Tuple[str, int]] = []
        for ch in ln["chips"][:3]:
            w_ch = int(len(ch) * 8.2 * 0.62 + 18)
            chip_svgs.append((ch, w_ch))
        tot_w = sum(w for _, w in chip_svgs) + 10 * (len(chip_svgs) - 1)
        cur_x = cx[i] - tot_w / 2
        for ch_text, w_ch in chip_svgs:
            b.append(f'<rect x="{cur_x:.1f}" y="186" width="{w_ch}" height="20" rx="10" fill="{ln["fill"]}" stroke="{ln["color"]}" stroke-width="1.3"/>')
            b.append(_t(cur_x + w_ch / 2, 199, ch_text, 8.3, 800, ln["color"], "middle"))
            cur_x += w_ch + 10
    msgs = s["messages"][:9]
    shown = _reveal(phase, len(msgs))
    for i, m in enumerate(msgs):
        y = 252 + i * 58
        a, c = m["from"], m["to"]
        active = i < shown
        col = m["color"] if active else "#94A3B8"
        if a == c:
            cw = 376
            x0 = cx[a] - cw / 2
            b.append(_r(x0, y - 20, cw, 40, 8, WHITE, col, 2.0 if active else 1.4))
            b.append(_num(x0 + 22, y, i + 1, col, 12))
            b.append(_t(x0 + 42, y - 4, m["text"], 10.2, 800, INK))
            b.append(_t(x0 + 42, y + 12, m["sub"], 8.6, 700, SLATE, mono=True))
            continue
        xa, xc = cx[a], cx[c]
        b.append(_flow([(xa, y), (xc, y)], col, phase, None, 1.6, 3.0 if active else 2.0, True, 1 if active else 0, dash="10 7" if active else "4 6", track=active))
        b.append(f'<circle cx="{xa:.1f}" cy="{y:.1f}" r="4.5" fill="{col}"/>')
        mid_x = (xa + xc) / 2
        cw = 432
        card_x = mid_x - cw / 2
        b.append(_r(card_x, y - 20, cw, 40, 8, WHITE, col, 1.8 if active else 1.2))
        b.append(_num(card_x + 22, y, i + 1, col, 12))
        b.append(_t(card_x + 42, y - 4, m["text"], 10.2, 800, INK))
        dir_tag = "→" if c > a else "←"
        b.append(_t(card_x + 42, y + 12, f"{dir_tag} {m['sub']}", 8.6, 700, SLATE, mono=True))
    for i, nt in enumerate(s["notes"][:3]):
        x = 56 + i * 510
        b.append(_r(x, 796, 488, 78, 10, WHITE, nt["color"], 1.6))
        b.append(_r(x, 796, 8, 78, 4, nt["color"]))
        b.append(_t(x + 20, 816, nt["head"], 10, 800, nt["color"]))
        b.append(_tl(x + 20, 833, _wrap(nt["body"], 64, 3), 9.6, 600, "#1E293B", 13))
    b.append(_r(56, 886, 1508, 44, 10, NAVY))
    b.append(_t(810, 913, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T27", META["T27"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T28 — Sketch-style explainer: 5 chunking strategies (Daily Dose of Data Science format)
# ----------------------------------------------------------------------------------------------------------------------
def render_t28(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = [_r(36, 128, 1528, 812, 16, "#FFFDF5", "#E7E5E4", 2)]
    for i, st in enumerate(s["strategies"][:5]):
        x, y = 56 + i * 300, 146
        col = st["color"]
        b.append(_r(x, y, 284, 600, 14, WHITE, col, 2.2, 'transform="rotate(-0.4)"' if i % 2 == 0 else 'transform="rotate(0.4)"'))
        b.append(_ht(x + 142, y + 30, f"{i + 1}. {st['name']}", 16, 800, col, "middle"))
        dx, dy, dw, dh = x + 42, y + 50, 200, 150
        b.append(_r(dx, dy, dw, dh, 4, "#FAFAF9", "#A8A29E", 1.5))
        for k in range(9):
            b.append(f'<line x1="{dx + 12}" y1="{dy + 14 + k * 15}" x2="{dx + dw - 12 - (18 if k % 3 == 2 else 0)}" y2="{dy + 14 + k * 15}" stroke="#D6D3D1" stroke-width="2" stroke-linecap="round"/>')
        kind = st["kind"]
        cuts: List[Tuple[float, float, float, float]] = []
        if kind == "fixed":
            cuts = [(dx, dy + 37, dx + dw, dy + 37), (dx, dy + 75, dx + dw, dy + 75), (dx, dy + 112, dx + dw, dy + 112)]
        elif kind == "recursive":
            cuts = [(dx, dy + 52, dx + dw, dy + 52), (dx, dy + 98, dx + dw, dy + 98), (dx + 60, dy + 98, dx + 60, dy + dh)]
        elif kind == "structure":
            cuts = [(dx, dy + 30, dx + dw, dy + 30), (dx, dy + 90, dx + dw, dy + 90)]
            for hy in (dy + 20, dy + 80):
                b.append(_r(dx + 12, hy - 8, 70, 10, 2, col))
        elif kind == "semantic":
            cuts = [(dx, dy + 44, dx + dw, dy + 44), (dx, dy + 118, dx + dw, dy + 118)]
            for (gx, gy, gc) in [(dx + 170, dy + 22, "#F59E0B"), (dx + 170, dy + 80, "#3B82F6"), (dx + 170, dy + 134, "#10B981")]:
                b.append(f'<circle cx="{gx}" cy="{gy}" r="7" fill="{gc}" fill-opacity="0.8"/>')
        else:  # contextual
            cuts = [(dx, dy + 60, dx + dw, dy + 60), (dx, dy + 110, dx + dw, dy + 110)]
            for cy_ in (dy + 60, dy + 110):
                b.append(_r(dx + 6, cy_ + 4, 110, 12, 3, "#FEF3C7", "#F59E0B", 1))
                b.append(_ht(dx + 10, cy_ + 13, "+ 50-token context", 8, 700, "#92400E"))
        for (x1, y1, x2, y2) in cuts:
            b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 5" stroke-linecap="round"/>')
        if cuts:
            x1, y1, x2, y2 = cuts[0]
            b.append(_flow([(x1, y1), (x2, y2)], col, phase, None, 1.8, 2, False, 1, dash="6 5", track=False))
        b.append(_ht(x + 16, y + 226, "HOW IT CUTS", 10, 800, SLATE))
        b.append(_htl(x + 16, y + 246, _wrap(st["how"], 34, 3), 12, 700, INK, 16))
        b.append(_ht(x + 16, y + 306, "BEST FOR", 10, 800, GREEN))
        b.append(_htl(x + 16, y + 326, _wrap(st["best"], 34, 3), 12, 700, "#064E3B", 16))
        b.append(_ht(x + 16, y + 386, "WATCH OUT", 10, 800, RED))
        b.append(_htl(x + 16, y + 406, _wrap(st["watch"], 34, 3), 12, 700, "#7F1D1D", 16))
        b.append(_r(x + 16, y + 462, 252, 46, 8, "#F5F5F4", col, 1.4))
        b.append(_ht(x + 28, y + 482, "START WITH", 9.5, 800, col))
        b.append(_ht(x + 28, y + 500, st["start"], 11.5, 800, INK))
        b.append(_ht(x + 16, y + 540, "TOOLS", 10, 800, SLATE))
        b.append(_htl(x + 16, y + 560, _wrap(st["tools"], 36, 2), 11, 700, "#1E293B", 15))
    b.append(_r(56, 766, 1508, 86, 12, "#FEF3C7", "#F59E0B", 2))
    b.append(_ht(74, 792, s["proof_head"], 12, 800, "#92400E"))
    b.append(_htl(74, 814, _wrap(s["proof"], 150, 2), 13, 700, "#1E293B", 18))
    b.append(_r(56, 866, 1508, 62, 12, NAVY))
    b.append(_ht(810, 892, s["rule_head"], 11, 800, "#93C5FD", "middle"))
    b.append(_ht(810, 914, s["rule"], 14, 800, WHITE, "middle"))
    return _frame("T28", META["T28"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T29 — AI by Hand: Cohen's kappa for judge vs human agreement, computed on grid paper
# ----------------------------------------------------------------------------------------------------------------------
def render_t29(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = [_r(36, 128, 1528, 812, 16, "#FFFFFF", "#E7E5E4", 2)]
    for gx in range(56, 1545, 24):
        b.append(f'<line x1="{gx}" y1="140" x2="{gx}" y2="928" stroke="#E0F2FE" stroke-width="1"/>')
    for gy in range(140, 929, 24):
        b.append(f'<line x1="56" y1="{gy}" x2="1544" y2="{gy}" stroke="#E0F2FE" stroke-width="1"/>')
    items = s["items"]
    n = len(items)
    show = _reveal(phase, 6)
    b.append(_ht(80, 170, "① The raw labels (10 traces)", 15, 800, BLUE))
    b.append(_ht(104, 198, "trace", 11, 800, SLATE))
    b.append(_ht(200, 198, "human", 11, 800, SLATE))
    b.append(_ht(296, 198, "judge", 11, 800, SLATE))
    b.append(_ht(392, 198, "agree?", 11, 800, SLATE))
    for i, it in enumerate(items):
        y = 224 + i * 34
        h, j = it["human"], it["judge"]
        b.append(_ht(104, y, f"#{i + 1}", 12, 700, INK))
        b.append(_ht(200, y, h, 12, 800, GREEN if h == "PASS" else RED))
        b.append(_ht(296, y, j, 12, 800, GREEN if j == "PASS" else RED))
        b.append(_ht(392, y, "✓" if h == j else "✗", 13, 800, GREEN if h == j else RED))
    a = sum(1 for it in items if it["human"] == "PASS" and it["judge"] == "PASS")
    bb = sum(1 for it in items if it["human"] == "FAIL" and it["judge"] == "PASS")
    c = sum(1 for it in items if it["human"] == "PASS" and it["judge"] == "FAIL")
    d = sum(1 for it in items if it["human"] == "FAIL" and it["judge"] == "FAIL")
    po = (a + d) / n
    ph_, pj = (a + c) / n, (a + bb) / n
    pe = ph_ * pj + (1 - ph_) * (1 - pj)
    kappa = (po - pe) / (1 - pe)
    b.append(_ht(560, 170, "② Count the four cells", 15, 800, PURPLE))
    grid = [(608, 236, a, "a = both PASS"), (752, 236, bb, "b = judge PASS, human FAIL"), (608, 332, c, "c = judge FAIL, human PASS"), (752, 332, d, "d = both FAIL")]
    b.append(_ht(680, 222, "human PASS", 10, 800, SLATE, "middle"))
    b.append(_ht(824, 222, "human FAIL", 10, 800, SLATE, "middle"))
    for i, (gx, gy, v, lbl) in enumerate(grid):
        b.append(_r(gx, gy, 144, 92, 4, WHITE, PURPLE, 2))
        if show >= 2:
            b.append(_ht(gx + 72, gy + 48, str(v), 30, 800, PURPLE, "middle"))
            b.append(_ht(gx + 72, gy + 78, lbl, 8.5, 700, SLATE, "middle"))
    b.append(_ht(586, 290, "judge", 10, 800, SLATE, "middle", extra='transform="rotate(-90 586 290)"'))
    b.append(_ht(560, 470, "③ Observed agreement", 15, 800, BLUE))
    if show >= 3:
        b.append(_ht(560, 500, f"po = (a + d) / n = ({a} + {d}) / {n} = {po:.2f}", 15, 800, INK))
    b.append(_ht(560, 548, "④ Agreement expected by pure chance", 15, 800, AMBER))
    if show >= 4:
        b.append(_ht(560, 578, f"P(human PASS) = {a + c}/{n} = {ph_:.1f}   •   P(judge PASS) = {a + bb}/{n} = {pj:.1f}", 13, 800, INK))
        b.append(_ht(560, 604, f"pe = {ph_:.1f}×{pj:.1f} + {1 - ph_:.1f}×{1 - pj:.1f} = {ph_ * pj:.2f} + {(1 - ph_) * (1 - pj):.2f} = {pe:.2f}", 15, 800, INK))
    b.append(_ht(560, 652, "⑤ Cohen's kappa = (po − pe) / (1 − pe)", 15, 800, GREEN))
    if show >= 5:
        b.append(_ht(560, 684, f"κ = ({po:.2f} − {pe:.2f}) / (1 − {pe:.2f}) = {po - pe:.2f} / {1 - pe:.2f} = {kappa:.3f}", 16, 800, INK))
    b.append(_r(1130, 160, 414, 560, 10, "#F0FDF4", GREEN, 2))
    b.append(_ht(1150, 190, "⑥ What κ = %.2f means" % kappa, 15, 800, GREEN))
    for i, band in enumerate(s["bands"][:5]):
        y = 220 + i * 58
        hit = band["lo"] <= kappa < band["hi"]
        b.append(_r(1150, y, 374, 46, 8, "#DCFCE7" if hit else WHITE, GREEN if hit else "#D1D5DB", 2.4 if hit else 1.2))
        b.append(_ht(1164, y + 20, band["range"], 12, 800, INK))
        b.append(_ht(1164, y + 38, band["action"], 11, 700, "#1E293B"))
        if hit and show >= 6:
            b.append(_ht(1512, y + 29, "◀ you", 13, 800, GREEN, "end"))
    b.append(_ht(1150, 528, "Why not plain agreement (80%)?", 12, 800, "#92400E"))
    b.append(_htl(1150, 550, _wrap(s["why_kappa"], 46, 5), 11.5, 700, "#1E293B", 17))
    b.append(_ht(1150, 660, "Landis & Koch (1977) bands; recompute every release.", 10.5, 700, SLATE))
    # Route dashed connectors cleanly through the column gutters without crossing text
    b.append(_flow([(250, 572), (496, 572), (496, 282), (566, 282)], SKY, phase, None, 2.8, 2.2, True, 1, dash="6 6", track=False))
    b.append(_flow([(980, 678), (1096, 678), (1096, 358), (1146, 358)], GREEN, phase, None, 2.8, 2.2, True, 1, dash="6 6", track=False))
    b.append(_r(56, 760, 1508, 92, 12, NAVY))
    b.append(_ht(78, 790, "DO THIS WITH YOUR OWN JUDGE (20 MINUTES)", 12, 800, "#93C5FD"))
    for i, stp in enumerate(s["today"][:3]):
        b.append(_htl(78 + i * 500, 816, _wrap(stp, 56, 2), 12, 700, WHITE, 16))
    b.append(_ht(810, 896, s["rule"], 13, 800, SLATE, "middle"))
    return _frame("T29", META["T29"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T30 — Paper-of-the-day digest card with a recreated key chart and a "should you care?" verdict
# ----------------------------------------------------------------------------------------------------------------------
def render_t30(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_r(56, 136, 720, 600, 14, WHITE, "#334155", 2, 'filter="url(#shadow)"'))
    b.append(_r(56, 136, 720, 40, 12, "#334155"))
    b.append(_t(74, 162, "PAPER OF THE DAY", 11, 800, WHITE))
    b.append(_t(758, 162, s["paper_id"], 10, 800, "#93C5FD", "end", mono=True))
    b.append(_tl(74, 202, _wrap(s["paper_title"], 62, 2), 14.5, 800, INK, 19))
    b.append(_t(74, 246, s["paper_meta"], 10, 700, SLATE))
    b.append(_r(74, 260, 684, 58, 8, "#EFF6FF", "#93C5FD", 1.4))
    b.append(_t(86, 277, "TL;DR IN ONE SENTENCE", 9, 800, BLUE))
    b.append(_tl(86, 294, _wrap(s["tldr"], 96, 2), 10.5, 700, INK, 14))
    for i, (head, body, col) in enumerate([("PROBLEM", s["problem"], RED), ("METHOD", s["method"], PURPLE), ("RESULT", s["result"], GREEN)]):
        y = 332 + i * 88
        b.append(_r(74, y, 684, 76, 8, "#F8FAFC", col, 1.2))
        b.append(_r(74, y, 8, 76, 4, col))
        b.append(_t(94, y + 18, head, 9.5, 800, col))
        b.append(_tl(94, y + 35, _wrap(body, 96, 3), 10.2, 600, "#1E293B", 13.5))
    b.append(_t(74, 614, "WHY A BUILDER SHOULD CARE", 9.5, 800, BLUE))
    b.append(_tl(74, 632, _wrap(s["why_care"], 104, 3), 10.5, 700, INK, 14))
    b.append(_t(74, 690, "CAVEATS", 9.5, 800, AMBER))
    b.append(_tl(74, 708, _wrap(s["caveats"], 104, 2), 10.5, 600, "#1E293B", 14))
    b.append(_card_head(800, 136, 764, 360, GREEN, "THE ONE CHART (RECREATED FROM THE PAPER'S REPORTED NUMBERS)"))
    bars = s["chart"]["bars"]
    mxv = max(bar["value"] for bar in bars)
    g = _grow(phase)
    for i, bar in enumerate(bars[:4]):
        y = 188 + i * 70
        w = 310 * bar["value"] / mxv * g
        b.append(_tl(816, y + 16, _wrap(bar["label"], 30, 2), 10.2, 800, INK, 13))
        b.append(_r(1040, y, 310, 36, 6, "#F1F5F9"))
        b.append(_r(1040, y, max(3, w), 36, 6, bar["color"]))
        b.append(_t(1040 + max(3, w) + 10, y + 23, bar["display"], 11, 800, bar["color"]))
    b.append(_t(816, 470, s["chart"]["caption"], 9.5, 700, SLATE))
    mini = s["pipeline"]
    b.append(_card_head(800, 516, 764, 220, AMBER, "METHOD IN FIVE BOXES (FOLLOW THE PACKET)"))
    for i, stp in enumerate(mini[:5]):
        x = 816 + i * 148
        b.append(_mb(x, 560, 132, 52, stp, AMBER))
        if i < 4:
            b.append(_fl([(x + 132, 586), (x + 148, 586)], AMBER, phase))
    b.append(_tl(816, 648, _wrap(s["pipeline_note"], 110, 4), 10.5, 600, "#1E293B", 15))
    b.append(_r(56, 756, 1508, 100, 12, WHITE, LINE, 1.8))
    b.append(_t(74, 782, "SHOULD YOU CARE?", 10.5, 800, INK))
    gx, gy, gr = 224, 842, 54
    b.append(_flow(_arc_pts(gx, gy, gr, 180, 360), "#E2E8F0", None, None, 1, 11, False, 0, track=False, solid=True))
    verdict_angle = {"SKIP": 200, "SKIM": 270, "READ NOW": 340}[s["verdict"]]
    b.append(_flow(_arc_pts(gx, gy, gr, 180, verdict_angle), GREEN if s["verdict"] == "READ NOW" else AMBER, phase, None, 2.4, 11, False, 1, track=False, solid=True))
    b.append(_t(gx, gy - 6, s["verdict"], 11.5, 800, INK, "middle"))
    b.append(_t(gx - gr - 10, gy - 2, "SKIP", 8, 800, SLATE, "end"))
    b.append(_t(gx, gy - gr - 10, "SKIM", 8, 800, SLATE, "middle"))
    b.append(_t(gx + gr + 10, gy - 2, "READ", 8, 800, GREEN, "start"))
    b.append(_t(344, 796, "TRY IT IN 15 MINUTES", 9.5, 800, GREEN))
    for i, stp in enumerate(s["try_steps"][:3]):
        b.append(_t(344 + i * 400, 820, f"{i + 1}. {stp}", 10.2, 700, "#1E293B"))
    b.append(_t(344, 844, s["verdict_reason"], 10.2, 600, SLATE))
    b.append(_r(56, 872, 1508, 56, 12, NAVY))
    b.append(_t(810, 906, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T30", META["T30"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T31 — "I built it in N lines" runnable demo card (terminal + output + what it proves)
# ----------------------------------------------------------------------------------------------------------------------
def render_t31(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    code = s["code_lines"]
    b.append(_r(56, 136, 820, 764, 12, "#0B1220", "#1E293B", 2))
    b.append(_r(56, 136, 820, 34, 10, "#1E293B"))
    for i, c in enumerate(["#EF4444", "#F59E0B", "#22C55E"]):
        b.append(f'<circle cx="{78 + i * 18}" cy="{153}" r="5.5" fill="{c}"/>')
    b.append(_t(140, 158, s["file_name"], 11, 800, "#CBD5E1", mono=True))
    b.append(_t(860, 158, f"{len(code)} lines • runs with python3, stdlib only", 10, 800, "#86EFAC", "end", mono=True))
    for i, ln in enumerate(code[:30]):
        y = 194 + i * 23
        b.append(_t(78, y, f"{i + 1:02d}", 10, 700, "#475569", mono=True))
        color = "#86EFAC" if ln.strip().startswith("#") else ("#F8FAFC" if not ln.strip().startswith(("def ", "import ", "for ", "if ", "return")) else "#93C5FD")
        b.append(_t(110, y, ln, 11.5, 700, color, mono=True))
    b.append(_flow([(66, 190), (66, 194 + min(len(code), 30) * 23 - 10)], TEAL, phase, None, 4.0, 2, True, 2, dash="6 6", track=False))
    b.append(_r(900, 136, 664, 330, 12, "#0B1220", "#1E293B", 2))
    b.append(_r(900, 136, 664, 34, 10, "#1E293B"))
    b.append(_t(918, 158, f"$ python3 {s['file_name']}", 11, 800, "#CBD5E1", mono=True))
    out = s["output_lines"]
    shown = _reveal(phase, len(out))
    for i, ln in enumerate(out[:10]):
        y = 196 + i * 26
        if i < shown:
            col = "#FCA5A5" if "FAIL" in ln else ("#FDE68A" if "blocked" in ln or "ceiling" in ln else "#86EFAC")
            b.append(_t(918, y, ln, 11.5, 700, col, mono=True))
    if phase is not None and shown < len(out):
        b.append(_r(918, 196 + shown * 26 - 12, 10, 16, 1, "#CBD5E1"))
    b.append(_card_head(900, 486, 664, 300, GREEN, "WHAT THIS 26-LINE RUN PROVES"))
    for i, pt in enumerate(s["proves"][:4]):
        y = 526 + i * 56
        b.append(_num(930, y + 10, i + 1, GREEN, 12))
        b.append(_tl(952, y + 4, _wrap(pt, 78, 2), 10.5, 700, "#1E293B", 14))
    b.append(_t(916, 758, s["swap_note"], 10, 700, "#1D4ED8"))
    b.append(_r(900, 806, 664, 94, 12, WHITE, LINE, 1.6))
    b.append(_t(916, 830, "CLONE, RUN, READ THE RECEIPT", 9.5, 800, INK))
    b.append(_r(916, 842, 632, 46, 6, "#0F172A"))
    b.append(_tl(926, 860, _wrap(s["run_command"], 84, 2), 10, 700, "#A7F3D0", 14, mono=True))
    b.append(_t(810, 922, s["rule"], 11.5, 800, SLATE, "middle"))
    return _frame("T31", META["T31"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T32 — Andrew Ng's four agentic patterns and the HumanEval leap
# ----------------------------------------------------------------------------------------------------------------------
def render_t32(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_card_head(56, 136, 640, 440, BLUE, "THE CHART ANDREW NG SHOWED (HUMANEVAL CODING BENCHMARK, MAR 2024)"))
    bars = s["bars"]
    g = _grow(phase)
    for i, bar in enumerate(bars[:3]):
        x = 110 + i * 200
        h = 300 * bar["value"] / 100 * g
        b.append(_r(x, 520 - h, 140, h, 8, bar["color"]))
        b.append(_t(x + 70, 512 - h, f"{bar['value']:.1f}%", 20, 800, INK, "middle"))
        b.append(_tl(x + 70, 540, _wrap(bar["label"], 22, 2), 10.5, 800, SLATE, 13, "middle"))
    b.append(f'<line x1="90" y1="520" x2="680" y2="520" stroke="#94A3B8" stroke-width="1.5"/>')
    b.append(_flow([(180, 200), (380, 200), (580, 200)], GREEN, phase, "same GPT-3.5, wrapped in an agentic loop", 2.6, 3, True, 2, dash="8 7", track=False))
    b.append(_t(72, 566, s["chart_note"], 9.5, 700, SLATE))
    for i, p in enumerate(s["patterns"][:4]):
        x, y = 720 + (i % 2) * 424, 136 + (i // 2) * 224
        b.append(_card_head(x, y, 412, 212, p["color"], f"{p['name'].upper()}  •  {p['maturity']}", head_h=26))
        if p["kind"] == "evaluator":
            cy = y + 84
            b.append(_t(x + 206, y + 44, "loop until evaluator says 'meets the bar' (or max rounds)", 8.6, 700, SLATE, "middle"))
            b.append(_mb(x + 20, cy - 16, 108, 32, "Generator LLM", p["color"]))
            b.append(_fl([(x + 128, cy - 7), (x + 244, cy - 7)], p["color"], phase, label="draft"))
            b.append(_mb(x + 246, cy - 16, 110, 32, "Evaluator LLM", AMBER))
            b.append(_fl([(x + 246, cy + 9), (x + 128, cy + 9)], AMBER, phase, label="feedback", dash="4 4"))
            b.append(_fl([(x + 301, cy + 16), (x + 301, cy + 40), (x + 392, cy + 40)], GREEN, phase, label="accepted"))
        if p["kind"] == "tools":
            b.append(_mb(x + 18, y + 70, 96, 34, "LLM", p["color"]))
            for j, t in enumerate(["web search", "code exec", "calendar"]):
                b.append(_fl([(x + 114, y + 87), (x + 166, y + 50 + j * 36)], p["color"], phase))
                b.append(_mb(x + 168, y + 36 + j * 36, 94, 28, t, p["color"]))
            b.append(_t(x + 336, y + 91, "calls, reads, acts", 8.8, 700, SLATE, "middle"))
        if p["kind"] == "planning":
            steps = ["goal", "step 1", "step 2", "step 3", "done"]
            for j, t in enumerate(steps):
                b.append(_mb(x + 20 + j * 76, y + 70, 66, 30, t, p["color"]))
                if j < 4:
                    b.append(_fl([(x + 86 + j * 76, y + 85), (x + 96 + j * 76, y + 85)], p["color"], phase))
            b.append(_t(x + 206, y + 122, "LLM decomposes, then executes (e.g. HuggingGPT)", 9, 700, SLATE, "middle"))
        if p["kind"] == "multi":
            for j, t in enumerate(["CEO", "Engineer", "QA"]):
                b.append(_mb(x + 24 + j * 124, y + 48, 100, 30, t, p["color"]))
                if j < 2:
                    b.append(_fl([(x + 124 + j * 124, y + 63), (x + 148 + j * 124, y + 63)], p["color"], phase))
            b.append(_fl([(x + 324, y + 78), (x + 324, y + 104), (x + 74, y + 104), (x + 74, y + 80)], p["color"], phase, label="review loop", dash="4 4"))
            b.append(_t(x + 206, y + 126, "role-play agents debate & hand off (ChatDev, AutoGen)", 9, 700, SLATE, "middle"))
        b.append(_tl(x + 14, y + 152, _wrap(p["one_liner"], 60, 2), 10.5, 700, INK, 14))
        b.append(_t(x + 14, y + 198, p["try"], 9.5, 800, p["color"]))
    b.append(_r(56, 596, 1508, 110, 12, "#ECFDF5", "#6EE7B7", 1.8))
    b.append(_t(74, 622, "WHAT NG ACTUALLY SAID (PARAPHRASED FROM THE TALK)", 10, 800, "#065F46"))
    for i, q in enumerate(s["quotes"][:3]):
        b.append(_tl(74 + i * 500, 646, _wrap(q, 66, 3), 10.5, 700, "#064E3B", 15))
    b.append(_r(56, 726, 1508, 130, 12, WHITE, LINE, 1.8))
    b.append(_t(74, 752, "HOW TO GET THE SAME LEAP ON YOUR TASK THIS WEEK", 10.5, 800, INK))
    for i, stp in enumerate(s["week"][:4]):
        b.append(_num(86 + i * 376, 788, i + 1, BLUE, 12))
        b.append(_tl(106 + i * 376, 784, _wrap(stp, 46, 3), 10.5, 700, "#1E293B", 14))
    b.append(_r(56, 872, 1508, 56, 12, NAVY))
    b.append(_t(810, 906, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T32", META["T32"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T33 — Jagged frontier task map (Ethan Mollick)
# ----------------------------------------------------------------------------------------------------------------------
def render_t33(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_r(56, 136, 960, 740, 14, "#F8FAFC", LINE, 1.8))
    for gx in range(56, 1017, 40):
        b.append(f'<line x1="{gx}" y1="136" x2="{gx}" y2="876" stroke="#EEF2F7" stroke-width="1"/>')
    for gy in range(136, 877, 40):
        b.append(f'<line x1="56" y1="{gy}" x2="1016" y2="{gy}" stroke="#EEF2F7" stroke-width="1"/>')
    poly = s["frontier"]
    pstr = " ".join(f"{x},{y}" for x, y in poly)
    b.append(f'<polygon points="{pstr}" fill="#DCFCE7" fill-opacity="0.75" stroke="{GREEN}" stroke-width="3.5" stroke-linejoin="round" class="pulse"/>')
    b.append(_flow([tuple(p) for p in poly] + [tuple(poly[0])], GREEN, phase, None, 9.0, 2, False, 3, dash="6 6", track=False))
    b.append(_t(540, 480, "INSIDE THE FRONTIER", 14, 800, "#065F46", "middle"))
    b.append(_t(540, 500, "agents succeed reliably today — delegate these", 10.5, 700, "#047857", "middle"))
    b.append(_t(120, 170, "OUTSIDE THE FRONTIER", 12, 800, "#991B1B"))
    b.append(_t(120, 188, "looks doable, fails unpredictably — keep a human in the loop", 10, 700, "#B91C1C"))
    for tsk in s["inside"]:
        x, y = tsk["x"], tsk["y"]
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{GREEN}" stroke="{WHITE}" stroke-width="2.5"/>')
        b.append(_tl(x + 14, y - 2, _wrap(tsk["label"], 26, 2), 10.5, 800, "#064E3B", 12))
    for tsk in s["outside"]:
        x, y = tsk["x"], tsk["y"]
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{RED}" stroke="{WHITE}" stroke-width="2.5"/>')
        b.append(_tl(x + 14, y - 2, _wrap(tsk["label"], 22, 2), 10.2, 800, "#7F1D1D", 12))
    b.append(_t(540, 858, s["map_note"], 9.5, 700, SLATE, "middle"))
    b.append(_card_head(1040, 136, 524, 300, BLUE, "THE STUDY BEHIND THE IDEA (DELL'ACQUA ET AL., 2023 — 758 BCG CONSULTANTS)"))
    for i, st in enumerate(s["stats"][:4]):
        y = 178 + i * 60
        b.append(_r(1056, y, 492, 50, 8, "#F8FAFC", st["color"], 1.4))
        b.append(_t(1068, y + 32, st["value"], 20, 800, st["color"]))
        b.append(_tl(1190, y + 22, _wrap(st["label"], 54, 2), 10, 700, "#1E293B", 13))
    b.append(_card_head(1040, 456, 524, 250, AMBER, "HOW TO DRAW YOUR OWN FRONTIER (MONTHLY, 1 HOUR)"))
    for i, stp in enumerate(s["how"][:4]):
        y = 500 + i * 48
        b.append(_num(1068, y + 6, i + 1, AMBER, 12))
        b.append(_tl(1090, y + 2, _wrap(stp, 64, 2), 10.5, 700, "#1E293B", 14))
    b.append(_r(1040, 726, 524, 150, 12, NAVY))
    b.append(_t(1058, 752, "WHY THE EDGE MOVES", 10.5, 800, "#93C5FD"))
    b.append(_tl(1058, 776, _wrap(s["edge_note"], 66, 5), 10.5, 700, WHITE, 16))
    b.append(_r(56, 892, 1508, 40, 10, "#ECFDF5", "#6EE7B7", 1.6))
    b.append(_t(810, 917, s["rule"], 12, 800, "#065F46", "middle"))
    return _frame("T33", META["T33"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T34 — The lethal trifecta Venn (Simon Willison)
# ----------------------------------------------------------------------------------------------------------------------
def render_t34(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    cxs = [(400, 420), (620, 420), (510, 610)]
    cols = [BLUE, AMBER, PURPLE]
    r = 190
    b.append(_r(56, 136, 920, 740, 14, WHITE, LINE, 1.8))
    for (cx_, cy_), col, circ in zip(cxs, cols, s["circles"]):
        b.append(f'<circle cx="{cx_}" cy="{cy_}" r="{r}" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2.5"/>')
    labels_pos = [(230, 258), (790, 258), (510, 816)]
    anchors = ["start", "end", "middle"]
    for idx_c, ((lx, ly), anc, col, circ) in enumerate(zip(labels_pos, anchors, cols, s["circles"])):
        b.append(_t(lx, ly, circ["name"], 12.5, 800, col, anc))
        wrap_w, max_l = (60, 1) if idx_c == 2 else (34, 2)
        b.append(_tl(lx, ly + 16, _wrap(circ["examples"], wrap_w, max_l), 9.5, 700, SLATE, 12, anc))
    b.append(f'<circle cx="510" cy="482" r="58" fill="{RED}" fill-opacity="0.9" class="breathe"/>')
    b.append(_t(510, 462, "LETHAL", 11.5, 800, WHITE, "middle"))
    b.append(_t(510, 476, "TRIFECTA", 11.5, 800, WHITE, "middle"))
    b.append(_t(510, 490, "data walks out", 8.5, 800, "#FECACA", "middle"))
    for (cx_, cy_), col in zip(cxs, cols):
        b.append(_flow([(cx_, cy_), (510 + (cx_ - 510) * 0.36, 482 + (cy_ - 482) * 0.36)], col, phase, None, 1.8, 2, True, 1, dash="5 5", track=False))
    for st in s["setups"]:
        x, y = st["x"], st["y"]
        b.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{st["color"]}" stroke="{WHITE}" stroke-width="2.5"/>')
        b.append(_t(x, y + 4, st["id"], 9.5, 800, WHITE, "middle"))
    b.append(_t(516, 860, s["venn_note"], 9.5, 700, SLATE, "middle"))
    b.append(_card_head(1000, 136, 564, 470, RED, "SIX REAL SETUPS — WHICH LEGS DO THEY HAVE?"))
    for i, st in enumerate(s["setups"][:6]):
        y = 176 + i * 70
        b.append(_r(1016, y, 532, 60, 8, "#F8FAFC", st["color"], 1.4))
        b.append(f'<circle cx="{1038}" cy="{y + 22}" r="11" fill="{st["color"]}"/>')
        b.append(_t(1038, y + 26, st["id"], 9.5, 800, WHITE, "middle"))
        b.append(_t(1058, y + 20, st["name"], 11, 800, INK))
        b.append(_t(1536, y + 20, st["legs"], 9.5, 800, st["color"], "end"))
        b.append(_tl(1058, y + 40, _wrap(st["why"], 72, 1), 9.5, 600, "#1E293B", 12))
    b.append(_card_head(1000, 626, 564, 250, GREEN, "THE FIX IS STRUCTURAL: REMOVE ONE LEG"))
    for i, fx in enumerate(s["fixes"][:3]):
        y = 664 + i * 66
        b.append(_r(1016, y, 532, 58, 8, "#ECFDF5", "#6EE7B7", 1.2))
        b.append(_t(1030, y + 18, fx["head"], 10.2, 800, "#065F46"))
        b.append(_tl(1030, y + 34, _wrap(fx["body"], 76, 2), 9.2, 700, "#064E3B", 12))
    b.append(_r(56, 892, 1508, 40, 10, NAVY))
    b.append(_t(810, 917, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T34", META["T34"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T35 — Orchestrator + parallel subagents (Anthropic multi-agent research system) with real token economics
# ----------------------------------------------------------------------------------------------------------------------
def render_t35(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_r(56, 136, 980, 740, 14, WHITE, LINE, 1.8))
    b.append(_mb(76, 480, 110, 60, "User question (open-ended)", SLATE, size=10))
    b.append(_fl([(186, 510), (236, 510)], SLATE, phase, 1.4))
    b.append(_card_head(240, 440, 220, 140, PURPLE, "LEAD AGENT (ORCHESTRATOR)", head_h=24))
    b.append(_tl(254, 486, _wrap(s["lead"], 30, 5), 10, 700, INK, 14))
    subs = s["subagents"][:4]
    for i, sa in enumerate(subs):
        y = 160 + i * 132
        b.append(_fl([(460, 510), (500, y + 48), (536, y + 48)], PURPLE, phase, 1.8, "spawn" if i == 0 else None, dash="4 4"))
        b.append(_card_head(540, y, 250, 96, sa["color"], sa["badge"], head_h=22))
        b.append(_tl(552, y + 40, _wrap(sa["task"], 36, 3), 9.5, 700, INK, 12.5))
        b.append(_t(552, y + 86, sa["budget"], 8.5, 800, sa["color"], mono=True))
        b.append(_fl([(790, y + 48), (826, y + 48), (860, 510), (884, 510)], sa["color"], phase, 2.0, dash="6 5"))
    b.append(_card_head(886, 460, 134, 100, GREEN, "SYNTHESIS", head_h=22))
    b.append(_tl(896, 498, _wrap(s["synthesis"], 18, 4), 9.5, 700, INK, 13))
    b.append(_fl([(951, 560), (951, 600)], GREEN, phase, 1.2))
    b.append(_card_head(846, 604, 174, 76, TEAL, "CITATION AGENT", head_h=22))
    b.append(_tl(858, 646, _wrap(s["citations"], 24, 3), 9.5, 700, INK, 13))
    b.append(_fl([(931, 680), (931, 720)], TEAL, phase, 1.2))
    b.append(_mb(846, 724, 174, 50, "Answer with sources", GREEN, size=10))
    b.append(_r(76, 700, 720, 160, 10, "#F8FAFC", LINE, 1.4))
    b.append(_t(92, 724, "THE SCALING RULES THE LEAD AGENT IS TAUGHT (FROM THE POST)", 10, 800, INK))
    for i, rule in enumerate(s["scaling"][:3]):
        b.append(_t(92, 750 + i * 32, "→", 12, 800, PURPLE))
        b.append(_tl(112, 750 + i * 32, _wrap(rule, 100, 1), 10.5, 700, "#1E293B", 13))
    b.append(_card_head(1060, 136, 504, 420, NAVY, "THE NUMBERS ANTHROPIC REPORTED"))
    for i, st in enumerate(s["numbers"][:4]):
        y = 176 + i * 92
        b.append(_r(1076, y, 472, 82, 8, "#F8FAFC", st["color"], 1.6))
        b.append(_t(1092, y + 32, st["value"], 23, 800, st["color"]))
        b.append(_tl(1092, y + 52, _wrap(st["label"], 64, 2), 9.6, 700, "#1E293B", 12.5))
        b.append(_t(1536, y + 20, st["tag"], 8.5, 800, SLATE, "end", mono=True))
    b.append(_card_head(1060, 576, 504, 300, AMBER, "USE IT ONLY WHEN THE TASK LOOKS LIKE THIS"))
    for i, c in enumerate(s["use_when"][:3]):
        y = 616 + i * 50
        b.append(_t(1076, y + 10, "✓", 13, 800, GREEN))
        b.append(_tl(1096, y + 6, _wrap(c, 64, 2), 10.5, 700, "#064E3B", 14))
    for i, c in enumerate(s["dont_when"][:2]):
        y = 770 + i * 46
        b.append(_t(1076, y + 10, "✘", 13, 800, RED))
        b.append(_tl(1096, y + 6, _wrap(c, 64, 2), 10.5, 700, "#7F1D1D", 14))
    b.append(_r(56, 892, 1508, 40, 10, NAVY))
    b.append(_t(810, 917, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T35", META["T35"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T36 — Cost-per-task waterfall with levers
# ----------------------------------------------------------------------------------------------------------------------
def render_t36(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_card_head(56, 136, 1000, 640, NAVY, s["chart_title"]))
    steps = s["steps"]
    base_y, scale = 700, 640
    g = _grow(phase)
    running = 0.0
    x = 76
    bw, gap = 72, 15
    prev_top: Optional[Tuple[float, float]] = None
    shown = _reveal(phase, len(steps)) if phase is not None else len(steps)
    for i, st in enumerate(steps):
        kind = st["kind"]
        if kind == "total":
            top = base_y - running * scale * g
            b.append(_r(x, top, bw, running * scale * g, 4, st["color"]))
            b.append(_t(x + bw / 2, top - 8, f"${running:.2f}", 11.5, 800, INK, "middle"))
        else:
            delta = st["value"]
            if i >= shown:
                delta = 0.0
            y0 = base_y - running * scale * g
            running = max(0.0, running + delta)
            y1 = base_y - running * scale * g
            top, h = min(y0, y1), abs(y1 - y0)
            b.append(_r(x, top, bw, max(2, h), 4, st["color"]))
            b.append(_t(x + bw / 2, top - 8, f"{'+' if delta >= 0 else '−'}${abs(delta):.2f}", 10.5, 800, st["color"], "middle"))
            if prev_top is not None:
                b.append(f'<line x1="{prev_top[0]}" y1="{prev_top[1]}" x2="{x}" y2="{y0}" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="3 3"/>')
            prev_top = (x + bw, y1)
        b.append(_tl(x + bw / 2, base_y + 20, _wrap(st["label"], 13, 3), 9, 800, SLATE, 11.5, "middle"))
        x += bw + gap
    b.append(f'<line x1="72" y1="{base_y}" x2="1040" y2="{base_y}" stroke="#334155" stroke-width="1.5"/>')
    b.append(_flow([(72, 180), (1040, 180)], BLUE, phase, None, 4.0, 2, True, 2, dash="6 6", track=False))
    b.append(_t(80, 172, s["chart_note"], 9.5, 700, SLATE))
    b.append(_card_head(1080, 136, 484, 640, GREEN, "THE FOUR LEVERS (GOOGLE CLOUD ⇄ OPEN SOURCE)"))
    for i, lv in enumerate(s["levers"][:4]):
        y = 176 + i * 150
        b.append(_r(1096, y, 452, 136, 8, "#F8FAFC", lv["color"], 1.6))
        b.append(_r(1096, y, 8, 136, 4, lv["color"]))
        b.append(_t(1116, y + 22, lv["name"], 11, 800, lv["color"]))
        b.append(_t(1536, y + 22, lv["saves"], 12, 800, lv["color"], "end"))
        b.append(_tl(1116, y + 42, _wrap(lv["how"], 62, 3), 10, 600, "#1E293B", 14))
        b.append(_pill(1116, y + 100, lv["stack"], lv["color"], size=8.5, h=20)[0])
    b.append(_r(56, 796, 1508, 76, 12, "#FFFBEB", "#F59E0B", 1.8))
    b.append(_t(74, 822, "HOW TO BUILD YOUR OWN WATERFALL (30 MINUTES WITH OPENTELEMETRY SPANS)", 10, 800, "#92400E"))
    b.append(_tl(74, 844, _wrap(s["how_to"], 180, 2), 10.5, 700, "#1E293B", 15))
    b.append(_r(56, 892, 1508, 40, 10, NAVY))
    b.append(_t(810, 917, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T36", META["T36"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T37 — Agent incident postmortem timeline (SRE format applied to AgentOps)
# ----------------------------------------------------------------------------------------------------------------------
def render_t37(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    events = s["events"][:7]
    b.append(_flow([(130, 156), (130, 832)], RED, phase, None, 6.0, 4, True, 3, dash="12 9"))
    shown = _reveal(phase, len(events))
    for i, ev in enumerate(events):
        y = 176 + i * 98
        col = ev["color"]
        b.append(f'<circle cx="130" cy="{y + 24}" r="15" fill="{WHITE}" stroke="{col}" stroke-width="4"/>')
        b.append(_t(130, y + 28, str(i + 1), 10, 800, col, "middle"))
        b.append(_t(118, y - 2, ev["time"], 10, 800, col, "end", mono=True))
        b.append(_r(168, y, 700, 82, 10, WHITE, col, 1.8 if i < shown else 1))
        b.append(_r(168, y, 8, 82, 4, col))
        b.append(_t(190, y + 22, ev["head"], 12, 800, INK))
        b.append(_tl(190, y + 42, _wrap(ev["body"], 92, 2), 10.5, 600, "#1E293B", 14))
        b.append(_t(852, y + 22, ev["impact"], 10, 800, col, "end", mono=True))
        if ev.get("control"):
            b.append(_flow([(868, y + 41), (912, y + 41)], GREEN, phase, None, 1.4, 2.4, True, 1, track=False))
            b.append(_r(916, y + 4, 648, 74, 10, "#ECFDF5", "#6EE7B7", 1.6))
            b.append(_t(932, y + 26, f"WOULD HAVE STOPPED IT HERE: {ev['control']['name']}", 10, 800, "#065F46"))
            b.append(_tl(932, y + 44, _wrap(ev["control"]["how"], 84, 2), 10, 700, "#064E3B", 13))
            b.append(_t(1548, y + 26, ev["control"]["saves"], 10, 800, GREEN, "end", mono=True))
    b.append(_r(56, 866, 1508, 64, 12, NAVY))
    b.append(_t(78, 890, "ACTION ITEMS (OWNER • DUE)", 10, 800, "#93C5FD"))
    for i, ai in enumerate(s["actions"][:3]):
        b.append(_t(78 + i * 494, 914, ai, 10.0, 800, WHITE))
    return _frame("T37", META["T37"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T38 — Tool spec clinic: bad vs good tool definition + Anthropic's tool-writing rules
# ----------------------------------------------------------------------------------------------------------------------
def render_t38(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    for (x, w, col, fill, head, lines, notes) in [
        (56, 628, RED, "#FFF5F5", s["bad_head"], s["bad_lines"], s["bad_notes"]),
        (908, 656, GREEN, "#F0FDF4", s["good_head"], s["good_lines"], s["good_notes"]),
    ]:
        b.append(_r(x, 136, w, 560, 12, fill, col, 2))
        b.append(_r(x, 136, w, 34, 10, col))
        b.append(_t(x + 16, 158, head, 11.5, 800, WHITE))
        b.append(_r(x + 12, 182, w - 24, 330, 6, "#0F172A"))
        for i, ln in enumerate(lines[:19]):
            b.append(_t(x + 20, 202 + i * 17, ln, 9.6, 700, "#F8FAFC" if not ln.strip().startswith("//") else "#86EFAC", mono=True))
        for i, nt in enumerate(notes[:4]):
            y = 526 + i * 40
            b.append(_t(x + 16, y + 10, "✘" if col == RED else "✓", 13, 800, col))
            b.append(_tl(x + 36, y + 6, _wrap(nt, 82, 2), 9.8, 700, "#1E293B", 13))
    for i, tr in enumerate(s["arrows"][:4]):
        y = 228 + i * 80
        b.append(_flow([(686, y), (904, y)], tr["color"], phase, tr["label"], 1.8, 2.6, True, 1, dash="7 6", label_at=0.5, label_dy=-15))
    for i, rl in enumerate(s["rules"][:5]):
        x = 56 + i * 302
        b.append(_r(x, 716, 290, 150, 10, WHITE, rl["color"], 1.8))
        b.append(_r(x, 716, 290, 26, 8, rl["color"]))
        b.append(_t(x + 12, 734, f"RULE {i + 1} • {rl['name']}", 9.2, 800, WHITE))
        b.append(_tl(x + 12, 762, _wrap(rl["body"], 40, 5), 10, 600, "#1E293B", 14))
        b.append(_t(x + 12, 856, rl["example"], 8.5, 800, rl["color"], mono=True))
    b.append(_r(56, 886, 1508, 44, 10, NAVY))
    b.append(_t(810, 913, s["rule"], 12.5, 800, WHITE, "middle"))
    return _frame("T38", META["T38"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T39 — Agent memory design matrix (working / episodic / semantic / procedural) with a live request flow
# ----------------------------------------------------------------------------------------------------------------------
def render_t39(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    b.append(_r(56, 136, 1508, 170, 12, WHITE, LINE, 1.8))
    b.append(_r(72, 168, 300, 104, 10, "#EFF6FF", BLUE, 1.6))
    b.append(_t(88, 192, "USER SAYS", 9.5, 800, BLUE))
    b.append(_tl(88, 212, _wrap(s["request"], 40, 3), 11.5, 800, INK, 16))
    mems = s["memories"][:4]
    for i, m in enumerate(mems):
        x = 400 + i * 230
        b.append(_fl([(372, 220), (396, 220), (396, 200 + i * 0), (x - 4, 220)] if i == 0 else [(x - 30, 220), (x - 4, 220)], m["color"], phase, 1.4))
        b.append(_card_head(x, 170, 200, 100, m["color"], m["name"].upper(), head_h=22))
        b.append(_tl(x + 10, 212, _wrap(m["touch"], 30, 3), 9.5, 700, INK, 13))
    b.append(_fl([(1320, 220), (1356, 220)], GREEN, phase, 1.4))
    b.append(_r(1360, 168, 188, 104, 10, "#ECFDF5", GREEN, 1.6))
    b.append(_t(1374, 192, "AGENT ACTS", 9.5, 800, GREEN))
    b.append(_tl(1374, 212, _wrap(s["action"], 26, 4), 10.5, 800, "#064E3B", 14))
    cols = [("MEMORY TYPE", 56, 190), ("WHAT IT STORES (EXAMPLE)", 250, 330), ("WHERE: GOOGLE ⇄ OPEN SOURCE", 584, 330), ("FRESHNESS RULE", 918, 300), ("IF YOU SKIP IT", 1222, 342)]
    b.append(_r(56, 326, 1508, 36, 8, NAVY))
    for name, x, w in cols:
        b.append(_t(x + 12, 349, name, 9.5, 800, WHITE))
    for i, m in enumerate(mems):
        y = 370 + i * 112
        b.append(_r(56, y, 1508, 100, 10, WHITE if i % 2 == 0 else "#F8FAFC", m["color"], 1.4))
        b.append(_r(56, y, 190, 100, 10, m["color"]))
        b.append(_t(68, y + 30, m["name"], 13, 800, WHITE))
        b.append(_tl(68, y + 50, _wrap(m["analogy"], 26, 3), 9.5, 700, "#F1F5F9", 13))
        b.append(_tl(262, y + 24, _wrap(m["stores"], 48, 3), 10, 700, INK, 14))
        b.append(_t(262, y + 84, m["example"], 9, 700, SLATE, mono=True))
        b.append(_tl(596, y + 24, _wrap(m["where"], 48, 4), 10, 700, "#1E293B", 14))
        b.append(_tl(930, y + 24, _wrap(m["fresh"], 44, 4), 10, 700, "#1E293B", 14))
        b.append(_tl(1234, y + 24, _wrap(m["fail"], 50, 4), 10, 700, "#7F1D1D", 14))
    b.append(_r(56, 826, 1508, 50, 12, "#FFFBEB", "#F59E0B", 1.8))
    b.append(_t(74, 848, "THE DESIGN RULE", 9.5, 800, "#92400E"))
    b.append(_t(74, 866, s["design_rule"], 11.5, 700, "#1E293B"))
    b.append(_r(56, 892, 1508, 40, 10, NAVY))
    b.append(_t(810, 917, s["rule"], 12, 800, WHITE, "middle"))
    return _frame("T39", META["T39"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# T40 — One chart, four interventions (annotated metric line)
# ----------------------------------------------------------------------------------------------------------------------
def render_t40(s: Dict[str, Any], phase: Optional[float] = None) -> str:
    b: List[str] = []
    x0, y0, x1, y1 = 120, 170, 1004, 760
    b.append(_r(56, 136, 1024, 690, 12, WHITE, LINE, 1.8))
    pts_v = s["points"]
    mxv = max(p["value"] for p in pts_v)
    n = len(pts_v)
    coords: List[Point] = []
    for i, p in enumerate(pts_v):
        px = x0 + (x1 - x0) * i / (n - 1)
        py = y1 - (y1 - y0) * p["value"] / mxv
        coords.append((px, py))
    for k in range(5):
        gy = y1 - (y1 - y0) * k / 4
        b.append(f'<line x1="{x0}" y1="{gy}" x2="{x1}" y2="{gy}" stroke="#E2E8F0" stroke-width="1"/>')
        b.append(_t(x0 - 10, gy + 4, f"{mxv * k / 4:.0f}{s['unit']}", 9.5, 700, SLATE, "end"))
    for i, (px, py) in enumerate(coords):
        b.append(_t(px, y1 + 18, pts_v[i]["x"], 9.5, 700, SLATE, "middle"))
    reveal_n = max(2, _reveal(phase, n))
    b.append(_flow(coords[:reveal_n], BLUE, phase, None, 5.0, 3.4, False, 1, track=False, solid=True))
    for i, (px, py) in enumerate(coords[:reveal_n]):
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{BLUE}" stroke="{WHITE}" stroke-width="2"/>')
        b.append(_t(px, py - 12, f"{pts_v[i]['value']}{s['unit']}", 9.5, 800, INK, "middle"))
    flag_ys = [188, 188, 232, 188]
    for j, ev in enumerate(s["events"][:4]):
        idx = ev["point_index"]
        if idx >= reveal_n:
            continue
        px, py = coords[idx]
        fy = flag_ys[j] if j < len(flag_ys) else 188
        fw = 132
        fx = min(max(px - fw / 2, x0), 1068 - fw)
        b.append(f'<line x1="{px}" y1="{py - 22}" x2="{px}" y2="{fy + 28}" stroke="{ev["color"]}" stroke-width="1.6" stroke-dasharray="4 4"/>')
        b.append(_r(fx, fy, fw, 28, 6, ev["color"]))
        b.append(_t(fx + fw / 2, fy + 18, f"{j + 1}. {ev['flag']}", 9.2, 800, WHITE, "middle"))
    b.append(_t(568, 800, s["chart_note"], 9.5, 700, SLATE, "middle"))
    b.append(_card_head(1104, 136, 460, 690, NAVY, "WHAT EACH FLAG CHANGED"))
    for j, ev in enumerate(s["events"][:4]):
        y = 176 + j * 128
        b.append(_r(1120, y, 428, 116, 8, "#F8FAFC", ev["color"], 1.6))
        b.append(_r(1120, y, 8, 116, 4, ev["color"]))
        b.append(_t(1140, y + 22, f"{j + 1}. {ev['name']}", 11, 800, ev["color"]))
        b.append(_t(1536, y + 22, ev["delta"], 11, 800, ev["color"], "end", mono=True))
        b.append(_tl(1140, y + 42, _wrap(ev["what"], 58, 3), 10, 600, "#1E293B", 14))
        b.append(_pill(1140, y + 86, ev["stack"], ev["color"], size=8.5, h=20)[0])
    b.append(_r(1120, 692, 428, 118, 8, "#ECFDF5", "#6EE7B7", 1.6))
    b.append(_t(1136, 716, "MAKE YOUR OWN IN A WEEK", 9.5, 800, "#065F46"))
    b.append(_tl(1136, 736, _wrap(s["how_to"], 60, 5), 10, 700, "#064E3B", 14))
    b.append(_r(56, 846, 1508, 84, 12, NAVY))
    b.append(_t(78, 874, "WHY THIS FORMAT WORKS", 10, 800, "#93C5FD"))
    b.append(_tl(78, 896, _wrap(s["why_format"], 180, 2), 11.5, 800, WHITE, 16))
    return _frame("T40", META["T40"], s["title"], s["subtitle"], b, s["source"], s["lineage"])


# ----------------------------------------------------------------------------------------------------------------------
# Metadata + demo specs
# ----------------------------------------------------------------------------------------------------------------------
META: Dict[str, Dict[str, Any]] = {
    "T21": {"name": "Pattern Picker", "best_for_short": "Which agent pattern to use", "content_types": ["Educational", "Grounded concepts", "Professional knowledge sharing"], "when_to_use": "A reader asks 'should this be a chain, a router, parallel calls, an orchestrator, an evaluator loop, or an agent?'", "dynamic": "Six live mini-schematics with packets; gate diamonds; feedback loops.", "lineage": "Anthropic, Building effective agents (Dec 2024)"},
    "T22": {"name": "Claude Code Playbook", "best_for_short": "Copy-paste agentic coding", "content_types": ["Working solution", "Professional knowledge sharing", "Easy to understand"], "when_to_use": "Teach the Explore → Plan → Code → Commit loop + Boris Cherny's 10 internal Claude Code habits (/loop, /desktop, /context, Goal+Effort+Check).", "dynamic": "Phase arrows, growing thinking-budget bars, TDD loop-back arrow.", "lineage": "Charlie Hills (Boris Cherny 10 Claude Code tips & 42 add-ons) • Anthropic Claude Code guide"},
    "T23": {"name": "Context Budget Ledger", "best_for_short": "Token budgets & compaction", "content_types": ["Grounded concepts", "Information", "Working solution"], "when_to_use": "Show exactly where 200K tokens go and what compaction + just-in-time retrieval frees up.", "dynamic": "Stacked ledgers grow; packets migrate from the bloated budget to the lean one.", "lineage": "Anthropic, Effective context engineering (Sep 2025)"},
    "T24": {"name": "Error Analysis Board", "best_for_short": "Evals that start from real traces", "content_types": ["Evaluation results", "Professional knowledge sharing", "Working solution"], "when_to_use": "Walk a team from 100 traces to a failure taxonomy, a Pareto, and a binary judge per failure mode.", "dynamic": "Notes flow into taxonomy buckets; Pareto bars grow.", "lineage": "Hamel Husain & Shreya Shankar, AI Evals method"},
    "T25": {"name": "Judge Calibration Card", "best_for_short": "Trustworthy LLM-as-a-judge", "content_types": ["Evaluation results", "Research topics", "Professional knowledge sharing"], "when_to_use": "Before anyone quotes a judge score: confusion matrix vs humans, known biases, the fix for each, a prompt skeleton.", "dynamic": "Matrix cells reveal in sequence; bias → fix arrows carry packets.", "lineage": "Eugene Yan • Shreya Shankar • MT-Bench (Zheng et al. 2023)"},
    "T26": {"name": "Trajectory Scorecard", "best_for_short": "Scoring agent tool calls", "content_types": ["Evaluation results", "Proof of concept", "Grounded concepts"], "when_to_use": "Explain how to grade an agent's tool-call sequence, not just its final answer.", "dynamic": "Packets step through expected vs actual calls; metric rows compute live.", "lineage": "Google, Agents Companion whitepaper (Feb 2025)"},
    "T27": {"name": "How-It-Works Walkthrough", "best_for_short": "Protocol explainers (MCP)", "content_types": ["Educational", "Easy to understand", "Information"], "when_to_use": "A numbered sequence & lifeline walkthrough of a protocol or control plane (MCP 9-message JSON-RPC 2.0 flow).", "dynamic": "Numbered message cards light up in order with packets traveling across 3 lifelines.", "lineage": "Brij Kishore Pandey (7-Layer Control Plane & MCP) • ByteByteGo • MCP specification"},
    "T28": {"name": "Sketch Explainer", "best_for_short": "Hand-drawn concept cards", "content_types": ["Educational", "Easy to understand", "Grounded concepts"], "when_to_use": "A warm, sketched comparison of 5 options (here: chunking strategies) with 'start with' defaults.", "dynamic": "Scissor packets travel the cut lines; tilted cards; marker typography.", "lineage": "Avi Chawla & Akshay Pachaar sketch format • Anthropic Contextual Retrieval (Sep 2024)"},
    "T29": {"name": "AI by Hand", "best_for_short": "Worked calculations", "content_types": ["Educational", "Evaluation results", "Grounded concepts"], "when_to_use": "Readers verify the math themselves: here Cohen's kappa for judge vs human agreement on grid paper.", "dynamic": "Steps reveal one by one; a packet traces the computation path.", "lineage": "Tom Yeh, AI by Hand format"},
    "T30": {"name": "Paper of the Day", "best_for_short": "30-second paper digests", "content_types": ["Research topics", "Information", "Educational"], "when_to_use": "One paper, one recreated chart, problem/method/result, caveats, and a read/skim/skip verdict.", "dynamic": "Chart bars grow; verdict gauge fills; method pipeline carries a packet.", "lineage": "Pascal Biese (LLM Watch) & Elvis Saravia (DAIR.AI) digest format"},
    "T31": {"name": "Runnable Demo Card", "best_for_short": "'I built it in 26 lines'", "content_types": ["Working solution", "Proof of concept", "Easy to understand"], "when_to_use": "Show real code, the real output, and what it proves — then the clone command.", "dynamic": "Terminal output types in line by line; a packet runs down the code gutter.", "lineage": "Shubham Saboo (awesome-llm-apps) & Nir Diamant demo-repo format"},
    "T32": {"name": "Ng's Four Patterns", "best_for_short": "Agentic workflow basics", "content_types": ["Educational", "Ideas", "Easy to understand"], "when_to_use": "Explain why agentic loops beat bigger models with the HumanEval chart and the four design patterns.", "dynamic": "Bars grow to 95.1%; each pattern has a live mini-loop.", "lineage": "Andrew Ng, Sequoia AI Ascent (Mar 2024)"},
    "T33": {"name": "Jagged Frontier Map", "best_for_short": "Where agents work today", "content_types": ["Ideas", "Professional knowledge sharing", "Grounded concepts"], "when_to_use": "Place concrete tasks inside/outside the capability frontier and show how to redraw it monthly.", "dynamic": "Frontier edge pulses with orbiting packets.", "lineage": "Ethan Mollick, jagged frontier (Dell'Acqua et al. 2023)"},
    "T34": {"name": "Lethal Trifecta Venn", "best_for_short": "5-second agent security test", "content_types": ["Easy to understand", "Grounded concepts", "Professional knowledge sharing"], "when_to_use": "Any agent that has private data + untrusted content + outbound comms can be made to leak; show which leg to remove.", "dynamic": "Packets from each circle converge on a pulsing danger core.", "lineage": "Simon Willison, The lethal trifecta for AI agents (Jun 2025)"},
    "T35": {"name": "Orchestrator + Subagents", "best_for_short": "Multi-agent research systems", "content_types": ["Grounded concepts", "Research topics", "Working solution"], "when_to_use": "Explain lead/subagent fan-out and when 15x tokens is worth it, with Anthropic's reported numbers.", "dynamic": "Spawn packets fan out and results fan back in to synthesis.", "lineage": "Anthropic, How we built our multi-agent research system (Jun 2025)"},
    "T36": {"name": "Cost Waterfall", "best_for_short": "Where the money goes", "content_types": ["Evaluation results", "Information", "Professional knowledge sharing"], "when_to_use": "Decompose cost per task into tokens, tools, retries, judges — then show the four levers.", "dynamic": "Waterfall bars drop in sequence; a scan packet crosses the chart.", "lineage": "Chip Huyen-style practical AI economics"},
    "T37": {"name": "Incident Postmortem", "best_for_short": "AgentOps & Kill-Switch", "content_types": ["Easy to understand", "Professional knowledge sharing", "Working solution"], "when_to_use": "Tell the $84 retry-storm story on a timeline and name the control + kill-switch that stops it at each step.", "dynamic": "Severity packets run down the timeline; green control cards attach per event.", "lineage": "Brij Kishore Pandey (How Do We Turn It Off? & 10-Field Agent Record) • Google SRE Postmortem"},
    "T38": {"name": "Tool Spec Clinic", "best_for_short": "Tool definitions agents use well", "content_types": ["Working solution", "Proof of concept", "Professional knowledge sharing"], "when_to_use": "Bad vs good tool JSON side by side with the five rules from Anthropic's tool-writing guide.", "dynamic": "Transformation arrows jump from each flaw to its fix.", "lineage": "Anthropic (Writing effective tools) • Brij Kishore Pandey (5-Layer Claude Code ADK & SKILL.md)"},
    "T39": {"name": "Memory Design Matrix", "best_for_short": "Agent memory decisions", "content_types": ["Grounded concepts", "Educational", "Information"], "when_to_use": "One request touches four memory types; decide what to store where, with freshness rules.", "dynamic": "A request packet touches each memory store before the agent acts.", "lineage": "CoALA (Sumers et al. 2023) • Lilian Weng (2023) • Aishwarya Naresh Reganti memory infographics"},
    "T40": {"name": "One-Chart Changelog", "best_for_short": "Cause → effect on one metric", "content_types": ["Evaluation results", "Proof of concept", "Ideas"], "when_to_use": "One metric over time, four annotated architecture changes, what each changed — build-in-public style.", "dynamic": "The line draws progressively; flags appear as the line reaches them.", "lineage": "Nate B. Jones 'one chart' • Santiago Valdarrama build-in-public"},
}

RENDERERS_V2 = {
    "T21": render_t21, "T22": render_t22, "T23": render_t23, "T24": render_t24, "T25": render_t25,
    "T26": render_t26, "T27": render_t27, "T28": render_t28, "T29": render_t29, "T30": render_t30,
    "T31": render_t31, "T32": render_t32, "T33": render_t33, "T34": render_t34, "T35": render_t35,
    "T36": render_t36, "T37": render_t37, "T38": render_t38, "T39": render_t39, "T40": render_t40,
}


DEMO_CODE_T31 = [
    "import hashlib, json",
    "",
    "def fingerprint(tool, args):",
    "    raw = tool + json.dumps(args, sort_keys=True)",
    "    return hashlib.sha256(raw.encode()).hexdigest()[:8]",
    "",
    "def run_agent(plan, tools, max_steps=15, max_usd=0.25):",
    "    seen, spent, log = {}, 0.0, []",
    "    for step, (tool, args) in enumerate(plan, 1):",
    "        key = fingerprint(tool, args)",
    "        if seen.get(key, 0) >= 2:                      # 3rd identical call",
    "            log.append(f'step {step}: {tool} blocked (3rd identical call) -> strategy shift')",
    "            continue",
    "        ok, cost = tools[tool](**args)",
    "        seen[key] = seen.get(key, 0) + 1",
    "        spent += cost",
    "        log.append(f\"step {step}: {tool}{args} -> {'ok' if ok else 'FAIL'} (${spent:.2f})\")",
    "        if spent > max_usd:                            # hard cost ceiling",
    "            log.append('budget ceiling hit -> escalate to human'); break",
    "        if ok and tool == 'verify':                    # deterministic 'done'",
    "            log.append(f'exit_code=0 -> done in {step} steps, ${spent:.2f}'); break",
    "    return log",
    "",
    "tools = {'search': lambda q: (q != 'flaky', 0.01), 'verify': lambda: (True, 0.0)}",
    "plan = [('search', {'q': 'flaky'})] * 3 + [('search', {'q': 'stable'}), ('verify', {})]",
    "print('\\n'.join(run_agent(plan, tools)))",
]

DEMO_OUTPUT_T31 = [
    "step 1: search{'q': 'flaky'} -> FAIL ($0.01)",
    "step 2: search{'q': 'flaky'} -> FAIL ($0.02)",
    "step 3: search blocked (3rd identical call) -> strategy shift",
    "step 4: search{'q': 'stable'} -> ok ($0.03)",
    "step 5: verify{} -> ok ($0.03)",
    "exit_code=0 -> done in 5 steps, $0.03",
]


def demo_specs_v2() -> Dict[str, Dict[str, Any]]:
    return {
        "T21": {
            "title": "Six Ways to Wire an LLM — and the One Question That Picks the Right One",
            "subtitle": "Anthropic's advice after a year with dozens of teams: the best systems used simple, composable patterns, not frameworks. Pick the simplest one that fits.",
            "source": "Anthropic Engineering, 'Building effective agents' (Erik Schluntz & Barry Zhang, Dec 19 2024)",
            "lineage": "Anthropic, Building effective agents (Dec 2024)",
            "rule": "Ask first: can I predict the steps? Yes → a workflow (1-5). No, and I can verify results → an agent (6). Start simple; add complexity only when it measurably helps.",
            "patterns": [
                {"name": "Prompt chaining", "tag": "workflow", "kind": "chain", "color": BLUE, "use": "The task splits into fixed, ordered steps and you trade a little latency for higher accuracy on each step.", "avoid": "Steps are not predictable, or one call already does the job well.", "example": "Write marketing copy → programmatic check it fits the brief → translate it. The gate stops bad drafts early."},
                {"name": "Routing", "tag": "workflow", "kind": "route", "color": PURPLE, "use": "Inputs fall into distinct categories that are handled better by separate prompts or cheaper/stronger models.", "avoid": "Categories blur together — a misroute is worse than one general prompt.", "example": "Support: refunds, technical, general each get a specialist prompt; easy questions go to a small, cheap model."},
                {"name": "Parallelization", "tag": "workflow", "kind": "parallel", "color": SKY, "use": "Independent subtasks (sectioning) or you want several opinions (voting) — speed or confidence.", "avoid": "Subtasks depend on each other's output.", "example": "One model answers while a guardrail model screens the input; three votes decide 'is this code vulnerable?'"},
                {"name": "Orchestrator-workers", "tag": "workflow", "kind": "orchestrator", "color": AMBER, "use": "You cannot predict the subtasks up front — a central LLM decides them and delegates.", "avoid": "Subtasks are known ahead of time (use parallelization — it is simpler).", "example": "A coding change that touches an unknown set of files: the orchestrator picks files, workers edit each one."},
                {"name": "Evaluator-optimizer", "tag": "workflow", "kind": "evaluator", "color": TEAL, "use": "You have clear evaluation criteria and iterating on feedback measurably improves the result.", "avoid": "There is no reliable way to judge the output.", "example": "Literary translation: one model drafts, a critic flags lost nuance, repeat until the critic is satisfied."},
                {"name": "Autonomous agent", "tag": "agent", "kind": "agent", "color": GREEN, "use": "Open-ended problems where you can't script the path, in a trusted environment with ground-truth feedback (tests, tool results).", "avoid": "A workflow would do; cost, latency, and compounding errors are real.", "example": "SWE-bench-style coding: edit until the tests pass; stop at max steps or a human checkpoint."},
            ],
        },
        "T22": {
            "title": "The Claude Code Loop That Ships: Explore → Plan → Code → Commit (with the exact words to type)",
            "subtitle": "Anthropic's best-practices guide + Charlie Hills's Boris Cherny 10-Change Cheatsheet (Goal + Effort + Check, /context, /loop, and 'Check it works in Chrome').",
            "source": "Anthropic Engineering, 'Claude Code: Best practices for agentic coding' (Apr 2025) • Charlie Hills, 'How Does Boris Cherny Use Claude Code Now?' & '42 Things to Install'",
            "lineage": "Charlie Hills (Boris Cherny 10 Claude Code changes & 42 add-ons) • Anthropic Claude Code guide",
            "rule": "Never let it code first. Goal + Effort (/effort high) + Check ('Check it works in Chrome') → Explore → Plan → Code → Commit & fold repeat fixes into CLAUDE.md or a skill.",
            "phases": [
                {"badge": "PHASE 1 • EXPLORE", "title": "Read & check /context first", "color": BLUE, "prompt": "Read src/auth/ and tests/test_auth.py. Do NOT write code yet. Run /context to keep the window under 60% and summarize where token refresh could race.", "why": "Loading the right files first and pruning stale MCP tools with /context keeps the plan grounded."},
                {"badge": "PHASE 2 • PLAN", "title": "Make it think, or Shift+Tab auto", "color": PURPLE, "prompt": "think hard (or /effort high): propose a plan to fix the refresh race. List files to change, the failing test to add first, and risks. Wait for my OK.", "why": "'think' < 'think hard' < 'think harder' < 'ultrathink' (and /effort high) allocate progressively larger reasoning budgets."},
                {"badge": "PHASE 3 • CODE", "title": "Goal + Effort + Check in Chrome", "color": AMBER, "prompt": "Implement the approved plan. Add the failing test first, make it pass, run the full suite, and check it works in Chrome before showing me the diff.", "why": "Tests + real browser verification ('Check it works in Chrome') let the agent close the loop itself."},
                {"badge": "PHASE 4 • COMMIT", "title": "Ship & promote to CLAUDE.md / skill", "color": GREEN, "prompt": "Commit with root cause, open a PR, and if you fixed a recurring mistake twice, fold the rule into CLAUDE.md or a reusable SKILL.md.", "why": "Boris Cherny's #10 rule: every repeated correction belongs in CLAUDE.md or a skill so the next session starts smarter."},
            ],
            "dial_title": "THINKING BUDGET DIAL (THE KEYWORDS ARE LITERAL)",
            "dial_keywords": ["think", "think hard", "think harder", "ultrathink"],
            "dial_note": "Pair with /effort high for architecture planning; use Shift+Tab auto mode once CLAUDE.md + tests lock the rails.",
            "claude_md_title": "CLAUDE.md & BORIS CHERNY 10-CHANGE CHECKLIST (CHARLIE HILLS)",
            "claude_md_items": ["Common bash commands (build, test, lint) + core files", "Prompting formula: Goal + Effort (/effort high) + Check", "Browser check: 'Check it works in Chrome' (Puppeteer/Playwright)", "Context hygiene: run > /context to prune unused MCP servers", "Parallel sessions: > claude agents + > /desktop worktrees", "Recurring loops: > /loop for polling & > /schedule for PR review", "Mobile continuity: > /remote-control from phone/tablet", "Keep CLAUDE.md under ~100 lines; move workflows to SKILL.md"],
            "variants": [
                {"badge": "VARIANT A • TEST-DRIVEN", "title": "Write tests → commit → code → iterate → commit", "color": GREEN, "steps": ["write failing tests", "confirm they fail", "commit tests", "code until green", "commit"], "loop_back": "iterate", "detail": "Tell it explicitly: 'we are doing TDD, do not write implementation yet'. Then let it loop against the tests — this is where agents shine.", "command": "claude \"Write tests for the refresh race based on these cases; don't implement yet. Confirm they fail.\""},
                {"badge": "VARIANT B • VISUAL ITERATION", "title": "Screenshot → implement → screenshot → compare", "color": PURPLE, "steps": ["paste mock", "implement", "screenshot", "compare", "repeat"], "loop_back": "until it matches", "detail": "Give it a way to see results (Puppeteer MCP, iOS simulator, or pasted screenshots). Output quality jumps after 2-3 visual iterations.", "command": "claude \"Implement this mock (pasted). Take a screenshot with the Puppeteer tool and iterate until it matches.\""},
                {"badge": "VARIANT C • HEADLESS & PARALLEL", "title": "Automate with -p; parallelize with /desktop & worktrees", "color": SKY, "steps": ["claude -p", "/schedule", "worktree A", "worktree B", "merge"], "loop_back": None, "detail": "Headless mode (-p) and /schedule run in CI; /desktop and separate git worktrees let several Claude sessions work on independent tasks in parallel.", "command": "claude -p \"Triage this issue and label it\" --output-format stream-json   |   git worktree add ../feat-a -b feat-a"},
            ],
        },
        "T23": {
            "title": "Where Your 200K Tokens Actually Go — and the 60K Version That Works Better",
            "subtitle": "Example budget for a coding agent at turn 12. Anthropic's rule: find the smallest set of high-signal tokens that maximizes the chance of the outcome you want.",
            "source": "Anthropic Engineering, 'Effective context engineering for AI agents' (Sep 29 2025) • Chroma 'Context Rot' study",
            "lineage": "Anthropic, Effective context engineering (Sep 2025)",
            "window_tokens": 200000,
            "before_label": "BEFORE — everything dumped into one window (example budget)",
            "before_note": "• attention is spread across 128K tokens of mostly stale material",
            "before": [
                {"name": "System prompt", "tokens": 3000, "color": "#334155"},
                {"name": "All 85 tool schemas", "tokens": 35000, "color": RED},
                {"name": "Rules / CLAUDE.md", "tokens": 4000, "color": BLUE},
                {"name": "Raw retrieved files & logs", "tokens": 60000, "color": AMBER},
                {"name": "Full chat history", "tokens": 70000, "color": PURPLE},
                {"name": "Notes", "tokens": 3000, "color": TEAL},
                {"name": "Output reserve", "tokens": 25000, "color": "#94A3B8"},
            ],
            "after_label": "AFTER — compaction + just-in-time retrieval + top-3 tools (same task)",
            "after_note": "• 70% smaller, rules stay near the top, nothing important lost",
            "after": [
                {"name": "System", "tokens": 3000, "color": "#334155"},
                {"name": "Top-3 tools", "tokens": 2400, "color": RED},
                {"name": "Rules", "tokens": 4000, "color": BLUE},
                {"name": "JIT pointers + 2 files", "tokens": 12000, "color": AMBER},
                {"name": "Compacted summary", "tokens": 10000, "color": PURPLE},
                {"name": "Notes", "tokens": 3600, "color": TEAL},
                {"name": "Output reserve", "tokens": 25000, "color": "#94A3B8"},
            ],
            "freed_label": "freed: 140K tokens of attention",
            "principles": [
                {"name": "Smallest high-signal set", "color": BLUE, "how": "Every token competes for attention. Cut anything the model does not need for the next step — especially stale tool outputs.", "stack": "Rule for any model"},
                {"name": "Just-in-time retrieval", "color": AMBER, "how": "Keep lightweight identifiers (paths, URLs, queries) in context and load the content only when the step needs it — the way Claude Code uses grep and head.", "stack": "GCS / MinIO pointers"},
                {"name": "Compaction at a threshold", "color": PURPLE, "how": "When the window nears its limit, summarize decisions, unresolved bugs, and next steps; drop raw tool results; re-initiate with the summary.", "stack": "ADK compactor • LangMem"},
                {"name": "Structured note-taking", "color": TEAL, "how": "Persist progress notes outside the window (NOTES.md, a memory tool) and pull them back after compaction — memory that survives the reset.", "stack": "Firestore • PostgreSQL"},
                {"name": "Sub-agent isolation", "color": GREEN, "how": "Give exploration to a subagent with a clean window; it returns a 1-2K token condensed summary instead of flooding the lead agent.", "stack": "ADK subagents • LangGraph subgraph"},
            ],
            "rot_title": "WHY BIGGER WINDOWS DID NOT SAVE YOU (CONTEXT ROT)",
            "rot_body": "As token count grows, the model's ability to recall and follow instructions degrades — well before the hard limit. Anthropic calls the usable capacity an 'attention budget'; Chroma measured the decline across 18 models. The fix is curation, not capacity.",
            "signals_title": "COMPACT WHEN YOU SEE ANY OF THESE",
            "signals": ["Window above ~60% used", "A single tool result larger than ~2KB", "More than ~15 turns on one task", "The model re-asks something it already knew", "You are about to spawn a subagent anyway"],
            "rule": "Treat context like a budget you spend, not a bucket you fill.",
        },
        "T24": {
            "title": "Stop Guessing Why Your Agent Fails: Read 100 Traces, Build a Taxonomy, Then Write the Judge",
            "subtitle": "The error-analysis method Hamel Husain and Shreya Shankar teach: look at the data first; evals come out of it, not the other way round. Example run on a support agent.",
            "source": "Hamel Husain, 'Your AI product needs evals' & LLM evals FAQ • Shreya Shankar et al., 'Who Validates the Validators?' (2024)",
            "lineage": "Hamel Husain & Shreya Shankar, AI Evals method",
            "rule": "Counts are an example run (90 failing + 10 passing traces); the method is the point.",
            "traces": [
                {"id": "0412", "user": "'Refund order 88213, I was charged twice'", "agent": "Issued one refund, never checked the duplicate charge.", "note": "ignored the second charge"},
                {"id": "0419", "user": "'Change my delivery to Friday'", "agent": "Said 'done' — no tool call was made.", "note": "fabricated a tool result"},
                {"id": "0433", "user": "'Cancel and refund'", "agent": "Asked 'are you sure?' three times.", "note": "over-asking, never acted"},
                {"id": "0447", "user": "'Where is order 88790?'", "agent": "Called get_order with the wrong ID (88970).", "note": "wrong tool arguments"},
                {"id": "0451", "user": "'Refund to my original card'", "agent": "Refunded to store credit.", "note": "ignored user constraint"},
                {"id": "0466", "user": "'Send me the invoice'", "agent": "Pasted raw JSON in the reply.", "note": "formatting, unreadable"},
            ],
            "pass_count": 10,
            "buckets": [
                {"name": "Wrong tool or arguments", "count": 31, "color": RED, "definition": "Right intent, wrong call: bad ID, wrong tool, missing required field.", "example": "get_order(88970) instead of 88790"},
                {"name": "Ignored a user constraint", "count": 22, "color": AMBER, "definition": "The answer is plausible but violates something the user said explicitly.", "example": "refund to store credit, not the card"},
                {"name": "Fabricated a tool result", "count": 17, "color": PURPLE, "definition": "Claims an action happened; no tool call exists in the trace.", "example": "'done' with zero tool calls"},
                {"name": "Over-asking / never acts", "count": 12, "color": SKY, "definition": "Loops on clarifying questions when it already has enough to act.", "example": "'are you sure?' x3"},
                {"name": "Formatting / unreadable", "count": 8, "color": "#64748B", "definition": "Correct content, unusable presentation.", "example": "raw JSON in a customer reply"},
            ],
            "pareto_note": "Two failure modes explain 59% of failures — fix those first; the long tail can wait.",
            "judge_prompt": "You are grading ONE failure mode only: 'Fabricated a tool result'. Read the trace. Did the assistant claim an action (refund, change, send) that has no matching tool call in the trace? Answer PASS if no fabricated claims, FAIL otherwise. Then give one sentence of evidence quoting the trace. Output JSON: {\"verdict\": \"PASS|FAIL\", \"evidence\": \"...\"}",
            "validation": "Label 40 held-out traces by hand. Run the judge. Require TPR >= 0.90 and TNR >= 0.90 before using it on thousands of traces; recheck after every prompt change.",
            "why_binary": "A 1-5 score hides what went wrong and drifts between graders. PASS/FAIL per failure mode, with a quoted reason, is reproducible and tells engineers exactly what to fix.",
            "today": ["Export 100 recent traces into a sheet; add a 'what went wrong' column.", "Group notes into 5-8 named failure modes; count them.", "Write one binary judge for the top mode; validate on 40 hand-labeled traces."],
        },
        "T25": {
            "title": "Before You Quote a Judge Score: Calibrate It Like a Lab Instrument",
            "subtitle": "A judge is only as good as its agreement with humans on cases where you know the answer. Example: 100 hand-labeled traces, one binary judge.",
            "source": "Zheng et al., 'Judging LLM-as-a-Judge with MT-Bench' (2023) • Shankar et al., 'Who Validates the Validators?' (2024) • Eugene Yan, evaluating LLM-evaluators",
            "lineage": "Eugene Yan • Shreya Shankar • MT-Bench (Zheng et al. 2023)",
            "tp": 46, "fp": 3, "fn": 4, "tn": 47,
            "matrix_note": "Numbers are an example calibration set; re-run yours every release.",
            "biases": [
                {"name": "Position bias", "symptom": "Prefers whichever answer is shown first in pairwise grading.", "fix": "Grade both orders and average; or switch to single-answer PASS/FAIL."},
                {"name": "Verbosity bias", "symptom": "Longer answers score higher even when they add nothing.", "fix": "Length-normalize; tell the rubric that extra words are not merit."},
                {"name": "Self-preference", "symptom": "A model rates its own outputs higher.", "fix": "Judge with a different model family than the one being judged."},
                {"name": "Likert drift", "symptom": "1-5 scores cluster at 3-4 and mean different things to different graders.", "fix": "Binary PASS/FAIL per failure mode with a quoted reason."},
                {"name": "Shallow math/logic grading", "symptom": "Misses wrong reasoning when the final answer looks fine.", "fix": "Provide a reference solution; ask the judge to verify step by step."},
            ],
            "prompt_lines": [
                "SYSTEM: You grade one criterion only.",
                "CRITERION: <one failure mode, e.g. 'fabricated tool result'>",
                "RUBRIC:",
                "  PASS = every claimed action has a matching tool call",
                "  FAIL = any claimed action lacks a tool call",
                "DO NOT reward length, tone, or politeness.",
                "",
                "INPUT:",
                "  user_message: ...",
                "  trace (tool calls + results): ...",
                "  final_answer: ...",
                "",
                "OUTPUT (JSON only):",
                "  {\"verdict\": \"PASS\" | \"FAIL\",",
                "   \"evidence\": \"<quote from the trace>\",",
                "   \"confidence\": 0.0-1.0}",
                "",
                "# Calibrate: compare to 40+ human labels;",
                "# require TPR >= 0.90 and TNR >= 0.90.",
            ],
            "routine": "Every release: re-grade 50 human-labeled traces; alert if TPR or TNR drops more than 5 points; keep 20% of labels hidden from prompt tuning.",
            "watch": "Watch TNR (does the judge catch real failures?) — a lenient judge quietly inflates every dashboard.",
            "sources": ["MT-Bench: GPT-4 agreed with humans ~80%, the same as humans with each other — but showed position, verbosity, and self-enhancement bias.", "Who Validates the Validators: humans' criteria drift as they grade; align judges iteratively, keep labeling.", "Hamel Husain: binary pass/fail beats Likert; validate judges with TPR/TNR on held-out labels."],
            "rule": "If you cannot show the confusion matrix, you do not have a judge — you have an opinion generator.",
        },
        "T26": {
            "title": "Grade the Path, Not Just the Answer: Six Trajectory Metrics on One Refund Run",
            "subtitle": "An agent can reach the right answer the wrong way (duplicate calls, skipped policy checks). Google's Agents Companion defines six ways to score the tool-call sequence.",
            "source": "Google, 'Agents Companion' whitepaper (Feb 2025): trajectory evaluation metrics",
            "lineage": "Google, Agents Companion whitepaper (Feb 2025)",
            "expected": ["search_docs", "get_order", "check_policy", "issue_refund", "send_confirmation"],
            "actual": ["search_docs", "get_order", "get_order", "check_policy", "issue_refund", "send_confirmation"],
            "actual_flags": ["ok", "ok", "extra", "ok", "ok", "ok"],
            "metrics": [
                {"name": "Exact match", "asks": "Is the actual sequence identical to the expected one?", "value": "0 (no)", "verdict": "FAIL", "color": RED},
                {"name": "In-order match", "asks": "Do the expected actions appear in the right order, extra actions allowed?", "value": "1 (yes)", "verdict": "PASS", "color": GREEN},
                {"name": "Any-order match", "asks": "Are all expected actions present, order ignored?", "value": "1 (yes)", "verdict": "PASS", "color": GREEN},
                {"name": "Precision", "asks": "What fraction of the agent's actions were expected ones?", "value": "5 / 6 = 0.83", "verdict": "WARN", "color": AMBER},
                {"name": "Recall", "asks": "What fraction of expected actions did the agent perform?", "value": "5 / 5 = 1.00", "verdict": "PASS", "color": GREEN},
                {"name": "Single-tool use", "asks": "Was the critical action (issue_refund) called?", "value": "yes", "verdict": "PASS", "color": GREEN},
            ],
            "when": [
                {"head": "Exact match", "body": "Compliance flows where the order is the policy (KYC, payments)."},
                {"head": "In-order match", "body": "Most business workflows: order matters, harmless extras are fine."},
                {"head": "Any-order match", "body": "Research or data-gathering where sequence is irrelevant."},
                {"head": "Precision & recall", "body": "Diagnosing waste (low precision) vs missed steps (low recall) — the pair you put on a dashboard."},
                {"head": "Single-tool use", "body": "Safety gates: 'did it call check_policy before issue_refund?'"},
            ],
            "final_response": "Also grade the outcome with a judge: 'Was the refund issued to the original payment method and confirmed?' — trajectory metrics catch process errors; outcome checks catch wrong results.",
            "rule": "Report in-order match + precision + recall together: a 100% in-order run with 0.5 precision is burning tokens on duplicate calls.",
        },
        "T27": {
            "title": "How MCP Actually Works: 9 Messages From 'User Asks' to 'Tool Result in Context'",
            "subtitle": "ByteByteGo & Brij Kishore Pandey control-plane walkthrough of the Model Context Protocol — JSON-RPC 2.0 handshake, schema discovery, consent gate, and tool call.",
            "source": "modelcontextprotocol.io specification • Brij Kishore Pandey, '7 Control Layers Between Intent and Action' & 'One Agent Action E2E'",
            "lineage": "Brij Kishore Pandey (7-Layer Control Plane & MCP) • ByteByteGo • MCP specification",
            "lanes": [
                {"name": "HOST APP", "sub": "Claude Desktop, an IDE, or your own agent (Google ADK / LangGraph)", "color": "#334155", "fill": "#F8FAFC", "chips": ["holds the LLM", "owns consent", "one client per server"]},
                {"name": "MCP CLIENT", "sub": "lives inside the host; speaks JSON-RPC 2.0 to one server", "color": BLUE, "fill": "#EFF6FF", "chips": ["initialize", "tools/list", "tools/call"]},
                {"name": "MCP SERVER", "sub": "GitHub, PostgreSQL, filesystem, your internal API", "color": GREEN, "fill": "#ECFDF5", "chips": ["tools", "resources", "prompts"]},
            ],
            "messages": [
                {"from": 0, "to": 0, "text": "User: 'Which open PRs touch auth?'", "sub": "host decides a tool may help", "color": "#334155"},
                {"from": 1, "to": 2, "text": "initialize", "sub": "protocol version + client capabilities", "color": BLUE},
                {"from": 2, "to": 1, "text": "initialize result → notifications/initialized", "sub": "server capabilities; handshake complete", "color": GREEN},
                {"from": 1, "to": 2, "text": "tools/list", "sub": "ask what the server can do", "color": BLUE},
                {"from": 2, "to": 1, "text": "tool schemas (name, description, JSON input schema)", "sub": "e.g. github.search_pull_requests", "color": GREEN},
                {"from": 1, "to": 0, "text": "host puts the schemas in the model's context", "sub": "model picks a tool + arguments", "color": "#334155"},
                {"from": 1, "to": 2, "text": "tools/call  {name, arguments}", "sub": "after user consent / runtime policy gate", "color": BLUE},
                {"from": 2, "to": 1, "text": "result: content blocks (text / image / resource)", "sub": "server ran the real API or query", "color": GREEN},
                {"from": 1, "to": 0, "text": "result enters context → model answers the user", "sub": "treat it as untrusted data, not instructions", "color": "#334155"},
            ],
            "notes": [
                {"head": "TRANSPORTS", "body": "stdio for local servers (the IDE launches the process); Streamable HTTP for remote servers behind auth.", "color": BLUE},
                {"head": "THREE PRIMITIVES + TWO CALLBACKS", "body": "Servers expose tools, resources, prompts. Servers can ask the client for sampling (an LLM call) or elicitation (ask the user).", "color": GREEN},
                {"head": "SECURITY IN ONE LINE", "body": "Tool results are untrusted content. Mixing a server that reads private data with one that sends messages creates Willison's lethal trifecta.", "color": RED},
            ],
            "rule": "Open source clients: MCP Python/TypeScript SDKs • Google ADK MCPToolset • LangChain MCP adapters — same nine messages everywhere.",
        },
        "T28": {
            "title": "Five Ways to Chop a Document — and the One Anthropic Measured a 67% Retrieval Win With",
            "subtitle": "Sketch-style card you can read in ten seconds. Chunking is the quiet reason most RAG agents feel dumb.",
            "source": "Anthropic, 'Introducing Contextual Retrieval' (Sep 2024) • LangChain / LlamaIndex text splitters • Jina 'late chunking'",
            "lineage": "Avi Chawla & Akshay Pachaar sketch format • Anthropic Contextual Retrieval (Sep 2024)",
            "strategies": [
                {"name": "Fixed-size", "kind": "fixed", "color": "#64748B", "how": "Cut every N tokens with a small overlap. Blind to meaning.", "best": "Logs, transcripts, anything without structure. Fast baseline.", "watch": "Splits sentences and tables mid-thought; retrieval misses context.", "start": "500 tokens • 10% overlap", "tools": "LangChain CharacterTextSplitter • LlamaIndex TokenTextSplitter"},
                {"name": "Recursive", "kind": "recursive", "color": BLUE, "how": "Try paragraphs, then sentences, then words until chunks fit.", "best": "Most prose, docs, emails. The sensible default.", "watch": "Still ignores headings and tables.", "start": "400-800 tokens • 10-15% overlap", "tools": "RecursiveCharacterTextSplitter • Vertex AI RAG Engine chunking"},
                {"name": "Structure-aware", "kind": "structure", "color": PURPLE, "how": "Split on headings, code blocks, table rows — the document's own skeleton.", "best": "Markdown, HTML, PDFs with real headings, code.", "watch": "Huge sections need a second pass.", "start": "one chunk per H2/H3 • cap 1K", "tools": "MarkdownHeaderTextSplitter • Document AI layout parser"},
                {"name": "Semantic", "kind": "semantic", "color": AMBER, "how": "Embed sentences; start a new chunk when meaning shifts.", "best": "Long narrative docs where topics drift.", "watch": "Slower; variable sizes; thresholds need tuning.", "start": "similarity threshold ~0.8 • cap 1K", "tools": "LangChain SemanticChunker • Gemini Embedding 2"},
                {"name": "Contextual retrieval", "kind": "contextual", "color": GREEN, "how": "Prepend a 50-100 token summary of where the chunk sits in the doc, then embed + BM25.", "best": "Knowledge bases where chunks lose meaning alone (contracts, specs).", "watch": "One LLM call per chunk at index time (prompt caching makes it cheap).", "start": "recursive chunks + context prefix", "tools": "Claude prompt caching • Vertex AI Search hybrid • Elasticsearch BM25"},
            ],
            "proof_head": "THE MEASURED WIN (ANTHROPIC, SEP 2024)",
            "proof": "Contextual embeddings + contextual BM25 cut top-20 retrieval failures by 49%; adding a reranker cut them by 67%. Same documents, same questions — only the chunk preparation changed.",
            "rule_head": "START HERE IF YOU HAVE NO TIME",
            "rule": "Recursive 400-800 tokens → measure recall@5 on 50 real questions → add contextual retrieval → add a reranker.",
        },
        "T29": {
            "title": "Is Your LLM Judge Really Agreeing With Humans? Compute Cohen's κ by Hand in Five Steps",
            "subtitle": "AI-by-Hand style: ten traces, two graders (human and judge), one number that corrects for luck. 80% agreement sounds great until you see κ.",
            "source": "Cohen (1960); Landis & Koch (1977) interpretation bands; Hamel Husain on judge validation",
            "lineage": "Tom Yeh, AI by Hand format",
            "items": [
                {"human": "PASS", "judge": "PASS"}, {"human": "PASS", "judge": "PASS"}, {"human": "FAIL", "judge": "FAIL"}, {"human": "PASS", "judge": "FAIL"},
                {"human": "FAIL", "judge": "PASS"}, {"human": "PASS", "judge": "PASS"}, {"human": "PASS", "judge": "PASS"}, {"human": "FAIL", "judge": "FAIL"},
                {"human": "PASS", "judge": "PASS"}, {"human": "FAIL", "judge": "FAIL"},
            ],
            "bands": [
                {"range": "κ < 0.20  slight", "action": "the judge is guessing — rewrite the rubric", "lo": -1.0, "hi": 0.20},
                {"range": "0.20 - 0.40  fair", "action": "add 5-10 worked examples to the judge prompt", "lo": 0.20, "hi": 0.40},
                {"range": "0.40 - 0.60  moderate", "action": "usable for triage; keep a human on every FAIL", "lo": 0.40, "hi": 0.60},
                {"range": "0.60 - 0.80  substantial", "action": "ship it; re-sample 50 traces per release", "lo": 0.60, "hi": 0.80},
                {"range": "0.80 - 1.00  almost perfect", "action": "automate the dashboard; audit monthly", "lo": 0.80, "hi": 1.01},
            ],
            "why_kappa": "If 60% of traces pass anyway, two graders flipping biased coins would agree ~52% of the time. κ subtracts that luck, so 80% raw agreement becomes 0.58 — honest, and still only 'moderate'.",
            "today": ["Pull 10-50 traces your team already labeled PASS/FAIL.", "Run your judge, fill the four cells a, b, c, d.", "Compute κ; if below 0.6, fix the rubric before trusting any dashboard."],
            "rule": "Raw agreement flatters every judge; κ tells you how much of it was skill.",
        },
        "T30": {
            "title": "Paper of the Day: HarnessEvolve — Learning From Reference Trajectories for Reliable Agent Self-Evolution",
            "subtitle": "One paper, one chart, three bullets, a verdict. Format borrowed from the daily paper-digest creators; numbers taken from Tables 1-3 of arXiv:2609.00829.",
            "source": "HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution (Wen Jiang et al., arXiv:2609.00829, Sep 2026)",
            "lineage": "Pascal Biese (LLM Watch) & Elvis Saravia (DAIR.AI) digest format",
            "paper_id": "arXiv:2609.00829",
            "paper_title": "HarnessEvolve: Learning from Reference Trajectories for Reliable Agent Self-Evolution",
            "paper_meta": "Wen Jiang et al. (Sep 2026) • 5 benchmarks (SearchQA, OfficeQA, SpreadsheetBench, CloudCoreNetwork-QA, Wireless-QA)",
            "tldr": "Compare failed trajectories against clean reference trajectories for step-level credit assignment, cluster failures into reusable skills, and enforce a two-tier competence gate.",
            "problem": "Teams fix agent failures by hand-editing prompts after each bug, which bloats instructions, overfits one-off cases, and silently breaks workflows that used to pass.",
            "method": "Reference-trajectory step-level credit assignment → failure clustering into generalizable skill updates → two-tier competence gating (quality/leakage check + snapshot pool regression check).",
            "result": "CloudCoreNetwork-QA jumps from 43.4% to 86.9% (+21.6 pts over GEPA 65.3%); SpreadsheetBench jumps from 44.3% to 76.4%; transfers across Hermes, OpenCode, LAMAgent, and DeepSeek Harness.",
            "why_care": "It turns 'prompt whack-a-mole' into a gated engineering loop: candidate updates that fail the two-tier gate are rejected before they can regress previously solved workflows.",
            "caveats": "Requires reference trajectories and step-level trace logging; a substantial fraction of candidate updates are rejected by the two-tier gate (which is why evaluation cost must be budgeted).",
            "chart": {"caption": "Reported accuracy (%) from Tables 1 & 2 of arXiv:2609.00829 comparing Base vs. strongest baseline (GEPA/ACE/SkillOpt) vs. HarnessEvolve.", "bars": [
                {"label": "CloudCoreNetwork-QA (Qwen3.6-27B)", "value": 86.9, "display": "86.9% (Base 43.4% • GEPA 65.3%)", "color": GREEN},
                {"label": "Wireless-QA (DeepSeek-V4-Flash)", "value": 92.8, "display": "92.8% (#1 vs. ACE / GEPA / SkillOpt)", "color": BLUE},
                {"label": "SpreadsheetBench (Open-Source, Table 2)", "value": 76.4, "display": "76.4% (Base 44.3% • SkillOpt 74.6%)", "color": AMBER},
                {"label": "SearchQA & OfficeQA (Open-Source, Table 2)", "value": 92.9, "display": "92.9% SearchQA • 70.9% OfficeQA", "color": PURPLE},
            ]},
            "pipeline": ["capture step-level traces", "diff vs. reference trajectory", "cluster failure causes", "propose skill/harness patch", "two-tier competence gate"],
            "pipeline_note": "Cross-framework transfer (Table 3): skills evolved on OpenClaw transfer directly to Hermes, OpenCode (SpreadsheetBench 57.5% → 87.9%), LAMAgent (45.0% → 80.0%), and DeepSeek Harness (56.4% → 86.8%).",
            "verdict": "READ NOW",
            "verdict_reason": "Verdict: READ NOW if you edit system prompts or agent skills more than once a week.",
            "try_steps": ["Export your last 20 failed traces with step indexes.", "Diff one against a clean reference trajectory.", "Gate every prompt/skill edit on a golden replay suite."],
            "rule": "A paper is worth your time when it changes a habit; this one replaces manual prompt edits with a two-tier regression-gated loop.",
        },
        "T31": {
            "title": "I Built an Agent Loop Guard in 26 Lines — Here Is the Code, the Run, and the Receipt",
            "subtitle": "Standard library only. Watch it block the third identical call, pivot, and stop on a deterministic 'done' — for $0.03.",
            "source": "IDEA-01 loop circuit breaker • equivalents: ADK RunConfig, LangGraph recursion_limit, CrewAI max_iter, OpenHands max_iterations",
            "lineage": "Shubham Saboo (awesome-llm-apps) & Nir Diamant demo-repo format",
            "file_name": "loop_guard.py",
            "code_lines": DEMO_CODE_T31,
            "output_lines": DEMO_OUTPUT_T31,
            "proves": [
                "The same failing tool call is allowed twice, then blocked — no 48-retry nights.",
                "A hard cost ceiling ($0.25) and step ceiling (15) sit outside the model; the model cannot talk its way past them.",
                "'Done' is a deterministic verify step returning ok, not the model saying 'done'.",
                "Every line of the run is a receipt you can paste into a postmortem.",
            ],
            "swap_note": "Swap-ins: ADK BeforeToolCallback + RunConfig • LangGraph pre_model_hook + recursion_limit • Redis ZADD for the sliding window.",
            "run_command": "git clone <repo> && cd generated-repos/gcp-adk-loop-circuit-breaker && python3 -m unittest discover -s tests -v",
            "rule": "If a demo cannot be re-run from a clean machine in under a minute, it is a screenshot, not a proof.",
        },
        "T32": {
            "title": "The Chart That Started 'Agentic Workflows': GPT-3.5 in a Loop Beat GPT-4 Zero-Shot (95.1% vs 67.0%)",
            "subtitle": "Andrew Ng's four design patterns — two robust, two emerging — and how to get the same leap on your own task this week.",
            "source": "Andrew Ng, 'What's next for AI agentic workflows', Sequoia AI Ascent (Mar 2024); HumanEval figures as presented in the talk",
            "lineage": "Andrew Ng, Sequoia AI Ascent (Mar 2024)",
            "bars": [
                {"label": "GPT-3.5 zero-shot", "value": 48.1, "color": "#94A3B8"},
                {"label": "GPT-4 zero-shot", "value": 67.0, "color": BLUE},
                {"label": "GPT-3.5 + agentic workflow", "value": 95.1, "color": GREEN},
            ],
            "chart_note": "HumanEval (coding) as reported in the talk; the loop = reflection + tool use + planning around the same weaker model.",
            "patterns": [
                {"name": "Reflection", "maturity": "ROBUST", "kind": "evaluator", "color": TEAL, "one_liner": "Ask the model to critique its own output, then revise. Cheap, reliable, works everywhere.", "try": "Try: 'Check this for bugs; then fix them.'"},
                {"name": "Tool use", "maturity": "ROBUST", "kind": "tools", "color": BLUE, "one_liner": "Let the model call search, code execution, calendars — it stops guessing facts and arithmetic.", "try": "Try: give it one tool and a verifier."},
                {"name": "Planning", "maturity": "EMERGING", "kind": "planning", "color": AMBER, "one_liner": "The model decomposes a goal into steps and sequences tools (HuggingGPT-style). Impressive, sometimes brittle.", "try": "Try: plan first, then execute step by step."},
                {"name": "Multi-agent collaboration", "maturity": "EMERGING", "kind": "multi", "color": PURPLE, "one_liner": "Role-play agents (coder, reviewer, tester) hand work to each other. Works best with typed handoffs.", "try": "Try: one writer, one critic, shared blackboard."},
            ],
            "quotes": ["Agentic workflows will drive massive AI progress this year — possibly more than the next generation of foundation models.", "Be patient: a slower agentic loop that returns a better answer in minutes beats an instant wrong answer.", "Fast token generation matters more than you think — agents read their own outputs many times."],
            "week": ["Pick one task with a checkable result (tests, a schema, a number).", "Add reflection: generate → critique → revise once.", "Add one tool that removes guessing (search or code execution).", "Measure pass rate on 30 examples before and after; keep what moved the number."],
            "rule": "Ng's point in one line: the loop around the model is where the next 2x lives — and it is available to you today.",
        },
        "T33": {
            "title": "Where Agents Work Today — a Jagged Frontier Map You Can Redraw Every Month",
            "subtitle": "Ethan Mollick's framing from the Harvard/BCG field experiment: AI capability is not a smooth wall; it is jagged. Tasks that look similar sit on opposite sides.",
            "source": "Dell'Acqua et al., 'Navigating the Jagged Technological Frontier' (HBS Working Paper 24-013, 2023) • Ethan Mollick, 'Centaurs and Cyborgs'",
            "lineage": "Ethan Mollick, jagged frontier (Dell'Acqua et al. 2023)",
            "frontier": [[300, 300], [470, 250], [620, 300], [760, 270], [860, 380], [800, 500], [880, 620], [760, 760], [600, 700], [470, 790], [330, 700], [220, 580], [260, 420]],
            "inside": [
                {"x": 400, "y": 360, "label": "Summarize a 20-page contract"},
                {"x": 560, "y": 330, "label": "Write unit tests for existing functions"},
                {"x": 700, "y": 400, "label": "Triage support tickets by category"},
                {"x": 380, "y": 560, "label": "Draft SQL from a described schema"},
                {"x": 640, "y": 580, "label": "Refactor when tests exist"},
                {"x": 500, "y": 680, "label": "Turn meeting notes into action items"},
            ],
            "outside": [
                {"x": 150, "y": 300, "label": "Multi-step arithmetic without tools"},
                {"x": 850, "y": 220, "label": "Facts newer than its context"},
                {"x": 815, "y": 516, "label": "Clicking through ambiguous web UIs"},
                {"x": 160, "y": 700, "label": "Judging its own code with no tests"},
                {"x": 760, "y": 808, "label": "Week-long tasks without checkpoints"},
            ],
            "map_note": "Task placement is an engineering judgment for coding/support agents in 2026 — redraw it with your own 20-task sample.",
            "stats": [
                {"value": "+12.2%", "label": "more tasks completed by consultants using GPT-4 inside the frontier", "color": GREEN},
                {"value": "25.1%", "label": "faster completion inside the frontier", "color": GREEN},
                {"value": "+40%", "label": "higher quality (expert-rated) inside the frontier", "color": GREEN},
                {"value": "−19 pts", "label": "less likely to produce correct solutions on the task outside the frontier", "color": RED},
            ],
            "how": ["Pick 20 real tasks your team gives the agent; run each 3 times.", "Mark reliably-right (inside), reliably-wrong (far outside), and flaky (the edge).", "Automate inside tasks fully; keep humans on the edge; do not deploy far-outside tasks.", "Repeat monthly — model upgrades move the edge, but never uniformly."],
            "edge_note": "Model releases, better tools (code execution, retrieval), and tighter harnesses (tests, checkpoints) each push specific bumps of the frontier outward — which is why a task that failed in March can pass in June while its neighbor still fails.",
            "rule": "Never assume a task is inside the frontier because a similar one is — check it.",
        },
        "T34": {
            "title": "The Lethal Trifecta: If Your Agent Has All Three, Someone Can Make It Leak",
            "subtitle": "Simon Willison's five-second security test. Private data + untrusted content + a way to send things out = exfiltration waiting for the right PDF.",
            "source": "Simon Willison, 'The lethal trifecta for AI agents' (Jun 2025) • Google Cloud Model Armor • OPA tool policies",
            "lineage": "Simon Willison, The lethal trifecta for AI agents (Jun 2025)",
            "circles": [
                {"name": "ACCESS TO PRIVATE DATA", "examples": "inbox, CRM, database, source code, files"},
                {"name": "EXPOSURE TO UNTRUSTED CONTENT", "examples": "web pages, PDFs, emails, tickets, tool results"},
                {"name": "ABILITY TO COMMUNICATE OUT", "examples": "send email, POST webhook, open URL, write issue"},
            ],
            "setups": [
                {"id": "1", "name": "Inbox assistant that reads and sends mail", "legs": "ALL THREE", "why": "A crafted email can instruct it to forward your threads.", "x": 490, "y": 514, "color": RED},
                {"id": "2", "name": "Browser agent using your logged-in sessions", "legs": "ALL THREE", "why": "Any page it visits can steer it; it can act as you.", "x": 530, "y": 514, "color": RED},
                {"id": "3", "name": "Coding agent in a sandbox with no network", "legs": "DATA + UNTRUSTED", "why": "Repo + issues are untrusted, but nothing can leave the box.", "x": 510, "y": 380, "color": AMBER},
                {"id": "4", "name": "Public web researcher, no private data", "legs": "UNTRUSTED + OUT", "why": "Can be hijacked, but has nothing of yours to leak.", "x": 610, "y": 560, "color": AMBER},
                {"id": "5", "name": "Internal SQL analyst, no web, no sending", "legs": "DATA ONLY", "why": "Reads sensitive data; no untrusted input, no exit.", "x": 330, "y": 400, "color": GREEN},
                {"id": "6", "name": "Doc summarizer with write tools unmounted", "legs": "DATA + UNTRUSTED", "why": "Capability downgrade removed the third leg at runtime.", "x": 470, "y": 350, "color": GREEN},
            ],
            "fixes": [
                {"head": "Remove 'communicate out' while reading untrusted content", "body": "Taint the session on ingress; unmount send_email / webhook / URL tools (ADK taint guard, LangGraph state flag, OPA policy)."},
                {"head": "Remove 'private data' from the reading agent", "body": "Split roles: one agent reads the web with no data access, another with data access never sees raw web content."},
                {"head": "Make 'communicate out' require a human", "body": "Any outbound action after untrusted input needs a signed approval (Cloud IAP JWT, Keycloak) — the model cannot forge it."},
            ],
            "venn_note": "Dots are placed by which legs each setup has; the red core is the only region where a prompt injection becomes a data breach.",
            "rule": "Scanners (Model Armor, Llama Guard) lower the odds; removing a leg removes the outcome.",
        },
        "T35": {
            "title": "How Anthropic's Research Agent Beat a Single Agent by 90% — and Spent 15x the Tokens Doing It",
            "subtitle": "A lead agent plans and spawns parallel subagents, each with its own context window; a citation agent finishes. Here is the shape, the numbers, and when it is worth it.",
            "source": "Anthropic Engineering, 'How we built our multi-agent research system' (Jun 13 2025)",
            "lineage": "Anthropic, How we built our multi-agent research system (Jun 2025)",
            "lead": "Reads the question, writes a plan to memory, decides how many subagents and what each searches, then synthesizes.",
            "subagents": [
                {"badge": "SUBAGENT 1 • SONNET-CLASS", "task": "Search angle A (e.g. market size); own context; returns a condensed digest.", "budget": "budget: 3-10 tool calls", "color": BLUE},
                {"badge": "SUBAGENT 2", "task": "Search angle B (competitors); runs in parallel with 1.", "budget": "budget: 10-15 calls for comparisons", "color": SKY},
                {"badge": "SUBAGENT 3", "task": "Search angle C (regulation); parallel tool calls inside the subagent too.", "budget": "parallel tool calls: up to 90% faster", "color": PURPLE},
                {"badge": "SUBAGENT N (10+ FOR COMPLEX)", "task": "Spawned only when the lead judges the query complex enough.", "budget": "scaled to complexity", "color": AMBER},
            ],
            "synthesis": "Lead merges digests, resolves conflicts",
            "citations": "Attributes every claim to a source",
            "scaling": ["Simple fact-finding: 1 agent, 3-10 tool calls.", "Direct comparisons: 2-4 subagents, 10-15 calls each.", "Complex research: 10+ subagents with clearly divided responsibilities."],
            "numbers": [
                {"value": "+90.2%", "label": "over single-agent Claude Opus 4 on Anthropic's internal research eval (lead Opus 4 + Sonnet 4 subagents)", "tag": "reported", "color": GREEN},
                {"value": "80%", "label": "of performance variance on BrowseComp explained by token usage alone", "tag": "reported", "color": BLUE},
                {"value": "~15x", "label": "tokens vs a chat interaction (single agents use ~4x)", "tag": "reported", "color": AMBER},
                {"value": "up to 90%", "label": "research time cut by parallel tool calls + parallel subagents on complex queries", "tag": "reported", "color": PURPLE},
            ],
            "use_when": ["The task is breadth-first and parallelizable (survey many sources, compare many options).", "The answer is worth far more than the tokens (due diligence, research, incident investigation).", "Subagents can return condensed digests — the lead never needs their raw context."],
            "dont_when": ["Steps depend on each other in sequence (most coding tasks) — a single agent with good tools wins.", "You cannot afford 15x tokens or the added latency and debugging surface."],
            "rule": "Open-source twins: LangGraph Send() fan-out or ADK ParallelAgent for subagents; Firestore / PostgreSQL for the lead's plan memory.",
        },
        "T36": {
            "title": "Where the $0.68 per Agent Task Went — and the Four Levers That Took It to $0.06",
            "subtitle": "A cost waterfall built from OpenTelemetry spans. Reference-harness decomposition of the measured before/after from IDEA-09; your split will differ, the levers will not.",
            "source": "IDEA-09 reference harness • vendor pricing: Anthropic prompt caching (cache reads ≈10% of input price), Vertex AI context caching discounts",
            "lineage": "Chip Huyen-style practical AI economics",
            "chart_title": "COST PER COMPLETED TASK — BEFORE (LEFT), LEVERS (MIDDLE), AFTER (RIGHT)",
            "chart_note": "Bars are USD per task; levers are applied in order, so each saving is measured after the previous one.",
            "steps": [
                {"kind": "add", "label": "Input tokens (every turn re-reads 20K)", "value": 0.21, "color": "#94A3B8"},
                {"kind": "add", "label": "Output tokens", "value": 0.14, "color": "#94A3B8"},
                {"kind": "add", "label": "Tool / API calls", "value": 0.06, "color": "#94A3B8"},
                {"kind": "add", "label": "Retries & loops", "value": 0.19, "color": RED},
                {"kind": "add", "label": "Judge / eval calls", "value": 0.08, "color": "#94A3B8"},
                {"kind": "total", "label": "BEFORE", "value": 0.0, "color": NAVY},
                {"kind": "sub", "label": "Prompt / context caching", "value": -0.12, "color": GREEN},
                {"kind": "sub", "label": "Flash / Gemma routing", "value": -0.30, "color": GREEN},
                {"kind": "sub", "label": "Loop guard (no retry storms)", "value": -0.17, "color": GREEN},
                {"kind": "sub", "label": "Top-3 tool schemas", "value": -0.03, "color": GREEN},
                {"kind": "total", "label": "AFTER", "value": 0.0, "color": GREEN},
            ],
            "levers": [
                {"name": "1. Cache the prefix", "saves": "−$0.12", "how": "System prompt, rules, and tool schemas are identical every turn — serve them from cache instead of re-billing them.", "stack": "Vertex context caching ⇄ vLLM / SGLang prefix cache", "color": BLUE},
                {"name": "2. Route by difficulty", "saves": "−$0.30", "how": "Send triage and extraction to a small model; reserve the frontier model for complexity > 0.75.", "stack": "ADK model router ⇄ LiteLLM router (Gemma 3 / Llama)", "color": PURPLE},
                {"name": "3. Stop paying for loops", "saves": "−$0.17", "how": "Block the third identical call; hard step and dollar ceilings outside the model.", "stack": "ADK RunConfig ⇄ LangGraph recursion_limit + Redis", "color": RED},
                {"name": "4. Mount only Top-3 tools", "saves": "−$0.03", "how": "85 schemas cost 35K tokens per turn; three cost 2.4K. Index the rest and load on demand.", "stack": "AlloyDB pgvector ⇄ Qdrant + MCP registry", "color": AMBER},
            ],
            "how_to": "Tag every span with task_id, model, input/output tokens, cached tokens, tool name, retry flag, and judge flag → sum by category in BigQuery or ClickHouse → plot the waterfall → apply one lever per week and keep the chart updated.",
            "rule": "Cost per completed task — not per token — is the only unit that survives a budget review.",
        },
        "T37": {
            "title": "Postmortem & Kill-Switch: How One 429 Became an $84 Night — and the 5 Controls That Stop It",
            "subtitle": "Google SRE postmortem + Brij Kishore Pandey's 'How Do We Turn It Off?' lifecycle (Register → Own → Measure → Review → Retire; 81% of CIOs lack agent oversight).",
            "source": "Brij Kishore Pandey, 'How Do We Turn It Off?' (Oct 2026; Dataiku/Harris Poll 685 CIOs) • Google SRE Book • IDEA-01 & IDEA-06",
            "lineage": "Brij Kishore Pandey ('How Do We Turn It Off?' 5-Stage Lifecycle & Kill-Switch) • Google SRE postmortem",
            "events": [
                {"time": "T+0:00", "head": "Vendor API starts returning 429 (rate limited)", "body": "The agent's create_ticket call fails with a generic error string; nothing in the harness distinguishes 'retry later' from 'try something else'.", "impact": "$0.00", "color": AMBER},
                {"time": "T+0:04", "head": "Agent retries the identical call", "body": "Same tool, same arguments. The model reads the error, concludes 'try again', and does — the context barely changed.", "impact": "$0.02", "color": AMBER, "control": {"name": "Loop circuit breaker", "how": "sha256(tool+args) seen twice in 5 turns → block the 3rd call, inject a strategy-shift directive (ask for a different approach or escalate).", "saves": "saves $83.9"}},
                {"time": "T+2:10", "head": "48th identical retry; context full of error strings", "body": "Each turn re-reads the growing history (~20K tokens); cost per turn climbs; no step ceiling exists.", "impact": "$9.40", "color": RED, "control": {"name": "Step ceiling (max_steps=15)", "how": "ADK RunConfig / LangGraph recursion_limit / OpenHands max_iterations end the run with a clean checkpoint at step 15.", "saves": "saves $74"}},
                {"time": "T+41:00", "head": "Billing alert fires at $84", "body": "The only control that worked was a daily budget alert — 41 minutes late.", "impact": "$84.00", "color": RED, "control": {"name": "Cost ceiling + Runtime Kill-Switch", "how": "Brij Pandey's 10-Field Agent Record requires a registered kill_switch_endpoint & named human owner before deploy; caps spend at $0.25.", "saves": "caps at $0.25"}},
                {"time": "T+45:00", "head": "On-call kills the job", "body": "No checkpoint exists; the whole task state lived in RAM.", "impact": "task lost", "color": RED, "control": {"name": "Durable step checkpoints", "how": "Firestore / PostgresSaver snapshot after every tool turn; resume at the last good step in ~40 ms instead of restarting.", "saves": "0 rework"}},
                {"time": "T+52:00", "head": "Duplicate ticket discovered", "body": "The 1st call had actually succeeded upstream before the 429 — the retries created a second ticket under the user's name.", "impact": "customer-visible", "color": RED, "control": {"name": "Idempotency key on every write", "how": "sha256(workflow+step+tool+args) ledger (Firestore / Redis SETNX); a repeated write returns the cached receipt instead of acting twice.", "saves": "0 duplicates"}},
                {"time": "T+1 day", "head": "Blameless postmortem + 5-Stage Lifecycle", "body": "Enforce Register → Own → Measure → Review → Retire (Dataiku survey: 83% lack lifecycle management; 47% retired >20 shadow agents).", "impact": "5 actions", "color": GREEN},
            ],
            "actions": ["10-Field Agent Record (owner + kill-switch + policy gate) • platform • sprint", "Loop breaker + step ceiling + $0.25 cost cap in harness • platform • sprint", "Idempotency keys on writes + step checkpoints • integrations & SRE • sprint"],
        },
        "T38": {
            "title": "Tool Spec Clinic: The Same Tool, Written So an Agent Fails With It — and Written So It Succeeds",
            "subtitle": "Anthropic's tool-writing guide + Brij Kishore Pandey's 5-Layer Claude Code ADK & SKILL.md standard: descriptions and response shapes matter as much as the API.",
            "source": "Anthropic Engineering, 'Writing effective tools for agents — with agents' (Sep 2025) • Brij Kishore Pandey, 'How Claude Code Becomes a Full Engineering Team' (5-Layer ADK & SKILL.md)",
            "lineage": "Anthropic (Writing effective tools) • Brij Kishore Pandey (5-Layer Claude Code ADK & SKILL.md)",
            "bad_head": "BEFORE — what most teams ship (the agent guesses)",
            "bad_lines": [
                "{",
                "  \"name\": \"search\",",
                "  \"description\": \"Searches things.\",",
                "  \"input_schema\": {",
                "    \"type\": \"object\",",
                "    \"properties\": {",
                "      \"q\": {\"type\": \"string\"},",
                "      \"limit\": {\"type\": \"integer\"}",
                "    }",
                "  }",
                "}",
                "",
                "// response: entire JSON dump, 40 KB,",
                "// UUIDs instead of names, no paging,",
                "// error: \"Error 500\"",
            ],
            "bad_notes": ["'search' collides with three other tools — the agent picks the wrong one a third of the time.", "No guidance on when (not) to use it, no example, no defaults.", "40 KB responses flood the context window; UUIDs force extra lookups.", "'Error 500' gives the agent nothing to act on, so it retries blindly."],
            "good_head": "AFTER — written for the agent that will read it",
            "good_lines": [
                "{",
                "  \"name\": \"github.search_pull_requests\",",
                "  \"description\": \"Find open or merged PRs in ONE repo by",
                "    text, label, or author. Use for 'which PRs touch X'.",
                "    Do NOT use for issues (github.search_issues) or",
                "    commits. Example: query='auth refresh', state='open'.\",",
                "  \"input_schema\": {",
                "    \"type\": \"object\",",
                "    \"required\": [\"repo\", \"query\"],",
                "    \"properties\": {",
                "      \"repo\": {\"type\": \"string\", \"description\": \"owner/name\"},",
                "      \"query\": {\"type\": \"string\"},",
                "      \"state\": {\"enum\": [\"open\",\"merged\",\"all\"], \"default\": \"open\"},",
                "      \"page_size\": {\"type\": \"integer\", \"default\": 10, \"maximum\": 50},",
                "      \"response_format\": {\"enum\": [\"concise\",\"detailed\"], \"default\": \"concise\"}",
                "  }}}",
                "// response: title, number, author NAME, url, 1-line summary;",
                "// next_page_token when truncated;",
                "// error: \"repo not found: did you mean acme/auth-service?\"",
            ],
            "good_notes": ["Namespaced name + 'use for / do not use for' + an example — the model routes correctly.", "Enums and defaults remove invalid calls; required fields are explicit.", "Concise mode + pagination keep each result under ~1K tokens; names instead of UUIDs save a round trip.", "Errors tell the agent what to do next — the difference between a fix and a retry storm."],
            "arrows": [
                {"label": "namespace + intent", "color": PURPLE},
                {"label": "enums + defaults", "color": AMBER},
                {"label": "token-efficient response", "color": BLUE},
                {"label": "actionable errors", "color": GREEN},
            ],
            "rules": [
                {"name": "FEWER, BETTER TOOLS", "body": "Consolidate: one schedule_event beats list_users + list_events + create_event. Build for the workflow the agent needs, not a 1:1 API mirror.", "example": "schedule_event(attendees, window)", "color": "#334155"},
                {"name": "NAMESPACE", "body": "Prefix by service and resource so similar tools stop colliding: github.search_pull_requests, asana.search_tasks.", "example": "service.resource_action", "color": PURPLE},
                {"name": "RETURN MEANINGFUL CONTEXT", "body": "Names over UUIDs, summaries over dumps; offer concise vs detailed response formats.", "example": "response_format: concise", "color": BLUE},
                {"name": "TOKEN EFFICIENCY", "body": "Paginate, filter, truncate with a next_page_token; make errors say what to do instead of a status code.", "example": "page_size <= 50, next_page_token", "color": AMBER},
                {"name": "PROMPT-ENGINEER & EVAL", "body": "Write descriptions like SKILL.md onboarding; test on real tasks; let the agent propose rewrites from failed traces.", "example": "eval: 30 real tasks, before/after", "color": GREEN},
            ],
            "rule": "Anthropic let Claude rewrite its own tool descriptions from failed transcripts — and accuracy went up. Pair with SKILL.md progressive disclosure.",
        },
        "T39": {
            "title": "One Request, Four Memories: What an Agent Must Remember to Book 'the Same Hotel as Last Time'",
            "subtitle": "The CoALA memory taxonomy (working, episodic, semantic, procedural) made concrete — with the store, the freshness rule, and the failure you get when each one is missing.",
            "source": "Sumers et al., 'Cognitive Architectures for Language Agents' (CoALA, 2023) • Lilian Weng, 'LLM Powered Autonomous Agents' (2023) • IDEA-07 evidence receipts",
            "lineage": "CoALA (Sumers et al. 2023) • Lilian Weng (2023) • Aishwarya Naresh Reganti memory infographics",
            "request": "\"Book the same hotel as last time in Chicago, under $200, and don't forget my usual room.\"",
            "action": "Books the Hyatt king room at $189 after checking the cancellation policy, cites the Oct trip.",
            "memories": [
                {"name": "Working", "color": BLUE, "touch": "Holds this turn's goal, budget, city", "analogy": "the whiteboard for this task", "stores": "Current goal, constraints, partial results, scratch notes for the active task.", "example": "goal=book_hotel city=Chicago max_usd=200", "where": "The context window itself (+ compaction) • ADK session state • LangGraph graph state", "fresh": "Dies with the task; compact above ~60% of the window.", "fail": "Agent forgets the $200 limit by turn 12 (context rot)."},
                {"name": "Episodic", "color": PURPLE, "touch": "Recalls the October Chicago trip", "analogy": "the diary of past events", "stores": "What happened before: past bookings, past tool results, past user decisions — with timestamps.", "example": "2025-10-14 booked Hyatt Chicago, king, $179", "where": "Firestore / PostgreSQL event log • Mem0 or Letta episodic store", "fresh": "Keep forever; rank by recency; never rewrite history.", "fail": "'Same as last time' has nothing to resolve against."},
                {"name": "Semantic", "color": GREEN, "touch": "Knows user prefers king beds", "analogy": "facts the agent believes", "stores": "Stable facts about the user and the world: preferences, entities, policies.", "example": "user.prefers_room = king; Hyatt cancel policy = 24h", "where": "AlloyDB / PostgreSQL + pgvector • Qdrant • Vertex AI Vector Search", "fresh": "Every fact carries source + timestamp (+ git SHA for code facts); flag STALE on mismatch.", "fail": "Books a double; or trusts a policy that changed last month."},
                {"name": "Procedural", "color": AMBER, "touch": "Knows how to call the booking API safely", "analogy": "skills and habits", "stores": "How to do things: tool-use recipes, learned rules ('always check cancellation first'), SKILL.md files.", "example": "skills/book_hotel/SKILL.md v7", "where": "Repo files (SKILL.md, AGENTS.md) • tool registry • prompts under version control", "fresh": "Change only through a reviewed PR + golden replay gate.", "fail": "Re-learns the API every session; repeats the same mistake twice."},
            ],
            "design_rule": "Store receipts, not vibes: every long-term memory carries where it came from and when — so the agent can tell 'I know this' from 'I knew this once'.",
            "rule": "Working memory is free; the other three are design decisions. Decide them before the first user does.",
        },
        "T40": {
            "title": "One Metric, Eight Releases, Four Flags: How p95 Latency Went From 42 s to 1.9 s",
            "subtitle": "Build-in-public format: one chart, every architecture change annotated where it landed. Reference-harness path from IDEA-09 (measured endpoints; weekly points interpolated).",
            "source": "IDEA-09 reference harness (p95 agent turn latency) • Cloud Trace / Langfuse spans",
            "lineage": "Nate B. Jones 'one chart' • Santiago Valdarrama build-in-public",
            "unit": " s",
            "points": [
                {"x": "wk 1", "value": 42.0}, {"x": "wk 2", "value": 40.5}, {"x": "wk 3", "value": 22.0}, {"x": "wk 4", "value": 20.1},
                {"x": "wk 5", "value": 9.8}, {"x": "wk 6", "value": 4.2}, {"x": "wk 7", "value": 2.6}, {"x": "wk 8", "value": 1.9},
            ],
            "events": [
                {"point_index": 2, "flag": "KV / prefix cache", "name": "Prefix caching on", "delta": "−18.5 s", "what": "System prompt, rules, and tool schemas served from Vertex context cache (vLLM prefix cache in the OSS twin); prefill latency collapsed.", "stack": "Vertex AI context caching ⇄ vLLM / SGLang", "color": BLUE},
                {"point_index": 4, "flag": "Flash routing", "name": "Route easy turns to a small model", "delta": "−10.3 s", "what": "Gemini 3.8 Flash (or Gemma 3 via LiteLLM) handles triage and extraction; the frontier model only sees complexity > 0.75.", "stack": "ADK router ⇄ LiteLLM", "color": PURPLE},
                {"point_index": 5, "flag": "Parallel reads", "name": "Fan out independent read tools", "delta": "−5.6 s", "what": "Four read-only tools that ran one after another now run in one wave (ParallelAgent / LangGraph Send()).", "stack": "ADK ParallelAgent ⇄ LangGraph Send()", "color": AMBER},
                {"point_index": 7, "flag": "Top-3 tools", "name": "Mount only the three relevant tools", "delta": "−0.7 s", "what": "35K tokens of tool schemas per turn became 2.4K; shorter prompts, faster first token, fewer wrong tool picks.", "stack": "AlloyDB pgvector ⇄ Qdrant + MCP registry", "color": GREEN},
            ],
            "chart_note": "p95 latency per agent turn, seconds (lower is better). Weekly points between measured endpoints are interpolated for illustration.",
            "how_to": "Pick one metric your users feel. Log it per release. Every time you change the architecture, drop a flag on the chart with the delta. Share the chart weekly — the flags become your changelog.",
            "why_format": "Readers trust cause-and-effect they can see. A single annotated line answers 'what did you change and did it work?' faster than any architecture diagram.",
        },
    }


register_templates(META, RENDERERS_V2, demo_specs_v2)
