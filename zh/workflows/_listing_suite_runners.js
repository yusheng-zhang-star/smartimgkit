/**
 * SmartImgKit — Listing Image Suite Runners v1
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  const PLATFORMS = {
    amazon:  { w: 1000, h: 1000 },
    ebay:    { w: 1600, h: 1600 },
    etsy:    { w: 2000, h: 2000 },
    shopify: { w: 2048, h: 2048 },
  };

  // 1. platformResize – 为每个选中平台生成一版
  runners.platformResize = async function (blob, opt, log) {
    const platforms = (opt.platforms || ['amazon']);
    log('resize → ' + platforms.join(', '));
    const img = await KIT.loadImage(blob);
    const results = [];
    for (const pid of platforms) {
      const p = PLATFORMS[pid];
      if (!p) continue;
      const c = document.createElement('canvas');
      c.width = p.w; c.height = p.h;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, p.w, p.h);
      const iA = img.width / img.height;
      const pA = p.w / p.h;
      let dx = 0, dy = 0, dw, dh;
      if (iA > pA) { dh = p.h; dw = img.width * (p.h / img.height); dx = (p.w - dw) / 2; }
      else { dw = p.w; dh = img.height * (p.w / img.width); dy = (p.h - dh) / 2; }
      ctx.drawImage(img, dx, dy, dw, dh);
      const b = await new Promise(res => c.toBlob(res, 'image/jpeg', 0.92));
      results.push({ platform: pid, blob: b });
    }
    const first = results[0] && results[0].blob;
    first._multi = results;
    return first;
  };

  // 2. watermark
  runners.watermark = async function (blob, opt, log) {
    const text = (opt.text || '').trim();
    if (!text) return blob;
    log('watermark "' + text + '"');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const fontSize = Math.max(16, Math.round(Math.max(img.width, img.height) * 0.04));
    ctx.globalAlpha = opt.opacity || 0.3;
    ctx.fillStyle = opt.color || '#ffffff';
    ctx.font = 'bold ' + fontSize + 'px sans-serif';
    ctx.textAlign = 'right'; ctx.textBaseline = 'bottom';
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 4;
    ctx.fillText(text, c.width - fontSize, c.height - fontSize);
    ctx.shadowColor = 'transparent'; ctx.globalAlpha = 1;
    return new Promise(res => c.toBlob(res, 'image/jpeg', 0.92));
  };

  // 3. compress
  runners.compress = async function (blob, opt, log) {
    const q = Math.max(0.1, Math.min(1, opt.quality || 0.82));
    log('compress @ ' + Math.round(q * 100) + '%');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    c.getContext('2d').drawImage(img, 0, 0);
    return new Promise(res => c.toBlob(res, 'image/jpeg', q));
  };

  // 4. exportZip – 支持 _multi
  runners.exportZip = async function (results, opt, log) {
    log('packing ' + results.length + ' files');
    const zip = new JSZip();
    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      const base = r.name.replace(/\.[^.]+$/, '');
      if (r.blob._multi) {
        for (const m of r.blob._multi) {
          zip.file(base + '_' + m.platform + '.jpg', m.blob);
        }
      } else {
        zip.file(r.name, r.blob);
      }
    }
    const blob = await zip.generateAsync({ type: 'blob' });
    SmartImgKit._triggerDownload(blob, opt.filename || 'listing-images.zip');
    return blob;
  };

  console.log('[SmartImgKit] Listing Image Suite runners loaded');
})();
