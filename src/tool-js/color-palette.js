const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImg = document.getElementById('previewImg');
    const countRange = document.getElementById('countRange');
    const countVal = document.getElementById('countVal');
    const extractBtn = document.getElementById('extractBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');
    const paletteResult = document.getElementById('paletteResult');
    const paletteGrid = document.getElementById('paletteGrid');
    const cssOutput = document.getElementById('cssOutput');

    let currentFile = null;

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });
    countRange.addEventListener('input', () => countVal.textContent = countRange.value);

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        previewImg.src = img.src;
        previewArea.classList.add('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.add('hidden');
        dropzone.classList.add('hidden');
        status.textContent = '';
        paletteResult.classList.add('hidden');
      });
    }

    function rgbToHex(r, g, b) {
      return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('');
    }

    function extractColors(img, count) {
      const canvas = ImageUtils.createCanvas(100, 100);
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, 100, 100);
      const data = ctx.getImageData(0, 0, 100, 100).data;
      const buckets = {};
      for (let i = 0; i < data.length; i += 4) {
        const r = Math.round(data[i] / 32) * 32;
        const g = Math.round(data[i + 1] / 32) * 32;
        const b = Math.round(data[i + 2] / 32) * 32;
        const key = r + ',' + g + ',' + b;
        buckets[key] = (buckets[key] || 0) + 1;
      }
      return Object.entries(buckets)
        .sort((a, b) => b[1] - a[1])
        .slice(0, count)
        .map(([key]) => key.split(',').map(Number));
    }

    extractBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      extractBtn.disabled = true;
      extractBtn.textContent = '🔄 Extracting...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const colors = extractColors(img, parseInt(countRange.value));
        paletteGrid.innerHTML = '';
        let css = ':root {\n';
        colors.forEach((c, i) => {
          const hex = rgbToHex(c[0], c[1], c[2]);
          css += `  --color-${i + 1}: ${hex};\n`;
          const div = document.createElement('div');
          div.className = 'palette-color';
          div.innerHTML = `<div class="palette-swatch" style="background:${hex}"></div><div class="palette-info"><code>${hex}</code><br>rgb(${c.join(',')})</div>`;
          div.addEventListener('click', () => { navigator.clipboard.writeText(hex); status.textContent = hex + ' copied!'; });
          paletteGrid.appendChild(div);
        });
        css += '}';
        cssOutput.textContent = css;
        paletteResult.classList.remove('hidden');
        status.textContent = 'Click any color to copy its HEX code.';
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        extractBtn.disabled = false;
        extractBtn.textContent = '🎨 Extract Colors';
      }
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null;
      previewArea.classList.remove('active');
          document.getElementById('beforeAfterPreview') && document.getElementById('beforeAfterPreview').classList.remove('hidden');
      dropzone.classList.remove('hidden');
      fileInput.value = ''; status.textContent = '';
      paletteResult.classList.add('hidden');
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1493552152660-f915ab47ae9d?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();