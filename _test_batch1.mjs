// Batch 1 verification: upload real files to each tool, verify download output.
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BASE = 'http://localhost:8000/tools';  // append .html for local dev server
const TEST_DIR = 'E:\\网站项目\\smartimgkit\\_test_files';
const OUT_DIR = 'E:\\网站项目\\smartimgkit\\_test_files\\output';
fs.mkdirSync(OUT_DIR, { recursive: true });

const tests = [
  { name: 'pdf-to-word', url: `${BASE}/pdf-to-word.html`, file: 'test_sample.pdf', expectExt: '.docx', btnText: 'Convert to Word' },
  { name: 'pdf-to-excel', url: `${BASE}/pdf-to-excel.html`, file: 'test_sample.pdf', expectExt: '.xlsx', btnText: 'Convert to Excel' },
  { name: 'pdf-to-ppt', url: `${BASE}/pdf-to-ppt.html`, file: 'test_sample.pdf', expectExt: '.pptx', btnText: 'Convert to PPT' },
  { name: 'word-to-pdf', url: `${BASE}/word-to-pdf.html`, file: 'test_sample.docx', expectExt: '.pdf', btnText: 'Convert to PDF' },
  { name: 'excel-to-pdf', url: `${BASE}/excel-to-pdf.html`, file: 'test_sample.xlsx', expectExt: '.pdf', btnText: 'Convert to PDF' },
];

function checkFileKind(filePath, ext) {
  if (!fs.existsSync(filePath)) return { ok: false, reason: 'file not found' };
  const stat = fs.statSync(filePath);
  if (stat.size < 100) return { ok: false, reason: `file too small (${stat.size} bytes)` };
  const buf = fs.readFileSync(filePath);
  // Check magic bytes
  if (ext === '.pdf') {
    const head = buf.slice(0, 5).toString('latin1');
    return { ok: head.startsWith('%PDF'), reason: head.startsWith('%PDF') ? `valid PDF (${stat.size} bytes)` : `bad magic: ${head}` };
  }
  if (ext === '.docx' || ext === '.xlsx' || ext === '.pptx') {
    // ZIP-based: starts with PK
    const head = buf.slice(0, 2).toString('latin1');
    const isZip = head === 'PK';
    return { ok: isZip, reason: isZip ? `valid OOXML/ZIP (${stat.size} bytes)` : `bad magic: ${head}` };
  }
  return { ok: true, reason: `${stat.size} bytes` };
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const results = [];

  for (const t of tests) {
    const page = await context.newPage();
    const consoleErrors = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', err => consoleErrors.push('PAGEERROR: ' + err.message));

    console.log(`\n=== Testing ${t.name} ===`);
    let status = 'FAIL', detail = '';
    try {
      await page.goto(t.url, { waitUntil: 'networkidle', timeout: 30000 });
      // Check libraries loaded
      const libsOk = await page.evaluate(() => ({
        pdfjs: typeof pdfjsLib !== 'undefined',
        docx: typeof docx !== 'undefined',
        xlsx: typeof XLSX !== 'undefined',
        pptx: typeof PptxGenJS !== 'undefined',
        jspdf: typeof jspdf !== 'undefined',
        jszip: typeof JSZip !== 'undefined',
        triggerDownload: typeof SmartImgKit !== 'undefined' && typeof SmartImgKit._triggerDownload === 'function'
      }));
      console.log('  Libraries:', JSON.stringify(libsOk));

      const filePath = path.join(TEST_DIR, t.file);
      // Set file on the hidden input
      const fileInput = page.locator('#fileInput');
      await fileInput.setInputFiles(filePath);
      // Wait for the convert button to be enabled
      await page.waitForTimeout(500);
      const btnEnabled = await page.isEnabled(`#convertBtn`);
      if (!btnEnabled) throw new Error('Convert button not enabled after file upload');

      // Set up download handler BEFORE clicking
      const downloadPromise = page.waitForEvent('download', { timeout: 60000 });
      await page.click(`#convertBtn`);

      // Wait for status to show done or download
      const download = await downloadPromise;
      const suggestedName = download.suggestedFilename();
      const savePath = path.join(OUT_DIR, `${t.name}${t.expectExt}`);
      await download.saveAs(savePath);

      // Verify file
      const check = checkFileKind(savePath, t.expectExt);
      const hasCorrectExt = suggestedName.toLowerCase().endsWith(t.expectExt);

      if (check.ok && hasCorrectExt) {
        status = 'PASS';
        detail = `downloaded "${suggestedName}" — ${check.reason}`;
      } else {
        status = 'FAIL';
        detail = `suggested="${suggestedName}" ext_ok=${hasCorrectExt} check=${check.reason}`;
      }
      console.log(`  Download: ${suggestedName}`);
      console.log(`  Saved to: ${savePath}`);
      console.log(`  Verify: ${check.reason}`);
    } catch (err) {
      status = 'FAIL';
      detail = err.message;
      console.log(`  ERROR: ${err.message}`);
    }

    if (consoleErrors.length) {
      console.log(`  Console errors (${consoleErrors.length}):`);
      consoleErrors.slice(0, 5).forEach(e => console.log('    ' + e));
      if (status === 'PASS') { status = 'WARN'; detail += ' | has console errors'; }
    }

    results.push({ name: t.name, status, detail });
    await page.close();
  }

  await browser.close();

  console.log('\n========== BATCH 1 TEST RESULTS ==========');
  let pass = 0, fail = 0;
  results.forEach(r => {
    const icon = r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌';
    console.log(`${icon} ${r.name.padEnd(16)} ${r.status} — ${r.detail}`);
    if (r.status === 'PASS') pass++; else fail++;
  });
  console.log(`\nTotal: ${pass} PASS, ${fail} FAIL/WARN out of ${results.length}`);
  process.exit(fail > 0 ? 1 : 0);
}

run().catch(e => { console.error('Fatal:', e); process.exit(2); });
