// Focused retest: compressor, watermark, text-on-image, background-remover (local + live)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const OUT_DIR = path.join(__dirname, 'output_focus');
fs.mkdirSync(OUT_DIR, { recursive: true });

const TARGETS = [
  { slug: 'compressor', btnHints: ['Compress'], waitMs: 60000 },
  { slug: 'watermark', btnHints: ['Apply Watermark', 'Apply', 'Add Watermark', 'Process'], waitMs: 60000 },
  { slug: 'text-on-image', btnHints: ['Add Text', 'Generate', 'Apply', 'Process'], waitMs: 60000 },
  { slug: 'background-remover', btnHints: ['Process', 'Remove Background', 'Remove'], waitMs: 240000 },
];

async function pageState(page) {
  return await page.evaluate(() => {
    const st = {};
    st.status = (document.querySelector('#statusText, #status, .status, #progressText') || {}).textContent || '';
    st.modelLoader = (document.querySelector('#modelLoaderTitle, #modelLoaderSub') || {}).textContent || '';
    st.canvases = Array.from(document.querySelectorAll('canvas')).filter(c => c.width > 50).length;
    st.dataImgs = Array.from(document.querySelectorAll('img')).filter(i => i.src && i.src.startsWith('data:image')).length;
    st.blobImgs = Array.from(document.querySelectorAll('img')).filter(i => i.src && i.src.startsWith('blob:')).length;
    st.visibleImgs = Array.from(document.querySelectorAll('img')).filter(i => {
      const r = i.getBoundingClientRect(); return r.width > 50 && r.height > 50;
    }).length;
    st.previewVisible = Array.from(document.querySelectorAll('#previewArea, #outputArea, #resultArea, .preview-list, .result-box, #workspace')).filter(el => {
      const st2 = getComputedStyle(el); return st2.display !== 'none' && st2.visibility !== 'hidden';
    }).length;
    st.downloadBtns = Array.from(document.querySelectorAll('a[download], button[id*="download" i], button:has-text("Download")')).filter(b => { const r = b.getBoundingClientRect(); return r.width > 0; }).length;
    st.buttons = Array.from(document.querySelectorAll('button')).map(b => (b.textContent || '').trim().substring(0, 40)).filter(Boolean).slice(0, 15);
    st.errors = [];
    return st;
  });
}

async function runTarget(base, t) {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 150)); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 150)));
  page.on('dialog', async d => { errors.push('DIALOG: ' + d.message().substring(0, 100)); await d.accept().catch(() => {}); });

  console.log(`\n=== ${t.slug} @ ${base} ===`);
  let status = 'FAIL', detail = '';
  try {
    await page.goto(`${base}/tools/${t.slug}.html`, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(3000);

    const fi = page.locator('input[type="file"]').first();
    if (await fi.count().then(c => c > 0)) {
      await fi.setInputFiles(TEST_IMAGE);
      await page.waitForTimeout(2500);
    }

    // Pick button by hint text (case-insensitive)
    let btn = null;
    for (const hint of t.btnHints) {
      const loc = page.locator(`button:has-text("${hint}")`).first();
      if (await loc.count().then(c => c > 0)) { btn = loc; break; }
    }
    if (!btn) {
      const state = await pageState(page);
      detail = 'NO BUTTON. Buttons: ' + JSON.stringify(state.buttons);
      console.log('  ' + detail);
      return { slug: t.slug, base, status: 'FAIL', detail, errors };
    }
    const disabled = await btn.isDisabled().catch(() => false);
    if (disabled) {
      const state = await pageState(page);
      detail = 'BUTTON DISABLED. status="' + state.status + '" model="' + state.modelLoader + '"';
      console.log('  ' + detail);
      return { slug: t.slug, base, status: 'FAIL', detail, errors };
    }

    let downloadGot = null;
    const dlP = page.waitForEvent('download', { timeout: t.waitMs }).catch(() => null);
    await btn.click({ timeout: 8000 }).catch(() => { detail = 'CLICK FAILED'; return; });

    const t0 = Date.now();
    let outFound = false, progressLogged = false;
    while (Date.now() - t0 < t.waitMs) {
      const dl = await Promise.race([dlP.then(d => ({ dl: d })), new Promise(r => setTimeout(() => r({ dl: null }), 2500))]);
      if (dl.dl) {
        const savePath = path.join(OUT_DIR, `${base.includes('smartimgkit') ? 'live' : 'local'}-${t.slug}-out`);
        await dl.dl.saveAs(savePath);
        downloadGot = { name: dl.dl.suggestedFilename(), size: fs.existsSync(savePath) ? fs.statSync(savePath).size : 0 };
        fs.unlinkSync(savePath);
        outFound = true;
        break;
      }
      const s = await pageState(page);
      if (s.dataImgs > 0 || s.blobImgs > 0 || s.canvases > 0 || s.previewVisible > 0 || s.downloadBtns > 0) { outFound = true; break; }
      if (Date.now() - t0 > 10000 && !progressLogged) {
        progressLogged = true;
        console.log(`  [progress ${((Date.now() - t0) / 1000).toFixed(0)}s] status="${s.status}" model="${s.modelLoader}"`);
      }
      await page.waitForTimeout(2500);
    }
    const s = await pageState(page);
    detail = `out=${outFound} dl=${downloadGot ? downloadGot.name + '(' + downloadGot.size + 'B)' : '-'} dataImg=${s.dataImgs} blobImg=${s.blobImgs} canvas=${s.canvases} preview=${s.previewVisible} dlBtns=${s.downloadBtns} status="${s.status}" model="${s.modelLoader}"`;
    status = outFound ? 'PASS' : 'FAIL';
    console.log(`  ${status} — ${detail}`);
  } catch (e) {
    detail = e.message.substring(0, 200);
    status = 'FAIL';
    console.log(`  ERROR: ${detail}`);
  }
  const realErrors = errors.filter(e => !/adsbygoogle|google|doubleclick|analytics/i.test(e));
  if (realErrors.length) { console.log('  Console errors:'); realErrors.slice(0, 5).forEach(e => console.log('    ' + e)); if (status === 'PASS') status = 'WARN'; }
  await browser.close();
  return { slug: t.slug, base, status, detail, errors: realErrors.slice(0, 6) };
}

(async () => {
  const results = [];
  for (const base of ['http://localhost:8000', 'https://smartimgkit.com']) {
    for (const t of TARGETS) {
      results.push(await runTarget(base, t));
    }
  }
  console.log('\n========== FOCUSED RETEST RESULTS ==========');
  let pass = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.slug.padEnd(20)} ${r.base.includes('smartimgkit') ? 'LIVE ' : 'LOCAL'} — ${r.detail}`);
    if (r.status === 'PASS') pass++;
  });
  console.log(`\nTotal: ${pass}/${results.length} PASS`);
  fs.writeFileSync(path.join(__dirname, 'focus_results.json'), JSON.stringify(results, null, 2));
  process.exit(0);
})();
