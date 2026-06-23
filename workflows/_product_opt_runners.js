/**
 * SmartImgKit — Product Image Optimizer Runners v1
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  // 1. compress
  runners.compress = async function (blob, opt, log) {
    const q = Math.max(0.1, Math.min(1, opt.quality || 0.82));
    log('compress @ ' + Math.round(q * 100) + '%');
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    c.getContext('2d').drawImage(img, 0, 0);
    return new Promise(res => c.toBlob(res, 'image/jpeg', q));
  };

  // 2. convertFormat
  runners.convertFormat = async function (blob, opt, log) {
    const fmt = (opt.format || 'jpeg').toLowerCase();
    const mime = fmt === 'webp' ? 'image/webp' : fmt === 'png' ? 'image/png' : 'image/jpeg';
    log('convert → ' + fmt);
    const img = await KIT.loadImage(blob);
    const c = document.createElement('canvas');
    c.width = img.width; c.height = img.height;
    const ctx = c.getContext('2d');
    if (fmt !== 'png') { ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, c.width, c.height); }
    ctx.drawImage(img, 0, 0);
    return new Promise(res => c.toBlob(res, mime));
  };

  // 3. stripExif – 重新编码丢弃 EXIF
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
    a.download = opt.filename || 'product-optimized.zip';
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); document.body.removeChild(a); }, 1000);
    return content;
  };

  console.log('[SmartImgKit] Product Image Optimizer runners loaded');
})();
