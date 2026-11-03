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


def _strip_html(raw: str) -> str:
    txt = str(raw or "")
    txt = re.sub(r"&lt;svg[\s\S]*?&lt;/svg&gt;", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"<svg[\s\S]*?</svg>", " ", txt, flags=re.IGNORECASE)
    txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</(?:div|p|li|tr|h[1-6])>", "\n", txt, flags=re.IGNORECASE)
    txt = re.sub(r"</?[a-zA-Z][^>]*>", " ", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"</?[a-zA-Z][^>]*>", " ", txt)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in txt.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines[:6])


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

    for cell in gm.findall(".//mxCell"):
        cid = cell.attrib.get("id", "")
        if cid in ("0", "1"):
            continue
        style = _parse_style(cell.attrib.get("style", ""))
        val_raw = cell.attrib.get("value", "")
        text = _strip_html(val_raw)
        geom = cell.find("mxGeometry")
        ox, oy = _parent_offset(cell.attrib.get("parent"))

        if cell.attrib.get("vertex") == "1" and geom is not None:
            if geom.attrib.get("relative") == "1":
                # Edge child label or relative badge
                parent_cell = cells_by_id.get(cell.attrib.get("parent", ""))
                if parent_cell is not None and parent_cell.attrib.get("edge") == "1":
                    continue
            x = float(geom.attrib.get("x", 0.0)) + ox
            y = float(geom.attrib.get("y", 0.0)) + oy
            w = float(geom.attrib.get("width", 0.0))
            h = float(geom.attrib.get("height", 0.0))
            if w <= 1.0 and h <= 1.0:
                continue
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
            pts: List[Tuple[float, float]] = []
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

    # Compute tight bounding box if vertices exceed page_w/page_h
    if vertices:
        max_r = max(v["x"] + v["w"] for v in vertices)
        max_b = max(v["y"] + v["h"] for v in vertices)
        page_w = max(page_w, max_r + 24.0)
        page_h = max(page_h, max_b + 24.0)

    v_map = {v["id"]: v for v in vertices}
    resolved_edges: List[Dict[str, Any]] = []
    for e in edges:
        pts: List[Tuple[float, float]] = []
        if e["source"] and e["source"] in v_map:
            sv = v_map[e["source"]]
            ex = float(e["style"].get("exitX", 0.5))
            ey = float(e["style"].get("exitY", 0.5))
            pts.append((sv["x"] + sv["w"] * ex, sv["y"] + sv["h"] * ey))
        elif e["source_pt"] is not None:
            pts.append(e["source_pt"])

        pts.extend(e["waypoints"])

        if e["target"] and e["target"] in v_map:
            tv = v_map[e["target"]]
            nx = float(e["style"].get("entryX", 0.5))
            ny = float(e["style"].get("entryY", 0.5))
            pts.append((tv["x"] + tv["w"] * nx, tv["y"] + tv["h"] * ny))
        elif e["target_pt"] is not None:
            pts.append(e["target_pt"])

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

    for v in vertices:
        # Skip huge full-page canvas wrapper if identical to page background
        if v["w"] >= cw * 0.97 and v["h"] >= ch * 0.95 and not v["text"]:
            continue
        vx2 = v["x"] + v["w"]
        vy2 = v["y"] + v["h"]
        if vx2 < cx0 + 2 or v["x"] > cx0 + cw - 2 or vy2 < cy0 + 2 or v["y"] > cy0 + ch - 2:
            continue

        x_emu = max(0, pad_x + int((v["x"] - cx0) * scale))
        y_emu = max(0, pad_y + int((v["y"] - cy0) * scale))
        w_emu = max(25400, int(v["w"] * scale))
        h_emu = max(25400, int(v["h"] * scale))

        st = v["style"]
        fill_hex = _clean_hex(st.get("fillColor"), "FFFFFF")
        stroke_hex = _clean_hex(st.get("strokeColor"), "CBD5E1")
        font_hex = _clean_hex(st.get("fontColor"), "0F172A") or "0F172A"
        prst = _shape_preset(st)

        fill_xml = f'<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill>' if fill_hex else "<a:noFill/>"
        if stroke_hex:
            sw_px = float(st.get("strokeWidth", 1.2) or 1.2)
            ln_w = max(9525, min(38100, int(sw_px * 9525)))
            dash_xml = '<a:prstDash val="dash"/>' if st.get("dashed") == "1" else ""
            ln_xml = f'<a:ln w="{ln_w}"><a:solidFill><a:srgbClr val="{stroke_hex}"/></a:solidFill>{dash_xml}</a:ln>'
        else:
            ln_xml = "<a:ln><a:noFill/></a:ln>"

        raw_fs = float(st.get("fontSize", 11.0) or 11.0)
        pt_sz = max(7.5, min(20.0, raw_fs * (scale / 9525.0) * 0.92 * font_scale))
        sz_hundredths = int(round(pt_sz * 100))
        is_bold = "1" if (st.get("fontStyle") in ("1", "3", "5") or "<b>" in str(st) or len(v["text"]) <= 28) else "0"
        align_map = {"left": "l", "center": "ctr", "right": "r"}
        algn = align_map.get(st.get("align", "center"), "ctr")
        valign_map = {"top": "t", "middle": "ctr", "bottom": "b"}
        anchor = valign_map.get(st.get("verticalAlign", "middle"), "ctr")

        if v["text"]:
            p_Xml = "\n".join(
                f'              <a:p><a:pPr algn="{algn}"/><a:r><a:rPr lang="en-US" sz="{sz_hundredths}" b="{is_bold}"><a:solidFill><a:srgbClr val="{font_hex}"/></a:solidFill></a:rPr><a:t>{_xml_esc(ln)}</a:t></a:r></a:p>'
                for ln in v["text"].split("\n")
            )
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

    # Native editable polyline connectors (`<a:custGeom>` with canonical positive coordinates, flipH=0, flipV=0)
    for e in edges:
        pts = e["points"]
        if any(px < cx0 - 8 or px > cx0 + cw + 8 or py < cy0 - 8 or py > cy0 + ch + 8 for (px, py) in pts):
            continue
        emu_pts = [(pad_x + int((px - cx0) * scale), pad_y + int((py - cy0) * scale)) for (px, py) in pts]
        min_x = min(p[0] for p in emu_pts)
        min_y = min(p[1] for p in emu_pts)
        max_x = max(p[0] for p in emu_pts)
        max_y = max(p[1] for p in emu_pts)
        ext_w = max(12700, max_x - min_x)
        ext_h = max(12700, max_y - min_y)

        st = e["style"]
        stroke_hex = _clean_hex(st.get("strokeColor"), "475569") or "475569"
        sw_px = float(st.get("strokeWidth", 1.8) or 1.8)
        ln_w = max(12700, min(38100, int(sw_px * 9525)))
        dash_xml = '<a:prstDash val="dash"/>' if st.get("dashed") == "1" else ""
        end_arrow = st.get("endArrow", "classic")
        tail_xml = '<a:tailEnd type="triangle" w="med" len="med"/>' if end_arrow != "none" else ""
        start_arrow = st.get("startArrow", "none")
        head_xml = '<a:headEnd type="triangle" w="med" len="med"/>' if start_arrow not in ("none", "") else ""

        rel_pts = [(p[0] - min_x, p[1] - min_y) for p in emu_pts]
        path_cmds = [f'<a:moveTo><a:pt x="{rel_pts[0][0]}" y="{rel_pts[0][1]}"/></a:moveTo>']
        for rx, ry in rel_pts[1:]:
            path_cmds.append(f'<a:lnTo><a:pt x="{rx}" y="{ry}"/></a:lnTo>')

        shapes.append(
            f"        <p:sp>\n"
            f'          <p:nvSpPr><p:cNvPr id="{next_id}" name="Edge_{next_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>\n'
            f"          <p:spPr>\n"
            f'            <a:xfrm><a:off x="{min_x}" y="{min_y}"/><a:ext cx="{ext_w}" cy="{ext_h}"/></a:xfrm>\n'
            f"            <a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l=\"l\" t=\"t\" r=\"r\" b=\"b\"/>"
            f'<a:pathLst><a:path w="{ext_w}" h="{ext_h}">{"".join(path_cmds)}</a:path></a:pathLst></a:custGeom>\n'
            f"            <a:noFill/>\n"
            f'            <a:ln w="{ln_w}"><a:solidFill><a:srgbClr val="{stroke_hex}"/></a:solidFill>{dash_xml}{head_xml}{tail_xml}</a:ln>\n'
            f"          </p:spPr>\n"
            f'          <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>\n'
            f"        </p:sp>"
        )
        next_id += 1

        if e["text"]:
            mid_idx = len(emu_pts) // 2
            mx, my = emu_pts[mid_idx]
            lbl_w = max(540000, min(1800000, len(e["text"]) * 62000))
            lbl_h = 228600
            lx = max(0, mx - lbl_w // 2)
            ly = max(0, my - lbl_h // 2)
            shapes.append(
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
    total_slides = 1 + (len(bands) if len(bands) >= 2 else 1)

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
        # Slide 2: Full-Bleed Widescreen Vector Zoom
        zoom_shapes, _ = _render_region_shapes_xml(
            vertices,
            edges,
            (0.0, 0.0, page_w, page_h),
            (280000, 760000, 11630000, 5640000),
            start_id=10,
            font_scale=1.18,
        )
        s2_shapes = _header_and_footer_shapes(
            tid,
            title,
            "Slide 2: Full-Width 16:9 Widescreen Editable Vector Canvas",
            2,
            total_slides,
        ) + zoom_shapes
        slide_xmls.append(_wrap_slide_xml("FFFFFF", s2_shapes))

    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    out_pptx = GALLERY_DIR / f"{tid}.pptx"
    with zipfile.ZipFile(out_pptx, "w", zipfile.ZIP_DEFLATED) as zf:
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


def _upload_pptx_to_google_slides(
    pptx_path: Path, pptx_buf: bytes, tid: str, title: str, existing_id: Optional[str], token: Optional[str]
) -> str:
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
