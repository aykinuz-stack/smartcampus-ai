# -*- coding: utf-8 -*-
"""
11. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Trigonometri
2. Analitik Geometri
3. Fonksiyonlarda Uygulamalar
4. Diziler
5. Logaritma
"""

MATEMATIK_11_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: TRIGONOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.11.1.TRIGONOMETRIK_ORANLAR": {
    "unite": "Trigonometri",
    "baslik": "Trigonometrik Oranlar ve Birim Cember",
    "icerik": """
TRIGONOMETRIK ORANLAR VE BIRIM CEMBER:

1. BIRIM CEMBER TANIMI:
   - Merkezi orijinde, yaricapi 1 birim olan cember
   - P(x, y) noktasi birim cember uzerinde ise x^2 + y^2 = 1
   - Alfa acisina karsilik gelen P noktasinin koordinatlari: P(cos(alfa), sin(alfa))

2. TEMEL TRIGONOMETRIK ORANLAR:
   - sin(alfa) = karsi dik kenar / hipotenus
   - cos(alfa) = komsu dik kenar / hipotenus
   - tan(alfa) = karsi dik kenar / komsu dik kenar = sin(alfa)/cos(alfa)
   - cot(alfa) = komsu dik kenar / karsi dik kenar = cos(alfa)/sin(alfa)

3. OZEL ACILARIN TRIGONOMETRIK DEGERLERI:
   - sin(0)=0, sin(30)=1/2, sin(45)=V2/2, sin(60)=V3/2, sin(90)=1
   - cos(0)=1, cos(30)=V3/2, cos(45)=V2/2, cos(60)=1/2, cos(90)=0
   - tan(0)=0, tan(30)=V3/3, tan(45)=1, tan(60)=V3, tan(90)=tanimsiz

4. ISARET DURUMU (BOLGELERE GORE):
   - I. bolge (0-90): sin(+), cos(+), tan(+), cot(+)
   - II. bolge (90-180): sin(+), cos(-), tan(-), cot(-)
   - III. bolge (180-270): sin(-), cos(-), tan(+), cot(+)
   - IV. bolge (270-360): sin(-), cos(+), tan(-), cot(-)

5. TEMEL OZDESLIKLER:
   - sin^2(alfa) + cos^2(alfa) = 1
   - 1 + tan^2(alfa) = 1/cos^2(alfa) = sec^2(alfa)
   - 1 + cot^2(alfa) = 1/sin^2(alfa) = csc^2(alfa)
   - tan(alfa) * cot(alfa) = 1
"""
},

"MAT.11.1.TOPLAM_FARK_FORMULLERI": {
    "unite": "Trigonometri",
    "baslik": "Toplam ve Fark Formulleri",
    "icerik": """
TOPLAM VE FARK FORMULLERI:

1. TOPLAM-FARK FORMULLERI:
   - sin(A + B) = sinA*cosB + cosA*sinB
   - sin(A - B) = sinA*cosB - cosA*sinB
   - cos(A + B) = cosA*cosB - sinA*sinB
   - cos(A - B) = cosA*cosB + sinA*sinB
   - tan(A + B) = (tanA + tanB) / (1 - tanA*tanB)
   - tan(A - B) = (tanA - tanB) / (1 + tanA*tanB)

2. CIFT ACI FORMULLERI (2A):
   - sin(2A) = 2*sinA*cosA
   - cos(2A) = cos^2(A) - sin^2(A) = 2cos^2(A) - 1 = 1 - 2sin^2(A)
   - tan(2A) = 2tanA / (1 - tan^2(A))

3. YARIM ACI FORMULLERI:
   - sin^2(A/2) = (1 - cosA) / 2
   - cos^2(A/2) = (1 + cosA) / 2
   - tan(A/2) = sinA / (1 + cosA) = (1 - cosA) / sinA

4. CARPIMDAN TOPLAMA GECIS:
   - sinA*cosB = (1/2)[sin(A+B) + sin(A-B)]
   - cosA*sinB = (1/2)[sin(A+B) - sin(A-B)]
   - cosA*cosB = (1/2)[cos(A-B) + cos(A+B)]
   - sinA*sinB = (1/2)[cos(A-B) - cos(A+B)]

5. TOPLAMDAN CARPIMA GECIS:
   - sinA + sinB = 2*sin((A+B)/2)*cos((A-B)/2)
   - sinA - sinB = 2*cos((A+B)/2)*sin((A-B)/2)
   - cosA + cosB = 2*cos((A+B)/2)*cos((A-B)/2)
   - cosA - cosB = -2*sin((A+B)/2)*sin((A-B)/2)

6. UYGULAMALAR:
   - sin(75) = sin(45+30) hesabi
   - cos(15) = cos(45-30) hesabi
   - tan(105) gibi ozel olmayan acilarin hesaplanmasi
"""
},

"MAT.11.1.TRIGONOMETRIK_DENKLEMLER": {
    "unite": "Trigonometri",
    "baslik": "Trigonometrik Denklemler ve Esitsizlikler",
    "icerik": """
TRIGONOMETRIK DENKLEMLER:

1. TEMEL DENKLEM COZUMLERI:
   - sin(x) = a => genel cozum: x = arcsin(a) + 2k*pi veya x = pi - arcsin(a) + 2k*pi
   - cos(x) = a => genel cozum: x = +/- arccos(a) + 2k*pi
   - tan(x) = a => genel cozum: x = arctan(a) + k*pi
   - (k tamsayi)

2. GENEL COZUM KURALLARI:
   - sin(x) = 0 => x = k*pi
   - cos(x) = 0 => x = pi/2 + k*pi
   - tan(x) = 0 => x = k*pi
   - sin(x) = 1 => x = pi/2 + 2k*pi
   - cos(x) = 1 => x = 2k*pi

3. OZEL DENKLEM TIPLERI:
   - a*sin(x) + b*cos(x) = c seklindeki denklemler
   - R*sin(x + fi) = c formuna donusturme (R = karekök(a^2+b^2))
   - Homojen trigonometrik denklemler (her terimin derecesi ayni)
   - Carpanlara ayirma ile cozulen denklemler

4. TRIGONOMETRIK ESITSIZLIKLER:
   - sin(x) > a, sin(x) < a turunde birim cember ile cozum
   - Grafiksel yorum: y = sin(x) ve y = a grafikleriyle cozum araligi
   - Cozum kumeleri aralik olarak yazilir

5. TERS TRIGONOMETRIK FONKSIYONLAR:
   - arcsin: [-1,1] -> [-pi/2, pi/2]
   - arccos: [-1,1] -> [0, pi]
   - arctan: R -> (-pi/2, pi/2)
   - sin(arcsin(x)) = x, fakat arcsin(sin(x)) her zaman x degildir
"""
},

"MAT.11.1.SINUS_KOSINUS_TEOREMLERI": {
    "unite": "Trigonometri",
    "baslik": "Sinus ve Kosinus Teoremleri",
    "icerik": """
SINUS VE KOSINUS TEOREMLERI:

1. SINUS TEOREMI:
   - a/sin(A) = b/sin(B) = c/sin(C) = 2R
   - R: ucgenin cevrel cember yaricapi
   - Herhangi bir ucgende kenarlar karsisindaki acilarin sinusleriyle orantilidir
   - Kullanim: Iki aci ve bir kenar biliniyorsa diger kenarlarin bulunmasi
   - AAS ve ASA durumlarinda ucgen cozumu

2. KOSINUS TEOREMI:
   - a^2 = b^2 + c^2 - 2bc*cos(A)
   - b^2 = a^2 + c^2 - 2ac*cos(B)
   - c^2 = a^2 + b^2 - 2ab*cos(C)
   - Pisagor teoreminin genellestirilmis halidir (A=90 icin cos90=0 -> a^2=b^2+c^2)
   - Kullanim: Uc kenar biliniyorsa acilarin bulunmasi (SSS durumu)
   - Iki kenar ve aradaki aci biliniyorsa ucuncu kenar (SAS durumu)

3. UCGENIN ALANI TRIGONOMETRIK FORMUL:
   - Alan = (1/2)*a*b*sin(C)
   - Alan = (1/2)*b*c*sin(A)
   - Alan = (1/2)*a*c*sin(B)
   - Iki kenar ve aradaki aci ile alan hesaplanir

4. UYGULAMALAR:
   - Arazi olcumu ve haritacilik problemleri
   - Uzaklik ve yukseklik hesaplama
   - Denizcilik ve navigasyon problemleri
   - Ucgenin tum elemanlarinin hesaplanmasi
   - Aci aciklik/donukluk tespiti: cos(A) > 0 ise dar, cos(A) < 0 ise genis aci
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: ANALITIK GEOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.11.2.DOGRU_DENKLEMI": {
    "unite": "Analitik Geometri",
    "baslik": "Dogrunun Analitik Incelenmesi",
    "icerik": """
DOGRUNUN ANALITIK INCELENMESI:

1. DOGRU DENKLEMI BICIMLERI:
   - Egim-nokta bicimi: y - y1 = m(x - x1)
   - Egim-kesim noktasi bicimi: y = mx + n
   - Genel denklem: ax + by + c = 0
   - Iki nokta bicimi: (y-y1)/(y2-y1) = (x-x1)/(x2-x1)
   - Eksen kesimleri bicimi: x/a + y/b = 1

2. EGIM (m) HESABI:
   - m = (y2 - y1) / (x2 - x1) (iki noktadan)
   - m = tan(alfa) (alfa: dogrunun x ekseniyle yaptigi pozitif yon acisi)
   - Yatay dogrularin egimi: m = 0
   - Dusey dogrularin egimi: tanimsiz
   - Yukari sag yonlu dogrular: m > 0
   - Asagi sag yonlu dogrular: m < 0

3. IKI DOGRUNUN BIRBIRINE DURUMU:
   - Paralel dogrular: m1 = m2 (egimler esit)
   - Dik dogrular: m1 * m2 = -1 (egimlerin carpimi -1)
   - Kesisen dogrular: m1 != m2
   - Cakisik dogrular: m1 = m2 ve ayni noktadan gecerler

4. NOKTANIN DOGRUYA UZAKLIGI:
   - d = |a*x0 + b*y0 + c| / karekök(a^2 + b^2)
   - A(x0, y0) noktasindan ax + by + c = 0 dogrusuna uzaklik

5. IKI PARALEL DOGRU ARASI UZAKLIK:
   - d1: ax + by + c1 = 0 ve d2: ax + by + c2 = 0
   - Uzaklik = |c1 - c2| / karekök(a^2 + b^2)
"""
},

"MAT.11.2.CEMBER_DENKLEMI": {
    "unite": "Analitik Geometri",
    "baslik": "Cemberin Analitik Incelenmesi",
    "icerik": """
CEMBERIN ANALITIK INCELENMESI:

1. STANDART CEMBER DENKLEMI:
   - (x - a)^2 + (y - b)^2 = r^2
   - Merkez: M(a, b), Yaricap: r
   - Orijin merkezli cember: x^2 + y^2 = r^2

2. GENEL CEMBER DENKLEMI:
   - x^2 + y^2 + Dx + Ey + F = 0
   - Merkez: M(-D/2, -E/2)
   - Yaricap: r = karekök(D^2/4 + E^2/4 - F)
   - Cember olma sarti: D^2/4 + E^2/4 - F > 0

3. NOKTANIN CEMBERE GORE DURUMU:
   - P(x0, y0) icin d = karekök((x0-a)^2 + (y0-b)^2)
   - d < r ise P cemberin icinde
   - d = r ise P cemberin uzerinde
   - d > r ise P cemberin disinda
   - Kuvvet: (x0-a)^2 + (y0-b)^2 - r^2 (pozitif: dis, negatif: ic)

4. DOGRU-CEMBER ILISKISI:
   - Merkezin dogruya uzakligi = d
   - d < r ise dogru cemberi iki noktada keser (kesen)
   - d = r ise dogru cembere teget
   - d > r ise dogru ile cember ayriktir (ortak nokta yok)

5. TEGET DOGRULAR:
   - Cember uzerindeki P(x1, y1) noktasindaki teget: (x1-a)(x-a) + (y1-b)(y-b) = r^2
   - Dis noktadan cembere cizilen teget uzunlugu: t = karekök(d^2 - r^2)
   - Dis noktadan cizilen iki teget parcasi esit uzunluktadir

6. IKI CEMBERIN BIRBIRINE DURUMU:
   - d: merkezler arasi uzaklik, r1 ve r2 yaricaplar
   - d > r1 + r2: dis ayrik
   - d = r1 + r2: distan teget
   - |r1 - r2| < d < r1 + r2: iki noktada kesisir
   - d = |r1 - r2|: icten teget
   - d < |r1 - r2|: ic ayrik
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: FONKSIYONLARDA UYGULAMALAR
# ═══════════════════════════════════════════════════════════════

"MAT.11.3.IKINCI_DERECE_FONKSIYON": {
    "unite": "Fonksiyonlarda Uygulamalar",
    "baslik": "Ikinci Dereceden Fonksiyonlar ve Grafikleri",
    "icerik": """
IKINCI DERECEDEN FONKSIYONLAR:

1. GENEL FORM:
   - f(x) = ax^2 + bx + c (a != 0)
   - Grafigi paraboldur
   - a > 0 ise parabol asagi acik (minimum noktasi vardir)
   - a < 0 ise parabol yukari acik (maksimum noktasi vardir)

2. TEPE NOKTASI:
   - x_t = -b / (2a)
   - y_t = f(x_t) = (4ac - b^2) / (4a)
   - Tepe noktasi: T(-b/2a, (4ac-b^2)/4a)
   - Simetri ekseni: x = -b/(2a)

3. DISKRIMINANT (delta = b^2 - 4ac):
   - delta > 0: Iki farkli reel kok (parabol x eksenini iki noktada keser)
   - delta = 0: Cakisik kok / tek kok (parabol x eksenine teget)
   - delta < 0: Reel kok yok (parabol x eksenini kesmez)

4. KOKLERIN OZELLIKLERI (VIETA FORMULLERI):
   - x1 + x2 = -b/a (koklerin toplami)
   - x1 * x2 = c/a (koklerin carpimi)
   - |x1 - x2| = karekök(delta) / |a| (kokler arasi fark)

5. IKINCI DERECE ESITSIZLIKLER:
   - ax^2 + bx + c > 0, ax^2 + bx + c <= 0 vb.
   - Cozum: kokleri bul, isaret tablosu olustur
   - a > 0 ve delta < 0 ise ax^2 + bx + c > 0 her x icin dogrudur
   - Parabol grafigi ile gorsel yorum

6. UYGULAMALAR:
   - Maksimum-minimum problemleri (alan, kar, maliyet)
   - Dikey atis hareketi: h(t) = -g*t^2/2 + v0*t + h0
   - Fizik ve ekonomi modellemeleri
"""
},

"MAT.11.3.FONKSIYON_UYGULAMALARI": {
    "unite": "Fonksiyonlarda Uygulamalar",
    "baslik": "Fonksiyonlarin Ozellikleri ve Donusumleri",
    "icerik": """
FONKSIYONLARIN OZELLIKLERI VE DONUSUMLERI:

1. FONKSIYON DONUSUMLERI:
   - Otelenme: f(x-a) + b -> yatayda a, dikeyde b kaydirma
   - f(x) + k: grafigi k birim yukari (k>0) veya asagi (k<0) kaydirma
   - f(x - h): grafigi h birim saga (h>0) veya sola (h<0) kaydirma
   - -f(x): x eksenine gore yansima
   - f(-x): y eksenine gore yansima
   - |f(x)|: x ekseninin altindaki kisim yukari katlanir
   - f(|x|): y eksenine gore simetrik grafik

2. CIFT VE TEK FONKSIYONLAR:
   - Cift fonksiyon: f(-x) = f(x) (y eksenine simetrik)
   - Tek fonksiyon: f(-x) = -f(x) (orijine simetrik)
   - Ornek cift: f(x) = x^2, cos(x)
   - Ornek tek: f(x) = x^3, sin(x)

3. ARTAN VE AZALAN FONKSIYONLAR:
   - Artan: x1 < x2 ise f(x1) < f(x2)
   - Azalan: x1 < x2 ise f(x1) > f(x2)
   - Monoton artan/azalan: tum tanim kumesinde artan/azalan

4. BILESKE FONKSIYON:
   - (f o g)(x) = f(g(x))
   - Degisme ozelligi yoktur: f o g != g o f (genel olarak)
   - Birlestirme ozelligi vardir: (f o g) o h = f o (g o h)
   - Tanim kumesi: g'nin tanim kumesindeki x'ler icin g(x), f'in tanim kumesinde olmali

5. TERS FONKSIYON:
   - f^(-1) var olma sarti: f bire-bir ve orten olmali
   - f(f^(-1)(x)) = x ve f^(-1)(f(x)) = x
   - f^(-1)'in grafigi, f'in y = x dogrusuna gore simetrisidir
   - Bulma yontemi: y = f(x) => x = f^(-1)(y), sonra x ve y degistir
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: DIZILER
# ═══════════════════════════════════════════════════════════════

"MAT.11.4.ARITMETIK_DIZI": {
    "unite": "Diziler",
    "baslik": "Aritmetik Diziler",
    "icerik": """
ARITMETIK DIZILER:

1. TANIM:
   - Ardisik iki terim arasindaki fark sabittir
   - Ortak fark: d = a_(n+1) - a_n
   - d > 0 ise artan dizi, d < 0 ise azalan dizi, d = 0 ise sabit dizi

2. GENEL TERIM:
   - a_n = a1 + (n-1)*d
   - a_n = a_k + (n-k)*d (herhangi bir terimden)
   - n. terim birinci terim ve ortak fark ile bulunur

3. ARDISIK UCLU ILISKISI:
   - a_n = (a_(n-1) + a_(n+1)) / 2
   - Her terim, kendinden onceki ve sonraki terimin aritmetik ortalamasidir
   - Bu ozellik ile bilinmeyen terimler hesaplanabilir

4. ILK n TERIMIN TOPLAMI:
   - S_n = n*(a1 + a_n) / 2
   - S_n = n*(2*a1 + (n-1)*d) / 2
   - S_n = n*a_ortanca (terim sayisi tek ise)
   - a_n = S_n - S_(n-1) (n >= 2 icin)

5. OZELLIKLER:
   - Bastan ve sondan esit uzakliktaki terimlerin toplami sabittir: a1+a_n = a2+a_(n-1)
   - Aritmetik dizinin her terimi k ile carpilirsa yine aritmetik dizidir (ortak fark k*d olur)
   - Aritmetik dizinin her terimine c eklenirse yine aritmetik dizidir (ortak fark degismez)

6. UYGULAMALAR:
   - Parasal birikim: Her ay esit miktar artan tasarruf
   - Koltuk dizilimi: Her sirada sabit sayi artan tiyatro koltuklari
   - Dogal sayilarin toplami: 1+2+3+...+n = n*(n+1)/2
"""
},

"MAT.11.4.GEOMETRIK_DIZI": {
    "unite": "Diziler",
    "baslik": "Geometrik Diziler",
    "icerik": """
GEOMETRIK DIZILER:

1. TANIM:
   - Ardisik iki terimin orani sabittir
   - Ortak oran: r = a_(n+1) / a_n (a_n != 0)
   - r > 1 ise artan, 0 < r < 1 ise azalan, r < 0 ise isaret degistiren dizi

2. GENEL TERIM:
   - a_n = a1 * r^(n-1)
   - a_n = a_k * r^(n-k) (herhangi bir terimden)

3. ARDISIK UCLU ILISKISI:
   - a_n^2 = a_(n-1) * a_(n+1)
   - Her terim, kendinden onceki ve sonraki terimin geometrik ortalamasidir
   - a_n = karekök(a_(n-1) * a_(n+1)) (terimlerin isareti ayniysa)

4. ILK n TERIMIN TOPLAMI:
   - r != 1 icin: S_n = a1*(1 - r^n) / (1 - r)
   - r = 1 icin: S_n = n*a1
   - |r| < 1 icin sonsuz toplam: S_sonsuz = a1 / (1 - r)

5. OZELLIKLER:
   - Bastan ve sondan esit uzakliktaki terimlerin carpimi sabittir: a1*a_n = a2*a_(n-1)
   - Geometrik dizinin her terimi k ile carpilirsa yine geometrik dizidir (ortak oran degismez)
   - Geometrik dizinin her terimi k. kuvvete alinirsa ortak oran r^k olur

6. UYGULAMALAR:
   - Bilesik faiz: A = P*(1+r)^n
   - Bakteri cogalmasi: Ikiye bolunme ile ustel buyume
   - Radyoaktif bozunma: Yarilama suresi ile azalan miktar
   - Tekrarlayan ondalik kesirlerin kesir olarak yazilmasi
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: LOGARITMA
# ═══════════════════════════════════════════════════════════════

"MAT.11.5.USTEL_FONKSIYON": {
    "unite": "Logaritma",
    "baslik": "Ustel Fonksiyon",
    "icerik": """
USTEL FONKSIYON:

1. TANIM:
   - f(x) = a^x (a > 0, a != 1)
   - Tanim kumesi: R (tum reel sayilar)
   - Deger kumesi: (0, +sonsuz) (her zaman pozitif)
   - a^0 = 1 (grafik daima (0,1) noktasindan gecer)

2. USTEL FONKSIYON GRAFIKLERI:
   - a > 1 ise artan fonksiyon (2^x, 3^x, e^x gibi)
   - 0 < a < 1 ise azalan fonksiyon ((1/2)^x, (1/3)^x gibi)
   - y = 0 (x ekseni) yatay asimptottur
   - Grafik her zaman x ekseninin uzerindedir

3. US KURALLARI:
   - a^m * a^n = a^(m+n)
   - a^m / a^n = a^(m-n)
   - (a^m)^n = a^(m*n)
   - (a*b)^n = a^n * b^n
   - a^(-n) = 1/a^n
   - a^(m/n) = n. dereceden kok(a^m)

4. USTEL DENKLEMLER:
   - a^f(x) = a^g(x) => f(x) = g(x) (taban ayni ise usler esittir)
   - Farkli tabanli denklemler: Ortak tabana donusturme veya logaritma alma
   - Yerine koyma yontemi: t = a^x denerek cebirsel denkleme donusturme

5. USTEL ESITSIZLIKLER:
   - a > 1 icin: a^f(x) > a^g(x) => f(x) > g(x) (yon korunur)
   - 0 < a < 1 icin: a^f(x) > a^g(x) => f(x) < g(x) (yon degisir)
   - Tabanin 1'den buyuk veya kucuk olmasina dikkat edilir
"""
},

"MAT.11.5.LOGARITMA": {
    "unite": "Logaritma",
    "baslik": "Logaritma Fonksiyonu ve Ozellikleri",
    "icerik": """
LOGARITMA FONKSIYONU VE OZELLIKLERI:

1. TANIM:
   - log_a(b) = c <=> a^c = b
   - a: taban (a > 0, a != 1)
   - b: numerus/antilogaritma (b > 0)
   - Logaritma, ustel fonksiyonun tersidir

2. OZEL LOGARITMALAR:
   - log (veya log10): 10 tabanli (Briggs) logaritma
   - ln (veya log_e): e = 2,71828 tabanli dogal logaritma
   - log2: 2 tabanli logaritma (bilgisayar biliminde onemli)

3. LOGARITMA OZELLIKLERI:
   - log_a(1) = 0 (cunku a^0 = 1)
   - log_a(a) = 1 (cunku a^1 = a)
   - log_a(x*y) = log_a(x) + log_a(y) (carpimin logaritmasi)
   - log_a(x/y) = log_a(x) - log_a(y) (bolumun logaritmasi)
   - log_a(x^n) = n*log_a(x) (kuvvetin logaritmasi)
   - log_a(n. dereceden kok(x)) = (1/n)*log_a(x) (kokun logaritmasi)

4. TABAN DEGISTIRME:
   - log_a(b) = log_c(b) / log_c(a) (herhangi bir c tabaninda)
   - log_a(b) = 1 / log_b(a) (ozel durum)
   - log_a(b) * log_b(c) = log_a(c) (zincir kurali)

5. LOGARITMIK DENKLEMLER:
   - Tanim kosuluna dikkat: numerus > 0, taban > 0 ve != 1
   - log_a(f(x)) = log_a(g(x)) => f(x) = g(x) (f(x)>0, g(x)>0 sarti ile)
   - Logaritmayi ustel forma cevirme yontemi

6. LOGARITMIK ESITSIZLIKLER:
   - a > 1 icin: log_a(f(x)) > log_a(g(x)) => f(x) > g(x) > 0
   - 0 < a < 1 icin: log_a(f(x)) > log_a(g(x)) => 0 < f(x) < g(x)
   - Taban buyuklugune gore esitsizlik yonu degisir

7. UYGULAMALAR:
   - Desibel olcegi: dB = 10*log(I/I0)
   - Richter olcegi: Deprem siddeti logaritmik olcer
   - pH degeri: pH = -log[H+]
   - Bilesik faiz suresi: n = log(A/P) / log(1+r)
"""
},

}

def get_matematik11_reference(topic: str) -> list:
    """Verilen konuya en yakin matematik 11 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_11_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_matematik11_keys() -> list:
    """Tum matematik 11 referans anahtarlarini dondurur."""
    return list(MATEMATIK_11_REFERANS.keys())
