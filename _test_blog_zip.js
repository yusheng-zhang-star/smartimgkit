const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(err.message));
  page.on('dialog', async dialog => { errors.push('DIALOG:' + dialog.message()); await dialog.accept().catch(()=>{}); });

  await page.goto(`${BASE_URL}/workflows/blog-image-pack.html`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Upload file
  const fi = page.locator('input[type="file"]').first();
  await fi.setInputFiles(TEST_IMAGE);
  await page.waitForTimeout(1500);

  // Click Run button
  const runBtn = page.locator('#runBtn');
  const downloadPromise = page.waitForEvent('download', { timeout: 60000 });
  await runBtn.click();
  const download = await downloadPromise;

  // Save the download
  const savePath = path.join(__dirname, 'test-output-blog-image-pack.zip');
  await download.saveAs(savePath);
  console.log('ZIP saved to:', savePath);
  console.log('ZIP size:', fs.statSync(savePath).size, 'bytes');

  // Verify it's a valid ZIP (check magic bytes)
  const buf = fs.readFileSync(savePath);
  const isZip = buf[0] === 0x50 && buf[1] === 0x4B; // PK
  console.log('Is valid ZIP:', isZip);
  console.log('First 4 bytes (hex):', buf.slice(0, 4).toString('hex'));

  if (errors.length) {
    console.log('Errors:', errors);
  } else {
    console.log('✅ No JS errors');
  }

  await browser.close();
})();
