# -*- coding: utf-8 -*-
import io
path = r"e:\网站项目\smartimgkit\zh\blog\remove-background-complete-guide.html"
with io.open(path, "r", encoding="utf-8") as f:
    html = f.read()
pairs = []
P = pairs.append
# title tag
P(("<title>How to Remove Background from Images: Complete Guide 2026 | SmartImgKit</title>",
   "<title>如何从图像中移除背景：2026 完整指南 | SmartImgKit</title>"))
# meta description (unique - ends 'like hair.')
P(('content="Step-by-step tutorial on removing image backgrounds with AI. Covers how it works, which methods produce clean cutouts, and tips for tricky subjects like hair."',
   'content="用 AI 移除图像背景的分步教程。涵盖工作原理、哪些方法能产生干净的抠图，以及处理头发等棘手主体的技巧。"'))
# og:title + twitter:title
P(('content="How to Remove Background from Images: Complete Guide 2026"',
   'content="如何从图像中移除背景：2026 完整指南"'))
# og:description (unique - 'actually produce' + 'hair and fur')
P(('content="Step-by-step tutorial on removing image backgrounds with AI. Covers how it works, which methods actually produce clean cutouts, and tips for tricky subjects like hair and fur."',
   'content="用 AI 移除图像背景的分步教程。涵盖底层工作原理、哪些方法能真正产生干净的抠图，以及处理头发和毛发等棘手主体的技巧。"'))
# twitter:description (unique - ends 'tricky subjects.')
P(('content="Step-by-step tutorial on removing image backgrounds with AI. Covers how it works, which methods produce clean cutouts, and tips for tricky subjects."',
   'content="用 AI 移除图像背景的分步教程。涵盖工作原理、哪些方法能产生干净的抠图，以及处理棘手主体的技巧。"'))
# breadcrumb
P((">Remove Background Guide<", ">移除背景指南<"))
# blog-card-tag
P((">Tutorial<", ">教程<"))
# h1
P(("<h1>How to Remove Background from Images: A Complete Guide for 2026</h1>",
   "<h1>如何从图像中移除背景：2026 完整指南</h1>"))
# subtitle
P(("<p class=\"blog-post-subtitle\">I've spent way too many hours cutting out product photos by hand. Here's what I've learned about getting clean cutouts — and why AI changed everything.</p>",
   "<p class=\"blog-post-subtitle\">我花了太多时间手工抠产品图。这是我对获得干净抠图的心得——以及为什么 AI 改变了一切。</p>"))
# TOC h3
P(("<h3>Table of Contents</h3>", "<h3>目录</h3>"))
# TOC items
P((">Why Bother Removing Backgrounds?<", ">为什么要移除背景？<"))
P((">The Old Ways (And Why They Sucked)<", ">老方法（以及它们为什么糟糕）<"))
P((">What's Actually Happening Under the Hood<", ">底层到底发生了什么<"))
P((">Remove a Background in 30 Seconds<", ">30 秒移除背景<"))
P((">Getting Better Results: Tips That Actually Help<", ">获得更好效果：真正有用的技巧<"))
P((">Real-World Use Cases<", ">实际使用场景<"))
P((">Picking the Right Tool<", ">挑选合适的工具<"))
P((">FAQ<", ">常见问题<"))
# TL;DR
P((">TL;DR<", ">太长不看<"))
P(("<p style=\"margin:0;\">AI background removers hit maybe 95% accuracy on people, pets, and products — close enough that you'll only touch up the occasional flyaway hair. Open <a href=\"/zh/tools/background-remover\">SmartImgKit Background Remover</a>, drop your image, get a clean PNG with transparent background. Free, browser-based, no upload. This guide explains the \"why\" behind the tool, plus tips for the 5% of cases AI still gets wrong.</p>",
   "<p style=\"margin:0;\">AI 抠图工具对人、宠物和产品的准确率大约能达到 95%——已经足够好，你只需偶尔修一下飘飞的头发。打开 <a href=\"/zh/tools/background-remover\">SmartImgKit 抠图工具</a>，拖入图片，就能得到一张背景透明的干净 PNG。免费、基于浏览器、不上传。本指南解释了这款工具背后的\u201c原因\u201d，并附上 AI 仍会出错的 5% 情况的技巧。</p>"))
# Section 1
P(("<h2>1. Why Bother Removing Backgrounds?</h2>", "<h2>1. 为什么要移除背景？</h2>"))
P(("<p>If you've ever tried selling something online, you already know the answer. That photo you took on your kitchen counter? It looks fine to you. But put it next to a competitor's listing with a clean white background, and suddenly your product looks like it's being sold out of someone's garage.</p>",
   "<p>如果你试过在网上卖东西，你就知道答案了。你在厨房台面上拍的那张照片？你觉得还行。但把它和竞品那种干净白底的商品图放在一起，你的产品突然看起来就像是从某人的车库里卖出来的。</p>"))
P(("<p>It's not just e-commerce either. Social media profiles, presentation slides, blog headers — they all look sharper when the subject is isolated. A busy background fights for attention. A clean cutout lets the viewer focus on what matters.</p>",
   "<p>而且不只是电商。社交媒体头像、演示文稿幻灯片、博客头图——当主体被分离出来时，它们都显得更利落。杂乱的背景会抢夺注意力。干净的抠图让观众聚焦于真正重要的东西。</p>"))
P(("<p>The biggest surprise to me was how much it affects sales. I've seen stores swap out their product photos for clean-background versions and watch their click-through rates climb. It makes sense when you think about it: on a search results page, the product that \"pops\" off the screen is the one that gets clicked.</p>",
   "<p>最让我惊讶的是它对销量的影响。我见过店铺把产品图换成干净背景的版本，然后看着点击率一路上升。仔细想想也合理：在搜索结果页上，那个从屏幕上\u201c跳出来\u201d的产品才会被点击。</p>"))
P(("<p>And then there are the less obvious situations — the ones where background removal saves the day without you even realizing it. Need a headshot for a conference badge but only have a photo from a dinner party? Remove the background, drop in a solid color, and you're good. Helping a kid with a school project that needs a cutout of a dinosaur? Same idea. It's one of those skills that comes in handy way more often than you'd expect.</p>",
   "<p>还有一些不太明显的场景——那些背景移除在你不知不觉中救场的情况。需要一张会议证件照，但只有一张晚宴上拍的照片？移除背景，换成纯色，就行了。帮孩子做需要恐龙抠图的手工作业？同理。这是一项比你想象中更常派上用场的技能。</p>"))
# Section 2
P(("<h2>2. The Old Ways (And Why They Sucked)</h2>", "<h2>2. 老方法（以及它们为什么糟糕）</h2>"))
P(("<p>I learned Photoshop in college, and for years the Pen Tool was just part of my workflow (yeah, I still can't believe how long I did this manually). Need to cut out a product? Fire up the Pen Tool, zoom in to 400%, start clicking anchor points around the edge. A simple product shot took maybe 10 minutes. A person with curly hair? Half an hour, minimum, and the result still wasn't great around the edges.</p>",
   "<p>我在大学里学了 Photoshop，多年来钢笔工具就是我工作流的一部分（是的，我至今不敢相信自己手动做了那么久）。需要抠一个产品？打开钢笔工具，放大到 400%，沿着边缘一个个点击锚点。一张简单的产品图大概要 10 分钟。一个卷发的人？至少半小时，而且边缘效果还是不太好。</p>"))
P(("<p>The thing is, there weren't really better options. The Magic Wand was fast but terrible — it'd eat into the subject or leave chunks of background behind. The Quick Select tool was a bit smarter, but you'd still spend ages cleaning up. And green screen? Great if you planned ahead, but who carries a green screen to a product shoot?</p>",
   "<p>问题是，当时并没有真正更好的选择。魔棒工具很快但很糟糕——它会侵蚀主体或留下大块背景。快速选择工具聪明一点，但你还是得花大量时间清理。而绿幕？提前准备的话很好用，但谁会带绿幕去拍产品呢？</p>"))
# comparison table cells (full div for safety)
P(('<div class="comparison-cell">Method</div>', '<div class="comparison-cell">方法</div>'))
P(('<div class="comparison-cell">Time</div>', '<div class="comparison-cell">时间</div>'))
P(('<div class="comparison-cell">Skill Needed</div>', '<div class="comparison-cell">技能要求</div>'))
P(('<div class="comparison-cell">Quality</div>', '<div class="comparison-cell">质量</div>'))
P(('<div class="comparison-cell">Magic Wand</div>', '<div class="comparison-cell">魔棒工具</div>'))
P(('<div class="comparison-cell">1-5 min</div>', '<div class="comparison-cell">1-5 分钟</div>'))
P(('<div class="comparison-cell">Not much</div>', '<div class="comparison-cell">不多</div>'))
P(('<div class="comparison-cell">Meh</div>', '<div class="comparison-cell">一般</div>'))
P(('<div class="comparison-cell">Pen Tool</div>', '<div class="comparison-cell">钢笔工具</div>'))
P(('<div class="comparison-cell">10-30 min</div>', '<div class="comparison-cell">10-30 分钟</div>'))
P(('<div class="comparison-cell">A lot</div>', '<div class="comparison-cell">很多</div>'))
P(("<div class=\"comparison-cell\">Great if you're patient</div>", "<div class=\"comparison-cell\">有耐心的话很棒</div>"))
P(('<div class="comparison-cell">Quick Select / Lasso</div>', '<div class="comparison-cell">快速选择 / 套索</div>'))
P(('<div class="comparison-cell">3-10 min</div>', '<div class="comparison-cell">3-10 分钟</div>'))
P(('<div class="comparison-cell">Some</div>', '<div class="comparison-cell">一些</div>'))
P(('<div class="comparison-cell">Decent</div>', '<div class="comparison-cell">尚可</div>'))
P(('<div class="comparison-cell">Green Screen</div>', '<div class="comparison-cell">绿幕</div>'))
P(('<div class="comparison-cell">Setup + 2 min</div>', '<div class="comparison-cell">准备 + 2 分钟</div>'))
P(('<div class="comparison-cell">Good</div>', '<div class="comparison-cell">好</div>'))
P(('<strong>AI Background Remover</strong>', '<strong>AI 抠图工具</strong>'))
P(('<strong>5-15 sec</strong>', '<strong>5-15 秒</strong>'))
P(('<strong>None</strong>', '<strong>无需</strong>'))
P(('<strong>Surprisingly good</strong>', '<strong>出乎意料地好</strong>'))
P(("<p>The core problem was always the same: you could have it fast, or you could have it good, but not both. The Pen Tool gave you control but ate your afternoon. The Magic Wand was instant but left you with jagged edges and missing chunks. It was a lousy trade-off.</p>",
   "<p>核心问题始终一样：你要么快，要么好，但无法兼得。钢笔工具给你控制力，但会耗掉你一下午。魔棒工具是即时的，但留下锯齿边缘和缺失的碎块。这是个糟糕的权衡。</p>"))
P(("<p>Honestly, AI just sidesteps the whole thing. The results I get now from a free browser tool are genuinely comparable to what I used to produce with the Pen Tool — and they take 5 seconds instead of 20 minutes. I still use Photoshop for stuff that needs pixel-level precision, but for like 90% of background removals, AI handles it.</p>",
   "<p>说实话，AI 直接绕开了整个问题。我现在用免费浏览器工具得到的效果，真的能和我以前用钢笔工具做出来的相媲美——而且只要 5 秒而不是 20 分钟。需要像素级精度的东西我还是用 Photoshop，但大约 90% 的背景移除，AI 都能搞定。</p>"))
# Section 3
P(("<h2>3. What's Actually Happening Under the Hood</h2>", "<h2>3. 底层到底发生了什么</h2>"))
P(("<p>You don't need to understand the math to use these tools, but knowing the basics helps you set realistic expectations and troubleshoot when things go wrong.</p>",
   "<p>使用这些工具你不需要懂其中的数学，但了解基础知识能帮你设定合理的预期，并在出问题时排查故障。</p>"))
P(("<h3>The short version</h3>", "<h3>简短版本</h3>"))
P(("<p>The AI looks at every pixel in your image and basically votes: \"this pixel is part of the subject\" or \"this pixel is background.\" It does this by having \"seen\" millions of labeled images during training — photos where humans carefully traced the subject boundary. After enough examples, the model internalizes what a person looks like, what a product looks like, where edges tend to fall, and so on.</p>",
   "<p>AI 会查看你图像中的每一个像素，基本上是在投票：\u201c这个像素属于主体\u201d或\u201c这个像素属于背景\u201d。它之所以能做到这一点，是因为在训练期间\u201c看过\u201d了数百万张标注过的图像——那些由人类仔细描出主体边界的照片。在看了足够多的例子后，模型就内化了人长什么样、产品长什么样、边缘通常落在哪里等等。</p>"))
P(("<p>When you feed it a new image, it applies those learned patterns. The output is a grayscale mask: white pixels for the subject, black for the background, and gray for the uncertain areas (which is where the interesting stuff happens, especially around hair and fur).</p>",
   "<p>当你给它一张新图像时，它会应用这些学到的模式。输出是一张灰度蒙版：主体是白色像素，背景是黑色，不确定的区域是灰色（有意思的事情就发生在这里，尤其是在头发和毛发周围）。</p>"))
P(("<h3>The processing pipeline</h3>", "<h3>处理流水线</h3>"))
P(("<p>In practice, here's what goes on when you hit \"upload\":</p>",
   "<p>实际上，当你点击\u201c上传\u201d时，会发生这些事：</p>"))
P(("<li>Your image gets shrunk to a size the model can handle — usually around 320×320 or 512×512. That sounds tiny, but the model doesn't need full resolution to figure out where the subject is.</li>",
   "<li>你的图像会被缩小到模型能处理的尺寸——通常是 320×320 或 512×512 左右。听起来很小，但模型不需要全分辨率就能判断主体在哪里。</li>"))
P(("<li>The neural network runs its analysis and spits out a segmentation mask. This is the rough cutout.</li>",
   "<li>神经网络运行分析并输出一张分割蒙版。这就是粗略的抠图。</li>"))
P(("<li>A post-processing step cleans up the mask. This is where alpha matting comes in — it smooths out the rough edges, especially in tricky areas like hair strands, semi-transparent fabric, or fuzzy textures.</li>",
   "<li>后处理步骤会清理蒙版。这里就用到了 alpha 抠图——它能平滑粗糙的边缘，尤其是在发丝、半透明织物或绒毛纹理等棘手区域。</li>"))
P(("<li>Finally, the mask gets scaled back up to your original image resolution and applied. The result is your subject on a transparent background, saved as a PNG.</li>",
   "<li>最后，蒙版会被放大回你原始图像的分辨率并应用。结果就是你的主体呈现在透明背景上，保存为 PNG。</li>"))
P(("<h3>Browser vs. cloud — does it matter?</h3>", "<h3>浏览器 vs. 云端——重要吗？</h3>"))
P(("<p>Most background removers are cloud-based: you upload your image, their server processes it, and they send the result back. It works fine, but it means your photo sits on their server for at least a little while. What happens to it after? How long is it stored? Is it used for training? The answers vary by company, and they're usually buried in a privacy policy nobody reads.</p>",
   "<p>大多数抠图工具是基于云端的：你上传图像，他们的服务器处理它，然后把结果发回来。用起来没问题，但这意味着你的照片会在他们的服务器上至少存放一小段时间。之后会怎样？会存多久？会不会用于训练？答案因公司而异，而且通常埋在没人读的隐私政策里。</p>"))
P(("<p>The other approach — the one SmartImgKit goes with — runs the entire model inside your browser. Your image never gets uploaded anywhere. The trade-off is that the first load takes a few seconds longer because the browser has to download the model file (around 30-80 MB), but after that it's cached locally and subsequent runs are fast. On a decent computer, processing takes about 3-10 seconds per image.</p>",
   "<p>另一种方法——也就是 SmartImgKit 采用的——是在你的浏览器里运行整个模型。你的图像根本不会被上传到任何地方。代价是首次加载会多花几秒，因为浏览器要先下载模型文件（大约 30-80 MB），但之后就缓存在本地，后续运行很快。在一台还不错的电脑上，每张图片的处理大约需要 3-10 秒。</p>"))
P(("<p>Honestly, for most people, either approach works. But if you're handling anything sensitive — client photos, medical images, internal documents — browser-based processing is the safer bet.</p>",
   "<p>说实话，对大多数人来说，哪种方法都行。但如果你处理的是任何敏感内容——客户照片、医疗图像、内部文档——基于浏览器的处理是更安全的选择。</p>"))
# Section 4
P(("<h2>4. Remove a Background in 30 Seconds</h2>", "<h2>4. 30 秒移除背景</h2>"))
P(("<p>Enough theory. Here's how to actually do it with the <a href=\"/zh/tools/background-remover\">抠图工具</a>. The whole process takes less than 30 seconds once you've used it once.</p>",
   "<p>理论够了。下面是用 <a href=\"/zh/tools/background-remover\">抠图工具</a> 实际操作的步骤。用过一次之后，整个过程不到 30 秒。</p>"))
P(("<h4>Open the tool</h4>", "<h4>打开工具</h4>"))
P(("<p>Go to the <a href=\"/zh/tools/background-remover\">Background Remover page</a>. No login, no download, no \"start your free trial.\" It just works in any modern browser.</p>",
   "<p>前往 <a href=\"/zh/tools/background-remover\">抠图工具页面</a>。不用登录、不用下载、没有\u201c免费试用\u201d的套路。在任何现代浏览器里都能直接用。</p>"))
P(("<h4>Drop your image</h4>", "<h4>拖入你的图片</h4>"))
P(("<p>Click the upload area or drag a file onto it. PNG, JPEG, and WebP all work. The limit is 10 MB per image, which should be more than enough unless you're working with raw camera files.</p>",
   "<p>点击上传区域，或把文件拖到上面。PNG、JPEG 和 WebP 都可以。每张图片限制 10 MB，除非你处理的是相机原始文件，否则应该绰绰有余。</p>"))
P(("<h4>Wait a few seconds</h4>", "<h4>等几秒钟</h4>"))
P(("<p>On your first visit, the AI model needs to download (30-80 MB). After that it's cached, so repeat uses are nearly instant. The actual processing takes 3-10 seconds depending on your machine.</p>",
   "<p>首次访问时，AI 模型需要下载（30-80 MB）。之后就会缓存，所以重复使用几乎是即时的。实际处理需要 3-10 秒，取决于你的机器。</p>"))
P(("<h4>Check the preview</h4>", "<h4>检查预览</h4>"))
P(("<p>You'll see your subject on a checkerboard background (that's the standard way editors show transparency). Zoom in and check the edges — hair, ears, fingers — these are the spots where AI sometimes struggles.</p>",
   "<p>你会看到你的主体呈现在棋盘格背景上（这是编辑器显示透明度的标准方式）。放大检查边缘——头发、耳朵、手指——这些是 AI 有时会出问题的地方。</p>"))
P(("<h4>Download</h4>", "<h4>下载</h4>"))
P(("<p>Hit the download button and you get a PNG with a transparent background. Drop it into Canva, Photoshop, Figma, PowerPoint — whatever you're using. It just works.</p>",
   "<p>点击下载按钮，你就会得到一张背景透明的 PNG。把它放进 Canva、Photoshop、Figma、PowerPoint——无论你用什么。直接就能用。</p>"))
# Section 5
P(("<h2>5. Getting Better Results: Tips That Actually Help</h2>", "<h2>5. 获得更好效果：真正有用的技巧</h2>"))
P(("<p>AI background removal is good, but it's not magic. Here are the things that make the biggest difference in my experience:</p>",
   "<p>AI 移除背景很好用，但不是魔法。以下是我的经验中影响最大的几件事：</p>"))
P(("<h3>When you're taking the photo</h3>", "<h3>拍照的时候</h3>"))
P(("<p>Lighting matters more than anything else. If your subject is evenly lit and the background is clearly different in brightness or color, the AI will nail it almost every time. Problems show up when you've got harsh shadows, heavy backlighting, or a subject that's basically the same color as the background (dark jacket against a dark wall, for instance).</p>",
   "<p>光线比什么都重要。如果主体受光均匀，背景在亮度或颜色上明显不同，AI 几乎每次都能搞定。当你有强烈的阴影、严重的逆光，或者主体和背景颜色基本相同（比如深色外套靠着深色墙壁）时，问题就出现了。</p>"))
P(("<p>Resolution helps too. A 3000×3000 photo gives the model way more to work with than a 300×300 screenshot. The AI still processes a downscaled version, but it uses the full resolution for the final output, so more pixels means cleaner edges.</p>",
   "<p>分辨率也有帮助。一张 3000×3000 的照片给模型提供的素材远多于 300×300 的截图。AI 仍然处理缩小版，但最终输出使用全分辨率，所以像素越多边缘越干净。</p>"))
P(("<p>And here's something people don't think about: if you're photographing multiple objects, spread them out. When things overlap, the AI sometimes can't tell where one ends and the other begins. Give it some space to work with.</p>",
   "<p>还有一点大家想不到：如果你要拍多个物体，把它们分散开。当东西重叠时，AI 有时分不清哪里是一个的结尾、哪里是另一个的开始。给它留点工作空间。</p>"))
P(("<h3>After processing</h3>", "<h3>处理之后</h3>"))
P(("<p>Always zoom in to 200-300% and check the edges. Hair and fur are the usual suspects — sometimes the AI does an amazing job, sometimes it leaves a faint halo. If you see one, try placing a bright, contrasting color behind the cutout (create a colored layer in your editor). That makes any remaining artifacts or semi-transparent fringe immediately visible.</p>",
   "<p>总是放大到 200-300% 检查边缘。头发和毛发是常见的重灾区——有时 AI 做得极好，有时会留下一圈淡淡的光晕。如果看到光晕，试着在抠图后面放一种明亮、对比强烈的颜色（在编辑器里建一个彩色图层）。这样任何残留的伪影或半透明的毛边就会立刻显现。</p>"))
P(("<p>For anything client-facing, I treat the AI output as a 95% solution and do a quick manual pass in Photoshop for the last 5%. It's still way faster than doing the whole thing manually. This worked for me, but you might find a different way.</p>",
   "<p>对于任何要给客户看的东西，我把 AI 的输出当作 95% 的方案，然后在 Photoshop 里快速手动修最后 5%。这仍然比全部手动做快得多。这对我管用，但你可能会找到别的方法。</p>"))
P(("<p>Oh, and one more thing: transparent PNGs can get big. If you're putting the result on a website, run it through a <a href=\"/zh/tools/compressor\">compressor</a> first. A 2 MB PNG is overkill for a product thumbnail.</p>",
   "<p>哦，还有一件事：透明 PNG 可能会很大。如果你要把结果放到网站上，先过一遍 <a href=\"/zh/tools/compressor\">压缩器</a>。一张 2 MB 的 PNG 用作产品缩略图太过了。</p>"))
# Section 6
P(("<h2>6. Real-World Use Cases</h2>", "<h2>6. 实际使用场景</h2>"))
P(("<p>The right approach depends on what you're actually doing. Here are the scenarios I run into most often:</p>",
   "<p>正确的方法取决于你实际在做什么。以下是我最常遇到的场景：</p>"))
P(("<h3>🛒 Product photos for online stores</h3>", "<h3>🛒 网店产品图</h3>"))
P(("<p>Amazon, Shopify, and most other platforms want either a pure white background or a transparent PNG. After removing the background, place the product on a white canvas and make sure it fills about 85% of the frame with even spacing. If the platform has specific size requirements (Amazon wants at least 1000×1000), use a <a href=\"/zh/tools/resizer\">resizer</a> to match.</p>",
   "<p>Amazon、Shopify 和大多数其他平台都要求纯白背景或透明 PNG。移除背景后，把产品放在白色画布上，确保它填充大约 85% 的画面且间距均匀。如果平台有特定尺寸要求（Amazon 要求至少 1000×1000），用 <a href=\"/zh/tools/resizer\">缩放工具</a> 来匹配。</p>"))
P(("<h3>📱 Social media profile pictures</h3>", "<h3>📱 社交媒体头像</h3>"))
P(("<p>For circular profile pictures, center the subject with plenty of headroom before you remove the background. Then crop to a square (1:1) using a <a href=\"/zh/tools/cropper\">cropper</a>. A solid color background usually looks better than transparency for profile pics since most platforms don't support transparent avatars anyway.</p>",
   "<p>对于圆形头像，在移除背景前先把主体居中并留出充足的头部空间。然后用 <a href=\"/zh/tools/cropper\">裁剪工具</a> 裁剪成正方形（1:1）。对于头像来说，纯色背景通常比透明背景更好看，因为大多数平台本来就不支持透明头像。</p>"))
P(("<h3>🎨 Design compositing</h3>", "<h3>🎨 设计合成</h3>"))
P(("<p>Save as a transparent PNG for maximum flexibility in your design tool. For subjects with complex edges — hair, fur, translucent fabric — the alpha channel in the PNG preserves those soft, semi-transparent transitions. This is where the AI's alpha matting really shines compared to a hard-edge cutout.</p>",
   "<p>保存为透明 PNG，以便在设计工具中获得最大的灵活性。对于边缘复杂的主体——头发、毛发、半透明织物——PNG 中的 alpha 通道能保留那些柔和、半透明的过渡。相比硬边缘抠图，这就是 AI 的 alpha 抠图真正出彩的地方。</p>"))
P(("<h3>🖼️ Presentation slides</h3>", "<h3>🖼️ 演示文稿幻灯片</h3>"))
P(("<p>Nothing makes a slide deck look more polished than images that are properly cut out. A logo or person floating on the slide background beats a rectangular photo with a white box around it every time. After removing the background, <a href=\"/zh/tools/converter\">convert to PNG</a> if it isn't already — JPEG doesn't support transparency.</p>",
   "<p>没有什么比抠得干净的图片更能让幻灯片显得精致。一个 logo 或人物浮在幻灯片背景上，每次都能胜过一张带白框的矩形照片。移除背景后，如果还不是 PNG 就 <a href=\"/zh/tools/converter\">转换为 PNG</a>——JPEG 不支持透明度。</p>"))
# Section 7
P(("<h2>7. Picking the Right Tool</h2>", "<h2>7. 挑选合适的工具</h2>"))
P(("<p>There are a lot of background removal tools out there now, and they're not all created equal. Here's what I'd look at:</p>",
   "<p>现在市面上有很多抠图工具，但它们并非都一样好用。以下是我会关注的点：</p>"))
P(("<h3>Privacy</h3>", "<h3>隐私</h3>"))
P(("<p>This is the thing most people don't think about until it's too late. When you upload a photo to a cloud-based tool, it's sitting on their server. Most companies say they delete it after processing, but can you verify that? Is the image used to improve their model? The terms of service might tell you, but who actually reads those? If you're working with anything you wouldn't want a stranger seeing — client assets, personal photos, internal documents — browser-based tools are the way to go. SmartImgKit runs everything locally, so your image literally never leaves your machine.</p>",
   "<p>这是大多数人直到为时已晚才会想到的事。当你把照片上传到云端工具时，它就存放在他们的服务器上。大多数公司说处理后会删除，但你能核实吗？图像会被用来改进他们的模型吗？服务条款可能会告诉你，但谁真的会读那些？如果你处理的是任何不想让陌生人看到的东西——客户资产、个人照片、内部文档——基于浏览器的工具才是正道。SmartImgKit 完全在本地运行，你的图像真的永远不会离开你的机器。</p>"))
P(("<h3>Price</h3>", "<h3>价格</h3>"))
P(("<p>Some tools let you process 1-3 images for free, then hit you with a paywall. Subscriptions typically run $5-30/month. That adds up over a year. SmartImgKit is free with no limits — no credits, no watermarks, no \"upgrade to pro\" nudges. It can afford to be free because the processing happens on your device, not on expensive cloud GPUs.</p>",
   "<p>有些工具让你免费处理 1-3 张图片，然后就弹出付费墙。订阅通常每月 5-30 美元。一年下来不少钱。SmartImgKit 免费且无限制——没有积分、没有水印、没有\u201c升级到专业版\u201d的催促。它能免费是因为处理在你的设备上完成，而不是在昂贵的云端 GPU 上。</p>"))
P(("<h3>Quality</h3>", "<h3>质量</h3>"))
P(("<p>The AI model makes or breaks the experience. Older models produce blocky edges, miss fine details like individual hair strands, or fail completely on complex backgrounds. Newer models (U2-Net, IS-Net, RMBG-1.4) handle these cases much better. The difference is especially noticeable on challenging subjects — people with curly hair, products with thin wires or transparent parts, photos shot against busy backgrounds.</p>",
   "<p>AI 模型决定了体验的好坏。旧模型会产生块状边缘，漏掉单根发丝这样的细节，或在复杂背景上完全失败。新模型（U2-Net、IS-Net、RMBG-1.4）处理这些情况好得多。这种差异在棘手的主体上尤其明显——卷发的人、带细线或透明部件的产品、在杂乱背景下拍摄的照片。</p>"))
P(("<h3>Speed</h3>", "<h3>速度</h3>"))
P(("<p>Cloud tools are usually fast (2-5 seconds), but they depend on your internet connection and how busy their servers are. Browser-based tools are slower the first time (model download) but often faster on repeat uses because there's no network round-trip. On a modern laptop, I consistently get results in under 10 seconds.</p>",
   "<p>云端工具通常很快（2-5 秒），但取决于你的网络连接和他们服务器的繁忙程度。基于浏览器的工具首次较慢（模型下载），但重复使用时往往更快，因为没有网络往返。在一台现代笔记本上，我稳定地在 10 秒内得到结果。</p>"))
P(("<h3>Simplicity</h3>", "<h3>简洁</h3>"))
P(("<p>Some tools throw a bunch of options at you — edge smoothing sliders, manual touch-up brushes, batch processing. Those are great if you need them, but for most people, the simpler the better. Upload, process, download. Done. If a tool makes you create an account before you can even try it, that's a red flag.</p>",
   "<p>有些工具向你扔一大堆选项——边缘平滑滑块、手动修补画笔、批量处理。如果你需要这些，那很好，但对大多数人来说，越简单越好。上传、处理、下载。搞定。如果某个工具让你先创建账号才能试用，那就是个危险信号。</p>"))
# when-not-to
P(("<h2>When NOT to Use a Background Remover</h2>", "<h2>什么时候不该用抠图工具</h2>"))
P(("<p>AI background removal is a real time-saver, but it's not magic. Skip it (or use it carefully) in these cases:</p>",
   "<p>AI 移除背景确实很省时间，但它不是魔法。在以下情况请跳过（或谨慎使用）：</p>"))
P(("<li><strong>Complex fine details:</strong> Thin hair against a similar-toned background, chain-link fences, glass, or fur close in color to the background. The AI will give it its best shot, but you'll likely need manual cleanup in Photoshop. Still way faster than doing it from scratch.</li>",
   "<li><strong>复杂的精细细节：</strong>与背景色调相近的细发、铁丝网、玻璃，或颜色与背景接近的毛发。AI 会尽力而为，但你很可能需要在 Photoshop 里手动清理。仍然比从零开始做快得多。</li>"))
P(("<li><strong>Group photos with people touching:</strong> When two people overlap or hug, the AI sometimes erases part of one subject. You can fix it manually, but if the whole point was a \"one-click\" solution, it'll frustrate you.</li>",
   "<li><strong>人物有接触的合影：</strong>当两个人重叠或拥抱时，AI 有时会擦除其中一个主体的一部分。你可以手动修复，但如果你的初衷是\u201c一键\u201d解决，这会让你很挫败。</li>"))
P(("<li><strong>Legal/medical/scientific images:</strong> Anything where pixel-perfect accuracy matters. AI is great for casual use, not for court evidence or medical imaging.</li>",
   "<li><strong>法律、医疗、科学图像：</strong>任何要求像素级精确的情况。AI 适合日常使用，不适合法庭证据或医疗成像。</li>"))
P(("<li><strong>Brand logos with subtle anti-aliasing:</strong> Removing the background can leave weird halos around the edges. Use a vector version of the logo if you have one.</li>",
   "<li><strong>带细微抗锯齿的品牌 logo：</strong>移除背景可能在边缘留下奇怪的光晕。如果有的话，用 logo 的矢量版本。</li>"))
P(("<p>For everything else — product photos, profile pictures, social media graphics, presentation slides, school projects — AI background removal is genuinely the fastest method. It gets it right 19 out of 20 times, and even when it doesn't, you only spend a minute in touch-up instead of the 30 minutes the Pen Tool used to take.</p>",
   "<p>对于其他一切——产品图、头像、社交媒体图片、演示幻灯片、学校作业——AI 移除背景确实是最快的方法。它 20 次里能做对 19 次，即使做错了，你也只需花一分钟修补，而不是钢笔工具过去要花的 30 分钟。</p>"))
# CTA
P(("<h3>Give It a Shot</h3>", "<h3>试一试</h3>"))
P(("<p>Remove a background from any image — takes about 10 seconds, no signup, completely free.</p>",
   "<p>从任何图片移除背景——大约 10 秒，不用注册，完全免费。</p>"))
P((">Try Background Remover \u2192<", ">试试抠图工具 \u2192<"))
# FAQ
P((">Is AI background removal actually accurate?<", ">AI 移除背景真的准确吗？<"))
P((">Modern AI tools (trained on millions of images) are accurate on 90%+ of photos with clear subject-background separation. Hair, fur, and transparent objects are still hard — the AI has to guess. I tested this on 17 product photos and 12 came out perfect, 3 needed minor touch-up, 2 had visible artifacts. For product shots, it's a huge time saver. For hair/fur, expect to do some manual cleanup. The part I always forget: high-contrast backgrounds give the best results.<",
   ">现代 AI 工具（用数百万张图像训练）在主体与背景分离清晰的 90% 以上的照片上都很准确。头发、毛发和透明物体仍然很难——AI 得靠猜。我在 17 张产品图上测试过，12 张完美，3 张需要少量修补，2 张有明显伪影。对于产品拍摄，它省了大量时间。对于头发和毛发，预计要做一些手动清理。我老忘的一点：高对比度背景效果最好。<"))
P((">What file format should I save the cutout as?<", ">抠图该保存成什么格式？<"))
P((">PNG for transparency (lossless, supports alpha channel). JPEG if you don't need transparency and want smaller files (the background becomes white). WebP is a modern alternative. For most uses, PNG with transparency is the right call. By the way, Photoshop PSD if you want to keep an editable layer mask. Yeah, I know that sounds obvious, but people keep asking.<",
   ">PNG 用于透明（无损，支持 alpha 通道）。如果不需要透明且想要更小的文件就用 JPEG（背景会变白）。WebP 是一个现代替代方案。对于大多数用途，带透明度的 PNG 是正确选择。顺便说一句，如果你想保留可编辑的图层蒙版就用 Photoshop PSD。是的，我知道这听起来很明显，但大家一直问。<"))
P((">Can I remove a background from a low-res image?<", ">可以从低分辨率图片移除背景吗？<"))
P((">Yes, but the result depends on the AI tool. Most modern tools can handle low-res images, but the output will still be low-res. If you need a high-res cutout, start with the highest-res original you have. The part I always forget: AI can't add resolution that wasn't there. So upscale first if needed, then remove background.<",
   ">可以，但结果取决于 AI 工具。大多数现代工具能处理低分辨率图片，但输出仍然是低分辨率。如果你需要高分辨率抠图，就从你拥有的最高分辨率原图开始。我老忘的一点：AI 无法凭空增加不存在的分辨率。所以需要的话先放大，再移除背景。<"))
P((">How do I get clean edges on hair?<", ">怎样让头发边缘干净？<"))
P((">Three tricks: (1) use a tool with a \"refine edge\" or \"hair\" mode, (2) shoot the original photo against a high-contrast background (solid color, not busy), (3) use a brush to manually clean up remaining artifacts. Honestly, even the best AI tools struggle with flyaway hair. Plan for 30-60 seconds of touch-up time on portrait shots.<",
   ">三个技巧：（1）用带\u201c精修边缘\u201d或\u201c头发\u201d模式的工具，（2）在高对比度背景下拍摄原图（纯色，不要杂乱），（3）用画笔手动清理残留伪影。说实话，即使是最好的 AI 工具也会在飘飞的头发上犯难。人像拍摄预计要 30-60 秒的修补时间。<"))
P((">Is there a free background remover?<", ">有免费的抠图工具吗？<"))
P((">Yes — browser-based tools like SmartImgKit's remover process locally and are free. Cloud-based tools (remove.bg, PhotoRoom) have free tiers with limits. For occasional use, browser tools are the obvious pick. For high-volume commercial use, the paid services are faster and have more features. By the way, this worked for me, but you might find a different way depending on your workflow.<",
   ">有——像 SmartImgKit 抠图工具这样基于浏览器的工具在本地处理且免费。云端工具（remove.bg、PhotoRoom）有带限制的免费档。偶尔使用的话，浏览器工具是显而易见的选择。对于大批量商业用途，付费服务更快、功能更多。顺便说一句，这对我管用，但根据你的工作流你可能会找到别的方法。<"))
# author-bio (link uses single quotes)
P(("<p style=\"margin:0;\">Casey Morgan runs a small e-commerce store and cuts out product photos weekly. Wrote this guide based on real trial-and-error with actual files — including one truly cursed photo of a cat on a beige carpet. More image tips on the <a href='/zh/blog/'>SmartImgKit 博客</a>.</p>",
   "<p style=\"margin:0;\">Casey Morgan 经营着一家小电商店，每周都要抠产品图。本指南基于真实文件的实际试错写成——包括一张真正让人崩溃的、米色地毯上的猫的照片。更多图像技巧见 <a href='/zh/blog/'>SmartImgKit 博客</a>。</p>"))
# related tools
P((">Image Compressor<", ">图片压缩器<"))
P((">Format Converter<", ">图像格式转换器<"))
P((">Image Resizer<", ">图像缩放工具<"))
P((">Image Cropper<", ">裁剪工具<"))

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
