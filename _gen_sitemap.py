#!/usr/bin/env python3
"""Generate complete sitemap.xml for SmartImgKit with all 7 languages."""

import json
import os
from datetime import date, datetime

TODAY = date.today().isoformat()  # 2026-06-25
LANGUAGES = ['es', 'pt', 'id', 'fr', 'vi', 'ar']
BASE = 'https://smartimgkit.com'

# Load tool slugs
with open(os.path.join(os.path.dirname(__file__), '_tools_data.json'), encoding='utf-8') as f:
    data = json.load(f)
tool_slugs = sorted(t['slug'] for t in data['tools'])

# Workflows
workflows = [
    'avatar-pipeline', 'ai-background-studio', 'batch-watermark-protect',
    'e-commerce-pack', 'listing-image-suite', 'product-image-optimizer', 'social-media-kit'
]

# Blog posts (from filesystem)
blog_posts = [
    'heic-to-jpeg-conversion-guide', 'image-compression-101', 'image-cropping-guide',
    'image-format-guide', 'image-resizing-social-media-guide', 'image-upscaler-guide',
    'image-watermark-guide', 'image-workflows-guide', 'meme-creation-guide',
    'pdf-to-image-conversion-guide', 'remove-background-complete-guide'
]

def url_entry(loc, priority='0.8', changefreq='monthly', lastmod=TODAY):
    return f"""  <url>
    <loc>{BASE}{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

entries = []

# ── English homepage ──
entries.append(url_entry('/', priority='1.0', changefreq='weekly'))

# ── English tools (45) ──
for slug in tool_slugs:
    entries.append(url_entry(f'/tools/{slug}', priority='0.9'))

# ── 6 languages × 45 tools = 270 ──
for lang in LANGUAGES:
    for slug in tool_slugs:
        entries.append(url_entry(f'/{lang}/tools/{slug}', priority='0.8'))

# ── Workflows ──
entries.append(url_entry('/workflows/', priority='0.9', changefreq='weekly'))
for wf in workflows:
    entries.append(url_entry(f'/workflows/{wf}.html', priority='0.8'))

# ── Blog (English) ──
entries.append(url_entry('/blog/', priority='0.8', changefreq='weekly'))
for bp in blog_posts:
    entries.append(url_entry(f'/blog/{bp}', priority='0.8'))

# ── Blog (6 languages) ──
for lang in LANGUAGES:
    entries.append(url_entry(f'/{lang}/blog/', priority='0.7', changefreq='weekly'))

# ── Static pages ──
entries.append(url_entry('/about', priority='0.7'))
entries.append(url_entry('/contact', priority='0.6'))
entries.append(url_entry('/privacy', priority='0.3', changefreq='yearly'))
entries.append(url_entry('/terms', priority='0.3', changefreq='yearly'))
entries.append(url_entry('/cookie-policy', priority='0.3', changefreq='yearly'))

# ── Assemble ──
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += '\n'.join(entries)
sitemap += '\n</urlset>\n'

sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f'✓ Sitemap written: {sitemap_path}')
print(f'  Total URLs: {len(entries)}')
print(f'  English tools: {len(tool_slugs)}')
print(f'  Lang tools: {len(LANGUAGES)} x {len(tool_slugs)} = {len(LANGUAGES) * len(tool_slugs)}')
print(f'  Workflows: {1 + len(workflows)} (list + pages)')
print(f'  Blog: {1 + len(blog_posts)} English + {len(LANGUAGES)} lang indexes')
print(f'  Static: 5 (about, contact, privacy, terms, cookie-policy)')
