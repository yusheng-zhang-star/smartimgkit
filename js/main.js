/**
 * SmartImgKit - Main JavaScript
 * Handles: Theme toggle, mobile menu, FAQ accordions, dropzone, cookie consent, utilities
 */

/* ===== Theme Toggle ===== */
const themeToggle = document.getElementById('themeToggle');
const htmlEl = document.documentElement;

function initTheme() {
  try {
    const saved = localStorage.getItem('theme');
    if (saved) {
      htmlEl.setAttribute('data-theme', saved);
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      htmlEl.setAttribute('data-theme', 'light');
    }
  } catch (e) {
    // localStorage may be blocked in private mode or sandboxed frames
  }
  updateThemeIcon();
}

function toggleTheme() {
  const current = htmlEl.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  htmlEl.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateThemeIcon();
}

function updateThemeIcon() {
  if (!themeToggle) return;
  const current = htmlEl.getAttribute('data-theme') || 'dark';
  themeToggle.textContent = current === 'dark' ? '☀️' : '🌙';
}

if (themeToggle) themeToggle.addEventListener('click', toggleTheme);

/* ===== Mobile Menu ===== */
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mainNav = document.querySelector('.main-nav');
if (mobileMenuBtn && mainNav) {
  mobileMenuBtn.addEventListener('click', () => {
    const isOpen = mainNav.classList.contains('nav-open');
    if (isOpen) {
      mainNav.classList.remove('nav-open');
      mobileMenuBtn.textContent = '☰';
    } else {
      mainNav.classList.add('nav-open');
      mobileMenuBtn.textContent = '✕';
    }
  });
  // Close on outside click
  document.addEventListener('click', (e) => {
    if (mainNav.classList.contains('nav-open') && 
        !mainNav.contains(e.target) && 
        !mobileMenuBtn.contains(e.target)) {
      mainNav.classList.remove('nav-open');
      mobileMenuBtn.textContent = '☰';
    }
  });
}

/* ===== FAQ Accordions ===== */
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.setAttribute('role', 'button');
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('tabindex', '0');
  
  function toggleFaq() {
    const item = btn.closest('.faq-item');
    const wasOpen = item.classList.contains('open');
    item.parentElement.querySelectorAll('.faq-item').forEach(i => {
      i.classList.remove('open');
      i.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
    });
    if (!wasOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
    }
  }
  
  btn.addEventListener('click', toggleFaq);
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleFaq();
    }
  });
});

/* ===== Cookie Consent (GDPR Compliant) ===== */
const GA4_MEASUREMENT_ID = 'G-KKYP8DMCMD';

function getConsent() {
  try {
    const raw = localStorage.getItem('cookie-consent');
    if (!raw) return null;
    return JSON.parse(raw);
  } catch { return null; }
}

function saveConsent(consent) {
  try {
    localStorage.setItem('cookie-consent', JSON.stringify(consent));
  } catch (e) { /* localStorage blocked */ }
}

let __ga4ConfigApplied = false;

function loadGA4() {
  if (!GA4_MEASUREMENT_ID) return;
  if (document.getElementById('ga4-script')) return;
  const s = document.createElement('script');
  s.id = 'ga4-script';
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_MEASUREMENT_ID);
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  });
}

function updateConsentState(consent) {
  if (!GA4_MEASUREMENT_ID) return;
  function gtag(){ window.dataLayer.push(arguments); }
  gtag('consent', 'update', {
    'analytics_storage': consent.analytics ? 'granted' : 'denied',
    'ad_storage': consent.advertising ? 'granted' : 'denied',
    'ad_user_data': consent.advertising ? 'granted' : 'denied',
    'ad_personalization': consent.advertising ? 'granted' : 'denied'
  });
  if (!__ga4ConfigApplied) {
    __ga4ConfigApplied = true;
    gtag('config', GA4_MEASUREMENT_ID, { anonymize_ip: true });
  }
}

function applyConsent(consent) {
  if (consent.analytics || consent.advertising) {
    loadGA4();
    updateConsentState(consent);
  }
}

/* ===== Cookie 横幅多语种文案 ===== */
const COOKIE_I18N = {
  en: {
    msg: 'We use cookies to improve your experience and serve relevant ads. You can customize your preferences or accept all cookies.',
    more: 'Learn more', accept: 'Accept All', reject: 'Reject All', customize: 'Customize',
    essentialT: 'Essential Cookies', essentialD: 'Required for the website to function. Cannot be disabled.',
    analyticsT: 'Analytics Cookies', analyticsD: 'Help us understand how visitors use our website (Google Analytics). Optional.',
    adsT: 'Advertising Cookies', adsD: 'Used to serve personalized ads and measure ad performance. Optional.',
    save: 'Save Preferences'
  },
  zh: {
    msg: '我们使用 Cookie 来改善浏览体验并展示相关广告。你可以自定义偏好设置，也可以全部接受。',
    more: '了解更多', accept: '全部接受', reject: '全部拒绝', customize: '自定义',
    essentialT: '必要 Cookie', essentialD: '网站运行所必需，无法关闭。',
    analyticsT: '分析 Cookie', analyticsD: '帮助我们了解访客如何使用本站（Google Analytics），可选。',
    adsT: '广告 Cookie', adsD: '用于展示个性化广告并衡量广告效果，可选。',
    save: '保存偏好'
  },
  es: {
    msg: 'Usamos cookies para mejorar tu experiencia y mostrar anuncios relevantes. Puedes ajustar tus preferencias o aceptarlas todas.',
    more: 'Más información', accept: 'Aceptar todas', reject: 'Rechazar todas', customize: 'Personalizar',
    essentialT: 'Cookies necesarias', essentialD: 'Imprescindibles para que la web funcione. No se pueden desactivar.',
    analyticsT: 'Cookies analíticas', analyticsD: 'Nos ayudan a entender cómo se usa el sitio (Google Analytics). Opcionales.',
    adsT: 'Cookies publicitarias', adsD: 'Se usan para mostrar anuncios personalizados y medir su rendimiento. Opcionales.',
    save: 'Guardar preferencias'
  },
  pt: {
    msg: 'Usamos cookies para melhorar sua experiência e exibir anúncios relevantes. Você pode ajustar suas preferências ou aceitar todas.',
    more: 'Saiba mais', accept: 'Aceitar todas', reject: 'Rejeitar todas', customize: 'Personalizar',
    essentialT: 'Cookies necessários', essentialD: 'Essenciais para o site funcionar. Não podem ser desativados.',
    analyticsT: 'Cookies de análise', analyticsD: 'Ajudam a entender como os visitantes usam o site (Google Analytics). Opcionais.',
    adsT: 'Cookies de publicidade', adsD: 'Servem para exibir anúncios personalizados e medir o desempenho. Opcionais.',
    save: 'Salvar preferências'
  },
  id: {
    msg: 'Kami memakai cookie untuk meningkatkan pengalaman Anda dan menampilkan iklan yang relevan. Anda bisa mengatur preferensi atau menerima semua cookie.',
    more: 'Pelajari lebih lanjut', accept: 'Terima Semua', reject: 'Tolak Semua', customize: 'Sesuaikan',
    essentialT: 'Cookie Esensial', essentialD: 'Diperlukan agar situs berfungsi. Tidak bisa dinonaktifkan.',
    analyticsT: 'Cookie Analitik', analyticsD: 'Membantu kami memahami cara pengunjung memakai situs (Google Analytics). Opsional.',
    adsT: 'Cookie Iklan', adsD: 'Dipakai untuk menampilkan iklan yang dipersonalisasi dan mengukur performanya. Opsional.',
    save: 'Simpan Preferensi'
  },
  fr: {
    msg: "Nous utilisons des cookies pour améliorer votre expérience et afficher des publicités pertinentes. Vous pouvez personnaliser vos préférences ou tout accepter.",
    more: 'En savoir plus', accept: 'Tout accepter', reject: 'Tout refuser', customize: 'Personnaliser',
    essentialT: 'Cookies essentiels', essentialD: 'Indispensables au fonctionnement du site. Ne peuvent pas être désactivés.',
    analyticsT: 'Cookies analytiques', analyticsD: "Nous aident à comprendre comment le site est utilisé (Google Analytics). Facultatifs.",
    adsT: 'Cookies publicitaires', adsD: 'Servent à afficher des publicités personnalisées et à mesurer leur performance. Facultatifs.',
    save: 'Enregistrer les préférences'
  },
  vi: {
    msg: 'Chúng tôi dùng cookie để cải thiện trải nghiệm và hiển thị quảng cáo phù hợp. Bạn có thể tùy chỉnh tùy chọn hoặc chấp nhận tất cả.',
    more: 'Tìm hiểu thêm', accept: 'Chấp nhận tất cả', reject: 'Từ chối tất cả', customize: 'Tùy chỉnh',
    essentialT: 'Cookie thiết yếu', essentialD: 'Cần thiết để trang hoạt động. Không thể tắt.',
    analyticsT: 'Cookie phân tích', analyticsD: 'Giúp chúng tôi hiểu cách khách truy cập dùng trang (Google Analytics). Không bắt buộc.',
    adsT: 'Cookie quảng cáo', adsD: 'Dùng để hiển thị quảng cáo cá nhân hóa và đo lường hiệu quả. Không bắt buộc.',
    save: 'Lưu tùy chọn'
  },
  ar: {
    msg: 'نستخدم ملفات تعريف الارتباط لتحسين تجربتك وعرض إعلانات مناسبة. يمكنك تخصيص تفضيلاتك أو قبول جميع الملفات.',
    more: 'اعرف المزيد', accept: 'قبول الكل', reject: 'رفض الكل', customize: 'تخصيص',
    essentialT: 'ملفات ضرورية', essentialD: 'لازمة لعمل الموقع ولا يمكن تعطيلها.',
    analyticsT: 'ملفات تحليلية', analyticsD: 'تساعدنا على فهم كيفية استخدام الزوار للموقع (Google Analytics). اختيارية.',
    adsT: 'ملفات إعلانية', adsD: 'تُستخدم لعرض إعلانات مخصصة وقياس أدائها. اختيارية.',
    save: 'حفظ التفضيلات'
  }
};

function cookieLang() {
  const seg = (location.pathname.split('/')[1] || '').toLowerCase();
  return COOKIE_I18N[seg] ? seg : 'en';
}

let __cookieInit = false;
function initCookieConsent() {
  if (__cookieInit) return;
  const existing = getConsent();
  if (existing) {
    __cookieInit = true;
    applyConsent(existing);
    return;
  }

  __cookieInit = true;
  const banner = document.createElement('div');
  banner.className = 'cookie-consent';
  const t = COOKIE_I18N[cookieLang()];
  banner.setAttribute('lang', cookieLang());
  banner.innerHTML = `
    <div class="cookie-consent-inner">
      <div class="cookie-consent-text">
        <p>${t.msg} <a href="/cookie-policy">${t.more}</a></p>
      </div>
      <div class="cookie-consent-actions">
        <button class="cookie-btn cookie-btn-accept" id="cookieAccept">${t.accept}</button>
        <button class="cookie-btn cookie-btn-decline" id="cookieDecline">${t.reject}</button>
        <button class="cookie-btn cookie-btn-customize" id="cookieCustomize">${t.customize}</button>
      </div>
    </div>
    <div class="cookie-customize" id="cookieCustomPanel">
      <div class="cookie-category">
        <div class="cookie-category-info">
          <h4>${t.essentialT}</h4>
          <p>${t.essentialD}</p>
        </div>
        <label class="cookie-toggle">
          <input type="checkbox" checked disabled>
          <span class="cookie-toggle-slider"></span>
        </label>
      </div>
      <div class="cookie-category">
        <div class="cookie-category-info">
          <h4>${t.analyticsT}</h4>
          <p>${t.analyticsD}</p>
        </div>
        <label class="cookie-toggle">
          <input type="checkbox" id="cookieAnalytics">
          <span class="cookie-toggle-slider"></span>
        </label>
      </div>
      <div class="cookie-category">
        <div class="cookie-category-info">
          <h4>${t.adsT}</h4>
          <p>${t.adsD}</p>
        </div>
        <label class="cookie-toggle">
          <input type="checkbox" id="cookieAdvertising">
          <span class="cookie-toggle-slider"></span>
        </label>
      </div>
      <div class="cookie-save-row">
        <button class="cookie-btn cookie-btn-accept" id="cookieSave">${t.save}</button>
      </div>
    </div>
  `;
  document.body.appendChild(banner);
  setTimeout(() => banner.classList.add('visible'), 500);

  function closeBanner() {
    banner.classList.remove('visible');
    setTimeout(() => banner.remove(), 400);
  }

  function acceptAll() {
    const consent = { essential: true, analytics: true, advertising: true, timestamp: Date.now() };
    saveConsent(consent);
    applyConsent(consent);
    closeBanner();
  }

  function rejectAll() {
    const consent = { essential: true, analytics: false, advertising: false, timestamp: Date.now() };
    saveConsent(consent);
    closeBanner();
  }

  function saveCustom() {
    const analyticsEl = document.getElementById('cookieAnalytics');
    const advertisingEl = document.getElementById('cookieAdvertising');
    const consent = {
      essential: true,
      analytics: !!(analyticsEl && analyticsEl.checked),
      advertising: !!(advertisingEl && advertisingEl.checked),
      timestamp: Date.now()
    };
    saveConsent(consent);
    applyConsent(consent);
    closeBanner();
  }

  const acceptBtn = document.getElementById('cookieAccept');
  const declineBtn = document.getElementById('cookieDecline');
  const customizeBtn = document.getElementById('cookieCustomize');
  const saveBtn = document.getElementById('cookieSave');

  if (acceptBtn) acceptBtn.addEventListener('click', acceptAll);
  if (declineBtn) declineBtn.addEventListener('click', rejectAll);
  if (customizeBtn) customizeBtn.addEventListener('click', () => {
    const panel = document.getElementById('cookieCustomPanel');
    if (panel) panel.classList.toggle('visible');
  });
  if (saveBtn) saveBtn.addEventListener('click', saveCustom);
}

/* ===== Dropzone Utilities ===== */
function setupDropzone(opts) {
  const { dropzoneId, inputId, onFile, accept = '*', multiple = false } = opts;
  const dz = document.getElementById(dropzoneId);
  const input = document.getElementById(inputId);
  if (!dz || !input) return;

  // <label for="fileInput"> native behavior already opens the file dialog on click.
  // Do NOT add a JS click handler that calls input.click() — it causes double dialog.
  // Drag & drop is still handled below.

  input.addEventListener('change', () => {
    const files = multiple ? Array.from(input.files) : input.files[0];
    if (files) onFile(files);
  });

  // Drag & drop
  ['dragenter', 'dragover'].forEach(evt => {
    dz.addEventListener(evt, e => { e.preventDefault(); dz.classList.add('dragover'); });
  });
  ['dragleave', 'drop'].forEach(evt => {
    dz.addEventListener(evt, e => { e.preventDefault(); dz.classList.remove('dragover'); });
  });
  dz.addEventListener('drop', e => {
    const files = multiple ? Array.from(e.dataTransfer.files) : e.dataTransfer.files[0];
    if (files) onFile(files);
  });
}

/* ===== Image Utilities ===== */
const ImageUtils = {
  load(file) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = URL.createObjectURL(file);
    });
  },
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  },
  canvasToBlob(canvas, type = 'image/png', quality = 0.92) {
    return new Promise(resolve => canvas.toBlob(resolve, type, quality));
  },
  createCanvas(width, height) {
    const c = document.createElement('canvas');
    c.width = width; c.height = height;
    return c;
  },
  download(canvasOrBlob, filename, mime) {
    let url;
    if (canvasOrBlob instanceof HTMLCanvasElement) {
      url = canvasOrBlob.toDataURL(mime || 'image/png');
    } else if (canvasOrBlob instanceof Blob) {
      url = URL.createObjectURL(canvasOrBlob);
    } else {
      url = canvasOrBlob;
    }
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    if (canvasOrBlob instanceof Blob) setTimeout(() => URL.revokeObjectURL(url), 1000);
  },
  getImageType(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const map = {
      jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png',
      webp: 'image/webp', gif: 'image/gif', bmp: 'image/bmp', tiff: 'image/tiff'
    };
    return map[ext] || 'image/png';
  },
  formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  },
  showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('visible'));
    setTimeout(() => {
      toast.classList.remove('visible');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
};

/* ===== Global Expose ===== */
window.setupDropzone = setupDropzone;
window.ImageUtils = ImageUtils;
window.initTheme = initTheme;

/* ===== Sample Image & Next Step ===== */
window.SmartImgNextStep = {
  show() {
    const el = document.getElementById('nextStepSection');
    if (el) el.classList.add('visible');
  },
  hide() {
    const el = document.getElementById('nextStepSection');
    if (el) el.classList.remove('visible');
  }
};

window.initSampleButton = function(sampleUrl, onFile) {
  const btn = document.getElementById('sampleBtn');
  if (!btn || !sampleUrl) return;
  btn.addEventListener('click', async (e) => {
    e.stopPropagation();
    e.preventDefault();
    btn.textContent = '⏳ Loading...';
    try {
      const resp = await fetch(sampleUrl);
      const blob = await resp.blob();
      const file = new File([blob], 'sample.jpg', { type: 'image/jpeg' });
      if (onFile) onFile(file);
    } catch (err) {
      btn.textContent = '🖼️ Try with a sample image';
    }
  });
};

/* Init */
initTheme();
initCookieConsent();

/* ===== Reliable Download Trigger (global) ===== */
window.SmartImgKit = window.SmartImgKit || {};
SmartImgKit._triggerDownload = function (blob, filename) {
  if (!filename.includes('.')) filename += '.zip';
  // Support dataURL strings (e.g. from canvas.toDataURL) by converting to Blob
  if (typeof blob === 'string' && blob.startsWith('data:')) {
    var commaIdx = blob.indexOf(',');
    var meta = blob.substring(5, commaIdx);
    var mime = meta.split(';')[0] || 'application/octet-stream';
    var byteString = atob(blob.substring(commaIdx + 1));
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i);
    blob = new Blob([ab], { type: mime });
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.setAttribute('download', filename);
  a.style.display = 'none';
  document.body.appendChild(a);
  const evt = new MouseEvent('click', { view: window, bubbles: true, cancelable: true });
  a.dispatchEvent(evt);
  setTimeout(() => {
    URL.revokeObjectURL(url);
    if (a.parentNode) a.parentNode.removeChild(a);
  }, 4000);
};
SmartImgKit._downloadBlob = function (blob, filename, type) {
  if (type && !filename.includes('.')) {
    const extMap = { 'application/pdf': '.pdf', 'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif', 'application/zip': '.zip', 'video/mp4': '.mp4', 'audio/mpeg': '.mp3', 'image/webp': '.webp' };
    filename += (extMap[type] || '');
  }
  SmartImgKit._triggerDownload(blob, filename);
};


/* ===== Homepage Tools Search & Category Pills ===== */
(function initToolsSearch() {
  var searchInput = document.getElementById('toolSearch');
  if (!searchInput) return;
  var grid = document.querySelector('.tools-grid');
  if (!grid) return;
  var toolCards = Array.prototype.slice.call(grid.querySelectorAll('.tool-card'));
  var catHeaders = Array.prototype.slice.call(grid.querySelectorAll('.tools-category-header'));
  var subHeaders = Array.prototype.slice.call(grid.querySelectorAll('.tools-subcategory-header'));
  var pills = Array.prototype.slice.call(document.querySelectorAll('.cat-pill'));
  var noResults = document.getElementById('noResults');
  var siteHeader = document.querySelector('.site-header');
  var nav = document.querySelector('.tools-nav');

  function adjustNavTop() {
    if (siteHeader && nav) nav.style.top = siteHeader.offsetHeight + 'px';
  }
  adjustNavTop();
  window.addEventListener('resize', adjustNavTop);

  var searchTimer;
  searchInput.addEventListener('input', function () {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(doSearch, 100);
  });

  function doSearch() {
    var q = searchInput.value.trim().toLowerCase();
    if (!q) {
      toolCards.forEach(function (c) { c.style.display = ''; });
      catHeaders.forEach(function (h) { h.style.display = ''; });
      subHeaders.forEach(function (h) { h.style.display = ''; });
      if (noResults) noResults.style.display = 'none';
      return;
    }
    var visible = 0;
    toolCards.forEach(function (card) {
      var text = (card.textContent || '').toLowerCase();
      var match = text.indexOf(q) !== -1;
      card.style.display = match ? '' : 'none';
      if (match) visible++;
    });
    catHeaders.forEach(function (h) {
      var cat = h.getAttribute('data-cat-key');
      var any = toolCards.some(function (c) {
        return c.getAttribute('data-cat') === cat && c.style.display !== 'none';
      });
      h.style.display = any ? '' : 'none';
    });
    subHeaders.forEach(function (h) {
      var cat = h.getAttribute('data-cat-key');
      var sub = h.getAttribute('data-sub-key');
      var any = toolCards.some(function (c) {
        return c.getAttribute('data-cat') === cat &&
               c.getAttribute('data-sub') === sub &&
               c.style.display !== 'none';
      });
      h.style.display = any ? '' : 'none';
    });
    if (noResults) noResults.style.display = visible === 0 ? 'block' : 'none';
  }

  function setActivePill(cat) {
    pills.forEach(function (p) {
      p.classList.toggle('active', p.getAttribute('data-cat') === cat);
    });
  }

  pills.forEach(function (pill) {
    pill.addEventListener('click', function (e) {
      e.preventDefault();
      var offset = (siteHeader ? siteHeader.offsetHeight : 0) +
                   (nav ? nav.offsetHeight : 0) + 12;
      var target;
      if (pill.getAttribute('data-cat') === 'all') {
        target = document.getElementById('tools');
      } else {
        target = document.querySelector(pill.getAttribute('href'));
      }
      if (target) {
        var y = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
      setActivePill(pill.getAttribute('data-cat'));
    });
  });

  /* Scroll-spy: highlight the pill for the category currently at the top */
  function getTopOffset() {
    return (siteHeader ? siteHeader.offsetHeight : 0) +
           (nav ? nav.offsetHeight : 0) + 30;
  }
  function updateActiveOnScroll() {
    var offset = getTopOffset();
    var current = 'all';
    for (var i = 0; i < catHeaders.length; i++) {
      var h = catHeaders[i];
      if (h.style.display === 'none') continue;
      var top = h.getBoundingClientRect().top;
      if (top - offset <= 5) {
        current = h.getAttribute('data-cat-key') || 'all';
      }
    }
    setActivePill(current);
  }
  var scrollTimer;
  window.addEventListener('scroll', function () {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(updateActiveOnScroll, 60);
  }, { passive: true });
  updateActiveOnScroll();
})();
