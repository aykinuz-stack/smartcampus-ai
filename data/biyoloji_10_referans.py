# -*- coding: utf-8 -*-
"""
10. Sinif Biyoloji dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Hucre Bolunmeleri
2. Kalitim (Mendel Genetigi)
3. DNA ve RNA Yapisi
4. Protein Sentezi
5. Mutasyon ve Genetik Muhendislik
"""

BIYOLOJI_10_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: HUCRE BOLUNMELERI
# ═══════════════════════════════════════════════════════════════

"BIY.10.1.MITOZ_BOLUNME": {
    "unite": "Hucre Bolunmeleri",
    "baslik": "Mitoz Bolunme ve Evreleri",
    "icerik": """
MITOZ BOLUNME:

1. TANIM VE AMAC:
   - Bir hucreden genetik olarak AYNI iki yavru hucre olusur
   - Buyume, onarim ve eseyiz ureme icin gereklidir
   - Kromozom sayisi DEGISMEZ (2n -> 2n)
   - Vucut hucrelerinde (somatik) gerceklesir

2. MITOZ EVRELERI:
   a) PROFAZ:
      - Kromatin iplikleri kisalip kalinlasarak KROMOZOM halini alir
      - Her kromozom iki KARDES KROMATID'den olusur (sentromerle bagli)
      - Cekirdek zari ve cekirdekçik erir
      - Sentrioller kutuplara goceder, ig iplikleri olusur
   b) METAFAZ:
      - Kromozomlar hucrenin ORTA DUZLEMINE (ekator) dizilir
      - Ig iplikleri kromozomlarin sentromerlerine baglanir
      - Kromozomlar en NET goruldugu evredir (karyotip analizi icin)
   c) ANAFAZ:
      - Sentromerler ayrilir, kardes kromatidler kutuplara cekilir
      - Hucrede kromozom sayisi gecici olarak iki katina cikar
      - En kisa sureli evredir
   d) TELOFAZ:
      - Kromozomlar kutuplara ulasir, tekrar kromatin haline doner
      - Cekirdek zari ve cekirdekçik yeniden olusur
      - Ig iplikleri kaybolur

3. SITOPLAZMA BOLUNMESI (SITOKINEZ):
   - Hayvan hucresi: Bosalma (invaginasyon) ile ortadan boğumlanir
   - Bitki hucresi: Ortada HUCRE PLAGI (ara lamel) olusur
   - Sonuc: Iki genetik olarak AYNI yavru hucre

4. ONEMLI NOKTALAR:
   - Mitoz oncesi INTERFAZ'da DNA eslesir (S evresi)
   - Hucre dongusu: G1 -> S -> G2 -> MITOZ
   - Kanser: Kontrolsuz mitoz bolunme sonucu olusur
"""
},

"BIY.10.1.MAYOZ_BOLUNME": {
    "unite": "Hucre Bolunmeleri",
    "baslik": "Mayoz Bolunme (Mayoz I ve Mayoz II)",
    "icerik": """
MAYOZ BOLUNME:

1. TANIM VE AMAC:
   - Eseyil ureme hucreleri (gamet) olusturmak icin yapilir
   - Kromozom sayisi YARILIR (2n -> n)
   - Genetik cesitlilik saglar (crossing over + bagimsiz dagılım)
   - Sadece ESEYIL UREME ORGANLARI'nda (gonad) gerceklesir

2. MAYOZ I (INDIRGENME BOLUNMESI):
   a) PROFAZ I:
      - Homolog kromozomlar ESLESIR (sinapsis/tetrad olusumu)
      - CROSSING OVER (parca degisimi) gerceklesir -> genetik cesitlilik
      - Cekirdek zari erir, ig iplikleri olusur
   b) METAFAZ I:
      - Homolog kromozom CIFTLERI hucre ortasina dizilir
      - Hangi homologun hangi kutba gidecegi RASTGELEDIR (bagimsiz dagılım)
   c) ANAFAZ I:
      - HOMOLOG KROMOZOMLAR birbirinden ayrilir (kardes kromatidler AYRILMAZ)
      - Her kutba n sayida kromozom gider (haploid)
   d) TELOFAZ I:
      - Iki FARKLI hucre olusur (n kromozom, 2 kromatidli)

3. MAYOZ II (MITOZA BENZER):
   a) Profaz II -> Metafaz II -> Anafaz II -> Telofaz II
   - Kardes kromatidler bu sefer AYRILIR
   - Sonuc: Toplam DORT haploid (n) hucre olusur

4. GAMET OLUSUMU:
   - Erkek: Bir spermatosit -> 4 sperm (hepsi fonksiyonel)
   - Disi: Bir oosit -> 1 yumurta + 3 kutup cisimcigi (1 fonksiyonel)
   - Kutup cisimcikleri: Sitoplazma esitsiz bolunerek buyuk yumurtaya besin saglar

5. MITOZ-MAYOZ FARKLARI:
   - Mitoz: 2n->2n, 2 hucre, genetik ayni, vucut hucresi
   - Mayoz: 2n->n, 4 hucre, genetik farkli, ureme hucresi
   - Mayoz'da crossing over VAR, mitoz'da YOK
"""
},

"BIY.10.1.HUCRE_DONGUSU": {
    "unite": "Hucre Bolunmeleri",
    "baslik": "Hucre Dongusu ve Interfaz",
    "icerik": """
HUCRE DONGUSU:

1. INTERFAZ (HAZIRLIK EVRESI):
   - G1 evresi: Hucre buyur, protein sentezler, organeller coğalir
   - S evresi: DNA ESLESMESI (replikasyon) gerceklesir
   - G2 evresi: Bolunme icin son hazirliklar, ATP birikimi
   - Interfaz hucre dongusunun EN UZUN evresidir (%90-95)

2. MITOTIK EVRE (M EVRESI):
   - Profaz -> Metafaz -> Anafaz -> Telofaz + Sitokinez
   - Hucre dongusunun en kisa evresidir

3. HUCRE DONGUSU KONTROL NOKTALARI:
   - G1 kontrol noktasi: Hucre bolunmeye hazir mi? (en onemli)
   - G2 kontrol noktasi: DNA dogru kopyalandi mi?
   - M kontrol noktasi: Kromozomlar ig ipliklerine dogru baglandi mi?
   - Kontrol bozulursa -> KANSER

4. G0 EVRESI:
   - Bolunmeyen hucreler bu evrede kalir
   - Sinir hucreleri, kas hucreleri gibi farklilasmiş hucreler
   - Bolunme sinyali alirsa tekrar donguye girebilir (bazi hucreler)
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: KALITIM (MENDEL GENETIGI)
# ═══════════════════════════════════════════════════════════════

"BIY.10.2.MENDEL_GENETIGI": {
    "unite": "Kalitim",
    "baslik": "Mendel Genetigi Temel Kavramlar",
    "icerik": """
MENDEL GENETIGI:

1. TEMEL KAVRAMLAR:
   - GEN: Kalitim birimi, DNA uzerinde belirli bir bolgedir
   - ALLEL: Bir genin farkli bicimleri (ornegin: A ve a)
   - GENOTIP: Bireyin genetik yapisi (AA, Aa, aa)
   - FENOTIP: Bireyin gozlenebilir ozelligi (uzun boylu, kisa boylu)
   - HOMOZIGOT: Iki allel AYNI (AA veya aa) -> saf dol
   - HETEROZIGOT: Iki allel FARKLI (Aa) -> melez
   - DOMINANT (baskin): Heterozigotta fenotipi belirleyen allel (A)
   - RESESIF (cekinik): Sadece homozigotta fenotipi belirleyen allel (a)

2. MENDEL'IN CALISMASI:
   - Bezelye (Pisum sativum) bitkisi ile deneyler yapti
   - 7 karakter inceledi (tohum rengi, sekli, cicek rengi vb.)
   - KONTROLLÜ CAPRAZLAMA yapti (saf dol ebeveynler)
   - Matematiksel oranlar kesfetti

3. MENDEL'IN 1. YASASI (AYRISMA YASASI):
   - Her birey bir karakter icin IKI ALLEL tasir
   - Gamet olusumunda alleler AYRILIR
   - Her gamete sadece BIR allel gider
   - Aa x Aa -> 1 AA : 2 Aa : 1 aa (genotip orani)
   - Fenotip orani: 3 dominant : 1 resesif

4. MENDEL'IN 2. YASASI (BAGIMSIZ DAGILIS):
   - Farkli karakterlere ait genler bagimsiz aktarilir
   - AaBb x AaBb -> 9:3:3:1 fenotip orani
   - Genler FARKLI KROMOZOMLARDA olmalidir
"""
},

"BIY.10.2.CAPRAZLAMA_PUNNETT": {
    "unite": "Kalitim",
    "baslik": "Caprazlama ve Punnett Karesi",
    "icerik": """
CAPRAZLAMA VE PUNNETT KARESI:

1. PUNNETT KARESI:
   - Caprazlama sonuclarini tahmin etmek icin kullanilir
   - Ebeveyn gametleri satirlara ve sutunlara yazilir
   - Kesisim noktalari olasi yavru genotiplerini gosterir

2. MONOHIBRIT CAPRAZLAMA (tek karakter):
   a) Saf dol x Saf dol: AA x aa -> tumu Aa (F1 hepsi melez)
   b) F1 x F1: Aa x Aa -> 1 AA : 2 Aa : 1 aa
      Fenotip: 3 baskin : 1 cekinik
   c) Geri caprazlama: Aa x aa -> 1 Aa : 1 aa (1:1 orani)
   d) Kontrol caprazlama: Baskin fenotipli bireyin genotipi bilinmek icin
      resesif homozigot ile caprazlama yapilir

3. DIHIBRIT CAPRAZLAMA (iki karakter):
   - AaBb x AaBb -> 16 kombinasyon
   - Fenotip orani: 9:3:3:1
   - 9 A_B_ : 3 A_bb : 3 aaB_ : 1 aabb

4. ORNEK PROBLEMLER:
   - Uzun boy (U) kisa boya (u) baskin
   - UU x uu -> tumu Uu (uzun)
   - Uu x Uu -> 3 uzun : 1 kisa
   - Uu x uu -> 1 uzun : 1 kisa
"""
},

"BIY.10.2.ES_BASKINLIK_EKSIK_BASKINLIK": {
    "unite": "Kalitim",
    "baslik": "Es Baskinlik ve Eksik Baskinlik",
    "icerik": """
ES BASKINLIK VE EKSIK BASKINLIK:

1. EKSIK BASKINLIK (YARIM BASKINLIK):
   - Heterozigotta iki allelin etkisi KARISIR
   - Ara fenotip (intermediate) ortaya cikar
   - Ornek: Kirmizi cicek (RR) x Beyaz cicek (R'R') -> Pembe cicek (RR')
   - F2 orani: 1 kirmizi : 2 pembe : 1 beyaz (1:2:1)
   - Genotip orani = Fenotip orani (1:2:1)

2. ES BASKINLIK (KODOMINANS):
   - Heterozigotta IKI ALLEL DE tam olarak ifade edilir
   - Karisma degil, IKI FENOTIPIN BIRLIKTE gorulmesi
   - Ornek: Kirmizi-beyaz benekli cicek
   - Her iki allel de AYNI GUCTE etkisini gosterir

3. FARKLAR:
   - Eksik baskinlik: Ara renk olusur (pembe)
   - Es baskinlik: Iki renk yan yana gorulur (kirmizi-beyaz benekli)
   - Her ikisinde de DOMINANT-RESESIF iliskisi YOKTUR
   - Her ikisinde de genotip orani = fenotip orani
"""
},

"BIY.10.2.KAN_GRUBU_ABO_RH": {
    "unite": "Kalitim",
    "baslik": "Kan Grubu (ABO ve Rh Sistemi) - Coklu Allel",
    "icerik": """
KAN GRUBU KALITIMI:

1. ABO KAN GRUBU SISTEMI (COKLU ALLEL):
   - Bir gende UCTEN FAZLA allel vardir: I^A, I^B, i
   - I^A ve I^B birbirine ES BASKIN (kodominant)
   - I^A ve I^B, i'ye BASKIN (dominant)
   - Genotipler ve Fenotipler:
     * A grubu: I^A I^A veya I^A i
     * B grubu: I^B I^B veya I^B i
     * AB grubu: I^A I^B (es baskinlik)
     * O grubu: ii (resesif homozigot)

2. ANTIKOR-ANTIJEN ILISKISI:
   - A grubu: A antijeni var, anti-B antikoru var
   - B grubu: B antijeni var, anti-A antikoru var
   - AB grubu: A+B antijeni var, antikoru YOK -> GENEL ALICI
   - O grubu: Antijeni YOK, anti-A + anti-B antikoru var -> GENEL VERICI

3. Rh FAKTORU:
   - Rh+ (baskin): RR veya Rr -> Rh antijeni VAR
   - Rh- (cekinik): rr -> Rh antijeni YOK
   - Eritroblastosis fetalis: Rh- anne, Rh+ bebek tasirsa
     2. gebelikte annenin antikorlari bebege zarar verebilir

4. KAN NAKLI KURALLARI:
   - Ayni gruptan nakil en guvenlidir
   - O Rh- : Genel verici (acil durumlarda herkese verilebilir)
   - AB Rh+ : Genel alici (herkesten alabilir)

5. ORNEK CAPRAZLAMA:
   - Anne I^A i x Baba I^B i
   - Cocuklar: I^A I^B (AB), I^A i (A), I^B i (B), ii (O)
   - 4 farkli kan grubu cocuk olabilir
"""
},

"BIY.10.2.ESEYE_BAGLI_KALITIM": {
    "unite": "Kalitim",
    "baslik": "Eseye Bagli Kalitim ve Soy Agaci Analizi",
    "icerik": """
ESEYE BAGLI KALITIM:

1. CINSIYET KROMOZOMLARI:
   - Disi: XX (homogametik)
   - Erkek: XY (heterogametik)
   - Cinsiyeti belirleyen: BABA (X veya Y sperm)
   - X kromozomu Y'den DAHA BUYUK, daha fazla gen tasir

2. X'E BAGLI RESESIF KALITIM:
   - Gen X kromozomu uzerindedir
   - Erkeklerde TEK bir resesif allel bile fenotipi belirler (hemizigot)
   - Disilerde iki resesif allel olmali (homozigot resesif)
   - Tasiyici disi: X^A X^a (fenotipte saglikli, geni tasir)
   - Hasta erkek: X^a Y
   - Ornekler: Renk korlugu, hemofili, kas distrofisi

3. RENK KORLUGU ORNEGI:
   - X^R X^R : Normal disi
   - X^R X^r : Tasiyici disi (normal goruslu)
   - X^r X^r : Renk kor disi
   - X^R Y : Normal erkek
   - X^r Y : Renk kor erkek
   - Tasiyici anne x Normal baba -> Ogullarin %50'si renk kor

4. SOY AGACI ANALIZI:
   - Daire: Disi, Kare: Erkek
   - Dolu sembol: Hasta birey
   - Yari dolu: Tasiyici (X'e bagli resesif icin)
   - Yatay cizgi: Eslesme
   - Dikey cizgi: Cocuk
   - Otozomal dominant: Her nesilde hasta var
   - Otozomal resesif: Saglikli ebeveynlerden hasta cocuk olabilir
   - X'e bagli: Erkeklerde daha sik, baba -> kiz aktarir
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: DNA VE RNA YAPISI
# ═══════════════════════════════════════════════════════════════

"BIY.10.3.DNA_YAPISI": {
    "unite": "DNA ve RNA",
    "baslik": "DNA Yapisi ve Ozellikleri",
    "icerik": """
DNA YAPISI:

1. DNA (DEOKSIRIBO NUKLEIK ASIT):
   - Genetik bilgiyi tasir ve nesillere aktarir
   - CIFT SARMAL (double helix) yapidadir (Watson-Crick modeli, 1953)
   - Nukleotid: DNA'nin YAPI BIRIMI

2. NUKLEOTID YAPISI:
   - Fosfat grubu (H3PO4)
   - Seker: DEOKSIRIBOZ (5 karbonlu, bir OH eksik)
   - Azotlu organik baz:
     * PURINLER (cift halkali): Adenin (A), Guanin (G)
     * PIRIMIDINLER (tek halkali): Sitozin (C), Timin (T)

3. BAZ ESLEME KURALI (CHARGAFF KURALI):
   - A = T (iki hidrojen bagi ile baglanir)
   - G ≡ C (uc hidrojen bagi ile baglanir)
   - A + G = T + C (purin sayisi = pirimidin sayisi)
   - G-C bagi daha gucludur (3 H bagi), DNA'yi daha dayanikli kilar

4. DNA OZELLIKLERI:
   - Cekirdekte, mitokondride ve kloroplastta bulunur
   - Kendini ESLEYEBILIR (replikasyon)
   - Her canli turunun DNA'si BENZERSIZDIR
   - Insan DNA'si yaklasik 3,2 milyar baz cifti icerir
"""
},

"BIY.10.3.RNA_YAPISI": {
    "unite": "DNA ve RNA",
    "baslik": "RNA Yapisi ve Cesitleri",
    "icerik": """
RNA YAPISI:

1. RNA (RIBONUKLEIK ASIT):
   - Protein sentezinde gorev alir
   - TEK ZINCIR yapidadir (DNA'dan farkli)
   - DNA'daki bilgiyi ribozomlara tasir

2. DNA'DAN FARKLARI:
   - Sekeri: RIBOZ (deoksiriboz degil)
   - Baz: Timin yerine URASIL (U) bulunur
   - Tek zincirdir (cift sarmal degil)
   - Daha kisa omurludur
   - Kendini ESLEYEMEZ (DNA kalibiyla sentezlenir)

3. RNA CESITLERI:
   a) mRNA (mesajci RNA):
      - DNA'daki genetik bilgiyi kopyalar (transkripsiyon)
      - Bilgiyi cekirdekten ribozoma tasir
      - KODON: mRNA uzerindeki 3'lu baz dizisi
   b) tRNA (tasiyici RNA):
      - Amino asitleri ribozoma tasir
      - ANTIKODON: tRNA uzerindeki 3'lu baz dizisi (kodona eslesir)
      - Yonca yapragi seklinde
      - 20 cesit amino asit icin farkli tRNA'lar vardir
   c) rRNA (ribozomal RNA):
      - Ribozomun yapisal bilesenidir
      - Protein sentezinin GERCEKLESTIGI yerdir
      - En bol bulunan RNA turudur
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: PROTEIN SENTEZI
# ═══════════════════════════════════════════════════════════════

"BIY.10.4.REPLIKASYON": {
    "unite": "Protein Sentezi",
    "baslik": "DNA Replikasyonu (Eslesmesi)",
    "icerik": """
DNA REPLIKASYONU:

1. TANIM:
   - DNA'nin kendisinin bir kopyasini olusturmasi
   - Hucre bolunmesinden once (S evresinde) gerceklesir
   - YARI KORUNUMLU (semi-conservative) model

2. REPLIKASYON ADIMLARI:
   a) Helikaz enzimi DNA cift sarmali cozer (fermuar gibi acar)
   b) Her bir ana zincir KALIP gorevi gorur
   c) DNA polimeraz enzimi serbest nukleotidleri kaliba gore baglar
   d) A-T, G-C eslesmesi yapilir
   e) Iki yeni DNA molekulu olusur

3. YARI KORUNUMLU MODEL:
   - Her yeni DNA molekulunde:
     * BIR eski (ana) zincir
     * BIR yeni (sentezlenen) zincir
   - Meselson-Stahl deneyi ile kanitlanmistir (1958)

4. ONEMLI ENZIMLER:
   - Helikaz: Cift sarmali acar
   - DNA polimeraz: Yeni nukleotidleri baglar + hata duzeltir
   - Ligaz: DNA parcalarini birlestirir (Okazaki parcalari)
   - Primaz: RNA primeri sentezler (baslangic noktasi)

5. HATA DUZELTME:
   - DNA polimeraz %99,99 dogrulukla calisir
   - Hatali bazlari keser ve dogrusunu koyar
   - Duzeltilemeyen hatalar -> MUTASYON
"""
},

"BIY.10.4.TRANSKRIPSIYON_TRANSLASYON": {
    "unite": "Protein Sentezi",
    "baslik": "Transkripsiyon ve Translasyon",
    "icerik": """
PROTEIN SENTEZI (SANTRAL DOGMA):

DNA -> (transkripsiyon) -> mRNA -> (translasyon) -> PROTEIN

1. TRANSKRIPSIYON (YAZILIM):
   - DNA'daki genetik bilgi mRNA'ya kopyalanir
   - CEKIRDEKTE gerceklesir
   - RNA polimeraz enzimi gorev alir
   - Sadece DNA'nin BIR ZINCIRI (kalip/anlamlı zincir) okunur
   - A->U, T->A, G->C, C->G (RNA'da Timin yok, Urasil var)
   - Sonuc: mRNA olusur, cekirdek porundan sitoplazmaya cikar

2. TRANSLASYON (CEVIRME):
   - mRNA'daki bilgi amino asit dizisine cevrilir
   - RIBOZOMDA (sitoplazmada) gerceklesir
   - KODON: mRNA uzerindeki 3'lu baz dizisi -> 1 amino asit kodlar
   - ANTIKODON: tRNA uzerindeki eslesen 3'lu baz dizisi

3. TRANSLASYON ADIMLARI:
   a) Baslama: Ribozom mRNA'ya baglanir, AUG (baslatici kodon) bulunur
   b) Uzama: tRNA amino asitleri getirir, peptit bagi olusur
   c) Sonlanma: DUR kodonu (UAA, UAG, UGA) gelince sentez biter
   d) Polipeptit zinciri olusur -> katlanarak PROTEIN olur

4. GENETIK KOD OZELLIKLERI:
   - UNIVERSALDIR: Tum canlilarda ayni kodlar ayni amino asidi kodlar
   - DEJENERE/YEDEKLI: Birden fazla kodon ayni amino asidi kodlayabilir
   - 4^3 = 64 kodon vardir (61'i amino asit, 3'u dur kodonu)
   - AUG: Hem baslatici kodon, hem metiyonin amino asidini kodlar
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: MUTASYON VE GENETIK MUHENDISLIK
# ═══════════════════════════════════════════════════════════════

"BIY.10.5.MUTASYON": {
    "unite": "Mutasyon ve Genetik Muhendislik",
    "baslik": "Mutasyon Cesitleri ve Etkileri",
    "icerik": """
MUTASYON:

1. TANIM:
   - DNA'daki baz dizisinde meydana gelen KALICI degisiklikler
   - Kendilginden (spontan) veya disaridan (induklenmiş) olusabilir
   - Evrimde cesitliligin TEMEL kaynagi

2. GEN MUTASYONLARI (NOKTA MUTASYONU):
   a) Baz degisimi (substitusyon):
      - Bir baz yerine baska baz gelir
      - Sessiz mutasyon: Amino asit degismez (dejenere kodon)
      - Yanlis anlamli (missense): Farkli amino asit kodlanir
      - Anlamsiz (nonsense): Dur kodonu olusur, protein kisalir
   b) Ekleme (insersiyon): Fazladan baz eklenir
   c) Cikarilma (delesyon): Baz kaybi olur
   - Ekleme/cikarilma -> CERCEVE KAYMASI mutasyonu (en zararli)

3. KROMOZOM MUTASYONLARI:
   a) Yapi mutasyonlari:
      - Delesyon: Kromozom parcasi kopup kaybolur
      - Duplikasyon: Bir bolge tekrarlanir
      - Inversiyon: Bir bolge ters doner
      - Translokasyon: Parcalar farkli kromozomlara tasinir
   b) Sayi mutasyonlari:
      - Anoploid: Tek kromozom fazla/eksik (2n+1, 2n-1)
      - Poliploid: Tam takim kromozom fazla (3n, 4n)
      - Down sendromu: 21. kromozom trizomisi (2n+1 = 47)

4. MUTAJENLER:
   - Kimyasal: Sigara dumani, boya maddeleri, bazi ilaclar
   - Fiziksel: UV isinlari, X isinlari, radyoaktif maddeler
   - Biyolojik: Bazi virusler (HPV -> serviks kanseri)
"""
},

"BIY.10.5.GENETIK_MUHENDISLIK": {
    "unite": "Mutasyon ve Genetik Muhendislik",
    "baslik": "Genetik Muhendislik ve Biyoteknoloji",
    "icerik": """
GENETIK MUHENDISLIK:

1. TANIM:
   - Canlilarin genetik yapisinin BILINÇLI olarak degistirilmesi
   - Rekombinant DNA teknolojisi kullanilir
   - Bir canlinin genini baska bir canliya aktarma

2. TEMEL TEKNIKLER:
   a) Restriksiyon enzimleri: DNA'yi belirli noktalardan keser
   b) DNA ligaz: DNA parcalarini birlestirir
   c) Vektor (tasiyici): Gen aktariminda kullanilir (plazmid, virus)
   d) PCR (Polimeraz Zincir Reaksiyonu): DNA'yi cogaltma
   e) Gel elektroforez: DNA parcalarini boyutlarina gore ayirma

3. UYGULAMA ALANLARI:
   a) TIP:
      - Insulin uretimi (E. coli bakterisinde insan insulin geni)
      - Gen tedavisi: Bozuk genin saglam kopyasiyla degistirilmesi
      - Asi uretimi (Hepatit B)
      - Tani: Genetik hastalik taramasi
   b) TARIM:
      - GDO (Genetigi Degistirilmis Organizma)
      - Zararlilara dayanikli bitkiler (Bt misir)
      - Verimi arttirilmiş bitkiler
      - Altin pirinc (beta-karoten zenginlestirilmis)
   c) ENDUSTRI:
      - Biyoyakit uretimi
      - Enzim uretimi (deterjan, gida)
      - Biyoplastik

4. DNA PARMAK IZI:
   - Her bireyin DNA'si benzersizdir (tek yumurta ikizleri haric)
   - Adli tip, babalik testi, suc arastirmasi
   - STR (Kisa Tekrar Dizisi) analizi kullanilir

5. ETIK TARTISMALAR:
   - GDO guvenligi ve cevresel etkiler
   - Insan klonlama yasagi
   - Gen tedavisinin sinirlari
   - Tasarlanmiş bebekler tartismasi
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_biyoloji10_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in BIYOLOJI_10_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_biyoloji10_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(BIYOLOJI_10_REFERANS.keys())
