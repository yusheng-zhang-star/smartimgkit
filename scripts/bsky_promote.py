#!/usr/bin/env python3
"""Post a Bluesky post promoting smartimgkit.com, with an optional screenshot."""
import requests
import json
import sys
import os
from datetime import datetime, timezone

HANDLE = "gpzys.bsky.social"
APP_PASSWORD = "ksco-atpz-xfi3-57ps"
SITE_ROOT = r"E:\网站项目\smartimgkit"

# Rotating promotion slots: (url_path, screenshot_file, promo_text, hashtags)
SLOTS = [
    ("/tools/background-remover", "background-remover.png",
     "Remove image backgrounds 100% in your browser — no upload, no sign-up, free. Privacy-first AI:",
     "#privacy #AI"),
    ("/tools/image-compressor", "compressor.png",
     "Compress images up to 90% smaller right in your browser — no upload, free:",
     "#webdev #performance"),
    ("/tools/image-converter", "converter.png",
     "Convert images to WebP/AVIF/PNG/JPG instantly in your browser — free, no upload:",
     "#webdev #images"),
    ("/tools/image-resizer", "resizer.png",
     "Resize images in batch, right in your browser. No upload, free, no sign-up:",
     "#design #productivity"),
    ("/tools/image-cropper", "cropper.png",
     "Crop images to any size or aspect ratio in your browser. Free, no upload:",
     "#design #editing"),
    ("/tools/pdf-to-image", "pdf-to-image.png",
     "Convert PDF pages to images in your browser — no upload, free:",
     "#productivity #pdf"),
    ("/tools/gif-editor", "gif-editor.png",
     "Create and edit GIFs in your browser — no upload, free, no sign-up:",
     "#gif #creator"),
    ("/tools/heic-converter", "heic-converter.png",
     "Convert iPhone HEIC photos to JPG/PNG in your browser — free, no upload:",
     "#iphone #photography"),
    ("/tools/qr-code-generator", "qr-code-generator.png",
     "Generate QR codes for free in your browser — no sign-up, no tracking:",
     "#marketing #qr"),
    ("/tools/image-upscaler", "image-upscaler.png",
     "Upscale images 4x with AI in your browser — no upload, free:",
     "#AI #photography"),
    ("/tools/image-merger", "image-merger.png",
     "Merge multiple images into one in your browser — free, no upload:",
     "#design #productivity"),
    ("/tools/watermark", "watermark.png",
     "Add watermarks to images in your browser — batch, free, no upload:",
     "#copyright #design"),
]

def main():
    # Pick slot based on day of year so it rotates automatically
    day_of_year = datetime.now().timetuple().tm_yday
    slot = SLOTS[day_of_year % len(SLOTS)]
    url_path, img_file, text, hashtags = slot
    full_url = f"https://smartimgkit.com{url_path}"
    post_text = f"{text} {full_url} {hashtags}"

    # Login
    r = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": HANDLE, "password": APP_PASSWORD},
        timeout=30,
    )
    r.raise_for_status()
    session = r.json()
    token = session["accessJwt"]
    did = session["did"]
    print(f"Logged in as {did}")

    # Upload image
    img_path = os.path.join(SITE_ROOT, "screenshots", img_file)
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    print(f"Uploading {img_file} ({len(img_bytes)} bytes)...")

    r = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
        headers={"Authorization": f"Bearer {token}"},
        data=img_bytes,
        timeout=60,
    )
    r.raise_for_status()
    blob = r.json()["blob"]
    print(f"Blob uploaded: {blob['ref']['$link']}")

    # Create post
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    record = {
        "$type": "app.bsky.feed.post",
        "text": post_text,
        "createdAt": now,
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [{
                "image": blob,
                "alt": f"SmartImgKit free online tool - {url_path.strip('/')}",
            }],
        },
    }
    body = {"repo": did, "collection": "app.bsky.feed.post", "record": record}

    r = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=30,
    )
    r.raise_for_status()
    result = r.json()
    print(f"Posted! URI: {result['uri']}")
    print(f"Promoted: {full_url}")

if __name__ == "__main__":
    main()
