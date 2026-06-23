const fs = require('fs');
const path = require('path');

// ============================================================
// DATA: FAQ content with translations for top 15 pages
// Format: faq[][en, es, pt, id]
// ============================================================
const content = {
  'background-remover': {
    faq: [
      ['What types of images work best?','¿Qué tipos de imágenes funcionan mejor?','Quais tipos de imagens funcionam melhor?','Jenis gambar apa yang paling cocok?'],
      ['What is the maximum image size?','¿Cuál es el tamaño máximo?','Qual é o tamanho máximo?','Apa ukuran maksimum gambar?'],
      ['Does this work for e-commerce?','¿Funciona para e-commerce?','Funciona para e-commerce?','Apakah ini bekerja untuk e-commerce?'],
      ['Can I use outputs commercially?','¿Puedo usar los resultados comercialmente?','Posso usar os resultados comercialmente?','Bisakah saya gunakan untuk komersial?'],
      ['How does AI work without uploading?','¿Cómo funciona la IA sin subir archivos?','Como a IA funciona sem upload?','Bagaimana AI bekerja tanpa upload?'],
      ['Does it work with animals?','¿Funciona con animales?','Funciona com animais?','Apakah bekerja dengan hewan?']
    ],
    es: { t:'Quitar Fondo de Imagen Online Gratis — SmartImgKit', h:'✂️ Quitar Fondo de Imagen', md:'Elimina el fondo de tus imágenes gratis con IA. 100% en tu navegador, sin subir archivos.', hd:'Elimina el fondo de cualquier imagen usando IA — completamente en tu navegador. Sin subidas. Obtén un PNG transparente en segundos.', bc:'✂️ Quitar Fondo de Imagen' },
    pt: { t:'Remover Fundo de Imagem Online Grátis — SmartImgKit', h:'✂️ Remover Fundo de Imagem', md:'Remova o fundo das suas imagens grátis com IA. 100% no seu navegador, sem uploads.', hd:'Remova o fundo de qualquer imagem usando IA — totalmente no seu navegador. Sem uploads. Obtenha um PNG transparente em segundos.', bc:'✂️ Remover Fundo de Imagem' },
    id: { t:'Hapus Latar Belakang Gambar Online Gratis — SmartImgKit', h:'✂️ Hapus Latar Belakang', md:'Hapus latar belakang gambar gratis dengan AI. 100% di browser Anda, tanpa upload.', hd:'Hapus latar belakang gambar apa pun menggunakan AI — sepenuhnya di browser Anda. Dapatkan PNG transparan dalam hitungan detik.', bc:'✂️ Hapus Latar Belakang' },
    faqAnswers: [
      ['Images with clear subjects and high contrast work best. Portraits and product photos work great.','Imágenes con sujetos claros y alto contraste funcionan mejor. Retratos y fotos de producto funcionan excelente.','Imagens com assuntos claros e alto contraste funcionam melhor. Retratos e fotos de produto funcionam muito bem.','Gambar dengan subjek jelas dan kontras tinggi paling cocok. Potret dan foto produk bekerja dengan baik.'],
      ['10MB per image. For best results use images between 500KB and 5MB.','10MB por imagen. Para mejores resultados usa imágenes entre 500KB y 5MB.','10MB por imagem. Para melhores resultados use imagens entre 500KB e 5MB.','10MB per gambar. Untuk hasil terbaik gunakan gambar antara 500KB dan 5MB.'],
      ['Yes. Optimized for product photography. Use the Product White Background tool after.','Sí. Optimizado para fotografía de producto. Usa la herramienta de Fondo Blanco después.','Sim. Otimizado para fotografia de produto. Use a ferramenta Fundo Branco depois.','Ya. Dioptimalkan untuk fotografi produk. Gunakan alat Latar Putih setelahnya.'],
      ['Yes. All images retain your full ownership. Use without attribution.','Sí. Todas las imágenes conservan tu propiedad total. Úsalas sin atribución.','Sim. Todas as imagens mantêm sua propriedade total. Use sem atribuição.','Ya. Semua gambar tetap milik Anda sepenuhnya. Gunakan tanpa atribusi.'],
      ['The model runs in your browser via WebAssembly. No server needed once loaded.','El modelo se ejecuta en tu navegador via WebAssembly. No necesita servidor.','O modelo roda no seu navegador via WebAssembly. Sem servidor.','Model berjalan di browser Anda via WebAssembly. Tanpa server setelah dimuat.'],
      ['Yes. Works for pets, vehicles, furniture, and any subject.','Sí. Funciona para mascotas, vehículos, muebles y cualquier objeto.','Sim. Funciona para animais, veículos, móveis e qualquer objeto.','Ya. Bekerja untuk hewan, kendaraan, furnitur, dan objek apa pun.']
    ]
  }
};

const LANG = ['es','pt','id'];
const FAQ_TITLES = {en:'More Frequently Asked Questions',es:'Más Preguntas Frecuentes',pt:'Mais Perguntas Frequentes',id:'Pertanyaan Umum Lainnya'};
const STEP_LABELS = {
  es: { 'How to Use':'Cómo Usar','Detailed User Guide':'Guía Detallada','Frequently Asked Questions':'Preguntas Frecuentes','Related Tools':'Herramientas Relacionadas','Home':'Inicio','Tools':'Herramientas','About':'Acerca de','Contact':'Contacto','Drop an image here':'Arrastra una imagen aquí','Try with a sample image':'Probar con imagen de ejemplo'},
  pt: { 'How to Use':'Como Usar','Detailed User Guide':'Guia Detalhada','Frequently Asked Questions':'Perguntas Frequentes','Related Tools':'Ferramentas Relacionadas','Home':'Início','Tools':'Ferramentas','About':'Sobre','Contact':'Contato','Drop an image here':'Arraste uma imagem aqui','Try with a sample image':'Testar com imagem de exemplo'},
  id: { 'How to Use':'Cara Menggunakan','Detailed User Guide':'Panduan Lengkap','Frequently Asked Questions':'Pertanyaan Umum','Related Tools':'Alat Terkait','Home':'Beranda','Tools':'Alat','About':'Tentang','Contact':'Kontak','Drop an image here':'Seret gambar ke sini','Try with a sample image':'Coba dengan gambar contoh'}
};
const FOOTER = {
  es: { free:'Herramientas de imagen gratuitas con IA que respetan tu privacidad.', rights:'Todos los derechos reservados.' },
  pt: { free:'Ferramentas de imagem gratuitas com IA que respeitam sua privacidade.', rights:'Todos os direitos reservados.' },
  id: { free:'Alat gambar gratis dengan AI yang menghormati privasi Anda.', rights:'Hak cipta dilindungi.' }
};

const BASE = path.join(__dirname);
const TOOLS = path.join(BASE,'tools');
console.log('TOOLS path:', TOOLS);
console.log('File exists:', fs.existsSync(path.join(TOOLS,'background-remover.html')));

// Process each layer - start with just background-remover as test
const name = 'background-remover';
const data = content[name];
const srcFile = path.join(TOOLS, name+'.html');
let enHTML = fs.readFileSync(srcFile,'utf8');

// --- Create FAQ QA pairs for EN and each lang ---
const enQA = data.faq.map((q,i) => [q[0], data.faqAnswers[i][0]]);
const langQA = {};
LANG.forEach((l, li) => {
  langQA[l] = data.faq.map((q,i) => [q[li+1], data.faqAnswers[i][li+1]]);
});

function genFAQSection(qas, title) {
  const items = qas.map(([q,a]) => '  <div class="faq-item"><button class="faq-question">'+q+'</button><div class="faq-answer">'+a+'</div></div>').join('\n');
  return `<section class="faq-section" style="margin-top:32px">\n  <h2>${title}</h2>\n${items}\n</section>`;
}

function genFAQSchema(qas) {
  return '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n' + qas.map(([q,a]) => '    {\n      "@type": "Question",\n      "name": '+JSON.stringify(q)+',\n      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": '+JSON.stringify(a)+'\n      }\n    }').join(',\n') + '\n  ]\n}\n</script>';
}

// --- Enhance English ---
enHTML = enHTML.replace('</main>', genFAQSection(enQA, 'More Frequently Asked Questions') + '\n    </main>');
enHTML = enHTML.replace('</body>', genFAQSchema(enQA) + '\n</body>');
// Add hreflangs
LANG.forEach(l => {
  if (!enHTML.includes('hreflang="'+l+'"'))
    enHTML = enHTML.replace('</head>', '\n  <link rel="alternate" hreflang="'+l+'" href="https://smartimgkit.com/'+l+'/tools/'+name+'">\n</head>');
});
if (!enHTML.includes('hreflang="en"'))
  enHTML = enHTML.replace('</head>', '\n  <link rel="alternate" hreflang="en" href="https://smartimgkit.com/tools/'+name+'">\n  <link rel="alternate" hreflang="x-default" href="https://smartimgkit.com/tools/'+name+'">\n</head>');
  
fs.writeFileSync(srcFile, enHTML, 'utf8');
console.log('EN done');

// --- Create language versions ---
LANG.forEach(l => {
  const dir = path.join(BASE, l, 'tools');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});
  const meta = data[l];
  let h = enHTML;
  
  h = h.replace('<html lang="en"', '<html lang="'+l+'"');
  h = h.replace(/<title>[^<]+<\/title>/, '<title>'+meta.t+'</title>');
  h = h.replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="'+meta.md+'"');
  h = h.replace(/<link rel="canonical"[^>]*>/, '<link rel="canonical" href="https://smartimgkit.com/'+l+'/tools/'+name+'">');
  h = h.replace(/\s*<link rel="alternate"[^>]*>/g, '');
  
  let ll = '';
  LANG.forEach(l2 => { ll += '\n  <link rel="alternate" hreflang="'+l2+'" href="https://smartimgkit.com/'+l2+'/tools/'+name+'">'; });
  ll += '\n  <link rel="alternate" hreflang="en" href="https://smartimgkit.com/tools/'+name+'">';
  ll += '\n  <link rel="alternate" hreflang="x-default" href="https://smartimgkit.com/tools/'+name+'">';
  h = h.replace('</head>', ll+'\n</head>');
  
  h = h.replace(/<meta property="og:title"[^>]*>/, '<meta property="og:title" content="'+meta.t+'">');
  h = h.replace(/<meta property="og:description"[^>]*>/, '<meta property="og:description" content="'+meta.md+'">');
  h = h.replace(/<meta property="og:url"[^>]*>/, '<meta property="og:url" content="https://smartimgkit.com/'+l+'/tools/'+name+'">');
  h = h.replace(/<meta name="twitter:title"[^>]*>/, '<meta name="twitter:title" content="'+meta.t+'">');
  h = h.replace(/<meta name="twitter:description"[^>]*>/, '<meta name="twitter:description" content="'+meta.md+'">');
  
  h = h.replace(/<h1>[^<]+<\/h1>/, '<h1>'+meta.h+'</h1>');
  h = h.replace(/<p>(Remove|Compress|Convert|Enlarge|Reduce|Resize|Crop|Create|Add|Combine|Rotate|Adjust|Split|Strip|Extract|Generate|Design|Enhance|Apply|Wrap|Compare|View|Check|Blur|Restore|Reshape|Design)[^<]*<\/p>/, '<p>'+meta.hd+'</p>');
  
  // Breadcrumb
  h = h.replace(/<span>[^<]*<\/span>\s*<\/nav>/, '<span>'+meta.bc+'</span>\n      </nav>');
  
  // Translate FAQ section (replace EN content with lang version)
  const enSection = genFAQSection(enQA, 'More Frequently Asked Questions');
  const langSection = genFAQSection(langQA[l], FAQ_TITLES[l]);
  h = h.replace(enSection, langSection);
  
  // Translate FAQ Schema
  const enSchema = genFAQSchema(enQA);
  const langSchema = genFAQSchema(langQA[l]);
  h = h.replace(enSchema, langSchema);
  
  // Apply step-by-step translations
  const st = STEP_LABELS[l];
  for (const [en_st, loc_st] of Object.entries(st)) {
    h = h.replace(new RegExp('>'+en_st.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'<','g'), '>'+loc_st+'<');
  }
  
  // Nav
  if (l === 'es') {
    h = h.replace(/>Home<\/a>/g,'>Inicio</a>').replace(/>Tools<\/a>/g,'>Herramientas</a>').replace(/>About<\/a>/g,'>Acerca de</a>').replace(/>Contact<\/a>/g,'>Contacto</a>');
  } else if (l === 'pt') {
    h = h.replace(/>Home<\/a>/g,'>Início</a>').replace(/>Tools<\/a>/g,'>Ferramentas</a>').replace(/>About<\/a>/g,'>Sobre</a>').replace(/>Contact<\/a>/g,'>Contato</a>');
  } else if (l === 'id') {
    h = h.replace(/>Home<\/a>/g,'>Beranda</a>').replace(/>Tools<\/a>/g,'>Alat</a>').replace(/>About<\/a>/g,'>Tentang</a>').replace(/>Contact<\/a>/g,'>Kontak</a>');
  }
  
  // Footer
  const ft = FOOTER[l];
  h = h.replace(/Free AI-powered image tools that respect your privacy\./g, ft.free);
  h = h.replace(/All rights reserved\./g, ft.rights);
  
  fs.writeFileSync(path.join(dir, name+'.html'), h, 'utf8');
  console.log(l+' done');
});

console.log('\nDONE - verify files');
