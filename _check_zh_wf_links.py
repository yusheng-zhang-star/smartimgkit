# -*- coding: utf-8 -*-
"""检查 zh/workflows 所有 HTML 文件的内链和死链"""
import io, os, re

WF_DIR = r'e:\网站项目\smartimgkit\zh\workflows'
SITE_ROOT = r'e:\网站项目\smartimgkit'

def resolve_url(href):
    if href.startswith('#') or href.startswith('http://') or href.startswith('https://'):
        return None
    if href.startswith('mailto:') or href.startswith('javascript:'):
        return None
    path = href.split('?')[0].split('#')[0]
    if not path:
        return None
    if path.startswith('/zh/'):
        local = path[4:]
        if local == '':
            return os.path.join(SITE_ROOT, 'zh', 'index.html')
        candidate = os.path.join(SITE_ROOT, 'zh', local.lstrip('/'))
        if os.path.isdir(candidate):
            return os.path.join(candidate, 'index.html')
        if os.path.exists(candidate):
            return candidate
        if os.path.exists(candidate + '.html'):
            return candidate + '.html'
        return candidate
    elif path.startswith('/'):
        local = path[1:]
        candidate = os.path.join(SITE_ROOT, local.lstrip('/'))
        if os.path.isdir(candidate):
            return os.path.join(candidate, 'index.html')
        if os.path.exists(candidate):
            return candidate
        if os.path.exists(candidate + '.html'):
            return candidate + '.html'
        return candidate
    return None

issues = []
files = sorted(f for f in os.listdir(WF_DIR) if f.endswith('.html') and not f.startswith('_'))

for fname in files:
    fpath = os.path.join(WF_DIR, fname)
    html = io.open(fpath, encoding='utf-8').read()

    # 检查指向英文工具/工作流页面的内链
    for m in re.finditer(r'href=["\'](/tools/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文工具页: {m.group(1)}')
    for m in re.finditer(r'href=["\'](/workflows/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文工作流页: {m.group(1)}')
    for m in re.finditer(r'href=["\'](/blog/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文博客页: {m.group(1)}')

    # 死链
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        local = resolve_url(href)
        if local is not None and not os.path.exists(local):
            issues.append(f'[{fname}] 死链: {href}')

    # lang 属性
    if 'lang="en"' in html[:200]:
        issues.append(f'[{fname}] lang="en" 应为 lang="zh"')

    # 重复 hreflang 指向中文路径
    for m in re.finditer(r'<link[^>]*hreflang=["\']en["\'][^>]*href=["\']([^"\']+)["\']', html):
        if '/zh/' in m.group(1):
            issues.append(f'[{fname}] hreflang="en" 错误指向中文路径: {m.group(1)}')

print('=' * 60)
if issues:
    print(f'发现 {len(issues)} 个问题:')
    for iss in issues:
        print('  -', iss)
else:
    print('未发现问题')
print('=' * 60)
