#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re

BASE = r'e:\网站项目\smartimgkit\ar'
total = 0
ok = 0
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.html'):
            total += 1
            html = open(os.path.join(root, f), encoding='utf-8').read()
            tag = re.search(r'<html[^>]*>', html)
            if tag and 'dir="rtl"' in tag.group(0):
                ok += 1
print('%d/%d Arabic pages have dir="rtl"' % (ok, total))
