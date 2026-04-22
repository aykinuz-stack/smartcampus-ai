# -*- coding: utf-8 -*-
"""
9. Sinif Fizik dersi
MEB 2025 mufredatina uygun referans verileri.

Uniteler:
1. Fizik Bilimine Giris
2. Madde ve Ozellikleri
3. Kuvvet ve Hareket
4. Enerji
5. Isi ve Sicaklik
6. Elektrostatik
7. Elektrik Akimi
"""

FIZIK_9_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: FIZIK BILIMINE GIRIS
# ═══════════════════════════════════════════════════════════════

"FIZ.9.1.FIZIK_ALANLARI": {
    "unite": "Fizik Bilimine Giris",
    "baslik": "Fizigin Alt Alanlari ve Bilimsel Yontem",
    "icerik": """
FIZIGIN ALT ALANLARI VE BILIMSEL YONTEM:

1. FIZIK NEDIR:
   - Madde ve enerji arasindaki etkilesimleri inceleyen temel bilim dalidir
   - Dogadaki olaylari gozlem, deney ve matematiksel modellerle aciklar
   - Tum muhendislik ve teknoloji alanlarinin temelidir

2. FIZIGIN ALT ALANLARI:
   - Mekanik: Kuvvet, hareket ve denge (Newton yasalari)
   - Termodinamik: Isi, sicaklik ve enerji donusumleri
   - Optik: Isik ve goruntulenme olaylari
   - Elektrik ve Manyetizma: Elektrik akimi, manyetik alan
   - Atom Fizigi: Atom yapisi ve atom alti parcaciklar
   - Nukleer Fizik: Cekirdek yapisi, radyoaktivite
   - Kathal Fizigi: Maddenin kati hal ozellikleri
   - Akiskanlar Mekanigi: Sivi ve gazlarin davranislari

3. BILIMSEL YONTEM ADIMLARI:
   - 1) Gozlem: Olayin dikkatle incelenmesi
   - 2) Problem belirleme: Arastirilacak sorunun tanimlanmasi
   - 3) Hipotez kurma: Oneri niteliginde gecici aciklama
   - 4) Deney tasarlama ve uygulama: Kontrol ve deney gruplari
   - 5) Verileri toplama ve analiz etme: Olcum ve hesaplama
   - 6) Sonuc cikarma: Hipotezin dogrulanmasi veya curutulmesi
   - 7) Teori / Yasa: Dogrulanan hipotezler teoriye, evrensel iliskiler yasaya donusur

4. HIPOTEZ - TEORI - YASA FARKI:
   - Hipotez: Henuz test edilmemis oneri (dogrulanabilir veya curutulebilir)
   - Teori: Tekrarlanan deneylerle desteklenmis kapsamli aciklama
   - Yasa: Matematik ifadeyle belirtilen evrensel iliski (orn. F = ma)
"""
},

"FIZ.9.1.BUYUKLUKLER_BIRIMLER": {
    "unite": "Fizik Bilimine Giris",
    "baslik": "Fiziksel Buyuklukler, SI Birim Sistemi ve Birim Donusumleri",
    "icerik": """
FIZIKSEL BUYUKLUKLER VE SI BIRIM SISTEMI:

1. FIZIKSEL BUYUKLUK TURLERI:
   a) Temel buyuklukler: Baska buyukluklere bagli olmayan, dogrudan olculen
   b) Turetilmis buyuklukler: Temel buyukluklerden matematiksel islemlerle elde edilen

2. SI TEMEL BUYUKLUKLER VE BIRIMLERI (7 adet):
   ╔═══════════════════════╦══════════════╦═══════════╗
   ║ Buyukluk              ║ Birim        ║ Sembol    ║
   ╠═══════════════════════╬══════════════╬═══════════╣
   ║ Uzunluk               ║ metre        ║ m         ║
   ║ Kutle                 ║ kilogram     ║ kg        ║
   ║ Zaman                 ║ saniye       ║ s         ║
   ║ Elektrik akimi        ║ amper        ║ A         ║
   ║ Sicaklik              ║ kelvin       ║ K         ║
   ║ Madde miktari         ║ mol          ║ mol       ║
   ║ Isik siddeti          ║ kandela      ║ cd        ║
   ╚═══════════════════════╩══════════════╩═══════════╝

3. TURETILMIS BUYUKLUK ORNEKLERI:
   - Hiz: m/s (uzunluk / zaman)
   - Ivme: m/s² (hiz / zaman)
   - Kuvvet: N = kg·m/s² (kutle × ivme)
   - Enerji / Is: J = N·m = kg·m²/s²
   - Guc: W = J/s = kg·m²/s³
   - Basinc: Pa = N/m² = kg/(m·s²)
   - Ozkutle: kg/m³ (kutle / hacim)

4. SI ONEKLERI (KATLAR VE ASKATLAR):
   - Tera (T): 10¹²     | mili (m): 10⁻³
   - Giga (G): 10⁹      | mikro (μ): 10⁻⁶
   - Mega (M): 10⁶      | nano (n): 10⁻⁹
   - Kilo (k): 10³      | piko (p): 10⁻¹²
   - Hekto (h): 10²     | santi (c): 10⁻²
   - Deka (da): 10¹     | desi (d): 10⁻¹

5. SKALER VE VEKTOREL BUYUKLUKLER:
   - Skaler: Yalnizca buyuklugu olan (kutle, sicaklik, zaman, enerji, hiz buyuklugu)
   - Vektorel: Hem buyuklugu hem yonu olan (kuvvet, hiz, ivme, yer degistirme, agirlik)

6. OLCME VE HASSASIYET:
   - Her olcumde belirli bir belirsizlik (hata payi) vardir
   - Olcum aleti hassasiyeti: En kucuk olcebilecegi deger
   - Duyarlilik: Olcum aletinin ayirt edebilecegi en kucuk degisim
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: MADDE VE OZELLIKLERI
# ═══════════════════════════════════════════════════════════════

"FIZ.9.2.KUTLE_HACIM_OZKUTLE": {
    "unite": "Madde ve Ozellikleri",
    "baslik": "Kutle, Hacim ve Ozkutle",
    "icerik": """
KUTLE, HACIM VE OZKUTLE:

1. KUTLE (m):
   - Bir cismin icerdigi madde miktaridir
   - SI birimi: kilogram (kg)
   - Skaler buyukluktur (yonu yoktur)
   - Bulundugu yere gore DEGISMEZ (Ay'da da, Dunya'da da ayni)
   - Esit kollu terazi ile olculur
   - 1 kg = 1000 g, 1 ton = 1000 kg

2. HACIM (V):
   - Bir cismin uzayda kapladiği yer miktaridir
   - SI birimi: metrekup (m³)
   - Diger birimler: litre (L), mililitre (mL), santimetrekup (cm³)
   - 1 m³ = 1000 L, 1 L = 1000 mL = 1000 cm³
   - Duzensiz cisimlerin hacmi: Sivi tasirma yontemi (Arsimed)

3. OZKUTLE (d veya ρ):
   ┌─────────────────────────────────────┐
   │  d = m / V                         │
   │  d: ozkutle (kg/m³ veya g/cm³)     │
   │  m: kutle (kg veya g)              │
   │  V: hacim (m³ veya cm³)            │
   └─────────────────────────────────────┘
   - Birim hacimde bulunan kutle miktaridir
   - Maddeye ozgu bir ozelliktir (ayirt edici)
   - Ayni maddeden yapilmis farkli buyuklukteki cisimlerin ozkutlesi AYNIDIR
   - Sicaklik artinca ozkutle genellikle AZALIR (hacim artar, kutle ayni kalir)
   - Su istisnasi: Su 4°C'de en buyuk ozkutleye sahiptir

4. BAZI MADDELERIN OZKUTLELERI (g/cm³):
   - Altin: 19,3    | Demir: 7,87   | Aluminyum: 2,7
   - Su: 1,0        | Buz: 0,92     | Civa: 13,6
   - Bakir: 8,96    | Kursun: 11,3  | Tahta (ortalama): 0,5
"""
},

"FIZ.9.2.SICAKLIK_GENLESME": {
    "unite": "Madde ve Ozellikleri",
    "baslik": "Sicaklik, Genlesme ve Hal Degisimleri",
    "icerik": """
SICAKLIK, GENLESME VE HAL DEGISIMLERI:

1. SICAKLIK (T):
   - Maddeyi olusturan taneciklerin ortalama kinetik enerjisinin olcusudur
   - SI birimi: kelvin (K)
   - Diger birimler: santigrat (°C), fahrenheit (°F)
   - Donusumler:
     T(K) = T(°C) + 273
     T(°F) = 1,8 × T(°C) + 32
   - Termometre ile olculur

2. GENLESME:
   - Maddelerin isitildiginda boyutlarinin artmasidir
   a) Kati cisimlerde:
      - Boyca genlesme: ΔL = α · L₀ · ΔT
        (α: boyca genlesme katsayisi, 1/°C)
      - Yuzey genlesme: ΔA = 2α · A₀ · ΔT
      - Hacimce genlesme: ΔV = 3α · V₀ · ΔT
   b) Sivilarda:
      - Yalnizca hacimce genlesme gorulur
      - ΔV = β · V₀ · ΔT  (β: hacimce genlesme katsayisi)
   c) Gazlarda:
      - En fazla genlesme gazlarda gorulur
      - Tum gazlarin genlesme katsayisi aynidir (1/273)

3. HAL DEGISIMLERI:
   ┌──────────────────────────────────────────────┐
   │  KATI ⇌ SIVI ⇌ GAZ                         │
   │  Erime ──→     Buharlaşma ──→               │
   │  ←── Donma     ←── Yogusma                  │
   │  KATI ──→ GAZ: Subleşme (Surgulasma)        │
   │  GAZ ──→ KATI: Kiragılaşma                  │
   └──────────────────────────────────────────────┘
   - Hal degisimi sirasinda sicaklik SABIT kalir
   - Hal degisimi sirasinda verilen/alinan isi: Q = m · L
     (L: erime/buharlaşma isisi, J/kg)
   - Suyun erime noktasi: 0°C (1 atm)
   - Suyun kaynama noktasi: 100°C (1 atm)

4. ISI HESAPLAMA:
   ┌─────────────────────────────────────┐
   │  Q = m · c · ΔT                    │
   │  Q: isi miktari (J veya cal)       │
   │  m: kutle (kg veya g)              │
   │  c: oz isi (J/(kg·°C))            │
   │  ΔT: sicaklik degisimi (°C veya K) │
   └─────────────────────────────────────┘
   - Suyun oz isisi: c = 4186 J/(kg·°C) = 1 cal/(g·°C)
   - 1 cal = 4,186 J
   - Isi alışverişinde: Q(alinan) = Q(verilen) (isi korunumu)
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: KUVVET VE HAREKET
# ═══════════════════════════════════════════════════════════════

"FIZ.9.3.KUVVET_NEWTON": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Kuvvet Kavrami ve Newton'un Hareket Yasalari",
    "icerik": """
KUVVET VE NEWTON'UN HAREKET YASALARI:

1. KUVVET (F):
   - Cisimlerin hareketini veya seklini degistiren etkidir
   - SI birimi: newton (N), 1 N = 1 kg·m/s²
   - Vektorel buyukluktur (buyuklugu, yonu ve dogrusu vardir)
   - Temas kuvvetleri: surtunme, normal kuvvet, gerilme
   - Uzaktan etkili kuvvetler: kutle cekimi, elektrik, manyetik

2. NEWTON'UN 1. YASASI (EYLEMSIZLIK):
   - Bir cisme etki eden net kuvvet sifir ise:
     * Duruyorsa durmaya devam eder
     * Hareket ediyorsa sabit hizla dogrusal hareket eder
   - F(net) = 0 → a = 0 (ivme sifir, hiz sabit)
   - Eylemsizlik: Cismin mevcut hareket durumunu koruma egilimi
   - Kutle ne kadar buyukse eylemsizlik o kadar fazladir

3. NEWTON'UN 2. YASASI (IVME):
   ┌─────────────────────────────────────┐
   │  F = m · a                          │
   │  F: net kuvvet (N)                  │
   │  m: kutle (kg)                      │
   │  a: ivme (m/s²)                     │
   └─────────────────────────────────────┘
   - Net kuvvet ile ivme dogru orantili: F arttikca a artar
   - Kutle ile ivme ters orantili: m arttikca a azalir
   - Kuvvet uygulanma yonunde ivme olusturur
   - 1 N: 1 kg kutleli cisme 1 m/s² ivme kazandiran kuvvet

4. NEWTON'UN 3. YASASI (ETKI-TEPKI):
   - Her etkiye esit buyuklukte ve zit yonde bir tepki vardir
   - F(etki) = -F(tepki)
   - Etki ve tepki kuvvetleri FARKLI cisimlere etkir
   - Ornek: Yer cisimleri ceker (agirlik), cisimler de Yer'i ceker
"""
},

"FIZ.9.3.SURTUNME_AGIRLIK": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Surtunme Kuvveti, Agirlik ve Serbest Dusme",
    "icerik": """
SURTUNME KUVVETI, AGIRLIK VE SERBEST DUSME:

1. SURTUNME KUVVETI (f veya Fs):
   - Birbirine temas eden yuzeyler arasinda harekete karsi yonde olusan kuvvet
   ┌─────────────────────────────────────────┐
   │  f = μ · N                              │
   │  f: surtunme kuvveti (N)                │
   │  μ: surtunme katsayisi (birimsiz)       │
   │  N: normal kuvvet (N)                   │
   └─────────────────────────────────────────┘
   - Statik (duragan) surtunme: Cisim henuz hareket etmiyorken (μs)
   - Kinetik (kayma) surtunme: Cisim hareket halindeyken (μk)
   - Her zaman μs > μk (harekete baslamak devam ettirmekten zordur)
   - Surtunmeyi etkileyen faktorler: yuzey puruzlulugu, normal kuvvet
   - Surtunme temas yuzey ALANINA bagimli DEGILDIR

2. AGIRLIK (G veya W):
   ┌─────────────────────────────────────┐
   │  G = m · g                          │
   │  G: agirlik (N)                     │
   │  m: kutle (kg)                      │
   │  g: yercekimi ivmesi (m/s²)         │
   └─────────────────────────────────────┘
   - Dunya yuzeyinde: g ≈ 9,8 m/s² (sorularda genelde g = 10 m/s²)
   - Agirlik vektorel buyukluktur (yonu Dunya merkezine dogru)
   - Kutle degismez ama agirlik gezegene gore degisir
   - Ay'da: g(Ay) ≈ 1,6 m/s² (Dunya'nin yaklasik 1/6'si)
   - Dinamometre (yayli terazi) ile olculur

3. SERBEST DUSME:
   - Yalnizca yercekimi etkisinde (hava direnci ihmal) dusme hareketidir
   - Tum cisimler ayni ivmeyle duser (kutleden bagimsiz): a = g
   - Baslangic hizi sifir (v₀ = 0) olan serbest dusme:
     v = g · t                (anlik hiz)
     h = ½ · g · t²           (dusme yuksekligi)
     v² = 2 · g · h           (hiz-yukseklik iliskisi)
   - Galileo'nun Pisa Kulesi deneyi: Farkli kutleli cisimler ayni anda duser

4. EGIK DUZLEMDE HAREKET:
   - Agirlik bilesenleri:
     * Egim boyunca: G·sin(θ) (cismi kaydirir)
     * Egime dik: G·cos(θ) = N (normal kuvvet)
   - Surtunmesiz egik duzlemde ivme: a = g·sin(θ)
   - Surtunmeli egik duzlemde ivme: a = g·sin(θ) - μ·g·cos(θ)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: ENERJI
# ═══════════════════════════════════════════════════════════════

"FIZ.9.4.IS_VE_ENERJI": {
    "unite": "Enerji",
    "baslik": "Is, Kinetik Enerji ve Potansiyel Enerji",
    "icerik": """
IS, KINETIK ENERJI VE POTANSIYEL ENERJI:

1. IS (W):
   ┌─────────────────────────────────────────┐
   │  W = F · d · cos(θ)                     │
   │  W: is (J = N·m)                        │
   │  F: uygulanan kuvvet (N)                │
   │  d: yer degistirme (m)                  │
   │  θ: kuvvet ile yer degistirme arasi aci │
   └─────────────────────────────────────────┘
   - Kuvvet yonunde yer degistirme olursa is yapilir
   - θ = 0° → W = F·d (maksimum is, kuvvet hareket yonunde)
   - θ = 90° → W = 0 (kuvvet harekete dik ise is yapilmaz)
   - θ = 180° → W = -F·d (negatif is, kuvvet harekete zit)
   - Skaler buyukluktur
   - 1 J = 1 N·m = 1 kg·m²/s²

2. KINETIK ENERJI (Ek):
   ┌─────────────────────────────────────┐
   │  Ek = ½ · m · v²                   │
   │  Ek: kinetik enerji (J)            │
   │  m: kutle (kg)                      │
   │  v: hiz (m/s)                       │
   └─────────────────────────────────────┘
   - Hareket halindeki cisimlerin sahip oldugu enerji
   - Hiz 2 katina cikarsa kinetik enerji 4 katina cikar (v²)
   - Daima pozitiftir veya sifirdir (negatif olamaz)
   - Is-enerji teoremi: W(net) = ΔEk = Ek₂ - Ek₁

3. POTANSIYEL ENERJI (Ep):
   a) Yercekimi potansiyel enerjisi:
   ┌─────────────────────────────────────┐
   │  Ep = m · g · h                     │
   │  Ep: potansiyel enerji (J)          │
   │  m: kutle (kg)                      │
   │  g: yercekimi ivmesi (m/s²)         │
   │  h: yukseklik (m)                   │
   └─────────────────────────────────────┘
   - Referans noktasina gore belirlenir (h = 0 secimi onemli)
   - Yukseklik arttikca potansiyel enerji artar

   b) Esneklik potansiyel enerjisi:
   - Ep = ½ · k · x²  (k: yay sabiti N/m, x: uzama m)
"""
},

"FIZ.9.4.ENERJI_KORUNUMU_GUC": {
    "unite": "Enerji",
    "baslik": "Mekanik Enerji Korunumu, Guc ve Verim",
    "icerik": """
MEKANIK ENERJI KORUNUMU, GUC VE VERIM:

1. MEKANIK ENERJI (Em):
   ┌─────────────────────────────────────┐
   │  Em = Ek + Ep                       │
   │  Em = ½mv² + mgh                    │
   └─────────────────────────────────────┘
   - Kinetik ve potansiyel enerjinin toplamidir

2. MEKANIK ENERJI KORUNUMU:
   - Yalnizca muhafazakar kuvvetler (yercekimi) is yaparsa:
     Em(baslangic) = Em(son)
     ½mv₁² + mgh₁ = ½mv₂² + mgh₂
   - Surtunme YOKSA mekanik enerji korunur
   - Surtunme VARSA mekanik enerji AZALIR (isiya donusur)
     Em₁ = Em₂ + W(surtunme)

3. ENERJI DONUSUMLERI:
   - Yuksekten dusen cisim: Ep → Ek
   - Yukari atilan cisim: Ek → Ep
   - Surtunme: Ek → Isi enerjisi
   - Enerji yoktan var olmaz, var olan enerji yok olmaz (korunum)

4. GUC (P):
   ┌─────────────────────────────────────┐
   │  P = W / t                          │
   │  P: guc (W = watt)                  │
   │  W: yapilan is (J)                  │
   │  t: gecen sure (s)                  │
   └─────────────────────────────────────┘
   - Birim zamanda yapilan istir
   - 1 W = 1 J/s
   - 1 kW = 1000 W
   - 1 beygir gucu (HP) ≈ 746 W
   - Ayrica: P = F · v (kuvvet × hiz)

5. VERIM (η):
   ┌─────────────────────────────────────────┐
   │  η = (W_faydali / W_toplam) × 100      │
   │  η = (P_cikis / P_giris) × 100         │
   └─────────────────────────────────────────┘
   - Faydalı isin toplam ise orani (yuzde olarak)
   - Her zaman η ≤ %100 (ideal durumda %100)
   - Gercek makinelerde surtunme nedeniyle η < %100
   - Birimsizdir (yuzde ile ifade edilir)
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: ISI VE SICAKLIK
# ═══════════════════════════════════════════════════════════════

"FIZ.9.5.ISI_ALISVERISI": {
    "unite": "Isi ve Sicaklik",
    "baslik": "Isi Alisverisi ve Oz Isi Kapasitesi",
    "icerik": """
ISI ALISVERISI VE OZ ISI:

1. ISI (Q):
   - Sicaklik farkindan dolayi maddeler arasinda aktarilan enerji
   - SI birimi: joule (J)
   - Diger birim: kalori (cal), 1 cal = 4,186 J
   - Isi her zaman SICAK cisimden SOGUK cisme akar
   - Termal denge: Iki cisim ayni sicakliga ulastigi durum

2. OZ ISI (c):
   - 1 kg maddenin sicakligini 1°C artirmak icin gereken isi miktari
   - SI birimi: J/(kg·°C) veya J/(kg·K)
   - Maddeye ozgu bir ozelliktir (ayirt edici)
   - Suyun oz isisi: c = 4186 J/(kg·°C) → en buyuk oz isili yaygin sivi
   - Oz isisi buyuk olan madde:
     * Gec isinir, gec sogur
     * Cok isi depolar
     * Iyi isi yalitimi saglar

3. ISI HESAPLAMA:
   ┌─────────────────────────────────────┐
   │  Q = m · c · ΔT                    │
   │  Q: alinan/verilen isi (J)         │
   │  m: kutle (kg)                      │
   │  c: oz isi (J/(kg·°C))             │
   │  ΔT = T(son) - T(ilk) (°C)        │
   └─────────────────────────────────────┘
   - ΔT > 0: Madde isi ALMISTIR (sicaklik artmis)
   - ΔT < 0: Madde isi VERMISTIR (sicaklik azalmis)

4. ISI ALISVERISI DENKLEMI:
   - Yalitilmis sistemde: Q(alinan) = Q(verilen)
   - m₁·c₁·(Td - T₁) = m₂·c₂·(T₂ - Td)
   - Td: denge sicakligi (karisim sicakligi)
   - Suyun oz isisi buyuk oldugundan denge sicakligi suya daha yakindir

5. ISI KAPASITESI (C):
   - C = m · c  (birimi: J/°C)
   - Cismin sicakligini 1°C artirmak icin gereken toplam isi
   - Q = C · ΔT
"""
},

"FIZ.9.5.ISI_ILETIM_YOLLARI": {
    "unite": "Isi ve Sicaklik",
    "baslik": "Isi Iletim Yollari: Iletim, Konveksiyon, Isinim",
    "icerik": """
ISI ILETIM YOLLARI:

1. ILETIM (KONDUKSIYON):
   - Madde icinde taneciklerin birbirine enerji aktararak isi tasimasidir
   - Madde hareketi YOKTUR, enerji tanecikten tanecige aktarilir
   - Katilarda en etkili, sivilarda az, gazlarda en az
   - Metaller iyi iletkendir (serbest elektronlar sayesinde)
   - Tahta, cam yunu, kopuk: kotu iletken = iyi yalitkan
   ┌──────────────────────────────────────────┐
   │  Q/t = k · A · ΔT / L                   │
   │  k: isi iletim katsayisi (W/(m·K))      │
   │  A: kesit alani (m²)                     │
   │  ΔT: sicaklik farki (K)                  │
   │  L: kalinlik (m)                          │
   └──────────────────────────────────────────┘

2. KONVEKSIYON (TASINIM):
   - Akiskanlarda (sivi ve gaz) madde hareketi ile isi tasinmasi
   - Isınan akiskan genlesir → ozkutlesi azalir → yukari cikar
   - Soguyan akiskan yogunlasir → ozkutlesi artar → asagi iner
   - Dogal konveksiyon: sicaklik farkiyla olusan akim (ruzgar, deniz meltemi)
   - Zorlanmis konveksiyon: fan, pompa ile desteklenen akim (kalorifer)
   - Katilarda konveksiyon OLMAZ

3. ISINIM (RADYASYON):
   - Elektromanyetik dalgalar araciligiyla isi transferi
   - Madde ortamina IHTIYAC DUYMAZ (vakumda da gerceklesir)
   - Gunes enerjisi Dunya'ya isinim yoluyla ulasir
   - Koyu renkli yuzeyler: Iyi soğurur + iyi yayar
   - Acik (parlak) renkli yuzeyler: Iyi yansitur, az sogurur
   - Tum cisimler sicakliklariyla orantili isinim yayar

4. GUNLUK HAYAT ORNEKLERI:
   - Iletim: Metal kasik isitinca sapinin isinmasi
   - Konveksiyon: Oda isitici yakininda hava akimi
   - Isinim: Atesten gelen sicaklik hissi, Gunes isigi
   - Termos: Her uc yolu da minimize eder (vakum + parlak yuzey + mantar)
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: ELEKTROSTATIK
# ═══════════════════════════════════════════════════════════════

"FIZ.9.6.ELEKTRIK_YUKLERI": {
    "unite": "Elektrostatik",
    "baslik": "Elektrik Yukleri ve Coulomb Yasasi",
    "icerik": """
ELEKTRIK YUKLERI VE COULOMB YASASI:

1. ELEKTRIK YUKU (q):
   - Maddenin temel ozelliklerinden biridir
   - SI birimi: coulomb (C)
   - Iki tur yuk: Pozitif (+) ve Negatif (-)
   - Proton: +e = +1,6 × 10⁻¹⁹ C
   - Elektron: -e = -1,6 × 10⁻¹⁹ C
   - Notron: Yuksuz (0 C)
   - Ayni isaret yukler ITER, zit isaret yukler CEKER

2. YUKLENME YOLLARI:
   a) Surtunme ile yuklenme:
      - Iki cisim birbirine surtulunce elektron transferi olur
      - Elektron alan: (-) yuklenir, Elektron veren: (+) yuklenir
      - Ornek: Cam cubuk + ipek → cam (+), ipek (-)
   b) Dokunma ile yuklenme:
      - Yuklu cisim notr cisme dokundurulur
      - Yukler paylasılır, her ikisi de AYNI ISARET yuklenir
   c) Etki ile yuklenme (Elektrostatik induksiyon):
      - Yuklu cisim yaklastirılir (dokunmadan)
      - Yakin taraf zit yuk, uzak taraf ayni yuk birikir
      - Topraklama yapilirsa kalici yuklenme olur

3. COULOMB YASASI:
   ┌──────────────────────────────────────────┐
   │  F = k · |q₁ · q₂| / r²                │
   │  F: elektrik kuvveti (N)                 │
   │  k = 9 × 10⁹ N·m²/C²  (Coulomb sabiti) │
   │  q₁, q₂: yuklerin buyuklugu (C)         │
   │  r: yukler arasi uzaklik (m)             │
   └──────────────────────────────────────────┘
   - Yukler arttikca kuvvet ARTAR (dogru orantili)
   - Uzaklik arttikca kuvvet AZALIR (ters orantili, r²)
   - Uzaklik 2 katina cikarsa kuvvet 4'te 1'ine duser
   - Newton'un 3. yasasina uyar: F₁₂ = -F₂₁

4. ELEKTRIK ALAN (E):
   ┌─────────────────────────────────────┐
   │  E = F / q = k · Q / r²            │
   │  E: elektrik alan siddeti (N/C)    │
   │  F: elektrik kuvveti (N)            │
   │  q: test yuku (C)                   │
   │  Q: alan olusturan yuk (C)          │
   │  r: uzaklik (m)                     │
   └─────────────────────────────────────┘
   - Pozitif yukten disa, negatif yuke dogru yonelir
   - Alan cizgileri birbirini kesmez
   - Vektorel buyukluktur

5. ELEKTRIK POTANSIYELI (V):
   - V = k · Q / r  (birimi: volt, V = J/C)
   - Birim pozitif yuku sonsuzdan o noktaya getirmek icin gereken is
   - Potansiyel fark: ΔV = V₁ - V₂
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. UNITE: ELEKTRIK AKIMI
# ═══════════════════════════════════════════════════════════════

"FIZ.9.7.AKIM_GERILIM_DIRENC": {
    "unite": "Elektrik Akimi",
    "baslik": "Elektrik Akimi, Gerilim, Direnc ve Ohm Yasasi",
    "icerik": """
ELEKTRIK AKIMI, GERILIM, DIRENC VE OHM YASASI:

1. ELEKTRIK AKIMI (I):
   ┌─────────────────────────────────────┐
   │  I = Q / t                          │
   │  I: akim siddeti (A = amper)        │
   │  Q: gecen yuk miktari (C)           │
   │  t: gecen sure (s)                  │
   └─────────────────────────────────────┘
   - Iletkenin kesitinden birim zamanda gecen yuk miktari
   - 1 A = 1 C/s (saniyede 1 coulomb yuk gecisi)
   - Akim yonu: Pozitif (+) kutuptan negatif (-) kutuba (geleneksel)
   - Elektron akis yonu: Negatiften pozitife (akim yonunun tersi)
   - Amperemetre ile olculur (devreye SERI baglanir)

2. GERILIM (POTANSIYEL FARK) (V):
   - Devredeki iki nokta arasindaki potansiyel farki
   - SI birimi: volt (V)
   - 1 V = 1 J/C (1 coulomb yuku tasimak icin 1 joule enerji)
   - Voltmetre ile olculur (devreye PARALEL baglanir)
   - Pil/batarya gerilim kaynagi saglar (EMK: elektromotor kuvvet)

3. DIRENC (R):
   ┌─────────────────────────────────────────┐
   │  R = ρ · L / A                          │
   │  R: direnc (Ω = ohm)                    │
   │  ρ: ozdirenc (Ω·m)                      │
   │  L: iletken uzunlugu (m)                │
   │  A: kesit alani (m²)                     │
   └─────────────────────────────────────────┘
   - Iletkenin elektrik akimina gosterdigi zorluk
   - Uzunluk arttikca direnc ARTAR (dogru orantili)
   - Kesit alani arttikca direnc AZALIR (ters orantili)
   - Sicaklik arttikca metallerde direnc ARTAR
   - Iletken: Direnci dusuk (bakir, gumus, altin)
   - Yalitkan: Direnci cok yuksek (plastik, cam, kaucuk)

4. OHM YASASI:
   ┌─────────────────────────────────────┐
   │  V = I · R                          │
   │  V: gerilim (V)                     │
   │  I: akim (A)                        │
   │  R: direnc (Ω)                      │
   └─────────────────────────────────────┘
   - Sabit sicaklikta, iletkenin ucundaki gerilim akimla dogru orantilidir
   - V-I grafigi dogrusaldır (egim = R)
"""
},

"FIZ.9.7.SERI_PARALEL_DEVRE": {
    "unite": "Elektrik Akimi",
    "baslik": "Seri ve Paralel Baglanti, Devre Hesaplamalari",
    "icerik": """
SERI VE PARALEL BAGLANTI:

1. SERI BAGLANTI:
   ┌───────────────────────────────────────────────┐
   │  Akim: I = I₁ = I₂ = I₃  (AYNI)             │
   │  Gerilim: V = V₁ + V₂ + V₃  (TOPLAM)        │
   │  Direnc: Rt = R₁ + R₂ + R₃  (TOPLAM)        │
   └───────────────────────────────────────────────┘
   - Tek yol vardir, akim her yerde aynidir
   - Toplam direnc en buyuk direnctcen daha buyuktur
   - Bir eleman bozulursa tum devre kesilir
   - Gerilim direncle orantili dagilir: V₁/V₂ = R₁/R₂

2. PARALEL BAGLANTI:
   ┌───────────────────────────────────────────────┐
   │  Gerilim: V = V₁ = V₂ = V₃  (AYNI)          │
   │  Akim: I = I₁ + I₂ + I₃  (TOPLAM)           │
   │  Direnc: 1/Rt = 1/R₁ + 1/R₂ + 1/R₃          │
   └───────────────────────────────────────────────┘
   - Her eleman ayni gerilimi gorur
   - Toplam direnc en kucuk direnctcen daha kucuktur
   - Bir eleman bozulursa digerler calismaya devam eder
   - Akim direncle ters orantili dagilir: I₁/I₂ = R₂/R₁
   - Iki direnc icin: Rt = (R₁ · R₂) / (R₁ + R₂)

3. ELEKTRIKSEL GUC VE ENERJI:
   ┌─────────────────────────────────────┐
   │  P = V · I                          │
   │  P = I² · R                         │
   │  P = V² / R                         │
   │  P: elektriksel guc (W)             │
   └─────────────────────────────────────┘
   - Elektriksel enerji: E = P · t = V · I · t
   - SI birimi: joule (J)
   - Pratik birim: kilowatt-saat (kWh)
   - 1 kWh = 3,6 × 10⁶ J = 3600 kJ
   - Elektrik faturasi kWh uzerinden hesaplanir

4. DEVRE ELEMANLARI VE SEMBOLLERI:
   - Pil: Gerilim kaynagi (+/- kutuplar)
   - Anahtar: Devreyi acar/kapar
   - Ampul/Lamba: Elektrik enerjisini isik + isiya donusturur
   - Direnc: Akimi sinirlar
   - Amperemetre (A): Seri baglanir, ic direnci cok kucuk
   - Voltmetre (V): Paralel baglanir, ic direnci cok buyuk
   - Sigorta: Asiri akimda devreyi keser (guvenlik)

5. KIRCHHOFF KURALLARI (giris seviyesi):
   - Dugum kurali: Bir dugume giren akimlarin toplami = cikan akimlarin toplami
   - Cevre kurali: Kapali bir cevredeki gerilim dusumlerinin toplami = EMK toplami
"""
},

}  # FIZIK_9_REFERANS sonu


# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_fizik9_reference(topic: str) -> dict:
    """
    Belirli bir konu anahtarina gore fizik 9 referans verisini dondurur.

    Parametre:
        topic (str): Konu anahtari (orn. "FIZ.9.3.KUVVET_NEWTON")

    Donus:
        dict: Konu icerigi {"unite", "baslik", "icerik"} veya None
    """
    return FIZIK_9_REFERANS.get(topic, None)


def get_all_fizik9_keys() -> list:
    """
    Tum fizik 9 referans konu anahtarlarini liste olarak dondurur.

    Donus:
        list: Konu anahtarlari listesi
    """
    return list(FIZIK_9_REFERANS.keys())


# ═══════════════════════════════════════════════════════════════
# MODUL TESTI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Fizik 9 Referans: {len(FIZIK_9_REFERANS)} konu yuklendi.")
    print("Anahtarlar:")
    for key in get_all_fizik9_keys():
        ref = get_fizik9_reference(key)
        print(f"  {key} -> {ref['unite']} / {ref['baslik']}")
