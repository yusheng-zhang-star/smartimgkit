"""
One-shot fix: strip extra </div> from workspace_html across all 7 language files.
Also fixes watermark's broken workspace_html (contains entire page content).

Rule:
- workspace_html should NOT close the tool-workspace div (template provides that)
- Remove trailing </div> lines that match the template's 6-space indent
- For watermark: truncate at <section class="how-to-section"> and add missing container closes
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


def strip_trailing_close_divs(html):
    """Remove trailing </div> lines with 6-space indent (template's tool-workspace close)."""
    if not html:
        return html
    lines = html.split('\n')
    # Strip trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()
    # Remove trailing </div> with 6-space indent
    while lines and re.match(r'^      </div>\s*$', lines[-1]):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    return '\n'.join(lines)


def fix_watermark_workspace(html):
    """Watermark has entire page content in workspace_html. Extract only the workspace part."""
    if not html:
        return html
    
    # Find where how-to section starts (the workspace ends here)
    idx = html.find('<section class="how-to-section">')
    if idx == -1:
        idx = html.find('how-to-section')
        if idx > 0:
            # Find the opening < tag
            tag_start = html.rfind('<', 0, idx)
            if tag_start >= 0:
                idx = tag_start
    
    if idx > 0:
        html = html[:idx].rstrip()
    
    # Now add the 2 missing closing divs for tool-container and its inner max-width container
    # (The original markup was missing these, which is why the full page was jammed in)
    html = html.rstrip() + '\n          </div>\n        </div>'
    
    return html


def main():
    for fname in DATA_FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            print(f'SKIP: {fname}')
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tools = data.get('tools', [])
        fixes = 0
        for t in tools:
            slug = t.get('slug', '')
            html = t.get('workspace_html', '')
            if not html:
                continue
            
            opens = html.count('<div')
            closes = html.count('</div>')
            
            if closes <= opens:
                continue  # already balanced or missing closes (different issue)
            
            if slug == 'watermark':
                new_html = fix_watermark_workspace(html)
            else:
                new_html = strip_trailing_close_divs(html)
            
            if new_html != html:
                t['workspace_html'] = new_html
                new_opens = new_html.count('<div')
                new_closes = new_html.count('</div>')
                balanced = '✓' if new_opens == new_closes else f'✗ (diff={new_opens - new_closes})'
                print(f'  [{fname}] {slug}: opens {opens}→{new_opens}, closes {closes}→{new_closes} {balanced}')
                fixes += 1
        
        if fixes > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'SAVED: {fname} ({fixes} tools fixed)\n')
        else:
            print(f'OK: {fname} (no changes needed)\n')

if __name__ == '__main__':
    main()
