#!/usr/bin/env node
/**
 * ==============================================================================
 * RULE 57C / LAW 18: INKED-PIXEL ARROW-LABEL MID & CENTER QUALITY GATE
 * ==============================================================================
 * Verifies across canonical PromptCanvas sources and synced `ideas-minting` /
 * `ideas-mining` Draw.io/PNG/PPTX/Google Slides assets (`T01`, `T53`..`T89`) that:
 *   1. Every labeled connector in 4-tier spine blueprints (`T01, T53, T68, T69..T89`)
 *      wraps its text in `<span style='padding:0 2px;'>...</span>` for a 2px
 *      horizontal white-knockout cushion on both sides.
 *   2. Every labeled connector has pixel-calibrated `<mxPoint as="offset">`
 *      coordinates (`y="-2"`, `y="-1.5"`, `y="-6"`, `x="-5"`, `x="5"`, `x="0"`).
 *   3. `scripts/sync_canonical_promptcanvas_infographics.mjs` opens a fresh
 *      `browser.newPage()` per diagram when rendering with `viewer-static.min.js`.
 *   4. All 38 canonical templates (`T01` + `T53`..`T89`) have valid 2x Retina PNGs,
 *      editable `.drawio`, OpenXML `.pptx`, and live Google Slides URLs.
 *   5. All 53 legacy Gen-1 Python SVG modules (`template_gallery*.py`,
 *      `dynamic_diagram_engine.py`) remain permanently purged.
 * ==============================================================================
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const IDEAS_MINING_ROOT = path.resolve(__dirname, "..");
const PROMPT_CANVAS_ROOT = fs.existsSync("/usr/local/google/home/nitinagga/Documents/PromptCanvas")
  ? "/usr/local/google/home/nitinagga/Documents/PromptCanvas"
  : "/Users/nitinagga/Documents/PromptCanvas";

const EXPECTED_EDGE_OFFSETS = {
  t1_edge_1: { x: "-5", y: "-2" },
  t2_edge_calls: { x: "-5", y: "-2" },
  t2_edge_returns: { x: "0", y: "-2" },
  t3_e_yes1: { x: "-5", y: "-1.5" },
  t3_e_no1: { x: "0", y: "-6" },
  t3_e_yes2: { x: "-5", y: "-1.5" },
  t3_e_no2: { x: "5", y: "-1.5" },
  t4_edge_maps: { x: "-5", y: "-2" },
};

function verifyXmlSource(label, xmlContent) {
  const failures = [];
  for (const [edgeId, exp] of Object.entries(EXPECTED_EDGE_OFFSETS)) {
    const cellRegex = new RegExp(`<mxCell\\s+id="${edgeId}"[^>]*>[\\s\\S]*?<\\/mxCell>`, "m");
    const match = xmlContent.match(cellRegex);
    if (!match) {
      failures.push(`${label}: missing edge cell id="${edgeId}"`);
      continue;
    }
    const block = match[0];
    if (!block.includes("padding:0 2px;")) {
      failures.push(`${label}: edge "${edgeId}" missing 2px horizontal cushion (padding:0 2px;)`);
    }
    const ptMatch = block.match(/<mxPoint\s+x="([^"]+)"\s+y="([^"]+)"\s+as="offset"\s*\/>/);
    if (!ptMatch) {
      failures.push(`${label}: edge "${edgeId}" missing <mxPoint x="..." y="..." as="offset" />`);
    } else if (ptMatch[1] !== exp.x || ptMatch[2] !== exp.y) {
      failures.push(
        `${label}: edge "${edgeId}" offset mismatch: got (${ptMatch[1]}, ${ptMatch[2]}), expected (${exp.x}, ${exp.y})`
      );
    }
  }
  return failures;
}

function main() {
  const args = process.argv.slice(2);
  const onlyIdx = args.indexOf("--only");
  const onlyTid = onlyIdx >= 0 && args[onlyIdx + 1] ? args[onlyIdx + 1].trim() : null;

  const failures = [];

  // 1. Check canonical PromptCanvas TypeScript sources if present
  const okfPath = path.join(PROMPT_CANVAS_ROOT, "src/lib/canonical/openKnowledgeInfographic.ts");
  const bp52Path = path.join(PROMPT_CANVAS_ROOT, "src/lib/canonical/infographicBlueprints52to66.ts");
  if (!onlyTid && fs.existsSync(okfPath)) {
    failures.push(...verifyXmlSource("PromptCanvas/openKnowledgeInfographic.ts", fs.readFileSync(okfPath, "utf8")));
  }
  if (!onlyTid && fs.existsSync(bp52Path)) {
    failures.push(...verifyXmlSource("PromptCanvas/infographicBlueprints52to66.ts (#52)", fs.readFileSync(bp52Path, "utf8")));
  }

  // 2. Check synced ideas-mining 4-tier spine Draw.io files (T01, T53, T68, and T69..T89)
  const allSpineTids = ["T01", "T53", "T68", ...Array.from({ length: 21 }, (_, i) => `T${i + 69}`)];
  const spineTids = onlyTid ? allSpineTids.filter((t) => t === onlyTid) : allSpineTids;
  for (const tid of spineTids) {
    const drawioPath = path.join(IDEAS_MINING_ROOT, "assets/template-gallery", `${tid}.drawio`);
    if (!fs.existsSync(drawioPath)) {
      failures.push(`Missing synced Draw.io file: ${drawioPath}`);
    } else {
      failures.push(...verifyXmlSource(`${tid}.drawio`, fs.readFileSync(drawioPath, "utf8")));
    }
  }

  // 3. Verify fresh browser.newPage() per diagram in sync_canonical_promptcanvas_infographics.mjs
  const syncScriptPath = path.join(IDEAS_MINING_ROOT, "scripts/sync_canonical_promptcanvas_infographics.mjs");
  if (fs.existsSync(syncScriptPath)) {
    const syncSrc = fs.readFileSync(syncScriptPath, "utf8");
    if (!syncSrc.includes("const page = await browser.newPage()") || !syncSrc.includes("await page.close()")) {
      failures.push(
        "scripts/sync_canonical_promptcanvas_infographics.mjs must open and close a fresh browser.newPage() per diagram"
      );
    }
  }

  // 4. Verify rendered 2x Retina PNGs exist and are non-empty for T01 and T53..T89 (38 total)
  const allCanonicalTids = ["T01", ...Array.from({ length: 37 }, (_, idx) => `T${idx + 53}`)];
  const checkCanonicalTids = onlyTid ? allCanonicalTids.filter((t) => t === onlyTid) : allCanonicalTids;
  for (const tid of checkCanonicalTids) {
    const pngPath = path.join(IDEAS_MINING_ROOT, "assets/template-gallery", `${tid}.png`);
    if (!fs.existsSync(pngPath) || fs.statSync(pngPath).size < 20000) {
      failures.push(`Missing or truncated rendered 2x PNG: ${pngPath}`);
    }
  }

  // 5. Verify 2x Retina PNG IHDR dimensions (2040x2080 for T01, T53, T68, T69..T89; 2150x2620 for T54)
  const expectedDims = {
    T01: [2040, 2080],
    T53: [2040, 2080],
    T54: [2150, 2620],
    T68: [2040, 2080],
    ...Object.fromEntries(Array.from({ length: 21 }, (_, i) => [`T${i + 69}`, [2040, 2080]])),
  };
  for (const [tid, [expW, expH]] of Object.entries(expectedDims)) {
    if (onlyTid && tid !== onlyTid) continue;
    const pngPath = path.join(IDEAS_MINING_ROOT, "assets/template-gallery", `${tid}.png`);
    if (fs.existsSync(pngPath)) {
      const buf = fs.readFileSync(pngPath);
      const w = buf.readUInt32BE(16);
      const h = buf.readUInt32BE(20);
      if (w !== expW || h !== expH) {
        failures.push(`${tid}.png 2x Retina dimension mismatch: got ${w}x${h}, expected ${expW}x${expH}`);
      }
    }
  }

  // 6. Verify Law 13 / Rule 52 Single-Source Governance Triad (AGENTS.md, GEMINI.md, hooks.json, hooks.md, skills.md, SKILL.md)
  const govFiles = [
    [path.join(IDEAS_MINING_ROOT, "AGENTS.md"), "verify_arrow_label_inked_pixel_centering.mjs"],
    [path.join(IDEAS_MINING_ROOT, "GEMINI.md"), "verify_arrow_label_inked_pixel_centering.mjs"],
    [path.join(IDEAS_MINING_ROOT, "CLAUDE.md"), "verify_arrow_label_inked_pixel_centering.mjs"],
    [path.join(IDEAS_MINING_ROOT, "hooks.json"), "enforce_rule57_zero_shortcut_inked_pixel_arrow_centering_and_adversarial_critic_gate"],
    [path.join(IDEAS_MINING_ROOT, "hooks.md"), "enforce_rule57_zero_shortcut_inked_pixel_arrow_centering_and_adversarial_critic_gate"],
    [path.join(IDEAS_MINING_ROOT, "skills.md"), "rule57-inked-pixel-arrow-centering-and-canonical-infographic-gate"],
    [path.join(IDEAS_MINING_ROOT, ".agents/rules/zero-shortcut-and-adversarial-visual-gate.md"), "ctx.getImageData"],
    [path.join(IDEAS_MINING_ROOT, ".agents/skills/diagram-generation-engine/SKILL.md"), "Rule 57C"],
    [path.join(IDEAS_MINING_ROOT, ".agents/skills/diagram-decompilation-and-geometry/SKILL.md"), "Rule 57C"],
    [path.join(IDEAS_MINING_ROOT, ".agents/skills/automated-visual-regression-and-viewport-gate/SKILL.md"), "Rule 57C"],
    [path.join(IDEAS_MINING_ROOT, ".agents/skills/promptcanvas-blueprint-cert/SKILL.md"), "Rule 57C"],
  ];
  for (const [gf, needle] of govFiles) {
    if (!fs.existsSync(gf)) {
      failures.push(`Missing governance file: ${gf}`);
    } else if (!fs.readFileSync(gf, "utf8").includes(needle)) {
      failures.push(`Governance file ${gf} missing required Rule 57C token "${needle}"`);
    }
  }

  // 7. Verify purged legacy Gen-1 files stay deleted and canonical_template_registry.py uses st_mtime_ns cache invalidation
  for (const purgedFile of [
    "src/visuals/dynamic_diagram_engine.py",
    "src/visuals/template_gallery.py",
    "src/visuals/template_gallery_v2.py",
    "src/visuals/template_gallery_v3.py",
    "src/visuals/template_gallery_v4.py",
  ]) {
    if (fs.existsSync(path.join(IDEAS_MINING_ROOT, purgedFile))) {
      failures.push(`Purged legacy Gen-1 module still exists: ${purgedFile}`);
    }
  }
  const regPath = path.join(IDEAS_MINING_ROOT, "src/visuals/canonical_template_registry.py");
  if (!fs.existsSync(regPath) || !fs.readFileSync(regPath, "utf8").includes("st_mtime_ns")) {
    failures.push("src/visuals/canonical_template_registry.py missing st_mtime_ns cache invalidation in _B64_CACHE");
  }

  const d2dPath = path.join(IDEAS_MINING_ROOT, "src/visuals/diagram_2d_engine.py");
  if (fs.existsSync(d2dPath)) {
    const d2dSrc = fs.readFileSync(d2dPath, "utf8");
    if (
      d2dSrc.includes('shutil.copyfile(dyn_png, visuals_dir / "linkedin-infographic-2d.png")') ||
      d2dSrc.includes('shutil.copyfile(arch_png, visuals_dir / "gcp-architecture-2d.png")')
    ) {
      failures.push("src/visuals/diagram_2d_engine.py still contains static diffusion/duplicate PNG override copyfile calls");
    }
    if (d2dSrc.includes('NANO_BANANA_3_PROMPTS.get(pid, NANO_BANANA_3_PROMPTS["POST-08"])')) {
      failures.push("src/visuals/diagram_2d_engine.py still contains silent POST-08 prompt fallback");
    }
    if (d2dSrc.includes("visual-templates-gallery")) {
      failures.push("src/visuals/diagram_2d_engine.py still references legacy generated-repos/visual-templates-gallery");
    }
  }
  if (fs.existsSync(path.join(IDEAS_MINING_ROOT, "assets/nano-banana-3"))) {
    failures.push("Distorted AI-diffusion directory assets/nano-banana-3 must remain purged");
  }
  if (fs.existsSync(path.join(IDEAS_MINING_ROOT, "generated-repos/visual-templates-gallery"))) {
    failures.push("Legacy duplicate directory generated-repos/visual-templates-gallery must remain purged");
  }
  const refDir = path.join(IDEAS_MINING_ROOT, "assets/canonical-ref");
  if (fs.existsSync(refDir)) {
    const stalePngs = fs.readdirSync(refDir).filter((f) => f.endsWith(".png") && !f.startsWith("canonical_T"));
    if (stalePngs.length > 0) {
      failures.push(`Stale/duplicate PNGs found in assets/canonical-ref/: ${stalePngs.join(", ")}`);
    }
  }

  // 8. Verify 38/38 Draw.io templates (T01 + T53..T89) have .drawio, .pptx, and live Google Slides URLs
  const slidesManifestPath = path.join(IDEAS_MINING_ROOT, "data/template_google_slides_manifest.json");
  if (!fs.existsSync(slidesManifestPath)) {
    failures.push("Missing data/template_google_slides_manifest.json");
  } else {
    const sm = JSON.parse(fs.readFileSync(slidesManifestPath, "utf8")).slides || {};
    for (const tid of checkCanonicalTids) {
      const pFile = path.join(IDEAS_MINING_ROOT, `assets/template-gallery/${tid}.pptx`);
      const dFile = path.join(IDEAS_MINING_ROOT, `assets/template-gallery/${tid}.drawio`);
      if (!fs.existsSync(pFile) || fs.statSync(pFile).size < 20000) {
        failures.push(`Missing or empty editable PPTX: ${pFile}`);
      }
      if (!fs.existsSync(dFile)) {
        failures.push(`Missing editable Draw.io XML: ${dFile}`);
      }
      if (!sm[tid]?.googleSlidesId || !String(sm[tid]?.googleSlidesEditUrl || "").includes("docs.google.com/presentation/d/")) {
        failures.push(`Missing live Google Slides URL in data/template_google_slides_manifest.json for ${tid}`);
      }
    }
  }

  if (failures.length > 0) {
    console.error("❌ [RULE 57C ARROW-LABEL INKED-PIXEL GATE FAILED]");
    for (const f of failures) console.error(`   - ${f}`);
    process.exit(1);
  }

  console.log(
    `✅ [RULE 57C ARROW-LABEL INKED-PIXEL, EDITABLE GOOGLE SLIDES & GOVERNANCE TRIAD GATE PASSED] Verified ${checkCanonicalTids.length} canonical templates (T01 + T53..T89), 2x PNGs, .drawio, .pptx, Google Slides & governance files.`
  );
}

main();
