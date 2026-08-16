# -*- coding: utf-8 -*-
"""检查 zh/blog 和 zh/workflows HTML 语法：标签闭合、script/style 完整性、破损实体"""
import io, os, re
from html.parser import HTMLParser

class TagChecker(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f'多余结束标签 </{tag}> at {self.getpos()}')
            return
        # 找到匹配的开标签
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                # 中间未闭合的标签
                for j in range(len(self.stack)-1, i, -1):
                    t, pos = self.stack[j]
                    self.errors.append(f'未闭合 <{t}> at {pos} (在 </{tag}> 之前)')
                del self.stack[i:]
                return
        self.errors.append(f'未匹配结束标签 </{tag}> at {self.getpos()}')

def check_file(fpath):
    fname = os.path.basename(fpath)
    h = io.open(fpath, encoding='utf-8').read()
    issues = []

    # 1. script/style 标签闭合检查
    script_open = len(re.findall(r'<script\b', h))
    script_close = len(re.findall(r'</script>', h))
    if script_open != script_close:
        issues.append(f'<script> 开{script_open} 闭{script_close} 不匹配')
    style_open = len(re.findall(r'<style\b', h))
    style_close = len(re.findall(r'</style>', h))
    if style_open != style_close:
        issues.append(f'<style> 开{style_open} 闭{style_close} 不匹配')

    # 2. 破损的 HTML 实体（& 后面不是合法实体）
    for m in re.finditer(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;|copy;|rarr;|rsaquo;|mdash;|ndash;|hellip;|nbsp;|laquo;|raquo;|ldquo;|rdquo;|lsquo;|rsquo;|trade;|reg;|deg;|times;|divide;|plusmn;|frac12;|frac14;|frac34;|sup2;|sup3;|eacute;|egrave;|agrave;|ccedil;|euro;|pound;|cent;|yen;|sect;|para;|middot;|bull;|dagger;|Dagger;|permil;|prime;|Prime;|lsaquo;|rsaquo;)', h):
        ctx = h[max(0,m.start()-20):m.start()+20]
        issues.append(f'可疑实体 & at pos {m.start()}: ...{ctx}...')

    # 3. 标签嵌套检查（用 HTMLParser）
    # 只检查 body 部分，跳过 script/style 内容
    body = re.search(r'<body[^>]*>(.*)</body>', h, re.S)
    if body:
        body_html = body.group(1)
        # 移除 script 和 style 块
        body_html = re.sub(r'<script[^>]*>.*?</script>', '', body_html, flags=re.S)
        body_html = re.sub(r'<style[^>]*>.*?</style>', '', body_html, flags=re.S)
        # 移除注释
        body_html = re.sub(r'<!--.*?-->', '', body_html, flags=re.S)
        checker = TagChecker()
        try:
            checker.feed(body_html)
        except Exception as e:
            issues.append(f'HTMLParser 异常: {e}')
        if checker.stack:
            for t, pos in checker.stack:
                issues.append(f'未闭合 <{t}> at {pos}')
        issues.extend(checker.errors)

    # 4. 重复 id 检查
    ids = re.findall(r'\bid="([^"]+)"', h)
    seen_ids = {}
    for idv in ids:
        seen_ids[idv] = seen_ids.get(idv, 0) + 1
    for idv, cnt in seen_ids.items():
        if cnt > 1 and idv not in ('adVerticalRight',):
            issues.append(f'重复 id="{idv}" ({cnt}次)')

    return fname, issues

# 检查 blog 目录
for subdir in ['blog', 'workflows']:
    d = os.path.join(r'e:\网站项目\smartimgkit\zh', subdir)
    if not os.path.isdir(d):
        continue
    print(f'\n=== 检查 zh/{subdir} ===')
    files = sorted(f for f in os.listdir(d) if f.endswith('.html') and not f.startswith('_'))
    total_issues = 0
    for fname in files:
        fpath = os.path.join(d, fname)
        name, issues = check_file(fpath)
        if issues:
            total_issues += len(issues)
            print(f'\n[{name}] {len(issues)} 个问题:')
            for iss in issues[:15]:
                print(f'  - {iss}')
            if len(issues) > 15:
                print(f'  ... 还有 {len(issues)-15} 个')
        else:
            print(f'[OK] {name}')
    print(f'\nzh/{subdir} 共 {total_issues} 个问题')
