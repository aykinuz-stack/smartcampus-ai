#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soru dosyalarını bilgi_yarismasi_game.py'ye birleştir."""
import pathlib

base = pathlib.Path(__file__).parent

# Soru dosyalarını oku
ilkokul = base.joinpath("_by_ilkokul.txt").read_text(encoding="utf-8").strip()
ortaokul = base.joinpath("_by_ortaokul.txt").read_text(encoding="utf-8").strip()
lise = base.joinpath("_by_lise.txt").read_text(encoding="utf-8").strip()

# bilgi_yarismasi_game.py oku
game_file = base.joinpath("bilgi_yarismasi_game.py")
content = game_file.read_text(encoding="utf-8")

# Placeholder'ları değiştir
content = content.replace("__ILKOKUL_PLACEHOLDER__", ilkokul)
content = content.replace("__ORTAOKUL_PLACEHOLDER__", ortaokul)
content = content.replace("__LISE_PLACEHOLDER__", lise)

game_file.write_text(content, encoding="utf-8")
print("OK — bilgi_yarismasi_game.py güncellendi")

# Doğrulama
import re
for label, placeholder in [("İlkokul", "__ILKOKUL_PLACEHOLDER__"),
                             ("Ortaokul", "__ORTAOKUL_PLACEHOLDER__"),
                             ("Lise", "__LISE_PLACEHOLDER__")]:
    if placeholder in content:
        print(f"  HATA: {label} placeholder hala duruyor!")
    else:
        matches = len(re.findall(r'\{k:"[^"]+",s:"[^"]+"', content))
        print(f"  {label}: placeholder değiştirildi")

# Toplam soru sayısı
total = len(re.findall(r'\{k:"[^"]+",s:"[^"]+"', content))
print(f"  Toplam soru: {total}")
