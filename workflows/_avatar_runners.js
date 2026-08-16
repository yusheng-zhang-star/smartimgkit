/**
 * SmartImgKit — Avatar Pipeline Runners v1
 *
 * 4 个 runner：circleCrop / filter / watermark / resize
 * 每个 runner: async (blob, options, log) => newBlob
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  // -------- 1. circleCrop --------
  // options: { sizePct=80, offsetX=0, offsetY=0, bg='transparent'|'white'|'custom', bgColor='#ffffff' }
  runners.circleCrop = async function (blob, opt = {}, log) {
    log('cropping');
    const img = await KIT.loadImage(blob);
    const W = img.width, H = img.height;
    const minSide = Math.min(W, H);
    const outSize = Math.max(minSide, 300);
    const c = document.createElement('canvas');
    c.width = outSize; c.height = outSize;
    const ctx = c.getContext('2d');
    const bg = opt.bg || 'white';
    if (bg === 'white' || bg === 'transparent') { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, outSize, outSize); }
    else if (bg === 'custom' && opt.bgColor) { ctx.fillStyle = opt.bgColor; ctx.fillRect(0, 0, outSize, outSize); }

    const pct = (opt.sizePct || 80) / 100;
    const radius = minSide * 0.5 * pct;
    const cx = minSide * 0.5 + ((opt.offsetX || 0) / 50) * (minSide * 0.5 - radius);
    const cy = minSide * 0.5 + ((opt.offsetY || 0) / 50) * (minSide * 0.5 - radius);
    const scale = outSize / minSide;

    ctx.save();
    ctx.scale(scale, scale);
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.closePath();
    ctx.clip();
    ctx.drawImage(img, 0, 0, W, H);
    ctx.restore();

    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // -------- 2. filter --------
  // options: { mode='none'|'sepia'|'grayscale'|'blur', blurPx=4 }
  runners.filter = async function (blob, opt = {}, log) {
    const mode = opt.mode || 'none';
    if (mode === 'none') { log('skip'); return blob; }
    log('applying ' + mode);
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    let filter = 'none';
    if (mode === 'sepia') filter = 'sepia(1)';
    else if (mode === 'grayscale') filter = 'grayscale(1)';
    else if (mode === 'blur') filter = `blur(${opt.blurPx || 4}px)`;
    ctx.filter = filter;
    ctx.drawImage(img, 0, 0);
    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // -------- 3. watermark --------
  // options: { text='', size=24, opacity=0.3, color='#000000' }
  //         或 { skipIfEmpty: true }（无文字直接返回原图）
  runners.watermark = async function (blob, opt = {}, log) {
    const text = (opt.text || '').trim();
    if (!text) { log('no text, skip'); return blob; }
    log('stamping "' + text + '"');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    ctx.globalAlpha = opt.opacity || 0.3;
    ctx.fillStyle = opt.color || '#000000';
    ctx.font = `${opt.size || 24}px sans-serif`;
    ctx.textBaseline = 'bottom';
    ctx.fillText(text, 12, c.height - 12);
    ctx.globalAlpha = 1;
    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // -------- 4. resize (single) --------
  // options: { size=256 }  输出正方形
  runners.resize = async function (blob, opt = {}, log) {
    const size = opt.size || 256;
    log('resize → ' + size);
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = size; c.height = size;
    const ctx = c.getContext('2d');
    // 居中裁切
    const aspect = img.width / img.height;
    let sx = 0, sy = 0, sw = img.width, sh = img.height;
    if (aspect > 1) { sw = img.height; sx = (img.width - sw) / 2; }
    else if (aspect < 1) { sh = img.width; sy = (img.height - sh) / 2; }
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, size, size);
    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  })();
