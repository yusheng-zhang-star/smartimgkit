# -*- coding: utf-8 -*-
"""Strip UTF-8 BOM from all git-tracked text files. Local-only. Do NOT commit."""
import os, subprocess

root = r'e:\网站项目\smartimgkit'
exts = ('.html', '.htm', '.js', '.css', '.xml', '.txt', '.json', '.svg', '.md')

# get git-tracked files
out = subprocess.check_output(['git', 'ls-files'], cwd=root, text=True)
files = [l.strip() for l in out.splitlines() if l.strip()]

BOM = b'\xef\xbb\xbf'
changed = []
for rel in files:
    if rel.startswith('_backup_'):
        continue
    if not rel.lower().endswith(exts):
        continue
    fp = os.path.join(root, rel.replace('/', os.sep))
    if not os.path.isfile(fp):
        continue
    with open(fp, 'rb') as fh:
        raw = fh.read()
    orig = raw
    while raw[:3] == BOM:
        raw = raw[3:]
    if raw is not orig:
        with open(fp, 'wb') as fh:
            fh.write(raw)
        changed.append(rel)

print('=== BOM stripped from %d files ===' % len(changed))
for r in changed:
    print(r)
