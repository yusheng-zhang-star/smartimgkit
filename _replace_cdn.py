#!/usr/bin/env python
"""Replace all CDN links with local paths in all HTML files."""
import os, re, glob

BASE = r'E:\网站项目\smartimgkit'

# Mapping: (regex pattern -> local path
REPLACEMENTS = [
    # JSZip
    (r'https://cdn\.jsdelivr\.net/npm/jszip@[^"]+/dist/jszip\.min\.js', '/js/jszip.min.js'),
    # browser-image-compression
    (r'https://cdn\.jsdelivr\.net/npm/browser-image-compression@[^"]+/dist/browser-image-compression\.min\.js', '/js/browser-image-compression.min.js'),
    # heic2any (jsdelivr)
    (r'https://cdn\.jsdelivr\.net/npm/heic2any@[^"]+/dist/heic2any\.min\.js', '/js/heic2any.min.js'),
    # heic2any (cdnjs)
    (r'https://cdnjs\.cloudflare\.com/ajax/libs/heic2any/[^"]+/heic2any\.min\.js', '/js/heic2any.min.js'),
]

count = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', '.vscode', '_backup_2026-06-13')]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue

        original = content
        for pattern, replacement in REPLACEMENTS:
            content = re.sub(pattern, replacement, content)

        if content != original:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(content)
            count += 1
            rel = os.path.relpath(path, BASE).replace('\\', '/')
            print(f'  ✅ {rel}')

print(f'\nTotal files updated: {count}')
