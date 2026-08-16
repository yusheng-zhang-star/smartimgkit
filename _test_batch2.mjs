// Batch 2 verification: upload real PDF to each editing tool, interact, verify download output.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BASE = 'http://localhost:8000/tools';
const TEST_DIR = 'E:\\网站项目\\smartimgkit\\_test_files';
const OUT_DIR = 'E:\\网站项目\\smartimgkit\\_test_files\\output_batch2';
fs.mkdirSync(OUT_DIR, { recursive: true });

function checkPdf(filePath) {
  if (!fs.existsSync(filePath)) return { ok: false, reason: 'file not found' };
  const stat = fs.statSync(filePath);
  if (stat.size < 200) return { ok: false, reason: `file too small (${stat.size} bytes)` };
  const buf = fs.readFileSync(filePath);
  const head = buf.slice(0, 5).toString('latin1');
  // tail check for %%EOF
  const tail = buf.slice(-1024).toString('latin1');
  const hasEof = tail.indexOf('%%EOF') > -1;
  return { ok: head.startsWith('%PDF') && hasEof, reason: head.startsWith('%PDF') ? `valid PDF (${stat.size} bytes, eof=${hasEof})` : `bad magic: ${head}` };
}

async function waitDownload(page, btnSelector, outName) {
  const downloadPromise = page.waitForEvent('download', { timeout: 60000 });
  await page.click(btnSelector);
  const download = await downloadPromise;
  const suggested = download.suggestedFilename();
  const savePath = path.join(OUT_DIR, outName);
  await download.saveAs(savePath);
  return { suggested, savePath };
}

async function newPage(context) {
  const page = await context.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  return { page, errors };
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const results = [];

  // ---- 1. pdf-editor ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-editor ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-editor.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#editorArea', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(1200); // render page
      // Click on canvas to add a text placement
      const canvas = page.locator('#pageCanvas');
      await canvas.waitFor({ state: 'visible' });
      const box = await canvas.boundingBox();
      await page.mouse.click(box.x + 120, box.y + 100);
      await page.waitForTimeout(300);
      // Verify a placement was added
      const listText = await page.locator('#placementList').textContent();
      if (!listText || listText.indexOf('Hello PDF') < 0) throw new Error('placement not added: ' + listText);
      const { suggested, savePath } = await waitDownload(page, '#downloadBtn', 'pdf-editor.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-editor', status, detail });
    await page.close();
  }

  // ---- 2. pdf-annotate ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-annotate ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-annotate.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#annotArea', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(1200);
      const canvas = page.locator('#pageCanvas');
      const box = await canvas.boundingBox();
      // Drag a highlight rectangle
      await page.mouse.move(box.x + 40, box.y + 80);
      await page.mouse.down();
      await page.mouse.move(box.x + 280, box.y + 160, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(300);
      const listText = await page.locator('#annotList').textContent();
      if (!listText || listText.indexOf('Highlight') < 0) throw new Error('annotation not added: ' + listText);
      const { suggested, savePath } = await waitDownload(page, '#downloadBtn', 'pdf-annotate.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-annotate', status, detail });
    await page.close();
  }

  // ---- 3. pdf-number-pages ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-number-pages ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-number-pages.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#controls', { state: 'visible', timeout: 15000 });
      // Keep defaults (bottom-center, "Page {n} of {total}")
      const { suggested, savePath } = await waitDownload(page, '#applyBtn', 'pdf-number-pages.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-number-pages', status, detail });
    await page.close();
  }

  // ---- 4. pdf-crop ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-crop ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-crop.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#cropArea', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(1200);
      const canvas = page.locator('#pageCanvas');
      const box = await canvas.boundingBox();
      // Drag a crop selection
      await page.mouse.move(box.x + 30, box.y + 30);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width - 40, box.y + box.height - 40, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(300);
      const info = await page.locator('#cropInfo').textContent();
      if (!info || info.indexOf('Selected') < 0) throw new Error('selection not made: ' + info);
      const { suggested, savePath } = await waitDownload(page, '#applyBtn', 'pdf-crop.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason} | ${info}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-crop', status, detail });
    await page.close();
  }

  // ---- 5. pdf-organize ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-organize ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-organize.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#organizeArea', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(1500);
      // Count thumbs
      const thumbCount = await page.locator('.page-thumb').count();
      if (thumbCount < 1) throw new Error('no page thumbnails rendered');
      // Click duplicate on first thumb, then delete second
      await page.locator('.dup-btn').first().click();
      await page.waitForTimeout(200);
      const { suggested, savePath } = await waitDownload(page, '#downloadBtn', 'pdf-organize.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason} | thumbs=${thumbCount}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-organize', status, detail });
    await page.close();
  }

  // ---- 6. pdf-compare (no download; verify comparison result text) ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-compare ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-compare.html`, { waitUntil: 'networkidle', timeout: 30000 });
      // Upload same PDF to both → should be identical
      await page.setInputFiles('#file1', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.setInputFiles('#file2', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForTimeout(800);
      const enabled = await page.isEnabled('#compareBtn');
      if (!enabled) throw new Error('compare button not enabled');
      await page.click('#compareBtn');
      // Wait for completion status
      await page.waitForFunction(() => {
        const t = document.getElementById('statusText').textContent || '';
        return t.indexOf('Comparison complete') > -1 || t.indexOf('Error') > -1;
      }, { timeout: 60000 });
      const statusText = await page.locator('#statusText').textContent();
      const badges = await page.locator('.diff-badge').count();
      if (statusText && statusText.indexOf('Comparison complete') > -1 && badges > 0) {
        status = 'PASS';
        detail = statusText + ` | badges=${badges}`;
      } else {
        status = 'FAIL';
        detail = 'no comparison result | status="' + statusText + '"';
      }
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-compare', status, detail });
    await page.close();
  }

  // ---- 7. pdf-redact ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing pdf-redact ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/pdf-redact.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.pdf'));
      await page.waitForSelector('#redactArea', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(1200);
      const canvas = page.locator('#pageCanvas');
      const box = await canvas.boundingBox();
      // Drag two redaction rectangles
      await page.mouse.move(box.x + 50, box.y + 60);
      await page.mouse.down();
      await page.mouse.move(box.x + 250, box.y + 140, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(200);
      await page.mouse.move(box.x + 50, box.y + 200);
      await page.mouse.down();
      await page.mouse.move(box.x + 250, box.y + 280, { steps: 8 });
      await page.mouse.up();
      await page.waitForTimeout(300);
      const listText = await page.locator('#redactionList').textContent();
      if (!listText || listText.indexOf('Redaction') < 0) throw new Error('redaction not added: ' + listText);
      const { suggested, savePath } = await waitDownload(page, '#downloadBtn', 'pdf-redact.pdf');
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'pdf-redact', status, detail });
    await page.close();
  }

  await browser.close();

  console.log('\n========== BATCH 2 TEST RESULTS ==========');
  let pass = 0, fail = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.name.padEnd(18)} ${r.status} — ${r.detail}`);
    if (r.status === 'PASS') pass++; else fail++;
  });
  console.log(`\nTotal: ${pass} PASS, ${fail} FAIL/WARN out of ${results.length}`);
  process.exit(fail > 0 ? 1 : 0);
}

run().catch(e => { console.error('Fatal:', e); process.exit(2); });
