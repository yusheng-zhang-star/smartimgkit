#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重新组织首页工具分类（保持URL不变）"""
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

CATEGORY_HEADERS = {
    "text_dev": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📝 Text &amp; Developer Tools</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Text processing, code formatting, and developer utilities.</p>
          </div>
''',
    "pdf": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📄 PDF Tools</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Merge, split, compress, rotate, and edit PDF files in your browser.</p>
          </div>
''',
    "video": '''          <div class="tools-category-header" style="grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);">
            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎬 Video Tools</h3>
            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Compress, convert, trim, and edit videos with ffmpeg.wasm in your browser.</p>
          </div>
''',
}

def reorganize_index(path):
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 把 "All Image Tools" 改为 "All Tools"
    content = content.replace("<h2>All Image Tools</h2>", "<h2>All Tools</h2>")
    
    # 2. 在 photo-restoration 之后、word-counter 之前插入 Text & Dev 分类标题
    # 找到 photo-restoration 卡片的结束位置
    photo_marker = '/tools/photo-restoration'
    if photo_marker not in content:
        photo_marker = '/tools/photo-restoration'
    
    # 找 photo-restoration 的 </a> 结束
    idx = content.find(photo_marker)
    if idx > 0:
        end_a = content.find('</a>', idx)
        if end_a > 0:
            insert_pos = end_a + len('</a>')
            # 检查是否已经插入了分类标题
            if 'tools-category-header' not in content:
                content = content[:insert_pos] + '\n' + CATEGORY_HEADERS["text_dev"] + content[insert_pos:]
    
    # 3. 在 html-encoder 之后、pdf-merge 之前插入 PDF 分类标题
    html_enc = '/tools/html-encoder'
    if html_enc in content:
        idx = content.find(html_enc)
        end_a = content.find('</a>', idx)
        if end_a > 0:
            insert_pos = end_a + len('</a>')
            # 检查是否已经有 pdf-merge
            if '/tools/pdf-merge' in content[insert_pos:insert_pos+500]:
                # 只插入一次
                if CATEGORY_HEADERS["pdf"].strip().split('\n')[1].strip() not in content:
                    content = content[:insert_pos] + '\n' + CATEGORY_HEADERS["pdf"] + content[insert_pos:]
    
    # 4. 在 pdf-extract-pages 之后、video 之前插入 Video 分类标题
    pdf_ext = '/tools/pdf-extract-pages'
    if pdf_ext in content:
        idx = content.find(pdf_ext)
        end_a = content.find('</a>', idx)
        if end_a > 0:
            insert_pos = end_a + len('</a>')
            # 检查是否已经有 video-compressor 或 video-to-gif
            next_section = content[insert_pos:insert_pos+500]
            if '/tools/video' in next_section:
                if CATEGORY_HEADERS["video"].strip().split('\n')[1].strip() not in content:
                    content = content[:insert_pos] + '\n' + CATEGORY_HEADERS["video"] + content[insert_pos:]
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {path}")
        return True
    else:
        print(f"  = {path} (no changes)")
        return False


def main():
    print("Reorganizing tool categories on all homepages...\n")
    changed = 0
    for lang_dir, lang_code in LANG_DIRS:
        path = os.path.join(ROOT, lang_dir, "index.html")
        if reorganize_index(path):
            changed += 1
    
    print(f"\nDone! Updated {changed} homepages.")


if __name__ == '__main__':
    main()
