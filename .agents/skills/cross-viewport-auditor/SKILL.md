---
name: cross-viewport-auditor
description: Multi-device and cross-browser viewport scaling tests across Mobile (390x844), Tablet (834x1194), and Ultra-Wide Desktop (1600x950) to ensure responsive layout balance.
---

# Cross-Viewport Responsive UI Auditor Skill

This skill provides multi-device viewport testing using Puppeteer to verify responsive breakpoints, navigation drawer collapse, search input wrapping, and canvas grid scaling across Mobile, Tablet, and Desktop screen sizes.

## 1. Standard Responsive Breakpoint Matrices

- **Mobile Viewport (iPhone 14/15 Pro)**: Width: 390px | Height: 844px
- **Tablet Viewport (iPad Pro 11")**: Width: 834px | Height: 1194px
- **Standard Desktop**: Width: 1280px | Height: 800px
- **Ultra-Wide Desktop**: Width: 1600px | Height: 950px

## 2. Multi-Viewport Automated Runner (`scratch/audit_responsive_viewports.js`)

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const viewports = [
  { name: 'mobile_iphone', width: 390, height: 844 },
  { name: 'tablet_ipad', width: 834, height: 1194 },
  { name: 'desktop_wide', width: 1600, height: 950 },
];

async function auditResponsiveViewports(targetUrl, outputDir = 'scratch/screenshots_responsive') {
  console.log(`📱 Running Cross-Viewport Responsive UI Audit on: ${targetUrl}`);
  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  for (const vp of viewports) {
    const page = await browser.newPage();
    await page.setViewport({ width: vp.width, height: vp.height });
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 2000));

    const screenshotPath = path.join(outputDir, `${vp.name}.png`);
    await page.screenshot({ path: screenshotPath });
    console.log(`📸 Captured ${vp.name} (${vp.width}x${vp.height}): file://${screenshotPath}`);
    await page.close();
  }

  await browser.close();
  console.log('✅ Multi-Viewport Responsive Audit Complete!');
}

module.exports = { auditResponsiveViewports };
```

## 3. Workflow Protocol
Run `auditResponsiveViewports(url)` when creating new UI components or modifying responsive Tailwind breakpoints (`md:`, `lg:`). In `demoes-ge` Fullscreen Theater Mode (`?present=1` / `body.google-slides-theater`), verify that `.visual-frame` and `#slide-img` fill `100vw × 100vh` with zero horizontal compression (`padding: 0`) and that `.karaoke-captions-bar` remains hidden by default (`captionsCollapsed = true`) unless explicitly toggled via `.theater-captions-explicit`.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
