# -*- coding: utf-8 -*-
"""MEB-aligned English curriculum data for Preschool (Grade 0 / Ages 4-6).

Preschool English focuses on language awareness through songs, games,
colours, numbers, and play-based learning. 36 weekly entries.

10 Units (aligned with content banks):
  1. Greetings (w1-4)      2. Colours (w5-8)       3. Numbers (w9-12)
  4. Weather (w13-16)       5. Toys & Party (w17-20) 6. Farm Animals (w21-24)
  7. Seasons (w25-27)       8. Beach & Nature (w28-30) 9. Community Helpers (w31-33)
  10. Goodbye & Review (w34-36)
"""

from __future__ import annotations


def _week(w, theme, theme_tr, vocab, structure, skills, categories=None):
    """Helper to build a consistent week entry."""
    return {
        "week": w,
        "theme": theme,
        "theme_tr": theme_tr,
        "vocab": vocab,
        "structure": structure,
        "skills": skills or {},
        "linked_content": {"categories": categories or []},
    }


CURRICULUM_PRESCHOOL = [
    # ── Unit 1: Greetings (Weeks 1-4) ──
    _week(1, "Greetings", "Selamlasma", ["hello", "hi", "bye", "friend", "name"],
          "Hello! What's your name?", {"listening": "Merhaba sarkisini dinler.", "speaking": "Merhaba der, adini soyler."}, ["Selamlasma"]),
    _week(2, "My Body", "Vucudum", ["head", "eyes", "nose", "mouth", "hands"],
          "Touch your nose!", {"listening": "Vucut sarkisini dinler.", "speaking": "Vucut bolumlerini gosterir."}, ["Vucut"]),
    _week(3, "Family", "Aile", ["mummy", "daddy", "baby", "sister", "brother"],
          "This is my mummy.", {"listening": "Aile sarkisini dinler.", "speaking": "Aile uyelerini soyler."}, ["Aile"]),
    _week(4, "Shapes", "Sekiller", ["circle", "square", "triangle", "star", "heart"],
          "Circle! Star!", {"listening": "Sekil sarkisini dinler.", "speaking": "Sekilleri isimlendirir."}, ["Sekiller"]),

    # ── Unit 2: Colours (Weeks 5-8) ──
    _week(5, "Colours", "Renkler", ["red", "blue", "yellow", "green", "orange"],
          "Red! Blue! What colour?", {"listening": "Renk sarkisini dinler.", "speaking": "Renkleri soyler."}, ["Renkler"]),
    _week(6, "More Colours", "Daha Fazla Renk", ["pink", "purple", "brown", "black", "white"],
          "It's pink!", {"listening": "Renk sarkisini dinler.", "speaking": "Yeni renkleri soyler."}, ["Renkler"]),
    _week(7, "Big & Small", "Buyuk ve Kucuk", ["big", "small", "tall", "short", "long"],
          "Big! Small!", {"listening": "Zitlik sarkisini dinler.", "speaking": "Zitliklari gosterir."}, ["Kavramlar"]),
    _week(8, "Fruit", "Meyveler", ["apple", "banana", "orange", "grape", "strawberry"],
          "I like apples!", {"listening": "Meyve sarkisini dinler.", "speaking": "Meyve isimlerini soyler."}, ["Yiyecekler"]),

    # ── Unit 3: Numbers (Weeks 9-12) ──
    _week(9, "Numbers", "Sayilar", ["one", "two", "three", "four", "five"],
          "One, two, three!", {"listening": "Sayma sarkisini dinler.", "speaking": "1-5 sayar."}, ["Sayilar"]),
    _week(10, "Numbers 6-10", "Sayilar 6-10", ["six", "seven", "eight", "nine", "ten"],
          "Six, seven, eight, nine, ten!", {"listening": "Sayma sarkisini dinler.", "speaking": "6-10 sayar."}, ["Sayilar"]),
    _week(11, "Feelings", "Duygular", ["happy", "sad", "angry", "scared", "sleepy"],
          "I'm happy!", {"listening": "Duygu sarkisini dinler.", "speaking": "Nasil hissettigini gosterir."}, ["Duygular"]),
    _week(12, "Review 1", "Tekrar 1", ["hello", "colours", "numbers", "body", "animals"],
          "Let's play!", {"listening": "Oyun talimatlarini dinler.", "speaking": "Ogrenilenleri tekrarlar."}, ["Tekrar"]),

    # ── Unit 4: Weather (Weeks 13-16) ──
    _week(13, "Weather", "Hava Durumu", ["sun", "rain", "cloud", "wind", "snow"],
          "It's sunny!", {"listening": "Hava sarkisini dinler.", "speaking": "Havayi soyler."}, ["Hava"]),
    _week(14, "Clothes", "Giysiler", ["shirt", "shoes", "hat", "coat", "socks"],
          "I'm wearing shoes.", {"listening": "Giysi sarkisini dinler.", "speaking": "Giysilerini soyler."}, ["Giysiler"]),
    _week(15, "Food & Drink", "Yiyecek Icecek", ["milk", "water", "bread", "cheese", "cake"],
          "Milk please!", {"listening": "Yemek sarkisini dinler.", "speaking": "Istedigini soyler."}, ["Yiyecekler"]),
    _week(16, "Actions", "Hareketler", ["run", "jump", "clap", "dance", "sit"],
          "Jump! Clap!", {"listening": "Hareket sarkisini dinler.", "speaking": "Hareketleri yapar."}, ["Hareketler"]),

    # ── Unit 5: Toys & Party (Weeks 17-20) ──
    _week(17, "Toys & Party", "Oyuncaklar ve Parti", ["ball", "doll", "car", "teddy", "puzzle"],
          "I have a ball.", {"listening": "Oyuncak sarkisini dinler.", "speaking": "Oyuncagini gosterir."}, ["Oyuncaklar"]),
    _week(18, "Party Time", "Parti Zamani", ["party", "cake", "balloon", "dance", "fun"],
          "Happy party!", {"listening": "Parti sarkisini dinler.", "speaking": "Parti kelimelerini kullanir."}, ["Kutlama"]),
    _week(19, "Review & Songs", "Tekrar ve Sarkilar", ["all previous words"],
          "Let's sing!", {"listening": "Tum sarkilari dinler.", "speaking": "Sarkilara katilir."}, ["Tekrar"]),
    _week(20, "In the House", "Evde", ["door", "window", "bed", "table", "chair"],
          "Open the door!", {"listening": "Ev sarkisini dinler.", "speaking": "Ev esyalarini soyler."}, ["Ev"]),

    # ── Unit 6: Farm Animals (Weeks 21-24) ──
    _week(21, "Farm Animals", "Ciftlik Hayvanlari", ["cow", "sheep", "horse", "chicken", "pig"],
          "Moo! Baa!", {"listening": "Ciftlik sarkisini dinler.", "speaking": "Hayvan seslerini taklit eder."}, ["Hayvanlar"]),
    _week(22, "Animals", "Hayvanlar", ["cat", "dog", "bird", "fish", "rabbit"],
          "Cat! Dog! What animal?", {"listening": "Hayvan seslerini dinler.", "speaking": "Hayvan isimlerini soyler."}, ["Hayvanlar"]),
    _week(23, "In the Garden", "Bahcede", ["flower", "tree", "grass", "butterfly", "bee"],
          "I see a flower!", {"listening": "Bahce sarkisini dinler.", "speaking": "Dogayi gosterir."}, ["Doga"]),
    _week(24, "Transport", "Ulasim", ["car", "bus", "bike", "train", "plane"],
          "I go by car.", {"listening": "Ulasim sarkisini dinler.", "speaking": "Araclari isimlendirir."}, ["Ulasim"]),

    # ── Unit 7: Seasons (Weeks 25-27) ──
    _week(25, "Seasons", "Mevsimler", ["spring", "summer", "autumn", "winter", "season"],
          "It's summer!", {"listening": "Mevsim sarkisini dinler.", "speaking": "Mevsimleri soyler."}, ["Mevsimler"]),
    _week(26, "Days", "Gunler", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "Today is Monday!", {"listening": "Gun sarkisini dinler.", "speaking": "Gunleri soyler."}, ["Zaman"]),
    _week(27, "Review & Games", "Tekrar ve Oyunlar", ["all words"],
          "Let's play a game!", {"listening": "Oyun kurallarini dinler.", "speaking": "Oyun oynar."}, ["Tekrar"]),

    # ── Unit 8: Beach & Nature (Weeks 28-30) ──
    _week(28, "Beach & Nature", "Sahil ve Doga", ["sand", "sea", "shell", "bucket", "sunglasses"],
          "I play in the sand!", {"listening": "Sahil sarkisini dinler.", "speaking": "Sahil kelimelerini kullanir."}, ["Tatil"]),
    _week(29, "My Room", "Odam", ["bed", "toy box", "lamp", "pillow", "blanket"],
          "This is my bed.", {"listening": "Oda sarkisini dinler.", "speaking": "Odasini anlatir."}, ["Ev"]),
    _week(30, "Food Likes", "Sevdiklerim", ["like", "don't like", "yummy", "yucky", "favourite"],
          "I like cake! Yummy!", {"listening": "Yemek sarkisini dinler.", "speaking": "Sevdigini soyler."}, ["Yiyecekler"]),

    # ── Unit 9: Community Helpers (Weeks 31-33) ──
    _week(31, "Community Helpers", "Yardimcilar", ["doctor", "teacher", "police", "fire fighter", "cook"],
          "She is a doctor.", {"listening": "Meslek sarkisini dinler.", "speaking": "Meslekleri soyler."}, ["Meslekler"]),
    _week(32, "Sports", "Sporlar", ["football", "swimming", "running", "jumping", "dancing"],
          "I like football!", {"listening": "Spor sarkisini dinler.", "speaking": "Sporlarini soyler."}, ["Spor"]),
    _week(33, "Review & Stories", "Tekrar ve Hikayeler", ["story", "book", "read", "picture", "page"],
          "Read me a story!", {"listening": "Kisa hikaye dinler.", "speaking": "Hikayeyi tekrarlar."}, ["Tekrar"]),

    # ── Unit 10: Goodbye & Review (Weeks 34-36) ──
    _week(34, "Goodbye & Review", "Hosca Kal ve Tekrar", ["favourite", "best", "love", "colour", "animal"],
          "My favourite colour is blue!", {"listening": "Tercih cumlelerini dinler.", "speaking": "Tercihlerini soyler."}, ["Kisisel"]),
    _week(35, "Show Time", "Gosteri Zamani", ["show", "sing", "dance", "act", "clap"],
          "Let's put on a show!", {"listening": "Gosteri sarkisini dinler.", "speaking": "Sahnede performans gosterir."}, ["Kutlama"]),
    _week(36, "Goodbye Song", "Hosca Kal Sarkisi", ["goodbye", "summer", "holiday", "see you", "miss you"],
          "Goodbye! See you!", {"listening": "Veda sarkisini dinler.", "speaking": "Veda eder."}, ["Veda"]),
]
