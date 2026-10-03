// Live-site functional test: run representative tools on https://smartimgkit.com
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const TEST_PDF = path.join(__dirname, '..', '_test_files', 'test_sample.pdf');
const OUT_DIR = path.join(__dirname, 'output_live');
fs.mkdirSync(OUT_DIR, { recursive: true });
const BASE = 'https://smartimgkit.com';

const TESTS = [
  { slug: 'converter', file: TEST_IMAGE, btn: '#convertBtn', waitMs: 30000, desc: '图片格式转换' },
  { slug: 'compressor', file: TEST_IMAGE, btn: '#compressBtn', waitMs: 30000, desc: '图片压缩' },
  { slug: 'resizer', file: TEST_IMAGE, btn: 'button:has-text("Resize")', waitMs: 30000, desc: '图片缩放' },
  { slug: 'qr-code-generator', file: null, btn: '#generateBtn', waitMs: 20000, desc: '二维码生成' },
  { slug: 'image-to-pdf', file: TEST_IMAGE, btn: '#convertBtn', waitMs: 40000, desc: '图片转PDF' },
  { slug: 'pdf-to-word', file: TEST_PDF, btn: '#convertBtn', waitMs: 60000, desc: 'PDF转Word' },
  { slug: 'watermark', file: TEST_IMAGE, btn: 'button:has-text("Process")', waitMs: 30000, desc: '加水印' },
  { slug: 'text-on-image', file: TEST_IMAGE, btn: 'button:has-text("Add Text")', waitMs: 30000, desc: '图片加文字' },
  { slug: 'background-remover', file: TEST_IMAGE, btn: 'button:has-text("Process")', waitMs: 180000, desc: 'AI抠图' },
  { slug: 'image-upscaler', file: TEST_IMAGE, btn: 'button:has-text("Upscale")', waitMs: 180000, desc: 'AI超分' },
];

async function checkOutput(page) {
  return await page.evaluate(() => {
    const out = { canvases: 0, previewImgs: 0, resultText: '', downloadLinks: 0 };
    document.querySelectorAll('canvas').forEach(c => { if (c.width > 50 && c.height > 50) out.canvases++; });
    document.querySelectorAll('img').forEach(i => { if (i.src && i.src.startsWith('data:image')) out.previewImgs++; });
    document.querySelectorAll('a[download]').forEach(() => out.downloadLinks++);
    const st = document.querySelector('#statusText, #status, .status, #result, #resultArea, #output');
    if (st) out.resultText = st.textContent.trim().substring(0, 120);
    return out;
  });
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  for (const t of TESTS) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 130)); });
    page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 130)));
    page.on('dialog', async d => { errors.push('DIALOG: ' + d.message().substring(0, 80)); await d.accept().catch(() => {}); });

    console.log(`\n=== ${t.slug} (${t.desc}) — LIVE ===`);
    let status = 'FAIL', detail = '';
    try {
      const resp = await page.goto(`${BASE}/tools/${t.slug}.html`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      if (!resp || resp.status() >= 400) throw new Error('HTTP ' + (resp && resp.status()));
      await page.waitForTimeout(2500);

      if (t.file) {
        const fi = page.locator('input[type="file"]').first();
        if (await fi.count().then(c => c > 0)) {
          await fi.setInputFiles(t.file);
          await page.waitForTimeout(1500);
        } else {
          throw new Error('no file input found');
        }
      } else {
        // qr-code-generator: type text first
        const input = page.locator('#textInput, #qrText, textarea, input[type="text"]').first();
        if (await input.count().then(c => c > 0)) {
          await input.fill('https://smartimgkit.com TEST 123');
          await page.waitForTimeout(500);
        }
      }

      const btn = page.locator(t.btn).first();
      if (!(await btn.count().then(c => c > 0))) throw new Error('button not found: ' + t.btn);
      const disabled = await btn.isDisabled().catch(() => false);
      if (disabled) throw new Error('button disabled after upload');

      let downloadGot = null;
      const dlP = page.waitForEvent('download', { timeout: t.waitMs }).catch(() => null);
      await btn.click({ timeout: 5000 }).catch(() => { throw new Error('click failed'); });

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
        const o = await checkOutput(page);
        if (o.previewImgs > 0 || o.canvases > 0 || (o.resultText && o.resultText.length > 3 && !/loading|wait|processing/i.test(o.resultText))) { outFound = true; break; }
        await page.waitForTimeout(3000);
      }
      const o = await checkOutput(page);
      detail = `out=${outFound} dl=${downloadGot ? downloadGot.name + '(' + downloadGot.size + 'B)' : '-'} preview=${o.previewImgs} canvas=${o.canvases} status="${o.resultText}"`;
      status = outFound ? 'PASS' : 'FAIL';
      console.log(`  ${status} — ${detail}`);
    } catch (e) {
      detail = e.message.substring(0, 160);
      status = 'FAIL';
      console.log(`  ERROR: ${detail}`);
    }
    const realErrors = errors.filter(e => !/adsbygoogle|google|doubleclick|analytics/i.test(e));
    if (realErrors.length) { console.log(`  Console errors (${realErrors.length}):`); realErrors.slice(0, 3).forEach(e => console.log('    ' + e)); if (status === 'PASS') status = 'WARN'; }
    results.push({ slug: t.slug, desc: t.desc, status, detail, errors: realErrors.slice(0, 5) });
    await ctx.close();
  }
  await browser.close();

  console.log('\n========== LIVE SITE RESULTS ==========');
  let pass = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.slug.padEnd(24)} ${r.status} — ${r.detail}`);
    if (r.status === 'PASS') pass++;
  });
  console.log(`\nTotal: ${pass}/${results.length} PASS`);
  fs.writeFileSync(path.join(__dirname, 'live_results.json'), JSON.stringify(results, null, 2));
  process.exit(0);
})();
