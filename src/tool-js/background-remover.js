(function() {
      // Global error display
      function showErr(msg) {
        var d = document.getElementById('_diag');
        var m = document.getElementById('_diagMsg');
        if (d && m) {
          m.innerHTML = '<div style="font-size:1.5rem;margin-bottom:12px;">⚠️ Something went wrong</div>' +
            '<div style="font-size:0.9rem;opacity:0.8;max-width:400px;">' + msg + '</div>' +
            '<div style="margin-top:16px;font-size:0.8rem;opacity:0.5;">Try refreshing with Ctrl+F5 or clearing your browser cache.</div>';
          d.style.display = 'flex';
        }
      }
      window.onerror = function(msg, src, line) {
        showErr('Script error at line ' + line + ': ' + msg);
        return false;
      };
      window.addEventListener('unhandledrejection', function(e) {
        showErr('Async error: ' + (e.reason && e.reason.message ? e.reason.message : e.reason));
      });

      try {
    // NOT a module script — ensures page renders even if CDN is blocked
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('previewArea');
    const previewImg = document.getElementById('previewImg');
    const removeBtn = document.getElementById('removeBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const resetBtn = document.getElementById('resetBtn');
    const status = document.getElementById('status');
    const resultArea = document.getElementById('resultArea');
    const resultImg = document.getElementById('resultImg');

    let currentFile = null;
    let resultBlob = null;
    let selectedModel = 'isnet_fp16';
    let _removeBackground = null; // cached after first dynamic import

    setupDropzone({ dropzoneId: 'dropzone', inputId: 'fileInput', onFile: handleFile });

    const beforeAfterPreview = document.getElementById('beforeAfterPreview');

    // Model quality selector
    document.querySelectorAll('.model-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.model-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedModel = btn.dataset.model;
      });
    });

    function handleFile(file) {
      if (!file.type.startsWith('image/')) { status.textContent = 'Please select an image file.'; return; }
      if (file.size > 10 * 1024 * 1024) { status.textContent = 'File is too large. Maximum size is 10MB.'; return; }
      currentFile = file;
      ImageUtils.load(file).then(img => {
        previewImg.src = img.src;
        previewArea.classList.add('active');
        dropzone.classList.add('hidden');
        beforeAfterPreview.classList.add('hidden');
        status.textContent = '';
        resultArea.classList.add('hidden');
        downloadBtn.classList.add('hidden');
      });
    }

    async function loadRemoveBackground() {
      if (_removeBackground) return _removeBackground;
      try {
        // Use new Function to avoid SyntaxError on browsers that don't support dynamic import()
        const loader = new Function('return import("https://cdn.jsdelivr.net/npm/@imgly/background-removal@1.7.0/+esm")');
        const mod = await loader();
        _removeBackground = mod.removeBackground;
        return _removeBackground;
      } catch (err) {
        throw new Error('Failed to load AI model library. Please check your internet connection and try again. If the problem persists, try using a VPN or switching to a different network.');
      }
    }

    async function processImage(file, model, isFallback) {
      const removeBackground = await loadRemoveBackground();
      const prefix = isFallback ? 'Network issue with selected model. Using Balanced instead. ' : '';
      status.innerHTML = '<div class="spinner"></div><p>' + prefix + 'AI is removing the background. This may take a moment on first use as the model loads.</p>';

      const blob = await removeBackground(file, {
        debug: false,
        model: model,
        progress: (key, current, total) => {
          const pct = total > 0 ? Math.round((current / total) * 100) : 0;
          const label = key.startsWith('fetch:') ? 'Downloading model' : 'Processing';
          status.innerHTML = `<div class="spinner"></div><p>${prefix}${label}... ${pct}%</p>`;
        }
      });

      resultBlob = blob;
      resultImg.src = URL.createObjectURL(blob);
      resultArea.classList.remove('hidden');
      downloadBtn.classList.remove('hidden');
      document.getElementById('nextStepSection').classList.add('visible');
      status.textContent = isFallback
        ? 'Done! (Auto-switched to Balanced mode — selected model unavailable on current network.)'
        : 'Done! Background removed successfully.';
    }

    removeBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      removeBtn.disabled = true;
      removeBtn.textContent = '🔄 Processing...';
      document.querySelectorAll('.model-btn').forEach(b => b.disabled = true);
      status.innerHTML = '<div class="spinner"></div><p>Loading AI engine...</p>';

      try {
        await processImage(currentFile, selectedModel, false);
      } catch (err) {
        const msg = err && err.message ? err.message : String(err);
        if (selectedModel !== 'isnet_fp16' && msg.toLowerCase().includes('fetch')) {
          try {
            await processImage(currentFile, 'isnet_fp16', true);
          } catch (fallbackErr) {
            status.textContent = 'Error: ' + (fallbackErr && fallbackErr.message ? fallbackErr.message : fallbackErr);
            console.error(fallbackErr);
          }
        } else {
          status.textContent = 'Error: ' + msg;
          console.error(err);
        }
      } finally {
        removeBtn.disabled = false;
        removeBtn.textContent = '🪄 Remove Background';
        document.querySelectorAll('.model-btn').forEach(b => b.disabled = false);
      }
    });

    downloadBtn.addEventListener('click', () => {
      if (resultBlob) ImageUtils.download(resultBlob, 'smartimgkit-no-bg.png');
    });

    resetBtn.addEventListener('click', () => {
      currentFile = null; resultBlob = null;
      previewArea.classList.remove('active');
      dropzone.classList.remove('hidden');
      beforeAfterPreview.classList.remove('hidden');
      fileInput.value = ''; status.textContent = '';
      resultArea.classList.add('hidden');
      downloadBtn.classList.add('hidden');
      document.getElementById('nextStepSection').classList.remove('visible');
    });

    // Sample image
    document.getElementById('sampleBtn').addEventListener('click', async () => {
      const btn = document.getElementById('sampleBtn');
      btn.textContent = '⏳ Loading...';
      try {
        const resp = await fetch('https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&q=80');
        const blob = await resp.blob();
        const file = new File([blob], 'sample.jpg', { type: 'image/jpeg' });
        handleFile(file);
      } catch (e) {
        btn.textContent = '🖼️ Try with a sample image';
      }
    });

    // Hide diagnostic layer on success
    var _diagEl = document.getElementById('_diag');
    if (_diagEl) _diagEl.style.display = 'none';
      } catch (err) {
        showErr('Page initialization failed: ' + (err && err.message ? err.message : err));
        console.error(err);
      }
    })();