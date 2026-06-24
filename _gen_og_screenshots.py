"""Batch generate OG screenshots for new languages (fr/vi/ar).
Takes 1200x630 screenshots of each tool page from smartimgkit.com.
V2: uses domcontentloaded (faster), reuses a single page.
"""
import json, os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "https://smartimgkit.com"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
VIEWPORT = {"width": 1200, "height": 630}
LANGUAGES = ["fr", "vi", "ar"]

def load_tools():
    with open(Path(__file__).parent / "_tools_data.json", encoding="utf-8") as f:
        data = json.load(f)
    return [t["slug"] for t in data["tools"]]

def main():
    tools = load_tools()
    total = len(tools) * len(LANGUAGES)
    print(f"Tools: {len(tools)}, Languages: {LANGUAGES}, Total: {total}")

    SCREENSHOTS_DIR.mkdir(exist_ok=True, parents=True)

    done = 0; skipped = 0; failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()

        for lang in LANGUAGES:
            print(f"\n--- {lang} ---")
            for slug in tools:
                out_path = SCREENSHOTS_DIR / f"{lang}-{slug}.png"
                if out_path.exists() and out_path.stat().st_size > 1000:
                    skipped += 1; done += 1
                    continue

                url = f"{BASE_URL}/{lang}/tools/{slug}"
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    page.wait_for_timeout(800)  # let fonts/icons render
                    page.screenshot(path=str(out_path), full_page=False)
                    size_kb = out_path.stat().st_size // 1024
                    done += 1
                    if done % 10 == 0:
                        print(f"  [{done}/{total}] {lang}/{slug} ({size_kb}KB)")
                except Exception as e:
                    failed += 1; done += 1
                    print(f"  [{done}/{total}] FAIL {lang}/{slug}: {str(e)[:60]}")

        page.close()
        browser.close()

    print(f"\nDONE: {done} total, {skipped} skipped, {failed} failed")

if __name__ == "__main__":
    main()
