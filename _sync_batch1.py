#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sync batch 1 PDF conversion tools to all language directories (es, pt, id, fr, vi, ar).

Pattern matches existing language tools: copy English tool, change lang attribute,
add hreflang links, update canonical. Tool UI stays in English (existing convention).
"""
import os, re

BASE = r'E:\网站项目\smartimgkit'
LANGS = ['es', 'pt', 'id', 'fr', 'vi', 'ar']
NEW_TOOLS = ['pdf-to-word', 'pdf-to-excel', 'pdf-to-ppt', 'word-to-pdf', 'excel-to-pdf']

def sync_tool(slug, lang):
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    # Change lang attribute
    html = html.replace('<html lang="en"', f'<html lang="{lang}"')
    # Update canonical
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/{slug}">',
        html
    )
    # The English tool already has hreflang for all langs including zh.
    # For language dir copies, we keep all hreflang links (they're absolute URLs).
    # Localize internal tool links
    html = html.replace('href="/tools/', f'href="/{lang}/tools/')
    # Logo link
    html = html.replace('href="/" class="logo"', f'href="/{lang}/" class="logo"')
    # Write
    dst_dir = os.path.join(BASE, lang, 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f'{slug}.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return dst

def main():
    print('=== Syncing batch 1 tools to language dirs ===')
    for slug in NEW_TOOLS:
        for lang in LANGS:
            dst = sync_tool(slug, lang)
            print(f'  ✅ {lang}/tools/{slug}.html')
    print(f'\nDone: {len(NEW_TOOLS)} tools × {len(LANGS)} langs = {len(NEW_TOOLS)*len(LANGS)} files')

if __name__ == '__main__':
    main()
