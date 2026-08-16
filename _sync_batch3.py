#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sync batch 3 tools (html/txt/csv/epub to pdf) to all language dirs (es,pt,id,fr,vi,ar,zh)."""
import os, re

BASE = r'E:\网站项目\smartimgkit'
LANGS = ['es', 'pt', 'id', 'fr', 'vi', 'ar']
NEW_TOOLS = ['html-to-pdf', 'txt-to-pdf', 'csv-to-pdf', 'epub-to-pdf']

TOOL_ZH = {
    'html-to-pdf': ('HTML 转 PDF – 免费', '🌐 HTML 转 PDF', '将 HTML 文件或代码转换为可搜索的 PDF。上传 .html 文件或粘贴代码，输出真实文本 PDF。100% 浏览器端处理。'),
    'txt-to-pdf': ('TXT 转 PDF – 免费', '📝 TXT 转 PDF', '将纯文本文件（.txt/.md/.log）转换为整洁、可搜索的 PDF。可选字号和页面大小。浏览器端处理。'),
    'csv-to-pdf': ('CSV 转 PDF – 免费', '📊 CSV 转 PDF', '将 CSV 文件转换为格式化的 PDF 表格。正确处理带引号的字段、字段内逗号和大批量数据。浏览器端。'),
    'epub-to-pdf': ('EPUB 转 PDF – 免费', '📚 EPUB 转 PDF', '将 EPUB 电子书转换为可搜索的 PDF。按阅读顺序提取章节、标题和段落。100% 浏览器端，不上传。'),
}


def sync_tool_lang(slug, lang):
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', f'<html lang="{lang}"')
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/{slug}">',
        html
    )
    html = html.replace('href="/tools/', f'href="/{lang}/tools/')
    html = html.replace('href="/" class="logo"', f'href="/{lang}/" class="logo"')
    dst_dir = os.path.join(BASE, lang, 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f'{slug}.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return dst


def sync_tool_zh(slug):
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', '<html lang="zh"')
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/zh/tools/{slug}">',
        html
    )
    html = html.replace('href="/tools/', 'href="/zh/tools/')
    html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
    zh_title, zh_h1, zh_desc = TOOL_ZH[slug]
    html = re.sub(r'<title>.*?</title>', '<title>%s | SmartImgKit</title>' % zh_title, html, count=1)
    html = re.sub(r'(<meta name="description" content=").*?(">)', r'\1%s\2' % zh_desc, html, count=1)
    html = re.sub(r'(<meta property="og:description" content=").*?(">)', r'\1%s\2' % zh_desc, html, count=1)
    html = re.sub(r'(<meta name="twitter:description" content=").*?(">)', r'\1%s\2' % zh_desc, html, count=1)
    html = re.sub(r'(<h1[^>]*>).*?(</h1>)', r'\1%s\2' % zh_h1, html, count=1)
    dst_dir = os.path.join(BASE, 'zh', 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f'{slug}.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return dst


def main():
    print('=== Syncing batch 3 tools to language dirs ===')
    count = 0
    for slug in NEW_TOOLS:
        for lang in LANGS:
            sync_tool_lang(slug, lang)
            print(f'  ✅ {lang}/tools/{slug}.html')
            count += 1
        sync_tool_zh(slug)
        print(f'  ✅ zh/tools/{slug}.html  (translated)')
        count += 1
    print(f'\nDone: {len(NEW_TOOLS)} tools × 7 langs = {count} files')


if __name__ == '__main__':
    main()
