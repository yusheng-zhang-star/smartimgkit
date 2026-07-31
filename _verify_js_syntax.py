#!/usr/bin/env python
"""Verify JavaScript syntax for ALL tool pages using Node."""

import os
import subprocess
import json

BASE = r'E:\网站项目\smartimgkit'

EXCLUDE_DIRS = ('node_modules', 'i18n', 'src', '_backup', '_old', 'dist')

def get_tool_html_files():
    html_files = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and 
                   not any(d.startswith(x) for x in EXCLUDE_DIRS)]
        for f in files:
            if f.endswith('.html') and ('/tools/' in root.replace('\\', '/') or root.endswith('tools')):
                full_path = os.path.join(root, f)
                try:
                    rel = os.path.relpath(full_path, BASE).replace('\\', '/')
                    html_files.append(rel)
                except ValueError:
                    pass
    return html_files


def main():
    html_files = get_tool_html_files()
    print(f"Checking {len(html_files)} tool HTML files...")
    
    errors = []
    ok = 0
    
    for rel in html_files:
        full = os.path.join(BASE, rel)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Extract inline scripts
        scripts = []
        import re
        for m in re.finditer(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', content):
            code = m.group(1).strip()
            if len(code) > 100:
                scripts.append(code)
        
        file_ok = True
        for code in scripts:
            # Use node to check syntax
            try:
                result = subprocess.run(
                    ['node', '-e', f'try {{ new Function({json.dumps(code)}); console.log("OK"); }} catch(e) {{ console.log("ERR:" + e.message); }}'],
                    capture_output=True, text=True, timeout=15
                )
                if result.stdout.strip().startswith('ERR:'):
                    errors.append({'file': rel, 'error': result.stdout.strip()[4:]})
                    file_ok = False
                    break
            except Exception as e:
                pass
        
        if file_ok:
            ok += 1
    
    print(f"\n✅ Syntax OK: {ok}/{len(html_files)}")
    print(f"❌ Syntax errors: {len(errors)}")
    
    if errors:
        print("\n=== ERRORS ===")
        for e in errors[:30]:
            print(f"  ❌ {e['file']}")
            print(f"     {e['error'][:150]}")


if __name__ == '__main__':
    main()
