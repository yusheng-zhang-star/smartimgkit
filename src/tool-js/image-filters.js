// ===== State =====
    let originalImg = null;
    let activePreset = 'none';

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');

    const brightnessSlider = document.getElementById('brightness');
    const contrastSlider = document.getElementById('contrast');
    const saturationSlider = document.getElementById('saturation');
    const blurSlider = document.getElementById('blur');
    const hueSlider = document.getElementById('hueRotate');
    const opacitySlider = document.getElementById('opacity');
    const outputFormat = document.getElementById('outputFormat');

    // ===== Preset Filters =====
    const PRESETS = {
      none:       { brightness:100, contrast:100, saturation:100, blur:0, hueRotate:0, opacity:100 },
      grayscale:   { brightness:100, contrast:110, saturation:0,   blur:0, hueRotate:0, opacity:100 },
      sepia:       { brightness:105, contrast:110, saturation:0,   blur:0, hueRotate:0, opacity:100, sepia: true },
      invert:      { brightness:100, contrast:100, saturation:100, blur:0, hueRotate:0, opacity:100, invert:true },
      blur:        { brightness:100, contrast:100, saturation:100, blur:8, hueRotate:0, opacity:100 },
      vintage:     { brightness:110, contrast:90,  saturation:60,  blur:1, hueRotate:0, opacity:100, sepia:true },
      cool:        { brightness:100, contrast:110, saturation:80,  blur:0, hueRotate:180, opacity:100 },
      warm:        { brightness:105, contrast:105, saturation:120, blur:0, hueRotate:30, opacity:100 },
      vibrant:    { brightness:105, contrast:120, saturation:180, blur:0, hueRotate:0, opacity:100 },
      polaroid:    { brightness:108, contrast:95,  saturation:85,  blur:0, hueRotate:0, opacity:100, sepia:true },
      emboss:      { brightness:100, contrast:150, saturation:0,   blur:0, hueRotate:0, opacity:100 },
      sharpen:     { brightness:100, contrast:130, saturation:110, blur:0, hueRotate:0, opacity:100 },
      'hue-rotate': { brightness:100, contrast:100, saturation:100, blur:0, hueRotate:180, opacity:100 },
      saturate:    { brightness:100, contrast:110, saturation:250, blur:0, hueRotate:0, opacity:100 },
    };

    // ===== Init Preset Buttons =====
    document.querySelectorAll('.filter-preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-preset-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activePreset = btn.dataset.filter;
        applyPreset(activePreset);
        renderPreview();
      });
    });

    function applyPreset(name) {
      const p = PRESETS[name];
      if (!p) return;
      brightnessSlider.value = p.brightness;
      contrastSlider.value = p.contrast;
      saturationSlider.value = p.saturation;
      blurSlider.value = p.blur;
      hueSlider.value = p.hueRotate;
      opacitySlider.value = p.opacity;
      updateSliderLabels();
    }

    function updateSliderLabels() {
      document.getElementById('brightnessVal').textContent = brightnessSlider.value + '%';
      document.getElementById('contrastVal').textContent = contrastSlider.value + '%';
      document.getElementById('saturationVal').textContent = saturationSlider.value + '%';
      document.getElementById('blurVal').textContent = blurSlider.value + 'px';
      document.getElementById('hueVal').textContent = hueSlider.value + '°';
      document.getElementById('opacityVal').textContent = opacitySlider.value + '%';
    }

    // ===== Slider Events =====
    [brightnessSlider, contrastSlider, saturationSlider, blurSlider, hueSlider, opacitySlider].forEach(slider => {
      slider.addEventListener('input', () => {
        updateSliderLabels();
        // Clear active preset when user manually adjusts
        document.querySelectorAll('.filter-preset-btn').forEach(b => b.classList.remove('active'));
        activePreset = null;
        renderPreview();
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
          renderPreview();
        } catch (e) {
          ImageUtils.showToast('Failed to load image', 'error');
        }
      }
    });

    // ===== Reset =====
    document.getElementById('resetBtn').addEventListener('click', () => {
      originalImg = null;
      workspace.style.display = 'none';
      dropzone.style.display = '';
      fileInput.value = '';
      applyPreset('none');
      document.querySelectorAll('.filter-preset-btn').forEach(b => b.classList.remove('active'));
      document.querySelector('[data-filter="none"]').classList.add('active');
      activePreset = 'none';
    });

    // ===== Download =====
    document.getElementById('downloadBtn').addEventListener('click', () => {
      const mime = outputFormat.value;
      const ext = mime === 'image/jpeg' ? 'jpg' : mime === 'image/webp' ? 'webp' : 'png';
      ImageUtils.download(canvas, 'filtered-image.' + ext, mime);
      ImageUtils.showToast('Image downloaded!');
    });

    // ===== Render =====
    function renderPreview() {
      if (!originalImg) return;
      const w = originalImg.width;
      const h = originalImg.height;
      canvas.width = w;
      canvas.height = h;
      ctx.clearRect(0, 0, w, h);

      // Build Canvas filter string
      const b = brightnessSlider.value;
      const c = contrastSlider.value;
      const s = saturationSlider.value;
      const bl = blurSlider.value;
      const hR = hueSlider.value;
      const o = opacitySlider.value;

      let filterStr = '';
      if (b != 100) filterStr += 'brightness(' + b + '%) ';
      if (c != 100) filterStr += 'contrast(' + c + '%) ';
      if (s != 100) filterStr += 'saturate(' + s + '%) ';
      if (bl > 0) filterStr += 'blur(' + bl + 'px) ';
      if (hR != 0) filterStr += 'hue-rotate(' + hR + 'deg) ';
      if (o != 100) filterStr += 'opacity(' + o + '%) ';

      // Handle special presets that need extra effects
      const preset = activePreset ? PRESETS[activePreset] : null;
      if (preset && preset.sepia) filterStr += 'sepia(100%) ';
      if (preset && preset.invert) filterStr += 'invert(100%) ';

      ctx.filter = filterStr.trim() || 'none';
      ctx.drawImage(originalImg, 0, 0, w, h);
      ctx.filter = 'none';

      document.getElementById('outSize').textContent = w + ' x ' + h;
    }

    // Init slider labels
    updateSliderLabels();
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1470252649199-925c5e8b0f4b?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();