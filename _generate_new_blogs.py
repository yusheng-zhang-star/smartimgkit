#!/usr/bin/env python3
"""Generate 2 new SEO blogs for smartimgkit.com."""
import json
import os
import urllib.request
from pathlib import Path

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
BLOG_DIR = Path(r"E:\网站项目\smartimgkit\blog")
SITE_URL = "https://smartimgkit.com"

NEW_BLOGS = [
    {
        "slug": "remove-background-iphone-no-app-2026",
        "title": "How to Remove Background from iPhone Photos Without Any App (2026 Guide)",
        "meta": "Learn how to remove backgrounds from iPhone photos for free using built-in iOS tools. No third-party apps needed. Step-by-step tutorial for iOS 17, 18, and 26.",
        "keywords": "remove background iphone no app, ios remove photo background free, iphone cutout background, how to erase background on iphone photos",
        "topic": "How to remove backgrounds from iPhone photos using built-in iOS features (Visual Look Up, Markup), no third-party apps required. Covers iOS 17/18/26.",
        "template": "modern-clean"
    },
    {
        "slug": "free-background-remover-mac-no-download",
        "title": "Best Free Background Remover for Mac (No Download Required)",
        "meta": "Discover the best free background remover tools for Mac that work right in your browser. No downloads, no installations, no watermarks. Perfect for MacBook and iMac users.",
        "keywords": "free background remover mac, remove background on mac no download, browser based background remover mac, mac photo editor background free",
        "topic": "Best free browser-based background remover tools for Mac users. Compare solutions that work on Safari, Chrome, and Edge without any downloads.",
        "template": "tech-professional"
    },
]

def call_deepseek(prompt, max_tokens=2500):
    url = "https://api.deepseek.com/v1/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an expert tech blogger writing SEO-optimized articles about photo editing tools. Write in natural, conversational English that reads like a real human wrote it. Use clear headings, bullet points, and practical examples."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.75
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def build_blog_html(blog_info, content):
    slug = blog_info["slug"]
    title = blog_info["title"]
    meta = blog_info["meta"]
    keywords = blog_info["keywords"]
    template = blog_info["template"]
    
    # Simple HTML template
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<title>{title} | SmartImgKit</title>
<meta name="description" content="{meta}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{SITE_URL}/blog/{slug}">
<meta name="theme-color" content="#6366f1">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{SITE_URL}/blog/{slug}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="SmartImgKit">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{meta}",
  "author": {{"@type": "Organization", "name": "SmartImgKit"}},
  "publisher": {{"@type": "Organization", "name": "SmartImgKit", "logo": {{"@type": "ImageObject", "url": "{SITE_URL}/favicon.svg"}}}},
  "datePublished": "2026-09-21",
  "dateModified": "2026-09-21",
  "mainEntityOfPage": "{SITE_URL}/blog/{slug}"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_URL}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE_URL}/blog/"}},
    {{"@type": "ListItem", "position": 3, "name": "{title}"}}
  ]
}}
</script>
</head>
<body>
<header style="background:#1a1b2e;padding:16px 0;">
  <div style="max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:0 20px;">
    <a href="/" style="color:#fff;text-decoration:none;font-weight:700;font-size:1.2rem;">SmartImgKit</a>
    <nav style="display:flex;gap:20px;">
      <a href="/tools/remove-background" style="color:#ccc;text-decoration:none;">Remove BG</a>
      <a href="/blog/" style="color:#fff;text-decoration:none;font-weight:600;">Blog</a>
    </nav>
  </div>
</header>
<main style="max-width:800px;margin:40px auto;padding:0 20px;">
  <nav style="color:#666;font-size:0.9rem;margin-bottom:20px;">
    <a href="/" style="color:#6366f1;text-decoration:none;">Home</a> &rarr; <a href="/blog/" style="color:#6366f1;text-decoration:none;">Blog</a> &rarr; <span>{title[:50]}...</span>
  </nav>
  <article>
    <h1 style="font-size:2.2rem;line-height:1.2;margin-bottom:16px;color:#1a1b2e;">{title}</h1>
    <div style="color:#888;margin-bottom:30px;font-size:0.95rem;">
      Published: September 21, 2026 &middot; 8 min read
    </div>
    <div style="font-size:1.1rem;line-height:1.8;color:#333;">
{content}
    </div>
  </article>
  <div style="margin-top:50px;padding:30px;background:#f5f5fa;border-radius:12px;">
    <h3 style="margin-top:0;color:#6366f1;">Try Our Free Tool</h3>
    <p style="margin:12px 0;">Remove backgrounds from any image in seconds with our AI-powered tool. No signup, no watermark, completely free.</p>
    <a href="/tools/remove-background" style="display:inline-block;padding:12px 24px;background:#6366f1;color:#fff;text-decoration:none;border-radius:8px;font-weight:600;">Remove Background Now</a>
  </div>
</main>
<footer style="background:#1a1b2e;color:#888;padding:40px 0;margin-top:60px;">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px;text-align:center;">
    <p>&copy; 2026 SmartImgKit. All rights reserved.</p>
  </div>
</footer>
</body>
</html>'''
    return html

print("=" * 60)
print("Generating 2 new SEO blogs for smartimgkit.com")
print("=" * 60)

success = 0
for i, blog in enumerate(NEW_BLOGS):
    print(f"\n[{i+1}/2] Generating: {blog['slug']}")
    
    filepath = BLOG_DIR / f"{blog['slug']}.html"
    if filepath.exists():
        print(f"  SKIP (already exists)")
        continue
    
    prompt = f"""Write a comprehensive, SEO-optimized blog article in English about: {blog['topic']}

Requirements:
- At least 1200 words
- Natural, conversational tone (like a real tech blogger)
- Include practical step-by-step instructions
- Add 4-5 FAQ questions at the end
- Use subheadings (H2, H3) to structure content
- Optimize for the keyword: {blog['keywords']}
- Include 3 internal links to relevant SmartImgKit tools
- End with a clear conclusion
"""
    
    content = call_deepseek(prompt, max_tokens=2500)
    if not content:
        print(f"  FAILED (API error)")
        continue
    
    # Convert markdown to HTML
    lines = content.split('\n')
    html_content = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('## '):
            html_content += f"      <h2 style=\"font-size:1.5rem;margin-top:35px;margin-bottom:15px;color:#1a1b2e;\">{line[3:]}</h2>\n"
        elif line.startswith('### '):
            html_content += f"      <h3 style=\"font-size:1.2rem;margin-top:25px;margin-bottom:10px;color:#333;\">{line[4:]}</h3>\n"
        elif line.startswith('- '):
            html_content += f"      <p style=\"margin:8px 0;\">&bull; {line[2:]}</p>\n"
        else:
            html_content += f"      <p style=\"margin:16px 0;\">{line}</p>\n"
    
    html = build_blog_html(blog, html_content)
    filepath.write_text(html, encoding='utf-8')
    word_count = len(content.split())
    print(f"  OK ({word_count} words)")
    success += 1

print(f"\n{'=' * 60}")
print(f"Done: {success}/2 blogs generated")
