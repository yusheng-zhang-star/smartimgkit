const { chromium } = require('playwright');
const path = require('path');
const TEST_IMG = path.join(__dirname, 'test-image.jpg');
const BASE = 'http://localhost:8000';

const tests = [
  // Key tools with ZIP downloads
  ['/tools/watermark.html', TEST_IMG, /\.zip$/, 'Watermark'],
  ['/tools/bulk-processor.html', TEST_IMG, /\.zip$/, 'Bulk processor'],
  ['/tools/background-remover.html', TEST_IMG, /\.zip$/, 'BG remover'],
  ['/tools/favicon-generator.html', TEST_IMG, /\.zip$/, 'Favicon'],
  ['/tools/image-compressor.html', TEST_IMG, /\.zip$/, 'Compressor'],
  ['/tools/converter.html', TEST_IMG, /\.zip$/, 'Converter'],
  ['/tools/pdf-to-image.html', path.join(__dirname, 'test-file.pdf'), /\.zip$/, 'PDF-to-image'],
  // Simple downloads
  ['/tools/qr-code-generator.html', null, /\.(png|svg)$/, 'QR code'],
  ['/tools/signature-maker.html', null, /\.(png|svg)$/, 'Signature'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  let pass = 0, fail = 0;
  for (const [urlPart, testFile, pattern, label] of tests) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    try {
      await page.goto(BASE + urlPart, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      if (testFile) {
        const fi = page.locator('input[type="file"]').first();
        if (await fi.count().then(c => c > 0)) {
          await fi.setInputFiles(testFile);
          await page.waitForTimeout(1500);
        }
      }
      // Try various buttons
      const btn = page.locator(
        'button:has-text("Download"), button:has-text("Process"), ' +
        'button:has-text("Convert"), button:has-text("Split"), ' +
        'button:has-text("Generate"), #downloadBtn, #downloadPngBtn, #processBtn'
      ).first();
      let dl = null;
      if (await btn.count().then(c => c > 0)) {
        try {
          const dlP = page.waitForEvent('download', { timeout: 30000 });
          await btn.click({ timeout: 5000 });
          dl = await dlP;
        } catch(e) {}
      }
      if (dl) {
        const fname = dl.suggestedFilename();
        if (pattern.test(fname)) {
          pass++; console.log(`✅ ${label}: ${fname}`);
        } else {
          fail++; console.log(`❌ ${label}: got "${fname}"`);
        }
      } else {
        fail++; console.log(`❌ ${label}: no download`);
      }
    } catch(e) {
      fail++; console.log(`❌ ${label}: error ${e.message.substring(0,60)}`);
    }
    await ctx.close();
  }
  await browser.close();
  console.log(`\n${pass}/${tests.length} PASS, ${fail} FAIL`);
  process.exit(fail > 0 ? 1 : 0);
})();
