/**
 * SmartImgKit — E-Commerce Pack Runners v1
 *
 * 4 个 runner：platformResize / compress / watermark / exportZip
 * 每个 runner: async (blob, options, log) => newBlob
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  // ===== 1. platformResize =====
  // options: { platform='amazon', customW=1000, customH=1000, bg='white'|'transparent'|'custom', bgColor='#ffffff' }
  // Platform presets:
  //   amazon:   1000×1000 (square, white bg)
  //   shopify:  2048×2048 (max, square)
  //   ebay:    1600×1600 (max, square)
  //   etsy:    2000×2000 (max, square)
  //   custom:   user-defined
  const PLATFORM = {
    amazon:  { w: 1000, h: 1000 },
    shopify: { w: 2048, h: 2048 },
    ebay:    { w: 1600, h: 1600 },
    etsy:    { w: 2000, h: 2000 },
  };
  runners.platformResize = async function (blob, opt = {}, log) {
    const p = opt.platform || 'amazon';
    let tw, th;
    if (p === 'custom') { tw = parseInt(opt.customW) || 1000; th = parseInt(opt.customH) || 1000; }
    else { tw = PLATFORM[p].w; th = PLATFORM[p].h; }
    log('resize → ' + tw + '×' + th);

    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = tw; c.height = th;
    const ctx = c.getContext('2d');

    // background
    const bg = opt.bg || 'white';
    if (bg === 'white') { ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, tw, th); }
    else if (bg === 'custom' && opt.bgColor) { ctx.fillStyle = opt.bgColor; ctx.fillRect(0, 0, tw, th); }
    // transparent: do nothing (canvas is transparent by default in PNG)

    // center-fit the image
    const imgAspect = img.width / img.height;
    const targetAspect = tw / th;
    let dx = 0, dy = 0, dw, dh;
    if (imgAspect > targetAspect) { dh = th; dw = img.width * (th / img.height); dx = (tw - dw) / 2; }
    else { dw = tw; dh = img.height * (tw / img.width); dy = (th - dh) / 2; }
    ctx.drawImage(img, dx, dy, dw, dh);

    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // ===== 2. compress =====
  // options: { quality=0.82 }  (0-1, for JPEG/PNG re-compress)
  // We re-encode as JPEG at given quality for maximum compression
  runners.compress = async function (blob, opt = {}, log) {
    const q = Math.max(0.1, Math.min(1, opt.quality || 0.82));
    log('compress @ ' + Math.round(q * 100) + '%');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', q));
  };

  // ===== 3. watermark =====
  // options: { text='', size=28, opacity=0.35, color='#ffffff', position='se' }
  // position: 'se'=southeast(bottom-right), 's'=south(bottom-center), 'center'
  runners.watermark = async function (blob, opt = {}, log) {
    const text = (opt.text || '').trim();
    if (!text) { log('no watermark, skip'); return blob; }
    log('watermark "' + text + '"');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);

    const fontSize = Math.max(12, Math.min(opt.size || 28, Math.round(Math.max(img.width, img.height) * 0.05)));
    ctx.globalAlpha = opt.opacity || 0.35;
    ctx.fillStyle = opt.color || '#ffffff';
    ctx.font = `bold ${fontSize}px sans-serif`;
    ctx.textBaseline = 'bottom';

    const pad = fontSize;
    let x, y;
    const pos = opt.position || 'se';
    if (pos === 'se') { ctx.textAlign = 'right'; x = c.width - pad; y = c.height - pad; }
    else if (pos === 's') { ctx.textAlign = 'center'; x = c.width / 2; y = c.height - pad; }
    else { ctx.textAlign = 'center'; x = c.width / 2; y = c.height / 2; }

    // shadow for readability
    ctx.shadowColor = 'rgba(0,0,0,0.5)';
    ctx.shadowBlur = 4;
    ctx.fillText(text, x, y);
    ctx.shadowColor = 'transparent';
    ctx.globalAlpha = 1;
    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // ===== 4. exportZip (called once at end, not per-step) =====
  // results: [{ name, blob }]
  // options: { filename='product-images.zip' }
  runners.exportZip = async function (results, opt = {}, log) {
    log('packing ' + results.length + ' files');
    const zip = new JSZip();
    for (const r of results) {
      zip.file(r.name, r.blob);
    }
    const content = await zip.generateAsync({ type: 'blob' });
    const url = URL.createObjectURL(content);
    const a = document.createElement('a');
    a.href = url;
    a.download = opt.filename || 'product-images.zip';
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 1000);
    log('download triggered');
    return content;
  };

  console.log('[SmartImgKit] E-Commerce Pack runners loaded');
})();
