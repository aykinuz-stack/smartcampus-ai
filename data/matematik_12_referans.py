# -*- coding: utf-8 -*-
"""
12. Sinif Matematik dersi - MEB 2025 mufredatina uygun referans verileri.
Ogrenme alanlari:
1. Ustel ve Logaritmik Fonksiyonlar
2. Diziler ve Seriler
3. Turev
4. Integral
5. Olasilik ve Istatistik
"""

MATEMATIK_12_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: USTEL VE LOGARITMIK FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

"MAT.12.1.USTEL_FONK": {
    "unite": "Üstel ve Logaritmik Fonksiyonlar",
    "baslik": "Üstel Fonksiyonlar",
    "icerik": """USTEL FONKSIYONLAR:

1. TANIM:
   - f(x) = a^x (a > 0, a ≠ 1) bicimindeki fonksiyonlara ustel fonksiyon denir.
   - Tanim kumesi: R (tum reel sayilar)
   - Deger kumesi: (0, +∞) — her zaman pozitif deger alir.

2. OZELLIKLER:
   - a > 1 ise fonksiyon kesinlikle artandir.
   - 0 < a < 1 ise fonksiyon kesinlikle azalandir.
   - f(0) = 1 her zaman gecerlidir (y-ekseni kesim noktasi).
   - Yatay asimptot: y = 0 (x-ekseni).
   - Fonksiyon bire-birdir ve ortendir (deger kumesine gore).

3. GRAFIK YORUMLAMA:
   - a > 1: Sol tarafta x-eksenine yaklasir, sag tarafta hizla yukselir.
   - 0 < a < 1: Sol tarafta hizla yukselir, sag tarafta x-eksenine yaklasir.
   - Tum ustel fonksiyonlar (0,1) noktasindan gecer.

4. USTEL DENKLEM VE ESITSIZLIKLER:
   - a^f(x) = a^g(x) ise f(x) = g(x) (a > 0, a ≠ 1).
   - a > 1 icin: a^f(x) > a^g(x) ise f(x) > g(x).
   - 0 < a < 1 icin: a^f(x) > a^g(x) ise f(x) < g(x) (esitsizlik yonu degisir).

5. UYGULAMALAR:
   - Nufus artisi: N(t) = N₀ · e^(kt) (k > 0 artis, k < 0 azalis).
   - Bilesik faiz: A = P(1 + r/n)^(nt).
   - Radyoaktif bozunma: N(t) = N₀ · (1/2)^(t/T) (T: yari omur).
"""
},

"MAT.12.1.LOGARITMA_TANIM": {
    "unite": "Üstel ve Logaritmik Fonksiyonlar",
    "baslik": "Logaritma Tanimi ve Ozellikleri",
    "icerik": """LOGARITMA:

1. TANIM:
   - a^b = c ise log_a(c) = b seklinde yazilir (a > 0, a ≠ 1, c > 0).
   - Logaritma, ustel fonksiyonun tersidir.
   - log_a(x): "a tabaninda x'in logaritmasi" diye okunur.

2. OZEL LOGARITMALAR:
   - log(x) veya log₁₀(x): 10 tabanli (Briggs) logaritma.
   - ln(x) veya logₑ(x): Dogal (Euler sayisi e ≈ 2,71828) logaritma.

3. TEMEL OZELLIKLER:
   - log_a(1) = 0 (cunku a^0 = 1).
   - log_a(a) = 1 (cunku a^1 = a).
   - log_a(a^n) = n.
   - a^(log_a(x)) = x (x > 0).

4. LOGARITMA KURALLARI:
   - Carpim: log_a(x · y) = log_a(x) + log_a(y).
   - Bolum: log_a(x / y) = log_a(x) - log_a(y).
   - Us: log_a(x^n) = n · log_a(x).
   - Taban degistirme: log_a(x) = log_b(x) / log_b(a).
   - Taban-arguman yer degistirme: log_a(b) = 1 / log_b(a).

5. LOGARITMIK FONKSIYON:
   - f(x) = log_a(x) fonksiyonunun tanim kumesi (0, +∞).
   - Deger kumesi: R.
   - a > 1 ise kesinlikle artan; 0 < a < 1 ise kesinlikle azalan.
   - Dusey asimptot: x = 0 (y-ekseni).
   - Grafik (1,0) noktasindan gecer.

6. LOGARITMIK DENKLEM VE ESITSIZLIKLER:
   - log_a(f(x)) = log_a(g(x)) ise f(x) = g(x), f(x) > 0, g(x) > 0.
   - a > 1 icin log_a(f(x)) > log_a(g(x)) ise f(x) > g(x).
   - 0 < a < 1 icin log_a(f(x)) > log_a(g(x)) ise f(x) < g(x).
"""
},

"MAT.12.1.USTEL_LOG_UYGULAMALARI": {
    "unite": "Üstel ve Logaritmik Fonksiyonlar",
    "baslik": "Üstel ve Logaritmik Fonksiyon Uygulamalari",
    "icerik": """USTEL VE LOGARITMIK FONKSIYON UYGULAMALARI:

1. DEPREM SIDDETINI OLCME (RICHTER OLCEGI):
   - M = log(A/A₀) formulu ile hesaplanir.
   - Her tam sayi artisi 10 kat daha buyuk genlik, ~31,6 kat daha fazla enerji demektir.

2. SES SIDDETI (DESIBEL):
   - β = 10 · log(I/I₀) (I₀ = 10⁻¹² W/m²).
   - Desibel olcegi logaritmiktir; 10 dB artis 10 kat siddet artisi demektir.

3. PH HESABI:
   - pH = -log[H⁺] (hidrojen iyonu konsantrasyonu).
   - pH < 7 asidik, pH = 7 notr, pH > 7 bazik.

4. NUFUS MODELLERI:
   - Ustel buyume: P(t) = P₀ · e^(rt).
   - Ikiye katlanma suresi: T = ln(2)/r.
   - Logistik buyume: P(t) = K / (1 + ((K-P₀)/P₀) · e^(-rt)).

5. BILESIK FAIZ VE SUREKLI FAIZ:
   - Bilesik: A = P(1 + r/n)^(nt).
   - Surekli: A = P · e^(rt) (n → ∞ limiti).

6. KARBON-14 YASLAMA:
   - N(t) = N₀ · e^(-λt), λ = ln(2)/5730.
   - t = -ln(N/N₀) / λ ile yasi hesaplanir.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: DIZILER VE SERILER
# ═══════════════════════════════════════════════════════════════

"MAT.12.2.DIZI_TANIM": {
    "unite": "Diziler ve Seriler",
    "baslik": "Diziler ve Temel Kavramlar",
    "icerik": """DIZILER:

1. TANIM:
   - Dogal sayilar kumesinden reel sayilara tanimlanan her fonksiyona dizi denir.
   - a: N → R, n → aₙ seklinde gosterilir.
   - aₙ: dizinin genel terimi (n. terimi).
   - (aₙ) = (a₁, a₂, a₃, ...) seklinde yazilir.

2. DIZI CESITLERI:
   - Artan dizi: Her n icin aₙ₊₁ > aₙ.
   - Azalan dizi: Her n icin aₙ₊₁ < aₙ.
   - Monoton dizi: Ya surekli artan ya da surekli azalan.
   - Sinirli dizi: Hem alttan hem ustten sinirli.

3. ARITMETIK DIZI:
   - Ardisik iki terim arasi fark sabittir: d = aₙ₊₁ - aₙ.
   - Genel terim: aₙ = a₁ + (n-1)d.
   - n terim toplami: Sₙ = n(a₁ + aₙ)/2 = n(2a₁ + (n-1)d)/2.
   - Orta terim ozelligi: aₙ = (aₙ₋₁ + aₙ₊₁)/2.

4. GEOMETRIK DIZI:
   - Ardisik iki terim orani sabittir: r = aₙ₊₁/aₙ (a₁ ≠ 0).
   - Genel terim: aₙ = a₁ · r^(n-1).
   - n terim toplami: Sₙ = a₁(r^n - 1)/(r - 1) (r ≠ 1).
   - Orta terim ozelligi: aₙ² = aₙ₋₁ · aₙ₊₁.

5. HARMONIK DIZI:
   - Bir aritmetik dizinin terimlerinin terslerinden olusan dizidir.
   - 1/aₙ aritmetik dizi ise (aₙ) harmonik dizidir.

6. FIBONACCI DIZISI:
   - F₁ = 1, F₂ = 1, Fₙ = Fₙ₋₁ + Fₙ₋₂ (n ≥ 3).
   - Ardisik terimlerin orani Altin Orana (φ ≈ 1,618) yakinsar.
"""
},

"MAT.12.2.SERILER": {
    "unite": "Diziler ve Seriler",
    "baslik": "Seriler ve Yakinsaklik",
    "icerik": """SERILER:

1. TANIM:
   - Bir dizinin terimlerinin toplamina seri denir.
   - Σ(n=1, ∞) aₙ = a₁ + a₂ + a₃ + ... seklinde yazilir.
   - Kismi toplamlar dizisi: Sₙ = a₁ + a₂ + ... + aₙ.
   - lim(n→∞) Sₙ = S (sonlu) ise seri yakinsar, S sonsuz ise iraksar.

2. GEOMETRIK SERI:
   - Σ(n=0, ∞) a·r^n = a/(1-r) (|r| < 1 ise yakinsar).
   - |r| ≥ 1 ise geometrik seri iraksar.
   - Ornek: 1 + 1/2 + 1/4 + 1/8 + ... = 2 (a=1, r=1/2).

3. TELESKOPIK SERI:
   - Ardisik terimler birbirini goturur.
   - Σ(1/(n(n+1))) = Σ(1/n - 1/(n+1)) = 1.
   - Kismi kesir ayristirilarak cozulur.

4. HARMONIK SERI:
   - Σ(1/n) = 1 + 1/2 + 1/3 + ... iraksar.
   - Yavascesine buyur ama sonsuza gider.

5. YAKINSAKLIK TESTLERI (TANITIM):
   - Gerekli kosul: lim(aₙ) = 0 olmali (yeterli degil).
   - Oran testi: lim|aₙ₊₁/aₙ| < 1 ise yakinsar.
   - Karsilastirma testi: 0 ≤ aₙ ≤ bₙ ve Σbₙ yakinsar ise Σaₙ yakinsar.

6. SONSUZ ONDALIK KESIRLERIN SERI GOSTERIMI:
   - 0,333... = 3/10 + 3/100 + 3/1000 + ... = 1/3.
   - Her devirli ondalik kesir geometrik seri ile rasyonel sayiya donusturulur.
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: TUREV
# ═══════════════════════════════════════════════════════════════

"MAT.12.3.TUREV_TANIM": {
    "unite": "Türev",
    "baslik": "Türevin Tanimi ve Temel Kurallar",
    "icerik": """TUREV TANIMI:

1. LIMIT ILE TANIM:
   - f'(x) = lim(h→0) [f(x+h) - f(x)] / h
   - Bir noktada turev: f'(a) = lim(x→a) [f(x) - f(a)] / (x - a)
   - Turev, fonksiyonun anlık degisim hizini verir.

2. GEOMETRIK ANLAM:
   - f'(a), f fonksiyonunun x = a noktasindaki teget dogrusu egimidir.
   - Teget denklemi: y - f(a) = f'(a)(x - a).
   - Normal dogrusu: Tegete dik, egim = -1/f'(a).

3. TUREV ALMA KURALLARI:
   - Sabit: (c)' = 0.
   - Kuvvet: (x^n)' = n·x^(n-1).
   - Sabit carpan: (c·f)' = c·f'.
   - Toplam/Fark: (f ± g)' = f' ± g'.
   - Carpim: (f·g)' = f'·g + f·g'.
   - Bolum: (f/g)' = (f'·g - f·g') / g².
   - Zincir kurali: (f(g(x)))' = f'(g(x))·g'(x).

4. OZEL FONKSIYONLARIN TUREVLERI:
   - (e^x)' = e^x.
   - (a^x)' = a^x · ln(a).
   - (ln x)' = 1/x.
   - (log_a x)' = 1/(x · ln a).
   - (sin x)' = cos x.
   - (cos x)' = -sin x.
   - (tan x)' = 1/cos²x = sec²x.

5. TUREVLENEBILIRLIK:
   - f, x = a'da turevlenebilir ise x = a'da sureklidir (tersi her zaman dogru degil).
   - |x| fonksiyonu x = 0'da sureklidir ama turevlenebilir degildir.
"""
},

"MAT.12.3.TUREV_UYGULAMALARI": {
    "unite": "Türev",
    "baslik": "Turev Uygulamalari",
    "icerik": """TUREV UYGULAMALARI:

1. ARTAN-AZALAN FONKSIYONLAR:
   - f'(x) > 0 olan araliklarda f artandir.
   - f'(x) < 0 olan araliklarda f azalandir.
   - f'(x) = 0 olan noktalar kritik noktalardir.

2. YEREL MAKSIMUM VE MINIMUM:
   - Birinci turev testi: f' isaret + → - gecisi ise yerel maks, - → + ise yerel min.
   - Ikinci turev testi: f'(c) = 0 ve f''(c) < 0 ise yerel maks, f''(c) > 0 ise yerel min.
   - Mutlak max/min: Kapali aralikta kritik noktalar ve uc degerler karsilastirilir.

3. BUKUM NOKTASI VE KONKAVLIK:
   - f''(x) > 0: Konkav yukari (cenak yukari, gulen yuz).
   - f''(x) < 0: Konkav asagi (cenak asagi, uzgun yuz).
   - Bukum noktasi: f''(x) isaret degistirir.

4. ASIMPTOTLAR:
   - Yatay: lim(x→±∞) f(x) = L ise y = L.
   - Dusey: f(x) → ±∞ olan x = a noktalari.
   - Egri: lim(x→∞) f(x)/x = a ve lim(x→∞)[f(x)-ax] = b ise y = ax + b.

5. EGRI CIZIMI:
   - Adimlar: Tanim kumesi → Simetri → Kesim noktalari → Turev (artan/azalan) →
     Kritik noktalar → Ikinci turev (konkavlik) → Asimptotlar → Grafik cizimi.

6. OPTIMIZASYON PROBLEMLERI:
   - Maks alan, min maliyet, maks hacim gibi problemlerde:
     a) Amac fonksiyonu olustur.
     b) Kisitlarla tek degiskenli yap.
     c) Turev al, sifira esitle, kritik noktalari bul.
     d) Ikinci turev veya aralik kontrolu ile maks/min dogrula.

7. ILISKILI DEGISIM HIZLARI:
   - Zincir kurali ile bagli degiskenlerin degisim hizlari hesaplanir.
   - Ornek: Balon sismesi, merdiven kaymasi, su deposu problemleri.
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: INTEGRAL
# ═══════════════════════════════════════════════════════════════

"MAT.12.4.BELIRSIZ_INTEGRAL": {
    "unite": "İntegral",
    "baslik": "Belirsiz Integral",
    "icerik": """BELIRSIZ INTEGRAL:

1. TANIM:
   - F'(x) = f(x) ise F(x), f(x)'in bir ters turevidir (anti-turev).
   - ∫f(x)dx = F(x) + C (C: integral sabiti, keyfi sabit).
   - Turev alma isleminin tersidir.

2. TEMEL INTEGRAL FORMULLERI:
   - ∫x^n dx = x^(n+1)/(n+1) + C (n ≠ -1).
   - ∫1/x dx = ln|x| + C.
   - ∫e^x dx = e^x + C.
   - ∫a^x dx = a^x/ln(a) + C.
   - ∫sin x dx = -cos x + C.
   - ∫cos x dx = sin x + C.
   - ∫sec²x dx = tan x + C.
   - ∫1/(1+x²) dx = arctan x + C.

3. INTEGRAL ALMA KURALLARI:
   - Sabit carpan: ∫c·f(x)dx = c·∫f(x)dx.
   - Toplam/Fark: ∫(f ± g)dx = ∫f dx ± ∫g dx.

4. YERDEGISTIRME (DONUSUM) YONTEMI:
   - u = g(x) secilir, du = g'(x)dx.
   - ∫f(g(x))·g'(x)dx = ∫f(u)du.
   - Ornek: ∫2x·e^(x²)dx → u=x², du=2xdx → e^u + C = e^(x²) + C.

5. KISMI INTEGRAL:
   - ∫u dv = u·v - ∫v du.
   - LIATE kurali: Logaritmik > Ters trigonometrik > Cebirsel > Trigonometrik > Ustel.
   - u secimi bu oncelik sirasina gore yapilir.

6. KISMI KESIR AYRISMASI:
   - Rasyonel fonksiyonlarin integralinde kullanilir.
   - P(x)/Q(x) → A/(x-a) + B/(x-b) + ... seklinde ayristirilir.
"""
},

"MAT.12.4.BELIRLI_INTEGRAL": {
    "unite": "İntegral",
    "baslik": "Belirli Integral ve Alan Hesabi",
    "icerik": """BELIRLI INTEGRAL:

1. TANIM:
   - ∫[a,b] f(x)dx = F(b) - F(a) (Analizin Temel Teoremi).
   - a: alt sinir, b: ust sinir.
   - Geometrik anlam: f(x) egrisi ile x-ekseni arasindaki net alan.

2. ANALIZIN TEMEL TEOREMI:
   - Birinci kisim: F(x) = ∫[a,x] f(t)dt ise F'(x) = f(x).
   - Ikinci kisim: ∫[a,b] f(x)dx = F(b) - F(a).
   - Turev ve integral arasindaki temel bag.

3. OZELLIKLER:
   - ∫[a,a] f(x)dx = 0.
   - ∫[a,b] f(x)dx = -∫[b,a] f(x)dx.
   - ∫[a,b] f(x)dx = ∫[a,c] f(x)dx + ∫[c,b] f(x)dx (a < c < b).
   - ∫[a,b] |f(x)|dx ≥ |∫[a,b] f(x)dx|.

4. ALAN HESABI:
   - Egri ile x-ekseni arasi alan: A = ∫[a,b] |f(x)|dx.
   - f(x) ≥ 0 ise A = ∫[a,b] f(x)dx.
   - f(x) < 0 ise o kismin mutlak degeri alinir.
   - Iki egri arasi alan: A = ∫[a,b] |f(x) - g(x)|dx.
   - Kesisim noktalari sinirlari belirler.

5. HACIM HESABI (DONEL CISIM):
   - x-ekseni etrafinda: V = π·∫[a,b] [f(x)]²dx (disk yontemi).
   - Iki fonksiyon arasi: V = π·∫[a,b] ([f(x)]² - [g(x)]²)dx (halka yontemi).

6. UYGULAMALAR:
   - Fizik: Konum = ∫hız dt, Hiz = ∫ivme dt.
   - Is = ∫F(x)dx (kuvvet-yer degistirme).
   - Ortalama deger: f_ort = (1/(b-a))·∫[a,b] f(x)dx.
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. OGRENME ALANI: OLASILIK VE ISTATISTIK
# ═══════════════════════════════════════════════════════════════

"MAT.12.5.OLASILIK": {
    "unite": "Olasılık ve İstatistik",
    "baslik": "Olasilik Dagilim Tablosu ve Beklenen Deger",
    "icerik": """OLASILIK:

1. OLASILIK DAGILIM TABLOSU:
   - Bir rasgele degiskenin alabilecegi tum degerleri ve olasiliklari gosterir.
   - Σ P(X = xᵢ) = 1 (tum olasiliklarin toplami 1'dir).
   - 0 ≤ P(X = xᵢ) ≤ 1 her deger icin.

2. BEKLENEN DEGER (ORTALAMA):
   - E(X) = μ = Σ xᵢ · P(X = xᵢ).
   - Uzun vadede rasgele degiskenin ortalama degeri.
   - E(aX + b) = a·E(X) + b (dogrusal ozellik).

3. VARYANS VE STANDART SAPMA:
   - Var(X) = E(X²) - [E(X)]² = Σ (xᵢ - μ)² · P(X = xᵢ).
   - σ = √Var(X) (standart sapma).
   - Var(aX + b) = a²·Var(X).

4. BINOM DAGILIMI:
   - n bagimsiz deneme, her denemede basari olasiligi p.
   - P(X = k) = C(n,k) · p^k · (1-p)^(n-k).
   - E(X) = n·p, Var(X) = n·p·(1-p).
   - Ornek: 10 kez yazi-tura, 3 kez yazi gelme olasiligi.

5. NORMAL DAGILIM (TANITIM):
   - Simetrik, can egrisine benzer grafik.
   - Ortalama μ, standart sapma σ ile belirlenir.
   - %68 veri μ ± σ, %95 veri μ ± 2σ, %99.7 veri μ ± 3σ araliginda.
   - Z-skoru: Z = (X - μ)/σ (standart normal dagilima donusum).

6. ISTATISTIKSEL UYGULAMALAR:
   - Regresyon analizi: En kucuk kareler yontemi ile dogru uydurma.
   - Korelasyon katsayisi: r (−1 ≤ r ≤ 1).
   - r > 0 pozitif iliski, r < 0 negatif iliski, r ≈ 0 iliski yok.
"""
},

}

def get_matematik12_reference(topic: str) -> list:
    """Verilen konuya en yakin matematik 12 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_12_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_matematik12_keys() -> list:
    """Tum matematik 12 referans anahtarlarini dondurur."""
    return list(MATEMATIK_12_REFERANS.keys())
