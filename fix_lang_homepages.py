"""
Fix language homepages (es/index.html, pt/index.html, id/index.html):
1. Fix CSS path: css/style.css → /css/style.css
2. Fix JS path: js/main.js → /js/main.js
3. Replace inline lang script with <script src="/js/lang.js"></script>
4. Fix dropdown links: remove onclick, add hreflang
5. Fix footer links: remove onclick
6. Fix tool card links: /tools/xxx → /<lang>/tools/xxx
7. Fix workflow links: /workflows/xxx → /<lang>/workflows/xxx
"""

import os
import re

BASE_DIR = r"E:\网站项目\smartimgkit"
LANGS = {
    "es": {"dropdown_flag": "🇪🇸", "dropdown_name": "ES"},
    "pt": {"dropdown_flag": "🇧🇷", "dropdown_name": "PT"},
    "id": {"dropdown_flag": "🇮🇩", "dropdown_name": "ID"},
}

def fix_file(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix CSS path
    content = content.replace('href="css/style.css', 'href="/css/style.css')

    # 2. Fix JS path for main.js
    content = content.replace('src="js/main.js', 'src="/js/main.js')

    # 3. Fix dropdown links: remove onclick, add hreflang
    # Pattern: <a href="/" onclick="localStorage.setItem('lang_chosen','en')"><span>🇬🇧</span> English</a>
    # Replace with: <a href="/" hreflang="en"><span>🇬🇧</span> English</a>
    dropdown_replacements = [
        (r'<a href="/" onclick="localStorage\.setItem\(\'lang_chosen\',\'en\'\)"><span>', '<a href="/" hreflang="en"><span>'),
        (r'<a href="/es/" onclick="localStorage\.setItem\(\'lang_chosen\',\'es\'\)"><span>', '<a href="/es/" hreflang="es"><span>'),
        (r'<a href="/pt/" onclick="localStorage\.setItem\(\'lang_chosen\',\'pt\'\)"><span>', '<a href="/pt/" hreflang="pt"><span>'),
        (r'<a href="/id/" onclick="localStorage\.setItem\(\'lang_chosen\',\'id\'\)"><span>', '<a href="/id/" hreflang="id"><span>'),
    ]
    for old, new in dropdown_replacements:
        content = re.sub(old, new, content)

    # 4. Fix footer links: remove onclick
    footer_replacements = [
        (r'<a href="/" onclick="localStorage\.setItem\(\'lang_chosen\',\'en\'\)" style="margin:0 6px;color:var\(--text-secondary\);text-decoration:none;">EN</a>',
         '<a href="/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">EN</a>'),
        (r'<a href="/es/" onclick="localStorage\.setItem\(\'lang_chosen\',\'es\'\)" style="margin:0 6px;color:var\(--text-secondary\);text-decoration:none;">ES</a>',
         '<a href="/es/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">ES</a>'),
        (r'<a href="/pt/" onclick="localStorage\.setItem\(\'lang_chosen\',\'pt\'\)" style="margin:0 6px;color:var\(--text-secondary\);text-decoration:none;">PT</a>',
         '<a href="/pt/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">PT</a>'),
        (r'<a href="/id/" onclick="localStorage\.setItem\(\'lang_chosen\',\'id\'\)" style="margin:0 6px;color:var\(--text-secondary\);text-decoration:none;">ID</a>',
         '<a href="/id/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">ID</a>'),
    ]
    for old, new in footer_replacements:
        content = re.sub(old, new, content)

    # 5. Remove legacy inline lang script (between the ad block script </script> and the last </script> before </body>)
    # The inline script starts with <script> after the ad block
    # Pattern: after the ad invoke.js script, there's a <script> block with toggleLangDropdown etc.
    # We need to remove everything from that <script> to its matching </script>
    
    # Find: <script>\n  function toggleLangDropdown... up to the closing </script>
    # And replace with <script src="/js/lang.js"></script>
    
    old_inline_pattern = r'\n  <script>\n  function toggleLangDropdown\(\) \{\n    document\.getElementById\(\'langSwitcher\'\)\.classList\.toggle\(\'open\'\);\n  \}\n  document\.addEventListener\(\'click\', function\(e\) \{\n    if \(\!e\.target\.closest\(\'\.lang-switcher\'\)\) \{\n      var el = document\.getElementById\(\'langSwitcher\'\);\n      if \(el\) el\.classList\.remove\(\'open\'\);\n    \}\n  \}\);[\s\S]*?\n  </script>'
    
    if re.search(old_inline_pattern, content):
        content = re.sub(old_inline_pattern, '\n  <script src="/js/lang.js"></script>', content)
    else:
        # Try a simpler fallback: find the first <script> after "END AD UNITS" comment
        marker = "<!-- ===== END AD UNITS ===== -->"
        marker_pos = content.find(marker)
        if marker_pos > 0:
            # Find the next <script> block after marker
            after_marker = content[marker_pos + len(marker):]
            script_start = after_marker.find('<script>')
            if script_start >= 0:
                # Find matching </script>
                script_end = after_marker.find('</script>', script_start)
                if script_end >= 0:
                    # Check if this is the lang script (contains toggleLangDropdown)
                    script_content = after_marker[script_start:script_end + 9]
                    if 'toggleLangDropdown' in script_content:
                        before = content[:marker_pos + len(marker)]
                        rest = after_marker[script_end + 9:]
                        content = before + '\n  <script src="/js/lang.js"></script>\n' + rest

    # 6. Fix tool card links: /tools/xxx → /<lang>/tools/xxx (only in main content)
    # These are href="/tools/xxx.html" patterns
    content = re.sub(
        r'href="(/tools/[^"]+\.html)"',
        r'href="/' + lang + r'\1"',
        content
    )
    
    # 7. Fix workflow card links (in Workflows section): /workflows/xxx → /<lang>/workflows/xxx
    content = re.sub(
        r'href="(/workflows/[^"]+\.html)"',
        r'href="/' + lang + r'\1"',
        content
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Fixed {filepath}")

# Run for all 3 languages
for lang_code in LANGS:
    filepath = os.path.join(BASE_DIR, lang_code, "index.html")
    if os.path.exists(filepath):
        fix_file(filepath, lang_code)
    else:
        print(f"WARNING: {filepath} not found!")

print("\nDone! All 3 language homepages fixed.")
