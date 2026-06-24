"""
Definitive fix for all workspace_html div balance issues across 7 language files.

Two patterns:
1. Standard tools: workspace_html ends with '      </div>' (closes tool-workspace, but template provides this)
   → Strip trailing '      </div>' lines
2. Watermark: workspace_html contains entire page (howto, guide, faq, related, footer)
   → Truncate at howto-section, then strip trailing '      </div>'
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


def balance_workspace_html(html):
    """Strip trailing </div> that matches template's tool-workspace close indent."""
    if not html:
        return html
    lines = html.split('\n')
    # Strip trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()
    # Remove trailing </div> with 6-space indent (template's '      </div>')
    while lines and re.match(r'^      </div>\s*$', lines[-1]):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    return '\n'.join(lines)


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
                continue  # balanced or missing

            # Watermark special case: entire page is in workspace_html
            if slug == 'watermark':
                idx = html.find('<section class="how-to-section">')
                if idx > 0:
                    html = html[:idx].rstrip()
                    opens = html.count('<div')
                    closes = html.count('</div>')

            new_html = balance_workspace_html(html)

            if new_html != html:
                t['workspace_html'] = new_html
                new_opens = new_html.count('<div')
                new_closes = new_html.count('</div>')
                ok = '✓' if new_opens == new_closes else f'✗ diff={new_opens - new_closes}'
                print(f'  [{fname}] {slug}: {opens}/{closes} → {new_opens}/{new_closes} {ok}')
                fixes += 1

        if fixes > 0:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f'  → SAVED ({fixes} tools)\n')
        else:
            print(f'  → no changes\n')


if __name__ == '__main__':
    main()
