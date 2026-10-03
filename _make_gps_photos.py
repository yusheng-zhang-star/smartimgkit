import sys
import os
sys.path.insert(0, os.path.expanduser('~') + '/AppData/Roaming/Python/Python312/site-packages')

import piexif

# Minimal 1x1 white JPEG (base64)
import base64
MINIMAL_JPEG_BASE64 = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigD//2Q=='

def deg_to_dms(value):
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes/60) * 3600
    return ((degrees, 1), (minutes, 1), (int(seconds * 10000), 10000))

def add_gps(image_bytes, lat, lon):
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
    return piexif.insert(exif_bytes, image_bytes)

# Main
download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
base_image = base64.b64decode(MINIMAL_JPEG_BASE64)

# Photo 1: Jinan
jinan = add_gps(base_image, 36.639, 117.1425)
jinan_path = os.path.join(download_dir, 'test_jinan_gps.jpg')
with open(jinan_path, 'wb') as f:
    f.write(jinan)
print(f'Saved: {jinan_path} ({len(jinan)} bytes)')

# Photo 2: Beijing
beijing = add_gps(base_image, 39.9163, 116.3972)
beijing_path = os.path.join(download_dir, 'test_beijing_gps.jpg')
with open(beijing_path, 'wb') as f:
    f.write(beijing)
print(f'Saved: {beijing_path} ({len(beijing)} bytes)')

print('\n✅ Done! Two GPS test photos saved to your Downloads folder.')
print('1. test_jinan_gps.jpg (36.639, 117.1425)')
print('2. test_beijing_gps.jpg (39.9163, 116.3972)')
