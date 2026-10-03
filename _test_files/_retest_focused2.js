// Focused retest v2: verified + suspected-false-positive tools (local + live)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const TEST_PDF = path.join(__dirname, '..', '_test_files', 'test_sample.pdf');
const OUT_DIR = path.join(__dirname, 'output_focus2');
fs.mkdirSync(OUT_DIR, { recursive: true });

// [base, slug, file, btnHints, waitMs, expectKind] expectKind: preview|download|canvas|status
const CASES = [
  ['LOCAL', 'compressor', TEST_IMAGE, ['Compress'], 45000],
  ['LOCAL', 'watermark', TEST_IMAGE, ['Apply Watermark', 'Apply', 'Add Watermark'], 45000],
  ['LOCAL', 'text-on-image', TEST_IMAGE, ['Add Text', 'Generate', 'Apply'], 45000],
  ['LOCAL', 'background-remover', TEST_IMAGE, ['Process', 'Remove Background'], 240000],
  ['LOCAL', 'pdf-compress', TEST_PDF, ['Compress'], 45000],
  ['LOCAL', 'pdf-rotate', TEST_PDF, ['Rotate', 'Apply'], 45000],
  ['LOCAL', 'pdf-annotate', TEST_PDF, ['Annotate', 'Add', 'Apply'], 45000],
  ['LOCAL', 'pdf-delete-pages', TEST_PDF, ['Delete'], 45000],
  ['LOCAL', 'pdf-extract-pages', TEST_PDF, ['Extract'], 45000],
  ['LIVE', 'compressor', TEST_IMAGE, ['Compress'], 45000],
  ['LIVE', 'watermark', TEST_IMAGE, ['Apply Watermark', 'Apply', 'Add Watermark'], 45000],
  ['LIVE', 'text-on-image', TEST_IMAGE, ['Add Text', 'Generate', 'Apply'], 45000],
  ['LIVE', 'background-remover', TEST_IMAGE, ['Process', 'Remove Background'], 240000],
  ['LIVE', 'gif-maker', TEST_IMAGE, ['Generate'], 60000],
  ['LIVE', 'pdf-to-images', TEST_PDF, ['Convert'], 60000],
];

async function state(page) {
  return await page.evaluate(() => {
    const st = {};
    st.status = (document.querySelector('#statusText, #status, .status, #progressText, #result') || {}).textContent || '';
    st.canvases = Array.from(document.querySelectorAll('canvas')).filter(c => c.width > 50).length;
    st.imgs = Array.from(document.querySelectorAll('img')).filter(i => i.src && (i.src.startsWith('data:image') || i.src.startsWith('blob:'))).length;
    st.previewVisible = Array.from(document.querySelectorAll('#previewArea, #outputArea, #resultArea, .preview-list, .result-box, #workspace, #resultContainer')).filter(el => { const s = getComputedStyle(el); return s.display !== 'none'; }).length;
    st.dlBtns = Array.from(document.querySelectorAll('a[download], button[id*="download"], button[id*="Download"]')).filter(b => b.getBoundingClientRect().width > 0).length;
    st.dialogs = 0;
    return st;
  });
}

async function run(base, slug, file, hints, waitMs) {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1400, height: 950 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 130)); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 130)));
  page.on('dialog', async d => { errors.push('DIALOG: ' + d.message().substring(0, 100)); await d.accept().catch(() => {}); });

  const urlBase = base === 'LOCAL' ? 'http://localhost:8000' : 'https://smartimgkit.com';
  console.log(`\n=== ${slug} @ ${base} ===`);
  let status = 'FAIL', detail = '';
  try {
    await page.goto(`${urlBase}/tools/${slug}.html`, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(3000);

    if (file) {
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) { await fi.setInputFiles(file); await page.waitForTimeout(2500); }
      else throw new Error('no file input');
    }

    // Special handling: pdf-delete-pages / pdf-extract-pages need page numbers input
    if (slug === 'pdf-delete-pages' || slug === 'pdf-extract-pages') {
      const numInput = page.locator('input[type="text"], input[type="number"]').first();
      if (await numInput.count().then(c => c > 0)) { await numInput.fill('1'); await page.waitForTimeout(300); }
    }

    let btn = null;
    for (const h of hints) {
      const loc = page.locator(`button:has-text("${h}")`).first();
      if (await loc.count().then(c => c > 0)) { btn = loc; break; }
    }
    if (!btn) {
      const s = await state(page);
      const btns = await page.evaluate(() => Array.from(document.querySelectorAll('button')).map(b => (b.textContent || '').trim().substring(0, 30)).slice(0, 12));
      detail = 'NO BTN. buttons=' + JSON.stringify(btns) + ' status="' + s.status + '"';
      console.log('  ' + detail);
      return { slug, base, status: 'FAIL', detail, errors };
    }
    const disabled = await btn.isDisabled().catch(() => false);
    if (disabled) {
      const s = await state(page);
      detail = 'BTN DISABLED. status="' + s.status + '"';
      console.log('  ' + detail);
      return { slug, base, status: 'FAIL', detail, errors };
    }

    let downloadGot = null;
    const dlP = page.waitForEvent('download', { timeout: waitMs }).catch(() => null);
    await btn.click({ timeout: 8000 }).catch(() => {});
    const t0 = Date.now();
    let outFound = false, progLogged = false;
    while (Date.now() - t0 < waitMs) {
      const dl = await Promise.race([dlP.then(d => ({ dl: d })), new Promise(r => setTimeout(() => r({ dl: null }), 2500))]);
      if (dl.dl) {
        const savePath = path.join(OUT_DIR, `${base}-${slug}-out`);
        await dl.dl.saveAs(savePath);
        downloadGot = { name: dl.dl.suggestedFilename(), size: fs.existsSync(savePath) ? fs.statSync(savePath).size : 0 };
        fs.unlinkSync(savePath);
        outFound = true;
        break;
      }
      const s = await state(page);
      if (s.imgs > 0 || s.canvases > 0 || s.previewVisible > 0 || s.dlBtns > 0) { outFound = true; break; }
      if (Date.now() - t0 > 12000 && !progLogged) { progLogged = true; console.log(`  [t=${((Date.now() - t0) / 1000).toFixed(0)}s] status="${s.status}"`); }
      await page.waitForTimeout(2500);
    }
    const s = await state(page);
    detail = `out=${outFound} dl=${downloadGot ? downloadGot.name + '(' + downloadGot.size + 'B)' : '-'} img=${s.imgs} canvas=${s.canvases} preview=${s.previewVisible} dlBtn=${s.dlBtns} status="${s.status}"`;
    status = outFound ? 'PASS' : 'FAIL';
    console.log(`  ${status} — ${detail}`);
  } catch (e) {
    detail = e.message.substring(0, 200);
    status = 'FAIL';
    console.log(`  ERROR: ${detail}`);
  }
  const realErrors = errors.filter(e => !/adsbygoogle|googlesyndication|doubleclick|analytics|ERR_CONNECTION/i.test(e));
  if (realErrors.length) { console.log('  Console errors:'); realErrors.slice(0, 5).forEach(e => console.log('    ' + e)); if (status === 'PASS') status = 'WARN'; }
  await browser.close();
  return { slug, base, status, detail, errors: realErrors.slice(0, 6) };
}

(async () => {
  const results = [];
  for (const c of CASES) {
    results.push(await run(c[0], c[1], c[2], c[3], c[4]));
  }
  console.log('\n========== FOCUSED RETEST v2 RESULTS ==========');
  let pass = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.slug.padEnd(22)} ${r.base.padEnd(5)} — ${r.detail}`);
    if (r.status === 'PASS') pass++;
  });
  console.log(`\nTotal: ${pass}/${results.length} PASS`);
  fs.writeFileSync(path.join(__dirname, 'focus2_results.json'), JSON.stringify(results, null, 2));
  process.exit(0);
})();
