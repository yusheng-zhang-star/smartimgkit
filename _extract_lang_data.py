#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_extract_lang_data.py — 从现有多语言 HTML 提取数据到 _tools_data_{LANG}.json

Usage:
  python _extract_lang_data.py es
  python _extract_lang_data.py pt
  python _extract_lang_data.py id
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def extract_from_html(html):
    """从单个工具的 HTML 提取所有字段"""
    result = {}

    # ── head metadata ──
    m = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    result['title'] = m.group(1).strip() if m else ''

    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html)
    result['description'] = m.group(1).strip() if m else ''

    m = re.search(r'<meta\s+name="keywords"\s+content="(.*?)"', html)
    result['keywords'] = m.group(1).strip() if m else ''

    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', html)
    result['canonical_url'] = m.group(1).strip() if m else ''

    m = re.search(r'<meta\s+name="theme-color"\s+content="(.*?)"', html)
    result['theme_color'] = m.group(1).strip() if m else '#6366f1'

    # ── OG / Twitter ──
    m = re.search(r'<meta\s+property="og:title"\s+content="(.*?)"', html)
    result['og_title'] = m.group(1).strip() if m else ''

    m = re.search(r'<meta\s+property="og:description"\s+content="(.*?)"', html)
    result['og_description'] = m.group(1).strip() if m else ''

    m = re.search(r'<meta\s+property="og:image"\s+content="(.*?)"', html)
    result['og_image'] = m.group(1).strip() if m else ''

    # ── slug from canonical ──
    canonical = result.get('canonical_url', '')
    slug = canonical.rsplit('/', 1)[-1] if '/' in canonical else ''
    result['slug'] = slug

    # ── h1 & subtitle ──
    m = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    result['h1'] = m.group(1).strip() if m else ''

    # subtitle: next <p> after tool-page-header
    m = re.search(r'<div class="tool-page-header">\s*<h1>.*?</h1>\s*<p>(.*?)</p>', html, re.DOTALL)
    result['subtitle'] = m.group(1).strip() if m else ''

    # ── breadcrumb last ──
    m = re.search(r'<nav class="breadcrumb">.*<span>([^<]+)</span>\s*</nav>', html, re.DOTALL)
    result['breadcrumb_last'] = m.group(1).strip() if m else ''

    # ── inline style ──
    m = re.search(r'<style>\s*\n(.*?)\n\s*</style>', html, re.DOTALL)
    result['inline_style'] = m.group(1).rstrip() if m else ''

    # ── workspace HTML ──
    m = re.search(
        r'<div class="tool-workspace">\s*\n(.*?)\n\s{6}</div>\s*\n\s*(?:<!-- Adsterra Banner 300x250|<section|<h2|{{HOWTO)',
        html, re.DOTALL
    )
    if not m:
        # fallback: match to 6-space </div> before any section marker
        m = re.search(
            r'<div class="tool-workspace">\s*\n(.*?)\n\s{6}</div>',
            html, re.DOTALL
        )
    if m:
        result['workspace_html'] = m.group(1).rstrip()
    else:
        result['workspace_html'] = ''

    # ── inline JS (the <script> after main.js) ──
    m = re.search(r'<script src="/js/main\.js[^>]*>\s*</script>\s*<script>\s*(.*?)</script>\s*<script src="/js/lang\.js">', html, re.DOTALL)
    if not m:
        m = re.search(r'<script src="/js/main\.js[^>]*>.*?</script>\s*<script>\s*(.*?)</script>', html, re.DOTALL)
    result['inline_js'] = m.group(1).strip() if m else ''

    # ── HOWTO ──
    m = re.search(r'(<section class="how-to-section">.*?</section>)', html, re.DOTALL)
    result['howto_html'] = m.group(1).strip() if m else ''

    # ── GUIDE ──
    m = re.search(r'<h2>(?:Guía|Panduan|Detailed\s+User\s+Guide|Guia).*?</h2>(.*?)(?=<section class="faq-section"|<section class="related-tools")', html, re.DOTALL)
    if not m:
        m = re.search(r'(<div class="guide-block">.*?</div>\s*</div>)?', html, re.DOTALL)
    result['guide_html'] = m.group(0).strip() if m and m.group(0).strip() else ''

    # ── FAQ ──
    m = re.search(r'(<section class="faq-section">.*?</section>)', html, re.DOTALL)
    result['faq_html'] = m.group(1).strip() if m else ''

    # ── related ──
    m = re.search(r'(<section class="related-tools">.*?</section>)', html, re.DOTALL)
    result['related_html'] = m.group(1).strip() if m else ''

    # ── JSON-LD ──
    ld_scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for ld in ld_scripts:
        try:
            obj = json.loads(ld.strip())
            ld_type = obj.get('@type', '')
            if ld_type == 'FAQPage':
                result['jsonld_faq'] = obj
            elif ld_type == 'HowTo':
                result['jsonld_howto'] = obj
            elif ld_type == 'WebApplication':
                result['jsonld_webapp'] = obj
        except:
            pass

    return result


def extract_lang_fields(html, lang):
    """从 HTML 提取语言级公共字段（只需从一个页面提取）"""
    fields = {}

    # lang attr
    m = re.search(r'<html lang="(.*?)"', html)
    fields['lang'] = m.group(1) if m else ''

    # nav HTML
    m = re.search(r'(<nav class="main-nav">.*?</nav>)', html, re.DOTALL)
    fields['nav_html'] = m.group(1).strip() if m else ''

    # lang switcher HTML
    m = re.search(r'(<div class="lang-switcher".*?</div>\s*</div>)\s*\n', html, re.DOTALL)
    if not m:
        m = re.search(r'(<div class="lang-switcher".*?</div>)', html, re.DOTALL)
    fields['lang_switcher_html'] = m.group(1).strip() if m else ''

    # footer HTML
    m = re.search(r'(<!-- Footer:.*?<footer class="site-footer">.*?</footer>)', html, re.DOTALL)
    if m:
        fields['footer_html'] = m.group(1).strip()
    else:
        m = re.search(r'(<footer class="site-footer">.*?</footer>)', html, re.DOTALL)
        fields['footer_html'] = m.group(1).strip() if m else ''

    # breadcrumb home/tools labels
    m = re.search(r'<nav class="breadcrumb"><a href="/">(.*?)</a>.*?<a href="(.*?)">(.*?)</a>', html, re.DOTALL)
    if m:
        fields['breadcrumb_home'] = m.group(1).strip()
        fields['breadcrumb_tools_url'] = m.group(2).strip()
        fields['breadcrumb_tools'] = m.group(3).strip()

    # tools_url — deterministic per language
    fields['tools_url'] = f'/{lang}/tools'

    return fields


def extract_lang(lang):
    """提取一个语言的所有工具数据"""
    tools_dir = os.path.join(ROOT, lang, 'tools')
    if not os.path.exists(tools_dir):
        print(f'ERROR: Directory not found: {tools_dir}')
        return

    html_files = sorted([f for f in os.listdir(tools_dir) if f.endswith('.html')])
    if not html_files:
        print(f'ERROR: No HTML files found in {tools_dir}')
        return

    print(f'Found {len(html_files)} HTML files for [{lang}]')

    # extract lang-level fields from first file
    first_html = os.path.join(tools_dir, html_files[0])
    with open(first_html, 'r', encoding='utf-8') as f:
        lang_fields = extract_lang_fields(f.read(), lang)
    print(f'  Lang-level fields extracted from {html_files[0]}')

    # extract tool data from each file
    tools = []
    errors = 0
    for filename in html_files:
        filepath = os.path.join(tools_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        tool_data = extract_from_html(html)
        
        # verify critical fields
        if not tool_data.get('h1'):
            print(f'  ⚠ {filename}: empty h1')
            errors += 1
        if not tool_data.get('workspace_html'):
            print(f'  ⚠ {filename}: empty workspace_html')
            errors += 1
            
        tools.append(tool_data)

    # assemble final data
    output = dict(lang_fields)
    output['tools'] = tools

    out_file = os.path.join(ROOT, f'_tools_data_{lang}.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f'\nWritten {len(tools)} tools to {out_file}')
    if errors:
        print(f'⚠ {errors} pages have missing fields — check manually')
    else:
        print('✅ All fields extracted successfully')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python _extract_lang_data.py <lang>  (es/pt/id)')
        sys.exit(1)
    extract_lang(sys.argv[1])
