"""Comprehensive audit: lang.js coverage, broken links, RTL consistency."""
import os, re, collections

ROOT = r'e:\网站项目\smartimgkit'
LANGS = ['en', 'zh', 'ar', 'es', 'fr', 'id', 'pt', 'vi']

# Skip these from lang.js check (legal/policy/verification pages)
SKIP_FILES = {
    '404.html', 'cookie-policy.html', 'privacy.html', 'terms.html',
    'test.html', 'geoip-js.html', 'yandex_69863cb66acb2020.html',
    '_workflow_template.html',
}

def should_skip(filename):
    if filename in SKIP_FILES:
        return True
    if filename.startswith('_'):
        return True
    return False

# ============ CHECK 1: lang.js coverage ============
print('=' * 70)
print('CHECK 1: lang.js coverage across all pages')
print('=' * 70)

missing_langjs = []
has_langjs = 0
total = 0

for lang in LANGS:
    base = ROOT if lang == 'en' else os.path.join(ROOT, lang)
    if not os.path.isdir(base):
        continue
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '_backup_2026-06-13' and d != 'src']
        for f in files:
            if not f.endswith('.html'):
                continue
            if should_skip(f):
                continue
            total += 1
            path = os.path.join(dirpath, f)
            content = open(path, encoding='utf-8', errors='replace').read()
            if 'lang.js' in content:
                has_langjs += 1
            else:
                missing_langjs.append(os.path.relpath(path, ROOT))

print(f'Pages with lang.js: {has_langjs}/{total}')
if missing_langjs:
    print(f'MISSING lang.js ({len(missing_langjs)}):')
    for p in missing_langjs[:20]:
        print(f'  - {p}')
    if len(missing_langjs) > 20:
        print(f'  ... and {len(missing_langjs) - 20} more')
else:
    print('  All pages have lang.js')

# ============ CHECK 2: Broken internal links ============
print()
print('=' * 70)
print('CHECK 2: Broken internal links (sample pages)')
print('=' * 70)

# Build set of all existing HTML paths
all_paths = set()
for lang in LANGS:
    base = ROOT if lang == 'en' else os.path.join(ROOT, lang)
    if not os.path.isdir(base):
        continue
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '_backup_2026-06-13' and d != 'src']
        for f in files:
            if f.endswith('.html'):
                relpath = os.path.relpath(os.path.join(dirpath, f), ROOT).replace('\\', '/')
                all_paths.add(relpath)

# Check links from sample pages
sample_pages = [
    'index.html', 'about.html', 'contact.html',
    'tools/cropper.html', 'tools/csv-to-pdf.html',
    'blog/index.html', 'workflows/index.html', 'workflows/avatar-pipeline.html',
    'zh/index.html', 'zh/tools/cropper.html', 'zh/blog/index.html', 'zh/workflows/index.html',
    'es/index.html', 'es/tools/cropper.html',
    'ar/index.html', 'ar/tools/cropper.html',
    'fr/index.html', 'id/index.html', 'pt/index.html', 'vi/index.html',
]

broken_links = []
for page in sample_pages:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        continue
    content = open(path, encoding='utf-8', errors='replace').read()
    # Find all internal href links
    for m in re.finditer(r'href="(/[^"]*)"', content):
        href = m.group(1)
        # Skip external, anchors, mailto
        if href.startswith('http') or href.startswith('#') or href.startswith('mailto') or href.startswith('tel'):
            continue
        # Normalize: remove trailing slash, add .html if no extension
        normalized = href.rstrip('/')
        if not os.path.splitext(normalized)[1]:
            # No extension - try .html
            test_path = normalized.lstrip('/') + '.html'
        else:
            test_path = normalized.lstrip('/')
        # Remove query strings
        test_path = test_path.split('?')[0]
        if test_path not in all_paths and test_path.replace('.html', '/index.html') not in all_paths:
            broken_links.append((page, href, test_path))

if broken_links:
    print(f'Broken links found ({len(broken_links)}):')
    for page, href, test in broken_links[:30]:
        print(f'  {page} -> {href} (not found: {test})')
else:
    print('  No broken links in sample pages')

# ============ CHECK 3: RTL consistency (ar pages) ============
print()
print('=' * 70)
print('CHECK 3: Arabic RTL consistency')
print('=' * 70)

ar_dir = os.path.join(ROOT, 'ar')
ar_issues = []
ar_total = 0
if os.path.isdir(ar_dir):
    for dirpath, dirs, files in os.walk(ar_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if not f.endswith('.html'):
                continue
            ar_total += 1
            path = os.path.join(dirpath, f)
            content = open(path, encoding='utf-8', errors='replace').read()
            # Check for dir="rtl"
            html_tag = re.search(r'<html[^>]*>', content)
            if html_tag:
                if 'dir="rtl"' not in html_tag.group() and "dir='rtl'" not in html_tag.group():
                    ar_issues.append((os.path.relpath(path, ROOT), 'Missing dir="rtl" in <html>'))
            # Check for Tajawal font
            if 'Tajawal' not in content and 'tajawal' not in content:
                ar_issues.append((os.path.relpath(path, ROOT), 'Missing Tajawal font'))

print(f'Arabic pages checked: {ar_total}')
if ar_issues:
    print(f'Issues ({len(ar_issues)}):')
    for path, issue in ar_issues[:20]:
        print(f'  {path}: {issue}')
else:
    print('  All Arabic pages have dir="rtl" and Tajawal font')

# ============ CHECK 4: CSS version consistency ============
print()
print('=' * 70)
print('CHECK 4: CSS/JS version consistency')
print('=' * 70)

css_versions = collections.Counter()
js_versions = collections.Counter()
for lang in LANGS:
    base = ROOT if lang == 'en' else os.path.join(ROOT, lang)
    if not os.path.isdir(base):
        continue
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != '_backup_2026-06-13' and d != 'src']
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(dirpath, f)
            content = open(path, encoding='utf-8', errors='replace').read()
            for m in re.finditer(r'style\.css\?v=(\d+)', content):
                css_versions[m.group(1)] += 1
            for m in re.finditer(r'main\.js\?v=(\d+)', content):
                js_versions[m.group(1)] += 1

print(f'CSS versions: {dict(css_versions)}')
print(f'JS versions: {dict(js_versions)}')

# ============ SUMMARY ============
print()
print('=' * 70)
print('SUMMARY')
print('=' * 70)
print(f'lang.js missing: {len(missing_langjs)} pages')
print(f'Broken links: {len(broken_links)}')
print(f'Arabic RTL issues: {len(ar_issues)}')
print(f'CSS version variants: {len(css_versions)}')
print(f'JS version variants: {len(js_versions)}')
