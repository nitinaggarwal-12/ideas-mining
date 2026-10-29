#!/usr/bin/env python3
"""Deterministic Canonical Draw.io XML Generator for Templates T79-T84 (6 Daily LinkedIn Creator Archetypes).

Enforces Rule 54 (Universal Light Theme #F8FAFC/#FFFFFF), Rule 57A (1-First Prototype Gate via --only T79),
Rule 57B/57C (1020x1040 proportional spine, >=76px horizontal & >=44px vertical visible arrow shafts,
2px knockout cushion `padding:0 2px;`, calibrated `<mxPoint as="offset"/>`, full-width 842px PROMPT tables,
zero typos, and zero forbidden vendor strings).
"""

from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Any, Dict, List

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DRAWIO_DIR = WORKSPACE_ROOT / "assets" / "canonical-ref" / "drawio"


def _attr(raw: str) -> str:
    """Escape HTML markup for placement inside an XML double-quoted attribute."""
    return (
        raw.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _prompt_bar_val(prompt_text: str) -> str:
    inner = (
        '<table style="width:842px;border-collapse:collapse;font-family:Inter,sans-serif;">'
        "<tr>"
        '<td style="width:62px;text-align:left;vertical-align:middle;">'
        '<span style="font-size:10.5px;font-weight:800;color:#64748B;letter-spacing:0.5px;">PROMPT</span>'
        "</td>"
        f'<td style="text-align:left;vertical-align:middle;font-size:12px;color:#0F172A;font-weight:500;">{html.escape(prompt_text)}</td>'
        '<td style="width:30px;text-align:right;vertical-align:middle;">'
        '<span style="display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;'
        'background:#0F172A;color:#FFFFFF;border-radius:999px;font-weight:800;font-size:12px;">↑</span>'
        "</td>"
        "</tr>"
        "</table>"
    )
    return _attr(inner)


def _pill_pair_val(width_px: int, left_bold: str, right_tag: str, right_color: str) -> str:
    inner = (
        f'<table style="width:{width_px}px;border-collapse:collapse;font-family:Inter,sans-serif;">'
        "<tr>"
        f'<td style="text-align:left;"><b style="color:#0F172A;font-size:11.5px;">{html.escape(left_bold)}</b></td>'
        f'<td style="text-align:right;color:{right_color};font-size:11px;font-weight:700;">{html.escape(right_tag)}</td>'
        "</tr>"
        "</table>"
    )
    return _attr(inner)


def _score_rows_val(rows: List[Dict[str, Any]], stack_footer: str) -> str:
    trs: List[str] = []
    for r in rows:
        bar_w = max(12, min(78, int(round(78 * float(r["ratio"])))))
        trs.append(
            '<tr style="border-bottom:1px solid #F1F5F9;">'
            f'<td style="padding:2px 0;text-align:left;width:96px;white-space:nowrap;"><b>{html.escape(r["label"])}</b></td>'
            '<td style="padding:2px 4px;width:82px;">'
            f'<div style="width:78px;height:7px;background:#DBEAFE;border-radius:99px;">'
            f'<div style="width:{bar_w}px;height:7px;background:{r["bar_color"]};border-radius:99px;"></div>'
            "</div></td>"
            f'<td style="padding:2px 0;text-align:right;color:{r["text_color"]};font-weight:700;white-space:nowrap;">{html.escape(r["metric"])}</td>'
            "</tr>"
        )
    trs.append(
        "<tr>"
        '<td style="padding:2px 0;text-align:left;white-space:nowrap;"><b>Stack</b></td>'
        f'<td colspan="2" style="padding:2px 0;text-align:right;color:#0F172A;font-weight:700;white-space:nowrap;">{html.escape(stack_footer)}</td>'
        "</tr>"
    )
    inner = (
        '<table style="width:312px;font-family:Inter,sans-serif;font-size:11px;line-height:1.28;'
        'margin:0 16px;color:#0F172A;border-collapse:collapse;">'
        + "".join(trs)
        + "</table>"
    )
    return _attr(inner)


def build_spine_xml(spec: Dict[str, Any]) -> str:
    tid = spec["tid"]
    p1, p2, p3, p4 = spec["header_parts"]
    header_html = (
        '<div style="font-family:Inter,sans-serif;text-align:left;">'
        f'<span style="font-size:30px;font-weight:900;color:#0F172A;letter-spacing:-0.5px;">{html.escape(p1)} </span>'
        '<span style="font-size:24px;font-weight:400;color:#94A3B8;">+</span>'
        f'<span style="font-size:30px;font-weight:900;color:#7C3AED;letter-spacing:-0.5px;"> {html.escape(p2)} </span>'
        '<span style="font-size:24px;font-weight:400;color:#94A3B8;">+</span>'
        f'<span style="font-size:30px;font-weight:900;color:#059669;letter-spacing:-0.5px;"> {html.escape(p3)} </span>'
        '<span style="font-size:24px;font-weight:400;color:#94A3B8;">+</span>'
        f'<span style="font-size:30px;font-weight:900;color:#2563EB;letter-spacing:-0.5px;"> {html.escape(p4)}</span>'
        "<br/>"
        f'<span style="font-size:13px;color:#475569;font-weight:500;">{html.escape(spec["sub_lead"])} </span>'
        f'<b style="font-size:13px;color:#0F172A;">{html.escape(spec["sub_bold"])}</b>'
        "</div>"
    )

    t1 = spec["t1"]
    t2 = spec["t2"]
    t3 = spec["t3"]
    t4 = spec["t4"]

    t1_title_html = (
        f'<div style="font-family:Inter,sans-serif;"><span style="font-size:20px;font-weight:800;color:#0F172A;">{html.escape(t1["heading"])}</span>'
        f'&nbsp;&nbsp;&nbsp;<span style="font-size:13.5px;font-weight:700;color:#475569;">{html.escape(t1["desc"])}</span></div>'
    )
    t2_title_html = (
        f'<div style="font-family:Inter,sans-serif;"><span style="font-size:20px;font-weight:800;color:#9333EA;">{html.escape(t2["heading"])}</span>'
        f'&nbsp;&nbsp;&nbsp;<span style="font-size:13.5px;font-weight:700;color:#475569;">{html.escape(t2["desc"])}</span></div>'
    )
    t3_title_html = (
        f'<div style="font-family:Inter,sans-serif;"><span style="font-size:20px;font-weight:800;color:#059669;">{html.escape(t3["heading"])}</span>'
        f'&nbsp;&nbsp;&nbsp;<span style="font-size:13.5px;font-weight:700;color:#475569;">{html.escape(t3["desc"])}</span></div>'
    )
    t4_title_html = (
        f'<div style="font-family:Inter,sans-serif;"><span style="font-size:20px;font-weight:800;color:#2563EB;">{html.escape(t4["heading"])}</span>'
        f'&nbsp;&nbsp;&nbsp;<span style="font-size:13.5px;font-weight:700;color:#475569;">{html.escape(t4["desc"])}</span></div>'
    )

    hex_blue = _attr(
        '<div style="text-align:center;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="28" height="28">'
        '<polygon points="18,4 30,11 30,25 18,32 6,25 6,11" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="18" cy="18" r="5" fill="#2563EB"/><circle cx="18" cy="18" r="2" fill="#FFFFFF"/></svg></div>'
    )
    hex_purple = _attr(
        '<div style="text-align:center;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="28" height="28">'
        '<polygon points="18,4 30,11 30,25 18,32 6,25 6,11" fill="#F3E8FF" stroke="#7C3AED" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="18" cy="18" r="5" fill="#7C3AED"/><circle cx="18" cy="18" r="2" fill="#FFFFFF"/></svg></div>'
    )
    hex_green = _attr(
        '<div style="text-align:center;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="28" height="28">'
        '<polygon points="18,4 30,11 30,25 18,32 6,25 6,11" fill="#ECFDF5" stroke="#059669" stroke-width="2.2" stroke-linejoin="round"/>'
        '<circle cx="18" cy="18" r="5" fill="#059669"/><circle cx="18" cy="18" r="2" fill="#FFFFFF"/></svg></div>'
    )

    t2_card1_html = _attr(
        f'<div style="text-align:left;padding-left:12px;"><span style="font-size:10px;font-weight:800;color:#6B21A8;">{html.escape(t2["card1_eyebrow"])}</span>'
        f'<br/><b style="font-size:12px;color:#0F172A;">{html.escape(t2["card1_title"])}</b></div>'
    )
    t2_card2_html = _attr(
        f'<div style="text-align:left;padding-left:12px;"><span style="font-size:10px;font-weight:800;color:#475569;">{html.escape(t2["card2_eyebrow"])}</span>'
        f'<br/><b style="font-size:12px;color:#0F172A;">{html.escape(t2["card2_title"])}</b></div>'
    )
    t3_check_html = _attr(
        f'<div style="text-align:left;padding-left:12px;"><span style="font-size:10px;font-weight:800;color:#065F46;">{html.escape(t3["check_eyebrow"])}</span>'
        f'<br/><b style="font-size:11.5px;color:#0F172A;">☐ {html.escape(t3["check_1"])}<br/>☐ {html.escape(t3["check_2"])}</b></div>'
    )
    footer_html = _attr(
        '<div style="display:flex;align-items:center;justify-content:center;gap:10px;font-family:Inter,sans-serif;">'
        f'<b style="color:#FFFFFF;font-size:12px;letter-spacing:0.7px;">{html.escape(spec["footer_left"])}</b>'
        '<span style="color:#38BDF8;font-size:14px;">•</span>'
        f'<span style="color:#E2E8F0;font-size:12px;">{html.escape(spec["footer_right"])}</span></div>'
    )

    def _bold_val(text: str, color: str, font_px: str = "11.5px", extra: str = "") -> str:
        st = f"font-size:{font_px};color:{color};{extra}"
        return _attr(f'<b style="{st}">{html.escape(text)}</b>')

    diag_name = html.escape(f"{p1} + {p2} + {p3} + {p4}")
    return f"""<mxfile host="embed.diagrams.net" modified="2026-10-29T01:00:00.000Z" agent="ArchitectureEngine"><diagram id="infographic_{tid}_L2" name="{diag_name}"><mxGraphModel dx="1020" dy="1040" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1020" pageHeight="1040" background="#F8FAFC" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>
      <mxCell id="header_title" value="{_attr(header_html)}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;" vertex="1" parent="1"><mxGeometry x="28" y="16" width="964" height="64" as="geometry"/></mxCell>
      <mxCell id="spine_line" value="" style="endArrow=oval;endFill=1;endSize=6;html=1;strokeColor=#CBD5E1;strokeWidth=2;" edge="1" parent="1"><mxGeometry width="50" height="50" relative="1" as="geometry"><mxPoint x="47" y="114" as="sourcePoint"/><mxPoint x="47" y="954" as="targetPoint"/></mxGeometry></mxCell>
      <mxCell id="badge_01" value="01" style="rounded=1;arcSize=24;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#F59E0B;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#B45309;" vertex="1" parent="1"><mxGeometry x="28" y="100" width="38" height="28" as="geometry"/></mxCell>
      <mxCell id="badge_02" value="02" style="rounded=1;arcSize=24;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#A855F7;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#7E22CE;" vertex="1" parent="1"><mxGeometry x="28" y="316" width="38" height="28" as="geometry"/></mxCell>
      <mxCell id="badge_03" value="03" style="rounded=1;arcSize=24;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#10B981;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#047857;" vertex="1" parent="1"><mxGeometry x="28" y="531" width="38" height="28" as="geometry"/></mxCell>
      <mxCell id="badge_04" value="04" style="rounded=1;arcSize=24;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#3B82F6;strokeWidth=1.5;fontStyle=1;fontSize=12;fontColor=#1D4ED8;" vertex="1" parent="1"><mxGeometry x="28" y="756" width="38" height="28" as="geometry"/></mxCell>

      <!-- TIER 01 -->
      <mxCell id="t1_card" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="82" y="92" width="910" height="202" as="geometry"/></mxCell>
      <mxCell id="t1_title" value="{_attr(t1_title_html)}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="100" width="866" height="28" as="geometry"/></mxCell>
      <mxCell id="t1_loaded_box" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#F59E0B;strokeWidth=1.5;dashed=1;dashPattern=4 4;" vertex="1" parent="1"><mxGeometry x="104" y="134" width="332" height="104" as="geometry"/></mxCell>
      <mxCell id="t1_loaded_lbl" value="{html.escape(t1['left_eyebrow'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontStyle=1;fontSize=10.5;fontColor=#92400E;" vertex="1" parent="1"><mxGeometry x="116" y="138" width="308" height="18" as="geometry"/></mxCell>
      <mxCell id="t1_prompt_pill" value="{_pill_pair_val(288, t1['left_top_l'], t1['left_top_r'], '#92400E')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#FCD34D;strokeWidth=1.2;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="116" y="159" width="308" height="26" as="geometry"/></mxCell>
      <mxCell id="t1_files_pill" value="{_bold_val(t1['left_chip1'], '#0F172A')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#FCD34D;strokeWidth=1.2;" vertex="1" parent="1"><mxGeometry x="116" y="190" width="150" height="26" as="geometry"/></mxCell>
      <mxCell id="t1_tools_pill" value="{_bold_val(t1['left_chip2'], '#6B21A8')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#D8B4FE;strokeWidth=1.2;" vertex="1" parent="1"><mxGeometry x="274" y="190" width="150" height="26" as="geometry"/></mxCell>
      <mxCell id="t1_more_lbl" value="{html.escape(t1['left_foot'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#475569;" vertex="1" parent="1"><mxGeometry x="116" y="218" width="308" height="16" as="geometry"/></mxCell>
      <mxCell id="t1_model_circle" value="{hex_blue}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="512" y="159" width="54" height="54" as="geometry"/></mxCell>
      <mxCell id="t1_model_lbl" value="{html.escape(t1['hub_lbl'])}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;fontStyle=1;fontSize=11.5;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="494" y="215" width="90" height="18" as="geometry"/></mxCell>
      <mxCell id="t1_edge_1" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;{html.escape(t1['edge_lbl'])}&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=10.5;fontColor=#475569;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t1_loaded_box" target="t1_model_circle"><mxGeometry relative="1" as="geometry"><mxPoint x="-5" y="-2" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t1_right_box" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#93C5FD;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="616" y="134" width="354" height="104" as="geometry"/></mxCell>
      <mxCell id="t1_right_lbl" value="{html.escape(t1['right_eyebrow'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontStyle=1;fontSize=10.5;fontColor=#1D4ED8;" vertex="1" parent="1"><mxGeometry x="628" y="138" width="330" height="18" as="geometry"/></mxCell>
      <mxCell id="t1_ask_1" value="{_pill_pair_val(306, t1['right_row1_l'], t1['right_row1_r'], '#1D4ED8')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#BFDBFE;strokeWidth=1.2;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="628" y="158" width="330" height="25" as="geometry"/></mxCell>
      <mxCell id="t1_ask_2" value="{_pill_pair_val(306, t1['right_row2_l'], t1['right_row2_r'], '#1D4ED8')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#BFDBFE;strokeWidth=1.2;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="628" y="187" width="330" height="25" as="geometry"/></mxCell>
      <mxCell id="t1_ask_3" value="{html.escape(t1['right_foot'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11.5;fontStyle=1;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="628" y="215" width="330" height="18" as="geometry"/></mxCell>
      <mxCell id="t1_edge_2" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t1_model_circle" target="t1_right_box"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t1_prompt_bar" value="{_prompt_bar_val(t1['prompt'])}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#E2E8F0;strokeWidth=1;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="246" width="866" height="36" as="geometry"/></mxCell>

      <!-- TIER 02 -->
      <mxCell id="t2_card" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="82" y="308" width="910" height="206" as="geometry"/></mxCell>
      <mxCell id="t2_title" value="{_attr(t2_title_html)}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="316" width="866" height="28" as="geometry"/></mxCell>
      <mxCell id="t2_harness_box" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#FAF5FF;strokeColor=#D8B4FE;strokeWidth=1.5;dashed=1;dashPattern=4 4;" vertex="1" parent="1"><mxGeometry x="104" y="350" width="866" height="108" as="geometry"/></mxCell>
      <mxCell id="t2_harness_lbl" value="{html.escape(t2['eyebrow'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontStyle=1;fontSize=10;fontColor=#6B21A8;" vertex="1" parent="1"><mxGeometry x="116" y="354" width="250" height="18" as="geometry"/></mxCell>
      <mxCell id="t2_in1_pill" value="{_pill_pair_val(204, t2['in1_l'], t2['in1_r'], '#6B21A8')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#C084FC;strokeWidth=1.5;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="116" y="374" width="224" height="28" as="geometry"/></mxCell>
      <mxCell id="t2_skills_pill" value="{_pill_pair_val(204, t2['in2_l'], t2['in2_r'], '#6B21A8')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#C084FC;strokeWidth=1.5;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="116" y="410" width="224" height="28" as="geometry"/></mxCell>
      <mxCell id="t2_model_circle" value="{hex_purple}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="388" y="376" width="56" height="56" as="geometry"/></mxCell>
      <mxCell id="t2_model_lbl" value="{html.escape(t2['hub_lbl'])}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=bottom;fontStyle=1;fontSize=11.5;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="371" y="355" width="90" height="18" as="geometry"/></mxCell>
      <mxCell id="t2_tools_card" value="{t2_card1_html}" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#C084FC;strokeWidth=1.5;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="528" y="376" width="210" height="56" as="geometry"/></mxCell>
      <mxCell id="t2_checks_card" value="{t2_card2_html}" style="rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="772" y="376" width="184" height="56" as="geometry"/></mxCell>
      <mxCell id="t2_edge_in" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t2_in1_pill" target="t2_model_circle"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="364" y="388"/><mxPoint x="364" y="404"/></Array></mxGeometry></mxCell>
      <mxCell id="t2_edge_in2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t2_skills_pill" target="t2_model_circle"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="364" y="424"/><mxPoint x="364" y="404"/></Array></mxGeometry></mxCell>
      <mxCell id="t2_edge_calls" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;{html.escape(t2['edge_calls'])}&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=10.5;fontColor=#475569;fontStyle=1;labelBackgroundColor=#FAF5FF;" edge="1" parent="1" source="t2_model_circle" target="t2_tools_card"><mxGeometry relative="1" as="geometry"><mxPoint x="-5" y="-2" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t2_edge_returns" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;{html.escape(t2['edge_returns'])}&lt;/span&gt;" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#64748B;strokeWidth=1.5;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=1;fontSize=10;fontColor=#475569;fontStyle=1;labelBackgroundColor=#FAF5FF;" edge="1" parent="1" source="t2_tools_card" target="t2_model_circle"><mxGeometry relative="1" as="geometry"><mxPoint x="0" y="-2" as="offset"/><Array as="points"><mxPoint x="633" y="449"/><mxPoint x="416" y="449"/></Array></mxGeometry></mxCell>
      <mxCell id="t2_edge_checks" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t2_tools_card" target="t2_checks_card"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t2_prompt_bar" value="{_prompt_bar_val(t2['prompt'])}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#E2E8F0;strokeWidth=1;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="466" width="866" height="36" as="geometry"/></mxCell>

      <!-- TIER 03 -->
      <mxCell id="t3_card" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="82" y="528" width="910" height="206" as="geometry"/></mxCell>
      <mxCell id="t3_title" value="{_attr(t3_title_html)}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="531" width="866" height="28" as="geometry"/></mxCell>
      <mxCell id="t3_model_circle" value="{hex_green}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="130" y="562" width="52" height="52" as="geometry"/></mxCell>
      <mxCell id="t3_model_lbl" value="{html.escape(t3['hub_lbl'])}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;fontStyle=1;fontSize=11.5;fontColor=#0F172A;" vertex="1" parent="1"><mxGeometry x="121" y="616" width="70" height="18" as="geometry"/></mxCell>
      <mxCell id="t3_check_box" value="{t3_check_html}" style="rounded=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#6EE7B7;strokeWidth=1.5;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="216" y="560" width="224" height="56" as="geometry"/></mxCell>
      <mxCell id="t3_fix_box" value="{_bold_val(t3['fix_lbl'], '#065F46', '12px')}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#D1FAE5;strokeColor=#34D399;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="216" y="648" width="224" height="30" as="geometry"/></mxCell>
      <mxCell id="t3_gate_pass" value="{_bold_val(t3['gate_1'], '#0F172A', '12px')}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#34D399;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="516" y="572" width="188" height="32" as="geometry"/></mxCell>
      <mxCell id="t3_gate_tries" value="{_bold_val(t3['gate_2'], '#0F172A', '12px')}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#34D399;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="516" y="648" width="188" height="30" as="geometry"/></mxCell>
      <mxCell id="t3_done_pill" value="{_bold_val(t3['done_lbl'], '#FFFFFF', '12.5px')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0F172A;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="784" y="572" width="186" height="32" as="geometry"/></mxCell>
      <mxCell id="t3_stop_pill" value="{_bold_val(t3['stop_lbl'], '#9A3412', '12.5px')}" style="rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#FFF7ED;strokeColor=#FB923C;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="784" y="648" width="186" height="30" as="geometry"/></mxCell>
      <mxCell id="t3_e1" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t3_model_circle" target="t3_check_box"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t3_e2" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t3_check_box" target="t3_gate_pass"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t3_e_yes1" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;yes&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#10B981;strokeWidth=2;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=11;fontColor=#047857;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t3_gate_pass" target="t3_done_pill"><mxGeometry relative="1" as="geometry"><mxPoint x="-5" y="-1.5" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t3_e_no1" value="&lt;span style=&apos;padding:0 2px;line-height:0.9;&apos;&gt;no&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;fontSize=10.5;fontColor=#475569;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t3_gate_pass" target="t3_gate_tries"><mxGeometry relative="1" as="geometry"><mxPoint x="0" y="-6" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t3_e_yes2" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;yes&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#DC2626;strokeWidth=2;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=11;fontColor=#B91C1C;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t3_gate_tries" target="t3_stop_pill"><mxGeometry relative="1" as="geometry"><mxPoint x="-5" y="-1.5" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t3_e_no2" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;no&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#10B981;strokeWidth=1.6;endArrow=block;endFill=1;exitX=0;exitY=0.5;entryX=1;entryY=0.5;fontSize=11;fontColor=#047857;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t3_gate_tries" target="t3_fix_box"><mxGeometry relative="1" as="geometry"><mxPoint x="5" y="-1.5" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t3_e_loop" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#10B981;strokeWidth=2;endArrow=block;endFill=1;exitX=0;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t3_fix_box" target="t3_model_circle"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="106" y="663"/><mxPoint x="106" y="588"/></Array></mxGeometry></mxCell>
      <mxCell id="t3_prompt_bar" value="{_prompt_bar_val(t3['prompt'])}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#E2E8F0;strokeWidth=1;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="686" width="866" height="36" as="geometry"/></mxCell>

      <!-- TIER 04 -->
      <mxCell id="t4_card" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="82" y="748" width="910" height="206" as="geometry"/></mxCell>
      <mxCell id="t4_title" value="{_attr(t4_title_html)}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="756" width="866" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_folder_box" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#93C5FD;strokeWidth=1.5;dashed=1;dashPattern=4 4;" vertex="1" parent="1"><mxGeometry x="104" y="790" width="432" height="104" as="geometry"/></mxCell>
      <mxCell id="t4_folder_lbl" value="{html.escape(t4['left_eyebrow'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontStyle=1;fontSize=10.5;fontColor=#1E3A8A;" vertex="1" parent="1"><mxGeometry x="116" y="794" width="235" height="18" as="geometry"/></mxCell>
      <mxCell id="t4_lines_lbl" value="{html.escape(t4['left_sub'])}" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontStyle=1;fontSize=10.5;fontColor=#475569;" vertex="1" parent="1"><mxGeometry x="322" y="794" width="200" height="18" as="geometry"/></mxCell>
      <mxCell id="t4_f_brief" value="{_bold_val(t4['n1'], '#0F172A')}" style="rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#60A5FA;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="116" y="816" width="118" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_f_draft" value="{_bold_val(t4['n2'], '#0F172A')}" style="rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#60A5FA;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="116" y="856" width="118" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_f_aud" value="{_bold_val(t4['n3'], '#0F172A')}" style="rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#60A5FA;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="260" y="816" width="118" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_f_offer" value="{_bold_val(t4['n4'], '#0F172A')}" style="rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#60A5FA;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="260" y="856" width="118" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_m1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.4;endArrow=none;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t4_f_brief" target="t4_f_aud"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_m2" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.4;endArrow=none;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="t4_f_brief" target="t4_f_draft"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_m3" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.4;endArrow=none;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="t4_f_draft" target="t4_f_offer"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_m4" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.4;endArrow=none;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" parent="1" source="t4_f_aud" target="t4_f_offer"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_m5" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.3;endArrow=none;exitX=1;exitY=1;entryX=0;entryY=0;" edge="1" parent="1" source="t4_f_brief" target="t4_f_offer"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_m6" value="" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.3;endArrow=none;exitX=1;exitY=0;entryX=0;entryY=1;" edge="1" parent="1" source="t4_f_draft" target="t4_f_aud"><mxGeometry relative="1" as="geometry"/></mxCell>
      <mxCell id="t4_f_notes" value="{_bold_val(t4['unlinked_node'], '#475569')}" style="rounded=1;arcSize=18;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#94A3B8;strokeWidth=1.5;dashed=1;dashPattern=3 3;" vertex="1" parent="1"><mxGeometry x="396" y="824" width="126" height="28" as="geometry"/></mxCell>
      <mxCell id="t4_unlinked_lbl" value="{html.escape(t4['unlinked_sub'])}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;fontSize=11;fontColor=#64748B;" vertex="1" parent="1"><mxGeometry x="409" y="856" width="100" height="18" as="geometry"/></mxCell>
      <mxCell id="t4_edge_maps" value="&lt;span style=&apos;padding:0 2px;&apos;&gt;{html.escape(t4['edge_lbl'])}&lt;/span&gt;" style="edgeStyle=none;html=1;strokeColor=#64748B;strokeWidth=1.6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=10.5;fontColor=#475569;fontStyle=1;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="t4_folder_box" target="t4_map_card"><mxGeometry relative="1" as="geometry"><mxPoint x="-5" y="-2" as="offset"/></mxGeometry></mxCell>
      <mxCell id="t4_map_card" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#93C5FD;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="626" y="790" width="344" height="104" as="geometry"/></mxCell>
      <mxCell id="t4_map_header" value="{_bold_val(t4['table_header'], '#1E3A8A', '11.5px', 'padding-left:12px;')}" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#93C5FD;strokeWidth=1;align=left;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="626" y="790" width="344" height="23" as="geometry"/></mxCell>
      <mxCell id="t4_map_rows" value="{_score_rows_val(t4['rows'], t4['stack'])}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacing=0;spacingLeft=0;spacingRight=0;" vertex="1" parent="1"><mxGeometry x="626" y="813" width="344" height="81" as="geometry"/></mxCell>
      <mxCell id="t4_prompt_bar" value="{_prompt_bar_val(t4['prompt'])}" style="rounded=1;arcSize=16;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#E2E8F0;strokeWidth=1;align=center;verticalAlign=middle;" vertex="1" parent="1"><mxGeometry x="104" y="906" width="866" height="36" as="geometry"/></mxCell>
      <mxCell id="footer_pill_52" value="{footer_html}" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#1E293B;strokeWidth=1.5;" vertex="1" parent="1"><mxGeometry x="130" y="968" width="760" height="42" as="geometry"/></mxCell>
    </root></mxGraphModel></diagram></mxfile>
"""


SPECS_T79_T84: Dict[str, Dict[str, Any]] = {
    "T79": {
        "tid": "T79",
        "header_parts": ("Prompt JSON", "Grammar Mask", "Semantic Gate", "Zero Retry"),
        "sub_lead": "Prompt-Based JSON vs. Constrained Decoding.",
        "sub_bold": "Why 99/100 valid replies still break pipelines — enforce shape and meaning.",
        "t1": {
            "heading": "Prompt JSON",
            "desc": "Asking in prose ('return only JSON') works 99 times; the 100th breaks your parser.",
            "left_eyebrow": "SAME MULTIMODAL INPUTS (UNCONSTRAINED)",
            "left_top_l": "Prompt Instruction",
            "left_top_r": "no token mask",
            "left_chip1": "Text + PDFs",
            "left_chip2": "CRM + Schema",
            "left_foot": "Missing keys, wrong types, or prose wrapper",
            "hub_lbl": "decoder",
            "edge_lbl": "masks",
            "right_eyebrow": "CONSTRAINED DECODING (GRAMMAR ENFORCED)",
            "right_row1_l": "FSM / CFG Token Mask",
            "right_row1_r": "100% valid shape",
            "right_row2_l": "Confidence + Source Span",
            "right_row2_r": "conf: 0.96",
            "right_foot": "Invalid tokens masked to -inf before sampling",
            "prompt": "Replace 'return only valid JSON' prose prompts with responseSchema / vLLM xgrammar FSM masks.",
        },
        "t2": {
            "heading": "Grammar Mask",
            "desc": "Compile Pydantic / JSON Schema into a deterministic finite-state token mask.",
            "eyebrow": "CONSTRAINED DECODING PIPELINE",
            "in1_l": "Pydantic Schema",
            "in1_r": "typed fields",
            "in2_l": "Source Grounding",
            "in2_r": "span offsets",
            "hub_lbl": "grammar",
            "edge_calls": "enforces",
            "edge_returns": "next valid token",
            "card1_eyebrow": "TYPED OUTPUT CONTRACT",
            "card1_title": "order_id · conf · span",
            "card2_eyebrow": "FORMAT RETRIES",
            "card2_title": "0 Parse Retries Needed",
            "prompt": "Bind response_mime_type='application/json' + response_schema so every emitted token satisfies the grammar.",
        },
        "t3": {
            "heading": "Semantic Gate",
            "desc": "One thing people miss: valid JSON shape does NOT guarantee the right order_id.",
            "hub_lbl": "payload",
            "check_eyebrow": "VERIFY MEANING (NOT JUST SHAPE)",
            "check_1": "order_id exists in source CRM",
            "check_2": "Calibrated conf >= 0.90",
            "fix_lbl": "Re-ground against source span",
            "gate_1": "Source record match?",
            "gate_2": "2 semantic checks tried?",
            "done_lbl": "Commit Verified JSON",
            "stop_lbl": "Route to Human Review",
            "prompt": "Pair constrained decoding with deterministic foreign-key / source-span verification and confidence routing.",
        },
        "t4": {
            "heading": "Zero Retry",
            "desc": "Prompt-only JSON trap vs. Constrained Decoding + Semantic Gate in production.",
            "left_eyebrow": "PROMPT-ONLY JSON FAILURE MODES",
            "left_sub": "99% pass = compound loop rot",
            "n1": "Missing Field",
            "n2": "Wrong Type",
            "n3": "Prose Wrapper",
            "n4": "Retry Pollution",
            "unlinked_node": "wrong_order_id",
            "unlinked_sub": "silent semantic bug",
            "edge_lbl": "eliminates",
            "table_header": "STRUCTURED OUTPUTS · PRODUCTION SCORECARD",
            "rows": [
                {"label": "Schema Pass", "ratio": 1.0, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "92% → 100.0%"},
                {"label": "Parse Retries", "ratio": 0.94, "bar_color": "#059669", "text_color": "#047857", "metric": "8.0% → 0.0%"},
                {"label": "Meaning Audit", "ratio": 0.96, "bar_color": "#7C3AED", "text_color": "#6D28D9", "metric": "Span + Conf Gate"},
            ],
            "stack": "Vertex Controlled Gen • vLLM Outlines",
            "prompt": "If downstream code depends on the output, never ask for structure — enforce schema and verify semantics.",
        },
        "footer_left": "CONSTRAINED DECODING & SEMANTIC VERIFICATION",
        "footer_right": "Sivasankar Natarajan Lineage • Vertex AI + vLLM Outlines",
    },
    "T80": {
        "tid": "T80",
        "header_parts": ("Before Call", "Inside Loop", "After Answer", "Routing Gains"),
        "sub_lead": "9 Typed Micro-Decisions Without Full LLM Calls.",
        "sub_bold": "Offload bool, choice, and score gates to calibrated System-1 classifiers.",
        "t1": {
            "heading": "Before Call",
            "desc": "Decisions 01-03 screen risk, gate retrieval, and score urgency before invoking an LLM.",
            "left_eyebrow": "PHASE 1 · BEFORE THE MAIN LLM CALL",
            "left_top_l": "01 Input Screening",
            "left_top_r": "bool + conf",
            "left_chip1": "02 Retrieval Gate",
            "left_chip2": "03 Priority Score",
            "left_foot": "Blocks injection & skips unneeded RAG calls",
            "hub_lbl": "system-1",
            "edge_lbl": "classifies",
            "right_eyebrow": "THREE TYPED OUTPUTS · SINGLE PASS",
            "right_row1_l": "bool · choice · score",
            "right_row1_r": "conf: 0.0–1.0",
            "right_row2_l": "Latency per Gate",
            "right_row2_r": "<15ms single pass",
            "right_foot": "Zero chain-of-thought token tax on simple gates",
            "prompt": "Run 01 Input Screening (bool), 02 Retrieval Gate (bool), and 03 Composite Risk Score before calling the main LLM.",
        },
        "t2": {
            "heading": "Inside Loop",
            "desc": "Decisions 04-06 gate risky tool calls, verify task completion, and route model tiers.",
            "eyebrow": "PHASE 2 · INSIDE THE AGENT LOOP",
            "in1_l": "04 Tool Call Gate",
            "in1_r": "allow / ask / block",
            "in2_l": "05 Stop Check",
            "in2_r": "done vs continue",
            "hub_lbl": "06 router",
            "edge_calls": "routes",
            "edge_returns": "step telemetry",
            "card1_eyebrow": "TIERED MODEL SELECTION",
            "card1_title": "Flash (Fast) vs Argon (Deep)",
            "card2_eyebrow": "APP CODE BOUNDARY",
            "card2_title": "RBAC · Budgets · Rules",
            "prompt": "Gate every proposed tool call (04), stop check (05), and model tier route (06) with typed choice judgments.",
        },
        "t3": {
            "heading": "After Answer",
            "desc": "Decisions 07-09 check document grounding, filter memory writes, and trigger handoffs.",
            "hub_lbl": "draft",
            "check_eyebrow": "PHASE 3 · POST-ANSWER GATES",
            "check_1": "07 Grounding backed by docs",
            "check_2": "08 Memory: long / session / drop",
            "fix_lbl": "Strip or re-ground claim",
            "gate_1": "09 Conf >= threshold?",
            "gate_2": "Retry budget exhausted?",
            "done_lbl": "Deliver + Write Memory",
            "stop_lbl": "Escalate to Human",
            "prompt": "Audit 07 Grounding, filter 08 Memory writes so junk never pollutes future runs, and enforce 09 Confidence Handoffs.",
        },
        "t4": {
            "heading": "Routing Gains",
            "desc": "Full LLM on every micro-decision vs. 3-layer System-1 + LLM + App Code split.",
            "left_eyebrow": "ALL-LLM DECISION OVERHEAD",
            "left_sub": "9 full LLM calls per turn = slow",
            "n1": "Latency Tax",
            "n2": "Token Burn",
            "n3": "Noisy Memory",
            "n4": "Over-Retrieval",
            "unlinked_node": "uncalibrated_conf",
            "unlinked_sub": "guessed prose",
            "edge_lbl": "compresses",
            "table_header": "9-DECISION AGENT LOOP · DIVISION OF LABOR",
            "rows": [
                {"label": "Typed Gates", "ratio": 0.95, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "01–09 (<15ms)"},
                {"label": "LLM Calls Cut", "ratio": 0.84, "bar_color": "#059669", "text_color": "#047857", "metric": "-60% to -75%"},
                {"label": "App Controls", "ratio": 1.0, "bar_color": "#7C3AED", "text_color": "#6D28D9", "metric": "100% Deterministic"},
            ],
            "stack": "Model Armor + Flash-Lite • TypeSafe Jev",
            "prompt": "Keep permissions in app code, typed judgments on calibrated small classifiers, and synthesis on frontier LLMs.",
        },
        "footer_left": "9 TYPED MICRO-DECISIONS IN THE AGENT LOOP",
        "footer_right": "Rathnakumar Udayakumar Lineage • Vertex AI + TypeSafe Jev",
    },
    "T81": {
        "tid": "T81",
        "header_parts": ("Repo Rules", "Continuity", "Maker-Checker", "Graph Rollback"),
        "sub_lead": "Harness Engineering from Scratch (14 Lectures · 8 Projects).",
        "sub_bold": "Build the deterministic engineering environment around coding agents.",
        "t1": {
            "heading": "Repo Rules",
            "desc": "Phases 1-2: Structure repository instructions, scoped context, and persistent memory.",
            "left_eyebrow": "PHASES 1–2 · INSTRUCTIONS & MEMORY",
            "left_top_l": "AGENTS.md + Layout",
            "left_top_r": "concise rules",
            "left_chip1": "Context Budget",
            "left_chip2": "Scoped Skills",
            "left_foot": "Same real application evolved across all 8 projects",
            "hub_lbl": "harness",
            "edge_lbl": "mounts",
            "right_eyebrow": "PHASES 3–4 · CONTINUITY & SCOPE CONTROL",
            "right_row1_l": "Multi-Session Handoff",
            "right_row1_r": "state ledger",
            "right_row2_l": "Task Scope & Progress",
            "right_row2_r": "bounded diff",
            "right_foot": "Prevents cross-session amnesia and scope creep",
            "prompt": "Start by codifying repository structure, concise agent instructions, and persistent multi-session handoff ledgers.",
        },
        "t2": {
            "heading": "Continuity",
            "desc": "Phases 5-6: Wire automated test suites, observability traces, and coding loops.",
            "eyebrow": "PHASES 5–6 · TESTS & OBSERVABILITY",
            "in1_l": "Deterministic Tests",
            "in1_r": "lint + pytest",
            "in2_l": "Execution Traces",
            "in2_r": "step telemetry",
            "hub_lbl": "verifier",
            "edge_calls": "validates",
            "edge_returns": "structured diff feedback",
            "card1_eyebrow": "AUTOMATED CODING LOOP",
            "card1_title": "Edit · Test · Trace · Fix",
            "card2_eyebrow": "REUSABLE TEMPLATES",
            "card2_title": "Harness-Creator Skill",
            "prompt": "Attach deterministic unit tests and OpenTelemetry traces to every edit loop before scaling autonomy.",
        },
        "t3": {
            "heading": "Maker-Checker",
            "desc": "Phase 7: Separate the Builder agent from an independent Checker with max-round caps.",
            "hub_lbl": "maker",
            "check_eyebrow": "INDEPENDENT CHECKER GATE",
            "check_1": "Tests + acceptance checks pass",
            "check_2": "Zero out-of-scope file edits",
            "fix_lbl": "Return actionable diff critique",
            "gate_1": "Checker approves PR?",
            "gate_2": "Max 3 rounds reached?",
            "done_lbl": "Merge Verified Commit",
            "stop_lbl": "Rollback + Handoff",
            "prompt": "Pair every Maker coding loop with an isolated Checker agent and a hard iteration cap so they never argue forever.",
        },
        "t4": {
            "heading": "Graph Rollback",
            "desc": "Phase 8: Parallel DAG orchestration, checkpointed rollback, and curriculum coverage.",
            "left_eyebrow": "PROMPT-ONLY CODING DEMO GAPS",
            "left_sub": "Happy-path courses skip rollback",
            "n1": "Session Amnesia",
            "n2": "Scope Drift",
            "n3": "Self-Grading",
            "n4": "No Rollback",
            "unlinked_node": "orphan_branch",
            "unlinked_sub": "unverified state",
            "edge_lbl": "graduates to",
            "table_header": "LEARN-HARNESS-ENGINEERING · CURRICULUM",
            "rows": [
                {"label": "Curriculum", "ratio": 1.0, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "14 Lectures · 8 Phases"},
                {"label": "Hands-On", "ratio": 0.92, "bar_color": "#059669", "text_color": "#047857", "metric": "8 Real-App Projects"},
                {"label": "Open Access", "ratio": 0.96, "bar_color": "#7C3AED", "text_color": "#6D28D9", "metric": "21K+ ★ · 15 Langs"},
            ],
            "stack": "Google Cloud ADK • walkinglabs MIT",
            "prompt": "Orchestrate parallel worktrees via a checkpointed graph so any failed branch rolls back cleanly in O(1).",
        },
        "footer_left": "8-PHASE HARNESS ENGINEERING FROM SCRATCH",
        "footer_right": "Mayank A. Lineage • walkinglabs/learn-harness-engineering + ADK",
    },
    "T82": {
        "tid": "T82",
        "header_parts": ("Replay Set", "Causal Triage", "Dual Timers", "Revision Gate"),
        "sub_lead": "Agent Code Review Evaluation: Measure What It Missed.",
        "sub_bold": "Connect automated code review to repo failure modes, not vendor hype.",
        "t1": {
            "heading": "Replay Set",
            "desc": "Seed representative PRs: a known defect, unusual valid code, and a clean change.",
            "left_eyebrow": "01 REPRESENTATIVE REPLAY-SET INPUTS",
            "left_top_l": "Seeded Known Defect",
            "left_top_r": "race / auth bug",
            "left_chip1": "Unusual Valid PR",
            "left_chip2": "Clean Baseline",
            "left_foot": "Tests recall on real risks AND restraint on clean diffs",
            "hub_lbl": "reviewer",
            "edge_lbl": "inspects",
            "right_eyebrow": "02 THREE CAUSAL REVIEW OUTCOMES",
            "right_row1_l": "Correct Finding vs False Alarm",
            "right_row1_r": "precision",
            "right_row2_l": "Missed Defect (Silent Escape)",
            "right_row2_r": "recall gap",
            "right_foot": "A review that cannot name its misses is just a stamp",
            "prompt": "Build a replay set with seeded race/permission defects, unusual valid code, and clean PRs before adopting AI review.",
        },
        "t2": {
            "heading": "Causal Triage",
            "desc": "Maintainers classify findings against ground-truth defects and record dual timers.",
            "eyebrow": "03–04 GROUND TRUTH & DUAL TIMERS",
            "in1_l": "Time to Run Review",
            "in1_r": "bot latency",
            "in2_l": "Time to Assess",
            "in2_r": "human triage tax",
            "hub_lbl": "triage",
            "edge_calls": "scores",
            "edge_returns": "update replay corpus",
            "card1_eyebrow": "MISSED DEFECT LEDGER",
            "card1_title": "Auth Drift · Race · Null Path",
            "card2_eyebrow": "REVISION PINNING",
            "card2_title": "Commit SHA Bound Receipt",
            "prompt": "Track Time to Review and Time to Assess Findings separately — ten noisy nits cost more than one precise warning.",
        },
        "t3": {
            "heading": "Dual Timers",
            "desc": "Enforce deterministic revision-pinned acceptance rules before trusting review sign-off.",
            "hub_lbl": "commit sha",
            "check_eyebrow": "05–06 SHA ACCEPTANCE GATE",
            "check_1": "Zero seeded misses on SHA",
            "check_2": "Triage <= maintainer budget",
            "fix_lbl": "Tune rules + prune noisy checks",
            "gate_1": "Current SHA verified?",
            "gate_2": "False-alarm cap exceeded?",
            "done_lbl": "Accept for Commit SHA",
            "stop_lbl": "Reject Stale / Noisy Run",
            "prompt": "Bind every review decision to the exact Git commit SHA so yesterday's green check never vouches for today's code.",
        },
        "t4": {
            "heading": "Revision Gate",
            "desc": "Vendor demo vanity volume vs. Evidence-based missed-defect & triage-cost audit.",
            "left_eyebrow": "UNMEASURED REVIEW TRAPS",
            "left_sub": "Comment count != code safety",
            "n1": "Silent Misses",
            "n2": "10 Style Nits",
            "n3": "Triage Fatigue",
            "n4": "Version Drift",
            "unlinked_node": "stale_approval",
            "unlinked_sub": "prior commit SHA",
            "edge_lbl": "replaces",
            "table_header": "CODE REVIEW EVAL · DECISION EVIDENCE",
            "rows": [
                {"label": "Defect Recall", "ratio": 0.95, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "100% Seeded Caught"},
                {"label": "Triage Tax", "ratio": 0.88, "bar_color": "#059669", "text_color": "#047857", "metric": "Dual Timer Bounded"},
                {"label": "SHA Pinning", "ratio": 1.0, "bar_color": "#7C3AED", "text_color": "#6D28D9", "metric": "0 Stale Sign-Offs"},
            ],
            "stack": "Gemini Code Assist • OpenHands",
            "prompt": "Pay for defect recall and bounded maintainer triage time — never review volume.",
        },
        "footer_left": "AGENT CODE REVIEW REPLAY-SET & MISSES HARNESS",
        "footer_right": "Bally S Kehal Lineage • Gemini Code Assist + OpenHands",
    },
    "T83": {
        "tid": "T83",
        "header_parts": ("Real Tasks", "Isolated Trials", "Code + Judge", "pass^k Gate"),
        "sub_lead": "Evaluating AI Agents: Outcome, Trajectory & Restraint.",
        "sub_bold": "75% per-run success passes 3 of 3 runs (pass^3) only 42.2% of the time.",
        "t1": {
            "heading": "Real Tasks",
            "desc": "Start with 20-50 real bug/support failures PLUS restraint tasks where acting is wrong.",
            "left_eyebrow": "STEP 1–2 · FAILURE CORPUS & RESTRAINT",
            "left_top_l": "20–50 Real Failures",
            "left_top_r": "bugs + tickets",
            "left_chip1": "Capability Tag",
            "left_chip2": "Restraint Cases",
            "left_foot": "Include refuse, clarify, and escalate-to-human tasks",
            "hub_lbl": "env.reset()",
            "edge_lbl": "isolates",
            "right_eyebrow": "STEP 3 · ISOLATED MULTI-TRIAL HARNESS",
            "right_row1_l": "Clean Sandbox State per Trial",
            "right_row1_r": "k = 5 runs",
            "right_row2_l": "Full Transcript + End State",
            "right_row2_r": "tools + DB rows",
            "right_foot": "Prevents Trial 1 side effects from leaking into Trial 2",
            "prompt": "Seed 20-50 real failure tasks plus explicit Restraint tasks, and call env.reset() before every single trial.",
        },
        "t2": {
            "heading": "Isolated Trials",
            "desc": "Grade Outcome (DB end state), Trajectory (safety order), Efficiency, and Restraint.",
            "eyebrow": "STEP 4–5 · CODE CHECKS + JUDGE",
            "in1_l": "Code State Checks",
            "in1_r": "DB + tool args",
            "in2_l": "Rubric LLM Judge",
            "in2_r": "allows 'unknown'",
            "hub_lbl": "grader",
            "edge_calls": "calibrates",
            "edge_returns": "audit transcripts",
            "card1_eyebrow": "5 GRADED DIMENSIONS",
            "card1_title": "Outcome · Path · pass^k · Restraint",
            "card2_eyebrow": "HUMAN CALIBRATION",
            "card2_title": "Expert Labels + Unknown",
            "prompt": "Grade final DB state and required tool ordering in deterministic code; calibrate rubric judges with an 'unknown' option.",
        },
        "t3": {
            "heading": "Code + Judge",
            "desc": "Gate customer-facing agent releases on pass^k (all k runs succeed), never pass@k.",
            "hub_lbl": "k trials",
            "check_eyebrow": "STEP 6 · RELIABILITY GATE",
            "check_1": "pass^5 >= release SLO target",
            "check_2": "100% restraint compliance",
            "fix_lbl": "Read transcripts + fix step",
            "gate_1": "All k trials pass?",
            "gate_2": "Grader bug detected?",
            "done_lbl": "Ship Customer Agent",
            "stop_lbl": "Block + Fix Harness",
            "prompt": "Measure coding search tools with pass@k (1 hit suffices), but gate customer-facing agents strictly on pass^k.",
        },
        "t4": {
            "heading": "pass^k Gate",
            "desc": "Single-run illusion (75% = 1 in 4 users fail) vs. Multi-trial pass^k reliability.",
            "left_eyebrow": "SINGLE-RUN DEMO ILLUSIONS",
            "left_sub": "0.75^3 = 42.2% 3-run consistency",
            "n1": "1-Run Luck",
            "n2": "No Restraint",
            "n3": "Dirty State",
            "n4": "Forced Judge",
            "unlinked_node": "pass_at_5_99pct",
            "unlinked_sub": "hides 25% fail rate",
            "edge_lbl": "exposes",
            "table_header": "75% PER-RUN AGENT · pass@k VS pass^k",
            "rows": [
                {"label": "pass@3 (Any 1)", "ratio": 0.98, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "98.4% (Optimistic)"},
                {"label": "pass^3 (All 3)", "ratio": 0.42, "bar_color": "#DC2626", "text_color": "#B91C1C", "metric": "42.2% (Real User)"},
                {"label": "Target pass^5", "ratio": 0.90, "bar_color": "#059669", "text_color": "#047857", "metric": ">= 90% + Restraint"},
            ],
            "stack": "Vertex AI Eval • Promptfoo / pytest",
            "prompt": "Read full failure transcripts on every release — scores tell you a capability broke; transcripts show why.",
        },
        "footer_left": "MULTI-TURN AGENT EVALUATION & pass^k RELIABILITY",
        "footer_right": "Shivani Virdi Lineage • Vertex AI Eval + Promptfoo / OpenHands",
    },
    "T84": {
        "tid": "T84",
        "header_parts": ("Prefill vs Decode", "KV-Cache Math", "Batching", "Goodput SLO"),
        "sub_lead": "Inference Engineering: Compute vs. HBM Bandwidth.",
        "sub_bold": "Why tok/s is not enough — optimize TTFT, ITL/TPOT, KV pressure & Goodput.",
        "t1": {
            "heading": "Prefill vs Decode",
            "desc": "Inference splits into parallel compute-bound Prefill (TTFT) and BW-bound Decode (ITL).",
            "left_eyebrow": "PHASE A · PREFILL (COMPUTE-BOUND -> TTFT)",
            "left_top_l": "Parallel Prompt Pass",
            "left_top_r": "builds KV state",
            "left_chip1": "High FLOP/Byte",
            "left_chip2": "Prefix Cache",
            "left_foot": "Long prompts stall decode unless chunked",
            "hub_lbl": "roofline",
            "edge_lbl": "splits",
            "right_eyebrow": "PHASE B · DECODE (MEMORY-BW-BOUND -> ITL)",
            "right_row1_l": "1 Token / Step Autoregressive",
            "right_row1_r": "reads weights + KV",
            "right_row2_l": "Disaggregated GPU Pools",
            "right_row2_r": "KV transfer link",
            "right_foot": "Constrained by HBM bandwidth at serving batch sizes",
            "prompt": "Profile Prefill (TTFT, compute-bound) and Decode (ITL/TPOT, HBM-bandwidth-bound) on separate Roofline regimes.",
        },
        "t2": {
            "heading": "KV-Cache Math",
            "desc": "KV bytes = 2 * L * T * H_KV * D_head * b — shrink traffic via GQA, Paged & FlashAttention.",
            "eyebrow": "MEMORY & ATTENTION OPTIMIZATION",
            "in1_l": "PagedAttention + GQA",
            "in1_r": "<4% KV waste",
            "in2_l": "FP8 / INT4 Quant",
            "in2_r": "-50% HBM BW",
            "hub_lbl": "kv-engine",
            "edge_calls": "schedules",
            "edge_returns": "draft verify loop",
            "card1_eyebrow": "CONTINUOUS + CHUNKED PREFILL",
            "card1_title": "Interleave Prefill & Decode",
            "card2_eyebrow": "SPECULATIVE DECODING",
            "card2_title": "Draft Propose · Target Verify",
            "prompt": "Combine FlashAttention, PagedAttention block tables, GQA, FP8 KV quantization, and chunked prefill to stop OOMs.",
        },
        "t3": {
            "heading": "Batching",
            "desc": "Balance Tensor/Pipeline/Expert parallelism and gate capacity on SLO-compliant Goodput.",
            "hub_lbl": "scheduler",
            "check_eyebrow": "SLO GOODPUT & TAIL GATE",
            "check_1": "p99 TTFT & ITL meet user SLO",
            "check_2": "KV occupancy < 85% cliff",
            "fix_lbl": "Chunk prefill / split pools",
            "gate_1": "Goodput SLO met?",
            "gate_2": "KV eviction thrashing?",
            "done_lbl": "Serve High Goodput",
            "stop_lbl": "Autoscale / Shed Load",
            "prompt": "Never size GPU/TPU fleets on raw aggregate tok/s — measure Goodput (requests/sec meeting both TTFT and TPOT SLOs).",
        },
        "t4": {
            "heading": "Goodput SLO",
            "desc": "Raw throughput vanity metrics vs. Roofline-grounded Inference Engineering diagnosis.",
            "left_eyebrow": "SERVING BOTTLENECK SYMPTOMS",
            "left_sub": "High tok/s can still starve TTFT",
            "n1": "Queueing Delay",
            "n2": "KV Fragmentation",
            "n3": "TP All-Reduce",
            "n4": "MoE Imbalance",
            "unlinked_node": "raw_tok_per_sec",
            "unlinked_sub": "ignores p99 TTFT",
            "edge_lbl": "diagnoses",
            "table_header": "INFERENCE ENGINEERING · FAST DIAGNOSIS",
            "rows": [
                {"label": "High TTFT", "ratio": 0.90, "bar_color": "#2563EB", "text_color": "#1D4ED8", "metric": "Chunk Prefill + Prefix"},
                {"label": "High ITL/TPOT", "ratio": 0.94, "bar_color": "#059669", "text_color": "#047857", "metric": "FP8 KV + Speculative"},
                {"label": "Fleet Metric", "ratio": 1.0, "bar_color": "#7C3AED", "text_color": "#6D28D9", "metric": "SLO Goodput (p99)"},
            ],
            "stack": "GKE TPU/GPU + Vertex • vLLM / SGLang",
            "prompt": "High TTFT -> fix queueing/prefill chunking; High TPOT -> cut HBM KV traffic; OOM -> quantize KV + PagedAttention.",
        },
        "footer_left": "INFERENCE ENGINEERING · ROOFLINE, KV-CACHE & GOODPUT",
        "footer_right": "Pallavi Ahuja Lineage • Vertex AI / GKE + vLLM / SGLang",
    },
}


def main() -> None:
    DRAWIO_DIR.mkdir(parents=True, exist_ok=True)
    only_tid = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only_tid = sys.argv[idx + 1]

    targets = [only_tid] if only_tid else list(SPECS_T79_T84.keys())
    for tid in targets:
        if tid not in SPECS_T79_T84:
            raise KeyError(f"Unknown template id: {tid}")
        xml = build_spine_xml(SPECS_T79_T84[tid])
        lower = xml.lower()
        assert "claude" not in lower and "anthropic" not in lower, f"Forbidden vendor token in {tid}"
        out_path = DRAWIO_DIR / f"{tid}.drawio"
        out_path.write_text(xml, encoding="utf-8")
        print(f"[build_t79_t84_drawio] Wrote {out_path} ({len(xml)} bytes)")


if __name__ == "__main__":
    main()
