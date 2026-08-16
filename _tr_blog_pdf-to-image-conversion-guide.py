# -*- coding: utf-8 -*-
import io

path = r"e:\网站项目\smartimgkit\zh\blog\pdf-to-image-conversion-guide.html"
with io.open(path, "r", encoding="utf-8") as f:
    html = f.read()

pairs = [
    # title tag
    ("<title>How to Convert PDF to Image Files: A Practical Guide for 2026 | SmartImgKit</title>",
     "<title>如何将 PDF 转换为图像文件：2026 实用指南 | SmartImgKit</title>"),
    # meta description (truncated version, unique to meta)
    ('content="I converted hundreds of PDFs to images and found the fastest free methods. Step-by-step instructions, format picks, and the mistakes that ruin your."',
     'content="我转换了数百个 PDF 为图像，找到了最快的免费方法。包含分步操作说明、格式选择，以及那些毁掉你成果的错误。"'),
    # og:title + twitter:title (content= prefix avoids JSON-LD headline)
    ('content="How to Convert PDF to Image Files: A Practical Guide for 2026"',
     'content="如何将 PDF 转换为图像文件：2026 实用指南"'),
    # og:description + twitter:description (content= prefix avoids JSON-LD description)
    ('content="I converted hundreds of PDFs to images and found the fastest free methods. Step-by-step instructions, format picks, and the mistakes that ruin your exports."',
     'content="我转换了数百个 PDF 为图像，找到了最快的免费方法。包含分步操作说明、格式选择，以及那些毁掉你导出成果的错误。"'),
    # breadcrumb
    (">PDF to Image Conversion Guide<", ">PDF 转图像指南<"),
    # h1
    ("<h1>How to Convert PDF to Image Files: A Practical Guide for 2026</h1>",
     "<h1>如何将 PDF 转换为图像文件：2026 实用指南</h1>"),
    # subtitle
    ('<p class="blog-post-subtitle">A client sent me a 47-page PDF deck last week and wanted it as images for Instagram. Here\'s what I learned after probably hundreds of conversions — including the format mistake that ruined my first 12 pages.</p>',
     '<p class="blog-post-subtitle">上周一位客户发给我一份 47 页的 PDF 演示稿，想把它转成图片发到 Instagram。在经历了大概上百次转换之后，这是我的心得——包括那个毁掉我前 12 页的格式错误。</p>'),
    # quick-answer p
    ('<p style="margin:0;">Converting PDF pages to images lets you post slides on Instagram, embed in websites, and share without PDF blockers. Use PNG for text-heavy pages, JPEG for photo-heavy content.</p>',
     '<p style="margin:0;">把 PDF 页面转换成图像后，你就可以把幻灯片发到 Instagram、嵌入网站，并且分享时不会遇到 PDF 被拦截的问题。文字多的页面用 PNG，照片多的内容用 JPEG。</p>'),
    # TOC h3
    ("<h3>Table of Contents</h3>", "<h3>目录</h3>"),
    # TOC items
    (">Why You'd Want to Convert a PDF to Images<", ">为什么需要把 PDF 转成图像<"),
    (">The Three Ways to Convert PDF to Image (Ranked)<", ">把 PDF 转成图像的三种方法（按推荐排序）<"),
    (">Resolution Matters More Than You Think<", ">分辨率比你想象的重要得多<"),
    (">What Image Format Should You Pick?<", ">该选哪种图像格式？<"),
    (">Step-by-Step: Convert PDF to Image With SmartImgKit<", ">分步教程：用 SmartImgKit 把 PDF 转成图像<"),
    (">Common Mistakes I See All the Time<", ">我常看到的那些错误<"),
    (">When the Browser Tool Isn't Enough<", ">浏览器工具不够用的时候<"),
    (">FAQ<", ">常见问题<"),
    # TL;DR label
    (">TL;DR<", ">太长不看<"),
    # TL;DR paragraph (has link)
    ('<p style="margin:0;">Converting PDF pages to images lets you drop them into slides, share on social, or edit in image editors. The fastest method: open <a href="/zh/tools/pdf-to-image">SmartImgKit PDF to Image</a>, drop the PDF, pick PNG or JPEG and resolution, download. This guide covers the rest: when PDF beats image, how to handle multi-page PDFs, and the one setting that ruins your exports.</p>',
     '<p style="margin:0;">把 PDF 页面转成图像后，你可以把它们放进幻灯片、分享到社交平台，或在图像编辑器里修改。最快的方法：打开 <a href="/zh/tools/pdf-to-image">SmartImgKit PDF 转图像</a>，拖入 PDF，选择 PNG 或 JPEG 以及分辨率，下载。本指南还会讲其余部分：什么时候 PDF 比图像更合适、如何处理多页 PDF，以及那个会毁掉你导出结果的设置。</p>'),
    # Section 1
    ("<h2>1. Why You'd Want to Convert a PDF to Images in the First Place</h2>",
     "<h2>1. 为什么一开始会需要把 PDF 转成图像</h2>"),
    ('<p>So I had a client send me a 47-page PDF deck last week. They wanted the slides \u201cas images\u201d for a quick Instagram carousel. Simple ask, right? Until I realized I\'d need an Adobe Acrobat subscription — which I don\'t pay for, and which costs like $20/month — just to save 47 pages as JPEGs. Or I could take screenshots one at a time. I tried that for about 4 minutes before I gave up and went looking for something better.</p>',
     '<p>上周有位客户发给我一份 47 页的 PDF 演示稿。他们想把幻灯片\u201c转成图片\u201d做一个 Instagram 轮播图。要求很简单，对吧？直到我意识到我得订阅 Adobe Acrobat——我没付费，而且它大概要 20 美元/月——就为了把 47 页存成 JPEG。或者我可以一张张截图。我试了大概 4 分钟就放弃了，开始找更好的办法。</p>'),
    ("<p>So here's the thing — converting PDF to image is one of those tasks that sounds boring but comes up constantly. Designers, marketers, students, accountants. Pretty much everyone needs it at some point.</p>",
     "<p>事情是这样的——把 PDF 转成图像听起来很无聊，但其实经常用到。设计师、营销人员、学生、会计，几乎每个人在某个时刻都会需要它。</p>"),
    ("<p>The big reasons people convert PDFs to images:</p>",
     "<p>大家把 PDF 转成图像的主要原因：</p>"),
    ("<li><strong>Social media sharing.</strong> Instagram, TikTok, LinkedIn carousels — none of them accept PDFs. If you've got a beautifully designed PDF report, you need images to post it as a swipe-through.</li>",
     "<li><strong>社交媒体分享。</strong>Instagram、TikTok、LinkedIn 的轮播图——没有一个接受 PDF。如果你有一份设计精美的 PDF 报告，你需要把它转成图片才能以滑动浏览的形式发布。</li>"),
    ("<li><strong>Website embedding.</strong> Images load faster and respond better to mobile than embedded PDF viewers. Plus, you can lazy-load images. PDFs just... sit there.</li>",
     "<li><strong>网站嵌入。</strong>图片比内嵌的 PDF 查看器加载更快，在手机上表现也更好。而且图片可以懒加载。PDF 就只能……杵在那儿。</li>"),
    ("<li><strong>Thumbnails and previews.</strong> Most file preview systems prefer image thumbnails. PDFs are clunky to render at small sizes.</li>",
     "<li><strong>缩略图和预览。</strong>大多数文件预览系统更偏好图片缩略图。PDF 在小尺寸下渲染很笨拙。</li>"),
    ("<li><strong>Email attachments.</strong> PDFs sometimes get blocked by email clients. Images almost never do.</li>",
     "<li><strong>邮件附件。</strong>PDF 有时会被邮件客户端拦截。图片几乎从来不会。</li>"),
    ("<li><strong>Editing in other tools.</strong> Want to use a slide as a Photoshop layer? Convert it. Want to add a watermark? Convert it first. Want to crop one section? Yeah, convert it.</li>",
     "<li><strong>在其他工具里编辑。</strong>想把某张幻灯片作为 Photoshop 图层？转一下。想加水印？先转一下。想裁剪某一部分？对，还是转一下。</li>"),
    ("<li><strong>Combining content.</strong> Combining a PDF page with other images in a collage or mood board? You'll want them all as image files first.</li>",
     "<li><strong>组合内容。</strong>想把 PDF 页面和其他图片拼成拼贴图或情绪板？你得先把它们都变成图片文件。</li>"),
    ("<p>Honestly, once you start looking for it, the use cases are everywhere. I use it probably twice a week for client work.</p>",
     "<p>说实话，一旦开始留意，你会发现使用场景无处不在。我大概每周为客户的活儿用两次。</p>"),
    # Section 2
    ("<h2>2. The Three Ways to Convert PDF to Image (Ranked)</h2>",
     "<h2>2. 把 PDF 转成图像的三种方法（按推荐排序）</h2>"),
    ("<p>I've tried basically every method out there. They fall into three buckets, and they're not all equal.</p>",
     "<p>基本上每种方法我都试过。它们可以归为三类，而且并不是都一样好用。</p>"),
    ("<h3>Browser-based tools (best for most people)</h3>",
     "<h3>浏览器工具（适合大多数人）</h3>"),
    ("<p>This is what I use 95% of the time now. You open a website, drop in your PDF, and download the result. No software. No account. No cost. The big advantage: privacy. The best tools run entirely in your browser. Your PDF never leaves your computer. For client work, financial documents, medical records — that matters.</p>",
     "<p>现在 95% 的情况我都在用这个。打开网站，拖入 PDF，下载结果。不用装软件、不用注册账号、不花钱。最大的好处是：隐私。最好的工具完全在你的浏览器里运行，PDF 根本不会离开你的电脑。对于客户文件、财务文档、医疗记录来说——这很重要。</p>"),
    ("<h3>Desktop software (overkill for most people)</h3>",
     "<h3>桌面软件（对多数人来说大材小用）</h3>"),
    ("<p>Adobe Acrobat, PDF Expert, Nitro, Foxit. Full PDF editors that include export-as-image. They work well — but they cost money. Acrobat Pro is $20/month. For something you do twice a month, that's a tough sell. Unless you already have a subscription. In which case, File > Export To > Image and you're done.</p>",
     "<p>Adobe Acrobat、PDF Expert、Nitro、Foxit。这些是完整的 PDF 编辑器，包含导出为图像的功能。它们很好用——但要花钱。Acrobat Pro 是 20 美元/月。对于一个月只做两次的事，这笔账不划算。除非你已经有订阅。那样的话，文件 > 导出为 > 图像，就搞定了。</p>"),
    ("<h3>Screenshotting (my least favorite)</h3>",
     "<h3>截图（我最不推荐）</h3>"),
    ('<p>This is what most people default to. Open the PDF, hit Print Screen, paste into an image editor, crop, save, repeat 47 times. For one page, fine. For a 50-page report, you\'re signing up for an hour of misery. Plus, screenshots are rasterized at your screen resolution — usually 1080p or 1440p. That means your \u201chigh-res\u201d image is actually only 2-3 megapixels. Look, screenshots are fine in a pinch. But if you\'re doing this more than once, grab a proper tool.</p>',
     '<p>这是大多数人默认采用的办法。打开 PDF，按 Print Screen，粘贴到图像编辑器里，裁剪，保存，重复 47 次。一页还好。一份 50 页的报告，你就是在给自己签下一小时的苦差事。而且，截图是以你屏幕分辨率栅格化的——通常是 1080p 或 1440p。也就是说你那张\u201c高清\u201d图其实只有 2-3 百万像素。听着，应急用截图没问题。但如果你不止做一次，就找个正经工具吧。</p>'),
    # Section 3
    ("<h2>3. Resolution Matters More Than You Think</h2>",
     "<h2>3. 分辨率比你想象的重要得多</h2>"),
    ("<p>Here's the part that tripped me up for years. When you convert a PDF to an image, the resulting image has a resolution. And the default on most tools is way too low.</p>",
     "<p>这里是让我栽了好多年的坑。当你把 PDF 转成图像时，生成的图像有一个分辨率。而大多数工具的默认值都太低了。</p>"),
    ("<p>A 1080p screenshot of a PDF page is about 2 megapixels. That sounds decent until you try to print it (needs 300 DPI minimum, so a letter-size page needs about 8 megapixels), zoom in on a chart (looks pixelated immediately), or use it on a high-DPI display (looks soft).</p>",
     "<p>一张 PDF 页面的 1080p 截图大约是 2 百万像素。听起来还行，直到你想把它打印出来（至少需要 300 DPI，所以一页 letter 尺寸大约需要 8 百万像素），放大看图表（立刻出现马赛克），或者在高 DPI 显示器上看（发虚）。</p>"),
    ("<p>What you want is at least 2x resolution, or ideally 3x. A 3x conversion of a US letter page produces an image around 2550x3300 pixels — about 8.4 megapixels. That's the sweet spot for most uses.</p>",
     "<p>你要的是至少 2 倍分辨率，理想情况下 3 倍。一页 US letter 的 3 倍转换会生成大约 2550x3300 像素的图像——约 8.4 百万像素。这是大多数用途的最佳甜区。</p>"),
    ("<p>Most browser-based tools default to 2x or 3x. The good ones let you pick. If a tool only gives you 1x, skip it.</p>",
     "<p>大多数浏览器工具默认 2 倍或 3 倍。好的工具让你自己选。如果某个工具只给 1 倍，跳过它。</p>"),
    ("<p>Honestly? I didn't know this for a long time. I just kept getting blurry, low-quality exports and assumed that was how PDFs worked. It wasn't. The tool was bad.</p>",
     "<p>说实话？很长一段时间我都不知道这个。我只是一直得到模糊、低质量的导出，以为 PDF 就是这样。并不是。是工具太差。</p>"),
    # Section 4
    ("<h2>4. What Image Format Should You Pick?</h2>",
     "<h2>4. 该选哪种图像格式？</h2>"),
    ("<p>This is the other thing that confused me when I started. PDF-to-image tools usually give you three or four format options. Here's how to pick:</p>",
     "<p>这是我刚开始时另一个让我困惑的事。PDF 转图像工具通常给你三四种格式选项。下面是选择方法：</p>"),
    ("<p><strong>PNG.</strong> Best for text-heavy pages, slides, anything with sharp lines. Lossless, so nothing gets fuzzy. File sizes are bigger, but quality is excellent. My default for client work.</p>",
     "<p><strong>PNG。</strong>最适合文字多的页面、幻灯片，以及任何有锐利线条的内容。无损，所以不会发虚。文件体积更大，但质量极佳。我做客户活儿时的默认选择。</p>"),
    ("<p><strong>JPEG.</strong> Best for photo-heavy PDFs — magazines, brochures, catalogs. Smaller files, but you lose some quality. Fine for web. For print, be careful — JPEG artifacts show up at high zoom.</p>",
     "<p><strong>JPEG。</strong>最适合照片多的 PDF——杂志、宣传册、目录。文件更小，但会损失一些质量。网页用没问题。要打印的话要小心——JPEG 的压缩伪影在高倍放大时会显现。</p>"),
    ("<p><strong>WebP.</strong> Smaller than JPEG at similar quality. Browser support is great now. Good for web, less so for print software.</p>",
     "<p><strong>WebP。</strong>在相近质量下比 JPEG 更小。现在浏览器支持已经很好。适合网页，对打印软件来说差一些。</p>"),
    ("<p><strong>TIFF.</strong> The print-industry standard. Massive files. Most people don't need this.</p>",
     "<p><strong>TIFF。</strong>印刷行业的标准。文件巨大。大多数人用不到。</p>"),
    ("<p>For most conversions, I go with PNG. Bigger file, but no weird compression artifacts around text. Quick tip: convert one page first to test your format and resolution. Don't run 50 pages at the wrong settings and then realize page one looks terrible.</p>",
     "<p>大多数转换我选 PNG。文件更大，但文字周围不会有奇怪的压缩伪影。一个小提示：先转换一页来测试你的格式和分辨率。别用错误的设置跑 50 页，然后才发现第一页看起来很糟。</p>"),
    # Section 5
    ("<h2>5. Step-by-Step: Convert PDF to Image With SmartImgKit</h2>",
     "<h2>5. 分步教程：用 SmartImgKit 把 PDF 转成图像</h2>"),
    ("<p>Here's the workflow I use most often. Free, fast, no signup.</p>",
     "<p>这是我最常用的工作流。免费、快速、不用注册。</p>"),
    ("<h3>Step 1: Open the PDF to Image tool</h3>",
     "<h3>第 1 步：打开 PDF 转图像工具</h3>"),
    ('<p>Head to the <a href="/zh/tools/pdf-to-image">SmartImgKit PDF to Image tool</a>. No download. No account creation. Works on any device with a modern browser.</p>',
     '<p>前往 <a href="/zh/tools/pdf-to-image">SmartImgKit PDF 转图像工具</a>。不用下载、不用创建账号。在任何带现代浏览器的设备上都能用。</p>'),
    ("<h3>Step 2: Upload your PDF</h3>",
     "<h3>第 2 步：上传你的 PDF</h3>"),
    ("<p>Drag your PDF into the upload area, or click to browse. The tool handles multi-page PDFs, which is the whole point. A 100-page report is no different from a 1-page report.</p>",
     "<p>把 PDF 拖到上传区域，或点击浏览选择。这个工具能处理多页 PDF，这正是它的意义所在。100 页的报告和 1 页的报告没区别。</p>"),
    ("<h3>Step 3: Choose your settings</h3>",
     "<h3>第 3 步：选择设置</h3>"),
    ("<p>You'll see options for format (PNG, JPEG, or WebP), resolution (150 for screen, 300 for print), and page range. I default to PNG at 150 DPI, and use the page range to skip the parts I don't need.</p>",
     "<p>你会看到格式（PNG、JPEG 或 WebP）、分辨率（屏幕用 150，打印用 300）以及页面范围的选项。我默认用 PNG 150 DPI，并用页面范围跳过不需要的部分。</p>"),
    ("<h3>Step 4: Convert and download</h3>",
     "<h3>第 4 步：转换并下载</h3>"),
    ("<p>Hit the convert button. The tool processes each page and packages them up. Download all as a ZIP, or grab them one at a time. A 20-page PDF usually takes under 30 seconds.</p>",
     "<p>点击转换按钮。工具会处理每一页并打包。下载全部为 ZIP，或一张张取。一份 20 页的 PDF 通常不到 30 秒就完成。</p>"),
    ("<h3>Step 5: Check the results</h3>",
     "<h3>第 5 步：检查结果</h3>"),
    ("<p>Open a few of the images. Zoom in. Check the text. If something's off, try a higher DPI or switch from JPEG to PNG. This worked for me on dozens of client projects, but you might find a different workflow that fits your needs.</p>",
     "<p>打开几张图片。放大。检查文字。如果哪里不对，试试更高的 DPI，或从 JPEG 换成 PNG。这在几十个客户项目上都管用，但你可能会找到更适合自己需求的工作流。</p>"),
    # Section 6
    ("<h2>6. Common Mistakes I See All the Time</h2>",
     "<h2>6. 我常看到的那些错误</h2>"),
    ("<p>After years of helping people with this, I notice the same mistakes come up over and over. Save yourself the headache.</p>",
     "<p>帮人处理这事多年后，我发现同样的错误反复出现。别让自己头疼。</p>"),
    ("<p><strong>Going too low on resolution.</strong> If you convert at 72 DPI, your image looks fine on a phone. It'll look awful on a desktop, tablet, or in print. 150 DPI is the default sweet spot. Go higher when in doubt — you can always downsize later, but you can't add pixels back.</p>",
     "<p><strong>分辨率设得太低。</strong>如果你用 72 DPI 转换，图片在手机上看起来还行。在桌面、平板或打印时会很难看。150 DPI 是默认的甜区。拿不准就调高——你总能缩小，但没法把像素加回来。</p>"),
    ("<p><strong>Picking JPEG when you need PNG.</strong> Text, charts, diagrams, sharp lines — JPEG adds compression artifacts around those edges. PNG avoids this. Bigger file, way better quality for text-heavy content.</p>",
     "<p><strong>该用 PNG 时选了 JPEG。</strong>文字、图表、示意图、锐利线条——JPEG 会在这些边缘加上压缩伪影。PNG 能避免。文件更大，但对文字多的内容质量好得多。</p>"),
    ("<p><strong>Forgetting the page range.</strong> Converting all 200 pages when you only need 12 wastes time and disk space. Most tools have a page range option. Use it.</p>",
     "<p><strong>忘了设页面范围。</strong>你只需要 12 页却转换全部 200 页，既浪费时间又浪费磁盘空间。大多数工具有页面范围选项。用上它。</p>"),
    ("<p><strong>Ignoring privacy.</strong> Some free tools upload your PDF to their server. For a homework assignment, who cares. For a confidential client document, that's a real problem. Pick a tool that processes in-browser.</p>",
     "<p><strong>忽视隐私。</strong>有些免费工具会把你的 PDF 上传到他们的服务器。作业文件无所谓。但机密的客户文件就是个真正的问题。选一个在浏览器里处理的工具。</p>"),
    ("<p><strong>Wrong aspect ratio.</strong> US letter is 8.5x11. A4 is slightly different. Set the wrong size and your output gets stretched or squished. Most tools auto-detect, but check the preview before converting 50 pages.</p>",
     "<p><strong>宽高比不对。</strong>US letter 是 8.5x11。A4 略有不同。设错尺寸，输出就会被拉伸或挤压。大多数工具会自动检测，但转换 50 页前还是检查一下预览。</p>"),
    # Section 7
    ("<h2>7. When the Browser Tool Isn't Enough</h2>",
     "<h2>7. 浏览器工具不够用的时候</h2>"),
    ("<p>For 95% of conversions, a free browser tool does the job. But there are cases where you might need something more.</p>",
     "<p>对于 95% 的转换，免费浏览器工具就够用。但有些情况你可能需要更强的东西。</p>"),
    ("<p><strong>If you have 500+ pages.</strong> Browser tools can handle it, but it'll be slow. A desktop tool with batch processing is faster.</p>",
     "<p><strong>如果你有 500 页以上。</strong>浏览器工具能处理，但会很慢。带批量处理的桌面工具更快。</p>"),
    ("<p><strong>If you need OCR.</strong> Scanned PDFs are images, not real text. The conversion will preserve that — the output is still a picture of text, not searchable. If you need selectable text, you need OCR on top of the conversion.</p>",
     "<p><strong>如果你需要 OCR。</strong>扫描版 PDF 是图像，不是真正的文字。转换会保留这一点——输出仍然是文字的图片，不能搜索。如果你需要可选中的文字，就要在转换之外再加 OCR。</p>"),
    ("<p><strong>If you need 600+ DPI print output.</strong> Browser tools usually max out at 300 DPI. For fine art or large-format commercial printing, you might need more. Adobe Acrobat handles this.</p>",
     "<p><strong>如果你需要 600 DPI 以上的打印输出。</strong>浏览器工具通常最高 300 DPI。对于美术作品或大幅面商业印刷，你可能需要更高。Adobe Acrobat 能处理。</p>"),
    ("<p><strong>If you need automation.</strong> Converting 100 PDFs a week? You want a script. Python with pdf2image or Node.js with pdf-poppler can batch-process.</p>",
     "<p><strong>如果你需要自动化。</strong>每周转换 100 个 PDF？你需要脚本。Python 配 pdf2image，或 Node.js 配 pdf-poppler 可以批量处理。</p>"),
    # when-not-to
    ("<h2>When NOT to convert PDF to image</h2>",
     "<h2>什么时候不该把 PDF 转成图像</h2>"),
    ("<p>If your PDF has selectable text and you need that text in the output, conversion to image flattens everything. You'll lose searchability and accessibility. Use PDF tools that preserve text layers instead.</p>",
     "<p>如果你的 PDF 有可选中文字，而你需要输出里保留这些文字，转成图像会把一切压平。你会失去可搜索性和可访问性。改用保留文字层的 PDF 工具。</p>"),
    ("<p>Also, if you're dealing with a PDF that needs to be accessible (screen readers, etc.), don't flatten it to images. Your mileage may vary, but if accessibility matters, keep it as a PDF.</p>",
     "<p>另外，如果你处理的 PDF 需要具备可访问性（屏幕阅读器等），别把它压平成图像。情况因人而异，但如果可访问性很重要，就保留为 PDF。</p>"),
    # FAQ (use >...< boundary to avoid JSON-LD)
    (">Will the converted images look the same as the PDF?<",
     ">转换后的图像会和 PDF 看起来一样吗？<"),
    (">Yes, the visual content matches exactly. The PDF's text and vector graphics get rendered to pixels at your chosen DPI. The trade-off: the output is no longer searchable or selectable as text. If you need searchable text, you need OCR on top of the conversion. I tested this on 17 different PDFs and got pixel-perfect output every time. The part I always forget: complex fonts may not render identically on all systems.<",
     ">是的，视觉内容完全一致。PDF 的文字和矢量图形会按你选择的 DPI 渲染成像素。代价是：输出不再是可搜索或可选中文字。如果你需要可搜索的文字，就要在转换之外再加 OCR。我在 17 个不同的 PDF 上测试过，每次都是像素级完美的输出。我老忘的一点：复杂字体在不同系统上渲染可能不完全一致。<"),
    (">What's the best DPI for PDF to image?<",
     ">PDF 转图像用多少 DPI 最好？<"),
    (">300 DPI is the standard for print-quality output. 150 DPI works for screen viewing and keeps file sizes smaller. 72 DPI is fine for thumbnails but text gets fuzzy. For archival or printing, go 300. For web previews, 150 is plenty. Honestly, most people use 200 as a compromise.<",
     ">300 DPI 是印刷质量输出的标准。150 DPI 适合屏幕查看，文件也更小。72 DPI 做缩略图还行，但文字会发虚。用于存档或印刷，选 300。用于网页预览，150 足够。说实话，大多数人用 200 作为折中。<"),
    (">Can I convert just one page from a PDF?<",
     ">可以只转换 PDF 的某一页吗？<"),
    ('>Yes \u2014 modern tools let you select a page range. You can extract pages 1-5, or just page 12, without processing the whole document. The part I always forget: PDF page numbering is 1-based, not 0-based. So page \u201c1\u201d is the first page, not page \u201c0.\u201d Yeah, that bit me on a project once.<',
     '>可以——现代工具让你选择页面范围。你可以只提取第 1-5 页，或只第 12 页，而不用处理整个文档。我老忘的一点：PDF 页码是从 1 开始的，不是从 0。所以\u201c1\u201d是第一页，不是\u201c0\u201d。嗯，这事在一个项目里坑过我一次。<'),
    (">What format should I export to?<",
     ">应该导出成什么格式？<"),
    ('>PNG for sharp text and line art (lossless). JPEG for photos and pages with lots of color (smaller files). WebP for web use (best compression). For most \u201cI just need to share this PDF page as an image\u201d cases, PNG at 200 DPI works great. By the way, I tested 4 formats and found PNG was the best balance of quality and compatibility.<',
     '>PNG 适合锐利文字和线条图（无损）。JPEG 适合照片和颜色丰富的页面（文件更小）。WebP 适合网页用途（压缩最好）。对于大多数\u201c我只想把这页 PDF 分享成图片\u201d的情况，200 DPI 的 PNG 就很好。顺便说一句，我测过 4 种格式，发现 PNG 在质量和兼容性上是最佳平衡。<'),
    (">Is PDF to image conversion safe?<",
     ">PDF 转图像安全吗？<"),
    (">Browser-based tools that process locally (like SmartImgKit's converter) are safe — the PDF never leaves your device. Cloud-based converters are riskier if the PDF contains sensitive data. For confidential documents, always use a local tool. Honestly, this is a big deal for legal/medical/financial PDFs.<",
     ">在本地处理的浏览器工具（比如 SmartImgKit 的转换器）是安全的——PDF 不会离开你的设备。如果 PDF 含有敏感数据，云端转换器风险更高。对于机密文档，始终用本地工具。说实话，对于法律、医疗、财务类的 PDF，这很重要。<"),
    # author-bio (has link)
    ('<p style="margin:0;">Riley Tanaka has processed literally thousands of PDFs for web use since 2019. Wrote this guide based on real trial-and-error with actual client files. More image tips on the <a href="/zh/blog/">SmartImgKit 博客</a>.</p>',
     '<p style="margin:0;">Riley Tanaka 自 2019 年以来为网页用途处理过成千上万个 PDF。本指南基于真实客户文件的实际试错写成。更多图像技巧见 <a href="/zh/blog/">SmartImgKit 博客</a>。</p>'),
    # footer brand
    ("<p>Free AI-powered image tools that respect your privacy.</p>",
     "<p>尊重你隐私的免费 AI 图像工具。</p>"),
    # footer h4 Workflows
    ("<h4>Workflows</h4>", "<h4>工作流</h4>"),
    # workflow links
    (">Avatar Pipeline<", ">头像流水线<"),
    (">E-Commerce Pack<", ">电商套装<"),
    (">Social Media Kit<", ">社交媒体套件<"),
    (">Listing Suite<", ">商品图套件<"),
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

print("Total replacements applied:", count)