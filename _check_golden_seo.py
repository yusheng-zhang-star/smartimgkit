import urllib.request
import re

base = 'https://golden.sendafun.com'

# 1. 检查 sitemap 和 robots
print('=== 1. SEO 基础 ===')
for path in ['/sitemap.xml', '/robots.txt']:
    try:
        req = urllib.request.Request(base + path, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        content = resp.read().decode('utf-8')
        print(f'{path}: {resp.status}, {len(content)} chars')
        if path == '/robots.txt':
            print(f'  Content: {content[:200]}')
        if path == '/sitemap.xml':
            urls = re.findall(r'<loc>(.*?)</loc>', content)
            print(f'  URLs in sitemap: {len(urls)}')
            for u in urls[:10]:
                print(f'    {u}')
    except Exception as e:
        print(f'{path}: {e}')

# 2. 检查首页 meta
print('\n=== 2. 首页 Meta ===')
req = urllib.request.Request(base + '/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

metas = re.findall(r'<meta[^>]+>', html)
for m in metas:
    print(f'  {m}')

# 3. 检查是否有结构化数据
print('\n=== 3. 结构化数据 ===')
if 'application/ld+json' in html:
    print('  Found JSON-LD structured data')
else:
    print('  NO structured data found')

# 4. 检查 OG 标签
print('\n=== 4. OG 标签 ===')
og_tags = re.findall(r'<meta property="og:[^"]+" content="[^"]*"', html)
for og in og_tags:
    print(f'  {og}')
if not og_tags:
    print('  NO OG tags found')
