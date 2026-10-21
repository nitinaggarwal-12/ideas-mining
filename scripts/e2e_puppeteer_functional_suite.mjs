import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire('/Users/nitinagga/Documents/PromptCanvas/package.json');
const puppeteer = require('puppeteer');

const BASE_URL = process.env.STUDIO_URL || 'http://127.0.0.1:8765';
const OUT_REPORT = path.resolve(__dirname, '../e2e_puppeteer_report.json');
const ARTIFACT_DIR = '/Users/nitinagga/.gemini/jetski/brain/41ff23f5-fdf4-4ee3-9558-941dc91e7ae3';

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
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new',
  args: ['--no-sandbox', '--disable-gpu', '--window-size=1600,1050'],
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

  // 1. Load Root Studio Workspace (View 1: 18 Repos)
  await page.goto(BASE_URL, { waitUntil: 'networkidle0', timeout: 30000 });

  // Verify Executive Light Theme (Rule 54) & Zero Horizontal Overflow
  const themeAndGeometry = await page.evaluate(() => {
    const bg = window.getComputedStyle(document.body).backgroundColor;
    const hasDarkClass = document.documentElement.classList.contains('dark') || document.body.classList.contains('dark');
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
    'Zero Horizontal Overflow on View 1 (18 Repos)',
    themeAndGeometry.scrollW <= themeAndGeometry.innerW,
    `scrollWidth=${themeAndGeometry.scrollW} <= innerWidth=${themeAndGeometry.innerW}`
  );
  recordAssertion(
    'View 1 Renders All 18 Repo Cards & 18 Matrix Rows',
    themeAndGeometry.repoCards === 18 && themeAndGeometry.matrixRows === 18,
    `cards=${themeAndGeometry.repoCards}, rows=${themeAndGeometry.matrixRows}, badges=${themeAndGeometry.reposBadge} | ${themeAndGeometry.testsBadge}`
  );

  // Verify all 18 repo card lead images load cleanly
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
    'All 18 Repo Card Lead SVGs Load with naturalWidth > 0',
    repoImagesStatus.total === 18 && repoImagesStatus.broken.length === 0,
    `loaded=${repoImagesStatus.total - repoImagesStatus.broken.length}/18`
  );

  // Test Series Filter (#filter-archetype)
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
  recordAssertion('Reset Filters Button Restores All 18 Repos', restoredCount === 18, `cards=${restoredCount}`);

  // 2. Test Right-Side Inspector Drawer & All 4 Drawer Tabs
  await page.click('[data-testid="repo-card-IDEA-01"] .btn-primary');
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
    'Inspector Drawer Tab 1 (Dynamic & @2d Visuals) Renders All Figures & Prompt',
    drawerTab1.badge.includes('IDEA-01') && drawerTab1.totalImgs >= 4 && drawerTab1.loadedImgs === drawerTab1.totalImgs && drawerTab1.nb3Len > 100,
    `badge="${drawerTab1.badge}", images=${drawerTab1.loadedImgs}/${drawerTab1.totalImgs}, promptChars=${drawerTab1.nb3Len}`
  );

  await page.click('#dtab-btn-slides');
  const slidesCount = await page.evaluate(() => {
    const text = document.getElementById('dtab-slides')?.innerText || '';
    const matches = text.match(/SLIDE \d+ OF 12/g) || [];
    return matches.length;
  });
  recordAssertion('Inspector Drawer Tab 2 (12-Slide Deck & Carousel) Renders 12 Slides', slidesCount === 12, `slides=${slidesCount}/12`);

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

  // 3. Test View 2: 68 Dynamic Visual Template Gallery (T01-T68)
  await page.click('#tab-btn-gallery');
  await page.waitForFunction(
    () => document.querySelectorAll('#gallery-cards-grid .repo-card').length === 68,
    { timeout: 10000 }
  );

  const galleryAllCheck = await page.evaluate(async () => {
    const cards = document.querySelectorAll('#gallery-cards-grid .repo-card').length;
    const badge = document.getElementById('gallery-count-badge')?.textContent?.trim();
    const pairings = document.querySelectorAll('#pairings-tbody tr').length;
    const imgs = Array.from(document.querySelectorAll('#gallery-cards-grid .repo-card img'));
    for (const img of imgs) {
      img.loading = 'eager';
    }
    await new Promise((r) => setTimeout(r, 600));
    const broken = imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src);
    return { cards, badge, pairings, totalImgs: imgs.length, broken };
  });
  recordAssertion(
    'View 2 Renders All 68 Dynamic Templates & 12 OSS/Google Stack Pairings',
    galleryAllCheck.cards === 68 && galleryAllCheck.pairings === 12 && galleryAllCheck.broken.length === 0,
    `cards=${galleryAllCheck.cards}, badge="${galleryAllCheck.badge}", pairings=${galleryAllCheck.pairings}, brokenImgs=${galleryAllCheck.broken.length}`
  );

  // Filter to PromptCanvas Infographic (T53-T68)
  await page.select('#gallery-filter-type', 'PromptCanvas Infographic');
  const pcFilterCheck = await page.evaluate(async () => {
    const cards = Array.from(document.querySelectorAll('#gallery-cards-grid .repo-card'));
    const ids = cards.map((c) => c.getAttribute('data-testid'));
    const badge = document.getElementById('gallery-count-badge')?.textContent?.trim();
    const imgs = Array.from(document.querySelectorAll('#gallery-cards-grid .repo-card img'));
    const dims = imgs.map((i) => ({ alt: i.alt, w: i.naturalWidth, h: i.naturalHeight }));
    return { count: cards.length, badge, firstId: ids[0], lastId: ids[ids.length - 1], dims };
  });
  recordAssertion(
    'Filter PromptCanvas Canonical Infographics Renders Exactly 16 Templates (T53-T68)',
    pcFilterCheck.count === 16 && pcFilterCheck.firstId === 'template-card-T53' && pcFilterCheck.lastId === 'template-card-T68',
    `badge="${pcFilterCheck.badge}", range=${pcFilterCheck.firstId}..${pcFilterCheck.lastId}`
  );

  if (fs.existsSync(ARTIFACT_DIR)) {
    await page.screenshot({ path: path.join(ARTIFACT_DIR, 'after_t53_t68_gallery.png') });
  }
  await page.select('#gallery-filter-type', 'ALL');

  // 4. Test View 3: Creator Mining Intelligence & Playbook
  await page.click('#tab-btn-playbook');
  const playbookCheck = await page.evaluate(() => {
    const summaryLen = (document.getElementById('playbook-summary-text')?.textContent || '').trim().length;
    const channels = document.querySelectorAll('#signal-channels-grid .repo-card').length;
    const archetypes = document.querySelectorAll('#archetypes-grid .repo-card').length;
    return { summaryLen, channels, archetypes };
  });
  recordAssertion(
    'View 3 (Creator Mining Playbook) Renders Signal Channels & 4 @2d Archetypes',
    playbookCheck.summaryLen > 50 && playbookCheck.channels >= 4 && playbookCheck.archetypes === 4,
    `summaryChars=${playbookCheck.summaryLen}, channels=${playbookCheck.channels}, archetypes=${playbookCheck.archetypes}`
  );

  // 5. Test View 4: Live Idea Miner & URL Ingestor
  await page.click('#tab-btn-miner');
  await page.waitForFunction(
    () => document.querySelectorAll('#live-arxiv-list > div').length > 0 && document.querySelectorAll('#live-github-list > div').length > 0,
    { timeout: 10000 }
  );
  await page.type('#inline-ingest-url-input', 'https://arxiv.org/abs/2503.09516');
  await page.type('#inline-ingest-title-input', 'Autonomous Agentic Verification');
  await page.click('#trigger-ingest-btn');
  await page.waitForFunction(
    () => {
      const b = document.getElementById('ingest-result-banner');
      return b && window.getComputedStyle(b).display !== 'none' && b.textContent.includes('Verified & Mapped:');
    },
    { timeout: 8000 }
  );
  const ingestBannerText = await page.$eval('#ingest-result-banner', (el) => el.textContent.trim());
  recordAssertion(
    'View 4 (Live Idea Miner & URL Ingestor) Feeds + POST /api/ingest-url E2E',
    ingestBannerText.includes('Verified & Mapped:'),
    ingestBannerText
  );

  // 6. Test View 5: OpenHands Autonomous Sandbox Console
  await page.click('#tab-btn-openhands');
  const ohCheck = await page.evaluate(() => {
    const cmpRows = document.querySelectorAll('#openhands-comparison-tbody tr').length;
    const trajCards = document.querySelectorAll('#openhands-trajectories-list > div').length;
    return { cmpRows, trajCards };
  });
  recordAssertion(
    'View 5 (OpenHands Sandbox Console) Renders Comparison Matrix & 18 Repo Trajectories',
    ohCheck.cmpRows === 5 && ohCheck.trajCards === 18,
    `comparisonRows=${ohCheck.cmpRows}, trajectories=${ohCheck.trajCards}/18`
  );

  // 7. Rule 26 Table Cell Containment & Rule 57C Canonical T53-T68 Zero Double-Footer Check
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

  // Check T53..T68 SVG viewBox == image height (zero 46px double-footer bar)
  let doubleFooterCount = 0;
  for (let i = 53; i <= 68; i++) {
    const tid = `T${i}`;
    const svgPath = path.resolve(__dirname, `../assets/template-gallery/${tid}.svg`);
    const rawSvg = fs.readFileSync(svgPath, 'utf8');
    const vbMatch = rawSvg.match(/viewBox="0 0 (\d+) (\d+)"/);
    const imgHMatch = rawSvg.match(/<image [^>]*height="(\d+)"/);
    if (!vbMatch || !imgHMatch || vbMatch[2] !== imgHMatch[1] || !rawSvg.includes('<title>') || !rawSvg.includes('<desc>')) {
      doubleFooterCount++;
    }
  }
  recordAssertion(
    'Rule 57C Canonical T53-T68 Zero Double-Footer (viewBox height === image height + W3C <title>/<desc>)',
    doubleFooterCount === 0,
    `verified=16/16 canonical PromptCanvas templates, doubleFooters=${doubleFooterCount}`
  );

  // 8. Zero Console Errors & Zero Failed HTTP Requests
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
