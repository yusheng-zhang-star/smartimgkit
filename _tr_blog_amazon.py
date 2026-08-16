# -*- coding: utf-8 -*-
"""Full translation for zh/blog/amazon-product-image-requirements-guide.html"""
import os, re

F = r'e:\网站项目\smartimgkit\zh\blog\amazon-product-image-requirements-guide.html'
h = open(F, encoding='utf-8').read()

def sub(pattern, repl, s=None, flags=0):
    global h
    h = re.sub(pattern, repl, h, count=1, flags=flags) if s is None else re.sub(pattern, repl, h, count=s, flags=flags)

# --- head ---
sub(r'(<title>)[^<]*(</title>)', r'\1Amazon 商品图片要求：无需 Photoshop 的纯白背景 | SmartImgKit\2')
sub(r'(<meta name="description" content=")[^"]*(")',
    r'\1无需 Photoshop 即可满足 2026 年 Amazon 商品图片要求。免费浏览器端工具，可添加纯白背景、调整尺寸并压缩商品照片。\2')
h = h.replace('<span>Amazon Product Image Guide</span>', '<span>Amazon 商品图片指南</span>')
h = h.replace('<span class="blog-card-tag">E-Commerce</span>', '<span class="blog-card-tag">电商</span>')
sub(r'(<h1>)[^<]*(</h1>)', r'\1Amazon 商品图片要求：无需 Photoshop 的纯白背景\2')
sub(r'(class="blog-post-subtitle">)[^<]*(</p>)',
    r'\1Amazon 因为背景不是纯白而拒收了我的商品。我没有 Photoshop。这是我在浏览器中批量修复商品照片的免费工作流——无需软件、无需上传、无需订阅。\2')
# quick answer body
h = h.replace(
    "<p style=\"margin:0;\">Amazon's main product image needs a pure white background (RGB 255,255,255), at least 1000×1000 pixels, and JPEG/TIFF/PNG format. You don't need Photoshop — <a href=\"/zh/tools/product-white-background\">SmartImgKit's Product White Background tool</a> removes the old background and replaces it with pure white, right in your browser.</p>",
    "<p style=\"margin:0;\">Amazon 的主商品图需要纯白背景（RGB 255,255,255）、至少 1000×1000 像素，以及 JPEG/TIFF/PNG 格式。您不需要 Photoshop——<a href=\"/zh/tools/product-white-background\">SmartImgKit 的商品白底工具</a>会移除旧背景并替换为纯白，全部在浏览器中完成。</p>")
# TOC heading
h = h.replace('<h3>Table of Contents</h3>', '<h3>目录</h3>')
TOC = [
    ('The Rejection Email That Started This', '一切始于那封拒收邮件'),
    ("Amazon's Image Rules (The Short Version)", 'Amazon 图片规则（简版）'),
    ('White Background Without Photoshop', '无需 Photoshop 的纯白背景'),
    ('Batch Processing: 50 Photos at Once', '批量处理：一次 50 张照片'),
    ('Platform-by-Platform Size Cheat Sheet', '各平台尺寸速查表'),
    ("Compression: Don't Let Amazon Compress For You", '压缩：别让 Amazon 替你压缩'),
]
for en, zh in TOC:
    h = h.replace('>' + en + '</a>', '>' + zh + '</a>')
# TL;DR
h = h.replace('<p style="margin:0 0 8px 0;font-weight:700;font-size:15px;">TL;DR</p>',
              '<p style="margin:0 0 8px 0;font-weight:700;font-size:15px;">太长不看</p>')
h = h.replace(
    "<p style=\"margin:0;\">Amazon requires a pure white background on your main listing image. Most sellers either pay for Photoshop or outsource to a photo editor. This guide shows how to do it free, in your browser, with the <a href=\"/zh/tools/product-white-background\">Product White Background Maker</a> for single images and the <a href=\"/zh/workflows/e-commerce-pack\">E-Commerce Pack</a> workflow for batch processing. No upload, no signup, no software install.</p>",
    "<p style=\"margin:0;\">Amazon 要求主商品图为纯白背景。大多数卖家要么付费购买 Photoshop，要么外包给修图师。本指南教你如何免费在浏览器中完成——单张图片用<a href=\"/zh/tools/product-white-background\">商品白底制作工具</a>，批量处理用<a href=\"/zh/workflows/e-commerce-pack\">电商图片包</a>工作流。无需上传、无需注册、无需安装软件。</p>")

# h2 headings
H2 = [
    ('1. The Rejection Email That Started This', '1. 一切始于那封拒收邮件'),
    ("2. Amazon's Image Rules (The Short Version)", '2. Amazon 图片规则（简版）'),
    ('3. White Background Without Photoshop', '3. 无需 Photoshop 的纯白背景'),
    ('4. Batch Processing: 50 Photos at Once', '4. 批量处理：一次 50 张照片'),
    ('5. Platform-by-Platform Size Cheat Sheet', '5. 各平台尺寸速查表'),
    ("6. Compression: Don't Let Amazon Compress For You", '6. 压缩：别让 Amazon 替你压缩'),
    ('7. FAQ', '7. 常见问题'),
]
for en, zh in H2:
    h = h.replace('>' + en + '</h2>', '>' + zh + '</h2>')

# table headers
h = h.replace('<th>Requirement</th><th>Spec</th>', '<th>要求</th><th>规格</th>')
# table rows
ROWS = [
    ('<td>Background color</td><td>Pure white (RGB 255, 255, 255)</td>', '<td>背景颜色</td><td>纯白（RGB 255, 255, 255）</td>'),
    ('<td>Minimum dimensions</td><td>1000 × 1000 pixels (for zoom)</td>', '<td>最小尺寸</td><td>1000 × 1000 像素（用于缩放）</td>'),
    ('<td>Recommended dimensions</td><td>1600 × 1600 pixels or larger</td>', '<td>推荐尺寸</td><td>1600 × 1600 像素或更大</td>'),
    ('<td>Maximum dimensions</td><td>10,000 × 10,000 pixels</td>', '<td>最大尺寸</td><td>10,000 × 10,000 像素</td>'),
    ('<td>File format</td><td>JPEG, TIFF, PNG, or GIF</td>', '<td>文件格式</td><td>JPEG、TIFF、PNG 或 GIF</td>'),
    ('<td>File size</td><td>Under 10 MB (practical: under 2 MB)</td>', '<td>文件大小</td><td>10 MB 以下（实际：2 MB 以下）</td>'),
    ('<td>Product fill</td><td>Product should fill 85% of the frame</td>', '<td>商品填充</td><td>商品应占画面 85%</td>'),
    ('<td>No text, logos, or watermarks</td><td>On the main image only</td>', '<td>无文字、Logo 或水印</td><td>仅限主图</td>'),
    ('<th>Platform</th><th>Min Size</th><th>Recommended</th><th>Background</th>',
     '<th>平台</th><th>最小尺寸</th><th>推荐</th><th>背景</th>'),
    ('<tr><td>Amazon</td><td>1000 × 1000</td><td>1600 × 1600</td><td>Pure white (main image)</td></tr>',
     '<tr><td>Amazon</td><td>1000 × 1000</td><td>1600 × 1600</td><td>纯白（主图）</td></tr>'),
    ('<tr><td>Shopify</td><td>2048 × 2048</td><td>2048 × 2048</td><td>Any (white recommended)</td></tr>',
     '<tr><td>Shopify</td><td>2048 × 2048</td><td>2048 × 2048</td><td>任意（推荐白色）</td></tr>'),
    ('<tr><td>eBay</td><td>500 × 500</td><td>1600 × 1600</td><td>Any</td></tr>',
     '<tr><td>eBay</td><td>500 × 500</td><td>1600 × 1600</td><td>任意</td></tr>'),
    ('<tr><td>Etsy</td><td>1000 × 1000</td><td>2000 × 2000</td><td>Any</td></tr>',
     '<tr><td>Etsy</td><td>1000 × 1000</td><td>2000 × 2000</td><td>任意</td></tr>'),
    ('<tr><td>Walmart</td><td>500 × 500</td><td>2000 × 2000</td><td>Pure white (main image)</td></tr>',
     '<tr><td>Walmart</td><td>500 × 500</td><td>2000 × 2000</td><td>纯白（主图）</td></tr>'),
]
for en, zh in ROWS:
    h = h.replace(en, zh)

# paragraphs (long) - map by exact text node
PARAS = [
    ("Last March, I uploaded 24 product photos to Amazon Seller Central for a client who sold handmade soap. Twenty-three of them went through fine. The twenty-fourth — the main listing image — got bounced back with a generic error: \"Image does not meet Amazon's product image requirements.\"",
     "去年三月，我为一位售卖手工皂的客户向 Amazon 卖家中心上传了 24 张商品照片。其中 23 张顺利通过。第 24 张——主商品图——被退回，并附有一条笼统的错误提示：“图片不符合 Amazon 的商品图片要求。”"),
    ("I stared at it. The photo looked fine. Good lighting, sharp focus, the soap centered in the frame. What was wrong?",
     "我盯着它看。照片看起来没问题。光线良好、对焦清晰、香皂居中。哪里出了错？"),
    ("The background. It was off-white. Not pure white. The kind of white that looks white to a human eye but reads as RGB 252, 248, 245 to Amazon's automated checker. Too warm. Rejected.",
     "是背景。它是偏白的，不是纯白。那种在人眼看来是白色、但 Amazon 自动检测器读作 RGB 252, 248, 245 的白。太暖了。被拒收。"),
    ("The fix was simple in theory: replace the background with pure white (RGB 255, 255, 255). The problem was I didn't own Photoshop, and my client wasn't about to pay $23/month for a Creative Cloud subscription to fix one photo. GIMP could do it, but the learning curve for background replacement is steep if you've never done it.",
     "理论上修复很简单：把背景换成纯白（RGB 255, 255, 255）。问题是我没有 Photoshop，而我的客户不会为了修一张照片每月付 23 美元订阅 Creative Cloud。GIMP 可以做到，但如果你从未做过背景替换，学习曲线相当陡峭。"),
    ("That's when I started building the <a href=\"/zh/tools/product-white-background\">Product White Background Maker</a>. The idea was dead simple: upload a product photo, the tool removes whatever background is there, drops in pure white, and gives you a compliant image. All in the browser, no upload to a server.",
     "就在那时我开始开发<a href=\"/zh/tools/product-white-background\">商品白底制作工具</a>。思路非常简单：上传一张商品照片，工具移除原有背景，填入纯白，给你一张合规的图片。全部在浏览器中完成，不上传到服务器。"),
    ("Amazon's <a href=\"/zh/workflows/e-commerce-pack\">Seller Central image requirements</a> are public, but they're buried in a 4,000-word help page. Here's what actually matters for the main listing image:",
     "Amazon 的<a href=\"/zh/workflows/e-commerce-pack\">卖家中心图片要求</a>是公开的，但埋在一份 4000 字的帮助页面里。以下是对主商品图真正重要的内容："),
    ("The pure white background rule is the one that trips people up the most. Your camera's auto white balance will rarely produce true 255,255,255 white. Even a lightbox can produce a slightly gray or warm background depending on the bulbs. And Amazon's checker is strict — it samples the corner pixels and if they're not pure white, the image gets rejected.",
     "纯白背景规则是最容易让人栽跟头的。你的相机自动白平衡很少能产生真正的 255,255,255 白。即使是灯箱，根据灯泡不同也可能产生略灰或偏暖的背景。而 Amazon 的检测器很严格——它采样角落像素，如果不是纯白，图片就会被拒。"),
    ("The 1000×1000 minimum is the second most common issue. Phone cameras shoot at 4000×3000 or larger, but if you crop tightly or downsize for web, you might end up under 1000 pixels on one side. No zoom for you.",
     "1000×1000 的最小尺寸是第二常见的问题。手机摄像头拍摄尺寸为 4000×3000 或更大，但如果你紧密裁剪或为网页缩小，可能某一边会低于 1000 像素。那样就无法缩放查看。"),
    ("Here's how to get a pure white background without owning any paid software:",
     "以下是在不拥有任何付费软件的情况下获得纯白背景的方法："),
    ("The whole process takes about 5 seconds per image. For a single product, it's faster than opening Photoshop.",
     "整个过程每张图片约 5 秒。对于单个商品，比打开 Photoshop 还快。"),
    ("Now, one thing I should be honest about: the AI background removal isn't perfect for everything. Products with hair-like textures, fur, or very thin stems can have rough edges. For those, you might need to do manual cleanup. But for 90% of e-commerce products — packaged goods, electronics, cosmetics, kitchenware — it works well enough that you won't need to touch it.",
     "有一点我要坦诚：AI 去背景并非对所有东西都完美。带有毛发状纹理、皮毛或非常细的茎的商品边缘可能粗糙。对这些，你可能需要手动修整。但对于 90% 的电商商品——包装食品、电子产品、化妆品、厨具——效果已经足够好，你无需再处理。"),
    ("If you have a catalog of 30+ products, doing them one at a time is tedious. That's where the <a href=\"/zh/workflows/e-commerce-pack\">E-Commerce Pack workflow</a> comes in.",
     "如果你有 30+ 个商品的目录，逐个处理会很繁琐。这时就该用<a href=\"/zh/workflows/e-commerce-pack\">电商图片包工作流</a>了。"),
    ("The workflow chains three steps together: resize → compress → (optional) watermark. You drop in up to 50 images, pick a platform preset (Amazon 1000×1000, Shopify 2048×2048, eBay 1600×1600, Etsy 2000×2000), and click run. Thirty seconds later, you download a ZIP with all your images processed.",
     "该工作流串联三个步骤：缩放 → 压缩 →（可选）水印。你最多放入 50 张图片，选择平台预设（Amazon 1000×1000、Shopify 2048×2048、eBay 1600×1600、Etsy 2000×2000），然后点击运行。三十秒后，你就能下载一个包含所有已处理图片的 ZIP。"),
    ("Here's the thing though — the E-Commerce Pack handles resize and compress, but it doesn't do the white background swap. So the ideal pipeline for a batch of Amazon products is:",
     "但要注意——电商图片包处理缩放和压缩，但不做白底替换。所以一批 Amazon 商品的理想流水线是："),
    ("For 30 products, that's about 5 minutes of white-background work plus 30 seconds of batch processing. Compare that to doing it manually in Photoshop: 5-10 minutes per image for background removal, resize, and export. You do the math.",
     "对于 30 个商品，大约 5 分钟的白底处理加上 30 秒的批量处理。相比之下在 Photoshop 中手动操作：每张图片去背景、缩放、导出需要 5-10 分钟。你自己算算。"),
    ("If you sell on multiple platforms, the size requirements differ. Here's a quick reference:",
     "如果你在多个平台销售，尺寸要求各不相同。以下是快速参考："),
    ("If you sell on multiple channels, the <a href=\"/zh/workflows/listing-image-suite\">Listing Image Suite</a> workflow generates all four platform sizes from a single upload. It runs the resize-compress chain four times in parallel and gives you four ZIPs. Saves about 30 minutes per product if you're listing everywhere.",
     "如果你在多个渠道销售，<a href=\"/zh/workflows/listing-image-suite\">商品图片套件</a>工作流可从一次上传生成全部四个平台的尺寸。它并行运行四次缩放-压缩链，给你四个 ZIP。如果你到处上架，每个商品可节省约 30 分钟。"),
    ("Here's a mistake I see constantly. Sellers upload a 5 MB product photo to Amazon, figuring \"bigger is better.\" Amazon's server then compresses it aggressively, and the result looks worse than if the seller had compressed it themselves.",
     "有一个我经常看到的错误。卖家把 5 MB 的商品照片上传到 Amazon，认为“越大越好”。然后 Amazon 的服务器激进地压缩它，结果比卖家自己压缩的还要差。"),
    ("Amazon's compression is not gentle. It's designed for speed, not quality. If you upload a 5 MB JPEG, it'll get crushed to maybe 300 KB with visible artifacts on smooth surfaces — white backgrounds, product labels, fabric.",
     "Amazon 的压缩并不温和。它为速度而非质量设计。如果你上传 5 MB 的 JPEG，它会被压到约 300 KB，在平滑表面——白色背景、商品标签、织物——上出现可见的伪影。"),
    ("The fix: compress before uploading. Aim for 200-500 KB per image at 1600×1600. At 80% JPEG quality, a typical product photo on a white background comes out to about 150-300 KB. That's small enough to load fast on mobile, and high enough quality that Amazon's re-compression won't destroy it.",
     "解决办法：上传前先压缩。目标是在 1600×1600 下每张图片 200-500 KB。以 80% 的 JPEG 质量，白底商品照片通常约为 150-300 KB。这小到可以在手机上快速加载，又足够高质量，Amazon 的再压缩不会毁掉它。"),
    ("The <a href=\"/zh/tools/compressor\">Image Compressor</a> handles this for single images. For batches, the E-Commerce Pack workflow compresses automatically at 82% by default — which I've found is the sweet spot. Below 65%, you get artifacts. Above 90%, you're doubling file size for zero visible improvement.",
     "<a href=\"/zh/tools/compressor\">图片压缩器</a>处理单张图片。对于批量，电商图片包工作流默认以 82% 自动压缩——我发现这是最佳点。低于 65% 会出现伪影。高于 90% 则文件翻倍却看不到任何改善。"),
    ("One more thing: strip EXIF metadata before uploading. Amazon does this anyway, but stripping it yourself saves 50-100 KB per image and prevents any location data from leaking. The <a href=\"/zh/tools/image-exif-remover\">EXIF Remover</a> does this in one click, or the E-Commerce Pack does it as part of the pipeline.",
     "还有一点：上传前去除 EXIF 元数据。Amazon 反正会做，但你自己去除每张图片可省 50-100 KB，并防止任何位置数据泄露。<a href=\"/zh/tools/image-exif-remover\">EXIF 去除器</a>一键完成，或电商图片包作为流水线的一部分完成。"),
]
for en, zh in PARAS:
    if en in h:
        h = h.replace(en, zh)
    else:
        print('MISS-PARA:', en[:60])

# list items
LIS = [
    ('<strong>Open the <a href="/zh/tools/product-white-background">Product White Background Maker</a></strong> — it\'s free, runs in your browser, and doesn\'t require an account.',
     '<strong>打开<a href="/zh/tools/product-white-background">商品白底制作工具</a></strong>——免费，在浏览器中运行，无需账号。'),
    ('<strong>Upload your product photo</strong> — drag and drop or click to browse. The image stays on your device. Nothing gets uploaded to a server.',
     '<strong>上传你的商品照片</strong>——拖放或点击浏览。图片保留在你的设备上，不会上传到服务器。'),
    ('<strong>The tool detects the subject and removes the existing background</strong> — this uses a client-side AI model that runs in your browser\'s WebGL. It\'s not as precise as a professional Photoshop mask, but for products with clean edges (bottles, boxes, jars), it\'s spot-on.',
     '<strong>工具检测主体并移除现有背景</strong>——这使用在浏览器 WebGL 中运行的客户端 AI 模型。它不如专业 Photoshop 抠图精确，但对于边缘清晰的商品（瓶、盒、罐），非常到位。'),
    ('<strong>Pick your background color</strong> — pure white is the default, but you can also choose soft blue, light gray, or transparent (PNG with alpha channel).',
     '<strong>选择背景颜色</strong>——默认为纯白，但你也可以选择柔蓝、浅灰或透明（带 alpha 通道的 PNG）。'),
    ('<strong>Download</strong> — the output is a JPEG with pure white background, ready for Amazon.',
     '<strong>下载</strong>——输出是带纯白背景的 JPEG，可直接用于 Amazon。'),
    ('Run each image through the <a href="/zh/tools/product-white-background">White Background Maker</a> first (5 seconds each)',
     '先用<a href="/zh/tools/product-white-background">白底制作工具</a>处理每张图片（每张 5 秒）'),
    ('Collect the white-background outputs', '收集白底输出'),
    ('Drop them all into the <a href="/zh/workflows/e-commerce-pack">E-Commerce Pack</a> for resizing to 1600×1600 and compression',
     '把它们全部放入<a href="/zh/workflows/e-commerce-pack\">电商图片包</a>缩放至 1600×1600 并压缩'),
    ('Download the ZIP and upload to Seller Central', '下载 ZIP 并上传到卖家中心'),
]
for en, zh in LIS:
    h = h.replace(en, zh)

# FAQ
FAQ = [
    ('Does Amazon require a white background for all product images?', 'Amazon 要求所有商品图片都是白底吗？'),
    ('No. Only the main (first) image needs pure white. Additional images can have lifestyle backgrounds, infographics, or different angles. But the main image — the one that shows in search results — must be pure white (RGB 255, 255, 255).',
     '不需要。只有主图（第一张）需要纯白。附加图片可以是生活场景背景、信息图或不同角度。但主图——即在搜索结果中显示的那张——必须是纯白（RGB 255, 255, 255）。'),
    ('What happens if my background isn\'t pure white?', '如果我的背景不是纯白会怎样？'),
    ('Amazon\'s automated system will reject the image during upload. You\'ll get an error in Seller Central saying the image doesn\'t meet requirements. The image won\'t go live until you fix it.',
     'Amazon 的自动系统会在上传时拒收图片。你会在卖家中心收到一条错误提示，说图片不符合要求。在你修复之前，图片不会上线。'),
    ('Can I use a lightbox instead of editing?', '我可以用灯箱代替编辑吗？'),
    ('A lightbox helps but rarely produces true 255,255,255 white. Even high-end lightboxes can produce 250-253 white depending on the bulbs and camera white balance. Running the photo through the white background tool after shooting ensures compliance.',
     '灯箱有帮助，但很少能产生真正的 255,255,255 白。即使是高端灯箱，根据灯泡和相机白平衡不同，也可能产生 250-253 的白。拍摄后用白底工具处理照片可确保合规。'),
    ('Is the Product White Background tool really free?', '商品白底工具真的免费吗？'),
    ('Yes. It runs entirely in your browser using client-side JavaScript and a WebAssembly AI model. No server costs, no subscription, no account. You can process as many images as you want.',
     '是的。它完全在浏览器中运行，使用客户端 JavaScript 和 WebAssembly AI 模型。无服务器成本、无订阅、无账号。你想处理多少图片都可以。'),
    ('What\'s the difference between the White Background tool and the Background Remover?', '白底工具和抠图工具有什么区别？'),
    ('The <a href="/zh/tools/background-remover">抠图工具</a> makes the background transparent (PNG with alpha). The <a href="/zh/tools/product-white-background">Product White Background Maker</a> removes the background and replaces it with solid white (or blue/gray). For Amazon, use the White Background tool. For creating product cutouts for compositing, use the Background Remover.',
     '<a href="/zh/tools/background-remover">抠图工具</a>把背景变透明（带 alpha 的 PNG）。<a href="/zh/tools/product-white-background">商品白底制作工具</a>移除背景并替换为纯白（或蓝/灰）。对于 Amazon，使用白底工具。要创建用于合成的商品抠图，使用抠图工具。'),
    ('How many images can I batch process?', '我可以批量处理多少张图片？'),
    ('The E-Commerce Pack handles up to 50 images per batch. For larger catalogs, run multiple batches. Each batch takes about 30 seconds on a modern laptop.',
     '电商图片包每批最多处理 50 张图片。对于更大的目录，分多批运行。在现代笔记本上每批约需 30 秒。'),
]
for en, zh in FAQ:
    h = h.replace(en, zh)

# CTA
h = h.replace('<h3>Ready to fix your product photos?</h3>', '<h3>准备好修复你的商品照片了吗？</h3>')
h = h.replace('<p>Try the Product White Background Maker — free, browser-based, no signup. Or batch-process your entire catalog with the E-Commerce Pack.</p>',
              '<p>试试商品白底制作工具——免费、浏览器端、无需注册。或用电商图片包批量处理你的整个目录。</p>')
h = h.replace('>Open White Background Tool →</a>', '>打开白底工具 →</a>')
h = h.replace('>Try E-Commerce Pack →</a>', '>试试电商图片包 →</a>')
# tags
TAGS = [('Amazon','Amazon'),('product images','商品图片'),('white background','白底'),('e-commerce','电商'),('batch processing','批量处理')]
for en, zh in TAGS:
    h = h.replace('<span class="blog-card-tag">' + en + '</span>', '<span class="blog-card-tag">' + zh + '</span>')
h = h.replace('>Share on X</a>', '>分享到 X</a>')
h = h.replace('>Share on LinkedIn</a>', '>分享到 LinkedIn</a>')
# author bio
h = h.replace(
    "Alex Carter is a freelance web developer in Austin, Texas, who builds small SaaS side projects and helps clients optimize their e-commerce listings. After losing a day to Amazon image rejections, he started building browser-based image tools to make the prep work faster. Find more guides on the <a href=\"/zh/blog/\">SmartImgKit 博客</a>.",
    "Alex Carter 是德克萨斯州奥斯汀的一名自由 Web 开发者，他开发小型 SaaS 副业项目，并帮助客户优化电商商品。在因 Amazon 图片拒收浪费了一整天后，他开始开发浏览器端图片工具以加快准备工作。更多指南见<a href=\"/zh/blog/\">SmartImgKit 博客</a>。")
# footer workflows section
h = h.replace('<h4>Workflows</h4>', '<h4>工作流</h4>')
h = h.replace('>Avatar Pipeline</a>', '>头像流水线</a>')
h = h.replace('>E-Commerce Pack</a>', '>电商图片包</a>')
h = h.replace('>Social Media Kit</a>', '>社交媒体套件</a>')
h = h.replace('>Listing Suite</a>', '>商品图片套件</a>')
h = h.replace('<p>Free AI-powered image tools that respect your privacy.</p>',
              '<p>尊重您隐私的免费 AI 图像工具。</p>')

with open(F, 'w', encoding='utf-8') as fh:
    fh.write(h)
print('amazon article translated, len:', len(h))
