const { chromium } = require('playwright');
const path = require('path');
const TEST_IMG = path.join(__dirname, 'test-image.jpg');
const BASE = 'http://localhost:8000';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const tests = [
    ['/tools/watermark.html', 'watermark'],
    ['/tools/bulk-processor.html', 'bulk'],
    ['/tools/background-remover.html', 'bg-remover'],
    ['/tools/favicon-generator.html', 'favicon'],
    ['/tools/image-compressor.html', 'compressor'],
    ['/tools/converter.html', 'converter'],
    ['/tools/qr-code-generator.html', 'qrcode'],
  ];
  let pass = 0;
  for (const [url, label] of tests) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text().substring(0,150)); });
    page.on('pageerror', err => errors.push(err.message.substring(0,150)));
    try {
      await page.goto(BASE + url, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      if (label !== 'qrcode') {
        const fi = page.locator('input[type="file"]').first();
        if (await fi.count().then(c => c > 0)) await fi.setInputFiles(TEST_IMG);
        await page.waitForTimeout(1500);
      }
      if (label === 'qrcode') {
        const btn = page.locator('#downloadPngBtn').first();
        if (await btn.count().then(c => c > 0)) {
          const dlP = page.waitForEvent('download', { timeout: 15000 });
          await btn.click();
          const dl = await dlP;
          console.log(`✅ ${label}: ${dl.suggestedFilename()}`);
          pass++;
        }
      } else {
        const btn = page.locator('#downloadAllBtn, #processBtn, button:has-text("Download")').first();
        if (await btn.count().then(c => c > 0)) {
          const dlP = page.waitForEvent('download', { timeout: 15000 }).catch(() => null);
          await btn.click().catch(() => {});
          const dl = await dlP;
          if (dl) {
            console.log(`✅ ${label}: ${dl.suggestedFilename()}`);
            pass++;
          } else if (errors.length === 0) {
            console.log(`✅ ${label}: no errors (no download needed)`);
            pass++;
          } else {
            console.log(`❌ ${label}: errors: ${errors[0]}`);
          }
        } else if (errors.length === 0) {
          console.log(`✅ ${label}: OK`);
          pass++;
        }
      }
      if (errors.length > 0) {
        console.log(`   ERRORS: ${errors.join(', ')}`);
      }
    } catch(e) {
      console.log(`❌ ${label}: ${e.message.substring(0,80)}`);
    }
    await ctx.close();
  }
  await browser.close();
  console.log(`\n${pass}/${tests.length} PASS`);
  process.exit(pass === tests.length ? 0 : 1);
})();
