// Targeted live check: gif-maker + pdf-to-images page state + interaction
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');
const TEST_PDF = path.join(__dirname, '..', '_test_files', 'test_sample.pdf');
const OUT_DIR = path.join(__dirname, 'output_live2');
fs.mkdirSync(OUT_DIR, { recursive: true });

async function dumpState(page, label) {
  const s = await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll('input')).map(i => ({ id: i.id, type: i.type, hidden: i.type === 'hidden', display: getComputedStyle(i).display }));
    const btns = Array.from(document.querySelectorAll('button')).map(b => ({ text: (b.textContent || '').trim().substring(0, 40), id: b.id, disabled: b.disabled }));
    const st = document.querySelector('#status, #statusText, .status, #progressText');
    return { inputs, btns, status: st ? st.textContent : '', bodyLen: document.body.innerHTML.length };
  });
  console.log(`[${label}] inputs=${JSON.stringify(s.inputs).substring(0, 300)}`);
  console.log(`[${label}] buttons=${JSON.stringify(s.btns).substring(0, 400)}`);
  console.log(`[${label}] status="${s.status}" bodyLen=${s.bodyLen}`);
  return s;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const [slug, file] of [['gif-maker', TEST_IMAGE], ['pdf-to-images', TEST_PDF]]) {
    const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1400, height: 950 } });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().substring(0, 150)); });
    page.on('pageerror', e => errors.push('PAGEERR: ' + e.message.substring(0, 150)));
    page.on('requestfailed', r => errors.push('REQFAIL: ' + r.url().substring(0, 120) + ' ' + (r.failure() || {}).errorText));

    console.log(`\n=== LIVE ${slug} ===`);
    try {
      await page.goto(`https://smartimgkit.com/workflows/${slug}.html`, { waitUntil: 'domcontentloaded', timeout: 40000 });
      await page.waitForTimeout(5000);
      await dumpState(page, 'after-load');

      const fi = page.locator('input[type="file"]').first();
      const cnt = await fi.count().catch(() => -1);
      console.log(`file input count: ${cnt}`);
      if (cnt > 0) {
        await fi.setInputFiles(file);
        await page.waitForTimeout(2500);
        await dumpState(page, 'after-upload');

        // find generate/convert button
        const btn = page.locator('button:has-text("Generate"), button:has-text("Convert"), #generateBtn, #convertBtn, button:has-text("Create")').first();
        const bcnt = await btn.count().catch(() => -1);
        console.log(`action button count: ${bcnt}`);
        if (bcnt > 0) {
          const dlP = page.waitForEvent('download', { timeout: 60000 }).catch(() => null);
          await btn.click({ timeout: 8000 }).catch(e => console.log('click err', e.message.substring(0, 80)));
          const t0 = Date.now();
          let done = false;
          while (Date.now() - t0 < 60000 && !done) {
            const dl = await Promise.race([dlP.then(d => ({ dl: d })), new Promise(r => setTimeout(() => r({ dl: null }), 2500))]);
            if (dl.dl) {
              const savePath = path.join(OUT_DIR, `${slug}-out`);
              await dl.dl.saveAs(savePath);
              console.log(`DOWNLOAD: ${dl.dl.suggestedFilename()} (${fs.existsSync(savePath) ? fs.statSync(savePath).size : 0}B)`);
              fs.unlinkSync(savePath);
              done = true;
              break;
            }
            const s = await page.evaluate(() => ({
              st: (document.querySelector('#status, #statusText, .status, #progressText') || {}).textContent || '',
              imgs: Array.from(document.querySelectorAll('img')).filter(i => i.src && (i.src.startsWith('data:') || i.src.startsWith('blob:'))).length
            }));
            if (s.st.includes('✅') || s.st.includes('Done') || s.imgs > 2) { console.log(`STATUS: "${s.st}" imgs=${s.imgs}`); done = true; break; }
            await page.waitForTimeout(2000);
          }
          if (!done) console.log('TIMEOUT waiting for output');
          await dumpState(page, 'after-process');
        }
      }
    } catch (e) {
      console.log('ERROR: ' + e.message.substring(0, 200));
    }
    console.log('Errors:');
    errors.slice(0, 8).forEach(e => console.log('  ' + e));
    await ctx.close();
  }
  await browser.close();
  process.exit(0);
})();
