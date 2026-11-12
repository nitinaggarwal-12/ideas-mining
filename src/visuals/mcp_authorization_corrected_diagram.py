"""Production-Hardened MCP Authorization Architecture Generator (4:5 1080x1350).

Produces a synchronized 5-format asset bundle correcting every typographical, formatting,
animation, WCAG contrast, and security-architecture flaw identified during forensic
audit of the original LinkedIn post ("How MCP Authorization Works", Jean Lee):

  1. W3C Zero-Origin SVG (1080x1350, Light Theme #F8FAFC/#FFFFFF, WCAG 2.2 AA >=4.5:1)
  2. @2x Retina PNG (2160x2700) + 1080x1350 1:1 PNG
  3. Sequential Animated GIF89a (1080x1350, 28 keyframes stepping Phases 1->6 cleanly)
  4. 100% Native Editable Draw.io XML (<mxfile>, 1080x1350)
  5. Publication-Ready LinkedIn Post Draft & Forensic Comparison Changelog (Markdown)
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.visuals.canonical_flow_svg import (
    BG,
    FONT,
    INK,
    MONO,
    NAVY,
    RED,
    SLATE,
    WHITE,
    _esc,
    resolve_chrome_bin,
    resolve_ffmpeg_bin,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "assets" / "corrected-posts" / "mcp-authorization-obo"

# WCAG 2.2 AA verified palette (>= 4.5:1 contrast with white badges AND soft pastel cards)
BLUE_AA = "#1D4ED8"     # 6.70:1 on white, 6.23:1 on #EFF6FF
PURPLE_AA = "#6D28D9"   # 6.94:1 on white, 6.42:1 on #F5F3FF
GREEN_AA = "#047857"    # 5.48:1 on white, 5.21:1 on #ECFDF5
AMBER_AA = "#B45309"    # 5.02:1 on white, 4.81:1 on #FFFBEB
TEAL_AA = "#0F766E"     # 5.47:1 on white, 5.25:1 on #F0FDFA
RED_AA = "#B91C1C"      # 6.47:1 on white

BLUE_BG = "#EFF6FF"
PURPLE_BG = "#F5F3FF"
GREEN_BG = "#ECFDF5"
AMBER_BG = "#FFFBEB"
TEAL_BG = "#F0FDFA"
BORDER = "#CBD5E1"
BORDER_LIGHT = "#E2E8F0"

W = 1080
H = 1350

# Five sequence lifelines separated cleanly by 210px horizontally
LANES = [
    {"id": "user", "x": 120, "title": "User / Browser", "sub": "Interactive PKCE (WIF->5)", "color": BLUE_AA, "bg": BLUE_BG},
    {"id": "client", "x": 330, "title": "MCP Client", "sub": "OAuth 2.1 Public / WIF", "color": PURPLE_AA, "bg": PURPLE_BG},
    {"id": "server", "x": 540, "title": "MCP Server", "sub": "Resource Server (RFC 9728)", "color": GREEN_AA, "bg": GREEN_BG},
    {"id": "auth", "x": 750, "title": "Auth Server (IdP)", "sub": "Co-hosted or Self-hosted", "color": AMBER_AA, "bg": AMBER_BG},
    {"id": "downstream", "x": 960, "title": "Downstream APIs", "sub": "GitHub · Gmail · Jira", "color": TEAL_AA, "bg": TEAL_BG},
]
LANE_X = {lane["id"]: lane["x"] for lane in LANES}

WHO_CARDS = [
    {
        "title": "User / Browser",
        "tag": "Resource Owner",
        "color": BLUE_AA,
        "bg": BLUE_BG,
        "lines": ["Consents via browser PKCE.", "Headless WIF skips to Step 5."],
    },
    {
        "title": "MCP Client",
        "tag": "OAuth 2.1 Client",
        "color": PURPLE_AA,
        "bg": PURPLE_BG,
        "lines": ["Host IDE or agent runtime.", "Uses PKCE/WIF; zero PATs."],
    },
    {
        "title": "MCP Server",
        "tag": "Resource Server",
        "color": GREEN_AA,
        "bg": GREEN_BG,
        "lines": ["Publishes RFC 9728 meta,", "checks aud + Write HITL."],
    },
    {
        "title": "Auth Server (IdP)",
        "tag": "Separate IdP Role",
        "color": AMBER_AA,
        "bg": AMBER_BG,
        "lines": ["Co-hosted or self-hosted.", "Issues JWT + RFC 8693 STS."],
    },
    {
        "title": "Downstream APIs",
        "tag": "External Services",
        "color": TEAL_AA,
        "bg": TEAL_BG,
        "lines": ["Receives short-lived OBO", "tokens (sub+act), user ACL."],
    },
]

# Every phase band is padded >= 7px ABOVE its first hop halo (hop.y - 25) and >= 10px BELOW its last arrow
PHASES = [
    {"id": 1, "name": "CHALLENGE", "y0": 374, "y1": 458, "color": BLUE_AA, "banner": "PHASE 1/6 · CHALLENGE (401 + WWW-Authenticate)"},
    {"id": 2, "name": "DISCOVER", "y0": 466, "y1": 590, "color": GREEN_AA, "banner": "PHASE 2/6 · DISCOVER (RFC 9728 + RFC 8414)"},
    {"id": 3, "name": "REGISTER", "y0": 598, "y1": 662, "color": PURPLE_AA, "banner": "PHASE 3/6 · REGISTER (Pre-reg > CIMD > DCR)"},
    {"id": 4, "name": "AUTHORIZE", "y0": 670, "y1": 794, "color": AMBER_AA, "banner": "PHASE 4/6 · AUTHORIZE (PKCE S256 + state + RFC 9207)"},
    {"id": 5, "name": "TOKEN", "y0": 802, "y1": 886, "color": BLUE_AA, "banner": "PHASE 5/6 · TOKEN (RFC 8707 aud-bound JWT)"},
    {"id": 6, "name": "OBO & CALL", "y0": 894, "y1": 1058, "color": TEAL_AA, "banner": "PHASE 6/6 · VERIFY + HITL + RFC 8693 OBO CALL"},
]

HOPS: List[Dict[str, Any]] = [
    # Phase 1: Challenge (y0=374, hop1=406 -> halo 381..402 strictly inside band)
    {"id": 1, "phase": 1, "src": "client", "dst": "server", "y": 406, "dashed": False, "color": BLUE_AA,
     "label": "1 · Call MCP tool (no token)", "mono": "POST /mcp"},
    {"id": 2, "phase": 1, "src": "server", "dst": "client", "y": 446, "dashed": True, "color": RED_AA,
     "label": "2 · Auth challenge", "mono": "401 + WWW-Authenticate"},
    # Phase 2: Discover (y0=466, hop3=498 -> halo 473..494 strictly inside band)
    {"id": 3, "phase": 2, "src": "client", "dst": "server", "y": 498, "dashed": False, "color": GREEN_AA,
     "label": "3 · Fetch resource meta", "mono": "GET /.well-known/oauth-protected-resource"},
    {"id": 4, "phase": 2, "src": "server", "dst": "client", "y": 538, "dashed": True, "color": GREEN_AA,
     "label": "4 · RFC 9728 response", "mono": "authorization_servers, scopes_supported"},
    {"id": 5, "phase": 2, "src": "client", "dst": "auth", "y": 578, "dashed": False, "bidir": True, "color": AMBER_AA,
     "label": "5 · Fetch auth server metadata", "mono": "RFC 8414 / OIDC (issuer, endpoints)"},
    # Phase 3: Register (y0=598, hop6=630 -> halo 605..626 strictly inside band)
    {"id": 6, "phase": 3, "src": "client", "dst": "auth", "y": 630, "dashed": False, "bidir": True, "color": PURPLE_AA,
     "label": "6 · Client ID resolution", "mono": "Pre-reg > CIMD (HTTPS) > DCR (legacy)"},
    # Phase 4: Authorize (y0=670, hop7=702 -> halo 677..698 strictly inside band)
    {"id": 7, "phase": 4, "src": "client", "dst": "user", "y": 702, "dashed": False, "color": PURPLE_AA, "min_x": 122.0,
     "label": "7 · Open auth URL", "mono": "PKCE S256 + state + resource + scope"},
    {"id": 8, "phase": 4, "src": "user", "dst": "auth", "y": 742, "dashed": False, "color": BLUE_AA,
     "label": "8 · Authenticate & grant scoped consent", "mono": ""},
    {"id": 9, "phase": 4, "src": "auth", "dst": "client", "y": 782, "dashed": True, "color": AMBER_AA,
     "label": "9 · Callback w/ mix-up check", "mono": "code + state + iss (RFC 9207)"},
    # Phase 5: Token (y0=802, hop10=834 -> halo 809..830 strictly inside band)
    {"id": 10, "phase": 5, "src": "client", "dst": "auth", "y": 834, "dashed": False, "color": BLUE_AA,
     "label": "10 · Exchange code + verifier", "mono": "POST /token + resource (RFC 8707)"},
    {"id": 11, "phase": 5, "src": "auth", "dst": "client", "y": 874, "dashed": True, "color": GREEN_AA,
     "label": "11 · Return aud-bound JWT", "mono": "aud=mcp-server, scope=mcp.read"},
    # Phase 6: Execute + Step-Up + Verify + RFC 8693 OBO (y0=894, hop12=926 -> halo 901..922 strictly inside band)
    {"id": 12, "phase": 6, "src": "client", "dst": "server", "y": 926, "dashed": False, "color": BLUE_AA,
     "label": "12 · Call tool (or 403 step-up)", "mono": "Bearer JWT / 403 insufficient_scope"},
    # Verify pill centered at y=943..971
    {"id": 13, "phase": 6, "src": "server", "dst": "auth", "y": 1006, "dashed": False, "bidir": True, "color": TEAL_AA,
     "label": "13 · RFC 8693 OBO", "mono": "urn:...:token-exchange · sub+act ≤5m"},
    {"id": 14, "phase": 6, "src": "server", "dst": "downstream", "y": 1046, "dashed": False, "color": TEAL_AA, "max_x": 1036.0,
     "label": "14 · Call downstream w/ OBO token (zero shared PAT)", "mono": "User ACL enforced"},
]

INVARIANTS = [
    {
        "num": "1",
        "title": "PKCE (S256) + RFC 9207 Mix-Up Check",
        "color": BLUE_AA,
        "bg": BLUE_BG,
        "phases": {4},
        "line1": "Mandate PKCE S256 + state + iss validation for browser/IDE apps.",
        "line2": "Headless backend agents use WIF/mTLS directly at Step 5 (/token).",
    },
    {
        "num": "2",
        "title": "Audience-Bound Tokens (RFC 8707)",
        "color": AMBER_AA,
        "bg": AMBER_BG,
        "phases": {5},
        "line1": "Include explicit resource URI on /authorize & /token. MCP server",
        "line2": "enforces aud matches its own server URI to block cross-server replay.",
    },
    {
        "num": "3",
        "title": "No Token Passthrough + RFC 8693 OBO",
        "color": TEAL_AA,
        "bg": TEAL_BG,
        "phases": {6},
        "line1": "Never forward client MCP JWTs OR share static PAT/service keys.",
        "line2": "Exchange at STS for ≤5m user-scoped OBO token (sub + act).",
    },
    {
        "num": "4",
        "title": "Least-Privilege Scopes + HITL Gate",
        "color": GREEN_AA,
        "bg": GREEN_BG,
        "phases": {2, 6},
        "line1": "Request narrow read scopes first; escalate lazily on demand via",
        "line2": "403 insufficient_scope. Require HITL approval for write mutations.",
    },
]

FRAME_SCHEDULE: List[Tuple[Optional[int], Optional[int], float, bool]] = [
    # Phase 1: Challenge (frames 0..3)
    (1, 1, 0.35, False),
    (1, 1, 0.85, False),
    (1, 2, 0.35, False),
    (1, 2, 0.85, False),
    # Phase 2: Discover (frames 4..8)
    (2, 3, 0.45, False),
    (2, 4, 0.50, False),
    (2, 5, 0.25, False),
    (2, 5, 0.60, False),
    (2, 5, 0.90, False),
    # Phase 3: Register (frames 9..11)
    (3, 6, 0.25, False),
    (3, 6, 0.55, False),
    (3, 6, 0.88, False),
    # Phase 4: Authorize (frames 12..16)
    (4, 7, 0.50, False),
    (4, 8, 0.40, False),
    (4, 8, 0.85, False),
    (4, 9, 0.45, False),
    (4, 9, 0.88, False),
    # Phase 5: Token (frames 17..20)
    (5, 10, 0.35, False),
    (5, 10, 0.85, False),
    (5, 11, 0.40, False),
    (5, 11, 0.85, False),
    # Phase 6: Execute + Verify/HITL + RFC 8693 OBO (frames 21..25)
    (6, 12, 0.55, False),
    (6, None, 0.50, True),
    (6, 13, 0.55, True),
    (6, 14, 0.40, False),
    (6, 14, 0.88, False),
    # End-to-End Summary Hold (frames 26..27, subtle pulse)
    (None, None, 0.96, True),
    (None, None, 1.0, False),
]

# Chrome-measured glyph widths for Inter 11px bold and JetBrains Mono 9.5px semibold
_MEASURED_SANS_W: Dict[str, float] = {
    "1 · Call MCP tool (no token)": 142.3,
    "2 · Auth challenge": 93.8,
    "3 · Fetch resource meta": 122.9,
    "4 · RFC 9728 response": 117.4,
    "5 · Fetch auth server metadata": 158.4,
    "6 · Client ID resolution": 116.2,
    "7 · Open auth URL": 95.4,
    "8 · Authenticate & grant scoped consent": 209.9,
    "9 · Callback w/ mix-up check": 148.6,
    "10 · Exchange code + verifier": 151.4,
    "11 · Return aud-bound JWT": 142.4,
    "12 · Call tool (or 403 step-up)": 150.4,
    "13 · RFC 8693 OBO": 99.7,
    "14 · Call downstream w/ OBO token (zero shared PAT)": 280.2,
}

_MEASURED_MONO_W: Dict[str, float] = {
    "POST /mcp": 51.5,
    "401 + WWW-Authenticate": 125.9,
    "GET /.well-known/oauth-protected-resource": 234.5,
    "authorization_servers, scopes_supported": 223.1,
    "RFC 8414 / OIDC (issuer, endpoints)": 200.2,
    "Pre-reg > CIMD (HTTPS) > DCR (legacy)": 211.7,
    "PKCE S256 + state + resource + scope": 206.0,
    "code + state + iss (RFC 9207)": 165.9,
    "POST /token + resource (RFC 8707)": 188.8,
    "aud=mcp-server, scope=mcp.read": 171.6,
    "Bearer JWT / 403 insufficient_scope": 200.2,
    "urn:...:token-exchange · sub+act ≤5m": 206.0,
    "User ACL enforced": 97.3,
}


def _sans_text_w(text: str, font_size: float = 11.0) -> float:
    if text in _MEASURED_SANS_W and abs(font_size - 11.0) < 0.1:
        return _MEASURED_SANS_W[text]
    return len(text) * font_size * 0.50 + 6.0


def _mono_pill_w(text: str, font_size: float = 9.5) -> float:
    txt_w = _MEASURED_MONO_W[text] if (text in _MEASURED_MONO_W and abs(font_size - 9.5) < 0.1) else (len(text) * font_size * 0.60)
    return txt_w + 14.0


def render_corrected_mcp_auth_svg(
    frame_idx: Optional[int] = None,
    total_frames: int = len(FRAME_SCHEDULE),
) -> str:
    """Render 1080x1350 (4:5) WCAG-AA Light-Theme SVG for static or sequential animated frame."""
    active_phase: Optional[int] = None
    active_hop: Optional[int] = None
    progress: float = 0.0
    highlight_verify: bool = False
    is_anim = frame_idx is not None
    if is_anim:
        sched = FRAME_SCHEDULE[frame_idx % len(FRAME_SCHEDULE)]
        active_phase, active_hop, progress, highlight_verify = sched

    banner_text = "14 PROTOCOL HOPS · ZERO TOKEN PASSTHROUGH"
    banner_color = "#1E3A5F"
    if active_phase is not None:
        ph = next(p for p in PHASES if p["id"] == active_phase)
        banner_text = ph["banner"]
        banner_color = ph["color"]
    elif is_anim:
        banner_text = "END-TO-END ZERO-TRUST · OAUTH 2.1 + RFC 8693 OBO"
        banner_color = GREEN_AA

    out: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        "<defs>",
        '  <filter id="cardShadow" x="-4%" y="-4%" width="108%" height="112%">',
        '    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.05"/>',
        "  </filter>",
        '  <filter id="glowActive" x="-20%" y="-20%" width="140%" height="140%">',
        '    <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#1D4ED8" flood-opacity="0.28"/>',
        "  </filter>",
    ]

    marker_colors = {
        "blue": BLUE_AA,
        "green": GREEN_AA,
        "purple": PURPLE_AA,
        "amber": AMBER_AA,
        "red": RED_AA,
        "teal": TEAL_AA,
        "slate": SLATE,
    }
    for name, hx in marker_colors.items():
        out.append(
            f'  <marker id="arr-{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="{hx}"/></marker>'
        )
    out.append("</defs>")

    # ── Canvas Backdrop (Executive Light Theme #F8FAFC) ────────────────────
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<rect x="0" y="0" width="270" height="5" fill="{BLUE_AA}"/>')
    out.append(f'<rect x="270" y="0" width="270" height="5" fill="{GREEN_AA}"/>')
    out.append(f'<rect x="540" y="0" width="270" height="5" fill="{AMBER_AA}"/>')
    out.append(f'<rect x="810" y="0" width="270" height="5" fill="{TEAL_AA}"/>')

    # ── Top Header Card (y=5..112) ─────────────────────────────────────────
    out.append(f'<rect x="0" y="5" width="{W}" height="107" fill="{WHITE}"/>')
    out.append(f'<line x1="0" y1="112" x2="{W}" y2="112" stroke="{BORDER_LIGHT}" stroke-width="1.5"/>')

    # Eyebrow badges (public-facing, zero internal prompt meta-words)
    out.append(f'<rect x="28" y="18" width="292" height="22" rx="11" fill="{BLUE_BG}" stroke="#BFDBFE" stroke-width="1"/>')
    out.append(
        f'<text x="174" y="33" text-anchor="middle" font-family="{FONT}" font-size="10.5" '
        f'font-weight="700" letter-spacing="0.4" fill="{BLUE_AA}">MCP AUTHORIZATION SPEC · OAUTH 2.1</text>'
    )
    out.append(f'<rect x="758" y="18" width="294" height="22" rx="11" fill="{TEAL_BG}" stroke="#99F6E4" stroke-width="1"/>')
    out.append(
        f'<text x="905" y="33" text-anchor="middle" font-family="{FONT}" font-size="10.5" '
        f'font-weight="700" letter-spacing="0.4" fill="{TEAL_AA}">RFC 9728 · RFC 8707 · RFC 9207 · RFC 8693 OBO</text>'
    )

    out.append(
        f'<text x="28" y="74" font-family="{FONT}" font-size="27" font-weight="800" fill="{INK}" '
        f'letter-spacing="-0.4">How MCP Authorization Works (Production Architecture)</text>'
    )
    out.append(
        f'<text x="28" y="98" font-family="{FONT}" font-size="13.2" font-weight="500" fill="{SLATE}">'
        f'End-to-end OAuth 2.1, RFC 9728/8414 discovery, PKCE + audience binding &amp; RFC 8693 OBO delegation</text>'
    )

    # ── Zone 1: WHO'S INVOLVED (y=122..270) ───────────────────────────────
    out.append(f'<rect x="28" y="122" width="1024" height="28" rx="7" fill="{NAVY}"/>')
    out.append(
        f'<text x="42" y="140" font-family="{FONT}" font-size="11.5" font-weight="800" '
        f'letter-spacing="0.7" fill="{WHITE}">1 · WHO&#39;S INVOLVED — 5 ROLES &amp; TRUST BOUNDARIES</text>'
    )
    out.append(
        f'<text x="1038" y="140" text-anchor="end" font-family="{FONT}" font-size="11" font-weight="600" '
        f'fill="#93C5FD">Browser PKCE (Interactive) or WIF (Headless -&gt; Step 5)</text>'
    )

    card_w = 195
    card_gap = 12.25
    for idx, card in enumerate(WHO_CARDS):
        cx = 28 + idx * (card_w + card_gap)
        cy = 158
        ch = 110
        out.append(
            f'<rect x="{cx:.1f}" y="{cy}" width="{card_w}" height="{ch}" rx="10" fill="{WHITE}" '
            f'stroke="{BORDER}" stroke-width="1.2" filter="url(#cardShadow)"/>'
        )
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{card_w}" height="5" rx="3" fill="{card["color"]}"/>')
        out.append(
            f'<rect x="{cx + 10:.1f}" y="{cy + 14}" width="{card_w - 20}" height="20" rx="5" fill="{card["bg"]}"/>'
        )
        out.append(
            f'<text x="{cx + card_w / 2:.1f}" y="{cy + 28}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="10.5" font-weight="700" fill="{card["color"]}">{_esc(card["tag"])}</text>'
        )
        out.append(
            f'<text x="{cx + card_w / 2:.1f}" y="{cy + 52}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="13.5" font-weight="800" fill="{INK}">{_esc(card["title"])}</text>'
        )
        out.append(
            f'<text x="{cx + card_w / 2:.1f}" y="{cy + 74}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11.5" font-weight="500" fill="{SLATE}">{_esc(card["lines"][0])}</text>'
        )
        out.append(
            f'<text x="{cx + card_w / 2:.1f}" y="{cy + 91}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11.5" font-weight="500" fill="{SLATE}">{_esc(card["lines"][1])}</text>'
        )

    # ── Zone 2: THE FLOW, STEP BY STEP (y=280..1070) ───────────────────────
    out.append(
        f'<rect x="28" y="280" width="1024" height="790" rx="12" fill="{WHITE}" '
        f'stroke="{BORDER}" stroke-width="1.3" filter="url(#cardShadow)"/>'
    )
    out.append(f'<rect x="28" y="280" width="1024" height="32" rx="10" fill="{NAVY}"/>')
    out.append(f'<rect x="28" y="300" width="1024" height="12" fill="{NAVY}"/>')
    out.append(
        f'<text x="42" y="300" font-family="{FONT}" font-size="11.5" font-weight="800" '
        f'letter-spacing="0.7" fill="{WHITE}">2 · THE FLOW, STEP BY STEP — RFC-COMPLIANT SEQUENCE</text>'
    )
    out.append(
        f'<rect x="646" y="285" width="394" height="22" rx="11" fill="{banner_color}" '
        f'stroke="rgba(255,255,255,0.32)" stroke-width="1"/>'
    )
    out.append(
        f'<text x="843" y="300" text-anchor="middle" font-family="{FONT}" font-size="10.5" '
        f'font-weight="700" letter-spacing="0.4" fill="{WHITE}">{_esc(banner_text)}</text>'
    )

    # Phase subtle horizontal bands + left step badges (strictly containing every hop halo + arrow!)
    for ph in PHASES:
        is_ph_active = active_phase == ph["id"]
        band_fill = "#F8FAFC" if ph["id"] % 2 == 1 else "#FFFFFF"
        band_stroke = "none"
        band_sw = "0"
        if is_ph_active:
            band_fill = BLUE_BG if ph["color"] == BLUE_AA else (
                GREEN_BG if ph["color"] == GREEN_AA else (
                    PURPLE_BG if ph["color"] == PURPLE_AA else (
                        AMBER_BG if ph["color"] == AMBER_AA else TEAL_BG
                    )
                )
            )
            band_stroke = ph["color"]
            band_sw = "1.6"
        out.append(
            f'<rect class="phase-band" data-phase="{ph["id"]}" x="34" y="{ph["y0"]}" width="1012" height="{ph["y1"] - ph["y0"]}" rx="8" '
            f'fill="{band_fill}" stroke="{band_stroke}" stroke-width="{band_sw}" '
            f'opacity="{"0.88" if is_ph_active else "0.58"}"/>'
        )
        py_mid = (ph["y0"] + ph["y1"]) / 2
        pill_fill = ph["color"] if (is_ph_active or not is_anim) else "#E2E8F0"
        pill_txt = WHITE if (is_ph_active or not is_anim) else "#334155"
        out.append(
            f'<rect x="38" y="{py_mid - 19:.1f}" width="66" height="38" rx="7" fill="{pill_fill}" '
            f'{"filter=\"url(#glowActive)\"" if is_ph_active else ""}/>'
        )
        out.append(
            f'<text x="71" y="{py_mid - 3:.1f}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="9.5" font-weight="800" fill="{pill_txt}">STEP {ph["id"]}</text>'
        )
        out.append(
            f'<text x="71" y="{py_mid + 11:.1f}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="9" font-weight="700" fill="{pill_txt}">{_esc(ph["name"])}</text>'
        )

    # 5 Lifeline Header Boxes (y=322..362) & Vertical Dashed Lines (y=362..1058)
    for lane in LANES:
        lx = lane["x"]
        out.append(
            f'<line x1="{lx}" y1="362" x2="{lx}" y2="1058" stroke="#CBD5E1" '
            f'stroke-width="1.6" stroke-dasharray="5,5"/>'
        )
        out.append(
            f'<rect x="{lx - 78}" y="322" width="156" height="40" rx="8" fill="{lane["bg"]}" '
            f'stroke="{lane["color"]}" stroke-width="1.5"/>'
        )
        out.append(
            f'<text x="{lx}" y="339" text-anchor="middle" font-family="{FONT}" font-size="12.5" '
            f'font-weight="800" fill="{INK}">{_esc(lane["title"])}</text>'
        )
        out.append(
            f'<text x="{lx}" y="355" text-anchor="middle" font-family="{FONT}" font-size="10" '
            f'font-weight="600" fill="{lane["color"]}">{_esc(lane["sub"])}</text>'
        )

    # Registration guidance caption strictly inside Phase 3 band (y=653 <= y1=662)
    out.append(
        f'<text x="540" y="653" text-anchor="middle" font-family="{FONT}" font-size="10.5" font-weight="500" fill="{SLATE}">'
        f'Prefer pre-registered client_id or HTTPS Client ID Metadata Documents (CIMD); use DCR only as legacy fallback.</text>'
    )

    color_to_marker = {
        BLUE_AA: "blue",
        GREEN_AA: "green",
        PURPLE_AA: "purple",
        AMBER_AA: "amber",
        RED_AA: "red",
        TEAL_AA: "teal",
        SLATE: "slate",
    }

    for hop in HOPS:
        sx = LANE_X[hop["src"]]
        dx = LANE_X[hop["dst"]]
        y = hop["y"]
        col = hop["color"]
        m_name = color_to_marker.get(col, "slate")

        is_hop_active = active_hop == hop["id"]
        is_hop_dim = is_anim and (active_phase is not None) and (hop["phase"] != active_phase)
        sw = 2.8 if is_hop_active else 1.8
        op = "0.60" if is_hop_dim else "1.0"
        dash_attr = ' stroke-dasharray="6,4"' if hop["dashed"] else ""
        start_attr = f' marker-start="url(#arr-{m_name})"' if hop.get("bidir") else ""

        x_start = sx + (6 if dx > sx else -6)
        x_end = dx - (6 if dx > sx else -6)

        out.append(f'<g opacity="{op}">')
        out.append(
            f'<line x1="{x_start}" y1="{y}" x2="{x_end}" y2="{y}" stroke="{col}" '
            f'stroke-width="{sw}"{dash_attr}{start_attr} marker-end="url(#arr-{m_name})"/>'
        )

        mid_x = (sx + dx) / 2
        sans_txt = hop["label"]
        mono_txt = hop["mono"]

        sans_w = _sans_text_w(sans_txt, 11.0)
        mono_w = _mono_pill_w(mono_txt, 9.5) if mono_txt else 0.0
        pad_x = 8.0
        gap_between = 8.0 if mono_txt else 0.0
        total_pill_w = round(pad_x + sans_w + gap_between + mono_w + pad_x, 1)

        min_x = float(hop.get("min_x", 112.0))
        max_x = float(hop.get("max_x", 1038.0))
        left_edge = round(max(min_x, min(max_x - total_pill_w, mid_x - total_pill_w / 2)), 1)

        halo_stroke = col if is_hop_active else "#E2E8F0"
        halo_sw = "1.6" if is_hop_active else "1.0"
        out.append(
            f'<rect class="hop-halo" data-hop="{hop["id"]}" data-phase="{hop["phase"]}" '
            f'x="{left_edge:.1f}" y="{y - 25}" width="{total_pill_w:.1f}" height="21" '
            f'rx="5" fill="{WHITE}" stroke="{halo_stroke}" stroke-width="{halo_sw}"/>'
        )
        out.append(
            f'<text class="hop-sans" data-hop="{hop["id"]}" x="{left_edge + pad_x:.1f}" y="{y - 10.8}" font-family="{FONT}" font-size="11" '
            f'font-weight="700" fill="{INK}">{_esc(sans_txt)}</text>'
        )
        if mono_txt:
            mx = round(left_edge + pad_x + sans_w + gap_between, 1)
            out.append(
                f'<rect class="hop-mono-box" data-hop="{hop["id"]}" x="{mx:.1f}" y="{y - 22}" width="{mono_w:.1f}" height="15" rx="4" '
                f'fill="#F1F5F9" stroke="#CBD5E1" stroke-width="0.8"/>'
            )
            out.append(
                f'<text class="hop-mono-txt" data-hop="{hop["id"]}" x="{mx + mono_w / 2:.1f}" y="{y - 11.2}" text-anchor="middle" font-family="{MONO}" '
                f'font-size="9.5" font-weight="600" fill="#1E293B">{_esc(mono_txt)}</text>'
            )
        out.append("</g>")

        if is_hop_active:
            px = x_start + (x_end - x_start) * progress
            out.append(
                f'<circle cx="{px:.1f}" cy="{y}" r="8.5" fill="{col}" opacity="0.22"/>'
                f'<circle cx="{px:.1f}" cy="{y}" r="4.8" fill="{WHITE}" stroke="{col}" stroke-width="2.5"/>'
            )

    # Inline Policy Verification & Write=HITL Pill centered on MCP Server lane (y=943..971)
    v_op = "0.60" if (is_anim and active_phase not in (None, 6)) else "1.0"
    v_fill = GREEN_AA if highlight_verify else GREEN_BG
    v_txt = WHITE if highlight_verify else "#065F46"
    v_stroke = GREEN_AA
    out.append(f'<g opacity="{v_op}">')
    out.append(
        f'<rect x="364" y="943" width="352" height="28" rx="14" fill="{v_fill}" '
        f'stroke="{v_stroke}" stroke-width="{"2.2" if highlight_verify else "1.5"}" '
        f'{"filter=\"url(#glowActive)\"" if highlight_verify else ""}/>'
    )
    out.append(
        f'<text x="540" y="961" text-anchor="middle" font-family="{FONT}" font-size="11.5" '
        f'font-weight="800" fill="{v_txt}">✓ Verify sig, aud &amp; scope · Read=Auto / Write=HITL Approval</text>'
    )
    out.append("</g>")

    # ── Zone 3: 4 PRODUCTION SECURITY INVARIANTS (y=1078..1286) ────────────
    out.append(f'<rect x="28" y="1078" width="1024" height="28" rx="7" fill="{NAVY}"/>')
    out.append(
        f'<text x="42" y="1096" font-family="{FONT}" font-size="11.5" font-weight="800" '
        f'letter-spacing="0.7" fill="{WHITE}">3 · PRODUCTION SECURITY INVARIANTS BAKED IN</text>'
    )
    out.append(
        f'<text x="1038" y="1096" text-anchor="end" font-family="{FONT}" font-size="11" font-weight="600" '
        f'fill="#6EE7B7">Stops Token Replay, Redirect Mix-Up &amp; Confused-Deputy</text>'
    )

    for idx, inv in enumerate(INVARIANTS):
        col_idx = idx % 2
        row_idx = idx // 2
        ix = 28 + col_idx * 518
        iy = 1114 + row_idx * 86
        iw = 506
        ih = 78

        is_inv_hi = (is_anim and active_phase in inv["phases"]) or (is_anim and active_phase is None)
        stroke_c = inv["color"] if is_inv_hi else BORDER
        stroke_w = "2.2" if is_inv_hi else "1.2"
        out.append(
            f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="10" fill="{WHITE}" '
            f'stroke="{stroke_c}" stroke-width="{stroke_w}" filter="url(#cardShadow)"/>'
        )
        out.append(f'<rect x="{ix}" y="{iy}" width="7" height="{ih}" rx="3" fill="{inv["color"]}"/>')
        out.append(
            f'<circle cx="{ix + 28}" cy="{iy + 24}" r="12" fill="{inv["bg"]}" stroke="{inv["color"]}" stroke-width="1.3"/>'
        )
        out.append(
            f'<text x="{ix + 28}" y="{iy + 28}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="11.5" font-weight="800" fill="{inv["color"]}">{inv["num"]}</text>'
        )
        out.append(
            f'<text x="{ix + 48}" y="{iy + 28}" font-family="{FONT}" font-size="13.5" '
            f'font-weight="800" fill="{INK}">{_esc(inv["title"])}</text>'
        )
        out.append(
            f'<text x="{ix + 20}" y="{iy + 49}" font-family="{FONT}" font-size="11.5" '
            f'font-weight="500" fill="{SLATE}">{_esc(inv["line1"])}</text>'
        )
        out.append(
            f'<text x="{ix + 20}" y="{iy + 65}" font-family="{FONT}" font-size="11.5" '
            f'font-weight="500" fill="{SLATE}">{_esc(inv["line2"])}</text>'
        )

    # ── Footer Attribution Bar (y=1296..1334) ──────────────────────────────
    out.append(f'<rect x="28" y="1296" width="1024" height="38" rx="9" fill="{NAVY}"/>')
    out.append(
        f'<text x="44" y="1319" font-family="{FONT}" font-size="11" font-weight="700" '
        f'fill="#93C5FD">REFERENCE GATEWAY: github.com/nitinaggarwal-12/ideas-mining (Zero-Bloat RFC 8693 OBO)</text>'
    )
    out.append(
        f'<text x="1036" y="1319" text-anchor="end" font-family="{FONT}" font-size="11" font-weight="700" '
        f'fill="{WHITE}">Nitin Aggarwal · AI Systems &amp; Cloud Architecture · 2026</text>'
    )

    out.append("</svg>")
    return "\n".join(out)


def render_corrected_mcp_auth_drawio() -> str:
    """Render 100% native editable Draw.io XML (<mxfile>) matching the 1080x1350 layout."""
    mxfile = ET.Element("mxfile", host="app.diagrams.net", agent="MCP-Auth-Production/2.1", version="24.7.0")
    diagram = ET.SubElement(mxfile, "diagram", id="mcp-auth-production-obo", name="MCP Auth (Zero-Trust + RFC 8693 OBO)")
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        dx="1200",
        dy="1400",
        grid="1",
        gridSize="10",
        guides="1",
        tooltips="1",
        connect="1",
        arrows="1",
        fold="1",
        page="1",
        pageScale="1",
        pageWidth=str(W),
        pageHeight=str(H),
        background=BG,
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    def add_box(cid: str, x: float, y: float, w: float, h: float, value: str, style: str) -> None:
        cell = ET.SubElement(root, "mxCell", id=cid, value=value, style=style, vertex="1", parent="1")
        ET.SubElement(
            cell,
            "mxGeometry",
            x=str(round(x, 1)),
            y=str(round(y, 1)),
            width=str(round(w, 1)),
            height=str(round(h, 1)),
            **{"as": "geometry"},
        )

    def add_edge(cid: str, x1: float, y1: float, x2: float, y2: float, value: str, color: str, dashed: bool = False, bidir: bool = False) -> None:
        dash_s = "dashed=1;dashPattern=6 4;" if dashed else ""
        start_s = "startArrow=classic;startFill=1;" if bidir else ""
        style = (
            f"{start_s}endArrow=classic;endFill=1;strokeColor={color};strokeWidth=2;{dash_s}"
            "rounded=0;labelBackgroundColor=#FFFFFF;fontColor=#0F172A;fontSize=11;fontStyle=1;"
        )
        cell = ET.SubElement(root, "mxCell", id=cid, value=value, style=style, edge="1", parent="1")
        geom = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(x1), y=str(y1), **{"as": "sourcePoint"})
        ET.SubElement(geom, "mxPoint", x=str(x2), y=str(y2), **{"as": "targetPoint"})
        ET.SubElement(geom, "mxPoint", x="0", y="-13", **{"as": "offset"})

    add_box(
        "hdr",
        28,
        14,
        1024,
        92,
        "<b>How MCP Authorization Works (Production Architecture)</b><br/>"
        "<font style=\'font-size:12px\'>End-to-end OAuth 2.1, RFC 9728/8414 discovery, PKCE + audience binding &amp; RFC 8693 OBO delegation</font>",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={BORDER};fontColor={INK};fontSize=20;align=center;verticalAlign=middle;",
    )
    add_box(
        "z1-hdr",
        28,
        122,
        1024,
        28,
        "1 · WHO\'S INVOLVED — 5 ROLES & TRUST BOUNDARIES",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={NAVY};strokeColor={NAVY};fontColor={WHITE};fontSize=12;fontStyle=1;align=left;spacingLeft=14;",
    )
    for idx, card in enumerate(WHO_CARDS):
        cx = 28 + idx * (195 + 12.25)
        add_box(
            f"who-{idx}",
            cx,
            158,
            195,
            110,
            f"<font color=\'{card['color']}\'><b>{card['tag']}</b></font><br/>"
            f"<b>{card['title']}</b><br/>{card['lines'][0]} {card['lines'][1]}",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={card['color']};strokeWidth=1.5;fontColor={INK};fontSize=11;align=center;",
        )

    add_box(
        "z2-hdr",
        28,
        280,
        1024,
        32,
        "2 · THE FLOW, STEP BY STEP — RFC-COMPLIANT SEQUENCE (RFC 9728 / 8414 / 8707 / 9207 / 8693)",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={NAVY};strokeColor={NAVY};fontColor={WHITE};fontSize=12;fontStyle=1;align=left;spacingLeft=14;",
    )
    for lane in LANES:
        lx = lane["x"]
        add_box(
            f"lane-{lane['id']}",
            lx - 78,
            322,
            156,
            40,
            f"<b>{lane['title']}</b><br/><font style=\'font-size:10px\'>{lane['sub']}</font>",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={lane['bg']};strokeColor={lane['color']};strokeWidth=1.5;fontColor={INK};fontSize=12;",
        )
        ll = ET.SubElement(
            root,
            "mxCell",
            id=f"ll-{lane['id']}",
            value="",
            style="endArrow=none;dashed=1;dashPattern=5 5;strokeColor=#CBD5E1;strokeWidth=1.5;",
            edge="1",
            parent="1",
        )
        geom = ET.SubElement(ll, "mxGeometry", relative="1", **{"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(lx), y="362", **{"as": "sourcePoint"})
        ET.SubElement(geom, "mxPoint", x=str(lx), y="1058", **{"as": "targetPoint"})

    for hop in HOPS:
        sx = LANE_X[hop["src"]]
        dx = LANE_X[hop["dst"]]
        lbl = hop["label"] + (f" [{hop['mono']}]" if hop["mono"] else "")
        add_edge(f"hop-{hop['id']}", sx, hop["y"], dx, hop["y"], lbl, hop["color"], hop["dashed"], bool(hop.get("bidir")))

    add_box(
        "verify-pill",
        364,
        943,
        352,
        28,
        "✓ Verify sig, aud & scope · Read=Auto / Write=HITL Approval",
        f"rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor={GREEN_BG};strokeColor={GREEN_AA};strokeWidth=1.5;fontColor=#065F46;fontSize=11;fontStyle=1;",
    )
    add_box(
        "z3-hdr",
        28,
        1078,
        1024,
        28,
        "3 · PRODUCTION SECURITY INVARIANTS BAKED IN",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={NAVY};strokeColor={NAVY};fontColor={WHITE};fontSize=12;fontStyle=1;align=left;spacingLeft=14;",
    )
    for idx, inv in enumerate(INVARIANTS):
        ix = 28 + (idx % 2) * 518
        iy = 1114 + (idx // 2) * 86
        add_box(
            f"inv-{inv['num']}",
            ix,
            iy,
            506,
            78,
            f"<b>{inv['num']} · {inv['title']}</b><br/>{inv['line1']} {inv['line2']}",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={WHITE};strokeColor={inv['color']};strokeWidth=1.5;fontColor={INK};fontSize=11;align=left;spacingLeft=12;",
        )

    add_box(
        "ftr",
        28,
        1296,
        1024,
        38,
        "REFERENCE GATEWAY: github.com/nitinaggarwal-12/ideas-mining (Zero-Bloat RFC 8693 OBO)  |  Nitin Aggarwal · 2026",
        f"rounded=1;whiteSpace=wrap;html=1;fillColor={NAVY};strokeColor={NAVY};fontColor={WHITE};fontSize=11;fontStyle=1;",
    )

    return ET.tostring(mxfile, encoding="unicode")


LINKEDIN_POST_DRAFT = """Your AI agent can call GitHub, Gmail, and Jira. Without OAuth 2.1 audience binding and On-Behalf-Of delegation, one leaked tool call compromises every downstream API.

Here is the production MCP authorization flow, cleanly updated for real-world enterprise deployments:

1. Challenge (401 + WWW-Authenticate)
Calling POST /mcp without a bearer token triggers a standard HTTP 401 challenge pointing to resource metadata.

2. Discover (RFC 9728 + RFC 8414)
The client fetches GET /.well-known/oauth-protected-resource (RFC 9728) to discover authorization_servers and scopes_supported, then resolves the IdP via RFC 8414 / OIDC discovery (issuer, endpoints, JWKS).

3. Client Registration (Pre-reg > CIMD > DCR)
Use pre-registered client_id or HTTPS Client ID Metadata Documents (CIMD) first; reserve Dynamic Client Registration (DCR) for legacy fallback.

4. Authorize (PKCE S256 + state + RFC 9207 iss)
Interactive desktop/IDE hosts run OAuth 2.1 with mandatory PKCE S256 and state; headless Cloud Run / backend agents use Workload Identity Federation (WIF) directly at Step 5 (/token). Callback validation checks both state and iss (RFC 9207) against RFC 8414 metadata to stop IdP mix-up attacks.

5. Audience-Bound Token (RFC 8707)
The client passes explicit resource= on /authorize and /token. The MCP server enforces aud matches its own server URI so sibling servers cannot replay tokens.

6. Execute, Step-Up (403) & RFC 8693 On-Behalf-Of (OBO)
Two rules keep downstream APIs safe from Confused-Deputy leaks:
→ Never forward the client MCP token downstream, AND never store a single shared static PAT / service key.
→ Exchange the MCP JWT via RFC 8693 Token Exchange (grant_type=urn:ietf:params:oauth:grant-type:token-exchange) for a short-lived (<=5m), narrow-scope API token carrying both sub (user) and act (MCP server), while gating mutating tool writes behind Human-in-the-Loop (HITL) approval.

Reference Google Cloud ADK + Zero-Bloat MCP Gateway implementation (Dynamic Tool Search + RFC 8693 OBO + Read=Auto / Write=HITL):
https://github.com/nitinaggarwal-12/ideas-mining/tree/main/generated-repos/gcp-mcp-zero-bloat-gateway

Which enterprise constraint breaks first in your MCP rollouts: Dynamic Client Registration (DCR) governance or RFC 8693 OBO delegation to legacy APIs?

@Google Cloud @Anthropic @Model Context Protocol
#MCP #ModelContextProtocol #OAuth2 #ZeroTrust #AgenticAI #AISecurity #CloudArchitecture #GoogleCloud #ADK
"""

CORRECTION_CHANGELOG_MD = """# Corrected MCP Authorization Package — Exact Fixes vs. Original Post & Pass-1 Critique

Source audited: Jean Lee (`jeanklee`), *"How MCP Authorization Works"*, LinkedIn `activity-7526630995425644545-x4Sk` (`1080×1350` `GIF89a`, `180` frames, `6.00s`, `2026-11-12T13:04:27Z`).

## 1. Visual Copy, Typo & Spacing Fixes (6/6 Resolved)
| Zone | Original Bug in GIF | Fixed in Production Version |
|---|---|---|
| Zone 1 (`Auth Server`) | `Separate role (can be-hosted)` | `Co-hosted or self-hosted` (`Separate IdP Role`) |
| Zone 2 (Step 2 / Hop 2) | `401 + www-Authenticate` | `401 + WWW-Authenticate` |
| Zone 2 (Step 3 / Hop 3) | `GET /.well-know/oauth-protected-resource` | `GET /.well-known/oauth-protected-resource` |
| Zone 2 (Step 5 / Hop 5) | `Fetch auth server Metadata IRFC 8414 / OIDC)` | `Fetch auth server metadata` `<->` `RFC 8414 / OIDC (issuer, endpoints)` |
| Zone 2 (Step 9 / Hop 9) | `scopped` | `scoped consent` |
| Zone 2 (Step 10 / Hop 10) | `resourse (RFC 8707)` | `resource (RFC 8707)` |
| Monospace Pills | Cramped punctuation (`scopes_supported.authorization_servers`, `PKCES256`) | Chrome-measured symmetric `8px` padded rounded monospace pills |

## 2. Adversarial Design & Protocol Fixes (Pass-2 Polish)
1. **Band Spotlight Containment (`5/6` fixed -> `0` border collisions)**: Shifted all Phase bands (`y0..y1`) so every hop halo (`y - 25 .. y - 4`) sits `>= 7px` inside its band top and `>= 12px` above its band bottom.
2. **Lifeline Alignment (`Hop 7` & `Hop 13`)**: Clamped `Hop 7` inside `[122..]` (zero bleed past User lifeline `x=120`) and tightened `Hop 13` (`13 · RFC 8693 OBO` `<->` `urn:...:token-exchange · sub+act ≤5m`), ending well before `Downstream APIs`.
3. **Strict Terminology & Protocol Precision**: Unified `Downstream APIs` (`External Services`); stripped meta-word `CORRECTED` from eyebrow pill; fixed subtitle comma (`OAuth 2.1, RFC 9728/8414 discovery, PKCE + audience binding`); replaced `grant_type=token-exchange` invalid literal with `urn:...:token-exchange · sub+act ≤5m` (full URN in post); added `state` to `Hop 7`; made `Hop 5` `<->` returning issuer metadata; clarified headless WIF skips Steps 7–9 directly to Step 5.
4. **WCAG 2.2 AA Contrast (`>= 4.5:1`)**: Darkened Amber (`#D97706 -> #B45309`), Emerald (`#059669 -> #047857`), and Teal (`#0D9488 -> #0F766E`) across all badges, subtitles, and step boxes.
"""


def build_corrected_mcp_authorization_bundle(
    out_dir: Optional[Path] = None,
    fps: float = 4.5,
) -> Dict[str, Any]:
    """Build SVG, 1x PNG, @2x PNG, sequential GIF89a, Draw.io XML, and Markdown drafts."""
    dest = out_dir or OUT_DIR
    dest.mkdir(parents=True, exist_ok=True)

    chrome = resolve_chrome_bin()
    ffmpeg = resolve_ffmpeg_bin()
    if not chrome:
        raise RuntimeError("Google Chrome binary not found for deterministic SVG rasterization")
    if not ffmpeg:
        raise RuntimeError("FFmpeg binary not found for palettegen GIF89a encoding")

    static_svg_path = dest / "mcp_authorization_corrected_4x5.svg"
    static_svg_text = render_corrected_mcp_auth_svg(frame_idx=None)
    static_svg_path.write_text(static_svg_text, encoding="utf-8")

    drawio_path = dest / "mcp_authorization_corrected_4x5.drawio"
    drawio_xml = render_corrected_mcp_auth_drawio()
    ET.fromstring(drawio_xml)
    drawio_path.write_text(drawio_xml, encoding="utf-8")

    post_md_path = dest / "linkedin_post_draft.md"
    post_md_path.write_text(LINKEDIN_POST_DRAFT, encoding="utf-8")
    changelog_path = dest / "correction_changelog.md"
    changelog_path.write_text(CORRECTION_CHANGELOG_MD, encoding="utf-8")

    png_1x_path = dest / "mcp_authorization_corrected_4x5.png"
    png_2x_path = dest / "mcp_authorization_corrected_4x5_2x.png"
    gif_path = dest / "mcp_authorization_corrected_4x5.gif"
    audit_path = dest / "dom_collision_audit.json"

    puppeteer_mod = Path("/usr/local/google/home/nitinagga/node_modules/puppeteer-core")
    if not puppeteer_mod.exists():
        puppeteer_mod = Path("/usr/local/google/home/nitinagga/node_modules/puppeteer")
    if not puppeteer_mod.exists():
        raise RuntimeError(f"puppeteer not found at {puppeteer_mod}")

    frames_spec = [{"name": "static", "svg": static_svg_text}]
    for i in range(len(FRAME_SCHEDULE)):
        frames_spec.append({"name": f"frame_{i:03d}", "svg": render_corrected_mcp_auth_svg(frame_idx=i)})

    with tempfile.TemporaryDirectory(prefix="mcp_auth_gif_") as tmp:
        tmp_dir = Path(tmp)
        spec_json = tmp_dir / "frames_spec.json"
        spec_json.write_text(json.dumps(frames_spec), encoding="utf-8")

        runner_js = tmp_dir / "render_all.mjs"
        runner_js.write_text(
            f"""
import fs from 'fs';
import path from 'path';
import {{ createRequire }} from 'module';
const require = createRequire(import.meta.url);
const puppeteer = require({json.dumps(str(puppeteer_mod))});

const frames = JSON.parse(fs.readFileSync({json.dumps(str(spec_json))}, 'utf-8'));
const tmpDir = {json.dumps(str(tmp_dir))};
const browser = await puppeteer.launch({{
  executablePath: {json.dumps(str(chrome))},
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
}});
try {{
  const page = await browser.newPage();
  await page.setViewport({{ width: {W}, height: {H}, deviceScaleFactor: 1 }});

  let staticAudit = null;
  for (let i = 0; i < frames.length; i++) {{
    const f = frames[i];
    const html = `<!doctype html><html><body style="margin:0;padding:0;background:#F8FAFC;overflow:hidden;">${{f.svg}}</body></html>`;
    await page.setContent(html, {{ waitUntil: 'load' }});
    if (f.name === 'static') {{
      staticAudit = await page.evaluate(() => {{
        const svg = document.querySelector('svg');
        const svgRect = svg.getBoundingClientRect();
        const texts = Array.from(svg.querySelectorAll('text')).map((el, idx) => {{
          const r = el.getBoundingClientRect();
          return {{
            idx,
            text: (el.textContent || '').trim(),
            left: r.left,
            top: r.top,
            right: r.right,
            bottom: r.bottom,
            width: r.width,
            height: r.height,
          }};
        }});
        const oob = texts.filter(t => t.left < 0 || t.top < 0 || t.right > 1080.5 || t.bottom > 1350.5);
        const overlaps = [];
        for (let a = 0; a < texts.length; a++) {{
          for (let b = a + 1; b < texts.length; b++) {{
            const t1 = texts[a], t2 = texts[b];
            const ix = Math.max(0, Math.min(t1.right, t2.right) - Math.max(t1.left, t2.left));
            const iy = Math.max(0, Math.min(t1.bottom, t2.bottom) - Math.max(t1.top, t2.top));
            if (ix > 1.5 && iy > 1.5) {{
              overlaps.push({{ a: t1.text, b: t2.text, ix, iy }});
            }}
          }}
        }}
        const pillViolations = [];
        const bandViolations = [];
        for (const h of svg.querySelectorAll('.hop-halo')) {{
          const hid = h.getAttribute('data-hop');
          const pid = h.getAttribute('data-phase');
          const hr = h.getBoundingClientRect();
          const band = svg.querySelector(`.phase-band[data-phase="${{pid}}"]`);
          if (band) {{
            const br = band.getBoundingClientRect();
            if (hr.top < br.top + 5 || hr.bottom > br.bottom - 5) {{
              bandViolations.push({{ hid, pid, haloTop: hr.top, haloBottom: hr.bottom, bandTop: br.top, bandBottom: br.bottom }});
            }}
          }}
          const sansEl = svg.querySelector(`.hop-sans[data-hop="${{hid}}"]`);
          if (sansEl) {{
            const sr = sansEl.getBoundingClientRect();
            if (sr.left < hr.left + 4 || sr.right > hr.right - 4) {{
              pillViolations.push({{ hid, kind: 'sans_outside_halo', sr, hr }});
            }}
          }}
          const mb = svg.querySelector(`.hop-mono-box[data-hop="${{hid}}"]`);
          const mt = svg.querySelector(`.hop-mono-txt[data-hop="${{hid}}"]`);
          if (mb && mt) {{
            const mbr = mb.getBoundingClientRect();
            const mtr = mt.getBoundingClientRect();
            if (mtr.left < mbr.left + 3 || mtr.right > mbr.right - 3 || mbr.right > hr.right - 4) {{
              pillViolations.push({{ hid, kind: 'mono_outside_pill', mtr, mbr, hr }});
            }}
          }}
        }}
        const fullTxt = texts.map(t => t.text).join(' ');
        const badTokens = ['scopped', 'be-hosted', 'www-Authenticate', 'well-know/', 'IRFC', 'resourse', 'CORRECTED ZERO-TRUST'];
        const foundTypos = badTokens.filter(tok => fullTxt.includes(tok));
        return {{
          width: svgRect.width,
          height: svgRect.height,
          textCount: texts.length,
          outOfBoundsCount: oob.length,
          oob,
          overlapCount: overlaps.length,
          overlaps,
          pillViolationCount: pillViolations.length,
          pillViolations,
          bandViolationCount: bandViolations.length,
          bandViolations,
          foundTypos,
        }};
      }});
      await page.screenshot({{ path: {json.dumps(str(png_1x_path))}, clip: {{ x: 0, y: 0, width: {W}, height: {H} }} }});
    }} else {{
      const outFrame = path.join(tmpDir, `${{f.name}}.png`);
      await page.screenshot({{ path: outFrame, clip: {{ x: 0, y: 0, width: {W}, height: {H} }} }});
    }}
  }}
  await page.close();

  const page2x = await browser.newPage();
  await page2x.setViewport({{ width: {W}, height: {H}, deviceScaleFactor: 2 }});
  await page2x.setContent(`<!doctype html><html><body style="margin:0;padding:0;background:#F8FAFC;overflow:hidden;">${{frames[0].svg}}</body></html>`, {{ waitUntil: 'load' }});
  await page2x.screenshot({{ path: {json.dumps(str(png_2x_path))}, clip: {{ x: 0, y: 0, width: {W}, height: {H} }} }});
  await page2x.close();

  fs.writeFileSync({json.dumps(str(audit_path))}, JSON.stringify(staticAudit, null, 2));
}} finally {{
  await browser.close();
}}
""",
            encoding="utf-8",
        )
        subprocess.run(["node", str(runner_js)], check=True)

        palette_png = tmp_dir / "palette.png"
        pattern = str(tmp_dir / "frame_%03d.png")
        subprocess.run(
            [
                str(ffmpeg), "-y", "-framerate", str(fps), "-i", pattern,
                "-vf", "palettegen=max_colors=256:stats_mode=diff",
                str(palette_png),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                str(ffmpeg), "-y", "-framerate", str(fps), "-i", pattern, "-i", str(palette_png),
                "-lavfi", "paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                "-loop", "0",
                str(gif_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    audit_data = json.loads(audit_path.read_text(encoding="utf-8"))
    return {
        "svg": str(static_svg_path),
        "png_1x": str(png_1x_path),
        "png_2x": str(png_2x_path),
        "gif": str(gif_path),
        "drawio": str(drawio_path),
        "linkedin_post_draft": str(post_md_path),
        "correction_changelog": str(changelog_path),
        "dom_audit": audit_data,
        "gif_bytes": gif_path.stat().st_size,
        "png_2x_bytes": png_2x_path.stat().st_size,
    }


if __name__ == "__main__":
    res = build_corrected_mcp_authorization_bundle()
    print(json.dumps(res, indent=2))
