# -*- coding: utf-8 -*-
"""Trace all 5 remaining ico-icon-generator localized files to find exact imbalance location.
Local-only. Do NOT commit.
"""
import os, re

root = r'e:\网站项目\smartimgkit'
files = ['fr/tools/ico-icon-generator.html', 'vi/tools/ico-icon-generator.html',
         'ar/tools/ico-icon-generator.html', 'pt/tools/ico-icon-generator.html',
         'id/tools/ico-icon-generator.html']

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

for rel in files:
    fp = os.path.join(root, rel.replace('/', os.sep))
    with open(fp, 'rb') as fh:
        raw = fh.read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    lines = raw.decode('utf-8').splitlines()

    stack = []
    issues = []
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'<(/?)(\w+)([^>]*)>', line):
            closing = m.group(1) == '/'
            tag = m.group(2).lower()
            if tag in VOID:
                continue
            if not closing:
                attrs = m.group(3)
                if attrs.rstrip().endswith('/'):
                    continue
                stack.append((tag, i, line.strip()[:90]))
            else:
                if not stack:
                    issues.append(('extra-close', tag, i, line.strip()[:90]))
                    continue
                found = False
                for j in range(len(stack)-1, -1, -1):
                    if stack[j][0] == tag:
                        for k in range(len(stack)-1, j, -1):
                            issues.append(('unclosed', stack[k][0], stack[k][1], stack[k][2], 'closedby', tag, i))
                        del stack[j:]
                        found = True
                        break
                if not found:
                    issues.append(('mismatch-close', tag, i, line.strip()[:90]))

    print('=== %s ===' % rel)
    print('final stack: %d, issues: %d' % (len(stack), len(issues)))
    for t, ln, s in stack:
        print('  EOF-unclosed: <%s> L%d: %s' % (t, ln, s))
    for it in issues:
        print('  %s' % (it,))
    print()
