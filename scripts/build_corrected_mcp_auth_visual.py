"""Build the Fully Corrected & Upgraded Enterprise MCP Authorization Visual Bundle.

Generates:
  1. Static @2x Retina PNG (2160x2700, 4:5 portrait)
  2. Sequential-Pulse Animated GIF89a (1080x1350, 4:5 portrait, Phases 1->7 / Steps 1->16)
  3. Clean Vector SVG (1080x1350)
  4. Native Editable Draw.io XML (.drawio)
  5. LinkedIn Post Markdown with RFC citations & runnable MINT-01 repository link

Fixes all 6 pixel-level typos and all 4 enterprise protocol/visual gaps identified in
the review of https://lnkd.in/p/euYbsfaf (Jean Lee's MCP Authorization infographic).
"""

from __future__ import annotations

import html
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.visuals.canonical_flow_svg import resolve_chrome_bin

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = WORKSPACE_ROOT / "assets" / "remixes" / "mcp-authorization-corrected"
ART_DIR = Path("/usr/local/google/home/nitinagga/.gemini/jetski/brain/016fe044-5d2e-431d-9b46-ee4a82f8029f")

# 5 Sequence Lifelines (canvas width = 1080)
LIFELINES = [
    {"id": "user", "label": "User / Browser", "x": 244, "w": 124, "bg": "#FEF9C3", "border": "#CA8A04", "fg": "#854D0E"},
    {"id": "client", "label": "MCP Client", "x": 424, "w": 122, "bg": "#EFF6FF", "border": "#2563EB", "fg": "#1E40AF"},
    {"id": "server", "label": "MCP Server", "x": 624, "w": 124, "bg": "#ECFDF5", "border": "#059669", "fg": "#065F46"},
    {"id": "auth", "label": "Auth Server / STS", "x": 826, "w": 138, "bg": "#FFFBEB", "border": "#D97706", "fg": "#92400E"},
    {"id": "upstream", "label": "Upstream API", "x": 990, "w": 116, "bg": "#F5F3FF", "border": "#7C3AED", "fg": "#5B21B6"},
]
LX = {l["id"]: l["x"] for l in LIFELINES}

PHASES = [
    {"num": 1, "name": "Challenge", "steps": [1, 2], "bg": "#F1F5F9", "rule": 4, "actors": ["client", "server"]},
    {"num": 2, "name": "Discover", "steps": [3, 4, 5], "bg": "#FFFFFF", "rule": 4, "actors": ["client", "server", "auth"]},
    {"num": 3, "name": "Register", "steps": [6], "bg": "#F1F5F9", "rule": 1, "actors": ["client", "auth"]},
    {"num": 4, "name": "Authorize", "steps": [7, 8, 9, 10], "bg": "#FFFFFF", "rule": 1, "actors": ["user", "client", "auth"]},
    {"num": 5, "name": "Token", "steps": [11, 12], "bg": "#F1F5F9", "rule": 2, "actors": ["client", "auth"]},
    {"num": 6, "name": "Call & Verify", "steps": [13, 14], "bg": "#FFFFFF", "rule": 2, "actors": ["client", "server"]},
    {"num": 7, "name": "Upstream OBO", "steps": [15, 16], "bg": "#F5F3FF", "rule": 3, "actors": ["server", "auth", "upstream"]},
]

# Each step: (num, phase_num, src, dst, dashed, bidir, tokens_html, plain_label)
STEPS: List[Dict[str, Any]] = [
    {
        "num": 1, "phase": 1, "src": "client", "dst": "server", "dashed": False, "bidir": False,
        "label_x": 524, "align": "center",
        "html": "<code>POST /mcp</code> no token &middot; <code>MCP-Protocol-Version</code>",
        "plain": "POST /mcp (no token) + MCP-Protocol-Version",
    },
    {
        "num": 2, "phase": 1, "src": "server", "dst": "client", "dashed": True, "bidir": False,
        "label_x": 524, "align": "center",
        "html": "<code>401</code> + <code>WWW-Authenticate</code>: resource_metadata, scope",
        "plain": "401 + WWW-Authenticate: resource_metadata, scope",
    },
    {
        "num": 3, "phase": 2, "src": "client", "dst": "server", "dashed": False, "bidir": False,
        "label_x": 524, "align": "center",
        "html": "<code>GET /.well-known/oauth-protected-resource</code> (RFC 9728)",
        "plain": "GET /.well-known/oauth-protected-resource (RFC 9728)",
    },
    {
        "num": 4, "phase": 2, "src": "server", "dst": "client", "dashed": True, "bidir": False,
        "label_x": 524, "align": "center",
        "html": "<code>authorization_servers</code>, <code>scopes_supported</code>, <code>resource</code>",
        "plain": "authorization_servers, scopes_supported, resource",
    },
    {
        "num": 5, "phase": 2, "src": "client", "dst": "auth", "dashed": False, "bidir": True,
        "label_x": 625, "align": "center",
        "html": "Fetch AS metadata <b>(RFC 8414 / OIDC)</b> &middot; verify <code>S256</code> PKCE",
        "plain": "Fetch AS metadata (RFC 8414 / OIDC) + verify S256 PKCE",
    },
    {
        "num": 6, "phase": 3, "src": "client", "dst": "auth", "dashed": False, "bidir": True,
        "label_x": 625, "align": "center",
        "html": "Get <code>client_id</code>: Pre-registered &gt; <b>CIMD</b> &gt; DCR (legacy fallback)",
        "plain": "Get client_id: Pre-registered > CIMD > DCR (legacy fallback)",
    },
    {
        "num": 7, "phase": 4, "src": "client", "dst": "user", "dashed": False, "bidir": False,
        "label_x": 388, "align": "center",
        "html": "Open <code>/authorize</code> + <code>S256</code> + <code>resource</code> + <code>state</code> + <code>redirect_uri</code>",
        "plain": "Open /authorize + PKCE S256 + resource + state + redirect_uri",
    },
    {
        "num": 8, "phase": 4, "src": "user", "dst": "auth", "dashed": False, "bidir": False,
        "label_x": 535, "align": "center",
        "html": "User signs in &amp; approves least-privilege scopes",
        "plain": "User signs in & approves least-privilege scopes",
    },
    {
        "num": 9, "phase": 4, "src": "auth", "dst": "user", "dashed": True, "bidir": False,
        "label_x": 535, "align": "center",
        "html": "Redirect callback with <code>code</code> + <code>state</code> + <code>iss</code> (RFC 9207)",
        "plain": "Redirect callback with code + state + iss (RFC 9207)",
    },
    {
        "num": 10, "phase": 4, "src": "user", "dst": "client", "dashed": False, "bidir": False,
        "label_x": 386, "align": "center",
        "html": "Callback &rarr; client verifies <code>state</code> &amp; <code>iss</code> match (blocks CSRF)",
        "plain": "Callback -> client verifies state & iss match (blocks CSRF/mix-up)",
    },
    {
        "num": 11, "phase": 5, "src": "client", "dst": "auth", "dashed": False, "bidir": False,
        "label_x": 625, "align": "center",
        "html": "<code>POST /token</code> + <code>code_verifier</code> + <code>redirect_uri</code> + <code>resource</code>",
        "plain": "POST /token + code_verifier + redirect_uri + resource",
    },
    {
        "num": 12, "phase": 5, "src": "auth", "dst": "client", "dashed": True, "bidir": False,
        "label_x": 625, "align": "center",
        "html": "Access token (<code>aud = this MCP server</code>) + <code>refresh_token</code>",
        "plain": "Access token (aud = this MCP server) + refresh_token",
    },
    {
        "num": 13, "phase": 6, "src": "client", "dst": "server", "dashed": False, "bidir": False,
        "label_x": 524, "align": "center",
        "html": "<code>POST /mcp</code> &middot; <code>Bearer &lt;token&gt;</code> &middot; <code>Mcp-Session-Id</code>",
        "plain": "POST /mcp + Authorization: Bearer <token> + Mcp-Session-Id",
    },
    {
        "num": 14, "phase": 6, "src": "server", "dst": "server", "dashed": False, "bidir": False,
        "label_x": 672, "align": "left",
        "html": "Validate signature, <code>exp</code>, <code>aud == self</code>, <code>scope</code>",
        "plain": "Validate signature, exp, aud == self, scope",
    },
    {
        "num": 15, "phase": 7, "src": "server", "dst": "auth", "dashed": False, "bidir": True,
        "label_x": 725, "align": "center",
        "html": "<b>RFC 8693 OBO</b> token swap (or per-user Token Vault)",
        "plain": "RFC 8693 OBO token swap (or per-user Token Vault)",
    },
    {
        "num": 16, "phase": 7, "src": "server", "dst": "upstream", "dashed": False, "bidir": False,
        "label_x": 807, "align": "center",
        "html": "Call upstream with caller-scoped OBO token &rarr; <code>200 OK</code>",
        "plain": "Call upstream with caller-scoped OBO token -> 200 OK",
    },
]

SECURITY_RULES = [
    {
        "num": 1,
        "title": "PKCE S256 + state + iss",
        "body": "Mandatory <b>S256</b> PKCE, <code>state</code> CSRF check, exact <code>redirect_uri</code>, and <code>iss</code> (RFC 9207) validation stop code interception &amp; mix-up.",
        "accent": "#2563EB",
        "icon": "lock",
    },
    {
        "num": 2,
        "title": "Audience-bound (RFC 8707)",
        "body": "The <code>resource</code> parameter binds every token (<code>aud</code>) to a single MCP server. Resource servers reject cross-server tokens.",
        "accent": "#7C3AED",
        "icon": "target",
    },
    {
        "num": 3,
        "title": "No passthrough &rarr; OBO",
        "body": "Never forward the client&rsquo;s MCP token or share static server keys. Exchange via <b>RFC 8693 OBO</b> or a per-user Token Vault.",
        "accent": "#059669",
        "icon": "shield",
    },
    {
        "num": 4,
        "title": "Least-privilege &amp; step-up",
        "body": "Ask only for challenged scopes. Missing permissions return <code>403 insufficient_scope</code> to trigger incremental re-auth.",
        "accent": "#D97706",
        "icon": "key",
    },
]


def _rule_icon_svg(kind: str, color: str) -> str:
    if kind == "lock":
        return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="4" y="10" width="16" height="11" rx="3" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-width="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="{color}" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="15.5" r="1.5" fill="{color}"/></svg>'
    if kind == "target":
        return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-width="2"/><circle cx="12" cy="12" r="5" stroke="{color}" stroke-width="2"/><circle cx="12" cy="12" r="1.8" fill="{color}"/></svg>'
    if kind == "shield":
        return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 3L4 6.5V12c0 4.8 3.4 8.7 8 9.8 4.6-1.1 8-5 8-9.8V6.5L12 3z" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-width="2" stroke-linejoin="round"/><path d="M9 12.2l2 2 4-4.2" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="8.5" cy="12" r="4.5" fill="{color}" fill-opacity="0.16" stroke="{color}" stroke-width="2"/><path d="M13 12h8M18 12v3M21 12v2.5" stroke="{color}" stroke-width="2" stroke-linecap="round"/></svg>'


def build_html_canvas(active_step: int = 0, step_progress: float = 0.5) -> str:
    """Render the exact 1080x1350 visual state for either static (active_step=0) or animated step (1..16)."""
    active_phase = 0
    active_rule = 0
    active_actors = set()
    if active_step > 0:
        st_obj = STEPS[active_step - 1]
        active_phase = st_obj["phase"]
        ph_obj = PHASES[active_phase - 1]
        active_rule = ph_obj["rule"]
        active_actors = set(ph_obj["actors"])

    # Band 2 inner body local coordinate space: width=1040 (x_local = x_canvas - 20), height=698 (y_local in [0, 698])
    row_top = 46.0
    row_pitch = 36.8
    phase_bands_html = []
    for ph in PHASES:
        s0 = ph["steps"][0] - 1
        s1 = ph["steps"][-1] - 1
        y_start = row_top + s0 * row_pitch - 3.0
        h = (s1 - s0 + 1) * row_pitch
        is_active = ph["num"] == active_phase
        bg = "#DBEAFE" if is_active else ph["bg"]
        border_left = "4px solid #2563EB" if is_active else "4px solid transparent"
        badge_bg = "#2563EB" if is_active else "#0F172A"
        phase_bands_html.append(
            f'<div class="phase-band" style="top:{y_start:.1f}px;height:{h:.1f}px;background:{bg};border-left:{border_left};">'
            f'<div class="phase-tag" style="top:{(h/2 - 11):.1f}px;">'
            f'<span class="p-num" style="background:{badge_bg};">{ph["num"]}</span>'
            f'<span class="p-name" style="color:{"#1E3A8A" if is_active else "#0F172A"};">{html.escape(ph["name"])}</span>'
            f'</div></div>'
        )

    # Lifeline headers (top=10px..38px) and vertical dashed lines (y=38..642) in Band 2 local coordinates
    lifeline_hdrs = []
    lifeline_lines = []
    for ll in LIFELINES:
        lx_local = ll["x"] - 20.0
        left = lx_local - ll["w"] / 2.0
        is_act = ll["id"] in active_actors
        ring = "box-shadow:0 0 0 3px rgba(37,99,235,0.35);" if is_act else ""
        lifeline_hdrs.append(
            f'<div class="ll-pill" style="left:{left:.1f}px;width:{ll["w"]}px;background:{ll["bg"]};border-color:{ll["border"]};color:{ll["fg"]};{ring}">'
            f'{html.escape(ll["label"])}</div>'
        )
        lifeline_lines.append(
            f'<line x1="{lx_local:.1f}" y1="38" x2="{lx_local:.1f}" y2="640" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="5,5"/>'
        )

    # Sequence arrows + animated packet dots + step pills (all in Band 2 local coordinates 0..1040 x 0..698)
    step_svg_parts = []
    step_labels_html = []
    for st in STEPS:
        idx = st["num"] - 1
        y_label = row_top + idx * row_pitch + 0.5
        y_arrow = row_top + idx * row_pitch + 27.0
        x1 = LX[st["src"]] - 20.0
        x2 = LX[st["dst"]] - 20.0
        is_cur = st["num"] == active_step
        is_done = active_step > 0 and st["num"] < active_step
        stroke = "#2563EB" if is_cur else ("#059669" if is_done else "#1E293B")
        sw = "2.5" if is_cur else "1.8"
        dash = 'stroke-dasharray="6,4"' if st["dashed"] else ""
        marker_end = 'marker-end="url(#arr-blue)"' if is_cur else ('marker-end="url(#arr-green)"' if is_done else 'marker-end="url(#arr-dark)"')
        marker_start = ('marker-start="url(#arr-blue-rev)"' if is_cur else ('marker-start="url(#arr-green-rev)"' if is_done else 'marker-start="url(#arr-dark-rev)"')) if st["bidir"] else ""

        if st["src"] == st["dst"]:
            # Clean self-loop bracket anchored right of MCP Server lifeline
            yc = row_top + idx * row_pitch + 17.5
            step_svg_parts.append(
                f'<path d="M {x1:.1f} {yc - 8:.1f} L {x1 + 28:.1f} {yc - 8:.1f} L {x1 + 28:.1f} {yc + 8:.1f} L {x1 + 6:.1f} {yc + 8:.1f}" '
                f'fill="none" stroke="{stroke}" stroke-width="{sw}" {marker_end}/>'
            )
            if is_cur:
                py = yc - 8.0 + 16.0 * step_progress
                step_svg_parts.append(
                    f'<circle cx="{x1 + 28:.1f}" cy="{py:.1f}" r="5.4" fill="#FDE047" stroke="#1E3A8A" stroke-width="2"/>'
                )
        else:
            adj_x1 = x1 + (7 if x2 > x1 else -7) if st["bidir"] else x1
            adj_x2 = x2 + (-7 if x2 > x1 else 7)
            step_svg_parts.append(
                f'<line x1="{adj_x1:.1f}" y1="{y_arrow:.1f}" x2="{adj_x2:.1f}" y2="{y_arrow:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash} {marker_start} {marker_end}/>'
            )
            if is_cur:
                t = max(0.10, min(0.90, step_progress))
                px = x1 + (x2 - x1) * t
                step_svg_parts.append(
                    f'<circle cx="{px:.1f}" cy="{y_arrow:.1f}" r="5.6" fill="#FDE047" stroke="#1E3A8A" stroke-width="2"/>'
                )

        num_bg = "#2563EB" if is_cur else ("#059669" if is_done else "#0F172A")
        lbl_border = "border:1.5px solid #2563EB;background:#EFF6FF;" if is_cur else "border:1px solid transparent;background:rgba(255,255,255,0.95);"
        lbl_x_local = st["label_x"] - 20.0
        if st["align"] == "left":
            yc = row_top + idx * row_pitch + 17.5
            pos_css = f"left:{x1 + 36:.1f}px;top:{yc - 10.5:.1f}px;"
        else:
            pos_css = f"left:{lbl_x_local:.1f}px;top:{y_label:.1f}px;transform:translateX(-50%);"
        step_labels_html.append(
            f'<div class="step-label" style="{pos_css}{lbl_border}">'
            f'<span class="s-num" style="background:{num_bg};">{st["num"]}</span>'
            f'<span class="s-txt">{st["html"]}</span>'
            f'</div>'
        )

    # Band 1 actor highlight state
    def _act_cls(aid: str) -> str:
        return "actor-card actor-active" if aid in active_actors else "actor-card"

    # Band 1 animated packet dots (SVG local coords 0..1040 x 0..238; ONLY shown during animation frames)
    b1_dots = []
    if active_step > 0:
        t = max(0.18, min(0.82, step_progress))
        if active_phase == 4:
            # Moving along User -> Auth Server L-connector horizontal leg
            b1_dots.append(f'<circle cx="{126 + (246-126)*t:.1f}" cy="187" r="5.2" fill="#FDE047" stroke="#1E3A8A" stroke-width="1.8"/>')
        elif active_phase in (1, 6):
            # Moving along MCP Client <-> MCP Server horizontal edge
            b1_dots.append(f'<circle cx="{484 + (510-484)*t:.1f}" cy="56" r="5.0" fill="#38BDF8" stroke="#0F172A" stroke-width="1.6"/>')
        elif active_phase in (2, 3, 5):
            # Moving along MCP Client <-> Auth Server vertical edge
            b1_dots.append(f'<circle cx="368" cy="{114 + (138-114)*t:.1f}" r="5.0" fill="#FDE047" stroke="#1E3A8A" stroke-width="1.6"/>')
        elif active_phase == 7:
            # Moving along MCP Server <-> Auth Server OBO swap AND MCP Server -> Upstream API
            b1_dots.append(f'<circle cx="634" cy="{114 + (138-114)*t:.1f}" r="5.0" fill="#A78BFA" stroke="#3B0764" stroke-width="1.6"/>')
            b1_dots.append(f'<circle cx="{756 + (782-756)*t:.1f}" cy="56" r="5.0" fill="#A78BFA" stroke="#3B0764" stroke-width="1.6"/>')

    # Band 3 security rule cards
    rule_cards_html = []
    for r in SECURITY_RULES:
        is_ra = r["num"] == active_rule
        border_css = f"2px solid {r['accent']};box-shadow:0 6px 18px rgba(37,99,235,0.14);background:#FFFFFF;" if is_ra else "1.5px solid #BBF7D0;background:#ECFDF5;"
        rule_cards_html.append(
            f'<div class="rule-card" style="border:{border_css}">'
            f'<div class="rule-top"><span class="r-num" style="background:{r["accent"]};">{r["num"]}</span>{_rule_icon_svg(r["icon"], r["accent"])}</div>'
            f'<div class="rule-title">{r["title"]}</div>'
            f'<div class="rule-body">{r["body"]}</div>'
            f'</div>'
        )

    progress_badge = f"STEP {active_step:02d}/16" if active_step > 0 else "7 PHASES · 16 VERIFIED STEPS"

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 1080px; height: 1350px; overflow: hidden; position: relative;
  background: #F8FAFC; color: #0F172A;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}}
.quad-bar {{
  position: absolute; top: 0; left: 0; right: 0; height: 5px;
  background: linear-gradient(90deg, #4285F4 0 25%, #EA4335 25% 50%, #FBBC04 50% 75%, #34A853 75% 100%);
}}
.header {{
  position: absolute; top: 14px; left: 20px; right: 20px; height: 92px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
}}
.header h1 {{
  font-size: 36px; font-weight: 900; letter-spacing: -0.025em; color: #0F172A; line-height: 1.15;
}}
.header h1 mark {{
  background: #FDE047; color: #0F172A; padding: 2px 12px; border-radius: 7px;
}}
.header p {{
  margin-top: 7px; font-size: 16px; color: #334155; font-weight: 500;
}}
.header p b {{ color: #0F172A; font-weight: 800; }}

.panel {{
  position: absolute; left: 20px; width: 1040px;
  background: #FFFFFF; border: 1.5px solid #CBD5E1; border-radius: 14px;
  box-shadow: 0 4px 14px rgba(15,23,42,0.04); overflow: hidden;
}}
.panel-hdr {{
  height: 36px; background: #1E293B; color: #FDE047;
  display: flex; align-items: center; justify-content: center; position: relative;
  font-size: 17px; font-weight: 800; letter-spacing: 0.01em;
}}
.panel-hdr .hdr-pill {{
  position: absolute; right: 14px; font-size: 11px; font-weight: 700;
  background: rgba(255,255,255,0.12); color: #E2E8F0; padding: 3px 10px; border-radius: 99px;
  letter-spacing: 0.03em;
}}

/* Band 1 */
#band1 {{ top: 112px; height: 274px; }}
.actor-card {{
  position: absolute; border-radius: 10px; padding: 9px 12px;
  border: 1.5px solid #CBD5E1; background: #FEFCE8;
}}
.actor-active {{
  box-shadow: 0 0 0 3px rgba(37,99,235,0.32); border-color: #2563EB !important;
}}
.actor-hdr {{ display: flex; align-items: center; gap: 7px; margin-bottom: 4px; }}
.actor-badge {{
  width: 22px; height: 22px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 900; color: #FFFFFF; flex-shrink: 0;
}}
.actor-name {{ font-size: 14.5px; font-weight: 800; color: #0F172A; line-height: 1.15; }}
.actor-role {{ font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 3px; }}
.actor-desc {{ font-size: 11.4px; color: #1E293B; line-height: 1.3; }}
.actor-desc code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10.6px;
  background: rgba(15,23,42,0.06); padding: 0 3px; border-radius: 3px; font-weight: 700;
}}
.edge-tag {{
  position: absolute; font-size: 11px; font-weight: 700; color: #0F172A;
  background: rgba(255,255,255,0.94); padding: 1px 6px; border-radius: 4px;
}}
.obo-note {{
  position: absolute; left: 790px; top: 170px; width: 236px; height: 92px;
  background: #F5F3FF; border: 1.5px solid #C4B5FD; border-radius: 10px; padding: 8px 10px;
}}
.obo-note .t {{ font-size: 11px; font-weight: 800; color: #5B21B6; margin-bottom: 3px; }}
.obo-note .b {{ font-size: 11px; color: #1E293B; line-height: 1.32; }}

/* Band 2 */
#band2 {{ top: 396px; height: 734px; }}
.phase-band {{
  position: absolute; left: 0; right: 0; z-index: 1;
}}
.phase-tag {{
  position: absolute; left: 14px; display: flex; align-items: center; gap: 7px; width: 150px;
}}
.p-num {{
  width: 22px; height: 22px; border-radius: 50%; color: #FFFFFF;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800; flex-shrink: 0;
}}
.p-name {{ font-size: 13.5px; font-weight: 800; letter-spacing: -0.01em; }}
.ll-pill {{
  position: absolute; top: 10px; height: 28px; border-radius: 8px; border: 1.5px solid;
  display: flex; align-items: center; justify-content: center;
  font-size: 12.2px; font-weight: 800; z-index: 3;
}}
.step-label {{
  position: absolute; z-index: 4; display: inline-flex; align-items: center; gap: 5px;
  padding: 1.5px 7px; border-radius: 6px; white-space: nowrap;
  font-size: 11.6px; color: #0F172A; font-weight: 600; line-height: 1.25;
}}
.s-num {{
  min-width: 17px; height: 17px; border-radius: 50%; color: #FFFFFF;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 800; padding: 0 4px; flex-shrink: 0;
}}
.s-txt code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 10.6px; font-weight: 700; color: #0F172A;
  background: #F1F5F9; border: 1px solid #CBD5E1; padding: 0px 4px; border-radius: 4px;
}}
.stepup-bar {{
  position: absolute; left: 16px; right: 16px; bottom: 10px; height: 36px; z-index: 4;
  background: #FFFBEB; border: 1.5px solid #F59E0B; border-radius: 9px;
  display: flex; align-items: center; justify-content: center; gap: 14px;
  font-size: 11.8px; font-weight: 700; color: #78350F;
}}
.stepup-bar code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px;
  background: #FEF3C7; border: 1px solid #FCD34D; padding: 1px 5px; border-radius: 4px; color: #92400E;
}}

/* Band 3 */
#band3 {{ top: 1140px; height: 174px; }}
.rules-grid {{
  position: absolute; top: 46px; left: 14px; right: 14px; bottom: 12px;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
}}
.rule-card {{
  border-radius: 10px; padding: 9px 11px; display: flex; flex-direction: column;
}}
.rule-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }}
.r-num {{
  width: 20px; height: 20px; border-radius: 50%; color: #FFFFFF;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 900;
}}
.rule-title {{ font-size: 13px; font-weight: 800; color: #0F172A; margin-bottom: 4px; letter-spacing: -0.01em; }}
.rule-body {{ font-size: 11.2px; color: #1E293B; line-height: 1.33; }}
.rule-body code {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10.3px;
  background: #FFFFFF; border: 1px solid #CBD5E1; padding: 0 3px; border-radius: 3px; font-weight: 700;
}}

.footer {{
  position: absolute; bottom: 8px; left: 24px; right: 24px; height: 22px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 10.8px; font-weight: 800; color: #475569; letter-spacing: 0.03em;
}}
.footer .brand {{ color: #0F172A; }}
</style>
</head>
<body>
<div class="quad-bar"></div>

<div class="header">
  <h1>How <mark>Enterprise MCP Authorization</mark> Works</h1>
  <p>How an AI app gets <b>scoped, audience-bound, On-Behalf-Of</b> access to a remote MCP server</p>
</div>

<!-- BAND 1 -->
<div class="panel" id="band1">
  <div class="panel-hdr">
    Who&rsquo;s Involved
    <span class="hdr-pill">MCP 2025-11-25 &middot; OAuth 2.1 + RFC 8693 OBO</span>
  </div>

  <!-- Connectors SVG inside Band 1 (top:36px -> local height 238px) -->
  <svg width="1040" height="238" viewBox="0 0 1040 238" style="position:absolute;top:36px;left:0;z-index:1;">
    <defs>
      <marker id="b1-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,1 L7,4 L0,7 Z" fill="#0F172A"/></marker>
      <marker id="b1-arr-rev" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,1 L1,4 L8,7 Z" fill="#0F172A"/></marker>
    </defs>
    <!-- Top row horizontal connectors (card vertical center = top 44 + 48 - 36 = 56) -->
    <line x1="218" y1="56" x2="256" y2="56" stroke="#0F172A" stroke-width="2" marker-end="url(#b1-arr)"/>
    <line x1="478" y1="56" x2="516" y2="56" stroke="#0F172A" stroke-width="2" marker-end="url(#b1-arr)"/>
    <line x1="750" y1="56" x2="788" y2="56" stroke="#0F172A" stroke-width="2" marker-end="url(#b1-arr)"/>
    <!-- User -> Auth Server (orthogonal L: bottom of User is 104, center of Auth Server is 187) -->
    <path d="M 116 104 L 116 187 L 256 187" fill="none" stroke="#0F172A" stroke-width="2" marker-end="url(#b1-arr)"/>
    <!-- MCP Client <-> Auth Server (40px vertical channel: y=106..146) -->
    <line x1="368" y1="106" x2="368" y2="146" stroke="#0F172A" stroke-width="2" marker-start="url(#b1-arr-rev)" marker-end="url(#b1-arr)"/>
    <!-- MCP Server <-> Auth Server (dashed: PRM names AS + OBO swap) -->
    <line x1="634" y1="106" x2="634" y2="146" stroke="#0F172A" stroke-width="2" stroke-dasharray="5,3.5" marker-start="url(#b1-arr-rev)" marker-end="url(#b1-arr)"/>
    {''.join(b1_dots)}
  </svg>

  <div class="{_act_cls('user')}" style="left:14px;top:44px;width:204px;height:96px;background:#FEF9C3;border-color:#CA8A04;z-index:2;">
    <div class="actor-hdr"><span class="actor-badge" style="background:#CA8A04;">U</span><span class="actor-name">User</span></div>
    <div class="actor-role">Resource owner</div>
    <div class="actor-desc">Signs in and approves scoped access in a browser</div>
  </div>

  <div class="{_act_cls('client')}" style="left:258px;top:44px;width:220px;height:96px;background:#EFF6FF;border-color:#2563EB;z-index:2;">
    <div class="actor-hdr"><span class="actor-badge" style="background:#2563EB;">C</span><span class="actor-name">MCP Client</span></div>
    <div class="actor-role">OAuth 2.1 client</div>
    <div class="actor-desc">Lives inside host app (IDE, chat app, ADK agent)</div>
  </div>

  <div class="{_act_cls('server')}" style="left:518px;top:44px;width:232px;height:96px;background:#ECFDF5;border-color:#059669;z-index:2;">
    <div class="actor-hdr"><span class="actor-badge" style="background:#059669;">S</span><span class="actor-name">MCP Server</span></div>
    <div class="actor-role">OAuth resource server</div>
    <div class="actor-desc">Publishes RFC 9728 metadata, validates every JWT &amp; <code>aud</code></div>
  </div>

  <div class="{_act_cls('upstream')}" style="left:790px;top:44px;width:236px;height:96px;background:#F5F3FF;border-color:#7C3AED;z-index:2;">
    <div class="actor-hdr"><span class="actor-badge" style="background:#7C3AED;">A</span><span class="actor-name">Upstream API</span></div>
    <div class="actor-role">Optional (GitHub &middot; Gmail &middot; Jira)</div>
    <div class="actor-desc">Enforces per-caller RLS using OBO token (never client&rsquo;s raw token)</div>
  </div>

  <div class="{_act_cls('auth')}" style="left:258px;top:184px;width:492px;height:78px;background:#FFFBEB;border-color:#D97706;z-index:2;">
    <div class="actor-hdr"><span class="actor-badge" style="background:#D97706;">AS</span><span class="actor-name">Authorization Server / IAM STS</span> <span style="font-size:11px;font-weight:700;color:#92400E;margin-left:auto;">Separate role (co-hosted or IdP-delegated)</span></div>
    <div class="actor-desc">Authenticates user, renders consent, enforces PKCE, mints <code>aud</code>-bound MCP tokens &amp; exchanges <b>RFC 8693 OBO</b> upstream tokens.</div>
  </div>

  <div class="edge-tag" style="left:134px;top:200px;z-index:2;">login + consent</div>
  <div class="edge-tag" style="left:378px;top:154px;z-index:2;">discover &middot; register &middot; token</div>
  <div class="edge-tag" style="left:644px;top:154px;z-index:2;">names AS &amp; OBO swap</div>

  <div class="obo-note" style="z-index:2;">
    <div class="t">NO STATIC KEYS / NO PASSTHROUGH</div>
    <div class="b">MCP Server exchanges caller identity via <b>RFC 8693 OBO</b> (or per-user Token Vault) to prevent Confused-Deputy bypass.</div>
  </div>
</div>

<!-- BAND 2 -->
<div class="panel" id="band2">
  <div class="panel-hdr">
    The Flow, Step by Step
    <span class="hdr-pill">{progress_badge}</span>
  </div>

  <!-- Local coordinate space: 1040 x 698 -->
  <div style="position:relative;width:1040px;height:698px;">
    {''.join(phase_bands_html)}
    {''.join(lifeline_hdrs)}

    <svg width="1040" height="698" viewBox="0 0 1040 698" style="position:absolute;top:0;left:0;z-index:2;">
      <defs>
        <marker id="arr-dark" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,1 L7,4 L0,7 Z" fill="#1E293B"/></marker>
        <marker id="arr-dark-rev" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,1 L1,4 L8,7 Z" fill="#1E293B"/></marker>
        <marker id="arr-blue" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,1 L8,4.5 L0,8 Z" fill="#2563EB"/></marker>
        <marker id="arr-blue-rev" markerWidth="9" markerHeight="9" refX="1" refY="4.5" orient="auto"><path d="M9,1 L1,4.5 L9,8 Z" fill="#2563EB"/></marker>
        <marker id="arr-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,1 L7,4 L0,7 Z" fill="#059669"/></marker>
        <marker id="arr-green-rev" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,1 L1,4 L8,7 Z" fill="#059669"/></marker>
      </defs>
      {''.join(lifeline_lines)}
      {''.join(step_svg_parts)}
    </svg>

    {''.join(step_labels_html)}

    <div class="stepup-bar">
      <span><b>Step-Up:</b> missing scope &rarr; <code>403 insufficient_scope</code> &rarr; incremental re-auth</span>
      <span style="color:#D97706;">|</span>
      <span><b>Headless / M2M Agents:</b> <code>ID-JAG (RFC 7523 + 8693)</code> or <code>client_credentials</code></span>
    </div>
  </div>
</div>

<!-- BAND 3 -->
<div class="panel" id="band3">
  <div class="panel-hdr">
    Enterprise Security Rules Baked In
    <span class="hdr-pill">ZERO-TRUST CHECKLIST</span>
  </div>
  <div class="rules-grid">
    {''.join(rule_cards_html)}
  </div>
</div>

<div class="footer">
  <span class="brand">NITIN AGGARWAL &middot; PRINCIPAL AI ARCHITECT, GOOGLE CLOUD</span>
  <span>MCP 2025-11-25 &middot; OAUTH 2.1 &middot; RFC 9728 &middot; RFC 8707 &middot; RFC 9207 &middot; RFC 8693 OBO</span>
</div>
</body>
</html>"""


def build_clean_standalone_svg() -> str:
    """Export a clean standalone 1080x1350 pure vector SVG 1.1 matching the HTML/PNG master."""
    import textwrap
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">',
        '<defs>',
        '<style>text{font-family:Inter,Arial,Helvetica,sans-serif;} .mono{font-family:monospace;}</style>',
        '<marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,1 L7,4 L0,7 Z" fill="#1E293B"/></marker>',
        '<marker id="ar" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8,1 L1,4 L8,7 Z" fill="#1E293B"/></marker>',
        '</defs>',
        '<rect width="1080" height="1350" fill="#F8FAFC"/>',
        '<rect x="0" y="0" width="270" height="5" fill="#4285F4"/>',
        '<rect x="270" y="0" width="270" height="5" fill="#EA4335"/>',
        '<rect x="540" y="0" width="270" height="5" fill="#FBBC04"/>',
        '<rect x="810" y="0" width="270" height="5" fill="#34A853"/>',
        '<rect x="272" y="20" width="492" height="44" rx="8" fill="#FDE047"/>',
        '<text x="540" y="53" text-anchor="middle" font-size="34" font-weight="900" fill="#0F172A">How Enterprise MCP Authorization Works</text>',
        '<text x="540" y="88" text-anchor="middle" font-size="16" font-weight="600" fill="#334155">How an AI app gets scoped, audience-bound, On-Behalf-Of access to a remote MCP server</text>',
        # Band 1 frame
        '<rect x="20" y="112" width="1040" height="274" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>',
        '<path d="M20,126 a14,14 0 0 1 14,-14 h1012 a14,14 0 0 1 14,14 v22 h-1040 z" fill="#1E293B"/>',
        '<text x="540" y="136" text-anchor="middle" font-size="17" font-weight="800" fill="#FDE047">Who’s Involved</text>',
        '<text x="1046" y="135" text-anchor="end" font-size="11" font-weight="700" fill="#E2E8F0">MCP 2025-11-25 · OAuth 2.1 + RFC 8693 OBO</text>',
    ]
    # Band 1 Actors
    b1_cards = [
        (34, 156, 204, 96, "#FEF9C3", "#CA8A04", "User", "Resource owner", "Signs in & approves scoped access"),
        (278, 156, 220, 96, "#EFF6FF", "#2563EB", "MCP Client", "OAuth 2.1 client", "Host app (IDE, chat, ADK agent)"),
        (538, 156, 232, 96, "#ECFDF5", "#059669", "MCP Server", "OAuth resource server", "Publishes RFC 9728, checks JWT + aud"),
        (810, 156, 236, 96, "#F5F3FF", "#7C3AED", "Upstream API", "Optional (GitHub · Gmail · Jira)", "Per-caller OBO token (never client’s)"),
        (278, 296, 492, 78, "#FFFBEB", "#D97706", "Authorization Server / IAM STS", "Separate role (co-hosted or IdP-delegated)", "PKCE consent + aud tokens + RFC 8693 OBO swap"),
    ]
    for x, y, w, h, bg, bd, t1, t2, t3 in b1_cards:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{bd}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+12}" y="{y+24}" font-size="14" font-weight="800" fill="#0F172A">{html.escape(t1)}</text>')
        parts.append(f'<text x="{x+12}" y="{y+42}" font-size="11" font-weight="700" fill="#475569">{html.escape(t2)}</text>')
        parts.append(f'<text x="{x+12}" y="{y+64}" font-size="11.5" fill="#1E293B">{html.escape(t3)}</text>')
    # OBO note card
    parts.extend([
        '<rect x="810" y="282" width="236" height="92" rx="10" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1.5"/>',
        '<text x="820" y="302" font-size="11" font-weight="800" fill="#5B21B6">NO STATIC KEYS / NO PASSTHROUGH</text>',
        '<text x="820" y="320" font-size="11" fill="#1E293B">MCP Server swaps caller identity via</text>',
        '<text x="820" y="336" font-size="11" font-weight="700" fill="#1E293B">RFC 8693 OBO (or Token Vault)</text>',
        '<text x="820" y="352" font-size="11" fill="#1E293B">to prevent Confused-Deputy bypass.</text>',
    ])
    # Band 1 Arrows + Edge labels
    parts.extend([
        '<line x1="238" y1="204" x2="274" y2="204" stroke="#0F172A" stroke-width="2" marker-end="url(#a)"/>',
        '<line x1="498" y1="204" x2="534" y2="204" stroke="#0F172A" stroke-width="2" marker-end="url(#a)"/>',
        '<line x1="770" y1="204" x2="806" y2="204" stroke="#0F172A" stroke-width="2" marker-end="url(#a)"/>',
        '<path d="M136,252 L136,335 L274,335" fill="none" stroke="#0F172A" stroke-width="2" marker-end="url(#a)"/>',
        '<text x="150" y="325" font-size="11" font-weight="700" fill="#0F172A">login + consent</text>',
        '<line x1="388" y1="254" x2="388" y2="294" stroke="#0F172A" stroke-width="2" marker-start="url(#ar)" marker-end="url(#a)"/>',
        '<text x="398" y="278" font-size="11" font-weight="700" fill="#0F172A">discover · register · token</text>',
        '<line x1="654" y1="254" x2="654" y2="294" stroke="#0F172A" stroke-width="2" stroke-dasharray="5,3.5" marker-start="url(#ar)" marker-end="url(#a)"/>',
        '<text x="664" y="278" font-size="11" font-weight="700" fill="#0F172A">names AS &amp; OBO swap</text>',
    ])
    # Band 2 frame
    parts.extend([
        '<rect x="20" y="396" width="1040" height="734" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>',
        '<path d="M20,410 a14,14 0 0 1 14,-14 h1012 a14,14 0 0 1 14,14 v22 h-1040 z" fill="#1E293B"/>',
        '<text x="540" y="420" text-anchor="middle" font-size="17" font-weight="800" fill="#FDE047">The Flow, Step by Step</text>',
        '<text x="1046" y="419" text-anchor="end" font-size="11" font-weight="700" fill="#E2E8F0">7 PHASES · 16 VERIFIED STEPS</text>',
    ])
    row_top = 478.0
    row_pitch = 36.8
    for ph in PHASES:
        s0, s1 = ph["steps"][0] - 1, ph["steps"][-1] - 1
        y_start = row_top + s0 * row_pitch - 3.0
        h = (s1 - s0 + 1) * row_pitch
        parts.append(f'<rect x="21" y="{y_start:.1f}" width="1038" height="{h:.1f}" fill="{ph["bg"]}"/>')
        ym = y_start + h / 2.0
        parts.append(f'<circle cx="44" cy="{ym:.1f}" r="11" fill="#0F172A"/>')
        parts.append(f'<text x="44" y="{ym+4:.1f}" text-anchor="middle" font-size="11" font-weight="800" fill="#FFFFFF">{ph["num"]}</text>')
        parts.append(f'<text x="62" y="{ym+4:.1f}" font-size="13" font-weight="800" fill="#0F172A">{html.escape(ph["name"])}</text>')
    for ll in LIFELINES:
        lx = ll["x"] - ll["w"] / 2.0
        parts.append(f'<rect x="{lx:.1f}" y="442" width="{ll["w"]}" height="28" rx="8" fill="{ll["bg"]}" stroke="{ll["border"]}" stroke-width="1.5"/>')
        parts.append(f'<text x="{ll["x"]}" y="460" text-anchor="middle" font-size="12" font-weight="800" fill="{ll["fg"]}">{html.escape(ll["label"])}</text>')
        parts.append(f'<line x1="{ll["x"]}" y1="470" x2="{ll["x"]}" y2="1072" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="5,5"/>')
    for st in STEPS:
        idx = st["num"] - 1
        ya = row_top + idx * row_pitch + 27.0
        yl = row_top + idx * row_pitch + 14.0
        x1, x2 = LX[st["src"]], LX[st["dst"]]
        dash = 'stroke-dasharray="6,4"' if st["dashed"] else ""
        ms = 'marker-start="url(#ar)"' if st["bidir"] else ""
        if st["src"] == st["dst"]:
            yc = row_top + idx * row_pitch + 17.5
            parts.append(f'<path d="M{x1},{yc-8:.1f} L{x1+28},{yc-8:.1f} L{x1+28},{yc+8:.1f} L{x1+6},{yc+8:.1f}" fill="none" stroke="#1E293B" stroke-width="1.8" marker-end="url(#a)"/>')
            parts.append(f'<text x="{x1+36}" y="{yc+4:.1f}" font-size="11.5" font-weight="700" fill="#0F172A">{st["num"]}. {html.escape(st["plain"])}</text>')
        else:
            ax1 = x1 + (6 if x2 > x1 else -6) if st["bidir"] else x1
            ax2 = x2 + (-6 if x2 > x1 else 6)
            parts.append(f'<line x1="{ax1}" y1="{ya:.1f}" x2="{ax2}" y2="{ya:.1f}" stroke="#1E293B" stroke-width="1.8" {dash} {ms} marker-end="url(#a)"/>')
            parts.append(f'<text x="{st["label_x"]}" y="{yl:.1f}" text-anchor="middle" font-size="11.2" font-weight="700" fill="#0F172A">{st["num"]}. {html.escape(st["plain"])}</text>')
    parts.extend([
        '<rect x="36" y="1084" width="1008" height="36" rx="9" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.5"/>',
        '<text x="540" y="1107" text-anchor="middle" font-size="11.8" font-weight="700" fill="#78350F">Step-Up: missing scope -&gt; 403 insufficient_scope -&gt; incremental re-auth  |  Headless / M2M Agents: ID-JAG (RFC 7523 + 8693) or client_credentials</text>',
        # Band 3
        '<rect x="20" y="1140" width="1040" height="174" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>',
        '<path d="M20,1154 a14,14 0 0 1 14,-14 h1012 a14,14 0 0 1 14,14 v20 h-1040 z" fill="#1E293B"/>',
        '<text x="540" y="1163" text-anchor="middle" font-size="16" font-weight="800" fill="#FDE047">Enterprise Security Rules Baked In</text>',
        '<text x="1046" y="1162" text-anchor="end" font-size="11" font-weight="700" fill="#E2E8F0">ZERO-TRUST CHECKLIST</text>',
    ])
    for i, r in enumerate(SECURITY_RULES):
        rx = 34 + i * 256
        parts.append(f'<rect x="{rx}" y="1186" width="244" height="116" rx="10" fill="#ECFDF5" stroke="#BBF7D0" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{rx+18}" cy="1204" r="10" fill="{r["accent"]}"/>')
        parts.append(f'<text x="{rx+18}" y="1208" text-anchor="middle" font-size="11" font-weight="800" fill="#FFFFFF">{r["num"]}</text>')
        clean_title = html.unescape(r["title"]).replace("→", "->")
        parts.append(f'<text x="{rx+12}" y="1232" font-size="13" font-weight="800" fill="#0F172A">{html.escape(clean_title)}</text>')
        clean_body = html.unescape(r["body"].replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", ""))
        wrapped = textwrap.wrap(clean_body, width=38)
        for li, line in enumerate(wrapped[:4]):
            parts.append(f'<text x="{rx+12}" y="{1252 + li*14}" font-size="10.6" fill="#1E293B">{html.escape(line)}</text>')
    parts.append('<text x="24" y="1336" font-size="11" font-weight="800" fill="#0F172A">NITIN AGGARWAL · PRINCIPAL AI ARCHITECT, GOOGLE CLOUD</text>')
    parts.append('<text x="1056" y="1336" text-anchor="end" font-size="11" font-weight="700" fill="#475569">MCP 2025-11-25 · OAUTH 2.1 · RFC 9728 · RFC 8707 · RFC 9207 · RFC 8693 OBO</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def build_editable_drawio_xml() -> str:
    """Build 100% native editable Draw.io XML with exact zero-collision vertices and edges."""
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        # Header
        '<mxCell id="hdr_bg" value="&lt;b&gt;How Enterprise MCP Authorization Works&lt;/b&gt;&lt;br/&gt;&lt;font style=&quot;font-size:13px;&quot;&gt;How an AI app gets scoped, audience-bound, On-Behalf-Of access to a remote MCP server (MCP 2025-11-25 + OAuth 2.1)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF9C3;strokeColor=#CA8A04;strokeWidth=2;fontSize=24;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="20" y="14" width="1040" height="84" as="geometry"/></mxCell>',
        # Band 1 Container
        '<mxCell id="b1_frame" value="Who\'s Involved (MCP 2025-11-25 + RFC 8693 OBO)" style="swimlane;startSize=34;rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;fontColor=#FDE047;strokeColor=#CBD5E1;strokeWidth=1.5;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="20" y="112" width="1040" height="274" as="geometry"/></mxCell>',
        '<mxCell id="v_user" value="&lt;b&gt;User&lt;/b&gt;&lt;br/&gt;&lt;i&gt;Resource owner&lt;/i&gt;&lt;br/&gt;Signs in &amp; approves scoped access in a browser" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF9C3;strokeColor=#CA8A04;strokeWidth=1.5;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b1_frame"><mxGeometry x="16" y="48" width="204" height="96" as="geometry"/></mxCell>',
        '<mxCell id="v_client" value="&lt;b&gt;MCP Client&lt;/b&gt;&lt;br/&gt;&lt;i&gt;OAuth 2.1 client&lt;/i&gt;&lt;br/&gt;Lives in host app (IDE, chat, ADK agent)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b1_frame"><mxGeometry x="258" y="48" width="220" height="96" as="geometry"/></mxCell>',
        '<mxCell id="v_server" value="&lt;b&gt;MCP Server&lt;/b&gt;&lt;br/&gt;&lt;i&gt;OAuth resource server&lt;/i&gt;&lt;br/&gt;Publishes RFC 9728 metadata, validates JWT + aud" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#059669;strokeWidth=1.5;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b1_frame"><mxGeometry x="518" y="48" width="232" height="96" as="geometry"/></mxCell>',
        '<mxCell id="v_upstream" value="&lt;b&gt;Upstream API&lt;/b&gt;&lt;br/&gt;&lt;i&gt;GitHub · Gmail · Jira&lt;/i&gt;&lt;br/&gt;Enforces per-caller RLS using RFC 8693 OBO token" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#7C3AED;strokeWidth=1.5;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b1_frame"><mxGeometry x="790" y="48" width="234" height="96" as="geometry"/></mxCell>',
        '<mxCell id="v_auth" value="&lt;b&gt;Authorization Server / IAM STS&lt;/b&gt; (Separate role: co-hosted or IdP-delegated)&lt;br/&gt;Authenticates user, renders consent, enforces PKCE, mints aud-bound MCP tokens &amp; RFC 8693 OBO upstream tokens" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#D97706;strokeWidth=1.5;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b1_frame"><mxGeometry x="258" y="180" width="492" height="78" as="geometry"/></mxCell>',
        '<mxCell id="v_obo_note" value="&lt;b&gt;NO STATIC KEYS / NO PASSTHROUGH&lt;/b&gt;&lt;br/&gt;MCP Server swaps caller JWT via RFC 8693 OBO (or per-user Token Vault) to block Confused-Deputy bypass." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#C4B5FD;strokeWidth=1.5;fontColor=#1E293B;fontSize=11;" vertex="1" parent="b1_frame"><mxGeometry x="790" y="168" width="234" height="90" as="geometry"/></mxCell>',
        # Band 1 Edges
        '<mxCell id="e_uc" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;" edge="1" parent="b1_frame" source="v_user" target="v_client"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e_cs" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;" edge="1" parent="b1_frame" source="v_client" target="v_server"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e_su" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;" edge="1" parent="b1_frame" source="v_server" target="v_upstream"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e_ua" value="login + consent" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;fontSize=11;fontStyle=1;" edge="1" parent="b1_frame" source="v_user" target="v_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e_ca" value="discover · register · token" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;startArrow=classic;endArrow=classic;fontSize=11;fontStyle=1;" edge="1" parent="b1_frame" source="v_client" target="v_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        '<mxCell id="e_sa" value="names AS + OBO swap" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0F172A;strokeWidth=2;dashed=1;startArrow=classic;endArrow=classic;fontSize=11;fontStyle=1;" edge="1" parent="b1_frame" source="v_server" target="v_auth"><mxGeometry relative="1" as="geometry"/></mxCell>',
        # Band 2 Container
        '<mxCell id="b2_frame" value="The Flow, Step by Step (7 Phases · 16 Verified Protocol Steps)" style="swimlane;startSize=34;rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;fontColor=#FDE047;strokeColor=#CBD5E1;strokeWidth=1.5;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="20" y="396" width="1040" height="734" as="geometry"/></mxCell>',
    ]
    for idx, st in enumerate(STEPS):
        y = 46 + idx * 38
        cells.append(
            f'<mxCell id="step_box_{st["num"]}" value="&lt;b&gt;{st["num"]:02d} [{html.escape(PHASES[st["phase"]-1]["name"])}]&lt;/b&gt; &amp;nbsp; {html.escape(st["src"].upper())} → {html.escape(st["dst"].upper())}: {html.escape(st["plain"])}" '
            f'style="rounded=1;whiteSpace=wrap;html=1;align=left;spacingLeft=12;fillColor={PHASES[st["phase"]-1]["bg"]};strokeColor=#CBD5E1;fontColor=#0F172A;fontSize=12;" vertex="1" parent="b2_frame">'
            f'<mxGeometry x="16" y="{y}" width="1008" height="32" as="geometry"/></mxCell>'
        )
    cells.append(
        '<mxCell id="b2_stepup" value="&lt;b&gt;Step-Up:&lt;/b&gt; missing scope → 403 insufficient_scope → incremental re-auth  |  &lt;b&gt;Headless / M2M Agents:&lt;/b&gt; ID-JAG (RFC 7523 + RFC 8693) or client_credentials" '
        'style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#78350F;fontSize=12;" vertex="1" parent="b2_frame"><mxGeometry x="16" y="684" width="1008" height="38" as="geometry"/></mxCell>'
    )
    # Band 3 Container
    cells.append(
        '<mxCell id="b3_frame" value="Enterprise Security Rules Baked In (Zero-Trust Checklist)" style="swimlane;startSize=34;rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;fontColor=#FDE047;strokeColor=#CBD5E1;strokeWidth=1.5;fontSize=15;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="20" y="1140" width="1040" height="174" as="geometry"/></mxCell>'
    )
    for i, r in enumerate(SECURITY_RULES):
        rx = 16 + i * 255
        clean_b = html.unescape(r["body"].replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", ""))
        title_c = html.unescape(r["title"])
        cells.append(
            f'<mxCell id="rule_{r["num"]}" value="&lt;b&gt;{r["num"]}. {html.escape(title_c)}&lt;/b&gt;&lt;br/&gt;{html.escape(clean_b)}" '
            f'style="rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=10;fillColor=#ECFDF5;strokeColor={r["accent"]};strokeWidth=1.5;fontColor=#0F172A;fontSize=11.5;" vertex="1" parent="b3_frame">'
            f'<mxGeometry x="{rx}" y="46" width="243" height="116" as="geometry"/></mxCell>'
        )

    return (
        '<mxfile host="app.diagrams.net" modified="2026-11-12T20:05:00.000Z" agent="IdeasMintingStudio" version="24.0.0">\n'
        '  <diagram id="enterprise-mcp-auth-v2" name="Enterprise MCP Authorization (Corrected)">\n'
        '    <mxGraphModel dx="1080" dy="1350" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1080" pageHeight="1350" math="0" shadow="0">\n'
        '      <root>\n        ' + "\n        ".join(cells) + '\n      </root>\n'
        '    </mxGraphModel>\n'
        '  </diagram>\n'
        '</mxfile>\n'
    )


def build_linkedin_post_markdown() -> str:
    return """# Your AI Agent Has Access to Your Tools. Who Governs Every Call? (Corrected Enterprise MCP Authorization Blueprint)

Connecting an AI Agent to GitHub, Gmail, or Jira without OAuth 2.1 authorization turns a productivity demo into an enterprise security incident.

The updated **MCP Authorization specification (`2025-11-25`)** cleanly separates the **MCP Server (OAuth Resource Server)** from the **Authorization Server** — and adds critical protections that many early tutorials miss.

Here is the complete **7-Phase, 16-Step Enterprise MCP Authorization Flow**:

1. **Challenge (`POST /mcp`)** -> Server responds `401` + `WWW-Authenticate: resource_metadata, scope`.
2. **Discover (`RFC 9728` + `RFC 8414`)** -> Client fetches `GET /.well-known/oauth-protected-resource` (notice the trailing `n`!) and Authorization Server metadata verifying mandatory `S256` PKCE support.
3. **Register** -> Resolve `client_id` in priority order: **Pre-registered > CIMD (Client ID Metadata Document) > DCR (legacy fallback)**.
4. **Authorize (`PKCE S256` + `state` + `iss`)** -> Browser sign-in with `resource` (RFC 8707), `state` (CSRF), `redirect_uri`, and `iss` (RFC 9207 mix-up protection).
5. **Token** -> Exchange authorization code + `code_verifier` + `redirect_uri` + `resource` for a short-lived, audience-bound `access_token` (`aud == this MCP server`).
6. **Call & Verify** -> Send `Authorization: Bearer <token>` + `MCP-Protocol-Version` + `Mcp-Session-Id`; server strictly validates signature, `exp`, `aud`, and `scope` (returning `403 insufficient_scope` for step-up consent).
7. **Upstream On-Behalf-Of (`RFC 8693 OBO`)** -> Never forward the client's raw MCP token upstream AND never share a single static server key across tenants (Confused-Deputy bypass). Exchange caller identity via **RFC 8693 OBO** (or a per-user Token Vault) before calling GitHub, Gmail, or Jira.

For headless/autonomous enterprise agents, pair this pattern with **Enterprise-Managed Authorization (`ID-JAG`: RFC 7523 + RFC 8693)** or scoped `client_credentials`.

Runnable Google Cloud ADK + FastMCP + IAM STS Reference Repo (`100`-trial evaluation harness & 24-slide architecture deck):
https://github.com/nitinaggarwal-12/ideas-mining/tree/main/generated-repos/gcp-mcp-zero-bloat-gateway

#MCP #ModelContextProtocol #AgenticAI #OAuth21 #ZeroTrust #GoogleCloud #VertexAI #CyberSecurity #AISecurity #EnterpriseAI
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chrome_bin = resolve_chrome_bin()
    if not chrome_bin:
        raise RuntimeError("Chrome binary not found")

    svg_path = OUT_DIR / "mcp_authorization_enterprise_v2.svg"
    drawio_path = OUT_DIR / "mcp_authorization_enterprise_v2.drawio"
    png_path = OUT_DIR / "mcp_authorization_enterprise_v2.png"
    gif_path = OUT_DIR / "mcp_authorization_enterprise_v2.gif"
    md_path = OUT_DIR / "mcp_authorization_linkedin_post.md"

    svg_path.write_text(build_clean_standalone_svg(), encoding="utf-8")
    drawio_path.write_text(build_editable_drawio_xml(), encoding="utf-8")
    md_path.write_text(build_linkedin_post_markdown(), encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="mcp_auth_v2_") as tmp_str:
        tmp = Path(tmp_str)
        # 1. Render static @2x Retina PNG (2160x2700) + run DOM collision audit via Puppeteer
        static_html = tmp / "static.html"
        static_html.write_text(build_html_canvas(active_step=0), encoding="utf-8")

        # 2. Generate 48 keyframes for sequential Steps 1..16 (3 sub-frames per step -> 16*3 = 48 frames + 4 overview frames = 52 frames @ 5fps = 10.4s)
        frame_htmls: List[Tuple[Path, Path]] = []
        frame_idx = 0
        # 4 intro overview frames (0.8s)
        for _ in range(4):
            hp = tmp / f"f_{frame_idx:03d}.html"
            pp = tmp / f"f_{frame_idx:03d}.png"
            hp.write_text(build_html_canvas(active_step=0), encoding="utf-8")
            frame_htmls.append((hp, pp))
            frame_idx += 1
        # 16 steps x 3 smooth packet positions (0.18, 0.50, 0.84) = 48 frames
        for s_num in range(1, 17):
            for prog in (0.18, 0.50, 0.84):
                hp = tmp / f"f_{frame_idx:03d}.html"
                pp = tmp / f"f_{frame_idx:03d}.png"
                hp.write_text(build_html_canvas(active_step=s_num, step_progress=prog), encoding="utf-8")
                frame_htmls.append((hp, pp))
                frame_idx += 1

        # Render static @2x PNG, run DOM bounding-box collision check, AND render all 52 GIF frames in a single Puppeteer browser instance!
        node_script = tmp / "render_all.js"
        node_script.write_text(
            f"""
const puppeteer = require('puppeteer');
const fs = require('fs');
(async () => {{
  const browser = await puppeteer.launch({{
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }});
  const page = await browser.newPage();

  // Static @2x Retina PNG + DOM collision check
  await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: 2 }});
  await page.goto('file://{static_html}', {{ waitUntil: 'load' }});
  const audit = await page.evaluate(() => {{
    const boxes = [];
    const checkSel = '.actor-card, .edge-tag, .obo-note, .phase-tag, .ll-pill, .step-label, .rule-card, .stepup-bar';
    document.querySelectorAll(checkSel).forEach((el, idx) => {{
      const r = el.getBoundingClientRect();
      boxes.push({{ idx, cls: el.className, text: el.textContent.trim().slice(0, 36), x1: r.left, y1: r.top, x2: r.right, y2: r.bottom }});
    }});
    const overlaps = [];
    const outOfBounds = [];
    for (const b of boxes) {{
      if (b.x1 < 0 || b.y1 < 0 || b.x2 > 1080.5 || b.y2 > 1350.5) outOfBounds.push(b);
    }}
    for (let i = 0; i < boxes.length; i++) {{
      for (let j = i + 1; j < boxes.length; j++) {{
        const a = boxes[i], b = boxes[j];
        const ix = Math.max(0, Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1));
        const iy = Math.max(0, Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1));
        if (ix > 1.5 && iy > 1.5) {{
          overlaps.push({{ a: a.text, b: b.text, area: Math.round(ix * iy) }});
        }}
      }}
    }}
    return {{ totalChecked: boxes.length, overlaps, outOfBounds }};
  }});
  console.log('DOM_AUDIT:', JSON.stringify(audit));
  await page.screenshot({{ path: '{png_path}' }});

  // Render 52 animated frames at 1x (1080x1350) for GIF89a
  await page.setViewport({{ width: 1080, height: 1350, deviceScaleFactor: 1 }});
  const total = {len(frame_htmls)};
  for (let i = 0; i < total; i++) {{
    const pad = String(i).padStart(3, '0');
    await page.goto(`file://{tmp}/f_${{pad}}.html`, {{ waitUntil: 'load' }});
    await page.screenshot({{ path: `{tmp}/f_${{pad}}.png` }});
  }}
  await browser.close();
}})();
""",
            encoding="utf-8",
        )
        node_env = {**os.environ, "NODE_PATH": f"{Path.home() / 'node_modules'}:{WORKSPACE_ROOT / 'node_modules'}"}
        subprocess.run(["node", str(node_script)], env=node_env, check=True)

        # Compile high-fidelity 4:5 GIF89a with ffmpeg palettegen + paletteuse
        palette = tmp / "palette.png"
        subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error", "-framerate", "5",
                "-i", str(tmp / "f_%03d.png"),
                "-vf", "palettegen=max_colors=192:stats_mode=diff",
                str(palette),
            ],
            check=True,
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error", "-framerate", "5",
                "-i", str(tmp / "f_%03d.png"),
                "-i", str(palette),
                "-lavfi", "paletteuse=dither=sierra2_4a",
                "-loop", "0",
                str(gif_path),
            ],
            check=True,
        )

        # Extract a mid-animation frame (Step 15 OBO active) for visual verification
        shutil.copyfile(str(tmp / "f_047.png"), str(ART_DIR / "mcp_auth_v2_anim_step15.png"))
        shutil.copyfile(str(tmp / "f_023.png"), str(ART_DIR / "mcp_auth_v2_anim_step07.png"))

    shutil.copyfile(str(png_path), str(ART_DIR / "mcp_authorization_enterprise_v2.png"))
    shutil.copyfile(str(gif_path), str(ART_DIR / "mcp_authorization_enterprise_v2.gif"))

    print("Artifacts written:")
    for p in (png_path, gif_path, svg_path, drawio_path, md_path):
        print(f"  - {p} ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
