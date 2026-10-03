// 线上部署后功能实测：gif-maker / image-rotator / before-after-comparison
const { chromium } = require('playwright');
const path = require('path');
const TEST_IMAGE = path.join(__dirname, '..', 'test-image.jpg');

async function run() {
  const browser = await chromium.launch();
  let allOk = true;

  async function test(name, fn) {
    const page = await browser.newPage();
    const pageErrors = [];
    page.on('pageerror', (e) => pageErrors.push(e.message));
    // 拦截被墙外部资源（广告/字体/统计），避免页面加载卡死
    await page.route(/fonts\.(googleapis|gstatic)\.com|pagead2\.googlesyndication\.com|googletagmanager\.com|google-analytics\.com|doubleclick\.net/, (route) => route.abort());
    await page.goto(name, { waitUntil: 'domcontentloaded', timeout: 45000 });
    let pass = false, note = '';
    try {
      const r = await fn(page);
      pass = r.pass; note = r.note;
    } catch (e) { note = 'EXCEPTION: ' + e.message; }
    const critical = pageErrors.filter(e => /blob is not defined|SyntaxError|Worker|gif\.worker|Identifier/.test(e));
    const ok = pass && critical.length === 0;
    allOk = allOk && ok;
    console.log((ok ? 'PASS' : 'FAIL') + ' | ' + name + ' | ' + note + (critical.length ? ' | pageErrors: ' + critical.join(' ;; ') : ''));
    await page.close();
  }

  await test('https://smartimgkit.com/workflows/gif-maker.html', async (page) => {
    await page.setInputFiles('#fileInput', [TEST_IMAGE, TEST_IMAGE]);
    await page.waitForTimeout(1500);
    const frames = await page.evaluate(() => document.querySelectorAll('#frames img').length);
    await page.click('#genBtn');
    const t0 = Date.now();
    let dlVisible = false;
    while (Date.now() - t0 < 90000) {
      dlVisible = await page.evaluate(() => {
        const b = document.querySelector('#dlBtn');
        return b ? getComputedStyle(b).display !== 'none' : false;
      });
      if (dlVisible) break;
      await page.waitForTimeout(1000);
    }
    const gifImg = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('#preview img'));
      return imgs.some(i => i.src && (i.src.startsWith('data:image/gif') || i.src.startsWith('blob:')));
    });
    return { pass: frames >= 2 && dlVisible && gifImg, note: 'frames=' + frames + ' dlVisible=' + dlVisible + ' gifImg=' + gifImg + ' elapsed=' + ((Date.now() - t0) / 1000).toFixed(1) + 's' };
  });

  await test('https://smartimgkit.com/tools/image-rotator.html', async (page) => {
    await page.setInputFiles('#fileInput', TEST_IMAGE);
    await page.waitForTimeout(1500);
    await page.click('#rotateRightBtn');
    await page.waitForTimeout(800);
    const dlPromise = page.waitForEvent('download', { timeout: 20000 }).then(d => d.suggestedFilename()).catch(() => null);
    await page.click('#downloadBtn');
    const dl = await dlPromise;
    await page.waitForTimeout(800);
    const disabled = await page.$eval('#downloadBtn', b => b.disabled);
    return { pass: !!dl && !disabled, note: 'dl=' + dl + ' btnDisabled=' + disabled };
  });

  await test('https://smartimgkit.com/workflows/before-after-comparison.html', async (page) => {
    await page.setInputFiles('#fileBefore', TEST_IMAGE);
    await page.setInputFiles('#fileAfter', TEST_IMAGE);
    await page.waitForTimeout(1200);
    const enabled = await page.$eval('#runBtn', b => !b.disabled);
    const dlPromise = page.waitForEvent('download', { timeout: 25000 }).then(d => d.suggestedFilename()).catch(() => null);
    await page.click('#runBtn');
    const dl = await dlPromise;
    await page.waitForTimeout(1500);
    const imgCount = await page.evaluate(() => document.querySelectorAll('#previewWrap img[src^="blob:"]').length);
    return { pass: enabled && !!dl && imgCount >= 1, note: 'runEnabled=' + enabled + ' dl=' + dl + ' previewImg=' + imgCount };
  });

  await browser.close();
  console.log(allOk ? '=== LIVE DEPLOY ALL OK ===' : '=== LIVE DEPLOY FAILED ===');
  process.exit(allOk ? 0 : 1);
}
run().catch(e => { console.error('FATAL', e); process.exit(2); });
