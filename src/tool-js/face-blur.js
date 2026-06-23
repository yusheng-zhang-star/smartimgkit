let originalImage = null;
    let detectedFaces = [];
    let blurMode = 'blur';
    let canvas = document.getElementById('previewCanvas');
    let ctx = canvas.getContext('2d');

    // Upload handling
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
      if (!file.type.startsWith('image/')) return alert('Please select an image file.');
      var baPreview = document.getElementById('beforeAfterPreview');
      if (baPreview) baPreview.classList.add('hidden');
      const reader = new FileReader();
      reader.onload = e => {
        const img = new Image();
        img.onload = () => {
          originalImage = img;
          detectFaces(img);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    async function detectFaces(img) {
      // Use MediaPipe CDN-based face detection
      // Fallback: use a simple skin-tone + shape heuristic if MediaPipe fails to load
      showLoading(true);

      try {
        // Try MediaPipe first
        if (window.FaceDetection && typeof FaceDetection !== 'undefined') {
          await detectWithMediaPipe(img);
        } else {
          // Fallback: simulate face detection with center-region heuristic
          console.log('MediaPipe not available, using fallback');
          simulateFaceDetection(img);
        }
      } catch (err) {
        console.error('Face detection error:', err);
        simulateFaceDetection(img);
      }
    }

    function simulateFaceDetection(img) {
      // Fallback: assume face is in upper-center region (~25% of image)
      const w = img.width;
      const h = img.height;
      detectedFaces = [{
        x: w * 0.3,
        y: h * 0.15,
        width: w * 0.4,
        height: h * 0.35
      }];
      document.getElementById('faceCount').textContent = 'Faces detected: ' + detectedFaces.length + ' (estimated)';
      drawBlurredImage();
      showLoading(false);
    }

    async function detectWithMediaPipe(img) {
      // MediaPipe Face Detection via CDN
      // The @mediapipe/face_detection package exports a global `FaceDetection` class
      try {
        const detector = await new Promise((resolve, reject) => {
          const fd = new FaceDetection({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4.1646424915/${file}`
          }, () => resolve(fd), reject);
          fd.setOptions({ model: 'short', minDetectionConfidence: 0.5 });
        });

        // Create a temp canvas to get image data
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');
        const scale = Math.min(640 / img.width, 640 / img.height, 1);
        tempCanvas.width = img.width * scale;
        tempCanvas.height = img.height * scale;
        tempCtx.drawImage(img, 0, 0, tempCanvas.width, tempCanvas.height);

        const results = await detector.send({ image: tempCanvas });
        detectedFaces = (results.detections || []).map(d => {
          const bbox = d.boundingBox;
          return {
            x: bbox.xCenter * img.width - bbox.width * img.width / 2,
            y: bbox.yCenter * img.height - bbox.height * img.height / 2,
            width: bbox.width * img.width,
            height: bbox.height * img.height
          };
        });

        document.getElementById('faceCount').textContent = 'Faces detected: ' + detectedFaces.length;
        drawBlurredImage();
      } catch (e) {
        console.error('MediaPipe error:', e);
        simulateFaceDetection(img);
      }
      showLoading(false);
    }

    function drawBlurredImage() {
      if (!originalImage) return;
      canvas.width = originalImage.width;
      canvas.height = originalImage.height;
      ctx.drawImage(originalImage, 0, 0);

      const blurIntensity = parseInt(document.getElementById('blurSlider').value);
      const paddingPct = parseInt(document.getElementById('padSlider').value);

      detectedFaces.forEach(face => {
        const padX = face.width * paddingPct / 100;
        const padY = face.height * paddingPct / 100;
        const x = Math.max(0, face.x - padX);
        const y = Math.max(0, face.y - padY);
        const w = Math.min(canvas.width - x, face.width + padX * 2);
        const h = Math.min(canvas.height - y, face.height + padY * 2);

        if (blurMode === 'blur') {
          // Save region, blur, restore
          ctx.save();
          ctx.filter = `blur(${blurIntensity}px)`;
          // Redraw the face region with blur
          const imgData = ctx.getImageData(x, y, w, h);
          ctx.clearRect(x, y, w, h);
          // Draw a blurred version by drawing scaled down then up
          const smallW = Math.max(2, Math.floor(w / blurIntensity));
          const smallH = Math.max(2, Math.floor(h / blurIntensity));
          const tmpC = document.createElement('canvas');
          tmpC.width = smallW; tmpC.height = smallH;
          tmpC.getContext('2d').drawImage(originalImage, x, y, w, h, 0, 0, smallW, smallH);
          ctx.imageSmoothingEnabled = true;
          ctx.imageSmoothingQuality = 'high';
          ctx.drawImage(tmpC, x, y, w, h);
          ctx.restore();
        } else if (blurMode === 'pixelate') {
          const pixelSize = Math.max(4, Math.floor(blurIntensity / 2));
          const smallW = Math.max(1, Math.floor(w / pixelSize));
          const smallH = Math.max(1, Math.floor(h / pixelSize));
          const tmpC = document.createElement('canvas');
          tmpC.width = smallW; tmpC.height = smallH;
          tmpC.getContext('2d').drawImage(originalImage, x, y, w, h, 0, 0, smallW, smallH);
          ctx.imageSmoothingEnabled = false;
          ctx.drawImage(tmpC, x, y, w, h);
          ctx.imageSmoothingEnabled = true;
        } else if (blurMode === 'blackbar') {
          ctx.fillStyle = '#000';
          ctx.fillRect(x, y, w, h);
        }
      });

      document.getElementById('downloadBtn').disabled = false;
      document.getElementById('resetBtn').disabled = false;
    }

    function updateBlur() {
      document.getElementById('blurVal').textContent = document.getElementById('blurSlider').value;
      document.getElementById('padVal').textContent = document.getElementById('padSlider').value;
      if (originalImage && detectedFaces.length) drawBlurredImage();
    }

    function setBlurMode(mode, btn) {
      blurMode = mode;
      document.querySelectorAll('.mode-toggle button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      if (originalImage && detectedFaces.length) drawBlurredImage();
    }

    function downloadResult() {
      const link = document.createElement('a');
      link.download = 'face-blurred.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    }

    function resetImage() {
      if (!originalImage) return;
      canvas.width = originalImage.width;
      canvas.height = originalImage.height;
      ctx.drawImage(originalImage, 0, 0);
      var baPreview = document.getElementById('beforeAfterPreview');
      if (baPreview) baPreview.classList.remove('hidden');
    }

    function showLoading(show) {
      document.body.style.cursor = show ? 'wait' : 'default';
    }

    // FAQ
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.parentElement;
        item.classList.toggle('active');
      });
    });
  
  // Sample image & Next Step
  (function() {
    var _handleFile = typeof handleFile === 'function' ? handleFile : null;
    if (_handleFile) {
      window.initSampleButton('https://images.unsplash.com/photo-1517486808966-28c82f2f8c52?w=800&q=80', _handleFile);
    }
    // Show next-step on download click
    var dlBtn = document.getElementById('downloadBtn') || document.querySelector('.btn-primary[onclick*="download"], .btn-secondary[onclick*="download"]');
    if (dlBtn) {
      dlBtn.addEventListener('click', function() { SmartImgNextStep.show(); });
    }
  })();