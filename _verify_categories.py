import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到tools-grid
gs = content.find('<div class="tools-grid">')

# 提取所有分类标题和工具卡片
text = content[gs:]

# 找分类标题
cat_pattern = r'<h3 style="font-size:1.3rem[^>]*>([^<]+)</h3>'
cats = re.findall(cat_pattern, text)

print("=== 分类顺序 ===")
for i, cat in enumerate(cats):
    print(f"{i+1}. {cat}")

# 统计每个分类下的工具数
card_pattern = r'<a href="(?:/[^/]+)?/tools/([^"]+)" class="tool-card">'
all_slugs = re.findall(card_pattern, text)
print(f"\n=== 总工具数: {len(all_slugs)} ===")

# 按分类计数（通过标题位置和下一个标题位置之间的卡片数）
cat_positions = []
for m in re.finditer(cat_pattern, text):
    cat_positions.append((m.group(1), m.start()))

for i, (cat_name, start) in enumerate(cat_positions):
    end = cat_positions[i+1][1] if i < len(cat_positions)-1 else len(text)
    section = text[start:end]
    slugs = re.findall(card_pattern, section)
    print(f"  {cat_name}: {len(slugs)} 个工具")
