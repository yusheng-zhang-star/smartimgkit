// ===== Template data (drawn on canvas, no external images needed) =====
    const TEMPLATES = {
      drake:        { name: 'Drake', draw: drawDrake },
      distracted:  { name: 'Distracted Boyfriend', draw: drawDistracted },
      womanyelling: { name: 'Woman Yelling', draw: drawWomanYelling },
      twobuttons:   { name: 'Two Buttons', draw: drawTwoButtons },
      changing:     { name: 'Change My Mind', draw: drawChangeMyMind },
    };

    // ===== State =====
    let bgImage = null; // background image (uploaded or template)
    let activeTemplate = null;

    // ===== DOM =====
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const templateSection = document.getElementById('templateSection');
    const templateGrid = document.getElementById('templateGrid');
    const workspace = document.getElementById('workspace');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');

    const topTextInput = document.getElementById('topText');
    const bottomTextInput = document.getElementById('bottomText');
    const fontSizeSlider = document.getElementById('fontSize');
    const outlineSlider = document.getElementById('outlineWidth');
    const textCaseSelect = document.getElementById('textCase');
    const outputFormat = document.getElementById('outputFormat');

    // ===== Build template grid =====
    Object.entries(TEMPLATES).forEach(([key, tpl]) => {
      const btn = document.createElement('button');
      btn.className = 'template-btn';
      btn.dataset.template = key;
      btn.innerHTML = '<span style="font-size:.7rem;padding:4px 0;">' + tpl.name + '</span>';
      // Draw a tiny preview icon on a mini canvas
      const miniC = document.createElement('canvas');
      miniC.width = 80; miniC.height = 60;
      const mCtx = miniC.getContext('2d');
      tpl.draw(mCtx, 80, 60, '', '');
      btn.appendChild(miniC);
      btn.addEventListener('click', () => {
        document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeTemplate = key;
        // Create a blank bg image (we'll draw the template on render)
        bgImage = null;
        if (workspace.style.display !== 'none') renderPreview();
      });
      templateGrid.appendChild(btn);
    });

    // ===== File Upload =====
    setupDropzone({
      dropzoneId: 'dropzone',
      inputId: 'fileInput',
      onFile: async (file) => {
        try {
          bgImage = await ImageUtils.load(file);
          activeTemplate = null;
          document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
          dropzone.style.display = 'none';
          templateSection.style.display = 'block';
          workspace.style.display = 'block';
          renderPreview();
        } catch (e) {
          ImageUtils.showToast('Failed to load image', 'error');
        }
      }
    });

    // ===== Text / Style Events =====
    [topTextInput, bottomTextInput].forEach(el => el.addEventListener('input', () => renderPreview()));
    [fontSizeSlider, outlineSlider, textCaseSelect].forEach(el => el.addEventListener('input', () => renderPreview()));

    // ===== Reset =====
    document.getElementById('resetBtn').addEventListener('click', () => {
      bgImage = null;
      activeTemplate = null;
      workspace.style.display = 'none';
      templateSection.style.display = 'none';
      dropzone.style.display = '';
      fileInput.value = '';
      topTextInput.value = '';
      bottomTextInput.value = '';
      fontSizeSlider.value = 60;
      outlineSlider.value = 6;
      textCaseSelect.value = 'uppercase';
      document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('infoRow').style.display = 'none';
    });

    // ===== Download =====
    document.getElementById('downloadBtn').addEventListener('click', () => {
      const mime = outputFormat.value;
      const ext = mime === 'image/jpeg' ? 'jpg' : mime === 'image/webp' ? 'webp' : 'png';
      ImageUtils.download(canvas, 'meme.' + ext, mime);
      ImageUtils.showToast('Meme downloaded!');
    });

    // ===== Render =====
    function renderPreview() {
      const W = 800, H = 600; // standard meme canvas size
      canvas.width = W;
      canvas.height = H;
      ctx.clearRect(0, 0, W, H);

      // Draw background (template or uploaded image)
      if (activeTemplate && TEMPLATES[activeTemplate]) {
        TEMPLATES[activeTemplate].draw(ctx, W, H, topTextInput.value, bottomTextInput.value);
      } else if (bgImage) {
        // Fit uploaded image
        const ratio = Math.min(W / bgImage.width, H / bgImage.height);
        const dw = bgImage.width * ratio;
        const dh = bgImage.height * ratio;
        const dx = (W - dw) / 2;
        const dy = (H - dh) / 2;
        ctx.drawImage(bgImage, dx, dy, dw, dh);
        // Draw text over it
        drawMemeText(ctx, W, H, topTextInput.value, bottomTextInput.value);
      } else {
        // Nothing loaded yet
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, W, H);
        drawMemeText(ctx, W, H, topTextInput.value, bottomTextInput.value);
      }

      document.getElementById('infoRow').style.display = 'flex';
      document.getElementById('outSize').textContent = W + ' x ' + H;
    }

    // ===== Draw meme text (outline style) =====
    function drawMemeText(ctx, W, H, topText, bottomText) {
      const fontSize = parseInt(fontSizeSlider.value);
      const outlineW = parseInt(outlineWidth.value);
      const textCase = textCaseSelect.value;

      function processText(t) {
        if (!t) return '';
        if (textCase === 'uppercase') return t.toUpperCase();
        if (textCase === 'capitalize') return t.replace(/\b\w/g, c => c.toUpperCase());
        return t;
      }

      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = 'bold ' + fontSize + 'px Impact, sans-serif';

      // Top text
      if (topText) {
        const txt = processText(topText);
        const y = fontSize + 20;
        ctx.lineWidth = outlineW;
        ctx.strokeStyle = '#000';
        ctx.fillStyle = '#fff';
        ctx.lineJoin = 'round';
        // Word wrap
        const lines = wrapText(ctx, txt, W - 40, fontSize);
        lines.forEach((line, i) => {
          const ly = y + i * (fontSize + 4);
          ctx.strokeText(line, W / 2, ly);
          ctx.fillText(line, W / 2, ly);
        });
      }

      // Bottom text
      if (bottomText) {
        const txt = processText(bottomText);
        ctx.lineWidth = outlineW;
        ctx.strokeStyle = '#000';
        ctx.fillStyle = '#fff';
        const lines = wrapText(ctx, txt, W - 40, fontSize);
        const totalH = lines.length * (fontSize + 4);
        const startY = H - totalH + fontSize;
        lines.forEach((line, i) => {
          const ly = startY + i * (fontSize + 4);
          ctx.strokeText(line, W / 2, ly);
          ctx.fillText(line, W / 2, ly);
        });
      }
    }

    function wrapText(ctx, text, maxWidth, fontSize) {
      const words = text.split(' ');
      const lines = [];
      let current = '';
      for (const word of words) {
        const test = current + (current ? ' ' : '') + word;
        if (ctx.measureText(test).width > maxWidth && current) {
          lines.push(current);
          current = word;
        } else {
          current = test;
        }
      }
      if (current) lines.push(current);
      return lines;
    }

    // ===== Template drawing functions (simplified representations) =====
    function drawDrake(ctx, W, H, top, bottom) {
      // Simple Drake meme: left = dislikes (top text), right = likes (bottom text)
      ctx.fillStyle = '#87ceeb';
      ctx.fillRect(0, 0, W, H);
      // Left side (dislikes)
      ctx.fillStyle = '#ddd';
      ctx.fillRect(0, 0, W/2, H);
      // Right side (likes)
      ctx.fillStyle = '#fff';
      ctx.fillRect(W/2, 0, W/2, H);
      // Simple figure representations
      ctx.fillStyle = '#8b4513';
      ctx.beginPath(); ctx.arc(W/4, H*0.6, 60, 0, Math.PI*2); ctx.fill(); // left head
      ctx.beginPath(); ctx.arc(W*3/4, H*0.6, 60, 0, Math.PI*2); ctx.fill(); // right head
      // Labels
      ctx.fillStyle = '#000';
      ctx.font = 'bold 24px Impact';
      ctx.textAlign = 'center';
      ctx.fillText('DISLIKES', W/4, 30);
      ctx.fillText('LIKES', W*3/4, 30);
      drawMemeText(ctx, W, H, top, bottom);
    }

    function drawDistracted(ctx, W, H, top, bottom) {
      ctx.fillStyle = '#f0e68c';
      ctx.fillRect(0, 0, W, H);
      // Three simple figures
      const colors = ['#4a90d9', '#d0021b', '#4a90d9'];
      colors.forEach((c, i) => {
        ctx.fillStyle = c;
        ctx.beginPath();
        ctx.arc(W*0.25 + i*W*0.25, H*0.55, 40, 0, Math.PI*2);
        ctx.fill();
      });
      drawMemeText(ctx, W, H, top, bottom);
    }

    function drawWomanYelling(ctx, W, H, top, bottom) {
      ctx.fillStyle = '#e8e8e8';
      ctx.fillRect(0, 0, W, H);
      // Woman (left)
      ctx.fillStyle = '#d0021b';
      ctx.beginPath(); ctx.arc(W*0.3, H*0.55, 50, 0, Math.PI*2); ctx.fill();
      // Cat (right)
      ctx.fillStyle = '#ff6b35';
      ctx.beginPath(); ctx.arc(W*0.7, H*0.6, 30, 0, Math.PI*2); ctx.fill();
      drawMemeText(ctx, W, H, top, bottom);
    }

    function drawTwoButtons(ctx, W, H, top, bottom) {
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, W, H);
      // Two buttons
      ctx.fillStyle = '#d0021b';
      ctx.beginPath(); ctx.arc(W/2 - 60, H/2, 30, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = '#4a90d9';
      ctx.beginPath(); ctx.arc(W/2 + 60, H/2, 30, 0, Math.PI*2); ctx.fill();
      drawMemeText(ctx, W, H, top, bottom);
    }

    function drawChangeMyMind(ctx, W, H, top, bottom) {
      ctx.fillStyle = '#87ceeb';
      ctx.fillRect(0, 0, W, H);
      // Person at table
      ctx.fillStyle = '#8b4513';
      ctx.beginPath(); ctx.arc(W*0.7, H*0.5, 50, 0, Math.PI*2); ctx.fill();
      drawMemeText(ctx, W, H, top, bottom);
    }

    // ===== Initial render if template selected =====
    // (nothing to do on load)
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();