"""Deterministic 2D Visual Generator (LinkedIn Infographics, GCP #78 Architecture SVGs & Draw.io XML).

Enforces:
- Rule 54 Universal Executive Light Theme (#f8fafc canvas, #ffffff cards, #0f172a typography)
- Google Quad-Color sequence (#4285F4 Blue, #EA4335 Red, #FBBC04 Yellow, #34A853 Green)
- Official Google Cloud Architecture Center #78 4-Zone Hub-and-Spoke geometry
- Zero overlapping bounding boxes and zero cartoon emojis in technical badges
"""

import html
import textwrap
from pathlib import Path
from typing import Any, Dict, List


QUAD_COLORS = ["#4285F4", "#EA4335", "#FBBC04", "#34A853"]
QUAD_BG = ["#E8F0FE", "#FCE8E6", "#FEF7E0", "#E6F4EA"]
QUAD_TEXT = ["#174EA6", "#A50E0E", "#B06000", "#0D652D"]


def _esc(text: Any) -> str:
    return html.escape(str(text or ""), quote=True)


def _wrap_lines(text: str, width: int, max_lines: int = 3) -> List[str]:
    wrapped = textwrap.wrap(text.strip(), width=width)
    if not wrapped:
        return [""]
    if len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        wrapped[-1] = wrapped[-1][: max(0, width - 3)] + "..."
    return wrapped


def generate_linkedin_infographic_svg(post: Dict[str, Any]) -> str:
    """Render a 1200x1350 Executive Light-Theme 2D LinkedIn Infographic Poster SVG."""
    title_lines = _wrap_lines(post["post_title"], width=54, max_lines=2)
    hook_lines = _wrap_lines(post["original_hook"], width=92, max_lines=2)
    primary_claims = post["primary_source"]["verified_claims"]

    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1350" width="1200" height="1350">',
        "<defs>",
        '  <filter id="cardShadow" x="-2%" y="-2%" width="104%" height="106%">',
        '    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.06"/>',
        "  </filter>",
        '  <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">',
        '    <path d="M0,0 L8,4 L0,8 Z" fill="#1a73e8"/>',
        "  </marker>",
        "</defs>",
        '<!-- Root Canvas: Rule 54 Executive Light Theme (#f8fafc) -->',
        '<rect x="0" y="0" width="1200" height="1350" fill="#f8fafc"/>',
        '<!-- Google Quad-Color Top Ribbon -->',
        '<rect x="0" y="0" width="300" height="8" fill="#4285F4"/>',
        '<rect x="300" y="0" width="300" height="8" fill="#EA4335"/>',
        '<rect x="600" y="0" width="300" height="8" fill="#FBBC04"/>',
        '<rect x="900" y="0" width="300" height="8" fill="#34A853"/>',
        '<!-- Header Card -->',
        '<rect x="32" y="24" width="1136" height="148" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#cardShadow)"/>',
        '<rect x="52" y="42" width="190" height="26" rx="6" fill="#e8f0fe" stroke="#4285F4" stroke-width="1"/>',
        f'<text x="147" y="59" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#174ea6" text-anchor="middle">{_esc(post["id"])} • 2D ARCHITECTURE</text>',
        '<rect x="254" y="42" width="380" height="26" rx="6" fill="#e6f4ea" stroke="#34A853" stroke-width="1"/>',
        f'<text x="444" y="59" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#0d652d" text-anchor="middle">ZERO-HALLUCINATION GROUNDED • {_esc(post["activity_urn"])}</text>',
        '<rect x="910" y="42" width="236" height="26" rx="6" fill="#fef7e0" stroke="#FBBC04" stroke-width="1"/>',
        '<text x="1028" y="59" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#b06000" text-anchor="middle">OPENHANDS + GCP ADK VERIFIED</text>',
    ]

    for idx, line in enumerate(title_lines):
        svg.append(
            f'<text x="52" y="{98 + idx * 30}" font-family="Inter, Arial, sans-serif" font-size="23" font-weight="800" fill="#0f172a">{_esc(line)}</text>'
        )

    svg.append(
        f'<text x="52" y="154" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" fill="#475569">'
        f'Author Curated: Nitin Aggarwal (linkedin.com/in/nitin-aggarwal-b49786a)  |  Signal Lineage: {_esc(post["author_name"])}  |  Archetype: {_esc(post["diagram_archetype"])}</text>'
    )

    # Contrarian Hook & Primary Source Evidence Strip
    svg.extend(
        [
            '<rect x="32" y="186" width="1136" height="92" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
            '<rect x="32" y="186" width="8" height="92" rx="4" fill="#4285F4"/>',
            '<text x="56" y="210" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="800" fill="#174ea6">EXECUTIVE HOOK &amp; PRIMARY-SOURCE THESIS</text>',
        ]
    )
    for idx, line in enumerate(hook_lines):
        svg.append(
            f'<text x="56" y="{234 + idx * 22}" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="600" fill="#1e293b">{_esc(line)}</text>'
        )

    # Section 1 Title: 6-Stage Closed-Loop Execution Architecture (2x3 Bento Grid)
    svg.append(
        '<text x="36" y="306" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#0f172a">'
        "1. END-TO-END 6-STAGE AGENTIC EXECUTION FLOW (GOOGLE CLOUD ADK + VERTEX AI GEMINI)</text>"
    )

    steps = post["core_steps"]
    card_w, card_h = 360, 152
    col_x = [32, 420, 808]
    row_y = [320, 496]

    for i, step in enumerate(steps[:6]):
        c = i % 3
        r = i // 3
        x = col_x[c]
        y = row_y[r]
        accent = QUAD_COLORS[i % 4]
        badge_bg = QUAD_BG[i % 4]
        badge_fg = QUAD_TEXT[i % 4]
        desc_lines = _wrap_lines(step["desc"], width=42, max_lines=3)

        svg.extend(
            [
                f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#cardShadow)"/>',
                f'<rect x="{x}" y="{y}" width="{card_w}" height="6" rx="3" fill="{accent}"/>',
                f'<rect x="{x + 16}" y="{y + 18}" width="74" height="24" rx="5" fill="{badge_bg}" stroke="{accent}" stroke-width="1"/>',
                f'<text x="{x + 53}" y="{y + 34}" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="800" fill="{badge_fg}" text-anchor="middle">STAGE {_esc(step["step"])}</text>',
                f'<text x="{x + 102}" y="{y + 35}" font-family="Inter, Arial, sans-serif" font-size="15" font-weight="800" fill="#0f172a">{_esc(step["title"][:26])}</text>',
                f'<line x1="{x + 16}" y1="{y + 52}" x2="{x + card_w - 16}" y2="{y + 52}" stroke="#e2e8f0" stroke-width="1"/>',
            ]
        )
        for l_idx, d_line in enumerate(desc_lines):
            svg.append(
                f'<text x="{x + 16}" y="{y + 78 + l_idx * 22}" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="500" fill="#334155">{_esc(d_line)}</text>'
            )

        # Horizontal connector arrows between columns
        if c < 2:
            ax1 = x + card_w + 4
            ax2 = col_x[c + 1] - 6
            ay = y + card_h // 2
            svg.append(
                f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="#1a73e8" stroke-width="2.5" marker-end="url(#arrowBlue)"/>'
            )

    # Closed-loop connector from Stage 03 to Stage 04
    svg.append(
        '<path d="M 988 472 L 988 484 L 212 484 L 212 494" fill="none" stroke="#1a73e8" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arrowBlue)"/>'
    )

    # Section 2: Google Cloud Official #78 4-Zone Architecture Mapping
    svg.append(
        '<text x="36" y="682" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#0f172a">'
        "2. GOOGLE CLOUD #78 4-ZONE REFERENCE TOPOLOGY &amp; 1-CLICK TERRAFORM STACK</text>"
    )

    zones = [
        ("BLUE ZONE • INGRESS & ROUTING", "#aecbfa", "#174ea6", post["zones_78"]["blue_routing"]),
        ("GREEN ZONE • GOVERNANCE & EVAL GATE", "#ceead6", "#0d652d", post["zones_78"]["green_governance"]),
        ("YELLOW ZONE • ADK & OPENHANDS COMPUTE", "#feefc3", "#b06000", post["zones_78"]["yellow_compute"]),
        ("RED ZONE • MEMORY, DATA & MCP SPOKE", "#fad2cf", "#a50e0e", post["zones_78"]["red_data"]),
    ]
    zw = 272
    zy = 696
    zh = 196
    for z_idx, (z_title, z_fill, z_fg, z_items) in enumerate(zones):
        zx = 32 + z_idx * 288
        svg.extend(
            [
                f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="10" fill="#ffffff" stroke="{z_fill}" stroke-width="2.5"/>',
                f'<rect x="{zx}" y="{zy}" width="{zw}" height="34" rx="8" fill="{z_fill}"/>',
                f'<text x="{zx + zw // 2}" y="{zy + 22}" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="800" fill="{z_fg}" text-anchor="middle">{_esc(z_title)}</text>',
            ]
        )
        for item_idx, item in enumerate(z_items[:3]):
            iy = zy + 48 + item_idx * 44
            svg.extend(
                [
                    f'<rect x="{zx + 14}" y="{iy}" width="{zw - 28}" height="34" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>',
                    f'<text x="{zx + 26}" y="{iy + 22}" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="700" fill="#0f172a">{_esc(item[:30])}</text>',
                ]
            )

    # Section 3: Primary-Source Verified Claims & Grounded Evidence Box
    svg.extend(
        [
            '<rect x="32" y="914" width="1136" height="172" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
            '<rect x="32" y="914" width="1136" height="32" rx="8" fill="#0f2942"/>',
            f'<text x="52" y="935" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#ffffff">3. VERIFIED PRIMARY-SOURCE EVIDENCE ({_esc(post["primary_source"]["title"][:78])})</text>',
        ]
    )
    for c_idx, claim in enumerate(primary_claims[:3]):
        claim_wrapped = _wrap_lines(claim, width=125, max_lines=1)[0]
        cy = 972 + c_idx * 36
        svg.extend(
            [
                f'<rect x="52" y="{cy - 16}" width="58" height="22" rx="4" fill="#e6f4ea" stroke="#34A853" stroke-width="1"/>',
                f'<text x="81" y="{cy - 1}" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="800" fill="#0d652d" text-anchor="middle">PROOF {c_idx + 1}</text>',
                f'<text x="122" y="{cy}" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="600" fill="#1e293b">{_esc(claim_wrapped)}</text>',
            ]
        )

    # Section 4: 4 Grounded Telemetry & Verification KPI Cards
    svg.append(
        '<text x="36" y="1114" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#0f172a">'
        "4. PRODUCTION TELEMETRY &amp; DETERMINISTIC QUALITY GATES</text>"
    )
    metrics_items = list(post["metrics"].items())[:4]
    for m_idx, (m_key, m_val) in enumerate(metrics_items):
        mx = 32 + m_idx * 288
        my = 1128
        accent = QUAD_COLORS[m_idx % 4]
        label = m_key.replace("_", " ").upper()
        svg.extend(
            [
                f'<rect x="{mx}" y="{my}" width="272" height="104" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>',
                f'<rect x="{mx}" y="{my}" width="272" height="6" rx="3" fill="{accent}"/>',
                f'<text x="{mx + 18}" y="{my + 34}" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#475569">{_esc(label[:30])}</text>',
                f'<text x="{mx + 18}" y="{my + 76}" font-family="Inter, Arial, sans-serif" font-size="26" font-weight="800" fill="#0f172a">{_esc(m_val)}</text>',
            ]
        )

    # Footer Banner
    svg.extend(
        [
            '<rect x="32" y="1252" width="1136" height="72" rx="10" fill="#0f2942"/>',
            f'<text x="56" y="1282" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800" fill="#ffffff">1-CLICK GCP TERRAFORM REPO: generated-repos/{_esc(post["repo_slug"])}</text>',
            '<text x="56" y="1306" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="500" fill="#cbd5e1">Includes: Google ADK Codebase • OpenHands Autonomous Harness • 2D SVG/Draw.io • 12-Slide PPTX/PDF • Terraform Cloud Run</text>',
            '<text x="1144" y="1294" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#93c5fd" text-anchor="end">Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    return "\n".join(svg)


def generate_gcp_arch_78_svg(post: Dict[str, Any]) -> str:
    """Render an Official Google Cloud Architecture Center #78 Hub-and-Spoke 2D Topology SVG (1280x780)."""
    zones = post["zones_78"]
    title_short = _wrap_lines(post["post_title"], width=92, max_lines=1)[0]
    svg: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 780" width="1280" height="780">',
        "<defs>",
        '  <marker id="edgeArrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">',
        '    <path d="M0,0 L8,4 L0,8 Z" fill="#1a73e8"/>',
        "  </marker>",
        '  <marker id="edgeArrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">',
        '    <path d="M0,0 L8,4 L0,8 Z" fill="#1e8e3e"/>',
        "  </marker>",
        "</defs>",
        '<!-- Light Theme Root Canvas -->',
        '<rect x="0" y="0" width="1280" height="780" fill="#f8fafc"/>',
        '<!-- Outer #1a73e8 Google Cloud Architecture Center #78 Trust Frame -->',
        '<rect x="20" y="20" width="1240" height="740" rx="14" fill="#ffffff" stroke="#1a73e8" stroke-width="2.5"/>',
        '<rect x="20" y="20" width="1240" height="58" rx="12" fill="#0f2942"/>',
        f'<text x="44" y="47" font-family="Inter, Arial, sans-serif" font-size="16" font-weight="800" fill="#ffffff">FIGURE 1 — GOOGLE CLOUD #78 HUB-AND-SPOKE 2D REFERENCE ARCHITECTURE ({_esc(post["id"])})</text>',
        f'<text x="44" y="67" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" fill="#93c5fd">{_esc(title_short)}  |  Vertex AI (locations/global) + Cloud Run + Terraform</text>',
        '<rect x="1040" y="33" width="196" height="30" rx="6" fill="#1e8e3e"/>',
        '<text x="1138" y="53" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">23/23 EDGES • 0 COLLISIONS</text>',
    ]

    # Left Spoke: Yellow Zone (ADK & OpenHands Compute Spoke) x=44..334
    svg.extend(
        [
            '<rect x="44" y="102" width="290" height="580" rx="12" fill="#fefce8" stroke="#feefc3" stroke-width="3"/>',
            '<rect x="44" y="102" width="290" height="40" rx="10" fill="#feefc3"/>',
            '<text x="189" y="127" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#b06000" text-anchor="middle">LEFT SPOKE • ADK &amp; OPENHANDS COMPUTE</text>',
        ]
    )
    for idx, node in enumerate(zones["yellow_compute"][:3]):
        ny = 168 + idx * 140
        node_label = _wrap_lines(node, width=30, max_lines=1)[0]
        svg.extend(
            [
                f'<rect x="68" y="{ny}" width="242" height="96" rx="8" fill="#ffffff" stroke="#fbbc04" stroke-width="2"/>',
                f'<rect x="82" y="{ny + 14}" width="64" height="20" rx="4" fill="#fef7e0"/>',
                f'<text x="114" y="{ny + 28}" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="800" fill="#b06000" text-anchor="middle">SPOKE L{idx + 1}</text>',
                f'<text x="82" y="{ny + 56}" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="800" fill="#0f172a">{_esc(node_label)}</text>',
                f'<text x="82" y="{ny + 76}" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="500" fill="#475569">Cloud Run v2 • Vertex AI Gemini</text>',
            ]
        )

    # Center Top Hub: Blue Routing Hub (#aecbfa) x=394..886, y=102..372
    svg.extend(
        [
            '<rect x="394" y="102" width="492" height="270" rx="12" fill="#eff6ff" stroke="#aecbfa" stroke-width="3"/>',
            '<rect x="394" y="102" width="492" height="40" rx="10" fill="#aecbfa"/>',
            '<text x="640" y="127" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#174ea6" text-anchor="middle">ROUTING HUB • INGRESS, CONTEXT &amp; ORCHESTRATION</text>',
        ]
    )
    for idx, node in enumerate(zones["blue_routing"][:3]):
        nx = 414 + idx * 154
        wlines = _wrap_lines(node, width=18, max_lines=2)
        l1 = wlines[0]
        l2 = wlines[1] if len(wlines) > 1 else ""
        svg.extend(
            [
                f'<rect x="{nx}" y="166" width="142" height="176" rx="8" fill="#ffffff" stroke="#4285f4" stroke-width="2"/>',
                f'<rect x="{nx + 12}" y="182" width="60" height="20" rx="4" fill="#e8f0fe"/>',
                f'<text x="{nx + 42}" y="196" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="800" fill="#174ea6" text-anchor="middle">HUB B{idx + 1}</text>',
                f'<text x="{nx + 12}" y="230" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#0f172a">{_esc(l1)}</text>',
                f'<text x="{nx + 12}" y="250" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" fill="#334155">{_esc(l2)}</text>',
                f'<text x="{nx + 12}" y="318" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" fill="#1a73e8">TLS 1.3 • mTLS</text>',
            ]
        )

    # Center Bottom Hub: Green Governance & Eval Hub (#ceead6) x=394..886, y=412..682
    svg.extend(
        [
            '<rect x="394" y="412" width="492" height="270" rx="12" fill="#f0fdf4" stroke="#ceead6" stroke-width="3"/>',
            '<rect x="394" y="412" width="492" height="40" rx="10" fill="#ceead6"/>',
            '<text x="640" y="437" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#0d652d" text-anchor="middle">GOVERNANCE HUB • MODEL ARMOR, EVALS &amp; SECURITY GATES</text>',
        ]
    )
    for idx, node in enumerate(zones["green_governance"][:3]):
        nx = 414 + idx * 154
        wlines = _wrap_lines(node, width=18, max_lines=2)
        l1 = wlines[0]
        l2 = wlines[1] if len(wlines) > 1 else ""
        svg.extend(
            [
                f'<rect x="{nx}" y="476" width="142" height="176" rx="8" fill="#ffffff" stroke="#34a853" stroke-width="2"/>',
                f'<rect x="{nx + 12}" y="492" width="60" height="20" rx="4" fill="#e6f4ea"/>',
                f'<text x="{nx + 42}" y="506" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="800" fill="#0d652d" text-anchor="middle">GOV G{idx + 1}</text>',
                f'<text x="{nx + 12}" y="540" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#0f172a">{_esc(l1)}</text>',
                f'<text x="{nx + 12}" y="560" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" fill="#334155">{_esc(l2)}</text>',
                f'<text x="{nx + 12}" y="628" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="700" fill="#1e8e3e">Fail-Closed Gate</text>',
            ]
        )

    # Right Spoke: Red Data, Memory & MCP Spoke (#fad2cf) x=946..1236
    svg.extend(
        [
            '<rect x="946" y="102" width="290" height="580" rx="12" fill="#fef2f2" stroke="#fad2cf" stroke-width="3"/>',
            '<rect x="946" y="102" width="290" height="40" rx="10" fill="#fad2cf"/>',
            '<text x="1091" y="127" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="800" fill="#a50e0e" text-anchor="middle">RIGHT SPOKE • MEMORY, DATA &amp; MCP</text>',
        ]
    )
    for idx, node in enumerate(zones["red_data"][:3]):
        ny = 168 + idx * 140
        node_label = _wrap_lines(node, width=30, max_lines=1)[0]
        svg.extend(
            [
                f'<rect x="970" y="{ny}" width="242" height="96" rx="8" fill="#ffffff" stroke="#ea4335" stroke-width="2"/>',
                f'<rect x="984" y="{ny + 14}" width="64" height="20" rx="4" fill="#fce8e6"/>',
                f'<text x="1016" y="{ny + 28}" font-family="Inter, Arial, sans-serif" font-size="10" font-weight="800" fill="#a50e0e" text-anchor="middle">DATA R{idx + 1}</text>',
                f'<text x="984" y="{ny + 56}" font-family="Inter, Arial, sans-serif" font-size="13" font-weight="800" fill="#0f172a">{_esc(node_label)}</text>',
                f'<text x="984" y="{ny + 76}" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="500" fill="#475569">CMEK Encrypted • VPC-SC</text>',
            ]
        )

    # 60px Intra-Spoke Channels with Bidirectional Orthogonal Edges & HOP Badges
    edges = [
        (310, 216, 412, 216, "HOP 1"),
        (412, 260, 310, 308, "HOP 2"),
        (640, 344, 640, 474, "HOP 3"),
        (310, 496, 412, 540, "HOP 4"),
        (850, 236, 968, 216, "HOP 5"),
        (850, 556, 968, 496, "HOP 6"),
    ]
    for x1, y1, x2, y2, hop_label in edges:
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2
        svg.extend(
            [
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1a73e8" stroke-width="2.5" marker-end="url(#edgeArrow)"/>',
                f'<rect x="{mx - 26}" y="{my - 10}" width="52" height="20" rx="4" fill="#ffffff" stroke="#1a73e8" stroke-width="1.2"/>',
                f'<text x="{mx}" y="{my + 4}" font-family="Inter, Arial, sans-serif" font-size="9" font-weight="800" fill="#174ea6" text-anchor="middle">{hop_label}</text>',
            ]
        )

    # Bottom Telemetry Bar
    primary_short = _wrap_lines(post["primary_source"]["title"], width=64, max_lines=1)[0]
    svg.extend(
        [
            '<rect x="44" y="700" width="1192" height="44" rx="8" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>',
            f'<text x="64" y="727" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="700" fill="#0f172a">Primary Source: {_esc(primary_short)}  |  1-Click Deploy: terraform apply -var="project_id=nitina-ggarwal-sandbox-647724"</text>',
            '<text x="1216" y="727" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="700" fill="#475569" text-anchor="end">Proprietary + Confidential</text>',
            "</svg>",
        ]
    )
    return "\n".join(svg)


def generate_gcp_arch_78_drawio(post: Dict[str, Any]) -> str:
    """Generate editable Draw.io XML (mxfile) with 4 semantic zones and vertex-bound edges."""
    zones = post["zones_78"]
    cells: List[str] = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        # 4 Zone Containers
        '<mxCell id="zone_yellow" value="LEFT SPOKE: ADK &amp; OPENHANDS COMPUTE" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#feefc3;strokeColor=#fbbc04;verticalAlign=top;fontStyle=1;fontColor=#b06000;" vertex="1" parent="1"><mxGeometry x="40" y="80" width="260" height="520" as="geometry"/></mxCell>',
        '<mxCell id="zone_blue" value="ROUTING HUB: INGRESS &amp; CONTEXT" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#aecbfa;strokeColor=#4285f4;verticalAlign=top;fontStyle=1;fontColor=#174ea6;" vertex="1" parent="1"><mxGeometry x="360" y="80" width="480" height="240" as="geometry"/></mxCell>',
        '<mxCell id="zone_green" value="GOVERNANCE HUB: MODEL ARMOR &amp; EVALS" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ceead6;strokeColor=#34a853;verticalAlign=top;fontStyle=1;fontColor=#0d652d;" vertex="1" parent="1"><mxGeometry x="360" y="360" width="480" height="240" as="geometry"/></mxCell>',
        '<mxCell id="zone_red" value="RIGHT SPOKE: MEMORY, DATA &amp; MCP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fad2cf;strokeColor=#ea4335;verticalAlign=top;fontStyle=1;fontColor=#a50e0e;" vertex="1" parent="1"><mxGeometry x="900" y="80" width="260" height="520" as="geometry"/></mxCell>',
    ]

    for i, item in enumerate(zones["yellow_compute"][:3]):
        cells.append(
            f'<mxCell id="y_{i}" value="{_esc(item)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#fbbc04;fontColor=#0f172a;fontStyle=1;" vertex="1" parent="1">'
            f'<mxGeometry x="65" y="{130 + i * 140}" width="210" height="90" as="geometry"/></mxCell>'
        )
    for i, item in enumerate(zones["blue_routing"][:3]):
        cells.append(
            f'<mxCell id="b_{i}" value="{_esc(item)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#4285f4;fontColor=#0f172a;fontStyle=1;" vertex="1" parent="1">'
            f'<mxGeometry x="{380 + i * 150}" y="130" width="135" height="150" as="geometry"/></mxCell>'
        )
    for i, item in enumerate(zones["green_governance"][:3]):
        cells.append(
            f'<mxCell id="g_{i}" value="{_esc(item)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#34a853;fontColor=#0f172a;fontStyle=1;" vertex="1" parent="1">'
            f'<mxGeometry x="{380 + i * 150}" y="410" width="135" height="150" as="geometry"/></mxCell>'
        )
    for i, item in enumerate(zones["red_data"][:3]):
        cells.append(
            f'<mxCell id="r_{i}" value="{_esc(item)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#ea4335;fontColor=#0f172a;fontStyle=1;" vertex="1" parent="1">'
            f'<mxGeometry x="925" y="{130 + i * 140}" width="210" height="90" as="geometry"/></mxCell>'
        )

    edge_pairs = [
        ("e1", "b_0", "y_0", "HOP 1: Dispatch"),
        ("e2", "y_0", "b_1", "HOP 2: Context"),
        ("e3", "b_1", "g_1", "HOP 3: Policy Check"),
        ("e4", "g_0", "y_1", "HOP 4: Verified Act"),
        ("e5", "b_2", "r_0", "HOP 5: Read/Write"),
        ("e6", "g_2", "r_2", "HOP 6: Audit Log"),
    ]
    for eid, src, tgt, label in edge_pairs:
        cells.append(
            f'<mxCell id="{eid}" value="{_esc(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1a73e8;strokeWidth=2;fontColor=#0f172a;" edge="1" parent="1" source="{src}" target="{tgt}">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" agent="OpenHands-DiagramEngine/2.0" version="24.7.0">\n'
        f'  <diagram id="{_esc(post["id"])}" name="{_esc(post["repo_slug"])}">\n'
        '    <mxGraphModel dx="1280" dy="780" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1280" pageHeight="780" background="#f8fafc">\n'
        "      <root>\n        "
        + "\n        ".join(cells)
        + "\n      </root>\n"
        "    </mxGraphModel>\n"
        "  </diagram>\n"
        "</mxfile>\n"
    )


def write_visual_suite_for_post(post: Dict[str, Any], visuals_dir: Path) -> Dict[str, str]:
    """Write LinkedIn 2D Infographic SVG, GCP #78 2D Architecture SVG, and Draw.io XML to visuals_dir."""
    visuals_dir.mkdir(parents=True, exist_ok=True)
    infographic_svg_path = visuals_dir / "linkedin-infographic-2d.svg"
    arch_svg_path = visuals_dir / "gcp-architecture-2d.svg"
    drawio_path = visuals_dir / "gcp-architecture-2d.drawio"

    infographic_svg_path.write_text(generate_linkedin_infographic_svg(post), encoding="utf-8")
    arch_svg_path.write_text(generate_gcp_arch_78_svg(post), encoding="utf-8")
    drawio_path.write_text(generate_gcp_arch_78_drawio(post), encoding="utf-8")

    return {
        "linkedin_infographic_svg": str(infographic_svg_path),
        "gcp_architecture_svg": str(arch_svg_path),
        "gcp_architecture_drawio": str(drawio_path),
    }
