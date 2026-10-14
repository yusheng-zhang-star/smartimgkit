import os, re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'nav', 'footer', 'header']:
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'footer', 'header']:
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data.strip())

def get_text_word_count(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parser = TextExtractor()
        parser.feed(content)
        full_text = ' '.join([t for t in parser.text if t])
        words = len(full_text.split())
        return words
    except Exception as e:
        return 0

# 扫描所有tools和blog下的html文件
thin_pages = []
all_html = []
for root, dirs, files in os.walk('.'):
    # 跳过多语言目录，只处理英文根目录下的页面
    if any(x in root for x in ['/ar/', '/es/', '/fr/', '/pt/', '/zh/', '/id/', '/vi/', '.wrangler', 'node_modules']):
        continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            all_html.append(path)
            wc = get_text_word_count(path)
            if wc < 300:
                rel_path = path.replace('./', '/').replace('\\', '/')
                thin_pages.append((rel_path, wc))

print(f"总英文HTML页面: {len(all_html)}")
print(f"正文<300词的薄页面: {len(thin_pages)}个")
print("\n薄页面列表:")
for p, wc in sorted(thin_pages, key=lambda x:x[1]):
    print(f"  {p}: {wc}词")

# 保存结果
with open("_thin_pages_list.txt", "w", encoding="utf-8") as f:
    for p, wc in thin_pages:
        f.write(f"{p}\t{wc}\n")
print("\n✅ 薄页面清单已保存到_thin_pages_list.txt")
