path = r'E:\网站项目\smartimgkit\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''            <span class="tool-tag">Privacy</span>
          </a>
          <div class="tools-category-header" id="cat-text"'''

new = '''            <span class="tool-tag">Privacy</span>
          </a>
          <a href="/tools/photo-map" class="tool-card" data-cat="utility">
            <div class="tool-icon">📍</div>
            <h3>Photo Location Map</h3>
            <p>Upload photos and see where they were taken on an interactive map. Extract GPS from EXIF, share and export GPX.</p>
            <span class="tool-tag">New · Map</span>
          </a>
          <a href="/tools/batch-exif-remover" class="tool-card" data-cat="utility">
            <div class="tool-icon">📦</div>
            <h3>Batch EXIF Remover</h3>
            <p>Remove EXIF metadata from multiple images at once. Preserve original format, download as ZIP. 100% private.</p>
            <span class="tool-tag">New · Privacy</span>
          </a>
          <div class="tools-category-header" id="cat-text"'''

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: Tools added to homepage')
else:
    print('ERROR: Pattern not found')
