import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire('/Users/nitinagga/Documents/PromptCanvas/package.json');
const puppeteer = require('puppeteer');

const IDEAS_ROOT = path.resolve(__dirname, '..');
const PC_PUBLIC = '/Users/nitinagga/Documents/PromptCanvas/public';
const DRAWIO_DIR = path.join(IDEAS_ROOT, 'assets/canonical-ref/drawio');
const REF_DIR = path.join(IDEAS_ROOT, 'assets/canonical-ref');
const GALLERY_DIR = path.join(IDEAS_ROOT, 'assets/template-gallery');

fs.mkdirSync(DRAWIO_DIR, { recursive: true });
fs.mkdirSync(REF_DIR, { recursive: true });
fs.mkdirSync(GALLERY_DIR, { recursive: true });

const PC_TIDS = new Set(['T53','T54','T55','T56','T57','T58','T59','T60','T61','T62','T63','T64','T65','T66','T67','T68']);
const filterTids = process.argv.slice(2).filter((a) => a.startsWith('T'));
if (filterTids.length === 0 || filterTids.some((t) => PC_TIDS.has(t))) {
  // Step 1: Export healed Draw.io XMLs from PromptCanvas canonical TypeScript
  execSync(`npx tsx ${path.join(__dirname, 'export_pc_xmls.ts')}`, {
    cwd: '/Users/nitinagga/Documents/PromptCanvas',
    stdio: 'inherit',
  });
}

const MAPPING = [
  { tid: 'T01', pcId: 't01_loop_guard' },
  { tid: 'T53', pcId: '52' },
  { tid: 'T54', pcId: '53' },
  { tid: 'T55', pcId: '54' },
  { tid: 'T56', pcId: '55' },
  { tid: 'T57', pcId: '56' },
  { tid: 'T58', pcId: '57' },
  { tid: 'T59', pcId: '58' },
  { tid: 'T60', pcId: '59' },
  { tid: 'T61', pcId: '60' },
  { tid: 'T62', pcId: '61' },
  { tid: 'T63', pcId: '62' },
  { tid: 'T64', pcId: '63' },
  { tid: 'T65', pcId: '64' },
  { tid: 'T66', pcId: '65' },
  { tid: 'T67', pcId: '66' },
  { tid: 'T68', pcId: 'open_knowledge' },
  { tid: 'T69', pcId: 'harness_squared' },
  { tid: 'T70', pcId: 'five_agent_repos' },
  { tid: 'T71', pcId: 'data_modeling_3x3' },
  { tid: 'T72', pcId: 'token_economizer' },
  { tid: 'T73', pcId: 'agentcore_11zone' },
  { tid: 'T74', pcId: 'agent_sandbox_6vendor' },
  { tid: 'T75', pcId: 'agent_5_blocks' },
  { tid: 'T76', pcId: 'gcp_12_ai_concepts' },
  { tid: 'T77', pcId: 'pharma_rd_2026' },
  { tid: 'T78', pcId: 'agentic_coding_6stage' },
  { tid: 'T79', pcId: 'cdm_schema_gate' },
  { tid: 'T80', pcId: 'jev_9_decisions' },
  { tid: 'T81', pcId: 'learn_harness_8phase' },
  { tid: 'T82', pcId: 'code_review_replay_eval' },
  { tid: 'T83', pcId: 'agent_evals_pass_k' },
  { tid: 'T84', pcId: 'inference_eng_goodput' },
];

const viewerJs = fs.readFileSync(path.join(PC_PUBLIC, 'viewer-static.min.js'), 'utf8');

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new',
  userDataDir: '/Users/nitinagga/.gemini/chrome_profile_ideas_e2e_sync',
  args: ['--no-sandbox', '--disable-gpu', '--disable-extensions', '--no-first-run', '--font-render-hinting=none'],
});

const dimJsonPath = path.join(REF_DIR, 'canonical_dimensions.json');
const dimensionsMap = fs.existsSync(dimJsonPath) ? JSON.parse(fs.readFileSync(dimJsonPath, 'utf8')) : {};
const activeMapping = filterTids.length > 0 ? MAPPING.filter((m) => filterTids.includes(m.tid)) : MAPPING;

try {
  for (const { tid, pcId } of activeMapping) {
    const page = await browser.newPage();
    const xml = fs.readFileSync(path.join(DRAWIO_DIR, `${tid}.drawio`), 'utf8');
    const wMatch = xml.match(/pageWidth="(\d+)"/);
    const hMatch = xml.match(/pageHeight="(\d+)"/);
    const bgMatch = xml.match(/background="(#[0-9A-Fa-f]{6})"/);
    const pw = wMatch ? parseInt(wMatch[1], 10) : 1075;
    const ph = hMatch ? parseInt(hMatch[1], 10) : 1290;
    const bg = bgMatch ? bgMatch[1] : '#F8FAFC';

    const cfg = JSON.stringify({
      xml,
      lightbox: false,
      nav: false,
      resize: false,
      toolbar: null,
      'toolbar-position': 'none',
      border: 0,
    });

    const html = `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:${bg};font-family:Inter,-apple-system,BlinkMacSystemFont,sans-serif;} #diagram-container{width:${pw}px;height:${ph}px;}</style></head><body><div class="mxgraph" id="diagram-container"></div><script>${viewerJs}</script><script>
      const root = document.getElementById("diagram-container");
      root.setAttribute("data-mxgraph", ${JSON.stringify(cfg)});
      window.GraphViewer.processElements();
    </script></body></html>`;

    await page.setViewport({ width: pw, height: ph, deviceScaleFactor: 2 });
    await page.setContent(html, { waitUntil: 'domcontentloaded' });
    await new Promise((r) => setTimeout(r, 380));

    const canonicalTidPngPath = path.join(REF_DIR, `canonical_${tid}.png`);
    const galleryPngPath = path.join(GALLERY_DIR, `${tid}.png`);
    const galleryDrawioPath = path.join(GALLERY_DIR, `${tid}.drawio`);

    await page.screenshot({ path: canonicalTidPngPath });
    fs.copyFileSync(canonicalTidPngPath, galleryPngPath);
    fs.copyFileSync(path.join(DRAWIO_DIR, `${tid}.drawio`), galleryDrawioPath);
    if (/^\d+$/.test(pcId)) {
      const pcTemplatePng = path.join(PC_PUBLIC, 'templates', `${pcId}.png`);
      if (fs.existsSync(path.dirname(pcTemplatePng))) {
        fs.copyFileSync(canonicalTidPngPath, pcTemplatePng);
      }
    }

    dimensionsMap[tid] = { pcId, width: pw, height: ph, background: bg };
    console.log(`[sync_canonical] ${tid} (#${pcId}): ${pw}x${ph}px (2x retina PNG=${fs.statSync(canonicalTidPngPath).size} bytes)`);
    await page.close();
  }

  fs.writeFileSync(path.join(REF_DIR, 'canonical_dimensions.json'), JSON.stringify(dimensionsMap, null, 2));
} finally {
  await browser.close();
}
