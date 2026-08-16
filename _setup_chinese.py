#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set up Chinese (zh) language version for SmartImgKit.

Creates:
  - zh/index.html  (Chinese homepage shell, tool cards link to /zh/tools/...)
  - zh/tools/*.html (copy of English tools with lang=zh, zh hreflang, translated title/h1/desc)
  - zh/blog/index.html (Chinese blog index)
Also updates _redirects (remove /zh redirect) — run _generate_sitemaps.py separately for sitemaps.
"""

import os
import re
import shutil

BASE = r'E:\网站项目\smartimgkit'
ZH = os.path.join(BASE, 'zh')

# ── Homepage shell translations (UI chrome only; tool card text stays English) ──
HOME_REPLACE = [
    # <head>
    ('<html lang="en" data-theme="dark">', '<html lang="zh" data-theme="dark">'),
    ('<title>SmartImgKit — Free Online AI Image Tools</title>',
     '<title>SmartImgKit — 免费在线 AI 图像工具</title>'),
    ('<meta name="description" content="SmartImgKit offers free AI-powered image tools: background remover, compressor, converter, resizer, cropper, watermark, color palette, base64, face blur, HEIC converter, metadata viewer, AVIF support, GIF editor, PDF to image converter. 100% browser-based. No uploads, no registration.">',
     '<meta name="description" content="SmartImgKit 提供免费 AI 图像工具：抠图、压缩、格式转换、缩放、裁剪、加水印、取色、Base64、人脸打码、HEIC 转换、元数据查看、AVIF 支持、GIF 编辑、PDF 转图片等。100% 浏览器端处理，无需上传，无需注册。">'),
    ('<link rel="canonical" href="https://smartimgkit.com/">',
     '<link rel="canonical" href="https://smartimgkit.com/zh/">'),
    # hreflang: add zh
    ('  <link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/">\n</head>',
     '  <link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/">\n  <link rel="alternate" hreflang="zh" href="https://smartimgkit.com/zh/">\n</head>'),
    # nav
    ('<a href="/" class="logo">\n      <span class="logo-icon">🎨</span>\n      <span class="logo-text">SmartImgKit</span>\n    </a>',
     '<a href="/zh/" class="logo">\n      <span class="logo-icon">🎨</span>\n      <span class="logo-text">SmartImgKit</span>\n    </a>'),
    ('<a href="/">Home</a>', '<a href="/zh/">首页</a>'),
    ('<a href="/tools/background-remover">Tools</a>', '<a href="/zh/tools/background-remover">工具</a>'),
    ('<a href="/workflows/">Workflows</a>', '<a href="/workflows/">工作流</a>'),
    ('<a href="/blog/">Blog</a>', '<a href="/zh/blog/">博客</a>'),
    ('<a href="/about">About</a>', '<a href="/about">关于</a>'),
    ('<a href="/contact">Contact</a>', '<a href="/contact">联系</a>'),
    # lang button default flag
    ('<span class="lang-flag">🇬🇧</span>\n            <span class="lang-name">EN</span>',
     '<span class="lang-flag">🇨🇳</span>\n            <span class="lang-name">ZH</span>'),
    # hero
    ('<h1 class="hero-title">Free AI-Powered<br><span class="gradient-text">Image Tools</span></h1>',
     '<h1 class="hero-title">免费 AI 驱动的<br><span class="gradient-text">图像工具</span></h1>'),
    ('<p class="hero-desc">Compress, convert, resize, crop, watermark, remove backgrounds, extract colors, and more — all in your browser. No uploads to external servers. 100% free, no registration required, privacy-first by design.</p>',
     '<p class="hero-desc">压缩、转换、缩放、裁剪、加水印、抠图、取色等——全部在浏览器中完成。无需上传到外部服务器。100% 免费，无需注册，隐私优先。</p>'),
    ('<a href="#tools" class="btn btn-primary">Explore Tools</a>', '<a href="#tools" class="btn btn-primary">浏览工具</a>'),
    ('<a href="/about" class="btn btn-secondary">Learn More</a>', '<a href="/about" class="btn btn-secondary">了解更多</a>'),
    ('<a href="/privacy" class="badge">🔒 Privacy First</a>', '<a href="/privacy" class="badge">🔒 隐私优先</a>'),
    ('<a href="/about" class="badge">⚡ Browser-Based</a>', '<a href="/about" class="badge">⚡ 浏览器端</a>'),
    ('<a href="/about" class="badge">💯 Free Forever</a>', '<a href="/about" class="badge">💯 永久免费</a>'),
    ('<a href="/about" class="badge">🚀 No Signup</a>', '<a href="/about" class="badge">🚀 无需注册</a>'),
    # tools section header
    ('<h2>All Tools</h2>', '<h2>全部工具</h2>'),
    ('<p>Powerful, easy-to-use tools that run entirely in your browser. No installs, no uploads, no tracking.</p>',
     '<p>强大易用的工具，完全在浏览器中运行。无需安装，无需上传，无需追踪。</p>'),
    # category headers
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📊 Optimize & Convert</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📊 优化与转换</h3>'),
    ('<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Compress, convert formats, and optimize images for web.</p>',
     '<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">压缩、转换格式、为网页优化图像。</p>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✂️ Resize & Crop</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✂️ 缩放与裁剪</h3>'),
    ('<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Resize, crop, and split images to any size.</p>',
     '<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">缩放、裁剪、拆分图像到任意尺寸。</p>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎨 Edit & Effects</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎨 编辑与特效</h3>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🤖 AI Enhance</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🤖 AI 增强</h3>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✨ Create & Design</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">✨ 创作与设计</h3>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🛠️ Utility & Analyze</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🛠️ 实用与分析</h3>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📝 Text & Developer Tools</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📝 文本与开发者工具</h3>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📄 PDF Tools</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">📄 PDF 工具</h3>'),
    ('<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Merge, split, compress, rotate, and edit PDF files in your browser.</p>',
     '<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">在浏览器中合并、拆分、压缩、旋转和编辑 PDF 文件。</p>'),
    ('<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎬 Video Tools</h3>',
     '<h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">🎬 视频工具</h3>'),
    ('<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">Compress, convert, trim, and edit videos with ffmpeg.wasm in your browser.</p>',
     '<p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">使用 ffmpeg.wasm 在浏览器中压缩、转换、剪辑和编辑视频。</p>'),
    # localize tool card links /tools/ -> /zh/tools/
    # (done via regex below)
    # features section
    ('<h2>Why SmartImgKit?</h2>', '<h2>为什么选择 SmartImgKit？</h2>'),
    ('<p>We built SmartImgKit with three core principles: privacy, speed, and simplicity.</p>',
     '<p>SmartImgKit 基于三大核心原则构建：隐私、速度与简洁。</p>'),
    ('<h3>Privacy First</h3>', '<h3>隐私优先</h3>'),
    ('<h3>Lightning Fast</h3>', '<h3>极速处理</h3>'),
    ('<h3>Privacy First</h3>\n            <p>All processing happens in your browser. Your images never leave your device, are never uploaded to our servers, and are never stored or analyzed. We can\'t see your images — because we never receive them. This is the most secure way to process sensitive or personal images online.</p>',
     '<h3>隐私优先</h3>\n            <p>所有处理都在你的浏览器中完成。图像永远不会离开你的设备，永远不会上传到我们的服务器，也永远不会被存储或分析。我们看不到你的图像——因为我们从未接收过。这是在线处理敏感或个人图像最安全的方式。</p>'),
    # footer
    ('<p>Free AI-powered image tools that respect your privacy. All processing happens in your browser — your images never leave your device.</p>',
     '<p>尊重隐私的免费 AI 图像工具。所有处理都在浏览器中完成——图像永远不会离开你的设备。</p>'),
    ('<h4>Top Tools</h4>', '<h4>热门工具</h4>'),
    ('<h4>More Tools</h4>', '<h4>更多工具</h4>'),
    ('<h4>Legal</h4>', '<h4>法律信息</h4>'),
    ('<a href="/privacy">Privacy Policy</a>', '<a href="/privacy">隐私政策</a>'),
    ('<a href="/terms">Terms of Service</a>', '<a href="/terms">服务条款</a>'),
    ('<a href="/cookie-policy">Cookie Policy</a>', '<a href="/cookie-policy">Cookie 政策</a>'),
    ('<a href="/contact">Contact</a>', '<a href="/contact">联系我们</a>'),
    # footer lang links: add ZH
    ('<a href="/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">EN</a>\n        <a href="/es/"',
     '<a href="/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">EN</a>\n        <a href="/zh/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;font-weight:700;">ZH</a>\n        <a href="/es/"'),
]

# ── Tool page SEO translations: slug -> (zh_title, zh_h1, zh_desc) ──
# Covers title, h1, meta description, and og:description for each tool.
TOOL_ZH = {
    'image-compressor': ('图像压缩器 – 免费在线图片压缩', '🗜️ 图像压缩器', '免费在线图像压缩器。在无明显画质损失下缩小 JPG、PNG、WebP 文件体积。100% 浏览器端，不上传服务器。'),
    'compressor': ('图片压缩器 – 免费在线压缩', '🗜️ 图片压缩器', '免费在线压缩图片。支持 JPG、PNG、WebP，可调节压缩级别。浏览器端处理，隐私优先。'),
    'converter': ('图像格式转换器 – 免费在线', '🔄 图像格式转换器', '在线免费转换 JPG、PNG、WebP、GIF、BMP、TIFF 格式。支持批量转换。'),
    'heic-converter': ('HEIC 转换器 – 免费', '🖼️ HEIC 转换器', '将 HEIC（iPhone 照片）转换为 JPG、PNG 或 WebP。免费，浏览器端，不上传。'),
    'pdf-to-image': ('PDF 转图片 – 免费', '📄 PDF 转图片', '将 PDF 页面转换为 PNG、JPG 或 WebP 图片。每页可 1x-3x 缩放渲染。基于 pdf.js。'),
    'svg-to-png': ('SVG 转 PNG – 免费', '📐 SVG 转 PNG', '将 SVG 矢量文件转换为 PNG、JPG 或 WebP。1x-4x 高质量栅格化。'),
    'avif-support': ('AVIF 支持 – 免费', '🅰 AVIF 支持', '检测浏览器 AVIF 支持，解码 AVIF 图像并转换为 JPG/PNG/WebP。'),
    'image-to-pdf': ('图片转 PDF – 免费', '📄 图片转 PDF', '将多张图片合并为单个 PDF 文件。可选页面大小、边距和方向。100% 浏览器端。'),
    'pdf-merge': ('PDF 合并 – 免费', '🔗 PDF 合并', '将多个 PDF 文件合并为单个 PDF。按选择顺序合并。全部在浏览器中完成。'),
    'pdf-split': ('PDF 拆分 – 免费', '✂️ PDF 拆分器', '将 PDF 拆分为多个文件。可选每 N 页、指定页面范围或每页单独拆分。'),
    'pdf-compress': ('PDF 压缩 – 免费', '🗜️ PDF 压缩器', '通过优化内容、扁平化注释和移除多余元数据来减小 PDF 体积。浏览器端。'),
    'pdf-delete-pages': ('PDF 删除页面 – 免费', '🗑️ PDF 删除页面', '从 PDF 中删除指定页面或页面范围。输入如"2, 5-7, 10"的页码即可删除。'),
    'pdf-rotate': ('PDF 旋转 – 免费', '🔄 PDF 旋转器', '将 PDF 页面旋转 90°、180° 或 270°。可应用于全部或指定页面。浏览器端，不上传。'),
    'pdf-extract-pages': ('PDF 提取页面 – 免费', '📑 PDF 提取页面', '从 PDF 中提取指定页面或范围生成新 PDF。只保留所需页面。隐私优先。'),
    'background-remover': ('抠图工具 – 免费 AI 去背景', '🎨 AI 抠图工具', '免费 AI 在线抠图，自动去除图片背景。100% 浏览器端处理，不上传，无需注册。'),
    'resizer': ('图像缩放工具 – 免费', '📐 图像缩放工具', '按像素或百分比缩放图像。保持比例或自由裁剪。支持批量缩放。'),
    'cropper': ('图像裁剪器 – 免费', '🖼️ 图像裁剪器', '自由裁剪和预设比例裁剪。适合社媒尺寸（Instagram、Facebook、Twitter、LinkedIn）。'),
    'watermark': ('水印工具 – 免费', '🔏 水印工具', '为图片添加文字或图片水印以保护作品。可控制位置、透明度、大小和颜色。'),
    'image-filters': ('图像滤镜 – 免费', '🌈 图像滤镜', '为图片应用各种滤镜效果：黑白、棕褐、模糊、锐化、复古等。浏览器端处理。'),
    'text-on-image': ('图片加文字 – 免费', '📝 图片加文字', '在图片上添加文字。可选字体、大小、颜色、位置和透明度。'),
    'meme-generator': ('表情包生成器 – 免费', '😂 表情包生成器', '在线制作表情包。顶部和底部文字，经典 meme 风格。免费，浏览器端。'),
    'gif-editor': ('GIF 编辑器 – 免费', '🎞️ GIF 编辑器', '编辑和创建 GIF 动画。调整速度、裁剪、添加文字。浏览器端处理。'),
    'image-merger': ('图片合并 – 免费', '🧩 图片合并', '将多张图片合并为一张。支持横向、纵向拼接。'),
    'image-rotator': ('图片旋转/翻转 – 免费', '🔄 图片旋转器', '旋转图片 90°、180°、270° 或水平/垂直翻转。'),
    'color-palette': ('取色器 – 免费', '🎨 取色器', '从图片中提取主色调色板。上传图片即可生成配色方案。'),
    'face-blur': ('人脸打码 – 免费', '🙈 人脸打码', '自动检测并模糊图片中的人脸，保护隐私。浏览器端处理。'),
    'screenshot-to-image': ('截图转图片 – 免费', '📸 截图转图片', '将截图转换为各种格式图片。'),
    'image-compare': ('图片对比 – 免费', '🔍 图片对比', '并排对比两张图片的差异。'),
    'base64': ('Base64 编解码 – 免费', '🔐 Base64 编解码', '将图片转换为 Base64 编码或解码。适合开发者嵌入。'),
    'metadata-viewer': ('元数据查看器 – 免费', '📋 元数据查看器', '查看图片的 EXIF 元数据：相机型号、拍摄时间、GPS 等。'),
    'print-resizer': ('打印尺寸缩放 – 免费', '🖨️ 打印尺寸缩放', '按精确 DPI 和纸张尺寸缩放图片。A4、Letter、A5、4×6、名片等。72-600 DPI。'),
    'image-adjust': ('图像调整 – 免费', '🎨 图像调整', '调整亮度、对比度、饱和度、色相等。'),
    'image-border': ('图片加边框 – 免费', '⬜ 图片加边框', '为图片添加边框。可选颜色、宽度、圆角。'),
    'image-flip': ('图片翻转 – 免费', '🔃 图片翻转', '水平或垂直翻转图片。'),
    'image-grayscale': ('图片转灰度 – 免费', '⚫ 图片转灰度', '将彩色图片转换为黑白灰度图。'),
    'image-shadow': ('图片加阴影 – 免费', '🌑 图片加阴影', '为图片添加投影阴影效果。'),
    'image-splitter': ('图片分割 – 免费', '✂️ 图片分割', '将图片分割为多块。可选行列数。'),
    'image-exif-remover': ('EXIF 移除 – 免费', '🚫 EXIF 移除', '移除图片中的 EXIF 元数据以保护隐私。'),
    'circle-crop': ('圆形裁剪 – 免费', '⭕ 圆形裁剪', '将图片裁剪为圆形。适合头像制作。'),
    'favicon-generator': ('Favicon 生成器 – 免费', '⭐ Favicon 生成器', '从图片生成网站 favicon。多种尺寸。'),
    'ocr': ('OCR 文字识别 – 免费', '🔍 OCR 文字识别', '从图片中识别提取文字。支持多语言。浏览器端处理。'),
    'bulk-processor': ('批量处理器 – 免费', '📦 批量处理器', '批量处理多张图片：压缩、转换、缩放等。'),
    'id-photo': ('证件照制作 – 免费', '🪪 证件照制作', '制作标准证件照。多种尺寸和背景色。'),
    'product-white-background': ('商品白底图 – 免费', '🛍️ 商品白底图', '为商品图片添加纯白背景。电商必备。'),
    'social-media-post': ('社媒配图 – 免费', '📱 社媒配图', '制作社交媒体配图。多种平台尺寸。'),
    'photo-restoration': ('老照片修复 – 免费', '🖼️ 老照片修复', 'AI 修复老照片，增强画质。'),
    'image-enhancer': ('图像增强 – 免费', '✨ 图像增强', 'AI 增强图片画质和分辨率。'),
    'image-upscaler': ('图像放大 – 免费', '🔍 图像放大', 'AI 放大图片，提高分辨率不失真。'),
    'beauty-editor': ('美颜编辑器 – 免费', '💄 美颜编辑器', '人像美颜：磨皮、美白、瘦脸等。'),
    'gif-splitter': ('GIF 分割 – 免费', '✂️ GIF 分割', '将 GIF 分割为单帧图片。'),
    'heic-to-jpg': ('HEIC 转 JPG – 免费', '🖼️ HEIC 转 JPG', '将 HEIC 转换为 JPG。简单快速。'),
    'html-encoder': ('HTML 实体编码 – 免费', '🏷️ HTML 实体编码', '将特殊字符编码为 HTML 实体，或反向解码。'),
    'ico-icon-generator': ('ICO 图标生成 – 免费', '⭐ ICO 图标生成', '从图片生成 ICO 图标文件。多种尺寸。'),
    'case-converter': ('大小写转换 – 免费', '🔤 大小写转换', '转换文本大小写：大写、小写、首字母大写等。'),
    'json-formatter': ('JSON 格式化 – 免费', '📋 JSON 格式化', '格式化、美化、压缩 JSON 数据。'),
    'password-generator': ('密码生成器 – 免费', '🔐 密码生成器', '生成强随机密码。可选长度和字符类型。'),
    'qr-code-generator': ('二维码生成器 – 免费', '📱 二维码生成器', '即时生成二维码。免费，在线。'),
    'regex-tester': ('正则测试 – 免费', '🧪 正则测试', '在线测试正则表达式。'),
    'signature-maker': ('签名制作 – 免费', '✍️ 签名制作', '手绘数字签名并下载为透明 PNG。'),
    'text-diff': ('文本对比 – 免费', '🔍 文本对比', '对比两段文本的差异。'),
    'text-find-replace': ('查找替换 – 免费', '✏️ 查找替换', '在文本中查找并替换内容。'),
    'text-sorter': ('文本排序 – 免费', '🔢 文本排序', '对文本行进行排序。'),
    'url-encoder': ('URL 编解码 – 免费', '🔗 URL 编解码', 'URL 编码和解码。'),
    'uuid-generator': ('UUID 生成器 – 免费', '🆔 UUID 生成器', '生成 UUID/GUID。'),
    'word-counter': ('字数统计 – 免费', '📊 字数统计', '统计文本的字数、字符数、行数。'),
    'video-compressor': ('视频压缩 – 免费', '🗜️ 视频压缩器', '调整质量（CRF）和分辨率来减小视频体积。不上传，ffmpeg.wasm 浏览器端处理。'),
    'video-to-gif': ('视频转 GIF – 免费', '🎞️ 视频转 GIF', '将 MP4、WebM 等视频转为 GIF 动画。'),
    'video-to-mp3': ('视频转 MP3 – 免费', '🎵 视频转 MP3', '从视频中提取高质量 MP3 音频。'),
    'video-crop': ('视频裁剪 – 免费', '✂️ 视频裁剪器', '剪辑视频去除不需要的部分。'),
    'video-to-frames': ('视频转帧 – 免费', '🖼️ 视频转帧', '从视频中提取高质量帧图片。'),
    'video-speed': ('视频变速 – 免费', '⏩ 视频变速', '视频加速或减速播放。'),
    'video-rotate': ('视频旋转 – 免费', '🔃 视频旋转器', '旋转视频 90°、180°、270° 或翻转。'),
    # ── Batch 1: PDF conversion tools ──
    'pdf-to-word': ('PDF 转 Word – 免费', '📝 PDF 转 Word', '将 PDF 转换为可编辑的 Word（.docx）。提取每页文本生成整洁的 Word 文档。100% 浏览器端处理。'),
    'pdf-to-excel': ('PDF 转 Excel – 免费', '📊 PDF 转 Excel', '将 PDF 转换为 Excel（.xlsx）。检测表格结构并将文本提取为电子表格行。不上传。'),
    'pdf-to-ppt': ('PDF 转 PPT – 免费', '📑 PDF 转 PowerPoint', '将 PDF 转换为 PowerPoint（.pptx）。每页渲染为高清图片幻灯片。适合演示文稿。'),
    'word-to-pdf': ('Word 转 PDF – 免费', '📄 Word 转 PDF', '将 Word（.docx）转换为 PDF。提取文本和段落，渲染整洁的 PDF。100% 浏览器端处理。'),
    'excel-to-pdf': ('Excel 转 PDF – 免费', '📊 Excel 转 PDF', '将 Excel（.xlsx）转换为 PDF。每个工作表生成一页带自适应表格的 PDF。浏览器端，不上传。'),
}


def localize_tool_links(html):
    """Rewrite /tools/ and /workflows/ links to /zh/ prefixed versions in main content."""
    # tool card links: href="/tools/xxx" -> href="/zh/tools/xxx"
    html = re.sub(r'href="/tools/([^"]*)"', r'href="/zh/tools/\1"', html)
    return html


def build_homepage():
    src = os.path.join(BASE, 'index.html')
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    for old, new in HOME_REPLACE:
        html = html.replace(old, new)
    # localize tool links (after shell replacements so /about etc. are already done)
    html = localize_tool_links(html)
    # ensure lang dropdown includes zh link (add before </div> of dropdown if missing)
    if 'hreflang="zh"' not in html:
        html = html.replace(
            '<a href="/ar/" hreflang="ar"><span>🇸🇦</span> العربية</a>',
            '<a href="/ar/" hreflang="ar"><span>🇸🇦</span> العربية</a>\n            <a href="/zh/" hreflang="zh"><span>🇨🇳</span> 中文</a>'
        )
    os.makedirs(ZH, exist_ok=True)
    with open(os.path.join(ZH, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ zh/index.html created')


def build_tools():
    src_dir = os.path.join(BASE, 'tools')
    dst_dir = os.path.join(ZH, 'tools')
    os.makedirs(dst_dir, exist_ok=True)
    count = 0
    for fname in os.listdir(src_dir):
        if not fname.endswith('.html'):
            continue
        slug = fname[:-5]
        src = os.path.join(src_dir, fname)
        with open(src, 'r', encoding='utf-8') as f:
            html = f.read()
        # lang attribute
        html = html.replace('<html lang="en"', '<html lang="zh"')
        # canonical
        html = re.sub(
            r'<link rel="canonical" href="https://smartimgkit\.com/tools/%s">' % slug,
            '<link rel="canonical" href="https://smartimgkit.com/zh/tools/%s">' % slug,
            html
        )
        # add zh hreflang (after the ar hreflang line which all tools have)
        if 'hreflang="zh"' not in html:
            html = html.replace(
                '<link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/tools/%s">' % slug,
                '<link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/tools/%s">\n  <link rel="alternate" hreflang="zh" href="https://smartimgkit.com/zh/tools/%s">' % (slug, slug)
            )
        # apply SEO translations if available
        if slug in TOOL_ZH:
            zh_title, zh_h1, zh_desc = TOOL_ZH[slug]
            # title: replace content between <title> and </title>
            html = re.sub(r'<title>.*?</title>', '<title>%s | SmartImgKit</title>' % zh_title, html, count=1)
            # meta description
            html = re.sub(r'(<meta name="description" content=").*?(">)', r'\1%s\2' % zh_desc.replace('\\', '\\\\'), html, count=1)
            # og:description
            html = re.sub(r'(<meta property="og:description" content=").*?(">)', r'\1%s\2' % zh_desc.replace('\\', '\\\\'), html, count=1)
            # twitter:description
            html = re.sub(r'(<meta name="twitter:description" content=").*?(">)', r'\1%s\2' % zh_desc.replace('\\', '\\\\'), html, count=1)
            # h1: match the first <h1>...</h1>
            html = re.sub(r'(<h1[^>]*>).*?(</h1>)', r'\1%s\2' % zh_h1, html, count=1)
        # localize internal tool links in nav/footer
        html = html.replace('href="/tools/', 'href="/zh/tools/')
        # logo link
        html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
        # lang dropdown: add zh link
        if 'hreflang="zh"' not in html.split('lang-dropdown')[1] if 'lang-dropdown' in html else True:
            html = html.replace(
                '<a href="/ar/" hreflang="ar" lang="ar">🇸🇦 العربية</a>',
                '<a href="/ar/" hreflang="ar" lang="ar">🇸🇦 العربية</a>\n            <a href="/zh/" hreflang="zh" lang="zh">🇨🇳 中文</a>'
            )
        dst = os.path.join(dst_dir, fname)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
    print('✅ zh/tools/ created: %d tools' % count)


def build_blog_index():
    """Copy blog index from en and localize."""
    src = os.path.join(BASE, 'blog', 'index.html')
    if not os.path.exists(src):
        print('  Skip: blog/index.html not found')
        return
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<html lang="en"', '<html lang="zh"')
    html = html.replace('href="/" class="logo"', 'href="/zh/" class="logo"')
    dst_dir = os.path.join(ZH, 'blog')
    os.makedirs(dst_dir, exist_ok=True)
    with open(os.path.join(dst_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ zh/blog/index.html created')


def update_redirects():
    path = os.path.join(BASE, '_redirects')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove the /zh redirect lines
    content = content.replace('/zh / 301\n', '')
    content = content.replace('/zh/* / 301\n', '')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ _redirects updated (removed /zh redirect)')


def update_english_index():
    """Add zh hreflang + lang switcher link to English index.html."""
    path = os.path.join(BASE, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    changed = False
    if 'hreflang="zh"' not in html:
        html = html.replace(
            '  <link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/">\n</head>',
            '  <link rel="alternate" hreflang="ar" href="https://smartimgkit.com/ar/">\n  <link rel="alternate" hreflang="zh" href="https://smartimgkit.com/zh/">\n</head>'
        )
        changed = True
    if 'href="/zh/" hreflang="zh"' not in html:
        html = html.replace(
            '<a href="/ar/" hreflang="ar"><span>🇸🇦</span> العربية</a>',
            '<a href="/ar/" hreflang="ar"><span>🇸🇦</span> العربية</a>\n            <a href="/zh/" hreflang="zh"><span>🇨🇳</span> 中文</a>'
        )
        changed = True
    # footer lang links
    if '/zh/"' not in html.split('footer-lang')[1] if 'footer-lang' in html else True:
        pass  # handled below
    if 'href="/zh/" style="margin:0 6px' not in html:
        html = html.replace(
            '<a href="/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">EN</a>\n        <a href="/es/"',
            '<a href="/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">EN</a>\n        <a href="/zh/" style="margin:0 6px;color:var(--text-secondary);text-decoration:none;">ZH</a>\n        <a href="/es/"'
        )
        changed = True
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('✅ index.html updated (added zh hreflang + switcher + footer link)')
    else:
        print('  index.html already has zh links')


def main():
    print('=== Setting up Chinese (zh) language version ===\n')
    update_redirects()
    update_english_index()
    build_homepage()
    build_tools()
    build_blog_index()
    print('\n✅ Chinese language setup complete!')
    print('   Next: run _generate_sitemaps.py to include zh in sitemaps.')


if __name__ == '__main__':
    main()
