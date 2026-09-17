// publish-gate.js — 定时发布门控（复用 golden.sendafun.com 的 publishAt 思路）
// 用法：在 <script src="/js/publish-gate.js" data-publish-at="2026-09-18T08:00:00+08:00"></script>
// 未到时间：页面显示"即将发布"，列表页隐藏卡片
(function(){
  var script = document.currentScript;
  var publishAt = script && script.getAttribute('data-publish-at');
  if(!publishAt) return;
  var now = new Date();
  var pub = new Date(publishAt);
  if(now < pub){
    // 单篇文章：替换内容
    document.addEventListener('DOMContentLoaded', function(){
      document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;min-height:80vh;text-align:center;font-family:Inter,system-ui,sans-serif;color:#94a3b8">' +
        '<div><div style="font-size:3rem;margin-bottom:1rem">⏳</div>' +
        '<h1 style="font-size:1.5rem;margin-bottom:.5rem">Coming Soon</h1>' +
        '<p>This article will be published at ' + pub.toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'}) + '</p></div></div>';
    });
  }
})();

// 列表页：隐藏未到时间的卡片
// 在卡片上加 data-publish-at="2026-09-18T08:00:00+08:00"
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var cards = document.querySelectorAll('[data-publish-at]');
    cards.forEach(function(card){
      var pub = new Date(card.getAttribute('data-publish-at'));
      if(new Date() < pub){
        card.style.display = 'none';
      }
    });
  });
})();
