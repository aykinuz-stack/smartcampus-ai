"""Bos JSON dosyalarini [] ile doldur."""
import os, json

fixed = 0
for root, dirs, files in os.walk("data"):
    for f in files:
        if f.endswith(".json"):
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
                if size <= 2:
                    with open(path, "r", encoding="utf-8") as fh:
                        content = fh.read().strip()
                    if content in ("", "[]", "{}", "null"):
                        with open(path, "w", encoding="utf-8") as fh:
                            json.dump([], fh)
                        fixed += 1
                        print(f"FIXED: {path}")
            except Exception as e:
                print(f"ERROR: {path} — {e}")

print(f"\nToplam {fixed} dosya duzeltildi.")
