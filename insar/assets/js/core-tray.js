/**
 * insar-geosettle — 全局 Data Tray 数据托盘（文档 4.2，核心交互创新）
 *
 * 职责：
 *   1. 内存中托管数据集（CSV 导入 / Excel 粘贴 / Demo 加载的结果）
 *   2. 右下角常驻悬浮托盘：显示数据集与点位数，一键 Clear All / Export
 *   3. 变更时广播事件，任何工具页可订阅获取数据（一次导入，全工具流转）
 *
 * 隐私铁律（文档 4.6）：
 *   - 全部数据仅存内存，刷新/关闭页面即销毁
 *   - 禁止写入 localStorage / sessionStorage / Cookie / 任何网络请求
 */
(function (global) {
  "use strict";

  var listeners = [];

  /** 内存态数据集列表：{ id, name, source, rows, fields } */
  var datasets = [];
  var seq = 0;

  function totalPoints() {
    return datasets.reduce(function (s, d) { return s + d.rows.length; }, 0);
  }

  function notify() {
    renderPanel();
    listeners.forEach(function (fn) { fn(getState()); });
  }

  function getState() {
    // 返回浅拷贝快照，防止外部直接改内部状态
    return {
      datasets: datasets.map(function (d) {
        return { id: d.id, name: d.name, source: d.source, count: d.rows.length, fields: d.fields };
      }),
      total: totalPoints(),
    };
  }

  /** 添加一个数据集（rows 为对象数组） */
  function add(name, source, rows, fields) {
    if (!rows || !rows.length) { throw new Error("Empty dataset"); }
    datasets.push({
      id: "ds" + (++seq),
      name: name,
      source: source,            // demo / csv / paste / computed
      rows: rows,
      fields: fields || Object.keys(rows[0]),
    });
    notify();
  }

  function clear() { datasets = []; notify(); }

  /** 把当前全部数据集导出为一个 CSV 下载 */
  function exportCSV() {
    if (!datasets.length) { return; }
    var out = "";
    datasets.forEach(function (d) {
      out += "# dataset: " + d.name + " (" + d.rows.length + " points)\n";
      out += d.fields.join(",") + "\n";
      d.rows.forEach(function (r) {
        out += d.fields.map(function (k) { return r[k]; }).join(",") + "\n";
      });
      out += "\n";
    });
    var blob = new Blob([out], { type: "text/csv" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "insar-geosettle-dataset.csv";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  function subscribe(fn) { listeners.push(fn); if (datasets.length) { fn(getState()); } }

  /* ---------------- 悬浮托盘 UI ---------------- */
  var panel = null;

  function mount() {
    if (panel) { return; }
    panel = document.createElement("div");
    panel.id = "ig-data-tray";
    document.body.appendChild(panel);
    renderPanel();
  }

  function renderPanel() {
    if (!panel) { return; }
    var html = '<div class="tray-head">Data Tray <span class="tray-badge">' + totalPoints() + ' pts</span></div>';
    if (datasets.length) {
      html += datasets.map(function (d) {
        return '<div class="tray-row"><span class="tray-src">' + d.source + '</span>'
          + d.name + ' <b>' + d.rows.length + '</b></div>';
      }).join("");
      html += '<div class="tray-btns">'
        + '<button data-act="export">Export</button>'
        + '<button data-act="clear">Clear All</button></div>';
    } else {
      html += '<div class="tray-row tray-empty">No dataset loaded. In-memory only — cleared on page close.</div>';
    }
    panel.innerHTML = html;
  }

  // 托盘按钮事件（事件委托，只绑一次）
  document.addEventListener("click", function (e) {
    var act = e.target.getAttribute && e.target.getAttribute("data-act");
    if (!act) { return; }
    if (act === "clear") { clear(); }
    if (act === "export") { exportCSV(); }
  });

  global.DataTray = {
    add: add,
    clear: clear,
    exportCSV: exportCSV,
    subscribe: subscribe,
    getState: getState,
    mount: mount,
  };
})(window);
