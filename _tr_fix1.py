# -*- coding: utf-8 -*-
import io

path = r"e:\网站项目\smartimgkit\zh\blog\pdf-to-image-conversion-guide.html"
with io.open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Use straight double quotes " to match the file; Chinese output uses curly quotes
pairs = [
    # Section 1 p1
    ('<p>So I had a client send me a 47-page PDF deck last week. They wanted the slides "as images" for a quick Instagram carousel. Simple ask, right? Until I realized I\'d need an Adobe Acrobat subscription \u2014 which I don\'t pay for, and which costs like $20/month \u2014 just to save 47 pages as JPEGs. Or I could take screenshots one at a time. I tried that for about 4 minutes before I gave up and went looking for something better.</p>',
     '<p>上周有位客户发给我一份 47 页的 PDF 演示稿。他们想把幻灯片\u201c转成图片\u201d做一个 Instagram 轮播图。要求很简单，对吧？直到我意识到我得订阅 Adobe Acrobat——我没付费，而且它大概要 20 美元/月——就为了把 47 页存成 JPEG。或者我可以一张张截图。我试了大概 4 分钟就放弃了，开始找更好的办法。</p>'),
    # Screenshot p
    ('<p>This is what most people default to. Open the PDF, hit Print Screen, paste into an image editor, crop, save, repeat 47 times. For one page, fine. For a 50-page report, you\'re signing up for an hour of misery. Plus, screenshots are rasterized at your screen resolution \u2014 usually 1080p or 1440p. That means your "high-res" image is actually only 2-3 megapixels. Look, screenshots are fine in a pinch. But if you\'re doing this more than once, grab a proper tool.</p>',
     '<p>这是大多数人默认采用的办法。打开 PDF，按 Print Screen，粘贴到图像编辑器里，裁剪，保存，重复 47 次。一页还好。一份 50 页的报告，你就是在给自己签下一小时的苦差事。而且，截图是以你屏幕分辨率栅格化的——通常是 1080p 或 1440p。也就是说你那张\u201c高清\u201d图其实只有 2-3 百万像素。听着，应急用截图没问题。但如果你不止做一次，就找个正经工具吧。</p>'),
    # FAQ a3
    ('>Yes \u2014 modern tools let you select a page range. You can extract pages 1-5, or just page 12, without processing the whole document. The part I always forget: PDF page numbering is 1-based, not 0-based. So page "1" is the first page, not page "0." Yeah, that bit me on a project once.<',
     '>可以——现代工具让你选择页面范围。你可以只提取第 1-5 页，或只第 12 页，而不用处理整个文档。我老忘的一点：PDF 页码是从 1 开始的，不是从 0。所以\u201c1\u201d是第一页，不是\u201c0\u201d。嗯，这事在一个项目里坑过我一次。<'),
    # FAQ a4
    ('>PNG for sharp text and line art (lossless). JPEG for photos and pages with lots of color (smaller files). WebP for web use (best compression). For most "I just need to share this PDF page as an image" cases, PNG at 200 DPI works great. By the way, I tested 4 formats and found PNG was the best balance of quality and compatibility.<',
     '>PNG 适合锐利文字和线条图（无损）。JPEG 适合照片和颜色丰富的页面（文件更小）。WebP 适合网页用途（压缩最好）。对于大多数\u201c我只想把这页 PDF 分享成图片\u201d的情况，200 DPI 的 PNG 就很好。顺便说一句，我测过 4 种格式，发现 PNG 在质量和兼容性上是最佳平衡。<'),
]

count = 0
for old, new in pairs:
    n = html.count(old)
    if n == 0:
        print("WARN NOT FOUND:", repr(old[:70]))
    html = html.replace(old, new)
    count += n

with io.open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("Fix replacements applied:", count)
