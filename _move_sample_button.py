path = r'E:\网站项目\smartimgkit\tools\photo-map.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove button from dropzone
old_in_dropzone = '''          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
          <div style="margin-top:16px;">
            <button class="btn btn-secondary" onclick="loadSampleData(event)" style="background:var(--bg-tertiary); border:1px solid var(--border-color); color:var(--text-primary); padding:8px 16px; border-radius:8px; cursor:pointer;">✨ Try with sample data</button>
          </div>
        </div>'''

new_in_dropzone = '''          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
        </div>'''

content = content.replace(old_in_dropzone, new_in_dropzone)

# 2. Add button after stats bar, before map-layout
old_stats_end = '''    </div>

    <!-- Map + Sidebar -->'''

new_stats_end = '''    </div>
    
    <!-- Quick Actions -->
    <div style="text-align:center; margin-bottom:20px;">
      <button onclick="loadSampleData()" style="background:linear-gradient(135deg, var(--gradient-from), var(--gradient-to)); color:white; border:none; padding:12px 28px; border-radius:10px; font-size:1rem; font-weight:600; cursor:pointer; box-shadow:0 4px 12px rgba(99,102,241,0.3);">
        ✨ Try with sample data (4 cities + 1 no-GPS)
      </button>
      <span style="margin-left:12px; color:var(--text-muted); font-size:0.85rem;">No photos? Click to test instantly</span>
    </div>

    <!-- Map + Sidebar -->'''

content = content.replace(old_stats_end, new_stats_end)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: Button moved to visible position')
