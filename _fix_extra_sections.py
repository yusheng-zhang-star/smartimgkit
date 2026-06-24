"""
Fix workspace_html that contains extra sections (panel, howto, guide, FAQ content).
Truncate at the first non-workspace section marker, then strip trailing </div>.
"""
import json
import re
import os

DATA_FILES = [
    '_tools_data.json',
    '_tools_data_es.json',
    '_tools_data_pt.json',
    '_tools_data_id.json',
    '_tools_data_fr.json',
    '_tools_data_vi.json',
    '_tools_data_ar.json',
]

BASE_DIR = r'E:\网站项目\smartimgkit'

SECTION_MARKERS = [
    '<section class="panel',
    '<section class="how-to',
    '<section',
    '<h2>',
    '<!-- How To',
    '<!-- How-To',
    '<div class="guide-',
    '<div class="tip"',
]


def truncate_to_workspace(html):
    """Find where non-workspace content starts and truncate."""
    if not html:
        return html
    earliest = len(html)
    for marker in SECTION_MARKERS:
        pos = html.find(marker)
        if pos != -1 and pos < earliest:
            before = html[:pos].strip()
            if len(before) > 50:
                earliest = pos
    if earliest < len(html):
        html = html[:earliest].rstrip()
    return html


def strip_trailing_close(html):
    """Remove trailing </div> lines (possibly with comments) if they cause imbalance."""
    if not html:
        return html
    opens = html.count('<div')
    closes = html.count('</div>')
    if closes <= opens:
        return html
    
    lines = html.split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    
    # Check if last line ends with </div> (possibly followed by comments)
    last = lines[-1].strip() if lines else ''
    # Match: </div> at end, optionally preceded by whitespace
    # Also match: </div><!-- ... -->
    if re.search(r'</div>\s*(?:<!--.*?-->)?\s*$', last) and last.count('</div>') == 1:
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    
    result = '\n'.join(lines)
    new_opens = result.count('<div')
    new_closes = result.count('</div>')
    
    if new_opens == new_closes:
        return result
    return html  # revert


def main():
    total_fixes = 0
    for fname in DATA_FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixes = 0
        for t in data['tools']:
            html = t.get('workspace_html', '')
            if not html:
                continue
            
            opens = html.count('<div')
            closes = html.count('</div>')
            if closes <= opens:
                continue
            
            slug = t.get('slug', 'unknown')
            
            # Truncate extra sections
            new_html = truncate_to_workspace(html)
            if new_html != html:
                t['workspace_html'] = new_html
                html = new_html
            
            # Try stripping trailing </div>
            final_html = strip_trailing_close(html)
            if final_html != html:
                t['workspace_html'] = final_html
            
            new_opens = t['workspace_html'].count('<div')
            new_closes = t['workspace_html'].count('</div>')
            status = '✓' if new_opens == new_closes else f'✗ diff={new_opens - new_closes}'
            print(f'  [{fname}] {slug}: {opens}/{closes} → {new_opens}/{new_closes} {status}')
            fixes += 1
        
        if fixes > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'  → SAVED ({fixes} tools)\n')
        else:
            print(f'  [{fname}] → no changes\n')
        total_fixes += fixes
    
    # Final verification
    print(f'\n=== Verification ===')
    for fname in DATA_FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        bad = []
        for t in data['tools']:
            html = t.get('workspace_html', '')
            if html:
                o = html.count('<div')
                c = html.count('</div>')
                if o != c:
                    bad.append(t['slug'] + '(' + str(o) + '/' + str(c) + ')')
        if bad:
            print(f'  {fname}: ❌ {len(bad)} unbalanced: {bad[:5]}...')
        else:
            print(f'  {fname}: ✅ all balanced')
    
    print(f'\nTotal fixes: {total_fixes}')

if __name__ == '__main__':
    main()
