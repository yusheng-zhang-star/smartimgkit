// ===== State =====
    let originalImg = null;
    let scaleFactor = 2;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const previewCanvas = document.getElementById('previewCanvas');
    const ctx = previewCanvas.getContext('2d');
    const sharpenSlider = document.getElementById('sharpenSlider');
    const sharpenValue = document.getElementById('sharpenValue');
    const origDim = document.getElementById('origDim');
    const newDim = document.getElementById('newDim');
    const outputFormat = document.getElementById('outputFormat');
    const upscaleBtn = document.getElementById('upscaleBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    // ===== Upload =====
    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    async function handleFile(file) {
      if (!file.type.startsWith('image/')) return;
      originalImg = await ImageUtils.load(file);
      dropzone.classList.add('hidden');
      workspace.style.display = '';
      updateDims();
      renderPreview();
    }

    // ===== Scale Buttons =====
    document.querySelectorAll('.scale-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.scale-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        scaleFactor = parseInt(btn.dataset.scale);
        updateDims();
        renderPreview();
      });
    });

    // ===== Sharpening =====
    sharpenSlider.addEventListener('input', () => {
      sharpenValue.textContent = sharpenSlider.value;
      renderPreview();
    });

    // ===== Dimension Display =====
    function updateDims() {
      if (!originalImg) return;
      const w = originalImg.naturalWidth;
      const h = originalImg.naturalHeight;
      origDim.textContent = `${w} × ${h}`;
      newDim.textContent = `${w * scaleFactor} × ${h * scaleFactor}`;
    }

    // ===== Preview Render =====
    function renderPreview() {
      if (!originalImg) return;
      const w = originalImg.naturalWidth;
      const h = originalImg.naturalHeight;
      const nw = w * scaleFactor;
      const nh = h * scaleFactor;

      previewCanvas.width = nw;
      previewCanvas.height = nh;

      // High-quality interpolation
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(originalImg, 0, 0, nw, nh);

      // Apply unsharp mask sharpening
      const strength = parseInt(sharpenSlider.value) / 100;
      if (strength > 0) applySharpen(ctx, nw, nh, strength);
    }

    // ===== Unsharp Mask Sharpening =====
    function applySharpen(ctx, w, h, strength) {
      const imageData = ctx.getImageData(0, 0, w, h);
      const data = imageData.data;

      // Create blurred version
      const blurred = new Uint8ClampedArray(data.length);
      const kernel = [1, 2, 1, 2, 4, 2, 1, 2, 1];
      const kSum = 16;

      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          for (let c = 0; c < 3; c++) {
            let sum = 0;
            let ki = 0;
            for (let ky = -1; ky <= 1; ky++) {
              for (let kx = -1; kx <= 1; kx++) {
                const idx = ((y + ky) * w + (x + kx)) * 4 + c;
                sum += data[idx] * kernel[ki++];
              }
            }
            blurred[(y * w + x) * 4 + c] = sum / kSum;
          }
          blurred[(y * w + x) * 4 + 3] = data[(y * w + x) * 4 + 3];
        }
      }

      // Unsharp mask: sharpened = original + strength * (original - blurred)
      const amount = strength * 1.5; // max 1.5x sharpening
      for (let i = 0; i < data.length; i += 4) {
        for (let c = 0; c < 3; c++) {
          const diff = data[i + c] - blurred[i + c];
          data[i + c] = Math.min(255, Math.max(0, data[i + c] + diff * amount));
        }
      }

      ctx.putImageData(imageData, 0, 0);
    }

    // ===== Upscale & Download =====
    upscaleBtn.addEventListener('click', async () => {
      if (!originalImg) return;
      upscaleBtn.disabled = true;
      upscaleBtn.textContent = '🔄 Upscaling...';
      status.textContent = '';

      try {
        const format = outputFormat.value;
        const quality = format === 'image/png' ? undefined : 0.92;
        const blob = await ImageUtils.canvasToBlob(previewCanvas, format, quality);
        const ext = format === 'image/png' ? 'png' : format === 'image/jpeg' ? 'jpg' : 'webp';
        ImageUtils.download(blob, `upscaled-${scaleFactor}x.${ext}`);
        status.textContent = `✅ Image upscaled to ${scaleFactor}x and downloaded!`;
      } catch (e) {
        status.textContent = '❌ Error: ' + e.message;
      }

      upscaleBtn.disabled = false;
      upscaleBtn.textContent = '🔍 Upscale & Download';
    });

    // ===== Reset =====
    resetBtn.addEventListener('click', () => {
      originalImg = null;
      workspace.style.display = 'none';
      dropzone.classList.remove('hidden');
      fileInput.value = '';
      status.textContent = '';
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1518173946687-a1e4e3e3f6be?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();