# -*- coding: utf-8 -*-
"""
8. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.
LGS (Liselere Gecis Sinavi) duzeyinde kapsamli icerik.

Ogrenme alanlari:
1. Sayilar ve Islemler (Carpanlar-Katlar, Uslu Ifadeler, Karekoklu Ifadeler)
2. Cebir (Cebirsel Ifadeler-Ozdeslikler, Dogrusal Denklemler, Esitsizlikler)
3. Geometri ve Olcme (Ucgenler, Eslik-Benzerlik, Donusum Geometrisi, Geometrik Cisimler)
4. Veri Isleme ve Olasilik (Veri Analizi, Olasilik)
"""

MATEMATIK_8_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: SAYILAR VE ISLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.8.1.CARPANLAR_KATLAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Carpanlar ve Katlar (EBOB - EKOK)",
    "kazanimlar": ["M.8.1.1.1", "M.8.1.1.2", "M.8.1.1.3"],
    "icerik": """
CARPANLAR VE KATLAR:

1. CARPAN (BOLEN):
   - Bir sayiyi tam boluen sayilara carpan (bolen) denir.
   - Ornek: 12'nin carpanlari = {1, 2, 3, 4, 6, 12}
   - Ornek: 18'in carpanlari = {1, 2, 3, 6, 9, 18}

2. KAT:
   - Bir sayinin dogal sayilarla carpimina kat denir.
   - Ornek: 5'in katlari = {0, 5, 10, 15, 20, 25, ...}

3. ASAL SAYI:
   - 1 ve kendisinden baska pozitif boleni olmayan, 1'den buyuk dogal sayi.
   - Ilk 10 asal: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
   - DIKKAT: 1 asal sayi degildir! 2 tek cift asal sayidir.

4. ASAL CARPANLARA AYIRMA:
   - Her bilesik sayi, asal sayilarin carpimi olarak yazilabilir.
   - Ornek: 60 = 2² × 3 × 5
   - Ornek: 84 = 2² × 3 × 7
   - Yontem: Sayiyi en kucuk asal sayidan baslayarak bolmeye devam et.

5. EBOB (En Buyuk Ortak Bolen):
   - Iki veya daha fazla sayinin ortak bolenlerinin en buyugu.
   - YONTEM: Asal carpanlara ayir → ortak asal carpanlarin EN KUCUK kuvvetlerini carp.
   - Ornek: EBOB(12, 18)
     12 = 2² × 3
     18 = 2 × 3²
     Ortak: 2 ve 3 → EBOB = 2¹ × 3¹ = 6
   - Ornek: EBOB(24, 36, 60)
     24 = 2³ × 3
     36 = 2² × 3²
     60 = 2² × 3 × 5
     Ortak: 2 ve 3 → EBOB = 2² × 3 = 12

6. EKOK (En Kucuk Ortak Kat):
   - Iki veya daha fazla sayinin ortak katlarinin en kucugu (sifir haric).
   - YONTEM: Asal carpanlara ayir → tum asal carpanlarin EN BUYUK kuvvetlerini carp.
   - Ornek: EKOK(12, 18)
     12 = 2² × 3
     18 = 2 × 3²
     Tumu: 2², 3² → EKOK = 4 × 9 = 36
   - Ornek: EKOK(8, 12, 15)
     8 = 2³
     12 = 2² × 3
     15 = 3 × 5
     Tumu: 2³, 3, 5 → EKOK = 8 × 3 × 5 = 120

7. EBOB-EKOK ILISKISI:
   - Iki sayi icin: EBOB(a,b) × EKOK(a,b) = a × b
   - Ornek: EBOB(12,18) × EKOK(12,18) = 6 × 36 = 216 = 12 × 18 ✓

8. ARALARINDA ASAL:
   - EBOB'lari 1 olan iki sayiya aralarinda asal denir.
   - Ornek: 8 ve 15 aralarinda asaldir (EBOB = 1).
   - DIKKAT: Aralarinda asal olmak icin sayilarin kendisinin asal olmasi gerekmez!

LGS ORNEK SORU:
Soru: 120 ile 84'un EBOB ve EKOK'unu bulunuz.
Cozum:
  120 = 2³ × 3 × 5
  84  = 2² × 3 × 7
  EBOB = 2² × 3 = 12
  EKOK = 2³ × 3 × 5 × 7 = 840
  Dogrulama: 12 × 840 = 10080 = 120 × 84 ✓
"""
},

"MAT.8.1.USLU_IFADELER": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Uslu Ifadeler ve Kurallari",
    "kazanimlar": ["M.8.1.2.1", "M.8.1.2.2"],
    "icerik": """
USLU IFADELER:

1. TANIM:
   - aⁿ = a × a × a × ... × a  (n tane a)
   - a: taban, n: us (kuvvet)
   - Ornek: 2⁵ = 2×2×2×2×2 = 32

2. TAM SAYI KUVVETLERI:
   - Pozitif us: aⁿ (n > 0) → normal carpim
   - Sifir us: a⁰ = 1  (a ≠ 0)
   - Negatif us: a⁻ⁿ = 1/aⁿ  (a ≠ 0)
   - Ornek: 3⁻² = 1/3² = 1/9
   - Ornek: 5⁰ = 1
   - Ornek: (-2)³ = -8,  (-2)⁴ = 16

3. ISARET KURALLARI:
   - Pozitif tabanin her kuvveti pozitiftir.
   - Negatif taban + cift us = pozitif sonuc:  (-3)² = 9
   - Negatif taban + tek us = negatif sonuc:   (-3)³ = -27
   - DIKKAT: (-2)⁴ = 16  ama  -2⁴ = -(2⁴) = -16

4. USLU IFADE KURALLARI:
   a) Ayni tabanli carpma: aᵐ × aⁿ = aᵐ⁺ⁿ
      Ornek: 2³ × 2⁴ = 2⁷ = 128

   b) Ayni tabanli bolme: aᵐ ÷ aⁿ = aᵐ⁻ⁿ  (a ≠ 0)
      Ornek: 5⁶ ÷ 5² = 5⁴ = 625

   c) Usun ussu: (aᵐ)ⁿ = aᵐˣⁿ
      Ornek: (2³)⁴ = 2¹² = 4096

   d) Carpimin kuvveti: (a × b)ⁿ = aⁿ × bⁿ
      Ornek: (2 × 3)⁴ = 2⁴ × 3⁴ = 16 × 81 = 1296

   e) Bolumun kuvveti: (a/b)ⁿ = aⁿ/bⁿ  (b ≠ 0)
      Ornek: (3/2)³ = 27/8

5. 10'UN KUVVETLERI VE BILIMSEL GOSTERIM:
   - 10¹ = 10, 10² = 100, 10³ = 1000, ...
   - 10⁻¹ = 0,1;  10⁻² = 0,01;  10⁻³ = 0,001
   - Bilimsel gosterim: a × 10ⁿ  (1 ≤ a < 10)
   - Ornek: 3.500.000 = 3,5 × 10⁶
   - Ornek: 0,00042 = 4,2 × 10⁻⁴

LGS ORNEK SORU:
Soru: 2⁸ × 3⁴ ifadesini 6'nin kuvveti olarak yaziniz.
Cozum:
  2⁸ × 3⁴ = 2⁴ × 2⁴ × 3⁴ = 2⁴ × (2×3)⁴ = 16 × 6⁴
  Veya: 2⁸ × 3⁴ = (2²)⁴ × 3⁴ = 4⁴ × 3⁴ = (4×3)⁴ = 12⁴
  Not: Dogrudan 6'nin kuvveti yazilamaz cunku 2 ve 3 usleri farkli.
"""
},

"MAT.8.1.KAREKOKLU_IFADELER": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Karekoklu Ifadeler ve Islemler",
    "kazanimlar": ["M.8.1.3.1", "M.8.1.3.2", "M.8.1.3.3"],
    "icerik": """
KAREKOKLU IFADELER:

1. KAREKOK KAVRAMI:
   - √a: karesi a olan negatif olmayan sayi (a ≥ 0)
   - √a = b  ise  b² = a  ve  b ≥ 0
   - Ornek: √9 = 3 (cunku 3² = 9)
   - Ornek: √25 = 5, √49 = 7, √144 = 12
   - DIKKAT: √4 = 2 (−2 degil, karekok daima negatif olmayan deger verir)

2. TAM KARELER:
   - 0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, ...
   - √(tam kare) = dogal sayi
   - Tam kare olmayan sayilarin karekokleri irrasyonel sayidir.
   - Ornek: √2, √3, √5, √7 → irrasyonel (ondalik acilimi sonsuz ve tekrarlanmaz)

3. KAREKOK ISLEM KURALLARI:
   a) Carpma: √a × √b = √(a×b)
      Ornek: √2 × √8 = √16 = 4

   b) Bolme: √a / √b = √(a/b)  (b > 0)
      Ornek: √50 / √2 = √25 = 5

   c) Toplama/Cikarma: Yalnizca kok ici ayni ise yapilir!
      Ornek: 3√5 + 2√5 = 5√5  ✓
      Ornek: √3 + √5 ≠ √8     ✗ (YANLIS!)

   d) Karekok sadeleştirme: √(a²×b) = a√b
      Ornek: √72 = √(36×2) = 6√2
      Ornek: √48 = √(16×3) = 4√3
      Ornek: √200 = √(100×2) = 10√2

4. PAYDAYI RASYONELLESTIRME:
   - a/√b = (a×√b)/(√b×√b) = (a√b)/b
   - Ornek: 6/√3 = (6√3)/3 = 2√3
   - Ornek: 1/√2 = √2/2
   - Eslenige carpma: a/(√b+√c) → pay ve paydayi (√b−√c) ile carp
   - Ornek: 1/(√5+√3) = (√5−√3)/((√5)²−(√3)²) = (√5−√3)/2

5. KAREKOK KARSILASTIRMA:
   - √a < √b  ise  a < b (a,b ≥ 0)
   - Ornek: √5 ile √7 → 5 < 7 oldugu icin √5 < √7
   - 3 ile √10 → 3 = √9 → √9 < √10 → 3 < √10

6. SAYI DOGRUSU:
   - √2 ≈ 1,41;  √3 ≈ 1,73;  √5 ≈ 2,24;  √6 ≈ 2,45;  √7 ≈ 2,65
   - Pisagor bagintisi ile sayi dogrusunda gosterim yapilir.

LGS ORNEK SORU:
Soru: √75 − √48 + √27 ifadesinin sonucunu bulunuz.
Cozum:
  √75 = √(25×3) = 5√3
  √48 = √(16×3) = 4√3
  √27 = √(9×3)  = 3√3
  Sonuc = 5√3 − 4√3 + 3√3 = 4√3

Soru: 2/(√7−√5) ifadesini sadelelestiriniz.
Cozum:
  2/(√7−√5) × (√7+√5)/(√7+√5) = 2(√7+√5)/(7−5) = 2(√7+√5)/2 = √7+√5
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: CEBIR
# ═══════════════════════════════════════════════════════════════

"MAT.8.2.CEBIRSEL_IFADELER_OZDESLIKLER": {
    "unite": "Cebir",
    "baslik": "Cebirsel Ifadeler ve Ozdeslikler",
    "kazanimlar": ["M.8.2.1.1", "M.8.2.1.2", "M.8.2.1.3"],
    "icerik": """
CEBIRSEL IFADELER VE OZDESLIKLER:

1. CEBIRSEL IFADE:
   - Sayilar, degiskenler ve islem isaretleri ile yazilan ifadeler.
   - Ornek: 3x + 5,  2a² − 4a + 1,  x² + y²

2. CARPMA ISLEMLERI:
   - Tek terimli × Tek terimli: 3x × 2x² = 6x³
   - Tek terimli × Cok terimli: 2x(3x − 5) = 6x² − 10x
   - Cok terimli × Cok terimli: (x+2)(x+3) = x² + 3x + 2x + 6 = x² + 5x + 6

3. OZDESLIKLER (FORMUL TABLOSU):

   ╔════════════════════════════════════════════════════════════╗
   ║  (a + b)² = a² + 2ab + b²        → Toplamin karesi       ║
   ║  (a − b)² = a² − 2ab + b²        → Farkin karesi         ║
   ║  (a + b)(a − b) = a² − b²        → Iki kare farki        ║
   ║  (a + b)³ = a³ + 3a²b + 3ab² + b³  (bilgi icin)         ║
   ╚════════════════════════════════════════════════════════════╝

   Ornekler:
   - (x + 3)² = x² + 6x + 9
   - (2x − 5)² = 4x² − 20x + 25
   - (x + 4)(x − 4) = x² − 16
   - (3a + 2b)² = 9a² + 12ab + 4b²

4. OZDESLIK UYGULAMALARI (LGS TAKTIK):
   - 101² = (100+1)² = 10000 + 200 + 1 = 10201
   - 99² = (100−1)² = 10000 − 200 + 1 = 9801
   - 51 × 49 = (50+1)(50−1) = 2500 − 1 = 2499
   - 103 × 97 = (100+3)(100−3) = 10000 − 9 = 9991

5. CARPANLARA AYIRMA YONTEMLERI:
   a) Ortak carpan parantezine alma:
      6x² + 9x = 3x(2x + 3)

   b) Gruplama yontemi:
      ax + ay + bx + by = a(x+y) + b(x+y) = (a+b)(x+y)

   c) Ozdeslik kullanma:
      x² − 9 = (x+3)(x−3)                     → iki kare farki
      x² + 6x + 9 = (x+3)²                     → toplamin karesi
      4x² − 12x + 9 = (2x−3)²                  → farkin karesi

   d) x² + bx + c turunde carpanlara ayirma:
      Carpimi c, toplami b olan iki sayi bul.
      x² + 7x + 12 = (x+3)(x+4)    [3×4=12, 3+4=7]
      x² − 5x + 6 = (x−2)(x−3)     [(-2)×(-3)=6, (-2)+(-3)=-5]
      x² + x − 6 = (x+3)(x−2)      [3×(-2)=-6, 3+(-2)=1]

LGS ORNEK SORU:
Soru: a² − b² = 48 ve a + b = 8 ise a − b kactir?
Cozum: a² − b² = (a+b)(a−b) = 48 → 8 × (a−b) = 48 → a−b = 6
"""
},

"MAT.8.2.DOGRUSAL_DENKLEMLER": {
    "unite": "Cebir",
    "baslik": "Birinci Dereceden Denklemler ve Problemler",
    "kazanimlar": ["M.8.2.2.1", "M.8.2.2.2", "M.8.2.2.3"],
    "icerik": """
DOGRUSAL DENKLEMLER:

1. BIRINCI DERECEDEN BIR BILINMEYENLI DENKLEMLER:
   - ax + b = 0  (a ≠ 0) seklindeki denklemler
   - Cozum: x = −b/a

   COZUM ADIMLARI:
   1. Parantez varsa ac
   2. Kesirli ise ortak paydayi bul, paydayi yok et
   3. Degiskenleri bir tarafa, sabitleri diger tarafa topla
   4. Degiskenin katsayisina bol

   Ornek: 3(x − 2) + 4 = 2x + 5
   3x − 6 + 4 = 2x + 5
   3x − 2 = 2x + 5
   3x − 2x = 5 + 2
   x = 7

   Ornek: (2x+1)/3 − (x−2)/4 = 1
   Ortak payda 12: 4(2x+1) − 3(x−2) = 12
   8x + 4 − 3x + 6 = 12
   5x + 10 = 12
   5x = 2  →  x = 2/5

2. DENKLEM KURUP COZME (SOZEL PROBLEMLER):
   - Ard isik sayi problemleri: x, x+1, x+2
   - Yas problemleri: simdiki yas ve gecmis/gelecek yas farki
   - Is-isci problemleri: birim zamanda yapilan is orani
   - Hiz-yol-zaman: Yol = Hiz × Zaman
   - Kar-zarar-yuzde: Kar = Satis − Alis

   Ornek: Ard isik uc dogal sayinin toplami 51 ise sayilari bulunuz.
   x + (x+1) + (x+2) = 51
   3x + 3 = 51  →  3x = 48  →  x = 16
   Sayilar: 16, 17, 18

3. BIRINCI DERECEDEN IKI BILINMEYENLI DENKLEM SISTEMLERI:
   - ax + by = c  ve  dx + ey = f

   YONTEM 1 - YERINE KOYMA:
   Bir denklemden bir bilinmeyeni yalniz birak, digerine yaz.

   YONTEM 2 - YOK ETME (ELEME):
   Bir bilinmeyenin katsayilarini esitleyip cikar veya topla.

   Ornek: x + y = 10 ve x − y = 4
   Toplarsak: 2x = 14 → x = 7, y = 3

   Ornek: 2x + 3y = 12 ve x − y = 1
   Ikinci denklemden: x = y + 1 → 2(y+1) + 3y = 12
   2y + 2 + 3y = 12 → 5y = 10 → y = 2, x = 3

LGS ORNEK SORU:
Soru: Bir sayinin 3 kati ile 7'nin toplami, o sayinin 5 katindan 1 eksiktir. Sayi kactir?
Cozum: 3x + 7 = 5x − 1 → 7 + 1 = 5x − 3x → 8 = 2x → x = 4
"""
},

"MAT.8.2.ESITSIZLIKLER": {
    "unite": "Cebir",
    "baslik": "Esitsizlikler",
    "kazanimlar": ["M.8.2.3.1", "M.8.2.3.2"],
    "icerik": """
ESITSIZLIKLER:

1. ESITSIZLIK SEMBOLLERI:
   - a < b  → a, b'den kucuktur
   - a > b  → a, b'den buyuktur
   - a ≤ b  → a, b'den kucuk veya esittir
   - a ≥ b  → a, b'den buyuk veya esittir

2. ESITSIZLIK KURALLARI:
   a) Her iki tarafa ayni sayi eklenip cikarilabilir (yon degismez):
      x − 3 > 5  →  x > 8

   b) Her iki taraf ayni POZITIF sayi ile carpilip bolunebilir (yon degismez):
      2x < 10  →  x < 5

   c) Her iki taraf NEGATIF sayi ile carpilir/bolunurse YON DEGISIR:
      −3x > 12  →  x < −4  (yon degisti!)

   d) DIKKAT: Negatif sayi ile carpma/bolme → esitsizlik yonu TERSINE DONER!

3. BIRINCI DERECEDEN ESITSIZLIK COZUMU:
   Ornek: 2x + 3 < 11
   2x < 8
   x < 4
   Cozum kumesi: {..., 1, 2, 3} (tam sayilarda) veya (−∞, 4) (reel sayilarda)

   Ornek: −2x + 5 ≥ 1
   −2x ≥ −4
   x ≤ 2  (negatif ile bolduk, yon degisti)

   Ornek: 3(x − 1) > 2x + 4
   3x − 3 > 2x + 4
   x > 7

4. SAYI DOGRUSUNDA GOSTERIM:
   - x > 3  → 3'ten saga, 3 dahil degil (bos daire ○)
   - x ≥ 3  → 3'ten saga, 3 dahil (dolu daire ●)
   - x < 3  → 3'ten sola, 3 dahil degil (bos daire ○)
   - x ≤ 3  → 3'ten sola, 3 dahil (dolu daire ●)

5. CIFT ESITSIZLIK:
   - Ornek: −2 < x + 1 ≤ 5
     Her taraftan 1 cikar: −3 < x ≤ 4
     Cozum: x, −3 ile 4 arasinda (−3 haric, 4 dahil)

LGS ORNEK SORU:
Soru: 3x − 2 > x + 6 esitsizligini saglayan en kucuk tam sayi kactir?
Cozum: 3x − x > 6 + 2 → 2x > 8 → x > 4
En kucuk tam sayi: 5
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: GEOMETRI VE OLCME
# ═══════════════════════════════════════════════════════════════

"MAT.8.3.UCGENLER": {
    "unite": "Geometri ve Olcme",
    "baslik": "Ucgenlerde Kenarortay, Aciortay, Yukseklik ve Pisagor Teoremi",
    "kazanimlar": ["M.8.3.1.1", "M.8.3.1.2", "M.8.3.1.3"],
    "icerik": """
UCGENLERDE TEMEL ELEMANLAR:

1. KENARORTAY:
   - Bir koseyi karsisindaki kenarin orta noktasina birlestiren dogru parcasi.
   - Her ucgenin 3 kenarortayi vardir.
   - Kenarortaylar agirlik merkezinde (G) kesisir.
   - Agirlik merkezi her kenarortayi koseden 2/3, kenardan 1/3 oraninda boler.
   - Kenarortay ucgeni alani esit 6 parcaya boler.

2. ACIORTAY:
   - Bir aciyi iki esit parcaya bolen isin.
   - Her ucgenin 3 aciortayi vardir.
   - Aciortaylar ic teget cember merkezinde (I) kesisir.
   - Ic aciortay teoremi: Aciortay karsi kenari, komsU kenarlarin oraniyla boler.
     BD/DC = AB/AC

3. YUKSEKLIK:
   - Bir koseden karsi kenara (veya uzantisina) indirilen dikme.
   - Her ucgenin 3 yuksekligi vardir.
   - Yukseklikler diklik merkezinde (H) kesisir.
   - Alan = (taban × yukseklik) / 2

4. PISAGOR TEOREMI:
   ╔══════════════════════════════════════════════════╗
   ║  Dik ucgende: Hipotenusun karesi =              ║
   ║  dik kenarlarin karelerinin toplamina esittir.   ║
   ║                                                  ║
   ║           c² = a² + b²                           ║
   ║                                                  ║
   ║  c: hipotenus (90° acinin karsisi, en uzun kenar)║
   ║  a, b: dik kenarlar                              ║
   ╚══════════════════════════════════════════════════╝

   Onemli Pisagor Uclulerı:
   - (3, 4, 5)   → 9 + 16 = 25  ✓
   - (5, 12, 13) → 25 + 144 = 169  ✓
   - (8, 15, 17) → 64 + 225 = 289  ✓
   - (7, 24, 25) → 49 + 576 = 625  ✓
   - Katlari da pisagor uclusudur: (6, 8, 10), (9, 12, 15), (10, 24, 26)

   Ornek: Dik kenarlari 6 cm ve 8 cm olan ucgenin hipotenusu:
   c² = 6² + 8² = 36 + 64 = 100 → c = 10 cm

5. PISAGOR TEOREMININ TERSI (UCGEN TURU BELIRLEME):
   - c² = a² + b²  →  Dik ucgen
   - c² > a² + b²  →  Genis acili ucgen
   - c² < a² + b²  →  Dar acili ucgen
   (c en buyuk kenar olmak uzere)

   Ornek: 7, 8, 10 → 10² = 100,  7²+8² = 49+64 = 113 → 100 < 113 → Dar acili

6. PISAGOR UYGULAMALARI:
   - Kosegen hesaplama: Dikdortgenin kosegeni = √(a² + b²)
   - Uzaklik hesaplama: iki nokta arasi = √((x₂−x₁)² + (y₂−y₁)²)
   - 3 boyutlu uzaklik: √(a² + b² + c²) (kutu kosegeni)

LGS ORNEK SORU:
Soru: Bir dikdortgenin kenarlari 5 cm ve 12 cm'dir. Kosegen uzunlugu kac cm'dir?
Cozum: d = √(5² + 12²) = √(25 + 144) = √169 = 13 cm
"""
},

"MAT.8.3.ESLIK_BENZERLIK": {
    "unite": "Geometri ve Olcme",
    "baslik": "Ucgenlerde Eslik ve Benzerlik",
    "kazanimlar": ["M.8.3.2.1", "M.8.3.2.2", "M.8.3.2.3"],
    "icerik": """
UCGENLERDE ESLIK VE BENZERLIK:

1. ES UCGENLER:
   - Kenar uzunluklari ve aci olculeri birebir ayni olan ucgenler.
   - Eslik durumu: ≅ sembolü ile gosterilir.
   - ABC ≅ DEF ise: AB=DE, BC=EF, AC=DF ve A=D, B=E, C=F

   ESLIK KOSULLARI:
   a) K.K.K. (Kenar-Kenar-Kenar):
      Uc kenari esit olan ucgenler estir.
   b) K.A.K. (Kenar-Aci-Kenar):
      Iki kenari ve aradaki acisi esit olan ucgenler estir.
   c) A.K.A. (Aci-Kenar-Aci):
      Iki acisi ve aradaki kenari esit olan ucgenler estir.

2. BENZER UCGENLER:
   - Acilari esit, kenarlari orantili olan ucgenler.
   - Benzerlik durumu: ~ sembolü ile gosterilir.
   - ABC ~ DEF ise: AB/DE = BC/EF = AC/DF = k (benzerlik orani)

   BENZERLIK KOSULLARI:
   a) A.A. (Aci-Aci):
      Iki acisi esit olan ucgenler benzerdir.
      (Ucuncu aci zaten esit olur: 180° kurali)
   b) K.K.K. (Kenar oranlari esit):
      Uc kenar orantili ise benzerdir.
   c) K.A.K. (Kenar orani esit + aradaki aci esit):

3. BENZERLIK ORANI VE SONUCLARI:
   - Kenar orani: k
   - Cevre orani: k
   - Alan orani: k²
   - Hacim orani: k³  (benzer cisimler icin)

   Ornek: Iki benzer ucgenin kenarlari orani 2/3 ise:
   - Cevre orani = 2/3
   - Alan orani = (2/3)² = 4/9

4. UCGENDE ACI-KENAR ILISKILERI:
   - Buyuk acinin karsisinda buyuk kenar bulunur.
   - Esit kenarlarin karsisinda esit acilar bulunur.
   - Ucgenin iki kenarinin toplami ucuncu kenardan buyuktur.
   - Ucgenin iki kenarinin farki ucuncu kenardan kucuktur.

5. OZEL UCGENLER:
   - Ikizkenar ucgen: Iki kenari esit, taban acilari esit.
   - Eskenar ucgen: Uc kenari esit, her aci 60°.
     Eskenar ucgen alani = (a²√3)/4
     Yukseklik = (a√3)/2

LGS ORNEK SORU:
Soru: ABC ~ DEF ucgenlerinde AB=6, DE=9, BC=8 ise EF kactir?
Cozum: AB/DE = BC/EF → 6/9 = 8/EF → EF = 8×9/6 = 12
"""
},

"MAT.8.3.DONUSUM_GEOMETRISI": {
    "unite": "Geometri ve Olcme",
    "baslik": "Donusum Geometrisi (Oteleme, Yansima, Donme)",
    "kazanimlar": ["M.8.3.3.1", "M.8.3.3.2", "M.8.3.3.3"],
    "icerik": """
DONUSUM GEOMETRISI:

1. OTELEME (KAYMA / TRANSLASYON):
   - Bir sekli, yonunu ve bicimini degistirmeden belirli bir yonde ve uzaklikta kaydirma.
   - Her nokta ayni yon ve uzaklikta hareket eder.
   - Oteleme vektoru: yonu ve buyuklugu belirler.
   - Ornek: A(2,3) noktasi (4,−1) oteleme vektoru ile → A'(2+4, 3+(−1)) = A'(6,2)
   - Ozellikler:
     * Sekil ve boyut degismez (es kalir)
     * Kenar uzunluklari ve acilar korunur
     * Yonelim (saat yonu) korunur

2. YANSIMA (SIMETRI / REFLEKSIYON):
   - Bir sekli, bir simetri dogrusu (ekseni) boyunca ayna goruntusu olarak olusturma.

   a) x-eksenine gore yansima: (x, y) → (x, −y)
      Ornek: A(3, 5) → A'(3, −5)

   b) y-eksenine gore yansima: (x, y) → (−x, y)
      Ornek: B(4, 2) → B'(−4, 2)

   c) y = x dogrusuna gore yansima: (x, y) → (y, x)
      Ornek: C(3, 7) → C'(7, 3)

   d) Orijine gore yansima: (x, y) → (−x, −y)
      Ornek: D(2, −3) → D'(−2, 3)

   - Ozellikler:
     * Sekil ve boyut degismez (es kalir)
     * Kenar uzunluklari ve acilar korunur
     * Yonelim (saat yonu) DEGISIR (ters doner)

3. DONME (ROTASYON):
   - Bir sekli, sabit bir nokta (donme merkezi) etrafinda belirli bir aciyla cevirmek.
   - Saat yonunun tersine: pozitif aci
   - Saat yonunde: negatif aci

   ORIJIN ETRAFINDA DONME FORMULLERI:
   a) 90° (saat yonu tersi): (x, y) → (−y, x)
      Ornek: A(3, 2) → A'(−2, 3)

   b) 180°: (x, y) → (−x, −y)
      Ornek: B(4, −1) → B'(−4, 1)

   c) 270° (veya −90°): (x, y) → (y, −x)
      Ornek: C(2, 5) → C'(5, −2)

   d) 360°: (x, y) → (x, y) (ayni noktaya doner)

   - Ozellikler:
     * Sekil ve boyut degismez (es kalir)
     * Kenar uzunluklari ve acilar korunur
     * Yonelim korunur
     * Merkeze uzaklik degismez

4. DONUSUMLERIN KARSILASTIRILMASI:
   ┌────────────┬──────────┬──────────┬──────────┐
   │ Ozellik    │ Oteleme  │ Yansima  │ Donme    │
   ├────────────┼──────────┼──────────┼──────────┤
   │ Boyut      │ Korunur  │ Korunur  │ Korunur  │
   │ Sekil      │ Korunur  │ Korunur  │ Korunur  │
   │ Yonelim    │ Korunur  │ DEGISIR  │ Korunur  │
   └────────────┴──────────┴──────────┴──────────┘

LGS ORNEK SORU:
Soru: A(3, −2) noktasinin orijin etrafinda 90° (saat yonu tersi) dondurulmesi
ile elde edilen nokta nedir?
Cozum: (x, y) → (−y, x) → A'(2, 3)
"""
},

"MAT.8.3.GEOMETRIK_CISIMLER_PRIZMA_SILINDIR": {
    "unite": "Geometri ve Olcme",
    "baslik": "Prizma ve Silindir (Yuzey Alani ve Hacim)",
    "kazanimlar": ["M.8.3.4.1", "M.8.3.4.2"],
    "icerik": """
PRIZMA VE SILINDIR:

1. PRIZMA:
   - Iki es ve paralel tabani olan, yan yuzleri dikdortgen olan cisim.
   - Tabanin sekline gore ad alir: ucgen prizma, dortgen prizma, besgen prizma...

   DIKDORTGENLER PRIZMAS (KUTU):
   ╔════════════════════════════════════════════════════╗
   ║  Hacim = a × b × c                                ║
   ║  Yuzey Alani = 2(ab + ac + bc)                    ║
   ║  Uzay Kosegeni = √(a² + b² + c²)                  ║
   ╚════════════════════════════════════════════════════╝

   KUP (tum kenarlari esit prizma):
   ╔════════════════════════════════════════════════════╗
   ║  Hacim = a³                                        ║
   ║  Yuzey Alani = 6a²                                 ║
   ║  Yuz Kosegeni = a√2                                ║
   ║  Uzay Kosegeni = a√3                               ║
   ╚════════════════════════════════════════════════════╝

   GENEL PRIZMA:
   ╔════════════════════════════════════════════════════╗
   ║  Hacim = Taban Alani × Yukseklik                   ║
   ║  Yuzey Alani = 2 × Taban Alani + Yan Alan          ║
   ║  Yan Alan = Taban Cevresi × Yukseklik               ║
   ╚════════════════════════════════════════════════════╝

   Ornek: Tabani bir kenarı 6 cm olan eskenar ucgen, yuksekligi 10 cm olan prizma.
   Taban Alani = (6²√3)/4 = 9√3 cm²
   Hacim = 9√3 × 10 = 90√3 cm³
   Yan Alan = (3×6) × 10 = 180 cm²
   Yuzey Alani = 2×9√3 + 180 = 18√3 + 180 cm²

2. SILINDIR:
   ╔════════════════════════════════════════════════════╗
   ║  Hacim = π × r² × h                               ║
   ║  Taban Alani = π × r²                              ║
   ║  Yan Alan = 2π × r × h                             ║
   ║  Toplam Yuzey Alani = 2πr² + 2πrh = 2πr(r + h)    ║
   ╚════════════════════════════════════════════════════╝

   - r: taban yaricapi, h: yukseklik
   - Silindirin yan yuzeyi acilinca dikdortgen olur:
     Genislik = 2πr (cember cevresi), Yukseklik = h

   Ornek: r = 3 cm, h = 10 cm
   Hacim = π × 9 × 10 = 90π cm³ ≈ 282,74 cm³
   Yan Alan = 2π × 3 × 10 = 60π cm²
   Yuzey Alani = 2π×9 + 60π = 18π + 60π = 78π cm²

LGS ORNEK SORU:
Soru: Bir dikdortgenler prizmasinin boyutlari 3, 4, 5 cm'dir. Hacmi ve yuzey alani kactir?
Cozum:
  Hacim = 3 × 4 × 5 = 60 cm³
  Yuzey Alani = 2(3×4 + 3×5 + 4×5) = 2(12 + 15 + 20) = 2 × 47 = 94 cm²
"""
},

"MAT.8.3.GEOMETRIK_CISIMLER_KONI_KURE": {
    "unite": "Geometri ve Olcme",
    "baslik": "Koni ve Kure (Yuzey Alani ve Hacim)",
    "kazanimlar": ["M.8.3.4.2", "M.8.3.4.3"],
    "icerik": """
KONI VE KURE:

1. KONI:
   - Bir daire tabani ve bir tepe noktasi olan cisim.
   - r: taban yaricapi, h: yukseklik, l: anamur (yan uzunluk / ana dogru)
   - Pisagor iliskisi: l² = r² + h²  →  l = √(r² + h²)

   ╔════════════════════════════════════════════════════╗
   ║  Hacim = (1/3) × π × r² × h                       ║
   ║  Taban Alani = π × r²                              ║
   ║  Yan Alan = π × r × l                              ║
   ║  Toplam Yuzey Alani = πr² + πrl = πr(r + l)        ║
   ╚════════════════════════════════════════════════════╝

   Ornek: r = 3 cm, h = 4 cm
   l = √(9 + 16) = √25 = 5 cm
   Hacim = (1/3) × π × 9 × 4 = 12π cm³
   Yan Alan = π × 3 × 5 = 15π cm²
   Yuzey Alani = π×9 + 15π = 9π + 15π = 24π cm²

   KONI-SILINDIR ILIKSISI:
   - Ayni taban ve yukseklige sahip koninin hacmi, silindirin hacminin 1/3'udur.
   - V_koni = (1/3) × V_silindir

2. KURE:
   - Bir noktaya esit uzakliktaki tum noktalarin olusturdugu cisim.
   - r: yaricap

   ╔════════════════════════════════════════════════════╗
   ║  Hacim = (4/3) × π × r³                           ║
   ║  Yuzey Alani = 4 × π × r²                         ║
   ╚════════════════════════════════════════════════════╝

   Ornek: r = 6 cm
   Hacim = (4/3) × π × 216 = 288π cm³ ≈ 904,78 cm³
   Yuzey Alani = 4π × 36 = 144π cm² ≈ 452,39 cm²

   YARI KURE:
   ╔════════════════════════════════════════════════════╗
   ║  Hacim = (2/3) × π × r³                           ║
   ║  Yuzey Alani = 3 × π × r²                         ║
   ║  (2πr²: dis yuzey + πr²: duz yuzey)               ║
   ╚════════════════════════════════════════════════════╝

3. FORMUL KARSILASTIRMA TABLOSU:
   ┌────────────┬─────────────────────┬──────────────────┐
   │ Cisim      │ Hacim               │ Yuzey Alani      │
   ├────────────┼─────────────────────┼──────────────────┤
   │ Kup        │ a³                  │ 6a²              │
   │ Prizma     │ Taban×h             │ 2Taban + Yan     │
   │ Silindir   │ πr²h                │ 2πr(r+h)         │
   │ Koni       │ (1/3)πr²h           │ πr(r+l)          │
   │ Kure       │ (4/3)πr³            │ 4πr²             │
   │ Yari Kure  │ (2/3)πr³            │ 3πr²             │
   └────────────┴─────────────────────┴──────────────────┘

LGS ORNEK SORU:
Soru: Yaricapi 3 cm olan bir kurenin hacmi ile ayni yaricapli bir silindirin
hacmi esit ise silindirin yuksekligi kac cm'dir?
Cozum:
  (4/3)πr³ = πr²h
  (4/3)π×27 = π×9×h
  36π = 9πh
  h = 4 cm
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: VERI ISLEME VE OLASILIK
# ═══════════════════════════════════════════════════════════════

"MAT.8.4.VERI_ANALIZI": {
    "unite": "Veri Isleme ve Olasilik",
    "baslik": "Veri Analizi ve Grafik Yorumlama",
    "kazanimlar": ["M.8.4.1.1", "M.8.4.1.2"],
    "icerik": """
VERI ANALIZI:

1. MERKEZI EGILIM OLCULERI:

   a) ARITMETIK ORTALAMA:
      - Tum degerlerin toplaminin deger sayisina bolunmesi.
      - Ortalama = Toplam / n
      - Ornek: 4, 6, 8, 10, 12 → Ortalama = 40/5 = 8
      - Ortalama tum degerlerden etkilenir (asiri degerlerden de).

   b) ORTANCA (MEDYAN):
      - Veriler kucukten buyuge siralandiginda ortadaki deger.
      - Tek sayida veri: ortadaki deger
        Ornek: 3, 5, 7, 9, 11 → Ortanca = 7
      - Cift sayida veri: ortadaki iki degerin ortalamasi
        Ornek: 2, 4, 6, 8 → Ortanca = (4+6)/2 = 5
      - Asiri degerlerden ortalamaya gore daha az etkilenir.

   c) TEPE DEGER (MOD):
      - En cok tekrar eden deger.
      - Ornek: 3, 5, 5, 7, 5, 9 → Tepe deger = 5
      - Birden fazla tepe deger olabilir (cok modlu).
      - Hic tekrar eden deger yoksa tepe deger yoktur.

2. YAYILIM OLCULERI:

   a) ARALIK (RANGE):
      - En buyuk deger − En kucuk deger
      - Ornek: 15, 22, 8, 31, 12 → Aralik = 31 − 8 = 23

   b) CEYREKLER:
      - Q1 (1. ceyrek): Alt yaridaki verilerin medyani
      - Q2 (2. ceyrek): Tum verilerin medyani = Ortanca
      - Q3 (3. ceyrek): Ust yaridaki verilerin medyani
      - IQR (Ceyrekler arasi aciklik) = Q3 − Q1

3. GRAFIK TURLERI:
   - Cizgi grafigi: Zamanla degisim (sureci gostermek icin)
   - Sutun/Cubuk grafigi: Karsilastirma
   - Daire grafigi: Yuzdelik dagilimlari gostermek
   - Histogram: Surekli verilerin siklik dagilimi
   - Cizgi-nokta (sacilim) grafigi: Iki degisken arasindaki iliski

4. YANILTICI GRAFIKLER:
   - Eksenlerin sifirdan baslamadigi grafikler buyuk fark yanilsamasi yaratir.
   - Farkli olcekli eksenler karsilastirmayi yanitici yapar.
   - Daire grafiklerinde dilimlerin toplami %100 olmali.

LGS ORNEK SORU:
Soru: 5 ogrencinin notlari: 60, 70, 80, 90, 100. Ortalama, ortanca ve aralik nedir?
Cozum:
  Ortalama = (60+70+80+90+100)/5 = 400/5 = 80
  Ortanca = 80 (ortadaki deger)
  Aralik = 100 − 60 = 40
"""
},

"MAT.8.4.OLASILIK": {
    "unite": "Veri Isleme ve Olasilik",
    "baslik": "Olasilik (Basit ve Deneysel)",
    "kazanimlar": ["M.8.4.2.1", "M.8.4.2.2", "M.8.4.2.3"],
    "icerik": """
OLASILIK:

1. TEMEL KAVRAMLAR:
   - Deney: Sonucu onceden bilinmeyen islem (zar atma, yazi-tura)
   - Ornek uzay (S): Tum mumkun sonuclarin kumesi
   - Olay (A): Ornek uzayin alt kumesi
   - Ornek: Zar atma → S = {1, 2, 3, 4, 5, 6}
   - Ornek: Cift gelme olayi → A = {2, 4, 6}

2. BASIT (KLASIK) OLASILIK:
   ╔════════════════════════════════════════════════════╗
   ║  P(A) = Istenen sonuc sayisi / Tum sonuc sayisi   ║
   ║  P(A) = n(A) / n(S)                               ║
   ╚════════════════════════════════════════════════════╝

   - 0 ≤ P(A) ≤ 1
   - P(A) = 0 → Imkansiz olay
   - P(A) = 1 → Kesin olay
   - P(A') = 1 − P(A)  (tamamlayici olay)

3. OLASILIK ORNEKLERI:

   ZAR (6 yuzlu):
   - P(3 gelme) = 1/6
   - P(cift gelme) = 3/6 = 1/2
   - P(asal gelme) = P({2,3,5}) = 3/6 = 1/2
   - P(4'ten buyuk) = P({5,6}) = 2/6 = 1/3
   - P(7 gelme) = 0 (imkansiz)

   YAZI-TURA (1 madeni para):
   - P(yazi) = 1/2,  P(tura) = 1/2
   - Iki para atilirsa: S = {YY, YT, TY, TT}
   - P(en az bir yazi) = 3/4

   KART/TOP CEKMEK:
   - 3 kirmizi, 5 mavi top → Toplam 8 top
   - P(kirmizi) = 3/8
   - P(mavi) = 5/8

4. DENEYSEL OLASILIK:
   - Gercek deneylerin sonuclarina dayanir.
   - Deneysel P(A) = A'nin gerceklestigi sayi / Toplam deney sayisi
   - Deney sayisi arttikca deneysel olasilik teorik olasliga yaklasir (Buyuk Sayilar Yasasi).
   - Ornek: 100 zar atisinda 18 kez 6 geldiyse → Deneysel P(6) = 18/100 = 0,18
     (Teorik P(6) = 1/6 ≈ 0,167)

5. BAGIMSIZ OLAYLAR:
   - Iki olay birbirinin sonucunu etkilemiyorsa bagımsizdir.
   - Bagimsiz olaylarda: P(A ve B) = P(A) × P(B)
   - Ornek: Bir zar ve bir para ayni anda atilirsa,
     P(6 ve Yazi) = 1/6 × 1/2 = 1/12

6. ORNEK UZAY VE AGAC DIYAGRAMI:
   - Iki zar atilirsa: Toplam sonuc = 6 × 6 = 36
   - P(toplam 7) = {(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)} = 6/36 = 1/6
   - P(toplam 12) = {(6,6)} = 1/36
   - P(cift-cift) = 3/6 × 3/6 = 9/36 = 1/4

LGS ORNEK SORU:
Soru: Bir kutuda 4 kirmizi, 3 yesil, 2 mavi top vardir. Rastgele bir top
cekildiginde kirmizi veya mavi gelme olasiligi kactir?
Cozum: Toplam = 9, Kirmizi veya Mavi = 4 + 2 = 6
P = 6/9 = 2/3
"""
},

# ═══════════════════════════════════════════════════════════════
# EK: LGS FORMUL KARTI
# ═══════════════════════════════════════════════════════════════

"MAT.8.EK.FORMUL_KARTI": {
    "unite": "Formul Karti",
    "baslik": "8. Sinif LGS Tum Formuller Ozet Tablosu",
    "kazanimlar": [],
    "icerik": """
LGS 8. SINIF MATEMATIK - FORMUL KARTI:

══════════════ SAYILAR VE ISLEMLER ══════════════

EBOB × EKOK = a × b  (iki sayi icin)
a⁰ = 1 (a≠0)          a⁻ⁿ = 1/aⁿ
aᵐ × aⁿ = aᵐ⁺ⁿ       aᵐ ÷ aⁿ = aᵐ⁻ⁿ
(aᵐ)ⁿ = aᵐˣⁿ          (ab)ⁿ = aⁿbⁿ
√(a×b) = √a × √b      √(a/b) = √a / √b
√(a²×b) = a√b          a/√b = a√b/b

══════════════ CEBIR ══════════════

(a+b)² = a² + 2ab + b²       → Toplamin karesi
(a−b)² = a² − 2ab + b²       → Farkin karesi
(a+b)(a−b) = a² − b²         → Iki kare farki

Denklem: ax + b = 0 → x = −b/a
Esitsizlik: Negatif ile carp/bol → yon degisir

══════════════ GEOMETRI ══════════════

PISAGOR: c² = a² + b²        (dik ucgen)
Pisagor Ucluleri: (3,4,5) (5,12,13) (8,15,17)

Dikdortgen kosegen = √(a²+b²)
Iki nokta uzakligi = √((x₂−x₁)²+(y₂−y₁)²)

BENZERLIK: Alan orani = k²    Cevre orani = k

Eskenar ucgen alani = (a²√3)/4
Eskenar ucgen yuksekligi = (a√3)/2

══════════════ CISIMLER ══════════════

DIKDORTGENLER PRIZMASI:  V = abc,  YA = 2(ab+ac+bc)
KUP:  V = a³,  YA = 6a²
SILINDIR:  V = πr²h,  YA = 2πr(r+h)
KONI:  V = (1/3)πr²h,  YA = πr(r+l),  l=√(r²+h²)
KURE:  V = (4/3)πr³,  YA = 4πr²
YARI KURE:  V = (2/3)πr³,  YA = 3πr²

══════════════ DONUSUM GEOMETRISI ══════════════

Oteleme (a,b):  (x,y) → (x+a, y+b)
x-ekseni yansima: (x,y) → (x,−y)
y-ekseni yansima: (x,y) → (−x,y)
Orijine gore: (x,y) → (−x,−y)
90° donme: (x,y) → (−y,x)
180° donme: (x,y) → (−x,−y)
270° donme: (x,y) → (y,−x)

══════════════ OLASILIK ══════════════

P(A) = n(A)/n(S)
P(A') = 1 − P(A)
P(A ve B) = P(A) × P(B)   (bagimsiz olaylar)
0 ≤ P(A) ≤ 1
"""
},

"MAT.8.EK.LGS_TAKTIK": {
    "unite": "LGS Taktik",
    "baslik": "LGS Sinav Taktikleri ve Sik Yapilan Hatalar",
    "kazanimlar": [],
    "icerik": """
LGS MATEMATIK - TAKTIKLER VE SIK HATALAR:

══════════════ SIK YAPILAN HATALAR ══════════════

1. KAREKOK HATALARI:
   ✗ √(a+b) = √a + √b  → YANLIS!
   ✓ √(a×b) = √a × √b  → DOGRU
   ✗ √4 = ±2  → YANLIS! (√4 = 2, yalnizca pozitif)

2. USLU IFADE HATALARI:
   ✗ (a+b)² = a² + b²   → YANLIS! (ortadaki terim 2ab eksik)
   ✓ (a+b)² = a² + 2ab + b²
   ✗ −2⁴ = 16  → YANLIS! (−2⁴ = −16, (−2)⁴ = 16)

3. ESITSIZLIK HATALARI:
   ✗ −3x > 6 → x > −2   → YANLIS! (negatifle bolunce yon degisir)
   ✓ −3x > 6 → x < −2

4. OLASILIK HATALARI:
   ✗ P(A veya B) = P(A) + P(B) (her zaman degil, ortak varsa cikar)
   ✗ Olasilik 1'den buyuk olamaz

5. GEOMETRI HATALARI:
   ✗ Koni hacmi = πr²h  → YANLIS! (1/3 katsayisi unutuluyor)
   ✓ Koni hacmi = (1/3)πr²h
   ✗ Kure YA = πr²  → YANLIS!
   ✓ Kure YA = 4πr²

══════════════ LGS TAKTIKLERI ══════════════

1. SAYISAL ISLEMLER:
   - EBOB/EKOK sorularinda once asal carpanlara ayir.
   - Uslu ifadelerde tabanlari esitlemeye calis.
   - Karekoklu islemlerde once sadelelestir.

2. CEBIR:
   - Ozdeslik sormuyorsa bile ozdeslik kullanmayi dene.
   - Carpanlara ayirmada once ortak carpan parantezine al, sonra ozdeslik dene.
   - Denklem sistemlerinde yok etme yontemi genellikle daha hizli.

3. GEOMETRI:
   - Pisagor uclulerini ezberle (3-4-5, 5-12-13, 8-15-17).
   - Benzerlik sorularinda oranlari dogru eslestir.
   - Cisim sorularinda birimlere dikkat et (cm², cm³).

4. OLASILIK:
   - Once ornek uzayi tam yaz.
   - "En az bir" sorusunda tamamlayici olay kullan: P(en az 1) = 1 − P(hic yok)

5. ZAMAN YONETIMI:
   - LGS'de 20 matematik sorusu icin yaklaşık 40-45 dakika.
   - Kolay sorulari once yap, zor sorulara son dak.
   - Emin olmadigin soruyu isaretle, dona gel.
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik8_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_8_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik8_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_8_REFERANS.keys())
