#!/usr/bin/env python3
"""Generate placeholder blog index pages for all 6 languages."""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

LANG_META = {
    'es': {
        'lang': 'es',
        'dir': '',
        'title': 'Blog de SmartImgKit - Guías y Tutoriales de Edición de Imágenes',
        'desc': 'Guías prácticas y tutoriales sobre edición de imágenes, compresión, eliminación de fondos y más. Todo gratis, sin registro.',
        'kw': 'blog edición imágenes, tutorial quitar fondo, guía comprimir imágenes, formatos imagen',
        'page_title': 'SmartImgKit Blog',
        'subtitle': 'Guías y tutoriales de edición de imágenes',
        'coming_soon': 'Próximamente: artículos en español sobre edición de imágenes, compresión, eliminación de fondos y más.',
        'home': 'Inicio',
        'blog': 'Blog',
    },
    'pt': {
        'lang': 'pt',
        'dir': '',
        'title': 'Blog SmartImgKit - Tutoriais de Edição de Imagens',
        'desc': 'Guias práticos e tutoriais sobre edição de imagens, compressão, remoção de fundo e mais. Tudo grátis, sem cadastro.',
        'kw': 'blog edição imagens, tutorial remover fundo, guia comprimir imagens, formatos imagem',
        'page_title': 'Blog SmartImgKit',
        'subtitle': 'Tutoriais e guias de edição de imagens',
        'coming_soon': 'Em breve: artigos em português sobre edição de imagens, compressão, remoção de fundo e mais.',
        'home': 'Início',
        'blog': 'Blog',
    },
    'id': {
        'lang': 'id',
        'dir': '',
        'title': 'Blog SmartImgKit - Panduan Edit Gambar',
        'desc': 'Panduan praktis dan tutorial tentang edit gambar, kompresi, hapus latar belakang, dan lainnya. Gratis, tanpa registrasi.',
        'kw': 'blog edit gambar, tutorial hapus background, panduan kompresi gambar, format gambar',
        'page_title': 'Blog SmartImgKit',
        'subtitle': 'Panduan dan tutorial edit gambar',
        'coming_soon': 'Segera hadir: artikel dalam bahasa Indonesia tentang edit gambar, kompresi, hapus latar belakang, dan lainnya.',
        'home': 'Beranda',
        'blog': 'Blog',
    },
    'fr': {
        'lang': 'fr',
        'dir': '',
        'title': 'Blog SmartImgKit - Guides et Tutoriels d\'Édition d\'Images',
        'desc': 'Guides pratiques et tutoriels sur l\'édition d\'images, la compression, la suppression d\'arrière-plan, et plus encore. Gratuit, sans inscription.',
        'kw': 'blog édition images, tutoriel supprimer fond, guide compression images, formats image',
        'page_title': 'Blog SmartImgKit',
        'subtitle': 'Guides et tutoriels d\'édition d\'images',
        'coming_soon': 'Bientôt disponible : des articles en français sur l\'édition d\'images, la compression, la suppression d\'arrière-plan et plus.',
        'home': 'Accueil',
        'blog': 'Blog',
    },
    'vi': {
        'lang': 'vi',
        'dir': '',
        'title': 'Blog SmartImgKit - Hướng Dẫn Chỉnh Sửa Ảnh',
        'desc': 'Hướng dẫn thực tế về chỉnh sửa ảnh, nén ảnh, xóa nền và nhiều hơn nữa. Miễn phí, không cần đăng ký.',
        'kw': 'blog chỉnh sửa ảnh, hướng dẫn xóa nền, cách nén ảnh, định dạng ảnh',
        'page_title': 'Blog SmartImgKit',
        'subtitle': 'Hướng dẫn chỉnh sửa ảnh',
        'coming_soon': 'Sắp ra mắt: bài viết bằng tiếng Việt về chỉnh sửa ảnh, nén ảnh, xóa nền và nhiều hơn nữa.',
        'home': 'Trang chủ',
        'blog': 'Blog',
    },
    'ar': {
        'lang': 'ar',
        'dir': ' dir="rtl"',
        'title': 'مدونة SmartImgKit - أدلة وشروحات تحرير الصور',
        'desc': 'أدلة عملية وشروحات حول تحرير الصور وضغطها وإزالة الخلفية والمزيد. مجاني، بدون تسجيل.',
        'kw': 'مدونة تحرير الصور, شرح إزالة الخلفية, دليل ضغط الصور, صيغ الصور',
        'page_title': 'مدونة SmartImgKit',
        'subtitle': 'أدلة وشروحات تحرير الصور',
        'coming_soon': 'قريباً: مقالات باللغة العربية حول تحرير الصور وضغطها وإزالة الخلفية والمزيد.',
        'home': 'الرئيسية',
        'blog': 'المدونة',
    },
}

NAV_TEXTS = {
    'es': ('Inicio', 'Herramientas', 'Workflows', 'Blog', 'Acerca de', 'Contacto'),
    'pt': ('Início', 'Ferramentas', 'Workflows', 'Blog', 'Sobre', 'Contato'),
    'id': ('Beranda', 'Alat', 'Workflows', 'Blog', 'Tentang', 'Kontak'),
    'fr': ('Accueil', 'Outils', 'Workflows', 'Blog', 'À propos', 'Contact'),
    'vi': ('Trang chủ', 'Công cụ', 'Workflows', 'Blog', 'Giới thiệu', 'Liên hệ'),
    'ar': ('الرئيسية', 'الأدوات', 'سير العمل', 'المدونة', 'حول', 'اتصل بنا'),
}

FOOTER_TEXTS = {
    'es': {
        'tagline': 'Herramientas de imagen gratuitas con IA que respetan tu privacidad.',
        'tools': 'Herramientas',
        'more_tools': 'Más herramientas',
        'legal': 'Legal',
    },
    'pt': {
        'tagline': 'Ferramentas de imagem gratuitas com IA que respeitam sua privacidade.',
        'tools': 'Ferramentas',
        'more_tools': 'Mais ferramentas',
        'legal': 'Legal',
    },
    'id': {
        'tagline': 'Alat gambar gratis dengan AI yang menghormati privasi Anda.',
        'tools': 'Alat',
        'more_tools': 'Alat lainnya',
        'legal': 'Hukum',
    },
    'fr': {
        'tagline': 'Outils d\'image gratuits avec IA qui respectent votre vie privée.',
        'tools': 'Outils',
        'more_tools': 'Plus d\'outils',
        'legal': 'Légal',
    },
    'vi': {
        'tagline': 'Công cụ chỉnh sửa ảnh miễn phí với AI, tôn trọng quyền riêng tư của bạn.',
        'tools': 'Công cụ',
        'more_tools': 'Công cụ khác',
        'legal': 'Pháp lý',
    },
    'ar': {
        'tagline': 'أدوات صور مجانية بالذكاء الاصطناعي تحترم خصوصيتك.',
        'tools': 'الأدوات',
        'more_tools': 'المزيد من الأدوات',
        'legal': 'قانوني',
    },
}

TOOLS_SHORT = [
    ('background-remover', 'Background Remover'),
    ('compressor', 'Compressor'),
    ('converter', 'Converter'),
    ('resizer', 'Resizer'),
    ('cropper', 'Cropper'),
    ('watermark', 'Watermark'),
]

PRIVACY_LINKS = {
    'es': ('Política de privacidad', 'Términos de servicio', 'Política de cookies', 'Contacto'),
    'pt': ('Política de Privacidade', 'Termos de Serviço', 'Política de Cookies', 'Contato'),
    'id': ('Kebijakan Privasi', 'Ketentuan Layanan', 'Kebijakan Cookie', 'Kontak'),
    'fr': ('Politique de confidentialité', 'Conditions d\'utilisation', 'Politique de cookies', 'Contact'),
    'vi': ('Chính sách bảo mật', 'Điều khoản dịch vụ', 'Chính sách cookie', 'Liên hệ'),
    'ar': ('سياسة الخصوصية', 'شروط الخدمة', 'سياسة ملفات تعريف الارتباط', 'اتصل بنا'),
}


def make_blog_index(lang_code):
    m = LANG_META[lang_code]
    nav = NAV_TEXTS[lang_code]
    ft = FOOTER_TEXTS[lang_code]
    pl = PRIVACY_LINKS[lang_code]
    rtl_attr = ' dir="rtl"' if lang_code == 'ar' else ''
    rtl_body = ' rtl' if lang_code == 'ar' else ''

    # build nav
    nav_html = (
        f'<nav class="main-nav">'
        f'<a href="/">{nav[0]}</a>'
        f'<a href="/{lang_code}/tools/background-remover.html">{nav[1]}</a>'
        f'<a href="/workflows/">{nav[2]}</a>'
        f'<a href="/{lang_code}/blog/" class="active">{nav[3]}</a>'
        f'<a href="/about.html">{nav[4]}</a>'
        f'<a href="/contact.html">{nav[5]}</a>'
        f'</nav>'
    )

    # build footer tools
    tools1 = ''.join(
        f'<a href="/{lang_code}/tools/{t[0]}.html">{t[1]}</a>'
        for t in TOOLS_SHORT[:4]
    )
    tools2 = ''.join(
        f'<a href="/{lang_code}/tools/{t[0]}.html">{t[1]}</a>'
        for t in TOOLS_SHORT[4:]
    )

    # hreflang tags
    hreflangs = [
        f'<link rel="alternate" hreflang="en" href="https://smartimgkit.com/blog/" />',
    ]
    for lc in ['es', 'pt', 'id', 'fr', 'vi', 'ar']:
        hreflangs.append(
            f'<link rel="alternate" hreflang="{lc}" href="https://smartimgkit.com/{lc}/blog/" />'
        )
    hreflang_html = '\n'.join(hreflangs)
    hreflang_html += '\n  <link rel="alternate" hreflang="x-default" href="https://smartimgkit.com/blog/" />'

    html = f'''<!DOCTYPE html>
<html lang="{m['lang']}"{rtl_attr} data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <title>{m['title']}</title>
  <meta name="description" content="{m['desc']}">
  <meta name="keywords" content="{m['kw']}">
  <link rel="canonical" href="https://smartimgkit.com/{lang_code}/blog/">
  <meta name="theme-color" content="#6366f1">
  <meta property="og:title" content="{m['title']}">
  <meta property="og:description" content="{m['desc']}">
  <meta property="og:url" content="https://smartimgkit.com/{lang_code}/blog/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SmartImgKit">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{m['title']}">
  <meta name="twitter:description" content="{m['desc']}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  {hreflang_html}
  <link rel="stylesheet" href="/css/style.css?v=3">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "SmartImgKit Blog - {m['lang']}",
    "url": "https://smartimgkit.com/{lang_code}/blog/",
    "description": "{m['desc']}",
    "publisher": {{
      "@type": "Organization",
      "name": "SmartImgKit",
      "url": "https://smartimgkit.com"
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "{m['home']}", "item": "https://smartimgkit.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{m['blog']}" }}
    ]
  }}
  </script>
</head>
<body{rtl_body}>
<header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">
        <span class="logo-icon">🎨</span>
        <span class="logo-text">SmartImgKit</span>
      </a>
      {nav_html}
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">🌙</button>
        <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Menu">☰</button>
      </div>
    </div>
  </header>

  <main>
    <section class="blog-hero">
      <div class="container">
        <h1>{m['page_title']}</h1>
        <p class="blog-hero-desc">{m['subtitle']}</p>
      </div>
    </section>

    <section class="blog-listing">
      <div class="container">
        <div class="blog-grid" style="display:block;text-align:center;padding:60px 20px;">
          <p style="font-size:1.1rem;color:var(--text-secondary);line-height:1.8;">
            {m['coming_soon']}
          </p>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="logo">
            <span class="logo-icon">🎨</span>
            <span class="logo-text">SmartImgKit</span>
          </a>
          <p>{ft['tagline']}</p>
        </div>
        <div class="footer-links">
          <h4>{ft['tools']}</h4>
          {tools1}
        </div>
        <div class="footer-links">
          <h4>{ft['more_tools']}</h4>
          {tools2}
        </div>
        <div class="footer-links">
          <h4>{ft['legal']}</h4>
          <a href="/privacy.html">{pl[0]}</a>
          <a href="/terms.html">{pl[1]}</a>
          <a href="/cookie-policy.html">{pl[2]}</a>
          <a href="/contact.html">{pl[3]}</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 SmartImgKit. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
'''
    return html


def main():
    for lang_code in ['es', 'pt', 'id', 'fr', 'vi', 'ar']:
        html = make_blog_index(lang_code)
        path = os.path.join(BASE, lang_code, 'blog', 'index.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'✓ Generated {lang_code}/blog/index.html ({len(html)} bytes)')


if __name__ == '__main__':
    main()
