/**
 * 工具 4 页面逻辑：InSAR（托盘）× GNSS（文件/粘贴/demo）→ 匹配 → 图表 → 导出
 */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };

  DataTray.mount();

  /* 页面内缓存最近托盘 rows（与工具 3 同一套 hook 方案） */
  var lastTrayRows = null;
  var origAdd = DataTray.add;
  DataTray.add = function (name, source, rows, fields) {
    lastTrayRows = rows;
    return origAdd(name, source, rows, fields);
  };

  function refreshSources() {
    var st = DataTray.getState();
    $("src-list").innerHTML = st.datasets.length
      ? st.datasets.map(function (d) { return "<div>▸ " + d.name + " (" + d.count + " pts)</div>"; }).join("")
      : "Data Tray is empty — run LOS Converter first, or use Load GNSS demo (auto-loads InSAR demo).";
  }
  DataTray.subscribe(refreshSources);
  refreshSources();

  var gnssRows = null;   // GNSS 原始行
  var result = null;     // Validation.match 输出
  var chart = null;

  function loadGnss(text, name) {
    try {
      var parsed = CSVUtils.parse(text);
      var map = CSVUtils.matchFields(parsed.fields, ["lon", "lat", "vertical_vel_gnss"]);
      gnssRows = parsed.rows.map(function (r, i) {
        return {
          point_id: r[map.point_id] || "G" + (i + 1),
          lon: Number(r[map.lon]), lat: Number(r[map.lat]),
          vertical_vel_gnss: Number(r[map.vertical_vel_gnss]),
        };
      });
      $("msg").textContent = "GNSS loaded: " + gnssRows.length + " points (" + name + ")";
    } catch (err) {
      $("msg").textContent = err.message;
    }
  }

  /** InSAR 侧：优先托盘；托盘为空且点了 demo 时自动加载 PS 样例并换算 */
  function insarRows() { return lastTrayRows; }

  function ensureInsarFromDemo(done) {
    if (insarRows()) { done(); return; }
    fetch("../../assets/sample-data/sample-insar-ps-points.csv")
      .then(function (r) { return r.text(); })
      .then(function (t) {
        var parsed = CSVUtils.parse(t);
        var map = CSVUtils.matchFields(parsed.fields, ["lon", "lat", "los_vel", "incidence_angle", "azimuth"]);
        var rows = parsed.rows.map(function (r, i) {
          var c = LOSConvert.computePoint({
            los_vel: Number(r[map.los_vel]), incidence_angle: Number(r[map.incidence_angle]),
            azimuth: Number(r[map.azimuth]), d_incidence: 0.5,
          });
          return { point_id: r[map.point_id] || "P" + (i + 1), lon: Number(r[map.lon]), lat: Number(r[map.lat]), vertical_vel: c.vertical_vel };
        });
        DataTray.add("demo (LOS-converted)", "demo", rows, ["point_id", "lon", "lat", "vertical_vel"]);
        done();
      });
  }

  function run() {
    if (!gnssRows) { $("msg").textContent = "Load GNSS data first."; return; }
    ensureInsarFromDemo(function () {
      result = Validation.match(
        insarRows(), gnssRows, null,
        Number($("in-radius").value), Number($("in-k").value));
      renderTable();
      renderChart();
      $("stats").innerHTML = result.n + " pairs matched | bias " + result.bias
        + " | RMSE " + result.rmse + " | σ " + result.std + " mm/yr";
      $("msg").textContent = "";
    });
  }

  function renderTable() {
    var html = "<thead><tr><th>GNSS</th><th>InSAR</th><th>d (m)</th><th>v_gnss</th><th>v_insar</th><th>res</th><th>flag</th></tr></thead><tbody>";
    result.pairs.forEach(function (p) {
      html += "<tr><td>" + p.gnss_id + "</td><td>" + (p.insar_id || "<i>unmatched</i>")
        + "</td><td>" + p.dist + "</td><td>" + p.v_gnss + "</td><td>" + (p.v_insar === null ? "—" : p.v_insar)
        + "</td><td>" + (p.res === null ? "—" : p.res)
        + "</td><td>" + (p.anomalous ? '<span class="pill bad">anomaly</span>' : (p.unmatched ? '<span class="pill warn">no pair</span>' : '<span class="pill ok">ok</span>'))
        + "</td></tr>";
    });
    $("table").innerHTML = html + "</tbody>";
  }

  /** 1:1 散点图：x=GNSS，y=InSAR，异常点标橙红 */
  function renderChart() {
    var pts = result.pairs.filter(function (p) { return p.res !== null; })
      .map(function (p) {
        return {
          value: [p.v_gnss, p.v_insar],
          itemStyle: { color: p.anomalous ? "#D84A4A" : "#184A54" },
          name: p.gnss_id + "/" + p.insar_id,
        };
      });
    // 1:1 参考线范围：覆盖所有点的包络
    var all = pts.map(function (p) { return p.value; }).flat();
    var lo = Math.min.apply(null, all) - 5, hi = Math.max.apply(null, all) + 5;
    if (chart) { chart.dispose(); }
    chart = IGCharts.render($("chart"), {
      tooltip: { formatter: function (p) { return p.data.name + "<br>GNSS " + p.value[0] + " / InSAR " + p.value[1] + " mm/yr"; } },
      legend: { show: false },
      xAxis: { type: "value", name: "GNSS (mm/yr)", min: lo, max: hi },
      yAxis: { type: "value", name: "InSAR (mm/yr)", min: lo, max: hi },
      series: [
        { type: "line", data: [[lo, lo], [hi, hi]], silent: true, showSymbol: false,
          lineStyle: { color: "#8a999f", type: "dashed" } },
        { type: "scatter", symbolSize: 12, data: pts },
      ],
    });
  }

  /* ---------- 导入入口 ---------- */
  $("btn-demo").onclick = function () {
    fetch("../../assets/sample-data/sample-ground-gnss.csv")
      .then(function (r) { return r.text(); })
      .then(function (t) { loadGnss(t, "demo"); });
  };
  $("btn-file").onclick = function () { $("in-file").click(); };
  $("in-file").onchange = function (e) {
    var f = e.target.files[0];
    if (!f) { return; }
    var rd = new FileReader();
    rd.onload = function () { loadGnss(rd.result, f.name); };
    rd.readAsText(f);
  };
  $("btn-paste-show") && ($("in-paste").style.display = "none"); // 保持占位
  $("btn-paste-run").onclick = function () { loadGnss($("in-paste").value, "pasted"); };
  $("btn-run").onclick = run;

  /* ---------- 导出 ---------- */
  function download(text, name, type) {
    var blob = new Blob([text], { type: type || "text/csv" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  $("btn-csv").onclick = function () {
    if (!result) { return; }
    var head = "gnss_id,insar_id,dist_m,v_gnss,v_insar,residual,anomalous\n";
    var body = result.pairs.map(function (p) {
      return [p.gnss_id, p.insar_id, p.dist, p.v_gnss, p.v_insar, p.res, p.anomalous].join(",");
    }).join("\n");
    download(head + body, "insar-gnss-pairs.csv");
    $("export-msg").textContent = "CSV downloaded";
  };

  $("btn-md").onclick = function () {
    if (!result) { return; }
    var md = Validation.conclusion(result, Number($("in-radius").value), Number($("in-k").value));
    download(md, "validation-conclusion.md", "text/markdown");
    $("conclusion").style.display = "block";
    $("conclusion").textContent = md;
    $("export-msg").textContent = "Markdown downloaded";
  };

  $("btn-copy").onclick = function () {
    if (!result) { return; }
    var md = Validation.conclusion(result, Number($("in-radius").value), Number($("in-k").value));
    navigator.clipboard.writeText(md).then(function () {
      $("export-msg").textContent = "Conclusion copied to clipboard";
    });
  };

  $("btn-png").onclick = function () {
    if (!chart) { return; }
    IGCharts.exportPNG300(chart, "insar-gnss-1to1-300dpi.png");
    $("export-msg").textContent = "PNG 300DPI downloaded";
  };
})();
