# -*- coding: utf-8 -*-
"""
12. Sinif Biyoloji dersi (AYT)
MEB 2025 mufredatina uygun DOGRU referans verileri.
AYT duzeyi icerikleri kapsar.

Uniteler:
1. Bitki Biyolojisi
2. Hayvan Biyolojisi (Canlilar Fizyolojisi)
3. Topluluk Ekolojisi
4. Evrim
5. Biyoteknoloji ve Genetik Muhendisligi
"""

BIYOLOJI_12_REFERANS = {

# ===============================================================
# 1. UNITE: BITKI BIYOLOJISI
# ===============================================================

"BIY.12.1.KOK_GOVDE_YAPRAK_YAPISI": {
    "unite": "Bitki Biyolojisi",
    "baslik": "Kok, Govde ve Yaprak Yapisi",
    "icerik": """
KOK, GOVDE VE YAPRAK YAPISI:

1. KOK YAPISI:
   - Bitkiyi topraga baglar, su ve mineral emilimini saglar
   - Epidermis: En dis tabaka, kok tuyleri burada bulunur
   - Korteks: Besin depolama ve madde iletimi
   - Endodermis: Kaspari seridi icerir, secici gecirgenlik saglar
   - Periskl: Yan koklerin olusumu burada baslar
   - Iletim demeti: Ksilem (su + mineral) icte, Floem (organik besin) dista
   - Tek cenetli koklerde iletim demetleri halka seklinde dizilir
   - Cift cenetli koklerde kambiyum bulunur, sekonder buyume gorulur

2. GOVDE YAPISI:
   - Toprak ustu organ, madde iletimi ve destek saglar
   - Tek cenetli govde: Iletim demetleri dagnik dizilir, kambiyum YOK
   - Cift cenetli govde: Iletim demetleri halka seklinde, kambiyum VAR
   - Ksilem: Su ve mineralleri kokten yapraga tasir (olu hucre, tek yon)
   - Floem: Organik besinleri yapraktan diger organlara tasir (canli, cift yon)
   - Kambiyum: Sekonder buyumeyi saglar (kalinlasma), yillik halka olusturur

3. YAPRAK YAPISI:
   - Fotosentezin ana organi
   - Ust epidermis: Kutikula tabakasi ile kapli (su kaybi onler)
   - Palizat parankimasi: Ust yuzde, silindirik hucreler, bol kloroplast, fotosentez yogun
   - Sunger parankimasi: Alt yuzde, duzensiz, hucreler arasi bosluklari fazla, gaz alisverisi
   - Alt epidermis: Stomalar (goz hucreleri) bulunur
   - Iletim demetleri: Yaprak damarlari (ksilem + floem)
   - Stoma: Gaz alisverisi ve terleme, bekci (goz) hucreleri ile acilir-kapanir
"""
},

"BIY.12.1.FOTOSENTEZ_ISIK_REAKSIYONLARI": {
    "unite": "Bitki Biyolojisi",
    "baslik": "Fotosentez - Isik Reaksiyonlari (Isiga Bagimli)",
    "icerik": """
FOTOSENTEZ - ISIK REAKSIYONLARI:

1. FOTOSENTEZ GENEL FORMULU:
   6CO2 + 6H2O + Isik Enerjisi -> C6H12O6 + 6O2
   - Isik enerjisi kimyasal enerjiye donusturulur
   - Gerceklestigi organel: KLOROPLAST

2. KLOROPLAST YAPISI:
   - Dis zar ve ic zar (cift zarli organel)
   - Tilakoit: Ic zar sistemi, disk seklinde yapilar
   - Granum: Ust uste yigilmis tilakoit diskleri
   - Stroma: Kloroplastin ic sivisi (karanlik reaksiyonlar burada)
   - Tilakoit zar: Klorofil ve diger pigmentler burada (isik reaksiyonlari)

3. ISIK REAKSIYONLARI (ISIGA BAGIMLI):
   - Gerceklestigi yer: Tilakoit ZARINDA
   - Isik enerjisi gereklidir

   a) Fotosistem II (PSII):
      - Klorofil isik enerjisi emerek uyarilir
      - Su molekulu parcalanir (FOTOLIZ): 2H2O -> 4H+ + 4e- + O2
      - Aciga cikan O2 atmosfere verilir (fotosentez urunu)
      - Elektronlar elektron tasima zincirine aktarilir

   b) Elektron Tasima Zinciri (ETZ):
      - Elektronlar PSII'den PSI'e tasinir
      - Bu sirada protonlar (H+) tilakoit ic bosluguna pompalanir
      - Proton gradyenti (kemiozmoz) olusur

   c) Fotosistem I (PSI):
      - Elektronlar tekrar uyarilir
      - NADP+ + 2H+ + 2e- -> NADPH (indirgenme gucu)

   d) Kemiozmoz ve ATP Sentezi:
      - Proton gradyenti ATP sentaz enziminden gecerek ATP uretir
      - ADP + Pi -> ATP (fosforilasyon)

4. ISIK REAKSIYONLARININ URUNLERI:
   - ATP (enerji)
   - NADPH (indirgenme gucu / hidrojen tasiyici)
   - O2 (suyun fotolizinden)
   - Bu urunlerden ATP ve NADPH karanlik reaksiyonlarda kullanilir
"""
},

"BIY.12.1.FOTOSENTEZ_KARANLIK_REAKSIYONLAR": {
    "unite": "Bitki Biyolojisi",
    "baslik": "Fotosentez - Calvin Dongusu (Karbon Reaksiyonlari)",
    "icerik": """
CALVIN DONGUSU (KARANLIK / KARBON REAKSIYONLARI):

1. GENEL BILGI:
   - Gerceklestigi yer: Kloroplastin STROMASINDA
   - Isiga dogrudan bagimli DEGILDIR (ama isik reaksiyonlarinin urunlerine bagimlidir)
   - CO2'nin organik bilesige donusturulmesi (karbon fiksasyonu)
   - ATP ve NADPH tuketilir (isik reaksiyonlarindan gelir)

2. CALVIN DONGUSUNUN ASAMALARI:

   a) Karbon Fiksasyonu:
      - CO2 + RuBP (5C) -> 2 molekul 3-fosfogliserat (3PG) (3C)
      - RuBisCO enzimi katalizler (dunyada en bol enzim)
      - 6 CO2 girisi icin 6 RuBP gerekir

   b) Indirgeme:
      - 3PG (3C) -> G3P (3C) donusumu
      - ATP enerji verir, NADPH hidrojen verir
      - 6 CO2 icin: 12 ATP + 12 NADPH harcanir

   c) RuBP Yenilenmesi:
      - 12 G3P'den 10 tanesi RuBP'ye geri donusturulur
      - 2 G3P net kazanctir -> Glikoz sentezinde kullanilir
      - 6 ATP harcanir (RuBP yenilenmesi icin)

3. GENEL MUHASEBE (1 GLIKOZ ICIN):
   - 6 CO2 sabitlenir
   - 18 ATP harcanir (12 indirgeme + 6 yenilenme)
   - 12 NADPH harcanir
   - 1 Glikoz (C6H12O6) uretilir

4. STOMA VE GAZ ALISVERISI:
   - Stomalar acildiginda: CO2 girer, O2 cikar
   - Stomalar kapandiginda: Fotosentez yavaslar (CO2 azalir)
   - Goz hucreleri turgor basincina gore acilip kapanir
   - Kurak ortamda stomalar kapanir -> CO2 azalir -> Fotosentez duser
   - C4 ve CAM bitkileri: Stoma sorunu icin ozel adaptasyonlar

5. FOTOSENTEZ HIZINI ETKILEYEN FAKTORLER (AYT):
   - Isik siddeti (arttikca hiz artar, doyma noktasina kadar)
   - CO2 yogunlugu (arttikca hiz artar, doyma noktasina kadar)
   - Sicaklik (enzim aktivitesini etkiler, optimum sicaklik)
   - Su miktari (yetersiz su -> stoma kapanir -> CO2 giremez)
   - Klorofil miktari (sari yapraklarda fotosentez dusuk)
   - Sinirlandirici faktor ilkesi: En dusuk olan faktor hizi belirler
"""
},

# ===============================================================
# 2. UNITE: HAYVAN BIYOLOJISI (CANLILAR FIZYOLOJISI)
# ===============================================================

"BIY.12.2.HOMEOSTAZI": {
    "unite": "Hayvan Biyolojisi",
    "baslik": "Homeostazi ve Geri Bildirim Mekanizmalari",
    "icerik": """
HOMEOSTAZI:

1. HOMEOSTAZI TANIMI:
   - Ic ortamin (vucut ici) sabit ve dengede tutulmasidir
   - Canli organizmalarin en temel ozelliklerinden biri
   - Dis ortam degisse bile ic ortam belirli sinirlar icinde tutulur
   - Ornek: Vucut sicakligi, kan sekeri, pH, su-tuz dengesi

2. GERI BILDIRIM MEKANIZMALARI:

   a) Negatif Geri Bildirim (En yaygin):
      - Sapmayi duzeltir, dengeye dondurur
      - Ornek 1: Kan sekeri yukselir -> Pankreastan insulin salgilanir ->
        Glikoz hucrelere alinir -> Kan sekeri duser -> Normal seviye
      - Ornek 2: Kan sekeri duser -> Pankreastan glukagon salgilanir ->
        Karacigerde glikojen parcalanir -> Kan sekeri yukselir -> Normal seviye
      - Ornek 3: Vucut sicakligi artarsa -> Terleme artar, damarlar genisler -> Soguma

   b) Pozitif Geri Bildirim (Nadir):
      - Sapmayi arttirir, belirli bir amaca ulasana kadar devam eder
      - Ornek 1: Dogum sirasinda oksitosin salgisi -> Kasilmalar artar -> Daha fazla oksitosin
      - Ornek 2: Kan pihtilasma kaskadi

3. HOMEOSTATIK KONTROL ELEMANLARI:
   - Reseptor (algilayici): Degisimi algilar
   - Kontrol merkezi: Bilgiyi degerlendirir, uygun tepkiyi belirler
   - Efektor: Tepkiyi gerceklestirir (kas, bez vb.)
   - Ornek: Sicaklik artisi -> Deri reseptorleri algilar -> Hipotalamus degerlendirir ->
     Ter bezleri (efektor) aktive edilir

4. HORMONLAR VE HOMEOSTAZI:
   - Insulin: Kan sekerini DUSURUR (pankreas beta hucreleri)
   - Glukagon: Kan sekerini YUKSELTIR (pankreas alfa hucreleri)
   - ADH (antidiuretik hormon): Su geri emilimini artirir (hipofiz)
   - Aldosteron: Na+ geri emilimi, K+ atilimi (bobrek ustu bezi)
   - Tiroksin: Metabolizma hizini duzenler (tiroit bezi)
"""
},

"BIY.12.2.TERMOREGULASYON": {
    "unite": "Hayvan Biyolojisi",
    "baslik": "Termoregulasyon - Vucut Sicakligi Duzenlenmesi",
    "icerik": """
TERMOREGULASYON:

1. TANIM:
   - Vucut sicakliginin belirli sinirlar icinde tutulmasidir
   - Kontrol merkezi: HIPOTALAMUS
   - Insan vucut sicakligi: Yaklasik 36,5-37,5 derece (ortalama 37 derece)

2. SICAKKANLI (ENDOTERMLER) vs SOGUKKANLI (EKTOTERMLER):

   a) Sicakkanli (Endoterm) Canlilar:
      - Vucut sicakligini metabolizma ile sabit tutar
      - Dis ortam degisse bile ic sicaklik sabit
      - Memeliler ve kuslar
      - Avantaj: Her iklimde aktif olabilir
      - Dezavantaj: Yuksek enerji tuketimi

   b) Sogukkanli (Ektoterm) Canlilar:
      - Vucut sicakligi dis ortama gore degisir
      - Surungen, amfibi, balik, omurgasizlar
      - Avantaj: Dusuk enerji tuketimi
      - Dezavantaj: Soguk havalarda aktivite azalir (kis uykusu)

3. SOGUKTA VUCUT TEPKILERI:
   - Damar buzusmesi (vazokonstriksiyon): Deri yuzeyinden isi kaybi azalir
   - Titreme: Kas kasilmalari ile isi uretimi artar
   - Kilpikinesi (tuy diklenme): Hava katmani olusturma (insanda etkisiz)
   - Metabolizma hizi artar: Tiroksin salgisi artar
   - Kahverengi yag dokusu: Ozellikle bebeklerde isi uretimi

4. SICAKTA VUCUT TEPKILERI:
   - Damar genislemesi (vazodilatasyon): Deri yuzeyinden isi kaybi artar
   - Terleme: Suyun buharlasmasiyla soguma
   - Metabolizma hizi azalir
   - Davranissal tepkiler: Golge arama, su icme

5. ATES (AYT ONEMLI):
   - Enfeksiyon durumunda hipotalamus set noktasini yukseltir
   - Vucut bu yeni set noktasina ulasmak icin titremeye baslar
   - Amac: Yuksek sicaklik patojenlerin cogalmasini yavaslatir
   - Ates dusurucu ilaclar set noktasini normale dondurur
"""
},

"BIY.12.2.OSMOREGULASYON": {
    "unite": "Hayvan Biyolojisi",
    "baslik": "Osmoregulasyon - Su ve Tuz Dengesi",
    "icerik": """
OSMOREGULASYON:

1. TANIM:
   - Vucut sivilarindaki su ve cozunmus madde (tuz, mineral) dengesinin duzenlenmesidir
   - Hucrelerin saglikli calisabilmesi icin ozmotik basincin sabit tutulmasi
   - Ana organ: BOBREKLER
   - Duzenleyici hormonlar: ADH, Aldosteron

2. BOBREK YAPISI VE ISLEYISI:
   - Nefron: Bobregin yapisal ve islevsel birimi
   - Bowman kapsulu: Kanin suzulmesi (glomerulus filtrasyon)
   - Proksimal tubul: Glikoz, aminoasit, Na+ geri emilimi
   - Henle kulpu: Su ve tuz geri emilimi (konsantrasyon gradyenti olusturur)
   - Distal tubul: Ince ayar (ADH ve aldosteron etkisi)
   - Toplama kanali: Son su geri emilimi (ADH etkisi ile)
   - Sonuc: Idrar olusumu

3. ADH (ANTIDIURETIK HORMON):
   - Salgilayan: Hipofiz bezi (hipotalamusun kontrolunde)
   - Gorevi: Toplama kanallarindan su geri emilimini ARTIRIR
   - Su kaybi fazla / kan ozmotik basinci yuksek -> ADH ARTAR -> Idrar azalir, yogunlasir
   - Su fazla alindiysa / kan ozmotik basinci dusuk -> ADH AZALIR -> Idrar artar, seyrellir
   - Alkol ADH salgilanmasini baskilar -> Idrar uretimi artar -> Dehidratasyon

4. ALDOSTERON:
   - Salgilayan: Bobrek ustu (adrenal) bezi
   - Gorevi: Bobreklerden Na+ geri emilimini artirir, K+ atilimini artirir
   - Na+ geri emildikce su da takip eder -> Kan hacmi artar -> Kan basinci artar

5. FARKLI ORTAMLARDA OSMOREGULASYON:
   - Tatli su baliklari: Vucut hiperton -> Su surekli girer -> Bol seyreltik idrar
   - Tuzlu su baliklari: Vucut hipoton -> Su surekli cikar -> Az yogun idrar, tuz atilimi (solungac)
   - Col hayvanlari: Su tasarrufu adaptasyonu -> Yogun idrar, az terleme
"""
},

# ===============================================================
# 3. UNITE: TOPLULUK EKOLOJISI
# ===============================================================

"BIY.12.3.POPULASYON_DINAMIKLERI": {
    "unite": "Topluluk Ekolojisi",
    "baslik": "Populasyon Dinamikleri ve Buyume Modelleri",
    "icerik": """
POPULASYON DINAMIKLERI:

1. POPULASYON TANIMI:
   - Belirli bir alanda, belirli bir zamanda yasayan ayni tur bireylerin toplulugu
   - Populasyon ekolojisi: Populasyonlarin buyumesi, dagilimi, yogunlugu inceler

2. POPULASYON OZELLIKLERI:
   - Populasyon buyuklugu (N): Birey sayisi
   - Populasyon yogunlugu: Birey sayisi / Alan
   - Yas yapisi: Ureme oncesi, ureme caginda, ureme sonrasi oranlari
   - Cinsiyet orani: Disi/Erkek orani
   - Dagilim sekli: Kumeli, duzgun (uniform), rastgele

3. POPULASYON BUYUME MODELLERI:

   a) Ustel (Eksponansiyel) Buyume:
      - Sinirlandirici faktor yok -> J-egrisi
      - dN/dt = r x N (r: dogal artis orani)
      - Ideal kosullar: Bol besin, predator yok, hastalik yok
      - Dogada nadirdir, yeni kolonize edilen ortamlarda kisa sureli gorulur

   b) Lojistik Buyume:
      - Sinirlandirici faktorler devreye girer -> S-egrisi (sigmoid)
      - dN/dt = r x N x (K-N)/K
      - K: Tasima kapasitesi (cevre direnci)
      - Populasyon K degerine yaklastikca buyume yavaslar
      - K degerinde: Dogum orani = Olum orani (denge)

4. POPULASYONU SINIRLANDIRAN FAKTORLER:
   - Yogunluga bagli: Rekabet, hastalik, predatorluk, parazitizm
   - Yogunluktan bagimsiz: Iklim degisiklikleri, dogal afetler, yanginlar
   - Tasima kapasitesi (K): Ortamin destekleyebilecegi maksimum birey sayisi

5. r-SECILIMI vs K-SECILIMI:
   - r-secilimi turler: Cok yavru, az ebeveyn bakimi, kisa omur (bocekler, bakteriler)
   - K-secilimi turler: Az yavru, cok ebeveyn bakimi, uzun omur (filler, insanlar)
"""
},

"BIY.12.3.TURLER_ARASI_ILISKILER": {
    "unite": "Topluluk Ekolojisi",
    "baslik": "Turler Arasi Iliskiler (Simbiyotik ve Diger)",
    "icerik": """
TURLER ARASI ILISKILER:

1. MUTUALIZM (Karsilikli Faydacilik) (+/+):
   - Her iki tur de fayda gorur
   - Zorunlu mutualizm: Birbirleri olmadan yasamazlar
     * Liken: Alg + Mantar (alg fotosentez yapar, mantar nem ve mineral saglar)
     * Mikorizalar: Bitki kokleri + Mantarlar (mineral alimi artar)
   - Ihtiyari mutualizm: Birlikte yasarlar ama ayri da yasayabilirler
     * Balik + Temizlikci balik
     * Bitki + Tozlastirici bocek

2. PARAZITIZM (+/-):
   - Parazit fayda gorur, konak zarar gorur
   - Dis parazitler (ektoparazit): Pire, bit, kene
   - Ic parazitler (endoparazit): Tenya, sivrisinek larvasi
   - Parazit genellikle konagi OLDURMEZ (olurse kendisi de olur)
   - Parazitoidler: Konagi sonunda oldurur (bazi aribotu turleri)

3. PREDATORLUK (Avci-Av Iliskisi) (+/-):
   - Predator (avci) avini yakalar ve yer
   - Populasyon dengesini saglar
   - Lotka-Volterra modeli: Avci ve av populasyonlari dongusel dalgalanir
   - Av artarsa -> Avci artar -> Av azalir -> Avci azalir -> Av tekrar artar
   - Ornek: Vasak (avci) - Kar tavsani (av)
   - Avlarin savunma mekanizmalari: Kamuflaj, aposematizm (uyari rengi), mimikri

4. KOMENSALIZM (+/0):
   - Bir tur fayda gorur, diger etkilenmez
   - Ornek: Kopekbaligi + Yapisan balik (remora)
   - Ornek: Agacin uzerinde yasayan epifit bitkiler (orkide)
   - Ornek: Aslan avladiktan sonra akbaba artiklari yer

5. REKABET (-/-):
   - Her iki tur de zarar gorur (kaynak paylasimi)
   - Turler arasi rekabet: Farkli turler ayni kaynagi kullanir
   - Rekabetci dislanma ilkesi (Gause): Ayni nisi paylasan iki tur birlikte yasamaz
   - Kaynak paylasimi / nis ayrimi: Rekabeti azaltma stratejisi

6. AMENSALIZM (-/0):
   - Bir tur zarar gorur, diger etkilenmez
   - Ornek: Buyuk agacin golgesinde kalan kucuk bitkinin isik alamamasi
   - Ornek: Ceviz agacinin topraga saldigi kimyasallar diger bitkileri engeller (allelopati)
"""
},

# ===============================================================
# 4. UNITE: EVRIM
# ===============================================================

"BIY.12.4.DARWIN_VE_DOGAL_SECILIM": {
    "unite": "Evrim",
    "baslik": "Darwin ve Dogal Secilim Mekanizmasi",
    "icerik": """
DARWIN VE DOGAL SECILIM:

1. CHARLES DARWIN (1809-1882):
   - HMS Beagle gezisi (1831-1836) -> Galapagos Adalari
   - "Turlerin Kokeni" (1859) kitabinda dogal secilimi acikladi
   - Alfred Russel Wallace da benzer fikirlere bagimsiz olarak ulasti

2. DOGAL SECILIM MEKANIZMASI:
   - Populasyonda bireyler arasi genetik cesitlilik vardir (varyasyon)
   - Kaynaklar sinirlidir -> Bireyler arasi yasam mucadelesi (rekabet)
   - Cevre kosullarina daha uygun bireyler hayatta kalir ve ureme sansi yuksek
   - Bu bireyler genlerini sonraki nesillere aktarir
   - Zaman icinde populasyonun genotip ve fenotip frekanslari degisir
   - ONEMLI: Dogal secilim bireyi DEGISTIRMEZ, populasyonun gen frekanslarini degistirir

3. DOGAL SECILIM CESITLERI:
   a) Yonlu (Directional) Secilim:
      - Bir uc fenotip favore edilir, ortalama kayar
      - Ornek: Endustriyel melanizm (koyu kelebekler kirli ortamda avantajli)

   b) Dengeleyici (Stabilizing) Secilim:
      - Ortalama fenotip favore edilir, uc fenotipler elenir
      - Ornek: Insan bebek dogum agirligi

   c) Ayristirici (Disruptive) Secilim:
      - Her iki uc fenotip favore edilir, ortalama elenir
      - Turlesmeye yol acabilir

4. CINSEL SECILIM:
   - Es seciminde avantaj saglayan ozelliklerin secilmesi
   - Ornek: Tavuskusu kuyrugu, aslan yelesi

5. YAPAY SECILIM:
   - Insanlarin istenen ozelliklere sahip bireyleri secip cogaltmasi
   - Ornekler: Kopek irklari, tarimsal urunler, sut verimi yuksek inekler
"""
},

"BIY.12.4.EVRIM_KANITLARI": {
    "unite": "Evrim",
    "baslik": "Evrim Kanitlari",
    "icerik": """
EVRIM KANITLARI:

1. FOSIL KANITLARI:
   - Fosil: Gecmiste yasamis canlilarin kalintilari veya izleri
   - Gecis formlari: Iki grup arasindaki ara ozelliklere sahip fosiller
     * Archaeopteryx: Surungenler ile kuslar arasi (dis, pence + tuy, kanat)
     * Tiktaalik: Balik ile amfibiler arasi (yuzgec + bacak ozellikleri)
   - Fosil tabakalarinda asagidan yukariya: Basit -> Karmasik canlilar
   - Radyometrik tarihlendirme: Fosillerin yasini belirler (C-14, K-Ar, U-Pb)

2. KARSILASTIRMALI ANATOMI:
   a) Homolog Organlar:
      - Koken ayni, islev farkli
      - Ortak atadan miras alinmis, farkli ortamlara uyum saglamis
      - Ornek: Insan kolu, yarasa kanadi, balina yuzgeci, at bacagi -> Hepsi ayni kemik yapisi
      - IRAKSAK (Diverjant) evrim kaniti

   b) Analog Organlar:
      - Koken farkli, islev ayni
      - Ortak ata DEGIL, benzer cevre kosullarina uyum
      - Ornek: Kus kanadi (kemikli) ve bocek kanadi (kitinden)
      - YAKINLASMA (Konverjant) evrim kaniti -> Akrabalik GOSTERMEZ

   c) Kalinti (Vestigial) Organlar:
      - Islevini yitirmis ama hala mevcut yapilar
      - Ornek: Insanda apandis, kucuk kulak kaslari, kuyruk sokumu kemigi
      - Balinalarda arka bacak kalintilari

3. EMBRIYOLOJI KANITLARI:
   - Farkli omurgalilarin embriyolari erken donemde birbirine cok benzer
   - Solungac yariklari, kuyruk yapilari ortak
   - Ortak atadan gelen genlerin embriyonik gelisimi yonlendirmesi

4. BIYOKIMYASAL (MOLEKULER) KANITLAR:
   - Tum canlilarda ortak biyomolekuller: DNA, RNA, protein, ATP
   - DNA dizi karsilastirmasi: Yakin akraba turler daha benzer dizilere sahip
   - Insan-sempanze DNA benzerligi: ~%98,7
   - Sitokrom c proteini: Tum aerobik canlilar kullanir
   - Evrensel genetik kod: Tum canlilarda ayni kodonlar ayni aminoasitleri sifrelir

5. BIYOCOGRAFYA KANITLARI:
   - Ada turlerinin anakaraya yakin ama benzersiz olmasi
   - Galapagos ispinozlari: Her adada farkli gaga yapisi (uyumsal yayilim)
   - Avustralya'nin kendine ozgu keseli memelileri (kitasal izolasyon)
"""
},

"BIY.12.4.TURLESME_VE_ADAPTASYON": {
    "unite": "Evrim",
    "baslik": "Turlesme, Adaptasyon ve Evrimsel Mekanizmalar",
    "icerik": """
TURLESME VE ADAPTASYON:

1. TUR TANIMI:
   - Biyolojik tur kavrami: Dogal kosullarda birbirleriyle ciftlesip verimli
     yavrular olusturabilen bireyler toplulugu
   - Ureme izolasyonu: Farkli turler arasinda gen akisi engellenir

2. TURLESME YOLLARI:

   a) Allopatrik Turlesme (Cografik izolasyon):
      - Populasyon fiziksel bir engelle (dag, nehir, okyanus) ikiye ayrilir
      - Her iki grup farkli cevre kosullarinda farkli yonlerde evrimlenir
      - Yeterli zaman gecince -> Ureme izolasyonu olusur -> Yeni tur
      - Ornek: Galapagos ispinozlari, Grand Kanyon sincaplari

   b) Simpatrik Turlesme (Cografik izolasyon olmadan):
      - Ayni alanda yasamaya devam ederek turlesme
      - Poliploidi (kromozom sayisi artisi) -> Ozellikle bitkilerde yaygin
      - Habitat farklilasmasi veya zamansal izolasyon

3. UREME IZOLASYON MEKANIZMALARI:
   a) Zigot oncesi bariyerler:
      - Habitat izolasyonu, zamansal izolasyon, davranissal izolasyon
      - Mekanik izolasyon, gametik izolasyon

   b) Zigot sonrasi bariyerler:
      - Melez cansizilik, melez kisirligi (katir = at x esek), melez cokuntusu

4. ADAPTASYON:
   - Canlilarin cevre kosullarina uyum saglamasidir
   - Yapisal adaptasyon: Kutup ayisinin kalin kurk, kaktusun dikeni
   - Fizyolojik adaptasyon: Col farelerinin yogun idrar uretimi
   - Davranissal adaptasyon: Goc, kis uykusu, gece avlanma
   - Adaptasyon bir amac DEGILDIR -> Dogal secilimin SONUCUDUR

5. UYUMSAL YAYILIM (ADAPTIVE RADIATION):
   - Bir turden birden fazla tur olusumasi (farkli nislere uyum)
   - Ornek: Darwin'in ispinozlari, Havai bal arisi kuslari
   - Genellikle yeni ortama geciste veya toplu yokolus sonrasi gorulur
"""
},

# ===============================================================
# 5. UNITE: BIYOTEKNOLOJI VE GENETIK MUHENDISLIGI
# ===============================================================

"BIY.12.5.GEN_KLONLAMA_VE_GDO": {
    "unite": "Biyoteknoloji ve Genetik Muhendisligi",
    "baslik": "Gen Klonlama, GDO ve Rekombinant DNA Teknolojisi",
    "icerik": """
GEN KLONLAMA VE GDO:

1. BIYOTEKNOLOJI TANIMI:
   - Canlilarin veya biyolojik sistemlerin urun ve hizmet uretmek icin kullanilmasi
   - Geleneksel biyoteknoloji: Ekmek, peynir, yogurt, sarap yapimi
   - Modern biyoteknoloji: Genetik muhendisligi, gen terapisi, klonlama

2. REKOMBINANT DNA TEKNOLOJISI:
   - Farkli canlilardan alinan DNA parcalarinin birlestirilmesi
   - Asamalar:
     a) Istenilen gen belirlenir ve izole edilir
     b) Restriksiyon enzimleri ile DNA kesilir (yapistirici uclar olusur)
     c) Vektor (plazmid, virus) secilir ve ayni enzimle kesilir
     d) DNA ligaz enzimi ile gen vektore yapistiriilir
     e) Vektor konak hucreye aktarilir (transformasyon)
     f) Konak hucre cogalir, istenilen protein uretilir

3. GDO (GENETIGI DEGISTIRILMIS ORGANIZMA):
   - Baska bir turden gen aktarilmis canli organizma
   - Ornekler:
     * Bt misir/pamuk: Bacillus thuringiensis geni -> Bocek direnci
     * Altin pirinc: Beta-karoten ureten gen -> A vitamini zenginlestirme
     * Herbisit direncli soya: Yabani ot ilacina dayanikli
   - Avantajlari: Verim artisi, vitamin zenginlestirme, ilac direnci
   - Riskleri: Alerji, biyocesitlilik etkisi, etik sorunlar, gen kacisi

4. GEN KLONLAMA:
   - Belirli bir genin cok sayida kopyasinin uretilmesi
   - Vektor: Genin tasinmasinda kullanilir (plazmid en yaygin)
   - Plazmid: Bakteri hucresinde bulunan halkasal DNA (kolay manipule edilir)

5. ILAC URETIMI ORNEKLERI:
   - Insan insulini: E. coli bakterisine insan insulin geni aktarildi (1982)
   - Buyume hormonu (HGH): Rekombinant olarak uretilir
   - Hepatit B asisi: Rekombinant protein asisi
"""
},

"BIY.12.5.PCR_VE_DNA_PARMAK_IZI": {
    "unite": "Biyoteknoloji ve Genetik Muhendisligi",
    "baslik": "PCR, DNA Parmak Izi ve Jel Elektroforez",
    "icerik": """
PCR VE DNA PARMAK IZI:

1. PCR (POLIMERAZ ZINCIR REAKSIYONU):
   - Cok az miktardaki DNA'nin milyonlarca kopyasini uretme teknigi
   - Kary Mullis tarafindan gelistirildi (1983, Nobel Odulu 1993)

   Asamalar (her dongu):
   a) Denaturasyon (94-98 derece): Cift iplikli DNA tek iplige ayrilir
   b) Baglanma (50-65 derece): Primerler tek iplikli DNA'ya baglanir
   c) Uzama (72 derece): Taq polimeraz enzimi yeni ipligi sentezler

   - Taq polimeraz: Thermus aquaticus (sicak su kaynagi) bakterisinden
   - Her dongu DNA miktarini 2 katina cikarir -> 30 dongu = yaklasik 1 milyar kopya
   - Kullanim alanlari: Adli tip, babalik testi, hastalik tanisi, fosil DNA

2. JEL ELEKTROFOREZ:
   - DNA parcalarini boyutlarina gore ayirma teknigi
   - Agaroz jel icinden elektrik akimi gecirilir
   - DNA negatif yuklu -> Pozitif kutba dogru hareket eder
   - Kucuk parcalar daha hizli, buyuk parcalar daha yavas hareket eder
   - Sonuc: DNA parcalari boyutlarina gore bant halinde ayrilir

3. DNA PARMAK IZI (DNA PROFILLEME):
   - Her bireyin DNA'sinda tekrar eden diziler (STR) vardir
   - Bu tekrar sayilari bireyden bireye farklidir (tek yumurta ikizleri HARIC)
   - Islem: DNA izolasyonu -> PCR ile cogaltma -> Restriksiyon enzimi ile kesme -> Jel elektroforez
   - Sonuc: Her bireye ozgu bant deseni (parmak izi gibi)

   Kullanim alanlari:
   - Adli tip: Suc mahalli ornekleri (kan, tukuruk, sac)
   - Babalik testi: Ebeveyn-cocuk iliskisi belirleme
   - Kimlik belirleme: Afet kurbanlarinin teshisi
   - Evrimsel calismalar: Turler arasi akrabalik
"""
},

"BIY.12.5.KOK_HUCRE_VE_GEN_TERAPISI": {
    "unite": "Biyoteknoloji ve Genetik Muhendisligi",
    "baslik": "Kok Hucre, Gen Terapisi ve Klonlama",
    "icerik": """
KOK HUCRE, GEN TERAPISI VE KLONLAMA:

1. KOK HUCRE:
   - Farkli hucre tiplerine farklilasmabilen ozellesmemis hucreler

   a) Embriyonik Kok Hucreler:
      - Blastosist asamasindaki embriyodan elde edilir
      - TOTIPOTENT / PLURIPOTENT: Her hucre tipine donusebilir
      - Etik tartismalar (embriyo kullanimi)

   b) Eriskin (Somatik) Kok Hucreler:
      - Kemik iligi, yag dokusu, kan, dis gibi dokularda bulunur
      - MULTIPOTENT: Sinirli sayida hucre tipine donusebilir
      - Ornek: Kemik iligi kok hucreleri -> Kan hucreleri

   c) Induklenmis Pluripotent Kok Hucre (iPSC):
      - Eriskin hucrelerin yeniden programlanmasiyla elde edilir (Yamanaka, Nobel 2012)
      - Etik sorun cok az, hasta kendinden elde edebilir

   Kullanim alanlari:
   - Losemi tedavisi (kemik iligi nakli)
   - Parkinson, Alzheimer, diyabet arastirmalari
   - Doku ve organ yenileme (rejeneratif tip)

2. GEN TERAPISI:
   - Hastaliga neden olan kusurlu genin duzeltilmesi veya sagliki genle degistirilmesi
   - Somatik gen terapisi: Vucut hucreleri hedeflenir, sonraki nesle gecmez
   - Germ hatti gen terapisi: Ureme hucreleri hedeflenir, ETIK olarak tartismali
   - Vektor: Genellikle zararsizlastirilmis virus (adenovirus, retrovirus, AAV)
   - CRISPR-Cas9: Gen duzenleme teknolojisi (hassas kesme ve yapistirma)

3. UREME AMACLI KLONLAMA:
   - Bir canlinin genetik kopyasinin olusturulmasi
   - Dolly koyunu (1996, Ian Wilmut): Ilk klonlanmis memeli
   - Somatik hucre cekirdek transferi (SCNT):
     a) Yumurta hucresinin cekirdegi cikarilir
     b) Somatik hucrenin cekirdegi yumurtaya aktarilir
     c) Elektrik uyarisi ile bolunme baslatilir
     d) Embriyo tasiyici anneye yerlestirilir
   - Sorunlar: Dusuk basari orani, erken yaslanma, etik kaygilar

4. BIYOETIK KONULAR:
   - GDO guvenligi ve etiketleme tartismalari
   - Embriyonik kok hucre kullaniminin etik boyutu
   - Insan klonlamasi yasagi (pek cok ulkede yasak)
   - CRISPR ile "tasarim bebek" endisesi
"""
},

}

# ===============================================================
# YARDIMCI FONKSIYONLAR
# ===============================================================

def get_biyoloji12_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in BIYOLOJI_12_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_biyoloji12_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(BIYOLOJI_12_REFERANS.keys())
