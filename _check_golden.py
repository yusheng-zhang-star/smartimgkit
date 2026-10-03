import urllib.request
import re

url = 'https://golden.sendafun.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode('utf-8')
    print('Status: OK')
    print(f'Content length: {len(content)} chars')
    m = re.search(r'<title>(.*?)</title>', content)
    if m: print(f'Title: {m.group(1)}')
    for keyword in ['privacy', 'about', 'contact', 'terms', 'blog', '隐私', '关于', '联系']:
        if keyword in content.lower():
            print(f'Found keyword: {keyword}')
    links = re.findall(r'href="([^"]+)"', content)
    print(f'Total links: {len(links)}')
    internal = [l for l in links if l.startswith('/') and not l.startswith('//')]
    print(f'Internal links: {len(internal)}')
    for l in internal[:30]:
        print(f'  {l}')
except Exception as e:
    print(f'Error: {e}')
