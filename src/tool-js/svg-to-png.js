// ===== State =====
    let svgSource = '';    // SVG string or data URL
    let svgSize = { w: 0, h: 0 };

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');

    const outputFormat = document.getElementById('outputFormat');
    const scaleFactor = document.getElementById('scaleFactor');
    const svgCodeArea = document.getElementById('svgCodeArea');
    const applySvgCodeBtn = document.getElementById('applySvgCode');

    // ===== Tabs =====
    document.querySelectorAll('.input-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.input-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
      });
    });

    // ===== File Upload =====
    setupDropzone({
      dropzoneId: 'dropzone',
      inputId: 'fileInput',
      onFile: async (file) => {
        try {
          const text = await file.text();
          svgSource = text;
          parseAndRender(text);
          dropzone.style.display = 'none';
          workspace.style.display = 'block';
        } catch (e) {
          ImageUtils.showToast('Failed to read SVG file', 'error');
        }
      }
    });

    // ===== Paste SVG Code =====
    applySvgCodeBtn.addEventListener('click', () => {
      const code = svgCodeArea.value.trim();
      if (!code) { ImageUtils.showToast('Please paste SVG code first', 'error'); return; }
      svgSource = code;
      parseAndRender(code);
      dropzone.style.display = 'none';
      workspace.style.display = 'block';
    });

    // ===== Re-upload =====
    document.getElementById('reuploadLink').addEventListener('click', (e) => {
      e.preventDefault();
      dropzone.style.display = '';
      workspace.style.display = 'none';
      fileInput.value = '';
    });

    // ===== Parse SVG dimensions =====
    function getSvgDimensions(svgString) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(svgString, 'image/svg+xml');
      const svg = doc.querySelector('svg');
      if (!svg) return null;

      let w = parseFloat(svg.getAttribute('width')) || 0;
      let h = parseFloat(svg.getAttribute('height')) || 0;

      // Try viewBox
      const viewBox = svg.getAttribute('viewBox');
      if ((!w || !h) && viewBox) {
        const parts = viewBox.split(/[\s,]+/).map(Number);
        if (parts.length === 4) { w = w || parts[2]; h = h || parts[3]; }
      }
      // Default if still 0
      w = w || 300; h = h || 150;
      return { w, h };
    }

    // ===== Render =====
    function parseAndRender(svgString) {
      const dims = getSvgDimensions(svgString);
      if (!dims) { ImageUtils.showToast('Invalid SVG code', 'error'); return; }
      svgSize = dims;
      document.getElementById('svgSize').textContent = dims.w + ' x ' + dims.h;

      const scale = parseInt(scaleFactor.value);
      canvas.width = dims.w * scale;
      canvas.height = dims.h * scale;

      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        document.getElementById('outSize').textContent = canvas.width + ' x ' + canvas.height;
      };
      img.onerror = () => { ImageUtils.showToast('Failed to render SVG', 'error'); };
      // Use data URL for SVG
      const dataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);
      img.src = dataUrl;
    }

    // ===== Scale Factor Change =====
    scaleFactor.addEventListener('change', () => {
      if (svgSource) parseAndRender(svgSource);
    });

    // ===== Reset =====
    document.getElementById('resetBtn').addEventListener('click', () => {
      svgSource = '';
      svgSize = { w: 0, h: 0 };
      workspace.style.display = 'none';
      dropzone.style.display = '';
      fileInput.value = '';
      svgCodeArea.value = '';
      document.getElementById('svgSize').textContent = '-';
      document.getElementById('outSize').textContent = '-';
    });

    // ===== Download =====
    document.getElementById('downloadBtn').addEventListener('click', () => {
      const mime = outputFormat.value;
      const ext = mime === 'image/jpeg' ? 'jpg' : mime === 'image/webp' ? 'webp' : 'png';
      // Re-render at current scale to ensure freshness
      if (svgSource) {
        parseAndRender(svgSource);
        // Small delay to let canvas render
        setTimeout(() => {
          ImageUtils.download(canvas, 'converted.' + ext, mime);
          ImageUtils.showToast('Image downloaded!');
        }, 100);
      }
    });
  
  // Next Step
  (function() {
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('[id*="download"], [id*="Download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();