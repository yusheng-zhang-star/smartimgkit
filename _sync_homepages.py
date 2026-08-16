#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync homepages: search bar, category pills, PDF subcats, fix tool placement."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LANGS = ['en','es','pt','id','fr','vi','ar','zh']

# ===== Category metadata (9 cats x 8 langs) =====
CAT_NAMES = {
    'optimize': {'en':'Optimize & Convert','es':'Optimizar y Convertir','pt':'Otimizar e Converter','id':'Optimalkan & Konversi','fr':'Optimiser et Convertir','vi':'Tối ưu & Chuyển đổi','ar':'تحسين وتحويل','zh':'优化与转换'},
    'resize': {'en':'Resize & Crop','es':'Redimensionar y Recortar','pt':'Redimensionar e Recortar','id':'Ubah Ukuran & Pangkas','fr':'Redimensionner et Rogner','vi':'Thay đổi kích thước & Cắt','ar':'تغيير الحجم والقص','zh':'缩放与裁剪'},
    'edit': {'en':'Edit & Effects','es':'Editar y Efectos','pt':'Editar e Efeitos','id':'Edit & Efek','fr':'Édition et Effets','vi':'Chỉnh sửa & Hiệu ứng','ar':'تحرير ومؤثرات','zh':'编辑与特效'},
    'ai': {'en':'AI Enhance','es':'Mejora con IA','pt':'Melhorar com IA','id':'Tingkatkan AI','fr':'Amélioration IA','vi':'Tăng cường AI','ar':'تحسين بالذكاء الاصطناعي','zh':'AI 增强'},
    'create': {'en':'Create & Design','es':'Crear y Diseñar','pt':'Criar e Design','id':'Buat & Desain','fr':'Créer et Concevoir','vi':'Tạo & Thiết kế','ar':'إنشاء وتصميم','zh':'创建与设计'},
    'utility': {'en':'Utility & Analyze','es':'Utilidad y Análisis','pt':'Utilitários e Análise','id':'Utilitas & Analisis','fr':'Utilitaires et Analyse','vi':'Tiện ích & Phân tích','ar':'أدوات وتحليل','zh':'实用与分析'},
    'text': {'en':'Text & Developer Tools','es':'Texto y Herramientas Dev','pt':'Texto e Ferramentas Dev','id':'Teks & Alat Dev','fr':'Texte et Outils Dev','vi':'Văn bản & Công cụ Dev','ar':'نصوص وأدوات المطورين','zh':'文本与开发者工具'},
    'pdf': {'en':'PDF Tools','es':'Herramientas PDF','pt':'Ferramentas PDF','id':'Alat PDF','fr':'Outils PDF','vi':'Công cụ PDF','ar':'أدوات PDF','zh':'PDF 工具'},
    'video': {'en':'Video Tools','es':'Herramientas de Video','pt':'Ferramentas de Vídeo','id':'Alat Video','fr':'Outils Vidéo','vi':'Công cụ Video','ar':'أدوات الفيديو','zh':'视频工具'},
}
CAT_ICONS = {'optimize':'📊','resize':'✂️','edit':'🎨','ai':'✨','create':'🎯','utility':'🔧','text':'📝','pdf':'📄','video':'🎬'}
CAT_ORDER = ['optimize','resize','edit','ai','create','utility','text','pdf','video']
CAT_DESC = {
    'optimize': {'en':'Compress, convert formats, and optimize images for web.','es':'Comprime, convierte formatos y optimiza imágenes para la web.','pt':'Comprima, converta formatos e otimize imagens para a web.','id':'Kompres, konversi format, dan optimalkan gambar untuk web.','fr':'Compressez, convertissez les formats et optimisez les images pour le web.','vi':'Nén, chuyển đổi định dạng và tối ưu hóa hình ảnh cho web.','ar':'ضغط وتحويل الصيغ وتحسين الصور للويب.','zh':'压缩、转换格式、为网页优化图像。'},
    'resize': {'en':'Resize, crop, and split images to any size.','es':'Redimensiona, recorta y divide imágenes a cualquier tamaño.','pt':'Redimensione, recorte e divida imagens em qualquer tamanho.','id':'Ubah ukuran, pangkas, dan bagi gambar ke ukuran apa pun.','fr':'Redimensionnez, rognez et divisez les images à toute taille.','vi':'Thay đổi kích thước, cắt và chia hình ảnh theo bất kỳ kích thước nào.','ar':'تغيير حجم الصور وقصها وتقسيمها لأي حجم.','zh':'缩放、裁剪、分割图片到任意尺寸。'},
    'edit': {'en':'Filters, adjustments, rotations, and creative effects.','es':'Filtros, ajustes, rotaciones y efectos creativos.','pt':'Filtros, ajustes, rotações e efeitos criativos.','id':'Filter, penyesuaian, rotasi, dan efek kreatif.','fr':'Filtres, ajustements, rotations et effets créatifs.','vi':'Bộ lọc, điều chỉnh, xoay và hiệu ứng sáng tạo.','ar':'فلاتر وتعديلات ودوران ومؤثرات إبداعية.','zh':'滤镜、调整、旋转和创意特效。'},
    'ai': {'en':'AI-powered background removal, upscaling, enhancement, and restoration.','es':'Eliminación de fondo con IA, escalado, mejora y restauración.','pt':'Remoção de fundo com IA, upscale, melhoria e restauração.','id':'Penghapusan latar belakang AI, upscale, peningkatan, dan restorasi.','fr':'Suppression de fond IA, upscaling, amélioration et restauration.','vi':'Xóa nền AI, nâng cấp, cải thiện và khôi phục hình ảnh.','ar':'إزالة الخلفية بالذكاء الاصطناعي وتكبير وتحسين واستعادة الصور.','zh':'AI 驱动的抠图、放大、增强和修复。'},
    'create': {'en':'Add text, create memes, GIFs, social posts, and product photos.','es':'Agrega texto, crea memes, GIFs, publicaciones y fotos de producto.','pt':'Adicione texto, crie memes, GIFs, posts e fotos de produto.','id':'Tambahkan teks, buat meme, GIF, postingan, dan foto produk.','fr':'Ajoutez du texte, créez des memes, GIFs, posts et photos produit.','vi':'Thêm văn bản, tạo meme, GIF, bài đăng và ảnh sản phẩm.','ar':'إضافة نص وإنشاء ميمات وGIF ومنشورات وصور منتجات.','zh':'添加文字、制作表情包、GIF、社交媒体帖子和商品图。'},
    'utility': {'en':'OCR, batch processing, color extraction, comparison, and metadata tools.','es':'OCR, procesamiento por lotes, extracción de color, comparación y metadatos.','pt':'OCR, processamento em lote, extração de cores, comparação e metadatos.','id':'OCR, pemrosesan batch, ekstraksi warna, perbandingan, dan metadata.','fr':'OCR, traitement par lot, extraction de couleurs, comparaison et métadonnées.','vi':'OCR, xử lý hàng loạt, trích xuất màu, so sánh và siêu dữ liệu.','ar':'OCR ومعالجة دفعية واستخراج الألوان والمقارنة والأدوات الوصفية.','zh':'OCR、批量处理、颜色提取、对比和元数据工具。'},
    'text': {'en':'Text processing, code formatting, and developer utilities.','es':'Procesamiento de texto, formato de código y utilidades para desarrolladores.','pt':'Processamento de texto, formatação de código e utilitários para desenvolvedores.','id':'Pemrosesan teks, format kode, dan utilitas pengembang.','fr':'Traitement de texte, formatage de code et utilitaires développeur.','vi':'Xử lý văn bản, định dạng mã và tiện ích nhà phát triển.','ar':'معالجة النصوص وتنسيق الأكواد وأدوات المطورين.','zh':'文本处理、代码格式化和开发者工具。'},
    'pdf': {'en':'Merge, split, compress, rotate, and edit PDF files in your browser.','es':'Fusiona, divide, comprime, rota y edita PDF en tu navegador.','pt':'Junte, divida, comprima, gire e edite PDFs no seu navegador.','id':'Gabung, pisahkan, kompres, putar, dan edit PDF di browser Anda.','fr':'Fusionnez, divisez, compressez, faites pivoter et éditez des PDF dans votre navigateur.','vi':'Gộp, tách, nén, xoay và chỉnh sửa PDF trong trình duyệt.','ar':'دمج وتقسيم وضغط وتدوير وتحرير ملفات PDF في متصفحك.','zh':'在浏览器中合并、拆分、压缩、旋转和编辑 PDF 文件。'},
    'video': {'en':'Compress, convert, trim, and edit videos with ffmpeg.wasm in your browser.','es':'Comprime, convierte, recorta y edita videos con ffmpeg.wasm en tu navegador.','pt':'Comprima, converta, corte e edite vídeos com ffmpeg.wasm no seu navegador.','id':'Kompres, konversi, potong, dan edit video dengan ffmpeg.wasm di browser Anda.','fr':'Compressez, convertissez, coupez et éditez des vidéos avec ffmpeg.wasm dans votre navigateur.','vi':'Nén, chuyển đổi, cắt và chỉnh sửa video với ffmpeg.wasm trong trình duyệt.','ar':'ضغط وتحويل وقص وتحرير الفيديو باستخدام ffmpeg.wasm في متصفحك.','zh':'使用 ffmpeg.wasm 在浏览器中压缩、转换、剪辑和编辑视频。'},
}

# ===== Section header strings =====
SECTION = {
    'en': ('All Tools','Powerful, easy-to-use tools that run entirely in your browser. No installs, no uploads, no tracking.'),
    'es': ('Todas las Herramientas','Herramientas potentes y fáciles de usar que funcionan en tu navegador. Sin instalaciones, sin subidas, sin rastreo.'),
    'pt': ('Todas as Ferramentas','Ferramentas poderosas e fáceis de usar que rodam totalmente no seu navegador. Sem instalações, sem uploads, sem rastreamento.'),
    'id': ('Semua Alat','Alat yang canggih dan mudah digunakan, berjalan sepenuhnya di browser Anda. Tanpa instalasi, tanpa upload, tanpa pelacakan.'),
    'fr': ('Tous les Outils','Des outils puissants et faciles à utiliser qui fonctionnent entièrement dans votre navigateur. Sans installation, sans upload, sans suivi.'),
    'vi': ('Tất cả Công cụ','Công cụ mạnh mẽ, dễ sử dụng chạy hoàn toàn trong trình duyệt. Không cài đặt, không tải lên, không theo dõi.'),
    'ar': ('جميع الأدوات','أدوات قوية وسهلة الاستخدام تعمل بالكامل في متصفحك. بدون تثبيت، بدون رفع، بدون تتبع.'),
    'zh': ('全部工具','强大易用的工具，完全在浏览器中运行。无需安装，无需上传，无需追踪。'),
}

# ===== UI strings =====
UI = {
    'en': {'search':'Search 88 tools…','all':'All','noResults':'No tools found. Try a different search.'},
    'es': {'search':'Buscar 88 herramientas…','all':'Todos','noResults':'No se encontraron herramientas. Prueba otra búsqueda.'},
    'pt': {'search':'Pesquisar 88 ferramentas…','all':'Todos','noResults':'Nenhuma ferramenta encontrada. Tente outra busca.'},
    'id': {'search':'Cari 88 alat…','all':'Semua','noResults':'Alat tidak ditemukan. Coba pencarian lain.'},
    'fr': {'search':'Rechercher 88 outils…','all':'Tous','noResults':'Aucun outil trouvé. Essayez une autre recherche.'},
    'vi': {'search':'Tìm kiếm 88 công cụ…','all':'Tất cả','noResults':'Không tìm thấy công cụ. Thử tìm kiếm khác.'},
    'ar': {'search':'ابحث في 88 أداة…','all':'الكل','noResults':'لم يتم العثور على أدوات. جرب بحثًا آخر.'},
    'zh': {'search':'搜索 88 个工具…','all':'全部','noResults':'未找到工具。试试其他搜索词。'},
}

# ===== PDF subcategories (5 groups, English names per convention) =====
PDF_SUBS = {
    'organize':         {'icon':'🗂️','name':'Organize & Pages'},
    'edit_annotate':    {'icon':'✏️','name':'Edit & Annotate'},
    'compress_compare': {'icon':'🗜️','name':'Compress & Compare'},
    'convert_to':       {'icon':'📥','name':'Convert TO PDF'},
    'convert_from':     {'icon':'📤','name':'Convert FROM PDF'},
}
PDF_SUB_ORDER = ['organize','edit_annotate','compress_compare','convert_to','convert_from']

# ===== 88 tools: [slug, category, subcat_or_None, icon, name, desc, tag] =====
# Reorganization vs current homepage:
#   pdf-to-image  : Optimize -> PDF (convert_from)
#   image-to-pdf  : Optimize -> PDF (convert_to)
#   gif-splitter  : Edit     -> Create
TOOLS = [
    # --- optimize (7) ---
    ['compressor','optimize',None,'🗜️','Image Compressor','Reduce file size without losing quality. Supports JPG, PNG, WebP with adjustable compression levels. Perfect for web optimization.','Optimize'],
    ['converter','optimize',None,'🔄','Image Converter','Convert between JPG, PNG, WebP, GIF, BMP, and TIFF formats instantly. Batch conversion supported.','Convert'],
    ['heic-converter','optimize',None,'🖼️','HEIC Converter','Convert HEIC (iPhone photos) to JPG, PNG, or WebP. Free, browser-based, no uploads. Powered by heic2any.','Convert'],
    ['heic-to-jpg','optimize',None,'🖼️','HEIC to JPG','Convert iPhone HEIC photos to JPG instantly. No upload, no signup.','Convert'],
    ['image-compressor','optimize',None,'🗜️','Image Compressor','Batch compress images with adjustable quality. Reduce file size significantly.','Optimize'],
    ['svg-to-png','optimize',None,'📐','SVG to PNG','Convert SVG vector files to PNG, JPG, or WebP. High-quality rasterization at 1x-4x scale. Upload files or paste SVG code directly.','Convert'],
    ['avif-support','optimize',None,'🅰','AVIF Support','Check browser AVIF support, decode AVIF images, and convert to JPG/PNG/WebP. Test Chrome, Firefox, Safari.','Decode'],
    # --- resize (5) ---
    ['resizer','resize',None,'📐','Image Resizer','Resize images by pixel dimensions or percentage. Maintain aspect ratio or crop freely. Batch resize multiple images at once.','Resize'],
    ['cropper','resize',None,'🖼️','Image Cropper','Free-form and preset aspect ratio cropping. Perfect for social media dimensions (Instagram, Facebook, Twitter, LinkedIn).','Edit'],
    ['print-resizer','resize',None,'🖨️','Print-Ready Resizer','Resize images for printing with exact DPI and paper sizes. A4, Letter, A5, 4×6, business cards. 72-600 DPI quality control.','Resize'],
    ['circle-crop','resize',None,'⭕','Circle Crop','Crop any image into a perfect circle with transparent background. Perfect for avatars, profile pictures, and social media.','New'],
    ['image-splitter','resize',None,'✂️','Image Splitter','Split images into grid pieces for Instagram carousels and grid feeds. Supports 2×2, 3×3, and more.','Utility'],
    # --- edit (9) ---
    ['image-filters','edit',None,'🎨','Image Filters','Apply 15+ preset filters and fine-tune brightness, contrast, saturation, blur, and hue. Grayscale, sepia, vintage, vibrant and more. Instant preview.','Edit'],
    ['image-rotator','edit',None,'🔄','Image Rotator & Flipper','Rotate images by any angle or flip them horizontally and vertically. Quick 90° rotations, custom angles, and mirror effects. Fix orientation in seconds.','Edit'],
    ['image-adjust','edit',None,'🎚️','Image Adjustment','Adjust brightness, contrast, and saturation with live preview. Fix underexposed photos, boost colors, or create black-and-white effects in seconds.','Edit'],
    ['image-border','edit',None,'🖼️','Image Border & Corners','Add rounded corners and custom borders to images. Make perfect circle profile pictures, add frames to product photos, all in your browser.','Edit'],
    ['image-flip','edit',None,'🔄','Image Flip','Flip images horizontally or vertically with a mirror effect. Fix selfie orientation or create symmetric designs.','Edit'],
    ['image-grayscale','edit',None,'🎨','Image Grayscale & Color','Convert images to grayscale, sepia, or invert colors. Multiple color effects for creative projects.','Edit'],
    ['image-shadow','edit',None,'🌑','Image Drop Shadow','Add realistic drop shadow to images. Customize offset, blur, and color for e-commerce and social media.','Edit'],
    ['image-merger','edit',None,'🖼️','Image Merger & Collage','Combine multiple images into one. Create photo collages, merge horizontally or vertically. Adjust spacing, corners, and background color.','Merge'],
    ['watermark','edit',None,'🔏','Watermark Tool','Add text or image watermarks. Adjust opacity, position, size, and rotation to protect your images from unauthorized use.','Protect'],
    # --- ai (6) ---
    ['background-remover','ai',None,'✂️','Background Remover','AI-powered instant background removal. Upload an image and get a transparent PNG in seconds. Uses WebAssembly + ONNX for local processing.','AI'],
    ['image-upscaler','ai',None,'🔍','Image Upscaler','Enlarge images to 2x, 3x, or 4x with smart interpolation and sharpening. Perfect for printing, wallpapers, and high-resolution displays.','Enhance'],
    ['beauty-editor','ai',None,'💄','Beauty Editor','Retouch portraits, smooth skin, and enhance facial features with AI.','AI'],
    ['image-enhancer','ai',None,'✨','AI Image Enhancer','Enhance photos with AI filters. Adjust brightness, contrast, saturation, sharpen. Auto-enhance with one click. 100% browser-based.','New'],
    ['face-blur','ai',None,'😶','Face Blur','Automatically detect and blur faces in images. Protect privacy before sharing photos online. MediaPipe powered.','Privacy'],
    ['photo-restoration','ai',None,'🕰️','Old Photo Restoration','Restore old, scratched, and faded photos. Remove noise, fix scratches, enhance contrast, bring memories back.','New'],
    # --- create (12) ---
    ['text-on-image','create',None,'✏️','Text on Image','Add custom text to images with beautiful fonts, colors, shadows, and outlines. Drag to position, rotate, and style. Perfect for memes, quotes, and watermarks.','Create'],
    ['meme-generator','create',None,'😂','Meme Generator','Create viral memes with famous templates or your own image. Add custom top/bottom text with outline, font size, and case options.','Create'],
    ['gif-editor','create',None,'🎬','GIF Editor','Create animated GIFs from multiple images. Adjust frame delay, resize, and optimize. gif.js powered.','Create'],
    ['gif-splitter','create',None,'🎞️','GIF Splitter','Split animated GIFs into individual frames as PNG images.','Edit'],
    ['qr-code-generator','create',None,'📱','QR Code Generator','Create custom QR codes for URLs, text, WiFi, email, and SMS. Adjustable size, colors, and transparent background.','New'],
    ['signature-maker','create',None,'✍️','Signature Maker','Draw or type your digital signature. Multiple handwriting fonts, colors, and sizes. Download as transparent PNG, JPG, or SVG.','New'],
    ['favicon-generator','create',None,'🌐','Favicon Generator','Generate all favicon sizes (16-512px) plus ICO file and PWA manifest from a single image. Download as ZIP.','New'],
    ['ico-icon-generator','create',None,'🏆','ICO Icon Generator','Create ICO icon files from images for Windows apps and folders.','Design'],
    ['screenshot-to-image','create',None,'🖼️','Screenshot to Image','Wrap screenshots in beautiful frames with gradient backgrounds, rounded corners, shadows, and browser or device mockups. Perfect for social media and presentations.','Present'],
    ['social-media-post','create',None,'📱','Social Media Post Maker','Design Instagram, Facebook, Twitter, TikTok, and LinkedIn posts with text overlays. Free templates.','New'],
    ['id-photo','create',None,'📸','ID Photo Maker','Create passport, visa, and ID photos for 30+ countries. Auto-crop, background removal, proper sizing.','New'],
    ['product-white-background','create',None,'🛍️','Product White Background','Create clean white-background product photos for e-commerce. Batch backgrounds for Amazon, Mercado Libre.','New'],
    # --- utility (7) ---
    ['ocr','utility',None,'🔤','OCR Image to Text','Extract text from any image using AI-powered OCR. Supports 100+ languages, output as editable text or TXT file.','New'],
    ['bulk-processor','utility',None,'📦','Bulk Image Processor','Batch resize, convert format, and add watermark to dozens of images at once. Download all as ZIP.','New'],
    ['color-palette','utility',None,'🎨','Color Palette','Extract dominant colors from any image. Generate CSS color palettes and export as HEX, RGB, or HSL values automatically.','Analyze'],
    ['image-compare','utility',None,'📊','Image Compare','Compare two images with interactive slider, side-by-side, or overlay mode. Perfect for before/after and compression quality checks.','Analyze'],
    ['base64','utility',None,'📋','Base64 Encoder','Convert images to Base64 data URLs and vice versa. Useful for embedding images directly in HTML, CSS, or JSON files.','Utility'],
    ['metadata-viewer','utility',None,'📋','Metadata Viewer','View hidden EXIF, IPTC, XMP, and GPS metadata in images. See camera settings and location data.','Analyze'],
    ['image-exif-remover','utility',None,'🗑️','EXIF Remover','Strip hidden metadata from images to protect your privacy. Remove GPS location, camera info, and more.','Privacy'],
    # --- text (11) ---
    ['word-counter','text',None,'📝','Word Counter','Count words, characters, sentences, paragraphs, and reading time in real time. Paste any text and see statistics instantly.','Text'],
    ['json-formatter','text',None,'🔧','JSON Formatter','Format, validate, minify, and beautify JSON with syntax highlighting. Detect errors and clean up messy JSON data.','Developer'],
    ['regex-tester','text',None,'🔍','Regex Tester','Test JavaScript regular expressions with real-time matching, highlight, and detailed match info including capture groups.','Developer'],
    ['url-encoder','text',None,'🔗','URL Encoder','Percent-encode and decode URL strings, query parameters, and form data according to RFC 3986 standard.','Developer'],
    ['uuid-generator','text',None,'🆔','UUID Generator','Generate UUID v4 (random), v7 (time-ordered), and v1 (timestamp) in bulk. Up to 10,000 per generation.','Developer'],
    ['password-generator','text',None,'🔐','Password Generator','Create secure, cryptographically random passwords. Customize length, character types, exclude ambiguous characters.','Security'],
    ['case-converter','text',None,'🔠','Case Converter','Convert text to UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, and kebab-case.','Text'],
    ['text-sorter','text',None,'↕️','Text Sorter','Sort lines alphabetically, numerically, by length, reverse order, random shuffle, and remove duplicate lines.','Text'],
    ['text-diff','text',None,'↔️','Text Diff Checker','Compare two text inputs and see differences highlighted line by line. LCS-based diff algorithm, same as Git.','Developer'],
    ['text-find-replace','text',None,'🔄','Find & Replace','Search and replace text with optional regex, case sensitivity, and replace-all modes. Backreference support in regex mode.','Text'],
    ['html-encoder','text',None,'🏷️','HTML Entity Encoder','Encode special characters to HTML entities (&amp;, &lt;, &gt;, &quot;, &#39;) and decode entities back to text.','Developer'],
    # --- pdf (24, 5 subcats) ---
    ['pdf-merge','pdf','organize','🔗','PDF Merge','Combine multiple PDF files into a single PDF. Files are merged in the order you select them. All in your browser.','PDF'],
    ['pdf-split','pdf','organize','✂️','PDF Splitter','Split PDF into multiple files. Choose every N pages, specific page ranges, or extract every page as a separate file.','PDF'],
    ['pdf-delete-pages','pdf','organize','🗑️','PDF Delete Pages','Remove specific pages or page ranges from a PDF. Enter page numbers like \'2, 5-7, 10\' to delete them.','PDF'],
    ['pdf-extract-pages','pdf','organize','📑','PDF Extract Pages','Extract specific pages or ranges from a PDF into a new PDF file. Keep only the pages you need. Privacy first.','PDF'],
    ['pdf-organize','pdf','organize','📋','PDF Organize','Reorder, delete, and duplicate PDF pages via drag-and-drop thumbnails. Visual page management. 100% browser-based.','New'],
    ['pdf-rotate','pdf','organize','🔄','PDF Rotator','Rotate PDF pages 90°, 180°, or 270°. Apply to all pages or specific page ranges. Browser-based, nothing uploaded.','PDF'],
    ['pdf-crop','pdf','organize','✂️','PDF Crop','Crop PDF page regions visually. Drag to select the crop area and apply to the current page or all pages. Privacy first.','New'],
    ['pdf-number-pages','pdf','organize','🔢','PDF Number Pages','Add page numbers to PDF. Choose position (top/bottom, left/center/right), format, and starting number. Browser-based.','New'],
    ['pdf-editor','pdf','edit_annotate','✏️','PDF Editor','Add text, images, and shapes to PDF pages. Click to place elements, adjust font, size, and color. 100% in your browser.','New'],
    ['pdf-annotate','pdf','edit_annotate','🖍️','PDF Annotate','Add highlights, underlines, and text notes to PDF. Highlight passages, underline key points, and leave comments. No uploads.','New'],
    ['pdf-redact','pdf','edit_annotate','⬛','Redact PDF','Black out sensitive information in PDFs. Drag rectangles to permanently cover private data. Local processing — perfect for privacy.','New'],
    ['pdf-compress','pdf','compress_compare','🗜️','PDF Compressor','Reduce PDF file size by optimizing content, flattening annotations, and removing unnecessary metadata. Browser-based.','PDF'],
    ['pdf-compare','pdf','compress_compare','🔍','PDF Compare','Compare two PDFs side by side. Renders each page and highlights identical vs. different pages. No uploads.','New'],
    ['image-to-pdf','pdf','convert_to','📄','Image to PDF','Convert multiple images into a single PDF file. Choose page size, margins, and orientation. 100% in browser.','New'],
    ['word-to-pdf','pdf','convert_to','📄','Word to PDF','Convert Word (.docx) to PDF. Extracts text and paragraphs, renders a clean PDF. 100% in your browser.','New'],
    ['excel-to-pdf','pdf','convert_to','📊','Excel to PDF','Convert Excel (.xlsx) to PDF. Each sheet becomes a page with an auto-fitted table. Browser-based, no uploads.','New'],
    ['html-to-pdf','pdf','convert_to','🌐','HTML to PDF','Convert HTML files or pasted code to a searchable, text-based PDF. Preserves headings, paragraphs, and lists. No uploads.','New'],
    ['txt-to-pdf','pdf','convert_to','📝','TXT to PDF','Convert plain text files (.txt, .md, .log) to a clean, searchable PDF. Choose font size, page size, and font family.','New'],
    ['csv-to-pdf','pdf','convert_to','📊','CSV to PDF','Convert CSV files to formatted PDF tables. Handles quoted fields, embedded commas, and large datasets with auto-pagination.','New'],
    ['epub-to-pdf','pdf','convert_to','📚','EPUB to PDF','Convert EPUB ebooks to a searchable PDF. Extracts chapters in reading order with headings and paragraphs. 100% local.','New'],
    ['pdf-to-image','pdf','convert_from','📄','PDF to Image','Convert PDF pages to PNG, JPG, or WebP images. Render each page at 1x-3x scale. pdf.js powered.','Convert'],
    ['pdf-to-word','pdf','convert_from','📝','PDF to Word','Convert PDF to editable Word (.docx). Extracts text from each page into a clean Word document. 100% browser-based.','New'],
    ['pdf-to-excel','pdf','convert_from','📊','PDF to Excel','Convert PDF to Excel (.xlsx). Detects tabular structures and extracts text into spreadsheet rows. No uploads.','New'],
    ['pdf-to-ppt','pdf','convert_from','📑','PDF to PowerPoint','Convert PDF to PowerPoint (.pptx). Each page rendered as a high-res image slide. Perfect for presentations.','New'],
    # --- video (7) ---
    ['video-compressor','video',None,'🗜️','Video Compressor','Reduce video file size by adjusting quality (CRF) and resolution. No upload, everything processed in your browser with ffmpeg.wasm.','Video'],
    ['video-to-gif','video',None,'🎞️','Video to GIF','Convert MP4, WebM, and other videos to animated GIF. Customize start time, duration, width, and FPS for perfect output.','Video'],
    ['video-to-mp3','video',None,'🎵','Video to MP3','Extract high-quality MP3 audio from video files. Choose bitrate from 64 to 320 kbps. All processing happens locally.','Video'],
    ['video-crop','video',None,'✂️','Video Cropper','Trim and cut video to remove unwanted parts. Set precise start and end times. Lossless cut when no re-encoding needed.','Video'],
    ['video-to-frames','video',None,'🖼️','Video to Frames','Extract high-quality frames (JPG or PNG) from any video. Choose FPS interval or total frame count. Download as ZIP.','Video'],
    ['video-speed','video',None,'⏩','Video Speed Changer','Speed up or slow down video playback from 0.25x to 4x. Both video and audio adjusted correctly. Browser-based.','Video'],
    ['video-rotate','video',None,'🔃','Video Rotator','Rotate video 90°, 180°, 270° or flip horizontally/vertically. Fix wrong orientation without quality loss.','Video'],
]

# ===== ZH overrides for the 5 tool cards that were previously translated =====
ZH_OVERRIDES = {
    'heic-to-jpg':        ('HEIC 转 JPG',       '即时将 iPhone HEIC 照片转为 JPG。无需上传、无需注册。',              '转换'),
    'image-compressor':   ('图片压缩器',         '批量压缩图片，可调质量。大幅减小文件体积。',                       '优化'),
    'beauty-editor':      ('美颜编辑器',         'AI 人像修图、磨皮和面部增强。',                               'AI'),
    'gif-splitter':       ('GIF 拆分器',         '将动画 GIF 拆分为单独的 PNG 帧图片。',                           '编辑'),
    'ico-icon-generator': ('ICO 图标生成器',     '从图片创建 ICO 图标文件，用于 Windows 应用和文件夹。',                '设计'),
}

def esc(s):
    """Escape double quotes for HTML attribute safety (descriptions already HTML-escaped)."""
    return s


def tool_link_prefix(lang):
    return '/tools/' if lang == 'en' else '/' + lang + '/tools/'


def get_tool_display(tool, lang):
    """Return (name, desc, tag) for a tool, applying ZH overrides where available."""
    slug = tool[0]
    name, desc, tag = tool[4], tool[5], tool[6]
    if lang == 'zh' and slug in ZH_OVERRIDES:
        name, desc, tag = ZH_OVERRIDES[slug]
    return name, desc, tag


def generate_section(lang):
    ui = UI[lang]
    prefix = tool_link_prefix(lang)
    head_title, head_desc = SECTION[lang]

    lines = []
    lines.append('    <section class="tools-section" id="tools">')
    lines.append('      <div class="container">')
    lines.append('        <div class="section-header">')
    lines.append('          <h2>%s</h2>' % head_title)
    lines.append('          <p>%s</p>' % head_desc)
    lines.append('        </div>')
    # Toolbar: search + pills
    lines.append('        <div class="tools-toolbar">')
    lines.append('          <div class="tools-search-wrap">')
    lines.append('            <span class="tools-search-icon">🔍</span>')
    lines.append('            <input type="search" id="toolSearch" class="tools-search" placeholder="%s" aria-label="%s">' % (ui['search'], ui['search']))
    lines.append('          </div>')
    lines.append('          <nav class="tools-nav" id="toolsNav">')
    lines.append('            <a href="#tools" class="cat-pill active" data-cat="all">%s</a>' % ui['all'])
    for cat in CAT_ORDER:
        lines.append('            <a href="#cat-%s" class="cat-pill" data-cat="%s">%s %s</a>' % (cat, cat, CAT_ICONS[cat], CAT_NAMES[cat][lang]))
    lines.append('          </nav>')
    lines.append('        </div>')
    # Grid
    lines.append('        <div class="tools-grid">')

    for idx, cat in enumerate(CAT_ORDER):
        # Category header
        style = 'grid-column:1/-1;margin:8px 0 4px 0;' if idx == 0 else 'grid-column:1/-1;margin-top:8px;padding-top:16px;border-top:1px solid var(--border);'
        lines.append('          <div class="tools-category-header" id="cat-%s" data-cat-key="%s" style="%s">' % (cat, cat, style))
        lines.append('            <h3 style="font-size:1.3rem;color:var(--text-primary);margin-bottom:4px;">%s %s</h3>' % (CAT_ICONS[cat], CAT_NAMES[cat][lang]))
        lines.append('            <p style="color:var(--text-secondary);font-size:0.9rem;margin:0;">%s</p>' % CAT_DESC[cat][lang])
        lines.append('          </div>')

        if cat == 'pdf':
            # PDF: render by subcategory
            for sub in PDF_SUB_ORDER:
                sub_info = PDF_SUBS[sub]
                lines.append('          <div class="tools-subcategory-header" data-cat-key="pdf" data-sub-key="%s">' % sub)
                lines.append('            <h4>%s %s</h4>' % (sub_info['icon'], sub_info['name']))
                lines.append('          </div>')
                for tool in TOOLS:
                    if tool[1] == 'pdf' and tool[2] == sub:
                        name, desc, tag = get_tool_display(tool, lang)
                        lines.append('          <a href="%s%s" class="tool-card" data-cat="pdf" data-sub="%s">' % (prefix, tool[0], sub))
                        lines.append('            <div class="tool-icon">%s</div>' % tool[3])
                        lines.append('            <h3>%s</h3>' % name)
                        lines.append('            <p>%s</p>' % desc)
                        lines.append('            <span class="tool-tag">%s</span>' % tag)
                        lines.append('          </a>')
        else:
            # Non-PDF: render all tools in this category
            for tool in TOOLS:
                if tool[1] == cat:
                    name, desc, tag = get_tool_display(tool, lang)
                    lines.append('          <a href="%s%s" class="tool-card" data-cat="%s">' % (prefix, tool[0], cat))
                    lines.append('            <div class="tool-icon">%s</div>' % tool[3])
                    lines.append('            <h3>%s</h3>' % name)
                    lines.append('            <p>%s</p>' % desc)
                    lines.append('            <span class="tool-tag">%s</span>' % tag)
                    lines.append('          </a>')

    # No results message
    lines.append('          <div class="no-results" id="noResults" style="display:none;">%s</div>' % ui['noResults'])
    lines.append('        </div>')
    lines.append('      </div>')
    lines.append('    </section>')
    return '\n'.join(lines)


def process_file(lang):
    if lang == 'en':
        fpath = os.path.join(ROOT, 'index.html')
    else:
        fpath = os.path.join(ROOT, lang, 'index.html')
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_section = generate_section(lang)
    # Replace the tools-section (non-greedy to first </section>)
    pattern = re.compile(r'<section class="tools-section" id="tools">[\s\S]*?</section>', re.MULTILINE)
    match = pattern.search(content)
    if not match:
        print('  [WARN] tools-section not found in %s' % fpath)
        return False
    content = content[:match.start()] + new_section + content[match.end():]

    # Bump CSS version: style.css?v=N -> ?v=6
    content = re.sub(r'(style\.css\?v=)\d+', r'\g<1>6', content)
    # Bump JS version: main.js?v=N -> ?v=6
    content = re.sub(r'(main\.js\?v=)\d+', r'\g<1>6', content)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    print('=== Syncing 8 language homepages ===')
    ok = 0
    for lang in LANGS:
        if process_file(lang):
            ok += 1
            print('  [OK] %s' % lang)
        else:
            print('  [FAIL] %s' % lang)
    print('Done: %d/8 succeeded.' % ok)

    # Verification summary
    print('\n=== Verification ===')
    for lang in LANGS:
        fpath = os.path.join(ROOT, 'index.html') if lang == 'en' else os.path.join(ROOT, lang, 'index.html')
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()
        has_search = 'id="toolSearch"' in c
        has_pills = c.count('class="cat-pill"') >= 9
        has_subs = c.count('tools-subcategory-header') >= 5
        cards = c.count('class="tool-card"')
        pdf_img = 'data-cat="pdf"' in c and '/pdf-to-image"' in c
        gif_split = 'data-cat="create"' in c and '/gif-splitter"' in c
        v5 = 'style.css?v=6' in c and 'main.js?v=6' in c
        print('  %s: search=%s pills=%d subs=%d cards=%d pdf-to-image-in-pdf=%s gif-splitter-in-create=%s v5=%s' % (
            lang, has_search, c.count('class="cat-pill"'), c.count('tools-subcategory-header'), cards, pdf_img, gif_split, v5))


if __name__ == '__main__':
    main()
