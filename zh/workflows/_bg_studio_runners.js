/**
 * SmartImgKit — AI Background Studio Runners v1
 *
 * 3 个 runner：removeBg / addBorder / addShadow
 * 每个 runner: async (blob, options, log) => newBlob
 *
 * 去背景算法：四角采样 → 判定主背景色 → 容差泛洪填充 → 透明化
 */
(function () {
  'use strict';
  const KIT = (window.SmartImgKit = window.SmartImgKit || {});
  const runners = (KIT.runners = KIT.runners || {});

  // -------- 工具函数：从 ImageData 获取某点颜色 --------
  function getColor(data, w, x, y) {
    const i = (y * w + x) * 4;
    return [data[i], data[i + 1], data[i + 2], data[i + 3]];
  }

  // -------- 工具函数：颜色距离（欧氏） --------
  function colorDist(c1, c2) {
    const dr = c1[0] - c2[0], dg = c1[1] - c2[1], db = c1[2] - c2[2];
    return Math.sqrt(dr * dr + dg * dg + db * db);
  }

  // -------- 1. removeBg --------
  // options: { tolerance=30, bgColor=null(自动)|'#rrggbb' }
  // 算法：采样四角判定背景色 → 遍历所有像素，与背景色距离<tolerance 的变透明
  runners.removeBg = async function (blob, opt = {}, log) {
    const tol = opt.tolerance || 30;
    log('removing background (tolerance=' + tol + ')');

    const img = await KIT.loadImage(blob);
    const W = img.width, H = img.height;

    // 创建临时 canvas 读取像素
    const srcC = document.createElement('canvas');
    srcC.width = W; srcC.height = H;
    const srcCtx = srcC.getContext('2d');
    srcCtx.drawImage(img, 0, 0);
    const imageData = srcCtx.getImageData(0, 0, W, H);
    const d = imageData.data;

    // 判定背景色：采样四角（取最常见或平均）
    let bgColors = [];
    const samplePoints = [[0, 0], [W - 1, 0], [0, H - 1], [W - 1, H - 1]];
    // 多采样几个边缘点提高准确度
    for (let s = 0; s < Math.floor(W / 10); s++) {
      samplePoints.push([s, 0], [W - 1 - s, 0], [0, s], [0, H - 1 - s]);
    }
    for (const [sx, sy] of samplePoints) {
      if (sx >= 0 && sx < W && sy >= 0 && sy < H) {
        bgColors.push(getColor(d, W, sx, sy));
      }
    }

    // 使用用户指定背景色或自动检测
    let bgColor;
    if (opt.bgColor && opt.bgColor !== 'auto') {
      // 解析 hex
      const hex = opt.bgColor.replace('#', '');
      bgColor = [
        parseInt(hex.slice(0, 2), 16),
        parseInt(hex.slice(2, 4), 16),
        parseInt(hex.slice(4, 6), 16),
        255
      ];
    } else {
      // 取出现最多的角落色簇中心
      const clusters = [];
      for (const c of bgColors) {
        let matched = false;
        for (const cl of clusters) {
          if (colorDist(c, cl.avg) < 20) {
            cl.count++;
            cl.sumR += c[0]; cl.sumG += c[1]; cl.sumB += c[2];
            cl.avg = [cl.sumR / cl.count, cl.sumG / cl.count, cl.sumB / cl.count, 255];
            matched = true;
            break;
          }
        }
        if (!matched) {
          clusters.push({ count: 1, sumR: c[0], sumG: c[1], sumB: c[2], avg: [...c] });
        }
      }
      clusters.sort((a, b) => b.count - a.count);
      bgColor = clusters.length > 0 ? clusters[0].avg : [255, 255, 255, 255];
    }

    log('detected bg color: rgb(' + bgColor.slice(0,3).join(',') + ')');

    // 遍历像素：接近背景色的变透明
    const tolSq = tol * tol;
    let removed = 0;
    for (let i = 0; i < d.length; i += 4) {
      const dr = d[i] - bgColor[0];
      const dg = d[i + 1] - bgColor[1];
      const db = d[i + 2] - bgColor[2];
      const distSq = dr * dr + dg * dg + db * db;
      if (distSq <= tolSq) {
        d[i + 3] = 0;
        removed++;
      }
    }

    log('made transparent: ' + removed + ' pixels (' + Math.round(removed / (W * H) * 100) + '%)');

    // 写回并导出
    srcCtx.putImageData(imageData, 0, 0);

    return new Promise(resolve => srcC.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // -------- 2. addBorder --------
  // options: { color='#ffffff', size=20, radius=0(方角)|>0(圆角) }
  runners.addBorder = async function (blob, opt = {}, log) {
    const color = opt.color || '#ffffff';
    const size = opt.size || 20;
    const radius = opt.radius || 0;
    log('adding border: ' + size + 'px ' + color + (radius ? ' rounded' : ''));

    const img = await KIT.loadImage(blob);
    const W = img.width, H = img.height;
    const pad = size;
    const outW = W + pad * 2;
    const outH = H + pad * 2;

    const c = document.createElement('canvas');
    c.width = outW; c.height = outH;
    const ctx = c.getContext('2d');

    // 绘制圆角矩形背景（边框色）
    if (radius > 0) {
      const r = Math.min(radius, Math.min(outW, outH) / 2);
      ctx.beginPath();
      ctx.moveTo(r, 0);
      ctx.lineTo(outW - r, 0);
      ctx.quadraticCurveTo(outW, 0, outW, r);
      ctx.lineTo(outW, outH - r);
      ctx.quadraticCurveTo(outW, outH, outW - r, outH);
      ctx.lineTo(r, outH);
      ctx.quadraticCurveTo(0, outH, 0, outH - r);
      ctx.lineTo(0, r);
      ctx.quadraticCurveTo(0, 0, r, 0);
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
      ctx.clip();
    } else {
      ctx.fillStyle = color;
      ctx.fillRect(0, 0, outW, outH);
    }

    // 绘制原图居中
    ctx.drawImage(img, pad, pad, W, H);

    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  // -------- 3. addShadow --------
  // options: { blur=15, offsetX=8, offsetY=8, color='rgba(0,0,0,0.35)', bg='#ffffff'|null }
  // 注意：阴影需要一个不透明的背景来显示效果
  runners.addShadow = async function (blob, opt = {}, log) {
    const blur = opt.blur || 15;
    const ox = opt.offsetX !== undefined ? opt.offsetX : 8;
    const oy = opt.offsetY !== undefined ? opt.offsetY : 8;
    const shadowColor = opt.shadowColor || 'rgba(0,0,0,0.35)';
    const bgColor = opt.bg || '#ffffff';

    log('adding shadow: blur=' + blur + ' offset=(' + ox + ',' + oy + ')');

    const img = await KIT.loadImage(blob);
    const W = img.width, H = img.height;
    // 扩展 canvas 以容纳阴影和偏移
    const ext = blur + Math.max(Math.abs(ox), Math.abs(oy)) + 20;
    const outW = W + ext * 2;
    const outH = H + ext * 2;

    const c = document.createElement('canvas');
    c.width = outW; c.height = outH;
    const ctx = c.getContext('2d');

    // 填充背景
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, outW, outH);

    // 配置阴影
    ctx.shadowColor = shadowColor;
    ctx.shadowBlur = blur;
    ctx.shadowOffsetX = ox;
    ctx.shadowOffsetY = oy;

    // 绘制图片（带阴影）
    ctx.drawImage(img, ext, ext, W, H);

    return new Promise(resolve => c.toBlob(b => resolve(b), 'image/jpeg', 0.92));
  };

  console.log('[SmartImgKit] AI Background Studio runners loaded');
})();
