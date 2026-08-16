# -*- coding: utf-8 -*-
"""Trace div open/close stack for id-photo localized versions to find the missing </div>.
Local-only. Do NOT commit.
"""
import os, re

root = r'e:\网站项目\smartimgkit'
files = ['es/tools/id-photo.html', 'id/tools/id-photo.html', 'pt/tools/id-photo.html']

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

for rel in files:
    fp = os.path.join(root, rel.replace('/', os.sep))
    with open(fp, 'rb') as fh:
        raw = fh.read()
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    lines = raw.decode('utf-8').splitlines()

    stack = []  # list of (tag, lineno, snippet)
    issues = []
    for i, line in enumerate(lines, 1):
        # find all tags
        for m in re.finditer(r'<(/?)(\w+)([^>]*)>', line):
            closing = m.group(1) == '/'
            tag = m.group(2).lower()
            if tag in VOID:
                continue
            if not closing:
                # skip self-closing like <div/>
                attrs = m.group(3)
                if attrs.rstrip().endswith('/'):
                    continue
                stack.append((tag, i, line.strip()[:80]))
            else:
                if not stack:
                    issues.append(('extra-close', tag, i, line.strip()[:80]))
                    continue
                # pop until match
                found = False
                for j in range(len(stack)-1, -1, -1):
                    if stack[j][0] == tag:
                        # anything above is unclosed
                        for k in range(len(stack)-1, j, -1):
                            issues.append(('unclosed', stack[k][0], stack[k][1], stack[k][2]))
                        del stack[j:]
                        found = True
                        break
                if not found:
                    issues.append(('mismatch-close', tag, i, line.strip()[:80]))

    print('=== %s ===' % rel)
    print('final stack (unclosed at EOF): %d' % len(stack))
    for t, ln, s in stack:
        print('  <%s> at L%d: %s' % (t, ln, s))
    print('issues: %d' % len(issues))
    for kind, tag, ln, s in issues[:10]:
        print('  %s: <%s> at L%d: %s' % (kind, tag, ln, s))
    print()
