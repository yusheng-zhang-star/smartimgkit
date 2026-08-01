#!/usr/bin/env python
"""Deep static scan - only active files, exclude backups."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
EXCLUDE_DIRS = ['_backup_2026-06-13', 'node_modules', '.git', 'src']

issues = []

def strip_query(path):
    """Remove ?v= query params from path."""
    return path.split('?')[0]

# Scan active HTML files
all_html = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if f.endswith('.html'):
            all_html.append(os.path.join(root, f))

print(f'Scanning {len(all_html)} active HTML files...\n')

for fpath in sorted(all_html):
    rel = os.path.relpath(fpath, BASE)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        issues.append((rel, 'ENCODING ERROR'))
        continue

    fdir = os.path.dirname(fpath)

    # Check 1: Template variables not replaced (exclude templates)
    if '_template' not in rel and 'src/' not in rel:
        for m in re.finditer(r'\{\{[A-Z_]+\}\}', content):
            issues.append((rel, f'TEMPLATE VAR NOT REPLACED: {m.group()}'))

    # Check 2: CDN references (should all be local now)
    for m in re.finditer(r'src="https?://cdn[^"]+"', content):
        issues.append((rel, f'STILL USING CDN: {m.group()[:100]}'))
    for m in re.finditer(r'href="https?://cdn[^"]+"', content):
        issues.append((rel, f'STILL USING CDN CSS: {m.group()[:100]}'))

    # Check 3: Extract script src and link href
    for m in re.finditer(r'<script[^>]+src="([^"]+)"', content):
        src = m.group(1)
        if src.startswith('http'): continue
        src_clean = strip_query(src)
        if src_clean.startswith('/'):
            full = os.path.join(BASE, src_clean.lstrip('/'))
        else:
            full = os.path.normpath(os.path.join(fdir, src_clean))
        if not os.path.exists(full):
            issues.append((rel, f'MISSING JS: {src}'))

    for m in re.finditer(r'<link[^>]+href="([^"]+)"', content):
        href = m.group(1)
        if 'stylesheet' not in content and 'icon' not in href: 
            pass  # might not be css
        if href.startswith('http'): continue
        if 'stylesheet' in content[max(0,content.find(href)-100):content.find(href)] or href.endswith('.css'):
            href_clean = strip_query(href)
            if href_clean.startswith('/'):
                full = os.path.join(BASE, href_clean.lstrip('/'))
            else:
                full = os.path.normpath(os.path.join(fdir, href_clean))
            if not os.path.exists(full):
                issues.append((rel, f'MISSING CSS: {href}'))

# Report
print('=' * 70)
print(f'ISSUES FOUND: {len(issues)}')
print('=' * 70)
for fpath, issue in sorted(issues):
    print(f'  ❌ {fpath}')
    print(f'     {issue}')

if not issues:
    print('  ✅ No issues found!')
