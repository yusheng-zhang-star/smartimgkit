/**
 * FINAL FULL TEST: 72 tools + 19 workflows = 91 pages
 * Check: no JS errors, no 404s
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE_URL = 'http://localhost:8000';
const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');

const toolFiles = fs.readdirSync(path.join(__dirname, 'tools'))
  .filter(f => f.endsWith('.html')).map(f => f.replace('.html', '')).sort();
const wfFiles = fs.readdirSync(path.join(__dirname, 'workflows'))
  .filter(f => f.endsWith('.html') && !f.startsWith('_')).map(f => f.replace('.html', '')).sort();

const allPages = [
  ...toolFiles.map(s => ({ slug: s, type: 'tools', url: `${BASE_URL}/tools/${s}.html` })),
  ...wfFiles.map(s => ({ slug: s, type: 'workflows', url: `${BASE_URL}/workflows/${s}.html` })),
];

(async () => {
  console.log('='.repeat(70));
  console.log(`FINAL FULL TEST: ${allPages.length} pages (${toolFiles.length} tools + ${wfFiles.length} workflows)`);
  console.log('='.repeat(70));
  const browser = await chromium.launch({ headless: true });
  let pass = 0, fail = 0;
  const failures = [];

  for (const pageInfo of allPages) {
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('[C] ' + msg.text().substring(0, 200)); });
    page.on('pageerror', err => errors.push('[P] ' + err.message.substring(0, 200)));
    page.on('response', resp => { if (resp.status() >= 400 && !resp.url().includes('favicon')) errors.push('[404] ' + resp.url().split('/').slice(-2).join('/')); });
    page.on('dialog', async dialog => { errors.push('[D] ' + dialog.message().substring(0, 100)); await dialog.accept().catch(()=>{}); });

    let uploaded = false;
    try {
      await page.goto(pageInfo.url, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      // Try to upload if file input exists
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        try { await fi.setInputFiles(TEST_IMAGE); uploaded = true; await page.waitForTimeout(1000); } catch(e) {}
      }
    } catch(e) { errors.push('[F] ' + e.message.substring(0, 100)); }

    if (errors.length === 0) {
      pass++;
    } else {
      fail++;
      failures.push({ slug: pageInfo.slug, type: pageInfo.type, errors });
      console.log(`❌ ${pageInfo.type}/${pageInfo.slug}`);
      errors.forEach(e => console.log(`   ${e}`));
    }
    await context.close();
  }

  await browser.close();
  console.log('\n' + '='.repeat(70));
  console.log(`RESULT: ${pass}/${allPages.length} PASS, ${fail} FAIL`);
  console.log('='.repeat(70));
  if (fail === 0) console.log('✅ ALL PASS!');
  process.exit(fail > 0 ? 1 : 0);
})();
