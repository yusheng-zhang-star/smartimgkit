/**
 * SmartImgKit — Social Media Kit Runners v1
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  const PLATFORMS = {
    instagram: { w: 1080, h: 1080 },
    facebook:  { w: 1200, h: 630  },
    twitter:   { w: 1500, h: 500  },
    linkedin:  { w: 1200, h: 627  },
  };

  // 1. platformCrop – 按选中平台各导出一版
  runners.platformCrop = async function (blob, opt, log) {
    const platforms = (opt.platforms || ['instagram']);
    log('crop → ' + platforms.join(', '));
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

  // 2. filter
  runners.filter = async function (blob, opt, log) {
    const mode = opt.mode || 'none';
    if (mode === 'none') return blob;
    log('filter → ' + mode);
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.filter = mode === 'sepia' ? 'sepia(0.8)' : mode === 'grayscale' ? 'grayscale(1)' : 'none';
    ctx.drawImage(img, 0, 0);
    return new Promise(res => c.toBlob(res, 'image/jpeg', 0.92));
  };

  // 3. watermark
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

  // 4. exportZip – 支持 _multi
  runners.exportZip = async function (results, opt, log) {
    log('packing ' + results.length + ' files');
    const zip = new JSZip();
    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      const base = r.name.replace(/\.[^.]+$/, '');
      if (r.blob._multi) {
        for (const m of r.blob._multi) {
          zip.file(base + '_' + m.platform + '.png', m.blob);
        }
      } else {
        zip.file(r.name, r.blob);
      }
    }
    const blob = await zip.generateAsync({ type: 'blob' });
    SmartImgKit._triggerDownload(blob, opt.filename || 'social-media-kit.zip');
    return blob;
  };

  })();
