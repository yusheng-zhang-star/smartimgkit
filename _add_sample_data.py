path = r'E:\网站项目\smartimgkit\tools\photo-map.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add sample data button to dropzone
old_dropzone = '''          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
        </div>'''

new_dropzone = '''          <div class="formats">Supports JPG, JPEG, PNG, HEIC, WebP — Multiple files OK</div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none">
          <div style="margin-top:16px;">
            <button class="btn btn-secondary" onclick="loadSampleData(event)" style="background:var(--bg-tertiary); border:1px solid var(--border-color); color:var(--text-primary); padding:8px 16px; border-radius:8px; cursor:pointer;">✨ Try with sample data</button>
          </div>
        </div>'''

content = content.replace(old_dropzone, new_dropzone)

# 2. Add loadSampleData function before checkSharedLocation
old_init = '''    // Check for shared location in URL
    function checkSharedLocation() {'''

new_init = '''    // Load sample data for testing
    window.loadSampleData = function(e) {
      if (e) e.stopPropagation();
      dropzone.style.display = 'none';
      
      var samples = [
        { name: 'jinan_spring.jpg', lat: 36.639, lon: 117.1425, date: '2026-09-10T10:00:00' },
        { name: 'beijing_forbidden_city.jpg', lat: 39.9163, lon: 116.3972, date: '2026-09-08T14:30:00' },
        { name: 'shanghai_bund.jpg', lat: 31.2397, lon: 121.4900, date: '2026-09-05T18:00:00' },
        { name: 'guangzhou_canton_tower.jpg', lat: 23.1066, lon: 113.3245, date: '2026-09-02T20:00:00' },
        { name: 'no_gps_screenshot.png', lat: null, lon: null, date: null }
      ];
      
      samples.forEach(function(s, i) {
        // Create a simple colored canvas as placeholder
        var canvas = document.createElement('canvas');
        canvas.width = 200;
        canvas.height = 200;
        var ctx = canvas.getContext('2d');
        var colors = ['#4682B4', '#CD853F', '#2E8B57', '#DC143C', '#708090'];
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillRect(0, 0, 200, 200);
        ctx.fillStyle = 'white';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(s.name.substring(0, 12), 100, 100);
        
        photos.push({
          name: s.name,
          url: canvas.toDataURL('image/jpeg'),
          lat: s.lat,
          lon: s.lon,
          date: s.date,
          hasGPS: s.lat !== null
        });
      });
      
      updateUI();
      updateMap();
    };

    // Check for shared location in URL
    function checkSharedLocation() {'''

content = content.replace(old_init, new_init)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: Sample data button added')
