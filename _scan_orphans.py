import os, re

all_pages = []
# 收集所有根目录下的html页面
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['_backup', '_test', 'src', '.wrangler', 'node_modules', 'zh/', 'es/', 'fr/', 'pt/', 'ar/', 'id/', 'vi/']):
        continue
    for f in files:
        if f.endswith('.html') and not f.startswith('_'):
            rel = os.path.join(root, f).replace('./', '/').replace('\\', '/')
            all_pages.append(rel)

# 收集所有页面里的内链
linked = set()
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['_backup', '_test', 'src', '.wrangler', 'node_modules']):
        continue
    for f in files:
        if f.endswith('.html'):
            try:
                with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
                    content = fh.read()
                # 提取所有href
                hrefs = re.findall(r'href="(/[^"#]*)"', content)
                for h in hrefs:
                    # 去掉末尾斜杠，标准化
                    h = h.rstrip('/')
                    if not h.endswith('.html'):
                        h += '.html'
                    linked.add(h)
            except:
                pass

# 找孤儿页：存在但没有任何其他页面链接指向
orphans = []
for p in all_pages:
    # 标准化p
    p_norm = p
    if not p_norm.endswith('.html'):
        p_norm += '.html'
    if p_norm not in linked:
        orphans.append(p)

print(f"总页面数: {len(all_pages)}")
print(f"发现孤儿页（没有内链指向）: {len(orphans)}个")
for o in sorted(orphans)[:30]:
    print(f"  {o}")

with open("_orphan_pages_list.txt", "w", encoding="utf-8") as f:
    for o in orphans:
        f.write(o+"\n")
print("\n✅ 孤儿页列表已保存到_orphan_pages_list.txt")
