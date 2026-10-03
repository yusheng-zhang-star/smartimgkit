from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
output_dir = r"E:\网站项目\smartimgkit\poster_previews"
os.makedirs(output_dir, exist_ok=True)

W, H = 2000, 3000

# Sample data
photos = [
    {"name": "Jinan Spring", "lat": 36.639, "lon": 117.1425, "color": (70, 130, 180)},
    {"name": "Beijing Forbidden City", "lat": 39.9163, "lon": 116.3972, "color": (205, 133, 63)},
    {"name": "Shanghai Bund", "lat": 31.2397, "lon": 121.4900, "color": (46, 139, 87)},
    {"name": "Guangzhou Canton Tower", "lat": 23.1066, "lon": 113.3245, "color": (220, 20, 60)},
]

styles = {
    "minimal": {
        "bg": (255, 255, 255),
        "text": (26, 26, 26),
        "subtext": (102, 102, 102),
        "accent": (99, 102, 241),
        "border": (224, 224, 224),
        "map_bg": (240, 240, 240),
    },
    "vintage": {
        "bg": (245, 230, 200),
        "text": (92, 64, 51),
        "subtext": (139, 115, 85),
        "accent": (139, 69, 19),
        "border": (201, 168, 108),
        "map_bg": (230, 215, 185),
    },
    "dark": {
        "bg": (15, 15, 26),
        "text": (255, 255, 255),
        "subtext": (156, 163, 175),
        "accent": (129, 140, 248),
        "border": (55, 65, 81),
        "map_bg": (26, 26, 46),
    },
}

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def draw_map_background(draw, x, y, w, h, style):
    # Draw map background
    draw.rectangle([x, y, x+w, y+h], fill=style["map_bg"])
    
    # Draw simple grid lines to simulate map
    grid_color = tuple(max(0, c-20) for c in style["map_bg"])
    for i in range(0, w, 80):
        draw.line([(x+i, y), (x+i, y+h)], fill=grid_color, width=1)
    for i in range(0, h, 80):
        draw.line([(x, y+i), (x+w, y+i)], fill=grid_color, width=1)
    
    # Draw some "roads"
    road_color = tuple(min(255, c+30) for c in style["map_bg"])
    draw.line([(x+100, y+200), (x+w-100, y+200)], fill=road_color, width=8)
    draw.line([(x+300, y+100), (x+300, y+h-100)], fill=road_color, width=6)
    draw.line([(x+600, y+300), (x+w-200, y+h-200)], fill=road_color, width=5)

def draw_photo_marker(draw, x, y, color, number, name, coords, style):
    radius = 85
    
    # Shadow
    draw.ellipse([x-radius+5, y-radius+10, x+radius+5, y+radius+10], fill=(0,0,0,60))
    
    # Photo circle (colored placeholder with gradient effect)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Add a simple "photo" pattern
    for i in range(0, radius*2, 20):
        draw.line([(x-radius+i, y-radius), (x-radius+i+10, y+radius)], fill=tuple(min(255,c+20) for c in color), width=1)
    
    # White border (thicker)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline=(255,255,255), width=7)
    
    # Number badge (larger)
    badge_r = 30
    bx, by = x + radius - 5, y - radius + 5
    draw.ellipse([bx-badge_r, by-badge_r, bx+badge_r, by+badge_r], fill=style["accent"])
    draw.ellipse([bx-badge_r, by-badge_r, bx+badge_r, by+badge_r], outline=(255,255,255), width=3)
    font = get_font(32, bold=True)
    bbox = draw.textbbox((0,0), str(number), font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((bx-tw//2, by-th//2-2), str(number), fill=(255,255,255), font=font)
    
    # Location name label
    label_y = y + radius + 35
    name_font = get_font(26, bold=True)
    bbox = draw.textbbox((0,0), name, font=name_font)
    nw = bbox[2]-bbox[0]
    draw.text((x - nw//2, label_y), name, fill=style["text"], font=name_font)
    
    # Coordinates
    coord_font = get_font(20)
    bbox = draw.textbbox((0,0), coords, font=coord_font)
    cw = bbox[2]-bbox[0]
    draw.text((x - cw//2, label_y + 32), coords, fill=style["subtext"], font=coord_font)

def generate_poster(style_name, style):
    img = Image.new("RGB", (W, H), style["bg"])
    draw = ImageDraw.Draw(img)
    
    # Decorative border
    draw.rectangle([60, 60, W-60, H-60], outline=style["border"], width=4)
    draw.rectangle([80, 80, W-80, H-80], outline=style["border"], width=1)
    
    # Title
    title_font = get_font(72, bold=True)
    title = "My Photo Map Journey"
    bbox = draw.textbbox((0,0), title, font=title_font)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 200), title, fill=style["text"], font=title_font)
    
    # Subtitle
    sub_font = get_font(32)
    subtitle = "Sep 2, 2026 — Sep 10, 2026"
    bbox = draw.textbbox((0,0), subtitle, font=sub_font)
    tw = bbox[2]-bbox[0]
    draw.text(((W-tw)//2, 290), subtitle, fill=style["subtext"], font=sub_font)
    
    # Accent line
    draw.line([(W//2-100, 340), (W//2+100, 340)], fill=style["accent"], width=3)
    
    # Map area
    mapX, mapY = 120, 360
    mapW, mapH = W-240, 1700
    draw_map_background(draw, mapX, mapY, mapW, mapH, style)
    
    # Map border
    draw.rectangle([mapX, mapY, mapX+mapW, mapY+mapH], outline=style["border"], width=3)
    
    # Calculate marker positions
    lats = [p["lat"] for p in photos]
    lons = [p["lon"] for p in photos]
    minLat, maxLat = min(lats), max(lats)
    minLon, maxLon = min(lons), max(lons)
    latPad = (maxLat - minLat) * 0.15 + 0.5
    lonPad = (maxLon - minLon) * 0.15 + 0.5
    minLat -= latPad
    maxLat += latPad
    minLon -= lonPad
    maxLon += lonPad
    
    # Draw markers
    for i, photo in enumerate(photos):
        mx = mapX + ((photo["lon"] - minLon) / (maxLon - minLon)) * mapW
        my = mapY + ((maxLat - photo["lat"]) / (maxLat - minLat)) * mapH
        name = photo["name"].replace(" Forbidden City", "").replace(" Canton Tower", "").replace(" Spring", "").replace(" Bund", "")
        coords = f"{photo['lat']:.2f}°, {photo['lon']:.2f}°"
        draw_photo_marker(draw, int(mx), int(my), photo["color"], i+1, name, coords, style)
    
    # Stats section
    statsY = mapY + mapH + 100
    stats = [
        ("4", "Photos"),
        ("4", "Locations"),
        ("1,847", "KM Traveled"),
        ("2026", "Year"),
    ]
    
    statWidth = (W - 300) // 4
    stat_font = get_font(64, bold=True)
    label_font = get_font(24)
    
    for i, (value, label) in enumerate(stats):
        sx = 150 + i * statWidth + statWidth // 2
        bbox = draw.textbbox((0,0), value, font=stat_font)
        vw = bbox[2]-bbox[0]
        draw.text((sx - vw//2, statsY), value, fill=style["accent"], font=stat_font)
        
        bbox = draw.textbbox((0,0), label.upper(), font=label_font)
        lw = bbox[2]-bbox[0]
        draw.text((sx - lw//2, statsY + 80), label.upper(), fill=style["subtext"], font=label_font)
    
    # Footer
    footer_font = get_font(24)
    footer1 = "Created with SmartImgKit Photo Location Map"
    bbox = draw.textbbox((0,0), footer1, font=footer_font)
    fw = bbox[2]-bbox[0]
    draw.text(((W-fw)//2, H-160), footer1, fill=style["subtext"], font=footer_font)
    
    footer_font2 = get_font(28, bold=True)
    footer2 = "smartimgkit.com"
    bbox = draw.textbbox((0,0), footer2, font=footer_font2)
    fw = bbox[2]-bbox[0]
    draw.text(((W-fw)//2, H-115), footer2, fill=style["accent"], font=footer_font2)
    
    # Save
    output_path = os.path.join(output_dir, f"poster_{style_name}.png")
    img.save(output_path, "PNG", quality=95)
    print(f"Generated: {output_path} ({os.path.getsize(output_path)} bytes)")
    return output_path

# Generate all 3 styles
for style_name, style in styles.items():
    generate_poster(style_name, style)

print("\nAll posters generated!")
