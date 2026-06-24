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
const GA4_MEASUREMENT_ID = 'G-KKYP8DMCMD'; // Replace with your real GA4 ID

function getConsent() {
  try {
    const raw = localStorage.getItem('cookie-consent');
    if (!raw) return null;
    return JSON.parse(raw);
  } catch { return null; }
}

function saveConsent(consent) {
  localStorage.setItem('cookie-consent', JSON.stringify(consent));
}

function loadGA4() {
  if (!GA4_MEASUREMENT_ID || GA4_MEASUREMENT_ID === 'G-KKYP8DMCMD') return;
  if (document.getElementById('ga4-script')) return;
  const s = document.createElement('script');
  s.id = 'ga4-script';
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_MEASUREMENT_ID;
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
  gtag('config', GA4_MEASUREMENT_ID, { anonymize_ip: true });
}

function updateConsentState(consent) {
  if (!GA4_MEASUREMENT_ID || GA4_MEASUREMENT_ID === 'G-KKYP8DMCMD') return;
  function gtag(){ window.dataLayer.push(arguments); }
  gtag('consent', 'update', {
    'analytics_storage': consent.analytics ? 'granted' : 'denied',
    'ad_storage': consent.advertising ? 'granted' : 'denied',
    'ad_user_data': consent.advertising ? 'granted' : 'denied',
    'ad_personalization': consent.advertising ? 'granted' : 'denied'
  });
}

function applyConsent(consent) {
  if (consent.analytics || consent.advertising) {
    loadGA4();
    updateConsentState(consent);
  }
}

function initCookieConsent() {
  const existing = getConsent();
  if (existing) {
    applyConsent(existing);
    return;
  }

  const banner = document.createElement('div');
  banner.className = 'cookie-consent';
  banner.innerHTML = `
    <div class="cookie-consent-inner">
      <div class="cookie-consent-text">
        <p>We use cookies to improve your experience and serve relevant ads. You can customize your preferences or accept all cookies. <a href="/cookie-policy.html">Learn more</a></p>
      </div>
      <div class="cookie-consent-actions">
        <button class="cookie-btn cookie-btn-accept" id="cookieAccept">Accept All</button>
        <button class="cookie-btn cookie-btn-decline" id="cookieDecline">Reject All</button>
        <button class="cookie-btn cookie-btn-customize" id="cookieCustomize">Customize</button>
      </div>
    </div>
    <div class="cookie-customize" id="cookieCustomPanel">
      <div class="cookie-category">
        <div class="cookie-category-info">
          <h4>Essential Cookies</h4>
          <p>Required for the website to function. Cannot be disabled.</p>
        </div>
        <label class="cookie-toggle">
          <input type="checkbox" checked disabled>
          <span class="cookie-toggle-slider"></span>
        </label>
      </div>
      <div class="cookie-category">
        <div class="cookie-category-info">
          <h4>Analytics Cookies</h4>
          <p>Help us understand how visitors use our website (Google Analytics). Optional.</p>
        </div>
        <label class="cookie-toggle">
          <input type="checkbox" id="cookieAnalytics">
          <span class="cookie-toggle-slider"></span>
        </label>
      </div>
      <div class="cookie-save-row">
        <button class="cookie-btn cookie-btn-accept" id="cookieSave">Save Preferences</button>
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
    const consent = {
      essential: true,
      analytics: document.getElementById('cookieAnalytics').checked,
      advertising: document.getElementById('cookieAdvertising').checked,
      timestamp: Date.now()
    };
    saveConsent(consent);
    applyConsent(consent);
    closeBanner();
  }

  document.getElementById('cookieAccept').addEventListener('click', acceptAll);
  document.getElementById('cookieDecline').addEventListener('click', rejectAll);
  document.getElementById('cookieCustomize').addEventListener('click', () => {
    document.getElementById('cookieCustomPanel').classList.toggle('visible');
  });
  document.getElementById('cookieSave').addEventListener('click', saveCustom);
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
      console.error('Sample load error:', err);
    }
  });
};

/* Init */
initTheme();
initCookieConsent();

