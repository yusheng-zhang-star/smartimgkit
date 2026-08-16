# -*- coding: utf-8 -*-
"""Quick HTML tag-balance check for git-tracked HTML files. Local-only. Do NOT commit.
Checks for unbalanced div/span/nav/section/article and unclosed important tags.
"""
import os, re, subprocess, html.parser

root = r'e:\网站项目\smartimgkit'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

out = subprocess.check_output(['git', 'ls-files', '*.html'], cwd=root, text=True)
files = [l.strip() for l in out.splitlines() if l.strip()]

class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(('extra-close', tag, self.getpos()))
            return
        # find matching
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                # anything above is unclosed
                for j in range(len(self.stack)-1, i, -1):
                    t, p = self.stack[j]
                    self.errors.append(('unclosed', t, p))
                del self.stack[i:]
                return
        self.errors.append(('mismatch-close', tag, self.getpos()))

problems = []
for rel in files:
    if rel.startswith('_backup_') or rel.startswith('src/'):
        continue
    fp = os.path.join(root, rel.replace('/', os.sep))
    try:
        with open(fp, 'rb') as fh:
            raw = fh.read()
        if raw[:3] == b'\xef\xbb\xbf':
            raw = raw[3:]
        c = raw.decode('utf-8', errors='replace')
    except Exception as e:
        problems.append((rel, 'read-error: %s' % e))
        continue
    ck = Checker()
    try:
        ck.feed(c)
    except Exception as e:
        problems.append((rel, 'parse-error: %s' % e))
        continue
    if ck.stack:
        for t, p in ck.stack:
            problems.append((rel, 'unclosed-at-end: <%s> line %d' % (t, p[0])))
    for kind, tag, p in ck.errors:
        problems.append((rel, '%s: <%s> line %d' % (kind, tag, p[0])))

print('=== tag-balance problems: %d ===' % len(problems))
for r, msg in problems[:60]:
    print('%-45s %s' % (r, msg))
if len(problems) > 60:
    print('... +%d more' % (len(problems)-60))
