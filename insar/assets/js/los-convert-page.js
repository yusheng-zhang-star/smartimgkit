/**
 * 工具 1 页面逻辑：输入联动、单点/批量计算、几何矢量图、导入导出
 * 计算内核在 los-convert.js（纯函数，便于复用与自检）
 */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var val = function (id) { return Number($(id).value); };

  DataTray.mount();

  /* ---------- 单点计算 ---------- */
  function singleInput() {
    return {
      los_vel: val("in-los"), incidence_angle: val("in-inc"),
      azimuth: val("in-az"), slope: val("in-slope"),
      aspect: val("in-asp"), d_incidence: val("in-dinc"),
    };
  }

  function renderSingle() {
    var p = singleInput();
    var r = LOSConvert.computePoint(p);
    var pill = r.slope_reliable
      ? '<span class="pill ok">slope component observable</span>'
      : '<span class="pill bad">slope component poorly observable (|projection| &lt; 0.15)</span>';
    $("single-result").innerHTML =
      '<table class="res">'
      + row("Vertical velocity v<sub>v</sub> (pure-vertical assumption)", r.vertical_vel + " mm/yr ± " + r.vertical_err)
      + row("Along-slope velocity u<sub>s</sub> (pure-slope assumption)", r.slope_vel === null ? "n/a" : r.slope_vel + " mm/yr")
      + row("Slope→LOS projection factor", r.slope_factor)
      + "</table>" + pill
      + '<div class="hint">Single-track ambiguity: vertical and along-slope cannot be resolved simultaneously. '
      + 'Report the assumption used. Combine ascending + descending tracks to separate the two components.</div>';

    drawGeometry(p, r);
  }

  function row(k, v) { return "<tr><td>" + k + "</td><td><b>" + v + "</b></td></tr>"; }

  /* ---------- 动态几何矢量图（原生 SVG，输入实时联动） ----------
     侧视剖面：沿 LOS 水平投影方向切开。
     画：坡面线、卫星视线（θ 自垂直方向）、垂直分量箭头、沿坡分量箭头 */
  function drawGeometry(p, r) {
    var svg = $("geom");
    var W = 480, H = 260, cx = 200, gy = 210;      // 坡脚位置
    var beta = p.slope * Math.PI / 180;             // 坡度
    var th = p.incidence_angle * Math.PI / 180;     // 入射角

    // 坡面：从坡脚向右上方抬升（下坡朝左）
    var toeX = cx - 120, topX = cx + 160, topY = gy - Math.tan(beta) * (topX - toeX);
    var s = "";
    s += '<line x1="20" y1="' + gy + '" x2="' + toeX + '" y2="' + gy + '" stroke="#8a999f" stroke-width="2"/>';
    s += '<line x1="' + toeX + '" y1="' + gy + '" x2="' + topX + '" y2="' + topY + '" stroke="#184A54" stroke-width="3"/>';

    // 监测点：坡面中点
    var mx = (toeX + topX) / 2, my = (gy + topY) / 2;

    // LOS 视线：从卫星（右上）指向监测点，与垂直方向夹角 θ
    var losLen = 110;
    var lx = mx - Math.sin(th) * losLen;            // LOS 水平投影朝 α 方向（画面上简化朝右）
    var ly = my - Math.cos(th) * losLen;
    s += '<line x1="' + lx + '" y1="' + ly + '" x2="' + mx + '" y2="' + my + '" stroke="#D27948" stroke-width="2.5" marker-end="url(#arrO)"/>';
    s += '<rect x="' + (lx - 14) + '" y="' + (ly - 16) + '" width="28" height="14" rx="2" fill="#D27948"/>';
    s += '<text x="' + lx + '" y="' + (ly - 5) + '" font-size="9" fill="#fff" text-anchor="middle">SAT</text>';

    // 垂直形变箭头（负值=沉降向下）
    var vLen = Math.max(-40, Math.min(40, r.vertical_vel)); // 视觉限幅
    var upDown = vLen < 0 ? 1 : -1;                  // 沉降 → 箭头向下
    s += '<line x1="' + mx + '" y1="' + my + '" x2="' + mx + '" y2="' + (my + upDown * Math.abs(vLen)) + '" stroke="#184A54" stroke-width="2.5" marker-end="url(#arrT)"/>';
    s += '<text x="' + (mx + 6) + '" y="' + (my + (vLen < 0 ? Math.abs(vLen) : 0) - 4) + '" font-size="10" fill="#184A54">v_v = ' + r.vertical_vel + ' mm/yr</text>';

    // 沿坡分量箭头（纯沿坡假设，可观测时画出）
    if (r.slope_vel !== null) {
      var uLen = Math.max(-50, Math.min(50, r.slope_vel));
      var dir = uLen < 0 ? -1 : 1;                   // 负值 → 沿下坡方向
      var ux = mx + dir * Math.cos(beta) * Math.abs(uLen) * 0.9;
      var uy = my - dir * Math.sin(beta) * Math.abs(uLen) * 0.9;
      s += '<line x1="' + mx + '" y1="' + my + '" x2="' + ux + '" y2="' + uy + '" stroke="#E28942" stroke-width="2.5" stroke-dasharray="5 3" marker-end="url(#arrM)"/>';
      s += '<text x="' + (ux + 4) + '" y="' + uy + '" font-size="10" fill="#E28942">u_s = ' + r.slope_vel + '</text>';
    }

    // 角度标注
    s += '<path d="M ' + mx + ' ' + (my - 40) + ' A 40 40 0 0 0 ' + (mx - Math.sin(th) * 40) + ' ' + (my - Math.cos(th) * 40) + '" fill="none" stroke="#8a999f"/>';
    s += '<text x="' + (mx - 26) + '" y="' + (my - 46) + '" font-size="10" fill="#5a6b72">θ=' + p.incidence_angle + '°</text>';
    s += '<text x="24" y="' + (gy + 18) + '" font-size="10" fill="#5a6b72">ground surface (aspect δ=' + p.aspect + '°)</text>';

    svg.innerHTML =
      '<defs>'
      + '<marker id="arrO" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#D27948"/></marker>'
      + '<marker id="arrT" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#184A54"/></marker>'
      + '<marker id="arrM" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#E28942"/></marker>'
      + "</defs>" + s;
  }

  /* ---------- 批量模式 ---------- */
  var batch = null;   // { rows: [计算结果], fields: [输出列名] }
  var scatterChart = null;

  function runBatch(text, name, source) {
    var parsed, map;
    try {
      parsed = CSVUtils.parse(text);
      map = CSVUtils.matchFields(parsed.fields, ["los_vel", "incidence_angle", "azimuth"]);
    } catch (err) {
      $("import-msg").textContent = err.message;
      return;
    }
    var out = parsed.rows.map(function (r) {
      var p = {
        los_vel: Number(r[map.los_vel]), incidence_angle: Number(r[map.incidence_angle]),
        azimuth: Number(r[map.azimuth]), aspect: Number(r[map.aspect] || 0),
        d_incidence: val("in-dinc"),
      };
      var res = LOSConvert.computePoint(p);
      return {
        point_id: r[map.point_id || ""] || ("#" + (out ? 0 : 0)),
        lon: r[map.lon] || "", lat: r[map.lat] || "",
        los_vel: p.los_vel, vertical_vel: res.vertical_vel,
        vertical_err: res.vertical_err, slope_vel: res.slope_vel,
        slope_factor: res.slope_factor,
      };
    });
    // 修正 point_id（map.point_id 可能不存在）
    out.forEach(function (o, i) { if (!o.point_id) { o.point_id = "P" + (i + 1); } });

    batch = { rows: out, fields: ["point_id", "lon", "lat", "los_vel", "vertical_vel", "vertical_err", "slope_vel", "slope_factor"] };
    renderBatchTable();
    renderScatter(out);
    summarize(out);

    // 转换结果注入 Data Tray：下游工具（分级/比对/报告）直接复用
    DataTray.add(name, source, out, batch.fields);
    $("import-msg").textContent = "Loaded " + out.length + " points → Data Tray";
  }

  function renderBatchTable() {
    var html = "<thead><tr>" + batch.fields.map(function (f) { return "<th>" + f + "</th>"; }).join("") + "</tr></thead><tbody>";
    batch.rows.slice(0, 200).forEach(function (r) {
      html += "<tr>" + batch.fields.map(function (f) { return "<td>" + r[f] + "</td>"; }).join("") + "</tr>";
    });
    $("batch-table").innerHTML = html + "</tbody>";
  }

  function summarize(rows) {
    var vv = rows.map(function (r) { return r.vertical_vel; });
    var min = Math.min.apply(null, vv), max = Math.max.apply(null, vv);
    var mean = vv.reduce(function (a, b) { return a + b; }, 0) / vv.length;
    var rapid = vv.filter(function (v) { return v < -15; }).length;   // 粗筛：< -15 mm/yr
    $("batch-summary").innerHTML =
      "n=" + rows.length + " | v_v min " + min + " / mean " + mean.toFixed(1) + " / max " + max
      + " mm/yr | rapid-subsidence points (&lt;-15): <b>" + rapid + "</b>";
  }

  function renderScatter(rows) {
    var pts = rows.filter(function (r) { return isFinite(r.lon) && isFinite(r.lat); })
      .map(function (r) {
        var c = r.vertical_vel < -25 ? "#7C1919" : r.vertical_vel < -15 ? "#D84A4A"
          : r.vertical_vel < -5 ? "#E28942" : r.vertical_vel < 3 ? "#48A969" : "#E6C249";
        return { value: [r.lon, r.lat], itemStyle: { color: c } };
      });
    if (!pts.length) { return; }
    if (scatterChart) { scatterChart.dispose(); }
    scatterChart = IGCharts.render($("scatter"), {
      tooltip: { formatter: function (p) { return p.value[0] + ", " + p.value[1]; } },
      xAxis: { type: "value", name: "lon", scale: true },
      yAxis: { type: "value", name: "lat", scale: true },
      series: [{ type: "scatter", symbolSize: 9, data: pts }],
    });
  }

  /* ---------- 导入入口 ---------- */
  $("btn-demo").onclick = function () {
    fetch("../../assets/sample-data/sample-insar-ps-points.csv")
      .then(function (r) { return r.text(); })
      .then(function (t) { runBatch(t, "sample-insar-ps-points.csv", "demo"); });
  };
  $("btn-file").onclick = function () { $("in-file").click(); };
  $("in-file").onchange = function (e) {
    var f = e.target.files[0];
    if (!f) { return; }
    var rd = new FileReader();
    rd.onload = function () { runBatch(rd.result, f.name, "csv"); };
    rd.readAsText(f);
  };
  $("btn-paste-show").onclick = function () {
    $("in-paste").style.display = "block"; $("btn-paste-run").style.display = "inline-block";
  };
  $("btn-paste-run").onclick = function () { runBatch($("in-paste").value, "pasted-data", "paste"); };

  /* ---------- 导出 ---------- */
  $("btn-export-csv").onclick = function () {
    if (!batch) { $("export-msg").textContent = "No batch results yet"; return; }
    var out = batch.fields.join(",") + "\n" + batch.rows
      .map(function (r) { return batch.fields.map(function (f) { return r[f]; }).join(","); }).join("\n");
    downloadText(out, "los-convert-results.csv");
    $("export-msg").textContent = "CSV downloaded (" + batch.rows.length + " rows)";
  };
  $("btn-export-svg").onclick = function () {
    var str = new XMLSerializer().serializeToString($("geom"));
    downloadText(str, "los-geometry.svg", "image/svg+xml");
    $("export-msg").textContent = "SVG downloaded";
  };
  function downloadText(text, name, type) {
    var blob = new Blob([text], { type: type || "text/csv" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  /* ---------- 联动 ---------- */
  $("btn-compute").onclick = renderSingle;
  $("btn-s1").onclick = function () {   // Sentinel-1 降轨默认参数
    $("in-inc").value = 38; $("in-az").value = 281; $("in-dinc").value = 0.5; renderSingle();
  };
  ["in-los", "in-inc", "in-az", "in-slope", "in-asp", "in-dinc"].forEach(function (id) {
    $(id).addEventListener("input", renderSingle);
  });

  renderSingle();
})();
