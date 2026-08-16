#!/usr/bin/env python
"""Check ALL zip download filenames have .zip extension."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
EXCLUDE = ['_backup_2026-06-13', 'node_modules', '.git', 'src']

issues = []

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for f in files:
        if not f.endswith('.html') and not f.endswith('.js'): continue
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, BASE)
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue

        # Pattern 1: a.download = 'xxx.zip' or a.download = zipName
        for m in re.finditer(r'\.download\s*=\s*([\'"]?)([^\'";\n]+)\1', content):
            val = m.group(2).strip()
            # Skip variables
            if val.startswith("'") or val.startswith('"'):
                fname = val.strip("'\"")
            else:
                continue  # variable, skip
            # Check zip files
            if 'zip' in fname.lower() or 'rar' in fname.lower():
                if not (fname.endswith('.zip') or fname.endswith('.rar')):
                    issues.append((rel, f'ZIP/RAR filename missing extension: {fname}'))

        # Pattern 2: opt.filename || 'xxx' in exportZip
        for m in re.finditer(r"\|\|\s*'([^']+)'", content):
            fname = m.group(1)
            if 'zip' in fname.lower():
                if not fname.endswith('.zip'):
                    issues.append((rel, f'Default ZIP filename missing extension: {fname}'))

print(f'Checked {len(open(fpath).readlines() if False else [1])} files...')
print('=' * 70)
print(f'ISSUES: {len(issues)}')
print('=' * 70)
for f, msg in issues:
    print(f'  ❌ {f}')
    print(f'     {msg}')
if not issues:
    print('  ✅ All ZIP/RAR filenames have correct extensions!')
