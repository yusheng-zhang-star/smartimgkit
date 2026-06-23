(function() {
        // Set pdf.js worker source
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js';

        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');
        const controlsSection = document.getElementById('controlsSection');
        const pdfInfo = document.getElementById('pdfInfo');
        const outputFormat = document.getElementById('outputFormat');
        const scaleFactor = document.getElementById('scaleFactor');
        const pageFrom = document.getElementById('pageFrom');
        const pageTo = document.getElementById('pageTo');
        const convertBtn = document.getElementById('convertBtn');
        const resetBtn = document.getElementById('resetBtn');
        const statusSection = document.getElementById('statusSection');
        const statusText = document.getElementById('statusText');
        const resultSection = document.getElementById('resultSection');
        const pagesGrid = document.getElementById('pagesGrid');
        const convertedCount = document.getElementById('convertedCount');
        const downloadAllBtn = document.getElementById('downloadAllBtn');

        let pdfDoc = null;
        let convertedPages = []; // { pageNum, dataUrl, blob }

        // Upload
        dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
        dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
        dropzone.addEventListener('drop', e => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener('change', e => {
            if (e.target.files.length > 0) handleFile(e.target.files[0]);
        });

        function handleFile(file) {
            if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) {
                alert('Please upload a PDF file.');
                return;
            }

            var baPreview = document.getElementById('beforeAfterPreview');
            if (baPreview) baPreview.classList.add('hidden');

            const reader = new FileReader();
            reader.onload = function(e) {
                loadPDF(e.target.result);
            };
            reader.readAsArrayBuffer(file);
            
            // Show controls
            pdfInfo.innerHTML = `<strong>File:</strong> ${file.name} &nbsp;|&nbsp; <strong>Size:</strong> ${(file.size/1024/1024).toFixed(2)} MB`;
            pageFrom.placeholder = '1';
            pageTo.placeholder = '?';
            controlsSection.classList.remove('hidden');
            resultSection.classList.add('hidden');
            convertedPages = [];
        }

        async function loadPDF(arrayBuffer) {
            try {
                const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
                pdfDoc = await loadingTask.promise;
                pageTo.placeholder = pdfDoc.numPages;
                pdfInfo.innerHTML += ` &nbsp;|&nbsp; <strong>Pages:</strong> ${pdfDoc.numPages}`;
                statusSection.classList.add('hidden');
            } catch (err) {
                alert('Failed to load PDF: ' + err.message);
            }
        }

        // Convert
        convertBtn.addEventListener('click', async function() {
            if (!pdfDoc) {
                alert('Please upload a PDF first.');
                return;
            }
            
            const format = outputFormat.value;
            const scale = parseFloat(scaleFactor.value);
            const from = pageFrom.value ? parseInt(pageFrom.value) : 1;
            const to = pageTo.value ? parseInt(pageTo.value) : pdfDoc.numPages;
            
            if (from < 1 || to > pdfDoc.numPages || from > to) {
                alert(`Please enter a valid page range (1-${pdfDoc.numPages}).`);
                return;
            }
            
            statusSection.classList.remove('hidden');
            resultSection.classList.add('hidden');
            convertBtn.disabled = true;
            convertedPages = [];
            pagesGrid.innerHTML = '';
            
            const totalPages = to - from + 1;
            
            for (let i = from; i <= to; i++) {
                statusText.textContent = `Converting page ${i}/${to}...`;
                
                try {
                    const page = await pdfDoc.getPage(i);
                    const viewport = page.getViewport({ scale: scale });
                    
                    const canvas = document.createElement('canvas');
                    canvas.width = viewport.width;
                    canvas.height = viewport.height;
                    const ctx = canvas.getContext('2d');
                    
                    await page.render({
                        canvasContext: ctx,
                        viewport: viewport
                    }).promise;
                    
                    const mimeType = format === 'jpeg' ? 'image/jpeg' : (format === 'webp' ? 'image/webp' : 'image/png');
                    const quality = format === 'jpeg' ? 0.92 : (format === 'webp' ? 0.92 : undefined);
                    const dataUrl = canvas.toDataURL(mimeType, quality);
                    
                    convertedPages.push({ pageNum: i, dataUrl, canvas });
                    
                    // Add to grid
                    const item = document.createElement('div');
                    item.className = 'page-item';
                    const previewCanvas = document.createElement('canvas');
                    // Create a smaller preview
                    const previewScale = Math.min(180 / canvas.width, 1);
                    previewCanvas.width = canvas.width * previewScale;
                    previewCanvas.height = canvas.height * previewScale;
                    previewCanvas.getContext('2d').drawImage(canvas, 0, 0, previewCanvas.width, previewCanvas.height);
                    item.appendChild(previewCanvas);
                    
                    const numDiv = document.createElement('div');
                    numDiv.className = 'page-num';
                    numDiv.textContent = `Page ${i}`;
                    item.appendChild(numDiv);
                    
                    const dlBtn = document.createElement('button');
                    dlBtn.className = 'dl-btn';
                    dlBtn.textContent = 'Download';
                    dlBtn.onclick = function() {
                        const a = document.createElement('a');
                        a.href = dataUrl;
                        a.download = `page-${i}.${format === 'jpeg' ? 'jpg' : format}`;
                        a.click();
                    };
                    item.appendChild(dlBtn);
                    
                    pagesGrid.appendChild(item);
                    convertedCount.textContent = convertedPages.length;
                    
                } catch (err) {
                    console.error(`Error converting page ${i}:`, err);
                }
            }
            
            statusText.textContent = `Done! Converted ${convertedPages.length} page(s).`;
            resultSection.classList.remove('hidden');
            convertBtn.disabled = false;
        });

        // Download all as ZIP
        downloadAllBtn.addEventListener('click', async function() {
            if (convertedPages.length === 0) return;
            
            statusText.textContent = 'Creating ZIP file...';
            statusSection.classList.remove('hidden');
            
            // Use dynamic import for JSZip (we'll load it from CDN)
            const JSZip = window.JSZip;
            if (!JSZip) {
                // Load JSZip from CDN
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';
                script.onload = function() {
                    createZip(window.JSZip);
                };
                document.head.appendChild(script);
            } else {
                createZip(JSZip);
            }
        });

        function createZip(JSZip) {
            const zip = new JSZip();
            const format = outputFormat.value;
            const ext = format === 'jpeg' ? 'jpg' : format;
            
            convertedPages.forEach(page => {
                const base64 = page.dataUrl.split(',')[1];
                zip.file(`page-${page.pageNum}.${ext}`, base64, { base64: true });
            });
            
            zip.generateAsync({ type: 'blob' }).then(function(blob) {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'pdf-pages.zip';
                a.click();
                URL.revokeObjectURL(url);
                statusSection.classList.add('hidden');
            });
        }

        // Reset
        resetBtn.addEventListener('click', function() {
            pdfDoc = null;
            convertedPages = [];
            pagesGrid.innerHTML = '';
            controlsSection.classList.add('hidden');
            resultSection.classList.add('hidden');
            statusSection.classList.add('hidden');
            fileInput.value = '';
            var baPreview = document.getElementById('beforeAfterPreview');
            if (baPreview) baPreview.classList.remove('hidden');
        });
    })();