import os

ADSENSE_CODE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2385875044602242" crossorigin="anonymous"></script>'

root = r'E:\网站项目\smartimgkit'
count = 0

for dirpath, dirnames, filenames in os.walk(root):
    if '.git' in dirpath or 'node_modules' in dirpath:
        continue
    for filename in filenames:
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'pagead2.googlesyndication.com' in content:
                continue
            if '</head>' in content:
                content = content.replace('</head>', ADSENSE_CODE + '\n</head>', 1)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
        except:
            pass

print(f'Modified: {count}')
