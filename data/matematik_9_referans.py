# -*- coding: utf-8 -*-
"""
9. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.
Lise 9. sinif duzeyi icerikleri kapsar.

Uniteler:
1. Kumeler
2. Denklemler ve Esitsizlikler
3. Ucgenler
4. Veri Analizi
5. Fonksiyon
6. Uslu ve Koklu Ifadeler
7. Polinomlar
"""

MATEMATIK_9_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: KUMELER
# ═══════════════════════════════════════════════════════════════

"MAT.9.1.KUME_KAVRAMI": {
    "unite": "Kumeler",
    "baslik": "Kume Kavrami, Alt Kume, Esit Kume",
    "icerik": """
KUME KAVRAMI:

1. TANIMLAR:
   - Kume: Ortak bir ozellige sahip, birbirinden farkli nesnelerin olusturdudu topluluk
   - Eleman: Kumenin icerisindeki her bir nesne
   - Gosterim: Buyuk harflerle (A, B, C...), elemanlar kume parantezi icinde { }
   - a eleman A => a ∈ A, a eleman degil A => a ∉ A

2. KUME GOSTERIM YONTEMLERI:
   - Liste yontemi: A = {1, 2, 3, 4, 5}
   - Ortak ozellik yontemi: A = {x | x < 6, x ∈ N+}
   - Venn semasi: Kapalı egri icinde gosterim

3. BOS KUME:
   - Hicbir elemani olmayan kume
   - Gosterim: ∅ veya { }
   - Dikkat: {∅} bos kume DEGILDIR, tek elemani olan bir kumedir
   - {0} bos kume DEGILDIR, elemani 0 olan bir kumedir

4. ALT KUME:
   - A kumesinin her elemani B kumesinde varsa A, B'nin alt kumesidir: A ⊂ B
   - Her kume kendisinin alt kumesidir: A ⊂ A
   - Bos kume her kumenin alt kumesidir: ∅ ⊂ A
   - n elemanli bir kumenin alt kume sayisi: 2^n
   - n elemanli bir kumenin ozel (kendisi haric) alt kume sayisi: 2^n - 1
   - n elemanli bir kumenin bos kumeden farkli alt kume sayisi: 2^n - 1
   - n elemanli bir kumenin ozel ve bos kumeden farkli alt kume sayisi: 2^n - 2

   ORNEK: A = {a, b, c} => n = 3
   - Alt kume sayisi: 2^3 = 8
   - Alt kumeler: ∅, {a}, {b}, {c}, {a,b}, {a,c}, {b,c}, {a,b,c}

5. ESIT KUME:
   - A ve B kumelerinin tum elemanlari ayniysa A = B
   - A ⊂ B ve B ⊂ A ise A = B
   - Elemanların sırası onemli degildir: {1, 2, 3} = {3, 1, 2}

6. DENK KUME:
   - Eleman sayilari esit olan kumeler: s(A) = s(B)
   - Denk kumeler esit olmak zorunda degildir: {1,2} ve {a,b} denktir ama esit degildir

7. EVRENSEL KUME (E):
   - Calisilan tum kumeleri kapsayan en buyuk kume
   - E veya U ile gosterilir
   - Tum kumeler evrensel kumenin alt kumesidir
"""
},

"MAT.9.1.KUME_ISLEMLERI": {
    "unite": "Kumeler",
    "baslik": "Kumelerde Islemler ve Venn Semalari",
    "icerik": """
KUMELERDE ISLEMLER:

1. BIRLESIM (∪):
   - A ∪ B = {x | x ∈ A veya x ∈ B}
   - En az birinde bulunan tum elemanlar
   - ORNEK: A = {1,2,3}, B = {2,3,4,5} => A ∪ B = {1,2,3,4,5}
   - Ozellikler:
     * A ∪ A = A
     * A ∪ ∅ = A
     * A ∪ E = E
     * A ∪ B = B ∪ A (degismeli)
     * (A ∪ B) ∪ C = A ∪ (B ∪ C) (birlesmeli)

2. KESISIM (∩):
   - A ∩ B = {x | x ∈ A ve x ∈ B}
   - Her ikisinde de bulunan ortak elemanlar
   - ORNEK: A = {1,2,3}, B = {2,3,4,5} => A ∩ B = {2,3}
   - Ozellikler:
     * A ∩ A = A
     * A ∩ ∅ = ∅
     * A ∩ E = A
     * A ∩ B = B ∩ A (degismeli)
     * A ⊂ B ise A ∩ B = A

3. FARK ( \\ ):
   - A \\ B = A - B = {x | x ∈ A ve x ∉ B}
   - A'da olup B'de olmayan elemanlar
   - ORNEK: A = {1,2,3,4}, B = {3,4,5} => A \\ B = {1,2}
   - Dikkat: A \\ B ≠ B \\ A (degismeli DEGILDIR)
   - A \\ B = A \\ (A ∩ B)

4. TUMLEYEN (A'):
   - A' = E \\ A = {x | x ∈ E ve x ∉ A}
   - Evrensel kumede olup A'da olmayan elemanlar
   - Ozellikler:
     * (A')' = A
     * A ∪ A' = E
     * A ∩ A' = ∅
     * E' = ∅, ∅' = E

5. DE MORGAN KURALLARI:
   - (A ∪ B)' = A' ∩ B' (Birlesimin tumliyeni = Tumliyenlerin kesisimi)
   - (A ∩ B)' = A' ∪ B' (Kesisimin tumliyeni = Tumliyenlerin birlesimi)

6. ELEMAN SAYISI FORMULLERI:
   - s(A ∪ B) = s(A) + s(B) - s(A ∩ B)
   - s(A ∪ B ∪ C) = s(A) + s(B) + s(C) - s(A ∩ B) - s(A ∩ C) - s(B ∩ C) + s(A ∩ B ∩ C)
   - s(A') = s(E) - s(A)
   - s(A \\ B) = s(A) - s(A ∩ B)

7. VENN SEMASI PROBLEM COZUMU:
   - Adim 1: Evrensel kume icine kumeleri ciz
   - Adim 2: Kesisim bolgesinden basla (ortak kisim)
   - Adim 3: Dista kalan bolgeleri hesapla
   - Adim 4: Tum bolgelerin toplami = s(E) olmali

   ORNEK: 40 ogrencili sinifta 25 Matematik, 20 Fizik seviyor. 8 ogrenci ikisini de seviyor.
   s(M ∪ F) = 25 + 20 - 8 = 37, Hic sevmeyen = 40 - 37 = 3
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: DENKLEMLER VE ESITSIZLIKLER
# ═══════════════════════════════════════════════════════════════

"MAT.9.2.BIRINCI_DERECE_DENKLEM": {
    "unite": "Denklemler ve Esitsizlikler",
    "baslik": "Birinci Dereceden Denklemler",
    "icerik": """
BIRINCI DERECEDEN DENKLEMLER:

1. TANIM:
   - ax + b = 0 (a ≠ 0) seklindeki denklemlerdir
   - Bilinmeyenin en buyuk kuvveti 1'dir
   - Cozum: x = -b/a

2. COZUM ADIMLARI:
   - Parantez varsa ac
   - Benzer terimleri bir araya topla
   - Bilinmeyenli terimleri bir tarafa, sabit terimleri diger tarafa topla
   - Taraf degistirirken isaret degisir
   - Katsayiya bol

3. ORNEKLER:
   - 3x + 7 = 22 => 3x = 15 => x = 5
   - 2(x - 3) + 4 = 10 => 2x - 6 + 4 = 10 => 2x = 12 => x = 6
   - (x+1)/3 = 5 => x + 1 = 15 => x = 14

4. OZEL DURUMLAR:
   - 0·x = 0 => Denklemin sonsuz cozumu vardir (ozdeslik)
   - 0·x = 5 => Denklemin cozumu yoktur (celiskili denklem)
   - a·x = b (a ≠ 0) => Tek cozum: x = b/a

5. PROBLEM COZUM STRATEJILERI:
   - Bilinmeyeni x olarak belirle
   - Problemdeki iliskileri denklem olarak yaz
   - Denklemi coz
   - Cevabi problem baglaminda kontrol et

   ORNEK: Bir sayinin 3 kati ile 7'nin toplami 28'dir. Bu sayi kactir?
   3x + 7 = 28 => 3x = 21 => x = 7
"""
},

"MAT.9.2.MUTLAK_DEGER_DENKLEMI": {
    "unite": "Denklemler ve Esitsizlikler",
    "baslik": "Mutlak Deger Denklemleri",
    "icerik": """
MUTLAK DEGER DENKLEMLERI:

1. MUTLAK DEGER TANIMI:
   - |x| = x, eger x >= 0
   - |x| = -x, eger x < 0
   - Geometrik anlam: x'in sayi dogrusunda 0'a uzakligi
   - |x| >= 0 (her zaman sifir veya pozitif)

2. TEMEL OZELLIKLER:
   - |a| = |-a|
   - |a · b| = |a| · |b|
   - |a/b| = |a| / |b| (b ≠ 0)
   - |a + b| <= |a| + |b| (ucgen esitsizligi)
   - |a|^2 = a^2

3. MUTLAK DEGER DENKLEM TURLERI:
   - |f(x)| = a (a > 0): f(x) = a veya f(x) = -a (2 cozum)
   - |f(x)| = a (a = 0): f(x) = 0 (1 cozum)
   - |f(x)| = a (a < 0): Cozum yoktur
   - |f(x)| = |g(x)|: f(x) = g(x) veya f(x) = -g(x)

4. COZUM ORNEKLERI:
   - |2x - 3| = 7
     Durum 1: 2x - 3 = 7 => x = 5
     Durum 2: 2x - 3 = -7 => x = -2
     Cozum kumesi: {-2, 5}

   - |x + 1| = |2x - 3|
     Durum 1: x + 1 = 2x - 3 => x = 4
     Durum 2: x + 1 = -(2x - 3) => x + 1 = -2x + 3 => 3x = 2 => x = 2/3
     Cozum kumesi: {2/3, 4}

5. OZEL DURUMLAR:
   - |x| = -5 => Cozum yoktur (mutlak deger negatif olamaz)
   - |x - 2| + |x + 3| = 0 => Her iki mutlak deger de 0 olmali
     x - 2 = 0 ve x + 3 = 0 ayni anda saglanamaz => Cozum yok
"""
},

"MAT.9.2.ESITSIZLIKLER": {
    "unite": "Denklemler ve Esitsizlikler",
    "baslik": "Birinci Dereceden Esitsizlikler ve Esitsizlik Sistemleri",
    "icerik": """
BIRINCI DERECEDEN ESITSIZLIKLER:

1. TANIM:
   - ax + b > 0, ax + b < 0, ax + b >= 0, ax + b <= 0 seklindeki ifadeler
   - Cozum kumesi genellikle bir aralik (interval) olur

2. ESITSIZLIK KURALLARI:
   - Her iki tarafa ayni sayi eklenebilir/cikarilabilir (yon degismez)
   - Her iki taraf ayni POZiTiF sayiyla carpilabilir/bolunebilir (yon degismez)
   - Her iki taraf ayni NEGATiF sayiyla carpilir/bolunurse ESITSIZLIK YONU DEGISIR!

   ORNEK: -2x > 6 => x < -3 (negatifle boldugumuzde yon degisti!)

3. ARALIK GOSTERIMI:
   - Acik aralik: (a, b) = {x | a < x < b}
   - Kapali aralik: [a, b] = {x | a <= x <= b}
   - Yarim acik: [a, b) veya (a, b]
   - Sonsuz araliklar: (-∞, a), (a, +∞), [a, +∞), (-∞, a]
   - ∞ isaretinin yaninda her zaman acik parantez kullanilir

4. COZUM ORNEKLERI:
   - 3x - 5 > 7 => 3x > 12 => x > 4, Cozum: (4, +∞)
   - -2x + 6 <= 10 => -2x <= 4 => x >= -2, Cozum: [-2, +∞)
   - 1 < 2x + 3 < 9 => -2 < 2x < 6 => -1 < x < 3, Cozum: (-1, 3)

5. ESITSIZLIK SISTEMLERI:
   - Birden fazla esitsizligin ayni anda saglanmasi
   - Her esitsizlik ayri ayri cozulur
   - Cozum kumeleri kesisilir (∩)

   ORNEK:
   x + 2 > 5 => x > 3
   2x - 1 < 9 => x < 5
   Sistem cozumu: x > 3 VE x < 5 => 3 < x < 5, Cozum: (3, 5)

6. MUTLAK DEGER ESITSIZLIKLERI:
   - |x| < a (a > 0) => -a < x < a
   - |x| > a (a > 0) => x < -a veya x > a
   - |x| <= a (a > 0) => -a <= x <= a
   - |x| >= a (a > 0) => x <= -a veya x >= a

   ORNEK: |2x - 1| < 5 => -5 < 2x - 1 < 5 => -4 < 2x < 6 => -2 < x < 3
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: UCGENLER
# ═══════════════════════════════════════════════════════════════

"MAT.9.3.UCGEN_TEMEL": {
    "unite": "Ucgenler",
    "baslik": "Ucgenin Kenarlari, Acilari ve Ucgen Esitsizligi",
    "icerik": """
UCGENIN KENARLARI VE ACILARI:

1. UCGEN TANIMI:
   - Ayni dogru uzerinde olmayan uc noktanin birlestirilmesiyle olusan kapalik sekil
   - 3 kenar, 3 aci, 3 koseye sahiptir
   - Ic acilar toplami = 180°

2. KENARLARINA GORE UCGENLER:
   - Cesitkenar ucgen: Tum kenarlari farkli uzunlukta
   - Ikizkenar ucgen: Iki kenari esit (taban acilari da esit)
   - Eskenar ucgen: Tum kenarlari esit (tum acilari 60°)

3. ACILARINA GORE UCGENLER:
   - Dar acili ucgen: Tum acilari 90°'den kucuk
   - Dik acili ucgen: Bir acisi 90° (diger ikisi dar)
   - Genis acili ucgen: Bir acisi 90°'den buyuk (diger ikisi dar)

4. UCGEN ESITSIZLIGI (COK ONEMLI):
   - Herhangi bir kenar, diger iki kenarin FARKINDAN buyuk,
     TOPLAMINDAN kucuk olmalidir
   - |a - b| < c < a + b (her uc kenar icin gecerli)
   - Bu sarti saglamayan uc uzunluk ucgen olusturamaz!

   ORNEK: 3, 5, 9 ucgen olusturur mu?
   |5 - 3| < 9 < 5 + 3 => 2 < 9 < 8 SAGLANMAZ! => Ucgen olusturamaz.

   ORNEK: 4, 6, 8 ucgen olusturur mu?
   |6 - 4| < 8 < 6 + 4 => 2 < 8 < 10 SAGLANIR! => Ucgen olusturur.

5. KENAR-ACI ILISKISI:
   - Buyuk kenarın karsisindaki aci buyuktur
   - Buyuk acinin karsisindaki kenar buyuktur
   - Esit kenarlarin karsisindaki acilar esittir
   - a > b > c ise A > B > C (karsisindaki acilar)

6. DIS ACI TEOREMI:
   - Bir ucgenin dis acisi, kendisine komsul olmayan iki ic acinin toplamina esittir
   - d = A + B (d, C kosesindeeki dis aci; A ve B komsul olmayan ic acilar)
   - Her kosedeki dis aci, ic acinin butunleyenidir: dis aci + ic aci = 180°
   - Dis acilar toplami = 360°

   ORNEK: A = 50°, B = 70° ise C kosesindeki dis aci = 50° + 70° = 120°
"""
},

"MAT.9.3.UCGEN_ELEMANLARI": {
    "unite": "Ucgenler",
    "baslik": "Aciortay, Kenarortay ve Ucgenin Alani",
    "icerik": """
UCGENIN OZEL ELEMANLARI VE ALAN:

1. ACIORTAY:
   - Bir aciyi iki esit parcaya bolen dogru parcasi
   - Aciortay uzerindeki her nokta, acinin kenarlarina esit uzakliktadir
   - Ic aciortaylar ucgenin IC MERKEZINDE (I) birlesir
   - Ic merkez, ic teget cemberin merkezidir
   - Dis aciortaylar ve ic aciortay bir noktada kesilebilir (dis teget merkez)

   ACIORTAY TEOREMI:
   A kosesindeki aciortay BC kenarini AB/AC oraninda boler
   |BD|/|DC| = |AB|/|AC|

2. KENARORTAY:
   - Bir koseyi karsisindaki kenarin orta noktasina birlestiren dogru parcasi
   - Ucgenin 3 kenarortayi AGIRLIK MERKEZINDE (G) birlesir
   - Agirlik merkezi kenarortayi 2:1 oraninda boler (koseden 2, orta noktadan 1)
   - Kenarortay ucgeni iki ESIT ALANA boler
   - Agirlik merkezi ucgeni 6 esit alanli ucgene boler

3. YUKSEKLIK:
   - Bir koseden karsisindaki kenara (veya uzantisina) dik indirilen dogru parcasi
   - 3 yukseklik DIKLIK MERKEZINDE (H) birlesir
   - Dik acili ucgende diklik merkezi = dik aci kosesi

4. KENAR ORTA DIKME:
   - Kenar orta noktasindan kenara dik cizilen dogru
   - 3 kenar orta dikmesi CEVRE MERKEZINDE (O) birlesir
   - Cevre merkezi, cevresi cizilen cemberin merkezidir
   - Cevre merkezinin tum koselere uzakligi esittir (yaricap R)

5. UCGENIN ALANI FORMULLERI:
   - A = (1/2) · taban · yukseklik
   - A = (1/2) · a · b · sin(C) (iki kenar ve aralarindaki aci)
   - Heron formulu: A = √[s(s-a)(s-b)(s-c)] burada s = (a+b+c)/2
   - Eskenar ucgen alani: A = (a² · √3) / 4

   ORNEK: Tabani 10 cm, yuksekligi 6 cm olan ucgenin alani:
   A = (1/2) · 10 · 6 = 30 cm²

6. OZEL UCGEN ALANLARI:
   - Dik ucgen: A = (1/2) · dik_kenar1 · dik_kenar2
   - Ikizkenar ucgende yukseklik: h = √(a² - (c/2)²) (a: esit kenar, c: taban)

7. PISAGOR TEOREMI (Dik ucgen):
   - Hipotenusun karesi = Dik kenarlarin karelerinin toplami
   - c² = a² + b² (c: hipotenüs)
   - ORNEK: a = 3, b = 4 => c = √(9 + 16) = √25 = 5
   - Pisagor uclusu: (3,4,5), (5,12,13), (8,15,17), (7,24,25)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: VERI ANALIZI
# ═══════════════════════════════════════════════════════════════

"MAT.9.4.MERKEZI_EGILIM": {
    "unite": "Veri Analizi",
    "baslik": "Merkezi Egilim Olculeri (Ortalama, Medyan, Mod)",
    "icerik": """
MERKEZI EGILIM OLCULERI:

1. ARITMETIK ORTALAMA:
   - Tum verilerin toplami / veri sayisi
   - x̄ = (x₁ + x₂ + ... + xₙ) / n = Σxᵢ / n
   - Tum verilere duyarlidir (asiri degerlerden etkilenir)
   - Frekansi veriler icin: x̄ = Σ(fᵢ · xᵢ) / Σfᵢ

   ORNEK: 4, 7, 8, 11, 15 => Ortalama = (4+7+8+11+15)/5 = 45/5 = 9

   OZELLIKLER:
   - Her veriye a eklenirse ortalama a artar
   - Her veri k ile carpilirsa ortalama k ile carpilir
   - Ortalamanin altindaki ve ustundeki sapmalar toplami = 0

2. MEDYAN (ORTANCA):
   - Veriler kucukten buyuge siralandiginda tam ortada kalan deger
   - n tek ise: Medyan = (n+1)/2. deger
   - n cift ise: Medyan = ortadaki iki degerin ortalamasi

   ORNEK (tek): 3, 5, 7, 9, 11 => Medyan = 7 (3. deger)
   ORNEK (cift): 2, 4, 6, 8 => Medyan = (4+6)/2 = 5

   OZELLIKLER:
   - Asiri degerlerden etkilenmez (robust/dayanikli)
   - Carpik dagilimli verilerde ortalamadan daha anlamlidir

3. MOD (TEPEDEGER):
   - Veri setinde en sik tekrar eden deger
   - Bir veri setinin birden fazla modu olabilir
     * Tek modlu (unimodal): 2, 3, 3, 5 => Mod = 3
     * Iki modlu (bimodal): 1, 2, 2, 4, 4, 5 => Mod = 2 ve 4
   - Tum degerler farkli ise mod yoktur
   - Kategorik veriler icin tek kullanilabilecek merkezi egilim olcusudur

4. KARSILASTIRMA:
   | Ozellik           | Ortalama   | Medyan     | Mod        |
   |--------------------|------------|------------|------------|
   | Asiri degere duyarli| Evet      | Hayir      | Hayir      |
   | Her zaman tektir   | Evet       | Evet       | Hayir      |
   | Hesaplama kolayligi| Kolay      | Siralama   | Sayma      |
   | Matematiksel islem | Uygun      | Sinirli    | Sinirli    |

5. SIMETRIK DAGILIMDA:
   - Ortalama = Medyan = Mod (ortuda ayni deger)
   - Saga carpik: Mod < Medyan < Ortalama
   - Sola carpik: Ortalama < Medyan < Mod
"""
},

"MAT.9.4.YAYILIM_OLCULERI": {
    "unite": "Veri Analizi",
    "baslik": "Yayilim Olculeri ve Veri Grafikleri",
    "icerik": """
YAYILIM OLCULERI VE GRAFIKLER:

1. ACIKLIK (RANGE):
   - En buyuk deger - En kucuk deger
   - R = x_max - x_min
   - Sadece iki ucdaki degere bakar, aradaki dagilimi gostermez
   - ORNEK: 3, 5, 7, 12, 20 => R = 20 - 3 = 17

2. VARYANS (σ²):
   - Verilerin ortalamadan sapmalarinin karelerinin ortalamasi
   - σ² = Σ(xᵢ - x̄)² / n (kitle varyans)
   - s² = Σ(xᵢ - x̄)² / (n-1) (orneklem varyans)
   - Her zaman >= 0 (negatif olamaz)
   - Birim: Verinin biriminin karesi

3. STANDART SAPMA (σ):
   - Varyansin karekoku: σ = √(σ²)
   - Verilerin ortalamadan ne kadar saptigini gosterir
   - Kucuk σ => Veriler ortalamaya yakin (homojen)
   - Buyuk σ => Veriler ortalamadan uzak (heterojen)

   ORNEK: 2, 4, 6, 8, 10 icin:
   x̄ = 6
   σ² = [(2-6)² + (4-6)² + (6-6)² + (8-6)² + (10-6)²] / 5
   σ² = [16 + 4 + 0 + 4 + 16] / 5 = 40/5 = 8
   σ = √8 ≈ 2.83

   OZELLIKLER:
   - Her veriye a eklenirse standart sapma DEGISMEZ
   - Her veri k ile carpilirsa standart sapma |k| ile carpilir

4. HISTOGRAM:
   - Surekli verilerin sinif araliklarinda gosterimi
   - X ekseni: Sinif araliklari, Y ekseni: Frekans
   - Sutunlar arasinda BOSLUK YOKTUR (surekli veri)
   - Sinif araliklari genellikle esit genislikte

5. KUTU GRAFIGI (Box Plot):
   - Bes sayilik ozet ile olusturulur:
     * Minimum (Q0)
     * 1. Ceyrek (Q1) = Alt %25
     * Medyan (Q2) = %50
     * 3. Ceyrek (Q3) = Ust %25
     * Maksimum (Q4)
   - Ceyrekler arasi aciklik (IQR) = Q3 - Q1
   - Aykiri deger (outlier): Q1 - 1.5·IQR altinda veya Q3 + 1.5·IQR ustunde
   - Kutu icindeki cizgi medyani gosterir

6. DIGER GRAFIKLER:
   - Daire grafigi: Oranlari gosterir (toplam %100)
   - Cizgi grafigi: Zamana bagli degisimleri gosterir
   - Sac-yaprak grafigi: Kumelenmis verileri gosterir
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: FONKSIYON
# ═══════════════════════════════════════════════════════════════

"MAT.9.5.FONKSIYON_KAVRAMI": {
    "unite": "Fonksiyon",
    "baslik": "Fonksiyon Kavrami, Tanim ve Deger Kumesi",
    "icerik": """
FONKSIYON KAVRAMI:

1. TANIM:
   - A kumesinin HER elemani B kumesinin TAM BIR elemaniyla eslestiriliyorsa
     bu eslestirmeye A'dan B'ye bir fonksiyon denir
   - f: A → B seklinde gosterilir
   - A: Tanim kumesi (domain), B: Deger kumesi (codomain)
   - f(x): x'in goruntüsü (image)

2. FONKSIYON OLMA KOSULLARI:
   - Tanim kumesinin her elemani MUTLAKA eslestirilmeli (acikta kalan yok)
   - Tanim kumesinin her elemani EN FAZLA BIR elemanla eslestirilmeli (dallanma yok)
   - Deger kumesinde acikta eleman kalabilir (eslesmeyen olabilir)

   FONKSIYON DEGILDIR:
   - Tanim kumesinde acikta eleman var => Fonksiyon degil
   - Tanim kumesinin bir elemani birden fazla elemanla eslesiyor => Fonksiyon degil

3. GORUNTU KUMESI:
   - f(A) = {f(x) | x ∈ A}: Tanim kumesindeki elemanlarin B'deki goruntuleri
   - Goruntu kumesi, deger kumesinin alt kumesidir: f(A) ⊂ B
   - Goruntu kumesi = Deger kumesi ise fonksiyon ORTEN

4. FONKSIYON SAYISI:
   - s(A) = m, s(B) = n ise A'dan B'ye tanimlanan fonksiyon sayisi: n^m
   - ORNEK: A = {1,2,3}, B = {a,b} => Fonksiyon sayisi = 2³ = 8

5. ESIT FONKSIYONLAR:
   - f = g ise:
     * Tanim kumeleri aynidir
     * Her x icin f(x) = g(x)

6. FONKSIYON TURLERI:
   - Birebir (enjektif): Farkli elemanlar farkli goruntulere gider
     x₁ ≠ x₂ => f(x₁) ≠ f(x₂)
     Birebir fonksiyon sayisi: n! / (n-m)! (n >= m gerekli)

   - Orten (surjektif): Deger kumesinin her elemani en az bir goruntudur
     f(A) = B (goruntu kumesi = deger kumesi)
     Her b ∈ B icin en az bir a ∈ A vardir: f(a) = b

   - Birebir ve orten (bijektif): Hem birebir hem orten
     s(A) = s(B) olmali
     Birebir orten fonksiyon sayisi: n! (n = m olmali)
"""
},

"MAT.9.5.FONKSIYON_GRAFIK": {
    "unite": "Fonksiyon",
    "baslik": "Fonksiyon Grafigi, Dogrusal ve Parcali Fonksiyon",
    "icerik": """
FONKSIYON GRAFIKLERI:

1. FONKSIYON GRAFIGI:
   - Kartezyen koordinat sisteminde (x, f(x)) noktalarinin olusturdugu egri
   - DIKEY DOGRU TESTI: Her dikey dogru grafigi en fazla bir noktada kesmelidir
     Birden fazla noktada kesiyorsa => fonksiyon degil

2. DOGRUSAL FONKSIYON:
   - f(x) = ax + b (a ≠ 0) seklindeki fonksiyon
   - Grafigi bir DOGRUDUR
   - a: Egim (slope), b: y-kesim noktasi (y-intercept)
   - a > 0: Artan fonksiyon (saga dogru yukselir)
   - a < 0: Azalan fonksiyon (saga dogru duser)
   - a = 0: Sabit fonksiyon f(x) = b (yatay dogru)

   EGIM FORMULU:
   - Iki nokta verilmisse: a = (y₂ - y₁) / (x₂ - x₁)
   - x-ekseni ile yapilan aci α ise: a = tan(α)

   ORNEK: (1, 3) ve (4, 9) noktalarindan gecen dogrusal fonksiyon:
   a = (9-3)/(4-1) = 6/3 = 2
   f(x) = 2x + b, f(1) = 3 => 2 + b = 3 => b = 1
   f(x) = 2x + 1

3. SABIT FONKSIYON:
   - f(x) = c (c sabit) seklindeki fonksiyon
   - Grafigi x-eksenine paralel yatay dogrurdur
   - Ne artan ne azalan: Sabittir

4. BIRIM (OZDESLIK) FONKSIYONU:
   - f(x) = x
   - Grafigi orijinden gecen 45° egimli dogru
   - Birebir ve orten

5. PARCALI FONKSIYON:
   - Farkli araliklarda farkli kuralli fonksiyon
   - Her parcada ayri kural uygulanir

   ORNEK:
   f(x) = { 2x + 1,  x < 0
           { x²,      x >= 0

   f(-2) = 2(-2) + 1 = -3
   f(3) = 3² = 9

6. MUTLAK DEGER FONKSIYONU:
   - f(x) = |x|: V sekilli grafik, kose noktasi orijinde
   - f(x) = |x - a| + b: Kose noktasi (a, b)'de
   - Grafik her zaman yukari acar (V sekli)
   - f(x) = -|x|: Ters V sekli (asagi acar)

7. DONUSUMLER:
   - f(x) + k: Grafik k birim yukari (k > 0) veya asagi (k < 0)
   - f(x - h): Grafik h birim saga (h > 0) veya sola (h < 0)
   - -f(x): x-eksenine gore simetri
   - f(-x): y-eksenine gore simetri
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: USLU VE KOKLU IFADELER
# ═══════════════════════════════════════════════════════════════

"MAT.9.6.USLU_IFADELER": {
    "unite": "Uslu ve Koklu Ifadeler",
    "baslik": "Tam Sayi Uslu Ifadeler",
    "icerik": """
TAM SAYI USLU IFADELER:

1. TANIM:
   - a^n = a · a · a · ... · a (n tane a, n pozitif tam sayi)
   - a: taban, n: us (kuvvet)
   - a^1 = a
   - a^0 = 1 (a ≠ 0)
   - 0^0 TANIMSIZDIR

2. NEGATIF US:
   - a^(-n) = 1 / a^n (a ≠ 0)
   - ORNEK: 2^(-3) = 1/2³ = 1/8
   - (a/b)^(-n) = (b/a)^n
   - ORNEK: (2/3)^(-2) = (3/2)² = 9/4

3. US KURALLARI:
   - a^m · a^n = a^(m+n) (ayni tabanli carpma: usler toplanir)
   - a^m / a^n = a^(m-n) (ayni tabanli bolme: usler cikarilir)
   - (a^m)^n = a^(m·n) (ustun ustu: usler carpilir)
   - (a · b)^n = a^n · b^n (carpimin ustu: us dagilir)
   - (a / b)^n = a^n / b^n (bolumun ustu: us dagilir)

4. OZEL DURUMLAR:
   - (-1)^(cift) = 1, (-1)^(tek) = -1
   - Negatif sayinin cift ustu pozitif: (-2)^4 = 16
   - Negatif sayinin tek ustu negatif: (-2)^3 = -8
   - Dikkat: -2^4 = -(2^4) = -16, ama (-2)^4 = 16

5. ORNEKLER:
   - 2^3 · 2^5 = 2^8 = 256
   - 3^6 / 3^4 = 3^2 = 9
   - (5^2)^3 = 5^6 = 15625
   - 2^3 · 3^3 = (2·3)^3 = 6^3 = 216

6. ONLUK KUVVETLER (BILIMSEL GOSTERIM):
   - Buyuk sayilar: 3.500.000 = 3,5 × 10^6
   - Kucuk sayilar: 0,00042 = 4,2 × 10^(-4)
   - Bilimsel gosterim: a × 10^n (1 <= a < 10)
"""
},

"MAT.9.6.KOKLU_IFADELER": {
    "unite": "Uslu ve Koklu Ifadeler",
    "baslik": "Koklu Ifadeler ve Denklik",
    "icerik": """
KOKLU IFADELER:

1. TANIM:
   - ⁿ√a = a^(1/n) (n: kok derecesi, a: kok ici)
   - Karekok: √a = ²√a = a^(1/2)
   - Kupkok: ³√a = a^(1/3)
   - n cift ise a >= 0 olmali (negatifin cift dereceden koku tanimsiz)
   - n tek ise a herhangi bir reel sayi olabilir

2. TEMEL OZELLIKLER:
   - √(a²) = |a| (mutlak deger!)
   - (√a)² = a (a >= 0)
   - ⁿ√(aⁿ) = |a| (n cift ise), ⁿ√(aⁿ) = a (n tek ise)
   - √a >= 0 (karekok her zaman negatif olmayan)

3. ISLEM KURALLARI:
   - √a · √b = √(a·b) (a,b >= 0)
   - √a / √b = √(a/b) (a >= 0, b > 0)
   - √(a+b) ≠ √a + √b (DIKKAT: Toplamin koku, koklerin toplami DEGILDIR!)
   - ⁿ√a · ⁿ√b = ⁿ√(a·b)
   - ᵐ√(ⁿ√a) = ᵐⁿ√a (ic ice kok: dereceler carpilir)

4. USLU-KOKLU DENKLIK:
   - a^(m/n) = ⁿ√(aᵐ) = (ⁿ√a)ᵐ
   - ORNEK: 8^(2/3) = ³√(8²) = ³√64 = 4
   - ORNEK: 27^(1/3) = ³√27 = 3

5. SADELESTIRME:
   - √12 = √(4·3) = 2√3
   - √50 = √(25·2) = 5√2
   - √72 = √(36·2) = 6√2
   - 3√2 + 5√2 = 8√2 (benzer koklu ifadeler toplanir)
   - 2√3 · 4√3 = 8 · 3 = 24

6. PAYDAYI RASYONELLESTIRME:
   - 1/√a = √a/a (payda ve payi √a ile carp)
   - 1/(√a + √b) = (√a - √b)/(a - b) (eslenigi ile carp)
   - 1/(√a - √b) = (√a + √b)/(a - b)

   ORNEK: 5/√3 = 5√3/3
   ORNEK: 2/(√5-√3) = 2(√5+√3)/((√5)²-(√3)²) = 2(√5+√3)/2 = √5+√3

7. KARSILASTIRMA:
   - Koklu ifadeleri karsilastirmak icin ayni kok derecesine getir
   - ORNEK: √3 ile ³√5 => ⁶√27 ile ⁶√25 => √3 > ³√5
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. UNITE: POLINOMLAR
# ═══════════════════════════════════════════════════════════════

"MAT.9.7.POLINOM_KAVRAMI": {
    "unite": "Polinomlar",
    "baslik": "Polinom Kavrami ve Polinom Islemleri",
    "icerik": """
POLINOM KAVRAMI VE ISLEMLERI:

1. TANIM:
   - P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀ (aₙ ≠ 0)
   - aₙ: Bas katsayi, a₀: Sabit terim
   - n: Polinomun derecesi (en buyuk x kuvveti)
   - aₙ, aₙ₋₁, ..., a₁, a₀: Katsayilar

2. DERECE:
   - Sabit polinom (sifir dereceli): P(x) = c (c ≠ 0), derece = 0
   - Sifir polinomu: P(x) = 0, derecesi TANIMSIZ
   - Dogrusal (1. derece): P(x) = ax + b (a ≠ 0)
   - Ikinci derece: P(x) = ax² + bx + c (a ≠ 0)
   - Ucuncu derece: P(x) = ax³ + bx² + cx + d (a ≠ 0)

3. ESIT POLINOMLAR:
   - P(x) = Q(x) ise ayni dereceli terimlerin katsayilari esittir
   - P(x) = ax² + bx + c ve Q(x) = 2x² + 3x + 1 esit ise
     a = 2, b = 3, c = 1

4. TOPLAMA VE CIKARMA:
   - Ayni dereceli terimlerin katsayilari toplanir/cikarilir
   - ORNEK: (3x² + 2x - 1) + (x² - 4x + 5) = 4x² - 2x + 4
   - der(P ± Q) <= max(der(P), der(Q))

5. CARPMA:
   - Her terim diger polinomun her terimiyle carpilir
   - ORNEK: (2x + 3)(x - 1) = 2x² - 2x + 3x - 3 = 2x² + x - 3
   - der(P · Q) = der(P) + der(Q)

6. POLINOM BOLME:
   - P(x) = Q(x) · B(x) + K(x) (Bolum algoritması)
   - P(x): Bolunen, Q(x): Bolen, B(x): Bolum, K(x): Kalan
   - der(K) < der(Q) (kalan derecesi bolen derecesinden kucuk)
   - Kalan 0 ise Q(x), P(x)'i tam boler

7. KALAN TEOREMI:
   - P(x) polinomu (x - a)'ya bolununce kalan = P(a)
   - ORNEK: P(x) = x³ - 2x + 1, (x - 1)'e bolum kalani:
     P(1) = 1 - 2 + 1 = 0 (kalan 0, yani x-1 tam boler)

8. CARPAN TEOREMI:
   - P(a) = 0 ise (x - a), P(x)'in bir CARPANIDIR
   - ORNEK: P(x) = x² - 5x + 6, P(2) = 4 - 10 + 6 = 0
     Yani (x - 2), P(x)'in carpanidir => P(x) = (x-2)(x-3)
"""
},

"MAT.9.7.CARPANLARA_AYIRMA": {
    "unite": "Polinomlar",
    "baslik": "Carpanlara Ayirma Yontemleri",
    "icerik": """
CARPANLARA AYIRMA:

1. ORTAK CARPAN PARANTEZINE ALMA:
   - Tum terimlerde ortak olan faktor paranteze alinir
   - ORNEK: 6x³ + 9x² = 3x²(2x + 3)
   - ORNEK: 4a²b - 8ab² + 12ab = 4ab(a - 2b + 3)

2. GRUPLAMA (IKILI GRUPLAMA):
   - Terimler gruplara ayrilir, her grupta ortak carpan cikarilir
   - ORNEK: ax + ay + bx + by = a(x+y) + b(x+y) = (x+y)(a+b)
   - ORNEK: x³ - x² + x - 1 = x²(x-1) + 1(x-1) = (x-1)(x²+1)

3. OZDESLIKLER:

   a) Iki terimin kareler farki:
      a² - b² = (a-b)(a+b)
      ORNEK: x² - 9 = (x-3)(x+3)
      ORNEK: 4x² - 25 = (2x-5)(2x+5)

   b) Tam kare acilimi:
      (a+b)² = a² + 2ab + b²
      (a-b)² = a² - 2ab + b²
      ORNEK: x² + 6x + 9 = (x+3)²
      ORNEK: x² - 10x + 25 = (x-5)²

   c) Iki terimin kupleri toplami ve farki:
      a³ + b³ = (a+b)(a² - ab + b²)
      a³ - b³ = (a-b)(a² + ab + b²)
      ORNEK: x³ - 8 = x³ - 2³ = (x-2)(x² + 2x + 4)
      ORNEK: 27x³ + 1 = (3x)³ + 1³ = (3x+1)(9x² - 3x + 1)

4. IKINCI DERECE UC TERIMLININ CARPANLARA AYRILMASI:
   - ax² + bx + c seklindeki ifade
   - Carpimi a·c, toplami b olan iki sayi bulunur
   - ORNEK: x² + 5x + 6 => carpimi 6, toplami 5: (2,3)
     x² + 5x + 6 = (x+2)(x+3)
   - ORNEK: 2x² + 7x + 3 => a·c = 6, toplami 7: (1,6)
     2x² + x + 6x + 3 = x(2x+1) + 3(2x+1) = (2x+1)(x+3)

5. FORMUL ILE KOK BULMA (DISKRIMINANT):
   - ax² + bx + c = 0 icin: Δ = b² - 4ac (diskriminant)
   - x₁,₂ = (-b ± √Δ) / (2a)
   - Δ > 0: Iki farkli reel kok
   - Δ = 0: Cakisik (esit) iki kok: x₁ = x₂ = -b/(2a)
   - Δ < 0: Reel kok yok
   - ax² + bx + c = a(x - x₁)(x - x₂)

   VIETA BAGLANTILARI:
   - x₁ + x₂ = -b/a (koklerin toplami)
   - x₁ · x₂ = c/a (koklerin carpimi)

   ORNEK: x² - 7x + 12 = 0
   Δ = 49 - 48 = 1, x = (7 ± 1)/2 => x₁ = 4, x₂ = 3
   x² - 7x + 12 = (x-4)(x-3)

6. KISIRLESTIRME UYGULAMALARI:
   - (x² - 4)/(x - 2) = (x-2)(x+2)/(x-2) = x + 2 (x ≠ 2)
   - Sadeleştirmede paydanin sifir yapan degeri haric tutulur
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik9_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_9_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik9_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_9_REFERANS.keys())
