#!/usr/bin/env python
"""Download all remaining CDN libraries to local js/ folder."""
import urllib.request, os

BASE = r'E:\网站项目\smartimgkit\js'
os.makedirs(BASE, exist_ok=True)

libs = [
    ('pako.min.js', 'https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js'),
    ('upng.min.js', 'https://cdn.jsdelivr.net/npm/upng-js@2.1.0/UPNG.min.js'),
    ('gifuct-js.min.js', 'https://cdn.jsdelivr.net/npm/gifuct-js@2.1.3/dist/gifuct-js.min.js'),
    ('jspdf.umd.min.js', 'https://cdn.jsdelivr.net/npm/jspdf@2.5.1/dist/jspdf.umd.min.js'),
    ('qrcode.min.js', 'https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js'),
    ('signature_pad.umd.min.js', 'https://cdn.jsdelivr.net/npm/signature_pad@4.2.0/dist/signature_pad.umd.min.js'),
]

for fname, url in libs:
    fpath = os.path.join(BASE, fname)
    if os.path.exists(fpath):
        print(f'  ⏭️  {fname} (already exists)')
        continue
    try:
        print(f'  📥 {fname}...', end=' ')
        urllib.request.urlretrieve(url, fpath)
        size = os.path.getsize(fpath)
        print(f'✅ ({size} bytes)')
    except Exception as e:
        print(f'❌ ERROR: {e}')

print('\nAll done!')
