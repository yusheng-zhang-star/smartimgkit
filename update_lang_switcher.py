#!/usr/bin/env python3
"""
更新所有工具页面，添加语言切换支持
1. 更新语言下拉列表HTML结构
2. 添加js/lang.js引用
"""

import os
import re

def update_tool_page(filepath):
    """更新单个工具页面"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 更新语言下拉列表HTML
    # 查找旧的lang-switcher结构
    old_pattern = r'<div class="lang-switcher" style="position:relative;">.*?<button class="lang-btn" aria-label="Switch language">.*?</button>.*?<div class="lang-dropdown".*?>.*?</div>.*?</div>'
    
    # 新的lang-switcher结构
    new_lang_switcher = '''        <div class="lang-switcher" id="langSwitcher">
          <button class="lang-btn" onclick="toggleLangDropdown()" aria-label="Select language">
            <span class="lang-flag">🇬🇧</span>
            <span class="lang-name">EN</span>
            <span class="lang-arrow">▾</span>
          </button>
          <div class="lang-dropdown">
            <a href="/" onclick="localStorage.setItem('lang_chosen','en')"><span>🇬🇧</span> English</a>
            <a href="/es/" onclick="localStorage.setItem('lang_chosen','es')"><span>🇪🇸</span> Español</a>
            <a href="/pt/" onclick="localStorage.setItem('lang_chosen','pt')"><span>🇧🇷</span> Português</a>
            <a href="/id/" onclick="localStorage.setItem('lang_chosen','id')"><span>🇮🇩</span> Bahasa Indonesia</a>
          </div>
        </div>'''
    
    # 使用正则表达式替换（简单的替换，可能需要根据实际情况调整）
    # 这里我们先不做HTML结构替换，因为正则表达式可能不可靠
    # 而是直接添加js/lang.js引用，让JavaScript来处理UI更新
    
    # 2. 添加js/lang.js引用
    if '../js/lang.js' not in content and 'js/lang.js' not in content:
        content = content.replace('</body>', '  <script src="../js/lang.js"></script>\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {filepath}")

def main():
    tools_dir = '/e/网站项目/smartimgkit/tools'
    
    # 更新 English tool pages
    for filename in os.listdir(tools_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(tools_dir, filename)
            update_tool_page(filepath)
    
    print("Done!")

if __name__ == '__main__':
    main()
