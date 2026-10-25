/**
 * SmartImgKit - Result Modal & Viral Sharing Module
 * Self-contained: injects CSS + DOM, exposes openResultModal(resultData)
 * Dependencies: none (pure vanilla JS)
 */
(function() {
  'use strict';

  /* ===== Config ===== */
  var N8N_WEBHOOK_URL = ''; // Fill in during deployment
  var SITE_URL = 'https://smartimgkit.com';
  var EMBED_CODE =
    '<!-- Embed SmartImgKit image compressor on your site -->\n' +
    '<iframe src="https://smartimgkit.com" width="800" height="600" frameborder="0" title="SmartImgKit Image Tool"></iframe>\n' +
    'Source: <a href="https://smartimgkit.com">SmartImgKit.com</a>';

  /* ===== Tool-specific configs ===== */
  var TOOL_CONFIGS = {
    'background-remover': {
      title: '✅ Background Removed Successfully',
      stat1Label: 'Original',
      stat2Label: 'Processed',
      stat3Label: 'Quality',
      twitterText: 'I just removed the background from an image with SmartImgKit — free and no signup! Try it:',
      systemText: 'I just removed the background from an image with SmartImgKit!',
      reportHeader: '✅ Background Removal Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Output: ',
      reportLine4: 'Quality: ',
      fileName: 'no-background'
    },
    'image-upscaler': {
      title: '✅ Image Upscaled Successfully',
      stat1Label: 'Original',
      stat2Label: 'Upscaled',
      stat3Label: 'Scale',
      twitterText: 'I just upscaled an image with AI using SmartImgKit — sharper and bigger! Try it free:',
      systemText: 'I just upscaled an image with AI using SmartImgKit!',
      reportHeader: '✅ Image Upscaling Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Upscaled: ',
      reportLine4: 'Scale: ',
      fileName: 'upscaled-image'
    },
    'image-compressor': {
      title: '✅ Image Optimized Successfully',
      stat1Label: 'Original',
      stat2Label: 'Optimized',
      stat3Label: 'Saved',
      twitterText: 'I just optimized an image with SmartImgKit — saved ',
      systemText: 'I just optimized an image and saved ',
      reportHeader: '✅ Image Optimization Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Optimized: ',
      reportLine4: 'Saved: ',
      fileName: 'optimized-image'
    },
    'image-cropper': {
      title: '✅ Image Cropped Successfully',
      stat1Label: 'Original',
      stat2Label: 'Cropped',
      stat3Label: 'Aspect',
      twitterText: 'I just cropped an image perfectly with SmartImgKit — free and easy! Try it:',
      systemText: 'I just cropped an image with SmartImgKit!',
      reportHeader: '✅ Image Cropping Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Cropped: ',
      reportLine4: 'Aspect Ratio: ',
      fileName: 'cropped-image'
    },
    'image-resizer': {
      title: '✅ Image Resized Successfully',
      stat1Label: 'Original',
      stat2Label: 'Resized',
      stat3Label: 'Dimensions',
      twitterText: 'I just resized an image with SmartImgKit — perfect dimensions every time! Try it free:',
      systemText: 'I just resized an image with SmartImgKit!',
      reportHeader: '✅ Image Resizing Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Resized: ',
      reportLine4: 'Dimensions: ',
      fileName: 'resized-image'
    },
    'image-converter': {
      title: '✅ Image Converted Successfully',
      stat1Label: 'Original',
      stat2Label: 'Converted',
      stat3Label: 'Format',
      twitterText: 'I just converted an image format with SmartImgKit — fast and free! Try it:',
      systemText: 'I just converted an image format with SmartImgKit!',
      reportHeader: '✅ Image Conversion Complete\n',
      reportLine2: 'Original: ',
      reportLine3: 'Converted: ',
      reportLine4: 'Format: ',
      fileName: 'converted-image'
    },
    'watermark': {
      title: '✅ Watermark Added Successfully',
      stat1Label: 'Original',
      stat2Label: 'Watermarked',
      stat3Label: 'Protected',
      twitterText: 'I just added a watermark to protect my image with SmartImgKit! Try it free:',
      systemText: 'I just added a watermark to my image with SmartImgKit!',
      reportHeader: '✅ Watermark Added\n',
      reportLine2: 'Original: ',
      reportLine3: 'Watermarked: ',
      reportLine4: 'Status: Protected\n',
      fileName: 'watermarked-image'
    },
    'bulk-processor': {
      title: '✅ Bulk Processing Complete',
      stat1Label: 'Input',
      stat2Label: 'Output',
      stat3Label: 'Saved',
      twitterText: 'I just batch-processed images with SmartImgKit — saved so much time! Try it free:',
      systemText: 'I just batch-processed images with SmartImgKit!',
      reportHeader: '✅ Bulk Processing Complete\n',
      reportLine2: 'Input: ',
      reportLine3: 'Output: ',
      reportLine4: 'Saved: ',
      fileName: 'processed-images'
    }
  };

  /* ===== Default config (fallback) ===== */
  var DEFAULT_CONFIG = {
    title: '✅ Image Processed Successfully',
    stat1Label: 'Original',
    stat2Label: 'Processed',
    stat3Label: 'Result',
    twitterText: 'I just processed an image with SmartImgKit — free online image tools! Try it:',
    systemText: 'I just processed an image with SmartImgKit!',
    reportHeader: '✅ Image Processing Complete\n',
    reportLine2: 'Original: ',
    reportLine3: 'Processed: ',
    reportLine4: 'Result: ',
    fileName: 'processed-image'
  };

  /* ===== Locale detection & UI strings ===== */
  var LANG = (function() {
    var m = window.location.pathname.match(/^\/(vi|fr|es|ar|id|pt|zh)(?:\/|$)/);
    return m ? m[1] : 'en';
  })();

  var I18N = {
    en: {
      title: '✅ Image Processed Successfully',
      l1: 'Original',
      l2: 'Processed',
      l3: 'Saved',
      watermark: 'Add "Powered by SmartImgKit" watermark',
      download: '📥 Download Image',
      copyReport: '📋 Copy Report',
      share: 'Share:',
      genCompare: 'Generate comparison preview',
      embed: 'Embed code',
      copyEmbed: 'Copy embed code',
      tip: '💡 Tip: Bookmark SmartImgKit for quick access next time.',
      emailPh: '(Optional) Enter email for full report',
      submit: 'Submit',
      submitting: 'Submitting...',
      needEmail: 'Please enter an email address.',
      invalidEmail: 'Invalid email format. Please check and try again.',
      thanks: '✓ Thank you! Your report will be sent shortly.',
      failed: 'Submission failed, but your image download is not affected.',
      copied: '✓ Copied!',
      systemShareOnly: 'System share is only available on mobile devices.',
      compareUnavailable: 'Comparison preview unavailable (missing original image data).',
      downloadComparison: '📥 Download Comparison',
      before: 'Before',
      after: 'After',
      processedBy: 'Processed by SmartImgKit',
      reportHeader: '✅ Image Processing Complete\n',
      reportOrig: 'Original: ',
      reportOut: 'Processed: ',
      reportThird: 'Saved: ',
      twitter: 'I just processed an image with SmartImgKit — free online image tools! Try it:',
      system: 'I just processed an image with SmartImgKit!',
      close: 'Close dialog',
      previewAlt: 'Processed image preview',
    },
    vi: {
      title: '✅ Xử lý ảnh thành công',
      l1: 'Ảnh gốc',
      l2: 'Kết quả',
      l3: 'Đã giảm',
      watermark: 'Thêm watermark "Powered by SmartImgKit"',
      download: '📥 Tải ảnh xuống',
      copyReport: '📋 Sao chép báo cáo',
      share: 'Chia sẻ:',
      genCompare: 'Tạo ảnh so sánh trước–sau',
      embed: 'Mã nhúng',
      copyEmbed: 'Sao chép mã nhúng',
      tip: '💡 Mẹo: lưu SmartImgKit vào bookmark để mở nhanh lần sau.',
      emailPh: '(Tùy chọn) Nhập email để nhận báo cáo đầy đủ',
      submit: 'Gửi',
      submitting: 'Đang gửi...',
      needEmail: 'Vui lòng nhập địa chỉ email.',
      invalidEmail: 'Email không hợp lệ, vui lòng kiểm tra lại.',
      thanks: '✓ Cảm ơn bạn! Báo cáo sẽ được gửi trong ít phút.',
      failed: 'Gửi báo cáo thất bại, nhưng ảnh vẫn tải xuống bình thường.',
      copied: '✓ Đã sao chép!',
      systemShareOnly: 'Chia sẻ hệ thống chỉ dùng được trên điện thoại.',
      compareUnavailable: 'Không tạo được ảnh so sánh (thiếu dữ liệu ảnh gốc).',
      downloadComparison: '📥 Tải ảnh so sánh',
      before: 'Trước',
      after: 'Sau',
      processedBy: 'Xử lý bởi SmartImgKit',
      reportHeader: '✅ Đã xử lý ảnh xong\n',
      reportOrig: 'Ảnh gốc: ',
      reportOut: 'Kết quả: ',
      reportThird: 'Đã giảm: ',
      twitter: 'Mình vừa xử lý ảnh bằng SmartImgKit — bộ công cụ ảnh miễn phí chạy ngay trên trình duyệt:',
      system: 'Mình vừa xử lý ảnh bằng SmartImgKit!',
      close: 'Đóng hộp thoại',
      previewAlt: 'Ảnh kết quả',
    },
    fr: {
      title: '✅ Image traitée avec succès',
      l1: 'Original',
      l2: 'Résultat',
      l3: 'Gain',
      watermark: 'Ajouter le filigrane « Powered by SmartImgKit »',
      download: '📥 Télécharger l’image',
      copyReport: '📋 Copier le rapport',
      share: 'Partager :',
      genCompare: 'Générer un aperçu comparatif',
      embed: 'Code d’intégration',
      copyEmbed: 'Copier le code',
      tip: '💡 Astuce : ajoutez SmartImgKit à vos favoris pour le retrouver vite.',
      emailPh: '(Facultatif) E-mail pour recevoir le rapport complet',
      submit: 'Envoyer',
      submitting: 'Envoi...',
      needEmail: 'Merci de saisir une adresse e-mail.',
      invalidEmail: 'Format d’e-mail invalide, vérifiez et réessayez.',
      thanks: '✓ Merci ! Votre rapport part dans quelques instants.',
      failed: 'Envoi impossible, mais le téléchargement de votre image n’est pas affecté.',
      copied: '✓ Copié !',
      systemShareOnly: 'Le partage système n’est disponible que sur mobile.',
      compareUnavailable: 'Aperçu comparatif indisponible (image d’origine manquante).',
      downloadComparison: '📥 Télécharger la comparaison',
      before: 'Avant',
      after: 'Après',
      processedBy: 'Traité par SmartImgKit',
      reportHeader: '✅ Traitement terminé\n',
      reportOrig: 'Original : ',
      reportOut: 'Résultat : ',
      reportThird: 'Gain : ',
      twitter: 'Je viens de traiter une image avec SmartImgKit, des outils photo gratuits qui tournent dans le navigateur :',
      system: 'Je viens de traiter une image avec SmartImgKit !',
      close: 'Fermer la fenêtre',
      previewAlt: 'Aperçu du résultat',
    },
    es: {
      title: '✅ Imagen procesada correctamente',
      l1: 'Original',
      l2: 'Resultado',
      l3: 'Ahorro',
      watermark: 'Añadir marca de agua «Powered by SmartImgKit»',
      download: '📥 Descargar imagen',
      copyReport: '📋 Copiar informe',
      share: 'Compartir:',
      genCompare: 'Generar vista comparativa',
      embed: 'Código para insertar',
      copyEmbed: 'Copiar código',
      tip: '💡 Consejo: guarda SmartImgKit en marcadores para volver rápido.',
      emailPh: '(Opcional) Escribe tu email para recibir el informe completo',
      submit: 'Enviar',
      submitting: 'Enviando...',
      needEmail: 'Escribe una dirección de email.',
      invalidEmail: 'El formato del email no es válido, revísalo e inténtalo otra vez.',
      thanks: '✓ ¡Gracias! Te enviaremos el informe en breve.',
      failed: 'No se pudo enviar, pero la descarga de tu imagen no se ve afectada.',
      copied: '✓ ¡Copiado!',
      systemShareOnly: 'Compartir del sistema solo está disponible en móviles.',
      compareUnavailable: 'Vista comparativa no disponible (falta la imagen original).',
      downloadComparison: '📥 Descargar comparación',
      before: 'Antes',
      after: 'Después',
      processedBy: 'Procesado con SmartImgKit',
      reportHeader: '✅ Procesamiento completado\n',
      reportOrig: 'Original: ',
      reportOut: 'Resultado: ',
      reportThird: 'Ahorro: ',
      twitter: 'Acabo de procesar una imagen con SmartImgKit, herramientas de foto gratis en el navegador:',
      system: '¡Acabo de procesar una imagen con SmartImgKit!',
      close: 'Cerrar diálogo',
      previewAlt: 'Vista previa del resultado',
    },
    pt: {
      title: '✅ Imagem processada com sucesso',
      l1: 'Original',
      l2: 'Resultado',
      l3: 'Economia',
      watermark: 'Adicionar marca d’água "Powered by SmartImgKit"',
      download: '📥 Baixar imagem',
      copyReport: '📋 Copiar relatório',
      share: 'Compartilhar:',
      genCompare: 'Gerar prévia comparativa',
      embed: 'Código de incorporação',
      copyEmbed: 'Copiar código',
      tip: '💡 Dica: salve o SmartImgKit nos favoritos para voltar depois.',
      emailPh: '(Opcional) Digite seu e-mail para receber o relatório completo',
      submit: 'Enviar',
      submitting: 'Enviando...',
      needEmail: 'Digite um endereço de e-mail.',
      invalidEmail: 'Formato de e-mail inválido, confira e tente de novo.',
      thanks: '✓ Obrigado! O relatório será enviado em instantes.',
      failed: 'Não foi possível enviar, mas o download da imagem não foi afetado.',
      copied: '✓ Copiado!',
      systemShareOnly: 'O compartilhamento do sistema só funciona no celular.',
      compareUnavailable: 'Prévia comparativa indisponível (imagem original ausente).',
      downloadComparison: '📥 Baixar comparação',
      before: 'Antes',
      after: 'Depois',
      processedBy: 'Processado com SmartImgKit',
      reportHeader: '✅ Processamento concluído\n',
      reportOrig: 'Original: ',
      reportOut: 'Resultado: ',
      reportThird: 'Economia: ',
      twitter: 'Acabei de processar uma imagem com o SmartImgKit, ferramentas de foto grátis no navegador:',
      system: 'Acabei de processar uma imagem com o SmartImgKit!',
      close: 'Fechar janela',
      previewAlt: 'Prévia do resultado',
    },
    id: {
      title: '✅ Gambar berhasil diproses',
      l1: 'Asli',
      l2: 'Hasil',
      l3: 'Hemat',
      watermark: 'Tambahkan tanda air "Powered by SmartImgKit"',
      download: '📥 Unduh gambar',
      copyReport: '📋 Salin laporan',
      share: 'Bagikan:',
      genCompare: 'Buat pratinjau perbandingan',
      embed: 'Kode semat',
      copyEmbed: 'Salin kode',
      tip: '💡 Tips: simpan SmartImgKit di bookmark agar cepat dibuka lagi.',
      emailPh: '(Opsional) Masukkan email untuk laporan lengkap',
      submit: 'Kirim',
      submitting: 'Mengirim...',
      needEmail: 'Masukkan alamat email.',
      invalidEmail: 'Format email tidak valid, periksa lagi.',
      thanks: '✓ Terima kasih! Laporan akan dikirim sebentar lagi.',
      failed: 'Gagal mengirim, tetapi unduhan gambar Anda tetap aman.',
      copied: '✓ Tersalin!',
      systemShareOnly: 'Bagikan sistem hanya tersedia di ponsel.',
      compareUnavailable: 'Pratinjau perbandingan tidak tersedia (gambar asli tidak ada).',
      downloadComparison: '📥 Unduh perbandingan',
      before: 'Sebelum',
      after: 'Sesudah',
      processedBy: 'Diproses dengan SmartImgKit',
      reportHeader: '✅ Pemrosesan selesai\n',
      reportOrig: 'Asli: ',
      reportOut: 'Hasil: ',
      reportThird: 'Hemat: ',
      twitter: 'Baru saja memproses gambar dengan SmartImgKit, alat foto gratis di browser:',
      system: 'Baru saja memproses gambar dengan SmartImgKit!',
      close: 'Tutup dialog',
      previewAlt: 'Pratinjau hasil',
    },
    ar: {
      title: '✅ تمت معالجة الصورة بنجاح',
      l1: 'الأصل',
      l2: 'النتيجة',
      l3: 'التوفير',
      watermark: 'إضافة علامة مائية "Powered by SmartImgKit"',
      download: '📥 تنزيل الصورة',
      copyReport: '📋 نسخ التقرير',
      share: 'مشاركة:',
      genCompare: 'إنشاء معاينة مقارنة',
      embed: 'كود التضمين',
      copyEmbed: 'نسخ كود التضمين',
      tip: '💡 نصيحة: أضف SmartImgKit إلى المفضلة للعودة سريعًا.',
      emailPh: '(اختياري) أدخل بريدك لاستلام التقرير الكامل',
      submit: 'إرسال',
      submitting: 'جارٍ الإرسال...',
      needEmail: 'يرجى إدخال عنوان بريد إلكتروني.',
      invalidEmail: 'صيغة البريد غير صحيحة، تحقق منها ثم أعد المحاولة.',
      thanks: '✓ شكرًا لك! سيصل التقرير بعد قليل.',
      failed: 'تعذّر الإرسال، لكن تنزيل صورتك لم يتأثر.',
      copied: '✓ تم النسخ!',
      systemShareOnly: 'المشاركة عبر النظام متاحة على الهاتف فقط.',
      compareUnavailable: 'المعاينة المقارنة غير متاحة (الصورة الأصلية مفقودة).',
      downloadComparison: '📥 تنزيل المقارنة',
      before: 'قبل',
      after: 'بعد',
      processedBy: 'معالجة بواسطة SmartImgKit',
      reportHeader: '✅ اكتملت المعالجة\n',
      reportOrig: 'الأصل: ',
      reportOut: 'النتيجة: ',
      reportThird: 'التوفير: ',
      twitter: 'عالجت صورة للتو باستخدام SmartImgKit، أدوات صور مجانية تعمل داخل المتصفح:',
      system: 'عالجت صورة للتو باستخدام SmartImgKit!',
      close: 'إغلاق النافذة',
      previewAlt: 'معاينة النتيجة',
    },
    zh: {
      title: '✅ 图片处理完成',
      l1: '原图',
      l2: '结果',
      l3: '已减小',
      watermark: '添加「Powered by SmartImgKit」水印',
      download: '📥 下载图片',
      copyReport: '📋 复制报告',
      share: '分享：',
      genCompare: '生成前后对比图',
      embed: '嵌入代码',
      copyEmbed: '复制嵌入代码',
      tip: '💡 小提示：把 SmartImgKit 加入书签，下次打开更快。',
      emailPh: '（可选）填写邮箱以接收完整报告',
      submit: '提交',
      submitting: '提交中...',
      needEmail: '请填写邮箱地址。',
      invalidEmail: '邮箱格式不正确，请检查后重试。',
      thanks: '✓ 谢谢！报告稍后会发送给你。',
      failed: '提交失败，但不会影响图片下载。',
      copied: '✓ 已复制！',
      systemShareOnly: '系统分享仅在手机上可用。',
      compareUnavailable: '无法生成对比图（缺少原图数据）。',
      downloadComparison: '📥 下载对比图',
      before: '处理前',
      after: '处理后',
      processedBy: '由 SmartImgKit 处理',
      reportHeader: '✅ 图片处理完成\n',
      reportOrig: '原图：',
      reportOut: '结果：',
      reportThird: '已减小：',
      twitter: '我刚用 SmartImgKit 处理了一张图片，免费在线图片工具，直接在浏览器里完成：',
      system: '我刚用 SmartImgKit 处理了一张图片！',
      close: '关闭对话框',
      previewAlt: '处理结果预览',
    },
  };

  function T(key) {
    var pack = I18N[LANG] || I18N.en;
    return (pack[key] !== undefined) ? pack[key] : (I18N.en[key] || '');
  }

  /* ===== Detect tool type from URL ===== */
  function detectToolType() {
    try {
      var path = window.location.pathname;
      // Match /tools/xxx or /xx/tools/xxx (language prefix)
      var match = path.match(/\/tools\/([a-z0-9-]+)/i);
      if (match) return match[1].toLowerCase();
      // Match /xxx/tools/xxx (e.g., /es/tools/background-remover)
      var match2 = path.match(/\/[a-z]{2}\/tools\/([a-z0-9-]+)/i);
      if (match2) return match2[1].toLowerCase();
    } catch(e) {}
    return '';
  }

  /* ===== Get tool config ===== */
  function getToolConfig(toolType) {
    toolType = toolType || detectToolType();
    var base = TOOL_CONFIGS[toolType] || DEFAULT_CONFIG;
    if (LANG === 'en') return base;
    // 非英语：标题/统计标签/分享文案/报告行按本语种界面包重写，文件名沿用工具配置
    return {
      title: T('title'),
      stat1Label: T('l1'),
      stat2Label: T('l2'),
      stat3Label: T('l3'),
      twitterText: T('twitter'),
      systemText: T('system'),
      reportHeader: T('reportHeader'),
      reportLine2: T('reportOrig'),
      reportLine3: T('reportOut'),
      reportLine4: T('reportThird'),
      fileName: base.fileName
    };
  }

  /* ===== State ===== */
  var state = {
    origSize: '',
    optSize: '',
    saveRate: '',
    originalBlob: null,
    resultBlob: null,
    resultUrl: null,
    watermarkOn: false,
    fileName: 'optimized-image'
  };

  /* ===== GA4 Helper ===== */
  function track(eventName, params) {
    params = params || {};
    try {
      if (typeof gtag === 'function') {
        gtag('event', eventName, params);
      } else if (window.dataLayer) {
        window.dataLayer.push({ event: eventName, event_params: params });
      }
    } catch(e) {}
  }

  /* ===== Inject CSS (self-contained, no external dependency) ===== */
  function injectCSS() {
    if (document.getElementById('result-modal-css')) return;
    var style = document.createElement('style');
    style.id = 'result-modal-css';
    style.textContent = `
.result-modal-overlay{display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);align-items:center;justify-content:center;padding:16px;}
.result-modal-overlay.open{display:flex;}
.result-modal{background:var(--bg-card,#fff);border:1px solid var(--border-color,#e2e4ea);border-radius:16px;max-width:520px;width:100%;max-height:90vh;overflow-y:auto;position:relative;box-shadow:0 8px 40px rgba(0,0,0,.3);}
.result-modal-close{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:50%;background:var(--bg-tertiary,#f0f1f5);border:1px solid var(--border-color,#e2e4ea);font-size:1.3rem;color:var(--text-secondary,#5a5a6e);cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1;z-index:2;}
.result-modal-close:hover{background:var(--bg-card-hover,#e8e9ee);}
.result-modal-body{padding:32px 24px 24px;}
.result-modal-body h2{font-size:1.3rem;font-weight:700;margin-bottom:16px;text-align:center;color:var(--text-primary,#1a1a2e);}
.result-preview{background:var(--bg-secondary,#f8f9fb);border-radius:12px;padding:16px;text-align:center;margin-bottom:20px;}
.result-preview img{max-width:100%;max-height:240px;border-radius:8px;}
.result-stats{display:flex;justify-content:space-around;gap:8px;margin-bottom:24px;flex-wrap:wrap;}
.stat-item{text-align:center;flex:1;min-width:90px;}
.stat-label{display:block;font-size:.75rem;color:var(--text-muted,#9a9aaa);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;}
.stat-value{display:block;font-size:1.1rem;font-weight:700;color:var(--text-primary,#1a1a2e);}
.stat-saved .stat-value{color:var(--success,#16a34a);}
.result-actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:20px;}
.rm-btn{padding:10px 20px;border-radius:10px;font-weight:600;font-size:.9rem;cursor:pointer;border:none;transition:all .25s cubic-bezier(.4,0,.2,1);display:inline-flex;align-items:center;gap:6px;}
.rm-btn-primary{background:linear-gradient(135deg,var(--gradient-from,#4f46e5),var(--gradient-to,#7c3aed));color:#fff;box-shadow:0 4px 20px var(--accent-glow,rgba(79,70,229,.15));}
.rm-btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 28px var(--accent-glow,rgba(79,70,229,.2));}
.rm-btn-secondary{background:var(--bg-tertiary,#f0f1f5);color:var(--text-primary,#1a1a2e);border:1px solid var(--border-color,#e2e4ea);}
.rm-btn-secondary:hover{background:var(--bg-card-hover,#e8e9ee);}
.result-share-section{display:flex;align-items:center;gap:10px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}
.share-label{font-size:.85rem;color:var(--text-secondary,#5a5a6e);font-weight:500;}
.share-btn{width:38px;height:38px;border-radius:50%;background:var(--bg-tertiary,#f0f1f5);border:1px solid var(--border-color,#e2e4ea);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .25s;}
.share-btn:hover{background:var(--accent,#4f46e5);color:#fff;border-color:var(--accent,#4f46e5);}
.result-toggle-row{display:flex;align-items:center;gap:8px;justify-content:center;margin-bottom:20px;}
.result-toggle-row label{font-size:.82rem;color:var(--text-secondary,#5a5a6e);cursor:pointer;}
.result-toggle-row input{cursor:pointer;}
.result-email-row{display:flex;gap:8px;margin-bottom:16px;}
.result-email-row input{flex:1;padding:10px 12px;border-radius:10px;border:1px solid var(--border-color,#e2e4ea);background:var(--bg-secondary,#f8f9fb);color:var(--text-primary,#1a1a2e);font-size:.85rem;font-family:inherit;}
.result-email-row input:focus{outline:none;border-color:var(--accent,#4f46e5);}
.result-email-row input::placeholder{color:var(--text-muted,#9a9aaa);}
.email-feedback{font-size:.8rem;text-align:center;margin-bottom:12px;min-height:18px;}
.email-feedback.success{color:var(--success,#16a34a);}
.email-feedback.error{color:#ef4444;}
.result-embed{background:var(--bg-secondary,#f8f9fb);border:1px solid var(--border-color,#e2e4ea);border-radius:10px;padding:12px;margin-bottom:16px;}
.result-embed summary{cursor:pointer;font-size:.82rem;color:var(--text-secondary,#5a5a6e);font-weight:500;outline:none;}
.result-embed summary:hover{color:var(--text-primary,#1a1a2e);}
.result-embed pre{margin:8px 0 8px;white-space:pre-wrap;word-break:break-all;font-size:.75rem;color:var(--text-secondary,#5a5a6e);font-family:'Courier New',monospace;}
.result-embed-copy{width:100%;padding:8px;border-radius:8px;font-size:.82rem;}
.result-email-section{margin-bottom:16px;}
.result-tip{font-size:.82rem;color:var(--text-muted,#9a9aaa);text-align:center;margin-top:12px;}
.result-compare-preview{margin-top:12px;text-align:center;display:none;}
.result-compare-preview img{max-width:100%;border-radius:8px;margin-top:8px;}
@media(max-width:520px){
  .result-modal-body{padding:24px 16px 16px;}
  .result-stats{flex-direction:column;gap:8px;}
  .result-actions{flex-direction:column;}
  .rm-btn{width:100%;justify-content:center;}
  .result-email-row{flex-direction:column;}
}
`;
    document.head.appendChild(style);
  }

  /* ===== Build modal DOM ===== */
  function buildModal() {
    if (document.getElementById('resultModalOverlay')) return;

    var overlay = document.createElement('div');
    overlay.className = 'result-modal-overlay';
    overlay.id = 'resultModalOverlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'resultModalTitle');
    overlay.innerHTML = `
      <div class="result-modal" role="document">
        <button class="result-modal-close" id="resultModalClose" aria-label="${T('close')}">&times;</button>
        <div class="result-modal-body">
          <h2 id="resultModalTitle">${T('title')}</h2>
          <div class="result-preview">
            <img id="resultPreviewImg" alt="${T('previewAlt')}" />
          </div>
          <div class="result-stats">
            <div class="stat-item"><span class="stat-label">${T('l1')}</span><span class="stat-value" id="statOrigSize" dir="ltr">-</span></div>
            <div class="stat-item"><span class="stat-label">${T('l2')}</span><span class="stat-value" id="statOptSize" dir="ltr">-</span></div>
            <div class="stat-item stat-saved"><span class="stat-label">${T('l3')}</span><span class="stat-value" id="statSaveRate" dir="ltr">-</span></div>
          </div>
          <div class="result-toggle-row">
            <label><input type="checkbox" id="rmWatermarkToggle" /> ${T('watermark')}</label>
          </div>
          <div class="result-actions">
            <button class="rm-btn rm-btn-primary" id="rmDownloadBtn">${T('download')}</button>
            <button class="rm-btn rm-btn-secondary" id="rmCopyReportBtn">${T('copyReport')}</button>
          </div>
          <div class="result-share-section">
            <span class="share-label">${T('share')}</span>
            <button class="share-btn" id="rmShareTwitter" title="X (Twitter)" aria-label="X (Twitter)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></button>
            <button class="share-btn" id="rmShareFacebook" title="Facebook" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.404 0 .763.008 1.107.022v3.36c-.43-.005-.752-.013-1.052-.013-1.35 0-1.872.617-1.872 2.264v1.925h3.287l-.706 3.667h-2.581v8.061c5.376-.608 9.562-5.218 9.562-10.769C22.061 5.679 17.382 1 12 1S1.939 5.679 1.939 11.7c0 5.551 4.186 10.161 9.562 10.769z"/></svg></button>
            <button class="share-btn" id="rmShareSystem" title="Share" aria-label="Share"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/></svg></button>
          </div>
          <div class="result-compare-preview" id="rmComparePreview">
            <button class="rm-btn rm-btn-secondary" id="rmGenerateCompareBtn">${T('genCompare')}</button>
            <div id="rmCompareImageContainer"></div>
          </div>
          <div class="result-email-section" id="rmEmailSection">
            <div class="result-email-row">
              <input type="email" id="rmEmailInput" placeholder="${T('emailPh')}" />
              <button class="rm-btn rm-btn-secondary" id="rmEmailSubmit">${T('submit')}</button>
            </div>
            <div class="email-feedback" id="rmEmailFeedback"></div>
          </div>
          <details class="result-embed">
            <summary>${T('embed')}</summary>
            <pre id="rmEmbedCode"></pre>
            <button class="rm-btn rm-btn-secondary result-embed-copy" id="rmCopyEmbedBtn">${T('copyEmbed')}</button>
          </details>
          <p class="result-tip">${T('tip')}</p>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    bindEvents();
  }

  /* ===== Apply watermark to a canvas ===== */
  function applyWatermark(canvas) {
    var ctx = canvas.getContext('2d');
    var fontSize = Math.max(10, Math.round(canvas.width * 0.018));
    ctx.font = fontSize + 'px Inter, Arial, sans-serif';
    ctx.fillStyle = 'rgba(128,128,128,0.25)';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'bottom';
    ctx.fillText('Powered by SmartImgKit', canvas.width - 8, canvas.height - 8);
  }

  /* ===== Download image (with optional watermark) ===== */
  function downloadResult() {
    if (!state.resultBlob) return;
    track('download_image', { file_size: state.optSize });

    if (state.watermarkOn) {
      // Redraw with watermark
      var img = new Image();
      img.onload = function() {
        var canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        applyWatermark(canvas);
        canvas.toBlob(function(wmBlob) {
          if (window.SmartImgKit && SmartImgKit._downloadBlob) {
            SmartImgKit._downloadBlob(wmBlob, state.fileName, state.resultBlob.type);
          } else {
            var url = URL.createObjectURL(wmBlob);
            var a = document.createElement('a');
            a.href = url; a.download = state.fileName;
            a.click();
            setTimeout(function() { URL.revokeObjectURL(url); }, 4000);
          }
        }, state.resultBlob.type || 'image/png');
      };
      img.src = state.resultUrl;
    } else {
      if (window.SmartImgKit && SmartImgKit._downloadBlob) {
        SmartImgKit._downloadBlob(state.resultBlob, state.fileName, state.resultBlob.type);
      } else {
        var url = URL.createObjectURL(state.resultBlob);
        var a = document.createElement('a');
        a.href = url; a.download = state.fileName;
        a.click();
        setTimeout(function() { URL.revokeObjectURL(url); }, 4000);
      }
    }
  }

  /* ===== Copy report text ===== */
  function copyReport() {
    var config = state.currentToolConfig || getToolConfig();
    var text =
      config.reportHeader +
      config.reportLine2 + state.origSize + '\n' +
      config.reportLine3 + state.optSize + '\n' +
      config.reportLine4 + state.saveRate + '\n\n' +
      T('processedBy') + '\n' +
      SITE_URL;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        track('copy_report', {});
        flashButton('rmCopyReportBtn', T('copied'));
      }).catch(function() { fallbackCopy(text); });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); track('copy_report', {}); flashButton('rmCopyReportBtn', T('copied')); }
    catch(e) {}
    document.body.removeChild(ta);
  }

  function flashButton(btnId, text) {
    var btn = document.getElementById(btnId);
    if (!btn) return;
    var orig = btn.textContent;
    btn.textContent = text;
    btn.disabled = true;
    setTimeout(function() { btn.textContent = orig; btn.disabled = false; }, 2000);
  }

  /* ===== Share ===== */
  function shareTwitter() {
    track('click_share', { platform: 'twitter' });
    var config = state.currentToolConfig || getToolConfig();
    var shareText = config.twitterText;
    // For compressor, append save rate
    if (config === TOOL_CONFIGS['image-compressor'] && state.saveRate && state.saveRate !== '-') {
      shareText += state.saveRate + '! Try it free:';
    }
    var text = encodeURIComponent(shareText);
    var url = 'https://twitter.com/intent/tweet?text=' + text + '&url=' + encodeURIComponent(SITE_URL);
    window.open(url, '_blank', 'noopener');
  }

  function shareFacebook() {
    track('click_share', { platform: 'facebook' });
    var url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(SITE_URL);
    window.open(url, '_blank', 'noopener');
  }

  function shareSystem() {
    track('click_share', { platform: 'system' });
    var config = state.currentToolConfig || getToolConfig();
    var shareText = config.systemText;
    // For compressor, append save rate
    if (config === TOOL_CONFIGS['image-compressor'] && state.saveRate && state.saveRate !== '-') {
      shareText += state.saveRate + '!';
    }
    if (navigator.share) {
      navigator.share({
        title: 'SmartImgKit — Free Image Tools',
        text: shareText,
        url: SITE_URL
      }).catch(function() {});
    } else {
      showToast(T('systemShareOnly'));
    }
  }

  /* ===== Toast notification (replaces alert) ===== */
  function showToast(message) {
    var toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--bg-tertiary,#333);color:var(--text-primary,#fff);padding:12px 24px;border-radius:8px;font-size:.85rem;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.3);opacity:0;transition:opacity .3s;border:1px solid var(--border-color,#555);';
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(function() { toast.style.opacity = '1'; });
    setTimeout(function() {
      toast.style.opacity = '0';
      setTimeout(function() { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 300);
    }, 3000);
  }

  /* ===== Generate comparison preview ===== */
  function generateComparePreview() {
    track('generate_compare_preview', {});

    if (!state.originalBlob || !state.resultBlob) {
      var container = document.getElementById('rmCompareImageContainer');
      container.innerHTML = '<p style="font-size:.8rem;color:var(--text-muted);">' + T('compareUnavailable') + '</p>';
      return;
    }

    var origImg = new Image();
    var resultImg = new Image();
    var loaded = 0;

    function tryCompose() {
      loaded++;
      if (loaded < 2) return;

      var gap = 4;
      var maxH = 300;
      var origRatio = maxH / origImg.naturalHeight;
      var resultRatio = maxH / resultImg.naturalHeight;
      var w1 = Math.round(origImg.naturalWidth * origRatio);
      var w2 = Math.round(resultImg.naturalWidth * resultRatio);
      var h = maxH;

      var canvas = document.createElement('canvas');
      canvas.width = w1 + gap + w2;
      canvas.height = h + 28; // extra space for label
      var ctx = canvas.getContext('2d');

      // Background
      ctx.fillStyle = '#f8f9fb';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Original (left)
      ctx.drawImage(origImg, 0, 0, w1, h);
      // Optimized (right)
      ctx.drawImage(resultImg, w1 + gap, 0, w2, h);

      // Labels
      ctx.font = 'bold 11px Inter, Arial, sans-serif';
      ctx.fillStyle = '#5a5a6e';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText(T('before'), 6, h + 6);
      ctx.fillText(T('after'), w1 + gap + 6, h + 6);

      // Watermark
      ctx.font = '10px Inter, Arial, sans-serif';
      ctx.fillStyle = 'rgba(128,128,128,0.3)';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'bottom';
      ctx.fillText('Powered by SmartImgKit', canvas.width - 6, canvas.height - 4);

      var dataUrl = canvas.toDataURL('image/png');
      var container = document.getElementById('rmCompareImageContainer');
      container.innerHTML =
        '<img src="' + dataUrl + '" alt="' + T('before') + ' / ' + T('after') + '" style="border-radius:8px;" />' +
        '<div style="margin-top:8px;"><a href="' + dataUrl + '" download="smartimgkit-comparison.png" class="rm-btn rm-btn-secondary" style="display:inline-flex;text-decoration:none;">' + T('downloadComparison') + '</a></div>';
    }

    origImg.onload = tryCompose;
    resultImg.onload = tryCompose;
    origImg.src = URL.createObjectURL(state.originalBlob);
    resultImg.src = state.resultUrl;
  }

  /* ===== Email submit ===== */
  function submitEmail() {
    var input = document.getElementById('rmEmailInput');
    var feedback = document.getElementById('rmEmailFeedback');
    var email = input.value.trim();

    if (!email) {
      feedback.className = 'email-feedback error';
      feedback.textContent = T('needEmail');
      return;
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      feedback.className = 'email-feedback error';
      feedback.textContent = T('invalidEmail');
      return;
    }

    function getUtmParam(name) {
      var params = new URLSearchParams(window.location.search);
      return params.get(name) || '';
    }

    var payload = {
      email: email,
      timestamp: new Date().toISOString(),
      source: window.location.href,
      origSize: state.origSize,
      optSize: state.optSize,
      savePercent: state.saveRate,
      utm_source: getUtmParam('utm_source')
    };

    var submitBtn = document.getElementById('rmEmailSubmit');
    submitBtn.disabled = true;
    submitBtn.textContent = T('submitting');

    if (!N8N_WEBHOOK_URL) {
      // Webhook not configured — simulate success but log warning
      console.warn('[SmartImgKit] N8N_WEBHOOK_URL not configured. Email not submitted.');
      track('email_submit', { status: 'no_webhook' });
      feedback.className = 'email-feedback success';
      feedback.textContent = T('thanks');
      input.value = '';
      submitBtn.disabled = false;
      submitBtn.textContent = T('submit');
      return;
    }

    fetch(N8N_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function(res) {
      if (res.ok) {
        track('email_submit', { status: 'success' });
        feedback.className = 'email-feedback success';
        feedback.textContent = T('thanks');
        input.value = '';
      } else {
        throw new Error('HTTP ' + res.status);
      }
    }).catch(function(err) {
      track('email_submit', { status: 'error' });
      feedback.className = 'email-feedback error';
      feedback.textContent = T('failed');
    }).finally(function() {
      submitBtn.disabled = false;
      submitBtn.textContent = T('submit');
    });
  }

  /* ===== Copy embed code ===== */
  function copyEmbedCode() {
    var code = EMBED_CODE;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(function() {
        track('copy_embed_code', {});
        flashButton('rmCopyEmbedBtn', T('copied'));
      }).catch(function() { fallbackCopyEmbed(code); });
    } else {
      fallbackCopyEmbed(code);
    }
  }

  function fallbackCopyEmbed(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); track('copy_embed_code', {}); flashButton('rmCopyEmbedBtn', T('copied')); } catch(e) {}
    document.body.removeChild(ta);
  }

  /* ===== Close modal ===== */
  function closeModal() {
    var overlay = document.getElementById('resultModalOverlay');
    if (overlay) overlay.classList.remove('open');
    // Revoke object URL to free memory
    if (state.resultUrl) {
      URL.revokeObjectURL(state.resultUrl);
      state.resultUrl = null;
    }
  }

  /* ===== Bind events ===== */
  function bindEvents() {
    document.getElementById('resultModalClose').addEventListener('click', closeModal);
    document.getElementById('resultModalOverlay').addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        var overlay = document.getElementById('resultModalOverlay');
        if (overlay && overlay.classList.contains('open')) closeModal();
      }
    });
    document.getElementById('rmDownloadBtn').addEventListener('click', downloadResult);
    document.getElementById('rmCopyReportBtn').addEventListener('click', copyReport);
    document.getElementById('rmShareTwitter').addEventListener('click', shareTwitter);
    document.getElementById('rmShareFacebook').addEventListener('click', shareFacebook);
    document.getElementById('rmShareSystem').addEventListener('click', shareSystem);
    document.getElementById('rmEmailSubmit').addEventListener('click', submitEmail);
    document.getElementById('rmCopyEmbedBtn').addEventListener('click', copyEmbedCode);
    document.getElementById('rmGenerateCompareBtn').addEventListener('click', generateComparePreview);

    var wmToggle = document.getElementById('rmWatermarkToggle');
    wmToggle.addEventListener('change', function() {
      state.watermarkOn = wmToggle.checked;
    });
  }

  /* ===== Format bytes ===== */
  function formatBytes(bytes) {
    if (!bytes) return '0 B';
    if (typeof bytes === 'string') return bytes; // already formatted
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(2) + ' MB';
  }

  /* ===== Public API: openResultModal ===== */
  window.openResultModal = function(data) {
    injectCSS();
    buildModal();

    // Build embed code with current page URL (not generic homepage)
    var pageUrl = window.location.origin + window.location.pathname;
    var toolName = document.title.split('—')[0].trim() || 'SmartImgKit Tool';
    var dynamicEmbedCode =
      '<!-- Embed ' + toolName + ' on your site -->\n' +
      '<iframe src="' + pageUrl + '" width="800" height="600" frameborder="0" title="' + toolName + '"></iframe>\n' +
      'Source: <a href="' + pageUrl + '">SmartImgKit.com</a>';

    // Update state
    state.origSize = data.origSize ? (typeof data.origSize === 'string' ? data.origSize : formatBytes(data.origSize)) : '-';
    state.optSize = data.optSize ? (typeof data.optSize === 'string' ? data.optSize : formatBytes(data.optSize)) : '-';
    state.saveRate = data.saveRate || '-';
    state.originalBlob = data.originalBlob || null;
    state.resultBlob = data.resultBlob || null;
    state.watermarkOn = false; // always reset to OFF

    // Get tool config for default file name
    var toolConfigForName = getToolConfig(data.toolType);
    state.fileName = data.fileName || toolConfigForName.fileName || 'processed-image';

    // Determine extension
    if (state.resultBlob && state.resultBlob.type) {
      var extMap = { 'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp', 'image/gif': '.gif', 'image/bmp': '.bmp' };
      var ext = extMap[state.resultBlob.type] || '.png';
      if (state.fileName.indexOf('.') === -1) state.fileName += ext;
    }

    // Create object URL for preview
    if (state.resultUrl) URL.revokeObjectURL(state.resultUrl);
    state.resultUrl = state.resultBlob ? URL.createObjectURL(state.resultBlob) : null;

    // Populate UI
    var previewImg = document.getElementById('resultPreviewImg');
    if (state.resultUrl) {
      previewImg.src = state.resultUrl;
      previewImg.style.display = 'block';
    } else {
      previewImg.style.display = 'none';
    }

    // Get tool-specific config
    var toolConfig = getToolConfig(data.toolType);
    state.currentToolConfig = toolConfig;

    // Dynamic title and stats based on tool type
    document.getElementById('resultModalTitle').textContent = toolConfig.title;

    // Update stat labels
    var statLabels = document.querySelectorAll('.result-stats .stat-label');
    if (statLabels.length >= 3) {
      statLabels[0].textContent = toolConfig.stat1Label;
      statLabels[1].textContent = toolConfig.stat2Label;
      statLabels[2].textContent = toolConfig.stat3Label;
    }

    document.getElementById('statOrigSize').textContent = state.origSize;
    document.getElementById('statOptSize').textContent = state.optSize;
    document.getElementById('statSaveRate').textContent = state.saveRate;

    // Reset watermark toggle
    var wmToggle = document.getElementById('rmWatermarkToggle');
    if (wmToggle) wmToggle.checked = false;

    // Reset email
    var emailInput = document.getElementById('rmEmailInput');
    if (emailInput) emailInput.value = '';
    var emailFeedback = document.getElementById('rmEmailFeedback');
    if (emailFeedback) { emailFeedback.textContent = ''; emailFeedback.className = 'email-feedback'; }

    // Embed code (dynamic per page)
    document.getElementById('rmEmbedCode').textContent = dynamicEmbedCode;

    // Hide email section if webhook not configured
    var emailSection = document.getElementById('rmEmailSection');
    if (emailSection) {
      emailSection.style.display = N8N_WEBHOOK_URL ? 'block' : 'none';
    }

    // Hide system share button on desktop (progressive enhancement)
    if (!navigator.share) {
      var sysBtn = document.getElementById('rmShareSystem');
      if (sysBtn) sysBtn.style.display = 'none';
    }

    // Focus management for accessibility
    var closeBtn = document.getElementById('resultModalClose');
    if (closeBtn) closeBtn.focus();

    // Reset compare preview
    var compareContainer = document.getElementById('rmCompareImageContainer');
    if (compareContainer) compareContainer.innerHTML = '';
    var compareSection = document.getElementById('rmComparePreview');
    if (compareSection) compareSection.style.display = (state.originalBlob && state.resultBlob) ? 'block' : 'none';

    // Show modal
    document.getElementById('resultModalOverlay').classList.add('open');
  };

  // Also expose under SmartImgKit namespace
  window.SmartImgKit = window.SmartImgKit || {};
  SmartImgKit.openResultModal = window.openResultModal;

  /* ===== Auto-hook: capture result blobs via monkey-patch =====
   * Strategy: many tool pages store processed result as a local variable
   * (const blob, convertedBlob, etc.) which is unreachable from outside.
   * We monkey-patch URL.createObjectURL to capture the most recent blob
   * (which is typically the processed result). When a result blob is captured,
   * we auto-trigger the modal once per session.
   */
  var _lastResultBlob = null;
  var _lastOriginalFile = null;
  var _modalShownForSession = false; // avoid spamming within one session
  var _captureIgnoreUntil = 0; // timestamp; ignore captures before this time

  function _tryCaptureOriginal() {
    try { if (typeof currentFile !== 'undefined' && currentFile) { _lastOriginalFile = currentFile; return; } } catch(e) {}
    try { if (typeof originalFile !== 'undefined' && originalFile) { _lastOriginalFile = originalFile; return; } } catch(e) {}
    try { if (typeof origFile !== 'undefined' && origFile) { _lastOriginalFile = origFile; return; } } catch(e) {}
    try {
      if (typeof files !== 'undefined' && files && files.length === 1 && files[0]) {
        _lastOriginalFile = files[0].file || files[0];
        return;
      }
    } catch(e) {}
  }

  function _triggerModalFromCapture() {
    if (_modalShownForSession) return; // only once per session
    if (!_lastResultBlob) return;
    _tryCaptureOriginal();

    var _rb = _lastResultBlob;
    var _of = _lastOriginalFile;
    var _origSize = (_of && _of.size) ? _of.size : 0;
    var _optSize = _rb.size || 0;
    var _saveRate = '0%';
    if (_origSize > 0 && _optSize > 0) {
      var _s = Math.round((1 - _optSize / _origSize) * 1000) / 10;
      _saveRate = (_s > 0 ? _s : 0) + '%';
    }
    var _fname = 'optimized-image.png';
    if (_of && _of.name) {
      _fname = _of.name.replace(/\.[^.]+$/, '') + '-optimized.' + (_of.name.split('.').pop() || 'png');
    }

    // Detect tool type and use appropriate file name
    var toolType = detectToolType();
    var toolConfig = getToolConfig(toolType);
    if (toolConfig.fileName && _of && _of.name) {
      var ext = _of.name.split('.').pop() || 'png';
      _fname = toolConfig.fileName + '.' + ext;
    }

    openResultModal({
      toolType: toolType,
      origSize: _origSize > 0 ? _origSize : 'Unknown',
      optSize: _optSize,
      saveRate: _saveRate,
      originalBlob: _of,
      resultBlob: _rb,
      fileName: _fname
    });
    _modalShownForSession = true;
  }

  // Monkey-patch URL.createObjectURL to capture result blobs
  if (!URL._smartimgkit_patched) {
    var _origCreateObjectURL = URL.createObjectURL;
    URL.createObjectURL = function(obj) {
      try {
        // Only capture Blob objects (NOT File objects which are user-uploaded originals)
        // File objects have .name and .lastModified; processed results are plain Blobs from canvas.toBlob
        var isPlainBlob = (obj instanceof Blob) && !(obj instanceof File);
        if (isPlainBlob && obj.size && obj.size > 0 && Date.now() > _captureIgnoreUntil) {
          var t = obj.type || '';
          if (t.indexOf('image') === 0 || t.indexOf('video') === 0 || t.indexOf('audio') === 0 || t.indexOf('application/pdf') === 0 || t.indexOf('application/zip') === 0) {
            _lastResultBlob = obj;
            // Trigger modal after a short delay (lets the page finish its own click handler)
            setTimeout(_triggerModalFromCapture, 200);
          }
        }
      } catch(e) {}
      return _origCreateObjectURL.apply(URL, arguments);
    };
    URL._smartimgkit_patched = true;
  }

  // Also expose a manual trigger for tool pages that want to call it explicitly
  SmartImgKit.triggerResultModal = _triggerModalFromCapture;

})();
