#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix workspace_html translation for ar/fr/vi: replace blind string-replace
with HTML-aware text-node-only translation.

Root cause: _gen_translations.py translate_workspace() did raw string
replacement on the entire workspace_html blob, corrupting HTML attributes,
class names, CSS properties, IDs, and JS code.

Fix: Parse HTML, only apply translations to text nodes and safe visible
attributes (placeholder, alt, title, aria-label).
"""

import json
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── UI labels: same as _gen_translations.py but we'll use them more carefully
UI_LABELS = {
    'fr': {
        # Short single-token labels — only for text nodes, NO HTML/attribute partials
        # Multi-word phrases first, then short words
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
        'Image Size': "Taille d'image",
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
        'file here': 'tệp vào đây',
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
        'Choose File': 'Chọn tệp',
        'per file': 'mỗi tệp',
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


class SafeTranslator(HTMLParser):
    """Parse HTML, translate text nodes only, leave tags/attributes intact."""

    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        self.parts = []
        # Sort labels by length (descending) so longer phrases match first
        self.sorted_keys = sorted(labels.keys(), key=len, reverse=True)

    def handle_starttag(self, tag, attrs):
        # Translate safe visible attributes: placeholder, alt, title, aria-label, data-*
        translated = []
        for name, val in attrs:
            if val and name in ('placeholder', 'alt', 'title', 'aria-label', 'data-tooltip'):
                val = self._translate_text(val)
            translated.append((name, val))
        # Reconstruct the tag
        attrs_str = ''
        for name, val in translated:
            if val is None:
                attrs_str += f' {name}'
            else:
                # Use appropriate quotes
                if '"' in val:
                    attrs_str += f" {name}='{val}'"
                else:
                    attrs_str += f' {name}="{val}"'
        self.parts.append(f'<{tag}{attrs_str}>')

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_startendtag(self, tag, attrs):
        translated = []
        for name, val in attrs:
            if val and name in ('placeholder', 'alt', 'title', 'aria-label', 'data-tooltip'):
                val = self._translate_text(val)
            translated.append((name, val))
        attrs_str = ''
        for name, val in translated:
            if val is None:
                attrs_str += f' {name}'
            else:
                if '"' in val:
                    attrs_str += f" {name}='{val}'"
                else:
                    attrs_str += f' {name}="{val}"'
        self.parts.append(f'<{tag}{attrs_str} />')

    def handle_data(self, data):
        self.parts.append(self._translate_text(data))

    def handle_comment(self, data):
        self.parts.append(f'<!--{data}-->')

    def handle_decl(self, decl):
        self.parts.append(f'<!{decl}>')

    def handle_pi(self, data):
        self.parts.append(f'<?{data}>')

    def handle_entityref(self, name):
        self.parts.append(f'&{name};')

    def handle_charref(self, name):
        self.parts.append(f'&#{name};')

    def unknown_decl(self, data):
        self.parts.append(f'<![{data}]>')

    def _translate_text(self, text):
        """Apply word-boundary-aware translation to text content.
        
        For short/ambiguous labels (<=3 chars, or containing only common letters),
        use word-boundary regex to prevent substring corruption.
        For longer labels, simple str.replace is fine.
        """
        result = text
        for en in self.sorted_keys:
            trans = self.labels[en]
            if not en or en not in result:
                continue
            
            # Short labels (<=3 chars) and common single words -> use word boundary
            # This prevents "or" from matching inside "Supports", "color", "border"
            if len(en) <= 3 or (len(en) <= 6 and ' ' not in en and en.isascii()):
                # Use regex: replace only when surrounded by non-alpha or boundaries
                pat = r'(?<![a-zA-Z])' + re.escape(en) + r'(?![a-zA-Z])'
                result = re.sub(pat, trans, result)
            else:
                # Longer phrases: simple replace (phrases won't appear as substrings)
                result = result.replace(en, trans)
        return result

    def get_output(self):
        return ''.join(self.parts)


def translate_workspace_safe(html_str, lang):
    """Translate workspace_html using HTML-aware parser — only text nodes."""
    labels = UI_LABELS.get(lang, {})
    if not labels:
        return html_str
    parser = SafeTranslator(labels)
    parser.feed(html_str)
    return parser.get_output()


def fix_data_file(lang_code):
    """Read English data, regenerate target language data with safe translation."""
    en_path = os.path.join(ROOT, '_tools_data.json')
    out_path = os.path.join(ROOT, f'_tools_data_{lang_code}.json')

    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # Read existing translated data for language-level and tool-level fields
    with open(out_path, 'r', encoding='utf-8') as f:
        old_data = json.load(f)

    # Rebuild: start from English, apply safe workspace translation
    import copy
    out = copy.deepcopy(en_data)
    
    # Copy language-level fields from old data
    for key in old_data:
        if key != 'tools':
            out[key] = old_data[key]
    
    # Process tools: copy translated howto/faq/related from old data,
    # but regenerate workspace_html with safe translation
    for tool in out['tools']:
        slug = tool['slug']
        
        # Find old tool data
        old_tool = None
        for ot in old_data.get('tools', []):
            if ot['slug'] == slug:
                old_tool = ot
                break
        
        if old_tool:
            # Copy translated fields from old data
            for key in old_tool:
                if key == 'workspace_html':
                    # RE-TRANSLATE with safe method
                    tool['workspace_html'] = translate_workspace_safe(
                        en_data['tools'][out['tools'].index(tool)]['workspace_html'],
                        lang_code
                    )
                elif key != 'slug':
                    tool[key] = old_tool[key]
        else:
            # New tool, translate workspace
            tool['workspace_html'] = translate_workspace_safe(
                tool['workspace_html'], lang_code
            )
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    
    # Validate: check that workspace_html doesn't contain corrupted classnames
    corruptions = 0
    for tool in out['tools']:
        ws = tool.get('workspace_html', '')
        slug = tool['slug']
        # Check for common corruption patterns
        bad_patterns = [
            'bأوder', 'bhoặcder', 'bouder',  # border
            'colأو', 'colhoặc', 'colou',      # color
            'befأوe', 'befhoặce', 'befoue',    # before
            'fأو=', 'fhoặc=', 'fou=',          # for=
            'fichierInput',                     # fileInput
            'أوig', 'hoặcig', 'ouig',          # orig
            'errأو',                             # error
            'Supphoặc', 'Suppou',               # Supports
            'type="fichier"',                    # type="file"
            'new image',                        # should NOT have this translation (JS var)
        ]
        for bp in bad_patterns:
            if bp in ws:
                corruptions += 1
                break  # only count once per tool
    
    print(f'  {lang_code}: {len(out["tools"])} tools, {corruptions} with corruptions remaining')
    if corruptions > 0:
        # Show which tools
        for tool in out['tools']:
            ws = tool.get('workspace_html', '')
            for bp in bad_patterns:
                if bp in ws:
                    print(f'    ⚠ {tool["slug"]}: found "{bp}" in workspace_html')
                    # Show context
                    idx = ws.find(bp)
                    print(f'       context: ...{ws[max(0,idx-30):idx+len(bp)+30]}...')
                    break
    
    return corruptions


def validate_en_data():
    """Check English data as baseline."""
    en_path = os.path.join(ROOT, '_tools_data.json')
    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    bad_patterns = [
        'bأوder', 'bhoặcder', 'bouder',
        'colأو', 'colhoặc', 'colou',
        'befأوe', 'befhoặce', 'befoue',
        'fأو=', 'fhoặc=', 'fou=',
        'fichierInput', 'أوig', 'hoặcig', 'ouig',
        'errأو', 'Supphoặc', 'Suppou',
        'type="fichier"',
    ]
    
    clean = 0
    dirty = 0
    for tool in en_data['tools']:
        ws = tool.get('workspace_html', '')
        is_clean = True
        for bp in bad_patterns:
            if bp in ws:
                dirty += 1
                is_clean = False
                print(f'  en/{tool["slug"]}: found "{bp}"')
                break
        if is_clean:
            clean += 1
    
    print(f'English data: {clean} clean, {dirty} corrupted')
    return dirty == 0


if __name__ == '__main__':
    # First validate English is clean
    print('Validating English data...')
    if not validate_en_data():
        print('ERROR: English data is corrupted! Aborting.')
        sys.exit(1)
    
    # Fix each language
    langs = ['ar', 'fr', 'vi']
    total_corruptions = 0
    for lang in langs:
        print(f'\nFixing {lang}...')
        c = fix_data_file(lang)
        total_corruptions += c
    
    if total_corruptions > 0:
        print(f'\n⚠ {total_corruptions} corruptions remain. May need manual fix.')
        sys.exit(1)
    else:
        print(f'\n✅ All {len(langs)} languages fixed! 0 corruptions.')
