# -*- coding: utf-8 -*-
"""
3. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme alanlari:
1. Sayilar ve Islemler (Dogal Sayilar 0-10000, Carpma, Bolme, Kesirler, Ondalik Giris)
2. Geometri (Cokgenler, Simetri, Cevre, Alan Giris)
3. Olcme (Tartma, Sivi Olcme, Zaman)
4. Veri Isleme (Cizgi Grafik)
"""

MATEMATIK_3_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. DOGAL SAYILAR 0-10000
# ═══════════════════════════════════════════════════════════════

"MAT.3.1.DOGAL_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Dogal Sayilar 0-10000",
    "icerik": """
DOGAL SAYILAR:
3. sinifta dogal sayilar 0'dan 10.000'e kadar genisletilir.

BASAMAK KAVRAMI:
- Birler basamagi: En sagdaki rakam (1, 2, 3...)
- Onlar basamagi: Sagdan ikinci rakam (10, 20, 30...)
- Yuzler basamagi: Sagdan ucuncu rakam (100, 200, 300...)
- Binler basamagi: Sagdan dorduncu rakam (1000, 2000, 3000...)

BASAMAK DEGERI:
- 4.567 sayisinda:
  * 4 → binler basamaginda → 4 × 1000 = 4000
  * 5 → yuzler basamaginda → 5 × 100 = 500
  * 6 → onlar basamaginda → 6 × 10 = 60
  * 7 → birler basamaginda → 7 × 1 = 7
  * 4000 + 500 + 60 + 7 = 4567

SAYILARI OKUMA VE YAZMA:
- 3.456 → Uc bin dort yuz elli alti
- 7.089 → Yedi bin seksen dokuz
- 10.000 → On bin

SAYILARI KARSILASTIRMA:
- Basamak sayisi fazla olan buyuktur: 1.000 > 999
- Basamak sayisi ayniysa soldan saga karsilastirilir:
  4.567 ve 4.589 → Binler ayni (4), yuzler ayni (5), onlar: 6 < 8 → 4.567 < 4.589
- Isaret: < (kucuktur), > (buyuktur), = (esittir)

SIRALAMA:
- Kucukten buyuge: 234, 567, 890, 1.234, 5.678
- Buyukten kucuge: 5.678, 1.234, 890, 567, 234

SAYILARLA TOPLAMA VE CIKARMA:
- Dort basamakli sayilarla toplama: 2.345 + 1.234 = 3.579
- Dort basamakli sayilarla cikarma: 5.678 - 2.345 = 3.333
- Eldeli toplama ve onluk bozma ile cikarma islemleri
- Zihinden toplama ve cikarma stratejileri:
  * Yuvarlama: 298 + 145 ≈ 300 + 145 = 445, sonra 2 cikar → 443
  * Parçalama: 345 + 228 = 300 + 200 + 40 + 20 + 5 + 8 = 573
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. CARPMA
# ═══════════════════════════════════════════════════════════════

"MAT.3.2.CARPMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Carpma Islemi ve Carpim Tablosu",
    "icerik": """
CARPMA ISLEMI:
Tekrarli toplamanin kisa yoludur.
3 + 3 + 3 + 3 = 4 × 3 = 12

CARPIM TABLOSU (3. SINIFTA TAM OGRENILIR):
1 × 1 = 1    2 × 1 = 2    3 × 1 = 3    4 × 1 = 4    5 × 1 = 5
1 × 2 = 2    2 × 2 = 4    3 × 2 = 6    4 × 2 = 8    5 × 2 = 10
1 × 3 = 3    2 × 3 = 6    3 × 3 = 9    4 × 3 = 12   5 × 3 = 15
1 × 4 = 4    2 × 4 = 8    3 × 4 = 12   4 × 4 = 16   5 × 4 = 20
1 × 5 = 5    2 × 5 = 10   3 × 5 = 15   4 × 5 = 20   5 × 5 = 25
1 × 6 = 6    2 × 6 = 12   3 × 6 = 18   4 × 6 = 24   5 × 6 = 30
1 × 7 = 7    2 × 7 = 14   3 × 7 = 21   4 × 7 = 28   5 × 7 = 35
1 × 8 = 8    2 × 8 = 16   3 × 8 = 24   4 × 8 = 32   5 × 8 = 40
1 × 9 = 9    2 × 9 = 18   3 × 9 = 27   4 × 9 = 36   5 × 9 = 45
1 × 10 = 10  2 × 10 = 20  3 × 10 = 30  4 × 10 = 40  5 × 10 = 50

6 × 6 = 36   7 × 6 = 42   8 × 6 = 48   9 × 6 = 54
6 × 7 = 42   7 × 7 = 49   8 × 7 = 56   9 × 7 = 63
6 × 8 = 48   7 × 8 = 56   8 × 8 = 64   9 × 8 = 72
6 × 9 = 54   7 × 9 = 63   8 × 9 = 72   9 × 9 = 81
6 × 10 = 60  7 × 10 = 70  8 × 10 = 80  9 × 10 = 90

CARPMANIN OZELLIKLERI (3. SINIF):
- Degisme ozelligi: 3 × 5 = 5 × 3 = 15
- 1 ile carpma: 7 × 1 = 7 (sayinin kendisi)
- 0 ile carpma: 7 × 0 = 0 (sonuc her zaman 0)
- 10 ile carpma: 7 × 10 = 70 (sona sifir eklenir)

IKI BASAMAKLI SAYILARLA CARPMA:
- 23 × 4 = (20 × 4) + (3 × 4) = 80 + 12 = 92
- 15 × 6 = (10 × 6) + (5 × 6) = 60 + 30 = 90
- Altalta carpma yontemi ogretilir

CARPMA ILE PROBLEM COZME:
- "Her kutuda 6 elma var. 4 kutu var. Toplam kac elma?" → 4 × 6 = 24 elma
- "5 rafta 8'er kitap var. Toplam kac kitap?" → 5 × 8 = 40 kitap
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. BOLME
# ═══════════════════════════════════════════════════════════════

"MAT.3.3.BOLME": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Bolme Islemi ve Kalanli Bolme",
    "icerik": """
BOLME ISLEMI:
Bir sayiyi esit gruplara ayirma islemidir.
Carpmanin tersi islemidir: 4 × 3 = 12 → 12 ÷ 3 = 4

BOLME TERIMLERI:
- Bolunen: Bolunecek sayi (12)
- Bolen: Kaca bolunecegi (3)
- Bolum: Sonuc (4)
- Kalan: Artan miktar (kalanli bolmede)

TAM BOLME:
- 12 ÷ 3 = 4 (kalan 0)
- 20 ÷ 5 = 4 (kalan 0)
- 36 ÷ 6 = 6 (kalan 0)
- 81 ÷ 9 = 9 (kalan 0)

KALANLI BOLME:
- 13 ÷ 3 = 4, kalan 1 (cunku 4 × 3 = 12, artan 13 - 12 = 1)
- 17 ÷ 5 = 3, kalan 2 (cunku 3 × 5 = 15, artan 17 - 15 = 2)
- 25 ÷ 4 = 6, kalan 1 (cunku 6 × 4 = 24, artan 25 - 24 = 1)

KALANLI BOLME KURALLARI:
- Kalan her zaman bolenden KUCUKTUR
- Kontrol: (Bolum × Bolen) + Kalan = Bolunen
  Ornek: 17 ÷ 5 = 3, kalan 2 → (3 × 5) + 2 = 15 + 2 = 17 ✓

BOLMENIN OZELLIKLERI:
- Bir sayi kendisine bolunurse sonuc 1'dir: 8 ÷ 8 = 1
- Bir sayi 1'e bolunurse kendisi olur: 8 ÷ 1 = 8
- 0 herhangi bir sayiya bolunurse sonuc 0'dir: 0 ÷ 5 = 0
- Bir sayi 0'a BOLUNEMEZ (tanimsiz)

CARPMA-BOLME ILISKISI:
- 5 × 6 = 30 → 30 ÷ 5 = 6 ve 30 ÷ 6 = 5
- Carpim tablosunu bilmek bolmeyi kolaylastirir

PROBLEM COZME:
- "24 elmayı 6 cocuga esit bolersek her cocuga kac elma duser?" → 24 ÷ 6 = 4 elma
- "25 ogrenci 4'erli gruplara ayrilirsa kac grup olur, kac kisi kalir?" → 25 ÷ 4 = 6 grup, 1 kisi kalir
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. KESIRLER
# ═══════════════════════════════════════════════════════════════

"MAT.3.4.KESIRLER": {
    "unite": "Sayilar ve Nicelikler",
    "baslik": "Kesirler - Birim Kesir ve Denk Kesir",
    "icerik": """
KESIR KAVRAMI (3. SINIF GIRIS):
Bir butunun esit parcalara bolunmesinde her parcayi gosterir.
- Pay: Alinan parca sayisi (ustteki sayi)
- Payda: Butunun kac esit parcaya bolundugu (alttaki sayi)

BIRIM KESIR:
Payi 1 olan kesirlerdir. Bir butunun esit parcalarindan birini gosterir.
- 1/2 → yarim (butun 2 esit parcaya bolunmus, 1 parca alinmis)
- 1/3 → ucte bir
- 1/4 → dortte bir (ceyrek)
- 1/5 → beste bir
- 1/6 → altida bir
- 1/8 → sekizde bir
- 1/10 → onda bir

BIRIM KESIR SIRALAMA:
- Paydasi kucuk olan birim kesir buyuktur:
  1/2 > 1/3 > 1/4 > 1/5 > 1/6 > 1/8 > 1/10
- Aciklama: Bir pizzayi 2'ye bolmek, 8'e bolmekten daha buyuk parcalar verir

BASIT KESIRLER (3. SINIF):
- 2/3 → ucte iki
- 3/4 → dortte uc
- 2/5 → beste iki
- 5/6 → altida bes

DENK KESIRLER (GIRIS):
Ayni buyuklugu gosteren farkli kesirler:
- 1/2 = 2/4 = 3/6 = 4/8
  (Bir pizzanin yarisi = 4 dilimden 2'si = 6 dilimden 3'u = 8 dilimden 4'u)
- 1/3 = 2/6
- 2/4 = 1/2 (sadeleştirme)

DENK KESIR BULMA:
- Pay ve payda ayni sayiyla carpilir:
  1/2 → pay ve payda 2 ile carpilir → 2/4
  1/3 → pay ve payda 3 ile carpilir → 3/9
- Pay ve payda ayni sayiyla bolunur (sadeleştirme):
  4/8 → pay ve payda 4 ile bolunur → 1/2

ONDALIK GOSTERIM GIRIS (3. SINIF):
- 1/2 = 0,5 (yarim)
- 1/4 = 0,25 (ceyrek)
- 3/4 = 0,75
- 1/10 = 0,1
- Parayla iliskilendirme: 1 TL = 100 kurus, 50 kurus = 0,50 TL = 1/2 TL

KESIRLERLE GUNLUK HAYAT:
- Yarim ekmek (1/2), ceyrek saat (1/4 saat = 15 dakika)
- Pizzanin 3/8'i, pastanin 1/4'u
- Saatin ceyregi (1/4), yarisi (1/2)
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. GEOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.3.5.GEOMETRI": {
    "unite": "Geometri",
    "baslik": "Geometrik Sekiller, Simetri, Cevre ve Alan Girisi",
    "icerik": """
COKGENLER:
Dogru parcalariyla cevrili kapali sekillerdir.

COKGEN TURLERI:
- Ucgen: 3 kenari, 3 kosesi var
- Dortgen: 4 kenari, 4 kosesi var (kare, dikdortgen, yamuk...)
- Besgen: 5 kenari, 5 kosesi var
- Altigen: 6 kenari, 6 kosesi var

KARE:
- 4 kenari esit uzunlukta
- 4 acisi dik aci (90°)
- Ornek: Satranc tahtasinin kareleri

DIKDORTGEN:
- Karsi kenarlari esit uzunlukta
- 4 acisi dik aci (90°)
- Ornek: Kitap, defter, kapi

UCGEN:
- 3 kenari olan cokgen
- Kenarlarina gore: eskenar, ikizkenar, cesitkenar
- 3. sinifta genel tanitim yapilir

DAIRE VE CEMBER:
- Cember: Bir noktaya esit uzakliktaki noktalarin olusturdugu egri
- Daire: Cember ve icteki bolge birlikte
- Merkez, yaricap, cap kavramlari

SIMETRI:
Tanim: Bir seklin bir dogru boyunca katlandiginda iki yarisi birbiriyle cakisiyorsa, o sekil simetriktir.
- Simetri dogrusu (ekseni): Sekli iki esit parcaya ayiran dogru
- Kare: 4 simetri ekseni var
- Dikdortgen: 2 simetri ekseni var
- Eskenar ucgen: 3 simetri ekseni var
- Daire: Sonsuz simetri ekseni var
- Gunluk hayat ornekleri: kelebek, yuz, yaprak

CEVRE HESAPLAMA:
Bir seklin disindaki kenarlarin toplam uzunlugu.

- Karenin cevresi: 4 × kenar = 4a
  Ornek: Kenari 5 cm olan kare → Cevre = 4 × 5 = 20 cm

- Dikdortgenin cevresi: 2 × (uzun kenar + kisa kenar) = 2 × (a + b)
  Ornek: Kenarlari 6 cm ve 4 cm → Cevre = 2 × (6 + 4) = 20 cm

- Ucgenin cevresi: kenar1 + kenar2 + kenar3
  Ornek: Kenarlari 3, 4, 5 cm → Cevre = 3 + 4 + 5 = 12 cm

ALAN KAVRAMINA GIRIS:
- Alan: Bir seklin kapladi yuzey buyuklugu
- Birim kare ile olcme: Bir seklin icine kac birim kare sigar?
- Karenin alani: kenar × kenar = a × a
  Ornek: Kenari 3 cm → Alan = 3 × 3 = 9 cm² (9 birim kare)
- Dikdortgenin alani: uzun kenar × kisa kenar = a × b
  Ornek: 5 cm × 3 cm → Alan = 15 cm²
- 3. sinifta alan kavramina birim karelerle giris yapilir
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. OLCME
# ═══════════════════════════════════════════════════════════════

"MAT.3.6.OLCME": {
    "unite": "Olcme",
    "baslik": "Tartma, Sivi Olcme ve Zaman",
    "icerik": """
TARTMA (KUTLE OLCME):

Birimler:
- kilogram (kg): Temel birim
- gram (g): Kucuk birimleri olcmek icin
- 1 kg = 1000 g

DONUSUMLER (kg - g):
- 1 kg = 1000 g
- 2 kg = 2000 g
- Yarim kg = 500 g
- Ceyrek kg = 250 g
- 3 kg 250 g = 3250 g
- 4500 g = 4 kg 500 g

TARTMA ARACLARI:
- Terazi: Iki kefeli, esit agirligi gosterir
- Dijital terazi: Sayisal deger gosterir
- Banyo tartisi: Vucut agirligini olcer

TARTMA PROBLEMLERI:
- "3 kg 500 g elma ve 2 kg 250 g portakal aldim. Toplam kac kg kac g?"
  → 3 kg 500 g + 2 kg 250 g = 5 kg 750 g

SIVI OLCME:

Birimler:
- litre (L): Temel birim
- mililitre (mL): Kucuk sivi miktarlari icin
- 1 L = 1000 mL

DONUSUMLER (L - mL):
- 1 L = 1000 mL
- 2 L = 2000 mL
- Yarim L = 500 mL
- Ceyrek L = 250 mL
- 1 L 500 mL = 1500 mL
- 3200 mL = 3 L 200 mL

SIVI OLCME ARACLARI:
- Olcu kabi (beher): mL isaretli
- Su sisesi: 500 mL, 1 L, 1.5 L
- Bardak: yaklasik 200 mL

SIVI OLCME PROBLEMLERI:
- "2 L 300 mL su ve 1 L 700 mL sut aldim. Toplam kac L?"
  → 2 L 300 mL + 1 L 700 mL = 4 L (3 L 1000 mL = 4 L)

ZAMAN:

DONUSUMLER (dakika - saat):
- 1 saat = 60 dakika
- 2 saat = 120 dakika
- Yarim saat = 30 dakika
- Ceyrek saat = 15 dakika
- 1 saat 30 dakika = 90 dakika
- 150 dakika = 2 saat 30 dakika

SAAT OKUMA (3. SINIF):
- Tam saat: 3:00 → "Saat uc"
- Buçuk: 3:30 → "Uc bucuk" veya "Ucu otuz geciyork"
- Ceyrek: 3:15 → "Ucu ceyrek geciyor", 3:45 → "Dordu ceyrek geciyor" / "Dorde ceyrek var"
- Bes bese: 3:05, 3:10, 3:20, 3:25, 3:35, 3:40, 3:50, 3:55
- "Geciyor" ve "var" kullanimi:
  * 12'den az → "geciyor" (3:20 → "Ucu yirmi geciyor")
  * 12'den fazla → "var" (3:40 → "Dordu yirmi geciyor" veya "Dorde yirmi var")

ZAMAN PROBLEMLERI:
- "Film 1 saat 45 dakika surdu. Saat 14:00'te basladi. Kacta bitti?" → 15:45
- "Okul 08:30'da basliyor. Ali evden 30 dakika once cikiyor. Kacta cikar?" → 08:00
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.3.7.VERI": {
    "unite": "Veri Isleme",
    "baslik": "Veri Toplama ve Cizgi Grafik",
    "icerik": """
VERI TOPLAMA (3. SINIF):
- Sayma ile veri toplama: siniftaki goz renkleri, favori meyveler
- Cizgi ile sayma: Her 5 cizgide bir grup (IIII ile gosterim)
- Tablo olusturma: Toplanan verileri tabloya yerlestime

SIKLIK (FREKANS) TABLOSU:
Verilerin kac kez tekrarlandigini gosteren tablo.
Ornek:
| Meyve    | Sayi |
|----------|------|
| Elma     | 8    |
| Portakal | 5    |
| Muz      | 7    |
| Cilek    | 4    |

SUTUN GRAFIGI (TEKRAR):
- Dikey cubuklerla veri gosterimi
- Yatay eksen: Kategoriler (elma, portakal...)
- Dikey eksen: Sayilar (1, 2, 3...)
- Her cubuk bir kategoriyi temsil eder

CIZGI GRAFIK (YENI - 3. SINIF):
Tanim: Verilerin noktalarla isaretlenip cizgiyle birlestirilmesiyle olusturulan grafik.
Genellikle zamana bagli degisimi gostermek icin kullanilir.

CIZGI GRAFIK OZELLIKLERI:
- Yatay eksen: Genellikle zaman (gunler, haftalar, aylar)
- Dikey eksen: Olculen deger (sicaklik, ogrenci sayisi, satislar)
- Her veri bir nokta ile isaretlenir
- Noktalar sirayla cizgiyle birlestirilir
- Artis, azalis ve sabit kalma gorulur

CIZGI GRAFIK OKUMA:
- Yukari giden cizgi → ARTIS (deger artmis)
- Asagi giden cizgi → AZALIS (deger azalmis)
- Duz cizgi → DEGISIM YOK (sabit kalmis)
- En yukari nokta → EN BUYUK DEGER
- En asagi nokta → EN KUCUK DEGER

ORNEK CIZGI GRAFIK VERISI:
Bir haftadaki sicaklik degisimi:
| Gun       | Sicaklik (°C) |
|-----------|---------------|
| Pazartesi | 15           |
| Sali      | 18           |
| Carsamba  | 20           |
| Persembe  | 17           |
| Cuma      | 22           |

Yorumlama:
- En sicak gun: Cuma (22°C)
- En soguk gun: Pazartesi (15°C)
- Saliden Carsambaya artis var (+2°C)
- Carsambadan Persembeye azalis var (-3°C)

GRAFIK OLUSTURMA ADIMLARI:
1. Veriyi topla ve tabloya yerlestir
2. Yatay ve dikey eksenleri ciz
3. Eksenlere uygun olcek belirle
4. Verileri nokta olarak isaretle
5. Noktalari cizgiyle birlestir
6. Grafige baslik yaz
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik3_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_3_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik3_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_3_REFERANS.keys())
