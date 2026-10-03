# -*- coding: utf-8 -*-
"""Compute per-category stats + final verdicts from clean_e2e_results.json"""
import json, io, os

base = r"E:\网站项目\smartimgkit\_test_files"
with io.open(os.path.join(base, "clean_e2e_results.json"), encoding="utf-8") as f:
    results = json.load(f)

# Final verdict overrides based on deep verification (test artifacts / env issues resolved)
FINAL_OK = {
    "pdf-delete-pages": "ok", "pdf-extract-pages": "ok", "pdf-rotate": "ok",
    "signature-maker": "ok", "pdf-annotate": "ok", "pdf-compress": "ok",
    "pdf-redact": "ok", "text-on-image": "ok", "compressor": "ok", "watermark": "ok",
}
FINAL_CDN = {"image-upscaler": "cdn", "ocr": "cdn", "product-white-background": "cdn",
             "pdf-to-images": "cdn"}
FINAL_BUG = {"image-rotator": "bug", "before-after-comparison": "bug", "gif-maker": "bug"}
FINAL_MINOR = {"color-palette-extractor": "minor"}

TEXT_TOOLS = {"base64","case-converter","html-encoder","url-encoder","json-formatter",
  "regex-tester","text-diff","text-find-replace","text-sorter","uuid-generator",
  "password-generator","word-counter","csv-to-pdf","excel-to-pdf","txt-to-pdf"}

def cat(slug, kind):
    if kind == "workflow":
        return "工作流"
    if slug.startswith("pdf-") or slug.endswith("-to-pdf"):
        return "PDF工具"
    if slug.startswith("video-"):
        return "视频工具"
    if slug in TEXT_TOOLS:
        return "文本工具"
    return "图片工具"

def verdict(r):
    slug = r["slug"]
    if slug in FINAL_OK:
        return "ok"
    if slug in FINAL_BUG:
        return "bug"
    if slug in FINAL_CDN:
        return "cdn"
    if slug in FINAL_MINOR:
        return "minor"
    if r["status"] == "PASS":
        return "ok"
    return "other"

cats = {}
rows = []
for r in results:
    c = cat(r["slug"], r["kind"])
    v = verdict(r)
    cats.setdefault(c, {"ok": 0, "bug": 0, "cdn": 0, "minor": 0, "other": 0})
    cats[c][v] += 1
    rows.append({"cat": c, "kind": r["kind"], "slug": r["slug"], "v": v,
                 "errors": r.get("errors", [])})

print("CATEGORY STATS:")
for c, d in sorted(cats.items()):
    tot = sum(d.values())
    print(f"  {c}: total={tot} ok={d['ok']} bug={d['bug']} cdn={d['cdn']} minor={d['minor']} other={d['other']}")

tot_ok = sum(d["ok"] for d in cats.values())
tot_bug = sum(d["bug"] for d in cats.values())
tot_cdn = sum(d["cdn"] for d in cats.values())
tot_minor = sum(d["minor"] for d in cats.values())
tot_other = sum(d["other"] for d in cats.values())
print(f"\nTOTAL ok={tot_ok} bug={tot_bug} cdn={tot_cdn} minor={tot_minor} other={tot_other} = {tot_ok+tot_bug+tot_cdn+tot_minor+tot_other}")

with io.open(os.path.join(base, "report_rows.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
with io.open(os.path.join(base, "report_cats.json"), "w", encoding="utf-8") as f:
    json.dump(cats, f, ensure_ascii=False, indent=1)
print("\nsaved report_rows.json / report_cats.json")
