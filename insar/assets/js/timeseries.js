/**
 * insar-geosettle — 工具 6 内核：时序累计沉降计算（文档 4.1-6）
 *
 * 输入：长表 { point_id, date, displacement_mm }（SBAS 时序导出，累计位移）
 * 计算：
 *   - 全程线性拟合速率（最小二乘，mm/yr）
 *   - 前后半段分段拟合速率 rate1 / rate2
 *   - 加速判定（筛查级）：rate2 − rate1 ≥ accelMin（默认 3 mm/yr 内增速）且 rate2 > rate1
 *   - 突跳检测：单期 |Δ| > stepMin（默认 15 mm/月）标记 step
 * 纯函数，便于自检。
 */
(function (global) {
  "use strict";

  var DAY = 864e5;

  /** 按点分组并按时间排序：[{ id, series:[{t:Date, tYears, d}] }] */
  function group(rows) {
    var map = {};
    rows.forEach(function (r) {
      var id = String(r.point_id);
      if (!map[id]) { map[id] = []; }
      map[id].push({ t: new Date(r.date), d: Number(r.displacement_mm) });
    });
    return Object.keys(map).map(function (id) {
      var s = map[id].sort(function (a, b) { return a.t - b.t; });
      var t0 = s[0].t.getTime();
      s.forEach(function (p) { p.tYears = (p.t.getTime() - t0) / (365.25 * DAY); });
      return { id: id, series: s };
    });
  }

  /** 最小二乘拟合：y = slope·x + b */
  function fit(pts) {
    var n = pts.length;
    if (n < 2) { return { slope: 0, intercept: pts.length ? pts[0].d : 0 }; }
    var sx = 0, sy = 0, sxy = 0, sxx = 0;
    pts.forEach(function (p) { sx += p.tYears; sy += p.d; sxy += p.tYears * p.d; sxx += p.tYears * p.tYears; });
    var slope = (n * sxy - sx * sy) / (n * sxx - sx * sx);
    return { slope: slope, intercept: (sy - slope * sx) / n };
  }

  /**
   * 批量分析。
   * accelMin：加速判定阈值（后半段相对前半段的速率增量下限，mm/yr）
   * stepMin：单期突跳阈值（mm）
   */
  function analyze(rows, accelMin, stepMin) {
    accelMin = accelMin || 3; stepMin = stepMin || 15;
    return group(rows).map(function (g) {
      var s = g.series;
      var whole = fit(s);
      var half = Math.ceil(s.length / 2);
      var r1 = fit(s.slice(0, half)).slope;
      var r2 = fit(s.slice(s.length - half)).slope;

      // 突跳：相邻期位移差
      var step = null;
      for (var i = 1; i < s.length; i++) {
        if (Math.abs(s[i].d - s[i - 1].d) > stepMin) { step = s[i].t.toISOString().slice(0, 10); break; }
      }

      // 加速判定（筛查级）：沉降方向增速 —— 后半段速率比前半段更负，且增量 ≥ accelMin
      var accelerating = (r1 - r2) >= accelMin;

      return {
        id: g.id,
        n: s.length,
        span_months: round1(s[s.length - 1].tYears * 12),
        total_disp: round2(s[s.length - 1].d),
        rate: round2(whole.slope),
        rate_first: round2(r1),
        rate_second: round2(r2),
        accelerating: accelerating,
        accel_delta: round2(r1 - r2),
        step_date: step,
      };
    });
  }

  function round1(x) { return Math.round(x * 10) / 10; }
  function round2(x) { return Math.round(x * 100) / 100; }

  global.TimeSeries = { group: group, fit: fit, analyze: analyze };
})(window);
