from PIL import Image, ImageDraw, ImageFont
import os

output_dir = r"E:\网站项目\smartimgkit\poster_previews"
os.makedirs(output_dir, exist_ok=True)

W, H = 2000, 3000

photos = [
    {"name": "Jinan Spring", "lat": 36.639, "lon": 117.1425, "color": (70, 130, 180), "date": "2026-09-10"},
    {"name": "Beijing Forbidden City", "lat": 39.9163, "lon": 116.3972, "color": (205, 133, 63), "date": "2026-09-08"},
    {"name": "Shanghai Bund", "lat": 31.2397, "lon": 121.4900, "color": (46, 139, 87), "date": "2026-09-05"},
    {"name": "Guangzhou Canton Tower", "lat": 23.1066, "lon": 113.3245, "color": (220, 20, 60), "date": "2026-09-02"},
]

styles = {
    "minimal": {"bg": (255,255,255), "text": (26,26,26), "subtext": (102,102,102), "accent": (99,102,241), "border": (224,224,224), "map_bg": (232,232,232)},
    "vintage": {"bg": (245,230,200), "text": (92,64,51), "subtext": (139,115,85), "accent": (139,69,19), "border": (201,168,108), "map_bg": (230,215,185)},
    "dark": {"bg": (15,15,26), "text": (255,255,255), "subtext": (156,163,175), "accent": (129,140,248), "border": (55,65,81), "map_bg": (26,26,46)},
}

def get_font(size, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except:
        return ImageFont.load_default()

def draw_map_bg(draw, x, y, w, h, style):
    draw.rectangle([x, y, x+w, y+h], fill=style["map_bg"])
    grid = tuple(max(0,c-15) for c in style["map_bg"])
    for i in range(0, w, 80):
        draw.line([(x+i, y), (x+i, y+h)], fill=grid, width=1)
    for i in range(0, h, 80):
        draw.line([(x, y+i), (x+w, y+i)], fill=grid, width=1)
    road = tuple(min(255,c+25) for c in style["map_bg"])
    draw.line([(x+100, y+300), (x+w-100, y+300)], fill=road, width=8)
    draw.line([(x+400, y+100), (x+400, y+h-100)], fill=road, width=6)
    draw.line([(x+700, y+500), (x+w-200, y+h-300)], fill=road, width=5)

def generate_poster(style_name, style):
    img = Image.new("RGB", (W, H), style["bg"])
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([60, 60, W-60, H-60], outline=style["border"], width=4)
    draw.rectangle([80, 80, W-80, H-80], outline=style["border"], width=1)
    
    # Title
    f = get_font(72, bold=True)
    title = "My Photo Map Journey"
    bbox = draw.textbbox((0,0), title, font=f)
    draw.text(((W-(bbox[2]-bbox[0]))//2, 180), title, fill=style["text"], font=f)
    
    # Subtitle
    f = get_font(32)
    sub = "Sep 2, 2026 — Sep 10, 2026"
    bbox = draw.textbbox((0,0), sub, font=f)
    draw.text(((W-(bbox[2]-bbox[0]))//2, 270), sub, fill=style["subtext"], font=f)
    
    # Accent line
    draw.line([(W//2-100, 310), (W//2+100, 310)], fill=style["accent"], width=3)
    
    # Map area
    mapX, mapY, mapW, mapH = 120, 350, W-240, 1400
    draw_map_bg(draw, mapX, mapY, mapW, mapH, style)
    draw.rectangle([mapX, mapY, mapX+mapW, mapY+mapH], outline=style["border"], width=3)
    
    # Marker positions
    lats = [p["lat"] for p in photos]
    lons = [p["lon"] for p in photos]
    minLat, maxLat = min(lats)-2, max(lats)+2
    minLon, maxLon = min(lons)-2, max(lons)+2
    positions = [(mapX + ((p["lon"]-minLon)/(maxLon-minLon))*mapW, mapY + ((maxLat-p["lat"])/(maxLat-minLat))*mapH) for p in photos]
    
    # Route lines
    if len(positions) > 1:
        draw.line([(positions[0][0], positions[0][1])] + [(p[0], p[1]) for p in positions[1:]], fill=style["accent"], width=4)
    
    # Markers
    for i, (p, pos) in enumerate(zip(photos, positions)):
        x, y = int(pos[0]), int(pos[1])
        r = 75
        # Shadow
        draw.ellipse([x-r+5, y-r+8, x+r+5, y+r+8], fill=(0,0,0,60))
        # White bg
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(255,255,255))
        # Photo color
        draw.ellipse([x-r+5, y-r+5, x+r-5, y+r-5], fill=p["color"])
        # Number badge
        br = 28
        bx, by = x+r-5, y-r+5
        draw.ellipse([bx-br, by-br, bx+br, by+br], fill=style["accent"], outline=(255,255,255), width=3)
        f = get_font(30, bold=True)
        bbox = draw.textbbox((0,0), str(i+1), font=f)
        draw.text((bx-(bbox[2]-bbox[0])//2, by-(bbox[3]-bbox[1])//2-2), str(i+1), fill=(255,255,255), font=f)
    
    # Photo list section
    listY = mapY + mapH + 60
    f = get_font(36, bold=True)
    draw.text((120, listY), "📸 Photo Journey", fill=style["text"], font=f)
    
    # Thumbnails
    thumbSize = 200
    gap = (W - 240 - len(photos)*thumbSize) // (len(photos) + 1)
    for i, p in enumerate(photos):
        tx = 120 + gap + i*(thumbSize+gap)
        ty = listY + 50
        
        # Number badge
        draw.ellipse([tx+1, ty+1, tx+49, ty+49], fill=style["accent"])
        f = get_font(24, bold=True)
        bbox = draw.textbbox((0,0), str(i+1), font=f)
        draw.text((tx+25-(bbox[2]-bbox[0])//2, ty+25-(bbox[3]-bbox[1])//2-2), str(i+1), fill=(255,255,255), font=f)
        
        # Thumbnail
        draw.rounded_rectangle([tx, ty, tx+thumbSize, ty+thumbSize], radius=12, fill=p["color"], outline=style["border"], width=2)
        
        # Name
        name = p["name"].replace(" Forbidden City","").replace(" Canton Tower","").replace(" Spring","").replace(" Bund","")
        f = get_font(20, bold=True)
        bbox = draw.textbbox((0,0), name, font=f)
        draw.text((tx+thumbSize//2-(bbox[2]-bbox[0])//2, ty+thumbSize+30), name, fill=style["text"], font=f)
        
        # Coords
        f = get_font(16)
        coords = f"{p['lat']:.2f}°, {p['lon']:.2f}°"
        bbox = draw.textbbox((0,0), coords, font=f)
        draw.text((tx+thumbSize//2-(bbox[2]-bbox[0])//2, ty+thumbSize+58), coords, fill=style["subtext"], font=f)
    
    # Stats
    statsY = listY + 380
    stats = [("4", "Photos"), ("4", "Locations"), ("1,847", "KM Traveled"), ("4", "Days")]
    statW = (W-300)//4
    for i, (val, label) in enumerate(stats):
        sx = 150 + i*statW + statW//2
        f = get_font(56, bold=True)
        bbox = draw.textbbox((0,0), val, font=f)
        draw.text((sx-(bbox[2]-bbox[0])//2, statsY), val, fill=style["accent"], font=f)
        f = get_font(22)
        bbox = draw.textbbox((0,0), label.upper(), font=f)
        draw.text((sx-(bbox[2]-bbox[0])//2, statsY+45), label.upper(), fill=style["subtext"], font=f)
    
    # Footer
    f = get_font(24)
    footer1 = "Created with SmartImgKit Photo Location Map"
    bbox = draw.textbbox((0,0), footer1, font=f)
    draw.text(((W-(bbox[2]-bbox[0]))//2, H-100), footer1, fill=style["subtext"], font=f)
    f = get_font(28, bold=True)
    footer2 = "smartimgkit.com"
    bbox = draw.textbbox((0,0), footer2, font=f)
    draw.text(((W-(bbox[2]-bbox[0]))//2, H-60), footer2, fill=style["accent"], font=f)
    
    path = os.path.join(output_dir, f"poster_{style_name}_v2.png")
    img.save(path, "PNG", quality=95)
    print(f"Generated: {path} ({os.path.getsize(path)} bytes)")

for name, style in styles.items():
    generate_poster(name, style)
print("\nDone!")
