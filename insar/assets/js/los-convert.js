/**
 * insar-geosettle — 工具 1：LOS → Vertical & Horizontal Converter（文档 4.1-1）
 *
 * 几何模型（单轨）：
 *   v_los = v_vertical · cos(θ) + u_slope · sin(θ) · cos(δ − α)
 *   θ=入射角  δ=坡向(下坡方位)  α=LOS 水平投影方位角
 *   单轨观测一个方程解两个未知数，故提供两种工程假设：
 *     A. 纯垂直假设:   v_v = v_los / cos θ           （默认，行业惯例）
 *     B. 纯沿坡假设:   u_s = v_los / [sin θ · cos(δ−α)]
 *   |cos(δ−α)| 小于阈值时沿坡分量不可观测，自动给出不可靠标记。
 * 误差估算（一阶泰勒）：d(v_v) = |v_los · tan θ| · dθ(rad)
 *
 * 约定：v_los < 0 表示远离卫星（沉降），输出单位 mm/yr。
 */
(function (global) {
  "use strict";

  var D2R = Math.PI / 180;

  /** 单点计算：返回垂直/沿坡估计与误差项 */
  function computePoint(p) {
    var los = p.los_vel, th = p.incidence_angle * D2R, az = p.azimuth;
    var slope = p.slope || 0, asp = p.aspect || 0;

    var vV = los / Math.cos(th);                       // A. 纯垂直假设
    var f = Math.sin(th) * Math.cos((asp - az) * D2R); // 沿坡→LOS 投影系数
    var uS = Math.abs(f) > 0.15 ? los / f : null;      // B. 纯沿坡假设（|f| 太小不可观测）
    var dInc = (p.d_incidence || 0.5) * D2R;
    var dVV = Math.abs(los * Math.tan(th)) * dInc;     // 入射角误差传递

    return {
      vertical_vel: round2(vV),
      slope_factor: round4(f),
      slope_vel: uS === null ? null : round2(uS),
      slope_reliable: uS !== null,
      vertical_err: round2(dVV),
    };
  }

  function round2(x) { return Math.round(x * 100) / 100; }
  function round4(x) { return Math.round(x * 10000) / 10000; }

  global.LOSConvert = { computePoint: computePoint };
})(window);
