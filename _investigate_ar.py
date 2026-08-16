#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Investigate Arabic pages: count, current html tag, check for existing dir attribute."""
import os, re

BASE = r'e:\网站项目\smartimgkit\ar'

ar_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.html'):
            ar_files.append(os.path.join(root, f))

print('Total Arabic HTML files: %d' % len(ar_files))
print()

# Check current html tags
has_dir = 0
no_dir = 0
for fpath in sorted(ar_files):
    html = open(fpath, encoding='utf-8').read()
    html_tag = re.search(r'<html[^>]*>', html)
    if html_tag:
        tag = html_tag.group(0)
        rel = os.path.relpath(fpath, BASE)
        if 'dir=' in tag:
            has_dir += 1
        else:
            no_dir += 1
            if no_dir <= 3:  # Show first 3 examples
                print('  %s: %s' % (rel, tag))

print('\nAlready has dir: %d' % has_dir)
print('Missing dir: %d' % no_dir)

# Check if main CSS has RTL support
css = open(os.path.join(r'e:\网站项目\smartimgkit\css\style.css'), encoding='utf-8').read()
rtl_rules = re.findall(r'\[dir=["\']rtl["\'][^}]*\}', css)
print('\nRTL CSS rules in style.css: %d' % len(rtl_rules))
if rtl_rules:
    for r in rtl_rules[:3]:
        print('  ', r[:100])

# Also check for html[dir="rtl"] patterns
rtl_patterns = re.findall(r'html\[dir["\']?=["\']?rtl[^}]*\}', css)
print('html[dir=rtl] patterns: %d' % len(rtl_patterns))
