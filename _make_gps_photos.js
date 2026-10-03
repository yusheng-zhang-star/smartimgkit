const piexif = require('piexifjs');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Download a simple image
function downloadImage(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

// Add GPS data to image
function addGPS(imageBuffer, lat, lon, name, date) {
  const base64 = imageBuffer.toString('base64');
  const dataUrl = 'data:image/jpeg;base64,' + base64;
  
  const latDms = piexif.GPSHelper.degToDms(lat);
  const lonDms = piexif.GPSHelper.degToDms(lon);
  
  const exifObj = {
    '0th': {
      Make: 'TestCamera',
      Model: 'GPS Test Model',
      ImageDescription: name
    },
    'Exif': {
      DateTimeOriginal: date
    },
    'GPS': {
      GPSLatitudeRef: lat >= 0 ? 'N' : 'S',
      GPSLatitude: latDms,
      GPSLongitudeRef: lon >= 0 ? 'E' : 'W',
      GPSLongitude: lonDms,
      GPSAltitude: [50, 1]
    }
  };
  
  const exifBytes = piexif.dump(exifObj);
  const newDataUrl = piexif.insert(exifBytes, dataUrl);
  const newBase64 = newDataUrl.split(',')[1];
  return Buffer.from(newBase64, 'base64');
}

async function main() {
  // Download a small test image (1x1 pixel JPEG)
  // Use a simple colored image from placeholder service
  const imageUrl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.jpg/320px-PNG_transparency_demonstration_1.jpg';
  
  console.log('Downloading base image...');
  const baseImage = await downloadImage(imageUrl);
  console.log('Base image downloaded:', baseImage.length, 'bytes');
  
  const downloadDir = path.join(process.env.USERPROFILE, 'Downloads');
  
  // Photo 1: Jinan
  const jinan = addGPS(baseImage, 36.639, 117.1425, 'Jinan Spring', '2026:09:10 10:00:00');
  const jinanPath = path.join(downloadDir, 'test_jinan_gps.jpg');
  fs.writeFileSync(jinanPath, jinan);
  console.log('Saved:', jinanPath, jinan.length, 'bytes');
  
  // Photo 2: Beijing
  const beijing = addGPS(baseImage, 39.9163, 116.3972, 'Beijing Forbidden City', '2026:09:08 14:30:00');
  const beijingPath = path.join(downloadDir, 'test_beijing_gps.jpg');
  fs.writeFileSync(beijingPath, beijing);
  console.log('Saved:', beijingPath, beijing.length, 'bytes');
  
  console.log('\n✅ Done! Two GPS test photos saved to your Downloads folder.');
  console.log('1. test_jinan_gps.jpg (36.639, 117.1425)');
  console.log('2. test_beijing_gps.jpg (39.9163, 116.3972)');
}

main().catch(console.error);
