#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Investigate English workflow pages: structure, content, translations needed."""
import os, re

WF_DIR = r'e:\网站项目\smartimgkit\workflows'

wfs = sorted([f for f in os.listdir(WF_DIR) if f.endswith('.html')])
print('Total workflow pages: %d' % len(wfs))
print('Slugs:', [f[:-5] for f in wfs])

# Check one workflow page structure
f = os.path.join(WF_DIR, wfs[0])
html = open(f, encoding='utf-8').read()
print('\n=== %s (first workflow) ===' % wfs[0])
print('Size: %d chars' % len(html))

# Title, h1, description
title = re.search(r'<title>([^<]+)</title>', html)
desc = re.search(r'<meta name="description" content="([^"]+)"', html)
h1 = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
print('title: %s' % (title.group(1)[:80] if title else 'N/A'))
print('desc: %s' % (desc.group(1)[:80] if desc else 'N/A'))
print('h1: %s' % (h1.group(1)[:80] if h1 else 'N/A'))

# Check lang attribute
lang_tag = re.search(r'<html lang="([^"]+)"', html)
print('lang: %s' % (lang_tag.group(1) if lang_tag else 'N/A'))

# Check for key structural elements
sections = re.findall(r'<section class="([^"]+)"', html)
print('Sections:', sections)

# Check for scripts
scripts = re.findall(r'<script src="([^"]+)"', html)
print('External scripts:', scripts)

# Check for Chinese workflow index
zh_wf_dir = r'e:\网站项目\smartimgkit\zh\workflows'
if os.path.isdir(zh_wf_dir):
    zh_wfs = [f for f in os.listdir(zh_wf_dir) if f.endswith('.html')]
    print('\nChinese workflows: %d' % len(zh_wfs))
else:
    print('\nChinese workflows dir: NOT FOUND')

# Check workflows index page
wf_index = os.path.join(WF_DIR, 'index.html')
if os.path.exists(wf_index):
    idx_html = open(wf_index, encoding='utf-8').read()
    print('\nWorkflows index exists: yes (%d chars)' % len(idx_html))
else:
    print('\nWorkflows index: NOT FOUND')

# Check all workflow titles for translation planning
print('\n=== All workflow titles ===')
for wf in wfs:
    fpath = os.path.join(WF_DIR, wf)
    h = open(fpath, encoding='utf-8').read()
    t = re.search(r'<title>([^<]+)</title>', h)
    h1m = re.search(r'<h1[^>]*>([^<]+)</h1>', h)
    print('  %s: %s | %s' % (wf[:-5], t.group(1)[:60] if t else 'N/A', h1m.group(1)[:40] if h1m else 'N/A'))
