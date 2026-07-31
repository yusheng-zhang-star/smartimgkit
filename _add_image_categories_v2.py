#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为图片工具添加分类标题（精确版本 - 只在tools-grid内操作）"""
import os

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

# 分类标题定义 - 在指定工具卡片之前插入
# 使用精确的锚点：工具卡片的 <a href="/tools/xxx" class="tool-card">
CATEGORY_INSERTIONS = [
    {
        "before_slug": "compressor",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin:8px 0 4px 0;">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📊 Optimize &amp; Convert</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Compress, convert formats, and optimize images for web.</p>
          </div>
'''
    },
    {
        "before_slug": "resizer",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✂️ Resize &amp; Crop</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Resize, crop, and split images to any size.</p>
          </div>
'''
    },
    {
        "before_slug": "image-filters",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎨 Edit &amp; Effects</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Filters, adjustments, rotations, and creative effects.</p>
          </div>
'''
    },
    {
        "before_slug": "background-remover",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✨ AI Enhance</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">AI-powered background removal, upscaling, enhancement, and restoration.</p>
          </div>
'''
    },
    {
        "before_slug": "text-on-image",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎯 Create &amp; Design</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Add text, create memes, GIFs, social posts, and product photos.</p>
          </div>
'''
    },
    {
        "before_slug": "ocr",
        "header": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🔧 Utility &amp; Analyze</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">OCR, batch processing, color extraction, comparison, and metadata tools.</p>
          </div>
'''
    },
]

def add_image_categories(path):
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 检查是否已经有图片分类标题了
    if 'Optimize &amp; Convert' in content:
        print(f"  = {path} (already has image categories)")
        return False
    
    # 找到 tools-grid 的开始和结束位置
    grid_start = content.find('<div class="tools-grid">')
    if grid_start < 0:
        print(f"  SKIP: {path} tools-grid not found")
        return False
    
    # 在 tools-grid 范围内操作
    grid_content = content[grid_start:]
    
    # 从后往前插入，避免位置偏移
    for item in reversed(CATEGORY_INSERTIONS):
        slug = item["before_slug"]
        # 使用精确的锚点：只匹配工具卡片 class="tool-card"
        marker = f'/tools/{slug}" class="tool-card"'
        idx = grid_content.find(marker)
        if idx > 0:
            # 找到这个卡片 <a 的开始位置
            card_start = grid_content.rfind('<a ', 0, idx)
            if card_start > 0:
                grid_content = grid_content[:card_start] + '\n' + item["header"] + grid_content[card_start:]
    
    content = content[:grid_start] + grid_content
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {path}")
        return True
    else:
        print(f"  = {path} (no changes)")
        return False


def main():
    print("Adding image tool categories to all homepages (precise mode)...\n")
    changed = 0
    for lang_dir, lang_code in LANG_DIRS:
        path = os.path.join(ROOT, lang_dir, "index.html")
        if add_image_categories(path):
            changed += 1
    
    print(f"\nDone! Updated {changed} homepages.")


if __name__ == '__main__':
    main()
