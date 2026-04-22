# -*- coding: utf-8 -*-
"""
12. Sinif Kimya dersi - MEB 2025 mufredatina uygun referans verileri.
Ogrenme alanlari:
1. Kimya ve Elektrik
2. Karbon Kimyasi (Organik)
3. Enerji Kaynaklari ve Yakitlar
"""

KIMYA_12_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: KIMYA VE ELEKTRIK
# ═══════════════════════════════════════════════════════════════

"KIM.12.1.ELEKTROKIMYA_GIRIS": {
    "unite": "Kimya ve Elektrik",
    "baslik": "Elektrokimya Temel Kavramlar",
    "icerik": """ELEKTROKIMYA TEMEL KAVRAMLAR:

1. YUKSELTGENME-INDIRGENME (REDOKS) TEPKIMELERI:
   - Yukseltgenme: Elektron kaybetme. Yukseltgenme basamagi artar.
   - Indirgenme: Elektron kazanma. Yukseltgenme basamagi azalir.
   - Redoks tepkimesi: Yukseltgenme ve indirgenmenin ayni anda gerceklesmesi.
   - Yukseltgen madde: Baskasini yukseltgeyip kendisi indirgenen.
   - Indirgen madde: Baskasini indirgevip kendisi yukseltgenen.

2. YUKSELTGENME BASAMAKLARI:
   - Saf element: 0 (Fe, O₂, H₂, Cu)
   - Alkali metaller: +1 (Na, K, Li)
   - Toprak alkali metaller: +2 (Ca, Mg, Ba)
   - Flor: Her zaman -1
   - Oksijen: Genellikle -2 (peroksitlerde -1, OF₂'de +2)
   - Hidrojen: Genellikle +1 (metal hidrürlerde -1)
   - Bileikteki tum yukseltgenme basamaklari toplami = 0.
   - Iyondaki toplam = iyon yuku.

3. REDOKS DENKLEMLERININ DENKLENMESI:
   - Yarim tepkime yontemi:
     a) Yukseltgenme ve indirgenme yarim tepkimelerini yaz.
     b) Her yarim tepkimede elektron sayisini dengele.
     c) Verilen/alinan elektron sayilarini esitle.
     d) Yarim tepkimeleri topla.
   - Ornek: Zn + Cu²⁺ → Zn²⁺ + Cu
     Yukseltgenme: Zn → Zn²⁺ + 2e⁻
     Indirgenme: Cu²⁺ + 2e⁻ → Cu

4. AKTIVITE SERISI (INDIRGEME POTANSIYELI):
   - Li > K > Ca > Na > Mg > Al > Zn > Fe > Ni > Sn > Pb > H > Cu > Ag > Pt > Au
   - Soldakiler daha aktif (kolay yukseltgenir), sagdakiler daha soy (zor yukseltgenir).
   - Aktif metal, seyreltiik asitle tepkime vererek H₂ gazi cikarir.
   - Cu, Ag, Pt, Au seyreltik asitlerle H₂ cikaramaz (H'den sonra gelir).
"""
},

"KIM.12.1.GALVANIK_PIL": {
    "unite": "Kimya ve Elektrik",
    "baslik": "Galvanik (Volta) Piller",
    "icerik": """GALVANIK PILLER:

1. TANIM:
   - Kendiliğinden gerceklesen redoks tepkimesinden elektrik enerjisi ureten duzeneketir.
   - Kimyasal enerji → Elektrik enerjisi donusumu.
   - Anot: Yukseltgenmenin gerceklestigi elektrot (- kutup).
   - Katot: Indirgenmenin gerceklestigi elektrot (+ kutup).

2. DANIELL PILI (ORNEK):
   - Anot: Zn levha, Zn → Zn²⁺ + 2e⁻ (yukseltgenme).
   - Katot: Cu levha, Cu²⁺ + 2e⁻ → Cu (indirgenme).
   - Tuz koprusu: Iyonlarin gecisini saglayarak devreyi tamamlar.
   - E°_pil = E°_katot - E°_anot = +0.34 - (-0.76) = +1.10 V.
   - Elektronlar dis devreden anottan katoda akar.

3. STANDART ELEKTROT POTANSIYELI (E°):
   - Standart hidrojen elektrodu (SHE) referans alinir: E° = 0.00 V.
   - E° > 0: Indirgenme egilimi yuksek (iyi yukseltgen).
   - E° < 0: Yukseltgenme egilimi yuksek (iyi indirgen).
   - E°_pil > 0 ise tepkime kendiliginden gerceklesir.

4. PIL TURLERI:
   - Kuru pil (Leclanché): Zn anot, MnO₂ katot, NH₄Cl elektrolit. 1.5 V.
   - Alkalin pil: Zn anot, MnO₂ katot, KOH elektrolit. Daha uzun omur.
   - Lityum pil: Li anot, yuksek enerji yogunlugu, hafif.
   - Kursun-asit aku: Pb/PbO₂, H₂SO₄. Araba akusu. Sarj edilebilir. 2 V/hucre.
   - Lityum-iyon pil: Li-iyon, sarj edilebilir, cep telefonu/laptop/EV.
   - Yakit hucresi: H₂ + O₂ → H₂O + elektrik. Surekli yakit beslemesi gerekir.

5. KOROZYON:
   - Metallerin cevre etkileriyle yukseltgenerek bozunmasi.
   - Demir paslanmasi: Fe → Fe²⁺ + 2e⁻ (anodik bolge).
   - O₂ + 2H₂O + 4e⁻ → 4OH⁻ (katodik bolge).
   - Fe(OH)₂ → Fe₂O₃·xH₂O (pas).
   - Korunma yontemleri: Boya, galvaniz (Zn kaplama), katodik koruma, alasim.
"""
},

"KIM.12.1.ELEKTROLIZ": {
    "unite": "Kimya ve Elektrik",
    "baslik": "Elektroliz",
    "icerik": """ELEKTROLIZ:

1. TANIM:
   - Dis elektrik enerjisi kullanilarak kendiliğinden gerceklesmeyen redoks
     tepkimesinin zorla gerceklestirilmesidir.
   - Elektrik enerjisi → Kimyasal enerji donusumu.
   - Galvanik pilin tersidir.
   - Anot: Yukseltgenmenin gerceklestigi elektrot (+ kutba bagli).
   - Katot: Indirgenmenin gerceklestigi elektrot (- kutba bagli).

2. ERIMIS TUZUN ELEKTROLIZI:
   - NaCl (erimis): Na⁺ ve Cl⁻ iyonlari serbest.
   - Katot: Na⁺ + e⁻ → Na (sivi sodyum metal).
   - Anot: 2Cl⁻ → Cl₂ + 2e⁻ (klor gazi).
   - Sodyum metal uretiminde kullanilir (Downs hucresi).

3. SULU COZELTININ ELEKTROLIZI:
   - Su da elektrolize katilir: 2H₂O → O₂ + 4H⁺ + 4e⁻ (anot) veya
     2H₂O + 2e⁻ → H₂ + 2OH⁻ (katot).
   - NaCl sulu cozeltisi:
     Katot: 2H₂O + 2e⁻ → H₂ + 2OH⁻ (Na yerine H₂O indirgenir, Na cok aktif).
     Anot: 2Cl⁻ → Cl₂ + 2e⁻ (klor gazi cikar).
   - CuSO₄ sulu cozeltisi:
     Katot: Cu²⁺ + 2e⁻ → Cu (bakir metal kaplamasi).
     Anot: 2H₂O → O₂ + 4H⁺ + 4e⁻ (oksijen gazi cikar).

4. FARADAY KANUNLARI:
   - Birinci kanun: Elektrolizde biriken madde miktari, gecen elektrik yukuyle doğru orantilidir.
   - m = (M × I × t) / (n × F)
     m: kutle (g), M: mol kutlesi, I: akim (A), t: sure (s),
     n: aktarilan elektron sayisi, F: Faraday sabiti = 96485 C/mol.
   - 1 Faraday = 1 mol elektron yuku = 96485 C.

5. ELEKTROLIZ UYGULAMALARI:
   - Elektrokaplama: Metal esyalarin baska bir metalle kaplanmasi (krom, nikel, altin).
   - Elektrorafinasyon: Saf olmayan metallerin saflandirilmasi (Cu rafinasyonu).
   - Aluminyum uretimi: Hall-Héroult prosesi (Al₂O₃ elektrolizi, kriyolit icinde).
   - Suyun elektrolizi: 2H₂O → 2H₂ + O₂ (hidrojen uretimi).
   - Klor-alkali prosesi: NaCl cozeltisinden NaOH, Cl₂, H₂ uretimi.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: KARBON KIMYASI (ORGANIK)
# ═══════════════════════════════════════════════════════════════

"KIM.12.2.KARBON_KIMYASI_TEMEL": {
    "unite": "Karbon Kimyası (Organik)",
    "baslik": "Karbon Kimyasi Temel Kavramlar ve Hibritlesmeler",
    "icerik": """KARBON KIMYASI:

1. KARBONUN OZELLIKLERI:
   - Atom numarasi: 6, elektron dizilimi: 1s² 2s² 2p².
   - 4 degerlidir → 4 kovalent bag yapabilir.
   - Kendisiyle uzun zincirler ve halkali yapilar olusturur (katenasyon).
   - sp³, sp², sp hibritlesmesi yapabilir.

2. HIBRITLESMELER:
   a) sp³ hibritlesmesi:
      - 4 sigma bagi, tetraedral geometri, 109.5° bag acisi.
      - Ornek: CH₄ (metan), C₂H₆ (etan).
   b) sp² hibritlesmesi:
      - 3 sigma + 1 pi bagi, duzlemsel ucgen, 120° bag acisi.
      - Ornek: C₂H₄ (etilen), C₆H₆ (benzen).
   c) sp hibritlesmesi:
      - 2 sigma + 2 pi bagi, dogrusal, 180° bag acisi.
      - Ornek: C₂H₂ (asetilen), HCN.

3. BAG TURLERI:
   - Tekli bag (σ): Serbest donuse izin verir, en uzun ve en zayif.
   - Ikili bag (σ + π): Donuse izin vermez, daha kisa ve guclu.
   - Uclu bag (σ + 2π): En kisa ve en guclu.

4. IZOMERLIK:
   a) Yapi (yapisal) izomerligi: Zincir, konum, fonksiyonel grup izomerligi.
   b) Geometrik (cis-trans) izomerlik: C=C cift baginda farkli gruplarin dizilisi.
   c) Optik izomerlik: Kiral karbon → ayna goruntusu ustuste gelmez.

5. ADLANDIRMA (IUPAC):
   - En uzun karbon zincirini bul.
   - Dallanmalara en yakin uctan numaralandir.
   - Dallari alfabe sirasina gore yaz.
   - Cift/uclu bag varsa -en/-in soneki ekle.
"""
},

"KIM.12.2.HIDROKARBONLAR": {
    "unite": "Karbon Kimyası (Organik)",
    "baslik": "Hidrokarbonlar: Alkanlar, Alkenler, Alkinler, Aromatikler",
    "icerik": """HIDROKARBONLAR:

1. ALKANLAR (DOYMUS):
   - Genel formul: CₙH₂ₙ₊₂ (n ≥ 1). Yalnizca tekli bag.
   - Tum karbonlar sp³ hibrit.
   - Metan CH₄, Etan C₂H₆, Propan C₃H₈, Butan C₄H₁₀, Pentan C₅H₁₂.
   - Fiziksel: C₁-C₄ gaz, C₅-C₁₇ sivi, C₁₈+ kati. Suda cozmez.
   - Tepkimeler: Yanma, halojenlenme (yer degistirme), krakingleme.

2. ALKENLER (BIR CIFT BAG):
   - Genel formul: CₙH₂ₙ (n ≥ 2). En az bir C=C ikili bagi.
   - sp² hibrit karbonlar. Eten (etilen) CH₂=CH₂ en basit alken.
   - Katilma tepkimeleri: Hidrojenlenme, halojenlenme, su katilmasi, HX katilmasi.
   - Markovnikov kurali: HX katilmasinda H, daha fazla H'li karbona baglanir.
   - Cis-trans izomerligi: Cift bagdaki her karbonda farkli gruplar olmali.
   - Polimerizasyon: nCH₂=CH₂ → (-CH₂-CH₂-)ₙ (polietilen).

3. ALKINLER (BIR UCLU BAG):
   - Genel formul: CₙH₂ₙ₋₂ (n ≥ 2). En az bir C≡C uclu bagi.
   - sp hibrit karbonlar. Etin (asetilen) CH≡CH en basit alkin.
   - 1 mol H₂ → alken, 2 mol H₂ → alkan. Brom suyu rengini giderir.

4. AROMATIK HIDROKARBONLAR:
   - Benzen C₆H₆: Duzlemsel, 6 karbon sp² hibrit, delokalize pi sistemi.
   - Huckel kurali: 4n+2 pi elektron → aromatik.
   - Yer degistirme tepkimesi verir (katilma degil): Nitrolama, halojenlenme, sulfonlama.
   - Turevleri: Toluen (C₆H₅CH₃), Fenol (C₆H₅OH), Anilin (C₆H₅NH₂).

5. SIKLOALKANLAR:
   - Genel formul: CₙH₂ₙ (n ≥ 3). Halkali yapilar.
   - Siklohekzan en kararli (sandalye formu).
"""
},

"KIM.12.2.FONKSIYONEL_GRUPLAR": {
    "unite": "Karbon Kimyası (Organik)",
    "baslik": "Fonksiyonel Gruplar: Alkoller, Eterler, Aldehitler, Ketonlar, Karboksilik Asitler, Esterler, Aminler",
    "icerik": """FONKSIYONEL GRUPLAR:

1. ALKOLLER (R-OH):
   - 1° alkol: R-CH₂OH, 2° alkol: R₂CHOH, 3° alkol: R₃COH.
   - H-bagi yapar → kaynama noktasi yuksek. Kucuk olanlar suda cozunur.
   - Yukseltgenme: 1° → aldehit → karboksilik asit; 2° → keton; 3° → yukseltgenmez.
   - Dehidratasyon: 170°C → alken, 140°C → eter.
   - Esterlesme: Alkol + karboksilik asit → ester + H₂O.

2. ETERLER (R-O-R'):
   - Alkollerle izomer (CₙH₂ₙ₊₂O). H-bagi yapamaz → dusuk kaynama noktasi.
   - Kimyasal olarak inert. Dietil eter anestezide kullanildi.

3. ALDEHITLER (R-CHO) VE KETONLAR (R-CO-R'):
   - Karbonil grubu C=O. Aldehit: Zincir ucunda. Keton: Zincir ortasinda.
   - Tollens testi: Aldehit gumus ayna verir, keton vermez.
   - Fehling testi: Aldehit kirmizi Cu₂O cokeltisi verir.
   - Aldehit kolayca karboksilik aside yukseltgenir.

4. KARBOKSILIK ASITLER (R-COOH):
   - Guclu H-bagi → en yuksek kaynama noktasi (esit mol kutlesinde).
   - Zayif asit: CH₃COOH ⇌ CH₃COO⁻ + H⁺.
   - Esterlesme: R-COOH + R'OH ⇌ RCOOR' + H₂O (tersinir).

5. ESTERLER (R-COO-R'):
   - Hos kokulu (meyve kokulari). H-bagi yapamaz.
   - Sabunlasma: Ester + NaOH → Karboksilat tuzu + alkol.
   - Yaglar: Trigliserit = gliserol + 3 yag asidi (ester bagi).

6. AMINLER (R-NH₂):
   - 1°, 2°, 3° aminler. Zayif baz ozelligi. Balik kokusu.
   - Amino asitler: H₂N-CHR-COOH (hem asit hem baz = amfoter).
   - Peptit bagi: -CO-NH- (proteinlerin temel bagi).

7. KAYNAMA NOKTASI SIRASI (esit mol kutlesi):
   Karboksilik asit > alkol > aldehit/keton > eter > alkan.
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: ENERJI KAYNAKLARI VE YAKITLAR
# ═══════════════════════════════════════════════════════════════

"KIM.12.3.FOSIL_YAKITLAR": {
    "unite": "Enerji Kaynakları ve Yakıtlar",
    "baslik": "Fosil Yakitlar ve Petrokimya",
    "icerik": """FOSIL YAKITLAR:

1. KOMUR:
   - En eski fosil yakit. Bitkisel kalintilarin milyonlarca yilda donusmesi.
   - Turler (artan karbon orani): Turba → Linyit → Tas komuru → Antrasit.
   - Yanma: C + O₂ → CO₂ + enerji.
   - Sorunlar: CO₂ emisyonu (sera etkisi), SO₂ (asit yagmuru), kul, civa.

2. PETROL:
   - Hidrokarbonlarin karisimi. Deniz organizmalarin fosili.
   - Fraksiyonlu damitma ile ayristirma (kaynama noktasina gore):
     * LPG (C₃-C₄): Tup gaz
     * Benzin (C₅-C₁₂): Arac yakiti
     * Gazyagi/Kerosin (C₁₂-C₁₆): Ucak yakiti, lampa
     * Mazot/Dizel (C₁₅-C₁₈): Dizel motorlar
     * Fuel oil (C₁₈-C₂₅): Sanayi yakiti
     * Asfalt/Bitum (C₂₅+): Yol kaplama
   - Oktan sayisi: Benzin kalitesi. Izooktan = 100, n-heptan = 0.
   - Krakingleme: Buyuk hidrokarbonlar → kucuk hidrokarbonlar (benzin verimi artar).

3. DOGAL GAZ:
   - Basagirlikli metan (CH₄, %70-90) + etan, propan, butan.
   - En temiz fosil yakit (birim enerji basina en az CO₂).
   - CH₄ + 2O₂ → CO₂ + 2H₂O.
   - LNG (sivilastirilmis dogal gaz): -162°C'de sivilastirilir, tasimada kullanilir.

4. PETROKIMYA URUNLERI:
   - Plastikler: PE, PP, PVC, PS, PET (monomerleri petrolden).
   - Sentetik lifler: Naylon, polyester.
   - Deterjanlar, boyalar, ilaclar, gubre hammaddesi.
   - Petrokimya sanayii modern yasamin temel taslarindan.
"""
},

"KIM.12.3.YENILENEBILIR_ENERJI": {
    "unite": "Enerji Kaynakları ve Yakıtlar",
    "baslik": "Yenilenebilir Enerji, Biyoyakitlar ve Hidrojen",
    "icerik": """YENILENEBILIR ENERJI VE ALTERNATIF YAKITLAR:

1. BIYOYAKITLAR:
   - Biyoetanol: Seker/nisastanin fermantasyonu → C₂H₅OH.
     C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂ (maya enzimleri).
   - Biyodizel: Bitkisel yag + metanol → FAME (transesterifikasyon).
   - Biyogaz: Organik atiklarin anaerobik ayrismasi → CH₄ + CO₂.
   - Karbon notralite: Bitkiler buyurken CO₂ emerek buyur, yandığında CO₂ salar.

2. HIDROJEN ENERJISI:
   - 2H₂ + O₂ → 2H₂O + enerji (tek urun SU!).
   - Yakit hucresi: H₂ + O₂ → elektrik + H₂O (dogrudan donusum).
   - Uretim: Elektroliz (2H₂O → 2H₂ + O₂), buhar reformlama (CH₄ + H₂O → CO + 3H₂).
   - Avantaj: Sifir emisyon, yuksek enerji yogunlugu (kutle basina).
   - Dezavantaj: Depolama zorlugu, patlayici, uretim maliyeti.

3. GUNES ENERJISI:
   - Fotovoltaik hucre: Silisyum yari iletken, isik → elektrik.
   - Gunes termal: Isitma ve elektrik uretimi.
   - Fotokimyasal: Suyun gunesle ayristirilmasi arastirmalari.

4. NUKLEER ENERJI:
   - Fisyon: ²³⁵U + n → parcalanma urunleri + 2-3 n + ~200 MeV.
   - Fuzyon: ²H + ³H → ⁴He + n + 17.6 MeV (Gunes enerjisinin kaynagi).
   - CO₂ emisyonu yok, ancak radyoaktif atik sorunu var.

5. CEVRE KIMYASI:
   - Sera etkisi: CO₂, CH₄, N₂O → Kuresel isinma.
   - Asit yagmurlari: SO₂ + H₂O → H₂SO₃, NO₂ + H₂O → HNO₃.
   - Ozon tabakasi: CFC'ler → O₃ tahribi. Montreal Protokolu (1987).
   - Karbon ayak izi: Bireylerin/kurumlarin CO₂ emisyon miktari.
   - Yesil kimya: Atik azaltma, yenilenebilir hammadde, enerji verimi.

6. POLIMER VE CEVRE:
   - Plastik kirlilik: Dogada yuz yillar bozunmaz. Mikroplastik sorunu.
   - Geri donusum kodlari: PET(1), HDPE(2), PVC(3), LDPE(4), PP(5), PS(6).
   - Biyobozunur polimerler: PLA (misir nisastasindan), PHA (bakteri uretimi).
"""
},

"KIM.12.3.POLIMER_KIMYASI": {
    "unite": "Enerji Kaynakları ve Yakıtlar",
    "baslik": "Polimer Kimyasi (Toplama ve Yogunlasma Polimerizasyonu)",
    "icerik": """POLIMER KIMYASI:

1. TEMEL KAVRAMLAR:
   - Monomer: Polimeri olusturan kucuk tekrarlanan birim.
   - Polimer: Cok sayida monomerin birlesimi (poly = cok, mer = parca).
   - Polimerizasyon derecesi (n): Tekrarlanan birim sayisi.

2. TOPLAMA (ADISYON) POLIMERIZASYONU:
   - Monomerlerde C=C cift bag vardir. Cift bag acilarak monomerler birlesir.
   - Yan urun OLUSTURMAZ.
   - nCH2=CH2 -> (-CH2-CH2-)n (polietilen / PE)
   - Ornekler:
     Polietilen (PE): Poset, ambalaj.
     Polipropilen (PP): Halat, mobilya.
     Polivinil klorur (PVC): Boru, doseme.
     Polistiren (PS): Strafor, bardak.
     Teflon (PTFE): Yapismaz tava (nCF2=CF2 -> (-CF2-CF2-)n).

3. YOGUNLASMA (KONDENSASYON) POLIMERIZASYONU:
   - Iki farkli fonksiyonel gruplu monomerler reaksiyona girer.
   - Yan urun olusur (genellikle H2O).
   - Ornekler:
     Naylon 6,6: Adipik asit + heksametilendiamin -> poliamit + H2O.
     Polyester (PET): Tereftalik asit + etilen glikol -> poliester + H2O.
     Bakalit: Fenol + formaldehit -> fenol-formaldehit polimeri + H2O.

4. TERMOPLASTIK vs TERMOSET:
   - Termoplastik: Isitilinca yumusar, soguyunca sertlesir (TERSINIR). Geri donusume UYGUN.
   - Termoset: Bir kez sekil aldiktan sonra tekrar sekillendirilmez (capraz bagli). Geri donusume uygun DEGIL.

5. KAUCUK VE VULKANIZASYON:
   - Dogal kaucuk: Poliizopren, elastik ama isiya dayanikli degil.
   - Vulkanizasyon: Kaucuk + kukurt (S) -> capraz bagli yapi (daha sert, dayanikli).
   - Sentetik kaucuk: SBR (stiren-butadien), Neopren (kimyasal direncli).
"""
},

"KIM.12.2.ORGANIK_TEPKIMELER": {
    "unite": "Karbon Kimyası",
    "baslik": "Organik Tepkime Turleri ve Ayirt Edici Testler",
    "icerik": """ORGANIK TEPKIME TURLERI:

1. KATILMA (ADISYON):
   - Doymamis bilesiklere (alken, alkin) kucuk molekul eklenmesi.
   - CH2=CH2 + H2 -> CH3-CH3 (hidrojenleme, Ni katalizor).
   - CH2=CH2 + Br2 -> CH2Br-CH2Br (brom suyu renksizlesir).
   - CH2=CH2 + HCl -> CH3-CH2Cl.
   - CH2=CH2 + H2O -> CH3-CH2OH (hidratasyon, H2SO4 katalizor).

2. YER DEGISTIRME (SUBSTITUSYON):
   - Doymus bilesiklerde (alkan, aromatik) bir atom/grup baskasi ile yer degistirir.
   - CH4 + Cl2 -> CH3Cl + HCl (UV isigi altinda).
   - Benzen + HNO3 -> Nitrobenzen + H2O (H2SO4 katalizor).

3. AYRILMA (ELIMINASYON):
   - Molekulden kucuk bir molekul (H2O, HX) ayrilarak cift bag olusur.
   - CH3-CH2OH -> CH2=CH2 + H2O (170 derece, H2SO4, dehidratasyon).

4. YUKSELTGENME-INDIRGENME:
   - 1. alkol -> aldehit -> karboksilik asit (yukseltgenme).
   - 2. alkol -> keton (yukseltgenme).
   - 3. alkol -> yukseltgenmez (normal kosullarda).
   - Aldehit + H2 -> 1. alkol (indirgenme).

5. ESTERLESME VE HIDROLIZ:
   - R-COOH + R'-OH -> R-COO-R' + H2O (esterlesme, asit katalizor).
   - R-COO-R' + NaOH -> R-COONa + R'-OH (sabunlasma/hidroliz).

6. AYIRT EDICI TESTLER:
   - Brom suyu: Doymamis bilesikelr renksizlestirir, doymuslar renksizlestirmez.
   - Tollens (gumus ayna): Aldehit (+), Keton (-).
   - Fehling/Benedict: Aldehit kirmizi cokelet, Keton tepki vermez.
   - Turnusol kagidi: Karboksilik asit (kirmizi), amin (mavi).
   - Sodyum metal: Alkol + Na -> H2 gazi cikar; eter + Na -> tepki vermez.
   - Lucas ayiraci: 3. alkol aninda bulanir, 2. alkol 5 dk, 1. alkol tepki vermez.
"""
},

"KIM.12.STRATEJI": {
    "unite": "AYT Strateji",
    "baslik": "AYT Kimya Sinav Stratejileri ve Ipuclari",
    "icerik": """AYT KIMYA SINAV STRATEJILERI:

1. ORGANIK KIMYA:
   - Fonksiyonel gruplari ve genel formulleri EZBERLE:
     Alkan CnH2n+2, Alken CnH2n, Alkin CnH2n-2.
   - Yukseltgenme sirasi: 1. alkol -> aldehit -> karboksilik asit, 2. alkol -> keton.
   - Kaynama noktasi sirasi: Karboksilik asit > alkol > aldehit/keton > eter > alkan.

2. ADLANDIRMA:
   - En uzun zincir + uygun sonek (-an, -en, -in, -ol, -al, -on, -oik asit).
   - En kucuk numara toplami kuralini uygula.

3. ELEKTROKIMYA:
   - Galvanik pil: Kendilginden gerceklesir, E > 0.
   - Elektroliz: Dis enerji gerekir, E < 0.
   - Anot (+) yukseltgenme, katot (-) indirgenme.

4. ENERJI KAYNAKLARI:
   - H2: Yandiginda sadece su olusturur (en temiz yakit).
   - Biyoyakit: Karbon notral.

5. POLIMER SORULARI:
   - Toplama: Cift bag -> yan urun yok.
   - Yogunlasma: Farkli fonksiyonel gruplar -> H2O cikar.

6. ZAMAN YONETIMI:
   - AYT Kimya: 13 soru, yaklasik 25 dakika.
   - Organik kimya AYT'de en agirlikli konu.
"""
},

}

def get_kimya12_reference(topic: str) -> list:
    """Verilen konuya en yakin kimya 12 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in KIMYA_12_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_kimya12_keys() -> list:
    """Tum kimya 12 referans anahtarlarini dondurur."""
    return list(KIMYA_12_REFERANS.keys())
