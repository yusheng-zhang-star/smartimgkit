// ===== State =====
    let images = []; // { id, file, img, name, width, height }
    let idCounter = 0;
    let layout = 'grid';
    let dragSrcId = null;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const imageList = document.getElementById('imageList');
    const imageCount = document.getElementById('imageCount');
    const addMoreBtn = document.getElementById('addMoreBtn');
    const addMoreInput = document.getElementById('addMoreInput');
    const previewCanvas = document.getElementById('previewCanvas');
    const ctx = previewCanvas.getContext('2d');
    const colsSelect = document.getElementById('colsSelect');
    const colsGroup = document.getElementById('colsGroup');
    const spacingSlider = document.getElementById('spacingSlider');
    const spacingValue = document.getElementById('spacingValue');
    const radiusSlider = document.getElementById('radiusSlider');
    const radiusValue = document.getElementById('radiusValue');
    const bgColor = document.getElementById('bgColor');
    const outputFormat = document.getElementById('outputFormat');
    const mergeBtn = document.getElementById('mergeBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');

    // ===== Upload =====
    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFiles, multiple: true });

    // addMoreBtn triggers addMoreInput via label binding
    addMoreInput.addEventListener('change', () => {
      if (addMoreInput.files.length) handleFiles(Array.from(addMoreInput.files));
      addMoreInput.value = '';
    });

    async function handleFiles(files) {
      const arr = Array.isArray(files) ? files : [files];
      for (const file of arr) {
        if (!file.type.startsWith('image/')) continue;
        const img = await ImageUtils.load(file);
        images.push({ id: ++idCounter, file, img, name: file.name, width: img.naturalWidth, height: img.naturalHeight });
      }
      if (images.length > 0) {
        dropzone.classList.add('hidden');
        workspace.style.display = '';
      }
      renderList();
      renderPreview();
    }

    // ===== Layout Buttons =====
    document.querySelectorAll('.layout-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        layout = btn.dataset.layout;
        colsGroup.style.display = layout === 'grid' ? '' : 'none';
        renderPreview();
      });
    });

    // ===== Controls =====
    spacingSlider.addEventListener('input', () => { spacingValue.textContent = spacingSlider.value; renderPreview(); });
    radiusSlider.addEventListener('input', () => { radiusValue.textContent = radiusSlider.value; renderPreview(); });
    bgColor.addEventListener('input', () => renderPreview());
    colsSelect.addEventListener('change', () => renderPreview());

    // ===== Image List (Drag & Drop Reorder) =====
    function renderList() {
      imageCount.textContent = images.length;
      imageList.innerHTML = '';
      images.forEach((item, idx) => {
        const el = document.createElement('div');
        el.className = 'image-list-item';
        el.draggable = true;
        el.dataset.id = item.id;
        el.innerHTML = `
          <img src="${URL.createObjectURL(item.file)}" alt="${item.name}">
          <div class="item-info">
            <div class="item-name">${item.name}</div>
            <div class="item-size">${item.width} × ${item.height}</div>
          </div>
          <button class="item-remove" data-idx="${idx}" title="Remove">&times;</button>
        `;

        // Drag reorder
        el.addEventListener('dragstart', e => { dragSrcId = item.id; el.classList.add('dragging'); e.dataTransfer.effectAllowed = 'move'; });
        el.addEventListener('dragend', () => { el.classList.remove('dragging'); document.querySelectorAll('.image-list-item').forEach(i => i.classList.remove('drag-over')); });
        el.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; el.classList.add('drag-over'); });
        el.addEventListener('dragleave', () => el.classList.remove('drag-over'));
        el.addEventListener('drop', e => {
          e.preventDefault();
          el.classList.remove('drag-over');
          const srcIdx = images.findIndex(i => i.id === dragSrcId);
          const dstIdx = images.findIndex(i => i.id === item.id);
          if (srcIdx !== -1 && dstIdx !== -1 && srcIdx !== dstIdx) {
            const [moved] = images.splice(srcIdx, 1);
            images.splice(dstIdx, 0, moved);
            renderList();
            renderPreview();
          }
        });

        // Touch reorder (mobile)
        let touchStartIdx = null;
        el.addEventListener('touchstart', () => { touchStartIdx = idx; }, { passive: true });

        // Remove
        el.querySelector('.item-remove').addEventListener('click', () => {
          images.splice(idx, 1);
          if (images.length === 0) { workspace.style.display = 'none'; dropzone.classList.remove('hidden'); }
          renderList();
          renderPreview();
        });

        imageList.appendChild(el);
      });
    }

    // ===== Preview Render =====
    function renderPreview() {
      if (images.length === 0) { previewCanvas.width = 0; previewCanvas.height = 0; return; }

      const spacing = parseInt(spacingSlider.value);
      const radius = parseInt(radiusSlider.value);
      const bg = bgColor.value;
      const colsOpt = colsSelect.value;

      if (layout === 'horizontal') renderHorizontal(spacing, radius, bg);
      else if (layout === 'vertical') renderVertical(spacing, radius, bg);
      else renderGrid(spacing, radius, bg, colsOpt);
    }

    function drawRoundedImage(ctx, img, x, y, w, h, r) {
      r = Math.min(r, w / 2, h / 2);
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.lineTo(x + w - r, y);
      ctx.arcTo(x + w, y, x + w, y + r, r);
      ctx.lineTo(x + w, y + h - r);
      ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
      ctx.lineTo(x + r, y + h);
      ctx.arcTo(x, y + h, x, y + h - r, r);
      ctx.lineTo(x, y + r);
      ctx.arcTo(x, y, x + r, y, r);
      ctx.closePath();
      ctx.clip();
      ctx.drawImage(img, x, y, w, h);
      ctx.restore();
    }

    function renderHorizontal(spacing, radius, bg) {
      // All images scaled to the same height (max height capped at 800)
      const maxH = Math.min(800, Math.max(...images.map(i => i.height)));
      const scaled = images.map(item => {
        const h = maxH;
        const w = Math.round(item.width * (h / item.height));
        return { img: item.img, w, h };
      });
      const totalW = scaled.reduce((s, i) => s + i.w, 0) + spacing * (images.length - 1) + spacing * 2;
      const totalH = maxH + spacing * 2;

      previewCanvas.width = totalW;
      previewCanvas.height = totalH;
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, totalW, totalH);

      let x = spacing;
      scaled.forEach(item => {
        drawRoundedImage(ctx, item.img, x, spacing, item.w, item.h, radius);
        x += item.w + spacing;
      });
    }

    function renderVertical(spacing, radius, bg) {
      const maxW = Math.min(800, Math.max(...images.map(i => i.width)));
      const scaled = images.map(item => {
        const w = maxW;
        const h = Math.round(item.height * (w / item.width));
        return { img: item.img, w, h };
      });
      const totalH = scaled.reduce((s, i) => s + i.h, 0) + spacing * (images.length - 1) + spacing * 2;
      const totalW = maxW + spacing * 2;

      previewCanvas.width = totalW;
      previewCanvas.height = totalH;
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, totalW, totalH);

      let y = spacing;
      scaled.forEach(item => {
        drawRoundedImage(ctx, item.img, spacing, y, item.w, item.h, radius);
        y += item.h + spacing;
      });
    }

    function renderGrid(spacing, radius, bg, colsOpt) {
      const n = images.length;
      let cols = colsOpt === 'auto' ? Math.ceil(Math.sqrt(n)) : parseInt(colsOpt);
      cols = Math.max(1, Math.min(cols, n));
      const rows = Math.ceil(n / cols);

      // Calculate cell size based on largest image, capped
      const maxDim = 600;
      const cellW = Math.min(maxDim, Math.max(...images.map(i => i.width)));
      const cellH = Math.min(maxDim, Math.max(...images.map(i => i.height)));

      const totalW = cols * cellW + (cols + 1) * spacing;
      const totalH = rows * cellH + (rows + 1) * spacing;

      previewCanvas.width = totalW;
      previewCanvas.height = totalH;
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, totalW, totalH);

      images.forEach((item, idx) => {
        const col = idx % cols;
        const row = Math.floor(idx / cols);
        const x = spacing + col * (cellW + spacing);
        const y = spacing + row * (cellH + spacing);

        // Fit image within cell preserving aspect ratio
        const scale = Math.min(cellW / item.width, cellH / item.height);
        const dw = Math.round(item.width * scale);
        const dh = Math.round(item.height * scale);
        const dx = x + Math.round((cellW - dw) / 2);
        const dy = y + Math.round((cellH - dh) / 2);

        drawRoundedImage(ctx, item.img, dx, dy, dw, dh, radius);
      });
    }

    // ===== Merge & Download =====
    mergeBtn.addEventListener('click', async () => {
      if (images.length === 0) return;
      mergeBtn.disabled = true;
      mergeBtn.textContent = '🔄 Merging...';
      status.textContent = '';

      try {
        const format = outputFormat.value;
        const quality = format === 'image/png' ? undefined : 0.92;
        const blob = await ImageUtils.canvasToBlob(previewCanvas, format, quality);
        const ext = format === 'image/png' ? 'png' : format === 'image/jpeg' ? 'jpg' : 'webp';
        ImageUtils.download(blob, `merged-image.${ext}`);
        status.textContent = '✅ Image merged and downloaded!';
      } catch (e) {
        status.textContent = '❌ Error: ' + e.message;
      }

      mergeBtn.disabled = false;
      mergeBtn.textContent = '🖼️ Merge & Download';
    });

    // ===== Reset =====
    resetBtn.addEventListener('click', () => {
      images = [];
      workspace.style.display = 'none';
      dropzone.classList.remove('hidden');
      fileInput.value = '';
      status.textContent = '';
    });
  
  // Next Step
  (function() {
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('[id*="download"], [id*="Download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();