const { chromium } = require('playwright');
const path = require('path');
const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';
const tools = ['favicon-generator', 'ico-icon-generator', 'metadata-viewer', 'avif-support'];

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const slug of tools) {
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('[C] ' + msg.text().substring(0, 200)); });
    page.on('pageerror', err => errors.push('[P] ' + err.message.substring(0, 200)));
    page.on('dialog', async dialog => { errors.push('[D] ' + dialog.type() + ': ' + dialog.message().substring(0, 150)); await dialog.accept().catch(()=>{}); });
    try {
      await page.goto(BASE_URL + '/tools/' + slug + '.html', { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(1000);
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) try { await fi.setInputFiles(TEST_IMAGE); await page.waitForTimeout(1500); } catch(e){}
    } catch(e) { errors.push('[F] ' + e.message.substring(0, 100)); }
    const status = errors.length === 0 ? '\u2705' : '\u274c';
    console.log(status + ' ' + slug + ' | errors: ' + errors.length);
    errors.forEach(e => console.log('   ' + e));
    await context.close();
  }
  await browser.close();
})();
