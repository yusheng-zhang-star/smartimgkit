#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enrich all tool pages with smallpdf-style content sections (English source in /tools/).
Injects: selling points, feature narrative, feature grid, trust badges, expanded FAQ.
URLs and core tool functionality are NOT changed.
"""
import os, re, json

BASE = r'E:\网站项目\smartimgkit'
TOOLS_DIR = os.path.join(BASE, 'tools')

# ---------------------------------------------------------------------------
# Per-tool content data: slug -> (name, icon, category, input, output, tagline,
#   [3 use cases], [(Q,A),(Q,A)] tool-specific extra FAQs)
# ---------------------------------------------------------------------------
TOOLS = {
 # ── Optimize & Convert ──
 'compressor': ('Image Compressor','🗜️','Optimize & Convert','JPG, PNG, WebP images','a smaller image file','Reduce image file size without losing visible quality',
   ['Shrink images for faster website loading and better Core Web Vitals','Compress photos to fit email attachment size limits','Optimize product images for e-commerce listings'],
   [('What compression levels are available?','You can choose from multiple quality levels — from light (near-lossless) to strong compression for maximum size reduction.'),('Does compression change image dimensions?','No. Compression reduces file size while keeping the original pixel dimensions. Use the Resizer tool to change dimensions.')]),
 'image-compressor': ('Image Compressor','🗜️','Optimize & Convert','JPG, PNG, WebP images','a smaller image file','Shrink image files with adjustable quality',
   ['Batch-compress photos for web publishing','Reduce image weight for mobile pages','Fit large images under upload limits'],
   [('Is batch compression supported?','Yes — select multiple files and they are processed together, each downloaded individually.'),('What is the maximum reduction?','Up to 80% smaller with strong compression, depending on the original.')]),
 'converter': ('Image Converter','🔄','Optimize & Convert','JPG, PNG, WebP, GIF, BMP, TIFF','images in a new format','Convert between image formats instantly',
   ['Convert PNG to JPG to reduce file size','Turn JPG into WebP for modern web performance','Batch-convert HEIC shots for cross-platform sharing'],
   [('Which formats are supported?','JPG, PNG, WebP, GIF, BMP, and TIFF — convert any to any.','Is metadata preserved?','Basic metadata is kept; use the EXIF Remover to strip it.')]),
 'heic-converter': ('HEIC Converter','🖼️','Optimize & Convert','HEIC photos (iPhone)','JPG, PNG, or WebP','Convert iPhone HEIC photos to universal formats',
   ['Make iPhone photos viewable on Windows and Android','Convert HEIC to JPG for compatibility with older software','Turn HEIC bursts into WebP for the web'],
   [('Why does iPhone use HEIC?','HEIC offers better compression than JPG, but compatibility is limited — converting solves that.','Are Live Photos supported?','Only the still image is converted; motion data is not preserved.')]),
 'heic-to-jpg': ('HEIC to JPG','🖼️','Optimize & Convert','HEIC files','JPG images','Convert HEIC to JPG instantly',
   ['Open iPhone photos on any device','Upload HEIC shots to services that require JPG','Share photos without compatibility issues'],
   [('Is there a quality loss?','Conversion is near-lossless at high quality settings.','Can I convert multiple files?','Yes, batch conversion is supported.')]),
 'svg-to-png': ('SVG to PNG','📐','Optimize & Convert','SVG vector files','PNG, JPG, or WebP','Rasterize SVG vectors to high-resolution images',
   ['Export logos at 4x scale for retina displays','Convert SVG icons to PNG for favicons','Generate social preview images from SVG'],
   [('What scales are supported?','1x, 2x, 3x, and 4x scale for crisp high-DPI output.','Can I paste SVG code instead of uploading?','Yes — paste SVG markup directly into the tool.')]),
 'avif-support': ('AVIF Support','🅰','Optimize & Convert','AVIF images','decoded JPG/PNG/WebP','Check AVIF support and decode AVIF images',
   ['Test whether your browser supports AVIF','Decode AVIF files to JPG for editing','Convert AVIF to PNG for maximum compatibility'],
   [('What is AVIF?','AVIF is a modern image format with excellent compression, supported in Chrome and Firefox.','Why decode AVIF?','Some editors and platforms do not yet accept AVIF natively.')]),
 'pdf-to-image': ('PDF to Image','📄','Optimize & Convert','PDF documents','PNG, JPG, or WebP images','Convert PDF pages to high-quality images',
   ['Extract PDF pages as images for presentations','Turn a PDF report into shareable image slides','Render PDF pages for social media posts'],
   [('What output resolutions are available?','1x, 2x, and 3x scale for standard to high-DPI output.','Are all pages exported?','Yes — every page is rendered to its own image file.')]),
 'image-to-pdf': ('Image to PDF','📄','Optimize & Convert','JPG, PNG, WebP images','a single PDF','Combine multiple images into one PDF',
   ['Bundle product photos into a single catalog PDF','Create a PDF album from vacation pictures','Compile scanned documents into one file'],
   [('Can I set page size and orientation?','Yes — A4, Letter, and more, with portrait or landscape orientation.','Are margins adjustable?','Yes, including a no-margin option for full-bleed images.')]),
 # ── Resize & Crop ──
 'resizer': ('Image Resizer','📐','Resize & Crop','any image','a resized image','Resize images by pixels or percentage',
   ['Resize photos for social media profile pictures','Scale images down for email thumbnails','Batch-resize product images to a uniform size'],
   [('Can I keep the aspect ratio?','Yes — enable "maintain aspect ratio" to avoid distortion.','Is batch resize supported?','Yes, resize multiple images at once with the same settings.')]),
 'cropper': ('Image Cropper','🖼️','Resize & Crop','any image','a cropped image','Crop images with free-form or preset ratios',
   ['Crop photos to Instagram, Facebook, and Twitter sizes','Remove unwanted edges from a screenshot','Frame a subject with aspect-ratio presets'],
   [('What aspect ratio presets are available?','1:1, 4:3, 16:9, 3:2, and common social media sizes.','Can I crop freely?','Yes — drag the crop box to any dimensions.')]),
 'print-resizer': ('Print-Ready Resizer','🖨️','Resize & Crop','any image','a print-ready image','Resize images for exact print sizes and DPI',
   ['Prepare photos for 4×6 prints at 300 DPI','Size images for A4 and Letter paper','Create business-card-sized images at 600 DPI'],
   [('What DPI range is supported?','72 to 600 DPI for screen to high-quality print.','Which paper sizes are included?','A4, A5, Letter, 4×6, and business card sizes.')]),
 'circle-crop': ('Circle Crop','⭕','Resize & Crop','any image','a circular image','Crop images into a perfect circle',
   ['Create circular profile pictures for social media','Make rounded avatars for team pages','Design circular logo badges'],
   [('Is the background transparent?','Yes — the area outside the circle is transparent (PNG).','Can I adjust the circle position?','Yes — drag to position the circle over your subject.')]),
 'image-splitter': ('Image Splitter','✂️','Resize & Crop','any image','a grid of image pieces','Split images into grid pieces',
   ['Create Instagram carousel grids from one image','Split a panorama into swipeable tiles','Cut a large image into printable sections'],
   [('What grid sizes are supported?','2×2, 3×3, and custom row/column counts.','Are pieces exported individually?','Yes — each piece is downloaded, or all as a ZIP.')]),
 'video-crop': ('Video Crop','🎬','Resize & Crop','video files','a cropped video','Crop video to any aspect ratio',
   ['Crop vertical video to 16:9 for YouTube','Reframe a video for Instagram squares','Remove unwanted borders from footage'],
   [('What video formats are supported?','MP4, WebM, and other browser-playable formats.','Is there a duration limit?','Long videos are supported but may take time to process.')]),
 # ── Edit & Effects ──
 'image-filters': ('Image Filters','🎨','Edit & Effects','any image','a filtered image','Apply 15+ preset filters and fine-tune settings',
   ['Apply vintage or sepia filters for a retro look','Boost dull photos with vibrant presets','Create consistent filter styles for a feed'],
   [('What adjustments can I fine-tune?','Brightness, contrast, saturation, blur, and hue.','Is there a live preview?','Yes — every change previews instantly before download.')]),
 'image-rotator': ('Image Rotator & Flipper','🔄','Edit & Effects','any image','a rotated or flipped image','Rotate by any angle or flip images',
   ['Fix sideways photos from cameras','Mirror an image for symmetric designs','Rotate a scanned document upright'],
   [('Can I rotate by custom angles?','Yes — any angle, plus quick 90° buttons.','What is the difference between flip and mirror?','Flip swaps pixels horizontally or vertically; rotate turns the whole image.')]),
 'image-adjust': ('Image Adjustment','🎚️','Edit & Effects','any image','an adjusted image','Adjust brightness, contrast, and saturation',
   ['Fix underexposed dark photos','Boost faded colors','Create a balanced look for product shots'],
   [('Is the preview live?','Yes — sliders update the image in real time.','Can I reset adjustments?','Yes — reset to original with one click.')]),
 'image-border': ('Image Border & Corners','🖼️','Edit & Effects','any image','an image with borders','Add rounded corners and custom borders',
   ['Add rounded corners to product thumbnails','Frame photos with colored borders','Make perfect circle profile pictures'],
   [('Can I set border color and width?','Yes — any color and pixel width.','Are rounded corners adjustable?','Yes — from slight rounding to a full circle.')]),
 'image-flip': ('Image Flip','🔄','Edit & Effects','any image','a flipped image','Flip images horizontally or vertically',
   ['Fix mirrored selfie orientation','Create symmetric designs by flipping','Correct scanned negatives'],
   [('Does flipping reduce quality?','No — flipping is lossless.','Can I flip and rotate together?','Yes — combine flips and rotations freely.')]),
 'image-grayscale': ('Image Grayscale & Color','🎨','Edit & Effects','any image','a grayscale or recolored image','Convert to grayscale, sepia, or invert colors',
   ['Create black-and-white photos','Apply sepia for a vintage feel','Invert colors for negative effects'],
   [('What color effects are available?','Grayscale, sepia, and color inversion.','Can I adjust the effect intensity?','Yes — partial effects are supported.')]),
 'image-shadow': ('Image Drop Shadow','🌑','Edit & Effects','any image','an image with shadow','Add realistic drop shadows',
   ['Add depth to product photos for e-commerce','Create shadow effects for design elements','Give logos a floating look'],
   [('Can I customize the shadow?','Yes — offset, blur radius, and color.','Is the background transparent?','Yes — output is PNG with transparency.')]),
 'image-merger': ('Image Merger','🧩','Edit & Effects','multiple images','one combined image','Merge multiple images side by side or stacked',
   ['Create before-and-after comparisons','Combine photos into a contact sheet','Build a collage layout'],
   [('What merge layouts are supported?','Horizontal, vertical, and grid layouts.','Can I set gaps between images?','Yes — adjustable spacing and background color.')]),
 'watermark': ('Watermark','💧','Edit & Effects','any image','a watermarked image','Add text or image watermarks',
   ['Protect photos with a copyright watermark','Brand product images with a logo','Add a subtle signature to artwork'],
   [('Can I use an image as a watermark?','Yes — upload a logo PNG and position it anywhere.','Is opacity adjustable?','Yes — from faint to fully opaque.')]),
 'gif-editor': ('GIF Editor','🎞️','Edit & Effects','GIF files','an edited GIF','Edit, optimize, and customize animated GIFs',
   ['Trim GIFs to a shorter loop','Optimize GIF file size','Adjust GIF playback speed'],
   [('Can I extract frames from a GIF?','Yes — split a GIF into individual frames.','Is frame-by-frame editing supported?','Yes — view and edit each frame.')]),
 'gif-splitter': ('GIF Splitter','🎞️','Edit & Effects','GIF files','individual frames','Split animated GIFs into frames',
   ['Extract specific frames from a GIF','Convert GIF frames to PNG for editing','Analyze GIF animation frame by frame'],
   [('What format are the frames?','PNG images, one per frame.','Can I download all frames at once?','Yes — as a ZIP archive.')]),
 # ── AI Enhance ──
 'background-remover': ('Background Remover','✨','AI Enhance','any image','an image with transparent background','Remove image backgrounds instantly with AI',
   ['Create product cutouts for e-commerce listings','Make transparent PNGs for design overlays','Remove backgrounds from profile photos'],
   [('How does AI background removal work?','A neural network segments the subject from the background — entirely in your browser.','Is the output transparent?','Yes — the background becomes transparent (PNG with alpha).')]),
 'image-enhancer': ('Image Enhancer','🌟','AI Enhance','any photo','an enhanced photo','Enhance photo clarity and detail',
   ['Sharpen blurry photos','Bring out detail in soft images','Improve old or low-quality pictures'],
   [('Does enhancement work on all photos?','It works best on photos with mild blur or softness.','Is the process automatic?','Yes — one-click enhancement with no settings needed.')]),
 'image-upscaler': ('Image Upscaler','🔍','AI Enhance','any image','an upscaled image','Upscale images up to 4x with AI',
   ['Enlarge low-resolution photos for printing','Upscale icons for high-DPI displays','Improve small images for presentations'],
   [('What scale factors are supported?','2x and 4x upscaling.','Does upscaling add real detail?','AI upscaling intelligently fills in detail, though it cannot create information that is not present.')]),
 'face-blur': ('Face Blur','🙈','AI Enhance','any photo','a photo with blurred faces','Automatically blur faces for privacy',
   ['Protect identities in street photography','Blur faces of minors before sharing','Anonymize people in documentary photos'],
   [('How are faces detected?','A browser-based face-detection model finds faces automatically.','Can I blur manually?','Yes — you can adjust or add blur regions manually.')]),
 'beauty-editor': ('Beauty Editor','💄','AI Enhance','any portrait','a retouched portrait','Retouch portraits and smooth skin',
   ['Smooth skin in portrait photos','Brighten and even out skin tone','Quick touch-ups for headshots'],
   [('Is the retouching natural-looking?','Yes — subtle adjustments that preserve natural features.','Can I control the strength?','Yes — adjustable intensity sliders.')]),
 'photo-restoration': ('Photo Restoration','🖼️','AI Enhance','old photos','a restored photo','Restore and enhance old photographs',
   ['Revive faded vintage family photos','Repair old scanned pictures','Bring color and clarity to aged photos'],
   [('Does it add color to black-and-white photos?','It enhances clarity; colorization is a separate enhancement.','What photo conditions are best?','Scanned old photos at the highest available resolution work best.')]),
 'product-white-background': ('Product White Background','🛍️','AI Enhance','product photos','a product on white background','Place products on a clean white background',
   ['Standardize e-commerce product images','Create marketplace-ready white-bg photos','Clean up product shots for catalogs'],
   [('How does it work?','The background is removed and replaced with pure white.','Is the product cutout accurate?','AI segmentation produces clean edges around the product.')]),
 'id-photo': ('ID Photo Maker','🪪','AI Enhance','a portrait photo','a compliant ID photo','Create ID photos with correct sizes and backgrounds',
   ['Make passport photos at home','Generate visa-size photos','Create student or employee ID photos'],
   [('What ID sizes are supported?','Passport, visa, and common national ID dimensions.','Can I change the background color?','Yes — white, blue, and red background options.')]),
 'ocr': ('OCR Text Recognition','🔤','AI Enhance','images with text','extracted text','Extract text from images with OCR',
   ['Digitize printed documents from photos','Extract text from screenshots','Convert scanned pages to editable text'],
   [('What languages does OCR support?','Multiple languages including English, with Latin-script text.','Does it work on handwriting?','OCR is optimized for printed text; handwriting accuracy varies.')]),
 # ── Create & Design ──
 'text-on-image': ('Text on Image','✍️','Create & Design','any image','an image with text overlay','Add stylish text to images',
   ['Create social media graphics with captions','Design image quotes and posters','Add labels and titles to photos'],
   [('Can I customize the font and color?','Yes — font family, size, color, and position are all adjustable.','Is text positioning flexible?','Yes — drag text to any position on the image.')]),
 'meme-generator': ('Meme Generator','😂','Create & Design','any image','a finished meme','Create memes with classic and custom text',
   ['Make classic top/bottom text memes','Design reaction memes for social media','Create custom memes from your photos'],
   [('Are classic meme templates included?','Yes — popular templates are built in.','Can I use my own image?','Yes — upload any image to meme-ify.')]),
 'signature-maker': ('Signature Maker','✒️','Create & Design','mouse or touch input','a signature image','Draw and export your signature',
   ['Create a digital signature for documents','Sign PDFs with a personal signature','Generate a clean signature PNG'],
   [('Can I draw with a mouse or stylus?','Yes — both are supported, plus touch on mobile.','What format is the signature?','Transparent PNG, ready to place on any document.')]),
 'favicon-generator': ('Favicon Generator','⭐','Create & Design','an image or logo','favicon files','Create favicons for your website',
   ['Generate a 16x16 and 32x32 favicon','Create favicons from a logo','Make app icons for browsers'],
   [('What sizes are generated?','16x16, 32x32, and 180x180 for Apple touch icons.','What format is the output?','ICO and PNG formats.')]),
 'ico-icon-generator': ('ICO Icon Generator','🏆','Create & Design','an image','an .ico file','Convert images to ICO icon files',
   ['Create Windows icons from images','Generate app icons','Make folder icons for desktop'],
   [('What sizes are in the ICO?','Multi-resolution: 16, 32, 48, and 64 pixels.','Can I use a PNG as input?','Yes — any raster image works.')]),
 'qr-code-generator': ('QR Code Generator','📱','Create & Design','a URL or text','a QR code image','Generate QR codes for links and text',
   ['Create QR codes for website links','Generate QR codes for Wi-Fi or contact info','Make QR codes for print materials'],
   [('Can I customize the QR code?','Yes — size, color, and error-correction level.','What can I encode?','URLs, text, phone numbers, and more.')]),
 'social-media-post': ('Social Media Post Maker','🖼️','Create & Design','any image','social-media-sized images','Create images sized for social platforms',
   ['Make Instagram post and story images','Create Facebook cover photos','Design Twitter header images'],
   [('Which platforms are supported?','Instagram, Facebook, Twitter, LinkedIn, and more.','Are the sizes preset?','Yes — correct dimensions for each platform are built in.')]),
 'screenshot-to-image': ('Screenshot to Image','📸','Create & Design','a screenshot','a polished image','Convert and enhance screenshots',
   ['Pretty-up screenshots for tutorials','Convert screenshot formats','Add frames to screenshots'],
   [('What screenshot formats work?','PNG, JPG, and other common image formats.','Can I crop the screenshot?','Yes — crop to the relevant area.')]),
 # ── Utility & Analyze ──
 'color-palette': ('Color Palette Extractor','🎨','Utility & Analyze','any image','a color palette','Extract dominant colors from images',
   ['Build a brand palette from a photo','Find matching colors for a design','Analyze the color scheme of an image'],
   [('How many colors are extracted?','The top 5–10 dominant colors.','Are color codes provided?','Yes — HEX codes for each color, ready to copy.')]),
 'metadata-viewer': ('Metadata Viewer','📋','Utility & Analyze','an image file','EXIF metadata','View EXIF and image metadata',
   ['Check camera settings used for a photo','Find the GPS location in an image','Verify image dimensions and format'],
   [('What metadata is shown?','EXIF fields like camera, lens, settings, GPS, and timestamps.','Is the metadata removed on download?','No — this tool only views metadata; use the EXIF Remover to strip it.')]),
 'image-exif-remover': ('EXIF Remover','🚫','Utility & Analyze','an image file','a clean image','Strip EXIF metadata from images',
   ['Remove GPS location before sharing photos','Strip camera info for privacy','Clean metadata before uploading online'],
   [('What metadata is removed?','EXIF fields including GPS, camera info, and timestamps.','Is the image quality affected?','No — only metadata is removed; pixels stay identical.')]),
 'image-compare': ('Image Compare','🔍','Utility & Analyze','two images','a visual comparison','Compare two images side by side',
   ['Spot differences between two versions','Compare before-and-after edits','Quality-check retouched images'],
   [('How are differences shown?','Side-by-side and overlay modes highlight differences.','Is pixel-level comparison supported?','Yes — a difference map shows changed pixels.')]),
 'bulk-processor': ('Bulk Processor','⚡','Utility & Analyze','multiple images','processed images','Batch-process many images at once',
   ['Apply the same edit to dozens of images','Batch-resize or compress a folder of photos','Automate repetitive image tasks'],
   [('What operations can be batched?','Resize, compress, convert, and more — applied to every file.','Is there a file count limit?','Limited only by your browser memory; hundreds of files work fine.')]),
 'word-counter': ('Word Counter','🔢','Utility & Analyze','text','word statistics','Count words, characters, and reading time',
   ['Check essay word counts','Estimate reading time for articles','Analyze text length for SEO'],
   [('What statistics are shown?','Words, characters, sentences, paragraphs, and reading time.','Is it accurate for all languages?','Yes — works for any text input.')]),
 'case-converter': ('Case Converter','🔠','Utility & Analyze','text','converted text','Convert text between cases',
   ['Convert to Title Case for headlines','Switch to UPPER or lower case','Fix sentence case in paragraphs'],
   [('What cases are supported?','UPPER, lower, Title, Sentence, and camelCase.','Is it instant?','Yes — conversion happens as you type.')]),
 'text-sorter': ('Text Sorter','🔤','Utility & Analyze','lines of text','sorted text','Sort and organize lines of text',
   ['Sort lists alphabetically','Remove duplicate lines','Reverse line order'],
   [('What sort options are there?','Alphabetical, numeric, reverse, and deduplicate.','Can it handle large lists?','Yes — thousands of lines are processed instantly.')]),
 'text-find-replace': ('Text Find & Replace','🔎','Utility & Analyze','text','edited text','Find and replace text with patterns',
   ['Bulk-replace words across text','Use regex for advanced replacements','Clean up formatting in text'],
   [('Is regex supported?','Yes — full regular expression find-and-replace.','Can I preview changes?','Yes — see matches before applying.')]),
 # ── Text & Developer Tools ──
 'base64': ('Base64 Encoder/Decoder','🔐','Text & Developer Tools','text or images','base64 strings','Encode and decode Base64 data',
   ['Encode images as Base64 for inline CSS','Decode Base64 strings to text','Convert data URIs for embedding'],
   [('Can it handle images?','Yes — encode image files to Base64 data URIs.','Is decoding accurate?','Yes — lossless round-trip encoding and decoding.')]),
 'html-encoder': ('HTML Encoder/Decoder','💻','Text & Developer Tools','text','HTML entities','Encode and decode HTML entities',
   ['Escape HTML special characters','Prepare text for safe HTML display','Decode entity-encoded content'],
   [('What characters are escaped?','<, >, &, ", and \' — the core HTML entities.','Is it bidirectional?','Yes — encode and decode both supported.')]),
 'url-encoder': ('URL Encoder/Decoder','🔗','Text & Developer Tools','text or URLs','encoded URLs','Encode and decode URL components',
   ['Encode query parameters safely','Decode encoded URLs for debugging','Prepare text for URL inclusion'],
   [('Does it follow RFC 3986?','Yes — standard percent-encoding for URLs.','Can it encode full URLs?','Yes — encode components or full URLs.')]),
 'json-formatter': ('JSON Formatter','📋','Text & Developer Tools','JSON text','formatted JSON','Format, validate, and beautify JSON',
   ['Pretty-print minified JSON','Validate JSON syntax errors','Beautify API responses for reading'],
   [('Does it validate JSON?','Yes — syntax errors are highlighted with line numbers.','Can it minify JSON?','Yes — switch between beautify and minify.')]),
 'regex-tester': ('Regex Tester','🧪','Text & Developer Tools','a regex pattern','match results','Test regular expressions live',
   ['Debug regex patterns','Test matches against sample text','Learn regex with live feedback'],
   [('Are match highlights shown?','Yes — matches are highlighted in the input text.','What regex flavor is used?','Standard JavaScript regular expressions.')]),
 'text-diff': ('Text Diff','📝','Text & Developer Tools','two text blocks','a diff view','Compare two text blocks and show differences',
   ['Compare two document versions','Find changes between text drafts','Review code or text edits'],
   [('How are differences shown?','Added and removed lines are highlighted in color.','Is it line-by-line?','Yes — classic line-based diff.')]),
 'password-generator': ('Password Generator','🔑','Text & Developer Tools','settings','a strong password','Generate secure random passwords',
   ['Create strong passwords for accounts','Generate passphrases for security keys','Make unique passwords per site'],
   [('Can I set length and character sets?','Yes — length, uppercase, lowercase, numbers, and symbols.','Are passwords generated locally?','Yes — entirely in your browser, never transmitted.')]),
 'uuid-generator': ('UUID Generator','🆔','Text & Developer Tools','settings','UUID values','Generate UUIDs (GUIDs)',
   ['Generate unique IDs for databases','Create UUIDs for distributed systems','Produce test identifiers'],
   [('What UUID versions are supported?','UUID v4 (random) is generated by default.','Can I batch-generate?','Yes — generate multiple UUIDs at once.')]),
 # ── PDF Tools ──
 'pdf-merge': ('PDF Merge','🔗','PDF Tools','multiple PDFs','one merged PDF','Combine multiple PDFs into one',
   ['Combine scanned pages into a single document','Merge multiple reports into one file','Join PDF chapters into a book'],
   [('Is there a file count limit?','No hard limit — merge as many PDFs as your browser can handle.','Are bookmarks preserved?','Page content is merged; the original file order is followed.')]),
 'pdf-split': ('PDF Split','✂️','PDF Tools','one PDF','multiple PDFs','Split a PDF into separate files',
   ['Extract chapters as separate PDFs','Split a large PDF into smaller chunks','Separate pages for individual sharing'],
   [('Can I split by page ranges?','Yes — define custom ranges or split every N pages.','Are split files individual PDFs?','Yes — each output is a valid standalone PDF.')]),
 'pdf-rotate': ('PDF Rotate','🔄','PDF Tools','a PDF','a rotated PDF','Rotate PDF pages',
   ['Fix sideways scanned pages','Rotate landscape pages to portrait','Correct orientation across a document'],
   [('Can I rotate individual pages?','Yes — rotate all pages or selected ones.','What rotations are supported?','90°, 180°, and 270° clockwise or counterclockwise.')]),
 'pdf-compress': ('PDF Compress','🗜️','PDF Tools','a PDF','a smaller PDF','Reduce PDF file size',
   ['Shrink PDFs for email attachments','Compress scanned documents','Reduce PDF size for web upload'],
   [('How much can a PDF shrink?','Reduction depends on content — image-heavy PDFs compress most.','Is quality preserved?','Yes — text stays crisp; images are re-encoded at a balanced quality.')]),
 'pdf-extract-pages': ('PDF Extract Pages','📄','PDF Tools','a PDF','selected pages as PDF','Extract specific pages from a PDF',
   ['Pull out the pages you need','Create a subset of a document','Share only relevant pages'],
   [('Can I choose any pages?','Yes — select individual pages or ranges.','Is the output a valid PDF?','Yes — extracted pages form a standalone PDF.')]),
 'pdf-delete-pages': ('PDF Delete Pages','🗑️','PDF Tools','a PDF','a PDF with pages removed','Remove unwanted pages from a PDF',
   ['Delete blank pages','Remove sensitive pages before sharing','Trim a document to its essentials'],
   [('Can I preview before deleting?','Yes — page thumbnails help you choose.','Is the original modified?','No — a new PDF is created without the deleted pages.')]),
 'pdf-to-word': ('PDF to Word','📝','PDF Tools','a PDF','an editable .docx','Convert PDF to editable Word',
   ['Edit PDF content in Microsoft Word','Extract text from a PDF report','Convert a PDF letter to a Word doc'],
   [('Is the output editable?','Yes — real .docx text you can edit, not images.','Are tables preserved?','Text and basic structure are extracted; complex layouts may simplify.')]),
 'pdf-to-excel': ('PDF to Excel','📊','PDF Tools','a PDF','an .xlsx spreadsheet','Convert PDF tables to Excel',
   ['Extract financial tables from PDF reports','Turn PDF data into editable spreadsheets','Convert bank statements to Excel'],
   [('How are tables detected?','The tool analyzes text X/Y positions to reconstruct rows and columns.','Does it work on scanned PDFs?','No — scanned PDFs need OCR first; this tool reads text layers.')]),
 'pdf-to-ppt': ('PDF to PPT','📑','PDF Tools','a PDF','a .pptx presentation','Convert PDF to PowerPoint',
   ['Turn a PDF report into a presentation','Create slides from a PDF document','Reuse PDF content in slide decks'],
   [('How are pages converted?','Each PDF page becomes a high-resolution image slide.','Is the text editable?','Slides contain page images; for editable text use PDF to Word.')]),
 'word-to-pdf': ('Word to PDF','📄','PDF Tools','a .docx file','a PDF','Convert Word documents to PDF',
   ['Share a Word doc as a non-editable PDF','Preserve formatting for printing','Convert resumes to PDF'],
   [('Is formatting preserved?','Text and paragraphs are rendered cleanly into the PDF.','Are fonts embedded?','Standard fonts are used for broad compatibility.')]),
 'excel-to-pdf': ('Excel to PDF','📊','PDF Tools','an .xlsx file','a PDF','Convert Excel spreadsheets to PDF',
   ['Share spreadsheets as read-only PDFs','Print Excel sheets with proper formatting','Archive financial data as PDF'],
   [('How are sheets handled?','Each worksheet becomes a page with an auto-fitted table.','Are large tables paginated?','Yes — wide tables flow across pages intelligently.')]),
 'pdf-editor': ('PDF Editor','✏️','PDF Tools','a PDF','an edited PDF','Add text, images, and shapes to PDFs',
   ['Annotate contracts before signing','Add notes and labels to PDF documents','Insert images into PDF reports'],
   [('What can I add to a PDF?','Text boxes, images, and shapes — placed anywhere on a page.','Is the original modified?','No — a new edited PDF is created.')]),
 'pdf-annotate': ('PDF Annotate','🖍️','PDF Tools','a PDF','an annotated PDF','Add highlights, underlines, and notes',
   ['Highlight key passages in study material','Underline important contract clauses','Add review notes to documents'],
   [('What annotation types are supported?','Highlights, underlines, and text comments.','Can I annotate multiple pages?','Yes — navigate and annotate every page.')]),
 'pdf-number-pages': ('PDF Number Pages','🔢','PDF Tools','a PDF','a numbered PDF','Add page numbers to PDFs',
   ['Number pages in a report','Add page numbers to a thesis','Index a long document'],
   [('Where can numbers appear?','Top or bottom, left, center, or right of each page.','What number formats are supported?','Plain numbers, "Page N", and "Page N of Total".')]),
 'pdf-crop': ('PDF Crop','✂️','PDF Tools','a PDF','a cropped PDF','Crop PDF page regions',
   ['Remove margins from a PDF','Trim unwanted borders from scanned pages','Focus on a specific area of a page'],
   [('Can I crop all pages at once?','Yes — apply the crop to the current page or every page.','Is the crop visual?','Yes — drag to select the crop area on a page preview.')]),
 'pdf-organize': ('PDF Organize','📋','PDF Tools','a PDF','a reorganized PDF','Reorder, delete, and duplicate pages',
   ['Rearrange pages in a document','Delete unwanted pages','Duplicate pages for repetition'],
   [('Can I drag pages to reorder?','Yes — drag-and-drop thumbnails to reorder pages.','Can I duplicate pages?','Yes — duplicate any page with one click.')]),
 'pdf-compare': ('PDF Compare','🔍','PDF Tools','two PDFs','a page-by-page comparison','Compare two PDFs side by side',
   ['Spot differences between contract versions','Compare revised and original documents','Verify changes across PDF drafts'],
   [('How are differences shown?','Each page pair is marked identical or different.','Is the comparison visual?','Yes — pages are rendered and compared pixel by pixel.')]),
 'pdf-redact': ('Redact PDF','⬛','PDF Tools','a PDF','a redacted PDF','Black out sensitive information in PDFs',
   ['Hide personal data before sharing','Redact confidential sections','Protect privacy in legal documents'],
   [('Is redaction permanent?','Yes — black rectangles are burned into the PDF, covering underlying content.','Can I redact multiple areas?','Yes — draw as many redaction rectangles as needed.')]),
 'html-to-pdf': ('HTML to PDF','🌐','PDF Tools','HTML files or code','a searchable PDF','Convert HTML to PDF',
   ['Save web content as a PDF','Convert HTML emails to PDF','Archive web pages as documents'],
   [('Is the PDF searchable?','Yes — real text, selectable and searchable.','Does it preserve CSS styling?','Document structure (headings, paragraphs, lists) is preserved; exact CSS layout is not.')]),
 'txt-to-pdf': ('TXT to PDF','📝','PDF Tools','text files','a searchable PDF','Convert text files to PDF',
   ['Convert notes to a shareable PDF','Turn log files into documents','Create a PDF from a markdown draft'],
   [('What text formats work?','.txt, .md, and .log — any plain text file.','Is the PDF searchable?','Yes — real text output.')]),
 'csv-to-pdf': ('CSV to PDF','📊','PDF Tools','CSV files','a formatted PDF table','Convert CSV data to PDF tables',
   ['Create a PDF report from CSV data','Share spreadsheet data as a PDF','Archive tabular data in PDF'],
   [('Does it handle quoted fields?','Yes — RFC 4180 compliant, including commas inside quotes.','Are large datasets supported?','Yes, with auto-pagination across pages.')]),
 'epub-to-pdf': ('EPUB to PDF','📚','PDF Tools','EPUB ebooks','a searchable PDF','Convert EPUB ebooks to PDF',
   ['Read ebooks on PDF-only devices','Print chapters from an ebook','Archive an ebook library as PDF'],
   [('Are chapters preserved?','Yes — extracted in reading order with headings.','Is the PDF searchable?','Yes — real text, selectable and searchable.')]),
 # ── Video Tools ──
 'video-rotate': ('Video Rotate','🔄','Video Tools','a video','a rotated video','Rotate videos to any orientation',
   ['Fix sideways phone videos','Rotate vertical video to horizontal','Correct orientation before sharing'],
   [('What rotations are supported?','90°, 180°, and 270°.','Are all video formats supported?','MP4, WebM, and other browser-playable formats.')]),
 'video-speed': ('Video Speed','⏩','Video Tools','a video','a speed-adjusted video','Change video playback speed',
   ['Create slow-motion clips','Speed up long footage for timelapse','Adjust speed for highlight reels'],
   [('What speed range is supported?','0.25x to 4x playback speed.','Is audio affected?','Audio pitch is adjusted with the speed.')]),
 'video-to-frames': ('Video to Frames','🎞️','Video Tools','a video','individual frames','Extract frames from a video',
   ['Grab stills from a video clip','Extract frames for animation','Capture a perfect still moment'],
   [('What format are frames?','PNG or JPG images.','Can I extract every frame?','Yes — or extract at a set interval.')]),
 'video-to-mp3': ('Video to MP3','🎵','Video Tools','a video','an MP3 audio file','Extract audio from videos as MP3',
   ['Pull audio from a music video','Extract a soundtrack from a clip','Save a video interview as audio'],
   [('What audio format is output?','MP3 audio, extracted from the video track.','Is there a length limit?','Long videos are supported but take longer to process.')]),
 'video-to-gif': ('Video to GIF','🎞️','Video Tools','a video','an animated GIF','Convert video clips to GIFs',
   ['Create GIFs for social media','Make animated stickers from video','Turn a clip into a looping GIF'],
   [('Can I trim the GIF?','Yes — select the start and end of the clip.','What is the output format?','Animated GIF, optimized for size.')]),
 'video-compressor': ('Video Compressor','🗜️','Video Tools','a video','a smaller video','Reduce video file size',
   ['Compress videos for email','Shrink footage for web upload','Reduce video size for storage'],
   [('How much can videos shrink?','Significant reduction with adjustable quality.','Is quality preserved?','Yes — balanced compression keeps quality acceptable.')]),
}

# ---------------------------------------------------------------------------
# Category-level data: feature grids and common FAQs
# ---------------------------------------------------------------------------
CATEGORY = {
 'Optimize & Convert': {
   'features': [
     ('⚡','Instant Conversion','Files are processed in your browser the moment you upload — no waiting in a queue.'),
     ('🔒','100% Private','Your files never leave your device. Everything runs locally in your browser.'),
     ('🎯','Adjustable Quality','Fine-tune compression or output settings to balance size and quality.'),
     ('📦','Batch Support','Process multiple files at once and download them together.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no hidden limits — completely free.'),
     ('🌐','Cross-Platform','Works on Windows, Mac, Linux, iOS, and Android — any modern browser.'),
   ],
   'faqs': [('Is there a file size limit?','Files up to 100MB are supported. Very large files may take a few extra seconds to process.'),('Do I need to install anything?','No. Everything runs in your browser — no apps, plugins, or extensions.')]
 },
 'Resize & Crop': {
   'features': [
     ('📐','Precise Dimensions','Set exact pixel sizes or percentages for pixel-perfect results.'),
     ('🔗','Aspect-Ratio Lock','Maintain proportions automatically to avoid distortion.'),
     ('✂️','Free-Form & Presets','Crop freely or use social-media-ready aspect-ratio presets.'),
     ('🔒','100% Private','All processing is local — your images never leave your browser.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no hidden limits.'),
     ('🌐','Cross-Platform','Works on any device with a modern browser.'),
   ],
   'faqs': [('Will resizing reduce quality?','Resizing uses high-quality interpolation. Upscaling cannot add detail that is not present in the original.'),('Can I process multiple images?','Yes — batch processing is supported for resize and crop operations.')]
 },
 'Edit & Effects': {
   'features': [
     ('🎨','Live Preview','See every adjustment instantly before you download.'),
     ('🎚️','Fine Controls','Adjust intensity, color, and position with precise sliders.'),
     ('🔄','Non-Destructive','Your original image is never modified — download a new copy.'),
     ('🔒','100% Private','All editing happens locally in your browser.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no limits.'),
     ('⚡','Instant Results','Edits apply instantly — no rendering queue.'),
   ],
   'faqs': [('Are edits reversible?','Yes — reset to the original at any time before downloading. Your source file is untouched.'),('Do edits work on all image formats?','Yes — JPG, PNG, WebP, and other common formats are supported.')]
 },
 'AI Enhance': {
   'features': [
     ('🤖','AI-Powered','Neural networks run in your browser — no cloud, no uploads.'),
     ('⚡','One-Click Results','Automatic enhancement with no complex settings.'),
     ('🔒','100% Private','Your photos are processed locally and never uploaded.'),
     ('🎯','Natural Results','Enhancements preserve a natural, unforced look.'),
     ('🆓','Free Forever','No sign-up, no credits, no watermarks.'),
     ('🌐','Cross-Platform','Works on any device with a modern browser.'),
   ],
   'faqs': [('Does AI processing happen on a server?','No. The AI models run entirely in your browser using WebAssembly and WebGL.'),('What if the result is not perfect?','AI enhancement is a starting point — use the Edit tools for fine-tuning.')]
 },
 'Create & Design': {
   'features': [
     ('✍️','Full Customization','Control fonts, colors, sizes, and positions.'),
     ('📐','Preset Sizes','Start with correct dimensions for social media and print.'),
     ('🎨','Live Preview','See your design update in real time.'),
     ('🔒','100% Private','All design work happens locally in your browser.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no limits.'),
     ('📤','Export Ready','Download production-ready images instantly.'),
   ],
   'faqs': [('Can I use my own images and fonts?','Yes — upload your own assets and use built-in font options.'),('Are the outputs watermarked?','No. Your downloads are clean and watermark-free.')]
 },
 'Utility & Analyze': {
   'features': [
     ('⚡','Instant Analysis','Results appear the moment you upload or paste.'),
     ('📋','Detailed Output','Get precise statistics, codes, or comparisons.'),
     ('🔒','100% Private','All analysis is local — nothing is uploaded.'),
     ('🔄','Non-Destructive','Your original files are never modified.'),
     ('🆓','Free Forever','No sign-up, no limits, completely free.'),
     ('🌐','Cross-Platform','Works on any device with a modern browser.'),
   ],
   'faqs': [('Is the analysis accurate?','Yes — tools use standard algorithms and parsers for reliable results.'),('Can I process multiple files?','Yes — batch analysis is supported where relevant.')]
 },
 'Text & Developer Tools': {
   'features': [
     ('⚡','Instant Processing','Conversion and validation happen as you type.'),
     ('🧪','Developer-Grade','Built for accurate, standards-compliant results.'),
     ('🔒','100% Private','All processing is local — no data is sent anywhere.'),
     ('📋','Copy & Export','One-click copy to clipboard for quick use.'),
     ('🆓','Free Forever','No sign-up, no API keys, no limits.'),
     ('🔧','Regex & JSON Support','Full regular expression and JSON validation built in.'),
   ],
   'faqs': [('Are these tools accurate enough for production?','Yes — they follow standard specifications (RFC 3986, JSON spec, etc.).'),('Is my input stored?','No. Everything is processed in your browser and discarded when you close the tab.')]
 },
 'PDF Tools': {
   'features': [
     ('⚡','Instant Processing','PDFs are processed in your browser the moment you upload.'),
     ('🔒','100% Private','Your PDFs never leave your device — no server uploads.'),
     ('📝','Text-Based Output','Conversions produce real, searchable, selectable text.'),
     ('📄','All-in-One PDF Suite','Merge, split, edit, annotate, convert — 25+ PDF tools.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no page limits.'),
     ('🌐','Cross-Platform','Works on Windows, Mac, Linux, iOS, and Android.'),
   ],
   'faqs': [('Are my PDFs uploaded to a server?','No. All processing happens locally in your browser using pdf-lib and pdf.js.'),('Is there a page or file limit?','There is no hard limit. Very large PDFs (100MB+) may slow down your browser.')]
 },
 'Video Tools': {
   'features': [
     ('⚡','Browser-Based','Video processing happens locally — no uploads.'),
     ('🎬','Common Formats','Supports MP4, WebM, and other browser-playable formats.'),
     ('✂️','Trim & Convert','Cut, rotate, speed up, and convert video clips.'),
     ('🔒','100% Private','Your videos never leave your device.'),
     ('🆓','Free Forever','No sign-up, no watermarks, no duration limits.'),
     ('🎞️','Frame & GIF Export','Extract frames or create animated GIFs from video.'),
   ],
   'faqs': [('What video formats are supported?','MP4, WebM, and other formats your browser can play. Processing uses ffmpeg.wasm.'),('Is there a video length limit?','No hard limit, but longer videos take more time and memory to process.')]
 },
}

# Trust badges (shared across all tools)
TRUST_BADGES = [
 ('🔒','100% Private','Files never leave your browser'),
 ('⚡','Browser-Based','No installs, no uploads'),
 ('💯','Free Forever','No sign-up, no watermarks'),
 ('🚀','No Signup','Start instantly, no account'),
]

# CSS for new sections
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

def build_selling_points(tool_name, tagline, use_cases):
    # 3 bullets: tagline + 2 use-case-derived benefits
    pts = [tagline]
    if len(use_cases) >= 2:
        pts.append(use_cases[0].replace('Shrink ','Reduce ').replace('Shrink images','Reduce file size') if 'Shrink' in use_cases[0] else use_cases[0])
        pts.append('100% private — runs in your browser')
    elif len(use_cases) >= 1:
        pts.append(use_cases[0])
        pts.append('100% private — runs in your browser')
    else:
        pts.append('Free and browser-based')
        pts.append('100% private — runs in your browser')
    html = '<div class="selling-points">\n'
    icons = ['✅','🎯','🔒']
    for i, p in enumerate(pts[:3]):
        html += f'  <div class="sp-item"><span class="sp-icon">{icons[i]}</span>{p}</div>\n'
    html += '</div>'
    return html

def build_feature_narrative(name, icon, tagline, input_desc, output_desc, use_cases):
    intro = f'{name} lets you {tagline.lower()}. Upload {input_desc} and get {output_desc} — all processed locally in your browser, with no uploads and no sign-up.'
    # 3 narrative blocks from use cases
    block_icons = ['⚡','🎯','🔒']
    blocks = ''
    for i, uc in enumerate(use_cases[:3]):
        blocks += f'''      <div class="fn-block">
        <div class="fn-icon">{block_icons[i]}</div>
        <div><h3>{uc}</h3><p>{uc}. This is one of the most common reasons people reach for {name} — and it handles the job in seconds, entirely in your browser.</p></div>
      </div>
'''
    return f'''      <section class="feature-narrative">
        <h2>{name}: {tagline}</h2>
        <p class="fn-intro">{intro}</p>
{blocks}      </section>'''

def build_features_grid(cat, name):
    cd = CATEGORY.get(cat, CATEGORY['PDF Tools'])
    cards = ''
    for ic, title, desc in cd['features']:
        cards += f'''        <div class="feature-card">
          <div class="fc-icon">{ic}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
        </div>
'''
    return f'''      <section class="features-grid-section">
        <h2>Everything You Need in a {name}</h2>
        <p class="fg-sub">Powerful features that make {name} fast, private, and free.</p>
        <div class="features-grid">
{cards}        </div>
      </section>'''

def build_trust_badges():
    html = '<div class="trust-badges">\n'
    for ic, title, desc in TRUST_BADGES:
        html += f'  <div class="trust-badge"><div class="tb-icon">{ic}</div><div class="tb-title">{title}</div><div class="tb-desc">{desc}</div></div>\n'
    html += '</div>'
    return html

def build_extra_faqs(tool_faqs, cat):
    cd = CATEGORY.get(cat, CATEGORY['PDF Tools'])
    all_faqs = list(tool_faqs) + cd['faqs']
    html = ''
    for q, a in all_faqs:
        html += f'<div class="faq-item"><button class="faq-question">{q}</button><div class="faq-answer">{a}</div></div>\n'
    return html

def enrich_tool(slug):
    data = TOOLS.get(slug)
    if not data:
        return False, 'no data'
    name, icon, cat, input_desc, output_desc, tagline, use_cases, tool_faqs = data
    # Normalize FAQ tuples: a 4-element tuple is actually two Q/A pairs merged — split them.
    norm_faqs = []
    for fq in tool_faqs:
        if isinstance(fq, tuple) and len(fq) == 4:
            norm_faqs.append((fq[0], fq[1]))
            norm_faqs.append((fq[2], fq[3]))
        else:
            norm_faqs.append(fq)
    tool_faqs = norm_faqs
    fpath = os.path.join(TOOLS_DIR, f'{slug}.html')
    if not os.path.exists(fpath):
        return False, 'file not found'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already enriched (idempotent)
    if 'feature-narrative' in html and 'selling-points' in html:
        return False, 'already enriched'

    # 1. Inject CSS before </head> (after lang-hover-style)
    if 'enrich-css' not in html:
        css_block = f'\n<style id="enrich-css">{ENRICH_CSS}</style>\n'
        html = html.replace('</head>', css_block + '</head>', 1)

    # 2. Inject selling points after tool-page-header </div>
    sp = build_selling_points(name, tagline, use_cases)
    # Find tool-page-header closing div, insert after it
    header_close = re.search(r'(<div class="tool-page-header">[\s\S]*?</div>\s*</div>)', html)
    if header_close:
        html = html.replace(header_close.group(0), header_close.group(0) + '\n        ' + sp, 1)

    # 3. Inject feature narrative + features grid + trust badges before how-to-section
    narrative = build_feature_narrative(name, icon, tagline, input_desc, output_desc, use_cases)
    grid = build_features_grid(cat, name)
    badges = build_trust_badges()
    enrichment_block = '\n' + narrative + '\n\n' + grid + '\n\n' + badges + '\n'
    if '<section class="how-to-section">' in html:
        html = html.replace('<section class="how-to-section">', enrichment_block + '      <section class="how-to-section">', 1)
    else:
        # fallback: before related-tools or before </main>
        if '<section class="related-tools">' in html:
            html = html.replace('<section class="related-tools">', enrichment_block + '      <section class="related-tools">', 1)
        else:
            html = html.replace('</main>', enrichment_block + '  </main>', 1)

    # 4. Append extra FAQ items before </section> of faq-section
    extra_faqs = build_extra_faqs(tool_faqs, cat)
    # Find faq-section closing
    faq_match = re.search(r'(<section class="faq-section">[\s\S]*?)(</section>)', html)
    if faq_match:
        html = html.replace(faq_match.group(0), faq_match.group(1) + extra_faqs + '      ' + faq_match.group(2), 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    return True, 'enriched'

def main():
    print('=== Enriching tool pages with smallpdf-style content ===\n')
    enriched, skipped, failed = 0, 0, 0
    for slug in sorted(TOOLS.keys()):
        ok, msg = enrich_tool(slug)
        if ok:
            enriched += 1
            print(f'  ✅ {slug}: {msg}')
        else:
            if msg == 'already enriched':
                skipped += 1
                print(f'  ⏭️  {slug}: {msg}')
            else:
                failed += 1
                print(f'  ❌ {slug}: {msg}')
    # Check for tools without data
    tool_files = [f[:-5] for f in os.listdir(TOOLS_DIR) if f.endswith('.html')]
    missing_data = [t for t in tool_files if t not in TOOLS]
    if missing_data:
        print(f'\n⚠️  {len(missing_data)} tool(s) have no content data (skipped): {missing_data}')
    print(f'\nDone: {enriched} enriched, {skipped} skipped, {failed} failed, {len(missing_data)} without data')

if __name__ == '__main__':
    main()
