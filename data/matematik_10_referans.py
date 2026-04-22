# -*- coding: utf-8 -*-
"""
10. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.
Lise 2. sinif duzeyinde kapsamli icerik.

Ogrenme alanlari:
1. Polinomlar (Bolme, Carpanlara Ayirma)
2. Ikinci Derece Denklemler (Diskriminant, Koklerin Ozellikleri)
3. Fonksiyonlar (Bileske, Ters Fonksiyon)
4. Trigonometri (Birim Cember, Trigonometrik Fonksiyonlar, Ozdeslikler, Grafikler)
5. Sayma (Permutasyon, Kombinasyon, Binom Acilimi)
6. Olasilik (Kosullu, Bagimsiz)
"""

MATEMATIK_10_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: POLINOMLAR
# ═══════════════════════════════════════════════════════════════

"MAT.10.1.POLINOM_TANIMI": {
    "unite": "Polinomlar",
    "baslik": "Polinom Tanimi ve Temel Kavramlar",
    "icerik": """
POLINOM TANIMI VE TEMEL KAVRAMLAR:

1. POLINOM NEDIR?
   - P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀  seklinde yazilan ifadeler.
   - aₙ, aₙ₋₁, ..., a₁, a₀ katsayilardir (reel sayilar).
   - aₙ ≠ 0 ise n polinomun derecesidir.
   - a₀: sabit terim, aₙ: baskat sayisi (baskatsayi).

2. POLINOM OLMA KOSULU:
   - Degiskenin kuvvetleri negatif olmayan tam sayi olmalidir.
   - Ornek: P(x) = 3x³ − 2x + 5 → polinom (derece = 3)
   - Ornek: Q(x) = x² + 1/x → polinom DEGILDIR (x⁻¹ terimi var)
   - Ornek: R(x) = √x + 1 → polinom DEGILDIR (x^(1/2) terimi var)

3. OZEL POLINOMLAR:
   - Sifir polinomu: P(x) = 0 (derecesi tanimsiz)
   - Sabit polinom: P(x) = c (c ≠ 0, derecesi 0)
   - Dogrusal: P(x) = ax + b (derece 1)
   - Kuadratik: P(x) = ax² + bx + c (derece 2)
   - Kubik: P(x) = ax³ + bx² + cx + d (derece 3)

4. POLINOM ESITLIGI:
   - P(x) = Q(x) ise tum katsayilar esittir.
   - P(x) = aₙxⁿ + ... + a₀ ve Q(x) = bₙxⁿ + ... + b₀ icin
     aₙ = bₙ, aₙ₋₁ = bₙ₋₁, ..., a₀ = b₀ olmalidir.

5. POLINOM DEGERI:
   - P(x) polinomunda x yerine bir sayi konarak P(a) hesaplanir.
   - Ornek: P(x) = 2x³ − x + 4 icin P(2) = 2(8) − 2 + 4 = 18
"""
},

"MAT.10.1.POLINOM_ISLEMLERI": {
    "unite": "Polinomlar",
    "baslik": "Polinomlarla Islemler (Toplama, Cikarma, Carpma)",
    "icerik": """
POLINOMLARLA ISLEMLER:

1. TOPLAMA VE CIKARMA:
   - Ayni dereceli terimlerin katsayilari toplanir/cikarilir.
   - Ornek: (3x² + 2x − 1) + (x² − 5x + 4) = 4x² − 3x + 3
   - Ornek: (3x² + 2x − 1) − (x² − 5x + 4) = 2x² + 7x − 5
   - Sonucun derecesi: max(derece(P), derece(Q))

2. CARPMA:
   - Her terim digerinin her terimiyle carpilir.
   - Ornek: (2x + 3)(x² − x + 1)
     = 2x³ − 2x² + 2x + 3x² − 3x + 3
     = 2x³ + x² − x + 3
   - Sonucun derecesi: derece(P) + derece(Q)

3. DERECE KURALLARI:
   - der(P + Q) ≤ max(der(P), der(Q))
   - der(P × Q) = der(P) + der(Q)
   - der(P − Q) ≤ max(der(P), der(Q))
   - DIKKAT: Toplama/cikarmada esitlik OLMAYABILIR (baskat sayilar sifirlanabilir)
"""
},

"MAT.10.1.POLINOM_BOLME": {
    "unite": "Polinomlar",
    "baslik": "Polinom Bolmesi ve Kalan Teoremi",
    "icerik": """
POLINOM BOLMESI:

1. BOLME ALGORITMASI:
   - P(x) = Q(x) . B(x) + K(x)
   - P(x): bolunen, Q(x): bolen, B(x): bolum, K(x): kalan
   - der(K) < der(Q) olmalidir.
   - der(B) = der(P) − der(Q)

2. UZUN BOLME YONTEMI:
   - Bolunenin baskat sayisini, bolenin baskat sayisina bol.
   - Sonucu bolen ile carp ve bolunenden cikar.
   - Islemi kalan polinomla tekrarla.
   - Ornek: (2x³ + 3x² − 5x + 1) ÷ (x − 2)
     Bolum: 2x² + 7x + 9, Kalan: 19

3. KALAN TEOREMI:
   - P(x) polinomu (x − a) ile bolundugunde kalan = P(a)
   - Ornek: P(x) = x³ − 2x + 1, (x − 3) ile bolumunden kalan:
     P(3) = 27 − 6 + 1 = 22
   - (x − a) ile bolumde kalan her zaman bir sabittir (derece 0).

4. CARPANLARA AYIRMA TEOREMI:
   - P(a) = 0 ise (x − a), P(x)'in bir carpanidir.
   - Ornek: P(x) = x³ − 6x² + 11x − 6
     P(1) = 1 − 6 + 11 − 6 = 0 → (x − 1) carpandir.
     P(x) = (x − 1)(x² − 5x + 6) = (x − 1)(x − 2)(x − 3)

5. SENTETIK BOLME (HORNER YONTEMI):
   - (x − a) ile bolmede hizli yontem.
   - Katsayilari yazilir, a ile asagi dogru islem yapilir.
   - Son sayi kalan, ust satirda katsayilar bolumdur.
   - Ornek: (2x³ + 3x² − 5x + 1) ÷ (x − 2)
     a = 2 | 2   3   −5   1
              |     4   14   18
              | 2   7    9   19  → Bolum: 2x² + 7x + 9, Kalan: 19

6. (ax + b) ILE BOLME:
   - P(x), (ax + b) ile bolundugunde kalan = P(−b/a)
   - Ornek: P(x) = 4x² − x + 3, (2x + 1) ile bolumde kalan:
     P(−1/2) = 4(1/4) − (−1/2) + 3 = 1 + 1/2 + 3 = 9/2
"""
},

"MAT.10.1.CARPANLARA_AYIRMA": {
    "unite": "Polinomlar",
    "baslik": "Carpanlara Ayirma Yontemleri",
    "icerik": """
CARPANLARA AYIRMA YONTEMLERI:

1. ORTAK CARPAN PARANTEZINE ALMA:
   - Tum terimlerde ortak olan carpanindan paranteze alinir.
   - Ornek: 6x³ − 9x² + 3x = 3x(2x² − 3x + 1)

2. GRUPLAMA:
   - Ortak carpan yoksa terimler gruplanir.
   - Ornek: x³ + x² − 4x − 4 = x²(x + 1) − 4(x + 1) = (x + 1)(x² − 4)
     = (x + 1)(x − 2)(x + 2)

3. ONEMLI OZDESLIKLER:
   - a² − b² = (a − b)(a + b)  → iki kare farki
   - a² + 2ab + b² = (a + b)²  → tam kare
   - a² − 2ab + b² = (a − b)²  → tam kare
   - a³ + b³ = (a + b)(a² − ab + b²)  → kuplerin toplami
   - a³ − b³ = (a − b)(a² + ab + b²)  → kuplerin farki
   - a³ + 3a²b + 3ab² + b³ = (a + b)³
   - a³ − 3a²b + 3ab² − b³ = (a − b)³

4. ax² + bx + c TIPI IFADELER:
   - Koku bulunur: x₁,₂ = (−b ± √(b² − 4ac)) / 2a
   - ax² + bx + c = a(x − x₁)(x − x₂)
   - Ornek: x² − 5x + 6 = (x − 2)(x − 3)
   - Ornek: 2x² − 7x + 3 = 2(x − 1/2)(x − 3) = (2x − 1)(x − 3)

5. IKILI CARPIM YONTEMI (ac YONTEMI):
   - ax² + bx + c icin a × c carpimini veren ve toplami b olan iki sayi bul.
   - Ornek: 6x² + 7x + 2 → a × c = 12, toplami 7: (3, 4)
     = 6x² + 3x + 4x + 2 = 3x(2x + 1) + 2(2x + 1) = (3x + 2)(2x + 1)
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: IKINCI DERECE DENKLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.10.2.IKINCI_DERECE_DENKLEM": {
    "unite": "Ikinci Derece Denklemler",
    "baslik": "Ikinci Derece Denklem ve Diskriminant",
    "icerik": """
IKINCI DERECE DENKLEMLER:

1. GENEL FORM:
   - ax² + bx + c = 0  (a ≠ 0)
   - a: baskat sayisi, b: x'in katsayisi, c: sabit terim

2. COZUM FORMULU (ABC FORMULU):
   - x₁,₂ = (−b ± √Δ) / (2a)
   - Δ (delta / diskriminant) = b² − 4ac

3. DISKRIMINANT VE KOK DURUMU:
   - Δ > 0 → Iki farkli reel kok (x₁ ≠ x₂)
   - Δ = 0 → Iki esit reel kok (x₁ = x₂ = −b / 2a) [cift kok]
   - Δ < 0 → Reel kok yok (kokler sanal/kompleks)

4. ORNEKLER:
   - x² − 5x + 6 = 0 → Δ = 25 − 24 = 1 > 0
     x₁ = (5 + 1)/2 = 3, x₂ = (5 − 1)/2 = 2
   - x² − 6x + 9 = 0 → Δ = 36 − 36 = 0
     x₁ = x₂ = 6/2 = 3 (cift kok)
   - x² + x + 1 = 0 → Δ = 1 − 4 = −3 < 0
     Reel kok yoktur.

5. OZEL DURUMLAR:
   - c = 0 ise: ax² + bx = 0 → x(ax + b) = 0 → x = 0 veya x = −b/a
   - b = 0 ise: ax² + c = 0 → x² = −c/a → x = ±√(−c/a) (c/a < 0 olmali)
"""
},

"MAT.10.2.KOKLERIN_OZELLIKLERI": {
    "unite": "Ikinci Derece Denklemler",
    "baslik": "Koklerin Toplami ve Carpimi (Vieta Formuleri)",
    "icerik": """
KOKLERIN TOPLAMI VE CARPIMI (VIETA FORMULERI):

1. VIETA FORMULERI:
   - ax² + bx + c = 0 denkleminin kokleri x₁ ve x₂ ise:
   - Koklerin toplami: x₁ + x₂ = −b / a
   - Koklerin carpimi: x₁ × x₂ = c / a
   - BU FORMULLER Δ ≥ 0 OLSUN OLMASIN GECERLIDIR.

2. KOKLERLE ISLEMLER:
   - x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂
   - (x₁ − x₂)² = (x₁ + x₂)² − 4x₁x₂
   - |x₁ − x₂| = √Δ / |a|
   - x₁³ + x₂³ = (x₁ + x₂)(x₁² − x₁x₂ + x₂²)
   - 1/x₁ + 1/x₂ = (x₁ + x₂) / (x₁x₂) = −b/c

3. TERS DENKLEM OLUSTURMA:
   - Kokleri x₁ ve x₂ olan denklem:
   - x² − (x₁ + x₂)x + x₁x₂ = 0
   - Ornek: Kokleri 3 ve −2 olan denklem:
     x² − (3 + (−2))x + 3(−2) = 0 → x² − x − 6 = 0

4. ORNEKLER:
   - 2x² − 7x + 3 = 0 icin:
     x₁ + x₂ = 7/2, x₁ × x₂ = 3/2
     x₁² + x₂² = (7/2)² − 2(3/2) = 49/4 − 3 = 37/4

5. KOKLERIN ISARETLERI:
   - x₁x₂ > 0 ve x₁ + x₂ > 0 → iki kok pozitif
   - x₁x₂ > 0 ve x₁ + x₂ < 0 → iki kok negatif
   - x₁x₂ < 0 → kokler zit isaretli
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

"MAT.10.3.FONKSIYON_TANIMI": {
    "unite": "Fonksiyonlar",
    "baslik": "Fonksiyon Tanimi, Cesitleri ve Ozellikleri",
    "icerik": """
FONKSIYON TANIMI VE CESITLERI:

1. FONKSIYON NEDIR?
   - A kumesinin her elemanini B kumesinin TAM BIR elemanina eslestiren bagidir.
   - f: A → B, her a ∈ A icin tek bir f(a) ∈ B vardir.
   - A: tanim kumesi (domain), B: deger kumesi, f(A): goruntu kumesi (range)
   - Goruntu kumesi ⊆ Deger kumesi

2. FONKSIYON OLMA KOSULU:
   - Tanim kumesindeki HER eleman eslenmelidir.
   - Her eleman YALNIZCA BIR elemana eslenmelidir.
   - Deger kumesinde eslenmemis eleman OLABILIR.

3. FONKSIYON CESITLERI:
   - Bire-bir (enjektif): Farkli elemanlarin goruntuleri farklidir.
     f(a₁) = f(a₂) → a₁ = a₂
   - Orten (surjektif): Goruntu kumesi = Deger kumesi (her eleman eslenir)
   - Icine (orten olmayan): Goruntu kumesi ⊂ Deger kumesi
   - Birebir-orten (bijektif): Hem bire-bir hem orten → tersi vardir.

4. FONKSIYON SAYISI:
   - |A| = m, |B| = n ise:
   - Toplam fonksiyon sayisi = nᵐ
   - Bire-bir fonksiyon (m ≤ n): P(n, m) = n! / (n − m)!
   - Orten fonksiyon: Dahil etme-disarida birakma prensibi ile hesaplanir.

5. DUSSEY CIZGI TESTI:
   - Grafik uzerinde her dussey dogruya en fazla 1 noktada kesiliyorsa fonksiyondur.
   - 1'den fazla noktada kesiyorsa fonksiyon degildir.
"""
},

"MAT.10.3.BILESKE_FONKSIYON": {
    "unite": "Fonksiyonlar",
    "baslik": "Bileske Fonksiyon",
    "icerik": """
BILESKE FONKSIYON:

1. TANIM:
   - (f ∘ g)(x) = f(g(x)) → once g, sonra f uygulanir.
   - (g ∘ f)(x) = g(f(x)) → once f, sonra g uygulanir.
   - f: A → B, g: B → C ise g ∘ f: A → C

2. ONEMLI OZELLIKLER:
   - Bileske islemi genellikle DEGISMELI DEGILDIR: f ∘ g ≠ g ∘ f
   - Bileske islemi BIRLESMELI'dir: (f ∘ g) ∘ h = f ∘ (g ∘ h)
   - Birim fonksiyon e(x) = x icin: f ∘ e = e ∘ f = f

3. ORNEKLER:
   - f(x) = 2x + 1, g(x) = x² icin:
     (f ∘ g)(x) = f(g(x)) = f(x²) = 2x² + 1
     (g ∘ f)(x) = g(f(x)) = g(2x + 1) = (2x + 1)²= 4x² + 4x + 1
   - f ∘ g ≠ g ∘ f oldugu gorulur.

4. BILESKE VE BIREBIR/ORTEN:
   - f ve g bire-bir ise g ∘ f de bire-birdir.
   - f ve g orten ise g ∘ f de ortendir.
   - f ve g bijektif ise g ∘ f de bijektiftir.

5. DENKLEM COZUMU:
   - (f ∘ g)(x) = h(x) verilmisse, f(g(x)) = h(x) denkleminden g(x) bulunur.
   - Ornek: f(x) = 3x − 2, (f ∘ g)(x) = 7x + 1
     f(g(x)) = 3g(x) − 2 = 7x + 1 → g(x) = (7x + 3) / 3
"""
},

"MAT.10.3.TERS_FONKSIYON": {
    "unite": "Fonksiyonlar",
    "baslik": "Ters Fonksiyon",
    "icerik": """
TERS FONKSIYON:

1. TANIM:
   - f: A → B bijektif (birebir ve orten) ise tersi vardir.
   - f⁻¹: B → A, f(a) = b ise f⁻¹(b) = a
   - f ∘ f⁻¹ = f⁻¹ ∘ f = e (birim fonksiyon)

2. TERS FONKSIYON BULMA:
   - y = f(x) yaz.
   - x'i y cinsinden coz.
   - x ve y'yi yer degistir.
   - Ornek: f(x) = 2x + 3
     y = 2x + 3 → x = (y − 3)/2 → f⁻¹(x) = (x − 3)/2

3. ORNEKLER:
   - f(x) = (3x − 1)/(x + 2) icin:
     y(x + 2) = 3x − 1 → yx + 2y = 3x − 1
     yx − 3x = −1 − 2y → x(y − 3) = −2y − 1
     x = (−2y − 1)/(y − 3) → f⁻¹(x) = (−2x − 1)/(x − 3)

4. GRAFIK OZELLIGI:
   - f ve f⁻¹'in grafikleri y = x dogrusuna gore simetriktir.
   - f'in (a, b) noktasi f⁻¹'in (b, a) noktasina karsilik gelir.

5. ONEMLI ILISKI:
   - f(f⁻¹(x)) = x (her x ∈ B icin)
   - f⁻¹(f(x)) = x (her x ∈ A icin)
   - (f⁻¹)⁻¹ = f
   - (g ∘ f)⁻¹ = f⁻¹ ∘ g⁻¹  (SIRA DEGISIR!)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: TRIGONOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.10.4.BIRIM_CEMBER": {
    "unite": "Trigonometri",
    "baslik": "Birim Cember ve Aci Olculeri",
    "icerik": """
BIRIM CEMBER VE ACI OLCULERI:

1. BIRIM CEMBER:
   - Merkezi orijin (0,0), yaricapi 1 olan cember.
   - Denklemi: x² + y² = 1
   - Cember uzerindeki P noktasi (cos α, sin α) koordinatlidir.

2. ACI OLCULERI:
   - Derece: Tam tur = 360°
   - Radyan: Tam tur = 2π rad
   - Donusum: α° = α × π/180 rad  |  α rad = α × 180/π derece
   - Onemli esitlikler:
     30° = π/6, 45° = π/4, 60° = π/3, 90° = π/2
     120° = 2π/3, 135° = 3π/4, 150° = 5π/6, 180° = π
     270° = 3π/2, 360° = 2π

3. YONLU ACI:
   - Pozitif yon: Saat yonunun tersi (trigonometrik yon)
   - Negatif yon: Saat yonu
   - Esdeger acilar: α ve α + 360°k (k tam sayi)

4. BOLGELERE GORE ISARETLER:
   - I. Bolge (0°−90°): sin +, cos +, tan +
   - II. Bolge (90°−180°): sin +, cos −, tan −
   - III. Bolge (180°−270°): sin −, cos −, tan +
   - IV. Bolge (270°−360°): sin −, cos +, tan −
   - EZBER: "Iste Su Tam Cemberdir" → I: S(in)+, II: S(in)+, III: T(an)+, IV: C(os)+
"""
},

"MAT.10.4.TRIGONOMETRIK_FONKSIYONLAR": {
    "unite": "Trigonometri",
    "baslik": "Sinus, Kosinus, Tanjant Fonksiyonlari",
    "icerik": """
TRIGONOMETRIK FONKSIYONLAR:

1. TEMEL TANIMLAR (Birim Cember):
   - sin α = y koordinati (karsisindaki kenar / hipotenus)
   - cos α = x koordinati (komsu kenar / hipotenus)
   - tan α = sin α / cos α = y/x (karsi kenar / komsu kenar)
   - cot α = cos α / sin α = x/y (komsu kenar / karsi kenar)
   - sec α = 1 / cos α
   - csc α = 1 / sin α

2. OZEL ACI DEGERLERI:
   - sin 0° = 0, sin 30° = 1/2, sin 45° = √2/2, sin 60° = √3/2, sin 90° = 1
   - cos 0° = 1, cos 30° = √3/2, cos 45° = √2/2, cos 60° = 1/2, cos 90° = 0
   - tan 0° = 0, tan 30° = √3/3, tan 45° = 1, tan 60° = √3, tan 90° = tanimsiz

3. DEGERLER TABLOSU (Ozel Acilar):
   α     | 0°  | 30°   | 45°   | 60°   | 90°
   sin α | 0   | 1/2   | √2/2  | √3/2  | 1
   cos α | 1   | √3/2  | √2/2  | 1/2   | 0
   tan α | 0   | √3/3  | 1     | √3    | ∞

4. PERIYOT:
   - sin x ve cos x periyodu: 2π (360°)
   - tan x ve cot x periyodu: π (180°)
   - sin(x + 2π) = sin x, cos(x + 2π) = cos x
   - tan(x + π) = tan x
"""
},

"MAT.10.4.TRIGONOMETRIK_OZDESLIKLER": {
    "unite": "Trigonometri",
    "baslik": "Trigonometrik Ozdeslikler",
    "icerik": """
TRIGONOMETRIK OZDESLIKLER:

1. TEMEL OZDESLIKLER:
   - sin²α + cos²α = 1  (Pisagor ozdeslig̈i)
   - 1 + tan²α = sec²α = 1/cos²α
   - 1 + cot²α = csc²α = 1/sin²α
   - tan α × cot α = 1

2. TOPLAM-FARK FORMULLERI:
   - sin(α ± β) = sin α cos β ± cos α sin β
   - cos(α ± β) = cos α cos β ∓ sin α sin β
   - tan(α ± β) = (tan α ± tan β) / (1 ∓ tan α tan β)

3. IKI KAT ACI FORMULLERI:
   - sin 2α = 2 sin α cos α
   - cos 2α = cos²α − sin²α = 2cos²α − 1 = 1 − 2sin²α
   - tan 2α = 2 tan α / (1 − tan²α)

4. YARIM ACI FORMULLERI:
   - sin²(α/2) = (1 − cos α) / 2
   - cos²(α/2) = (1 + cos α) / 2
   - tan(α/2) = sin α / (1 + cos α) = (1 − cos α) / sin α

5. CARPIMDAN TOPLAMA:
   - sin α cos β = [sin(α + β) + sin(α − β)] / 2
   - cos α cos β = [cos(α − β) + cos(α + β)] / 2
   - sin α sin β = [cos(α − β) − cos(α + β)] / 2

6. TOPLAMDAN CARPIMA:
   - sin A + sin B = 2 sin((A+B)/2) cos((A−B)/2)
   - sin A − sin B = 2 cos((A+B)/2) sin((A−B)/2)
   - cos A + cos B = 2 cos((A+B)/2) cos((A−B)/2)
   - cos A − cos B = −2 sin((A+B)/2) sin((A−B)/2)
"""
},

"MAT.10.4.TRIGONOMETRIK_GRAFIKLER": {
    "unite": "Trigonometri",
    "baslik": "Trigonometrik Fonksiyon Grafikleri",
    "icerik": """
TRIGONOMETRIK FONKSIYON GRAFIKLERI:

1. y = sin x GRAFIGI:
   - Tanim kumesi: Tum reel sayilar (R)
   - Deger kumesi: [−1, 1]
   - Periyot: 2π, Genlik: 1
   - x = 0'da y = 0, x = π/2'de y = 1, x = π'de y = 0
   - x = 3π/2'de y = −1, x = 2π'de y = 0
   - Orijinden simetrik (tek fonksiyon): sin(−x) = −sin x

2. y = cos x GRAFIGI:
   - Tanim kumesi: R, Deger kumesi: [−1, 1]
   - Periyot: 2π, Genlik: 1
   - x = 0'da y = 1, x = π/2'de y = 0, x = π'de y = −1
   - y eksenine gore simetrik (cift fonksiyon): cos(−x) = cos x
   - cos x = sin(x + π/2) → sin grafiginin π/2 sola kaymisi

3. y = tan x GRAFIGI:
   - Tanim kumesi: R − {π/2 + kπ | k ∈ Z}
   - Deger kumesi: R (tum reel sayilar)
   - Periyot: π
   - x = π/2 + kπ noktalarinda dussey asimptot vardir.
   - Orijinden simetrik (tek fonksiyon): tan(−x) = −tan x
   - Surekli artandir (her periyotta)

4. DONUSUMLER: y = a sin(bx + c) + d
   - a: Genlik (|a|), grafigi y yonunde gerer/sikstirir
   - b: Periyot = 2π/|b|, grafigi x yonunde sikstirir/gerer
   - c: Yatay kayma (c/b kadar sola)
   - d: Dussey kayma (d kadar yukari)
   - Ornek: y = 3 sin(2x − π/3) + 1
     Genlik = 3, Periyot = π, Sag kayma = π/6, Yukari kayma = 1
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. OGRENME ALANI: SAYMA
# ═══════════════════════════════════════════════════════════════

"MAT.10.5.PERMUTASYON": {
    "unite": "Sayma",
    "baslik": "Faktoriyel ve Permutasyon",
    "icerik": """
FAKTORIYEL VE PERMUTASYON:

1. FAKTORIYEL:
   - n! = n × (n−1) × (n−2) × ... × 2 × 1
   - 0! = 1 (tanimla belirlenir)
   - 1! = 1, 2! = 2, 3! = 6, 4! = 24, 5! = 120
   - 6! = 720, 7! = 5040, 8! = 40320, 9! = 362880, 10! = 3628800
   - n! = n × (n−1)!  (ozyinelemeli tanim)

2. PERMUTASYON (SIRALAMA):
   - n elemanin r tanesini SIRALI secme.
   - P(n, r) = n! / (n − r)!
   - Ornek: P(5, 3) = 5! / 2! = 120 / 2 = 60
   - P(n, n) = n!  (tum elemanlarin sirali dizilisi)
   - P(n, 1) = n

3. CARPMA ILKESI:
   - Bir is m, ikinci is n yolla yapilabiliyorsa toplam = m × n
   - Ornek: 3 gomlek, 4 pantolon → 3 × 4 = 12 farkli kombinasyon

4. TOPLAMA ILKESI:
   - Bir is m VEYA n yolla yapilabiliyorsa toplam = m + n
   - (isler birlikte yapilamaz, yani ayrik olaylar)

5. TEKRARLI PERMUTASYON:
   - n elemanin r tanesinin tekrarli sirali dizilisi = nʳ
   - Ornek: 3 harften 2 basamakli sifreler (tekrarli): 3² = 9

6. AYNI CINSTEN ELEMANLARIN PERMUTASYONU:
   - n elemandan n₁ tanesi ayni, n₂ tanesi ayni, ... nₖ tanesi ayni ise:
   - Permutasyon = n! / (n₁! × n₂! × ... × nₖ!)
   - Ornek: "MALATYA" kelimesinin harf permutasyonu:
     7 harf, A:3 tane, M:1, L:1, T:1, Y:1 → 7! / 3! = 5040 / 6 = 840
"""
},

"MAT.10.5.KOMBINASYON": {
    "unite": "Sayma",
    "baslik": "Kombinasyon",
    "icerik": """
KOMBINASYON:

1. TANIM:
   - n elemanin r tanesini SIRASIZ secme (siralama ONEMSIZ).
   - C(n, r) = n! / (r! × (n − r)!)
   - Diger gosterimler: ₙCᵣ, (n r) [binom katsayisi]

2. ORNEKLER:
   - C(5, 2) = 5! / (2! × 3!) = 120 / (2 × 6) = 10
   - C(10, 3) = 10! / (3! × 7!) = 720 / 6 = 120
   - C(6, 0) = 1, C(6, 6) = 1, C(6, 1) = 6

3. ONEMLI OZELLIKLER:
   - C(n, r) = C(n, n − r) → simetri ozelligi
   - C(n, 0) = C(n, n) = 1
   - C(n, 1) = C(n, n − 1) = n
   - C(n, r) = C(n − 1, r − 1) + C(n − 1, r) → Pascal ozelligi

4. PERMUTASYON - KOMBINASYON FARKI:
   - Permutasyon: SIRA ONEMLI (baskan, baskan yrd secimi)
   - Kombinasyon: SIRA ONEMSIZ (komite secimi)
   - P(n, r) = C(n, r) × r!
   - Ornek: 5 kisiden 3 kisilik komite: C(5,3) = 10
   - Ornek: 5 kisiden baskan + bsk.yrd. + sekreter: P(5,3) = 60

5. PASCAL UCGENI:
        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1
   1 5 10 10 5 1
   - n. satir: C(n,0), C(n,1), ..., C(n,n)
"""
},

"MAT.10.5.BINOM_ACILIMI": {
    "unite": "Sayma",
    "baslik": "Binom Acilimi (Newton Binomu)",
    "icerik": """
BINOM ACILIMI:

1. BINOM FORMULU:
   - (a + b)ⁿ = Σ C(n, k) × aⁿ⁻ᵏ × bᵏ  (k = 0'dan n'e kadar)
   - (a + b)ⁿ = C(n,0)aⁿ + C(n,1)aⁿ⁻¹b + C(n,2)aⁿ⁻²b² + ... + C(n,n)bⁿ

2. ORNEKLER:
   - (x + y)⁴ = x⁴ + 4x³y + 6x²y² + 4xy³ + y⁴
   - (a − b)³ = a³ − 3a²b + 3ab² − b³
   - (2x + 1)³ = 8x³ + 12x² + 6x + 1

3. GENEL TERIM:
   - (a + b)ⁿ aciliminin (r + 1). terimi:
   - Tᵣ₊₁ = C(n, r) × aⁿ⁻ʳ × bʳ   (r = 0, 1, 2, ..., n)
   - Ornek: (x + 2)⁵'in 3. terimi (r = 2):
     T₃ = C(5,2) × x³ × 2² = 10 × x³ × 4 = 40x³

4. ONEMLI OZELLIKLER:
   - Toplam terim sayisi: n + 1
   - Katsayilar toplami: (1 + 1)ⁿ = 2ⁿ → a = b = 1 konulur
   - Isaret degisimli katsayilar toplami: (1 − 1)ⁿ = 0 → b = −1 konulur
   - Orta terim: n cift ise (n/2 + 1). terim; n tek ise iki orta terim

5. OZEL DURUMLAR:
   - (1 + x)ⁿ = 1 + nx + C(n,2)x² + C(n,3)x³ + ... + xⁿ
   - (a − b)ⁿ icinde b yerine (−b) yazilir → isaret degisir:
     C(n,k)(−1)ᵏ × aⁿ⁻ᵏ × bᵏ
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. OGRENME ALANI: OLASILIK
# ═══════════════════════════════════════════════════════════════

"MAT.10.6.OLASILIK_TEMELLERI": {
    "unite": "Olasilik",
    "baslik": "Olasilik Temel Kavramlari",
    "icerik": """
OLASILIK TEMEL KAVRAMLARI:

1. DENEY VE ORNEK UZAY:
   - Deney: Sonucu onceden kesin bilinemeyen islem (zar atma, yazi-tura)
   - Ornek uzay (S): Tum olasi sonuclarin kumesi
   - Olay (A): Ornek uzayin alt kumesi
   - Ornek: Zar atma → S = {1, 2, 3, 4, 5, 6}, |S| = 6
   - "Cift gelme" olayi: A = {2, 4, 6}, |A| = 3

2. KLASIK OLASILIK:
   - P(A) = |A| / |S| = Istenen sonuc sayisi / Toplam sonuc sayisi
   - 0 ≤ P(A) ≤ 1
   - P(∅) = 0 (imkansiz olay), P(S) = 1 (kesin olay)

3. TAMAMLAYICI OLAY:
   - A' (A tamamlayani): A'nin olmamasi
   - P(A') = 1 − P(A)
   - Ornek: Zar atildiginda asal gelmeme olasiligi:
     Asal = {2, 3, 5} → P = 3/6 = 1/2 → gelmeme = 1 − 1/2 = 1/2

4. BIRLESIM VE KESISIM:
   - P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
   - A ve B ayrik (mutually exclusive) ise: P(A ∪ B) = P(A) + P(B)
   - Ornek: Zar → A: cift, B: 3'ten buyuk
     A = {2,4,6}, B = {4,5,6}, A ∩ B = {4,6}
     P(A ∪ B) = 3/6 + 3/6 − 2/6 = 4/6 = 2/3
"""
},

"MAT.10.6.KOSULLU_OLASILIK": {
    "unite": "Olasilik",
    "baslik": "Kosullu Olasilik ve Bagimsiz Olaylar",
    "icerik": """
KOSULLU OLASILIK VE BAGIMSIZ OLAYLAR:

1. KOSULLU OLASILIK:
   - B olayi gerceklestikten sonra A'nin olasiligi:
   - P(A|B) = P(A ∩ B) / P(B)  (P(B) > 0)
   - Ornek: Bir zardan 3'ten buyuk geldigi biliniyor. Cift olma olasiligi?
     B = {4,5,6}, A ∩ B = {4,6} → P(A|B) = 2/3

2. CARPIM KURALI:
   - P(A ∩ B) = P(A|B) × P(B) = P(B|A) × P(A)
   - Ornek: Torbada 5 kirmizi, 3 mavi top. Iade etmeden 2 top cekilir.
     Ikisinin de kirmizi olma olasiligi:
     P = (5/8) × (4/7) = 20/56 = 5/14

3. BAGIMSIZ OLAYLAR:
   - A ve B bagimsiz ise: P(A ∩ B) = P(A) × P(B)
   - Ayrica: P(A|B) = P(A) ve P(B|A) = P(B)
   - Ornek: Iki zar atilir. Birincide 6, ikincide cift gelme olasiligi:
     P = (1/6) × (3/6) = 1/12

4. BAYES TEOREMI:
   - P(A|B) = P(B|A) × P(A) / P(B)
   - Toplam olasilik: P(B) = P(B|A₁)P(A₁) + P(B|A₂)P(A₂) + ... + P(B|Aₙ)P(Aₙ)

5. AGAC DIYAGRAMI:
   - Ardisik olaylarda dallanma ile gosterim.
   - Her dalda olasiliklarla carpim yapilir.
   - Ayni seviyedeki toplam olasilik = 1
   - Ornek: 2 kez yazi-tura:
     YY: 1/4, YT: 1/4, TY: 1/4, TT: 1/4 → Toplam = 1

6. "EN AZ BIR" PROBLEMLERI:
   - P(en az 1) = 1 − P(hic olmamasi)
   - Ornek: 3 kez zar. En az bir 6 gelme olasiligi:
     P(hic 6 gelmemesi) = (5/6)³ = 125/216
     P(en az bir 6) = 1 − 125/216 = 91/216
"""
},

# ═══════════════════════════════════════════════════════════════
# SINAV STRATEJISI VE IPUCLARI
# ═══════════════════════════════════════════════════════════════

"MAT.10.SINAV_STRATEJISI": {
    "unite": "Sinav Stratejisi",
    "baslik": "10. Sinif Matematik Sinav Ipuclari",
    "icerik": """
10. SINIF MATEMATIK SINAV STRATEJISI:

1. POLINOMLAR:
   - Kalan teoremini aktif kullan: P(x), (x−a) ile bolumde kalan = P(a).
   - Carpanlara ayirmada once ortak carpan, sonra ozdeslik, sonra kok bulma dene.
   - Sentetik bolme (Horner) uzun bolmeden hizlidir.

2. IKINCI DERECE DENKLEMLER:
   - Diskriminanti hesapla: Δ = b² − 4ac ile kok durumunu belirle.
   - Vieta formulleri ile kok bulmadan islem yapabilirsin.
   - x₁² + x₂² = (x₁ + x₂)² − 2x₁x₂ formulunu ezberle.

3. FONKSIYONLAR:
   - Bileske fonksiyonda is sirasi: (f ∘ g)(x) = f(g(x)) → once g sonra f.
   - Ters fonksiyon icin y = f(x) yaz, x'i coz, x-y yer degistir.
   - Bijektif (birebir + orten) olmayan fonksiyonun tersi yoktur.

4. TRIGONOMETRI:
   - sin²α + cos²α = 1 ozdesligini her zaman aklinda tut.
   - Ozel aci degerlerini (30°, 45°, 60°) ezberle.
   - Bolgelerdeki isaret kuralini hatirlayarak kontrol et.

5. SAYMA VE OLASILIK:
   - Sira onemliyse permutasyon, onemsizse kombinasyon.
   - "En az bir" → tamamlayici olay kullan.
   - Agac diyagrami karmasik ardisik olaylarda cok faydali.
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik10_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_10_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik10_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_10_REFERANS.keys())
