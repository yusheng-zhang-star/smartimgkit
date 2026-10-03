#!/usr/bin/env python3
"""Inject Amazon affiliate recommendations into tools/, workflows/, and blog/."""
import os
import re

BASE = r"E:\网站项目\smartimgkit"
TAG = "sendafun20-20"

PRODUCTS = {
    # Printing
    "photo_paper":    ("B000TT7YRY", "Glossy Photo Paper",      "High-quality photo paper for printing your edited pictures."),
    "art_paper":      ("B0000721Z3", "Matte Inkjet Art Paper",  "Matte heavy-weight paper for art prints & graphic works."),
    "canon_selphy":   ("B0BF6T86WD", "Canon SELPHY CP1500",     "Wireless compact photo printer — print 4x6 photos from your phone."),
    # Photography gear
    "photo_tent":     ("B01GIL6EU4", "Amazon Basics Photo Tent", "25x30x25 foldable light box with LED — product photography for e-commerce sellers."),
    "reflector_43":   ("B002ZIMEMW", "NEEWER 43\" 5-in-1 Reflector", "Best-selling light reflector — 5 surfaces for portraits & product shots. 19k+ reviews."),
    "reflector_22":   ("B004ATGN4Y", "NEEWER 22\" 5-in-1 Reflector", "Compact travel-size reflector — Amazon's Choice for small-space photography."),
    "reflector_emart":("B07QQ9HMDL", "EMART 24\" 5-in-1 Reflector", "Budget-friendly reflector under $10 — great starter kit for beginners."),
    "reflector_etek": ("B00DIHSZCC", "Etekcity 24\" 5-in-1 Reflector", "Ultra-lightweight 8oz reflector — easy to carry on location shoots."),
    "tripod":         ("B0869BX44Y", "UBeesize 60\" Phone Tripod", "Adjustable tripod with phone mount — perfect for product videos and live streams."),
    # Storage
    "sandisk_ssd":    ("B08HN37XC1", "SanDisk Extreme SSD 1TB", "Rugged portable SSD — fast backup for photos, videos, and large files."),
    # Design
    "led_tracing":    ("B07H7FLJX1", "LED Light Tracing Pad",   "Light box for tracing sketches, inking, and artwork."),
    # Audio / Video
    "mic_mini":       ("B0CMJTSVRW", "Mini Mic Pro for iPhone", "#1 best-selling iPhone microphone — crystal-clear audio for videos and podcasts."),
    "mic_fifine":     ("B0BMFQP2ZZ", "FIFINE AM8 USB Microphone", "USB/XLR dynamic mic — great for podcasts, streaming, and voiceovers."),
    "mic_dji":        ("B0DDL8WGH5", "DJI Mic Mini (2-pack)", "Ultralight wireless lav mics with charging case — professional audio on the go."),
}

CATEGORIES = {
    "ai_photo":  ["photo_tent", "reflector_43", "canon_selphy", "tripod", "sandisk_ssd", "photo_paper"],
    "pdf":       ["canon_selphy", "sandisk_ssd", "art_paper", "photo_paper"],
    "dev":       ["sandisk_ssd", "mic_mini", "led_tracing", "photo_paper"],
    "video":     ["mic_dji", "mic_fifine", "tripod", "sandisk_ssd", "canon_selphy"],
    "design":    ["led_tracing", "reflector_22", "photo_paper", "canon_selphy", "reflector_emart"],
    "default":   ["photo_paper", "canon_selphy", "art_paper", "sandisk_ssd", "reflector_etek"],
}

HEADLINES = {
    "ai_photo":  ("Recommended Gear for Product Photography", "Everything an e-commerce seller needs for clean listing photos."),
    "pdf":       ("Recommended Tools for Document Work", "Gear that pairs perfectly with your PDF workflow."),
    "dev":       ("Recommended Gear for Creators & Developers", "Upgrade your workspace with these essentials."),
    "video":     ("Recommended Gear for Video & Podcasting", "Audio and tools that speed up your video workflow."),
    "design":    ("Recommended Gear for Creators", "Tools that pair perfectly with your design and social media work."),
    "default":   ("Recommended Tools for Image Projects", "Check these useful supplies to print and create your edited images."),
}

OLD_BLOCK_RE = re.compile(
    r'\n?\s*<section class="amazon-store-section">.*?</section>\n?',
    re.DOTALL
)

def categorize(filename, subdir):
    name = filename.replace(".html", "")

    if subdir == "workflows":
        if any(k in name for k in ["amazon","e-commerce","product","listing","photo-pack","studio","background"]):
            return "ai_photo"
        if any(k in name for k in ["social","instagram","pinterest","youtube","podcast","avatar","gif","screenshot","thumbnail","resume","cv","wallpaper"]):
            return "design"
        if "pdf" in name:
            return "pdf"
        return "ai_photo"

    if subdir == "blog":
        if any(k in name for k in ["amazon","product","ecommerce","e-commerce","background-remover","remove-background","upscaler","restoration","object-remover","inpaint"]):
            return "ai_photo"
        if any(k in name for k in ["pdf","document","scanner"]):
            return "pdf"
        if any(k in name for k in ["social","instagram","youtube","thumbnail","pinterest","design","meme","gif"]):
            return "design"
        if any(k in name for k in ["video","mp4","clip"]):
            return "video"
        return "default"

    # tools/ (original logic)
    if name.startswith("video-"):
        return "video"
    if name.startswith("pdf-") or name in ("word-to-pdf","excel-to-pdf","csv-to-pdf","epub-to-pdf","html-to-pdf","txt-to-pdf","image-to-pdf"):
        return "pdf"
    if name in ("json-formatter","regex-tester","base64","uuid-generator","password-generator","url-encoder","html-encoder","text-diff","text-sorter","text-find-replace","word-counter","case-converter"):
        return "dev"
    if name in ("background-remover","image-upscaler","beauty-editor","photo-restoration","object-remover","product-white-background","face-blur","image-enhancer"):
        return "ai_photo"
    if name in ("meme-generator","social-media-post","text-on-image","screenshot-to-image","image-border","image-shadow","image-merger","gif-editor","color-palette","image-filters","circle-crop","image-splitter","watermark","signature-maker","qr-code-generator","favicon-generator","ico-icon-generator"):
        return "design"
    return "default"

def build_section(product_keys, headline, subhead):
    cards = []
    for key in product_keys:
        asin, title, desc = PRODUCTS[key]
        cards.append(
            f'          <a class="amazon-card" href="https://www.amazon.com/dp/{asin}?tag={TAG}" target="_blank" rel="noopener sponsored nofollow">\n'
            f'            <h3>{title}</h3>\n'
            f'            <p>{desc}</p>\n'
            f'          </a>'
        )
    cards_html = "\n".join(cards)
    return (
        f'\n    <section class="amazon-store-section">\n'
        f'      <div class="container">\n'
        f'        <h2 style="font-size:1.3rem;font-weight:700;text-align:center;margin-bottom:6px;">{headline}</h2>\n'
        f'        <p style="text-align:center;color:var(--text-secondary);font-size:.9rem;margin-bottom:0;">{subhead}</p>\n'
        f'        <div class="amazon-store-grid">\n{cards_html}\n'
        f'        </div>\n'
        f'        <p class="amazon-disclaimer">As an Amazon Associate, we earn from qualifying purchases.</p>\n'
        f'      </div>\n'
        f'    </section>\n'
    )

def find_insert_point(html):
    faq_pos = html.find('<section class="faq-section">')
    if faq_pos != -1:
        return faq_pos
    rt_pos = html.find('<section class="related-tools">')
    if rt_pos != -1:
        return rt_pos
    main_end = html.rfind("</main>")
    if main_end != -1:
        section_end = html.rfind("</section>", 0, main_end)
        if section_end != -1:
            return section_end + len("</section>")
        return main_end
    art_end = html.rfind("</article>")
    if art_end != -1:
        return art_end
    return -1

def process_dir(subdir):
    dirpath = os.path.join(BASE, subdir)
    if not os.path.isdir(dirpath):
        print(f"  [SKIP] {subdir}: not found")
        return 0, 0

    updated = errors = 0
    for fname in sorted(os.listdir(dirpath)):
        if not fname.endswith(".html") or fname.startswith("_") or fname == "index.html":
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            print(f"  [SKIP] {subdir}/{fname}: {e}")
            errors += 1
            continue

        if "amazon-store-section" in html:
            html = OLD_BLOCK_RE.sub("\n", html)

        cat = categorize(fname, subdir)
        products = CATEGORIES[cat]
        headline, subhead = HEADLINES[cat]
        section = build_section(products, headline, subhead)

        insert_pos = find_insert_point(html)
        if insert_pos == -1:
            print(f"  [SKIP] {subdir}/{fname}: no insert point")
            errors += 1
            continue

        new_html = html[:insert_pos] + "\n" + section + html[insert_pos:]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        updated += 1
        print(f"  [OK] {subdir}/{fname} -> {cat}")

    return updated, errors

def main():
    total_updated = total_errors = 0
    for subdir in ["tools", "workflows", "blog"]:
        print(f"\n=== {subdir}/ ===")
        u, e = process_dir(subdir)
        total_updated += u
        total_errors += e

    print(f"\n=== DONE: {total_updated} updated, {total_errors} errors ===")

if __name__ == "__main__":
    main()
