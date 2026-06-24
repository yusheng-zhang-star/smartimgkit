"""
Translate howto_html and guide_html for all tools in ES, PT, ID.
Uses translation dictionaries for all unique h4/h3/p texts.
"""
import json
import re

# ============================================================
# HOWTO H4 TITLE TRANSLATIONS
# ============================================================
HOWTO_H4 = {
    # EN → {es, pt, id}
    "AI Processing": {"es": "Procesamiento IA", "pt": "Processamento IA", "id": "Pemrosesan AI"},
    "Add Text": {"es": "Añadir Texto", "pt": "Adicionar Texto", "id": "Tambah Teks"},
    "Add to Site": {"es": "Añadir al Sitio", "pt": "Adicionar ao Site", "id": "Tambahkan ke Situs"},
    "Adjust": {"es": "Ajustar", "pt": "Ajustar", "id": "Sesuaikan"},
    "Adjust Circle": {"es": "Ajustar Círculo", "pt": "Ajustar Círculo", "id": "Sesuaikan Lingkaran"},
    "Adjust Count": {"es": "Ajustar Cantidad", "pt": "Ajustar Quantidade", "id": "Sesuaikan Jumlah"},
    "Adjust Quality": {"es": "Ajustar Calidad", "pt": "Ajustar Qualidade", "id": "Sesuaikan Kualitas"},
    "Adjust Selection": {"es": "Ajustar Selección", "pt": "Ajustar Seleção", "id": "Sesuaikan Pilihan"},
    "Adjust Settings": {"es": "Ajustar Configuración", "pt": "Ajustar Configurações", "id": "Sesuaikan Pengaturan"},
    "Adjust Shadow": {"es": "Ajustar Sombra", "pt": "Ajustar Sombra", "id": "Sesuaikan Bayangan"},
    "Apply & Save": {"es": "Aplicar y Guardar", "pt": "Aplicar e Salvar", "id": "Terapkan & Simpan"},
    "Blur Mode": {"es": "Modo Difuminado", "pt": "Modo Desfoque", "id": "Mode Buram"},
    "Check Browser Support": {"es": "Verificar Compatibilidad", "pt": "Verificar Suporte", "id": "Periksa Dukungan"},
    "Choose Background": {"es": "Elegir Fondo", "pt": "Escolher Fundo", "id": "Pilih Latar"},
    "Choose Direction": {"es": "Elegir Dirección", "pt": "Escolher Direção", "id": "Pilih Arah"},
    "Choose Effect": {"es": "Elegir Efecto", "pt": "Escolher Efeito", "id": "Pilih Efek"},
    "Choose Format": {"es": "Elegir Formato", "pt": "Escolher Formato", "id": "Pilih Format"},
    "Choose Frame Style": {"es": "Elegir Estilo Marco", "pt": "Escolher Estilo Moldura", "id": "Pilih Gaya Bingkai"},
    "Choose Grid": {"es": "Elegir Cuadrícula", "pt": "Escolher Grade", "id": "Pilih Grid"},
    "Choose Layout": {"es": "Elegir Diseño", "pt": "Escolher Layout", "id": "Pilih Tata Letak"},
    "Choose Mode": {"es": "Elegir Modo", "pt": "Escolher Modo", "id": "Pilih Mode"},
    "Choose Output Format": {"es": "Elegir Formato Salida", "pt": "Escolher Formato Saída", "id": "Pilih Format Output"},
    "Choose Paper Size": {"es": "Elegir Tamaño Papel", "pt": "Escolher Tamanho Papel", "id": "Pilih Ukuran Kertas"},
    "Choose Preset Filter": {"es": "Elegir Filtro Predefinido", "pt": "Escolher Filtro Predefinido", "id": "Pilih Filter Preset"},
    "Choose Scale": {"es": "Elegir Escala", "pt": "Escolher Escala", "id": "Pilih Skala"},
    "Choose Settings": {"es": "Elegir Ajustes", "pt": "Escolher Configurações", "id": "Pilih Pengaturan"},
    "Choose Template": {"es": "Elegir Plantilla", "pt": "Escolher Modelo", "id": "Pilih Template"},
    "Compare": {"es": "Comparar", "pt": "Comparar", "id": "Bandingkan"},
    "Compress & Download": {"es": "Comprimir y Descargar", "pt": "Comprimir e Baixar", "id": "Kompres & Unduh"},
    "Configure": {"es": "Configurar", "pt": "Configurar", "id": "Konfigurasi"},
    "Convert": {"es": "Convertir", "pt": "Converter", "id": "Konversi"},
    "Convert & Download": {"es": "Convertir y Descargar", "pt": "Converter e Baixar", "id": "Konversi & Unduh"},
    "Copy or Download": {"es": "Copiar o Descargar", "pt": "Copiar ou Baixar", "id": "Salin atau Unduh"},
    "Crop & Save": {"es": "Recortar y Guardar", "pt": "Recortar e Salvar", "id": "Potong & Simpan"},
    "Customize": {"es": "Personalizar", "pt": "Personalizar", "id": "Kustomisasi"},
    "Customize Appearance": {"es": "Personalizar Apariencia", "pt": "Personalizar Aparência", "id": "Kustomisasi Tampilan"},
    "Download": {"es": "Descargar", "pt": "Baixar", "id": "Unduh"},
    "Download PNG": {"es": "Descargar PNG", "pt": "Baixar PNG", "id": "Unduh PNG"},
    "Download ZIP": {"es": "Descargar ZIP", "pt": "Baixar ZIP", "id": "Unduh ZIP"},
    "Drop Images": {"es": "Soltar Imágenes", "pt": "Soltar Imagens", "id": "Lepaskan Gambar"},
    "Export or Remove": {"es": "Exportar o Eliminar", "pt": "Exportar ou Remover", "id": "Ekspor atau Hapus"},
    "Extract": {"es": "Extraer", "pt": "Extrair", "id": "Ekstrak"},
    "Extract & Copy": {"es": "Extraer y Copiar", "pt": "Extrair e Copiar", "id": "Ekstrak & Salin"},
    "Fine-Tune": {"es": "Ajustar Detalles", "pt": "Ajustar Detalhes", "id": "Sempurnakan"},
    "Generate": {"es": "Generar", "pt": "Gerar", "id": "Hasilkan"},
    "Get Result": {"es": "Obtener Resultado", "pt": "Obter Resultado", "id": "Dapatkan Hasil"},
    "Input": {"es": "Entrada", "pt": "Entrada", "id": "Masukan"},
    "Pick Language": {"es": "Elegir Idioma", "pt": "Escolher Idioma", "id": "Pilih Bahasa"},
    "Pick Sizes": {"es": "Elegir Tamaños", "pt": "Escolher Tamanhos", "id": "Pilih Ukuran"},
    "Pick a Type": {"es": "Elegir Tipo", "pt": "Escolher Tipo", "id": "Pilih Jenis"},
    "Position & Customize": {"es": "Posicionar y Personalizar", "pt": "Posicionar e Personalizar", "id": "Posisikan & Kustomisasi"},
    "Preview": {"es": "Vista Previa", "pt": "Pré-visualizar", "id": "Pratinjau"},
    "Preview Sizes": {"es": "Vista Previa Tamaños", "pt": "Pré-visualizar Tamanhos", "id": "Pratinjau Ukuran"},
    "Process All": {"es": "Procesar Todo", "pt": "Processar Tudo", "id": "Proses Semua"},
    "Remove EXIF": {"es": "Eliminar EXIF", "pt": "Remover EXIF", "id": "Hapus EXIF"},
    "Reorder": {"es": "Reordenar", "pt": "Reordenar", "id": "Urutkan Ulang"},
    "Resize & Save": {"es": "Redimensionar y Guardar", "pt": "Redimensionar e Salvar", "id": "Ubah Ukuran & Simpan"},
    "Rotate or Flip": {"es": "Rotar o Voltear", "pt": "Rotacionar ou Inverter", "id": "Putar atau Balik"},
    "Set DPI": {"es": "Establecer DPI", "pt": "Definir DPI", "id": "Atur DPI"},
    "Set Dimensions": {"es": "Establecer Dimensiones", "pt": "Definir Dimensões", "id": "Atur Dimensi"},
    "Set Max Width": {"es": "Establecer Ancho Máx", "pt": "Definir Largura Máx", "id": "Atur Lebar Maks"},
    "Set Options": {"es": "Establecer Opciones", "pt": "Definir Opções", "id": "Atur Opsi"},
    "Set Quality": {"es": "Establecer Calidad", "pt": "Definir Qualidade", "id": "Atur Kualitas"},
    "Tweak": {"es": "Ajustar", "pt": "Ajustar", "id": "Sesuaikan"},
    "Type Your Text": {"es": "Escribe tu Texto", "pt": "Digite seu Texto", "id": "Ketik Teks Anda"},
    "Upload": {"es": "Subir", "pt": "Enviar", "id": "Unggah"},
    "Upload AVIF": {"es": "Subir AVIF", "pt": "Enviar AVIF", "id": "Unggah AVIF"},
    "Upload Both Images": {"es": "Subir Ambas Imágenes", "pt": "Enviar Ambas Imagens", "id": "Unggah Kedua Gambar"},
    "Upload HEIC": {"es": "Subir HEIC", "pt": "Enviar HEIC", "id": "Unggah HEIC"},
    "Upload Image": {"es": "Subir Imagen", "pt": "Enviar Imagem", "id": "Unggah Gambar"},
    "Upload Images": {"es": "Subir Imágenes", "pt": "Enviar Imagens", "id": "Unggah Gambar"},
    "Upload PDF": {"es": "Subir PDF", "pt": "Enviar PDF", "id": "Unggah PDF"},
    "Upload SVG": {"es": "Subir SVG", "pt": "Enviar SVG", "id": "Unggah SVG"},
    "Upload Screenshot": {"es": "Subir Captura", "pt": "Enviar Captura", "id": "Unggah Screenshot"},
    "View Metadata": {"es": "Ver Metadatos", "pt": "Ver Metadados", "id": "Lihat Metadata"},
}

# ============================================================
# GUIDE H3 TITLE TRANSLATIONS
# ============================================================
GUIDE_H3 = {
    "Best Settings by Use Case": {"es": "Mejores Ajustes por Caso de Uso", "pt": "Melhores Configurações por Caso de Uso", "id": "Pengaturan Terbaik per Kasus"},
    "Best Use Cases": {"es": "Mejores Casos de Uso", "pt": "Melhores Casos de Uso", "id": "Kasus Penggunaan Terbaik"},
    "Browser Support Summary": {"es": "Resumen de Compatibilidad", "pt": "Resumo de Compatibilidade", "id": "Ringkasan Dukungan Browser"},
    "Common Conversion Scenarios": {"es": "Escenarios Comunes de Conversión", "pt": "Cenários Comuns de Conversão", "id": "Skenario Konversi Umum"},
    "Common Social Media Sizes": {"es": "Tamaños Comunes para Redes Sociales", "pt": "Tamanhos Comuns para Redes Sociais", "id": "Ukuran Umum Media Sosial"},
    "Common Use Cases": {"es": "Casos de Uso Comunes", "pt": "Casos de Uso Comuns", "id": "Kasus Penggunaan Umum"},
    "Error Correction Levels": {"es": "Niveles de Corrección de Errores", "pt": "Níveis de Correção de Erros", "id": "Level Koreksi Error"},
    "HEIC vs JPG vs PNG": {"es": "HEIC vs JPG vs PNG", "pt": "HEIC vs JPG vs PNG", "id": "HEIC vs JPG vs PNG"},
    "ICO File Format": {"es": "Formato de Archivo ICO", "pt": "Formato de Arquivo ICO", "id": "Format File ICO"},
    "Mode 1: Image → Base64 (Encoding)": {"es": "Modo 1: Imagen → Base64 (Codificar)", "pt": "Modo 1: Imagem → Base64 (Codificar)", "id": "Mode 1: Gambar → Base64 (Encoding)"},
    "Mode 2: Base64 → Image (Decoding)": {"es": "Modo 2: Base64 → Imagen (Decodificar)", "pt": "Modo 2: Base64 → Imagem (Decodificar)", "id": "Mode 2: Base64 → Gambar (Decoding)"},
    "Privacy Risks": {"es": "Riesgos de Privacidad", "pt": "Riscos de Privacidade", "id": "Risiko Privasi"},
    "Pro Tips": {"es": "Consejos Profesionales", "pt": "Dicas Profissionais", "id": "Tips Profesional"},
    "What AI Model Is Used?": {"es": "¿Qué Modelo de IA se Usa?", "pt": "Qual Modelo de IA é Usado?", "id": "Model AI Apa yang Digunakan?"},
    "What is EXIF?": {"es": "¿Qué es EXIF?", "pt": "O que é EXIF?", "id": "Apa itu EXIF?"},
    "What is HEIC?": {"es": "¿Qué es HEIC?", "pt": "O que é HEIC?", "id": "Apa itu HEIC?"},
    "When to Blur Faces": {"es": "Cuándo Difuminar Rostros", "pt": "Quando Desfocar Rostos", "id": "Kapan Memburamkan Wajah"},
    "Why All These Sizes?": {"es": "¿Por Qué Tantos Tamaños?", "pt": "Por Que Tantos Tamanhos?", "id": "Mengapa Banyak Ukuran?"},
    "Why Remove EXIF?": {"es": "¿Por Qué Eliminar EXIF?", "pt": "Por Que Remover EXIF?", "id": "Mengapa Hapus EXIF?"},
}

# Step N: prefixes
STEP_PREFIXES = {
    "es": {"Step": "Paso", "Check Your Browser Support": "Verificar Compatibilidad del Navegador",
           "Choose a Content Type": "Elegir Tipo de Contenido", "Choose a Template": "Elegir Plantilla",
           "Upload Both Images": "Subir Ambas Imágenes", "Upload HEIC Files": "Subir Archivos HEIC",
           "Upload Images": "Subir Imágenes", "Upload Multiple Images": "Subir Varias Imágenes",
           "Upload PDF": "Subir PDF", "Upload Your Image": "Subir tu Imagen",
           "Upload Your Images": "Subir tus Imágenes", "Upload Your Screenshot": "Subir tu Captura",
           "Upload a Square Image": "Subir Imagen Cuadrada", "Upload an Image": "Subir una Imagen",
           "Upload or Paste SVG": "Subir o Pegar SVG", "Add Your Text": "Añadir tu Texto",
           "Adjust Border & Corner Settings": "Ajustar Borde y Esquinas",
           "Adjust Brightness, Contrast & Saturation": "Ajustar Brillo, Contraste y Saturación",
           "Adjust Quality Settings": "Ajustar Configuración de Calidad",
           "Adjust the Crop Area": "Ajustar Área de Recorte", "Apply a Preset Filter": "Aplicar Filtro Predefinido",
           "Choose Blur Mode": "Elegir Modo de Difuminado", "Choose Color Count": "Elegir Cantidad de Colores",
           "Choose Comparison Mode": "Elegir Modo de Comparación", "Choose Flip Direction": "Elegir Dirección de Volteo",
           "Choose Grid Size": "Elegir Tamaño de Cuadrícula", "Choose Output Format": "Elegir Formato de Salida",
           "Choose Page Range": "Elegir Rango de Páginas", "Choose Paper Size": "Elegir Tamaño de Papel",
           "Choose Quality": "Elegir Calidad", "Choose Watermark Type": "Elegir Tipo de Marca de Agua",
           "Choose Your Scale Factor": "Elegir Factor de Escala", "Choose Your Transformation": "Elegir Transformación",
           "Choose a Color Effect": "Elegir Efecto de Color", "Choose a Frame Style": "Elegir Estilo de Marco",
           "Configure Processing Options": "Configurar Opciones de Procesamiento",
           "Customize Shadow Settings": "Personalizar Ajustes de Sombra", "Enter Your Text": "Introducir tu Texto",
           "Fill in the Content": "Rellenar Contenido", "Pick Sizes": "Elegir Tamaños",
           "Pick a Layout Mode": "Elegir Modo de Diseño", "Pick the Language": "Elegir Idioma",
           "Position the Circle": "Posicionar el Círculo", "Preview All Sizes": "Previsualizar Todos los Tamaños",
           "Remove EXIF Metadata": "Eliminar Metadatos EXIF", "Reorder Frames": "Reordenar Fotogramas",
           "Reorder Pages": "Reordenar Páginas", "Set New Dimensions": "Establecer Nuevas Dimensiones",
           "Set Quality": "Establecer Calidad", "View Metadata Categories": "Ver Categorías de Metadatos",
           "Adjust Blur Strength": "Ajustar Fuerza de Difuminado", "Adjust Quality": "Ajustar Calidad",
           "Adjust Rendering": "Ajustar Renderizado", "Adjust Settings": "Ajustar Configuración",
           "Adjust Sharpening": "Ajustar Nitidez", "Apply & Download": "Aplicar y Descargar",
           "Check for Privacy Risks": "Verificar Riesgos de Privacidad",
           "Choose Background": "Elegir Fondo",
           "Click \"Remove Background\"": 'Hacer Clic en "Quitar Fondo"',
           "Compress & Compare": "Comprimir y Comparar",
           "Configure Page Settings": "Configurar Ajustes de Página", "Convert": "Convertir",
           "Convert & Download": "Convertir y Descargar", "Crop & Download": "Recortar y Descargar",
           "Customize Appearance": "Personalizar Apariencia", "Customize Text Style": "Personalizar Estilo de Texto",
           "Customize the Appearance": "Personalizar la Apariencia",
           "Download Clean Image": "Descargar Imagen Limpia", "Download Pieces": "Descargar Piezas",
           "Download ZIP": "Descargar ZIP", "Extract & Use": "Extraer y Usar", "Extract Text": "Extraer Texto",
           "Fine-Tune the Result": "Ajustar el Resultado", "Fine-Tune with Sliders": "Ajustar con Deslizadores",
           "Interact & Compare": "Interactuar y Comparar", "Position & Apply": "Posicionar y Aplicar",
           "Position & Style": "Posicionar y Estilizar", "Process All": "Procesar Todo",
           "Reorder & Customize": "Reordenar y Personalizar",
           "Resize & Download": "Redimensionar y Descargar",
           "Set DPI (Dots Per Inch)": "Establecer DPI (Puntos por Pulgada)",
           "Set Max Width (Optional)": "Establecer Ancho Máx (Opcional)",
           "Set Scale Factor": "Establecer Factor de Escala",
           "Add a Center Logo (Optional)": "Añadir Logo Central (Opcional)",
           "Add to Your Site": "Añadir a tu Sitio",
           "Compress and Download": "Comprimir y Descargar",
           "Convert and Download": "Convertir y Descargar",
           "Copy or Download": "Copiar o Descargar", "Download": "Descargar",
           "Generate GIF": "Generar GIF", "Merge & Download": "Unir y Descargar",
           "Preview": "Vista Previa", "Preview & Refine": "Previsualizar y Refinar",
           "Preview the Result": "Previsualizar el Resultado",
           "Remove Metadata (Optional)": "Eliminar Metadatos (Opcional)",
           "Set Resolution": "Establecer Resolución",
           "Upload AVIF File": "Subir Archivo AVIF",
           "Upscale & Download": "Ampliar y Descargar",
           "Preview & Download": "Previsualizar y Descargar",
           "Batch (Optional)": "Lote (Opcional)",
           "Tips for Best Accuracy": "Consejos para Mejor Precisión",
           "Tips for Better GIFs": "Consejos para Mejores GIFs",
    },
    "pt": {"Step": "Passo", "Check Your Browser Support": "Verificar Suporte do Navegador",
           "Choose a Content Type": "Escolher Tipo de Conteúdo", "Choose a Template": "Escolher Modelo",
           "Upload Both Images": "Enviar Ambas Imagens", "Upload HEIC Files": "Enviar Arquivos HEIC",
           "Upload Images": "Enviar Imagens", "Upload Multiple Images": "Enviar Várias Imagens",
           "Upload PDF": "Enviar PDF", "Upload Your Image": "Enviar sua Imagem",
           "Upload Your Images": "Enviar suas Imagens", "Upload Your Screenshot": "Enviar sua Captura",
           "Upload a Square Image": "Enviar Imagem Quadrada", "Upload an Image": "Enviar uma Imagem",
           "Upload or Paste SVG": "Enviar ou Colar SVG", "Add Your Text": "Adicionar seu Texto",
           "Adjust Border & Corner Settings": "Ajustar Borda e Cantos",
           "Adjust Brightness, Contrast & Saturation": "Ajustar Brilho, Contraste e Saturação",
           "Adjust Quality Settings": "Ajustar Configurações de Qualidade",
           "Adjust the Crop Area": "Ajustar Área de Recorte", "Apply a Preset Filter": "Aplicar Filtro Predefinido",
           "Choose Blur Mode": "Escolher Modo de Desfoque", "Choose Color Count": "Escolher Quantidade de Cores",
           "Choose Comparison Mode": "Escolher Modo de Comparação", "Choose Flip Direction": "Escolher Direção de Inversão",
           "Choose Grid Size": "Escolher Tamanho da Grade", "Choose Output Format": "Escolher Formato de Saída",
           "Choose Page Range": "Escolher Intervalo de Páginas", "Choose Paper Size": "Escolher Tamanho do Papel",
           "Choose Quality": "Escolher Qualidade", "Choose Watermark Type": "Escolher Tipo de Marca D'água",
           "Choose Your Scale Factor": "Escolher Fator de Escala", "Choose Your Transformation": "Escolher Transformação",
           "Choose a Color Effect": "Escolher Efeito de Cor", "Choose a Frame Style": "Escolher Estilo de Moldura",
           "Configure Processing Options": "Configurar Opções de Processamento",
           "Customize Shadow Settings": "Personalizar Configurações de Sombra", "Enter Your Text": "Digitar seu Texto",
           "Fill in the Content": "Preencher Conteúdo", "Pick Sizes": "Escolher Tamanhos",
           "Pick a Layout Mode": "Escolher Modo de Layout", "Pick the Language": "Escolher Idioma",
           "Position the Circle": "Posicionar o Círculo", "Preview All Sizes": "Pré-visualizar Todos os Tamanhos",
           "Remove EXIF Metadata": "Remover Metadados EXIF", "Reorder Frames": "Reordenar Quadros",
           "Reorder Pages": "Reordenar Páginas", "Set New Dimensions": "Definir Novas Dimensões",
           "Set Quality": "Definir Qualidade", "View Metadata Categories": "Ver Categorias de Metadados",
           "Adjust Blur Strength": "Ajustar Força do Desfoque", "Adjust Quality": "Ajustar Qualidade",
           "Adjust Rendering": "Ajustar Renderização", "Adjust Settings": "Ajustar Configurações",
           "Adjust Sharpening": "Ajustar Nitidez", "Apply & Download": "Aplicar e Baixar",
           "Check for Privacy Risks": "Verificar Riscos de Privacidade",
           "Choose Background": "Escolher Fundo",
           "Click \"Remove Background\"": 'Clicar em "Remover Fundo"',
           "Compress & Compare": "Comprimir e Comparar",
           "Configure Page Settings": "Configurar Ajustes de Página", "Convert": "Converter",
           "Convert & Download": "Converter e Baixar", "Crop & Download": "Recortar e Baixar",
           "Customize Appearance": "Personalizar Aparência", "Customize Text Style": "Personalizar Estilo do Texto",
           "Customize the Appearance": "Personalizar a Aparência",
           "Download Clean Image": "Baixar Imagem Limpa", "Download Pieces": "Baixar Partes",
           "Download ZIP": "Baixar ZIP", "Extract & Use": "Extrair e Usar", "Extract Text": "Extrair Texto",
           "Fine-Tune the Result": "Ajustar o Resultado", "Fine-Tune with Sliders": "Ajustar com Controles",
           "Interact & Compare": "Interagir e Comparar", "Position & Apply": "Posicionar e Aplicar",
           "Position & Style": "Posicionar e Estilizar", "Process All": "Processar Tudo",
           "Reorder & Customize": "Reordenar e Personalizar",
           "Resize & Download": "Redimensionar e Baixar",
           "Set DPI (Dots Per Inch)": "Definir DPI (Pontos por Polegada)",
           "Set Max Width (Optional)": "Definir Largura Máx (Opcional)",
           "Set Scale Factor": "Definir Fator de Escala",
           "Add a Center Logo (Optional)": "Adicionar Logo Central (Opcional)",
           "Add to Your Site": "Adicionar ao seu Site",
           "Compress and Download": "Comprimir e Baixar",
           "Convert and Download": "Converter e Baixar",
           "Copy or Download": "Copiar ou Baixar", "Download": "Baixar",
           "Generate GIF": "Gerar GIF", "Merge & Download": "Unir e Baixar",
           "Preview": "Pré-visualizar", "Preview & Refine": "Pré-visualizar e Refinar",
           "Preview the Result": "Pré-visualizar o Resultado",
           "Remove Metadata (Optional)": "Remover Metadados (Opcional)",
           "Set Resolution": "Definir Resolução",
           "Upload AVIF File": "Enviar Arquivo AVIF",
           "Upscale & Download": "Ampliar e Baixar",
           "Preview & Download": "Pré-visualizar e Baixar",
           "Batch (Optional)": "Lote (Opcional)",
           "Tips for Best Accuracy": "Dicas para Melhor Precisão",
           "Tips for Better GIFs": "Dicas para Melhores GIFs",
    },
    "id": {"Step": "Langkah", "Check Your Browser Support": "Periksa Dukungan Browser Anda",
           "Choose a Content Type": "Pilih Jenis Konten", "Choose a Template": "Pilih Template",
           "Upload Both Images": "Unggah Kedua Gambar", "Upload HEIC Files": "Unggah File HEIC",
           "Upload Images": "Unggah Gambar", "Upload Multiple Images": "Unggah Beberapa Gambar",
           "Upload PDF": "Unggah PDF", "Upload Your Image": "Unggah Gambar Anda",
           "Upload Your Images": "Unggah Gambar Anda", "Upload Your Screenshot": "Unggah Screenshot Anda",
           "Upload a Square Image": "Unggah Gambar Persegi", "Upload an Image": "Unggah Gambar",
           "Upload or Paste SVG": "Unggah atau Tempel SVG", "Add Your Text": "Tambah Teks Anda",
           "Adjust Border & Corner Settings": "Sesuaikan Pengaturan Bingkai & Sudut",
           "Adjust Brightness, Contrast & Saturation": "Sesuaikan Kecerahan, Kontras & Saturasi",
           "Adjust Quality Settings": "Sesuaikan Pengaturan Kualitas",
           "Adjust the Crop Area": "Sesuaikan Area Potong", "Apply a Preset Filter": "Terapkan Filter Preset",
           "Choose Blur Mode": "Pilih Mode Buram", "Choose Color Count": "Pilih Jumlah Warna",
           "Choose Comparison Mode": "Pilih Mode Perbandingan", "Choose Flip Direction": "Pilih Arah Balik",
           "Choose Grid Size": "Pilih Ukuran Grid", "Choose Output Format": "Pilih Format Output",
           "Choose Page Range": "Pilih Rentang Halaman", "Choose Paper Size": "Pilih Ukuran Kertas",
           "Choose Quality": "Pilih Kualitas", "Choose Watermark Type": "Pilih Jenis Watermark",
           "Choose Your Scale Factor": "Pilih Faktor Skala", "Choose Your Transformation": "Pilih Transformasi",
           "Choose a Color Effect": "Pilih Efek Warna", "Choose a Frame Style": "Pilih Gaya Bingkai",
           "Configure Processing Options": "Konfigurasi Opsi Pemrosesan",
           "Customize Shadow Settings": "Kustomisasi Pengaturan Bayangan", "Enter Your Text": "Masukkan Teks Anda",
           "Fill in the Content": "Isi Konten", "Pick Sizes": "Pilih Ukuran",
           "Pick a Layout Mode": "Pilih Mode Tata Letak", "Pick the Language": "Pilih Bahasa",
           "Position the Circle": "Posisikan Lingkaran", "Preview All Sizes": "Pratinjau Semua Ukuran",
           "Remove EXIF Metadata": "Hapus Metadata EXIF", "Reorder Frames": "Urutkan Ulang Frame",
           "Reorder Pages": "Urutkan Ulang Halaman", "Set New Dimensions": "Atur Dimensi Baru",
           "Set Quality": "Atur Kualitas", "View Metadata Categories": "Lihat Kategori Metadata",
           "Adjust Blur Strength": "Sesuaikan Kekuatan Buram", "Adjust Quality": "Sesuaikan Kualitas",
           "Adjust Rendering": "Sesuaikan Rendering", "Adjust Settings": "Sesuaikan Pengaturan",
           "Adjust Sharpening": "Sesuaikan Ketajaman", "Apply & Download": "Terapkan & Unduh",
           "Check for Privacy Risks": "Periksa Risiko Privasi",
           "Choose Background": "Pilih Latar Belakang",
           "Click \"Remove Background\"": 'Klik "Hapus Latar Belakang"',
           "Compress & Compare": "Kompres & Bandingkan",
           "Configure Page Settings": "Konfigurasi Pengaturan Halaman", "Convert": "Konversi",
           "Convert & Download": "Konversi & Unduh", "Crop & Download": "Potong & Unduh",
           "Customize Appearance": "Kustomisasi Tampilan", "Customize Text Style": "Kustomisasi Gaya Teks",
           "Customize the Appearance": "Kustomisasi Tampilan",
           "Download Clean Image": "Unduh Gambar Bersih", "Download Pieces": "Unduh Potongan",
           "Download ZIP": "Unduh ZIP", "Extract & Use": "Ekstrak & Gunakan", "Extract Text": "Ekstrak Teks",
           "Fine-Tune the Result": "Sempurnakan Hasil", "Fine-Tune with Sliders": "Sempurnakan dengan Slider",
           "Interact & Compare": "Interaksi & Bandingkan", "Position & Apply": "Posisikan & Terapkan",
           "Position & Style": "Posisikan & Gaya", "Process All": "Proses Semua",
           "Reorder & Customize": "Urutkan Ulang & Kustomisasi",
           "Resize & Download": "Ubah Ukuran & Unduh",
           "Set DPI (Dots Per Inch)": "Atur DPI (Titik per Inci)",
           "Set Max Width (Optional)": "Atur Lebar Maks (Opsional)",
           "Set Scale Factor": "Atur Faktor Skala",
           "Add a Center Logo (Optional)": "Tambah Logo Tengah (Opsional)",
           "Add to Your Site": "Tambahkan ke Situs Anda",
           "Compress and Download": "Kompres dan Unduh",
           "Convert and Download": "Konversi dan Unduh",
           "Copy or Download": "Salin atau Unduh", "Download": "Unduh",
           "Generate GIF": "Hasilkan GIF", "Merge & Download": "Gabung & Unduh",
           "Preview": "Pratinjau", "Preview & Refine": "Pratinjau & Sempurnakan",
           "Preview the Result": "Pratinjau Hasil",
           "Remove Metadata (Optional)": "Hapus Metadata (Opsional)",
           "Set Resolution": "Atur Resolusi",
           "Upload AVIF File": "Unggah File AVIF",
           "Upscale & Download": "Perbesar & Unduh",
           "Preview & Download": "Pratinjau & Unduh",
           "Batch (Optional)": "Batch (Opsional)",
           "Tips for Best Accuracy": "Tips untuk Akurasi Terbaik",
           "Tips for Better GIFs": "Tips untuk GIF Lebih Baik",
    },
}

# ============================================================
# HOWTO P DESCRIPTION TRANSLATIONS
# ============================================================
HOWTO_P = {}

# Add all howto p descriptions to the translation map
_raw_howto_ps = {
    "Adjust corner radius, border width, and colors.": {
        "es": "Ajusta el radio de esquina, ancho de borde y colores.",
        "pt": "Ajuste o raio do canto, largura da borda e cores.",
        "id": "Sesuaikan radius sudut, lebar bingkai, dan warna."
    },
    "Adjust padding, corner radius, shadow, scale, and other visual options.": {
        "es": "Ajusta el relleno, radio de esquina, sombra, escala y otras opciones visuales.",
        "pt": "Ajuste o preenchimento, raio do canto, sombra, escala e outras opções visuais.",
        "id": "Sesuaikan padding, radius sudut, bayangan, skala, dan opsi visual lainnya."
    },
    "Adjust scaling, rounded corners, background, and padding.": {
        "es": "Ajusta la escala, esquinas redondeadas, fondo y relleno.",
        "pt": "Ajuste a escala, cantos arredondados, fundo e preenchimento.",
        "id": "Sesuaikan skala, sudut bulat, latar belakang, dan padding."
    },
    "Adjust spacing, border radius, background color. Drag to reorder images.": {
        "es": "Ajusta el espaciado, radio de borde y color de fondo. Arrastra para reordenar.",
        "pt": "Ajuste o espaçamento, raio da borda e cor de fundo. Arraste para reordenar.",
        "id": "Sesuaikan jarak, radius bingkai, warna latar. Seret untuk mengurutkan ulang."
    },
    "Adjust the quality slider (lower = smaller files).": {
        "es": "Ajusta el control de calidad (menor = archivos más pequeños).",
        "pt": "Ajuste o controle de qualidade (menor = arquivos menores).",
        "id": "Sesuaikan slider kualitas (lebih rendah = file lebih kecil)."
    },
    "All detected metadata is displayed by category.": {
        "es": "Todos los metadatos detectados se muestran por categoría.",
        "pt": "Todos os metadados detectados são exibidos por categoria.",
        "id": "Semua metadata yang terdeteksi ditampilkan berdasarkan kategori."
    },
    "Change text case, outline width, and font size.": {
        "es": "Cambia mayúsculas, ancho de contorno y tamaño de fuente.",
        "pt": "Altere caixa do texto, largura do contorno e tamanho da fonte.",
        "id": "Ubah kapitalisasi teks, lebar outline, dan ukuran font."
    },
    "Check horizontal, vertical, or both.": {
        "es": "Marca horizontal, vertical o ambos.",
        "pt": "Marque horizontal, vertical ou ambos.",
        "id": "Centang horizontal, vertikal, atau keduanya."
    },
    "Choose 72–600 DPI depending on print quality needed.": {
        "es": "Elige 72–600 DPI según la calidad de impresión necesaria.",
        "pt": "Escolha 72–600 DPI dependendo da qualidade de impressão necessária.",
        "id": "Pilih 72–600 DPI tergantung kualitas cetak yang dibutuhkan."
    },
    "Choose URL, plain text, WiFi credentials, vCard, or email.": {
        "es": "Elige URL, texto plano, credenciales WiFi, vCard o email.",
        "pt": "Escolha URL, texto simples, credenciais WiFi, vCard ou email.",
        "id": "Pilih URL, teks biasa, kredensial WiFi, vCard, atau email."
    },
    "Choose auto-detect, manual, or both.": {
        "es": "Elige detección automática, manual o ambas.",
        "pt": "Escolha detecção automática, manual ou ambas.",
        "id": "Pilih deteksi otomatis, manual, atau keduanya."
    },
    "Choose how many dominant colors to extract (3–12).": {
        "es": "Elige cuántos colores dominantes extraer (3–12).",
        "pt": "Escolha quantas cores dominantes extrair (3–12).",
        "id": "Pilih berapa banyak warna dominan yang diekstrak (3–12)."
    },
    "Choose output format and scale factor for high-resolution output.": {
        "es": "Elige formato de salida y factor de escala para alta resolución.",
        "pt": "Escolha o formato de saída e o fator de escala para alta resolução.",
        "id": "Pilih format output dan faktor skala untuk output resolusi tinggi."
    },
    "Choose page size, margin, and orientation.": {
        "es": "Elige tamaño de página, margen y orientación.",
        "pt": "Escolha tamanho da página, margem e orientação.",
        "id": "Pilih ukuran halaman, margin, dan orientasi."
    },
    "Click \"Compress All\" and download as ZIP.": {
        "es": 'Haz clic en "Comprimir Todo" y descarga como ZIP.',
        "pt": 'Clique em "Comprimir Tudo" e baixe como ZIP.',
        "id": 'Klik "Kompres Semua" dan unduh sebagai ZIP.'
    },
    "Click \"Convert All\" and download results.": {
        "es": 'Haz clic en "Convertir Todo" y descarga los resultados.',
        "pt": 'Clique em "Converter Tudo" e baixe os resultados.',
        "id": 'Klik "Konversi Semua" dan unduh hasilnya.'
    },
    "Click \"Convert All\" and wait for processing.": {
        "es": 'Haz clic en "Convertir Todo" y espera el procesamiento.',
        "pt": 'Clique em "Converter Tudo" e aguarde o processamento.',
        "id": 'Klik "Konversi Semua" dan tunggu pemrosesan.'
    },
    "Click \"Convert to Images\" and wait.": {
        "es": 'Haz clic en "Convertir a Imágenes" y espera.',
        "pt": 'Clique em "Converter para Imagens" e aguarde.',
        "id": 'Klik "Konversi ke Gambar" dan tunggu.'
    },
    "Click \"Convert to PDF\" and download.": {
        "es": 'Haz clic en "Convertir a PDF" y descarga.',
        "pt": 'Clique em "Converter para PDF" e baixe.',
        "id": 'Klik "Konversi ke PDF" dan unduh.'
    },
    "Click \"Download PNG\" to save your circular image.": {
        "es": 'Haz clic en "Descargar PNG" para guardar tu imagen circular.',
        "pt": 'Clique em "Baixar PNG" para salvar sua imagem circular.',
        "id": 'Klik "Unduh PNG" untuk menyimpan gambar lingkaran Anda.'
    },
    "Click \"Download\" to save the blurred image.": {
        "es": 'Haz clic en "Descargar" para guardar la imagen difuminada.',
        "pt": 'Clique em "Baixar" para salvar a imagem desfocada.',
        "id": 'Klik "Unduh" untuk menyimpan gambar yang diburamkan.'
    },
    "Click \"Extract Text\" and wait for processing.": {
        "es": 'Haz clic en "Extraer Texto" y espera el procesamiento.',
        "pt": 'Clique em "Extrair Texto" e aguarde o processamento.',
        "id": 'Klik "Ekstrak Teks" dan tunggu pemrosesan.'
    },
    "Click \"Process All\" and watch progress.": {
        "es": 'Haz clic en "Procesar Todo" y observa el progreso.',
        "pt": 'Clique em "Processar Tudo" e acompanhe o progresso.',
        "id": 'Klik "Proses Semua" dan lihat progresnya.'
    },
    "Click \"Remove Background\" and let the AI model process.": {
        "es": 'Haz clic en "Quitar Fondo" y deja que el modelo IA procese.',
        "pt": 'Clique em "Remover Fundo" e deixe o modelo IA processar.',
        "id": 'Klik "Hapus Latar Belakang" dan biarkan model AI memproses.'
    },
    "Click \"Remove EXIF\" to strip all metadata.": {
        "es": 'Haz clic en "Eliminar EXIF" para quitar todos los metadatos.',
        "pt": 'Clique em "Remover EXIF" para remover todos os metadados.',
        "id": 'Klik "Hapus EXIF" untuk menghapus semua metadata.'
    },
    "Click \"Upscale & Download\" to save the high-resolution image.": {
        "es": 'Haz clic en "Ampliar y Descargar" para guardar la imagen de alta resolución.',
        "pt": 'Clique em "Ampliar e Baixar" para salvar a imagem de alta resolução.',
        "id": 'Klik "Perbesar & Unduh" untuk menyimpan gambar resolusi tinggi.'
    },
    "Click Apply Watermark and download the protected image.": {
        "es": "Haz clic en Aplicar Marca de Agua y descarga la imagen protegida.",
        "pt": "Clique em Aplicar Marca D'água e baixe a imagem protegida.",
        "id": "Klik Terapkan Watermark dan unduh gambar yang dilindungi."
    },
    "Click Apply to process, then Download to save the result.": {
        "es": "Haz clic en Aplicar para procesar, luego en Descargar para guardar.",
        "pt": "Clique em Aplicar para processar, depois em Baixar para salvar.",
        "id": "Klik Terapkan untuk memproses, lalu Unduh untuk menyimpan."
    },
    "Click Apply to process, then Download to save.": {
        "es": "Haz clic en Aplicar para procesar, luego en Descargar para guardar.",
        "pt": "Clique em Aplicar para processar, depois em Baixar para salvar.",
        "id": "Klik Terapkan untuk memproses, lalu Unduh untuk menyimpan."
    },
    "Click Compress and download the optimized image.": {
        "es": "Haz clic en Comprimir y descarga la imagen optimizada.",
        "pt": "Clique em Comprimir e baixe a imagem otimizada.",
        "id": "Klik Kompres dan unduh gambar yang dioptimalkan."
    },
    "Click Convert and save your new file.": {
        "es": "Haz clic en Convertir y guarda tu nuevo archivo.",
        "pt": "Clique em Converter e salve seu novo arquivo.",
        "id": "Klik Konversi dan simpan file baru Anda."
    },
    "Click Crop and download the result.": {
        "es": "Haz clic en Recortar y descarga el resultado.",
        "pt": "Clique em Recortar e baixe o resultado.",
        "id": "Klik Potong dan unduh hasilnya."
    },
    "Click Download PNG for raster, Download SVG for vector.": {
        "es": "Haz clic en Descargar PNG para ráster o Descargar SVG para vector.",
        "pt": "Clique em Baixar PNG para raster ou Baixar SVG para vetor.",
        "id": "Klik Unduh PNG untuk raster atau Unduh SVG untuk vektor."
    },
    "Click Download to save the image with your text overlay.": {
        "es": "Haz clic en Descargar para guardar la imagen con tu texto superpuesto.",
        "pt": "Clique em Baixar para salvar a imagem com seu texto sobreposto.",
        "id": "Klik Unduh untuk menyimpan gambar dengan teks Anda."
    },
    "Click Download to save the rotated or flipped image.": {
        "es": "Haz clic en Descargar para guardar la imagen rotada o volteada.",
        "pt": "Clique em Baixar para salvar a imagem rotacionada ou invertida.",
        "id": "Klik Unduh untuk menyimpan gambar yang diputar atau dibalik."
    },
    "Click Download to save your beautifully framed screenshot.": {
        "es": "Haz clic en Descargar para guardar tu captura bellamente enmarcada.",
        "pt": "Clique em Baixar para salvar sua captura lindamente emoldurada.",
        "id": "Klik Unduh untuk menyimpan screenshot Anda dengan bingkai indah."
    },
    "Click Download to save your filtered image.": {
        "es": "Haz clic en Descargar para guardar tu imagen filtrada.",
        "pt": "Clique em Baixar para salvar sua imagem filtrada.",
        "id": "Klik Unduh untuk menyimpan gambar yang difilter."
    },
    "Click Extract Colors, then click any color to copy its hex code.": {
        "es": "Haz clic en Extraer Colores, luego en cualquier color para copiar su código HEX.",
        "pt": "Clique em Extrair Cores, depois em qualquer cor para copiar seu código HEX.",
        "id": "Klik Ekstrak Warna, lalu klik warna apa pun untuk menyalin kode HEX."
    },
    "Click Generate GIF. All processing happens in your browser.": {
        "es": "Haz clic en Generar GIF. Todo el procesamiento ocurre en tu navegador.",
        "pt": "Clique em Gerar GIF. Todo o processamento acontece no seu navegador.",
        "id": "Klik Hasilkan GIF. Semua pemrosesan terjadi di browser Anda."
    },
    "Click Merge & Download to save your combined image.": {
        "es": "Haz clic en Unir y Descargar para guardar tu imagen combinada.",
        "pt": "Clique em Unir e Baixar para salvar sua imagem combinada.",
        "id": "Klik Gabung & Unduh untuk menyimpan gambar gabungan Anda."
    },
    "Click Resize and download the result.": {
        "es": "Haz clic en Redimensionar y descarga el resultado.",
        "pt": "Clique em Redimensionar e baixe o resultado.",
        "id": "Klik Ubah Ukuran dan unduh hasilnya."
    },
    "Click a preset filter button to apply it instantly.": {
        "es": "Haz clic en un botón de filtro predefinido para aplicarlo al instante.",
        "pt": "Clique em um botão de filtro predefinido para aplicá-lo instantaneamente.",
        "id": "Klik tombol filter preset untuk menerapkannya secara instan."
    },
    "Click each upload area to add Image A and Image B.": {
        "es": "Haz clic en cada área de carga para añadir Imagen A e Imagen B.",
        "pt": "Clique em cada área de upload para adicionar Imagem A e Imagem B.",
        "id": "Klik setiap area unggah untuk menambahkan Gambar A dan Gambar B."
    },
    "Click the upload area or drag and drop your image file.": {
        "es": "Haz clic en el área de carga o arrastra y suelta tu archivo de imagen.",
        "pt": "Clique na área de upload ou arraste e solte seu arquivo de imagem.",
        "id": "Klik area unggah atau seret dan lepas file gambar Anda."
    },
    "Click the upload area or drag and drop your screenshot file.": {
        "es": "Haz clic en el área de carga o arrastra y suelta tu archivo de captura.",
        "pt": "Clique na área de upload ou arraste e solte seu arquivo de captura.",
        "id": "Klik area unggah atau seret dan lepas file screenshot Anda."
    },
    "Click upload area or drag and drop your .avif file.": {
        "es": "Haz clic en el área de carga o arrastra y suelta tu archivo .avif.",
        "pt": "Clique na área de upload ou arraste e solte seu arquivo .avif.",
        "id": "Klik area unggah atau seret dan lepas file .avif Anda."
    },
    "Copy the HTML snippet into your site's &lt;head&gt;.": {
        "es": "Copia el fragmento HTML en el &lt;head&gt; de tu sitio.",
        "pt": "Copie o trecho HTML no &lt;head&gt; do seu site.",
        "id": "Salin potongan HTML ke &lt;head&gt; situs Anda."
    },
    "Copy the output or download it directly.": {
        "es": "Copia el resultado o descárgalo directamente.",
        "pt": "Copie o resultado ou baixe-o diretamente.",
        "id": "Salin output atau unduh langsung."
    },
    "Copy the text to clipboard, or download as TXT.": {
        "es": "Copia el texto al portapapeles o descarga como TXT.",
        "pt": "Copie o texto para a área de transferência ou baixe como TXT.",
        "id": "Salin teks ke clipboard atau unduh sebagai TXT."
    },
    "Download a single .ico file or a full ZIP pack.": {
        "es": "Descarga un solo archivo .ico o un paquete ZIP completo.",
        "pt": "Baixe um único arquivo .ico ou um pacote ZIP completo.",
        "id": "Unduh satu file .ico atau paket ZIP lengkap."
    },
    "Download individual files or all as a ZIP.": {
        "es": "Descarga archivos individuales o todo como ZIP.",
        "pt": "Baixe arquivos individuais ou todos como ZIP.",
        "id": "Unduh file individual atau semua sebagai ZIP."
    },
    "Download individual pages or all as a ZIP.": {
        "es": "Descarga páginas individuales o todas como ZIP.",
        "pt": "Baixe páginas individuais ou todas como ZIP.",
        "id": "Unduh halaman individual atau semua sebagai ZIP."
    },
    "Download pieces individually or all as a ZIP.": {
        "es": "Descarga las piezas individualmente o todas como ZIP.",
        "pt": "Baixe as partes individualmente ou todas como ZIP.",
        "id": "Unduh potongan secara individual atau semua sebagai ZIP."
    },
    "Download the clean image with no hidden data.": {
        "es": "Descarga la imagen limpia sin datos ocultos.",
        "pt": "Baixe a imagem limpa sem dados ocultos.",
        "id": "Unduh gambar bersih tanpa data tersembunyi."
    },
    "Download the converted image.": {
        "es": "Descarga la imagen convertida.",
        "pt": "Baixe a imagem convertida.",
        "id": "Unduh gambar yang dikonversi."
    },
    "Drag and drop multiple images in any order.": {
        "es": "Arrastra y suelta varias imágenes en cualquier orden.",
        "pt": "Arraste e solte várias imagens em qualquer ordem.",
        "id": "Seret dan lepas beberapa gambar dalam urutan apa pun."
    },
    "Drag and drop one or more .HEIC files from your iPhone.": {
        "es": "Arrastra y suelta uno o más archivos .HEIC de tu iPhone.",
        "pt": "Arraste e solte um ou mais arquivos .HEIC do seu iPhone.",
        "id": "Seret dan lepas satu atau lebih file .HEIC dari iPhone Anda."
    },
    "Drag and drop one or more .HEIC files.": {
        "es": "Arrastra y suelta uno o más archivos .HEIC.",
        "pt": "Arraste e solte um ou mais arquivos .HEIC.",
        "id": "Seret dan lepas satu atau lebih file .HEIC."
    },
    "Drag and drop or click to select an image (JPG, PNG, WebP, BMP).": {
        "es": "Arrastra y suelta o haz clic para seleccionar una imagen (JPG, PNG, WebP, BMP).",
        "pt": "Arraste e solte ou clique para selecionar uma imagem (JPG, PNG, WebP, BMP).",
        "id": "Seret dan lepas atau klik untuk memilih gambar (JPG, PNG, WebP, BMP)."
    },
    "Drag and drop or click to select an image.": {
        "es": "Arrastra y suelta o haz clic para seleccionar una imagen.",
        "pt": "Arraste e solte ou clique para selecionar uma imagem.",
        "id": "Seret dan lepas atau klik untuk memilih gambar."
    },
    "Drag and drop or select multiple image files.": {
        "es": "Arrastra y suelta o selecciona varios archivos de imagen.",
        "pt": "Arraste e solte ou selecione vários arquivos de imagem.",
        "id": "Seret dan lepas atau pilih beberapa file gambar."
    },
    "Drag items in the list to change the page order.": {
        "es": "Arrastra elementos en la lista para cambiar el orden de las páginas.",
        "pt": "Arraste itens na lista para alterar a ordem das páginas.",
        "id": "Seret item di daftar untuk mengubah urutan halaman."
    },
    "Drag text on the canvas to position it. Adjust shadow, outline, opacity, and rotation.": {
        "es": "Arrastra el texto en el lienzo para posicionarlo. Ajusta sombra, contorno, opacidad y rotación.",
        "pt": "Arraste o texto no canvas para posicioná-lo. Ajuste sombra, contorno, opacidade e rotação.",
        "id": "Seret teks di kanvas untuk memposisikannya. Sesuaikan bayangan, outline, opasitas, dan rotasi."
    },
    "Drag the overlay to move, or use handles to resize. Pick an aspect ratio preset if needed.": {
        "es": "Arrastra la superposición para mover, o usa los controles para redimensionar. Elige una proporción predefinida si es necesario.",
        "pt": "Arraste a sobreposição para mover ou use as alças para redimensionar. Escolha uma proporção predefinida se necessário.",
        "id": "Seret overlay untuk memindahkan, atau gunakan handle untuk mengubah ukuran. Pilih preset rasio aspek jika perlu."
    },
    "Drag the slider or adjust overlay opacity to compare.": {
        "es": "Arrastra el deslizador o ajusta la opacidad de superposición para comparar.",
        "pt": "Arraste o controle ou ajuste a opacidade da sobreposição para comparar.",
        "id": "Seret slider atau sesuaikan opasitas overlay untuk membandingkan."
    },
    "Drop a square image (PNG with transparency works best).": {
        "es": "Suelta una imagen cuadrada (PNG con transparencia funciona mejor).",
        "pt": "Solte uma imagem quadrada (PNG com transparência funciona melhor).",
        "id": "Lepaskan gambar persegi (PNG dengan transparansi paling cocok)."
    },
    "Drop a square image (any common format).": {
        "es": "Suelta una imagen cuadrada (cualquier formato común).",
        "pt": "Solte uma imagem quadrada (qualquer formato comum).",
        "id": "Lepaskan gambar persegi (format umum apa pun)."
    },
    "Drop an SVG file or paste SVG code directly.": {
        "es": "Suelta un archivo SVG o pega código SVG directamente.",
        "pt": "Solte um arquivo SVG ou cole código SVG diretamente.",
        "id": "Lepaskan file SVG atau tempel kode SVG langsung."
    },
    "Drop an image containing text — photo, scan, screenshot.": {
        "es": "Suelta una imagen que contenga texto — foto, escaneo, captura.",
        "pt": "Solte uma imagem contendo texto — foto, digitalização, captura.",
        "id": "Lepaskan gambar berisi teks — foto, scan, screenshot."
    },
    "Drop multiple image files or select a folder.": {
        "es": "Suelta varios archivos de imagen o selecciona una carpeta.",
        "pt": "Solte vários arquivos de imagem ou selecione uma pasta.",
        "id": "Lepaskan beberapa file gambar atau pilih folder."
    },
    "Enter text in the sidebar. Choose font, size, color, and style.": {
        "es": "Introduce texto en la barra lateral. Elige fuente, tamaño, color y estilo.",
        "pt": "Digite o texto na barra lateral. Escolha fonte, tamanho, cor e estilo.",
        "id": "Masukkan teks di sidebar. Pilih font, ukuran, warna, dan gaya."
    },
    "Enter text or upload a logo. Adjust color, size, opacity, and position.": {
        "es": "Introduce texto o sube un logo. Ajusta color, tamaño, opacidad y posición.",
        "pt": "Digite texto ou envie um logo. Ajuste cor, tamanho, opacidade e posição.",
        "id": "Masukkan teks atau unggah logo. Sesuaikan warna, ukuran, opasitas, dan posisi."
    },
    "Enter width and height in pixels, or use the percentage slider.": {
        "es": "Introduce ancho y alto en píxeles, o usa el control de porcentaje.",
        "pt": "Insira largura e altura em pixels ou use o controle de porcentagem.",
        "id": "Masukkan lebar dan tinggi dalam piksel, atau gunakan slider persentase."
    },
    "Expand \"Processing Options\" to set resize, format, quality, and watermark.": {
        "es": 'Expande "Opciones de Procesamiento" para configurar tamaño, formato, calidad y marca de agua.',
        "pt": 'Expanda "Opções de Processamento" para definir tamanho, formato, qualidade e marca d\'água.',
        "id": 'Perluas "Opsi Pemrosesan" untuk mengatur ukuran, format, kualitas, dan watermark.'
    },
    "Get all favicon files, HTML snippet, and manifest.json in one ZIP.": {
        "es": "Obtén todos los archivos favicon, fragmento HTML y manifest.json en un ZIP.",
        "pt": "Obtenha todos os arquivos favicon, trecho HTML e manifest.json em um ZIP.",
        "id": "Dapatkan semua file favicon, potongan HTML, dan manifest.json dalam satu ZIP."
    },
    "Optionally remove metadata and download clean image.": {
        "es": "Opcionalmente elimina metadatos y descarga la imagen limpia.",
        "pt": "Opcionalmente remova metadados e baixe a imagem limpa.",
        "id": "Opsional hapus metadata dan unduh gambar bersih."
    },
    "Optionally resize images to a max width.": {
        "es": "Opcionalmente redimensiona imágenes a un ancho máximo.",
        "pt": "Opcionalmente redimensione imagens para uma largura máxima.",
        "id": "Opsional ubah ukuran gambar ke lebar maksimum."
    },
    "Pick 2×2, 3×3, or other grid sizes.": {
        "es": "Elige cuadrícula 2×2, 3×3 u otros tamaños.",
        "pt": "Escolha grade 2×2, 3×3 ou outros tamanhos.",
        "id": "Pilih grid 2×2, 3×3, atau ukuran lainnya."
    },
    "Pick Grid Collage, Horizontal Merge, or Vertical Merge.": {
        "es": "Elige Collage en Cuadrícula, Unión Horizontal o Unión Vertical.",
        "pt": "Escolha Colagem em Grade, União Horizontal ou União Vertical.",
        "id": "Pilih Kolase Grid, Gabung Horizontal, atau Gabung Vertikal."
    },
    "Pick a famous meme template or upload your own image.": {
        "es": "Elige una plantilla de meme famosa o sube tu propia imagen.",
        "pt": "Escolha um modelo de meme famoso ou envie sua própria imagem.",
        "id": "Pilih template meme terkenal atau unggah gambar sendiri."
    },
    "Pick grayscale, sepia, invert, or other effects.": {
        "es": "Elige escala de grises, sepia, invertir u otros efectos.",
        "pt": "Escolha escala de cinza, sépia, inverter ou outros efeitos.",
        "id": "Pilih grayscale, sepia, invert, atau efek lainnya."
    },
    "Pick the output format from the dropdown.": {
        "es": "Elige el formato de salida del menú desplegable.",
        "pt": "Escolha o formato de saída no menu suspenso.",
        "id": "Pilih format output dari dropdown."
    },
    "Pick transparent (best for avatars), solid color, or pick a custom color.": {
        "es": "Elige transparente (ideal para avatares), color sólido o color personalizado.",
        "pt": "Escolha transparente (melhor para avatares), cor sólida ou cor personalizada.",
        "id": "Pilih transparan (terbaik untuk avatar), warna solid, atau warna kustom."
    },
    "Preview and download your GIF.": {
        "es": "Previsualiza y descarga tu GIF.",
        "pt": "Pré-visualize e baixe seu GIF.",
        "id": "Pratinjau dan unduh GIF Anda."
    },
    "Save the comparison as a single combined image.": {
        "es": "Guarda la comparación como una sola imagen combinada.",
        "pt": "Salve a comparação como uma única imagem combinada.",
        "id": "Simpan perbandingan sebagai satu gambar gabungan."
    },
    "Save your PNG, JPG, or WebP file.": {
        "es": "Guarda tu archivo PNG, JPG o WebP.",
        "pt": "Salve seu arquivo PNG, JPG ou WebP.",
        "id": "Simpan file PNG, JPG, atau WebP Anda."
    },
    "Save your meme as PNG, JPG, or WebP.": {
        "es": "Guarda tu meme como PNG, JPG o WebP.",
        "pt": "Salve seu meme como PNG, JPG ou WebP.",
        "id": "Simpan meme Anda sebagai PNG, JPG, atau WebP."
    },
    "Save your print-ready image.": {
        "es": "Guarda tu imagen lista para imprimir.",
        "pt": "Salve sua imagem pronta para impressão.",
        "id": "Simpan gambar siap cetak Anda."
    },
    "Save your transparent PNG with one click.": {
        "es": "Guarda tu PNG transparente con un clic.",
        "pt": "Salve seu PNG transparente com um clique.",
        "id": "Simpan PNG transparan Anda dengan satu klik."
    },
    "See all generated sizes in the browser preview.": {
        "es": "Ve todos los tamaños generados en la vista previa del navegador.",
        "pt": "Veja todos os tamanhos gerados na pré-visualização do navegador.",
        "id": "Lihat semua ukuran yang dihasilkan di pratinjau browser."
    },
    "See the result instantly. The preview updates in real-time as you adjust.": {
        "es": "Ve el resultado al instante. La vista previa se actualiza en tiempo real mientras ajustas.",
        "pt": "Veja o resultado instantaneamente. A pré-visualização atualiza em tempo real conforme você ajusta.",
        "id": "Lihat hasilnya langsung. Pratinjau diperbarui real-time saat Anda menyesuaikan."
    },
    "See the upscaled result with dimensions displayed for comparison.": {
        "es": "Ve el resultado ampliado con las dimensiones mostradas para comparar.",
        "pt": "Veja o resultado ampliado com as dimensões exibidas para comparação.",
        "id": "Lihat hasil yang diperbesar dengan dimensi ditampilkan untuk perbandingan."
    },
    "Select 2x, 3x, or 4x enlargement. Adjust sharpening if needed.": {
        "es": "Selecciona ampliación 2x, 3x o 4x. Ajusta la nitidez si es necesario.",
        "pt": "Selecione ampliação 2x, 3x ou 4x. Ajuste a nitidez se necessário.",
        "id": "Pilih pembesaran 2x, 3x, atau 4x. Sesuaikan ketajaman jika perlu."
    },
    "Select JPG (smaller) or PNG (lossless), and quality.": {
        "es": "Selecciona JPG (más pequeño) o PNG (sin pérdida), y calidad.",
        "pt": "Selecione JPG (menor) ou PNG (sem perda), e qualidade.",
        "id": "Pilih JPG (lebih kecil) atau PNG (lossless), dan kualitas."
    },
    "Select JPG, PNG, or WebP as output.": {
        "es": "Selecciona JPG, PNG o WebP como salida.",
        "pt": "Selecione JPG, PNG ou WebP como saída.",
        "id": "Pilih JPG, PNG, atau WebP sebagai output."
    },
    "Select JPG, PNG, or WebP output format.": {
        "es": "Selecciona formato de salida JPG, PNG o WebP.",
        "pt": "Selecione o formato de saída JPG, PNG ou WebP.",
        "id": "Pilih format output JPG, PNG, atau WebP."
    },
    "Select a JPG, PNG, or WebP image from your device.": {
        "es": "Selecciona una imagen JPG, PNG o WebP de tu dispositivo.",
        "pt": "Selecione uma imagem JPG, PNG ou WebP do seu dispositivo.",
        "id": "Pilih gambar JPG, PNG, atau WebP dari perangkat Anda."
    },
    "Select a PDF file from your device.": {
        "es": "Selecciona un archivo PDF de tu dispositivo.",
        "pt": "Selecione um arquivo PDF do seu dispositivo.",
        "id": "Pilih file PDF dari perangkat Anda."
    },
    "Select a background gradient, browser frame, or device mockup style.": {
        "es": "Selecciona un degradado de fondo, marco de navegador o estilo de mockup.",
        "pt": "Selecione um gradiente de fundo, moldura de navegador ou estilo de mockup.",
        "id": "Pilih gradien latar, bingkai browser, atau gaya mockup perangkat."
    },
    "Select a preset or enter custom dimensions.": {
        "es": "Selecciona un predefinido o introduce dimensiones personalizadas.",
        "pt": "Selecione um predefinido ou insira dimensões personalizadas.",
        "id": "Pilih preset atau masukkan dimensi kustom."
    },
    "Select an image from your device or try with a sample image.": {
        "es": "Selecciona una imagen de tu dispositivo o prueba con una imagen de muestra.",
        "pt": "Selecione uma imagem do seu dispositivo ou teste com uma imagem de exemplo.",
        "id": "Pilih gambar dari perangkat Anda atau coba dengan gambar contoh."
    },
    "Select an image from your device or try with a sample.": {
        "es": "Selecciona una imagen de tu dispositivo o prueba con una muestra.",
        "pt": "Selecione uma imagem do seu dispositivo ou teste com uma amostra.",
        "id": "Pilih gambar dari perangkat Anda atau coba dengan sampel."
    },
    "Select an image from your device.": {
        "es": "Selecciona una imagen de tu dispositivo.",
        "pt": "Selecione uma imagem do seu dispositivo.",
        "id": "Pilih gambar dari perangkat Anda."
    },
    "Select an image to analyze.": {
        "es": "Selecciona una imagen para analizar.",
        "pt": "Selecione uma imagem para analisar.",
        "id": "Pilih gambar untuk dianalisis."
    },
    "Select multiple images in the order you want them to appear.": {
        "es": "Selecciona varias imágenes en el orden en que quieres que aparezcan.",
        "pt": "Selecione várias imagens na ordem em que deseja que apareçam.",
        "id": "Pilih beberapa gambar dalam urutan yang Anda inginkan."
    },
    "Select multiple images or drag and drop them into the upload area.": {
        "es": "Selecciona varias imágenes o arrástralas y suéltalas en el área de carga.",
        "pt": "Selecione várias imagens ou arraste e solte na área de upload.",
        "id": "Pilih beberapa gambar atau seret dan lepas ke area unggah."
    },
    "Select output format, DPI, and page range.": {
        "es": "Selecciona formato de salida, DPI y rango de páginas.",
        "pt": "Selecione formato de saída, DPI e intervalo de páginas.",
        "id": "Pilih format output, DPI, dan rentang halaman."
    },
    "Select the image you want to convert.": {
        "es": "Selecciona la imagen que quieres convertir.",
        "pt": "Selecione a imagem que deseja converter.",
        "id": "Pilih gambar yang ingin Anda konversi."
    },
    "Select the image you want to crop.": {
        "es": "Selecciona la imagen que quieres recortar.",
        "pt": "Selecione a imagem que deseja recortar.",
        "id": "Pilih gambar yang ingin Anda potong."
    },
    "Select the image you want to resize.": {
        "es": "Selecciona la imagen que quieres redimensionar.",
        "pt": "Selecione a imagem que deseja redimensionar.",
        "id": "Pilih gambar yang ingin Anda ubah ukurannya."
    },
    "Select the image you want to watermark.": {
        "es": "Selecciona la imagen que quieres proteger con marca de agua.",
        "pt": "Selecione a imagem que deseja proteger com marca d'água.",
        "id": "Pilih gambar yang ingin Anda beri watermark."
    },
    "Select the text language (auto-detect available for some).": {
        "es": "Selecciona el idioma del texto (detección automática disponible para algunos).",
        "pt": "Selecione o idioma do texto (detecção automática disponível para alguns).",
        "id": "Pilih bahasa teks (deteksi otomatis tersedia untuk beberapa)."
    },
    "Set blur strength and preview the result.": {
        "es": "Establece la fuerza de difuminado y previsualiza el resultado.",
        "pt": "Defina a força do desfoque e pré-visualize o resultado.",
        "id": "Atur kekuatan blur dan pratinjau hasilnya."
    },
    "Set foreground and background colors, error correction, and output size.": {
        "es": "Establece colores de primer plano y fondo, corrección de errores y tamaño de salida.",
        "pt": "Defina cores de primeiro plano e fundo, correção de erros e tamanho de saída.",
        "id": "Atur warna foreground dan background, koreksi error, dan ukuran output."
    },
    "Set frame delay, resize, and quality.": {
        "es": "Establece retardo de fotograma, redimensionar y calidad.",
        "pt": "Defina atraso do quadro, redimensionar e qualidade.",
        "id": "Atur jeda frame, ubah ukuran, dan kualitas."
    },
    "Set offset, blur radius, and shadow color.": {
        "es": "Establece desplazamiento, radio de desenfoque y color de sombra.",
        "pt": "Defina deslocamento, raio de desfoque e cor da sombra.",
        "id": "Atur offset, radius blur, dan warna bayangan."
    },
    "Set the quality level (10-100%).": {
        "es": "Establece el nivel de calidad (10-100%).",
        "pt": "Defina o nível de qualidade (10-100%).",
        "id": "Atur level kualitas (10-100%)."
    },
    "Slider, Side-by-Side, or Overlay — pick what works best.": {
        "es": "Deslizador, Lado a Lado o Superposición — elige lo que mejor funcione.",
        "pt": "Controle deslizante, Lado a Lado ou Sobreposição — escolha o que funciona melhor.",
        "id": "Slider, Berdampingan, atau Overlay — pilih yang paling cocok."
    },
    "Switch between Encode (image→text) or Decode (text→image).": {
        "es": "Cambia entre Codificar (imagen→texto) o Decodificar (texto→imagen).",
        "pt": "Alterne entre Codificar (imagem→texto) ou Decodificar (texto→imagem).",
        "id": "Beralih antara Encode (gambar→teks) atau Decode (teks→gambar)."
    },
    "The SVG is rasterized instantly in your browser.": {
        "es": "El SVG se rasteriza al instante en tu navegador.",
        "pt": "O SVG é rasterizado instantaneamente no seu navegador.",
        "id": "SVG dirasterisasi langsung di browser Anda."
    },
    "Toggle chips to select exactly which sizes you want.": {
        "es": "Activa los botones para seleccionar exactamente qué tamaños quieres.",
        "pt": "Ative os botões para selecionar exatamente quais tamanhos você quer.",
        "id": "Aktifkan chip untuk memilih ukuran yang Anda inginkan."
    },
    "Type top and bottom text. Adjust font size and outline.": {
        "es": "Escribe el texto superior e inferior. Ajusta el tamaño de fuente y contorno.",
        "pt": "Digite o texto superior e inferior. Ajuste o tamanho da fonte e contorno.",
        "id": "Ketik teks atas dan bawah. Sesuaikan ukuran font dan outline."
    },
    "Upload an image or paste a Base64 string.": {
        "es": "Sube una imagen o pega una cadena Base64.",
        "pt": "Envie uma imagem ou cole uma string Base64.",
        "id": "Unggah gambar atau tempel string Base64."
    },
    "Use quick rotation buttons (90° left/right), custom angle slider, or flip buttons.": {
        "es": "Usa botones de rotación rápida (90° izq/der), control de ángulo personalizado o botones de volteo.",
        "pt": "Use botões de rotação rápida (90° esq/dir), controle de ângulo personalizado ou botões de inversão.",
        "id": "Gunakan tombol rotasi cepat (90° kiri/kanan), slider sudut kustom, atau tombol balik."
    },
    "Use the size and offset sliders to position the circle exactly where you want.": {
        "es": "Usa los controles de tamaño y desplazamiento para posicionar el círculo exactamente donde quieres.",
        "pt": "Use os controles de tamanho e deslocamento para posicionar o círculo exatamente onde deseja.",
        "id": "Gunakan slider ukuran dan offset untuk memposisikan lingkaran tepat di tempat yang diinginkan."
    },
    "Use the slider to balance file size and image quality.": {
        "es": "Usa el deslizador para equilibrar tamaño de archivo y calidad de imagen.",
        "pt": "Use o controle para equilibrar tamanho do arquivo e qualidade da imagem.",
        "id": "Gunakan slider untuk menyeimbangkan ukuran file dan kualitas gambar."
    },
    "Use the sliders to adjust brightness, contrast, and saturation.": {
        "es": "Usa los deslizadores para ajustar brillo, contraste y saturación.",
        "pt": "Use os controles para ajustar brilho, contraste e saturação.",
        "id": "Gunakan slider untuk menyesuaikan kecerahan, kontras, dan saturasi."
    },
    "Use the sliders to adjust brightness, contrast, saturation, blur, and hue rotate.": {
        "es": "Usa los deslizadores para ajustar brillo, contraste, saturación, desenfoque y rotación de tono.",
        "pt": "Use os controles para ajustar brilho, contraste, saturação, desfoque e rotação de matiz.",
        "id": "Gunakan slider untuk menyesuaikan kecerahan, kontras, saturasi, blur, dan rotasi hue."
    },
    "View your browser's AVIF support status.": {
        "es": "Ve el estado de compatibilidad AVIF de tu navegador.",
        "pt": "Veja o status de suporte AVIF do seu navegador.",
        "id": "Lihat status dukungan AVIF browser Anda."
    },
    "When done, download all processed images as a ZIP.": {
        "es": "Al terminar, descarga todas las imágenes procesadas como ZIP.",
        "pt": "Ao terminar, baixe todas as imagens processadas como ZIP.",
        "id": "Setelah selesai, unduh semua gambar yang diproses sebagai ZIP."
    },
}

HOWTO_P = _raw_howto_ps.copy()

# Import GUIDE_P from external file (156 unique guide paragraph translations)
try:
    from _guide_p_translations import GUIDE_P
except ImportError:
    GUIDE_P = {}
    print("WARNING: _guide_p_translations.py not found, guide p tags will not be translated")

# We also need to handle any remaining untranslated p descriptions.
# For those, we'll do a simple word-for-word translation fallback.


def translate_howto_h4(en_text, lang):
    """Translate a howto h4 title."""
    if en_text in HOWTO_H4:
        return HOWTO_H4[en_text].get(lang, en_text)
    return en_text


def translate_howto_p(en_text, lang):
    """Translate a howto p description."""
    if en_text in HOWTO_P:
        return HOWTO_P[en_text].get(lang, en_text)
    return en_text


def translate_guide_h3(en_text, lang):
    """Translate a guide h3 title."""
    # First check exact match in GUIDE_H3
    if en_text in GUIDE_H3:
        return GUIDE_H3[en_text].get(lang, en_text)
    
    # Try Step N: pattern
    m = re.match(r'^(Step \d+): (.+)$', en_text)
    if m:
        step_num = m.group(1)
        detail = m.group(2)
        step_prefix = STEP_PREFIXES.get(lang, {}).get("Step", "Step")
        translated_step = step_num.replace("Step", step_prefix)
        if detail in STEP_PREFIXES.get(lang, {}):
            return f"{translated_step}: {STEP_PREFIXES[lang][detail]}"
        # Try translating the detail via HOWTO_H4
        if detail in HOWTO_H4:
            return f"{translated_step}: {HOWTO_H4[detail].get(lang, detail)}"
        return en_text
    
    return en_text


def translate_guide_p(en_text, lang):
    """Translate a guide p description using GUIDE_P map first, then HOWTO_P."""
    if en_text in GUIDE_P:
        return GUIDE_P[en_text].get(lang, en_text)
    if en_text in HOWTO_P:
        return HOWTO_P[en_text].get(lang, en_text)
    return en_text


def process_language(lang):
    """Translate howto_html and guide_html for one language."""
    filepath = f'_tools_data_{lang}.json'
    print(f'\nProcessing howto/guide for {filepath}...')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    howto_updated = 0
    guide_updated = 0
    howto_missing_h4 = set()
    howto_missing_p = set()
    guide_missing_h3 = set()
    guide_missing_p = set()
    
    for tool in data['tools']:
        # Process howto_html
        howto = tool.get('howto_html', '')
        if howto:
            original = howto
            
            # Translate h4 titles
            def replace_h4(m):
                en = m.group(1)
                translated = translate_howto_h4(en, lang)
                if translated == en:
                    howto_missing_h4.add(en)
                return f'<h4>{translated}</h4>'
            howto = re.sub(r'<h4>(.*?)</h4>', replace_h4, howto)
            
            # Translate p descriptions
            def replace_p(m):
                en = m.group(1)
                translated = translate_howto_p(en, lang)
                if translated == en:
                    howto_missing_p.add(en)
                return f'<p>{translated}</p>'
            howto = re.sub(r'<p>(.*?)</p>', replace_p, howto)
            
            if howto != original:
                tool['howto_html'] = howto
                howto_updated += 1
        
        # Process guide_html
        guide = tool.get('guide_html', '')
        if guide:
            original = guide
            
            # Translate h3 titles
            def replace_h3(m):
                en = m.group(1)
                translated = translate_guide_h3(en, lang)
                if translated == en:
                    guide_missing_h3.add(en)
                return f'<h3>{translated}</h3>'
            guide = re.sub(r'<h3>(.*?)</h3>', replace_h3, guide)
            
            # Translate p descriptions
            def replace_p2(m):
                en = m.group(1)
                translated = translate_guide_p(en, lang)
                if translated == en:
                    guide_missing_p.add(en)
                return f'<p>{translated}</p>'
            guide = re.sub(r'<p>(.*?)</p>', replace_p2, guide)
            
            # Also translate <li> items
            def replace_li(m):
                en = m.group(1)
                # Check common patterns
                patterns = {
                    "Chrome 85+ — Full support": "Chrome 85+ — Compatibilidad total",
                    "Firefox 93+ — Full support": "Firefox 93+ — Compatibilidad total",
                    "Safari 16.4+ — Full support": "Safari 16.4+ — Compatibilidad total",
                }
                if lang == 'es' and en in patterns:
                    return f'<li>{patterns[en]}</li>'
                return m.group(0)
            guide = re.sub(r'<li>(.*?)</li>', replace_li, guide)
            
            if guide != original:
                tool['guide_html'] = guide
                guide_updated += 1
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'  howto updated: {howto_updated}/{len(data["tools"])}')
    print(f'  guide updated: {guide_updated}/{len(data["tools"])}')
    if howto_missing_h4:
        print(f'  ⚠️ Missing howto h4 translations ({len(howto_missing_h4)}):')
        for h in sorted(howto_missing_h4):
            print(f'    - {h}')
    if howto_missing_p:
        print(f'  ⚠️ Missing howto p translations ({len(howto_missing_p)}):')
        for p in sorted(howto_missing_p):
            print(f'    - {p[:80]}...')
    if guide_missing_h3:
        print(f'  ⚠️ Missing guide h3 translations ({len(guide_missing_h3)}):')
        for h in sorted(guide_missing_h3):
            print(f'    - {h}')
    if guide_missing_p:
        print(f'  ⚠️ Missing guide p translations ({len(guide_missing_p)}):')
        for p in sorted(guide_missing_p):
            print(f'    - {p[:80]}...')


if __name__ == '__main__':
    for lang in ['es', 'pt', 'id']:
        process_language(lang)
    
    print('\n✅ Howto/guide translation complete!')
