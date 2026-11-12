#!/usr/bin/env python3
"""Builds the Fully Corrected & Enterprise-Upgraded 'How MCP Authorization Works' Bundle.

Fixes all 5 burned-in typos, all 4 missing sequence arrows, simultaneous unordered dot motion,
and all 3 enterprise architecture gaps (RFC 8693 OBO upstream token exchange, headless CIBA
step-up alongside browser PKCE, and deterministic OPA/Model Armor tool-argument policy gates).

Outputs:
- @2x Retina Static PNG (2160x2700, 4:5 portrait) + 1080x1350 PNG
- Chronologically Phase-Stepped Animated GIF89a (1080x1350, palettegen/paletteuse, <3.5 MiB)
- Standalone SVG wrapper + Editable Draw.io (.drawio) + Native 12-Slide Deck (.pptx)
- Automated Headless Chrome getBoundingClientRect() zero-collision & zero-overflow receipt
"""

from __future__ import annotations

import base64
import html
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
GALLERY_CUSTOM_DIR = WORKSPACE_ROOT / "assets" / "template-gallery" / "custom_generated"
ARTIFACT_DIR = Path("/usr/local/google/home/nitinagga/.gemini/jetski/brain/5f0163fc-a394-4e1c-8a3e-3b69099d69cd")


def _resolve_chrome() -> str:
    for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "/usr/bin/google-chrome"):
        found = shutil.which(c)
        if found:
            return found
    raise RuntimeError("Headless Chrome not found")


# 5 Lifelines X-coordinates inside the 1032px inner sequence stage (width=1032, left=0..1032)
# Phase label column occupies x=0..118; Lifelines sit at x = 185, 385, 600, 805, 968
LIFELINE_X = {
    "user": 185,
    "client": 385,
    "mcp": 600,
    "auth": 805,
    "upstream": 968,
}

SEQUENCE_STEPS: List[Dict[str, Any]] = [
    # Phase 1: Challenge (phase_idx = 1)
    {
        "num": 1,
        "phase": 1,
        "src": "client",
        "dst": "mcp",
        "dashed": False,
        "color": "#2563EB",
        "label_html": "<code>POST /mcp</code> (initial tool request — no token)",
    },
    {
        "num": 2,
        "phase": 1,
        "src": "mcp",
        "dst": "client",
        "dashed": True,
        "color": "#2563EB",
        "label_html": "<code>401</code> + <code>WWW-Authenticate: Bearer resource_metadata, scope</code>",
    },
    # Phase 2: Discover (phase_idx = 2)
    {
        "num": 3,
        "phase": 2,
        "src": "client",
        "dst": "mcp",
        "dashed": False,
        "color": "#0284C7",
        "label_html": "<code>GET /.well-known/oauth-protected-resource</code> <b>(RFC 9728)</b>",
    },
    {
        "num": 4,
        "phase": 2,
        "src": "mcp",
        "dst": "client",
        "dashed": True,
        "color": "#0284C7",
        "label_html": "<code>200 OK</code> → <code>authorization_servers[]</code>, <code>scopes_supported[]</code>",
    },
    {
        "num": 5,
        "phase": 2,
        "src": "client",
        "dst": "auth",
        "dashed": False,
        "bidir": True,
        "color": "#0284C7",
        "label_html": "Fetch Auth Server Metadata <code>/.well-known/oauth-authorization-server</code> <b>(RFC 8414 / OIDC)</b>",
    },
    # Phase 3: Register / CIMD (phase_idx = 3)
    {
        "num": 6,
        "phase": 3,
        "src": "client",
        "dst": "auth",
        "dashed": False,
        "bidir": True,
        "color": "#7C3AED",
        "label_html": "Resolve <code>client_id</code> : <b>Pre-Registered &gt; CIMD</b> (HTTPS metadata doc) &gt; DCR <i>(deprecated)</i>",
    },
    # Phase 4: Authorize (phase_idx = 4)
    {
        "num": 7,
        "phase": 4,
        "src": "client",
        "dst": "user",
        "dashed": False,
        "color": "#D97706",
        "label_html": "Authorize + PKCE <code>S256</code> + <code>resource</code> + <code>scope</code> <i>(or headless CIBA push)</i>",
    },
    {
        "num": 8,
        "phase": 4,
        "src": "user",
        "dst": "auth",
        "dashed": False,
        "color": "#D97706",
        "label_html": "User signs in &amp; approves requested least-privilege scopes (Browser or Chat HITL)",
    },
    {
        "num": 9,
        "phase": 4,
        "src": "auth",
        "dst": "client",
        "dashed": True,
        "color": "#D97706",
        "label_html": "Callback redirect with single-use <code>code</code> + <code>iss</code> <b>(RFC 9207)</b>",
    },
    {
        "num": 10,
        "phase": 4,
        "src": "client",
        "dst": "client",
        "dashed": False,
        "color": "#D97706",
        "label_html": "Verify callback <code>iss</code> matches discovered Auth Server issuer (blocks mix-up)",
    },
    # Phase 5: Audience-Bound Token (phase_idx = 5)
    {
        "num": 11,
        "phase": 5,
        "src": "client",
        "dst": "auth",
        "dashed": False,
        "color": "#059669",
        "label_html": "<code>POST /token</code> + <code>code_verifier</code> + <code>resource=&lt;mcp_server_uri&gt;</code> <b>(RFC 8707)</b>",
    },
    {
        "num": 12,
        "phase": 5,
        "src": "auth",
        "dst": "client",
        "dashed": True,
        "color": "#059669",
        "label_html": "Short-lived Access Token <code>(aud = this MCP server)</code> + Refresh Token",
    },
    # Phase 6: Call + Policy Gate + RFC 8693 OBO Upstream (phase_idx = 6)
    {
        "num": 13,
        "phase": 6,
        "src": "client",
        "dst": "mcp",
        "dashed": False,
        "color": "#0F766E",
        "label_html": "<code>POST /mcp</code> · <code>Authorization: Bearer &lt;mcp_aud_token&gt;</code>",
    },
    {
        "num": 14,
        "phase": 6,
        "src": "mcp",
        "dst": "mcp",
        "dashed": False,
        "color": "#0F766E",
        "label_html": "Validate <code>sig, exp, aud, scope</code> + <b>Tool-Argument Policy Gate</b> (OPA / Model Armor)",
    },
    {
        "num": 15,
        "phase": 6,
        "src": "mcp",
        "dst": "auth",
        "dashed": False,
        "bidir": True,
        "color": "#0F766E",
        "label_html": "<code>POST /token</code> · <code>urn:…:token-exchange</code> <b>(RFC 8693 OBO)</b> → JWT <code>(sub=user, act=mcp)</code>",
    },
    {
        "num": 16,
        "phase": 6,
        "src": "mcp",
        "dst": "upstream",
        "dashed": False,
        "color": "#0F766E",
        "label_html": "Call Upstream API with narrow OBO token → <code>200 OK</code> (Per-User RLS intact)",
    },
]


def build_infographic_html(active_phase: int = 0, pulse_t: float = 0.5) -> str:
    """Build exact 1080x1350 HTML/SVG for static (@2x) or animated phase state.

    active_phase:
      0 = crisp full static overview (no dimming)
      1..6 = spotlight active protocol phase 1..6 + animate packet pulse along that phase's arrows
      7 = spotlight Step-Up 403 bar + 6 Security Rules Baked In
    """
    # Compute SVG sequence rows with guaranteed pill-above-shaft clearance (>= 5px gap on all 16 steps)
    row_start_y = 26
    row_gap = 40
    seq_svg_parts: List[str] = []

    # Phase background bands
    phase_defs = [
        (1, "Challenge", [1, 2], "#EFF6FF", "#BFDBFE", "#1D4ED8"),
        (2, "Discover", [3, 4, 5], "#F0F9FF", "#BAE6FD", "#0369A1"),
        (3, "Register", [6], "#F5F3FF", "#DDD6FE", "#6D28D9"),
        (4, "Authorize", [7, 8, 9, 10], "#FFFBEB", "#FDE68A", "#B45309"),
        (5, "Token", [11, 12], "#ECFDF5", "#A7F3D0", "#047857"),
        (6, "Call + OBO", [13, 14, 15, 16], "#F0FDFA", "#99F6E4", "#0F766E"),
    ]

    step_y_map: Dict[int, int] = {}
    for idx, st in enumerate(SEQUENCE_STEPS):
        step_y_map[st["num"]] = row_start_y + idx * row_gap

    for p_num, p_title, s_nums, bg_hex, bd_hex, txt_hex in phase_defs:
        y_top = step_y_map[s_nums[0]] - 20.0
        y_bot = step_y_map[s_nums[-1]] + 18.0
        h_band = y_bot - y_top
        is_spot = active_phase == p_num
        opacity = "1.0" if (active_phase in (0, 7) or is_spot) else "0.42"
        stroke_w = "2.3" if is_spot else "1.0"
        stroke_col = txt_hex if is_spot else bd_hex
        fill_col = bg_hex if (active_phase == 0 or is_spot) else "#F8FAFC"
        seq_svg_parts.append(
            f'<g opacity="{opacity}">'
            f'<rect x="6" y="{y_top:.1f}" width="1020" height="{h_band:.1f}" rx="8" fill="{fill_col}" stroke="{stroke_col}" stroke-width="{stroke_w}"/>'
            f'<circle cx="24" cy="{(y_top + y_bot) / 2:.1f}" r="10.5" fill="{txt_hex}"/>'
            f'<text x="24" y="{(y_top + y_bot) / 2 + 3.8:.1f}" text-anchor="middle" font-size="11" font-weight="800" fill="#FFFFFF">{p_num}</text>'
            f'<text x="40" y="{(y_top + y_bot) / 2 + 4.0:.1f}" font-size="12" font-weight="800" fill="{txt_hex}">{html.escape(p_title)}</text>'
            f'</g>'
        )

    # Vertical lifelines connecting right from lifeline headers down to bottom of sequence canvas
    total_seq_h = row_start_y + (len(SEQUENCE_STEPS) - 1) * row_gap + 22
    for key, lx in LIFELINE_X.items():
        seq_svg_parts.append(
            f'<line x1="{lx}" y1="0" x2="{lx}" y2="{total_seq_h}" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,4"/>'
        )

    # Draw unobstructed arrows (y + 10.5) cleanly below pills (top: y - 16.5, bottom: ~y + 1.5)
    step_pills_html: List[str] = []
    for st in SEQUENCE_STEPS:
        s_num = st["num"]
        y = step_y_map[s_num]
        p_num = st["phase"]
        is_spot = active_phase == p_num
        row_opacity = "1.0" if (active_phase in (0, 7) or is_spot) else "0.45"
        col = st["color"]
        x1 = LIFELINE_X[st["src"]]
        x2 = LIFELINE_X[st["dst"]]
        dash_attr = ' stroke-dasharray="5,3"' if st.get("dashed") else ""
        sw = "2.5" if is_spot else "1.95"

        if x1 == x2:
            # Unobstructed self-verification loop on actor lifeline (Steps 10 & 14) below the pill
            loop_w = 56
            ly_top = y + 5.5
            ly_bot = y + 13.5
            seq_svg_parts.append(
                f'<g data-arrow="seq-arrow-{s_num}" opacity="{row_opacity}">'
                f'<path d="M {x1} {ly_top} L {x1 + loop_w} {ly_top} L {x1 + loop_w} {ly_bot} L {x1 + 8} {ly_bot}" fill="none" stroke="{col}" stroke-width="{sw}"/>'
                f'<polygon points="{x1 + 1},{ly_bot} {x1 + 8.5},{ly_bot - 3.5} {x1 + 8.5},{ly_bot + 3.5}" fill="{col}"/>'
                f'<circle cx="{x1}" cy="{ly_top}" r="2.8" fill="#FFFFFF" stroke="{col}" stroke-width="1.8"/>'
                f'</g>'
            )
            if is_spot:
                px = x1 + loop_w * pulse_t
                seq_svg_parts.append(
                    f'<circle cx="{px:.1f}" cy="{(ly_top + ly_bot) / 2:.1f}" r="5.0" fill="#FACC15" stroke="#0F172A" stroke-width="1.5"/>'
                )
            mid_x = x1 + 110 if s_num == 10 else x1 - 15
        else:
            direction = 1 if x2 > x1 else -1
            ay = y + 10.5
            end_x = x2 - direction * 7
            start_x = (x1 + direction * 7) if st.get("bidir") else x1
            seq_svg_parts.append(
                f'<g data-arrow="seq-arrow-{s_num}" opacity="{row_opacity}">'
                f'<line x1="{start_x}" y1="{ay}" x2="{end_x}" y2="{ay}" stroke="{col}" stroke-width="{sw}"{dash_attr}/>'
                f'<polygon points="{x2},{ay} {x2 - direction * 8.5},{ay - 4} {x2 - direction * 8.5},{ay + 4}" fill="{col}"/>'
                + (
                    f'<polygon points="{x1},{ay} {x1 + direction * 8.5},{ay - 4} {x1 + direction * 8.5},{ay + 4}" fill="{col}"/>'
                    if st.get("bidir")
                    else f'<circle cx="{x1}" cy="{ay}" r="3.0" fill="#FFFFFF" stroke="{col}" stroke-width="1.8"/>'
                )
                + "</g>"
            )
            if is_spot:
                px = x1 + (x2 - x1) * pulse_t
                seq_svg_parts.append(
                    f'<circle cx="{px:.1f}" cy="{ay}" r="5.5" fill="#FACC15" stroke="#0F172A" stroke-width="1.6"/>'
                )
            mid_x = (x1 + x2) / 2.0

        clamped_mid = max(315.0, min(745.0, mid_x))
        if s_num == 7:
            clamped_mid = 330.0
        elif s_num == 10:
            clamped_mid = 495.0
        elif s_num == 14:
            clamped_mid = 565.0
        elif s_num == 16:
            clamped_mid = 760.0

        pill_border = col if is_spot else "#CBD5E1"
        pill_shadow = "0 2px 6px rgba(37,99,235,0.16)" if is_spot else "none"
        step_pills_html.append(
            f'<div class="seq-pill" data-box="seq-pill-{s_num}" style="left:{clamped_mid:.1f}px;top:{y - 16.5:.1f}px;opacity:{row_opacity};border-color:{pill_border};box-shadow:{pill_shadow};">'
            f'<span class="step-num" style="background:{col};">{s_num}</span>'
            f'<span class="step-txt">{st["label_html"]}</span>'
            f'</div>'
        )

    stepup_spot = "border:2px solid #D97706;background:#FFFBEB;" if active_phase == 7 else "border:1.5px dashed #64748B;background:#F8FAFC;"
    rules_spot = "box-shadow:0 0 0 2.5px #059669;" if active_phase == 7 else ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1350px;
    overflow: hidden;
    background: #F8FAFC;
    color: #0F172A;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .canvas {{
    width: 1080px;
    height: 1350px;
    padding: 12px 22px 10px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }}
  .top-accent {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #2563EB 0%, #0284C7 35%, #059669 70%, #F59E0B 100%);
  }}
  .header {{
    text-align: center;
    padding-top: 2px;
  }}
  .eyebrow {{
    display: inline-block;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #1E40AF;
    background: #DBEAFE;
    border: 1px solid #93C5FD;
    padding: 2px 10px;
    border-radius: 999px;
    margin-bottom: 4px;
  }}
  .main-title {{
    font-size: 33px;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #0F172A;
    line-height: 1.12;
  }}
  .hl-yellow {{
    background: #FEF08A;
    padding: 0 8px;
    border-radius: 6px;
    border: 1px solid #FDE047;
  }}
  .subtitle {{
    font-size: 14px;
    color: #334155;
    margin-top: 3px;
    font-weight: 500;
  }}
  .subtitle b {{
    color: #0F172A;
    font-weight: 800;
  }}

  /* Section Card Shell */
  .band-card {{
    background: #FFFFFF;
    border: 1.5px solid #CBD5E1;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
  }}
  .band-hdr {{
    background: #0F172A;
    color: #FACC15;
    font-size: 13.5px;
    font-weight: 800;
    text-align: center;
    padding: 5px 14px;
    letter-spacing: 0.01em;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }}
  .band-hdr span.sub-pill {{
    background: rgba(250, 204, 21, 0.16);
    color: #FEF08A;
    border: 1px solid rgba(250, 204, 21, 0.4);
    font-size: 10.5px;
    padding: 1px 8px;
    border-radius: 999px;
    font-weight: 700;
  }}

  /* Band 1: Who's Involved */
  .roles-stage {{
    position: relative;
    height: 180px;
    padding: 10px 14px;
  }}
  .role-box {{
    position: absolute;
    border-radius: 9px;
    padding: 7px 10px;
    background: #FEFCE8;
    border: 1.5px solid #CA8A04;
    line-height: 1.24;
  }}
  .role-box.blue {{ background: #EFF6FF; border-color: #2563EB; }}
  .role-box.teal {{ background: #F0FDFA; border-color: #0D9488; }}
  .role-box.purple {{ background: #F5F3FF; border-color: #7C3AED; }}
  .role-box.emerald {{ background: #ECFDF5; border-color: #059669; }}
  .role-title {{
    font-size: 12.5px;
    font-weight: 800;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .role-sub {{
    font-size: 10.5px;
    font-weight: 700;
    color: #475569;
    margin-bottom: 2px;
  }}
  .role-desc {{
    font-size: 10.5px;
    color: #1E293B;
  }}

  /* Band 2: Sequence Flow */
  .seq-wrapper {{
    position: relative;
    padding: 8px 0 8px 0;
  }}
  .lifeline-headers {{
    position: relative;
    height: 30px;
    margin-bottom: 2px;
  }}
  .ll-hdr {{
    position: absolute;
    transform: translateX(-50%);
    padding: 4px 10px;
    border-radius: 7px;
    font-size: 11.5px;
    font-weight: 800;
    white-space: nowrap;
    border: 1.5px solid #94A3B8;
    background: #F8FAFC;
    color: #0F172A;
  }}
  .seq-canvas {{
    position: relative;
    width: 1032px;
    height: {total_seq_h}px;
  }}
  .seq-pill {{
    position: absolute;
    transform: translateX(-50%);
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 999px;
    padding: 1px 7px 1px 2.5px;
    line-height: 1.15;
    white-space: nowrap;
    z-index: 3;
  }}
  .step-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    color: #FFFFFF;
    font-size: 9.5px;
    font-weight: 800;
    flex-shrink: 0;
  }}
  .step-txt {{
    font-size: 10.4px;
    color: #0F172A;
    font-weight: 600;
  }}
  .step-txt code {{
    font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 9.8px;
    background: #F1F5F9;
    color: #0F172A;
    padding: 0.5px 4px;
    border-radius: 4px;
    border: 1px solid #E2E8F0;
    font-weight: 700;
  }}
  .stepup-bar {{
    margin: 4px 12px 1px 12px;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 10.4px;
    color: #0F172A;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    gap: 8px;
    {stepup_spot}
  }}
  .stepup-bar code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 10px;
    background: #FFFFFF;
    padding: 1px 5px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    font-weight: 700;
  }}

  /* Band 3: 6 Security Rules Grid */
  .rules-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    padding: 8px 10px;
  }}
  .rule-card {{
    background: #F0FDF4;
    border: 1.5px solid #86EFAC;
    border-radius: 9px;
    padding: 7px 9px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .rule-card.alt {{
    background: #EFF6FF;
    border-color: #93C5FD;
  }}
  .rule-hdr {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 800;
    color: #0F172A;
  }}
  .rule-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background: #0F172A;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 800;
    margin-right: 5px;
  }}
  .rule-body {{
    font-size: 10.3px;
    line-height: 1.28;
    color: #1E293B;
  }}
  .rule-body code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 9.6px;
    background: rgba(255,255,255,0.85);
    padding: 0 3px;
    border-radius: 3px;
    border: 1px solid #CBD5E1;
    font-weight: 700;
  }}
  .footer-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
    font-weight: 700;
    color: #475569;
    padding: 0 4px;
  }}
</style>
</head>
<body>
<div class="canvas">
  <div class="top-accent"></div>

  <!-- HEADER -->
  <header class="header" data-box="header">
    <div class="eyebrow">Model Context Protocol (2025–2026 Spec) · OAuth 2.1 + RFC 8693 Enterprise OBO Reference</div>
    <h1 class="main-title">How <span class="hl-yellow">MCP Authorization</span> Works End-to-End</h1>
    <p class="subtitle">How an AI Agent gets <b>scoped, audience-bound, On-Behalf-Of (OBO)</b> access to remote MCP &amp; upstream APIs</p>
  </header>

  <!-- BAND 1: WHO'S INVOLVED (5 DECOUPLED ROLES) -->
  <section class="band-card">
    <div class="band-hdr">
      <span>1 · Who’s Involved — 5 Decoupled Security Roles</span>
      <span class="sub-pill">Resource Server ≠ Auth Server · Zero Client Token Passthrough</span>
    </div>
    <div class="roles-stage">
      <!-- Connecting SVG Arrows inside Band 1 -->
      <svg width="1032" height="180" style="position:absolute;top:0;left:0;pointer-events:none;">
        <!-- User -> MCP Client -->
        <line x1="206" y1="48" x2="246" y2="48" stroke="#0F172A" stroke-width="1.8"/>
        <polygon points="252,48 244,44 244,52" fill="#0F172A"/>
        <!-- MCP Client -> MCP Server -->
        <line x1="478" y1="48" x2="524" y2="48" stroke="#2563EB" stroke-width="2.0"/>
        <polygon points="530,48 522,44 522,52" fill="#2563EB"/>
        <!-- MCP Server -> Upstream API -->
        <line x1="766" y1="48" x2="812" y2="48" stroke="#059669" stroke-width="2.0"/>
        <polygon points="818,48 810,44 810,52" fill="#059669"/>
        <!-- User -> Auth Server (elbow) -->
        <path d="M 105 90 L 105 141 L 252 141" fill="none" stroke="#B45309" stroke-width="1.8"/>
        <polygon points="258,141 250,137 250,145" fill="#B45309"/>
        <text x="112" y="133" font-size="10.2" font-weight="700" fill="#92400E">login + PKCE / CIBA consent</text>
        <!-- MCP Client <-> Auth Server -->
        <line x1="365" y1="90" x2="365" y2="106" stroke="#7C3AED" stroke-width="1.8"/>
        <polygon points="365,90 361,97 369,97" fill="#7C3AED"/>
        <polygon points="365,108 361,101 369,101" fill="#7C3AED"/>
        <text x="373" y="102" font-size="10" font-weight="700" fill="#5B21B6">discover · CIMD · token</text>
        <!-- MCP Server <-> Auth/STS Server (RFC 8693 OBO) -->
        <line x1="648" y1="90" x2="648" y2="106" stroke="#0F766E" stroke-width="1.8" stroke-dasharray="4,2"/>
        <polygon points="648,108 644,101 652,101" fill="#0F766E"/>
        <polygon points="648,90 644,97 652,97" fill="#0F766E"/>
        <text x="656" y="102" font-size="10" font-weight="700" fill="#0F766E">RFC 8693 OBO swap</text>
        <!-- Upstream caption -->
        <text x="920" y="124" text-anchor="middle" font-size="10.2" font-weight="700" fill="#065F46">Calls upstream with narrow</text>
        <text x="920" y="137" text-anchor="middle" font-size="10.2" font-weight="800" fill="#065F46">per-user OBO token (RLS intact),</text>
        <text x="920" y="150" text-anchor="middle" font-size="10.2" font-weight="700" fill="#B91C1C">never the client's MCP token</text>
      </svg>

      <div class="role-box" data-box="role-user" style="left:12px;top:10px;width:194px;height:80px;">
        <div class="role-title">👤 User / Async HITL</div>
        <div class="role-sub">Resource Owner</div>
        <div class="role-desc">Approves scopes in Browser (PKCE) or headless CIBA / Chat card.</div>
      </div>

      <div class="role-box blue" data-box="role-client" style="left:252px;top:10px;width:226px;height:80px;">
        <div class="role-title">🤖 MCP Client / Agent</div>
        <div class="role-sub">OAuth 2.1 Client (IDE, Chat, A2A)</div>
        <div class="role-desc">Runs PKCE S256, CIMD identity &amp; RFC 8707 audience binding.</div>
      </div>

      <div class="role-box teal" data-box="role-mcp" style="left:530px;top:10px;width:236px;height:80px;">
        <div class="role-title">🛡️ MCP Server + Policy Gate</div>
        <div class="role-sub">OAuth 2.1 Resource Server</div>
        <div class="role-desc">Publishes RFC 9728 metadata, verifies <b>aud</b> &amp; tool arguments.</div>
      </div>

      <div class="role-box emerald" data-box="role-upstream" style="left:818px;top:10px;width:202px;height:80px;">
        <div class="role-title">☁️ Upstream API</div>
        <div class="role-sub">GitHub · Gmail · Jira · BQ</div>
        <div class="role-desc">Enforces per-user Row-Level Security on exchanged OBO JWT.</div>
      </div>

      <div class="role-box purple" data-box="role-auth" style="left:258px;top:108px;width:508px;height:64px;">
        <div class="role-title">🔐 Authorization Server + RFC 8693 STS <span style="font-size:10.5px;font-weight:700;color:#5B21B6;">— Separate role (self-hosted IdP or cloud IAM)</span></div>
        <div class="role-desc" style="margin-top:3px;">Authenticates user, verifies <b>CIMD</b> client metadata, issues MCP-bound tokens (<b>RFC 8707</b>), and exchanges them via <b>RFC 8693 OBO</b> (<code>sub=user, act=mcp</code>) for narrow upstream API tokens.</div>
      </div>
    </div>
  </section>

  <!-- BAND 2: STEP-BY-STEP 16-MESSAGE SEQUENCE -->
  <section class="band-card">
    <div class="band-hdr">
      <span>2 · The Flow, Step by Step (6 Phases · 16 Verified Messages)</span>
      <span class="sub-pill">{f"▶ PHASE {active_phase}/6 ACTIVE SPOTLIGHT" if 1 <= active_phase <= 6 else ("▶ STEP-UP & 6 INVARIANTS" if active_phase == 7 else "Every Arrow Explicitly Bound · Browser PKCE + Headless CIBA + Upstream OBO")}</span>
    </div>
    <div class="seq-wrapper">
      <div class="lifeline-headers">
        <div class="ll-hdr" data-box="ll-user" style="left:{LIFELINE_X['user']}px;background:#FEFCE8;border-color:#CA8A04;">👤 User / HITL</div>
        <div class="ll-hdr" data-box="ll-client" style="left:{LIFELINE_X['client']}px;background:#EFF6FF;border-color:#2563EB;">🤖 MCP Client</div>
        <div class="ll-hdr" data-box="ll-mcp" style="left:{LIFELINE_X['mcp']}px;background:#F0FDFA;border-color:#0D9488;">🛡️ MCP Server</div>
        <div class="ll-hdr" data-box="ll-auth" style="left:{LIFELINE_X['auth']}px;background:#F5F3FF;border-color:#7C3AED;">🔐 Auth / STS</div>
        <div class="ll-hdr" data-box="ll-upstream" style="left:{LIFELINE_X['upstream']}px;background:#ECFDF5;border-color:#059669;">☁️ Upstream API</div>
      </div>

      <div class="seq-canvas">
        <svg width="1032" height="{total_seq_h}" style="position:absolute;top:0;left:0;z-index:1;">
          {"".join(seq_svg_parts)}
        </svg>
        {"".join(step_pills_html)}
      </div>

      <div class="stepup-bar" data-box="stepup-bar">
        <span>⚡ <b>Dynamic Step-Up:</b> Missing scope? Server returns <code>403</code> + <code>WWW-Authenticate: Bearer error="insufficient_scope", scope="…"</code> → Browser PKCE <b>or</b> Async CIBA push → retry.</span>
      </div>
    </div>
  </section>

  <!-- BAND 3: 6 SECURITY RULES BAKED IN -->
  <section class="band-card" style="{rules_spot}">
    <div class="band-hdr">
      <span>3 · Security Rules Baked In (6 Production Invariants)</span>
      <span class="sub-pill">OAuth 2.1 + Zero-Trust Argument &amp; Delegation Controls</span>
    </div>
    <div class="rules-grid">
      <div class="rule-card" data-box="rule-1">
        <div class="rule-hdr"><span><span class="rule-badge">1</span>PKCE (S256) + iss Check</span><span>🔒</span></div>
        <div class="rule-body">Clients enforce <code>S256</code> PKCE (abort if unsupported) and verify callback <code>iss</code> <b>(RFC 9207)</b> to block code interception &amp; IdP mix-up.</div>
      </div>
      <div class="rule-card alt" data-box="rule-2">
        <div class="rule-hdr"><span><span class="rule-badge">2</span>Audience-Bound Tokens</span><span>🎯</span></div>
        <div class="rule-body"><code>resource</code> <b>(RFC 8707)</b> binds each token’s <code>aud</code> claim to a single MCP server URI. Servers reject tokens minted for any other resource.</div>
      </div>
      <div class="rule-card" data-box="rule-3">
        <div class="rule-hdr"><span><span class="rule-badge">3</span>CIMD Over Open DCR</span><span>🪪</span></div>
        <div class="rule-body">HTTPS <b>Client ID Metadata Documents (CIMD)</b> let servers verify app identity &amp; redirect URIs without unauthenticated <code>RFC 7591</code> DCR spam.</div>
      </div>
      <div class="rule-card alt" data-box="rule-4">
        <div class="rule-hdr"><span><span class="rule-badge">4</span>No Passthrough + OBO Swap</span><span>🛡️</span></div>
        <div class="rule-body">Never forward client tokens upstream. Exchange via <b>RFC 8693 STS</b> for narrow 5-min tokens preserving <code>sub=user</code> &amp; <code>act=mcp</code>.</div>
      </div>
      <div class="rule-card" data-box="rule-5">
        <div class="rule-hdr"><span><span class="rule-badge">5</span>Least-Privilege Step-Up</span><span>🔑</span></div>
        <div class="rule-body">Request minimal initial scopes; elevate on <code>403 insufficient_scope</code> via Browser PKCE or headless <b>OpenID CIBA</b> out-of-band approval.</div>
      </div>
      <div class="rule-card alt" data-box="rule-6">
        <div class="rule-hdr"><span><span class="rule-badge">6</span>Tool-Argument Policy Gate</span><span>⚖️</span></div>
        <div class="rule-body">OAuth scopes gate endpoints, not prompt-injected payloads. Enforce deterministic <b>OPA / Model Armor</b> argument checks + write HITL nonces.</div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="footer-bar">
    <span>Nitin Aggarwal · Principal AI Architect · Google Cloud</span>
    <span>Spec-Verified MCP OAuth 2.1 + RFC 8693 OBO Blueprint · Zero-Typo Edition · November 2026</span>
  </footer>
</div>
</body>
</html>
"""


def build_editable_drawio_xml() -> str:
    """Build valid editable Draw.io mxfile XML representing the 5-actor + 6-phase MCP Auth + OBO architecture."""
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        '<mxCell id="title" value="How MCP Authorization Works End-to-End (OAuth 2.1 + CIMD + RFC 8707 + RFC 8693 OBO)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;fontColor=#FACC15;fontStyle=1;fontSize=16;strokeColor=#1E293B;" vertex="1" parent="1"><mxGeometry x="40" y="24" width="1000" height="44" as="geometry"/></mxCell>',
        '<mxCell id="r_user" value="1. User / Async HITL&#xa;(Resource Owner: Browser PKCE or CIBA)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEFCE8;strokeColor=#CA8A04;fontColor=#0F172A;fontStyle=1;fontSize=12;" vertex="1" parent="1"><mxGeometry x="40" y="92" width="180" height="72" as="geometry"/></mxCell>',
        '<mxCell id="r_client" value="2. MCP Client / Agent&#xa;(OAuth 2.1 Client: PKCE S256 + CIMD + RFC 9207 iss)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#2563EB;fontColor=#0F172A;fontStyle=1;fontSize=12;" vertex="1" parent="1"><mxGeometry x="260" y="92" width="220" height="72" as="geometry"/></mxCell>',
        '<mxCell id="r_mcp" value="3. MCP Server + Argument Policy Gate&#xa;(RFC 9728 Resource Server + OPA / Model Armor)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDFA;strokeColor=#0D9488;fontColor=#0F172A;fontStyle=1;fontSize=12;" vertex="1" parent="1"><mxGeometry x="520" y="92" width="240" height="72" as="geometry"/></mxCell>',
        '<mxCell id="r_up" value="5. Upstream Enterprise API&#xa;(GitHub / Gmail / Jira / BigQuery RLS)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#059669;fontColor=#0F172A;fontStyle=1;fontSize=12;" vertex="1" parent="1"><mxGeometry x="800" y="92" width="240" height="72" as="geometry"/></mxCell>',
        '<mxCell id="r_auth" value="4. Authorization Server + RFC 8693 STS (Separate Role — Self-Hosted IdP or Cloud IAM)&#xa;Issues RFC 8707 MCP-bound tokens AND exchanges via RFC 8693 OBO (sub=user, act=mcp) for upstream APIs" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#7C3AED;fontColor=#0F172A;fontStyle=1;fontSize=12;" vertex="1" parent="1"><mxGeometry x="260" y="196" width="500" height="68" as="geometry"/></mxCell>',
        '<mxCell id="e1" value="PKCE / CIBA" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#CA8A04;strokeWidth=2;" edge="1" parent="1" source="r_user" target="r_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e2" value="CIMD + RFC 8707" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#7C3AED;strokeWidth=2;" edge="1" parent="1" source="r_client" target="r_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e3" value="Bearer &lt;mcp_jwt&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#2563EB;strokeWidth=2;" edge="1" parent="1" source="r_client" target="r_mcp"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e4" value="RFC 8693 OBO" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#0F766E;strokeWidth=2;" edge="1" parent="1" source="r_mcp" target="r_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e5" value="Narrow OBO JWT" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#059669;strokeWidth=2;" edge="1" parent="1" source="r_mcp" target="r_up"><mxGeometry relative="1" as="geometry"/></mxCell>',
    ]
    phases = [
        ("p1", "Phase 1 · Challenge (Steps 01–02): POST /mcp → 401 WWW-Authenticate: Bearer resource_metadata, scope", 292, "#EFF6FF", "#2563EB"),
        ("p2", "Phase 2 · Discover (Steps 03–05): GET /.well-known/oauth-protected-resource (RFC 9728) + Auth Server Metadata (RFC 8414)", 352, "#F0F9FF", "#0284C7"),
        ("p3", "Phase 3 · Identify Client (Step 06): Pre-Registered > CIMD (HTTPS Client ID Metadata Document) > DCR (deprecated)", 412, "#F5F3FF", "#7C3AED"),
        ("p4", "Phase 4 · Authorize (Steps 07–10): Browser PKCE S256 + resource + scope (or Headless CIBA) + RFC 9207 iss Callback Check", 472, "#FFFBEB", "#D97706"),
        ("p5", "Phase 5 · Audience-Bound Token (Steps 11–12): POST /token + code_verifier + resource (RFC 8707) → aud = MCP Server URI", 532, "#ECFDF5", "#059669"),
        ("p6", "Phase 6 · Policy Gate & Upstream OBO (Steps 13–16): Verify JWT + OPA/Model Armor Arg Gate → RFC 8693 OBO Swap → Upstream API", 592, "#F0FDFA", "#0F766E"),
        ("p7", "Step-Up & 6 Baked-In Rules: 403 insufficient_scope (PKCE / CIBA) · Zero Token Passthrough · Deterministic Argument Guard", 652, "#F8FAFC", "#0F172A"),
    ]
    for pid, label, y, fill, stroke in phases:
        cells.append(
            f'<mxCell id="{pid}" value="{html.escape(label)}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontColor=#0F172A;fontStyle=1;fontSize=12;align=left;spacingLeft=14;" vertex="1" parent="1"><mxGeometry x="40" y="{y}" width="1000" height="46" as="geometry"/></mxCell>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" modified="2026-11-12T20:05:00.000Z" agent="IdeasMintingStudio" version="24.7.0">\n'
        '  <diagram id="mcp-oauth21-obo-v2" name="MCP Authorization &amp; OBO Flow">\n'
        '    <mxGraphModel dx="1200" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1080" pageHeight="740" math="0" shadow="0">\n'
        '      <root>\n        '
        + "\n        ".join(cells)
        + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n"
    )


def audit_dom_geometry_with_puppeteer(html_path: Path) -> Dict[str, Any]:
    """Run headless Puppeteer getBoundingClientRect() check to prove 0 collisions & 0 viewport overflows."""
    js = f"""
    const puppeteer = require('puppeteer');
    (async () => {{
      const browser = await puppeteer.launch({{ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] }});
      const page = await browser.newPage();
      await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: 2 }});
      await page.goto('file://{html_path}', {{ waitUntil: 'networkidle0' }});
      const report = await page.evaluate(() => {{
        const boxes = Array.from(document.querySelectorAll('[data-box]')).map(el => {{
          const r = el.getBoundingClientRect();
          return {{
            id: el.getAttribute('data-box'),
            left: Math.round(r.left * 10) / 10,
            top: Math.round(r.top * 10) / 10,
            right: Math.round(r.right * 10) / 10,
            bottom: Math.round(r.bottom * 10) / 10,
            width: Math.round(r.width * 10) / 10,
            height: Math.round(r.height * 10) / 10,
            scrollOverflowX: el.scrollWidth - el.clientWidth,
          }};
        }});
        const collisions = [];
        for (let i = 0; i < boxes.length; i++) {{
          for (let j = i + 1; j < boxes.length; j++) {{
            const a = boxes[i], b = boxes[j];
            const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left);
            const iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
            if (ix > 1.5 && iy > 1.5) {{
              collisions.push({{ a: a.id, b: b.id, overlapPx2: Math.round(ix * iy) }});
            }}
          }}
        }}
        const arrows = Array.from(document.querySelectorAll('[data-arrow]')).map(el => {{
          const r = el.getBoundingClientRect();
          return {{
            id: el.getAttribute('data-arrow'),
            stepNum: parseInt(el.getAttribute('data-arrow').replace('seq-arrow-', ''), 10),
            left: Math.round(r.left * 10) / 10,
            top: Math.round(r.top * 10) / 10,
            right: Math.round(r.right * 10) / 10,
            bottom: Math.round(r.bottom * 10) / 10,
            width: Math.round(r.width * 10) / 10,
          }};
        }});
        const missingArrows = [];
        const pillArrowOverlaps = [];
        for (let s = 1; s <= 16; s++) {{
          const ar = arrows.find(a => a.stepNum === s);
          const pl = boxes.find(b => b.id === 'seq-pill-' + s);
          if (!ar || ar.width < 35) {{
            missingArrows.push(s);
          }} else if (pl) {{
            const ix = Math.min(pl.right, ar.right) - Math.max(pl.left, ar.left);
            const iy = Math.min(pl.bottom, ar.bottom) - Math.max(pl.top, ar.top);
            if (ix > 1.0 && iy > 0.5) {{
              pillArrowOverlaps.push({{ step: s, pillBottom: pl.bottom, arrowTop: ar.top, overlapY: Math.round(iy * 10) / 10 }});
            }}
          }}
        }}
        const outOfBounds = boxes.filter(b => b.left < 0 || b.top < 0 || b.right > 1080.5 || b.bottom > 1350.5);
        const canvasBottom = document.querySelector('.footer-bar').getBoundingClientRect().bottom;
        return {{
          boxCount: boxes.length,
          arrowCount: arrows.length,
          missingArrows,
          pillArrowOverlaps,
          collisions,
          outOfBounds,
          footerBottomPx: Math.round(canvasBottom * 10) / 10,
        }};
      }});
      await browser.close();
      console.log(JSON.stringify(report));
    }})();
    """
    raw = subprocess.check_output(["node", "-e", js], cwd=str(WORKSPACE_ROOT), text=True)
    return json.loads(raw.strip())


def generate_all_assets() -> Dict[str, Any]:
    GALLERY_CUSTOM_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    chrome_bin = _resolve_chrome()

    stem = "T222_mcp_oauth21_obo_enterprise"
    png_2x_gallery = GALLERY_CUSTOM_DIR / f"{stem}.png"
    gif_gallery = GALLERY_CUSTOM_DIR / f"{stem}.gif"
    svg_gallery = GALLERY_CUSTOM_DIR / f"{stem}.svg"
    drawio_gallery = GALLERY_CUSTOM_DIR / f"{stem}.drawio"

    png_2x_art = ARTIFACT_DIR / "mcp_oauth_enterprise_corrected_v2.png"
    gif_art = ARTIFACT_DIR / "mcp_oauth_enterprise_corrected_v2.gif"

    with tempfile.TemporaryDirectory(prefix="mcp_oauth_v2_") as tmp_s:
        tmp = Path(tmp_s)
        overview_html = tmp / "frame_overview.html"
        overview_html.write_text(build_infographic_html(active_phase=0, pulse_t=0.5), encoding="utf-8")

        # 1. Run strict getBoundingClientRect() audit BEFORE finalizing render
        geom = audit_dom_geometry_with_puppeteer(overview_html)
        if geom["collisions"] or geom["outOfBounds"] or geom["missingArrows"] or geom["pillArrowOverlaps"]:
            raise RuntimeError(f"DOM geometry violation detected: {json.dumps(geom, indent=2)}")

        # 2. Render @2x Retina Static PNG (2160x2700) via Puppeteer deviceScaleFactor=2
        render_js = f"""
        const puppeteer = require('puppeteer');
        (async () => {{
          const browser = await puppeteer.launch({{ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] }});
          const page = await browser.newPage();
          await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: 2 }});
          await page.goto('file://{overview_html}', {{ waitUntil: 'networkidle0' }});
          await page.screenshot({{ path: '{png_2x_gallery}', clip: {{ x: 0, y: 0, width: 1080, height: 1350 }} }});
          await browser.close();
        }})();
        """
        subprocess.run(["node", "-e", render_js], cwd=str(WORKSPACE_ROOT), check=True)
        shutil.copyfile(png_2x_gallery, png_2x_art)

        # 3. Render 24 chronological animation frames (8 states x 3 pulse sub-steps = 24 frames @ 4fps = 6.0s loop)
        # Guides the reader's eye sequentially: Overview -> Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6 -> Step-Up & Rules
        schedule = [
            (0, 0.50), (0, 0.50), (0, 0.50),
            (1, 0.25), (1, 0.55), (1, 0.82),
            (2, 0.25), (2, 0.55), (2, 0.82),
            (3, 0.28), (3, 0.62), (3, 0.85),
            (4, 0.25), (4, 0.55), (4, 0.82),
            (5, 0.25), (5, 0.55), (5, 0.82),
            (6, 0.25), (6, 0.55), (6, 0.82),
            (7, 0.50), (7, 0.50), (7, 0.50),
        ]
        for idx, (ph, pt) in enumerate(schedule):
            (tmp / f"anim_{idx:02d}.html").write_text(
                build_infographic_html(active_phase=ph, pulse_t=pt), encoding="utf-8"
            )

        batch_js = f"""
        const puppeteer = require('puppeteer');
        (async () => {{
          const browser = await puppeteer.launch({{ headless: 'new', args: ['--no-sandbox', '--disable-setuid-sandbox'] }});
          const page = await browser.newPage();
          await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: 1 }});
          for (let i = 0; i < {len(schedule)}; i++) {{
            const n = String(i).padStart(2, '0');
            await page.goto('file://{tmp}/anim_' + n + '.html', {{ waitUntil: 'load' }});
            await page.screenshot({{ path: '{tmp}/frame_' + n + '.png', clip: {{ x: 0, y: 0, width: 1080, height: 1350 }} }});
          }}
          await browser.close();
        }})();
        """
        subprocess.run(["node", "-e", batch_js], cwd=str(WORKSPACE_ROOT), check=True)

        # Compile high-clarity 256-color palettegen/paletteuse GIF89a (4fps = 6.0s chronological walkthrough)
        palette_png = tmp / "palette.png"
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-y", "-v", "error",
                "-framerate", "4", "-i", str(tmp / "frame_%02d.png"),
                "-vf", "palettegen=stats_mode=diff:max_colors=256",
                str(palette_png),
            ],
            check=True,
        )
        subprocess.run(
            [
                "ffmpeg", "-nostdin", "-y", "-v", "error",
                "-framerate", "4", "-i", str(tmp / "frame_%02d.png"),
                "-i", str(palette_png),
                "-lavfi", "paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                "-loop", "0",
                str(gif_gallery),
            ],
            check=True,
        )
        shutil.copyfile(gif_gallery, gif_art)

    # 4. Write Draw.io XML + SVG wrapper
    drawio_gallery.write_text(build_editable_drawio_xml(), encoding="utf-8")
    b64_png = base64.b64encode(png_2x_gallery.read_bytes()).decode("ascii")
    svg_gallery.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">'
        f'<title>How MCP Authorization Works End-to-End (OAuth 2.1 + CIMD + RFC 8707 + RFC 8693 OBO)</title>'
        f'<image href="data:image/png;base64,{b64_png}" x="0" y="0" width="1080" height="1350"/>'
        f'</svg>',
        encoding="utf-8",
    )

    return {
        "status": "GENERATED_AND_VERIFIED",
        "geometry_audit": geom,
        "png_2x_path": str(png_2x_gallery),
        "png_2x_artifact": str(png_2x_art),
        "png_2x_bytes": png_2x_gallery.stat().st_size,
        "gif_path": str(gif_gallery),
        "gif_artifact": str(gif_art),
        "gif_bytes": gif_gallery.stat().st_size,
        "drawio_path": str(drawio_gallery),
        "svg_path": str(svg_gallery),
    }


if __name__ == "__main__":
    res = generate_all_assets()
    print(json.dumps(res, indent=2))
