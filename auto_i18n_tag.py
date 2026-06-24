#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_i18n_tag.py — 自动给英文工具页加 data-i18n 标记

用法：python auto_i18n_tag.py tools/pdf-to-image.html

功能：
1. 解析 HTML，找到所有用户可见文案（text node、attribute）
2. 自动加 data-i18n="key" 属性
3. 生成 i18n/en/tools/pdf-to-image.json（英文文案库）
4. 输出标记好的 HTML

key 命名规则：
  title_*       → <title> 相关
  meta_*         → meta 标签
  h1, h2, h3   → 标题
  p_*            → 段落
  btn_*          → 按钮
  label_*        → label
  option_*       → select option
  faq_q_*       → FAQ 问题
  faq_a_*       → FAQ 回答
  guide_*        → 指南文案
  related_*      → 相关工具
  footer_*       → 页脚
  js_*           → JS 里的字符串（单独处理）
"""

import re
import json
import sys
import os

def auto_tag(html, tool_slug):
    """
    自动给 HTML 加 data-i18n 标记。
    返回 (marked_html, i18n_dict)
    """
    i18n = {}
    counter = {}

    def next_key(prefix):
        cnt = counter.get(prefix, 0) + 1
        counter[prefix] = cnt
        return f"{prefix}_{cnt}"

    # 1) <title> 内容加标记
    def tag_title(m):
        key = "title"
        text = m.group(1).strip()
        i18n[key] = text
        return f'<title data-i18n="{key}">{text}</title>'

    html = re.sub(r'<title>(.*?)</title>', tag_title, html, flags=re.DOTALL)

    # 2) meta description / og:title / og:description / twitter:* 的 content 属性
    def tag_meta_content(m):
        full = m.group(0)
        prop = m.group(1) or ''
        name = m.group(2) or ''
        content = m.group(3)
        key_prefix = None
        if 'og:title' in prop:
            key_prefix = 'og_title'
        elif 'og:description' in prop:
            key_prefix = 'og_description'
        elif 'description' == name:
            key_prefix = 'meta_description'
        elif 'twitter:title' in name:
            key_prefix = 'twitter_title'
        elif 'twitter:description' in name:
            key_prefix = 'twitter_description'
        if key_prefix:
            key = next_key(key_prefix)
            i18n[key] = content
            return full.replace(f'content="{content}"', f'data-i18n="{key}" content="{content}"')
        return full

    html = re.sub(
        r'<meta\s+(?:property="([^"]*)"\s+)?(?:name="([^"]*)"\s+)?content="([^"]*)"\s*/?\s*>',
        tag_meta_content, html
    )

    # 3) 可见元素：h1 h2 h3 h4 p li strong（直接 text）
    #    处理格式：<tag ...>TEXT</tag>
    def tag_visible_text(m):
        tag = m.group(1)
        attrs = m.group(2) or ''
        text = m.group(3).strip()
        if not text or len(text) < 2:
            return m.group(0)
        key = next_key(tag)
        i18n[key] = text
        return f'<{tag}{attrs} data-i18n="{key}">{text}</{tag}>'

    for tag in ['h1', 'h2', 'h3', 'h4']:
        html = re.sub(
            rf'<({tag})([^>]*)>(.*?)</{tag}>',
            tag_visible_text, html, flags=re.DOTALL
        )

    # 4) <button> 文本
    def tag_button(m):
        attrs = m.group(1) or ''
        text = m.group(2).strip()
        key = next_key('btn')
        i18n[key] = text
        return f'<button{attrs} data-i18n="{key}">{text}</button>'

    html = re.sub(r'<button([^>]*)>(.*?)</button>', tag_button, html, flags=re.DOTALL)

    # 5) <option> 文本
    def tag_option(m):
        attrs = m.group(1) or ''
        text = m.group(2).strip()
        key = next_key('option')
        i18n[key] = text
        return f'<option{attrs} data-i18n="{key}">{text}</option>'

    html = re.sub(r'<option([^>]*)>(.*?)</option>', tag_option, html, flags=re.DOTALL)

    # 6) label 文本
    def tag_label(m):
        attrs = m.group(1) or ''
        text = m.group(2).strip()
        key = next_key('label')
        i18n[key] = text
        return f'<label{attrs} data-i18n="{key}">{text}</label>'

    html = re.sub(r'<label([^>]*)>(.*?)</label>', tag_label, html, flags=re.DOTALL)

    # 7) p 标签（只处理短文本，避免误伤）
    def tag_p(m):
        attrs = m.group(1) or ''
        text = m.group(2).strip()
        # 跳过含 HTML 子标签的
        if '<' in text:
            return m.group(0)
        key = next_key('p')
        i18n[key] = text
        return f'<p{attrs} data-i18n="{key}">{text}</p>'

    html = re.sub(r'<p([^>]*)>(.*?)</p>', tag_p, html, flags=re.DOTALL)

    return html, i18n


def extract_js_strings(html):
    """
    从 <script> 中提取 JS 弹窗字符串：
      alert('...')  alert("...")
      confirm('...')  confirm("...")
    返回 { "js_N": "text" } 字典
    """
    js_strings = {}
    cnt = 0

    def repl_alert(m):
        nonlocal cnt
        text = m.group(1) or m.group(2)
        cnt += 1
        key = f"js_{cnt}"
        js_strings[key] = text
        # 把 alert('text') 替换成 alert(_t('key'))
        quote = m.group(1) and "'" or '"'
        return f"alert(_t('{key}'))"

    def repl_confirm(m):
        nonlocal cnt
        text = m.group(1) or m.group(2)
        cnt += 1
        key = f"js_{cnt}"
        js_strings[key] = text
        return f"confirm(_t('{key}'))"

    # 只处理非 ld+json 的 script
    script_re = re.compile(
        r'<script(?! type="application/ld\+json")([^>]*)>(.*?)</script>',
        re.DOTALL
    )

    def process_script(m):
        nonlocal cnt
        script_content = m.group(2)
        # alert
        script_content = re.sub(
            r'''alert\(\s*(['"])(.*?)\1\s*\)''',
            repl_alert, script_content
        )
        # confirm
        script_content = re.sub(
            r'''confirm\(\s*(['"])(.*?)\1\s*\)''',
            repl_confirm, script_content
        )
        return f'<script{m.group(1)}>{script_content}</script>'

    new_html = script_re.sub(process_script, html)
    return new_html, js_strings


def main():
    if len(sys.argv) < 2:
        print("用法: python auto_i18n_tag.py <tool_html_path>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"文件不存在: {path}")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    tool_slug = os.path.splitext(os.path.basename(path))[0]

    # 第一步：加 data-i18n 标记（HTML 部分）
    marked_html, i18n_dict = auto_tag(html, tool_slug)

    # 第二步：提取 JS 字符串（并替换 alert/confirm 为 _t() 调用）
    # 暂时跳过 JS 替换，先只生成 i18n JSON
    # marked_html, js_strings = extract_js_strings(marked_html)
    # i18n_dict.update(js_strings)

    # 写回标记好的 HTML
    out_path = path  # 直接覆盖（可改为 .bak）
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(marked_html)
    print(f"✓ 已加 data-i18n 标记: {out_path}")

    # 写 i18n JSON
    i18n_dir = os.path.join('i18n', 'en', 'tools')
    os.makedirs(i18n_dir, exist_ok=True)
    json_path = os.path.join(i18n_dir, f"{tool_slug}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(i18n_dict, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 i18n JSON: {json_path}")
    print(f"  共 {len(i18n_dict)} 条文案")


if __name__ == '__main__':
    main()
