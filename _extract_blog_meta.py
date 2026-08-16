# -*- coding: utf-8 -*-
"""Extract key metadata + headings from EN blog articles for translation planning."""
import os
import re

SRC = r'e:\网站项目\smartimgkit\blog'

for fname in sorted(os.listdir(SRC)):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    html = open(os.path.join(SRC, fname), encoding='utf-8').read()
    print('\n==== %s ====' % fname[:-5])
    t = re.search(r'<title>([^<]+)</title>', html)
    print('TITLE:', t.group(1) if t else 'N/A')
    d = re.search(r'<meta name="description" content="([^"]+)"', html)
    print('DESC:', d.group(1)[:140] if d else 'N/A')
    h1 = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    print('H1:', h1.group(1) if h1 else 'N/A')
    sub = re.search(r'class="blog-post-subtitle">([^<]+)</p>', html)
    print('SUB:', sub.group(1)[:120] if sub else 'N/A')
    qa = re.search(r'"quick-answer".*?<p style="margin:0;">([^<]+)</p>', html, re.S)
    print('QA:', qa.group(1)[:140] if qa else 'N/A')
    # h2 headings
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.S)
    print('H2 count:', len(h2s))
    for h in h2s[:20]:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        print('  -', clean[:80])
