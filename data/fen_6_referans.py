# -*- coding: utf-8 -*-
"""
6. Sinif Fen Bilimleri dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Gunes Sistemi ve Tutulmalar
2. Vucudumuzdaki Sistemler
3. Kuvvet ve Enerji
4. Madde ve Degisim
5. Ses
6. Elektrik
7. Dogal Surecler
"""

FEN_6_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: GUNES SISTEMI VE TUTULMALAR
# ═══════════════════════════════════════════════════════════════

"FEN.6.1.GUNES_SISTEMI": {
    "unite": "Gunes Sistemi ve Tutulmalar",
    "baslik": "Gunes Sistemi ve Gezegenler",
    "icerik": """
GUNES SISTEMI:
- Merkezinde Gunes (yildiz) bulunur.
- Gunes, Samanyolu galaksisindedir.
- Gunes etrafinda 8 gezegen, cuce gezegenler, asteroitler, kuyruklu yildizlar ve meteorlar bulunur.
- Gezegenler, Gunes'e yakinliktan uzakliga dogru: Merkur, Venus, Dunya, Mars, Jupiter, Saturn, Uranus, Neptun.

IC GEZEGENLER (KAYALIK GEZEGENLER):
- Gunes'e yakin olan ilk 4 gezegen: Merkur, Venus, Dunya, Mars
- Ortak ozellikler:
  * Kucuk boyutlu, yogun ve kayalik yapida
  * Katı yüzeyleri vardir
  * Az sayida uyduya sahip veya uydusu yoktur
  * Yavas donerler (dolanma sureleri kisa, donme sureleri uzun)

1. MERKUR:
   - Gunes'e en yakin gezegen
   - En kucuk gezegen
   - Atmosferi yok denecek kadar azdir
   - Uydusu yoktur
   - Gunes etrafindaki dolanma suresi: 88 gun (en kisa yil)

2. VENUS:
   - Dunya'dan "Aksamyildizi" veya "Sabahyildizi" olarak gorunur
   - En sicak gezegen (yogun CO2 atmosferi sera etkisi olusturur)
   - Dunya'ya en yakin gezegen
   - Uydusu yoktur
   - Ters yonde doner (retrograd rotasyon)

3. DUNYA:
   - Yasam olan bilinen tek gezegen
   - %71 su, %29 kara
   - 1 uydusu var: Ay
   - Atmosferi yasam icin uygun gazlar icerir (azot %78, oksijen %21)
   - Gunes etrafinda dolanma suresi: 365,25 gun (1 yil)
   - Kendi etrafinda donme suresi: 24 saat (1 gun)

4. MARS:
   - "Kizil Gezegen" olarak bilinir (yuzeyinde demir oksit)
   - 2 uydusu var: Phobos ve Deimos
   - Olympus Mons: Gunes Sistemi'ndeki en buyuk yanardag
   - Ince CO2 atmosferi vardir

DIS GEZEGENLER (GAZ DEV GEZEGENLER):
- Gunes'e uzak olan 4 gezegen: Jupiter, Saturn, Uranus, Neptun
- Ortak ozellikler:
  * Buyuk boyutlu
  * Gaz yapili (hidrojen, helyum)
  * Kati yüzeyleri yoktur
  * Cok sayida uyduya sahiptir
  * Halka sistemleri vardir
  * Hizli donerler

5. JUPITER:
   - Gunes Sistemi'nin en buyuk gezegeni
   - Buyuk Kirmizi Leke: Dev bir firtina (yuzyillardir devam eder)
   - 95'ten fazla uydusu var (en buyukleri: Ganymede, Europa, Io, Callisto)
   - Kendi etrafinda donme suresi: yaklasik 10 saat (en hizli donen gezegen)

6. SATURN:
   - En belirgin halka sistemine sahip gezegen
   - Halkalari buz ve kaya parcaciklarindan olusur
   - Yogunlugu sudan dusuktur (suda yuzer!)
   - 140'tan fazla uydusu var (en buyugu: Titan)

7. URANUS:
   - Yan yatmis eksende doner (98 derece egiklik)
   - Metan gazi nedeniyle yesil-mavi gorunur
   - 27 uydusu vardir

8. NEPTUN:
   - Gunes'e en uzak gezegen
   - En hizli ruzgarlara sahip gezegen (2000 km/saat)
   - Metan gazi nedeniyle koyu mavi gorunur
   - 16 uydusu vardir (en buyugu: Triton)

CUCE GEZEGENLER:
- Pluton: 2006'da cuce gezegen sinifina alindi
- Ceres, Eris, Makemake, Haumea

DIGER GOK CISIMLERI:
- Asteroid: Kayalik, duzensiz sekilli cisimler (cogu Mars-Jupiter arasinda Asteroid Kusagi'nda)
- Kuyruklu yildiz (Kuyrukluyildiz): Buz ve tozdan olusur, Gunes'e yaklasinca kuyruklari olusur
- Meteor: Atmosfere giren kucuk gok cismi (gokyuzunde "akan yildiz" gorunumu)
- Meteorit: Yeryuzune dusen meteor parcasi
"""
},

"FEN.6.1.TUTULMALAR": {
    "unite": "Gunes Sistemi ve Tutulmalar",
    "baslik": "Gunes Tutulmasi ve Ay Tutulmasi",
    "icerik": """
TUTULMA KAVRAMI:
- Gunes, Dunya ve Ay'in belirli bir hizaya gelmesi sonucu olusan olay.
- Tutulmalar periyodik olarak tekrarlanir.

GUNES TUTULMASI:
- Olusma kosulu: Ay, Gunes ile Dunya arasina girer.
- Siralama: Gunes → Ay → Dunya
- Ay'in golgesinin Dunya uzerine dusmesiyle olusur.
- Sadece yeniay evresinde gerceklesir.
- Turleri:
  * Tam (total) Gunes tutulmasi: Gunes tamamen kapanir, sadece tacindan isik gorunur
  * Kismi (partial) Gunes tutulmasi: Gunes'in bir kismi kapanir
  * Halkali (annular) Gunes tutulmasi: Ay kucuk gorunur, Gunes'in kenarlari gorunur
- Dunya'nin dar bir seridinden gozlenir (Ay'in golge konisi).
- UYARI: Gunes tutulmasini ciplak gozle izlemek gozlere zarar verir! Ozel filtre gerekir.

AY TUTULMASI:
- Olusma kosulu: Dunya, Gunes ile Ay arasina girer.
- Siralama: Gunes → Dunya → Ay
- Dunya'nin golgesinin Ay uzerine dusmesiyle olusur.
- Sadece dolunay evresinde gerceklesir.
- Turleri:
  * Tam Ay tutulmasi: Ay tamamen Dunya'nin golgesine girer (kirmizimsi gorunur)
  * Kismi Ay tutulmasi: Ay'in bir kismi golgeye girer
  * Yarimgolge Ay tutulmasi: Ay yarimgolge bolgesine girer, zor fark edilir
- Dunya'nin gece olan yarisinden gozlenebilir.
- Ciplak gozle guvenle izlenebilir.

AY'IN EVRELERI (TUTULMALARLA ILISKISI):
- Yeniay: Ay, Gunes ile ayni yondedir (Gunes tutulmasi olabilir)
- Ilk dordun: Ay'in sag yarisi aydinlik
- Dolunay: Ay, Gunes'in tam karsisindadir (Ay tutulmasi olabilir)
- Son dordun: Ay'in sol yarisi aydinlik
- Ay'in Dunya etrafindaki dolanma suresi: yaklasik 29,5 gun (bir ay = evre dongusu)

ONEMLI FARK:
- Gunes tutulmasi: Sadece dar bir bolgeden gozlenir, kisa surer (dakikalar)
- Ay tutulmasi: Genis bolgeden gozlenir, uzun surer (saatler)
- Her yeniay/dolunay'da tutulma OLMAZ (Ay'in yoru 5 derece egik)
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: VUCUDUMUZDAKI SISTEMLER
# ═══════════════════════════════════════════════════════════════

"FEN.6.2.DESTEK_HAREKET": {
    "unite": "Vucudumuzdaki Sistemler",
    "baslik": "Destek ve Hareket Sistemi (Iskelet ve Kaslar)",
    "icerik": """
ISKELET SISTEMI:
- Yetiskin bir insanda 206 kemik bulunur.
- Bebekler daha fazla kemige sahiptir (yaklasik 270-300), zamanla bazi kemikler kaynasir.

KEMIK TURLERI:
1. Uzun kemikler: Kol (humerus), bacak (femur, tibia, fibula)
2. Kisa kemikler: El bilegi, ayak bilegi kemikleri
3. Yassi kemikler: Kafatasi, kurek kemigi, kaburga
4. Duzensiz kemikler: Omurlar, yuz kemikleri

ISKELETIN GOREVLERI:
- Vucuda sekil ve destek verir
- Ic organlari korur (kafatasi→beyin, kaburgalar→kalp ve akciger)
- Hareketi saglar (kaslarla birlikte)
- Kan hucreleri uretir (kemik iligi)
- Mineral depolar (kalsiyum, fosfor)

EKLEMLER (KEMIK BIRLESIMLERI):
1. Oynar eklem: Genis hareket, omuz, kalca, diz, dirsek
   - Top-yuva eklemi: Omuz, kalca (her yone hareket)
   - Mentese eklemi: Diz, dirsek (tek yonde hareket)
   - Donme eklemi: Bas-boyun birlesimi
2. Yarim oynar eklem: Sinirli hareket, omurga, kaburga-gogus birlesimleri
3. Oynamaz eklem: Hareket yok, kafatasi kemikleri (dikisler)

KAS SISTEMI:
- Insan vucudunda yaklasik 600'den fazla kas vardir.
- Vucut agirliginin yaklasik %40-50'sini kaslar olusturur.

KAS TURLERI:
1. Iskelet kaslari (cizgili kas):
   - Istemli calisir (irade ile kontrol edilir)
   - Kemiklere kirisle baglanir
   - Hareketi saglar
   - Ornek: Biceps, triceps, quadriceps, karın kaslari

2. Duz kaslar:
   - Istemsiz calisir (irade ile kontrol edilmez)
   - Ic organlarin duvarinda bulunur
   - Ornek: Mide, bagirsak, damar duvarlari, mesane

3. Kalp kasi:
   - Istemsiz calisir
   - Sadece kalpte bulunur
   - Yasam boyu yorulmadan calisir
   - Ozel cizgili yapisi vardir

KASLAR NASIL CALISIR:
- Kaslar sadece KASILARAK (kisalarak) is yapar
- Kas cifleri (antagonist kaslar) birlikte calisir:
  * Biceps kasilir → kol bukumlur (dirsek bukulmesi)
  * Triceps kasilir → kol acilir (dirsek acilmasi)
- Bir kas kasilirken, karsit kas gevser

KEMIK VE KAS SAGLIGI:
- Kalsiyum ve D vitamini yeterli alinmali (sut, yogurt, peynir)
- Duzenli egzersiz kemik ve kas sagligini guclendirir
- Dogru oturma ve duruş bozukluklarini onler (skolyoz, kifoz, lordoz)
- Agir tasimalardan kacinilmali
"""
},

"FEN.6.2.SINDIRIM": {
    "unite": "Vucudumuzdaki Sistemler",
    "baslik": "Sindirim Sistemi",
    "icerik": """
SINDIRIM KAVRAMI:
- Besinlerin vucutta kullanilabilir kucuk molekullere parcalanmasi
- Iki tur sindirim vardir:
  * Mekanik sindirim: Besinlerin fiziksel olarak kucultulmesi (disler, mide hareketi)
  * Kimyasal sindirim: Enzimler yardimiyla besinlerin kimyasal parcalanmasi

SINDIRIM SISTEMI ORGANLARI (SIRASI ILE):

1. AGIZ:
   - Mekanik sindirim: Disler besini parcalar
   - Kimyasal sindirim: Tukarik bezlerinden salinan tukarik (amilaz enzimi) nisastayi parcalar
   - Dil besini karistirir ve yutkunmaya yardimci olur
   - Dis turleri: Kesici (8), kopek (4), kucuk azı (8), buyuk azi (12) = toplam 32 (yetiskin)

2. YUTKUNMA VE YEMEK BORUSU:
   - Agizdan mideye besini tasir
   - Peristaltik hareket: Kas kasılmalariyla besini iter
   - Yaklasik 25 cm uzunlugunda

3. MIDE:
   - Mekanik sindirim: Mide kaslari besini yogurur
   - Kimyasal sindirim: Mide ozu (HCl + pepsin enzimi) proteinleri parcalar
   - Mide asidi (HCl) mikropları oldurur
   - pH: 1,5-3,5 (asidik)
   - Kapasite: yaklasik 1,5-2 litre

4. INCE BAGIRSAK:
   - En onemli sindirim ve emilim organi
   - Uzunlugu: yaklasik 6-7 metre
   - Uc bolumu: onikiparmak (duodenum), jejunum, ileum
   - Pankreas ozu ve safra burada sindirime katilir
   - Karbonhidrat, protein ve yaglarin sindirimi tamamlanir
   - Villus (tümsek) yapisi emilim yuzeyini arttirir
   - Sindirilen besinler kan ve lenf damarlarına emilir

5. KALIN BAGIRSAK:
   - Uzunlugu: yaklasik 1,5 metre
   - Su ve mineral emilimi yapilir
   - Sindirilemeyen maddeler diskilastirilir
   - Faydali bakteriler (flora) B ve K vitamini uretir

6. ANUS:
   - Sindirim artiklari vucuttan atilir

YARDIMCI SINDIRIM ORGANLARI:
- Tukarik bezleri: Amilaz enzimi uretir (nisasta sindirimi)
- Karaciger: Safra uretir (yaglari kucuk damlaciclara ayirir = emulsifikasyon)
  * Vucudun en buyuk ic organi
  * Zararlı maddeleri notralize eder
- Safra kesesi: Safrayi depolar
- Pankreas: Sindirim enzimleri uretir (amilaz, lipaz, tripsin) + insulin hormonu

BESIN OGELERININ SINDIRIMI:
- Karbonhidratlar: Agizda baslar (amilaz) → Ince bagirsakta tamamlanir → Glikoz
- Proteinler: Midede baslar (pepsin) → Ince bagirsakta tamamlanir → Amino asit
- Yaglar: Ince bagirsakta baslar (safra + lipaz) → Yag asidi + Gliserol
- Su, mineraller, vitaminler: Sindirime GEREK YOKTUR (dogrudan emilir)
"""
},

"FEN.6.2.DOLASIM": {
    "unite": "Vucudumuzdaki Sistemler",
    "baslik": "Dolasim Sistemi",
    "icerik": """
DOLASIM SISTEMI GOREVLERI:
- Besin, oksijen ve hormonlari hucrelere tasir
- Atik maddeleri (CO2, ure) ilgili organlara tasir
- Vucudun bagisiklik savunmasini saglar
- Vucut sicakligini duzenlemeye yardimci olur

KALP:
- Dolasim sisteminin merkezi pompasidir
- Gogus kafesinde, iki akciger arasinda, hafifce solda bulunur
- Yaklasik yumruk buyuklugundedir (250-350 gram)
- 4 odaciktan olusur:
  * Sag kulakcik (atriyum): Kirli kani (CO2'li) toplar
  * Sag karincik (ventrikul): Kirli kani akciğerlere pompalar
  * Sol kulakcik: Temiz kani (O2'li) akcigerllerden toplar
  * Sol karincik: Temiz kani vucuda pompalar (en kalin duvarli odacik)
- Kapakciklar: Kanin geri akmasini engeller
- Kalp dakikada ortalama 70-80 kez atar (yetiskin)
- Istemsiz calisir (kalp kasi)

KAN DAMARLARI:
1. ATARDAMAR (ARTER):
   - Kani kalpten organlara tasir
   - Kalin ve elastik duvarli
   - Yuksek basincla kan tasir
   - Nabiz hissedilir
   - Derinde bulunur (yaralanmaya karsi koruma)

2. TOPLARDAMAR (VEN):
   - Kani organlardan kalbe tasir
   - Ince duvarli
   - Dusuk basincla kan tasir
   - Icinde kapakciklar bulunur (kanin geri akmasini engeller)
   - Yuzeysel bulunur

3. KILCAL DAMAR (KAPILER):
   - Atardamar ve toplardamari birbirine baglar
   - Cok ince duvarli (tek hucre kalinliginda)
   - Madde alisverisi burada yapilir (O2, CO2, besin, atik)
   - Vucut genelinde ag gibi yayilir

KAN DOLASIMI:
1. KUCUK DOLASIM (AKCIGER DOLASIMI):
   Sag karincik → Akciger atardamari → Akciger (CO2 birakir, O2 alir) → Akciger toplardamari → Sol kulakcik

2. BUYUK DOLASIM (VUCUT DOLASIMI):
   Sol karincik → Aort (ana atardamar) → Vucut (O2 birakir, CO2 alir) → Ust/Alt ana toplardamar → Sag kulakcik

ONEMLI NOT:
- Akciger atardamari: Kirli kan tasir (istisna!)
- Akciger toplardamari: Temiz kan tasir (istisna!)
- Diger tum atardamarlar temiz, toplardamarlar kirli kan tasir

KAN:
- Yetiskin bir insanda yaklasik 5-6 litre kan bulunur
- Bilesenleri:
  * Plazma (%55): Sari renkli sivi, besin/hormon/atik tasir
  * Alyuvar (eritrosit): Oksijen tasir (hemoglobin icin demir gerekli), cekirdeksiz
  * Akyuvar (lokosit): Bagisiklik, mikroplarla savasir
  * Kan pulcuklari (trombosit): Kan pihtilasmasini saglar

KAN GRUPLARI:
- A, B, AB, O (ABO sistemi)
- Rh faktoru: (+) veya (-)
- 0 Rh(-): Genel verici (herkese kan verebilir)
- AB Rh(+): Genel alici (herkesten kan alabilir)
"""
},

"FEN.6.2.SOLUNUM": {
    "unite": "Vucudumuzdaki Sistemler",
    "baslik": "Solunum Sistemi",
    "icerik": """
SOLUNUM KAVRAMI:
- Oksijen (O2) alarak besinlerden enerji uretme ve karbondioksit (CO2) atma sureci
- Hucresel solunum: Glikoz + O2 → CO2 + H2O + Enerji (ATP)
- C6H12O6 + 6O2 → 6CO2 + 6H2O + Enerji

SOLUNUM SISTEMI ORGANLARI:

1. BURUN:
   - Havanin vucuda giris noktasi
   - Havayi isitir, nemlendirir ve filtreler
   - Burun killari ve mukus tabakasi tozu/mikroplari tutar
   - Koku alma duyusu burada bulunur

2. YUTAK (FARINKS):
   - Burun ve agiz boslugunun birlestigi alan
   - Hava ve besin yolu burada kesisir
   - Girtlak kapagi (epiglottis) yutkunurken hava yolunu kapatir

3. GIRTLAK (LARINKS):
   - Ses tellerini icerir
   - Ses uretiminden sorumlu
   - Havayolu ile yemek borusunun ayrildigi bolge

4. SOLUK BORUSU (TRAKEA):
   - Yaklasik 12 cm uzunlugunda
   - "C" seklinde kikirdak halkalari ile acik tutulur
   - Ic yuzeyindeki silia (titrek tuycukler) mukusu yukari tasir

5. BRONLSAR:
   - Soluk borusunun ikiye ayrildigi dallar
   - Sag ve sol akcigere giden hava yollari
   - Dallanarak bronsculer olusturur

6. AKCIGER:
   - Gaz degisiminin yapildigi ana organ
   - Sag akciger 3 lob, sol akciger 2 lobdan olusur (kalp sola dayanir)
   - Icinde milyonlarca alveol (hava kesecigi) bulunur

7. ALVEOL (HAVA KESECIKLERI):
   - Gaz degisiminin gerceklestigi yapilar
   - Yaklasik 300-500 milyon adet bulunur
   - Toplam yuzey alani: yaklasik 70-100 m² (bir tenis kortu buyuklugunde)
   - Ince duvarli → O2 kana gecer, CO2 havaya gecer (difuzyon)

SOLUNUM MEKANIZMASI:
- Nefes alma (inspirasyon):
  * Diyafram kasılır ve asagi iner
  * Kaburgalar arasi kaslar kasilir, kaburgalar yukarı kalkar
  * Gogus boslugu genisler → Akcigerlere hava girer

- Nefes verme (ekspirasyon):
  * Diyafram gevser ve yukari cikar
  * Kaburgalar asagi iner
  * Gogus boslugu daralir → Akciglerden hava cikar

SOLUNUMU ETKILEYEN FAKTORLER:
- Egzersiz: Solunum hizi artar (daha fazla O2 ihtiyaci)
- Sigara: Alveollere zarar verir, silia'yi yok eder
- Hava kirliligi: Solunum yolu hastaliklarina neden olur
"""
},

"FEN.6.2.BOSALTIM": {
    "unite": "Vucudumuzdaki Sistemler",
    "baslik": "Bosaltim Sistemi",
    "icerik": """
BOSALTIM KAVRAMI:
- Metabolizma sonucu olusan zararlı atik maddelerin vucuttan uzaklastirilmasi
- Bosaltim ≠ Sindirim atiklari (diski bosaltim urunu degildir, sindirilemeyen maddedir)

BOSALTIM SISTEMI ORGANLARI:

1. BOBREKLER:
   - Ana bosaltim organi
   - Fasulye seklinde, bel bolgesinin iki yaninda
   - Sag bobrek biraz daha asagidadir (karaciger nedeniyle)
   - Her biri yaklasik 150 gram, 10-12 cm uzunlugunda
   - Gunde yaklasik 180 litre kani filtreler, 1,5-2 litre idrar olusturur

   NEFRON (BOBREK BIRIMI):
   - Her bobrekte yaklasik 1 milyon nefron bulunur
   - Kanin filtrelendigi yapisal ve islevsel birim
   - Islem: Filtrasyon → Geri emilim → Salgilanma → Idrar olusumu
   - Kandarki ure, urik asit, fazla su ve mineralleri suzar

2. IDRAR BORULARI (URETER):
   - Bobreklerden mesaneye idrar tasir
   - Yaklasik 25-30 cm uzunlugunda
   - Peristaltik hareketlerle idrar iletilir

3. IDRAR KESESI (MESANE):
   - Idrari gecici olarak depolar
   - Kapasite: yaklasik 300-500 ml
   - Doldugunda sinir sistemi araciligiyla idrar yapma istegi olusur

4. IDRAR KANALI (URETRA):
   - Idrarin vucuttan atildigi kanal

IDRAR BILESIMI:
- %95 su
- %2 ure (protein metabolizmasi atigi)
- %3 diger: urik asit, kreatinin, tuz, amonyak

DIGER BOSALTIM ORGANLARI:
- Akciger: CO2 ve su buharina atar (solunum atigi)
- Deri: Ter bezleri ile su, tuz ve az miktarda ure atar
- Karaciger: Zararlı maddeleri notralize eder, ureyi sentezler

BOSALTIM SAGLIGI:
- Bol su icmek (gunde 1,5-2 litre)
- Asiri tuzlu/proteinli beslenme bobrek yukunu arttirir
- Idrari tutmamak (mesane enfeksiyonlarina neden olabilir)
- Ilac ve zararlı madde kullanimından kacinmak
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: KUVVET VE ENERJI
# ═══════════════════════════════════════════════════════════════

"FEN.6.3.KUTLE_AGIRLIK": {
    "unite": "Kuvvet ve Enerji",
    "baslik": "Kutle, Agirlik ve Yercekimi Kuvveti",
    "icerik": """
KUTLE:
- Bir cismin icerdigi madde miktari
- Birimi: kilogram (kg), gram (g), miligram (mg)
- 1 kg = 1000 g, 1 g = 1000 mg
- Olcme araci: Esit kollu terazi (veya elektronik terazi)
- Kutle DEGISMEZ: Dunya'da, Ay'da, uzayda ayni kalir
- Skaler buyukluktur (yonu yoktur)

AGIRLIK (AGIRLIK KUVVETI):
- Gezegenin/gok cisminin bir cisme uyguladigi cekim kuvveti
- Birimi: Newton (N)
- Olcme araci: Dinamometre (yay tartisi)
- Agirlik DEGISIR: Bulunulan gok cismine gore degisir
- Vektorel buyukluktur (yonu her zaman merkezedir)

AGIRLIK FORMULU:
  G = m × g

  G: Agirlik kuvveti (Newton, N)
  m: Kutle (kilogram, kg)
  g: Yercekimi ivmesi (m/s²)

YERCEKIMI IVMESI DEGERLERI:
  Dunya: g = 10 N/kg (veya ~9,8 m/s²)
  Ay: g = 1,6 N/kg (Dunya'nin ~1/6'si)
  Jupiter: g = 25 N/kg
  Mars: g = 3,7 N/kg

ORNEK HESAPLAMALAR:
  Dunya'da 60 kg kutle → G = 60 × 10 = 600 N
  Ay'da 60 kg kutle → G = 60 × 1,6 = 96 N
  (Kutle degismedi: 60 kg, ama agirlik degisti!)

KUTLE VE AGIRLIK FARKI:
  | Ozellik     | Kutle            | Agirlik           |
  |-------------|------------------|-------------------|
  | Tanim       | Madde miktari    | Cekim kuvveti     |
  | Birim       | kg               | Newton (N)        |
  | Olcme araci | Terazi           | Dinamometre       |
  | Degisim     | Degismez         | Gok cismine gore  |
  | Tur         | Skaler           | Vektorel          |

YERCEKIMI KUVVETI:
- Her kutle birbirini ceker (Newton'un Evrensel Cekim Yasasi)
- Kutleler artarsa cekim artar
- Mesafe artarsa cekim azalir
- Gezegenlerin Gunes etrafinda donmesi → Yercekimi
- Ay'in Dunya etrafinda donmesi → Yercekimi
- Cismin yere dusmesi → Yercekimi
"""
},

"FEN.6.3.ENERJI": {
    "unite": "Kuvvet ve Enerji",
    "baslik": "Enerji Turleri ve Donusumleri",
    "icerik": """
ENERJI KAVRAMI:
- Is yapabilme yetenegi
- Enerji yoktan var olmaz, vardan yok olmaz (Enerjinin Korunumu Yasasi)
- Sadece bir turden digerine donusur
- Birimi: Joule (J), kilojoule (kJ), kalori (cal)
- 1 kJ = 1000 J
- 1 cal = 4,18 J

KINETIK ENERJI (HAREKET ENERJISI):
- Hareket eden cisimlerin sahip oldugu enerji
- Formul: Ek = (1/2) × m × v²
  * Ek: Kinetik enerji (Joule)
  * m: Kutle (kg)
  * v: Hiz (m/s)
- Hiz artarsa kinetik enerji ARTAR (hiz ile orantili, karesel)
- Kutle artarsa kinetik enerji ARTAR
- Ornek: Hizla giden araba > yavas giden araba (ayni kutle)
- Ornek: Kamyon > otomobil (ayni hiz, farkli kutle)

POTANSIYEL ENERJI (KONUM/DEPOLANMIS ENERJI):

1. Yercekimi Potansiyel Enerjisi:
   - Yuksekte bulunan cisimlerin sahip oldugu enerji
   - Formul: Ep = m × g × h
     * Ep: Potansiyel enerji (Joule)
     * m: Kutle (kg)
     * g: Yercekimi ivmesi (10 N/kg)
     * h: Yukseklik (m)
   - Yukseklik artarsa potansiyel enerji ARTAR
   - Kutle artarsa potansiyel enerji ARTAR
   - Ornek: 2 kg cisim 5 m yukseklikte → Ep = 2 × 10 × 5 = 100 J

2. Esneklik Potansiyel Enerjisi:
   - Gerilmis/sıkıstırılmis esnek cisimlerin enerjisi
   - Ornek: Gerilmis lastik, yay, ok, sapan

MEKANIK ENERJI:
- Mekanik Enerji = Kinetik Enerji + Potansiyel Enerji
- Em = Ek + Ep
- Serbest dususte: Potansiyel enerji azalir, kinetik enerji artar
- Yukari atista: Kinetik enerji azalir, potansiyel enerji artar
- Toplam mekanik enerji (suturmesiz ortamda) korunur

DIGER ENERJI TURLERI:
- Isı enerjisi: Sicaklik farkindan kaynaklanan enerji
- Isik enerjisi: Gunes, ampul, ates
- Ses enerjisi: Titresimlerden kaynaklanan enerji
- Elektrik enerjisi: Elektrik akimindan elde edilen enerji
- Kimyasal enerji: Besin, yakit, pil icinde depolanan enerji
- Nukleer enerji: Atom cekirdegindeki enerji

ENERJI DONUSUMLERI (ORNEKLER):
- Gunes paneli: Isik enerjisi → Elektrik enerjisi
- Elektrik sobasi: Elektrik enerjisi → Isi enerjisi
- Televizyon: Elektrik → Isik + Ses enerjisi
- Araba motoru: Kimyasal enerji → Kinetik + Isi enerjisi
- Hidroelektrik santral: Potansiyel → Kinetik → Elektrik enerjisi
- Fotosentez: Isik enerjisi → Kimyasal enerji
- Besin yeme: Kimyasal enerji → Kinetik + Isi enerjisi
- Ruzgar turbini: Kinetik enerji → Elektrik enerjisi
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: MADDE VE DEGISIM
# ═══════════════════════════════════════════════════════════════

"FEN.6.4.TANECIKLI_YAPI": {
    "unite": "Madde ve Degisim",
    "baslik": "Maddenin Tanecikli Yapisi ve Siniflandirilmasi",
    "icerik": """
MADDE KAVRAMI:
- Kutle ve hacme sahip her sey maddedir.
- Maddeler taneciklerden (atom, molekul) olusur.
- Tanecikler surekli hareket halindedir.
- Tanecikler arasi boslukllar ve cekim kuvvetleri vardir.

MADDENIN HALLERI:
1. KATI:
   - Tanecikler birbirine yakin, duzgun dizilimli
   - Tanecikler arasi cekim kuvveti en fazla
   - Titresim hareketi yapar (yerinde sallanir)
   - Belirli sekli ve hacmi vardir
   - Sikistirilamaz
   - Ornek: Buz, demir, tas

2. SIVI:
   - Tanecikler katiya gore daha uzak
   - Tanecikler birbirleri uzerinden kayar
   - Belirli hacmi vardir, sekli kaba gore degisir
   - Sikistirilamaz (ihmal edilebilir)
   - Ornek: Su, sut, yag

3. GAZ:
   - Tanecikler birbirinden cok uzak
   - Tanecikler arasi cekim kuvveti en az
   - Serbest ve hizli hareket eder
   - Belirli sekli ve hacmi yoktur (kabi doldurur)
   - Sikistiririlabilir
   - Ornek: Hava, oksijen, karbondioksit

HAL DEGISIKLIKLERI:
- Erime: Kati → Sivi (isi alir) [Buz → Su, 0°C]
- Donma: Sivi → Kati (isi verir) [Su → Buz, 0°C]
- Buharlarma: Sivi → Gaz (isi alir) [Su → Su buhqri, 100°C]
- Yogunlasma: Gaz → Sivi (isi verir) [Su buhari → Su]
- Sublesbme: Kati → Gaz (isi alir) [Naftalin, kuru buz]
- Kiragılanma: Gaz → Kati (isi verir) [Kar taneleri olusumu]

ELEMENT:
- Ayni tur atomlardan olusur
- Kimyasal yontemlerle daha basit maddelere ayrılamazz
- Simge ile gosterilir: O (oksijen), Fe (demir), Au (altin), C (karbon)
- 118 element bilinmektedir (periyodik tablo)
- Ornek: Demir (Fe), Bakir (Cu), Altin (Au), Oksijen (O2), Hidrojen (H2)

BILESIK:
- Farkli tur atomlarin belirli oranlarla birlesmesinden olusur
- Formul ile gosterilir
- Kimyasal yontemlerle bilesenllerine ayrilabilir
- Ozellikleri kendisini olusturan elementlerden farklidir
- Ornek: Su (H2O) → 2 Hidrojen + 1 Oksijen
  Sofra tuzu (NaCl) → Sodyum + Klor
  Karbondioksit (CO2) → 1 Karbon + 2 Oksijen
  Seker (C12H22O11)

KARISIM:
- Iki veya daha fazla maddenin belirli bir oran olmadan bir araya gelmesi
- Fiziksel yontemlerle ayrilabilir
- Homojen karisim: Her yerinde ayni gorunumde (cozeltiler)
  Ornek: Tuzlu su, serbetc, hava, cellik
- Heterojen karisim: Her yerinde farkli gorunumde
  Ornek: Kumlu su, salata, toprak, zeytinyagli su

KARISIM AYIRMA YONTEMLERI:
- Suzme: Kati-sivi karisimi (kumlu su)
- Buharlas irma: Cozunmus kati elde etme (tuzlu su→tuz)
- Damitma: Sivi-sivi karisimi (su+alkol)
- Miknatislanma: Demir iceren karisimlar
- Yuzdurmme-batirma: Yogunluk farkiyla ayirma
- Elekten gecirme: Farkli boyuttaki katilari ayirma
"""
},

"FEN.6.4.FIZIKSEL_KIMYASAL": {
    "unite": "Madde ve Degisim",
    "baslik": "Fiziksel ve Kimyasal Degisim, Yogunluk",
    "icerik": """
FIZIKSEL DEGISIM:
- Maddenin dis gorunusu veya hali degisir, kimligii degismez
- Geri donusumlu (tersinir) degisimlerdir
- Yeni madde OLUSMAZ
- Ornekler:
  * Buzun erimesi (kati su → sivi su, hala H2O)
  * Kagit yirtma (parcalar hala kagit)
  * Sekkerin suda erimesi (seker hala sekerdir)
  * Cam kirma
  * Buharlaama
  * Eriyen mum (erime, hal degisimi)
  * Demir teli bukme

KIMYASAL DEGISIM:
- Maddenin ic yapisi ve kimligi degisir
- Genellikle geri donusumsuz (tersinmez) degisimlerdir
- YENI madde olusur
- Belirtileri: Renk degisimi, gaz cikisi, cokkelme, isi/isik cikisi, koku degisimi
- Ornekler:
  * Kagit yanmasi (kagit → kul + CO2 + H2O, yeni maddeler olusur)
  * Demir paslanmasi (Fe + O2 → Fe2O3)
  * Sut eksmesi (yeni maddeler olusur, koku degisir)
  * Yumurta pisirmesi
  * Mum yanmasi (yanma kimyasal, erime fiziksel)
  * Ekmek kufllenmesi
  * Yaprak sararması
  * Meyve curumesi
  * Sirke + kabartma tozu → gaz cikisi (CO2)

KARSILASTIRMA:
  | Ozellik        | Fiziksel Degisim    | Kimyasal Degisim     |
  |----------------|---------------------|----------------------|
  | Yeni madde     | Olusmaz             | Olusur               |
  | Geri donus     | Mumkun              | Genellikle mumkun degil |
  | Ne degisir     | Dis gorunum/hal     | Ic yapi/kimlik       |
  | Ornek          | Buz erime           | Odun yanma           |

YOGUNLUK:
- Birim hacimdeki kutle miktari
- Her saf maddenin kendine ozgu yogunlugu vardir (ayirt edici ozellik)
- Sicaklik ve hal degisimi yogunlugu etkiler

YOGUNLUK FORMULU:
  d = m / V

  d: Yogunluk (g/cm³ veya kg/m³)
  m: Kutle (g veya kg)
  V: Hacim (cm³ veya m³)

  Diger formlar:
  m = d × V
  V = m / d

BAZI MADDELERIN YOGUNLUGU (g/cm³):
  Saf su: 1,0 g/cm³
  Buz: 0,9 g/cm³ (bu yuzden suda yuzer!)
  Demir: 7,87 g/cm³
  Altin: 19,3 g/cm³
  Aluminyum: 2,7 g/cm³
  Bakir: 8,96 g/cm³
  Tahta (mesee): ~0,6-0,9 g/cm³
  Zeytinyagi: ~0,92 g/cm³
  Hava: 0,0013 g/cm³

ORNEK HESAPLAMA:
  Kutle: 500 g, Hacim: 250 cm³
  d = 500 / 250 = 2 g/cm³

YOGUNLUK VE YUZME-BATMA:
- Cismin yogunlugu < Sivinin yogunlugu → YUZER
- Cismin yogunlugu > Sivinin yogunlugu → BATAR
- Cismin yogunlugu = Sivinin yogunlugu → ASKIDA KALIR
- Ornek: Buz (0,9) < Su (1,0) → Buz suda yuzer
- Ornek: Demir (7,87) > Su (1,0) → Demir suda batar
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: SES
# ═══════════════════════════════════════════════════════════════

"FEN.6.5.SES": {
    "unite": "Ses",
    "baslik": "Sesin Olusumu, Yayilmasi ve Ozellikleri",
    "icerik": """
SESIN OLUSUMU:
- Ses, maddenin titresimi sonucu olusur.
- Titresim: Bir cismin belirli bir konum etrafinda ileri-geri hareketi.
- Titresim dururdugunda ses de durur.
- Ornek: Gitar teli titresir → ses olusur, tel durdurulursa ses kesilir.

SESIN YAYILMASI:
- Ses bir enerji turudur ve dalga seklinde yayilir.
- Ses dalgalari boyuna (longitudinal) dalgadir.
- Sesin yayilmasi icin maddesel ortam GEREKLIDIR.
- Boslukta (vakumda) ses yayilmaz! (Uzayda ses duyulmaz)
- Ses kati, sivi ve gaz ortamda yayilabilir.

SESIN YAYILMA HIZI:
- Kati > Sivi > Gaz (siralamasi)
- Katida en hizli yayilir (tanecikler yakin, titresim hizli iletilir)
- Gaza en yavas yayilir (tanecikler uzak)
- Havada ses hizi: yaklasik 340 m/s (20°C'de)
- Suda ses hizi: yaklasik 1500 m/s
- Celikte ses hizi: yaklasik 5000 m/s
- Sicaklik artarsa ses hizi artar (tanecik hareketi artar)

SESIN OZELLIKLERI:

1. FREKANS (SIKLIK):
   - Bir saniyedeki titresim sayisi
   - Birimi: Hertz (Hz)
   - 1 Hz = saniyede 1 titresim
   - Frekans artar → ses INCE (tiz) olur
   - Frekans azalir → ses KALIN (pes) olur
   - Insan kulagi: 20 Hz - 20.000 Hz arasini duyar
   - 20 Hz altı: Infrasound (ses alti, filler duyar)
   - 20.000 Hz ustu: Ultrasound (ses ustu, yarasalar, yunuslar duyar)
   - Kadinlarin sesi genellikle erkeklerden daha tizdir (frekans yuksek)

2. GENLIK (SIDDET):
   - Titresimin buyuklugu (genisligi)
   - Genlik artar → ses GUCLÜ (siddetli) olur
   - Genlik azalir → ses ZAYIF (hafif) olur
   - Ses siddeti birimi: desibel (dB)
   - Fisildama: ~20 dB
   - Normal konusma: ~60 dB
   - Trafik gurultusu: ~80 dB
   - Rock konseri: ~110 dB
   - Agri esigi: ~120 dB
   - 85 dB ustu uzun sureli maruz kalma isitme kaybina yol acar

3. TINI (SES RENGI):
   - Ayni frekansta farkli kaynaklarin farkli duyulmasi
   - Her sesin "parmak izi" gibidir
   - Ayni notayi calan keman ve piyano farkli duyulur → Tini farki
   - Tanidik insanlarin sesini ayirt etmemizi saglar

SESIN YANSIMASI VE YANKI:
- Ses dalgalari sert yüzeylere carpinca geri doner (yansima)
- YANKI: Yansıyan sesin orijinal sesten ayirt edilebilmesi
- Yanki olusma kosulu: Ses kaynagi ile yansitici yuzey arasi mesafe en az 17 m olmali
  (Ses gidip donmeli: 2 × 17 = 34 m, ses hızı 340 m/s, 34/340 = 0,1 saniye gecikme)
- Kulak 0,1 saniyeden kisa aralikli sesleri ayirt edemez
- Yanki kullanim alanlari:
  * Sonar (deniz dibi haritasi, denizalti tespiti)
  * Ultrason (tipta goruntuleme)
  * Yarasalarin yolunu bulmasi (ekolokasyon)

GURULTU VE SES KIRLILIGI:
- Istenmeyen ve rahatsiz edici ses → gurultu
- Ses kirliligi kaynaklari: trafik, insaat, fabrika, yuksek muzik
- Zararları: isitme kaybi, stres, uyku bozuklugu, dikkat eksikligi
- Onlemler: ses yalitimi, kisisel koruyucu (kulaklık), mesafe
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: ELEKTRIK
# ═══════════════════════════════════════════════════════════════

"FEN.6.6.ELEKTRIK_DEVRELERI": {
    "unite": "Elektrik",
    "baslik": "Elektrik Devreleri ve Seri-Paralel Baglanti",
    "icerik": """
ELEKTRIK DEVRESI KAVRAMI:
- Elektrik enerjisinin bir kaynaktan tuketiciye iletilmesini saglayan kapalı yol
- Devrenin calismasi icin KAPALI olmasi gerekir (anahtar kapali)

TEMEL DEVRE ELEMANLARI:
1. Enerji kaynagi: Pil, batarya, jenerator (elektrik enerjisi sagllar)
2. Iletken tel: Bakir veya aluminyum tel (akimi iletir)
3. Tuketici (yuklk): Ampul, motor, rezistans (elektrik enerjisini donusturur)
4. Anahtar: Devreyi acar/kapatir
5. Sigorta: Asiri akimda devreyi keser (koruma)

ELEKTRIK AKIMI:
- Elektrik yuklerinin iletken boyunca hareketi
- Birimi: Amper (A)
- Olcme araci: Ampermetre
- Ampermetre devreye SERI baglanir
- Simgesi: A (daire icinde)

GERILIM (POTANSIYEL FARKI / VOLTAJ):
- Elektrik yuklerini harekete geciren kuvvet
- Birimi: Volt (V)
- Olcme araci: Voltmetre
- Voltmetre devreye PARALEL baglanir
- Simgesi: V (daire icinde)
- Pilin gerilimi ne kadar yuksekse, ampul o kadar parlak yanar

DIRENC:
- Maddenin elektrik akimina karsi gosterdigi zorluk
- Birimi: Ohm (Ω, omega)
- Iletken tellerde direnc dusuktur (baakir, gumus)
- Yalitkanlarda direnc cok yuksektir (plastik, cam, kaucuk)
- Direnci etkileyen faktorler:
  * Uzunluk artar → Direnc artar
  * Kesit alani artar → Direnc azalir
  * Madde cinsi (iletkenlik)
  * Sicaklik artar → Direnc genellikle artar

OHM YASASI (TEMELLER):
  V = I × R

  V: Gerilim (Volt)
  I: Akım (Amper)
  R: Direnc (Ohm)

  Diger formlar:
  I = V / R
  R = V / I

  Ornek: 12 V pil, 4 Ω direnc → I = 12/4 = 3 A

SERI BAGLANTI:
- Devre elemanlari ard arda (tek yol) baglanir
- Ozellikler:
  * Akim her noktada AYNIDIR: I_toplam = I1 = I2 = I3
  * Gerilim PAYLASILI: V_toplam = V1 + V2 + V3
  * Toplam direnc ARTAR: R_toplam = R1 + R2 + R3
  * Bir ampul cikarilirsa tum devre kesilir (noel isiklari gibi)
  * Ampul sayisi artarsa ampuller daha SONIUK yanar

PARALEL BAGLANTI:
- Devre elemanlari yan yana (ayri kollar) baglanir
- Ozellikler:
  * Gerilim her kolda AYNIDIR: V_toplam = V1 = V2 = V3
  * Akim PAYLASILI: I_toplam = I1 + I2 + I3
  * Toplam direnc AZALIR: 1/R_toplam = 1/R1 + 1/R2 + 1/R3
  * Bir ampul cikarilirsa diger ampuller CALISMAYA DEVAM EDER
  * Ampuller ayni parlaklikta yanar (esit direncliyse)
  * Evlerdeki elektrik tesisati paralel baglantidir

KARSILASTIRMA:
  | Ozellik     | Seri Baglanti         | Paralel Baglanti        |
  |-------------|----------------------|------------------------|
  | Akim        | Her yerde ayni       | Kollara dagilir         |
  | Gerilim     | Elemanlara dagilir   | Her kolda ayni          |
  | Direnc      | Toplanır (artar)     | Azalir                  |
  | Bir eleman  | Tum devre kesilir    | Diger kollar calisir    |
  | Parlakllik  | Eleman artinca azalir| Ayni kalir              |

ELEKTRIK GUVENLIGI:
- Islak elle elektrik cihazlarina dokunulmaz
- Hasarli kablo kullanilmaz
- Priz delikllerine cisim sokulmmaz
- Topraklama hatti onemlidir
- Sigorta/kaçak akım rölesi koruma saglar
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. UNITE: DOGAL SURECLER
# ═══════════════════════════════════════════════════════════════

"FEN.6.7.DOGAL_SURECLER": {
    "unite": "Dogal Surecler",
    "baslik": "Deprem, Volkan, Erozyon, Heyelan ve Dogal Afetlerden Korunma",
    "icerik": """
DUNYA'NIN KATMANLI YAPISI:
- Yerkabugu (litosfer): En dis katman, ince (5-70 km), katidir
- Manto: Yerkabugu altinda, yarim akiskkan, cok sicak
- Dis cekirdek: Sivi metal (demir-nikel)
- Ic cekirdek: Katı metal (cok yuksek sicaklik ve basinc)

LEVHA TEKTONIGI:
- Yerkabugu buyuk parcalara (levha/plaka) ayrilmistir
- Levhalar manto uzerinde yavas yavas hareket eder (yilda birkac cm)
- Levha sinirlarinda deprem ve volkanik faaliyetler yogunlasir
- Levha hareketleri: Yakinlasan (carpisan), uzaklasan (ayrilan), yatay kayma

═══════════════════════════
1. DEPREM:
═══════════════════════════
- Yerkabugundaki kırık (fay) hatlari boyunca birikenn enerjinin aniden bosalmasiyla olusan sarsinti
- Odak noktasi (hiposantr): Enerjinin bosaldigi yer (yeraltinda)
- Dis merkez (episantr): Odak noktasinin yeryuzundeki izdusumu (en cok hasar burada)
- Sismograf: Deprem dalgalarini kaydeden cihaz
- Buyukluk olcegi: Richter olcegi (logaritmik)
  * 3'ten kucuk: Genellikle hissedilmez
  * 4-5: Hafif hasarr
  * 6-7: Orta-agir hasar
  * 7+: Yikici deprem

DEPREMDEN KORUNMA:
- Depreme dayanikli bina yapimi (en onemli onlem)
- Cap-Yan-Kapan: Saga sola tutunarak cok, sagllam mobilya yanında kapan
  (Yeni yaklaasim: Deprem ani pozisyonu)
- Asansor KULLANILMAZ
- Merdivenlere yonelin
- Aciik alanda elektrik diregi, bina kenarlarindan uzak dur
- Afet cantasi hazir bulundurulmali
- AFAD deprem toplanma noktalarini bilin

═══════════════════════════
2. VOLKAN (YANARDAG):
═══════════════════════════
- Yerin derinliklerindeki magmanin yeryuzune cikmasiyla olusan dogal yapilar
- Magma yeryuzune cikinca LAV adini alir
- Lav sicakligi: 700-1200°C
- Volkanik malzemeler: Lav, kul, gaz, pomza tasi, volkanik bomba

VOLKAN TURLERI:
1. Aktif volkan: Halen faaliyette veya yakin zamanda patlama gerceklesmis
2. Uyuyan volkan: Uzun suredir patlamayan ama potansiyeli olan
3. Sonmus volkan: Tamamen faaliyetini yitirmis

VOLKANIK ETKILER:
- Olumsuz: Can/mal kaybi, hava kirliligi, iklim degisikligi (kul bulutu)
- Olumlu: Verimli topraklar olusturur, jeotermal enerji kaynagi, yeni kara olusumu

═══════════════════════════
3. EROZYON:
═══════════════════════════
- Topragin su, ruzgar ve yercekimi etkisiyle asinarak tasinmasi
- Dogal bir surectir ama insan faaliyetleri hizlandirir

EROZYON NEDENLERI:
- Ormanlarin kesilmesi (en onemli neden)
- Bitki ortusunun tahrip edilmesi
- Asiri otlatma
- Yanlis arazi kullanimi
- Egimli arazilerde yanlis tarim

EROZYON ONLEME:
- Agaclandirma ve bitki ortusunu koruma
- Teraslama (egimli arazide basamak tarim)
- Rotasyon (nöbetlese ekim)
- Ruzgar perdesi (agac sirasi dikme)
- Asiri otlatmanin onlenmesi

═══════════════════════════
4. HEYELAN:
═══════════════════════════
- Toprak veya kaya kutlelerinin egim yonunde kayarak yer degistirmesi
- Genellikle yogun yagislar sonrasi olusur
- Egimli, ormansiz, gevssek zeminlerde sik gorulur

HEYELAN NEDENLERI:
- Yogun yagis (zemin suya doyar)
- Egimli arazi
- Deprem
- Orman tahribi
- Yanlis kazı ve insaat calimalari

HEYELANDAN KORUNMA:
- Egimli arazilerde agaclandirma
- Drenaj kanallari yapma (su birikmesini onleme)
- Istinat duvarlari insa etme
- Heyelan riski olan bolgelerrde yerlesim kurulmamalı

═══════════════════════════
5. DIGER DOGAL AFETLER:
═══════════════════════════
- Sel/Tasskin: Asiri yagis sonucu sularin tasmasi
- Cigr: Dag yamacindan kar kutlesinin kaymaasi
- Tsunami: Deniz dibindeki depremler sonucu olusan dev dalgalar
- Hortum/Kasirga: Siddetli atmosferik olaylar

GENEL AFET HAZIRLIK:
- Afet ve acil durum cantasi hazirla (su, yiyecek, ilk yardim, fener, dueduek)
- Aile iletisim plani olustur
- AFAD toplanma alanlarini ogren
- Ilk yardim bilgisi edin
- Binalarin deprem dayaniklilıgini kontrol et
- 112 Acil, AFAD: 122 numaralarini bil
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_fen6_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in FEN_6_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_fen6_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(FEN_6_REFERANS.keys())
