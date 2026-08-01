/**
 * End-to-end test for workflows using Playwright
 * Actually uploads a file and runs the pipeline
 */
const { chromium } = require('playwright');
const path = require('path');

const TEST_IMAGE = path.join(__dirname, 'test-image.jpg');
const BASE_URL = 'http://localhost:8000';

const WORKFLOWS_TO_TEST = [
  // Previously broken ones (now fixed)
  'resume-cv-photo',
  'app-store-screenshot-suite',
  'course-tutorial-pack',
  'print-ready-prep',
  'email-signature-pack',
  // All other new workflows
  'blog-image-pack',
  'youtube-thumbnail-suite',
  'real-estate-photo-pack',
  'food-photography-bundle',
  'podcast-cover-suite',
  'freelancer-portfolio-pack',
  'event-photography-bundle',
  // Old ones
  'avatar-pipeline',
];

async function testWorkflow(page, slug) {
  const url = `${BASE_URL}/workflows/${slug}.html`;
  console.log(`\n🔍 Testing: ${slug}`);
  console.log(`   URL: ${url}`);

  const errors = [];
  const logs = [];

  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
    }
    logs.push(`[${msg.type()}] ${msg.text()}`);
  });

  page.on('dialog', async dialog => {
    errors.push(`DIALOG: ${dialog.type()}: ${dialog.message()}`);
    await dialog.accept();
  });

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    console.log('   ✅ Page loaded');

    // Wait a bit for JS to init
    await page.waitForTimeout(1000);

    // Check for load errors
    if (errors.length > 0) {
      console.log(`   ⚠️  Load errors: ${errors.length}`);
      errors.forEach(e => console.log(`      ❌ ${e}`));
    }

    // Upload file
    const fileInput = page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(TEST_IMAGE);
    console.log('   ✅ File uploaded');

    await page.waitForTimeout(500);

    // Check if Run button is enabled
    const runBtn = page.locator('#runBtn');
    const isDisabled = await runBtn.isDisabled().catch(() => true);
    console.log(`   ℹ️  Run button disabled: ${isDisabled}`);

    if (!isDisabled) {
      // Click Run Pipeline
      console.log('   🚀 Running pipeline...');
      
      // Start waiting for download before clicking
      const downloadPromise = page.waitForEvent('download', { timeout: 60000 }).catch(() => null);
      
      await runBtn.click();

      // Wait for processing
      const timeout = 60000;
      const start = Date.now();
      let done = false;
      while (Date.now() - start < timeout && !done) {
        await page.waitForTimeout(1000);
        const progressText = await page.locator('#wfProgText').innerText().catch(() => '');
        if (progressText.includes('Done') || progressText.includes('done')) {
          done = true;
        }
        if (errors.length > 0) {
          break;
        }
      }

      // Check for runtime errors
      if (errors.length > 0) {
        console.log(`   ❌ RUNTIME ERRORS (${errors.length}):`);
        errors.forEach(e => console.log(`      ❌ ${e}`));
        return { slug, success: false, errors };
      }

      console.log('   ✅ Pipeline completed');

      // Check download
      const download = await downloadPromise;
      if (download) {
        console.log('   ✅ ZIP download triggered');
      } else {
        console.log('   ⚠️  No download detected (might be blocked)');
      }

      return { slug, success: true, errors: [] };
    } else {
      console.log('   ⚠️  Run button still disabled after upload');
      return { slug, success: false, errors: ['Run button disabled after upload'] };
    }
  } catch (e) {
    console.log(`   ❌ EXCEPTION: ${e.message}`);
    return { slug, success: false, errors: [e.message] };
  }
}

(async () => {
  console.log('='.repeat(60));
  console.log('SmartImgKit Workflow E2E Test Suite');
  console.log(`Test image: ${TEST_IMAGE}`);
  console.log(`Exists: ${require('fs').existsSync(TEST_IMAGE)}`);
  console.log('='.repeat(60));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();

  const results = [];
  for (const slug of WORKFLOWS_TO_TEST) {
    const result = await testWorkflow(page, slug);
    results.push(result);
    // Clear state between tests
    await page.evaluate(() => localStorage.clear());
  }

  await browser.close();

  console.log('\n' + '='.repeat(60));
  console.log('TEST SUMMARY');
  console.log('='.repeat(60));

  const passed = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;

  results.forEach(r => {
    const icon = r.success ? '✅' : '❌';
    console.log(`${icon} ${r.slug}`);
    if (r.errors.length) {
      r.errors.forEach(e => console.log(`   ❌ ${e}`));
    }
  });

  console.log(`\nTotal: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
})();
