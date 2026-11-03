---
name: visual-regression-testing
description: Automated pixel-by-pixel image comparison using pixelmatch and canvas to detect visual layout shifts, CSS regressions, and font rendering anomalies between baseline and current screenshots.
---

# Visual Regression Testing & Image Diffing Skill

This skill provides automated pixel-level image comparison workflows to ensure UI design integrity across code refactors and framework upgrades.

## 1. Directory Structure

Baseline images and diff results are stored in the project workspace:
- Baseline Screenshots: `scratch/screenshots_baseline/`
- Current Screenshots: `scratch/screenshots_current/`
- Diff Visual Artifacts: `scratch/screenshots_diff/`

## 2. Automated Image Diffing Script (`scratch/diff_screenshots.js`)

```javascript
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const PNG = require('pngjs').PNG;
const pixelmatch = require('pixelmatch');

async function launchSignedBrowser() {
  const macChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  return await puppeteer.launch({
    executablePath: fs.existsSync(macChromePath) ? macChromePath : undefined,
    headless: 'new',
    args: ['--headless=new', '--no-sandbox', '--disable-gpu', '--window-size=1600,1000']
  });
}

function compareScreenshots(baselinePath, currentPath, diffOutputPath) {
  if (!fs.existsSync(baselinePath) || !fs.existsSync(currentPath)) {
    console.error('❌ Missing baseline or current screenshot for comparison.');
    return { mismatchedPixels: -1, diffPercentage: 100 };
  }

  const img1 = PNG.sync.read(fs.readFileSync(baselinePath));
  const img2 = PNG.sync.read(fs.readFileSync(currentPath));

  const { width, height } = img1;
  const diff = new PNG({ width, height });

  const numDiffPixels = pixelmatch(img1.data, img2.data, diff.data, width, height, {
    threshold: 0.1,
    includeAA: false,
  });

  const totalPixels = width * height;
  const diffPercentage = ((numDiffPixels / totalPixels) * 100).toFixed(2);

  fs.mkdirSync(path.dirname(diffOutputPath), { recursive: true });
  fs.writeFileSync(diffOutputPath, PNG.sync.write(diff));

  console.log(`📊 Image Diff Results: ${numDiffPixels} mismatched pixels (${diffPercentage}% difference)`);
  console.log(`🖼️ Diff image saved to: file://${diffOutputPath}`);

  return { numDiffPixels, diffPercentage, diffOutputPath };
}

module.exports = { compareScreenshots };
```

## 3. Workflow Protocol

1. **Capture Baseline**: Run Puppeteer suite on `main` branch and save to `scratch/screenshots_baseline/`.
2. **Capture Current**: Run Puppeteer suite on feature branch and save to `scratch/screenshots_current/`.
3. **Compare & Report**: Execute `compareScreenshots()`. If `diffPercentage > 0.5%`, output a warning and present the diff file link `[01_diff.png](file:///path/to/scratch/screenshots_diff/01_diff.png)`.

## 4. Google Cloud Training & Coursera Focused-Crop Slide Composition Rules (`Pattern A`, `Pattern C`, Lossless Rectangular `cropPx`, Zero Seam-Carving & `Left-Center` Shape Alignment)

- **Pattern A (Single Shared Left-Nav Anchor `1×` + 3-Step Continuation Screenshots)**: When a slide demonstrates multiple navigation destinations from the same sidebar (e.g., Slide 4 `01_ge_portal_home.png`), render the Left Navigation Rail **once (`1×` Only)** on the left with numbered highlight callouts (`①`, `②`, `③`), and pair it on the right with 9 tightly cropped 3-step continuation screenshots across `Agent Skills Hub`, `Multi-Step Workflows`, and `Interactive Chat Agents`. Never repeat the left navigation bar twice on the same slide.
- **Pattern C (Lossless Rectangular UI Piece Crops + Zero Seam-Carving)**: On multi-action build slides (`Slide 6`, `Slide 7`, `Slide 10`, `Slide 12`, `Slide 16`), use pure, lossless rectangular cropping (`cropPx(b64, sx, sy, sw, sh, masks)`) with VDI top-bar/taskbar exclusion (`sy = 152, sh = 1290..1320`) and pill-interior background pixel sampling (`sampleX, sampleY` in `PROMO_PILL_MASK_HOME`, `PROMO_PILL_MASK_MENU`, `PROMO_PILL_MASK_SLASH`). **Never run column/row seam-carving (`seamCarveH` / `window.__stripWhitespacePreserveAspect`)** on UI screenshots, as it slices characters and distorts card borders.
- **Left-Center (`left center`) Shape & Screenshot Alignment**: Across all 18 slides, align content inside every card/shape at **Left-Center** (`justify-content: center; align-items: stretch/flex-start; text-align: left;`) and align every screenshot container at **Left-Center** (`display: flex; align-items: center; justify-content: flex-start;` with `object-fit: contain; object-position: left center;`).

## 5. Real-Screenshot Provenance Rule (Rule 66 — No Mock-Ups for Requested Live Screens)

- If the user requests screenshots of Gemini Enterprise or Google Cloud Console, capture the **real, signed-in** pages via an isolated Chrome profile + `puppeteer-core.connect({ browserURL })` (see `scripts/screenshots/capture_real_merck_adk_ge_and_console.mjs`). Never render HTML look-alikes or device composites and never call them "authentic".
- Record each capture in `raw_sources/real/real_capture_manifest.json` (`finalUrl`, `title`, `viewport@dpr`, `capturedAtUtc`, `source: LIVE_BROWSER_CAPTURE`) and reference it only as `rawFile: 'real/<name>.png'`; `cropPx` is in CSS px and is scaled by the capture DPR.
- GE DOM lives in shadow roots (`document.body.innerText` is empty) and the chat scrolls in an inner container, so `fullPage` does not expand — use tall viewports (`1600×2600`, `390×2240@3x`, `412×2150@2.625x`). Console "Learn/Tutorial" panels occupy the right ~300 CSS px; crop to `w: 1290` when they cannot be closed.
- If a screen does not exist (no VPC-SC perimeter, no WIF pool, no GCS bucket), surface it as an explicit **gap** on the slide instead of fabricating it. Keep the only non-capture asset (architecture diagram) explicitly labelled "Diagram".
- Gate: `scripts/tdd/run_level10_deep_forensic_audit.mjs` F-14 fails the build on any non-`real/` step source, any mock-up renderer, or any synthetic raw source left on disk.

### 5.1 Step-Card Keyboard Navigation (Rule 66 Addendum)
When verifying multi-step slide decks, assert that `ArrowRight` advances `window.__currentMerckSlideStep` 1→N before `currentIdx` changes, and that `ArrowLeft` from step 1 lands on the previous slide's last step (see `stepForwardOrNextSlide` / `stepBackOrPrevSlide` in `slides-fullscreen.html`).


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
