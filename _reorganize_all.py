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

# 图片工具按分类分组的顺序
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

def extract_tool_cards(content):
    """从tools-grid中提取所有工具卡片，返回{slug: html}字典和原始顺序"""
    grid_start = content.find('<div class="tools-grid">')
    if grid_start < 0:
        return None, None, None
    
    # 找到grid的结束位置（找Text & Developer Tools分类标题或grid结束）
    # 先找现有的 Text & Developer Tools 分类标题（作为图片工具结束的标记）
    text_dev_marker = 'Text &amp; Developer Tools'
    text_dev_idx = content.find(text_dev_marker, grid_start)
    
    if text_dev_idx > 0:
        # 找到 Text & Developer Tools 分类标题前的位置
        grid_end = content.rfind('</div>', grid_start, text_dev_idx)
        # 实际上我们只需要图片工具，到 Text & Developer Tools 之前
        end_pos = text_dev_idx
    else:
        # 找grid结束
        grid_end = content.find('</div>', grid_start + 30)
        end_pos = grid_end
    
    grid_section = content[grid_start:end_pos]
    
    # 提取每个工具卡片
    cards = {}
    order = []
    
    # 匹配 <a href="/tools/xxx" class="tool-card"> ... </a>
    pattern = r'<a href="/tools/([^"]+)" class="tool-card">.*?</a>'
    matches = re.findall(pattern, grid_section, re.DOTALL)
    
    for match in re.finditer(pattern, grid_section, re.DOTALL):
        slug = match.group(1)
        html = match.group(0)
        cards[slug] = html
        order.append(slug)
    
    return cards, order, grid_start, end_pos


def reorganize_index(path):
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 提取所有工具卡片
    result = extract_tool_cards(content)
    if result[0] is None:
        print(f"  SKIP: {path} tools-grid not found")
        return False
    
    cards, order, grid_start, end_pos = result
    
    # 构建重新组织后的图片工具部分
    new_image_section = '        <div class="tools-grid">\n'
    
    for cat_idx, category in enumerate(IMAGE_CATEGORIES):
        # 添加分类标题
        if cat_idx == 0:
            # 第一个分类没有顶部边框
            header_style = 'margin:8px 0 4px 0;'
        else:
            header_style = 'margin-top:8px;padding-top:16px;border-top:1px solid var(--border);'
        
        new_image_section += f'''          <div class="tools-category-header" style="grid-column:1/-1;{header_style}">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">{category["title"]}</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">{category["desc"]}</p>
          </div>
'''
        
        # 添加该分类下的工具卡片
        for slug in category["slugs"]:
            if slug in cards:
                # 确保卡片有正确的缩进
                card_html = cards[slug].strip()
                new_image_section += card_html + '\n'
            else:
                print(f"  WARN: {slug} not found in cards")
    
    # 保留原始内容中图片工具之后的部分（Text & Dev, PDF, Video 等）
    new_content = content[:grid_start] + new_image_section + '\n' + content[end_pos:]
    
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
