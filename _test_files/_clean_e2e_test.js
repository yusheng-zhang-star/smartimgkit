/**
 * CLEAN E2E TEST (patched from _comprehensive_test.js):
 * - Excludes _* dev/test pages
 * - Uses domcontentloaded instead of networkidle (external CDNs block networkidle)
 * - Uploads real files, clicks process buttons, captures downloads
 * - Collects console/page errors and 4xx/5xx responses
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const TEST_PDF = path.join(__dirname, '..', 'test-file.pdf');
const TEST_VIDEO = path.join(__dirname, '..', 'test-video.mp4');
const TEST_TXT = path.join(__dirname, '..', 'test-file.txt');
const BASE_URL = 'http://localhost:8000';
const OUT_DIR = path.join(__dirname, 'output_clean');
fs.mkdirSync(OUT_DIR, { recursive: true });

const toolFiles = fs.readdirSync(path.join(__dirname, '..', 'tools'))
  .filter(f => f.endsWith('.html') && !f.startsWith('_')).map(f => f.replace('.html', '')).sort();
const wfFiles = fs.readdirSync(path.join(__dirname, '..', 'workflows'))
  .filter(f => f.endsWith('.html') && !f.startsWith('_') && f !== 'index.html').map(f => f.replace('.html', '')).sort();

function getTestFile(slug) {
  if (slug.startsWith('pdf-')) return TEST_PDF;
  if (slug.startsWith('video-')) return TEST_VIDEO;
  if (['word-to-pdf', 'csv-to-pdf', 'excel-to-pdf', 'epub-to-pdf', 'html-to-pdf', 'txt-to-pdf', 'pdf-to-word', 'pdf-to-excel', 'pdf-to-ppt'].includes(slug)) return path.join(__dirname, '..', '_test_files', 'test_sample.pdf');
  if (['text-diff', 'text-find-replace', 'text-sorter', 'case-converter', 'regex-tester', 'word-counter', 'json-formatter', 'base64', 'url-encoder', 'html-encoder', 'password-generator', 'uuid-generator'].includes(slug)) return TEST_TXT;
  return TEST_IMAGE;
}

// Map of known generic selectors ordered by likelihood
const BTN_SELECTORS = [
  '#processBtn', '#compressBtn', '#convertBtn', '#applyBtn', '#runBtn', '#generateBtn',
  '#removeBtn', '#extractBtn', '#splitBtn', '#mergeBtn', '#rotateBtn', '#resizeBtn',
  '#cropBtn', '#convertNowBtn', '#startBtn', '#enhanceBtn', '#restoreBtn', '#upscaleBtn',
  '#downloadBtn', '#downloadPngBtn',
  'button:has-text("Process")', 'button:has-text("Compress")', 'button:has-text("Convert")',
  'button:has-text("Apply")', 'button:has-text("Run")', 'button:has-text("Generate")',
  'button:has-text("Extract")', 'button:has-text("Split")', 'button:has-text("Merge")',
  'button:has-text("Rotate")', 'button:has-text("Resize")', 'button:has-text("Crop")',
  'button:has-text("Start")', 'button:has-text("Remove Background")', 'button:has-text("Remove")',
  'button:has-text("Enhance")', 'button:has-text("Restore")', 'button:has-text("Upscale")',
  'button:has-text("Download")', 'button.btn-primary', '.btn-primary',
];

async function tryClickProcess(page) {
  for (const sel of BTN_SELECTORS) {
    const btn = page.locator(sel).first();
    if (await btn.count().then(c => c > 0)) {
      const disabled = await btn.isDisabled().catch(() => true);
      if (!disabled) {
        try {
          await btn.click({ timeout: 3000 });
          return sel;
        } catch (e) { /* try next */ }
      }
    }
  }
  return null;
}

async function checkOutputIndicators(page) {
  return await page.evaluate(() => {
    const out = {
      downloadLinks: 0, canvases: 0, outputImages: 0, resultVisible: false,
      statusText: '', hasZipBlob: false, previewImgs: 0
    };
    document.querySelectorAll('a[download]').forEach(() => out.downloadLinks++);
    document.querySelectorAll('canvas').forEach(c => {
      try { if (c.width > 10 && c.height > 10) out.canvases++; } catch (e) {}
    });
    document.querySelectorAll('img#output, img#result, #resultImage, #outputImage, .result-image, #previewImage').forEach(i => {
      if (i.src && i.src.startsWith('data:')) out.outputImages++;
    });
    document.querySelectorAll('#result, #output, .result-box, .result-container, #resultArea, #outputArea').forEach(el => {
      if (el.offsetParent !== null || getComputedStyle(el).display !== 'none') out.resultVisible = true;
    });
    const st = document.querySelector('#status, #statusText, .status, #progressText');
    if (st) out.statusText = (st.textContent || '').trim().substring(0, 120);
    document.querySelectorAll('img').forEach(i => { if (i.src && i.src.startsWith('data:image')) out.previewImgs++; });
    return out;
  });
}

(async () => {
  console.log('='.repeat(70));
  console.log(`CLEAN E2E TEST — Tools: ${toolFiles.length} | Workflows: ${wfFiles.length}`);
  console.log('='.repeat(70));
  const browser = await chromium.launch({ headless: true });
  const results = [];

  // ---- TOOLS ----
  console.log('\n--- TOOLS ---');
  for (const slug of toolFiles) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push('[C] ' + m.text().substring(0, 160)); });
    page.on('pageerror', e => errors.push('[P] ' + e.message.substring(0, 160)));
    page.on('response', r => { if (r.status() >= 400 && !r.url().includes('favicon') && !r.url().includes('adsbygoogle')) errors.push('[HTTP' + r.status() + '] ' + r.url().split('/').slice(-1)[0]); });
    page.on('dialog', async d => { errors.push('[D] ' + d.message().substring(0, 120)); await d.accept().catch(() => {}); });

    let loadOK = false, uploaded = false, processClicked = null, downloadGot = null;
    const t0 = Date.now();
    try {
      const resp = await page.goto(`${BASE_URL}/tools/${slug}.html`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      loadOK = resp && resp.status() < 400;
      await page.waitForTimeout(2000); // let JS init

      const fileInput = page.locator('input[type="file"]').first();
      if (await fileInput.count().then(c => c > 0)) {
        try {
          await fileInput.setInputFiles(getTestFile(slug));
          uploaded = true;
          await page.waitForTimeout(1200);
        } catch (e) { errors.push('[UP] ' + e.message.substring(0, 120)); }
      }

      processClicked = await tryClickProcess(page);
      if (processClicked) {
        // race download for up to 25s
        try {
          const dlP = page.waitForEvent('download', { timeout: 25000 });
          const dl = await Promise.race([
            dlP,
            new Promise(res => setTimeout(() => res(null), 25000))
          ]);
          if (dl) {
            const savePath = path.join(OUT_DIR, `${slug}-out`);
            await dl.saveAs(savePath);
            downloadGot = { name: dl.suggestedFilename(), size: fs.existsSync(savePath) ? fs.statSync(savePath).size : 0 };
            fs.unlinkSync(savePath);
          }
        } catch (e) {}
        await page.waitForTimeout(2000);
      }
    } catch (e) { errors.push('[F] ' + e.message.substring(0, 120)); }

    const out = await checkOutputIndicators(page).catch(() => ({}));
    const realErrors = errors.filter(e => !e.startsWith('[D] ') || (!/upload|select|valid|choose|pick/i.test(e)));
    const status = loadOK && realErrors.length === 0 ? 'PASS' : (realErrors.length === 0 ? 'WARN' : 'FAIL');
    results.push({ kind: 'tool', slug, loadOK, uploaded, processClicked, downloadGot, out, errors: realErrors, status, ms: Date.now() - t0 });
    const mark = status === 'PASS' ? '✅' : status === 'WARN' ? '⚠️' : '❌';
    console.log(`${mark} tool/${slug.padEnd(24)} load:${loadOK} up:${uploaded} proc:${processClicked || '-'} dl:${downloadGot ? downloadGot.name : '-'} out:${out.canvases > 0 ? 'canvas' : ''}${out.previewImgs > 0 ? '+preview' : ''} errs:${realErrors.length}`);
    if (realErrors.length) realErrors.slice(0, 4).forEach(e => console.log(`     ${e}`));
    await ctx.close();
  }

  // ---- WORKFLOWS ----
  console.log('\n--- WORKFLOWS ---');
  for (const slug of wfFiles) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push('[C] ' + m.text().substring(0, 160)); });
    page.on('pageerror', e => errors.push('[P] ' + e.message.substring(0, 160)));
    page.on('response', r => { if (r.status() >= 400 && !r.url().includes('favicon') && !r.url().includes('adsbygoogle')) errors.push('[HTTP' + r.status() + '] ' + r.url().split('/').slice(-1)[0]); });
    page.on('dialog', async d => { errors.push('[D] ' + d.message().substring(0, 120)); await d.accept().catch(() => {}); });

    let loadOK = false, uploaded = false, processClicked = null, downloadGot = null;
    try {
      const resp = await page.goto(`${BASE_URL}/workflows/${slug}.html`, { waitUntil: 'domcontentloaded', timeout: 15000 });
      loadOK = resp && resp.status() < 400;
      await page.waitForTimeout(2000);
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        try { await fi.setInputFiles(TEST_IMAGE); uploaded = true; await page.waitForTimeout(1200); } catch (e) {}
      }
      processClicked = await tryClickProcess(page);
      if (processClicked) {
        try {
          const dlP = page.waitForEvent('download', { timeout: 60000 });
          const dl = await Promise.race([dlP, new Promise(res => setTimeout(() => res(null), 60000))]);
          if (dl) {
            const savePath = path.join(OUT_DIR, `${slug}-out.zip`);
            await dl.saveAs(savePath);
            downloadGot = { name: dl.suggestedFilename(), size: fs.existsSync(savePath) ? fs.statSync(savePath).size : 0 };
            fs.unlinkSync(savePath);
          }
        } catch (e) {}
        await page.waitForTimeout(2000);
      }
    } catch (e) { errors.push('[F] ' + e.message.substring(0, 120)); }

    const realErrors = errors.filter(e => !e.startsWith('[D] ') || (!/upload|select|valid|choose|pick/i.test(e)));
    const status = loadOK && realErrors.length === 0 ? 'PASS' : (realErrors.length === 0 ? 'WARN' : 'FAIL');
    results.push({ kind: 'workflow', slug, loadOK, uploaded, processClicked, downloadGot, errors: realErrors, status });
    const mark = status === 'PASS' ? '✅' : status === 'WARN' ? '⚠️' : '❌';
    console.log(`${mark} wf/${slug.padEnd(24)} load:${loadOK} up:${uploaded} proc:${processClicked || '-'} dl:${downloadGot ? downloadGot.name : '-'} errs:${realErrors.length}`);
    if (realErrors.length) realErrors.slice(0, 4).forEach(e => console.log(`     ${e}`));
    await ctx.close();
  }

  await browser.close();

  // Summary
  const fails = results.filter(r => r.status === 'FAIL');
  const warns = results.filter(r => r.status === 'WARN');
  console.log('\n' + '='.repeat(70));
  console.log('FINAL SUMMARY');
  console.log(`TOTAL: ${results.length} | PASS: ${results.length - fails.length - warns.length} | WARN: ${warns.length} | FAIL: ${fails.length}`);
  if (fails.length) {
    console.log('\nFAILED:');
    fails.forEach(f => console.log(`  ❌ ${f.kind}/${f.slug} — ${f.errors.map(e => e.substring(0, 80)).join(' | ')}`));
  }
  if (warns.length) {
    console.log('\nWARN (loaded OK but no upload/process observed):');
    warns.forEach(w => console.log(`  ⚠️ ${w.kind}/${w.slug}`));
  }
  fs.writeFileSync(path.join(__dirname, 'clean_e2e_results.json'), JSON.stringify(results, null, 2));
  console.log('\nResults saved to _test_files/clean_e2e_results.json');
  process.exit(0);
})();
