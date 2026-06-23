let currentFile = null;
    let currentImageDataUrl = null;
    let parsedMetadata = null;

    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const resultsSection = document.getElementById('resultsSection');
    dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.style.borderColor = 'var(--accent)'; });
    dropzone.addEventListener('dragleave', () => { dropzone.style.borderColor = 'var(--border-color)'; });
    dropzone.addEventListener('drop', e => {
      e.preventDefault();
      dropzone.style.borderColor = 'var(--border-color)';
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', e => { if (e.target.files.length) handleFile(e.target.files[0]); });

    async function handleFile(file) {
      currentFile = file;
      showLoading(true);
      document.getElementById('resultsSection').style.display = 'none';

      // Read file as ArrayBuffer for exifr
      const arrayBuffer = await file.arrayBuffer();

      try {
        // Parse all metadata segments
        const options = {
          exif: true,
          gps: true,
          iptc: true,
          xmp: true,
          icc: true,
          jfif: true,
          ihdr: true,
        };
        parsedMetadata = await exifr.parse(arrayBuffer, options);
        console.log('Parsed metadata:', parsedMetadata);

        // Also get image for preview
        const reader = new FileReader();
        reader.onload = e => {
          currentImageDataUrl = e.target.result;
          document.getElementById('previewImg').src = currentImageDataUrl;
          renderMetadata(parsedMetadata);
          document.getElementById('resultsSection').style.display = 'block';
          showLoading(false);
        };
        reader.readAsDataURL(file);
      } catch (err) {
        console.error('Metadata parse error:', err);
        // Still show image even if metadata parsing fails
        const reader = new FileReader();
        reader.onload = e => {
          currentImageDataUrl = e.target.result;
          document.getElementById('previewImg').src = currentImageDataUrl;
          document.getElementById('metaSections').innerHTML = '<div class="no-meta">No readable metadata found in this image.</div>';
          document.getElementById('resultsSection').style.display = 'block';
          showLoading(false);
        };
        reader.readAsDataURL(file);
      }
    }

    function renderMetadata(meta) {
      const container = document.getElementById('metaSections');
      if (!meta || Object.keys(meta).length === 0) {
        container.innerHTML = '<div class="no-meta">No metadata detected. Try uploading a JPG photo taken with a camera.</div>';
        document.getElementById('privacyWarning').style.display = 'none';
        return;
      }

      let html = '';
      let hasGPS = false;

      // EXIF section
      const exifFields = ['Make','Model','DateTimeOriginal','ExposureTime','FNumber','ISOSpeedRatings',
        'FocalLength','LensModel','Orientation','XResolution','YResolution','ResolutionUnit',
        'ExposureProgram','MeteringMode','Flash','WhiteBalance','Software','HostComputer',
        'ImageWidth','ImageHeight','BitsPerSample','ColorSpace','PixelXDimension','PixelYDimension'];

      const exifData = {};
      let hasExif = false;
      exifFields.forEach(f => { if (meta[f] !== undefined) { exifData[f] = meta[f]; hasExif = true; } });
      // Also check for nested exif
      if (meta.exif && typeof meta.exif === 'object') {
        Object.assign(exifData, meta.exif);
        hasExif = true;
      }

      if (hasExif) {
        html += buildMetaSection('📷 EXIF —Camera Settings', exifData, 'exif');
      }

      // GPS section
      if (meta.latitude !== undefined && meta.longitude !== undefined) {
        hasGPS = true;
        const gpsData = {
          'Latitude': meta.latitude + '掳 (' + (meta.latitude > 0 ? 'N' : 'S') + ')',
          'Longitude': meta.longitude + '掳 (' + (meta.longitude > 0 ? 'E' : 'W') + ')',
          'Altitude': meta.altitude !== undefined ? meta.altitude + 'm' : 'N/A',
        };
        if (meta.latitude !== undefined) {
          gpsData['Google Maps'] = `<a class="gps-link" href="https://maps.google.com/?q=${meta.latitude},${meta.longitude}" target="_blank" rel="noopener">View on Google Maps ↺/a>`;
          gpsData['OpenStreetMap'] = `<a class="gps-link" href="https://www.openstreetmap.org/?mlat=${meta.latitude}&mlon=${meta.longitude}" target="_blank" rel="noopener">View on OSM ↺/a>`;
        }
        html += buildMetaSection('📍 GPS Location', gpsData, 'gps');
      }

      // IPTC section
      const iptcFields = ['Headline','Caption','Credit','Source','CopyrightNotice','ObjectName',
        'Keywords','DateCreated','Byline','BylineTitle','City','ProvinceState','CountryName','CountryCode'];
      const iptcData = {};
      let hasIPTC = false;
      iptcFields.forEach(f => { if (meta[f] !== undefined) { iptcData[f] = meta[f]; hasIPTC = true; } });
      if (meta.iptc && typeof meta.iptc === 'object') {
        Object.assign(iptcData, meta.iptc);
        hasIPTC = true;
      }
      if (hasIPTC) {
        html += buildMetaSection('🏷️ IPTC —Copyright & Caption', iptcData, 'iptc');
      }

      // File info section
      if (currentFile) {
        const fileData = {
          'File Name': currentFile.name,
          'File Size': formatBytes(currentFile.size),
          'MIME Type': currentFile.type || 'unknown',
          'Last Modified': new Date(currentFile.lastModified).toLocaleString(),
        };
        html += buildMetaSection('📁 File Information', fileData, 'file');
      }

      // XMP section (simplified)
      if (meta.xmp && typeof meta.xmp === 'object') {
        const xmpData = {};
        Object.keys(meta.xmp).slice(0, 20).forEach(k => { xmpData[k] = meta.xmp[k]; });
        html += buildMetaSection('📑 XMP Data', xmpData, 'xmp');
      }

      container.innerHTML = html || '<div class="no-meta">No standard metadata found.</div>';

      // Toggle handlers
      document.querySelectorAll('.meta-section-header').forEach(h => {
        h.addEventListener('click', () => h.parentElement.classList.toggle('open'));
      });

      // Show GPS warning
      document.getElementById('privacyWarning').style.display = hasGPS ? 'block' : 'none';
    }

    function buildMetaSection(title, dataObj, id) {
      let rows = '';
      for (const [key, val] of Object.entries(dataObj)) {
        const displayVal = Array.isArray(val) ? val.join(', ') : (typeof val === 'object' ? JSON.stringify(val) : String(val));
        rows += `<tr><td>${escapeHtml(key)}</td><td>${displayVal.startsWith('<a') ? displayVal : escapeHtml(displayVal)}</td></tr>`;
      }
      return `<div class="meta-section" id="section-${id}">
        <div class="meta-section-header">${title} <span class="toggle-icon"></span></div>
        <div class="meta-section-body"><table class="meta-table">${rows}</table></div>
      </div>`;
    }

    function escapeHtml(s) {
      const d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }

    function formatBytes(b) {
      if (b < 1024) return b + ' B';
      if (b < 1048576) return (b/1024).toFixed(1) + ' KB';
      return (b/1048576).toFixed(1) + ' MB';
    }

    function downloadClean() {
      if (!currentImageDataUrl) return;
      // Create canvas and re-draw without metadata (canvas automatically strips metadata)
      const img = new Image();
      img.onload = () => {
        const c = document.createElement('canvas');
        c.width = img.width;
        c.height = img.height;
        c.getContext('2d').drawImage(img, 0, 0);
        const ext = currentFile.name.includes('.') ? currentFile.name.split('.').pop().split('?')[0] : 'png';
        const fmt = (ext === 'jpg' || ext === 'jpeg') ? 'image/jpeg' : 'image/png';
        const link = document.createElement('a');
        link.download = currentFile.name.replace(/\.[^.]+$/, '') + '_clean.' + (fmt === 'image/jpeg' ? 'jpg' : 'png');
        link.href = c.toDataURL(fmt);
        link.click();
      };
      img.src = currentImageDataUrl;
    }

    function downloadJSON() {
      if (!parsedMetadata) return;
      const json = JSON.stringify(parsedMetadata, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const link = document.createElement('a');
      link.download = (currentFile ? currentFile.name.replace(/\.[^.]+$/, '') : 'metadata') + '.json';
      link.href = URL.createObjectURL(blob);
      link.click();
      URL.revokeObjectURL(link.href);
    }

    function showLoading(show) {
      document.body.style.cursor = show ? 'wait' : 'default';
    }

    // FAQ
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => { btn.parentElement.classList.toggle('active'); });
    });