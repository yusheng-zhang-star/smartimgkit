
    let map = null;
    let markers = [];
    let photos = [];
    let activePhotoIndex = -1;

    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const mapContainer = document.getElementById('mapContainer');
    const photoList = document.getElementById('photoList');
    const photoCount = document.getElementById('photoCount');

    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('drag'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag'));
    dropzone.addEventListener('drop', e => {
      e.preventDefault();
      dropzone.classList.remove('drag');
      handleFiles(e.dataTransfer.files);
    });
    fileInput.addEventListener('change', e => handleFiles(e.target.files));

    // Init map on page load - container is always visible
    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);
    setTimeout(() => map.invalidateSize(), 100);

    async function handleFiles(files) {
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

    function processFile(file) {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = async e => {
          const dataUrl = e.target.result;
          let gps = null;
          let dateTime = null;

          try {
            const exif = await exifr.parse(file, { gps: true, exif: true });
            if (exif && exif.latitude && exif.longitude) {
              gps = { lat: exif.latitude, lng: exif.longitude };
            }
            if (exif && exif.DateTimeOriginal) {
              dateTime = exif.DateTimeOriginal;
            }
          } catch (err) {
            console.log('EXIF parse error:', err);
          }

          const photo = {
            name: file.name,
            dataUrl,
            gps,
            dateTime,
            index: photos.length
          };
          photos.push(photo);

          if (gps && map) {
            const marker = L.marker([gps.lat, gps.lng]).addTo(map);
            const popupContent = `
              <img src="${dataUrl}" alt="${file.name}">
              <div class="popup-name">${file.name}</div>
              <div class="popup-coords">${gps.lat.toFixed(6)}, ${gps.lng.toFixed(6)}</div>
            `;
            marker.bindPopup(popupContent);
            marker.on('click', () => setActivePhoto(photo.index));
            markers.push({ marker, photoIndex: photo.index });
          }

          renderPhotoList();
          resolve();
        };
        reader.onerror = () => resolve();
        reader.readAsDataURL(file);
      });
    }

    function renderPhotoList() {
      photoList.innerHTML = '';
      photos.forEach((photo, i) => {
        const item = document.createElement('div');
        item.className = 'photo-item' + (photo.gps ? '' : ' no-gps') + (i === activePhotoIndex ? ' active' : '');
        item.innerHTML = `
          <img src="${photo.dataUrl}" class="photo-thumb" alt="${photo.name}">
          <div class="photo-info">
            <div class="photo-name">${photo.name}</div>
            <div class="photo-coords">${photo.gps ? `${photo.gps.lat.toFixed(4)}, ${photo.gps.lng.toFixed(4)}` : '⚠️ No GPS data'}</div>
            ${photo.dateTime ? `<div class="photo-date">${new Date(photo.dateTime).toLocaleDateString()}</div>` : ''}
          </div>
        `;
        item.addEventListener('click', () => {
          if (photo.gps) {
            setActivePhoto(i);
            map.setView([photo.gps.lat, photo.gps.lng], 14);
            markers.find(m => m.photoIndex === i)?.marker.openPopup();
          }
        });
        photoList.appendChild(item);
      });
      photoCount.textContent = photos.length;
    }

    function setActivePhoto(index) {
      activePhotoIndex = index;
      document.querySelectorAll('.photo-item').forEach((el, i) => {
        el.classList.toggle('active', i === index);
      });
    }

    function updateStats() {
      const withGps = photos.filter(p => p.gps).length;
      const noGps = photos.length - withGps;
      const uniqueLocs = new Set(photos.filter(p => p.gps).map(p => `${p.gps.lat.toFixed(4)},${p.gps.lng.toFixed(4)}`)).size;

      document.getElementById('totalPhotos').textContent = photos.length;
      document.getElementById('gpsPhotos').textContent = withGps;
      document.getElementById('noGpsPhotos').textContent = noGps;
      document.getElementById('uniqueLocations').textContent = uniqueLocs;

      document.getElementById('shareBtn').disabled = withGps === 0;
      document.getElementById('gpxBtn').disabled = withGps === 0;
    }

    function fitMapToMarkers() {
      if (markers.length > 0) {
        const group = L.featureGroup(markers.map(m => m.marker));
        map.fitBounds(group.getBounds().pad(0.2));
      }
    }

    // Share map
    document.getElementById('shareBtn').addEventListener('click', () => {
      const gpsPhotos = photos.filter(p => p.gps);
      if (gpsPhotos.length === 0) return;
      const coords = gpsPhotos.map(p => `${p.gps.lat.toFixed(6)},${p.gps.lng.toFixed(6)}`).join('|');
      const shareUrl = `${window.location.origin}${window.location.pathname}?p=${encodeURIComponent(coords)}`;
      navigator.clipboard.writeText(shareUrl).then(() => {
        alert('Share link copied to clipboard!\n\n' + shareUrl);
      }).catch(() => {
        prompt('Copy this share link:', shareUrl);
      });
    });

    // Export GPX
    document.getElementById('gpxBtn').addEventListener('click', () => {
      const gpsPhotos = photos.filter(p => p.gps);
      if (gpsPhotos.length === 0) return;

      let gpx = '<?xml version="1.0" encoding="UTF-8"?>\n';
      gpx += '<gpx version="1.1" creator="SmartImgKit Photo Map">\n';
      gpsPhotos.forEach((p, i) => {
        gpx += `  <wpt lat="${p.gps.lat}" lon="${p.gps.lng}">\n`;
        gpx += `    <name>${p.name}</name>\n`;
        if (p.dateTime) gpx += `    <time>${new Date(p.dateTime).toISOString()}</time>\n`;
        gpx += `  </wpt>\n`;
      });
      gpx += '</gpx>';

      const blob = new Blob([gpx], { type: 'application/gpx+xml' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'photo-locations.gpx';
      a.click();
      URL.revokeObjectURL(url);
    });

    // Reset
    document.getElementById('resetBtn').addEventListener('click', () => {
      photos = [];
      markers.forEach(m => map.removeLayer(m.marker));
      markers = [];
      activePhotoIndex = -1;
      dropzone.style.display = 'flex';
      fileInput.value = '';
      updateStats();
      map.setView([20, 0], 2);
      map.invalidateSize();
    });

    // Load from URL params (shared map)
    const urlParams = new URLSearchParams(window.location.search);
    const sharedPoints = urlParams.get('p');
    if (sharedPoints) {
      const points = sharedPoints.split('|').map(p => {
        const [lat, lng] = p.split(',').map(Number);
        return { lat, lng };
      });
      if (points.length > 0) {
        dropzone.style.display = 'none';
        points.forEach((pt, i) => {
          L.marker([pt.lat, pt.lng]).addTo(map)
            .bindPopup(`<div class="popup-name">Shared Location ${i + 1}</div><div class="popup-coords">${pt.lat.toFixed(6)}, ${pt.lng.toFixed(6)}</div>`);
        });
        const group = L.featureGroup(points.map(p => L.marker([p.lat, p.lng])));
        map.fitBounds(group.getBounds().pad(0.2));
        map.invalidateSize();
        document.getElementById('totalPhotos').textContent = points.length;
        document.getElementById('gpsPhotos').textContent = points.length;
        document.getElementById('uniqueLocations').textContent = new Set(points.map(p => `${p.lat.toFixed(4)},${p.lng.toFixed(4)}`)).size;
      }
    }

    // FAQ toggle
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => {
        const answer = btn.nextElementSibling;
        const arrow = btn.querySelector('span');
        answer.style.display = answer.style.display === 'none' ? 'block' : 'none';
        arrow.textContent = answer.style.display === 'none' ? '▼' : '▲';
      });
    });
  