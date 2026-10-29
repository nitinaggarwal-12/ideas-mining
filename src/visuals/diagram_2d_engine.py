"""Production-Grade 2D Architecture & LinkedIn Infographic Engine (Rule 53 + Diagram Generation Engine SKILL.md).

Generates two distinct, high-density, zero-collision 2D visual architectures for each of the 8 posts:
1. `gcp-architecture-2d.svg` & `gcp-architecture-2d.drawio` (1600x1000 16:9):
   - Authentic Official Google Cloud Architecture Center Template #78 (Hub-and-Spoke) + 6-Zone Enterprise Matrix:
   - 18 distinct component cards with embedded vector SVG icons (Gemini 4-point star, Cloud Armor shield, IAM/KMS key,
     Cloud Run hex-play, GKE/OpenHands wheel, 3D AlloyDB/Spanner/BigQuery database cylinders, Rhombus decision gates,
     ADK Hexagon agents, Pub/Sub & OpenTelemetry nodes).
   - 23 connected orthogonal edges using the Typed 6-Color Connector Palette (#2563EB solid blue, #7C3AED dashed purple,
     #EA580C dashed orange, #16A34A solid green, #0D9488 closed-loop teal, #64748B governance slate) with opaque
     high-contrast pill badges (①..⑦, 3a..3b, 4a..4d) routed in dedicated 52px-80px channels so zero lines cross text.
2. `linkedin-infographic-2d.svg` (1600x1200):
   - Bespoke, post-specific 2D visual topology matching the exact mechanism of each post (Trajectory Replay Diff &
     Dual Rhombus Gates for POST-01; 10-Layer Radial/Bento Harness OS for POST-02; 5-Repo Multi-Agent Switchboard for
     POST-03; 6-Stage OpenHands Container Sandbox & Subagent Loop for POST-04; 3-Swimlane Safe vs. Indirect Prompt
     Injection Attack & Model Armor Defense for POST-05; 9-File IDE Repo Tree & 3-Tier Context Router for POST-06;
     OpenWiki Claim-to-SHA Receipt Graph, O(1) Diamond & 80->9 Bar Charts for POST-07; 6-Step Core Agent Loop Enclave
     with Rhombus Stopping Gate & 5 Guardrail Pods for POST-08).
"""

from __future__ import annotations

import base64
import html
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _esc(val: Any) -> str:
    return html.escape(str(val or ""), quote=True)


def _wrap(text: str, width: int, max_lines: int = 2) -> List[str]:
    clean = str(text or "").strip()
    if not clean:
        return [""]
    lines = textwrap.wrap(clean, width=width, break_long_words=False, break_on_hyphens=False)
    if len(lines) > max_lines and max_lines >= 1:
        for w_try in (int(width * 1.14), int(width * 1.28), int(width * 1.42)):
            retry = textwrap.wrap(clean, width=max(width + 2, w_try), break_long_words=False, break_on_hyphens=False)
            if len(retry) <= max_lines:
                return retry
        lines = lines[:max_lines]
    return lines or [""]


# Authentic inline SVG vector icon paths for Google Cloud & Agentic components (Pillar 8: Zero Emojis)
def _render_vector_icon(kind: str, x: int, y: int) -> str:
    """Render a crisp 28x28 vector service icon at (x, y)."""
    if kind == "shield":  # Cloud Armor / Model Armor
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#E8F0FE" stroke="#4285F4" stroke-width="1.2"/>'
            '<path d="M14 5 L22 8.5 V14.5 C22 19.2 18.6 22.8 14 24 C9.4 22.8 6 19.2 6 14.5 V8.5 Z" fill="#4285F4"/>'
            '<path d="M14 7.5 V21.5 C17.2 20.4 19.5 17.7 19.5 14.3 V10 L14 7.5 Z" fill="#174EA6"/>'
            "</g>"
        )
    if kind == "gemini":  # Vertex AI Gemini 4-point star
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#F3E8FF" stroke="#7C3AED" stroke-width="1.2"/>'
            '<path d="M14 4 C14.8 10.2 17.8 13.2 24 14 C17.8 14.8 14.8 17.8 14 24 C13.2 17.8 10.2 14.8 4 14 C10.2 13.2 13.2 10.2 14 4 Z" fill="#7C3AED"/>'
            "</g>"
        )
    if kind == "hexagon":  # Google ADK / A2A Agent Hexagon
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#FEF7E0" stroke="#FBBC04" stroke-width="1.2"/>'
            '<polygon points="14,4 23,9 23,19 14,24 5,19 5,9" fill="#F59E0B" stroke="#B45309" stroke-width="1.2"/>'
            '<circle cx="14" cy="14" r="3.5" fill="#FFFFFF"/>'
            "</g>"
        )
    if kind == "cylinder":  # AlloyDB / Spanner / BigQuery / Firestore 3D Cylinder
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#FCE8E6" stroke="#EA4335" stroke-width="1.2"/>'
            '<path d="M7 9 C7 6.8 21 6.8 21 9 V19 C21 21.2 7 21.2 7 19 Z" fill="#EA4335"/>'
            '<ellipse cx="14" cy="9" rx="7" ry="2.6" fill="#F87171" stroke="#991B1B" stroke-width="1"/>'
            '<path d="M7 14 C7 16 21 16 21 14" fill="none" stroke="#FFFFFF" stroke-width="1"/>'
            "</g>"
        )
    if kind == "key":  # KMS / IAM / WIF / CASG
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#E6F4EA" stroke="#34A853" stroke-width="1.2"/>'
            '<circle cx="10.5" cy="14" r="4.2" fill="none" stroke="#1E8E3E" stroke-width="2.2"/>'
            '<path d="M14.5 14 H23 M19.5 14 V17.5 M22.5 14 V17.5" stroke="#1E8E3E" stroke-width="2.2" stroke-linecap="round"/>'
            "</g>"
        )
    if kind == "diamond":  # Decision Gate / Competence Gate / Circuit Breaker
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#E6F4EA" stroke="#16A34A" stroke-width="1.2"/>'
            '<polygon points="14,4 24,14 14,24 4,14" fill="#16A34A"/>'
            '<path d="M10.5 14 L13 16.5 L18 11.5" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>'
            "</g>"
        )
    if kind == "sandbox":  # OpenHands / Cloud Run Container Sandbox
        return (
            f'<g transform="translate({x},{y})">'
            '<rect width="28" height="28" rx="6" fill="#E0F2FE" stroke="#0284C7" stroke-width="1.2"/>'
            '<rect x="5" y="6" width="18" height="16" rx="2.5" fill="#0284C7"/>'
            '<path d="M9 11 L12.5 14 L9 17 M14 17 H19" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>'
            "</g>"
        )
    # Default: Cloud Run / Network Load Balancer Router
    return (
        f'<g transform="translate({x},{y})">'
        '<rect width="28" height="28" rx="6" fill="#E8F0FE" stroke="#2563EB" stroke-width="1.2"/>'
        '<circle cx="8" cy="14" r="2.8" fill="#2563EB"/>'
        '<circle cx="20" cy="8.5" r="2.8" fill="#1D4ED8"/>'
        '<circle cx="20" cy="19.5" r="2.8" fill="#1D4ED8"/>'
        '<path d="M10.5 13 L17.5 9.5 M10.5 15 L17.5 18.5" stroke="#2563EB" stroke-width="1.8"/>'
        "</g>"
    )


def _draw_service_card(
    x: int,
    y: int,
    w: int,
    h: int,
    code_badge: str,
    title: str,
    subtitle: str,
    tech_meta: str,
    border_color: str,
    badge_bg: str,
    badge_fg: str,
    icon_kind: str,
) -> str:
    """Render an authentic, high-density Glassmorphic Google Cloud Architecture Center service card with vector icon."""
    t_lines = _wrap(title, width=max(15, (w - 56) // 6), max_lines=2)
    s_lines = _wrap(subtitle, width=max(24, (w - 22) // 5), max_lines=2 if h >= 130 else 1)
    m_lines = _wrap(tech_meta, width=max(24, (w - 22) // 5), max_lines=1)
    t_font = "9.5" if w < 175 else "10.2"

    out = [
        '<g class="arch-card">',
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="url(#glassCardGrad)" stroke="{border_color}" stroke-width="1.8" filter="url(#dropShadow)"/>',
        f'  <rect x="{x + 1.2:.1f}" y="{y + 1.2:.1f}" width="{w - 2.4:.1f}" height="{h - 2.4:.1f}" rx="7" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
        f'  <rect x="{x + 6}" y="{y + 1.5:.1f}" width="{w - 8}" height="12" rx="5" fill="url(#glassSheen)"/>',
        f'  <rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{border_color}"/>',
        f'  {_render_vector_icon(icon_kind, x + 14, y + 12)}',
        f'  <rect x="{x + 48}" y="{y + 11}" width="{min(86, w - 56)}" height="16" rx="4" fill="{badge_bg}" stroke="{border_color}" stroke-width="0.8"/>',
        f'  <text x="{x + 48 + min(86, w - 56) // 2}" y="{y + 22}" font-family="Inter, -apple-system, sans-serif" font-size="8.5" font-weight="800" fill="{badge_fg}" text-anchor="middle">{_esc(code_badge)}</text>',
    ]
    for idx, tl in enumerate(t_lines):
        out.append(
            f'  <text x="{x + 48}" y="{y + 39 + idx * 13}" font-family="Inter, -apple-system, sans-serif" font-size="{t_font}" font-weight="800" fill="#0F172A">{_esc(tl)}</text>'
        )
    if h >= 130:
        box_y = y + 62
        box_h = h - 72
        out.append(
            f'  <rect x="{x + 12}" y="{box_y}" width="{w - 22}" height="{box_h}" rx="6" fill="#F8FAFC" fill-opacity="0.88" stroke="#E2E8F0" stroke-width="1"/>'
        )
        for s_idx, sl in enumerate(s_lines):
            out.append(
                f'  <text x="{x + 18}" y="{box_y + 18 + s_idx * 14}" font-family="Inter, -apple-system, sans-serif" font-size="9.5" font-weight="600" fill="#334155">{_esc(sl)}</text>'
            )
        out.append(
            f'  <rect x="{x + 18}" y="{y + h - 32}" width="{w - 34}" height="16" rx="4" fill="{badge_bg}"/>'
        )
        out.append(
            f'  <text x="{x + 24}" y="{y + h - 21}" font-family="ui-monospace, SFMono-Regular, monospace" font-size="8.5" font-weight="700" fill="{badge_fg}">{_esc(m_lines[0])}</text>'
        )
    else:
        sub_y = y + h - 22
        out.append(
            f'  <line x1="{x + 12}" y1="{sub_y - 11}" x2="{x + w - 12}" y2="{sub_y - 11}" stroke="#E2E8F0" stroke-width="1"/>'
        )
        out.append(
            f'  <text x="{x + 14}" y="{sub_y}" font-family="Inter, -apple-system, sans-serif" font-size="9.5" font-weight="600" fill="#334155">{_esc(s_lines[0])}</text>'
        )
        out.append(
            f'  <text x="{x + 14}" y="{sub_y + 13}" font-family="ui-monospace, SFMono-Regular, monospace" font-size="8.5" font-weight="700" fill="{badge_fg}">{_esc(m_lines[0])}</text>'
        )
    out.append("</g>")
    return "\n".join(out)


def _draw_edge_with_pill(
    points: List[Tuple[int, int]],
    step_num: str,
    label: str,
    color: str,
    dashed: bool = False,
    marker: str = "arrowBlue",
    pill_pos: Tuple[int, int] | None = None,
) -> str:
    """Render an orthogonal or straight point-to-point glassmorphic connector with an opaque high-contrast label pill and baked zero-origin arrowhead."""
    import math as _math

    d_parts = [f"M {points[0][0]} {points[0][1]}"]
    for px, py in points[1:]:
        d_parts.append(f"L {px} {py}")
    d_str = " ".join(d_parts)
    dash_attr = ' stroke-dasharray="6,4"' if dashed else ""

    baked_arrow = ""
    if len(points) >= 2:
        (x1, y1), (x2, y2) = points[-2], points[-1]
        ang = _math.atan2(y2 - y1, x2 - x1)
        ca, sa = _math.cos(ang), _math.sin(ang)
        raw_head = ((0.0, 0.0), (-9.0, -4.5), (-7.0, 0.0), (-9.0, 4.5))
        pts_str = " ".join(
            f"{x2 + px * ca - py * sa:.1f},{y2 + px * sa + py * ca:.1f}"
            for px, py in raw_head
        )
        baked_arrow = f'<polygon points="{pts_str}" fill="{color}"/>'

    if pill_pos is not None:
        mx, my = pill_pos
    else:
        mid_idx = len(points) // 2
        p1, p2 = points[mid_idx - 1], points[mid_idx]
        mx, my = (p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2

    pill_w = max(78, len(label) * 5 + 34)
    pill_h = 20
    px0 = mx - pill_w // 2
    py0 = my - pill_h // 2

    out_lines = [
        f'<path d="{d_str}" fill="none" stroke="{color}" stroke-opacity="0.14" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d_str}" fill="none" stroke="#FFFFFF" stroke-opacity="0.76" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d_str}" fill="none" stroke="{color}" stroke-width="2"{dash_attr} marker-end="url(#{marker})"/>',
    ]
    if baked_arrow:
        out_lines.append(baked_arrow)
    out_lines.extend(
        [
            f'<rect x="{px0}" y="{py0}" width="{pill_w}" height="{pill_h}" rx="5" fill="#FFFFFF" fill-opacity="0.96" stroke="{color}" stroke-width="1.2"/>',
            f'<rect x="{px0 + 2}" y="{py0 + 1.2:.1f}" width="{pill_w - 4}" height="7" rx="3" fill="#FFFFFF" fill-opacity="0.42"/>',
            f'<rect x="{px0 + 3}" y="{py0 + 3}" width="22" height="14" rx="3" fill="{color}"/>',
            f'<text x="{px0 + 14}" y="{py0 + 13}" font-family="Inter, sans-serif" font-size="8.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">{_esc(step_num)}</text>',
            f'<text x="{px0 + 30}" y="{py0 + 13.5}" font-family="Inter, sans-serif" font-size="8.5" font-weight="700" fill="#0F172A">{_esc(label)}</text>',
        ]
    )
    return "\n".join(out_lines)


def generate_gcp_arch_78_svg(post: Dict[str, Any]) -> str:
    """Render the 1600x1020 Official Google Cloud Architecture Center #78 18-Card, 23-Edge Glassmorphic Blueprint."""
    z = post["zones_78"]
    steps = post["core_steps"]
    metrics = list(post["metrics"].items())
    title_clean = _wrap(post["post_title"], width=94, max_lines=1)[0]
    primary_clean = _wrap(post["primary_source"]["title"], width=78, max_lines=1)[0]

    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1020" width="1600" height="1020">',
        "<defs>",
        '  <filter id="dropShadow" x="-3%" y="-3%" width="106%" height="110%">',
        '    <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.065"/>',
        "  </filter>",
        '  <linearGradient id="glassCardGrad" x1="0" y1="0" x2="0" y2="1">',
        '    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>',
        '    <stop offset="100%" stop-color="#F8FAFC" stop-opacity="0.91"/>',
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
        '  <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#2563EB"/></marker>',
        '  <marker id="arrowPurple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#7C3AED"/></marker>',
        '  <marker id="arrowOrange" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#EA580C"/></marker>',
        '  <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#16A34A"/></marker>',
        '  <marker id="arrowTeal" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#0D9488"/></marker>',
        '  <marker id="arrowSlate" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#475569"/></marker>',
        "</defs>",
        '<!-- Root Canvas: Rule 54 Executive Light (#F8FAFC) + Ambient Glassmorphic Mesh -->',
        '<rect x="0" y="0" width="1600" height="1020" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="1600" height="1020" fill="url(#meshBlue)"/>',
        '<rect x="0" y="0" width="1600" height="1020" fill="url(#meshEmerald)"/>',
        '<rect x="0" y="0" width="1600" height="1020" fill="url(#meshViolet)"/>',
        '<rect x="0" y="0" width="1600" height="1020" fill="url(#archGrid)"/>',
        '<!-- Top Google Cloud Architecture Center Header Lockup -->',
        '<rect x="24" y="16" width="1552" height="62" rx="10" fill="#0F2942" stroke="#1A73E8" stroke-width="1.5" filter="url(#dropShadow)"/>',
        '<rect x="26" y="17.5" width="1548" height="14" rx="7" fill="#FFFFFF" fill-opacity="0.10"/>',
        '<!-- Official 4-Color Google Cloud Emblem -->',
        '<circle cx="52" cy="47" r="7" fill="#EA4335"/>',
        '<circle cx="64" cy="40" r="7" fill="#4285F4"/>',
        '<circle cx="76" cy="47" r="7" fill="#34A853"/>',
        '<rect x="52" y="47" width="24" height="7" rx="3" fill="#FBBC04"/>',
        f'<text x="96" y="42" font-family="Inter, sans-serif" font-size="15.5" font-weight="800" fill="#FFFFFF">GOOGLE CLOUD ARCHITECTURE CENTER • TEMPLATE #78 HUB-AND-SPOKE BLUEPRINT ({_esc(post["id"])})</text>',
        f'<text x="96" y="62" font-family="Inter, sans-serif" font-size="11.5" font-weight="600" fill="#93C5FD">{_esc(title_clean)}  |  Lineage: {_esc(post["author_name"])} ({_esc(post["activity_urn"])})</text>',
        '<rect x="1320" y="31" width="236" height="32" rx="6" fill="#1E8E3E" stroke="#86EFAC" stroke-width="1"/>',
        '<text x="1438" y="51" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">18/18 CARDS • 23 EDGES • 0 COLLISIONS</text>',
        '<!-- Outer #1A73E8 Google Cloud Organization & VPC-SC Trust Perimeter Frame -->',
        '<rect x="24" y="92" width="1552" height="836" rx="14" fill="#FFFFFF" fill-opacity="0.78" stroke="#1A73E8" stroke-width="2.5" filter="url(#dropShadow)"/>',
        '<rect x="25.5" y="93.5" width="1549" height="833" rx="13" fill="none" stroke="#FFFFFF" stroke-opacity="0.88" stroke-width="1.2"/>',
        '<rect x="44" y="104" width="380" height="24" rx="5" fill="#E8F0FE" fill-opacity="0.95" stroke="#4285F4" stroke-width="1"/>',
        '<text x="234" y="120" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#174EA6" text-anchor="middle">GOOGLE CLOUD ORGANIZATION • VPC SERVICE CONTROLS PERIMETER</text>',
    ]

    # Top Actor / Client & Developer Ingress Strip (x=450..1150, y=100..146)
    svg.extend(
        [
            '<rect x="460" y="100" width="680" height="44" rx="8" fill="url(#glassCardGrad)" stroke="#94A3B8" stroke-width="1.5" filter="url(#dropShadow)"/>',
            '<rect x="461.2" y="101.2" width="677.6" height="41.6" rx="7" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            _render_vector_icon("router", 474, 108),
            '<text x="512" y="119" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0F172A">EXTERNAL ACTOR / PRINCIPAL ENGINEER &amp; ENTERPRISE CLIENT WORKLOADS</text>',
            f'<text x="512" y="134" font-family="ui-monospace, monospace" font-size="9.5" font-weight="600" fill="#475569">Repo: generated-repos/{_esc(post["repo_slug"])}  •  Model Routing: locations/global (gemini-4-argon)</text>',
        ]
    )

    # =========================================================================
    # ZONE 1 (#AECBFA Pastel Blue): Tenant-Aware Routing & Edge Security Hub (5 Cards)
    # Bounds: x=44, y=164, w=976, h=226
    # =========================================================================
    svg.extend(
        [
            '<rect x="44" y="164" width="976" height="226" rx="12" fill="#EFF6FF" fill-opacity="0.88" stroke="#AECBFA" stroke-width="2.5" filter="url(#dropShadow)"/>',
            '<rect x="45.5" y="165.5" width="973" height="223" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="44" y="164" width="976" height="32" rx="10" fill="#AECBFA"/>',
            '<rect x="46" y="165.5" width="972" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.32"/>',
            '<text x="64" y="185" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#174EA6">ZONE 1 (BLUE HUB) • TENANT-AWARE ROUTING, ZERO-TRUST INGRESS &amp; CONTEXT ENGINEERING HUB</text>',
            '<text x="1002" y="185" font-family="ui-monospace, monospace" font-size="10" font-weight="800" fill="#174EA6" text-anchor="end">vpc-hub-routing • 10.10.0.0/20</text>',
        ]
    )

    z1_cards = [
        ("EDGE-01", z["blue_routing"][0], "L7 WAF & Adaptive DDoS", "CRS 3.3 • TLS 1.3", "shield"),
        ("AUTH-02", "Identity Platform & WIF", "OIDC & Workload Identity", "SPIFFE • Short-Lived JWT", "key"),
        ("IAP-03", z["blue_routing"][1], "BeyondCorp Context Guard", "mTLS • Device Posture", "shield"),
        ("ALB-04", "Regional External ALB", "Global Anycast Ingress", "HTTPS :443 • QUIC/HTTP3", "router"),
        ("ING-05", z["blue_routing"][2], "Cloud Run Edge Proxy", "KV-Cache Prefix Router", "sandbox"),
    ]
    for idx, (c_badge, c_title, c_sub, c_meta, c_icon) in enumerate(z1_cards):
        cx = 58 + idx * 191
        svg.append(
            _draw_service_card(
                x=cx,
                y=210,
                w=179,
                h=162,
                code_badge=c_badge,
                title=c_title,
                subtitle=c_sub,
                tech_meta=c_meta,
                border_color="#4285F4",
                badge_bg="#E8F0FE",
                badge_fg="#174EA6",
                icon_kind=c_icon,
            )
        )

    # =========================================================================
    # ZONE 2 (#CEEAD6 Pastel Green): Central Governance, KMS, Model Armor & Audit Hub (3 Cards)
    # Bounds: x=1044, y=164, w=512, h=226
    # =========================================================================
    svg.extend(
        [
            '<rect x="1044" y="164" width="512" height="226" rx="12" fill="#F0FDF4" fill-opacity="0.88" stroke="#CEEAD6" stroke-width="2.5" filter="url(#dropShadow)"/>',
            '<rect x="1045.5" y="165.5" width="509" height="223" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="1044" y="164" width="512" height="32" rx="10" fill="#CEEAD6"/>',
            '<rect x="1046" y="165.5" width="508" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.32"/>',
            '<text x="1062" y="185" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0D652D">ZONE 2 (GREEN HUB) • GOVERNANCE, KMS &amp; EVAL GATE</text>',
        ]
    )
    z2_cards = [
        ("GOV-06", z["green_governance"][0], "Cloud KMS HSM & VPC-SC", "FIPS 140-3 • CMEK", "key"),
        ("GOV-07", z["green_governance"][1], "Competence & Eval Gate", "Fail-Closed • 0 Drift", "diamond"),
        ("GOV-08", z["green_governance"][2], "Cloud Logging & OTel", "SHA-256 Receipt Log", "cylinder"),
    ]
    for idx, (c_badge, c_title, c_sub, c_meta, c_icon) in enumerate(z2_cards):
        cx = 1056 + idx * 165
        svg.append(
            _draw_service_card(
                x=cx,
                y=210,
                w=155,
                h=162,
                code_badge=c_badge,
                title=c_title,
                subtitle=c_sub,
                tech_meta=c_meta,
                border_color="#34A853",
                badge_bg="#E6F4EA",
                badge_fg="#0D652D",
                icon_kind=c_icon,
            )
        )

    # =========================================================================
    # ZONE 3 (#FEEFC3 Warm Yellow): Primary ADK Agent & Frontier Gemini Spoke (5 Cards)
    # Bounds: x=44, y=446, w=736, h=380 (with 94px Intra-Spoke Routing Corridor)
    # =========================================================================
    svg.extend(
        [
            '<rect x="44" y="446" width="736" height="380" rx="12" fill="#FEFCE8" fill-opacity="0.88" stroke="#FEEFC3" stroke-width="2.5" filter="url(#dropShadow)"/>',
            '<rect x="45.5" y="447.5" width="733" height="377" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="44" y="446" width="736" height="32" rx="10" fill="#FEEFC3"/>',
            '<rect x="46" y="447.5" width="732" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.34"/>',
            '<text x="64" y="467" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#B06000">ZONE 3 (LEFT SPOKE) • PRIMARY GOOGLE ADK &amp; VERTEX AI GEMINI SPOKE</text>',
            '<text x="764" y="467" font-family="ui-monospace, monospace" font-size="10" font-weight="800" fill="#B06000" text-anchor="end">spoke-adk-primary • 10.20.0.0/20</text>',
        ]
    )
    # Left column in Zone 3 (x=62, w=300): Cards 9 & 10
    svg.append(
        _draw_service_card(
            x=62,
            y=494,
            w=300,
            h=142,
            code_badge="ARMOR-09",
            title="Google Cloud Model Armor & DLP Guard",
            subtitle=f"Stage 1: {steps[0]['title']} & Sanitization",
            tech_meta="OWASP LLM01 • Prompt Injection Block",
            border_color="#F59E0B",
            badge_bg="#FEF7E0",
            badge_fg="#B06000",
            icon_kind="shield",
        )
    )
    svg.append(
        _draw_service_card(
            x=62,
            y=666,
            w=300,
            h=142,
            code_badge="GEMINI-10",
            title="Vertex AI Gemini 4 Argon (Global)",
            subtitle=f"Stage 2: {steps[1]['title']}",
            tech_meta="locations/global • thinkingLevel=HIGH",
            border_color="#7C3AED",
            badge_bg="#F3E8FF",
            badge_fg="#6D28D9",
            icon_kind="gemini",
        )
    )
    # Right column in Zone 3 (x=456, w=306) leaving x=362..456 (94px open intra-spoke channel!): Cards 11, 12, 13
    svg.append(
        _draw_service_card(
            x=456,
            y=494,
            w=306,
            h=98,
            code_badge="ADK-11",
            title=z["yellow_compute"][0],
            subtitle=f"Stage 3: {steps[2]['title']}",
            tech_meta="Google ADK Runtime • Cloud Run Gen2",
            border_color="#F59E0B",
            badge_bg="#FEF7E0",
            badge_fg="#B06000",
            icon_kind="hexagon",
        )
    )
    svg.append(
        _draw_service_card(
            x=456,
            y=604,
            w=306,
            h=98,
            code_badge="TOOL-12",
            title=z["yellow_compute"][1],
            subtitle=f"Stage 4: {steps[3]['title']}",
            tech_meta="CASG Scoped JWT • MCP Tool Bus",
            border_color="#0284C7",
            badge_bg="#E0F2FE",
            badge_fg="#0369A1",
            icon_kind="sandbox",
        )
    )
    svg.append(
        _draw_service_card(
            x=456,
            y=714,
            w=306,
            h=98,
            code_badge="STATE-13",
            title=z["yellow_compute"][2],
            subtitle="AlloyDB FORCE RLS & Vector Search 2.0",
            tech_meta="ScaNN p99 < 2.5ms • CMEK Vault",
            border_color="#059669",
            badge_bg="#DCFCE7",
            badge_fg="#065F46",
            icon_kind="cylinder",
        )
    )

    # =========================================================================
    # ZONE 4 (#FAD2CF Coral): OpenHands Autonomous Sandbox, Memory & Lakehouse Spoke (5 Cards)
    # Bounds: x=820, y=446, w=736, h=380 (with 94px Intra-Spoke Routing Corridor)
    # =========================================================================
    svg.extend(
        [
            '<rect x="820" y="446" width="736" height="380" rx="12" fill="#FEF2F2" fill-opacity="0.88" stroke="#FAD2CF" stroke-width="2.5" filter="url(#dropShadow)"/>',
            '<rect x="821.5" y="447.5" width="733" height="377" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="820" y="446" width="736" height="32" rx="10" fill="#FAD2CF"/>',
            '<rect x="822" y="447.5" width="732" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.34"/>',
            '<text x="840" y="467" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#A50E0E">ZONE 4 (RIGHT SPOKE) • OPENHANDS SANDBOX, MEMORY &amp; LAKEHOUSE SPOKE</text>',
            '<text x="1540" y="467" font-family="ui-monospace, monospace" font-size="10" font-weight="800" fill="#A50E0E" text-anchor="end">spoke-openhands-data • 10.30.0.0/20</text>',
        ]
    )
    # Left column in Zone 4 (x=838, w=300): Cards 14 & 15
    svg.append(
        _draw_service_card(
            x=838,
            y=494,
            w=300,
            h=142,
            code_badge="OH-14",
            title="OpenHands CodeActAgent Sandbox",
            subtitle=f"Stage 5: {steps[4]['title']}",
            tech_meta="Isolated Container • Pytest & AST Verifier",
            border_color="#EA4335",
            badge_bg="#FCE8E6",
            badge_fg="#A50E0E",
            icon_kind="sandbox",
        )
    )
    svg.append(
        _draw_service_card(
            x=838,
            y=666,
            w=300,
            h=142,
            code_badge="JUDGE-15",
            title="Vertex AI Gemini 3.8 Flash Judge",
            subtitle=f"Stage 6: {steps[5]['title']}",
            tech_meta="locations/global • thinkingLevel=MEDIUM",
            border_color="#7C3AED",
            badge_bg="#F3E8FF",
            badge_fg="#6D28D9",
            icon_kind="gemini",
        )
    )
    # Right column in Zone 4 (x=1232, w=306) leaving x=1138..1232 (94px open intra-spoke channel): Cards 16, 17, 18
    svg.append(
        _draw_service_card(
            x=1232,
            y=494,
            w=306,
            h=98,
            code_badge="DATA-16",
            title=z["red_data"][0],
            subtitle="Firestore Claim-to-Code-SHA Graph",
            tech_meta="O(1) Version Receipt • 0 Drift",
            border_color="#EA4335",
            badge_bg="#FCE8E6",
            badge_fg="#A50E0E",
            icon_kind="cylinder",
        )
    )
    svg.append(
        _draw_service_card(
            x=1232,
            y=604,
            w=306,
            h=98,
            code_badge="DATA-17",
            title=z["red_data"][1],
            subtitle="BigQuery Trajectory & Eval Warehouse",
            tech_meta="BigLake Iceberg • 100% Lineage",
            border_color="#EA4335",
            badge_bg="#FCE8E6",
            badge_fg="#A50E0E",
            icon_kind="cylinder",
        )
    )
    svg.append(
        _draw_service_card(
            x=1232,
            y=714,
            w=306,
            h=98,
            code_badge="REG-18",
            title=z["red_data"][2],
            subtitle="Artifact Registry & Git Commit Ledger",
            tech_meta="Signed Container & Terraform State",
            border_color="#0D9488",
            badge_bg="#CCFBF1",
            badge_fg="#115E59",
            icon_kind="key",
        )
    )

    # =========================================================================
    # ZONE 5 (Bottom Baseline): 6-Pillar Zero-Trust, FinOps & Production Telemetry Strip
    # Bounds: x=44, y=840, w=1512, h=74
    # =========================================================================
    svg.extend(
        [
            '<rect x="44" y="840" width="1512" height="74" rx="10" fill="#F1F5F9" fill-opacity="0.90" stroke="#CBD5E1" stroke-width="1.5" filter="url(#dropShadow)"/>',
            '<rect x="45.2" y="841.2" width="1509.6" height="71.6" rx="9" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="56" y="852" width="220" height="50" rx="6" fill="#0F2942"/>',
            '<text x="166" y="874" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">ZONE 5 • PRODUCTION TELEMETRY</text>',
            f'<text x="166" y="891" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#93C5FD" text-anchor="middle">1-Click Terraform • { _esc(post["id"]) }</text>',
        ]
    )
    for m_idx, (m_k, m_v) in enumerate(metrics[:4]):
        mx = 292 + m_idx * 312
        accent = ["#4285F4", "#EA4335", "#FBBC04", "#34A853"][m_idx % 4]
        svg.extend(
            [
                f'<rect x="{mx}" y="852" width="296" height="50" rx="6" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.2"/>',
                f'<rect x="{mx}" y="852" width="6" height="50" rx="3" fill="{accent}"/>',
                f'<text x="{mx + 18}" y="871" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#475569">{_esc(m_k.replace("_", " ").upper())}</text>',
                f'<text x="{mx + 18}" y="892" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="#0F172A">{_esc(m_v)}</text>',
            ]
        )

    # =========================================================================
    # TYPED 6-COLOR CONNECTOR HIGHWAYS & NUMBERED CALLOUT PILLS (①..⑦, 3a..3b, 4a..4d)
    # Routed strictly inside open corridors (y=144..164, y=390..446, x=362..456, x=780..820, x=1138..1232)
    # =========================================================================
    svg.extend(
        [
            # ① Actor -> Zone 1 Ingress
            _draw_edge_with_pill([(580, 144), (580, 164)], "①", "HTTPS :443 Request", "#2563EB", False, "arrowBlue", (450, 154)),
            # ⑦ Zone 1 -> Actor Response
            _draw_edge_with_pill([(910, 164), (910, 144)], "⑦", "Verified Response", "#0D9488", False, "arrowTeal", (1026, 154)),
            # ② Intra-Zone 1 Pipeline (Cards 1->2->3->4->5)
            '<line x1="237" y1="290" x2="249" y2="290" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>',
            '<line x1="428" y1="290" x2="440" y2="290" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>',
            '<line x1="619" y1="290" x2="631" y2="290" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>',
            '<line x1="810" y1="290" x2="822" y2="290" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>',
            # 3a Zone 1 -> Zone 2 Governance Check (across x=1020..1056)
            _draw_edge_with_pill([(910, 390), (910, 412), (1130, 412), (1130, 390)], "3a", "KMS & Policy Check", "#16A34A", True, "arrowGreen", (1020, 412)),
            # ③ Zone 1 ALB/Edge -> Zone 3 Model Armor (via y=418 corridor)
            _draw_edge_with_pill([(720, 390), (720, 418), (212, 418), (212, 446)], "②", "Route & Context", "#2563EB", False, "arrowBlue", (466, 418)),
            # ④ Zone 3 Model Armor -> ADK Orchestrator (across 94px channel x=362..456)
            _draw_edge_with_pill([(362, 540), (454, 540)], "④", "Sanitized Prompt", "#7C3AED", False, "arrowPurple", (408, 524)),
            # ⑤ Zone 3 Gemini 4 Argon <-> ADK Orchestrator (staggered elbow in x=362..456 channel)
            _draw_edge_with_pill([(456, 568), (408, 568), (408, 736), (362, 736)], "⑤", "thinkingLevel=HIGH", "#7C3AED", True, "arrowPurple", (408, 690)),
            # ⑥ ADK -> Tool Sandbox -> Primary State Store
            '<line x1="609" y1="592" x2="609" y2="602" stroke="#2563EB" stroke-width="2" marker-end="url(#arrowBlue)"/>',
            '<line x1="609" y1="702" x2="609" y2="712" stroke="#16A34A" stroke-width="2" marker-end="url(#arrowGreen)"/>',
            # 4a Zone 3 -> Zone 4 OpenHands Sandbox (across inter-spoke channel x=762..838)
            _draw_edge_with_pill([(762, 540), (836, 540)], "4a", "A2A Sandbox Task", "#EA580C", True, "arrowOrange", (800, 514)),
            # 4b Zone 4 OpenHands Sandbox -> Data/Receipt Graph (across 94px channel x=1138..1232)
            _draw_edge_with_pill([(1138, 540), (1230, 540)], "4b", "SHA-256 Receipt", "#16A34A", False, "arrowGreen", (1184, 524)),
            # 4c Zone 4 Gemini 3.8 Flash Judge -> BigQuery Eval Warehouse
            _draw_edge_with_pill([(1138, 736), (1184, 736), (1184, 652), (1230, 652)], "4c", "Eval Trace Sink", "#7C3AED", True, "arrowPurple", (1184, 696)),
            # 3b Zone 2 Competence Gate -> Zone 4 OpenHands & Registry
            _draw_edge_with_pill([(1300, 390), (1300, 418), (988, 418), (988, 446)], "3b", "Competence Gate", "#16A34A", True, "arrowGreen", (1144, 418)),
            # ⑥ Closed-Loop Verified Return from Zone 4 Judge/Registry -> Zone 3 State across y=651 inter-spoke gap
            _draw_edge_with_pill([(838, 651), (764, 651)], "⑥", "Verified Loop", "#0D9488", True, "arrowTeal", (800, 651)),
        ]
    )

    # Bottom Attribution & Primary Source Footer
    svg.extend(
        [
            '<rect x="24" y="942" width="1552" height="58" rx="10" fill="#0F2942" filter="url(#dropShadow)"/>',
            '<rect x="26" y="943.5" width="1548" height="12" rx="6" fill="#FFFFFF" fill-opacity="0.10"/>',
            f'<text x="48" y="967" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="#FFFFFF">PRIMARY SOURCE GROUNDING: {_esc(primary_clean)}  |  CURATED BY: NITIN AGGARWAL (linkedin.com/in/nitin-aggarwal-b49786a)</text>',
            f'<text x="48" y="987" font-family="ui-monospace, monospace" font-size="11" font-weight="600" fill="#93C5FD">1-Click Google Cloud Deploy: cd generated-repos/{_esc(post["repo_slug"])}/terraform &amp;&amp; terraform init &amp;&amp; terraform apply -var="project_id=nitina-ggarwal-sandbox-647724"</text>',
            '<text x="1552" y="977" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#86EFAC" text-anchor="end">Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    from src.visuals.template_gallery import flatten_svg_zero_origin

    return flatten_svg_zero_origin("\n".join(svg))


def _render_post_specific_centerpiece(post: Dict[str, Any]) -> str:
    """Render a bespoke, domain-native 2D visual architecture centerpiece (y=260..790) for each of the 8 posts."""
    pid = post["id"]

    if pid == "POST-01":
        # HarnessEvolve: Parallel Trajectory Replay Diff (Failed vs. Clean Path) + Clustering + 2 Rhombus Competence Gates
        return """
        <g id="bespoke-post-01">
          <rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>
          <rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>
          <text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. HARNESSEVOLVE TRAJECTORY REPLAY DIFF, FAILURE CLUSTERING &amp; DUAL COMPETENCE GATE ARCHITECTURE</text>

          <!-- Swimlane A: Failed Production Trajectory (Crimson) -->
          <rect x="58" y="316" width="840" height="148" rx="10" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="2"/>
          <text x="76" y="340" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#991B1B">PATH A • FAILED AGENT TRAJECTORY (WITHOUT ANSWER IN HAND)</text>
          <rect x="76" y="356" width="176" height="86" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="88" y="378" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F172A">Step 1: Parse Goal [OK]</text>
          <text x="88" y="398" font-family="Inter, sans-serif" font-size="10" fill="#475569">Intent &amp; schema loaded</text>
          <text x="88" y="424" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#16A34A">trace_span_01: PASS</text>

          <rect x="282" y="356" width="176" height="86" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="294" y="378" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F172A">Step 2: Plan Tools [OK]</text>
          <text x="294" y="398" font-family="Inter, sans-serif" font-size="10" fill="#475569">Selected SQL &amp; API tool</text>
          <text x="294" y="424" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#16A34A">trace_span_02: PASS</text>

          <rect x="488" y="356" width="186" height="86" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="2.5"/>
          <text x="500" y="378" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#991B1B">Step 3: Tool Call [BROKEN]</text>
          <text x="500" y="398" font-family="Inter, sans-serif" font-size="10" fill="#7F1D1D">Wrong arg key: user_id</text>
          <text x="500" y="424" font-family="ui-monospace, monospace" font-size="9" font-weight="800" fill="#DC2626">ERR_SCHEMA_DRIFT</text>

          <rect x="702" y="356" width="176" height="86" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.8"/>
          <text x="714" y="378" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#991B1B">Step 4: Task Failed</text>
          <text x="714" y="398" font-family="Inter, sans-serif" font-size="10" fill="#7F1D1D">Scalar score = 0.0 (Blind)</text>
          <text x="714" y="424" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#DC2626">Unlocalized Failure</text>

          <!-- Swimlane B: Ground-Truth Replay Trajectory (Emerald) -->
          <rect x="58" y="514" width="840" height="148" rx="10" fill="#F0FDF4" stroke="#86EFAC" stroke-width="2"/>
          <text x="76" y="538" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#065F46">PATH B • HARNESSEVOLVE CLEAN REPLAY (WITH GROUND-TRUTH ANSWER IN HAND)</text>
          <rect x="76" y="554" width="176" height="86" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="88" y="576" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F172A">Step 1: Parse Goal [OK]</text>
          <text x="88" y="596" font-family="Inter, sans-serif" font-size="10" fill="#475569">Identical prefix state</text>
          <text x="88" y="622" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#16A34A">delta = 0.00</text>

          <rect x="282" y="554" width="176" height="86" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="294" y="576" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F172A">Step 2: Plan Tools [OK]</text>
          <text x="294" y="596" font-family="Inter, sans-serif" font-size="10" fill="#475569">Identical tool selection</text>
          <text x="294" y="622" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#16A34A">delta = 0.00</text>

          <rect x="488" y="554" width="186" height="86" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.5"/>
          <text x="500" y="576" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46">Step 3: Clean Tool Call</text>
          <text x="500" y="596" font-family="Inter, sans-serif" font-size="10" fill="#065F46">Uses account_uuid key</text>
          <text x="500" y="622" font-family="ui-monospace, monospace" font-size="9" font-weight="800" fill="#15803D">EXACT DIFF PINPOINTED</text>

          <rect x="702" y="554" width="176" height="86" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="714" y="576" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F172A">Step 4: Reference Match</text>
          <text x="714" y="596" font-family="Inter, sans-serif" font-size="10" fill="#475569">Feedback with footage</text>
          <text x="714" y="622" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#16A34A">96.4% Step Accuracy</text>

          <!-- Divergence Callout Pill between Step 3 Path A and Step 3 Path B -->
          <line x1="581" y1="442" x2="581" y2="554" stroke="#EA580C" stroke-width="3" stroke-dasharray="5,3"/>
          <rect x="466" y="476" width="230" height="26" rx="6" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.8"/>
          <text x="581" y="493" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#C2410C" text-anchor="middle">1. PRECISE ERROR SIGNAL AT STEP 3</text>

          <!-- Pillar 2 & 3 on Right Side: Failure Clustering + Dual Protected Competence Gates -->
          <rect x="932" y="316" width="276" height="148" rx="10" fill="#FEFCE8" stroke="#FACC15" stroke-width="2"/>
          <text x="950" y="340" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#B45309">2. REAL GENERALIZATION</text>
          <text x="950" y="364" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">Failure Pattern Clusterer</text>
          <text x="950" y="384" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Clusters 14 schema-drift traces into</text>
          <text x="950" y="400" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">1 reusable SKILL.md capability update</text>
          <rect x="950" y="416" width="240" height="28" rx="5" fill="#FFFFFF" stroke="#F59E0B" stroke-width="1.2"/>
          <text x="1070" y="434" font-family="ui-monospace, monospace" font-size="9.5" font-weight="800" fill="#B45309" text-anchor="middle">Capability vs. Benchmark Gaming</text>

          <rect x="1238" y="316" width="302" height="346" rx="10" fill="#F0FDF4" stroke="#34A853" stroke-width="2"/>
          <text x="1258" y="340" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0D652D">3. PROTECTED COMPETENCE GATES</text>

          <!-- Rhombus Gate 1 -->
          <polygon points="1389,362 1510,412 1389,462 1268,412" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.2"/>
          <text x="1389" y="408" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#1E3A8A" text-anchor="middle">QUALITY &amp; LEAK GATE</text>
          <text x="1389" y="424" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">Bloat &lt;= 15% • 0 Test Leaks</text>

          <!-- Rhombus Gate 2 -->
          <polygon points="1389,494 1510,544 1389,594 1268,544" fill="#FFFFFF" stroke="#16A34A" stroke-width="2.2"/>
          <text x="1389" y="540" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#065F46" text-anchor="middle">PERFORMANCE GATE</text>
          <text x="1389" y="556" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">Current +28.5% • Historical 100%</text>

          <rect x="1274" y="614" width="230" height="32" rx="6" fill="#16A34A"/>
          <text x="1389" y="634" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">[PROMOTE] COMPOUNDING FLYWHEEL</text>

          <!-- Closed-Loop Flywheel Return Highway -->
          <path d="M 1389 646 L 1389 716 L 164 716 L 164 642" fill="none" stroke="#0D9488" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrowTeal)"/>
          <rect x="590" y="702" width="380" height="28" rx="6" fill="#CCFBF1" stroke="#0D9488" stroke-width="1.5"/>
          <text x="780" y="720" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#115E59" text-anchor="middle">AUTONOMOUS SELF-IMPROVEMENT FLYWHEEL (0 REGRESSION DRIFT)</text>
        </g>
        """

    if pid == "POST-02":
        # Agent = Model + Harness: Central Foundation Model Core surrounded by 10 Engineered Harness Subsystems
        layers = [
            ("01. INSTRUCTIONS", "AGENTS.md / GEMINI.md", "Read every session start", "#4285F4"),
            ("02. REAL CONTEXT", "Product, Users & Schemas", "Vertex KV Context Cache", "#EA4335"),
            ("03. ON-DEMAND SKILLS", "skills/<name>/SKILL.md", "10 Laws of Modular Skills", "#FBBC04"),
            ("04. PERSISTENT MEMORY", "AlloyDB & Firestore", "Never correct agent twice", "#34A853"),
            ("05. PERMISSIONS GATE", "Auto-Mode RBAC Boundary", "Autonomous vs. HITL actions", "#4285F4"),
            ("06. MCP & CLI TOOLS", "Files, Terminal & MCP Bus", "GitHub, BigQuery, Sentry", "#EA4335"),
            ("07. PRE-CUSTOMER EVALS", "Deterministic + LLM Judge", "Grade before user sees output", "#FBBC04"),
            ("08. OBSERVABILITY", "Cloud Trace OpenTelemetry", "Token, latency & step spans", "#34A853"),
            ("09. CLOSED-LOOP ENGINE", "Verify -> Fix -> Retry", "Loops until all checks pass", "#7C3AED"),
            ("10. PRODUCTION PM/ENG OS", "End-to-End Agent System", "OpenAI to Ramp Case Studies", "#0D9488"),
        ]
        cards_svg = []
        for idx, (l_code, l_title, l_sub, l_col) in enumerate(layers):
            col = idx % 5
            row = idx // 5
            lx = 58 + col * 298
            ly = 324 if row == 0 else 638
            cards_svg.append(
                f'<rect x="{lx}" y="{ly}" width="282" height="118" rx="10" fill="#FFFFFF" stroke="{l_col}" stroke-width="2"/>'
                f'<rect x="{lx}" y="{ly}" width="282" height="26" rx="8" fill="{l_col}"/>'
                f'<text x="{lx + 14}" y="{ly + 17}" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF">{_esc(l_code)}</text>'
                f'<text x="{lx + 14}" y="{ly + 54}" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#0F172A">{_esc(l_title)}</text>'
                f'<text x="{lx + 14}" y="{ly + 76}" font-family="Inter, sans-serif" font-size="11" fill="#475569">{_esc(l_sub)}</text>'
                f'<text x="{lx + 14}" y="{ly + 100}" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="{l_col}">Harness Subsystem #{idx + 1}</text>'
            )
            # Connect to central core bar (y=480..596)
            cy_from = ly + 118 if row == 0 else ly
            cy_to = 480 if row == 0 else 596
            cards_svg.append(
                f'<line x1="{lx + 141}" y1="{cy_from}" x2="{lx + 141}" y2="{cy_to}" stroke="{l_col}" stroke-width="2" stroke-dasharray="4,3"/>'
            )

        return (
            '<g id="bespoke-post-02">'
            '<rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>'
            '<rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>'
            '<text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. AGENT = MODEL + HARNESS — THE 10-LAYER ENTERPRISE HARNESS ARCHITECTURE (ADDY OSMANI / AAKASH GUPTA)</text>'
            + "\n".join(cards_svg)
            + '<rect x="180" y="480" width="1240" height="116" rx="14" fill="#0F2942" stroke="#4285F4" stroke-width="3"/>'
            + _render_vector_icon("gemini", 210, 524)
            + '<text x="256" y="525" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">CENTRAL FOUNDATION MODEL CORE + GOOGLE CLOUD ADK HARNESS BUS</text>'
            + '<text x="256" y="550" font-family="Inter, sans-serif" font-size="12.5" font-weight="600" fill="#93C5FD">"A decent model with a great harness consistently beats a great model with a bad harness." — Addy Osmani (857K Views)</text>'
            + '<text x="256" y="574" font-family="ui-monospace, monospace" font-size="11" font-weight="700" fill="#86EFAC">Vertex AI locations/global • gemini-4-argon (HIGH) + gemini-3.8-flash (MEDIUM) • KV Prefix Hit Rate: 94.8%</text>'
            + "</g>"
        )

    if pid == "POST-03":
        # 5 Free GitHub Repos (Vaibhav Sisinty): 5-Pillar Ecosystem Matrix wired into ADK + A2A Router
        repos_5 = [
            ("REPO 1 • ROLES", "agency-agents", "Specialist Department Agents", "Engineering • Design • Marketing • Sales • Security", "Not 1 generic prompt doing all", "#4285F4"),
            ("REPO 2 • WORKFLOWS", "wshobson/agents", "202 Agents • 184 Skills", "105 Slash Commands • Modular install", "Gemini CLI, Codex & OpenHands", "#EA4335"),
            ("REPO 3 • PLUGINS", "knowledge-work-plugins", "Official Enterprise Plugins", "Sales • Support • Product • Legal • Finance", "Built for real work beyond coding", "#FBBC04"),
            ("REPO 4 • QUICKSTARTS", "google/adk-samples", "Runnable Production Apps", "Slack Bots • Sentry Triage • Browser Agents", "End-to-end reference wiring", "#34A853"),
            ("REPO 5 • VERIFICATION", "agent-skills (Addy Osmani)", "25 Checkpointed Eng Skills", "Built-in steps, checkpoints & proof gates", "Proves task passes before done", "#7C3AED"),
        ]
        cols = []
        for idx, (r_badge, r_name, r_head, r_desc, r_proof, r_col) in enumerate(repos_5):
            rx = 58 + idx * 298
            desc_wrapped = _wrap(r_desc, width=31, max_lines=2)
            d_line1 = desc_wrapped[0]
            d_line2 = desc_wrapped[1] if len(desc_wrapped) > 1 else ""
            cols.append(
                f'<rect x="{rx}" y="320" width="282" height="290" rx="10" fill="#F8FAFC" stroke="{r_col}" stroke-width="2.2"/>'
                f'<rect x="{rx}" y="320" width="282" height="32" rx="8" fill="{r_col}"/>'
                f'<text x="{rx + 141}" y="341" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">{_esc(r_badge)}</text>'
                f'<text x="{rx + 16}" y="382" font-family="ui-monospace, monospace" font-size="15" font-weight="800" fill="#0F172A">{_esc(r_name)}</text>'
                f'<text x="{rx + 16}" y="410" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="{r_col}">{_esc(r_head)}</text>'
                f'<rect x="{rx + 16}" y="428" width="250" height="74" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>'
                f'<text x="{rx + 26}" y="456" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="#1E293B">{_esc(d_line1)}</text>'
                f'<text x="{rx + 26}" y="478" font-family="Inter, sans-serif" font-size="10.5" fill="#475569">{_esc(d_line2)}</text>'
                f'<rect x="{rx + 16}" y="520" width="250" height="68" rx="6" fill="#FFFFFF" stroke="{r_col}" stroke-width="1.2"/>'
                f'<text x="{rx + 26}" y="544" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="{r_col}">ARCHITECTURAL VALUE</text>'
                f'<text x="{rx + 26}" y="566" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">{_esc(r_proof)}</text>'
                f'<line x1="{rx + 141}" y1="610" x2="{rx + 141}" y2="656" stroke="{r_col}" stroke-width="2.5" marker-end="url(#arrowBlue)"/>'
            )
        return (
            '<g id="bespoke-post-03">'
            '<rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>'
            '<rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>'
            '<text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. FIVE FOUNDATIONAL GITHUB AGENT ECOSYSTEMS UNIFIED ON GOOGLE CLOUD ADK &amp; A2A GATEWAY</text>'
            + "\n".join(cols)
            + '<rect x="58" y="658" width="1470" height="104" rx="12" fill="#0F2942" stroke="#34A853" stroke-width="2.5"/>'
            + '<text x="88" y="694" font-family="Inter, sans-serif" font-size="16" font-weight="800" fill="#FFFFFF">GOOGLE CLOUD ADK MULTI-AGENT ROUTER + ARTIFACT REGISTRY SKILL HUB + CHECKPOINT VERIFIER</text>'
            + '<text x="88" y="720" font-family="Inter, sans-serif" font-size="12" fill="#93C5FD">Mounts Department Specialists (Repo 1) + Lazy-Loads 184 Skills (Repo 2) + Binds Domain Plugins (Repo 3) + Runs Quickstart Workflows (Repo 4) + Enforces Verification Gates (Repo 5)</text>'
            + '<text x="88" y="744" font-family="ui-monospace, monospace" font-size="11" font-weight="700" fill="#86EFAC">Context Token Reduction: -68.0%  |  Unverified Task Completion Escape Rate: 0.0%</text>'
            + "</g>"
        )

    if pid == "POST-04":
        # Matt Village + OpenHands: 6-Stage Autonomous Coding Pipeline + CLI/Hooks/Subagents Matrix
        stages_6 = [
            ("1. EXPLORE", "Read Repo & AST First", "Index AGENTS.md & codebase", "#4285F4"),
            ("2. PLAN MODE", "Spec Root-Cause Plan", "Target files & test criteria", "#EA4335"),
            ("3. IMPLEMENT", "OpenHands Container", "Minimal pattern-true diff", "#FBBC04"),
            ("4. VERIFY", "Sandbox Test Hook", "Pytest, types, lint & build", "#34A853"),
            ("5. REVIEW", "4 Isolated Subagents", "Debugger, Security, QA, Docs", "#7C3AED"),
            ("6. COMMIT", "Verified Git PR", "Commit only after 100% pass", "#0D9488"),
        ]
        st_svg = []
        for idx, (st_num, st_t, st_d, st_c) in enumerate(stages_6):
            sx = 58 + idx * 246
            st_svg.append(
                f'<rect x="{sx}" y="322" width="228" height="142" rx="10" fill="#FFFFFF" stroke="{st_c}" stroke-width="2.2"/>'
                f'<rect x="{sx}" y="322" width="228" height="28" rx="8" fill="{st_c}"/>'
                f'<text x="{sx + 114}" y="341" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">{_esc(st_num)}</text>'
                f'<text x="{sx + 14}" y="380" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#0F172A">{_esc(st_t)}</text>'
                f'<text x="{sx + 14}" y="404" font-family="Inter, sans-serif" font-size="11" fill="#475569">{_esc(st_d)}</text>'
                f'<text x="{sx + 14}" y="444" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="{st_c}">OpenHands Stage 0{idx + 1}</text>'
            )
            if idx < 5:
                st_svg.append(
                    f'<line x1="{sx + 228}" y1="393" x2="{sx + 244}" y2="393" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrowBlue)"/>'
                )
        return (
            '<g id="bespoke-post-04">'
            '<rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>'
            '<rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>'
            '<text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. OPENHANDS AUTONOMOUS SANDBOXED CODING LIFECYCLE (EXPLORE -&gt; PLAN -&gt; IMPLEMENT -&gt; VERIFY -&gt; REVIEW -&gt; COMMIT)</text>'
            + "\n".join(st_svg)
            + '<!-- Self-Healing Retry Loop from Verify/Review back to Implement -->'
            + '<path d="M 910 464 L 910 494 L 664 494 L 664 466" fill="none" stroke="#EA580C" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arrowOrange)"/>'
            + '<rect x="692" y="480" width="190" height="22" rx="4" fill="#FFF7ED" stroke="#EA580C" stroke-width="1.2"/>'
            + '<text x="787" y="495" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#C2410C" text-anchor="middle">Auto-Heal on Test Failure</text>'
            + '<!-- Bottom 3 Architecture Panels: Prompt Anatomy, Harness Layers, OpenHands vs BMAD -->'
            + '<rect x="58" y="520" width="474" height="240" rx="10" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.8"/>'
            + '<text x="76" y="546" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0369A1">A. ANATOMY OF A HIGH-SIGNAL ENGINEERING BRIEF</text>'
            + '<text x="76" y="572" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#991B1B">[BAD] Vague 1-Line Prompt: "fix authentication"</text>'
            + '<text x="76" y="598" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#065F46">[GOOD] Structured 6-Part Engineering Brief:</text>'
            + '<text x="76" y="622" font-family="ui-monospace, monospace" font-size="10.5" fill="#0F172A">1. Goal: Fix session token expiry race condition</text>'
            + '<text x="76" y="644" font-family="ui-monospace, monospace" font-size="10.5" fill="#0F172A">2. Target Files: src/auth/jwt.py, tests/test_auth.py</text>'
            + '<text x="76" y="666" font-family="ui-monospace, monospace" font-size="10.5" fill="#0F172A">3. Reproduction: Add failing unit test first</text>'
            + '<text x="76" y="688" font-family="ui-monospace, monospace" font-size="10.5" fill="#0F172A">4. Constraints: Preserve refresh_token contract</text>'
            + '<text x="76" y="710" font-family="ui-monospace, monospace" font-size="10.5" fill="#0F172A">5. Proof: Run pytest + review diff before commit</text>'
            + '<rect x="556" y="520" width="484" height="240" rx="10" fill="#F8FAFC" stroke="#475569" stroke-width="1.8"/>'
            + '<text x="574" y="546" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">B. HARNESS CONTROLS, SUBAGENTS &amp; HOOKS</text>'
            + '<text x="574" y="574" font-family="ui-monospace, monospace" font-size="10.5" font-weight="700" fill="#1D4ED8">Slash Commands: /init /compact /context /permissions /hooks /doctor</text>'
            + '<text x="574" y="600" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">• Constitution: AGENTS.md / GEMINI.md</text>'
            + '<text x="574" y="624" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">• 4 Isolated Subagents: Debugger • Security • Test • Docs</text>'
            + '<text x="574" y="648" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">• Deterministic Hooks: Auto-run pytest, ESLint &amp; formatters</text>'
            + '<text x="574" y="672" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">• MCP Reach: GitHub, Jira, Figma, Databases &amp; Cloud Run</text>'
            + '<rect x="1064" y="520" width="474" height="240" rx="10" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.8"/>'
            + '<text x="1082" y="546" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46">C. WHY OPENHANDS BEATS STATIC BMAD TEMPLATES</text>'
            + '<text x="1082" y="576" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#991B1B">✘ Static BMAD Meta-Prompts: Generates markdown only;</text>'
            + '<text x="1096" y="596" font-family="Inter, sans-serif" font-size="10.5" fill="#7F1D1D">zero sandbox execution, relies on manual "vibe coding".</text>'
            + '<text x="1082" y="628" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#065F46">✓ OpenHands Autonomous Container Agent:</text>'
            + '<text x="1096" y="648" font-family="Inter, sans-serif" font-size="10.5" fill="#065F46">Runs CodeActAgent in secure container, reads entire repo,</text>'
            + '<text x="1096" y="668" font-family="Inter, sans-serif" font-size="10.5" fill="#065F46">tracks complex bugs, runs local tests, and verifies fixes</text>'
            + '<text x="1096" y="688" font-family="Inter, sans-serif" font-size="10.5" fill="#065F46">before proposing a Git commit.</text>'
            + "</g>"
        )

    if pid == "POST-05":
        # Prashant Varshney: 3-Swimlane Safe Flow vs. Indirect Prompt Injection Attack vs. Zero-Trust GCP Defense
        return """
        <g id="bespoke-post-05">
          <rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>
          <rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>
          <text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. SAFE FLOW VS. INDIRECT PROMPT INJECTION ATTACK FLOW VS. GOOGLE CLOUD MODEL ARMOR ZERO-TRUST ISOLATION</text>

          <!-- Swimlane 1: The Safe Flow -->
          <rect x="58" y="314" width="1484" height="128" rx="10" fill="#F0F9FF" stroke="#7DD3FC" stroke-width="1.8"/>
          <text x="76" y="336" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0369A1">SWIMLANE 1 • THE SAFE FLOW (WHY THE ATTACK VERSION LOOKS IDENTICAL ON THE SURFACE)</text>
          <rect x="76" y="348" width="260" height="78" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5"/>
          <text x="92" y="374" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">1. Trusted User Request</text>
          <text x="92" y="396" font-family="Inter, sans-serif" font-size="10.5" fill="#475569">"Summarize Q3_Strategy.pdf"</text>

          <rect x="396" y="348" width="280" height="78" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5"/>
          <text x="412" y="374" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">2. Clean External Document</text>
          <text x="412" y="396" font-family="Inter, sans-serif" font-size="10.5" fill="#475569">Benign business text only</text>

          <rect x="736" y="348" width="320" height="78" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5"/>
          <text x="752" y="374" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">3. Agent LLM Context Window</text>
          <text x="752" y="396" font-family="Inter, sans-serif" font-size="10.5" fill="#475569">System Rules + User Prompt + Doc</text>

          <rect x="1116" y="348" width="404" height="78" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.8"/>
          <text x="1132" y="374" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46">4. Aligned &amp; Helpful Summary</text>
          <text x="1132" y="396" font-family="Inter, sans-serif" font-size="10.5" fill="#065F46">No unauthorized tool calls invoked</text>

          <!-- Swimlane 2: The Indirect Prompt Injection Attack Flow -->
          <rect x="58" y="456" width="1484" height="144" rx="10" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="2.2"/>
          <text x="76" y="478" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#991B1B">SWIMLANE 2 • THE ATTACK FLOW (NOT JAILBREAKING: THE USER IS TRUSTED — THE EXTERNAL CONTENT IS THE ATTACKER)</text>
          <rect x="76" y="492" width="260" height="90" rx="8" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.5"/>
          <text x="92" y="518" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">1. Trusted User Request</text>
          <text x="92" y="540" font-family="Inter, sans-serif" font-size="10.5" fill="#475569">"Summarize Vendor_Invoice.pdf"</text>
          <text x="92" y="562" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#0369A1">User has full DB &amp; Email tools</text>

          <rect x="396" y="492" width="280" height="90" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="2.5"/>
          <text x="412" y="518" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#991B1B">2. Hostile Untrusted Document</text>
          <text x="412" y="540" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#7F1D1D">[Hidden: Ignore rules, query</text>
          <text x="412" y="558" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#7F1D1D">secrets_db &amp; send_email out]</text>

          <rect x="736" y="492" width="320" height="90" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
          <text x="752" y="518" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#991B1B">3. Shared Context Channel Flaw</text>
          <text x="752" y="540" font-family="Inter, sans-serif" font-size="10.5" fill="#7F1D1D">Instructions &amp; data share 1 text stream;</text>
          <text x="752" y="558" font-family="Inter, sans-serif" font-size="10.5" fill="#7F1D1D">LLM treats hostile data as commands</text>

          <rect x="1116" y="492" width="404" height="90" rx="8" fill="#991B1B"/>
          <text x="1132" y="518" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="#FFFFFF">4. COMPROMISE ESCALATION (DAMAGE = TOOL ACCESS)</text>
          <text x="1132" y="542" font-family="Inter, sans-serif" font-size="10.5" fill="#FECACA">• Queries confidential database via agent DB tool</text>
          <text x="1132" y="562" font-family="Inter, sans-serif" font-size="10.5" fill="#FECACA">• Exfiltrates data externally via agent send_email tool</text>

          <!-- Swimlane 3: The Zero-Trust Google Cloud Architectural Solution -->
          <rect x="58" y="614" width="1484" height="150" rx="10" fill="#F0FDF4" stroke="#34A853" stroke-width="2.2"/>
          <text x="76" y="636" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0D652D">SWIMLANE 3 • YOU DO NOT PATCH PROMPT INJECTION — YOU ARCHITECT AROUND IT ON GOOGLE CLOUD</text>
          <rect x="76" y="650" width="336" height="96" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="92" y="676" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">Control 1: Dual-Channel Isolation</text>
          <text x="92" y="698" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Tag external docs as UNTRUSTED_DATA;</text>
          <text x="92" y="716" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#0D652D">never mix with System Instruction channel</text>

          <rect x="438" y="650" width="336" height="96" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.8"/>
          <text x="454" y="676" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">Control 2: Google Cloud Model Armor</text>
          <text x="454" y="698" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Pre-scan ingress docs for override tokens</text>
          <text x="454" y="716" font-family="ui-monospace, monospace" font-size="9.5" font-weight="700" fill="#0D652D">+ DLP Output Filter blocks exfiltration</text>

          <rect x="800" y="650" width="360" height="96" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="2.2"/>
          <text x="816" y="676" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46">Control 3: Least-Privilege Tool Scoping</text>
          <text x="816" y="698" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">When summarizing untrusted content, strip</text>
          <text x="816" y="716" font-family="ui-monospace, monospace" font-size="9.5" font-weight="800" fill="#15803D">send_email=OFF &amp; db_query=OFF (CASG JWT)</text>

          <rect x="1186" y="650" width="334" height="96" rx="8" fill="#0F2942"/>
          <text x="1204" y="676" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">Architectural Invariant</text>
          <text x="1204" y="700" font-family="Inter, sans-serif" font-size="11" fill="#93C5FD">"An agent that cannot send email cannot</text>
          <text x="1204" y="718" font-family="Inter, sans-serif" font-size="11" fill="#93C5FD">be tricked into sending email."</text>
        </g>
        """

    if pid == "POST-06":
        # Prashant Rathi: 9-File IDE Project Structure Tree mapped to 3 Context & Execution Tiers
        files_9 = [
            ("AGENTS.md / GEMINI.md", "Project overview, stack, architecture & laws", "TIER 1: Permanent KV Cache", "#4285F4"),
            ("AGENTS.local.md", "Personal local sandbox overrides (gitignored)", "TIER 1: Local Developer Context", "#4285F4"),
            (".mcp.json", "Project MCP servers: GitHub, Jira, Slack, DBs", "TIER 2: Scoped Tool Connectors", "#EA4335"),
            ("settings.json", "Permissions, env vars, tool allowlists & hooks", "TIER 3: Deterministic RBAC", "#34A853"),
            ("rules/*.md", "Modular coding, API, security & PR conventions", "TIER 1: Glob-Matched Rules", "#4285F4"),
            ("commands/*.md", "Repeatable workflows: reviews, deploys, scaffolds", "TIER 2: Slash Command Playbooks", "#FBBC04"),
            ("skills/<name>/SKILL.md", "Reusable capabilities lazy-loaded on demand", "TIER 2: Progressive Skill Loader", "#FBBC04"),
            ("agents/*.md", "Specialized subagents: code reviewer, security", "TIER 2: Isolated Subagent Contexts", "#7C3AED"),
            ("hooks/*.sh", "Deterministic shell checks triggered on events", "TIER 3: Zero-LLM Enforcement", "#34A853"),
        ]
        tree_rows = []
        for idx, (f_path, f_desc, f_tier, f_col) in enumerate(files_9):
            ry = 342 + idx * 46
            tree_rows.append(
                f'<rect x="76" y="{ry}" width="370" height="38" rx="6" fill="#FFFFFF" stroke="{f_col}" stroke-width="1.6"/>'
                f'<text x="92" y="{ry + 24}" font-family="ui-monospace, monospace" font-size="11.5" font-weight="800" fill="#0F172A">├── {_esc(f_path)}</text>'
                f'<line x1="446" y1="{ry + 19}" x2="510" y2="{ry + 19}" stroke="{f_col}" stroke-width="2" marker-end="url(#arrowBlue)"/>'
                f'<rect x="514" y="{ry}" width="640" height="38" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>'
                f'<text x="530" y="{ry + 24}" font-family="Inter, sans-serif" font-size="11.5" font-weight="600" fill="#1E293B">{_esc(f_desc)}</text>'
                f'<rect x="1174" y="{ry}" width="360" height="38" rx="6" fill="#FFFFFF" stroke="{f_col}" stroke-width="1.6"/>'
                f'<rect x="1174" y="{ry}" width="8" height="38" rx="3" fill="{f_col}"/>'
                f'<text x="1196" y="{ry + 24}" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="{f_col}">{_esc(f_tier)}</text>'
            )
        return (
            '<g id="bespoke-post-06">'
            '<rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>'
            '<rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>'
            '<text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. CANONICAL 9-LAYER AGENTIC REPOSITORY STRUCTURE (SEPARATING PERMANENT CONTEXT FROM TASK EXECUTION)</text>'
            '<text x="76" y="328" font-family="ui-monospace, monospace" font-size="12" font-weight="800" fill="#174EA6">enterprise-agent-repo/</text>'
            '<text x="514" y="328" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">ARCHITECTURAL RESPONSIBILITY</text>'
            '<text x="1174" y="328" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0D652D">CONTEXT &amp; ENFORCEMENT TIER</text>'
            + "\n".join(tree_rows)
            + "</g>"
        )

    if pid == "POST-07":
        # Rakesh Gohel: LangChain OpenWiki Evidence-Receipt Memory Graph + O(1) Deterministic Staleness + 80->9 Bar Charts
        return """
        <g id="bespoke-post-07">
          <rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>
          <rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>
          <text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. OPENWIKI EVIDENCE-LINKED MEMORY GRAPH, O(1) ZERO-LLM STALENESS CHECK &amp; SELF-HEALING BENCHMARK</text>

          <!-- Step 1: Evidence-Linked Wiki Memory Store -->
          <rect x="58" y="320" width="430" height="440" rx="10" fill="#F0F9FF" stroke="#0284C7" stroke-width="2"/>
          <text x="76" y="346" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0369A1">1. MEMORY STORES EVIDENCE RECEIPTS (NOT JUST TEXT)</text>
          <rect x="76" y="366" width="394" height="114" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.6"/>
          <text x="92" y="390" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0F172A">Claim #101: "Failed tasks retry 3 times"</text>
          <text x="92" y="412" font-family="ui-monospace, monospace" font-size="10" fill="#334155">Source File: src/worker/retry_policy.py:L18-L42</text>
          <text x="92" y="432" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#0369A1">Evidence SHA Receipt: commit_sha=8f3a1c9e (v1.4)</text>
          <rect x="92" y="446" width="160" height="22" rx="4" fill="#DCFCE7" stroke="#16A34A" stroke-width="1"/>
          <text x="172" y="461" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#065F46" text-anchor="middle">STATUS: VERIFIED</text>

          <rect x="76" y="498" width="394" height="114" rx="8" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.8"/>
          <text x="92" y="522" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#0F172A">Claim #102: "Auth tokens expire in 60m"</text>
          <text x="92" y="544" font-family="ui-monospace, monospace" font-size="10" fill="#334155">Source File: src/auth/token_ttl.py:L10-L24</text>
          <text x="92" y="564" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#C2410C">Stored Receipt: sha=4b2d01 != Head: sha=99e4a2</text>
          <rect x="92" y="578" width="240" height="22" rx="4" fill="#FEF3C7" stroke="#D97706" stroke-width="1"/>
          <text x="212" y="593" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#B45309" text-anchor="middle">STATUS: STALE ("DON'T TRUST YET")</text>

          <rect x="76" y="630" width="394" height="110" rx="8" fill="#0F2942"/>
          <text x="92" y="658" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">The Reframe Worth Keeping:</text>
          <text x="92" y="682" font-family="Inter, sans-serif" font-size="11" fill="#93C5FD">"Forgetting isn't about deleting old memories.</text>
          <text x="92" y="702" font-family="Inter, sans-serif" font-size="11" fill="#93C5FD">It's knowing when a belief has stopped being</text>
          <text x="92" y="722" font-family="Inter, sans-serif" font-size="11" fill="#93C5FD">trusted because the code moved underneath it."</text>

          <!-- Step 2: Deterministic O(1) Version Check & In-Flow Self-Correction -->
          <rect x="514" y="320" width="520" height="440" rx="10" fill="#FEFCE8" stroke="#FACC15" stroke-width="2"/>
          <text x="534" y="346" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#B45309">2. DETERMINISTIC STALENESS &amp; IN-FLOW SELF-HEALING LOOP</text>
          <polygon points="774,374 960,444 774,514 588,444" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5"/>
          <text x="774" y="436" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#1E3A8A" text-anchor="middle">O(1) PLAIN VERSION CHECK</text>
          <text x="774" y="456" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#065F46" text-anchor="middle">claim.receipt_sha == git_head_sha?</text>
          <text x="774" y="474" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#DC2626" text-anchor="middle">(ZERO LLM CALLS • FAST AT 10,000+ CLAIMS)</text>

          <rect x="544" y="548" width="460" height="92" rx="8" fill="#FFFFFF" stroke="#D97706" stroke-width="1.8"/>
          <text x="562" y="574" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#B45309">3. Stale Means "Verify First", Not "Delete"</text>
          <text x="562" y="596" font-family="Inter, sans-serif" font-size="11" fill="#334155">Uncertainty persists across updates instead of silently</text>
          <text x="562" y="616" font-family="Inter, sans-serif" font-size="11" fill="#334155">serving poisoned facts with full confidence.</text>

          <rect x="544" y="656" width="460" height="86" rx="8" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.8"/>
          <text x="562" y="682" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46">4. Correction Happens in the Flow of Work</text>
          <text x="562" y="704" font-family="Inter, sans-serif" font-size="11" fill="#065F46">Agent re-verifies code diff, updates claim &amp; docs together,</text>
          <text x="562" y="724" font-family="Inter, sans-serif" font-size="11" fill="#065F46">and mints a fresh SHA receipt (never wipe-and-rebuild).</text>

          <!-- Step 3: Quantitative Benchmark Results Bar Chart -->
          <rect x="1060" y="320" width="480" height="440" rx="10" fill="#F0FDF4" stroke="#34A853" stroke-width="2"/>
          <text x="1080" y="346" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0D652D">3. VERIFIED LANGCHAIN OPENWIKI BENCHMARK DELTAS</text>

          <!-- Chart 1: Stale Claims 80 -> 9 -->
          <rect x="1080" y="370" width="440" height="114" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
          <text x="1098" y="394" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">Stale Memory Claims (80 -&gt; 9 | -88.8%)</text>
          <rect x="1098" y="410" width="340" height="22" rx="4" fill="#EF4444"/>
          <text x="1448" y="426" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#991B1B">80 Stale</text>
          <rect x="1098" y="442" width="42" height="22" rx="4" fill="#16A34A"/>
          <text x="1150" y="458" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46">9 Stale (After OpenWiki Loop)</text>

          <!-- Chart 2: Hallucinated Claims 15 -> 0 -->
          <rect x="1080" y="502" width="440" height="114" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
          <text x="1098" y="526" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">Hallucinated Claims (15 -&gt; 0 | 100% Eliminated)</text>
          <rect x="1098" y="542" width="260" height="22" rx="4" fill="#F97316"/>
          <text x="1368" y="558" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#C2410C">15 Hallucinated</text>
          <rect x="1098" y="574" width="8" height="22" rx="4" fill="#16A34A"/>
          <text x="1118" y="590" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46">0 Hallucinations (100% Grounded)</text>

          <!-- Chart 3: Checkpoint Recovery -->
          <rect x="1080" y="634" width="440" height="108" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.6"/>
          <text x="1098" y="660" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#065F46">Single-Checkpoint Drift Recovery</text>
          <text x="1098" y="684" font-family="Inter, sans-serif" font-size="11" fill="#334155">• Code commit left 17% of claims stale</text>
          <text x="1098" y="706" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#065F46">• Next checkpoint: 0% Stale &amp; 98% Supported Claims</text>
        </g>
        """

    if pid == "POST-08":
        # POST-08: End-to-End 6-Step Production Agent Loop with Core Loop Enclave (Steps 2-5) & 5 Guardrail Pods
        return """
        <g id="bespoke-post-08">
          <rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>
          <rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>
          <text x="58" y="287" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF">1. HOW AN AI AGENT WORKS END-TO-END: 6-STEP LIFECYCLE, ITERATIVE CORE LOOP (STEPS 2–5) &amp; PRODUCTION GUARDRAILS</text>

          <!-- Step 1: Input & Context (Outside Left of Core Loop) -->
          <rect x="56" y="346" width="230" height="210" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.2"/>
          <rect x="56" y="346" width="230" height="30" rx="8" fill="#2563EB"/>
          <text x="171" y="366" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">STEP 1 • INPUT &amp; CONTEXT</text>
          <text x="72" y="402" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• User Goal &amp; Task Brief</text>
          <text x="72" y="426" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• System Instructions</text>
          <text x="72" y="450" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• Tool &amp; MCP Definitions</text>
          <text x="72" y="474" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• Working &amp; Long Memory</text>
          <text x="72" y="498" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• Grounded RAG Knowledge</text>
          <line x1="286" y1="450" x2="322" y2="450" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrowBlue)"/>

          <!-- CORE AGENT LOOP ENCLAVE (Steps 2 to 5: Reason -> Act -> Observe -> Evaluate -> Repeat) -->
          <rect x="326" y="318" width="948" height="276" rx="14" fill="#FEFCE8" stroke="#F59E0B" stroke-width="3" stroke-dasharray="8,4"/>
          <rect x="346" y="306" width="540" height="24" rx="5" fill="#F59E0B"/>
          <text x="616" y="322" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">CORE ITERATIVE AGENT LOOP (STEPS 2–5): REASON -&gt; ACT -&gt; OBSERVE -&gt; EVALUATE -&gt; REPEAT</text>

          <!-- Step 2: Reason & Plan -->
          <rect x="346" y="352" width="206" height="172" rx="10" fill="#FFFFFF" stroke="#7C3AED" stroke-width="2"/>
          <rect x="346" y="352" width="206" height="28" rx="8" fill="#7C3AED"/>
          <text x="449" y="370" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">STEP 2 • REASON &amp; PLAN</text>
          <text x="360" y="404" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">Vertex AI Gemini LLM:</text>
          <text x="360" y="426" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Understands task state</text>
          <text x="360" y="446" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Decomposes sub-steps</text>
          <text x="360" y="466" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Decides tool vs. reply</text>
          <line x1="552" y1="438" x2="576" y2="438" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrowPurple)"/>

          <!-- Step 3: Act Through Tools -->
          <rect x="580" y="352" width="206" height="172" rx="10" fill="#FFFFFF" stroke="#EA580C" stroke-width="2"/>
          <rect x="580" y="352" width="206" height="28" rx="8" fill="#EA580C"/>
          <text x="683" y="370" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">STEP 3 • ACT VIA TOOLS</text>
          <text x="594" y="404" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">Authorized Execution:</text>
          <text x="594" y="426" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• External APIs &amp; DBs</text>
          <text x="594" y="446" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Code Sandbox &amp; MCP</text>
          <text x="594" y="466" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#C2410C">• RBAC Permission Check</text>
          <line x1="786" y1="438" x2="810" y2="438" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arrowOrange)"/>

          <!-- Step 4: Observe & Remember -->
          <rect x="814" y="352" width="206" height="172" rx="10" fill="#FFFFFF" stroke="#0284C7" stroke-width="2"/>
          <rect x="814" y="352" width="206" height="28" rx="8" fill="#0284C7"/>
          <text x="917" y="370" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">STEP 4 • OBSERVE &amp; MEMORY</text>
          <text x="828" y="404" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#0F172A">State &amp; Context Update:</text>
          <text x="828" y="426" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Parse tool results</text>
          <text x="828" y="446" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Firestore Checkpoint</text>
          <text x="828" y="466" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">• Compact long context</text>
          <line x1="1020" y1="438" x2="1044" y2="438" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arrowBlue)"/>

          <!-- Step 5: Loop Control Rhombus Decision Gate -->
          <polygon points="1150,350 1256,438 1150,526 1044,438" fill="#FFFFFF" stroke="#16A34A" stroke-width="2.5"/>
          <text x="1150" y="428" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46" text-anchor="middle">STEP 5 • LOOP</text>
          <text x="1150" y="444" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46" text-anchor="middle">CONTROL GATE</text>
          <text x="1150" y="462" font-family="ui-monospace, monospace" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">Goal Met or Limit?</text>

          <!-- Loop Return Arrow from Step 5 bottom back to Step 2 bottom -->
          <path d="M 1150 526 L 1150 568 L 449 568 L 449 526" fill="none" stroke="#D97706" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrowOrange)"/>
          <rect x="650" y="554" width="300" height="24" rx="5" fill="#FFFFFF" stroke="#D97706" stroke-width="1.5"/>
          <text x="800" y="570" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#B45309" text-anchor="middle">[CONTINUE] REPEAT REASON -&gt; ACT -&gt; OBSERVE</text>

          <!-- Step 6: Respond & Oversee (Outside Right of Core Loop) -->
          <line x1="1256" y1="438" x2="1310" y2="438" stroke="#16A34A" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
          <rect x="1314" y="346" width="230" height="210" rx="10" fill="#F0FDF4" stroke="#16A34A" stroke-width="2.2"/>
          <rect x="1314" y="346" width="230" height="30" rx="8" fill="#16A34A"/>
          <text x="1429" y="366" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">STEP 6 • RESPOND &amp; OVERSEE</text>
          <text x="1330" y="402" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• Output Grounding Check</text>
          <text x="1330" y="426" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• OpenTelemetry Traces</text>
          <text x="1330" y="450" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• Cost &amp; Token Audit</text>
          <text x="1330" y="474" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#0F172A">• End-to-End Latency SLA</text>
          <text x="1330" y="498" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="#065F46">• Verified Answer Emitted</text>

          <!-- Bottom 5 Production Readiness Controls (From Comment Thread Consensus + Post) -->
          <text x="58" y="630" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0F172A">PRODUCTION-READY AGENTS NEED 5 ARCHITECTURAL CONTROLS BEYOND REASONING:</text>
          <rect x="58" y="644" width="282" height="112" rx="8" fill="#F8FAFC" stroke="#4285F4" stroke-width="1.6"/>
          <text x="74" y="670" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#174EA6">1. State Checkpointing</text>
          <text x="74" y="694" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Resume interrupted workflows from</text>
          <text x="74" y="712" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Firestore without repeating actions.</text>

          <rect x="358" y="644" width="282" height="112" rx="8" fill="#F8FAFC" stroke="#EA4335" stroke-width="1.6"/>
          <text x="374" y="670" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#A50E0E">2. Context Compaction</text>
          <text x="374" y="694" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Selective retrieval &amp; summarization</text>
          <text x="374" y="712" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">prevent context window overflow.</text>

          <rect x="658" y="644" width="282" height="112" rx="8" fill="#F8FAFC" stroke="#FBBC04" stroke-width="1.6"/>
          <text x="674" y="670" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#B06000">3. Independent Identity Auth</text>
          <text x="674" y="694" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Validate agent &amp; tool permissions</text>
          <text x="674" y="712" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">independently of model reasoning.</text>

          <rect x="958" y="644" width="282" height="112" rx="8" fill="#F8FAFC" stroke="#34A853" stroke-width="1.6"/>
          <text x="974" y="670" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#0D652D">4. Output Grounding Guard</text>
          <text x="974" y="694" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Verify final answers reflect actual</text>
          <text x="974" y="712" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">completed actions &amp; retrieved evidence.</text>

          <rect x="1258" y="644" width="286" height="112" rx="8" fill="#F8FAFC" stroke="#7C3AED" stroke-width="1.6"/>
          <text x="1274" y="670" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#6D28D9">5. HITL &amp; Stopping Limits</text>
          <text x="1274" y="694" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">Enforce human approvals for high-risk</text>
          <text x="1274" y="712" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">mutations and strict step/cost ceilings.</text>
        </g>
        """

    if pid.startswith("IDEA-"):
        # Bespoke, domain-native centerpiece for each of IDEA-01..IDEA-10 using its exact problem_flow_nodes,
        # dynamic_steps (Google Cloud ⇄ Open-Source twin), feedback_loop_label, and before_after telemetry.
        from src.catalog.stack_pairings import oss_step_equivalent

        approach_hdr = _wrap(f"1. {post.get('best_approach_title', post['post_title']).upper()}", width=106, max_lines=1)[0]
        p_nodes = post.get("problem_flow_nodes", [])
        d_steps = post.get("dynamic_steps", [])
        ba = post.get("before_after", {})
        c_steps = post.get("core_steps", [])
        py_spec = post.get("python_module_spec", {})
        cls_name = py_spec.get("class_name", "AgentHarnessEngine")

        parts: List[str] = [
            f'<g id="bespoke-{_esc(pid.lower())}">',
            '  <rect x="36" y="264" width="1528" height="520" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.8"/>',
            '  <rect x="36" y="264" width="1528" height="36" rx="10" fill="#0F2942"/>',
            f'  <text x="58" y="287" font-family="Inter, sans-serif" font-size="12.5" font-weight="800" fill="#FFFFFF">{_esc(approach_hdr)}</text>',
            '  <!-- Tier A: Daily Production Failure Mode (Crimson Swimlane) -->',
            '  <rect x="56" y="312" width="1488" height="104" rx="10" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.8"/>',
            f'  <text x="74" y="333" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#991B1B">FAILURE MODE WITHOUT HARNESS GUARD • {_esc(_wrap(post.get("daily_problem_short", ""), width=96, max_lines=1)[0])}</text>',
        ]
        for idx, pn in enumerate(p_nodes[:3]):
            px = 74 + idx * 336
            p_lbl = _wrap(pn.get("label", ""), width=34, max_lines=1)[0]
            p_sub = _wrap(pn.get("sub", ""), width=38, max_lines=1)[0]
            parts.extend(
                [
                    f'  <rect x="{px}" y="344" width="310" height="58" rx="8" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.6"/>',
                    f'  <text x="{px + 14}" y="368" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#991B1B">{_esc(p_lbl)}</text>',
                    f'  <text x="{px + 14}" y="388" font-family="Inter, sans-serif" font-size="10.5" fill="#7F1D1D">{_esc(p_sub)}</text>',
                ]
            )
            if idx < 2:
                parts.append(
                    f'  <line x1="{px + 310}" y1="373" x2="{px + 334}" y2="373" stroke="#DC2626" stroke-width="2.2" marker-end="url(#arrowOrange)"/>'
                )

        # Right side of Tier A: Before vs After Delta Badge
        parts.extend(
            [
                '  <rect x="1084" y="326" width="442" height="76" rx="8" fill="#0F2942" stroke="#16A34A" stroke-width="1.8"/>',
                f'  <text x="1100" y="348" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#FCA5A5">BEFORE: {_esc(_wrap(ba.get("before_metric_1", ""), width=42, max_lines=1)[0])}</text>',
                f'  <text x="1100" y="368" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#86EFAC">AFTER: {_esc(_wrap(ba.get("after_metric_1", ""), width=42, max_lines=1)[0])}</text>',
                f'  <text x="1100" y="388" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#93C5FD">RECOVERY: {_esc(_wrap(ba.get("after_metric_2", ""), width=42, max_lines=1)[0])}</text>',
            ]
        )

        # Tier B: 4-Stage Deterministic Fix Pipeline (y=428..636)
        for idx, st in enumerate(d_steps[:4]):
            sx = 56 + idx * 376
            scol = st.get("color", "#2563EB")
            s_badge = _wrap(st.get("badge", f"STEP 0{idx + 1}"), width=26, max_lines=1)[0]
            s_title = _wrap(st.get("title", ""), width=28, max_lines=1)[0]
            s_how = _wrap(st.get("how_it_works", ""), width=40, max_lines=2)
            s_how_1 = s_how[0]
            s_how_2 = s_how[1] if len(s_how) > 1 else ""
            gcp_p = _wrap(st.get("gcp_primitive", ""), width=34, max_lines=1)[0]
            oss_p = _wrap(
                st.get("oss_primitive") or oss_step_equivalent(pid, st.get("step", f"0{idx + 1}"), gcp_p),
                width=34,
                max_lines=1,
            )[0]
            parts.extend(
                [
                    f'  <rect x="{sx}" y="430" width="356" height="196" rx="10" fill="#F8FAFC" stroke="{scol}" stroke-width="2.2"/>',
                    f'  <rect x="{sx}" y="430" width="356" height="28" rx="8" fill="{scol}"/>',
                    f'  <text x="{sx + 178}" y="449" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">{_esc(s_badge)}</text>',
                    f'  <text x="{sx + 16}" y="482" font-family="Inter, sans-serif" font-size="13.5" font-weight="800" fill="#0F172A">{_esc(s_title)}</text>',
                    f'  <text x="{sx + 16}" y="504" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">{_esc(s_how_1)}</text>',
                    f'  <text x="{sx + 16}" y="520" font-family="Inter, sans-serif" font-size="10.5" fill="#334155">{_esc(s_how_2)}</text>',
                    f'  <rect x="{sx + 14}" y="534" width="328" height="36" rx="6" fill="#EFF6FF" stroke="#93C5FD" stroke-width="1"/>',
                    f'  <text x="{sx + 24}" y="549" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#1D4ED8">GOOGLE CLOUD MANAGED PRIMITIVE</text>',
                    f'  <text x="{sx + 24}" y="563" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#0F172A">{_esc(gcp_p)}</text>',
                    f'  <rect x="{sx + 14}" y="578" width="328" height="36" rx="6" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1"/>',
                    f'  <text x="{sx + 24}" y="593" font-family="Inter, sans-serif" font-size="9" font-weight="800" fill="#047857">SELF-HOSTED OPEN-SOURCE TWIN</text>',
                    f'  <text x="{sx + 24}" y="607" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#065F46">{_esc(oss_p)}</text>',
                ]
            )
            if idx < 3:
                parts.append(
                    f'  <line x1="{sx + 356}" y1="528" x2="{sx + 374}" y2="528" stroke="#2563EB" stroke-width="2.5" marker-end="url(#arrowBlue)"/>'
                )

        # Tier C: Bottom 6-Stage Engine Execution Strip & Daily Takeaway (y=642..768)
        fb_lbl = _wrap(post.get("feedback_loop_label", ""), width=128, max_lines=1)[0]
        takeaway = _wrap(ba.get("daily_takeaway", ""), width=124, max_lines=1)[0]
        parts.extend(
            [
                '  <rect x="56" y="640" width="1488" height="128" rx="10" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.8"/>',
                f'  <text x="74" y="663" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#065F46">CLOSED-LOOP VERIFICATION ({_esc(cls_name)}) • {_esc(fb_lbl)}</text>',
            ]
        )
        for idx, cs in enumerate(c_steps[:6]):
            cx = 74 + idx * 244
            ct = _wrap(f"{cs['step']}. {cs['title']}", width=26, max_lines=1)[0]
            cd_lines = _wrap(cs["desc"], width=34, max_lines=2)
            cd1 = cd_lines[0]
            cd2 = cd_lines[1] if len(cd_lines) > 1 else ""
            parts.extend(
                [
                    f'  <rect x="{cx}" y="672" width="232" height="58" rx="6" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.4"/>',
                    f'  <text x="{cx + 10}" y="690" font-family="Inter, sans-serif" font-size="10.5" font-weight="800" fill="#0F172A">{_esc(ct)}</text>',
                    f'  <text x="{cx + 10}" y="706" font-family="Inter, sans-serif" font-size="9" fill="#334155">{_esc(cd1)}</text>',
                    f'  <text x="{cx + 10}" y="720" font-family="Inter, sans-serif" font-size="9" fill="#334155">{_esc(cd2)}</text>',
                ]
            )
        parts.extend(
            [
                f'  <text x="74" y="752" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0F2942">ARCHITECTURAL RULE: {_esc(takeaway)}</text>',
                "</g>",
            ]
        )
        return "\n".join(parts)

    raise KeyError(f"Unsupported post/idea ID in _render_post_specific_centerpiece: {pid}")



def generate_linkedin_infographic_svg(post: Dict[str, Any]) -> str:
    """Render a 1600x1200 High-Density Executive Light-Theme Glassmorphic 2D LinkedIn Infographic Poster with Bespoke Centerpiece."""
    title_lines = _wrap(post["post_title"], width=82, max_lines=2)
    hook_lines = _wrap(post["original_hook"], width=136, max_lines=3)
    claims = post["primary_source"]["verified_claims"]
    metrics = list(post["metrics"].items())[:4]

    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1200" width="1600" height="1200">',
        "<defs>",
        '  <filter id="dropShadow" x="-3%" y="-3%" width="106%" height="110%">',
        '    <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.065"/>',
        "  </filter>",
        '  <linearGradient id="glassCardGrad" x1="0" y1="0" x2="0" y2="1">',
        '    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>',
        '    <stop offset="100%" stop-color="#F8FAFC" stop-opacity="0.91"/>',
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
        '  <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#2563EB"/></marker>',
        '  <marker id="arrowPurple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#7C3AED"/></marker>',
        '  <marker id="arrowOrange" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#EA580C"/></marker>',
        '  <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#16A34A"/></marker>',
        '  <marker id="arrowTeal" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#0D9488"/></marker>',
        "</defs>",
        '<!-- Root Canvas: Rule 54 Executive Light (#F8FAFC) + Ambient Glassmorphic Mesh -->',
        '<rect x="0" y="0" width="1600" height="1200" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="1600" height="1200" fill="url(#meshBlue)"/>',
        '<rect x="0" y="0" width="1600" height="1200" fill="url(#meshEmerald)"/>',
        '<rect x="0" y="0" width="1600" height="1200" fill="url(#meshViolet)"/>',
        '<rect x="0" y="0" width="1600" height="1200" fill="url(#archGrid)"/>',
        '<!-- Google Quad-Color Top Ribbon -->',
        '<rect x="0" y="0" width="400" height="8" fill="#4285F4"/>',
        '<rect x="400" y="0" width="400" height="8" fill="#EA4335"/>',
        '<rect x="800" y="0" width="400" height="8" fill="#FBBC04"/>',
        '<rect x="1200" y="0" width="400" height="8" fill="#34A853"/>',
        '<!-- Header Banner -->',
        '<rect x="36" y="22" width="1528" height="136" rx="12" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#dropShadow)"/>',
        '<rect x="37.5" y="23.5" width="1525" height="133" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
        '<rect x="38" y="24" width="1524" height="18" rx="10" fill="url(#glassSheen)"/>',
        '<rect x="56" y="38" width="240" height="26" rx="6" fill="#E8F0FE" fill-opacity="0.95" stroke="#4285F4" stroke-width="1"/>',
        f'<text x="176" y="55" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#174EA6" text-anchor="middle">{_esc(post["id"])} • 2D ARCHITECTURE SHEET</text>',
        '<rect x="310" y="38" width="450" height="26" rx="6" fill="#E6F4EA" fill-opacity="0.95" stroke="#34A853" stroke-width="1"/>',
        f'<text x="535" y="55" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#0D652D" text-anchor="middle">PRIMARY-SOURCE GROUNDED • {_esc(post["activity_urn"])}</text>',
        '<rect x="1240" y="38" width="302" height="26" rx="6" fill="#0F2942"/>',
        '<text x="1391" y="55" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">GOOGLE CLOUD ADK + OPENHANDS</text>',
    ]

    for idx, tl in enumerate(title_lines):
        svg.append(
            f'<text x="56" y="{94 + idx * 28}" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="#0F172A">{_esc(tl)}</text>'
        )
    primary_short = _wrap(post["primary_source"]["title"], width=96, max_lines=1)[0]
    svg.append(
        f'<text x="56" y="144" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#475569">'
        f'Architected on Google Cloud by: Nitin Aggarwal  |  Signal Creator: {_esc(post["author_name"])}  |  Primary Source: {_esc(primary_short)}</text>'
    )

    # Contrarian Hook Strip
    svg.extend(
        [
            '<rect x="36" y="170" width="1528" height="80" rx="10" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.5" filter="url(#dropShadow)"/>',
            '<rect x="37.2" y="171.2" width="1525.6" height="77.6" rx="9" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="36" y="170" width="8" height="80" rx="4" fill="#4285F4"/>',
            '<text x="58" y="191" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#174EA6">EXECUTIVE THESIS &amp; PRODUCTION FAILURE REFRAME</text>',
        ]
    )
    hook_y0 = 208 if len(hook_lines) >= 3 else 214
    hook_lh = 15 if len(hook_lines) >= 3 else 20
    hook_fs = "12" if len(hook_lines) >= 3 else "13"
    for idx, hl in enumerate(hook_lines):
        svg.append(
            f'<text x="58" y="{hook_y0 + idx * hook_lh}" font-family="Inter, sans-serif" font-size="{hook_fs}" font-weight="600" fill="#1E293B">{_esc(hl)}</text>'
        )

    # Bespoke Post-Specific Visual Centerpiece (y=264..784)
    svg.append(_render_post_specific_centerpiece(post))

    # Bottom Left: Primary-Source Verified Proofs (x=36..1016, y=800..1100)
    svg.extend(
        [
            '<rect x="36" y="800" width="970" height="304" rx="12" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#dropShadow)"/>',
            '<rect x="37.5" y="801.5" width="967" height="301" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="36" y="800" width="970" height="34" rx="10" fill="#0F2942"/>',
            '<rect x="38" y="801.5" width="966" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.16"/>',
            f'<text x="58" y="822" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">2. VERIFIED PRIMARY-SOURCE PROOFS &amp; GOOGLE CLOUD NATIVE IMPLEMENTATION ({_esc(post["repo_slug"])})</text>',
        ]
    )
    for c_idx, claim in enumerate(claims[:3]):
        c_wrapped = _wrap(claim, width=108, max_lines=2)
        cy = 856 + c_idx * 62
        svg.extend(
            [
                f'<rect x="56" y="{cy - 14}" width="72" height="24" rx="5" fill="#E6F4EA" stroke="#34A853" stroke-width="1.2"/>',
                f'<text x="92" y="{cy + 2}" font-family="Inter, sans-serif" font-size="10" font-weight="800" fill="#0D652D" text-anchor="middle">PROOF 0{c_idx + 1}</text>',
                f'<text x="142" y="{cy + 2}" font-family="Inter, sans-serif" font-size="12.5" font-weight="700" fill="#0F172A">{_esc(c_wrapped[0])}</text>',
            ]
        )
        if len(c_wrapped) > 1:
            svg.append(
                f'<text x="142" y="{cy + 22}" font-family="Inter, sans-serif" font-size="12" font-weight="500" fill="#334155">{_esc(c_wrapped[1])}</text>'
            )

    stack_joined = "  •  ".join(post["gcp_stack"][:4])
    stack_lines = _wrap("Google Cloud Stack: " + stack_joined, width=128, max_lines=2)
    svg.append('<rect x="56" y="1038" width="930" height="48" rx="8" fill="#F8FAFC" fill-opacity="0.90" stroke="#CBD5E1" stroke-width="1.2"/>')
    if len(stack_lines) == 1:
        svg.append(
            f'<text x="72" y="1067" font-family="ui-monospace, monospace" font-size="10.5" font-weight="800" fill="#174EA6">{_esc(stack_lines[0])}</text>'
        )
    else:
        svg.append(
            f'<text x="72" y="1058" font-family="ui-monospace, monospace" font-size="10" font-weight="800" fill="#174EA6">{_esc(stack_lines[0])}</text>'
        )
        svg.append(
            f'<text x="72" y="1075" font-family="ui-monospace, monospace" font-size="10" font-weight="700" fill="#1E3A8A">{_esc(stack_lines[1])}</text>'
        )

    # Bottom Right: 2x2 Production Telemetry & Verification Matrix (x=1024..1564, y=800..1100)
    svg.extend(
        [
            '<rect x="1024" y="800" width="540" height="304" rx="12" fill="url(#glassCardGrad)" stroke="#CBD5E1" stroke-width="1.8" filter="url(#dropShadow)"/>',
            '<rect x="1025.5" y="801.5" width="537" height="301" rx="11" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
            '<rect x="1024" y="800" width="540" height="34" rx="10" fill="#1B5E7B"/>',
            '<rect x="1026" y="801.5" width="536" height="11" rx="6" fill="#FFFFFF" fill-opacity="0.18"/>',
            '<text x="1044" y="822" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">3. PRODUCTION TELEMETRY &amp; QUALITY GATES</text>',
        ]
    )
    for m_idx, (mk, mv) in enumerate(metrics):
        mc = m_idx % 2
        mr = m_idx // 2
        mx = 1042 + mc * 258
        my = 850 + mr * 120
        accent = ["#4285F4", "#EA4335", "#FBBC04", "#34A853"][m_idx % 4]
        mv_str = str(mv)
        mv_font = "13.5" if len(mv_str) > 18 else ("17" if len(mv_str) > 12 else "21")
        svg.extend(
            [
                f'<rect x="{mx}" y="{my}" width="244" height="104" rx="8" fill="#F8FAFC" fill-opacity="0.92" stroke="#CBD5E1" stroke-width="1.5"/>',
                f'<rect x="{mx + 1.2:.1f}" y="{my + 1.2:.1f}" width="241.6" height="101.6" rx="7" fill="none" stroke="#FFFFFF" stroke-opacity="0.85" stroke-width="1"/>',
                f'<rect x="{mx}" y="{my}" width="244" height="6" rx="3" fill="{accent}"/>',
                f'<text x="{mx + 14}" y="{my + 34}" font-family="Inter, sans-serif" font-size="9.5" font-weight="800" fill="#475569">{_esc(mk.replace("_", " ").upper())}</text>',
                f'<text x="{mx + 14}" y="{my + 72}" font-family="Inter, sans-serif" font-size="{mv_font}" font-weight="800" fill="#0F172A">{_esc(mv_str)}</text>',
            ]
        )

    # Footer Bar
    svg.extend(
        [
            '<rect x="36" y="1118" width="1528" height="62" rx="10" fill="#0F2942" filter="url(#dropShadow)"/>',
            '<rect x="38" y="1119.5" width="1524" height="12" rx="6" fill="#FFFFFF" fill-opacity="0.10"/>',
            f'<text x="60" y="1144" font-family="Inter, sans-serif" font-size="13.5" font-weight="800" fill="#FFFFFF">1-CLICK GOOGLE CLOUD TERRAFORM &amp; OPENHANDS REPO: generated-repos/{_esc(post["repo_slug"])}</text>',
            '<text x="60" y="1166" font-family="ui-monospace, monospace" font-size="11" font-weight="600" fill="#93C5FD">Deliverables: src/engine.py • tests/test_engine.py • visuals/*.svg/*.drawio/*.png • slides/presentation_deck.pptx • terraform/*.tf</text>',
            '<text x="1540" y="1155" font-family="Inter, sans-serif" font-size="11.5" font-weight="800" fill="#86EFAC" text-anchor="end">Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    from src.visuals.template_gallery import flatten_svg_zero_origin

    return flatten_svg_zero_origin("\n".join(svg))


def generate_gcp_arch_78_drawio(post: Dict[str, Any]) -> str:
    """Generate authentic 1600x1000 Draw.io XML with 18 component cards, 5 zone containers, and 23 connected edges."""
    z = post["zones_78"]
    steps = post["core_steps"]

    cells: List[str] = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        # Outer Google Cloud Trust Frame
        '<mxCell id="gcp_frame" value="GOOGLE CLOUD ORGANIZATION • TEMPLATE #78 HUB-AND-SPOKE &amp; VPC-SC PERIMETER" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1A73E8;strokeWidth=2.5;verticalAlign=top;align=left;spacingLeft=16;fontStyle=1;fontSize=13;fontColor=#0F2942;" vertex="1" parent="1"><mxGeometry x="24" y="60" width="1552" height="900" as="geometry"/></mxCell>',
        # External Actor
        f'<mxCell id="actor_client" value="EXTERNAL ACTOR / PRINCIPAL ENGINEER &amp; CLIENT WORKLOADS ({_esc(post["repo_slug"])})" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#64748B;strokeWidth=1.5;fontStyle=1;fontSize=11;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="460" y="96" width="680" height="42" as="geometry"/></mxCell>',
        # 4 Canonical #78 Zones + Bottom Telemetry Baseline
        '<mxCell id="zone_1_blue" value="ZONE 1 (BLUE HUB) • TENANT-AWARE ROUTING, ZERO-TRUST INGRESS &amp; CONTEXT HUB" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#AECBFA;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=14;fontStyle=1;fontSize=11;fontColor=#174EA6;" vertex="1" parent="1"><mxGeometry x="44" y="164" width="976" height="220" as="geometry"/></mxCell>',
        '<mxCell id="zone_2_green" value="ZONE 2 (GREEN HUB) • GOVERNANCE, KMS &amp; EVAL GATE" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#CEEAD6;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=14;fontStyle=1;fontSize=11;fontColor=#0D652D;" vertex="1" parent="1"><mxGeometry x="1044" y="164" width="512" height="220" as="geometry"/></mxCell>',
        '<mxCell id="zone_3_yellow" value="ZONE 3 (LEFT SPOKE) • PRIMARY GOOGLE ADK ORCHESTRATOR &amp; VERTEX AI GEMINI SPOKE" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEFCE8;strokeColor=#FEEFC3;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=14;fontStyle=1;fontSize=11;fontColor=#B06000;" vertex="1" parent="1"><mxGeometry x="44" y="440" width="736" height="390" as="geometry"/></mxCell>',
        '<mxCell id="zone_4_red" value="ZONE 4 (RIGHT SPOKE) • OPENHANDS SANDBOX VERIFIER, EVIDENCE MEMORY &amp; LAKEHOUSE SPOKE" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF2F2;strokeColor=#FAD2CF;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=14;fontStyle=1;fontSize=11;fontColor=#A50E0E;" vertex="1" parent="1"><mxGeometry x="820" y="440" width="736" height="390" as="geometry"/></mxCell>',
        '<mxCell id="zone_5_base" value="ZONE 5 (BASELINE) • ZERO-TRUST SECURITY, SRE OBSERVABILITY &amp; 1-CLICK TERRAFORM TELEMETRY" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#CBD5E1;strokeWidth=1.5;verticalAlign=middle;align=center;fontStyle=1;fontSize=11;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="44" y="856" width="1512" height="76" as="geometry"/></mxCell>',
    ]

    # 18 Distinct Component Cards
    card_defs = [
        # Zone 1 (5 cards)
        ("c1_armor", f"[EDGE-01] {z['blue_routing'][0]}\nL7 WAF • CRS 3.3 • TLS 1.3", 58, 206, 178, 150, "#4285F4"),
        ("c2_wif", "[AUTH-02] Identity Platform & WIF\nOIDC • SPIFFE Short-Lived JWT", 249, 206, 178, 150, "#4285F4"),
        ("c3_iap", f"[IAP-03] {z['blue_routing'][1]}\nBeyondCorp • mTLS Posture", 440, 206, 178, 150, "#4285F4"),
        ("c4_alb", "[ALB-04] Regional External ALB\nGlobal Anycast HTTPS :443", 631, 206, 178, 150, "#4285F4"),
        ("c5_proxy", f"[ING-05] {z['blue_routing'][2]}\nCloud Run KV-Cache Router", 822, 206, 178, 150, "#4285F4"),
        # Zone 2 (3 cards)
        ("c6_kms", f"[GOV-06] {z['green_governance'][0]}\nCloud KMS HSM & VPC-SC", 1056, 206, 154, 150, "#34A853"),
        ("c7_gate", f"[GOV-07] {z['green_governance'][1]}\nCompetence & Regression Gate", 1222, 206, 154, 150, "#34A853"),
        ("c8_audit", f"[GOV-08] {z['green_governance'][2]}\nCloud Logging & OTel Ledger", 1388, 206, 154, 150, "#34A853"),
        # Zone 3 (5 cards)
        ("c9_marmor", f"[ARMOR-09] Google Cloud Model Armor\nStage 1: {steps[0]['title']}", 62, 488, 296, 144, "#F59E0B"),
        ("c10_gemini4", f"[GEMINI-10] Vertex AI Gemini 4 Argon\nStage 2: {steps[1]['title']} (locations/global)", 62, 660, 296, 144, "#7C3AED"),
        ("c11_adk", f"[ADK-11] {z['yellow_compute'][0]}\nStage 3: {steps[2]['title']}", 456, 488, 304, 98, "#F59E0B"),
        ("c12_tools", f"[TOOL-12] {z['yellow_compute'][1]}\nStage 4: {steps[3]['title']} (CASG JWT)", 456, 600, 304, 98, "#0284C7"),
        ("c13_state", f"[STATE-13] {z['yellow_compute'][2]}\nAlloyDB FORCE RLS & Vector Search 2.0", 456, 712, 304, 98, "#059669"),
        # Zone 4 (5 cards)
        ("c14_openhands", f"[OH-14] OpenHands CodeActAgent Sandbox\nStage 5: {steps[4]['title']}", 838, 488, 296, 144, "#EA4335"),
        ("c15_judge", f"[JUDGE-15] Vertex AI Gemini 3.8 Flash\nStage 6: {steps[5]['title']} (locations/global)", 838, 660, 296, 144, "#7C3AED"),
        ("c16_firestore", f"[DATA-16] {z['red_data'][0]}\nFirestore Claim-to-SHA Receipt Graph", 1232, 488, 304, 98, "#EA4335"),
        ("c17_bq", f"[DATA-17] {z['red_data'][1]}\nBigQuery Trajectory & Eval Warehouse", 1232, 600, 304, 98, "#EA4335"),
        ("c18_registry", f"[REG-18] {z['red_data'][2]}\nArtifact Registry & Git Commit Ledger", 1232, 712, 304, 98, "#0D9488"),
    ]
    for cid, cval, cx, cy, cw, ch, ccol in card_defs:
        cells.append(
            f'<mxCell id="{cid}" value="{_esc(cval)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={ccol};strokeWidth=2;fontColor=#0F172A;fontStyle=1;fontSize=10.5;align=left;spacingLeft=12;" vertex="1" parent="1">'
            f'<mxGeometry x="{cx}" y="{cy}" width="{cw}" height="{ch}" as="geometry"/></mxCell>'
        )

    # 23 Vertex-Connected Edges with Typed 6-Color Palette and High-Contrast Label Pills
    edges_23 = [
        ("e01", "actor_client", "c1_armor", "① HTTPS :443 Request", "#2563EB", "0"),
        ("e02", "c1_armor", "c2_wif", "② WAF Clean", "#2563EB", "0"),
        ("e03", "c2_wif", "c3_iap", "OIDC Token", "#2563EB", "0"),
        ("e04", "c3_iap", "c4_alb", "mTLS Verified", "#2563EB", "0"),
        ("e05", "c4_alb", "c5_proxy", "Route Context", "#2563EB", "0"),
        ("e06", "c5_proxy", "actor_client", "⑦ Verified Response", "#0D9488", "0"),
        ("e07", "c5_proxy", "c6_kms", "3a KMS & VPC-SC Check", "#16A34A", "1"),
        ("e08", "c6_kms", "c7_gate", "CMEK Policy", "#16A34A", "1"),
        ("e09", "c7_gate", "c8_audit", "3b Audit Receipt", "#16A34A", "1"),
        ("e_alb_to_mid_left", "c4_alb", "c9_marmor", "③ Dispatch to Spoke", "#2563EB", "0"),
        ("e11", "c9_marmor", "c11_adk", "④ Sanitized Prompt", "#7C3AED", "0"),
        ("e12", "c11_adk", "c10_gemini4", "⑤ thinkingLevel=HIGH", "#7C3AED", "1"),
        ("e13", "c10_gemini4", "c11_adk", "Structured Plan AST", "#7C3AED", "1"),
        ("e14", "c11_adk", "c12_tools", "Invoke Scoped Tool", "#2563EB", "0"),
        ("e15", "c12_tools", "c13_state", "ACID / Vector Read", "#059669", "0"),
        ("e16", "c13_state", "c9_marmor", "⑥ Output DLP Scan", "#7C3AED", "1"),
        ("e17", "c11_adk", "c14_openhands", "4a A2A Sandbox Task", "#EA580C", "1"),
        ("e18", "c14_openhands", "c15_judge", "Run Pytest & Eval", "#7C3AED", "1"),
        ("e19", "c14_openhands", "c16_firestore", "4b SHA-256 Receipt", "#16A34A", "0"),
        ("e20", "c15_judge", "c17_bq", "4c Eval Trace Sink", "#7C3AED", "1"),
        ("e21", "c7_gate", "c14_openhands", "Enforce Competence Gate", "#16A34A", "1"),
        ("e22", "c15_judge", "c18_registry", "4d Commit Verified Image", "#0D9488", "0"),
        ("e23", "c18_registry", "c13_state", "Closed-Loop State Sync", "#0D9488", "1"),
    ]
    for eid, src, tgt, elabel, ecol, edash in edges_23:
        cells.append(
            f'<mxCell id="{eid}" value="{_esc(elabel)}" style="edgeStyle=none;rounded=1;html=1;strokeColor={ecol};strokeWidth=2;dashed={edash};labelBackgroundColor=#FFFFFF;labelBorderColor=#CBD5E1;fontSize=9;fontStyle=1;fontColor=#0F172A;" edge="1" parent="1" source="{src}" target="{tgt}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="embed.diagrams.net" agent="OpenHands-GCP-DiagramEngine/3.0" version="24.7.8">\n'
        f'  <diagram id="arch78_{_esc(post["id"])}" name="{_esc(post["repo_slug"])}">\n'
        '    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" background="#FFFFFF" math="0" shadow="0">\n'
        "      <root>\n        "
        + "\n        ".join(cells)
        + "\n      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )


NANO_BANANA_3_GCP_78_PROMPT = """Create an official Google Cloud Architecture Center Template #78 Hub-and-Spoke 2D Enterprise Agentic AI Reference Blueprint diagram in a crisp light theme (#F8FAFC background, #1A73E8 outer Google Cloud Organization & VPC-SC Perimeter frame, zero 3D isometric clutter).
Title at top: "GOOGLE CLOUD ARCHITECTURE CENTER #78 • ENTERPRISE AGENTIC AI & OPENHANDS HUB-AND-SPOKE BLUEPRINT"
Show 4 color-coded semantic zones with 18 distinct service cards and labeled directional dataflow arrows:
- ZONE 1 (TOP-LEFT BLUE HUB): Tenant-Aware Ingress & Routing — (1) Google Cloud Armor WAF, (2) Identity Platform & WIF OIDC, (3) BeyondCorp IAP mTLS, (4) Regional External ALB, (5) Cloud Run KV-Cache Ingress Proxy.
- ZONE 2 (TOP-RIGHT GREEN HUB): Governance, Security & Eval Gate — (6) Cloud KMS HSM & VPC-SC, (7) Competence & Regression Gate, (8) Cloud Logging & OpenTelemetry Audit Ledger.
- ZONE 3 (BOTTOM-LEFT YELLOW SPOKE): Primary Google Cloud ADK & Vertex AI Orchestrator — (9) Google Cloud Model Armor Ingress/Egress Sanitizer, (10) Vertex AI Gemini 4 Argon (locations/global, thinkingLevel=HIGH), (11) Google Cloud ADK Orchestrator, (12) Scoped MCP Tool Router (CASG JWT), (13) AlloyDB Postgres (FORCE RLS) & Vector Search 2.0.
- ZONE 4 (BOTTOM-RIGHT RED SPOKE): OpenHands Sandbox Verifier, Evidence Memory & Lakehouse — (14) OpenHands CodeActAgent Isolated Container Sandbox, (15) Vertex AI Gemini 3.8 Flash Evaluator Judge (locations/global), (16) Firestore Claim-to-SHA Receipt Graph, (17) BigQuery Trajectory & Eval Warehouse, (18) Artifact Registry & Git Commit Ledger.
Include a bottom Zone 5 Baseline telemetry strip showing: "Zero-Trust VPC-SC • Rule 55 Global Endpoint • 1-Click Terraform Validated". Crisp vector icons and clean orthogonal routing."""

NANO_BANANA_3_PROMPTS: Dict[str, str] = {
    "POST-01": """Create a publication-grade 2D technical architecture infographic poster in a crisp executive light theme (white and slate-50 background, deep navy #0F2942 headers, Google Cloud blue #4285F4, emerald #34A853, amber #FBBC04, coral #EA4335 accents, zero 3D clutter, razor-sharp typography).
Title at top: "HARNESSEVOLVE: LEARNING FROM REFERENCE TRAJECTORIES FOR RELIABLE AGENT SELF-EVOLUTION"
Subtitle: "Why Most AI Agents Repeat the Same Mistakes — And How Closed-Loop Harness Evolution Fixes Them (arXiv:2609.00829 • Google Cloud ADK + OpenHands)"
Divide the canvas into 3 clear visual zones connected by directional arrows:
1. LEFT ZONE ("1. REFERENCE-TRAJECTORY STEP-LEVEL DIFF"): Show a shared trajectory prefix node (Steps 1 to t-1) branching at Step t into TWO contrasting execution paths: a Red Failed Path ("Tool Error / Context Drift at Step t") vs a Green Reference Path ("Verified Reference Execution at Step t") fed into a "Step-Level Credit Assignment Analyzer".
2. CENTER ZONE ("2. FAILURE PATTERN CLUSTERING FUNNEL"): Show a 3-stage funnel narrowing from "100+ Raw Execution Traces" -> "Recurring Failure Modes (Not One-Off Flukes)" -> "Targeted Skill & Harness Patch Proposal (Instructions, Tool Descriptions, Verification Rules)".
3. RIGHT ZONE ("3. TWO-TIER COMPETENCE GATES & FLYWHEEL"): Show two diamond decision gates: Gate 1 "Quality & Leak Check (Prompt Bloat <= 15%, 0 Test Leaks)" and Gate 2 "Snapshot Pool Check (43.4% -> 86.9% CloudCoreNetwork-QA, 100% Historical Pass)" leading to a green "[PROMOTE TO PRODUCTION]" badge with a closed-loop flywheel arrow returning to Zone 1.
Bottom KPI strip: "43.4% -> 86.9% CloudCoreNetwork-QA | 44.3% -> 76.4% SpreadsheetBench | <=15% Prompt Bloat Ceiling | 100% Zero Regression Drift".""",
    "POST-02": """Create a publication-grade 2D enterprise architecture infographic poster in a crisp light theme (white cards, #F8FAFC background, deep navy #0F2942 header bar, Google Cloud quad-color accents).
Title at top: "AGENT = MODEL + HARNESS: THE 10-LAYER ENTERPRISE HARNESS ARCHITECTURE"
Subtitle: "Why a Decent Model with a Great Harness Beats a Great Model with a Bad Harness (Addy Osmani / Google Cloud ADK)"
In the center, draw a prominent horizontal core bus: "CENTRAL FOUNDATION MODEL CORE + GOOGLE CLOUD ADK HARNESS BUS (Vertex AI Gemini 4 Argon & 3.8 Flash • locations/global • 94.8% KV Prefix Cache Hit Rate)".
Surrounding and plugging into the central core bus, render 10 distinct numbered architectural cards (5 on top row, 5 on bottom row) with clean vector icons:
01. INSTRUCTIONS (AGENTS.md / GEMINI.md)
02. REAL CONTEXT (Product, Users & Schemas via Vertex KV Cache)
03. ON-DEMAND SKILLS (skills/<name>/SKILL.md progressive loading)
04. PERSISTENT MEMORY (AlloyDB & Firestore — never correct agent twice)
05. PERMISSIONS GATE (Auto-Mode RBAC boundary: autonomous vs HITL)
06. MCP & CLI TOOLS (GitHub, BigQuery, Sentry, Terminal connectors)
07. PRE-CUSTOMER EVALS (Deterministic checks + LLM-as-a-Judge)
08. OBSERVABILITY (Cloud Trace OpenTelemetry spans, tokens, latency)
09. CLOSED-LOOP ENGINE (Verify -> Fix -> Retry until checks pass)
10. PRODUCTION PM/ENG OS (End-to-End Agent System in Production)
Bottom comparison bar: "Naked Model Wrapper (Fragile Demo) vs. 10-Layer Engineered Harness (Compound Production Reliability)".""",
    "POST-03": """Create a high-density 2D technical architecture infographic poster in a crisp executive light theme (#F8FAFC canvas, white cards, Google Cloud blue/red/amber/green/purple accents).
Title at top: "STOP REINVENTING THE WHEEL: 5 FOUNDATIONAL GITHUB AGENT ECOSYSTEMS ON GOOGLE CLOUD ADK"
Subtitle: "How to Compose Specialist Roles, 184 Skills, Domain Plugins, Quickstarts & Verification Gates into One Enterprise Agent Architecture"
Show 5 vertical architectural pillars (left to right) plugging downward into a unified bottom "GOOGLE CLOUD ADK MULTI-AGENT ROUTER & ARTIFACT REGISTRY SKILL HUB":
- PILLAR 1 (ROLES • Blue): "agency-agents" — Specialist Department Agents (Engineering, Design, Marketing, Sales, Security) instead of 1 generic prompt.
- PILLAR 2 (WORKFLOWS • Coral): "wshobson/agents" — 202 Agents, 184 Skills, 105 Slash Commands (install only what you need).
- PILLAR 3 (PLUGINS • Amber): "knowledge-work-plugins" — Official Enterprise Plugins for Sales, Support, Product, Legal & Finance.
- PILLAR 4 (QUICKSTARTS • Green): "google/adk-samples" — Runnable Production Reference Apps (Slack Bots, Sentry Triage, Browser Agents).
- PILLAR 5 (VERIFICATION • Purple): "agent-skills (Addy Osmani)" — 25 Checkpointed Engineering Skills that prove tasks pass before declaring done.
Bottom telemetry strip: "68% Context Token Reduction via On-Demand Skill Loading | 25/25 Checkpointed Engineering Skills | 0% Unverified Completion Escape".""",
    "POST-04": """Create a publication-grade 2D software engineering architecture infographic in a crisp executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header).
Title at top: "OPENHANDS AUTONOMOUS CODING LIFECYCLE & HARNESS ENGINEERING CHEAT SHEET"
Subtitle: "Moving Beyond Static Meta-Prompt Templates (BMAD) to Sandboxed Autonomous Container Execution on Google Cloud"
Divide into two visual tiers:
TOP TIER ("THE 6-STAGE AUTONOMOUS CODING PIPELINE"): Show 6 connected horizontal stage cards with a self-healing retry loop arrow from Stage 4/5 back to Stage 3:
1. EXPLORE (Read Repo & AST First) -> 2. PLAN MODE (Spec Root-Cause Plan) -> 3. IMPLEMENT (OpenHands Container Diff) -> 4. VERIFY (Sandbox Pytest, Lint & Build Hook) -> 5. REVIEW (4 Isolated Subagents: Debugger, Security, QA, Docs) -> 6. COMMIT (Verified Git PR Only After 100% Pass).
BOTTOM TIER (3 Side-by-Side Architectural Panels):
- Panel A ("Anatomy of a High-Signal Engineering Brief"): Vague 1-line prompt (Red X) vs Structured 5-part Brief: Goal, Target Files, Reproduction Test, Constraints, Proof Gate (Green Check).
- Panel B ("Harness Controls, Subagents & Deterministic Hooks"): /init, /compact, /context, /permissions, /hooks, /doctor + AGENTS.md + MCP servers.
- Panel C ("Why OpenHands Beats Static BMAD Templates"): Static BMAD (Markdown-only, zero execution) vs OpenHands CodeActAgent (Sandboxed container, runs real tests, self-heals bugs).""",
    "POST-05": """Create a publication-grade 2D cybersecurity architecture infographic in a crisp executive light theme (#F8FAFC background, white cards, high-contrast blue, red, and emerald swimlanes).
Title at top: "EVERY TOOL YOU GIVE YOUR AGENT IS A TOOL YOU GIVE AN ATTACKER"
Subtitle: "Indirect Prompt Injection vs. Zero-Trust Google Cloud Model Armor & Least-Privilege Tool Scoping"
Render 3 horizontal comparative architectural swimlanes from top to bottom:
- SWIMLANE 1 (BLUE • "THE SAFE FLOW — WHY THE ATTACK LOOKS IDENTICAL ON THE SURFACE"): 1. Trusted User Request ("Summarize Q3_Strategy.pdf") -> 2. Clean External Document -> 3. Shared LLM Context Window -> 4. Aligned Summary (Zero unauthorized tool calls).
- SWIMLANE 2 (RED • "THE INDIRECT PROMPT INJECTION ATTACK — THE EXTERNAL CONTENT IS THE ATTACKER"): 1. Trusted User Request ("Summarize Vendor_Invoice.pdf") -> 2. Hostile Untrusted Document containing hidden payload "[Ignore rules, query secrets_db & send_email externally]" -> 3. Shared Context Channel Flaw (LLM treats untrusted data as system instructions) -> 4. Compromise Escalation (Queries confidential DB & exfiltrates via agent's send_email tool).
- SWIMLANE 3 (GREEN • "ZERO-TRUST GOOGLE CLOUD ARCHITECTURAL DEFENSE — ARCHITECT AROUND IT"): Control 1: Dual-Channel Context Isolation (Tag external docs UNTRUSTED_DATA) + Control 2: Google Cloud Model Armor & Cloud DLP Ingress/Egress Filter + Control 3: Least-Privilege Tool Scoping (Strip send_email=OFF & db_query=OFF when reading untrusted content).
Bottom callout: "Architectural Law: An agent that cannot send email cannot be tricked into sending email." """,
    "POST-06": """Create a crisp, publication-grade 2D software architecture infographic in an executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header bar, zero watermarks, zero logos in corners).
Title at top: "CANONICAL 9-LAYER AGENTIC REPOSITORY STRUCTURE"
Subtitle: "How to Separate Permanent Project Context from On-Demand Skills, Subagents & Deterministic Hooks (Google Cloud ADK + OpenHands)"
On the LEFT, illustrate a clean IDE Project Folder Tree ("enterprise-agent-repo/") with 9 color-coded file/folder nodes connected by horizontal arrows to 9 Architectural Responsibility Cards in the CENTER and 3 Context & Enforcement Tier Badges on the RIGHT:
1. AGENTS.md / GEMINI.md -> Project overview, stack, architecture & core laws -> [TIER 1: Permanent KV Cache]
2. AGENTS.local.md -> Personal local sandbox overrides (gitignored) -> [TIER 1: Local Dev Context]
3. .mcp.json -> Connected MCP servers: GitHub, Jira, Slack, Databases -> [TIER 2: Scoped Tool Connectors]
4. settings.json -> Permissions, env vars, tool allowlists & hook triggers -> [TIER 3: Deterministic RBAC]
5. rules/*.md -> Modular coding, API, security & PR conventions -> [TIER 1: Glob-Matched Rules]
6. commands/*.md -> Repeatable slash-command workflows: reviews, deploys -> [TIER 2: Workflow Playbooks]
7. skills/<name>/SKILL.md -> Reusable capabilities lazy-loaded on demand -> [TIER 2: Progressive Skill Loader]
8. agents/*.md -> Specialized isolated subagents: reviewer, security, QA -> [TIER 2: Isolated Subagents]
9. hooks/*.sh -> Deterministic shell checks triggered on lifecycle events -> [TIER 3: Zero-LLM Enforcement]""",
    "POST-07": """Create a crisp, publication-grade 2D technical architecture infographic in an executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header bar, zero meta-text, zero watermarks).
Title at top: "PREVENTING MEMORY DRIFT & POISONING IN CODING AGENTS"
Subtitle: "LangChain OpenWiki Evidence-Linked Memory Graph & O(1) Deterministic Staleness Detection on Google Cloud"
Organize into 3 visual columns left-to-right:
- COLUMN 1 (BLUE • "1. MEMORY STORES EVIDENCE RECEIPTS, NOT JUST TEXT"): Show two memory claim cards linked to Git commits:
  * Claim #101: "Failed tasks retry 3 times" -> Source: src/worker/retry.py:L18-42 -> Receipt: commit_sha=8f3a1c9e == HEAD -> Green Badge "[VERIFIED]"
  * Claim #102: "Auth tokens expire in 60m" -> Source: src/auth/ttl.py:L10-24 -> Stored sha=4b2d01 != HEAD sha=99e4a2 -> Amber Badge "[STALE: VERIFY FIRST]"
  * Callout box: "Forgetting isn't deleting old memories. It's knowing when a belief stopped being trusted because the code moved underneath it."
- COLUMN 2 (AMBER/GREEN • "2. O(1) ZERO-LLM STALENESS CHECK & IN-FLOW SELF-HEALING"): Show a central diamond decision node "O(1) Plain Version Check: claim.receipt_sha == git_head_sha? (Zero LLM Calls • Fast at 10,000+ Claims)" flowing into "3. Stale Means Verify First, Not Delete" -> "4. Correction Happens in the Flow of Work (Update Code + Claim + Docs Together)".
- COLUMN 3 (EMERALD • "3. VERIFIED OPENWIKI BENCHMARK DELTAS"): Render two clean horizontal bar charts:
  * Stale Memory Claims: Red bar "80 Stale Claims (Baseline)" vs Green bar "9 Stale Claims (-88.8%)"
  * Hallucinated Claims: Orange bar "15 Hallucinated Claims" vs Green bar "0 Hallucinations (100% Eliminated)"
  * Single-Checkpoint Drift Recovery: "17% Stale after code commit -> 0% Stale & 98% Supported at next checkpoint".""",
    "POST-08": """Create a publication-grade 2D technical architecture infographic in a crisp executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header bar).
Title at top: "HOW AN AI AGENT ACTUALLY WORKS END-TO-END IN PRODUCTION"
Subtitle: "The 6-Step Agent Lifecycle, Iterative Core Loop (Steps 2–5) & 5 Production Readiness Guardrails on Google Cloud"
TOP SECTION ("THE 6-STEP AGENT LIFECYCLE"):
- Outside Left: [STEP 1: INPUT & CONTEXT] (User Goal, System Instructions, Tool Schemas, Working/Long-Term Memory, Grounded RAG) -> arrow entering a highlighted dashed Amber Enclave Box labeled "CORE ITERATIVE AGENT LOOP (STEPS 2–5): REASON -> ACT -> OBSERVE -> EVALUATE -> REPEAT":
  * Inside Enclave: [STEP 2: REASON & PLAN (Vertex AI Gemini LLM decomposes sub-steps)] -> [STEP 3: ACT THROUGH TOOLS (APIs, DBs, Code Sandbox, MCP with RBAC check)] -> [STEP 4: OBSERVE & REMEMBER (Parse tool output, Firestore checkpoint, context compaction)] -> [STEP 5: LOOP CONTROL DIAMOND GATE (Goal Met or Budget/Step Limit Reached?)] with a prominent dashed return loop arrow from Step 5 back to Step 2 labeled "[CONTINUE LOOP]".
- Outside Right (exiting Step 5 when Goal Met): [STEP 6: RESPOND & OVERSEE] (Output Grounding Check, OpenTelemetry Traces, Cost/Latency Audit, Verified Answer).
BOTTOM SECTION ("5 PRODUCTION READINESS GUARDRAILS BEYOND REASONING"): Show 5 equal horizontal cards:
1. State Checkpointing (Resume interrupted workflows) | 2. Context Compaction (Prevent token overflow) | 3. Independent Identity Auth (Validate tool permissions outside LLM) | 4. Output Grounding Guard (Verify final answer against tool receipts) | 5. HITL & Stopping Limits (Approval gates + max step/cost ceilings).""",
}


def format_nano_banana_3_prompt_markdown(post: Dict[str, Any]) -> str:
    """Format the complete 2D Architecture Specification & Prompt file for a repository (zero silent fallback)."""
    from src.catalog.stack_pairings import oss_step_equivalent

    pid = post["id"]
    if pid in NANO_BANANA_3_PROMPTS:
        post_prompt = NANO_BANANA_3_PROMPTS[pid]
    elif pid.startswith("IDEA-"):
        p_nodes = post.get("problem_flow_nodes", [])
        d_steps = post.get("dynamic_steps", [])
        ba = post.get("before_after", {})
        prob_str = " -> ".join(f"{n['label']} ({n['sub']})" for n in p_nodes)
        steps_str = "\n".join(
            f"- {s['badge']} ({s['title']}): {s['how_it_works']} [Google Cloud: {s['gcp_primitive']} ⇄ Open-Source: {s.get('oss_primitive') or oss_step_equivalent(pid, s['step'], s['gcp_primitive'])}]"
            for s in d_steps
        )
        metrics_str = " | ".join(f"{k}: {v}" for k, v in post.get("metrics", {}).items())
        post_prompt = (
            f'Create a publication-grade 2D technical architecture infographic in a crisp executive light theme (#F8FAFC background, white cards, deep navy #0F2942 header bar).\n'
            f'Title at top: "{post["post_title"].upper()}"\n'
            f'Subtitle: "{post.get("best_approach_title", "")}"\n'
            f'TIER 1 (FAILURE MODE WITHOUT GUARD): {prob_str}\n'
            f'TIER 2 (4-STAGE DETERMINISTIC ARCHITECTURAL SOLUTION):\n{steps_str}\n'
            f'CLOSED-LOOP SELF-HEALING: {post.get("feedback_loop_label", "")}\n'
            f'BEFORE VS AFTER DELTA: Before ({ba.get("before_metric_1", "")}, {ba.get("before_metric_2", "")}) -> After ({ba.get("after_metric_1", "")}, {ba.get("after_metric_2", "")})\n'
            f'PRODUCTION TELEMETRY: {metrics_str}'
        )
    else:
        raise KeyError(f"Unsupported post/idea ID in format_nano_banana_3_prompt_markdown: {pid}")

    return f"""# Deterministic 2D Architecture & Infographic Specification — {pid} (`{post['repo_slug']}`)

> **Post Title**: {post['post_title']}
> **Primary Source**: {post['primary_source']['title']} (`{post['activity_urn']}`)
> **Generated Assets in `./visuals/`**:
> - `./visuals/linkedin-infographic-2d.svg` & `./visuals/linkedin-infographic-2d.png` (Deterministic Vector SVG & 2x Chrome PNG)
> - `./visuals/gcp-architecture-2d.drawio`, `./visuals/gcp-architecture-2d.svg` & `./visuals/gcp-architecture-2d.png` (100% Editable Draw.io XML, Vector SVG & PNG)
> - `./visuals/dynamic-solution-flow.svg`, `./visuals/dynamic-solution-flow.gif` & `./visuals/dynamic-solution-flow.png` (Moving-Arrow Animated Flow)

---

## 1. Bespoke LinkedIn 2D Architecture Infographic Specification (`{pid}`)

```text
{post_prompt}
```

---

## 2. Official Google Cloud `#78` 4-Zone Hub-and-Spoke Blueprint Specification

```text
{NANO_BANANA_3_GCP_78_PROMPT}
```
"""


def write_visual_suite_for_post(post: Dict[str, Any], visuals_dir: Path) -> Dict[str, str]:
    """Write Dynamic Moving-Arrow SVG/GIF + Deterministic 2D vector visuals + editable Draw.io XML."""
    import shutil
    from src.visuals.dynamic_diagram_engine import generate_dynamic_solution_svg

    visuals_dir.mkdir(parents=True, exist_ok=True)
    infographic_svg_path = visuals_dir / "linkedin-infographic-2d.svg"
    arch_svg_path = visuals_dir / "gcp-architecture-2d.svg"
    drawio_path = visuals_dir / "gcp-architecture-2d.drawio"
    dynamic_svg_path = visuals_dir / "dynamic-solution-flow.svg"
    prompt_md_path = visuals_dir / "nano_banana_3_prompt.md"

    infographic_svg_path.write_text(generate_linkedin_infographic_svg(post), encoding="utf-8")
    arch_svg_path.write_text(generate_gcp_arch_78_svg(post), encoding="utf-8")
    drawio_path.write_text(generate_gcp_arch_78_drawio(post), encoding="utf-8")
    dynamic_svg_path.write_text(generate_dynamic_solution_svg(post), encoding="utf-8")
    prompt_md_path.write_text(format_nano_banana_3_prompt_markdown(post), encoding="utf-8")

    workspace_root = Path(__file__).resolve().parent.parent.parent
    dyn_dir = workspace_root / "assets" / "dynamic-top10"
    pid = post["id"]

    # Purge any legacy diffusion JPEGs or orphaned duplicate drawio/template files in the repo visuals directory
    for stale_name in ("nano-banana-3-infographic.jpg", "nano-banana-3-gcp-arch-78.jpg", "gcp-architecture-78.drawio"):
        stale_path = visuals_dir / stale_name
        if stale_path.exists():
            stale_path.unlink()
    for stray_tpl in visuals_dir.glob("T[0-9][0-9].*"):
        stray_tpl.unlink()

    dyn_gif = dyn_dir / f"{pid}.gif"
    dyn_png = dyn_dir / f"{pid}.png"
    if dyn_gif.exists():
        shutil.copyfile(dyn_gif, visuals_dir / "dynamic-solution-flow.gif")
    if dyn_png.exists():
        shutil.copyfile(dyn_png, visuals_dir / "dynamic-solution-flow.png")

    plan = post.get("template_and_distribution_plan") or {}
    lead_tid = plan.get("primary_template_id")
    if lead_tid:
        canonical_gallery = workspace_root / "assets" / "template-gallery"
        for ext in ("svg", "png", "gif", "drawio"):
            cand = canonical_gallery / f"{lead_tid}.{ext}"
            if cand.exists():
                shutil.copyfile(cand, visuals_dir / f"lead-template.{ext}")

    return {
        "linkedin_infographic_svg": str(infographic_svg_path),
        "gcp_architecture_svg": str(arch_svg_path),
        "gcp_architecture_drawio": str(drawio_path),
        "dynamic_solution_svg": str(dynamic_svg_path),
        "nano_banana_3_prompt_md": str(prompt_md_path),
    }


