---
name: puppeteer-pair-programming
description: Comprehensive architecture, cheatsheet, and patterns for building robust end-to-end (E2E) Puppeteer automation suites that run asynchronously in the background during pair programming with interactive setup modes, clean profile management, and framework-safe DOM interactions.
---

# Puppeteer Pair Programming & E2E Testing Suite

This skill provides the architectural foundation and reusable patterns for writing Puppeteer test suites designed specifically for **pair programming** where an agent runs background tasks while the user observes or collaborates.

## 1. macOS Signed Chrome & Santa Endpoint Security Bypass

On corporate macOS environments protected by Santa Endpoint Security, default Puppeteer launches fail because downloaded `Google Chrome for Testing` / Chromium binaries (`~/.cache/puppeteer/...`) are unnotarized and receive `SIGKILL` (`Code: null`).

**Universal Invariant for macOS**: 
- ALWAYS explicitly set `executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'`. Because the system-installed Google Chrome is officially signed and notarized, Santa permits headless execution without restrictions.
- NEVER fallback to unnotarized Chromium binaries on macOS.
- ALWAYS use dynamic per-run isolated temporary user profile directories (`path.join(__dirname, '.chrome_profile_' + Date.now())` or `/tmp/chrome_headless_*`) to prevent `SingletonLock` process crashes when running back-to-back tests.
- NEVER copy, read, or touch `~/Library/Application Support/Google/Chrome/*/Cookies` via `cp`, `sqlite3`, or any CLI/file tool on macOS, as Santa `ChromeProfileCookiesLoud` blocks access and displays a desktop alert.

```javascript
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function launchPairProgrammingBrowser(options = {}) {
  // 1. Mandatory Google-Signed Chrome check on macOS
  const macChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  let executablePath = options.executablePath;

  if (process.platform === 'darwin') {
    if (fs.existsSync(macChromePath)) {
      executablePath = macChromePath;
    } else {
      throw new Error(
        `[Santa Security Guard] Google-signed Chrome not found at ${macChromePath}. ` +
        `Do not launch Google Chrome for Testing as Santa will block execution.`
      );
    }
  }

  // 2. Dynamic isolated profile to eliminate SingletonLock collisions
  const tempProfileDir = path.join(__dirname, '.chrome_profile_' + Date.now());
  fs.mkdirSync(tempProfileDir, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath,
    headless: 'new', // Headless mode for background execution without GUI popups
    defaultViewport: { width: 1600, height: 1000 },
    userDataDir: tempProfileDir,
    args: [
      '--headless=new',
      '--window-size=1600,1000',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--no-default-browser-check',
      '--no-first-run',
      '--disable-blink-features=AutomationControlled'
    ],
    ...options
  });

  return { browser, tempProfileDir };
}
```

> **Navigation Tip for Next.js**: When testing against live Next.js development servers (`localhost:3000` / `localhost:3001`), use `waitUntil: 'domcontentloaded'` instead of `networkidle2` to prevent active Hot-Module-Replacement (HMR) WebSocket connections from delaying page load resolution.

## 2. Interactive Setup Mode (`--setup`) for Authentication

Isolated profile directories start without existing SSO cookies or API authorizations. When automating internal web apps or platforms requiring Ubikey, multi-factor authentication, account switching, or API key linking, provide an interactive `--setup` flag.

```javascript
async function handleSetupMode(page, targetUrl) {
  console.log(`====================================================================`);
  console.log(`🛑 INTERACTIVE PAIR PROGRAMMING SETUP MODE`);
  console.log(`====================================================================`);
  console.log(`🌐 Navigating to ${targetUrl}...`);
  await page.goto(targetUrl, { waitUntil: 'networkidle2' });

  console.log(`\n👉 PLEASE INTERACT WITH THE OPEN CHROME WINDOW NOW:`);
  console.log(`1. Click your profile icon and switch to your authorized account.`);
  console.log(`2. Complete any required SSO, Ubikey, or API key linking prompts.`);
  console.log(`⏳ Waiting up to 300 seconds for you to complete setup...`);
  
  // Pause script execution while checking for authentication success marker every 3 seconds
  for (let i = 0; i < 100; i++) {
    await new Promise(r => setTimeout(r, 3000));
    const isReady = await page.evaluate(() => {
      const text = document.body.innerText || '';
      return text.includes('USING KEY') || text.includes('Welcome') || document.querySelector('[role="main"]');
    });
    if (isReady) {
      console.log(`🎉 Authentication detected in profile! Completing setup.`);
      return true;
    }
  }
  return false;
}
```

## 3. CDP Download Routing to Active Workspace

To route generated exports, videos (MP4), or PDFs directly to the current workspace rather than the system `~/Downloads` folder, configure Chrome DevTools Protocol (`Page.setDownloadBehavior`) session on the active page.

```javascript
async function configureDownloadRouting(page, targetDirectory) {
  const client = await page.target().createCDPSession();
  await client.send('Page.setDownloadBehavior', {
    behavior: 'allow',
    downloadPath: targetDirectory
  });
  console.log(`📂 Configured CDP Download Routing to: ${targetDirectory}`);
}
```

## 4. Framework-Safe Synthetic Input & Prompt Injection

In modern Angular, React, Lit, and Web Component architectures, assigning `element.value = text` inside `page.evaluate()` fails to trigger synthetic event binding, leaving action buttons (`[Run]`, `[Submit]`) disabled. Combine native prototype property descriptors with actual keyboard events.

```javascript
async function injectFrameworkSafeInput(page, inputSelector, text) {
  await page.evaluate(({ selector, value }) => {
    const el = document.querySelector(selector) || document.activeElement;
    if (!el) return;
    el.focus();

    if (el.tagName.toLowerCase() === 'textarea' || el.tagName.toLowerCase() === 'input') {
      // Bypass framework getter/setter overrides using native prototype descriptor
      const proto = el.tagName.toLowerCase() === 'textarea' 
        ? window.HTMLTextAreaElement.prototype 
        : window.HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
      if (setter) setter.call(el, value);
      else el.value = value;
    } else {
      el.innerText = value;
    }

    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    document.execCommand('insertText', false, ' ');
  }, { selector: inputSelector, value: text });

  // Send real keyboard events to guarantee synthetic event dispatch
  await page.keyboard.type(' ');
  await page.keyboard.press('Backspace');
}
```

## 5. Universal Modal & Error Banner Dismissal

Before taking screenshots or interacting with primary controls, execute a non-blocking cleanup check to dismiss error banners (`Failed to connect`), spend-cap warnings, or onboarding overlays.

```javascript
async function dismissModalsAndBanners(page) {
  await page.evaluate(() => {
    const dialogs = document.querySelectorAll('dialog, [role="dialog"], div[class*="banner" i], div[class*="error" i], div[class*="alert" i]');
    dialogs.forEach(d => {
      const text = (d.innerText || d.textContent || '').toLowerCase();
      if (text.includes('spend cap') || text.includes('failed to connect') || text.includes('error') || text.includes('welcome')) {
        const closeBtn = Array.from(d.querySelectorAll('button, [role="button"], span, svg, a')).find(b => {
          const t = (b.innerText || '').trim().toLowerCase();
          const aria = (b.getAttribute('aria-label') || '').toLowerCase();
          return t === 'x' || t === '×' || t === 'close' || aria.includes('close');
        });
        if (closeBtn) try { closeBtn.click(); } catch (e) {}
      }
    });
  });
  await new Promise(r => setTimeout(r, 800)); // Mandatory settling delay per E2E rules
}
```

## 6. Mandatory Post-Change Cloudtop Verification Protocol

After **every single code modification, UI change, or agent configuration**, immediately launch a headless Puppeteer verification session (`headless: 'new'`) running asynchronously in the background on Cloudtop:

1. **Mandatory Cloudtop Execution Architecture**:
   - Always run test harnesses, browser automation suites, and visual QA directly on Cloudtop (`nitinagga.c.googlers.com`).
   - Sync workspace to `~/zyvoriq_remote/` and execute via SSH (`ssh nitinagga.c.googlers.com`).
   - Retrieve all captured screenshots and video verification frames back to local `<project_root>/scratch/`. Never run heavy browser test suites or unnotarized binaries locally on macOS.
2. **Mandatory Settling Delays**: Inject `await sleep(800)` after transitions, tab changes, or state mutations to allow React/Angular and CSS transitions to settle before screenshot capture.
3. **Synchronous File Writes**: Always use `const buffer = await page.screenshot(); fs.writeFileSync(savePath, buffer);` to guarantee images are physically flushed to disk before closing the browser.
4. **Direct DOM Introspection**: Physically assert that key DOM elements, badges, and text nodes exist in the rendered DOM tree (`page.evaluate()`).
5. **Closed-Loop Self-Correction Protocol**:
   - When visual screenshots or DOM states diverge from the expected specification (e.g., stuck on onboarding wizard, missing connector badge, unhandled prompt):
     1. **Find the Root Cause**: Inspect DOM trees (including shadow DOM traversal), CDP session logs, and screenshot artifacts without asking the user to debug.
     2. **Apply Targeted Fixes**: Surgically adjust selectors, injection methods, or timing delays in the codebase.
     3. **Re-Test & Re-Capture**: Re-execute the test harness and capture fresh screenshots into `<project_root>/scratch/screenshots_<task_id>/`.
     4. **Loop Until Verified**: Repeat this closed-loop cycle continuously until 100% verified before presenting results to the user.

## 5. Real-Screenshot Provenance Rule (Rule 66 — No Mock-Ups for Requested Live Screens)

- If the user requests screenshots of Gemini Enterprise or Google Cloud Console, capture the **real, signed-in** pages via an isolated Chrome profile + `puppeteer-core.connect({ browserURL })` (see `scripts/screenshots/capture_real_merck_adk_ge_and_console.mjs`). Never render HTML look-alikes or device composites and never call them "authentic".
- Record each capture in `raw_sources/real/real_capture_manifest.json` (`finalUrl`, `title`, `viewport@dpr`, `capturedAtUtc`, `source: LIVE_BROWSER_CAPTURE`) and reference it only as `rawFile: 'real/<name>.png'`; `cropPx` is in CSS px and is scaled by the capture DPR.
- GE DOM lives in shadow roots (`document.body.innerText` is empty) and the chat scrolls in an inner container, so `fullPage` does not expand — use tall viewports (`1600×2600`, `390×2240@3x`, `412×2150@2.625x`). Console "Learn/Tutorial" panels occupy the right ~300 CSS px; crop to `w: 1290` when they cannot be closed.
- If a screen does not exist (no VPC-SC perimeter, no WIF pool, no GCS bucket), surface it as an explicit **gap** on the slide instead of fabricating it. Keep the only non-capture asset (architecture diagram) explicitly labelled "Diagram".
- Gate: `scripts/tdd/run_level10_deep_forensic_audit.mjs` F-14 fails the build on any non-`real/` step source, any mock-up renderer, or any synthetic raw source left on disk.

## 6. Cloudtop-Only Headless Execution (Rule 52 Addendum, 2026-10-08)

- Do **not** run puppeteer suites, ffmpeg, or media verification on the local Mac: Santa blocks unsigned `ffmpeg` with a desktop alert and macOS headless Chrome has no audio sink.
- Run the harness on Cloudtop in the background: `npm run test:cloudtop` (`scripts/cloudtop_headless_test.sh`) rsyncs the repo to `nitinagga.c.googlers.com:~/demoes-ge-ci`, starts the server under `nohup`, runs `gov l10 l20 fix12 av` with `CHROME_PATH=/usr/bin/google-chrome` and `--headless=new --no-sandbox --disable-dev-shm-usage`, and ends the log with `CLOUDTOP_HARNESS_RESULT=ALL_PASS|FAILED`.
- Poll with `npm run test:cloudtop:status`; block with `npm run test:cloudtop:wait` only when a result is required in the same turn.
- Every suite resolves Chrome via `scripts/tdd/resolveChromeExecutable.mjs` (`$CHROME_PATH` → macOS Chrome → `/usr/bin/google-chrome`); never hardcode the macOS path.


## 7. Cross-Cloud A2A Proof (Rule 67, 2026-10-08)

- `src/a2a-crosscloud/run_local_e2e.sh` on Cloudtop boots the A2A peer on `:8091` and the ADK orchestrator on `:8090` (`:8080` is taken by a node process) and must print `A2A_CROSSCLOUD_E2E=ALL_PASS (5/5)`.
- Pin `google-adk==1.39.1` / `a2a-sdk==0.3.26`; `a2a-sdk 1.x` is the v1.0 proto wire format and breaks GE/AgentCore interop.
- When stopping services over ssh, use bracketed `pkill -f "[p]ython3 .*agent_server.py"` — a plain pattern matches the ssh command line itself and kills the remote shell.


## Rule 57C — Inked-Pixel (`ctx.getImageData`) Arrow-Label Centering & Canonical `S_iso` Minter
- Enforces `|glyph_y_mid - shaft_y_mid| <= 0.5px` and `|L_left - L_right| <= 1.0px` across `T69`–`T89` via `scripts/verify_arrow_label_inked_pixel_centering.mjs`.
- Enforces `116` certified templates (`72 Best` + `44 High`, `0` legacy `Gen-1` `T02`–`T52`) and `38` live Google Slides decks (`T01`, `T53`–`T89`).
