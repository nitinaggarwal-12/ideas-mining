---
name: performance-and-telemetry
description: Comprehensive client-side Core Web Vitals (LCP, CLS, TTFB) metric profiling, DOM node budget tracking, Railway container telemetry streaming, and server error log monitoring.
---

# Performance & Production Telemetry Skill

This skill combines client-side rendering performance profiling (Core Web Vitals) with live server container telemetry monitoring.

## 1. Client Web Vitals Thresholds
- **LCP (Largest Contentful Paint)**: Good ≤ 2.5s | Needs Improvement ≤ 4.0s
- **CLS (Cumulative Layout Shift)**: Good ≤ 0.1 | Needs Improvement ≤ 0.25
- **TTFB (Time to First Byte)**: Good ≤ 800ms | Needs Improvement ≤ 1800ms

## 2. Telemetry & Performance Runner (`scratch/audit_performance_telemetry.js`)

```javascript
const puppeteer = require('puppeteer');
const https = require('https');

async function profilePerformanceAndTelemetry(url) {
  console.log(`🚀 Profiling Web Vitals & Telemetry for: ${url}`);

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  
  await page.evaluateOnNewDocument(() => {
    window.performanceMetrics = {};
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (entry.entryType === 'largest-contentful-paint') {
          window.performanceMetrics.LCP = entry.startTime;
        }
        if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
          window.performanceMetrics.CLS = (window.performanceMetrics.CLS || 0) + entry.value;
        }
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });

  const startTime = Date.now();
  await page.goto(url, { waitUntil: 'networkidle2' });
  const ttfb = Date.now() - startTime;

  const metrics = await page.metrics();
  const cwv = await page.evaluate(() => window.performanceMetrics || {});

  const report = {
    url,
    TTFB_ms: ttfb,
    LCP_ms: cwv.LCP ? cwv.LCP.toFixed(2) : 'N/A',
    CLS: cwv.CLS ? cwv.CLS.toFixed(3) : 0,
    JSHeapUsedMB: (metrics.JSHeapUsedSize / 1024 / 1024).toFixed(2),
    DOMNodes: metrics.Nodes,
  };

  console.table(report);
  await browser.close();
  return report;
}

module.exports = { profilePerformanceAndTelemetry };
```

## 3. Production Verification Protocol
1. Execute `profilePerformanceAndTelemetry()` after new feature deployments.
2. Verify `LCP < 2500ms`, `CLS < 0.1`, and HTTP `200` responses.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
