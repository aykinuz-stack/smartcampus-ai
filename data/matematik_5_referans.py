# -*- coding: utf-8 -*-
"""
5. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme alanlari:
1. Geometrik Sekiller
2. Sayilar ve Nicelikler
3. Cebir
4. Veri Isleme
"""

MATEMATIK_5_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: GEOMETRIK SEKILLER
# ═══════════════════════════════════════════════════════════════

"MAT.5.1.GEOMETRIK_CIZIM": {
    "unite": "Geometrik Sekiller",
    "baslik": "Temel Geometrik Cizimler ve Insalar",
    "icerik": """
TEMEL GEOMETRIK KAVRAMLAR:

1. NOKTA:
   - Boyutsuz (uzunlugu, genisligi, yuksekligi yoktur)
   - Buyuk harflerle gosterilir: A, B, C
   - "Bir noktanin konumu vardir ama boyutu yoktur."

2. DOGRU:
   - Iki yonde sonsuza uzanan duz cizgi
   - Iki buyuk harfle veya kucuk harfle gosterilir: AB dogrusu veya d dogrusu
   - Uzunlugu olculemez (sonsuz)
   - Iki noktadan yalnizca bir dogru gecer

3. DOGRU PARCASI:
   - Iki noktayla sinirlandirilmis dogru parcasi
   - [AB] seklinde gosterilir
   - Uzunlugu olculebilir: |AB| = 5 cm gibi

4. ISIN:
   - Bir uctandan baslayip bir yonde sonsuza giden yari-dogru
   - [AB isini: A baslangic noktasi, B yonu belirler
   - Bir baslangic noktasi vardir ama sonu yoktur

5. ACI:
   - Ayni noktadan cikan iki isinin olusturdugu sekil
   - Olcu birimi: derece (°)
   - Acinin koseleri buyuk harfle, aci sembolü ile gosterilir: ∠ABC veya ∠B
   - Aci turleri:
     * Dar aci: 0° < aci < 90°
     * Dik aci: Tam 90° (kare sembolü ile gosterilir)
     * Genis aci: 90° < aci < 180°
     * Dogru aci: Tam 180°
     * Tam aci: Tam 360°

6. CEMBER:
   - Bir noktaya esit uzakliktaki tum noktalarin olusturdugu kapalı egri
   - Merkez: Cemberin orta noktasi (O ile gosterilir)
   - Yaricap (r): Merkezden cember uzerindeki herhangi bir noktaya olan uzaklik
   - Cap (d): Cember uzerindeki iki noktayi merkezden gecirerek birlestiren dogru parcasi
   - d = 2r (cap, yariçapin iki katidir)
   - Pergel ile cizilir

7. DIKME:
   - Bir dogru veya dogru parcasina dik olan dogru
   - 90 derecelik aci olusturur
   - Gonye veya pergel ile cizilebilir
   - Bir noktadan bir dogruya yalnizca bir dikme cizilebilir
   - Dikme, bir noktanin dogruya en kisa uzakligini gosterir

ARACLAR:
- Cetvel: Dogru, dogru parcasi cizmek, uzunluk olcmek
- Iletki: Aci olcmek ve aci cizmek (0°-180° arasi)
- Pergel: Cember cizmek, esit uzunluk tasimak
- Gonye: Dik aci olcmek ve cizmek (30-60-90 veya 45-45-90 gonye)
"""
},

"MAT.5.1.ACI_OLCME": {
    "unite": "Geometrik Sekiller",
    "baslik": "Aci Olcme ve Cesitleri",
    "icerik": """
ACI OLCME:
- Arac: Iletki (aciolcer)
- Birim: Derece (°)
- Iletki kullanimi:
  1. Iletkinin merkez noktasini acinin kose noktasina yerlestir
  2. Iletkinin sifir cizgisini acinin bir koluyla cakistir
  3. Diger kolun gosterdigi dereceyi oku

ACI CESITLERI:
- Dar aci: 0° ile 90° arasinda (orn: 45°, 30°, 60°, 75°)
- Dik aci: Tam 90° — kose noktasinda kucuk kare ile gosterilir
- Genis aci: 90° ile 180° arasinda (orn: 120°, 135°, 150°)
- Dogru aci: Tam 180° — bir dogru olusturur
- Tam aci: Tam 360° — tam bir donuş

ACI ILISKILERI:
- Komsu acilar: Ortak bir kosleri ve bir kollari olan acilar
- Butunler acilar: Toplami 90° olan iki aci (orn: 30° + 60° = 90°)
- Butunler acilar: Toplami 180° olan iki aci (orn: 110° + 70° = 180°)
  * DIKKAT: 5. sinifta "tümler" (90°) ve "bütünler" (180°) ayrimi:
    - Tumler aci: Toplami 90° → "iki aci tümlerdir" (complementary)
    - Butunler aci: Toplami 180° → "iki aci bütünlerdir" (supplementary)

UCGEN VE ACI ILISKISI:
- Bir ucgenin ic acilari toplami = 180°
- Ornek: Bir ucgende iki aci 60° ve 70° ise ucuncu aci = 180° - 60° - 70° = 50°
"""
},

"MAT.5.1.UCGEN_DORTGEN": {
    "unite": "Geometrik Sekiller",
    "baslik": "Ucgenler ve Dortgenler",
    "icerik": """
UCGEN:
Tanim: Uc dogru parcasinin birlestirilmesiyle olusan kapalı geometrik sekil.
Ozellikleri:
- 3 kenar, 3 kose noktasi, 3 ic aci
- Ic acilar toplami = 180°
- Herhangi iki kenar uzunlugu toplami, ucuncu kenardan buyuktur (Ucgen esitsizligi)

KENARLARINA GORE UCGENLER:
1. Eskenar ucgen: Uc kenari esit. Uc acisi da esit (60°-60°-60°)
2. Ikizkenar ucgen: Iki kenari esit. Esit kenarlarin karsisindaki acilar da esittir.
3. Cesitkenar ucgen: Uc kenari farkli uzunlukta. Uc acisi da farkli.

ACILARINA GORE UCGENLER:
1. Dar acili ucgen: Uc acisi da dar acı (hepsi 90°'den kucuk)
2. Dik acili ucgen: Bir acisi dik aci (90°). Dik acinin karsisindaki kenar "hipotenüs"tur (en uzun kenar).
3. Genis acili ucgen: Bir acisi genis aci (90°'den buyuk)

UCGENIN CEVRESI:
Cevre = kenar1 + kenar2 + kenar3
Ornek: Kenarlari 3 cm, 4 cm, 5 cm olan ucgenin cevresi = 3 + 4 + 5 = 12 cm

UCGENIN ALANI:
Alan = (taban × yukseklik) / 2
Ornek: Tabani 6 cm, yuksekligi 4 cm → Alan = (6 × 4) / 2 = 12 cm²

DORTGENLER:
Tanim: Dort dogru parcasinin birlestirilmesiyle olusan kapalı geometrik sekil.

1. KARE:
   - 4 kenari esit, 4 acisi dik aci (90°)
   - Cevre = 4 × kenar = 4a
   - Alan = kenar × kenar = a²
   - Kosegenleri esit ve birbirini dik olarak ortalar

2. DIKDORTGEN:
   - Karsi kenarlari esit, 4 acisi dik aci (90°)
   - Cevre = 2 × (uzun kenar + kisa kenar) = 2(a + b)
   - Alan = uzun kenar × kisa kenar = a × b
   - Kosegenleri esit ve birbirini ortalar (dik degil)

3. PARALELKENAR:
   - Karsi kenarlari paralel ve esit
   - Karsi acilari esit
   - Cevre = 2(a + b)
   - Alan = taban × yukseklik

4. ESKENAR DORTGEN:
   - 4 kenari esit ama acilari dik olmak zorunda degil
   - Karsi acilari esit

5. YAMUK:
   - Yalnizca iki kenari paralel (paralel kenarlar: ust taban ve alt taban)
   - Ikizkenar yamuk: Paralel olmayan kenarlari esit
   - Alan = ((ust taban + alt taban) × yukseklik) / 2

DORTGENIN IC ACILARI TOPLAMI = 360°
"""
},

"MAT.5.1.CEMBER_DAIRE": {
    "unite": "Geometrik Sekiller",
    "baslik": "Cember ve Daire",
    "icerik": """
CEMBER:
Tanim: Bir noktaya (merkez) esit uzaklikta bulunan tum noktalarin olusturdugu kapali egri.
- Merkez noktasi: O
- Yaricap (r): Merkezden cember uzerindeki noktaya uzaklik
- Cap (d): Cemberden gecen ve merkezden gecen dogru parcasi → d = 2r
- Cemberin uzunlugu (cevre): C = 2πr = πd (π ≈ 3,14)

DAIRE:
Tanim: Cember ve cemberin ic bolgesi birlikte.
- Dairenin alani: A = πr² (π ≈ 3,14)
- Ornek: r = 7 cm → A = 3,14 × 7² = 3,14 × 49 = 153,86 cm²

π (Pi) SAYISI:
- Cemberin cevresinin capina orani her zaman sabittir: C/d = π
- π ≈ 3,14159265... (irrasyonel sayi — ondalik kismi sonsuza gider, tekrar etmez)
- 5. sinifta π ≈ 3,14 olarak alinir
- Gecmiste farkli medeniyetler π'yi yaklasik olarak hesaplamistir

CEMBERDE OZEL DOGRU PARCALARI:
- Yaricap: Merkezden cember uzerine
- Cap: Cember uzerindeki iki noktayi merkezden gecirerek birlestiren
- Kiriş: Cember uzerindeki herhangi iki noktayi birlestiren dogru parcasi
- Cap en buyuk kiristir
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: SAYILAR VE NICELIKLER
# ═══════════════════════════════════════════════════════════════

"MAT.5.2.DOGAL_SAYILAR": {
    "unite": "Sayilar ve Nicelikler",
    "baslik": "Dogal Sayilar ve Islemler",
    "icerik": """
DOGAL SAYILAR:
- Dogal sayilar kumesi: N = {0, 1, 2, 3, 4, 5, ...}
- Sayma sayilari: N* = {1, 2, 3, 4, 5, ...} (sifir dahil degil)
- Dogal sayilarin sonuncusu yoktur (sonsuz)

BASAMAK VE BASAMAK DEGERI:
- Birler basamagi, onlar basamagi, yuzler basamagi, binler basamagi...
- Basamak degeri = Rakamdaki sayi × Basamagin degeri
  Ornek: 3.456'da 4'un basamak degeri = 4 × 100 = 400

DORT ISLEM:
1. Toplama: 234 + 567 = 801 (toplanan + toplanan = toplam)
2. Cikarma: 801 - 567 = 234 (eksilen - cikan = fark)
3. Carpma: 23 × 15 = 345 (carpan × carpan = carpim)
4. Bolme: 345 ÷ 15 = 23 (bolunen ÷ bolen = bolum)
   - Kalanlı bolme: 347 ÷ 15 = 23, kalan 2
   - Kalan her zaman bolenden kucuktur

ISLEM SIRASI (ONCELIK):
1. Parantez icindeki islemler
2. Carpma ve bolme (soldan saga)
3. Toplama ve cikarma (soldan saga)
Ornek: 3 + 4 × 2 = 3 + 8 = 11 (carpma once!)
Ornek: (3 + 4) × 2 = 7 × 2 = 14 (parantez once!)

CARPMA VE BOLMENIN OZELLIKLERI:
- Degisme ozelligi: a × b = b × a (5 × 3 = 3 × 5 = 15)
- Birleme ozelligi: (a × b) × c = a × (b × c)
- Etkisiz eleman: a × 1 = a (1 ile carpim sayinin kendisi)
- Yutan eleman: a × 0 = 0 (0 ile carpim her zaman 0)
- Dagılma ozelligi: a × (b + c) = a × b + a × c
- Sifira bolme TANIMSIZDIR (hicbir sayi sifira bolunemez)
"""
},

"MAT.5.2.KESIRLER": {
    "unite": "Sayilar ve Nicelikler",
    "baslik": "Kesirler",
    "icerik": """
KESIR KAVRAMI:
- Bir butunun esit parcalara bolunmesinde her bir parcayi ifade eder
- a/b seklinde yazilir (a: pay, b: payda)
- Payda sifir olamaz

KESIR TURLERI:
1. Basit kesir: Pay < Payda → 3/5, 2/7, 1/4
2. Bileşik kesir: Pay > Payda → 7/3, 5/2, 9/4
3. Tam sayili kesir: Tam sayi + basit kesir → 2 1/3, 3 2/5
   - Bilesik kesirden → tam sayili: 7/3 = 2 1/3 (7÷3=2 kalan 1)
   - Tam sayili → bilesik: 2 1/3 = (2×3+1)/3 = 7/3

DENK KESIRLER:
- Ayni buyuklugu gosteren farkli kesirler
- Pay ve payda ayni sayiyla carpilir veya bolunur
- 1/2 = 2/4 = 3/6 = 4/8 = 5/10

KESIRLERI SADELEŞTIRME:
- Pay ve paydayi ortak bolenlerine bolme
- 6/8 → pay ve payda 2'ye bolunur → 3/4
- En sade hali: Pay ve paydanin 1 disinda ortak boleni yoksa

KESIRLERDE SIRALAMA:
- Ayni paydali kesirler: Payi buyuk olan buyuktur (3/7 > 2/7)
- Ayni payli kesirler: Paydasi kucuk olan buyuktur (2/3 > 2/5)
- Farkli paydali: Paydalar esitlenir sonra karsilastirilir

KESIRLERDE TOPLAMA-CIKARMA:
- Ayni paydali: Paydalar ayni kalir, paylar toplanir/cikarilir
  3/7 + 2/7 = 5/7
- Farkli paydali: Paydalar esitlenir (EKOK alinir)
  1/3 + 1/4 = 4/12 + 3/12 = 7/12

KESIRLERDE CARPMA:
- Pay × pay / Payda × payda
- 2/3 × 4/5 = 8/15
- Tam sayiyla carpma: 3 × 2/5 = 6/5 = 1 1/5

ONDALIK GOSTERIM:
- Paydasi 10, 100, 1000 olan kesirler ondalik olarak yazilabilir
- 1/2 = 5/10 = 0,5
- 1/4 = 25/100 = 0,25
- 3/4 = 75/100 = 0,75
"""
},

"MAT.5.2.ONDALIK_GOSTERIM": {
    "unite": "Sayilar ve Nicelikler",
    "baslik": "Ondalik Gosterim ve Yuzde",
    "icerik": """
ONDALIK KESIR:
- Virgulun solu: Tam kisim
- Virgulun sagi: Ondalik kisim
- Basamaklar: Onda birler (0,1), Yuzde birler (0,01), Binde birler (0,001)

ONDALIK KESIRLERDE ISLEMLER:
Toplama/Cikarma: Virguller alt alta gelecek sekilde yazilir
  2,35 + 1,40 = 3,75
  5,80 - 2,35 = 3,45

Carpma: Normal carpilir, ondalik basamak sayilari toplanir
  1,2 × 0,3 = 0,36 (1 + 1 = 2 ondalik basamak)

Bolme: Bolucu tam sayiya cevrilerek bolunur
  4,5 ÷ 0,5 = 45 ÷ 5 = 9

YUZDE (%):
- "Yuzde" demek "yuzdeki pay" demektir → %25 = 25/100 = 0,25
- Kesirden yuzdeye: 3/4 = 75/100 = %75
- Yüzdeden kesire: %40 = 40/100 = 2/5

YUZDE HESAPLAMA:
- Bir sayinin %'si: Sayi × yuzde/100
  Ornek: 200'un %25'i = 200 × 25/100 = 50
- Yuzde artis: 100 TL'de %20 artis = 100 + 20 = 120 TL
- Yuzde azalis: 100 TL'de %20 azalis = 100 - 20 = 80 TL

KESIR - ONDALIK - YUZDE DONUSUMLERI:
1/2 = 0,5 = %50
1/4 = 0,25 = %25
3/4 = 0,75 = %75
1/5 = 0,2 = %20
1/10 = 0,1 = %10
1/3 ≈ 0,333... = %33,3...
"""
},

"MAT.5.2.OLCME": {
    "unite": "Sayilar ve Nicelikler",
    "baslik": "Olcme (Uzunluk, Alan, Hacim, Zaman, Tartma)",
    "icerik": """
UZUNLUK OLCULERI:
- Temel birim: metre (m)
- 1 km = 1.000 m
- 1 m = 10 dm = 100 cm = 1.000 mm
- 1 dm = 10 cm
- 1 cm = 10 mm
- Buyukten kucuge her basamakta 10 ile carpilir, kucukten buyuge 10 ile bolunur

ALAN OLCULERI:
- Temel birim: metrekare (m²)
- 1 m² = 100 dm² = 10.000 cm²
- 1 km² = 1.000.000 m²
- 1 dm² = 100 cm²
- Buyukten kucuge her basamakta 100 ile carpilir

HACIM OLCULERI:
- Temel birim: metrekup (m³)
- 1 m³ = 1.000 dm³ = 1.000.000 cm³
- 1 dm³ = 1.000 cm³
- 1 dm³ = 1 litre (L)
- 1 m³ = 1.000 litre
- Buyukten kucuge her basamakta 1.000 ile carpilir

SIVI OLCULERI:
- 1 L (litre) = 1.000 mL (mililitre)
- 1 L = 1 dm³
- 1 mL = 1 cm³

ZAMAN OLCULERI:
- 1 yil = 12 ay = 365 gun (artik yil: 366 gun)
- 1 ay = 28, 29, 30 veya 31 gun
- 1 hafta = 7 gun
- 1 gun = 24 saat
- 1 saat = 60 dakika
- 1 dakika = 60 saniye
- 1 saat = 3.600 saniye

TARTMA (KUTLE) OLCULERI:
- 1 ton = 1.000 kg
- 1 kg = 1.000 g
- 1 g = 1.000 mg
- Yari kg = 500 g
- Ceyrek kg = 250 g
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: CEBIR
# ═══════════════════════════════════════════════════════════════

"MAT.5.3.CEBIR": {
    "unite": "Cebir",
    "baslik": "Cebirsel Ifadeler ve Denklemler",
    "icerik": """
ORUNTU (PATTERN):
Tanim: Belirli bir kurala gore tekrarlanan veya degisen yapilar.
- Sayi oruntusu: 2, 4, 6, 8, ... (kurali: +2)
- Sekil oruntusu: Geometrik sekillerin belirli kurala gore tekrari
- Oruntunun kuralini bulma: Ardisik terimler arasindaki iliskiyi belirleme

DEGISKEN:
- Bilinmeyen veya degisen bir sayiyi temsil eden harf
- Genellikle x, y, n, a gibi harfler kullanilir
- Ornek: "Bir sayinin 3 kati" → 3 × x veya 3x

CEBIRSEL IFADE:
- Sayi ve degiskenlerden olusan matematiksel ifade
- Ornekler:
  * 2x + 3 (x'in 2 kati arti 3)
  * 5n - 7 (n'in 5 kati eksi 7)
  * a/4 + 1 (a'nin 4'te biri arti 1)

ESITLIK VE DENKLEM:
- Esitlik: Iki ifadenin birbirine esit oldugunu gosteren matematiksel cumle
- Denklem: Icinde bilinmeyen (degisken) bulunan esitlik
- Ornek: x + 5 = 12 (x kac?)
  Cozum: x = 12 - 5 = 7

DENKLEM COZME:
- Ters islem yontemi:
  * Toplama ↔ Cikarma (tersi)
  * Carpma ↔ Bolme (tersi)
- x + 7 = 15 → x = 15 - 7 = 8
- x - 3 = 10 → x = 10 + 3 = 13
- 4x = 20 → x = 20 ÷ 4 = 5
- x/3 = 6 → x = 6 × 3 = 18

ESITLIGIN OZELLIKLERI:
- Her iki tarafa ayni sayi eklenir/cikarilir → esitlik bozulmaz
- Her iki taraf ayni sayiyla carpilir/bolunur → esitlik bozulmaz
- Ornek: x + 3 = 10 → her iki taraftan 3 cikar → x = 7
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.5.4.VERI": {
    "unite": "Veri Isleme",
    "baslik": "Veri Toplama, Duzenleme ve Yorumlama",
    "icerik": """
VERI TOPLAMA:
- Anket: Sorular hazirlayarak bilgi toplama
- Gozlem: Dogrudan izleyerek veri elde etme
- Deney: Kontrollü kosullarda veri toplama
- Kaynak tarama: Mevcut verilerden yararlanma

VERI DUZENLEME:
1. Sıklık tablosu (frekans tablosu):
   - Verilerin kac kez tekrarlandigini gosteren tablo
   - Ornek: Siniftaki ogrencilerin goz renkleri

2. Stem-and-leaf (gövde-yaprak) gösterimi:
   - Verileri basamak degerlerine gore gruplama

GRAFIK TURLERI:

1. Sutun grafigi (Bar chart):
   - Kategorik verileri gostermek icin
   - Yatay eksen: Kategoriler
   - Dikey eksen: Degerler (frekans, miktar)
   - Sutunlar arasinda bosluk bulunur

2. Cizgi grafigi (Line chart):
   - Zamana bagli degisimi gostermek icin
   - Noktalar cizgiyle birlestirilir
   - Artis ve azalis egilimleri gorulur

3. Daire (pasta) grafigi (Pie chart):
   - Bir butunun parcalarini gostermek icin
   - Tam daire = %100 = 360°
   - Her dilimin buyuklugu oranıyla orantilidir

ORTALAMA (ARITMETIK ORTALAMA):
- Tum degerlerin toplami / deger sayisi
- Ornek: 70, 80, 90, 60, 100 → Ortalama = (70+80+90+60+100) / 5 = 400/5 = 80

ORTANCA (MEDYAN):
- Veriler kucukten buyuge siralandiginda ortadaki deger
- Tek sayida veri: Ortadaki deger
- Cift sayida veri: Ortadaki iki degerin ortalamasi
- Ornek: 3, 5, 7, 9, 11 → Ortanca = 7

TEPE DEGER (MOD):
- En cok tekrarlanan deger
- Ornek: 3, 5, 5, 7, 5, 9 → Tepe deger = 5

ARALIK (RANGE):
- En buyuk deger - En kucuk deger
- Ornek: 3, 5, 7, 9, 11 → Aralik = 11 - 3 = 8
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik5_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_5_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik5_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_5_REFERANS.keys())
