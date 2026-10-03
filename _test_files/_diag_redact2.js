// Diagnostic v2 for pdf-redact: global event capture + overlay detection
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.log('[PAGEERR]', e.message.substring(0, 200)));

  try {
    await page.goto('http://localhost:8000/tools/pdf-redact.html', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(2500);
    await page.setInputFiles('#fileInput', path.join(__dirname, '..', '_test_files', 'test_sample.pdf'));
    await page.waitForSelector('#redactArea', { state: 'visible', timeout: 15000 });
    await page.waitForTimeout(1500);

    const canvas = page.locator('#pageCanvas');
    const box = await canvas.boundingBox();
    console.log('Canvas box:', JSON.stringify(box));

    // Global capture at document level
    await page.evaluate(() => {
      window.__evts = [];
      ['mousedown', 'mousemove', 'mouseup', 'pointerdown', 'pointerup', 'click'].forEach(ev => {
        document.addEventListener(ev, (e) => {
          const t = e.target;
          window.__evts.push(ev + '@' + Math.round(e.clientX) + ',' + Math.round(e.clientY) + ' -> ' + (t.id || t.tagName + '.' + String(t.className).substring(0, 40)));
        }, true);
      });
      // Check for fixed/absolute overlays
      window.__overlays = [];
      document.querySelectorAll('*').forEach(el => {
        const st = getComputedStyle(el);
        if ((st.position === 'fixed' || st.position === 'absolute') && st.display !== 'none') {
          const r = el.getBoundingClientRect();
          if (r.width > 0 && r.height > 0 && (st.zIndex >= 5 || st.position === 'fixed')) {
            window.__overlays.push(el.tagName + '#' + el.id + '.' + String(el.className).substring(0, 30) + ' pos=' + st.position + ' z=' + st.zIndex + ' rect=' + Math.round(r.x) + ',' + Math.round(r.y) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
          }
        }
      });
    });

    const overlays = await page.evaluate(() => window.__overlays);
    console.log('Overlays (fixed/absolute):', JSON.stringify(overlays, null, 0).substring(0, 800));

    await page.mouse.move(box.x + 50, box.y + 60);
    await page.mouse.down();
    await page.mouse.move(box.x + 250, box.y + 140, { steps: 12 });
    await page.mouse.up();
    await page.waitForTimeout(600);

    const evts = await page.evaluate(() => window.__evts);
    console.log('Document events:');
    evts.forEach(e => console.log('  ' + e));

    const listText = await page.locator('#redactionList').textContent();
    console.log('Redaction list:', listText.trim().substring(0, 100));

    // Also test drag within the top-left safe area, smaller drag
    await page.evaluate(() => { window.__evts = []; });
    await page.mouse.move(box.x + 20, box.y + 20);
    await page.mouse.down();
    await page.mouse.move(box.x + 120, box.y + 80, { steps: 8 });
    await page.mouse.up();
    await page.waitForTimeout(500);
    const evts2 = await page.evaluate(() => window.__evts);
    console.log('Second drag events:');
    evts2.forEach(e => console.log('  ' + e));
    const listText2 = await page.locator('#redactionList').textContent();
    console.log('Redaction list after 2nd drag:', listText2.trim().substring(0, 100));
  } catch (e) {
    console.log('ERROR:', e.message.substring(0, 300));
  }
  await browser.close();
})();
