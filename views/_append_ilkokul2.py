#!/usr/bin/env python3
"""Append final 10 ilkokul questions"""
import os

questions = [
'{k:"Spor",s:"Hangi spor dalinda top kullanilmaz?",o:["Futbol","Basketbol","Yuzme","Voleybol"],d:2,a:"Yuzme sporunda top kullanilmaz."}',
'{k:"Spor",s:"Hentbolda bir takimda kac oyuncu sahadad\u0131r?",o:["5","6","7","8"],d:2,a:"Hentbolda her tak\u0131mdan 7 oyuncu sahada bulunur."}',
'{k:"Spor",s:"Bisiklet yarisi hangi spor dalina girer?",o:["Atletizm","Cimnastik","Bisiklet","Yuzme"],d:2,a:"Bisiklet yarisi bisiklet sporu dalindadir."}',
'{k:"Spor",s:"Hangi spor dalinda buz uzerinde kayilir?",o:["Kayak","Buz pateni","Snowboard","Curling"],d:1,a:"Buz pateni buz uzerinde kayilarak yapilan bir spordur."}',
'{k:"T\u00fcrkiye",s:"Truva Antik Kenti hangi ildedir?",o:["Balikesir","Canakkale","Bursa","Tekirdag"],d:1,a:"Truva Antik Kenti Canakkale ilinde yer alir."}',
'{k:"T\u00fcrkiye",s:"Uzungol hangi ildedir?",o:["Rize","Artvin","Trabzon","Giresun"],d:2,a:"Uzungol Trabzon ilinin Caykara ilcesindedir."}',
'{k:"T\u00fcrkiye",s:"Turkiye de en cok uretilen tarim urunu hangisidir?",o:["Bugday","Misir","Pamuk","Findik"],d:0,a:"Bugday Turkiye de en cok uretilen tarim urunlerinden biridir."}',
'{k:"T\u00fcrkiye",s:"Anıtkabir hangi ildedir?",o:["Istanbul","Ankara","Izmir","Bursa"],d:1,a:"Ataturk un mozolesi Anitkabir Ankara dadır."}',
'{k:"T\u00fcrkiye",s:"Turkiye nin en batisindaki il hangisidir?",o:["Izmir","Canakkale","Edirne","Mugla"],d:2,a:"Edirne Turkiye nin en batisindaki ildir."}',
'{k:"T\u00fcrkiye",s:"Karain Magarasi hangi ildedir?",o:["Burdur","Isparta","Antalya","Mersin"],d:2,a:"Karain Magarasi Antalya dadır ve Anadolunun en eski yerlesimlerinden biridir."}',
]

filepath = os.path.join("c:", os.sep, "Users", "safir", "OneDrive", "Masaüstü", "SmartCampusAI", "views", "_by_ilkokul.txt")

with open(filepath, "a", encoding="utf-8") as f:
    for q in questions:
        f.write(q + "\n")

with open(filepath, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip().startswith("{k:")]
    print(f"Total: {len(lines)}")
    cats = {}
    for l in lines:
        cat = l.split('"')[1]
        cats[cat] = cats.get(cat, 0) + 1
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")
