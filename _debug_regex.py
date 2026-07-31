import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

gs = content.find('<div class="tools-grid">')
print(f'grid start: {gs}')

m = re.search(r'<a href="/tools/compressor" class="tool-card">', content[gs:gs+500])
print(f'found compressor: {m is not None}')

pattern = r'<a href="/tools/([^"]+)" class="tool-card">.*?</a>'
matches = re.findall(pattern, content[gs:gs+2000], re.DOTALL)
print(f'matches found: {len(matches)}')
print(f'first 5: {matches[:5]}')
