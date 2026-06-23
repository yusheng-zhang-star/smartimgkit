const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImg = document.getElementById('previewImg');
    const keepRatio = document.getElementById('keepRatio');
    const widthInput = document.getElementById('widthInput');
    const heightInput = document.getElementById('heightInput');
    const pctRange = document.getElementById('pctRange');
    const pctVal = document.getElementById('pctVal');
    const resizeBtn = document.getElementById('resizeBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    let currentFile = null, origW = 0, origH = 0, resultBlob = null;

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        origW = img.naturalWidth; origH = img.naturalHeight;
        previewImg.src = img.src;
        widthInput.value = origW; heightInput.value = origH;
        pctRange.value = 100; pctVal.textContent = '100%';
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        downloadBtn.classList.add('hidden');
      });
    }

    keepRatio.addEventListener('change', () => {
      if (keepRatio.checked && origW) { heightInput.value = Math.round(parseInt(widthInput.value||0) * (origH/origW)); }
    });
    widthInput.addEventListener('input', () => {
      if (keepRatio.checked && origW) { heightInput.value = Math.round(parseInt(widthInput.value||0) * (origH/origW)); }
    });
    heightInput.addEventListener('input', () => {
      if (keepRatio.checked && origH) { widthInput.value = Math.round(parseInt(heightInput.value||0) * (origW/origH)); }
    });
    pctRange.addEventListener('input', () => {
      pctVal.textContent = pctRange.value + '%';
      if (origW) { widthInput.value = Math.round(origW * pctRange.value / 100); heightInput.value = Math.round(origH * pctRange.value / 100); }
    });

    resizeBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      const w = parseInt(widthInput.value) || origW;
      const h = parseInt(heightInput.value) || origH;
      resizeBtn.disabled = true;
      resizeBtn.textContent = '🔄 Resizing...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const canvas = ImageUtils.createCanvas(w, h);
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        const blob = await ImageUtils.canvasToBlob(canvas, currentFile.type, 0.92);
        resultBlob = blob;
        previewImg.src = canvas.toDataURL();
        downloadBtn.classList.remove('hidden');
        status.textContent = 'Resized to ' + w + '×' + h;
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        resizeBtn.disabled = false;
        resizeBtn.textContent = '📐 Resize';
      }
    });

    downloadBtn.addEventListener('click', () => {
      if (resultBlob) {
        const ext = currentFile.name.split('.').pop();
        const base = currentFile.name.replace(/\.[^.]+$/, '');
        ImageUtils.download(resultBlob, base + '-resized.' + ext);
      }
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null; resultBlob = null; origW = 0; origH = 0;
      previewArea.classList.remove('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.remove('hidden');
      dropzone.classList.remove('hidden');
      fileInput.value = ''; status.textContent = '';
      downloadBtn.classList.add('hidden');
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();