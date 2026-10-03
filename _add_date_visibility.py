#!/usr/bin/env python3
"""Add date-based visibility control to all 15 blogs and blog index.
Blogs before their publish date are hidden automatically via JavaScript."""
import os
import re

BLOG_DIR = r"E:\网站项目\smartimgkit\blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.html")

# Publish schedule: every 2 days starting from today (2026-09-10)
BLOG_SCHEDULE = [
    ("remove-bg-shutting-down-best-free-alternative", "2026-09-10", "Sep 10, 2026"),
    ("10-best-free-remove-bg-alternatives-2026", "2026-09-12", "Sep 12, 2026"),
    ("how-to-remove-background-without-remove-bg", "2026-09-14", "Sep 14, 2026"),
    ("remove-bg-credits-expiring-what-to-do", "2026-09-16", "Sep 16, 2026"),
    ("best-background-remover-for-product-photos-ecommerce", "2026-09-18", "Sep 18, 2026"),
    ("how-to-remove-background-from-hair-ai-tools", "2026-09-20", "Sep 20, 2026"),
    ("free-background-remover-no-watermark-top-tools", "2026-09-22", "Sep 22, 2026"),
    ("remove-bg-vs-canva-which-is-better", "2026-09-24", "Sep 24, 2026"),
    ("batch-remove-backgrounds-from-multiple-images-free", "2026-09-26", "Sep 26, 2026"),
    ("best-background-remover-for-photographers-portrait-wedding", "2026-09-28", "Sep 28, 2026"),
    ("in-browser-ai-private-local-image-processing-future", "2026-09-30", "Sep 30, 2026"),
    ("how-to-make-png-transparent-background-free", "2026-10-02", "Oct 2, 2026"),
    ("remove-bg-api-alternatives-free-paid-options", "2026-10-04", "Oct 4, 2026"),
    ("best-background-remover-for-social-media-instagram-tiktok", "2026-10-06", "Oct 6, 2026"),
    ("complete-guide-ai-background-removal-2026", "2026-10-08", "Oct 8, 2026"),
]

# JavaScript to inject into each blog detail page
BLOG_JS = """
<script>
(function() {
  var publishDate = "PUBLISH_DATE";
  var now = new Date();
  var pub = new Date(publishDate + "T00:00:00");
  if (now < pub) {
    document.body.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;font-family:system-ui,sans-serif;background:#f9fafb;color:#1f2937;text-align:center;padding:40px;"><div style="font-size:4rem;margin-bottom:20px;">📅</div><h1 style="font-size:1.8rem;margin-bottom:12px;">Coming Soon</h1><p style="color:#6b7280;font-size:1.1rem;max-width:400px;">This article will be published on <strong style="color:#6366f1;">' + publishDate + '</strong>. Please check back soon!</p><a href="/blog/" style="margin-top:24px;display:inline-block;padding:12px 28px;background:#6366f1;color:white;text-decoration:none;border-radius:8px;font-weight:600;">← Back to Blog</a></div>';
    document.title = "Coming Soon - SmartImgKit Blog";
  }
})();
</script>
"""

# Step 1: Add publish date JS to each blog detail page
for slug, pub_date, display_date in BLOG_SCHEDULE:
    path = os.path.join(BLOG_DIR, f"{slug}.html")
    if not os.path.exists(path):
        print(f"  ⚠️  Not found: {slug}.html")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Skip if already has the script
    if 'PUBLISH_DATE' in content or 'Coming Soon' in content:
        print(f"  ⏭️  Already has date script: {slug}")
        continue
    # Inject JS before </body>
    js = BLOG_JS.replace("PUBLISH_DATE", pub_date)
    content = content.replace("</body>", js + "\n</body>")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Added date control: {slug} (publishes {pub_date})")

print("\n--- Updating blog index cards ---")

# Step 2: Update blog index - add data-publish-date to each card and add filtering JS
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Add data-publish-date to each blog card link
for slug, pub_date, display_date in BLOG_SCHEDULE:
    # Find the card link for this blog and add data attribute
    old_link = f'href="/blog/{slug}" class="blog-card"'
    new_link = f'href="/blog/{slug}" class="blog-card" data-publish-date="{pub_date}"'
    if old_link in index_content:
        index_content = index_content.replace(old_link, new_link)
        print(f"  ✓ Added data-publish-date to card: {slug}")
    else:
        print(f"  ⚠️  Card not found: {slug}")

# Add filtering JavaScript before </body> in index
FILTER_JS = """
<script>
(function() {
  var now = new Date();
  var cards = document.querySelectorAll('.blog-card[data-publish-date]');
  var hiddenCount = 0;
  cards.forEach(function(card) {
    var pubDate = new Date(card.getAttribute('data-publish-date') + 'T00:00:00');
    if (now < pubDate) {
      card.style.display = 'none';
      hiddenCount++;
    }
  });
  if (hiddenCount > 0) {
    var grid = document.querySelector('.blog-grid');
    if (grid) {
      var notice = document.createElement('div');
      notice.style.cssText = 'grid-column:1/-1;text-align:center;padding:20px;color:#6b7280;font-size:0.9rem;';
      notice.innerHTML = '📅 ' + hiddenCount + ' more articles scheduled for the coming weeks — check back every 2 days!';
      grid.appendChild(notice);
    }
  }
})();
</script>
"""

if 'data-publish-date' in index_content and 'blog-card-filter' not in index_content:
    index_content = index_content.replace("</body>", FILTER_JS + "\n</body>")
    print("\n  ✓ Added filtering JavaScript to blog index")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("\n✅ Done! All 15 blogs now have date-based visibility control.")
print(f"   Publish schedule: every 2 days from 2026-09-10 to 2026-10-08")
