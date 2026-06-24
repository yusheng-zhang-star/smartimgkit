"""
Fix workspace_html div balance across all language data files.
Issue: workspace_html for many tools ends with extra </div>,
causing the template's tool-workspace close div to close container instead.
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
    """Remove trailing </div> lines that match the template's 6-space indent."""
    if not html:
        return html, 0
    lines = html.split('\n')
    removed = 0
    
    # Strip trailing blank lines first
    while lines and not lines[-1].strip():
        lines.pop()
    
    # Remove trailing </div> with 6-space indent (matches template '      </div>')
    while lines and re.match(r'^      </div>\s*$', lines[-1]):
        lines.pop()
        removed += 1
        # Also strip trailing blank lines between divs
        while lines and not lines[-1].strip():
            lines.pop()
    
    return '\n'.join(lines), removed


def clean_converter_workspace(html):
    """Converter has ad-placeholder and extra junk in workspace_html."""
    if not html:
        return html, 0
    # Remove ad-placeholder line and everything after it
    # Also remove extra closing divs
    lines = html.split('\n')
    cleaned = []
    removed = 0
    for line in lines:
        if 'ad-placeholder' in line.lower():
            removed += 1
            continue
        if line.strip() in ('</body>', '</html>'):
            removed += 1
            continue
        if '<script' in line and '</script>' not in line:
            # Start of inline script that doesn't belong in workspace
            break
        cleaned.append(line)
    
    if len(cleaned) < len(lines):
        removed += len(lines) - len(cleaned)
    
    html = '\n'.join(cleaned)
    # Now strip trailing </div>s
    html, divs_removed = strip_trailing_close_divs(html)
    return html, removed + divs_removed


def clean_watermark_workspace(html):
    """Watermark has scripts and </body></html> in workspace_html."""
    if not html:
        return html, 0
    lines = html.split('\n')
    # Find where the actual workspace ends and scripts begin
    # Look for <script> tag after workspace content
    cleaned = []
    removed = 0
    in_script = False
    for line in lines:
        if '<script>' in line or '<script ' in line:
            in_script = True
        if in_script:
            removed += 1
            continue
        if line.strip() in ('</body>', '</html>'):
            removed += 1
            continue
        if in_script and '</script>' in line:
            in_script = False
            removed += 1
            continue
        cleaned.append(line)
    
    html = '\n'.join(cleaned)
    html, divs_removed = strip_trailing_close_divs(html)
    return html, removed + divs_removed


def main():
    total_fixes = 0
    for fname in DATA_FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            print(f'SKIP: {fname} (not found)')
            continue
        
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tools = data.get('tools', [])
        file_fixes = 0
        for t in tools:
            slug = t.get('slug', '')
            html = t.get('workspace_html', '')
            if not html:
                continue
            
            opens = html.count('<div')
            closes = html.count('</div>')
            
            if closes <= opens:
                continue  # already balanced or missing (missing is different issue)
            
            # Special handling for converter and watermark
            if slug == 'converter':
                new_html, fixed = clean_converter_workspace(html)
            elif slug == 'watermark':
                new_html, fixed = clean_watermark_workspace(html)
            else:
                new_html, fixed = strip_trailing_close_divs(html)
            
            if fixed > 0:
                t['workspace_html'] = new_html
                new_opens = new_html.count('<div')
                new_closes = new_html.count('</div>')
                print(f'  {fname}/{slug}: removed {fixed} lines, opens={new_opens}, closes={new_closes}, balanced={new_opens==new_closes}')
                file_fixes += 1
                total_fixes += 1
        
        if file_fixes > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'SAVED: {fname} ({file_fixes} tools fixed)')
        else:
            print(f'OK: {fname} (no issues)')
    
    print(f'\n=== DONE: {total_fixes} total fixes across {len(DATA_FILES)} files ===')

if __name__ == '__main__':
    main()
