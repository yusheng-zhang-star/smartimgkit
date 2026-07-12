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
    'en': { flag: '\u{1F1EC}\u{1F1E7}', name: 'EN' },
    'es': { flag: '\u{1F1EA}\u{1F1F8}', name: 'ES' },
    'pt': { flag: '\u{1F1E7}\u{1F1F7}', name: 'PT' },
    'id': { flag: '\u{1F1EE}\u{1F1E9}', name: 'ID' },
    'fr': { flag: '\u{1F1EB}\u{1F1F7}', name: 'FR' },
    'vi': { flag: '\u{1F1FB}\u{1F1F3}', name: 'VI' },
    'ar': { flag: '\u{1F1F8}\u{1F1E6}', name: 'AR' }
  };

  var PREFIXES = ['es', 'pt', 'id', 'fr', 'vi', 'ar'];

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
    return 'en';
  }

  // ── Update the lang button display ───────────────────────────────
  function updateLangButton() {
    var lang = getCurrentLanguage();
    var info = LANGS[lang];
    if (!info) return;

    var buttons = document.querySelectorAll('.lang-btn');
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var flagSpan = btn.querySelector('.lang-flag');
      var nameSpan = btn.querySelector('.lang-name');

      if (flagSpan && nameSpan) {
        flagSpan.textContent = info.flag;
        nameSpan.textContent = info.name;
      } else {
        // Plain button format (tool pages)
        btn.innerHTML = info.flag + ' ' + info.name;
      }
    }
  }

  // ── Fix all dropdown links ───────────────────────────────────────
  function updateDropdownLinks() {
    var dropdowns = document.querySelectorAll('.lang-dropdown');
    for (var d = 0; d < dropdowns.length; d++) {
      var links = dropdowns[d].querySelectorAll('a');
      for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var lang = link.getAttribute('hreflang');
        if (!lang) {
          lang = langFromHref(link.getAttribute('href') || '');
        }
        if (!lang || !LANGS[lang]) continue;

        // Fix href to point to translated version of current page
        link.href = constructLanguageURL(lang);

        // Replace onclick with proper switch
        link.removeAttribute('onclick');
        (function(l) {
          link.addEventListener('click', function(e) {
            e.preventDefault();
            switchLanguage(l);
          });
        })(lang);

        // Mark active language
        if (lang === getCurrentLanguage()) {
          link.classList.add('active-lang');
        } else {
          link.classList.remove('active-lang');
        }
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

  // ── Initialize on DOM ready ──────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function() {
    updateLangButton();
    updateDropdownLinks();
    updateFooterLinks();
    rewriteLocalLinks();
  });

})();
