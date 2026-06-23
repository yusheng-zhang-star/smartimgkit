/**
 * SmartImgKit — Workflow Engine v1
 *
 * 一个工作流 = 一组"步骤"，每个步骤是一个工具的处理函数。
 * 工作流页用 _workflow_template.html + _workflows_data.json 生成，
 * 该引擎在客户端读 window.WORKFLOW_CONFIG 并依次执行。
 *
 * 步骤对象结构（由 _workflows_data.json 注入到页面）：
 *   { id, label, description, runner: 'circleCrop' | 'filter' | 'watermark' | 'resize', options: {...} }
 *
 * runner 必须挂载到 window.SmartImgKit.runners[runnerName]，签名：
 *   async function (blob, options, log) => { return newBlob; }
 */
(function () {
  'use strict';

  const SmartImgKit = (window.SmartImgKit = window.SmartImgKit || {});

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

  // -------- runPipeline: 跑一组文件 × 一组步骤 --------
  /**
   * @param {File[]} files
   * @param {Array} steps
   * @param {Object} hooks  { onStepStart(step,i,total), onFileStart(file,i,total), onProgress(p), onDone(results) }
   * @returns {Promise<Array<{name,blob}>>}
   */
  SmartImgKit.runPipeline = async function (files, steps, hooks = {}) {
    if (!files || !files.length) throw new Error('No files provided');
    if (!steps || !steps.length) throw new Error('No steps provided');

    const { bar, fill, text } = ensureProgressBar();
    bar.style.display = 'block';
    const results = [];
    const totalUnits = files.length * steps.length;
    let doneUnits = 0;

    for (let fi = 0; fi < files.length; fi++) {
      const f = files[fi];
      hooks.onFileStart && hooks.onFileStart(f, fi, files.length);
      let cur = f;
      for (let si = 0; si < steps.length; si++) {
        const step = steps[si];
        hooks.onStepStart && hooks.onStepStart(step, si, steps.length);
        text.textContent = `[${fi + 1}/${files.length}] ${f.name} → ${step.label}`;
        const runner = SmartImgKit.runners[step.runner];
        if (!runner) throw new Error('Unknown runner: ' + step.runner);
        const log = msg => { text.textContent = `[${fi + 1}/${files.length}] ${f.name} → ${step.label}: ${msg}`; };
        cur = await runner(cur, step.options || {}, log);
        doneUnits++;
        const pct = Math.round((doneUnits / totalUnits) * 100);
        fill.style.width = pct + '%';
        hooks.onProgress && hooks.onProgress(pct);
      }
      // 输出文件名：保留原名
      const dot = f.name.lastIndexOf('.');
      const base = dot > -1 ? f.name.slice(0, dot) : f.name;
      results.push({ name: base + '.png', blob: cur });
    }
    text.textContent = `Done! ${results.length} image(s) processed.`;
    return results;
  };

  // -------- ZIP 批量下载（独立可复用） --------
  SmartImgKit.downloadZip = async function (items, zipName = 'output.zip', onProgress) {
    if (typeof JSZip === 'undefined') throw new Error('JSZip is not loaded');
    const zip = new JSZip();
    items.forEach(it => zip.file(it.name, it.blob));
    const blob = await zip.generateAsync({ type: 'blob' }, meta => {
      onProgress && onProgress(meta.percent | 0);
    });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = zipName;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
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
