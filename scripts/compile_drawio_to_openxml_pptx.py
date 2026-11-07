#!/usr/bin/env python3
"""Zero-Dependency Cross-Platform Draw.io (.drawio) -> Native Editable OpenXML (.pptx) & Live Google Slides Compiler.

Compiles every canonical Draw.io blueprint (`T01`, `T53`–`T209`) into 100% native
editable OpenXML PowerPoint (.pptx) shapes, textboxes, and polyline connectors
(zero raster diagram PNGs, zero `<a:tr h="0">` tables) and syncs canonical decks
to Google Slides via Server-Side OAuth Refresh Token (`Rule 47`) or `gdrive` CLI.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

IDEAS_ROOT = Path(__file__).resolve().parent.parent
DRAWIO_DIR = IDEAS_ROOT / "assets" / "canonical-ref" / "drawio"
GALLERY_DIR = IDEAS_ROOT / "assets" / "template-gallery"
MANIFEST_PATH = IDEAS_ROOT / "data" / "template_google_slides_manifest.json"
QUOTA_PROJECT = "ramp-portal-dev"

SLIDE_W_EMU = 12192000  # 13.333 in * 914400
SLIDE_H_EMU = 6858000   # 7.500 in * 914400

TOKEN_PATHS = [
    IDEAS_ROOT / ".gsheet_oauth_token.json",
    Path.home() / "Documents" / "gantry-pulse" / ".gsheet_oauth_token.json",
    Path.home() / "Documents" / "PromptCanvas" / ".gsheet_oauth_token.json",
    Path.home() / "Documents" / "blogs" / ".gsheet_oauth_token.json",
]

GDRIVE_BIN = Path("/google/bin/releases/gemini-agents-gdrive/gdrive")
GSLIDES_BIN = Path("/google/bin/releases/gemini-agents-gslides/gslides")
SCRATCH_BATCH_DIR = Path(
    "/usr/local/google/home/nitinagga/.gemini/jetski/brain/57999333-132a-4bd6-9b5e-5329281d864c/scratch"
)


def _hex_to_rgb_float(hex6: Optional[str]) -> Dict[str, float]:
    c = _clean_hex(hex6, "0F172A") or "0F172A"
    return {
        "red": round(int(c[0:2], 16) / 255.0, 4),
        "green": round(int(c[2:4], 16) / 255.0, 4),
        "blue": round(int(c[4:6], 16) / 255.0, 4),
    }


def _xml_esc(val: Any) -> str:
    return html.escape(str(val or ""), quote=True)


def _clean_hex(raw: Optional[str], fallback: str = "FFFFFF") -> Optional[str]:
    if raw is None:
        return fallback
    s = str(raw).strip()
    if not s or s.lower() in ("none", "transparent"):
        return None
    m = s.lstrip("#")
    if re.fullmatch(r"[0-9A-Fa-f]{6}", m):
        return m.upper()
    if re.fullmatch(r"[0-9A-Fa-f]{3}", m):
        return "".join(ch * 2 for ch in m).upper()
    return fallback


def _is_dark_hex(hex6: Optional[str]) -> bool:
    if not hex6 or len(hex6) != 6:
        return False
    try:
        r = int(hex6[0:2], 16)
        g = int(hex6[2:4], 16)
        b = int(hex6[4:6], 16)
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return lum < 155.0
    except ValueError:
        return False


def _strip_html(raw: str) -> str:
    txt = html.unescape(str(raw or ""))
    txt = re.sub(r"<defs[\s\S]*?</defs>", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"<style[\s\S]*?</style>", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</text>", "\n", txt, flags=re.IGNORECASE)
    txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</(?:div|p|li|tr|h[1-6])>", "\n", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</?[a-zA-Z][^>]*>", " ", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"</?[a-zA-Z][^>]*>", " ", txt)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in txt.splitlines()]
    lines = [ln for ln in lines if ln and ln not in (">_", "✓", "×", "★")]
    return "\n".join(lines[:6])


def _resolve_edge_points(
    sbox: Optional[Tuple[float, float, float, float]],
    tbox: Optional[Tuple[float, float, float, float]],
    style: Dict[str, str],
    waypoints: List[Tuple[float, float]],
    source_pt: Optional[Tuple[float, float]],
    target_pt: Optional[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    pts: List[Tuple[float, float]] = []
    if sbox is not None:
        sx, sy, sw, sh = sbox
        if "exitX" in style or "exitY" in style:
            ex = float(style.get("exitX", 0.5))
            ey = float(style.get("exitY", 0.5))
            pts.append((sx + sw * ex, sy + sh * ey))
        elif waypoints:
            wx, wy = waypoints[0]
            cx, cy = sx + sw / 2.0, sy + sh / 2.0
            if abs(wx - cx) >= abs(wy - cy):
                pts.append((sx + sw if wx >= cx else sx, max(sy, min(sy + sh, wy))))
            else:
                pts.append((max(sx, min(sx + sw, wx)), sy + sh if wy >= cy else sy))
        elif tbox is not None:
            tx, ty, tw, th = tbox
            scx, scy = sx + sw / 2.0, sy + sh / 2.0
            tcx, tcy = tx + tw / 2.0, ty + th / 2.0
            if abs(tcx - scx) >= abs(tcy - scy):
                pts.append((sx + sw if tcx >= scx else sx, scy))
            else:
                pts.append((scx, sy + sh if tcy >= scy else sy))
    elif source_pt is not None:
        pts.append(source_pt)

    pts.extend(waypoints)

    if tbox is not None:
        tx, ty, tw, th = tbox
        if "entryX" in style or "entryY" in style:
            nx = float(style.get("entryX", 0.5))
            ny = float(style.get("entryY", 0.5))
            pts.append((tx + tw * nx, ty + th * ny))
        elif pts:
            lx, ly = pts[-1]
            if tx <= lx <= tx + tw:
                pts.append((lx, ty if ly <= ty + th / 2.0 else ty + th))
            elif ty <= ly <= ty + th:
                pts.append((tx if lx <= tx + tw / 2.0 else tx + tw, ly))
            else:
                cx, cy = tx + tw / 2.0, ty + th / 2.0
                if abs(lx - cx) >= abs(ly - cy):
                    pts.append((tx if lx < cx else tx + tw, cy))
                else:
                    pts.append((cx, ty if ly < cy else ty + th))
    elif target_pt is not None:
        pts.append(target_pt)

    # Orthogonalize any diagonal hop so every connector segment is 100% horizontal or vertical
    ortho: List[Tuple[float, float]] = []
    for p in pts:
        if not ortho:
            ortho.append(p)
            continue
        px, py = ortho[-1]
        nx, ny = p
        if abs(nx - px) > 2.0 and abs(ny - py) > 2.0:
            if not waypoints and style.get("exitY") in ("0", "1") and style.get("entryY") in ("0", "1"):
                mid_y = (py + ny) / 2.0
                ortho.append((px, mid_y))
                ortho.append((nx, mid_y))
            elif not waypoints and style.get("exitX") in ("0", "1") and style.get("entryX") in ("0", "1"):
                mid_x = (px + nx) / 2.0
                ortho.append((mid_x, py))
                ortho.append((mid_x, ny))
            else:
                ortho.append((nx, py))
        if abs(nx - ortho[-1][0]) > 0.5 or abs(ny - ortho[-1][1]) > 0.5:
            ortho.append((nx, ny))
    return ortho


def _parse_style(style_str: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in str(style_str or "").split(";"):
        t = part.strip()
        if not t:
            continue
        if "=" in t:
            k, v = t.split("=", 1)
            out[k.strip()] = v.strip()
        else:
            out[t] = "1"
    return out


def parse_drawio(drawio_path: Path) -> Dict[str, Any]:
    root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
    gm = root.find(".//mxGraphModel")
    if gm is None:
        gm = root
    page_w = float(gm.attrib.get("pageWidth") or 1200)
    page_h = float(gm.attrib.get("pageHeight") or 1350)
    bg_hex = _clean_hex(gm.attrib.get("background") or "#F8FAFC", "F8FAFC") or "F8FAFC"

    cells_by_id: Dict[str, ET.Element] = {}
    for cell in gm.findall(".//mxCell"):
        cid = cell.attrib.get("id")
        if cid:
            cells_by_id[cid] = cell

    def _parent_offset(pid: Optional[str], depth: int = 0) -> Tuple[float, float]:
        if not pid or pid in ("0", "1") or depth > 8 or pid not in cells_by_id:
            return (0.0, 0.0)
        pcell = cells_by_id[pid]
        geom = pcell.find("mxGeometry")
        px = float(geom.attrib.get("x", 0.0)) if geom is not None and geom.attrib.get("relative") != "1" else 0.0
        py = float(geom.attrib.get("y", 0.0)) if geom is not None and geom.attrib.get("relative") != "1" else 0.0
        ox, oy = _parent_offset(pcell.attrib.get("parent"), depth + 1)
        return (px + ox, py + oy)

    vertices: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    poster_svg_texts: List[str] = []

    for cell in gm.findall(".//mxCell"):
        cid = cell.attrib.get("id", "")
        if cid in ("0", "1"):
            continue
        style = _parse_style(cell.attrib.get("style", ""))
        val_raw = cell.attrib.get("value", "")
        unesc_val = html.unescape(val_raw)
        if cid.startswith(("bg", "poster_bg")) and "<svg" in unesc_val:
            poster_svg_texts.append(unesc_val)
            continue

        text = _strip_html(val_raw)
        geom = cell.find("mxGeometry")
        ox, oy = _parent_offset(cell.attrib.get("parent"))

        if cell.attrib.get("vertex") == "1" and geom is not None:
            if geom.attrib.get("relative") == "1":
                parent_cell = cells_by_id.get(cell.attrib.get("parent", ""))
                if parent_cell is not None and parent_cell.attrib.get("edge") == "1":
                    continue
            x = float(geom.attrib.get("x", 0.0)) + ox
            y = float(geom.attrib.get("y", 0.0)) + oy
            w = float(geom.attrib.get("width", 0.0))
            h = float(geom.attrib.get("height", 0.0))
            if w <= 1.0 and h <= 1.0:
                continue
            # If vertex is an inline SVG card/bubble with fillColor=none, inherit fill/stroke from its outer SVG rect/circle
            if "<svg" in unesc_val and style.get("fillColor", "none").lower() == "none":
                cm = re.search(r'<circle\b[^>]*\bfill="([^"]+)"[^>]*\bstroke="([^"]+)"', unesc_val)
                rm = re.search(r'<rect\b[^>]*\bfill="([^"]+)"[^>]*\bstroke="([^"]+)"', unesc_val)
                if cm and abs(w - h) <= 12.0:
                    style = {**style, "shape": "ellipse", "fillColor": cm.group(1), "strokeColor": cm.group(2)}
                elif rm:
                    style = {**style, "rounded": "1", "fillColor": rm.group(1), "strokeColor": rm.group(2)}
            elif "text" in style and "fillColor" not in style:
                bg_m = re.search(r"background:\s*(#[0-9A-Fa-f]{6})", unesc_val)
                bd_m = re.search(r"border:\s*[0-9.]+px\s+solid\s+(#[0-9A-Fa-f]{6})", unesc_val)
                if bg_m and bd_m:
                    style = {
                        **style,
                        "rounded": "1",
                        "fillColor": bg_m.group(1),
                        "strokeColor": bd_m.group(1),
                    }
            vertices.append(
                {
                    "id": cid,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "text": text,
                    "style": style,
                }
            )
        elif cell.attrib.get("edge") == "1":
            src_id = cell.attrib.get("source")
            tgt_id = cell.attrib.get("target")
            sp_el = None
            tp_el = None
            arr_pts: List[Tuple[float, float]] = []
            if geom is not None:
                for pt in geom.findall("mxPoint"):
                    role = pt.attrib.get("as", "")
                    if role == "sourcePoint":
                        sp_el = (float(pt.attrib.get("x", 0.0)) + ox, float(pt.attrib.get("y", 0.0)) + oy)
                    elif role == "targetPoint":
                        tp_el = (float(pt.attrib.get("x", 0.0)) + ox, float(pt.attrib.get("y", 0.0)) + oy)
                arr = geom.find("Array[@as='points']")
                if arr is not None:
                    for pt in arr.findall("mxPoint"):
                        arr_pts.append((float(pt.attrib.get("x", 0.0)) + ox, float(pt.attrib.get("y", 0.0)) + oy))

            edges.append(
                {
                    "id": cid,
                    "source": src_id,
                    "target": tgt_id,
                    "source_pt": sp_el,
                    "target_pt": tp_el,
                    "waypoints": arr_pts,
                    "text": text,
                    "style": style,
                }
            )

    # Extract native editable shapes and lines from poster_bg / bg_ SVG backdrops when present
    for svg_idx, p_svg in enumerate(poster_svg_texts):
        body = re.sub(r"<defs[\s\S]*?</defs>", "", p_svg, flags=re.IGNORECASE)
        body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.IGNORECASE)
        svg_texts: List[Tuple[float, float, str]] = []
        for tm in re.finditer(r"<text\b([^>]*)>(.*?)</text>", body, flags=re.DOTALL | re.IGNORECASE):
            t_attrs = dict(re.findall(r'([a-zA-Z0-9_:-]+)="([^"]*)"', tm.group(1) or ""))
            clean_t = re.sub(r"<[^>]+>", " ", tm.group(2) or "").strip()
            clean_t = html.unescape(re.sub(r"\s+", " ", clean_t))
            if clean_t:
                try:
                    svg_texts.append((float(t_attrs.get("x", 0.0)), float(t_attrs.get("y", 0.0)), clean_t))
                except ValueError:
                    pass

        sub_idx = 0
        raw_svg_shapes: List[Dict[str, Any]] = []
        for sm in re.finditer(r"<(rect|circle|line)\b([^>]*)/?>", body, flags=re.IGNORECASE):
            tag = sm.group(1).lower()
            s_attrs = dict(re.findall(r'([a-zA-Z0-9_:-]+)="([^"]*)"', sm.group(2) or ""))
            sub_idx += 1
            if tag == "rect":
                try:
                    rx = float(s_attrs.get("x", 0.0))
                    ry = float(s_attrs.get("y", 0.0))
                    rw = float(s_attrs.get("width", 0.0))
                    rh = float(s_attrs.get("height", 0.0))
                    if rw >= page_w * 0.94 and rh >= page_h * 0.85:
                        continue
                    if rw < 42.0 or rh < 20.0 or ry < 110.0 or ry > page_h - 48.0:
                        continue
                    f_col = s_attrs.get("fill", "#FFFFFF")
                    if f_col.startswith("url(") or f_col == "none":
                        f_col = "#FFFFFF"
                    st_col = s_attrs.get("stroke", "#CBD5E1")
                    raw_svg_shapes.append(
                        {
                            "kind": "rect",
                            "id": f"svg_rect_{svg_idx}_{sub_idx}",
                            "x": rx,
                            "y": ry,
                            "w": rw,
                            "h": rh,
                            "order": sub_idx,
                            "style": {
                                "rounded": "1" if s_attrs.get("rx") else "0",
                                "fillColor": f_col,
                                "strokeColor": st_col,
                                "fontSize": "9.5" if rh <= 30.0 else "10.5",
                            },
                        }
                    )
                except ValueError:
                    pass
            elif tag == "circle":
                try:
                    cx = float(s_attrs["cx"])
                    cy = float(s_attrs["cy"])
                    r = float(s_attrs["r"])
                    if r < 15.0 or r > 140.0 or cy < 130.0 or cy > page_h - 50.0:
                        continue
                    f_col = s_attrs.get("fill", "#FFFFFF")
                    if f_col.startswith("url(") or f_col == "none":
                        f_col = "#FFFFFF"
                    st_col = s_attrs.get("stroke", "#2563EB")
                    raw_svg_shapes.append(
                        {
                            "kind": "circle",
                            "id": f"svg_circ_{svg_idx}_{sub_idx}",
                            "x": cx - r,
                            "y": cy - r,
                            "w": 2.0 * r,
                            "h": 2.0 * r,
                            "cx": cx,
                            "cy": cy,
                            "r": r,
                            "order": sub_idx,
                            "style": {
                                "shape": "ellipse",
                                "fillColor": f_col,
                                "strokeColor": st_col,
                                "fontSize": "9.5",
                                "verticalAlign": "bottom" if r >= 70.0 else "middle",
                            },
                        }
                    )
                except (KeyError, ValueError):
                    pass
            elif tag == "line":
                try:
                    x1 = float(s_attrs["x1"])
                    y1 = float(s_attrs["y1"])
                    x2 = float(s_attrs["x2"])
                    y2 = float(s_attrs["y2"])
                    llen = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    is_ortho = abs(x1 - x2) <= 3.0 or abs(y1 - y2) <= 3.0
                    if 18.0 <= llen <= 780.0 and min(y1, y2) >= 130.0 and max(y1, y2) <= page_h - 50.0 and is_ortho:
                        st_col = s_attrs.get("stroke", "#475569")
                        edges.append(
                            {
                                "id": f"svg_line_{svg_idx}_{sub_idx}",
                                "source": None,
                                "target": None,
                                "source_pt": (x1, y1),
                                "target_pt": (x2, y2),
                                "waypoints": [],
                                "text": "",
                                "style": {
                                    "strokeColor": st_col,
                                    "strokeWidth": s_attrs.get("stroke-width", "1.8"),
                                    "dashed": "1" if s_attrs.get("stroke-dasharray") else "0",
                                    "endArrow": "classic" if s_attrs.get("marker-end") else "none",
                                },
                            }
                        )
                except (KeyError, ValueError):
                    pass

        # Claim svg_texts smallest-shape-first so inner pill rects never duplicate their text onto outer lens circles
        claimed_text_idxs: set[int] = set()
        for shp in sorted(raw_svg_shapes, key=lambda s: s["w"] * s["h"]):
            matched: List[str] = []
            for t_idx, (tx, ty, t_str) in enumerate(svg_texts):
                if t_idx in claimed_text_idxs:
                    continue
                if shp["kind"] == "rect":
                    if shp["x"] - 6.0 <= tx <= shp["x"] + shp["w"] + 6.0 and shp["y"] <= ty <= shp["y"] + shp["h"] + 5.0:
                        matched.append(t_str)
                        claimed_text_idxs.add(t_idx)
                else:
                    if (tx - shp["cx"]) ** 2 + (ty - shp["cy"]) ** 2 <= (shp["r"] + 8.0) ** 2:
                        matched.append(t_str)
                        claimed_text_idxs.add(t_idx)
            shp["text"] = "\n".join(matched[:4])

        for shp in sorted(raw_svg_shapes, key=lambda s: s["order"]):
            if shp["kind"] == "rect" and shp["w"] > page_w * 0.75 and shp["h"] > 360.0 and not shp["text"]:
                continue
            vertices.append(
                {
                    "id": shp["id"],
                    "x": shp["x"],
                    "y": shp["y"],
                    "w": shp["w"],
                    "h": shp["h"],
                    "text": shp["text"],
                    "style": shp["style"],
                }
            )

    # Compute tight bounding box if vertices exceed page_w/page_h
    if vertices:
        max_r = max(v["x"] + v["w"] for v in vertices)
        max_b = max(v["y"] + v["h"] for v in vertices)
        page_w = max(page_w, max_r + 24.0)
        page_h = max(page_h, max_b + 24.0)

    v_map = {v["id"]: v for v in vertices}
    resolved_edges: List[Dict[str, Any]] = []
    for e in edges:
        sv = v_map.get(e["source"]) if e["source"] else None
        tv = v_map.get(e["target"]) if e["target"] else None
        sbox = (sv["x"], sv["y"], sv["w"], sv["h"]) if sv else None
        tbox = (tv["x"], tv["y"], tv["w"], tv["h"]) if tv else None
        pts = _resolve_edge_points(sbox, tbox, e["style"], e["waypoints"], e["source_pt"], e["target_pt"])
        if len(pts) >= 2:
            resolved_edges.append({**e, "points": pts})

    return {
        "page_w": page_w,
        "page_h": page_h,
        "bg_hex": bg_hex,
        "vertices": vertices,
        "edges": resolved_edges,
    }


def _detect_section_bands(vertices: List[Dict[str, Any]], page_w: float) -> List[Dict[str, Any]]:
    bands = []
    for v in vertices:
        if v["w"] >= page_w * 0.68 and 140 <= v["h"] <= 460 and v["y"] >= 90:
            fill = _clean_hex(v["style"].get("fillColor"), "")
            stroke = _clean_hex(v["style"].get("strokeColor"), "")
            if fill or stroke:
                bands.append(v)
    bands.sort(key=lambda b: b["y"])
    deduped: List[Dict[str, Any]] = []
    for b in bands:
        if not deduped or abs(b["y"] - deduped[-1]["y"]) > 90:
            deduped.append(b)
    return deduped[:5]


def _shape_preset(style: Dict[str, str]) -> str:
    sh = style.get("shape", "")
    if "ellipse" in style or sh == "ellipse":
        return "ellipse"
    if "rhombus" in style or sh == "rhombus":
        return "diamond"
    if sh == "hexagon":
        return "hexagon"
    if sh in ("cylinder", "cylinder3"):
        return "can"
    if style.get("rounded") == "1":
        return "roundRect"
    return "rect"


def _partition_bg_and_fg_vertices(
    vertices: List[Dict[str, Any]], crop: Tuple[float, float, float, float]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    cx0, cy0, cw, ch = crop
    visible: List[Dict[str, Any]] = []
    for v in vertices:
        if v["w"] >= cw * 0.97 and v["h"] >= ch * 0.95 and not v["text"]:
            continue
        vx2 = v["x"] + v["w"]
        vy2 = v["y"] + v["h"]
        if vx2 < cx0 + 2 or v["x"] > cx0 + cw - 2 or vy2 < cy0 + 2 or v["y"] > cy0 + ch - 2:
            continue
        visible.append(v)

    bg_containers: List[Dict[str, Any]] = []
    fg_cards: List[Dict[str, Any]] = []
    for a in visible:
        a_area = a["w"] * a["h"]
        contains_smaller = any(
            b["id"] != a["id"]
            and (b["w"] * b["h"]) < a_area * 0.85
            and (b["x"] + b["w"] / 2.0) >= a["x"] + 2.0
            and (b["x"] + b["w"] / 2.0) <= a["x"] + a["w"] - 2.0
            and (b["y"] + b["h"] / 2.0) >= a["y"] + 2.0
            and (b["y"] + b["h"] / 2.0) <= a["y"] + a["h"] - 2.0
            for b in visible
        )
        if contains_smaller or (a["w"] >= cw * 0.62 and a["h"] >= 110.0 and not a["text"]):
            bg_containers.append(a)
        else:
            fg_cards.append(a)
    bg_containers.sort(key=lambda b: -(b["w"] * b["h"]))
    return bg_containers, fg_cards


def _render_region_shapes_xml(
    vertices: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    crop: Tuple[float, float, float, float],
    dest_emu: Tuple[int, int, int, int],
    start_id: int = 10,
    font_scale: float = 1.0,
) -> Tuple[List[str], int]:
    cx0, cy0, cw, ch = crop
    dx0, dy0, dw, dh = dest_emu
    sx = dw / max(cw, 1.0)
    sy = dh / max(ch, 1.0)
    scale = min(sx, sy)
    pad_x = dx0 + int((dw - cw * scale) / 2.0)
    pad_y = dy0 + int((dh - ch * scale) / 2.0)

    shapes: List[str] = []
    next_id = start_id
    bg_containers, fg_cards = _partition_bg_and_fg_vertices(vertices, crop)

    def _emit_vertex_xml(v: Dict[str, Any]) -> None:
        nonlocal next_id
        x_emu = max(0, pad_x + int((v["x"] - cx0) * scale))
        y_emu = max(0, pad_y + int((v["y"] - cy0) * scale))
        w_emu = max(25400, int(v["w"] * scale))
        h_emu = max(25400, int(v["h"] * scale))

        st = v["style"]
        is_text_only = "text" in st and "fillColor" not in st and "strokeColor" not in st
        fill_hex = None if is_text_only else _clean_hex(st.get("fillColor"), "FFFFFF")
        stroke_hex = None if is_text_only else _clean_hex(st.get("strokeColor"), "CBD5E1")
        is_dark = _is_dark_hex(fill_hex)
        default_font = "FFFFFF" if is_dark else "0F172A"
        font_hex = _clean_hex(st.get("fontColor"), default_font) or default_font
        prst = _shape_preset(st)

        fill_xml = f'<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill>' if fill_hex else "<a:noFill/>"
        if stroke_hex:
            sw_px = float(st.get("strokeWidth", 1.2) or 1.2)
            ln_w = max(9525, min(38100, int(sw_px * 9525)))
            dash_xml = '<a:prstDash val="dash"/>' if st.get("dashed") == "1" else ""
            ln_xml = f'<a:ln w="{ln_w}"><a:solidFill><a:srgbClr val="{stroke_hex}"/></a:solidFill>{dash_xml}</a:ln>'
        else:
            ln_xml = "<a:ln><a:noFill/></a:ln>"

        raw_fs = float(st.get("fontSize", 11.5) or 11.5)
        pt_sz = max(7.5, min(20.0, raw_fs * (scale / 9525.0) * 0.92 * font_scale))
        align_map = {"left": "l", "center": "ctr", "right": "r"}
        algn = align_map.get(st.get("align", "center"), "ctr")
        valign_map = {"top": "t", "middle": "ctr", "bottom": "b"}
        anchor = valign_map.get(st.get("verticalAlign", "middle"), "ctr")

        if v["text"]:
            lines = v["text"].split("\n")
            p_rows: List[str] = []
            for l_idx, ln in enumerate(lines):
                if len(lines) >= 2 and l_idx == 0:
                    line_b = "1"
                    line_sz = int(round(min(21.0, pt_sz * 1.12) * 100))
                    line_col = "FFFFFF" if is_dark else (font_hex if font_hex != "0F172A" else "1E3A8A")
                elif len(lines) >= 2:
                    line_b = "0"
                    line_sz = int(round(max(7.0, pt_sz * 0.90) * 100))
                    line_col = "E2E8F0" if is_dark else "334155"
                else:
                    line_b = "1" if (st.get("fontStyle") in ("1", "3", "5") or len(v["text"]) <= 36) else "0"
                    line_sz = int(round(pt_sz * 100))
                    line_col = font_hex
                p_rows.append(
                    f'              <a:p><a:pPr algn="{algn}"/><a:r><a:rPr lang="en-US" sz="{line_sz}" b="{line_b}"><a:solidFill><a:srgbClr val="{line_col}"/></a:solidFill></a:rPr><a:t>{_xml_esc(ln)}</a:t></a:r></a:p>'
                )
            p_Xml = "\n".join(p_rows)
            tx_xml = (
                f"          <p:txBody>\n"
                f'            <a:bodyPr wrap="square" anchor="{anchor}" lIns="45720" tIns="27432" rIns="45720" bIns="27432"/>\n'
                f"            <a:lstStyle/>\n"
                f"{p_Xml}\n"
                f"          </p:txBody>"
            )
        else:
            tx_xml = '          <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>'

        shapes.append(
            f"        <p:sp>\n"
            f'          <p:nvSpPr><p:cNvPr id="{next_id}" name="Node_{next_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
            f"          <p:spPr>\n"
            f'            <a:xfrm><a:off x="{x_emu}" y="{y_emu}"/><a:ext cx="{w_emu}" cy="{h_emu}"/></a:xfrm>\n'
            f'            <a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>\n'
            f"            {fill_xml}\n"
            f"            {ln_xml}\n"
            f"          </p:spPr>\n"
            f"{tx_xml}\n"
            f"        </p:sp>"
        )
        next_id += 1

    # Pass 1: Background containers & section bands
    for v in bg_containers:
        _emit_vertex_xml(v)

    # Pass 2: Native editable orthogonal straightConnector1 segments (<p:cxnSp>)
    edge_label_shapes: List[str] = []
    for e in edges:
        pts = e["points"]
        if any(px < cx0 - 8 or px > cx0 + cw + 8 or py < cy0 - 8 or py > cy0 + ch + 8 for (px, py) in pts):
            continue
        emu_pts = [(pad_x + int((px - cx0) * scale), pad_y + int((py - cy0) * scale)) for (px, py) in pts]

        st = e["style"]
        stroke_hex = _clean_hex(st.get("strokeColor"), "475569") or "475569"
        sw_px = float(st.get("strokeWidth", 1.8) or 1.8)
        ln_w = max(12700, min(38100, int(sw_px * 9525)))
        dash_xml = '<a:prstDash val="dash"/>' if st.get("dashed") == "1" else ""
        end_arrow = st.get("endArrow", "classic")
        start_arrow = st.get("startArrow", "none")

        num_segs = len(emu_pts) - 1
        for seg_idx in range(num_segs):
            (x1, y1), (x2, y2) = emu_pts[seg_idx], emu_pts[seg_idx + 1]
            if abs(x2 - x1) < 100 and abs(y2 - y1) < 100:
                continue
            seg_min_x = min(x1, x2)
            seg_min_y = min(y1, y2)
            seg_w = max(0, abs(x2 - x1))
            seg_h = max(0, abs(y2 - y1))
            flip_attrs = ""
            if x2 < x1:
                flip_attrs += ' flipH="1"'
            if y2 < y1:
                flip_attrs += ' flipV="1"'
            head_xml = (
                '<a:headEnd type="triangle" w="med" len="med"/>'
                if (seg_idx == 0 and start_arrow not in ("none", ""))
                else ""
            )
            tail_xml = (
                '<a:tailEnd type="triangle" w="med" len="med"/>'
                if (seg_idx == num_segs - 1 and end_arrow != "none")
                else ""
            )
            shapes.append(
                f"        <p:cxnSp>\n"
                f'          <p:nvCxnSpPr><p:cNvPr id="{next_id}" name="EdgeSeg_{next_id}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>\n'
                f"          <p:spPr>\n"
                f'            <a:xfrm{flip_attrs}><a:off x="{seg_min_x}" y="{seg_min_y}"/><a:ext cx="{seg_w}" cy="{seg_h}"/></a:xfrm>\n'
                f'            <a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>\n'
                f'            <a:ln w="{ln_w}"><a:solidFill><a:srgbClr val="{stroke_hex}"/></a:solidFill>{dash_xml}{head_xml}{tail_xml}</a:ln>\n'
                f"          </p:spPr>\n"
                f"        </p:cxnSp>"
            )
            next_id += 1

        if e["text"]:
            mid_idx = len(emu_pts) // 2
            mx, my = emu_pts[mid_idx]
            lbl_w = max(540000, min(1800000, len(e["text"]) * 62000))
            lbl_h = 228600
            lx = max(0, mx - lbl_w // 2)
            ly = max(0, my - lbl_h // 2)
            edge_label_shapes.append(
                f"        <p:sp>\n"
                f'          <p:nvSpPr><p:cNvPr id="{next_id}" name="EdgeLabel_{next_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
                f"          <p:spPr>\n"
                f'            <a:xfrm><a:off x="{lx}" y="{ly}"/><a:ext cx="{lbl_w}" cy="{lbl_h}"/></a:xfrm>\n'
                f'            <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>\n'
                f'            <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>\n'
                f'            <a:ln w="9525"><a:solidFill><a:srgbClr val="{stroke_hex}"/></a:solidFill></a:ln>\n'
                f"          </p:spPr>\n"
                f"          <p:txBody>\n"
                f'            <a:bodyPr wrap="square" anchor="ctr" lIns="27432" tIns="9144" rIns="27432" bIns="9144"/>\n'
                f"            <a:lstStyle/>\n"
                f'            <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="800" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{_xml_esc(e["text"])}</a:t></a:r></a:p>\n'
                f"          </p:txBody>\n"
                f"        </p:sp>"
            )
            next_id += 1

    # Pass 3: Foreground cards, badges, pills, headers, footers & edge labels (sit cleanly above edges)
    for v in fg_cards:
        _emit_vertex_xml(v)
    shapes.extend(edge_label_shapes)

    return shapes, next_id


def _wrap_slide_xml(bg_hex: str, shapes: List[str]) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
        "  <p:cSld>\n"
        f'    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg_hex}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>\n'
        "    <p:spTree>\n"
        '      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>\n'
        '      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>\n'
        + "\n".join(shapes)
        + "\n    </p:spTree>\n"
        "  </p:cSld>\n"
        "  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>\n"
        "</p:sld>\n"
    )


def _header_and_footer_shapes(tid: str, title: str, subtitle: str, slide_idx: int, total_slides: int) -> List[str]:
    return [
        f"""        <p:sp>
          <p:nvSpPr><p:cNvPr id="2" name="TopBanner"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="320000" y="160000"/><a:ext cx="9200000" cy="540000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:noFill/>
          </p:spPr>
          <p:txBody>
            <a:bodyPr wrap="square" anchor="t"/>
            <a:lstStyle/>
            <a:p><a:r><a:rPr lang="en-US" sz="1550" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{_xml_esc(tid)} — {_xml_esc(title)}</a:t></a:r></a:p>
            <a:p><a:r><a:rPr lang="en-US" sz="950" b="1"><a:solidFill><a:srgbClr val="475569"/></a:solidFill></a:rPr><a:t>{_xml_esc(subtitle)}</a:t></a:r></a:p>
          </p:txBody>
        </p:sp>""",
        """        <p:sp>
          <p:nvSpPr><p:cNvPr id="3" name="NativeBadge"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="9620000" y="210000"/><a:ext cx="2250000" cy="320000"/></a:xfrm>
            <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
            <a:solidFill><a:srgbClr val="ECFDF5"/></a:solidFill>
            <a:ln w="12700"><a:solidFill><a:srgbClr val="10B981"/></a:solidFill></a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr anchor="ctr"/>
            <a:lstStyle/>
            <a:p><a:pPr algn="ctr"/><a:r><a:rPr lang="en-US" sz="880" b="1"><a:solidFill><a:srgbClr val="065F46"/></a:solidFill></a:rPr><a:t>100% Native Editable Shapes</a:t></a:r></a:p>
          </p:txBody>
        </p:sp>""",
        f"""        <p:sp>
          <p:nvSpPr><p:cNvPr id="4" name="FooterBar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="320000" y="6480000"/><a:ext cx="11550000" cy="260000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:noFill/>
          </p:spPr>
          <p:txBody>
            <a:bodyPr anchor="ctr"/>
            <a:lstStyle/>
            <a:p><a:r><a:rPr lang="en-US" sz="850" b="1"><a:solidFill><a:srgbClr val="64748B"/></a:solidFill></a:rPr><a:t>Proprietary + Confidential  |  Cloudstyle 2.0 Canonical Blueprint ({_xml_esc(tid)})  |  Slide {slide_idx} of {total_slides}</a:t></a:r></a:p>
          </p:txBody>
        </p:sp>""",
    ]


def _notes_xml(tid: str, title: str, slide_idx: int) -> str:
    p1 = f"Here on Slide {slide_idx}, we examine the 100% native editable architecture blueprint for {tid}: {title}."
    p2 = "Every shape, connector, badge, and metric callout on this canvas is compiled directly from canonical Draw.io geometry with zero raster diagram screenshots."
    p3 = "Teams can customize every node label, trust boundary, and SLO target directly in Google Slides or PowerPoint."
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
        "  <p:cSld><p:spTree>\n"
        '    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>\n'
        '    <p:sp><p:nvSpPr><p:cNvPr id="2" name="Notes"/><p:cNvSpPr/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>\n'
        "      <p:txBody><a:bodyPr/><a:lstStyle/>\n"
        f'        <a:p><a:r><a:rPr lang="en-US" sz="1100"/><a:t>{_xml_esc(p1)}</a:t></a:r></a:p>\n'
        f'        <a:p><a:r><a:rPr lang="en-US" sz="1100"/><a:t>{_xml_esc(p2)}</a:t></a:r></a:p>\n'
        f'        <a:p><a:r><a:rPr lang="en-US" sz="1100"/><a:t>{_xml_esc(p3)}</a:t></a:r></a:p>\n'
        "      </p:txBody></p:sp>\n"
        "  </p:spTree></p:cSld>\n"
        "</p:notes>\n"
    )


def compile_drawio_to_pptx(tid: str, title: str) -> Tuple[Path, bytes, int]:
    drawio_path = DRAWIO_DIR / f"{tid}.drawio"
    if not drawio_path.exists():
        drawio_path = GALLERY_DIR / f"{tid}.drawio"
    if not drawio_path.exists():
        raise FileNotFoundError(f"Missing Draw.io blueprint for {tid}: {drawio_path}")

    parsed = parse_drawio(drawio_path)
    page_w = parsed["page_w"]
    page_h = parsed["page_h"]
    bg_hex = parsed["bg_hex"]
    vertices = parsed["vertices"]
    edges = parsed["edges"]

    bands = _detect_section_bands(vertices, page_w)
    total_slides = 1 + (len(bands) if len(bands) >= 2 else 2)

    slide_xmls: List[str] = []

    # Slide 1: Full-Poster Native Editable Overview + Right Executive Design Rail when portrait
    if page_h > page_w * 0.92:
        # Left 68% Blueprint + Right 32% 3-Card Executive Design Rail (Cloudstyle 2.0 Master Layout)
        bp_shapes, next_id = _render_region_shapes_xml(
            vertices,
            edges,
            (0.0, 0.0, page_w, page_h),
            (320000, 760000, 7820000, 5620000),
            start_id=10,
            font_scale=1.08,
        )
        rail_cards = [
            ("DESIGN INVARIANT", "Canonical Geometry", f"Compiled from {tid}.drawio with zero text collisions and native vector connectors.", "2563EB", 780000),
            ("PRODUCTION STACK", "Google Cloud ADK ⇄ OSS", "Vertex AI Gemini 4 Argon / 3.8 Flash (locations/global) + Model Armor + OpenHands.", "059669", 2680000),
            ("CAREER & SLO IMPACT", "Staff+ Proof Telemetry", "100% editable shapes in Google Slides & PowerPoint for executive & customer reviews.", "7C3AED", 4580000),
        ]
        for badge, ctitle, cbody, col, ry in rail_cards:
            bp_shapes.append(
                f"""        <p:sp>
          <p:nvSpPr><p:cNvPr id="{next_id}" name="Rail_{next_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="8320000" y="{ry}"/><a:ext cx="3550000" cy="1740000"/></a:xfrm>
            <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
            <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
            <a:ln w="15875"><a:solidFill><a:srgbClr val="{col}"/></a:solidFill></a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr wrap="square" anchor="t" lIns="114300" tIns="91440" rIns="114300" bIns="91440"/>
            <a:lstStyle/>
            <a:p><a:r><a:rPr lang="en-US" sz="900" b="1"><a:solidFill><a:srgbClr val="{col}"/></a:solidFill></a:rPr><a:t>{_xml_esc(badge)}</a:t></a:r></a:p>
            <a:p><a:r><a:rPr lang="en-US" sz="1250" b="1"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill></a:rPr><a:t>{_xml_esc(ctitle)}</a:t></a:r></a:p>
            <a:p><a:r><a:rPr lang="en-US" sz="1000"><a:solidFill><a:srgbClr val="334155"/></a:solidFill></a:rPr><a:t>{_xml_esc(cbody)}</a:t></a:r></a:p>
          </p:txBody>
        </p:sp>"""
            )
            next_id += 1
    else:
        bp_shapes, _ = _render_region_shapes_xml(
            vertices,
            edges,
            (0.0, 0.0, page_w, page_h),
            (320000, 760000, 11550000, 5620000),
            start_id=10,
            font_scale=1.05,
        )

    s1_shapes = _header_and_footer_shapes(
        tid,
        title,
        "Slide 1: Complete Cloudstyle 2.0 Native Editable Blueprint Overview",
        1,
        total_slides,
    ) + bp_shapes
    slide_xmls.append(_wrap_slide_xml("F8FAFC" if bg_hex == "FFFFFF" else bg_hex, s1_shapes))

    if len(bands) >= 2:
        for b_idx, band in enumerate(bands, start=2):
            band_shapes, _ = _render_region_shapes_xml(
                vertices,
                edges,
                (max(0.0, band["x"] - 24.0), max(0.0, band["y"] - 12.0), min(page_w, band["w"] + 48.0), band["h"] + 24.0),
                (320000, 820000, 11550000, 5520000),
                start_id=10,
                font_scale=1.25,
            )
            sb_shapes = _header_and_footer_shapes(
                tid,
                title,
                f"Slide {b_idx}: Widescreen Section Band {b_idx - 1:02d} Native Architecture Zoom",
                b_idx,
                total_slides,
            ) + band_shapes
            slide_xmls.append(_wrap_slide_xml("F8FAFC", sb_shapes))
    else:
        # Slide 2: Upper Architecture Stage Widescreen Vector Zoom
        zoom_top, _ = _render_region_shapes_xml(
            vertices,
            edges,
            (0.0, 0.0, page_w, page_h * 0.58),
            (280000, 760000, 11630000, 5640000),
            start_id=10,
            font_scale=1.22,
        )
        s2_shapes = _header_and_footer_shapes(
            tid,
            title,
            "Slide 2: Upper Architecture Stage 16:9 Widescreen Editable Vector Zoom",
            2,
            total_slides,
        ) + zoom_top
        slide_xmls.append(_wrap_slide_xml("FFFFFF", s2_shapes))

        # Slide 3: Lower Execution & Telemetry Widescreen Vector Zoom
        zoom_bot, _ = _render_region_shapes_xml(
            vertices,
            edges,
            (0.0, page_h * 0.42, page_w, page_h * 0.58),
            (280000, 760000, 11630000, 5640000),
            start_id=10,
            font_scale=1.22,
        )
        s3_shapes = _header_and_footer_shapes(
            tid,
            title,
            "Slide 3: Lower Execution & Telemetry 16:9 Widescreen Editable Vector Zoom",
            3,
            total_slides,
        ) + zoom_bot
        slide_xmls.append(_wrap_slide_xml("F8FAFC", s3_shapes))

    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    out_pptx = GALLERY_DIR / f"{tid}.pptx"
    with zipfile.ZipFile(out_pptx, "w", zipfile.ZIP_STORED) as zf:
        ct_overrides = [
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        ]
        sld_ids = []
        pres_rels = [
            '<Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
        ]
        for idx, s_xml in enumerate(slide_xmls, start=1):
            ct_overrides.append(
                f'<Override PartName="/ppt/slides/slide{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            )
            ct_overrides.append(
                f'<Override PartName="/ppt/notesSlides/notesSlide{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
            )
            sld_ids.append(f'<p:sldId id="{255 + idx}" r:id="rIdSlide{idx}"/>')
            pres_rels.append(
                f'<Relationship Id="rIdSlide{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{idx}.xml"/>'
            )
            zf.writestr(f"ppt/slides/slide{idx}.xml", s_xml)
            zf.writestr(
                f"ppt/slides/_rels/slide{idx}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>\n'
                f'  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{idx}.xml"/>\n'
                "</Relationships>\n",
            )
            zf.writestr(f"ppt/notesSlides/notesSlide{idx}.xml", _notes_xml(tid, title, idx))
            zf.writestr(
                f"ppt/notesSlides/_rels/notesSlide{idx}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
                f'  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{idx}.xml"/>\n'
                "</Relationships>\n",
            )

        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
            '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
            '  <Default Extension="xml" ContentType="application/xml"/>\n  '
            + "\n  ".join(ct_overrides)
            + "\n</Types>\n",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>\n'
            "</Relationships>\n",
        )
        zf.writestr(
            "ppt/presentation.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
            '  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rIdMaster1"/></p:sldMasterIdLst>\n'
            f'  <p:sldIdLst>{"".join(sld_ids)}</p:sldIdLst>\n'
            f'  <p:sldSz cx="{SLIDE_W_EMU}" cy="{SLIDE_H_EMU}" type="custom"/>\n'
            '  <p:notesSz cx="6858000" cy="9144000"/>\n'
            "</p:presentation>\n",
        )
        zf.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n  '
            + "\n  ".join(pres_rels)
            + "\n</Relationships>\n",
        )
        zf.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">\n'
            '  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>\n'
            '  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>\n'
            '  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rIdLayout1"/></p:sldLayoutIdLst>\n'
            "</p:sldMaster>\n",
        )
        zf.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            '  <Relationship Id="rIdLayout1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>\n'
            "</Relationships>\n",
        )
        zf.writestr(
            "ppt/slideLayouts/slideLayout1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">\n'
            '  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>\n'
            "</p:sldLayout>\n",
        )

    pptx_bytes = out_pptx.read_bytes()
    return out_pptx, pptx_bytes, len(slide_xmls)


def _get_refresh_access_token() -> Optional[str]:
    for tp in TOKEN_PATHS:
        if not tp.exists():
            continue
        try:
            raw = json.loads(tp.read_text(encoding="utf-8"))
            if not (raw.get("client_id") and raw.get("client_secret") and raw.get("refresh_token")):
                continue
            data = urllib.parse.urlencode(
                {
                    "client_id": raw["client_id"],
                    "client_secret": raw["client_secret"],
                    "refresh_token": raw["refresh_token"],
                    "grant_type": "refresh_token",
                }
            ).encode("utf-8")
            req = urllib.request.Request(
                "https://oauth2.googleapis.com/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                tok = json.loads(resp.read().decode("utf-8")).get("access_token")
                if tok:
                    return str(tok)
        except Exception:
            continue
    return None


def _gslides_shape_type(style: Dict[str, str]) -> str:
    sh = style.get("shape", "")
    if "ellipse" in style or sh == "ellipse":
        return "ELLIPSE"
    if "rhombus" in style or sh == "rhombus":
        return "DIAMOND"
    if sh == "hexagon":
        return "HEXAGON"
    if sh in ("cylinder", "cylinder3"):
        return "CAN"
    if style.get("rounded") == "1":
        return "ROUND_RECTANGLE"
    return "RECTANGLE"


def _make_gslides_shape_With_text_reqs(
    obj_id: str,
    slide_id: str,
    shape_type: str,
    x_emu: int,
    y_emu: int,
    w_emu: int,
    h_emu: int,
    fill_hex: Optional[str],
    stroke_hex: Optional[str],
    stroke_emu: int,
    dashed: bool,
    text_str: str,
    pt_sz: float,
    align: str = "CENTER",
    valign: str = "MIDDLE",
    font_hex: str = "0F172A",
    force_bold_single: bool = False,
) -> List[Dict[str, Any]]:
    reqs: List[Dict[str, Any]] = [
        {
            "createShape": {
                "objectId": obj_id,
                "shapeType": shape_type,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width": {"magnitude": max(12700, int(w_emu)), "unit": "EMU"},
                        "height": {"magnitude": max(12700, int(h_emu)), "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": max(0, int(x_emu)),
                        "translateY": max(0, int(y_emu)),
                        "unit": "EMU",
                    },
                },
            }
        }
    ]

    shape_props: Dict[str, Any] = {"contentAlignment": valign}
    fields = ["contentAlignment"]
    if fill_hex:
        shape_props["shapeBackgroundFill"] = {
            "solidFill": {"color": {"rgbColor": _hex_to_rgb_float(fill_hex)}, "alpha": 1}
        }
        fields.append("shapeBackgroundFill")
    else:
        shape_props["shapeBackgroundFill"] = {"propertyState": "NOT_RENDERED"}
        fields.append("shapeBackgroundFill.propertyState")

    if stroke_hex:
        shape_props["outline"] = {
            "outlineFill": {"solidFill": {"color": {"rgbColor": _hex_to_rgb_float(stroke_hex)}}},
            "weight": {"magnitude": max(9525, int(stroke_emu)), "unit": "EMU"},
            "dashStyle": "DASH" if dashed else "SOLID",
        }
        fields.extend(["outline.outlineFill", "outline.weight", "outline.dashStyle"])
    else:
        shape_props["outline"] = {"propertyState": "NOT_RENDERED"}
        fields.append("outline.propertyState")

    reqs.append(
        {
            "updateShapeProperties": {
                "objectId": obj_id,
                "shapeProperties": shape_props,
                "fields": ",".join(fields),
            }
        }
    )

    clean_txt = (text_str or "").strip()
    if clean_txt:
        is_dark = _is_dark_hex(fill_hex)
        lines = clean_txt.split("\n")
        w_pt = max(8.0, w_emu / 12700.0)
        h_pt = max(6.0, h_emu / 12700.0)
        is_compact_badge = (
            len(lines) == 1
            and len(clean_txt) <= 16
            and (fill_hex is not None or stroke_hex is not None)
            and (shape_type == "ELLIPSE" or w_emu < 1250000 or h_emu < 380000)
        )

        # Fit pt_sz so no word ever breaks mid-word ("boar\nd", "Clou\nd") and total lines never overflow h_pt
        usable_w_pt = w_pt * (0.82 if shape_type == "ELLIPSE" else 0.94)
        if not is_compact_badge:
            words = re.findall(r"[A-Za-z0-9+/._-]+", clean_txt)
            max_word_len = max((len(w) for w in words), default=1)
            if max_word_len >= 4 and len(clean_txt) <= 48:
                pt_sz = min(pt_sz, usable_w_pt / (max_word_len * 0.57))
            for _ in range(3):
                cpl = max(5.0, usable_w_pt / max(2.0, pt_sz * 0.53))
                vis_lines = sum(max(1, int((len(ln) + cpl - 1) // cpl)) for ln in lines)
                max_h_pt = (h_pt * 0.92) / max(1.0, vis_lines * 1.22)
                if pt_sz > max_h_pt:
                    pt_sz = max_h_pt
        pt_sz = max(3.6, pt_sz)

        # Compensate for Google Slides' built-in 7.2pt horizontal (182,880 EMU) and 3.6pt vertical (91,440 EMU) textbox margins
        PAD_X_EMU = 91440
        PAD_Y_EMU = 45720
        text_target_id = obj_id
        if fill_hex is not None or stroke_hex is not None:
            text_target_id = f"{obj_id}_t"
            cx_emu = x_emu + w_emu // 2
            cy_emu = y_emu + h_emu // 2
            if is_compact_badge:
                tb_w = max(w_emu + 420000, len(clean_txt) * 125000 + 320000)
                tb_h = max(h_emu + 90000, 260000)
                tb_x = max(0, cx_emu - tb_w // 2)
                tb_y = max(0, cy_emu - tb_h // 2)
            elif shape_type == "ELLIPSE":
                inscribed_w = int(w_emu * 0.84) + PAD_X_EMU * 2
                inscribed_h = int(h_emu * 0.84) + PAD_Y_EMU * 2
                tb_w = max(127000, inscribed_w)
                tb_h = max(127000, inscribed_h)
                tb_x = max(0, cx_emu - tb_w // 2)
                tb_y = max(0, cy_emu - tb_h // 2)
            else:
                tb_w = w_emu + PAD_X_EMU * 2
                tb_h = h_emu + PAD_Y_EMU * 2
                tb_x = max(0, x_emu - PAD_X_EMU)
                tb_y = max(0, y_emu - PAD_Y_EMU)
            reqs.append(
                {
                    "createShape": {
                        "objectId": text_target_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {
                                "width": {"magnitude": int(tb_w), "unit": "EMU"},
                                "height": {"magnitude": int(tb_h), "unit": "EMU"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": int(tb_x),
                                "translateY": int(tb_y),
                                "unit": "EMU",
                            },
                        },
                    }
                }
            )
            reqs.append(
                {
                    "updateShapeProperties": {
                        "objectId": text_target_id,
                        "shapeProperties": {
                            "contentAlignment": "MIDDLE" if is_compact_badge else valign,
                            "shapeBackgroundFill": {"propertyState": "NOT_RENDERED"},
                            "outline": {"propertyState": "NOT_RENDERED"},
                        },
                        "fields": "contentAlignment,shapeBackgroundFill.propertyState,outline.propertyState",
                    }
                }
            )
        else:
            # Pure borderless text shape: widen/heighten in place to offset Google Slides' 7.2pt/3.6pt inset
            reqs[0]["createShape"]["elementProperties"]["size"]["width"]["magnitude"] = max(12700, int(w_emu + PAD_X_EMU * 2))
            reqs[0]["createShape"]["elementProperties"]["size"]["height"]["magnitude"] = max(12700, int(h_emu + PAD_Y_EMU * 2))
            reqs[0]["createShape"]["elementProperties"]["transform"]["translateX"] = max(0, int(x_emu - PAD_X_EMU))
            reqs[0]["createShape"]["elementProperties"]["transform"]["translateY"] = max(0, int(y_emu - PAD_Y_EMU))

        reqs.append(
            {
                "insertText": {
                    "objectId": text_target_id,
                    "text": clean_txt,
                }
            }
        )
        reqs.append(
            {
                "updateParagraphStyle": {
                    "objectId": text_target_id,
                    "textRange": {"type": "ALL"},
                    "style": {
                        "alignment": "CENTER" if is_compact_badge else align,
                        "lineSpacing": 100,
                        "spaceAbove": {"magnitude": 0.1, "unit": "PT"},
                        "spaceBelow": {"magnitude": 0.5 if len(lines) > 1 else 0.1, "unit": "PT"},
                    },
                    "fields": "alignment,lineSpacing,spaceAbove,spaceBelow",
                }
            }
        )
        if len(lines) >= 2:
            head_len = len(lines[0])
            head_col = "FFFFFF" if is_dark else (font_hex if font_hex != "0F172A" else "1E3A8A")
            body_col = "E2E8F0" if is_dark else "334155"
            head_pt = round(max(3.8, min(16.0, pt_sz * 1.06)), 1)
            body_pt = round(max(3.5, min(13.5, pt_sz * 0.90)), 1)
            reqs.append(
                {
                    "updateTextStyle": {
                        "objectId": text_target_id,
                        "textRange": {"type": "ALL"},
                        "style": {
                            "fontFamily": "Arial",
                            "fontSize": {"magnitude": head_pt, "unit": "PT"},
                            "bold": True,
                            "foregroundColor": {"opaqueColor": {"rgbColor": _hex_to_rgb_float(head_col)}},
                        },
                        "fields": "fontFamily,fontSize,bold,foregroundColor",
                    }
                }
            )
            if len(clean_txt) > head_len + 1:
                reqs.append(
                    {
                        "updateTextStyle": {
                            "objectId": text_target_id,
                            "textRange": {
                                "type": "FIXED_RANGE",
                                "startIndex": head_len + 1,
                                "endIndex": len(clean_txt),
                            },
                            "style": {
                                "fontFamily": "Arial",
                                "fontSize": {"magnitude": body_pt, "unit": "PT"},
                                "bold": False,
                                "foregroundColor": {"opaqueColor": {"rgbColor": _hex_to_rgb_float(body_col)}},
                            },
                            "fields": "fontFamily,fontSize,bold,foregroundColor",
                        }
                    }
                )
        else:
            single_pt = round(max(3.8, min(16.0, pt_sz * (0.90 if is_compact_badge else 1.0))), 1)
            reqs.append(
                {
                    "updateTextStyle": {
                        "objectId": text_target_id,
                        "textRange": {"type": "ALL"},
                        "style": {
                            "fontFamily": "Arial",
                            "fontSize": {"magnitude": single_pt, "unit": "PT"},
                            "bold": bool(force_bold_single or len(clean_txt) <= 42),
                            "foregroundColor": {"opaqueColor": {"rgbColor": _hex_to_rgb_float(font_hex)}},
                        },
                        "fields": "fontFamily,fontSize,bold,foregroundColor",
                    }
                }
            )
    return reqs


def _build_gslides_region_requests(
    slide_id: str,
    prefix: str,
    vertices: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    crop: Tuple[float, float, float, float],
    dest_emu: Tuple[int, int, int, int],
    emu_sx: float,
    emu_sy: float,
    font_scale: float = 1.0,
) -> List[Dict[str, Any]]:
    cx0, cy0, cw, ch = crop
    dx0, dy0, dw, dh = dest_emu
    sx = dw / max(cw, 1.0)
    sy = dh / max(ch, 1.0)
    scale = min(sx, sy)
    pad_x = dx0 + int((dw - cw * scale) / 2.0)
    pad_y = dy0 + int((dh - ch * scale) / 2.0)
    emu_s = min(emu_sx, emu_sy)

    reqs: List[Dict[str, Any]] = []
    seq = 0
    bg_containers, fg_cards = _partition_bg_and_fg_vertices(vertices, crop)

    def _emit_vertex_gslides(v: Dict[str, Any]) -> None:
        nonlocal seq
        seq += 1
        obj_id = f"{prefix}_n_{seq}"
        x_emu = int((pad_x + int((v["x"] - cx0) * scale)) * emu_sx)
        y_emu = int((pad_y + int((v["y"] - cy0) * scale)) * emu_sy)
        w_emu = max(18000, int(v["w"] * scale * emu_sx))
        h_emu = max(18000, int(v["h"] * scale * emu_sy))

        st = v["style"]
        is_text_only = "text" in st and "fillColor" not in st and "strokeColor" not in st
        fill_hex = None if is_text_only else _clean_hex(st.get("fillColor"), "FFFFFF")
        stroke_hex = None if is_text_only else _clean_hex(st.get("strokeColor"), "CBD5E1")
        is_dark = _is_dark_hex(fill_hex)
        default_font = "FFFFFF" if is_dark else "0F172A"
        font_hex = _clean_hex(st.get("fontColor"), default_font) or default_font
        shape_type = _gslides_shape_type(st)

        sw_px = float(st.get("strokeWidth", 1.2) or 1.2)
        ln_w = max(9525, min(38100, int(sw_px * 9525 * emu_s)))
        raw_fs = float(st.get("fontSize", 11.5) or 11.5)
        pt_sz = max(4.2, min(16.5, raw_fs * (scale / 9525.0) * 0.88 * font_scale * emu_s))

        align_map = {"left": "START", "center": "CENTER", "right": "END"}
        algn = align_map.get(st.get("align", "center"), "CENTER")
        valign_map = {"top": "TOP", "middle": "MIDDLE", "bottom": "BOTTOM"}
        valgn = valign_map.get(st.get("verticalAlign", "middle"), "MIDDLE")

        if is_text_only and "\n" not in v["text"] and algn == "START":
            w_emu = max(w_emu, int((len(v["text"]) * 145000 + 260000) * emu_s))
        if v["w"] >= cw * 0.85 and v["h"] <= 56.0 and "\n" not in v["text"] and len(v["text"]) > 40:
            max_banner_pt = max(5.5, ((w_emu / 12700.0) - 18.0) / max(1.0, len(v["text"]) * 0.62))
            pt_sz = min(pt_sz, max_banner_pt)

        reqs.extend(
            _make_gslides_shape_With_text_reqs(
                obj_id=obj_id,
                slide_id=slide_id,
                shape_type=shape_type,
                x_emu=x_emu,
                y_emu=y_emu,
                w_emu=w_emu,
                h_emu=h_emu,
                fill_hex=fill_hex,
                stroke_hex=stroke_hex,
                stroke_emu=ln_w,
                dashed=(st.get("dashed") == "1"),
                text_str=v["text"],
                pt_sz=pt_sz,
                align=algn,
                valign=valgn,
                font_hex=font_hex,
                force_bold_single=(st.get("fontStyle") in ("1", "3", "5")),
            )
        )

    # Pass 1: Background section bands & containers
    for v in bg_containers:
        _emit_vertex_gslides(v)

    # Pass 2: Strictly orthogonal STRAIGHT lines (scaleX=1, scaleY=1, 0 diagonal distortions)
    edge_label_reqs: List[Dict[str, Any]] = []
    for e in edges:
        pts = e["points"]
        if any(px < cx0 - 8 or px > cx0 + cw + 8 or py < cy0 - 8 or py > cy0 + ch + 8 for (px, py) in pts):
            continue
        emu_pts = [
            (int((pad_x + int((px - cx0) * scale)) * emu_sx), int((pad_y + int((py - cy0) * scale)) * emu_sy))
            for (px, py) in pts
        ]
        st = e["style"]
        stroke_hex = _clean_hex(st.get("strokeColor"), "2554B0") or "2554B0"
        sw_px = float(st.get("strokeWidth", 1.8) or 1.8)
        ln_w = max(12700, min(32000, int(sw_px * 9525 * emu_s)))
        is_dashed = st.get("dashed") == "1"
        end_arrow_raw = st.get("endArrow", "classic")
        start_arrow_raw = st.get("startArrow", "none")

        num_segs = len(emu_pts) - 1
        for seg_idx in range(num_segs):
            (x1, y1), (x2, y2) = emu_pts[seg_idx], emu_pts[seg_idx + 1]
            if abs(x2 - x1) < 6000 and abs(y2 - y1) < 6000:
                continue
            s_arr = "FILL_ARROW" if (seg_idx == 0 and start_arrow_raw not in ("none", "")) else "NONE"
            e_arr = "FILL_ARROW" if (seg_idx == num_segs - 1 and end_arrow_raw != "none") else "NONE"

            if abs(x2 - x1) >= abs(y2 - y1):
                mid_y = (y1 + y2) // 2
                if x2 < x1:
                    x1, x2 = x2, x1
                    s_arr, e_arr = e_arr, s_arr
                w_mag = max(12700, x2 - x1)
                h_mag = 12700
                tx, ty = x1, mid_y
            else:
                mid_x = (x1 + x2) // 2
                if y2 < y1:
                    y1, y2 = y2, y1
                    s_arr, e_arr = e_arr, s_arr
                w_mag = 12700
                h_mag = max(12700, y2 - y1)
                tx, ty = mid_x, y1

            seq += 1
            line_id = f"{prefix}_l_{seq}"
            reqs.append(
                {
                    "createLine": {
                        "objectId": line_id,
                        "category": "STRAIGHT",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {
                                "width": {"magnitude": w_mag, "unit": "EMU"},
                                "height": {"magnitude": h_mag, "unit": "EMU"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": max(0, tx),
                                "translateY": max(0, ty),
                                "unit": "EMU",
                            },
                        },
                    }
                }
            )
            reqs.append(
                {
                    "updateLineProperties": {
                        "objectId": line_id,
                        "lineProperties": {
                            "lineFill": {"solidFill": {"color": {"rgbColor": _hex_to_rgb_float(stroke_hex)}}},
                            "weight": {"magnitude": ln_w, "unit": "EMU"},
                            "dashStyle": "DASH" if is_dashed else "SOLID",
                            "startArrow": s_arr,
                            "endArrow": e_arr,
                        },
                        "fields": "lineFill,weight,dashStyle,startArrow,endArrow",
                    }
                }
            )

        if e["text"]:
            seq += 1
            mid_idx = len(emu_pts) // 2
            mx, my = emu_pts[mid_idx]
            lbl_w = max(int(520000 * emu_sx), min(int(1750000 * emu_sx), int(len(e["text"]) * 60000 * emu_sx)))
            lbl_h = max(180000, int(228600 * emu_sy))
            edge_label_reqs.extend(
                _make_gslides_shape_With_text_reqs(
                    obj_id=f"{prefix}_el_{seq}",
                    slide_id=slide_id,
                    shape_type="ROUND_RECTANGLE",
                    x_emu=max(0, mx - lbl_w // 2),
                    y_emu=max(0, my - lbl_h // 2),
                    w_emu=lbl_w,
                    h_emu=lbl_h,
                    fill_hex="FFFFFF",
                    stroke_hex=stroke_hex,
                    stroke_emu=9525,
                    dashed=False,
                    text_str=e["text"],
                    pt_sz=max(6.5, 7.8 * emu_s),
                    align="CENTER",
                    valign="MIDDLE",
                    font_hex="0F172A",
                    force_bold_single=True,
                )
            )

    # Pass 3: Foreground cards, pills, badges & edge labels
    for v in fg_cards:
        _emit_vertex_gslides(v)
    reqs.extend(edge_label_reqs)
    return reqs


def _sync_via_gslides_cli(tid: str, title: str, existing_id: Optional[str]) -> str:
    drawio_path = DRAWIO_DIR / f"{tid}.drawio"
    if not drawio_path.exists():
        drawio_path = GALLERY_DIR / f"{tid}.drawio"
    parsed = parse_drawio(drawio_path)
    page_w = parsed["page_w"]
    page_h = parsed["page_h"]
    bg_hex = parsed["bg_hex"]
    vertices = parsed["vertices"]
    edges = parsed["edges"]
    bands = _detect_section_bands(vertices, page_w)
    total_slides = 1 + (len(bands) if len(bands) >= 2 else 2)

    deck_name = f"{tid} — {title} (Editable Google Slides)"
    pres_id = existing_id if (existing_id and len(str(existing_id)) >= 40) else None
    if not pres_id:
        cr = subprocess.run(
            [str(GSLIDES_BIN), "mutate", "create", "--title", deck_name],
            capture_output=True,
            text=True,
            check=True,
        )
        m_id = re.search(r"\(ID:\s*([A-Za-z0-9_-]+)\)", cr.stdout)
        if m_id:
            pres_id = m_id.group(1)
        else:
            cr_json = json.loads(cr.stdout[cr.stdout.find("{") :])
            pres_id = str(cr_json.get("presentationId") or cr_json.get("id"))
        subprocess.run(
            [str(GSLIDES_BIN), "mutate", "share", pres_id, "--role", "reader", "--type", "domain", "--domain", "google.com"],
            capture_output=True,
            text=True,
            check=False,
        )

    info_res = subprocess.run(
        [str(GSLIDES_BIN), "readonly", "info", pres_id, "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    info_json = json.loads(info_res.stdout[info_res.stdout.find("{") :])
    ps = info_json.get("pageSize") or {}
    pres_w_emu = float((ps.get("width") or {}).get("magnitude") or SLIDE_W_EMU)
    pres_h_emu = float((ps.get("height") or {}).get("magnitude") or SLIDE_H_EMU)
    emu_sx = pres_w_emu / SLIDE_W_EMU
    emu_sy = pres_h_emu / SLIDE_H_EMU
    emu_s = min(emu_sx, emu_sy)
    old_slide_ids = [str(s["objectId"]) for s in (info_json.get("slides") or []) if s.get("objectId")]
    layouts = info_json.get("layouts") or []
    slide_layout_ref = (
        {"layoutId": str(layouts[0]["objectId"])}
        if layouts and layouts[0].get("objectId")
        else {"predefinedLayout": "BLANK"}
    )

    run_tag = uuid.uuid4().hex[:6]
    all_reqs: List[Dict[str, Any]] = []

    def _add_slide_chrome(sid: str, pfx: str, subtitle: str, s_idx: int, slide_bg: str) -> None:
        all_reqs.append(
            {
                "createSlide": {
                    "objectId": sid,
                    "slideLayoutReference": slide_layout_ref,
                }
            }
        )
        all_reqs.append(
            {
                "updatePageProperties": {
                    "objectId": sid,
                    "pageProperties": {
                        "pageBackgroundFill": {
                            "solidFill": {"color": {"rgbColor": _hex_to_rgb_float(slide_bg)}}
                        }
                    },
                    "fields": "pageBackgroundFill.solidFill.color",
                }
            }
        )
        # Top banner
        all_reqs.extend(
            _make_gslides_shape_With_text_reqs(
                obj_id=f"{pfx}_hdr",
                slide_id=sid,
                shape_type="RECTANGLE",
                x_emu=int(320000 * emu_sx),
                y_emu=int(140000 * emu_sy),
                w_emu=int(9200000 * emu_sx),
                h_emu=int(560000 * emu_sy),
                fill_hex=None,
                stroke_hex=None,
                stroke_emu=0,
                dashed=False,
                text_str=f"{tid} — {title}\n{subtitle}",
                pt_sz=12.5 * emu_s,
                align="START",
                valign="TOP",
                font_hex="0F172A",
            )
        )
        # Green native badge
        all_reqs.extend(
            _make_gslides_shape_With_text_reqs(
                obj_id=f"{pfx}_bdg",
                slide_id=sid,
                shape_type="ROUND_RECTANGLE",
                x_emu=int(9620000 * emu_sx),
                y_emu=int(190000 * emu_sy),
                w_emu=int(2250000 * emu_sx),
                h_emu=int(320000 * emu_sy),
                fill_hex="ECFDF5",
                stroke_hex="10B981",
                stroke_emu=int(12700 * emu_s),
                dashed=False,
                text_str="100% Native Editable Shapes",
                pt_sz=8.5 * emu_s,
                align="CENTER",
                valign="MIDDLE",
                font_hex="065F46",
                force_bold_single=True,
            )
        )
        # Footer bar
        all_reqs.extend(
            _make_gslides_shape_With_text_reqs(
                obj_id=f"{pfx}_ftr",
                slide_id=sid,
                shape_type="RECTANGLE",
                x_emu=int(320000 * emu_sx),
                y_emu=int(6480000 * emu_sy),
                w_emu=int(11550000 * emu_sx),
                h_emu=int(260000 * emu_sy),
                fill_hex=None,
                stroke_hex=None,
                stroke_emu=0,
                dashed=False,
                text_str=f"Proprietary + Confidential  |  Cloudstyle 2.0 Canonical Blueprint ({tid})  |  Slide {s_idx} of {total_slides}",
                pt_sz=8.2 * emu_s,
                align="START",
                valign="MIDDLE",
                font_hex="64748B",
                force_bold_single=True,
            )
        )

    # Slide 1: Full-Poster Overview + Right Executive Design Rail
    s1_id = f"s1_{run_tag}"
    p1_fx = f"p1_{run_tag}"
    _add_slide_chrome(
        s1_id,
        p1_fx,
        "Slide 1: Complete Cloudstyle 2.0 Native Editable Blueprint Overview",
        1,
        "F8FAFC" if bg_hex == "FFFFFF" else bg_hex,
    )
    if page_h > page_w * 0.92:
        all_reqs.extend(
            _build_gslides_region_requests(
                s1_id,
                p1_fx,
                vertices,
                edges,
                (0.0, 0.0, page_w, page_h),
                (320000, 760000, 7820000, 5620000),
                emu_sx,
                emu_sy,
                font_scale=1.08,
            )
        )
        rail_cards = [
            ("DESIGN INVARIANT — Canonical Geometry", f"Compiled from {tid}.drawio with zero text collisions and 100% orthogonal vector connectors.", "2563EB", 780000),
            ("PRODUCTION STACK — Google Cloud ADK ⇄ OSS", "Vertex AI Gemini 4 Argon / 3.8 Flash (locations/global) + Model Armor + OpenHands.", "059669", 2680000),
            ("CAREER & SLO IMPACT — Staff+ Proof Telemetry", "100% editable shapes in Google Slides & PowerPoint for executive & customer reviews.", "7C3AED", 4580000),
        ]
        for r_idx, (r_head, r_body, r_col, ry) in enumerate(rail_cards, start=1):
            all_reqs.extend(
                _make_gslides_shape_With_text_reqs(
                    obj_id=f"{p1_fx}_rail_{r_idx}",
                    slide_id=s1_id,
                    shape_type="ROUND_RECTANGLE",
                    x_emu=int(8320000 * emu_sx),
                    y_emu=int(ry * emu_sy),
                    w_emu=int(3550000 * emu_sx),
                    h_emu=int(1740000 * emu_sy),
                    fill_hex="FFFFFF",
                    stroke_hex=r_col,
                    stroke_emu=int(15875 * emu_s),
                    dashed=False,
                    text_str=f"{r_head}\n{r_body}",
                    pt_sz=10.5 * emu_s,
                    align="START",
                    valign="MIDDLE",
                    font_hex=r_col,
                )
            )
    else:
        all_reqs.extend(
            _build_gslides_region_requests(
                s1_id,
                p1_fx,
                vertices,
                edges,
                (0.0, 0.0, page_w, page_h),
                (320000, 760000, 11550000, 5620000),
                emu_sx,
                emu_sy,
                font_scale=1.05,
            )
        )

    if len(bands) >= 2:
        for b_idx, band in enumerate(bands, start=2):
            sb_id = f"s{b_idx}_{run_tag}"
            pb_fx = f"p{b_idx}_{run_tag}"
            _add_slide_chrome(
                sb_id,
                pb_fx,
                f"Slide {b_idx}: Widescreen Section Band {b_idx - 1:02d} Native Architecture Zoom",
                b_idx,
                "F8FAFC",
            )
            all_reqs.extend(
                _build_gslides_region_requests(
                    sb_id,
                    pb_fx,
                    vertices,
                    edges,
                    (max(0.0, band["x"] - 24.0), max(0.0, band["y"] - 12.0), min(page_w, band["w"] + 48.0), band["h"] + 24.0),
                    (320000, 820000, 11550000, 5520000),
                    emu_sx,
                    emu_sy,
                    font_scale=1.25,
                )
            )
    else:
        s2_id = f"s2_{run_tag}"
        p2_fx = f"p2_{run_tag}"
        _add_slide_chrome(
            s2_id,
            p2_fx,
            "Slide 2: Upper Architecture Stage 16:9 Widescreen Editable Vector Zoom",
            2,
            "FFFFFF",
        )
        all_reqs.extend(
            _build_gslides_region_requests(
                s2_id,
                p2_fx,
                vertices,
                edges,
                (0.0, 0.0, page_w, page_h * 0.58),
                (280000, 760000, 11630000, 5640000),
                emu_sx,
                emu_sy,
                font_scale=1.22,
            )
        )
        s3_id = f"s3_{run_tag}"
        p3_fx = f"p3_{run_tag}"
        _add_slide_chrome(
            s3_id,
            p3_fx,
            "Slide 3: Lower Execution & Telemetry 16:9 Widescreen Editable Vector Zoom",
            3,
            "F8FAFC",
        )
        all_reqs.extend(
            _build_gslides_region_requests(
                s3_id,
                p3_fx,
                vertices,
                edges,
                (0.0, page_h * 0.42, page_w, page_h * 0.58),
                (280000, 760000, 11630000, 5640000),
                emu_sx,
                emu_sy,
                font_scale=1.22,
            )
        )

    for old_sid in old_slide_ids:
        all_reqs.append({"deleteObject": {"objectId": old_sid}})

    SCRATCH_BATCH_DIR.mkdir(parents=True, exist_ok=True)
    chunk_size = 500
    for c_idx in range(0, len(all_reqs), chunk_size):
        chunk = all_reqs[c_idx : c_idx + chunk_size]
        batch_file = SCRATCH_BATCH_DIR / f"gslides_batch_{tid}_{c_idx // chunk_size}.json"
        batch_file.write_text(json.dumps({"requests": chunk}), encoding="utf-8")
        subprocess.run(
            [str(GSLIDES_BIN), "mutate", "raw-batch", pres_id, "--file", str(batch_file)],
            capture_output=True,
            text=True,
            check=True,
        )
    return pres_id


def _upload_pptx_to_google_slides(
    pptx_path: Path, pptx_buf: bytes, tid: str, title: str, existing_id: Optional[str], token: Optional[str]
) -> str:
    if GSLIDES_BIN.exists():
        return _sync_via_gslides_cli(tid, title, existing_id)
    deck_name = f"{tid} — {title} (Editable Google Slides)"
    if token:
        boundary = f"----TemplateSlidesBridge{uuid.uuid4().hex}"
        meta_json = json.dumps(
            {"name": deck_name, "mimeType": "application/vnd.google-apps.presentation"}
        ).encode("utf-8")
        body = (
            f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode("utf-8")
            + meta_json
            + f"\r\n--{boundary}\r\nContent-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n\r\n".encode("utf-8")
            + pptx_buf
            + f"\r\n--{boundary}--\r\n".encode("utf-8")
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "x-goog-user-project": QUOTA_PROJECT,
            "Content-Type": f"multipart/related; boundary={boundary}",
        }
        if existing_id:
            try:
                patch_req = urllib.request.Request(
                    f"https://www.googleapis.com/upload/drive/v3/files/{existing_id}?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink",
                    data=body,
                    headers=headers,
                    method="PATCH",
                )
                with urllib.request.urlopen(patch_req, timeout=45) as resp:
                    return str(json.loads(resp.read().decode("utf-8"))["id"])
            except Exception:
                pass
        post_req = urllib.request.Request(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink",
            data=body,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(post_req, timeout=45) as resp:
            return str(json.loads(resp.read().decode("utf-8"))["id"])

    if GDRIVE_BIN.exists():
        if existing_id:
            upd = subprocess.run(
                [str(GDRIVE_BIN), "mutate", "update", existing_id, str(pptx_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            if upd.returncode == 0:
                return existing_id
        res = subprocess.run(
            [str(GDRIVE_BIN), "mutate", "upload", str(pptx_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        m = re.search(r"\(ID:\s*([A-Za-z0-9_-]+)\)", res.stdout)
        if not m:
            raise RuntimeError(f"Unexpected gdrive mutate upload output: {res.stdout} {res.stderr}")
        fid = m.group(1)
        subprocess.run(
            [str(GDRIVE_BIN), "mutate", "rename", fid, deck_name],
            capture_output=True,
            text=True,
            check=False,
        )
        return fid

    raise RuntimeError("Neither refresh_token nor gdrive CLI available for Google Slides upload")


def main() -> None:
    args = sys.argv[1:]
    local_pptx_only = "--local-pptx-only" in args
    all_drawio = "--all-drawio" in args
    skip_existing = "--skip-existing" in args
    force = "--force" in args

    only_tids: List[str] = []
    if "--only" in args:
        idx = args.index("--only")
        if idx + 1 < len(args):
            only_tids.append(args[idx + 1])
    for i, a in enumerate(args):
        if re.fullmatch(r"T\d+", a) and (i == 0 or args[i - 1] != "--only"):
            only_tids.append(a)

    if only_tids:
        target_tids = list(dict.fromkeys(only_tids))
    elif all_drawio:
        target_tids = sorted(
            [p.stem for p in DRAWIO_DIR.glob("T*.drawio")],
            key=lambda t: int(t[1:]),
        )
    else:
        target_tids = ["T01"] + [f"T{i}" for i in range(53, 90)]

    sys.path.insert(0, str(IDEAS_ROOT))
    title_by_tid: Dict[str, str] = {}
    try:
        from src.visuals.canonical_template_registry import TEMPLATE_META, TOPIC_POSTS_T79

        for k, v in TEMPLATE_META.items():
            title_by_tid[k] = v["name"]
        for tp in TOPIC_POSTS_T79:
            title_by_tid[tp["id"]] = tp.get("title") or tp.get("name", tp["id"])
    except Exception:
        pass

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    manifest: Dict[str, Any] = {
        "updatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "accountEmail": "nitinagga@google.com",
        "slides": {},
    }
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    token = None if local_pptx_only else _get_refresh_access_token()

    for tid in target_tids:
        existing_pptx = GALLERY_DIR / f"{tid}.pptx"
        if skip_existing and existing_pptx.exists() and not force:
            continue
        title = title_by_tid.get(tid, f"{tid} Editable Architecture Blueprint")
        pptx_path, pptx_buf, slide_count = compile_drawio_to_pptx(tid, title)
        if local_pptx_only:
            print(f"[local_pptx] {tid} ({slide_count} editable slides, {len(pptx_buf)}B) -> {pptx_path}")
            continue

        sha256 = hashlib.sha256(pptx_buf).hexdigest()
        existing = (manifest.get("slides") or {}).get(tid) or {}
        slide_id = existing.get("googleSlidesId")
        if not slide_id or existing.get("sha256") != sha256 or force:
            slide_id = _upload_pptx_to_google_slides(pptx_path, pptx_buf, tid, title, slide_id, token)

        entry = {
            "tid": tid,
            "title": title,
            "pptxFile": f"{tid}.pptx",
            "slideCount": slide_count,
            "sizeBytes": len(pptx_buf),
            "sha256": sha256,
            "googleSlidesId": slide_id,
            "googleSlidesEditUrl": f"https://docs.google.com/presentation/d/{slide_id}/edit?authuser=nitinagga%40google.com",
            "googleSlidesPreviewUrl": f"https://docs.google.com/presentation/d/{slide_id}/preview",
            "googleSlidesEmbedUrl": f"https://docs.google.com/presentation/d/{slide_id}/embed?start=false&loop=false&delayms=5000",
            "googleSlidesPdfUrl": f"https://docs.google.com/presentation/d/{slide_id}/export/pdf",
            "syncedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        manifest.setdefault("slides", {})[tid] = entry
        print(f"[slides_sync] {tid} ({slide_count} editable slides, {len(pptx_buf)}B) -> {entry['googleSlidesEditUrl']}")

    if not local_pptx_only:
        manifest["updatedAt"] = dt.datetime.now(dt.timezone.utc).isoformat()
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Enrich gallery_manifest.json if present
    gm_path = GALLERY_DIR / "gallery_manifest.json"
    if gm_path.exists():
        gm = json.loads(gm_path.read_text(encoding="utf-8"))
        slides_dict = manifest.get("slides") or {}
        for t in gm.get("templates") or []:
            t.setdefault("files", {})
            if (GALLERY_DIR / f"{t['id']}.drawio").exists():
                t["files"]["drawio"] = f"{t['id']}.drawio"
            if (GALLERY_DIR / f"{t['id']}.pptx").exists():
                t["files"]["pptx"] = f"{t['id']}.pptx"
            sm = slides_dict.get(t["id"])
            if sm:
                t["google_slides_id"] = sm["googleSlidesId"]
                t["google_slides_url"] = sm["googleSlidesEditUrl"]
                t["google_slides_preview_url"] = sm["googleSlidesPreviewUrl"]
                t["editable_slide_count"] = sm["slideCount"]
            for tp in t.get("topic_posts") or []:
                tp.setdefault("files", {})
                if (GALLERY_DIR / f"{tp['id']}.drawio").exists():
                    tp["files"]["drawio"] = f"{tp['id']}.drawio"
                if (GALLERY_DIR / f"{tp['id']}.pptx").exists():
                    tp["files"]["pptx"] = f"{tp['id']}.pptx"
                tsm = slides_dict.get(tp["id"])
                if tsm:
                    tp["google_slides_id"] = tsm["googleSlidesId"]
                    tp["google_slides_url"] = tsm["googleSlidesEditUrl"]
                    tp["google_slides_preview_url"] = tsm["googleSlidesPreviewUrl"]
                    tp["editable_slide_count"] = tsm["slideCount"]
        gm_path.write_text(json.dumps(gm, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
