/**
 * insar-geosettle — 工具 5 内核：InSAR 误差预算合成（文档 4.1-5）
 *
 * 模型：各误差源相互独立，按方和根（quadrature）合成：
 *   σ_total = sqrt(Σ σi²)，贡献占比 = σi² / Σ σj²
 * 默认值为筛查级典型量级（Sentinel-1 小基线场景），仅供初筛，
 * 评审文本须按项目实际处理参数核验（文档 16-2）。
 */
(function (global) {
  "use strict";

  /** 五项误差源默认值（mm，或速度场景 mm/yr），editable */
  var SOURCES = [
    { key: "dem", label: "DEM error", def: 2.0, note: "small-baseline Sentinel-1, height-ambiguity driven" },
    { key: "orbit", label: "Orbit error", def: 1.0, note: "precise orbit products (POEORB)" },
    { key: "atmos", label: "Atmospheric delay (troposphere)", def: 6.0, note: "dominant in humid/relief terrain" },
    { key: "decor", label: "Decorrelation noise", def: 2.0, note: "coherence-dependent" },
    { key: "incidence", label: "Incidence angle error", def: 1.5, note: "geometry projection error" },
  ];

  /** 正交合成：返回 { total, items:[{key,label,value,share}] }，share 为百分比 */
  function combine(values) {
    var sq = values.map(function (v) { return v * v; });
    var sum = sq.reduce(function (a, b) { return a + b; }, 0);
    var items = values.map(function (v, i) {
      return {
        key: SOURCES[i].key, label: SOURCES[i].label,
        value: round2(v), share: sum ? round2(100 * sq[i] / sum) : 0,
      };
    });
    return { total: round2(Math.sqrt(sum)), items: items };
  }

  /** Markdown 摘要（评审用，克制措辞） */
  function summary(c, unit) {
    var lines = [
      "InSAR error budget (screening-level, " + unit + "):",
      "combined 1σ uncertainty σ_total = " + c.total + " " + unit + ".",
      "Contribution shares: " + c.items.map(function (it) {
        return it.label + " " + it.share + "%";
      }).join("; ") + ".",
      "Dominant source: " + c.items.slice().sort(function (a, b) { return b.share - a.share; })[0].label
        + ". Values are screening defaults — refine with project-specific processing parameters before formal use.",
    ];
    return lines.join(" ");
  }

  function round2(x) { return Math.round(x * 100) / 100; }

  global.ErrorBudget = { SOURCES: SOURCES, combine: combine, summary: summary };
})(window);
