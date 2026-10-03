path = r'E:\网站项目\smartimgkit\tools\photo-map.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace HTML structure: move dropzone inside mapContainer as overlay
old_html = '''      <div class="tool-workspace">
        <!-- Upload Zone -->
        <div class="dropzone-map" id="dropzone">
          <div class="icon">📸</div>
          <h3>Drop photos here or click to browse</h3>
          <p>We'll extract GPS coordinates and plot them on the map</p>
          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
        </div>

        <!-- Map View (hidden until photos loaded) -->
        <div class="photo-map-container" id="mapContainer" style="display:none;">
          <div class="stats-bar">
            <div class="stat-item"><div class="stat-value" id="totalPhotos">0</div><div class="stat-label">Photos</div></div>
            <div class="stat-item"><div class="stat-value" id="gpsPhotos">0</div><div class="stat-label">With GPS</div></div>
            <div class="stat-item"><div class="stat-value" id="noGpsPhotos">0</div><div class="stat-label">No GPS</div></div>
            <div class="stat-item"><div class="stat-value" id="uniqueLocations">0</div><div class="stat-label">Locations</div></div>
          </div>

          <div class="map-layout">
            <div id="map"></div>
            <div class="photo-sidebar">
              <div class="sidebar-header">
                <h3>📷 Photos</h3>
                <span class="photo-count" id="photoCount">0</span>
              </div>
              <div class="photo-list" id="photoList"></div>
              <div class="map-actions">
                <button class="map-btn primary" id="shareBtn" disabled>🔗 Share Map</button>
                <button class="map-btn secondary" id="gpxBtn" disabled>📥 Export GPX</button>
                <button class="map-btn secondary" id="resetBtn">🔄 Reset</button>
              </div>
            </div>
          </div>
        </div>
      </div>'''

new_html = '''      <div class="tool-workspace">
        <div class="photo-map-container" id="mapContainer">
          <div class="stats-bar">
            <div class="stat-item"><div class="stat-value" id="totalPhotos">0</div><div class="stat-label">Photos</div></div>
            <div class="stat-item"><div class="stat-value" id="gpsPhotos">0</div><div class="stat-label">With GPS</div></div>
            <div class="stat-item"><div class="stat-value" id="noGpsPhotos">0</div><div class="stat-label">No GPS</div></div>
            <div class="stat-item"><div class="stat-value" id="uniqueLocations">0</div><div class="stat-label">Locations</div></div>
          </div>

          <div class="map-layout" style="position:relative;">
            <div id="map"></div>
            <div class="photo-sidebar">
              <div class="sidebar-header">
                <h3>📷 Photos</h3>
                <span class="photo-count" id="photoCount">0</span>
              </div>
              <div class="photo-list" id="photoList"></div>
              <div class="map-actions">
                <button class="map-btn primary" id="shareBtn" disabled>🔗 Share Map</button>
                <button class="map-btn secondary" id="gpxBtn" disabled>📥 Export GPX</button>
                <button class="map-btn secondary" id="resetBtn">🔄 Reset</button>
              </div>
            </div>
            <!-- Upload Overlay -->
            <div class="dropzone-map" id="dropzone" style="position:absolute; top:0; left:0; right:336px; bottom:0; z-index:10; background:var(--bg-primary); border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
              <div class="icon">📸</div>
              <h3>Drop photos here or click to browse</h3>
              <p>We'll extract GPS coordinates and plot them on the map</p>
              <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
              <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
            </div>
          </div>
        </div>
      </div>'''

content = content.replace(old_html, new_html)

# 2. Add responsive CSS for overlay
old_css = '''    @media(max-width: 900px) { .map-layout { grid-template-columns: 1fr; } }'''
new_css = '''    @media(max-width: 900px) { .map-layout { grid-template-columns: 1fr; } #dropzone { right:0 !important; bottom:50% !important; } }'''
content = content.replace(old_css, new_css)

# 3. Replace JS: init map on page load, handleFiles just hides overlay
old_js = '''    async function handleFiles(files) {
      const imageFiles = Array.from(files).filter(f => f.type.startsWith('image/'));
      if (imageFiles.length === 0) { alert('Please select image files.'); return; }

      dropzone.style.display = 'none';
      mapContainer.style.display = 'flex';

      // Wait for layout to settle, then init map
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));

      if (!map) {
        initMap();
      }
      map.invalidateSize();

      for (const file of imageFiles) {
        await processFile(file);
      }
      updateStats();
      fitMapToMarkers();
      map.invalidateSize();
    }

    function initMap() {
      const mapEl = document.getElementById('map');
      mapEl.style.width = '100%';
      mapEl.style.height = '520px';
      map = L.map('map').setView([20, 0], 2);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);
      map.invalidateSize();
    }'''

new_js = '''    async function handleFiles(files) {
      const imageFiles = Array.from(files).filter(f => f.type.startsWith('image/'));
      if (imageFiles.length === 0) { alert('Please select image files.'); return; }

      dropzone.style.display = 'none';
      map.invalidateSize();

      for (const file of imageFiles) {
        await processFile(file);
      }
      updateStats();
      fitMapToMarkers();
      map.invalidateSize();
    }

    function initMap() {
      map = L.map('map').setView([20, 0], 2);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(map);
    }'''

content = content.replace(old_js, new_js)

# 4. Add map initialization on page load (before other event listeners)
old_init = '''    // Drag and drop
    dropzone.addEventListener('click', () => fileInput.click());'''
new_init = '''    // Init map immediately (container is visible)
    initMap();

    // Drag and drop
    dropzone.addEventListener('click', () => fileInput.click());'''
content = content.replace(old_init, new_init)

# 5. Fix reset function to show overlay again
old_reset = '''    document.getElementById('resetBtn').addEventListener('click', () => {
      photos = [];
      markers = [];
      photoList.innerHTML = '';
      map.remove();
      map = null;
      mapContainer.style.display = 'none';
      dropzone.style.display = 'flex';
      updateStats();
      fileInput.value = '';
    });'''
new_reset = '''    document.getElementById('resetBtn').addEventListener('click', () => {
      photos = [];
      markers.forEach(m => map.removeLayer(m.marker));
      markers = [];
      photoList.innerHTML = '';
      dropzone.style.display = 'flex';
      updateStats();
      fileInput.value = '';
      map.setView([20, 0], 2);
      map.invalidateSize();
    });'''
content = content.replace(old_reset, new_reset)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: photo-map.html fully restructured')
