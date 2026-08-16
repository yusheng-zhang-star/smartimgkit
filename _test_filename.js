const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true });
  const page = await ctx.newPage();

  console.log('Testing e-commerce-pack download filename...');

  await page.goto('http://localhost:8000/workflows/e-commerce-pack.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);

  // Upload file
  const fi = page.locator('input[type="file"]').first();
  await fi.setInputFiles(path.join(__dirname, 'test-image.jpg'));
  await page.waitForTimeout(1000);

  // Run pipeline
  const runBtn = page.locator('#runBtn').first();
  const dlPromise = page.waitForEvent('download', { timeout: 60000 });
  await runBtn.click({ timeout: 5000 });
  const dl = await dlPromise;

  const suggestedName = dl.suggestedFilename();
  console.log(`Suggested filename: ${suggestedName}`);

  const savePath = path.join(__dirname, '_test_final.zip');
  await dl.saveAs(savePath);
  const size = fs.statSync(savePath).size;
  console.log(`File size: ${size} bytes`);

  // Verify ZIP
  const buf = fs.readFileSync(savePath);
  const isZip = buf[0] === 0x50 && buf[1] === 0x4B;
  console.log(`Valid ZIP: ${isZip ? 'YES' : 'NO'}`);

  fs.unlinkSync(savePath);
  await browser.close();

  if (suggestedName === 'product-images.zip' && isZip) {
    console.log('\n✅ SUCCESS: Filename is correct and ZIP is valid!');
    process.exit(0);
  } else {
    console.log('\n❌ FAILED');
    process.exit(1);
  }
})();
