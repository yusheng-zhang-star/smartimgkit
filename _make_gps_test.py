import sys
import os
sys.path.insert(0, os.path.expanduser('~') + '/AppData/Roaming/Python/Python312/site-packages')

from PIL import Image, ImageDraw
import piexif
import os

# Create a simple test image
img = Image.new('RGB', (800, 600), color=(70, 130, 180))
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 750, 550], outline=(255,255,255), width=3)
draw.text((300, 280), 'GPS Test Photo', fill=(255,255,255))

# GPS coordinates: Jinan, China
lat = 36.639
lon = 117.1425

def to_dms(value):
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes/60) * 3600
    return ((degrees, 1), (minutes, 1), (int(seconds * 10000), 10000))

lat_dms = to_dms(abs(lat))
lon_dms = to_dms(abs(lon))

exif_dict = {
    'GPS': {
        piexif.GPSIFD.GPSLatitudeRef: 'N',
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLongitudeRef: 'E',
        piexif.GPSIFD.GPSLongitude: lon_dms,
        piexif.GPSIFD.GPSAltitude: (100, 1),
    },
    'Exif': {
        piexif.ExifIFD.DateTimeOriginal: '2026:09:10 12:00:00',
    },
    '0th': {
        piexif.ImageIFD.Make: 'TestCamera',
        piexif.ImageIFD.Model: 'GPS Test Model',
    }
}

exif_bytes = piexif.dump(exif_dict)
output_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'gps_test_photo.jpg')
img.save(output_path, 'JPEG', exif=exif_bytes)
print(f'Test photo saved to: {output_path}')
print(f'GPS: {lat}, {lon} (Jinan, China)')
