/**
 * Test ALL downloadable features for correct filenames.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMG = path.join(__dirname, 'test-image.jpg');
const TEST_PDF = path.join(__dirname, 'test-file.pdf');
const BASE = 'http://localhost:8000';

// Test cases: [url, testFile, expectedFilenamePattern, action]
const tests = [
  // Workflows
  ['/workflows/e-commerce-pack.html', TEST_IMG, /product-images\.zip/, 'runPipeline'],
  ['/workflows/social-media-kit.html', TEST_IMG, /social-media-kit\.zip/, 'runPipeline'],
  ['/workflows/batch-watermark-protect.html', TEST_IMG, /watermarked\.zip/, 'runPipeline'],
  ['/workflows/listing-image-suite.html', TEST_IMG, /listing-images\.zip/, 'runPipeline'],
  ['/workflows/product-image-optimizer.html', TEST_IMG, /product-optimized\.zip/, 'runPipeline'],
  ['/workflows/blog-image-pack.html', TEST_IMG, /blog-image-pack-output\.zip/, 'runPipeline'],
  ['/workflows/avatar-pipeline.html', TEST_IMG, /avatars-.*\.zip/, 'runPipeline'],
  ['/workflows/ai-background-studio.html', TEST_IMG, /bg-studio-.*\.zip/, 'runPipeline'],
  ['/workflows/app-store-screenshot-suite.html', TEST_IMG, /app-store-screenshots\.zip/, 'runPipeline'],
  ['/workflows/resume-cv-photo.html', TEST_IMG, /cv-photos\.zip/, 'runPipeline'],
  ['/workflows/email-signature-pack.html', TEST_IMG, /email-signatures\.zip/, 'runPipeline'],
  ['/workflows/print-ready-prep.html', TEST_IMG, /print-ready-images\.zip/, 'runPipeline'],
  ['/workflows/podcast-cover-suite.html', TEST_IMG, /podcast-covers\.zip/, 'runPipeline'],
  ['/workflows/youtube-thumbnail-suite.html', TEST_IMG, /youtube-thumbnails\.zip/, 'runPipeline'],
  ['/workflows/freelancer-portfolio-pack.html', TEST_IMG, /portfolio-images\.zip/, 'runPipeline'],
  ['/workflows/course-tutorial-pack.html', TEST_IMG, /course-images\.zip/, 'runPipeline'],
  ['/workflows/event-photography-bundle.html', TEST_IMG, /event-photos\.zip/, 'runPipeline'],
  ['/workflows/food-photography-bundle.html', TEST_IMG, /food-photos\.zip/, 'runPipeline'],
  ['/workflows/real-estate-photo-pack.html', TEST_IMG, /real-estate-photos\.zip/, 'runPipeline'],
  // Tools with ZIP downloads
  ['/tools/watermark.html', TEST_IMG, /watermarked-images\.zip/, 'process'],
  ['/tools/bulk-processor.html', TEST_IMG, /processed-images\.zip/, 'process'],
  ['/tools/converter.html', TEST_IMG, /converted-images\.zip/, 'process'],
  ['/tools/background-remover.html', TEST_IMG, /no-background-images\.zip/, 'process'],
  ['/tools/favicon-generator.html', TEST_IMG, /favicons\.zip/, 'process'],
  ['/tools/heic-to-jpg.html', TEST_IMG, /converted-images\.zip/, 'process'],
  ['/tools/image-compressor.html', TEST_IMG, /compressed-images\.zip/, 'process'],
  ['/tools/gif-splitter.html', TEST_IMG, /-frames\.zip/, 'process'],
  ['/tools/product-white-background.html', TEST_IMG, /product-white-background-images\.zip/, 'process'],
  ['/tools/image-splitter.html', TEST_IMG, /_split\.zip/, 'process'],
  ['/tools/pdf-to-image.html', TEST_PDF, /pdf-pages\.zip/, 'process'],
  // Tools with simple downloads
  ['/tools/qr-code-generator.html', null, /qrcode\.(png|svg)/, 'downloadQR'],
];

(async () => {
  console.log(`Testing ${tests.length} download features...\n`);
  const browser = await chromium.launch({ headless: true });
  let pass = 0, fail = 0;
  const failures = [];

  for (const [urlPart, testFile, expectedPattern, action] of tests) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const name = urlPart.split('/').pop().replace('.html', '');

    try {
      await page.goto(BASE + urlPart, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);

      // Upload if needed
      if (testFile) {
        const fi = page.locator('input[type="file"]').first();
        if (await fi.count().then(c => c > 0)) {
          await fi.setInputFiles(testFile);
          await page.waitForTimeout(1000);
        }
      }

      let dl;
      if (action === 'runPipeline') {
        const btn = page.locator('#runBtn').first();
        if (await btn.count().then(c => c > 0) && !await btn.isDisabled().catch(() => true)) {
          const dlP = page.waitForEvent('download', { timeout: 60000 });
          await btn.click({ timeout: 5000 });
          dl = await dlP;
        }
      } else if (action === 'downloadQR') {
        const btn = page.locator('#downloadPngBtn, #downloadSvgBtn').first();
        if (await btn.count().then(c => c > 0)) {
          const dlP = page.waitForEvent('download', { timeout: 30000 });
          await btn.click({ timeout: 5000 });
          dl = await dlP;
        }
      } else if (action === 'process') {
        // Try to find a download/process button
        const btn = page.locator('#downloadBtn, button:has-text("Download"), button:has-text("Process"), button:has-text("Convert"), button:has-text("Split")').first();
        if (await btn.count().then(c => c > 0)) {
          try {
            const dlP = page.waitForEvent('download', { timeout: 30000 });
            await btn.click({ timeout: 5000 });
            dl = await dlP;
          } catch(e) {}
        }
      }

      if (dl) {
        const fname = dl.suggestedFilename();
        const match = expectedPattern.test(fname);
        if (match) {
          pass++;
          console.log(`✅ ${name} → ${fname}`);
        } else {
          fail++;
          failures.push({ name, got: fname, expected: expectedPattern });
          console.log(`❌ ${name} → got "${fname}", expected pattern "${expectedPattern}"`);
        }
      } else {
        fail++;
        failures.push({ name, got: 'NO DOWNLOAD', expected: expectedPattern });
        console.log(`❌ ${name} → no download triggered`);
      }
    } catch(e) {
      fail++;
      failures.push({ name, got: 'ERROR: ' + e.message.substring(0, 80) });
      console.log(`❌ ${name} → error: ${e.message.substring(0, 80)}`);
    }
    await ctx.close();
  }

  await browser.close();
  console.log(`\n${'='.repeat(60)}`);
  console.log(`RESULT: ${pass}/${tests.length} PASS, ${fail} FAIL`);
  if (failures.length) {
    console.log('\nFailures:');
    failures.forEach(f => console.log(`  ❌ ${f.name}: ${f.got}`));
  }
  process.exit(fail > 0 ? 1 : 0);
})();
