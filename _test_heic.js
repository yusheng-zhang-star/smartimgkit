/**
 * Quick test for heic-to-jpg specifically
 */
const { chromium } = require('playwright');
const BASE_URL = 'http://localhost:8000';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(`[CONSOLE] ${msg.text()}`); });
  page.on('pageerror', err => errors.push(`[PAGEERROR] ${err.message}`));
  page.on('response', resp => { if (resp.status() >= 400) errors.push(`[HTTP ${resp.status()}] ${resp.url()}`); });

  await page.goto(`${BASE_URL}/tools/heic-to-jpg.html`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  console.log('heic-to-jpg errors:');
  if (errors.length === 0) console.log('  NONE ✅');
  else errors.forEach(e => console.log('  ❌', e.substring(0, 200)));

  await browser.close();
})();
