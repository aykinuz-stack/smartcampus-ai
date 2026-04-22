# -*- coding: utf-8 -*-
"""
10. Sinif Fizik dersi
MEB 2025 mufredatina uygun referans verileri.

Uniteler:
1. Elektrik ve Manyetizma
2. Basinc ve Kaldirma Kuvveti
3. Dalgalar
4. Optik
"""

FIZIK_10_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: ELEKTRIK VE MANYETIZMA
# ═══════════════════════════════════════════════════════════════

"FIZ.10.1.ELEKTRIK_YUKLER": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Elektrik Yukleri ve Elektrikleme",
    "icerik": """
ELEKTRIK YUKLERI:
- Madde atomlardan olusur. Atomda proton (+), notron (notr) ve elektron (-) bulunur.
- Bir cisim esit sayida proton ve elektrona sahipse notr (yuksuzdur).
- Cisim elektron kaybederse pozitif, elektron kazanirsa negatif yuklenir.
- Elektrik yuklerinin birimi Coulomb (C) dir. Bir elektronun yuku: e = 1,6 × 10⁻¹⁹ C.
- Yuk kuantalanmasi: Bir cismin yuku q = n × e seklinde ifade edilir (n tam sayi).
- Ayni tur yukler birbirini iter, zit tur yukler birbirini ceker.

ELEKTRIKLEME YONTEMLERI:
1. Surtunme ile elektrikleme:
   - Iki notr cisim birbirine surtulunce elektron aktarimi olur.
   - Bir cisim (+), digeri (-) yuklenir. Ornek: cam cubugu ipek kumasa surtme.
   - Surtunme sirasi (triboelektrik seri): Kedi derisi, cam, yun, ipek, pamuk, ebonit, plastik.

2. Dokunma ile elektrikleme:
   - Yuklu cisim notr cisme dokundurulunca yuk paylasimi olur.
   - Iki cisim de ayni isarette yuklenir.
   - Iletken kurelerde yuk, yaricaplariyla orantili dagilir: q₁/q₂ = r₁/r₂.

3. Etki ile elektrikleme (Elektrostatik induksiyon):
   - Yuklu cisim notr iletkene yaklastirildiginda yuk ayrisimi olur.
   - Cisim yakin yuzde zit, uzak yuzde ayni isarette yuklenir.
   - Topraklama yapilirsa cisim kalici olarak yuklenir.

ELEKTROSKOP:
- Elektrik yukunu tespit eden arac. Metal cubuk ve ince yapraktan olusur.
- Yuklu cisim yaklastirildiginda yapraklar acilir.
- Elektroskop ile yuklerin isareti ve buyuklugu karsilastirilabilir.
"""
},

"FIZ.10.1.COULOMB": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Coulomb Kanunu ve Elektrik Alani",
    "icerik": """
COULOMB KANUNU:
- Iki noktasal yuk arasindaki elektriksel kuvveti ifade eder.
- F = k × |q₁ × q₂| / r²
  k = 9 × 10⁹ N·m²/C² (Coulomb sabiti)
  q₁, q₂ = yuklerin buyuklugu (C)
  r = yukler arasi uzaklik (m)
- Kuvvet, yuklerle dogru, uzakligin karesiyle ters orantilidir.
- Ayni isaret yukler: itme kuvveti; zit isaret yukler: cekme kuvveti.
- Ortam degisirse k sabiti degisir (k_ortam = k / ε_r, ε_r: bagil gecirgenlik).

ELEKTRIK ALAN:
- Yuklu cismin cevresinde olusturdugu etkiye elektrik alan denir.
- E = F / q₀ = k × Q / r² (birim: N/C veya V/m)
  Q: alan olusturan yuk, r: yuke olan uzaklik, q₀: test yuku
- Elektrik alan cizgileri (+) yukten cikar, (-) yuke girer.
- Alan cizgileri birbirini kesmez.
- Pozitif yukun alani disariya dogru, negatif yukun alani iceridogru yonelir.
- Duzgun elektrik alan: Paralel plakalar arasinda olusur, alan cizgileri paralel ve esit araliklidir.

ELEKTRIK ALAN KUVVET ILISKISI:
- Pozitif yuk, elektrik alan yonunde kuvvet hisseder.
- Negatif yuk, elektrik alanin ters yonunde kuvvet hisseder.
- F = q × E
- Superposition ilkesi: Birden fazla yukun olusturdugu alan, her yukun alaninin vektorel toplamidir.
"""
},

"FIZ.10.1.ELEKTRIK_POTANSIYEL": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Elektrik Potansiyeli ve Potansiyel Enerji",
    "icerik": """
ELEKTRIK POTANSIYEL ENERJI:
- Yuklu cismin elektrik alaninda bulunmasindan kaynaklanan enerjidir.
- U = k × q₁ × q₂ / r (birim: Joule)
- Ayni isaret yukler: pozitif potansiyel enerji (itme).
- Zit isaret yukler: negatif potansiyel enerji (cekme).

ELEKTRIK POTANSIYEL:
- Birim pozitif yukun potansiyel enerjisidir.
- V = U / q = k × Q / r (birim: Volt = J/C)
- Pozitif yukun potansiyeli pozitif, negatif yukun potansiyeli negatiftir.
- Esit potansiyel yuzeyler: Uzerindeki her noktada potansiyelin ayni oldugu yuzeyler.
  Noktasal yuk icin kuresel yuzeylerdir.

POTANSIYEL FARKI (GERILIM):
- Iki nokta arasindaki potansiyel farkidir: ΔV = V_A - V_B.
- Elektrik alaninda yuk tasimak icin is yapilir: W = q × ΔV.
- Pozitif yukler yuksek potansiyelden alcak potansiyele dogru hareket eder.
- 1 elektronvolt (eV) = 1,6 × 10⁻¹⁹ J (bir elektronun 1 V potansiyel farkinda kazandigi enerji).

KONDANSATOR (SIGAC):
- Elektrik yukunu depolayan aygittir.
- Duzlem kondansator: Iki paralel iletken plakadan olusur.
- Siginim: C = Q / V (birim: Farad, F)
- Duzlem kondansator sigasi: C = ε₀ × ε_r × A / d
  (ε₀ = 8,85×10⁻¹² F/m, A: plaka alani, d: plakalar arasi uzaklik)
- Kondansatorde depolanan enerji: U = ½ × C × V² = ½ × Q × V = Q²/(2C)
"""
},

"FIZ.10.1.ELEKTRIK_AKIM": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Elektrik Akimi ve Devreler",
    "icerik": """
ELEKTRIK AKIMI:
- Yuklu parcaciklarin duzenli hareketidir.
- I = Q / t (birim: Amper, A = C/s)
- Akim yonu, konvansiyonel olarak (+) kutuptan (-) kutba dogrudur.
- Elektron akis yonu, akim yonunun tersidir.

DIRENC VE OHM KANUNU:
- Direnc: Iletkenin akima gosterdigi zorluktur. Birim: Ohm (Ω).
- Ohm Kanunu: V = I × R
  V: gerilim (Volt), I: akim (Amper), R: direnc (Ohm)
- Iletkenin direnci: R = ρ × L / A
  ρ: ozdirenc (Ω·m), L: uzunluk (m), A: kesit alani (m²)
- Sicaklik artinca metallerde direnc artar, yarililetkenlerde azalir.

SERI VE PARALEL BAGLANMA:
Seri baglanti:
- Akim her direncte aynidir: I = I₁ = I₂ = I₃
- Toplam gerilim: V = V₁ + V₂ + V₃
- Toplam direnc: R_top = R₁ + R₂ + R₃
- Bir eleman bozulursa devre acilir.

Paralel baglanti:
- Gerilim her direncte aynidir: V = V₁ = V₂ = V₃
- Toplam akim: I = I₁ + I₂ + I₃
- Toplam direnc: 1/R_top = 1/R₁ + 1/R₂ + 1/R₃
- Bir eleman bozulursa digerleri calismaya devam eder.

ELEKTRIK ENERJISI VE GUCU:
- Guc: P = V × I = I² × R = V² / R (birim: Watt, W)
- Enerji: E = P × t (birim: Joule; elektrik sayacinda kWh kullanilir)
- 1 kWh = 3,6 × 10⁶ J
"""
},

"FIZ.10.1.MANYETIZMA": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Manyetizma ve Elektromanyetik Induksiyon",
    "icerik": """
MIKNATISLAR VE MANYETIK ALAN:
- Her miknatista kuzey (N) ve guney (S) kutbu vardir.
- Ayni kutuplar iter, zit kutuplar ceker.
- Manyetik alan cizgileri N kutbundan cikar, S kutbuna girer.
- Dunya buyuk bir miknatis gibi davranir. Cografi kuzey kutbu yakininda manyetik guney kutbu bulunur.
- Bir miknatis ikiye bolununce her parca yeni bir miknatis olur (tek kutup olusturulamaz).

AKIMIN MANYETIK ETKISI:
- Elektrik akimi gecen iletkenin cevresinde manyetik alan olusur (Oersted deneyi).
- Duz iletken: Manyetik alan cizgileri iletkeni saran dairelerdir.
  Yon: Sag el kurali - bas parmak akim yonu, kapanan parmaklar alan yonu.
- Dairesel iletken (bobin): Ic kisimda duzgun manyetik alan olusur.
- Selenoid (uzun bobin): Icinde duzgun manyetik alan olusur, miknatis gibi davranir.
  B = μ₀ × n × I (n: birim uzunluktaki sarim sayisi, I: akim)

ELEKTROMANYETIK INDUKSIYON (FARADAY KANUNU):
- Manyetik aki degisimi iletken devrede EMK (gerilim) olusturur.
- Faraday kanunu: EMK = -ΔΦ / Δt (Φ: manyetik aki = B × A × cos θ)
- Lenz kanunu: Induksiyon akiminin yonu, aki degisimini engellemeye yoneliktir.
- Uygulamalar: Jenerator (mekanik enerji → elektrik enerjisi), transformator.

TRANSFORMATOR:
- AC gerilimi yukseltmek veya dusurmeye yarar.
- V₁/V₂ = N₁/N₂ (N: sarim sayisi)
- Ideal transformatorde: V₁ × I₁ = V₂ × I₂ (guc korunumu)
- Yukseltec trafo: N₂ > N₁; dusuruc trafo: N₂ < N₁
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: BASINC VE KALDIRMA KUVVETI
# ═══════════════════════════════════════════════════════════════

"FIZ.10.2.KATI_BASINC": {
    "unite": "Basinc ve Kaldirma Kuvveti",
    "baslik": "Kati Basinc",
    "icerik": """
BASINC KAVRAMI:
- Birim yuzey alanina dik olarak uygulanan kuvvettir.
- P = F / A (birim: Pascal, Pa = N/m²)
- Diger birimler: 1 atm = 101325 Pa = 760 mmHg = 76 cmHg = 1013,25 hPa
- Basinc skaler bir buyukluktur, yonu yoktur.

KATI BASINC:
- Kati cisimlerin yuzey uzerine uyguladigi basinctir.
- P = F_dik / A (F_dik: yuzeve dik kuvvet bileseni)
- Cismin agirligi: F = m × g (g = 10 m/s²)
- Kati basinc artirmak icin: Kuvvet arttirilir veya temas alani kuculturur.
  Ornek: Bicak ucu keskin yapilir (alan azalir, basinc artar).
- Kati basinc azaltmak icin: Temas alani arttirilir.
  Ornek: Paletli araclar (temas alani buyuk, basinc az).

KATI CISIM BASINCI PROBLEMLERI:
- Dikdortgen prizma: Farkli yuzeyler uzerine konuldugunda farkli basinc uygular.
  En kucuk yuzeye oturursa en buyuk basinc, en buyuk yuzeye oturursa en kucuk basinc.
- Kup: Her yuze oturdugunda basinc aynidir (tum yuzler esit).
- Ust uste konan cisimler: Alt cismin zemine uyguladigi basinc hesaplanirken
  toplam agirlik (ust + alt) ve alt cismin taban alani kullanilir.
"""
},

"FIZ.10.2.SIVI_BASINC": {
    "unite": "Basinc ve Kaldirma Kuvveti",
    "baslik": "Sivi Basinci ve Pascal Prensibi",
    "icerik": """
SIVI BASINCI:
- Sivi icindeki bir noktadaki basinc derinlikle dogru orantilidir.
- P_sivi = d × g × h
  d: sivinin yogunlugu (kg/m³), g: yercekimi ivmesi, h: derinlik (m)
- Sivi basinci yalnizca derinlige ve sivi yogunluguna bagli, kap seklinden bagimsizdir.
- Ayni derinlikteki tum noktalar ayni basinca sahiptir.
- Sivilar her yone esit basinc uygular (Pascal ilkesi).
- Bir noktadaki toplam (mutlak) basinc: P_toplam = P_atmosfer + d × g × h

PASCAL PRENSIBI:
- Kapali bir kaptaki sivinin bir noktasina uygulanan basinc,
  sivinin her noktasina ayni buyuklukte iletilir.
- Hidrolik sistemlerin temelidir.
- Hidrolik pres: F₁/A₁ = F₂/A₂
  Kucuk pistona uygulanan kuvvet, buyuk pistonda buyutulmus olarak ortaya cikar.
- Uygulamalar: Hidrolik fren, hidrolik kriko, dis sandalyesi.

BILESIK KAPLAR:
- Birbirine bagli kaplar sistemidir.
- Ayni sivi kullanilirsa: Tum kollarda sivi ayni seviyeye yukselir.
- Farkli sivilar kullanilirsa: Yogunlugu buyuk olan sivi daha az yukselir.
  d₁ × h₁ = d₂ × h₂ (dengedeki sivi sutunlari)
"""
},

"FIZ.10.2.GAZ_BASINC": {
    "unite": "Basinc ve Kaldirma Kuvveti",
    "baslik": "Gaz Basinci ve Atmosfer Basinci",
    "icerik": """
ATMOSFER BASINCI:
- Havanin agirligindan kaynaklanan basinca atmosfer basinci denir.
- Deniz seviyesinde: 1 atm = 760 mmHg = 101325 Pa.
- Yukseklik arttikca atmosfer basinci azalir (hava tabakasi incelir).
- Torricelli deneyi: Civayla dolu tupun tersine cevrilerek atmosfer basinci olculur.

ACIK HAVA BASINCI OLCUMU:
- Barometre: Atmosfer basincini olcer.
- Manometre: Kapali kaptaki gaz basincini olcer.
  - Acik uclu manometre: P_gaz = P_atm ± d × g × h
  - Kapali uclu manometre: P_gaz = d_civa × g × h

GAZ BASINCI:
- Gaz molekullerinin kap cidarina carpmasindan olusur.
- Gaz basincini etkileyen faktorler:
  1. Sicaklik: Artarsa basinc artar (hacim sabit).
  2. Hacim: Azalirsa basinc artar (sicaklik sabit) - Boyle-Mariotte.
  3. Mol sayisi: Artarsa basinc artar.

GAZ KANUNLARI (Giris):
- Boyle-Mariotte: P₁V₁ = P₂V₂ (sabit sicaklik)
- Charles: V₁/T₁ = V₂/T₂ (sabit basinc)
- Gay-Lussac: P₁/T₁ = P₂/T₂ (sabit hacim)
- Birlesik gaz kanunu: P₁V₁/T₁ = P₂V₂/T₂
- Ideal gaz denklemi: PV = nRT (R = 8,314 J/mol·K)
"""
},

"FIZ.10.2.KALDIRMA": {
    "unite": "Basinc ve Kaldirma Kuvveti",
    "baslik": "Kaldirma Kuvveti ve Archimedes Prensibi",
    "icerik": """
ARCHIMEDES PRENSIBI:
- Bir siviya batirilan cisme, cismin yerinden oldurdugu sivi agirligina esit
  buyuklukte yukari yonde kaldirma kuvveti uygulanir.
- F_kaldirma = d_sivi × V_batan × g
  d_sivi: sivinin yogunlugu, V_batan: cismin siviya batan hacmi

CISMIN SIVIDAKI DURUMU:
1. Batar: d_cisim > d_sivi → F_kaldirma < G (agirlik) → cisim dibe coker.
2. Askida kalir: d_cisim = d_sivi → F_kaldirma = G → cisim sivi icinde dengededir.
3. Yuzer: d_cisim < d_sivi → cisim sivi yuzeyinde dengeye gelir.
   Yuzme kosulu: F_kaldirma = G → d_sivi × V_batan × g = d_cisim × V_cisim × g

YUZME VE BATMA ORANLARI:
- Yuzen cisimde: V_batan / V_cisim = d_cisim / d_sivi
- Cismin yogunlugu sivinin yogunlugunun %80'i ise cismin %80'i batar, %20'si suyun disinda kalir.
- Buz suda yuzer: d_buz = 0,92 g/cm³ < d_su = 1 g/cm³. Buzun %92'si suyun icinde, %8'i disinda.

KALDIRMA KUVVETINI ETKILEYEN FAKTORLER:
- Sivinin yogunlugu (arttikca kaldirma kuvveti artar)
- Cismin batan hacmi (arttikca kaldirma kuvveti artar)
- Yercekimi ivmesi (arttikca kaldirma kuvveti artar)
- Cismin seklinden, agirligindan, derinliginden BAGIMLI DEGILDIR (ayni hacim icin).
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: DALGALAR
# ═══════════════════════════════════════════════════════════════

"FIZ.10.3.DALGA_TEMEL": {
    "unite": "Dalgalar",
    "baslik": "Dalga Temelleri ve Dalga Turleri",
    "icerik": """
DALGA KAVRAMI:
- Titresim hareketinin ortam boyunca yayilmasina dalga denir.
- Dalga enerji tasir ancak madde tasimaz.
- Dalgalarin olusabilmesi icin bir titresim kaynagi ve yayilma ortami gereklidir
  (elektromanyetik dalgalar haric - bos uzayda da yayilir).

DALGA TURLERI:
1. Yayilma yonune gore:
   a) Enine dalga: Titresim yonu yayilma yonune diktir.
      Ornekler: Su dalgasi, isik, ip dalgasi.
      Tepe ve cukurlardan olusur.
   b) Boyuna dalga: Titresim yonu yayilma yonuyle aynidir.
      Ornekler: Ses dalgasi, yay dalgasi.
      Sikisma ve genlesmelerden olusur.

2. Ortam gereksinimine gore:
   a) Mekanik dalgalar: Yayilmak icin maddesel ortam gerektirir.
      Ornekler: Ses, su dalgasi, deprem dalgasi.
   b) Elektromanyetik dalgalar: Ortam gerekmez, bos uzayda yayilir.
      Ornekler: Isik, radyo dalgasi, X isini, mikro dalga.

DALGA BUYUKLUKLERI:
- Genlik (A): Denge noktasindan maksimum uzaklik. Enerjiyle iliskilidir.
- Dalga boyu (lambda): Art arda iki tepe (veya cukur) arasi mesafe.
- Frekans (f): Birim zamandaki titresim sayisi (birim: Hz = 1/s).
- Periyot (T): Bir tam titresimin suresi (T = 1/f).
- Dalga hizi: v = lambda × f = lambda / T
- Dalga hizi ortamin ozelligine baglidir, kaynaga baglimsizdir.
"""
},

"FIZ.10.3.SES_DALGALARI": {
    "unite": "Dalgalar",
    "baslik": "Ses Dalgalari",
    "icerik": """
SES DALGASI OZELLIKLERI:
- Ses boyuna bir mekanik dalgadir; yayilmak icin ortam gerekir.
- Ses bos uzayda (vakumda) yayilamaz.
- Sesin yayilma hizi ortamin cinsine ve sicakligina bagli:
  Katilarda en hizli, sivilarda orta, gazlarda en yavas.
  Havada (20°C): v = 340 m/s
  Suda: v = 1500 m/s
  Celikte: v = 5000 m/s
- Sicaklik artinca sesin havadaki hizi artar.

SESIN OZELLIKLERI:
1. Siddet (Ses Siddeti):
   - Sesin guclu veya zayif duyulmasidir.
   - Genlikle dogru orantilidir (genlik artarsa siddet artar).
   - Birim: desibel (dB). Normal konusma = 60 dB, agri esigi = 130 dB.

2. Yukseklik (Perde):
   - Sesin ince veya kalin olmasi.
   - Frekansla dogru orantili: Yuksek frekans → ince ses, dusuk frekans → kalin ses.
   - Kadin/cocuk sesi ince (yuksek frekans), erkek sesi kalindir (dusuk frekans).

3. Tini (Renk):
   - Farkli kaynaklardan cikan seslerin ayirt edilmesi.
   - Harmonikler (ust perdeler) belirler. Her enstrumanin tinisi farklidir.

ISITMA ESIKLERI:
- Insan kulagi 20 Hz - 20.000 Hz (20 kHz) frekans araligini duyar.
- 20 Hz alti: infrasound (filler duyar).
- 20 kHz ustu: ultrasound (yarasalar, yunuslar kullanir).
- Ultrasonun uygulamalari: Tibbi goruntuleme, sonar, sanayi temizligi.

YANKI (EKO):
- Sesin bir engele carpip geri donmesiyle duyulan tekrardir.
- Yankinin ayirt edilmesi icin en az 17 m mesafe (ses 34 m gidip donmeli, yaklasik 0,1 s).
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: OPTIK
# ═══════════════════════════════════════════════════════════════

"FIZ.10.4.ISIK_TEMEL": {
    "unite": "Optik",
    "baslik": "Isigin Temelleri ve Yansima",
    "icerik": """
ISIK KAVRAMI:
- Isik elektromanyetik bir dalgadir; bos uzayda yayilabilir.
- Isik hizi (vakumda): c = 3 × 10⁸ m/s (evrendeki en yuksek hiz).
- Isik hem dalga hem parcacik ozelligi gosterir (dalga-parcacik ikiligi).
- Gorunur isik dalga boyu: yaklasik 400 nm (mor) - 700 nm (kirmizi).

ISIK KAYNAKLARI:
- Dogal kaynaklar: Gunes, yildizlar, atesbocegi.
- Yapay kaynaklar: Ampul, LED, lazer, mum.
- Isik kaynagi kendi isigini yayan cisimdir; aydinlanan cisimler isik kaynagi degildir.

ISIGIN DOGRUSAL YAYILMASI:
- Isik homojen ortamda dogru cizgiler boyunca yayilir.
- Golge olusumu isigin dogrusal yayilmasinin kanitidir.
- Tam golge (golge): Isik ulasamayan bolge.
- Yarigolge (penumbra): Kismi isik alan bolge (buyuk kaynaklarda olusur).
- Gunes tutulmasi: Ay, Gunes ile Dunya arasina girdiginde.
- Ay tutulmasi: Dunya, Gunes ile Ay arasina girdiginde.

ISIGIN YANSIMASI:
- Isik, bir yuzeyden carptiktan sonra geri donmesidir.
- Yansima kanunlari:
  1. Gelis acisi = Yansima acisi (teta_i = teta_r)
  2. Gelen isik, yansıyan isik ve normal ayni duzlemdedir.
- Duzgun yansima: Duz yuzeylerden (ayna); goruntu olusur.
- Daginik (difuz) yansima: Puruzlu yuzeylerden; goruntu olusmaz ama cisim gorunur olur.
"""
},

"FIZ.10.4.AYNALAR": {
    "unite": "Optik",
    "baslik": "Duz Ayna ve Kuresel Aynalar",
    "icerik": """
DUZ AYNA:
- Goruntu sanaltir (aynanin arkasinda olusur), diktir ve cisimle ayni buyukluktedir.
- Cisim-ayna uzakligi = Goruntu-ayna uzakligi.
- Goruntu simetridir: Sag-sol degisimi olur (lateral inversiyon).
- Iki duz ayna arasindaki goruntu sayisi: n = (360/alfa) - 1 (alfa: aynalar arasi aci).

KURESEL AYNALAR:
Temel kavramlar:
- Merkez (C): Aynanin kuresel yuzeyinin merkezi.
- Odak noktasi (F): Eksene paralel isinlarin yansidiktan sonra toplandigi nokta.
  f = R/2 (f: odak uzakligi, R: egrilik yaricapi)
- Tepe noktasi (O): Aynanin optik eksen uzerindeki noktasi.

Cukur (Icbukey) Ayna:
- Yansitici yuzey icbukeydir.
- Paralel isinlar odakta toplanir (yakinlasmaci).
- Goruntu durumu cismin konumuna bagli:
  C otesinde: Gercek, ters, kucultulmus
  C'de: Gercek, ters, ayni buyuklukte
  F-C arasi: Gercek, ters, buyutulmus
  F'de: Goruntu sonsuzdadir
  F onunde: Sanal, dik, buyutulmus
- Kullanim: Far, reflektorler, gunes ocagi, tiras aynasi.

Tumsek (Disbukey) Ayna:
- Yansitici yuzey disbukeydir.
- Paralel isinlar yansidiktan sonra iraksaklasir; uzantilari odakta birlesir.
- Her durumda: Sanal, dik ve kucultulmus goruntu olusturur.
- Genis gorus acisi saglar.
- Kullanim: Arac yan aynalari, market guvenlik aynalari.

AYNA FORMULU:
- 1/f = 1/d_o + 1/d_i
  d_o: cisim uzakligi, d_i: goruntu uzakligi
- Buyutme: m = -d_i / d_o = h_i / h_o
"""
},

"FIZ.10.4.ISIK_KIRILMA": {
    "unite": "Optik",
    "baslik": "Isigin Kirilmasi ve Mercekler",
    "icerik": """
ISIGIN KIRILMASI:
- Isik farkli optik yogunluktaki ortama gecerken yon degistirmesidir.
- Snell kanunu: n₁ × sin teta₁ = n₂ × sin teta₂
  n: kirilma indisi, teta: acilar (normalle yapilan)
- Kirilma indisi: n = c / v (c: vakumdaki isik hizi, v: ortamdaki hiz).
- Isik seyrek ortamdan yogun ortama gecerken normale yaklasir (yavaslar).
- Isik yogun ortamdan seyrek ortama gecerken normalden uzaklasir (hizlanir).

TAM YANSIMA (IC YANSIMA):
- Isik yogun ortamdan seyrek ortama gecerken kirilma acisi 90 derece olursa:
  bu aciya sinir (kritik) aci denir: sin teta_c = n₂/n₁
- Gelis acisi sinir aciyi asarsa isik kirilmaz, tamamen yansir.
- Uygulamalar: Fiber optik kablolar, elmas parlakligi, prizmalar.

MERCEKLER:
Ince kenarli (Tumsek/Yakinsak) Mercek:
- Kenarlari ince, ortasi kalindir.
- Paralel isinlari odakta toplar.
- Gercek ve sanal goruntu olusturabilir.
- Kullanim: Buyutec, fotograf makinesi, goz mercegi.

Kalin kenarli (Cukur/Iraksak) Mercek:
- Kenarlari kalin, ortasi incedir.
- Paralel isinlari iraksaklastirir.
- Her zaman sanal, dik, kucultulmus goruntu olusturur.
- Kullanim: Miyop gozlukleri.

MERCEK FORMULU:
- 1/f = 1/d_o + 1/d_i
- Mercek gucu: D = 1/f (birim: diyoptri, m⁻¹)
- Yakinsak mercegin odak uzakligi pozitif, iraksak mercegin negatiftir.
"""
},

}


def get_fizik10_reference(topic: str) -> list:
    """Verilen konuya en uygun fizik 10 referans kayitlarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in FIZIK_10_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_fizik10_keys() -> list:
    """Tum fizik 10 referans anahtarlarini dondurur."""
    return list(FIZIK_10_REFERANS.keys())
