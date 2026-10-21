"""Dynamic Moving-Arrow 2D Diagram Engine for Agentic AI Daily Problem & Solution Flows.

Generates:
1. Self-contained 60fps Animated Vector SVGs (`dynamic-solution-flow.svg`) with:
   - Moving dashed arrow streams (CSS `@keyframes arrowStream`)
   - Traveling glowing signal packets & chevrons (`<animateMotion>`) along every arrow
   - Sequential step-card pulse highlights
2. Multi-frame looping Animated GIFs (`dynamic-solution-flow.gif`) via deterministic
   phase-frame rendering + ffmpeg palettegen/paletteuse so moving arrows animate
   natively inside LinkedIn posts, GitHub READMEs, and Markdown artifacts.
"""

from __future__ import annotations

import html
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional


CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG_BIN = "/opt/homebrew/bin/ffmpeg"


def _esc(val: Any) -> str:
    return html.escape(str(val or ""), quote=True)


def _wrap(text: str, width: int, max_lines: int = 3) -> List[str]:
    clean = str(text or "").strip()
    if not clean:
        return [""]
    lines = textwrap.wrap(clean, width=width)
    if len(lines) > max_lines:
        for extra in range(4, 36, 4):
            retry = textwrap.wrap(clean, width=width + extra)
            if len(retry) <= max_lines:
                return retry
        return lines[:max_lines]
    return lines


def _concise_gcp_primitive(raw: str) -> str:
    """Return a clean, whole-word Google Cloud primitive name <= 32 chars (zero mid-word slicing)."""
    base = raw.split("(")[0].strip()
    if "Gemini 4 Argon" in raw:
        return "Vertex AI Gemini 4 Argon"
    if "Gemini 3.8 Flash" in raw:
        return "Vertex AI Gemini 3.8 Flash"
    if len(base) <= 32:
        return base
    words = base.split()
    out: List[str] = []
    for w in words:
        cand = " ".join(out + [w])
        if len(cand) > 32:
            break
        out.append(w)
    return " ".join(out) or base[:32]


def _normalize_idea_spec(post_or_idea: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure both TOMORROW_TOP10_IDEAS and POSTS_CATALOG items work seamlessly."""
    if "dynamic_steps" in post_or_idea and "problem_flow_nodes" in post_or_idea:
        return post_or_idea

    steps = post_or_idea.get("core_steps", [])
    colors = ["#2563EB", "#7C3AED", "#D97706", "#059669"]
    dyn_steps = []
    for idx, s in enumerate(steps[:4]):
        dyn_steps.append(
            {
                "step": f"0{idx + 1}",
                "badge": f"STEP {idx + 1} • STAGE 0{idx + 1}",
                "title": s["title"],
                "how_it_works": s["desc"],
                "gcp_primitive": _concise_gcp_primitive(post_or_idea["gcp_stack"][idx % len(post_or_idea["gcp_stack"])]),
                "arrow_label": f"Step {idx + 1} -> {idx + 2}",
                "color": colors[idx % 4],
            }
        )
    metrics_items = list(post_or_idea.get("metrics", {}).items())
    m1 = f"{metrics_items[0][0]}: {metrics_items[0][1]}" if len(metrics_items) > 0 else "100% Verified"
    m2 = f"{metrics_items[1][0]}: {metrics_items[1][1]}" if len(metrics_items) > 1 else "Zero Drift"
    src_short = post_or_idea["primary_source"]["title"].split("(")[0].strip()
    if len(src_short) > 68:
        src_short = src_short.split(":")[0].strip()

    return {
        "id": post_or_idea["id"],
        "est_post_time": post_or_idea.get("est_post_time", "Published Signal • Verified Google Cloud Repo"),
        "repo_slug": post_or_idea["repo_slug"],
        "post_title": post_or_idea["post_title"],
        "best_approach_title": post_or_idea["primary_source"]["title"],
        "why_it_happens_plain": post_or_idea["original_hook"],
        "primary_source": post_or_idea["primary_source"],
        "problem_flow_nodes": [
            {"label": "1. Naive Prompt-Only Agent", "sub": "No harness or deterministic gates"},
            {"label": "2. Silent Drift & Failure", "sub": "Repeats errors or drops context"},
            {"label": "3. Production Outage / Risk", "sub": "Unverified output reaches users"},
        ],
        "dynamic_steps": dyn_steps,
        "feedback_loop_label": f"Closed-Loop Verification: Stage 4 validates against {src_short}",
        "before_after": {
            "before_metric_1": "Fragile Prompt-Only Wrapper",
            "before_metric_2": "Unverified Hallucination Risk",
            "after_metric_1": m1[:38],
            "after_metric_2": m2[:38],
            "daily_takeaway": post_or_idea["primary_source"]["verified_claims"][0],
        },
    }


def _render_moving_horizontal_arrow(
    arrow_id: str,
    x1: int,
    x2: int,
    y: int,
    color: str,
    label: Optional[str] = None,
    frame_phase: Optional[float] = None,
    dur: str = "1.5s",
) -> str:
    """Render an ultra-visible glassmorphic horizontal arrow with moving dashes, chevron, and 4-layer glowing packet."""
    dash_offset = 0.0 if frame_phase is None else -frame_phase * 24.0
    path_d = f"M {x1 + 4} {y} L {x2 - 12} {y}"

    parts = [
        # Outer luminous glass aura track
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{color}" stroke-opacity="0.16" stroke-width="11" stroke-linecap="round"/>',
        # Frosted white inner channel
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.76" stroke-width="5.6" stroke-linecap="round"/>',
        # Animated moving dashed stream
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" class="moving-arrow-line" stroke="{color}" stroke-width="3.8" stroke-dasharray="12 8" stroke-dashoffset="{dash_offset:.1f}"/>',
        # Destination arrowhead
        f'<polygon points="{x2},{y} {x2 - 15},{y - 9} {x2 - 11},{y} {x2 - 15},{y + 9}" fill="{color}"/>',
    ]

    if label:
        mid_x = (x1 + x2) // 2
        pill_w = min(x2 - x1 - 8, max(72, len(label) * 6 + 14))
        px0 = mid_x - pill_w // 2
        py0 = y - 36
        parts.extend(
            [
                f'<rect x="{px0}" y="{py0}" width="{pill_w}" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.95" stroke="{color}" stroke-width="1.6"/>',
                f'<rect x="{px0 + 2}" y="{py0 + 1.5:.1f}" width="{pill_w - 4}" height="8" rx="4" fill="#FFFFFF" fill-opacity="0.45"/>',
                f'<text x="{mid_x}" y="{y - 21}" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="{color}" text-anchor="middle">{_esc(label)}</text>',
            ]
        )

    if frame_phase is None:
        parts.extend(
            [
                f'<path id="{arrow_id}_path" d="{path_d}" fill="none" stroke="none"/>',
                "<g>",
                f'  <circle r="9.5" fill="{color}" fill-opacity="0.16"/>',
                f'  <circle r="6.4" fill="{color}" fill-opacity="0.30"/>',
                f'  <circle r="4.8" fill="#FFFFFF" stroke="{color}" stroke-width="2.6"/>',
                f'  <circle r="1.9" fill="{color}"/>',
                f'  <animateMotion dur="{dur}" repeatCount="indefinite"><mpath href="#{arrow_id}_path"/></animateMotion>',
                "</g>",
            ]
        )
    else:
        px = (x1 + 6) + frame_phase * (x2 - 16 - (x1 + 6))
        parts.extend(
            [
                f'<circle cx="{px:.1f}" cy="{y}" r="9.5" fill="{color}" fill-opacity="0.16"/>',
                f'<circle cx="{px:.1f}" cy="{y}" r="6.4" fill="{color}" fill-opacity="0.32"/>',
                f'<circle cx="{px:.1f}" cy="{y}" r="5" fill="#FFFFFF" stroke="{color}" stroke-width="2.6"/>',
                f'<circle cx="{px:.1f}" cy="{y}" r="2.0" fill="{color}"/>',
            ]
        )

    return "\n".join(parts)


def generate_dynamic_solution_svg(post_or_idea: Dict[str, Any], frame_phase: Optional[float] = None) -> str:
    """Generate a 1600x980 Executive Light-Theme Glassmorphic Dynamic Diagram with Moving Arrows."""
    idea = _normalize_idea_spec(post_or_idea)
    p_nodes = idea["problem_flow_nodes"][:3]
    d_steps = idea["dynamic_steps"][:4]
    ba = idea["before_after"]

    active_step_idx = -1
    if frame_phase is not None:
        active_step_idx = int(frame_phase * 4) % 4

    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 980" width="1600" height="980">',
        "<defs>",
        '  <filter id="cardShadow" x="-3%" y="-3%" width="106%" height="110%">',
        '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.065"/>',
        "  </filter>",
        '  <linearGradient id="glassCardGrad" x1="0" y1="0" x2="0" y2="1">',
        '    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>',
        '    <stop offset="100%" stop-color="#F8FAFC" stop-opacity="0.90"/>',
        "  </linearGradient>",
        '  <linearGradient id="glassSheen" x1="0" y1="0" x2="0" y2="1">',
        '    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.72"/>',
        '    <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0"/>',
        "  </linearGradient>",
        '  <radialGradient id="meshBlue" cx="14%" cy="18%" r="48%">',
        '    <stop offset="0%" stop-color="#4285F4" stop-opacity="0.065"/>',
        '    <stop offset="100%" stop-color="#4285F4" stop-opacity="0.0"/>',
        "  </radialGradient>",
        '  <radialGradient id="meshEmerald" cx="86%" cy="20%" r="46%">',
        '    <stop offset="0%" stop-color="#10B981" stop-opacity="0.055"/>',
        '    <stop offset="100%" stop-color="#10B981" stop-opacity="0.0"/>',
        "  </radialGradient>",
        '  <radialGradient id="meshViolet" cx="50%" cy="84%" r="52%">',
        '    <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.048"/>',
        '    <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.0"/>',
        "  </radialGradient>",
        '  <pattern id="archGrid" width="24" height="24" patternUnits="userSpaceOnUse">',
        '    <circle cx="2" cy="2" r="1" fill="#94A3B8" fill-opacity="0.22"/>',
        "  </pattern>",
        "  <style>",
        "    @keyframes arrowStream {",
        "      from { stroke-dashoffset: 40; }",
        "      to   { stroke-dashoffset: 0; }",
        "    }",
        "    @keyframes returnStream {",
        "      from { stroke-dashoffset: 0; }",
        "      to   { stroke-dashoffset: 48; }",
        "    }",
        "    @keyframes pulseGlow {",
        "      0%, 100% { stroke-width: 2.4px; }",
        "      50%      { stroke-width: 4.2px; }",
        "    }",
        "    .moving-arrow-line {",
        "      animation: arrowStream 1.0s linear infinite;",
        "    }",
        "    .moving-return-line {",
        "      animation: returnStream 1.2s linear infinite;",
        "    }",
        "    .step-card-animated {",
        "      animation: pulseGlow 2.4s ease-in-out infinite;",
        "    }",
        "  </style>",
        "</defs>",
        '<!-- Root Canvas: Rule 54 Universal Light Theme (#F8FAFC) + Ambient Glassmorphic Mesh -->',
        '<rect x="0" y="0" width="1600" height="980" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshBlue)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshEmerald)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshViolet)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#archGrid)"/>',
        '<!-- Google Quad-Color Top Accent Bar -->',
        '<rect x="0" y="0" width="400" height="7" fill="#4285F4"/>',
        '<rect x="400" y="0" width="400" height="7" fill="#EA4335"/>',
        '<rect x="800" y="0" width="400" height="7" fill="#FBBC04"/>',
        '<rect x="1200" y="0" width="400" height="7" fill="#34A853"/>',
        '<!-- Top Title Banner (y=18..126) -->',
        '<rect x="36" y="18" width="1528" height="108" rx="12" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#cardShadow)"/>',
        '<rect x="37.5" y="19.5" width="1525" height="105" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
        '<rect x="38" y="20" width="1524" height="18" rx="10" fill="url(#glassSheen)"/>',
        '<rect x="56" y="32" width="334" height="24" rx="6" fill="#EFF6FF" fill-opacity="0.95" stroke="#2563EB" stroke-width="1.2"/>',
        f'<text x="223" y="48" font-family="Inter, sans-serif" font-size="10.8" font-weight="800" fill="#1D4ED8" text-anchor="middle">{_esc(idea["id"])} • {_esc(idea.get("est_post_time", "MORNING EST"))}</text>',
        '<rect x="402" y="32" width="380" height="24" rx="6" fill="#ECFDF5" fill-opacity="0.95" stroke="#059669" stroke-width="1.2"/>',
        '<text x="592" y="48" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">DAILY AGENTIC AI PAIN POINT &amp; PRODUCTION FIX</text>',
        '<rect x="1216" y="32" width="328" height="24" rx="6" fill="#0F2942"/>',
        '<text x="1380" y="48" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#38BDF8" text-anchor="middle">&gt;&gt;&gt; DYNAMIC FLOW • MOVING ARROWS</text>',
        f'<text x="56" y="84" font-family="Inter, sans-serif" font-size="{17.5 if len(idea["post_title"]) > 115 else (20 if len(idea["post_title"]) > 92 else 23.5)}" font-weight="800" fill="#0F172A">{_esc(idea["post_title"])}</text>',
        f'<text x="56" y="110" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="#475569">Best Approach: {_esc(idea["best_approach_title"])}  •  Repo: generated-repos/{_esc(idea["repo_slug"])}</text>',
    ]

    # =========================================================================
    # BAND 1: THE DAILY PROBLEM USERS FACE EVERY DAY (y=140..314)
    # =========================================================================
    svg.extend(
        [
            '<rect x="36" y="140" width="1528" height="174" rx="12" fill="#FFF5F5" fill-opacity="0.93" stroke="#FCA5A5" stroke-width="2" filter="url(#cardShadow)"/>',
            '<rect x="37.5" y="141.5" width="1525" height="171" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.82" stroke-width="1"/>',
            '<rect x="36" y="140" width="1528" height="32" rx="10" fill="#991B1B"/>',
            '<rect x="38" y="141.5" width="1524" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.18"/>',
            '<text x="58" y="161" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="#FFFFFF">1. THE DAILY PROBLEM USERS FACE EVERY DAY — WHAT GOES WRONG IN STANDARD AGENTS</text>',
        ]
    )

    for idx, pnode in enumerate(p_nodes):
        px = 56 + idx * 336
        is_last = idx == 2
        card_fill = "#FEE2E2" if is_last else "#FFFFFF"
        border_col = "#DC2626" if is_last else "#F87171"
        title_col = "#991B1B" if is_last else "#0F172A"
        sub_lines = _wrap(pnode["sub"], width=34, max_lines=2)
        svg.extend(
            [
                f'<rect x="{px}" y="188" width="272" height="106" rx="10" fill="{card_fill}" fill-opacity="0.94" stroke="{border_col}" stroke-width="2.2" filter="url(#cardShadow)"/>',
                f'<rect x="{px + 1.2:.1f}" y="189.2" width="269.6" height="103.6" rx="9" fill="none" stroke="#FFFFFF" stroke-opacity="0.82" stroke-width="1"/>',
                f'<rect x="{px}" y="188" width="272" height="24" rx="8" fill="{border_col}"/>',
                f'<rect x="{px + 2}" y="189.4" width="268" height="8" rx="4" fill="#FFFFFF" fill-opacity="0.22"/>',
                f'<text x="{px + 136}" y="204" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">{"FAILURE TRIGGER" if idx == 0 else ("FAILURE AMPLIFIER" if idx == 1 else "DAILY USER PAIN")}</text>',
                f'<text x="{px + 14}" y="236" font-family="Inter, sans-serif" font-size="13.5" font-weight="800" fill="{title_col}">{_esc(pnode["label"])}</text>',
                f'<text x="{px + 14}" y="260" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="#475569">{_esc(sub_lines[0])}</text>',
            ]
        )
        if len(sub_lines) > 1:
            svg.append(
                f'<text x="{px + 14}" y="278" font-family="Inter, sans-serif" font-size="11.5" font-weight="600" fill="#64748B">{_esc(sub_lines[1])}</text>'
            )
        if idx < 2:
            svg.append(
                _render_moving_horizontal_arrow(
                    arrow_id=f"prob_arr_{idx}",
                    x1=px + 276,
                    x2=px + 332,
                    y=241,
                    color="#DC2626",
                    label=None,
                    frame_phase=frame_phase,
                    dur="1.3s",
                )
            )

    # Plain-English Root Cause Box on the Right of Band 1
    why_lines = _wrap(idea["why_it_happens_plain"], width=58, max_lines=4)
    svg.extend(
        [
            '<rect x="1068" y="186" width="474" height="110" rx="10" fill="url(#glassCardGrad)" stroke="#DC2626" stroke-width="1.8" filter="url(#cardShadow)"/>',
            '<rect x="1069.2" y="187.2" width="471.6" height="107.6" rx="9" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="1068" y="186" width="8" height="110" rx="4" fill="#DC2626"/>',
            '<text x="1090" y="208" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#991B1B">WHY THIS HAPPENS (PLAIN-ENGLISH ROOT CAUSE)</text>',
        ]
    )
    for w_idx, wl in enumerate(why_lines):
        svg.append(
            f'<text x="1090" y="{229 + w_idx * 17.5:.1f}" font-family="Inter, sans-serif" font-size="11.8" font-weight="600" fill="#1E293B">{_esc(wl)}</text>'
        )

    # =========================================================================
    # BAND 2: THE 4-STEP ARCHITECTURAL SOLUTION WITH MOVING ARROWS (y=328..748)
    # =========================================================================
    svg.extend(
        [
            '<rect x="36" y="328" width="1528" height="420" rx="12" fill="url(#glassCardGrad)" stroke="#93C5FD" stroke-width="2.2" filter="url(#cardShadow)"/>',
            '<rect x="37.5" y="329.5" width="1525" height="417" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="36" y="328" width="1528" height="34" rx="10" fill="#0F2942"/>',
            '<rect x="38" y="329.5" width="1524" height="12" rx="6" fill="#FFFFFF" fill-opacity="0.16"/>',
            '<text x="58" y="350" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="#FFFFFF">2. THE BEST-PRACTICE ARCHITECTURAL SOLUTION — FOLLOW THE 4-STEP DYNAMIC FLOW &amp; CLOSED-LOOP GUARD</text>',
        ]
    )

    # 4 Step Cards: width=284, gap=110 (so x = 56, 450, 844, 1238; right edge of card 4 = 1522)
    for idx, st in enumerate(d_steps):
        sx = 56 + idx * 394
        scol = st["color"]
        how_lines = _wrap(st["how_it_works"], width=35, max_lines=4)
        is_active = idx == active_step_idx
        stroke_w = "4.2" if is_active else "2.4"
        anim_cls = "step-card-animated" if frame_phase is None else ""

        svg.extend(
            [
                f'<rect x="{sx}" y="380" width="284" height="244" rx="12" class="{anim_cls}" fill="url(#glassCardGrad)" stroke="{scol}" stroke-width="{stroke_w}" filter="url(#cardShadow)"/>',
                f'<rect x="{sx + 1.2:.1f}" y="381.2" width="281.6" height="241.6" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
                f'<rect x="{sx}" y="380" width="284" height="34" rx="10" fill="{scol}"/>',
                f'<rect x="{sx + 2}" y="381.5" width="280" height="12" rx="6" fill="#FFFFFF" fill-opacity="0.22"/>',
                f'<text x="{sx + 142}" y="402" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">{_esc(st["badge"])}</text>',
                f'<text x="{sx + 16}" y="442" font-family="Inter, sans-serif" font-size="15.5" font-weight="800" fill="#0F172A">{_esc(st["title"])}</text>',
                f'<line x1="{sx + 16}" y1="456" x2="{sx + 268}" y2="456" stroke="#CBD5E1" stroke-width="1.2"/>',
                f'<text x="{sx + 16}" y="476" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="{scol}">HOW IT WORKS:</text>',
            ]
        )
        for h_idx, hl in enumerate(how_lines):
            svg.append(
                f'<text x="{sx + 16}" y="{496 + h_idx * 18}" font-family="Inter, sans-serif" font-size="12" font-weight="600" fill="#1E293B">{_esc(hl)}</text>'
            )

        # Bottom Dual-Stack Pill: Google Cloud primitive + Open-Source equivalent
        from src.catalog.stack_pairings import oss_step_equivalent

        oss_label = st.get("oss_primitive") or oss_step_equivalent(idea["id"], st["step"], st["gcp_primitive"])
        svg.extend(
            [
                f'<rect x="{sx + 14}" y="{566}" width="256" height="46" rx="8" fill="#FFFFFF" fill-opacity="0.95" stroke="{scol}" stroke-width="1.6"/>',
                f'<rect x="{sx + 14}" y="{566}" width="256" height="23" rx="8" fill="{scol}" fill-opacity="0.10"/>',
                f'<text x="{sx + 24}" y="{582}" font-family="ui-monospace, monospace" font-size="9.5" font-weight="800" fill="{scol}">GOOGLE: {_esc(st["gcp_primitive"][:36])}</text>',
                f'<text x="{sx + 24}" y="{603}" font-family="ui-monospace, monospace" font-size="9.5" font-weight="800" fill="#0F172A">OSS: {_esc(oss_label[:38])}</text>',
            ]
        )

        # Render Moving Arrow in the generous 110px channel between Step idx and Step idx+1
        if idx < 3:
            svg.append(
                _render_moving_horizontal_arrow(
                    arrow_id=f"sol_arr_{idx}",
                    x1=sx + 288,
                    x2=sx + 390,
                    y=502,
                    color=scol,
                    label=st.get("arrow_label", "Next"),
                    frame_phase=frame_phase,
                    dur="1.5s",
                )
            )

    # Animated Closed-Loop Self-Healing Return Highway (y=666 unobstructed track + pill below at y=696..730)
    ret_dash_offset = 0.0 if frame_phase is None else frame_phase * 40.0
    return_path_d = "M 1380 626 L 1380 668 L 198 668 L 198 632"
    svg.extend(
        [
            f'<path d="{return_path_d}" fill="none" stroke="#059669" stroke-opacity="0.16" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{return_path_d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.74" stroke-width="5.6" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path id="closed_loop_return_path" d="{return_path_d}" class="moving-return-line" fill="none" stroke="#059669" stroke-width="3.8" stroke-dasharray="14 10" stroke-dashoffset="{ret_dash_offset:.1f}"/>',
            '<polygon points="198,626 189,641 198,637 207,641" fill="#059669"/>',
            # Left-pointing directional chevrons along the return highway at y=668
            '<polygon points="480,668 492,661 490,668 492,675" fill="#059669"/>',
            '<polygon points="790,668 802,661 800,668 802,675" fill="#059669"/>',
            '<polygon points="1100,668 1112,661 1110,668 1112,675" fill="#059669"/>',
            # Unobstructed Closed-Loop Label Pill below the return highway (y=694..730)
            '<rect x="230" y="694" width="1140" height="34" rx="17" fill="#ECFDF5" fill-opacity="0.95" stroke="#059669" stroke-width="1.8"/>',
            '<rect x="234" y="696" width="1132" height="12" rx="6" fill="#FFFFFF" fill-opacity="0.42"/>',
            f'<text x="800" y="716" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46" text-anchor="middle">CLOSED-LOOP FEEDBACK &lt;&lt;&lt; {_esc(idea["feedback_loop_label"])}</text>',
        ]
    )

    if frame_phase is None:
        svg.extend(
            [
                "<g>",
                '  <circle r="9.5" fill="#059669" fill-opacity="0.16"/>',
                '  <circle r="6.4" fill="#059669" fill-opacity="0.30"/>',
                '  <circle r="5" fill="#FFFFFF" stroke="#059669" stroke-width="2.6"/>',
                '  <circle r="2" fill="#059669"/>',
                '  <animateMotion dur="2.8s" repeatCount="indefinite"><mpath href="#closed_loop_return_path"/></animateMotion>',
                "</g>",
            ]
        )
    else:
        rx1 = 1380 - frame_phase * (1380 - 198)
        rx2 = 1380 - ((frame_phase + 0.5) % 1.0) * (1380 - 198)
        for rx_val in (rx1, rx2):
            svg.extend(
                [
                    f'<circle cx="{rx_val:.1f}" cy="668" r="9.5" fill="#059669" fill-opacity="0.16"/>',
                    f'<circle cx="{rx_val:.1f}" cy="668" r="6.4" fill="#059669" fill-opacity="0.32"/>',
                    f'<circle cx="{rx_val:.1f}" cy="668" r="5" fill="#FFFFFF" stroke="#059669" stroke-width="2.6"/>',
                    f'<circle cx="{rx_val:.1f}" cy="668" r="2" fill="#059669"/>',
                ]
            )

    # =========================================================================
    # BAND 3: BEFORE vs. AFTER PRODUCTION IMPACT & GOLDEN RULE (y=764..960)
    # =========================================================================
    # Card A: BEFORE (x=36..486, width=450)
    svg.extend(
        [
            '<rect x="36" y="764" width="450" height="196" rx="12" fill="url(#glassCardGrad)" stroke="#FCA5A5" stroke-width="2" filter="url(#cardShadow)"/>',
            '<rect x="37.5" y="765.5" width="447" height="193" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="36" y="764" width="450" height="32" rx="10" fill="#991B1B"/>',
            '<rect x="38" y="765.5" width="446" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.20"/>',
            '<text x="56" y="785" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">[X] BEFORE (STANDARD UNPROTECTED AGENT)</text>',
            '<rect x="54" y="812" width="414" height="56" rx="8" fill="#FEF2F2" fill-opacity="0.94" stroke="#FECACA" stroke-width="1.5"/>',
            f'<text x="72" y="846" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="#991B1B">✘ {_esc(ba["before_metric_1"])}</text>',
            '<rect x="54" y="882" width="414" height="56" rx="8" fill="#FEF2F2" fill-opacity="0.94" stroke="#FECACA" stroke-width="1.5"/>',
            f'<text x="72" y="916" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="#991B1B">✘ {_esc(ba["before_metric_2"])}</text>',
        ]
    )

    # Moving Transformation Arrow in the 92px channel between BEFORE (x=486) and AFTER (x=578)
    svg.append(
        _render_moving_horizontal_arrow(
            arrow_id="ba_transform_arr",
            x1=490,
            x2=574,
            y=868,
            color="#059669",
            label="UPGRADE",
            frame_phase=frame_phase,
            dur="1.2s",
        )
    )

    # Card B: AFTER (x=578..1028, width=450)
    svg.extend(
        [
            '<rect x="578" y="764" width="450" height="196" rx="12" fill="url(#glassCardGrad)" stroke="#6EE7B7" stroke-width="2.2" filter="url(#cardShadow)"/>',
            '<rect x="579.5" y="765.5" width="447" height="193" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="578" y="764" width="450" height="32" rx="10" fill="#065F46"/>',
            '<rect x="580" y="765.5" width="446" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.20"/>',
            '<text x="598" y="785" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">[✓] AFTER (ENGINEERED HARNESS: GOOGLE CLOUD + OPEN SOURCE)</text>',
            '<rect x="596" y="812" width="414" height="56" rx="8" fill="#ECFDF5" fill-opacity="0.94" stroke="#A7F3D0" stroke-width="1.8"/>',
            f'<text x="614" y="846" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="#065F46">✓ {_esc(ba["after_metric_1"])}</text>',
            '<rect x="596" y="882" width="414" height="56" rx="8" fill="#ECFDF5" fill-opacity="0.94" stroke="#A7F3D0" stroke-width="1.8"/>',
            f'<text x="614" y="916" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="#065F46">✓ {_esc(ba["after_metric_2"])}</text>',
        ]
    )

    # Card C: GOLDEN DAILY RULE TO APPLY TODAY (x=1052..1564, width=512)
    takeaway_lines = _wrap(ba["daily_takeaway"], width=56, max_lines=3)
    src_lines = _wrap("Source: " + idea["primary_source"]["title"], width=64, max_lines=2)
    svg.extend(
        [
            '<rect x="1052" y="764" width="512" height="196" rx="12" fill="#0F2942" stroke="#1E3A8A" stroke-width="2" filter="url(#cardShadow)"/>',
            '<rect x="1054" y="765.5" width="508" height="14" rx="8" fill="#FFFFFF" fill-opacity="0.10"/>',
            '<rect x="1072" y="780" width="248" height="24" rx="6" fill="#1D4ED8"/>',
            '<text x="1196" y="796" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GOLDEN RULE TO APPLY TODAY</text>',
        ]
    )
    for t_idx, tl in enumerate(takeaway_lines):
        svg.append(
            f'<text x="1072" y="{828 + t_idx * 21}" font-family="Inter, sans-serif" font-size="13" font-weight="700" fill="#F8FAFC">{_esc(tl)}</text>'
        )
    for s_idx, sl in enumerate(src_lines):
        svg.append(
            f'<text x="1072" y="{900 + s_idx * 16}" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#93C5FD">{_esc(sl)}</text>'
        )
    svg.extend(
        [
            '<text x="1072" y="944" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#86EFAC">Curated by Nitin Aggarwal  •  Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    from src.visuals.template_gallery import flatten_svg_zero_origin

    return flatten_svg_zero_origin("\n".join(svg))


def render_animated_gif_for_idea(
    post_or_idea: Dict[str, Any],
    output_gif_path: Path,
    output_png_path: Optional[Path] = None,
    num_frames: int = 6,
) -> bool:
    """Compile a multi-frame looping Animated GIF with moving arrows using Headless Chrome + ffmpeg."""
    chrome = Path(CHROME_BIN)
    ffmpeg = Path(FFMPEG_BIN)
    if not chrome.exists() or not ffmpeg.exists():
        return False

    output_gif_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dyn_arrow_frames_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        for f_idx in range(num_frames):
            phase = f_idx / float(num_frames)
            svg_text = generate_dynamic_solution_svg(post_or_idea, frame_phase=phase)
            frame_svg = tmp_path / f"frame_{f_idx:02d}.svg"
            frame_png = tmp_path / f"frame_{f_idx:02d}.png"
            frame_svg.write_text(svg_text, encoding="utf-8")
            subprocess.run(
                [
                    str(chrome),
                    "--headless",
                    "--disable-gpu",
                    "--window-size=1600,980",
                    f"--screenshot={frame_png}",
                    f"file://{frame_svg}",
                ],
                check=False,
                capture_output=True,
            )
            if f_idx == 1 and output_png_path is not None and frame_png.exists():
                output_png_path.write_bytes(frame_png.read_bytes())

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
                str(output_gif_path),
            ],
            check=False,
            capture_output=True,
        )

    return output_gif_path.exists()
