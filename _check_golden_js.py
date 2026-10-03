import urllib.request
import re

# 获取首页 HTML
req = urllib.request.Request('https://golden.sendafun.com/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# 找到 JS bundle
js_files = re.findall(r'src="(/assets/[^"]+\.js)"', html)
print(f'JS files: {js_files}')

# 下载主 JS bundle 并查找路由
for js in js_files:
    url = 'https://golden.sendafun.com' + js
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15)
    js_content = resp.read().decode('utf-8')
    print(f'\n{js}: {len(js_content)} chars')
    
    # 查找路由路径
    routes = re.findall(r'["\'](/[a-z0-9\-/]+)["\']', js_content)
    unique_routes = sorted(set(r for r in routes if len(r) > 3 and not r.startswith('/assets') and not r.startswith('/favicon')))
    print(f'Potential routes ({len(unique_routes)}):')
    for r in unique_routes[:30]:
        print(f'  {r}')
    
    # 查找页面标题或内容关键词
    for keyword in ['privacy', 'about', 'contact', 'terms', 'blog', 'Golden Hour', 'photography']:
        if keyword.lower() in js_content.lower():
            print(f'  Found keyword: {keyword}')
