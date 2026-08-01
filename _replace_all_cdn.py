#!/usr/bin/env python
"""Replace ALL CDN references with local paths in ALL HTML files."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
EXCLUDE_DIRS = ['_backup_2026-06-13', 'node_modules', '.git', 'src']

# Mapping: CDN URL pattern -> local path (relative to site root, starting with /)
CDN_MAP = [
    # JSZip
    (r'https://cdn\.jsdelivr\.net/npm/jszip@3\.10\.1/dist/jszip\.min\.js', '/js/jszip.min.js'),
    (r'https://cdnjs\.cloudflare\.com/ajax/libs/jszip/3\.10\.1/jszip\.min\.js', '/js/jszip.min.js'),
    # heic2any
    (r'https://cdn\.jsdelivr\.net/npm/heic2any@0\.0\.4/dist/heic2any\.min\.js', '/js/heic2any.min.js'),
    # browser-image-compression
    (r'https://cdn\.jsdelivr\.net/npm/browser-image-compression@2\.0\.2/dist/browser-image-compression\.min\.js', '/js/browser-image-compression.min.js'),
    # pako (GIF)
    (r'https://cdn\.jsdelivr\.net/npm/pako@2\.1\.0/dist/pako\.min\.js', '/js/pako.min.js'),
    # UPNG (GIF)
    (r'https://cdn\.jsdelivr\.net/npm/upng-js@2\.1\.0/UPNG\.min\.js', '/js/upng.min.js'),
    # gifuct-js
    (r'https://cdn\.jsdelivr\.net/npm/gifuct-js@2\.1\.3/dist/gifuct-js\.min\.js', '/js/gifuct-js.min.js'),
    (r'https://cdn\.jsdelivr\.net/npm/gifuct-js@[^/]+/[^"]+', '/js/gifuct-js.min.js'),  # any version
    # jsPDF
    (r'https://cdn\.jsdelivr\.net/npm/jspdf@2\.5\.1/dist/jspdf\.umd\.min\.js', '/js/jspdf.umd.min.js'),
    # qrcodejs
    (r'https://cdn\.jsdelivr\.net/npm/qrcodejs@1\.0\.0/qrcode\.min\.js', '/js/qrcode.min.js'),
    # signature_pad
    (r'https://cdn\.jsdelivr\.net/npm/signature_pad@4\.2\.0/dist/signature_pad\.umd\.min\.js', '/js/signature_pad.umd.min.js'),
]

count_files = 0
count_replacements = 0

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if not f.endswith('.html'): continue
        fpath = os.path.join(root, f)
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        
        original = content
        for pattern, replacement in CDN_MAP:
            content = re.sub(pattern, replacement, content)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            count_files += 1
            # Count how many replacements were made
            for pattern, replacement in CDN_MAP:
                count_replacements += len(re.findall(pattern, original))

print(f'Files modified: {count_files}')
print(f'Total replacements: {count_replacements}')
