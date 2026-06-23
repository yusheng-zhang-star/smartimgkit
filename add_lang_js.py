#!/usr/bin/env python3
"""
为所有工具页面添加 js/lang.js 引用
"""

import os
import re

def add_lang_js_to_file(filepath, script_path):
    """为单个HTML文件添加js/lang.js引用"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有js/lang.js引用
    if 'js/lang.js' in content:
        print(f"Skip (already has lang.js): {filepath}")
        return
    
    # 在</body>前添加script引用
    script_tag = f'  <script src="{script_path}"></script>\n</body>'
    new_content = content.replace('</body>', script_tag)
    
    if new_content == content:
        print(f"ERROR: Could not find </body> in {filepath}")
        return
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added lang.js: {filepath}")

def process_directory(tools_dir, script_path):
    """处理目录中的所有HTML文件"""
    for filename in os.listdir(tools_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(tools_dir, filename)
            add_lang_js_to_file(filepath, script_path)

def main():
    base_dir = 'E:\\网站项目\\smartimgkit'
    
    # 处理 English tool pages
    print("Processing English tool pages...")
    process_directory(os.path.join(base_dir, 'tools'), '../js/lang.js')
    
    # 处理 Spanish tool pages
    print("\nProcessing Spanish tool pages...")
    process_directory(os.path.join(base_dir, 'es', 'tools'), '../../js/lang.js')
    
    # 处理 Portuguese tool pages
    print("\nProcessing Portuguese tool pages...")
    process_directory(os.path.join(base_dir, 'pt', 'tools'), '../../js/lang.js')
    
    # 处理 Indonesian tool pages
    print("\nProcessing Indonesian tool pages...")
    process_directory(os.path.join(base_dir, 'id', 'tools'), '../../js/lang.js')
    
    print("\nDone!")

if __name__ == '__main__':
    main()
