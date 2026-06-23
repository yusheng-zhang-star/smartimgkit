const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const origImg = document.getElementById('origImg');
    const compImg = document.getElementById('compImg');
    const origSize = document.getElementById('origSize');
    const compSize = document.getElementById('compSize');
    const qualityRange = document.getElementById('qualityRange');
    const qualityVal = document.getElementById('qualityVal');
    const compressBtn = document.getElementById('compressBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    let currentFile = null;
    let resultBlob = null;

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    qualityRange.addEventListener('input', () => qualityVal.textContent = qualityRange.value + '%');

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        origImg.src = img.src;
        origSize.textContent = ImageUtils.formatBytes(file.size) + ' — ' + img.naturalWidth + '×' + img.naturalHeight;
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        downloadBtn.classList.add('hidden');
        compImg.src = '';
        compSize.textContent = '';
      });
    }

    compressBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      compressBtn.disabled = true;
      compressBtn.textContent = '🔄 Compressing...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const canvas = ImageUtils.createCanvas(img.naturalWidth, img.naturalHeight);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        const quality = parseInt(qualityRange.value) / 100;
        const outType = currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg';
        const blob = await ImageUtils.canvasToBlob(canvas, outType, quality);
        resultBlob = blob;
        const url = URL.createObjectURL(blob);
        compImg.src = url;
        compSize.textContent = ImageUtils.formatBytes(blob.size) + ' — Saved ' + Math.round((1 - blob.size / currentFile.size) * 100) + '%';
        downloadBtn.classList.remove('hidden');
        status.textContent = '';
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        compressBtn.disabled = false;
        compressBtn.textContent = '🗜️ Compress';
      }
    });

    downloadBtn.addEventListener('click', () => {
      if (resultBlob) {
        const ext = currentFile.name.split('.').pop();
        const base = currentFile.name.replace(/\.[^.]+$/, '');
        ImageUtils.download(resultBlob, base + '-compressed.' + ext);
      }
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null; resultBlob = null;
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
      window.initSampleButton('https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();