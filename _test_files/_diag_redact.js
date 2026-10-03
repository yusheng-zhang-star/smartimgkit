// Diagnostic for pdf-redact drag interaction
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ acceptDownloads: true });
  const page = await ctx.newPage();
  page.on('console', m => { if (m.type() === 'error') console.log('[CONSOLE]', m.text().substring(0, 200)); });
  page.on('pageerror', e => console.log('[PAGEERR]', e.message.substring(0, 200)));

  try {
    await page.goto('http://localhost:8000/tools/pdf-redact.html', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(2500);
    await page.setInputFiles('#fileInput', path.join(__dirname, '..', '_test_files', 'test_sample.pdf'));
    await page.waitForSelector('#redactArea', { state: 'visible', timeout: 15000 });
    await page.waitForTimeout(1500);

    const canvas = page.locator('#pageCanvas');
    const box = await canvas.boundingBox();
    console.log('Canvas boundingBox:', JSON.stringify(box));
    const props = await page.evaluate(() => {
      const c = document.getElementById('pageCanvas');
      const st = getComputedStyle(c);
      return { cssW: st.width, cssH: st.height, attrW: c.width, attrH: c.height, parentRect: c.parentElement ? c.parentElement.getBoundingClientRect().width : 0, display: st.display, pointerEvents: st.pointerEvents };
    });
    console.log('Canvas props:', JSON.stringify(props));

    // Check element at the drag start point
    const elAt = await page.evaluate(({ x, y }) => {
      const el = document.elementFromPoint(x, y);
      return el ? (el.id || el.tagName + '.' + el.className) : 'none';
    }, { x: box.x + 50, y: box.y + 60 });
    console.log('Element at drag start:', elAt);

    // Attach listeners to trace events
    await page.evaluate(() => {
      const c = document.getElementById('pageCanvas');
      window.__events = [];
      ['mousedown', 'mousemove', 'mouseup', 'pointerdown', 'pointerup'].forEach(ev => {
        c.addEventListener(ev, (e) => window.__events.push(ev + '@' + Math.round(e.clientX) + ',' + Math.round(e.clientY)));
      });
    });

    await page.mouse.move(box.x + 50, box.y + 60);
    await page.mouse.down();
    await page.mouse.move(box.x + 250, box.y + 140, { steps: 8 });
    await page.mouse.up();
    await page.waitForTimeout(500);

    const events = await page.evaluate(() => window.__events);
    console.log('Events captured:', JSON.stringify(events));

    const listText = await page.locator('#redactionList').textContent();
    console.log('Redaction list:', listText.trim().substring(0, 120));
  } catch (e) {
    console.log('ERROR:', e.message.substring(0, 300));
  }
  await browser.close();
})();
