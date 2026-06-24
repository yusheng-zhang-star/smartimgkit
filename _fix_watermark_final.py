"""Final fix for watermark workspace_html - add missing closing divs."""
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

for fname in DATA_FILES:
    fpath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(fpath):
        print(f'SKIP: {fname}')
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for t in data.get('tools', []):
        if t.get('slug') != 'watermark':
            continue
        
        html = t.get('workspace_html', '')
        # Find how-to section and truncate
        idx = html.find('<section class="how-to-section">')
        if idx > 0:
            html = html[:idx].rstrip()
        
        # Add 2 missing closing divs for tool-container and max-width container
        html = html.rstrip() + '\n          </div>\n        </div>'
        
        opens = html.count('<div')
        closes = html.count('</div>')
        t['workspace_html'] = html
        print(f'  {fname}/watermark: opens={opens}, closes={closes}, balanced={opens==closes}')
        break
    
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'SAVED: {fname}')

print('\nDone.')
