# -*- coding: utf-8 -*-
"""
9. Sınıf Coğrafya dersi
MEB 2025 müfredatına uygun referans verileri.

Bu dosya, AI ders anlatımında doğru bilgi kullanılmasını sağlamak için
kazanım kodlarına göre organize edilmiş referans içerik barındırır.

Üniteler:
1. Doğa ve İnsan (C.9.1.1 - C.9.1.2)
2. Dünya'nın Şekli ve Hareketleri (C.9.2.1 - C.9.2.2)
3. Koordinat Sistemi (C.9.3.1 - C.9.3.2)
4. Harita Bilgisi (C.9.4.1 - C.9.4.2)
5. Atmosfer ve Sıcaklık (C.9.5.1 - C.9.5.2)
6. Basınç ve Rüzgârlar (C.9.6.1 - C.9.6.2)
7. Nem ve Yağış (C.9.7.1 - C.9.7.2)
8. İklim Tipleri (C.9.8.1)
9. Yer Şekilleri (C.9.9.1 - C.9.9.2)
"""

COGRAFYA_9_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 1: DOĞA VE İNSAN
# ═══════════════════════════════════════════════════════════════

"C.9.1.1": {
    "unite": "1. Doğa ve İnsan",
    "baslik": "Coğrafyanın Konusu ve Bölümleri",
    "icerik": """
COĞRAFYANIN TANIMI:
- Coğrafya, yeryüzünü doğal ve beşerî yönleriyle inceleyen bilim dalıdır.
- Kelime anlamı: Yunanca "geo" (yer) + "graphein" (yazmak/çizmek) = yer yazımı.
- Coğrafyanın temel amacı: İnsan ile doğal çevre arasındaki karşılıklı etkileşimi ortaya koymaktır.

COĞRAFYANIN KONU ALANI:
- Doğal unsurlar: İklim, yer şekilleri, su kaynakları, toprak, bitki örtüsü.
- Beşerî unsurlar: Nüfus, yerleşme, ekonomik faaliyetler, ulaşım, kültür.
- Coğrafya, "nerede?", "niçin orada?", "nasıl bir dağılış gösterir?" sorularına yanıt arar.

COĞRAFYANIN BÖLÜMLERİ:
a) Fiziki Coğrafya:
   - Jeomorfoloji (yer şekilleri bilimi)
   - Klimatoloji (iklim bilimi)
   - Hidrografya (su bilimi)
   - Biyocoğrafya (canlıların dağılışı)
   - Toprak coğrafyası
b) Beşerî ve Ekonomik Coğrafya:
   - Nüfus coğrafyası
   - Yerleşme coğrafyası
   - Ekonomik coğrafya (tarım, sanayi, turizm, ulaşım)
   - Siyasi coğrafya
c) Bölgesel Coğrafya:
   - Kıtalar, ülkeler veya bölgelerin coğrafi özelliklerini inceler.

COĞRAFYANIN DİĞER BİLİMLERLE İLİŞKİSİ:
- Jeoloji (yer bilimi), Meteoroloji (hava olayları), Astronomi (gök bilimleri),
  Kartografya (harita bilimi), Tarih, Sosyoloji, Ekonomi ile yakın ilişki içindedir.
"""
},

"C.9.1.2": {
    "unite": "1. Doğa ve İnsan",
    "baslik": "Coğrafi Araştırma Yöntemleri",
    "icerik": """
COĞRAFİ ARAŞTIRMA AŞAMALARI:
1. Problemi belirleme (araştırma sorusu oluşturma)
2. Veri toplama (gözlem, anket, ölçme, kaynak tarama)
3. Verileri sınıflandırma ve analiz etme
4. Hipotez oluşturma ve test etme
5. Sonuca ulaşma ve rapor yazma

VERİ TOPLAMA YÖNTEMLERİ:
a) Gözlem: Doğrudan arazi gözlemi (saha çalışması). Birincil veri kaynağıdır.
b) Anket ve Mülakat: Beşerî coğrafya araştırmalarında kullanılır.
c) Ölçme ve Sayım: Sıcaklık, yağış, nüfus gibi verilerin nicel olarak elde edilmesi.
d) Kaynak Tarama: Kitap, makale, istatistik verileri (ikincil kaynaklar).
e) Uzaktan Algılama: Uydu görüntüleri, hava fotoğrafları ile veri toplama.

COĞRAFİ BİLGİ SİSTEMLERİ (CBS / GIS):
- Coğrafi verilerin bilgisayar ortamında toplanması, depolanması, analiz edilmesi ve haritalanmasıdır.
- GPS (Küresel Konumlama Sistemi) ile konum belirleme yapılır.
- CBS kullanım alanları: Şehir planlaması, afet yönetimi, tarım, çevre koruma, ulaşım planlaması.

SAHA ÇALIŞMASI (ARAZİ ÇALIŞMASI):
- Coğrafyanın temel veri toplama yöntemidir.
- Arazi gözlemi, ölçüm, fotoğraflama, örnekleme gibi işlemleri kapsar.
- Toplanan veriler harita, grafik, tablo ve diyagramlarla sunulur.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 2: DÜNYA'NIN ŞEKLİ VE HAREKETLERİ
# ═══════════════════════════════════════════════════════════════

"C.9.2.1": {
    "unite": "2. Dünya'nın Şekli ve Hareketleri",
    "baslik": "Günlük Hareket (Dönme Hareketi)",
    "icerik": """
DÜNYA'NIN ŞEKLİ:
- Dünya tam küre değildir; kutuplardan basık, Ekvator'dan şişkin bir şekle sahiptir (geoid).
- Ekvator çevresi: ~40.076 km, Kutuplar arası çevre: ~40.009 km.
- Ekvator yarıçapı: ~6.378 km, Kutup yarıçapı: ~6.357 km (fark ~21 km).

GÜNLÜK HAREKET (DÖNME / ROTASYON):
- Dünya kendi ekseni etrafında batıdan doğuya doğru döner.
- Bir tam dönüş süresi: 23 saat 56 dakika 4 saniye (yaklaşık 24 saat).
- Dönme hızı Ekvator'da en fazla (~1.670 km/saat), kutuplara doğru azalır, kutuplarda sıfırdır.

GÜNLÜK HAREKETİN SONUÇLARI:
1. Gece-gündüz oluşması (aydınlanma çemberi).
2. Güneş'in doğudan doğup batıdan batması (görünür hareket).
3. Yerel saat farkları (her 15° boylamda 1 saat fark).
4. Coriolis kuvveti (sapma kuvveti): Kuzey Yarımküre'de sağa, Güney Yarımküre'de sola sapma.
   - Rüzgârlar, okyanus akıntıları ve akarsuların yataklarını etkiler.
5. Günlük sıcaklık farkları (gündüz ısınma, gece soğuma).
6. Canlıların biyolojik ritimlerinin oluşması.

AYDINLANMA ÇEMBERİ:
- Dünya'nın yarısı her an Güneş'ten aydınlık, diğer yarısı karanlıktır.
- Aydınlık-karanlık sınırı "aydınlanma çemberi" olarak adlandırılır.
"""
},

"C.9.2.2": {
    "unite": "2. Dünya'nın Şekli ve Hareketleri",
    "baslik": "Yıllık Hareket (Dolanma Hareketi)",
    "icerik": """
YILLIK HAREKET (DOLANMA / REVOLÜSYON):
- Dünya, Güneş etrafında elips (oval) bir yörüngede dolanır.
- Bir tam dolanma süresi: 365 gün 6 saat (yaklaşık 1 yıl).
- Fazladan 6 saat, her 4 yılda bir artık yıl (şubat 29 gün) oluşturur.
- Dünya'nın eksen eğikliği: 23° 27' (yörünge düzlemine dik çizgiye göre).

YILLIK HAREKETİN SONUÇLARI:
1. Mevsimlerin oluşması (eksen eğikliği + dolanma hareketi birlikte).
2. Gece-gündüz sürelerinin değişmesi.
3. Güneş ışınlarının geliş açısının değişmesi.
4. Sıcaklık kuşaklarının oluşması (sıcak, ılıman, soğuk kuşak).
5. İklim çeşitliliğinin ortaya çıkması.

ÖNEMLİ TARİHLER VE ÖZEL GÜNLER:
- 21 Mart (İlkbahar ekinoksu): Güneş ışınları Ekvator'a dik. Gece = gündüz (her yerde 12 saat).
- 21 Haziran (Yaz gündönümü): Güneş ışınları Yengeç Dönencesi'ne (23°27'K) dik.
  Kuzey Yarımküre'de en uzun gündüz, Güney Yarımküre'de en kısa gündüz.
- 23 Eylül (Sonbahar ekinoksu): Güneş ışınları tekrar Ekvator'a dik. Gece = gündüz.
- 21 Aralık (Kış gündönümü): Güneş ışınları Oğlak Dönencesi'ne (23°27'G) dik.
  Kuzey Yarımküre'de en kısa gündüz, Güney Yarımküre'de en uzun gündüz.

KUTUP DAİRESİ VE GECE-GÜNDÜZ:
- 66°33' enlemlerinden sonra (kutup daireleri) bazı günlerde Güneş hiç batmaz veya hiç doğmaz.
- Kutuplarda 6 ay gece, 6 ay gündüz yaşanır.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 3: KOORDİNAT SİSTEMİ
# ═══════════════════════════════════════════════════════════════

"C.9.3.1": {
    "unite": "3. Koordinat Sistemi",
    "baslik": "Paraleller ve Meridyenler",
    "icerik": """
KOORDİNAT SİSTEMİ:
- Yeryüzündeki herhangi bir noktanın konumunu belirlemek için kullanılan enlem-boylam sistemidir.
- İlk sistemli kullanım: Eski Yunan - Hipparkhos (MÖ 2. yüzyıl).

PARALELLER (ENLEM DAİRELERİ):
- Ekvator'a paralel olarak çizilen hayalî çemberlerdir.
- Ekvator: 0° paraleli (en büyük daire, ~40.076 km).
- Kuzey Yarımküre: 0°-90°K (Kuzey Kutbu 90°K).
- Güney Yarımküre: 0°-90°G (Güney Kutbu 90°G).
- Toplam 180 paralel (90 kuzey + 90 güney), Ekvator dahil 181 paralel.
- İki paralel arası mesafe her yerde ~111 km'dir (sabit).

ÖZEL PARALELLER:
- 0° Ekvator
- 23°27'K Yengeç Dönencesi
- 23°27'G Oğlak Dönencesi
- 66°33'K Kuzey Kutup Dairesi
- 66°33'G Güney Kutup Dairesi

MERİDYENLER (BOYLAM DAİRELERİ):
- Kuzey Kutbu'ndan Güney Kutbu'na uzanan hayalî yarım çemberlerdir.
- Başlangıç meridyeni: 0° Greenwich (Londra/İngiltere) meridyeni.
- Doğu Yarımküre: 0°-180°D, Batı Yarımküre: 0°-180°B.
- Toplam 360 meridyen.
- İki meridyen arası mesafe Ekvator'da ~111 km, kutuplara doğru daralır, kutuplarda 0 km.

ENLEM VE BOYLAM:
- Enlem: Ekvator'a olan açısal uzaklık (0°-90°).
- Boylam: Greenwich meridyenine olan açısal uzaklık (0°-180°).
- Bir noktanın koordinatı: Örneğin Ankara → 40°K, 33°D.
"""
},

"C.9.3.2": {
    "unite": "3. Koordinat Sistemi",
    "baslik": "Yerel Saat ve Ülke Saati",
    "icerik": """
YEREL SAAT:
- Güneş'in gökyüzündeki konumuna göre belirlenen saattir.
- Aynı meridyen üzerindeki tüm noktaların yerel saati aynıdır.
- Her 15° boylam farkı = 1 saat fark.
- Her 1° boylam farkı = 4 dakika fark.
- Doğuya gidildikçe saat ileri, batıya gidildikçe saat geridir.

YEREL SAAT HESAPLAMA:
- İki yer arasındaki boylam farkı bulunur.
- Boylam farkı × 4 dakika = saat farkı.
- Doğudaki yerin saati daha ileridir.
- Örnek: 30°D meridyeninde saat 12:00 iken, 45°D meridyeninde saat kaçtır?
  Fark: 45° - 30° = 15° → 15 × 4 = 60 dakika = 1 saat → Saat 13:00.

ÜLKE SAATİ (STANDART SAAT):
- Yerel saat farklılıklarının yaşamı zorlaştırması nedeniyle ülkeler standart saat kullanır.
- Dünya 24 saat dilimine ayrılmıştır (her dilim 15° boylamlık).
- Türkiye: UTC+3 (45°D meridyen esas alınır). 2016'dan beri sürekli yaz saati uygulamasındadır.

TARİH DEĞİŞTİRME ÇİZGİSİ:
- 180° meridyeni (Büyük Okyanus üzerinde).
- Batıdan doğuya geçildiğinde tarih 1 gün geri alınır.
- Doğudan batıya geçildiğinde tarih 1 gün ileri alınır.
- Düz bir çizgi değildir; bazı ülkelerin toprak bütünlüğü için kıvrılır.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 4: HARİTA BİLGİSİ
# ═══════════════════════════════════════════════════════════════

"C.9.4.1": {
    "unite": "4. Harita Bilgisi",
    "baslik": "Harita Türleri ve Ölçek",
    "icerik": """
HARİTANIN TANIMI:
- Yeryüzünün tamamının veya bir bölümünün belli bir ölçeğe göre küçültülerek
  düzleme aktarılmış gösterimidir.
- Bir çizimin harita sayılabilmesi için: ölçek, projeksiyon, küçültme ve düzleme aktarma şartları gereklidir.

HARİTA TÜRLERİ:
a) Genel Haritalar:
   - Fiziki haritalar: Yer şekillerini gösterir (renklendirme: yeşil=ova, sarı=yayla, kahverengi=dağ, mavi=su).
   - Siyasi haritalar: Ülke ve il sınırlarını gösterir.
   - Beşerî ve ekonomik haritalar: Nüfus, tarım, sanayi gibi verileri gösterir.
b) Özel (Tematik) Haritalar:
   - İklim, toprak, jeoloji, bitki örtüsü, turizm gibi tek konu haritaları.
c) Topografya Haritaları:
   - Yer şekillerini eş yükselti (izohips) eğrileriyle gösterir. Hem fiziki hem beşerî bilgi içerir.

ÖLÇEK:
- Haritadaki küçültme oranıdır. Gerçek uzunluğun haritadaki uzunluğa oranıdır.
- Kesir (sayısal) ölçek: 1/100.000 (haritada 1 cm = gerçekte 1 km).
- Çizgi (grafik) ölçek: Bir doğru üzerinde gerçek uzaklıkların gösterilmesi.
- Ölçek büyüklüğü: Payda küçüldükçe ölçek büyür (1/25.000 > 1/500.000).

ÖLÇEK VE AYRINTILAR:
- Büyük ölçekli harita: Küçük alanı ayrıntılı gösterir (örn. 1/5.000 - şehir planı).
- Küçük ölçekli harita: Geniş alanı az ayrıntıyla gösterir (örn. 1/10.000.000 - dünya haritası).
- Ölçek büyüdükçe: ayrıntı artar, gösterilen alan küçülür, gerçeğe benzerlik artar.
"""
},

"C.9.4.2": {
    "unite": "4. Harita Bilgisi",
    "baslik": "Profil Çıkarma ve İzohips",
    "icerik": """
İZOHİPS (EŞ YÜKSELTİ EĞRİLERİ):
- Deniz seviyesinden aynı yükseklikteki noktaların birleştirilmesiyle oluşan kapalı eğrilerdir.
- Topografya haritalarında yer şekillerini göstermek için kullanılır.
- Eğri aralıkları (equidistans): Haritanın ölçeğine göre belirlenir (örn. 100 m, 200 m, 500 m).

İZOHİPS ÖZELLİKLERİ:
- İzohipsler birbirini kesmez.
- Kapalı eğrilerdir (haritanın kenarında açık görünebilir).
- En içteki eğri en yüksek veya en alçak noktayı gösterir.
- Eğriler sıklaşıyorsa yamaç dikleşir; seyrekleşiyorsa yamaç düzleşir.
- Akarsu vadilerinde "V" şeklinde, sırtlarda ters "V" şeklinde kıvrılır.
- Daire şeklinde iç içe eğriler: tepe (zirve) veya çukur (krater) gösterir.

PROFİL (KESİT) ÇIKARMA:
- Topografya haritası üzerinde belirlenen iki nokta arasındaki yükseklik değişiminin
  yan görünüşünün (dikey kesit) çizilmesidir.
- Profil çıkarma adımları:
  1. İki nokta arasına bir çizgi çekilir.
  2. Bu çizginin izohipslerle kesiştiği noktalar belirlenir.
  3. Milimetrik kâğıda yatay eksen (mesafe) ve dikey eksen (yükseklik) çizilir.
  4. Kesişim noktalarındaki yükseklik değerleri dikey eksende işaretlenir.
  5. Noktalar birleştirilerek profil elde edilir.

DİĞER İZO ÇİZGİLERİ:
- İzobar: Eşit basınç noktalarını birleştiren çizgi.
- İzoterm: Eşit sıcaklık noktalarını birleştiren çizgi.
- İzohyet: Eşit yağış miktarı alan noktaları birleştiren çizgi.
- İzobat: Eşit derinlik noktalarını birleştiren çizgi.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 5: ATMOSFER VE SICAKLIK
# ═══════════════════════════════════════════════════════════════

"C.9.5.1": {
    "unite": "5. Atmosfer ve Sıcaklık",
    "baslik": "Atmosferin Yapısı ve Isınma",
    "icerik": """
ATMOSFERİN TANIMI:
- Dünya'yı çepeçevre saran gaz karışımından oluşan hava küreye atmosfer denir.
- Yerçekimi sayesinde Dünya'ya bağlıdır.
- Atmosferin kalınlığı yaklaşık 10.000 km olmakla birlikte, yoğunluğun %99'u ilk 30 km'dedir.

ATMOSFERİN BİLEŞİMİ:
- Azot (%78), Oksijen (%21), Argon (%0.93), Karbondioksit (%0.04), diğer gazlar ve su buharı.
- Su buharı miktarı değişkendir; tropik bölgelerde %4'e kadar çıkabilir.

ATMOSFER KATMANLARI:
1. Troposfer (0-12 km): Hava olaylarının yaşandığı katman. Yükseldikçe sıcaklık azalır (her 200 m'de ~1°C).
2. Stratosfer (12-50 km): Ozon tabakası bulunur (UV ışınlarını süzer). Uçaklar burada uçar.
3. Mezosfer (50-80 km): En soğuk katman (-90°C). Göktaşları burada yanar.
4. Termosfer (80-700 km): Sıcaklık çok yükselir (>1000°C). Kutup ışıkları burada oluşur.
5. Ekzosfer (700+ km): Atmosferin uzaya geçiş katmanı. Gaz molekülleri çok seyrektir.

DÜNYA'NIN ISINMASI:
- Güneş enerjisi atmosferden geçerken: %19 atmosfer tarafından emilir, %30 yansır (albedo), %51 yer tarafından emilir.
- Yer, emdiği enerjiyi uzun dalga (kızılötesi) olarak geri yayar → atmosfer bu enerjiyi tutar (sera etkisi).
- Dünya doğrudan Güneş ışınlarıyla değil, dolaylı olarak yer yüzeyinden ısınır.
- Bu nedenle yükseldikçe (troposferde) sıcaklık azalır.
"""
},

"C.9.5.2": {
    "unite": "5. Atmosfer ve Sıcaklık",
    "baslik": "Sıcaklık Dağılışını Etkileyen Faktörler",
    "icerik": """
SICAKLIK DAĞILIŞINI ETKİLEYEN FAKTÖRLER:

1. ENLEM (MATEMATİK KONUM):
- En önemli faktördür. Ekvator'dan kutuplara doğru sıcaklık azalır.
- Güneş ışınlarının geliş açısı enlem arttıkça küçülür, ısı yayılan alan genişler.
- Ekvator bölgesi: yıllık ortalama ~25-28°C, Kutuplar: yıllık ortalama ~-30°C.

2. YÜKSELTİ:
- Troposferde her 200 m yükseklikte sıcaklık yaklaşık 1°C azalır.
- Ekvator'da bile yüksek dağların zirveleri karla kaplı olabilir (örn. Kilimanjaro, 5.895 m).

3. KARA-DENİZ DAĞILIŞI:
- Kara çabuk ısınır, çabuk soğur; deniz geç ısınır, geç soğur (denizin ısı kapasitesi yüksek).
- Kıyı bölgelerde sıcaklık farkı az (ılıman), iç kesimlerde sıcaklık farkı fazla (karasal).
- Denizellik-karasallık kavramı bu farka dayanır.

4. OKYANUS AKINTILARI:
- Sıcak akıntılar: Geçtikleri kıyıları ısıtır (örn. Gulf Stream → Batı Avrupa).
- Soğuk akıntılar: Geçtikleri kıyıları soğutur (örn. Benguela → Güneybatı Afrika).

5. BAKIŞ YÖNÜ (BAKIYÖN):
- Kuzey Yarımküre'de güneye bakan yamaçlar (güney bakı) daha sıcak ve kuraktır.
- Kuzeye bakan yamaçlar daha serin ve nemlidir. Orman sınırı güney yamaçta daha yüksektir.

6. RÜZGÂRLARIN ETKİSİ:
- Sıcak bölgelerden esen rüzgârlar sıcaklığı artırır.
- Soğuk bölgelerden esen rüzgârlar sıcaklığı düşürür.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 6: BASINÇ VE RÜZGÂRLAR
# ═══════════════════════════════════════════════════════════════

"C.9.6.1": {
    "unite": "6. Basınç ve Rüzgârlar",
    "baslik": "Atmosfer Basıncı ve Basınç Merkezleri",
    "icerik": """
ATMOSFER BASINCI:
- Havanın birim alana uyguladığı kuvvettir.
- Deniz seviyesinde ortalama basınç: 1013,25 mb (milibar) = 760 mm Hg.
- İlk ölçüm: Torricelli (1643) - cıvalı barometreyle ölçmüştür.

BASINCI ETKİLEYEN FAKTÖRLER:
1. Yükselti: Yükseldikçe basınç azalır (her 110 m'de ~10 mb azalır).
2. Sıcaklık: Sıcaklık arttıkça hava genişler, yoğunluk azalır → basınç düşer.
   Sıcak yerlerde alçak basınç, soğuk yerlerde yüksek basınç oluşur.
3. Nem: Nemli hava kuru havadan daha hafiftir → nemli havada basınç daha düşüktür.

BASINÇ MERKEZLERİ (SICAKLIK KAYNAKLI):
a) Termik Alçak Basınç: Ekvator (0°) ve 60° enlemleri → sıcaklıktan dolayı yükselen hava.
b) Termik Yüksek Basınç: 30° enlemleri (dinamik etkiyle birlikte) ve kutuplar (90°).

GENEL ATMOSFERİK DOLAŞIM:
- Ekvator'da ısınan hava yükselir (Ekvator alçak basıncı).
- Yükselen hava 30° enlemlere doğru hareket eder, soğuyarak çöker (subtropikal yüksek basınç).
- 60° enlemlerde sıcak ve soğuk hava kütleleri buluşur (ılıman kuşak alçak basıncı).
- Kutuplarda soğuk ve ağır hava çöker (kutup yüksek basıncı).
- Bu sistem Hadley, Ferrel ve Polar hücrelerinden oluşur.
"""
},

"C.9.6.2": {
    "unite": "6. Basınç ve Rüzgârlar",
    "baslik": "Rüzgâr Çeşitleri",
    "icerik": """
RÜZGÂR NEDİR:
- Yüksek basınç alanından alçak basınç alanına doğru yatay hava hareketidir.
- Basınç farkı arttıkça rüzgâr hızı artar.
- Coriolis kuvveti nedeniyle Kuzey Yarımküre'de sağa, Güney Yarımküre'de sola sapar.

A) SÜREKLİ RÜZGÂRLAR (Genel atmosferik dolaşıma bağlı):
1. Alizeler: 30° yüksek basınçtan Ekvator alçak basıncına eser.
   - K.Y.'de kuzeydoğu, G.Y.'de güneydoğu yönünden.
   - Dünya'nın en düzenli rüzgârlarıdır.
2. Batı Rüzgârları: 30° yüksek basınçtan 60° alçak basıncına eser.
   - K.Y.'de güneybatı, G.Y.'de kuzeybatı yönünden.
   - Yağış taşıyan rüzgârlardır (Batı Avrupa'ya bol yağış getirir).
3. Kutup Rüzgârları: 90° kutup yüksek basıncından 60° alçak basıncına eser.
   - Soğuk ve kuru rüzgârlardır.

B) MEVSİMLİK RÜZGÂRLAR:
1. Muson: Kara-deniz arasında mevsimlik basınç farkından doğar.
   - Yazın denizden karaya (nemli, yağışlı) → yaz musonu.
   - Kışın karadan denize (kuru) → kış musonu.
   - En belirgin: Güney ve Güneydoğu Asya (Hindistan, Bangladeş).
2. Meltem: Gece-gündüz arasında kara ve deniz arasındaki sıcaklık farkından doğar.
   - Gündüz: Denizden karaya (deniz meltemi) → serinletir.
   - Gece: Karadan denize (kara meltemi).
   - Dağ-vadi meltemi: Gündüz vadiden dağa, gece dağdan vadiye.

C) YEREL RÜZGÂRLAR:
- Föhn (sıcak-kuru dağ rüzgârı), Hamsin (Kuzey Afrika'dan sıcak), Mistral (Fransa'da soğuk kuzey rüzgârı), Lodos (Marmara'da güneybatı), Poyraz (kuzeydoğu).
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 7: NEM VE YAĞIŞ
# ═══════════════════════════════════════════════════════════════

"C.9.7.1": {
    "unite": "7. Nem ve Yağış",
    "baslik": "Nem Türleri ve Yoğuşma",
    "icerik": """
NEM NEDİR:
- Atmosferdeki su buharı miktarına nem denir.
- Su buharı, su döngüsünün (hidrolojik döngü) temel bileşenidir.
- Buharlaşma → Yoğuşma → Yağış → Akış döngüsü sürekli devam eder.

NEM TÜRLERİ:
a) Mutlak Nem: 1 m³ havadaki su buharı miktarı (g/m³).
   - Sıcaklık arttıkça havanın su buharı taşıma kapasitesi artar.
b) Maksimum Nem: 1 m³ havanın taşıyabileceği en fazla su buharı miktarı.
   - Sıcaklıkla doğru orantılıdır.
c) Bağıl (Oransal/Nispi) Nem: Mutlak nemin maksimum neme oranı (%).
   - Bağıl nem = (Mutlak nem / Maksimum nem) × 100
   - %100 olduğunda hava doygun hâle gelir → yoğuşma başlar.
   - Ekvator'da bağıl nem yüksek (~%80-90), çöllerde düşük (~%10-20).

YOĞUŞMA (KONDENSASİYON):
- Su buharının sıvıya (veya katıya) dönüşmesidir.
- Yoğuşma koşulları: Havanın soğuması + doygun hâle gelmesi + yoğuşma çekirdeği bulunması.
- Yoğuşma çekirdekleri: Toz, duman, polen, tuz kristalleri.

YOĞUŞMA ÇEŞİTLERİ:
- Bulut: Yüksekte oluşan yoğuşma. Farklı türleri: Sirüs (tüy), Kümülüs (pamuk), Stratüs (tabaka), Kümülonimbüs (sağanak).
- Sis: Yer seviyesinde oluşan yoğuşma. Görüş mesafesini 1 km'nin altına düşürür.
- Çiy: Yüzeylerde su damlacıkları şeklinde oluşan yoğuşma (sıcaklık 0°C üstünde).
- Kırağı (Kırç): Yüzeylerde buz kristalleri şeklinde oluşan yoğuşma (sıcaklık 0°C altında).
"""
},

"C.9.7.2": {
    "unite": "7. Nem ve Yağış",
    "baslik": "Yağış Çeşitleri ve Dağılışı",
    "icerik": """
YAĞIŞ NEDİR:
- Atmosferdeki su buharının yoğuşarak yeryüzüne düşmesidir.
- Yağış türleri: Yağmur (sıvı), kar (katı), dolu (katı), sulu kar (karışık).

YAĞIŞ ÇEŞİTLERİ (OLUŞUM MEKANİZMASINA GÖRE):

1. Yamaç (Orografik) Yağışı:
   - Nemli hava kütlesi dağa çarparak yükselir, soğur ve yoğuşarak yağış bırakır.
   - Dağın rüzgâr alan yamacı (nemli yamaç) bol yağışlı, arka yamacı (kuru yamaç) kuraktır.
   - Fön etkisi: Nemsiz hava arka yamaçtan inerken ısınır (her 100 m'de ~1°C) → sıcak ve kuru rüzgâr.

2. Konveksiyonel (Yükselim/Isınma) Yağışı:
   - Yeryüzünün şiddetli ısınmasıyla hava yükselir, soğur ve yoğuşarak yağış oluşur.
   - Ekvator bölgesinde her gün öğleden sonra görülür.
   - Türkiye'de yaz aylarında iç kesimlerde "sağanak yağış" bu türdendir.
   - Genellikle gök gürültüsü ve şimşek eşlik eder (konvektif fırtına).

3. Cephe (Frontal) Yağışı:
   - Farklı sıcaklıktaki (sıcak ve soğuk) hava kütlelerinin karşılaşmasıyla oluşur.
   - Sıcak hava soğuk havanın üstüne yükselir, soğuyarak yoğuşur.
   - Ilıman kuşakta yaygındır (Türkiye'de kış yağışlarının çoğu cephe yağışıdır).
   - Sıcak cephe: Sürekli, uzun süreli yağış. Soğuk cephe: Kısa süreli sağanak.

YAĞIŞ DAĞILIŞI:
- En yağışlı yerler: Ekvator çevresi, muson bölgeleri, dağların rüzgâr alan yamaçları.
- En kurak yerler: 30° enlemleri (çöl kuşağı), kıtaların iç kesimleri, kutuplar.
- Dünya ortalaması: Yılda yaklaşık 1.000 mm. En yağışlı yer: Cherrapunji (Hindistan) ~11.000 mm/yıl.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 8: İKLİM TİPLERİ
# ═══════════════════════════════════════════════════════════════

"C.9.8.1": {
    "unite": "8. İklim Tipleri",
    "baslik": "Dünya İklim Tipleri",
    "icerik": """
İKLİM VE HAVA DURUMU:
- Hava durumu: Kısa süreli atmosfer koşulları (günlük, saatlik).
- İklim: Uzun yıllar (en az 30 yıl) boyunca gözlenen ortalama atmosfer koşulları.

SICAK KUŞAK İKLİMLERİ (0°-30° enlemler):

1. Ekvator İklimi: Yıl boyu sıcak ve yağışlı. Yıllık ortalama ~25-27°C. Yağış: >2000 mm (konveksiyonel).
   Bitki örtüsü: Ekvatoral yağmur ormanları (tropikal orman). Brezilya, Kongo, Endonezya.

2. Tropikal (Savan) İklim: Yazları yağışlı, kışları kurak. Sıcaklık yüksek.
   Bitki örtüsü: Savan (uzun otlar + seyrek ağaçlar). Afrika, Güney Amerika.

3. Muson İklimi: Yazları aşırı yağışlı (yaz musonu), kışları kurak. Güney/Güneydoğu Asya.
   Bitki örtüsü: Muson ormanları (kışın yaprak döken tropik orman).

4. Çöl İklimi: Yıl boyu kurak. Gece-gündüz sıcaklık farkı çok yüksek. Yağış: <250 mm.
   Bitki örtüsü: Çöl bitkileri (kaktüs vb.) veya hiç bitki yok. Sahra, Arabistan, Gobi.

ILIMAN KUŞAK İKLİMLERİ (30°-60° enlemler):

5. Akdeniz İklimi: Yazları sıcak-kurak, kışları ılık-yağışlı.
   Bitki örtüsü: Maki (sert yapraklı, her dem yeşil çalılar). Akdeniz çevresi, Kaliforniya, Şili.

6. Karasal İklim: Yazları sıcak, kışları çok soğuk. Yıllık sıcaklık farkı büyük. Yağış az-orta.
   Bitki örtüsü: Bozkır (step). İç Anadolu, Orta Asya, ABD iç kesimleri.

7. Okyanusal İklim: Yıl boyu ılık, yağışlı. Sıcaklık farkı az. Yağış: >750 mm.
   Bitki örtüsü: Geniş yapraklı ormanlar. Batı Avrupa, İngiltere, Yeni Zelanda.

SOĞUK KUŞAK İKLİMLERİ (60°-90° enlemler):

8. Tundra İklimi: Çok uzun ve çok soğuk kışlar. En sıcak ay ortalaması 0-10°C.
   Bitki örtüsü: Tundra (yosun, liken, cüce çalılar). Kuzey Kanada, Sibirya kıyıları.

9. Kutup İklimi: Yıl boyu dondurucu soğuk. En sıcak ay ortalaması 0°C altında.
   Bitki örtüsü: Yok (sürekli buzullar). Antarktika, Grönland iç kesimleri.
"""
},

# ═══════════════════════════════════════════════════════════════
# ÜNİTE 9: YER ŞEKİLLERİ
# ═══════════════════════════════════════════════════════════════

"C.9.9.1": {
    "unite": "9. Yer Şekilleri",
    "baslik": "İç Kuvvetler",
    "icerik": """
İÇ KUVVETLER:
- Dünya'nın iç enerji kaynaklarından (radyoaktif ışınım, manto konveksiyonu) beslenen,
  yer kabuğunu şekillendiren kuvvetlerdir.
- Genel olarak engebeyi artırırlar (dağ oluşumu, yükselme).

LEVHA TEKTONİĞİ:
- Yer kabuğu büyük levhalardan (plakalardan) oluşur.
- Levhalar manto üzerinde yüzer ve hareket eder.
- Levha sınırları: Yaklaşan (yıkıcı), uzaklaşan (yapıcı), yanal kaydıran (transform).

1. OROJENez (Dağ Oluşumu):
- Levhaların çarpışmasıyla kıvrılma ve kırılma yoluyla dağlar oluşur.
- Kıvrım dağları: Esnek (plastik) tabakaların kıvrılmasıyla → Alpler, Himalayalar, Toroslar.
  - Antiklinal: Yukarı doğru kıvrım (kubbe). Senklinal: Aşağı doğru kıvrım (çukur).
- Kırık (fay) dağları: Sert tabakaların kırılmasıyla → Horst (yükselen blok), Graben (çöken blok/çöküntü ovası).
  - Türkiye'de: Horst → Yunt Dağı, Bozdağ. Graben → Büyük Menderes, Gediz, Bakırçay ovaları.

2. EPİROJENEZ (Kıta Oluşumu):
- Geniş alanların yavaşça yükselmesi veya alçalmasıdır.
- Pozitif epirojenez: Yükselme → deniz geriler (regresyon).
- Negatif epirojenez: Çökme → deniz ilerler (transgresyon).
- Taraçalar ve yükseltilmiş kıyılar epirojeneze kanıttır.

3. VOLKANİZMA:
- Magmanın yer kabuğundaki çatlaklardan yüzeye çıkmasıdır.
- Volkanik dağlar: Ağrı Dağı, Erciyes, Fuji, Vezüv, Kilimanjaro.
- Volkanik oluşumlar: Krater, kaldera, lav platosu, volkanik ada (Hawai).
- Aktif volkan kuşakları: Pasifik Ateş Çemberi, Akdeniz-Himalaya kuşağı.

4. DEPREM (SİSMİK AKTİVİTE):
- Yer kabuğundaki kırılma ve yerdeğiştirme sonucu oluşan titreşimlerdir.
- Odak noktası (hiposantr): Kırılmanın başladığı yer.
- Merkez üssü (episantr): Odak noktasının yeryüzündeki izdüşümü.
- Deprem ölçeği: Richter (büyüklük), Mercalli (şiddet).
- Deprem kuşakları: Türkiye aktif deprem kuşağında yer alır (Kuzey Anadolu Fayı, Doğu Anadolu Fayı).
"""
},

"C.9.9.2": {
    "unite": "9. Yer Şekilleri",
    "baslik": "Dış Kuvvetler",
    "icerik": """
DIŞ KUVVETLER:
- Enerji kaynağı Güneş'tir. Atmosfer, su ve canlılar aracılığıyla etkili olur.
- Genel olarak engebeyi azaltırlar (aşındırma ve biriktirme yoluyla düzleştirme).
- Aşındırma → Taşıma → Biriktirme süreçleri hepsinde ortaktır.

1. AKARSULARIN ETKİSİ:
- En yaygın dış kuvvettir. Akarsular mekanik ve kimyasal aşınım yapar.
- Aşındırma şekilleri: Vadi (V vadi, kanyon, boğaz), dev kazanı, peribacası, kırgıbayır (badlands).
- Biriktirme şekilleri: Ova (alüvyal ova), delta, birikinti konisi (yelpazesi), seki (taraça).
- Türkiye'de: Çukurova (delta), Sakarya vadisi, Tuz Gölü çevresi (alüvyal ova).

2. BUZULLARIN ETKİSİ:
- Buzul aşındırması: Sirk (buzul çanağı), tekne vadi (U vadi), hörgüç kaya, fiyord.
- Buzul biriktirmesi: Moren (buzultaş) setleri (yan moren, taban moren, uç moren).
- Türkiye'de: Kaçkar Dağları, Cilo-Sat Dağları, Ağrı Dağı'nda buzul şekilleri.

3. RÜZGÂRLARIN ETKİSİ:
- Özellikle kurak ve yarı kurak bölgelerde (çöl, bozkır) etkilidir.
- Aşındırma şekilleri: Mantar kaya (şapka kaya), yardang (rüzgâr oluğu), çöl kaldırımı.
- Biriktirme şekilleri: Kum tepeleri (barkan, seif), löss (rüzgârın taşıdığı ince taneli toprak).
- Türkiye'de: İç Anadolu'da rüzgâr aşındırma şekilleri (Kapadokya peribacaları kısmen).

4. DALGA VE AKINTILAR (DENİZ ETKİSİ):
- Kıyı aşındırma şekilleri: Falez (yalıyar/aşınım dibi), kıyı platformu, deniz mağarası, doğal köprü.
- Kıyı biriktirme şekilleri: Kıyı oku (tombolo, lagün, kıyı set gölü).
- Türkiye'de: Antalya falezleri, Dalyan lagünü, Sinop tombolosu.

5. KARSTLAŞMA (KİMYASAL ÇÖZÜNME):
- Kalkerli (kireçtaşı) arazilerde suyun kimyasal çözünme etkisiyle oluşur.
- Yüzey şekilleri: Lapya, dolin, uvala, polye, obruk.
- Yeraltı şekilleri: Mağara, sarkıt (tavandan aşağı), dikit (tabandan yukarı), sütun.
- Türkiye'de: Antalya-Burdur göller bölgesi, Obruk Platosu (Konya), Damlataş mağarası.

6. TOPRAK KAYMALARI (KÜTLE HAREKETLERİ):
- Yamaçlarda toprak ve kaya kütlelerinin yerçekimi etkisiyle hareket etmesidir.
- Heyelan, kaya düşmesi, çığ, toprak akması (soliflüksiyon).
- Eğim, su, bitki örtüsü yokluğu ve deprem tetikleyici faktörlerdir.
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════════

def get_cografya9_reference(kod: str) -> dict | None:
    """
    Verilen kazanım koduna göre referans verisini döndürür.

    Args:
        kod: Kazanım kodu (örn. "C.9.1.1", "C.9.5.2")

    Returns:
        dict: Kazanım referans verisi (unite, baslik, icerik) veya None
    """
    return COGRAFYA_9_REFERANS.get(kod)


def get_all_cografya9_keys() -> list[str]:
    """
    Tüm kazanım kodlarını sıralı olarak döndürür.

    Returns:
        list[str]: Kazanım kodları listesi (örn. ["C.9.1.1", "C.9.1.2", ...])
    """
    return sorted(COGRAFYA_9_REFERANS.keys())
