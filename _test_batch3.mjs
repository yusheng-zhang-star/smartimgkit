// Batch 3 verification: html/txt/csv/epub -> pdf with real files.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BASE = 'http://localhost:8000/tools';
const TEST_DIR = 'E:\\网站项目\\smartimgkit\\_test_files';
const OUT_DIR = 'E:\\网站项目\\smartimgkit\\_test_files\\output_batch3';
fs.mkdirSync(OUT_DIR, { recursive: true });

function checkPdf(filePath) {
  if (!fs.existsSync(filePath)) return { ok: false, reason: 'file not found' };
  const stat = fs.statSync(filePath);
  if (stat.size < 300) return { ok: false, reason: `file too small (${stat.size} bytes)` };
  const buf = fs.readFileSync(filePath);
  const head = buf.slice(0, 5).toString('latin1');
  const tail = buf.slice(-1024).toString('latin1');
  const hasEof = tail.indexOf('%%EOF') > -1;
  return { ok: head.startsWith('%PDF') && hasEof, reason: head.startsWith('%PDF') ? `valid PDF (${stat.size} bytes, eof=${hasEof})` : `bad magic: ${head}` };
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

  // ---- 1. html-to-pdf (file mode) ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing html-to-pdf (file mode) ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/html-to-pdf.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.html'));
      await page.waitForTimeout(300);
      const enabled = await page.isEnabled('#convertBtn');
      if (!enabled) throw new Error('convert button not enabled');
      const dl = page.waitForEvent('download', { timeout: 60000 });
      await page.click('#convertBtn');
      const download = await dl;
      const suggested = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, 'html-to-pdf.pdf');
      await download.saveAs(savePath);
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'html-to-pdf', status, detail });
    await page.close();
  }

  // ---- 1b. html-to-pdf (paste mode) ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing html-to-pdf (paste mode) ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/html-to-pdf.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.click('.mode-tab[data-mode="paste"]');
      await page.fill('#htmlCode', '<h1>Pasted Title</h1><p>This is pasted HTML content for testing.</p>');
      await page.waitForTimeout(200);
      const dl = page.waitForEvent('download', { timeout: 60000 });
      await page.click('#convertBtn');
      const download = await dl;
      const suggested = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, 'html-to-pdf-paste.pdf');
      await download.saveAs(savePath);
      const check = checkPdf(savePath);
      status = (check.ok && suggested.toLowerCase().endsWith('.pdf')) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'html-to-pdf (paste)', status, detail });
    await page.close();
  }

  // ---- 2. txt-to-pdf ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing txt-to-pdf ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/txt-to-pdf.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.txt'));
      await page.waitForTimeout(300);
      const dl = page.waitForEvent('download', { timeout: 60000 });
      await page.click('#convertBtn');
      const download = await dl;
      const suggested = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, 'txt-to-pdf.pdf');
      await download.saveAs(savePath);
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'txt-to-pdf', status, detail });
    await page.close();
  }

  // ---- 3. csv-to-pdf ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing csv-to-pdf ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/csv-to-pdf.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.csv'));
      // Wait for preview to render
      await page.waitForSelector('.preview-box table', { timeout: 10000 });
      const previewRows = await page.locator('.preview-box tbody tr').count();
      if (previewRows < 3) throw new Error(`preview rows too few: ${previewRows}`);
      const dl = page.waitForEvent('download', { timeout: 60000 });
      await page.click('#convertBtn');
      const download = await dl;
      const suggested = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, 'csv-to-pdf.pdf');
      await download.saveAs(savePath);
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason} | preview rows=${previewRows}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'csv-to-pdf', status, detail });
    await page.close();
  }

  // ---- 4. epub-to-pdf ----
  {
    const { page, errors } = await newPage(context);
    console.log('\n=== Testing epub-to-pdf ===');
    let status = 'FAIL', detail = '';
    try {
      await page.goto(`${BASE}/epub-to-pdf.html`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.setInputFiles('#fileInput', path.join(TEST_DIR, 'test_sample.epub'));
      await page.waitForTimeout(300);
      const dl = page.waitForEvent('download', { timeout: 90000 });
      await page.click('#convertBtn');
      const download = await dl;
      const suggested = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, 'epub-to-pdf.pdf');
      await download.saveAs(savePath);
      const check = checkPdf(savePath);
      const extOk = suggested.toLowerCase().endsWith('.pdf');
      status = (check.ok && extOk) ? 'PASS' : 'FAIL';
      detail = `"${suggested}" — ${check.reason}`;
      console.log('  ' + detail);
    } catch (err) { detail = err.message; console.log('  ERROR: ' + err.message); }
    if (errors.length) { errors.slice(0,3).forEach(e => console.log('    ERR: ' + e)); if (status==='PASS') { status='WARN'; detail += ' | console errors'; } }
    results.push({ name: 'epub-to-pdf', status, detail });
    await page.close();
  }

  await browser.close();

  console.log('\n========== BATCH 3 TEST RESULTS ==========');
  let pass = 0, fail = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.name.padEnd(22)} ${r.status} — ${r.detail}`);
    if (r.status === 'PASS') pass++; else fail++;
  });
  console.log(`\nTotal: ${pass} PASS, ${fail} FAIL/WARN out of ${results.length}`);
  process.exit(fail > 0 ? 1 : 0);
}

run().catch(e => { console.error('Fatal:', e); process.exit(2); });
