// ===== State =====
    let originalImg = null;
    let rotation = 0;    // degrees
    let flipH = false;
    let flipV = false;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const previewCanvas = document.getElementById('previewCanvas');
    const ctx = previewCanvas.getContext('2d');
    const angleSlider = document.getElementById('angleSlider');
    const angleValue = document.getElementById('angleValue');
    const bgColor = document.getElementById('bgColor');
    const outputFormat = document.getElementById('outputFormat');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    // ===== Upload =====
    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    async function handleFile(file) {
      if (!file.type.startsWith('image/')) return;
      originalImg = await ImageUtils.load(file);
      rotation = 0; flipH = false; flipV = false;
      angleSlider.value = 0;
      angleValue.textContent = '0';
      dropzone.classList.add('hidden');
      workspace.style.display = '';
      renderPreview();
    }

    // ===== Quick Rotate =====
    document.getElementById('rotateLeftBtn').addEventListener('click', () => {
      rotation = (rotation - 90 + 360) % 360;
      angleSlider.value = rotation;
      angleValue.textContent = rotation;
      renderPreview();
    });
    document.getElementById('rotateRightBtn').addEventListener('click', () => {
      rotation = (rotation + 90) % 360;
      angleSlider.value = rotation;
      angleValue.textContent = rotation;
      renderPreview();
    });
    document.getElementById('rotate180Btn').addEventListener('click', () => {
      rotation = (rotation + 180) % 360;
      angleSlider.value = rotation;
      angleValue.textContent = rotation;
      renderPreview();
    });
    document.getElementById('resetAngleBtn').addEventListener('click', () => {
      rotation = 0; flipH = false; flipV = false;
      angleSlider.value = 0;
      angleValue.textContent = '0';
      renderPreview();
    });

    // ===== Custom Angle =====
    angleSlider.addEventListener('input', () => {
      rotation = parseInt(angleSlider.value);
      angleValue.textContent = rotation;
      renderPreview();
    });

    // ===== Flip =====
    document.getElementById('flipHBtn').addEventListener('click', () => {
      flipH = !flipH;
      renderPreview();
    });
    document.getElementById('flipVBtn').addEventListener('click', () => {
      flipV = !flipV;
      renderPreview();
    });

    // ===== BG Color =====
    bgColor.addEventListener('input', () => renderPreview());

    // ===== Preview Render =====
    function renderPreview() {
      if (!originalImg) return;
      const w = originalImg.naturalWidth;
      const h = originalImg.naturalHeight;
      const rad = rotation * Math.PI / 180;

      // Calculate bounding box of rotated image
      const cos = Math.abs(Math.cos(rad));
      const sin = Math.abs(Math.sin(rad));
      const newW = Math.ceil(w * cos + h * sin);
      const newH = Math.ceil(w * sin + h * cos);

      previewCanvas.width = newW;
      previewCanvas.height = newH;

      // Fill background
      ctx.fillStyle = bgColor.value;
      ctx.fillRect(0, 0, newW, newH);

      // Transform
      ctx.save();
      ctx.translate(newW / 2, newH / 2);
      ctx.rotate(rad);
      ctx.scale(flipH ? -1 : 1, flipV ? -1 : 1);
      ctx.drawImage(originalImg, -w / 2, -h / 2, w, h);
      ctx.restore();
    }

    // ===== Download =====
    downloadBtn.addEventListener('click', async () => {
      if (!originalImg) return;
      downloadBtn.disabled = true;
      downloadBtn.textContent = '🔄 Processing...';
      status.textContent = '';
      try {
        const format = outputFormat.value;
        const quality = format === 'image/png' ? undefined : 0.92;
        const blob = await ImageUtils.canvasToBlob(previewCanvas, format, quality);
        const ext = format === 'image/png' ? 'png' : format === 'image/jpeg' ? 'jpg' : 'webp';
        ImageUtils.download(blob, `rotated-image.${ext}`);
        status.textContent = '✅ Image downloaded!';
      } catch (e) {
        status.textContent = '❌ Error: ' + e.message;
      }
      downloadBtn.disabled = false;
      downloadBtn.textContent = '💾 Download';
    });

    // ===== Reset =====
    resetBtn.addEventListener('click', () => {
      originalImg = null;
      rotation = 0; flipH = false; flipV = false;
      workspace.style.display = 'none';
      dropzone.classList.remove('hidden');
      fileInput.value = '';
      status.textContent = '';
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1475924156734-278096522a22?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();