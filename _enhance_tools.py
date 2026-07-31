#!/usr/bin/env python
"""Enhance GIF Editor with UPNG.js (APNG support) and fix Photo Restoration."""

import os, re

# ============ 1. Enhance GIF Editor ============
gif_path = r'E:\网站项目\smartimgkit\tools\gif-editor.html'

with open(gif_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add UPNG.js + pako CDN before /js/main.js
upng_scripts = '''  <script src="https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/upng-js@2.1.0/UPNG.min.js"></script>
'''

if 'upng-js' not in content:
    content = content.replace(
        '  <script src="/js/main.js?v=4"></script>',
        upng_scripts + '  <script src="/js/main.js?v=4"></script>'
    )

# Add APNG export option to quality select and add APNG output format
content = content.replace(
    '''<option value="3">High (larger file)</option>
                </select>''',
    '''<option value="3">High (larger file)</option>
                    <option value="apng">APNG (lossless, better quality)</option>
                </select>'''
)

# Update file input to accept APNG too
content = content.replace(
    'accept="image/*" multiple',
    'accept="image/*,.apng" multiple'
)

# Update handleFiles to support APNG parsing (split into frames)
old_handle_files = '''    function handleFiles(fileList) {
        const files = Array.from(fileList).filter(f => f.type.startsWith('image/'));
        if (!files.length) return;
        var ba = document.getElementById('beforeAfterPreview');
        if (ba) ba.classList.add('hidden');
        files.forEach(f => {
            var reader = new FileReader();
            reader.onload = function(evt) {
                var img = new Image();
                img.onload = function() {
                    frames.push({ file: f, imgDataUrl: evt.target.result, img: img, delay: parseInt(globalDelay.value) });
                    renderFrames();
                };
                img.src = evt.target.result;
            };
            reader.readAsDataURL(f);
        });
    }'''

new_handle_files = '''    function handleFiles(fileList) {
        const files = Array.from(fileList).filter(f => f.type.startsWith('image/') || f.name.toLowerCase().endsWith('.apng'));
        if (!files.length) return;
        var ba = document.getElementById('beforeAfterPreview');
        if (ba) ba.classList.add('hidden');
        files.forEach(f => {
            var reader = new FileReader();
            reader.onload = function(evt) {
                var fname = f.name.toLowerCase();
                if (fname.endsWith('.apng') || (f.type === 'image/png' && window.UPNG)) {
                    try {
                        var buf = evt.target.result;
                        var img = UPNG.decode(buf);
                        var rgbaFrames = UPNG.toRGBA8(img);
                        var delays = img.frames.map(fr => fr.delay);
                        rgbaFrames.forEach((rgba, i) => {
                            var c = document.createElement('canvas');
                            c.width = img.width; c.height = img.height;
                            var cctx = c.getContext('2d');
                            var imgData = cctx.createImageData(img.width, img.height);
                            new Uint8Array(imgData.data.buffer).set(new Uint8Array(rgba));
                            cctx.putImageData(imgData, 0, 0);
                            var delay = delays[i] || parseInt(globalDelay.value);
                            frames.push({ file: f, imgDataUrl: c.toDataURL(), img: c, delay: delay });
                        });
                        renderFrames();
                        return;
                    } catch(e) { console.log('APNG parse failed, falling back:', e); }
                }
                var img = new Image();
                img.onload = function() {
                    frames.push({ file: f, imgDataUrl: evt.target.result, img: img, delay: parseInt(globalDelay.value) });
                    renderFrames();
                };
                img.src = evt.target.result;
            };
            if (fname.endsWith('.apng')) reader.readAsArrayBuffer(f);
            else reader.readAsDataURL(f);
        });
    }'''

content = content.replace(old_handle_files, new_handle_files)

# Add APNG export to generate handler
old_generate = '''        gif.on('finished', function(blob) {
            var url = URL.createObjectURL(blob);
            resultGif.src = url;
            resultSection.classList.remove('hidden');
            progressSection.classList.add('hidden');
            generateBtn.disabled = false;
            downloadBtn.onclick = function() {
                var a = document.createElement('a'); a.href = url; a.download = 'smartimgkit-animation.gif'; a.click();
            };
        });
        gif.render();'''

new_generate = '''        var isApng = quality.value === 'apng';
        if (isApng) {
            try {
                statusText.textContent = 'Encoding APNG...';
                var targetW = resizeWidth.value ? parseInt(resizeWidth.value) : null;
                var outW = targetW || frames[0].img.naturalWidth;
                var outH = targetW ? Math.round(frames[0].img.naturalHeight * (targetW / frames[0].img.naturalWidth)) : frames[0].img.naturalHeight;
                var frameBufs = [];
                var frameDelays = [];
                frames.forEach((frame, idx) => {
                    var canvas = document.createElement('canvas');
                    var w = frame.img.naturalWidth || frame.img.width;
                    var h = frame.img.naturalHeight || frame.img.height;
                    if (targetW) { h = Math.round(h * (targetW / w)); w = targetW; }
                    canvas.width = w; canvas.height = h;
                    canvas.getContext('2d').drawImage(frame.img, 0, 0, w, h);
                    var idata = canvas.getContext('2d').getImageData(0, 0, w, h);
                    frameBufs.push(idata.data.buffer);
                    frameDelays.push(frame.delay);
                    progressFill.style.width = Math.round((idx+1) / frames.length * 50) + '%';
                });
                statusText.textContent = 'Compressing APNG...';
                progressFill.style.width = '60%';
                var apngBuf = UPNG.encode(frameBufs, outW, outH, 0, frameDelays);
                progressFill.style.width = '100%';
                var blob = new Blob([apngBuf], { type: 'image/apng' });
                var url = URL.createObjectURL(blob);
                resultGif.src = url;
                resultSection.classList.remove('hidden');
                progressSection.classList.add('hidden');
                generateBtn.disabled = false;
                downloadBtn.textContent = '⬇️ Download APNG';
                downloadBtn.onclick = function() {
                    var a = document.createElement('a'); a.href = url; a.download = 'smartimgkit-animation.png'; a.click();
                };
            } catch(err) {
                alert('APNG export failed: ' + err.message);
                generateBtn.disabled = false;
                progressSection.classList.add('hidden');
            }
            return;
        }

        gif.on('finished', function(blob) {
            var url = URL.createObjectURL(blob);
            resultGif.src = url;
            resultSection.classList.remove('hidden');
            progressSection.classList.add('hidden');
            generateBtn.disabled = false;
            downloadBtn.textContent = '⬇️ Download GIF';
            downloadBtn.onclick = function() {
                var a = document.createElement('a'); a.href = url; a.download = 'smartimgkit-animation.gif'; a.click();
            };
        });
        gif.render();'''

content = content.replace(old_generate, new_generate)

with open(gif_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Enhanced: {gif_path}")

# ============ 2. Fix Photo Restoration ============
pr_path = r'E:\网站项目\smartimgkit\tools\photo-restoration.html'

with open(pr_path, 'r', encoding='utf-8') as f:
    pr_content = f.read()

# Replace empty script with actual implementation
photo_script = '''<script>
(function(){
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const previewCanvas = document.getElementById('previewCanvas');
  const ctx = previewCanvas.getContext('2d');
  const placeholderText = document.getElementById('placeholderText');
  const downloadBtn = document.getElementById('downloadBtn');
  const progressFill = document.getElementById('progressFill');

  let origImage = null;
  let origImageData = null;
  let isComparing = false;
  let beforeCanvas = null, afterCanvas = null;

  // Drag & drop
  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => {
    e.preventDefault(); dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  dropzone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', e => { if (e.target.files.length) handleFile(e.target.files[0]); });

  function handleFile(file) {
    if (!file.type.startsWith('image/')) { alert('Please upload an image file.'); return; }
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = new Image();
      img.onload = function() {
        origImage = img;
        // Fit to reasonable size
        const maxW = 1200, maxH = 900;
        let w = img.width, h = img.height;
        if (w > maxW) { h = h * maxW / w; w = maxW; }
        if (h > maxH) { w = w * maxH / h; h = maxH; }
        previewCanvas.width = w; previewCanvas.height = h;
        previewCanvas.style.display = 'block';
        placeholderText.style.display = 'none';
        ctx.drawImage(img, 0, 0, w, h);
        origImageData = ctx.getImageData(0, 0, w, h);
        downloadBtn.disabled = false;
        document.getElementById('compareBox').style.display = 'none';
        document.getElementById('compareToggle').checked = false;
        isComparing = false;
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  // ---- Image processing algorithms ----

  function applyMedianFilter(imgData, strength) {
    const w = imgData.width, h = imgData.height, src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    const radius = Math.max(1, Math.round(strength / 30));
    const window = [];
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        for (let c = 0; c < 3; c++) {
          window.length = 0;
          for (let dy = -radius; dy <= radius; dy++) {
            for (let dx = -radius; dx <= radius; dx++) {
              const yy = Math.max(0, Math.min(h-1, y+dy));
              const xx = Math.max(0, Math.min(w-1, x+dx));
              window.push(src[(yy*w+xx)*4+c]);
            }
          }
          window.sort((a,b) => a-b);
          dst[(y*w+x)*4+c] = window[Math.floor(window.length/2)];
        }
        dst[(y*w+x)*4+3] = src[(y*w+x)*4+3];
      }
    }
    return new ImageData(dst, w, h);
  }

  function applyScratchRemoval(imgData, strength) {
    const w = imgData.width, h = imgData.height, src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    const threshold = Math.max(15, 80 - strength * 0.6);
    for (let y = 1; y < h-1; y++) {
      for (let x = 2; x < w-2; x++) {
        const idx = (y*w+x)*4;
        for (let c = 0; c < 3; c++) {
          const val = src[idx+c];
          const leftAvg = (src[(y*w+x-2)*4+c] + src[(y*w+x-1)*4+c]) / 2;
          const rightAvg = (src[(y*w+x+1)*4+c] + src[(y*w+x+2)*4+c]) / 2;
          const neighborAvg = (leftAvg + rightAvg) / 2;
          if (Math.abs(val - neighborAvg) > threshold && strength > 20) {
            dst[idx+c] = Math.round(neighborAvg);
          }
        }
      }
    }
    return new ImageData(dst, w, h);
  }

  function applyContrastStretch(imgData, strength) {
    const w = imgData.width, h = imgData.height, src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    const clip = (100 - strength) * 0.005;
    // Find min/max with clipping
    for (let c = 0; c < 3; c++) {
      const hist = new Array(256).fill(0);
      for (let i = c; i < src.length; i += 4) hist[src[i]]++;
      const total = w * h;
      let minV = 0, maxV = 255, count = 0;
      for (let i = 0; i < 256; i++) { count += hist[i]; if (count > total * clip) { minV = i; break; } }
      count = 0;
      for (let i = 255; i >= 0; i--) { count += hist[i]; if (count > total * clip) { maxV = i; break; } }
      const range = maxV - minV;
      if (range > 1) {
        for (let i = c; i < src.length; i += 4) {
          dst[i] = Math.max(0, Math.min(255, Math.round((src[i] - minV) * 255 / range)));
        }
      }
    }
    return new ImageData(dst, w, h);
  }

  function applySharpen(imgData, strength) {
    const w = imgData.width, h = imgData.height;
    const amount = strength / 100 * 2;
    const kernel = [0, -amount, 0, -amount, 1 + 4*amount, -amount, 0, -amount, 0];
    const src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    for (let y = 1; y < h-1; y++) {
      for (let x = 1; x < w-1; x++) {
        for (let c = 0; c < 3; c++) {
          let val = 0;
          for (let ky = -1; ky <= 1; ky++) {
            for (let kx = -1; kx <= 1; kx++) {
              val += src[((y+ky)*w + (x+kx))*4 + c] * kernel[(ky+1)*3 + (kx+1)];
            }
          }
          dst[(y*w+x)*4+c] = Math.max(0, Math.min(255, val));
        }
      }
    }
    return new ImageData(dst, w, h);
  }

  function applyBrightness(imgData, amount) {
    const src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    const v = Math.round(amount * 2.55);
    for (let i = 0; i < src.length; i += 4) {
      dst[i] = Math.max(0, Math.min(255, src[i] + v));
      dst[i+1] = Math.max(0, Math.min(255, src[i+1] + v));
      dst[i+2] = Math.max(0, Math.min(255, src[i+2] + v));
    }
    return new ImageData(dst, imgData.width, imgData.height);
  }

  function applySepia(imgData, strength) {
    const src = imgData.data;
    const dst = new Uint8ClampedArray(src);
    const s = strength / 100;
    for (let i = 0; i < src.length; i += 4) {
      const r = src[i], g = src[i+1], b = src[i+2];
      const tr = 0.393*r + 0.769*g + 0.189*b;
      const tg = 0.349*r + 0.686*g + 0.168*b;
      const tb = 0.272*r + 0.534*g + 0.131*b;
      dst[i] = Math.round(r * (1-s) + tr * s);
      dst[i+1] = Math.round(g * (1-s) + tg * s);
      dst[i+2] = Math.round(b * (1-s) + tb * s);
    }
    return new ImageData(dst, imgData.width, imgData.height);
  }

  // ---- UI wiring ----

  function onSliderChange() {
    if (!origImage) return;
    document.getElementById('denoiseVal').textContent = document.getElementById('denoiseSlider').value;
    document.getElementById('scratchVal').textContent = document.getElementById('scratchSlider').value;
    document.getElementById('contrastVal').textContent = document.getElementById('contrastSlider').value;
    document.getElementById('sharpenVal').textContent = document.getElementById('sharpenSlider').value;
    document.getElementById('brightVal').textContent = document.getElementById('brightSlider').value;
    document.getElementById('sepiaVal').textContent = document.getElementById('sepiaSlider').value;
    applyFilters();
    if (isComparing) updateCompare();
  }

  function applyFilters() {
    if (!origImageData) return;
    let imgData = new ImageData(new Uint8ClampedArray(origImageData.data), origImageData.width, origImageData.height);
    const denoise = parseInt(document.getElementById('denoiseSlider').value);
    const scratch = parseInt(document.getElementById('scratchSlider').value);
    const contrast = parseInt(document.getElementById('contrastSlider').value);
    const sharpen = parseInt(document.getElementById('sharpenSlider').value);
    const bright = parseInt(document.getElementById('brightSlider').value);
    const sepia = parseInt(document.getElementById('sepiaSlider').value);
    if (denoise > 0) imgData = applyMedianFilter(imgData, denoise);
    if (scratch > 0) imgData = applyScratchRemoval(imgData, scratch);
    if (contrast > 0) imgData = applyContrastStretch(imgData, contrast);
    if (sharpen > 0) imgData = applySharpen(imgData, sharpen);
    if (bright !== 0) imgData = applyBrightness(imgData, bright);
    if (sepia > 0) imgData = applySepia(imgData, sepia);
    ctx.putImageData(imgData, 0, 0);
  }

  function applyPreset(name) {
    const presets = {
      'auto-restore': { denoise: 40, scratch: 60, contrast: 40, sharpen: 50, bright: 10, sepia: 0 },
      'remove-scratches': { denoise: 20, scratch: 80, contrast: 20, sharpen: 30, bright: 5, sepia: 0 },
      'reduce-noise': { denoise: 70, scratch: 20, contrast: 15, sharpen: 25, bright: 0, sepia: 0 },
      'sharpen-face': { denoise: 15, scratch: 20, contrast: 25, sharpen: 70, bright: 5, sepia: 0 },
      'enhance-contrast': { denoise: 10, scratch: 10, contrast: 70, sharpen: 40, bright: 10, sepia: 0 }
    };
    const p = presets[name]; if (!p) return;
    document.getElementById('denoiseSlider').value = p.denoise;
    document.getElementById('scratchSlider').value = p.scratch;
    document.getElementById('contrastSlider').value = p.contrast;
    document.getElementById('sharpenSlider').value = p.sharpen;
    document.getElementById('brightSlider').value = p.bright;
    document.getElementById('sepiaSlider').value = p.sepia;
    onSliderChange();
  }

  function resetSliders() {
    ['denoise','scratch','contrast','sharpen','sepia'].forEach(id => {
      document.getElementById(id+'Slider').value = 0;
      document.getElementById(id+'Val').textContent = '0';
    });
    document.getElementById('brightSlider').value = 0;
    document.getElementById('brightVal').textContent = '0';
    applyFilters();
  }

  function toggleCompare() {
    isComparing = document.getElementById('compareToggle').checked;
    document.getElementById('compareBox').style.display = isComparing ? 'block' : 'none';
    if (isComparing) setupCompare();
  }

  function setupCompare() {
    beforeCanvas = document.getElementById('beforeCanvas');
    afterCanvas = document.getElementById('afterCanvas');
    if (!origImage) return;
    const maxW = 800, maxH = 600;
    let w = previewCanvas.width, h = previewCanvas.height;
    beforeCanvas.width = afterCanvas.width = w;
    beforeCanvas.height = afterCanvas.height = h;
    beforeCanvas.getContext('2d').drawImage(origImage, 0, 0, w, h);
    updateCompare();
    const box = document.getElementById('compareBox');
    let dragging = false;
    const moveSlider = function(e) {
      const rect = box.getBoundingClientRect();
      let x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      x = Math.max(0, Math.min(rect.width, x));
      afterCanvas.style.clipPath = `inset(0 ${rect.width - x}px 0 0)`;
      document.getElementById('sliderHandle').style.left = x + 'px';
    };
    box.addEventListener('mousedown', e => { dragging = true; moveSlider(e); });
    box.addEventListener('touchstart', e => { dragging = true; moveSlider(e); });
    document.addEventListener('mousemove', e => { if (dragging) moveSlider(e); });
    document.addEventListener('touchmove', e => { if (dragging) moveSlider(e); });
    document.addEventListener('mouseup', () => dragging = false);
    document.addEventListener('touchend', () => dragging = false);
  }

  function updateCompare() {
    if (!afterCanvas) return;
    const aCtx = afterCanvas.getContext('2d');
    aCtx.clearRect(0, 0, afterCanvas.width, afterCanvas.height);
    aCtx.drawImage(previewCanvas, 0, 0);
  }

  function downloadImage() {
    const link = document.createElement('a');
    link.download = 'restored-photo.png';
    link.href = previewCanvas.toDataURL('image/png');
    link.click();
  }

  // Expose to global
  window.onSliderChange = onSliderChange;
  window.applyPreset = applyPreset;
  window.resetSliders = resetSliders;
  window.toggleCompare = toggleCompare;
  window.downloadImage = downloadImage;
})();
  </script>'''

pr_content = pr_content.replace(
    '  <script>\n\n  </script>',
    photo_script
)

with open(pr_path, 'w', encoding='utf-8') as f:
    f.write(pr_content)
print(f"Fixed: {pr_path}")

print("\nDone! Enhanced GIF Editor + Fixed Photo Restoration")
