# -*- coding: utf-8 -*-
"""
10. Sinif Cografya dersi
MEB 2025 mufredatina uygun referans verileri.

Uniteler:
1. Dunya'nin Sekli ve Hareketleri
2. Atmosfer ve Sicaklik
3. Iklim Tipleri
4. Basinc ve Ruzgarlar
5. Nem-Yagis-Buharlaşma
6. Su Cografyasi (Akarsular, Goller, Okyanuslar)
"""

COGRAFYA_10_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: DUNYA'NIN SEKLI VE HAREKETLERI
# ═══════════════════════════════════════════════════════════════

"COG.10.1.DUNYA_SEKLI": {
    "unite": "Dunya'nin Sekli ve Hareketleri",
    "baslik": "Dunya'nin Sekli ve Boyutlari",
    "icerik": """
DUNYA'NIN SEKLI:
- Dunya tam bir kure degildir; kutuplardan basik, ekvatordan siskin bir geoiddir.
- Ekvator cevresi: yaklasik 40.076 km.
- Kutuplar arasi cevre: yaklasik 40.009 km (ekvatordan daha kisa).
- Ekvator yaricapi: 6.378 km; kutup yaricapi: 6.357 km.
- Bu fark Dunya'nin kendi ekseni etrafinda donmesinden kaynaklanir.

DUNYA'NIN SEKLINE KANITLAR:
- Gemilerin ufukta once diregi, sonra govdesi gorunur.
- Ay tutulmasinda Dunya'nin golgesi dairedir.
- Kuzey Yildizi'nin gozlem acisi enlemle degisir.
- Uzaydan cekilen fotograflar.
- Farkli enlemlerde cisimlerin golge boylarinin farkli olmasi.

KOORDINAT SISTEMI:
- Enlem: Ekvatora paralel daireler (0°-90° Kuzey/Guney).
  Ekvator: 0°, Yengec Donencesi: 23°27' K, Oglak Donencesi: 23°27' G,
  Kuzey Kutup Dairesi: 66°33' K, Guney Kutup Dairesi: 66°33' G.
- Boylam: Kutupları birlestiren yarim daireler (0°-180° Dogu/Bati).
  Baslangiç meridyeni: Greenwich (0°).
- Her derece enlem arasi mesafe yaklasik 111 km'dir.
- Her derece boylam arasi mesafe ekvatorda 111 km, kutuplara dogru azalir.
"""
},

"COG.10.1.DUNYA_HAREKETLERI": {
    "unite": "Dunya'nin Sekli ve Hareketleri",
    "baslik": "Dunya'nin Günlük ve Yillik Hareketleri",
    "icerik": """
GUNLUK HAREKET (EKSEN HAREKETI):
- Dunya kendi ekseni etrafinda bati-dogu yonunde doner.
- Bir tam donusu 23 saat 56 dakika 4 saniyedir (yaklasik 24 saat).
- Sonuclari:
  1. Gece-gunduz olur (aydinlik ve karanlik yarikure).
  2. Yerel saat farkliliklari olusur (15 boylam = 1 saat fark).
  3. Doguya gidildiginde saat ileri, batiya gidildiginde geri alinir.
  4. Coriolis etkisi: Hareketli cisimler K yarikurede saga, G yarikurede sola sapar.
  5. Gel-git olayinda yardimci etken.

YILLIK HAREKET (YÖRÜNGE HAREKETI):
- Dunya, Gunes etrafinda eliptik yörüngede doner.
- Bir tam donusu 365 gun 6 saattir (1 yıl). Fazladan 6 saat 4 yilda 1 gun yapar (artik yil).
- Dunya'nin ekseni yorunge duzlemine 23°27' egiktir ve bu egiim hep ayni yone bakar.
- Sonuclari:
  1. Mevsimler olusur (eksen eğimligi nedeniyle Gunes isinlarinin gelis acisi degisir).
  2. Gece-gunduz sureleri degisir (yaz yarikuresinde gunduz uzun, kis yarikuresinde kisa).
  3. Isinim farklilasmasi: Gunes'e dik aciyla alinana isinlar en yoğun ısıtır.

OZEL GUNLER:
- 21 Mart (Ilkbahar ekinoksu): Gunes Ekvator'a dik. Gece = Gunduz (12 saat).
- 21 Haziran (Yaz gun donumu): Gunes Yengec Donencesi'ne dik. K yarikurede en uzun gunduz.
- 23 Eylul (Sonbahar ekinoksu): Gunes tekrar Ekvator'a dik. Gece = Gunduz.
- 21 Aralik (Kis gun donumu): Gunes Oglak Donencesi'ne dik. K yarikurede en kisa gunduz.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: ATMOSFER VE SICAKLIK
# ═══════════════════════════════════════════════════════════════

"COG.10.2.ATMOSFER": {
    "unite": "Atmosfer ve Sicaklik",
    "baslik": "Atmosferin Yapisi ve Isinma",
    "icerik": """
ATMOSFER KATMANLARI:
1. Troposfer (0-12 km):
   - Hava olaylari (yagis, bulut, rüzgar) burada gerceklesir.
   - Yukseldikce sicaklik duşer (her 200 m'de yaklasik 1°C azalır).
   - Atmosferin kutle olarak %75'i burada bulunur.
   - Kalınlığı ekvatorda fazla (~17 km), kutuplarda az (~8 km).

2. Stratosfer (12-50 km):
   - Ozon tabakasi burada bulunur (20-25 km).
   - Ozon, Gunes'in zararli UV isinlarini emer.
   - Yukseldikce sicaklik artar (ozon isinlari emmesi nedeniyle).
   - Ucaklar bu katmanin alt bolumunde ucar (hava olaylari yok).

3. Mezosfer (50-80 km):
   - En soguk katman (yaklasik -90°C'ye dusen sicakliklar).
   - Meteorlar burada yanar (kayan yildiz).

4. Termosfer (80-700 km):
   - Sicaklik cok yuksektir (1000°C ustu) ancak molekul sayisi az.
   - Kutup isiklari (aurora) burada olusur.
   - Radyo dalgalari bu katmandan yansir.

5. Ekzosfer (700+ km):
   - Atmosferin en dis katmani, uzaya gecis bolgesi.

ATMOSFERIN BILEŞIMI:
- %78 Azot (N₂), %21 Oksijen (O₂), %0,93 Argon (Ar), %0,04 Karbondioksit (CO₂).
- Su buhari, toz parcaciklari ve diger gazlar (eser miktarda).
"""
},

"COG.10.2.SICAKLIK": {
    "unite": "Atmosfer ve Sicaklik",
    "baslik": "Sicaklik Dagılışı ve Etkileyen Faktorler",
    "icerik": """
SICAKLIGI ETKILEYEN FAKTORLER:

1. ENLEM:
   - Ekvatordan kutuplara gidildikce sicaklik azalir.
   - Gunes isinlarinin gelis acisi enlemle degisir (dik aciyla gelen isinlar daha cok isitir).
   - Tropikal bölgeler sicak, kutuplar soguktur.

2. YÜKSEKLIK:
   - Yukseklik arttikca sicaklik duşer.
   - Her 200 m'de ortalama 1°C azalir (sicaklik gradyani).
   - Dağ zirvelerinde kar ve buzullar bulunur.

3. KARASALLIK VE DENIZSELLIK:
   - Deniz kenarinda sicaklik farklari az (ılıman / okyanusal).
   - Ic kesimlerde sicaklik farklari buyuk (karasal iklim).
   - Suyun ozel isisi yuksek oldugu icin yavas isinir yavas sogur.

4. OKYANUS AKINTILARI:
   - Sicak akıntilar: Gecgtikleri kıyilarda sicakligi artirır. Ornek: Gulf Stream.
   - Soguk akintilar: Kiyilarda sicakligi dusurur. Ornek: Labrador.

5. BAKI (YAMAÇ YÖNÜ):
   - Güneye bakan yamaclar (K yarikure) daha fazla Gunes isigi alir (daha sıcak).
   - Kuzeye bakan yamaclar daha az isik alir (daha serin, kar daha gec erir).

6. BITKI ORTUSU:
   - Ormanlik alanlar sicaklik farkini azaltır (golgeler, nem tutar).
   - Cilak arazilerde gunduz-gece sicaklik farki buyuktur.

SICAKLIK HARITALARI:
- Izoterm: Ayni sicakliktaki noktalari birlestiren egri.
- Izotermler ekvatora paralel uzanır ancak kara-deniz dagilimi nedeniyle bozulur.
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: IKLIM TIPLERI
# ═══════════════════════════════════════════════════════════════

"COG.10.3.IKLIM_TIPLERI": {
    "unite": "Iklim Tipleri",
    "baslik": "Dunya Iklim Tipleri",
    "icerik": """
SICAK IKLIMLER:

1. Ekvatoral Iklim:
   - Ekvator cevresinde (0-10° enlemler).
   - Yil boyunca sicak ve yagisli. Yillik sicaklik farki az.
   - Konveksiyonel yagislar (ogle saatlerinde saganak).
   - Bitki ortusu: Tropikal yagmur ormanlari (Amazon, Kongo).

2. Tropikal (Savana) Iklim:
   - 10-20° enlemler arasi.
   - Yaz yagisli, kis kurak.
   - Bitki ortusu: Uzun otlar ve seyrek agaclar (savan).
   - Afrika, Guney Amerika, Guney Asya.

3. Cöl (Kurak) Iklim:
   - Donenceler civarinda (20-30° enlemler).
   - Cok az yagis (yillik < 250 mm).
   - Gunduz-gece sicaklik farki cok buyuk.
   - Bitki ortusu: Kaktus, diken, cok seyrek.
   - Sahra, Arabistan, Gobi colleri.

ILIMAN IKLIMLER:

4. Akdeniz Iklimi:
   - 30-40° enlemler, kitalarin bati kiyilari.
   - Yaz sicak ve kurak, kis ilik ve yagisli.
   - Bitki ortusu: Maki (sert yaprakli, herdem yesil calilar).
   - Akdeniz kiyilari, Kaliforniya, Sili.

5. Okyanus (Bati Avrupa) Iklimi:
   - 40-60° enlemler, kitalarin bati kiyilari.
   - Yil boyunca iliman ve yagisli. Yazlar serin, kislar ilik.
   - Bitki ortusu: Yaprak doken ormanlar, cayirlar.
   - Bati Avrupa, Britanya Adalari, Yeni Zelanda.

6. Karasal Iklim:
   - Ic kesimler, deniz etkisinden uzak bolgeler.
   - Yazlar sicak, kislar cok soguk. Yillik sicaklik farki buyuk.
   - Yagislar az veya orta duzey.
   - Bitki ortusu: Bozkir (step). Orta Asya, ic Anadolu.

SOGUK IKLIMLER:
7. Tundra: Kutup cerclesinde. Yaz kisa ve serin. Buzullar, yosun-liken.
8. Kutup (Buz): Yil boyu soguk. Grönland, Antarktika.
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: BASINC VE RUZGARLAR
# ═══════════════════════════════════════════════════════════════

"COG.10.4.BASINC_RUZGAR": {
    "unite": "Basinc ve Ruzgarlar",
    "baslik": "Atmosfer Basinci ve Ruzgar Sistemleri",
    "icerik": """
ATMOSFER BASINCI:
- Havanin agirligindan kaynaklanan kuvvettir.
- Deniz seviyesinde ortalama: 1013 hPa (milibar) = 760 mmHg.
- Basinci etkileyen faktorler:
  1. Yükseklik: Arttikça basinc azalir.
  2. Sicaklik: Arttikca hava genlesir, yükselir, basinc azalir (alcak basinc).
                Azaldikca hava sogur, coker, basinc artar (yuksek basinc).
  3. Nem: Nemli hava kuru havadan hafiftir (dusuk basinc).
- Izobar: Ayni basincli noktalari birlestiren egri.

RUZGAR KAVRAMI:
- Yuksek basinc alanlarindan alcak basinc alanlarina dogan hava akimidir.
- Basinc farki arttikca ruzgar hizi artar.
- Coriolis etkisi: K yarikurede saga, G yarikurede sola saptirir.

SUREIKLI (GEZEGENSEL) RUZGARLAR:
1. Alize ruzgarlari: 30° enlmelerden ekvatora dogru eser.
   K yarikurede KD, G yarikurede GD yonundedir.
2. Bati ruzgarlari: 30-60° enlemler arasi, batidan doguya.
   Okyanus ikliminin ic kesimlere tasınmasında etkili.
3. Kutup ruzgarlari: Kutuplardan 60° enlemlere dogru soğuk ruzgarlar.

MEVSIMLIK RUZGARLAR:
- Muson: Yaz ve kis mevsimlerinde yon degistiren ruzgar.
  Yaz musonu: Okyanustan karaya (yagisli). Kis musonu: Karadan okyanusa (kurak).
  Guney ve Guneydogu Asya'da etkili (Hindistan, Bangladesh).

YEREL RUZGARLAR:
- Meltem: Gunduz denizden karaya (deniz meltemi), gece karadan denize (kara meltemi).
- Fon (foehn): Dagı asan havanin kuru ve sicak inmesi.
- Lodos: Guneybatidan esen sicak ruzgar (Marmara).
- Poyraz: Kuzeydogudan esen soguk ruzgar (Marmara).
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: NEM-YAGIS-BUHARLAŞMA
# ═══════════════════════════════════════════════════════════════

"COG.10.5.NEM_YAGIS": {
    "unite": "Nem-Yagis-Buharlaşma",
    "baslik": "Nem, Buharlaşma ve Yagis Turleri",
    "icerik": """
NEM KAVRAMI:
- Havadaki su buhari miktaridir.
- Mutlak nem: Birim hacimdeki su buhari miktari (g/m³).
- Bagil nem: Havadaki su buharinin, havani tasiyabilecegi maksimum su buhari
  miktarina orani (%). Bagil nem = (Mutlak nem / Maksimum nem) × 100
- Sicaklik artinca havanin su buhari tasima kapasitesi artar.
- Bagil nem %100 olursa hava doygun hale gelir → yogunlasma baslar.
- Cigilenme (cig noktasi): Havanin soguyarak doygun hale geldigi sicaklik.

BUHARLAŞMA:
- Sivi suyun gaz haline (su buhari) donusmesi.
- Buharlaşmayi artiran faktorler: Sicaklik artisi, ruzgar, nem azligi, su yuzeyi geniisligi.
- Buharlaşma ekvator cevresinde ve collerde fazla, kutuplarda azdir.

YOGUNLAŞMA VE YAGIS:
- Su buharinin soguyarak sivi veya kati hale donusmesi yogunlaşmadir.
- Yogunlaşma icin: Havanin sogumasi + yogunlasma cekirdegi (toz, polen) gerekir.

YAGIS TURLERI:
1. Konveksiyonel (yükselim) yagis:
   - Isinanan hava yukselir, sogur, yogunlaşır, yagis olusur.
   - Ekvator kusaginda ve yaz mevsiminde yaygın.
   - Saganak ve gok gurultulu.

2. Orogafik (yamaç) yagis:
   - Nemli hava dagla karsilasinca yükselir ve soguyarak yagis birakir.
   - Ruzgara bakan yamaç (rzgaralti) yagisli, arka yamaç (rzgarustu) kurak.

3. Cephesel (frontal) yagis:
   - Sicak ve soguk hava kutlelerinin karsilasmasiyla olusur.
   - Iliman kusak'ta yaygındir. Uzun sureli, genis alanli yagislar.

YAGIS BICIMLERI:
- Yagmur: Sivi su damlalari (sicaklik 0°C ustu).
- Kar: Buz kristalleri (sicaklik 0°C alti).
- Dolu: Buyuk buz parcaciklari (saganak sirasinda dikey hava akimlari).
- Ciselenme: Cok ince yagmur damlalari.
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: SU COGRAFYASI
# ═══════════════════════════════════════════════════════════════

"COG.10.6.AKARSULAR": {
    "unite": "Su Cografyasi",
    "baslik": "Akarsular ve Akarsu Ozellikleri",
    "icerik": """
AKARSU KAVRAMI:
- Belirli bir yatak icinde akan su kutlesidir.
- Kaynak: Akarsuyun cikis noktasi (pinar, gol, buzul).
- Agiz (mansap): Akarsuyun deniz/gol/baska akarsuya kavustugu nokta.
- Havza: Bir akarsuyun sularını topladigi alan.
- Su bolumu cizgisi: Komsu havzalari ayiran sinir.

AKARSU REJIMI:
- Akarsuyun yil boyunca akim (debi) degisimidir.
- Duzensiz rejim: Akim mevsimden mevsime cok degisir (Akdeniz ikliml akarslular).
- Duzenli rejim: Akim yil boyunca yaklasik sabit (ekvator kusagi akarslular).
- Karma rejim: Birden fazla kaynakla beslenen akarsularda gorutur.

AKARSU ASINMA VE BIRIKTIRME:
- Asinma (erozyon): Akarsuyun yatak ve kıyilarini asindirilmasi.
  Ust cığır: Dik egim, derin vadiler, cevrinti (V vadi), selale.
  Orta cığır: Menderes, yanal asinma.
  Alt cığır: Delta ovaları, biriktirme, genis yataklar.
- Delta: Akarsuyun agzında bilaiktirdiği malzemenin olusturdugu duzluk.
  Durgun denizlerde olusur (gel-git az ise). Cukurova, Nil deltasi.
- Haliç (Estuar): Gel-git etkisiyle genislemis akarsu agzi. Thames, Elbe.

AKARSU HIDROGRAFISI:
- Debi (akim): Birim zamanda akan su miktari (m³/s).
- Akim katsayisi: Yillik yagis miktarinin yillik akisa orani.
- Havza buyuklugu, iklim, bitki ortusu, arazi yapisi debiyi etkiler.
"""
},

"COG.10.6.GOLLER_OKYANUSLAR": {
    "unite": "Su Cografyasi",
    "baslik": "Goller, Okyanuslar ve Yeraltı Sulari",
    "icerik": """
GOLLER:
- Karalardaki cukur alanlarda biriken su kutleleridir.

Olusumuna gore gol turleri:
1. Tektonik goller: Fay kırılmasiyla olusan cukurluklarda. Ornek: Hazar, Baykal.
2. Volkanik goller: Volkan kraterinde veya maar cukurunda. Ornek: Nemrut Golu.
3. Buzul golleri: Buzulların oyduğu cukurlarda. Ornek: Fin golleri, Buyuk Goller.
4. Set golleri: Heyelan, lav, aluvyon, buzul setleriyle olusmus.
   Ornek: Tortum Golu (heyelan), Van Golu (lav seti).
5. Dogal set (Lagün): Kıyıda kum birikimiyle denizden ayrilan gol. Ornek: Küçükçekmece.

Suyuna gore goller:
- Tatli su goller: Gideri (akarsuyun ciktigi) olan goller. Beyşehir, Burdur.
- Tuzlu goller: Gideri olmayan goller (buharlaşmayla su kaybi). Tuz Golu, Lut Golu.

OKYANUSLAR VE DENIZLER:
- Buyuk Okyanus (Pasifik): Dunyanin en buyuk okyanusu.
- Atlas Okyanusu (Atlantik): Ikinci en buyuk.
- Hint Okyanusu: Ucuncu en buyuk.
- Kuzey Buz Denizi (Arktik): En kucuk okyanus.
- Tuzluluk ortalamasi: %3,5 (binde 35).
  Tuzlulugu artiran: Buharlaşma, donma.
  Tuzlulugu azaltan: Yagış, akarsu agizlari, buzul erimesi.

GEL-GIT:
- Ay ve Gunes'in cekim kuvveti etkisiyle deniz suyunun yükselmesi ve alçalmasidir.
- Günde 2 kez gel-git olur (yaklasık 6 saat arayla).
- Gel-git genliği: Okyanusların açik bölgelerinde az, dar korfezlerde buyuktur.

YERALTI SULARI:
- Yağisin toprak altina sizan kismı yeraltı suyunu oluşturur.
- Gecirimsiz tabaka uzerinde birikir.
- Artezyen: Basincli yeralti suyu kaynagi (iki gecirimsiz tabaka arasi).
- Karstik kaynaklar: Kireçtaşı bolgelerinde yeraltı suyu yüzeye çıkması.
"""
},

}


def get_cografya10_reference(topic: str) -> list:
    """Verilen konuya en uygun cografya 10 referans kayitlarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in COGRAFYA_10_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_cografya10_keys() -> list:
    """Tum cografya 10 referans anahtarlarini dondurur."""
    return list(COGRAFYA_10_REFERANS.keys())
