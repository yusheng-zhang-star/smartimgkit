#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Deep verification: extract text from batch 3 output PDFs to confirm content is real."""
import os
import pdfplumber

OUT_DIR = r'E:\网站项目\smartimgkit\_test_files\output_batch3'

checks = [
    ('html-to-pdf.pdf', ['SmartImgKit Test Article', 'Section One', 'Quick Brown Fox'.lower(), '100 percent browser-based'.lower()]),
    ('html-to-pdf-paste.pdf', ['Pasted Title', 'pasted HTML content']),
    ('txt-to-pdf.pdf', ['SmartImgKit TXT to PDF', 'plain text file', 'END OF TEST FILE']),
    ('csv-to-pdf.pdf', ['Product', 'Category', 'Widget A', 'Gadget X', 'Cable M']),
    ('epub-to-pdf.pdf', ['Chapter One', 'Chapter Two', 'lazy dog', 'blockquote'.lower(), 'first chapter']),
]

print('=== Batch 3 PDF content verification ===\n')
all_ok = True
for fname, expected in checks:
    fpath = os.path.join(OUT_DIR, fname)
    if not os.path.exists(fpath):
        print(f'❌ {fname}: FILE NOT FOUND')
        all_ok = False
        continue
    text = ''
    try:
        with pdfplumber.open(fpath) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ''
                text += t + '\n'
    except Exception as e:
        print(f'❌ {fname}: failed to extract ({e})')
        all_ok = False
        continue
    text_lower = text.lower()
    found = [e for e in expected if e.lower() in text_lower]
    missing = [e for e in expected if e.lower() not in text_lower]
    ok = len(missing) == 0
    status = '✅' if ok else '⚠️'
    print(f'{status} {fname}: {len(pdf.pages) if "pdf" in dir() else "?"} pages, text={len(text)} chars')
    print(f'   Found ({len(found)}/{len(expected)}): {found}')
    if missing:
        print(f'   Missing: {missing}')
        all_ok = False

print('\n' + ('✅ All content verifications passed!' if all_ok else '⚠️ Some content missing — review above.'))
