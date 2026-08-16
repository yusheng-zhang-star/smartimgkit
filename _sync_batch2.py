#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sync batch 2 PDF editing tools to all language directories (es, pt, id, fr, vi, ar, zh).

- For es/pt/id/fr/vi/ar: copy English tool, change lang, canonical, localize links.
- For zh: additionally apply SEO translations (title/h1/desc) per _setup_chinese.py convention.
"""
import os, re

BASE = r'E:\网站项目\smartimgkit'
LANGS = ['es', 'pt', 'id', 'fr', 'vi', 'ar']
NEW_TOOLS = ['pdf-editor', 'pdf-annotate', 'pdf-number-pages', 'pdf-crop', 'pdf-organize', 'pdf-compare', 'pdf-redact']

# zh SEO translations: slug -> (zh_title, zh_h1, zh_desc)
TOOL_ZH = {
    'pdf-editor': ('PDF 编辑器 – 免费', '✏️ PDF 编辑器', '在 PDF 上添加文字、图片和形状。点击页面放置元素，调整字体、大小和颜色。100% 浏览器端处理，不上传。'),
    'pdf-annotate': ('PDF 批注 – 免费', '🖍️ PDF 批注', '为 PDF 添加高亮、下划线和文本注释。办公常用。浏览器端处理，不上传服务器。'),
    'pdf-number-pages': ('PDF 加页码 – 免费', '🔢 PDF 加页码', '为 PDF 添加页码。可选位置（顶部/底部、左/中/右）、格式和起始页码。浏览器端处理。'),
    'pdf-crop': ('PDF 裁剪 – 免费', '✂️ PDF 裁剪', '裁剪 PDF 页面区域。可视化拖选裁剪范围，可应用到当前页或所有页。隐私优先，不上传。'),
    'pdf-organize': ('PDF 排序整理 – 免费', '📋 PDF 排序整理', '拖拽排序 PDF 页面，删除、复制页面。可视化缩略图管理。浏览器端处理，不上传。'),
    'pdf-compare': ('PDF 对比 – 免费', '🔍 PDF 对比', '并排对比两个 PDF 的页面差异。逐页渲染并标记相同/不同。隐私优先，不上传。'),
    'pdf-redact': ('PDF 隐藏敏感信息 – 免费', '⬛ PDF 隐藏敏感信息', '在 PDF 上绘制黑块覆盖敏感信息。隐私刚需，本地处理，不上传服务器。契合隐私卖点。'),
}


def sync_tool_lang(slug, lang):
    """Sync to a non-zh language: copy English tool with lang/canonical/link localization."""
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', f'<html lang="{lang}"')
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/{slug}">',
        html
    )
    # Localize internal tool links + logo
    html = html.replace('href="/tools/', f'href="/{lang}/tools/')
    html = html.replace('href="/" class="logo"', f'href="/{lang}/" class="logo"')
    dst_dir = os.path.join(BASE, lang, 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f'{slug}.html')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(html)
    return dst


def sync_tool_zh(slug):
    """Sync to zh: copy English tool, localize, and apply SEO translations."""
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', '<html lang="zh"')
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
        f'<link rel="canonical" href="https://smartimgkit.com/zh/tools/{slug}">',
        html
    )
    # zh hreflang already present in English source (added during creation); ensure it points to zh
    # Localize links + logo
    html = html.replace('href="/tools/', 'href="/zh/tools/')
    html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
    # Apply SEO translations
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
    print('=== Syncing batch 2 tools to language dirs ===')
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
