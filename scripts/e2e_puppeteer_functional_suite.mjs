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
    '--window-size=1600,1050',
  ],
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1050, deviceScaleFactor: 2 });

  page.on('pageerror', (err) => {
    consoleErrors.push(err.message || String(err));
  });
  page.on('response', (res) => {
    if (res.status() >= 400 && !res.url().includes('favicon.ico')) {
      failedRequests.push(`${res.status()} ${res.url()}`);
    }
  });

  // 1. Load Root Studio Workspace (View 1: 19 Repos)
  await page.goto(BASE_URL, { waitUntil: 'networkidle0', timeout: 30000 });

  const themeAndGeometry = await page.evaluate(() => {
    const bg = window.getComputedStyle(document.body).backgroundColor;
    const hasDarkClass =
      document.documentElement.classList.contains('dark') || document.body.classList.contains('dark');
    const scrollW = document.documentElement.scrollWidth;
    const innerW = window.innerWidth;
    const repoCards = document.querySelectorAll('#repos-cards-grid .repo-card').length;
    const matrixRows = document.querySelectorAll('#repos-matrix-tbody tr').length;
    const reposBadge = document.getElementById('telemetry-repos-badge')?.textContent?.trim();
    const testsBadge = document.getElementById('telemetry-tests-badge')?.textContent?.trim();
    return { bg, hasDarkClass, scrollW, innerW, repoCards, matrixRows, reposBadge, testsBadge };
  });

  recordAssertion(
    'Rule 54 Executive Light Theme Default',
    themeAndGeometry.bg === 'rgb(248, 250, 252)' && !themeAndGeometry.hasDarkClass,
    `body bg=${themeAndGeometry.bg}, darkClass=${themeAndGeometry.hasDarkClass}`
  );
  recordAssertion(
    'Zero Horizontal Overflow on View 1 (19 Repos)',
    themeAndGeometry.scrollW <= themeAndGeometry.innerW,
    `scrollWidth=${themeAndGeometry.scrollW} <= innerWidth=${themeAndGeometry.innerW}`
  );
  recordAssertion(
    'View 1 Renders All 19 Repo Cards & 19 Matrix Rows',
    themeAndGeometry.repoCards === 19 && themeAndGeometry.matrixRows === 19,
    `cards=${themeAndGeometry.repoCards}, rows=${themeAndGeometry.matrixRows}, badges=${themeAndGeometry.reposBadge} | ${themeAndGeometry.testsBadge}`
  );

  // Verify all 19 repo card lead images load cleanly
  const repoImagesStatus = await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('#repos-cards-grid .repo-card img'));
    for (const img of imgs) {
      img.loading = 'eager';
      img.scrollIntoView();
    }
    await new Promise((r) => setTimeout(r, 400));
    const broken = imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src);
    return { total: imgs.length, broken };
  });
  recordAssertion(
    'All 19 Repo Card Lead SVGs Load with naturalWidth > 0',
    repoImagesStatus.total === 19 && repoImagesStatus.broken.length === 0,
    `loaded=${repoImagesStatus.total - repoImagesStatus.broken.length}/19`
  );

  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 200));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view1_repos.png') });

  // Test Series Filter (#filter-archetype)
  await page.select('#filter-archetype', 'MINT');
  const mintCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Series MINT (Flagship Career-Minting Exemplar MINT-01)', mintCount === 1, `cards=${mintCount}`);

  await page.select('#filter-archetype', 'ARCH-DYN');
  const dynCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Series ARCH-DYN (Tomorrow Morning EST Top 10)', dynCount === 10, `cards=${dynCount}`);

  await page.select('#filter-archetype', 'ARCH-2D');
  const postCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Series ARCH-2D (8 Creator Signal Posts)', postCount === 8, `cards=${postCount}`);

  await page.select('#filter-archetype', 'ALL');

  // Test Creator Filter (#filter-author)
  await page.select('#filter-author', 'Rakesh Gohel');
  const rakeshCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Creator Rakesh Gohel', rakeshCount >= 2, `cards=${rakeshCount}`);
  await page.select('#filter-author', 'ALL');

  // Test Search Input & Empty State Reset (Rule 25K)
  await page.type('#search-input', 'zzzz_nonexistent_query_999');
  const emptyVisible = await page.$eval('#no-matching-cards', (el) => window.getComputedStyle(el).display !== 'none');
  recordAssertion('Empty Search Shows Resilient Empty State (#no-matching-cards)', emptyVisible, 'empty state visible');

  await page.click('#reset-filters-btn');
  const restoredCount = await page.$$eval('#repos-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Reset Filters Button Restores All 19 Repos', restoredCount === 19, `cards=${restoredCount}`);

  // 2. Test Right-Side Inspector Drawer on MINT-01 & All 4 Drawer Tabs
  await page.click('[data-testid="inspect-repo-btn-MINT-01"]');
  await page.waitForSelector('#repo-inspector-drawer.open', { timeout: 5000 });

  const drawerTab1 = await page.evaluate(async () => {
    const badge = document.getElementById('drawer-repo-badge')?.textContent?.trim() || '';
    const title = document.getElementById('drawer-repo-title')?.textContent?.trim() || '';
    const imgs = Array.from(document.querySelectorAll('#dtab-visuals img'));
    await new Promise((r) => setTimeout(r, 350));
    const loadedImgs = imgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    const nb3Len = document.getElementById('nb3-prompt-pre')?.innerText?.length || 0;
    return { badge, title, totalImgs: imgs.length, loadedImgs, nb3Len };
  });
  recordAssertion(
    'Inspector Drawer Tab 1 (MINT-01 Dynamic & @2d Visuals) Renders All Figures & Prompt',
    drawerTab1.badge.includes('MINT-01') &&
      drawerTab1.totalImgs >= 4 &&
      drawerTab1.loadedImgs === drawerTab1.totalImgs &&
      drawerTab1.nb3Len > 100,
    `badge="${drawerTab1.badge}", images=${drawerTab1.loadedImgs}/${drawerTab1.totalImgs}, promptChars=${drawerTab1.nb3Len}`
  );

  await page.click('#dtab-btn-slides');
  const slidesCheck = await page.evaluate(() => {
    const text = document.getElementById('dtab-slides')?.innerText || '';
    const matches = text.match(/SLIDE \d+ OF 12/g) || [];
    const has24SlideBtn = Boolean(document.querySelector('[data-testid="drawer-open-24slide-deck-btn"]'));
    return { count: matches.length, has24SlideBtn };
  });
  recordAssertion(
    'Inspector Drawer Tab 2 Renders 24-Slide Google Slides Link + 12-Slide Deck',
    slidesCheck.count === 12 && slidesCheck.has24SlideBtn,
    `slides=${slidesCheck.count}/12, 24SlideBtn=${slidesCheck.has24SlideBtn}`
  );

  await page.click('#dtab-btn-terraform');
  const tfCheck = await page.evaluate(() => {
    const text = document.getElementById('dtab-terraform')?.innerText || '';
    return {
      hasMainTf: text.includes('google_cloud_run_v2_service'),
      hasEnginePy: text.includes('locations/global') && text.includes('thinkingLevel'),
    };
  });
  recordAssertion(
    'Inspector Drawer Tab 3 (1-Click GCP Terraform & ADK Code) Renders main.tf & Rule 55 engine.py',
    tfCheck.hasMainTf && tfCheck.hasEnginePy,
    `main.tf=${tfCheck.hasMainTf}, engine.py=${tfCheck.hasEnginePy}`
  );

  await page.click('#dtab-btn-linkedin');
  const liCheck = await page.evaluate(() => {
    const text = document.getElementById('dtab-linkedin')?.innerText || '';
    const draftLen = document.getElementById('linkedin-copy-pre')?.innerText?.length || 0;
    return {
      hasGroups: text.includes('PRIMARY HIGH-REACH GROUPS') && text.includes('NICHE EXECUTIVE'),
      draftLen,
    };
  });
  recordAssertion(
    'Inspector Drawer Tab 4 (LinkedIn Copy & Group Distribution Plan)',
    liCheck.hasGroups && liCheck.draftLen > 200,
    `hasGroups=${liCheck.hasGroups}, draftChars=${liCheck.draftLen}`
  );

  await page.click('#close-drawer-btn');
  const drawerClosed = await page.$eval('#repo-inspector-drawer', (el) => !el.classList.contains('open'));
  recordAssertion('Close Drawer Button Collapses Inspector Drawer', drawerClosed, 'drawer closed');

  // 3. Test View 2: 116 Certified Visual Template Gallery (72 Best + 44 High)
  await page.click('#tab-btn-gallery');
  await page.waitForFunction(
    () => document.querySelectorAll('#gallery-cards-grid .repo-card').length === 116,
    { timeout: 12000 }
  );

  const galleryAllCheck = await page.evaluate(async () => {
    const cards = document.querySelectorAll('#gallery-cards-grid .repo-card').length;
    const badge = document.getElementById('gallery-count-badge')?.textContent?.trim();
    const pairings = document.querySelectorAll('#pairings-tbody tr').length;
    const t79TopicsCount = document.querySelectorAll('[data-testid="t79-topic-posts-showcase"] a').length;
    return { cards, badge, pairings, t79TopicsCount };
  });
  recordAssertion(
    'View 2 Renders All 116 Certified Templates (72 Best + 44 High), 23 T79 Topic Variants & 12 Stack Pairings',
    galleryAllCheck.cards === 116 && galleryAllCheck.pairings === 12 && galleryAllCheck.t79TopicsCount === 23,
    `cards=${galleryAllCheck.cards}, badge="${galleryAllCheck.badge}", t79Variants=${galleryAllCheck.t79TopicsCount}, pairings=${galleryAllCheck.pairings}`
  );

  // Test Quality Tier Filter (Best = 72, High = 44)
  await page.select('#gallery-filter-tier', 'Best');
  const bestTierCount = await page.$$eval('#gallery-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Quality Tier Best Renders 72 Certified Best Templates', bestTierCount === 72, `cards=${bestTierCount}`);

  await page.select('#gallery-filter-tier', 'High');
  const highTierCount = await page.$$eval('#gallery-cards-grid .repo-card', (els) => els.length);
  recordAssertion('Filter Quality Tier High Renders 44 Certified High Templates', highTierCount === 44, `cards=${highTierCount}`);
  await page.select('#gallery-filter-tier', 'ALL');

  // Filter to PromptCanvas Infographic (15 unique archetypes T54-T67 + T79 hosting 23 topic variants)
  await page.select('#gallery-filter-type', 'PromptCanvas Infographic');
  const pcFilterCheck = await page.evaluate(async () => {
    const cards = Array.from(document.querySelectorAll('#gallery-cards-grid .repo-card'));
    const ids = cards.map((c) => c.getAttribute('data-testid'));
    const badge = document.getElementById('gallery-count-badge')?.textContent?.trim();
    const imgs = Array.from(document.querySelectorAll('#gallery-cards-grid .repo-card img'));
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 400));
    const broken = imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src);
    return {
      count: cards.length,
      badge,
      firstId: ids[0],
      lastId: ids[ids.length - 1],
      brokenCount: broken.length,
    };
  });
  recordAssertion(
    'Filter PromptCanvas Canonical Infographics Renders 15 Archetypes (T54-T67 + T79 with 23 Topic Variants)',
    pcFilterCheck.count === 15 &&
      pcFilterCheck.firstId === 'template-card-T54' &&
      pcFilterCheck.lastId === 'template-card-T79' &&
      pcFilterCheck.brokenCount === 0,
    `badge="${pcFilterCheck.badge}", range=${pcFilterCheck.firstId}..${pcFilterCheck.lastId}, brokenImgs=${pcFilterCheck.brokenCount}`
  );

  await page.evaluate(() => {
    const el = document.querySelector('[data-testid="template-card-T79"]');
    if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    window.scrollBy(0, -90);
  });
  await new Promise((r) => setTimeout(r, 350));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view2_gallery.png') });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.select('#gallery-filter-type', 'ALL');

  // 4. Test View 3: Creator Mining Intelligence & 16 Creator Profiles + Zero Badge Overflow
  await page.click('#tab-btn-playbook');
  const playbookCheck = await page.evaluate(() => {
    const summaryLen = (document.getElementById('playbook-summary-text')?.textContent || '').trim().length;
    const channels = document.querySelectorAll('#signal-channels-grid .repo-card').length;
    const creatorCards = document.querySelectorAll('#creator-profiles-grid .creator-profile-card').length;
    const archetypes = document.querySelectorAll('#archetypes-grid .repo-card').length;

    const allCards = Array.from(
      document.querySelectorAll('#view-playbook .repo-card, #view-playbook .creator-profile-card')
    );
    let badgeOverflowCount = 0;
    for (const card of allCards) {
      const cRect = card.getBoundingClientRect();
      for (const badge of card.querySelectorAll('.brand-badge, .pill-badge')) {
        const bRect = badge.getBoundingClientRect();
        if (bRect.right > cRect.right + 1.5 || bRect.left < cRect.left - 1.5) {
          badgeOverflowCount++;
        }
      }
    }
    return { summaryLen, channels, creatorCards, archetypes, badgeOverflowCount };
  });
  recordAssertion(
    'View 3 Renders 4 Signal Channels, 16 Creator Profiles, 4 @2d Archetypes & Zero Badge Overflow',
    playbookCheck.summaryLen > 50 &&
      playbookCheck.channels === 4 &&
      playbookCheck.creatorCards === 16 &&
      playbookCheck.archetypes === 4 &&
      playbookCheck.badgeOverflowCount === 0,
    `channels=${playbookCheck.channels}, creators=${playbookCheck.creatorCards}/16, archetypes=${playbookCheck.archetypes}, badgeOverflows=${playbookCheck.badgeOverflowCount}`
  );

  // 5. Test View 4: Daily Top-5 Editorial & Multi-Platform Auto-Publisher + Daily LinkedIn Generator
  await page.click('#tab-btn-miner');
  await page.waitForFunction(
    () =>
      document.querySelectorAll('#top5-ideas-column .top5-idea-card').length === 5 &&
      document.querySelectorAll('[data-testid="top5-template-pills"] button').length === 5 &&
      document.querySelectorAll('[data-testid="top5-mode-pills"] button').length === 8 &&
      document.querySelectorAll('[data-testid="top5-platform-preview-tabs"] button').length === 13 &&
      document.querySelectorAll('#daily-generated-posts-grid .daily-post-card').length >= 3 &&
      document.querySelectorAll('#live-arxiv-list > div').length > 0 &&
      document.querySelectorAll('#live-github-list > div').length > 0,
    { timeout: 15000 }
  );

  // Verify Top-5 Editorial Desk interactive switching (Idea -> Template -> Mode -> Platform -> Stage -> Approve)
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 300));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view4_top5_editorial_desk.png') });

  // Switch Mode to Carousel and inspect Instagram (4:5 JPEGs, zero raw URLs) & TikTok (9:16 JPEGs)
  await page.click('[data-testid="top5-mode-pill-Carousel"]');
  await new Promise((r) => setTimeout(r, 350));
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
    'View 4 Daily Top-5 Editorial Desk: 5 Unique Ideas × 5 Templates × 8 Modes × 13 Platforms (IG 4:5 JPEG Compliance)',
    igCompliance.hasJpeg4x5 &&
      !igCompliance.hasRawUrlInIgCaption &&
      igCompliance.thumbCount >= 9 &&
      igCompliance.loadedImgs === igCompliance.thumbCount,
    `JPEG_4x5=${igCompliance.hasJpeg4x5}, rawUrlsInCaption=${igCompliance.hasRawUrlInIgCaption}, carouselImgs=${igCompliance.loadedImgs}/${igCompliance.thumbCount}`
  );

  // Switch Mode to Short_Video (9:16 Vertical Short MP4) and verify 3-part Length Budget + Video Element
  await page.click('[data-testid="top5-mode-pill-Short_Video"]');
  await new Promise((r) => setTimeout(r, 350));
  await page.click('[data-testid="top5-plat-tab-youtube_shorts"]');
  await new Promise((r) => setTimeout(r, 250));
  const shortVideoCheck = await page.evaluate(() => {
    const budgetCards = document.querySelectorAll('[data-testid="top5-length-budget-strip"] .top5-budget-card').length;
    const budgetText = document.querySelector('[data-testid="top5-length-budget-strip"]')?.innerText || '';
    const vid = document.querySelector('#top5-platform-preview-stage video');
    return {
      budgetCards,
      has916Budget: budgetText.includes('40–55 sec MP4') || budgetText.includes('5 vertical tier-zoom'),
      hasVideoSrc: Boolean(vid && vid.getAttribute('src')?.includes('vertical_short_9x16.mp4')),
    };
  });
  recordAssertion(
    'View 4 Mode Selector Updates 3-Part Content-Length Contract & Mounts 9:16 Safe-Zone Short MP4',
    shortVideoCheck.budgetCards === 3 && shortVideoCheck.has916Budget && shortVideoCheck.hasVideoSrc,
    `budgetCards=${shortVideoCheck.budgetCards}, 9x16Budget=${shortVideoCheck.has916Budget}, videoSrc=${shortVideoCheck.hasVideoSrc}`
  );

  // Switch to Idea #2 & Template #2, Stage Selected Channels, and Approve Pending Outbox
  await page.click('[data-testid="top5-idea-card-2"]');
  await new Promise((r) => setTimeout(r, 350));
  await page.click('[data-testid="top5-tpl-pill-2"]');
  await new Promise((r) => setTimeout(r, 350));
  await page.click('#stage-selected-platforms-btn');
  await new Promise((r) => setTimeout(r, 450));
  await page.click('#approve-all-outbox-btn');
  await new Promise((r) => setTimeout(r, 500));

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
    'View 4 HITL Outbox Stages, Approves & Validates Multi-Platform Queue + Serves Valid RSS 2.0 & Security Headers',
    outboxAndRssCheck.rows >= 5 &&
      outboxAndRssCheck.hasValidatedStatus &&
      outboxAndRssCheck.rssOk &&
      outboxAndRssCheck.nosniff === 'nosniff',
    `outboxRows=${outboxAndRssCheck.rows}, validated=${outboxAndRssCheck.hasValidatedStatus}, rss200=${outboxAndRssCheck.rssOk}, nosniff=${outboxAndRssCheck.nosniff}`
  );

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
    await new Promise((r) => setTimeout(r, 400));
    const loadedSvgs = imgs.filter((i) => i.complete && i.naturalWidth > 0).length;
    const copiedLen = (window.__LAST_COPIED_TEXT__ || '').length;
    const statusText = document.getElementById('daily-posts-status-badge')?.textContent?.trim() || '';
    return { cardCount: cards.length, totalSvgs: imgs.length, loadedSvgs, copiedLen, statusText };
  });
  recordAssertion(
    'View 4 Daily Post Generator Studio Synthesizes 6 Posts, Loads Custom SVGs & Copies Post + Comment #1',
    dailyStudioCheck.cardCount === 6 && dailyStudioCheck.loadedSvgs === 6 && dailyStudioCheck.copiedLen > 200,
    `cards=${dailyStudioCheck.cardCount}, svgs=${dailyStudioCheck.loadedSvgs}/6, copiedChars=${dailyStudioCheck.copiedLen}`
  );

  // 6. Test View 5: OpenHands Autonomous Sandbox Console (19 Repos)
  await page.click('#tab-btn-openhands');
  const ohCheck = await page.evaluate(() => {
    const cmpRows = document.querySelectorAll('#openhands-comparison-tbody tr').length;
    const trajCards = document.querySelectorAll('#openhands-trajectories-list > div').length;
    return { cmpRows, trajCards };
  });
  recordAssertion(
    'View 5 (OpenHands Sandbox Console) Renders Comparison Matrix & 19 Repo Trajectories',
    ohCheck.cmpRows === 5 && ohCheck.trajCards === 19,
    `comparisonRows=${ohCheck.cmpRows}, trajectories=${ohCheck.trajCards}/19`
  );

  // 7. Test View 6: Idea-Minting & Video Studio (MINT-01..12, HTTP 206 Video, 24-Slide Google Slides)
  await page.click('#tab-btn-minting-studio');
  await page.waitForFunction(
    () => document.querySelectorAll('#minting-topics-grid .repo-card').length === 12,
    { timeout: 10000 }
  );

  const mintingStudioCheck = await page.evaluate(async () => {
    const walkVid = document.getElementById('mint01-walkthrough-video');
    const twinVid = document.getElementById('mint01-twin-video');
    if (walkVid && walkVid.readyState < 3) {
      walkVid.load();
    }
    if (twinVid && twinVid.readyState < 3) {
      twinVid.load();
    }
    for (let i = 0; i < 40; i++) {
      if (
        walkVid &&
        walkVid.readyState >= 3 &&
        !walkVid.seeking &&
        twinVid &&
        twinVid.readyState >= 3 &&
        !twinVid.seeking
      ) {
        break;
      }
      await new Promise((r) => setTimeout(r, 150));
    }
    if (walkVid) walkVid.pause();
    if (twinVid) twinVid.pause();
    const topicCards = document.querySelectorAll('#minting-topics-grid .repo-card').length;
    const deckHref = document.getElementById('open-24slide-google-slides-btn')?.getAttribute('href') || '';
    const imgs = Array.from(document.querySelectorAll('#minting-topics-grid .repo-card img'));
    for (const img of imgs) img.loading = 'eager';
    await new Promise((r) => setTimeout(r, 400));
    const brokenImgs = imgs.filter((i) => !i.complete || i.naturalWidth === 0).length;
    return {
      topicCards,
      deckHref,
      walkReadyState: walkVid?.readyState || 0,
      walkWidth: walkVid?.videoWidth || 0,
      walkHeight: walkVid?.videoHeight || 0,
      walkDuration: Math.round(walkVid?.duration || 0),
      twinReadyState: twinVid?.readyState || 0,
      brokenImgs,
    };
  });
  recordAssertion(
    'View 6 (Idea-Minting & Video Studio) Renders 12 MINT Topics, 1080p30 Video & 24-Slide Google Slides Link',
    mintingStudioCheck.topicCards === 12 &&
      mintingStudioCheck.deckHref.includes('1vY7Fji2pmT5LKgK0U2NDEqUBaMyaCJhbpyUyyU7lXYY') &&
      mintingStudioCheck.walkReadyState >= 1 &&
      mintingStudioCheck.walkWidth === 1920 &&
      mintingStudioCheck.walkHeight === 1080 &&
      mintingStudioCheck.twinReadyState >= 1 &&
      mintingStudioCheck.brokenImgs === 0,
    `topics=${mintingStudioCheck.topicCards}/12, video=${mintingStudioCheck.walkWidth}x${mintingStudioCheck.walkHeight} (${mintingStudioCheck.walkDuration}s, readyState=${mintingStudioCheck.walkReadyState}), brokenImgs=${mintingStudioCheck.brokenImgs}`
  );

  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 300));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_view6_minting_studio.png') });

  // 8. Rule 26 Table Cell Containment & Rule 57C Canonical T01 + T53-T89 Zero Double-Footer Check
  const tableContainmentCheck = await page.evaluate(() => {
    const tds = Array.from(document.querySelectorAll('table.table-fixed tbody td'));
    const uncontained = tds.filter((td) => {
      const st = window.getComputedStyle(td);
      return st.overflow !== 'hidden';
    });
    return { totalTds: tds.length, uncontainedCount: uncontained.length };
  });
  recordAssertion(
    'Rule 26 Table Cell Containment (overflow: hidden on all table-fixed tbody td)',
    tableContainmentCheck.totalTds > 0 && tableContainmentCheck.uncontainedCount === 0,
    `checkedCells=${tableContainmentCheck.totalTds}, uncontained=${tableContainmentCheck.uncontainedCount}`
  );

  let doubleFooterCount = 0;
  const canonicalTids = ['T01', ...Array.from({ length: 37 }, (_, idx) => `T${53 + idx}`)];
  for (const tid of canonicalTids) {
    const svgPath = path.resolve(__dirname, `../assets/template-gallery/${tid}.svg`);
    const rawSvg = fs.readFileSync(svgPath, 'utf8');
    const vbMatch = rawSvg.match(/viewBox="0 0 (\d+) (\d+)"/);
    const imgHMatch = rawSvg.match(/<image [^>]*height="(\d+)"/);
    if (
      !vbMatch ||
      !imgHMatch ||
      vbMatch[2] !== imgHMatch[1] ||
      !rawSvg.includes('<title>') ||
      !rawSvg.includes('<desc>')
    ) {
      doubleFooterCount++;
    }
  }
  recordAssertion(
    'Rule 57C Canonical T01 + T53-T89 Zero Double-Footer (viewBox height === image height + W3C <title>/<desc>)',
    doubleFooterCount === 0,
    `verified=38/38 canonical PromptCanvas/Spine templates, doubleFooters=${doubleFooterCount}`
  );

  // 9. Mobile iPhone 390x844 Viewport Overflow Audit Across All 6 Views (Rule 59)
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  let maxMobileOverflow = 0;
  const mobileDetails = [];
  for (const btnId of [
    'tab-btn-repos',
    'tab-btn-gallery',
    'tab-btn-playbook',
    'tab-btn-miner',
    'tab-btn-openhands',
    'tab-btn-minting-studio',
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
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 200));
  await page.screenshot({ path: path.join(PROOF_DIR, 'after_mobile_390x844.png') });
  recordAssertion(
    'Mobile 390x844 Responsive Layout Preserved (docOverflowPx === 0 across Views 1-6)',
    maxMobileOverflow === 0,
    mobileDetails.join(', ')
  );

  // 10. Zero Console Errors & Zero Failed HTTP Requests
  recordAssertion('Zero Browser Page/Runtime Errors', consoleErrors.length === 0, `errors=${consoleErrors.length}`);
  recordAssertion('Zero HTTP >= 400 Responses', failedRequests.length === 0, `failedRequests=${failedRequests.length}`);

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
