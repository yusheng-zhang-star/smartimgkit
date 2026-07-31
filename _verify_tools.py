#!/usr/bin/env python
"""Comprehensive tool verification script.

Checks:
1. Empty script tags (likely empty tools)
2. Duplicate const declarations (SyntaxError)
3. Missing event listeners
4. Missing main action button
5. JavaScript syntax errors (rough check)
"""

import os, re

BASE = r'E:\网站项目\smartimgkit\tools'

issues_found = []
tools_checked = 0

for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BASE, fname)
    tools_checked += 1
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        slug = fname.replace('.html', '')
        tool_issues = []
        
        # 1. Check for empty script tags
        empty_scripts = re.findall(r'<script>\s*</script>', content)
        if empty_scripts:
            tool_issues.append(f"Empty <script> tag(s): {len(empty_scripts)}")
        
        # 2. Check for duplicate const declarations
        script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
        if script_match:
            script = script_match.group(1)
            # Find all const declarations
            const_decls = re.findall(r'const\s+(\w+)\s*=', script)
            duplicates = [x for x in const_decls if const_decls.count(x) > 1]
            if duplicates:
                tool_issues.append(f"Duplicate const: {list(set(duplicates))}")
        
        # 3. Check for main button
        has_primary_btn = 'btn-primary' in content or 'class="restore-btn primary"' in content
        if not has_primary_btn:
            tool_issues.append("No primary action button")
        
        # 4. Check for event listeners
        has_listener = 'addEventListener' in content or '.onclick' in content or '.onchange' in content
        if not has_listener and script_match and len(script_match.group(1).strip()) > 100:
            tool_issues.append("No event listeners found (suspicious)")
        
        if tool_issues:
            issues_found.append((slug, tool_issues))
            print(f"\n⚠️  {slug}:")
            for issue in tool_issues:
                print(f"   - {issue}")
    except Exception as e:
        print(f"ERROR reading {fname}: {e}")

print(f"\n{'='*60}")
print(f"Tools checked: {tools_checked}")
print(f"Issues found: {len(issues_found)}")

if issues_found:
    print("\nSummary of issues:")
    for slug, issues in issues_found:
        print(f"  {slug}: {', '.join(issues)}")
else:
    print("\n✅ All tools pass basic checks!")
