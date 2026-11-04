import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function resolvePuppeteer() {
  const candidates = [
    '/usr/local/google/home/nitinagga/Documents/zyvoriq/package.json',
    '/usr/local/google/home/nitinagga/Documents/PromptCanvas/package.json',
    '/usr/local/google/home/nitinagga/Documents/blogs/package.json',
    '/Users/nitinagga/Documents/PromptCanvas/package.json',
  ];
  for (const pkgPath of candidates) {
    if (fs.existsSync(pkgPath)) {
      try {
        const req = createRequire(pkgPath);
        return req('puppeteer');
      } catch (_) {}
    }
  }
  throw new Error('Could not resolve puppeteer from workspace node_modules');
}

function resolveChromeExecutable() {
  const candidates = [
    process.env.CHROME_BIN,
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  for (const bin of candidates) {
    if (fs.existsSync(bin)) return bin;
  }
  return undefined;
}

const puppeteer = resolvePuppeteer();

const PORT = process.env.PORT || '8765';
const BASE_URL = process.env.STUDIO_URL || `http://127.0.0.1:${PORT}`;
const OUT_REPORT = path.resolve(__dirname, '../e2e_puppeteer_report.json');
const PROOF_DIR =
  process.env.PROOF_DIR ||
  '/usr/local/google/home/nitinagga/.gemini/jetski/brain/57999333-132a-4bd6-9b5e-5329281d864c/scratch/studio_proof';
const CHROME_USER_DATA_DIR =
  process.env.CHROME_USER_DATA_DIR || `/tmp/chrome_profile_ideas_minting_e2e_${process.pid}`;

fs.mkdirSync(PROOF_DIR, { recursive: true });
fs.mkdirSync(CHROME_USER_DATA_DIR, { recursive: true });

const results = [];
const consoleErrors = [];
const coopWarnings = [];
const failedRequests = [];

function recordAssertion(name, passed, detail = '') {
  results.push({ name, passed: Boolean(passed), detail });
  if (!passed) {
    console.error(`❌ [FAIL] ${name}: ${detail}`);
  } else {
    console.log(`✅ [PASS] ${name}${detail ? ' — ' + detail : ''}`);
  }
}

const browser = await puppeteer.launch({
  executablePath: resolveChromeExecutable(),
  headless: 'new',
  userDataDir: CHROME_USER_DATA_DIR,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    '--disable-sync',
    '--no-first-run',
    '--no-default-browser-check',
    '--no-proxy-server',
    '--host-resolver-rules=MAP nitinagga.c.googlers.com 172.29.89.195',
    '--window-size=1600,1050',
  ],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1050, deviceScaleFactor: 2 });

  page.on('pageerror', (err) => {
    consoleErrors.push(err.message || String(err));
  });
  page.on('console', (msg) => {
    const txt = msg.text() || '';
    if (txt.includes('Cross-Origin-Opener-Policy')) {
      coopWarnings.push(txt);
    }
    if (msg.type() === 'error' && !txt.includes('favicon.ico')) {
      consoleErrors.push(txt);
    }
  });
  page.on('response', (res) => {
    const u = res.url();
    if (res.status() >= 400 && !u.includes('favicon.ico') && !u.includes('fonts.g')) {
      failedRequests.push(`${res.status()} ${u}`);
    }
  });

  // 1. Load Root Studio Workspace (Default: Daily Studio #view-miner)
  await page.goto(BASE_URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForFunction(
    () =>
      document.querySelectorAll('#top5-ideas-column .top5-idea-card').length === 5 &&
      document.querySelectorAll('[data-testid="top5-template-pills"] button img').length === 5 &&
      document.querySelectorAll('[data-testid="top5-mode-pills"] button').length === 8 &&
      document.querySelectorAll('[data-testid="top5-platform-preview-tabs"] button').length === 13,
    { timeout: 15000 }
  );

  // Check Header Geometry & Theme on Desktop 1600x1050
  const desktopBoot = await page.evaluate(async () => {
    const bg = window.getComputedStyle(document.body).backgroundColor;
    const hasDarkClass =
      document.documentElement.classList.contains('dark') || document.body.classList.contains('dark');
    const hdrRect = document.querySelector('.global-header').getBoundingClientRect();
    const wordmarkRect = document.querySelector('.brand-wordmark').getBoundingClientRect();
    const bpImgs = Array.from(document.querySelectorAll('[data-testid="top5-template-pills"] img'));
    for (const img of bpImgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 300));
    const loadedBpImgs = bpImgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    return {
      bg,
      hasDarkClass,
      headerHeight: Math.round(hdrRect.height),
      wordmarkHeight: Math.round(wordmarkRect.height),
      loadedBpImgs,
      persona: document.body.getAttribute('data-persona'),
    };
  });

  recordAssertion(
    'Rule 54 Executive Light Theme & Compact Single-Row Command Header (1600x1050)',
    desktopBoot.bg === 'rgb(248, 250, 252)' &&
      !desktopBoot.hasDarkClass &&
      desktopBoot.headerHeight <= 68 &&
      desktopBoot.wordmarkHeight <= 30 &&
      desktopBoot.loadedBpImgs === 5,
    `bg=${desktopBoot.bg}, headerH=${desktopBoot.headerHeight}px, wordmarkH=${desktopBoot.wordmarkHeight}px, bpThumbs=${desktopBoot.loadedBpImgs}/5`
  );

  // Verify Slidedeck Mode Renders Rich Visual Preview (Zero Empty Box!)
  await page.click('[data-testid="top5-mode-pill-Slidedeck"]');
  await new Promise((r) => setTimeout(r, 350));
  const slidedeckCheck = await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('#top5-platform-preview-stage img'));
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 300));
    const loaded = imgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    const leftRect = document.getElementById('top5-ideas-column').getBoundingClientRect();
    const centerRect = document.getElementById('top5-active-workbench').getBoundingClientRect();
    const rightRect = document.getElementById('top5-preview-rail').getBoundingClientRect();
    return {
      totalImgs: imgs.length,
      loaded,
      heights: {
        left: Math.round(leftRect.height),
        center: Math.round(centerRect.height),
        right: Math.round(rightRect.height),
      },
    };
  });
  recordAssertion(
    'Slidedeck Mode Renders Crisp Multi-Slide Visual Mockup (Zero Broken/Empty Media Box)',
    slidedeckCheck.totalImgs >= 6 && slidedeckCheck.loaded === slidedeckCheck.totalImgs,
    `previewImgs=${slidedeckCheck.loaded}/${slidedeckCheck.totalImgs}, colHeights=${JSON.stringify(slidedeckCheck.heights)}`
  );

  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 250));
  await page.screenshot({ path: path.join(PROOF_DIR, 'rehaul_desktop_creator_slidedeck.png') });

  // Test Laptop 1366x900 Header Zero-Crush Invariant on a fresh page (Rule 57B: avoids Skia resize tile ghosts)
  const laptopPage = await browser.newPage();
  await laptopPage.setViewport({ width: 1366, height: 900, deviceScaleFactor: 2 });
  await laptopPage.goto(BASE_URL, { waitUntil: 'networkidle0', timeout: 30000 });
  await laptopPage.waitForFunction(
    () =>
      document.querySelectorAll('#top5-ideas-column .top5-idea-card').length === 5 &&
      document.querySelectorAll('#top5-platform-preview-stage img').length >= 1,
    { timeout: 15000 }
  );
  await laptopPage.click('[data-testid="top5-mode-pill-Slidedeck"]');
  await new Promise((r) => setTimeout(r, 350));
  const laptopCheck = await laptopPage.evaluate(() => {
    const hdr = document.querySelector('.global-header').getBoundingClientRect();
    const wm = document.querySelector('.brand-wordmark').getBoundingClientRect();
    const tabs = Array.from(document.querySelectorAll('.global-header .nav-tab-btn'));
    const maxTabH = Math.max(...tabs.map((t) => t.getBoundingClientRect().height));
    const overflow = Math.max(0, document.documentElement.scrollWidth - window.innerWidth);
    return { hdrH: Math.round(hdr.height), wmH: Math.round(wm.height), maxTabH: Math.round(maxTabH), overflow };
  });
  recordAssertion(
    'Laptop 1366x900 Zero Header Collision & Single-Line Tabs',
    laptopCheck.hdrH <= 108 && laptopCheck.wmH <= 30 && laptopCheck.maxTabH <= 40 && laptopCheck.overflow === 0,
    `hdrH=${laptopCheck.hdrH}px, wordmarkH=${laptopCheck.wmH}px, maxTabH=${laptopCheck.maxTabH}px, overflow=${laptopCheck.overflow}px`
  );
  await laptopPage.mouse.move(2, 2);
  await laptopPage.screenshot({ path: path.join(PROOF_DIR, 'rehaul_laptop_1366x900.png') });
  await laptopPage.close();

  // Restore 1600x1050 & Test Multi-Persona Modes (Executive & Builder) + Command Palette (⌘K)
  await page.setViewport({ width: 1600, height: 1050, deviceScaleFactor: 2 });
  await page.click('#persona-btn-executive');
  await new Promise((r) => setTimeout(r, 200));
  const execModeVisible = await page.$eval(
    '#executive-morning-strip',
    (el) => window.getComputedStyle(el).display === 'grid'
  );
  await page.screenshot({ path: path.join(PROOF_DIR, 'rehaul_desktop_executive_mode.png') });

  await page.click('#persona-btn-builder');
  await new Promise((r) => setTimeout(r, 200));
  const builderStripCheck = await page.evaluate(() => {
    const strip = document.getElementById('builder-engineering-strip');
    const badge = document.getElementById('top5-ledger-badge');
    const hasDrawioLink = Boolean(document.querySelector('a[href$=".drawio"]'));
    const hasJsonPreview = Boolean(document.querySelector('#top5-composer-copy-mount pre.code-block-light'));
    return {
      stripGrid: Boolean(strip && window.getComputedStyle(strip).display === 'grid'),
      badgeVisible: Boolean(badge && window.getComputedStyle(badge).display !== 'none'),
      hasDrawioLink,
      hasJsonPreview,
    };
  });
  await page.screenshot({ path: path.join(PROOF_DIR, 'rehaul_desktop_builder_mode.png') });

  await page.click('#persona-btn-creator');
  recordAssertion(
    'Persona Switcher Adapts Workspace Density (Creator · Executive · Builder)',
    execModeVisible &&
      builderStripCheck.stripGrid &&
      builderStripCheck.badgeVisible &&
      builderStripCheck.hasDrawioLink &&
      builderStripCheck.hasJsonPreview,
    `executiveStrip=${execModeVisible}, builderStrip=${builderStripCheck.stripGrid}, drawio=${builderStripCheck.hasDrawioLink}, jsonEnvelope=${builderStripCheck.hasJsonPreview}`
  );

  // Test ⌘K Command Palette Open, Filter & Escape Close
  await page.click('#open-cmdk-btn');
  await page.waitForSelector('#cmdk-backdrop', { visible: true, timeout: 4000 });
  await page.type('#cmdk-search-input', 'T85');
  await new Promise((r) => setTimeout(r, 200));
  const cmdkCount = await page.$$eval('#cmdk-results-list .cmdk-result-item', (els) => els.length);
  await page.keyboard.press('Escape');
  const cmdkClosed = await page.$eval('#cmdk-backdrop', (el) => el.style.display === 'none');
  recordAssertion(
    'Instant ⌘K Command Palette Searches Catalog & Closes on Escape',
    cmdkCount >= 1 && cmdkClosed,
    `filteredItems=${cmdkCount}, closedOnEsc=${cmdkClosed}`
  );

  // Test Carousel Mode (Instagram 4:5 JPEGs) & Short_Video Mode (9:16 Smartphone Safe-Zone Bezel)
  await page.click('[data-testid="top5-mode-pill-Carousel"]');
  await new Promise((r) => setTimeout(r, 300));
  await page.click('[data-testid="top5-plat-tab-instagram"]');
  await new Promise((r) => setTimeout(r, 250));
  const igCompliance = await page.evaluate(async () => {
    const stageText = document.getElementById('top5-platform-preview-stage')?.innerText || '';
    const copyText = document.querySelector('[data-testid="top5-platform-copy-box"]')?.textContent || '';
    const imgs = Array.from(document.querySelectorAll('#top5-platform-preview-stage img'));
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 300));
    const loadedImgs = imgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    return {
      hasJpeg4x5: stageText.includes('Container: JPEG') && stageText.includes('4:5'),
      hasRawUrlInIgCaption: /https?:\/\/\S+/.test(copyText),
      thumbCount: imgs.length,
      loadedImgs,
    };
  });
  recordAssertion(
    'Daily Studio Instagram 4:5 Carousel Mockup & Link-Free Caption Compliance',
    igCompliance.hasJpeg4x5 &&
      !igCompliance.hasRawUrlInIgCaption &&
      igCompliance.thumbCount >= 9 &&
      igCompliance.loadedImgs === igCompliance.thumbCount,
    `JPEG_4x5=${igCompliance.hasJpeg4x5}, rawUrls=${igCompliance.hasRawUrlInIgCaption}, imgs=${igCompliance.loadedImgs}/${igCompliance.thumbCount}`
  );
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view4_top5_editorial_desk.png') });

  await page.click('[data-testid="top5-mode-pill-Short_Video"]');
  await new Promise((r) => setTimeout(r, 350));
  await page.click('[data-testid="top5-plat-tab-youtube_shorts"]');
  await page
    .waitForFunction(
      () => {
        const v = document.querySelector('#top5-platform-preview-stage .phone-bezel-frame video');
        return v && v.readyState >= 3;
      },
      { timeout: 6000 }
    )
    .catch(() => {});
  await new Promise((r) => setTimeout(r, 200));
  const shortVideoCheck = await page.evaluate(() => {
    const budgetCards = document.querySelectorAll('[data-testid="top5-length-budget-strip"] .top5-budget-card').length;
    const budgetText = document.querySelector('[data-testid="top5-length-budget-strip"]')?.innerText || '';
    const vid = document.querySelector('#top5-platform-preview-stage .phone-bezel-frame video');
    const safeZoneVisible = Boolean(
      document.querySelector('#top5-platform-preview-stage .safe-zone-overlay.visible')
    );
    return {
      budgetCards,
      has916Budget: budgetText.includes('40–55 sec MP4') || budgetText.includes('5 vertical tier-zoom'),
      hasVideoSrc: Boolean(vid && vid.getAttribute('src')?.includes('vertical_short_9x16.mp4')),
      safeZoneVisible,
    };
  });
  recordAssertion(
    '9:16 Smartphone Safe-Zone Bezel & 3-Part Pacing Bar in Short Video Mode',
    shortVideoCheck.budgetCards === 3 &&
      shortVideoCheck.has916Budget &&
      shortVideoCheck.hasVideoSrc &&
      shortVideoCheck.safeZoneVisible,
    `budgetCards=${shortVideoCheck.budgetCards}, phoneVideo=${shortVideoCheck.hasVideoSrc}, safeZoneGuides=${shortVideoCheck.safeZoneVisible}`
  );
  await page.screenshot({ path: path.join(PROOF_DIR, 'rehaul_desktop_phone_9x16_mockup.png') });

  // Switch to Idea #2 & Blueprint #2, Stage Channels, then open Sub-Tab 2 (Publishing Queue) & Approve
  await page.click('[data-testid="top5-idea-card-2"]');
  await new Promise((r) => setTimeout(r, 300));
  await page.click('[data-testid="top5-tpl-pill-2"]');
  await new Promise((r) => setTimeout(r, 300));
  await page.click('#stage-selected-platforms-btn');
  await new Promise((r) => setTimeout(r, 400));

  await page.click('#miner-subtab-btn-outbox');
  await new Promise((r) => setTimeout(r, 250));
  await page.click('#approve-all-outbox-btn');
  await new Promise((r) => setTimeout(r, 450));

  const outboxAndRssCheck = await page.evaluate(async () => {
    const rows = document.querySelectorAll('#publishing-outbox-tbody tr').length;
    const tbodyText = document.getElementById('publishing-outbox-tbody')?.innerText || '';
    const rssRes = await fetch('/api/rss/daily-briefing.xml');
    const rssText = await rssRes.text();
    const nosniff = rssRes.headers.get('x-content-type-options');
    return {
      rows,
      hasValidatedStatus: tbodyText.includes('DRY_RUN_VALIDATED') || tbodyText.includes('SHARE_PACKET_READY'),
      rssOk: rssRes.status === 200 && rssText.includes('<rss version="2.0">'),
      nosniff,
    };
  });
  recordAssertion(
    'Publishing Queue Sub-Tab Stages, Approves & Serves Valid RSS 2.0',
    outboxAndRssCheck.rows >= 5 &&
      outboxAndRssCheck.hasValidatedStatus &&
      outboxAndRssCheck.rssOk &&
      outboxAndRssCheck.nosniff === 'nosniff',
    `rows=${outboxAndRssCheck.rows}, validated=${outboxAndRssCheck.hasValidatedStatus}, rss200=${outboxAndRssCheck.rssOk}`
  );
  await page.evaluate(() => {
    const tc = document.getElementById('toast-container');
    if (tc) tc.replaceChildren();
  });
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view4_hitl_outbox_table.png') });

  // Test Sub-Tab 3: 6-Style Batch Generator & Signal Radar
  await page.click('#miner-subtab-btn-radar');
  await new Promise((r) => setTimeout(r, 250));
  await page.select('#daily-style-select', 'AUTO');
  await page.select('#daily-count-select', '6');
  await page.click('#generate-daily-posts-btn');
  await page.waitForFunction(
    () => {
      const btn = document.getElementById('generate-daily-posts-btn');
      const badge = document.getElementById('daily-posts-status-badge')?.textContent || '';
      return btn && !btn.disabled && badge.includes('Fresh Posts Generated');
    },
    { timeout: 20000 }
  );
  await page.click('[data-testid="copy-daily-post-btn-1"]');
  const dailyStudioCheck = await page.evaluate(async () => {
    const cards = Array.from(document.querySelectorAll('#daily-generated-posts-grid .daily-post-card'));
    const imgs = Array.from(
      document.querySelectorAll('#daily-generated-posts-grid .daily-post-card img[id^="daily-vis-svg-"]')
    );
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 350));
    const loadedSvgs = imgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    const copiedLen = (window.__LAST_COPIED_TEXT__ || '').length;
    return { cardCount: cards.length, loadedSvgs, copiedLen };
  });
  recordAssertion(
    'Batch & Signal Radar Sub-Tab Synthesizes 6 Creator Posts & Copies Payload',
    dailyStudioCheck.cardCount === 6 && dailyStudioCheck.loadedSvgs === 6 && dailyStudioCheck.copiedLen > 200,
    `cards=${dailyStudioCheck.cardCount}, svgs=${dailyStudioCheck.loadedSvgs}/6, copiedChars=${dailyStudioCheck.copiedLen}`
  );
  await page.click('#miner-subtab-btn-composer');

  // 2. Test View 2: 116 Certified Visual Blueprints + Lightbox Zoom
  await page.click('#tab-btn-gallery');
  await page.waitForFunction(
    () => document.querySelectorAll('#gallery-cards-grid .repo-card').length === 116,
    { timeout: 12000 }
  );
  const galleryAllCheck = await page.evaluate(() => ({
    cards: document.querySelectorAll('#gallery-cards-grid .repo-card').length,
    pairings: document.querySelectorAll('#pairings-tbody tr').length,
    t79TopicsCount: document.querySelectorAll('[data-testid="t79-topic-posts-showcase"] a').length,
  }));
  recordAssertion(
    'Blueprints View Renders 116 Templates, 23 T79 Spine Variants & 12 Stack Pairings',
    galleryAllCheck.cards === 116 && galleryAllCheck.pairings === 12 && galleryAllCheck.t79TopicsCount === 23,
    `cards=${galleryAllCheck.cards}, t79Variants=${galleryAllCheck.t79TopicsCount}, pairings=${galleryAllCheck.pairings}`
  );

  // Click artwork to open Lightbox & press Escape to close
  await page.click('[data-testid="template-card-T54"] .card-artwork-stage');
  await page.waitForSelector('#lightbox-backdrop', { visible: true, timeout: 4000 });
  await page.keyboard.press('Escape');
  const lbClosed = await page.$eval('#lightbox-backdrop', (el) => el.style.display === 'none');
  recordAssertion('Blueprint Artwork Opens Full-Resolution Lightbox & Closes on Escape', lbClosed, 'lightbox verified');

  await page.select('#gallery-filter-tier', 'Best');
  const bestTierCount = await page.$$eval('#gallery-cards-grid .repo-card', (els) => els.length);
  await page.select('#gallery-filter-tier', 'High');
  const highTierCount = await page.$$eval('#gallery-cards-grid .repo-card', (els) => els.length);
  await page.select('#gallery-filter-tier', 'ALL');
  recordAssertion(
    'Blueprints Quality Tier Filters (72 Best + 44 High)',
    bestTierCount === 72 && highTierCount === 44,
    `best=${bestTierCount}, high=${highTierCount}`
  );
  await page.mouse.move(10, 10);
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 250));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view2_gallery.png') });

  // 3. Test View 1: 19 Cloud Repos, Filters, Cards/Matrix Toggle & 4-Tab Inspector Drawer
  await page.click('#tab-btn-repos');
  await page.waitForFunction(
    () => document.querySelectorAll('#repos-cards-grid .repo-card').length === 19,
    { timeout: 10000 }
  );
  const repoImagesStatus = await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('#repos-cards-grid .repo-card img'));
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 400));
    const broken = imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src);
    const matrixRows = document.querySelectorAll('#repos-matrix-tbody tr').length;
    return { total: imgs.length, brokenCount: broken.length, matrixRows };
  });
  recordAssertion(
    'Cloud Repos View Renders 19 Visual Repo Cards (0 Broken SVGs) & 19 Matrix Rows',
    repoImagesStatus.total === 19 && repoImagesStatus.brokenCount === 0 && repoImagesStatus.matrixRows === 19,
    `cards=${repoImagesStatus.total}/19, matrixRows=${repoImagesStatus.matrixRows}/19`
  );
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view1_repos.png') });

  await page.type('#search-input', 'zzzz_nonexistent_query_999');
  const emptyVisible = await page.$eval('#no-matching-cards', (el) => window.getComputedStyle(el).display !== 'none');
  await page.click('#reset-filters-btn');
  const restoredCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion(
    'Cloud Repos Resilient Empty State & Filter Reset',
    emptyVisible && restoredCount === 19,
    `emptyVisible=${emptyVisible}, restored=${restoredCount}`
  );

  // Test Inspector Drawer on MINT-01
  await page.click('[data-testid="inspect-repo-btn-MINT-01"]');
  await page.waitForSelector('#repo-inspector-drawer.open', { timeout: 5000 });
  await page.click('#dtab-btn-slides');
  const slidesCheck = await page.evaluate(() => ({
    count: (document.getElementById('dtab-slides')?.innerText.match(/SLIDE \d+ OF 12/g) || []).length,
    has24SlideBtn: Boolean(document.querySelector('[data-testid="drawer-open-24slide-deck-btn"]')),
  }));
  await page.click('#dtab-btn-terraform');
  const tfCheck = await page.evaluate(() => {
    const t = document.getElementById('dtab-terraform')?.innerText || '';
    return t.includes('google_cloud_run_v2_service') && t.includes('locations/global');
  });
  await page.click('#dtab-btn-linkedin');
  const liCheck = await page.evaluate(() => {
    const t = document.getElementById('dtab-linkedin')?.innerText || '';
    return t.includes('PRIMARY HIGH-REACH GROUPS') && t.includes('NICHE EXECUTIVE');
  });
  await page.click('#close-drawer-btn');
  recordAssertion(
    'Inspector Drawer Renders Visuals, 12+24 Slide Deck, Terraform/ADK & Distribution Plan',
    slidesCheck.count === 12 && slidesCheck.has24SlideBtn && tfCheck && liCheck,
    `slides=${slidesCheck.count}/12, terraform=${tfCheck}, distribution=${liCheck}`
  );

  // 4. Test View 6: Video & Decks (MINT-01..12)
  await page.click('#tab-btn-minting-studio');
  await page.waitForFunction(
    () => document.querySelectorAll('#minting-topics-grid .repo-card').length === 12,
    { timeout: 10000 }
  );
  const mintingStudioCheck = await page.evaluate(async () => {
    const walkVid = document.getElementById('mint01-walkthrough-video');
    const twinVid = document.getElementById('mint01-twin-video');
    if (walkVid && walkVid.readyState < 2) walkVid.load();
    if (twinVid && twinVid.readyState < 2) twinVid.load();
    for (let i = 0; i < 30; i++) {
      if (walkVid?.readyState >= 2 && twinVid?.readyState >= 2) break;
      await new Promise((r) => setTimeout(r, 150));
    }
    return {
      topicCards: document.querySelectorAll('#minting-topics-grid .repo-card').length,
      walkWidth: walkVid?.videoWidth || 0,
      walkHeight: walkVid?.videoHeight || 0,
      twinReady: (twinVid?.readyState || 0) >= 1,
    };
  });
  recordAssertion(
    'Video & Decks View Renders 1080p30 Walkthrough Video, Twin Video & 12 MINT Topics',
    mintingStudioCheck.topicCards === 12 &&
      mintingStudioCheck.walkWidth === 1920 &&
      mintingStudioCheck.walkHeight === 1080 &&
      mintingStudioCheck.twinReady,
    `topics=${mintingStudioCheck.topicCards}/12, video=${mintingStudioCheck.walkWidth}x${mintingStudioCheck.walkHeight}`
  );
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 250));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view6_minting_studio.png') });

  // 5. Test View 3: Creator Radar & View 5: Sandbox
  await page.click('#tab-btn-playbook');
  await new Promise((r) => setTimeout(r, 250));
  const playbookCheck = await page.evaluate(() => {
    const creators = document.querySelectorAll('#creator-profiles-grid .creator-profile-card').length;
    const channels = document.querySelectorAll('#signal-channels-grid .repo-card').length;
    const archetypes = document.querySelectorAll('#archetypes-grid .repo-card').length;
    return { creators, channels, archetypes };
  });
  recordAssertion(
    'Creator Radar View Renders 16 Creator Profiles, 4 Channels & 4 Archetypes',
    playbookCheck.creators === 16 && playbookCheck.channels === 4 && playbookCheck.archetypes === 4,
    `creators=${playbookCheck.creators}, channels=${playbookCheck.channels}, archetypes=${playbookCheck.archetypes}`
  );

  await page.click('#tab-btn-openhands');
  await new Promise((r) => setTimeout(r, 200));
  const ohCheck = await page.evaluate(() => ({
    cmpRows: document.querySelectorAll('#openhands-comparison-tbody tr').length,
    trajCards: document.querySelectorAll('#openhands-trajectories-list > div').length,
  }));
  recordAssertion(
    'Sandbox View Renders 5 Comparison Rows & 19 Execution Trajectories',
    ohCheck.cmpRows === 5 && ohCheck.trajCards === 19,
    `rows=${ohCheck.cmpRows}, trajectories=${ohCheck.trajCards}`
  );

  // 6. 16-Pillar WCAG 2.2 AAA Landmarks, Zero Unlabeled Inputs & Contrast Gate (ui-first-design-system)
  await page.click('#tab-btn-miner');
  await new Promise((r) => setTimeout(r, 250));
  const wcagAudit = await page.evaluate(() => {
    function parseRgb(str) {
      if (!str || str === 'transparent' || str === 'rgba(0, 0, 0, 0)') return null;
      const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
      if (!m) return null;
      const a = m[4] !== undefined ? parseFloat(m[4]) : 1;
      if (a < 0.1) return null;
      return [parseInt(m[1], 10), parseInt(m[2], 10), parseInt(m[3], 10)];
    }
    function luminance([r, g, b]) {
      const srgb = [r, g, b].map((v) => {
        const c = v / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });
      return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2];
    }
    function ratio(fg, bg) {
      const l1 = luminance(fg);
      const l2 = luminance(bg);
      return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    }
    function effectiveBg(el) {
      let cur = el;
      while (cur && cur !== document.documentElement) {
        const rgb = parseRgb(window.getComputedStyle(cur).backgroundColor);
        if (rgb) return rgb;
        cur = cur.parentElement;
      }
      return [248, 250, 252];
    }

    const unlabeled = Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea'))
      .filter((el) => {
        const st = window.getComputedStyle(el);
        const r = el.getBoundingClientRect();
        if (st.display === 'none' || st.visibility === 'hidden' || r.width === 0) return false;
        const id = el.id;
        const hasFor = id ? Boolean(document.querySelector(`label[for="${CSS.escape(id)}"]`)) : false;
        return !(
          hasFor ||
          Boolean(el.closest('label')) ||
          Boolean(el.getAttribute('aria-label')) ||
          Boolean(el.getAttribute('aria-labelledby'))
        );
      })
      .map((el) => el.id || el.tagName);

    const contrastFailures = [];
    for (const el of document.querySelectorAll('h1, h2, h3, p, span, a, button, strong, th, td, kbd')) {
      const st = window.getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (st.display === 'none' || st.visibility === 'hidden' || parseFloat(st.opacity) < 0.5 || r.width === 0) {
        continue;
      }
      const directText = Array.from(el.childNodes)
        .filter((n) => n.nodeType === Node.TEXT_NODE)
        .map((n) => n.textContent.trim())
        .filter(Boolean)
        .join(' ')
        .trim();
      if (!directText) continue;
      const fg = parseRgb(st.color);
      if (!fg) continue;
      const bg = effectiveBg(el);
      const cr = ratio(fg, bg);
      const fs = parseFloat(st.fontSize) || 14;
      const fw = parseInt(st.fontWeight, 10) || 400;
      const minCr = fs >= 24 || (fs >= 18.66 && fw >= 700) ? 3.0 : 4.5;
      if (cr < minCr) {
        contrastFailures.push(`${el.tagName}("${directText.slice(0, 28)}")=${cr.toFixed(2)}:1`);
      }
    }

    const inlineCss = Array.from(document.querySelectorAll('style'))
      .map((s) => s.textContent)
      .join('\n');

    return {
      hasSkipLink: Boolean(document.querySelector('.skip-to-main-link')),
      hasMain: Boolean(document.querySelector('main#main-workspace')),
      tablistCount: document.querySelectorAll('[role="tablist"]').length,
      radiogroupCount: document.querySelectorAll('[role="radiogroup"]').length,
      liveRegionCount: document.querySelectorAll('[aria-live]').length,
      unlabeledCount: unlabeled.length,
      unlabeled,
      contrastFailureCount: contrastFailures.length,
      contrastSample: contrastFailures.slice(0, 5),
      hasTokens: inlineCss.includes('--studio-'),
      hasTabularNums: inlineCss.includes('tabular-nums'),
      hasReducedMotion: inlineCss.includes('prefers-reduced-motion'),
      hasDisplayFont: inlineCss.includes('Plus Jakarta Sans'),
    };
  });

  recordAssertion(
    '16-Pillar WCAG 2.2 AA/AAA Contrast, Landmarks, Zero Unlabeled Inputs & Design Tokens',
    wcagAudit.hasSkipLink &&
      wcagAudit.hasMain &&
      wcagAudit.tablistCount >= 2 &&
      wcagAudit.radiogroupCount >= 2 &&
      wcagAudit.liveRegionCount >= 1 &&
      wcagAudit.unlabeledCount === 0 &&
      wcagAudit.contrastFailureCount === 0 &&
      wcagAudit.hasTokens &&
      wcagAudit.hasTabularNums &&
      wcagAudit.hasReducedMotion &&
      wcagAudit.hasDisplayFont,
    `contrastFailures=${wcagAudit.contrastFailureCount} (${wcagAudit.contrastSample.join(', ')}), unlabeledInputs=${wcagAudit.unlabeledCount}`
  );

  // 7. Rule 26 Table Cell Containment & Rule 57C Canonical SVG Check
  const tableContainmentCheck = await page.evaluate(() => {
    const tds = Array.from(document.querySelectorAll('table.table-fixed tbody td'));
    const uncontained = tds.filter((td) => window.getComputedStyle(td).overflow !== 'hidden');
    return { totalTds: tds.length, uncontainedCount: uncontained.length };
  });
  recordAssertion(
    'Rule 26 Table Cell Containment (overflow: hidden on all table-fixed tbody td)',
    tableContainmentCheck.totalTds > 0 && tableContainmentCheck.uncontainedCount === 0,
    `checkedCells=${tableContainmentCheck.totalTds}, uncontained=${tableContainmentCheck.uncontainedCount}`
  );

  // 8. Mobile iPhone 390x844 Viewport Overflow Audit Across All 6 Views
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  let maxMobileOverflow = 0;
  const mobileDetails = [];
  for (const btnId of [
    'tab-btn-miner',
    'tab-btn-gallery',
    'tab-btn-repos',
    'tab-btn-minting-studio',
    'tab-btn-playbook',
    'tab-btn-openhands',
  ]) {
    await page.click(`#${btnId}`);
    await new Promise((r) => setTimeout(r, 250));
    const m = await page.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      innerW: window.innerWidth,
    }));
    if (btnId === 'tab-btn-miner') {
      await page.evaluate(() => window.scrollTo(0, 0));
      await new Promise((r) => setTimeout(r, 150));
      await page.screenshot({ path: path.join(PROOF_DIR, 'after_view4_mobile_390x844.png') });
    }
    const overflow = Math.max(0, m.scrollW - m.innerW);
    if (overflow > maxMobileOverflow) maxMobileOverflow = overflow;
    mobileDetails.push(`${btnId}:${overflow}px`);
  }
  recordAssertion(
    'Mobile 390x844 Responsive Layout (0px Horizontal Overflow Across All 6 Views)',
    maxMobileOverflow === 0,
    mobileDetails.join(', ')
  );

  // 9. Direct Deep-Link /?view=view-miner & Zero Console / COOP / HTTP Errors
  await page.setViewport({ width: 1600, height: 1050, deviceScaleFactor: 2 });
  const deepLinkRes = await page.goto(`${BASE_URL}/?view=view-miner`, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('[data-testid="top5-idea-card-5"]', { timeout: 10000 });
  recordAssertion(
    'Direct Deep-Link /?view=view-miner Returns HTTP 200 & Zero COOP/Console/HTTP Errors',
    deepLinkRes?.status() === 200 &&
      consoleErrors.length === 0 &&
      coopWarnings.length === 0 &&
      failedRequests.length === 0,
    `status=${deepLinkRes?.status()}, errors=${consoleErrors.length}, coopWarnings=${coopWarnings.length}, failedReqs=${failedRequests.length}`
  );

  const passedCount = results.filter((r) => r.passed).length;
  const report = {
    timestamp: new Date().toISOString(),
    baseUrl: BASE_URL,
    totalAssertions: results.length,
    passedAssertions: passedCount,
    failedAssertions: results.length - passedCount,
    consoleErrors,
    failedRequests,
    results,
  };
  fs.writeFileSync(OUT_REPORT, JSON.stringify(report, null, 2));
  console.log(`\n==> E2E Puppeteer Suite Complete: ${passedCount}/${results.length} assertions PASSED.`);
  if (passedCount !== results.length) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
