// Verify enrichment: check sections exist + screenshot + functional smoke test.
import { chromium } from 'playwright';
import fs from 'fs';

const BASE = 'http://localhost:8000/tools';
const OUT = 'E:\\网站项目\\smartimgkit\\_test_files\\enrich_screenshots';
fs.mkdirSync(OUT, { recursive: true });

const samples = ['pdf-to-excel', 'background-remover', 'compressor', 'html-to-pdf'];

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  let allOk = true;
  for (const slug of samples) {
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    console.log(`\n=== ${slug} ===`);
    await page.goto(`${BASE}/${slug}.html`, { waitUntil: 'networkidle', timeout: 30000 });
    // Check sections exist
    const checks = {
      'selling-points': await page.locator('.selling-points').count(),
      'feature-narrative': await page.locator('.feature-narrative').count(),
      'features-grid': await page.locator('.features-grid').count(),
      'trust-badges': await page.locator('.trust-badges').count(),
    };
    let sectionsOk = true;
    for (const [name, count] of Object.entries(checks)) {
      const ok = count > 0;
      if (!ok) sectionsOk = false;
      console.log(`  ${ok ? '✅' : '❌'} ${name}: ${count}`);
    }
    // Count FAQ items (should be > 3 now)
    const faqCount = await page.locator('.faq-item').count();
    console.log(`  ${faqCount >= 5 ? '✅' : '❌'} FAQ items: ${faqCount} (expected 5+)`);
    if (faqCount < 5) sectionsOk = false;
    // Screenshot
    await page.screenshot({ path: `${OUT}/${slug}.png`, fullPage: true });
    console.log(`  📸 screenshot saved`);
    if (errors.length) { console.log(`  ⚠️ page errors: ${errors.slice(0,2).join('; ')}`); allOk = false; }
    if (!sectionsOk) allOk = false;
    await page.close();
  }

  // Functional smoke: pdf-to-excel still converts
  console.log('\n=== Functional smoke: pdf-to-excel ===');
  const page = await context.newPage();
  await page.goto(`${BASE}/pdf-to-excel.html`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.setInputFiles('#fileInput', 'E:\\网站项目\\smartimgkit\\_test_files\\test_sample.pdf');
  const dl = page.waitForEvent('download', { timeout: 60000 });
  await page.click('#convertBtn');
  const download = await dl;
  console.log(`  ✅ Conversion still works: ${download.suggestedFilename()}`);
  await page.close();

  await browser.close();
  console.log(`\n${allOk ? '✅ All enrichment checks passed' : '⚠️ Some checks failed'}`);
  process.exit(allOk ? 0 : 1);
}
run().catch(e => { console.error('Fatal:', e); process.exit(2); });
