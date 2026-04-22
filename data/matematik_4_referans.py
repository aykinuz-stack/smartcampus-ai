# -*- coding: utf-8 -*-
"""
4. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme Alanlari:
1. Sayilar ve Islemler (dogal sayilar, dort islem, kesirler, ondalik gosterim)
2. Geometri (acılar, ucgen-dortgen, cevre-alan, simetri)
3. Olcme (uzunluk, alan, hacim, zaman)
4. Veri Isleme (grafik, tablo)
5. Oruntu ve Iliski
"""

MATEMATIK_4_REFERANS = {

# =====================================================================
# 1. OGRENME ALANI: SAYILAR VE ISLEMLER
# =====================================================================

"MAT.4.1.DOGAL_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Dogal Sayilar - 6 ve Daha Fazla Basamakli Sayilar",
    "icerik": """
DOGAL SAYILAR:
0, 1, 2, 3, 4, ... seklinde devam eden sayilara dogal sayilar denir.
En kucuk dogal sayi 0'dir. En buyuk dogal sayi yoktur (sonsuz).

BASAMAK VE BOLUKLERI (6+ basamak):

1. BASAMAK KAVRAMLARI:
   - Birler basamagi, Onlar basamagi, Yuzler basamagi
   - Binler basamagi, On binler basamagi, Yuz binler basamagi
   - Milyonlar basamagi (7. basamak)

2. BOLUKLER:
   - Birler bolugu: Birler, Onlar, Yuzler
   - Binler bolugu: Binler, On binler, Yuz binler
   - Milyonlar bolugu: Milyonlar, On milyonlar, Yuz milyonlar

3. ORNEK: 543.216 sayisi
   - 5 → Yuz binler basamaginda (basamak degeri: 500.000)
   - 4 → On binler basamaginda (basamak degeri: 40.000)
   - 3 → Binler basamaginda (basamak degeri: 3.000)
   - 2 → Yuzler basamaginda (basamak degeri: 200)
   - 1 → Onlar basamaginda (basamak degeri: 10)
   - 6 → Birler basamaginda (basamak degeri: 6)

4. OKUMA VE YAZMA:
   - 543.216 → "Bes yuz kirk uc bin iki yuz on alti"
   - 1.000.000 → "Bir milyon"
   - Sayilar saga dogru ucerli gruplara ayrilir (nokta ile)

5. SIRALAMA VE KARSILASTIRMA:
   - Basamak sayisi fazla olan sayi buyuktur: 10.000 > 9.999
   - Basamak sayilari esitse soldan saga basamak degerleri karsilastirilir
   - Kucukten buyuge: < / Buyukten kucuge: >
   - Ornek: 456.789 < 465.789 (on binler basamagi karsilastirilir: 5 < 6)

6. YUVARLATMA:
   - Onluga: Birler 0-4 ise asagi, 5-9 ise yukari → 547 ≈ 550
   - Yuzluge: Onlar 0-4 ise asagi, 5-9 ise yukari → 547 ≈ 500
   - Binlige: Yuzler 0-4 ise asagi, 5-9 ise yukari → 2.547 ≈ 3.000
"""
},

"MAT.4.1.DORT_ISLEM": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Dort Islem - Buyuk Sayilarla Toplama, Cikarma, Carpma, Bolme",
    "icerik": """
DORT ISLEM (buyuk sayilarla):

1. TOPLAMA:
   - Ayni basamaktaki rakamlar alt alta yazilir
   - Sagdan sola (birler basamagindan) baslanir
   - Toplam 10 veya daha buyukse elde vardir
   - Ornek: 34.567 + 28.945 = 63.512
   - Toplama degisme ozelligi: a + b = b + a
   - Toplama birleme ozelligi: (a + b) + c = a + (b + c)
   - Etkisiz eleman: a + 0 = a

2. CIKARMA:
   - Ayni basamaktaki rakamlar alt alta yazilir
   - Sagdan sola baslanir
   - Ust basamak kucukse komsu basamaktan 1 onluk (10) alinir
   - Ornek: 50.000 - 23.467 = 26.533
   - Cikarma degisme ozelligine SAHIP DEGILDIR: a - b ≠ b - a

3. CARPMA:
   - Bir basamakli ile carpma: 4.523 × 7 = 31.661
   - Iki basamakli ile carpma: 345 × 26
     345 × 6 = 2.070
     345 × 20 = 6.900
     Toplam = 8.970
   - Carpma degisme ozelligi: a × b = b × a
   - Carpma birleme ozelligi: (a × b) × c = a × (b × c)
   - Etkisiz eleman: a × 1 = a
   - Yutan eleman: a × 0 = 0
   - Dagılma ozelligi: a × (b + c) = a×b + a×c

4. BOLME:
   - Bolunen ÷ Bolen = Bolum (kalan varsa + Kalan)
   - Bolunen = (Bolen × Bolum) + Kalan
   - Kalan her zaman bolenden kucuktur
   - Ornek: 7.354 ÷ 6 = 1.225 kalan 4
   - Sifira bolme tanimsizdir (yapilamaz!)

5. ISLEM ONCELIGI:
   - Parantez icindeki islem once yapilir
   - Carpma ve bolme, toplama ve cikarmadan once yapilir
   - Ayni oncelige sahip islemler soldan saga yapilir
   - Ornek: 3 + 4 × 2 = 3 + 8 = 11 (carpma once!)
   - Ornek: (3 + 4) × 2 = 7 × 2 = 14 (parantez once!)

6. ZIHINDEN ISLEM STRATEJILERI:
   - Kolay sayiya yuvarla, islem yap, farki duzelt
   - 99 + 47 = 100 + 47 - 1 = 146
   - 25 × 12 = 25 × 4 × 3 = 100 × 3 = 300
"""
},

"MAT.4.1.KESIRLER": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Kesirler - Toplama, Cikarma, Denk Kesir, Siralama",
    "icerik": """
KESIR NEDIR?
Bir butunun esit parcalara bolunmesiyle elde edilen parcayi gosteren sayidir.

KESIR GOSTERIMI:
   Pay
  ─────  → Pay: Alinan parca sayisi / Payda: Butunun bolundugu esit parca sayisi
  Payda

KESIR CESITLERI:
1. Basit kesir: Pay < Payda → 3/4, 2/5, 1/8
2. Bilesik kesir: Pay > Payda → 5/3, 7/4, 9/2
3. Tam sayili kesir: 1 3/4, 2 1/2

DONUSUMLER:
- Bilesik → Tam sayili: 7/4 = 1 3/4 (7÷4 = 1 kalan 3)
- Tam sayili → Bilesik: 2 1/3 = (2×3+1)/3 = 7/3

DENK (ESIT) KESIRLER:
- Pay ve paydasi ayni sayiyla carpilan veya bolunen kesirler denktir
- 1/2 = 2/4 = 3/6 = 4/8 (hepsi ayni degeri gosterir)
- Sadesletirme: Pay ve payda ortak bolene bolunur → 6/8 = 3/4

PAYDASI ESIT KESIRLERDE TOPLAMA:
- Paydalar ayni kalir, paylar toplanir
- 2/7 + 3/7 = 5/7
- Ornek: 1/5 + 3/5 = 4/5

PAYDASI ESIT KESIRLERDE CIKARMA:
- Paydalar ayni kalir, paylar cikarilir
- 5/8 - 2/8 = 3/8
- Ornek: 4/6 - 1/6 = 3/6 = 1/2

PAYDASI FARKLI KESIRLERDE TOPLAMA-CIKARMA:
- Oncelikle paydalari esitle (EKOK bul)
- 1/2 + 1/3 → payda EKOK(2,3) = 6 → 3/6 + 2/6 = 5/6
- 3/4 - 1/3 → payda EKOK(4,3) = 12 → 9/12 - 4/12 = 5/12

KESIRLERI SIRALAMA:
- Paydalari esit ise: Payi buyuk olan buyuktur → 3/5 > 2/5
- Paylari esit ise: Paydasi kucuk olan buyuktur → 1/3 > 1/5
- Genel: Paydalari esitle, sonra karsilastir

KESIRLERDE TAM SAYILI ISLEMLER:
- 2 1/4 + 1 2/4 = (2+1) + (1/4 + 2/4) = 3 3/4
- 3 3/5 - 1 1/5 = (3-1) + (3/5 - 1/5) = 2 2/5
"""
},

"MAT.4.1.ONDALIK_GOSTERIM": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Ondalik Gosterim - Kesir ile Ondalik Iliski",
    "icerik": """
ONDALIK GOSTERIM NEDIR?
Paydasi 10, 100, 1000 gibi 10'un kuvvetleri olan kesirlerin
virgul kullanilarak yazilma bicimi.

KESIRDEN ONDALIGA DONUSUM:
- 1/10 = 0,1 (onda bir)
- 3/10 = 0,3 (onda uc)
- 7/10 = 0,7 (onda yedi)
- 1/100 = 0,01 (yuzde bir)
- 23/100 = 0,23 (yuzde yirmi uc)
- 1/2 = 5/10 = 0,5
- 1/4 = 25/100 = 0,25
- 3/4 = 75/100 = 0,75

ONDALIK SAYI OKUMA:
- 0,3 → "Sifir tam onda uc"
- 2,5 → "Iki tam onda bes"
- 0,07 → "Sifir tam yuzde yedi"
- 3,14 → "Uc tam yuzde on dort"

BASAMAK DEGERLERI:
   Birler , Onda birler   Yuzde birler
     3   ,      1              4         → 3,14

ONDALIK SAYILARI SIRALAMA:
- Once tam kisim karsilastirilir
- Tam kisimlar esitse ondalik kisim karsilastirilir
- 2,7 > 2,3 (tam kisimlar esit, 7 > 3)
- 3,1 > 2,9 (3 > 2)

ONDALIK SAYILARDA TOPLAMA-CIKARMA:
- Virgullar alt alta gelecek sekilde yazilir
- Birler, onlar gibi basamak basamak islem yapilir
- 2,4 + 1,3 = 3,7
- 5,8 - 2,5 = 3,3
"""
},

# =====================================================================
# 2. OGRENME ALANI: GEOMETRI
# =====================================================================

"MAT.4.2.ACILAR_UCGEN_DORTGEN": {
    "unite": "Geometri",
    "baslik": "Acilar, Ucgen ve Dortgen Ozellikleri",
    "icerik": """
ACI CESITLERI:
1. Dar aci: 0° ile 90° arasi (ornek: 45°, 30°, 60°)
2. Dik aci: Tam 90° (kare sembolüyle gösterilir)
3. Genis aci: 90° ile 180° arasi (ornek: 120°, 150°)
4. Dogru aci: Tam 180°

ACI OLCME:
- Iletki (aciolcer) kullanilir
- Birimi derece (°)
- Iletkinin merkezi acinin kosesine, taban cizgisi acinin bir koluna yerlestirilir

UCGEN:
Tanim: Uc dogru parcasinin birlestirilmesiyle olusan kapalı sekil.
Ozellikleri:
- 3 kenar, 3 kose, 3 ic aci
- Ic acilari toplami = 180°

Kenar uzunluklarina gore:
a) Eskenar ucgen: Uc kenari da esit. Tum acilari 60°.
b) Ikizkenar ucgen: Iki kenari esit. Esit kenarlarin karsisindaki acilar da esit.
c) Cesitkenar ucgen: Uc kenari da farkli uzunlukta.

Acilarina gore:
a) Dar acili ucgen: Tum acilari 90°'den kucuk
b) Dik acili ucgen: Bir acisi 90° (dik aci)
c) Genis acili ucgen: Bir acisi 90°'den buyuk

DORTGEN:
Tanim: Dort dogru parcasinin birlestirilmesiyle olusan kapalı sekil.
Ozellikleri:
- 4 kenar, 4 kose, 4 ic aci
- Ic acilari toplami = 360°

Ozel dortgenler:
a) Kare:
   - 4 kenar esit, 4 aci dik (90°)
   - Kosegenleri esit ve birbirini dik keser
b) Dikdortgen:
   - Karsilikli kenarlar esit, 4 aci dik (90°)
   - Kosegenleri esit
c) Paralelkenar:
   - Karsilikli kenarlar paralel ve esit
   - Karsilikli acilar esit
d) Eskenar dortgen:
   - 4 kenar esit
   - Karsilikli acilar esit, kosegenleri birbirini dik keser

UCGEN KURALI (4. sinif):
- Herhangi iki kenar uzunlugu toplami ucuncu kenardan buyuk olmalidir.
- Ornek: 3, 4, 8 kenarli ucgen CIZILEMEZ cunku 3 + 4 = 7 < 8
"""
},

"MAT.4.2.CEVRE_ALAN_SIMETRI": {
    "unite": "Geometri",
    "baslik": "Cevre ve Alan Hesaplama, Simetri",
    "icerik": """
CEVRE NEDIR?
Bir seklin dis kenarlari boyunca olculen toplam uzunluktur.

CEVRE FORMULLERI:
1. Kare: Cevre = 4 × kenar = 4a
   - Ornek: Kenari 5 cm olan karenin cevresi = 4 × 5 = 20 cm
2. Dikdortgen: Cevre = 2 × (uzun kenar + kisa kenar) = 2 × (a + b)
   - Ornek: 6 cm ve 4 cm kenarlı dikdortgenin cevresi = 2 × (6+4) = 20 cm
3. Ucgen: Cevre = kenar1 + kenar2 + kenar3
   - Ornek: 3 cm, 4 cm, 5 cm kenarlı ucgenin cevresi = 3+4+5 = 12 cm

ALAN NEDIR?
Bir seklin kapladigi yuzey buyuklugudur. Birimi kare birimdir (cm², m²).

ALAN FORMULLERI:
1. Kare: Alan = kenar × kenar = a²
   - Ornek: Kenari 5 cm olan karenin alani = 5 × 5 = 25 cm²
2. Dikdortgen: Alan = uzun kenar × kisa kenar = a × b
   - Ornek: 6 cm ve 4 cm kenarli dikdortgenin alani = 6 × 4 = 24 cm²

CEVRE-ALAN ILISKISI:
- Cevre uzunluk birimiyle (cm, m), alan ise kare birimle (cm², m²) olculur
- Ayni cevreye sahip farkli sekillerin alanlari farkli olabilir
- Kare, ayni cevreye sahip dikdortgenlerden daha buyuk alana sahiptir

SIMETRI:
Tanim: Bir seklin bir dogru boyunca katlandiginda iki parcasinin birebir ust uste gelmesi.

Simetri ekseni (simetri dogrusu):
- Kare: 4 simetri ekseni (2 kosegen + 2 kenar ortay)
- Dikdortgen: 2 simetri ekseni (kenar ortaylari)
- Eskenar ucgen: 3 simetri ekseni
- Ikizkenar ucgen: 1 simetri ekseni
- Daire: Sonsuz simetri ekseni

Simetri ozellikleri:
- Simetrik iki nokta, simetri eksenine esit uzakliktadir
- Aynasal yansima simetri orneklerinden biridir
- Dogada simetri: kelebek kanatlari, insan yüzü, yapraklar
"""
},

# =====================================================================
# 3. OGRENME ALANI: OLCME
# =====================================================================

"MAT.4.3.OLCME_BIRIMLERI": {
    "unite": "Olcme",
    "baslik": "Uzunluk, Alan, Hacim Birimleri ve Zaman",
    "icerik": """
1. UZUNLUK OLCULERI:
   km → m → dm → cm → mm

   Donusumler (her biri 10 kat):
   - 1 km = 1.000 m
   - 1 m = 10 dm = 100 cm = 1.000 mm
   - 1 dm = 10 cm = 100 mm
   - 1 cm = 10 mm

   Ornekler:
   - 3 km 500 m = 3.500 m
   - 2 m 45 cm = 245 cm
   - 150 cm = 1 m 50 cm

2. ALAN OLCULERI:
   - 1 m² = 10.000 cm² (100 × 100)
   - 1 dm² = 100 cm²
   - 1 cm² = 100 mm²
   - Alan olculerinde bir basamak = 100 kat (iki sifir)

3. HACIM VE SIVI OLCULERI:
   - 1 litre (L) = 1.000 mililitre (mL)
   - 1 litre = 1 dm³
   - Yarim litre = 500 mL
   - Ceyrek litre = 250 mL

   Ornekler:
   - 2 L 300 mL = 2.300 mL
   - 3.750 mL = 3 L 750 mL

4. KUTLE (AGIRLIK) OLCULERI:
   - 1 ton = 1.000 kg
   - 1 kg = 1.000 g
   - 1 g = 1.000 mg
   - Yarim kg = 500 g
   - Ceyrek kg = 250 g

5. ZAMAN OLCULERI:
   - 1 yil = 12 ay = 365 gun (artik yil 366)
   - 1 ay = 28/29/30/31 gun
   - 1 hafta = 7 gun
   - 1 gun = 24 saat
   - 1 saat = 60 dakika
   - 1 dakika = 60 saniye
   - 1 saat = 3.600 saniye

   Zaman hesaplama:
   - 3 saat 45 dk + 2 saat 30 dk = 6 saat 15 dk
   - 5 saat 20 dk - 2 saat 40 dk = 4 saat 80 dk - 2 saat 40 dk = 2 saat 40 dk
     (60 dk bosanan 1 saat: 5 saat 20 dk = 4 saat 80 dk)

6. PARA:
   - 1 TL = 100 kurus
   - Madeni paralar: 5 kr, 10 kr, 25 kr, 50 kr, 1 TL
   - Kagit paralar: 5 TL, 10 TL, 20 TL, 50 TL, 100 TL, 200 TL
"""
},

# =====================================================================
# 4. OGRENME ALANI: VERI ISLEME
# =====================================================================

"MAT.4.4.VERI_GRAFIK": {
    "unite": "Veri Isleme",
    "baslik": "Veri Toplama, Tablo ve Grafik (Sutun, Cizgi)",
    "icerik": """
VERI TOPLAMA VE DUZENLEME:

1. VERI TOPLAMA YONTEMLERI:
   - Sayma (siklik tablosu)
   - Anket / Sorusturma
   - Gozlem

2. SIKLIK TABLOSU:
   - Verilerin kac kez tekrar ettigini gosterir
   - Cizgi sayma yontemi: Her veri icin bir cizgi, 5. cizgi capraz

   Ornek:
   Meyve     | Cizgi    | Siklik
   Elma      | IIII I   | 6
   Armut     | III      | 3
   Cilek     | IIII     | 4
   Uzum      | II       | 2

3. SUTUN GRAFIGI (CUBUK GRAFIGI):
   - Verileri dikdortgen sutunlarla gosterir
   - Yatay eksen: Kategoriler (meyve turleri)
   - Dikey eksen: Degerler (sayilar)
   - Sutunlarin yuksekligi degeri gosterir
   - Karsilastirma yapmak icin idealdir
   - Sutunlar esit aralikli ve esit genislikte olmalidir

4. CIZGI GRAFIGI:
   - Verinin zamana gore degisimini gosterir
   - Noktalar isaretlenir, cizgiyle birlestirilir
   - Artis, azalis ve sabit kalma durumlarini gosterir
   - Ornek: Haftalik sicaklik degisimi, aylik kitap okuma sayisi

5. GRAFIKTEN BILGI OKUMA:
   - En buyuk ve en kucuk degeri bulma
   - Iki kategori arasindaki farki hesaplama
   - Toplam degeri bulma
   - Artis/azalis yorumu yapma

6. ORTALAMA (ARITMETIK ORTALAMA):
   - Tum degerlerin toplami / deger sayisi
   - Ornek: 8, 6, 10, 4, 7 → Toplam = 35, Sayi = 5, Ortalama = 35÷5 = 7
"""
},

# =====================================================================
# 5. OGRENME ALANI: ORUNTU VE ILISKI
# =====================================================================

"MAT.4.5.ORUNTU": {
    "unite": "Oruntu ve Iliski",
    "baslik": "Sayi Oruntusu ve Geometrik Oruntu",
    "icerik": """
ORUNTU NEDIR?
Belirli bir kurala gore tekrar eden veya degisen yapidir.

1. SAYI ORUNTULERI:
   a) Toplama ile olusanlar:
      - 3, 6, 9, 12, 15, ... (kural: +3)
      - 5, 10, 15, 20, 25, ... (kural: +5)
      - 2, 5, 8, 11, 14, ... (kural: +3)

   b) Cikarma ile olusanlar:
      - 100, 90, 80, 70, 60, ... (kural: -10)
      - 50, 45, 40, 35, 30, ... (kural: -5)

   c) Carpma ile olusanlar:
      - 2, 4, 8, 16, 32, ... (kural: ×2)
      - 3, 9, 27, 81, ... (kural: ×3)

   d) Karisik oruntuler:
      - 1, 2, 4, 7, 11, ... (kural: +1, +2, +3, +4 artan fark)
      - 1, 1, 2, 3, 5, 8, ... (onceki ikisinin toplami - Fibonacci benzeri)

2. GEOMETRIK ORUNTULER:
   - Sekillerin belirli bir duzenle tekrar etmesi
   - Ornek: ○ □ △ ○ □ △ ○ □ △ ... (uc sekil tekrar ediyor)
   - Ornek: Her adimda bir kare eklenen merdiven deseni

3. ORUNTU KURALI BULMA:
   - Ardisik terimler arasindaki farki/orani hesapla
   - 4, 7, 10, 13, ? → Fark: 3, 3, 3 → Kural: +3 → Sonraki: 16
   - 2, 6, 18, 54, ? → Oran: ×3 → Sonraki: 162

4. TABLO ILE ORUNTU:
   Adim  | Kibrit sayisi
   1     | 4
   2     | 7
   3     | 10
   4     | 13
   Kural: 3n + 1 (her adimda 3 kibrit eklenir)

5. ORUNTU VE GUNLUK HAYAT:
   - Takvimde gunlerin tekrari (7 gunluk oruntu)
   - Mevsimlerin dongusu (4 mevsim)
   - Fayans, duvar kagidi, kumas desenleri
"""
},

}

# =====================================================================
# YARDIMCI FONKSIYONLAR
# =====================================================================

def get_matematik4_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_4_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik4_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_4_REFERANS.keys())
