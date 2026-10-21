/**
 * insar-geosettle — 统一绘图与导出封装（基于 ECharts）
 *
 * 职责：
 *   1. 统一 SVG 渲染器初始化（矢量导出是核心交付卖点）
 *   2. exportSVG   —— 序列化当前图表为 .svg 文件下载
 *   3. exportPNG300 —— 离屏 Canvas 高像素比重绘，导出 300DPI PNG
 *   4. 统一工程图风格（色弱友好风险色卡、关闭花哨动画）
 *
 * 全部计算在浏览器本地完成，不产生任何网络请求。
 */
(function (global) {
  "use strict";

  /** 全站统一风险色卡（9.1 节，色弱友好） */
  var RISK_COLORS = {
    stable: "#48A969",
    low: "#E6C249",
    moderate: "#E28942",
    high: "#D84A4A",
    critical: "#7C1919",
  };

  /** 300DPI 对应的像素比（浏览器基准 96DPI） */
  var DPI_SCALE = 300 / 96;

  /** 工程图统一基础配置：关闭动画、克制网格线 */
  function baseOption() {
    return {
      animation: false,
      textStyle: { fontFamily: "Inter, system-ui, sans-serif" },
    };
  }

  /** 初始化 SVG 渲染器图表 */
  function render(el, option) {
    var chart = echarts.init(el, null, { renderer: "svg" });
    chart.setOption(merge(baseOption(), option));
    return chart;
  }

  /** 浅合并（工程图配置足够，不引深度合并库） */
  function merge(a, b) {
    var out = {};
    var k;
    for (k in a) { out[k] = a[k]; }
    for (k in b) { out[k] = b[k]; }
    return out;
  }

  /** 触发浏览器下载 */
  function download(blobOrUrl, filename) {
    var a = document.createElement("a");
    if (typeof blobOrUrl === "string") {
      a.href = blobOrUrl;
    } else {
      a.href = URL.createObjectURL(blobOrUrl);
    }
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  /**
   * 导出 SVG。
   * 依赖 SVG 渲染器：从 zrender painter 中取根 <svg> 节点序列化。
   * 返回 svg 字符串（便于自检）；同时触发下载。
   */
  function exportSVG(chart, filename) {
    var painter = chart.getZr().painter;
    var svgEl = null;
    if (painter.getSvgDom) {
      var dom = painter.getSvgDom();
      svgEl = dom && (dom.length ? dom[0] : dom);   // 不同 zrender 版本返回数组或单节点
    } else if (painter.getRoot) {
      svgEl = painter.getRoot();
    }
    if (!svgEl) { throw new Error("SVG painter not found"); }
    var str = new XMLSerializer().serializeToString(svgEl);
    download(new Blob([str], { type: "image/svg+xml" }), filename || "chart.svg");
    return str;
  }

  /**
   * 导出 300DPI PNG。
   * 原理：离屏容器 + Canvas 渲染器 + pixelRatio≈3.125 重绘，再 getDataURL。
   * 返回 dataURL（便于自检）；同时触发下载。
   */
  function exportPNG300(chart, filename) {
    var opt = chart.getOption();
    var size = { width: chart.getWidth(), height: chart.getHeight() };

    var holder = document.createElement("div");
    holder.style.cssText =
      "position:fixed;left:-99999px;top:0;width:" + size.width + "px;height:" + size.height + "px;";
    document.body.appendChild(holder);

    var off = echarts.init(holder, null, { renderer: "canvas", pixelRatio: DPI_SCALE });
    off.setOption(merge(baseOption(), opt));
    var dataURL = off.getDataURL({ type: "png", pixelRatio: DPI_SCALE, backgroundColor: "#fff" });
    off.dispose();
    document.body.removeChild(holder);

    download(dataURL, filename || "chart-300dpi.png");
    return dataURL;
  }

  global.IGCharts = {
    RISK_COLORS: RISK_COLORS,
    render: render,
    exportSVG: exportSVG,
    exportPNG300: exportPNG300,
  };
})(window);
