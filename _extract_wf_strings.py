# -*- coding: utf-8 -*-
"""Extract all visible text strings (between > and <) from zh/workflows pages,
dedupe, and print. Used to build a complete translation vocabulary."""
import os
import re
from collections import Counter

DST = r'e:\网站项目\smartimgkit\zh\workflows'

all_strings = Counter()
for fname in sorted(os.listdir(DST)):
    if not fname.endswith('.html') or fname in ('index.html', '_workflow_template.html'):
        continue
    html = open(os.path.join(DST, fname), encoding='utf-8').read()
    # visible text between > and <
    for m in re.finditer(r'>([^<>]{2,200})<', html):
        s = m.group(1).strip()
        # skip if already mostly Chinese or empty or pure punctuation/numbers
        if not s:
            continue
        # count chinese chars
        zh = sum(1 for c in s if '\u4e00' <= c <= '\u9fff')
        en = sum(1 for c in s if c.isalpha() and ord(c) < 128)
        if en < 2:
            continue
        # skip if already translated (zh chars present and en < zh)
        if zh > 0 and zh >= en:
            continue
        all_strings[s] += 1

print('TOTAL unique untranslated strings:', len(all_strings))
print('---')
for s, c in sorted(all_strings.items(), key=lambda x: (-x[1], x[0])):
    print('[%d] %s' % (c, s))
