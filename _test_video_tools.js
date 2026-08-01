const { chromium } = require('playwright');
const path = require('path');
const TEST_VIDEO = path.join(__dirname, 'test-video.mp4');
const BASE_URL = 'http://localhost:8000';

const videoTools = [
  'video-compressor', 'video-crop', 'video-rotate',
  'video-speed', 'video-to-frames', 'video-to-gif', 'video-to-mp3'
];

(async () => {
  console.log('='.repeat(60));
  console.log('ALL 7 VIDEO TOOLS E2E TEST (with actual video file)');
  console.log('Test video: ' + TEST_VIDEO);
  console.log('='.repeat(60));
  const browser = await chromium.launch({ headless: true });
  for (const slug of videoTools) {
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    page.on('console', msg => { if (msg.type() === 'error') errors.push('[C] ' + msg.text().substring(0, 200)); });
    page.on('pageerror', err => errors.push('[P] ' + err.message.substring(0, 200)));
    page.on('dialog', async dialog => { errors.push('[D] ' + dialog.type() + ': ' + dialog.message().substring(0, 150)); await dialog.accept().catch(()=>{}); });

    let uploaded = false, ranProcess = false;
    try {
      await page.goto(`${BASE_URL}/tools/${slug}.html`, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(800);
      const fi = page.locator('input[type="file"]').first();
      if (await fi.count().then(c => c > 0)) {
        try { await fi.setInputFiles(TEST_VIDEO); uploaded = true; await page.waitForTimeout(2000); } catch(e) {}
      }
      // Try to click main process button
      if (uploaded) {
        const btnSels = ['#processBtn', '#compressBtn', '#convertBtn', '#runBtn', '#generateBtn',
          'button:has-text("Compress")', 'button:has-text("Convert")', 'button:has-text("Process")',
          'button:has-text("Run")', 'button:has-text("Generate")', 'button.btn-primary'];
        for (const sel of btnSels) {
          const btn = page.locator(sel).first();
          if (await btn.count().then(c => c > 0)) {
            const isDisabled = await btn.isDisabled().catch(() => true);
            if (!isDisabled) {
              try { await Promise.race([btn.click({ timeout: 5000 }), new Promise(r => setTimeout(r, 5000))]); ranProcess = true; await page.waitForTimeout(2000); } catch(e) {}
              break;
            }
          }
        }
      }
    } catch(e) { errors.push('[F] ' + e.message.substring(0, 100)); }

    const status = errors.length === 0 ? '\u2705' : '\u274c';
    console.log(`${status} ${slug.padEnd(20)} | up:${uploaded?'\u2705':'\u274c'} run:${ranProcess?'\u2705':'\u274c'} | err:${errors.length}`);
    errors.forEach(e => console.log(`   ${e}`));
    await context.close();
  }
  await browser.close();
})();
