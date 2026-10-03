import urllib.request, re, os

# 获取线上博客列表
req = urllib.request.Request('https://smartimgkit.com/blog/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
content = resp.read().decode('utf-8')
links = re.findall(r'href="/blog/([^"]+)"', content)
live_blogs = set(l for l in links if not l.endswith('/'))
print(f'Live blogs: {len(live_blogs)}')

# 检查本地博客
local_blogs = [f for f in os.listdir(r'E:\网站项目\smartimgkit\blog') if f.endswith('.html') and f != 'index.html']
print(f'\nLocal blogs: {len(local_blogs)}')

not_live = []
for blog in local_blogs:
    if blog not in live_blogs:
        not_live.append(blog)
        size = os.path.getsize(os.path.join(r'E:\网站项目\smartimgkit\blog', blog))
        print(f'  NOT LIVE: {blog} ({size} bytes)')

print(f'\nBlogs not yet live: {len(not_live)}')
