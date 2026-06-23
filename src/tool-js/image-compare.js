// ===== State =====
    let imgA = null, imgB = null;
    let mode = 'slider';

    // ===== DOM =====
    const uploadA = document.getElementById('uploadA');
    const uploadB = document.getElementById('uploadB');
    const fileAInput = document.getElementById('fileA');
    const fileBInput = document.getElementById('fileB');
    const preview = document.getElementById('comparePreview');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const infoRow = document.getElementById('infoRow');

    // ===== Upload A =====
    fileAInput.addEventListener('change', async () => {
      if (fileAInput.files[0]) { imgA = await ImageUtils.load(fileAInput.files[0]); onImageLoaded(); }
    });
    setupDropzoneSimple(uploadA, (file) => { ImageUtils.load(file).then(img => { imgA = img; onImageLoaded(); }); });

    // ===== Upload B =====
    fileBInput.addEventListener('change', async () => {
      if (fileBInput.files[0]) { imgB = await ImageUtils.load(fileBInput.files[0]); onImageLoaded(); }
    });
    setupDropzoneSimple(uploadB, (file) => { ImageUtils.load(file).then(img => { imgB = img; onImageLoaded(); }); });

    function setupDropzoneSimple(el, cb) {
      el.addEventListener('dragover', e => { e.preventDefault(); el.style.borderColor = 'var(--accent)'; });
      el.addEventListener('dragleave', () => { el.style.borderColor = ''; });
      el.addEventListener('drop', e => { e.preventDefault(); el.style.borderColor = ''; if (e.dataTransfer.files[0]) cb(e.dataTransfer.files[0]); });
    }

    // ===== Mode buttons =====
    document.querySelectorAll('.mode-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        mode = btn.dataset.mode;
        renderComparison();
      });
    });

    // ===== On both images loaded =====
    function onImageLoaded() {
      if (imgA) { uploadA.classList.add('loaded'); uploadA.querySelector('.upload-label').textContent = imgA.width + '×' + imgA.height; }
      if (imgB) { uploadB.classList.add('loaded'); uploadB.querySelector('.upload-label').textContent = imgB.width + '×' + imgB.height; }
      if (imgA && imgB) {
        infoRow.style.display = 'flex';
        document.getElementById('sizeA').textContent = imgA.width + '×' + imgA.height;
        document.getElementById('sizeB').textContent = imgB.width + '×' + imgB.height;
        downloadBtn.style.display = '';
        renderComparison();
      }
    }

    // ===== Render =====
    function renderComparison() {
      if (!imgA || !imgB) return;
      preview.innerHTML = '';

      if (mode === 'slider') {
        renderSlider();
      } else if (mode === 'sidebyside') {
        renderSideBySide();
      } else if (mode === 'overlay') {
        renderOverlay();
      }
    }

    function renderSlider() {
      const container = document.createElement('div');
      container.className = 'slider-container';

      const imgBottom = document.createElement('img');
      imgBottom.className = 'slider-img-bottom';
      imgBottom.src = imgB.src || imgB;
      imgBottom.alt = 'Image B';

      const imgTop = document.createElement('img');
      imgTop.className = 'slider-img-top';
      imgTop.src = imgA.src || imgA;
      imgTop.alt = 'Image A';

      const handle = document.createElement('div');
      handle.className = 'slider-handle';

      container.appendChild(imgBottom);
      container.appendChild(imgTop);
      container.appendChild(handle);
      preview.appendChild(container);

      function updateSlider(clientX) {
        const rect = container.getBoundingClientRect();
        let ratio = (clientX - rect.left) / rect.width;
        ratio = Math.max(0, Math.min(1, ratio));
        imgTop.style.clipPath = 'inset(0 ' + ((1 - ratio) * 100) + '% 0 0)';
        handle.style.left = (ratio * 100) + '%';
      }

      container.addEventListener('mousedown', (e) => {
        updateSlider(e.clientX);
        const onMove = (ev) => updateSlider(ev.clientX);
        const onUp = () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp); };
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
      });
      container.addEventListener('touchstart', (e) => {
        e.preventDefault();
        updateSlider(e.touches[0].clientX);
        const onMove = (ev) => updateSlider(ev.touches[0].clientX);
        const onUp = () => { document.removeEventListener('touchmove', onMove); document.removeEventListener('touchend', onUp); };
        document.addEventListener('touchmove', onMove, { passive: false });
        document.addEventListener('touchend', onUp);
      }, { passive: false });

      // Init at 50%
      setTimeout(() => {
        const rect = container.getBoundingClientRect();
        updateSlider(rect.left + rect.width / 2);
      }, 50);
    }

    function renderSideBySide() {
      const container = document.createElement('div');
      container.className = 'sidebyside-container';

      const img1 = document.createElement('img');
      img1.src = imgA.src || imgA;
      img1.alt = 'Image A';

      const img2 = document.createElement('img');
      img2.src = imgB.src || imgB;
      img2.alt = 'Image B';

      container.appendChild(img1);
      container.appendChild(img2);
      preview.appendChild(container);
    }

    function renderOverlay() {
      const wrapper = document.createElement('div');
      wrapper.className = 'overlay-container';

      const imgBottom = document.createElement('img');
      imgBottom.className = 'overlay-bottom';
      imgBottom.src = imgA.src || imgA;
      imgBottom.alt = 'Image A';

      const imgTop = document.createElement('img');
      imgTop.className = 'overlay-top';
      imgTop.src = imgB.src || imgB;
      imgTop.alt = 'Image B';

      const slider = document.createElement('input');
      slider.type = 'range';
      slider.className = 'overlay-slider';
      slider.min = 0; slider.max = 100; slider.value = 50;
      slider.addEventListener('input', () => { imgTop.style.opacity = slider.value / 100; });

      wrapper.appendChild(imgBottom);
      wrapper.appendChild(imgTop);
      preview.appendChild(wrapper);
      preview.appendChild(slider);
    }

    // ===== Reset =====
    resetBtn.addEventListener('click', () => {
      imgA = null; imgB = null;
      fileAInput.value = ''; fileBInput.value = '';
      uploadA.classList.remove('loaded');
      uploadB.classList.remove('loaded');
      uploadA.querySelector('.upload-label').textContent = 'Before / Image A';
      uploadB.querySelector('.upload-label').textContent = 'After / Image B';
      preview.innerHTML = '<p style="color:var(--text-muted);font-size:.9rem;">Upload two images to start comparing</p>';
      infoRow.style.display = 'none';
      downloadBtn.style.display = 'none';
    });

    // ===== Download =====
    downloadBtn.addEventListener('click', () => {
      if (!imgA || !imgB) return;
      // Create side-by-side canvas
      const w = Math.max(imgA.width, imgB.width);
      const h = Math.max(imgA.height, imgB.height);
      const canvas = document.createElement('canvas');
      canvas.width = w * 2 + 20; // 20px gap
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#1a1a2e';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(imgA, 0, 0, imgA.width, imgA.height);
      ctx.drawImage(imgB, w + 20, 0, imgB.width, imgB.height);
      ImageUtils.download(canvas, 'comparison.png', 'image/png');
      ImageUtils.showToast('Comparison downloaded!');
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