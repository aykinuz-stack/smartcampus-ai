"""
Soru Sablonlari
===============
Tum dersler icin zengin soru havuzu.
Zorluk seviyelerine gore siniflandirilmis.
"""

from __future__ import annotations
import random

# ==================== MATEMATIK ====================

MATEMATIK_SORULARI = {
    "Kolay": [
        # Temel islemler (dinamik)
        {"text": "{a} + {b} = ?", "template": "addition", "vars": {"a": (1, 20), "b": (1, 20)}},
        {"text": "{a} - {b} = ?", "template": "subtraction", "vars": {"a": (10, 30), "b": (1, 10)}},
        {"text": "{a} x {b} = ?", "template": "multiplication", "vars": {"a": (2, 10), "b": (2, 10)}},
        {"text": "{a} : {b} = ?", "template": "division", "vars": {"a": "multiple", "b": (2, 10)}},
        # Kesirler
        {"text": "1/2 + 1/4 isleminin sonucu kactir?", "options": ["1/4", "2/4", "3/4", "4/4"], "answer": "C"},
        {"text": "3/6 kesrinin en sade hali nedir?", "options": ["1/3", "1/2", "2/3", "3/4"], "answer": "B"},
        {"text": "2/5 + 1/5 isleminin sonucu kactir?", "options": ["1/5", "2/5", "3/5", "4/5"], "answer": "C"},
        {"text": "4/8 kesrinin en sade hali nedir?", "options": ["1/4", "1/2", "2/4", "3/4"], "answer": "B"},
        {"text": "1/3 + 1/3 kactir?", "options": ["1/3", "2/3", "1/6", "2/6"], "answer": "B"},
        # Yuzde
        {"text": "100'un %25'i kactir?", "options": ["15", "20", "25", "30"], "answer": "C"},
        {"text": "50'nin %10'u kactir?", "options": ["5", "10", "15", "20"], "answer": "A"},
        {"text": "200'un %50'si kactir?", "options": ["50", "100", "150", "200"], "answer": "B"},
        {"text": "80'in %25'i kactir?", "options": ["10", "15", "20", "25"], "answer": "C"},
        {"text": "40'in %75'i kactir?", "options": ["10", "20", "30", "35"], "answer": "C"},
        # Geometri temel
        {"text": "Bir karenin tum acilarinin toplami kac derecedir?", "options": ["180", "270", "360", "450"], "answer": "C"},
        {"text": "Bir ucgenin ic acilar toplami kac derecedir?", "options": ["90", "180", "270", "360"], "answer": "B"},
        {"text": "Bir duzgun altigenin ic acilar toplami kac derecedir?", "options": ["540", "720", "900", "1080"], "answer": "B"},
        {"text": "Bir besgenin ic acilar toplami kac derecedir?", "options": ["360", "450", "540", "630"], "answer": "C"},
        # Sayilar
        {"text": "Ilk 5 dogal sayinin toplami kactir?", "options": ["10", "15", "20", "25"], "answer": "B"},
        {"text": "1'den 10'a kadar cift sayilarin toplami kactir?", "options": ["20", "25", "30", "35"], "answer": "C"},
        {"text": "-5 ile +3'un toplami kactir?", "options": ["-8", "-2", "2", "8"], "answer": "B"},
        {"text": "|-7| kactir?", "options": ["-7", "0", "7", "14"], "answer": "C"},
        {"text": "0.5 + 0.25 kactir?", "options": ["0.25", "0.5", "0.75", "1"], "answer": "C"},
    ],
    "Orta": [
        # Denklemler
        {"text": "2x + 5 = 15 denkleminde x kactir?", "options": ["3", "4", "5", "6"], "answer": "C"},
        {"text": "3x - 7 = 14 denkleminde x kactir?", "options": ["5", "6", "7", "8"], "answer": "C"},
        {"text": "x + x + x = 27 ise x kactir?", "options": ["7", "8", "9", "10"], "answer": "C"},
        {"text": "4x + 8 = 2x + 16 denkleminde x kactir?", "options": ["2", "4", "6", "8"], "answer": "B"},
        {"text": "5(x - 2) = 15 denkleminde x kactir?", "options": ["3", "4", "5", "6"], "answer": "C"},
        {"text": "x/2 + 3 = 7 denkleminde x kactir?", "options": ["4", "6", "8", "10"], "answer": "C"},
        # Carpanlar
        {"text": "24 sayisinin kac tane pozitif boleni vardir?", "options": ["6", "7", "8", "9"], "answer": "C"},
        {"text": "EBOB(12, 18) kactir?", "options": ["2", "3", "6", "9"], "answer": "C"},
        {"text": "EKOK(4, 6) kactir?", "options": ["10", "12", "18", "24"], "answer": "B"},
        {"text": "EBOB(15, 25) kactir?", "options": ["3", "5", "10", "15"], "answer": "B"},
        {"text": "EKOK(3, 5) kactir?", "options": ["8", "10", "15", "20"], "answer": "C"},
        {"text": "36 sayisinin asal carpanlarinin toplami kactir?", "options": ["5", "6", "7", "8"], "answer": "A"},
        # Oran-Orant
        {"text": "3/4 = x/20 ise x kactir?", "options": ["12", "15", "16", "18"], "answer": "B"},
        {"text": "A ve B'nin yasi orani 2/3'tur. A 10 yasindaysa B kac yasindadir?", "options": ["12", "15", "18", "20"], "answer": "B"},
        {"text": "5/8 = 15/x ise x kactir?", "options": ["20", "24", "28", "32"], "answer": "B"},
        {"text": "Bir kitabin %60'i 120 sayfadır. Kitap toplam kac sayfadir?", "options": ["180", "200", "220", "240"], "answer": "B"},
        # Geometri
        {"text": "Kenarlari 5 cm ve 8 cm olan dikdortgenin cevresi kac cm'dir?", "options": ["13", "26", "40", "52"], "answer": "B"},
        {"text": "Yaricapi 7 cm olan dairenin capi kac cm'dir?", "options": ["3.5", "7", "14", "21"], "answer": "C"},
        {"text": "Bir karenin alani 49 cm^2 ise bir kenar uzunlugu kac cm'dir?", "options": ["5", "6", "7", "8"], "answer": "C"},
        {"text": "Taban 6 cm, yuksekligi 4 cm olan ucgenin alani kac cm^2'dir?", "options": ["10", "12", "24", "48"], "answer": "B"},
        {"text": "Cevresi 20 cm olan karenin bir kenari kac cm'dir?", "options": ["4", "5", "6", "10"], "answer": "B"},
        # Fonksiyon
        {"text": "f(x) = 2x + 3 ise f(4) kactir?", "options": ["8", "9", "10", "11"], "answer": "D"},
        {"text": "f(x) = x^2 ise f(3) kactir?", "options": ["6", "8", "9", "12"], "answer": "C"},
        {"text": "f(x) = 3x - 1 ise f(5) kactir?", "options": ["12", "13", "14", "15"], "answer": "C"},
        {"text": "f(x) = x^2 + 1 ise f(2) kactir?", "options": ["3", "4", "5", "6"], "answer": "C"},
        {"text": "f(x) = 2x^2 ise f(-2) kactir?", "options": ["-8", "-4", "4", "8"], "answer": "D"},
    ],
    "Zor": [
        # Ikinci derece denklem
        {"text": "x^2 - 5x + 6 = 0 denkleminin kokleri toplami kactir?", "options": ["3", "4", "5", "6"], "answer": "C"},
        {"text": "x^2 - 9 = 0 denkleminin pozitif koku kactir?", "options": ["1", "2", "3", "4"], "answer": "C"},
        {"text": "x^2 + 4x + 4 = 0 denkleminin koku kactir?", "options": ["-4", "-2", "2", "4"], "answer": "B"},
        {"text": "x^2 - 7x + 12 = 0 denkleminin koklerinin carpimi kactir?", "options": ["7", "10", "12", "14"], "answer": "C"},
        {"text": "2x^2 - 8 = 0 denkleminin pozitif koku kactir?", "options": ["1", "2", "3", "4"], "answer": "B"},
        # Uslu sayilar
        {"text": "2^3 x 2^4 = 2^x ise x kactir?", "options": ["5", "6", "7", "12"], "answer": "C"},
        {"text": "(3^2)^3 kactir?", "options": ["27", "81", "243", "729"], "answer": "D"},
        {"text": "5^0 + 5^1 kactir?", "options": ["5", "6", "10", "25"], "answer": "B"},
        {"text": "8^(2/3) kactir?", "options": ["2", "4", "8", "16"], "answer": "B"},
        {"text": "27^(1/3) kactir?", "options": ["3", "9", "27", "81"], "answer": "A"},
        # Logaritma
        {"text": "log2(8) kactir?", "options": ["2", "3", "4", "8"], "answer": "B"},
        {"text": "log10(1000) kactir?", "options": ["2", "3", "4", "10"], "answer": "B"},
        {"text": "log3(27) kactir?", "options": ["2", "3", "4", "9"], "answer": "B"},
        {"text": "log5(125) kactir?", "options": ["2", "3", "4", "5"], "answer": "B"},
        {"text": "log4(16) kactir?", "options": ["1", "2", "3", "4"], "answer": "B"},
        # Trigonometri
        {"text": "sin(30) kactir?", "options": ["0", "1/2", "kok2/2", "kok3/2"], "answer": "B"},
        {"text": "cos(60) kactir?", "options": ["0", "1/2", "kok2/2", "kok3/2"], "answer": "B"},
        {"text": "tan(45) kactir?", "options": ["0", "1/2", "1", "kok2"], "answer": "C"},
        {"text": "sin(90) kactir?", "options": ["0", "1/2", "kok2/2", "1"], "answer": "D"},
        {"text": "cos(0) kactir?", "options": ["0", "1/2", "kok2/2", "1"], "answer": "D"},
        # Turev
        {"text": "f(x) = x^3 fonksiyonunun turevinde f'(2) kactir?", "options": ["4", "8", "12", "16"], "answer": "C"},
        {"text": "f(x) = 3x^2 + 2x fonksiyonunun turevi nedir?", "options": ["3x + 2", "6x + 2", "6x^2 + 2", "3x^2"], "answer": "B"},
        {"text": "f(x) = 5x^4 fonksiyonunun turevi nedir?", "options": ["5x^3", "20x^3", "4x^3", "x^5"], "answer": "B"},
        {"text": "f(x) = sin(x) fonksiyonunun turevi nedir?", "options": ["-sin(x)", "cos(x)", "-cos(x)", "tan(x)"], "answer": "B"},
        # Integral
        {"text": "integral(2x dx) sonucu nedir?", "options": ["x + C", "x^2 + C", "2x^2 + C", "x^2/2 + C"], "answer": "B"},
        {"text": "integral(3x^2 dx) sonucu nedir?", "options": ["x^3 + C", "6x + C", "3x^3 + C", "x^2 + C"], "answer": "A"},
        # Kombinasyon/Permutasyon
        {"text": "5 kisiden 3 kisilik komite kac farkli sekilde olusturulabilir?", "options": ["6", "8", "10", "12"], "answer": "C"},
        {"text": "4! kactir?", "options": ["12", "16", "20", "24"], "answer": "D"},
        {"text": "P(5,2) kactir?", "options": ["10", "15", "20", "25"], "answer": "C"},
        {"text": "C(6,2) kactir?", "options": ["12", "15", "18", "30"], "answer": "B"},
    ],
}

# ==================== FIZIK ====================

FIZIK_SORULARI = {
    "Kolay": [
        # Birimler
        {"text": "Hiz birimi asagidakilerden hangisidir?", "options": ["m/s", "m/s^2", "kg", "N"], "answer": "A"},
        {"text": "Kuvvet birimi asagidakilerden hangisidir?", "options": ["m/s", "kg", "N", "J"], "answer": "C"},
        {"text": "Enerji birimi asagidakilerden hangisidir?", "options": ["N", "W", "J", "Pa"], "answer": "C"},
        {"text": "Guc birimi asagidakilerden hangisidir?", "options": ["N", "W", "J", "Pa"], "answer": "B"},
        {"text": "Basinc birimi asagidakilerden hangisidir?", "options": ["N", "W", "J", "Pa"], "answer": "D"},
        {"text": "Elektrik akimi birimi asagidakilerden hangisidir?", "options": ["Volt", "Amper", "Ohm", "Watt"], "answer": "B"},
        # Temel bilgiler
        {"text": "Isik vakumda saniyede yaklasik kac km yol alir?", "options": ["30.000", "300.000", "3.000.000", "30.000.000"], "answer": "B"},
        {"text": "Hangisi temel buyukluk degildir?", "options": ["Uzunluk", "Kutle", "Zaman", "Hiz"], "answer": "D"},
        {"text": "Sicaklik birimi asagidakilerden hangisidir?", "options": ["Joule", "Newton", "Kelvin", "Watt"], "answer": "C"},
        {"text": "Su hangi sicaklikta kaynar? (deniz seviyesinde)", "options": ["90C", "95C", "100C", "110C"], "answer": "C"},
        {"text": "Yer cekimi ivmesi yaklasik kac m/s^2'dir?", "options": ["5", "8", "10", "15"], "answer": "C"},
        {"text": "Ses havada yaklasik kac m/s hizla yayilir?", "options": ["100", "200", "340", "500"], "answer": "C"},
        {"text": "Su hangi sicaklikta donar?", "options": ["-10C", "0C", "4C", "10C"], "answer": "B"},
        {"text": "1 kilometre kac metredir?", "options": ["10", "100", "1000", "10000"], "answer": "C"},
        {"text": "Hangisi skaler buyukluktur?", "options": ["Hiz", "Kuvvet", "Kutle", "Ivme"], "answer": "C"},
        {"text": "Hangisi vektorel buyukluktur?", "options": ["Sicaklik", "Zaman", "Kutle", "Kuvvet"], "answer": "D"},
    ],
    "Orta": [
        # Newton kanunlari
        {"text": "5 kg kutleli cisme 20 N kuvvet uygulanirsa ivme kac m/s^2 olur?", "options": ["2", "4", "5", "10"], "answer": "B"},
        {"text": "10 m/s hizla giden bir cisim 5 saniyede kac metre yol alir?", "options": ["2", "15", "50", "100"], "answer": "C"},
        {"text": "Durgun bir cisim 4 m/s^2 ivme ile 3 saniye hareket ederse hizi kac m/s olur?", "options": ["7", "10", "12", "14"], "answer": "C"},
        {"text": "8 kg kutleli cisme 40 N kuvvet uygulanirsa ivme kac m/s^2 olur?", "options": ["3", "4", "5", "6"], "answer": "C"},
        {"text": "F = m.a formulunde m neyi ifade eder?", "options": ["Hiz", "Ivme", "Kutle", "Kuvvet"], "answer": "C"},
        # Enerji
        {"text": "2 kg kutleli cisim 10 m yukseklikten serbest birakilirsa potansiyel enerjisi kac J'dur? (g=10)", "options": ["20", "100", "200", "400"], "answer": "C"},
        {"text": "500 W gucundeki makine 20 saniyede kac J is yapar?", "options": ["25", "100", "1000", "10000"], "answer": "D"},
        {"text": "4 m/s hizla giden 5 kg kutleli cismin kinetik enerjisi kac J'dur?", "options": ["20", "40", "60", "80"], "answer": "B"},
        {"text": "Bir cismin hem potansiyel hem kinetik enerjisi varsa toplam enerji nedir?", "options": ["Sadece potansiyel", "Sadece kinetik", "Mekanik enerji", "Isil enerji"], "answer": "C"},
        # Elektrik
        {"text": "Elektrik devresinde 12 V gerilim ve 4 A akim varsa direnc kac Ohm'dur?", "options": ["2", "3", "4", "8"], "answer": "B"},
        {"text": "V = I.R formulunde I neyi ifade eder?", "options": ["Gerilim", "Akim", "Direnc", "Guc"], "answer": "B"},
        {"text": "220 V gerilim ve 2 A akim oldugunda guc kac W'dir?", "options": ["110", "220", "440", "880"], "answer": "C"},
        # Optik
        {"text": "Isik cam ortamda havaya gore nasil kirilir?", "options": ["Normale yaklasir", "Normalden uzaklasir", "Kirilmaz", "Geri doner"], "answer": "B"},
        {"text": "Duz aynada goruntu nasil olusur?", "options": ["Ters-ayni boyda", "Duz-ayni boyda", "Ters-kucuk", "Duz-buyuk"], "answer": "B"},
        # Birim donusumleri
        {"text": "100 g = kac kg?", "options": ["0.01", "0.1", "1", "10"], "answer": "B"},
        {"text": "2 km = kac m?", "options": ["200", "2000", "20000", "200000"], "answer": "B"},
        {"text": "1 saat = kac saniye?", "options": ["60", "360", "3600", "36000"], "answer": "C"},
    ],
    "Zor": [
        # Kinetik ve potansiyel enerji
        {"text": "3 m/s hizla giden 2 kg kutleli cismin kinetik enerjisi kac J'dur?", "options": ["3", "6", "9", "12"], "answer": "C"},
        {"text": "5 m/s hizla giden 4 kg kutleli cismin kinetik enerjisi kac J'dur?", "options": ["25", "50", "100", "200"], "answer": "B"},
        # Serbest dusus
        {"text": "Serbest dususte 3 saniye sonra hiz kac m/s olur? (g=10)", "options": ["15", "30", "45", "90"], "answer": "B"},
        {"text": "Serbest dususte 2 saniyede alinan yol kac m'dir? (g=10)", "options": ["10", "20", "30", "40"], "answer": "B"},
        {"text": "45 m yukseklikten serbest birakilan cisim kac saniyede yere ulasir? (g=10)", "options": ["2", "3", "4", "5"], "answer": "B"},
        # Elektrik devreleri
        {"text": "5 Ohm ve 10 Ohm direncler seri baglanirsa toplam direnc kac Ohm olur?", "options": ["3.33", "7.5", "15", "50"], "answer": "C"},
        {"text": "6 Ohm ve 3 Ohm direncler paralel baglanirsa toplam direnc kac Ohm olur?", "options": ["2", "4.5", "9", "18"], "answer": "A"},
        {"text": "4 Ohm ve 4 Ohm direncler paralel baglanirsa toplam direnc kac Ohm olur?", "options": ["1", "2", "4", "8"], "answer": "B"},
        {"text": "2 Ohm, 3 Ohm ve 5 Ohm direncler seri baglanirsa toplam direnc kac Ohm olur?", "options": ["3.33", "5", "10", "30"], "answer": "C"},
        # Dalgalar
        {"text": "Dalga boyu 2 m, frekans 5 Hz ise dalga hizi kac m/s'dir?", "options": ["2.5", "5", "7", "10"], "answer": "D"},
        {"text": "Dalga hizi 340 m/s, frekans 170 Hz ise dalga boyu kac m'dir?", "options": ["0.5", "1", "2", "4"], "answer": "C"},
        # Momentum
        {"text": "Bir cismin momentumu 20 kg.m/s ve kutlesi 4 kg ise hizi kac m/s'dir?", "options": ["4", "5", "16", "80"], "answer": "B"},
        {"text": "3 kg kutleli cisim 6 m/s hizla hareket ediyorsa momentumu kac kg.m/s'dir?", "options": ["2", "9", "18", "36"], "answer": "C"},
        # Cembersel hareket
        {"text": "Cembersel harekette merkezcil ivme formulü nedir?", "options": ["v/r", "v^2/r", "v.r", "v^2.r"], "answer": "B"},
        {"text": "Cembersel harekette periyod T = 2 saniye ise frekans kac Hz'dir?", "options": ["0.25", "0.5", "1", "2"], "answer": "B"},
        # Is-Enerji
        {"text": "100 N kuvvet ile 5 m yol alan cisim uzerine yapilan is kac J'dur?", "options": ["20", "95", "105", "500"], "answer": "D"},
    ],
}

# ==================== KIMYA ====================

KIMYA_SORULARI = {
    "Kolay": [
        {"text": "Su'yun kimyasal formulu nedir?", "options": ["H2O", "CO2", "NaCl", "O2"], "answer": "A"},
        {"text": "Asagidakilerden hangisi element degildir?", "options": ["Altin (Au)", "Su (H2O)", "Demir (Fe)", "Karbon (C)"], "answer": "B"},
        {"text": "Periyodik tabloda atomlar neye gore siralanir?", "options": ["Atom numarasi", "Atom kutlesi", "Elektron sayisi", "Hacim"], "answer": "A"},
        {"text": "Hidrojen atomunda kac proton vardir?", "options": ["0", "1", "2", "3"], "answer": "B"},
        {"text": "Oksijen'in sembolü nedir?", "options": ["Ok", "Ox", "O", "O2"], "answer": "C"},
        {"text": "Asagidakilerden hangisi metal degildir?", "options": ["Demir", "Bakir", "Karbon", "Alüminyum"], "answer": "C"},
        {"text": "pH degeri 7 olan cozelti nasil bir ozellik gosterir?", "options": ["Asidik", "Bazik", "Notr", "Tuzlu"], "answer": "C"},
        {"text": "Havadaki en cok bulunan gaz hangisidir?", "options": ["Oksijen", "Karbon dioksit", "Azot", "Helyum"], "answer": "C"},
    ],
    "Orta": [
        {"text": "NaCl bilesigindeki baglanma turu nedir?", "options": ["Kovalent", "Iyonik", "Metalik", "Hidrojen"], "answer": "B"},
        {"text": "Asit ve baz tepkimesine ne ad verilir?", "options": ["Notrallesme", "Yanma", "Ayrisma", "Birlisme"], "answer": "A"},
        {"text": "Periyodik tabloda 1A grubundaki elementlere ne ad verilir?", "options": ["Halojenler", "Soy gazlar", "Alkali metaller", "Toprak alkali metaller"], "answer": "C"},
        {"text": "Elektronlari paylasarak olusan bag hangisidir?", "options": ["Iyonik", "Kovalent", "Metalik", "Van der Waals"], "answer": "B"},
        {"text": "CO2'nin adı nedir?", "options": ["Karbon monoksit", "Karbon dioksit", "Karbonlu su", "Karbonat"], "answer": "B"},
        {"text": "Mol sayisi birimi nedir?", "options": ["gram", "litre", "mol", "molar"], "answer": "C"},
        {"text": "Avogadro sayisi yaklasik kactir?", "options": ["6.02 x 10^20", "6.02 x 10^23", "6.02 x 10^26", "6.02 x 10^30"], "answer": "B"},
        {"text": "Hangi element soy gaz grubundadir?", "options": ["Azot", "Oksijen", "Helyum", "Hidrojen"], "answer": "C"},
    ],
    "Zor": [
        {"text": "2H2 + O2 -> 2H2O tepkimesinde 4 mol H2 kullanilirsa kac mol H2O olusur?", "options": ["2", "4", "6", "8"], "answer": "B"},
        {"text": "pH degeri 2 olan cozeltinin H+ konsantrasyonu kactir?", "options": ["10^-2 M", "10^-4 M", "2 M", "0.2 M"], "answer": "A"},
        {"text": "Suyun molar kutlesi kac g/mol'dur?", "options": ["16", "17", "18", "19"], "answer": "C"},
        {"text": "0.5 mol NaCl'nin kutlesi kac gramdır? (Na=23, Cl=35.5)", "options": ["29.25", "58.5", "117", "234"], "answer": "A"},
        {"text": "Ideal gaz denkleminde PV = ?", "options": ["mRT", "nRT", "NRT", "kT"], "answer": "B"},
        {"text": "Elektroliz sirasinda katotta ne olusur?", "options": ["Oksidasyon", "Indirgenme", "Notrallesme", "Buharlaşma"], "answer": "B"},
        {"text": "Organik kimyada -OH grubu iceren bilesiklere ne ad verilir?", "options": ["Eter", "Aldehit", "Alkol", "Keton"], "answer": "C"},
        {"text": "Lewis asidi nedir?", "options": ["Proton vericisi", "Proton alicisi", "Elektron cifti alicisi", "Elektron cifti vericisi"], "answer": "C"},
    ],
}

# ==================== BIYOLOJI ====================

BIYOLOJI_SORULARI = {
    "Kolay": [
        {"text": "Hucrenin enerji uretimiinden sorumlu organeli hangisidir?", "options": ["Ribozom", "Mitokondri", "Golgi", "Lizozom"], "answer": "B"},
        {"text": "Fotosentez hangi organelde gerceklesir?", "options": ["Mitokondri", "Ribozom", "Kloroplast", "Cekirdek"], "answer": "C"},
        {"text": "DNA'nin acilimi nedir?", "options": ["Deoksi Nitrik Asit", "Deoksiribo Nukleik Asit", "Di Nitro Amid", "Deoksi Nükleotit Amino"], "answer": "B"},
        {"text": "Insan vucudundaki en buyuk organ hangisidir?", "options": ["Kalp", "Karaciger", "Bobrek", "Deri"], "answer": "D"},
        {"text": "Kanin rengi neden kirmizidir?", "options": ["Demir", "Hemoglobin", "Plazma", "Trombosit"], "answer": "B"},
        {"text": "Bitkilerde suyun tasindigi doku hangisidir?", "options": ["Floem", "Ksilem", "Parankima", "Sklerenkima"], "answer": "B"},
        {"text": "Insanda kac cift kromozom bulunur?", "options": ["21", "22", "23", "46"], "answer": "C"},
        {"text": "Solunum olayinda hangi gaz alinir?", "options": ["Karbon dioksit", "Azot", "Oksijen", "Helyum"], "answer": "C"},
    ],
    "Orta": [
        {"text": "Protein sentezi hangi organelde gerceklesir?", "options": ["Mitokondri", "Ribozom", "Lizozom", "Golgi"], "answer": "B"},
        {"text": "Mayoz bolunme sonucunda kac hucre olusur?", "options": ["2", "4", "6", "8"], "answer": "B"},
        {"text": "Mitoz bolunme sonucunda kac hucre olusur?", "options": ["1", "2", "4", "8"], "answer": "B"},
        {"text": "DNA'nin yapitasi olan molekul hangisidir?", "options": ["Amino asit", "Nokleotit", "Glikoz", "Yag asidi"], "answer": "B"},
        {"text": "Asagidakilerden hangisi prokaryot canlidir?", "options": ["Bakteri", "Mantar", "Bitki", "Hayvan"], "answer": "A"},
        {"text": "Okaryot hucrelerde genetik bilgi nerede bulunur?", "options": ["Sitoplazma", "Ribozom", "Cekirdek", "Golgi"], "answer": "C"},
        {"text": "Enzimler yapica nedir?", "options": ["Karbonhidrat", "Lipit", "Protein", "Nokleik asit"], "answer": "C"},
        {"text": "ATP'nin acilimi nedir?", "options": ["Adenin Tri Fosfat", "Adenozin Tri Fosfat", "Amino Tri Protein", "Asit Tri Polimer"], "answer": "B"},
    ],
    "Zor": [
        {"text": "Mendel'in birinci yasasi nedir?", "options": ["Bagimsiz dagilim", "Ayrılma", "Baskinlik", "Coklu alel"], "answer": "B"},
        {"text": "Homozigot genotip asagidakilerden hangisidir?", "options": ["Aa", "AB", "AA", "aB"], "answer": "C"},
        {"text": "Aa x Aa caprazlamasinda fenotip orani nedir?", "options": ["1:1", "1:2:1", "3:1", "9:3:3:1"], "answer": "C"},
        {"text": "Protein sentezinde mRNA'nin gorevi nedir?", "options": ["Amino asit tasima", "Genetik bilgi tasima", "Ribozom olusturma", "Enerji uretimi"], "answer": "B"},
        {"text": "Krebs dongusu nerede gerceklesir?", "options": ["Sitoplazma", "Kloroplast", "Mitokondri matriks", "Golgi"], "answer": "C"},
        {"text": "Fotosentezin isik tepkimeleri nerede gerceklesir?", "options": ["Stroma", "Tilakoit", "Mitokondri", "Sitoplazma"], "answer": "B"},
        {"text": "Glikoliz sonucunda net kac ATP uretilir?", "options": ["2", "4", "32", "36"], "answer": "A"},
        {"text": "PCR ne ise yarar?", "options": ["DNA cogaltma", "RNA sentezi", "Protein uretimi", "Hucre bolunmesi"], "answer": "A"},
    ],
}

# ==================== TARIH ====================

TARIH_SORULARI = {
    "Kolay": [
        {"text": "Turkiye Cumhuriyeti hangi yil ilan edildi?", "options": ["1920", "1921", "1922", "1923"], "answer": "D"},
        {"text": "Ataturk'un dogum yili hangisidir?", "options": ["1879", "1881", "1883", "1885"], "answer": "B"},
        {"text": "TBMM hangi yil acildi?", "options": ["1919", "1920", "1921", "1922"], "answer": "B"},
        {"text": "Kurtulus Savasi hangi antlasma ile sona erdi?", "options": ["Sevr", "Mondros", "Lozan", "Mudanya"], "answer": "C"},
        {"text": "Istanbul hangi yil fethedildi?", "options": ["1299", "1402", "1453", "1517"], "answer": "C"},
        {"text": "Osmanli Devleti'nin kurucusu kimdir?", "options": ["Osman Bey", "Orhan Bey", "Murat I", "Fatih Sultan Mehmet"], "answer": "A"},
        {"text": "Ilk Turk devleti hangisidir?", "options": ["Hunlar", "Gokturkler", "Uygurlar", "Selcuklular"], "answer": "A"},
        {"text": "Malazgirt Savasi hangi yil yapildi?", "options": ["1071", "1176", "1243", "1402"], "answer": "A"},
    ],
    "Orta": [
        {"text": "Tanzimat Fermani hangi yil ilan edildi?", "options": ["1808", "1839", "1856", "1876"], "answer": "B"},
        {"text": "I. Mesrutiyet hangi yil ilan edildi?", "options": ["1856", "1876", "1908", "1919"], "answer": "B"},
        {"text": "Sakarya Meydan Muharebesi hangi yil yapildi?", "options": ["1919", "1920", "1921", "1922"], "answer": "C"},
        {"text": "Buyuk Taarruz hangi yil gerceklesti?", "options": ["1920", "1921", "1922", "1923"], "answer": "C"},
        {"text": "Misak-i Milli hangi kongrede kabul edildi?", "options": ["Erzurum", "Sivas", "Son Osmanli Meclis-i Mebusan", "TBMM"], "answer": "C"},
        {"text": "Harf Inkilabi hangi yil yapildi?", "options": ["1924", "1926", "1928", "1930"], "answer": "C"},
        {"text": "Kadinlara secme ve secilme hakki hangi yil verildi?", "options": ["1930", "1932", "1934", "1936"], "answer": "C"},
        {"text": "Soyadi Kanunu hangi yil cikarildi?", "options": ["1924", "1928", "1930", "1934"], "answer": "D"},
    ],
    "Zor": [
        {"text": "Mondros Mutarekesi'nden sonra Istanbul hangi tarihte isgal edildi?", "options": ["13 Kasim 1918", "15 Mayis 1919", "16 Mart 1920", "23 Nisan 1920"], "answer": "C"},
        {"text": "Ataturk 'Ordular! Ilk hedefiniz Akdeniz'dir' emrini ne zaman verdi?", "options": ["Sakarya Savasi", "Buyuk Taarruz", "Inonu Savasi", "Kurtulus Savasi basi"], "answer": "B"},
        {"text": "Osmanli-Safevi mucadelesinin temel nedeni neydi?", "options": ["Toprak", "Mezhep", "Ticaret", "Hanedanlik"], "answer": "B"},
        {"text": "Divan-i Humayun'un yerine hangi kurum getirildi?", "options": ["Meclis-i Vukela", "Meclis-i Mebusan", "Meclis-i Ayan", "TBMM"], "answer": "A"},
        {"text": "Osmanli'da ilk matbaa hangi padisah doneminde kuruldu?", "options": ["Fatih", "Kanuni", "III. Ahmet", "II. Mahmut"], "answer": "C"},
        {"text": "Celali Isyanlari'nin temel nedeni neydi?", "options": ["Dini nedenler", "Ekonomik sikinti", "Milliyetcilik", "Dis mudahale"], "answer": "B"},
        {"text": "Gulhane Hatt-i Humayunu'nu hazırlayan devlet adami kimdir?", "options": ["Alemdar Mustafa Pasa", "Mustafa Resit Pasa", "Ali Pasa", "Fuat Pasa"], "answer": "B"},
    ],
}

# ==================== COGRAFYA ====================

COGRAFYA_SORULARI = {
    "Kolay": [
        {"text": "Turkiye'nin baskenti hangisidir?", "options": ["Istanbul", "Ankara", "Izmir", "Bursa"], "answer": "B"},
        {"text": "Turkiye'nin en buyuk golu hangisidir?", "options": ["Tuz Golu", "Van Golu", "Beysehir Golu", "Egirdir Golu"], "answer": "B"},
        {"text": "Dunya'nin en buyuk okyanusu hangisidir?", "options": ["Atlantik", "Hint", "Pasifik", "Arktik"], "answer": "C"},
        {"text": "Turkiye kac cografi bolgeye ayrilir?", "options": ["5", "6", "7", "8"], "answer": "C"},
        {"text": "Turkiye'nin en uzun nehri hangisidir?", "options": ["Firat", "Dicle", "Kizilirmak", "Sakarya"], "answer": "C"},
        {"text": "Dunya'nin en yuksek dagi hangisidir?", "options": ["K2", "Everest", "Kilimanjaro", "Agri"], "answer": "B"},
        {"text": "Asagidakilerden hangisi bir kit'a degildir?", "options": ["Asya", "Avrupa", "Atlantik", "Afrika"], "answer": "C"},
        {"text": "Turkiye'nin en kalabalik sehri hangisidir?", "options": ["Ankara", "Izmir", "Istanbul", "Bursa"], "answer": "C"},
    ],
    "Orta": [
        {"text": "Asagidakilerden hangisi bir iklim unsurudur?", "options": ["Enlem", "Sicaklik", "Yukselti", "Denize uzaklik"], "answer": "B"},
        {"text": "Turkiye'de Akdeniz iklimi en cok hangi bolgede gokulur?", "options": ["Karadeniz", "Ic Anadolu", "Akdeniz", "Dogu Anadolu"], "answer": "C"},
        {"text": "Yukseltinin artmasiyla sicaklik nasil degisir?", "options": ["Artar", "Azalir", "Ayni kalir", "Duzensiz degisir"], "answer": "B"},
        {"text": "Turkiye'de kontinental iklim en cok hangi bolgede gokulur?", "options": ["Akdeniz", "Ege", "Ic Anadolu", "Karadeniz"], "answer": "C"},
        {"text": "Ruzgar hangi basinctan hangi basinca dogru eser?", "options": ["Yuksekten alcaga", "Alcaktan yuksege", "Esit basinc", "Rastgele"], "answer": "A"},
        {"text": "Asagidakilerden hangisi bir iklim faktoru degildir?", "options": ["Enlem", "Yukselti", "Sicaklik", "Denize uzaklik"], "answer": "C"},
        {"text": "Turkiye'de cayir ve mera alanlarinin en fazla oldugu bolge hangisidir?", "options": ["Akdeniz", "Ege", "Dogu Anadolu", "Marmara"], "answer": "C"},
        {"text": "Dogal afetlerden hangisi tektonik kokenlidir?", "options": ["Sel", "Heyelan", "Deprem", "Kasirga"], "answer": "C"},
    ],
    "Zor": [
        {"text": "Turkiye'nin en yuksek golu hangisidir?", "options": ["Van Golu", "Nemrut Golu", "Cildir Golu", "Burdur Golu"], "answer": "B"},
        {"text": "Asagidaki plato-bolge eslestirilmelerinden hangisi yanlistir?", "options": ["Obruk-Ic Anadolu", "Haymana-Ic Anadolu", "Cihanbeyli-Ege", "Uzunyayla-Dogu Anadolu"], "answer": "C"},
        {"text": "Turkiye'de en az yagis alan bolge hangisidir?", "options": ["Ege", "Ic Anadolu", "Guneydogu Anadolu", "Dogu Anadolu"], "answer": "B"},
        {"text": "Fohn ruzgari nasil bir etkiye sahiptir?", "options": ["Sogutma", "Isitma ve kurutma", "Nemlendirme", "Donturma"], "answer": "B"},
        {"text": "Turkiye'de petrol cikarilan baslica il hangisidir?", "options": ["Diyarbakir", "Sanliurfa", "Batman", "Adana"], "answer": "C"},
        {"text": "Asagidakilerden hangisi birincil ekonomik faaliyettir?", "options": ["Tarim", "Sanayi", "Ticaret", "Turizm"], "answer": "A"},
        {"text": "Nufus piramidinde genis taban ne anlama gelir?", "options": ["Yasli nufus fazla", "Genc nufus fazla", "Nufus duragan", "Nufus azaliyor"], "answer": "B"},
    ],
}

# ==================== TURKCE ====================

TURKCE_SORULARI = {
    "Kolay": [
        {"text": "Asagidaki cumlelerden hangisinde yazim yanlisi vardir?", "options": ["Herkez geldi.", "Herkes gelmis.", "Kimse yok.", "Biri var."], "answer": "A"},
        {"text": "'Kitap' sozcugu hangi tur isme ornektir?", "options": ["Ozel isim", "Cins isim", "Soyut isim", "Topluluk ismi"], "answer": "B"},
        {"text": "Asagidakilerden hangisi sifat degildir?", "options": ["guzel", "hizli", "kosmak", "buyuk"], "answer": "C"},
        {"text": "Hangi sozcuk fiildir?", "options": ["kitap", "guzel", "yurumek", "ev"], "answer": "C"},
        {"text": "'de/da' nasil yazilir?", "options": ["Bitisik", "Ayri", "Ikisi de olur", "Cumleye gore"], "answer": "B"},
        {"text": "'ki' eki ne zaman bitisik yazilir?", "options": ["Hicbir zaman", "Her zaman", "Sifat yaptigi zaman", "Baglac oldugu zaman"], "answer": "C"},
        {"text": "Asagidaki sozcuklerden hangisi somut isimdir?", "options": ["Mutluluk", "Ozlem", "Masa", "Ask"], "answer": "C"},
        {"text": "'Gel-' fiilinin olumsuzu nedir?", "options": ["Gelme", "Gelmemek", "Gelmez", "Hepsi"], "answer": "A"},
    ],
    "Orta": [
        {"text": "'Kitap okumak faydalidir' cumlesinin yargisi nedir?", "options": ["Soru", "Haber", "Emir", "Istek"], "answer": "B"},
        {"text": "Asagidaki cumlelerin hangisinde belirtisiz isim tamlamasi vardir?", "options": ["Kapinin kolu", "Masa ortusu", "Ali'nin kalemi", "Onun evi"], "answer": "B"},
        {"text": "'Bugün eve erken geldim' cumlesinde zarf tumleci hangisidir?", "options": ["Bugün ve erken", "Eve", "Geldim", "Bugün"], "answer": "A"},
        {"text": "Asagidaki cumlelerden hangisi basit cumledir?", "options": ["Kitap okudum ve uyudum", "Gelseydin gorusurduk", "Hava guzel", "Ne yaparsan yap"], "answer": "C"},
        {"text": "'Kirmizi elma' sozcuk grubunda 'kirmizi' ne gorevdedir?", "options": ["Isim", "Zamir", "Sifat", "Zarf"], "answer": "C"},
        {"text": "Asagidakilerden hangisi unlu uyumuna uymaz?", "options": ["Kalem", "Defter", "Kitap", "Anne"], "answer": "D"},
        {"text": "'Caliskan ogrenci basarili olur' cumlesinde ozne hangisidir?", "options": ["Caliskan", "Ogrenci", "Caliskan ogrenci", "Basarili"], "answer": "C"},
        {"text": "'-miş' eki ne tur bir ektir?", "options": ["Zaman eki", "Kisi eki", "Yapim eki", "Hal eki"], "answer": "A"},
    ],
    "Zor": [
        {"text": "Asagidaki cumlelerin hangisinde anlatim bozuklugu vardir?", "options": ["Eve gittim", "Okula basladi", "Seni cok ozledim", "Iceri girdim"], "answer": "B"},
        {"text": "'Yurutmek' fiilinin ettirgen cati hali nedir?", "options": ["Yurumek", "Yuruttürmek", "Yurunmek", "Yurusulmek"], "answer": "B"},
        {"text": "Asagidakilerden hangisi zincirleme isim tamlamasidir?", "options": ["Arkadas evi", "Arkadasimin evinin kapisi", "Kapı kolu", "Ev sahibi"], "answer": "B"},
        {"text": "'Kar yagdi, okullar tatil edildi' cumlesi hangi tur birlesik cumledir?", "options": ["Sartli", "Neden-sonuc", "Ki'li", "Girisik"], "answer": "B"},
        {"text": "Asagidaki sozcuklerden hangisi turemis sozcuktur?", "options": ["Goz", "Gozluk", "Kitap", "Ev"], "answer": "B"},
        {"text": "'Orman' sozcugundeki ses olayı nedir?", "options": ["Unlu daralmasi", "Unlu dusmesi", "Unsuz yumusamasi", "Ses olayi yok"], "answer": "D"},
        {"text": "Asagidakilerden hangisi devrik cumledir?", "options": ["Ali geldi", "Geldi Ali bugun", "Bugun Ali geldi", "Ali bugun geldi"], "answer": "B"},
    ],
}

# ==================== INGILIZCE ====================

INGILIZCE_SORULARI = {
    "Kolay": [
        {"text": "She ___ to school every day.", "options": ["go", "goes", "going", "gone"], "answer": "B"},
        {"text": "What is the past tense of 'eat'?", "options": ["eated", "ate", "eaten", "eating"], "answer": "B"},
        {"text": "Which word is a noun?", "options": ["quickly", "beautiful", "happiness", "run"], "answer": "C"},
        {"text": "I ___ a student.", "options": ["is", "am", "are", "be"], "answer": "B"},
        {"text": "They ___ playing football now.", "options": ["is", "am", "are", "was"], "answer": "C"},
        {"text": "___ you speak English?", "options": ["Do", "Does", "Is", "Are"], "answer": "A"},
        {"text": "This is ___ apple.", "options": ["a", "an", "the", "---"], "answer": "B"},
        {"text": "He ___ TV yesterday.", "options": ["watch", "watches", "watched", "watching"], "answer": "C"},
    ],
    "Orta": [
        {"text": "If it rains, I ___ stay home.", "options": ["will", "would", "shall", "might"], "answer": "A"},
        {"text": "She has been working here ___ 2015.", "options": ["for", "since", "from", "at"], "answer": "B"},
        {"text": "The book ___ by Mark Twain.", "options": ["wrote", "written", "was written", "has written"], "answer": "C"},
        {"text": "I wish I ___ rich.", "options": ["am", "was", "were", "be"], "answer": "C"},
        {"text": "He asked me where I ___.", "options": ["live", "lived", "living", "lives"], "answer": "B"},
        {"text": "___ I borrow your pen?", "options": ["May", "Should", "Must", "Will"], "answer": "A"},
        {"text": "She is ___ than her sister.", "options": ["tall", "taller", "tallest", "more tall"], "answer": "B"},
        {"text": "I have ___ finished my homework.", "options": ["yet", "already", "still", "ever"], "answer": "B"},
    ],
    "Zor": [
        {"text": "Had I known earlier, I ___ have helped.", "options": ["will", "would", "shall", "can"], "answer": "B"},
        {"text": "Not only ___ intelligent, but she is also hardworking.", "options": ["she is", "is she", "was she", "she was"], "answer": "B"},
        {"text": "The more you practice, ___ you become.", "options": ["better", "the better", "best", "the best"], "answer": "B"},
        {"text": "He denied ___ the money.", "options": ["steal", "stealing", "to steal", "stolen"], "answer": "B"},
        {"text": "I'd rather you ___ smoke here.", "options": ["don't", "didn't", "won't", "not"], "answer": "B"},
        {"text": "It's high time we ___ home.", "options": ["go", "went", "going", "gone"], "answer": "B"},
        {"text": "Hardly ___ arrived when it started raining.", "options": ["I had", "had I", "I have", "have I"], "answer": "B"},
        {"text": "She suggested that he ___ a doctor.", "options": ["sees", "see", "saw", "seeing"], "answer": "B"},
    ],
}

# ==================== FELSEFE ====================

FELSEFE_SORULARI = {
    "Kolay": [
        {"text": "'Varlik nedir?' sorusu hangi felsefi alanla ilgilidir?", "options": ["Etik", "Estetik", "Ontoloji", "Epistemoloji"], "answer": "C"},
        {"text": "'Bilgi nedir?' sorusu hangi felsefi alanla ilgilidir?", "options": ["Ontoloji", "Epistemoloji", "Etik", "Estetik"], "answer": "B"},
        {"text": "'Iyi ve kotu nedir?' sorusu hangi felsefi alanla ilgilidir?", "options": ["Ontoloji", "Epistemoloji", "Etik", "Mantik"], "answer": "C"},
        {"text": "'Guzel nedir?' sorusu hangi felsefi alanla ilgilidir?", "options": ["Etik", "Estetik", "Ontoloji", "Mantik"], "answer": "B"},
        {"text": "Felsefe kelimesi hangi dilden gelmektedir?", "options": ["Latince", "Arapca", "Yunanca", "Farsca"], "answer": "C"},
        {"text": "Sokrates'in ogretim yontemi hangisidir?", "options": ["Dogmatik", "Diyalektik", "Analitik", "Sentetik"], "answer": "B"},
        {"text": "Platon'un hocasi kimdir?", "options": ["Aristoteles", "Sokrates", "Tales", "Pisagor"], "answer": "B"},
        {"text": "Aristoteles'in hocasi kimdir?", "options": ["Sokrates", "Platon", "Tales", "Herakleitos"], "answer": "B"},
    ],
    "Orta": [
        {"text": "'Dusunuyorum, o halde varim' sozunu soyleyen kimdir?", "options": ["Platon", "Aristoteles", "Descartes", "Kant"], "answer": "C"},
        {"text": "Pragmatizm felsefesinin kurucusu kimdir?", "options": ["Hegel", "Nietzsche", "William James", "Heidegger"], "answer": "C"},
        {"text": "Varoluşculuk akiminin temsilcisi kimdir?", "options": ["Kant", "Hegel", "Sartre", "Platon"], "answer": "C"},
        {"text": "'Tanri oldu' diyen filozof kimdir?", "options": ["Marx", "Hegel", "Nietzsche", "Freud"], "answer": "C"},
        {"text": "Rasyonalizm ne demektir?", "options": ["Deneycilik", "Akılcılık", "Sezgicilik", "Dogmacilik"], "answer": "B"},
        {"text": "Empirizm ne demektir?", "options": ["Akılcılık", "Deneycilik", "Dogmacilik", "Sezgicilik"], "answer": "B"},
        {"text": "Kategorik imperatif kavramini gelistiren kimdir?", "options": ["Hegel", "Kant", "Nietzsche", "Heidegger"], "answer": "B"},
        {"text": "Idea kavrami hangi filozofa aittir?", "options": ["Aristoteles", "Platon", "Sokrates", "Tales"], "answer": "B"},
    ],
    "Zor": [
        {"text": "Fenomenoloji akiminin kurucusu kimdir?", "options": ["Heidegger", "Husserl", "Sartre", "Merleau-Ponty"], "answer": "B"},
        {"text": "'Varlık ve Zaman' eserinin yazari kimdir?", "options": ["Husserl", "Heidegger", "Sartre", "Jaspers"], "answer": "B"},
        {"text": "Frankfurt Okulu hangi akimla iliskilidir?", "options": ["Pragmatizm", "Elestirel teori", "Pozitivizm", "Varoluşculuk"], "answer": "B"},
        {"text": "Yapısökümü (Deconstruction) teorisinin temsilcisi kimdir?", "options": ["Foucault", "Derrida", "Deleuze", "Lyotard"], "answer": "B"},
        {"text": "Dil oyunlari kavramini gelistiren kimdir?", "options": ["Russell", "Wittgenstein", "Frege", "Carnap"], "answer": "B"},
        {"text": "Simülakr kavramini gelistiren filosof kimdir?", "options": ["Deleuze", "Baudrillard", "Lyotard", "Foucault"], "answer": "B"},
        {"text": "Bilimsel devrimlerin yapisi eserinin yazari kimdir?", "options": ["Popper", "Kuhn", "Lakatos", "Feyerabend"], "answer": "B"},
    ],
}


def get_question_from_template(subject: str, difficulty: str) -> dict | None:
    """Sablondan soru uret."""
    templates = {
        "Matematik": MATEMATIK_SORULARI,
        "Fizik": FIZIK_SORULARI,
        "Kimya": KIMYA_SORULARI,
        "Biyoloji": BIYOLOJI_SORULARI,
        "Tarih": TARIH_SORULARI,
        "Cografya": COGRAFYA_SORULARI,
        "Turkce": TURKCE_SORULARI,
        "Ingilizce": INGILIZCE_SORULARI,
        "Felsefe": FELSEFE_SORULARI,
    }

    subject_questions = templates.get(subject)
    if not subject_questions:
        return None

    difficulty_questions = subject_questions.get(difficulty, subject_questions.get("Orta", []))
    if not difficulty_questions:
        return None

    q = random.choice(difficulty_questions).copy()

    # Template varsa isle
    if "template" in q:
        q = _process_template(q)

    q["subject"] = subject
    q["difficulty"] = difficulty

    return q


def _process_template(q: dict) -> dict:
    """Template soruyu isle ve degerleri uret."""
    template_type = q.get("template")
    vars_config = q.get("vars", {})

    if template_type == "addition":
        a = random.randint(*vars_config.get("a", (1, 20)))
        b = random.randint(*vars_config.get("b", (1, 20)))
        answer = a + b
        q["text"] = q["text"].format(a=a, b=b)
        q["options"] = [str(answer - 1), str(answer), str(answer + 1), str(answer + 2)]
        q["answer"] = "B"

    elif template_type == "subtraction":
        a = random.randint(*vars_config.get("a", (10, 30)))
        b = random.randint(*vars_config.get("b", (1, 10)))
        answer = a - b
        q["text"] = q["text"].format(a=a, b=b)
        q["options"] = [str(answer - 2), str(answer - 1), str(answer), str(answer + 1)]
        q["answer"] = "C"

    elif template_type == "multiplication":
        a = random.randint(*vars_config.get("a", (2, 10)))
        b = random.randint(*vars_config.get("b", (2, 10)))
        answer = a * b
        q["text"] = q["text"].format(a=a, b=b)
        wrong1 = answer - b if answer > b else answer + b
        wrong2 = answer + a
        wrong3 = answer + b
        q["options"] = [str(wrong1), str(answer), str(wrong2), str(wrong3)]
        q["answer"] = "B"

    elif template_type == "division":
        b = random.randint(*vars_config.get("b", (2, 10)))
        multiplier = random.randint(2, 10)
        a = b * multiplier
        answer = multiplier
        q["text"] = q["text"].format(a=a, b=b)
        q["options"] = [str(answer - 1), str(answer), str(answer + 1), str(answer + 2)]
        q["answer"] = "B"

    # Template ve vars'i kaldir
    q.pop("template", None)
    q.pop("vars", None)

    return q
