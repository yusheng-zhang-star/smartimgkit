const encodeTab = document.getElementById('encodeTab');
    const decodeTab = document.getElementById('decodeTab');
    const encodePanel = document.getElementById('encodePanel');
    const decodePanel = document.getElementById('decodePanel');
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImg = document.getElementById('previewImg');
    const fileInfo = document.getElementById('fileInfo');
    const encodeBtn = document.getElementById('encodeBtn');
    const encodeResult = document.getElementById('encodeResult');
    const b64Output = document.getElementById('b64Output');
    const copyBtn = document.getElementById('copyBtn');
    const downloadTxtBtn = document.getElementById('downloadTxtBtn');
    const resetBtn = document.getElementById('resetBtn');
    const b64Input = document.getElementById('b64Input');
    const decodeBtn = document.getElementById('decodeBtn');
    const dlImgBtn = document.getElementById('dlImgBtn');
    const decodeResult = document.getElementById('decodeResult');
    const decodedImg = document.getElementById('decodedImg');
    const status = document.getElementById('status');

    let currentFile = null;

    encodeTab.addEventListener('click', () => { encodeTab.classList.add('active'); decodeTab.classList.remove('active'); encodePanel.classList.remove('hidden'); decodePanel.classList.add('hidden'); status.textContent=''; });
    decodeTab.addEventListener('click', () => { decodeTab.classList.add('active'); encodeTab.classList.remove('active'); decodePanel.classList.remove('hidden'); encodePanel.classList.add('hidden'); status.textContent=''; });

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        previewImg.src = img.src;
        fileInfo.textContent = file.name + ' — ' + ImageUtils.formatBytes(file.size) + ' — ' + img.naturalWidth + '×' + img.naturalHeight;
        previewArea.classList.add('active');
        dropzone.classList.add('hidden');
        status.textContent = '';
        encodeResult.classList.add('hidden');
      });
    }

    encodeBtn.addEventListener('click', () => {
      if (!currentFile) return;
      encodeBtn.disabled = true; encodeBtn.textContent = '🔄 Encoding...';
      const reader = new FileReader();
      reader.onload = () => {
        b64Output.value = reader.result;
        encodeResult.classList.remove('hidden');
        status.textContent = 'Encoded! String length: ' + reader.result.length.toLocaleString() + ' chars';
        encodeBtn.disabled = false; encodeBtn.textContent = '📋 Encode to Base64';
      };
      reader.readAsDataURL(currentFile);
    });

    copyBtn.addEventListener('click', () => { navigator.clipboard.writeText(b64Output.value); status.textContent = 'Copied to clipboard!'; });
    downloadTxtBtn.addEventListener('click', () => {
      const blob = new Blob([b64Output.value], {type:'text/plain'});
      ImageUtils.download(blob, currentFile.name.replace(/\.[^.]+$/, '.txt'));
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null;
      previewArea.classList.remove('active');
      dropzone.classList.remove('hidden');
      fileInput.value = ''; status.textContent = '';
      encodeResult.classList.add('hidden');
    });

    decodeBtn.addEventListener('click', () => {
      const str = b64Input.value.trim();
      if (!str) return;
      decodeBtn.disabled = true; decodeBtn.textContent = '🔄 Decoding...';
      try {
        let url = str;
        if (!url.startsWith('data:')) url = 'data:image/png;base64,' + url;
        decodedImg.src = url;
        decodeResult.classList.remove('hidden');
        dlImgBtn.classList.remove('hidden');
        status.textContent = 'Decoded successfully!';
      } catch (err) {
        status.textContent = 'Error: Invalid Base64 string';
      } finally {
        decodeBtn.disabled = false; decodeBtn.textContent = '🔄 Decode to Image';
      }
    });

    dlImgBtn.addEventListener('click', () => {
      const a = document.createElement('a');
      a.href = decodedImg.src; a.download = 'decoded-image.png'; a.click();
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1550684847-1e1b7dc3275a?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();