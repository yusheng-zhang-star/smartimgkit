/**
 * Full site tool test: ALL 85 tools with actual file uploads
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const TEST_PDF = path.join(__dirname, 'test-file.pdf');
const TEST_TXT = path.join(__dirname, 'test-file.txt');
const BASE_URL = 'http://localhost:8000';

// Get all tool pages
const toolFiles = fs.readdirSync(path.join(__dirname, 'tools'))
  .filter(f => f.endsWith('.html'))
  .map(f => f.replace('.html', ''))
  .sort();

// Categorize tools
function getToolType(slug) {
  if (slug.startsWith('pdf-')) return 'pdf';
  if (slug.startsWith('video-')) return 'video';
  if (['ocr'].includes(slug)) return 'image';
  if (['qr-code-generator', 'password-generator', 'uuid-generator',
       'json-formatter', 'base64', 'url-encoder', 'html-encoder',
       'case-converter', 'word-counter', 'text-sorter', 'text-diff',
       'text-find-replace', 'regex-tester'].includes(slug)) return 'text';
  return 'image';
}

function getTestFile(slug) {
  const type = getToolType(slug);
  if (type === 'pdf') return TEST_PDF;
  if (type === 'video') return TEST_IMAGE; // No video test file, try image
  return TEST_IMAGE;
}

(async () => {
  console.log('='.repeat(70));
  console.log('FULL SITE: ALL ' + toolFiles.length + ' TOOLS E2E TEST');
  console.log('='.repeat(70));

  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (let i = 0; i < toolFiles.length; i++) {
    const slug = toolFiles[i];
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const url = `${BASE_URL}/tools/${slug}.html`;
    const type = getToolType(slug);
    const errors = [];

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(`[C] ${msg.text().substring(0, 200)}`);
    });
    page.on('pageerror', err => errors.push(`[P] ${err.message.substring(0, 200)}`));
    page.on('dialog', async dialog => {
      errors.push(`[D] ${dialog.type()}: ${dialog.message().substring(0, 150)}`);
      await dialog.accept().catch(() => {});
    });

    let loadOK = false, uploaded = false, ranProcess = false;

    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      loadOK = resp && resp.status() < 400;
      await page.waitForTimeout(800);

      // For text-only tools (no file upload), just test page loads OK
      if (type !== 'text') {
        const fileInput = page.locator('input[type="file"]').first();
        if (await fileInput.count().then(c => c > 0)) {
          try {
            await fileInput.setInputFiles(getTestFile(slug));
            uploaded = true;
            await page.waitForTimeout(1000);
          } catch(e) {}
        }

        // Try to click main button
        if (uploaded || type === 'text') {
          const btnSelectors = [
            '#processBtn', '#compressBtn', '#convertBtn', '#applyBtn',
            '#runBtn', '#generateBtn', '#downloadBtn',
            'button:has-text("Process")', 'button:has-text("Compress")',
            'button:has-text("Convert")', 'button:has-text("Apply")',
            'button:has-text("Run")', 'button:has-text("Generate")',
            'button:has-text("Extract")', 'button:has-text("Split")',
            'button:has-text("Merge")', 'button:has-text("Rotate")',
            'button.btn-primary',
          ];
          for (const sel of btnSelectors) {
            const btn = page.locator(sel).first();
            if (await btn.count().then(c => c > 0)) {
              const isDisabled = await btn.isDisabled().catch(() => true);
              if (!isDisabled) {
                try {
                  await Promise.race([
                    btn.click({ timeout: 3000 }),
                    new Promise(r => setTimeout(r, 3000)),
                  ]);
                  ranProcess = true;
                  await page.waitForTimeout(1500);
                } catch(e) {}
                break;
              }
            }
          }
        }
      }

    } catch (e) {
      errors.push(`[F] ${e.message.substring(0, 150)}`);
    }

    const status = errors.length === 0 ? '\u2705' : '\u274c';
    const typeTag = `[${type.toUpperCase()}]`;
    console.log(`${status} ${typeTag} ${slug.padEnd(26)} | load:${loadOK?'\u2705':'\u274c'} up:${uploaded?'\u2705':'\u274c'} run:${ranProcess?'\u2705':'\u274c'} | err:${errors.length}`);
    if (errors.length) {
      errors.forEach(e => console.log(`      ${e}`));
    }

    results.push({ slug, type, loadOK, uploaded, ranProcess, errors });
    await context.close();
  }

  await browser.close();

  console.log('\n' + '='.repeat(70));
  console.log('FINAL SUMMARY');
  console.log('='.repeat(70));
  const total = results.length;
  const noErrors = results.filter(r => r.errors.length === 0).length;
  const withErrors = results.filter(r => r.errors.length > 0);
  console.log(`Total tools: ${total}`);
  console.log(`No errors: ${noErrors}`);
  console.log(`With errors: ${withErrors.length}`);
  if (withErrors.length) {
    console.log('\nTools with errors:');
    withErrors.forEach(r => console.log(`  \u274c ${r.slug} [${r.type}] (${r.errors.length})`));
  }
  process.exit(withErrors.length > 0 ? 1 : 0);
})();
