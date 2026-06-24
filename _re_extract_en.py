"""Re-extract English tools data from HTML files, replacing workspace_html."""
import json
import os
import re

ROOT = r'E:\网站项目\smartimgkit'
tools_dir = os.path.join(ROOT, 'tools')

def extract_workspace(html):
    """Extract the inner content of tool-workspace div."""
    # Find <div class="tool-workspace"> ... </div>
    # But we need to handle nested divs
    start = html.find('<div class="tool-workspace">')
    if start == -1:
        return ''
    
    # Find the matching closing </div>
    pos = start + len('<div class="tool-workspace">')
    depth = 1
    i = pos
    while i < len(html) and depth > 0:
        if html[i:i+4] == '<div' and html[i:i+5] != '<div ' and html[i:i+5] != '<div>':
            pass  # not a div
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end = i
                break
        i += 1
    else:
        return ''  # not found
    
    inner = html[pos:end].strip()
    return inner


def main():
    files = sorted([f for f in os.listdir(tools_dir) if f.endswith('.html')])
    print(f'Found {len(files)} HTML files')

    # Load existing data to preserve lang-level fields
    with open(os.path.join(ROOT, '_tools_data.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    tools = []
    for fname in files:
        fpath = os.path.join(tools_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        ws = extract_workspace(html)
        opens = ws.count('<div')
        closes = ws.count('</div>')
        
        # Find matching tool in existing data
        slug = fname.replace('.html', '')
        old_tool = None
        for t in data['tools']:
            if t.get('slug') == slug:
                old_tool = t
                break
        
        if old_tool:
            old_ws = old_tool.get('workspace_html', '')
            old_o = old_ws.count('<div')
            old_c = old_ws.count('</div>')
            status = '✓' if opens == closes else f'✗ diff={opens-closes}'
            old_status = '✓' if old_o == old_c else f'✗ diff={old_o-old_c}'
            print(f'  {slug}: was {old_o}/{old_c} → now {opens}/{closes} {status}')
            
            # Only update workspace_html, preserve other fields
            old_tool['workspace_html'] = ws
            tools.append(old_tool)

    data['tools'] = tools
    
    with open(os.path.join(ROOT, '_tools_data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('SAVED _tools_data.json')

if __name__ == '__main__':
    main()
