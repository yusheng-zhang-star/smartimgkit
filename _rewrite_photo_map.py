path = r'E:\网站项目\smartimgkit\tools\photo-map.html'

new_content = '''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-tool-id="photo-map">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <title>Photo Location Map — View Where Photos Were Taken | SmartImgKit</title>
  <meta name="description" content="Upload photos and see where they were taken on an interactive map. Extract GPS coordinates from EXIF data, view photo locations, and share. Free, private, browser-based.">
  <meta name="keywords" content="photo location map, where was this photo taken, photo GPS viewer, EXIF GPS location, photo map, geotag viewer, photo location finder">
  <link rel="canonical" href="https://smartimgkit.com/tools/photo-map">
  <meta name="theme-color" content="#6366f1">
  <meta property="og:title" content="Photo Location Map — See Where Your Photos Were Taken">
  <meta property="og:description" content="Upload photos and instantly see where they were taken on an interactive map. Free, private, no upload to server.">
  <meta property="og:url" content="https://smartimgkit.com/tools/photo-map">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="SmartImgKit">
  <meta property="og:image" content="https://smartimgkit.com/screenshots/home.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Photo Location Map — See Where Your Photos Were Taken">
  <meta name="twitter:description" content="Upload photos and instantly see where they were taken on an interactive map.">
  <meta name="twitter:image" content="https://smartimgkit.com/screenshots/home.png">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate" hreflang="x-default" href="https://smartimgkit.com/tools/photo-map">
  <link rel="stylesheet" href="/css/style.css?v=10">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Photo Location Map",
  "url": "https://smartimgkit.com/tools/photo-map",
  "applicationCategory": "MultimediaApplication",
  "operatingSystem": "Any",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "description": "View photo GPS locations on an interactive map. Extract EXIF coordinates and see where photos were taken."
}
  </script>
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Find Where a Photo Was Taken",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "Upload Photos", "text": "Drag and drop or select photos from your device."},
    {"@type": "HowToStep", "position": 2, "name": "View on Map", "text": "GPS coordinates are extracted from EXIF and shown on an interactive map."},
    {"@type": "HowToStep", "position": 3, "name": "Explore & Share", "text": "Click photos to view locations, share the map, or export GPX."}
  ]
}
  </script>
  <style>
    .tool-hero { text-align: center; padding: 48px 24px 32px; }
    .tool-hero h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 12px; background: linear-gradient(135deg, var(--gradient-from), var(--gradient-to)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .tool-hero p { color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto; }
    .tool-body { max-width: 1200px; margin: 0 auto; padding: 0 24px 48px; }
    .stats-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 20px; text-align: center; }
    .stat-number { font-size: 1.8rem; font-weight: 700; color: var(--accent); }
    .stat-label { font-size: 0.85rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
    .map-layout { display: grid; grid-template-columns: 1fr 320px; gap: 16px; min-height: 500px; position: relative; }
    @media(max-width: 900px) { .map-layout { grid-template-columns: 1fr; } .stats-bar { grid-template-columns: repeat(2, 1fr); } }
    .map-wrapper { position: relative; border-radius: 12px; overflow: hidden; border: 1px solid var(--border-color); height: 520px; }
    .map-wrapper iframe { width: 100%; height: 100%; border: none; display: block; }
    .dropzone-map { position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: 10; background: var(--bg-secondary); display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: opacity 0.2s; }
    .dropzone-map.dragover { background: var(--bg-tertiary); border: 2px dashed var(--accent); }
    .dropzone-map .icon { font-size: 3rem; margin-bottom: 16px; }
    .dropzone-map h3 { font-size: 1.2rem; margin-bottom: 8px; }
    .dropzone-map p { color: var(--text-secondary); margin-bottom: 12px; }
    .dropzone-map .formats { font-size: 0.8rem; color: var(--text-muted); }
    .photo-sidebar { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 16px; display: flex; flex-direction: column; }
    .photo-sidebar h3 { font-size: 1rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    .photo-list { flex: 1; overflow-y: auto; max-height: 400px; }
    .photo-item { display: flex; gap: 12px; padding: 10px; border-radius: 8px; cursor: pointer; margin-bottom: 8px; border: 1px solid transparent; transition: all 0.2s; }
    .photo-item:hover { background: var(--bg-card-hover); }
    .photo-item.active { border-color: var(--accent); background: var(--accent-glow); }
    .photo-item img { width: 48px; height: 48px; object-fit: cover; border-radius: 6px; flex-shrink: 0; }
    .photo-item-info { flex: 1; min-width: 0; }
    .photo-item-name { font-size: 0.85rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .photo-item-coords { font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }
    .photo-item-date { font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }
    .photo-item.nogps { opacity: 0.5; }
    .sidebar-actions { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-color); }
    .btn { padding: 10px 16px; border-radius: 8px; font-size: 0.9rem; font-weight: 500; cursor: pointer; transition: all 0.2s; border: none; display: flex; align-items: center; justify-content: center; gap: 8px; }
    .btn-primary { background: var(--accent); color: white; }
    .btn-primary:hover { opacity: 0.9; }
    .btn-secondary { background: var(--bg-tertiary); color: var(--text-primary); border: 1px solid var(--border-color); }
    .btn-secondary:hover { background: var(--bg-card-hover); }
    .faq-section { max-width: 800px; margin: 48px auto; padding: 0 24px; }
    .faq-section h2 { font-size: 1.5rem; margin-bottom: 24px; text-align: center; }
    .faq-item { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 12px; overflow: hidden; }
    .faq-question { padding: 16px 20px; cursor: pointer; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }
    .faq-answer { padding: 0 20px 16px; color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; display: none; }
    .faq-item.open .faq-answer { display: block; }
    .related-tools { max-width: 1200px; margin: 48px auto; padding: 0 24px; }
    .related-tools h2 { font-size: 1.5rem; margin-bottom: 24px; text-align: center; }
    .tools-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; }
    .tool-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 24px; text-decoration: none; transition: all 0.2s; }
    .tool-card:hover { border-color: var(--accent); transform: translateY(-2px); }
    .tool-card .icon { font-size: 2rem; margin-bottom: 12px; }
    .tool-card h3 { font-size: 1.1rem; margin-bottom: 8px; }
    .tool-card p { font-size: 0.9rem; color: var(--text-secondary); }
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">🎨 SmartImgKit</a>
      <nav class="nav-links">
        <a href="/">Home</a>
        <a href="/tools/">Tools</a>
        <a href="/workflows/">Workflows</a>
        <a href="/blog/">Blog</a>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
      </nav>
    </div>
  </header>

  <section class="tool-hero">
    <h1>📍 Photo Location Map</h1>
    <p>Upload your photos and instantly see where they were taken on an interactive map. GPS coordinates are extracted directly from EXIF data — 100% private, nothing uploaded to any server.</p>
  </section>

  <div class="tool-body">
    <!-- Stats -->
    <div class="stats-bar">
      <div class="stat-card"><div class="stat-number" id="statTotal">0</div><div class="stat-label">Photos</div></div>
      <div class="stat-card"><div class="stat-number" id="statGPS">0</div><div class="stat-label">With GPS</div></div>
      <div class="stat-card"><div class="stat-number" id="statNoGPS">0</div><div class="stat-label">No GPS</div></div>
      <div class="stat-card"><div class="stat-number" id="statLocations">0</div><div class="stat-label">Locations</div></div>
    </div>

    <!-- Map + Sidebar -->
    <div class="map-layout">
      <div class="map-wrapper">
        <iframe id="mapFrame" src="about:blank" loading="lazy"></iframe>
        <!-- Upload Overlay -->
        <div class="dropzone-map" id="dropzone">
          <div class="icon">📸</div>
          <h3>Drop photos here or click to browse</h3>
          <p>We'll extract GPS coordinates and plot them on the map</p>
          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
        </div>
      </div>
      <div class="photo-sidebar">
        <h3>📷 Photos <span id="photoCount" style="margin-left:auto; background:var(--bg-tertiary); padding:2px 8px; border-radius:12px; font-size:0.8rem;">0</span></h3>
        <div class="photo-list" id="photoList">
          <p style="color:var(--text-muted); text-align:center; padding:20px; font-size:0.9rem;">No photos yet. Upload some to get started!</p>
        </div>
        <div class="sidebar-actions">
          <button class="btn btn-primary" id="shareBtn" disabled>🔗 Share Map</button>
          <button class="btn btn-secondary" id="gpxBtn" disabled>📥 Export GPX</button>
          <button class="btn btn-secondary" id="resetBtn">🔄 Reset</button>
        </div>
      </div>
    </div>
  </div>

  <!-- FAQ -->
  <section class="faq-section">
    <h2>Frequently Asked Questions</h2>
    <div class="faq-item">
      <div class="faq-question">How does photo location map work? <span>+</span></div>
      <div class="faq-answer">When you upload a photo, our tool reads the EXIF metadata embedded in the image file. Most smartphones and digital cameras automatically record GPS coordinates when a photo is taken. We extract these coordinates and display them on an interactive map powered by OpenStreetMap.</div>
    </div>
    <div class="faq-item">
      <div class="faq-question">Are my photos uploaded to a server? <span>+</span></div>
      <div class="faq-answer">No! All processing happens directly in your browser. Your photos never leave your device. This means your location data stays completely private and secure.</div>
    </div>
    <div class="faq-item">
      <div class="faq-question">Why don't some photos show GPS data? <span>+</span></div>
      <div class="faq-answer">Photos may lack GPS data if location services were disabled on the camera/phone, if the photo was edited and metadata was stripped, or if the camera doesn't have GPS capability. You can check our EXIF viewer tool to see all metadata in a photo.</div>
    </div>
    <div class="faq-item">
      <div class="faq-question">Can I share my photo map? <span>+</span></div>
      <div class="faq-answer">Yes! Click the "Share Map" button to generate a shareable link. The link includes the GPS coordinates so recipients can see the same map view. Note: photos themselves are not shared, only the locations.</div>
    </div>
  </section>

  <!-- Related Tools -->
  <section class="related-tools">
    <h2>Related Tools</h2>
    <div class="tools-grid">
      <a href="/tools/metadata-viewer" class="tool-card"><div class="icon">🔍</div><h3>EXIF Metadata Viewer</h3><p>View all metadata embedded in your photos including camera settings, GPS, and more.</p></a>
      <a href="/tools/image-exif-remover" class="tool-card"><div class="icon">🛡️</div><h3>EXIF Remover</h3><p>Strip all metadata from your photos to protect your privacy before sharing online.</p></a>
      <a href="/tools/batch-exif-remover" class="tool-card"><div class="icon">📦</div><h3>Batch EXIF Remover</h3><p>Remove metadata from multiple photos at once and download as a ZIP file.</p></a>
    </div>
  </section>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 SmartImgKit. All rights reserved.</p>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/exifr/7.1.3/full.min.js"></script>
  <script>
    // State
    let photos = [];
    let selectedIndex = -1;

    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const mapFrame = document.getElementById('mapFrame');
    const photoList = document.getElementById('photoList');
    const photoCount = document.getElementById('photoCount');
    const shareBtn = document.getElementById('shareBtn');
    const gpxBtn = document.getElementById('gpxBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Stats
    const statTotal = document.getElementById('statTotal');
    const statGPS = document.getElementById('statGPS');
    const statNoGPS = document.getElementById('statNoGPS');
    const statLocations = document.getElementById('statLocations');

    // Event Listeners
    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => { e.preventDefault(); dropzone.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });
    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
    shareBtn.addEventListener('click', shareMap);
    gpxBtn.addEventListener('click', exportGPX);
    resetBtn.addEventListener('click', resetAll);

    // FAQ toggle
    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
    });

    // Handle file uploads
    async function handleFiles(files) {
      const fileArray = Array.from(files).filter(f => f.type.startsWith('image/'));
      if (fileArray.length === 0) return;

      dropzone.style.display = 'none';

      for (const file of fileArray) {
        try {
          const data = await exifr.parse(file, { gps: true });
          const hasGPS = data && data.latitude && data.longitude;
          const photo = {
            name: file.name,
            file: file,
            url: URL.createObjectURL(file),
            lat: hasGPS ? data.latitude : null,
            lon: hasGPS ? data.longitude : null,
            date: data && data.DateTimeOriginal ? data.DateTimeOriginal : null,
            hasGPS: hasGPS
          };
          photos.push(photo);
        } catch (e) {
          photos.push({
            name: file.name,
            file: file,
            url: URL.createObjectURL(file),
            lat: null,
            lon: null,
            date: null,
            hasGPS: false
          });
        }
      }

      updateUI();
      updateMap();
    }

    // Update UI
    function updateUI() {
      const gpsPhotos = photos.filter(p => p.hasGPS);
      const noGPSPhotos = photos.filter(p => !p.hasGPS);
      const uniqueLocations = new Set(gpsPhotos.map(p => p.lat.toFixed(4) + ',' + p.lon.toFixed(4)));

      statTotal.textContent = photos.length;
      statGPS.textContent = gpsPhotos.length;
      statNoGPS.textContent = noGPSPhotos.length;
      statLocations.textContent = uniqueLocations.size;
      photoCount.textContent = photos.length;

      shareBtn.disabled = gpsPhotos.length === 0;
      gpxBtn.disabled = gpsPhotos.length === 0;

      // Render photo list
      if (photos.length === 0) {
        photoList.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:20px; font-size:0.9rem;">No photos yet. Upload some to get started!</p>';
        return;
      }

      photoList.innerHTML = photos.map((p, i) => `
        <div class="photo-item ${p.hasGPS ? '' : 'nogps'} ${i === selectedIndex ? 'active' : ''}" onclick="selectPhoto(${i})">
          <img src="${p.url}" alt="${p.name}">
          <div class="photo-item-info">
            <div class="photo-item-name">${p.name}</div>
            <div class="photo-item-coords">${p.hasGPS ? p.lat.toFixed(4) + ', ' + p.lon.toFixed(4) : 'No GPS data'}</div>
            <div class="photo-item-date">${p.date ? new Date(p.date).toLocaleDateString() : 'Unknown date'}</div>
          </div>
        </div>
      `).join('');
    }

    // Select photo
    window.selectPhoto = function(index) {
      selectedIndex = index;
      updateUI();
      if (photos[index].hasGPS) {
        showSingleLocation(photos[index].lat, photos[index].lon);
      }
    };

    // Update map to show all GPS photos
    function updateMap() {
      const gpsPhotos = photos.filter(p => p.hasGPS);
      if (gpsPhotos.length === 0) {
        mapFrame.src = 'about:blank';
        return;
      }

      if (gpsPhotos.length === 1) {
        showSingleLocation(gpsPhotos[0].lat, gpsPhotos[0].lon);
      } else {
        showAllLocations(gpsPhotos);
      }
    }

    // Show single location on map
    function showSingleLocation(lat, lon) {
      const delta = 0.05;
      const bbox = `${lon - delta},${lat - delta},${lon + delta},${lat + delta}`;
      const url = `https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(bbox)}&layer=mapnik&marker=${lat},${lon}`;
      mapFrame.src = url;
    }

    // Show all locations on map
    function showAllLocations(gpsPhotos) {
      const lats = gpsPhotos.map(p => p.lat);
      const lons = gpsPhotos.map(p => p.lon);
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLon = Math.min(...lons);
      const maxLon = Math.max(...lons);
      const latPad = (maxLat - minLat) * 0.2 + 0.01;
      const lonPad = (maxLon - minLon) * 0.2 + 0.01;
      const bbox = `${minLon - lonPad},${minLat - latPad},${maxLon + lonPad},${maxLat + latPad}`;
      
      // Use first photo as marker (OSM embed only supports one marker)
      const marker = gpsPhotos[0];
      const url = `https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(bbox)}&layer=mapnik&marker=${marker.lat},${marker.lon}`;
      mapFrame.src = url;
    }

    // Share map
    function shareMap() {
      const gpsPhotos = photos.filter(p => p.hasGPS);
      if (gpsPhotos.length === 0) return;

      const lats = gpsPhotos.map(p => p.lat);
      const lons = gpsPhotos.map(p => p.lon);
      const centerLat = (Math.min(...lats) + Math.max(...lats)) / 2;
      const centerLon = (Math.min(...lons) + Math.max(...lons)) / 2;
      
      const shareUrl = `${window.location.origin}${window.location.pathname}?lat=${centerLat.toFixed(6)}&lon=${centerLon.toFixed(6)}`;
      
      if (navigator.clipboard) {
        navigator.clipboard.writeText(shareUrl).then(() => {
          alert('Map link copied to clipboard!\\n\\n' + shareUrl);
        });
      } else {
        prompt('Copy this link to share:', shareUrl);
      }
    }

    // Export GPX
    function exportGPX() {
      const gpsPhotos = photos.filter(p => p.hasGPS);
      if (gpsPhotos.length === 0) return;

      let gpx = '<?xml version="1.0" encoding="UTF-8"?>\\n';
      gpx += '<gpx version="1.1" creator="SmartImgKit" xmlns="http://www.topografix.com/GPX/1/1">\\n';
      
      gpsPhotos.forEach((p, i) => {
        gpx += `  <wpt lat="${p.lat}" lon="${p.lon}">\\n`;
        gpx += `    <name>${p.name}</name>\\n`;
        if (p.date) gpx += `    <time>${new Date(p.date).toISOString()}</time>\\n`;
        gpx += '  </wpt>\\n';
      });
      
      gpx += '</gpx>';

      const blob = new Blob([gpx], { type: 'application/gpx+xml' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'photo-locations.gpx';
      a.click();
      URL.revokeObjectURL(url);
    }

    // Reset
    function resetAll() {
      photos.forEach(p => URL.revokeObjectURL(p.url));
      photos = [];
      selectedIndex = -1;
      dropzone.style.display = 'flex';
      mapFrame.src = 'about:blank';
      fileInput.value = '';
      updateUI();
    }

    // Check for shared location in URL
    function checkSharedLocation() {
      const params = new URLSearchParams(window.location.search);
      const lat = params.get('lat');
      const lon = params.get('lon');
      if (lat && lon) {
        dropzone.style.display = 'none';
        showSingleLocation(parseFloat(lat), parseFloat(lon));
      }
    }

    // Initialize
    checkSharedLocation();
  </script>
</body>
</html>
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('OK: photo-map.html rewritten with iframe solution')
