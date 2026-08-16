# -*- coding: utf-8 -*-
import io, re
h = io.open(r'e:\网站项目\smartimgkit\zh\workflows\index.html', encoding='utf-8').read()
# 移除 script/style
h2 = re.sub(r'<script[^>]*>.*?</script>', '', h, flags=re.S)
h2 = re.sub(r'<style[^>]*>.*?</style>', '', h2, flags=re.S)
# 找所有 >text< 段落中的英文
segs = re.findall(r'>[^<>]{2,}<', h2)
brand = set('SmartImgKit Avatar Pipeline E-Commerce Pack Social Media Kit Product Image Optimizer Batch Watermark Protect Listing Image Suite JPEG PNG WebP SVG HEIC GIF AVIF PDF EXIF RAW Photoshop Shopify Amazon eBay Etsy Instagram Facebook Twitter LinkedIn YouTube Pinterest TikTok API CDN CPU RAM DevTools Network Photoshop Canva IMG Impact GIMP iOS Android Safari Chrome Firefox Edge WordPress Squarespace AirDrop Mac Windows Linux Blog FAQ CSS JS HTML JSON URL SEO SLA UI UX CSV KB MB MP API SDK Vimeo ID URL RTMP HLS'.split())
out = []
for s in segs:
    t = s[1:-1].strip()
    if not t:
        continue
    words = re.findall(r'[A-Za-z][A-Za-z\-]{2,}', t)
    bad = [w for w in words if w not in brand and not w.isdigit()]
    if bad:
        out.append((t[:100], bad))
print(f'残留英文段落数: {len(out)}')
for t, bad in out:
    print(f'  [{",".join(bad[:5])}] {t}')
