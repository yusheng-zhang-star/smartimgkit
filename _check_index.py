import urllib.request, re

req = urllib.request.Request('https://smartimgkit.com/blog/', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
content = resp.read().decode('utf-8')

if 'ai-object-remover-lama-inpainting' in content:
    print('Blog index already contains the new post')
else:
    print('Blog index does NOT contain the new post - needs update')

links = re.findall(r'href="/blog/([^"]+)"', content)
unique = sorted(set(l for l in links if not l.endswith('/')))
print(f'Total posts in index: {len(unique)}')
for u in unique:
    print(f'  {u}')
