#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全面静态分析所有24个新工具的功能完整性"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

TOOL_SLUGS = [
    # Text/Dev
    "word-counter", "json-formatter", "regex-tester", "url-encoder",
    "uuid-generator", "password-generator", "case-converter", "text-sorter",
    "text-diff", "text-find-replace", "html-encoder",
    # PDF
    "pdf-merge", "pdf-split", "pdf-compress", "pdf-delete-pages",
    "pdf-rotate", "pdf-extract-pages",
    # Video
    "video-compressor", "video-to-gif", "video-to-mp3", "video-crop",
    "video-to-frames", "video-speed", "video-rotate",
]

def analyze_tool(slug):
    filepath = os.path.join(ROOT, "tools", f"{slug}.html")
    result = {"slug": slug, "exists": os.path.exists(filepath), "issues": [], "positives": []}
    
    if not result["exists"]:
        result["issues"].append("文件不存在")
        return result
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. 检查是否有主按钮
    has_primary_btn = bool(re.search(r'class="[^"]*btn-primary[^"]*"', html))
    if has_primary_btn:
        result["positives"].append("主按钮(btn-primary)")
    else:
        result["issues"].append("缺少主按钮(btn-primary)")
    
    # 2. 检查是否有按钮ID
    btn_id_match = re.search(r'<button[^>]*id="([^"]+)"[^>]*class="[^"]*btn-primary', html)
    if btn_id_match:
        result["btn_id"] = btn_id_match.group(1)
        result["positives"].append(f"按钮ID: {btn_id_match.group(1)}")
    
    # 3. 检查是否有事件监听器
    has_listener = bool(re.search(r'addEventListener', html))
    if has_listener:
        result["positives"].append("事件监听器(addEventListener)")
    else:
        result["issues"].append("缺少事件监听器")
    
    # 4. 检查是否有onclick处理
    has_onclick = bool(re.search(r'onclick\s*=', html))
    if has_onclick:
        result["positives"].append("onclick处理")
    
    # 5. 检查是否有文件输入
    has_file_input = bool(re.search(r'type="file"', html))
    if has_file_input:
        result["positives"].append("文件输入")
    
    # 6. 检查是否有状态显示
    has_status = bool(re.search(r'id="[^"]*(?:status|statusMsg|result|output)[^"]*"', html))
    if has_status:
        result["positives"].append("状态/结果显示")
    else:
        result["issues"].append("缺少状态/结果显示")
    
    # 7. 检查是否有try-catch（错误处理）
    has_try_catch = bool(re.search(r'try\s*\{', html))
    if has_try_catch:
        result["positives"].append("错误处理(try-catch)")
    
    # 8. PDF工具特殊检查
    if slug.startswith("pdf-"):
        has_pdf_lib = "pdf-lib" in html or "PDFLib" in html
        if has_pdf_lib:
            result["positives"].append("pdf-lib集成")
        else:
            result["issues"].append("缺少pdf-lib集成")
        
        has_blob = bool(re.search(r'Blob\(|createObjectURL', html))
        if has_blob:
            result["positives"].append("Blob/下载支持")
        else:
            result["issues"].append("缺少Blob/下载支持")
        
        has_file_reader = bool(re.search(r'FileReader|readAsArrayBuffer|readAsDataURL', html))
        if has_file_reader:
            result["positives"].append("FileReader文件读取")
        else:
            result["issues"].append("缺少FileReader文件读取")
    
    # 9. 视频工具特殊检查
    if slug.startswith("video-"):
        has_ffmpeg = "ffmpeg" in html.lower() or "FFmpeg" in html
        if has_ffmpeg:
            result["positives"].append("ffmpeg.wasm集成")
        else:
            result["issues"].append("缺少ffmpeg.wasm集成")
        
        has_blob = bool(re.search(r'Blob\(|createObjectURL', html))
        if has_blob:
            result["positives"].append("Blob/下载支持")
        else:
            result["issues"].append("缺少Blob/下载支持")
    
    # 10. 文本工具特殊检查
    text_tools = ["word-counter", "json-formatter", "regex-tester", "url-encoder",
                  "uuid-generator", "password-generator", "case-converter", "text-sorter",
                  "text-diff", "text-find-replace", "html-encoder"]
    if slug in text_tools:
        has_textarea = bool(re.search(r'<textarea', html))
        if has_textarea:
            result["positives"].append("文本输入(textarea)")
        
        has_output = bool(re.search(r'<pre|id="output"|id="result"', html))
        if has_output:
            result["positives"].append("输出显示区")
    
    return result


def main():
    print("=" * 80)
    print("静态功能完整性分析 - 24个新工具")
    print("=" * 80)
    
    all_results = []
    for slug in TOOL_SLUGS:
        result = analyze_tool(slug)
        all_results.append(result)
        
        status = "✓" if not result["issues"] else "✗"
        print(f"\n{status} {result['slug']}")
        if result["positives"]:
            print(f"  功能: {', '.join(result['positives'])}")
        if result["issues"]:
            print(f"  问题: {', '.join(result['issues'])}")
    
    # 汇总
    print("\n" + "=" * 80)
    total = len(all_results)
    passed = sum(1 for r in all_results if not r["issues"])
    failed = total - passed
    print(f"汇总: {passed}/{total} 通过, {failed} 有问题")
    
    if failed > 0:
        print("\n有问题的工具:")
        for r in all_results:
            if r["issues"]:
                print(f"  ✗ {r['slug']}: {', '.join(r['issues'])}")


if __name__ == '__main__':
    main()
