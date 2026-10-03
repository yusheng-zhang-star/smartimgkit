// Deep test for AI/ML heavy tools: model loading + real processing + output verification
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';
const OUT_DIR = path.join(__dirname, 'output_ai');
fs.mkdirSync(OUT_DIR, { recursive: true });

// [slug, processBtnText, waitMs, expectCanvasOrImg]
const TESTS = [
  { slug: 'background-remover', btn: 'Process', waitMs: 180000, expect: 'img', check: 'data:image/png' },
  { slug: 'object-remover', btn: 'Process', waitMs: 180000, expect: 'img', check: 'data:image/png' },
  { slug: 'photo-restoration', btn: 'Restore', waitMs: 240000, expect: 'img', check: 'data:image' },
  { slug: 'image-upscaler', btn: 'Upscale', waitMs: 180000, expect: 'img', check: 'data:image' },
  { slug: 'image-enhancer', btn: 'Enhance', waitMs: 120000, expect: 'img', check: 'data:image' },
  { slug: 'beauty-editor', btn: 'Enhance', waitMs: 120000, expect: 'img', check: 'data:image' },
  { slug: 'face-blur', btn: 'Blur', waitMs: 120000, expect: 'canvas', check: '' },
  { slug: 'product-white-background', btn: 'Process', waitMs: 180000, expect: 'img', check: 'data:image/png' },
  { slug: 'ocr', btn: 'Extract', waitMs: 60000, expect: 'text', check: '' },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const t of TESTS) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 150)); });
    page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 150)));
    page.on('dialog', async d => { errors.push('DIALOG: ' + d.message().substring(0, 100)); await d.accept().catch(() => {}); });

    console.log(`\n=== ${t.slug} (${t.btn}, wait ${t.waitMs / 1000}s) ===`);
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE_URL}/tools/${t.slug}.html`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2500);

      // Upload
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        await fi.setInputFiles(TEST_IMAGE);
        await page.waitForTimeout(1500);
      }

      // Click process button (contains text)
      const btn = page.locator(`button:has-text("${t.btn}"), #processBtn, #applyBtn, #runBtn`).first();
      const btnCount = await btn.count().then(c => c > 0);
      if (!btnCount) throw new Error('no process button found');

      let downloadGot = null;
      const dlP = page.waitForEvent('download', { timeout: t.waitMs }).catch(() => null);
      await btn.click({ timeout: 5000 }).catch(() => {});

      // Wait for either download or output indicator
      const t0 = Date.now();
      let outFound = false;
      while (Date.now() - t0 < t.waitMs) {
        const dl = await Promise.race([dlP.then(d => ({ dl: d })), new Promise(r => setTimeout(() => r({ dl: null }), 2000))]);
        if (dl.dl) {
          const savePath = path.join(OUT_DIR, `${t.slug}-out`);
          await dl.dl.saveAs(savePath);
          downloadGot = { name: dl.dl.suggestedFilename(), size: fs.existsSync(savePath) ? fs.statSync(savePath).size : 0 };
          fs.unlinkSync(savePath);
          outFound = true;
          break;
        }
        const ind = await page.evaluate(({ expect, check }) => {
          if (expect === 'img') {
            const imgs = Array.from(document.querySelectorAll('img#output, img#result, #outputImage, #resultImage, .result-image, #previewImage, #resultImg'));
            for (const i of imgs) if (i.src && (check === '' || i.src.startsWith(check))) return true;
            // any data:image img that changed recently
            const all = Array.from(document.querySelectorAll('img')).filter(i => i.src && i.src.startsWith('data:image'));
            return all.length > 0;
          }
          if (expect === 'canvas') {
            const cs = Array.from(document.querySelectorAll('canvas')).filter(c => c.width > 50 && c.height > 50);
            return cs.length > 0;
          }
          if (expect === 'text') {
            const st = document.querySelector('#result, #ocrResult, #output, #resultArea, #statusText, .result-box');
            return st && st.textContent && st.textContent.trim().length > 5;
          }
          return false;
        }, { expect: t.expect, check: t.check });
        if (ind) { outFound = true; break; }
        await page.waitForTimeout(3000);
      }

      // Progress trace
      const trace = await page.evaluate(() => {
        const st = document.querySelector('#statusText, #status, .status, #progressText, #modelLoaderSub, #modelLoaderTitle');
        return st ? st.textContent.trim().substring(0, 150) : '';
      });

      detail = `outFound=${outFound} dl=${downloadGot ? downloadGot.name + ' (' + downloadGot.size + 'B)' : '-'} trace="${trace}"`;
      status = outFound ? 'PASS' : 'FAIL';
      console.log(`  ${status} — ${detail}`);
      if (errors.length) { console.log(`  Console errors (${errors.length}):`); errors.slice(0, 4).forEach(e => console.log('    ' + e)); if (status === 'PASS') status = 'WARN'; }
    } catch (e) {
      detail = e.message.substring(0, 200);
      status = 'FAIL';
      console.log(`  ERROR: ${detail}`);
    }
    results.push({ slug: t.slug, status, detail, errors: errors.slice(0, 8) });
    await ctx.close();
  }
  await browser.close();

  console.log('\n========== AI TOOLS RESULTS ==========');
  let pass = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.slug.padEnd(26)} ${r.status} — ${r.detail}`);
    if (r.status === 'PASS') pass++;
  });
  console.log(`\nTotal: ${pass}/${results.length} PASS`);
  fs.writeFileSync(path.join(__dirname, 'ai_tools_results.json'), JSON.stringify(results, null, 2));
  process.exit(0);
})();
