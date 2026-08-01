const { chromium } = require('playwright');
const path = require('path');
const BASE_URL = 'http://localhost:8000';

// Pages that previously had errors, plus some workflow pages
const testPages = [
  `${BASE_URL}/tools/gif-splitter.html`,
  `${BASE_URL}/tools/gif-editor.html`,
  `${BASE_URL}/tools/heic-converter.html`,
  `${BASE_URL}/tools/heic-to-jpg.html`,
  `${BASE_URL}/tools/image-to-pdf.html`,
  `${BASE_URL}/tools/qr-code-generator.html`,
  `${BASE_URL}/tools/signature-maker.html`,
  `${BASE_URL}/tools/favicon-generator.html`,
  `${BASE_URL}/tools/bulk-processor.html`,
  `${BASE_URL}/workflows/avatar-pipeline.html`,
  `${BASE_URL}/workflows/blog-image-pack.html`,
  `${BASE_URL}/workflows/social-media-kit.html`,
  `${BASE_URL}/workflows/e-commerce-pack.html`,
  `${BASE_URL}/workflows/batch-watermark-protect.html`,
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  let pass = 0, fail = 0;
  for (const url of testPages) {
    const page = await browser.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('C:' + msg.text().substring(0, 150)); });
    page.on('pageerror', err => errors.push('P:' + err.message.substring(0, 150)));
    page.on('dialog', async d => { errors.push('D:' + d.message().substring(0, 100)); await d.accept().catch(()=>{}); });
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(800);
    } catch(e) { errors.push('F:' + e.message.substring(0, 100)); }
    const name = url.split('/').slice(-2).join('/');
    if (errors.length === 0) { console.log(`✅ ${name}`); pass++; }
    else { console.log(`❌ ${name}`); errors.forEach(e => console.log(`   ${e}`)); fail++; }
    await page.close();
  }
  await browser.close();
  console.log(`\n${pass}/${testPages.length} PASS, ${fail} FAIL`);
  process.exit(fail > 0 ? 1 : 0);
})();
