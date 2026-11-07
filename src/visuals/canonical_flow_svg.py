"""Canonical Flow SVG & Zero-Origin W3C Flattener (Cross-Platform Linux/macOS).

Provides:
- Cross-platform `resolve_chrome_bin()` and `resolve_ffmpeg_bin()` (`shutil.which` + OS fallbacks).
- Zero-Origin W3C SVG Flattener (`flatten_svg_zero_origin`, `audit_zero_origin_svg`) for Dendrite / Google Slides / Draw.io compatibility.
- Animated conduit primitive `_flow()` with baked zero-origin polygon arrowheads and `<animateMotion>` signal packets.
- Executive Light-Theme (`#F8FAFC` / `#FFFFFF`) 4-step problem-to-solution dynamic flow generator (`generate_dynamic_solution_svg`) and looping GIF compiler (`render_animated_gif_for_idea`) with Role-Label-Only attribution (`Rule 53`).
"""

from __future__ import annotations

import html
import math
import re
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

W, H = 1600, 980
BLUE, PURPLE, AMBER, GREEN, RED = "#2563EB", "#7C3AED", "#D97706", "#059669", "#DC2626"
NAVY, INK, SLATE, MUTED, LINE = "#0F2942", "#0F172A", "#475569", "#64748B", "#CBD5E1"
BG, WHITE, TEAL, SKY = "#F8FAFC", "#FFFFFF", "#0D9488", "#0284C7"
FONT = "Inter, -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

Point = Tuple[float, float]

CSS = """
@keyframes flowDash { from { stroke-dashoffset: 40; } to { stroke-dashoffset: 0; } }
.flow-line { animation: flowDash 1.0s linear infinite; }
@keyframes pulseStroke { 0%,100% { stroke-width: 2.4px; } 50% { stroke-width: 5px; } }
.pulse { animation: pulseStroke 2.2s ease-in-out infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }
.blink { animation: blink 1.4s ease-in-out infinite; }
@keyframes phaseSpot1 { 0%,24% { opacity: 0.96; stroke-width: 3.4px; } 26%,100% { opacity: 0.22; stroke-width: 1.5px; } }
@keyframes phaseSpot2 { 0%,24% { opacity: 0.22; stroke-width: 1.5px; } 25%,49% { opacity: 0.96; stroke-width: 3.4px; } 51%,100% { opacity: 0.22; stroke-width: 1.5px; } }
@keyframes phaseSpot3 { 0%,49% { opacity: 0.22; stroke-width: 1.5px; } 50%,74% { opacity: 0.96; stroke-width: 3.4px; } 76%,100% { opacity: 0.22; stroke-width: 1.5px; } }
@keyframes phaseSpot4 { 0%,74% { opacity: 0.22; stroke-width: 1.5px; } 75%,99% { opacity: 0.96; stroke-width: 3.4px; } 100% { opacity: 0.22; stroke-width: 1.5px; } }
.phase-glow-1 { animation: phaseSpot1 4.8s ease-in-out infinite; }
.phase-glow-2 { animation: phaseSpot2 4.8s ease-in-out infinite; }
.phase-glow-3 { animation: phaseSpot3 4.8s ease-in-out infinite; }
.phase-glow-4 { animation: phaseSpot4 4.8s ease-in-out infinite; }
"""


def resolve_chrome_bin() -> Optional[Path]:
    """Resolve Headless Chrome / Chromium binary across Linux and macOS."""
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found and Path(found).exists():
            return Path(found)
    for candidate in (
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ):
        p = Path(candidate)
        if p.exists():
            return p
    return None


def resolve_ffmpeg_bin() -> Optional[Path]:
    """Resolve FFmpeg binary across Linux and macOS."""
    found = shutil.which("ffmpeg")
    if found and Path(found).exists():
        return Path(found)
    for candidate in ("/usr/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg"):
        p = Path(candidate)
        if p.exists():
            return p
    return None


def _esc(val: Any) -> str:
    return html.escape("" if val is None else str(val), quote=True)


def _wrap(text: Any, width: int, max_lines: int = 3) -> List[str]:
    clean = str(text or "").strip()
    if not clean:
        return [""]
    lines = textwrap.wrap(clean, width=max(8, int(width)))
    if len(lines) > max_lines:
        for extra in range(4, 36, 4):
            retry = textwrap.wrap(clean, width=width + extra)
            if len(retry) <= max_lines:
                return retry
        return lines[:max_lines]
    return lines


def _t(
    x: float,
    y: float,
    s: Any,
    size: float = 12,
    weight: int = 600,
    fill: str = INK,
    anchor: str = "start",
    mono: bool = False,
    extra: str = "",
) -> str:
    fam = MONO if mono else FONT
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" {extra}>{_esc(s)}</text>'
    )


def _plen(pts: Sequence[Point]) -> Tuple[List[float], float]:
    segs: List[float] = []
    total = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg_len = math.hypot(x2 - x1, y2 - y1)
        segs.append(seg_len)
        total += seg_len
    return segs, total


def _pat(pts: Sequence[Point], t: float) -> Point:
    segs, total = _plen(pts)
    d = max(0.0, min(1.0, t)) * total
    for (x1, y1), (x2, y2), seg_len in zip(pts, pts[1:], segs):
        if d <= seg_len or seg_len == 0:
            r = 0.0 if seg_len == 0 else d / seg_len
            return x1 + (x2 - x1) * r, y1 + (y2 - y1) * r
        d -= seg_len
    return pts[-1]


def _flow(
    pts: Sequence[Point],
    color: str,
    phase: Optional[float] = None,
    label: Optional[str] = None,
    dur: float = 1.6,
    width: float = 2.8,
    head: bool = True,
    packets: int = 1,
    dash: str = "10 6",
    track: bool = True,
    label_dy: float = -22,
    label_at: float = 0.5,
    solid: bool = False,
    converge_x: Optional[float] = None,
) -> str:
    """Zero-origin moving-arrow conduit with baked polygon arrowheads and clamped packet positions."""
    pts = [(float(x), float(y)) for x, y in pts]
    if converge_x is not None and len(pts) == 2:
        (sx, sy), (tx, ty) = pts[0], pts[1]
        cx = float(converge_x)
        pts = [(sx, sy), (cx, sy), (cx, ty), (tx, ty)]
    _, total_len = _plen(pts)
    if total_len < 38.0:
        h_len, h_wing, h_notch, retract = 8.5, 4.8, 6.4, 5.5
    elif total_len < 64.0:
        h_len, h_wing, h_notch, retract = 10.8, 6.0, 8.0, 7.2
    else:
        h_len, h_wing, h_notch, retract = 12.8, 7.2, 9.6, 10.0
    ang = 0.0
    if head and len(pts) >= 2:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        seg_len = math.hypot(x2 - x1, y2 - y1) or 1.0
        ux, uy = (x2 - x1) / seg_len, (y2 - y1) / seg_len
        actual_retract = min(retract, seg_len * 0.42)
        line_pts = list(pts[:-1]) + [(x2 - ux * actual_retract, y2 - uy * actual_retract)]
        ang = math.degrees(math.atan2(uy, ux))
    else:
        line_pts = list(pts)
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in line_pts)
    out: List[str] = []
    eff_width = min(width, 2.4) if total_len < 42.0 else width
    if track:
        halo_w = eff_width + (4.2 if total_len < 48.0 else 5.8)
        out.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="0.11" stroke-width="{halo_w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
        out.append(
            f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.80" stroke-width="{eff_width + 2.0:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if solid:
        out.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{eff_width:.1f}" stroke-linejoin="round" stroke-linecap="round"/>'
        )
    else:
        off = 0.0 if phase is None else -phase * 20.0
        cls = ' class="flow-line"' if phase is None else ""
        out.append(
            f'<path d="{d}"{cls} fill="none" stroke="{color}" stroke-width="{eff_width:.1f}" stroke-linejoin="round" '
            f'stroke-dasharray="{dash}" stroke-dashoffset="{off:.1f}"/>'
        )
    if head and len(pts) >= 2:
        x2, y2 = pts[-1]
        rad = math.radians(ang)
        ca, sa = math.cos(rad), math.sin(rad)
        raw_head = ((0.0, 0.0), (-h_len, -h_wing), (-h_notch, 0.0), (-h_len, h_wing))
        baked_pts = " ".join(
            f"{x2 + px * ca - py * sa:.1f},{y2 + px * sa + py * ca:.1f}"
            for px, py in raw_head
        )
        out.append(f'<polygon points="{baked_pts}" fill="{color}"/>')
    r_outer = 5.6 if total_len < 84.0 else 7.4
    r_mid = 3.8 if total_len < 84.0 else 5.0
    r_ring = 2.8 if total_len < 84.0 else 3.8
    r_core = 1.3 if total_len < 84.0 else 1.7
    if phase is None:
        for k in range(max(0, packets)):
            begin = -(k * dur / max(1, packets))
            out.append(
                f"<g>"
                f'<circle r="{r_outer:.1f}" fill="{color}" fill-opacity="0.15"/>'
                f'<circle r="{r_mid:.1f}" fill="{color}" fill-opacity="0.28"/>'
                f'<circle r="{r_ring:.1f}" fill="#FFFFFF" stroke="{color}" stroke-width="2.0"/>'
                f'<circle r="{r_core:.1f}" fill="{color}"/>'
                f'<animateMotion dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite" path="{d}"/>'
                f"</g>"
            )
    else:
        eff_packets = 0 if total_len < 42.0 else packets
        for k in range(max(0, eff_packets)):
            raw_t = (phase + k / max(1, eff_packets)) % 1.0
            clamped_t = 0.22 + 0.52 * raw_t
            px, py = _pat(line_pts, clamped_t)
            out.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_outer:.1f}" fill="{color}" fill-opacity="0.15"/>'
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_mid:.1f}" fill="{color}" fill-opacity="0.28"/>'
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_ring:.1f}" fill="#FFFFFF" stroke="{color}" stroke-width="2.0"/>'
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r_core:.1f}" fill="{color}"/>'
            )
    if label:
        lx, ly = _pat(line_pts, label_at)
        pw = min(620, int(len(label) * 5.9 + 24))
        px0, py0 = lx - pw / 2, ly + label_dy - 11
        out.append(
            f'<rect x="{px0 - 2:.1f}" y="{py0 - 1.5:.1f}" width="{pw + 4}" height="25" rx="12.5" fill="#FFFFFF" fill-opacity="0.96"/>'
            f'<rect x="{px0:.1f}" y="{py0:.1f}" width="{pw}" height="22" rx="11" fill="#FFFFFF" fill-opacity="1.0" '
            f'stroke="{color}" stroke-width="1.4"/>'
        )
        out.append(_t(lx, ly + label_dy + 3.5, label, 9.3, 800, color, "middle"))
    return "\n".join(out)


def flatten_svg_zero_origin(svg_xml: str) -> str:
    """Zero-Origin W3C SVG Flattener (Dendrite b/571807152 compatibility gate)."""
    def _expand_hex(m: re.Match[str]) -> str:
        attr, h = m.group(1), m.group(2).upper()
        return f'{attr}="#{h[0]*2}{h[1]*2}{h[2]*2}"'

    svg_xml = re.sub(r'\b(fill|stroke|flood-color|stop-color)="#([0-9a-fA-F]{3})"', _expand_hex, svg_xml)

    def _bake_poly(m: re.Match[str]) -> str:
        pts_str, fill_col, tx_s, ty_s, ang_s = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        tx, ty, rad = float(tx_s), float(ty_s), math.radians(float(ang_s))
        ca, sa = math.cos(rad), math.sin(rad)
        baked: List[str] = []
        for pair in pts_str.strip().split():
            px_s, py_s = pair.split(",")
            px, py = float(px_s), float(py_s)
            baked.append(f"{tx + px * ca - py * sa:.1f},{ty + px * sa + py * ca:.1f}")
        return f'<polygon points="{" ".join(baked)}" fill="{fill_col}"/>'

    svg_xml = re.sub(
        r'<polygon points="([^"]+)" fill="([^"]+)" transform="translate\(([-0-9.]+)[ ,]+([-0-9.]+)\) rotate\(([-0-9.]+)\)"\s*/>',
        _bake_poly,
        svg_xml,
    )
    return svg_xml


def audit_zero_origin_svg(svg_xml: str) -> Dict[str, Any]:
    """Deterministic Zero-Origin W3C SVG, 2D Text-Collision & Official Google Cloud Brand Gate."""
    import xml.etree.ElementTree as ET

    transform_polygons = len(re.findall(r'<polygon[^>]*\btransform=', svg_xml))
    unanchored_rotations = len(re.findall(r'\btransform="rotate\(\s*[-0-9.]+\s*\)"', svg_xml))
    three_digit_hex_attrs = len(re.findall(r'\b(?:fill|stroke|flood-color|stop-color)="#[0-9a-fA-F]{3}"', svg_xml))
    text_bodies = " ".join(re.findall(r'<text[^>]*>([^<]+)</text>', svg_xml))
    standalone_gcp = len(re.findall(r'(?<![A-Za-z0-9_-])GCP(?![A-Za-z0-9_-])', text_bodies))

    text_bbox_overlaps = 0
    try:
        root = ET.fromstring(svg_xml)
        boxes: List[Tuple[float, float, float, float]] = []
        for el in root.iter():
            if el.tag.split("}")[-1] == "text":
                txt = ("".join(el.itertext())).strip()
                if not txt:
                    continue
                x = float(el.attrib.get("x", 0.0))
                y = float(el.attrib.get("y", 0.0))
                fs = float(el.attrib.get("font-size", 11.0))
                anchor = el.attrib.get("text-anchor", "start")
                fam = el.attrib.get("font-family", "")
                char_w = fs * (0.58 if "mono" in fam.lower() else 0.52)
                w = len(txt) * char_w
                if anchor == "middle":
                    x0, x1 = x - w / 2.0, x + w / 2.0
                elif anchor == "end":
                    x0, x1 = x - w, x
                else:
                    x0, x1 = x, x + w
                y0, y1 = y - fs * 0.82, y + fs * 0.18
                boxes.append((x0, y0, x1, y1))
        for i in range(len(boxes)):
            ax0, ay0, ax1, ay1 = boxes[i]
            for j in range(i + 1, len(boxes)):
                bx0, by0, bx1, by1 = boxes[j]
                if min(ax1, bx1) - max(ax0, bx0) > 8.0 and min(ay1, by1) - max(ay0, by0) > 4.5:
                    text_bbox_overlaps += 1
    except Exception:
        text_bbox_overlaps = 999

    return {
        "transform_polygons": transform_polygons,
        "unanchored_rotations": unanchored_rotations,
        "three_digit_hex_attrs": three_digit_hex_attrs,
        "standalone_gcp_brand_violations": standalone_gcp,
        "text_bbox_overlaps": text_bbox_overlaps,
        "passed": (
            transform_polygons == 0
            and unanchored_rotations == 0
            and three_digit_hex_attrs == 0
            and standalone_gcp == 0
            and text_bbox_overlaps == 0
        ),
    }


def _concise_gcp_primitive(raw: str) -> str:
    base = str(raw or "").split("(")[0].strip()
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
    if "dynamic_steps" in post_or_idea and "problem_flow_nodes" in post_or_idea:
        return post_or_idea

    steps = post_or_idea.get("core_steps", [])
    colors = ["#2563EB", "#7C3AED", "#D97706", "#059669"]
    gcp_stack = post_or_idea.get("gcp_stack") or ["Google Cloud ADK", "Vertex AI Gemini 3.8 Flash", "Model Armor", "Cloud Run"]
    dyn_steps = []
    for idx, s in enumerate(steps[:4]):
        dyn_steps.append(
            {
                "step": f"0{idx + 1}",
                "badge": f"STEP {idx + 1} • STAGE 0{idx + 1}",
                "title": s["title"],
                "how_it_works": s["desc"],
                "gcp_primitive": _concise_gcp_primitive(gcp_stack[idx % len(gcp_stack)]),
                "arrow_label": f"Step {idx + 1} -> {idx + 2}",
                "color": colors[idx % 4],
            }
        )
    metrics_items = list(post_or_idea.get("metrics", {}).items())
    m1 = f"{metrics_items[0][0]}: {metrics_items[0][1]}" if len(metrics_items) > 0 else "100% Verified"
    m2 = f"{metrics_items[1][0]}: {metrics_items[1][1]}" if len(metrics_items) > 1 else "Zero Drift"
    src_obj = post_or_idea.get("primary_source", {"title": "Google Cloud Agentic Architecture", "verified_claims": ["Deterministic runtime verification"]})
    src_short = src_obj["title"].split("(")[0].strip()
    if len(src_short) > 68:
        src_short = src_short.split(":")[0].strip()

    return {
        "id": post_or_idea["id"],
        "est_post_time": post_or_idea.get("est_post_time", "Published Signal • Verified Google Cloud Repo"),
        "repo_slug": post_or_idea["repo_slug"],
        "post_title": post_or_idea["post_title"],
        "best_approach_title": src_obj["title"],
        "why_it_happens_plain": post_or_idea.get("original_hook", "Unprotected agent loops drift without deterministic contracts."),
        "primary_source": src_obj,
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
            "daily_takeaway": src_obj["verified_claims"][0],
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
    dash_offset = 0.0 if frame_phase is None else -frame_phase * 24.0
    path_d = f"M {x1 + 4} {y} L {x2 - 12} {y}"
    parts = [
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{color}" stroke-opacity="0.16" stroke-width="11" stroke-linecap="round"/>',
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.76" stroke-width="5.6" stroke-linecap="round"/>',
        f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" class="moving-arrow-line" stroke="{color}" stroke-width="3.8" stroke-dasharray="12 8" stroke-dashoffset="{dash_offset:.1f}"/>',
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


def _step_contract_spec(idea_id: str, idx: int, st: Dict[str, Any]) -> Tuple[str, str, str]:
    if st.get("header_cap") and st.get("code_contract") and st.get("status_tag"):
        return str(st["header_cap"]), str(st["code_contract"]), str(st["status_tag"])
    if "T01" in str(idea_id) or str(idea_id) == "IDEA-01":
        specs = [
            ("SHA-256 HASH", "h = sha256(tool + canon(args))", "DETERMINISTIC"),
            ("0 LLM TOKENS", "if win5.count(h) >= 2: block()", "SHORT-CIRCUIT"),
            ("STRATEGY PIVOT", "inject('switch_tool | ask')", "94% RECOVERY"),
            ("HARD CEILING", "RunConfig(steps=15, usd=0.25)", "CHECKPOINTED"),
        ]
        return specs[idx % 4]
    prim_slug = st.get("gcp_primitive", "adk_guard").lower().replace(" ", "_")[:16].strip("_")
    fallback = [
        ("STAGE 01 GATE", f"fingerprint({prim_slug})", "DETERMINISTIC"),
        ("STAGE 02 GUARD", f"enforce_guard({prim_slug})", "0 DRIFT"),
        ("STAGE 03 ROUTE", f"route_verified({prim_slug})", "GROUNDED"),
        ("STAGE 04 AUDIT", f"commit_receipt({prim_slug})", "CHECKPOINTED"),
    ]
    return fallback[idx % 4]


def _render_step_vector_icon(idx: int, x: float, y: float, color: str) -> str:
    box = f'<rect x="{x:.1f}" y="{y:.1f}" width="28" height="28" rx="7" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="1.5"/>'
    cx, cy = x + 14.0, y + 14.0
    if idx == 0:
        glyph = (
            f'<line x1="{cx - 6:.1f}" y1="{cy - 3:.1f}" x2="{cx + 6:.1f}" y2="{cy - 3:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
            f'<line x1="{cx - 6:.1f}" y1="{cy + 3:.1f}" x2="{cx + 6:.1f}" y2="{cy + 3:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
            f'<line x1="{cx - 3:.1f}" y1="{cy - 6:.1f}" x2="{cx - 3:.1f}" y2="{cy + 6:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
            f'<line x1="{cx + 3:.1f}" y1="{cy - 6:.1f}" x2="{cx + 3:.1f}" y2="{cy + 6:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        )
    elif idx == 1:
        glyph = (
            f'<polygon points="{cx:.1f},{cy - 7:.1f} {cx + 6.5:.1f},{cy - 4:.1f} {cx + 5.0:.1f},{cy + 4.5:.1f} {cx:.1f},{cy + 7.5:.1f} {cx - 5.0:.1f},{cy + 4.5:.1f} {cx - 6.5:.1f},{cy - 4:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.9" stroke-linejoin="round"/>'
            f'<line x1="{cx - 2.8:.1f}" y1="{cy:.1f}" x2="{cx + 2.8:.1f}" y2="{cy:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>'
        )
    elif idx == 2:
        glyph = (
            f'<circle cx="{cx - 4.5:.1f}" cy="{cy + 4.5:.1f}" r="2.5" fill="{color}"/>'
            f'<circle cx="{cx + 5.0:.1f}" cy="{cy - 4.5:.1f}" r="2.5" fill="{color}"/>'
            f'<circle cx="{cx + 5.0:.1f}" cy="{cy + 4.5:.1f}" r="2.5" fill="none" stroke="{color}" stroke-width="1.6"/>'
            f'<path d="M {cx - 2.0:.1f} {cy + 4.5:.1f} L {cx + 1.0:.1f} {cy - 4.5:.1f} L {cx + 2.5:.1f} {cy - 4.5:.1f}" fill="none" stroke="{color}" stroke-width="1.9" stroke-linecap="round"/>'
        )
    else:
        glyph = (
            f'<rect x="{cx - 5.5:.1f}" y="{cy - 1.0:.1f}" width="11" height="8" rx="2" fill="none" stroke="{color}" stroke-width="1.9"/>'
            f'<path d="M {cx - 3.2:.1f} {cy - 1.0:.1f} L {cx - 3.2:.1f} {cy - 4.5:.1f} A 3.2 3.2 0 0 1 {cx + 3.2:.1f} {cy - 4.5:.1f} L {cx + 3.2:.1f} {cy - 1.0:.1f}" fill="none" stroke="{color}" stroke-width="1.8"/>'
        )
    return box + glyph


def generate_dynamic_solution_svg(post_or_idea: Dict[str, Any], frame_phase: Optional[float] = None) -> str:
    """Generate a 1600x980 Publication-Grade Executive Light-Theme Dynamic Flow Diagram (`Rule 53` & `Rule 54`)."""
    idea = _normalize_idea_spec(post_or_idea)
    p_nodes = idea["problem_flow_nodes"][:3]
    d_steps = idea["dynamic_steps"][:4]
    ba = idea["before_after"]

    active_step_idx = -1 if frame_phase is None else int(frame_phase * 4) % 4
    title_str = str(idea["post_title"])
    title_fs = 17.5 if len(title_str) > 118 else (20.0 if len(title_str) > 92 else 22.5)
    sub_str = f"Best Approach: {idea['best_approach_title']}  •  Repo: generated-repos/{idea['repo_slug']}"
    if len(sub_str) > 185:
        sub_str = sub_str[:182].rsplit(" ", 1)[0].rstrip("• ")

    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 980" width="1600" height="980">',
        "<defs>",
        '  <filter id="cardShadow" x="-3%" y="-3%" width="106%" height="110%">',
        '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.065"/>',
        "  </filter>",
        '  <linearGradient id="glassCardGrad" x1="0" y1="0" x2="0" y2="1">',
        '    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.98"/>',
        '    <stop offset="100%" stop-color="#F8FAFC" stop-opacity="0.94"/>',
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
        "    @keyframes arrowStream { from { stroke-dashoffset: 40; } to { stroke-dashoffset: 0; } }",
        "    @keyframes returnStream { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 48; } }",
        "    @keyframes pulseGlow { 0%, 100% { stroke-width: 2.2px; } 50% { stroke-width: 3.8px; } }",
        "    .moving-arrow-line { animation: arrowStream 1.0s linear infinite; }",
        "    .moving-return-line { animation: returnStream 1.2s linear infinite; }",
        "    .step-card-animated { animation: pulseGlow 2.4s ease-in-out infinite; }",
        "  </style>",
        "</defs>",
        '<rect x="0" y="0" width="1600" height="980" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshBlue)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshEmerald)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#meshViolet)"/>',
        '<rect x="0" y="0" width="1600" height="980" fill="url(#archGrid)"/>',
        '<rect x="0" y="0" width="400" height="6" fill="#4285F4"/>',
        '<rect x="400" y="0" width="400" height="6" fill="#EA4335"/>',
        '<rect x="800" y="0" width="400" height="6" fill="#FBBC04"/>',
        '<rect x="1200" y="0" width="400" height="6" fill="#34A853"/>',
        '<line x1="28" y1="142" x2="28" y2="918" stroke="#CBD5E1" stroke-width="2.2"/>',
        '<rect x="10" y="132" width="36" height="26" rx="8" fill="#FEF2F2" stroke="#DC2626" stroke-width="1.8"/>',
        '<text x="28" y="149" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#B91C1C" text-anchor="middle">01</text>',
        '<rect x="10" y="346" width="36" height="26" rx="8" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.8"/>',
        '<text x="28" y="363" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#1D4ED8" text-anchor="middle">02</text>',
        '<rect x="10" y="762" width="36" height="26" rx="8" fill="#ECFDF5" stroke="#059669" stroke-width="1.8"/>',
        '<text x="28" y="779" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">03</text>',
        '<circle cx="28" cy="920" r="4" fill="#94A3B8"/>',
        '<rect x="56" y="14" width="1508" height="100" rx="14" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#cardShadow)"/>',
        '<rect x="58" y="16" width="1504" height="16" rx="10" fill="url(#glassSheen)"/>',
        '<rect x="74" y="24" width="334" height="22" rx="6" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.2"/>',
        f'<text x="241" y="39" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#1D4ED8" text-anchor="middle">{_esc(idea["id"])} • {_esc(idea.get("est_post_time", "MORNING EST"))}</text>',
        '<rect x="420" y="24" width="388" height="22" rx="6" fill="#ECFDF5" stroke="#059669" stroke-width="1.2"/>',
        '<text x="614" y="39" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#047857" text-anchor="middle">DAILY AGENTIC AI PAIN POINT &amp; PRODUCTION FIX</text>',
        '<rect x="820" y="24" width="388" height="22" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.2"/>',
        '<text x="1014" y="39" font-family="Inter, sans-serif" font-size="9.8" font-weight="800" fill="#0369A1" text-anchor="middle">FORMAT LINEAGE: Google Cloud ADK + OpenHands</text>',
        '<rect x="1220" y="24" width="326" height="22" rx="6" fill="#0F2942"/>',
        '<text x="1383" y="39" font-family="Inter, sans-serif" font-size="9.8" font-weight="800" fill="#38BDF8" text-anchor="middle">&gt;&gt;&gt; DYNAMIC FLOW • MOVING ARROWS</text>',
        f'<text x="74" y="74" font-family="Inter, sans-serif" font-size="{title_fs}" font-weight="800" fill="#0F172A">{_esc(title_str)}</text>',
        f'<text x="74" y="99" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#475569">{_esc(sub_str)}</text>',
        '<rect x="56" y="124" width="1508" height="204" rx="14" fill="url(#glassCardGrad)" stroke="#FCA5A5" stroke-width="1.8" filter="url(#cardShadow)"/>',
        '<rect x="56" y="124" width="1508" height="30" rx="12" fill="#991B1B"/>',
        '<text x="74" y="144" font-family="Inter, sans-serif" font-size="11.8" font-weight="800" fill="#FFFFFF">1. THE DAILY PROBLEM USERS FACE EVERY DAY — WHAT GOES WRONG IN STANDARD AGENTS</text>',
        '<rect x="1194" y="128" width="352" height="22" rx="11" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.2"/>',
        '<text x="1370" y="143" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#991B1B" text-anchor="middle">INCIDENT TRACE • UNPROTECTED RETRY CASCADE</text>',
        '<rect x="68" y="160" width="1004" height="126" rx="10" fill="#FFF5F5" fill-opacity="0.92" stroke="#F87171" stroke-width="1.6" stroke-dasharray="6 4"/>',
    ]

    fail_capsules = ["HTTP 429/503", "x48 RETRIES", "-$400 BURN"]
    fail_traces = [
        "err: ToolTimeoutError(status=503)",
        "sha256(call) repeated 48x in window",
        "182,400 wasted tok • state=lost",
    ]
    for idx, pnode in enumerate(p_nodes):
        px = 78 + idx * 346
        is_last = idx == 2
        card_fill = "#FEE2E2" if is_last else "#FFFFFF"
        border_col = "#DC2626" if is_last else "#EF4444"
        title_col = "#991B1B" if is_last else "#0F172A"
        stage_tag = "01 | FAILURE TRIGGER" if idx == 0 else ("02 | FAILURE AMPLIFIER" if idx == 1 else "03 | DAILY USER PAIN")
        sub_lines = _wrap(pnode["sub"], width=42, max_lines=2)
        svg.extend(
            [
                f'<rect x="{px}" y="166" width="292" height="114" rx="10" fill="{card_fill}" stroke="{border_col}" stroke-width="2.0" filter="url(#cardShadow)"/>',
                f'<rect x="{px}" y="166" width="292" height="26" rx="8" fill="{border_col}"/>',
                f'<text x="{px + 12}" y="183" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#FFFFFF">{stage_tag}</text>',
                f'<rect x="{px + 194}" y="170" width="88" height="18" rx="9" fill="#FFFFFF"/>',
                f'<text x="{px + 238}" y="182" font-family="Inter, sans-serif" font-size="8.6" font-weight="800" fill="{border_col}" text-anchor="middle">{fail_capsules[idx]}</text>',
                f'<text x="{px + 14}" y="210" font-family="Inter, sans-serif" font-size="13.2" font-weight="800" fill="{title_col}">{_esc(pnode["label"])}</text>',
                f'<text x="{px + 14}" y="230" font-family="Inter, sans-serif" font-size="11.2" font-weight="600" fill="#475569">{_esc(sub_lines[0])}</text>',
            ]
        )
        if len(sub_lines) > 1:
            svg.append(
                f'<text x="{px + 14}" y="245" font-family="Inter, sans-serif" font-size="10.8" font-weight="600" fill="#64748B">{_esc(sub_lines[1])}</text>'
            )
        svg.extend(
            [
                f'<rect x="{px + 10}" y="250" width="272" height="22" rx="6" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.2"/>',
                f'<text x="{px + 18}" y="265" font-family="ui-monospace, monospace" font-size="9.2" font-weight="700" fill="#991B1B">{fail_traces[idx]}</text>',
            ]
        )
        if idx < 2:
            svg.append(
                _render_moving_horizontal_arrow(
                    arrow_id=f"prob_arr_{idx}",
                    x1=px + 296,
                    x2=px + 342,
                    y=223,
                    color="#DC2626",
                    label=None,
                    frame_phase=frame_phase,
                    dur="1.3s",
                )
            )

    why_lines = _wrap(idea["why_it_happens_plain"], width=56, max_lines=3)
    svg.extend(
        [
            '<rect x="1084" y="160" width="466" height="126" rx="10" fill="url(#glassCardGrad)" stroke="#DC2626" stroke-width="1.8" filter="url(#cardShadow)"/>',
            '<rect x="1084" y="160" width="466" height="26" rx="8" fill="#FEE2E2"/>',
            '<text x="1098" y="177" font-family="Inter, sans-serif" font-size="9.8" font-weight="800" fill="#991B1B">WHY THIS HAPPENS (PLAIN-ENGLISH ROOT CAUSE)</text>',
        ]
    )
    for w_idx, wl in enumerate(why_lines):
        svg.append(
            f'<text x="1098" y="{203 + w_idx * 16.5:.1f}" font-family="Inter, sans-serif" font-size="11.2" font-weight="600" fill="#1E293B">{_esc(wl)}</text>'
        )
    svg.extend(
        [
            '<rect x="1096" y="252" width="442" height="24" rx="6" fill="#F8FAFC" stroke="#FCA5A5" stroke-width="1.2"/>',
            '<text x="1106" y="268" font-family="ui-monospace, monospace" font-size="9.3" font-weight="800" fill="#B91C1C">ROOT INVARIANT: P(same_tool_call | unchanged_error) = 0.94</text>',
            '<rect x="68" y="294" width="1482" height="26" rx="7" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>',
            '<text x="82" y="311" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#64748B">DIAGNOSTIC</text>',
            '<text x="164" y="311" font-family="Inter, sans-serif" font-size="10.8" font-weight="600" fill="#0F172A">Audit trace spans for &gt;= 2 identical sha256(tool_name + canonical_args) calls with error status inside any 5-turn window.</text>',
            '<circle cx="1532" cy="307" r="9" fill="#0F172A"/>',
            '<text x="1532" y="311" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">↑</text>',
            '<rect x="56" y="338" width="1508" height="408" rx="14" fill="url(#glassCardGrad)" stroke="#93C5FD" stroke-width="2.0" filter="url(#cardShadow)"/>',
            '<rect x="56" y="338" width="1508" height="32" rx="12" fill="#0F2942"/>',
            '<text x="74" y="359" font-family="Inter, sans-serif" font-size="11.8" font-weight="800" fill="#FFFFFF">2. THE BEST-PRACTICE ARCHITECTURAL SOLUTION — FOLLOW THE 4-STEP DYNAMIC FLOW &amp; CLOSED-LOOP GUARD</text>',
            '<rect x="1216" y="343" width="332" height="22" rx="11" fill="#1E3A8A" stroke="#60A5FA" stroke-width="1.2"/>',
            '<text x="1382" y="358" font-family="Inter, sans-serif" font-size="9.2" font-weight="800" fill="#BAE6FD" text-anchor="middle">GOOGLE CLOUD ADK ⇄ OPENHANDS / LANGGRAPH</text>',
        ]
    )

    from src.catalog.stack_pairings import oss_step_equivalent

    for idx, st in enumerate(d_steps):
        sx = 72 + idx * 390
        scol = st["color"]
        how_lines = _wrap(st["how_it_works"], width=38, max_lines=3)
        is_active = idx == active_step_idx
        stroke_w = "3.8" if is_active else "2.2"
        anim_cls = "step-card-animated" if frame_phase is None else ""
        header_cap, code_expr, status_tag = _step_contract_spec(idea["id"], idx, st)
        st_title = str(st["title"])
        st_title_fs = 12.6 if len(st_title) > 25 else 14.2

        svg.extend(
            [
                f'<rect x="{sx}" y="378" width="298" height="258" rx="12" class="{anim_cls}" fill="url(#glassCardGrad)" stroke="{scol}" stroke-width="{stroke_w}" filter="url(#cardShadow)"/>',
                f'<rect x="{sx}" y="378" width="298" height="32" rx="10" fill="{scol}"/>',
                f'<text x="{sx + 12}" y="399" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF">{_esc(st["badge"])}</text>',
                f'<rect x="{sx + 194}" y="384" width="94" height="20" rx="10" fill="#FFFFFF"/>',
                f'<text x="{sx + 241}" y="398" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="{scol}" text-anchor="middle">{_esc(header_cap)}</text>',
                _render_step_vector_icon(idx, sx + 12, 418, scol),
                f'<text x="{sx + 48}" y="438" font-family="Inter, sans-serif" font-size="{st_title_fs}" font-weight="800" fill="#0F172A">{_esc(st_title)}</text>',
                f'<line x1="{sx + 12}" y1="454" x2="{sx + 286}" y2="454" stroke="#E2E8F0" stroke-width="1.2"/>',
                f'<text x="{sx + 14}" y="470" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="{scol}">HOW IT WORKS:</text>',
            ]
        )
        for h_idx, hl in enumerate(how_lines):
            svg.append(
                f'<text x="{sx + 14}" y="{487 + h_idx * 16.5:.1f}" font-family="Inter, sans-serif" font-size="11.2" font-weight="600" fill="#1E293B">{_esc(hl)}</text>'
            )

        svg.extend(
            [
                f'<rect x="{sx + 12}" y="532" width="274" height="42" rx="8" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.3"/>',
                f'<text x="{sx + 20}" y="546" font-family="Inter, sans-serif" font-size="8.2" font-weight="800" fill="#64748B">RUNTIME CONTRACT</text>',
                f'<rect x="{sx + 194}" y="536" width="84" height="15" rx="7.5" fill="#DCFCE7" stroke="#16A34A" stroke-width="1"/>',
                f'<text x="{sx + 236}" y="547" font-family="Inter, sans-serif" font-size="7.6" font-weight="800" fill="#15803D" text-anchor="middle">{_esc(status_tag)}</text>',
                f'<text x="{sx + 20}" y="566" font-family="ui-monospace, monospace" font-size="9.6" font-weight="800" fill="#0F172A">{_esc(code_expr)}</text>',
            ]
        )

        oss_label = st.get("oss_primitive") or oss_step_equivalent(idea["id"], st["step"], st["gcp_primitive"])
        svg.extend(
            [
                f'<rect x="{sx + 12}" y="582" width="274" height="46" rx="8" fill="#FFFFFF" stroke="{scol}" stroke-width="1.5"/>',
                f'<rect x="{sx + 12}" y="582" width="274" height="23" rx="7" fill="{scol}" fill-opacity="0.10"/>',
                f'<text x="{sx + 22}" y="598" font-family="ui-monospace, monospace" font-size="9.4" font-weight="800" fill="{scol}">GOOGLE: {_esc(st["gcp_primitive"][:36])}</text>',
                f'<text x="{sx + 22}" y="619" font-family="ui-monospace, monospace" font-size="9.4" font-weight="800" fill="#0F172A">OSS: {_esc(oss_label[:38])}</text>',
            ]
        )

        if idx < 3:
            svg.append(
                _render_moving_horizontal_arrow(
                    arrow_id=f"sol_arr_{idx}",
                    x1=sx + 302,
                    x2=sx + 386,
                    y=506,
                    color=scol,
                    label=st.get("arrow_label", "Next"),
                    frame_phase=frame_phase,
                    dur="1.5s",
                )
            )

    ret_dash_offset = 0.0 if frame_phase is None else frame_phase * 40.0
    return_path_d = "M 1391 638 L 1391 658 L 221 658 L 221 640"
    svg.extend(
        [
            f'<path d="{return_path_d}" fill="none" stroke="#059669" stroke-opacity="0.16" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{return_path_d}" fill="none" stroke="#FFFFFF" stroke-opacity="0.76" stroke-width="5.2" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path id="closed_loop_return_path" d="{return_path_d}" class="moving-return-line" fill="none" stroke="#059669" stroke-width="3.6" stroke-dasharray="14 10" stroke-dashoffset="{ret_dash_offset:.1f}"/>',
            '<polygon points="221,636 212,649 221,645 230,649" fill="#059669"/>',
            '<polygon points="480,658 492,651 490,658 492,665" fill="#059669"/>',
            '<polygon points="790,658 802,651 800,658 802,665" fill="#059669"/>',
            '<polygon points="1100,658 1112,651 1110,658 1112,665" fill="#059669"/>',
            '<rect x="180" y="672" width="1252" height="28" rx="14" fill="#ECFDF5" stroke="#059669" stroke-width="1.6"/>',
            f'<text x="806" y="690" font-family="Inter, sans-serif" font-size="11.2" font-weight="800" fill="#065F46" text-anchor="middle">CLOSED-LOOP FEEDBACK &lt;&lt;&lt; {_esc(idea["feedback_loop_label"])}</text>',
            '<rect x="68" y="710" width="1482" height="26" rx="7" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>',
            '<text x="82" y="727" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#1D4ED8">PROMPT / HOOK</text>',
            '<text x="182" y="727" font-family="Inter, sans-serif" font-size="10.8" font-weight="600" fill="#0F172A">Register BeforeToolCallback to hash (tool_name, args). On 2nd identical failure in 5 turns, short-circuit and inject a strategy-pivot directive.</text>',
            '<circle cx="1532" cy="723" r="9" fill="#0F172A"/>',
            '<text x="1532" y="727" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">↑</text>',
        ]
    )

    if frame_phase is None:
        svg.extend(
            [
                "<g>",
                '  <circle r="8.5" fill="#059669" fill-opacity="0.16"/>',
                '  <circle r="5.8" fill="#059669" fill-opacity="0.30"/>',
                '  <circle r="4.5" fill="#FFFFFF" stroke="#059669" stroke-width="2.4"/>',
                '  <circle r="1.8" fill="#059669"/>',
                '  <animateMotion dur="2.8s" repeatCount="indefinite"><mpath href="#closed_loop_return_path"/></animateMotion>',
                "</g>",
            ]
        )
    else:
        rx1 = 1391 - frame_phase * (1391 - 221)
        rx2 = 1391 - ((frame_phase + 0.5) % 1.0) * (1391 - 221)
        for rx_val in (rx1, rx2):
            svg.extend(
                [
                    f'<circle cx="{rx_val:.1f}" cy="658" r="8.5" fill="#059669" fill-opacity="0.16"/>',
                    f'<circle cx="{rx_val:.1f}" cy="658" r="5.8" fill="#059669" fill-opacity="0.32"/>',
                    f'<circle cx="{rx_val:.1f}" cy="658" r="4.5" fill="#FFFFFF" stroke="#059669" stroke-width="2.4"/>',
                    f'<circle cx="{rx_val:.1f}" cy="658" r="1.8" fill="#059669"/>',
                ]
            )

    svg.extend(
        [
            '<rect x="56" y="756" width="1508" height="176" rx="14" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#cardShadow)"/>',
            '<rect x="68" y="766" width="430" height="156" rx="10" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.8"/>',
            '<rect x="68" y="766" width="430" height="28" rx="8" fill="#991B1B"/>',
            '<text x="84" y="784" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF">3A. [X] BEFORE (STANDARD UNPROTECTED AGENT)</text>',
            '<rect x="82" y="804" width="402" height="48" rx="8" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.4"/>',
            f'<text x="96" y="833" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#991B1B">✘ {_esc(ba["before_metric_1"])}</text>',
            '<rect x="394" y="817" width="80" height="22" rx="11" fill="#FEE2E2" stroke="#F87171" stroke-width="1.1"/>',
            '<text x="434" y="832" font-family="Inter, sans-serif" font-size="8.2" font-weight="800" fill="#991B1B" text-anchor="middle">UNBOUNDED</text>',
            '<rect x="82" y="862" width="402" height="48" rx="8" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.4"/>',
            f'<text x="96" y="891" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#991B1B">✘ {_esc(ba["before_metric_2"])}</text>',
            '<rect x="394" y="875" width="80" height="22" rx="11" fill="#FEE2E2" stroke="#F87171" stroke-width="1.1"/>',
            '<text x="434" y="890" font-family="Inter, sans-serif" font-size="8.2" font-weight="800" fill="#991B1B" text-anchor="middle">HIGH RISK</text>',
            _render_moving_horizontal_arrow(
                arrow_id="ba_transform_arr",
                x1=502,
                x2=582,
                y=854,
                color="#059669",
                label="UPGRADE",
                frame_phase=frame_phase,
                dur="1.2s",
            ),
            '<rect x="586" y="766" width="440" height="156" rx="10" fill="#FFFFFF" stroke="#6EE7B7" stroke-width="2.0"/>',
            '<rect x="586" y="766" width="440" height="28" rx="8" fill="#065F46"/>',
            '<text x="602" y="784" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF">3B. [✓] AFTER (ENGINEERED HARNESS: GOOGLE + OSS)</text>',
            '<rect x="600" y="804" width="412" height="48" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>',
            f'<text x="614" y="833" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#065F46">✓ {_esc(ba["after_metric_1"])}</text>',
            '<rect x="920" y="817" width="82" height="22" rx="11" fill="#D1FAE5" stroke="#10B981" stroke-width="1.1"/>',
            '<text x="961" y="832" font-family="Inter, sans-serif" font-size="8.2" font-weight="800" fill="#065F46" text-anchor="middle">VERIFIED</text>',
            '<rect x="600" y="862" width="412" height="48" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>',
            f'<text x="614" y="891" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#065F46">✓ {_esc(ba["after_metric_2"])}</text>',
            '<rect x="920" y="875" width="82" height="22" rx="11" fill="#D1FAE5" stroke="#10B981" stroke-width="1.1"/>',
            '<text x="961" y="890" font-family="Inter, sans-serif" font-size="8.2" font-weight="800" fill="#065F46" text-anchor="middle">PRODUCTION</text>',
        ]
    )

    takeaway_lines = _wrap(ba["daily_takeaway"], width=64, max_lines=3)
    src_lines = _wrap("Source: " + idea["primary_source"]["title"], width=68, max_lines=2)
    svg.extend(
        [
            '<rect x="1040" y="766" width="510" height="156" rx="10" fill="#0F2942" stroke="#1E3A8A" stroke-width="2.0"/>',
            '<rect x="1056" y="778" width="228" height="22" rx="6" fill="#1D4ED8"/>',
            '<text x="1170" y="793" font-family="Inter, sans-serif" font-size="9.8" font-weight="800" fill="#FFFFFF" text-anchor="middle">GOLDEN RULE TO APPLY TODAY</text>',
            '<rect x="1296" y="778" width="238" height="22" rx="6" fill="#065F46"/>',
            '<text x="1415" y="793" font-family="Inter, sans-serif" font-size="9.2" font-weight="800" fill="#A7F3D0" text-anchor="middle">ZERO UNBOUNDED RETRIES</text>',
        ]
    )
    for t_idx, tl in enumerate(takeaway_lines):
        svg.append(
            f'<text x="1056" y="{822 + t_idx * 19.5:.1f}" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#F8FAFC">{_esc(tl)}</text>'
        )
    for s_idx, sl in enumerate(src_lines):
        svg.append(
            f'<text x="1056" y="{884 + s_idx * 15.0:.1f}" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#93C5FD">{_esc(sl)}</text>'
        )

    svg.extend(
        [
            '<rect x="210" y="942" width="1180" height="28" rx="14" fill="#0F172A"/>',
            '<text x="800" y="960" font-family="Inter, sans-serif" font-size="10.8" font-weight="800" fill="#F8FAFC" text-anchor="middle">3-BREAKER LOOP GUARD  •  Google Cloud ADK ⇄ OpenHands / LangGraph  •  Google Cloud Agentic Architecture Engineering  •  Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    return flatten_svg_zero_origin("\n".join(svg))


def render_animated_gif_for_idea(
    post_or_idea: Dict[str, Any],
    output_gif_path: Path,
    output_png_path: Optional[Path] = None,
    num_frames: int = 6,
) -> bool:
    """Compile a multi-frame looping Animated GIF with moving arrows using Headless Chrome + FFmpeg."""
    chrome = resolve_chrome_bin()
    ffmpeg = resolve_ffmpeg_bin()
    if chrome is None or ffmpeg is None:
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
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
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
