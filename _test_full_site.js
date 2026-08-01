/**
 * Full site E2E test: all tools + workflows
 * Smart, auto-detects page type and runs appropriate tests
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

// List all tool pages (from tools/ directory)
const TOOLS_DIR = path.join(__dirname, 'tools');
const ALL_TOOLS = fs.readdirSync(TOOLS_DIR)
  .filter(f => f.endsWith('.html') && !f.startsWith('_'))
  .map(f => f.replace('.html', ''));

const ALL_WORKFLOWS = [
  'avatar-pipeline', 'e-commerce-pack', 'social-media-kit',
  'product-image-optimizer', 'batch-watermark-protect', 'listing-image-suite',
  'ai-background-studio', 'blog-image-pack', 'youtube-thumbnail-suite',
  'real-estate-photo-pack', 'food-photography-bundle', 'podcast-cover-suite',
  'email-signature-pack', 'freelancer-portfolio-pack', 'event-photography-bundle',
  'print-ready-prep', 'app-store-screenshot-suite', 'course-tutorial-pack',
  'resume-cv-photo',
];

console.log(`Testing ${ALL_TOOLS.length} tools + ${ALL_WORKFLOWS.length} workflows = ${ALL_TOOLS.length + ALL_WORKFLOWS.length} pages`);
console.log(`Test image: ${TEST_IMAGE} (exists: ${fs.existsSync(TEST_IMAGE)})`);

async function testPage(page, type, slug) {
  const url = type === 'tool' 
    ? `${BASE_URL}/tools/${slug}.html`
    : `${BASE_URL}/workflows/${slug}.html`;

  const errors = [];
  const logs = [];

  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(`[CONSOLE] ${msg.text()}`);
    logs.push(`[${msg.type()}] ${msg.text()}`);
  });

  page.on('pageerror', err => {
    errors.push(`[PAGEERROR] ${err.message}`);
  });

  page.on('dialog', async dialog => {
    errors.push(`[DIALOG] ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept().catch(() => {});
  });

  const result = {
    type, slug, url,
    loadOK: false,
    hasFileInput: false,
    hasProcessButton: false,
    ranProcess: false,
    processOK: false,
    errors: [],
  };

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    result.loadOK = true;
    await page.waitForTimeout(1500);

    // Check for file input
    const fileInput = page.locator('input[type="file"]').first();
    const hasFileInput = await fileInput.count().then(c => c > 0).catch(() => false);
    result.hasFileInput = hasFileInput;

    // Look for a main action button
    const processBtnSelectors = [
      '#runBtn', '#processBtn', '#convertBtn', '#compressBtn',
      'button:has-text("Run")', 'button:has-text("Process")',
      'button:has-text("Convert")', 'button:has-text("Compress")',
      'button:has-text("Generate")', 'button:has-text("Upload")',
      'button.btn-primary',
    ];

    let processBtn = null;
    for (const sel of processBtnSelectors) {
      const btn = page.locator(sel).first();
      if (await btn.count().then(c => c > 0).catch(() => false)) {
        processBtn = btn;
        break;
      }
    }
    result.hasProcessButton = !!processBtn;

    // If there's a file input, upload the test image
    if (hasFileInput) {
      try {
        await fileInput.setInputFiles(TEST_IMAGE);
        await page.waitForTimeout(1000);
      } catch (e) {
        errors.push(`[UPLOAD] ${e.message}`);
      }
    }

    // If there's a process button and it's not disabled, click it
    if (processBtn) {
      try {
        const isDisabled = await processBtn.isDisabled().catch(() => true);
        if (!isDisabled) {
          result.ranProcess = true;
          await Promise.race([
            processBtn.click({ timeout: 5000 }),
            new Promise(r => setTimeout(r, 5000)),
          ]);
          await page.waitForTimeout(3000);
          result.processOK = true;
        }
      } catch (e) {
        errors.push(`[PROCESS] ${e.message}`);
      }
    }

    result.errors = errors;
    return result;

  } catch (e) {
    result.errors = [...errors, `[FATAL] ${e.message}`];
    return result;
  }
}

(async () => {
  console.log('='.repeat(70));
  console.log('SmartImgKit FULL SITE E2E Test');
  console.log('='.repeat(70));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();

  const results = [];

  // Test all tools
  console.log(`\n📦 Testing ${ALL_TOOLS.length} tools...`);
  for (let i = 0; i < ALL_TOOLS.length; i++) {
    const slug = ALL_TOOLS[i];
    const r = await testPage(page, 'tool', slug);
    results.push(r);
    const icon = r.errors.length === 0 ? '✅' : '❌';
    const extra = [];
    if (r.hasFileInput) extra.push('file-input');
    if (r.hasProcessButton) extra.push('process-btn');
    if (r.ranProcess) extra.push('executed');
    console.log(`  ${String(i+1).padStart(2)}. ${icon} ${slug} [${extra.join(', ')}]`);
    if (r.errors.length) {
      r.errors.forEach(e => console.log(`        ❌ ${e.substring(0, 120)}`));
    }
  }

  // Test all workflows
  console.log(`\n🔄 Testing ${ALL_WORKFLOWS.length} workflows...`);
  for (let i = 0; i < ALL_WORKFLOWS.length; i++) {
    const slug = ALL_WORKFLOWS[i];
    const r = await testPage(page, 'workflow', slug);
    results.push(r);
    const icon = r.errors.length === 0 ? '✅' : '❌';
    console.log(`  ${String(i+1).padStart(2)}. ${icon} ${slug}`);
    if (r.errors.length) {
      r.errors.forEach(e => console.log(`        ❌ ${e.substring(0, 120)}`));
    }
  }

  await browser.close();

  // Summary
  console.log('\n' + '='.repeat(70));
  console.log('TEST SUMMARY');
  console.log('='.repeat(70));

  const total = results.length;
  const loadOK = results.filter(r => r.loadOK).length;
  const withErrors = results.filter(r => r.errors.length > 0);
  const noErrors = results.filter(r => r.errors.length === 0);
  const withFileInput = results.filter(r => r.hasFileInput).length;
  const withProcessBtn = results.filter(r => r.hasProcessButton).length;
  const executed = results.filter(r => r.ranProcess).length;

  console.log(`Total pages:     ${total}`);
  console.log(`Loaded OK:       ${loadOK}/${total}`);
  console.log(`With file input: ${withFileInput}`);
  console.log(`With process btn: ${withProcessBtn}`);
  console.log(`Executed:        ${executed}`);
  console.log(`No errors:       ${noErrors.length} ✅`);
  console.log(`With errors:     ${withErrors.length} ❌`);

  if (withErrors.length) {
    console.log('\n❌ Pages with errors:');
    withErrors.forEach(r => {
      console.log(`  ${r.type}/${r.slug}:`);
      r.errors.forEach(e => console.log(`    - ${e.substring(0, 150)}`));
    });
  }

  process.exit(withErrors.length > 0 ? 1 : 0);
})();
