const piexif = require('piexifjs');
const fs = require('fs');
const path = require('path');

// Minimal 1x1 white JPEG (base64)
const MINIMAL_JPEG_BASE64 = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q==';

function degToDms(deg) {
  const d = Math.floor(deg);
  const mFloat = (deg - d) * 60;
  const m = Math.floor(mFloat);
  const s = (mFloat - m) * 60;
  return [[d, 1], [m, 1], [Math.round(s * 10000), 10000]];
}

function addGPS(base64Image, lat, lon, name, date) {
  const dataUrl = 'data:image/jpeg;base64,' + base64Image;
  
  const latDms = degToDms(Math.abs(lat));
  const lonDms = degToDms(Math.abs(lon));
  
  const exifObj = {
    'GPS': {
      GPSLatitudeRef: lat >= 0 ? 'N' : 'S',
      GPSLatitude: latDms,
      GPSLongitudeRef: lon >= 0 ? 'E' : 'W',
      GPSLongitude: lonDms
    }
  };
  
  const exifBytes = piexif.dump(exifObj);
  const newDataUrl = piexif.insert(exifBytes, dataUrl);
  const newBase64 = newDataUrl.split(',')[1];
  return Buffer.from(newBase64, 'base64');
}

function main() {
  const downloadDir = path.join(process.env.USERPROFILE, 'Downloads');
  
  // Photo 1: Jinan
  const jinan = addGPS(MINIMAL_JPEG_BASE64, 36.639, 117.1425, 'Jinan Spring', '2026:09:10 10:00:00');
  const jinanPath = path.join(downloadDir, 'test_jinan_gps.jpg');
  fs.writeFileSync(jinanPath, jinan);
  console.log('Saved:', jinanPath, jinan.length, 'bytes');
  
  // Photo 2: Beijing
  const beijing = addGPS(MINIMAL_JPEG_BASE64, 39.9163, 116.3972, 'Beijing Forbidden City', '2026:09:08 14:30:00');
  const beijingPath = path.join(downloadDir, 'test_beijing_gps.jpg');
  fs.writeFileSync(beijingPath, beijing);
  console.log('Saved:', beijingPath, beijing.length, 'bytes');
  
  console.log('\n✅ Done! Two GPS test photos saved to your Downloads folder.');
  console.log('1. test_jinan_gps.jpg (36.639, 117.1425)');
  console.log('2. test_beijing_gps.jpg (39.9163, 116.3972)');
}

main();
