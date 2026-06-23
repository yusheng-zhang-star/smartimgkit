/**
 * SmartImgKit 全面审计脚本
 * 检查项：
 * 1. 工具页对等性（各语言目录工具是否齐全）
 * 2. 内链完整性（所有 href/src 是否指向存在的文件或有效URL）
 * 3. FAQ 容器结构（</div> 关闭位置）
 * 4. 语言切换器一致性
 * 5. 模板变量残留
 * 6. CSS/JS 引用路径正确性
 * 7. 404/broken pages
 * 8. sitemap 覆盖度
 * 9. _redirects 覆盖率
 */
const fs = require('fs');
const path = require('path');

const BASE = 'E:/网站项目/smartimgkit';
const BASE_URL = 'https://smartimgkit.com';

// ===== 1. TOOL FILE INVENTORY =====
console.log('\n========== 1. 工具页清单 (Tool Inventory) ==========');

const langDirs = ['es/tools', 'pt/tools', 'id/tools', 'tools', 'dist/tools'];
const toolSets = {};

for (const dir of langDirs) {
  const full = path.join(BASE, dir);
  if (!fs.existsSync(full)) continue;
  const files = fs.readdirSync(full).filter(f => f.endsWith('.html')).sort();
  toolSets[dir] = files;
  console.log(`  ${dir}: ${files.length} tools`);
}

// Find tools that exist in some dirs but not others
const allToolNames = new Set();
for (const [, files] of Object.entries(toolSets)) {
  for (const f of files) allToolNames.add(f);
}

console.log(`\n  唯一工具名总数: ${allToolNames.size}`);

// Check parity between tools/ (full English) and language dirs
const enTools = new Set(toolSets['tools'] || []);
const distTools = new Set(toolSets['dist/tools'] || []);

console.log('\n  --- tools/ (45) vs dist/tools/ (24) 差异 ---');
const enOnly = [...enTools].filter(f => !distTools.has(f));
const distOnly = [...distTools].filter(f => !enTools.has(f));
console.log(`  Only in tools/: ${enOnly.length} files`);
enOnly.forEach(f => console.log(`    - ${f}`));
if (distOnly.length > 0) {
  console.log(`  Only in dist/tools/: ${distOnly.length} files`);
  distOnly.forEach(f => console.log(`    - ${f}`));
}

// Check each language has all tools from tools/
for (const lang of ['es/tools', 'pt/tools', 'id/tools']) {
  const langSet = new Set(toolSets[lang] || []);
  const missing = [...enTools].filter(f => !langSet.has(f));
  const extra = [...langSet].filter(f => !enTools.has(f));
  console.log(`\n  ${lang} vs tools/ 对比:`);
  if (missing.length > 0) console.log(`    Missing (${missing.length}): ${missing.join(', ')}`);
  else console.log(`    ✅ All ${enTools.size} tools present`);
  if (extra.length > 0) console.log(`    Extra (${extra.length}): ${extra.join(', ')}`);
}

// ===== 2. FAQ CONTAINER CHECK =====
console.log('\n========== 2. FAQ 容器结构检查 ==========');

// Check for the wrong pattern: </div> closing before second FAQ section
const faqIssuePattern = /<\/section>\s*\n\s*<\/div>\s*\n\s*\n?\s*<section class="faq-section" style="margin-top:32px">/;

let faqIssues = [];
for (const [dir, files] of Object.entries(toolSets)) {
  for (const f of files) {
    const fp = path.join(BASE, dir, f);
    const content = fs.readFileSync(fp, 'utf8');
    if (faqIssuePattern.test(content)) {
      faqIssues.push(`${dir}/${f}`);
    }
  }
}

if (faqIssues.length === 0) {
  console.log('  ✅ 所有工具页 FAQ 容器结构正确');
} else {
  console.log(`  ❌ ${faqIssues.length} 个文件仍有 FAQ 容器问题:`);
  faqIssues.forEach(f => console.log(`    - ${f}`));
}

// ===== 3. TEMPLATE VARIABLE CHECK =====
console.log('\n========== 3. 模板变量残留检查 ==========');

const templateVars = [
  '{{SLUG}}', '{{DOC_TITLE}}', '{{META_DESC}}', '{{META_KW}}',
  '{{CANONICAL_URL}}', '{{THEME_COLOR}}', '{{OG_TITLE}}', '{{OG_DESC}}',
  '{{OG_URL}}', '{{OG_IMAGE}}', '{{TWITTER_TITLE}}', '{{TWITTER_DESC}}',
  '{{TWITTER_IMAGE}}', '{{H1}}', '{{SUBTITLE}}', '{{BREADCRUMB_LAST}}',
  '{{TOOL_WORKSPACE}}', '{{HOWTO_HTML}}', '{{GUIDE_HTML}}',
  '{{FAQ_HTML}}', '{{RELATED_HTML}}', '{{INLINE_STYLE}}',
  '{{INLINE_JS}}', '{{JSONLD_WEBAPP}}', '{{JSONLD_HOWTO}}', '{{JSONLD_FAQ}}'
];

let templateIssues = [];
for (const [dir, files] of Object.entries(toolSets)) {
  for (const f of files) {
    const fp = path.join(BASE, dir, f);
    const content = fs.readFileSync(fp, 'utf8');
    for (const v of templateVars) {
      if (content.includes(v)) {
        templateIssues.push({ file: `${dir}/${f}`, var: v });
      }
    }
  }
}

if (templateIssues.length === 0) {
  console.log('  ✅ 无模板变量残留');
} else {
  console.log(`  ❌ ${templateIssues.length} 处模板变量残留:`);
  templateIssues.forEach(t => console.log(`    - ${t.file}: ${t.var}`));
}

// ===== 4. INTERNAL LINK CHECK =====
console.log('\n========== 4. 内链完整性检查 ==========');

// Collect all valid local file paths
const validPaths = new Set();
validPaths.add('/');
validPaths.add('/404.html');
validPaths.add('/about.html');
validPaths.add('/contact.html');
validPaths.add('/privacy.html');
validPaths.add('/terms.html');
validPaths.add('/cookie-policy.html');
validPaths.add('/blog/');
validPaths.add('/blog/index.html');
validPaths.add('/workflows/');
validPaths.add('/workflows/index.html');
validPaths.add('/sitemap.xml');
validPaths.add('/robots.txt');
validPaths.add('/favicon.svg');
validPaths.add('/favicon.ico');
validPaths.add('/favicon.png');
validPaths.add('/css/style.css');
validPaths.add('/js/main.js');
validPaths.add('/js/pdf.min.js');
validPaths.add('/js/pdf.worker.min.js');

// Add blog pages
const blogDir = path.join(BASE, 'blog');
if (fs.existsSync(blogDir)) {
  for (const f of fs.readdirSync(blogDir)) {
    if (f.endsWith('.html')) validPaths.add(`/blog/${f}`);
  }
}

// Add all tool pages (both /tools/xxx.html and /dist/tools/xxx.html)
for (const f of (toolSets['tools'] || [])) validPaths.add(`/tools/${f}`);
for (const f of (toolSets['dist/tools'] || [])) validPaths.add(`/dist/tools/${f}`);
for (const f of (toolSets['es/tools'] || [])) validPaths.add(`/es/tools/${f}`);
for (const f of (toolSets['pt/tools'] || [])) validPaths.add(`/pt/tools/${f}`);
for (const f of (toolSets['id/tools'] || [])) validPaths.add(`/id/tools/${f}`);
validPaths.add('/es/');
validPaths.add('/pt/');
validPaths.add('/id/');

// Add workflow pages
const wfDir = path.join(BASE, 'workflows');
if (fs.existsSync(wfDir)) {
  for (const f of fs.readdirSync(wfDir)) {
    if (f.endsWith('.html')) validPaths.add(`/workflows/${f}`);
  }
}

// Scrape all HTML files for internal links
function getInternalLinks(html, sourceFile) {
  const links = [];
  // href links
  const hrefRegex = /href=["']([^"']+)["']/g;
  let m;
  while ((m = hrefRegex.exec(html)) !== null) {
    const url = m[1];
    if (url.startsWith('/') && !url.startsWith('//')) {
      // Remove query string and hash
      const clean = url.split('?')[0].split('#')[0];
      links.push({ type: 'href', url: clean, file: sourceFile });
    }
    // Also check relative paths like ../css/
    if (url.startsWith('../') || url.startsWith('./')) {
      links.push({ type: 'href', url: url, file: sourceFile });
    }
  }
  // src links
  const srcRegex = /src=["']([^"']+)["']/g;
  while ((m = srcRegex.exec(html)) !== null) {
    const url = m[1];
    if (url.startsWith('/') && !url.startsWith('//')) {
      const clean = url.split('?')[0].split('#')[0];
      links.push({ type: 'src', url: clean, file: sourceFile });
    }
  }
  return links;
}

// Collect all internal links
let allLinks = [];

// Root-level HTML files
const rootFiles = fs.readdirSync(BASE).filter(f => f.endsWith('.html'));
for (const f of rootFiles) {
  const content = fs.readFileSync(path.join(BASE, f), 'utf8');
  allLinks.push(...getInternalLinks(content, f));
}

// Tool pages
for (const [dir, files] of Object.entries(toolSets)) {
  for (const f of files) {
    const content = fs.readFileSync(path.join(BASE, dir, f), 'utf8');
    allLinks.push(...getInternalLinks(content, `${dir}/${f}`));
  }
}

// Blog pages
if (fs.existsSync(blogDir)) {
  for (const f of fs.readdirSync(blogDir).filter(x => x.endsWith('.html'))) {
    const content = fs.readFileSync(path.join(BASE, 'blog', f), 'utf8');
    allLinks.push(...getInternalLinks(content, `blog/${f}`));
  }
}

// Check for broken links
let brokenLinks = [];
const checkedUrls = new Set();

for (const link of allLinks) {
  const url = link.url;
  if (checkedUrls.has(url)) continue;
  checkedUrls.add(url);

  // Handle relative paths like ../css/style.css from lang/tools/ pages
  let resolvedUrl = url;
  if (url.startsWith('../') || url.startsWith('./')) {
    // For tool pages in lang/tools/, ../ resolves to lang/, ../../ resolves to /
    resolvedUrl = url; // skip relative path check for now
    continue;
  }

  if (!validPaths.has(url)) {
    // Check if it's an external URL
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('mailto:') || url.startsWith('#')) {
      continue;
    }
    // Check if it's a workflow path
    if (url.startsWith('/workflows/')) {
      const wfFile = path.join(BASE, 'workflows', url.replace('/workflows/', ''));
      if (!fs.existsSync(wfFile) && !fs.existsSync(wfFile + '.html')) {
        // Check if workflows/ dir exists
        const wfDirExists = fs.existsSync(path.join(BASE, 'workflows'));
        if (wfDirExists) {
          const wfFiles = fs.readdirSync(path.join(BASE, 'workflows')).filter(f => f.endsWith('.html'));
          const matched = wfFiles.find(f => url.endsWith(f) || url.endsWith(f.replace('.html', '')));
          if (!matched) {
            brokenLinks.push({ ...link, reason: 'workflow file not found' });
          }
        } else {
          brokenLinks.push({ ...link, reason: 'workflows dir missing' });
        }
      }
      continue;
    }
    brokenLinks.push({ ...link, reason: 'path not in valid set' });
  }
}

// Also check for links to /tools/xxx.html that should exist
// These are the most common pattern from nav and footers
const toolsHtmlLinks = [...checkedUrls].filter(u => u.startsWith('/tools/') && u.endsWith('.html'));
for (const link of toolsHtmlLinks) {
  const fp = path.join(BASE, link);
  if (!fs.existsSync(fp)) {
    brokenLinks.push({ url: link, file: '(nav/footer reference)', reason: 'file does not exist in tools/' });
  }
}

console.log(`  Total unique internal links checked: ${checkedUrls.size}`);
if (brokenLinks.length === 0) {
  console.log('  ✅ 所有内链有效');
} else {
  console.log(`  ❌ ${brokenLinks.length} 个断链:`);
  // Group by URL
  const brokenByUrl = {};
  for (const b of brokenLinks) {
    if (!brokenByUrl[b.url]) brokenByUrl[b.url] = [];
    brokenByUrl[b.url].push(b.file);
  }
  for (const [url, files] of Object.entries(brokenByUrl)) {
    console.log(`    ${url} (${files.length} refs)`);
    if (files.length <= 5) files.forEach(f => console.log(`      ← ${f}`));
  }
}

// ===== 5. LANGUAGE SWITCHER CHECK =====
console.log('\n========== 5. 语言切换器检查 ==========');

// Check if language switcher exists on key pages
const keyPages = [
  { file: 'index.html', path: path.join(BASE, 'index.html') },
  { file: 'es/index.html', path: path.join(BASE, 'es/index.html') },
  { file: 'pt/index.html', path: path.join(BASE, 'pt/index.html') },
  { file: 'id/index.html', path: path.join(BASE, 'id/index.html') },
  { file: 'about.html', path: path.join(BASE, 'about.html') },
  { file: 'contact.html', path: path.join(BASE, 'contact.html') },
];

for (const { file, path: fp } of keyPages) {
  if (!fs.existsSync(fp)) {
    console.log(`  ⚠️ ${file} 不存在`);
    continue;
  }
  const content = fs.readFileSync(fp, 'utf8');
  const hasSwitcher = content.includes('lang-switcher') || content.includes('language-switcher') || content.includes('langSwitcher');
  const hasHreflang = content.includes('hreflang');
  const hasLangAlt = content.includes('alternate');
  console.log(`  ${file}: switcher=${hasSwitcher ? '✅' : '❌'}, hreflang=${hasHreflang ? '✅' : '❌'}, alternates=${hasLangAlt ? '✅' : '❌'}`);
}

// Check tool pages for lang switcher
console.log('\n  --- 工具页语言切换器抽样 ---');
const sampleTools = ['compressor.html', 'background-remover.html', 'converter.html'];
for (const tool of sampleTools) {
  for (const dir of langDirs) {
    const fp = path.join(BASE, dir, tool);
    if (!fs.existsSync(fp)) continue;
    const content = fs.readFileSync(fp, 'utf8');
    const hasSwitcher = content.includes('lang-switcher') || content.includes('langSwitcher');
    console.log(`  ${dir}/${tool}: switcher=${hasSwitcher ? '✅' : '❌'}`);
  }
}

// ===== 6. CSS/JS REFERENCE CHECK =====
console.log('\n========== 6. CSS/JS 引用路径检查 ==========');

// Check: root-level pages should use css/style.css, lang/tools/ pages should use ../../css/style.css
// dist/tools/ pages should use ../css/style.css
const cssRefIssues = [];

for (const f of rootFiles) {
  const content = fs.readFileSync(path.join(BASE, f), 'utf8');
  // Should reference css/style.css or /css/style.css
  if (!content.includes('css/style.css') && !content.includes('/css/style.css')) {
    if (content.includes('.css')) {
      cssRefIssues.push({ file: f, issue: 'No style.css reference found' });
    }
  }
}

// Check dist/tools/ files
for (const f of (toolSets['dist/tools'] || [])) {
  const fp = path.join(BASE, 'dist/tools', f);
  const content = fs.readFileSync(fp, 'utf8');
  if (!content.includes('../css/style.css') && !content.includes('/css/style.css')) {
    if (content.includes('.css')) {
      cssRefIssues.push({ file: `dist/tools/${f}`, issue: 'CSS path may be wrong' });
    }
  }
  // JS - dist/tools should use ../js/main.js
  if (!content.includes('../js/main.js') && !content.includes('/js/main.js')) {
    if (content.includes('main.js')) {
      cssRefIssues.push({ file: `dist/tools/${f}`, issue: 'JS path may be wrong' });
    }
  }
}

// Check lang/tools/ files (es/pt/id) - should use ../../css/style.css and ../../js/main.js
for (const lang of ['es/tools', 'pt/tools', 'id/tools']) {
  for (const f of (toolSets[lang] || [])) {
    const fp = path.join(BASE, lang, f);
    const content = fs.readFileSync(fp, 'utf8');
    // Check CSS path
    if (!content.includes('../../css/style.css') && !content.includes('/css/style.css')) {
      if (content.includes('.css')) {
        cssRefIssues.push({ file: `${lang}/${f}`, issue: 'CSS path may be wrong (expected ../../css/style.css)' });
      }
    }
    // Check JS path
    if (!content.includes('../../js/main.js') && !content.includes('/js/main.js')) {
      if (content.includes('main.js')) {
        cssRefIssues.push({ file: `${lang}/${f}`, issue: 'JS path may be wrong (expected ../../js/main.js)' });
      }
    }
  }
}

if (cssRefIssues.length === 0) {
  console.log('  ✅ CSS/JS 引用路径正确');
} else {
  console.log(`  ⚠️ ${cssRefIssues.length} 个 CSS/JS 引用问题:`);
  cssRefIssues.forEach(i => console.log(`    - ${i.file}: ${i.issue}`));
}

// ===== 7. WORKFLOWS DIRECTORY CHECK =====
console.log('\n========== 7. Workflows 目录检查 ==========');

const wfPath = path.join(BASE, 'workflows');
if (!fs.existsSync(wfPath)) {
  console.log('  ❌ workflows/ 目录不存在！导航栏引用了 /workflows/');
} else {
  const wfFiles = fs.readdirSync(wfPath).filter(f => f.endsWith('.html'));
  console.log(`  workflows/ 文件数: ${wfFiles.length}`);
  if (wfFiles.length === 0) {
    console.log('  ⚠️ workflows/ 目录为空！');
  } else {
    wfFiles.forEach(f => console.log(`    - ${f}`));
  }
  // Check for index.html
  if (!fs.existsSync(path.join(wfPath, 'index.html'))) {
    console.log('  ⚠️ workflows/ 缺少 index.html');
  }
}

// ===== 8. SITEMAP COVERAGE =====
console.log('\n========== 8. Sitemap 覆盖度检查 ==========');

const sitemapPath = path.join(BASE, 'sitemap.xml');
if (fs.existsSync(sitemapPath)) {
  const sitemap = fs.readFileSync(sitemapPath, 'utf8');
  const sitemapUrls = [];
  const locRegex = /<loc>([^<]+)<\/loc>/g;
  let lm;
  while ((lm = locRegex.exec(sitemap)) !== null) {
    sitemapUrls.push(lm[1].replace(BASE_URL, ''));
  }
  console.log(`  Sitemap URL 数: ${sitemapUrls.length}`);
  
  // Check if main pages are in sitemap
  const expectedInSitemap = ['/', '/about.html', '/contact.html', '/privacy.html', '/terms.html', '/cookie-policy.html', '/blog/'];
  for (const ep of expectedInSitemap) {
    const found = sitemapUrls.some(u => u === ep || u === ep.replace('.html', '') || u === ep.replace(/\/$/, ''));
    if (!found) console.log(`  ⚠️ 缺失: ${ep}`);
  }
  
  // Check clean URL vs .html in sitemap
  const cleanUrls = sitemapUrls.filter(u => u.startsWith('/tools/') && !u.endsWith('.html'));
  const htmlUrls = sitemapUrls.filter(u => u.startsWith('/tools/') && u.endsWith('.html'));
  console.log(`  Tools URLs: ${cleanUrls.length} clean / ${htmlUrls.length} .html`);
} else {
  console.log('  ❌ sitemap.xml 不存在');
}

// ===== 9. INLINE STYLE CHECK (possibly duplicated) =====
console.log('\n========== 9. 行内样式重复检查 (抽样) =====');

const dupStyleCheck = ['tools/compressor.html', 'dist/tools/compressor.html', 'es/tools/compressor.html'];
for (const fp of dupStyleCheck) {
  const fullPath = path.join(BASE, fp);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⚠️ ${fp} 不存在`);
    continue;
  }
  const content = fs.readFileSync(fullPath, 'utf8');
  // Check for common issues
  const inlineStyleCount = (content.match(/<style>/g) || []).length;
  const bodyStyleCount = (content.match(/body\s*\{/g) || []).length;
  console.log(`  ${fp}: <style> blocks=${inlineStyleCount}, body{} rules=${bodyStyleCount}`);
}

// ===== 10. HREFLANG CONSISTENCY =====
console.log('\n========== 10. Hreflang 一致性检查 =====');

// Check that index.html has hreflang tags for all languages
const indexPath = path.join(BASE, 'index.html');
if (fs.existsSync(indexPath)) {
  const content = fs.readFileSync(indexPath, 'utf8');
  const hreflangMatches = content.match(/hreflang="([^"]+)"/g) || [];
  const hreflangs = hreflangMatches.map(m => m.match(/"([^"]+)"/)[1]);
  console.log(`  index.html hreflangs: ${hreflangs.join(', ')}`);
}

// Check lang index pages have correct hreflang
for (const lang of ['es', 'pt', 'id']) {
  const fp = path.join(BASE, lang, 'index.html');
  if (!fs.existsSync(fp)) {
    console.log(`  ❌ ${lang}/index.html 不存在`);
    continue;
  }
  const content = fs.readFileSync(fp, 'utf8');
  const hasSelf = content.includes(`hreflang="${lang}"`);
  const hasEn = content.includes('hreflang="en"');
  const hasXDefault = content.includes('hreflang="x-default"');
  console.log(`  ${lang}/index.html: self=${hasSelf ? '✅' : '❌'}, en=${hasEn ? '✅' : '❌'}, x-default=${hasXDefault ? '✅' : '❌'}`);
}

// ===== 11. TOOLS/ vs DIST/TOOLS/ DUPLICATION =====
console.log('\n========== 11. tools/ vs dist/tools/ 重复检查 =====');

const bothIn = [...distTools].filter(f => enTools.has(f));
console.log(`  两处都存在的工具: ${bothIn.length} 个`);
bothIn.forEach(f => console.log(`    - ${f}`));

// ===== 12. H1/META TITLE CHECK =====
console.log('\n========== 12. 页面标题抽样检查 =====');

const titleSamples = [
  'index.html', 'about.html', 'contact.html',
  'tools/background-remover.html', 'dist/tools/compressor.html',
  'es/tools/compressor.html', 'blog/index.html'
];

for (const fp of titleSamples) {
  const fullPath = path.join(BASE, fp);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⚠️ ${fp} 不存在`);
    continue;
  }
  const content = fs.readFileSync(fullPath, 'utf8');
  const titleMatch = content.match(/<title>([^<]+)<\/title>/);
  const h1Match = content.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const descMatch = content.match(/<meta name="description" content="([^"]+)"/);
  const title = titleMatch ? titleMatch[1] : '(none)';
  const h1 = h1Match ? h1Match[1] : '(none)';
  const desc = descMatch ? descMatch[1].substring(0, 80) + '...' : '(none)';
  console.log(`  ${fp}:`);
  console.log(`    title: ${title}`);
  console.log(`    h1: ${h1}`);
  if (title !== h1.replace(/<[^>]+>/g, '') && h1 !== '(none)') {
    // Check if title contains the h1 text
    if (!title.includes(h1.replace(/<[^>]+>/g, ''))) {
      console.log(`    ⚠️ title 与 h1 不匹配`);
    }
  }
}

// ===== 13. KEY PAGES EXISTENCE =====
console.log('\n========== 13. 关键页面存在性 =====');

const criticalPages = [
  'index.html', 'about.html', 'contact.html', 'privacy.html',
  'terms.html', 'cookie-policy.html', '404.html',
  'robots.txt', 'sitemap.xml', '_headers', '_redirects',
  'ads.txt', 'favicon.svg', 'favicon.ico',
  'css/style.css', 'js/main.js'
];

for (const p of criticalPages) {
  const fp = path.join(BASE, p);
  const exists = fs.existsSync(fp);
  const size = exists ? fs.statSync(fp).size : 0;
  const status = exists ? (size > 0 ? '✅' : '⚠️ (empty)') : '❌ MISSING';
  console.log(`  ${p}: ${status}`);
}

// ===== 14. IMAGE/ASSET CHECK =====
console.log('\n========== 14. 图片资源检查 =====');

const imgDirs = ['screenshots'];
for (const d of imgDirs) {
  const fp = path.join(BASE, d);
  if (!fs.existsSync(fp)) {
    console.log(`  ❌ ${d}/ 目录不存在`);
    continue;
  }
  const files = fs.readdirSync(fp);
  console.log(`  ${d}/: ${files.length} 文件`);
}

// ===== 15. NAV CONSISTENCY =====
console.log('\n========== 15. 导航一致性检查 =====');

const navSamples = ['index.html', 'tools/compressor.html', 'es/tools/compressor.html', 'blog/index.html', 'about.html'];
for (const fp of navSamples) {
  const fullPath = path.join(BASE, fp);
  if (!fs.existsSync(fullPath)) continue;
  const content = fs.readFileSync(fullPath, 'utf8');
  // Extract nav links
  const navMatch = content.match(/<nav class="main-nav"[^>]*>([\s\S]*?)<\/nav>/);
  if (navMatch) {
    const navLinks = navMatch[1].match(/href="([^"]+)"/g) || [];
    const navHrefs = navLinks.map(m => m.match(/"([^"]+)"/)[1]);
    console.log(`  ${fp}: nav=[${navHrefs.join(', ')}]`);
  }
}

console.log('\n========== 审计完成 ==========\n');
