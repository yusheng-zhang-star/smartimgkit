#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deep-verify batch 1 output files contain real content."""
import os, zipfile

OUT = r'E:\网站项目\smartimgkit\_test_files\output'

def check_docx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        assert 'word/document.xml' in names, 'missing word/document.xml'
        xml = z.read('word/document.xml').decode('utf-8')
        # Extract text from <w:t> elements
        import re
        texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml)
        joined = ' '.join(texts)
        return len(joined) > 20, f'{len(texts)} text runs, {len(joined)} chars: "{joined[:80]}..."'

def check_xlsx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        sheets = [n for n in names if n.startswith('xl/worksheets/sheet')]
        assert sheets, 'no worksheets found'
        return True, f'{len(sheets)} sheet(s): {sheets}'

def check_pptx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        slides = [n for n in names if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        media = [n for n in names if n.startswith('ppt/media/')]
        return len(slides) > 0, f'{len(slides)} slide(s), {len(media)} media file(s)'

def check_pdf(path):
    with open(path, 'rb') as f:
        data = f.read()
    # Count pages
    pages = data.count(b'/Type /Page') + data.count(b'/Type/Page')
    # Check for text streams
    has_stream = b'stream' in data
    return pages > 0, f'{pages} page(s), has_stream={has_stream}, {len(data)} bytes'

checks = [
    ('pdf-to-word.docx', check_docx),
    ('pdf-to-excel.xlsx', check_xlsx),
    ('pdf-to-ppt.pptx', check_pptx),
    ('word-to-pdf.pdf', check_pdf),
    ('excel-to-pdf.pdf', check_pdf),
]

print('=== Deep Content Verification ===')
all_ok = True
for fname, checker in checks:
    p = os.path.join(OUT, fname)
    try:
        ok, detail = checker(p)
        icon = '✅' if ok else '❌'
        print(f'{icon} {fname:24} {detail}')
        if not ok: all_ok = False
    except Exception as e:
        print(f'❌ {fname:24} ERROR: {e}')
        all_ok = False

print(f'\n{"ALL CHECKS PASSED ✅" if all_ok else "SOME CHECKS FAILED ❌"}')
