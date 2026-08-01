/**
 * Full tool test: actually upload image and run process for ALL image tools
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

// Image tools that accept image uploads
const IMAGE_TOOLS = [
  'background-remover', 'compressor', 'converter', 'cropper',
  'circle-crop', 'face-blur', 'favicon-generator', 'gif-editor',
  'gif-splitter', 'ico-icon-generator', 'id-photo',
  'image-adjust', 'image-border', 'image-compare', 'image-compressor',
  'image-enhancer', 'image-exif-remover', 'image-filters', 'image-flip',
  'image-grayscale', 'image-merger', 'image-rotator', 'image-shadow',
  'image-splitter', 'image-upscaler', 'image-to-pdf',
  'meme-generator', 'metadata-viewer', 'print-resizer',
  'product-white-background', 'resizer', 'signature-maker',
  'social-media-post', 'text-on-image', 'watermark',
  'beauty-editor', 'photo-restoration', 'color-palette',
  'bulk-processor', 'screenshot-to-image', 'svg-to-png',
  'avif-support',
];

(async () => {
  console.log('='.repeat(70));
  console.log('ALL IMAGE TOOLS E2E TEST (' + IMAGE_TOOLS.length + ' tools)');
  console.log('Test image: ' + TEST_IMAGE);
  console.log('='.repeat(70));

  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const slug of IMAGE_TOOLS) {
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const url = `${BASE_URL}/tools/${slug}.html`;
    const errors = [];

    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(`[CONSOLE] ${msg.text().substring(0, 200)}`);
    });
    page.on('pageerror', err => errors.push(`[PAGEERROR] ${err.message.substring(0, 200)}`));
    page.on('dialog', async dialog => {
      errors.push(`[DIALOG] ${dialog.type()}: ${dialog.message().substring(0, 200)}`);
      await dialog.accept().catch(() => {});
    });

    let loadOK = false, uploaded = false, ranProcess = false;

    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      loadOK = resp && resp.status() < 400;
      await page.waitForTimeout(1000);

      // Try to find and upload via file input
      const fileInput = page.locator('input[type="file"]').first();
      if (await fileInput.count().then(c => c > 0)) {
        try {
          await fileInput.setInputFiles(TEST_IMAGE);
          uploaded = true;
          await page.waitForTimeout(800);
        } catch(e) { errors.push(`[UPLOAD] ${e.message.substring(0, 100)}`); }
      }

      // Try to find and click main button
      if (uploaded) {
        const btnSelectors = [
          '#processBtn', '#compressBtn', '#convertBtn', '#applyBtn',
          '#runBtn', '#generateBtn', '#downloadBtn',
          'button:has-text("Process")', 'button:has-text("Compress")',
          'button:has-text("Convert")', 'button:has-text("Apply")',
          'button:has-text("Run")', 'button:has-text("Generate")',
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
                await page.waitForTimeout(2000);
              } catch(e) {}
              break;
            }
          }
        }
      }

    } catch (e) {
      errors.push(`[FATAL] ${e.message.substring(0, 150)}`);
    }

    const status = errors.length === 0 ? '✅' : '❌';
    console.log(`${status} ${slug.padEnd(28)} | load:${loadOK?'✅':'❌'} upload:${uploaded?'✅':'❌'} run:${ranProcess?'✅':'❌'} | errors:${errors.length}`);
    if (errors.length) {
      errors.forEach(e => console.log(`      ❌ ${e}`));
    }

    results.push({ slug, loadOK, uploaded, ranProcess, errors });
    await context.close();
  }

  await browser.close();

  console.log('\n' + '='.repeat(70));
  console.log('FINAL SUMMARY');
  console.log('='.repeat(70));
  const total = results.length;
  const noErrors = results.filter(r => r.errors.length === 0).length;
  const withErrors = results.filter(r => r.errors.length > 0);
  console.log(`Total: ${total} | No errors: ${noErrors} | With errors: ${withErrors.length}`);
  if (withErrors.length) {
    console.log('\nTools with errors:');
    withErrors.forEach(r => console.log(`  ❌ ${r.slug} (${r.errors.length})`));
  }
  process.exit(withErrors.length > 0 ? 1 : 0);
})();
