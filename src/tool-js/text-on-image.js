// ===== State =====
    let originalImg = null;
    let textX = 0.5;  // proportional position (0-1)
    let textY = 0.5;
    let isDragging = false;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const previewCanvas = document.getElementById('previewCanvas');
    const ctx = previewCanvas.getContext('2d');
    const canvasWrapper = document.getElementById('canvasWrapper');
    const textInput = document.getElementById('textInput');
    const fontFamily = document.getElementById('fontFamily');
    const fontSize = document.getElementById('fontSize');
    const sizeValue = document.getElementById('sizeValue');
    const fontWeight = document.getElementById('fontWeight');
    const textColor = document.getElementById('textColor');
    const outlineColor = document.getElementById('outlineColor');
    const outlineWidth = document.getElementById('outlineWidth');
    const outlineValue = document.getElementById('outlineValue');
    const shadowBlur = document.getElementById('shadowBlur');
    const shadowValue = document.getElementById('shadowValue');
    const opacity = document.getElementById('opacity');
    const opacityValue = document.getElementById('opacityValue');
    const rotation = document.getElementById('rotation');
    const rotationValue = document.getElementById('rotationValue');
    const outputFormat = document.getElementById('outputFormat');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    // ===== Upload =====
    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    async function handleFile(file) {
      if (!file.type.startsWith('image/')) return;
      originalImg = await ImageUtils.load(file);
      textX = 0.5; textY = 0.5;
      dropzone.classList.add('hidden');
      workspace.style.display = '';
      renderPreview();
    }

    // ===== Controls =====
    const liveControls = [textInput, fontFamily, fontWeight, textColor, outlineColor];
    liveControls.forEach(el => el.addEventListener('input', () => renderPreview()));

    const sliderControls = [
      [fontSize, sizeValue], [outlineWidth, outlineValue],
      [shadowBlur, shadowValue], [opacity, opacityValue], [rotation, rotationValue]
    ];
    sliderControls.forEach(([slider, display]) => {
      slider.addEventListener('input', () => { display.textContent = slider.value; renderPreview(); });
    });

    // ===== Quick Position =====
    document.querySelectorAll('.pos-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.pos-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        textX = parseFloat(btn.dataset.x);
        textY = parseFloat(btn.dataset.y);
        renderPreview();
      });
    });

    // ===== Drag on Canvas =====
    previewCanvas.addEventListener('mousedown', startDrag);
    previewCanvas.addEventListener('touchstart', startDrag, { passive: false });

    function startDrag(e) {
      e.preventDefault();
      isDragging = true;
      moveDrag(e);
      document.addEventListener('mousemove', moveDrag);
      document.addEventListener('mouseup', stopDrag);
      document.addEventListener('touchmove', moveDrag, { passive: false });
      document.addEventListener('touchend', stopDrag);
    }

    function moveDrag(e) {
      if (!isDragging || !originalImg) return;
      e.preventDefault();
      const rect = previewCanvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      textX = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
      textY = Math.max(0, Math.min(1, (clientY - rect.top) / rect.height));
      document.querySelectorAll('.pos-btn').forEach(b => b.classList.remove('active'));
      renderPreview();
    }

    function stopDrag() {
      isDragging = false;
      document.removeEventListener('mousemove', moveDrag);
      document.removeEventListener('mouseup', stopDrag);
      document.removeEventListener('touchmove', moveDrag);
      document.removeEventListener('touchend', stopDrag);
    }

    // ===== Preview Render =====
    function renderPreview() {
      if (!originalImg) return;
      const w = originalImg.naturalWidth;
      const h = originalImg.naturalHeight;

      previewCanvas.width = w;
      previewCanvas.height = h;
      ctx.drawImage(originalImg, 0, 0, w, h);

      const text = textInput.value;
      if (!text) return;

      const fSize = parseInt(fontSize.value);
      const fWeight = fontWeight.value;
      const fFamily = fontFamily.value;
      const tColor = textColor.value;
      const oColor = outlineColor.value;
      const oWidth = parseInt(outlineWidth.value);
      const sBlur = parseInt(shadowBlur.value);
      const alpha = parseInt(opacity.value) / 100;
      const rot = parseInt(rotation.value) * Math.PI / 180;

      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.font = `${fWeight} ${fSize}px "${fFamily}"`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const px = textX * w;
      const py = textY * h;

      ctx.translate(px, py);
      ctx.rotate(rot);

      // Shadow
      if (sBlur > 0) {
        ctx.shadowColor = 'rgba(0,0,0,0.6)';
        ctx.shadowBlur = sBlur;
        ctx.shadowOffsetX = Math.round(sBlur / 4);
        ctx.shadowOffsetY = Math.round(sBlur / 4);
      }

      // Draw multiline text
      const lines = text.split('\n');
      const lineHeight = fSize * 1.3;
      const totalHeight = lineHeight * lines.length;
      const startY = -(totalHeight / 2) + lineHeight / 2;

      lines.forEach((line, i) => {
        const ly = startY + i * lineHeight;

        // Outline
        if (oWidth > 0) {
          ctx.strokeStyle = oColor;
          ctx.lineWidth = oWidth * 2;
          ctx.lineJoin = 'round';
          ctx.miterLimit = 2;
          ctx.strokeText(line, 0, ly);
        }

        // Fill
        ctx.fillStyle = tColor;
        ctx.fillText(line, 0, ly);
      });

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
        ImageUtils.download(blob, `text-on-image.${ext}`);
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
      workspace.style.display = 'none';
      dropzone.classList.remove('hidden');
      fileInput.value = '';
      textInput.value = 'Hello World';
      status.textContent = '';
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();