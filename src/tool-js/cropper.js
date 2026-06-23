const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const sourceImg = document.getElementById('sourceImg');
    const cropOverlay = document.getElementById('cropOverlay');
    const cropWrapper = document.getElementById('cropWrapper');
    const ratioSelect = document.getElementById('ratioSelect');
    const cropBtn = document.getElementById('cropBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    let currentFile = null;

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        sourceImg.src = img.src;
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        downloadBtn.classList.add('hidden');
        setTimeout(initCropOverlay, 100);
      });
    }

    function initCropOverlay() {
      cropOverlay.style.top = '20%'; cropOverlay.style.left = '20%';
      cropOverlay.style.width = '60%'; cropOverlay.style.height = '60%';
      applyRatio();
    }

    ratioSelect.addEventListener('change', applyRatio);

    function applyRatio() {
      const ratio = ratioSelect.value;
      if (ratio === 'free') return;
      const [w, h] = ratio.split(':').map(Number);
      const ow = cropWrapper.offsetWidth;
      const oh = cropWrapper.offsetHeight;
      let nw = ow * 0.6, nh = nw * (h / w);
      if (nh > oh) { nh = oh * 0.6; nw = nh * (w / h); }
      cropOverlay.style.width = nw + 'px';
      cropOverlay.style.height = nh + 'px';
    }

    // Simple drag
    let dragging = false, dragStart = { x: 0, y: 0 }, elStart = { left: 0, top: 0 };
    cropOverlay.addEventListener('mousedown', e => {
      if (e.target.classList.contains('crop-handle')) return;
      dragging = true;
      dragStart = { x: e.clientX, y: e.clientY };
      elStart = { left: cropOverlay.offsetLeft, top: cropOverlay.offsetTop };
    });
    window.addEventListener('mousemove', e => {
      if (!dragging) return;
      const dx = e.clientX - dragStart.x, dy = e.clientY - dragStart.y;
      cropOverlay.style.left = Math.max(0, Math.min(cropWrapper.offsetWidth - cropOverlay.offsetWidth, elStart.left + dx)) + 'px';
      cropOverlay.style.top = Math.max(0, Math.min(cropWrapper.offsetHeight - cropOverlay.offsetHeight, elStart.top + dy)) + 'px';
    });
    window.addEventListener('mouseup', () => dragging = false);

    // Resize handle
    let resizing = false, resizeHandle = null, resizeStart = { x: 0, y: 0, w: 0, h: 0, l: 0, t: 0 };
    document.querySelectorAll('.crop-handle').forEach(h => {
      h.addEventListener('mousedown', e => {
        e.stopPropagation();
        resizing = true; resizeHandle = h.classList[1];
        resizeStart = { x: e.clientX, y: e.clientY, w: cropOverlay.offsetWidth, h: cropOverlay.offsetHeight, l: cropOverlay.offsetLeft, t: cropOverlay.offsetTop };
      });
    });
    window.addEventListener('mousemove', e => {
      if (!resizing) return;
      const dx = e.clientX - resizeStart.x, dy = e.clientY - resizeStart.y;
      if (resizeHandle === 'se') {
        cropOverlay.style.width = Math.max(30, resizeStart.w + dx) + 'px';
        cropOverlay.style.height = Math.max(30, resizeStart.h + dy) + 'px';
      }
      if (ratioSelect.value !== 'free') applyRatio();
    });
    window.addEventListener('mouseup', () => resizing = false);

    cropBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      cropBtn.disabled = true; cropBtn.textContent = '🔄 Cropping...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const scaleX = img.naturalWidth / cropWrapper.offsetWidth;
        const scaleY = img.naturalHeight / cropWrapper.offsetHeight;
        const sx = Math.round(cropOverlay.offsetLeft * scaleX);
        const sy = Math.round(cropOverlay.offsetTop * scaleY);
        const sw = Math.round(cropOverlay.offsetWidth * scaleX);
        const sh = Math.round(cropOverlay.offsetHeight * scaleY);
        const canvas = ImageUtils.createCanvas(sw, sh);
        canvas.getContext('2d').drawImage(img, sx, sy, sw, sh, 0, 0, sw, sh);
        const blob = await ImageUtils.canvasToBlob(canvas, currentFile.type, 0.95);
        sourceImg.src = canvas.toDataURL();
        cropOverlay.style.display = 'none';
        downloadBtn.classList.remove('hidden');
        downloadBtn.onclick = () => ImageUtils.download(blob, currentFile.name.replace(/\.[^.]+$/, '-cropped.png'));
        status.textContent = 'Cropped to ' + sw + '×' + sh;
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        cropBtn.disabled = false; cropBtn.textContent = '✂️ Crop';
      }
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null;
      previewArea.classList.remove('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.remove('hidden');
      dropzone.classList.remove('hidden');
      fileInput.value = ''; status.textContent = '';
      downloadBtn.classList.add('hidden');
      cropOverlay.style.display = '';
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();