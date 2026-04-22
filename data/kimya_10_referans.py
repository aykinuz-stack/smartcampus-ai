# -*- coding: utf-8 -*-
"""
10. Sinif Kimya dersi
MEB 2025 mufredatina uygun referans verileri.

Uniteler:
1. Kimyanin Temel Kanunlari ve Kimyasal Hesaplamalar
2. Karisimlar
3. Asitler Bazlar Tuzlar
4. Kimya Her Yerde
"""

KIMYA_10_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: KIMYANIN TEMEL KANUNLARI VE KIMYASAL HESAPLAMALAR
# ═══════════════════════════════════════════════════════════════

"KIM.10.1.KUTLE_KORUNUMU": {
    "unite": "Kimyanin Temel Kanunlari ve Kimyasal Hesaplamalar",
    "baslik": "Kutlenin Korunumu Kanunu",
    "icerik": """
KUTLENIN KORUNUMU KANUNU (LAVOISIER):
- Kimyasal tepkimelerde toplam kutle degismez.
- Girenler kutlesi = Urunler kutlesi
- Antoine Lavoisier (1789) tarafindan kanitlanmistir.
- Kapali bir sistemde kimyasal reaksiyon oncesi ve sonrasi kutle aynidir.
- Ornek: 2H₂ + O₂ → 2H₂O
  4 g H₂ + 32 g O₂ = 36 g H₂O

ATOM SAYISININ KORUNUMU:
- Tepkimede atom turleri ve sayilari degismez.
- Yalnizca atomlar arasi baglar degisir; atomlar yok olmaz veya yeniden olusturulamaz.
- Denklestirilmis kimyasal denklemde her elementin atom sayisi iki tarafta esittir.

KIMYASAL DENKLEM DENKLESTIRME:
- Denklestirilmemis denklem: Atom sayilari esit degildir.
- Denklestirme adimlari:
  1. Tepkime yazilir (girenler → urunler).
  2. Her elementin atom sayisi kontrol edilir.
  3. Katsayilar ayarlanarak esitlik saglanir.
  4. En kucuk tam sayi katsayilari kullanilir.
- Ornek: Fe + O₂ → Fe₂O₃ denklestirilmis hali: 4Fe + 3O₂ → 2Fe₂O₃
"""
},

"KIM.10.1.SABIT_ORANLAR": {
    "unite": "Kimyanin Temel Kanunlari ve Kimyasal Hesaplamalar",
    "baslik": "Sabit Oranlar ve Katli Oranlar Kanunu",
    "icerik": """
SABIT ORANLAR KANUNU (PROUST):
- Bir bilesikteki elementlerin kutle oranlari her zaman sabittir.
- Bilesik nereden elde edilirse edilsin, ayni elementleri ayni oranda icerir.
- Joseph Proust (1799) tarafindan ortaya konmustur.
- Ornek: Su (H₂O) her zaman kutle olarak %11,1 hidrojen ve %88,9 oksijen icerir.
  m_H / m_O = 2/16 = 1/8 (her zaman sabit)

KATLI ORANLAR KANUNU (DALTON):
- Iki element birden fazla bilesik olusturuyorsa, sabit kutle olan elemente
  karsilik gelen diger elementin kutleleri arasinda basit tam sayi orani vardir.
- John Dalton (1803) tarafindan ortaya konmustur.
- Ornek: CO ve CO₂
  CO: 12 g C ile 16 g O birlesir
  CO₂: 12 g C ile 32 g O birlesir
  O oranlari: 16/32 = 1/2 (basit tam sayi orani)

HACIM ORANLARI KANUNU (GAY-LUSSAC):
- Gaz halindeki maddeler arasindaki tepkimelerde gazlarin hacimleri
  arasinda basit tam sayi oranlari vardir (ayni sicaklik ve basincta).
- Ornek: 2H₂(g) + O₂(g) → 2H₂O(g) → hacim orani 2:1:2

AVOGADRO HIPOTEZI:
- Ayni sicaklik ve basincta esit hacimdeki gazlar esit sayida molekul icerir.
- Normal kosullarda (0°C, 1 atm) 1 mol gazin hacmi 22,4 L dir.
"""
},

"KIM.10.1.MOL_KAVRAMI": {
    "unite": "Kimyanin Temel Kanunlari ve Kimyasal Hesaplamalar",
    "baslik": "Mol Kavrami ve Kimyasal Hesaplamalar",
    "icerik": """
MOL KAVRAMI:
- Mol, madde miktarinin SI birimidir.
- 1 mol = 6,022 × 10²³ tane parcacik (Avogadro sayisi, Nₐ)
- Parcacik sayisi: N = n × Nₐ (n: mol sayisi)
- Mol, atom, molekul, iyon veya formul birimi icin kullanilir.

MOL KUTLESI:
- 1 mol maddenin gram cinsinden kutlesidir.
- Atom kutle biriminden (akb) gram/mol'e donusum: Sayisal deger aynidir.
- Ornek: C atomunun mol kutlesi = 12 g/mol, H₂O'nun mol kutlesi = 18 g/mol
- n = m / M (n: mol, m: kutle gram, M: mol kutlesi g/mol)

KIMYASAL HESAPLAMALAR:
- Denklestirilmis tepkime denklemi uzerinden hesaplamalar yapilir.
- Katsayilar mol oranlarini verir.
- Ornek: 2H₂ + O₂ → 2H₂O
  2 mol H₂ ile 1 mol O₂ tepkimeye girer, 2 mol H₂O olusur.

SINIRLANDIRICI BILESEN:
- Tepkimede once tukenecek olan madde sinirlandirici bilesendir.
- Urunlerin miktarini sinirlandirici bilesen belirler.
- Diger madde fazla (artik) kalir.

VERIM HESABI:
- Teorik verim: Hesaplamadan bulunan urun miktari.
- Gercek verim: Deneyde elde edilen urun miktari.
- Yuzde verim = (Gercek verim / Teorik verim) × 100
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: KARISIMLAR
# ═══════════════════════════════════════════════════════════════

"KIM.10.2.KARISIM_TURLERI": {
    "unite": "Karisimlar",
    "baslik": "Karisim Turleri ve Ozellikleri",
    "icerik": """
KARISIM KAVRAMI:
- Iki veya daha fazla maddenin kimyasal bag olusturmadan bir arada bulunmasidir.
- Bilesenler kendi ozelliklerini korur.
- Karisim formulu yoktur; belirli erime/kaynama noktasi yoktur.
- Fiziksel yontemlerle bilesenlere ayrilabilir.

HOMOJEN KARISIMLAR (COZELTILER):
- Her yerinde ayni gorunumde ve bileşimde olan karisimlardir.
- Tek fazlidir; gorunurde tekduzedir.
- Ornekler: Tuzlu su, sekerli su, hava (gaz karisimlari), alkol-su, alasimlar.
- Alasimlar: Kati-kati homojen karisim. Ornek: Celik (Fe+C), pirinc (Cu+Zn), bronz (Cu+Sn).

HETEROJEN KARISIMLAR:
- Her yerinde ayni gorunum ve bilesimde olmayan karisimlardir.
- Birden fazla faz icerir.
- Turleri:
  1. Suspansiyon: Kati-sivi heterojen. Buyuk parcaciklar. Bekletince coker.
     Ornekler: Ayran, camurlu su, kan.
  2. Emulsiyon: Sivi-sivi heterojen. Birbiri icinde cozunmeyen sivilar.
     Ornekler: Sut, mayanez, yag-su karisimlari.
  3. Aerosol: Sivi/kati-gaz heterojen.
     Ornekler: Sis (sivi-gaz), duman (kati-gaz), sprey.
  4. Kolloid: Parcacik boyutu suspansiyon ve cozeltinin arasinda (1-1000 nm).
     Ornekler: Jole, tutkal, murekep, kan plazmasi.
     Tyndall etkisi gosterir (isik sacilimi).
"""
},

"KIM.10.2.AYIRMA_YONTEMLERI": {
    "unite": "Karisimlar",
    "baslik": "Karisim Ayirma Yontemleri",
    "icerik": """
FIZIKSEL AYIRMA YONTEMLERI:

1. SUZME (FILTRASYON):
   - Cozunmemis kati parcaciklari sividan ayirir.
   - Filtre kagidi veya suzgec kullanilir.
   - Ornek: Kum-su karisimindan kumu ayirma.

2. BUHARLASTIRMA:
   - Cozeltideki cozucu buharlasilarak cozen elde edilir.
   - Ornek: Tuzlu sudan tuzu elde etme.

3. DAMITMA (DISTILASYON):
   - Kaynama noktasi farki olan sivilari ayirir.
   - Basit damitma: Cozeltiden cozucuyu ayirma (tuzlu su).
   - Ayrimsal damitma: Kaynama noktalari yakin sivilari ayirma (ham petrol).

4. KRISTALLENDIRME:
   - Doymus cozeltiden sicaklik dusurulerek kristaller elde edilir.
   - Ornek: Seker veya tuz kristalleri elde etme.

5. DEKANTASYON:
   - Yogunluk farki ile cokelmeyi bekleyip ust siviyi ayirma.
   - Ornek: Camurlu suyun durultulmasi.

6. SANTRIFUJLEME:
   - Merkezkas kuvvetle yogunluk farki olan bilesenleri ayirir.
   - Ornek: Kanin bilesenlere ayrilmasi.

7. AYIRMA HUNISI:
   - Birbirine karismayan sivilari yogunluk farkiyla ayirir.
   - Ornek: Yag-su karisimi.

8. KROMATOGRAFI:
   - Bilesenlerin hareketli ve durgun faz arasindaki dagilim farkiyla ayrilmasi.
   - Kagit kromatografisi, sutun kromatografisi.
   - Ornek: Murekkepteki renk bilesenlerini ayirma.

9. MIKNATISLA AYIRMA:
   - Manyetik ozellikteki maddeleri diger maddelerden ayirir.
   - Ornek: Demir tozunu kumdan ayirma.
"""
},

"KIM.10.2.COZELTI": {
    "unite": "Karisimlar",
    "baslik": "Cozelti ve Cozunurluk",
    "icerik": """
COZELTI KAVRAMLARI:
- Cozucu: Miktari fazla olan bilesen (genellikle sivi).
- Cozunen: Miktari az olan bilesen (kati, sivi veya gaz olabilir).
- Cozelti = Cozucu + Cozunen

COZUNURLUK:
- Belirli sicaklikta 100 g cozucude cozunebilen maksimum madde miktaridir.
- Birim: g madde / 100 g cozucu
- Sicaklik artinca: Katilarin cogunun cozunurlugu artar, gazlarin cozunurlugu azalir.
- Basinc artinca: Gazlarin cozunurlugu artar (Henry kanunu), katilara etkisi yok.

COZELTI TIPLERI:
- Doymamis cozelti: Cozunurluk sinirina ulasilmamis; daha fazla madde cozunebilir.
- Doymus cozelti: Cozunurluk sinirina ulasilmis; daha fazla madde cozunmez.
- Asiri doymus cozelti: Cozunurluk sinirinin ustunde madde cozunmustur; kararsizdir.

DERISIM (KONSANTRASYON):
- Cozeltinin birim hacmindeki veya kutlesindeki cozunen miktari.

1. Kutle yuzde derisimi: % = (m_cozunen / m_cozelti) × 100
2. Hacim yuzde derisimi: % = (V_cozunen / V_cozelti) × 100
3. ppm (milyonda bir): mg_cozunen / kg_cozelti
4. Molarite (M): M = n / V (mol/L)
   n: cozunenin mol sayisi, V: cozeltinin hacmi (L)

SEYRELTIME:
- M₁ × V₁ = M₂ × V₂ (cozunen mol sayisi degismez)
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: ASITLER BAZLAR TUZLAR
# ═══════════════════════════════════════════════════════════════

"KIM.10.3.ASITLER": {
    "unite": "Asitler Bazlar Tuzlar",
    "baslik": "Asitler ve Ozellikleri",
    "icerik": """
ASIT TANIMI:
- Arrhenius: Suda cozundugunde H⁺ (H₃O⁺) iyonu veren maddeler.
- Bronsted-Lowry: Proton (H⁺) vericisi.
- Asitler sulu cozeltide iyonlasir: HA → H⁺ + A⁻

ASITLERIN GENEL OZELLIKLERI:
- Eksi (tadi) eksir.
- Mavi turnusol kagidini kirmiziya cevirir.
- pH degeri 7'den kucuktur.
- Aktif metallerle (Zn, Fe, Mg) tepkimeye girerek H₂ gazi cikarir.
- Karbonatlarla (CaCO₃) tepkimeye girerek CO₂ gazi olusturur.
- Elektrik akimini iletir (elektrolit).

KUVVETLI VE ZAYIF ASITLER:
- Kuvvetli asitler suda tamamen iyonlasir:
  HCl (hidroklorik asit), H₂SO₄ (sulfurik asit), HNO₃ (nitrik asit)
- Zayif asitler suda kismi iyonlasir:
  CH₃COOH (asetik asit / sirke asidi), H₂CO₃ (karbonik asit), HF (hidroflorik asit)

YAYGIN ASITLER:
- HCl: Mide asidi, sanayi temizligi.
- H₂SO₄: Aku asidi, gubre uretimi. Dikkat: Seyreltime sirasinda asit suya eklenir, su asite EKLENMEZ.
- HNO₃: Gubre, patlayici uretimi.
- CH₃COOH: Sirke, gida sanayisi.
- H₃PO₄ (fosforik asit): Kola iceceklerinde, gubre uretiminde.
- Sitrik asit: Narenciye meyveleri.
"""
},

"KIM.10.3.BAZLAR": {
    "unite": "Asitler Bazlar Tuzlar",
    "baslik": "Bazlar ve Ozellikleri",
    "icerik": """
BAZ TANIMI:
- Arrhenius: Suda cozundugunde OH⁻ iyonu veren maddeler.
- Bronsted-Lowry: Proton (H⁺) alicisi.
- Bazlar sulu cozeltide cozunur: BOH → B⁺ + OH⁻

BAZLARIN GENEL OZELLIKLERI:
- Ele kaygan hissi verir (sabun hissi).
- Kirmizi turnusol kagidini maviye cevirir.
- pH degeri 7'den buyuktur.
- Aci tatlari vardir.
- Elektrik akimini iletir (elektrolit).
- Yag ve proteinleri cozer (yakici ozellik).

KUVVETLI VE ZAYIF BAZLAR:
- Kuvvetli bazlar suda tamamen iyonlasir:
  NaOH (sodyum hidroksit), KOH (potasyum hidroksit), Ca(OH)₂ (kalsiyum hidroksit)
- Zayif bazlar suda kismi iyonlasir:
  NH₃ (amonyak), Mg(OH)₂ (magnezyum hidroksit), Al(OH)₃

YAYGIN BAZLAR:
- NaOH (kostik soda): Sabun yapimi, kagit sanayi.
- KOH: Pil uretimi, sivi sabun.
- Ca(OH)₂ (sonmus kirec): Insaat, su aritma.
- NH₃ (amonyak): Temizlik urunleri, gubre sanayi.
- Mg(OH)₂: Antasit (mide ilaci).
- NaHCO₃ (sodyum bikarbonat): Kabartma tozu, mide yanmasinda kullanilir.

NOTRLESME TEPKIMESI:
- Asit + Baz → Tuz + Su
- HCl + NaOH → NaCl + H₂O
- pH 7 oldiginda tam notrlesme gerceklesir.
"""
},

"KIM.10.3.PH_OLCEGI": {
    "unite": "Asitler Bazlar Tuzlar",
    "baslik": "pH Olcegi ve Indikatorler",
    "icerik": """
pH KAVRAMI:
- Cozeltinin asitlik veya bazlik derecesini gosteren olcektir.
- pH = -log[H⁺] (H⁺ iyon derismine baglidir)
- pH olcegi 0-14 arasindadir:
  pH < 7: Asidik cozelti
  pH = 7: Notr cozelti (saf su)
  pH > 7: Bazik cozelti
- pH duserse asitlik artar, pH yukselirse bazlik artar.
- Her 1 birim pH degisimi, H⁺ derisiminde 10 kat degisim demektir.

INDIKATORLER:
- Asit-baz ortaminda renk degistiren maddelerdir.
- Turnusol kagidi: Asitte kirmizi, bazda mavi.
- Fenolftalein: Asitte renksiz, bazda pembe-mor.
- Metil oranj: Asitte kirmizi, bazda sari.
- Evrensel indikator: Tum pH araliginda farkli renk gosterir.
- pH metresi: Elektronik olarak pH olcer (en hassas yontem).

GUNLUK HAYATTA pH:
- Mide asidi: pH = 1-2 (kuvvetli asit)
- Limon suyu: pH = 2-3
- Sirke: pH = 3
- Yagmur suyu: pH = 5,6 (CO₂ cozunmesi nedeniyle hafif asidik)
- Saf su: pH = 7
- Kan: pH = 7,4 (hafif bazik, tampon cozelti ile sabit tutulur)
- Sabun: pH = 9-10
- Camasir suyu: pH = 12-13

ASIT YAGMURLARI:
- Normal yagmurun pH'i 5,6'dir (atmosferdeki CO₂ nedeniyle).
- pH < 5,6 ise asit yagmuru sayilir.
- SO₂ ve NOₓ gazlari (fosil yakit yanmasi) atmosferde H₂SO₄ ve HNO₃ olusturur.
- Zararlari: Orman tahribi, gol/akarsu asitlenmesi, bina/heykel asinmasi.
"""
},

"KIM.10.3.TUZLAR": {
    "unite": "Asitler Bazlar Tuzlar",
    "baslik": "Tuzlar ve Tepkimeleri",
    "icerik": """
TUZ KAVRAMI:
- Asit-baz notrlesme tepkimesinin urunudur.
- Asit + Baz → Tuz + Su
- Tuzlar iyon bilesikleridir; katyon (metalden) ve anyon (asit kalintisindan) icerir.

TUZ TURLERI:
1. Normal tuz: Asit veya baz fazlasi yok. Ornek: NaCl, KNO₃
2. Asidik tuz: Yapisinda H⁺ icerir. Ornek: NaHSO₄, NaHCO₃
3. Bazik tuz: Yapisinda OH⁻ icerir. Ornek: Mg(OH)Cl, Fe(OH)₂Cl

TUZLARIN OZELLIKLERI:
- Oda sicakliginda kati haldedir.
- Genellikle yuksek erime ve kaynama noktasina sahiptir.
- Suda cozundugunde iyon olusturur; elektrik akimi iletir.
- Kati halde elektrik iletmez (iyonlar hareketsiz).
- Erimis halde elektrik iletir.

YAYGIN TUZLAR VE KULLANIM ALANLARI:
- NaCl (sofra tuzu): Gida, kimya sanayi, yol buzlanmasi.
- CaCO₃ (kalsiyum karbonat): Mermer, tebesir, antasit.
- NaHCO₃ (sodyum bikarbonat): Kabartma tozu.
- CaSO₄ · 2H₂O (alci tasi): Insaat, tip (alci).
- KNO₃ (guhercile): Barut yapimi, gubre.
- Na₂CO₃ (soda): Cam sanayi, temizlik.

COKTURME TEPKIMESI:
- Iki cozelti karistirildiginda cozunmeyen tuz olusursa cokme meydana gelir.
- AgNO₃ + NaCl → AgCl (cokelti) + NaNO₃ (AgCl beyaz cokelti olusturur)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: KIMYA HER YERDE
# ═══════════════════════════════════════════════════════════════

"KIM.10.4.TEMIZ_SU": {
    "unite": "Kimya Her Yerde",
    "baslik": "Su Aritma ve Temiz Su",
    "icerik": """
SUYUN ONEMI:
- Yasam icin vazgecilmez bir maddedir.
- Dunya yuzeyinin %71'i sularla kaplidir ancak tatli su orani sadece %2,5 civarindadir.
- Icme suyu kaynaklari: Yeralti sulari, goller, akarsular, barajlar.

SU ARITMA ADIMLARI:
1. Izgaradan gecirme: Buyuk katilarin (dal, yaprak) tutulmasi.
2. On coktürme: Kum ve agir parcaciklarin cokelmeye birakilmasi.
3. Pihtilastirma (koagulasyon): Al₂(SO₄)₃ veya FeCl₃ gibi maddeler eklenerek
   asili parcaciklarin toplandirilmasi.
4. Yumaklastirma (flokülasyon): Pihtilasan parcaciklarin buyuk yumaklara donusmesi.
5. Durultma (cokturme): Yumaklarin dibe cokmesi.
6. Suzme: Kum ve catir filtrelerinden gecirilmesi.
7. Dezenfeksiyon: Klor, ozon veya UV ile mikrop giderme.
   En yaygin: Klorlama (Cl₂ veya NaClO kullanilir).

SUYUN SERTLIGI:
- Ca²⁺ ve Mg²⁺ iyonlarindan kaynaklanir.
- Sert su: Sabun kopur tutmaz, borularda kirec birikimi yapar.
- Gecici sertlik: Ca(HCO₃)₂ ve Mg(HCO₃)₂ → Kaynatmayla giderilebilir.
  Ca(HCO₃)₂ → CaCO₃ + H₂O + CO₂
- Kalici sertlik: CaSO₄, MgSO₄ → Kaynatmayla giderilemez, iyon degistirici gerekir.
"""
},

"KIM.10.4.KIMYA_YASAM": {
    "unite": "Kimya Her Yerde",
    "baslik": "Kimya ve Yasam",
    "icerik": """
SABUN VE DETERJAN:
- Sabun: Yag + NaOH → Sabun + Gliserol (sabunlasma tepkimesi).
  Sabun molekulunun bir ucu suyu sever (hidrofilik), diger ucu yagi sever (hidrofobik).
  Sert suda iyi kopur tutmaz (Ca/Mg ile coktu olusturur).
- Deterjan: Petrol turevlerinden sentezlenir.
  Sert suda da etkilidir.
  Biyolojik olarak parcalanmasi sabuna gore daha zordur.

POLIMER VE PLASTIK:
- Polimer: Kucuk monomer birimlerinin tekrarli baglanmasiyla olusan buyuk molekuller.
- Dogal polimerler: Nisasta, seluloz, protein, DNA, kaucuk.
- Sentetik polimerler: Polietilen (PE), polipropilen (PP), PVC, polistiren (PS), teflon, naylon.
- Plastik geri donusum kodlari: 1-PET, 2-HDPE, 3-PVC, 4-LDPE, 5-PP, 6-PS, 7-Diger.
- Plastik kirliligi: Dogada yuzlerce yil parcalanmaz; deniz ve toprak kirliligi yaratir.

GUBRE VE TARIM KIMYASI:
- Bitkilerin temel besin elementleri: N, P, K (azot, fosfor, potasyum).
- Azotlu gubreler: NH₄NO₃, ure [CO(NH₂)₂]
- Fosforlu gubreler: Superfosfat, triple superfosfat.
- Potasyumlu gubreler: KCl, K₂SO₄
- Asiri gubre kullanimi: Toprak kirliligi, su kaynaklarinin otrofikasyonu.

ILAC VE SAGLIK:
- Aspirin (asetilsalisilik asit): Agri kesici, ates dusurucu.
- Antibiyotik: Bakterilere karsi (penisilin, amoksisilin).
- Antasit: Mide asidini notralize eden bazik ilaclar (Mg(OH)₂, Al(OH)₃).
"""
},

}


def get_kimya10_reference(topic: str) -> list:
    """Verilen konuya en uygun kimya 10 referans kayitlarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in KIMYA_10_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_kimya10_keys() -> list:
    """Tum kimya 10 referans anahtarlarini dondurur."""
    return list(KIMYA_10_REFERANS.keys())
