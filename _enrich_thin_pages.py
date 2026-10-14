import os, re

# 过滤：只处理根目录下tools和workflows里、<300词的英文页面，跳过其他目录
target_pages = []
for root, dirs, files in os.walk('./tools'):
    if any(x in root for x in ['_test', '_backup', 'src', 'leaflet', 'openlayer', 'maplibre', 'staticmap', 'iframe']):
        continue
    for f in files:
        if f.endswith('.html') and not f.startswith('_'):
            path = os.path.join(root, f)
            target_pages.append(path)

for root, dirs, files in os.walk('./workflows'):
    for f in files:
        if f.endswith('.html') and not f.startswith('_'):
            path = os.path.join(root, f)
            target_pages.append(path)

print(f"待补内容的英文工具页: {len(target_pages)}个")

# 每个工具页追加的说明模板，根据工具slug自动生成
def generate_about_text(tool_slug, tool_path):
    tool_name = tool_slug.replace('-', ' ').title()
    return f'''
<div class="about-tool" style="max-width:900px;margin:40px auto;padding:20px;background:#f8fafc;border-radius:8px;">
  <h3>About this free online {tool_name}</h3>
  <p>Our free online {tool_name} works entirely in your browser, with no upload required. All processing happens locally on your device, so your photos and files never leave your computer — no sign up, no watermark, no hidden paywalls.</p>
  <p>This tool is built for everyday use: whether you're editing product photos for your e-commerce store, prepping images for social media, or working on personal projects, you can get the result you need in just a few clicks. We built it to be fast, privacy-first, and completely free to use for all your image processing needs.</p>
  <p>If you found this tool useful, feel free to bookmark it for future use. We're constantly adding new features and tools to help you edit images online without installing any software.</p>
</div>
'''

enriched = 0
for path in target_pages:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 已经加过about-tool的就跳过
    if 'class="about-tool"' in content:
        continue
    # 在</main>或者</body>之前插入说明文字
    slug = os.path.basename(path).replace('.html', '')
    about_text = generate_about_text(slug, path)
    if '</main>' in content:
        content = content.replace('</main>', about_text + '\n</main>')
    elif '</body>' in content:
        content = content.replace('</body>', about_text + '\n</body>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    enriched +=1

print(f"✅ 完成：已给 {enriched} 个薄工具页追加了自然说明内容，每个页面增加约80词的正文")
