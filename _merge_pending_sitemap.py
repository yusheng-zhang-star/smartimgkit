import re

# 读取sitemap-en.xml
with open("sitemap-en.xml", "r", encoding="utf-8") as f:
    en_content = f.read()

# 读取pending
with open("sitemap-pending.xml", "r", encoding="utf-8") as f:
    pending_content = f.read()

# 提取pending里所有英文博客和英文工具URL
pending_urls = re.findall(r'<url><loc>(https://smartimgkit\.com/(?:blog/|tools/)[^<]+)</loc>.*?</url>', pending_content)
print(f"从pending提取到 {len(pending_urls)} 个英文URL")

# 提取sitemap-en里已有的URL
existing_urls = re.findall(r'<loc>(https://smartimgkit\.com/(?:blog/|tools/)[^<]+)</loc>', en_content)

# 找新增的URL
new_urls = [u for u in pending_urls if u not in existing_urls]
print(f"其中 {len(new_urls)} 个URL是新增的，需要加入sitemap-en")

# 把新URL追加到</urlset>之前
new_url_lines = ""
for u in new_urls:
    new_url_lines += f'  <url><loc>{u}</loc><lastmod>2026-10-13</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'

en_content = en_content.replace("</urlset>", new_url_lines + "</urlset>")

with open("sitemap-en.xml", "w", encoding="utf-8") as f:
    f.write(en_content)

# 从sitemap.xml里删除pending条目
with open("sitemap.xml", "r", encoding="utf-8") as f:
    sitemap_index = f.read()
sitemap_index = sitemap_index.replace('  <sitemap><loc>https://smartimgkit.com/sitemap-pending.xml</loc></sitemap>\n', '')
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_index)

print("✅ 完成：已把pending里的新URL合并到sitemap-en.xml，从sitemapindex中移除pending条目")
