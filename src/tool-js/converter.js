const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImg = document.getElementById('previewImg');
    const formatSelect = document.getElementById('formatSelect');
    const convertBtn = document.getElementById('convertBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    let currentFile = null;
    let resultBlob = null;

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        previewImg.src = img.src;
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        downloadBtn.classList.add('hidden');
      });
    }

    convertBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      convertBtn.disabled = true;
      convertBtn.textContent = '🔄 Converting...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const canvas = ImageUtils.createCanvas(img.naturalWidth, img.naturalHeight);
        canvas.getContext('2d').drawImage(img, 0, 0);
        const format = formatSelect.value;
        const blob = await ImageUtils.canvasToBlob(canvas, format, 0.92);
        resultBlob = blob;
        downloadBtn.classList.remove('hidden');
        status.textContent = 'Converted to ' + format.split('/')[1].toUpperCase() + ' — ' + ImageUtils.formatBytes(blob.size);
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        convertBtn.disabled = false;
        convertBtn.textContent = '🔄 Convert';
      }
    });

    downloadBtn.addEventListener('click', () => {
      if (resultBlob) {
        const ext = formatSelect.value.split('/')[1];
        const base = currentFile.name.replace(/\.[^.]+$/, '');
        ImageUtils.download(resultBlob, base + '.' + ext);
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
      window.initSampleButton('https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();