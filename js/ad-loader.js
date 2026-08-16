/**
 * Adsterra Ad Loader — direct insertion with sequential banner init
 * All ad slots use standard banner units (no Native Banner).
 * Banner slots are initialised sequentially with a small delay to
 * avoid atOptions collisions between multiple banner units.
 */
(function () {
  'use strict';

  var ADSTERRA_BASE = 'https://www.highperformanceformat.com';

  var UNITS = {
    banner728: { key: '06fb7e42c90488701f7f9fd5764497fe', width: 728, height: 90 },
    banner320: { key: '9e6fe2ec8816adf4abe212c2a2b8dea8', width: 320, height: 50 },
    square300: { key: 'c95d26a94d4f8dc640cd33ad5ec91528', width: 300, height: 250 }
  };

  function buildOptionsScript(unit) {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.text = "atOptions = {'key' : '" + unit.key + "','format' : 'iframe','height' : " + unit.height + ",'width' : " + unit.width + ",'params' : {}};";
    return script;
  }

  function buildInvokeScript(unit) {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = ADSTERRA_BASE + '/' + unit.key + '/invoke.js';
    return script;
  }

  function loadBanner(slot, unit) {
    slot.appendChild(buildOptionsScript(unit));
    slot.appendChild(buildInvokeScript(unit));
  }

  function pickHeaderUnit() {
    return window.matchMedia('(max-width: 768px)').matches ? UNITS.banner320 : UNITS.banner728;
  }

  function clearSlot(slot) {
    slot.innerHTML = '';
  }

  function loadSlot(slot) {
    var type = slot.getAttribute('data-ad-type');
    var isMobile = window.matchMedia('(max-width: 768px)').matches;

    if (type === 'header') {
      clearSlot(slot);
      slot.setAttribute('data-current-mobile', isMobile ? '1' : '0');
      loadBanner(slot, pickHeaderUnit());
    } else if (type === 'middle') {
      clearSlot(slot);
      if (!isMobile) {
        loadBanner(slot, UNITS.square300);
      }
    } else if (type === 'footer') {
      clearSlot(slot);
      loadBanner(slot, pickHeaderUnit());
    }
  }

  function init() {
    var slots = Array.prototype.slice.call(document.querySelectorAll('.ad-loader-slot'));
    // Sequential init prevents atOptions collisions between banner units.
    var index = 0;
    function next() {
      if (index >= slots.length) return;
      try {
        loadSlot(slots[index]);
      } catch (e) {
        // Skip failed slots
      }
      index += 1;
      setTimeout(next, 150);
    }
    next();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Reload header ad when crossing the mobile breakpoint
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
          loadSlot(slot);
        }
      }
    }, 250);
  });
})();
