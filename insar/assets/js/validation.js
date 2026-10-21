/**
 * insar-geosettle — 工具 4 内核：InSAR ↔ 地面实测比对（文档 4.1-4）
 *
 * 流程：GNSS 点 → 就近匹配 InSAR 点（haversine，限最大匹配半径）
 *      → 残差 res = v_insar − v_gnss → RMSE / Bias(系统偏差) / σ
 *      → |res| > k·σ 标记偏差异常点（默认 k=2）
 * 全部纯函数，便于自检与复用。
 */
(function (global) {
  "use strict";

  var D2R = Math.PI / 180;

  function distM(a, b) {
    var dLat = (b.lat - a.lat) * D2R, dLon = (b.lon - a.lon) * D2R;
    var m = Math.pow(Math.sin(dLat / 2), 2)
      + Math.cos(a.lat * D2R) * Math.cos(b.lat * D2R) * Math.pow(Math.sin(dLon / 2), 2);
    return 6371000 * 2 * Math.atan2(Math.sqrt(m), Math.sqrt(1 - m));
  }

  /**
   * 就近匹配：每个 GNSS 点找最近 InSAR 点。
   * maxDistM 内匹配成功，否则 unmatched。
   * 返回 pairs: [{ gnss_id, insar_id, lon, lat, v_gnss, v_insar, res, dist, anomalous }]
   */
  function match(insarRows, gnssRows, getI, maxDistM, kSigma) {
    var pairs = [];
    gnssRows.forEach(function (g) {
      var best = null, bestD = Infinity;
      insarRows.forEach(function (s) {
        var d = distM(
          { lat: Number(g.lat), lon: Number(g.lon) },
          { lat: Number(s.lat), lon: Number(s.lon) });
        if (d < bestD) { bestD = d; best = s; }
      });
      var vG = Number(g.vertical_vel_gnss);
      var vS = best ? Number(best.vertical_vel) : null;
      var ok = best && bestD <= maxDistM;
      pairs.push({
        gnss_id: g.point_id || g.gnss_id || "G",
        insar_id: ok ? (best.point_id || "S") : "",
        lon: Number(g.lon), lat: Number(g.lat),
        v_gnss: round2(vG),
        v_insar: ok ? round2(vS) : null,
        res: ok ? round2(vS - vG) : null,
        dist: Math.round(bestD),
        anomalous: false,
        unmatched: !ok,
      });
    });

    // 统计量与异常标记（仅对匹配成功的对）
    var res = pairs.filter(function (p) { return p.res !== null; }).map(function (p) { return p.res; });
    var n = res.length;
    var bias = n ? res.reduce(function (a, b) { return a + b; }, 0) / n : null;
    var rmse = n ? Math.sqrt(res.reduce(function (s, r) { return s + r * r; }, 0) / n) : null;
    var std = n ? Math.sqrt(Math.max(rmse * rmse - bias * bias, 0)) : null;   // σ² = RMSE² − Bias²
    var thr = std === null ? Infinity : kSigma * std + Math.abs(bias);
    pairs.forEach(function (p) {
      if (p.res !== null && Math.abs(p.res - bias) > thr) { p.anomalous = true; }
    });

    return { pairs: pairs, n: n, bias: round2(bias), rmse: round2(rmse), std: round2(std) };
  }

  /**
   * 标准化比对结论段落（英文，可直接粘进报告）。
   * 措辞克制：初筛性质 + 现场核验要求，符合文档 12 章免责红线。
   */
  function conclusion(m, maxDistM, kSigma) {
    if (!m.n) { return "No InSAR–GNSS pairs matched within the search radius."; }
    var res = m.pairs.filter(function (p) { return p.res !== null; }).map(function (p) { return p.res; });
    var min = Math.min.apply(null, res), max = Math.max.apply(null, res);
    var anom = m.pairs.filter(function (p) { return p.anomalous; });
    return [
      "InSAR–ground survey comparison (" + m.n + " collocated pairs, match radius " + maxDistM + " m):",
      "mean systematic bias (InSAR − GNSS) = " + m.bias + " mm/yr; RMSE = " + m.rmse + " mm/yr; "
        + "residual σ = " + m.std + " mm/yr; residual range " + min + " to " + max + " mm/yr.",
      anom.length
        ? anom.length + " pair(s) exceeded " + kSigma + "σ screening tolerance and were flagged for review: "
          + anom.map(function (p) { return p.gnss_id + "/" + p.insar_id; }).join(", ") + "."
        : "No pair exceeded the " + kSigma + "σ screening tolerance.",
      "This screening-level comparison indicates acceptable agreement for preliminary interpretation; "
        + "discrepancies require field verification by qualified professionals before engineering use.",
    ].join(" ");
  }

  function round2(x) { return x === null || isNaN(x) ? null : Math.round(x * 100) / 100; }

  global.Validation = { match: match, conclusion: conclusion, distM: distM };
})(window);
