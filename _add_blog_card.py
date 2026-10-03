with open('blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_card = '''          <a href="/blog/remove-bg-shutting-down-best-free-alternative" class="blog-card">
            <div class="blog-card-image">
              <span class="blog-card-icon">⚠️</span>
            </div>
            <div class="blog-card-content">
              <span class="blog-card-tag">News · Alternative</span>
              <h3>remove.bg Is Shutting Down Dec 1, 2026 — Best Free Alternative</h3>
              <p>remove.bg is closing! Find the best free alternative — unlimited background removal, no watermark, 100% private in-browser processing. Switch before your credits expire.</p>
              <span class="blog-card-date">Sep 10, 2026</span>
            </div>
          </a>
'''

marker = '<a href="/blog/photo-location-map-exif-gps-guide" class="blog-card">'
if marker in content:
    content = content.replace(marker, new_card + marker, 1)
    with open('blog/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Blog list updated successfully')
else:
    print('Marker not found!')
