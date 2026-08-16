# -*- coding: utf-8 -*-
"""Copy EN blog articles -> zh/blog with path/lang/canonical/hreflang fixes."""
import os
import re

BASE = r'e:\网站项目\smartimgkit'
SRC = os.path.join(BASE, 'blog')
DST = os.path.join(BASE, 'zh', 'blog')

os.makedirs(DST, exist_ok=True)


def transform_html(html, fname):
    slug = fname[:-5]
    # 1. lang
    html = html.replace('<html lang="en"', '<html lang="zh"')
    # 2. canonical & og:url -> /zh/blog/
    html = html.replace('https://smartimgkit.com/blog/',
                        'https://smartimgkit.com/zh/blog/')
    # mainEntityOfPage url in JSON-LD: "https://smartimgkit.com/blog/<slug>"
    # already replaced by the blanket replace above (blog/ -> zh/blog/)
    # 3. hreflang block
    zh_url = 'https://smartimgkit.com/zh/blog/' + slug
    en_url = 'https://smartimgkit.com/blog/' + slug
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*', '\n  ', html)
    hreflang_block = ('<link rel="alternate" hreflang="zh" href="%s">\n  '
                      '<link rel="alternate" hreflang="en" href="%s">\n  '
                      '<link rel="alternate" hreflang="x-default" href="%s">\n  ') % (zh_url, en_url, en_url)
    html = html.replace('<link rel="icon" type="image/svg+xml" href="/favicon.svg">',
                        hreflang_block + '<link rel="icon" type="image/svg+xml" href="/favicon.svg">')
    # 4. CSS path
    html = html.replace('../css/', '../../css/')
    html = html.replace('../js/', '../../js/')
    # 5. nav & internal links
    for old, new in [
        ('href="/blog/"', 'href="/zh/blog/"'),
        ('href="/workflows/"', 'href="/zh/workflows/"'),
        ('href="/about"', 'href="/zh/about"'),
        ('href="/contact"', 'href="/zh/contact"'),
    ]:
        html = html.replace(old, new)
    html = re.sub(r'href="/tools/([a-z0-9-]+)"', r'href="/zh/tools/\1"', html)
    html = re.sub(r'href="/workflows/([a-z0-9-]+)"', r'href="/zh/workflows/\1"', html)
    html = re.sub(r'href="/blog/([a-z0-9-]+)"', r'href="/zh/blog/\1"', html)
    # logo + home
    html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
    html = re.sub(r'href="/">Home</a>', 'href="/zh/">首页</a>', html)
    return html


copied = 0
for fname in sorted(os.listdir(SRC)):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    html = open(os.path.join(SRC, fname), encoding='utf-8').read()
    html = transform_html(html, fname)
    with open(os.path.join(DST, fname), 'w', encoding='utf-8') as fh:
        fh.write(html)
    copied += 1

print('Copied blog articles:', copied)
