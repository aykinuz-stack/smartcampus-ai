# -*- coding: utf-8 -*-
"""
11. Sinif Cografya dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Nufus (dunya nufusu, dagilisi, nufus politikalari)
2. Gocler (goc turleri, nedenleri, sonuclari)
3. Kuresel Ticaret (uluslararasi ticaret, ekonomik orgutler)
4. Kalkinma (gelismislik, insani gelisme endeksi)
5. Enerji Kaynaklari (fosil yakit, yenilenebilir enerji)
6. Cevre ve Toplum (cevre sorunlari, surdurulebilirlik)
7. Dogal Afetler ve Yonetimi (afet turleri, risk azaltma)
8. Bolgesel Cografya (kuresellesme, bolgesel farklilasma)
"""

COGRAFYA_11_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: NUFUS
# ═══════════════════════════════════════════════════════════════

"COG.11.1.DUNYA_NUFUSU": {
    "unite": "Nufus",
    "baslik": "Dunya Nufusu ve Dagilisi",
    "icerik": """
DUNYA NUFUSU VE DAGILISI:

1. NUFUS DAGILISINI ETKILEYEN FAKTÖRLER:
   a) Dogal Faktorler:
      - Iklim: Iliman iklim bölgeleri yogun nufusludur
      - Yer sekilleri: Ovalik alanlar daglara göre daha yogun nufuslanir
      - Su kaynaklari: Akarsu boyları ve kiyilar yogun nufusludur
      - Toprak verimililigi: Verimli topraklar nufusu ceker
   b) Beseri Faktorler:
      - Sanayilesme: Sanayi bolgeleri goc alir
      - Ulasim: Ulasim aglarina yakin bolgeler avantajlidir
      - Tarihi birikim: Eski medeniyet merkezleri yogun nufusludur
      - Turizm ve ticaret: Ekonomik firsatlar nufusu etkiler

2. YOGUN NUFUSLU BOLGELER:
   - Guney Asya (Hindistan, Bangladesh): Monsun iklimi, verimli ovalar
   - Dogu Asya (Cin, Japonya): Tarim alanlari, sanayilesme
   - Bati Avrupa: Sanayilesme, gelismis ekonomi
   - Kuzey Amerika dogu kiyisi: Ekonomik faaliyet yogunlugu

3. SEYREK NUFUSLU BOLGELER:
   - Kutup bolgeleri: Asiri soguk, tarim yapilamaz
   - Coller (Sahra, Gobi): Su kitligi, asiri sicaklik
   - Yuksek daglik alanlar: Sert iklim, ulasim zorlugu
   - Yogun orman alanlari (Amazon): Ulasim ve yerlesmee zorlugu

4. NUFUS ARTIS HIZI:
   - Dogal nufus artisi = Dogum orani - Olum orani
   - Gelismis ulkelerde artis hizi dusuktur (<%1)
   - Gelismemis ulkelerde artis hizi yuksektir (>%2)
   - Dunya nufusu 8 milyari asmistir (2024)
"""
},

"COG.11.1.NUFUS_POLITIKALARI": {
    "unite": "Nufus",
    "baslik": "Nufus Politikalari ve Demografik Donusum",
    "icerik": """
NUFUS POLITIKALARI:

1. NUFUS ARTISINI ONLEMEYE YONELIK POLITIKALAR:
   - Aile planlamasi programlari
   - Egitim seviyesinin yukseltilmesi (ozellikle kadin egitimi)
   - Ekonomik tesvik/caydiricilar
   - Ornek: Cin'in eski tek cocuk politikasi, Hindistan'in aile planlamasi

2. NUFUS ARTISINI TESVIK EDEN POLITIKALAR:
   - Dogum yardimi ve cocuk paraasi
   - Annelik/babalik izni haklari
   - Vergi indirimleri
   - Ornek: Fransa, Almanya, Japonya, Turkiye

3. DEMOGRAFIK DONUSUM MODELI:
   - 1. Asama: Yuksek dogum, yuksek olum → yavas artis (geleneksel toplum)
   - 2. Asama: Yuksek dogum, dusen olum → hizli artis (gelisen toplum)
   - 3. Asama: Dusen dogum, dusuk olum → yavaslayan artis (gelismis toplum)
   - 4. Asama: Dusuk dogum, dusuk olum → duragan/azalan nufus
   - 5. Asama: Cok dusuk dogum → nufus azalmasi (Japonya, Guney Kore)

4. NUFUS PIRAMITLERI:
   - Genis tabanli (uc seklinde): Genc nufus yogun, az gelismis ulkeler
   - Arı kovani seklinde: Dengeli dagılim, gelisen ulkeler
   - Tersine piramit: Yasli nufus yogun, gelismis ulkeler (Almanya, Japonya)

5. NUFUS YAPISI GOSTERGELERI:
   - Medyan yas: Nufusun yarısinin uzerinde ve altinda kaldigi yas
   - Bagimlilik orani: (0-14 yas + 65+ yas) / Calisma cagi nufusu
   - Dogurganlik hizi: Bir kadinin yasami boyunca ortalama cocuk sayisi
   - Nufus yenileme hizi: 2.1 cocuk (nesil yenilenmesi icin gerekli)
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: GOCLER
# ═══════════════════════════════════════════════════════════════

"COG.11.2.GOC_TURLERI": {
    "unite": "Gocler",
    "baslik": "Goc Turleri, Nedenleri ve Sonuclari",
    "icerik": """
GOCLER:

1. GOC CESITLERI:
   a) Surelerine gore:
      - Mevsimlik goc: Belli donemlerde yapilir (tarim iscileri, yaylacılık)
      - Gecici goc: Belirli sure icin (ogrenim, is, askerlik)
      - Surekli goc: Kalici yerlesim degisikligi
   b) Yapilis sekillerine gore:
      - Gonullu goc: Kendi iradesiyle (is, egitim)
      - Zorunlu goc: Mecbur kalinarak (savas, afet, surgun)
   c) Mekansal olarak:
      - Ic goc: Ulke sinirları icinde (kirdan kente, kentten kente)
      - Dis goc: Ulke sinirlarini asan goc (isci gocu, multeci akini)
      - Beyin gocu: Nitelikli isgucunun yurt disina cikmasi

2. GOC NEDENLERI:
   - Ekonomik: Issizlik, dusuk gelir, is imkani arayisi
   - Siyasi: Savas, ic karisiklik, baski rejimi
   - Sosyal: Egitim, saglik hizmeti, yasam kalitesi
   - Dogal: Deprem, kuraklik, sel, volkan
   - Dini/etnik: Ayrimcilik, zuulum

3. GOCUN SONUCLARI:
   a) Goc veren bolgede:
      - Nufus azalir, yaslanir
      - Isgücu kaybi, ekonomik gerileme
      - Tarimsal uretim duser
      - Sosyal yapiyla zayiflar
   b) Goc alan bolgede:
      - Nufus artar, genclesir
      - Isgucü kazanci, ekonomik canlanma
      - Cehre sorunlari, altyapi yetersizligi
      - Kulturel etkilesim ve uyum sorunlari

4. KURESEL GOC AKIMLARI:
   - Guney → Kuzey: Afrika/Ortadogu'dan Avrupa'ya
   - Latin Amerika → Kuzey Amerika
   - Guney Asya / Guneydogu Asya → Korfez ulkeleri
   - Suriye ic savasi → Turkiye, Lubnan, Avrupa multeci krizi
   - Beyin gocu: Gelismekte olan ulkelerden gelismis ulkelere
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: KURESEL TICARET
# ═══════════════════════════════════════════════════════════════

"COG.11.3.KURESEL_TICARET": {
    "unite": "Kuresel Ticaret",
    "baslik": "Uluslararasi Ticaret ve Ekonomik Orgutler",
    "icerik": """
KURESEL TICARET:

1. ULUSLARARASI TICARET:
   - Her ulke her uruunu yeterli miktarda uretememektedir
   - Karsilıklı bagimlilik uluslararasi ticareti zorunlu kilar
   - Ihracat: Ulke disinaa mal/hizmet satimi
   - Ithalat: Ulke disından mal/hizmet alimi
   - Dis ticaret dengesi = Ihracat - Ithalat (fazla veya acik)

2. TICARETI ETKILEYEN FAKTORLER:
   - Dogal kaynaklar: Petrol, madenler, tarim urunleri
   - Teknoloji duzeyi: Katma degeri yuksek urun uretimi
   - Ulasim aglari: Limanlarin, hava/kara yollarinin gelismisligi
   - Ekonomik politikalar: Gumruk vergileri, serbest ticaret anlasmalaari
   - Kur politikasi: Ulusal para biriminin degeri

3. EKONOMIK ORGUTLER:
   - DTÖ (Dunya Ticaret Orgutu): Uluslararasi ticaretin kurallarini belirler
   - AB (Avrupa Birligi): Ortak pazar, serbest dolasim, Euro
   - NAFTA/USMCA: ABD, Kanada, Meksika serbest ticaret anlasmasi
   - OPEC: Petrol ihrac eden ulkeler orgutu (fiyat kontrolu)
   - ASEAN: Guneydogu Asya ulkeleri birligi
   - G7/G20: Buyuk ekonomilerin isbirligi platformlari
   - BRICS: Brezilya, Rusya, Hindistan, Cin, Guney Afrika (yukselen ekonomiler)

4. SERBEST BOLGELER VE LIMANLAR:
   - Serbest ticaret bolgeleri: Gumruksuz veya dusuk gumruklu ticaret alanlari
   - Dunya'nin onemli limanlari: Sanghay, Singapur, Rotterdam
   - Turkiye'deki serbest bolgeler: Mersin, Ege, Antalya, Istanbul

5. KURESEL TICARET AKIMLARI:
   - Gelismis ulkeler: Sanayi ve teknoloji urunu ihrac eder
   - Gelismekte olan ulkeler: Hammadde ve tarim urunu ihrac eder
   - Esitsiz ticaret: Hammadde ucuz, islenmis urun pahali → ticaret acigi
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: KALKINMA
# ═══════════════════════════════════════════════════════════════

"COG.11.4.KALKINMA": {
    "unite": "Kalkinma",
    "baslik": "Gelismislik Gostergeleri ve Insani Gelisme",
    "icerik": """
KALKINMA VE GELISMISLIK:

1. KALKINMA KAVRAMI:
   - Ekonomik buyume: GSYH (Gayri Safi Yurt Ici Hasila) artisi
   - Kalkinma: Ekonomik buyume + sosyal gelisme + yasam kalitesi artisi
   - Bir ulke ekonomik olarak buyuyebilir ama kalkinamayabilir
   - Kalkinma daha genis ve kapsamli bir kavramdir

2. GELISMISLIK GOSTERGELERI:
   a) Ekonomik gostergeler:
      - Kisi basi GSYH (milli gelir)
      - Sektorel dagılım (tarim/sanayi/hizmet)
      - Ihracat/ithalat yapisi
      - Issizlik oranı
   b) Sosyal gostergeler:
      - Okur-yazarlik oranı, okullasmma oranı
      - Ortalama yasam suresi
      - Bebek olum orani
      - Saglik harcamalari / kisi basi doktor sayisi
   c) Demografik gostergeler:
      - Nufus artis hizi
      - Kentlesme orani
      - Medyan yas

3. INSANI GELISME ENDEKSI (IGE / HDI):
   - Birlesmis Milletler tarafindan hesaplanir
   - Uc temel boyut: Saglik, Egitim, Gelir
   - 0 ile 1 arasinda deger alir (1'e yakin = gelismis)
   - Cok yuksek IGE: Norvec, Isvicre, Avustralya
   - Dusuk IGE: Sahra alti Afrika ulkeleri

4. GELISMIS VE GELISMEMIS ULKE FARKLARI:
   - Gelismis: Hizmet sektoru agirlikli, dusuk nufus artisi, yuksek gelir
   - Gelismekte olan: Sanayi gelisiyor, orta gelir, hizli kentlesme
   - Az gelismis: Tarim agirlikli, yuksek nufus artisi, dusuk gelir

5. SURDURULEBILIR KALKINMA:
   - Bugunku nesillerin ihtiyaclarini karsilarken
     gelecek nesillerin kaynaklarini tuketmemek
   - BM Surdurulebilir Kalkinma Amaclari (17 hedef)
   - Yoksullugun sona erdirilmesi, acligin sonlandirilmasi,
     nitelikli egitim, temiz su, iklim eylemi vb.
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: ENERJI KAYNAKLARI
# ═══════════════════════════════════════════════════════════════

"COG.11.5.ENERJI_KAYNAKLARI": {
    "unite": "Enerji Kaynaklari",
    "baslik": "Fosil Yakitlar ve Yenilenebilir Enerji",
    "icerik": """
ENERJI KAYNAKLARI:

1. FOSIL YAKITLAR (TUKENEN KAYNAKLAR):
   a) Petrol:
      - Dunya'nin en onemli enerji kaynagi
      - Ulasim, petrokimya, plastik, ilacc sanayisinin hammaddesi
      - Baslica uretici ulkeler: Suudi Arabistan, ABD, Rusya, Irak, Kanada
      - OPEC ulkeleri dunya petrol uretiminin onemli kismini kontrol eder
      - Ortadogu dunyaa petrol rezervlerinin ~%48'ine sahiptir
   b) Dogalgaz:
      - Temiz fosil yakit (petrole gore daha az karbon emisyonu)
      - Isınma, elektrik uretimi, sanayi
      - Baslica uretici: ABD, Rusya, Iran, Katar
      - Boru hatlari ve LNG (sivilastirilmis dogalgaz) ile tasinir
   c) Komur:
      - Ilk kullanilan fosil yakit (Sanayi Devrimi)
      - En kirletici fosil yakit (yuksek karbon emisyonu)
      - Baslica uretici: Cin, Hindistan, ABD, Endonezya, Avustralya
      - Hala bazi ulkelerde elektrik uretiminin temelini olusturur

2. YENILENEBILIR ENERJI KAYNAKLARI:
   a) Gunes enerjisi: Gunes panelleri, sicak bolgelerde verimli
   b) Ruzgar enerjisi: Ruzgar turbinleri, kiyilar ve acik alanlar
   c) Hidroelektrik: Barajlar ve akarsu potansiyeli
   d) Jeotermal: Yer altı sicak su kaynaklari (Turkiye zengin)
   e) Biyokütle: Organik atıklardan enerji, biyoyakit
   f) Dalga/gelgit enerjisi: Okyanus enerjisi

3. ENERJI POLITIKALARI:
   - Enerji guevnligi: Ulkelerin enerji ihtiyacini kesintisiz karsilamasi
   - Enerji bagimliligi: Ithalata bagimli ulkelerde jeopolitik risk
   - Enerji donusumu: Fosil yakittan yenilenebilir enerjiye gecis trendi
   - Paris Iklim Anlasmasi: Karbon emisyonlarini azaltma taahhutleri

4. TURKIYE'NIN ENERJI PROFILI:
   - Enerjide disaa bagimlilik yuksek (petrol ve dogalgaz ithalati)
   - Hidroelektrik potansiyeli yuksek (Firat, Dicle, Coruh)
   - Jeotermal kaynaklarda dunya liderleri arasinda
   - Ruzgar ve gunes enerjisi yatirimlari artmakta
   - Nukleer enerji: Akkuyu NGS (Mersin) projesi
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: CEVRE VE TOPLUM
# ═══════════════════════════════════════════════════════════════

"COG.11.6.CEVRE_TOPLUM": {
    "unite": "Cevre ve Toplum",
    "baslik": "Cevre Sorunlari ve Surdurulebilirlik",
    "icerik": """
CEVRE VE TOPLUM:

1. KURESEL CEVRE SORUNLARI:
   a) Kuresel isinma ve iklim degisikligi:
      - Sera gazlari (CO2, metan) atmosferde birikerek sicakligi arttirir
      - Buzullarin erimesi, deniz seviyesinin yuukselmesi
      - Asiri hava olaylari: Kuraklik, sel, kasirga siddetinde artis
      - Paris Iklim Anlasmasi (2015): Sicaklik artisini 1.5°C ile sinirlandirma hedefi
   b) Ozon tabakasinin incelmesi:
      - CFC gazlari ozon tabakasina zarar verir
      - Montreal Protokolu (1987) ile CFC kullanimi yasaklandi
   c) Asit yagmurlari:
      - Fosil yakit yakilmasi sonucu SO2 ve NOx emisyonlari
      - Ormanlara, sulara, yapilara zarar verir
   d) Su kirliligi ve kitligi:
      - Sanayi atiklari, tarimsal kimyasallar, evsel atiklar
      - Dunya nufusunun onemli bir kismi temiz suya erisemiyor

2. ORMANSIZLASMA:
   - Amazon yagmur ormanlari hizla tahrip ediliyor
   - Tarim alani acma, odun/kereste uretimi, kentlesme
   - Biyocesitlilik kaybi, karbon depolama kapasitesinin azalmasi
   - Erozyon artisi, iklim degisikligine katki

3. CEVRE KORUMA YAKLASIMLARI:
   - Surdurulebilir kalkinma: Dogal kayniklarin dengeli kullanimi
   - Geri donusum ve atik yonetimi
   - Yesil enerji gecisi
   - Koruma alanlari: Milli parklar, biyosfer rezervleri
   - Uluslararasi anlasmlalar: Ramsar, CITES, Kyoto, Paris

4. EKOLOJIK AYAK IZI:
   - Bir kisinin/toplumun dogal kaynak tuketimi olcusu
   - Gelismis ulkelerde ekolojik ayak izi cok yuksek
   - Dunya'nin tasima kapasitesinin uzerinde tuketim yapiliyor
   - Bireysel onlemler: Enerji tasarrufu, toplu tasima, yerel tuketim
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. UNITE: DOGAL AFETLER VE YONETIMI
# ═══════════════════════════════════════════════════════════════

"COG.11.7.DOGAL_AFETLER": {
    "unite": "Dogal Afetler ve Yonetimi",
    "baslik": "Afet Turleri ve Risk Yonetimi",
    "icerik": """
DOGAL AFETLER VE YONETIMI:

1. JEOLOJIK KAYNAKLI AFETLER:
   a) Deprem:
      - Yer kabugunun kirilmasi sonucu oolusan titresimler
      - Fay hatlari uzerinde yogunlasir
      - Richter olcegi ile buyuklugu, Mercalli ile siddeti olculur
      - Turkiye, Alp-Himalaya deprem kusaginda yer alir
      - Kuzey Anadolu Fay Hatti (KAF), Dogu Anadolu Fay Hatti (DAF)
   b) Volkanizma:
      - Magmanin yer yuzune cikmaasi
      - Pasifik Ates Cemberi: En yogun volkanik faaliyet kusagi
      - Lav akintisi, kul bulutu, tsunami tetikleme riski
   c) Heyelan:
      - Yamaclardaki toprak/kaya kutlesinin kayması
      - Ağir yagis, deprem, ormansızlasma tetikler
      - Karadeniz Bolgesi heyelan riski yuksek

2. METEOROLOJIK / KLIMATOLOJIK AFETLER:
   - Sel ve taşkin: Sağanak yağis, yetersiz altyapi
   - Kuraklik: Uzun sureli yagis yoklugu, su kitligi
   - Kasirga/tayfun: Tropikal bolgelerde olusan siddetli firtinalar
   - Cig: Daglik bolgelerde kar kutlesinin kayması
   - Don olayı: Tarimsal uretime zarar

3. AFET RISK YONETIMI:
   a) Zarar azaltma (Hazirlik oncesi):
      - Risk analizi ve haritaliama
      - Imar planlari ve yapı denetimi
      - Depreme dayanikli yapi tasarimi
      - Erken uyari sistemleri
   b) Hazirlik:
      - Afet egitimi ve tatbikatlari
      - Afet canta hazirligii
      - Toplanma alanlari belirleme
      - AFAD ve sivil toplum koordinasyonu
   c) Mudahale:
      - Arama kurtarma (AFAD, AKUT, STK'lar)
      - Ilk yardim ve saglik hizmetleri
      - Barinma ve beslenme
   d) Iyilestirme:
      - Yaralaarin sarilmasi, psikolojik destek
      - Yeniden insaa
      - Daha dayaniikli yapilasma

4. TURKIYE VE AFET RISKI:
   - 1. derece deprem bolgesinde nufusun büyük kismi yasar
   - 6 Subat 2023 Kahramanmaras depremleri: Buyuk yikim
   - AFAD: Afet ve Acil Durum Yonetimi Baskanligi
   - Zorunlu deprem sigortasi (DASK)
"""
},

# ═══════════════════════════════════════════════════════════════
# 8. UNITE: BOLGESEL COGRAFYA VE KURESELLESME
# ═══════════════════════════════════════════════════════════════

"COG.11.8.KURESELLESME": {
    "unite": "Bolgesel Cografya ve Kuresellesme",
    "baslik": "Kuresellesme, Bolgesel Farklilasmalar",
    "icerik": """
KURESELLESME VE BOLGESEL COGRAFYA:

1. KURESELLESME KAVRAMI:
   - Ulkeler arasi ekonomik, kulturel, siyasi ve teknolojik entegrasyon
   - Iletisim ve ulasim teknolojilerindeki gelismelerle hiz kazanmistir
   - "Kuresel koy" kavrami: Dunya'nın kuculmesi metaforu
   - Sermaye, mal, hizmet ve bilginin serbestce dolaasimi

2. KURESELLESMENIN BOYUTLARI:
   a) Ekonomik boyut:
      - Cok uluslu sirketler (Apple, Samsung, Toyota)
      - Serbest ticaret anlasmalari
      - Kuresel tedarik zincirleri
      - Dogrudan yabanci yatirim
   b) Kulturel boyut:
      - Kuresel markalar, fast-food zincileri
      - Sosyal medya ve kuresel iletisim
      - Kulturel homojenlesme vs. yerel direnis
   c) Siyasi boyut:
      - Uluslararasi orgutler (BM, NATO, AB)
      - Insan haklari evrensel beyannaamesi
      - Kuresel yonetisim sorunlari

3. KURESELLESMENIN OLUMLU YONLERI:
   - Ekonomik buyume ve refah artisi
   - Teknoloji ve bilgi transferi
   - Kulturel etkilesim ve zenginlesme
   - Kuresel sorunlara ortak cozum uretme imkani

4. KURESELLESMENIN OLUMSUZ YONLERI:
   - Gelir esitsizliginin artmasi (Kuzey-Guney ucurumu)
   - Yerel kulturlerin assinmasi
   - Cevre tahribati (aşırı uretim/tuketim)
   - Ekonomik krizlerin hizla yayilmasi (domino etkisi)
   - Gelismemis ulkelerin hammadde deposu olarak kalma riski

5. BOLGESEL FARKLILASMA:
   - Kuzey-Guney ayirimi: Gelismis (Kuzey) vs az gelismis (Guney)
   - Merkez-cevre teorisi: Gelismis ulkeler merkez, digerleri cevre
   - Bolgesel entegrasyonlar: AB, ASEAN, Afrika Birligi, Mercosur
   - Jeostrateji: Enerji koridorlari, bogazlar, ticaret yollari
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_cografya11_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in COGRAFYA_11_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_cografya11_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(COGRAFYA_11_REFERANS.keys())
