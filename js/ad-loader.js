/**
 * Adsterra Ad Loader — iframe-isolated to avoid atOptions conflicts
 * Each ad slot is rendered inside an independent iframe so that
 * window.atOptions never collides between multiple ad units on one page.
 */
(function () {
  'use strict';

  var ADSTERRA_BASE = 'https://www.highperformanceformat.com';
  var NATIVE_SRC = 'https://pl29741299.effectivecpmnetwork.com/5a540a2ce35c794ad7d73a726a88971c/invoke.js';
  var NATIVE_CONTAINER = 'container-5a540a2ce35c794ad7d73a726a88971c';

  // Ad unit keys
  var UNITS = {
    banner728: { key: '06fb7e42c90488701f7f9fd5764497fe', width: 728, height: 90 },
    banner320: { key: '9e6fe2ec8816adf4abe212c2a2b8dea8', width: 320, height: 50 },
    square300: { key: 'c95d26a94d4f8dc640cd33ad5ec91528', width: 300, height: 250 }
  };

  function buildBannerHTML(unit) {
    return '<!DOCTYPE html><html><head><meta charset="UTF-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<style>html,body{margin:0;padding:0;overflow:hidden;background:transparent}body{display:flex;align-items:center;justify-content:center}</style>' +
      '</head><body>' +
      '<script type="text/javascript">atOptions = {' +
      "'key' : '" + unit.key + "'," +
      "'format' : 'iframe'," +
      "'height' : " + unit.height + ',' +
      "'width' : " + unit.width + ',' +
      "'params' : {}" +
      "};<\/script>" +
      '<script type="text/javascript" src="' + ADSTERRA_BASE + '/' + unit.key + '/invoke.js"><\/script>' +
      '</body></html>';
  }

  function buildNativeHTML() {
    return '<!DOCTYPE html><html><head><meta charset="UTF-8">' +
      '<meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<style>html,body{margin:0;padding:0;overflow:hidden;background:transparent}</style>' +
      '</head><body>' +
      '<script async="async" data-cfasync="false" src="' + NATIVE_SRC + '"><\/script>' +
      '<div id="' + NATIVE_CONTAINER + '"></div>' +
      '</body></html>';
  }

  function createIframe(html, width, height) {
    var iframe = document.createElement('iframe');
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('marginwidth', '0');
    iframe.setAttribute('marginheight', '0');
    iframe.style.width = '100%';
    iframe.style.maxWidth = width + 'px';
    iframe.style.height = height + 'px';
    iframe.style.border = '0';
    iframe.style.display = 'block';
    iframe.style.margin = '0 auto';
    iframe.style.background = 'transparent';
    iframe.setAttribute('aria-hidden', 'false');
    iframe.setAttribute('role', 'complementary');
    iframe.setAttribute('title', 'Advertisement');
    // Use srcdoc for inline content; fallback to blob URL if srcdoc unsupported
    if ('srcdoc' in iframe) {
      iframe.setAttribute('srcdoc', html);
    } else {
      // Fallback for very old browsers
      var blob = new Blob([html], { type: 'text/html' });
      iframe.src = URL.createObjectURL(blob);
    }
    return iframe;
  }

  function loadAd(slot) {
    var type = slot.getAttribute('data-ad-type');
    var isMobile = window.matchMedia('(max-width: 768px)').matches;

    if (type === 'header') {
      // Responsive: PC = 728x90, Mobile = 320x50
      var unit = isMobile ? UNITS.banner320 : UNITS.banner728;
      slot.appendChild(createIframe(buildBannerHTML(unit), unit.width, unit.height));
    } else if (type === 'middle') {
      // 300x250, hidden on mobile via CSS
      if (!isMobile) {
        slot.appendChild(createIframe(buildBannerHTML(UNITS.square300), UNITS.square300.width, UNITS.square300.height));
      }
    } else if (type === 'footer') {
      // Native banner
      slot.appendChild(createIframe(buildNativeHTML(), 728, 120));
    }
  }

  function init() {
    var slots = document.querySelectorAll('.ad-loader-slot');
    for (var i = 0; i < slots.length; i++) {
      try {
        loadAd(slots[i]);
      } catch (e) {
        // Silently skip failed ad slots
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Reload ads on orientation change (responsive switch)
  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      var isMobile = window.matchMedia('(max-width: 768px)').matches;
      var headerSlots = document.querySelectorAll('.ad-loader-slot[data-ad-type="header"]');
      for (var i = 0; i < headerSlots.length; i++) {
        var slot = headerSlots[i];
        var currentIsMobile = slot.getAttribute('data-current-mobile') === '1';
        if (currentIsMobile !== isMobile) {
          slot.innerHTML = '';
          slot.setAttribute('data-current-mobile', isMobile ? '1' : '0');
          loadAd(slot);
        }
      }
    }, 250);
  });
})();
