#!/usr/bin/env python
"""Check ALL zip download filenames have .zip extension."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
EXCLUDE = ['_backup_2026-06-13', 'node_modules', '.git', 'src']

issues = []
total_checked = 0

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for f in files:
        if not f.endswith('.html') and not f.endswith('.js'): continue
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, BASE)
        total_checked += 1
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue

        # Find all string literals used in .download assignments
        # Pattern: .download = 'something' or .download = "something"
        for m in re.finditer(r'\.download\s*=\s*[\'"]([^\'"]+)[\'"]', content):
            fname = m.group(1)
            # Check if it looks like a zip/archive name
            lower = fname.lower()
            if 'zip' in lower or 'rar' in lower or '7z' in lower or 'archive' in lower or 'pack' in lower or 'output' in lower:
                if not (fname.endswith('.zip') or fname.endswith('.rar') or fname.endswith('.7z')):
                    issues.append((rel, f'Archive filename missing extension: {fname}'))

print(f'Checked {total_checked} files...')
print('=' * 70)
print(f'ISSUES: {len(issues)}')
print('=' * 70)
for f, msg in issues:
    print(f'  ❌ {f}')
    print(f'     {msg}')
if not issues:
    print('  ✅ All archive download filenames have correct extensions!')
