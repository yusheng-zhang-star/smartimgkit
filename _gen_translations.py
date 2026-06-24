#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate translated _tools_data_{LANG}.json from English _tools_data.json.
Run: python _gen_translations.py fr vi ar
"""

import json, os, sys, copy

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, '_tools_data.json')

# ═══════════════════════════════════════════════════
# LANGUAGE-LEVEL TRANSLATIONS
# ═══════════════════════════════════════════════════

LANG_FIELDS = {
    'fr': {
        'lang': 'fr',
        'nav_html': '<nav class="main-nav"><a href="/">Accueil</a><a href="/fr/tools/background-remover.html">Outils</a><a href="/workflows/">Workflows</a><a href="/blog/">Blog</a><a href="/about.html">À propos</a><a href="/contact.html">Contact</a></nav>',
        'lang_switcher_html': '<div class="lang-switcher" style="position:relative;">\n          <button class="lang-btn" aria-label="Changer de langue">🇫🇷 FR</button>\n          <div class="lang-dropdown" style="display:none!important;position:absolute!important;top:100%;right:0;z-index:100;min-width:160px;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:4px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,0.15);">\n            <a href="/" hreflang="en" lang="en">🇬🇧 English</a>\n            <a href="/es/" hreflang="es" lang="es">🇪🇸 Español</a>\n            <a href="/pt/" hreflang="pt" lang="pt">🇧🇷 Português</a>\n            <a href="/id/" hreflang="id" lang="id">🇮🇩 Bahasa Indonesia</a>\n            <a href="/vi/" hreflang="vi" lang="vi">🇻🇳 Tiếng Việt</a>\n            <a href="/ar/" hreflang="ar" lang="ar">🇸🇦 العربية</a>\n          </div>\n        </div>',
        'footer_html': '<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><a href="/" class="logo"><span class="logo-icon">🎨</span><span class="logo-text">SmartImgKit</span></a><p>Outils d\'image gratuits avec IA qui respectent votre vie privée.</p></div><div class="footer-links"><h4>Outils</h4><a href="/fr/tools/background-remover.html">Supprimer l\'arrière-plan</a><a href="/fr/tools/compressor.html">Compresseur</a><a href="/fr/tools/converter.html">Convertisseur</a><a href="/fr/tools/resizer.html">Redimensionneur</a><a href="/fr/tools/cropper.html">Recadrage</a><a href="/fr/tools/watermark.html">Filigrane</a></div><div class="footer-links"><h4>Plus d\'outils</h4><a href="/fr/tools/image-upscaler.html">Agrandisseur</a><a href="/fr/tools/gif-editor.html">Éditeur GIF</a><a href="/fr/tools/pdf-to-image.html">PDF vers Image</a><a href="/fr/tools/heic-converter.html">Convertisseur HEIC</a><a href="/fr/tools/meme-generator.html">Générateur de Mèmes</a><a href="/fr/tools/face-blur.html">Flouter les Visages</a></div><div class="footer-links"><h4>Site</h4><a href="/about.html">À propos</a><a href="/contact.html">Contact</a><a href="/privacy.html">Confidentialité</a><a href="/terms.html">Conditions</a></div></div><div class="footer-bottom"><p>© 2026 SmartImgKit. Traitement 100% local — vos fichiers ne quittent jamais votre appareil.</p></div></div></footer>',
        'breadcrumb_home': 'Accueil',
        'breadcrumb_tools': 'Outils',
        'breadcrumb_tools_url': '/',
        'tools_url': '/fr/tools',
    },
    'vi': {
        'lang': 'vi',
        'nav_html': '<nav class="main-nav"><a href="/">Trang chủ</a><a href="/vi/tools/background-remover.html">Công cụ</a><a href="/workflows/">Workflows</a><a href="/blog/">Blog</a><a href="/about.html">Giới thiệu</a><a href="/contact.html">Liên hệ</a></nav>',
        'lang_switcher_html': '<div class="lang-switcher" style="position:relative;">\n          <button class="lang-btn" aria-label="Đổi ngôn ngữ">🇻🇳 VI</button>\n          <div class="lang-dropdown" style="display:none!important;position:absolute!important;top:100%;right:0;z-index:100;min-width:160px;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:4px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,0.15);">\n            <a href="/" hreflang="en" lang="en">🇬🇧 English</a>\n            <a href="/es/" hreflang="es" lang="es">🇪🇸 Español</a>\n            <a href="/pt/" hreflang="pt" lang="pt">🇧🇷 Português</a>\n            <a href="/id/" hreflang="id" lang="id">🇮🇩 Bahasa Indonesia</a>\n            <a href="/fr/" hreflang="fr" lang="fr">🇫🇷 Français</a>\n            <a href="/ar/" hreflang="ar" lang="ar">🇸🇦 العربية</a>\n          </div>\n        </div>',
        'footer_html': '<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><a href="/" class="logo"><span class="logo-icon">🎨</span><span class="logo-text">SmartImgKit</span></a><p>Công cụ hình ảnh AI miễn phí, tôn trọng quyền riêng tư.</p></div><div class="footer-links"><h4>Công cụ</h4><a href="/vi/tools/background-remover.html">Xóa nền</a><a href="/vi/tools/compressor.html">Nén ảnh</a><a href="/vi/tools/converter.html">Chuyển đổi</a><a href="/vi/tools/resizer.html">Đổi kích thước</a><a href="/vi/tools/cropper.html">Cắt ảnh</a><a href="/vi/tools/watermark.html">Watermark</a></div><div class="footer-links"><h4>Công cụ khác</h4><a href="/vi/tools/image-upscaler.html">Phóng to ảnh</a><a href="/vi/tools/gif-editor.html">Chỉnh sửa GIF</a><a href="/vi/tools/pdf-to-image.html">PDF sang Ảnh</a><a href="/vi/tools/heic-converter.html">Chuyển đổi HEIC</a><a href="/vi/tools/meme-generator.html">Tạo Meme</a><a href="/vi/tools/face-blur.html">Làm mờ khuôn mặt</a></div><div class="footer-links"><h4>Trang web</h4><a href="/about.html">Giới thiệu</a><a href="/contact.html">Liên hệ</a><a href="/privacy.html">Bảo mật</a><a href="/terms.html">Điều khoản</a></div></div><div class="footer-bottom"><p>© 2026 SmartImgKit. Xử lý 100% cục bộ — tệp của bạn không bao giờ rời khỏi thiết bị.</p></div></div></footer>',
        'breadcrumb_home': 'Trang chủ',
        'breadcrumb_tools': 'Công cụ',
        'breadcrumb_tools_url': '/',
        'tools_url': '/vi/tools',
    },
    'ar': {
        'lang': 'ar',
        'nav_html': '<nav class="main-nav"><a href="/">الرئيسية</a><a href="/ar/tools/background-remover.html">الأدوات</a><a href="/workflows/">سير العمل</a><a href="/blog/">المدونة</a><a href="/about.html">حول</a><a href="/contact.html">اتصل بنا</a></nav>',
        'lang_switcher_html': '<div class="lang-switcher" style="position:relative;">\n          <button class="lang-btn" aria-label="تغيير اللغة">🇸🇦 العربية</button>\n          <div class="lang-dropdown" style="display:none!important;position:absolute!important;top:100%;right:0;z-index:100;min-width:160px;background:var(--bg-secondary);border:1px solid var(--border-color);border-radius:12px;padding:4px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,0.15);">\n            <a href="/" hreflang="en" lang="en">🇬🇧 English</a>\n            <a href="/es/" hreflang="es" lang="es">🇪🇸 Español</a>\n            <a href="/pt/" hreflang="pt" lang="pt">🇧🇷 Português</a>\n            <a href="/id/" hreflang="id" lang="id">🇮🇩 Bahasa Indonesia</a>\n            <a href="/fr/" hreflang="fr" lang="fr">🇫🇷 Français</a>\n            <a href="/vi/" hreflang="vi" lang="vi">🇻🇳 Tiếng Việt</a>\n          </div>\n        </div>',
        'footer_html': '<footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><a href="/" class="logo"><span class="logo-icon">🎨</span><span class="logo-text">SmartImgKit</span></a><p>أدوات صور مجانية بالذكاء الاصطناعي تحترم خصوصيتك.</p></div><div class="footer-links"><h4>الأدوات</h4><a href="/ar/tools/background-remover.html">إزالة الخلفية</a><a href="/ar/tools/compressor.html">ضاغط الصور</a><a href="/ar/tools/converter.html">محول الصور</a><a href="/ar/tools/resizer.html">تغيير الحجم</a><a href="/ar/tools/cropper.html">قص الصور</a><a href="/ar/tools/watermark.html">علامة مائية</a></div><div class="footer-links"><h4>المزيد</h4><a href="/ar/tools/image-upscaler.html">تكبير الصور</a><a href="/ar/tools/gif-editor.html">محرر GIF</a><a href="/ar/tools/pdf-to-image.html">PDF إلى صورة</a><a href="/ar/tools/heic-converter.html">محول HEIC</a><a href="/ar/tools/meme-generator.html">منشئ الميمات</a><a href="/ar/tools/face-blur.html">تمويه الوجوه</a></div><div class="footer-links"><h4>الموقع</h4><a href="/about.html">حول</a><a href="/contact.html">اتصل بنا</a><a href="/privacy.html">الخصوصية</a><a href="/terms.html">الشروط</a></div></div><div class="footer-bottom"><p>© 2026 SmartImgKit. معالجة 100% محلية — ملفاتك لا تغادر جهازك أبداً.</p></div></div></footer>',
        'breadcrumb_home': 'الرئيسية',
        'breadcrumb_tools': 'الأدوات',
        'breadcrumb_tools_url': '/',
        'tools_url': '/ar/tools',
    },
}

# ═══════════════════════════════════════════════════
# TOOL-LEVEL TRANSLATIONS BY LANGUAGE
# Key: tool_slug -> {field: translation}
# ═══════════════════════════════════════════════════

TOOL_TRANSLATIONS = {}

# ── FRENCH ──
TOOL_TRANSLATIONS['fr'] = {
    'avif-support': {
        'title': 'Support AVIF — Décodez et Convertissez Gratuitement | SmartImgKit',
        'description': 'Vérifiez le support AVIF de votre navigateur, décodez et convertissez en JPG/PNG/WebP. Gratuit, dans le navigateur, sans téléchargement.',
        'keywords': 'support AVIF, convertisseur AVIF, décoder AVIF, AVIF vers JPG, AVIF vers PNG, compatibilité navigateur AVIF, format image nouvelle génération',
        'h1': '🖼️ Support AVIF — Décoder et Convertir',
        'subtitle': 'Vérifiez le support AVIF de votre navigateur, décodez les images AVIF et convertissez en JPG/PNG/WebP. 100% dans le navigateur.',
        'og_title': 'Support AVIF Gratuit — SmartImgKit',
        'og_description': 'Vérifiez le support AVIF et convertissez en JPG/PNG/WebP. 100% dans le navigateur.',
        'breadcrumb_last': '🖼️ Support AVIF',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Vérifier le Support</h4><p>Consultez l\'état du support AVIF de votre navigateur.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Télécharger AVIF</h4><p>Cliquez ou glissez-déposez votre fichier .avif.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Choisir le Format</h4><p>Sélectionnez JPG, PNG ou WebP comme sortie.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Téléchargez l\'image convertie.</p></div>\n  </div>\n</section>',
        'guide_html': '<h2>Guide Détaillé</h2>\n\n      <div class="guide-block">\n        <h3>Étape 1 : Vérifier le Support du Navigateur</h3>\n        <p>Le haut de la page affiche votre navigateur actuel et sa capacité à décoder l\'AVIF.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Étape 2 : Choisir le Format de Sortie</h3>\n        <p>Sélectionnez JPG (universel), PNG (sans perte) ou WebP (équilibré).</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Étape 3 : Régler la Qualité</h3>\n        <p>Utilisez le curseur (10-100%) pour contrôler la taille du fichier de sortie.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Étape 4 : Télécharger le Fichier AVIF</h3>\n        <p>Cliquez ou glissez-déposez un fichier .avif. Maximum 30 Mo.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Étape 5 : Convertir et Télécharger</h3>\n        <p>Cliquez sur "Convertir" puis "Télécharger" pour enregistrer.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Résumé de Compatibilité</h3>\n        <ul><li>Chrome 85+ — Support complet</li><li>Firefox 93+ — Support complet</li><li>Safari 16.4+ — Support complet</li></ul>\n      </div>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Quels navigateurs prennent en charge AVIF ?</button><div class="faq-answer">Chrome 85+, Firefox 93+, Safari 16.4+. Edge aussi car basé sur Chromium.</div></div>\n  <div class="faq-item"><button class="faq-question">Pourquoi convertir AVIF en JPG ?</button><div class="faq-answer">AVIF a un support limité sur les réseaux sociaux et les anciens navigateurs.</div></div>\n  <div class="faq-item"><button class="faq-question">La conversion réduit-elle la qualité ?</button><div class="faq-answer">La conversion AVIF vers JPG à 90-100% de qualité préserve bien la qualité visuelle.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/compressor.html" class="related-tool-card">\n      <span class="tool-icon">🗜️</span>\n      <div class="tool-info">\n        <strong>Compresseur d\'Image</strong>\n        <span class="tool-desc">Compressez les images AVIF après décodage</span>\n      </div>\n      <span class="tool-arrow">→</span>\n    </a>\n    <a href="/fr/tools/converter.html" class="related-tool-card">\n      <span class="tool-icon">🔄</span>\n      <div class="tool-info">\n        <strong>Convertisseur d\'Image</strong>\n        <span class="tool-desc">Convertissez AVIF en JPG/PNG/WebP</span>\n      </div>\n      <span class="tool-arrow">→</span>\n    </a>\n    <a href="/fr/tools/image-upscaler.html" class="related-tool-card">\n      <span class="tool-icon">🔍</span>\n      <div class="tool-info">\n        <strong>Agrandisseur d\'Image</strong>\n        <span class="tool-desc">Agrandissez les images AVIF après décodage</span>\n      </div>\n      <span class="tool-arrow">→</span>\n    </a>\n  </div>\n</section>',
        'jsonld_webapp': {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'Support AVIF', 'url': 'https://smartimgkit.com/fr/tools/avif-support', 'applicationCategory': 'MultimediaApplication', 'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'description': 'Vérifiez le support AVIF et convertissez en JPG/PNG/WebP.'},
        'jsonld_howto': {'@context': 'https://schema.org', '@type': 'HowTo', 'name': 'Comment Convertir des Images AVIF', 'step': [{'@type': 'HowToStep', 'position': 1, 'name': 'Vérifier le Support', 'text': 'Consultez le support AVIF de votre navigateur.'}, {'@type': 'HowToStep', 'position': 2, 'name': 'Télécharger AVIF', 'text': 'Glissez-déposez votre fichier .avif.'}, {'@type': 'HowToStep', 'position': 3, 'name': 'Choisir le Format', 'text': 'Sélectionnez JPG, PNG ou WebP.'}, {'@type': 'HowToStep', 'position': 4, 'name': 'Télécharger', 'text': 'Téléchargez l\'image convertie.'}]},
        'jsonld_faq': {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Quels navigateurs prennent en charge AVIF ?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Chrome 85+, Firefox 93+, Safari 16.4+.'}}, {'@type': 'Question', 'name': 'Pourquoi convertir AVIF en JPG ?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'AVIF a un support limité sur les réseaux sociaux et les anciens navigateurs.'}}, {'@type': 'Question', 'name': 'La conversion réduit-elle la qualité ?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'La conversion AVIF vers JPG à 90-100% préserve bien la qualité visuelle.'}}]},
    },
    'background-remover': {
        'title': 'Supprimer l\'Arrière-plan d\'une Image Gratuitement | SmartImgKit',
        'description': 'Supprimez l\'arrière-plan des images gratuitement avec l\'IA. 100% dans le navigateur, pas de téléchargement. Traitement instantané, prend en charge JPG/PNG/WebP.',
        'keywords': 'supprimer arrière-plan, suppression arrière-plan, outil suppression fond, fond transparent, suppression arrière-plan IA, enlever arrière-plan gratuit',
        'h1': '🎯 Supprimer l\'Arrière-plan d\'une Image',
        'subtitle': 'Supprimez l\'arrière-plan des images instantanément avec l\'IA. 100% gratuit, dans le navigateur.',
        'og_title': 'Supprimer l\'Arrière-plan Gratuit — SmartImgKit',
        'og_description': 'Supprimez l\'arrière-plan des images avec l\'IA. Gratuit, dans le navigateur.',
        'breadcrumb_last': '🎯 Supprimer l\'Arrière-plan',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger l\'Image</h4><p>Cliquez ou glissez-déposez votre image.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>IA Traitement Automatique</h4><p>L\'IA supprime l\'arrière-plan en quelques secondes.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Télécharger</h4><p>Enregistrez votre image au format PNG avec fond transparent.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Comment fonctionne la suppression d\'arrière-plan ?</button><div class="faq-answer">Notre IA détecte automatiquement le sujet et supprime l\'arrière-plan.</div></div>\n  <div class="faq-item"><button class="faq-question">Quels formats sont pris en charge ?</button><div class="faq-answer">JPG, PNG et WebP comme entrée. PNG transparent comme sortie.</div></div>\n  <div class="faq-item"><button class="faq-question">Mes images sont-elles privées ?</button><div class="faq-answer">Oui, tout le traitement se fait dans votre navigateur, rien n\'est téléchargé.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Compresseur d\'Image</strong><span class="tool-desc">Compressez après suppression du fond</span></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Convertisseur d\'Image</strong><span class="tool-desc">Convertissez en JPG ou WebP</span></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Recadrage d\'Image</strong><span class="tool-desc">Recadrez après suppression du fond</span></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'compressor': {
        'title': 'Compresseur d\'Image Gratuit en Ligne | SmartImgKit',
        'description': 'Compressez JPG, PNG, WebP gratuitement. Réduisez la taille jusqu\'à 90% sans perte visible. Traitement dans le navigateur, pas de téléchargement.',
        'keywords': 'compresseur image, compresser image, réduire taille image, compression JPG, compression PNG, compression WebP, compresser image en ligne gratuit',
        'h1': '🗜️ Compresseur d\'Image',
        'subtitle': 'Compressez JPG, PNG, WebP gratuitement. Réduisez la taille jusqu\'à 90% sans perte visible.',
        'og_title': 'Compresseur d\'Image Gratuit — SmartImgKit',
        'og_description': 'Compressez JPG, PNG, WebP. Réduisez jusqu\'à 90% sans perte. 100% navigateur.',
        'breadcrumb_last': '🗜️ Compresseur d\'Image',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez vos images JPG, PNG ou WebP.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Régler la Qualité</h4><p>Ajustez le curseur pour équilibrer taille et qualité.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Compresser</h4><p>Cliquez sur Compresser et voyez la réduction.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Enregistrez l\'image compressée.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">La compression réduit-elle la qualité ?</button><div class="faq-answer">À 80-90%, la perte est imperceptible mais la taille est fortement réduite.</div></div>\n  <div class="faq-item"><button class="faq-question">Quelle taille maximale puis-je télécharger ?</button><div class="faq-answer">Jusqu\'à 30 Mo par fichier.</div></div>\n  <div class="faq-item"><button class="faq-question">Mes fichiers sont-ils en sécurité ?</button><div class="faq-answer">Oui, tout le traitement se fait localement dans votre navigateur.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Convertisseur d\'Image</strong><span class="tool-desc">Convertissez entre formats</span></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Redimensionneur</strong><span class="tool-desc">Redimensionnez aux dimensions exactes</span></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/bulk-processor.html" class="related-tool-card"><span class="tool-icon">📦</span><div class="tool-info"><strong>Traitement par Lot</strong><span class="tool-desc">Compressez plusieurs images à la fois</span></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'converter': {
        'title': 'Convertisseur d\'Image Gratuit en Ligne | SmartImgKit',
        'description': 'Convertissez entre JPG, PNG, WebP, BMP, GIF gratuitement. 100% dans le navigateur, pas de téléchargement.',
        'keywords': 'convertisseur image, convertir image, JPG vers PNG, PNG vers WebP, conversion format image, convertisseur format image gratuit',
        'h1': '🔄 Convertisseur d\'Image',
        'subtitle': 'Convertissez entre JPG, PNG, WebP, BMP, GIF. 100% dans le navigateur, gratuit.',
        'og_title': 'Convertisseur d\'Image Gratuit — SmartImgKit',
        'og_description': 'Convertissez entre JPG, PNG, WebP, BMP, GIF. 100% navigateur.',
        'breadcrumb_last': '🔄 Convertisseur d\'Image',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez votre image.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Choisir le Format</h4><p>Sélectionnez le format de sortie (JPG, PNG, WebP, BMP, GIF).</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Convertir</h4><p>Cliquez pour convertir instantanément.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Enregistrez l\'image convertie.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Quels formats sont pris en charge ?</button><div class="faq-answer">Entrée : JPG, PNG, WebP, BMP, GIF. Sortie : JPG, PNG, WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">La conversion est-elle sans perte ?</button><div class="faq-answer">La conversion vers des formats avec perte (JPG) peut réduire la qualité. PNG vers PNG est sans perte.</div></div>\n  <div class="faq-item"><button class="faq-question">Y a-t-il une limite de taille ?</button><div class="faq-answer">Maximum 30 Mo par fichier.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Compresseur d\'Image</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Redimensionneur</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/heic-converter.html" class="related-tool-card"><span class="tool-icon">📱</span><div class="tool-info"><strong>Convertisseur HEIC</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'resizer': {
        'title': 'Redimensionneur d\'Image Gratuit en Ligne | SmartImgKit',
        'description': 'Redimensionnez les images aux dimensions exactes. Prend en charge JPG, PNG, WebP. 100% dans le navigateur, gratuit.',
        'keywords': 'redimensionner image, changer taille image, redimensionnement image, resize image, outil redimensionnement gratuit',
        'h1': '📐 Redimensionneur d\'Image',
        'subtitle': 'Redimensionnez vos images aux dimensions exactes. Conservez les proportions ou définissez des tailles personnalisées.',
        'og_title': 'Redimensionneur d\'Image Gratuit — SmartImgKit',
        'og_description': 'Redimensionnez les images aux dimensions exactes. 100% navigateur.',
        'breadcrumb_last': '📐 Redimensionneur d\'Image',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez votre image.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Définir les Dimensions</h4><p>Entrez la largeur et la hauteur souhaitées.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Ajuster</h4><p>Activez "Conserver les proportions" si nécessaire.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Enregistrez l\'image redimensionnée.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Puis-je conserver les proportions ?</button><div class="faq-answer">Oui, activez l\'option "Conserver les proportions".</div></div>\n  <div class="faq-item"><button class="faq-question">Quels formats sont pris en charge ?</button><div class="faq-answer">JPG, PNG et WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">Y a-t-il des tailles prédéfinies ?</button><div class="faq-answer">Oui, pour les réseaux sociaux et dimensions courantes.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Compresseur d\'Image</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Recadrage d\'Image</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Convertisseur</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'cropper': {
        'title': 'Recadrage d\'Image Gratuit en Ligne | SmartImgKit',
        'description': 'Recadrez les images avec précision. Prend en charge JPG, PNG, WebP. 100% dans le navigateur, gratuit.',
        'keywords': 'recadrer image, outil recadrage, crop image, recadrage photo gratuit, rogner image',
        'h1': '✂️ Recadrage d\'Image',
        'subtitle': 'Recadrez vos images avec des ratios prédéfinis ou librement. 100% dans le navigateur.',
        'og_title': 'Recadrage d\'Image Gratuit — SmartImgKit',
        'og_description': 'Recadrez les images avec précision. 100% navigateur.',
        'breadcrumb_last': '✂️ Recadrage d\'Image',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez votre image.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Ajuster</h4><p>Faites glisser les poignées pour sélectionner la zone.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Ratio</h4><p>Choisissez un ratio prédéfini ou libre.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Appliquer</h4><p>Cliquez pour recadrer et télécharger.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Quels ratios sont disponibles ?</button><div class="faq-answer">1:1, 4:3, 16:9, 3:2 et recadrage libre.</div></div>\n  <div class="faq-item"><button class="faq-question">Le recadrage est-il réversible ?</button><div class="faq-answer">Vous pouvez réinitialiser avant de confirmer.</div></div>\n  <div class="faq-item"><button class="faq-question">Quels formats sont pris en charge ?</button><div class="faq-answer">JPG, PNG et WebP.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Redimensionneur</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>Supprimer l\'Arrière-plan</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Compresseur</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'watermark': {
        'title': 'Ajouter un Filigrane aux Images Gratuitement | SmartImgKit',
        'description': 'Ajoutez des filigranes texte ou image. Contrôle de l\'opacité et de la position. 100% dans le navigateur.',
        'keywords': 'ajouter filigrane, watermark image, filigrane photo, outil filigrane gratuit, protéger image',
        'h1': '💧 Ajouter un Filigrane',
        'subtitle': 'Ajoutez des filigranes texte ou image. Contrôlez l\'opacité et la position.',
        'og_title': 'Filigrane d\'Image Gratuit — SmartImgKit',
        'og_description': 'Ajoutez des filigranes texte ou image. 100% navigateur.',
        'breadcrumb_last': '💧 Filigrane',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez votre image.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Type de Filigrane</h4><p>Choisissez texte ou image.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Personnaliser</h4><p>Définissez l\'opacité, la position et la taille.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Enregistrez l\'image avec filigrane.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Puis-je utiliser une image comme filigrane ?</button><div class="faq-answer">Oui, téléchargez votre logo ou toute image comme filigrane.</div></div>\n  <div class="faq-item"><button class="faq-question">Puis-je ajuster la transparence ?</button><div class="faq-answer">Oui, utilisez le curseur d\'opacité.</div></div>\n  <div class="faq-item"><button class="faq-question">Le filigrane est-il permanent ?</button><div class="faq-answer">Il est intégré à l\'image téléchargée mais peut être recouvert.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/face-blur.html" class="related-tool-card"><span class="tool-icon">😷</span><div class="tool-info"><strong>Flouter les Visages</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Compresseur</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Convertisseur</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'face-blur': {
        'title': 'Flouter les Visages Gratuitement en Ligne | SmartImgKit',
        'description': 'Floutez les visages automatiquement avec l\'IA. Protection de la vie privée. 100% dans le navigateur.',
        'keywords': 'flouter visage, cacher visage, anonymiser photo, protection vie privée, flou visage IA',
        'h1': '😷 Flouter les Visages',
        'subtitle': 'Floutez automatiquement les visages avec l\'IA. Protégez la vie privée instantanément.',
        'og_title': 'Flouter les Visages Gratuit — SmartImgKit',
        'og_description': 'Floutez les visages automatiquement avec l\'IA. 100% navigateur.',
        'breadcrumb_last': '😷 Flouter les Visages',
        'howto_html': '<section class="how-to-section">\n  <h2>Comment Utiliser</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Télécharger</h4><p>Glissez-déposez votre photo.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Détection IA</h4><p>L\'IA détecte automatiquement les visages.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Ajuster</h4><p>Réglez l\'intensité du flou.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Télécharger</h4><p>Enregistrez la photo anonymisée.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Questions Fréquentes</h2>\n  <div class="faq-item"><button class="faq-question">Comment fonctionne la détection de visage ?</button><div class="faq-answer">L\'IA détecte les visages en utilisant votre navigateur, aucune donnée n\'est envoyée.</div></div>\n  <div class="faq-item"><button class="faq-question">Puis-je flouter manuellement ?</button><div class="faq-answer">Oui, vous pouvez aussi appliquer un flou manuel sur n\'importe quelle zone.</div></div>\n  <div class="faq-item"><button class="faq-question">Le flou peut-il être annulé ?</button><div class="faq-answer">Non, une fois appliqué et sauvegardé, le flou est permanent.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Vous Pourriez Aussi Aimer</h2>\n  <div class="related-tools-grid">\n    <a href="/fr/tools/watermark.html" class="related-tool-card"><span class="tool-icon">💧</span><div class="tool-info"><strong>Filigrane</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>Supprimer l\'Arrière-plan</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/fr/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Recadrage</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
}

# ── VIETNAMESE ──
TOOL_TRANSLATIONS['vi'] = {
    'avif-support': {
        'title': 'Hỗ Trợ AVIF — Giải Mã & Chuyển Đổi Miễn Phí | SmartImgKit',
        'description': 'Kiểm tra hỗ trợ AVIF của trình duyệt, giải mã và chuyển đổi sang JPG/PNG/WebP. Miễn phí, xử lý trong trình duyệt.',
        'keywords': 'hỗ trợ AVIF, chuyển đổi AVIF, giải mã AVIF, AVIF sang JPG, AVIF sang PNG, trình duyệt hỗ trợ AVIF, định dạng ảnh thế hệ mới',
        'h1': '🖼️ Hỗ Trợ AVIF — Giải Mã & Chuyển Đổi',
        'subtitle': 'Kiểm tra hỗ trợ AVIF, giải mã và chuyển đổi sang JPG/PNG/WebP. 100% trong trình duyệt.',
        'og_title': 'Hỗ Trợ AVIF Miễn Phí — SmartImgKit',
        'og_description': 'Kiểm tra hỗ trợ AVIF và chuyển đổi sang JPG/PNG/WebP. 100% trình duyệt.',
        'breadcrumb_last': '🖼️ Hỗ Trợ AVIF',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Kiểm Tra Hỗ Trợ</h4><p>Xem trạng thái hỗ trợ AVIF của trình duyệt.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Tải Lên AVIF</h4><p>Nhấp hoặc kéo thả file .avif.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Chọn Định Dạng</h4><p>Chọn JPG, PNG hoặc WebP làm đầu ra.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Tải ảnh đã chuyển đổi.</p></div>\n  </div>\n</section>',
        'guide_html': '<h2>Hướng Dẫn Chi Tiết</h2>\n\n      <div class="guide-block">\n        <h3>Bước 1: Kiểm Tra Trình Duyệt</h3>\n        <p>Đầu trang hiển thị trình duyệt của bạn và khả năng giải mã AVIF.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Bước 2: Chọn Định Dạng Đầu Ra</h3>\n        <p>Chọn JPG (phổ biến), PNG (không mất dữ liệu) hoặc WebP (cân bằng).</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Bước 3: Đặt Chất Lượng</h3>\n        <p>Sử dụng thanh trượt (10-100%) để kiểm soát kích thước file.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Bước 4: Tải Lên File AVIF</h3>\n        <p>Nhấp hoặc kéo thả file .avif. Tối đa 30MB.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Bước 5: Chuyển Đổi và Tải Xuống</h3>\n        <p>Nhấp "Chuyển đổi" rồi "Tải xuống".</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>Tóm Tắt Hỗ Trợ Trình Duyệt</h3>\n        <ul><li>Chrome 85+ — Hỗ trợ đầy đủ</li><li>Firefox 93+ — Hỗ trợ đầy đủ</li><li>Safari 16.4+ — Hỗ trợ đầy đủ</li></ul>\n      </div>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Trình duyệt nào hỗ trợ AVIF?</button><div class="faq-answer">Chrome 85+, Firefox 93+, Safari 16.4+. Edge cũng hỗ trợ vì dùng Chromium.</div></div>\n  <div class="faq-item"><button class="faq-question">Tại sao nên chuyển AVIF sang JPG?</button><div class="faq-answer">AVIF có hỗ trợ hạn chế trên mạng xã hội và trình duyệt cũ.</div></div>\n  <div class="faq-item"><button class="faq-question">Chuyển đổi có làm giảm chất lượng không?</button><div class="faq-answer">Chuyển AVIF sang JPG ở chất lượng 90-100% giữ được chất lượng tốt.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong><span class="tool-desc">Nén ảnh AVIF sau khi giải mã</span></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Chuyển Đổi Ảnh</strong><span class="tool-desc">Chuyển AVIF sang JPG/PNG/WebP</span></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/image-upscaler.html" class="related-tool-card"><span class="tool-icon">🔍</span><div class="tool-info"><strong>Phóng To Ảnh</strong><span class="tool-desc">Phóng to ảnh AVIF sau khi giải mã</span></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'background-remover': {
        'title': 'Xóa Nền Ảnh Miễn Phí Trực Tuyến | SmartImgKit',
        'description': 'Xóa nền ảnh miễn phí bằng AI. 100% trong trình duyệt, không tải lên. Xử lý tức thì, hỗ trợ JPG/PNG/WebP.',
        'keywords': 'xóa nền, xóa phông, tách nền, nền trong suốt, xóa nền AI, xóa nền miễn phí',
        'h1': '🎯 Xóa Nền Ảnh',
        'subtitle': 'Xóa nền ảnh ngay lập tức với AI. 100% miễn phí, trong trình duyệt.',
        'og_title': 'Xóa Nền Miễn Phí — SmartImgKit',
        'og_description': 'Xóa nền ảnh bằng AI. Miễn phí, trong trình duyệt.',
        'breadcrumb_last': '🎯 Xóa Nền',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Ảnh Lên</h4><p>Nhấp hoặc kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Xử Lý Tự Động</h4><p>AI xóa nền trong vài giây.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Tải Xuống</h4><p>Lưu ảnh PNG nền trong suốt.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Xóa nền hoạt động như thế nào?</button><div class="faq-answer">AI của chúng tôi tự động phát hiện chủ thể và xóa nền.</div></div>\n  <div class="faq-item"><button class="faq-question">Hỗ trợ định dạng nào?</button><div class="faq-answer">Đầu vào: JPG, PNG, WebP. Đầu ra: PNG trong suốt.</div></div>\n  <div class="faq-item"><button class="faq-question">Ảnh của tôi có riêng tư không?</button><div class="faq-answer">Có, mọi xử lý diễn ra trong trình duyệt, không gửi đi đâu.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Chuyển Đổi Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Cắt Ảnh</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'compressor': {
        'title': 'Nén Ảnh Trực Tuyến Miễn Phí | SmartImgKit',
        'description': 'Nén JPG, PNG, WebP miễn phí. Giảm dung lượng đến 90% không mất chất lượng. Xử lý trong trình duyệt.',
        'keywords': 'nén ảnh, nén hình ảnh, giảm dung lượng ảnh, nén JPG, nén PNG, nén WebP, nén ảnh trực tuyến miễn phí',
        'h1': '🗜️ Nén Ảnh',
        'subtitle': 'Nén JPG, PNG, WebP miễn phí. Giảm đến 90% dung lượng không mất chất lượng.',
        'og_title': 'Nén Ảnh Miễn Phí — SmartImgKit',
        'og_description': 'Nén JPG, PNG, WebP. Giảm đến 90%. 100% trình duyệt.',
        'breadcrumb_last': '🗜️ Nén Ảnh',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh JPG, PNG hoặc WebP.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Điều Chỉnh</h4><p>Dùng thanh trượt để cân bằng chất lượng.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Nén</h4><p>Nhấp Nén và xem mức giảm.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Lưu ảnh đã nén.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Nén có làm giảm chất lượng không?</button><div class="faq-answer">Ở mức 80-90%, tổn thất không đáng kể nhưng kích thước giảm mạnh.</div></div>\n  <div class="faq-item"><button class="faq-question">Tải lên tối đa bao nhiêu?</button><div class="faq-answer">Tối đa 30MB mỗi file.</div></div>\n  <div class="faq-item"><button class="faq-question">File có an toàn không?</button><div class="faq-answer">Có, mọi xử lý diễn ra cục bộ trong trình duyệt.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Chuyển Đổi</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Đổi Kích Thước</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/bulk-processor.html" class="related-tool-card"><span class="tool-icon">📦</span><div class="tool-info"><strong>Xử Lý Hàng Loạt</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'converter': {
        'title': 'Chuyển Đổi Ảnh Trực Tuyến Miễn Phí | SmartImgKit',
        'description': 'Chuyển đổi giữa JPG, PNG, WebP, BMP, GIF miễn phí. 100% trong trình duyệt.',
        'keywords': 'chuyển đổi ảnh, chuyển JPG sang PNG, chuyển PNG sang WebP, đổi định dạng ảnh, chuyển đổi ảnh miễn phí',
        'h1': '🔄 Chuyển Đổi Ảnh',
        'subtitle': 'Chuyển đổi giữa JPG, PNG, WebP, BMP, GIF. 100% trong trình duyệt, miễn phí.',
        'og_title': 'Chuyển Đổi Ảnh Miễn Phí — SmartImgKit',
        'og_description': 'Chuyển đổi giữa JPG, PNG, WebP, BMP, GIF. 100% trình duyệt.',
        'breadcrumb_last': '🔄 Chuyển Đổi Ảnh',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Chọn Định Dạng</h4><p>Chọn định dạng đầu ra (JPG, PNG, WebP, BMP, GIF).</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Chuyển Đổi</h4><p>Nhấp để chuyển đổi ngay.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Lưu ảnh đã chuyển đổi.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Hỗ trợ định dạng nào?</button><div class="faq-answer">Đầu vào: JPG, PNG, WebP, BMP, GIF. Đầu ra: JPG, PNG, WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">Chuyển đổi có mất dữ liệu không?</button><div class="faq-answer">Chuyển sang định dạng nén (JPG) có thể giảm chất lượng. PNG sang PNG không mất.</div></div>\n  <div class="faq-item"><button class="faq-question">Có giới hạn kích thước không?</button><div class="faq-answer">Tối đa 30MB mỗi file.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Đổi Kích Thước</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/heic-converter.html" class="related-tool-card"><span class="tool-icon">📱</span><div class="tool-info"><strong>Chuyển HEIC</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'resizer': {
        'title': 'Đổi Kích Thước Ảnh Trực Tuyến Miễn Phí | SmartImgKit',
        'description': 'Đổi kích thước ảnh theo kích thước chính xác. Hỗ trợ JPG, PNG, WebP. 100% trong trình duyệt.',
        'keywords': 'đổi kích thước ảnh, thay đổi kích thước, resize ảnh, công cụ đổi kích thước miễn phí',
        'h1': '📐 Đổi Kích Thước Ảnh',
        'subtitle': 'Đổi kích thước ảnh theo kích thước chính xác. Giữ tỷ lệ hoặc tùy chỉnh.',
        'og_title': 'Đổi Kích Thước Ảnh Miễn Phí — SmartImgKit',
        'og_description': 'Đổi kích thước ảnh chính xác. 100% trình duyệt.',
        'breadcrumb_last': '📐 Đổi Kích Thước',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Đặt Kích Thước</h4><p>Nhập chiều rộng và chiều cao mong muốn.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Điều Chỉnh</h4><p>Bật "Giữ tỷ lệ" nếu cần.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Lưu ảnh đã đổi kích thước.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Có thể giữ tỷ lệ không?</button><div class="faq-answer">Có, bật tùy chọn "Giữ tỷ lệ".</div></div>\n  <div class="faq-item"><button class="faq-question">Hỗ trợ định dạng nào?</button><div class="faq-answer">JPG, PNG và WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">Có kích thước đặt trước không?</button><div class="faq-answer">Có, cho mạng xã hội và kích thước phổ biến.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Cắt Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Chuyển Đổi</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'cropper': {
        'title': 'Cắt Ảnh Trực Tuyến Miễn Phí | SmartImgKit',
        'description': 'Cắt ảnh chính xác với nhiều tỷ lệ. Hỗ trợ JPG, PNG, WebP. 100% trong trình duyệt.',
        'keywords': 'cắt ảnh, crop ảnh, cắt ảnh miễn phí, cắt ảnh theo tỷ lệ',
        'h1': '✂️ Cắt Ảnh',
        'subtitle': 'Cắt ảnh với tỷ lệ có sẵn hoặc tự do. 100% trong trình duyệt.',
        'og_title': 'Cắt Ảnh Miễn Phí — SmartImgKit',
        'og_description': 'Cắt ảnh chính xác. 100% trình duyệt.',
        'breadcrumb_last': '✂️ Cắt Ảnh',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Điều Chỉnh</h4><p>Kéo các điểm để chọn vùng.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Tỷ Lệ</h4><p>Chọn tỷ lệ có sẵn hoặc tự do.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Áp Dụng</h4><p>Nhấp để cắt và tải xuống.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Có những tỷ lệ nào?</button><div class="faq-answer">1:1, 4:3, 16:9, 3:2 và cắt tự do.</div></div>\n  <div class="faq-item"><button class="faq-question">Có thể hoàn tác không?</button><div class="faq-answer">Có thể đặt lại trước khi xác nhận.</div></div>\n  <div class="faq-item"><button class="faq-question">Hỗ trợ định dạng nào?</button><div class="faq-answer">JPG, PNG và WebP.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>Đổi Kích Thước</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>Xóa Nền</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'watermark': {
        'title': 'Thêm Watermark Ảnh Miễn Phí | SmartImgKit',
        'description': 'Thêm watermark văn bản hoặc hình ảnh. Tùy chỉnh độ mờ và vị trí. 100% trong trình duyệt.',
        'keywords': 'thêm watermark, đóng dấu ảnh, watermark ảnh, bảo vệ ảnh, công cụ watermark miễn phí',
        'h1': '💧 Thêm Watermark',
        'subtitle': 'Thêm watermark văn bản hoặc hình ảnh. Kiểm soát độ mờ và vị trí.',
        'og_title': 'Watermark Ảnh Miễn Phí — SmartImgKit',
        'og_description': 'Thêm watermark văn bản hoặc hình ảnh. 100% trình duyệt.',
        'breadcrumb_last': '💧 Watermark',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Loại Watermark</h4><p>Chọn văn bản hoặc hình ảnh.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Tùy Chỉnh</h4><p>Đặt độ mờ, vị trí và kích thước.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Lưu ảnh có watermark.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Có thể dùng ảnh làm watermark không?</button><div class="faq-answer">Có, tải lên logo hoặc bất kỳ ảnh nào.</div></div>\n  <div class="faq-item"><button class="faq-question">Có thể điều chỉnh độ trong suốt không?</button><div class="faq-answer">Có, dùng thanh trượt độ mờ.</div></div>\n  <div class="faq-item"><button class="faq-question">Watermark có vĩnh viễn không?</button><div class="faq-answer">Được nhúng vào ảnh tải xuống nhưng có thể bị che.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/face-blur.html" class="related-tool-card"><span class="tool-icon">😷</span><div class="tool-info"><strong>Làm Mờ Mặt</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>Nén Ảnh</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>Chuyển Đổi</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'face-blur': {
        'title': 'Làm Mờ Khuôn Mặt Trực Tuyến Miễn Phí | SmartImgKit',
        'description': 'Làm mờ khuôn mặt tự động bằng AI. Bảo vệ quyền riêng tư. 100% trong trình duyệt.',
        'keywords': 'làm mờ mặt, che mặt, ẩn danh ảnh, bảo vệ quyền riêng tư, làm mờ mặt AI',
        'h1': '😷 Làm Mờ Khuôn Mặt',
        'subtitle': 'Tự động làm mờ khuôn mặt với AI. Bảo vệ quyền riêng tư ngay lập tức.',
        'og_title': 'Làm Mờ Mặt Miễn Phí — SmartImgKit',
        'og_description': 'Làm mờ khuôn mặt tự động với AI. 100% trình duyệt.',
        'breadcrumb_last': '😷 Làm Mờ Mặt',
        'howto_html': '<section class="how-to-section">\n  <h2>Cách Sử Dụng</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>Tải Lên</h4><p>Kéo thả ảnh của bạn.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>Phát Hiện AI</h4><p>AI tự động phát hiện khuôn mặt.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>Điều Chỉnh</h4><p>Chỉnh cường độ làm mờ.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>Tải Xuống</h4><p>Lưu ảnh đã ẩn danh.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>Câu Hỏi Thường Gặp</h2>\n  <div class="faq-item"><button class="faq-question">Phát hiện khuôn mặt hoạt động thế nào?</button><div class="faq-answer">AI phát hiện trong trình duyệt, không gửi dữ liệu đi đâu.</div></div>\n  <div class="faq-item"><button class="faq-question">Có thể làm mờ thủ công không?</button><div class="faq-answer">Có, bạn có thể làm mờ bất kỳ vùng nào.</div></div>\n  <div class="faq-item"><button class="faq-question">Có thể hoàn tác không?</button><div class="faq-answer">Không, sau khi lưu, làm mờ là vĩnh viễn.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>Có Thể Bạn Cũng Thích</h2>\n  <div class="related-tools-grid">\n    <a href="/vi/tools/watermark.html" class="related-tool-card"><span class="tool-icon">💧</span><div class="tool-info"><strong>Watermark</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>Xóa Nền</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/vi/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>Cắt Ảnh</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
}

# ── ARABIC ──
TOOL_TRANSLATIONS['ar'] = {
    'avif-support': {
        'title': 'دعم AVIF — فك وتحويل مجاني | SmartImgKit',
        'description': 'تحقق من دعم AVIF في متصفحك، فك وتحويل إلى JPG/PNG/WebP. مجاني، في المتصفح، بدون رفع.',
        'keywords': 'دعم AVIF, محول AVIF, فك AVIF, AVIF إلى JPG, AVIF إلى PNG, توافق المتصفح مع AVIF, تنسيق صور الجيل الجديد',
        'h1': '🖼️ دعم AVIF — فك وتحويل',
        'subtitle': 'تحقق من دعم AVIF في متصفحك، فك صور AVIF وتحويلها إلى JPG/PNG/WebP. 100% في المتصفح.',
        'og_title': 'دعم AVIF مجاني — SmartImgKit',
        'og_description': 'تحقق من دعم AVIF وحول إلى JPG/PNG/WebP. 100% في المتصفح.',
        'breadcrumb_last': '🖼️ دعم AVIF',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>تحقق من الدعم</h4><p>شاهد حالة دعم AVIF في متصفحك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>ارفع ملف AVIF</h4><p>انقر أو اسحب وأفلت ملف .avif.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>اختر التنسيق</h4><p>اختر JPG أو PNG أو WebP كمخرج.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>تحميل</h4><p>حمل الصورة المحولة.</p></div>\n  </div>\n</section>',
        'guide_html': '<h2>دليل مفصل</h2>\n\n      <div class="guide-block">\n        <h3>الخطوة 1: تحقق من دعم المتصفح</h3>\n        <p>أعلى الصفحة يعرض متصفحك الحالي وقدرته على فك AVIF.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>الخطوة 2: اختر تنسيق المخرج</h3>\n        <p>اختر JPG (عالمي، ملفات أصغر)، PNG (بدون فقدان)، أو WebP (متوازن).</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>الخطوة 3: اضبط الجودة</h3>\n        <p>استخدم شريط التمرير (10-100%) للتحكم في حجم الملف.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>الخطوة 4: ارفع ملف AVIF</h3>\n        <p>انقر أو اسحب وأفلت ملف .avif. الحد الأقصى 30 ميجابايت.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>الخطوة 5: حول وحمل</h3>\n        <p>انقر "تحويل" ثم "تحميل" للحفظ.</p>\n      </div>\n\n      <div class="guide-block">\n        <h3>ملخص دعم المتصفحات</h3>\n        <ul><li>Chrome 85+ — دعم كامل</li><li>Firefox 93+ — دعم كامل</li><li>Safari 16.4+ — دعم كامل</li></ul>\n      </div>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">ما المتصفحات التي تدعم AVIF؟</button><div class="faq-answer">Chrome 85+، Firefox 93+، Safari 16.4+. Edge أيضاً لأنه مبني على Chromium.</div></div>\n  <div class="faq-item"><button class="faq-question">لماذا أحول AVIF إلى JPG؟</button><div class="faq-answer">AVIF لديه دعم محدود على منصات التواصل الاجتماعي والمتصفحات القديمة.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يقلل التحويل من الجودة؟</button><div class="faq-answer">تحويل AVIF إلى JPG بجودة 90-100% يحافظ على الجودة البصرية جيداً.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong><span class="tool-desc">ضغط صور AVIF بعد الفك</span></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>محول الصور</strong><span class="tool-desc">تحويل AVIF إلى JPG/PNG/WebP</span></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/image-upscaler.html" class="related-tool-card"><span class="tool-icon">🔍</span><div class="tool-info"><strong>تكبير الصور</strong><span class="tool-desc">تكبير صور AVIF بعد الفك</span></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'background-remover': {
        'title': 'إزالة خلفية الصورة مجاناً | SmartImgKit',
        'description': 'أزل خلفية الصور مجاناً بالذكاء الاصطناعي. 100% في المتصفح، بدون رفع. معالجة فورية، يدعم JPG/PNG/WebP.',
        'keywords': 'إزالة الخلفية, إزالة خلفية الصورة, أداة إزالة الخلفية, خلفية شفافة, إزالة الخلفية بالذكاء الاصطناعي, إزالة خلفية مجانية',
        'h1': '🎯 إزالة خلفية الصورة',
        'subtitle': 'أزل خلفية الصور فوراً بالذكاء الاصطناعي. 100% مجاني، في المتصفح.',
        'og_title': 'إزالة الخلفية مجاناً — SmartImgKit',
        'og_description': 'أزل خلفية الصور بالذكاء الاصطناعي. مجاني، في المتصفح.',
        'breadcrumb_last': '🎯 إزالة الخلفية',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع الصورة</h4><p>انقر أو اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>معالجة تلقائية</h4><p>الذكاء الاصطناعي يزيل الخلفية في ثوانٍ.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>تحميل</h4><p>احفظ صورتك بصيغة PNG بخلفية شفافة.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">كيف تعمل إزالة الخلفية؟</button><div class="faq-answer">الذكاء الاصطناعي يكتشف الموضوع تلقائياً ويزيل الخلفية.</div></div>\n  <div class="faq-item"><button class="faq-question">ما التنسيقات المدعومة؟</button><div class="faq-answer">الإدخال: JPG، PNG، WebP. الإخراج: PNG شفاف.</div></div>\n  <div class="faq-item"><button class="faq-question">هل صوري خاصة؟</button><div class="faq-answer">نعم، كل المعالجة تتم في متصفحك، لا يتم رفع أي شيء.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>محول الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>قص الصور</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'compressor': {
        'title': 'ضاغط صور مجاني على الإنترنت | SmartImgKit',
        'description': 'ضغط JPG، PNG، WebP مجاناً. قلل الحجم حتى 90% بدون فقدان ملحوظ. معالجة في المتصفح.',
        'keywords': 'ضاغط صور, ضغط الصور, تقليل حجم الصورة, ضغط JPG, ضغط PNG, ضغط WebP, ضغط صور مجاني',
        'h1': '🗜️ ضاغط الصور',
        'subtitle': 'ضغط JPG، PNG، WebP مجاناً. قلل الحجم حتى 90% بدون فقدان ملحوظ.',
        'og_title': 'ضاغط صور مجاني — SmartImgKit',
        'og_description': 'ضغط JPG، PNG، WebP. قلل حتى 90%. 100% متصفح.',
        'breadcrumb_last': '🗜️ ضاغط الصور',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صور JPG أو PNG أو WebP.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>اضبط</h4><p>استخدم شريط التمرير لموازنة الجودة.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>اضغط</h4><p>انقر ضغط وشاهد التخفيض.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>حمل</h4><p>احفظ الصورة المضغوطة.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">هل يقلل الضغط من الجودة؟</button><div class="faq-answer">عند 80-90%، الفقد غير ملحوظ لكن الحجم ينخفض كثيراً.</div></div>\n  <div class="faq-item"><button class="faq-question">ما الحد الأقصى للرفع؟</button><div class="faq-answer">حتى 30 ميجابايت لكل ملف.</div></div>\n  <div class="faq-item"><button class="faq-question">هل ملفاتي آمنة؟</button><div class="faq-answer">نعم، كل المعالجة محلية في متصفحك.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>محول الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>تغيير الحجم</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/bulk-processor.html" class="related-tool-card"><span class="tool-icon">📦</span><div class="tool-info"><strong>معالجة مجمعة</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'converter': {
        'title': 'محول صور مجاني على الإنترنت | SmartImgKit',
        'description': 'حول بين JPG، PNG، WebP، BMP، GIF مجاناً. 100% في المتصفح.',
        'keywords': 'محول صور, تحويل الصور, JPG إلى PNG, PNG إلى WebP, تحويل تنسيق الصورة, محول صور مجاني',
        'h1': '🔄 محول الصور',
        'subtitle': 'حول بين JPG، PNG، WebP، BMP، GIF. 100% في المتصفح، مجاني.',
        'og_title': 'محول صور مجاني — SmartImgKit',
        'og_description': 'حول بين JPG، PNG، WebP، BMP، GIF. 100% متصفح.',
        'breadcrumb_last': '🔄 محول الصور',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>اختر التنسيق</h4><p>اختر تنسيق المخرج (JPG، PNG، WebP، BMP، GIF).</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>حول</h4><p>انقر للتحويل الفوري.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>حمل</h4><p>احفظ الصورة المحولة.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">ما التنسيقات المدعومة؟</button><div class="faq-answer">الإدخال: JPG، PNG، WebP، BMP، GIF. الإخراج: JPG، PNG، WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">هل التحويل بدون فقدان؟</button><div class="faq-answer">التحويل إلى تنسيقات مضغوطة (JPG) قد يقلل الجودة. PNG إلى PNG بدون فقدان.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يوجد حد للحجم؟</button><div class="faq-answer">الحد الأقصى 30 ميجابايت لكل ملف.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>تغيير الحجم</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/heic-converter.html" class="related-tool-card"><span class="tool-icon">📱</span><div class="tool-info"><strong>محول HEIC</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'resizer': {
        'title': 'تغيير حجم الصور مجاناً على الإنترنت | SmartImgKit',
        'description': 'غير حجم الصور بأبعاد دقيقة. يدعم JPG، PNG، WebP. 100% في المتصفح.',
        'keywords': 'تغيير حجم الصورة, تصغير الصورة, تكبير الصورة, أداة تغيير الحجم مجانية',
        'h1': '📐 تغيير حجم الصورة',
        'subtitle': 'غير حجم صورك بأبعاد دقيقة. حافظ على النسب أو حدد أحجاماً مخصصة.',
        'og_title': 'تغيير حجم الصورة مجاناً — SmartImgKit',
        'og_description': 'غير حجم الصور بأبعاد دقيقة. 100% متصفح.',
        'breadcrumb_last': '📐 تغيير الحجم',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>حدد الأبعاد</h4><p>أدخل العرض والارتفاع المطلوبين.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>اضبط</h4><p>فعل "الحفاظ على النسب" إذا لزم الأمر.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>حمل</h4><p>احفظ الصورة بالحجم الجديد.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">هل يمكنني الحفاظ على النسب؟</button><div class="faq-answer">نعم، فعل خيار "الحفاظ على النسب".</div></div>\n  <div class="faq-item"><button class="faq-question">ما التنسيقات المدعومة؟</button><div class="faq-answer">JPG، PNG و WebP.</div></div>\n  <div class="faq-item"><button class="faq-question">هل توجد أحجام محددة مسبقاً؟</button><div class="faq-answer">نعم، لوسائل التواصل الاجتماعي والأحجام الشائعة.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>قص الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>محول الصور</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'cropper': {
        'title': 'قص الصور مجاناً على الإنترنت | SmartImgKit',
        'description': 'قص الصور بدقة مع نسب متعددة. يدعم JPG، PNG، WebP. 100% في المتصفح.',
        'keywords': 'قص الصور, crop صورة, قص صورة مجاني, قص حسب النسبة',
        'h1': '✂️ قص الصور',
        'subtitle': 'قص صورك بنسب محددة مسبقاً أو بحرية. 100% في المتصفح.',
        'og_title': 'قص الصور مجاناً — SmartImgKit',
        'og_description': 'قص الصور بدقة. 100% متصفح.',
        'breadcrumb_last': '✂️ قص الصور',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>اضبط</h4><p>اسحب المقابض لتحديد المنطقة.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>النسبة</h4><p>اختر نسبة محددة مسبقاً أو حر.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>طبق</h4><p>انقر للقص والتحميل.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">ما النسب المتاحة؟</button><div class="faq-answer">1:1، 4:3، 16:9، 3:2 وقص حر.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يمكن التراجع؟</button><div class="faq-answer">يمكنك إعادة التعيين قبل التأكيد.</div></div>\n  <div class="faq-item"><button class="faq-question">ما التنسيقات المدعومة؟</button><div class="faq-answer">JPG، PNG و WebP.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/resizer.html" class="related-tool-card"><span class="tool-icon">📐</span><div class="tool-info"><strong>تغيير الحجم</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>إزالة الخلفية</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'watermark': {
        'title': 'إضافة علامة مائية للصور مجاناً | SmartImgKit',
        'description': 'أضف علامة مائية نصية أو صورة. تحكم في الشفافية والموقع. 100% في المتصفح.',
        'keywords': 'إضافة علامة مائية, علامة مائية للصور, حماية الصور, أداة علامة مائية مجانية',
        'h1': '💧 إضافة علامة مائية',
        'subtitle': 'أضف علامة مائية نصية أو صورة. تحكم في الشفافية والموقع.',
        'og_title': 'علامة مائية مجانية — SmartImgKit',
        'og_description': 'أضف علامة مائية نصية أو صورة. 100% متصفح.',
        'breadcrumb_last': '💧 علامة مائية',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>نوع العلامة</h4><p>اختر نصاً أو صورة.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>خصص</h4><p>حدد الشفافية والموقع والحجم.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>حمل</h4><p>احفظ الصورة بالعلامة المائية.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">هل يمكنني استخدام صورة كعلامة مائية؟</button><div class="faq-answer">نعم، ارفع شعارك أو أي صورة.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يمكنني ضبط الشفافية؟</button><div class="faq-answer">نعم، استخدم شريط تمرير الشفافية.</div></div>\n  <div class="faq-item"><button class="faq-question">هل العلامة المائية دائمة؟</button><div class="faq-answer">تدمج في الصورة المحملة لكن يمكن تغطيتها.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/face-blur.html" class="related-tool-card"><span class="tool-icon">😷</span><div class="tool-info"><strong>تمويه الوجوه</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/compressor.html" class="related-tool-card"><span class="tool-icon">🗜️</span><div class="tool-info"><strong>ضاغط الصور</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/converter.html" class="related-tool-card"><span class="tool-icon">🔄</span><div class="tool-info"><strong>محول الصور</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
    'face-blur': {
        'title': 'تمويه الوجوه مجاناً على الإنترنت | SmartImgKit',
        'description': 'موه الوجوه تلقائياً بالذكاء الاصطناعي. حماية الخصوصية. 100% في المتصفح.',
        'keywords': 'تمويه الوجه, إخفاء الوجه, إخفاء هوية الصورة, حماية الخصوصية, تمويه الوجه بالذكاء الاصطناعي',
        'h1': '😷 تمويه الوجوه',
        'subtitle': 'موه الوجوه تلقائياً بالذكاء الاصطناعي. احمِ الخصوصية فوراً.',
        'og_title': 'تمويه الوجوه مجاناً — SmartImgKit',
        'og_description': 'موه الوجوه تلقائياً بالذكاء الاصطناعي. 100% متصفح.',
        'breadcrumb_last': '😷 تمويه الوجوه',
        'howto_html': '<section class="how-to-section">\n  <h2>كيفية الاستخدام</h2>\n  <div class="how-to-steps">\n    <div class="how-to-step"><div class="step-number">1</div><h4>ارفع</h4><p>اسحب وأفلت صورتك.</p></div>\n    <div class="how-to-step"><div class="step-number">2</div><h4>اكتشاف AI</h4><p>الذكاء الاصطناعي يكتشف الوجوه تلقائياً.</p></div>\n    <div class="how-to-step"><div class="step-number">3</div><h4>اضبط</h4><p>عدل شدة التمويه.</p></div>\n    <div class="how-to-step"><div class="step-number">4</div><h4>حمل</h4><p>احفظ الصورة بدون هوية.</p></div>\n  </div>\n</section>',
        'faq_html': '<section class="faq-section">\n  <h2>أسئلة شائعة</h2>\n  <div class="faq-item"><button class="faq-question">كيف يعمل اكتشاف الوجه؟</button><div class="faq-answer">الذكاء الاصطناعي يكتشف الوجوه في متصفحك، لا ترسل بيانات.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يمكنني التمويه يدوياً؟</button><div class="faq-answer">نعم، يمكنك تمويه أي منطقة يدوياً.</div></div>\n  <div class="faq-item"><button class="faq-question">هل يمكن التراجع؟</button><div class="faq-answer">لا، بعد الحفظ، التمويه دائم.</div></div>\n</section>',
        'related_html': '<section class="related-tools">\n  <h2>قد يعجبك أيضاً</h2>\n  <div class="related-tools-grid">\n    <a href="/ar/tools/watermark.html" class="related-tool-card"><span class="tool-icon">💧</span><div class="tool-info"><strong>علامة مائية</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/background-remover.html" class="related-tool-card"><span class="tool-icon">🎯</span><div class="tool-info"><strong>إزالة الخلفية</strong></div><span class="tool-arrow">→</span></a>\n    <a href="/ar/tools/cropper.html" class="related-tool-card"><span class="tool-icon">✂️</span><div class="tool-info"><strong>قص الصور</strong></div><span class="tool-arrow">→</span></a>\n  </div>\n</section>',
    },
}

# ═══════════════════════════════════════════════════
# WORKSPACE_HTML TRANSLATIONS (UI labels in tools)
# ═══════════════════════════════════════════════════

# Keys: (tool_slug, english_label) -> translated label
UI_LABELS = {
    'fr': {
        # Generic labels
        'Click or drag': 'Cliquez ou glissez',
        'file here': 'le fichier ici',
        'Upload': 'Télécharger',
        'Download': 'Télécharger',
        'Convert': 'Convertir',
        'Reset': 'Réinitialiser',
        'Quality': 'Qualité',
        'Output Format': 'Format de sortie',
        'Choose format': 'Choisir le format',
        'Select': 'Sélectionner',
        'Apply': 'Appliquer',
        'Cancel': 'Annuler',
        'Processing': 'Traitement en cours',
        'Max': 'Maximum',
        'Your Browser': 'Votre Navigateur',
        'Browser Support': 'Support du Navigateur',
        'Converting': 'Conversion en cours',
        'Downloading': 'Téléchargement en cours',
        'Original': 'Original',
        'Compressed': 'Compressé',
        'Saved': 'Économisé',
        'Width': 'Largeur',
        'Height': 'Hauteur',
        'Maintain aspect ratio': 'Conserver les proportions',
        'Copy': 'Copier',
        'Paste': 'Coller',
        'Image': 'Image',
        'Text': 'Texte',
        'Opacity': 'Opacité',
        'Position': 'Position',
        'Size': 'Taille',
        'Font': 'Police',
        'Color': 'Couleur',
        'Background': 'Arrière-plan',
        'Foreground': 'Premier plan',
        'Preview': 'Aperçu',
        'Save': 'Enregistrer',
        'Load': 'Charger',
        'Clear': 'Effacer',
        'Add': 'Ajouter',
        'Remove': 'Supprimer',
        'Settings': 'Paramètres',
        'Options': 'Options',
        'Result': 'Résultat',
        'Results': 'Résultats',
        'Drop': 'Déposer',
        'or': 'ou',
        'drag and drop': 'glisser-déposer',
        'No file chosen': 'Aucun fichier choisi',
        'Choose File': 'Choisir un fichier',
        'files': 'fichiers',
        'file': 'fichier',
        'per file': 'par fichier',
        'Size': 'Taille',
        'Format': 'Format',
        'Dimensions': 'Dimensions',
        'Compression': 'Compression',
        'Level': 'Niveau',
        'Filter': 'Filtre',
        'Effect': 'Effet',
        'Strength': 'Force',
        'Detected': 'Détecté',
        'faces': 'visages',
        'blur': 'flou',
        'Export': 'Exporter',
        'Import': 'Importer',
        'Copy to clipboard': 'Copier dans le presse-papier',
        'Copied': 'Copié',
        'Close': 'Fermer',
        'Back': 'Retour',
        'Next': 'Suivant',
        'Finish': 'Terminer',
        'Start': 'Démarrer',
        'Continue': 'Continuer',
        'Submit': 'Envoyer',
        'Share': 'Partager',
        'Help': 'Aide',
        'More': 'Plus',
        'No': 'Non',
        'Yes': 'Oui',
        'On': 'Activé',
        'Off': 'Désactivé',
        'Auto': 'Auto',
        'Manual': 'Manuel',
        'Custom': 'Personnalisé',
        'Default': 'Par défaut',
        'Advanced': 'Avancé',
        'Basic': 'Basique',
        'Free': 'Gratuit',
        'Pro': 'Pro',
        'Image Size': 'Taille d\'image',
        'File Size': 'Taille du fichier',
        'Processed': 'Traité',
        'Error': 'Erreur',
        'Success': 'Succès',
        'Warning': 'Attention',
        'Please select': 'Veuillez sélectionner',
        'Drag & drop': 'Glissez-déposez',
        'click to browse': 'cliquez pour parcourir',
    },
    'vi': {
        'Click or drag': 'Nhấp hoặc kéo',
        'file here': 'file vào đây',
        'Upload': 'Tải lên',
        'Download': 'Tải xuống',
        'Convert': 'Chuyển đổi',
        'Reset': 'Đặt lại',
        'Quality': 'Chất lượng',
        'Output Format': 'Định dạng đầu ra',
        'Choose format': 'Chọn định dạng',
        'Select': 'Chọn',
        'Apply': 'Áp dụng',
        'Cancel': 'Hủy',
        'Processing': 'Đang xử lý',
        'Max': 'Tối đa',
        'Your Browser': 'Trình duyệt của bạn',
        'Browser Support': 'Hỗ trợ trình duyệt',
        'Converting': 'Đang chuyển đổi',
        'Downloading': 'Đang tải xuống',
        'Original': 'Gốc',
        'Compressed': 'Đã nén',
        'Saved': 'Đã lưu',
        'Width': 'Chiều rộng',
        'Height': 'Chiều cao',
        'Maintain aspect ratio': 'Giữ tỷ lệ',
        'Copy': 'Sao chép',
        'Paste': 'Dán',
        'Image': 'Hình ảnh',
        'Text': 'Văn bản',
        'Opacity': 'Độ mờ',
        'Position': 'Vị trí',
        'Font': 'Phông chữ',
        'Color': 'Màu sắc',
        'Preview': 'Xem trước',
        'Save': 'Lưu',
        'Clear': 'Xóa',
        'Remove': 'Gỡ bỏ',
        'Settings': 'Cài đặt',
        'Result': 'Kết quả',
        'Drop': 'Thả',
        'or': 'hoặc',
        'Choose File': 'Chọn file',
        'per file': 'mỗi file',
        'Detected': 'Đã phát hiện',
        'faces': 'khuôn mặt',
        'blur': 'làm mờ',
        'Export': 'Xuất',
        'Copied': 'Đã sao chép',
        'Close': 'Đóng',
        'Start': 'Bắt đầu',
        'Error': 'Lỗi',
        'Success': 'Thành công',
        'Please select': 'Vui lòng chọn',
        'Drag & drop': 'Kéo và thả',
    },
    'ar': {
        'Click or drag': 'انقر أو اسحب',
        'file here': 'الملف هنا',
        'Upload': 'رفع',
        'Download': 'تحميل',
        'Convert': 'تحويل',
        'Reset': 'إعادة تعيين',
        'Quality': 'الجودة',
        'Output Format': 'تنسيق الإخراج',
        'Choose format': 'اختر التنسيق',
        'Select': 'اختيار',
        'Apply': 'تطبيق',
        'Cancel': 'إلغاء',
        'Processing': 'جاري المعالجة',
        'Max': 'الحد الأقصى',
        'Your Browser': 'متصفحك',
        'Browser Support': 'دعم المتصفح',
        'Converting': 'جاري التحويل',
        'Downloading': 'جاري التحميل',
        'Original': 'الأصلي',
        'Compressed': 'مضغوط',
        'Saved': 'تم الحفظ',
        'Width': 'العرض',
        'Height': 'الارتفاع',
        'Maintain aspect ratio': 'الحفاظ على النسب',
        'Copy': 'نسخ',
        'Paste': 'لصق',
        'Image': 'صورة',
        'Text': 'نص',
        'Opacity': 'الشفافية',
        'Position': 'الموقع',
        'Font': 'الخط',
        'Color': 'اللون',
        'Preview': 'معاينة',
        'Save': 'حفظ',
        'Clear': 'مسح',
        'Remove': 'إزالة',
        'Settings': 'الإعدادات',
        'Result': 'النتيجة',
        'Drop': 'إفلات',
        'or': 'أو',
        'Choose File': 'اختر ملفاً',
        'per file': 'لكل ملف',
        'Detected': 'تم الاكتشاف',
        'faces': 'وجوه',
        'blur': 'تمويه',
        'Export': 'تصدير',
        'Copied': 'تم النسخ',
        'Close': 'إغلاق',
        'Start': 'بدء',
        'Error': 'خطأ',
        'Success': 'نجاح',
        'Please select': 'الرجاء الاختيار',
        'Drag & drop': 'اسحب وأفلت',
    },
}

# ═══════════════════════════════════════════════════
# GENERATOR
# ═══════════════════════════════════════════════════

def translate_workspace(html, lang):
    """Translate UI labels in workspace_html"""
    labels = UI_LABELS.get(lang, {})
    result = html
    for en, trans in labels.items():
        result = result.replace(en, trans)
    return result

def generate_lang(lang_code):
    """Generate _tools_data_{LANG}.json"""
    with open(SRC, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    out = {}
    # Copy lang-level fields
    out.update(LANG_FIELDS.get(lang_code, {}))
    
    tools = []
    translations = TOOL_TRANSLATIONS.get(lang_code, {})
    
    for en_tool in en_data['tools']:
        slug = en_tool['slug']
        tool = copy.deepcopy(en_tool)
        
        # Apply translated fields
        tdata = translations.get(slug, {})
        for key in tdata:
            tool[key] = tdata[key]
        
        # Translate workspace_html labels
        if tool.get('workspace_html'):
            tool['workspace_html'] = translate_workspace(tool['workspace_html'], lang_code)
        
        # Update lang-specific paths in workspace/related
        if lang_code != 'en':
            # Replace /tools/ → /LANG/tools/ in related_html
            for field in ['related_html']:
                if tool.get(field):
                    tool[field] = tool[field].replace('/tools/', f'/{lang_code}/tools/')
        
        tools.append(tool)
    
    out['tools'] = tools
    
    # Write output
    out_path = os.path.join(ROOT, f'_tools_data_{lang_code}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    
    print(f'  ✓ Generated {out_path} ({len(tools)} tools)')
    return len(tools)

if __name__ == '__main__':
    langs = sys.argv[1:] if len(sys.argv) > 1 else ['fr', 'vi', 'ar']
    total = 0
    for lang in langs:
        if lang in LANG_FIELDS:
            total += generate_lang(lang)
        else:
            print(f'  ✗ Unknown language: {lang}')
    print(f'\nDone. {total} tools generated across {len(langs)} languages.')
