#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate test files for batch 3 tools (html/txt/csv/epub -> pdf)."""
import os, zipfile

TEST_DIR = r'E:\网站项目\smartimgkit\_test_files'
os.makedirs(TEST_DIR, exist_ok=True)

# 1. HTML test file
html_path = os.path.join(TEST_DIR, 'test_sample.html')
html = '''<!DOCTYPE html>
<html><head><title>Test Article</title></head>
<body>
<h1>SmartImgKit Test Article</h1>
<p>This is a test HTML document for the HTML to PDF converter. It contains multiple paragraphs of text that should be rendered into a searchable PDF.</p>
<h2>Section One: Introduction</h2>
<p>The quick brown fox jumps over the lazy dog. This sentence is used to verify text rendering and word wrapping in the generated PDF output.</p>
<p>Another paragraph here. The converter should preserve document structure including headings, paragraphs, and lists.</p>
<h2>Section Two: Features</h2>
<ul>
<li>Text-based, searchable PDF output</li>
<li>Preserves heading hierarchy (H1 through H6)</li>
<li>Automatic word wrapping and pagination</li>
<li>100 percent browser-based processing</li>
</ul>
<h3>Subsection: Notes</h3>
<blockquote>This is a blockquote example. It should be rendered with indentation to distinguish it from regular paragraphs.</blockquote>
<p>Final paragraph. The conversion happens entirely in your browser using jsPDF. No content is uploaded to any server.</p>
</body></html>'''
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'OK HTML: {html_path} ({os.path.getsize(html_path)} bytes)')

# 2. TXT test file
txt_path = os.path.join(TEST_DIR, 'test_sample.txt')
lines = [
    'SmartImgKit TXT to PDF Test Document',
    '=====================================',
    '',
    'This is a plain text file used to verify the TXT to PDF converter.',
    'Long lines should wrap automatically to fit the page width without being cut off. The converter uses jsPDF to render real text that can be selected, copied, and searched in the resulting PDF document.',
    '',
    'Paragraph two follows an empty line above it. Empty lines act as paragraph breaks in the output PDF.',
    '',
    'Paragraph three. The tool supports configurable font size, page size (A4 or Letter), and font family (Helvetica, Courier, or Times).',
    '',
    'Line four with some      extra spaces      that should be preserved.',
    'Line five immediately after line four (no blank line between).',
    '',
    'END OF TEST FILE.',
]
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'OK TXT: {txt_path} ({os.path.getsize(txt_path)} bytes)')

# 3. CSV test file with quoted fields and commas inside
csv_path = os.path.join(TEST_DIR, 'test_sample.csv')
csv = '''Product,Category,Price,Stock,Notes
Widget A,Hardware,12.50,120,"In stock, ships today"
Widget B,Hardware,8.99,0,"Out of stock, backordered"
Gadget X,"Electronics, Gadgets",45.00,35,"Popular item"
Gadget Y,Electronics,89.99,12,Limited quantity
Book Z,Media,15.75,200,Bestseller
Cable M,Accessories,5.25,500,"Length: 2m, USB-C"
'''
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write(csv)
print(f'OK CSV: {csv_path} ({os.path.getsize(csv_path)} bytes)')

# 4. EPUB test file (minimal valid EPUB 2 structure)
epub_path = os.path.join(TEST_DIR, 'test_sample.epub')

container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

content_opf = '''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>SmartImgKit EPUB Test</dc:title>
    <dc:creator>Test Author</dc:creator>
    <dc:identifier id="BookID" opf:scheme="UUID">test-epub-001</dc:identifier>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="ch1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="ch2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="ch1"/>
    <itemref idref="ch2"/>
  </spine>
</package>'''

toc_ncx = '''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="test-epub-001"/></head>
  <docTitle><text>SmartImgKit EPUB Test</text></docTitle>
  <navMap>
    <navPoint id="n1" playOrder="1"><navLabel><text>Chapter 1</text></navLabel><content src="chapter1.xhtml"/></navPoint>
    <navPoint id="n2" playOrder="2"><navLabel><text>Chapter 2</text></navLabel><content src="chapter2.xhtml"/></navPoint>
  </navMap>
</ncx>'''

chapter1 = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Chapter 1</title></head><body>
<h1>Chapter One: The Beginning</h1>
<p>This is the first chapter of the test EPUB. The converter should extract this text and render it into a searchable PDF in reading order.</p>
<p>The quick brown fox jumps over the lazy dog. This sentence verifies that text rendering works correctly across page boundaries.</p>
<h2>A Subsection</h2>
<p>Subsection content goes here. The heading hierarchy should be preserved with appropriate font sizes.</p>
<ul>
<li>First list item in the ebook</li>
<li>Second list item with more detail</li>
<li>Third list item to verify list rendering</li>
</ul>
</body></html>'''

chapter2 = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Chapter 2</title></head><body>
<h1>Chapter Two: Conclusion</h1>
<p>This is the second chapter. It should start on a new page in the generated PDF, following chapter one.</p>
<p>The EPUB to PDF converter parses the EPUB archive using JSZip, reads the OPF spine to determine chapter order, then extracts text blocks from each XHTML document.</p>
<blockquote>This is a blockquote in the ebook. It should be rendered with indentation.</blockquote>
<p>End of the test ebook. The conversion is complete.</p>
</body></html>'''

# Write EPUB: mimetype must be first and stored (not compressed)
with zipfile.ZipFile(epub_path, 'w') as zf:
    zf.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    zf.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)
    zf.writestr('OEBPS/content.opf', content_opf, compress_type=zipfile.ZIP_DEFLATED)
    zf.writestr('OEBPS/toc.ncx', toc_ncx, compress_type=zipfile.ZIP_DEFLATED)
    zf.writestr('OEBPS/chapter1.xhtml', chapter1, compress_type=zipfile.ZIP_DEFLATED)
    zf.writestr('OEBPS/chapter2.xhtml', chapter2, compress_type=zipfile.ZIP_DEFLATED)
print(f'OK EPUB: {epub_path} ({os.path.getsize(epub_path)} bytes)')

print('\nAll batch 3 test files created in', TEST_DIR)
