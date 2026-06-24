"""
SmartImgKit 全站布局审计脚本 v2
检测：重复ID、容器结构、隐藏元素、死链、内链完整性
"""
import os, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser

BASE = r"E:\网站项目\smartimgkit"

class LayoutAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.div_depth = 0
        self.main_depth = 0
        self.in_main = False
        self.in_container = False
        self.container_depth = -1
        self.in_faq = False
        self.faq_count = 0
        self.in_section = False
        self.section_stack = []  # track nested sections
        self.all_links = []  # href links
        self.images = []
        self.hidden_elements = []  # elements with class hidden
        self.tags = Counter()
        self.errors = []
        self.tag_stack = []
        self.line_no = 0

    def handle_starttag(self, tag, attrs):
        self.tags[tag] += 1
        attr_dict = dict(attrs)
        
        # Track IDs
        if 'id' in attr_dict:
            self.ids.append(attr_dict['id'])
        
        # Track links
        href = attr_dict.get('href', '')
        if href and tag == 'a':
            self.all_links.append(('a', href))
        
        src = attr_dict.get('src', '')
        if src and tag in ('img', 'script', 'iframe', 'source'):
            self.all_links.append((tag, src))
            if tag == 'img':
                self.images.append(src)
        
        # CSS background images
        style = attr_dict.get('style', '')
        bg_match = re.search(r'url\(["\']?([^)"\']+)', style)
        if bg_match:
            self.all_links.append(('css-bg', bg_match.group(1)))
        
        # Track hidden elements
        classes = attr_dict.get('class', '')
        if 'hidden' in classes.split() and tag not in ('html', 'body', 'head'):
            style_inline = attr_dict.get('style', '')
            self.hidden_elements.append({
                'tag': tag,
                'id': attr_dict.get('id', ''),
                'class': classes,
                'style': style_inline
            })
        
        if tag == 'main':
            self.in_main = True
            self.main_depth = self.div_depth
        
        if tag == 'section':
            self.in_section = True
            self.section_stack.append(attr_dict.get('class', ''))
        
        if 'container' in classes and not self.in_container:
            self.in_container = True
            self.container_depth = self.div_depth
        
        if 'faq-section' in classes or 'faq' in attr_dict.get('id', ''):
            self.in_faq = True
            self.faq_count += 1
        
        self.tag_stack.append(tag)
        if tag in ('div', 'section', 'main', 'article', 'nav', 'header', 'footer'):
            self.div_depth += 1

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
            # Check if container was closed inside main
            if self.in_container and self.div_depth == self.container_depth:
                self.in_container = False
        
        if tag == 'section':
            self.in_section = False
            if self.section_stack:
                self.section_stack.pop()
        
        if self.in_container and tag == 'div' and self.div_depth == self.container_depth + 1:
            # Closing container's parent div
            pass
        
        if tag in ('div', 'section', 'main', 'article', 'nav', 'header', 'footer'):
            self.div_depth -= 1
            if self.div_depth <= self.container_depth and self.in_container:
                self.in_container = False
        
        self.tag_stack.pop() if self.tag_stack else None


def check_page(filepath):
    """Check a single HTML file for layout issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    auditor = LayoutAuditor()
    # Feed line by line for better error tracking
    for i, line in enumerate(content.split('\n'), 1):
        auditor.line_no = i
        try:
            auditor.feed(line + '\n')
        except:
            pass
    
    issues = []
    rel_path = os.path.relpath(filepath, BASE)
    
    # 1. Duplicate IDs
    id_counts = Counter(auditor.ids)
    dupes = {k: v for k, v in id_counts.items() if v > 1}
    if dupes:
        for id_name, count in dupes.items():
            issues.append(f"重复ID: #{id_name} 出现{count}次")
    
    # 2. Check for important missing IDs (file input)
    if 'fileInput' not in id_counts:
        # Only for tool pages
        if '/tools/' in rel_path:
            issues.append("缺少 #fileInput")
    
    # 3. FAQ sections outside container
    if auditor.faq_count > 1 and not auditor.in_container:
        issues.append(f"FAQ section 可能在 container 外 (共{auditor.faq_count}个FAQ)")
    
    # 4. Hidden file inputs
    for elem in auditor.hidden_elements:
        if elem['tag'] == 'input' and elem.get('type') == 'file':
            # Check if it has id
            if not elem['id']:
                issues.append(f"隐藏的 file input 缺少 id")
    
    # 5. Broken internal links
    broken = []
    external = []
    for tag, link in auditor.all_links:
        if link.startswith('http'):
            external.append(link)
        elif link.startswith('/') and not link.startswith('//'):
            # Internal absolute link
            if link.endswith(('.png', '.jpg', '.webp', '.svg', '.ico', '.js', '.css')):
                local_path = BASE + link
                if not os.path.exists(local_path):
                    broken.append(link)
            elif '.html' in link or not '.' in link.split('/')[-1]:
                # HTML link or directory
                local_path = BASE + link
                if not os.path.exists(local_path) and not os.path.exists(local_path + '.html'):
                    broken.append(link)
        elif link.startswith('#'):
            # Anchor - check if the target exists on the page
            anchor = link[1:]
            if anchor and anchor not in auditor.ids:
                broken.append(link)
    
    if broken:
        issues.append(f"死链: {broken}")
    
    return {
        'file': rel_path,
        'issues': issues,
        'link_count': len(auditor.all_links),
        'internal_links': len([l for t, l in auditor.all_links if l.startswith('/')]),
        'external_links': len([l for t, l in auditor.all_links if l.startswith('http')]),
        'broken_links': len(broken),
        'unique_ids': len(set(auditor.ids)),
        'total_ids': len(auditor.ids),
        'hidden_elements': len(auditor.hidden_elements),
        'faq_count': auditor.faq_count,
        'tags': dict(auditor.tags.most_common(10))
    }


def main():
    print("=" * 60)
    print("SmartImgKit 全站布局 + 死链审计")
    print("=" * 60)
    
    # Collect all HTML files
    html_files = []
    for root, dirs, files in os.walk(BASE):
        # Skip hidden dirs and backups
        dirs[:] = [d for d in dirs if not d.startswith('_') and not d.startswith('.') and d != '__pycache__' and d != '.git']
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    
    print(f"\n找到 {len(html_files)} 个 HTML 文件\n")
    
    # Check each file
    results = []
    pages_with_issues = 0
    
    for fp in html_files:
        result = check_page(fp)
        results.append(result)
        if result['issues']:
            pages_with_issues += 1
            print(f"❌ {result['file']}")
            for issue in result['issues']:
                print(f"   → {issue}")
    
    # Summary
    total_ids = sum(r['total_ids'] for r in results)
    total_unique = sum(r['unique_ids'] for r in results)
    total_links = sum(r['link_count'] for r in results)
    total_broken = sum(r['broken_links'] for r in results)
    total_hidden = sum(r['hidden_elements'] for r in results)
    
    print(f"\n{'='*60}")
    print(f"📊 汇总统计")
    print(f"{'='*60}")
    print(f"HTML 文件:         {len(html_files)}")
    print(f"有问题页面:        {pages_with_issues}")
    print(f"总 ID 数:          {total_ids}")
    print(f"唯一 ID 数:        {total_unique}  (重复: {total_ids - total_unique})")
    print(f"总链接数:          {total_links}")
    print(f"死链数:            {total_broken}")
    print(f"隐藏元素:          {total_hidden}")
    print(f"干净页面:          {len(html_files) - pages_with_issues}")
    
    # Map of IDs per file (spot check)
    id_summary = [(r['file'], r['unique_ids'], r['total_ids']) for r in results]
    id_summary.sort(key=lambda x: x[2], reverse=True)
    print(f"\n📋 ID 数量 Top 10 页面:")
    for fname, uid, tid in id_summary[:10]:
        flag = "⚠️ " if uid != tid else "✅"
        print(f"  {flag} {fname}: {uid} unique / {tid} total")
    
    # Write full report
    report_path = os.path.join(BASE, '_audit_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n完整报告: {report_path}")
    
    return pages_with_issues == 0


if __name__ == '__main__':
    ok = main()
    print(f"\n{'✅ 全部通过' if ok else '⚠️ 发现问题，请查看上方详情'}")
