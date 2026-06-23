// ===== Paper size presets (width × height in inches) =====
    const PAPER = {
      a4:         { w: 8.2677,  h: 11.6929, label: 'A4 (210×297mm)' },
      letter:     { w: 8.5,     h: 11,      label: 'Letter (8.5×11")' },
      a5:         { w: 5.8268,  h: 8.2677,  label: 'A5 (148×210mm)' },
      '4x6':      { w: 4,       h: 6,       label: '4×6" (10×15cm)' },
      '5x7':      { w: 5,       h: 7,       label: '5×7" (13×18cm)' },
      business:   { w: 3.5,     h: 2,       label: 'Business Card (3.5×2")' },
      custom:     null,
    };

    // ===== State =====
    let originalImg = null;
    let activePreset = null;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');
    const presetGrid = document.getElementById('presetGrid');
    const customSizeDiv = document.getElementById('customSize');
    const dpiSelect = document.getElementById('dpiSelect');
    const outputFormat = document.getElementById('outputFormat');
    const dimensionInfo = document.getElementById('dimensionInfo');

    // ===== Init Preset Buttons =====
    presetGrid.querySelectorAll('.preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activePreset = btn.dataset.preset;
        customSizeDiv.style.display = activePreset === 'custom' ? '' : 'none';
        if (originalImg) renderPreview();
      });
    });

    // ===== File Upload =====
    setupDropzone({
      dropzoneId: 'dropzone',
      inputId: 'fileInput',
      onFile: async (file) => {
        try {
          originalImg = await ImageUtils.load(file);
          dropzone.style.display = 'none';
          workspace.style.display = 'block';
          // Auto-select A4
          if (!activePreset) {
            document.querySelector('[data-preset="a4"]').click();
          } else {
            renderPreview();
          }
        } catch (e) {
          ImageUtils.showToast('Failed to load image', 'error');
        }
      }
    });

    // ===== DPI / Format change =====
    dpiSelect.addEventListener('change', () => { if (originalImg) renderPreview(); });
    outputFormat.addEventListener('change', () => { if (originalImg) renderPreview(); });
    document.getElementById('customW').addEventListener('input', () => { if (activePreset === 'custom' && originalImg) renderPreview(); });
    document.getElementById('customH').addEventListener('input', () => { if (activePreset === 'custom' && originalImg) renderPreview(); });

    // ===== Reset =====
    document.getElementById('resetBtn').addEventListener('click', () => {
      originalImg = null;
      workspace.style.display = 'none';
      dropzone.style.display = '';
      fileInput.value = '';
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      activePreset = null;
      customSizeDiv.style.display = 'none';
      dimensionInfo.style.display = 'none';
    });

    // ===== Download =====
    document.getElementById('downloadBtn').addEventListener('click', () => {
      const mime = outputFormat.value;
      const ext = mime === 'image/jpeg' ? 'jpg' : 'png';
      const preset = PAPER[activePreset];
      const label = preset ? preset.label.replace(/[^a-zA-Z0-9]/g, '_') : 'custom';
      ImageUtils.download(canvas, 'print-ready_' + label + '.' + ext, mime);
      ImageUtils.showToast('Image downloaded!');
    });

    // ===== Render =====
    function renderPreview() {
      if (!originalImg || !activePreset) return;

      const dpi = parseInt(dpiSelect.value);
      let pw, ph; // paper width/height in inches

      if (activePreset === 'custom') {
        pw = parseFloat(document.getElementById('customW').value) || 8.5;
        ph = parseFloat(document.getElementById('customH').value) || 11;
      } else {
        const p = PAPER[activePreset];
        if (!p) return;
        pw = p.w; ph = p.h;
      }

      const canvasW = Math.round(pw * dpi);
      const canvasH = Math.round(ph * dpi);

      canvas.width = canvasW;
      canvas.height = canvasH;

      // White background (print-ready)
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvasW, canvasH);

      // Fit original image into canvas (contain, center)
      const imgW = originalImg.width;
      const imgH = originalImg.height;
      const ratio = Math.min(canvasW / imgW, canvasH / imgH);
      const drawW = Math.round(imgW * ratio);
      const drawH = Math.round(imgH * ratio);
      const offX = Math.round((canvasW - drawW) / 2);
      const offY = Math.round((canvasH - drawH) / 2);

      ctx.drawImage(originalImg, offX, offY, drawW, drawH);

      // Update info
      dimensionInfo.style.display = 'flex';
      document.getElementById('outDims').textContent = canvasW + ' × ' + canvasH + ' px';
      document.getElementById('printSize').textContent = pw.toFixed(2) + '" × ' + ph.toFixed(2) + '" @ ' + dpi + ' DPI';

      // Estimate file size
      const mime = outputFormat.value;
      const estBytes = mime === 'image/jpeg'
        ? Math.round(canvasW * canvasH * 0.15)
        : Math.round(canvasW * canvasH * 3);
      document.getElementById('estSize').textContent = ImageUtils.formatBytes(estBytes);
    }
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();