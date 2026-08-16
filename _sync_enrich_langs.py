#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sync enriched English tool pages to all non-zh language dirs (es,pt,id,fr,vi,ar).
Copies the enriched /tools/*.html with lang/canonical/link localization.
Enrichment content stays English (consistent with existing language-page pattern)."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
SRC_DIR = os.path.join(BASE, 'tools')
LANGS = ['es', 'pt', 'id', 'fr', 'vi', 'ar']

def sync_tool(slug, lang):
    src = os.path.join(SRC_DIR, f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', f'<html lang="{lang}"')
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s\.html">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/{slug}.html">',
        html
    )
    # Some canonicals may not have .html; handle both
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/{slug}">',
        html
    )
    # Localize tool links + logo (only /tools/ and root logo, not /css /js /privacy etc.)
    html = html.replace('href="/tools/', f'href="/{lang}/tools/')
    html = html.replace('href="/" class="logo"', f'href="/{lang}/" class="logo"')
    dst_dir = os.path.join(BASE, lang, 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f'{slug}.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    tools = [f[:-5] for f in os.listdir(SRC_DIR) if f.endswith('.html')]
    print(f'Syncing {len(tools)} enriched tools to {len(LANGS)} languages...')
    count = 0
    for slug in sorted(tools):
        for lang in LANGS:
            sync_tool(slug, lang)
            count += 1
    print(f'Done: {count} files synced ({len(tools)} tools x {len(LANGS)} langs)')

if __name__ == '__main__':
    main()
