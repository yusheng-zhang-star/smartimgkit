#!/usr/bin/env python
"""Deep static scan of ALL HTML files for common bugs."""
import os, re, glob
from html.parser import HTMLParser

BASE = r'E:\网站项目\smartimgkit'
issues = []

class MyHTMLParser(HTMLParser):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.ids = set()
        self.id_refs = []  # (id, context)
        self.scripts = []  # src or inline
        self.css_links = []
        self.inline_script = ''
        self.in_script = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.add(d['id'])
        # Collect id references in common JS patterns
        if tag == 'script':
            if 'src' in d:
                self.scripts.append(('external', d['src']))
                self.in_script = False
            else:
                self.in_script = True
                self.inline_script = ''
        elif tag == 'link' and d.get('rel') == 'stylesheet':
            if 'href' in d:
                self.css_links.append(d['href'])
    def handle_endtag(self, tag):
        if tag == 'script' and self.in_script:
            self.in_script = False
            self.scripts.append(('inline', self.inline_script))
    def handle_data(self, data):
        if self.in_script:
            self.inline_script += data

# 1. Scan all HTML files
all_html = []
for root, dirs, files in os.walk(BASE):
    if 'node_modules' in root or '.git' in root: continue
    for f in files:
        if f.endswith('.html'):
            all_html.append(os.path.join(root, f))

print(f'Scanning {len(all_html)} HTML files...\n')

for fpath in sorted(all_html):
    rel = os.path.relpath(fpath, BASE)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        issues.append((rel, 'encoding error'))
        continue

    parser = MyHTMLParser(rel)
    try:
        parser.feed(content)
    except:
        pass

    # Check 1: Template variables not replaced
    for m in re.finditer(r'\{\{[A-Z_]+\}\}', content):
        if '_template' not in rel and 'src/' not in rel:
            issues.append((rel, f'TEMPLATE VARIABLE NOT REPLACED: {m.group()}'))

    # Check 2: CDN references (should all be local now)
    for m in re.finditer(r'src="https?://cdn[^"]+"', content):
        issues.append((rel, f'STILL USING CDN: {m.group()[:80]}'))

    # Check 3: Check getElementById references vs actual ids
    all_js = ''
    for stype, scontent in parser.scripts:
        if stype == 'inline': all_js += scontent
    # Also check external scripts (we won't parse them, just check they exist)
    
    # Check 4: Missing file references
    fdir = os.path.dirname(fpath)
    for stype, src in parser.scripts:
        if stype == 'external':
            # Resolve relative paths
            if src.startswith('http'): continue
            if src.startswith('/'):
                full = os.path.join(BASE, src.lstrip('/'))
            else:
                full = os.path.normpath(os.path.join(fdir, src))
            if not os.path.exists(full):
                issues.append((rel, f'MISSING JS FILE: {src}'))
    for href in parser.css_links:
        if href.startswith('http'): continue
        if href.startswith('/'):
            full = os.path.join(BASE, href.lstrip('/'))
        else:
            full = os.path.normpath(os.path.join(fdir, href))
        if not os.path.exists(full):
            issues.append((rel, f'MISSING CSS FILE: {href}'))

# Report
print('=' * 70)
print(f'ISSUES FOUND: {len(issues)}')
print('=' * 70)
for fpath, issue in sorted(issues):
    print(f'  ❌ {fpath}')
    print(f'     {issue}')

if not issues:
    print('  ✅ No issues found!')
