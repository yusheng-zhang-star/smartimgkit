/**
 * insar-geosettle — CSV / Excel 粘贴解析与表头自动识别（文档 5.1、8.5）
 *
 * 支持：逗号/分号/Tab 分隔、Excel 直接复制粘贴、常见软件表头同义词
 * 识别失败时抛出带具体诊断信息的 Error（对接 8.5 友好报错）
 */
(function (global) {
  "use strict";

  /** 表头同义词表（兼容 MintPy / LiCSBAS / insarmaps / GNSS 导出） */
  var SYNONYMS = {
    point_id: ["point_id", "point", "id", "name", "ps_id"],
    lon: ["lon", "longitude", "lng"],
    lat: ["lat", "latitude"],
    easting: ["easting", "utm_e", "x_utm", "e"],
    northing: ["northing", "utm_n", "y_utm", "n"],
    los_vel: ["los_vel", "los_velocity", "los velocity", "velocity", "mean_velocity", "vel", "v_los", "defo"],
    incidence_angle: ["incidence_angle", "incidence", "look_angle", "inc_angle"],
    azimuth: ["azimuth", "los_azimuth", "az", "heading", "track"],
    slope: ["slope", "slope_angle"],
    aspect: ["aspect", "aspect_angle", "slope_aspect"],
    vertical_vel_gnss: ["vertical_vel_gnss", "vertical_velocity", "gnss_vel", "up_vel"],
    gnss_accuracy: ["gnss_accuracy", "accuracy", "sigma"],
    displacement_mm: ["displacement_mm", "displacement", "cumulative_mm", "deformation_mm"],
    date: ["date", "date_end", "time", "acquisition"],
  };

  /** 探测分隔符：在首行取 , ; \t 中出现次数最多且一致者 */
  function detectDelimiter(line) {
    var counts = { ",": (line.match(/,/g) || []).length, ";": (line.match(/;/g) || []).length, "\t": (line.match(/\t/g) || []).length };
    var best = ",", bestN = 0;
    Object.keys(counts).forEach(function (d) {
      if (counts[d] > bestN) { best = d; bestN = counts[d]; }
    });
    return best;
  }

  /** 解析 CSV/TSV 文本 → { fields, rows }（数值列自动转 Number） */
  function parse(text) {
    if (!text || !text.trim()) { throw new Error("Empty input"); }
    // 跳过 # 注释行
    var lines = text.split(/\r?\n/).filter(function (l) { return l.trim() && l[0] !== "#"; });
    var delim = detectDelimiter(lines[0]);
    var headers = lines[0].split(delim).map(function (h) { return h.trim().toLowerCase(); });

    var rows = lines.slice(1).map(function (line) {
      var cells = line.split(delim);
      var obj = {};
      headers.forEach(function (h, i) { obj[h] = (cells[i] || "").trim(); });
      return obj;
    });

    // 数值化：能转的列都转 Number
    var sample = rows[0];
    Object.keys(sample).forEach(function (k) {
      var v = sample[k];
      if (v !== "" && !isNaN(Number(v))) {
        rows.forEach(function (r) { r[k] = Number(r[k]); });
      }
    });

    if (!rows.length) { throw new Error("No data rows detected below header"); }
    return { fields: headers, rows: rows, delimiter: delim };
  }

  /**
   * 标准 InSAR 字段自动匹配。
   * 返回 { lon, lat, los_vel, ... } → 实际列名；缺关键列时抛出诊断错误（文档 8.5 格式）
   */
  function matchFields(fields, required) {
    var map = {};
    Object.keys(SYNONYMS).forEach(function (std) {
      SYNONYMS[std].forEach(function (syn) {
        if (fields.indexOf(syn) !== -1 && map[std] === undefined) { map[std] = syn; }
      });
    });
    var missing = (required || []).filter(function (k) { return !map[k]; });
    if (missing.length) {
      throw new Error("Detected: missing column(s) [" + missing.join(", ")
        + "] → Fix: re-export from your InSAR software including these fields. See /docs/csv-format-spec.html");
    }
    return map;
  }

  global.CSVUtils = { parse: parse, matchFields: matchFields };
})(window);
