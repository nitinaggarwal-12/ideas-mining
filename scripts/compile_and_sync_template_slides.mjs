#!/usr/bin/env node
/**
 * ==============================================================================
 * DRAW.IO (.drawio) -> 100% NATIVE EDITABLE PPTX & GOOGLE SLIDES COMPILER
 * ==============================================================================
 * Compiles Draw.io editorial posters (`T01.drawio`, `T53.drawio`..`T68.drawio`)
 * into 100% native editable PowerPoint (.pptx) decks and syncs them to live
 * Google Slides presentations via Server-Side OAuth Refresh Token (Rule 47).
 *
 * Slide Architecture per Template:
 *   - Slide 1: Full-Poster Native Editable Overview (all <mxCell> vertices,
 *     inner pills, badges, toggle switches, tables, and arrows as native shapes)
 *   - Slides 2..N: Full-Width 16:9 Widescreen Section Deep-Dives (each section
 *     band `01`, `02`, `03`, `04` scaled to fill a 13.333" x 7.5" slide with
 *     10pt–16pt native editable cards, code pills, badges, and connectors).
 * ==============================================================================
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const IDEAS_ROOT = path.resolve(__dirname, '..');
const requirePC = createRequire('/Users/nitinagga/Documents/PromptCanvas/package.json');

const PptxGenJS = requirePC('pptxgenjs');
const JSZip = requirePC('jszip');
const { XMLParser } = requirePC('fast-xml-parser');

const DRAWIO_DIR = path.join(IDEAS_ROOT, 'assets/canonical-ref/drawio');
const GALLERY_DIR = path.join(IDEAS_ROOT, 'assets/template-gallery');
const MANIFEST_PATH = path.join(IDEAS_ROOT, 'data/template_google_slides_manifest.json');
const QUOTA_PROJECT = 'ramp-portal-dev';

const TOKEN_PATHS = [
  path.join(IDEAS_ROOT, '.gsheet_oauth_token.json'),
  '/Users/nitinagga/Documents/gantry-pulse/.gsheet_oauth_token.json',
  '/Users/nitinagga/Documents/PromptCanvas/.gsheet_oauth_token.json',
  '/Users/nitinagga/Documents/blogs/.gsheet_oauth_token.json',
];

function decodeHtmlEntities(str = '') {
  return String(str)
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&bull;/g, '•')
    .replace(/&middot;/g, '·')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–')
    .replace(/&rarr;/g, '→')
    .replace(/&larr;/g, '←')
    .replace(/&uarr;/g, '↑')
    .replace(/&darr;/g, '↓')
    .replace(/&harr;/g, '↔')
    .replace(/&ge;/g, '≥')
    .replace(/&le;/g, '≤')
    .replace(/&ne;/g, '≠')
    .replace(/&times;/g, '×')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, dec) => String.fromCodePoint(Number(dec)))
    .replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => String.fromCodePoint(parseInt(hex, 16)))
    .replace(/&amp;/g, '&');
}

function stripTags(html = '') {
  const withoutTags = String(html)
    .replace(/&lt;svg[\s\S]*?&lt;\/svg&gt;/gi, ' ')
    .replace(/<svg[\s\S]*?<\/svg>/gi, ' ')
    .replace(/<\/?[a-zA-Z][^>]*>/g, ' ');
  return decodeHtmlEntities(withoutTags)
    .replace(/<\/?[a-zA-Z][^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function cleanHex(c, fallback = 'FFFFFF') {
  if (!c || c === 'none' || c === 'transparent') return fallback;
  const m = String(c).trim().replace(/^#/, '');
  if (/^[0-9A-Fa-f]{6}$/.test(m)) return m.toUpperCase();
  if (/^[0-9A-Fa-f]{3}$/.test(m)) {
    return m
      .split('')
      .map((ch) => ch + ch)
      .join('')
      .toUpperCase();
  }
  return fallback;
}

function parseStyle(styleStr = '') {
  const out = {};
  for (const part of String(styleStr).split(';')) {
    const t = part.trim();
    if (!t) continue;
    const eq = t.indexOf('=');
    if (eq === -1) out[t] = '1';
    else out[t.slice(0, eq).trim()] = t.slice(eq + 1).trim();
  }
  return out;
}

function parseDrawioXml(xmlStr) {
  const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: '@_',
  });
  const parsed = parser.parse(xmlStr);
  const gm = parsed?.mxfile?.diagram?.mxGraphModel;
  const pageW = Number(gm?.['@_pageWidth'] || 1020);
  const pageH = Number(gm?.['@_pageHeight'] || 1180);
  const bgHex = cleanHex(gm?.['@_background'] || '#FAF8F2', 'FAF8F2');
  const rawCells = gm?.root?.mxCell || [];
  const cellArr = Array.isArray(rawCells) ? rawCells : [rawCells];

  const vertices = [];
  const edges = [];
  const byId = new Map();

  for (const c of cellArr) {
    const id = String(c['@_id'] || '');
    if (id === '0' || id === '1') continue;
    const style = parseStyle(c['@_style'] || '');
    const val = decodeHtmlEntities(c['@_value'] || '');
    const g = c.mxGeometry || {};
    if (c['@_vertex'] === '1') {
      const v = {
        id,
        value: val,
        style,
        x: Number(g['@_x'] || 0),
        y: Number(g['@_y'] || 0),
        w: Number(g['@_width'] || 0),
        h: Number(g['@_height'] || 0),
      };
      vertices.push(v);
      byId.set(id, v);
    } else if (c['@_edge'] === '1') {
      let ox = 0;
      let oy = 0;
      const pts = g.mxPoint ? (Array.isArray(g.mxPoint) ? g.mxPoint : [g.mxPoint]) : [];
      let sourcePt = null;
      let targetPt = null;
      for (const p of pts) {
        if (p['@_as'] === 'offset') {
          ox = Number(p['@_x'] || 0);
          oy = Number(p['@_y'] || 0);
        } else if (p['@_as'] === 'sourcePoint') {
          sourcePt = { x: Number(p['@_x'] || 0), y: Number(g['@_y'] || p['@_y'] || 0) };
        } else if (p['@_as'] === 'targetPoint') {
          targetPt = { x: Number(p['@_x'] || 0), y: Number(p['@_y'] || 0) };
        }
      }
      edges.push({
        id,
        value: String(c['@_value'] || ''),
        style,
        source: c['@_source'] || '',
        target: c['@_target'] || '',
        ox,
        oy,
        sourcePt,
        targetPt,
      });
    }
  }

  return { pageW, pageH, bgHex, vertices, edges, byId };
}

/**
 * Extracts rich structured content from an editorial <mxCell> HTML value:
 * - Top-left category label + top-right pill badge
 * - Bold card title
 * - Subtitle / description text
 * - Bottom monospace formula/code pill
 * - Multi-row key-value comparison table rows
 * - Single-line bottom bar (ROOT CAUSE / PROMPT / GOLDEN RULE)
 */
function inferVisualIcon(cellId = '', title = '', eyebrow = '', eyebrowColor = '2563EB', pillBg = 'DBEAFE') {
  const combined = `${cellId} ${title} ${eyebrow}`.toLowerCase();
  if (cellId === 't1_c1' || /flaky|timeout|503|trigger/.test(combined)) {
    return { iconSymbol: '⚡', iconBg: 'FEE2E2', iconBorder: 'EF4444', iconTextColor: 'DC2626' };
  }
  if (cellId === 't1_c2' || /blind retry|vortex|48x/.test(combined)) {
    return { iconSymbol: '48×', iconBg: 'FEE2E2', iconBorder: 'EF4444', iconTextColor: '991B1B' };
  }
  if (cellId === 't1_c3' || /overflow|crash|\$400/.test(combined)) {
    return { iconSymbol: '$400', iconBg: '0F172A', iconBorder: 'DC2626', iconTextColor: 'FCA5A5' };
  }
  if (cellId === 'b1_hash' || /fingerprint|hash|sha-256/.test(combined)) {
    return { iconSymbol: '🔑', iconBg: 'DBEAFE', iconBorder: '2563EB', iconTextColor: '1D4ED8' };
  }
  if (cellId === 'b2_gate' || /seen|window|turns/.test(combined)) {
    return { iconSymbol: '2/5', iconBg: 'F3E8FF', iconBorder: '7C3AED', iconTextColor: '6D28D9' };
  }
  if (cellId === 'b_exec_ok' || /execute|safe path|allowed/.test(combined)) {
    return { iconSymbol: '✓', iconBg: 'DCFCE7', iconBorder: '10B981', iconTextColor: '047857' };
  }
  if (cellId === 'b_replan' || /switch tool|recovery|replan/.test(combined)) {
    return { iconSymbol: 'ALT', iconBg: 'DCFCE7', iconBorder: '10B981', iconTextColor: '047857' };
  }
  if (cellId === 'b3_pivot' || /block 3rd|pivot|shift/.test(combined)) {
    return { iconSymbol: 'STOP', iconBg: 'FEF3C7', iconBorder: 'D97706', iconTextColor: 'B45309' };
  }
  if (cellId === 'b4_cap' || /fuse|ceiling|\$0\.25/.test(combined)) {
    return { iconSymbol: '$0.25', iconBg: 'F1F5F9', iconBorder: '0F172A', iconTextColor: '0F172A' };
  }
  return {
    iconSymbol: '◆',
    iconBg: pillBg || 'EFF6FF',
    iconBorder: eyebrowColor || '2563EB',
    iconTextColor: eyebrowColor || '1D4ED8',
  };
}

function analyzeCardHtml(html, cellId = '') {
  if (!html) return { kind: 'empty' };

  // 1. Check if this is a multi-row key-value or visual-bar comparison table (e.g. t3_before_rows / t3_after_rows)
  const trMatches = Array.from(html.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi));
  if (trMatches.length >= 2) {
    const rows = [];
    for (const tr of trMatches) {
      const tds = Array.from(tr[1].matchAll(/<td\b([^>]*)>([\s\S]*?)<\/td>/gi));
      if (tds.length >= 3) {
        const leftText = stripTags(tds[0][2]);
        const midHtml = tds[1][2];
        const rightCell = tds[tds.length - 1];
        const rightText = stripTags(rightCell[2]);
        const rColorMatch = (rightCell[1] + rightCell[2]).match(/color\s*:\s*#([0-9A-Fa-f]{6})/i);
        const widths = Array.from(midHtml.matchAll(/width\s*:\s*(\d+)px/gi)).map((m) => Number(m[1]));
        const bgs = Array.from(midHtml.matchAll(/background\s*:\s*#([0-9A-Fa-f]{6})/gi)).map((m) => m[1].toUpperCase());
        const hasBar = widths.length >= 2;
        const barRatio = hasBar ? Math.max(0.06, Math.min(1.0, widths[1] / Math.max(1, widths[0]))) : 0.5;
        rows.push({
          left: leftText,
          right: rightText,
          rightColor: rColorMatch ? rColorMatch[1].toUpperCase() : '0F172A',
          hasBar,
          barRatio,
          trackBg: bgs[0] || 'E2E8F0',
          barBg: bgs[1] || '10B981',
        });
      } else if (tds.length === 2) {
        const leftText = stripTags(tds[0][2]);
        const rightText = stripTags(tds[1][2]);
        const rColorMatch = (tds[1][1] + tds[1][2]).match(/color\s*:\s*#([0-9A-Fa-f]{6})/i);
        rows.push({
          left: leftText,
          right: rightText,
          rightColor: rColorMatch ? rColorMatch[1].toUpperCase() : '0F172A',
          hasBar: false,
          barRatio: 0.5,
          trackBg: 'E2E8F0',
          barBg: '2563EB',
        });
      }
    }
    if (rows.length >= 2) {
      return { kind: 'kv-rows', rows };
    }
  }

  // 2. Check if this is a single-row 3-column bar (ROOT CAUSE / PROMPT / GOLDEN RULE)
  if (trMatches.length === 1) {
    const tds = Array.from(trMatches[0][1].matchAll(/<td\b([^>]*)>([\s\S]*?)<\/td>/gi));
    if (tds.length === 3) {
      const col1 = stripTags(tds[0][2]);
      const col2 = stripTags(tds[1][2]);
      const col3 = stripTags(tds[2][2]);
      const c1Color = (tds[0][2].match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '2563EB';
      const c3Bg = (tds[2][2].match(/background\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '0F172A';
      const c3Color = (tds[2][2].match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || 'FFFFFF';
      return {
        kind: 'prompt-bar',
        tag: col1,
        tagColor: c1Color.toUpperCase(),
        body: col2,
        rightBadge: col3,
        rightBg: c3Bg.toUpperCase(),
        rightColor: c3Color.toUpperCase(),
      };
    }
    if (tds.length === 2) {
      // Section title bar with toggle switch or BEFORE/AFTER table header
      const leftHtml = tds[0][2];
      const rightHtml = tds[1][2];
      const hasToggleOff = />\s*OFF\s*</i.test(rightHtml);
      const hasToggleOn = />\s*ON\s*</i.test(rightHtml);
      if (hasToggleOff || hasToggleOn) {
        const spans = Array.from(leftHtml.matchAll(/<span\b([^>]*)>([\s\S]*?)<\/span>/gi));
        const mainTitle = spans[0] ? stripTags(spans[0][2]) : stripTags(leftHtml);
        const mainColor = ((spans[0]?.[1] || leftHtml).match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '0F172A';
        const subTitle = spans[1] ? stripTags(spans[1][2]) : '';
        return {
          kind: 'section-header',
          title: mainTitle,
          titleColor: mainColor.toUpperCase(),
          subtitle: subTitle,
          toggleState: hasToggleOn ? 'ON' : 'OFF',
        };
      }
      // 2-column card header (e.g. BEFORE · UNPROTECTED AGENT | GUARD OFF) or 2-column pill (e.g. Your prompt | the current request)
      const leftText = stripTags(leftHtml);
      const rightText = stripTags(rightHtml);
      const lColor = (leftHtml.match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '0F172A';
      const rBgMatch = rightHtml.match(/background\s*:\s*#([0-9A-Fa-f]{6})/i);
      const rColor = ((rightHtml + tds[1][1]).match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '0F172A';
      return {
        kind: 'card-banner-header',
        leftText,
        leftColor: lColor.toUpperCase(),
        rightText,
        hasRightPill: Boolean(rBgMatch),
        rightBg: (rBgMatch ? rBgMatch[1] : 'E2E8F0').toUpperCase(),
        rightColor: rColor.toUpperCase(),
      };
    }
  }

  // 3. Process Card with Top Eyebrow + Right Pill + Visual Icon + Title + Formula Pill
  if (html.includes('justify-content:space-between') && !cellId.includes('header')) {
    const topFlexMatch = html.match(/<div\b[^>]*justify-content\s*:\s*space-between[^>]*>([\s\S]*?)<\/div>/i);
    let eyebrow = '';
    let eyebrowColor = '1D4ED8';
    let pillText = '';
    let pillBg = 'DBEAFE';
    let pillColor = '1E40AF';
    if (topFlexMatch) {
      const spans = Array.from(topFlexMatch[1].matchAll(/<span\b([^>]*)>([\s\S]*?)<\/span>/gi));
      if (spans[0]) {
        eyebrow = stripTags(spans[0][2]);
        eyebrowColor = ((spans[0][1] || '').match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '1D4ED8';
      }
      if (spans[1]) {
        pillText = stripTags(spans[1][2]);
        pillBg = ((spans[1][1] || '').match(/background\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || 'DBEAFE';
        pillColor = ((spans[1][1] || '').match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '1E40AF';
      }
    }
    let restHtml = topFlexMatch ? html.replace(topFlexMatch[0], '') : html;
    restHtml = restHtml.replace(/^<div\s+style="[^"]*box-sizing:border-box[^"]*">/i, '').replace(/<\/div>\s*$/i, '');
    const divBlocks = Array.from(restHtml.matchAll(/<div\b([^>]*)>([\s\S]*?)<\/div>/gi));
    let title = '';
    let desc = '';
    let codeText = '';
    let codeBg = 'F1F5F9';
    let codeBorder = 'CBD5E1';
    let codeColor = '0F172A';

    for (const db of divBlocks) {
      const styleAttr = db[1] || '';
      const inner = stripTags(db[2]);
      if (!inner) continue;
      if (styleAttr.includes('monospace')) {
        codeText = inner;
        codeBg = (styleAttr.match(/background\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || 'F1F5F9';
        codeBorder = (styleAttr.match(/border\s*:\s*1px solid #([0-9A-Fa-f]{6})/i) || [])[1] || 'CBD5E1';
        codeColor = (styleAttr.match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '0F172A';
      } else if (!title && /font-weight\s*:\s*800/i.test(styleAttr)) {
        title = inner;
      } else if (!desc) {
        desc = inner;
      }
    }

    if (title) {
      const iconMeta = inferVisualIcon(cellId, title, eyebrow, eyebrowColor.toUpperCase(), pillBg.toUpperCase());
      return {
        kind: 'process-card',
        eyebrow,
        eyebrowColor: eyebrowColor.toUpperCase(),
        pillText,
        pillBg: pillBg.toUpperCase(),
        pillColor: pillColor.toUpperCase(),
        title,
        desc,
        codeText,
        codeBg: codeBg.toUpperCase(),
        codeBorder: codeBorder.toUpperCase(),
        codeColor: codeColor.toUpperCase(),
        ...iconMeta,
      };
    }
  }

  // 4. Poster Main Header (header_title)
  if (cellId === 'header_title' || /font-size\s*:\s*3[0-9]px/i.test(html)) {
    const topFlexBar = html.match(/<div\b[^>]*justify-content\s*:\s*space-between[^>]*>([\s\S]*?)<\/div>/i);
    let kpiLeft = 'GOOGLE CLOUD ADK + VERTEX AI • OPENHANDS + LANGGRAPH';
    let kpiRight = 'ARCHITECTURE BLUEPRINT';
    if (topFlexBar) {
      const topSpans = Array.from(topFlexBar[1].matchAll(/<span\b([^>]*)>([\s\S]*?)<\/span>/gi));
      if (topSpans.length >= 2) {
        kpiLeft = stripTags(topSpans[0][2]);
        kpiRight = stripTags(topSpans[1][2]);
      }
    }
    const bodyHtml = topFlexBar ? html.replace(topFlexBar[0], '') : html;
    const lines = bodyHtml
      .split(/<br\s*\/?>/i)
      .map((l) => stripTags(l))
      .filter(Boolean);
    return {
      kind: 'poster-header',
      kpiLeft,
      kpiRight,
      headline: lines[0] || stripTags(bodyHtml),
      subtitle: lines.slice(1).join(' '),
    };
  }

  // 5. Simple Section Title without Toggle (e.g. t3_title)
  const spans = Array.from(html.matchAll(/<span\b([^>]*)>([\s\S]*?)<\/span>/gi));
  if (spans.length >= 2 && /font-size\s*:\s*(?:18|19|20|21|22)px/i.test(spans[0][1])) {
    const tColor = ((spans[0][1] || '').match(/color\s*:\s*#([0-9A-Fa-f]{6})/i) || [])[1] || '059669';
    return {
      kind: 'section-header',
      title: stripTags(spans[0][2]),
      titleColor: tColor.toUpperCase(),
      subtitle: stripTags(spans[1][2]),
      toggleState: null,
    };
  }

  // 6. Default multi-line or single-line text
  const plain = stripTags(html);
  return { kind: 'plain', text: plain };
}

/**
 * Renders a set of Draw.io vertices & edges onto a PptxGenJS slide within a target viewport
 * as 100% native editable vector shapes, pills, toggles, tables, and connectors.
 */
function renderCellsToSlide(pptx, slide, vertices, edges, byId, cropBox, slideBox, fontScale = 1.0, maxStretchY = 1.48) {
  const scaleX = slideBox.w / cropBox.w;
  const rawScaleY = slideBox.h / cropBox.h;
  const scaleW = Math.min(scaleX, rawScaleY);
  const scaleH = Math.min(rawScaleY, scaleW * maxStretchY);
  const offsetX = slideBox.x + (slideBox.w - cropBox.w * scaleW) / 2;
  const offsetY = slideBox.y + (slideBox.h - cropBox.h * scaleH) / 2;
  const effScale = Math.sqrt(scaleW * scaleH);

  const sx = (x) => Number((offsetX + (x - cropBox.x) * scaleW).toFixed(3));
  const sy = (y) => Number((offsetY + (y - cropBox.y) * scaleH).toFixed(3));
  const sw = (w) => Number(Math.max(0.05, w * scaleW).toFixed(3));
  const sh = (h) => Number(Math.max(0.05, h * scaleH).toFixed(3));
  const pt = (px) => Number(Math.max(6.5, px * effScale * 54 * fontScale).toFixed(1));

  // Filter vertices inside cropBox
  const activeVertices = vertices.filter((v) => {
    if (v.id === 'poster_bg' || v.id === 'bg') return false;
    const cx = v.x + v.w / 2;
    const cy = v.y + v.h / 2;
    return cx >= cropBox.x - 10 && cx <= cropBox.x + cropBox.w + 10 && cy >= cropBox.y - 10 && cy <= cropBox.y + cropBox.h + 10;
  });

  // Sort: background cards/enclaves first, smaller foreground cards/badges on top
  activeVertices.sort((a, b) => b.w * b.h - a.w * a.h);

  for (const v of activeVertices) {
    const x = sx(v.x);
    const y = sy(v.y);
    const w = sw(v.w);
    const isCircleOrSquareBadge = v.style.ellipse === '1' || v.style.shape === 'ellipse' || /^badge_\d+$/.test(v.id);
    const h = isCircleOrSquareBadge ? sw(v.h) : sh(v.h);
    const st = v.style;
    const hasFill = st.fillColor && st.fillColor !== 'none' && st.fillColor !== 'transparent';
    const hasStroke = st.strokeColor && st.strokeColor !== 'none' && st.strokeColor !== 'transparent';
    const fillHex = cleanHex(st.fillColor, 'FFFFFF');
    const strokeHex = cleanHex(st.strokeColor, 'CBD5E1');
    const isDashed = st.dashed === '1';
    const isEllipse = st.ellipse === '1' || st.shape === 'ellipse';
    const isRounded = st.rounded === '1';

    const info = analyzeCardHtml(v.value, v.id);

    // Draw base container shape if it has fill or stroke
    if (hasFill || hasStroke) {
      let shapeType = pptx.ShapeType.rect;
      if (isEllipse) shapeType = pptx.ShapeType.ellipse;
      else if (isRounded) shapeType = pptx.ShapeType.roundRect;

      slide.addShape(shapeType, {
        x,
        y,
        w,
        h,
        rectRadius: shapeType === pptx.ShapeType.roundRect ? (Number(st.arcSize || 10) >= 35 ? 0.25 : 0.05) : undefined,
        fill: hasFill ? { color: fillHex } : undefined,
        line: hasStroke
          ? {
              color: strokeHex,
              width: Number(st.strokeWidth || 1) * 0.75,
              dashType: isDashed ? 'dash' : 'solid',
            }
          : undefined,
      });

      // If this is an SVG-icon ellipse (e.g., t1_model_circle), draw the inner blue hub badge natively
      if (isEllipse && /<svg/i.test(v.value)) {
        const innerR = Math.min(w, h) * 0.52;
        slide.addShape(pptx.ShapeType.ellipse, {
          x: Number((x + (w - innerR) / 2).toFixed(3)),
          y: Number((y + (h - innerR) / 2).toFixed(3)),
          w: Number(innerR.toFixed(3)),
          h: Number(innerR.toFixed(3)),
          fill: { color: 'EFF6FF' },
          line: { color: '2563EB', width: 1.5 },
        });
        const coreR = Math.min(w, h) * 0.18;
        slide.addShape(pptx.ShapeType.ellipse, {
          x: Number((x + (w - coreR) / 2).toFixed(3)),
          y: Number((y + (h - coreR) / 2).toFixed(3)),
          w: Number(coreR.toFixed(3)),
          h: Number(coreR.toFixed(3)),
          fill: { color: '2563EB' },
        });
      }
    }

    if (info.kind === 'empty') continue;

    if (info.kind === 'poster-header') {
      slide.addText(info.kpiLeft, {
        x,
        y,
        w: Number((w * 0.68).toFixed(3)),
        h: Number((h * 0.24).toFixed(3)),
        fontSize: pt(11.0),
        bold: true,
        color: '1E40AF',
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      const pillW = Math.min(w * 0.30, sw(235));
      const pillH = Math.max(0.18, h * 0.22);
      slide.addShape(pptx.ShapeType.roundRect, {
        x: Number((x + w - pillW).toFixed(3)),
        y: Number((y + 0.01).toFixed(3)),
        w: Number(pillW.toFixed(3)),
        h: Number(pillH.toFixed(3)),
        rectRadius: 0.2,
        fill: { color: '0F172A' },
      });
      slide.addText(info.kpiRight, {
        x: Number((x + w - pillW).toFixed(3)),
        y: Number((y + 0.01).toFixed(3)),
        w: Number(pillW.toFixed(3)),
        h: Number(pillH.toFixed(3)),
        fontSize: pt(9.0),
        bold: true,
        color: 'FFFFFF',
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });
      slide.addText(info.headline, {
        x,
        y: Number((y + h * 0.26).toFixed(3)),
        w,
        h: Number((h * 0.44).toFixed(3)),
        fontSize: pt(24),
        bold: true,
        color: '0F172A',
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      if (info.subtitle) {
        slide.addText(info.subtitle, {
          x,
          y: Number((y + h * 0.72).toFixed(3)),
          w,
          h: Number((h * 0.26).toFixed(3)),
          fontSize: pt(12.5),
          color: '475569',
          fontFace: 'Arial',
          valign: 'middle',
          margin: 0,
        });
      }
      continue;
    }

    if (info.kind === 'section-header') {
      slide.addText(
        [
          { text: `${info.title}   `, options: { fontSize: pt(16.8), bold: true, color: info.titleColor } },
          { text: info.subtitle || '', options: { fontSize: pt(10.6), bold: true, color: '475569' } },
        ],
        {
          x,
          y,
          w: Number((w * 0.845).toFixed(3)),
          h,
          fontFace: 'Arial',
          valign: 'middle',
          margin: 0,
        }
      );

      const isOff = info.toggleState === 'OFF';
      const badgeLabel = info.toggleState ? `LOOP GUARD ${info.toggleState}` : 'VERIFIED PROOF';
      const badgeW = sw(126);
      const badgeH = Math.min(h * 0.88, 0.34);
      const badgeX = x + w - badgeW;
      const badgeY = y + (h - badgeH) / 2;
      slide.addShape(pptx.ShapeType.roundRect, {
        x: Number(badgeX.toFixed(3)),
        y: Number(badgeY.toFixed(3)),
        w: Number(badgeW.toFixed(3)),
        h: Number(badgeH.toFixed(3)),
        rectRadius: 0.2,
        fill: { color: isOff ? 'FEF2F2' : 'ECFDF5' },
        line: { color: isOff ? 'FCA5A5' : '6EE7B7', width: 0.85 },
      });
      slide.addText(badgeLabel, {
        x: Number((badgeX + sw(6)).toFixed(3)),
        y: Number(badgeY.toFixed(3)),
        w: Number((badgeW - sw(12)).toFixed(3)),
        h: Number(badgeH.toFixed(3)),
        fontSize: pt(9.0),
        bold: true,
        color: isOff ? '991B1B' : '065F46',
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });
      continue;
    }

    if (info.kind === 'process-card') {
      const padX = sw(10);
      const topY = y + h * 0.06;
      const topH = Math.min(0.24, h * 0.15);
      // Left Eyebrow
      slide.addText(info.eyebrow, {
        x: Number((x + padX).toFixed(3)),
        y: Number(topY.toFixed(3)),
        w: Number((w * 0.58).toFixed(3)),
        h: Number(topH.toFixed(3)),
        fontSize: pt(8.8),
        bold: true,
        color: info.eyebrowColor,
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      // Right Badge Pill
      if (info.pillText) {
        const pW = Math.min(w * 0.38, sw(76));
        const pX = x + w - padX - pW;
        slide.addShape(pptx.ShapeType.roundRect, {
          x: Number(pX.toFixed(3)),
          y: Number(topY.toFixed(3)),
          w: Number(pW.toFixed(3)),
          h: Number(topH.toFixed(3)),
          rectRadius: 0.2,
          fill: { color: info.pillBg },
        });
        slide.addText(info.pillText, {
          x: Number(pX.toFixed(3)),
          y: Number(topY.toFixed(3)),
          w: Number(pW.toFixed(3)),
          h: Number(topH.toFixed(3)),
          fontSize: pt(8.0),
          bold: true,
          color: info.pillColor,
          align: 'center',
          valign: 'middle',
          fontFace: 'Arial',
          margin: 0,
        });
      }

      // Centered Circular Visual Icon Badge (Visual-First Node!)
      const iconD = Number(Math.min(0.46, h * 0.28).toFixed(3));
      const iconX = Number((x + (w - iconD) / 2).toFixed(3));
      const iconY = Number((y + h * 0.23).toFixed(3));
      slide.addShape(pptx.ShapeType.ellipse, {
        x: iconX,
        y: iconY,
        w: iconD,
        h: iconD,
        fill: { color: info.iconBg || 'EFF6FF' },
        line: { color: info.iconBorder || info.eyebrowColor, width: 1.2 },
      });
      slide.addText(info.iconSymbol || '◆', {
        x: iconX,
        y: iconY,
        w: iconD,
        h: iconD,
        fontSize: pt(9.6),
        bold: true,
        color: info.iconTextColor || info.eyebrowColor,
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });

      // Bold Centered 2-3 Word Visual Title
      slide.addText(info.title, {
        x: Number((x + padX).toFixed(3)),
        y: Number((y + h * 0.53).toFixed(3)),
        w: Number((w - padX * 2).toFixed(3)),
        h: Number((h * 0.19).toFixed(3)),
        fontSize: pt(12.8),
        bold: true,
        color: '0F172A',
        align: 'center',
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });

      // Bottom Compact Formula / Tag Pill
      const bottomTag = info.codeText || info.desc;
      if (bottomTag) {
        const cX = x + padX;
        const cY = y + h * 0.75;
        const cW = w - padX * 2;
        const cH = Math.min(0.28, h * 0.18);
        slide.addShape(pptx.ShapeType.roundRect, {
          x: Number(cX.toFixed(3)),
          y: Number(cY.toFixed(3)),
          w: Number(cW.toFixed(3)),
          h: Number(cH.toFixed(3)),
          rectRadius: 0.06,
          fill: { color: info.codeBg },
          line: { color: info.codeBorder, width: 0.6 },
        });
        slide.addText(bottomTag.length > 34 ? `${bottomTag.slice(0, 32)}..` : bottomTag, {
          x: Number(cX.toFixed(3)),
          y: Number(cY.toFixed(3)),
          w: Number(cW.toFixed(3)),
          h: Number(cH.toFixed(3)),
          fontSize: pt(8.8),
          bold: true,
          color: info.codeColor,
          align: 'center',
          valign: 'middle',
          fontFace: 'Courier New',
          margin: 0,
        });
      }
      continue;
    }

    if (info.kind === 'card-banner-header') {
      const padX = sw(12);
      slide.addText(info.leftText, {
        x: Number((x + padX).toFixed(3)),
        y,
        w: Number((w * (info.hasRightPill ? 0.72 : 0.56)).toFixed(3)),
        h,
        fontSize: pt(10.8),
        bold: true,
        color: info.leftColor,
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      if (info.hasRightPill) {
        const rW = sw(76);
        const rH = Math.min(0.24, h * 0.74);
        const rX = x + w - padX - rW;
        const rY = y + (h - rH) / 2;
        const sameAsBanner = info.rightBg === fillHex;
        const pillFill = sameAsBanner ? (fillHex === 'FEE2E2' ? 'DC2626' : '0F172A') : info.rightBg;
        const pillTextCol = sameAsBanner ? 'FFFFFF' : info.rightColor;
        slide.addShape(pptx.ShapeType.roundRect, {
          x: Number(rX.toFixed(3)),
          y: Number(rY.toFixed(3)),
          w: Number(rW.toFixed(3)),
          h: Number(rH.toFixed(3)),
          rectRadius: 0.2,
          fill: { color: pillFill },
        });
        slide.addText(info.rightText, {
          x: Number(rX.toFixed(3)),
          y: Number(rY.toFixed(3)),
          w: Number(rW.toFixed(3)),
          h: Number(rH.toFixed(3)),
          fontSize: pt(8.5),
          bold: true,
          color: pillTextCol,
          align: 'center',
          valign: 'middle',
          fontFace: 'Arial',
          margin: 0,
        });
      } else {
        slide.addText(info.rightText, {
          x: Number((x + padX + w * 0.44).toFixed(3)),
          y,
          w: Number((w * 0.56 - padX * 2).toFixed(3)),
          h,
          fontSize: pt(10.2),
          bold: true,
          color: info.rightColor,
          align: 'right',
          valign: 'middle',
          fontFace: 'Arial',
          margin: 0,
        });
      }
      continue;
    }

    if (info.kind === 'kv-rows') {
      const padX = sw(14);
      const rowH = h / info.rows.length;
      const innerW = w - padX * 2;
      info.rows.forEach((r, idx) => {
        const ry = y + idx * rowH;
        if (idx < info.rows.length - 1) {
          slide.addShape(pptx.ShapeType.line, {
            x: Number((x + padX).toFixed(3)),
            y: Number((ry + rowH).toFixed(3)),
            w: Number(innerW.toFixed(3)),
            h: 0,
            line: { color: 'CBD5E1', width: 0.5 },
          });
        }
        if (r.hasBar) {
          // 3-Column Visual Gauge Row: Left Label (32%) | Horizontal Bar Gauge (40%) | Right Metric (28%)
          const leftW = innerW * 0.33;
          const barW = innerW * 0.37;
          const rightW = innerW * 0.30;
          const barX = x + padX + leftW;
          const barH = Math.min(0.14, rowH * 0.26);
          const barY = ry + (rowH - barH) / 2;

          slide.addText(r.left, {
            x: Number((x + padX).toFixed(3)),
            y: Number(ry.toFixed(3)),
            w: Number(leftW.toFixed(3)),
            h: Number(rowH.toFixed(3)),
            fontSize: pt(10.5),
            bold: true,
            color: '0F172A',
            align: 'left',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
          // Track Bar
          slide.addShape(pptx.ShapeType.roundRect, {
            x: Number(barX.toFixed(3)),
            y: Number(barY.toFixed(3)),
            w: Number(barW.toFixed(3)),
            h: Number(barH.toFixed(3)),
            rectRadius: 0.2,
            fill: { color: r.trackBg },
          });
          // Active Fill Bar
          slide.addShape(pptx.ShapeType.roundRect, {
            x: Number(barX.toFixed(3)),
            y: Number(barY.toFixed(3)),
            w: Number(Math.max(0.10, barW * r.barRatio).toFixed(3)),
            h: Number(barH.toFixed(3)),
            rectRadius: 0.2,
            fill: { color: r.barBg },
          });
          slide.addText(r.right, {
            x: Number((barX + barW).toFixed(3)),
            y: Number(ry.toFixed(3)),
            w: Number(rightW.toFixed(3)),
            h: Number(rowH.toFixed(3)),
            fontSize: pt(10.5),
            bold: true,
            color: r.rightColor,
            align: 'right',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
        } else {
          slide.addText(r.left, {
            x: Number((x + padX).toFixed(3)),
            y: Number(ry.toFixed(3)),
            w: Number((innerW * 0.36).toFixed(3)),
            h: Number(rowH.toFixed(3)),
            fontSize: pt(10.5),
            bold: true,
            color: '0F172A',
            align: 'left',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
          slide.addText(r.right, {
            x: Number((x + padX + innerW * 0.36).toFixed(3)),
            y: Number(ry.toFixed(3)),
            w: Number((innerW * 0.64).toFixed(3)),
            h: Number(rowH.toFixed(3)),
            fontSize: pt(10.2),
            bold: true,
            color: r.rightColor,
            align: 'right',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
        }
      });
      continue;
    }

    if (info.kind === 'prompt-bar') {
      const padX = sw(12);
      const tagW = Math.max(sw(108), sw((info.tag?.length || 10) * 8.4 + 14));
      const isUpCircle = info.rightBadge === '↑';
      const rightW = isUpCircle ? Math.min(0.28, h * 0.64) : sw(68);
      slide.addText(info.tag, {
        x: Number((x + padX).toFixed(3)),
        y,
        w: Number(tagW.toFixed(3)),
        h,
        fontSize: pt(9.8),
        bold: true,
        color: info.tagColor,
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      slide.addText(info.body, {
        x: Number((x + padX + tagW).toFixed(3)),
        y,
        w: Number((w - padX * 2 - tagW - rightW - sw(8)).toFixed(3)),
        h,
        fontSize: pt(10.6),
        bold: true,
        color: '0F172A',
        fontFace: 'Arial',
        valign: 'middle',
        margin: 0,
      });
      const rH = isUpCircle ? rightW : Math.min(0.26, h * 0.68);
      const rX = x + w - padX - rightW;
      const rY = y + (h - rH) / 2;
      slide.addShape(isUpCircle ? pptx.ShapeType.ellipse : pptx.ShapeType.roundRect, {
        x: Number(rX.toFixed(3)),
        y: Number(rY.toFixed(3)),
        w: Number(rightW.toFixed(3)),
        h: Number(rH.toFixed(3)),
        rectRadius: isUpCircle ? undefined : 0.2,
        fill: { color: info.rightBg },
      });
      slide.addText(info.rightBadge, {
        x: Number(rX.toFixed(3)),
        y: Number(rY.toFixed(3)),
        w: Number(rightW.toFixed(3)),
        h: Number(rH.toFixed(3)),
        fontSize: pt(8.8),
        bold: true,
        color: info.rightColor,
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });
      continue;
    }

    if (info.kind === 'plain' && info.text) {
      const fSize = Number(st.fontSize || 11);
      const fColor = cleanHex(st.fontColor || (fillHex === '0F172A' ? 'FFFFFF' : '0F172A'), '0F172A');
      slide.addText(info.text, {
        x,
        y,
        w,
        h,
        fontSize: pt(fSize),
        bold: st.fontStyle === '1' || /<b>/i.test(v.value),
        color: fColor,
        align: st.align || 'center',
        valign: st.verticalAlign || 'middle',
        fontFace: 'Arial',
        margin: 0,
        wrap: true,
      });
    }
  }

  // Render Connectors (Edges) inside cropBox
  for (const e of edges) {
    if (e.id === 'spine_line' && cropBox.h < 800) continue;
    let x1, y1, x2, y2;
    if (e.source && e.target && byId.has(e.source) && byId.has(e.target)) {
      const s = byId.get(e.source);
      const t = byId.get(e.target);
      const exX = e.style.exitX !== undefined ? Number(e.style.exitX) : s.x + s.w <= t.x ? 1 : s.x >= t.x + t.w ? 0 : 0.5;
      const exY = e.style.exitY !== undefined ? Number(e.style.exitY) : s.y + s.h <= t.y ? 1 : s.y >= t.y + t.h ? 0 : 0.5;
      const enX = e.style.entryX !== undefined ? Number(e.style.entryX) : s.x + s.w <= t.x ? 0 : s.x >= t.x + t.w ? 1 : 0.5;
      const enY = e.style.entryY !== undefined ? Number(e.style.entryY) : s.y + s.h <= t.y ? 0 : s.y >= t.y + t.h ? 1 : 0.5;
      x1 = s.x + s.w * exX;
      y1 = s.y + s.h * exY;
      x2 = t.x + t.w * enX;
      y2 = t.y + t.h * enY;
    } else if (e.sourcePt && e.targetPt) {
      x1 = e.sourcePt.x;
      y1 = e.sourcePt.y;
      x2 = e.targetPt.x;
      y2 = e.targetPt.y;
    } else {
      continue;
    }

    const midX = (x1 + x2) / 2;
    const midY = (y1 + y2) / 2;
    if (midX < cropBox.x - 15 || midX > cropBox.x + cropBox.w + 15 || midY < cropBox.y - 15 || midY > cropBox.y + cropBox.h + 15) {
      continue;
    }

    const sx1 = sx(x1);
    const sy1 = sy(y1);
    const sx2 = sx(x2);
    const sy2 = sy(y2);
    const lineX = Math.min(sx1, sx2);
    const lineY = Math.min(sy1, sy2);
    const lineW = Math.max(0.001, Math.abs(sx2 - sx1));
    const lineH = Math.max(0.001, Math.abs(sy2 - sy1));
    const strokeHex = cleanHex(e.style.strokeColor, '475569');
    const hasArrow = e.style.endArrow !== 'none' && e.style.endArrow !== 'oval';

    slide.addShape(pptx.ShapeType.line, {
      x: Number(lineX.toFixed(3)),
      y: Number(lineY.toFixed(3)),
      w: Number(lineW.toFixed(3)),
      h: Number(lineH.toFixed(3)),
      flipH: sx2 < sx1,
      flipV: sy2 < sy1,
      line: {
        color: strokeHex,
        width: Math.max(1.0, Number(e.style.strokeWidth || 1.5) * 0.8),
        endArrowType: hasArrow ? 'triangle' : 'none',
      },
    });

    const lblText = stripTags(e.value);
    if (lblText) {
      const lblW = Math.max(sw(48), sw(lblText.length * 6.8 + 12));
      const lblH = Math.min(0.24, sh(17));
      const lx = sx(midX + (e.ox || 0)) - lblW / 2;
      const ly = sy(midY + (e.oy || 0)) - lblH / 2;
      const lblBg = cleanHex(e.style.labelBackgroundColor, 'FFFFFF');
      const lblColor = cleanHex(e.style.fontColor, strokeHex);

      slide.addShape(pptx.ShapeType.roundRect, {
        x: Number(lx.toFixed(3)),
        y: Number(ly.toFixed(3)),
        w: Number(lblW.toFixed(3)),
        h: Number(lblH.toFixed(3)),
        rectRadius: 0.12,
        fill: { color: lblBg },
      });
      slide.addText(lblText, {
        x: Number(lx.toFixed(3)),
        y: Number(ly.toFixed(3)),
        w: Number(lblW.toFixed(3)),
        h: Number(lblH.toFixed(3)),
        fontSize: pt(9.8),
        bold: true,
        color: lblColor,
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });
    }
  }
}

async function postProcessArrowheads(base64Pptx) {
  const zip = await JSZip.loadAsync(Buffer.from(base64Pptx, 'base64'));
  for (const fileName of Object.keys(zip.files)) {
    if (/^ppt\/slides\/slide\d+\.xml$/.test(fileName)) {
      const xml = await zip.files[fileName].async('string');
      const updated = xml.replace(/<a:tailEnd\s+type="triangle"(?!\s+w=)\s*\/>/g, '<a:tailEnd type="triangle" w="sm" len="sm"/>');
      if (updated !== xml) zip.file(fileName, updated);
    }
  }
  return zip.generateAsync({ type: 'nodebuffer' });
}

/**
 * Extracts visual-first flow nodes and horizontal gauge bars from a section band
 * so Slide 1 (Executive Visual Map) renders connected icon nodes + native bar charts
 * with zero walls of text.
 */
function extractBandHighlights(band, vertices, idx) {
  const bandCells = vertices
    .filter((v) => v.id !== band.id && v.y >= band.y - 8 && v.y + v.h <= band.y + band.h + 12)
    .sort((a, b) => (Math.abs(a.y - b.y) > 20 ? a.y - b.y : a.x - b.x));

  const titleCell = bandCells.find((v) => v.w >= 300 && v.h <= 45) || bandCells[0];
  const titleInfo = analyzeCardHtml(titleCell?.value || '', titleCell?.id || '');
  const secTitle = titleInfo.title || `Section 0${idx + 1}`;
  const secSub = titleInfo.subtitle || 'Visual flow & runtime gauges.';
  const secColor = titleInfo.titleColor || (idx === 0 ? 'DC2626' : idx === 1 ? '2563EB' : idx === 2 ? '059669' : '7C3AED');
  const toggleState = titleInfo.toggleState;

  const items = [];
  const kvTables = [];
  let promptBar = null;

  for (const c of bandCells) {
    if (c === titleCell) continue;
    const inf = analyzeCardHtml(c.value, c.id);
    if (inf.kind === 'process-card') {
      items.push({
        isGaugeCard: false,
        eyebrow: inf.eyebrow || `STEP 0${items.length + 1}`,
        eyebrowColor: inf.eyebrowColor || secColor,
        pillText: inf.pillText || '',
        pillBg: inf.pillBg || 'EFF6FF',
        pillColor: inf.pillColor || secColor,
        title: inf.title,
        codeText: inf.codeText || '',
        iconSymbol: inf.iconSymbol || '◆',
        iconBg: inf.iconBg || 'EFF6FF',
        iconBorder: inf.iconBorder || secColor,
        iconTextColor: inf.iconTextColor || secColor,
      });
    } else if (inf.kind === 'kv-rows') {
      kvTables.push(inf);
    } else if (inf.kind === 'prompt-bar') {
      promptBar = inf;
    } else if (inf.kind === 'card-banner-header' && !inf.hasRightPill && items.length < 4) {
      items.push({
        isGaugeCard: false,
        eyebrow: 'MODULE',
        eyebrowColor: secColor,
        pillText: inf.rightText,
        pillBg: 'F1F5F9',
        pillColor: inf.rightColor || '334155',
        title: inf.leftText,
        codeText: '',
        iconSymbol: `0${items.length + 1}`,
        iconBg: 'EFF6FF',
        iconBorder: secColor,
        iconTextColor: secColor,
      });
    } else if (inf.kind === 'plain' && inf.text && c.w >= 110 && c.h >= 24 && items.length < 4 && !/^(01|02|03|04)$/.test(inf.text)) {
      items.push({
        isGaugeCard: false,
        eyebrow: `STEP 0${items.length + 1}`,
        eyebrowColor: secColor,
        pillText: '',
        pillBg: 'EFF6FF',
        pillColor: secColor,
        title: inf.text.slice(0, 38),
        codeText: '',
        iconSymbol: `0${items.length + 1}`,
        iconBg: 'EFF6FF',
        iconBorder: secColor,
        iconTextColor: secColor,
      });
    }
  }

  if (kvTables.length >= 2) {
    const beforeRows = kvTables[0].rows || [];
    const afterRows = kvTables[1].rows || [];
    const pairCount = Math.min(3, Math.max(beforeRows.length, afterRows.length));
    for (let i = 0; i < pairCount; i++) {
      const rb = beforeRows[i] || afterRows[i];
      const ra = afterRows[i] || beforeRows[i];
      items.push({
        isGaugeCard: true,
        title: rb.left,
        pillText: ra.right,
        pillBg: 'DCFCE7',
        pillColor: '065F46',
        beforeVal: rb.right,
        afterVal: ra.right,
        beforeRatio: rb.hasBar ? rb.barRatio : i === 2 ? 0.08 : 0.96,
        afterRatio: ra.hasBar ? ra.barRatio : i === 2 ? 0.94 : 0.12,
      });
    }
  } else if (kvTables.length === 1) {
    for (const r of kvTables[0].rows.slice(0, 3)) {
      items.push({
        isGaugeCard: false,
        eyebrow: 'METRIC',
        eyebrowColor: r.rightColor || secColor,
        pillText: r.right,
        pillBg: r.rightColor === 'B91C1C' ? 'FEE2E2' : 'DCFCE7',
        pillColor: r.rightColor || '065F46',
        title: r.left,
        codeText: r.right,
        iconSymbol: '📊',
        iconBg: 'ECFDF5',
        iconBorder: '10B981',
        iconTextColor: '047857',
      });
    }
  }

  return {
    secTitle,
    secSub,
    secColor,
    toggleState,
    items: items.slice(0, 4),
    promptBar,
  };
}

export async function compileDrawioTemplateToEditablePptx(tid, titleHint = '') {
  const xmlPath = path.join(DRAWIO_DIR, `${tid}.drawio`);
  const xmlStr = fs.readFileSync(xmlPath, 'utf8');
  const { pageW, pageH, bgHex, vertices, edges, byId } = parseDrawioXml(xmlStr);

  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_WIDE'; // 13.333" x 7.5"
  pptx.author = 'Google Cloud Architecture Center • Agentic AI Studio';
  pptx.company = 'Google Cloud';
  pptx.title = `${tid} — ${titleHint || 'Editable Architecture Poster & Section Deck'}`;

  // Identify major horizontal section bands (`t1_card`, `t2_card`, `t3_card`, `t4_card` or `band*_1`..`band*_4`)
  let sectionBands = vertices
    .filter((v) => /^t\d+_card$/.test(v.id) || /^band\d*_\d+$/.test(v.id))
    .sort((a, b) => a.y - b.y);
  if (sectionBands.length === 0) {
    const candidates = vertices
      .filter((v) => v.w >= pageW * 0.78 && v.h >= 150 && v.h <= pageH * 0.55 && v.y >= 90 && !v.id.includes('enclave'))
      .sort((a, b) => a.y - b.y);
    sectionBands = candidates.filter(
      (c, i) => !candidates.some((other, j) => i !== j && c.y >= other.y && c.y + c.h <= other.y + other.h)
    );
  }
  if (sectionBands.length === 0) {
    sectionBands = [{ id: 'widescreen_canvas', x: 20, y: 84, w: pageW - 40, h: pageH - 104 }];
  }

  const hdrCell = vertices.find((v) => v.id === 'header_title') || vertices[0];
  const hdrInfo = analyzeCardHtml(hdrCell?.value || '', hdrCell?.id || '');
  const posterHeadline = hdrInfo.headline || titleHint || `${tid} Architecture Blueprint`;
  const posterSub = hdrInfo.subtitle || '100% Native Editable Google Slides & Draw.io Vector Architecture';
  const kpiLeft = hdrInfo.kpiLeft || 'GOOGLE CLOUD ADK + VERTEX AI • OPENHANDS + LANGGRAPH';
  const kpiRight = hdrInfo.kpiRight || `${tid} • VISUAL FLOW EXPLAINER`;

  // ============================================================================
  // SLIDE 1: VISUAL-FIRST 16:9 STORYBOARD MAP (CONNECTED ICON NODES + BAR GAUGES)
  // ============================================================================
  const s1 = pptx.addSlide();
  s1.background = { color: bgHex };

  // Top Full-Width Executive Header Card (x=0.36, y=0.24, w=12.61, h=1.34)
  s1.addShape(pptx.ShapeType.roundRect, {
    x: 0.36,
    y: 0.24,
    w: 12.61,
    h: 1.34,
    rectRadius: 0.04,
    fill: { color: 'FFFFFF' },
    line: { color: 'CBD5E1', width: 1 },
  });
  s1.addShape(pptx.ShapeType.roundRect, {
    x: 0.56,
    y: 0.36,
    w: 2.55,
    h: 0.26,
    rectRadius: 0.2,
    fill: { color: '0F172A' },
  });
  s1.addText(kpiRight, {
    x: 0.56,
    y: 0.36,
    w: 2.55,
    h: 0.26,
    fontSize: 8.5,
    bold: true,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });
  s1.addShape(pptx.ShapeType.roundRect, {
    x: 8.35,
    y: 0.36,
    w: 4.42,
    h: 0.26,
    rectRadius: 0.2,
    fill: { color: 'EFF6FF' },
    line: { color: '93C5FD', width: 0.75 },
  });
  s1.addText(kpiLeft, {
    x: 8.35,
    y: 0.36,
    w: 4.42,
    h: 0.26,
    fontSize: 8.2,
    bold: true,
    color: '1D4ED8',
    align: 'center',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });
  s1.addText(posterHeadline, {
    x: 0.56,
    y: 0.68,
    w: 12.20,
    h: 0.44,
    fontSize: 19.5,
    bold: true,
    color: '0F172A',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });
  s1.addText(posterSub, {
    x: 0.56,
    y: 1.14,
    w: 12.20,
    h: 0.34,
    fontSize: 11.0,
    color: '475569',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });

  if (sectionBands.length >= 2) {
    const nCols = sectionBands.length;
    const gapW = 0.24;
    const totalW = 12.61;
    const colW = Number(((totalW - gapW * (nCols - 1)) / nCols).toFixed(3));
    const colY = 1.74;
    const colH = 4.84;

    sectionBands.forEach((band, idx) => {
      const colX = Number((0.36 + idx * (colW + gapW)).toFixed(3));
      const hl = extractBandHighlights(band, vertices, idx);

      // Column Card Container
      s1.addShape(pptx.ShapeType.roundRect, {
        x: colX,
        y: colY,
        w: colW,
        h: colH,
        rectRadius: 0.04,
        fill: { color: 'FFFFFF' },
        line: { color: 'CBD5E1', width: 1.0 },
      });

      // Top Accent Header Bar inside Column
      const topBg = idx === 0 ? 'FEF2F2' : idx === 1 ? 'EFF6FF' : idx === 2 ? 'ECFDF5' : 'FAF5FF';
      const topBorder = idx === 0 ? 'FCA5A5' : idx === 1 ? '93C5FD' : idx === 2 ? '6EE7B7' : 'D8B4FE';
      s1.addShape(pptx.ShapeType.roundRect, {
        x: colX,
        y: colY,
        w: colW,
        h: 0.42,
        rectRadius: 0.04,
        fill: { color: topBg },
        line: { color: topBorder, width: 0.8 },
      });
      s1.addText(`STAGE 0${idx + 1}  •  SLIDE 0${idx + 2}`, {
        x: Number((colX + 0.14).toFixed(3)),
        y: colY,
        w: Number((colW * 0.58).toFixed(3)),
        h: 0.42,
        fontSize: 9.0,
        bold: true,
        color: hl.secColor,
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });
      const colBadgeText = hl.toggleState ? `GUARD ${hl.toggleState}` : idx === 2 ? 'GAUGE PROOF' : `STAGE 0${idx + 1}`;
      const colBadgeFill = hl.toggleState === 'OFF' ? 'DC2626' : hl.toggleState === 'ON' ? '059669' : hl.secColor;
      const pW = 1.18;
      s1.addShape(pptx.ShapeType.roundRect, {
        x: Number((colX + colW - pW - 0.12).toFixed(3)),
        y: Number((colY + 0.09).toFixed(3)),
        w: pW,
        h: 0.24,
        rectRadius: 0.2,
        fill: { color: colBadgeFill },
      });
      s1.addText(colBadgeText, {
        x: Number((colX + colW - pW - 0.12).toFixed(3)),
        y: Number((colY + 0.09).toFixed(3)),
        w: pW,
        h: 0.24,
        fontSize: 7.8,
        bold: true,
        color: 'FFFFFF',
        align: 'center',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });

      // Stage Title (1-line visual header, zero long paragraph subtitles!)
      s1.addText(hl.secTitle, {
        x: Number((colX + 0.16).toFixed(3)),
        y: Number((colY + 0.48).toFixed(3)),
        w: Number((colW - 0.32).toFixed(3)),
        h: 0.34,
        fontSize: 14.0,
        bold: true,
        color: '0F172A',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
      });

      // Connected Visual Flow Nodes inside Column (y = colY + 0.88 .. colY + 4.14)
      const subItems = hl.items.slice(0, 3);
      const availSubH = 3.22;
      const subGap = 0.22; // gap holds the vertical flow arrow!
      const subH = Number(((availSubH - subGap * Math.max(0, subItems.length - 1)) / Math.max(1, subItems.length)).toFixed(3));

      subItems.forEach((it, sIdx) => {
        const sy = Number((colY + 0.88 + sIdx * (subH + subGap)).toFixed(3));
        const sx = Number((colX + 0.14).toFixed(3));
        const sw = Number((colW - 0.28).toFixed(3));

        s1.addShape(pptx.ShapeType.roundRect, {
          x: sx,
          y: sy,
          w: sw,
          h: subH,
          rectRadius: 0.05,
          fill: { color: 'F8FAFC' },
          line: { color: 'CBD5E1', width: 0.85 },
        });

        if (it.isGaugeCard) {
          // Visual Before vs. After Horizontal Bar Chart Card!
          s1.addText(it.title, {
            x: Number((sx + 0.12).toFixed(3)),
            y: Number((sy + 0.06).toFixed(3)),
            w: Number((sw * 0.56).toFixed(3)),
            h: 0.22,
            fontSize: 10.2,
            bold: true,
            color: '0F172A',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
          const pw = Math.min(1.22, sw * 0.40);
          s1.addShape(pptx.ShapeType.roundRect, {
            x: Number((sx + sw - pw - 0.08).toFixed(3)),
            y: Number((sy + 0.06).toFixed(3)),
            w: Number(pw.toFixed(3)),
            h: 0.20,
            rectRadius: 0.2,
            fill: { color: 'DCFCE7' },
          });
          s1.addText(it.pillText, {
            x: Number((sx + sw - pw - 0.08).toFixed(3)),
            y: Number((sy + 0.06).toFixed(3)),
            w: Number(pw.toFixed(3)),
            h: 0.20,
            fontSize: 7.5,
            bold: true,
            color: '065F46',
            align: 'center',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });

          const barTrackX = Number((sx + 0.68).toFixed(3));
          const barTrackW = Number((sw - 1.62).toFixed(3));
          // Row 1: BEFORE Bar (Red)
          const r1Y = Number((sy + 0.36).toFixed(3));
          s1.addText('OFF', {
            x: Number((sx + 0.12).toFixed(3)),
            y: Number((r1Y - 0.03).toFixed(3)),
            w: 0.52,
            h: 0.18,
            fontSize: 7.5,
            bold: true,
            color: 'B91C1C',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
          s1.addShape(pptx.ShapeType.roundRect, {
            x: barTrackX,
            y: r1Y,
            w: barTrackW,
            h: 0.12,
            rectRadius: 0.2,
            fill: { color: 'FECACA' },
          });
          s1.addShape(pptx.ShapeType.roundRect, {
            x: barTrackX,
            y: r1Y,
            w: Number(Math.max(0.08, barTrackW * it.beforeRatio).toFixed(3)),
            h: 0.12,
            rectRadius: 0.2,
            fill: { color: 'DC2626' },
          });
          s1.addText(it.beforeVal, {
            x: Number((barTrackX + barTrackW + 0.04).toFixed(3)),
            y: Number((r1Y - 0.04).toFixed(3)),
            w: 0.82,
            h: 0.20,
            fontSize: 7.5,
            bold: true,
            color: 'B91C1C',
            align: 'right',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });

          // Row 2: AFTER Bar (Green)
          const r2Y = Number((sy + 0.60).toFixed(3));
          s1.addText('ON', {
            x: Number((sx + 0.12).toFixed(3)),
            y: Number((r2Y - 0.03).toFixed(3)),
            w: 0.52,
            h: 0.18,
            fontSize: 7.5,
            bold: true,
            color: '047857',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
          s1.addShape(pptx.ShapeType.roundRect, {
            x: barTrackX,
            y: r2Y,
            w: barTrackW,
            h: 0.12,
            rectRadius: 0.2,
            fill: { color: 'A7F3D0' },
          });
          s1.addShape(pptx.ShapeType.roundRect, {
            x: barTrackX,
            y: r2Y,
            w: Number(Math.max(0.08, barTrackW * it.afterRatio).toFixed(3)),
            h: 0.12,
            rectRadius: 0.2,
            fill: { color: '059669' },
          });
          s1.addText(it.afterVal, {
            x: Number((barTrackX + barTrackW + 0.04).toFixed(3)),
            y: Number((r2Y - 0.04).toFixed(3)),
            w: 0.82,
            h: 0.20,
            fontSize: 7.5,
            bold: true,
            color: '047857',
            align: 'right',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });
        } else {
          // Visual Icon Node Card (Left circular icon badge + bold title + right pill + compact formula tag)
          const iconD = 0.44;
          const iconX = Number((sx + 0.12).toFixed(3));
          const iconY = Number((sy + (subH - iconD) / 2).toFixed(3));
          s1.addShape(pptx.ShapeType.ellipse, {
            x: iconX,
            y: iconY,
            w: iconD,
            h: iconD,
            fill: { color: it.iconBg },
            line: { color: it.iconBorder, width: 1.2 },
          });
          s1.addText(it.iconSymbol, {
            x: iconX,
            y: iconY,
            w: iconD,
            h: iconD,
            fontSize: 9.2,
            bold: true,
            color: it.iconTextColor,
            align: 'center',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });

          const textLeftX = Number((sx + 0.66).toFixed(3));
          const textW = Number((sw - 0.76).toFixed(3));

          if (it.pillText) {
            const pw = Math.min(1.18, textW * 0.44);
            s1.addShape(pptx.ShapeType.roundRect, {
              x: Number((sx + sw - pw - 0.08).toFixed(3)),
              y: Number((sy + 0.08).toFixed(3)),
              w: Number(pw.toFixed(3)),
              h: 0.20,
              rectRadius: 0.2,
              fill: { color: it.pillBg },
            });
            s1.addText(it.pillText, {
              x: Number((sx + sw - pw - 0.08).toFixed(3)),
              y: Number((sy + 0.08).toFixed(3)),
              w: Number(pw.toFixed(3)),
              h: 0.20,
              fontSize: 7.4,
              bold: true,
              color: it.pillColor,
              align: 'center',
              valign: 'middle',
              fontFace: 'Arial',
              margin: 0,
            });
          }

          s1.addText(it.title, {
            x: textLeftX,
            y: Number((sy + 0.10).toFixed(3)),
            w: Number((textW * (it.pillText ? 0.56 : 0.96)).toFixed(3)),
            h: 0.28,
            fontSize: nCols >= 4 ? 9.5 : 11.0,
            bold: true,
            color: '0F172A',
            valign: 'middle',
            fontFace: 'Arial',
            margin: 0,
          });

          if (it.codeText) {
            s1.addShape(pptx.ShapeType.roundRect, {
              x: textLeftX,
              y: Number((sy + 0.46).toFixed(3)),
              w: Number((textW - 0.04).toFixed(3)),
              h: 0.26,
              rectRadius: 0.05,
              fill: { color: 'FFFFFF' },
              line: { color: 'CBD5E1', width: 0.6 },
            });
            s1.addText(it.codeText, {
              x: textLeftX,
              y: Number((sy + 0.46).toFixed(3)),
              w: Number((textW - 0.04).toFixed(3)),
              h: 0.26,
              fontSize: 8.2,
              bold: true,
              color: '334155',
              align: 'center',
              valign: 'middle',
              fontFace: 'Courier New',
              margin: 0,
            });
          }

          // Vertical flow connector arrow to next node inside column!
          if (sIdx < subItems.length - 1) {
            s1.addShape(pptx.ShapeType.line, {
              x: Number((colX + colW / 2).toFixed(3)),
              y: Number((sy + subH + 0.02).toFixed(3)),
              w: 0.001,
              h: Number((subGap - 0.04).toFixed(3)),
              line: { color: hl.secColor, width: 1.5, endArrowType: 'triangle' },
            });
          }
        }
      });

      // Bottom Compact Visual Rule Pill inside Column
      const rawFootText = hl.promptBar ? `${hl.promptBar.tag}: ${hl.promptBar.body}` : `Slide 0${idx + 2} → Full 16:9 Diagram`;
      const footText = nCols >= 4 && rawFootText.length > 96 ? `${rawFootText.slice(0, 93).trim()}...` : rawFootText;
      s1.addShape(pptx.ShapeType.roundRect, {
        x: Number((colX + 0.14).toFixed(3)),
        y: Number((colY + colH - 0.56).toFixed(3)),
        w: Number((colW - 0.28).toFixed(3)),
        h: 0.44,
        rectRadius: 0.04,
        fill: { color: 'F1F5F9' },
        line: { color: 'CBD5E1', width: 0.6 },
      });
      s1.addText(footText, {
        x: Number((colX + 0.22).toFixed(3)),
        y: Number((colY + colH - 0.56).toFixed(3)),
        w: Number((colW - 0.44).toFixed(3)),
        h: 0.44,
        fontSize: nCols >= 4 ? 7.4 : 8.2,
        bold: true,
        color: '0F172A',
        valign: 'middle',
        fontFace: 'Arial',
        margin: 0,
        wrap: true,
      });

      // Horizontal flow arrow to next column
      if (idx < nCols - 1) {
        s1.addShape(pptx.ShapeType.line, {
          x: Number((colX + colW + 0.03).toFixed(3)),
          y: Number((colY + colH / 2).toFixed(3)),
          w: Number((gapW - 0.06).toFixed(3)),
          h: 0.001,
          line: { color: '64748B', width: 1.5, endArrowType: 'triangle' },
        });
      }
    });
  } else {
    renderCellsToSlide(
      pptx,
      s1,
      vertices,
      edges,
      byId,
      { x: 20, y: 84, w: pageW - 40, h: pageH - 104 },
      { x: 0.36, y: 1.72, w: 12.61, h: 4.86 },
      1.05,
      1.25
    );
  }

  // Bottom Executive Footer Bar on Slide 1 (x=0.36, y=6.70, w=12.61, h=0.52)
  s1.addShape(pptx.ShapeType.roundRect, {
    x: 0.36,
    y: 6.70,
    w: 12.61,
    h: 0.52,
    rectRadius: 0.04,
    fill: { color: '0F172A' },
  });
  s1.addText(`SLIDE 01 OF 0${1 + sectionBands.length}  •  EXECUTIVE ARCHITECTURE OVERVIEW`, {
    x: 0.56,
    y: 6.70,
    w: 4.60,
    h: 0.52,
    fontSize: 9.0,
    bold: true,
    color: '38BDF8',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });
  s1.addText(`Slides 02–0${1 + sectionBands.length} render each architecture section as a full-bleed 16:9 widescreen editable diagram.`, {
    x: 5.20,
    y: 6.70,
    w: 7.55,
    h: 0.52,
    fontSize: 9.2,
    bold: true,
    color: 'F8FAFC',
    align: 'right',
    valign: 'middle',
    fontFace: 'Arial',
    margin: 0,
  });

  // ============================================================================
  // SLIDES 2..N: FULL-SCREEN 16:9 WIDESCREEN EDITABLE SECTION DEEP-DIVE SLIDES
  // ============================================================================
  sectionBands.forEach((band, idx) => {
    const s = pptx.addSlide();
    s.background = { color: bgHex };

    // Top Widescreen Slide Header Bar (x=0.36, y=0.24, w=12.61, h=0.58)
    s.addShape(pptx.ShapeType.roundRect, {
      x: 0.36,
      y: 0.24,
      w: 12.61,
      h: 0.58,
      rectRadius: 0.04,
      fill: { color: 'FFFFFF' },
      line: { color: 'CBD5E1', width: 0.85 },
    });
    s.addShape(pptx.ShapeType.roundRect, {
      x: 0.52,
      y: 0.35,
      w: 2.02,
      h: 0.36,
      rectRadius: 0.2,
      fill: { color: 'EFF6FF' },
      line: { color: '93C5FD', width: 0.75 },
    });
    s.addText(`${tid} • SECTION 0${idx + 1} OF 0${sectionBands.length}`, {
      x: 0.52,
      y: 0.35,
      w: 2.02,
      h: 0.36,
      fontSize: 8.8,
      bold: true,
      color: '1D4ED8',
      align: 'center',
      valign: 'middle',
      fontFace: 'Arial',
      margin: 0,
    });
    s.addText(posterHeadline, {
      x: 2.68,
      y: 0.24,
      w: 7.50,
      h: 0.58,
      fontSize: 13.8,
      bold: true,
      color: '0F172A',
      valign: 'middle',
      fontFace: 'Arial',
      margin: 0,
    });
    s.addShape(pptx.ShapeType.roundRect, {
      x: 10.32,
      y: 0.35,
      w: 2.48,
      h: 0.36,
      rectRadius: 0.2,
      fill: { color: 'ECFDF5' },
      line: { color: '6EE7B7', width: 0.75 },
    });
    s.addText('100% Native Editable Shapes', {
      x: 10.32,
      y: 0.35,
      w: 2.48,
      h: 0.36,
      fontSize: 8.8,
      bold: true,
      color: '065F46',
      align: 'center',
      valign: 'middle',
      fontFace: 'Arial',
      margin: 0,
    });

    const isCompactSingleRowBand = band.h <= 275;
    const diagramBox = { x: 0.36, y: 0.94, w: 12.61, h: 6.26 };

    // Render this section band (including its left spine badge) at full 16:9 widescreen width & height
    renderCellsToSlide(
      pptx,
      s,
      vertices,
      edges,
      byId,
      { x: 20, y: band.y - 6, w: pageW - 32, h: band.h + 12 },
      diagramBox,
      isCompactSingleRowBand ? 1.18 : 1.12,
      isCompactSingleRowBand ? 2.15 : 1.38
    );
  });

  const b64 = await pptx.write({ outputType: 'base64' });
  const pptxBuf = await postProcessArrowheads(b64);

  const outPptxPath = path.join(GALLERY_DIR, `${tid}.pptx`);
  fs.writeFileSync(outPptxPath, pptxBuf);
  return { pptxPath: outPptxPath, pptxBuf, slideCount: 1 + sectionBands.length };
}

async function getDriveAccessToken() {
  for (const tp of TOKEN_PATHS) {
    if (!fs.existsSync(tp)) continue;
    const raw = JSON.parse(fs.readFileSync(tp, 'utf8'));
    if (!raw.client_id || !raw.client_secret || !raw.refresh_token) continue;
    const body = new URLSearchParams({
      client_id: raw.client_id,
      client_secret: raw.client_secret,
      refresh_token: raw.refresh_token,
      grant_type: 'refresh_token',
    });
    const res = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.access_token) return data.access_token;
    }
  }
  throw new Error('Could not obtain Google Drive OAuth access_token via refresh_token');
}

async function uploadToGoogleSlides(pptxBuf, tid, title, existingId, token) {
  const boundary = '----TemplateSlidesBridge' + crypto.randomUUID().replace(/-/g, '');
  const metaJson = JSON.stringify({
    name: `${tid} — ${title} (Editable Google Slides)`,
    mimeType: 'application/vnd.google-apps.presentation',
  });
  const multipartBody = Buffer.concat([
    Buffer.from(
      `--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${metaJson}\r\n--${boundary}\r\nContent-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation\r\n\r\n`,
      'utf8'
    ),
    pptxBuf,
    Buffer.from(`\r\n--${boundary}--\r\n`, 'utf8'),
  ]);

  if (existingId) {
    const patchRes = await fetch(
      `https://www.googleapis.com/upload/drive/v3/files/${existingId}?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink`,
      {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
          'x-goog-user-project': QUOTA_PROJECT,
          'Content-Type': `multipart/related; boundary=${boundary}`,
        },
        body: multipartBody,
      }
    );
    if (patchRes.ok) {
      return patchRes.json();
    }
  }

  const createRes = await fetch(
    'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink',
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'x-goog-user-project': QUOTA_PROJECT,
        'Content-Type': `multipart/related; boundary=${boundary}`,
      },
      body: multipartBody,
    }
  );
  if (!createRes.ok) {
    throw new Error(`Google Drive upload failed (${createRes.status}): ${await createRes.text()}`);
  }
  return createRes.json();
}

async function exportLiveSlideThumbnails(slideId, tid, outDir, token) {
  fs.mkdirSync(outDir, { recursive: true });
  const presRes = await fetch(`https://slides.googleapis.com/v1/presentations/${slideId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      'x-goog-user-project': QUOTA_PROJECT,
    },
  });
  if (!presRes.ok) {
    throw new Error(`Failed to fetch presentation ${slideId}: ${presRes.status}`);
  }
  const pres = await presRes.json();
  const slides = pres.slides || [];
  for (let i = 0; i < slides.length; i++) {
    const pageId = slides[i].objectId;
    const tRes = await fetch(
      `https://slides.googleapis.com/v1/presentations/${slideId}/pages/${pageId}/thumbnail?thumbnailProperties.thumbnailSize=LARGE&thumbnailProperties.mimeType=PNG`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'x-goog-user-project': QUOTA_PROJECT,
        },
      }
    );
    if (tRes.ok) {
      const tJson = await tRes.json();
      const imgRes = await fetch(tJson.contentUrl);
      const buf = Buffer.from(await imgRes.arrayBuffer());
      const outPath = path.join(outDir, `gslides_${tid}_slide_${i + 1}.png`);
      fs.writeFileSync(outPath, buf);
      console.log(`[thumbnail_export] ${tid} Slide ${i + 1}/${slides.length} -> ${outPath} (${buf.length}B)`);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  const thumbIdx = args.indexOf('--export-thumbnails');
  const exportThumbDir = thumbIdx !== -1 && args[thumbIdx + 1] ? args[thumbIdx + 1] : null;
  const filterTids = args.filter((a) => /^T\d+$/.test(a));
  const allTids = ['T01', ...Array.from({ length: 32 }, (_, i) => `T${i + 53}`)];
  const targetTids = filterTids.length > 0 ? filterTids : allTids;

  fs.mkdirSync(path.dirname(MANIFEST_PATH), { recursive: true });
  let manifest = { updatedAt: new Date().toISOString(), accountEmail: 'nitinagga@google.com', slides: {} };
  if (fs.existsSync(MANIFEST_PATH)) {
    try {
      manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
    } catch {}
  }

  const galleryManifestPath = path.join(GALLERY_DIR, 'gallery_manifest.json');
  let galleryManifest = { templates: [] };
  if (fs.existsSync(galleryManifestPath)) {
    galleryManifest = JSON.parse(fs.readFileSync(galleryManifestPath, 'utf8'));
  }
  const titleByTid = Object.fromEntries((galleryManifest.templates || []).map((t) => [t.id, t.name]));

  const token = await getDriveAccessToken();

  for (const tid of targetTids) {
    const title = titleByTid[tid] || `${tid} Editable Architecture Blueprint`;
    const { pptxPath, pptxBuf, slideCount } = await compileDrawioTemplateToEditablePptx(tid, title);
    const sha256 = crypto.createHash('sha256').update(pptxBuf).digest('hex');
    const existing = manifest.slides?.[tid];

    let slideId = existing?.googleSlidesId;
    if (!slideId || existing?.sha256 !== sha256 || args.includes('--force')) {
      const uploaded = await uploadToGoogleSlides(pptxBuf, tid, title, slideId, token);
      slideId = uploaded.id;
    }

    if (exportThumbDir && slideId) {
      await exportLiveSlideThumbnails(slideId, tid, exportThumbDir, token);
    }

    const entry = {
      tid,
      title,
      pptxFile: `${tid}.pptx`,
      slideCount,
      sizeBytes: pptxBuf.length,
      sha256,
      googleSlidesId: slideId,
      googleSlidesEditUrl: `https://docs.google.com/presentation/d/${slideId}/edit?authuser=nitinagga%40google.com`,
      googleSlidesPreviewUrl: `https://docs.google.com/presentation/d/${slideId}/preview`,
      googleSlidesEmbedUrl: `https://docs.google.com/presentation/d/${slideId}/embed?start=false&loop=false&delayms=5000`,
      googleSlidesPdfUrl: `https://docs.google.com/presentation/d/${slideId}/export/pdf`,
      syncedAt: new Date().toISOString(),
    };
    manifest.slides[tid] = entry;
    console.log(`[slides_sync] ${tid} (${slideCount} editable slides, ${pptxBuf.length}B) -> ${entry.googleSlidesEditUrl}`);
  }

  manifest.updatedAt = new Date().toISOString();
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf8');

  // Enrich gallery_manifest.json with .drawio, .pptx, and google_slides_url
  if (fs.existsSync(galleryManifestPath)) {
    for (const t of galleryManifest.templates || []) {
      const m = manifest.slides[t.id];
      if (m) {
        t.files = t.files || {};
        t.files.drawio = `${t.id}.drawio`;
        t.files.pptx = `${t.id}.pptx`;
        t.google_slides_id = m.googleSlidesId;
        t.google_slides_url = m.googleSlidesEditUrl;
        t.google_slides_preview_url = m.googleSlidesPreviewUrl;
        t.editable_slide_count = m.slideCount;
      }
    }
    fs.writeFileSync(galleryManifestPath, JSON.stringify(galleryManifest, null, 2), 'utf8');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
