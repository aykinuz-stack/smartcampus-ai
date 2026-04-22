# -*- coding: utf-8 -*-
"""
7. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme alanlari:
1. Sayilar ve Islemler
2. Cebir
3. Geometri ve Olcme
4. Veri Isleme
"""

MATEMATIK_7_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: SAYILAR VE ISLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.7.1.TAM_SAYILARLA_ISLEMLER": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Tam Sayilarla Islemler",
    "kazanimlar": ["M.7.1.1.1", "M.7.1.1.2", "M.7.1.1.3", "M.7.1.1.4", "M.7.1.1.5"],
    "icerik": """
TAM SAYILAR KUMESI:
Z = {..., -3, -2, -1, 0, 1, 2, 3, ...}
- Pozitif tam sayilar: Z+ = {1, 2, 3, ...}
- Negatif tam sayilar: Z- = {..., -3, -2, -1}
- Sifir ne pozitif ne negatiftir.

TAM SAYILARDA TOPLAMA:
- Ayni isaretli iki tam sayi toplanirken: Mutlak degerler toplanir, ortak isaret yazilir.
  Ornek: (+5) + (+3) = +8    |    (-4) + (-6) = -10
- Farkli isaretli iki tam sayi toplanirken: Mutlak degerler cikarilir (buyukten kucuk), mutlak degeri buyuk olanin isareti yazilir.
  Ornek: (+7) + (-3) = +4    |    (-9) + (+4) = -5

TAM SAYILARDA CIKARMA:
- Cikarma islemi, cikarin isaretini degistirip toplamaya donusturulur.
  a - b = a + (-b)
  Ornek: (+8) - (+3) = (+8) + (-3) = +5
  Ornek: (-5) - (-2) = (-5) + (+2) = -3
  Ornek: (+4) - (+9) = (+4) + (-9) = -5

TAM SAYILARDA CARPMA:
- Ayni isaretli iki sayi carpilirsa sonuc POZiTiF:
  (+) x (+) = (+)    |    (-) x (-) = (+)
  Ornek: (+3) x (+4) = +12    |    (-5) x (-3) = +15
- Farkli isaretli iki sayi carpilirsa sonuc NEGATiF:
  (+) x (-) = (-)    |    (-) x (+) = (-)
  Ornek: (+6) x (-2) = -12    |    (-7) x (+3) = -21
- Sifir ile carpma: a x 0 = 0

TAM SAYILARDA BOLME:
- Isaret kurallari carpma ile aynidir:
  (+) / (+) = (+)    |    (-) / (-) = (+)
  (+) / (-) = (-)    |    (-) / (+) = (-)
  Ornek: (+20) / (+4) = +5    |    (-18) / (-3) = +6
  Ornek: (+15) / (-5) = -3    |    (-24) / (+6) = -4
- Sifira bolme tanimsizdir: a / 0 = TANIMSIZ

ISLEM ONCELIGI (PEMDAS/BODMAS):
1. Parantez icindeki islemler
2. Us alma
3. Carpma ve bolme (soldan saga)
4. Toplama ve cikarma (soldan saga)
Ornek: 3 + 2 x (4 - 1) = 3 + 2 x 3 = 3 + 6 = 9

TAM SAYILARDA US ALMA (M.7.1.1.5):
- a^n = a x a x ... x a (n tane a carpimi)
- Pozitif tabanda: Her zaman pozitif sonuc
  (+2)^3 = 8    |    (+3)^4 = 81
- Negatif tabanda:
  * Cift us → pozitif sonuc: (-2)^4 = +16
  * Tek us → negatif sonuc: (-2)^3 = -8
- Ozel durumlar:
  a^0 = 1 (a ≠ 0)    |    a^1 = a    |    0^n = 0 (n > 0)
"""
},

"MAT.7.1.RASYONEL_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Rasyonel Sayilar",
    "kazanimlar": ["M.7.1.2.1", "M.7.1.2.2", "M.7.1.2.3"],
    "icerik": """
RASYONEL SAYI TANIMI:
- a/b seklinde yazilabilen sayilara rasyonel sayi denir (a, b tam sayi; b ≠ 0).
- Q ile gosterilir: Q = {a/b | a, b ∈ Z, b ≠ 0}
- Tum tam sayilar rasyonel sayidir (orn: 5 = 5/1).
- Tum kesirler rasyonel sayidir.
- Kume iliskisi: N ⊂ Z ⊂ Q (Dogal sayilar ⊂ Tam sayilar ⊂ Rasyonel sayilar)

RASYONEL SAYILARIN DENKLIK VE SADELEŞTIRME:
- a/b = (a x k) / (b x k) — genisletme (k ≠ 0)
  Ornek: 2/3 = 4/6 = 6/9 = 8/12
- a/b = (a / k) / (b / k) — sadelestirme (k, OBEB)
  Ornek: 12/18 = 6/9 = 2/3 (OBEB = 6)

RASYONEL SAYILARIN ONDALIK GOSTERIMI:
- Sonlu ondalik: 3/4 = 0,75    |    1/8 = 0,125
- Devirli ondalik: 1/3 = 0,333... = 0,3̄    |    2/11 = 0,1818... = 0,18̄
- Her rasyonel sayi sonlu veya devirli ondalik olarak yazilabilir.

SAYI DOGRUSU UZERINDE RASYONEL SAYILAR:
- Rasyonel sayilar sayi dogrusu uzerinde tam olarak gosterilebilir.
- Iki rasyonel sayi arasinda sonsuz sayida rasyonel sayi vardir (yogunluk ozelligi).
- Siralama: Paydalari esitlenerek veya ondalik gosterime donusturerek karsilastirilir.
  Ornek: 2/5 ile 3/7 → 14/35 ile 15/35 → 2/5 < 3/7

RASYONEL SAYILARIN MUTLAK DEGERI:
- |a/b| = sayi dogrusunda sifira olan uzaklik
- |3/4| = 3/4    |    |-5/2| = 5/2    |    |0| = 0
- Mutlak deger daima sifir veya pozitiftir.

RASYONEL SAYILARIN ZITLIĞI (KARSI SAYI):
- a/b sayisinin zitti (karsi sayisi) = -a/b
- Bir sayi ile zittinin toplami sifirdir: a/b + (-a/b) = 0
"""
},

"MAT.7.1.RASYONEL_ISLEMLER": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Rasyonel Sayilarla Islemler",
    "kazanimlar": ["M.7.1.3.1", "M.7.1.3.2", "M.7.1.3.3"],
    "icerik": """
RASYONEL SAYILARDA TOPLAMA VE CIKARMA:

1. Paydalari esit ise:
   a/c + b/c = (a + b) / c
   Ornek: 2/7 + 3/7 = 5/7    |    5/9 - 2/9 = 3/9 = 1/3

2. Paydalari farkli ise: Ortak payda bulunur (EKOK).
   a/b + c/d = (a x d + c x b) / (b x d) veya EKOK ile
   Ornek: 1/3 + 1/4 = 4/12 + 3/12 = 7/12
   Ornek: 3/5 - 1/3 = 9/15 - 5/15 = 4/15

3. Bileşik kesirlerle islem:
   Oncelikle bileşik kesir = tam kisim x payda + pay / payda
   Ornek: 2 1/3 + 1 2/5 = 7/3 + 7/5 = 35/15 + 21/15 = 56/15 = 3 11/15

RASYONEL SAYILARDA CARPMA:
- a/b x c/d = (a x c) / (b x d)
  Ornek: 2/3 x 4/5 = 8/15
  Ornek: (-3/4) x (2/7) = -6/28 = -3/14
- Capraz saDelestirme yapilabilir:
  Ornek: 6/7 x 14/9 → (6 ve 9'u 3'e sadElestir, 7 ve 14'u 7'ye sadElestir) = 2/1 x 2/3 = 4/3

RASYONEL SAYILARDA BOLME:
- a/b ÷ c/d = a/b x d/c (ikinci kesrin tersi ile carpilir)
  Ornek: 3/4 ÷ 2/5 = 3/4 x 5/2 = 15/8 = 1 7/8
  Ornek: (-5/6) ÷ (10/3) = (-5/6) x (3/10) = -15/60 = -1/4
- Sifir ile bolme tanimsizdir: a/b ÷ 0 = TANIMSIZ

RASYONEL SAYILARIN TERS (CARPMAYA GORE TERS):
- a/b sayisinin tersi = b/a (a ≠ 0, b ≠ 0)
- Bir sayi ile tersinin carpimi 1'dir: (a/b) x (b/a) = 1
- 0'in carpmaya gore tersi yoktur.
  Ornek: 3/5'in tersi = 5/3    |    -2/7'nin tersi = -7/2

ISLEM ONCELIGI (RASYONEL SAYILARDA):
1. Parantez
2. Us alma
3. Carpma ve bolme (soldan saga)
4. Toplama ve cikarma (soldan saga)
Ornek: 1/2 + 3/4 x 2/3 = 1/2 + 6/12 = 1/2 + 1/2 = 1
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: CEBIR
# ═══════════════════════════════════════════════════════════════

"MAT.7.2.CEBIRSEL_IFADELER": {
    "unite": "Cebir",
    "baslik": "Cebirsel Ifadeler",
    "kazanimlar": ["M.7.2.1.1", "M.7.2.1.2", "M.7.2.1.3", "M.7.2.1.4"],
    "icerik": """
CEBIRSEL IFADE TANIMI:
- Sayilar, degiskenler (harfler) ve islem isaretleriyle olusturulan matematiksel ifadeler.
- Degisken: Bilinmeyen veya degisen degeri temsil eden harf (x, y, a, b, n, ...)
- Sabit: Degeri degismeyen sayi (3, -5, 1/2, ...)
- Katsayi: Degiskenin onundeki sayi (3x'te katsayi 3'tur)

TERIM VE KATSAYI:
- Terim: +/- isaretleriyle ayrilan her bir parca
  Ornek: 3x² + 5x - 7 ifadesinde terimler: 3x², 5x, -7
- Katsayi: Degiskenin onundeki sayisal carpan
  Ornek: 5x'te katsayi = 5    |    -2y²'de katsayi = -2
- x = 1x (katsayi 1)    |    -x = -1x (katsayi -1)
- Sabit terim: Degisken icermeyen terim (orn: -7)

BENZER TERIMLER:
- Ayni degiskenlerin ayni kuvvetlerini iceren terimler.
  Ornek: 3x ve 5x benzer    |    2x² ve -4x² benzer
  Ornek: 3x ve 3x² BENZER DEGIL    |    2xy ve 5yx BENZER
- Sadece benzer terimler toplanip cikartilabilir.
  Ornek: 3x + 5x = 8x    |    7x² - 2x² = 5x²
  Ornek: 3x + 2y (sadElestirilemez — farkli degiskenler)

CEBIRSEL IFADELERDE TOPLAMA VE CIKARMA (M.7.2.1.2):
- Benzer terimler birlestirilir:
  (3x + 5) + (2x - 3) = 3x + 2x + 5 - 3 = 5x + 2
  (4a² - 2a + 1) - (a² + 3a - 5) = 4a² - a² - 2a - 3a + 1 + 5 = 3a² - 5a + 6
- DIKKAT: Cikarma isleminde parantez acilirken tum terimlerin isareti degisir!

CEBIRSEL IFADELERDE CARPMA (M.7.2.1.3):
- Sayi ile carpma: k x (ax + b) = kax + kb (dagitma ozelligi)
  Ornek: 3(2x + 4) = 6x + 12
  Ornek: -2(3a - 5) = -6a + 10
- Degisken ile carpma: x(2x + 3) = 2x² + 3x
- Carpma kurali: a^m x a^n = a^(m+n)
  Ornek: x² x x³ = x^5

CEBIRSEL IFADELERIN DEGER HESAPLAMA (M.7.2.1.4):
- Degiskene sayi degeri atanarak ifadenin sayisal degeri bulunur.
  Ornek: 2x + 3 ifadesinde x = 4 → 2(4) + 3 = 8 + 3 = 11
  Ornek: a² - 3a + 2 ifadesinde a = -1 → (-1)² - 3(-1) + 2 = 1 + 3 + 2 = 6
"""
},

"MAT.7.2.ESITLIK_DENKLEM": {
    "unite": "Cebir",
    "baslik": "Esitlik ve Denklem",
    "kazanimlar": ["M.7.2.2.1", "M.7.2.2.2", "M.7.2.2.3", "M.7.2.2.4"],
    "icerik": """
DENKLEM TANIMI:
- Icinde en az bir bilinmeyen (degisken) bulunan esitlige denklem denir.
- Denklemin sol tarafi = Denklemin sag tarafi
  Ornek: 2x + 3 = 11 bir denklemdir (bilinmeyen: x)

BIRINCI DERECEDEN BIR BILINMEYENLI DENKLEM:
- ax + b = c seklinde (a ≠ 0)
- Bilinmeyenin (degiskenin) kuvveti 1'dir.
- Cozum: Bilinmeyeni yalniz birakma

DENKLEM COZME KURALLARI (TERAZI ILKESI):
1. Esitligin iki tarafina da AYNI sayi eklenebilir.
   x - 5 = 3 → x - 5 + 5 = 3 + 5 → x = 8
2. Esitligin iki tarafindan da AYNI sayi cikarilabilir.
   x + 7 = 12 → x + 7 - 7 = 12 - 7 → x = 5
3. Esitligin iki tarafi da AYNI sayiyla carpilabiLir (0 haric).
   x/3 = 4 → 3 x (x/3) = 3 x 4 → x = 12
4. Esitligin iki tarafi da AYNI sayiya bolunebiLir (0 haric).
   4x = 20 → 4x/4 = 20/4 → x = 5

TARAF DEGISTIRME (KISA YOL):
- Bir terim esitligin diger tarafina isaret DEGISTIREREK gecer.
  2x + 3 = 11 → 2x = 11 - 3 → 2x = 8 → x = 4
  3x - 7 = 2x + 5 → 3x - 2x = 5 + 7 → x = 12

DENKLEM COZUM ADIMLARI:
1. Parantezler acilir
2. Benzer terimler birlestirilir
3. Degiskenli terimler bir tarafa, sabit terimler diger tarafa tasinir
4. Bilinmeyen yalniz birakilir

ORNEKLER:
Ornek 1: 5x - 3 = 2x + 9
  5x - 2x = 9 + 3 → 3x = 12 → x = 4

Ornek 2: 3(x + 2) = 2(x - 1) + 13
  3x + 6 = 2x - 2 + 13 → 3x + 6 = 2x + 11
  3x - 2x = 11 - 6 → x = 5

Ornek 3: (x + 1)/2 = 3
  x + 1 = 6 → x = 5

DENKLEM KURMA (PROBLEM COZME) (M.7.2.2.4):
1. Bilinmeyen belirlenir (x)
2. Verilen bilgilerle denklem kurulur
3. Denklem cozulur
4. Sonuc kontrol edilir

Ornek: Bir sayinin 3 kati ile 5'in toplami 20'dir. Bu sayi kactir?
  3x + 5 = 20 → 3x = 15 → x = 5
  Kontrol: 3(5) + 5 = 15 + 5 = 20 ✓
"""
},

"MAT.7.2.ESITSIZLIK": {
    "unite": "Cebir",
    "baslik": "Esitsizlik",
    "kazanimlar": ["M.7.2.3.1", "M.7.2.3.2"],
    "icerik": """
ESITSIZLIK TANIMI:
- Iki ifade arasindaki buyukluk-kuculuk iliskisini gosteren matematiksel ifade.
- Esitsizlik sembolleri:
  < : kucuktur (orn: 3 < 5)
  > : buyuktur (orn: 7 > 2)
  ≤ : kucuk esittir (orn: x ≤ 10)
  ≥ : buyuk esittir (orn: y ≥ 0)

BIRINCI DERECEDEN BIR BILINMEYENLI ESITSIZLIK:
- ax + b < c, ax + b > c, ax + b ≤ c, ax + b ≥ c seklinde

ESITSIZLIK OZELLIKLERI:
1. Esitsizligin iki tarafina ayni sayi eklenip cikarilabilir (yon degismez).
   x - 3 > 5 → x > 8
2. Esitsizligin iki tarafi POZITIF sayiyla carpilip bolunebilir (yon degismez).
   2x < 10 → x < 5
3. Esitsizligin iki tarafi NEGATIF sayiyla carpilir veya bolunurse yon DEGISIR!
   -3x > 12 → x < -4 (isaret dondu!)
   -x ≤ 5 → x ≥ -5 (isaret dondu!)

ESITSIZLIK COZME ADIMLARI:
1. Denklem cozme adimlari uygulanir
2. Negatif sayiyla carpma/bolmede esitsizlik yonu ters cerilir
3. Cozum kumesi sayi dogrusu uzerinde gosterilir

SAYI DOGRUSU GOSTERIMI:
- < veya > : Acik nokta (o) — sinir degeri dahil degil
- ≤ veya ≥ : Dolu/kapali nokta (●) — sinir degeri dahil
- Cozum yonu okla gosterilir

ORNEKLER:
Ornek 1: 2x + 1 > 7
  2x > 6 → x > 3
  Cozum kumesi: {x | x > 3, x ∈ Z} (tam sayi cozumleri: 4, 5, 6, ...)

Ornek 2: -4x + 8 ≤ 0
  -4x ≤ -8 → x ≥ 2 (negatif sayiya bolunde yon degisti)

Ornek 3: 3(x - 1) < 2x + 5
  3x - 3 < 2x + 5 → 3x - 2x < 5 + 3 → x < 8
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: GEOMETRI VE OLCME
# ═══════════════════════════════════════════════════════════════

"MAT.7.3.DOGRULAR_ACILAR": {
    "unite": "Geometri ve Olcme",
    "baslik": "Dogrular ve Acilar",
    "kazanimlar": ["M.7.3.1.1", "M.7.3.1.2", "M.7.3.1.3"],
    "icerik": """
IKI DOGRUNUN BIRBIRINE GORE DURUMLARI:
1. Kesisen dogrular: Bir noktada kesisir.
2. Paralel dogrular: Hicbir noktada kesismez, aralarindaki uzaklik sabittir. (d₁ // d₂)
3. Cakisik dogrular: Tum noktalarda ortusur (ayni dogruya denk gelir).

KESISEN IKI DOGRUNUN OLUSTURDUGU ACILAR:
- Komsu acilar: Ortak kose ve ortak kollu, toplami 180°
- Ters acilar (KARSI ACILAR): Kose noktasinda karsi karşiya, EŞITTIR.
  Ornek: Iki dogru kesisirse 4 aci olusur. Karsi acilar esittir.
  a ve c ters aci → a = c    |    b ve d ters aci → b = d
  a + b = 180° (komsu — butunler)

PARALEL DOGRULAR VE ACILAR (M.7.3.1.2):
Bir kesen dogru iki paralel dogruyu kestiginde 8 aci olusur.

ACI ILISKILERI:
1. Yondes acilar (F konumu): Esittir.
   - Ayni yon ve konumda olan acilar.
   Ornek: a₁ = a₂ (yondes)

2. Ic ters acilar (Z konumu): Esittir.
   - Paraleller arasinda, kesenin farkli taraflarinda.
   Ornek: a₃ = a₆ (ic ters)

3. Dis ters acilar: Esittir.
   - Paralellerin disinda, kesenin farkli taraflarinda.
   Ornek: a₁ = a₈ (dis ters)

4. Ic yan acilar: Toplami 180°
   - Paraleller arasinda, kesenin ayni tarafinda.
   Ornek: a₃ + a₅ = 180° (ic yan)

ORNEKLER:
Ornek 1: d₁ // d₂, kesen dogru ile a₁ = 70° → yondes a₂ = 70°
  ic ters: 70°, dis ters: 70°, ic yan: 180° - 70° = 110°

Ornek 2: d₁ // d₂, bir aci 3x + 10° ve ic ters acisi 2x + 40°
  3x + 10 = 2x + 40 (ic ters acilar esit) → x = 30
  Acilar: 3(30) + 10 = 100°

BIR UCGENIN IC VE DIS ACILARI (M.7.3.1.3):
- Ic acilar toplami = 180°
- Dis aci = Kendisine komsu olmayan iki ic acinin toplami
  Ornek: Ucgende A = 50°, B = 60° → C = 70°, C'nin dis acisi = 50° + 60° = 110°
- Bir ucgenin dis acilari toplami = 360°
"""
},

"MAT.7.3.COKGENLER": {
    "unite": "Geometri ve Olcme",
    "baslik": "Cokgenler",
    "kazanimlar": ["M.7.3.2.1", "M.7.3.2.2"],
    "icerik": """
COKGEN TANIMI:
- En az 3 dogru parcasinin uc uca birlestirilmesiyle olusan kapalI duzlemsel sekil.
- n-gen: n kenarli cokgen

COKGENIN IC ACILAR TOPLAMI FORMULU:
  Ic acilar toplami = (n - 2) x 180°
  n = kenar sayisi

  Ucgen (n=3): (3-2) x 180° = 180°
  Dortgen (n=4): (4-2) x 180° = 360°
  Besgen (n=5): (5-2) x 180° = 540°
  Altigen (n=6): (6-2) x 180° = 720°
  Yedigen (n=7): (7-2) x 180° = 900°
  Sekizgen (n=8): (8-2) x 180° = 1080°

DUZGUN (DUZGUN = ESKENAR + ESACILI) COKGENDE BIR IC ACI:
  Bir ic aci = (n - 2) x 180° / n

  Duzgun ucgen: 180° / 3 = 60°
  Kare (duzgun dortgen): 360° / 4 = 90°
  Duzgun besgen: 540° / 5 = 108°
  Duzgun altigen: 720° / 6 = 120°

COKGENIN DIS ACILAR TOPLAMI:
- Her cokgenin dis acilar toplami = 360° (kenar sayisindan bagimsiz!)
- Duzgun cokgende bir dis aci = 360° / n

COKGENIN KOSEGEN SAYISI:
  Kosegen sayisi = n(n - 3) / 2
  Ucgen: 3(0)/2 = 0 (kosegen yok)
  Dortgen: 4(1)/2 = 2
  Besgen: 5(2)/2 = 5
  Altigen: 6(3)/2 = 9

OZEL DORTGENLER VE OZELLIKLERI (M.7.3.2.2):
1. KARE: 4 kenar esit, 4 aci 90°, kosegenleri esit ve dik, birbirini ortalar
2. DIKDORTGEN: Karsi kenarlari esit, 4 aci 90°, kosegenleri esit ve birbirini ortalar
3. ESKENAR DORTGEN (ESBAH): 4 kenar esit, karsi acilari esit, kosegenleri dik ve birbirini ortalar
4. PARALELKENAR: Karsi kenarlari paralel ve esit, karsi acilari esit, kosegenleri birbirini ortalar
5. YAMUK: Sadece iki kenari paralel (taban ve ust taban)
   - Ikizkenar yamuk: Paralel olmayan kenarlari esit, taban acilari esit

DORTGEN HIYERARSISI:
  Kare → Dikdortgen → Paralelkenar → Yamuk
  Kare → Eskenar dortgen → Paralelkenar → Yamuk
  (Her kare bir dikdortgendir, her dikdortgen bir paralelkenardir, ...)
"""
},

"MAT.7.3.CEMBER_DAIRE": {
    "unite": "Geometri ve Olcme",
    "baslik": "Cember ve Daire",
    "kazanimlar": ["M.7.3.3.1", "M.7.3.3.2", "M.7.3.3.3"],
    "icerik": """
CEMBER VE DAIRE KAVRAMLARI:
- Cember: Bir noktaya (merkez) esit uzakliktaki tum noktalarin kumesi (sadece cizgi).
- Daire: Cember ve ic bolgesinin birlesimi (alan iceren bolge).
- Merkez: O    |    Yaricap: r    |    Cap: d = 2r

CEMBERIN ELEMANLARI:
1. Yaricap (r): Merkezden cember uzerine cizilen dogru parcasi
2. Cap (d): Cember uzerindeki iki noktayi merkezden gecirerek birlestiren dogru parcasi, d = 2r
3. Kiris: Cember uzerindeki iki noktayi birlestiren dogru parcasi
   - Cap, en uzun kiristir.
4. Teget: Cembere tek bir noktada dokunan dogru
   - Teget noktasinda yaricap ile teget diktir (90°).
5. Secant (kesen): Cemberi iki noktada kesen dogru
6. Yay: Cember uzerindeki iki nokta arasinda kalan parca

CEMBERIN CEVRESI (UZUNLUGU):
  C = 2πr = πd
  π ≈ 3,14 veya 22/7

  Ornek: r = 7 cm → C = 2 x 22/7 x 7 = 44 cm
  Ornek: d = 10 cm → C = 3,14 x 10 = 31,4 cm

DAIRENIN ALANI:
  A = πr²

  Ornek: r = 5 cm → A = 3,14 x 25 = 78,5 cm²
  Ornek: d = 14 cm → r = 7 cm → A = 22/7 x 49 = 154 cm²

MERKEZ ACI VE CEVRE ACI (M.7.3.3.2):
- Merkez aci: Tepesi cemberin merkezinde olan aci.
- Cevre aci: Tepesi cember uzerinde, kollari kiris olan aci.
- ALTIN KURAL: Ayni yaya bakan cevre aci, merkez acinin YARISIDIR.
  Cevre aci = Merkez aci / 2
  Ornek: Merkez aci = 80° → Ayni yaya bakan cevre aci = 40°
- Yari cemberi goren cevre aci = 90° (Thales teoremi)

DAIRE DILIMI VE YAY UZUNLUGU (M.7.3.3.3):
- Yay uzunlugu: L = (a / 360°) x 2πr (a = merkez aci)
  Ornek: r = 10 cm, a = 72° → L = (72/360) x 2 x 3,14 x 10 = (1/5) x 62,8 = 12,56 cm

- Daire dilimi alani: A_dilim = (a / 360°) x πr²
  Ornek: r = 6 cm, a = 60° → A_dilim = (60/360) x 3,14 x 36 = (1/6) x 113,04 = 18,84 cm²
"""
},

"MAT.7.3.ALAN_OLCME": {
    "unite": "Geometri ve Olcme",
    "baslik": "Alan Olcme",
    "kazanimlar": ["M.7.3.4.1", "M.7.3.4.2"],
    "icerik": """
ALAN FORMULLERI:

1. UCGEN ALANI:
   A = (taban x yukseklik) / 2 = (a x h) / 2
   Ornek: a = 8 cm, h = 5 cm → A = (8 x 5) / 2 = 20 cm²

2. KARE ALANI:
   A = kenar x kenar = a²
   Ornek: a = 6 cm → A = 36 cm²

3. DIKDORTGEN ALANI:
   A = uzun kenar x kisa kenar = a x b
   Ornek: a = 8 cm, b = 5 cm → A = 40 cm²

4. PARALELKENAR ALANI:
   A = taban x yukseklik = a x h
   Ornek: a = 10 cm, h = 6 cm → A = 60 cm²
   NOT: Yan kenar degil, yukseklik kullanilir!

5. ESKENAR DORTGEN ALANI:
   A = (d₁ x d₂) / 2 (d₁, d₂: kosegen uzunluklari)
   Ornek: d₁ = 8 cm, d₂ = 6 cm → A = (8 x 6) / 2 = 24 cm²

6. YAMUK ALANI:
   A = ((ust taban + alt taban) x yukseklik) / 2 = ((a + c) x h) / 2
   Ornek: a = 5, c = 9, h = 6 → A = ((5 + 9) x 6) / 2 = 42 cm²

7. DAIRE ALANI:
   A = πr²
   Ornek: r = 7 cm → A = 22/7 x 49 = 154 cm²

ALAN BIRIMLERI VE DONUSUMLERI:
  1 m² = 10.000 cm² = 100 dm²
  1 dm² = 100 cm²
  1 km² = 1.000.000 m²
  1 hektar (ha) = 10.000 m²
  1 ar = 100 m²

BILESIK SEKILLERIN ALANI:
- Karmasik sekiller, bilinen basit sekillere ayrilir.
- Toplam alan = alt sekillerin alanlari toplami
- Veya: Buyuk sekilden cikartilan parcalar
  Ornek: L seklindeki bolgenin alani = Buyuk dikdortgen - Kucuk dikdortgen
"""
},

"MAT.7.3.DONUSUM_GEOMETRISI": {
    "unite": "Geometri ve Olcme",
    "baslik": "Donusum Geometrisi",
    "kazanimlar": ["M.7.3.5.1", "M.7.3.5.2", "M.7.3.5.3"],
    "icerik": """
DONUSUM GEOMETRISI:
Bir sekli belirli kurallara gore baska bir konuma tasima islemi.
Donusumlerde seklin boyutu ve bicimi DEGISMEZ (eslik donusumleri).

1. OTELEME (TRANSLASYON):
- Bir sekli belirli bir yon ve uzaklikta kaydirma.
- Her nokta ayni yon ve mesafede hareket eder.
- Oteleme vektoru: Yonu ve buyuklugu ile tanimlanir.
  Ornek: (x, y) → (x + a, y + b) seklinde her nokta (a, b) kadar kaydirilir.
  Ornek: A(2, 3) noktasi (4, -1) vektoru ile → A'(6, 2)
- Ozellikler:
  * Seklin boyutu ve sekli degismez
  * Kenar uzunluklari ve acilar korunur
  * Yon korunur (cevrilmez)

2. YANSIMA (SIMETRI):
- Bir sekli bir dogru (simetri ekseni) boyunca ayna goruntusu olusturarak tasima.
  a) x-eksenine gore yansima: (x, y) → (x, -y)
     Ornek: A(3, 5) → A'(3, -5)
  b) y-eksenine gore yansima: (x, y) → (-x, y)
     Ornek: B(-2, 4) → B'(2, 4)
  c) y = x dogrusuna gore yansima: (x, y) → (y, x)
     Ornek: C(1, 3) → C'(3, 1)
- Ozellikler:
  * Seklin boyutu ve sekli degismez
  * Kenar uzunluklari ve acilar korunur
  * Yon TERS DONER (saat yonu ↔ saat yonunun tersi)
  * Her nokta simetri eksenine esit uzakliktadir

3. DONME (ROTASYON):
- Bir sekli sabit bir nokta (donme merkezi) etrafinda belirli bir aci kadar cevirme.
- Donme merkezi, donme acisi ve donme yonu belirtilmelidir.
  * Pozitif aci: Saat yonunun tersine
  * Negatif aci: Saat yonunde
- Ozel donmeler (orijin etrafinda):
  90° donme: (x, y) → (-y, x)
  180° donme: (x, y) → (-x, -y)
  270° donme: (x, y) → (y, -x)
  360° donme: (x, y) → (x, y) (basa doner)
- Ozellikler:
  * Seklin boyutu ve sekli degismez
  * Kenar uzunluklari ve acilar korunur
  * Donme merkezine uzaklik korunur

KOORDINAT DUZLEMINDE UYGULAMALAR:
Ornek: ABC ucgeni; A(1,2), B(4,2), C(1,5)
- 3 birim saga oteleme: A'(4,2), B'(7,2), C'(4,5)
- x-eksenine yansima: A'(1,-2), B'(4,-2), C'(1,-5)
- Orijin etrafinda 180° donme: A'(-1,-2), B'(-4,-2), C'(-1,-5)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.7.4.GRAFIK_TURLERI": {
    "unite": "Veri Isleme",
    "baslik": "Cizgi ve Daire Grafikleri",
    "kazanimlar": ["M.7.4.1.1", "M.7.4.1.2", "M.7.4.1.3"],
    "icerik": """
CIZGI GRAFIGI:
- Verilerin zamana bagli degisimini gostermek icin kullanilir.
- Yatay eksen (x): Zaman (gun, hafta, ay, yil)
- Dikey eksen (y): Deger (sicaklik, nufus, satis, ...)
- Noktalar cizgiyle birlestirilir.
- Artis, azalis ve sabit kalma eGilimleri gorulur.

CIZGI GRAFIGI YORUMLAMA:
- Yukari egim → artis
- Asagi egim → azalis
- Yatay cizgi → degisim yok (sabit)
- Dik egim → hizli degisim
- Yatik egim → yavas degisim

Ornek: Bir haftalik sicaklik verileri:
  Pazartesi: 15°C, Sali: 18°C, Carsamba: 20°C, Persembe: 17°C, Cuma: 22°C
  → Genel eGilim artis, ancak Persembe gunu dusus yasanmis.

DAIRE (PASTA) GRAFIGI:
- Bir butunun parcalarini oran olarak gostermek icin kullanilir.
- Tam daire = %100 = 360°
- Her dilimin acisi = (deger / toplam) x 360°
- Her dilimin yuzdesi = (deger / toplam) x 100

Ornek: Siniftaki ogrencilerin favori spor dallari:
  Futbol: 12, Basketbol: 8, Voleybol: 6, Yuzme: 4 → Toplam: 30
  Futbol acisi = (12/30) x 360° = 144° (%40)
  Basketbol acisi = (8/30) x 360° = 96° (%26,7)
  Voleybol acisi = (6/30) x 360° = 72° (%20)
  Yuzme acisi = (4/30) x 360° = 48° (%13,3)

GRAFIK SECIMI:
- Zamana gore degisim → Cizgi grafigi
- Oransal karsilastirma → Daire grafigi
- Kategori karsilastirmasi → Sutun grafigi
- Iliskisel veri → Sacilim grafigi

GRAFIK CIZIM KURALLARI:
1. Baslik yazilir
2. Eksenler adlandirilir ve birimleri belirtilir
3. Uygun olcek secilir (duzgun aralikli)
4. Veriler dogru islenir
5. Renk/desen ile ayirt edici gosterim yapilir (daire grafiginde aciklama kutusu)
"""
},

"MAT.7.4.MERKEZI_EGILIM": {
    "unite": "Veri Isleme",
    "baslik": "Merkezi Egilim ve Yayilim Olculeri",
    "kazanimlar": ["M.7.4.2.1", "M.7.4.2.2"],
    "icerik": """
MERKEZI EGILIM OLCULERI:

1. ARITMETIK ORTALAMA (MEAN):
   Ortalama = Tum degerlerin toplami / Deger sayisi
   x̄ = (x₁ + x₂ + ... + xₙ) / n

   Ornek: 70, 80, 90, 60, 100
   x̄ = (70 + 80 + 90 + 60 + 100) / 5 = 400 / 5 = 80

   Ozellikler:
   - Tum verileri dikkate alir
   - Asiri degerlerden (ucdegerler) etkilenir
   - Ortalama, en kucuk ile en buyuk deger arasindadir

2. ORTANCA (MEDYAN / MEDIAN):
   Veriler kucukten buyuge siralandiginda ortadaki deger.
   - Tek sayida veri (n tek): Ortadaki deger → (n+1)/2. siradaki
   - Cift sayida veri (n cift): Ortadaki iki degerin ortalamasi → n/2. ve (n/2+1). degerler

   Ornek (tek): 3, 5, 7, 9, 11 → Ortanca = 7 (3. siradaki)
   Ornek (cift): 2, 4, 6, 8, 10, 12 → Ortanca = (6+8)/2 = 7

   Ozellikler:
   - Asiri degerlerden fazla etkilenmez
   - Siralama gerektirir

3. TEPE DEGER (MOD / MODE):
   En cok tekrar eden deger.
   Ornek: 3, 5, 5, 7, 5, 9 → Tepe deger = 5 (3 kez tekrar)
   - Birden fazla tepe deger olabilir (cok modlu)
   - Hic tekrar yoksa tepe deger tanimlanamaz

   Ornek: 2, 3, 3, 5, 5, 7 → Tepe degerler: 3 ve 5 (cift modlu)

YAYILIM OLCULERI:

1. DEGISIM ARALIGI (RANGE):
   Aralik = En buyuk deger - En kucuk deger
   Ornek: 3, 5, 7, 9, 15 → Aralik = 15 - 3 = 12

   - Verinin ne kadar genis bir aralIga yayildigini gosterir
   - Sadece iki uc degere bagli oldugu icin sinirlidir

2. CEYREKLER VE CEYREKLER ARASI ACIKLIK (IQR):
   - Q1 (1. ceyrek): Verinin alt yarisinIn ortancasi (%25)
   - Q2 (2. ceyrek): Ortanca (medyan) (%50)
   - Q3 (3. ceyrek): Verinin ust yarisinIn ortancasi (%75)
   - IQR = Q3 - Q1

   Ornek: 2, 4, 6, 8, 10, 12, 14
   Q1 = 4, Q2 = 8, Q3 = 12
   IQR = 12 - 4 = 8

UYGUN OLCU SECIMI:
- Simetrik dagilim, asiri deger yoksa → Aritmetik Ortalama
- Asiri degerler (uc degerler) varsa → Ortanca (Medyan)
- Kategorik veri veya en sik degeri bulmak icin → Tepe Deger (Mod)
"""
},

# ═══════════════════════════════════════════════════════════════
# EK: ORAN-ORANTI (7. SINIF DESTEK KONUSU)
# ═══════════════════════════════════════════════════════════════

"MAT.7.EK.ORAN_ORANTI": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Oran ve Oranti",
    "kazanimlar": ["M.7.1.4.1", "M.7.1.4.2", "M.7.1.4.3"],
    "icerik": """
ORAN:
- Ayni turden iki niceligin bolumune ORAN denir.
- a/b veya a:b seklinde yazilir.
- Ornek: Sinifta 12 kiz, 18 erkek → kiz/erkek = 12/18 = 2/3
- Oran birimsizdir.

ORANTI:
- Iki oranin esitligine ORANTI denir.
- a/b = c/d ise bu bir orantidir.
- Capraz carpim: a x d = b x c
  Ornek: 2/3 = 8/12 → 2 x 12 = 3 x 8 → 24 = 24 ✓

DOGRUDAN ORANTI (DOGRU ORANTI):
- Bir buyukluk artarken diger buyukluk de AYNI ORANDA artiyorsa dogru orantilidir.
- x/y = k (sabit) veya y = kx
- Grafigi orijinden gecen dogru
  Ornek: 3 kalem 12 TL ise 5 kalem kac TL?
  3/12 = 5/x → 3x = 60 → x = 20 TL
  Veya: 1 kalem = 4 TL → 5 kalem = 20 TL

TERS ORANTI:
- Bir buyukluk artarken diger buyukluk AYNI ORANDA azaliyorsa ters orantilidir.
- x x y = k (sabit) veya y = k/x
  Ornek: 6 isci bir isi 10 gunde bitirir. 15 isci ayni isi kac gunde bitirir?
  6 x 10 = 15 x t → 60 = 15t → t = 4 gun

  Ornek: 80 km/h hizla 3 saatte gidilen yol, 60 km/h hizla kac saatte gidilir?
  80 x 3 = 60 x t → 240 = 60t → t = 4 saat

ORANTI KURMA VE COZME:
  a/b = c/d → a x d = b x c (capraz carpim)

  Ornek: x/5 = 12/15
  15x = 60 → x = 4

YUZDE HESAPLAMALARI (ORANLA ILISKILI):
- %a = a/100
- Bir sayinin %a'si = sayi x a/100
  Ornek: 250'nin %20'si = 250 x 20/100 = 50
- Yuzde artis: Yeni deger = Eski deger x (1 + oran/100)
  Ornek: 200 TL'ye %15 zam → 200 x 1,15 = 230 TL
- Yuzde azalis: Yeni deger = Eski deger x (1 - oran/100)
  Ornek: 500 TL'de %30 indirim → 500 x 0,70 = 350 TL
"""
},

"MAT.7.EK.TAMSAYI_USLU_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Tam Sayi Uslu Sayilar",
    "kazanimlar": ["M.7.1.5.1", "M.7.1.5.2"],
    "icerik": """
US ALMA KURALLARI:

TANIM:
a^n = a x a x a x ... x a (n tane a carpimi, n pozitif tam sayi)
a: taban    |    n: us (kuvvet)

TEMEL KURALLAR:
1. a^0 = 1 (a ≠ 0)
   Ornek: 5^0 = 1    |    (-3)^0 = 1    |    0^0 = tanimsiz

2. a^1 = a
   Ornek: 7^1 = 7    |    (-4)^1 = -4

3. a^(-n) = 1 / a^n (negatif us = tersi)
   Ornek: 2^(-3) = 1/2³ = 1/8
   Ornek: 5^(-2) = 1/5² = 1/25

4. (a/b)^(-n) = (b/a)^n
   Ornek: (2/3)^(-2) = (3/2)^2 = 9/4

US ISLEM KURALLARI:

1. AYNI TABANLI CARPMA: a^m x a^n = a^(m+n)
   Ornek: 2^3 x 2^4 = 2^7 = 128
   Ornek: x^5 x x^3 = x^8

2. AYNI TABANLI BOLME: a^m / a^n = a^(m-n)
   Ornek: 3^5 / 3^2 = 3^3 = 27
   Ornek: y^7 / y^4 = y^3

3. USUN USSE ALMA: (a^m)^n = a^(m x n)
   Ornek: (2^3)^4 = 2^12 = 4096
   Ornek: (x^2)^5 = x^10

4. CARPIMIN USSE ALMA: (a x b)^n = a^n x b^n
   Ornek: (2 x 3)^4 = 2^4 x 3^4 = 16 x 81 = 1296

5. BOLMENIN USSE ALMA: (a/b)^n = a^n / b^n
   Ornek: (3/5)^2 = 9/25

10'UN KUVVETLERI VE BILIMSEL GOSTERIM:
10^1 = 10         |    10^(-1) = 0,1
10^2 = 100        |    10^(-2) = 0,01
10^3 = 1.000      |    10^(-3) = 0,001
10^6 = 1.000.000  |    10^(-6) = 0,000001

Bilimsel gosterim: a x 10^n (1 ≤ a < 10)
Ornek: 3.500.000 = 3,5 x 10^6
Ornek: 0,00042 = 4,2 x 10^(-4)
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik7_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_7_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik7_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_7_REFERANS.keys())


def get_matematik7_by_kazanim(kazanim_kodu: str) -> dict:
    """Kazanim koduna gore ilgili referans icerigini dondurur.
    Ornek: get_matematik7_by_kazanim('M.7.2.2.1') → Esitlik ve Denklem konusu
    """
    kazanim_kodu = kazanim_kodu.strip().upper()
    for key, val in MATEMATIK_7_REFERANS.items():
        if kazanim_kodu in val.get("kazanimlar", []):
            return {"anahtar": key, **val}
    return {}


def get_matematik7_by_unite(unite_adi: str) -> list:
    """Unite adina gore tum referans konularini dondurur.
    Ornek: get_matematik7_by_unite('Cebir') → Cebirsel Ifadeler, Esitlik, Esitsizlik
    """
    unite_lower = unite_adi.lower()
    results = []
    for key, val in MATEMATIK_7_REFERANS.items():
        if unite_lower in val["unite"].lower():
            results.append({"anahtar": key, **val})
    return results


def get_matematik7_formulas() -> dict:
    """Tum onemli formulleri kategorilere gore dondurur."""
    return {
        "Alan Formulleri": {
            "Ucgen": "A = (a x h) / 2",
            "Kare": "A = a²",
            "Dikdortgen": "A = a x b",
            "Paralelkenar": "A = a x h",
            "Eskenar Dortgen": "A = (d₁ x d₂) / 2",
            "Yamuk": "A = ((a + c) x h) / 2",
            "Daire": "A = πr²",
            "Daire Dilimi": "A = (a/360) x πr²",
        },
        "Cevre Formulleri": {
            "Cember": "C = 2πr = πd",
            "Yay Uzunlugu": "L = (a/360) x 2πr",
        },
        "Aci Formulleri": {
            "Cokgen Ic Acilar Toplami": "(n-2) x 180°",
            "Duzgun Cokgen Bir Ic Aci": "(n-2) x 180° / n",
            "Dis Acilar Toplami": "360°",
            "Duzgun Cokgen Bir Dis Aci": "360° / n",
            "Kosegen Sayisi": "n(n-3) / 2",
        },
        "Us Kurallari": {
            "Carpma": "a^m x a^n = a^(m+n)",
            "Bolme": "a^m / a^n = a^(m-n)",
            "Usun Usse Alma": "(a^m)^n = a^(m x n)",
            "Negatif Us": "a^(-n) = 1 / a^n",
            "Sifir Us": "a^0 = 1 (a ≠ 0)",
        },
        "Oranti": {
            "Dogru Oranti": "x/y = k (sabit)",
            "Ters Oranti": "x x y = k (sabit)",
            "Capraz Carpim": "a/b = c/d → a x d = b x c",
        },
    }
