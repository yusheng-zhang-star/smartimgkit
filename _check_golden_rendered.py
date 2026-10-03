from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://golden.sendafun.com/', wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(3000)
    
    content = page.content()
    print(f'Rendered HTML length: {len(content)}')
    
    # 获取可见文本
    text = page.inner_text('body')
    print(f'Visible text length: {len(text)}')
    print(f'First 500 chars of text:')
    print(text[:500])
    
    # 统计链接
    links = page.eval_on_selector_all('a', 'els => els.map(e => e.href)')
    internal = [l for l in links if 'golden.sendafun.com' in l]
    print(f'\nTotal links: {len(links)}')
    print(f'Internal links: {len(internal)}')
    for l in internal[:20]:
        print(f'  {l}')
    
    # 检查是否有隐私政策等链接
    for keyword in ['privacy', 'about', 'contact', 'terms', 'blog']:
        found = [l for l in links if keyword in l.lower()]
        if found:
            print(f'\n{keyword} links: {found[:3]}')
    
    browser.close()
