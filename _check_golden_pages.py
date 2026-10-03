import urllib.request

base = 'https://golden.sendafun.com'
pages = ['/privacy', '/privacy-policy', '/about', '/contact', '/terms', '/terms-of-service', '/blog', '/faq']

for page in pages:
    url = base + page
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        content = resp.read().decode('utf-8')
        status = resp.status
        # 检查是否是 404 页面
        is_404 = '404' in content[:500] or 'not found' in content[:500].lower()
        print(f'{page}: {status}, len={len(content)}, 404={is_404}')
    except urllib.error.HTTPError as e:
        print(f'{page}: HTTP {e.code}')
    except Exception as e:
        print(f'{page}: Error {e}')
