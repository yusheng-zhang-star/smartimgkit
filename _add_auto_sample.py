path = r'E:\网站项目\smartimgkit\tools\photo-map.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Modify checkSharedLocation to also check for sample parameter
old_init = '''    // Check for shared location in URL
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
    checkSharedLocation();'''

new_init = '''    // Check for shared location or sample data in URL
    function checkSharedLocation() {
      const params = new URLSearchParams(window.location.search);
      const lat = params.get('lat');
      const lon = params.get('lon');
      const sample = params.get('sample');
      
      if (sample === '1') {
        // Auto-load sample data
        setTimeout(function() { loadSampleData(); }, 500);
      } else if (lat && lon) {
        dropzone.style.display = 'none';
        showSingleLocation(parseFloat(lat), parseFloat(lon));
      }
    }

    // Initialize
    checkSharedLocation();'''

content = content.replace(old_init, new_init)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('OK: Auto-load sample data via ?sample=1 parameter')
