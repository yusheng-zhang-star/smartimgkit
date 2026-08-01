import urllib.request, os
url = 'https://cdn.jsdelivr.net/npm/@flyskywhy/gifuct-js@3.0.0/lib/index.min.js'
fpath = r'E:\网站项目\smartimgkit\js\gifuct-js.min.js'
urllib.request.urlretrieve(url, fpath)
size = os.path.getsize(fpath)
print(f'Downloaded: {size} bytes')
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read(300)
    print(content[:300])
