import sys
import os
sys.path.insert(0, os.path.expanduser('~') + '/AppData/Roaming/Python/Python312/site-packages')

import piexif

def deg_to_dms(value):
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes/60) * 3600
    return ((degrees, 1), (minutes, 1), (int(seconds * 10000), 10000))

def add_gps(input_path, output_path, lat, lon):
    lat_dms = deg_to_dms(abs(lat))
    lon_dms = deg_to_dms(abs(lon))
    
    exif_dict = {
        'GPS': {
            piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
            piexif.GPSIFD.GPSLatitude: lat_dms,
            piexif.GPSIFD.GPSLongitudeRef: 'E' if lon >= 0 else 'W',
            piexif.GPSIFD.GPSLongitude: lon_dms,
        }
    }
    
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, input_path, output_path)

# Main
base_path = r'E:\网站项目\smartimgkit\test-image.jpg'
download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

print(f'Base image: {base_path}')

# Photo 1: Jinan
jinan_path = os.path.join(download_dir, 'test_jinan_gps.jpg')
add_gps(base_path, jinan_path, 36.639, 117.1425)
print(f'Saved: {jinan_path} ({os.path.getsize(jinan_path)} bytes)')

# Photo 2: Beijing
beijing_path = os.path.join(download_dir, 'test_beijing_gps.jpg')
add_gps(base_path, beijing_path, 39.9163, 116.3972)
print(f'Saved: {beijing_path} ({os.path.getsize(beijing_path)} bytes)')

print('\n✅ Done! Two GPS test photos saved to your Downloads folder.')
print('1. test_jinan_gps.jpg (36.639, 117.1425)')
print('2. test_beijing_gps.jpg (39.9163, 116.3972)')
