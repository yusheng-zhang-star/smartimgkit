// ===== Gradient Presets =====
    const GRADIENTS = [
      { name: 'Indigo',   colors: ['#6366f1', '#8b5cf6'] },
      { name: 'Sunset',   colors: ['#f97316', '#ec4899'] },
      { name: 'Ocean',    colors: ['#0ea5e9', '#6366f1'] },
      { name: 'Emerald',  colors: ['#10b981', '#06b6d4'] },
      { name: 'Rose',     colors: ['#f43f5e', '#a855f7'] },
      { name: 'Sky',      colors: ['#38bdf8', '#818cf8'] },
      { name: 'Amber',    colors: ['#f59e0b', '#ef4444'] },
      { name: 'Teal',     colors: ['#14b8a6', '#3b82f6'] },
      { name: 'Purple',   colors: ['#a855f7', '#ec4899'] },
      { name: 'Slate',    colors: ['#475569', '#1e293b'] },
    ];

    // ===== State =====
    let originalImg = null;
    let frameStyle = 'none';
    let gradientIndex = 0;
    let useCustomBg = false;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const workspace = document.getElementById('workspace');
    const previewCanvas = document.getElementById('previewCanvas');
    const ctx = previewCanvas.getContext('2d');

    const paddingSlider = document.getElementById('padding');
    const paddingValue = document.getElementById('paddingValue');
    const radiusSlider = document.getElementById('cornerRadius');
    const radiusValue = document.getElementById('radiusValue');
    const shadowBlurSlider = document.getElementById('shadowBlur');
    const shadowValue = document.getElementById('shadowValue');
    const shadowOpSlider = document.getElementById('shadowOpacity');
    const shadowOpValue = document.getElementById('shadowOpValue');
    const scaleSlider = document.getElementById('imageScale');
    const scaleValue = document.getElementById('scaleValue');
    const bgColorInput = document.getElementById('bgColor');
    const outputFormat = document.getElementById('outputFormat');

    // ===== Init Gradient Swatches =====
    const gradientPresetsEl = document.getElementById('gradientPresets');
    GRADIENTS.forEach((g, i) => {
      const swatch = document.createElement('div');
      swatch.className = 'gradient-swatch' + (i === 0 ? ' active' : '');
      swatch.style.background = `linear-gradient(135deg, ${g.colors[0]}, ${g.colors[1]})`;
      swatch.title = g.name;
      swatch.dataset.index = i;
      swatch.addEventListener('click', () => {
        document.querySelectorAll('.gradient-swatch').forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        gradientIndex = i;
        useCustomBg = false;
        renderPreview();
      });
      gradientPresetsEl.appendChild(swatch);
    });

    // ===== Frame Buttons =====
    document.querySelectorAll('.frame-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.frame-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        frameStyle = btn.dataset.frame;
        renderPreview();
      });
    });

    // ===== File Upload =====
    setupDropzone({
      dropzoneId: 'dropzone',
      inputId: 'fileInput',
      onFile: async (file) => {
        try {
          originalImg = await ImageUtils.load(file);
          document.getElementById('origSize').textContent = originalImg.width + ' x ' + originalImg.height;
          dropzone.style.display = 'none';
          workspace.style.display = 'block';
          renderPreview();
        } catch (e) {
          ImageUtils.showToast('Failed to load image', 'error');
        }
      }
    });

    // ===== Slider Events =====
    paddingSlider.addEventListener('input', () => { paddingValue.textContent = paddingSlider.value; renderPreview(); });
    radiusSlider.addEventListener('input', () => { radiusValue.textContent = radiusSlider.value; renderPreview(); });
    shadowBlurSlider.addEventListener('input', () => { shadowValue.textContent = shadowBlurSlider.value; renderPreview(); });
    shadowOpSlider.addEventListener('input', () => { shadowOpValue.textContent = shadowOpSlider.value; renderPreview(); });
    scaleSlider.addEventListener('input', () => { scaleValue.textContent = scaleSlider.value; renderPreview(); });
    bgColorInput.addEventListener('input', () => { useCustomBg = true; document.querySelectorAll('.gradient-swatch').forEach(s => s.classList.remove('active')); renderPreview(); });

    // ===== Reset =====
    document.getElementById('resetBtn').addEventListener('click', () => {
      originalImg = null;
      workspace.style.display = 'none';
      dropzone.style.display = '';
      fileInput.value = '';
      frameStyle = 'none';
      gradientIndex = 0;
      useCustomBg = false;
      paddingSlider.value = 64; paddingValue.textContent = '64';
      radiusSlider.value = 16; radiusValue.textContent = '16';
      shadowBlurSlider.value = 40; shadowValue.textContent = '40';
      shadowOpSlider.value = 25; shadowOpValue.textContent = '25';
      scaleSlider.value = 75; scaleValue.textContent = '75';
      document.querySelectorAll('.frame-btn').forEach(b => b.classList.remove('active'));
      document.querySelector('[data-frame="none"]').classList.add('active');
      document.querySelectorAll('.gradient-swatch').forEach((s, i) => {
        s.classList.toggle('active', i === 0);
      });
    });

    // ===== Download =====
    document.getElementById('downloadBtn').addEventListener('click', () => {
      const mime = outputFormat.value;
      const ext = mime === 'image/jpeg' ? 'jpg' : mime === 'image/webp' ? 'webp' : 'png';
      ImageUtils.download(previewCanvas, 'screenshot-framed.' + ext, mime);
      ImageUtils.showToast('Image downloaded!');
    });

    // ===== Render Preview =====
    function renderPreview() {
      if (!originalImg) return;

      const pad = parseInt(paddingSlider.value);
      const radius = parseInt(radiusSlider.value);
      const shadowB = parseInt(shadowBlurSlider.value);
      const shadowO = parseInt(shadowOpSlider.value) / 100;
      const scale = parseInt(scaleSlider.value) / 100;

      const imgW = originalImg.width;
      const imgH = originalImg.height;

      // Calculate dimensions based on frame style
      let canvasW, canvasH, screenX, screenY, screenW, screenH;
      const scaledW = Math.round(imgW * scale);
      const scaledH = Math.round(imgH * scale);

      if (frameStyle === 'browser') {
        const titleBarH = 40;
        const addressBarH = 36;
        const chromeH = titleBarH + addressBarH;
        screenW = scaledW;
        screenH = scaledH;
        screenX = pad;
        screenY = pad + chromeH;
        canvasW = scaledW + pad * 2;
        canvasH = scaledH + chromeH + pad * 2;
      } else if (frameStyle === 'laptop') {
        const bezel = 16;
        const titleBarH = 36;
        const baseH = 60;
        const baseSide = 60;
        screenW = scaledW;
        screenH = scaledH;
        screenX = pad + bezel;
        screenY = pad + bezel + titleBarH;
        canvasW = scaledW + (bezel + pad) * 2;
        canvasH = scaledH + bezel * 2 + titleBarH + baseH + pad * 2;
      } else if (frameStyle === 'phone') {
        const bezel = 24;
        const notchW = Math.round(scaledW * 0.35);
        const notchH = 28;
        const homeH = 20;
        screenW = scaledW;
        screenH = scaledH;
        screenX = pad + bezel;
        screenY = pad + bezel + notchH;
        canvasW = scaledW + (bezel + pad) * 2;
        canvasH = scaledH + notchH + homeH + bezel * 2 + pad * 2;
      } else {
        screenW = scaledW;
        screenH = scaledH;
        screenX = pad;
        screenY = pad;
        canvasW = scaledW + pad * 2;
        canvasH = scaledH + pad * 2;
      }

      previewCanvas.width = canvasW;
      previewCanvas.height = canvasH;

      // Clear
      ctx.clearRect(0, 0, canvasW, canvasH);

      // Draw background
      if (useCustomBg) {
        ctx.fillStyle = bgColorInput.value;
        ctx.fillRect(0, 0, canvasW, canvasH);
      } else {
        const grad = GRADIENTS[gradientIndex];
        const gradient = ctx.createLinearGradient(0, 0, canvasW, canvasH);
        gradient.addColorStop(0, grad.colors[0]);
        gradient.addColorStop(1, grad.colors[1]);
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvasW, canvasH);
      }

      // Draw frame + screenshot
      if (frameStyle === 'browser') {
        drawBrowserFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO);
      } else if (frameStyle === 'laptop') {
        drawLaptopFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO);
      } else if (frameStyle === 'phone') {
        drawPhoneFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO);
      } else {
        // No frame — just the screenshot with rounded corners and shadow
        drawSimpleFrame(ctx, screenX, screenY, screenW, screenH, radius, shadowB, shadowO);
      }

      // Update info
      document.getElementById('outSize').textContent = canvasW + ' x ' + canvasH;
    }

    // ===== Simple Frame (no device) =====
    function drawSimpleFrame(ctx, x, y, w, h, radius, shadowB, shadowO) {
      ctx.save();

      // Shadow
      if (shadowB > 0) {
        ctx.shadowColor = 'rgba(0,0,0,' + shadowO + ')';
        ctx.shadowBlur = shadowB;
        ctx.shadowOffsetY = shadowB / 4;
      }

      // Rounded rect clip
      roundedRect(ctx, x, y, w, h, radius);
      ctx.clip();

      ctx.drawImage(originalImg, x, y, w, h);

      ctx.restore();
    }

    // ===== Browser Frame =====
    function drawBrowserFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO) {
      const titleBarH = 40;
      const addressBarH = 36;
      const chromeH = titleBarH + addressBarH;
      const frameX = screenX;
      const frameY = screenY - chromeH;
      const frameW = screenW;
      const frameH = chromeH + screenH;

      ctx.save();

      // Shadow
      if (shadowB > 0) {
        ctx.shadowColor = 'rgba(0,0,0,' + shadowO + ')';
        ctx.shadowBlur = shadowB;
        ctx.shadowOffsetY = shadowB / 4;
      }

      // Window background
      ctx.fillStyle = '#1e1e2e';
      roundedRect(ctx, frameX, frameY, frameW, frameH, radius);
      ctx.fill();

      // Reset shadow for inner elements
      ctx.shadowColor = 'transparent';
      ctx.shadowBlur = 0;
      ctx.shadowOffsetY = 0;

      // Title bar background
      ctx.fillStyle = '#181825';
      roundedRectTop(ctx, frameX, frameY, frameW, titleBarH, radius);
      ctx.fill();

      // Traffic light buttons
      const btnY = frameY + titleBarH / 2;
      const btnR = 6;
      const btnStartX = frameX + 18;
      // Red
      ctx.beginPath();
      ctx.arc(btnStartX, btnY, btnR, 0, Math.PI * 2);
      ctx.fillStyle = '#ff5f57';
      ctx.fill();
      // Yellow
      ctx.beginPath();
      ctx.arc(btnStartX + 22, btnY, btnR, 0, Math.PI * 2);
      ctx.fillStyle = '#febc2e';
      ctx.fill();
      // Green
      ctx.beginPath();
      ctx.arc(btnStartX + 44, btnY, btnR, 0, Math.PI * 2);
      ctx.fillStyle = '#28c840';
      ctx.fill();

      // Address bar
      const addrY = frameY + titleBarH;
      ctx.fillStyle = '#1e1e2e';
      ctx.fillRect(frameX, addrY, frameW, addressBarH);

      // Address bar inner
      const addrPad = 8;
      const addrH = 24;
      const addrInnerY = addrY + (addressBarH - addrH) / 2;
      ctx.fillStyle = '#313244';
      roundedRect(ctx, frameX + addrPad, addrInnerY, frameW - addrPad * 2, addrH, 6);
      ctx.fill();

      // Address text
      ctx.fillStyle = '#6c7086';
      ctx.font = '12px Inter, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('https://example.com', frameX + frameW / 2, addrInnerY + addrH / 2);

      // Screenshot content — clip to bottom rounded rect
      ctx.save();
      roundedRectBottom(ctx, frameX, screenY - 1, screenW, screenH + 1, radius);
      ctx.clip();
      ctx.drawImage(originalImg, screenX, screenY, screenW, screenH);
      ctx.restore();

      ctx.restore();
    }

    // ===== Laptop Frame =====
    function drawLaptopFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO) {
      const bezel = 16;
      const titleBarH = 36;
      const baseH = 60;
      const baseSide = 60;

      const frameX = screenX - bezel;
      const frameY = screenY - bezel - titleBarH;
      const frameW = screenW + bezel * 2;
      const frameH = screenH + bezel * 2 + titleBarH;

      ctx.save();

      // Shadow
      if (shadowB > 0) {
        ctx.shadowColor = 'rgba(0,0,0,' + shadowO + ')';
        ctx.shadowBlur = shadowB;
        ctx.shadowOffsetY = shadowB / 4;
      }

      // Screen bezel
      ctx.fillStyle = '#1e1e2e';
      roundedRect(ctx, frameX, frameY, frameW, frameH, radius);
      ctx.fill();

      // Reset shadow
      ctx.shadowColor = 'transparent';
      ctx.shadowBlur = 0;
      ctx.shadowOffsetY = 0;

      // Title bar (within screen)
      ctx.fillStyle = '#181825';
      roundedRectTop(ctx, frameX, frameY, frameW, titleBarH + bezel, radius);
      ctx.fill();

      // Traffic light dots
      const btnY = frameY + bezel + titleBarH / 2;
      const btnR = 5;
      const btnStartX = frameX + bezel + 14;
      ctx.beginPath(); ctx.arc(btnStartX, btnY, btnR, 0, Math.PI * 2); ctx.fillStyle = '#ff5f57'; ctx.fill();
      ctx.beginPath(); ctx.arc(btnStartX + 18, btnY, btnR, 0, Math.PI * 2); ctx.fillStyle = '#febc2e'; ctx.fill();
      ctx.beginPath(); ctx.arc(btnStartX + 36, btnY, btnR, 0, Math.PI * 2); ctx.fillStyle = '#28c840'; ctx.fill();

      // Screen content
      ctx.save();
      roundedRectBottom(ctx, screenX - 1, screenY - 1, screenW + 2, screenH + bezel + 2, Math.max(radius - 4, 4));
      ctx.clip();
      ctx.drawImage(originalImg, screenX, screenY, screenW, screenH);
      ctx.restore();

      // Laptop base
      const baseY = frameY + frameH + 4;
      const baseX = frameX - baseSide;
      const baseW = frameW + baseSide * 2;

      // Base shadow
      ctx.fillStyle = '#0f0f1a';
      roundedRect(ctx, baseX, baseY, baseW, baseH, 8);
      ctx.fill();

      // Base top surface
      ctx.fillStyle = '#1e1e2e';
      roundedRectTop(ctx, baseX, baseY, baseW, baseH - 8, 8);
      ctx.fill();

      // Trackpad
      const tpW = baseW * 0.3;
      const tpH = baseH * 0.5;
      const tpX = baseX + (baseW - tpW) / 2;
      const tpY = baseY + (baseH - tpH) / 2 - 2;
      ctx.strokeStyle = '#313244';
      ctx.lineWidth = 1;
      roundedRect(ctx, tpX, tpY, tpW, tpH, 4);
      ctx.stroke();

      // Camera dot on bezel
      ctx.beginPath();
      ctx.arc(frameX + frameW / 2, frameY + bezel / 2, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#313244';
      ctx.fill();

      ctx.restore();
    }

    // ===== Phone Frame =====
    function drawPhoneFrame(ctx, screenX, screenY, screenW, screenH, pad, radius, shadowB, shadowO) {
      const bezel = 24;
      const notchW = Math.round(screenW * 0.35);
      const notchH = 28;
      const homeH = 20;

      const frameX = screenX - bezel;
      const frameY = screenY - bezel - notchH;
      const frameW = screenW + bezel * 2;
      const frameH = screenH + notchH + homeH + bezel * 2;

      ctx.save();

      // Shadow
      if (shadowB > 0) {
        ctx.shadowColor = 'rgba(0,0,0,' + shadowO + ')';
        ctx.shadowBlur = shadowB;
        ctx.shadowOffsetY = shadowB / 4;
      }

      // Phone body
      ctx.fillStyle = '#1e1e2e';
      roundedRect(ctx, frameX, frameY, frameW, frameH, Math.max(radius, 28));
      ctx.fill();

      // Reset shadow
      ctx.shadowColor = 'transparent';
      ctx.shadowBlur = 0;
      ctx.shadowOffsetY = 0;

      // Side buttons (right side)
      ctx.fillStyle = '#313244';
      ctx.fillRect(frameX + frameW, frameY + frameH * 0.25, 3, 30);
      ctx.fillRect(frameX + frameW, frameY + frameH * 0.35, 3, 50);
      ctx.fillRect(frameX + frameW, frameY + frameH * 0.50, 3, 50);

      // Screen content
      ctx.save();
      roundedRect(ctx, screenX, screenY, screenW, screenH, 0);
      ctx.clip();
      ctx.drawImage(originalImg, screenX, screenY, screenW, screenH);
      ctx.restore();

      // Notch (dynamic island style)
      const notchX = screenX + (screenW - notchW) / 2;
      const notchY = screenY - notchH + 4;
      ctx.fillStyle = '#0f0f1a';
      roundedRect(ctx, notchX, notchY, notchW, notchH, 14);
      ctx.fill();

      // Camera dot in notch
      ctx.beginPath();
      ctx.arc(notchX + notchW - 20, notchY + notchH / 2, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#1e293b';
      ctx.fill();
      ctx.beginPath();
      ctx.arc(notchX + notchW - 20, notchY + notchH / 2, 2, 0, Math.PI * 2);
      ctx.fillStyle = '#334155';
      ctx.fill();

      // Home indicator
      const homeW = screenW * 0.3;
      const homeY = screenY + screenH + (homeH + bezel - 5) / 2;
      ctx.fillStyle = '#6c7086';
      roundedRect(ctx, screenX + (screenW - homeW) / 2, homeY, homeW, 4, 2);
      ctx.fill();

      ctx.restore();
    }

    // ===== Rounded Rect Helpers =====
    function roundedRect(ctx, x, y, w, h, r) {
      r = Math.min(r, w / 2, h / 2);
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
    }

    function roundedRectTop(ctx, x, y, w, h, r) {
      r = Math.min(r, w / 2, h);
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.lineTo(x + w - r, y);
      ctx.arcTo(x + w, y, x + w, y + r, r);
      ctx.lineTo(x + w, y + h);
      ctx.lineTo(x, y + h);
      ctx.lineTo(x, y + r);
      ctx.arcTo(x, y, x + r, y, r);
      ctx.closePath();
    }

    function roundedRectBottom(ctx, x, y, w, h, r) {
      r = Math.min(r, w / 2, h);
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + w, y);
      ctx.lineTo(x + w, y + h - r);
      ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
      ctx.lineTo(x + r, y + h);
      ctx.arcTo(x, y + h, x, y + h - r, r);
      ctx.lineTo(x, y);
      ctx.closePath();
    }
  
  // Next Step
  (function() {
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('[id*="download"], [id*="Download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();