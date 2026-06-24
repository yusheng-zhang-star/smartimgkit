"""Fix watermark workspace_html across all language data files.
Watermark's workspace_html incorrectly contains howto, guide, faq, related, and footer sections.
Trim to only the actual workspace content (before <section class="how-to-section">).
"""
import json
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

def fix_watermark(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tools = data.get('tools', [])
    fixed = False
    for t in tools:
        if t.get('slug') != 'watermark':
            continue
        ws = t.get('workspace_html', '')
        # Find where how-to section starts
        idx = ws.find('<section class="how-to-section">')
        if idx == -1:
            # Try other markers
            idx = ws.find('how-to-section')
            if idx > 0:
                # Find the opening tag
                tag_start = ws.rfind('<', 0, idx)
                if tag_start >= 0:
                    idx = tag_start
        
        if idx > 0:
            old_len = len(ws)
            new_ws = ws[:idx].rstrip()
            # Strip trailing </div> lines
            lines = new_ws.split('\n')
            import re
            while lines and re.match(r'^\s*</div>\s*$', lines[-1].strip()):
                lines.pop()
            new_ws = '\n'.join(lines)
            
            t['workspace_html'] = new_ws
            opens = new_ws.count('<div')
            closes = new_ws.count('</div>')
            new_len = len(new_ws)
            print(f'  {os.path.basename(fpath)}/watermark: {old_len} -> {new_len} chars, opens={opens}, closes={closes}, balanced={opens==closes}')
            fixed = True
        break
    
    if fixed:
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    return False

def main():
    for fname in DATA_FILES:
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            fix_watermark(fpath)
        else:
            print(f'SKIP: {fname}')

if __name__ == '__main__':
    main()
