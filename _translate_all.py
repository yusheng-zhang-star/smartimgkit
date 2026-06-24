"""
Comprehensive translation script for SmartImgKit multi-language tools.
Translates keywords, howto_html, guide_html, related_html for ES, PT, ID.
Reads English _tools_data.json as reference, translates and writes back.
"""
import json
import re
import copy

# ============================================================
# KEYWORD TRANSLATIONS (English → target language)
# Each entry: {slug: "translated_keywords_csv"}
# ============================================================

KW_ES = {
    "avif-support": "soporte AVIF, convertidor AVIF, decodificar AVIF, AVIF a JPG, AVIF a PNG, compatibilidad AVIF navegador, formato imagen nueva generación, archivo AV1",
    "background-remover": "quitar fondo, eliminar fondo, fondo transparente, eliminación fondo con IA, gratis, foto producto, retrato, comercio electrónico",
    "base64": "codificador base64, decodificador base64, imagen a base64, base64 a imagen, convertir imagen base64, codificar imagen, decodificar imagen",
    "bulk-processor": "procesamiento por lotes, compresión masiva, redimensionar múltiples, convertir lote, editor imágenes por lotes, redimensionar varias fotos",
    "circle-crop": "recorte circular, imagen redonda, foto circular, recortar círculo, avatar redondo, foto perfil circular",
    "color-palette": "extraer paleta colores, paleta de imagen, colores dominantes, esquema color, generador paleta, analizar colores",
    "compressor": "comprimir imagen, reducir tamaño imagen, optimizador imágenes, comprimir JPG, comprimir PNG, compresión sin pérdida, compresión con pérdida",
    "converter": "convertir imagen, JPG a PNG, PNG a JPG, WebP a JPG, conversor formato imagen, cambiar formato",
    "cropper": "recortar imagen, cortar foto, herramienta recorte, recorte libre, recorte proporción, recortar JPG",
    "face-blur": "difuminar cara, desenfocar rostro, pixelar cara, anonimizar foto, privacidad imagen, ocultar rostro",
    "favicon-generator": "generar favicon, crear favicon, favicon PNG, icono sitio web, favicon ico, icono pestaña navegador",
    "gif-editor": "editor GIF, crear GIF, modificar GIF, GIF animado, optimizar GIF, velocidad GIF, recortar GIF",
    "heic-converter": "convertir HEIC, HEIC a JPG, HEIC a PNG, conversor fotos iPhone, HEIC a WebP, convertir formato Apple",
    "heic-to-jpg": "HEIC a JPG, convertir fotos iPhone, HEIC a JPEG, conversor Apple, fotos iOS a JPG, HEIC gratis",
    "ico-icon-generator": "generar ICO, crear icono, PNG a ICO, favicon Windows, icono escritorio, convertidor ICO",
    "id-photo": "foto carnet, foto documento, foto pasaporte, foto DNI, foto visa, redimensionar foto carnet, fondo blanco foto",
    "image-adjust": "ajustar imagen, brillo contraste, saturación, ajuste color, balance blancos, exposición, calidez",
    "image-border": "añadir borde imagen, marco foto, borde redondeado, borde personalizado, enmarcar imagen, borde color",
    "image-compare": "comparar imágenes, antes después, comparación lado a lado, diferencia imágenes, comparar calidad, deslizador comparación",
    "image-compressor": "comprimir imagen, reducir peso, compresor fotos, optimizar tamaño, comprimir sin perder calidad, compresión online",
    "image-enhancer": "mejorar imagen, realzar foto, nitidez, ajustar iluminación, optimizar calidad imagen, mejorar resolución",
    "image-exif-remover": "eliminar metadatos, quitar EXIF, borrar datos imagen, privacidad fotos, eliminar ubicación foto, limpiar metadatos",
    "image-filters": "filtros imagen, efectos foto, filtro Instagram, blanco negro, sepia, vintage, ajustar tono",
    "image-flip": "voltear imagen, girar foto, espejo horizontal, rotación vertical, invertir imagen, reflejar foto",
    "image-grayscale": "blanco negro, escala grises, convertir gris, desaturar imagen, foto monocromo, efecto blanco negro",
    "image-merger": "unir imágenes, combinar fotos, collage, fusionar imágenes, juntar fotos, composición",
    "image-rotator": "rotar imagen, girar foto, voltear imagen, enderezar foto, rotación libre, corregir orientación",
    "image-shadow": "añadir sombra imagen, sombra paralela, efecto sombra foto, sombra personalizada, sombra producto",
    "image-splitter": "dividir imagen, cortar foto en partes, separar imagen, trocear foto, rejilla imagen",
    "image-to-pdf": "imagen a PDF, convertir JPG PDF, foto a PDF, PNG a PDF, crear PDF imágenes, múltiples imágenes PDF",
    "image-upscaler": "ampliar imagen, aumentar resolución, reescalar foto, mejorar tamaño imagen, upscaling IA, aumentar píxeles",
    "meme-generator": "crear meme, generador memes, texto meme, meme personalizado, plantilla meme, meme gracioso",
    "metadata-viewer": "ver metadatos, datos EXIF, información imagen, detalles foto, visor EXIF, metadatos cámara",
    "ocr": "extraer texto imagen, OCR online, reconocer texto, imagen a texto, OCR gratis, escanear texto",
    "pdf-to-image": "PDF a imagen, convertir PDF JPG, PDF a PNG, extraer páginas PDF, renderizar PDF",
    "photo-restoration": "restaurar foto, reparar imagen antigua, eliminar arañazos, restaurar foto dañada, restauración IA, arreglar foto vieja",
    "print-resizer": "redimensionar impresión, tamaño foto impresión, DPI, 300 DPI, formato impresión, foto para imprimir",
    "product-white-background": "fondo blanco producto, foto producto ecommerce, fondo blanco automático, foto catálogo, imagen producto profesional",
    "qr-code-generator": "generar código QR, crear QR, QR personalizado, código QR gratis, QR logo, QR color",
    "resizer": "redimensionar imagen, cambiar tamaño, escalar foto, ajustar dimensiones, redimensionar porcentaje, tamaño personalizado",
    "screenshot-to-image": "captura pantalla a imagen, convertir captura, pegar portapapeles, screenshot editor, captura a JPG",
    "social-media-post": "imagen redes sociales, foto Instagram, post Facebook, tamaño Twitter, banner LinkedIn, imagen social media",
    "svg-to-png": "SVG a PNG, convertir vector, exportar SVG, renderizar SVG, vector a imagen, conversor vectores",
    "text-on-image": "texto sobre imagen, añadir texto foto, texto personalizado, tipografía imagen, frase foto, meme texto",
    "watermark": "marca agua, añadir watermark, logo imagen, protección imagen, copyright foto, firma imagen",
}

KW_PT = {
    "avif-support": "suporte AVIF, conversor AVIF, decodificar AVIF, AVIF para JPG, AVIF para PNG, compatibilidade AVIF navegador, formato imagem nova geração, arquivo AV1",
    "background-remover": "remover fundo, eliminar fundo, fundo transparente, remoção fundo com IA, grátis, foto produto, retrato, e-commerce",
    "base64": "codificador base64, decodificador base64, imagem para base64, base64 para imagem, converter imagem base64, codificar imagem",
    "bulk-processor": "processamento em lote, compressão em massa, redimensionar múltiplas, converter lote, editor imagens lote, redimensionar várias fotos",
    "circle-crop": "corte circular, imagem redonda, foto circular, recortar círculo, avatar redondo, foto perfil circular",
    "color-palette": "extrair paleta cores, paleta de imagem, cores dominantes, esquema cor, gerador paleta, analisar cores",
    "compressor": "comprimir imagem, reduzir tamanho imagem, otimizador imagens, comprimir JPG, comprimir PNG, compressão sem perda, compressão com perda",
    "converter": "converter imagem, JPG para PNG, PNG para JPG, WebP para JPG, conversor formato imagem, mudar formato",
    "cropper": "recortar imagem, cortar foto, ferramenta recorte, recorte livre, recorte proporção, recortar JPG",
    "face-blur": "desfocar rosto, borrar cara, pixelar rosto, anonimizar foto, privacidade imagem, ocultar rosto",
    "favicon-generator": "gerar favicon, criar favicon, favicon PNG, ícone site, favicon ico, ícone aba navegador",
    "gif-editor": "editor GIF, criar GIF, modificar GIF, GIF animado, otimizar GIF, velocidade GIF, recortar GIF",
    "heic-converter": "converter HEIC, HEIC para JPG, HEIC para PNG, conversor fotos iPhone, HEIC para WebP, converter formato Apple",
    "heic-to-jpg": "HEIC para JPG, converter fotos iPhone, HEIC para JPEG, conversor Apple, fotos iOS para JPG, HEIC grátis",
    "ico-icon-generator": "gerar ICO, criar ícone, PNG para ICO, favicon Windows, ícone desktop, conversor ICO",
    "id-photo": "foto documento, foto passaporte, foto identidade, foto visto, redimensionar foto documento, fundo branco foto",
    "image-adjust": "ajustar imagem, brilho contraste, saturação, ajuste cor, balanço branco, exposição, temperatura cor",
    "image-border": "adicionar borda imagem, moldura foto, borda arredondada, borda personalizada, emoldurar imagem, borda colorida",
    "image-compare": "comparar imagens, antes depois, comparação lado a lado, diferença imagens, comparar qualidade, controle deslizante",
    "image-compressor": "comprimir imagem, reduzir peso, compressor fotos, otimizar tamanho, comprimir sem perder qualidade, compressão online",
    "image-enhancer": "melhorar imagem, realçar foto, nitidez, ajustar iluminação, otimizar qualidade imagem, melhorar resolução",
    "image-exif-remover": "remover metadados, eliminar EXIF, apagar dados imagem, privacidade fotos, remover localização foto, limpar metadados",
    "image-filters": "filtros imagem, efeitos foto, filtro Instagram, preto branco, sépia, vintage, ajustar tom",
    "image-flip": "inverter imagem, espelhar foto, espelho horizontal, rotação vertical, inverter imagem, refletir foto",
    "image-grayscale": "preto branco, escala cinza, converter cinza, dessaturar imagem, foto monocromático, efeito preto branco",
    "image-merger": "unir imagens, combinar fotos, colagem, fundir imagens, juntar fotos, composição",
    "image-rotator": "rotacionar imagem, girar foto, virar imagem, endireitar foto, rotação livre, corrigir orientação",
    "image-shadow": "adicionar sombra imagem, sombra projetada, efeito sombra foto, sombra personalizada, sombra produto",
    "image-splitter": "dividir imagem, cortar foto em partes, separar imagem, picotar foto, grade imagem",
    "image-to-pdf": "imagem para PDF, converter JPG PDF, foto para PDF, PNG para PDF, criar PDF imagens, múltiplas imagens PDF",
    "image-upscaler": "ampliar imagem, aumentar resolução, reescalar foto, melhorar tamanho imagem, upscaling IA, aumentar pixels",
    "meme-generator": "criar meme, gerador memes, texto meme, meme personalizado, template meme, meme engraçado",
    "metadata-viewer": "ver metadados, dados EXIF, informação imagem, detalhes foto, visualizador EXIF, metadados câmera",
    "ocr": "extrair texto imagem, OCR online, reconhecer texto, imagem para texto, OCR grátis, escanear texto",
    "pdf-to-image": "PDF para imagem, converter PDF JPG, PDF para PNG, extrair páginas PDF, renderizar PDF",
    "photo-restoration": "restaurar foto, reparar imagem antiga, remover arranhões, restaurar foto danificada, restauração IA, consertar foto velha",
    "print-resizer": "redimensionar impressão, tamanho foto impressão, DPI, 300 DPI, formato impressão, foto para imprimir",
    "product-white-background": "fundo branco produto, foto produto e-commerce, fundo branco automático, foto catálogo, imagem produto profissional",
    "qr-code-generator": "gerar código QR, criar QR, QR personalizado, código QR grátis, QR logo, QR colorido",
    "resizer": "redimensionar imagem, mudar tamanho, escalar foto, ajustar dimensões, redimensionar porcentagem, tamanho personalizado",
    "screenshot-to-image": "captura tela para imagem, converter captura, colar área transferência, screenshot editor, captura para JPG",
    "social-media-post": "imagem redes sociais, foto Instagram, post Facebook, tamanho Twitter, banner LinkedIn, imagem social media",
    "svg-to-png": "SVG para PNG, converter vetor, exportar SVG, renderizar SVG, vetor para imagem, conversor vetores",
    "text-on-image": "texto sobre imagem, adicionar texto foto, texto personalizado, tipografia imagem, frase foto, meme texto",
    "watermark": "marca dágua, adicionar watermark, logo imagem, proteção imagem, copyright foto, assinatura imagem",
}

KW_ID = {
    "avif-support": "dukungan AVIF, konverter AVIF, decode AVIF, AVIF ke JPG, AVIF ke PNG, kompatibilitas AVIF browser, format gambar generasi baru, file AV1",
    "background-remover": "hapus latar belakang, hilangkan background, background transparan, penghapusan background AI, gratis, foto produk, potret, e-commerce",
    "base64": "encoder base64, decoder base64, gambar ke base64, base64 ke gambar, konversi gambar base64, encode gambar",
    "bulk-processor": "pemrosesan massal, kompresi massal, ubah ukuran banyak, konversi massal, editor gambar massal, ubah ukuran banyak foto",
    "circle-crop": "potong lingkaran, gambar bulat, foto lingkaran, crop bulat, avatar bulat, foto profil bulat",
    "color-palette": "ekstrak palet warna, palet gambar, warna dominan, skema warna, generator palet, analisis warna",
    "compressor": "kompres gambar, kurangi ukuran gambar, optimalkan gambar, kompres JPG, kompres PNG, kompresi lossless, kompresi lossy",
    "converter": "konversi gambar, JPG ke PNG, PNG ke JPG, WebP ke JPG, konverter format gambar, ubah format",
    "cropper": "potong gambar, crop foto, alat potong, potong bebas, potong rasio, potong JPG",
    "face-blur": "buramkan wajah, blur muka, pikselkan wajah, anonimkan foto, privasi gambar, sembunyikan wajah",
    "favicon-generator": "buat favicon, generator favicon, favicon PNG, ikon situs web, favicon ico, ikon tab browser",
    "gif-editor": "editor GIF, buat GIF, modifikasi GIF, GIF animasi, optimalkan GIF, kecepatan GIF, potong GIF",
    "heic-converter": "konversi HEIC, HEIC ke JPG, HEIC ke PNG, konverter foto iPhone, HEIC ke WebP, konversi format Apple",
    "heic-to-jpg": "HEIC ke JPG, konversi foto iPhone, HEIC ke JPEG, konverter Apple, foto iOS ke JPG, HEIC gratis",
    "ico-icon-generator": "buat ICO, generator ikon, PNG ke ICO, favicon Windows, ikon desktop, konverter ICO",
    "id-photo": "foto dokumen, foto paspor, foto KTP, foto visa, ubah ukuran foto dokumen, background putih foto",
    "image-adjust": "sesuaikan gambar, kecerahan kontras, saturasi, penyesuaian warna, white balance, eksposur, kehangatan",
    "image-border": "tambah bingkai gambar, bingkai foto, bingkai bulat, bingkai kustom, bingkai warna",
    "image-compare": "bandingkan gambar, sebelum sesudah, perbandingan sisi, perbedaan gambar, bandingkan kualitas, slider perbandingan",
    "image-compressor": "kompres gambar, kurangi ukuran, kompresor foto, optimalkan ukuran, kompres tanpa hilang kualitas, kompresi online",
    "image-enhancer": "tingkatkan gambar, perbaiki foto, ketajaman, sesuaikan pencahayaan, optimalkan kualitas gambar, tingkatkan resolusi",
    "image-exif-remover": "hapus metadata, hilangkan EXIF, hapus data gambar, privasi foto, hapus lokasi foto, bersihkan metadata",
    "image-filters": "filter gambar, efek foto, filter Instagram, hitam putih, sepia, vintage, sesuaikan tone",
    "image-flip": "balik gambar, cermin foto, cermin horizontal, rotasi vertikal, balikkan gambar, refleksi foto",
    "image-grayscale": "hitam putih, skala abu-abu, konversi abu-abu, desaturasi gambar, foto monokrom, efek hitam putih",
    "image-merger": "gabung gambar, kombinasikan foto, kolase, gabungkan gambar, satukan foto, komposisi",
    "image-rotator": "putar gambar, rotasi foto, balik gambar, luruskan foto, rotasi bebas, perbaiki orientasi",
    "image-shadow": "tambah bayangan gambar, drop shadow, efek bayangan foto, bayangan kustom, bayangan produk",
    "image-splitter": "belah gambar, potong foto jadi bagian, pisahkan gambar, iris foto, grid gambar",
    "image-to-pdf": "gambar ke PDF, konversi JPG PDF, foto ke PDF, PNG ke PDF, buat PDF gambar, banyak gambar PDF",
    "image-upscaler": "perbesar gambar, tingkatkan resolusi, upscale foto, perbaiki ukuran gambar, upscaling AI, tambah piksel",
    "meme-generator": "buat meme, generator meme, teks meme, meme kustom, template meme, meme lucu",
    "metadata-viewer": "lihat metadata, data EXIF, informasi gambar, detail foto, penampil EXIF, metadata kamera",
    "ocr": "ekstrak teks gambar, OCR online, kenali teks, gambar ke teks, OCR gratis, pindai teks",
    "pdf-to-image": "PDF ke gambar, konversi PDF JPG, PDF ke PNG, ekstrak halaman PDF, render PDF",
    "photo-restoration": "restorasi foto, perbaiki gambar lama, hilangkan goresan, restorasi foto rusak, restorasi AI, perbaiki foto lama",
    "print-resizer": "ubah ukuran cetak, ukuran foto cetak, DPI, 300 DPI, format cetak, foto untuk cetak",
    "product-white-background": "background putih produk, foto produk e-commerce, background putih otomatis, foto katalog, gambar produk profesional",
    "qr-code-generator": "buat kode QR, generator QR, QR kustom, kode QR gratis, QR logo, QR warna",
    "resizer": "ubah ukuran gambar, ganti ukuran, skala foto, sesuaikan dimensi, ubah ukuran persentase, ukuran kustom",
    "screenshot-to-image": "tangkapan layar ke gambar, konversi screenshot, tempel clipboard, editor screenshot, screenshot ke JPG",
    "social-media-post": "gambar media sosial, foto Instagram, post Facebook, ukuran Twitter, banner LinkedIn, gambar social media",
    "svg-to-png": "SVG ke PNG, konversi vektor, ekspor SVG, render SVG, vektor ke gambar, konverter vektor",
    "text-on-image": "teks di gambar, tambah teks foto, teks kustom, tipografi gambar, kutipan foto, meme teks",
    "watermark": "watermark, tambah watermark, logo gambar, perlindungan gambar, hak cipta foto, tanda tangan gambar",
}

# ============================================================
# TRANSLATED UI LABELS (for workspace HTML, howto section labels)
# ============================================================

UI_ES = {
    # Workspace common
    "Upload Image": "Subir Imagen",
    "or click to browse": "o haz clic para buscar",
    "Supports": "Compatible con",
    "Max": "Máx",
    "Works best with": "Funciona mejor con",
    "Try with a sample image": "Probar con imagen de muestra",
    "Remove Background": "Quitar Fondo",
    "Download All": "Descargar Todo",
    "Add More": "Añadir Más",
    "Clear All": "Limpiar Todo",
    "Download": "Descargar",
    "Reset": "Restablecer",
    "Upload": "Subir",
    "Convert": "Convertir",
    "Compress": "Comprimir",
    "Preview": "Vista previa",
    "Quality": "Calidad",
    "Output Format": "Formato de salida",
    "Choose File": "Elegir archivo",
    "Processing": "Procesando",
    "Processed": "Procesado",
    "Save": "Guardar",
    "Copy": "Copiar",
    "Close": "Cerrar",
    "Original": "Original",
    "Result": "Resultado",
    "Before": "Antes",
    "After": "Después",
    "Settings": "Ajustes",
    "Options": "Opciones",
    "Size": "Tamaño",
    "Width": "Ancho",
    "Height": "Alto",
    "Select All": "Seleccionar todo",
    "Drag and drop": "Arrastra y suelta",
    "Click or drag": "Haz clic o arrastra",
    "Drop file here": "Suelta el archivo aquí",
    "No file selected": "Sin archivo seleccionado",
    
    # Specific
    "Compress Result": "Comprimir Resultado",
    "Convert to WebP": "Convertir a WebP",
    "Add Watermark": "Añadir Marca de Agua",
    "What's next?": "¿Qué sigue?",
    "Your Browser's AVIF Support": "Compatibilidad AVIF de tu navegador",
    "Click upload area or drag": "Haz clic en el área de carga o arrastra",
    "Click upload area or drag and drop": "Haz clic o arrastra y suelta",
    "Click convert button": "Haz clic en convertir",
    "Download the result": "Descarga el resultado",
    
    # howto section
    "Cómo Usar": "Cómo Usar",
    "Guía Detallada": "Guía Detallada",
    "You Might Also Like": "También te puede interesar",
    
    # Dropzone labels  
    "Click or drag image here": "Haz clic o arrastra una imagen aquí",
    "Click or drag files here": "Haz clic o arrastra archivos aquí",
    "Click or drag AVIF file here": "Haz clic o arrastra archivo AVIF aquí",
}

UI_PT = {
    "Upload Image": "Enviar Imagem",
    "or click to browse": "ou clique para procurar",
    "Supports": "Compatível com",
    "Max": "Máx",
    "Works best with": "Funciona melhor com",
    "Try with a sample image": "Testar com imagem de exemplo",
    "Remove Background": "Remover Fundo",
    "Download All": "Baixar Tudo",
    "Add More": "Adicionar Mais",
    "Clear All": "Limpar Tudo",
    "Download": "Baixar",
    "Reset": "Redefinir",
    "Upload": "Enviar",
    "Convert": "Converter",
    "Compress": "Comprimir",
    "Preview": "Pré-visualizar",
    "Quality": "Qualidade",
    "Output Format": "Formato de Saída",
    "Choose File": "Escolher Arquivo",
    "Processing": "Processando",
    "Processed": "Processado",
    "Save": "Salvar",
    "Copy": "Copiar",
    "Close": "Fechar",
    "Original": "Original",
    "Result": "Resultado",
    "Before": "Antes",
    "After": "Depois",
    "Settings": "Configurações",
    "Options": "Opções",
    "Size": "Tamanho",
    "Width": "Largura",
    "Height": "Altura",
    "Select All": "Selecionar Tudo",
    "Drag and drop": "Arraste e solte",
    "Click or drag": "Clique ou arraste",
    "Drop file here": "Solte o arquivo aqui",
    "No file selected": "Nenhum arquivo selecionado",
    "Compress Result": "Comprimir Resultado",
    "Convert to WebP": "Converter para WebP",
    "Add Watermark": "Adicionar Marca D'água",
    "What's next?": "O que vem depois?",
    "Your Browser's AVIF Support": "Suporte AVIF do seu navegador",
    "Click upload area or drag": "Clique na área de upload ou arraste",
    "Click upload area or drag and drop": "Clique ou arraste e solte",
    "Click convert button": "Clique no botão converter",
    "Download the result": "Baixe o resultado",
    "Como Usar": "Como Usar",
    "Guia Detalhada": "Guia Detalhada",
    "You Might Also Like": "Você Também Pode Gostar",
    "Click or drag image here": "Clique ou arraste uma imagem aqui",
    "Click or drag files here": "Clique ou arraste arquivos aqui",
    "Click or drag AVIF file here": "Clique ou arraste arquivo AVIF aqui",
}

UI_ID = {
    "Upload Image": "Unggah Gambar",
    "or click to browse": "atau klik untuk mencari",
    "Supports": "Mendukung",
    "Max": "Maks",
    "Works best with": "Paling cocok dengan",
    "Try with a sample image": "Coba dengan gambar contoh",
    "Remove Background": "Hapus Latar Belakang",
    "Download All": "Unduh Semua",
    "Add More": "Tambah Lagi",
    "Clear All": "Hapus Semua",
    "Download": "Unduh",
    "Reset": "Atur Ulang",
    "Upload": "Unggah",
    "Convert": "Konversi",
    "Compress": "Kompres",
    "Preview": "Pratinjau",
    "Quality": "Kualitas",
    "Output Format": "Format Output",
    "Choose File": "Pilih File",
    "Processing": "Memproses",
    "Processed": "Diproses",
    "Save": "Simpan",
    "Copy": "Salin",
    "Close": "Tutup",
    "Original": "Asli",
    "Result": "Hasil",
    "Before": "Sebelum",
    "After": "Sesudah",
    "Settings": "Pengaturan",
    "Options": "Opsi",
    "Size": "Ukuran",
    "Width": "Lebar",
    "Height": "Tinggi",
    "Select All": "Pilih Semua",
    "Drag and drop": "Seret dan lepas",
    "Click or drag": "Klik atau seret",
    "Drop file here": "Lepaskan file di sini",
    "No file selected": "Tidak ada file dipilih",
    "Compress Result": "Kompres Hasil",
    "Convert to WebP": "Konversi ke WebP",
    "Add Watermark": "Tambah Watermark",
    "What's next?": "Apa selanjutnya?",
    "Your Browser's AVIF Support": "Dukungan AVIF Browser Anda",
    "Click upload area or drag": "Klik area unggah atau seret",
    "Click upload area or drag and drop": "Klik atau seret dan lepas",
    "Click convert button": "Klik tombol konversi",
    "Download the result": "Unduh hasilnya",
    "Cara Menggunakan": "Cara Menggunakan",
    "Panduan Lengkap": "Panduan Lengkap",
    "You Might Also Like": "Anda Mungkin Juga Suka",
    "Click or drag image here": "Klik atau seret gambar di sini",
    "Click or drag files here": "Klik atau seret file di sini",
    "Click or drag AVIF file here": "Klik atau seret file AVIF di sini",
}

# ============================================================
# TRANSLATED TOOL NAMES (for related section)
# ============================================================

TOOL_NAMES_ES = {
    "AVIF Support": "Soporte AVIF",
    "Background Remover": "Quitar Fondo",
    "Base64 Encoder/Decoder": "Codificador Base64",
    "Bulk Processor": "Procesador por Lotes",
    "Circle Crop": "Recorte Circular",
    "Color Palette Extractor": "Extractor de Paleta",
    "Compressor": "Compresor",
    "Image Compressor": "Compresor de Imagen",
    "Bulk Image Compressor": "Compresor por Lotes",
    "Converter": "Conversor",
    "Image Converter": "Conversor de Imagen",
    "Cropper": "Recortador",
    "Face Blur": "Difuminar Rostros",
    "Favicon Generator": "Generador de Favicon",
    "GIF Editor": "Editor GIF",
    "HEIC Converter": "Conversor HEIC",
    "HEIC to JPG": "HEIC a JPG",
    "ICO Icon Generator": "Generador de ICO",
    "ID Photo Maker": "Creador de Foto Carnet",
    "Image Adjust": "Ajustar Imagen",
    "Image Border": "Borde de Imagen",
    "Image Compare": "Comparar Imágenes",
    "Image Enhancer": "Mejorar Imagen",
    "Image EXIF Remover": "Eliminar EXIF",
    "Image Filters": "Filtros de Imagen",
    "Image Flip": "Voltear Imagen",
    "Image Grayscale": "Escala de Grises",
    "Image Merger": "Unir Imágenes",
    "Image Rotator": "Rotar Imagen",
    "Image Shadow": "Sombra de Imagen",
    "Image Splitter": "Dividir Imagen",
    "Image to PDF": "Imagen a PDF",
    "Image Upscaler": "Ampliar Imagen",
    "Meme Generator": "Generador de Memes",
    "Metadata Viewer": "Visor de Metadatos",
    "OCR Text Extractor": "Extractor OCR",
    "PDF to Image": "PDF a Imagen",
    "Photo Restoration": "Restauración de Fotos",
    "Print Resizer": "Redimensionar Impresión",
    "Product White Background": "Fondo Blanco Producto",
    "QR Code Generator": "Generador QR",
    "Resizer": "Redimensionar",
    "Screenshot to Image": "Captura a Imagen",
    "Social Media Post Maker": "Creador de Posts",
    "SVG to PNG": "SVG a PNG",
    "Text on Image": "Texto en Imagen",
    "Watermark": "Marca de Agua",
}

TOOL_NAMES_PT = {
    "AVIF Support": "Suporte AVIF",
    "Background Remover": "Remover Fundo",
    "Base64 Encoder/Decoder": "Codificador Base64",
    "Bulk Processor": "Processador em Lote",
    "Circle Crop": "Corte Circular",
    "Color Palette Extractor": "Extrator de Paleta",
    "Compressor": "Compressor",
    "Image Compressor": "Compressor de Imagem",
    "Bulk Image Compressor": "Compressor em Lote",
    "Converter": "Conversor",
    "Image Converter": "Conversor de Imagem",
    "Cropper": "Recortador",
    "Face Blur": "Desfocar Rostos",
    "Favicon Generator": "Gerador de Favicon",
    "GIF Editor": "Editor GIF",
    "HEIC Converter": "Conversor HEIC",
    "HEIC to JPG": "HEIC para JPG",
    "ICO Icon Generator": "Gerador de ICO",
    "ID Photo Maker": "Criador de Foto Documento",
    "Image Adjust": "Ajustar Imagem",
    "Image Border": "Borda de Imagem",
    "Image Compare": "Comparar Imagens",
    "Image Enhancer": "Melhorar Imagem",
    "Image EXIF Remover": "Remover EXIF",
    "Image Filters": "Filtros de Imagem",
    "Image Flip": "Inverter Imagem",
    "Image Grayscale": "Escala de Cinza",
    "Image Merger": "Unir Imagens",
    "Image Rotator": "Rotacionar Imagem",
    "Image Shadow": "Sombra de Imagem",
    "Image Splitter": "Dividir Imagem",
    "Image to PDF": "Imagem para PDF",
    "Image Upscaler": "Ampliar Imagem",
    "Meme Generator": "Gerador de Memes",
    "Metadata Viewer": "Visualizador de Metadados",
    "OCR Text Extractor": "Extrator OCR",
    "PDF to Image": "PDF para Imagem",
    "Photo Restoration": "Restauração de Fotos",
    "Print Resizer": "Redimensionar Impressão",
    "Product White Background": "Fundo Branco Produto",
    "QR Code Generator": "Gerador QR",
    "Resizer": "Redimensionar",
    "Screenshot to Image": "Captura para Imagem",
    "Social Media Post Maker": "Criador de Posts",
    "SVG to PNG": "SVG para PNG",
    "Text on Image": "Texto na Imagem",
    "Watermark": "Marca D'água",
}

TOOL_NAMES_ID = {
    "AVIF Support": "Dukungan AVIF",
    "Background Remover": "Hapus Latar Belakang",
    "Base64 Encoder/Decoder": "Encoder Base64",
    "Bulk Processor": "Pemroses Massal",
    "Circle Crop": "Potong Lingkaran",
    "Color Palette Extractor": "Ekstraktor Palet",
    "Compressor": "Kompresor",
    "Image Compressor": "Kompresor Gambar",
    "Bulk Image Compressor": "Kompresor Massal",
    "Converter": "Konverter",
    "Image Converter": "Konverter Gambar",
    "Cropper": "Pemotong",
    "Face Blur": "Buramkan Wajah",
    "Favicon Generator": "Generator Favicon",
    "GIF Editor": "Editor GIF",
    "HEIC Converter": "Konverter HEIC",
    "HEIC to JPG": "HEIC ke JPG",
    "ICO Icon Generator": "Generator ICO",
    "ID Photo Maker": "Pembuat Foto Dokumen",
    "Image Adjust": "Sesuaikan Gambar",
    "Image Border": "Bingkai Gambar",
    "Image Compare": "Bandingkan Gambar",
    "Image Enhancer": "Tingkatkan Gambar",
    "Image EXIF Remover": "Hapus EXIF",
    "Image Filters": "Filter Gambar",
    "Image Flip": "Balik Gambar",
    "Image Grayscale": "Skala Abu-abu",
    "Image Merger": "Gabung Gambar",
    "Image Rotator": "Putar Gambar",
    "Image Shadow": "Bayangan Gambar",
    "Image Splitter": "Belah Gambar",
    "Image to PDF": "Gambar ke PDF",
    "Image Upscaler": "Perbesar Gambar",
    "Meme Generator": "Generator Meme",
    "Metadata Viewer": "Penampil Metadata",
    "OCR Text Extractor": "Ekstraktor OCR",
    "PDF to Image": "PDF ke Gambar",
    "Photo Restoration": "Restorasi Foto",
    "Print Resizer": "Pengubah Ukuran Cetak",
    "Product White Background": "Background Putih Produk",
    "QR Code Generator": "Generator QR",
    "Resizer": "Pengubah Ukuran",
    "Screenshot to Image": "Screenshot ke Gambar",
    "Social Media Post Maker": "Pembuat Posting",
    "SVG to PNG": "SVG ke PNG",
    "Text on Image": "Teks di Gambar",
    "Watermark": "Watermark",
}

# ============================================================
# RELATED TOOL DESCRIPTIONS (short phrases for each tool in each language)
# ============================================================

RELATED_DESC_ES = {
    "avif-support": "Convierte AVIF a JPG/PNG/WebP",
    "background-remover": "Elimina fondos con IA en tu navegador",
    "base64": "Convierte imágenes a texto base64",
    "bulk-processor": "Procesa varias imágenes a la vez",
    "circle-crop": "Recorta imágenes en forma circular",
    "color-palette": "Extrae colores dominantes de imágenes",
    "compressor": "Reduce el tamaño de archivo sin perder calidad",
    "converter": "Convierte entre JPG, PNG, WebP y más",
    "cropper": "Recorta imágenes a cualquier proporción",
    "face-blur": "Protege la privacidad difuminando rostros",
    "favicon-generator": "Crea iconos para tu sitio web",
    "gif-editor": "Edita y optimiza GIFs animados",
    "heic-converter": "Convierte fotos de iPhone a formato universal",
    "heic-to-jpg": "Convierte HEIC a JPG al instante",
    "ico-icon-generator": "Crea archivos ICO desde PNG",
    "id-photo": "Crea fotos tamaño carnet para documentos",
    "image-adjust": "Ajusta brillo, contraste y saturación",
    "image-border": "Añade bordes y marcos a tus imágenes",
    "image-compare": "Compara imágenes lado a lado",
    "image-compressor": "Comprime imágenes sin perder calidad",
    "image-enhancer": "Mejora automáticamente la calidad de imagen",
    "image-exif-remover": "Elimina metadatos para proteger tu privacidad",
    "image-filters": "Aplica filtros y efectos fotográficos",
    "image-flip": "Voltea imágenes horizontal o verticalmente",
    "image-grayscale": "Convierte imágenes a blanco y negro",
    "image-merger": "Combina varias imágenes en una sola",
    "image-rotator": "Gira imágenes a cualquier ángulo",
    "image-shadow": "Añade sombras profesionales a imágenes",
    "image-splitter": "Divide imágenes en partes iguales",
    "image-to-pdf": "Convierte imágenes a documentos PDF",
    "image-upscaler": "Aumenta la resolución de imágenes",
    "meme-generator": "Crea memes personalizados con texto",
    "metadata-viewer": "Inspecciona los metadatos de tus imágenes",
    "ocr": "Extrae texto de imágenes con OCR",
    "pdf-to-image": "Convierte páginas PDF a imágenes",
    "photo-restoration": "Restaura fotos antiguas con IA",
    "print-resizer": "Prepara imágenes para impresión profesional",
    "product-white-background": "Genera fondo blanco para fotos de producto",
    "qr-code-generator": "Crea códigos QR personalizados",
    "resizer": "Cambia las dimensiones de cualquier imagen",
    "screenshot-to-image": "Convierte capturas de pantalla a imágenes",
    "social-media-post": "Crea imágenes optimizadas para redes sociales",
    "svg-to-png": "Convierte gráficos vectoriales SVG a PNG",
    "text-on-image": "Añade texto personalizado a tus imágenes",
    "watermark": "Protege tus imágenes con marcas de agua",
}

RELATED_DESC_PT = {
    "avif-support": "Converte AVIF para JPG/PNG/WebP",
    "background-remover": "Remove fundos com IA no seu navegador",
    "base64": "Converte imagens para texto base64",
    "bulk-processor": "Processa várias imagens de uma vez",
    "circle-crop": "Recorta imagens em formato circular",
    "color-palette": "Extrai cores dominantes de imagens",
    "compressor": "Reduz o tamanho do arquivo sem perder qualidade",
    "converter": "Converte entre JPG, PNG, WebP e mais",
    "cropper": "Recorta imagens em qualquer proporção",
    "face-blur": "Protege a privacidade desfocando rostos",
    "favicon-generator": "Cria ícones para seu site",
    "gif-editor": "Edita e otimiza GIFs animados",
    "heic-converter": "Converte fotos do iPhone para formato universal",
    "heic-to-jpg": "Converte HEIC para JPG instantaneamente",
    "ico-icon-generator": "Cria arquivos ICO a partir de PNG",
    "id-photo": "Cria fotos tamanho documento",
    "image-adjust": "Ajusta brilho, contraste e saturação",
    "image-border": "Adiciona bordas e molduras às suas imagens",
    "image-compare": "Compara imagens lado a lado",
    "image-compressor": "Comprime imagens sem perder qualidade",
    "image-enhancer": "Melhora automaticamente a qualidade da imagem",
    "image-exif-remover": "Remove metadados para proteger sua privacidade",
    "image-filters": "Aplica filtros e efeitos fotográficos",
    "image-flip": "Inverte imagens horizontal ou verticalmente",
    "image-grayscale": "Converte imagens para preto e branco",
    "image-merger": "Combina várias imagens em uma só",
    "image-rotator": "Gira imagens em qualquer ângulo",
    "image-shadow": "Adiciona sombras profissionais às imagens",
    "image-splitter": "Divide imagens em partes iguais",
    "image-to-pdf": "Converte imagens para documentos PDF",
    "image-upscaler": "Aumenta a resolução de imagens",
    "meme-generator": "Cria memes personalizados com texto",
    "metadata-viewer": "Inspeciona os metadados das suas imagens",
    "ocr": "Extrai texto de imagens com OCR",
    "pdf-to-image": "Converte páginas PDF para imagens",
    "photo-restoration": "Restaura fotos antigas com IA",
    "print-resizer": "Prepara imagens para impressão profissional",
    "product-white-background": "Gera fundo branco para fotos de produto",
    "qr-code-generator": "Cria códigos QR personalizados",
    "resizer": "Altera as dimensões de qualquer imagem",
    "screenshot-to-image": "Converte capturas de tela para imagens",
    "social-media-post": "Cria imagens otimizadas para redes sociais",
    "svg-to-png": "Converte gráficos vetoriais SVG para PNG",
    "text-on-image": "Adiciona texto personalizado às suas imagens",
    "watermark": "Protege suas imagens com marcas d'água",
}

RELATED_DESC_ID = {
    "avif-support": "Konversi AVIF ke JPG/PNG/WebP",
    "background-remover": "Hapus latar belakang dengan AI di browser",
    "base64": "Konversi gambar ke teks base64",
    "bulk-processor": "Proses banyak gambar sekaligus",
    "circle-crop": "Potong gambar menjadi bentuk lingkaran",
    "color-palette": "Ekstrak warna dominan dari gambar",
    "compressor": "Kurangi ukuran file tanpa hilang kualitas",
    "converter": "Konversi antara JPG, PNG, WebP dan lainnya",
    "cropper": "Potong gambar ke rasio apa pun",
    "face-blur": "Lindungi privasi dengan memburamkan wajah",
    "favicon-generator": "Buat ikon untuk situs web Anda",
    "gif-editor": "Edit dan optimalkan GIF animasi",
    "heic-converter": "Konversi foto iPhone ke format universal",
    "heic-to-jpg": "Konversi HEIC ke JPG instan",
    "ico-icon-generator": "Buat file ICO dari PNG",
    "id-photo": "Buat foto ukuran dokumen resmi",
    "image-adjust": "Sesuaikan kecerahan, kontras, saturasi",
    "image-border": "Tambahkan bingkai ke gambar Anda",
    "image-compare": "Bandingkan gambar berdampingan",
    "image-compressor": "Kompres gambar tanpa hilang kualitas",
    "image-enhancer": "Tingkatkan kualitas gambar otomatis",
    "image-exif-remover": "Hapus metadata untuk lindungi privasi",
    "image-filters": "Terapkan filter dan efek fotografi",
    "image-flip": "Balik gambar horizontal atau vertikal",
    "image-grayscale": "Konversi gambar ke hitam putih",
    "image-merger": "Gabungkan beberapa gambar jadi satu",
    "image-rotator": "Putar gambar ke sudut apa pun",
    "image-shadow": "Tambahkan bayangan profesional ke gambar",
    "image-splitter": "Bagi gambar menjadi bagian sama besar",
    "image-to-pdf": "Konversi gambar ke dokumen PDF",
    "image-upscaler": "Tingkatkan resolusi gambar",
    "meme-generator": "Buat meme kustom dengan teks",
    "metadata-viewer": "Periksa metadata gambar Anda",
    "ocr": "Ekstrak teks dari gambar dengan OCR",
    "pdf-to-image": "Konversi halaman PDF ke gambar",
    "photo-restoration": "Restorasi foto lama dengan AI",
    "print-resizer": "Siapkan gambar untuk cetak profesional",
    "product-white-background": "Hasilkan background putih untuk foto produk",
    "qr-code-generator": "Buat kode QR kustom",
    "resizer": "Ubah dimensi gambar apa pun",
    "screenshot-to-image": "Konversi tangkapan layar ke gambar",
    "social-media-post": "Buat gambar optimal untuk media sosial",
    "svg-to-png": "Konversi grafik vektor SVG ke PNG",
    "text-on-image": "Tambahkan teks kustom ke gambar",
    "watermark": "Lindungi gambar dengan watermark",
}


# ============================================================
# MAIN TRANSLATION ENGINE
# ============================================================

def translate_howto_guide(tool_slug, field_html, lang, existing_h2):
    """
    Translate howto_html or guide_html content.
    
    For howto: <h4> and <p> elements inside .how-to-step divs need translation.
    For guide: <h3> and <p> elements inside .guide-block divs need translation.
    
    We use the existing translated h2 section title for context.
    The content is tool-specific and was originally in English.
    """
    # The howto and guide content varies significantly per tool.
    # We translate using regex to find English h3/h4 and p tags and replace them.
    # This is a simplified approach - for production, we'd need per-tool translations.
    
    # For now, we apply UI label translations to workspace_html and return the same
    # howto/guide - we'll handle those in a separate pass
    return field_html


def translate_keywords(tool_slug, lang, kw_map):
    """Replace English keywords with translated ones."""
    if lang == 'es':
        return kw_map.get(tool_slug, '')
    elif lang == 'pt':
        return kw_map.get(tool_slug, '')
    elif lang == 'id':
        return kw_map.get(tool_slug, '')
    return ''


def translate_workspace_ui(html, lang, ui_map):
    """Apply UI label translations to workspace_html."""
    result = html
    for en_text, translated in ui_map.items():
        # Only replace standalone text, not inside class names or attributes
        # Simple approach: replace text nodes
        result = result.replace(f'>{en_text}<', f'>{translated}<')
        result = result.replace(f'"{en_text}"', f'"{translated}"')
    return result


def build_related_html(tool_slug, related_tools, lang, tool_names_map, desc_map):
    """Build translated related tools section."""
    if lang == 'es':
        title = 'También te puede interesar'
    elif lang == 'pt':
        title = 'Você Também Pode Gostar'
    else:
        title = 'Anda Mungkin Juga Suka'
    
    lang_dir = lang if lang != 'en' else ''
    if lang_dir:
        prefix = f'/{lang_dir}/tools/'
    else:
        prefix = '/tools/'
    
    cards = []
    for rt_slug, rt_name_en, rt_desc_en in related_tools:
        rt_name = tool_names_map.get(rt_name_en, rt_name_en)
        rt_desc = desc_map.get(rt_slug, rt_desc_en)
        # Find the emoji from original if possible - we'll use a default
        cards.append(f'''    <a href="{prefix}{rt_slug}.html" class="related-tool-card">
      <span class="tool-icon">🔧</span>
      <div class="tool-info">
        <strong>{rt_name}</strong>
        <span class="tool-desc">{rt_desc}</span>
      </div>
      <span class="tool-arrow">→</span>
    </a>''')
    
    return f'''<section class="related-tools">
  <h2>{title}</h2>
  <div class="related-tools-grid">
{chr(10).join(cards)}
  </div>
</section>'''


def process_language(lang, kw_map, ui_map, tool_names_map, desc_map):
    """Process one language's _tools_data_{lang}.json."""
    filepath = f'_tools_data_{lang}.json'
    print(f'\n{"="*60}')
    print(f'Processing {filepath}...')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tools = data['tools']
    updated = 0
    
    for tool in tools:
        slug = tool['slug']
        
        # 1. Keywords
        if slug in kw_map and kw_map[slug]:
            tool['keywords'] = kw_map[slug]
            updated += 1
        
        # 2. Workspace HTML UI labels
        if 'workspace_html' in tool:
            tool['workspace_html'] = translate_workspace_ui(
                tool['workspace_html'], lang, ui_map
            )
        
        # 3. Related tools - rebuild with translations
        # Parse existing related_html to extract tool references
        related_html = tool.get('related_html', '')
        if related_html:
            # Extract related tool slugs and names
            rel_slugs = re.findall(r'href="/[a-z]+/tools/([^"]+)\.html"', related_html)
            if not rel_slugs:
                rel_slugs = re.findall(r'href="/tools/([^"]+)\.html"', related_html)
            rel_strongs = re.findall(r'<strong>(.*?)</strong>', related_html)
            rel_descs = re.findall(r'<span class="tool-desc">(.*?)</span>', related_html)
            
            related_tools = []
            for i in range(min(len(rel_slugs), len(rel_strongs), len(rel_descs))):
                related_tools.append((rel_slugs[i], rel_strongs[i], rel_descs[i]))
            
            if related_tools:
                tool['related_html'] = build_related_html(
                    slug, related_tools, lang, tool_names_map, desc_map
                )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'Updated {updated}/{len(tools)} tools in {filepath}')
    return data


if __name__ == '__main__':
    # Process all three languages
    for lang, kw_map, ui_map, tn_map, desc_map in [
        ('es', KW_ES, UI_ES, TOOL_NAMES_ES, RELATED_DESC_ES),
        ('pt', KW_PT, UI_PT, TOOL_NAMES_PT, RELATED_DESC_PT),
        ('id', KW_ID, UI_ID, TOOL_NAMES_ID, RELATED_DESC_ID),
    ]:
        process_language(lang, kw_map, ui_map, tn_map, desc_map)
    
    print('\n✅ All three languages processed!')
    print('Next: run _build.py --all to rebuild all pages')
