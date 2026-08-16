#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inject Chinese-translated enrichment sections into zh/tools/*.html.
Preserves existing zh title/h1 translations; adds Chinese selling points,
feature narrative, feature grid, trust badges, and expanded FAQ.
"""
import os, re

BASE = r'E:\网站项目\smartimgkit'
ZH_DIR = os.path.join(BASE, 'zh', 'tools')

# Chinese trust badges (shared)
ZH_TRUST = [
 ('🔒','100% 隐私','文件不离开浏览器'),
 ('⚡','浏览器端','无需安装、不上传'),
 ('💯','永久免费','无需注册、无水印'),
 ('🚀','无需注册','即刻开始，无需账号'),
]

# Chinese category data: feature grids + common FAQs
ZH_CATEGORY = {
 'Optimize & Convert': {
   'features': [('⚡','即时转换','文件上传瞬间即在浏览器内处理——无需排队等待。'),('🔒','100% 隐私','文件从不离开你的设备，全部本地运行。'),('🎯','可调质量','精细调节压缩或输出设置，平衡体积与画质。'),('📦','批量处理','一次处理多个文件并一起下载。'),('🆓','永久免费','无需注册、无水印、无隐藏限制。'),('🌐','跨平台','Windows、Mac、Linux、iOS、Android 任意现代浏览器可用。')],
   'faqs': [('有文件大小限制吗？','支持最大 100MB 的文件。超大文件可能需要多几秒处理。'),('需要安装任何东西吗？','不需要。全部在浏览器内运行——无需应用、插件或扩展。')],
 },
 'Resize & Crop': {
   'features': [('📐','精确尺寸','按精确像素或百分比设置，像素级精准。'),('🔗','锁定比例','自动保持比例，避免拉伸变形。'),('✂️','自由与预设','自由裁剪或使用社交媒体现成的比例预设。'),('🔒','100% 隐私','全部本地处理——图片不离开浏览器。'),('🆓','永久免费','无需注册、无水印、无隐藏限制。'),('🌐','跨平台','任意现代浏览器设备可用。')],
   'faqs': [('缩放会降低画质吗？','缩放使用高质量插值。放大无法添加原图中不存在的细节。'),('可以处理多张图片吗？','可以——缩放和裁剪均支持批量处理。')],
 },
 'Edit & Effects': {
   'features': [('🎨','实时预览','每次调整下载前即时可见。'),('🎚️','精细控制','用精确滑块调节强度、颜色和位置。'),('🔄','无损编辑','原图绝不会被修改——下载的是新副本。'),('🔒','100% 隐私','全部编辑在浏览器本地完成。'),('🆓','永久免费','无需注册、无水印、无限制。'),('⚡','即时出图','编辑即时生效——无需渲染队列。')],
   'faqs': [('编辑可撤销吗？','可以——下载前随时重置为原图。源文件不受影响。'),('所有图片格式都支持吗？','支持 JPG、PNG、WebP 等常见格式。')],
 },
 'AI Enhance': {
   'features': [('🤖','AI 驱动','神经网络在浏览器内运行——无需云端、不上传。'),('⚡','一键出效','自动增强，无需复杂设置。'),('🔒','100% 隐私','照片本地处理，绝不上传。'),('🎯','自然效果','增强保留自然、不夸张的外观。'),('🆓','永久免费','无需注册、无积分、无水印。'),('🌐','跨平台','任意现代浏览器设备可用。')],
   'faqs': [('AI 处理在服务器上吗？','不在。AI 模型完全在浏览器内通过 WebAssembly 和 WebGL 运行。'),('效果不理想怎么办？','AI 增强是起点——可用编辑工具进一步微调。')],
 },
 'Create & Design': {
   'features': [('✍️','完全自定义','控制字体、颜色、尺寸和位置。'),('📐','预设尺寸','从社交媒体和印刷的正确尺寸开始。'),('🎨','实时预览','设计实时更新可见。'),('🔒','100% 隐私','全部设计工作在浏览器本地完成。'),('🆓','永久免费','无需注册、无水印、无限制。'),('📤','导出就绪','即时下载可投入使用的图片。')],
   'faqs': [('可以用自己的图片和字体吗？','可以——上传自己的素材并使用内置字体选项。'),('下载有水印吗？','没有。下载内容干净无水印。')],
 },
 'Utility & Analyze': {
   'features': [('⚡','即时分析','上传或粘贴瞬间即出结果。'),('📋','详细输出','获得精确的统计、代码或对比。'),('🔒','100% 隐私','全部本地分析——不上传任何内容。'),('🔄','无损操作','原文件绝不会被修改。'),('🆓','永久免费','无需注册、无限制、完全免费。'),('🌐','跨平台','任意现代浏览器设备可用。')],
   'faqs': [('分析准确吗？','准确——工具使用标准算法和解析器，结果可靠。'),('可以处理多个文件吗？','可以——在适用时支持批量分析。')],
 },
 'Text & Developer Tools': {
   'features': [('⚡','即时处理','输入即转换、即校验。'),('🧪','开发者级','为准确、符合标准的结果而构建。'),('🔒','100% 隐私','全部本地处理——数据不外传。'),('📋','复制导出','一键复制到剪贴板，方便使用。'),('🆓','永久免费','无需注册、无 API 密钥、无限制。'),('🔧','正则与 JSON','内置完整正则表达式和 JSON 校验。')],
   'faqs': [('这些工具生产环境够用吗？','够用——遵循标准规范（RFC 3986、JSON 规范等）。'),('输入会被存储吗？','不会。全部在浏览器内处理，关闭标签页即丢弃。')],
 },
 'PDF Tools': {
   'features': [('⚡','即时处理','PDF 上传瞬间即在浏览器内处理。'),('🔒','100% 隐私','PDF 从不离开你的设备——不上传服务器。'),('📝','文本型输出','转换产出真实、可搜索、可选中的文本。'),('📄','一站式 PDF 套件','合并、拆分、编辑、批注、转换——25+ PDF 工具。'),('🆓','永久免费','无需注册、无水印、无页数限制。'),('🌐','跨平台','Windows、Mac、Linux、iOS、Android 可用。')],
   'faqs': [('PDF 会上传到服务器吗？','不会。全部通过 pdf-lib 和 pdf.js 在浏览器本地处理。'),('有页数或文件限制吗？','无硬性限制。超大 PDF（100MB+）可能拖慢浏览器。')],
 },
 'Video Tools': {
   'features': [('⚡','浏览器端','视频本地处理——不上传。'),('🎬','常见格式','支持 MP4、WebM 等浏览器可播放格式。'),('✂️','裁剪转换','剪切、旋转、加速、转换视频片段。'),('🔒','100% 隐私','视频从不离开你的设备。'),('🆓','永久免费','无需注册、无水印、无时长限制。'),('🎞️','帧与 GIF 导出','从视频提取帧或制作动画 GIF。')],
   'faqs': [('支持哪些视频格式？','MP4、WebM 等浏览器可播放的格式。处理使用 ffmpeg.wasm。'),('有视频时长限制吗？','无硬性限制，但越长视频耗时越多、内存占用越大。')],
 },
}

# Chinese per-tool data: slug -> (name_zh, cat, tagline_zh, [3 use cases zh], [(Q,A),(Q,A)] tool FAQs)
# name_zh kept close to existing translated h1 where possible.
ZH_TOOLS = {
 'compressor': ('图片压缩器','Optimize & Convert','在不损失可见画质的前提下减小图片体积',['压缩图片以加快网站加载、提升 Core Web Vitals','压缩照片以符合邮件附件大小限制','优化电商商品图片'],[('提供哪些压缩级别？','可从多个质量级别选择——从轻度（近乎无损）到强力压缩以最大缩减体积。'),('压缩会改变图片尺寸吗？','不会。压缩减小文件体积但保持原始像素尺寸。改变尺寸请用缩放工具。')]),
 'image-compressor': ('图片压缩器','Optimize & Convert','可调质量压缩图片文件',['批量压缩照片用于网页发布','为移动页面减轻图片体积','让大图符合上传限制'],[('支持批量压缩吗？','支持——选择多个文件一起处理，各自单独下载。'),('最大能压缩多少？','强力压缩最多可缩小 80%，视原图而定。')]),
 'converter': ('图片格式转换器','Optimize & Convert','即时转换图片格式',['将 PNG 转 JPG 以减小体积','把 JPG 转 WebP 提升现代网页性能','批量转换 HEIC 照片以便跨平台分享'],[('支持哪些格式？','JPG、PNG、WebP、GIF、BMP、TIFF——任意互转。'),('会保留元数据吗？','保留基本元数据；如需清除请用 EXIF 移除工具。')]),
 'heic-converter': ('HEIC 转换器','Optimize & Convert','将 iPhone HEIC 照片转为通用格式',['让 iPhone 照片在 Windows 和安卓上可看','将 HEIC 转 JPG 以兼容旧软件','把 HEIC 连拍转为 WebP 供网页使用'],[('iPhone 为什么用 HEIC？','HEIC 压缩优于 JPG，但兼容性有限——转换即可解决。'),('支持 Live Photos 吗？','仅转换静态图像，动态数据不保留。')]),
 'heic-to-jpg': ('HEIC 转 JPG','Optimize & Convert','即时将 HEIC 转为 JPG',['在任何设备上打开 iPhone 照片','上传 HEIC 照片到需要 JPG 的服务','无兼容问题地分享照片'],[('会有画质损失吗？','高质量设置下转换近乎无损。'),('可以转换多个文件吗？','可以，支持批量转换。')]),
 'svg-to-png': ('SVG 转 PNG','Optimize & Convert','将 SVG 矢量图栅格化为高分辨率图片',['以 4x 缩放导出 Logo 供视网膜屏','将 SVG 图标转 PNG 用作 favicon','从 SVG 生成社交预览图'],[('支持哪些缩放倍数？','1x、2x、3x、4x，输出清晰高 DPI。'),('可以粘贴 SVG 代码而非上传吗？','可以——直接粘贴 SVG 标记到工具中。')]),
 'avif-support': ('AVIF 支持','Optimize & Convert','检测 AVIF 支持并解码 AVIF 图片',['测试浏览器是否支持 AVIF','将 AVIF 解码为 JPG 以便编辑','把 AVIF 转 PNG 获得最大兼容'],[('AVIF 是什么？','AVIF 是现代图片格式，压缩出色，Chrome 和 Firefox 支持。'),('为什么要解码 AVIF？','部分编辑器和平台尚不接受原生 AVIF。')]),
 'pdf-to-image': ('PDF 转图片','Optimize & Convert','将 PDF 页面转为高质量图片',['将 PDF 页面提取为图片用于演示','把 PDF 报告转为可分享的图片幻灯片','为社交媒体渲染 PDF 页面'],[('有哪些输出分辨率？','1x、2x、3x 缩放，从标准到高 DPI。'),('所有页面都会导出吗？','是的——每页渲染为独立图片文件。')]),
 'image-to-pdf': ('图片转 PDF','Optimize & Convert','将多张图片合并为一个 PDF',['将商品照片打包成单一目录 PDF','从旅行照片创建 PDF 相册','将扫描件汇编为一个文件'],[('可以设置页面尺寸和方向吗？','可以——A4、Letter 等，纵向或横向。'),('边距可调吗？','可以，含无边距选项以实现满版图片。')]),
 'resizer': ('图片缩放器','Resize & Crop','按像素或百分比缩放图片',['为社交媒体头像缩放照片','缩小图片用作邮件缩略图','批量将商品图缩放为统一尺寸'],[('可以保持宽高比吗？','可以——启用"保持宽高比"避免变形。'),('支持批量缩放吗？','支持，用相同设置一次缩放多张图片。')]),
 'cropper': ('图片裁剪器','Resize & Crop','自由裁剪或按预设比例裁剪',['裁剪照片为 Instagram、Facebook、Twitter 尺寸','去除截图多余边缘','按比例预设框选主体'],[('有哪些比例预设？','1:1、4:3、16:9、3:2 及常见社交媒体尺寸。'),('可以自由裁剪吗？','可以——拖动裁剪框至任意尺寸。')]),
 'print-resizer': ('打印尺寸缩放器','Resize & Crop','按精确打印尺寸和 DPI 缩放图片',['为 4×6 照片准备 300 DPI 图','为 A4 和 Letter 纸张设定尺寸','制作 600 DPI 名片尺寸图片'],[('支持哪些 DPI 范围？','72 至 600 DPI，从屏幕到高品质打印。'),('包含哪些纸张尺寸？','A4、A5、Letter、4×6 及名片尺寸。')]),
 'circle-crop': ('圆形裁剪','Resize & Crop','将图片裁剪为完美圆形',['为社交媒体制作圆形头像','为团队页制作圆角头像','设计圆形 Logo 徽章'],[('背景透明吗？','是的——圆外区域为透明（PNG）。'),('可以调整圆形位置吗？','可以——拖动将圆定位到主体上。')]),
 'image-splitter': ('图片分割器','Resize & Crop','将图片分割为网格碎片',['从一张图创建 Instagram 轮播网格','将全景图切分为可滑动瓦片','将大图切成可打印的区块'],[('支持哪些网格尺寸？','2×2、3×3 及自定义行列数。'),('碎片是单独导出吗？','是的——每片单独下载，或全部打包为 ZIP。')]),
 'video-crop': ('视频裁剪','Resize & Crop','将视频裁剪为任意比例',['将竖屏视频裁为 16:9 用于 YouTube','为 Instagram 方形重新构图视频','去除素材多余边框'],[('支持哪些视频格式？','MP4、WebM 等浏览器可播放格式。'),('有时长限制吗？','长视频支持但处理需时间。')]),
 'image-filters': ('图片滤镜','Edit & Effects','应用 15+ 预设滤镜并精细调节',['应用复古或棕褐滤镜营造怀旧感','用鲜艳预设提亮暗淡照片','为信息流创建一致滤镜风格'],[('可精细调节哪些参数？','亮度、对比度、饱和度、模糊、色相。'),('有实时预览吗？','有——每次更改下载前即时预览。')]),
 'image-rotator': ('图片旋转与翻转','Edit & Effects','按任意角度旋转或翻转图片',['修正相机拍出的横向照片','镜像图片做对称设计','将扫描文档旋正'],[('可以自定义角度旋转吗？','可以——任意角度，加快速 90° 按钮。'),('翻转和镜像有何区别？','翻转水平或垂直交换像素；旋转转动整张图。')]),
 'image-adjust': ('图片调色','Edit & Effects','调节亮度、对比度和饱和度',['修正欠曝暗照','提亮褪色色彩','为商品照打造均衡外观'],[('预览是实时的吗？','是的——滑块实时更新图像。'),('可以重置调节吗？','可以——一键重置为原图。')]),
 'image-border': ('图片边框与圆角','Edit & Effects','添加圆角和自定义边框',['为商品缩略图加圆角','用彩色边框为照片镶框','制作完美圆形头像'],[('可设置边框颜色和宽度吗？','可以——任意颜色和像素宽度。'),('圆角可调吗？','可以——从微圆到完整圆形。')]),
 'image-flip': ('图片翻转','Edit & Effects','水平或垂直翻转图片',['修正镜像自拍方向','翻转图片做对称设计','修正扫描底片'],[('翻转会降质吗？','不会——翻转无损。'),('可以同时翻转和旋转吗？','可以——自由组合翻转与旋转。')]),
 'image-grayscale': ('图片灰度与色彩','Edit & Effects','转为灰度、棕褐或反色',['制作黑白照片','应用棕褐营造怀旧感','反色制作负片效果'],[('有哪些色彩效果？','灰度、棕褐、颜色反转。'),('可调节效果强度吗？','可以——支持部分效果。')]),
 'image-shadow': ('图片投影','Edit & Effects','添加逼真投影',['为电商商品照增加层次感','为设计元素加投影效果','让 Logo 呈漂浮感'],[('投影可自定义吗？','可以——偏移、模糊半径和颜色。'),('背景透明吗？','是的——输出为带透明通道的 PNG。')]),
 'image-merger': ('图片合并器','Edit & Effects','并排或堆叠合并多张图片',['创建前后对比图','将照片合并为联系表','构建拼贴布局'],[('支持哪些合并布局？','水平、垂直和网格布局。'),('可设置图片间距吗？','可以——可调间距和背景色。')]),
 'watermark': ('水印工具','Edit & Effects','添加文字或图片水印',['用版权水印保护照片','用 Logo 为商品图打标','为作品加淡雅签名'],[('可以用图片作水印吗？','可以——上传 Logo PNG 并放置任意位置。'),('透明度可调吗？','可以——从淡到完全不透明。')]),
 'gif-editor': ('GIF 编辑器','Edit & Effects','编辑、优化和定制动画 GIF',['将 GIF 裁剪为更短循环','优化 GIF 文件体积','调整 GIF 播放速度'],[('可以从 GIF 提取帧吗？','可以——将 GIF 拆分为单帧。'),('支持逐帧编辑吗？','支持——查看并编辑每一帧。')]),
 'gif-splitter': ('GIF 拆分器','Edit & Effects','将动画 GIF 拆分为帧',['从 GIF 提取特定帧','将 GIF 帧转 PNG 以便编辑','逐帧分析 GIF 动画'],[('帧是什么格式？','PNG 图片，每帧一张。'),('可以一次下载所有帧吗？','可以——打包为 ZIP。')]),
 'background-remover': ('背景移除器','AI Enhance','用 AI 即时移除图片背景',['为电商商品图制作抠图','为设计叠加制作透明 PNG','移除头像照片背景'],[('AI 背景移除如何工作？','神经网络在浏览器内将主体与背景分离。'),('输出透明吗？','是的——背景变为透明（带 alpha 的 PNG）。')]),
 'image-enhancer': ('图片增强器','AI Enhance','增强照片清晰度和细节',['锐化模糊照片','提亮柔和图像细节','改善老旧或低质图片'],[('所有照片都适用吗？','对轻度模糊或柔和的照片效果最佳。'),('过程是自动的吗？','是的——一键增强，无需设置。')]),
 'image-upscaler': ('图片放大器','AI Enhance','用 AI 放大图片最高 4x',['放大低分辨率照片用于打印','为高 DPI 屏放大图标','为演示改善小图'],[('支持哪些放大倍数？','2x 和 4x 放大。'),('放大会增加真实细节吗？','AI 放大智能填补细节，但无法创造原图不存在的信息。')]),
 'face-blur': ('人脸模糊','AI Enhance','自动模糊人脸以保护隐私',['在街拍中保护身份','分享前模糊未成年人面部','在纪实照片中匿名化人物'],[('如何检测人脸？','浏览器端人脸检测模型自动查找人脸。'),('可以手动模糊吗？','可以——手动调整或添加模糊区域。')]),
 'beauty-editor': ('美颜编辑器','AI Enhance','人像修图和磨皮',['为人像照片磨皮','提亮并均匀肤色','头像快速修整'],[('修图自然吗？','是的——细微调整保留自然特征。'),('可以控制强度吗？','可以——可调强度滑块。')]),
 'photo-restoration': ('老照片修复','AI Enhance','修复和增强老旧照片',['修复褪色的复古家庭照','修补老旧扫描照','为陈旧照片增色添清晰'],[('会给黑白照上色吗？','它增强清晰度；上色是单独的增强。'),('什么照片条件最佳？','以最高可用分辨率扫描的老照片效果最佳。')]),
 'product-white-background': ('商品白底图','AI Enhance','将商品置于纯白背景',['统一电商商品图','制作符合市场要求的白底照','为目录清理商品照'],[('如何工作？','移除背景并替换为纯白。'),('商品抠图准确吗？','AI 分割在商品周围产生干净边缘。')]),
 'id-photo': ('证件照制作器','AI Enhance','制作尺寸和背景合规的证件照',['在家制作护照照','生成签证尺寸照片','制作学生或员工证件照'],[('支持哪些证件尺寸？','护照、签证及常见国家证件尺寸。'),('可改背景色吗？','可以——白、蓝、红背景选项。')]),
 'ocr': ('OCR 文字识别','AI Enhance','从图片中提取文字',['从照片数字化印刷文档','从截图提取文字','将扫描页转为可编辑文本'],[('OCR 支持哪些语言？','多语言含英文，支持拉丁字母文字。'),('手写体可用吗？','OCR 针对印刷文字优化；手写准确率不一。')]),
 'text-on-image': ('图片加文字','Create & Design','为图片添加 stylish 文字',['创建带字幕的社交媒体图','设计图文语录和海报','为照片加标签和标题'],[('可自定义字体和颜色吗？','可以——字体、字号、颜色、位置均可调。'),('文字定位灵活吗？','可以——拖动文字到图片任意位置。')]),
 'meme-generator': ('表情包生成器','Create & Design','用经典和自定义文字制作表情包',['制作经典上下文字表情包','为社交媒体设计反应表情','从照片制作自定义表情'],[('含经典表情模板吗？','是的——内置热门模板。'),('可以用自己的图吗？','可以——上传任意图片制作表情。')]),
 'signature-maker': ('签名制作器','Create & Design','绘制并导出你的签名',['为文档创建数字签名','用个人签名签署 PDF','生成干净的签名 PNG'],[('可用鼠标或手写笔吗？','可以——均支持，移动端还支持触摸。'),('签名是什么格式？','透明 PNG，可放置于任何文档。')]),
 'favicon-generator': ('Favicon 生成器','Create & Design','为网站创建 favicon',['生成 16x16 和 32x32 favicon','从 Logo 创建 favicon','为浏览器制作应用图标'],[('生成哪些尺寸？','16x16、32x32 及 180x180 Apple touch 图标。'),('输出什么格式？','ICO 和 PNG 格式。')]),
 'ico-icon-generator': ('ICO 图标生成器','Create & Design','将图片转为 ICO 图标文件',['从图片创建 Windows 图标','生成应用图标','制作桌面文件夹图标'],[('ICO 含哪些尺寸？','多分辨率：16、32、48、64 像素。'),('可用 PNG 作输入吗？','可以——任意位图均可。')]),
 'qr-code-generator': ('二维码生成器','Create & Design','为链接和文字生成二维码',['为网站链接创建二维码','为 Wi-Fi 或联系信息生成二维码','为印刷品制作二维码'],[('二维码可定制吗？','可以——尺寸、颜色和纠错等级。'),('可编码什么？','网址、文字、电话号码等。')]),
 'social-media-post': ('社交媒体配图制作器','Create & Design','制作适配社交平台的图片',['制作 Instagram 帖子和故事图','创建 Facebook 封面照','设计 Twitter 头图'],[('支持哪些平台？','Instagram、Facebook、Twitter、LinkedIn 等。'),('尺寸是预设的吗？','是的——每个平台正确尺寸内置。')]),
 'screenshot-to-image': ('截图转图片','Create & Design','转换并增强截图',['为教程美化截图','转换截图格式','为截图加边框'],[('支持哪些截图格式？','PNG、JPG 等常见图片格式。'),('可以裁剪截图吗？','可以——裁剪到相关区域。')]),
 'color-palette': ('配色提取器','Utility & Analyze','从图片提取主色调',['从照片构建品牌色板','为设计寻找匹配色','分析图片配色方案'],[('提取多少种颜色？','前 5–10 种主色。'),('提供色值吗？','是的——每种颜色的 HEX 码，可复制。')]),
 'metadata-viewer': ('元数据查看器','Utility & Analyze','查看 EXIF 和图片元数据',['查看照片所用相机设置','查找图片中的 GPS 位置','核实图片尺寸和格式'],[('显示哪些元数据？','EXIF 字段如相机、镜头、设置、GPS、时间戳。'),('下载会移除元数据吗？','不会——此工具仅查看；清除请用 EXIF 移除工具。')]),
 'image-exif-remover': ('EXIF 移除器','Utility & Analyze','去除图片 EXIF 元数据',['分享前移除 GPS 位置','为隐私去除相机信息','上传前清除元数据'],[('移除哪些元数据？','EXIF 字段含 GPS、相机信息、时间戳。'),('影响画质吗？','不会——仅移除元数据，像素不变。')]),
 'image-compare': ('图片对比','Utility & Analyze','并排对比两张图片',['找出两版差异','对比编辑前后','质检修图效果'],[('差异如何显示？','并排和叠加模式高亮差异。'),('支持像素级对比吗？','是的——差异图显示变化像素。')]),
 'bulk-processor': ('批量处理器','Utility & Analyze','一次批量处理多张图片',['对数十张图片应用相同编辑','批量缩放或压缩照片文件夹','自动化重复图片任务'],[('哪些操作可批量？','缩放、压缩、转换等——应用于每个文件。'),('有文件数限制吗？','仅受浏览器内存限制；数百文件无压力。')]),
 'word-counter': ('字数统计器','Utility & Analyze','统计字数、字符数和阅读时间',['检查论文字数','估算文章阅读时间','分析文本长度用于 SEO'],[('显示哪些统计？','字数、字符、句子、段落、阅读时间。'),('所有语言都准吗？','是的——适用于任意文本输入。')]),
 'case-converter': ('大小写转换器','Utility & Analyze','在大小写间转换文本',['转标题式用于标题','切换为全大写或全小写','修正段落句式大小写'],[('支持哪些大小写？','全大写、全小写、标题式、句式、驼峰式。'),('即时吗？','是的——输入即转换。')]),
 'text-sorter': ('文本排序器','Utility & Analyze','排序和整理文本行',['按字母排序列表','去除重复行','反转行顺序'],[('有哪些排序选项？','字母、数字、反转、去重。'),('能处理大列表吗？','可以——数千行即时处理。')]),
 'text-find-replace': ('文本查找替换','Utility & Analyze','按模式查找和替换文本',['跨文本批量替换词语','用正则做高级替换','清理文本格式'],[('支持正则吗？','支持——完整正则查找替换。'),('可预览更改吗？','可以——应用前查看匹配。')]),
 'base64': ('Base64 编解码器','Text & Developer Tools','编码和解码 Base64 数据',['将图片编码为 Base64 用于内联 CSS','解码 Base64 字符串为文本','转换数据 URI 用于嵌入'],[('能处理图片吗？','可以——将图片文件编码为 Base64 数据 URI。'),('解码准确吗？','是的——无损往返编解码。')]),
 'html-encoder': ('HTML 编解码器','Text & Developer Tools','编码和解码 HTML 实体',['转义 HTML 特殊字符','为安全 HTML 显示准备文本','解码实体编码内容'],[('转义哪些字符？','<、>、&、"、\' ——核心 HTML 实体。'),('双向吗？','是的——编码和解码均支持。')]),
 'url-encoder': ('URL 编解码器','Text & Developer Tools','编码和解码 URL 组件',['安全编码查询参数','解码编码 URL 以调试','为 URL 包含准备文本'],[('遵循 RFC 3986 吗？','是的——标准 URL 百分号编码。'),('可编码完整 URL 吗？','可以——编码组件或完整 URL。')]),
 'json-formatter': ('JSON 格式化器','Text & Developer Tools','格式化、校验和美化 JSON',['美化压缩的 JSON','校验 JSON 语法错误','美化 API 响应便于阅读'],[('会校验 JSON 吗？','是的——语法错误带行号高亮。'),('可压缩 JSON 吗？','可以——在美化和压缩间切换。')]),
 'regex-tester': ('正则测试器','Text & Developer Tools','实时测试正则表达式',['调试正则模式','用样例文本测试匹配','通过实时反馈学习正则'],[('显示匹配高亮吗？','是的——匹配在输入文本中高亮。'),('用哪种正则？','标准 JavaScript 正则表达式。')]),
 'text-diff': ('文本差异对比','Text & Developer Tools','对比两段文本并显示差异',['对比两个文档版本','找出文本草稿间更改','审查代码或文本编辑'],[('差异如何显示？','新增和删除行以颜色高亮。'),('是逐行吗？','是的——经典逐行差异。')]),
 'password-generator': ('密码生成器','Text & Developer Tools','生成安全的随机密码',['为账户创建强密码','为安全密钥生成密码短语','为每个站点生成唯一密码'],[('可设置长度和字符集吗？','可以——长度、大小写、数字、符号。'),('密码本地生成吗？','是的——完全在浏览器内，绝不外传。')]),
 'uuid-generator': ('UUID 生成器','Text & Developer Tools','生成 UUID（GUID）',['为数据库生成唯一 ID','为分布式系统创建 UUID','生成测试标识符'],[('支持哪些 UUID 版本？','默认生成 UUID v4（随机）。'),('可批量生成吗？','可以——一次生成多个 UUID。')]),
 'pdf-merge': ('PDF 合并','PDF Tools','将多个 PDF 合并为一个',['将扫描页合并为单文档','将多份报告合并为一个文件','将 PDF 章节合订成书'],[('有文件数限制吗？','无硬性限制——浏览器能处理多少就合并多少。'),('保留书签吗？','合并页面内容；按原文件顺序排列。')]),
 'pdf-split': ('PDF 拆分','PDF Tools','将 PDF 拆分为多个文件',['将章节提取为独立 PDF','将大 PDF 拆为小块','按页分离以便单独分享'],[('可按页码范围拆分吗？','可以——自定义范围或每 N 页拆分。'),('拆分后是独立 PDF 吗？','是的——每个输出都是有效独立 PDF。')]),
 'pdf-rotate': ('PDF 旋转','PDF Tools','旋转 PDF 页面',['修正横向扫描页','将横向页旋为纵向','统一文档方向'],[('可旋转单页吗？','可以——旋转全部或选中页。'),('支持哪些旋转？','顺时针或逆时针 90°、180°、270°。')]),
 'pdf-compress': ('PDF 压缩','PDF Tools','减小 PDF 文件体积',['为邮件附件压缩 PDF','压缩扫描文档','为网页上传减小 PDF 体积'],[('PDF 能缩多少？','视内容而定——图片密集型 PDF 压缩最多。'),('保留画质吗？','是的——文字清晰；图片以均衡质量重新编码。')]),
 'pdf-extract-pages': ('PDF 提取页面','PDF Tools','从 PDF 提取指定页面',['抽出需要的页面','创建文档子集','只分享相关页面'],[('可选任意页吗？','可以——选单页或范围。'),('输出是有效 PDF 吗？','是的——提取页面组成独立 PDF。')]),
 'pdf-delete-pages': ('PDF 删除页面','PDF Tools','从 PDF 移除不需要的页面',['删除空白页','分享前移除敏感页','精简文档至 essentials'],[('删除前可预览吗？','可以——页面缩略图助你选择。'),('会修改原件吗？','不会——创建不含已删页的新 PDF。')]),
 'pdf-to-word': ('PDF 转 Word','PDF Tools','将 PDF 转为可编辑 Word',['在 Microsoft Word 中编辑 PDF 内容','从 PDF 报告提取文字','将 PDF 信件转为 Word 文档'],[('输出可编辑吗？','是的——真实 .docx 文字可编辑，非图片。'),('表格会保留吗？','提取文字和基本结构；复杂布局可能简化。')]),
 'pdf-to-excel': ('PDF 转 Excel','PDF Tools','将 PDF 表格转为 Excel',['从 PDF 报告提取财务表格','将 PDF 数据转为可编辑表格','将银行流水转为 Excel'],[('如何检测表格？','工具分析文字 X/Y 坐标重建行列。'),('扫描 PDF 可用吗？','不可——扫描 PDF 需先 OCR；此工具读取文字层。')]),
 'pdf-to-ppt': ('PDF 转 PPT','PDF Tools','将 PDF 转为 PowerPoint',['将 PDF 报告转为演示文稿','从 PDF 文档创建幻灯片','在幻灯片中复用 PDF 内容'],[('页面如何转换？','每页 PDF 成为一张高分辨率图片幻灯片。'),('文字可编辑吗？','幻灯片含页面图片；可编辑文字请用 PDF 转 Word。')]),
 'word-to-pdf': ('Word 转 PDF','PDF Tools','将 Word 文档转为 PDF',['将 Word 文档作为不可编辑 PDF 分享','为打印保留格式','将简历转为 PDF'],[('格式会保留吗？','文字和段落干净渲染到 PDF。'),('字体内嵌吗？','使用标准字体确保广泛兼容。')]),
 'excel-to-pdf': ('Excel 转 PDF','PDF Tools','将 Excel 表格转为 PDF',['将表格作为只读 PDF 分享','以正确格式打印 Excel 工作表','将财务数据存档为 PDF'],[('工作表如何处理？','每个工作表成为一页带自适应表格。'),('大表格会分页吗？','是的——宽表格智能跨页。')]),
 'pdf-editor': ('PDF 编辑器','PDF Tools','为 PDF 添加文字、图片和形状',['签署前批注合同','为 PDF 文档加备注和标签','在 PDF 报告中插入图片'],[('可为 PDF 添加什么？','文本框、图片和形状——放置于页面任意位置。'),('会修改原件吗？','不会——创建新的已编辑 PDF。')]),
 'pdf-annotate': ('PDF 批注','PDF Tools','添加高亮、下划线和备注',['在学习材料中高亮关键段落','在合同条款下划线','为文档添加审阅备注'],[('支持哪些批注类型？','高亮、下划线和文字备注。'),('可批注多页吗？','可以——浏览并批注每一页。')]),
 'pdf-number-pages': ('PDF 加页码','PDF Tools','为 PDF 添加页码',['为报告编号','为论文加页码','为长文档建立索引'],[('页码可出现在哪？','每页顶部或底部、左、中、右。'),('支持哪些页码格式？','纯数字、"第 N 页"、"第 N 页/共 M 页"。')]),
 'pdf-crop': ('PDF 裁剪','PDF Tools','裁剪 PDF 页面区域',['去除 PDF 边距','裁剪扫描页多余边框','聚焦页面特定区域'],[('可一次裁剪所有页吗？','可以——应用于当前页或每页。'),('裁剪是可视的吗？','是的——在页面预览上拖选裁剪区域。')]),
 'pdf-organize': ('PDF 排序整理','PDF Tools','重排、删除和复制页面',['重排文档页面','删除不需要的页面','复制页面以重复使用'],[('可拖动重排吗？','可以——拖放缩略图重排页面。'),('可复制页面吗？','可以——一键复制任意页。')]),
 'pdf-compare': ('PDF 对比','PDF Tools','并排对比两个 PDF',['找出合同版本间差异','对比修订版与原始文档','核实 PDF 草稿间更改'],[('差异如何显示？','每对页面标记相同或不同。'),('对比是可视的吗？','是的——逐页渲染并按像素对比。')]),
 'pdf-redact': ('PDF 隐藏敏感信息','PDF Tools','用黑块覆盖 PDF 中的敏感信息',['分享前隐藏个人数据','遮盖机密段落','保护法律文档隐私'],[('遮盖是永久的吗？','是的——黑块烧入 PDF，覆盖下方内容。'),('可遮盖多处吗？','可以——按需绘制任意多遮盖矩形。')]),
 'html-to-pdf': ('HTML 转 PDF','PDF Tools','将 HTML 转为 PDF',['将网页内容存为 PDF','将 HTML 邮件转为 PDF','将网页存档为文档'],[('PDF 可搜索吗？','是的——真实文字，可选中可搜索。'),('保留 CSS 样式吗？','保留文档结构（标题、段落、列表）；不保留精确 CSS 布局。')]),
 'txt-to-pdf': ('TXT 转 PDF','PDF Tools','将文本文件转为 PDF',['将笔记转为可分享 PDF','将日志文件转为文档','从 Markdown 草稿创建 PDF'],[('支持哪些文本格式？','.txt、.md、.log——任意纯文本文件。'),('PDF 可搜索吗？','是的——真实文字输出。')]),
 'csv-to-pdf': ('CSV 转 PDF','PDF Tools','将 CSV 数据转为 PDF 表格',['从 CSV 数据创建 PDF 报告','将表格数据作为 PDF 分享','在 PDF 中存档表格数据'],[('处理带引号字段吗？','是的——符合 RFC 4180，含引号内逗号。'),('支持大数据集吗？','是的，自动跨页分页。')]),
 'epub-to-pdf': ('EPUB 转 PDF','PDF Tools','将 EPUB 电子书转为 PDF',['在仅支持 PDF 的设备上阅读电子书','从电子书打印章节','将电子书库存档为 PDF'],[('章节会保留吗？','是的——按阅读顺序提取含标题。'),('PDF 可搜索吗？','是的——真实文字，可选中可搜索。')]),
 'video-rotate': ('视频旋转','Video Tools','将视频旋转至任意方向',['修正手机横向视频','将竖屏视频旋为横屏','分享前纠正方向'],[('支持哪些旋转？','90°、180°、270°。'),('所有视频格式都支持吗？','MP4、WebM 等浏览器可播放格式。')]),
 'video-speed': ('视频变速','Video Tools','改变视频播放速度',['制作慢动作片段','加速长素材做延时','为集锦调节速度'],[('支持哪些速度范围？','0.25x 至 4x 播放速度。'),('音频会受影响吗？','音频音高随速度调整。')]),
 'video-to-frames': ('视频转帧','Video Tools','从视频提取帧',['从视频片段抓取静帧','为动画提取帧','捕捉完美静帧瞬间'],[('帧是什么格式？','PNG 或 JPG 图片。'),('可提取每一帧吗？','可以——或按设定间隔提取。')]),
 'video-to-mp3': ('视频转 MP3','Video Tools','将视频音频提取为 MP3',['从 MV 提取音频','从片段提取原声带','将视频访谈存为音频'],[('输出什么音频格式？','MP3 音频，从视频轨道提取。'),('有时长限制吗？','长视频支持但耗时更长。')]),
 'video-to-gif': ('视频转 GIF','Video Tools','将视频片段转为 GIF',['为社交媒体制作 GIF','从视频制作动态贴纸','将片段转为循环 GIF'],[('可裁剪 GIF 吗？','可以——选择片段起止。'),('输出什么格式？','动画 GIF，已优化体积。')]),
 'video-compressor': ('视频压缩器','Video Tools','减小视频文件体积',['为邮件压缩视频','为网页上传缩减素材','减小视频体积以存储'],[('视频能缩多少？','可调质量下显著缩减。'),('保留画质吗？','是的——均衡压缩保持可接受画质。')]),
}

# CSS is identical to English version (already in pages via enrich-css id, but zh pages don't have it yet)
ENRICH_CSS = '''
.selling-points{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:1rem 0 1.5rem}
.sp-item{display:flex;align-items:center;gap:8px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:999px;padding:8px 16px;font-size:0.85rem;color:var(--text-secondary);font-weight:500}
.sp-item span.sp-icon{font-size:1rem}
.feature-narrative{margin:2.5rem 0;padding:0 1rem}
.feature-narrative h2{font-size:1.6rem;color:var(--text-primary);margin-bottom:0.5rem;text-align:center}
.feature-narrative .fn-intro{text-align:center;max-width:680px;margin:0 auto 2rem;color:var(--text-secondary);font-size:1rem;line-height:1.6}
.fn-block{display:flex;gap:1.5rem;align-items:flex-start;margin:1.5rem 0;padding:1.25rem;background:var(--bg-secondary);border-radius:12px;border:1px solid var(--border)}
.fn-block .fn-icon{font-size:2rem;flex-shrink:0;line-height:1}
.fn-block h3{font-size:1.05rem;color:var(--text-primary);margin:0 0 0.4rem}
.fn-block p{color:var(--text-secondary);font-size:0.9rem;line-height:1.6;margin:0}
.features-grid-section{margin:2.5rem 0;padding:0 1rem}
.features-grid-section h2{font-size:1.6rem;color:var(--text-primary);margin-bottom:0.5rem;text-align:center}
.features-grid-section .fg-sub{text-align:center;color:var(--text-secondary);font-size:0.95rem;margin-bottom:2rem}
.features-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;max-width:1000px;margin:0 auto}
.feature-card{background:var(--bg-secondary);border:1px solid var(--border);border-radius:12px;padding:1.25rem;transition:transform .2s,border-color .2s}
.feature-card:hover{transform:translateY(-2px);border-color:var(--accent)}
.feature-card .fc-icon{font-size:1.8rem;margin-bottom:0.5rem}
.feature-card h3{font-size:1rem;color:var(--text-primary);margin:0 0 0.4rem}
.feature-card p{color:var(--text-secondary);font-size:0.85rem;line-height:1.5;margin:0}
.trust-badges{display:flex;flex-wrap:wrap;gap:16px;justify-content:center;margin:2rem 0;padding:1.5rem;background:var(--bg-secondary);border-radius:12px;border:1px solid var(--border)}
.trust-badge{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:120px}
.trust-badge .tb-icon{font-size:1.6rem}
.trust-badge .tb-title{font-size:0.85rem;font-weight:700;color:var(--text-primary)}
.trust-badge .tb-desc{font-size:0.72rem;color:var(--text-secondary)}
@media(max-width:640px){.fn-block{flex-direction:column}.features-grid{grid-template-columns:1fr}.trust-badges{gap:12px}.trust-badge{min-width:90px}}
'''

def build_zh_selling_points(tagline, use_cases):
    pts = [tagline]
    if len(use_cases) >= 2:
        pts.append(use_cases[0])
        pts.append('100% 隐私 —— 浏览器端运行')
    else:
        pts.append('免费且浏览器端运行')
        pts.append('100% 隐私 —— 浏览器端运行')
    html = '<div class="selling-points">\n'
    icons = ['✅','🎯','🔒']
    for i, p in enumerate(pts[:3]):
        html += f'  <div class="sp-item"><span class="sp-icon">{icons[i]}</span>{p}</div>\n'
    html += '</div>'
    return html

def build_zh_narrative(name, tagline, input_desc_unused, output_desc_unused, use_cases):
    intro = f'{name}让你{tagline}。全部在浏览器本地处理，无需上传、无需注册。'
    block_icons = ['⚡','🎯','🔒']
    blocks = ''
    for i, uc in enumerate(use_cases[:3]):
        blocks += f'''      <div class="fn-block">
        <div class="fn-icon">{block_icons[i]}</div>
        <div><h3>{uc}</h3><p>{uc}。这是人们使用{name}最常见的理由之一——几秒内即可在浏览器中完成。</p></div>
      </div>
'''
    return f'''      <section class="feature-narrative">
        <h2>{name}：{tagline}</h2>
        <p class="fn-intro">{intro}</p>
{blocks}      </section>'''

def build_zh_features_grid(cat, name):
    cd = ZH_CATEGORY.get(cat, ZH_CATEGORY['PDF Tools'])
    cards = ''
    for ic, title, desc in cd['features']:
        cards += f'''        <div class="feature-card">
          <div class="fc-icon">{ic}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>
'''
    return f'''      <section class="features-grid-section">
        <h2>{name}所需的一切功能</h2>
        <p class="fg-sub">让{name}快速、私密且免费的强大功能。</p>
        <div class="features-grid">
{cards}        </div>
      </section>'''

def build_zh_trust():
    html = '<div class="trust-badges">\n'
    for ic, title, desc in ZH_TRUST:
        html += f'  <div class="trust-badge"><div class="tb-icon">{ic}</div><div class="tb-title">{title}</div><div class="tb-desc">{desc}</div></div>\n'
    html += '</div>'
    return html

def build_zh_extra_faqs(tool_faqs, cat):
    cd = ZH_CATEGORY.get(cat, ZH_CATEGORY['PDF Tools'])
    # Normalize 4-element tuples
    norm = []
    for fq in tool_faqs:
        if isinstance(fq, tuple) and len(fq) == 4:
            norm.append((fq[0], fq[1])); norm.append((fq[2], fq[3]))
        else:
            norm.append(fq)
    all_faqs = norm + cd['faqs']
    html = ''
    for q, a in all_faqs:
        html += f'<div class="faq-item"><button class="faq-question">{q}</button><div class="faq-answer">{a}</div></div>\n'
    return html

def enrich_zh(slug):
    data = ZH_TOOLS.get(slug)
    if not data:
        return False, 'no zh data'
    name, cat, tagline, use_cases, tool_faqs = data
    fpath = os.path.join(ZH_DIR, f'{slug}.html')
    if not os.path.exists(fpath):
        return False, 'file not found'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'feature-narrative' in html and 'selling-points' in html:
        return False, 'already enriched'

    # 1. CSS
    if 'enrich-css' not in html:
        html = html.replace('</head>', '\n<style id="enrich-css">' + ENRICH_CSS + '</style>\n</head>', 1)

    # 2. Selling points after tool-page-header
    sp = build_zh_selling_points(tagline, use_cases)
    header_close = re.search(r'(<div class="tool-page-header">[\s\S]*?</div>\s*</div>)', html)
    if header_close:
        html = html.replace(header_close.group(0), header_close.group(0) + '\n        ' + sp, 1)

    # 3. Narrative + grid + badges before how-to-section
    narrative = build_zh_narrative(name, tagline, '', '', use_cases)
    grid = build_zh_features_grid(cat, name)
    badges = build_zh_trust()
    block = '\n' + narrative + '\n\n' + grid + '\n\n' + badges + '\n'
    if '<section class="how-to-section">' in html:
        html = html.replace('<section class="how-to-section">', block + '      <section class="how-to-section">', 1)
    elif '<section class="related-tools">' in html:
        html = html.replace('<section class="related-tools">', block + '      <section class="related-tools">', 1)
    else:
        html = html.replace('</main>', block + '  </main>', 1)

    # 4. Extra FAQs
    extra = build_zh_extra_faqs(tool_faqs, cat)
    faq_match = re.search(r'(<section class="faq-section">[\s\S]*?)(</section>)', html)
    if faq_match:
        html = html.replace(faq_match.group(0), faq_match.group(1) + extra + '      ' + faq_match.group(2), 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    return True, 'enriched (zh)'

def main():
    print('=== Enriching zh tool pages with Chinese content ===\n')
    enriched, skipped, nodata = 0, 0, 0
    zh_files = [f[:-5] for f in os.listdir(ZH_DIR) if f.endswith('.html')]
    for slug in sorted(zh_files):
        if slug not in ZH_TOOLS:
            nodata += 1
            print(f'  ⏭️  {slug}: no zh data (skipped)')
            continue
        ok, msg = enrich_zh(slug)
        if ok:
            enriched += 1
            print(f'  ✅ {slug}: {msg}')
        else:
            skipped += 1
            print(f'  ⏭️  {slug}: {msg}')
    print(f'\nDone: {enriched} enriched, {skipped} skipped, {nodata} without data (of {len(zh_files)} zh files)')

if __name__ == '__main__':
    main()
