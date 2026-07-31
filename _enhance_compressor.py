#!/usr/bin/env python
"""Enhance compressor + create GIF splitter + create beauty tool."""

import os

BASE = r'E:\网站项目\smartimgkit'

# ============ 1. Enhance Compressor ============
compressor_path = os.path.join(BASE, 'tools', 'compressor.html')

with open(compressor_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add output format selector after quality slider
old_quality = '''          <div style="max-width:400px;margin:0 auto 16px">
            <label style="display:flex;justify-content:space-between;color:var(--text-secondary);font-size:.85rem;margin-bottom:6px">
              <span>Quality</span><span id="qualityVal">80%</span>
            </label>
            <input type="range" id="qualityRange" min="10" max="95" value="80">
          </div>'''

new_quality = '''          <div style="max-width:400px;margin:0 auto 16px">
            <label style="display:flex;justify-content:space-between;color:var(--text-secondary);font-size:.85rem;margin-bottom:6px">
              <span>Output Format</span>
            </label>
            <select id="formatSelect" style="width:100%;padding:10px;border:1px solid var(--border);border-radius:8px;background:var(--bg-primary);color:var(--text-primary);margin-bottom:16px">
              <option value="auto">Auto (same as input)</option>
              <option value="image/jpeg">JPEG</option>
              <option value="image/webp">WebP (smallest)</option>
              <option value="image/png">PNG (lossless)</option>
            </select>
            <label style="display:flex;justify-content:space-between;color:var(--text-secondary);font-size:.85rem;margin-bottom:6px">
              <span>Quality</span><span id="qualityVal">80%</span>
            </label>
            <input type="range" id="qualityRange" min="10" max="95" value="80">
          </div>
          <div id="sizeCompare" class="hidden" style="max-width:600px;margin:0 auto 16px;padding:16px;background:var(--bg-secondary);border-radius:12px">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:.85rem">
              <span id="compareOrigLabel" style="color:var(--text-secondary)">Original: —</span>
              <span id="compareSavedLabel" style="color:var(--accent);font-weight:600"></span>
              <span id="compareCompLabel" style="color:var(--text-secondary)">Compressed: —</span>
            </div>
            <div style="display:flex;gap:2px;height:24px;border-radius:6px;overflow:hidden;background:var(--bg-primary)">
              <div id="compareOrigBar" style="background:#f59e0b;transition:width 0.3s;width:50%;display:flex;align-items:center;justify-content:center;font-size:.75rem;color:white;font-weight:600"></div>
              <div id="compareCompBar" style="background:#10b981;transition:width 0.3s;width:50%;display:flex;align-items:center;justify-content:center;font-size:.75rem;color:white;font-weight:600"></div>
            </div>
          </div>'''

content = content.replace(old_quality, new_quality)

# Update script to add live preview + format selection + size comparison
old_script_start = '''    qualityRange.addEventListener('input', () => qualityVal.textContent = qualityRange.value + '%');'''

new_script_start = '''    const formatSelect = document.getElementById('formatSelect');
    const sizeCompare = document.getElementById('sizeCompare');
    const compareOrigBar = document.getElementById('compareOrigBar');
    const compareCompBar = document.getElementById('compareCompBar');
    const compareOrigLabel = document.getElementById('compareOrigLabel');
    const compareCompLabel = document.getElementById('compareCompLabel');
    const compareSavedLabel = document.getElementById('compareSavedLabel');
    
    let previewDebounce = null;
    let previewImage = null;
    
    qualityRange.addEventListener('input', () => {
      qualityVal.textContent = qualityRange.value + '%';
      // Live preview (debounced)
      if (currentFile) {
        clearTimeout(previewDebounce);
        previewDebounce = setTimeout(doCompress, 150);
      }
    });
    formatSelect.addEventListener('change', () => {
      if (currentFile) doCompress();
    });
    
    function updateSizeCompare(origSize, compSize) {
      sizeCompare.classList.remove('hidden');
      const total = origSize + compSize;
      const origPct = Math.round(origSize / total * 100);
      const compPct = 100 - origPct;
      compareOrigBar.style.width = origPct + '%';
      compareCompBar.style.width = compPct + '%';
      compareOrigLabel.textContent = 'Original: ' + ImageUtils.formatBytes(origSize);
      compareCompLabel.textContent = 'Compressed: ' + ImageUtils.formatBytes(compSize);
      const saved = Math.round((1 - compSize / origSize) * 100);
      if (saved > 0) {
        compareSavedLabel.textContent = '↓ ' + saved + '% saved';
      } else {
        compareSavedLabel.textContent = '↑ ' + Math.abs(saved) + '% larger';
      }
    }'''

content = content.replace(old_script_start, new_script_start)

# Change compressBtn to call doCompress instead, and rename function
old_compress_click = '''    compressBtn.addEventListener('click', async () => {
      if (!currentFile) return;
      compressBtn.disabled = true;
      compressBtn.textContent = '🔄 Compressing...';
      status.innerHTML = '<div class="spinner"></div>';
      try {
        const img = await ImageUtils.load(currentFile);
        const canvas = ImageUtils.createCanvas(img.naturalWidth, img.naturalHeight);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        const quality = parseInt(qualityRange.value) / 100;
        const outType = currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg';
        const blob = await ImageUtils.canvasToBlob(canvas, outType, quality);
        resultBlob = blob;
        const url = URL.createObjectURL(blob);
        compImg.src = url;
        compSize.textContent = ImageUtils.formatBytes(blob.size) + ' — Saved ' + Math.round((1 - blob.size / currentFile.size) * 100) + '%';
        downloadBtn.classList.remove('hidden');
        status.textContent = '';
      } catch (err) {
        status.textContent = 'Error: ' + err.message;
      } finally {
        compressBtn.disabled = false;
        compressBtn.textContent = '🗜️ Compress';
      }
    });'''

new_compress_click = '''    async function doCompress() {
      if (!currentFile) return;
      try {
        const img = await ImageUtils.load(currentFile);
        const canvas = ImageUtils.createCanvas(img.naturalWidth, img.naturalHeight);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        const quality = parseInt(qualityRange.value) / 100;
        let outType = formatSelect.value;
        if (outType === 'auto') {
          outType = currentFile.type === 'image/png' ? 'image/png' : 'image/jpeg';
        }
        const blob = await ImageUtils.canvasToBlob(canvas, outType, quality);
        resultBlob = blob;
        const url = URL.createObjectURL(blob);
        compImg.src = url;
        const saved = Math.round((1 - blob.size / currentFile.size) * 100);
        compSize.textContent = ImageUtils.formatBytes(blob.size) + ' — ' + (saved > 0 ? 'Saved ' + saved + '%' : 'Larger by ' + Math.abs(saved) + '%');
        downloadBtn.classList.remove('hidden');
        updateSizeCompare(currentFile.size, blob.size);
      } catch (err) {
        console.error(err);
      }
    }

    compressBtn.addEventListener('click', () => {
      if (!currentFile) return;
      doCompress();
    });'''

content = content.replace(old_compress_click, new_compress_click)

# Update download to use correct extension based on format
old_download = '''    downloadBtn.addEventListener('click', () => {
      if (resultBlob) {
        const ext = currentFile.name.split('.').pop();
        const base = currentFile.name.replace(/\.[^.]+$/, '');
        ImageUtils.download(resultBlob, base + '-compressed.' + ext);
      }
    });'''

new_download = '''    downloadBtn.addEventListener('click', () => {
      if (resultBlob) {
        let outType = formatSelect.value;
        if (outType === 'auto') outType = currentFile.type;
        const extMap = { 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/png': 'png' };
        const ext = extMap[outType] || currentFile.name.split('.').pop();
        const base = currentFile.name.replace(/\.[^.]+$/, '');
        ImageUtils.download(resultBlob, base + '-compressed.' + ext);
      }
    });'''

content = content.replace(old_download, new_download)

with open(compressor_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Enhanced: tools/compressor.html")

print("\n✅ Compressor enhanced!")
