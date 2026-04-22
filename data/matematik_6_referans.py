# -*- coding: utf-8 -*-
"""
6. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme alanlari:
1. Sayilar ve Nicelikler (1) - Carpanlar, Katlar, EBOB, EKOK
2. Sayilar ve Nicelikler (2) - Tam Sayilar
3. Kesirlerle Islemler
4. Oran-Oranti
5. Cebirsel Ifadeler
6. Geometrik Sekiller
7. Veri Isleme
"""

MATEMATIK_6_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: SAYILAR VE NICELIKLER (1)
#    Carpanlar, Katlar, Bolunebilme, Asal Sayilar, EBOB, EKOK
# ═══════════════════════════════════════════════════════════════

"MAT.6.1.CARPAN_KAT": {
    "unite": "Sayilar ve Nicelikler (1)",
    "baslik": "Dogal Sayilarin Carpanlari ve Katlari",
    "icerik": """
CARPAN VE KAT KAVRAMI:

1. CARPAN (BOLEN):
   - Bir sayiyi kalansiz bolen dogal sayilara o sayinin carpanlari denir.
   - 12'nin carpanlari: {1, 2, 3, 4, 6, 12}
     Cunku 12 = 1×12 = 2×6 = 3×4
   - Her dogal sayinin en kucuk carpani 1, en buyuk carpani kendisidir.
   - Carpan sayisi sinirlidir (sonlu).

2. KAT:
   - Bir sayinin dogal sayilarla carpilmasiyla elde edilen sayilara o sayinin katlari denir.
   - 5'in katlari: {0, 5, 10, 15, 20, 25, 30, ...}
   - 5×0=0, 5×1=5, 5×2=10, 5×3=15, ...
   - Her sayinin en kucuk kati 0'dir.
   - Bir sayinin katlari sonsuzdur.
   - Sifir her sayinin katidir.

3. CARPAN-KAT ILISKISI:
   - a, b'nin carpani ise b, a'nin katidir.
   - Ornek: 4, 20'nin carpanidir → 20, 4'un katidir.
   - a | b gosterimi: "a, b'yi boler" (a, b'nin carpanidir)

4. CARPAN BULMA YONTEMI:
   - 1'den baslayarak sayiyi kalansiz bolen tum sayilar yazilir.
   - Ornek: 24'un carpanlari:
     24÷1=24, 24÷2=12, 24÷3=8, 24÷4=6
     Carpanlar: {1, 2, 3, 4, 6, 8, 12, 24}
"""
},

"MAT.6.1.BOLUNEBILME": {
    "unite": "Sayilar ve Nicelikler (1)",
    "baslik": "Bolunebilme Kurallari",
    "icerik": """
BOLUNEBILME KURALLARI:

1. 2'YE BOLUNEBILME:
   - Birler basamagi cift sayi (0, 2, 4, 6, 8) olan sayilar 2'ye bolunur.
   - Ornekler: 124 (evet), 357 (hayir), 4680 (evet)

2. 3'E BOLUNEBILME:
   - Rakamlar toplami 3'un kati olan sayilar 3'e bolunur.
   - Ornek: 243 → 2+4+3 = 9 (9, 3'un kati) → 3'e bolunur
   - Ornek: 514 → 5+1+4 = 10 (10, 3'un kati degil) → 3'e bolunmez

3. 4'E BOLUNEBILME:
   - Son iki basamagi 4'e bolunen sayilar 4'e bolunur.
   - Son iki basamagi 00 olan sayilar da 4'e bolunur.
   - Ornek: 1324 → 24÷4=6 → 4'e bolunur
   - Ornek: 1518 → 18÷4=4 kalan 2 → 4'e bolunmez

4. 5'E BOLUNEBILME:
   - Birler basamagi 0 veya 5 olan sayilar 5'e bolunur.
   - Ornekler: 235 (evet), 470 (evet), 123 (hayir)

5. 6'YA BOLUNEBILME:
   - Hem 2'ye hem 3'e bolunen sayilar 6'ya bolunur.
   - Ornek: 234 → Son basamak 4 (cift, 2'ye bolunur) ve 2+3+4=9 (3'e bolunur) → 6'ya bolunur

6. 9'A BOLUNEBILME:
   - Rakamlar toplami 9'un kati olan sayilar 9'a bolunur.
   - Ornek: 738 → 7+3+8 = 18 (18, 9'un kati) → 9'a bolunur
   - Ornek: 524 → 5+2+4 = 11 (11, 9'un kati degil) → 9'a bolunmez

7. 10'A BOLUNEBILME:
   - Birler basamagi 0 olan sayilar 10'a bolunur.
   - Ornekler: 250 (evet), 1000 (evet), 345 (hayir)

ONEMLI NOT:
- Bir sayi baska bir sayiya bolunuyorsa, o sayinin tum carpanlarina da bolunur.
  Ornek: 12'ye bolunen sayi → 2, 3, 4, 6'ya da bolunur.
"""
},

"MAT.6.1.ASAL_SAYI": {
    "unite": "Sayilar ve Nicelikler (1)",
    "baslik": "Asal Sayilar ve Asal Carpanlara Ayirma",
    "icerik": """
ASAL SAYI:
- 1'den buyuk, yalnizca 1'e ve kendisine bolunen dogal sayilar.
- En kucuk asal sayi: 2
- 2, tek cift asal sayidir. Diger tum asal sayilar tektir.
- 1 asal sayi DEGILDIR (tanimdan dolayi).
- 0 asal sayi DEGILDIR.

ILK 25 ASAL SAYI:
2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
73, 79, 83, 89, 97

ASAL SAYI DEGIL (BILESIK SAYI):
- 1'den buyuk ve asal olmayan sayilar bilesik sayidir.
- Bilesik sayilarin 1 ve kendisinden baska carpanlari vardir.
- Ornekler: 4, 6, 8, 9, 10, 12, 14, 15, ...
- 1 ne asaldir ne bilesiktir (ozel sayidir).

ERATOSTHENES KALBURU:
- Asal sayilari bulmak icin kullanilan yontem.
- 1 cizilir, 2'den baslayarak her asal sayinin katlari elenir.

ASAL CARPANLARA AYIRMA:
- Bir bilesik sayiyi asal sayilarin carpimi olarak yazmak.
- Yontem: En kucuk asal bolenden baslanarak ust uste bolme yapilir.

Ornek: 60'i asal carpanlara ayirma:
  60 | 2
  30 | 2
  15 | 3
   5 | 5
   1
  60 = 2 × 2 × 3 × 5 = 2² × 3 × 5

Ornek: 84'u asal carpanlara ayirma:
  84 | 2
  42 | 2
  21 | 3
   7 | 7
   1
  84 = 2² × 3 × 7

ONEMLI:
- Her bilesik sayi, asal carpanlarinin carpimi olarak TEK bir sekilde yazilabilir
  (Aritmetigin Temel Teoremi).
- Asal carpanlara ayirma, EBOB ve EKOK hesaplamada temel aractir.
"""
},

"MAT.6.1.EBOB_EKOK": {
    "unite": "Sayilar ve Nicelikler (1)",
    "baslik": "EBOB ve EKOK",
    "icerik": """
EBOB (EN BUYUK ORTAK BOLEN):
- Iki veya daha fazla sayinin ortak carpanlarinin en buyugudur.
- Gosterim: EBOB(a, b) veya (a, b)

EBOB BULMA YONTEMLERI:

1. Carpanlarla bulma:
   - 12'nin carpanlari: {1, 2, 3, 4, 6, 12}
   - 18'in carpanlari: {1, 2, 3, 6, 9, 18}
   - Ortak carpanlar: {1, 2, 3, 6}
   - EBOB(12, 18) = 6

2. Asal carpanlarla bulma (TEMEL YONTEM):
   - Sayilarin asal carpanlarina ayrilir.
   - Ortak asal carpanlarin EN KUCUK kuvvetleri carpilir.
   - 12 = 2² × 3
   - 18 = 2 × 3²
   - Ortak asallar: 2 ve 3
   - EBOB = 2¹ × 3¹ = 6

EKOK (EN KUCUK ORTAK KAT):
- Iki veya daha fazla sayinin ortak katlarinin en kucugudur (sifir haric).
- Gosterim: EKOK(a, b) veya [a, b]

EKOK BULMA YONTEMLERI:

1. Katlarla bulma:
   - 4'un katlari: {4, 8, 12, 16, 20, 24, 28, 32, 36, ...}
   - 6'nin katlari: {6, 12, 18, 24, 30, 36, ...}
   - Ortak katlar: {12, 24, 36, ...}
   - EKOK(4, 6) = 12

2. Asal carpanlarla bulma (TEMEL YONTEM):
   - Sayilarin asal carpanlarina ayrilir.
   - Tum asal carpanlarin EN BUYUK kuvvetleri carpilir.
   - 12 = 2² × 3
   - 18 = 2 × 3²
   - EKOK = 2² × 3² = 4 × 9 = 36

EBOB VE EKOK ILISKISI:
- EBOB(a, b) × EKOK(a, b) = a × b
- Ornek: EBOB(12, 18) × EKOK(12, 18) = 6 × 36 = 216 = 12 × 18 ✓

UYGULAMA ALANLARI:
- EBOB: "En buyuk esit parcalara bolme" problemleri
  Ornek: 24 elma ve 36 portakali en cok kac kisiye esit dagitiriz? → EBOB(24,36)=12
- EKOK: "En erken birlikte tekrarlama" problemleri
  Ornek: Her 4 gunde bir A, her 6 gunde bir B geliyorsa birlikte ne zaman? → EKOK(4,6)=12
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: SAYILAR VE NICELIKLER (2) - TAM SAYILAR
# ═══════════════════════════════════════════════════════════════

"MAT.6.2.TAM_SAYILAR": {
    "unite": "Sayilar ve Nicelikler (2)",
    "baslik": "Tam Sayilar ve Sayi Dogrusu",
    "icerik": """
TAM SAYILAR:
- Tam sayilar kumesi: Z = {..., -3, -2, -1, 0, 1, 2, 3, ...}
- Pozitif tam sayilar: Z⁺ = {1, 2, 3, 4, ...} (dogal sayilarla ayni, sifir haric)
- Negatif tam sayilar: Z⁻ = {-1, -2, -3, -4, ...}
- Sifir (0): Ne pozitif ne negatiftir.

KUME ILISKISI:
- Dogal sayilar ⊂ Tam sayilar (N ⊂ Z)
- Her dogal sayi bir tam sayidir, ama her tam sayi dogal sayi degildir.
- Negatif sayilar dogal sayi degildir.

SAYI DOGRUSU:
- Yatay bir dogru uzerinde sayilarin gosterimi
- Sag tarafa gidildikce sayilar buyur
- Sol tarafa gidildikce sayilar kuculur
- 0, sayı dogrusunun orta referans noktasidir
- Pozitif sayilar 0'in saginda, negatif sayilar 0'in solundadir
- Iki ardisik tam sayi arasi esit araliklidir

TAM SAYILARIN KARSILASTIRILMASI:
- Her pozitif sayi sifirdan buyuktur: 5 > 0
- Her negatif sayi sifirdan kucuktur: -3 < 0
- Her pozitif sayi her negatif sayidan buyuktur: 1 > -100
- Negatif sayilarda: Mutlak degeri kucuk olan buyuktur!
  -2 > -5 (cunku |-2| < |-5|)
- Siralama: ... < -3 < -2 < -1 < 0 < 1 < 2 < 3 < ...

ZITLIK KAVRAMI:
- Bir tam sayinin zit isareti (ters isareti)
- 5'in zitti: -5
- -3'un zitti: 3
- 0'in zitti: 0 (kendisi)
- Bir sayi ile zittinin toplami her zaman 0'dir: a + (-a) = 0
"""
},

"MAT.6.2.TAM_SAYILARDA_ISLEM": {
    "unite": "Sayilar ve Nicelikler (2)",
    "baslik": "Tam Sayilarda Toplama, Cikarma ve Mutlak Deger",
    "icerik": """
MUTLAK DEGER:
- Bir sayinin sayi dogrusunda sifira olan uzakligi.
- Gosterim: |a|
- Her zaman pozitif veya sifirdir (negatif olamaz).
- |5| = 5, |-5| = 5, |0| = 0
- |a| = |-a| (bir sayi ile zittinin mutlak degeri esittir)

TAM SAYILARDA TOPLAMA:

1. Ayni isaretli iki sayinin toplami:
   - Mutlak degerler toplanir, ortak isaret verilir.
   - (+3) + (+5) = +8
   - (-4) + (-7) = -11

2. Farkli isaretli iki sayinin toplami:
   - Mutlak degerler cikarilir (buyukten kucuk), mutlak degeri buyuk olanin isareti verilir.
   - (+8) + (-3) = +5 (|8| > |3|, isaret +)
   - (-10) + (+4) = -6 (|-10| > |4|, isaret -)

3. Bir sayi ile zittinin toplami:
   - (+7) + (-7) = 0
   - (-3) + (+3) = 0

TAM SAYILARDA CIKARMA:
- Cikarma islemi, ikinci sayinin zittini toplama donusturulur.
- a - b = a + (-b)
- (+5) - (+3) = (+5) + (-3) = +2
- (+5) - (-3) = (+5) + (+3) = +8
- (-5) - (+3) = (-5) + (-3) = -8
- (-5) - (-3) = (-5) + (+3) = -2

ISLEM ONCELIGI (TAM SAYILARDA):
1. Parantez icindeki islemler
2. Carpma ve bolme (soldan saga)
3. Toplama ve cikarma (soldan saga)

ONEMLI KURALLAR:
- Ard arda iki eksi isareti arti olur: -(-5) = +5
- Ard arda arti ve eksi isareti eksi olur: +(-3) = -3
- Toplama islemi degisme ozelligine sahiptir: a + b = b + a
- Toplama islemi birleme ozelligine sahiptir: (a + b) + c = a + (b + c)
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: KESIRLERLE ISLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.6.3.KESIR_CARPMA_BOLME": {
    "unite": "Kesirlerle Islemler",
    "baslik": "Kesirlerle Carpma ve Bolme Islemleri",
    "icerik": """
KESIRLERDE CARPMA:

1. Kesir × Kesir:
   - Paylar carpilir, paydalar carpilir.
   - (a/b) × (c/d) = (a×c) / (b×d)
   - Ornek: 2/3 × 4/5 = 8/15
   - Ornek: 3/4 × 2/7 = 6/28 = 3/14

2. Tam sayi × Kesir:
   - Tam sayi 1 paydali kesir olarak yazilir.
   - 5 × 3/4 = 5/1 × 3/4 = 15/4 = 3 3/4
   - 4 × 2/3 = 8/3 = 2 2/3

3. Tam sayili kesir × Kesir:
   - Tam sayili kesir once bilesik kesre cevrilir.
   - 2 1/3 × 3/5 = 7/3 × 3/5 = 21/15 = 7/5 = 1 2/5

4. CAPRAZ SADELEŞTIRME:
   - Carpma isleminde bir paylayi diger paydayla sadelestirmek mumkundur.
   - 3/8 × 4/9 → 3 ile 9'u 3'e bol (1 ve 3), 4 ile 8'i 4'e bol (1 ve 2)
   - = 1/2 × 1/3 = 1/6

KESIRLERDE BOLME:

1. Kural: Bolen kesrin TERSINE cevrilerek carpilir.
   - (a/b) ÷ (c/d) = (a/b) × (d/c)
   - Ornek: 3/4 ÷ 2/5 = 3/4 × 5/2 = 15/8 = 1 7/8
   - Ornek: 5/6 ÷ 1/3 = 5/6 × 3/1 = 15/6 = 5/2 = 2 1/2

2. Tam sayi ÷ Kesir:
   - 6 ÷ 2/3 = 6/1 × 3/2 = 18/2 = 9
   - "6 icinde 2/3'ler kac tane var?" → 9 tane

3. Kesir ÷ Tam sayi:
   - 3/4 ÷ 2 = 3/4 × 1/2 = 3/8
   - "3/4'un yarisi nedir?" → 3/8

ONEMLI KURALLAR:
- 1 ile carpma: a/b × 1 = a/b (etkisiz eleman)
- 0 ile carpma: a/b × 0 = 0 (yutan eleman)
- Sifira bolme TANIMSIZDIR.
- Bir sayinin kendisiyle bolu = 1 (a/b ÷ a/b = 1)
- Carpma degisme ve birleme ozelligine sahiptir.
- Bolme degisme ozelligine sahip DEGILDIR.
"""
},

"MAT.6.3.ONDALIK_ISLEM": {
    "unite": "Kesirlerle Islemler",
    "baslik": "Ondalik Gosterimlerle Islemler",
    "icerik": """
ONDALIK KESIR HATIRLATMA:
- 0,5 = 5/10 = 1/2
- 0,25 = 25/100 = 1/4
- 0,1 = 1/10
- 0,01 = 1/100
- 0,001 = 1/1000

ONDALIK KESIRLERDE CARPMA:

1. Ondalik × Tam sayi:
   - Normal carpma yapilir, sonuca virgul konur.
   - 2,5 × 3 = 7,5
   - 0,12 × 4 = 0,48

2. Ondalik × Ondalik:
   - Virguller kaldirilir, normal carpma yapilir.
   - Sonuctaki ondalik basamak sayisi = iki sayinin ondalik basamak sayilari toplami.
   - 1,2 × 0,3 = 0,36 (1+1=2 ondalik basamak)
   - 2,5 × 1,4 = 3,50 = 3,5 (1+1=2 ondalik basamak)
   - 0,03 × 0,2 = 0,006 (2+1=3 ondalik basamak)

3. 10, 100, 1000 ile carpma:
   - Virgul saga kaydirilir.
   - 2,345 × 10 = 23,45 (1 basamak saga)
   - 2,345 × 100 = 234,5 (2 basamak saga)
   - 2,345 × 1000 = 2345 (3 basamak saga)

ONDALIK KESIRLERDE BOLME:

1. Ondalik ÷ Tam sayi:
   - Normal bolme yapilir, virgul ayni hizaya konur.
   - 7,5 ÷ 3 = 2,5
   - 0,48 ÷ 4 = 0,12

2. Ondalik ÷ Ondalik:
   - Bolen tam sayiya cevrilerek bolunur (her ikisinin virgulu ayni yonde kaydirilir).
   - 4,5 ÷ 0,5 → 45 ÷ 5 = 9
   - 0,36 ÷ 0,06 → 36 ÷ 6 = 6
   - 7,2 ÷ 0,3 → 72 ÷ 3 = 24

3. 10, 100, 1000'e bolme:
   - Virgul sola kaydirilir.
   - 234,5 ÷ 10 = 23,45 (1 basamak sola)
   - 234,5 ÷ 100 = 2,345 (2 basamak sola)
   - 234,5 ÷ 1000 = 0,2345 (3 basamak sola)

KESIR ↔ ONDALIK DONUSUMU:
- Kesirden ondaliga: Pay ÷ Payda
  3/4 = 3 ÷ 4 = 0,75
  1/8 = 1 ÷ 8 = 0,125
- Ondaliktan kesire: Virgulden sonraki basamak sayisi kadar 10'un kuvveti paydaya yazilir.
  0,6 = 6/10 = 3/5
  0,125 = 125/1000 = 1/8
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: ORAN-ORANTI
# ═══════════════════════════════════════════════════════════════

"MAT.6.4.ORAN_ORANTI": {
    "unite": "Oran-Oranti",
    "baslik": "Oran Kavrami, Dogru Oranti ve Ters Oranti",
    "icerik": """
ORAN:
- Ayni turden iki niceligin birbirine bolunmesiyle elde edilen iliskidir.
- Gosterim: a/b veya a:b (a bolu b orani)
- Ornek: Sinifta 12 kiz, 18 erkek varsa kiz/erkek orani = 12/18 = 2/3
- Oran bir BIRIM degildir, birimsiz bir sayidir.
- Oranin basitlestirilmesi: Pay ve payda ortak bolene bolunur.
  12:18 = 2:3 (her ikisi 6'ya bolundu)

ORANTI:
- Iki oranin birbirine esit olmasidir.
- a/b = c/d ise bu bir orantidir.
- Gosterim: a:b = c:d
- Capraz carpim kurali: a×d = b×c (ic carpim = dis carpim)
- Ornek: 2/3 = 8/12 → 2×12 = 3×8 → 24 = 24 ✓

BILINMEYEN BULMA:
- x/3 = 8/12 → x×12 = 3×8 → 12x = 24 → x = 2
- 5/x = 15/9 → 5×9 = x×15 → 45 = 15x → x = 3

DOGRU ORANTI:
- Bir nicelik artarken diger nicelik de AYNI ORANDA artiyorsa dogru orantidir.
- y/x = k (sabit) → y = k × x
- k: orantı sabiti
- Ornek: 3 kalem 12 TL ise, 5 kalem kac TL?
  3/12 = 5/x → 3x = 60 → x = 20 TL
- Ornek: 2 saat → 100 km ise, 5 saat → ? km
  2/100 = 5/x → 2x = 500 → x = 250 km

DOGRU ORANTI GRAFIGI:
- Orijinden (0,0) gecen dogru bir cizgidir.
- Yatay eksen: Bagimsiz degisken (x)
- Dikey eksen: Bagimli degisken (y)

TERS ORANTI:
- Bir nicelik artarken diger nicelik AYNI ORANDA azaliyorsa ters orantidir.
- x × y = k (sabit)
- Ornek: 4 isci bir isi 6 gunde bitirir. 3 isci ayni isi kac gunde bitirir?
  4 × 6 = 3 × x → 24 = 3x → x = 8 gun
  (Isci azaldikca sure artar)
- Ornek: 60 km/saat hizla 3 saatte gidilen yol, 90 km/saat hizla kac saatte gidilir?
  60 × 3 = 90 × x → 180 = 90x → x = 2 saat

DOGRU ORANTI MI TERS ORANTI MI?
- Biri artarken digeri de artiyorsa → DOGRU ORANTI
- Biri artarken digeri azaliyorsa → TERS ORANTI
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. OGRENME ALANI: CEBIRSEL IFADELER
# ═══════════════════════════════════════════════════════════════

"MAT.6.5.CEBIR": {
    "unite": "Cebirsel Ifadeler",
    "baslik": "Cebirsel Ifadeler ve Bir Bilinmeyenli Denklemler",
    "icerik": """
CEBIRSEL IFADE:
- Sayi, degisken ve islem isaretlerinden olusan matematiksel ifade.
- Degisken: Bilinmeyen sayiyi temsil eden harf (x, y, a, n, ...)

SOZEL IFADEYI CEBIRSEL IFADEYE CEVIRME:
- "Bir sayinin 3 kati" → 3x
- "Bir sayinin 5 fazlasi" → x + 5
- "Bir sayinin 2 kati ile 7'nin toplami" → 2x + 7
- "Bir sayinin yarisi eksi 4" → x/2 - 4
- "Iki sayinin toplami" → x + y
- "Bir sayinin karesi" → x²

CEBIRSEL IFADELERDE SADESLETIRME:
- Benzer terimler toplanir/cikarilir.
- Benzer terimler: Degiskeni ve kuvveti ayni olan terimler.
- 3x + 5x = 8x
- 7a - 2a = 5a
- 4x + 3y + 2x - y = (4x + 2x) + (3y - y) = 6x + 2y
- 5x + 3 - 2x + 7 = 3x + 10

CEBIRSEL IFADEDE DEGER HESAPLAMA:
- x = 3 icin 2x + 5 = 2(3) + 5 = 6 + 5 = 11
- a = 4, b = 2 icin 3a - 2b = 3(4) - 2(2) = 12 - 4 = 8

BIR BILINMEYENLI DENKLEM:
- Icinde bir bilinmeyen (degisken) bulunan esitlik.
- Amac: Bilinmeyenin degerini bulmak.

DENKLEM COZME (TERS ISLEM YONTEMI):
1. Toplama ↔ Cikarma
   - x + 5 = 12 → x = 12 - 5 → x = 7
   - x - 8 = 3 → x = 3 + 8 → x = 11

2. Carpma ↔ Bolme
   - 4x = 28 → x = 28 ÷ 4 → x = 7
   - x/3 = 9 → x = 9 × 3 → x = 27

3. Cok islemli denklemler:
   - 2x + 3 = 15 → 2x = 15 - 3 → 2x = 12 → x = 6
   - 3x - 7 = 20 → 3x = 20 + 7 → 3x = 27 → x = 9
   - (x + 4)/2 = 10 → x + 4 = 20 → x = 16

DENKLEM DOGRULAMA:
- Bulunan degeri denkleme yerleştir.
- 2x + 3 = 15, x = 6 → 2(6) + 3 = 12 + 3 = 15 ✓

ESITLIK ILKESI:
- Esitligin her iki tarafina ayni islem uygulanirsa esitlik bozulmaz.
- x + 5 = 12 → Her iki taraftan 5 cikar → x = 7
- 3x = 21 → Her iki tarafi 3'e bol → x = 7
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. OGRENME ALANI: GEOMETRIK SEKILLER
# ═══════════════════════════════════════════════════════════════

"MAT.6.6.ACI_COKGEN": {
    "unite": "Geometrik Sekiller",
    "baslik": "Acilar ve Cokgenler",
    "icerik": """
ACILARDA HATIRLATMA:
- Dar aci: 0° < aci < 90°
- Dik aci: 90°
- Genis aci: 90° < aci < 180°
- Dogru aci: 180°
- Yansima acisi: 180° < aci < 360°
- Tam aci: 360°

KOMSU ACILAR VE TAMAMLAYICI ACILAR:
- Tumler (bütünleyen) acilar: Toplami 90° → a + b = 90°
  Ornek: 35° ve 55° tumler acilardir.
- Butunler (tamamlayan) acilar: Toplami 180° → a + b = 180°
  Ornek: 110° ve 70° butunler acilardir.

TERS ACILAR (KOSE ACILARI):
- Iki dogrunun kesiştigi noktada karsi karşıya olusan acilar.
- Ters acilar birbirine esittir.

COKGEN:
- En az 3 dogru parcasiyla sinirlandirilmis kapalı duz sekil.
- n-gen: n kenari olan cokgen (3-gen = ucgen, 4-gen = dortgen, ...)

COKGENLERIN IC ACILARI TOPLAMI:
- Formul: (n - 2) × 180°
  * Ucgen (n=3): (3-2) × 180° = 180°
  * Dortgen (n=4): (4-2) × 180° = 360°
  * Besgen (n=5): (5-2) × 180° = 540°
  * Altigen (n=6): (6-2) × 180° = 720°

DUZGUN COKGEN:
- Tum kenarlari ve tum acilari esit olan cokgen.
- Duzgun ucgen (eskenar): Her aci = 60°
- Duzgun dortgen (kare): Her aci = 90°
- Duzgun besgen: Her aci = 108°
- Duzgun altigen: Her aci = 120°
- Bir ic aci = (n-2) × 180° / n

DORTGEN CESITLERI HATIRLATMA:
- Kare: 4 kenar esit, 4 aci dik
- Dikdortgen: Karsi kenarlar esit, 4 aci dik
- Paralelkenar: Karsi kenarlar paralel ve esit
- Yamuk: Yalnizca iki kenari paralel
- Eskenar dortgen: 4 kenar esit (acilar dik olmayabilir)
"""
},

"MAT.6.6.CEMBER_DAIRE_ALAN": {
    "unite": "Geometrik Sekiller",
    "baslik": "Cemberin Uzunlugu ve Dairenin Alani",
    "icerik": """
π (PI) SAYISI:
- Cemberin cevresinin capina orani: π = C/d
- π ≈ 3,14 (6. sinifta bu yaklasik deger kullanilir)
- π irrasyonel bir sayidir (tam olarak yazilamaz)

CEMBERIN UZUNLUGU (CEVRESI):
- C = 2πr (yaricap biliniyorsa)
- C = πd (cap biliniyorsa)
- Ornek: r = 5 cm → C = 2 × 3,14 × 5 = 31,4 cm
- Ornek: d = 14 cm → C = 3,14 × 14 = 43,96 cm

DAIRENIN ALANI:
- A = πr²
- Ornek: r = 7 cm → A = 3,14 × 7² = 3,14 × 49 = 153,86 cm²
- Ornek: r = 10 cm → A = 3,14 × 100 = 314 cm²

YARICAP → CAP DONUSUMU:
- d = 2r → r = d/2
- Ornek: d = 20 cm → r = 10 cm

YARI DAIRE:
- Yari dairenin alani = πr²/2
- Yari dairenin cevresi = πr + 2r = πr + d (egri kisim + cap)
- Ornek: r = 6 cm → Alan = 3,14 × 36 / 2 = 56,52 cm²

CEYREK DAIRE:
- Ceyrek dairenin alani = πr²/4
- Ceyrek dairenin cevresi = πr/2 + 2r (egri kisim + 2 yaricap)

HALKA (IKI DAIRE ARASI ALAN):
- Ic yaricap: r, Dis yaricap: R
- Halka alani = πR² - πr² = π(R² - r²)
- Ornek: R = 10, r = 6 → Alan = 3,14 × (100 - 36) = 3,14 × 64 = 200,96 cm²

PRATIK PROBLEMLER:
- Bisiklet tekerleginin cemberi → katedilen yol (C × tur sayisi)
- Dairesel bahce alani → cimleme, boyama hesaplamalari
- Pi gunu: 14 Mart (3/14) tarihinde kutlanir
"""
},

"MAT.6.6.PRIZMA_HACIM": {
    "unite": "Geometrik Sekiller",
    "baslik": "Prizmalar ve Hacim Hesaplama",
    "icerik": """
PRIZMA:
- Iki paralel ve esit tabani olan, yan yuzleri dikdortgen (veya paralelkenar) olan geometrik cisim.
- Prizmanin adi tabana gore belirlenir.

DIKDORTGENLER PRIZMASI:
- 6 yuzu dikdortgen (veya kare) olan prizma
- 3 farkli kenar uzunlugu: a (uzunluk), b (genislik), c (yukseklik)
- Kose sayisi: 8
- Ayrıt sayisi: 12
- Yuz sayisi: 6

Hacim:
- V = a × b × c (uzunluk × genislik × yukseklik)
- V = Taban alani × Yukseklik
- Ornek: a=5 cm, b=3 cm, c=4 cm → V = 5 × 3 × 4 = 60 cm³

Yuzey Alani:
- Toplam yuzey alani = 2(ab + ac + bc)
- Ornek: a=5, b=3, c=4 → YA = 2(15 + 20 + 12) = 2 × 47 = 94 cm²

KUP:
- Ozel dikdortgenler prizmasi: Tum kenarlari esit (a = b = c)
- 6 yuzu kare
- Hacim: V = a³ (a × a × a)
  Ornek: a = 4 cm → V = 4³ = 64 cm³
- Yuzey alani: YA = 6a²
  Ornek: a = 4 cm → YA = 6 × 16 = 96 cm²

HACIM BIRIMLERI:
- 1 cm³ = 1 mL (mililitre)
- 1 dm³ = 1 L (litre) = 1000 cm³
- 1 m³ = 1000 L = 1.000.000 cm³

HACIM BIRIM DONUSUMLERI:
- m³ → dm³: × 1000
- dm³ → cm³: × 1000
- cm³ → mm³: × 1000
- Buyukten kucuge her basamakta 1000 ile carpilir

SIVI KAPASITESI:
- Bir kabin icine alabildigi sivi miktari = ic hacmi
- Ornek: 20 cm × 15 cm × 10 cm kutu → V = 3000 cm³ = 3000 mL = 3 L

PRATIKTE HACIM PROBLEMLERI:
- Havuz doldurma: Havuzun hacmi = uzunluk × genislik × derinlik
- Kutu kaplama: Yuzey alani hesaplama
- Istif problemleri: Kup veya dikdortgenler prizmalarini ust uste dizme
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. OGRENME ALANI: VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.6.7.VERI_ANALIZI": {
    "unite": "Veri Isleme",
    "baslik": "Veri Analizi, Grafikler ve Aritmetik Ortalama",
    "icerik": """
VERI TOPLAMA VE DUZENLEME:
- Veri: Arastirma sonucu elde edilen bilgi, sayi veya olcumler.
- Ham veri: Duzenlenmemis, islanmamis veri.
- Siklik (frekans) tablosu: Verilerin kac kez tekrarlandigini gosteren tablo.

SIKLIK TABLOSU ORNEGI:
  Not Araligi | Ogrenci Sayisi (Siklik)
  0-49        | 3
  50-69       | 8
  70-84       | 12
  85-100      | 7
  Toplam      | 30

GRAFIK TURLERI:

1. SUTUN GRAFIGI (Bar Chart):
   - Kategorik verileri karsilastirmak icin kullanilir.
   - Yatay eksen: Kategoriler (ders adlari, sehirler, vb.)
   - Dikey eksen: Sayisal degerler (siklik, miktar, vb.)
   - Sutunlar arasinda esit bosluk bulunur.
   - Sutunlarin yuksekligi degeri temsil eder.
   - Hem dikey hem yatay sutun grafigi olabilir.

2. CIZGI GRAFIGI (Line Chart):
   - Zamana bagli degisimi gostermek icin idealdir.
   - Noktalar isaretlenir ve duz cizgiyle birlestirilir.
   - Artis, azalis ve sabit kalma egilimlerini gosterir.
   - Ornekler: Aylik sicaklik, yillik nufus, haftalik satis

3. PASTA (DAIRE) GRAFIGI:
   - Bir butunun parcalarini oransal olarak gosterir.
   - Tam daire = %100 = 360°
   - Her dilim, toplam icindeki orani gosterir.
   - Dilimin acisi = (deger / toplam) × 360°

GRAFIK OKUMA VE YORUMLAMA:
- Baslik: Grafigin ne anlattigi
- Eksen etiketleri: Her eksenin ne gosterdigi
- Olcek: Eksenlerdeki degerlerin araligi
- En buyuk/en kucuk deger
- Artis/azalis egilimi
- Karsilastirma: Kategoriler arasi farklar

ARITMETIK ORTALAMA:
- Tum degerlerin toplami bolü deger sayisi
- Formul: Ortalama = (x₁ + x₂ + ... + xₙ) / n
- Ornek: 70, 85, 90, 65, 80 → Ortalama = (70+85+90+65+80)/5 = 390/5 = 78

ARITMETIK ORTALAMA OZELLIKLERI:
- Ortalama her zaman en kucuk ve en buyuk deger arasindadir.
- Tum degerler esitse ortalama da o degere esittir.
- Bir deger degistiginde ortalama da degisir.
- Ortalama = Toplam / Sayi → Toplam = Ortalama × Sayi
  Ornek: 5 sinavin ortalamasi 80 ise toplam puan = 80 × 5 = 400

ORTANCA (MEDYAN):
- Veriler kucukten buyuge siralandiginda ortadaki deger.
- n tek ise: (n+1)/2. deger
- n cift ise: Ortadaki iki degerin ortalamasi
- Ornek: 3, 7, 9, 12, 15 → Ortanca = 9 (3. deger)
- Ornek: 3, 7, 9, 12 → Ortanca = (7+9)/2 = 8

TEPE DEGER (MOD):
- En cok tekrar eden deger.
- Birden fazla tepe deger olabilir.
- Ornek: 5, 3, 7, 5, 9, 5, 3 → Tepe deger = 5

ARALIK:
- En buyuk deger - En kucuk deger
- Verinin yayilimini gosterir.
- Ornek: 45, 67, 89, 23, 78 → Aralik = 89 - 23 = 66
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik6_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_6_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik6_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_6_REFERANS.keys())


def get_matematik6_by_unite(unite_name: str) -> list:
    """Belirtilen uniteye ait tum referanslari dondurur."""
    results = []
    for key, val in MATEMATIK_6_REFERANS.items():
        if unite_name.lower() in val["unite"].lower():
            results.append((key, val))
    return results


def get_matematik6_summary() -> dict:
    """Her unite icin konu basliklarinin ozetini dondurur."""
    summary = {}
    for key, val in MATEMATIK_6_REFERANS.items():
        unite = val["unite"]
        if unite not in summary:
            summary[unite] = []
        summary[unite].append({"anahtar": key, "baslik": val["baslik"]})
    return summary
