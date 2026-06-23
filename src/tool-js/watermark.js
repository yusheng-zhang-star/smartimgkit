const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const canvas = document.getElementById('canvas');
    const textModeBtn = document.getElementById('textModeBtn');
    const imgModeBtn = document.getElementById('imgModeBtn');
    const textControls = document.getElementById('textControls');
    const imgControls = document.getElementById('imgControls');
    const wmText = document.getElementById('wmText');
    const wmColor = document.getElementById('wmColor');
    const wmSize = document.getElementById('wmSize');
    const wmOp = document.getElementById('wmOp');
    const wmImgInput = document.getElementById('wmImgInput');
    const wmImgOp = document.getElementById('wmImgOp');
    const wmPos = document.getElementById('wmPos');
    const applyBtn = document.getElementById('applyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    let currentFile = null, sourceImg = null, wmImage = null, mode = 'text';

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    textModeBtn.addEventListener('click', () => { mode = 'text'; textControls.classList.remove('hidden'); imgControls.classList.add('hidden'); });
    imgModeBtn.addEventListener('click', () => { mode = 'image'; textControls.classList.add('hidden'); imgControls.classList.remove('hidden'); });

    wmImgInput.addEventListener('change', async () => {
      if (wmImgInput.files[0]) wmImage = await ImageUtils.load(wmImgInput.files[0]);
    });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        sourceImg = img;
        canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
        canvas.getContext('2d').drawImage(img, 0, 0);
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        downloadBtn.classList.add('hidden');
      });
    }

    applyBtn.addEventListener('click', async () => {
      if (!sourceImg) return;
      applyBtn.disabled = true;
      applyBtn.textContent = '🔄 Applying...';
      status.innerHTML = '<div class="spinner"></div>';
      const ctx = canvas.getContext('2d');
      ctx.drawImage(sourceImg, 0, 0);
      const pos = wmPos.value;
      let x = 0, y = 0;
      const pad = 20;
      if (mode === 'text') {
        const size = parseInt(wmSize.value) || 48;
        ctx.font = size + 'px sans-serif';
        ctx.globalAlpha = (parseInt(wmOp.value) || 50) / 100;
        ctx.fillStyle = wmColor.value;
        const metrics = ctx.measureText(wmText.value);
        if (pos === 'bottom-right') { x = canvas.width - metrics.width - pad; y = canvas.height - pad; }
        else if (pos === 'bottom-left') { x = pad; y = canvas.height - pad; }
        else if (pos === 'top-right') { x = canvas.width - metrics.width - pad; y = size + pad; }
        else if (pos === 'top-left') { x = pad; y = size + pad; }
        else if (pos === 'center') { x = (canvas.width - metrics.width) / 2; y = canvas.height / 2; }
        ctx.fillText(wmText.value, x, y);
      } else if (mode === 'image' && wmImage) {
        const op = (parseInt(wmImgOp.value) || 50) / 100;
        const iw = canvas.width * 0.2, ih = iw * (wmImage.naturalHeight / wmImage.naturalWidth);
        ctx.globalAlpha = op;
        if (pos === 'bottom-right') { x = canvas.width - iw - pad; y = canvas.height - ih - pad; }
        else if (pos === 'bottom-left') { x = pad; y = canvas.height - ih - pad; }
        else if (pos === 'top-right') { x = canvas.width - iw - pad; y = pad; }
        else if (pos === 'top-left') { x = pad; y = pad; }
        else if (pos === 'center') { x = (canvas.width - iw) / 2; y = (canvas.height - ih) / 2; }
        ctx.drawImage(wmImage, x, y, iw, ih);
      }
      ctx.globalAlpha = 1;
      const blob = await ImageUtils.canvasToBlob(canvas, currentFile.type, 0.92);
      downloadBtn.classList.remove('hidden');
      downloadBtn.onclick = () => ImageUtils.download(blob, currentFile.name.replace(/\.[^.]+$/, '-watermarked.png'));
      status.textContent = 'Watermark applied!';
      applyBtn.disabled = false;
      applyBtn.textContent = '🔏 Apply Watermark';
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null; sourceImg = null; wmImage = null;
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
      window.initSampleButton('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();