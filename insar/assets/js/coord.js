/**
 * insar-geosettle — 工具 7 内核：批量坐标转换（文档 4.1-7，proj4js 封装）
 * 禁止手写投影公式（文档 13.1）——全部经 proj4js。
 */
(function (global) {
  "use strict";

  var D2R = Math.PI / 180;

  /** 经度 → UTM 分带号（1–60） */
  function zoneOf(lon) {
    return Math.floor((lon + 180) / 6) + 1;
  }

  /** proj4 UTM 定义（WGS84；南半球加 +south） */
  function utmDef(zone, south) {
    return "+proj=utm +zone=" + zone + (south ? " +south" : "") + " +datum=WGS84 +units=m +no_defs";
  }

  /** WGS84 → UTM：返回 { zone, easting, northing, south } */
  function toUTM(lon, lat) {
    var zone = zoneOf(lon), south = lat < 0;
    var p = proj4("WGS84", utmDef(zone, south), [lon, lat]);
    return { zone: zone, south: south, easting: round2(p[0]), northing: round2(p[1]) };
  }

  /** UTM → WGS84（须指定分带与半球）：返回 { lon, lat } */
  function toLonLat(zone, south, easting, northing) {
    var p = proj4(utmDef(zone, south), "WGS84", [easting, northing]);
    return { lon: round6(p[0]), lat: round6(p[1]) };
  }

  /** GeoJSON FeatureCollection（Point）批量转 UTM */
  function geojsonToUTM(gj) {
    var out = [];
    (gj.features || []).forEach(function (f) {
      if (f.geometry && f.geometry.type === "Point") {
        var r = toUTM(f.geometry.coordinates[0], f.geometry.coordinates[1]);
        out.push({ lon: f.geometry.coordinates[0], lat: f.geometry.coordinates[1],
          easting: r.easting, northing: r.northing, zone: r.zone, props: f.properties || {} });
      }
    });
    return out;
  }

  function round2(x) { return Math.round(x * 100) / 100; }
  function round6(x) { return Math.round(x * 1e6) / 1e6; }

  global.CoordTool = { zoneOf: zoneOf, toUTM: toUTM, toLonLat: toLonLat, geojsonToUTM: geojsonToUTM, utmDef: utmDef };
})(window);
