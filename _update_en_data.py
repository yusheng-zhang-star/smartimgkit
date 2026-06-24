#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_update_en_data.py — 给 _tools_data.json 添加 lang 级字段

从当前 template 跟 generated page 提取字段值，确保生成结果一字不差。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, '_tools_data.json')

# ── English language-level fields (exact match with generated HTML) ──
EN_LANG_FIELDS = {
    "lang": "en",
    "nav_html": '<nav class="main-nav"><a href="/">Home</a><a href="/tools/background-remover.html">Tools</a><a href="/workflows/">Workflows</a><a href="/blog/">Blog</a><a href="/about.html">About</a><a href="/contact.html">Contact</a></nav>',
    "lang_switcher_html": '''<div class="lang-switcher" style="position:relative;">
          <button class="lang-btn" aria-label="Switch language">🇬🇧 EN</button>
          <div class="lang-dropdown" style="display:none!important;position:absolute!important;top:100%;right:0;z-index:100;min-width:160px;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:4px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,0.15);">
            <a href="/es/" hreflang="es" lang="es">🇪🇸 Español</a>
            <a href="/pt/" hreflang="pt" lang="pt">🇧🇷 Português</a>
            <a href="/id/" hreflang="id" lang="id">🇮🇩 Bahasa Indonesia</a>
          </div>
        </div>''',
    "footer_html": '''  <!-- Footer: exact match image-rotator compact format -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand"><a href="/" class="logo"><span class="logo-icon">🎨</span><span class="logo-text">SmartImgKit</span></a><p>Free AI-powered image tools that respect your privacy.</p></div>
        <div class="footer-links"><h4>Tools</h4><a href="/tools/background-remover.html">Background Remover</a><a href="/tools/compressor.html">Compressor</a><a href="/tools/converter.html">Converter</a><a href="/tools/resizer.html">Resizer</a>
          <a href="/tools/gif-editor.html">GIF Editor</a>
          <a href="/tools/pdf-to-image.html">PDF to Image</a>
        </div>
        <div class="footer-links"><h4>More Tools</h4><a href="/tools/cropper.html">Cropper</a><a href="/tools/watermark.html">Watermark</a><a href="/tools/image-merger.html">Image Merger</a><a href="/tools/screenshot-to-image.html">Screenshot to Image</a><a href="/tools/image-filters.html">Image Filters</a><a href="/tools/svg-to-png.html">SVG to PNG</a><a href="/tools/image-compare.html">Image Compare</a><a href="/tools/print-resizer.html">Print-Ready Resizer</a><a href="/tools/meme-generator.html">Meme Generator</a>          <a href="/tools/face-blur.html">Face Blur</a>
          <a href="/tools/heic-converter.html">HEIC Converter</a>
          <a href="/tools/metadata-viewer.html">Metadata Viewer</a>
          <a href="/tools/avif-support.html">AVIF Support</a>
          <a href="/tools/image-adjust.html">Image Adjustment</a>
          <a href="/tools/image-border.html">Image Border</a>
          <a href="/tools/image-flip.html">Image Flip</a>
          <a href="/tools/image-grayscale.html">Image Grayscale</a>
          <a href="/tools/image-shadow.html">Image Shadow</a>
          <a href="/tools/image-splitter.html">Image Splitter</a>
          <a href="/tools/image-exif-remover.html">EXIF Remover</a><a href="/tools/circle-crop.html">Circle Crop</a><a href="/tools/favicon-generator.html">Favicon Generator</a><a href="/tools/ocr.html">OCR Text</a><a href="/tools/bulk-processor.html">Bulk Processor</a><a href="/tools/image-to-pdf.html">Image to PDF</a>          <a href="/tools/id-photo.html">ID Photo Maker</a>
          <a href="/tools/product-white-background.html">Product White BG</a>
          <a href="/tools/social-media-post.html">Social Media Post</a>
          <a href="/tools/photo-restoration.html">Photo Restoration</a><a href="/tools/image-enhancer.html">Image Enhancer</a>
        </div>
        <div class="footer-links"><h4>Legal</h4><a href="/privacy.html">Privacy Policy</a><a href="/terms.html">Terms of Service</a><a href="/cookie-policy.html">Cookie Policy</a>
        </div>
      </div>
      <div class="footer-bottom"><p>&copy; 2026 SmartImgKit. All rights reserved. | <a href="https://comprimefotos.com/" style="color: var(--accent); font-weight: 500;">Español: ComprimeFotos — Comprimir Imágenes Online</a></p></div>
    </div>
  </footer>''',
    "tools_url": "/tools",
    "breadcrumb_home": "Home",
    "breadcrumb_tools": "Tools",
    "breadcrumb_tools_url": "/",
}


def update():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # merge lang fields at top level (don't overwrite tools array)
    for k, v in EN_LANG_FIELDS.items():
        data[k] = v

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f'Updated {DATA_FILE} with {len(EN_LANG_FIELDS)} language-level fields.')
    print(f'Total tools: {len(data.get("tools", []))}')


if __name__ == '__main__':
    update()
