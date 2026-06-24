"""
Direct fix for remaining English guide p texts in id-photo, image-enhancer, and bulk-processor tools.
These paragraphs exist in language JSON files but may not be in the English template (or are text-divergent).
"""
import json, re

# Translation maps for remaining guide p texts (substring match on first 50-60 chars)
ID_PHOTO_MAP = {
    "The quality of your final ID photo depends heavily on the source image. For best results, follow these tips:" : {
        "es": "La calidad de tu foto de identificación final depende en gran medida de la imagen de origen. Para obtener los mejores resultados, sigue estos consejos:",
        "pt": "A qualidade da sua foto de identificação final depende muito da imagem de origem. Para obter os melhores resultados, siga estas dicas:",
        "id": "Kualitas foto ID akhir Anda sangat bergantung pada gambar sumber. Untuk hasil terbaik, ikuti tips berikut:"
    },
    "Stand against a plain, light-colored wall (white or off-white works best). Make sure your face is centered in the frame and both ears are visible. Use": {
        "es": "Párate contra una pared lisa y de color claro (blanco o blanco roto funciona mejor). Asegúrate de que tu rostro esté centrado y ambas orejas sean visibles. Usa",
        "pt": "Fique em frente a uma parede lisa e de cor clara (branco ou quase branco funciona melhor). Certifique-se de que seu rosto esteja centralizado e ambas as orelhas estejam visíveis. Use",
        "id": "Berdiri di depan dinding polos berwarna terang (putih atau putih gading paling cocok). Pastikan wajah Anda berada di tengah bingkai dan kedua telinga terlihat. Gunakan"
    },
    "Remove headwear such as hats, caps, or scarves unless worn for religious or medical reasons. Keep a neutral expression with your mouth closed and both": {
        "es": "Quítate sombreros, gorras o bufandas a menos que se usen por razones religiosas o médicas. Mantén una expresión neutral con la boca cerrada y ambos",
        "pt": "Remova chapéus, bonés ou cachecóis, a menos que sejam usados por razões religiosas ou médicas. Mantenha uma expressão neutra com a boca fechada e ambos",
        "id": "Lepaskan penutup kepala seperti topi atau syal kecuali dikenakan karena alasan agama atau medis. Jaga ekspresi netral dengan mulut tertutup dan kedua"
    },
    "Browse the country list below the upload area and click on the photo type you need. Each country has specific size requirements measured in millimeter": {
        "es": "Explora la lista de países debajo del área de carga y haz clic en el tipo de foto que necesitas. Cada país tiene requisitos de tamaño específicos medidos en milímetros",
        "pt": "Navegue pela lista de países abaixo da área de upload e clique no tipo de foto que você precisa. Cada país tem requisitos de tamanho específicos medidos em milímetros",
        "id": "Telusuri daftar negara di bawah area unggah dan klik jenis foto yang Anda butuhkan. Setiap negara memiliki persyaratan ukuran spesifik yang diukur dalam milimeter"
    },
    "If your specific ID type is not listed, use the <strong>Custom Size</strong> option at the bottom of the country list and enter the exact dimensions r": {
        "es": 'Si tu tipo de identificación específico no aparece, usa la opción <strong>Tamaño Personalizado</strong> al final de la lista de países e introduce las dimensiones exactas r',
        "pt": 'Se o seu tipo de ID específico não estiver listado, use a opção <strong>Tamanho Personalizado</strong> no final da lista de países e insira as dimensões exatas r',
        "id": 'Jika jenis ID spesifik Anda tidak tercantum, gunakan opsi <strong>Ukuran Kustom</strong> di bagian bawah daftar negara dan masukkan dimensi yang tepat r'
    },
    "Different ID documents require different background colors. Our tool lets you select from five preset colors or pick a custom color:": {
        "es": "Diferentes documentos de identidad requieren diferentes colores de fondo. Nuestra herramienta te permite seleccionar entre cinco colores predefinidos o elegir un color personalizado:",
        "pt": "Diferentes documentos de identificação exigem cores de fundo diferentes. Nossa ferramenta permite selecionar entre cinco cores predefinidas ou escolher uma cor personalizada:",
        "id": "Dokumen ID yang berbeda memerlukan warna latar belakang yang berbeda. Alat kami memungkinkan Anda memilih dari lima warna preset atau memilih warna kustom:"
    },
    "The AI background removal engine processes your photo and replaces the original background cleanly. The result is a professional, uniform background c": {
        "es": "El motor de eliminación de fondo con IA procesa tu foto y reemplaza el fondo original de forma limpia. El resultado es un fondo profesional, uniforme y c",
        "pt": "O motor de remoção de fundo com IA processa sua foto e substitui o fundo original de forma limpa. O resultado é um fundo profissional, uniforme e c",
        "id": "Mesin penghapus latar belakang AI memproses foto Anda dan mengganti latar belakang asli dengan bersih. Hasilnya adalah latar belakang profesional, seragam, dan c"
    },
    "Once you've uploaded your photo, selected the country standard, and chosen your background color, click the <strong>\"Generate ID Photo\"</strong> butto": {
        "es": 'Una vez que hayas subido tu foto, seleccionado el estándar del país y elegido el color de fondo, haz clic en el botón <strong>"Generar Foto de Identidad"</strong>',
        "pt": 'Depois de enviar sua foto, selecionar o padrão do país e escolher a cor de fundo, clique no botão <strong>"Gerar Foto de ID"</strong>',
        "id": 'Setelah Anda mengunggah foto, memilih standar negara, dan memilih warna latar belakang, klik tombol <strong>"Hasilkan Foto ID"</strong>'
    },
    "Processing typically takes 3–10 seconds depending on your device. The AI model runs entirely in your browser — nothing is uploaded to any server. Afte": {
        "es": "El procesamiento suele tardar de 3 a 10 segundos según tu dispositivo. El modelo de IA se ejecuta completamente en tu navegador — no se sube nada a ningún servidor. Despué",
        "pt": "O processamento geralmente leva de 3 a 10 segundos, dependendo do seu dispositivo. O modelo de IA é executado totalmente no seu navegador — nada é enviado para nenhum servidor. Depoi",
        "id": "Pemrosesan biasanya memakan waktu 3-10 detik tergantung perangkat Anda. Model AI berjalan sepenuhnya di browser Anda — tidak ada yang diunggah ke server mana pun. Setela"
    },
}

IMAGE_ENHANCER_MAP = {
    "Click <strong>Auto Enhance</strong> for a one-click improvement. Or try Portrait (skin tone optimize), Landscape (color boost), Vivid (max saturation)": {
        "es": "Haz clic en <strong>Mejora Automática</strong> para una mejora con un solo clic. O prueba los predefinidos Retrato (optimizar tono de piel), Paisaje (realzar color), Vibrante (saturación máx)",
        "pt": "Clique em <strong>Melhoria Automática</strong> para uma melhoria com um clique. Ou experimente as predefinições Retrato (otimizar tom de pele), Paisagem (realçar cor), Vibrante (saturação máx)",
        "id": "Klik <strong>Peningkatan Otomatis</strong> untuk peningkatan satu klik. Atau coba preset Potret (optimalkan warna kulit), Lanskap (tingkatkan warna), Cerah (saturasi maks)"
    },
    "Check \"Show Before/After\" to enable the slider comparison. Drag the slider handle to compare original and enhanced versions side by side.": {
        "es": 'Marca "Mostrar Antes/Después" para activar la comparación con deslizador. Arrastra el control deslizante para comparar las versiones original y mejorada lado a lado.',
        "pt": 'Marque "Mostrar Antes/Depois" para ativar a comparação com controle deslizante. Arraste o controle para comparar as versões original e melhorada lado a lado.',
        "id": 'Centang "Tampilkan Sebelum/Sesudah" untuk mengaktifkan perbandingan slider. Seret pegangan slider untuk membandingkan versi asli dan yang ditingkatkan berdampingan.'
    },
    "Click \"Download Enhanced\" to save your image as PNG. All processing is done in your browser — no data is uploaded to any server.": {
        "es": 'Haz clic en "Descargar Imagen Mejorada" para guardar tu imagen como PNG. Todo el procesamiento se realiza en tu navegador — no se suben datos a ningún servidor.',
        "pt": 'Clique em "Baixar Imagem Melhorada" para salvar sua imagem como PNG. Todo o processamento é feito no seu navegador — nenhum dado é enviado para nenhum servidor.',
        "id": 'Klik "Unduh Gambar yang Ditingkatkan" untuk menyimpan gambar Anda sebagai PNG. Semua pemrosesan dilakukan di browser Anda — tidak ada data yang diunggah ke server mana pun.'
    },
}

BULK_PROCESSOR_MAP = {
    "<strong>Tip:</strong> Use descriptive prefixes like <code>product_</code>, <code>gallery_</code>, or <code>photo_</code>": {
        "es": "<strong>Consejo:</strong> Usa prefijos descriptivos como <code>producto_</code>, <code>galeria_</code> o <code>foto_</code>",
        "pt": "<strong>Dica:</strong> Use prefixos descritivos como <code>produto_</code>, <code>galeria_</code> ou <code>foto_</code>",
        "id": "<strong>Tips:</strong> Gunakan awalan deskriptif seperti <code>produk_</code>, <code>galeri_</code>, atau <code>foto_</code>"
    },
    "Toggle \"Rename output files\" and set a prefix and starting number. Files will be named sequentially: <code>prefix_001.ex": {
        "es": 'Activa "Renombrar archivos de salida" y establece un prefijo y número inicial. Los archivos se nombrarán secuencialmente: <code>prefijo_001.ex',
        "pt": 'Ative "Renomear arquivos de saída" e defina um prefixo e número inicial. Os arquivos serão nomeados sequencialmente: <code>prefixo_001.ex',
        "id": 'Aktifkan "Ganti nama file output" dan atur awalan serta nomor awal. File akan dinamai secara berurutan: <code>awalan_001.ex'
    },
    "Enter target width and/or height in the Resize section. With \"Keep aspect ratio\" checked (default), the tool automatical": {
        "es": 'Introduce el ancho y/o alto deseado en la sección Redimensionar. Con "Mantener proporción" marcado (predeterminado), la herramienta calcula automáticamente',
        "pt": 'Insira a largura e/ou altura desejada na seção Redimensionar. Com "Manter proporção" marcado (padrão), a ferramenta calcula automaticamente',
        "id": 'Masukkan lebar dan/atau tinggi target di bagian Ubah Ukuran. Dengan "Pertahankan rasio aspek" dicentang (default), alat secara otomatis'
    },
    "Enter watermark text, adjust font size and opacity, and choose a position (bottom-right, bottom-left, top-right, top-lef": {
        "es": "Introduce el texto de la marca de agua, ajusta el tamaño de fuente y la opacidad, y elige una posición (abajo derecha, abajo izquierda, arriba derecha, arriba izquierda",
        "pt": "Digite o texto da marca d'água, ajuste o tamanho da fonte e a opacidade, e escolha uma posição (inferior direito, inferior esquerdo, superior direito, superior esquerdo",
        "id": "Masukkan teks watermark, sesuaikan ukuran font dan opasitas, lalu pilih posisi (kanan bawah, kiri bawah, kanan atas, kiri atas"
    },
    "Use the Output Format dropdown to convert all images to JPG, PNG, or WebP. JPG is best for photograph": {
        "es": "Usa el menú desplegable de Formato de Salida para convertir todas las imágenes a JPG, PNG o WebP. JPG es la mejor opción para fotografías",
        "pt": "Use o menu suspenso Formato de Saída para converter todas as imagens para JPG, PNG ou WebP. JPG é a melhor opção para fotografias",
        "id": "Gunakan dropdown Format Output untuk mengonversi semua gambar ke JPG, PNG, atau WebP. JPG adalah pilihan terbaik untuk foto"
    },
    "After applying a preset, you can still fine-tune individual settings in the Processing Options panel.": {
        "es": "Después de aplicar un predefinido, aún puedes ajustar las configuraciones individuales en el panel de Opciones de Procesamiento.",
        "pt": "Após aplicar uma predefinição, você ainda pode ajustar as configurações individuais no painel de Opções de Processamento.",
        "id": "Setelah menerapkan preset, Anda masih dapat menyempurnakan pengaturan individual di panel Opsi Pemrosesan."
    },
}

# Compile all maps keyed by slug
TOOL_MAPS = {
    'id-photo': ID_PHOTO_MAP,
    'image-enhancer': IMAGE_ENHANCER_MAP,
    'bulk-processor': BULK_PROCESSOR_MAP,
}

for lang in ['es', 'pt', 'id']:
    filepath = f'_tools_data_{lang}.json'
    print(f'\n=== Fixing {lang} ===')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_fixed = 0
    
    for tool in data['tools']:
        slug = tool['slug']
        if slug not in TOOL_MAPS:
            continue
        
        html = tool.get('guide_html', '')
        if not html:
            continue
        
        trans_map = TOOL_MAPS[slug]
        original = html
        tool_fixed = 0
        
        # Replace each p tag that matches a key (substring match on first 50 chars)
        for en_key, translations in trans_map.items():
            trans = translations.get(lang)
            if not trans:
                continue
            
            # Find the p tag containing this text (match first 60 chars to be safe)
            key_fragment = en_key[:60]
            if key_fragment not in html:
                continue
            
            # Build regex: <p> + escaped first 50 chars + rest of content + </p>
            escaped_key = re.escape(en_key[:50])
            before = html
            html = re.sub(
                rf'<p>({escaped_key}.*?)</p>',
                lambda m: f'<p>{trans}{m.group(1)[len(en_key):]}</p>',
                html,
                flags=re.DOTALL
            )
            if html != before:
                tool_fixed += 1
        
        if html != original:
            tool['guide_html'] = html
            print(f'  {slug}: fixed {tool_fixed} p tags')
            total_fixed += tool_fixed
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'  → Total fixed in {lang}: {total_fixed}')

print('\nDone.')
