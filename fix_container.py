"""Fix premature container closing in static HTML tool pages.

Pattern to fix:
      </div>              ← closes tool-workspace
      </div>              ← closes container (PREMATURE - remove)
<section class="how-to-section">

Or with ad-placeholder:
      </div>              ← closes tool-workspace  
      </div>              ← closes container (PREMATURE - remove)
      <div class="ad-placeholder">Advertisement</div>  ← remove
      </div>              ← remove
<section class="how-to-section">
"""
import os, glob, re

TOOLS_DIR = r'E:\网站项目\smartimgkit\tools'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: tool-workspace </div> followed immediately by container </div>,
    # then how-to-section. Match within the context of tool-workspace close.
    # The pattern is: two </div> lines (with optional whitespace/comments/ad between),
    # directly before <section class="how-to-section">
    
    # Pattern: </div>\n...whitespace...\n</div>\n...<section class="how-to-section">
    # The first </div> closes tool-workspace, second closes container.
    # We want to remove the SECOND </div> and any ad-placeholder in between.
    
    # More flexible: match the region from last </div> before how-to-section up to how-to-section
    pattern = re.compile(
        r'(</div>)\s*'           # tool-workspace close
        r'('                     # group 2: stuff to remove
        r'\s*</div>\s*'          # premature container close
        r'(?:<!--[^>]*-->\s*)*'  # optional comments like <!-- AdSense -->
        r'(?:<div[^>]*ad-placeholder[^>]*>.*?</div>\s*)?'  # optional ad block
        r')'
        r'(<section\s[^>]*class="[^"]*how-to-section[^"]*"[^>]*>)',  # how-to-section start
        re.DOTALL
    )
    
    match = pattern.search(content)
    if not match:
        return False
    
    # Verify we're in the right context: check if there's tool-workspace above
    before = content[:match.start()]
    if 'class="tool-workspace"' not in before:
        return False
    
    # Rebuild: keep tool-workspace close (group 1), remove premature stuff (group 2),
    # keep how-to-section (group 3)
    new_content = content[:match.start()] + match.group(1) + '\n' + match.group(3)
    remaining = content[match.end():]
    
    # Need to close the container now. Find </main> and add a </div> before it.
    # Actually no - the container is still open! We need to keep the container open
    # until after related-tools. Let me check if there's already a closing </div>
    # before </main>
    
    # Check if there's a </div> just before </main>
    main_match = re.search(r'\n(\s*)</main>', remaining)
    if main_match:
        main_indent = main_match.group(1)
        # Check if the line before </main> is already a </div>
        before_main = remaining[:main_match.start()].rstrip()
        if before_main.endswith('</div>'):
            # Already has closing div - good
            pass
        else:
            # Need to add container close
            new_content += remaining[:main_match.start()]
            new_content += '\n' + main_indent + '    </div>'  # one level deeper
            new_content += remaining[main_match.start():]
            remaining = ''  # consumed
    
    if remaining:
        new_content += remaining
    
    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Count changes
        removed_lines = original.count('\n') - new_content.count('\n')
        print(f"  Fixed: {os.path.basename(filepath)}")
        return True
    
    return False

def main():
    files = sorted([f for f in glob.glob(os.path.join(TOOLS_DIR, '*.html'))])
    
    fixed = 0
    for fp in files:
        if fix_file(fp):
            fixed += 1
    
    print(f"\nFixed {fixed} files total.")

if __name__ == '__main__':
    main()
