(function(){
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const framesSection = document.getElementById('framesSection');
    const framesGrid = document.getElementById('framesGrid');
    const frameCount = document.getElementById('frameCount');
    const controlsSection = document.getElementById('controlsSection');
    const globalDelay = document.getElementById('globalDelay');
    const resizeWidth = document.getElementById('resizeWidth');
    const quality = document.getElementById('quality');
    const generateBtn = document.getElementById('generateBtn');
    const resetBtn = document.getElementById('resetBtn');
    const progressSection = document.getElementById('progressSection');
    const statusText = document.getElementById('statusText');
    const progressFill = document.getElementById('progressFill');
    const resultSection = document.getElementById('resultSection');
    const resultGif = document.getElementById('resultGif');
    const downloadBtn = document.getElementById('downloadBtn');
    const newGifBtn = document.getElementById('newGifBtn');

    let frames = [];

    // Drag & drop
    dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', e => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
    fileInput.addEventListener('change', e => handleFiles(e.target.files));

    function handleFiles(fileList) {
        const files = Array.from(fileList).filter(f => f.type.startsWith('image/'));
        if (!files.length) return;
        var ba = document.getElementById('beforeAfterPreview');
        if (ba) ba.classList.add('hidden');
        files.forEach(f => {
            var reader = new FileReader();
            reader.onload = function(evt) {
                var img = new Image();
                img.onload = function() {
                    frames.push({ file: f, imgDataUrl: evt.target.result, img: img, delay: parseInt(globalDelay.value) });
                    renderFrames();
                };
                img.src = evt.target.result;
            };
            reader.readAsDataURL(f);
        });
    }

    function renderFrames() {
        frameCount.textContent = frames.length;
        framesGrid.innerHTML = '';
        frames.forEach((frame, i) => {
            var div = document.createElement('div');
            div.className = 'frame-item';
            div.innerHTML = '<span class="frame-num">#' + (i+1) + '</span><button class="remove-btn" data-idx="' + i + '">✕</button><img src="' + frame.imgDataUrl + '" alt="Frame ' + (i+1) + '"><input type="number" class="delay-input" data-idx="' + i + '" value="' + frame.delay + '" min="50" max="5000" placeholder="Delay (ms)">';
            framesGrid.appendChild(div);
        });
        framesGrid.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', function() { frames.splice(parseInt(this.dataset.idx), 1); renderFrames(); });
        });
        framesGrid.querySelectorAll('.delay-input').forEach(inp => {
            inp.addEventListener('change', function() { frames[parseInt(this.dataset.idx)].delay = parseInt(this.value) || 500; });
        });
        framesSection.classList.remove('hidden');
        controlsSection.classList.remove('hidden');
    }

    generateBtn.addEventListener('click', function() {
        if (frames.length < 2) { alert('Please add at least 2 images.'); return; }
        progressSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
        statusText.textContent = 'Starting GIF encoding...';
        progressFill.style.width = '0%';
        generateBtn.disabled = true;

        var gif = new GIF({
            workers: Math.min(4, frames.length),
            quality: parseInt(quality.value),
            workerScript: 'https://cdn.jsdelivr.net/npm/gif.js@0.2.0/dist/gif.worker.js'
        });
        var targetW = resizeWidth.value ? parseInt(resizeWidth.value) : null;
        frames.forEach(frame => {
            var canvas = document.createElement('canvas');
            var w = frame.img.naturalWidth, h = frame.img.naturalHeight;
            if (targetW) { h = Math.round(h * (targetW / w)); w = targetW; }
            canvas.width = w; canvas.height = h;
            canvas.getContext('2d').drawImage(frame.img, 0, 0, w, h);
            gif.addFrame(canvas, { delay: frame.delay, copy: true });
        });
        gif.on('progress', function(p) {
            var pct = Math.round(p * 100);
            progressFill.style.width = pct + '%';
            statusText.textContent = 'Encoding GIF: ' + pct + '%';
        });
        gif.on('finished', function(blob) {
            var url = URL.createObjectURL(blob);
            resultGif.src = url;
            resultSection.classList.remove('hidden');
            progressSection.classList.add('hidden');
            generateBtn.disabled = false;
            downloadBtn.onclick = function() {
                var a = document.createElement('a'); a.href = url; a.download = 'smartimgkit-animation.gif'; a.click();
            };
        });
        gif.render();
    });

    resetBtn.addEventListener('click', function() {
        frames = []; framesGrid.innerHTML = '';
        framesSection.classList.add('hidden');
        controlsSection.classList.add('hidden');
        progressSection.classList.add('hidden');
        resultSection.classList.add('hidden');
        fileInput.value = '';
        var ba = document.getElementById('beforeAfterPreview');
        if (ba) ba.classList.remove('hidden');
    });
    newGifBtn.addEventListener('click', function() {
        resultSection.classList.add('hidden');
        progressSection.classList.add('hidden');
    });
})();