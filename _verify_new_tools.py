#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证所有新生成工具页面的正确性"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

NEW_TOOL_SLUGS = [
    # Batch 1: Text/Dev tools (11)
    "word-counter", "json-formatter", "regex-tester",
    "url-encoder", "uuid-generator", "password-generator",
    "case-converter", "text-sorter", "text-diff",
    "find-replace", "html-entities",
    # Batch 2: PDF tools (6)
    "pdf-merge", "pdf-split", "pdf-compress",
    "pdf-delete-pages", "pdf-rotate", "pdf-extract-pages",
    # Batch 3: Video tools (7)
    "video-compress", "video-to-gif", "video-to-mp3",
    "video-crop", "video-frames", "video-speed", "video-rotate",
]

LANG_DIRS = ["", "es/", "pt/", "id/", "fr/", "vi/", "ar/"]


def check_page(filepath):
    """检查单个页面"""
    errors = []
    warnings = []
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 检查基本结构
    if '<!DOCTYPE html>' not in html:
        errors.append("Missing DOCTYPE")
    if 'id="fileInput"' not in html and 'id="textInput"' not in html and 'word-counter' not in filepath:
        errors.append("Missing file input or text input")

    # 2. 检查是否有 dropzone
    if any(t in filepath for t in ['pdf-', 'video-']):
        if 'id="dropzone"' not in html:
            errors.append("Missing dropzone")
        if 'class="dropzone"' not in html:
            errors.append("Missing dropzone class")

    # 3. 检查JS是否包含错误处理（try-catch in handleFile）
    if 'handleFile' in html:
        # 检查handleFile中的onload回调是否有try-catch
        handlefile_match = re.search(r'function handleFile\(.*?\)\s*\{(.*?)(?=\n  function |\n  processBtn|\n  resetBtn|\n}\)\(\);)', html, re.DOTALL)
        if handlefile_match:
            func_body = handlefile_match.group(1)
            if 'onload' in func_body and 'try {' not in func_body:
                errors.append("handleFile onload callback missing try-catch")
            if 'statusSection.textContent' not in func_body:
                warnings.append("handleFile missing status feedback")

    # 4. 检查processBtn是否有错误处理
    if 'processBtn' in html or 'mergeBtn' in html or 'splitBtn' in html:
        btn_match = re.search(r'(?:processBtn|mergeBtn|splitBtn)\.addEventListener\(\'click\',\s*async\s*\(\)\s*=>\s*\{(.*?)(?=\n  \}\);|\n  function |\n}\)\(\);)', html, re.DOTALL)
        if btn_match:
            handler_body = btn_match.group(1)
            if 'try {' not in handler_body:
                errors.append("Process button handler missing try-catch")
            if 'catch' not in handler_body:
                errors.append("Process button handler missing catch")

    # 5. 检查是否有状态显示区域
    if 'id="statusSection"' not in html:
        errors.append("Missing statusSection")

    # 6. 检查控件区
    if 'id="controlsSection"' not in html and 'word-counter' not in filepath:
        errors.append("Missing controlsSection")

    return errors, warnings


def main():
    total_pages = 0
    total_errors = 0
    total_warnings = 0
    failed_pages = []

    for slug in NEW_TOOL_SLUGS:
        for lang_dir in LANG_DIRS:
            filepath = os.path.join(ROOT, lang_dir, "tools", f"{slug}.html")
            if not os.path.exists(filepath):
                print(f"  MISSING: {filepath}")
                total_errors += 1
                failed_pages.append((filepath, ["File not found"]))
                continue

            total_pages += 1
            errors, warnings = check_page(filepath)
            if errors:
                total_errors += len(errors)
                failed_pages.append((filepath, errors))
                print(f"  ✗ {os.path.join(lang_dir, slug)}.html: {len(errors)} errors")
                for e in errors:
                    print(f"    - {e}")
            if warnings:
                total_warnings += len(warnings)

    print(f"\n{'='*60}")
    print(f"Total pages checked: {total_pages}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    print(f"Failed pages: {len(failed_pages)}")
    if total_errors == 0:
        print("✓ ALL PAGES PASSED!")
        return 0
    else:
        print("✗ SOME PAGES FAILED!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
