/**
 * Reliable download trigger helper.
 * Place in _workflow_engine.js and use everywhere.
 */
window.SmartImgKit = window.SmartImgKit || {};
SmartImgKit.triggerDownload = function (source, filename) {
  function guessExtFromMime(mime) {
    if (!mime) return '';
    var type = mime.toLowerCase();
    if (type === 'image/png') return '.png';
    if (type === 'image/jpeg' || type === 'image/jpg') return '.jpg';
    if (type === 'image/webp') return '.webp';
    if (type === 'image/gif') return '.gif';
    if (type === 'image/apng') return '.png';
    if (type === 'image/svg+xml') return '.svg';
    if (type === 'application/pdf') return '.pdf';
    if (type === 'text/plain') return '.txt';
    if (type === 'application/zip') return '.zip';
    if (type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return '.docx';
    if (type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') return '.xlsx';
    if (type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation') return '.pptx';
    return '';
  }

  function ensureExt(name, sourceObj) {
    if (/\.[A-Za-z0-9]{1,8}$/.test(name)) return name;
    var mime = sourceObj && sourceObj.type ? sourceObj.type : '';
    return name + (guessExtFromMime(mime) || '.zip');
  }

  var blob = source;
  if (typeof source === 'string') {
    if (source.indexOf('data:') === 0) {
      blob = SmartImgKit.dataURLToBlob ? SmartImgKit.dataURLToBlob(source) : null;
      if (blob && typeof blob.then === 'function') {
        return blob.then(function (resolvedBlob) {
          return SmartImgKit.triggerDownload(resolvedBlob, filename);
        });
      }
    } else {
      blob = new Blob([source], { type: 'text/plain' });
    }
  }

  if (!blob) throw new Error('Unsupported download source');
  filename = ensureExt(filename, blob);

  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.setAttribute('download', filename);
  a.style.display = 'none';
  document.body.appendChild(a);

  const evt = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true
  });
  a.dispatchEvent(evt);

  setTimeout(() => {
    URL.revokeObjectURL(url);
    if (a.parentNode) a.parentNode.removeChild(a);
  }, 4000);
};
