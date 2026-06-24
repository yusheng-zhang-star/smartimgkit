#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
i18n_build.py — 从英文 HTML + 翻译 JSON 生成各语言版工具页

用法：
  python i18n_build.py              # 构建所有已配置的语言
  python i18n_build.py es         # 仅构建 es
  python i18n_build.py es pt id  # 构建指定语言

原理：
  1. 读 tools/{slug}.html（英文版，代码唯一来源）
  2. 读 i18n/{lang}/tools/{slug}.json（翻译映射）
  3. 逐条做字符串替换
  4. 写回 {lang}/tools/{slug}.html

JSON 格式：
{
  "meta": {
    "tool": "pdf-to-image",
    "lang": "es",
    "slug": "pdf-to-image"
  },
  "strings": {
    "PDF to Image — Convert PDF Pages to PNG/JPG/WebP Free | SmartImgKit":
      "PDF a Imagen Online Gratis — SmartImgKit",
    "Convert PDF pages to high-quality images online for free...":
      "Convierte páginas PDF a PNG, JPG o WebP...",
    ...
  },
  "js_strings": {
    "Please upload a PDF first.": "Sube un PDF primero.",
    ...
  }
}

注意：
  - strings 匹配区分大小写，需和英文版完全一致
  - js_strings 会替换 JS 中的 alert/confirm 字符串
  - 运行前备份目标文件
"""

import json
import os
import sys
import shutil
import re

TOOLS_DIR = 'tools'
I18N_DIR  = 'i18n'
SUPPORTED_LANGS = ['es', 'pt', 'id']


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def backup(path):
    if os.path.exists(path):
        bak = path + '.bak'
        shutil.copy2(path, bak)
        return bak
    return None


def apply_string_replacements(html, strings):
    """对 HTML 做字符串替换（最简单直接的方式）"""
    for eng, trans in strings.items():
        if eng in html:
            html = html.replace(eng, trans)
        else:
            print(f"  ⚠ 未匹配: {eng[:60]}")
    return html


def apply_js_string_replacements(html, js_strings):
    """
    替换 JS 中的字符串字面量。
    将  alert('...') / alert("...") 中的 ... 替换
    暂时只做简单替换（不做 AST 解析）
    """
    def repl_alert(m):
        q       = m.group(1) or m.group(2)   # 引号类型
        eng_txt = m.group(3) or m.group(4)
        if eng_txt in js_strings:
            new_txt = js_strings[eng_txt]
            return f"alert({q}{new_txt}{q})"
        return m.group(0)

    def repl_confirm(m):
        q       = m.group(1) or m.group(2)
        eng_txt = m.group(3) or m.group(4)
        if eng_txt in js_strings:
            new_txt = js_strings[eng_txt]
            return f"confirm({q}{new_txt}{q})"
        return m.group(0)

    # alert('...')  or alert("...")
    html = re.sub(
        r'''alert\(\s*(['"])(.*?)\1\s*\)''',
        repl_alert, html, flags=re.DOTALL
    )
    # confirm('...') or confirm("...")
    html = re.sub(
        r'''confirm\(\s*(['"])(.*?)\1\s*\)''',
        repl_confirm, html, flags=re.DOTALL
    )
    return html


def patch_lang_hreflang(html, lang):
    """修正 hreflang 和 canonic al URL"""
    # canonic al
    html = re.sub(
        r'<link rel="canonical" href="https://smartimgkit\.com/tools/([^"]+)"',
        f'<link rel="canonical" href="https://smartimgkit.com/{lang}/tools/\\1"',
        html
    )
    # og:url
    html = re.sub(
        r'<meta property="og:url" content="https://smartimgkit\.com/tools/([^"]+)"',
        f'<meta property="og:url" content="https://smartimgkit.com/{lang}/tools/\\1"',
        html
    )
    # twitter: 不用改（canonic al 已够）
    # lang 属性
    html = re.sub(r'<html lang="en"', f'<html lang="{lang}"', html)
    return html


def build_tool(tool_slug, lang, strings, js_strings):
    """为一个语言构建一个工具页"""
    en_path = os.path.join(TOOLS_DIR, f"{tool_slug}.html")
    lang_path = os.path.join(lang, 'tools', f"{tool_slug}.html")

    if not os.path.exists(en_path):
        print(f"  ✗ 英文源文件不存在: {en_path}")
        return False

    os.makedirs(os.path.join(lang, 'tools'), exist_ok=True)
    backup(lang_path)

    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1) HTML 文案替换
    html = apply_string_replacements(html, strings)

    # 2) JS 字符串替换
    if js_strings:
        html = apply_js_string_replacements(html, js_strings)

    # 3) hreflang / canonic al / lang 属性
    html = patch_lang_hreflang(html, lang)

    with open(lang_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ {lang}/tools/{tool_slug}.html")
    return True


def main():
    args = sys.argv[1:]
    if not args:
        langs = SUPPORTED_LANGS
    else:
        langs = [l for l in args if l in SUPPORTED_LANGS]
        if not langs:
            print(f"用法: python {sys.argv[0]} [es|pt|id] ...")
            sys.exit(1)

    # 扫瞄 tools/*.html 作为要构建的工具列表
    tools = [f[:-5] for f in os.listdir(TOOLS_DIR) if f.endswith('.html')]
    print(f"发现 {len(tools)} 个工具: {', '.join(tools)}")
    print(f"目标语言: {', '.join(langs)}\n")

    total = 0
    for tool in tools:
        for lang in langs:
            json_path = os.path.join(I18N_DIR, lang, 'tools', f"{tool}.json")
            if not os.path.exists(json_path):
                print(f"  — 跳过 {lang}/{tool}（无 JSON: {json_path}）")
                continue

            data = load_json(json_path)
            strings   = data.get('strings', {})
            js_strings = data.get('js_strings', {})
            ok = build_tool(tool, lang, strings, js_strings)
            if ok:
                total += 1

    print(f"\n✓ 完成：共生成 {total} 个文件")


if __name__ == '__main__':
    main()
