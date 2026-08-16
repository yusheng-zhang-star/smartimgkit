# -*- coding: utf-8 -*-
"""检查 zh/blog 所有 HTML 文件的内链、死链、重复 hreflang、语法问题"""
import io, os, re

BLOG_DIR = r'e:\网站项目\smartimgkit\zh\blog'
SITE_ROOT = r'e:\网站项目\smartimgkit'

def resolve_url(href):
    """将 URL 路径映射到本地文件路径，返回 None 表示外部链接/锚点"""
    if href.startswith('#') or href.startswith('http://') or href.startswith('https://'):
        return None
    if href.startswith('mailto:') or href.startswith('javascript:'):
        return None
    # 去除查询参数和锚点
    path = href.split('?')[0].split('#')[0]
    if not path:
        return None
    # 映射到本地
    if path.startswith('/zh/'):
        local = path[4:]  # 去掉 /zh/
        if local == '':
            return os.path.join(SITE_ROOT, 'zh', 'index.html')
        # 尝试 .html
        candidate = os.path.join(SITE_ROOT, 'zh', local.lstrip('/'))
        if os.path.isdir(candidate):
            return os.path.join(candidate, 'index.html')
        if os.path.exists(candidate):
            return candidate
        if os.path.exists(candidate + '.html'):
            return candidate + '.html'
        return candidate  # 返回用于报错
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
files = sorted(f for f in os.listdir(BLOG_DIR) if f.endswith('.html') and not f.startswith('_'))

for fname in files:
    fpath = os.path.join(BLOG_DIR, fname)
    html = io.open(fpath, encoding='utf-8').read()

    # 1. 检查重复 hreflang 标签
    hreflangs = re.findall(r'<link[^>]*hreflang=[\'"]([^\'"]+)[\'"][^>]*>', html)
    seen = {}
    for hl in hreflangs:
        seen[hl] = seen.get(hl, 0) + 1
    for hl, cnt in seen.items():
        if cnt > 1:
            issues.append(f'[{fname}] 重复 hreflang="{hl}" ({cnt}次)')

    # 2. 检查错误的 hreflang 指向（en 应指向 /blog/ 而非 /zh/blog/）
    for m in re.finditer(r'<link[^>]*hreflang=["\']en["\'][^>]*href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        if '/zh/blog/' in href:
            issues.append(f'[{fname}] hreflang="en" 错误指向中文路径: {href}')
    for m in re.finditer(r'<link[^>]*hreflang=["\']x-default["\'][^>]*href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        if '/zh/blog/' in href:
            issues.append(f'[{fname}] hreflang="x-default" 错误指向中文路径: {href}')

    # 3. 检查指向英文工具/工作流页面的内链（应指向 /zh/）
    for m in re.finditer(r'href=["\'](/tools/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文工具页(应加/zh前缀): {m.group(1)}')
    for m in re.finditer(r'href=["\'](/workflows/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文工作流页(应加/zh前缀): {m.group(1)}')
    for m in re.finditer(r'href=["\'](/blog/[^"\']+)["\']', html):
        issues.append(f'[{fname}] 内链指向英文博客页(应加/zh前缀): {m.group(1)}')

    # 4. 检查死链（内部链接目标是否存在）
    for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
        href = m.group(1)
        local = resolve_url(href)
        if local is not None and not os.path.exists(local):
            issues.append(f'[{fname}] 死链: {href} -> {local}')

    # 5. 检查 lang 属性
    if 'lang="en"' in html[:200]:
        issues.append(f'[{fname}] <html> lang="en" 应为 lang="zh"')

print('=' * 60)
if issues:
    print(f'发现 {len(issues)} 个问题:')
    for iss in issues:
        print('  -', iss)
else:
    print('未发现问题')
print('=' * 60)
