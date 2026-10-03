// Minimal cross-origin worker test (local server)
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 150)); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 150)));

  await page.goto('http://localhost:8000/_test_files/worker_test.html', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(5000);
  const text = await page.locator('#out').textContent();
  console.log('RESULT:\n' + text);
  console.log('Console errors:', JSON.stringify(errors.slice(0, 5)));
  await browser.close();
  process.exit(0);
})();
