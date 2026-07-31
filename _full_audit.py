#!/usr/bin/env python
"""Comprehensive code audit for smartimgkit - find all potential issues."""

import os
import re
from collections import defaultdict

BASE = r'E:\网站项目\smartimgkit'

EXCLUDE_DIRS = ('node_modules', 'i18n', 'src', '_backup', '_old', 'dist')
EXCLUDE_FILES = ('_tool_template.html', 'test.html', '404.html')

LANG_DIRS = ['', 'es', 'pt', 'id', 'fr', 'vi', 'ar']


def get_all_html_files():
    html_files = set()
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and 
                   not any(d.startswith(x) for x in EXCLUDE_DIRS)]
        for f in files:
            if f.endswith('.html') and f not in EXCLUDE_FILES:
                full_path = os.path.join(root, f)
                try:
                    rel = os.path.relpath(full_path, BASE).replace('\\', '/')
                    html_files.add(rel)
                except ValueError:
                    pass
    return html_files


def check_duplicate_const(html_files):
    """Check for duplicate const declarations in the same scope."""
    print("="*70)
    print("CHECK 1: Duplicate const/let/var declarations")
    print("="*70)
    
    issues = []
    for html_file in sorted(html_files):
        filepath = os.path.join(BASE, html_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Extract all script blocks
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        
        for script in scripts:
            # Find all const/let/var declarations (top-level only)
            declarations = re.findall(r'(?:^|\n)\s*(const|let|var)\s+(\w+)', script)
            
            seen = defaultdict(list)
            for idx, (decl_type, name) in enumerate(declarations):
                seen[name].append((decl_type, idx))
            
            for name, occurrences in seen.items():
                if len(occurrences) > 1:
                    # Only flag if same declaration type and not in different blocks
                    types = [t for t, _ in occurrences]
                    if types.count('const') > 1:
                        issues.append((html_file, name, len(occurrences)))
    
    if issues:
        print(f"❌ Found {len(issues)} files with duplicate const declarations:")
        for f, name, count in sorted(issues)[:20]:
            print(f"   {f}: '{name}' declared {count} times")
        if len(issues) > 20:
            print(f"   ... and {len(issues)-20} more")
    else:
        print("✅ No duplicate const declarations found")
    
    return issues


def check_double_click(html_files):
    """Check for duplicate click handlers on file inputs (double click bug)."""
    print("\n" + "="*70)
    print("CHECK 2: Double click / duplicate event handlers")
    print("="*70)
    
    issues = []
    for html_file in sorted(html_files):
        filepath = os.path.join(BASE, html_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Check for pattern: both <label for="fileInput"> AND dropzone.addEventListener('click', ...fileInput.click())
        has_label_for = bool(re.search(r'<label[^>]*for=["\']fileInput["\']', content))
        has_click_listener = bool(re.search(r'(?:dropzone|uploadArea)\.addEventListener\s*\(\s*["\']click["\'][^)]*fileInput\.click\(\)', content))
        
        # Also check for multiple addEventListener('click' on the same element
        click_listeners = re.findall(r'(\w+)\.addEventListener\s*\(\s*["\']click["\']', content)
        from collections import Counter
        listener_counts = Counter(click_listeners)
        multi_click = {k: v for k, v in listener_counts.items() if v > 1}
        
        if (has_label_for and has_click_listener) or multi_click:
            issues.append((html_file, has_label_for, has_click_listener, multi_click))
    
    if issues:
        print(f"❌ Found {len(issues)} files with potential double-click issues:")
        for f, has_label, has_listener, multi in sorted(issues):
            reasons = []
            if has_label and has_listener:
                reasons.append("label+click listener conflict")
            if multi:
                reasons.append(f"multiple click listeners on: {list(multi.keys())}")
            print(f"   {f}: {', '.join(reasons)}")
    else:
        print("✅ No double-click issues found")
    
    return issues


def check_empty_scripts(html_files):
    """Check for empty script tags in tool pages."""
    print("\n" + "="*70)
    print("CHECK 3: Empty scripts (shell tools)")
    print("="*70)
    
    issues = []
    for html_file in sorted(html_files):
        if '/tools/' not in html_file:
            continue
            
        filepath = os.path.join(BASE, html_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Extract all script blocks (not external src)
        inline_scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', content, re.DOTALL)
        
        has_substantive_code = False
        for script in inline_scripts:
            # Strip comments and whitespace
            clean = re.sub(r'//.*?$', '', script, flags=re.MULTILINE)
            clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
            clean = clean.strip()
            
            # Check if it has real code (function calls, event listeners, etc.)
            if len(clean) > 100 and ('addEventListener' in clean or 'function' in clean or 
                                          'getElementById' in clean or 'querySelector' in clean):
                has_substantive_code = True
                break
        
        if not has_substantive_code:
            issues.append(html_file)
    
    if issues:
        print(f"❌ Found {len(issues)} tool files with empty/minimal scripts:")
        for f in sorted(issues):
            print(f"   {f}")
    else:
        print("✅ All tool files have substantive code")
    
    return issues


def check_cdn_resources(html_files):
    """Check CDN resource references."""
    print("\n" + "="*70)
    print("CHECK 4: CDN resource references")
    print("="*70)
    
    all_cdn_urls = set()
    cdn_by_file = defaultdict(set)
    
    for html_file in sorted(html_files):
        filepath = os.path.join(BASE, html_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Find all CDN src/href
        urls = re.findall(r'(?:src|href)\s*=\s*["\']((?:https?:)?//[^"\']+)["\']', content)
        for url in urls:
            all_cdn_urls.add(url)
            cdn_by_file[html_file].add(url)
    
    # Group by domain
    by_domain = defaultdict(set)
    for url in all_cdn_urls:
        m = re.match(r'(?:https?:)?//([^/]+)', url)
        if m:
            by_domain[m.group(1)].add(url)
    
    print(f"📊 Found {len(all_cdn_urls)} unique CDN URLs across {len(cdn_by_file)} files")
    print(f"   Domains: {', '.join(sorted(by_domain.keys()))}")
    
    # Check for potentially risky CDNs (not commonly used)
    trusted_domains = {'cdn.jsdelivr.net', 'cdnjs.cloudflare.com', 'fonts.googleapis.com',
                       'fonts.gstatic.com', 'unpkg.com', 'cdn.jsdelivr.net', 
                       'stackpath.bootstrapcdn.com'}
    unusual = [d for d in by_domain if d not in trusted_domains]
    if unusual:
        print(f"⚠️  Unusual CDN domains: {', '.join(unusual)}")
    else:
        print("✅ All CDN domains are trusted")
    
    return all_cdn_urls, cdn_by_file


def check_robots_sitemap_consistency():
    """Check robots.txt vs sitemap consistency."""
    print("\n" + "="*70)
    print("CHECK 5: robots.txt vs sitemap consistency")
    print("="*70)
    
    robots_path = os.path.join(BASE, 'robots.txt')
    if not os.path.exists(robots_path):
        print("⚠️  No robots.txt found")
        return None
    
    with open(robots_path, 'r', encoding='utf-8') as f:
        robots = f.read()
    
    print("📄 robots.txt contents:")
    print(robots[:500])
    
    # Check if sitemap is referenced
    if 'Sitemap:' not in robots:
        print("⚠️  robots.txt does not reference sitemap.xml")
    else:
        m = re.search(r'Sitemap:\s*(\S+)', robots)
        if m:
            print(f"✅ References sitemap: {m.group(1)}")
    
    return robots


def check_local_resource_refs(html_files):
    """Check local JS/CSS file references."""
    print("\n" + "="*70)
    print("CHECK 6: Local resource references (JS/CSS)")
    print("="*70)
    
    all_files = set()
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and 
                   not any(d.startswith(x) for x in EXCLUDE_DIRS)]
        for f in files:
            full_path = os.path.join(root, f)
            try:
                rel = os.path.relpath(full_path, BASE).replace('\\', '/')
                all_files.add(rel)
            except ValueError:
                pass
    
    missing = defaultdict(list)
    
    for html_file in sorted(html_files):
        filepath = os.path.join(BASE, html_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Find local src/href (not starting with http)
        refs = re.findall(r'(?:src|href)\s*=\s*["\'](/[^"\']+)["\']', content)
        for ref in refs:
            # Strip query string
            clean_ref = ref.split('?')[0].split('#')[0]
            if clean_ref.startswith('/'):
                clean_ref = clean_ref[1:]
            
            if clean_ref and clean_ref not in all_files:
                # Try with .html
                if clean_ref + '.html' not in all_files:
                    if clean_ref + '/index.html' not in all_files:
                        missing[html_file].append(ref)
    
    if missing:
        print(f"❌ Found {len(missing)} files referencing missing local resources:")
        for f, refs in sorted(missing.items())[:10]:
            print(f"   {f}:")
            for r in refs[:3]:
                print(f"      - {r}")
            if len(refs) > 3:
                print(f"      ... and {len(refs)-3} more")
        if len(missing) > 10:
            print(f"   ... and {len(missing)-10} more files")
    else:
        print("✅ All local resource references are valid")
    
    return missing


def main():
    html_files = get_all_html_files()
    print(f"📊 Auditing {len(html_files)} HTML files\n")
    
    issues1 = check_duplicate_const(html_files)
    issues2 = check_double_click(html_files)
    issues3 = check_empty_scripts(html_files)
    issues4_cdn, _ = check_cdn_resources(html_files)
    issues5 = check_robots_sitemap_consistency()
    issues6 = check_local_resource_refs(html_files)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Files with duplicate const: {len(issues1)}")
    print(f"Files with double-click issues: {len(issues2)}")
    print(f"Files with empty scripts: {len(issues3)}")
    print(f"CDN URLs: {len(issues4_cdn)}")
    print(f"Missing local refs: {len(issues6) if issues6 else 0}")
    
    total_issues = len(issues1) + len(issues2) + len(issues3)
    print(f"\n🔴 Total issues to fix: {total_issues}")


if __name__ == '__main__':
    main()
