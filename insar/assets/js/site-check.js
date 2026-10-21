/**
 * insar-geosettle — 工具 2 内核：场址适宜性预检（文档 4.1-2，招牌差异化工具）
 *
 * 评分模型（0–100，四分项加权）：
 *   相干性预期 ×0.40 ｜几何风险(叠掩/阴影) ×0.30 ｜大气干扰 ×0.20 ｜目标形变适配 ×0.10
 * ⚠️ 模型性质：筛查级启发式，权重与基础分透明可调；
 *    输出仅为前期可行性初筛，不替代正式 InSAR 可行性研究。
 */
(function (global) {
  "use strict";

  var WEIGHTS = { coherence: 0.4, geometry: 0.3, atmosphere: 0.2, fit: 0.1 };

  /** 地表覆盖基础相干性分（C 波段参考；L 波段穿透更强另加成） */
  var COVER = {
    urban:  { label: "Urban / built-up", base: 90 },
    bare:   { label: "Bare rock / desert", base: 85 },
    grass:  { label: "Grassland / shrubland", base: 65 },
    cropland: { label: "Cropland", base: 55 },
    forest: { label: "Forest", base: 30 },
    water:  { label: "Water / wetland", base: 5 },
    snow:   { label: "Snow / ice", base: 15 },
  };

  var CLIMATE = { arid: { label: "Arid", base: 90 }, temperate: { label: "Temperate", base: 70 }, tropical: { label: "Tropical / humid", base: 40 } };

  var clamp = function (x) { return Math.max(0, Math.min(100, x)); };
  var round1 = function (x) { return Math.round(x * 10) / 10; };

  /**
   * 评分主函数。
   * input: { cover, sensor('C'|'L'), relief(°), climate, target('slow'|'seasonal'|'rapid'), bbox:[w,s,e,n] }
   */
  function score(input) {
    var flags = [];

    /* 1. 相干性预期 */
    var cov = COVER[input.cover];
    var coh = cov.base;
    if (input.sensor === "L") {           // L 波段穿透植被
      coh += input.cover === "forest" ? 25 : input.cover === "cropland" ? 15 : input.cover === "grass" ? 10 : 0;
    }
    coh -= Math.max(0, input.relief - 15) * 0.5;   // 高起伏局部几何失相干
    coh = clamp(coh);

    /* 2. 几何风险（叠掩/阴影，与坡度和入射角关系） */
    var inc = input.sensor === "L" ? 34 : 38;      // 典型入射角
    var geo = clamp(100 - Math.max(0, input.relief - 10) * 3);
    if (input.relief > inc - 8) {
      geo = Math.min(geo, 20);
      flags.push("Severe layover/shadow risk: max slope (" + input.relief + "°) approaches incidence angle (" + inc + "°). Check both ascending and descending tracks and local incidence maps.");
    }

    /* 3. 大气干扰 */
    var atm = clamp(CLIMATE[input.climate].base - input.relief * 0.5);
    if (input.climate === "tropical" && input.relief > 15) {
      flags.push("Tropical humidity combined with high relief: expect strong atmospheric phase screens; consider GNSS-based or weather-model correction (e.g., GACOS / ERA5).");
    }

    /* 4. 目标形变适配 */
    var fit = input.target === "slow" ? 85 : input.target === "seasonal" ? 80 : 70;

    var sub = { coherence: round1(coh), geometry: round1(geo), atmosphere: round1(atm), fit: fit };
    var total = round1(
      sub.coherence * WEIGHTS.coherence + sub.geometry * WEIGHTS.geometry
      + sub.atmosphere * WEIGHTS.atmosphere + sub.fit * WEIGHTS.fit);

    /* 红线预警 */
    if (input.cover === "water") { flags.push("RED FLAG: open water / wetland has negligible coherent returns — InSAR point targets unavailable. Interpret banks/structures only."); }
    if (input.cover === "snow") { flags.push("RED FLAG: seasonal snow/ice cover destroys temporal coherence for most of the year."); }
    if (input.cover === "forest" && input.sensor === "C") {
      flags.push("RED FLAG: dense forest with C-band (Sentinel-1) → severe volume decorrelation. Strongly consider L-band (ALOS-2/ALOS-4) or accept sparse PS coverage.");
    }

    return { total: total, sub: sub, flags: flags, class: total >= 75 ? "Good" : total >= 50 ? "Moderate" : "Poor" };
  }

  /** 算法 / 传感器 / 轨道推荐 */
  function recommend(r, input) {
    var algo, sensor, orbit;
    if (input.target === "rapid") {
      algo = "DInSAR (per-pair) supplemented by SBAS for the overall series";
    } else if (r.sub.coherence >= 70) {
      algo = "PS-InSAR (persistent scatterer) primary; SBAS cross-check";
    } else if (r.sub.coherence >= 50) {
      algo = "SBAS (small baseline subset); DS-InSAR if SLC archive allows";
    } else {
      algo = "DS-InSAR (distributed scatterer) with L-band data preferred";
    }
    sensor = (input.cover === "forest" || input.cover === "cropland")
      ? "ALOS-2 / ALOS-4 L-band preferred (vegetation penetration); Sentinel-1 C-band as free supplementary"
      : "Sentinel-1 C-band (free, 12-day) is sufficient; ALOS-2 optional for finer pixels";
    orbit = "Process both ascending and descending tracks — single-track geometry cannot separate vertical from along-slope motion.";
    return { algo: algo, sensor: sensor, orbit: orbit };
  }

  /** HyP3 任务参数包（一键复制到 ASF HyP3） */
  function hyp3Package(input) {
    var b = input.bbox;   // [w,s,e,n]
    return [
      "HyP3 job package (paste into ASF Vertex batch script or SDK):",
      'job_type: INSAR_GUNW (baseline pairs) + RTC_GAMMA (ancillary)',
      "reference_frame: Sentinel-1 A/B, both ascending & descending",
      "bbox: [" + b.join(", ") + "]  (W, S, E, N)",
      "weather_model: ERA5 (if available) — atmospheric phase correction",
      "dem_name: copernicus_glo_30",
      "NOTE: adjust bbox order/encoding to the HyP3 SDK schema of your account version.",
    ].join("\n");
  }

  global.SiteCheck = { WEIGHTS: WEIGHTS, COVER: COVER, CLIMATE: CLIMATE, score: score, recommend: recommend, hyp3Package: hyp3Package };
})(window);
