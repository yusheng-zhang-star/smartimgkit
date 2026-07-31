#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重新组织首页工具卡片顺序（按分类分组，保持URL不变）"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

LANG_DIRS = [
    ("", "en"),
    ("es/", "es"),
    ("pt/", "pt"),
    ("id/", "id"),
    ("fr/", "fr"),
    ("vi/", "vi"),
    ("ar/", "ar"),
]

IMAGE_CATEGORIES = [
    {
        "title": "📊 Optimize & Convert",
        "desc": "Compress, convert formats, and optimize images for web.",
        "slugs": [
            "compressor", "converter", "heic-converter", "pdf-to-image",
            "svg-to-png", "avif-support", "image-to-pdf"
        ]
    },
    {
        "title": "✂️ Resize & Crop",
        "desc": "Resize, crop, and split images to any size.",
        "slugs": [
            "resizer", "cropper", "print-resizer", "circle-crop", "image-splitter"
        ]
    },
    {
        "title": "🎨 Edit & Effects",
        "desc": "Filters, adjustments, rotations, and creative effects.",
        "slugs": [
            "image-filters", "image-rotator", "image-adjust", "image-border",
            "image-flip", "image-grayscale", "image-shadow", "image-merger",
            "watermark"
        ]
    },
    {
        "title": "✨ AI Enhance",
        "desc": "AI-powered background removal, upscaling, enhancement, and restoration.",
        "slugs": [
            "background-remover", "image-upscaler", "image-enhancer",
            "face-blur", "photo-restoration"
        ]
    },
    {
        "title": "🎯 Create & Design",
        "desc": "Add text, create memes, GIFs, social posts, and product photos.",
        "slugs": [
            "text-on-image", "meme-generator", "gif-editor", "favicon-generator",
            "screenshot-to-image", "social-media-post", "id-photo",
            "product-white-background"
        ]
    },
    {
        "title": "🔧 Utility & Analyze",
        "desc": "OCR, batch processing, color extraction, comparison, and metadata tools.",
        "slugs": [
            "ocr", "bulk-processor", "color-palette", "image-compare",
            "base64", "metadata-viewer", "image-exif-remover"
        ]
    },
]

CARD_PATTERN = r'<a href="(?:/[^/]+)?/tools/([^"]+)" class="tool-card">.*?</a>'

def reorganize_index(path):
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    grid_start = content.find('<div class="tools-grid">')
    if grid_start < 0:
        print(f"  SKIP: {path} tools-grid not found")
        return False
    
    # 使用第一个文本工具 word-counter 作为图片工具区域结束的标记
    end_marker = 'word-counter'
    end_idx = content.find(end_marker, grid_start)
    if end_idx < 0:
        print(f"  SKIP: {path} word-counter marker not found")
        return False
    
    # 找到 word-counter 卡片之前的位置
    section_end = content.rfind('<a ', grid_start, end_idx)
    if section_end < 0:
        section_end = end_idx
    
    grid_section = content[grid_start:section_end]
    
    # 提取所有卡片 {slug: html}
    cards = {}
    for match in re.finditer(CARD_PATTERN, grid_section, re.DOTALL):
        slug = match.group(1)
        cards[slug] = match.group(0)
    
    print(f"  Found {len(cards)} image tool cards")
    
    if len(cards) < 30:
        print(f"  WARN: Too few cards found, skipping")
        return False
    
    # 构建新的图片工具部分
    new_section = '        <div class="tools-grid">\n'
    
    for cat_idx, category in enumerate(IMAGE_CATEGORIES):
        if cat_idx == 0:
            header_style = 'margin:8px 0 4px 0;'
        else:
            header_style = 'margin-top:8px;padding-top:16px;border-top:1px solid var(--border);'
        
        new_section += f'''          <div class="tools-category-header" style="grid-column:1/-1;{header_style}">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">{category["title"]}</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">{category["desc"]}</p>
          </div>
'''
        
        for slug in category["slugs"]:
            if slug in cards:
                new_section += cards[slug] + '\n'
            else:
                print(f"  WARN: {slug} not found")
    
    new_content = content[:grid_start] + new_section + '\n' + content[section_end:]
    
    if new_content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {path}")
        return True
    else:
        print(f"  = {path} (no changes)")
        return False


def main():
    print("Reorganizing tool cards by category (URLs unchanged)...\n")
    changed = 0
    for lang_dir, lang_code in LANG_DIRS:
        path = os.path.join(ROOT, lang_dir, "index.html")
        if reorganize_index(path):
            changed += 1
    
    print(f"\nDone! Updated {changed} homepages.")


if __name__ == '__main__':
    main()
