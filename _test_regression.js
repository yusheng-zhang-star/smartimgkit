/**
 * Quick regression test for fixed pages
 */
const { chromium } = require('playwright');
const path = require('path');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

const PAGES = [
  { slug: 'face-blur', type: 'tool', needsFile: true },
  { slug: 'watermark', type: 'tool', needsFile: true },
  { slug: 'gif-editor', type: 'tool', needsFile: true },
  { slug: 'image-compressor', type: 'tool', needsFile: true },
  { slug: 'heic-to-jpg', type: 'tool', needsFile: false },
  { slug: 'heic-converter', type: 'tool', needsFile: false, expectRedirect: true },
  { slug: 'resume-cv-photo', type: 'workflow', needsFile: true },
  { slug: 'app-store-screenshot-suite', type: 'workflow', needsFile: true },
];

(async () => {
  console.log('='.repeat(60));
  console.log('Regression Test for Fixed Pages');
  console.log('='.repeat(60));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();

  const results = [];

  for (const p of PAGES) {
    const url = p.type === 'tool'
      ? `${BASE_URL}/tools/${p.slug}.html`
      : `${BASE_URL}/workflows/${p.slug}.html`;

    console.log(`\n🔍 Testing: ${p.type}/${p.slug}`);

    const errors = [];
    const logs = [];

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(`[CONSOLE] ${msg.text()}`);
    });
    page.on('pageerror', err => {
      errors.push(`[PAGEERROR] ${err.message}`);
    });
    page.on('dialog', async dialog => {
      errors.push(`[DIALOG] ${dialog.type()}: ${dialog.message()}`);
      await dialog.accept().catch(() => {});
    });

    let loadOK = false;
    let redirected = false;

    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      loadOK = true;
      await page.waitForTimeout(1500);

      const finalUrl = page.url();
      if (p.expectRedirect && finalUrl !== url) {
        redirected = true;
        console.log(`   ✅ Redirected to: ${finalUrl}`);
      }

      if (p.needsFile && !redirected) {
        const fileInput = page.locator('input[type="file"]').first();
        if (await fileInput.count().then(c => c > 0)) {
          await fileInput.setInputFiles(TEST_IMAGE);
          await page.waitForTimeout(1000);
        }

        // Try to find and click main button
        const btnSelectors = [
          '#runBtn', '#compressBtn', '#convertBtn', '#applyBtn', '#processBtn',
          'button:has-text("Run")', 'button:has-text("Compress")', 'button:has-text("Convert")',
          'button:has-text("Apply")', 'button.btn-primary',
        ];
        for (const sel of btnSelectors) {
          const btn = page.locator(sel).first();
          if (await btn.count().then(c => c > 0)) {
            const isDisabled = await btn.isDisabled().catch(() => true);
            if (!isDisabled) {
              try {
                await Promise.race([
                  btn.click({ timeout: 5000 }),
                  new Promise(r => setTimeout(r, 5000)),
                ]);
                await page.waitForTimeout(3000);
              } catch (e) {}
              break;
            }
          }
        }
      }

    } catch (e) {
      errors.push(`[FATAL] ${e.message}`);
    }

    const status = errors.length === 0 ? '✅' : '❌';
    console.log(`   ${status} Errors: ${errors.length}`);
    if (errors.length) {
      errors.forEach(e => console.log(`      ❌ ${e.substring(0, 150)}`));
    }

    results.push({ ...p, errors, loadOK, redirected });
  }

  await browser.close();

  console.log('\n' + '='.repeat(60));
  console.log('REGRESSION TEST SUMMARY');
  console.log('='.repeat(60));
  const passed = results.filter(r => r.errors.length === 0).length;
  console.log(`Passed: ${passed}/${results.length}`);
  results.forEach(r => {
    const icon = r.errors.length === 0 ? '✅' : '❌';
    console.log(`${icon} ${r.type}/${r.slug} (${r.errors.length} errors)`);
  });
  process.exit(results.some(r => r.errors.length > 0) ? 1 : 0);
})();
