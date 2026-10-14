import os, re

deleted = 0
for root, dirs, files in os.walk('.'):
    if any(x in root for x in ['_backup', '_test', 'src', '.wrangler', 'node_modules']):
        continue
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                if 'class="about-tool"' in content:
                    # 正则匹配整个about-tool div块并删除
                    new_content = re.sub(r'\s*<div class="about-tool".*?</div>\s*', '\n', content, flags=re.DOTALL)
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as fh:
                            fh.write(new_content)
                        deleted +=1
            except Exception as e:
                pass

print(f"✅ 已回滚删除 {deleted} 个页面上的重复About模板，消除doorway page风险")
