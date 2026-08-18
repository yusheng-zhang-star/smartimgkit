/**
 * SmartImgKit - Result Modal & Viral Sharing Module
 * Self-contained: injects CSS + DOM, exposes openResultModal(resultData)
 * Dependencies: none (pure vanilla JS)
 */
(function() {
  'use strict';

  /* ===== Config ===== */
  var N8N_WEBHOOK_URL = ''; // Fill in during deployment
  var SITE_URL = 'https://smartimgkit.com';
  var EMBED_CODE =
    '<!-- Embed SmartImgKit image compressor on your site -->\n' +
    '<iframe src="https://smartimgkit.com" width="800" height="600" frameborder="0" title="SmartImgKit Image Tool"></iframe>\n' +
    'Source: <a href="https://smartimgkit.com">SmartImgKit.com</a>';

  /* ===== State ===== */
  var state = {
    origSize: '',
    optSize: '',
    saveRate: '',
    originalBlob: null,
    resultBlob: null,
    resultUrl: null,
    watermarkOn: false,
    fileName: 'optimized-image'
  };

  /* ===== GA4 Helper ===== */
  function track(eventName, params) {
    params = params || {};
    try {
      if (typeof gtag === 'function') {
        gtag('event', eventName, params);
      } else if (window.dataLayer) {
        window.dataLayer.push({ event: eventName, event_params: params });
      }
    } catch(e) {}
  }

  /* ===== Inject CSS (self-contained, no external dependency) ===== */
  function injectCSS() {
    if (document.getElementById('result-modal-css')) return;
    var style = document.createElement('style');
    style.id = 'result-modal-css';
    style.textContent = `
.result-modal-overlay{display:none;position:fixed;inset:0;z-index:999;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);align-items:center;justify-content:center;padding:16px;}
.result-modal-overlay.open{display:flex;}
.result-modal{background:var(--bg-card,#fff);border:1px solid var(--border-color,#e2e4ea);border-radius:16px;max-width:520px;width:100%;max-height:90vh;overflow-y:auto;position:relative;box-shadow:0 8px 40px rgba(0,0,0,.3);}
.result-modal-close{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:50%;background:var(--bg-tertiary,#f0f1f5);border:1px solid var(--border-color,#e2e4ea);font-size:1.3rem;color:var(--text-secondary,#5a5a6e);cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1;z-index:2;}
.result-modal-close:hover{background:var(--bg-card-hover,#e8e9ee);}
.result-modal-body{padding:32px 24px 24px;}
.result-modal-body h2{font-size:1.3rem;font-weight:700;margin-bottom:16px;text-align:center;color:var(--text-primary,#1a1a2e);}
.result-preview{background:var(--bg-secondary,#f8f9fb);border-radius:12px;padding:16px;text-align:center;margin-bottom:20px;}
.result-preview img{max-width:100%;max-height:240px;border-radius:8px;}
.result-stats{display:flex;justify-content:space-around;gap:8px;margin-bottom:24px;flex-wrap:wrap;}
.stat-item{text-align:center;flex:1;min-width:90px;}
.stat-label{display:block;font-size:.75rem;color:var(--text-muted,#9a9aaa);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;}
.stat-value{display:block;font-size:1.1rem;font-weight:700;color:var(--text-primary,#1a1a2e);}
.stat-saved .stat-value{color:var(--success,#16a34a);}
.result-actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:20px;}
.rm-btn{padding:10px 20px;border-radius:10px;font-weight:600;font-size:.9rem;cursor:pointer;border:none;transition:all .25s cubic-bezier(.4,0,.2,1);display:inline-flex;align-items:center;gap:6px;}
.rm-btn-primary{background:linear-gradient(135deg,var(--gradient-from,#4f46e5),var(--gradient-to,#7c3aed));color:#fff;box-shadow:0 4px 20px var(--accent-glow,rgba(79,70,229,.15));}
.rm-btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 28px var(--accent-glow,rgba(79,70,229,.2));}
.rm-btn-secondary{background:var(--bg-tertiary,#f0f1f5);color:var(--text-primary,#1a1a2e);border:1px solid var(--border-color,#e2e4ea);}
.rm-btn-secondary:hover{background:var(--bg-card-hover,#e8e9ee);}
.result-share-section{display:flex;align-items:center;gap:10px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}
.share-label{font-size:.85rem;color:var(--text-secondary,#5a5a6e);font-weight:500;}
.share-btn{width:38px;height:38px;border-radius:50%;background:var(--bg-tertiary,#f0f1f5);border:1px solid var(--border-color,#e2e4ea);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .25s;}
.share-btn:hover{background:var(--accent,#4f46e5);color:#fff;border-color:var(--accent,#4f46e5);}
.result-toggle-row{display:flex;align-items:center;gap:8px;justify-content:center;margin-bottom:20px;}
.result-toggle-row label{font-size:.82rem;color:var(--text-secondary,#5a5a6e);cursor:pointer;}
.result-toggle-row input{cursor:pointer;}
.result-email-row{display:flex;gap:8px;margin-bottom:16px;}
.result-email-row input{flex:1;padding:10px 12px;border-radius:10px;border:1px solid var(--border-color,#e2e4ea);background:var(--bg-secondary,#f8f9fb);color:var(--text-primary,#1a1a2e);font-size:.85rem;font-family:inherit;}
.result-email-row input:focus{outline:none;border-color:var(--accent,#4f46e5);}
.result-email-row input::placeholder{color:var(--text-muted,#9a9aaa);}
.email-feedback{font-size:.8rem;text-align:center;margin-bottom:12px;min-height:18px;}
.email-feedback.success{color:var(--success,#16a34a);}
.email-feedback.error{color:#ef4444;}
.result-embed{background:var(--bg-secondary,#f8f9fb);border:1px solid var(--border-color,#e2e4ea);border-radius:10px;padding:12px;margin-bottom:16px;}
.result-embed summary{cursor:pointer;font-size:.82rem;color:var(--text-secondary,#5a5a6e);font-weight:500;outline:none;}
.result-embed summary:hover{color:var(--text-primary,#1a1a2e);}
.result-embed pre{margin:8px 0 8px;white-space:pre-wrap;word-break:break-all;font-size:.75rem;color:var(--text-secondary,#5a5a6e);font-family:'Courier New',monospace;}
.result-embed-copy{width:100%;padding:8px;border-radius:8px;font-size:.82rem;}
.result-email-section{margin-bottom:16px;}
.result-tip{font-size:.82rem;color:var(--text-muted,#9a9aaa);text-align:center;margin-top:12px;}
.result-compare-preview{margin-top:12px;text-align:center;display:none;}
.result-compare-preview img{max-width:100%;border-radius:8px;margin-top:8px;}
@media(max-width:520px){
  .result-modal-body{padding:24px 16px 16px;}
  .result-stats{flex-direction:column;gap:8px;}
  .result-actions{flex-direction:column;}
  .rm-btn{width:100%;justify-content:center;}
  .result-email-row{flex-direction:column;}
}
`;
    document.head.appendChild(style);
  }

  /* ===== Build modal DOM ===== */
  function buildModal() {
    if (document.getElementById('resultModalOverlay')) return;

    var overlay = document.createElement('div');
    overlay.className = 'result-modal-overlay';
    overlay.id = 'resultModalOverlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'resultModalTitle');
    overlay.innerHTML = `
      <div class="result-modal" role="document">
        <button class="result-modal-close" id="resultModalClose" aria-label="Close dialog">&times;</button>
        <div class="result-modal-body">
          <h2 id="resultModalTitle">✅ Image Optimization Complete</h2>
          <div class="result-preview">
            <img id="resultPreviewImg" alt="Processed image preview" />
          </div>
          <div class="result-stats">
            <div class="stat-item"><span class="stat-label">Original</span><span class="stat-value" id="statOrigSize">-</span></div>
            <div class="stat-item"><span class="stat-label">Optimized</span><span class="stat-value" id="statOptSize">-</span></div>
            <div class="stat-item stat-saved"><span class="stat-label">Saved</span><span class="stat-value" id="statSaveRate">-</span></div>
          </div>
          <div class="result-toggle-row">
            <label><input type="checkbox" id="rmWatermarkToggle" /> Add "Powered by SmartImgKit" watermark</label>
          </div>
          <div class="result-actions">
            <button class="rm-btn rm-btn-primary" id="rmDownloadBtn">📥 Download Image</button>
            <button class="rm-btn rm-btn-secondary" id="rmCopyReportBtn">📋 Copy Report</button>
          </div>
          <div class="result-share-section">
            <span class="share-label">Share:</span>
            <button class="share-btn" id="rmShareTwitter" title="Share on X (Twitter)" aria-label="Share on X (Twitter)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></button>
            <button class="share-btn" id="rmShareFacebook" title="Share on Facebook" aria-label="Share on Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.404 0 .763.008 1.107.022v3.36c-.43-.005-.752-.013-1.052-.013-1.35 0-1.872.617-1.872 2.264v1.925h3.287l-.706 3.667h-2.581v8.061c5.376-.608 9.562-5.218 9.562-10.769C22.061 5.679 17.382 1 12 1S1.939 5.679 1.939 11.7c0 5.551 4.186 10.161 9.562 10.769z"/></svg></button>
            <button class="share-btn" id="rmShareSystem" title="System Share" aria-label="Share via system"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/></svg></button>
          </div>
          <div class="result-compare-preview" id="rmComparePreview">
            <button class="rm-btn rm-btn-secondary" id="rmGenerateCompareBtn">Generate comparison preview</button>
            <div id="rmCompareImageContainer"></div>
          </div>
          <div class="result-email-section" id="rmEmailSection">
            <div class="result-email-row">
              <input type="email" id="rmEmailInput" placeholder="(Optional) Enter email for full report" />
              <button class="rm-btn rm-btn-secondary" id="rmEmailSubmit">Submit</button>
            </div>
            <div class="email-feedback" id="rmEmailFeedback"></div>
          </div>
          <details class="result-embed">
            <summary>Embed code</summary>
            <pre id="rmEmbedCode"></pre>
            <button class="rm-btn rm-btn-secondary result-embed-copy" id="rmCopyEmbedBtn">Copy embed code</button>
          </details>
          <p class="result-tip">💡 Tip: Bookmark SmartImgKit for quick access next time.</p>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    bindEvents();
  }

  /* ===== Apply watermark to a canvas ===== */
  function applyWatermark(canvas) {
    var ctx = canvas.getContext('2d');
    var fontSize = Math.max(10, Math.round(canvas.width * 0.018));
    ctx.font = fontSize + 'px Inter, Arial, sans-serif';
    ctx.fillStyle = 'rgba(128,128,128,0.25)';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'bottom';
    ctx.fillText('Powered by SmartImgKit', canvas.width - 8, canvas.height - 8);
  }

  /* ===== Download image (with optional watermark) ===== */
  function downloadResult() {
    if (!state.resultBlob) return;
    track('download_image', { file_size: state.optSize });

    if (state.watermarkOn) {
      // Redraw with watermark
      var img = new Image();
      img.onload = function() {
        var canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        applyWatermark(canvas);
        canvas.toBlob(function(wmBlob) {
          if (window.SmartImgKit && SmartImgKit._downloadBlob) {
            SmartImgKit._downloadBlob(wmBlob, state.fileName, state.resultBlob.type);
          } else {
            var url = URL.createObjectURL(wmBlob);
            var a = document.createElement('a');
            a.href = url; a.download = state.fileName;
            a.click();
            setTimeout(function() { URL.revokeObjectURL(url); }, 4000);
          }
        }, state.resultBlob.type || 'image/png');
      };
      img.src = state.resultUrl;
    } else {
      if (window.SmartImgKit && SmartImgKit._downloadBlob) {
        SmartImgKit._downloadBlob(state.resultBlob, state.fileName, state.resultBlob.type);
      } else {
        var url = URL.createObjectURL(state.resultBlob);
        var a = document.createElement('a');
        a.href = url; a.download = state.fileName;
        a.click();
        setTimeout(function() { URL.revokeObjectURL(url); }, 4000);
      }
    }
  }

  /* ===== Copy report text ===== */
  function copyReport() {
    var text =
      '✅ Image Optimization Complete\n' +
      'Original: ' + state.origSize + '\n' +
      'Optimized: ' + state.optSize + '\n' +
      'Saved: ' + state.saveRate + '\n\n' +
      'Processed by SmartImgKit\n' +
      SITE_URL;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        track('copy_report', {});
        flashButton('rmCopyReportBtn', '✓ Copied!');
      }).catch(function() { fallbackCopy(text); });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); track('copy_report', {}); flashButton('rmCopyReportBtn', '✓ Copied!'); }
    catch(e) {}
    document.body.removeChild(ta);
  }

  function flashButton(btnId, text) {
    var btn = document.getElementById(btnId);
    if (!btn) return;
    var orig = btn.textContent;
    btn.textContent = text;
    btn.disabled = true;
    setTimeout(function() { btn.textContent = orig; btn.disabled = false; }, 2000);
  }

  /* ===== Share ===== */
  function shareTwitter() {
    track('click_share', { platform: 'twitter' });
    var text = encodeURIComponent('I just optimized an image with SmartImgKit — saved ' + state.saveRate + '! Try it free:');
    var url = 'https://twitter.com/intent/tweet?text=' + text + '&url=' + encodeURIComponent(SITE_URL);
    window.open(url, '_blank', 'noopener');
  }

  function shareFacebook() {
    track('click_share', { platform: 'facebook' });
    var url = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(SITE_URL);
    window.open(url, '_blank', 'noopener');
  }

  function shareSystem() {
    track('click_share', { platform: 'system' });
    if (navigator.share) {
      navigator.share({
        title: 'SmartImgKit — Free Image Tools',
        text: 'I just optimized an image and saved ' + state.saveRate + '!',
        url: SITE_URL
      }).catch(function() {});
    } else {
      showToast('System share is only available on mobile devices.');
    }
  }

  /* ===== Toast notification (replaces alert) ===== */
  function showToast(message) {
    var toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--bg-tertiary,#333);color:var(--text-primary,#fff);padding:12px 24px;border-radius:8px;font-size:.85rem;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.3);opacity:0;transition:opacity .3s;border:1px solid var(--border-color,#555);';
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(function() { toast.style.opacity = '1'; });
    setTimeout(function() {
      toast.style.opacity = '0';
      setTimeout(function() { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 300);
    }, 3000);
  }

  /* ===== Generate comparison preview ===== */
  function generateComparePreview() {
    track('generate_compare_preview', {});

    if (!state.originalBlob || !state.resultBlob) {
      var container = document.getElementById('rmCompareImageContainer');
      container.innerHTML = '<p style="font-size:.8rem;color:var(--text-muted);">Comparison preview unavailable (missing original image data).</p>';
      return;
    }

    var origImg = new Image();
    var resultImg = new Image();
    var loaded = 0;

    function tryCompose() {
      loaded++;
      if (loaded < 2) return;

      var gap = 4;
      var maxH = 300;
      var origRatio = maxH / origImg.naturalHeight;
      var resultRatio = maxH / resultImg.naturalHeight;
      var w1 = Math.round(origImg.naturalWidth * origRatio);
      var w2 = Math.round(resultImg.naturalWidth * resultRatio);
      var h = maxH;

      var canvas = document.createElement('canvas');
      canvas.width = w1 + gap + w2;
      canvas.height = h + 28; // extra space for label
      var ctx = canvas.getContext('2d');

      // Background
      ctx.fillStyle = '#f8f9fb';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Original (left)
      ctx.drawImage(origImg, 0, 0, w1, h);
      // Optimized (right)
      ctx.drawImage(resultImg, w1 + gap, 0, w2, h);

      // Labels
      ctx.font = 'bold 11px Inter, Arial, sans-serif';
      ctx.fillStyle = '#5a5a6e';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'top';
      ctx.fillText('Before', 6, h + 6);
      ctx.fillText('After', w1 + gap + 6, h + 6);

      // Watermark
      ctx.font = '10px Inter, Arial, sans-serif';
      ctx.fillStyle = 'rgba(128,128,128,0.3)';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'bottom';
      ctx.fillText('Powered by SmartImgKit', canvas.width - 6, canvas.height - 4);

      var dataUrl = canvas.toDataURL('image/png');
      var container = document.getElementById('rmCompareImageContainer');
      container.innerHTML =
        '<img src="' + dataUrl + '" alt="Before and after comparison" style="border-radius:8px;" />' +
        '<div style="margin-top:8px;"><a href="' + dataUrl + '" download="smartimgkit-comparison.png" class="rm-btn rm-btn-secondary" style="display:inline-flex;text-decoration:none;">📥 Download Comparison</a></div>';
    }

    origImg.onload = tryCompose;
    resultImg.onload = tryCompose;
    origImg.src = URL.createObjectURL(state.originalBlob);
    resultImg.src = state.resultUrl;
  }

  /* ===== Email submit ===== */
  function submitEmail() {
    var input = document.getElementById('rmEmailInput');
    var feedback = document.getElementById('rmEmailFeedback');
    var email = input.value.trim();

    if (!email) {
      feedback.className = 'email-feedback error';
      feedback.textContent = 'Please enter an email address.';
      return;
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      feedback.className = 'email-feedback error';
      feedback.textContent = 'Invalid email format. Please check and try again.';
      return;
    }

    function getUtmParam(name) {
      var params = new URLSearchParams(window.location.search);
      return params.get(name) || '';
    }

    var payload = {
      email: email,
      timestamp: new Date().toISOString(),
      source: window.location.href,
      origSize: state.origSize,
      optSize: state.optSize,
      savePercent: state.saveRate,
      utm_source: getUtmParam('utm_source')
    };

    var submitBtn = document.getElementById('rmEmailSubmit');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    if (!N8N_WEBHOOK_URL) {
      // Webhook not configured — simulate success but log warning
      console.warn('[SmartImgKit] N8N_WEBHOOK_URL not configured. Email not submitted.');
      track('email_submit', { status: 'no_webhook' });
      feedback.className = 'email-feedback success';
      feedback.textContent = '✓ Thank you! Your report will be sent shortly.';
      input.value = '';
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit';
      return;
    }

    fetch(N8N_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function(res) {
      if (res.ok) {
        track('email_submit', { status: 'success' });
        feedback.className = 'email-feedback success';
        feedback.textContent = '✓ Thank you! Your report will be sent shortly.';
        input.value = '';
      } else {
        throw new Error('HTTP ' + res.status);
      }
    }).catch(function(err) {
      track('email_submit', { status: 'error' });
      feedback.className = 'email-feedback error';
      feedback.textContent = 'Submission failed, but your image download is not affected.';
    }).finally(function() {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit';
    });
  }

  /* ===== Copy embed code ===== */
  function copyEmbedCode() {
    var code = EMBED_CODE;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(code).then(function() {
        track('copy_embed_code', {});
        flashButton('rmCopyEmbedBtn', '✓ Copied!');
      }).catch(function() { fallbackCopyEmbed(code); });
    } else {
      fallbackCopyEmbed(code);
    }
  }

  function fallbackCopyEmbed(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); track('copy_embed_code', {}); flashButton('rmCopyEmbedBtn', '✓ Copied!'); } catch(e) {}
    document.body.removeChild(ta);
  }

  /* ===== Close modal ===== */
  function closeModal() {
    var overlay = document.getElementById('resultModalOverlay');
    if (overlay) overlay.classList.remove('open');
    // Revoke object URL to free memory
    if (state.resultUrl) {
      URL.revokeObjectURL(state.resultUrl);
      state.resultUrl = null;
    }
  }

  /* ===== Bind events ===== */
  function bindEvents() {
    document.getElementById('resultModalClose').addEventListener('click', closeModal);
    document.getElementById('resultModalOverlay').addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        var overlay = document.getElementById('resultModalOverlay');
        if (overlay && overlay.classList.contains('open')) closeModal();
      }
    });
    document.getElementById('rmDownloadBtn').addEventListener('click', downloadResult);
    document.getElementById('rmCopyReportBtn').addEventListener('click', copyReport);
    document.getElementById('rmShareTwitter').addEventListener('click', shareTwitter);
    document.getElementById('rmShareFacebook').addEventListener('click', shareFacebook);
    document.getElementById('rmShareSystem').addEventListener('click', shareSystem);
    document.getElementById('rmEmailSubmit').addEventListener('click', submitEmail);
    document.getElementById('rmCopyEmbedBtn').addEventListener('click', copyEmbedCode);
    document.getElementById('rmGenerateCompareBtn').addEventListener('click', generateComparePreview);

    var wmToggle = document.getElementById('rmWatermarkToggle');
    wmToggle.addEventListener('change', function() {
      state.watermarkOn = wmToggle.checked;
    });
  }

  /* ===== Format bytes ===== */
  function formatBytes(bytes) {
    if (!bytes) return '0 B';
    if (typeof bytes === 'string') return bytes; // already formatted
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(2) + ' MB';
  }

  /* ===== Public API: openResultModal ===== */
  window.openResultModal = function(data) {
    injectCSS();
    buildModal();

    // Build embed code with current page URL (not generic homepage)
    var pageUrl = window.location.origin + window.location.pathname;
    var toolName = document.title.split('—')[0].trim() || 'SmartImgKit Tool';
    var dynamicEmbedCode =
      '<!-- Embed ' + toolName + ' on your site -->\n' +
      '<iframe src="' + pageUrl + '" width="800" height="600" frameborder="0" title="' + toolName + '"></iframe>\n' +
      'Source: <a href="' + pageUrl + '">SmartImgKit.com</a>';

    // Update state
    state.origSize = data.origSize ? (typeof data.origSize === 'string' ? data.origSize : formatBytes(data.origSize)) : '-';
    state.optSize = data.optSize ? (typeof data.optSize === 'string' ? data.optSize : formatBytes(data.optSize)) : '-';
    state.saveRate = data.saveRate || '-';
    state.originalBlob = data.originalBlob || null;
    state.resultBlob = data.resultBlob || null;
    state.watermarkOn = false; // always reset to OFF
    state.fileName = data.fileName || 'optimized-image';

    // Determine extension
    if (state.resultBlob && state.resultBlob.type) {
      var extMap = { 'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp', 'image/gif': '.gif', 'image/bmp': '.bmp' };
      var ext = extMap[state.resultBlob.type] || '.png';
      if (state.fileName.indexOf('.') === -1) state.fileName += ext;
    }

    // Create object URL for preview
    if (state.resultUrl) URL.revokeObjectURL(state.resultUrl);
    state.resultUrl = state.resultBlob ? URL.createObjectURL(state.resultBlob) : null;

    // Populate UI
    var previewImg = document.getElementById('resultPreviewImg');
    if (state.resultUrl) {
      previewImg.src = state.resultUrl;
      previewImg.style.display = 'block';
    } else {
      previewImg.style.display = 'none';
    }

    document.getElementById('statOrigSize').textContent = state.origSize;
    document.getElementById('statOptSize').textContent = state.optSize;
    document.getElementById('statSaveRate').textContent = state.saveRate;

    // Reset watermark toggle
    var wmToggle = document.getElementById('rmWatermarkToggle');
    if (wmToggle) wmToggle.checked = false;

    // Reset email
    var emailInput = document.getElementById('rmEmailInput');
    if (emailInput) emailInput.value = '';
    var emailFeedback = document.getElementById('rmEmailFeedback');
    if (emailFeedback) { emailFeedback.textContent = ''; emailFeedback.className = 'email-feedback'; }

    // Embed code (dynamic per page)
    document.getElementById('rmEmbedCode').textContent = dynamicEmbedCode;

    // Hide email section if webhook not configured
    var emailSection = document.getElementById('rmEmailSection');
    if (emailSection) {
      emailSection.style.display = N8N_WEBHOOK_URL ? 'block' : 'none';
    }

    // Hide system share button on desktop (progressive enhancement)
    if (!navigator.share) {
      var sysBtn = document.getElementById('rmShareSystem');
      if (sysBtn) sysBtn.style.display = 'none';
    }

    // Focus management for accessibility
    var closeBtn = document.getElementById('resultModalClose');
    if (closeBtn) closeBtn.focus();

    // Reset compare preview
    var compareContainer = document.getElementById('rmCompareImageContainer');
    if (compareContainer) compareContainer.innerHTML = '';
    var compareSection = document.getElementById('rmComparePreview');
    if (compareSection) compareSection.style.display = (state.originalBlob && state.resultBlob) ? 'block' : 'none';

    // Show modal
    document.getElementById('resultModalOverlay').classList.add('open');
  };

  // Also expose under SmartImgKit namespace
  window.SmartImgKit = window.SmartImgKit || {};
  SmartImgKit.openResultModal = window.openResultModal;

  /* ===== Auto-hook: capture result blobs via monkey-patch =====
   * Strategy: many tool pages store processed result as a local variable
   * (const blob, convertedBlob, etc.) which is unreachable from outside.
   * We monkey-patch URL.createObjectURL to capture the most recent blob
   * (which is typically the processed result). When a result blob is captured,
   * we auto-trigger the modal once per session.
   */
  var _lastResultBlob = null;
  var _lastOriginalFile = null;
  var _modalShownForSession = false; // avoid spamming within one session
  var _captureIgnoreUntil = 0; // timestamp; ignore captures before this time

  function _tryCaptureOriginal() {
    try { if (typeof currentFile !== 'undefined' && currentFile) { _lastOriginalFile = currentFile; return; } } catch(e) {}
    try { if (typeof originalFile !== 'undefined' && originalFile) { _lastOriginalFile = originalFile; return; } } catch(e) {}
    try { if (typeof origFile !== 'undefined' && origFile) { _lastOriginalFile = origFile; return; } } catch(e) {}
    try {
      if (typeof files !== 'undefined' && files && files.length === 1 && files[0]) {
        _lastOriginalFile = files[0].file || files[0];
        return;
      }
    } catch(e) {}
  }

  function _triggerModalFromCapture() {
    if (_modalShownForSession) return; // only once per session
    if (!_lastResultBlob) return;
    _tryCaptureOriginal();

    var _rb = _lastResultBlob;
    var _of = _lastOriginalFile;
    var _origSize = (_of && _of.size) ? _of.size : 0;
    var _optSize = _rb.size || 0;
    var _saveRate = '0%';
    if (_origSize > 0 && _optSize > 0) {
      var _s = Math.round((1 - _optSize / _origSize) * 1000) / 10;
      _saveRate = (_s > 0 ? _s : 0) + '%';
    }
    var _fname = 'optimized-image.png';
    if (_of && _of.name) {
      _fname = _of.name.replace(/\.[^.]+$/, '') + '-optimized.' + (_of.name.split('.').pop() || 'png');
    }

    openResultModal({
      origSize: _origSize > 0 ? _origSize : 'Unknown',
      optSize: _optSize,
      saveRate: _saveRate,
      originalBlob: _of,
      resultBlob: _rb,
      fileName: _fname
    });
    _modalShownForSession = true;
  }

  // Monkey-patch URL.createObjectURL to capture result blobs
  if (!URL._smartimgkit_patched) {
    var _origCreateObjectURL = URL.createObjectURL;
    URL.createObjectURL = function(obj) {
      try {
        // Only capture Blob objects (NOT File objects which are user-uploaded originals)
        // File objects have .name and .lastModified; processed results are plain Blobs from canvas.toBlob
        var isPlainBlob = (obj instanceof Blob) && !(obj instanceof File);
        if (isPlainBlob && obj.size && obj.size > 0 && Date.now() > _captureIgnoreUntil) {
          var t = obj.type || '';
          if (t.indexOf('image') === 0 || t.indexOf('video') === 0 || t.indexOf('audio') === 0 || t.indexOf('application/pdf') === 0 || t.indexOf('application/zip') === 0) {
            _lastResultBlob = obj;
            // Trigger modal after a short delay (lets the page finish its own click handler)
            setTimeout(_triggerModalFromCapture, 200);
          }
        }
      } catch(e) {}
      return _origCreateObjectURL.apply(URL, arguments);
    };
    URL._smartimgkit_patched = true;
  }

  // Also expose a manual trigger for tool pages that want to call it explicitly
  SmartImgKit.triggerResultModal = _triggerModalFromCapture;

})();
