// Diagnostic: pdf-rotate, pdf-delete-pages, pdf-extract-pages real usability
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_PDF = path.join(__dirname, '..', '_test_files', 'test_sample.pdf');
const OUT_DIR = path.join(__dirname, 'output_pdfdiag');
fs.mkdirSync(OUT_DIR, { recursive: true });

async function testOne(slug, setup) {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1400, height: 950 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 150)); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 150)));
  page.on('dialog', async d => { errors.push('DIALOG: ' + d.message().substring(0, 100)); await d.accept().catch(() => {}); });

  console.log(`\n=== ${slug} ===`);
  let status = 'FAIL', detail = '';
  try {
    await page.goto(`http://localhost:8000/tools/${slug}.html`, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(3000);
    const fi = page.locator('#fileInput').first();
    await fi.setInputFiles(TEST_PDF);
    await page.waitForTimeout(4000); // wait pdf render

    if (setup) await setup(page);

    const btn = page.locator('#processBtn, #applyBtn').first();
    console.log('btn count:', await btn.count().then(c => c > 0), 'disabled:', await btn.isDisabled().catch(() => '?'));
    const box = await btn.boundingBox();
    console.log('btn box:', JSON.stringify(box));
    // check what element is at button center
    const atBtn = await page.evaluate(({ x, y }) => {
      const el = document.elementFromPoint(x, y);
      return el ? el.id + '.' + el.className : 'none';
    }, { x: box.x + box.width / 2, y: box.y + box.height / 2 });
    console.log('element at button center:', atBtn);

    const dlP = page.waitForEvent('download', { timeout: 40000 }).catch(() => null);
    await btn.click({ timeout: 5000 }).catch(e => console.log('click err:', e.message.substring(0, 80)));
    const dl = await Promise.race([dlP, new Promise(r => setTimeout(() => r(null), 40000))]);
    if (dl) {
      const savePath = path.join(OUT_DIR, slug + '-out');
      await dl.saveAs(savePath);
      const size = fs.existsSync(savePath) ? fs.statSync(savePath).size : 0;
      const buf = fs.readFileSync(savePath);
      const magic = buf.slice(0, 5).toString('latin1');
      console.log(`DOWNLOAD: ${dl.suggestedFilename()} (${size}B) magic=${magic}`);
      fs.unlinkSync(savePath);
      status = magic.startsWith('%PDF') ? 'PASS' : 'FAIL';
      detail = `dl=${dl.suggestedFilename()} ${size}B magic=${magic}`;
    } else {
      const st = await page.evaluate(() => {
        const s = document.querySelector('#statusSection, #status, .status-text');
        return s ? s.textContent.trim().substring(0, 150) : '(no status el)';
      });
      detail = 'no download. status="' + st + '"';
      console.log('NO DOWNLOAD. status=' + st);
    }
  } catch (e) {
    detail = e.message.substring(0, 200);
    console.log('ERROR:', detail);
  }
  const realErrors = errors.filter(e => !/adsbygoogle|googlesyndication|recaptcha/i.test(e));
  if (realErrors.length) { console.log('Console errors:', realErrors.slice(0, 4)); if (status === 'PASS') status = 'WARN'; }
  await browser.close();
  return { slug, status, detail, errors: realErrors.slice(0, 5) };
}

(async () => {
  const results = [];
  results.push(await testOne('pdf-rotate', null));
  results.push(await testOne('pdf-delete-pages', async (page) => {
    await page.fill('#delPages', '1');
    await page.waitForTimeout(300);
  }));
  results.push(await testOne('pdf-extract-pages', async (page) => {
    await page.fill('#extPages', '1');
    await page.waitForTimeout(300);
  }));
  console.log('\n========== PDF DIAG RESULTS ==========');
  results.forEach(r => console.log(`${r.status === 'PASS' ? '✅' : r.status === 'WARN' ? '⚠️' : '❌'} ${r.slug} — ${r.detail}`));
  process.exit(0);
})();
