// Cloudflare Pages Function: /api/info?url=IMAGE_URL
// Returns image metadata as JSON
export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const imageUrl = url.searchParams.get('url');

  if (!imageUrl) {
    return new Response(JSON.stringify({ error: 'Missing url parameter', ok: false }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }

  try {
    const resp = await fetch(imageUrl, { redirect: 'follow' });
    if (!resp.ok) throw new Error('Fetch failed: ' + resp.status);

    const contentType = resp.headers.get('content-type') || '';
    const contentLength = resp.headers.get('content-length');

    // Read first 32KB to parse image header
    const buf = new Uint8Array(await resp.arrayBuffer());
    const size = buf.byteLength;

    let width = 0, height = 0, type = contentType;

    // Parse PNG
    if (buf[0] === 0x89 && buf[1] === 0x50) {
      width = new DataView(buf.buffer).getUint32(16, false);
      height = new DataView(buf.buffer).getUint32(20, false);
      type = 'image/png';
    }
    // Parse JPEG
    else if (buf[0] === 0xFF && buf[1] === 0xD8) {
      let i = 2;
      while (i < buf.length) {
        if (buf[i] !== 0xFF) { i++; continue; }
        const marker = buf[i+1];
        if (marker >= 0xC0 && marker <= 0xC3) {
          height = new DataView(buf.buffer).getUint16(i+5, false);
          width = new DataView(buf.buffer).getUint16(i+7, false);
          break;
        }
        const len = new DataView(buf.buffer).getUint16(i+2, false);
        i += 2 + len;
      }
      type = 'image/jpeg';
    }
    // Parse GIF
    else if (buf[0] === 0x47 && buf[1] === 0x49) {
      width = new DataView(buf.buffer).getUint16(6, true);
      height = new DataView(buf.buffer).getUint16(8, true);
      type = 'image/gif';
    }
    // Parse WebP (VP8)
    else if (buf[0] === 0x52 && buf[1] === 0x49) {
      width = new DataView(buf.buffer).getUint16(26, true);
      height = new DataView(buf.buffer).getUint16(28, true);
      type = 'image/webp';
    }

    return new Response(JSON.stringify({
      width, height, type,
      size: contentLength ? parseInt(contentLength) : size,
      ok: true
    }), {
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message, ok: false }), {
      status: 502,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
    });
  }
}
