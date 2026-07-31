#!/usr/bin/env python
"""Sync new tools (gif-splitter, beauty-editor) to all language versions."""

import os
import shutil

BASE = r'E:\网站项目\smartimgkit'
LANGS = ['es', 'pt', 'id', 'fr', 'vi', 'ar']
NEW_TOOLS = ['gif-splitter', 'beauty-editor']

def sync_tool(tool_slug):
    """Sync a tool from English to all other languages."""
    src = os.path.join(BASE, 'tools', tool_slug + '.html')
    if not os.path.exists(src):
        print(f"❌ Source not found: {src}")
        return False
    
    count = 0
    for lang in LANGS:
        dst_dir = os.path.join(BASE, lang, 'tools')
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, tool_slug + '.html')
        shutil.copy2(src, dst)
        count += 1
        print(f"✅ Copied to {lang}/tools/{tool_slug}.html")
    
    return count

def main():
    total = 0
    for tool in NEW_TOOLS:
        print(f"\nSyncing {tool}...")
        c = sync_tool(tool)
        total += c
    
    print(f"\n✅ Total files synced: {total}")

if __name__ == '__main__':
    main()
