# -*- coding: utf-8 -*-
import io, re
# 检查英文版博客列表页的链接格式
h = io.open(r'e:\网站项目\smartimgkit\blog\index.html', encoding='utf-8').read()
links = re.findall(r'href="(/blog/[^"]+)"', h)
print('英文版博客列表页链接格式:')
for l in links[:5]:
    print(f'  {l}')
print(f'  总共 {len(links)} 个链接')
# 检查是否有 .html 后缀
has_html = any(l.endswith('.html') for l in links)
print(f'  有.html后缀: {has_html}')

# 检查英文版工具页面的链接格式
h2 = io.open(r'e:\网站项目\smartimgkit\index.html', encoding='utf-8').read()
tool_links = re.findall(r'href="(/tools/[^"]+)"', h2)
print('\n英文版首页工具链接格式:')
for l in tool_links[:3]:
    print(f'  {l}')
has_html2 = any(l.endswith('.html') for l in tool_links)
print(f'  有.html后缀: {has_html2}')
