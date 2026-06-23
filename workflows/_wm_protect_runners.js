/**
 * SmartImgKit — Batch Watermark & Protect Runners v1
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  // 1. textWatermark
  runners.textWatermark = async function (blob, opt, log) {
    const text = (opt.text || '').trim();
    if (!text) return blob;
    log('text watermark "' + text + '"');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const fontSize = Math.max(14, Math.round(Math.max(img.width, img.height) * 0.04));
    ctx.globalAlpha = opt.opacity || 0.35;
    ctx.fillStyle = opt.color || '#ffffff';
    ctx.font = 'bold ' + fontSize + 'px sans-serif';
    ctx.textAlign = 'right'; ctx.textBaseline = 'bottom';
    ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 4;
    ctx.fillText(text, c.width - fontSize, c.height - fontSize);
    ctx.shadowColor = 'transparent'; ctx.globalAlpha = 1;
    return new Promise(res => c.toBlob(res, 'image/png'));
  };

  // 2. imageWatermark
  runners.imageWatermark = async function (blob, opt, log) {
    if (!opt.logoBlob) return blob;
    log('image watermark');
    const [img, logo] = await Promise.all([KIT.loadImage(blob), KIT.loadImage(opt.logoBlob)]);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const lw = Math.round(img.width * 0.2), lh = Math.round(lw * (logo.height / logo.width));
    ctx.globalAlpha = opt.opacity || 0.5;
    ctx.drawImage(logo, img.width - lw - 20, img.height - lh - 20, lw, lh);
    ctx.globalAlpha = 1;
    return new Promise(res => c.toBlob(res, 'image/png'));
  };

  // 3. stripExif
  runners.stripExif = async function (blob, opt, log) {
    log('strip EXIF');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    c.getContext('2d').drawImage(img, 0, 0);
    return new Promise(res => c.toBlob(res, 'image/jpeg', 0.92));
  };

  // 4. exportZip
  runners.exportZip = async function (results, opt, log) {
    log('packing ' + results.length + ' files');
    const zip = new JSZip();
    for (const r of results) zip.file(r.name, r.blob);
    const content = await zip.generateAsync({ type: 'blob' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(content);
    a.download = opt.filename || 'watermarked.zip';
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); document.body.removeChild(a); }, 1000);
    return content;
  };

  console.log('[SmartImgKit] Batch Watermark & Protect runners loaded');
})();
