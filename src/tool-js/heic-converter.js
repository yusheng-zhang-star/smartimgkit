let heicFile = null;
    let heicArrayBuffer = null;
    let outputFormat = 'jpg';
    let convertedBlobs = [];

    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.style.borderColor = 'var(--accent)'; });
    dropzone.addEventListener('dragleave', () => { dropzone.style.borderColor = 'var(--border-color)'; });
    dropzone.addEventListener('drop', e => {
      e.preventDefault();
      dropzone.style.borderColor = 'var(--border-color)';
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', e => { if (e.target.files.length) handleFile(e.target.files[0]); });

    function handleFile(file) {
      if (!file.name.match(/\.(heic|heif)$/i) && !file.type.match(/heic|heif/)) {
        return alert('Please select a .heic or .heif file.');
      }
      var baPreview = document.getElementById('beforeAfterPreview');
      if (baPreview) baPreview.classList.add('hidden');
      heicFile = file;
      const reader = new FileReader();
      reader.onload = e => {
        heicArrayBuffer = e.target.result;
        showFileInfo(file);
        document.getElementById('convertBtn').disabled = false;
        document.getElementById('resetBtn').disabled = false;
      };
      reader.readAsArrayBuffer(file);
    }

    function showFileInfo(file) {
      const info = document.getElementById('fileInfo');
      info.style.display = 'block';
      info.innerHTML = `<strong>File:</strong> ${file.name}<br><strong>Size:</strong> ${formatBytes(file.size)}<br><strong>Type:</strong> ${file.type || 'image/heic'}`;
    }

    function formatBytes(b) {
      if (b < 1024) return b + ' B';
      if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
      return (b/1048576).toFixed(1) + ' MB';
    }

    function setFormat(fmt, btn) {
      outputFormat = fmt;
      document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('qualityCard').style.display = (fmt === 'png') ? 'none' : 'block';
    }

    function updateQuality() {
      document.getElementById('qualVal').textContent = document.getElementById('qualSlider').value;
    }

    async function convertHeic() {
      if (!heicArrayBuffer) return;
      const btn = document.getElementById('convertBtn');
      btn.disabled = true;
      btn.textContent = '⏳Converting...';
      showLoading(true);

      try {
        // heic2any returns an Array of ArrayBuffer (one per image in HEIC)
        const conversionOpts = { blob: heicArrayBuffer };
        if (outputFormat === 'image/jpeg') conversionOpts.mimeType = 'image/jpeg';
        else if (outputFormat === 'image/png') conversionOpts.mimeType = 'image/png';
        else if (outputFormat === 'image/webp') conversionOpts.mimeType = 'image/webp';

        // Actually heic2any expects { blob: File|Blob } and returns Blob[]
        const inputBlob = new Blob([heicArrayBuffer], { type: 'image/heic' });

        let mimeType;
        if (outputFormat === 'jpg') mimeType = 'image/jpeg';
        else if (outputFormat === 'png') mimeType = 'image/png';
        else mimeType = 'image/webp';

        const outputBlobs = await heic2any({ blob: inputBlob, toType: mimeType });

        convertedBlobs = Array.isArray(outputBlobs) ? outputBlobs : [outputBlobs];
        showResults(convertedBlobs);
      } catch (err) {
        console.error('HEIC conversion error:', err);
        alert('Conversion failed: ' + err.message + '\n\nNote: HEIC decoding requires a modern browser with HEIF support, or the heic2any WASM decoder.');
      }

      showLoading(false);
      btn.disabled = false;
      btn.textContent = '▶️ Convert';
    }

    function showResults(blobs) {
      const canvas = document.getElementById('previewCanvas');
      const ctx = canvas.getContext('2d');
      const placeholder = document.getElementById('placeholderText');
      const downloadArea = document.getElementById('downloadArea');

      placeholder.style.display = 'none';
      canvas.style.display = 'block';

      // Show first image as preview
      const firstBlob = blobs[0];
      const imgUrl = URL.createObjectURL(firstBlob);
      const img = new Image();
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(imgUrl);
      };
      img.src = imgUrl;

      // Download links
      downloadArea.style.display = 'flex';
      downloadArea.innerHTML = '<strong style="font-size:.82rem;color:var(--text-primary)">Downloads:</strong>';
      blobs.forEach((blob, i) => {
        const ext = outputFormat === 'jpg' ? 'jpg' : outputFormat;
        const filename = heicFile.name.replace(/\.(heic|heif)$/i, '') + (blobs.length > 1 ? `_${i+1}` : '') + '.' + ext;
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.innerHTML = `⬇️${filename} <span style="color:var(--text-secondary)">(${formatBytes(blob.size)})</span>`;
        downloadArea.appendChild(a);
      });
    }

    function resetAll() {
      heicFile = null;
      heicArrayBuffer = null;
      convertedBlobs = [];
      document.getElementById('fileInput').value = '';
      document.getElementById('fileInfo').style.display = 'none';
      document.getElementById('downloadArea').style.display = 'none';
      document.getElementById('downloadArea').innerHTML = '';
      document.getElementById('previewCanvas').style.display = 'none';
      document.getElementById('placeholderText').style.display = 'block';
      document.getElementById('convertBtn').disabled = true;
      document.getElementById('resetBtn').disabled = true;
      var baPreview = document.getElementById('beforeAfterPreview');
      if (baPreview) baPreview.classList.remove('hidden');
    }

    function showLoading(show) {
      document.body.style.cursor = show ? 'wait' : 'default';
    }

    // FAQ
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => { btn.parentElement.classList.toggle('active'); });
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();