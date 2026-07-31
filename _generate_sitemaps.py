#!/usr/bin/env python
"""Generate per-language sitemaps and sitemap index for smartimgkit.com."""

import os
import datetime

BASE = r'E:\网站项目\smartimgkit'
SITE = 'https://smartimgkit.com'
TODAY = datetime.date.today().isoformat()

LANGS = [
    {'code': 'en', 'dir': '', 'name': 'English'},
    {'code': 'es', 'dir': 'es', 'name': 'Spanish'},
    {'code': 'pt', 'dir': 'pt', 'name': 'Portuguese'},
    {'code': 'id', 'dir': 'id', 'name': 'Indonesian'},
    {'code': 'fr', 'dir': 'fr', 'name': 'French'},
    {'code': 'vi', 'dir': 'vi', 'name': 'Vietnamese'},
    {'code': 'ar', 'dir': 'ar', 'name': 'Arabic'},
]

# All tool slugs (from /tools/ directory)
TOOL_SLUGS = [
    'avif-support', 'background-remover', 'base64', 'bulk-processor',
    'case-converter', 'circle-crop', 'color-palette', 'compressor',
    'converter', 'cropper', 'face-blur', 'favicon-generator',
    'gif-editor', 'gif-splitter', 'heic-converter', 'heic-to-jpg',
    'html-encoder', 'ico-icon-generator', 'id-photo', 'image-adjust',
    'image-border', 'image-compare', 'image-compressor', 'image-enhancer',
    'image-exif-remover', 'image-filters', 'image-flip', 'image-grayscale',
    'image-merger', 'image-rotator', 'image-shadow', 'image-splitter',
    'image-to-pdf', 'image-upscaler', 'json-formatter', 'meme-generator',
    'metadata-viewer', 'ocr', 'password-generator', 'pdf-compress',
    'pdf-delete-pages', 'pdf-extract-pages', 'pdf-merge', 'pdf-rotate',
    'pdf-split', 'pdf-to-image', 'photo-restoration', 'print-resizer',
    'product-white-background', 'qr-code-generator', 'regex-tester',
    'resizer', 'screenshot-to-image', 'signature-maker', 'social-media-post',
    'svg-to-png', 'text-diff', 'text-find-replace', 'text-on-image',
    'text-sorter', 'url-encoder', 'uuid-generator', 'video-compressor',
    'video-crop', 'video-rotate', 'video-speed', 'video-to-frames',
    'video-to-gif', 'video-to-mp3', 'watermark', 'word-counter',
    'beauty-editor',
]

# Static pages (only in English root)
STATIC_PAGES = [
    'about', 'contact', 'privacy', 'terms', 'cookie-policy',
]

# Blog posts (only in English root)
BLOG_POSTS = [
    'image-compression-101', 'image-cropping-guide', 'image-format-guide',
    'image-upscaler-guide', 'image-watermark-guide', 'image-workflows-guide',
    'meme-creation-guide', 'heic-to-jpeg-conversion-guide',
    'pdf-to-image-conversion-guide', 'remove-background-complete-guide',
    'image-resizing-social-media-guide',
]


def url_entry(loc, priority, changefreq='weekly'):
    return f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>'''


def generate_lang_sitemap(lang_code, lang_dir):
    """Generate sitemap for a specific language."""
    prefix = f'/{lang_dir}' if lang_dir else ''
    urls = []

    # Homepage
    urls.append(url_entry(f'{SITE}{prefix}/', '1.0', 'weekly'))

    # Blog index
    urls.append(url_entry(f'{SITE}{prefix}/blog/', '0.7', 'weekly'))

    # Tools
    for slug in TOOL_SLUGS:
        urls.append(url_entry(f'{SITE}{prefix}/tools/{slug}', '0.9', 'monthly'))

    # Only English has static pages and blog posts
    if not lang_dir:  # English
        for page in STATIC_PAGES:
            urls.append(url_entry(f'{SITE}/{page}', '0.6', 'monthly'))
        for post in BLOG_POSTS:
            urls.append(url_entry(f'{SITE}/blog/{post}', '0.8', 'monthly'))

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
'''
    return xml


def generate_sitemap_index():
    """Generate sitemap index referencing all language sitemaps."""
    entries = []
    for lang in LANGS:
        sm_name = f'sitemap-{lang["code"]}.xml'
        entries.append(f'''  <sitemap>
    <loc>{SITE}/{sm_name}</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>''')

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</sitemapindex>
'''
    return xml


def main():
    # Generate per-language sitemaps
    total_urls = 0
    for lang in LANGS:
        xml = generate_lang_sitemap(lang['code'], lang['dir'])
        filename = f'sitemap-{lang["code"]}.xml'
        filepath = os.path.join(BASE, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml)
        count = xml.count('<url>')
        total_urls += count
        print(f'✅ {filename}: {count} URLs ({lang["name"]})')

    # Generate sitemap index
    index_xml = generate_sitemap_index()
    index_path = os.path.join(BASE, 'sitemap.xml')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_xml)
    print(f'\n✅ sitemap.xml (index with {len(LANGS)} language sitemaps)')
    print(f'\n📊 Total URLs across all sitemaps: {total_urls}')


if __name__ == '__main__':
    main()
