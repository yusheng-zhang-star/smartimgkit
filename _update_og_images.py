"""Update og_image paths in _tools_data_{LANG}.json to use language-specific screenshots."""
import json
from pathlib import Path

BASE_URL = "https://smartimgkit.com"
LANGUAGES = ["fr", "vi", "ar"]

def main():
    total_updated = 0
    for lang in LANGUAGES:
        data_path = Path(__file__).parent / f"_tools_data_{lang}.json"
        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)

        updated = 0
        for t in data["tools"]:
            slug = t["slug"]
            new_og = f"{BASE_URL}/screenshots/{lang}-{slug}.png"
            old_og = t.get("og_image", "")
            if old_og != new_og:
                t["og_image"] = new_og
                t["twitter_image"] = new_og
                updated += 1

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"{lang}: updated {updated} tools")

    print(f"\nTotal updated: {total_updated}")
    print("Next: run `python _build.py --lang fr/vi/ar` to regenerate HTML pages")

if __name__ == "__main__":
    main()
