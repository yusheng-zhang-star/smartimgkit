/**
 * SmartImgKit - Universal Language Switcher v2
 * Single source of truth for ALL language switching across the entire site.
 * 
 * What it does:
 * 1. Detects current language from URL path
 * 2. Updates lang-btn to show current language flag+name
 * 3. Rewrites ALL lang-dropdown links to point to translated version of CURRENT page
 * 4. Rewrites footer language links
 * 5. On non-English homepages, rewrites tool card links to translated versions
 */

(function() {
  'use strict';

  var LANGS = {
    'en': { flag: 'gb', name: 'EN', native: 'English' },
    'es': { flag: 'es', name: 'ES', native: 'Espa\u00f1ol' },
    'pt': { flag: 'pt', name: 'PT', native: 'Portugu\u00eas' },
    'id': { flag: 'id', name: 'ID', native: 'Bahasa Indonesia' },
    'fr': { flag: 'fr', name: 'FR', native: 'Fran\u00e7ais' },
    'vi': { flag: 'vn', name: 'VI', native: 'Ti\u1EBFng Vi\u1EC7t' },
    'ar': { flag: 'sa', name: 'AR', native: '\u0627\u0644\u0639\u0631\u0628\u064A\u0629' },
    'zh': { flag: 'cn', name: 'ZH', native: '\u4E2D\u6587' }
  };

  var FLAG_CDN = 'https://flagcdn.com/w40/';

  // Ordered list of language codes for dropdown rendering
  var LANG_ORDER = ['en', 'es', 'pt', 'id', 'fr', 'vi', 'ar', 'zh'];

  var PREFIXES = ['es', 'pt', 'id', 'fr', 'vi', 'ar', 'zh'];

  // ── Detect current language ──────────────────────────────────────
  function getCurrentLanguage() {
    try {
      var saved = localStorage.getItem('lang_chosen');
      if (saved && LANGS[saved]) return saved;
    } catch(e) {}

    var path = window.location.pathname.replace(/\/$/, '');
    for (var i = 0; i < PREFIXES.length; i++) {
      var p = PREFIXES[i];
      var re = new RegExp('^\\/' + p + '($|\\/)');
      if (re.test(path)) return p;
    }
    return 'en';
  }

  // ── Strip language prefix from path ──────────────────────────────
  function getBasePath() {
    var path = window.location.pathname;
    for (var i = 0; i < PREFIXES.length; i++) {
      var p = PREFIXES[i];
      if (path === '/' + p || path === '/' + p + '/') return '/';
      if (path.indexOf('/' + p + '/') === 0) return path.substring(3 + (p.length - 2));
    }
    return path;
  }

  // ── Build language-specific URL for current page ─────────────────
  function constructLanguageURL(lang) {
    var base = getBasePath();
    if (lang === 'en') {
      return base;
    }
    return '/' + lang + (base === '/' ? '/' : base);
  }

  // ── Navigate to language version ─────────────────────────────────
  function switchLanguage(lang) {
    try {
      localStorage.setItem('lang_chosen', lang);
      sessionStorage.setItem('lang_choice', '1');
    } catch(e) {}
    var target = constructLanguageURL(lang);
    if (target === window.location.pathname || target === window.location.pathname.replace(/\/$/, '') + '/') {
      return;
    }
    window.location.href = target;
  }

  // ── Guess language from href ─────────────────────────────────────
  function langFromHref(href) {
    if (!href || href === '/' || href === '') return 'en';
    if (href.indexOf('/es') === 0) return 'es';
    if (href.indexOf('/pt') === 0) return 'pt';
    if (href.indexOf('/id') === 0) return 'id';
    if (href.indexOf('/fr') === 0) return 'fr';
    if (href.indexOf('/vi') === 0) return 'vi';
    if (href.indexOf('/ar') === 0) return 'ar';
    if (href.indexOf('/zh') === 0) return 'zh';
    return 'en';
  }

  // ── Update the lang button display ───────────────────────────────
  function updateLangButton() {
    var lang = getCurrentLanguage();
    var info = LANGS[lang];
    if (!info) return;

    var flagUrl = FLAG_CDN + info.flag + '.png';
    var buttons = document.querySelectorAll('.lang-btn');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].innerHTML =
        '<img class="lang-flag-img" src="' + flagUrl + '" alt="" loading="lazy" width="24" height="16"> ' +
        '<span class="lang-name">' + info.name + '</span>' +
        '<span class="lang-arrow">\u25BE</span>';
      buttons[i].setAttribute('aria-label', 'Switch to ' + info.native);
    }
  }

  // ── Rebuild all dropdowns from scratch (single source of truth) ───
  function rebuildDropdowns() {
    var currentLang = getCurrentLanguage();
    var switchers = document.querySelectorAll('.lang-switcher');

    for (var s = 0; s < switchers.length; s++) {
      var switcher = switchers[s];
      // Ensure it has an id for toggleLangDropdown
      if (!switcher.id) switcher.id = 'langSwitcher';

      // Ensure the button has onclick handler
      var btn = switcher.querySelector('.lang-btn');
      if (btn && !btn.getAttribute('onclick')) {
        btn.setAttribute('onclick', 'toggleLangDropdown()');
      }

      // Find or create the dropdown container
      var dropdown = switcher.querySelector('.lang-dropdown');
      if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.className = 'lang-dropdown';
        switcher.appendChild(dropdown);
      }
      // Remove any inline style that might force display:none!important
      dropdown.removeAttribute('style');
      // Also remove inline style from switcher itself
      switcher.removeAttribute('style');

      // Clear existing content and rebuild with ALL 8 languages
      dropdown.innerHTML = '';
      for (var i = 0; i < LANG_ORDER.length; i++) {
        var code = LANG_ORDER[i];
        var info = LANGS[code];
        if (!info) continue;

        var link = document.createElement('a');
        link.setAttribute('hreflang', code);
        link.href = constructLanguageURL(code);
        if (code === currentLang) {
          link.classList.add('active-lang');
        }
        var flagUrl = FLAG_CDN + info.flag + '.png';
        link.innerHTML = '<img class="lang-flag-img" src="' + flagUrl + '" alt="" loading="lazy" width="24" height="16"> ' + info.native;

        // Attach switch handler
        (function(l) {
          link.addEventListener('click', function(e) {
            e.preventDefault();
            switchLanguage(l);
          });
        })(code);

        dropdown.appendChild(link);
      }
    }
  }

  // ── Fix footer language links ────────────────────────────────────
  function updateFooterLinks() {
    var footer = document.querySelector('.footer-lang');
    if (!footer) return;

    var links = footer.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var href = link.getAttribute('href') || '';
      var lang = langFromHref(href);
      if (!LANGS[lang]) continue;

      link.href = constructLanguageURL(lang);
      link.removeAttribute('onclick');
      (function(l) {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          switchLanguage(l);
        });
      })(lang);
    }
  }

  // ── On non-English pages, rewrite tool cards to language versions ─
  function rewriteLocalLinks() {
    var lang = getCurrentLanguage();
    if (lang === 'en') return;

    // Only rewrite links inside main content (not header/footer nav)
    var main = document.querySelector('main');
    if (!main) return;

    var allLinks = main.querySelectorAll('a');
    for (var i = 0; i < allLinks.length; i++) {
      var link = allLinks[i];
      var href = link.getAttribute('href');
      if (!href) continue;

      // Tool pages: /tools/xxx → /<lang>/tools/xxx
      if (href.indexOf('/tools/') === 0) {
        link.href = '/' + lang + href;
      }
      // Workflow pages: /workflows/xxx → /<lang>/workflows/xxx
      else if (href.indexOf('/workflows/') === 0) {
        link.href = '/' + lang + href;
      }
    }
  }

  // ── Toggle dropdown (exported globally for button onclick) ───────
  window.toggleLangDropdown = function() {
    var sw = document.getElementById('langSwitcher');
    if (sw) {
      if (sw.classList.contains('open')) {
        sw.classList.remove('open');
      } else {
        // Close all other open dropdowns first
        var all = document.querySelectorAll('.lang-switcher.open');
        for (var i = 0; i < all.length; i++) {
          all[i].classList.remove('open');
        }
        sw.classList.add('open');
      }
    }
  };

  // ── Close dropdown on outside click ──────────────────────────────
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.lang-switcher')) {
      var all = document.querySelectorAll('.lang-switcher.open');
      for (var i = 0; i < all.length; i++) {
        all[i].classList.remove('open');
      }
    }
  });

  // ── Inject a lang-switcher if the page doesn't have one ──────────
  function injectSwitcher() {
    if (document.querySelector('.lang-switcher')) return;

    var headerActions = document.querySelector('.header-actions');
    if (!headerActions) return;

    var currentLang = getCurrentLanguage();
    var info = LANGS[currentLang] || LANGS['en'];
    var flagUrl = FLAG_CDN + info.flag + '.png';

    var switcher = document.createElement('div');
    switcher.className = 'lang-switcher';
    switcher.id = 'langSwitcher';
    switcher.innerHTML =
      '<button class="lang-btn" onclick="toggleLangDropdown()" aria-label="Switch language">' +
      '<img class="lang-flag-img" src="' + flagUrl + '" alt="" loading="lazy" width="24" height="16"> ' +
      '<span class="lang-name">' + info.name + '</span>' +
      '<span class="lang-arrow">\u25BE</span>' +
      '</button>';

    headerActions.insertBefore(switcher, headerActions.firstChild);
  }

  // ── Initialize on DOM ready ──────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function() {
    injectSwitcher();
    updateLangButton();
    rebuildDropdowns();
    updateFooterLinks();
    rewriteLocalLinks();
  });

})();
