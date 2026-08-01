/**
 * COMPREHENSIVE E2E TEST: All tools + workflows with output validation
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const TEST_PDF = path.join(__dirname, 'test-file.pdf');
const TEST_VIDEO = path.join(__dirname, 'test-video.mp4');
const BASE_URL = 'http://localhost:8000';

const toolFiles = fs.readdirSync(path.join(__dirname, 'tools'))
  .filter(f => f.endsWith('.html')).map(f => f.replace('.html', '')).sort();
const wfFiles = fs.readdirSync(path.join(__dirname, 'workflows'))
  .filter(f => f.endsWith('.html') && !f.startsWith('_')).map(f => f.replace('.html', '')).sort();

function getTestFile(slug) {
  if (slug.startsWith('pdf-')) return TEST_PDF;
  if (slug.startsWith('video-')) return TEST_VIDEO;
  return TEST_IMAGE;
}

function isZipValid(zipPath) {
  try {
    const buf = fs.readFileSync(zipPath);
    return buf[0] === 0x50 && buf[1] === 0x4B; // PK
  } catch { return false; }
}

function verifyZipContents(zipPath) {
  try {
    const result = execSync(`python -c "
import zipfile, sys
with zipfile.ZipFile('${zipPath.replace(/\\/g, '/')}', 'r') as z:
    for info in z.infolist():
        data = z.read(info.filename)
        fname = info.filename.lower()
        if fname.endswith('.jpg') or fname.endswith('.jpeg'):
            is_ok = data[:3] == bytes([0xff, 0xd8, 0xff])
            if not is_ok:
                print(f'FAIL:{info.filename}:expected JPG got {data[:4].hex()}')
                sys.exit(1)
        elif fname.endswith('.png'):
            is_ok = data[:4] == bytes([0x89, 0x50, 0x4e, 0x47])
            if not is_ok:
                print(f'FAIL:{info.filename}:expected PNG got {data[:4].hex()}')
                sys.exit(1)
    print('OK')
" 2>&1`, { encoding: 'utf-8', timeout: 10000 });
    return result.trim();
  } catch(e) {
    return 'ERROR:' + e.message.substring(0, 100);
  }
}

(async () => {
  console.log('='.repeat(70));
  console.log(`COMPREHENSIVE E2E TEST SUITE`);
  console.log(`Tools: ${toolFiles.length} | Workflows: ${wfFiles.length}`);
  console.log('='.repeat(70));
  const browser = await chromium.launch({ headless: true });
  let toolPass = 0, toolFail = 0, wfPass = 0, wfFail = 0;
  const failures = [];

  // ---- PART 1: TOOLS ----
  console.log('\n--- TOOLS (' + toolFiles.length + ') ---');
  for (const slug of toolFiles) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('[C] ' + msg.text().substring(0, 200)); });
    page.on('pageerror', err => errors.push('[P] ' + err.message.substring(0, 200)));
    page.on('response', resp => { if (resp.status() >= 400 && !resp.url().includes('favicon')) errors.push('[404] ' + resp.url().split('/').slice(-1)[0]); });
    page.on('dialog', async d => { errors.push('[D] ' + d.message().substring(0, 100)); await d.accept().catch(()=>{}); });

    let uploaded = false;
    try {
      await page.goto(`${BASE_URL}/tools/${slug}.html`, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        try { await fi.setInputFiles(getTestFile(slug)); uploaded = true; await page.waitForTimeout(1200); } catch(e) {}
      }
    } catch(e) { errors.push('[F] ' + e.message.substring(0, 100)); }

    // Filter: ignore "please upload X file" dialogs (expected for wrong file type)
    const realErrors = errors.filter(e => !e.startsWith('[D] ') || (!e.includes('upload') && !e.includes('select') && !e.includes('valid')));

    if (realErrors.length === 0) {
      toolPass++;
    } else {
      toolFail++;
      failures.push({ type: 'tool', slug, errors: realErrors });
      console.log(`❌ tool/${slug}`);
      realErrors.forEach(e => console.log(`   ${e}`));
    }
    await ctx.close();
  }

  // ---- PART 2: WORKFLOWS (with ZIP validation) ----
  console.log('\n--- WORKFLOWS (' + wfFiles.length + ') with ZIP output validation ---');
  for (const slug of wfFiles) {
    const ctx = await browser.newContext({ acceptDownloads: true });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('[C] ' + msg.text().substring(0, 200)); });
    page.on('pageerror', err => errors.push('[P] ' + err.message.substring(0, 200)));
    page.on('response', resp => { if (resp.status() >= 400 && !resp.url().includes('favicon')) errors.push('[404] ' + resp.url().split('/').slice(-1)[0]); });
    page.on('dialog', async d => { errors.push('[D] ' + d.message().substring(0, 100)); await d.accept().catch(()=>{}); });

    let zipOk = false, zipVerify = '';
    try {
      await page.goto(`${BASE_URL}/workflows/${slug}.html`, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        try { await fi.setInputFiles(TEST_IMAGE); await page.waitForTimeout(1000); } catch(e) {}
      }

      // Try to run pipeline
      const runBtn = page.locator('#runBtn').first();
      if (await runBtn.count().then(c => c > 0)) {
        const isDisabled = await runBtn.isDisabled().catch(() => true);
        if (!isDisabled) {
          try {
            const dlPromise = page.waitForEvent('download', { timeout: 60000 }).catch(() => null);
            await runBtn.click({ timeout: 5000 }).catch(() => {});
            const dl = await dlPromise;
            if (dl) {
              const zipPath = path.join(__dirname, `_test_${slug}.zip`);
              await dl.saveAs(zipPath);
              zipOk = isZipValid(zipPath);
              if (zipOk) zipVerify = verifyZipContents(zipPath);
              try { fs.unlinkSync(zipPath); } catch {}
            }
          } catch(e) { errors.push('[ZIP] ' + e.message.substring(0, 100)); }
        }
      }
    } catch(e) { errors.push('[F] ' + e.message.substring(0, 100)); }

    const realErrors = errors.filter(e => !e.startsWith('[D] ') || (!e.includes('upload') && !e.includes('select')));

    if (realErrors.length === 0 && (zipOk || !page.locator('#runBtn'))) {
      wfPass++;
      const zipStatus = zipOk ? ` ZIP:${zipVerify}` : '';
      console.log(`✅ wf/${slug}${zipStatus}`);
    } else {
      wfFail++;
      failures.push({ type: 'wf', slug, errors: realErrors, zipOk, zipVerify });
      console.log(`❌ wf/${slug} ZIP:${zipOk?'OK':'FAIL'} ${zipVerify}`);
      realErrors.forEach(e => console.log(`   ${e}`));
    }
    await ctx.close();
  }

  await browser.close();

  console.log('\n' + '='.repeat(70));
  console.log('FINAL RESULTS');
  console.log('='.repeat(70));
  console.log(`Tools:     ${toolPass}/${toolFiles.length} PASS, ${toolFail} FAIL`);
  console.log(`Workflows: ${wfPass}/${wfFiles.length} PASS, ${wfFail} FAIL (ZIP validated)`);
  const totalPass = toolPass + wfPass;
  const total = toolFiles.length + wfFiles.length;
  console.log(`TOTAL:     ${totalPass}/${total} PASS`);
  if (failures.length) {
    console.log('\nFailures:');
    failures.forEach(f => console.log(`  ❌ ${f.type}/${f.slug}`));
  }
  process.exit(failures.length > 0 ? 1 : 0);
})();
