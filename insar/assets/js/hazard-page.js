/**
 * 工具 3 页面逻辑：判据包选择、Data Tray 数据接入、分级、风险图/柱状图、CSV/KML/PNG 导出
 */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var C = IGCharts.RISK_COLORS, L = Hazard.LABELS;
  var CLS_COLOR = [C.stable, C.low, C.moderate, C.high, C.critical];

  DataTray.mount();

  /* ---------- 判据包选择 ---------- */
  var pkgSel = $("in-pkg");
  Object.keys(Hazard.PACKAGES).forEach(function (k) {
    var o = document.createElement("option");
    o.value = k; o.textContent = Hazard.PACKAGES[k].name;
    pkgSel.appendChild(o);
  });
  pkgSel.onchange = syncPkg;
  function pkg() { return Hazard.PACKAGES[pkgSel.value]; }
  function syncPkg() {
    $("pkg-ref").textContent = pkg().ref + " Gradients (mm/m): " + pkg().gradients.join(" / ");
    $("in-radius").value = pkg().radius;
  }
  syncPkg();

  /* ---------- 数据源（Data Tray 快照） ---------- */
  var working = null;   // {rows:[{lon,lat,vertical_vel}...], name}
  function refreshSources() {
    var st = DataTray.getState();
    if (!st.datasets.length) {
      $("src-list").textContent = "Data Tray is empty — use LOS Converter first, or load the demo.";
      return;
    }
    $("src-list").innerHTML = st.datasets.map(function (d) {
      return "<div>▸ " + d.name + " (" + d.count + " pts)</div>";
    }).join("");
  }
  DataTray.subscribe(refreshSources);
  refreshSources();

  /** 页面内缓存最近一次托盘 rows（托盘快照只含元数据，hook add 拿到 rows 引用） */
  var lastTrayRows = null;
  var origAdd = DataTray.add;
  DataTray.add = function (name, source, rows, fields) {
    lastTrayRows = rows;
    return origAdd(name, source, rows, fields);
  };

  /* ---------- Demo 加载：PS CSV → 纯垂直换算 → 分级 ---------- */
  $("btn-demo").onclick = function () {
    fetch("../../../assets/sample-data/sample-insar-ps-points.csv")
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
        run();
      });
  };

  /* ---------- 分级主流程 ---------- */
  var result = null;  // {points, out, pkgKey}

  function run() {
    if (!lastTrayRows || !lastTrayRows.length) {
      $("run-msg").textContent = "No data. Load demo or import via LOS Converter first.";
      return;
    }
    var p = pkg();
    p.radius = Number($("in-radius").value);   // 允许覆盖半径
    var rows = lastTrayRows;
    var out = Hazard.analyze(
      rows,
      function (r) { return r.lon; }, function (r) { return r.lat; },
      function (r) { return r.vertical_vel; }, p);
    result = { points: rows, out: out, pkgKey: pkgSel.value };
    renderTable();
    renderMap();
    renderBars();
    var dist = [0, 0, 0, 0, 0];
    out.forEach(function (o) { dist[o.cls]++; });
    $("summary").innerHTML = "n=" + rows.length + " | R=" + p.radius + " m | "
      + dist.map(function (c, i) { return '<span class="pill" style="background:' + CLS_COLOR[i] + '">' + L[i] + " " + c + "</span>"; }).join(" ");
    $("run-msg").textContent = "";
  }
  $("btn-run").onclick = run;

  function renderTable() {
    var html = "<thead><tr><th>point</th><th>v_v (mm/yr)</th><th>grad (mm/m)</th><th>nb</th><th>class</th></tr></thead><tbody>";
    result.points.forEach(function (r, i) {
      var o = result.out[i];
      html += "<tr><td>" + (r.point_id || i + 1) + "</td><td>" + r.vertical_vel
        + "</td><td>" + (o.gradient === null ? "—" : o.gradient) + "</td><td>" + o.neighbors
        + '</td><td><span class="pill" style="background:' + CLS_COLOR[o.cls] + '">' + o.label
        + (o.isolated ? " *" : "") + "</span></td></tr>";
    });
    $("table").innerHTML = html + "</tbody>";
  }

  function renderMap() {
    var pts = result.points.map(function (r, i) {
      return {
        value: [r.lon, r.lat],
        itemStyle: { color: CLS_COLOR[result.out[i].cls] },
        point_id: r.point_id, v: r.vertical_vel, cls: result.out[i].label,
      };
    });
    if (run.mapChart) { run.mapChart.dispose(); }
    run.mapChart = IGCharts.render($("map"), {
      tooltip: { formatter: function (p) { return p.data.point_id + "<br>v_v " + p.data.v + " mm/yr<br>" + p.data.cls; } },
      xAxis: { type: "value", name: "lon", scale: true },
      yAxis: { type: "value", name: "lat", scale: true },
      series: [{ type: "scatter", symbolSize: 10, data: pts }],
    });
  }

  function renderBars() {
    var dist = [0, 0, 0, 0, 0];
    result.out.forEach(function (o) { dist[o.cls]++; });
    if (run.barChart) { run.barChart.dispose(); }
    run.barChart = IGCharts.render($("bars"), {
      xAxis: { type: "category", data: L },
      yAxis: { type: "value", name: "points" },
      series: [{ type: "bar", data: dist.map(function (v, i) {
        return { value: v, itemStyle: { color: CLS_COLOR[i] } };
      }) }],
    });
  }

  /* ---------- 导出：CSV / KML / PNG ---------- */
  function download(text, name, type) {
    var blob = new Blob([text], { type: type || "text/csv" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  $("btn-csv").onclick = function () {
    if (!result) { return; }
    var head = "point_id,lon,lat,vertical_vel,gradient_mm_per_m,neighbors,class" + (result.out.some(function (o) { return o.isolated; }) ? ",isolated" : "") + "\n";
    var body = result.points.map(function (r, i) {
      var o = result.out[i];
      return [r.point_id || i + 1, r.lon, r.lat, r.vertical_vel, o.gradient === null ? "" : o.gradient, o.neighbors, o.label].join(",");
    }).join("\n");
    download(head + body, "hazard-classified.csv");
    $("export-msg").textContent = "CSV downloaded";
  };

  // KML：点样式按风险色（KML 颜色格式 aabbggrr）
  $("btn-kml").onclick = function () {
    if (!result) { return; }
    function kmlColor(hex) {
      var r = hex.slice(1, 3), g = hex.slice(3, 5), b = hex.slice(5, 7);
      return "ff" + b + g + r;
    }
    var k = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>insar-geosettle hazard classes</name>\n';
    L.forEach(function (label, i) {
      k += '<Style id="c' + i + '"><IconStyle><color>' + kmlColor(CLS_COLOR[i]) + '</color><scale>0.9</scale><Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon></IconStyle></Style>\n';
    });
    result.points.forEach(function (r, i) {
      var o = result.out[i];
      k += '<Placemark><name>' + (r.point_id || i + 1) + "</name>"
        + '<styleUrl>#c' + o.cls + "</styleUrl>"
        + "<description>v_v " + r.vertical_vel + " mm/yr; gradient " + o.gradient + " mm/m; " + o.label + "</description>"
        + "<Point><coordinates>" + r.lon + "," + r.lat + ",0</coordinates></Point></Placemark>\n";
    });
    k += "</Document></kml>";
    download(k, "hazard-classified.kml", "application/vnd.google-earth.kml+xml");
    $("export-msg").textContent = "KML downloaded";
  };

  $("btn-png").onclick = function () {
    if (!run.mapChart) { return; }
    IGCharts.exportPNG300(run.mapChart, "hazard-map-300dpi.png");
    $("export-msg").textContent = "PNG 300DPI downloaded";
  };
})();
