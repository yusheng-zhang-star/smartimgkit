# -*- coding: utf-8 -*-
"""Copy EN workflows -> zh/workflows with path/lang/canonical/hreflang fixes.
Mechanical transformations only; visible text translation done separately.
"""
import os
import re
import shutil

BASE = r'e:\网站项目\smartimgkit'
SRC = os.path.join(BASE, 'workflows')
DST = os.path.join(BASE, 'zh', 'workflows')

os.makedirs(DST, exist_ok=True)

# Files to copy
html_files = []
js_files = []
for name in sorted(os.listdir(SRC)):
    fpath = os.path.join(SRC, name)
    if not os.path.isfile(fpath):
        continue
    if name.endswith('.html'):
        html_files.append(name)
    elif name.endswith('.js'):
        js_files.append(name)

print('HTML files:', len(html_files))
print('JS files:', len(js_files))


def transform_html(html, fname):
    # 1. lang
    html = html.replace('<html lang="en"', '<html lang="zh"')

    # 2. canonical & og:url -> /zh/workflows/
    # handle both trailing slash and specific page
    html = html.replace('https://smartimgkit.com/workflows/',
                        'https://smartimgkit.com/zh/workflows/')

    # 3. hreflang block: replace en + x-default lines with zh/en/x-default
    # Existing pattern:
    #   <link rel="alternate" hreflang="en" href="https://smartimgkit.com/zh/workflows/...">
    #   <link rel="alternate" hreflang="x-default" href="https://smartimgkit.com/zh/workflows/...">
    # (after step 2 both point to zh). Build correct set:
    zh_url = 'https://smartimgkit.com/zh/workflows/' + (fname if fname != 'index.html' else '')
    en_url = 'https://smartimgkit.com/workflows/' + (fname if fname != 'index.html' else '')
    # remove existing hreflang lines
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*', '\n  ', html)
    # insert new hreflang block right before </head>... actually insert after canonical link
    hreflang_block = ('<link rel="alternate" hreflang="zh" href="%s">\n  '
                      '<link rel="alternate" hreflang="en" href="%s">\n  '
                      '<link rel="alternate" hreflang="x-default" href="%s">\n  ') % (zh_url, en_url, en_url)
    # insert before favicon link
    html = html.replace('<link rel="icon" type="image/svg+xml" href="/favicon.svg">',
                        hreflang_block + '<link rel="icon" type="image/svg+xml" href="/favicon.svg">')

    # 4. CSS relative path: ../css/ -> ../../css/
    html = html.replace('../css/', '../../css/')
    # 5. relative js (../js/) -> ../../js/  (rare)
    html = html.replace('../js/', '../../js/')

    # 6. Nav & internal absolute links -> /zh/ variants
    # Order matters: more specific first
    replacements = [
        ('href="/workflows/"', 'href="/zh/workflows/"'),
        ('href="/blog/"', 'href="/zh/blog/"'),
        ('href="/about"', 'href="/zh/about"'),
        ('href="/contact"', 'href="/zh/contact"'),
        # tool links /tools/xxx  (but not /tools/ bare in nav which usually is /tools/background-remover)
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    # /tools/<name>  -> /zh/tools/<name>
    html = re.sub(r'href="/tools/([a-z0-9-]+)"', r'href="/zh/tools/\1"', html)
    # /workflows/<name> -> /zh/workflows/<name>
    html = re.sub(r'href="/workflows/([a-z0-9-]+)"', r'href="/zh/workflows/\1"', html)
    # /blog/<name> -> /zh/blog/<name>
    html = re.sub(r'href="/blog/([a-z0-9-]+)"', r'href="/zh/blog/\1"', html)

    # 7. Logo home link href="/" -> href="/zh/"  (only the logo anchor, careful)
    # The logo is: <a href="/" class="logo">
    html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
    # nav Home link <a href="/">Home</a>
    html = html.replace('href="/">Home</a>', 'href="/zh/">首页</a>')
    # other bare href="/" that are nav home
    html = re.sub(r'href="/">Home</a>', 'href="/zh/">首页</a>', html)

    return html


copied = 0
for fname in html_files:
    src = os.path.join(SRC, fname)
    dst = os.path.join(DST, fname)
    html = open(src, encoding='utf-8').read()
    html = transform_html(html, fname)
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(html)
    copied += 1

# Copy JS files as-is (shared logic, relative refs still valid)
for fname in js_files:
    shutil.copy2(os.path.join(SRC, fname), os.path.join(DST, fname))

print('Copied HTML:', copied)
print('Copied JS:', len(js_files))
print('DONE')
