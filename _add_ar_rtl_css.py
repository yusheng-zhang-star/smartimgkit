#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inject RTL-specific CSS overrides into all Arabic HTML pages.
Handles text alignment, flexbox direction, and margin flipping."""
import os, re

BASE = r'e:\网站项目\smartimgkit\ar'

RTL_CSS = '''
/* RTL overrides for Arabic */
[dir="rtl"] body { text-align: right; }
[dir="rtl"] .breadcrumb { direction: rtl; text-align: right; }
[dir="rtl"] .tool-page-header { text-align: right; }
[dir="rtl"] .tool-page-header h1,
[dir="rtl"] .tool-page-header p { text-align: right; }
[dir="rtl"] .status { text-align: center; }
[dir="rtl"] .note { text-align: right; }
[dir="rtl"] .how-to-section h2,
[dir="rtl"] .feature-narrative h2,
[dir="rtl"] .features-grid-section h2,
[dir="rtl"] .faq-section h2,
[dir="rtl"] .related-tools h2 { text-align: right; }
[dir="rtl"] .how-to-step { text-align: right; }
[dir="rtl"] .how-to-step .step-number { margin-left: 0; margin-right: 0; }
[dir="rtl"] .faq-question { text-align: right; flex-direction: row-reverse; }
[dir="rtl"] .faq-answer { text-align: right; }
[dir="rtl"] .fn-block { flex-direction: row-reverse; }
[dir="rtl"] .fn-block .fn-icon { margin-right: 0; margin-left: 1.5rem; }
[dir="rtl"] .fn-intro { text-align: center; }
[dir="rtl"] .fg-sub { text-align: center; }
[dir="rtl"] .sp-item { direction: rtl; }
[dir="rtl"] .trust-badge { direction: rtl; }
[dir="rtl"] .feature-card { text-align: right; }
[dir="rtl"] .related-tool-card { flex-direction: row-reverse; text-align: right; }
[dir="rtl"] .related-tool-card .tool-arrow { transform: scaleX(-1); }
[dir="rtl"] .result-card { flex-direction: row-reverse; }
[dir="rtl"] .tool-tag { float: left; }
[dir="rtl"] .dropzone { text-align: center; }
[dir="rtl"] .site-header .container { direction: rtl; }
[dir="rtl"] .main-nav { direction: rtl; }
[dir="rtl"] .footer-grid { direction: rtl; }
[dir="rtl"] .footer-links { text-align: right; }
[dir="rtl"] .lang-switcher { direction: ltr; }
'''

fixed = 0
skipped = 0

for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith('.html'):
            continue
        fpath = os.path.join(root, f)
        with open(fpath, 'r', encoding='utf-8') as fh:
            html = fh.read()

        if 'rtl-css' in html:
            skipped += 1
            continue

        # Inject RTL CSS before </head>
        style_block = '<style id="rtl-css">%s\n</style>\n' % RTL_CSS
        html = html.replace('</head>', style_block + '</head>', 1)

        with open(fpath, 'w', encoding='utf-8') as fh:
            fh.write(html)
        fixed += 1

print('Fixed: %d, Already had rtl-css: %d' % (fixed, skipped))
