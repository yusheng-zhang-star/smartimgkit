# -*- coding: utf-8 -*-
"""Emit compact JS array of report rows for embedding into HTML report"""
import json, io, os

base = r"E:\网站项目\smartimgkit\_test_files"
with io.open(os.path.join(base, "report_rows.json"), encoding="utf-8") as f:
    rows = json.load(f)

# sort: kind (tools first), category, slug
def sort_key(r):
    ki = 0 if r["kind"] == "tool" else 1
    ci = {"图片工具": 0, "PDF工具": 1, "视频工具": 2, "文本工具": 3, "工作流": 4}[r["cat"]]
    return (ki, ci, r["slug"])

rows.sort(key=sort_key)

# Build compact JS: [cat, kind, slug, verdict, errorText]
lines = []
for r in rows:
    errs = r.get("errors") or []
    # pick the most meaningful error text (first non-trivial)
    etxt = ""
    for e in errs:
        t = e
        if t.startswith("[C]") and ("adsbygoogle" in t or "googlesyndication" in t or "doubleclick" in t):
            continue
        t = t.replace("'", "\\'").replace('"', '\\"')
        etxt = t[:120]
        break
    vmap = {"ok": "OK", "bug": "BUG", "cdn": "CDN", "minor": "MIN", "other": "FLG"}
    lines.append('["%s","%s","%s","%s","%s"]' % (r["cat"], r["kind"], r["slug"], vmap[r["v"]], etxt))

js = "[\n" + ",\n".join(lines) + "\n]"
with io.open(os.path.join(base, "report_data.js"), "w", encoding="utf-8") as f:
    f.write(js)
print("rows:", len(lines))
