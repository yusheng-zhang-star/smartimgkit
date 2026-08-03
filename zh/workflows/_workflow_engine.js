/**
 * SmartImgKit — Workflow Engine v2
 *
 * 一个工作流 = 一组"步骤"，每个步骤是一个工具的处理函数。
 * v2 新增：并发处理池（默认并发 3）、大图自动降采样、更好的进度显示
 *
 * 步骤对象结构：
 *   { id, label, description, runner: 'circleCrop' | 'filter' | 'watermark' | 'resize', options: {...} }
 *
 * runner 必须挂载到 window.SmartImgKit.runners[runnerName]，签名：
 *   async function (blob, options, log) => { return newBlob; }
 */
(function () {
  'use strict';

  const SmartImgKit = (window.SmartImgKit = window.SmartImgKit || {});
  SmartImgKit.runners = SmartImgKit.runners || {};

  // -------- 配置 --------
  const CONFIG = {
    CONCURRENCY: 3,        // 并发处理文件数
    MAX_IMAGE_PX: 4096,   // 超过这个尺寸自动降采样
  };

  // -------- 公共工具：file/blob 互转 --------
  SmartImgKit.blobToDataURL = function (blob) {
    return new Promise((resolve, reject) => {
      const r = new FileReader();
      r.onload = e => resolve(e.target.result);
      r.onerror = reject;
      r.readAsDataURL(blob);
    });
  };

  SmartImgKit.dataURLToBlob = function (dataURL) {
    const [meta, b64] = dataURL.split(',');
    const mime = (meta.match(/data:(.*?);/) || [])[1] || 'image/png';
    const bin = atob(b64);
    const u8 = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
    return new Blob([u8], { type: mime });
  };

  SmartImgKit.loadImage = function (blob) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = URL.createObjectURL(blob);
    });
  };

  // -------- 大图自动降采样（防止超大图卡死） --------
  SmartImgKit.downscaleIfNeeded = async function (blob, maxPx = CONFIG.MAX_IMAGE_PX) {
    if (!blob || !blob.type.startsWith('image/')) return blob;
    const img = await SmartImgKit.loadImage(blob);
    const maxDim = Math.max(img.naturalWidth, img.naturalHeight);
    if (maxDim <= maxPx) return blob;
    const scale = maxPx / maxDim;
    const w = Math.round(img.naturalWidth * scale);
    const h = Math.round(img.naturalHeight * scale);
    const canvas = document.createElement('canvas');
    canvas.width = w; canvas.height = h;
    canvas.getContext('2d').drawImage(img, 0, 0, w, h);
    return new Promise(resolve => canvas.toBlob(b => resolve(b), blob.type || 'image/jpeg', 0.92));
  };

  // -------- 并发控制：Promise 池 --------
  async function runInParallel(items, concurrency, processor, onItemDone) {
    const results = new Array(items.length);
    let nextIdx = 0;
    let doneCount = 0;

    async function worker() {
      while (nextIdx < items.length) {
        const idx = nextIdx++;
        try {
          results[idx] = await processor(items[idx], idx);
        } catch (e) {
          results[idx] = { error: e, item: items[idx] };
        }
        doneCount++;
        onItemDone && onItemDone(doneCount, items.length);
      }
    }

    const workers = [];
    for (let i = 0; i < Math.min(concurrency, items.length); i++) {
      workers.push(worker());
    }
    await Promise.all(workers);
    return results;
  }

  // -------- 进度 UI --------
  function ensureProgressBar() {
    let bar = document.getElementById('wfProgBar');
    if (bar) return { bar, fill: bar.querySelector('.progress-fill'), text: document.getElementById('wfProgText') };
    bar = document.createElement('div');
    bar.id = 'wfProgBar';
    bar.className = 'progress-bar';
    bar.style.display = 'none';
    bar.innerHTML = '<div class="progress-fill" style="width:0%"></div><div id="wfProgText" class="progress-text"></div>';
    document.body.appendChild(bar);
    return { bar, fill: bar.querySelector('.progress-fill'), text: document.getElementById('wfProgText') };
  }

  // -------- runPipeline: 跑一组文件 × 一组步骤（v2 并发版） --------
  /**
   * @param {File[]} files
   * @param {Array} steps
   * @param {Object} hooks  { onStepStart, onFileStart, onProgress(p), onDone(results) }
   * @param {Object} options  { concurrency: 3 }
   * @returns {Promise<Array<{name,blob}>>}
   */
  SmartImgKit.runPipeline = async function (files, steps, hooks = {}, options = {}) {
    if (!files || !files.length) throw new Error('No files provided');
    if (!steps || !steps.length) throw new Error('No steps provided');

    const concurrency = options.concurrency || CONFIG.CONCURRENCY;
    const { bar, fill, text } = ensureProgressBar();
    bar.style.display = 'block';

    const totalFiles = files.length;
    const totalSteps = steps.length;
    let doneFiles = 0;

    text.textContent = `Starting ${totalFiles} file(s) × ${totalSteps} step(s) with ${concurrency} workers...`;

    async function processSingleFile(file, fi) {
      hooks.onFileStart && hooks.onFileStart(file, fi, totalFiles);
      // 大图预处理
      let cur = await SmartImgKit.downscaleIfNeeded(file);

      for (let si = 0; si < totalSteps; si++) {
        const step = steps[si];
        hooks.onStepStart && hooks.onStepStart(step, si, totalSteps);
        text.textContent = `[${fi + 1}/${totalFiles}] ${file.name} → ${step.label} (${doneFiles + 1}/${totalFiles} done)`;
        const runner = SmartImgKit.runners[step.runner];
        if (!runner) throw new Error('Unknown runner: ' + step.runner);
        const log = msg => { text.textContent = `[${fi + 1}/${totalFiles}] ${file.name} → ${step.label}: ${msg}`; };
        cur = await runner(cur, step.options || {}, log);
      }

      const dot = file.name.lastIndexOf('.');
      const base = dot > -1 ? file.name.slice(0, dot) : file.name;
      return { name: base + '.png', blob: cur };
    }

    const results = await runInParallel(
      files,
      concurrency,
      processSingleFile,
      (done, total) => {
        doneFiles = done;
        const pct = Math.round((done / total) * 100);
        fill.style.width = pct + '%';
        hooks.onProgress && hooks.onProgress(pct);
      }
    );

    // 过滤错误
    const okResults = results.filter(r => r && !r.error);
    const errors = results.filter(r => r && r.error);

    if (errors.length) {
      text.textContent = `Done! ${okResults.length} OK, ${errors.length} failed.`;
      console.warn('[Workflow] Errors:', errors);
    } else {
      text.textContent = `Done! ${okResults.length} image(s) processed.`;
    }

    return okResults;
  };

  // -------- 可靠下载触发辅助函数 --------
  SmartImgKit._triggerDownload = function (blob, filename) {
    if (!filename.includes('.')) filename += '.zip';
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.setAttribute('download', filename);
    a.style.display = 'none';
    document.body.appendChild(a);
    const evt = new MouseEvent('click', { view: window, bubbles: true, cancelable: true });
    a.dispatchEvent(evt);
    setTimeout(() => {
      URL.revokeObjectURL(url);
      if (a.parentNode) a.parentNode.removeChild(a);
    }, 4000);
  };

  // -------- ZIP 批量下载（独立可复用） --------
  SmartImgKit.downloadZip = async function (items, zipName = 'output.zip', onProgress) {
    if (typeof JSZip === 'undefined') throw new Error('JSZip is not loaded');
    const zip = new JSZip();
    items.forEach(it => zip.file(it.name, it.blob));
    const blob = await zip.generateAsync({ type: 'blob' }, meta => {
      onProgress && onProgress(meta.percent | 0);
    });
    SmartImgKit._triggerDownload(blob, zipName);
    return blob;
  };

  // -------- runFlow (UI 级封装): 文件 → 跑步骤 → ZIP --------
  SmartImgKit.runFlow = async function (config) {
    // config: { files, steps, zipName }
    const { files, steps, zipName } = config;
    const results = await SmartImgKit.runPipeline(files, steps, {
      onProgress: p => {
        const evt = new CustomEvent('wf:progress', { detail: { p } });
        document.dispatchEvent(evt);
      }
    });
    await SmartImgKit.downloadZip(results, zipName);
    const evt = new CustomEvent('wf:done', { detail: { count: results.length } });
    document.dispatchEvent(evt);
  };

  console.log('[SmartImgKit] Workflow Engine v1 loaded');
})();
