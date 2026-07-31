import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

grid_start = content.find('<div class="tools-grid">')
print(f'grid_start: {grid_start}')

text_dev_marker = 'Text &amp; Developer Tools'
text_dev_idx = content.find(text_dev_marker, grid_start)
print(f'text_dev_idx: {text_dev_idx}')

# 看看 text_dev_idx 前后的内容
if text_dev_idx > 0:
    print(f'context before: ...{content[text_dev_idx-100:text_dev_idx]}...')
    print(f'context after: ...{content[text_dev_idx:text_dev_idx+100]}...')

# 看看我们能不能在 grid 范围内找到卡片
pattern = r'<a href="/tools/([^"]+)" class="tool-card">.*?</a>'
if text_dev_idx > 0:
    grid_section = content[grid_start:text_dev_idx]
else:
    grid_section = content[grid_start:]

print(f'grid_section length: {len(grid_section)}')

matches = re.findall(pattern, grid_section, re.DOTALL)
print(f'all matches: {len(matches)}')
print(f'slugs: {matches}')
