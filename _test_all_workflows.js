/**
 * Test ALL workflows for JSZip and actual pipeline execution
 */
const { chromium } = require('playwright');
const path = require('path');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

const ALL_WORKFLOWS = [
  'avatar-pipeline',
  'e-commerce-pack',
  'social-media-kit',
  'product-image-optimizer',
  'batch-watermark-protect',
  'listing-image-suite',
  'ai-background-studio',
  'blog-image-pack',
  'youtube-thumbnail-suite',
  'real-estate-photo-pack',
  'food-photography-bundle',
  'podcast-cover-suite',
  'email-signature-pack',
  'freelancer-portfolio-pack',
  'event-photography-bundle',
  'print-ready-prep',
  'app-store-screenshot-suite',
  'course-tutorial-pack',
  'resume-cv-photo',
];

(async () => {
  console.log('='.repeat(70));
  console.log('ALL WORKFLOWS JSZip + Pipeline Test');
  console.log('='.repeat(70));

  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const slug of ALL_WORKFLOWS) {
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const url = `${BASE_URL}/workflows/${slug}.html`;

    const errors = [];
    const logs = [];
    let jszipOK = false;
    let pipelineOK = false;

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(`[CONSOLE] ${msg.text()}`);
      logs.push(`[${msg.type()}] ${msg.text()}`);
    });
    page.on('pageerror', err => errors.push(`[PAGEERROR] ${err.message}`));
    page.on('dialog', async dialog => {
      errors.push(`[DIALOG] ${dialog.type()}: ${dialog.message()}`);
      await dialog.accept().catch(() => {});
    });

    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(1500);

      // Check if JSZip is defined
      jszipOK = await page.evaluate(() => typeof JSZip !== 'undefined').catch(() => false);

      // Upload test image
      const fileInput = page.locator('input[type="file"]').first();
      if (await fileInput.count().then(c => c > 0)) {
        await fileInput.setInputFiles(TEST_IMAGE);
        await page.waitForTimeout(1000);
      }

      // Check Run button
      const runBtn = page.locator('#runBtn');
      if (await runBtn.count().then(c => c > 0)) {
        const isDisabled = await runBtn.isDisabled().catch(() => true);
        if (!isDisabled) {
          const downloadPromise = page.waitForEvent('download', { timeout: 60000 }).catch(() => null);
          await runBtn.click();

          // Wait for processing
          const timeout = 60000;
          const start = Date.now();
          while (Date.now() - start < timeout && errors.length === 0) {
            await page.waitForTimeout(1000);
            const btnDisabled = await runBtn.isDisabled().catch(() => false);
            if (!btnDisabled) break;
          }

          pipelineOK = errors.length === 0;
          const download = await downloadPromise;
          if (download) pipelineOK = true;
        }
      }

    } catch (e) {
      errors.push(`[FATAL] ${e.message}`);
    }

    const status = errors.length === 0 ? '✅' : '❌';
    console.log(`${status} ${slug} | JSZip: ${jszipOK ? '✅' : '❌'} | Pipeline: ${pipelineOK ? '✅' : '❌'} | Errors: ${errors.length}`);
    if (errors.length) {
      errors.forEach(e => console.log(`      ❌ ${e.substring(0, 180)}`));
    }

    results.push({ slug, jszipOK, pipelineOK, errors });
    await context.close();
  }

  await browser.close();

  console.log('\n' + '='.repeat(70));
  console.log('FINAL SUMMARY');
  console.log('='.repeat(70));
  const allOK = results.filter(r => r.errors.length === 0).length;
  const jszipFail = results.filter(r => !r.jszipOK).map(r => r.slug);
  console.log(`Total: ${results.length} | OK: ${allOK} | Fail: ${results.length - allOK}`);
  if (jszipFail.length) console.log(`JSZip missing: ${jszipFail.join(', ')}`);
  process.exit(allOK === results.length ? 0 : 1);
})();
