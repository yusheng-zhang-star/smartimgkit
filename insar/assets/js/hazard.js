/**
 * insar-geosettle — 工具 3 内核：沉降梯度风险分级（文档 4.1-3）
 *
 * 梯度定义：点对差异沉降速率 / 水平距离 = mm/m
 *   对每个点取半径 R 内最陡邻差 |Δv_v| / d 作为该点代表梯度。
 * 联合判险（文档 3.3）：梯度分级 + 单点速率加严（v_v 低于 velocityHigh/Critical 阈值时上调一级/至 Critical）。
 *
 * ⚠️ 判据性质（文档 16-2 风险管控）：以下阈值为筛查级默认值，
 *    来源为公开规范的差异沉降控制实践，输出仅作初筛，须对照项目规范核验。
 */
(function (global) {
  "use strict";

  var D2R = Math.PI / 180;

  /** 内置判据包（gradients 为 4 个分界值，划分 5 级） */
  var PACKAGES = {
    highway: {
      name: "Highway (AASHTO-informed screening)",
      ref: "Screening defaults informed by AASHTO highway differential-settlement practice. Verify against the project specification.",
      radius: 100, gradients: [0.5, 1, 2, 4], velocityHigh: -25, velocityCritical: -50,
    },
    railway: {
      name: "Railway embankment (screening)",
      ref: "Stricter screening defaults for railway embankments. Verify against the governing railway code.",
      radius: 100, gradients: [0.25, 0.5, 1, 2], velocityHigh: -25, velocityCritical: -50,
    },
    mine: {
      name: "Open-pit mine slope (screening)",
      ref: "Screening defaults for open-pit slope monitoring campaigns. Verify against mine regulations.",
      radius: 200, gradients: [2, 5, 10, 20], velocityHigh: -40, velocityCritical: -80,
    },
    foundation: {
      name: "Building foundation (screening)",
      ref: "Screening defaults for building foundations. Verify against local building code.",
      radius: 50, gradients: [0.5, 1, 2.5, 5], velocityHigh: -25, velocityCritical: -50,
    },
  };

  var LABELS = ["Stable", "Low Concern", "Moderate", "High Hazard", "Critical"];

  /** 两点球面距离（m），Demo/工程点位均为小范围，haversine 足够 */
  function distM(a, b) {
    var dLat = (b.lat - a.lat) * D2R, dLon = (b.lon - a.lon) * D2R;
    var m = Math.pow(Math.sin(dLat / 2), 2)
      + Math.cos(a.lat * D2R) * Math.cos(b.lat * D2R) * Math.pow(Math.sin(dLon / 2), 2);
    return 6371000 * 2 * Math.atan2(Math.sqrt(m), Math.sqrt(1 - m));
  }

  /** 梯度分级（纯梯度） */
  function classOf(gradient, pkg) {
    var g = pkg.gradients, i = 0;
    while (i < 4 && gradient >= g[i]) { i++; }
    return i;
  }

  /**
   * 批量计算：rows 需含 lon/lat 与速率字段。
   * 返回每点 { gradient, neighbors, cls }；无邻居的点 gradient=null，仅按速率分级并标记 isolated。
   */
  function analyze(rows, getLon, getLat, getV, pkg) {
    var n = rows.length, out = new Array(n);
    for (var i = 0; i < n; i++) {
      var best = null, cnt = 0;
      for (var j = 0; j < n; j++) {
        if (i === j) { continue; }
        var d = distM(
          { lat: getLat(rows[i]), lon: getLon(rows[i]) },
          { lat: getLat(rows[j]), lon: getLon(rows[j]) });
        if (d <= pkg.radius && d > 0.01) {
          cnt++;
          var g = Math.abs(getV(rows[i]) - getV(rows[j])) / d;
          if (best === null || g > best) { best = g; }
        }
      }
      var v = getV(rows[i]);
      var cls = best === null ? classOf(0, pkg) : classOf(best, pkg);
      // 速率加严
      if (v <= pkg.velocityCritical) { cls = 4; }
      else if (v <= pkg.velocityHigh && cls < 3) { cls = 3; }
      out[i] = {
        gradient: best === null ? null : Math.round(best * 1000) / 1000,
        neighbors: cnt,
        isolated: best === null,
        cls: cls, label: LABELS[cls],
      };
    }
    return out;
  }

  global.Hazard = { PACKAGES: PACKAGES, LABELS: LABELS, analyze: analyze, classOf: classOf, distM: distM };
})(window);
