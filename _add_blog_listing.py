path = r'E:\网站项目\smartimgkit\blog\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        <div class="blog-grid">
                    <a href="/blog/ai-object-remover-lama-inpainting" class="blog-card">'''

new = '''        <div class="blog-grid">
                    <a href="/blog/photo-location-map-exif-gps-guide" class="blog-card">
            <div class="blog-card-image">
              <span class="blog-card-icon">📍</span>
            </div>
            <div class="blog-card-content">
              <span class="blog-card-tag">Tutorial · Privacy</span>
              <h3>How to Find Where a Photo Was Taken (And Remove GPS Data)</h3>
              <p>Learn how to extract GPS coordinates from photos, view them on an interactive map, and batch remove EXIF metadata to protect your privacy. Free tools included.</p>
              <span class="blog-card-date">Sep 10, 2026</span>
            </div>
          </a>
          <a href="/blog/ai-object-remover-lama-inpainting" class="blog-card">'''

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: Blog added to listing')
else:
    print('ERROR: Pattern not found')
