#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix lang_switcher_html in JSON data files to include all 7 languages."""

import json

new_langs = """            <a href="/fr/" hreflang="fr" lang="fr">🇫🇷 Français</a>
            <a href="/vi/" hreflang="vi" lang="vi">🇻🇳 Tiếng Việt</a>
            <a href="/ar/" hreflang="ar" lang="ar">🇸🇦 العربية</a>
          </div>
        </div>"""

old_close = '          </div>\n        </div>'

for suffix in ['', '_es', '_pt', '_id']:
    fname = '_tools_data' + suffix + '.json'
    with open(fname, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    html = data['lang_switcher_html']
    
    if 'العربية' in html:
        print(fname + ': already 7 langs, skip')
        continue
    
    html = html.replace(old_close, new_langs)
    data['lang_switcher_html'] = html
    with open(fname, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    
    ok = 'العربية' in html
    print(fname + ': ' + ('OK' if ok else 'FAIL'))
