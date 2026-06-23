"""
Fix all tool pages: change relative lang.js path to absolute /js/lang.js
Also fix relative CSS path to absolute /css/style.css
"""
import os
import glob

BASE_DIR = r"E:\网站项目\smartimgkit"

# All tool page directories
dirs_to_fix = [
    os.path.join(BASE_DIR, "tools"),
    os.path.join(BASE_DIR, "es", "tools"),
    os.path.join(BASE_DIR, "pt", "tools"),
    os.path.join(BASE_DIR, "id", "tools"),
]

fixed_count = 0

for d in dirs_to_fix:
    if not os.path.isdir(d):
        print(f"SKIP (not found): {d}")
        continue
    
    for filepath in glob.glob(os.path.join(d, "*.html")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        modified = False
        
        # Fix relative lang.js path to absolute
        # ../js/lang.js or ../../js/lang.js → /js/lang.js
        if 'src="../js/lang.js"' in content:
            content = content.replace('src="../js/lang.js"', 'src="/js/lang.js"')
            modified = True
        if 'src="../../js/lang.js"' in content:
            content = content.replace('src="../../js/lang.js"', 'src="/js/lang.js"')
            modified = True
        
        # Fix relative CSS path to absolute (for translated tool pages)
        if 'href="../../css/style.css' in content:
            content = content.replace('href="../../css/style.css', 'href="/css/style.css')
            modified = True
        if 'href="../css/style.css' in content:
            content = content.replace('href="../css/style.css', 'href="/css/style.css')
            modified = True
        
        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print(f"Fixed: {filepath}")

print(f"\nDone! Fixed {fixed_count} tool pages.")
