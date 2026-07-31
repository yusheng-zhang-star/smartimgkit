#!/usr/bin/env python
"""Sync new tools and enhancements to all language versions."""

import os, shutil, re

BASE = r'E:\网站项目\smartimgkit'
LANGUAGES = ['es', 'pt', 'id', 'fr', 'vi', 'ar']

# Tool translations
TOOL_TRANSLATIONS = {
    'qr-code-generator': {
        'es': {'name': 'Generador de Códigos QR', 'desc': 'Genera códigos QR al instante. Gratis, online.'},
        'pt': {'name': 'Gerador de QR Code', 'desc': 'Gere códigos QR instantaneamente. Grátis, online.'},
        'id': {'name': 'Pembuat Kode QR', 'desc': 'Buat kode QR secara instan. Gratis, online.'},
        'fr': {'name': 'Générateur de QR Code', 'desc': 'Générez des codes QR instantanément. Gratuit, en ligne.'},
        'vi': {'name': 'Tạo QR Code', 'desc': 'Tạo mã QR tức thì. Miễn phí, trực tuyến.'},
        'ar': {'name': 'منشئ رمز الاستجابة السريعة', 'desc': 'أنشئ رموز QR فوراً. مجاني، عبر الإنترنت.'}
    },
    'signature-maker': {
        'es': {'name': 'Creador de Firmas', 'desc': 'Dibuja tu firma digital y descárgala como PNG transparente.'},
        'pt': {'name': 'Criador de Assinaturas', 'desc': 'Desenhe sua assinatura digital e baixe como PNG transparente.'},
        'id': {'name': 'Pembuat Tanda Tangan', 'desc': 'Gambar tanda tangan digital Anda dan unduh sebagai PNG transparan.'},
        'fr': {'name': 'Créateur de Signature', 'desc': 'Dessinez votre signature numérique et téléchargez-la en PNG transparent.'},
        'vi': {'name': 'Tạo Chữ Ký', 'desc': 'Vẽ chữ ký số của bạn và tải xuống dưới dạng PNG trong suốt.'},
        'ar': {'name': 'صانع التوقيع', 'desc': 'ارسم توقيعك الرقمي وقم بتنزيله كـ PNG شفاف.'}
    }
}

def replace_text(html, lang, slug):
    if slug in TOOL_TRANSLATIONS and lang in TOOL_TRANSLATIONS[slug]:
        t = TOOL_TRANSLATIONS[slug][lang]
        html = html.replace('<html lang="en"', f'<html lang="{lang}"' + (' dir="rtl"' if lang == 'ar' else ''))
        html = html.replace('<title>QR Code Generator — Generate QR Codes Free Online</title>', f'<title>{t["name"]} — SmartImgKit</title>')
        html = html.replace('<title>Signature Maker — Create Digital Signature Free Online</title>', f'<title>{t["name"]} — SmartImgKit</title>')
        html = html.replace('<h1>📱 QR Code Generator</h1>', f'<h1>📱 {t["name"]}</h1>')
        html = html.replace('<h1>✍️ Signature Maker</h1>', f'<h1>✍️ {t["name"]}</h1>')
        html = html.replace('Generate QR codes instantly. Free, online, no signup.', t['desc'])
        html = html.replace('Draw your digital signature and download as transparent PNG. Free, online.', t['desc'])
        html = html.replace('href="https://smartimgkit.com/tools/qr-code-generator"', f'href="https://smartimgkit.com/{lang}/tools/qr-code-generator"')
        html = html.replace('href="https://smartimgkit.com/tools/signature-maker"', f'href="https://smartimgkit.com/{lang}/tools/signature-maker"')
    return html

# 1. Copy new tools to all languages
for slug in ['qr-code-generator', 'signature-maker']:
    src = os.path.join(BASE, 'tools', f'{slug}.html')
    with open(src, 'r', encoding='utf-8') as f:
        src_content = f.read()
    for lang in LANGUAGES:
        dst_dir = os.path.join(BASE, lang, 'tools')
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f'{slug}.html')
        content = replace_text(src_content, lang, slug)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Created: {lang}/tools/{slug}.html")

# 2. Sync GIF Editor enhancements to all languages
src_gif = os.path.join(BASE, 'tools', 'gif-editor.html')
with open(src_gif, 'r', encoding='utf-8') as f:
    src_gif_content = f.read()
# Extract the UPNG scripts, APNG option, handleFiles, and generate changes
for lang in LANGUAGES:
    dst_gif = os.path.join(BASE, lang, 'tools', 'gif-editor.html')
    if not os.path.exists(dst_gif):
        print(f"  Skip: {lang}/tools/gif-editor.html not found")
        continue
    with open(dst_gif, 'r', encoding='utf-8') as f:
        dst_content = f.read()
    # Add UPNG scripts
    if 'upng-js' not in dst_content:
        dst_content = dst_content.replace(
            '<script src="/js/main.js?v=4"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/upng-js@2.1.0/UPNG.min.js"></script>\n  <script src="/js/main.js?v=4"></script>'
        )
    # Add APNG quality option
    if 'apng' not in dst_content:
        dst_content = dst_content.replace(
            '<option value="3">High (larger file)</option>\n                </select>',
            '<option value="3">High (larger file)</option>\n                    <option value="apng">APNG (lossless)</option>\n                </select>'
        )
    with open(dst_gif, 'w', encoding='utf-8') as f:
        f.write(dst_content)
    print(f"  Updated: {lang}/tools/gif-editor.html")

# 3. Sync Photo Restoration fix to all languages
src_pr = os.path.join(BASE, 'tools', 'photo-restoration.html')
with open(src_pr, 'r', encoding='utf-8') as f:
    src_pr_content = f.read()
# Extract the photo script
photo_script_match = re.search(r'(<script>\n\(function\(\)\{.*?\}\)\(\);\n  </script>)', src_pr_content, re.DOTALL)
if photo_script_match:
    photo_script = photo_script_match.group(1)
    for lang in LANGUAGES:
        dst_pr = os.path.join(BASE, lang, 'tools', 'photo-restoration.html')
        if not os.path.exists(dst_pr):
            print(f"  Skip: {lang}/tools/photo-restoration.html not found")
            continue
        with open(dst_pr, 'r', encoding='utf-8') as f:
            dst_content = f.read()
        dst_content = re.sub(
            r'<script>\s*\n\s*</script>',
            photo_script,
            dst_content
        )
        with open(dst_pr, 'w', encoding='utf-8') as f:
            f.write(dst_content)
        print(f"  Updated: {lang}/tools/photo-restoration.html")

print("\n✅ All tools synced to all language versions!")
