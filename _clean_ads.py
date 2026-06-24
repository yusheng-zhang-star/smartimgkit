"""Clean ad-related content from _tools_data_*.json files.
Removes: <!-- AdSense --> comments, <div class="ad-placeholder">...</div> blocks.
"""
import json
import re
import glob
import os

BASE = r"E:\网站项目\smartimgkit"

def clean_html(html_str):
    """Remove all ad-related content from HTML string."""
    if not html_str:
        return html_str

    original = html_str

    # Remove <!-- AdSense --> comments
    html_str = re.sub(r'\n\s*<!--\s*AdSense\s*-->', '', html_str)

    # Remove <div class="ad-placeholder">Advertisement</div>
    html_str = re.sub(
        r'\n\s*<div\s+class="ad-placeholder"[^>]*>\s*Advertisement\s*</div>\s*',
        '',
        html_str
    )

    return html_str

def clean_file(filepath):
    """Clean a single JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tools = data.get('tools', [])
    if not tools:
        print(f"  ⏭️ {os.path.basename(filepath)} — no 'tools' field, skipping")
        return False

    changed = False
    cleaned_count = 0
    for tool in tools:
        if 'workspace_html' in tool:
            old = tool['workspace_html']
            new = clean_html(old)
            if old != new:
                tool['workspace_html'] = new
                changed = True
                cleaned_count += 1

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ {os.path.basename(filepath)} — cleaned {cleaned_count} tools, saved")
        return True
    else:
        print(f"  ⏭️ {os.path.basename(filepath)} — no changes needed")
        return False

# Find all language JSON files
files = glob.glob(os.path.join(BASE, '_tools_data_*.json'))
print(f"Found {len(files)} language JSON files\n")

total_cleaned = 0
for f in sorted(files):
    print(f"Processing {os.path.basename(f)}:")
    if clean_file(f):
        total_cleaned += 1

print(f"\nDone. Cleaned {total_cleaned} files.")
