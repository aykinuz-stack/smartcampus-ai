# -*- coding: utf-8 -*-
"""Ortaokul (5-8. sinif) 36 haftalik CEFR A2 mufredati.

Her sinif icin:
- 36 haftalik unite/tema plani
- Gunluk ders aktiviteleri (Pzt-Cum)
- Main Course (4 saat) + Skills (4-5 saat) + Native (2 saat) dagitimi
- CEFR A2.1 (5.sinif) -> A2.4 (8.sinif)

Unit grouping (10 units from 36 weeks via build_unit_groups):
  Unit 1: positions 0-3   (weeks 1-4)
  Unit 2: positions 4-7   (weeks 5-8)
  Unit 3: positions 8-11  (weeks 9-12)
  Unit 4: positions 12-15 (weeks 13-16)
  Unit 5: positions 16-19 (weeks 17-20)
  Unit 6: positions 20-23 (weeks 21-24)
  Unit 7: positions 24-26 (weeks 25-27)
  Unit 8: positions 27-29 (weeks 28-30)
  Unit 9: positions 30-32 (weeks 31-33)
  Unit 10: positions 33-35 (weeks 34-36)
"""

# =============================================================================
# 5. SINIF - CEFR A2.1 (Temel Iletisim)
# =============================================================================


# -*- coding: utf-8 -*-
"""Grade 5 & Grade 6 curriculum data (36 weeks each)."""

CURRICULUM_GRADE5 = [
    # ===== UNIT 1: Back to School (Weeks 1-4) =====
    {
        "week": 1,
        "theme": "Back to School",
        "theme_tr": "Okula Donus",
        "vocab": ["subject", "timetable", "break", "canteen", "library", "lab", "corridor",
                  "locker", "homework", "notebook", "pencil case", "eraser", "ruler", "schedule", "term"],
        "structure": "What subjects do you have on Monday? I have Maths and Science. My favourite subject is...",
        "skills": {
            "listening": "Okul programi hakkindaki diyaloglari dinler, ders saatlerini ve gunleri tespit eder.",
            "speaking": "Ders programini anlatir, sevdigi dersleri aciklar: 'My favourite subject is... because...'",
            "reading": "Bir ogrencinin okul gununu anlatan kisa metni (80-100 kelime) okur, sorulari cevaplar.",
            "writing": "Kendi ders programini tablo olarak yazar ve 4-5 cumleyle anlatir.",
        },
        "linked_content": {
            "categories": ["Okul", "Gunluk Yasam"],
            "songs": ["School Days Song"],
            "games": ["Hafiza Kartlari", "Eslestir"],
            "dialogues": ["What's Your Timetable?"],
            "readings": ["My School Day"],
            "writings": ["My Timetable"],
            "grammar": ["Present Simple (have/has)"],
            "phonics": ["Word Stress"],
            "listening": ["Okul Diyaloglari"],
        },
        "days": {
            "mon": ["Ana Ders: Okula Donus temel kelimelerini tanitim (subject/timetable/break) + yapi sunumu: What subjects do you have on Monday? I have Maths", "Beceri Lab: Dinleme — 'Okula Donus' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What subjects do you have on Monday? I have Maths yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Okula Donus konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Okula Donus' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Okula Donus konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (canteen/library/lab) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Okula Donus temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Okula Donus konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Ders programini tablo olarak hazirlayip sozlu anlatabilir.",
    },
    {
        "week": 2,
        "theme": "My Daily Routine",
        "theme_tr": "Gunluk Rutinim",
        "vocab": ["wake up", "get dressed", "brush teeth", "have breakfast", "go to school", "come home",
                  "do homework", "have dinner", "take a shower", "go to bed", "routine", "always", "usually", "sometimes", "never"],
        "structure": "I always wake up at 7. She usually has breakfast at 8. What time do you...?",
        "skills": {
            "listening": "Gunluk rutin anlatan ses kayitlarini dinler, saatleri ve aktiviteleri eslestirir.",
            "speaking": "Kendi gunluk rutinini siklik zarflari kullanarak anlatir.",
            "reading": "Bir ogrencinin gununu anlatan metni okur, dogru/yanlis sorularini cevaplar.",
            "writing": "Gunluk rutinini saat belirterek 6-7 cumleyle yazar.",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam"],
            "songs": ["Daily Routine Song"],
            "games": ["Siralama Oyunu", "Dogru / Yanlis"],
            "dialogues": ["What Time Do You Wake Up?"],
            "readings": ["A Day in My Life"],
            "writings": ["My Daily Routine"],
            "grammar": ["Present Simple + adverbs of frequency"],
            "phonics": ["Sentence Stress"],
            "listening": ["Gunluk Rutin Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Gunluk Rutinim temel kelimelerini tanitim (wake up/get dressed/brush teeth) + yapi sunumu: I always wake up at 7. She usually has breakfast", "Beceri Lab: Dinleme — 'Gunluk Rutinim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I always wake up at 7. She usually has breakfast yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Gunluk Rutinim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Gunluk Rutinim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Gunluk Rutinim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (have breakfast/go to school/come home) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Gunluk Rutinim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Gunluk Rutinim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Gunluk rutinini siklik zarflari ve saatlerle anlatabilir.",
    },
    {
        "week": 3,
        "theme": "Classroom Rules",
        "theme_tr": "Sinif Kurallari",
        "vocab": ["raise hand", "be quiet", "listen", "pay attention", "line up", "share", "respect",
                  "permission", "rule", "behave", "responsible", "fair", "cooperate", "polite", "apologise"],
        "structure": "You must listen to the teacher. You mustn't run in the corridor. Can I go to the toilet, please?",
        "skills": {
            "listening": "Sinif kurallarini dinler, kurallari listeler.",
            "speaking": "Sinif kurallarini anlatir, izin ister: 'Can I...?'",
            "reading": "Sinif kurallari posterini okur, kurallari siniflandirir.",
            "writing": "Kendi sinifi icin 8-10 kural yazar.",
        },
        "linked_content": {
            "categories": ["Okul"],
            "songs": ["Classroom Rules Chant"],
            "games": ["Kural Eslestir", "Dogru / Yanlis"],
            "dialogues": ["Can I Go Out?"],
            "readings": ["Our Classroom Rules"],
            "writings": ["Rules for My Class"],
            "grammar": ["must/mustn't, Can I...?"],
            "phonics": ["Intonation in questions"],
            "listening": ["Sinif Kurallari Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Sinif Kurallari temel kelimelerini tanitim (raise hand/be quiet/listen) + yapi sunumu: You must listen to the teacher. You mustn't run", "Beceri Lab: Dinleme — 'Sinif Kurallari' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — You must listen to the teacher. You mustn't run yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Sinif Kurallari konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Sinif Kurallari' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Sinif Kurallari konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (pay attention/line up/share) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Sinif Kurallari temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Sinif Kurallari konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sinif kurallarini must/mustn't ile ifade edebilir.",
    },
    {
        "week": 4,
        "theme": "School Clubs & Activities",
        "theme_tr": "Okul Kulupleri",
        "vocab": ["club", "drama", "choir", "chess", "debate", "science club", "art club",
                  "member", "meeting", "captain", "volunteer", "rehearsal", "tournament", "participate", "organise"],
        "structure": "I'm a member of the chess club. We meet on Thursdays. Would you like to join...?",
        "skills": {
            "listening": "Okul kulupleri tanitimini dinler, kulupleri ve aktiviteleri eslestirir.",
            "speaking": "Uye oldugu kulubu tanitir, arkadasini davet eder.",
            "reading": "Okul kulupleri brosurunu okur, bilgileri cikarir.",
            "writing": "Kendi kulubunu tanitan kisa bir yazi yazar (6-8 cumle).",
        },
        "linked_content": {
            "categories": ["Okul", "Hobiler"],
            "songs": [],
            "games": ["Kulup Eslestir", "Kim Hangi Kulupte?"],
            "dialogues": ["Join Our Club!"],
            "readings": ["School Clubs Fair"],
            "writings": ["My Club"],
            "grammar": ["Present Simple + like/enjoy + V-ing"],
            "phonics": ["/dʒ/ vs /tʃ/ sounds"],
            "listening": ["Kulup Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Okul Kulupleri temel kelimelerini tanitim (club/drama/choir) + yapi sunumu: I'm a member of the chess club. We meet on Thursdays", "Beceri Lab: Dinleme — 'Okul Kulupleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I'm a member of the chess club. We meet on Thursdays yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Okul Kulupleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Okul Kulupleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Okul Kulupleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (chess/debate/science club) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Okul Kulupleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Okul Kulupleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir okul kulubunu tanitip arkadasini davet edebilir.",
    },
    # ===== UNIT 2: My Family (Weeks 5-8) =====
    {
        "week": 5,
        "theme": "My Family",
        "theme_tr": "Ailem",
        "vocab": ["mother", "father", "brother", "sister", "uncle", "aunt", "cousin", "nephew",
                  "niece", "grandparents", "relatives", "parents", "siblings", "twins", "generation"],
        "structure": "I have two brothers. My mother's name is... She is a teacher. How many siblings do you have?",
        "skills": {
            "listening": "Aile tanitimini dinler, aile bireylerini ve mesleklerini saptar.",
            "speaking": "Ailesini tanitir, her bireyin adini ve meslegini soyler.",
            "reading": "Bir ailenin tanitim metnini okur, aile agaci semasini tamamlar.",
            "writing": "Kendi aile agacini cizer ve her bireyi 1-2 cumleyle tanitir.",
        },
        "linked_content": {
            "categories": ["Aile"],
            "songs": ["Family Song"],
            "games": ["Aile Agaci Eslestir", "Kim Bu?"],
            "dialogues": ["Tell Me About Your Family"],
            "readings": ["The Johnson Family"],
            "writings": ["My Family Tree"],
            "grammar": ["Possessive adjectives (my/your/his/her)"],
            "phonics": ["/θ/ vs /ð/ sounds"],
            "listening": ["Aile Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Ailem temel kelimelerini tanitim (mother/father/brother) + yapi sunumu: I have two brothers. My mother's name is...", "Beceri Lab: Dinleme — 'Ailem' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I have two brothers. My mother's name is... yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Ailem konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Ailem' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Ailem konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (uncle/aunt/cousin) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Ailem temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Ailem konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Aile agacini cizerek her bireyi tanitabilir.",
    },
    {
        "week": 6,
        "theme": "Describing People",
        "theme_tr": "Insanlari Tanimlamak",
        "vocab": ["tall", "short", "slim", "plump", "curly", "straight", "blond", "dark",
                  "moustache", "beard", "glasses", "freckles", "appearance", "personality", "cheerful"],
        "structure": "She is tall and slim. He has curly hair. She looks cheerful. What does he look like?",
        "skills": {
            "listening": "Kisi tanimlarini dinler, dogru resmi secer.",
            "speaking": "Bir kisiyi dis gorunusu ve kisilik ozellikleriyle tanitir.",
            "reading": "Kayip ilan metnini okur, kisinin ozelliklerini listeler.",
            "writing": "En yakin arkadasini fiziksel ve kisilik ozellikleriyle tanitir (6-8 cumle).",
        },
        "linked_content": {
            "categories": ["Insanlar", "Aile"],
            "songs": [],
            "games": ["Kim Bu? Tahmin Et", "Eslestir"],
            "dialogues": ["What Does She Look Like?"],
            "readings": ["Missing Person Notice"],
            "writings": ["My Best Friend"],
            "grammar": ["have/has + adjective order"],
            "phonics": ["Long vowels /iː/ /uː/"],
            "listening": ["Kisi Tanimlama"],
        },
        "days": {
            "mon": ["Ana Ders: Insanlari Tanimlamak temel kelimelerini tanitim (tall/short/slim) + yapi sunumu: She is tall and slim. He has curly hair", "Beceri Lab: Dinleme — 'Insanlari Tanimlamak' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — She is tall and slim. He has curly hair yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Insanlari Tanimlamak konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Insanlari Tanimlamak' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Insanlari Tanimlamak konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (plump/curly/straight) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Insanlari Tanimlamak temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Insanlari Tanimlamak konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir kisiyi gorunus ve kisilik ozellikleriyle tanimlayabilir.",
    },
    {
        "week": 7,
        "theme": "Family Activities",
        "theme_tr": "Aile Aktiviteleri",
        "vocab": ["picnic", "barbecue", "visit", "celebrate", "birthday", "anniversary", "gathering",
                  "play board games", "cook together", "watch movies", "go camping", "weekend", "quality time", "tradition", "memory"],
        "structure": "We usually have a picnic on Sundays. My family celebrates birthdays together. What do you do at weekends?",
        "skills": {
            "listening": "Aile aktivitelerini anlatan diyalogu dinler, aktiviteleri saptar.",
            "speaking": "Ailesiyle yaptigi aktiviteleri anlatir.",
            "reading": "Bir ailenin hafta sonu planini okur, sorulari cevaplar.",
            "writing": "Ailesiyle yaptigi en guzel aktiviteyi 6-8 cumleyle anlatir.",
        },
        "linked_content": {
            "categories": ["Aile", "Gunluk Yasam"],
            "songs": ["Family Fun Song"],
            "games": ["Aktivite Eslestir", "Hafta Sonu Planlama"],
            "dialogues": ["What Does Your Family Do at Weekends?"],
            "readings": ["A Family Weekend"],
            "writings": ["Our Family Tradition"],
            "grammar": ["Present Simple + frequency expressions"],
            "phonics": ["/æ/ vs /ɑː/ sounds"],
            "listening": ["Aile Hafta Sonu Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Aile Aktiviteleri temel kelimelerini tanitim (picnic/barbecue/visit) + yapi sunumu: We usually have a picnic on Sundays", "Beceri Lab: Dinleme — 'Aile Aktiviteleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — We usually have a picnic on Sundays yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Aile Aktiviteleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Aile Aktiviteleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Aile Aktiviteleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (celebrate/birthday/gathering) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Aile Aktiviteleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Aile Aktiviteleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Aile aktivitelerini siklik zarflariyla anlatabilir.",
    },
    {
        "week": 8,
        "theme": "Possessions & Belongings",
        "theme_tr": "Esyalar ve Aitlik",
        "vocab": ["whose", "mine", "yours", "his", "hers", "ours", "theirs", "belong",
                  "own", "wallet", "keychain", "backpack", "lunchbox", "diary", "treasure"],
        "structure": "Whose bag is this? It's mine. This book belongs to Ali. Is this yours?",
        "skills": {
            "listening": "Aitlik diyaloglarini dinler, esyalarin kime ait oldugunu belirler.",
            "speaking": "Esyalarini tanitir, aitlik sorar.",
            "reading": "Kayip esya ilanlarini okur, sahiplerini eslestirir.",
            "writing": "Odasindaki esyalari ve kime ait olduklarini yazar (6-8 cumle).",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam", "Aile"],
            "songs": [],
            "games": ["Kimin Esyasi?", "Eslestir"],
            "dialogues": ["Whose Is This?"],
            "readings": ["Lost and Found"],
            "writings": ["Things in My Room"],
            "grammar": ["Possessive pronouns (mine/yours/his/hers)"],
            "phonics": ["/z/ vs /s/ endings"],
            "listening": ["Kayip Esya Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Esyalar ve Aitlik temel kelimelerini tanitim (whose/mine/yours) + yapi sunumu: Whose bag is this? It's mine", "Beceri Lab: Dinleme — 'Esyalar ve Aitlik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Whose bag is this? It's mine yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Esyalar ve Aitlik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Esyalar ve Aitlik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Esyalar ve Aitlik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (hers/ours/theirs) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Esyalar ve Aitlik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Esyalar ve Aitlik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Esyalarin aitligini possessive pronouns ile ifade edebilir.",
    },
    # ===== UNIT 3: My Neighbourhood (Weeks 9-12) =====
    {
        "week": 9,
        "theme": "My Neighbourhood",
        "theme_tr": "Mahallemi Taniyorum",
        "vocab": ["neighbourhood", "bakery", "pharmacy", "grocery", "mosque", "park", "post office",
                  "bank", "hospital", "fire station", "police station", "bus stop", "pavement", "crosswalk", "block"],
        "structure": "There is a bakery next to the park. The hospital is opposite the school. Is there a...?",
        "skills": {
            "listening": "Mahalle tarifini dinler, harita uzerinde yerleri isaretler.",
            "speaking": "Mahallesindeki yerleri tanitir ve konumlarini belirtir.",
            "reading": "Bir mahallenin tanitim metnini okur, haritayla eslestirir.",
            "writing": "Kendi mahallesini 6-8 cumleyle tanitir, yerleri ve konumlarini yazar.",
        },
        "linked_content": {
            "categories": ["Sehir", "Gunluk Yasam"],
            "songs": ["In My Neighbourhood"],
            "games": ["Harita Eslestir", "Nerede?"],
            "dialogues": ["Where is the Bakery?"],
            "readings": ["My Neighbourhood"],
            "writings": ["About My Neighbourhood"],
            "grammar": ["There is/are + prepositions of place"],
            "phonics": ["/eɪ/ vs /æ/ sounds"],
            "listening": ["Mahalle Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Mahallemi Taniyorum temel kelimelerini tanitim (neighbourhood/bakery/pharmacy) + yapi sunumu: There is a bakery next to the park", "Beceri Lab: Dinleme — 'Mahallemi Taniyorum' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — There is a bakery next to the park yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Mahallemi Taniyorum konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Mahallemi Taniyorum' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Mahallemi Taniyorum konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (grocery/mosque/park) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Mahallemi Taniyorum temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Mahallemi Taniyorum konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Mahallesindeki yerleri konumlariyla birlikte anlatabilir.",
    },
    {
        "week": 10,
        "theme": "Giving Directions",
        "theme_tr": "Yol Tarifi",
        "vocab": ["turn left", "turn right", "go straight", "go past", "crossroads", "roundabout",
                  "traffic lights", "corner", "block", "across from", "between", "near", "far", "map", "direction"],
        "structure": "Go straight and turn left at the traffic lights. It's on your right. Excuse me, how can I get to...?",
        "skills": {
            "listening": "Yol tarifini dinler, harita uzerinde rotayi cizer.",
            "speaking": "Yol tarifi verir ve sorar: 'How can I get to the hospital?'",
            "reading": "Yol tarifi icerikli metni okur, haritada rotayi takip eder.",
            "writing": "Evden okula olan rotayi adim adim yazar.",
        },
        "linked_content": {
            "categories": ["Sehir"],
            "songs": [],
            "games": ["Yol Tarifi Yarismasi", "Harita Takip"],
            "dialogues": ["How Can I Get to the Museum?"],
            "readings": ["Finding the Way"],
            "writings": ["From Home to School"],
            "grammar": ["Imperatives + prepositions of movement"],
            "phonics": ["/l/ vs /r/ sounds"],
            "listening": ["Yol Tarifi Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Yol Tarifi temel kelimelerini tanitim (turn left/turn right/go straight) + yapi sunumu: Go straight and turn left at the traffic lights", "Beceri Lab: Dinleme — 'Yol Tarifi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Go straight and turn left at the traffic lights yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yol Tarifi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yol Tarifi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yol Tarifi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (go past/crossroads/roundabout) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yol Tarifi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yol Tarifi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Harita uzerinde yol tarifi verebilir ve anlayabilir.",
    },
    {
        "week": 11,
        "theme": "Public Transport",
        "theme_tr": "Toplu Tasima",
        "vocab": ["bus", "tram", "metro", "taxi", "ferry", "ticket", "station", "stop",
                  "platform", "timetable", "fare", "single", "return", "passenger", "commute"],
        "structure": "How do you get to school? I take the bus. Which bus goes to the city centre? Get off at the third stop.",
        "skills": {
            "listening": "Toplu tasima anonslarini dinler, durak ve hat bilgilerini saptar.",
            "speaking": "Ulasim tercihleri hakkinda konusur, bilet satin alir.",
            "reading": "Otobus/metro tarifesini okur, rota planlar.",
            "writing": "Evden okula ulasim rotasini adim adim yazar.",
        },
        "linked_content": {
            "categories": ["Sehir", "Ulasim"],
            "songs": ["The Wheels on the Bus"],
            "games": ["Rota Planla", "Bilet Al"],
            "dialogues": ["A Single Ticket, Please"],
            "readings": ["Getting Around the City"],
            "writings": ["My Journey to School"],
            "grammar": ["How do you...? + by + transport"],
            "phonics": ["/ʌ/ vs /ɑː/ sounds"],
            "listening": ["Toplu Tasima Anonslari"],
        },
        "days": {
            "mon": ["Ana Ders: Toplu Tasima temel kelimelerini tanitim (bus/tram/metro) + yapi sunumu: How do you get to school? I take the bus", "Beceri Lab: Dinleme — 'Toplu Tasima' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — How do you get to school? I take the bus yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Toplu Tasima konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Toplu Tasima' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Toplu Tasima konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (taxi/ferry/ticket) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Toplu Tasima temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Toplu Tasima konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Toplu tasima ile ilgili bilgi sorabilir ve rota planlayabilir.",
    },
    {
        "week": 12,
        "theme": "Review & Project Week 1",
        "theme_tr": "Tekrar ve Proje Haftasi 1",
        "vocab": [],
        "structure": "Unite 1-3 genel tekrar: Okul, Aile, Mahalle konulari",
        "skills": {
            "listening": "Genel tekrar dinleme aktiviteleri.",
            "speaking": "Sinif ici mini sunumlar: mahalle haritasi + aile tanitimi.",
            "reading": "Karisik metin okuma ve anlama.",
            "writing": "Mahalle rehberi projesi yazma.",
        },
        "linked_content": {
            "categories": ["Tekrar", "Proje"],
            "songs": [],
            "games": ["Buyuk Quiz", "Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Mahalle Rehberi Projesi"],
            "grammar": ["Unite 1-3 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Karisik Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 1-3 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — karisik temali dinleme aktiviteleri"],
            "tue": ["Ana Ders: Gramer odak — Unite 1-3 gramer yapilari genel tekrar", "Beceri Lab: Konusma — sinif ici mini sunumlar"],
            "wed": ["Ana Ders: Okuma — karisik metin okuma ve anlama sorulari", "Beceri Lab: Yazma — Mahalle Rehberi projesi yazma"],
            "thu": ["Ana Ders: Proje hazirlama ve sunum provasi", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 1-3 genel degerlendirme + mahalle rehberi projesi.",
    },
    # ===== UNIT 4: Seasons & Weather (Weeks 13-16) =====
    {
        "week": 13,
        "theme": "Seasons & Weather",
        "theme_tr": "Mevsimler ve Hava Durumu",
        "vocab": ["sunny", "cloudy", "rainy", "snowy", "windy", "foggy", "stormy", "temperature",
                  "degree", "forecast", "season", "spring", "autumn", "umbrella", "raincoat"],
        "structure": "What's the weather like today? It's sunny and warm. In winter, it usually snows.",
        "skills": {
            "listening": "Hava durumu tahminini dinler, haftalik tabloyu doldurur.",
            "speaking": "Gunun havasini ve mevsim ozelliklerini anlatir.",
            "reading": "Hava durumu raporunu okur, sehirlerin havalarini karsilastirir.",
            "writing": "Haftalik hava durumu tablosu + en sevdigi mevsimi anlatan paragraf yazar.",
        },
        "linked_content": {
            "categories": ["Doga", "Gunluk Yasam"],
            "songs": ["Weather Song"],
            "games": ["Hava Durumu Eslestir", "Mevsim Sinifla"],
            "dialogues": ["What's the Weather Like?"],
            "readings": ["Weather Report"],
            "writings": ["My Favourite Season"],
            "grammar": ["Present Simple for facts + It's + adjective"],
            "phonics": ["/w/ sound practice"],
            "listening": ["Hava Durumu Tahmini"],
        },
        "days": {
            "mon": ["Ana Ders: Mevsimler ve Hava Durumu temel kelimelerini tanitim (sunny/cloudy/rainy) + yapi sunumu: What's the weather like today? It's sunny and warm", "Beceri Lab: Dinleme — 'Mevsimler ve Hava Durumu' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What's the weather like today? It's sunny and warm yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Mevsimler ve Hava Durumu konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Mevsimler ve Hava Durumu' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Mevsimler ve Hava Durumu konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (snowy/windy/foggy) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Mevsimler ve Hava Durumu temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Mevsimler ve Hava Durumu konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hava durumunu ve mevsimleri tanimlar, haftalik tahmin tablosu doldurur.",
    },
    {
        "week": 14,
        "theme": "Clothes & Dressing",
        "theme_tr": "Giysiler ve Giyinme",
        "vocab": ["jacket", "coat", "scarf", "boots", "sandals", "shorts", "sweater", "gloves",
                  "sunglasses", "hat", "uniform", "casual", "formal", "fashion", "outfit"],
        "structure": "I wear a coat in winter. She is wearing a red dress. What are you wearing today?",
        "skills": {
            "listening": "Giysi tariflerini dinler, dogru kisiyi/resmi secer.",
            "speaking": "Bugunku kiyafetini ve mevsime gore giyinmeyi anlatir.",
            "reading": "Moda/giyim metnini okur, kiyafetleri siniflandirir.",
            "writing": "En sevdigi kiyafetini ve neden sevdigini yazar (6-8 cumle).",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam", "Doga"],
            "songs": ["Getting Dressed Song"],
            "games": ["Kiyafet Eslestir", "Mevsim-Kiyafet"],
            "dialogues": ["What Are You Wearing?"],
            "readings": ["Dressing for the Weather"],
            "writings": ["My Favourite Outfit"],
            "grammar": ["Present Continuous for now + wear vs put on"],
            "phonics": ["/ɪ/ vs /iː/ sounds"],
            "listening": ["Kiyafet Tanimlama"],
        },
        "days": {
            "mon": ["Ana Ders: Giysiler ve Giyinme temel kelimelerini tanitim (jacket/coat/scarf) + yapi sunumu: I wear a coat in winter. She is wearing a red dress", "Beceri Lab: Dinleme — 'Giysiler ve Giyinme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I wear a coat in winter. She is wearing a red dress yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Giysiler ve Giyinme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Giysiler ve Giyinme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Giysiler ve Giyinme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (boots/sandals/shorts) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Giysiler ve Giyinme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Giysiler ve Giyinme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Mevsime uygun giyinmeyi Present Continuous ile anlatabilir.",
    },
    {
        "week": 15,
        "theme": "Present Continuous Activities",
        "theme_tr": "Simdiki Zaman Aktiviteleri",
        "vocab": ["running", "jumping", "swimming", "drawing", "painting", "dancing", "singing",
                  "cooking", "playing", "studying", "sleeping", "reading", "writing", "laughing", "crying"],
        "structure": "What are you doing now? I'm studying. She is playing the guitar. They aren't sleeping.",
        "skills": {
            "listening": "Aktivite anlatimlarini dinler, resimleri eslestirir.",
            "speaking": "Su anda ne yaptigini anlatir, baskalarinin ne yaptigini soyler.",
            "reading": "Bir parkta olan olaylari anlatan metni okur, kisileri ve aktiviteleri eslestirir.",
            "writing": "Bir resme bakarak ne oldugunu 6-8 cumleyle tasvir eder.",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam"],
            "songs": ["What Are You Doing?"],
            "games": ["Pantomim", "Resim Anlat"],
            "dialogues": ["What's Happening?"],
            "readings": ["A Day in the Park"],
            "writings": ["Describe the Picture"],
            "grammar": ["Present Continuous (affirmative/negative/question)"],
            "phonics": ["-ing pronunciation"],
            "listening": ["Aktivite Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Simdiki Zaman Aktiviteleri temel kelimelerini tanitim (running/jumping/swimming) + yapi sunumu: What are you doing now? I'm studying", "Beceri Lab: Dinleme — 'Simdiki Zaman Aktiviteleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What are you doing now? I'm studying yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Simdiki Zaman Aktiviteleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Simdiki Zaman Aktiviteleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Simdiki Zaman Aktiviteleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (drawing/painting/dancing) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Simdiki Zaman Aktiviteleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Simdiki Zaman Aktiviteleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Present Continuous ile su anki aktiviteleri anlatabilir.",
    },
    {
        "week": 16,
        "theme": "Festivals & Celebrations",
        "theme_tr": "Festivaller ve Kutlamalar",
        "vocab": ["festival", "celebration", "fireworks", "parade", "costume", "decoration", "invitation",
                  "gift", "balloon", "candle", "traditional", "national", "religious", "harvest", "ceremony"],
        "structure": "We celebrate Republic Day on 29th October. People wear costumes and watch fireworks.",
        "skills": {
            "listening": "Festival tanitimini dinler, onemli bilgileri not eder.",
            "speaking": "Ulkesindeki onemli festivalleri ve kutlamalari anlatir.",
            "reading": "Farkli ulkelerin festivallerini anlatan metni okur, karsilastirir.",
            "writing": "En sevdigi festivali anlatan paragraf yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Kultur", "Gunluk Yasam"],
            "songs": ["Celebration Song"],
            "games": ["Festival Eslestir", "Bayrak-Ulke"],
            "dialogues": ["Tell Me About Your Festival"],
            "readings": ["Festivals Around the World"],
            "writings": ["My Favourite Festival"],
            "grammar": ["Present Simple for routines + on/in/at for dates"],
            "phonics": ["/ʃ/ vs /s/ sounds"],
            "listening": ["Festival Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Festivaller ve Kutlamalar temel kelimelerini tanitim (festival/celebration/fireworks) + yapi sunumu: We celebrate Republic Day on 29th October", "Beceri Lab: Dinleme — 'Festivaller ve Kutlamalar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — We celebrate Republic Day on 29th October yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Festivaller ve Kutlamalar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Festivaller ve Kutlamalar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Festivaller ve Kutlamalar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (parade/costume/decoration) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Festivaller ve Kutlamalar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Festivaller ve Kutlamalar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Onemli festivalleri tarih ve gelenekleriyle anlatabilir.",
    },
    # ===== UNIT 5: Food & Shopping (Weeks 17-20) =====
    {
        "week": 17,
        "theme": "Food & Shopping",
        "theme_tr": "Yiyecek ve Alisveris",
        "vocab": ["menu", "order", "starter", "main course", "dessert", "bill", "waiter",
                  "delicious", "spicy", "sour", "sweet", "bitter", "ingredient", "recipe", "portion"],
        "structure": "I'd like a pizza, please. Can I have the bill? How much is it? What would you like?",
        "skills": {
            "listening": "Restoran diyalogunu dinler, siparisleri not eder.",
            "speaking": "Restoranda siparis verir ve hesap sorar.",
            "reading": "Bir menuyu okur, yemekleri kategorize eder.",
            "writing": "Kendi hayali restoraninin menusunu ve bir yemek tarifini yazar.",
        },
        "linked_content": {
            "categories": ["Yiyecek", "Alisveris"],
            "songs": ["Food Song"],
            "games": ["Menu Eslestir", "Restoran Roleplay"],
            "dialogues": ["At the Restaurant"],
            "readings": ["The Best Pizza in Town"],
            "writings": ["My Restaurant Menu"],
            "grammar": ["Countable/Uncountable + some/any"],
            "phonics": ["/ʌ/ vs /ɑː/ sounds"],
            "listening": ["Restoran Siparis"],
        },
        "days": {
            "mon": ["Ana Ders: Yiyecek ve Alisveris temel kelimelerini tanitim (menu/order/starter) + yapi sunumu: I'd like a pizza, please. Can I have the bill?", "Beceri Lab: Dinleme — 'Yiyecek ve Alisveris' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I'd like a pizza, please. Can I have the bill? yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yiyecek ve Alisveris konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yiyecek ve Alisveris' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yiyecek ve Alisveris konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (main course/dessert/bill) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yiyecek ve Alisveris temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yiyecek ve Alisveris konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Restoranda siparis verebilir, menu okuyabilir.",
    },
    {
        "week": 18,
        "theme": "At the Market",
        "theme_tr": "Markette",
        "vocab": ["basket", "trolley", "aisle", "cashier", "receipt", "discount", "bargain",
                  "fresh", "frozen", "organic", "packet", "tin", "bottle", "jar", "carton"],
        "structure": "How much are the apples? They are 5 lira a kilo. I need a bottle of milk.",
        "skills": {
            "listening": "Market diyalogunu dinler, alinan urunleri ve fiyatlari saptar.",
            "speaking": "Markette alisveris yapar, fiyat sorar, miktar belirtir.",
            "reading": "Alisveris listesini ve market brosurunu okur.",
            "writing": "Haftalik alisveris listesi + market deneyimini anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Alisveris", "Yiyecek"],
            "songs": [],
            "games": ["Market Roleplay", "Fiyat Tahmin"],
            "dialogues": ["At the Grocery Store"],
            "readings": ["Shopping List"],
            "writings": ["My Shopping Experience"],
            "grammar": ["How much/How many + a/an/some/any"],
            "phonics": ["/p/ vs /b/ sounds"],
            "listening": ["Market Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Markette temel kelimelerini tanitim (basket/trolley/aisle) + yapi sunumu: How much are the apples? They are 5 lira a kilo", "Beceri Lab: Dinleme — 'Markette' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — How much are the apples? They are 5 lira a kilo yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Markette konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Markette' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Markette konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (cashier/receipt/discount) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Markette temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Markette konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Markette alisveris yapabilir, fiyat sorabilir ve miktar belirtebilir.",
    },
    {
        "week": 19,
        "theme": "Healthy Eating",
        "theme_tr": "Saglikli Beslenme",
        "vocab": ["protein", "carbohydrate", "vitamin", "mineral", "fibre", "calcium", "balanced diet",
                  "junk food", "fast food", "nutrition", "calorie", "portion", "organic", "vegetable", "fruit"],
        "structure": "You should eat more vegetables. Junk food is bad for you. How often do you eat fruit?",
        "skills": {
            "listening": "Saglikli beslenme tavsiyelerini dinler, bilgileri not eder.",
            "speaking": "Beslenme aliskanliklarini anlatir, tavsiye verir.",
            "reading": "Besin piramidi ve saglikli beslenme metnini okur.",
            "writing": "Bir gunluk saglikli menu planlar ve yazar.",
        },
        "linked_content": {
            "categories": ["Saglik", "Yiyecek"],
            "songs": ["Healthy Food Song"],
            "games": ["Besin Piramidi", "Saglikli/Sagliksiz Sinifla"],
            "dialogues": ["What Should I Eat?"],
            "readings": ["The Food Pyramid"],
            "writings": ["My Healthy Menu"],
            "grammar": ["should/shouldn't + How often...?"],
            "phonics": ["/f/ vs /v/ sounds"],
            "listening": ["Saglikli Beslenme Tavsiyeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Saglikli Beslenme temel kelimelerini tanitim (protein/carbohydrate/vitamin) + yapi sunumu: You should eat more vegetables", "Beceri Lab: Dinleme — 'Saglikli Beslenme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — You should eat more vegetables yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Saglikli Beslenme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Saglikli Beslenme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Saglikli Beslenme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (mineral/fibre/calcium) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Saglikli Beslenme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Saglikli Beslenme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Saglikli beslenme tavsiyeleri verebilir, gunluk menu planlayabilir.",
    },
    {
        "week": 20,
        "theme": "Midterm Review & Assessment",
        "theme_tr": "Ara Sinav Tekrari ve Degerlendirme",
        "vocab": [],
        "structure": "Unite 1-5 genel tekrar ve degerlendirme",
        "skills": {
            "listening": "Ara sinav dinleme degerlendirmesi.",
            "speaking": "Ara sinav sozlu degerlendirme.",
            "reading": "Ara sinav okuma degerlendirmesi.",
            "writing": "Ara sinav yazma degerlendirmesi.",
        },
        "linked_content": {
            "categories": ["Degerlendirme"],
            "songs": [],
            "games": ["Buyuk Quiz", "Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Ara Sinav Yazma"],
            "grammar": ["Unite 1-5 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Ara Sinav Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 1-5 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — ara sinav dinleme degerlendirmesi"],
            "tue": ["Ana Ders: Gramer odak — Unite 1-5 gramer yapilari genel tekrar", "Beceri Lab: Konusma — ara sinav sozlu degerlendirme"],
            "wed": ["Ana Ders: Okuma — ara sinav okuma degerlendirmesi", "Beceri Lab: Yazma — ara sinav yazma degerlendirmesi"],
            "thu": ["Ana Ders: Eksik konularin tekrari ve pekistirme alishtirmalari", "Beceri Lab: Proje/Sunum — donem sonu mini proje sunumlari"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 1-5 ara sinav: 4 beceri degerlendirmesi.",
    },
    # ===== UNIT 6: Hobbies & Free Time (Weeks 21-24) =====
    {
        "week": 21,
        "theme": "Hobbies & Free Time",
        "theme_tr": "Hobiler ve Serbest Zaman",
        "vocab": ["hobby", "collect", "stamp", "coin", "model", "puzzle", "gardening", "photography",
                  "painting", "knitting", "fishing", "camping", "interested", "keen on", "enjoy"],
        "structure": "What are your hobbies? I like collecting stamps. She enjoys painting. I'm interested in photography.",
        "skills": {
            "listening": "Hobi tanitimlarini dinler, kisileri ve hobileri eslestirir.",
            "speaking": "Hobilerini anlatir, baskalarinin hobilerini sorar.",
            "reading": "Hobi kulupleri hakkinda metin okur, bilgileri cikarir.",
            "writing": "En sevdigi hobisini ve neden sevdigini yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Hobiler", "Gunluk Yasam"],
            "songs": ["Hobby Song"],
            "games": ["Hobi Eslestir", "Pantomim"],
            "dialogues": ["What Do You Do in Your Free Time?"],
            "readings": ["Popular Hobbies"],
            "writings": ["My Favourite Hobby"],
            "grammar": ["like/enjoy/be interested in + V-ing"],
            "phonics": ["/ɒ/ vs /əʊ/ sounds"],
            "listening": ["Hobi Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Hobiler ve Serbest Zaman temel kelimelerini tanitim (hobby/collect/stamp) + yapi sunumu: What are your hobbies? I like collecting stamps", "Beceri Lab: Dinleme — 'Hobiler ve Serbest Zaman' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What are your hobbies? I like collecting stamps yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Hobiler ve Serbest Zaman konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Hobiler ve Serbest Zaman' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Hobiler ve Serbest Zaman konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (coin/model/puzzle) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Hobiler ve Serbest Zaman temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Hobiler ve Serbest Zaman konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hobilerini like/enjoy + V-ing ile anlatabilir.",
    },
    {
        "week": 22,
        "theme": "Sports & Games",
        "theme_tr": "Spor ve Oyunlar",
        "vocab": ["football", "basketball", "volleyball", "swimming", "cycling", "running", "tennis",
                  "gymnastics", "team", "match", "score", "win", "lose", "draw", "competition"],
        "structure": "I play football on Saturdays. She is good at swimming. Do you like playing...?",
        "skills": {
            "listening": "Spor roportajini dinler, sporlari ve tercihleri saptar.",
            "speaking": "Yaptigi sporlari ve tercihlerini anlatir.",
            "reading": "Bir sporcunun biyografisini okur, bilgileri cikarir.",
            "writing": "En sevdigi sporu ve neden sevdigini 6-8 cumleyle yazar.",
        },
        "linked_content": {
            "categories": ["Spor"],
            "songs": ["Sports Chant"],
            "games": ["Spor Eslestir", "Pantomim"],
            "dialogues": ["What Sport Do You Play?"],
            "readings": ["A Young Athlete"],
            "writings": ["My Favourite Sport"],
            "grammar": ["play/do/go + sports"],
            "phonics": ["/ɔː/ vs /ɒ/ sounds"],
            "listening": ["Spor Roportaji"],
        },
        "days": {
            "mon": ["Ana Ders: Spor ve Oyunlar temel kelimelerini tanitim (football/basketball/volleyball) + yapi sunumu: I play football on Saturdays. She is good at swimming", "Beceri Lab: Dinleme — 'Spor ve Oyunlar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I play football on Saturdays. She is good at swimming yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Spor ve Oyunlar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Spor ve Oyunlar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Spor ve Oyunlar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (swimming/cycling/running) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Spor ve Oyunlar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Spor ve Oyunlar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sevdigi sporlari anlatabilir, sporcu biyografisi anlayabilir.",
    },
    {
        "week": 23,
        "theme": "Movies & Entertainment",
        "theme_tr": "Filmler ve Eglence",
        "vocab": ["comedy", "action", "horror", "cartoon", "documentary", "character", "director",
                  "scene", "plot", "review", "recommend", "boring", "exciting", "funny", "scary"],
        "structure": "What kind of movies do you like? I prefer comedies. The film was really exciting.",
        "skills": {
            "listening": "Film tanitimini dinler, tur ve ozellikleri saptar.",
            "speaking": "Sevdigi filmleri ve turleri anlatir, film onerir.",
            "reading": "Film incelemesi okur, olumlu/olumsuz yorumlari ayirir.",
            "writing": "En sevdigi filmin incelemesini yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Eglence"],
            "songs": [],
            "games": ["Film Tahmin", "Tur Eslestir"],
            "dialogues": ["Let's Watch a Movie"],
            "readings": ["Movie Review: The Lion King"],
            "writings": ["My Favourite Movie"],
            "grammar": ["like/prefer/enjoy + noun/V-ing + adjectives"],
            "phonics": ["/dʒ/ vs /ʒ/ sounds"],
            "listening": ["Film Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Filmler ve Eglence temel kelimelerini tanitim (comedy/action/horror) + yapi sunumu: What kind of movies do you like? I prefer comedies", "Beceri Lab: Dinleme — 'Filmler ve Eglence' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What kind of movies do you like? I prefer comedies yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Filmler ve Eglence konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Filmler ve Eglence' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Filmler ve Eglence konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (cartoon/documentary/character) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Filmler ve Eglence temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Filmler ve Eglence konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Film turlerini ve tercihlerini anlatabilir, film incelemesi yazabilir.",
    },
    {
        "week": 24,
        "theme": "Review & Project Week 2",
        "theme_tr": "Tekrar ve Proje Haftasi 2",
        "vocab": [],
        "structure": "Unite 4-6 genel tekrar: Mevsimler, Yiyecek, Hobiler konulari",
        "skills": {
            "listening": "Genel tekrar dinleme aktiviteleri.",
            "speaking": "Sinif ici mini sunumlar: hobi tanitimi + film incelemesi.",
            "reading": "Karisik metin okuma ve anlama.",
            "writing": "Hobi dergisi projesi yazma.",
        },
        "linked_content": {
            "categories": ["Tekrar", "Proje"],
            "songs": [],
            "games": ["Buyuk Quiz", "Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Hobi Dergisi Projesi"],
            "grammar": ["Unite 4-6 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Karisik Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 4-6 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — karisik temali dinleme aktiviteleri"],
            "tue": ["Ana Ders: Gramer odak — Unite 4-6 gramer yapilari genel tekrar", "Beceri Lab: Konusma — sinif ici mini sunumlar"],
            "wed": ["Ana Ders: Okuma — karisik metin okuma ve anlama sorulari", "Beceri Lab: Yazma — Hobi Dergisi projesi yazma"],
            "thu": ["Ana Ders: Proje hazirlama ve sunum provasi", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 4-6 genel degerlendirme + hobi dergisi projesi.",
    },
    # ===== UNIT 7: Animals & Nature (Weeks 25-27) =====
    {
        "week": 25,
        "theme": "Animals & Nature",
        "theme_tr": "Hayvanlar ve Doga",
        "vocab": ["elephant", "giraffe", "penguin", "dolphin", "eagle", "snake", "habitat", "wild",
                  "domestic", "endangered", "species", "jungle", "ocean", "desert", "forest"],
        "structure": "Elephants live in Africa. They eat grass. A penguin can swim but it can't fly.",
        "skills": {
            "listening": "Hayvan belgeselini dinler, hayvanlarin ozelliklerini saptar.",
            "speaking": "Sevdigi hayvani tanitir, ozelliklerini anlatir.",
            "reading": "Hayvan ansiklopedisinden bir madde okur, bilgileri cikarir.",
            "writing": "Bir hayvani tanitici metin yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Doga", "Hayvanlar"],
            "songs": ["Animal Song"],
            "games": ["Hayvan Tahmin", "Habitat Eslestir"],
            "dialogues": ["At the Zoo"],
            "readings": ["Amazing Animals"],
            "writings": ["My Favourite Animal"],
            "grammar": ["Simple Present for facts + can/can't for ability"],
            "phonics": ["/ŋ/ sound practice"],
            "listening": ["Hayvan Belgeseli"],
        },
        "days": {
            "mon": ["Ana Ders: Hayvanlar ve Doga temel kelimelerini tanitim (elephant/giraffe/penguin) + yapi sunumu: Elephants live in Africa. They eat grass", "Beceri Lab: Dinleme — 'Hayvanlar ve Doga' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Elephants live in Africa. They eat grass yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Hayvanlar ve Doga konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Hayvanlar ve Doga' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Hayvanlar ve Doga konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (dolphin/eagle/snake) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Hayvanlar ve Doga temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Hayvanlar ve Doga konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir hayvani habitat ve ozellikleriyle tanitabilir.",
    },
    {
        "week": 26,
        "theme": "At the Zoo",
        "theme_tr": "Hayvanat Bahcesinde",
        "vocab": ["zoo", "cage", "aquarium", "keeper", "feed", "exhibit", "sign", "entrance",
                  "exit", "guide", "tour", "nocturnal", "mammal", "reptile", "insect"],
        "structure": "The lions are in the big cage. Don't feed the animals! I saw a parrot yesterday.",
        "skills": {
            "listening": "Zoo rehberinin anlatimini dinler, hayvanlari ve yerlerini saptar.",
            "speaking": "Hayvanat bahcesi gezisini anlatir, izlenimleri paylasir.",
            "reading": "Hayvanat bahcesi brosurunu okur, bilgileri cikarir.",
            "writing": "Hayvanat bahcesi gezisi hakkinda gunluk yazisi yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Hayvanlar", "Geziler"],
            "songs": [],
            "games": ["Zoo Haritasi", "Hayvan Sinifla"],
            "dialogues": ["At the Zoo Entrance"],
            "readings": ["A Day at the Zoo"],
            "writings": ["My Zoo Visit"],
            "grammar": ["Simple Past (regular) + Don't + imperative"],
            "phonics": ["-ed pronunciation /t/ /d/ /ɪd/"],
            "listening": ["Zoo Rehberi"],
        },
        "days": {
            "mon": ["Ana Ders: Hayvanat Bahcesinde temel kelimelerini tanitim (zoo/cage/aquarium) + yapi sunumu: The lions are in the big cage. Don't feed the animals!", "Beceri Lab: Dinleme — 'Hayvanat Bahcesinde' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — The lions are in the big cage. Don't feed the animals! yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Hayvanat Bahcesinde konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Hayvanat Bahcesinde' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Hayvanat Bahcesinde konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (keeper/feed/exhibit) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Hayvanat Bahcesinde temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Hayvanat Bahcesinde konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hayvanat bahcesi gezisini Simple Past ile anlatabilir.",
    },
    {
        "week": 27,
        "theme": "Protecting Nature",
        "theme_tr": "Dogayi Korumak",
        "vocab": ["pollution", "recycle", "reduce", "reuse", "waste", "plastic", "energy", "solar",
                  "plant", "protect", "environment", "global warming", "eco-friendly", "bin", "compost"],
        "structure": "We should recycle paper. Don't waste water! Pollution is a big problem.",
        "skills": {
            "listening": "Cevre koruma kampanyasini dinler, onemli mesajlari saptar.",
            "speaking": "Cevre koruma icin yapilabilecekleri anlatir.",
            "reading": "Cevre koruma posterini/metnini okur, onerileri listeler.",
            "writing": "Cevre koruma posteri/slogan + kisa metin yazar.",
        },
        "linked_content": {
            "categories": ["Doga", "Cevre"],
            "songs": ["Save the Earth Song"],
            "games": ["Geri Donusum Sinifla", "Cevre Quiz"],
            "dialogues": ["How Can We Save the Planet?"],
            "readings": ["Going Green"],
            "writings": ["My Green Promise"],
            "grammar": ["should/must + imperatives for advice"],
            "phonics": ["/ɜː/ sound practice"],
            "listening": ["Cevre Kampanyasi"],
        },
        "days": {
            "mon": ["Ana Ders: Dogayi Korumak temel kelimelerini tanitim (pollution/recycle/reduce) + yapi sunumu: We should recycle paper. Don't waste water!", "Beceri Lab: Dinleme — 'Dogayi Korumak' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — We should recycle paper. Don't waste water! yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dogayi Korumak konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dogayi Korumak' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dogayi Korumak konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (reuse/waste/plastic) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dogayi Korumak temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dogayi Korumak konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Cevre koruma onerileri should/must ile ifade edebilir.",
    },
    # ===== UNIT 8: Summer Holidays (Weeks 28-30) =====
    {
        "week": 28,
        "theme": "Summer Holidays",
        "theme_tr": "Yaz Tatili",
        "vocab": ["holiday", "vacation", "beach", "sunbathe", "swim", "sightseeing", "souvenir",
                  "luggage", "passport", "boarding pass", "flight", "hotel", "resort", "adventure", "itinerary"],
        "structure": "I'm going to visit my grandparents. We are going to go to the beach. Are you going to travel?",
        "skills": {
            "listening": "Tatil planlarini dinler, destinasyonlari ve aktiviteleri saptar.",
            "speaking": "Yaz tatili planlarini going to ile anlatir.",
            "reading": "Tatil brosurunu/blogunu okur, bilgileri cikarir.",
            "writing": "Yaz tatili planini going to ile yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Tatil", "Seyahat"],
            "songs": ["Holiday Song"],
            "games": ["Tatil Planlama", "Destinasyon Eslestir"],
            "dialogues": ["Where Are You Going This Summer?"],
            "readings": ["Summer Holiday Plans"],
            "writings": ["My Summer Holiday Plan"],
            "grammar": ["going to for future plans"],
            "phonics": ["/əʊ/ vs /aʊ/ sounds"],
            "listening": ["Tatil Planlari"],
        },
        "days": {
            "mon": ["Ana Ders: Yaz Tatili temel kelimelerini tanitim (holiday/vacation/beach) + yapi sunumu: I'm going to visit my grandparents", "Beceri Lab: Dinleme — 'Yaz Tatili' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I'm going to visit my grandparents yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yaz Tatili konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yaz Tatili' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yaz Tatili konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (sunbathe/swim/sightseeing) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yaz Tatili temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yaz Tatili konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yaz tatili planlarini going to ile anlatabilir.",
    },
    {
        "week": 29,
        "theme": "Travel Experiences",
        "theme_tr": "Seyahat Deneyimleri",
        "vocab": ["travel", "journey", "trip", "explore", "discover", "visit", "stay",
                  "guide", "map", "camera", "memory", "experience", "amazing", "unforgettable", "traditional"],
        "structure": "Last summer, I went to Antalya. We stayed at a hotel. It was amazing!",
        "skills": {
            "listening": "Seyahat anlatimini dinler, yerleri ve aktiviteleri saptar.",
            "speaking": "Gecmis seyahat deneyimini anlatir.",
            "reading": "Seyahat blogunu okur, onemli bilgileri cikarir.",
            "writing": "Bir seyahat deneyimini Simple Past ile yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Seyahat"],
            "songs": [],
            "games": ["Seyahat Hikayesi", "Nereye Gittim?"],
            "dialogues": ["How Was Your Trip?"],
            "readings": ["A Trip to Cappadocia"],
            "writings": ["My Best Trip"],
            "grammar": ["Simple Past (regular + irregular)"],
            "phonics": ["-ed endings revision"],
            "listening": ["Seyahat Anlatimi"],
        },
        "days": {
            "mon": ["Ana Ders: Seyahat Deneyimleri temel kelimelerini tanitim (travel/journey/trip) + yapi sunumu: Last summer, I went to Antalya", "Beceri Lab: Dinleme — 'Seyahat Deneyimleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Last summer, I went to Antalya yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Seyahat Deneyimleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Seyahat Deneyimleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Seyahat Deneyimleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (explore/discover/visit) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Seyahat Deneyimleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Seyahat Deneyimleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Gecmis seyahat deneyimini Simple Past ile anlatabilir.",
    },
    {
        "week": 30,
        "theme": "Planning a Trip",
        "theme_tr": "Seyahat Planlama",
        "vocab": ["destination", "accommodation", "reservation", "budget", "schedule", "pack",
                  "checklist", "transportation", "currency", "visa", "insurance", "weather forecast", "suitcase", "backpack", "agency"],
        "structure": "First, we are going to book a hotel. Then, we are going to pack our suitcases.",
        "skills": {
            "listening": "Seyahat planlama diyalogunu dinler, adimlari siralar.",
            "speaking": "Bir seyahat planini adim adim anlatir.",
            "reading": "Seyahat rehberini okur, onemli bilgileri cikarir.",
            "writing": "Hayali bir seyahat plani yazar (destinasyon, konaklama, aktiviteler).",
        },
        "linked_content": {
            "categories": ["Seyahat", "Planlama"],
            "songs": [],
            "games": ["Seyahat Planlama Oyunu", "Bavul Hazirla"],
            "dialogues": ["Planning Our Trip"],
            "readings": ["Travel Guide: Istanbul"],
            "writings": ["My Dream Trip"],
            "grammar": ["going to + sequencing words (first, then, after that)"],
            "phonics": ["/eə/ vs /ɪə/ sounds"],
            "listening": ["Seyahat Planlama Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Seyahat Planlama temel kelimelerini tanitim (destination/accommodation/reservation) + yapi sunumu: First, we are going to book a hotel", "Beceri Lab: Dinleme — 'Seyahat Planlama' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — First, we are going to book a hotel yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Seyahat Planlama konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Seyahat Planlama' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Seyahat Planlama konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (budget/schedule/pack) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Seyahat Planlama temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Seyahat Planlama konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir seyahat planini going to ve siralama kelimeleriyle anlatabilir.",
    },
    # ===== UNIT 9: Jobs & Careers (Weeks 31-33) =====
    {
        "week": 31,
        "theme": "Jobs & Careers",
        "theme_tr": "Meslekler ve Kariyer",
        "vocab": ["doctor", "engineer", "teacher", "pilot", "firefighter", "chef", "dentist",
                  "vet", "architect", "journalist", "lawyer", "mechanic", "salary", "profession", "career"],
        "structure": "What do you want to be? I want to be a doctor. A teacher should be patient.",
        "skills": {
            "listening": "Meslek tanitimlarini dinler, meslekleri ve gorevleri eslestirir.",
            "speaking": "Gelecekteki meslegini ve nedenini anlatir.",
            "reading": "Meslek tanitim metnini okur, meslekleri karsilastirir.",
            "writing": "Olmak istedigi meslegi ve nedenini yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Meslekler"],
            "songs": ["When I Grow Up"],
            "games": ["Meslek Tahmin", "Pantomim"],
            "dialogues": ["What Do You Want to Be?"],
            "readings": ["Jobs and Duties"],
            "writings": ["My Dream Job"],
            "grammar": ["want to be + should/must/have to"],
            "phonics": ["/ʒ/ vs /dʒ/ sounds"],
            "listening": ["Meslek Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Meslekler ve Kariyer temel kelimelerini tanitim (doctor/engineer/teacher) + yapi sunumu: What do you want to be? I want to be a doctor", "Beceri Lab: Dinleme — 'Meslekler ve Kariyer' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What do you want to be? I want to be a doctor yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Meslekler ve Kariyer konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Meslekler ve Kariyer' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Meslekler ve Kariyer konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (pilot/firefighter/chef) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Meslekler ve Kariyer temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Meslekler ve Kariyer konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Meslekleri ve gorevlerini anlatabilir, gelecek planlarini ifade edebilir.",
    },
    {
        "week": 32,
        "theme": "Rules & Obligations",
        "theme_tr": "Kurallar ve Zorunluluklar",
        "vocab": ["rule", "obligation", "duty", "responsibility", "permission", "allow", "forbid",
                  "fine", "law", "traffic", "safety", "helmet", "seatbelt", "forbidden", "compulsory"],
        "structure": "You must wear a seatbelt. You have to be on time. You don't have to wear a uniform.",
        "skills": {
            "listening": "Kural ve zorunluluk ifadelerini dinler, siniflandirir.",
            "speaking": "Okul ve trafik kurallarini must/have to ile anlatir.",
            "reading": "Kural ve isaret metinlerini okur, zorunlu/yasak olanlari ayirir.",
            "writing": "Okul kurallari posteri hazirlar, must/have to/mustn't ile yazar.",
        },
        "linked_content": {
            "categories": ["Kurallar", "Gunluk Yasam"],
            "songs": [],
            "games": ["Kural Sinifla", "Isaret Eslestir"],
            "dialogues": ["What Are the Rules?"],
            "readings": ["School Rules & Traffic Rules"],
            "writings": ["Rules Poster"],
            "grammar": ["must/mustn't/have to/don't have to"],
            "phonics": ["/t/ vs /d/ final sounds"],
            "listening": ["Kural Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Kurallar ve Zorunluluklar temel kelimelerini tanitim (rule/obligation/duty) + yapi sunumu: You must wear a seatbelt. You have to be on time", "Beceri Lab: Dinleme — 'Kurallar ve Zorunluluklar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — You must wear a seatbelt. You have to be on time yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kurallar ve Zorunluluklar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kurallar ve Zorunluluklar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kurallar ve Zorunluluklar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (responsibility/permission/allow) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kurallar ve Zorunluluklar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kurallar ve Zorunluluklar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kural ve zorunluluklari must/have to ile ifade edebilir.",
    },
    {
        "week": 33,
        "theme": "Health & Illness",
        "theme_tr": "Saglik ve Hastalik",
        "vocab": ["headache", "stomachache", "toothache", "fever", "cough", "cold", "flu",
                  "medicine", "rest", "doctor", "nurse", "appointment", "symptom", "healthy", "ill"],
        "structure": "What's the matter? I have a headache. You should see a doctor.",
        "skills": {
            "listening": "Doktor-hasta diyalogunu dinler, semptomlari ve tavsiyeleri saptar.",
            "speaking": "Rahatsizligini ifade eder ve tavsiye verir.",
            "reading": "Saglik brosurunu okur, saglikli yasam ipuclarini listeler.",
            "writing": "Hastalandiginda ne yaptigini anlatan kisa bir metin yazar.",
        },
        "linked_content": {
            "categories": ["Saglik"],
            "songs": [],
            "games": ["Semptom Eslestir", "Doktor Roleplay"],
            "dialogues": ["At the Doctor's"],
            "readings": ["Stay Healthy!"],
            "writings": ["When I Am Ill"],
            "grammar": ["should/shouldn't for advice"],
            "phonics": ["/ʃ/ vs /tʃ/ sounds"],
            "listening": ["Doktor Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Saglik ve Hastalik temel kelimelerini tanitim (headache/stomachache/toothache) + yapi sunumu: What's the matter? I have a headache", "Beceri Lab: Dinleme — 'Saglik ve Hastalik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — What's the matter? I have a headache yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Saglik ve Hastalik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Saglik ve Hastalik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Saglik ve Hastalik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (fever/cough/cold) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Saglik ve Hastalik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Saglik ve Hastalik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Saglik sorunlarini ifade edip tavsiye verebilir.",
    },
    # ===== UNIT 10: Heritage & Digital Life (Weeks 34-36) =====
    {
        "week": 34,
        "theme": "Heritage & Digital Life",
        "theme_tr": "Kultur Mirasi ve Dijital Yasam",
        "vocab": ["heritage", "culture", "tradition", "monument", "museum", "ancient", "modern",
                  "digital", "internet", "website", "social media", "online", "technology", "device", "screen"],
        "structure": "Turkey has many historical places. The internet is important for learning. However, we must also protect our heritage.",
        "skills": {
            "listening": "Kultur mirasi ve dijital yasam hakkinda sunumu dinler, ana fikirleri saptar.",
            "speaking": "Kulturel miras ve dijital yasam arasinda dengeyi anlatir.",
            "reading": "Kultur ve teknoloji konulu metni okur, karsilastirmali analiz yapar.",
            "writing": "Kultur mirasi ve dijital yasam hakkinda kisa kompozisyon yazar (10 cumle).",
        },
        "linked_content": {
            "categories": ["Kultur", "Teknoloji"],
            "songs": [],
            "games": ["Tarih-Teknoloji Eslestir", "Quiz"],
            "dialogues": ["Old Traditions, New Technology"],
            "readings": ["Heritage Meets Digital"],
            "writings": ["My Cultural Heritage"],
            "grammar": ["Linking words (however, also, because, so)"],
            "phonics": ["/h/ sound practice"],
            "listening": ["Kultur ve Teknoloji Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Kultur Mirasi ve Dijital Yasam temel kelimelerini tanitim (heritage/culture/tradition) + yapi sunumu: Turkey has many historical places", "Beceri Lab: Dinleme — 'Kultur Mirasi ve Dijital Yasam' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Turkey has many historical places + baglac kullanimi yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kultur Mirasi ve Dijital Yasam konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kultur Mirasi ve Dijital Yasam' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kultur Mirasi ve Dijital Yasam konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (monument/museum/ancient) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kultur Mirasi ve Dijital Yasam temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kultur Mirasi ve Dijital Yasam konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kultur mirasi ve dijital yasami baglac kullanarak anlatabilir.",
    },
    {
        "week": 35,
        "theme": "End of Year Project",
        "theme_tr": "Yil Sonu Projesi",
        "vocab": [],
        "structure": "Yil boyunca ogrenilenler uzerine proje",
        "skills": {
            "listening": "Sinif arkadaslarinin projelerini dinler, geri bildirim verir.",
            "speaking": "Projesini 3-5 dakikalik sunumla sinifa anlatir.",
            "reading": "Proje icin arastirma yapar, kaynak okur.",
            "writing": "Proje raporunu yazar (giris, gelisme, sonuc).",
        },
        "linked_content": {
            "categories": ["Proje"],
            "songs": [],
            "games": [],
            "dialogues": [],
            "readings": [],
            "writings": ["Proje Raporu"],
            "grammar": ["Yil genel tekrar"],
            "phonics": ["Yil genel tekrar"],
            "listening": ["Sunum Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Yil Sonu Projesi — proje konusu secimi ve planlama", "Beceri Lab: Dinleme — ornek proje sunumlarini dinle, not al"],
            "tue": ["Ana Ders: Proje arastirma ve icerik hazirlama", "Beceri Lab: Konusma — proje sunumu provasi"],
            "wed": ["Ana Ders: Proje raporu yazma (giris, gelisme, sonuc)", "Beceri Lab: Yazma — proje raporunu duzenle ve tamamla"],
            "thu": ["Ana Ders: Proje sunumu provasi ve geri bildirim", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Proje sunumlari + geri bildirim + yil sonu degerlendirmesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yil sonu projesi: sunum + rapor degerlendirmesi.",
    },
    {
        "week": 36,
        "theme": "Final Review & Assessment",
        "theme_tr": "Yil Sonu Genel Degerlendirme",
        "vocab": [],
        "structure": "Tum yil konulari genel tekrar ve degerlendirme",
        "skills": {
            "listening": "Yil sonu genel dinleme degerlendirmesi.",
            "speaking": "Yil sonu sozlu sinav: secilen konuda 3-5 dakika sunum.",
            "reading": "Yil sonu genel okuma degerlendirmesi.",
            "writing": "Yil sonu genel yazma degerlendirmesi.",
        },
        "linked_content": {
            "categories": ["Degerlendirme"],
            "songs": [],
            "games": ["Final Jeopardy", "Buyuk Quiz"],
            "dialogues": [],
            "readings": [],
            "writings": ["Yil Sonu Yazma"],
            "grammar": ["Yil genel tekrar"],
            "phonics": ["Yil genel tekrar"],
            "listening": ["Yil Sonu Degerlendirme"],
        },
        "days": {
            "mon": ["Ana Ders: Yil Sonu Genel Degerlendirme — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — yil sonu dinleme degerlendirmesi"],
            "tue": ["Ana Ders: Gramer odak — tum yil gramer yapilari genel tekrar", "Beceri Lab: Konusma — yil sonu sozlu sinav"],
            "wed": ["Ana Ders: Okuma — yil sonu genel okuma degerlendirmesi", "Beceri Lab: Yazma — yil sonu genel yazma degerlendirmesi"],
            "thu": ["Ana Ders: Eksik konularin tekrari ve pekistirme", "Beceri Lab: Proje/Sunum — proje sunumlari"],
            "fri": ["Native Speaker: Yil sonu serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yil sonu genel degerlendirmesi: 4 beceri + proje notu.",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# 6. SINIF — CEFR A2.2 (Gelisim)
# Toplam: 10 saat/hafta = Main 4 + Skills 4 + Native 2
# ═══════════════════════════════════════════════════════════════════════════════

CURRICULUM_GRADE6 = [
    # ===== UNIT 1: Life in Two Worlds (Weeks 1-4) =====
    {
        "week": 1,
        "theme": "Life in Two Worlds",
        "theme_tr": "Iki Dunya Arasinda Yasam",
        "vocab": ["city", "countryside", "village", "urban", "rural", "crowded", "peaceful", "traffic",
                  "nature", "pollution", "neighbour", "field", "skyscraper", "barn", "commute"],
        "structure": "I have lived in Istanbul for 5 years. She has moved to a village. Have you ever lived in the countryside?",
        "skills": {
            "listening": "Sehir ve koy yasami karsilastirmasi dinler, farklari saptar.",
            "speaking": "Yasadigi yeri tanitir, sehir/koy avantaj ve dezavantajlarini tartisir.",
            "reading": "Sehir ve koy yasami hakkinda karsilastirmali metin okur (120 kelime).",
            "writing": "Sehir ve koy yasami karsilastirma paragraf yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Sehir", "Doga", "Gunluk Yasam"],
            "songs": ["City or Country?"],
            "games": ["Sehir-Koy Sinifla", "Avantaj-Dezavantaj"],
            "dialogues": ["Where Do You Prefer to Live?"],
            "readings": ["City Life vs Country Life"],
            "writings": ["My Ideal Place to Live"],
            "grammar": ["Present Perfect (for/since) + comparatives"],
            "phonics": ["/ɪ/ vs /iː/ contrast"],
            "listening": ["Sehir-Koy Karsilastirmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Iki Dunya Arasinda Yasam temel kelimelerini tanitim (city/countryside/village) + yapi sunumu: I have lived in Istanbul for 5 years", "Beceri Lab: Dinleme — 'Iki Dunya Arasinda Yasam' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I have lived in Istanbul for 5 years yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Iki Dunya Arasinda Yasam konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Iki Dunya Arasinda Yasam' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Iki Dunya Arasinda Yasam konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (urban/rural/crowded) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Iki Dunya Arasinda Yasam temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Iki Dunya Arasinda Yasam konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sehir ve koy yasami karsilastirmasi yapabilir, Present Perfect kullanabilir.",
    },
    {
        "week": 2,
        "theme": "Changes in Life",
        "theme_tr": "Hayattaki Degisimler",
        "vocab": ["change", "move", "improve", "develop", "grow up", "adapt", "modern", "progress",
                  "technology", "transport", "lifestyle", "population", "opportunity", "challenge", "experience"],
        "structure": "Life has changed a lot. People have started using smartphones. Technology has improved our lives.",
        "skills": {
            "listening": "Hayattaki degisimler hakkinda sunumu dinler, ana fikirleri saptar.",
            "speaking": "Hayatindaki ve cevresindeki degisimlerden bahseder.",
            "reading": "Teknoloji ve yasam degisimlerini anlatan metni okur.",
            "writing": "Son 10 yildaki degisimleri anlatan paragraf yazar.",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam", "Teknoloji"],
            "songs": [],
            "games": ["Gecmis-Simdi Eslestir", "Degisim Zaman Cizelgesi"],
            "dialogues": ["How Has Life Changed?"],
            "readings": ["Life Then and Now"],
            "writings": ["Changes in My Town"],
            "grammar": ["Present Perfect for changes + already/yet/just"],
            "phonics": ["/dʒ/ sound practice"],
            "listening": ["Degisim Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Hayattaki Degisimler temel kelimelerini tanitim (change/move/improve) + yapi sunumu: Life has changed a lot. People have started using smartphones", "Beceri Lab: Dinleme — 'Hayattaki Degisimler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Life has changed a lot. People have started using smartphones yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Hayattaki Degisimler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Hayattaki Degisimler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Hayattaki Degisimler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (develop/grow up/adapt) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Hayattaki Degisimler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Hayattaki Degisimler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hayattaki degisimleri Present Perfect ile anlatabilir.",
    },
    {
        "week": 3,
        "theme": "Comparing Places",
        "theme_tr": "Yerleri Karsilastirmak",
        "vocab": ["bigger", "smaller", "more crowded", "less polluted", "quieter", "noisier", "safer",
                  "more dangerous", "more expensive", "cheaper", "the most", "the least", "than", "as...as", "different from"],
        "structure": "Istanbul is bigger than Ankara. The countryside is quieter than the city. It's the most beautiful place I've ever seen.",
        "skills": {
            "listening": "Yer karsilastirma diyaloglarini dinler, karsilastirmalari saptar.",
            "speaking": "Iki yeri karsilastirarak anlatir.",
            "reading": "Iki sehri karsilastiran metin okur, farklari ve benzerlikleri listeler.",
            "writing": "Iki yeri karsilastiran paragraf yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Sehir", "Doga"],
            "songs": [],
            "games": ["Karsilastir Oyunu", "En Buyuk-En Kucuk"],
            "dialogues": ["Which City Is Better?"],
            "readings": ["Comparing Two Cities"],
            "writings": ["My Town vs the Capital"],
            "grammar": ["Comparatives + superlatives + as...as"],
            "phonics": ["/ə/ schwa sound"],
            "listening": ["Sehir Karsilastirmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Yerleri Karsilastirmak temel kelimelerini tanitim (bigger/smaller/more crowded) + yapi sunumu: Istanbul is bigger than Ankara", "Beceri Lab: Dinleme — 'Yerleri Karsilastirmak' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Istanbul is bigger than Ankara yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yerleri Karsilastirmak konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yerleri Karsilastirmak' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yerleri Karsilastirmak konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (less polluted/quieter/noisier) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yerleri Karsilastirmak temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yerleri Karsilastirmak konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Iki yeri comparative ve superlative yapilarla karsilastirabilir.",
    },
    {
        "week": 4,
        "theme": "My Dream Place",
        "theme_tr": "Hayal Ettigim Yer",
        "vocab": ["dream", "ideal", "imagine", "design", "create", "location", "facilities", "scenery",
                  "landscape", "community", "sustainable", "garden", "swimming pool", "playground", "cozy"],
        "structure": "My dream place has a big garden. It is near the sea. I would like to live in a quiet town.",
        "skills": {
            "listening": "Hayali yer tanitimini dinler, ozellikleri not eder.",
            "speaking": "Hayali yasam yerini detayli anlatir.",
            "reading": "Ideal yasam yeri hakkinda metin okur.",
            "writing": "Hayali yerini tanimlayan detayli paragraf yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Gunluk Yasam", "Hayal"],
            "songs": [],
            "games": ["Hayal Evi Tasarla", "Yer Tahmin"],
            "dialogues": ["Describe Your Dream Place"],
            "readings": ["My Dream Home"],
            "writings": ["The Place I'd Like to Live"],
            "grammar": ["would like to + there is/are + adjective order"],
            "phonics": ["/aɪ/ vs /eɪ/ sounds"],
            "listening": ["Hayal Yeri Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Hayal Ettigim Yer temel kelimelerini tanitim (dream/ideal/imagine) + yapi sunumu: My dream place has a big garden. It is near the sea", "Beceri Lab: Dinleme — 'Hayal Ettigim Yer' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — My dream place has a big garden. It is near the sea yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Hayal Ettigim Yer konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Hayal Ettigim Yer' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Hayal Ettigim Yer konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (design/create/location) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Hayal Ettigim Yer temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Hayal Ettigim Yer konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hayali yasam yerini detayli tanimlayabilir.",
    },
    # ===== UNIT 2: Famous People (Weeks 5-8) =====
    {
        "week": 5,
        "theme": "Famous People",
        "theme_tr": "Unlu Kisiler",
        "vocab": ["biography", "achievement", "discover", "invent", "explore", "inspire", "born",
                  "childhood", "education", "career", "award", "famous", "successful", "contribution", "legacy"],
        "structure": "Ataturk was born in 1881. He founded the Republic. She has won many awards. Did he discover anything?",
        "skills": {
            "listening": "Unlu kisi biyografisi dinler, onemli tarihleri ve olaylari saptar.",
            "speaking": "Unlu bir kisiyi biyografik bilgilerle tanitir.",
            "reading": "Biyografi metnini okur (150 kelime), bilgileri cikarir.",
            "writing": "Hayranligi olduklarini bir kisiyi biyografi paragraf ile yazar.",
        },
        "linked_content": {
            "categories": ["Insanlar", "Tarih"],
            "songs": [],
            "games": ["Kim Bu Unlu?", "Biyografi Eslestir"],
            "dialogues": ["Tell Me About a Famous Person"],
            "readings": ["The Life of Marie Curie"],
            "writings": ["A Person I Admire"],
            "grammar": ["Past Simple vs Present Perfect"],
            "phonics": ["/ɜː/ vs /ɔː/ sounds"],
            "listening": ["Biyografi Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unlu Kisiler temel kelimelerini tanitim (biography/achievement/discover) + yapi sunumu: Ataturk was born in 1881. He founded the Republic", "Beceri Lab: Dinleme — 'Unlu Kisiler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Past Simple vs Present Perfect yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Unlu Kisiler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Unlu Kisiler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Unlu Kisiler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (invent/explore/inspire) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Unlu Kisiler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Unlu Kisiler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unlu bir kisiyi Past Simple ve Present Perfect ile tanitabilir.",
    },
    {
        "week": 6,
        "theme": "Historical Figures",
        "theme_tr": "Tarihi Sahsiyetler",
        "vocab": ["emperor", "sultan", "warrior", "philosopher", "scientist", "artist", "leader",
                  "battle", "empire", "reign", "conquer", "unite", "reform", "revolution", "independence"],
        "structure": "He was a great leader. He conquered many lands. The empire lasted for 600 years.",
        "skills": {
            "listening": "Tarihi kisi anlatimini dinler, onemli olaylari siralar.",
            "speaking": "Bir tarihi sahsiyeti kronolojik olarak anlatir.",
            "reading": "Tarihi metin okur, olaylari zaman cizelgesine yerlestirir.",
            "writing": "Bir tarihi sahsiyetin hayatini kronolojik olarak yazar.",
        },
        "linked_content": {
            "categories": ["Tarih", "Insanlar"],
            "songs": [],
            "games": ["Tarih Zaman Cizelgesi", "Kim Bu Sahsiyet?"],
            "dialogues": ["Who Was This Leader?"],
            "readings": ["Great Leaders in History"],
            "writings": ["A Historical Figure I Admire"],
            "grammar": ["Past Simple (irregular verbs) + time expressions"],
            "phonics": ["/ɒ/ vs /əʊ/ sounds"],
            "listening": ["Tarihi Sahsiyet Anlatimi"],
        },
        "days": {
            "mon": ["Ana Ders: Tarihi Sahsiyetler temel kelimelerini tanitim (emperor/sultan/warrior) + yapi sunumu: He was a great leader. He conquered many lands", "Beceri Lab: Dinleme — 'Tarihi Sahsiyetler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — He was a great leader. He conquered many lands yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Tarihi Sahsiyetler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Tarihi Sahsiyetler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Tarihi Sahsiyetler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (philosopher/scientist/artist) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Tarihi Sahsiyetler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Tarihi Sahsiyetler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir tarihi sahsiyeti Past Simple ile kronolojik anlatabilir.",
    },
    {
        "week": 7,
        "theme": "Modern Heroes",
        "theme_tr": "Modern Kahramanlar",
        "vocab": ["hero", "volunteer", "donate", "charity", "courage", "sacrifice", "rescue",
                  "humanitarian", "role model", "influence", "motivate", "dedicate", "honour", "medal", "ceremony"],
        "structure": "She has helped thousands of people. He has dedicated his life to education. Have you ever volunteered?",
        "skills": {
            "listening": "Modern kahraman hikayesini dinler, basarilarini saptar.",
            "speaking": "Kendisi icin kahraman olan birini tanitir.",
            "reading": "Gonullu/hayirsever hakkinda metin okur.",
            "writing": "Kendisi icin kahraman olan kisiyi anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Insanlar", "Toplum"],
            "songs": ["Heroes Song"],
            "games": ["Kahraman Eslestir", "Basari Hikayesi"],
            "dialogues": ["Who Is Your Hero?"],
            "readings": ["Modern Day Heroes"],
            "writings": ["My Hero"],
            "grammar": ["Present Perfect + ever/never + for/since"],
            "phonics": ["/h/ vs silent h"],
            "listening": ["Kahraman Hikayesi"],
        },
        "days": {
            "mon": ["Ana Ders: Modern Kahramanlar temel kelimelerini tanitim (hero/volunteer/donate) + yapi sunumu: She has helped thousands of people", "Beceri Lab: Dinleme — 'Modern Kahramanlar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — She has helped thousands of people yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Modern Kahramanlar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Modern Kahramanlar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Modern Kahramanlar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (charity/courage/sacrifice) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Modern Kahramanlar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Modern Kahramanlar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir modern kahramani Present Perfect ile tanitabilir.",
    },
    {
        "week": 8,
        "theme": "Review & Biography Project",
        "theme_tr": "Tekrar ve Biyografi Projesi",
        "vocab": [],
        "structure": "Unite 1-2 genel tekrar: Yasam karsilastirmasi ve unlu kisiler",
        "skills": {
            "listening": "Genel tekrar dinleme aktiviteleri.",
            "speaking": "Biyografi sunumu: secilen unlu kisi hakkinda 3-5 dakika sunum.",
            "reading": "Karisik metin okuma ve anlama.",
            "writing": "Biyografi projesi yazma.",
        },
        "linked_content": {
            "categories": ["Tekrar", "Proje"],
            "songs": [],
            "games": ["Buyuk Quiz", "Biyografi Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Biyografi Projesi"],
            "grammar": ["Unite 1-2 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Karisik Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 1-2 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — karisik temali dinleme aktiviteleri"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect vs Past Simple genel tekrar", "Beceri Lab: Konusma — biyografi sunumu provasi"],
            "wed": ["Ana Ders: Okuma — karisik metin okuma ve anlama sorulari", "Beceri Lab: Yazma — biyografi projesi yazma"],
            "thu": ["Ana Ders: Proje hazirlama ve sunum provasi", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 1-2 genel degerlendirme + biyografi projesi.",
    },
    # ===== UNIT 3: My Home (Weeks 9-12) =====
    {
        "week": 9,
        "theme": "My Home",
        "theme_tr": "Evim",
        "vocab": ["living room", "bedroom", "kitchen", "bathroom", "balcony", "garage", "attic",
                  "basement", "furniture", "sofa", "cupboard", "wardrobe", "shelf", "carpet", "curtain"],
        "structure": "There are three bedrooms in my house. The sofa is in front of the window. My room is next to the kitchen.",
        "skills": {
            "listening": "Ev tanitimini dinler, odalari ve esyalari haritada isaretler.",
            "speaking": "Evini ve odasini detayli tanitir.",
            "reading": "Ev ilanini/tanitimini okur, bilgileri cikarir.",
            "writing": "Evini ve odasini detayli tanimlayan yazi yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Ev", "Gunluk Yasam"],
            "songs": ["My House Song"],
            "games": ["Oda Eslestir", "Esya Nerede?"],
            "dialogues": ["Welcome to My Home"],
            "readings": ["House for Sale"],
            "writings": ["My Room"],
            "grammar": ["There is/are + prepositions of place (in/on/under/next to/between)"],
            "phonics": ["/aʊ/ sound practice"],
            "listening": ["Ev Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Evim temel kelimelerini tanitim (living room/bedroom/kitchen) + yapi sunumu: There are three bedrooms in my house", "Beceri Lab: Dinleme — 'Evim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — There are three bedrooms in my house yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Evim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Evim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Evim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (bathroom/balcony/garage) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Evim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Evim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Evini ve odasini prepositions kullanarak detayli tanitabilir.",
    },
    {
        "week": 10,
        "theme": "Room Design",
        "theme_tr": "Oda Tasarimi",
        "vocab": ["design", "decorate", "paint", "wallpaper", "poster", "lamp", "desk", "chair",
                  "mirror", "rug", "plant", "colour", "style", "modern", "cozy"],
        "structure": "I'd like to paint my room blue. I'm going to put a poster on the wall. There should be a desk near the window.",
        "skills": {
            "listening": "Oda tasarimi tavsiyelerini dinler, fikirleri not eder.",
            "speaking": "Hayali odasini tasarlayip anlatir.",
            "reading": "Ic dekorasyon dergisi metnini okur.",
            "writing": "Hayali odasinin tasarimini detayli yazar.",
        },
        "linked_content": {
            "categories": ["Ev", "Tasarim"],
            "songs": [],
            "games": ["Oda Tasarla", "Eslestir"],
            "dialogues": ["How Would You Design Your Room?"],
            "readings": ["Cool Room Ideas"],
            "writings": ["My Dream Room"],
            "grammar": ["going to + would like to + should for suggestions"],
            "phonics": ["/uː/ vs /ʊ/ sounds"],
            "listening": ["Oda Tasarimi Tavsiyeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Oda Tasarimi temel kelimelerini tanitim (design/decorate/paint) + yapi sunumu: I'd like to paint my room blue", "Beceri Lab: Dinleme — 'Oda Tasarimi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I'd like to paint my room blue yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Oda Tasarimi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Oda Tasarimi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Oda Tasarimi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (wallpaper/poster/lamp) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Oda Tasarimi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Oda Tasarimi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hayali odasini going to ve would like to ile tanimlayabilir.",
    },
    {
        "week": 11,
        "theme": "Household Chores",
        "theme_tr": "Ev Isleri",
        "vocab": ["clean", "tidy up", "wash dishes", "do laundry", "vacuum", "iron", "cook",
                  "sweep", "mop", "take out rubbish", "water plants", "set the table", "make the bed", "dust", "chore"],
        "structure": "I always make my bed. She has to wash the dishes. We should share the housework.",
        "skills": {
            "listening": "Ev isleri dagitimi hakkinda diyalogu dinler, gorevleri saptar.",
            "speaking": "Evdeki gorev dagitimini anlatir.",
            "reading": "Ev isleri cizelgesini okur, bilgileri cikarir.",
            "writing": "Haftalik ev isleri cizelgesi hazirlar ve anlatir.",
        },
        "linked_content": {
            "categories": ["Ev", "Gunluk Yasam"],
            "songs": ["Chores Song"],
            "games": ["Gorev Dagit", "Ev Isi Eslestir"],
            "dialogues": ["Can You Help at Home?"],
            "readings": ["Sharing Housework"],
            "writings": ["My Chore Schedule"],
            "grammar": ["have to/don't have to + should + frequency adverbs"],
            "phonics": ["/tʃ/ vs /ʃ/ sounds"],
            "listening": ["Ev Isleri Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Ev Isleri temel kelimelerini tanitim (clean/tidy up/wash dishes) + yapi sunumu: I always make my bed. She has to wash the dishes", "Beceri Lab: Dinleme — 'Ev Isleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I always make my bed. She has to wash the dishes yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Ev Isleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Ev Isleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Ev Isleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (do laundry/vacuum/iron) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Ev Isleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Ev Isleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Ev islerini have to/should ile anlatabilir, gorev dagitimi yapabilir.",
    },
    {
        "week": 12,
        "theme": "Homes Around the World",
        "theme_tr": "Dunyanin Farkli Evleri",
        "vocab": ["igloo", "houseboat", "treehouse", "tent", "cottage", "mansion", "apartment",
                  "hut", "palace", "castle", "traditional", "unusual", "material", "brick", "wood"],
        "structure": "In some countries, people live in houseboats. An igloo is made of ice. Which type of house would you prefer?",
        "skills": {
            "listening": "Farkli ev turlerini anlatan sunumu dinler.",
            "speaking": "Farkli ev turlerini karsilastirarak anlatir.",
            "reading": "Dunya evleri hakkinda metin okur, siniflandirir.",
            "writing": "En ilginc buldugu ev turunu tanimlayan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Ev", "Kultur"],
            "songs": [],
            "games": ["Ev Turu Eslestir", "Ulke-Ev"],
            "dialogues": ["What Kind of House Is This?"],
            "readings": ["Unusual Homes"],
            "writings": ["The Most Interesting House"],
            "grammar": ["is made of + passive voice introduction"],
            "phonics": ["/eɪ/ vs /aɪ/ sounds"],
            "listening": ["Dunya Evleri Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Dunyanin Farkli Evleri temel kelimelerini tanitim (igloo/houseboat/treehouse) + yapi sunumu: In some countries, people live in houseboats", "Beceri Lab: Dinleme — 'Dunyanin Farkli Evleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — In some countries, people live in houseboats yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dunyanin Farkli Evleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dunyanin Farkli Evleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dunyanin Farkli Evleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (tent/cottage/mansion) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dunyanin Farkli Evleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dunyanin Farkli Evleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Farkli ev turlerini tanimlayip karsilastirabilir.",
    },
    # ===== UNIT 4: First Experiences (Weeks 13-16) =====
    {
        "week": 13,
        "theme": "First Experiences",
        "theme_tr": "Ilk Deneyimler",
        "vocab": ["experience", "first time", "nervous", "excited", "surprised", "amazed", "scared",
                  "proud", "disappointed", "embarrassed", "adventure", "challenge", "overcome", "memory", "unforgettable"],
        "structure": "Have you ever ridden a horse? I have never been abroad. She has already tried sushi.",
        "skills": {
            "listening": "Ilk deneyim hikayelerini dinler, duygulari ve olaylari saptar.",
            "speaking": "Ilk deneyimlerini ever/never ile paylasir.",
            "reading": "Ilk deneyim hikayesini okur (150 kelime), sorulari cevaplar.",
            "writing": "Unutulmaz bir ilk deneyimini anlatan yazi yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Deneyimler", "Duygular"],
            "songs": ["First Time Song"],
            "games": ["Hic... Yaptin mi?", "Deneyim Bingo"],
            "dialogues": ["Have You Ever...?"],
            "readings": ["My First Adventure"],
            "writings": ["An Unforgettable First"],
            "grammar": ["Present Perfect + ever/never/already/yet"],
            "phonics": ["/ɪə/ vs /eə/ sounds"],
            "listening": ["Ilk Deneyim Hikayeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Ilk Deneyimler temel kelimelerini tanitim (experience/first time/nervous) + yapi sunumu: Have you ever ridden a horse?", "Beceri Lab: Dinleme — 'Ilk Deneyimler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Have you ever ridden a horse? yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Ilk Deneyimler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Ilk Deneyimler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Ilk Deneyimler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (excited/surprised/amazed) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Ilk Deneyimler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Ilk Deneyimler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Ilk deneyimlerini Present Perfect ever/never ile anlatabilir.",
    },
    {
        "week": 14,
        "theme": "Emotions & Feelings",
        "theme_tr": "Duygular ve Hisler",
        "vocab": ["happy", "sad", "angry", "frightened", "anxious", "jealous", "grateful", "lonely",
                  "confident", "ashamed", "relieved", "thrilled", "homesick", "hopeful", "emotion"],
        "structure": "I felt really nervous. She was thrilled about the news. How did you feel when...?",
        "skills": {
            "listening": "Duygu ifadelerini dinler, durumlari ve duygulari eslestirir.",
            "speaking": "Duygularini ifade eder, baskalarinin duygularini sorar.",
            "reading": "Duygu gunlugu/metni okur, duygulari analiz eder.",
            "writing": "Farkli duygular yasadigi bir gunu anlatan gunluk yazar.",
        },
        "linked_content": {
            "categories": ["Duygular"],
            "songs": ["Feelings Song"],
            "games": ["Duygu Eslestir", "Yuz Ifadesi Tahmin"],
            "dialogues": ["How Do You Feel?"],
            "readings": ["A Day Full of Emotions"],
            "writings": ["My Emotion Diary"],
            "grammar": ["felt/was/were + adjectives for emotions"],
            "phonics": ["/æ/ vs /e/ sounds"],
            "listening": ["Duygu Ifadeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Duygular ve Hisler temel kelimelerini tanitim (happy/sad/angry) + yapi sunumu: I felt really nervous. She was thrilled", "Beceri Lab: Dinleme — 'Duygular ve Hisler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I felt really nervous. She was thrilled yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Duygular ve Hisler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Duygular ve Hisler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Duygular ve Hisler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (frightened/anxious/jealous) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Duygular ve Hisler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Duygular ve Hisler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Duygularini cesitli sifatlarla ifade edebilir.",
    },
    {
        "week": 15,
        "theme": "Achievements & Goals",
        "theme_tr": "Basarilar ve Hedefler",
        "vocab": ["achieve", "goal", "target", "dream", "succeed", "fail", "try", "effort",
                  "practice", "improve", "certificate", "competition", "prize", "scholarship", "determination"],
        "structure": "I have achieved my goal. She hasn't finished yet. He has already won the competition.",
        "skills": {
            "listening": "Basari hikayelerini dinler, hedef ve sonuclari saptar.",
            "speaking": "Kendi basarilarini ve hedeflerini anlatir.",
            "reading": "Ogrenci basari hikayesini okur.",
            "writing": "Hedeflerini ve planlarini anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Basari", "Motivasyon"],
            "songs": [],
            "games": ["Hedef Tablosu", "Basari Hikayesi"],
            "dialogues": ["What Are Your Goals?"],
            "readings": ["A Student's Success Story"],
            "writings": ["My Goals and Plans"],
            "grammar": ["Present Perfect + already/yet/just + goal expressions"],
            "phonics": ["/iː/ vs /ɪ/ minimal pairs"],
            "listening": ["Basari Hikayeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Basarilar ve Hedefler temel kelimelerini tanitim (achieve/goal/target) + yapi sunumu: I have achieved my goal", "Beceri Lab: Dinleme — 'Basarilar ve Hedefler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I have achieved my goal yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Basarilar ve Hedefler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Basarilar ve Hedefler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Basarilar ve Hedefler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (dream/succeed/fail) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Basarilar ve Hedefler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Basarilar ve Hedefler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Basarilarini ve hedeflerini Present Perfect ile anlatabilir.",
    },
    {
        "week": 16,
        "theme": "Midterm Review & Assessment",
        "theme_tr": "Ara Sinav Tekrari ve Degerlendirme",
        "vocab": [],
        "structure": "Unite 1-4 genel tekrar ve degerlendirme",
        "skills": {
            "listening": "Ara sinav dinleme degerlendirmesi.",
            "speaking": "Ara sinav sozlu degerlendirme.",
            "reading": "Ara sinav okuma degerlendirmesi.",
            "writing": "Ara sinav yazma degerlendirmesi.",
        },
        "linked_content": {
            "categories": ["Degerlendirme"],
            "songs": [],
            "games": ["Buyuk Quiz", "Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Ara Sinav Yazma"],
            "grammar": ["Unite 1-4 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Ara Sinav Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 1-4 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — ara sinav dinleme degerlendirmesi"],
            "tue": ["Ana Ders: Gramer odak — Unite 1-4 gramer yapilari genel tekrar", "Beceri Lab: Konusma — ara sinav sozlu degerlendirme"],
            "wed": ["Ana Ders: Okuma — ara sinav okuma degerlendirmesi", "Beceri Lab: Yazma — ara sinav yazma degerlendirmesi"],
            "thu": ["Ana Ders: Eksik konularin tekrari ve pekistirme alishtirmalari", "Beceri Lab: Proje/Sunum — donem sonu mini proje sunumlari"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 1-4 ara sinav: 4 beceri degerlendirmesi.",
    },
    # ===== UNIT 5: World Food (Weeks 17-20) =====
    {
        "week": 17,
        "theme": "World Food",
        "theme_tr": "Dunya Mutfagi",
        "vocab": ["cuisine", "dish", "recipe", "ingredient", "spice", "flavour", "taste", "serve",
                  "traditional", "street food", "appetizer", "main course", "dessert", "beverage", "portion"],
        "structure": "Turkish cuisine is famous for kebab. This dish is made with rice and vegetables. Have you ever tried sushi?",
        "skills": {
            "listening": "Dunya mutfaklari hakkinda sunumu dinler, yemekleri ve ulkeleri eslestirir.",
            "speaking": "Ulkelerin yemek kulturlerini anlatir, karsilastirir.",
            "reading": "Dunya yemekleri hakkinda metin okur (150 kelime).",
            "writing": "Bir ulkenin mutfagini tanitan yazi yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Yiyecek", "Kultur"],
            "songs": ["Food Around the World"],
            "games": ["Yemek-Ulke Eslestir", "Lezzet Tahmin"],
            "dialogues": ["What's Your Favourite Cuisine?"],
            "readings": ["Street Food Around the World"],
            "writings": ["A Famous Dish from My Country"],
            "grammar": ["is made with/of + countable/uncountable review"],
            "phonics": ["/ʊ/ vs /uː/ sounds"],
            "listening": ["Dunya Mutfagi Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Dunya Mutfagi temel kelimelerini tanitim (cuisine/dish/recipe) + yapi sunumu: Turkish cuisine is famous for kebab", "Beceri Lab: Dinleme — 'Dunya Mutfagi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Turkish cuisine is famous for kebab yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dunya Mutfagi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dunya Mutfagi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dunya Mutfagi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (ingredient/spice/flavour) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dunya Mutfagi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dunya Mutfagi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Dunya mutfaklarini tanitip karsilastirabilir.",
    },
    {
        "week": 18,
        "theme": "Cooking & Recipes",
        "theme_tr": "Yemek Yapma ve Tarifler",
        "vocab": ["chop", "slice", "stir", "boil", "fry", "bake", "grill", "mix",
                  "peel", "pour", "add", "measure", "oven", "pan", "bowl"],
        "structure": "First, chop the onions. Then, fry them in oil. After that, add the tomatoes. Finally, serve hot.",
        "skills": {
            "listening": "Yemek tarifi anlatimini dinler, adimlari siralar.",
            "speaking": "Bir yemek tarifini adim adim anlatir.",
            "reading": "Yemek tarifi okur, malzemeleri ve adimlari listeler.",
            "writing": "En sevdigi yemegin tarifini adim adim yazar.",
        },
        "linked_content": {
            "categories": ["Yiyecek"],
            "songs": [],
            "games": ["Tarif Siralama", "Malzeme Eslestir"],
            "dialogues": ["How Do You Make This?"],
            "readings": ["Easy Recipes for Students"],
            "writings": ["My Favourite Recipe"],
            "grammar": ["Imperatives + sequencing words (first/then/after that/finally)"],
            "phonics": ["/ɔɪ/ sound practice"],
            "listening": ["Yemek Tarifi Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Yemek Yapma ve Tarifler temel kelimelerini tanitim (chop/slice/stir) + yapi sunumu: First, chop the onions. Then, fry them in oil", "Beceri Lab: Dinleme — 'Yemek Yapma ve Tarifler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — First, chop the onions. Then, fry them in oil yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yemek Yapma ve Tarifler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yemek Yapma ve Tarifler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yemek Yapma ve Tarifler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (boil/fry/bake) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yemek Yapma ve Tarifler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yemek Yapma ve Tarifler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir yemek tarifini siralama kelimeleriyle adim adim anlatabilir.",
    },
    {
        "week": 19,
        "theme": "Food & Health",
        "theme_tr": "Yiyecek ve Saglik",
        "vocab": ["balanced", "nutritious", "diet", "calorie", "protein", "vitamin", "mineral",
                  "organic", "processed", "allergy", "vegetarian", "vegan", "gluten-free", "intolerance", "label"],
        "structure": "You should eat a balanced diet. Too much sugar is unhealthy. How many calories does this have?",
        "skills": {
            "listening": "Saglikli beslenme tavsiyelerini dinler, onemli bilgileri not eder.",
            "speaking": "Saglikli beslenme konusunda tavsiye verir.",
            "reading": "Gida etiketi ve saglikli beslenme metnini okur.",
            "writing": "Saglikli beslenme onerileri iceren brosur yazar.",
        },
        "linked_content": {
            "categories": ["Yiyecek", "Saglik"],
            "songs": [],
            "games": ["Saglikli/Sagliksiz Sinifla", "Etiket Oku"],
            "dialogues": ["What Should I Eat?"],
            "readings": ["Reading Food Labels"],
            "writings": ["Healthy Eating Guide"],
            "grammar": ["should/shouldn't + too much/too many/enough"],
            "phonics": ["/f/ vs /v/ minimal pairs"],
            "listening": ["Saglikli Beslenme Tavsiyeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Yiyecek ve Saglik temel kelimelerini tanitim (balanced/nutritious/diet) + yapi sunumu: You should eat a balanced diet", "Beceri Lab: Dinleme — 'Yiyecek ve Saglik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — You should eat a balanced diet yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yiyecek ve Saglik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yiyecek ve Saglik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yiyecek ve Saglik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (calorie/protein/vitamin) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yiyecek ve Saglik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yiyecek ve Saglik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Saglikli beslenme tavsiyelerini should + miktar ifadeleriyle verebilir.",
    },
    {
        "week": 20,
        "theme": "Review & Food Project",
        "theme_tr": "Tekrar ve Yemek Projesi",
        "vocab": [],
        "structure": "Unite 3-5 genel tekrar: Ev, Deneyimler, Yemek konulari",
        "skills": {
            "listening": "Genel tekrar dinleme aktiviteleri.",
            "speaking": "Yemek kitabi projesi sunumu.",
            "reading": "Karisik metin okuma ve anlama.",
            "writing": "Sinif yemek kitabi projesi yazma.",
        },
        "linked_content": {
            "categories": ["Tekrar", "Proje"],
            "songs": [],
            "games": ["Buyuk Quiz", "Yemek Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Sinif Yemek Kitabi"],
            "grammar": ["Unite 3-5 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Karisik Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 3-5 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — karisik temali dinleme aktiviteleri"],
            "tue": ["Ana Ders: Gramer odak — Unite 3-5 gramer yapilari genel tekrar", "Beceri Lab: Konusma — sinif ici mini sunumlar"],
            "wed": ["Ana Ders: Okuma — karisik metin okuma ve anlama sorulari", "Beceri Lab: Yazma — sinif yemek kitabi projesi yazma"],
            "thu": ["Ana Ders: Proje hazirlama ve sunum provasi", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 3-5 genel degerlendirme + sinif yemek kitabi projesi.",
    },
    # ===== UNIT 6: Travel & Postcards (Weeks 21-24) =====
    {
        "week": 21,
        "theme": "Travel & Postcards",
        "theme_tr": "Seyahat ve Kartpostallar",
        "vocab": ["destination", "sightseeing", "souvenir", "postcard", "landmark", "tour", "guidebook",
                  "luggage", "passport", "boarding pass", "departure", "arrival", "terminal", "flight", "cruise"],
        "structure": "I'm going to visit Paris next summer. We will see the Eiffel Tower. I'll send you a postcard!",
        "skills": {
            "listening": "Seyahat planlarini dinler, destinasyonlari ve aktiviteleri saptar.",
            "speaking": "Seyahat planlarini going to/will ile anlatir.",
            "reading": "Seyahat brosurunu/kartpostalini okur, bilgileri cikarir.",
            "writing": "Bir seyahatten kartpostal yazar (adres + mesaj).",
        },
        "linked_content": {
            "categories": ["Seyahat"],
            "songs": ["Travel Song"],
            "games": ["Destinasyon Eslestir", "Kartpostal Yaz"],
            "dialogues": ["Where Are You Going?"],
            "readings": ["Postcards from Around the World"],
            "writings": ["A Postcard from My Trip"],
            "grammar": ["going to vs will for future"],
            "phonics": ["/əʊ/ sound practice"],
            "listening": ["Seyahat Planlari"],
        },
        "days": {
            "mon": ["Ana Ders: Seyahat ve Kartpostallar temel kelimelerini tanitim (destination/sightseeing/souvenir) + yapi sunumu: I'm going to visit Paris next summer", "Beceri Lab: Dinleme — 'Seyahat ve Kartpostallar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — going to vs will for future yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Seyahat ve Kartpostallar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Seyahat ve Kartpostallar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Seyahat ve Kartpostallar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (postcard/landmark/tour) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Seyahat ve Kartpostallar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Seyahat ve Kartpostallar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Seyahat planlarini going to/will ile anlatabilir, kartpostal yazabilir.",
    },
    {
        "week": 22,
        "theme": "Holiday Experiences",
        "theme_tr": "Tatil Deneyimleri",
        "vocab": ["abroad", "resort", "campsite", "excursion", "adventure", "relaxing", "tiring",
                  "memorable", "explore", "discover", "scenery", "culture", "local", "cuisine", "accommodation"],
        "structure": "Last year, we went to Greece. We stayed at a resort. The scenery was breathtaking.",
        "skills": {
            "listening": "Tatil deneyimi anlatimini dinler, yerleri ve izlenimleri saptar.",
            "speaking": "Gecmis tatil deneyimini detayli anlatir.",
            "reading": "Tatil blogunu okur, izlenimleri ve onerileri cikarir.",
            "writing": "Gecmis tatil deneyimini anlatan blog yazisi yazar.",
        },
        "linked_content": {
            "categories": ["Seyahat", "Tatil"],
            "songs": [],
            "games": ["Tatil Hikayesi", "Izlenim Eslestir"],
            "dialogues": ["How Was Your Holiday?"],
            "readings": ["A Holiday Blog"],
            "writings": ["My Holiday Blog"],
            "grammar": ["Past Simple for experiences + adjectives for opinion"],
            "phonics": ["/ɑː/ vs /æ/ sounds"],
            "listening": ["Tatil Deneyimi"],
        },
        "days": {
            "mon": ["Ana Ders: Tatil Deneyimleri temel kelimelerini tanitim (abroad/resort/campsite) + yapi sunumu: Last year, we went to Greece", "Beceri Lab: Dinleme — 'Tatil Deneyimleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Last year, we went to Greece yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Tatil Deneyimleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Tatil Deneyimleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Tatil Deneyimleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (excursion/adventure/relaxing) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Tatil Deneyimleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Tatil Deneyimleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Gecmis tatil deneyimini Past Simple ile detayli anlatabilir.",
    },
    {
        "week": 23,
        "theme": "Future Plans",
        "theme_tr": "Gelecek Planlari",
        "vocab": ["plan", "predict", "expect", "hope", "promise", "decision", "arrangement", "schedule",
                  "calendar", "appointment", "definitely", "probably", "perhaps", "maybe", "certainly"],
        "structure": "I'm going to study medicine. I think it will rain tomorrow. I'll probably visit my cousin.",
        "skills": {
            "listening": "Gelecek planlari hakkinda diyalogu dinler, planlari ve tahminleri ayirir.",
            "speaking": "Gelecek planlarini ve tahminlerini going to/will ile ifade eder.",
            "reading": "Gelecek planlari/hedefleri hakkinda metin okur.",
            "writing": "Gelecek planlarini ve hayallerini anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Planlama", "Gelecek"],
            "songs": [],
            "games": ["Gelecek Tahmini", "Plan Yap"],
            "dialogues": ["What Are Your Plans?"],
            "readings": ["My Plans for the Future"],
            "writings": ["My Future Plans"],
            "grammar": ["going to (plans) vs will (predictions/spontaneous)"],
            "phonics": ["Weak forms: gonna, will/won't"],
            "listening": ["Gelecek Planlari Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Gelecek Planlari temel kelimelerini tanitim (plan/predict/expect) + yapi sunumu: I'm going to study medicine. I think it will rain", "Beceri Lab: Dinleme — 'Gelecek Planlari' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — going to (plans) vs will (predictions) yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Gelecek Planlari konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Gelecek Planlari' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Gelecek Planlari konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (hope/promise/decision) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Gelecek Planlari temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Gelecek Planlari konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Gelecek planlarini ve tahminlerini going to/will ile ifade edebilir.",
    },
    {
        "week": 24,
        "theme": "Review & Travel Project",
        "theme_tr": "Tekrar ve Seyahat Projesi",
        "vocab": [],
        "structure": "Unite 5-6 genel tekrar: Yemek ve Seyahat konulari",
        "skills": {
            "listening": "Genel tekrar dinleme aktiviteleri.",
            "speaking": "Seyahat rehberi projesi sunumu.",
            "reading": "Karisik metin okuma ve anlama.",
            "writing": "Seyahat rehberi projesi yazma.",
        },
        "linked_content": {
            "categories": ["Tekrar", "Proje"],
            "songs": [],
            "games": ["Buyuk Quiz", "Seyahat Jeopardy"],
            "dialogues": [],
            "readings": [],
            "writings": ["Seyahat Rehberi Projesi"],
            "grammar": ["Unite 5-6 tekrar"],
            "phonics": ["Genel tekrar"],
            "listening": ["Karisik Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Unite 5-6 genel tekrar — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — karisik temali dinleme aktiviteleri"],
            "tue": ["Ana Ders: Gramer odak — Unite 5-6 gramer yapilari genel tekrar", "Beceri Lab: Konusma — seyahat rehberi sunumu provasi"],
            "wed": ["Ana Ders: Okuma — karisik metin okuma ve anlama sorulari", "Beceri Lab: Yazma — seyahat rehberi projesi yazma"],
            "thu": ["Ana Ders: Proje hazirlama ve sunum provasi", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unite 5-6 genel degerlendirme + seyahat rehberi projesi.",
    },
    # ===== UNIT 7: Talents & Abilities (Weeks 25-27) =====
    {
        "week": 25,
        "theme": "Talents & Abilities",
        "theme_tr": "Yetenekler ve Beceriler",
        "vocab": ["talent", "ability", "skill", "gifted", "creative", "artistic", "musical", "athletic",
                  "brilliant", "capable", "perform", "master", "instrument", "stage", "audience"],
        "structure": "She can play the piano very well. He could swim when he was 5. You should practise every day.",
        "skills": {
            "listening": "Yetenek tanitimlarini dinler, kisileri ve yeteneklerini eslestirir.",
            "speaking": "Kendi yeteneklerini ve baskalarin yeteneklerini anlatir.",
            "reading": "Yetenekli ogrenci hakkinda metin okur.",
            "writing": "Kendi yeteneklerini ve gelistirmek istedigi becerileri yazar.",
        },
        "linked_content": {
            "categories": ["Yetenekler", "Hobiler"],
            "songs": ["Talent Show Song"],
            "games": ["Yetenek Tahmin", "Ne Yapabilir?"],
            "dialogues": ["What Can You Do?"],
            "readings": ["Young Talents"],
            "writings": ["My Talents and Skills"],
            "grammar": ["can/could/should for ability and advice"],
            "phonics": ["/k/ vs /g/ sounds"],
            "listening": ["Yetenek Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Yetenekler ve Beceriler temel kelimelerini tanitim (talent/ability/skill) + yapi sunumu: She can play the piano very well", "Beceri Lab: Dinleme — 'Yetenekler ve Beceriler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — can/could/should yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yetenekler ve Beceriler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yetenekler ve Beceriler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yetenekler ve Beceriler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (gifted/creative/artistic) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yetenekler ve Beceriler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yetenekler ve Beceriler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yeteneklerini can/could/should ile anlatabilir.",
    },
    {
        "week": 26,
        "theme": "Talent Show",
        "theme_tr": "Yetenek Gosterisi",
        "vocab": ["performance", "rehearsal", "backstage", "costume", "microphone", "spotlight",
                  "applause", "judge", "contestant", "vote", "winner", "runner-up", "feedback", "confidence", "stage fright"],
        "structure": "She performed a dance. The judges gave her 9 points. He could sing beautifully.",
        "skills": {
            "listening": "Yetenek gosterisi anlatimini dinler, performanslari degerlendirir.",
            "speaking": "Bir performansi degerlendirip yorum yapar.",
            "reading": "Yetenek gosterisi haberini okur, sonuclari cikarir.",
            "writing": "Bir yetenek gosterisi etkinligini anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Yetenekler", "Eglence"],
            "songs": [],
            "games": ["Mini Yetenek Gosterisi", "Juri Puanlama"],
            "dialogues": ["What Did You Think of the Show?"],
            "readings": ["School Talent Show"],
            "writings": ["The Best Performance"],
            "grammar": ["Past Simple for events + could for past ability"],
            "phonics": ["/ʃ/ vs /s/ sounds"],
            "listening": ["Yetenek Gosterisi Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Yetenek Gosterisi temel kelimelerini tanitim (performance/rehearsal/backstage) + yapi sunumu: She performed a dance. The judges gave her 9 points", "Beceri Lab: Dinleme — 'Yetenek Gosterisi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — She performed a dance. The judges gave her 9 points yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yetenek Gosterisi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yetenek Gosterisi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yetenek Gosterisi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (costume/microphone/spotlight) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yetenek Gosterisi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yetenek Gosterisi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir yetenek gosterisi etkinligini anlatip degerlendirme yapabilir.",
    },
    {
        "week": 27,
        "theme": "Learning New Skills",
        "theme_tr": "Yeni Beceriler Ogrenmek",
        "vocab": ["learn", "practise", "improve", "beginner", "intermediate", "advanced", "course",
                  "lesson", "tutor", "online", "tutorial", "patience", "progress", "mistake", "feedback"],
        "structure": "I'm learning to play the guitar. You should practise regularly. I could play better if I practised more.",
        "skills": {
            "listening": "Beceri ogrenme deneyimlerini dinler, tavsiyeleri saptar.",
            "speaking": "Ogrenmek istedigi becerileri ve planlarini anlatir.",
            "reading": "Beceri ogrenme rehberini okur.",
            "writing": "Yeni bir beceri ogrenme planini yazar.",
        },
        "linked_content": {
            "categories": ["Yetenekler", "Egitim"],
            "songs": [],
            "games": ["Beceri Planlama", "Hedef Belirleme"],
            "dialogues": ["How Are You Learning?"],
            "readings": ["Tips for Learning New Skills"],
            "writings": ["My Learning Plan"],
            "grammar": ["should + learning to + if clause (simple)"],
            "phonics": ["/n/ vs /ŋ/ sounds"],
            "listening": ["Beceri Ogrenme Deneyimleri"],
        },
        "days": {
            "mon": ["Ana Ders: Yeni Beceriler Ogrenmek temel kelimelerini tanitim (learn/practise/improve) + yapi sunumu: I'm learning to play the guitar", "Beceri Lab: Dinleme — 'Yeni Beceriler Ogrenmek' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I'm learning to play the guitar yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yeni Beceriler Ogrenmek konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yeni Beceriler Ogrenmek' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yeni Beceriler Ogrenmek konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (beginner/intermediate/advanced) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yeni Beceriler Ogrenmek temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yeni Beceriler Ogrenmek konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yeni beceri ogrenme planini should ve learning to ile anlatabilir.",
    },
    # ===== UNIT 8: Amazing Places (Weeks 28-30) =====
    {
        "week": 28,
        "theme": "Amazing Places",
        "theme_tr": "Sira Disi Yerler",
        "vocab": ["amazing", "breathtaking", "spectacular", "unique", "ancient", "mysterious", "natural",
                  "wonder", "cave", "waterfall", "cliff", "volcano", "canyon", "glacier", "coral reef"],
        "structure": "There is a spectacular waterfall in this region. The cave is 500 metres deep. It's one of the most amazing places in the world.",
        "skills": {
            "listening": "Sira disi yer tanitimini dinler, ozellikleri ve konumlari saptar.",
            "speaking": "Sira disi bir yeri detayli tanitir ve tanimlar.",
            "reading": "Doga harikaları hakkinda metin okur (150 kelime).",
            "writing": "Sira disi bir yeri tanitan detayli yazi yazar (12 cumle).",
        },
        "linked_content": {
            "categories": ["Doga", "Seyahat"],
            "songs": ["Amazing World Song"],
            "games": ["Yer Tahmin", "Doga Harikasi Eslestir"],
            "dialogues": ["Have You Heard of This Place?"],
            "readings": ["Natural Wonders of the World"],
            "writings": ["An Amazing Place I Want to Visit"],
            "grammar": ["There is/are + superlatives + descriptive adjectives"],
            "phonics": ["/eɪ/ sound practice"],
            "listening": ["Doga Harikasi Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Sira Disi Yerler temel kelimelerini tanitim (amazing/breathtaking/spectacular) + yapi sunumu: There is a spectacular waterfall in this region", "Beceri Lab: Dinleme — 'Sira Disi Yerler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — There is a spectacular waterfall in this region yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Sira Disi Yerler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Sira Disi Yerler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Sira Disi Yerler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (unique/ancient/mysterious) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Sira Disi Yerler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Sira Disi Yerler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sira disi bir yeri there is/are ve superlatives ile tanitabilir.",
    },
    {
        "week": 29,
        "theme": "Famous Landmarks",
        "theme_tr": "Unlu Yapilar",
        "vocab": ["landmark", "monument", "tower", "bridge", "cathedral", "mosque", "temple",
                  "statue", "pyramid", "palace", "heritage", "architect", "design", "construction", "restore"],
        "structure": "The Pyramids were built thousands of years ago. Hagia Sophia is one of the most famous landmarks.",
        "skills": {
            "listening": "Unlu yapi tanitimini dinler, tarihce ve ozellikleri not eder.",
            "speaking": "Unlu bir yapiyi tarihce ve ozellikleriyle tanitir.",
            "reading": "Unlu yapi hakkinda metin okur, bilgileri cikarir.",
            "writing": "Unlu bir yapiyi tanitan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Tarih", "Seyahat"],
            "songs": [],
            "games": ["Yapi Eslestir", "Nerede Bu?"],
            "dialogues": ["Tell Me About This Landmark"],
            "readings": ["Famous Landmarks of Turkey"],
            "writings": ["A Landmark I'd Like to Visit"],
            "grammar": ["was/were built + passive voice basics"],
            "phonics": ["/ɔː/ sound practice"],
            "listening": ["Unlu Yapi Tanitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Unlu Yapilar temel kelimelerini tanitim (landmark/monument/tower) + yapi sunumu: The Pyramids were built thousands of years ago", "Beceri Lab: Dinleme — 'Unlu Yapilar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — The Pyramids were built thousands of years ago yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Unlu Yapilar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Unlu Yapilar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Unlu Yapilar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (bridge/cathedral/mosque) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Unlu Yapilar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Unlu Yapilar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Unlu bir yapiyi tarihce ve ozellikleriyle tanitabilir.",
    },
    {
        "week": 30,
        "theme": "Eco-Tourism",
        "theme_tr": "Eko-Turizm",
        "vocab": ["eco-tourism", "sustainable", "responsible", "conservation", "wildlife", "habitat",
                  "endangered", "protect", "preserve", "national park", "safari", "hiking", "camping", "carbon footprint", "green travel"],
        "structure": "We should protect natural habitats. Eco-tourism helps local communities. Don't leave rubbish in nature.",
        "skills": {
            "listening": "Eko-turizm sunumunu dinler, prensipleri ve uygulamalari saptar.",
            "speaking": "Eko-turizm hakkinda goruslerini paylasir.",
            "reading": "Eko-turizm rehberini okur, onerileri listeler.",
            "writing": "Sorumlu turist olmak icin oneriler iceren brosur yazar.",
        },
        "linked_content": {
            "categories": ["Doga", "Seyahat", "Cevre"],
            "songs": [],
            "games": ["Eko-Turizm Quiz", "Sorumlu Turist"],
            "dialogues": ["What Is Eco-Tourism?"],
            "readings": ["Responsible Travel Guide"],
            "writings": ["Be a Responsible Tourist"],
            "grammar": ["should/must + imperatives + linking words"],
            "phonics": ["/iː/ vs /ɪ/ review"],
            "listening": ["Eko-Turizm Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Eko-Turizm temel kelimelerini tanitim (eco-tourism/sustainable/responsible) + yapi sunumu: We should protect natural habitats", "Beceri Lab: Dinleme — 'Eko-Turizm' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — We should protect natural habitats yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Eko-Turizm konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Eko-Turizm' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Eko-Turizm konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (conservation/wildlife/habitat) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Eko-Turizm temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Eko-Turizm konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Eko-turizm prensiplerini should/must ile anlatabilir.",
    },
    # ===== UNIT 9: Friendship (Weeks 31-33) =====
    {
        "week": 31,
        "theme": "Friendship",
        "theme_tr": "Arkadaslik",
        "vocab": ["friendship", "trust", "loyal", "honest", "reliable", "supportive", "caring",
                  "generous", "forgiving", "patient", "conflict", "argue", "apologise", "forgive", "respect"],
        "structure": "A good friend is someone who listens to you. She is the friend that I trust the most. Friends who support each other are happy.",
        "skills": {
            "listening": "Arkadaslik hakkinda diyalogu dinler, ozellikleri ve durumlari saptar.",
            "speaking": "Iyi bir arkadas ozelliklerini anlatir, arkadaslik deneyimlerini paylasir.",
            "reading": "Arkadaslik hakkinda metin okur (150 kelime), ana fikri cikarir.",
            "writing": "En iyi arkadasini ve arkadasliklarini anlatan yazi yazar (12 cumle).",
        },
        "linked_content": {
            "categories": ["Iliskiler", "Duygular"],
            "songs": ["Friendship Song"],
            "games": ["Arkadaslik Ozellikleri Eslestir", "Senaryo Cozme"],
            "dialogues": ["What Makes a Good Friend?"],
            "readings": ["The Meaning of Friendship"],
            "writings": ["My Best Friend"],
            "grammar": ["Relative clauses (who/which/that)"],
            "phonics": ["/r/ vs /w/ sounds"],
            "listening": ["Arkadaslik Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Arkadaslik temel kelimelerini tanitim (friendship/trust/loyal) + yapi sunumu: A good friend is someone who listens to you", "Beceri Lab: Dinleme — 'Arkadaslik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — relative clauses (who/which/that) yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Arkadaslik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Arkadaslik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Arkadaslik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (honest/reliable/supportive) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Arkadaslik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Arkadaslik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Arkadaslik ozelliklerini relative clauses ile tanimlayabilir.",
    },
    {
        "week": 32,
        "theme": "Solving Problems",
        "theme_tr": "Sorun Cozme",
        "vocab": ["problem", "solution", "advice", "suggest", "recommend", "discuss", "compromise",
                  "misunderstanding", "communicate", "empathy", "perspective", "opinion", "agree", "disagree", "resolve"],
        "structure": "You should talk to her. I suggest that you apologise. If you listen, you can understand each other.",
        "skills": {
            "listening": "Sorun cozme diyaloglarini dinler, onerileri saptar.",
            "speaking": "Bir soruna cozum onerir, farkli bakis acilarini degerlendirip tavsiye verir.",
            "reading": "Sorun cozme senaryolarini okur, en iyi cozumu secer.",
            "writing": "Bir sorunu ve cozumunu anlatan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Iliskiler", "Iletisim"],
            "songs": [],
            "games": ["Sorun-Cozum Eslestir", "Senaryo Tartisma"],
            "dialogues": ["What Should I Do?"],
            "readings": ["Solving Friendship Problems"],
            "writings": ["A Problem and Its Solution"],
            "grammar": ["should/suggest/recommend + if clause (zero/first conditional)"],
            "phonics": ["/s/ vs /z/ sounds"],
            "listening": ["Sorun Cozme Diyalogu"],
        },
        "days": {
            "mon": ["Ana Ders: Sorun Cozme temel kelimelerini tanitim (problem/solution/advice) + yapi sunumu: You should talk to her. I suggest that you apologise", "Beceri Lab: Dinleme — 'Sorun Cozme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — should/suggest/recommend yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Sorun Cozme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Sorun Cozme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Sorun Cozme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (suggest/recommend/discuss) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Sorun Cozme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Sorun Cozme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir soruna cozum onerebilir, tavsiye verebilir.",
    },
    {
        "week": 33,
        "theme": "Online Friendship",
        "theme_tr": "Cevrimici Arkadaslik",
        "vocab": ["online", "social media", "chat", "message", "follower", "profile", "privacy",
                  "cyberbullying", "block", "report", "safe", "stranger", "identity", "password", "digital footprint"],
        "structure": "You should never share your password. People who cyberbully others are wrong. Be careful with strangers online.",
        "skills": {
            "listening": "Internet guvenligi tavsiyelerini dinler, kurallari listeler.",
            "speaking": "Cevrimici guvenlik kurallari hakkinda konusur.",
            "reading": "Internet guvenligi metnini okur, kurallari siralar.",
            "writing": "Cevrimici guvenlik posteri/brosuru yazar.",
        },
        "linked_content": {
            "categories": ["Teknoloji", "Guvenlik"],
            "songs": [],
            "games": ["Guvenlik Quiz", "Dogru/Yanlis"],
            "dialogues": ["Is It Safe Online?"],
            "readings": ["Staying Safe Online"],
            "writings": ["Online Safety Rules"],
            "grammar": ["should/must/mustn't + relative clauses review"],
            "phonics": ["/tʃ/ vs /dʒ/ sounds"],
            "listening": ["Internet Guvenligi Tavsiyeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Cevrimici Arkadaslik temel kelimelerini tanitim (online/social media/chat) + yapi sunumu: You should never share your password", "Beceri Lab: Dinleme — 'Cevrimici Arkadaslik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — should/must/mustn't yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Cevrimici Arkadaslik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Cevrimici Arkadaslik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Cevrimici Arkadaslik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (cyberbullying/block/report) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Cevrimici Arkadaslik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Cevrimici Arkadaslik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Cevrimici guvenlik kurallarini should/must ile ifade edebilir.",
    },
    # ===== UNIT 10: Health & Wellness (Weeks 34-36) =====
    {
        "week": 34,
        "theme": "Health & Wellness",
        "theme_tr": "Saglik ve Yasam Kalitesi",
        "vocab": ["wellness", "mental health", "physical health", "exercise", "meditation", "stress",
                  "sleep", "hygiene", "balanced", "routine", "screen time", "fresh air", "habit", "lifestyle", "wellbeing"],
        "structure": "You should exercise regularly. Too much screen time is bad for your eyes. However, walking in nature can reduce stress. Also, sleeping 8 hours is important.",
        "skills": {
            "listening": "Saglikli yasam tavsiyeleri dinler, onemli bilgileri saptar.",
            "speaking": "Saglikli yasam aliskanliklarini ve onerilerini anlatir.",
            "reading": "Saglik ve yasam kalitesi hakkinda metin okur, onerileri cikarir.",
            "writing": "Saglikli yasam rehberi yazar, linking words kullanir (12+ cumle).",
        },
        "linked_content": {
            "categories": ["Saglik", "Gunluk Yasam"],
            "songs": ["Healthy Life Song"],
            "games": ["Saglikli Aliskanlik Quiz", "Dogru/Yanlis"],
            "dialogues": ["How Can I Be Healthier?"],
            "readings": ["A Guide to Healthy Living"],
            "writings": ["My Healthy Living Guide"],
            "grammar": ["Linking words (however, also, because, so, although, in addition)"],
            "phonics": ["/θ/ vs /ð/ review"],
            "listening": ["Saglikli Yasam Tavsiyeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Saglik ve Yasam Kalitesi temel kelimelerini tanitim (wellness/mental health/physical health) + yapi sunumu: You should exercise regularly", "Beceri Lab: Dinleme — 'Saglik ve Yasam Kalitesi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Linking words (however/also/because/so) yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Saglik ve Yasam Kalitesi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Saglik ve Yasam Kalitesi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Saglik ve Yasam Kalitesi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (exercise/meditation/stress) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Saglik ve Yasam Kalitesi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Saglik ve Yasam Kalitesi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Saglikli yasam onerilerini linking words ile baglantili sekilde anlatabilir.",
    },
    {
        "week": 35,
        "theme": "End of Year Project",
        "theme_tr": "Yil Sonu Projesi",
        "vocab": [],
        "structure": "Yil boyunca ogrenilenler uzerine proje",
        "skills": {
            "listening": "Sinif arkadaslarinin projelerini dinler, geri bildirim verir.",
            "speaking": "Projesini 3-5 dakikalik sunumla sinifa anlatir.",
            "reading": "Proje icin arastirma yapar, kaynak okur.",
            "writing": "Proje raporunu yazar (giris, gelisme, sonuc).",
        },
        "linked_content": {
            "categories": ["Proje"],
            "songs": [],
            "games": [],
            "dialogues": [],
            "readings": [],
            "writings": ["Proje Raporu"],
            "grammar": ["Yil genel tekrar"],
            "phonics": ["Yil genel tekrar"],
            "listening": ["Sunum Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Yil Sonu Projesi — proje konusu secimi ve planlama", "Beceri Lab: Dinleme — ornek proje sunumlarini dinle, not al"],
            "tue": ["Ana Ders: Proje arastirma ve icerik hazirlama", "Beceri Lab: Konusma — proje sunumu provasi"],
            "wed": ["Ana Ders: Proje raporu yazma (giris, gelisme, sonuc)", "Beceri Lab: Yazma — proje raporunu duzenle ve tamamla"],
            "thu": ["Ana Ders: Proje sunumu provasi ve geri bildirim", "Beceri Lab: Proje/Sunum — poster/sunum hazirlama"],
            "fri": ["Native Speaker: Proje sunumlari + geri bildirim + yil sonu degerlendirmesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yil sonu projesi: sunum + rapor degerlendirmesi.",
    },
    {
        "week": 36,
        "theme": "Final Review & Assessment",
        "theme_tr": "Yil Sonu Genel Degerlendirme",
        "vocab": [],
        "structure": "Tum yil konulari genel tekrar ve degerlendirme",
        "skills": {
            "listening": "Yil sonu genel dinleme degerlendirmesi.",
            "speaking": "Yil sonu sozlu sinav: secilen konuda 3-5 dakika sunum.",
            "reading": "Yil sonu genel okuma degerlendirmesi.",
            "writing": "Yil sonu genel yazma degerlendirmesi.",
        },
        "linked_content": {
            "categories": ["Degerlendirme"],
            "songs": [],
            "games": ["Final Jeopardy", "Buyuk Quiz"],
            "dialogues": [],
            "readings": [],
            "writings": ["Yil Sonu Yazma"],
            "grammar": ["Yil genel tekrar"],
            "phonics": ["Yil genel tekrar"],
            "listening": ["Yil Sonu Degerlendirme"],
        },
        "days": {
            "mon": ["Ana Ders: Yil Sonu Genel Degerlendirme — anahtar kelime ve yapi tekrari + quiz", "Beceri Lab: Dinleme — yil sonu dinleme degerlendirmesi"],
            "tue": ["Ana Ders: Gramer odak — tum yil gramer yapilari genel tekrar", "Beceri Lab: Konusma — yil sonu sozlu sinav"],
            "wed": ["Ana Ders: Okuma — yil sonu genel okuma degerlendirmesi", "Beceri Lab: Yazma — yil sonu genel yazma degerlendirmesi"],
            "thu": ["Ana Ders: Eksik konularin tekrari ve pekistirme", "Beceri Lab: Proje/Sunum — proje sunumlari"],
            "fri": ["Native Speaker: Yil sonu serbest konusma + kulturel karsilastirma + oyun", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yil sonu genel degerlendirmesi: 4 beceri + proje notu.",
    },
]


# =============================================================================
# 7. SINIF - CEFR A2.3 (Orta-alt Iletisim)
# =============================================================================

CURRICULUM_GRADE7 = [
  {
    "week": 1,
    "theme": "Personal Identity",
    "theme_tr": "Kisisel Kimlik",
    "vocab": [
      "identity",
      "personality",
      "values",
      "beliefs",
      "self-awareness",
      "character",
      "role model",
      "unique",
      "diverse",
      "individual"
    ],
    "structure": "I consider myself a creative person. What kind of person are you?",
    "skills": {
      "listening": "Kimlik ve kisilik hakkinda diyalog dinler.",
      "speaking": "Kendi kisiligini ve degerlerini anlatir.",
      "reading": "Kisisel kimlik uzerine metin okur.",
      "writing": "Kendini tanimlayan paragraf yazar."
    },
    "linked_content": {
      "categories": [
        "Kimlik"
      ],
      "songs": [
        "Personal Identity Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Personal Identity Dialogue"
      ],
      "readings": [
        "Personal Identity Reading"
      ],
      "writings": [
        "Personal Identity Writing"
      ],
      "grammar": [
        "I consider myself a creative person"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Personal Identity Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Personal Identity temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Personal Identity temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - I consider myself a creative person. What kind of ",
        "Beceri Lab: Konusma - esli calisma, Personal Identity konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Personal Identity temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Personal Identity konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Personal Identity temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Personal Identity konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Personal Identity konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 2,
    "theme": "Who Am I?",
    "theme_tr": "Ben Kimim?",
    "vocab": [
      "trait",
      "strength",
      "weakness",
      "goal",
      "dream",
      "ambition",
      "confident",
      "shy",
      "outgoing",
      "introvert"
    ],
    "structure": "My biggest strength is empathy. I dream of becoming a scientist.",
    "skills": {
      "listening": "Genclik hikayeleri dinler.",
      "speaking": "Guclui ve zayif yonlerini tartisir.",
      "reading": "Genc biyografileri okur.",
      "writing": "Kisisel profil yazar."
    },
    "linked_content": {
      "categories": [
        "Kimlik"
      ],
      "songs": [
        "Who Am I? Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Who Am I? Dialogue"
      ],
      "readings": [
        "Who Am I? Reading"
      ],
      "writings": [
        "Who Am I? Writing"
      ],
      "grammar": [
        "My biggest strength is empathy"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Who Am I? Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Who Am I? temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Who Am I? temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - My biggest strength is empathy. I dream of becomin",
        "Beceri Lab: Konusma - esli calisma, Who Am I? konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Who Am I? temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Who Am I? konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Who Am I? temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Who Am I? konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Who Am I? konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 3,
    "theme": "Values & Beliefs",
    "theme_tr": "Degerler ve Inanclar",
    "vocab": [
      "respect",
      "honesty",
      "fairness",
      "responsibility",
      "compassion",
      "integrity",
      "tolerance",
      "equality",
      "justice",
      "freedom"
    ],
    "structure": "I believe that honesty is the most important value.",
    "skills": {
      "listening": "Deger tartismalarini dinler.",
      "speaking": "Degerlerini aciklar.",
      "reading": "Degerler uzerine makale okur.",
      "writing": "Deger kompozisyonu yazar."
    },
    "linked_content": {
      "categories": [
        "Degerler"
      ],
      "songs": [
        "Values & Beliefs Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Values & Beliefs Dialogue"
      ],
      "readings": [
        "Values & Beliefs Reading"
      ],
      "writings": [
        "Values & Beliefs Writing"
      ],
      "grammar": [
        "I believe that honesty is the most important value"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Values & Beliefs Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Values & Beliefs temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Values & Beliefs temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - I believe that honesty is the most important value",
        "Beceri Lab: Konusma - esli calisma, Values & Beliefs konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Values & Beliefs temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Values & Beliefs konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Values & Beliefs temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Values & Beliefs konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Values & Beliefs konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 4,
    "theme": "Review: My Identity",
    "theme_tr": "Tekrar: Kimligim",
    "vocab": [
      "identity",
      "personality",
      "values",
      "strength",
      "weakness",
      "unique",
      "character",
      "dream",
      "goal",
      "confident"
    ],
    "structure": "Let me tell you about myself. I am unique because...",
    "skills": {
      "listening": "Sinif arkadaslarinin sunumlarini dinler.",
      "speaking": "Kimlik sunumu yapar.",
      "reading": "Sinif arkadaslarinin profillerini okur.",
      "writing": "Kimlik portfolyosu tamamlar."
    },
    "linked_content": {
      "categories": [
        "Tekrar"
      ],
      "songs": [
        "Review: My Identity Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Review: My Identity Dialogue"
      ],
      "readings": [
        "Review: My Identity Reading"
      ],
      "writings": [
        "Review: My Identity Writing"
      ],
      "grammar": [
        "Let me tell you about myself"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Review: My Identity Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Review: My Identity temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Review: My Identity temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Let me tell you about myself. I am unique because.",
        "Beceri Lab: Konusma - esli calisma, Review: My Identity konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Review: My Identity temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Review: My Identity konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Review: My Identity temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Review: My Identity konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Review: My Identity konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 5,
    "theme": "Cultural Traditions",
    "theme_tr": "Kulturel Gelenekler",
    "vocab": [
      "tradition",
      "ceremony",
      "custom",
      "ritual",
      "celebration",
      "heritage",
      "ancestor",
      "generation",
      "preserve",
      "cultural"
    ],
    "structure": "In my culture, we celebrate Eid with family gatherings.",
    "skills": {
      "listening": "Kulturel gelenek anlatimlarini dinler.",
      "speaking": "Kendi kulturel geleneklerini anlatir.",
      "reading": "Dunya gelenekleri hakkinda metin okur.",
      "writing": "Gelenek tanimlayan paragraf yazar."
    },
    "linked_content": {
      "categories": [
        "Kultur"
      ],
      "songs": [
        "Cultural Traditions Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Cultural Traditions Dialogue"
      ],
      "readings": [
        "Cultural Traditions Reading"
      ],
      "writings": [
        "Cultural Traditions Writing"
      ],
      "grammar": [
        "In my culture, we celebrate Eid with family gatherings"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Cultural Traditions Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Cultural Traditions temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Cultural Traditions temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - In my culture, we celebrate Eid with family gather",
        "Beceri Lab: Konusma - esli calisma, Cultural Traditions konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Cultural Traditions temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Cultural Traditions konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Cultural Traditions temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Cultural Traditions konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Cultural Traditions konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 6,
    "theme": "Festivals Around the World",
    "theme_tr": "Dunya Festivalleri",
    "vocab": [
      "festival",
      "carnival",
      "parade",
      "costume",
      "fireworks",
      "lantern",
      "harvest",
      "blessing",
      "feast",
      "decoration"
    ],
    "structure": "The Holi festival is celebrated by throwing coloured powder.",
    "skills": {
      "listening": "Festival tanitim videolari dinler.",
      "speaking": "Festivalleri karsilastirir.",
      "reading": "Festival rehberi okur.",
      "writing": "Festival tanitim yazisi yazar."
    },
    "linked_content": {
      "categories": [
        "Kultur"
      ],
      "songs": [
        "Festivals Around the World Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Festivals Around the World Dialogue"
      ],
      "readings": [
        "Festivals Around the World Reading"
      ],
      "writings": [
        "Festivals Around the World Writing"
      ],
      "grammar": [
        "The Holi festival is celebrated by throwing coloured powder"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Festivals Around the World Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Festivals Around the World temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Festivals Around the World temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - The Holi festival is celebrated by throwing colour",
        "Beceri Lab: Konusma - esli calisma, Festivals Around the World konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Festivals Around the World temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Festivals Around the World konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Festivals Around the World temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Festivals Around the World konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Festivals Around the World konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 7,
    "theme": "Wedding Customs",
    "theme_tr": "Dugun Gelenekleri",
    "vocab": [
      "wedding",
      "bride",
      "groom",
      "ceremony",
      "reception",
      "invitation",
      "guest",
      "bouquet",
      "vow",
      "ring"
    ],
    "structure": "In Turkish weddings, guests pin gold coins on the bride.",
    "skills": {
      "listening": "Dugun anlatimlarini dinler.",
      "speaking": "Dugun geleneklerini karsilastirir.",
      "reading": "Dugun gelenekleri makalesini okur.",
      "writing": "Dugun tanitimi yazar."
    },
    "linked_content": {
      "categories": [
        "Kultur"
      ],
      "songs": [
        "Wedding Customs Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Wedding Customs Dialogue"
      ],
      "readings": [
        "Wedding Customs Reading"
      ],
      "writings": [
        "Wedding Customs Writing"
      ],
      "grammar": [
        "In Turkish weddings, guests pin gold coins on the bride"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Wedding Customs Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Wedding Customs temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Wedding Customs temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - In Turkish weddings, guests pin gold coins on the ",
        "Beceri Lab: Konusma - esli calisma, Wedding Customs konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Wedding Customs temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Wedding Customs konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Wedding Customs temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Wedding Customs konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Wedding Customs konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 8,
    "theme": "Our Heritage",
    "theme_tr": "Mirasimiz",
    "vocab": [
      "heritage",
      "monument",
      "artifact",
      "museum",
      "historic",
      "ancient",
      "UNESCO",
      "landmark",
      "ruins",
      "excavation"
    ],
    "structure": "Gobekli Tepe is one of the oldest heritage sites in the world.",
    "skills": {
      "listening": "Miras koruma projelerini dinler.",
      "speaking": "Yerel mirasi tartisir.",
      "reading": "UNESCO listesi hakkinda okur.",
      "writing": "Miras koruma posteri yazar."
    },
    "linked_content": {
      "categories": [
        "Kultur"
      ],
      "songs": [
        "Our Heritage Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Our Heritage Dialogue"
      ],
      "readings": [
        "Our Heritage Reading"
      ],
      "writings": [
        "Our Heritage Writing"
      ],
      "grammar": [
        "Gobekli Tepe is one of the oldest heritage sites in the world"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Our Heritage Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Our Heritage temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Our Heritage temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Gobekli Tepe is one of the oldest heritage sites i",
        "Beceri Lab: Konusma - esli calisma, Our Heritage konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Our Heritage temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Our Heritage konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Our Heritage temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Our Heritage konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Our Heritage konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 9,
    "theme": "Jobs & Careers",
    "theme_tr": "Meslekler ve Kariyer",
    "vocab": [
      "career",
      "profession",
      "occupation",
      "salary",
      "qualification",
      "experience",
      "interview",
      "resume",
      "skill",
      "employer"
    ],
    "structure": "If I studied harder, I would become a doctor.",
    "skills": {
      "listening": "Kariyer tanitim konusmalarini dinler.",
      "speaking": "Kariyer hedeflerini tartisir.",
      "reading": "Gelecek meslekleri hakkinda okur.",
      "writing": "Kariyer plani yazar."
    },
    "linked_content": {
      "categories": [
        "Meslekler"
      ],
      "songs": [
        "Jobs & Careers Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Jobs & Careers Dialogue"
      ],
      "readings": [
        "Jobs & Careers Reading"
      ],
      "writings": [
        "Jobs & Careers Writing"
      ],
      "grammar": [
        "If I studied harder, I would become a doctor"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Jobs & Careers Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Jobs & Careers temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Jobs & Careers temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - If I studied harder, I would become a doctor.",
        "Beceri Lab: Konusma - esli calisma, Jobs & Careers konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Jobs & Careers temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Jobs & Careers konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Jobs & Careers temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Jobs & Careers konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Jobs & Careers konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 10,
    "theme": "New Jobs of the Future",
    "theme_tr": "Gelecegin Yeni Meslekleri",
    "vocab": [
      "app developer",
      "data analyst",
      "drone pilot",
      "social media manager",
      "AI trainer",
      "content creator",
      "sustainability consultant",
      "UX designer",
      "cybersecurity",
      "freelancer"
    ],
    "structure": "Ten years ago, being a YouTuber was not a real job.",
    "skills": {
      "listening": "Girisimci roportajlarini dinler.",
      "speaking": "Gelecek mesleklerini tahmin eder.",
      "reading": "Teknoloji meslekleri makalesini okur.",
      "writing": "Gelecek meslegi tanitimi yazar."
    },
    "linked_content": {
      "categories": [
        "Meslekler"
      ],
      "songs": [
        "New Jobs of the Future Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "New Jobs of the Future Dialogue"
      ],
      "readings": [
        "New Jobs of the Future Reading"
      ],
      "writings": [
        "New Jobs of the Future Writing"
      ],
      "grammar": [
        "Ten years ago, being a YouTuber was not a real job"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "New Jobs of the Future Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: New Jobs of the Future temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - New Jobs of the Future temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Ten years ago, being a YouTuber was not a real job",
        "Beceri Lab: Konusma - esli calisma, New Jobs of the Future konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - New Jobs of the Future temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - New Jobs of the Future konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - New Jobs of the Future temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: New Jobs of the Future konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "New Jobs of the Future konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 11,
    "theme": "Work Skills",
    "theme_tr": "Is Becerileri",
    "vocab": [
      "teamwork",
      "communication",
      "problem-solving",
      "creativity",
      "leadership",
      "time management",
      "adaptability",
      "critical thinking",
      "digital literacy",
      "collaboration"
    ],
    "structure": "Employers value teamwork and communication skills.",
    "skills": {
      "listening": "Is becerisi sunumlarini dinler.",
      "speaking": "En onemli becerileri tartisir.",
      "reading": "Beceri gelistirme rehberi okur.",
      "writing": "Beceri degerlendirmesi yazar."
    },
    "linked_content": {
      "categories": [
        "Beceriler"
      ],
      "songs": [
        "Work Skills Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Work Skills Dialogue"
      ],
      "readings": [
        "Work Skills Reading"
      ],
      "writings": [
        "Work Skills Writing"
      ],
      "grammar": [
        "Employers value teamwork and communication skills"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Work Skills Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Work Skills temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Work Skills temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Employers value teamwork and communication skills.",
        "Beceri Lab: Konusma - esli calisma, Work Skills konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Work Skills temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Work Skills konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Work Skills temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Work Skills konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Work Skills konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 12,
    "theme": "Career Day",
    "theme_tr": "Kariyer Gunu",
    "vocab": [
      "presentation",
      "volunteer",
      "internship",
      "mentor",
      "shadowing",
      "networking",
      "portfolio",
      "goal setting",
      "motivation",
      "opportunity"
    ],
    "structure": "During Career Day, I learned about different professions.",
    "skills": {
      "listening": "Kariyer gunu konusmalarini dinler.",
      "speaking": "Meslek sunumu yapar.",
      "reading": "Kariyer gunu raporu okur.",
      "writing": "Kariyer gunu yansimasi yazar."
    },
    "linked_content": {
      "categories": [
        "Meslekler"
      ],
      "songs": [
        "Career Day Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Career Day Dialogue"
      ],
      "readings": [
        "Career Day Reading"
      ],
      "writings": [
        "Career Day Writing"
      ],
      "grammar": [
        "During Career Day, I learned about different professions"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Career Day Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Career Day temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Career Day temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - During Career Day, I learned about different profe",
        "Beceri Lab: Konusma - esli calisma, Career Day konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Career Day temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Career Day konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Career Day temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Career Day konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Career Day konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 13,
    "theme": "Media Literacy",
    "theme_tr": "Medya Okuryazarligi",
    "vocab": [
      "media",
      "source",
      "reliable",
      "biased",
      "fact",
      "opinion",
      "headline",
      "journalist",
      "clickbait",
      "verify"
    ],
    "structure": "This news article was written by a reliable journalist.",
    "skills": {
      "listening": "Haber analizi dinler.",
      "speaking": "Haberlerin guvenilirligini tartisir.",
      "reading": "Medya okuryazarligi rehberi okur.",
      "writing": "Haber analizi yazar."
    },
    "linked_content": {
      "categories": [
        "Medya"
      ],
      "songs": [
        "Media Literacy Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Media Literacy Dialogue"
      ],
      "readings": [
        "Media Literacy Reading"
      ],
      "writings": [
        "Media Literacy Writing"
      ],
      "grammar": [
        "This news article was written by a reliable journalist"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Media Literacy Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Media Literacy temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Media Literacy temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - This news article was written by a reliable journa",
        "Beceri Lab: Konusma - esli calisma, Media Literacy konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Media Literacy temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Media Literacy konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Media Literacy temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Media Literacy konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Media Literacy konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 14,
    "theme": "Fake News",
    "theme_tr": "Sahte Haberler",
    "vocab": [
      "misinformation",
      "propaganda",
      "fact-check",
      "evidence",
      "claim",
      "hoax",
      "viral",
      "misleading",
      "credible",
      "investigate"
    ],
    "structure": "Can you spot fake news? Always check the source!",
    "skills": {
      "listening": "Sahte haber orneklerini dinler.",
      "speaking": "Sahte haberleri tespit eder.",
      "reading": "Gercek/sahte haber karsilastirmasi okur.",
      "writing": "Sahte haber raporu yazar."
    },
    "linked_content": {
      "categories": [
        "Medya"
      ],
      "songs": [
        "Fake News Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Fake News Dialogue"
      ],
      "readings": [
        "Fake News Reading"
      ],
      "writings": [
        "Fake News Writing"
      ],
      "grammar": [
        "Can you spot fake news? Always"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Fake News Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Fake News temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Fake News temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Can you spot fake news? Always check the source!",
        "Beceri Lab: Konusma - esli calisma, Fake News konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Fake News temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Fake News konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Fake News temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Fake News konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Fake News konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 15,
    "theme": "Advertising & Persuasion",
    "theme_tr": "Reklam ve Ikna",
    "vocab": [
      "advertisement",
      "target audience",
      "slogan",
      "brand",
      "consumer",
      "influence",
      "persuade",
      "commercial",
      "sponsor",
      "marketing"
    ],
    "structure": "This ad is designed to persuade teenagers to buy the product.",
    "skills": {
      "listening": "Reklam analizlerini dinler.",
      "speaking": "Reklam stratejilerini tartisir.",
      "reading": "Reklam teknikleri makalesini okur.",
      "writing": "Reklam analizi yazar."
    },
    "linked_content": {
      "categories": [
        "Medya"
      ],
      "songs": [
        "Advertising & Persuasion Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Advertising & Persuasion Dialogue"
      ],
      "readings": [
        "Advertising & Persuasion Reading"
      ],
      "writings": [
        "Advertising & Persuasion Writing"
      ],
      "grammar": [
        "This ad is designed to persuade teenagers to buy the product"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Advertising & Persuasion Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Advertising & Persuasion temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Advertising & Persuasion temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - This ad is designed to persuade teenagers to buy t",
        "Beceri Lab: Konusma - esli calisma, Advertising & Persuasion konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Advertising & Persuasion temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Advertising & Persuasion konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Advertising & Persuasion temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Advertising & Persuasion konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Advertising & Persuasion konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 16,
    "theme": "Digital Citizenship",
    "theme_tr": "Dijital Vatandaslik",
    "vocab": [
      "privacy",
      "password",
      "cyberbullying",
      "netiquette",
      "digital footprint",
      "online safety",
      "responsible",
      "respectful",
      "screenshot",
      "report"
    ],
    "structure": "A responsible digital citizen protects their personal data.",
    "skills": {
      "listening": "Dijital guvenlik sunumlarini dinler.",
      "speaking": "Cevrimici guvenlik kurallarini tartisir.",
      "reading": "Dijital vatandaslik rehberi okur.",
      "writing": "Dijital guvenlik posteri yazar."
    },
    "linked_content": {
      "categories": [
        "Medya"
      ],
      "songs": [
        "Digital Citizenship Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Digital Citizenship Dialogue"
      ],
      "readings": [
        "Digital Citizenship Reading"
      ],
      "writings": [
        "Digital Citizenship Writing"
      ],
      "grammar": [
        "A responsible digital citizen protects their personal data"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Digital Citizenship Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Digital Citizenship temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Digital Citizenship temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - A responsible digital citizen protects their perso",
        "Beceri Lab: Konusma - esli calisma, Digital Citizenship konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Digital Citizenship temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Digital Citizenship konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Digital Citizenship temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Digital Citizenship konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Digital Citizenship konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 17,
    "theme": "Health & Wellness",
    "theme_tr": "Saglik ve Iyi Olus",
    "vocab": [
      "wellness",
      "nutrition",
      "exercise",
      "mental health",
      "stress",
      "balanced diet",
      "hydration",
      "sleep",
      "meditation",
      "lifestyle"
    ],
    "structure": "A healthy lifestyle includes regular exercise and good nutrition.",
    "skills": {
      "listening": "Saglik tavsiyeleri dinler.",
      "speaking": "Saglikli yasam aliskanliklarini tartisir.",
      "reading": "Saglikli yasam rehberi okur.",
      "writing": "Saglikli yasam plani yazar."
    },
    "linked_content": {
      "categories": [
        "Saglik"
      ],
      "songs": [
        "Health & Wellness Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Health & Wellness Dialogue"
      ],
      "readings": [
        "Health & Wellness Reading"
      ],
      "writings": [
        "Health & Wellness Writing"
      ],
      "grammar": [
        "A healthy lifestyle includes regular exercise and good nutrition"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Health & Wellness Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Health & Wellness temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Health & Wellness temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - A healthy lifestyle includes regular exercise and ",
        "Beceri Lab: Konusma - esli calisma, Health & Wellness konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Health & Wellness temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Health & Wellness konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Health & Wellness temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Health & Wellness konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Health & Wellness konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 18,
    "theme": "The Science of Sleep",
    "theme_tr": "Uyku Bilimi",
    "vocab": [
      "circadian rhythm",
      "REM sleep",
      "insomnia",
      "fatigue",
      "nap",
      "melatonin",
      "sleep cycle",
      "restful",
      "drowsy",
      "refreshed"
    ],
    "structure": "Teenagers need about 8-10 hours of sleep per night.",
    "skills": {
      "listening": "Uyku arastirmasi sonuclarini dinler.",
      "speaking": "Uyku aliskanliklarini tartisir.",
      "reading": "Uyku bilimi makalesini okur.",
      "writing": "Uyku gunlugu tutar."
    },
    "linked_content": {
      "categories": [
        "Saglik"
      ],
      "songs": [
        "The Science of Sleep Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "The Science of Sleep Dialogue"
      ],
      "readings": [
        "The Science of Sleep Reading"
      ],
      "writings": [
        "The Science of Sleep Writing"
      ],
      "grammar": [
        "Teenagers need about 8-10 hours of sleep per night"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "The Science of Sleep Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: The Science of Sleep temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - The Science of Sleep temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Teenagers need about 8-10 hours of sleep per night",
        "Beceri Lab: Konusma - esli calisma, The Science of Sleep konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - The Science of Sleep temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - The Science of Sleep konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - The Science of Sleep temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: The Science of Sleep konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "The Science of Sleep konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 19,
    "theme": "Mental Health Awareness",
    "theme_tr": "Ruh Sagligi Farkindaligi",
    "vocab": [
      "anxiety",
      "depression",
      "self-care",
      "therapy",
      "counsellor",
      "coping",
      "mindfulness",
      "resilience",
      "support",
      "wellbeing"
    ],
    "structure": "It is important to talk about your feelings with someone you trust.",
    "skills": {
      "listening": "Ruh sagligi farkindalik sunumlarini dinler.",
      "speaking": "Ruh sagligi konusunda tartisir.",
      "reading": "Ruh sagligi makalesini okur.",
      "writing": "Destek kaynaklari posteri yazar."
    },
    "linked_content": {
      "categories": [
        "Saglik"
      ],
      "songs": [
        "Mental Health Awareness Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Mental Health Awareness Dialogue"
      ],
      "readings": [
        "Mental Health Awareness Reading"
      ],
      "writings": [
        "Mental Health Awareness Writing"
      ],
      "grammar": [
        "It is important to talk about your feelings with someone you trust"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Mental Health Awareness Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Mental Health Awareness temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Mental Health Awareness temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - It is important to talk about your feelings with s",
        "Beceri Lab: Konusma - esli calisma, Mental Health Awareness konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Mental Health Awareness temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Mental Health Awareness konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Mental Health Awareness temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Mental Health Awareness konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Mental Health Awareness konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 20,
    "theme": "Active Living",
    "theme_tr": "Aktif Yasam",
    "vocab": [
      "workout",
      "stamina",
      "flexibility",
      "warm-up",
      "cool-down",
      "marathon",
      "yoga",
      "aerobic",
      "strength",
      "endurance"
    ],
    "structure": "I exercise three times a week to stay fit and healthy.",
    "skills": {
      "listening": "Spor programi tanitimlarini dinler.",
      "speaking": "Egzersiz rutinlerini paylasir.",
      "reading": "Aktif yasam makalesi okur.",
      "writing": "Haftalik egzersiz plani yazar."
    },
    "linked_content": {
      "categories": [
        "Saglik"
      ],
      "songs": [
        "Active Living Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Active Living Dialogue"
      ],
      "readings": [
        "Active Living Reading"
      ],
      "writings": [
        "Active Living Writing"
      ],
      "grammar": [
        "I exercise three times a week to stay fit and healthy"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Active Living Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Active Living temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Active Living temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - I exercise three times a week to stay fit and heal",
        "Beceri Lab: Konusma - esli calisma, Active Living konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Active Living temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Active Living konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Active Living temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Active Living konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Active Living konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 21,
    "theme": "Space & Science",
    "theme_tr": "Uzay ve Bilim",
    "vocab": [
      "planet",
      "galaxy",
      "orbit",
      "satellite",
      "astronaut",
      "telescope",
      "gravity",
      "solar system",
      "universe",
      "exploration"
    ],
    "structure": "The teacher said that Mars is called the Red Planet.",
    "skills": {
      "listening": "Uzay belgeseli dinler.",
      "speaking": "Uzay kesfi hakkinda tartisir.",
      "reading": "Gunes sistemi makalesini okur.",
      "writing": "Gezegen tanitimi yazar."
    },
    "linked_content": {
      "categories": [
        "Bilim"
      ],
      "songs": [
        "Space & Science Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Space & Science Dialogue"
      ],
      "readings": [
        "Space & Science Reading"
      ],
      "writings": [
        "Space & Science Writing"
      ],
      "grammar": [
        "The teacher said that Mars is called the Red Planet"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Space & Science Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Space & Science temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Space & Science temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - The teacher said that Mars is called the Red Plane",
        "Beceri Lab: Konusma - esli calisma, Space & Science konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Space & Science temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Space & Science konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Space & Science temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Space & Science konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Space & Science konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 22,
    "theme": "Life on Other Planets",
    "theme_tr": "Diger Gezegenlerde Yasam",
    "vocab": [
      "extraterrestrial",
      "habitable",
      "atmosphere",
      "oxygen",
      "water",
      "Mars rover",
      "exoplanet",
      "alien",
      "colonise",
      "NASA"
    ],
    "structure": "Scientists reported that water had been found on Mars.",
    "skills": {
      "listening": "Uzay haberleri dinler.",
      "speaking": "Uzayda yasam olasiliklarini tartisir.",
      "reading": "Uzay arastirmasi makalesi okur.",
      "writing": "Uzay haberi yazar."
    },
    "linked_content": {
      "categories": [
        "Bilim"
      ],
      "songs": [
        "Life on Other Planets Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Life on Other Planets Dialogue"
      ],
      "readings": [
        "Life on Other Planets Reading"
      ],
      "writings": [
        "Life on Other Planets Writing"
      ],
      "grammar": [
        "Scientists reported that water had been found on Mars"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Life on Other Planets Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Life on Other Planets temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Life on Other Planets temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Scientists reported that water had been found on M",
        "Beceri Lab: Konusma - esli calisma, Life on Other Planets konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Life on Other Planets temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Life on Other Planets konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Life on Other Planets temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Life on Other Planets konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Life on Other Planets konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 23,
    "theme": "Great Discoveries",
    "theme_tr": "Buyuk Kesifler",
    "vocab": [
      "discovery",
      "experiment",
      "theory",
      "hypothesis",
      "laboratory",
      "microscope",
      "DNA",
      "vaccine",
      "radiation",
      "evolution"
    ],
    "structure": "Marie Curie discovered radium in 1898.",
    "skills": {
      "listening": "Bilim tarihi anlatimlarini dinler.",
      "speaking": "En onemli kesifleri tartisir.",
      "reading": "Bilim insanlari biyografileri okur.",
      "writing": "Kesif hikayesi yazar."
    },
    "linked_content": {
      "categories": [
        "Bilim"
      ],
      "songs": [
        "Great Discoveries Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Great Discoveries Dialogue"
      ],
      "readings": [
        "Great Discoveries Reading"
      ],
      "writings": [
        "Great Discoveries Writing"
      ],
      "grammar": [
        "Marie Curie discovered radium in 1898"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Great Discoveries Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Great Discoveries temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Great Discoveries temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Marie Curie discovered radium in 1898.",
        "Beceri Lab: Konusma - esli calisma, Great Discoveries konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Great Discoveries temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Great Discoveries konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Great Discoveries temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Great Discoveries konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Great Discoveries konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 24,
    "theme": "Turkey in Space",
    "theme_tr": "Turkiyenin Uzay Seruveni",
    "vocab": [
      "space agency",
      "rocket",
      "launch",
      "mission",
      "cosmonaut",
      "space station",
      "research",
      "technology",
      "innovation",
      "TUBITAK"
    ],
    "structure": "Turkey established its national space agency in 2018.",
    "skills": {
      "listening": "Turkiye uzay programi sunumlarini dinler.",
      "speaking": "Turkiyenin uzay hedeflerini tartisir.",
      "reading": "TUBITAK projeleri hakkinda okur.",
      "writing": "Uzay programi tanitimi yazar."
    },
    "linked_content": {
      "categories": [
        "Bilim"
      ],
      "songs": [
        "Turkey in Space Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Turkey in Space Dialogue"
      ],
      "readings": [
        "Turkey in Space Reading"
      ],
      "writings": [
        "Turkey in Space Writing"
      ],
      "grammar": [
        "Turkey established its national space agency in 2018"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Turkey in Space Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Turkey in Space temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Turkey in Space temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Turkey established its national space agency in 20",
        "Beceri Lab: Konusma - esli calisma, Turkey in Space konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Turkey in Space temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Turkey in Space konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Turkey in Space temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Turkey in Space konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Turkey in Space konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 25,
    "theme": "Migration & Culture",
    "theme_tr": "Goc ve Kultur",
    "vocab": [
      "migration",
      "immigrant",
      "refugee",
      "border",
      "homeland",
      "diaspora",
      "integration",
      "multicultural",
      "asylum",
      "displacement"
    ],
    "structure": "There are too many challenges for refugees, but they are not enough supported.",
    "skills": {
      "listening": "Goc hikayeleri dinler.",
      "speaking": "Goc konusunda tartisir.",
      "reading": "Goc makalesi okur.",
      "writing": "Goc hikayesi yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Migration & Culture Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Migration & Culture Dialogue"
      ],
      "readings": [
        "Migration & Culture Reading"
      ],
      "writings": [
        "Migration & Culture Writing"
      ],
      "grammar": [
        "There are too many challenges for refugees, but they are not enough supported"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Migration & Culture Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Migration & Culture temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Migration & Culture temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - There are too many challenges for refugees, but th",
        "Beceri Lab: Konusma - esli calisma, Migration & Culture konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Migration & Culture temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Migration & Culture konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Migration & Culture temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Migration & Culture konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Migration & Culture konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 26,
    "theme": "Living Between Cultures",
    "theme_tr": "Kulturler Arasinda Yasamak",
    "vocab": [
      "bilingual",
      "assimilation",
      "identity crisis",
      "dual nationality",
      "culture shock",
      "adaptation",
      "belonging",
      "roots",
      "diversity",
      "acceptance"
    ],
    "structure": "Moving to a new country was too difficult for Kwame at first.",
    "skills": {
      "listening": "Kulturlerarasi deneyimleri dinler.",
      "speaking": "Kulturel uyum konusunda tartisir.",
      "reading": "Kulturlerarasi hikayeler okur.",
      "writing": "Kulturel deneyim anlatisi yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Living Between Cultures Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Living Between Cultures Dialogue"
      ],
      "readings": [
        "Living Between Cultures Reading"
      ],
      "writings": [
        "Living Between Cultures Writing"
      ],
      "grammar": [
        "Moving to a new country was too difficult for Kwame at first"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Living Between Cultures Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Living Between Cultures temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Living Between Cultures temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Moving to a new country was too difficult for Kwam",
        "Beceri Lab: Konusma - esli calisma, Living Between Cultures konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Living Between Cultures temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Living Between Cultures konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Living Between Cultures temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Living Between Cultures konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Living Between Cultures konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 27,
    "theme": "Welcome to Our Community",
    "theme_tr": "Toplumumuza Hosgeldiniz",
    "vocab": [
      "community",
      "volunteer",
      "charity",
      "donate",
      "shelter",
      "support",
      "solidarity",
      "empathy",
      "inclusion",
      "harmony"
    ],
    "structure": "Our community organised enough food and clothing for the new families.",
    "skills": {
      "listening": "Topluluk projeleri hakkinda dinler.",
      "speaking": "Topluluk destegi fikirlerini tartisir.",
      "reading": "Topluluk projesi raporunu okur.",
      "writing": "Karsilama projesi onerisi yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Welcome to Our Community Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Welcome to Our Community Dialogue"
      ],
      "readings": [
        "Welcome to Our Community Reading"
      ],
      "writings": [
        "Welcome to Our Community Writing"
      ],
      "grammar": [
        "Our community organised enough food and clothing for the new families"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Welcome to Our Community Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Welcome to Our Community temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Welcome to Our Community temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Our community organised enough food and clothing f",
        "Beceri Lab: Konusma - esli calisma, Welcome to Our Community konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Welcome to Our Community temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Welcome to Our Community konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Welcome to Our Community temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Welcome to Our Community konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Welcome to Our Community konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 28,
    "theme": "Film & Media",
    "theme_tr": "Film ve Medya",
    "vocab": [
      "director",
      "screenplay",
      "actor",
      "genre",
      "documentary",
      "animation",
      "sequel",
      "review",
      "soundtrack",
      "scene"
    ],
    "structure": "I enjoy watching documentaries about nature and wildlife.",
    "skills": {
      "listening": "Film tanitim fragmanlarini dinler.",
      "speaking": "Film turlerini tartisir.",
      "reading": "Film elestirisi okur.",
      "writing": "Film incelemesi yazar."
    },
    "linked_content": {
      "categories": [
        "Sanat"
      ],
      "songs": [
        "Film & Media Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Film & Media Dialogue"
      ],
      "readings": [
        "Film & Media Reading"
      ],
      "writings": [
        "Film & Media Writing"
      ],
      "grammar": [
        "I enjoy watching documentaries about nature and wildlife"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Film & Media Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Film & Media temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Film & Media temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - I enjoy watching documentaries about nature and wi",
        "Beceri Lab: Konusma - esli calisma, Film & Media konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Film & Media temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Film & Media konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Film & Media temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Film & Media konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Film & Media konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 29,
    "theme": "How Movies Shape Our World",
    "theme_tr": "Filmler Dunyamizi Nasil Sekillendiriyor",
    "vocab": [
      "influence",
      "stereotype",
      "representation",
      "diversity",
      "blockbuster",
      "independent film",
      "cinematography",
      "special effects",
      "award",
      "premiere"
    ],
    "structure": "Movies can influence how people think about different cultures.",
    "skills": {
      "listening": "Film analizi sunumlarini dinler.",
      "speaking": "Filmlerin etkisini tartisir.",
      "reading": "Sinema tarihi makalesini okur.",
      "writing": "Film oneri yazisi yazar."
    },
    "linked_content": {
      "categories": [
        "Sanat"
      ],
      "songs": [
        "How Movies Shape Our World Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "How Movies Shape Our World Dialogue"
      ],
      "readings": [
        "How Movies Shape Our World Reading"
      ],
      "writings": [
        "How Movies Shape Our World Writing"
      ],
      "grammar": [
        "Movies can influence how people think about different cultures"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "How Movies Shape Our World Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: How Movies Shape Our World temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - How Movies Shape Our World temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Movies can influence how people think about differ",
        "Beceri Lab: Konusma - esli calisma, How Movies Shape Our World konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - How Movies Shape Our World temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - How Movies Shape Our World konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - How Movies Shape Our World temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: How Movies Shape Our World konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "How Movies Shape Our World konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 30,
    "theme": "Lights, Camera, Action!",
    "theme_tr": "Isiklar, Kamera, Motor!",
    "vocab": [
      "script",
      "cast",
      "crew",
      "costume",
      "set design",
      "editing",
      "storyboard",
      "audition",
      "rehearsal",
      "production"
    ],
    "structure": "First, write a script. Then, choose your cast and start rehearsing.",
    "skills": {
      "listening": "Film yapim surecini dinler.",
      "speaking": "Kisa film fikirlerini paylasir.",
      "reading": "Film yapim rehberini okur.",
      "writing": "Kisa film senaryosu yazar."
    },
    "linked_content": {
      "categories": [
        "Sanat"
      ],
      "songs": [
        "Lights, Camera, Action! Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Lights, Camera, Action! Dialogue"
      ],
      "readings": [
        "Lights, Camera, Action! Reading"
      ],
      "writings": [
        "Lights, Camera, Action! Writing"
      ],
      "grammar": [
        "First, write a script"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Lights, Camera, Action! Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Lights, Camera, Action! temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Lights, Camera, Action! temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - First, write a script. Then, choose your cast and ",
        "Beceri Lab: Konusma - esli calisma, Lights, Camera, Action! konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Lights, Camera, Action! temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Lights, Camera, Action! konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Lights, Camera, Action! temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Lights, Camera, Action! konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Lights, Camera, Action! konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 31,
    "theme": "Technology & AI",
    "theme_tr": "Teknoloji ve Yapay Zeka",
    "vocab": [
      "artificial intelligence",
      "algorithm",
      "automation",
      "robot",
      "machine learning",
      "virtual reality",
      "smart device",
      "innovation",
      "coding",
      "data"
    ],
    "structure": "AI is being used in many areas of our daily lives.",
    "skills": {
      "listening": "Teknoloji haberleri dinler.",
      "speaking": "Yapay zekanin etkisini tartisir.",
      "reading": "AI makalesi okur.",
      "writing": "Teknoloji blog yazisi yazar."
    },
    "linked_content": {
      "categories": [
        "Teknoloji"
      ],
      "songs": [
        "Technology & AI Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Technology & AI Dialogue"
      ],
      "readings": [
        "Technology & AI Reading"
      ],
      "writings": [
        "Technology & AI Writing"
      ],
      "grammar": [
        "AI is being used in many areas of our daily lives"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Technology & AI Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Technology & AI temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Technology & AI temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - AI is being used in many areas of our daily lives.",
        "Beceri Lab: Konusma - esli calisma, Technology & AI konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Technology & AI temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Technology & AI konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Technology & AI temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Technology & AI konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Technology & AI konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 32,
    "theme": "Living with AI",
    "theme_tr": "Yapay Zeka ile Yasamak",
    "vocab": [
      "chatbot",
      "recommendation",
      "personalised",
      "ethical",
      "bias",
      "privacy",
      "surveillance",
      "autonomous",
      "self-driving",
      "predictive"
    ],
    "structure": "Should we be worried about AI making decisions for us?",
    "skills": {
      "listening": "AI tartisma programi dinler.",
      "speaking": "AI etik konularini tartisir.",
      "reading": "AI etik makalesi okur.",
      "writing": "AI politika onerisi yazar."
    },
    "linked_content": {
      "categories": [
        "Teknoloji"
      ],
      "songs": [
        "Living with AI Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Living with AI Dialogue"
      ],
      "readings": [
        "Living with AI Reading"
      ],
      "writings": [
        "Living with AI Writing"
      ],
      "grammar": [
        "Should we be worried about AI "
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Living with AI Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Living with AI temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Living with AI temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Should we be worried about AI making decisions for",
        "Beceri Lab: Konusma - esli calisma, Living with AI konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Living with AI temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Living with AI konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Living with AI temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Living with AI konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Living with AI konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 33,
    "theme": "Digital Future",
    "theme_tr": "Dijital Gelecek",
    "vocab": [
      "blockchain",
      "metaverse",
      "wearable tech",
      "5G",
      "Internet of Things",
      "cloud computing",
      "digital twin",
      "smart city",
      "renewable",
      "sustainable tech"
    ],
    "structure": "In the future, smart cities will use AI to manage traffic.",
    "skills": {
      "listening": "Gelecek teknoloji sunumlarini dinler.",
      "speaking": "Dijital gelecegi tahmin eder.",
      "reading": "Gelecek teknoloji makalesi okur.",
      "writing": "Gelecek vizyonu kompozisyonu yazar."
    },
    "linked_content": {
      "categories": [
        "Teknoloji"
      ],
      "songs": [
        "Digital Future Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Digital Future Dialogue"
      ],
      "readings": [
        "Digital Future Reading"
      ],
      "writings": [
        "Digital Future Writing"
      ],
      "grammar": [
        "In the future, smart cities will use AI to manage traffic"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Digital Future Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Digital Future temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Digital Future temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - In the future, smart cities will use AI to manage ",
        "Beceri Lab: Konusma - esli calisma, Digital Future konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Digital Future temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Digital Future konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Digital Future temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Digital Future konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Digital Future konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 34,
    "theme": "Making a Difference",
    "theme_tr": "Fark Yaratmak",
    "vocab": [
      "activist",
      "campaign",
      "petition",
      "awareness",
      "impact",
      "inspire",
      "advocate",
      "change",
      "movement",
      "sustainable"
    ],
    "structure": "Young people can make a real difference in the world, can not they?",
    "skills": {
      "listening": "Genc aktivist hikayelerini dinler.",
      "speaking": "Degisim yaratma yollarini tartisir.",
      "reading": "Fark yaratan cocuklar makalesi okur.",
      "writing": "Degisim kampanyasi onerisi yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Making a Difference Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Making a Difference Dialogue"
      ],
      "readings": [
        "Making a Difference Reading"
      ],
      "writings": [
        "Making a Difference Writing"
      ],
      "grammar": [
        "Young people can make a real d"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Making a Difference Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Making a Difference temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Making a Difference temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Young people can make a real difference in the wor",
        "Beceri Lab: Konusma - esli calisma, Making a Difference konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Making a Difference temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Making a Difference konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Making a Difference temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Making a Difference konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Making a Difference konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 35,
    "theme": "Young Leaders",
    "theme_tr": "Genc Liderler",
    "vocab": [
      "leadership",
      "initiative",
      "community service",
      "fundraising",
      "environmental",
      "social justice",
      "human rights",
      "education",
      "empowerment",
      "legacy"
    ],
    "structure": "Greta Thunberg started a global movement, did not she?",
    "skills": {
      "listening": "Genc lider roportajlarini dinler.",
      "speaking": "Liderlik niteliklerini tartisir.",
      "reading": "Genc liderler biyografisi okur.",
      "writing": "Liderlik profili yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Young Leaders Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Young Leaders Dialogue"
      ],
      "readings": [
        "Young Leaders Reading"
      ],
      "writings": [
        "Young Leaders Writing"
      ],
      "grammar": [
        "Greta Thunberg started a globa"
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Young Leaders Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Young Leaders temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Young Leaders temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - Greta Thunberg started a global movement, did not ",
        "Beceri Lab: Konusma - esli calisma, Young Leaders konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Young Leaders temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Young Leaders konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Young Leaders temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Young Leaders konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Young Leaders konusunda beceri degerlendirmesi yapilir."
  },
  {
    "week": 36,
    "theme": "Our Action Plan",
    "theme_tr": "Eylem Planimiz",
    "vocab": [
      "project",
      "goal",
      "timeline",
      "resource",
      "teamwork",
      "evaluate",
      "feedback",
      "presentation",
      "reflection",
      "achievement"
    ],
    "structure": "We have planned our community project, have not we?",
    "skills": {
      "listening": "Proje sunumlarini dinler.",
      "speaking": "Sinif projesini planlar.",
      "reading": "Proje degerlendirme rehberi okur.",
      "writing": "Proje yansima raporu yazar."
    },
    "linked_content": {
      "categories": [
        "Toplum"
      ],
      "songs": [
        "Our Action Plan Song"
      ],
      "games": [
        "Eslestirme",
        "Kelime Avi"
      ],
      "dialogues": [
        "Our Action Plan Dialogue"
      ],
      "readings": [
        "Our Action Plan Reading"
      ],
      "writings": [
        "Our Action Plan Writing"
      ],
      "grammar": [
        "We have planned our community "
      ],
      "phonics": [
        "Sentence Stress"
      ],
      "listening": [
        "Our Action Plan Listening"
      ]
    },
    "days": {
      "mon": [
        "Ana Ders: Our Action Plan temel kelimelerini tanitim + yapi sunumu",
        "Beceri Lab: Dinleme - Our Action Plan temali diyalogu dinle"
      ],
      "tue": [
        "Ana Ders: Gramer odak - We have planned our community project, have not we",
        "Beceri Lab: Konusma - esli calisma, Our Action Plan konusunda soru-cevap"
      ],
      "wed": [
        "Ana Ders: Okuma - Our Action Plan temali metin oku, anlama sorularini cevapla",
        "Beceri Lab: Yazma - Our Action Plan konusunda rehberli paragraf yazma"
      ],
      "thu": [
        "Ana Ders: Kelime pekistirme + gramer tekrari ve alishtirmalar",
        "Beceri Lab: Proje/Sunum - Our Action Plan temali poster/sunum hazirlama"
      ],
      "fri": [
        "Native Speaker: Our Action Plan konusunda serbest konusma + kulturel karsilastirma",
        "Native Speaker: Telaffuz + haftalik kelime/yapi tekrar oyunlari"
      ]
    },
    "assessment": "Our Action Plan konusunda beceri degerlendirmesi yapilir."
  }
]


# =============================================================================
# 8. SINIF - CEFR A2.4/B1 (Ust Iletisim)
# =============================================================================

CURRICULUM_GRADE8 = [
    # ===== DONEM 1 (Hafta 1-18) =====
    # ===== UNITE 1: Identity & Personality (Hafta 1-4) =====
    {
        "week": 1,
        "theme": "Identity & Personality",
        "theme_tr": "Kimlik ve Kisilik",
        "vocab": ["identity", "personality", "trait", "confident", "generous", "stubborn", "ambitious",
                  "reliable", "outgoing", "shy", "selfish", "honest", "loyal", "independent", "creative"],
        "structure": "I consider myself reliable. She is the kind of person who... What are your strengths and weaknesses?",
        "skills": {
            "listening": "Kisilik ozelliklerini anlatan roportajlari dinler, sifatlari ve aciklamalari eslestirir.",
            "speaking": "Kendi kisilik ozelliklerini guclu ve zayif yonleriyle tanitir.",
            "reading": "Farkli kisilik tiplerini anlatan metni okur (120-140 kelime), sorulari cevaplar.",
            "writing": "Kendi kimligini ve kisilik ozelliklerini anlatan bir paragraf yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Kisilik", "Kimlik"],
            "songs": ["Who Am I?"],
            "games": ["Kisilik Testi", "Sifat Eslestir"],
            "dialogues": ["Describing Yourself"],
            "readings": ["Personality Types"],
            "writings": ["About Myself"],
            "grammar": ["Relative clauses (who/that/which)"],
            "phonics": ["Syllable stress in adjectives"],
            "listening": ["Kisilik Roportaji"],
        },
        "days": {
            "mon": ["Ana Ders: Kimlik ve Kisilik temel kelimelerini tanitim (identity/personality/trait) + yapi sunumu: I consider myself reliable. She is the kind of person who...", "Beceri Lab: Dinleme — 'Kimlik ve Kisilik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Relative clauses (who/that/which) yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kimlik ve Kisilik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kimlik ve Kisilik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kimlik ve Kisilik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (confident/generous/stubborn) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kimlik ve Kisilik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kimlik ve Kisilik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kendi kisilik ozelliklerini relative clause kullanarak tanimlayabilir.",
    },
    {
        "week": 2,
        "theme": "Personal Values",
        "theme_tr": "Kisisel Degerler",
        "vocab": ["value", "respect", "tolerance", "empathy", "integrity", "responsibility", "fairness",
                  "courage", "compassion", "dignity", "principle", "moral", "ethical", "virtue", "belief"],
        "structure": "I believe that honesty is important. In my opinion, respect means... What values are important to you?",
        "skills": {
            "listening": "Degerler hakkindaki tartismalari dinler, farkli gorusleri saptar.",
            "speaking": "Kendisi icin onemli olan degerleri aciklar ve nedenleriyle sunar.",
            "reading": "Degerler hakkinda kisa bir makaleyi okur, ana fikirleri cikarir.",
            "writing": "En onemli buldugu uc degeri aciklayan bir yazi yazar (8-10 cumle).",
        },
        "linked_content": {
            "categories": ["Degerler", "Kisilik"],
            "songs": [],
            "games": ["Deger Siralama", "Tartisma Kartlari"],
            "dialogues": ["What Do You Value Most?"],
            "readings": ["Values That Matter"],
            "writings": ["My Core Values"],
            "grammar": ["I believe that... / In my opinion... + noun clauses"],
            "phonics": ["Intonation in opinion statements"],
            "listening": ["Degerler Tartismasi"],
        },
        "days": {
            "mon": ["Ana Ders: Kisisel Degerler temel kelimelerini tanitim (value/respect/tolerance) + yapi sunumu: I believe that honesty is important. In my opinion...", "Beceri Lab: Dinleme — 'Kisisel Degerler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I believe that... / In my opinion... + noun clauses yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kisisel Degerler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kisisel Degerler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kisisel Degerler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (empathy/integrity/responsibility) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kisisel Degerler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kisisel Degerler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kisisel degerlerini nedenleriyle aciklayabilir ve goruslerini ifade edebilir.",
    },
    {
        "week": 3,
        "theme": "Role Models",
        "theme_tr": "Rol Modeller",
        "vocab": ["role model", "inspire", "influence", "admire", "achievement", "determination", "dedication",
                  "overcome", "obstacle", "success", "goal", "motivation", "idol", "contribution", "legacy"],
        "structure": "I admire her because she overcame many obstacles. He inspires me to... The person who influenced me most is...",
        "skills": {
            "listening": "Bir rol model hakkindaki sunumu dinler, basarilarini ve ozelliklerini not eder.",
            "speaking": "Rol modelini tanitir ve neden onu ornek aldigini aciklar.",
            "reading": "Ilham veren bir kisinin hikayesini okur, onemli detaylari cikarir.",
            "writing": "Rol modelini tanitan bir kompozisyon yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Kisilik", "Biyografi"],
            "songs": [],
            "games": ["Tahmin Et Kim?", "Biyografi Eslestir"],
            "dialogues": ["Who Is Your Role Model?"],
            "readings": ["Inspiring People"],
            "writings": ["My Role Model"],
            "grammar": ["Past Simple + because clauses"],
            "phonics": ["Connected speech: linking sounds"],
            "listening": ["Rol Model Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Rol Modeller temel kelimelerini tanitim (role model/inspire/influence) + yapi sunumu: I admire her because she overcame many obstacles.", "Beceri Lab: Dinleme — 'Rol Modeller' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Past Simple + because clauses yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Rol Modeller konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Rol Modeller' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Rol Modeller konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (admire/achievement/determination) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Rol Modeller temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Rol Modeller konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Rol modelini tanitabilir ve neden onu ornek aldigini aciklayabilir.",
    },
    {
        "week": 4,
        "theme": "Self-Awareness",
        "theme_tr": "Oz Farkindalik",
        "vocab": ["self-awareness", "strength", "weakness", "improve", "develop", "reflect", "emotion",
                  "behaviour", "attitude", "mindset", "growth", "potential", "challenge", "feedback", "goal-setting"],
        "structure": "I need to improve my... One of my strengths is... I'm trying to develop... If I could change one thing about myself...",
        "skills": {
            "listening": "Oz degerlendirme hakkindaki konusmalari dinler, guclu ve zayif yonleri belirler.",
            "speaking": "Kendi guclu ve zayif yonlerini degerlendirir, gelisim hedeflerini paylasir.",
            "reading": "Oz farkindalik hakkinda bir metni okur, stratejileri listeler.",
            "writing": "Kisisel SWOT analizi yapar ve gelisim plani yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Kisilik", "Gelisim"],
            "songs": [],
            "games": ["SWOT Kartlari", "Hedef Belirleme"],
            "dialogues": ["Setting Personal Goals"],
            "readings": ["Know Yourself"],
            "writings": ["My Personal SWOT"],
            "grammar": ["need to / trying to + infinitive; If + Past Simple (2nd conditional intro)"],
            "phonics": ["Stress in compound words"],
            "listening": ["Oz Degerlendirme Konusmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Oz Farkindalik temel kelimelerini tanitim (self-awareness/strength/weakness) + yapi sunumu: I need to improve my... One of my strengths is...", "Beceri Lab: Dinleme — 'Oz Farkindalik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — need to / trying to + infinitive; If + Past Simple yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Oz Farkindalik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Oz Farkindalik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Oz Farkindalik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (improve/develop/reflect) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Oz Farkindalik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Oz Farkindalik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kisisel guclu/zayif yonlerini degerlendirip gelisim hedefi belirleyebilir.",
    },
    # ===== UNITE 2: Languages & Communication (Hafta 5-8) =====
    {
        "week": 5,
        "theme": "Languages & Communication",
        "theme_tr": "Diller ve Iletisim",
        "vocab": ["language", "multilingual", "bilingual", "mother tongue", "foreign language", "dialect",
                  "accent", "fluent", "communicate", "expression", "gesture", "interpret", "translate", "native speaker", "global"],
        "structure": "How many languages can you speak? I can speak... fluently. English is spoken all over the world.",
        "skills": {
            "listening": "Cok dilli kisilerin deneyimlerini dinler, dil bilgilerini ve goruslerini saptar.",
            "speaking": "Bildigi dilleri ve dil ogrenme deneyimlerini anlatir.",
            "reading": "Dunya dillerini tanitan bir makaleyi okur, istatistikleri yorumlar.",
            "writing": "Dil ogrenmenin onemine dair goruslerini iceren bir paragraf yazar.",
        },
        "linked_content": {
            "categories": ["Diller", "Iletisim"],
            "songs": ["Languages of the World"],
            "games": ["Dil Haritasi", "Ceviri Yarismasi"],
            "dialogues": ["How Many Languages Do You Speak?"],
            "readings": ["World Languages"],
            "writings": ["Why Learn Languages?"],
            "grammar": ["Passive Voice (Present Simple): is spoken / are used"],
            "phonics": ["Vowel sounds across languages"],
            "listening": ["Cok Dilli Roportaj"],
        },
        "days": {
            "mon": ["Ana Ders: Diller ve Iletisim temel kelimelerini tanitim (language/multilingual/bilingual) + yapi sunumu: How many languages can you speak? English is spoken all over the world.", "Beceri Lab: Dinleme — 'Diller ve Iletisim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive Voice (Present Simple): is spoken / are used yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Diller ve Iletisim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Diller ve Iletisim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Diller ve Iletisim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (fluent/communicate/expression) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Diller ve Iletisim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Diller ve Iletisim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Dil cesitliligini ve iletisimin onemini passive voice kullanarak aciklayabilir.",
    },
    {
        "week": 6,
        "theme": "Body Language",
        "theme_tr": "Beden Dili",
        "vocab": ["body language", "facial expression", "eye contact", "posture", "gesture", "nod", "shake",
                  "cross arms", "smile", "frown", "signal", "nonverbal", "impression", "confident", "nervous"],
        "structure": "If you cross your arms, it means... Making eye contact shows... Body language is as important as words.",
        "skills": {
            "listening": "Beden dili hakkinda bir sunumu dinler, anlamlari ve ipuclarini eslestirir.",
            "speaking": "Farkli beden dili isaretlerini tanitir ve anlamlarini aciklar.",
            "reading": "Beden dili ve kulturel farkliliklari anlatan metni okur.",
            "writing": "Beden dilinin iletisimdeki rolu hakkinda bir paragraf yazar.",
        },
        "linked_content": {
            "categories": ["Iletisim", "Kultur"],
            "songs": [],
            "games": ["Pantomim", "Beden Dili Tahmin"],
            "dialogues": ["What Does This Gesture Mean?"],
            "readings": ["The Power of Body Language"],
            "writings": ["Body Language Around the World"],
            "grammar": ["If + Present Simple (1st conditional); means + gerund/noun"],
            "phonics": ["Intonation patterns for emphasis"],
            "listening": ["Beden Dili Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Beden Dili temel kelimelerini tanitim (body language/facial expression/eye contact) + yapi sunumu: If you cross your arms, it means...", "Beceri Lab: Dinleme — 'Beden Dili' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — If + Present Simple (1st conditional); means + gerund/noun yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Beden Dili konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Beden Dili' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Beden Dili konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (posture/gesture/nod) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Beden Dili temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Beden Dili konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Beden dili isaretlerini taniyabilir ve kulturel farkliliklari aciklayabilir.",
    },
    {
        "week": 7,
        "theme": "Digital Communication",
        "theme_tr": "Dijital Iletisim",
        "vocab": ["email", "text message", "video call", "emoji", "abbreviation", "formal", "informal",
                  "attachment", "subject line", "recipient", "forward", "reply", "cc", "netiquette", "tone"],
        "structure": "Could you please send me...? I'm writing to inform you that... In formal emails, you should...",
        "skills": {
            "listening": "Resmi ve gayriresmi iletisim farklarini anlatan konusmayi dinler.",
            "speaking": "Resmi ve gayriresmi dijital iletisim arasindaki farklari tartisir.",
            "reading": "Resmi bir e-posta ve gayriresmi bir mesaji karsilastirarak okur.",
            "writing": "Bir resmi e-posta ve bir gayriresmi mesaj yazar.",
        },
        "linked_content": {
            "categories": ["Iletisim", "Teknoloji"],
            "songs": [],
            "games": ["Resmi mi Gayriresmi mi?", "E-posta Duzenleme"],
            "dialogues": ["Writing a Formal Email"],
            "readings": ["Formal vs Informal Communication"],
            "writings": ["A Formal Email"],
            "grammar": ["Could you please...? / I'm writing to... / formal register"],
            "phonics": ["Polite intonation"],
            "listening": ["Resmi-Gayriresmi Karsilastirma"],
        },
        "days": {
            "mon": ["Ana Ders: Dijital Iletisim temel kelimelerini tanitim (email/text message/video call) + yapi sunumu: Could you please send me...? I'm writing to inform you that...", "Beceri Lab: Dinleme — 'Dijital Iletisim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Could you please...? / I'm writing to... / formal register yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dijital Iletisim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dijital Iletisim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dijital Iletisim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (formal/informal/attachment) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dijital Iletisim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dijital Iletisim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Resmi e-posta ve gayriresmi mesaj arasindaki farklari bilir ve yazabilir.",
    },
    {
        "week": 8,
        "theme": "Intercultural Communication",
        "theme_tr": "Kulturlerarasi Iletisim",
        "vocab": ["culture", "custom", "tradition", "etiquette", "greet", "handshake", "bow", "taboo",
                  "stereotype", "diversity", "multicultural", "misunderstanding", "adapt", "open-minded", "awareness"],
        "structure": "In Turkey, people usually... whereas in Japan... It is considered rude to... You are expected to...",
        "skills": {
            "listening": "Farkli kulturlerdeki iletisim adetlerini anlatan sunumu dinler.",
            "speaking": "Turk kulturundeki iletisim adetlerini diger kulturlerle karsilastirir.",
            "reading": "Kulturlerarasi iletisim hatalarini anlatan metni okur.",
            "writing": "Kendi kulturundeki iletisim adetlerini anlatan bir yazi yazar.",
        },
        "linked_content": {
            "categories": ["Kultur", "Iletisim"],
            "songs": [],
            "games": ["Kultur Bilgi Yarismasi", "Adet Eslestir"],
            "dialogues": ["Cultural Differences in Communication"],
            "readings": ["Communication Across Cultures"],
            "writings": ["Communication Customs in My Culture"],
            "grammar": ["Passive: is considered / are expected + contrast: whereas / while"],
            "phonics": ["Rising vs falling intonation"],
            "listening": ["Kulturel Farkliliklar Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Kulturlerarasi Iletisim temel kelimelerini tanitim (culture/custom/tradition) + yapi sunumu: In Turkey, people usually... whereas in Japan...", "Beceri Lab: Dinleme — 'Kulturlerarasi Iletisim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive: is considered / are expected + contrast: whereas / while yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kulturlerarasi Iletisim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kulturlerarasi Iletisim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kulturlerarasi Iletisim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (etiquette/greet/handshake) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kulturlerarasi Iletisim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kulturlerarasi Iletisim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Farkli kulturlerdeki iletisim adetlerini karsilastirabilir ve kulturel farkindalik gosterebilir.",
    },
    # ===== UNITE 3: Science & Ethics (Hafta 9-12) =====
    {
        "week": 9,
        "theme": "Science & Ethics",
        "theme_tr": "Bilim ve Etik",
        "vocab": ["science", "ethics", "experiment", "hypothesis", "evidence", "research", "discovery",
                  "invention", "laboratory", "scientist", "theory", "conclusion", "data", "method", "breakthrough"],
        "structure": "Scientists have discovered that... This experiment was conducted to... According to the research...",
        "skills": {
            "listening": "Bilimsel bir kesfin anlatimini dinler, asamalari ve sonuclari saptar.",
            "speaking": "Bilimsel bir kesfin onemini ve etkilerini tartisir.",
            "reading": "Onemli bir bilimsel kesif hakkinda makale okur, bilgileri cikarir.",
            "writing": "Bir bilimsel kesfi ozetleyen bir paragraf yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Bilim", "Etik"],
            "songs": [],
            "games": ["Bilim Bilgi Yarismasi", "Kesif Zaman Cizelgesi"],
            "dialogues": ["Great Scientific Discoveries"],
            "readings": ["Breakthroughs in Science"],
            "writings": ["A Scientific Discovery"],
            "grammar": ["Present Perfect: have discovered / has been conducted"],
            "phonics": ["Word stress in scientific terms"],
            "listening": ["Bilimsel Kesif Anlatimi"],
        },
        "days": {
            "mon": ["Ana Ders: Bilim ve Etik temel kelimelerini tanitim (science/ethics/experiment) + yapi sunumu: Scientists have discovered that... This experiment was conducted to...", "Beceri Lab: Dinleme — 'Bilim ve Etik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect: have discovered / has been conducted yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Bilim ve Etik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Bilim ve Etik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Bilim ve Etik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (hypothesis/evidence/research) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Bilim ve Etik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Bilim ve Etik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bilimsel kesfin asamalarini Present Perfect kullanarak anlatabilir.",
    },
    {
        "week": 10,
        "theme": "Famous Scientists",
        "theme_tr": "Unlu Bilim Insanlari",
        "vocab": ["physicist", "chemist", "biologist", "Nobel Prize", "contribution", "pioneering", "genius",
                  "publish", "patent", "collaborate", "peer review", "groundbreaking", "influential", "legacy", "innovator"],
        "structure": "Marie Curie was awarded the Nobel Prize. He is known for... She devoted her life to...",
        "skills": {
            "listening": "Unlu bir bilim insaninin biyografisini dinler, onemli tarihleri ve basarilari not eder.",
            "speaking": "Bir bilim insanini tanitir, hayatini ve katkilarini ozetler.",
            "reading": "Iki bilim insaninin biyografilerini karsilastirarak okur.",
            "writing": "Bir bilim insaninin biyografisini yazar (12-14 cumle).",
        },
        "linked_content": {
            "categories": ["Bilim", "Biyografi"],
            "songs": [],
            "games": ["Bilim Insani Eslestir", "Zaman Cizelgesi"],
            "dialogues": ["Talking About Scientists"],
            "readings": ["Great Minds in Science"],
            "writings": ["Biography of a Scientist"],
            "grammar": ["Passive Voice (Past): was awarded / was published / is known for"],
            "phonics": ["Pronunciation of -tion / -sion endings"],
            "listening": ["Bilim Insani Biyografisi"],
        },
        "days": {
            "mon": ["Ana Ders: Unlu Bilim Insanlari temel kelimelerini tanitim (physicist/chemist/biologist) + yapi sunumu: Marie Curie was awarded the Nobel Prize. He is known for...", "Beceri Lab: Dinleme — 'Unlu Bilim Insanlari' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive Voice (Past): was awarded / was published / is known for yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Unlu Bilim Insanlari konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Unlu Bilim Insanlari' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Unlu Bilim Insanlari konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (Nobel Prize/contribution/pioneering) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Unlu Bilim Insanlari temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Unlu Bilim Insanlari konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir bilim insaninin hayatini ve katkilarini Passive Voice ile anlatabilir.",
    },
    {
        "week": 11,
        "theme": "Ethical Dilemmas",
        "theme_tr": "Etik Ikilemler",
        "vocab": ["dilemma", "consequence", "decision", "moral", "right", "wrong", "fair", "unfair",
                  "justify", "argue", "perspective", "debate", "compromise", "principle", "controversial"],
        "structure": "On one hand... on the other hand... I think it would be better if... What would you do if...?",
        "skills": {
            "listening": "Etik ikilem tartismasini dinler, farkli bakis acilarini saptar.",
            "speaking": "Bir etik ikilem hakkinda gorusunu ifade eder ve tartisir.",
            "reading": "Etik ikilem senaryolarini okur, kararlari ve sonuclarini analiz eder.",
            "writing": "Bir etik ikilem hakkinda lehte ve aleyhte goruslerini yazar.",
        },
        "linked_content": {
            "categories": ["Etik", "Tartisma"],
            "songs": [],
            "games": ["Ikilem Kartlari", "Munazara"],
            "dialogues": ["What Would You Do?"],
            "readings": ["Ethical Dilemmas for Teens"],
            "writings": ["My Opinion on an Ethical Issue"],
            "grammar": ["2nd Conditional: If I were... I would... + on one hand / on the other hand"],
            "phonics": ["Emphasis and stress in arguments"],
            "listening": ["Etik Ikilem Tartismasi"],
        },
        "days": {
            "mon": ["Ana Ders: Etik Ikilemler temel kelimelerini tanitim (dilemma/consequence/decision) + yapi sunumu: On one hand... on the other hand... What would you do if...?", "Beceri Lab: Dinleme — 'Etik Ikilemler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — 2nd Conditional: If I were... I would... + on one hand / on the other hand yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Etik Ikilemler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Etik Ikilemler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Etik Ikilemler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (justify/argue/perspective) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Etik Ikilemler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Etik Ikilemler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir etik ikilem hakkinda 2nd Conditional kullanarak lehte/aleyhte goruslerini sunabilir.",
    },
    {
        "week": 12,
        "theme": "Technology & Responsibility",
        "theme_tr": "Teknoloji ve Sorumluluk",
        "vocab": ["artificial intelligence", "privacy", "data", "security", "hack", "cyber", "algorithm",
                  "automation", "robot", "ethical", "responsible", "regulate", "impact", "benefit", "risk"],
        "structure": "Technology should be used responsibly. AI has both benefits and risks. We must consider the impact of...",
        "skills": {
            "listening": "Teknoloji ve sorumluluk konulu paneli dinler, argumalari degerlendirir.",
            "speaking": "Teknolojinin olumlu ve olumsuz etkilerini tartisir.",
            "reading": "Yapay zeka etigi hakkinda bir makaleyi okur, ana argumanlari cikarir.",
            "writing": "Teknolojinin sorumlu kullanimi hakkinda goruslerini iceren bir makale yazar.",
        },
        "linked_content": {
            "categories": ["Teknoloji", "Etik"],
            "songs": [],
            "games": ["Teknoloji Tartisma Kartlari", "Fayda-Risk Analizi"],
            "dialogues": ["Should AI Be Regulated?"],
            "readings": ["The Ethics of Technology"],
            "writings": ["Responsible Use of Technology"],
            "grammar": ["should / must / have to for obligation + both...and / neither...nor"],
            "phonics": ["Stress in technology vocabulary"],
            "listening": ["Teknoloji Paneli"],
        },
        "days": {
            "mon": ["Ana Ders: Teknoloji ve Sorumluluk temel kelimelerini tanitim (artificial intelligence/privacy/data) + yapi sunumu: Technology should be used responsibly.", "Beceri Lab: Dinleme — 'Teknoloji ve Sorumluluk' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — should / must / have to for obligation + both...and / neither...nor yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Teknoloji ve Sorumluluk konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Teknoloji ve Sorumluluk' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Teknoloji ve Sorumluluk konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (security/hack/algorithm) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Teknoloji ve Sorumluluk temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Teknoloji ve Sorumluluk konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Teknolojinin fayda ve risklerini tartisabilir, sorumlu kullanim hakkinda goruslerini yazabilir.",
    },
    # ===== UNITE 4: Digital Storytelling (Hafta 13-16) =====
    {
        "week": 13,
        "theme": "Digital Storytelling",
        "theme_tr": "Dijital Hikaye Anlaticiligi",
        "vocab": ["digital story", "narrative", "plot", "character", "setting", "conflict", "resolution",
                  "storyboard", "script", "scene", "voiceover", "animation", "multimedia", "audience", "creative"],
        "structure": "The story takes place in... The main character is... First... Then... Finally...",
        "skills": {
            "listening": "Dijital bir hikayeyi dinler/izler, olay orgusunu ve karakterleri saptar.",
            "speaking": "Bir hikayenin olay orgusunu sirasyla anlatir.",
            "reading": "Kisa bir hikayeyi okur, hikaye unsurlarini (karakter, mekan, catisma) belirler.",
            "writing": "Bir dijital hikaye icin senaryo taslagi (storyboard) olusturur.",
        },
        "linked_content": {
            "categories": ["Hikaye", "Dijital"],
            "songs": [],
            "games": ["Hikaye Siralama", "Karakter Olusturma"],
            "dialogues": ["Planning a Digital Story"],
            "readings": ["Elements of a Good Story"],
            "writings": ["My Digital Story Plan"],
            "grammar": ["Narrative tenses: Past Simple + Past Continuous + sequencers (first/then/finally)"],
            "phonics": ["Dramatic intonation in storytelling"],
            "listening": ["Dijital Hikaye Ornegi"],
        },
        "days": {
            "mon": ["Ana Ders: Dijital Hikaye Anlaticiligi temel kelimelerini tanitim (digital story/narrative/plot) + yapi sunumu: The story takes place in... The main character is...", "Beceri Lab: Dinleme — 'Dijital Hikaye Anlaticiligi' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Narrative tenses: Past Simple + Past Continuous + sequencers yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dijital Hikaye Anlaticiligi konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dijital Hikaye Anlaticiligi' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dijital Hikaye Anlaticiligi konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (character/setting/conflict) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dijital Hikaye Anlaticiligi temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dijital Hikaye Anlaticiligi konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir hikayenin unsurlarini belirleyebilir ve storyboard olusturabilir.",
    },
    {
        "week": 14,
        "theme": "Creating Content",
        "theme_tr": "Icerik Olusturma",
        "vocab": ["content", "blog", "vlog", "podcast", "edit", "record", "upload", "publish",
                  "subscribe", "follower", "viewer", "thumbnail", "caption", "hashtag", "platform"],
        "structure": "I have been working on... The video was edited by... You need to... in order to...",
        "skills": {
            "listening": "Bir icerik ureticisinin deneyimlerini dinler, asamalari saptar.",
            "speaking": "Dijital icerik uretme surecini adim adim anlatir.",
            "reading": "Basarili bir icerik ureticisinin hikayesini okur.",
            "writing": "Kendi blog/vlog fikri icin bir plan yazar.",
        },
        "linked_content": {
            "categories": ["Dijital", "Medya"],
            "songs": [],
            "games": ["Icerik Planlama", "Platform Eslestir"],
            "dialogues": ["How to Start a Blog"],
            "readings": ["Life of a Content Creator"],
            "writings": ["My Content Plan"],
            "grammar": ["Present Perfect Continuous: have been working on + in order to + infinitive"],
            "phonics": ["Rhythm in English sentences"],
            "listening": ["Icerik Ureticisi Roportaji"],
        },
        "days": {
            "mon": ["Ana Ders: Icerik Olusturma temel kelimelerini tanitim (content/blog/vlog) + yapi sunumu: I have been working on... You need to... in order to...", "Beceri Lab: Dinleme — 'Icerik Olusturma' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect Continuous: have been working on + in order to + infinitive yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Icerik Olusturma konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Icerik Olusturma' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Icerik Olusturma konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (edit/record/upload) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Icerik Olusturma temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Icerik Olusturma konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Dijital icerik uretme surecini aciklayabilir ve bir icerik plani olusturabilir.",
    },
    {
        "week": 15,
        "theme": "Visual Narratives",
        "theme_tr": "Gorsel Anlatimlar",
        "vocab": ["comic strip", "graphic novel", "panel", "speech bubble", "thought bubble", "caption",
                  "illustration", "frame", "sequence", "visual", "symbol", "icon", "infographic", "meme", "collage"],
        "structure": "In the first panel... The character says... This image represents... The message behind this is...",
        "skills": {
            "listening": "Gorsel anlatim teknikleri hakkindaki sunumu dinler.",
            "speaking": "Bir cizgi roman/grafik roman sahnesini anlama dayali olarak anlatir.",
            "reading": "Kisa bir cizgi roman okur, gorsel ve metin unsurlarini analiz eder.",
            "writing": "4-6 karede kendi gorsel hikayesini planlar ve diyaloglarini yazar.",
        },
        "linked_content": {
            "categories": ["Hikaye", "Sanat"],
            "songs": [],
            "games": ["Cizgi Roman Siralama", "Konusma Balonu Doldur"],
            "dialogues": ["Describing a Comic Strip"],
            "readings": ["The Art of Visual Storytelling"],
            "writings": ["My Comic Strip"],
            "grammar": ["Direct speech in speech bubbles + Present Simple for descriptions"],
            "phonics": ["Expressive reading: onomatopoeia"],
            "listening": ["Gorsel Anlatim Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Gorsel Anlatimlar temel kelimelerini tanitim (comic strip/graphic novel/panel) + yapi sunumu: In the first panel... The character says...", "Beceri Lab: Dinleme — 'Gorsel Anlatimlar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Direct speech in speech bubbles + Present Simple for descriptions yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Gorsel Anlatimlar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Gorsel Anlatimlar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Gorsel Anlatimlar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (speech bubble/thought bubble/caption) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Gorsel Anlatimlar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Gorsel Anlatimlar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Gorsel anlatim unsurlarini analiz edebilir ve kendi cizgi romanini olusturabilir.",
    },
    {
        "week": 16,
        "theme": "Presenting Digital Projects",
        "theme_tr": "Dijital Proje Sunumu",
        "vocab": ["presentation", "slide", "template", "transition", "bullet point", "highlight", "summarise",
                  "conclude", "Q&A", "feedback", "rehearse", "engage", "visual aid", "key point", "handout"],
        "structure": "I'd like to start by... Moving on to... To sum up... Are there any questions?",
        "skills": {
            "listening": "Bir dijital proje sunumunu dinler, yapisi ve tekniklerini degerlendirir.",
            "speaking": "Dijital projesini sinifa sunar, soru-cevap kismi yonetir.",
            "reading": "Etkili sunum teknikleri hakkinda bir rehber okur.",
            "writing": "Sunumunun ozetini ve yansitma (reflection) yazisi yazar.",
        },
        "linked_content": {
            "categories": ["Sunum", "Dijital"],
            "songs": [],
            "games": ["Sunum Degerlendirme", "Dogaclama Sunum"],
            "dialogues": ["Giving a Great Presentation"],
            "readings": ["Tips for Effective Presentations"],
            "writings": ["My Presentation Reflection"],
            "grammar": ["Formal discourse markers: I'd like to / Moving on to / To sum up"],
            "phonics": ["Public speaking: pace and pausing"],
            "listening": ["Dijital Proje Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Dijital Proje Sunumu temel kelimelerini tanitim (presentation/slide/template) + yapi sunumu: I'd like to start by... Moving on to... To sum up...", "Beceri Lab: Dinleme — 'Dijital Proje Sunumu' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Formal discourse markers: I'd like to / Moving on to / To sum up yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dijital Proje Sunumu konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dijital Proje Sunumu' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dijital Proje Sunumu konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (transition/bullet point/highlight) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dijital Proje Sunumu temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dijital Proje Sunumu konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Dijital projesini etkili bir sekilde sunabilir ve soru-cevap yonetebilir.",
    },
    # ===== UNITE 5: Nature & Geography (Hafta 17-20) =====
    {
        "week": 17,
        "theme": "Nature & Geography",
        "theme_tr": "Doga ve Cografya",
        "vocab": ["continent", "ocean", "mountain range", "desert", "rainforest", "glacier", "volcano",
                  "earthquake", "climate", "ecosystem", "biodiversity", "habitat", "landscape", "terrain", "peninsula"],
        "structure": "Turkey is located in... It is surrounded by... The climate varies from... compared to...",
        "skills": {
            "listening": "Cografi ozellikler hakkindaki belgeseli dinler, yerleri haritada isaretler.",
            "speaking": "Turkiye'nin cografi ozelliklerini diger ulkelerle karsilastirarak anlatir.",
            "reading": "Farkli cografi bolgeleri anlatan metni okur, karsilastirma tablosu olusturur.",
            "writing": "Bir ulkenin cografi ozelliklerini anlatan bir yazi yazar (10-12 cumle).",
        },
        "linked_content": {
            "categories": ["Doga", "Cografya"],
            "songs": ["Wonders of Nature"],
            "games": ["Cografya Bilgi Yarismasi", "Harita Eslestir"],
            "dialogues": ["Describing Geographical Features"],
            "readings": ["Geographical Wonders"],
            "writings": ["The Geography of My Country"],
            "grammar": ["Passive: is located / is surrounded + comparatives & superlatives"],
            "phonics": ["Pronunciation of geographical terms"],
            "listening": ["Cografi Belgesel"],
        },
        "days": {
            "mon": ["Ana Ders: Doga ve Cografya temel kelimelerini tanitim (continent/ocean/mountain range) + yapi sunumu: Turkey is located in... It is surrounded by...", "Beceri Lab: Dinleme — 'Doga ve Cografya' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive: is located / is surrounded + comparatives & superlatives yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Doga ve Cografya konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Doga ve Cografya' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Doga ve Cografya konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (desert/rainforest/glacier) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Doga ve Cografya temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Doga ve Cografya konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir ulkenin cografi ozelliklerini karsilastirmali olarak anlatabilir.",
    },
    {
        "week": 18,
        "theme": "Natural Disasters",
        "theme_tr": "Dogal Afetler",
        "vocab": ["earthquake", "flood", "tsunami", "hurricane", "drought", "wildfire", "avalanche",
                  "landslide", "evacuate", "shelter", "rescue", "emergency", "damage", "survivor", "relief"],
        "structure": "The earthquake struck at... Thousands of people were evacuated. If an earthquake happens, you should...",
        "skills": {
            "listening": "Dogal afet haber bulteni dinler, olaylarin kronolojisini cikarir.",
            "speaking": "Dogal afet durumunda yapilmasi gerekenleri anlatir.",
            "reading": "Bir dogal afet hakkinda haber metnini okur, istatistikleri yorumlar.",
            "writing": "Bir dogal afeti ve etkilerini anlatan haber metni yazar.",
        },
        "linked_content": {
            "categories": ["Doga", "Afet"],
            "songs": [],
            "games": ["Afet Hazirlik Kontrol Listesi", "Acil Durum Senaryolari"],
            "dialogues": ["What to Do in an Emergency"],
            "readings": ["Natural Disasters Around the World"],
            "writings": ["A News Report on a Natural Disaster"],
            "grammar": ["Past Simple Passive: were evacuated / was destroyed + 1st Conditional for advice"],
            "phonics": ["Stress in emergency commands"],
            "listening": ["Afet Haber Bulteni"],
        },
        "days": {
            "mon": ["Ana Ders: Dogal Afetler temel kelimelerini tanitim (earthquake/flood/tsunami) + yapi sunumu: The earthquake struck at... Thousands of people were evacuated.", "Beceri Lab: Dinleme — 'Dogal Afetler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Past Simple Passive: were evacuated / was destroyed + 1st Conditional for advice yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dogal Afetler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dogal Afetler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dogal Afetler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (hurricane/drought/wildfire) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dogal Afetler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dogal Afetler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Dogal afetleri ve etkilerini Passive Voice ile anlatan haber metni yazabilir.",
    },
    # ===== DONEM 2 (Hafta 19-36) =====
    {
        "week": 19,
        "theme": "Environmental Issues",
        "theme_tr": "Cevre Sorunlari",
        "vocab": ["pollution", "deforestation", "global warming", "carbon footprint", "greenhouse gas",
                  "ozone layer", "endangered species", "recycling", "renewable energy", "sustainable",
                  "conservation", "waste", "emission", "fossil fuel", "ecological"],
        "structure": "If we don't stop polluting, the Earth will... We should reduce our carbon footprint by... Unless we act now...",
        "skills": {
            "listening": "Cevre sorunlari hakkindaki belgeseli dinler, sorunlari ve cozumleri saptar.",
            "speaking": "Cevre sorunlarini tartisir ve cozum onerileri sunar.",
            "reading": "Kuresel isinma hakkinda makale okur, neden-sonuc iliskilerini cikarir.",
            "writing": "Bir cevre sorunu ve cozum onerisini iceren makale yazar.",
        },
        "linked_content": {
            "categories": ["Cevre", "Doga"],
            "songs": ["Save Our Planet"],
            "games": ["Cevre Bilgi Yarismasi", "Karbon Ayak Izi Hesapla"],
            "dialogues": ["How Can We Help the Environment?"],
            "readings": ["Climate Change: Facts and Solutions"],
            "writings": ["An Environmental Problem and Its Solution"],
            "grammar": ["1st Conditional: If we don't... will... + Unless + gerunds after prepositions"],
            "phonics": ["Pronunciation of environmental vocabulary"],
            "listening": ["Cevre Belgeseli"],
        },
        "days": {
            "mon": ["Ana Ders: Cevre Sorunlari temel kelimelerini tanitim (pollution/deforestation/global warming) + yapi sunumu: If we don't stop polluting, the Earth will...", "Beceri Lab: Dinleme — 'Cevre Sorunlari' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — 1st Conditional: If we don't... will... + Unless + gerunds after prepositions yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Cevre Sorunlari konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Cevre Sorunlari' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Cevre Sorunlari konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (carbon footprint/greenhouse gas/ozone layer) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Cevre Sorunlari temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Cevre Sorunlari konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Cevre sorunlarini neden-sonuc iliskisiyle aciklayabilir ve cozum onerebilir.",
    },
    {
        "week": 20,
        "theme": "Wildlife Conservation",
        "theme_tr": "Yaban Hayati Koruma",
        "vocab": ["wildlife", "conservation", "endangered", "extinct", "habitat loss", "poaching", "sanctuary",
                  "breed", "migrate", "prey", "predator", "food chain", "ecosystem", "protect", "awareness"],
        "structure": "Many species are endangered because of... If we protect their habitats, they will... It is essential that we...",
        "skills": {
            "listening": "Yaban hayati koruma projesi hakkindaki sunumu dinler, stratejileri saptar.",
            "speaking": "Nesli tukenmekte olan bir hayvan hakkinda bilgi verir ve koruma onerileri sunar.",
            "reading": "Yaban hayati koruma hakkinda makale okur, tehditleri ve cozumleri listeler.",
            "writing": "Nesli tukenmekte olan bir hayvan icin koruma kampanya metni yazar.",
        },
        "linked_content": {
            "categories": ["Doga", "Cevre"],
            "songs": [],
            "games": ["Yaban Hayati Hafiza Oyunu", "Besin Zinciri Eslestir"],
            "dialogues": ["Protecting Endangered Species"],
            "readings": ["Saving Wildlife"],
            "writings": ["Save the...! Campaign"],
            "grammar": ["It is essential that... + Passive: are endangered / are protected"],
            "phonics": ["Silent letters in nature words"],
            "listening": ["Yaban Hayati Koruma Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Yaban Hayati Koruma temel kelimelerini tanitim (wildlife/conservation/endangered) + yapi sunumu: Many species are endangered because of...", "Beceri Lab: Dinleme — 'Yaban Hayati Koruma' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — It is essential that... + Passive: are endangered / are protected yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yaban Hayati Koruma konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yaban Hayati Koruma' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yaban Hayati Koruma konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (extinct/habitat loss/poaching) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yaban Hayati Koruma temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yaban Hayati Koruma konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Nesli tukenmekte olan turlerin korunmasi icin kampanya metni yazabilir.",
    },
    # ===== UNITE 6: Social Media (Hafta 21-24) =====
    {
        "week": 21,
        "theme": "Social Media",
        "theme_tr": "Sosyal Medya",
        "vocab": ["social media", "account", "profile", "post", "share", "like", "comment", "follow",
                  "influencer", "trend", "viral", "notification", "privacy settings", "screen time", "digital footprint"],
        "structure": "Social media is used for... I spend... hours a day on... It has both advantages and disadvantages.",
        "skills": {
            "listening": "Sosyal medya kullanim aliskanliklari hakkindaki anketi dinler, verileri saptar.",
            "speaking": "Sosyal medya kullanim aliskanliklarini ve goruslerini paylasir.",
            "reading": "Sosyal medyanin gencler uzerindeki etkisini anlatan makaleyi okur.",
            "writing": "Sosyal medyanin avantaj ve dezavantajlarini karsilastiran bir makale yazar.",
        },
        "linked_content": {
            "categories": ["Sosyal Medya", "Teknoloji"],
            "songs": [],
            "games": ["Sosyal Medya Bilgi Testi", "Avantaj-Dezavantaj Siralama"],
            "dialogues": ["How Do You Use Social Media?"],
            "readings": ["Social Media and Teenagers"],
            "writings": ["Pros and Cons of Social Media"],
            "grammar": ["Passive: is used for + spend + time + -ing + advantages/disadvantages structure"],
            "phonics": ["Fast speech: gonna/wanna/gotta"],
            "listening": ["Sosyal Medya Anketi"],
        },
        "days": {
            "mon": ["Ana Ders: Sosyal Medya temel kelimelerini tanitim (social media/account/profile) + yapi sunumu: Social media is used for... I spend... hours a day on...", "Beceri Lab: Dinleme — 'Sosyal Medya' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive: is used for + spend + time + -ing + advantages/disadvantages structure yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Sosyal Medya konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Sosyal Medya' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Sosyal Medya konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (share/like/comment) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Sosyal Medya temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Sosyal Medya konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sosyal medyanin avantaj ve dezavantajlarini karsilastirmali olarak yazabilir.",
    },
    {
        "week": 22,
        "theme": "Online Safety",
        "theme_tr": "Cevrimici Guvenlik",
        "vocab": ["cyberbullying", "phishing", "scam", "password", "identity theft", "privacy", "report",
                  "block", "suspicious", "verify", "personal information", "stranger", "screenshot", "evidence", "awareness"],
        "structure": "You should never share your password with... If someone bullies you online, you must... It's important to...",
        "skills": {
            "listening": "Cevrimici guvenlik hakkindaki egitim videosunu dinler, kurallari listeler.",
            "speaking": "Cevrimici guvenlik kurallarini aciklar ve tavsiyeler verir.",
            "reading": "Siber zorbalik hakkinda bir vakay okur, cozum yollarini tartisir.",
            "writing": "Cevrimici guvenlik posteri icin slogan ve aciklama yazilari yazar.",
        },
        "linked_content": {
            "categories": ["Guvenlik", "Teknoloji"],
            "songs": [],
            "games": ["Guvenlik Kontrol Listesi", "Dolandiricilik Tespit"],
            "dialogues": ["Staying Safe Online"],
            "readings": ["A Cyberbullying Case Study"],
            "writings": ["Online Safety Poster"],
            "grammar": ["should never / must + It's important to + reported speech intro"],
            "phonics": ["Word stress in compound nouns"],
            "listening": ["Cevrimici Guvenlik Egitimi"],
        },
        "days": {
            "mon": ["Ana Ders: Cevrimici Guvenlik temel kelimelerini tanitim (cyberbullying/phishing/scam) + yapi sunumu: You should never share your password with...", "Beceri Lab: Dinleme — 'Cevrimici Guvenlik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — should never / must + It's important to + reported speech intro yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Cevrimici Guvenlik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Cevrimici Guvenlik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Cevrimici Guvenlik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (password/identity theft/privacy) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Cevrimici Guvenlik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Cevrimici Guvenlik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Cevrimici guvenlik kurallarini aciklayabilir ve guvenlik posteri olusturabilir.",
    },
    {
        "week": 23,
        "theme": "Digital Citizenship",
        "theme_tr": "Dijital Vatandaslik",
        "vocab": ["digital citizen", "responsible", "respect", "copyright", "plagiarism", "credible",
                  "source", "fact-check", "fake news", "misinformation", "media literacy", "critical", "ethical", "reliable", "bias"],
        "structure": "A responsible digital citizen should... We need to check whether the information is... It is claimed that...",
        "skills": {
            "listening": "Medya okuryazarligi hakkindaki konusmayi dinler, stratejileri saptar.",
            "speaking": "Sahte haberleri nasil tespit edecegini aciklar.",
            "reading": "Gercek ve sahte haber orneklerini karsilastirarak okur.",
            "writing": "Dijital vatandaslik kurallari hakkinda bir rehber yazar.",
        },
        "linked_content": {
            "categories": ["Dijital", "Medya"],
            "songs": [],
            "games": ["Gercek mi Sahte mi?", "Kaynak Degerlendirme"],
            "dialogues": ["Is This News Real or Fake?"],
            "readings": ["How to Spot Fake News"],
            "writings": ["A Guide to Digital Citizenship"],
            "grammar": ["Reported speech: It is claimed/reported that... + whether/if clauses"],
            "phonics": ["Sentence stress for emphasis"],
            "listening": ["Medya Okuryazarligi Konusmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Dijital Vatandaslik temel kelimelerini tanitim (digital citizen/responsible/copyright) + yapi sunumu: A responsible digital citizen should...", "Beceri Lab: Dinleme — 'Dijital Vatandaslik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Reported speech: It is claimed/reported that... + whether/if clauses yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Dijital Vatandaslik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Dijital Vatandaslik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Dijital Vatandaslik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (plagiarism/credible/fact-check) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Dijital Vatandaslik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Dijital Vatandaslik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sahte haberleri tespit edebilir ve dijital vatandaslik rehberi yazabilir.",
    },
    {
        "week": 24,
        "theme": "Social Media Projects",
        "theme_tr": "Sosyal Medya Projeleri",
        "vocab": ["campaign", "awareness", "challenge", "hashtag campaign", "donation", "volunteer",
                  "cause", "impact", "reach", "engage", "collaborate", "crowdfunding", "petition", "movement", "initiative"],
        "structure": "Our campaign aims to... We have been raising awareness about... So far, we have reached...",
        "skills": {
            "listening": "Basarili sosyal medya kampanyalarini anlatan sunumu dinler.",
            "speaking": "Kendi sosyal medya kampanya fikrini sunar ve hedeflerini aciklar.",
            "reading": "Sosyal medya uzerinden basarili olmus kampanyalari okur.",
            "writing": "Bir sosyal medya kampanyasi plani ve tanitim metni yazar.",
        },
        "linked_content": {
            "categories": ["Sosyal Medya", "Proje"],
            "songs": [],
            "games": ["Kampanya Planlama", "Etki Degerlendirme"],
            "dialogues": ["Planning a Social Media Campaign"],
            "readings": ["Successful Social Media Campaigns"],
            "writings": ["My Social Media Campaign Plan"],
            "grammar": ["Present Perfect: have been raising / have reached + aims to + infinitive"],
            "phonics": ["Persuasive speech techniques"],
            "listening": ["Sosyal Medya Kampanyasi Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Sosyal Medya Projeleri temel kelimelerini tanitim (campaign/awareness/challenge) + yapi sunumu: Our campaign aims to... We have been raising awareness about...", "Beceri Lab: Dinleme — 'Sosyal Medya Projeleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect: have been raising / have reached + aims to + infinitive yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Sosyal Medya Projeleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Sosyal Medya Projeleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Sosyal Medya Projeleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (donation/volunteer/cause) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Sosyal Medya Projeleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Sosyal Medya Projeleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Sosyal medya kampanyasi planlayabilir ve tanitim metni yazabilir.",
    },
    # ===== UNITE 7: History & Heroes (Hafta 25-27) =====
    {
        "week": 25,
        "theme": "History & Heroes",
        "theme_tr": "Tarih ve Kahramanlar",
        "vocab": ["hero", "heroine", "battle", "independence", "revolution", "empire", "republic",
                  "leader", "sacrifice", "freedom", "patriot", "monument", "memorial", "era", "founding"],
        "structure": "Ataturk founded the Republic of Turkey in 1923. He was known as... The battle was fought in...",
        "skills": {
            "listening": "Tarihi bir olayun anlatimini dinler, kronolojik siralama yapar.",
            "speaking": "Bir tarihi kahramani tanitir, basarilarini ve mirasini anlatir.",
            "reading": "Turkiye Cumhuriyeti'nin kurulusunu anlatan metni okur.",
            "writing": "Bir tarihi kahramanin biyografisini yazar (12-14 cumle).",
        },
        "linked_content": {
            "categories": ["Tarih", "Kahramanlar"],
            "songs": [],
            "games": ["Tarih Zaman Cizelgesi", "Kahraman Eslestir"],
            "dialogues": ["Talking About Historical Heroes"],
            "readings": ["The Founding of the Republic"],
            "writings": ["A Hero in History"],
            "grammar": ["Past Simple Passive: was founded / was fought + Past Perfect intro: had already..."],
            "phonics": ["Pronunciation of historical dates and names"],
            "listening": ["Tarihi Olay Anlatimi"],
        },
        "days": {
            "mon": ["Ana Ders: Tarih ve Kahramanlar temel kelimelerini tanitim (hero/heroine/battle) + yapi sunumu: Ataturk founded the Republic of Turkey in 1923.", "Beceri Lab: Dinleme — 'Tarih ve Kahramanlar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Past Simple Passive: was founded / was fought + Past Perfect intro yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Tarih ve Kahramanlar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Tarih ve Kahramanlar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Tarih ve Kahramanlar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (independence/revolution/empire) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Tarih ve Kahramanlar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Tarih ve Kahramanlar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Tarihi bir kahramanin biyografisini Past Passive ve Past Perfect kullanarak yazabilir.",
    },
    {
        "week": 26,
        "theme": "Everyday Heroes",
        "theme_tr": "Gunluk Kahramanlar",
        "vocab": ["firefighter", "paramedic", "volunteer", "charity", "selfless", "brave", "courageous",
                  "dedication", "serve", "community", "first responder", "humanitarian", "rescue", "gratitude", "unsung hero"],
        "structure": "She has been helping people for... He risked his life to... These people deserve to be recognised because...",
        "skills": {
            "listening": "Gunluk kahramanlarin hikayelerini dinler, ortak ozelliklerini saptar.",
            "speaking": "Tanidigi bir gunluk kahramani tanitir ve neden kahraman oldugunu aciklar.",
            "reading": "Farkli mesleklerden gunluk kahramanlari anlatan metinleri okur.",
            "writing": "Tanidigi bir gunluk kahramani anlatan bir yazi yazar.",
        },
        "linked_content": {
            "categories": ["Kahramanlar", "Toplum"],
            "songs": ["Everyday Heroes Song"],
            "games": ["Kahraman Meslek Eslestir", "Hikaye Tamamla"],
            "dialogues": ["Who Are Everyday Heroes?"],
            "readings": ["Unsung Heroes Around Us"],
            "writings": ["An Everyday Hero I Know"],
            "grammar": ["Present Perfect Continuous: has been helping + deserve to be + past participle"],
            "phonics": ["Emotional tone in speech"],
            "listening": ["Gunluk Kahraman Hikayeleri"],
        },
        "days": {
            "mon": ["Ana Ders: Gunluk Kahramanlar temel kelimelerini tanitim (firefighter/paramedic/volunteer) + yapi sunumu: She has been helping people for... He risked his life to...", "Beceri Lab: Dinleme — 'Gunluk Kahramanlar' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect Continuous: has been helping + deserve to be + past participle yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Gunluk Kahramanlar konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Gunluk Kahramanlar' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Gunluk Kahramanlar konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (selfless/brave/courageous) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Gunluk Kahramanlar temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Gunluk Kahramanlar konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Tanidigi bir gunluk kahramani Present Perfect Continuous ile anlatabilir.",
    },
    {
        "week": 27,
        "theme": "Legacy & Memory",
        "theme_tr": "Miras ve Hafiza",
        "vocab": ["legacy", "memory", "heritage", "preserve", "commemorate", "ancestor", "descendant",
                  "archive", "artefact", "museum", "documentary", "oral history", "tradition", "cultural heritage", "identity"],
        "structure": "This monument was built to commemorate... Our heritage should be preserved for... It has been a tradition since...",
        "skills": {
            "listening": "Kulturel miras koruma projesi hakkindaki belgeseli dinler.",
            "speaking": "Kulturel mirasin korunmasinin onemini tartisir.",
            "reading": "Bir kulturel miras alani hakkinda makale okur.",
            "writing": "Kendi bolgesindeki bir kulturel miras unsurunu tanitan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Tarih", "Kultur"],
            "songs": [],
            "games": ["Miras Eslestir", "Zaman Kapsulu"],
            "dialogues": ["Why Is Heritage Important?"],
            "readings": ["Preserving Our Heritage"],
            "writings": ["A Cultural Heritage Site"],
            "grammar": ["Passive Perfect: has been preserved / was built to + should be + past participle"],
            "phonics": ["Pronunciation of heritage vocabulary"],
            "listening": ["Kulturel Miras Belgeseli"],
        },
        "days": {
            "mon": ["Ana Ders: Miras ve Hafiza temel kelimelerini tanitim (legacy/memory/heritage) + yapi sunumu: This monument was built to commemorate... Our heritage should be preserved for...", "Beceri Lab: Dinleme — 'Miras ve Hafiza' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Passive Perfect: has been preserved / was built to + should be + past participle yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Miras ve Hafiza konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Miras ve Hafiza' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Miras ve Hafiza konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (preserve/commemorate/ancestor) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Miras ve Hafiza temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Miras ve Hafiza konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kulturel miras unsurlarini tanitan ve korunma onemini aciklayan yazi yazabilir.",
    },
    # ===== UNITE 8: Narrative & Stories (Hafta 28-30) =====
    {
        "week": 28,
        "theme": "Narrative & Stories",
        "theme_tr": "Anlatim ve Hikayeler",
        "vocab": ["narrator", "protagonist", "antagonist", "climax", "suspense", "twist", "moral",
                  "fiction", "non-fiction", "genre", "fairy tale", "legend", "myth", "fable", "folklore"],
        "structure": "Once upon a time... The story is set in... The moral of the story is... It turned out that...",
        "skills": {
            "listening": "Bir halk hikayesini dinler, hikaye unsurlarini (baslangic, gelisme, doruk, sonuc) saptar.",
            "speaking": "Bildigi bir hikayeyi hikaye anlatim teknikleri kullanarak anlatir.",
            "reading": "Farkli turlerden kisa hikayeleri okur, turlerini ve ozelliklerini karsilastirir.",
            "writing": "Bir kisa hikaye yazar, tum hikaye unsurlarini icerir (14-16 cumle).",
        },
        "linked_content": {
            "categories": ["Hikaye", "Edebiyat"],
            "songs": [],
            "games": ["Hikaye Kupu", "Tur Eslestir"],
            "dialogues": ["Retelling a Story"],
            "readings": ["Stories from Around the World"],
            "writings": ["My Short Story"],
            "grammar": ["Past Perfect: had already / had never + narrative tenses review"],
            "phonics": ["Dramatic pause and intonation"],
            "listening": ["Halk Hikayesi Dinleme"],
        },
        "days": {
            "mon": ["Ana Ders: Anlatim ve Hikayeler temel kelimelerini tanitim (narrator/protagonist/antagonist) + yapi sunumu: Once upon a time... The story is set in...", "Beceri Lab: Dinleme — 'Anlatim ve Hikayeler' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Past Perfect: had already / had never + narrative tenses review yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Anlatim ve Hikayeler konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Anlatim ve Hikayeler' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Anlatim ve Hikayeler konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (climax/suspense/twist) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Anlatim ve Hikayeler temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Anlatim ve Hikayeler konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Hikaye unsurlarini belirleyebilir ve Past Perfect kullanarak kisa hikaye yazabilir.",
    },
    {
        "week": 29,
        "theme": "Book Reviews",
        "theme_tr": "Kitap Incelemeleri",
        "vocab": ["review", "recommend", "plot summary", "character development", "theme", "setting",
                  "author", "chapter", "page-turner", "bestseller", "rating", "spoiler", "bookworm", "edition", "series"],
        "structure": "I would recommend this book because... The author describes... In my opinion, the best part was...",
        "skills": {
            "listening": "Kitap incelemesi podcast'ini dinler, kitabin ozelliklerini saptar.",
            "speaking": "Okudugu bir kitabi tanitir ve neden tavsiye ettigini aciklar.",
            "reading": "Bir kitap incelemesi okur, yazarin goruslerini ve argumanlarini analiz eder.",
            "writing": "Okudugu bir kitabin incelemesini yazar (12-14 cumle).",
        },
        "linked_content": {
            "categories": ["Edebiyat", "Inceleme"],
            "songs": [],
            "games": ["Kitap Bilgi Yarismasi", "Kitap-Yazar Eslestir"],
            "dialogues": ["Have You Read Any Good Books?"],
            "readings": ["Book Review Examples"],
            "writings": ["My Book Review"],
            "grammar": ["I would recommend... because + reported speech: The author says/describes..."],
            "phonics": ["Reading aloud with expression"],
            "listening": ["Kitap Incelemesi Podcast"],
        },
        "days": {
            "mon": ["Ana Ders: Kitap Incelemeleri temel kelimelerini tanitim (review/recommend/plot summary) + yapi sunumu: I would recommend this book because... The author describes...", "Beceri Lab: Dinleme — 'Kitap Incelemeleri' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — I would recommend... because + reported speech: The author says/describes... yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kitap Incelemeleri konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kitap Incelemeleri' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kitap Incelemeleri konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (character development/theme/setting) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kitap Incelemeleri temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kitap Incelemeleri konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Okudugu bir kitabin incelemesini argumanlariyla birlikte yazabilir.",
    },
    {
        "week": 30,
        "theme": "Creative Writing",
        "theme_tr": "Yaratici Yazarlik",
        "vocab": ["imagination", "inspiration", "draft", "revise", "edit", "proofread", "metaphor",
                  "simile", "imagery", "dialogue", "description", "flashback", "cliffhanger", "point of view", "tone"],
        "structure": "As if... It felt like... He wondered whether... Suddenly, everything changed when...",
        "skills": {
            "listening": "Bir yazarin yaratici sureci hakkindaki konusmasini dinler.",
            "speaking": "Kendi yaratici yazma surecini ve ilham kaynaklarini anlatir.",
            "reading": "Farkli edebi teknikleri iceren metin orneklerini okur ve analiz eder.",
            "writing": "Edebi teknikleri kullanarak yaratici bir metin yazar (14-16 cumle).",
        },
        "linked_content": {
            "categories": ["Edebiyat", "Yaraticilik"],
            "songs": [],
            "games": ["Hikaye Baslangici Tamamla", "Edebi Teknik Bul"],
            "dialogues": ["Where Do You Get Your Inspiration?"],
            "readings": ["Literary Techniques in Action"],
            "writings": ["My Creative Piece"],
            "grammar": ["as if + Past Simple; wondered whether + simile/metaphor usage"],
            "phonics": ["Expressive reading: pace, tone, pause"],
            "listening": ["Yazar Konusmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Yaratici Yazarlik temel kelimelerini tanitim (imagination/inspiration/draft) + yapi sunumu: As if... It felt like... Suddenly, everything changed when...", "Beceri Lab: Dinleme — 'Yaratici Yazarlik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — as if + Past Simple; wondered whether + simile/metaphor usage yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yaratici Yazarlik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yaratici Yazarlik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yaratici Yazarlik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (metaphor/simile/imagery) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yaratici Yazarlik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yaratici Yazarlik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Edebi teknikleri kullanarak yaratici bir metin yazabilir.",
    },
    # ===== UNITE 9: Global Citizenship (Hafta 31-33) =====
    {
        "week": 31,
        "theme": "Global Citizenship",
        "theme_tr": "Kuresel Vatandaslik",
        "vocab": ["global citizen", "human rights", "equality", "justice", "democracy", "poverty",
                  "refugee", "migration", "solidarity", "cooperation", "United Nations", "NGO", "aid", "sustainable development", "peace"],
        "structure": "Every person has the right to... We are responsible for... It is estimated that... million people...",
        "skills": {
            "listening": "Kuresel sorunlar hakkindaki BM sunumunu dinler, istatistikleri ve cozum onerilerini saptar.",
            "speaking": "Kuresel bir sorunu tanitir ve cozum onerileri sunar.",
            "reading": "Insan haklari beyannamesi ve kuresel sorunlar hakkinda makale okur.",
            "writing": "Kuresel bir sorun hakkinda farkindalik yazisi yazar.",
        },
        "linked_content": {
            "categories": ["Kuresel", "Toplum"],
            "songs": ["We Are the World"],
            "games": ["Kuresel Sorun Haritasi", "Haklar Eslestir"],
            "dialogues": ["What Does Global Citizenship Mean?"],
            "readings": ["Global Issues and Solutions"],
            "writings": ["Raising Awareness About a Global Issue"],
            "grammar": ["Every person has the right to + Passive: It is estimated that... + responsible for + gerund"],
            "phonics": ["Pronunciation of international organizations"],
            "listening": ["BM Sunumu"],
        },
        "days": {
            "mon": ["Ana Ders: Kuresel Vatandaslik temel kelimelerini tanitim (global citizen/human rights/equality) + yapi sunumu: Every person has the right to...", "Beceri Lab: Dinleme — 'Kuresel Vatandaslik' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Every person has the right to + Passive: It is estimated that... yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kuresel Vatandaslik konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kuresel Vatandaslik' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kuresel Vatandaslik konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (justice/democracy/poverty) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kuresel Vatandaslik temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kuresel Vatandaslik konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Kuresel bir sorun hakkinda farkindalik yazisi yazabilir ve cozum onerebilir.",
    },
    {
        "week": 32,
        "theme": "Sustainable Future",
        "theme_tr": "Surdurulebilir Gelecek",
        "vocab": ["sustainability", "renewable", "solar energy", "wind power", "electric vehicle", "recycle",
                  "reduce", "reuse", "zero waste", "organic", "carbon neutral", "green", "eco-friendly", "footprint", "innovation"],
        "structure": "By 2050, we will have... If everyone recycled, the world would... We ought to switch to...",
        "skills": {
            "listening": "Surdurulebilir gelecek hakkindaki TED konusmasini dinler.",
            "speaking": "Surdurulebilir yasam icin somut oneriler sunar ve tartisir.",
            "reading": "Surdurulebilir kalkinma hedeflerini anlatan metni okur.",
            "writing": "Surdurulebilir gelecek icin eylem plani yazar.",
        },
        "linked_content": {
            "categories": ["Cevre", "Gelecek"],
            "songs": [],
            "games": ["Karbon Ayak Izi Hesapla", "Eko Cozum Bulma"],
            "dialogues": ["How Can We Build a Sustainable Future?"],
            "readings": ["Sustainable Development Goals"],
            "writings": ["My Action Plan for a Green Future"],
            "grammar": ["Future Perfect: will have + 2nd Conditional review + ought to / had better"],
            "phonics": ["Stress in environmental compound nouns"],
            "listening": ["Surdurulebilirlik TED Konusmasi"],
        },
        "days": {
            "mon": ["Ana Ders: Surdurulebilir Gelecek temel kelimelerini tanitim (sustainability/renewable/solar energy) + yapi sunumu: By 2050, we will have... We ought to switch to...", "Beceri Lab: Dinleme — 'Surdurulebilir Gelecek' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Future Perfect: will have + 2nd Conditional review + ought to / had better yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Surdurulebilir Gelecek konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Surdurulebilir Gelecek' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Surdurulebilir Gelecek konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (wind power/electric vehicle/zero waste) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Surdurulebilir Gelecek temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Surdurulebilir Gelecek konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Surdurulebilir gelecek icin Future Perfect kullanarak eylem plani yazabilir.",
    },
    {
        "week": 33,
        "theme": "Cultural Exchange",
        "theme_tr": "Kulturel Degisim",
        "vocab": ["exchange", "host family", "abroad", "scholarship", "programme", "immersion", "adapt",
                  "homesick", "experience", "perspective", "open-minded", "cross-cultural", "ambassador", "global village", "interconnected"],
        "structure": "If I had the chance, I would... Living abroad would help me... I wish I could... It must be amazing to...",
        "skills": {
            "listening": "Degisim ogrencisinin deneyimlerini dinler, zorluklari ve kazanimlari saptar.",
            "speaking": "Yurt disinda yasama deneyimi hakkindaki goruslerini paylasir.",
            "reading": "Bir degisim programi deneyimini anlatan blog yazisini okur.",
            "writing": "Bir degisim programina basvuru motivasyon mektubu yazar.",
        },
        "linked_content": {
            "categories": ["Kultur", "Egitim"],
            "songs": [],
            "games": ["Kultur Bilgi Yarismasi", "Durum Senaryolari"],
            "dialogues": ["Studying Abroad"],
            "readings": ["My Exchange Year"],
            "writings": ["Motivation Letter for Exchange Programme"],
            "grammar": ["Wish + Past Simple; If I had... I would (2nd conditional) + must be + adjective"],
            "phonics": ["Fluency practice: natural speech rhythm"],
            "listening": ["Degisim Ogrencisi Roportaji"],
        },
        "days": {
            "mon": ["Ana Ders: Kulturel Degisim temel kelimelerini tanitim (exchange/host family/abroad) + yapi sunumu: If I had the chance, I would... I wish I could...", "Beceri Lab: Dinleme — 'Kulturel Degisim' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Wish + Past Simple; If I had... I would (2nd conditional) + must be + adjective yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Kulturel Degisim konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Kulturel Degisim' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Kulturel Degisim konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (scholarship/immersion/adapt) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Kulturel Degisim temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Kulturel Degisim konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Degisim programi motivasyon mektubu yazabilir ve kulturel degisim deneyimini tartisabilir.",
    },
    # ===== UNITE 10: Critical Thinking (Hafta 34-36) =====
    {
        "week": 34,
        "theme": "Critical Thinking",
        "theme_tr": "Elestirel Dusunme",
        "vocab": ["critical thinking", "analyse", "evaluate", "evidence", "argument", "assumption", "bias",
                  "logical", "fallacy", "perspective", "objective", "subjective", "conclude", "reasoning", "criteria"],
        "structure": "Based on the evidence... It can be concluded that... This argument is flawed because... From my perspective...",
        "skills": {
            "listening": "Bir tartisma programini dinler, argumanlarin guclu ve zayif yonlerini degerlendirir.",
            "speaking": "Bir konu hakkinda kanitlara dayali argumanlar sunar.",
            "reading": "Farkli bakis acilarindan yazilmis metinleri okur, onyargilari tespit eder.",
            "writing": "Bir konunun lehinde ve aleyhinde argumanlari iceren tartisma yazisi yazar.",
        },
        "linked_content": {
            "categories": ["Dusunme", "Tartisma"],
            "songs": [],
            "games": ["Arguman Analizi", "Mantik Bulmacalari"],
            "dialogues": ["Evaluating Arguments"],
            "readings": ["How to Think Critically"],
            "writings": ["A For-and-Against Essay"],
            "grammar": ["Based on... / It can be concluded that... + linking words: however, therefore, moreover"],
            "phonics": ["Academic English pronunciation"],
            "listening": ["Tartisma Programi"],
        },
        "days": {
            "mon": ["Ana Ders: Elestirel Dusunme temel kelimelerini tanitim (critical thinking/analyse/evaluate) + yapi sunumu: Based on the evidence... It can be concluded that...", "Beceri Lab: Dinleme — 'Elestirel Dusunme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Based on... / It can be concluded that... + linking words yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Elestirel Dusunme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Elestirel Dusunme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Elestirel Dusunme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (evidence/argument/assumption) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Elestirel Dusunme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Elestirel Dusunme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Argumanlari kanitlara dayali olarak degerlendirebilir ve tartisma yazisi yazabilir.",
    },
    {
        "week": 35,
        "theme": "Problem Solving",
        "theme_tr": "Problem Cozme",
        "vocab": ["problem", "solution", "brainstorm", "strategy", "approach", "alternative", "implement",
                  "outcome", "trial and error", "collaborate", "innovative", "effective", "efficient", "prioritise", "systematic"],
        "structure": "The main problem is... One possible solution would be... If we implemented this strategy, we could...",
        "skills": {
            "listening": "Problem cozme sureci hakkindaki vaka calismasini dinler.",
            "speaking": "Bir problemi analiz eder ve sistematik cozum onerileri sunar.",
            "reading": "Farkli problem cozme yaklasimlarini anlatan metni okur.",
            "writing": "Bir problemi ve cozum onerilerini adim adim aciklayan yazi yazar.",
        },
        "linked_content": {
            "categories": ["Dusunme", "Proje"],
            "songs": [],
            "games": ["Beyin Firtinasi", "Cozum Haritasi"],
            "dialogues": ["How Would You Solve This Problem?"],
            "readings": ["Problem-Solving Strategies"],
            "writings": ["Problem and Solution Essay"],
            "grammar": ["One possible solution would be + 2nd Conditional: If we implemented... + could/would"],
            "phonics": ["Hedging language intonation"],
            "listening": ["Problem Cozme Vaka Calismasi"],
        },
        "days": {
            "mon": ["Ana Ders: Problem Cozme temel kelimelerini tanitim (problem/solution/brainstorm) + yapi sunumu: The main problem is... One possible solution would be...", "Beceri Lab: Dinleme — 'Problem Cozme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — One possible solution would be + 2nd Conditional: If we implemented... + could/would yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Problem Cozme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Problem Cozme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Problem Cozme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (strategy/approach/alternative) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Problem Cozme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Problem Cozme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Bir problemi sistematik olarak analiz edebilir ve adim adim cozum yazabilir.",
    },
    {
        "week": 36,
        "theme": "Year-End Review & Reflection",
        "theme_tr": "Yil Sonu Degerlendirme ve Yansitma",
        "vocab": ["reflect", "progress", "achievement", "milestone", "growth", "portfolio", "self-assessment",
                  "feedback", "improvement", "goal", "accomplishment", "journey", "transition", "high school", "readiness"],
        "structure": "Over this year, I have learned... Looking back, I wish I had... Next year, I am going to... I am proud of...",
        "skills": {
            "listening": "Sinif arkadaslarinin yil sonu yansitma sunumlarini dinler, degerlendirme yapar.",
            "speaking": "Yillik gelisimini ozetler, en onemli kazanimlarini paylasir ve lise hedeflerini aciklar.",
            "reading": "Yil boyunca okunan metinlerden secmeleri tekrar okur, gelisimini degerlendirir.",
            "writing": "Yil sonu yansitma yazisi + lise hazirlik hedeflerini iceren portfolio ozeti yazar.",
        },
        "linked_content": {
            "categories": ["Degerlendirme", "Gelisim"],
            "songs": [],
            "games": ["Yil Sonu Bilgi Yarismasi", "Basari Haritasi"],
            "dialogues": ["Reflecting on My Year"],
            "readings": ["Year in Review"],
            "writings": ["My Year-End Reflection and High School Goals"],
            "grammar": ["Present Perfect review + wish + Past Perfect + going to for future plans"],
            "phonics": ["Overall pronunciation review and fluency check"],
            "listening": ["Yansitma Sunumlari"],
        },
        "days": {
            "mon": ["Ana Ders: Yil Sonu Degerlendirme temel kelimelerini tanitim (reflect/progress/achievement) + yapi sunumu: Over this year, I have learned... Looking back, I wish I had...", "Beceri Lab: Dinleme — 'Yil Sonu Degerlendirme' temali diyalogu dinle, anahtar kelimeleri bul"],
            "tue": ["Ana Ders: Gramer odak — Present Perfect review + wish + Past Perfect + going to for future plans yapisini acikla ve ornek cumleler kur", "Beceri Lab: Konusma — esli calisma, Yil Sonu Degerlendirme konusunda soru-cevap pratigi"],
            "wed": ["Ana Ders: Okuma — 'Yil Sonu Degerlendirme' temali metin oku, anlama sorularini cevapla", "Beceri Lab: Yazma — Yil Sonu Degerlendirme konusunda rehberli paragraf/cumle yazma"],
            "thu": ["Ana Ders: Kelime pekistirme (milestone/growth/portfolio) + gramer tekrari ve alishtirmalar", "Beceri Lab: Proje/Sunum — Yil Sonu Degerlendirme temali poster/sunum/yaratici etkinlik hazirlama"],
            "fri": ["Native Speaker: Yil Sonu Degerlendirme konusunda serbest konusma + kulturel karsilastirma + gercek yasam Ingilizcesi", "Native Speaker: Telaffuz calismalari + haftalik kelime/yapi tekrar oyunlari + akicilik pratigi"],
        },
        "assessment": "Yillik gelisimini ozetleyebilir, yansitma yazisi yazabilir ve lise hedeflerini belirleyebilir.",
    },
]

