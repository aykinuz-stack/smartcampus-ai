# -*- coding: utf-8 -*-
"""
2. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Bu dosya, AI ders anlatiminda dogru bilgi kullanilmasini saglamak icin
ogrenme alanlarina gore organize edilmis referans icerik barindirir.

Ogrenme Alanlari:
1. Sayilar ve Islemler
2. Geometri
3. Olcme
4. Veri Isleme
"""

MATEMATIK_2_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: SAYILAR VE ISLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.2.1.DOGAL_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Dogal Sayilar 0-1000 ve Basamak Degeri",
    "icerik": """
DOGAL SAYILAR 0-1000:
- 2. sinifta dogal sayilar 0'dan 1000'e kadar ogrenilir
- Sayilari okuma, yazma ve siralama
- Sayi dogrusu uzerinde gosterme

BASAMAK DEGERI:
1. Birler basamagi: 0-9 arasi degerler
   - Ornek: 7 sayisinda 7 birler basamagindadir → degeri 7
2. Onlar basamagi: 10, 20, 30, ..., 90
   - Ornek: 45 sayisinda 4, onlar basamagindadir → degeri 40
3. Yuzler basamagi: 100, 200, 300, ..., 900
   - Ornek: 368 sayisinda 3, yuzler basamagindadir → degeri 300

BASAMAK DEGERI ORNEKLERI:
- 524: 5 yuzluk + 2 onluk + 4 birlik = 500 + 20 + 4
- 703: 7 yuzluk + 0 onluk + 3 birlik = 700 + 0 + 3
- 999: 9 yuzluk + 9 onluk + 9 birlik = 900 + 90 + 9

SAYILARI KARSILASTIRMA:
- Buyuktur (>): 45 > 32
- Kucuktur (<): 18 < 25
- Esittir (=): 50 = 50
- Once basamak sayisina bak: 3 basamakli sayi > 2 basamakli sayi
- Ayni basamak sayisinda: Soldaki buyuk basamaktan basla
  Ornek: 456 ile 439 → yuzler ayni (4=4), onlar: 5 > 3 → 456 > 439

SAYILARI SIRALAMA:
- Kucukten buyuge: 12, 35, 67, 89, 124
- Buyukten kucuge: 999, 750, 500, 250, 100
- Ikiser ikiser sayma: 2, 4, 6, 8, 10, ...
- Beser beser sayma: 5, 10, 15, 20, 25, ...
- Onar onar sayma: 10, 20, 30, 40, 50, ...
- Yuzer yuzer sayma: 100, 200, 300, 400, 500, ...
"""
},

"MAT.2.1.TOPLAMA_CIKARMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Toplama ve Cikarma Islemleri",
    "icerik": """
TOPLAMA ISLEMI:
- Toplanan + Toplanan = Toplam
- 2. sinifta 3 basamakli sayilarla toplama yapilir

ELDESIZ TOPLAMA:
- Birler, onlar, yuzler basamagi ayri ayri toplanir
- Ornek: 234 + 152 = 386
  Birler: 4 + 2 = 6
  Onlar: 3 + 5 = 8
  Yuzler: 2 + 1 = 3

ELDELI TOPLAMA:
- Bir basamakta toplam 10 veya daha fazla olursa, bir ust basamaga 1 elde tasinir
- Ornek: 167 + 258 = 425
  Birler: 7 + 8 = 15 → 5 yaz, 1 elde
  Onlar: 6 + 5 + 1(elde) = 12 → 2 yaz, 1 elde
  Yuzler: 1 + 2 + 1(elde) = 4

CIKARMA ISLEMI:
- Eksilen - Cikan = Fark
- 2. sinifta 3 basamakli sayilarla cikarma yapilir

ONLUK BOZMALI CIKARMA:
- Alt basamaktaki rakam cikan rakamdan kucukse, ust basamaktan 1 onluk/yuzluk alinir
- Ornek: 423 - 187 = 236
  Birler: 3'ten 7 cikmaz → onlardan 1 al: 13 - 7 = 6
  Onlar: 1(kalan) ten 8 cikmaz → yuzlerden 1 al: 11 - 8 = 3 (aslinda 2-1=1, sonra 11-8=3)
  Yuzler: 3 - 1 = 2 (4'ten 1 almıştik → 3)

TOPLAMA VE CIKARMA ILISKISI:
- Toplama ile cikarma ters islemlerdir
- 25 + 30 = 55 ise 55 - 30 = 25 ve 55 - 25 = 30
- Dogrulama: Cikarma sonucunu toplamayla kontrol et
  345 - 128 = 217 → Kontrol: 217 + 128 = 345 ✓

ZIHINDEN ISLEM STRATEJILERI:
- Yakin sayiya yuvarlama: 48 + 25 → 50 + 25 - 2 = 73
- Kolay parcalara ayirma: 36 + 27 → 36 + 20 + 7 = 63
- Onlukları tamamlama: 38 + 5 → 38 + 2 + 3 = 43
"""
},

"MAT.2.1.CARPMA_GIRISI": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Carpma Islemine Giris",
    "icerik": """
CARPMA KAVRAMI:
- Carpma, tekrarli toplamanin kisa yoludur
- 3 + 3 + 3 + 3 = 4 tane 3 = 4 × 3 = 12
- 5 + 5 + 5 = 3 tane 5 = 3 × 5 = 15
- Carpan × Carpan = Carpim

TEKRARLI TOPLAMA VE CARPMA ILISKISI:
- 2 + 2 + 2 = 3 × 2 = 6
- 4 + 4 + 4 + 4 + 4 = 5 × 4 = 20
- 7 + 7 = 2 × 7 = 14
- Esit gruplara ayirma: 12 tane elmayı 3'erli gruplara ayir → 4 grup → 4 × 3 = 12

CARPIM TABLOSU (1-5):
1'ler: 1×1=1, 1×2=2, 1×3=3, 1×4=4, 1×5=5, 1×6=6, 1×7=7, 1×8=8, 1×9=9, 1×10=10
2'ler: 2×1=2, 2×2=4, 2×3=6, 2×4=8, 2×5=10, 2×6=12, 2×7=14, 2×8=16, 2×9=18, 2×10=20
3'ler: 3×1=3, 3×2=6, 3×3=9, 3×4=12, 3×5=15, 3×6=18, 3×7=21, 3×8=24, 3×9=27, 3×10=30
4'ler: 4×1=4, 4×2=8, 4×3=12, 4×4=16, 4×5=20, 4×6=24, 4×7=28, 4×8=32, 4×9=36, 4×10=40
5'ler: 5×1=5, 5×2=10, 5×3=15, 5×4=20, 5×5=25, 5×6=30, 5×7=35, 5×8=40, 5×9=45, 5×10=50

CARPMANIN OZELLIKLERI (2. SINIF DUZEYI):
- Degisme ozelligi: 3 × 4 = 4 × 3 = 12 (carpanlarin yeri degisir, sonuc degismez)
- 1 ile carpma: Herhangi bir sayi × 1 = kendisi (5 × 1 = 5)
- 0 ile carpma: Herhangi bir sayi × 0 = 0 (5 × 0 = 0)

CARPMA STRATEJILERI:
- Parmakla sayma (kucuk sayilarda)
- Ikiser ikiser atlayarak sayma (2'nin katlari)
- Beser beser atlayarak sayma (5'in katlari)
- Resimle gosterme (gruplar halinde nesneler cizme)
"""
},

"MAT.2.1.BOLME_GIRISI": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Bolme Islemine Giris",
    "icerik": """
BOLME KAVRAMI:
- Bolme, esit paylastirma veya esit gruplara ayirma islemidir
- Bolunen ÷ Bolen = Bolum
- Carpmanin tersi islemidir

ESIT PAYLASTIRMA:
- 12 elmayi 3 cocuga esit paylastir → Her birine 4 elma → 12 ÷ 3 = 4
- 15 kalemi 5 masaya esit dagit → Her masaya 3 kalem → 15 ÷ 5 = 3
- 20 seker 4 kisiye → Her kisiye 5 seker → 20 ÷ 4 = 5
- Somut nesnelerle uygulama yapilir

GRUPLAMA:
- 12 elmayi 4'erli gruplara ayir → 3 grup olur → 12 ÷ 4 = 3
- 18 top 6'sarli gruplara ayir → 3 grup olur → 18 ÷ 6 = 3
- 10 bisiklet 2'serli gruplara ayir → 5 grup olur → 10 ÷ 2 = 5
- Gruplama ile esit paylastirma ayni sonucu verir

CARPMA VE BOLME ILISKISI:
- 3 × 4 = 12 ise → 12 ÷ 3 = 4 ve 12 ÷ 4 = 3
- 5 × 2 = 10 ise → 10 ÷ 5 = 2 ve 10 ÷ 2 = 5
- Dogrulama: Bolum × Bolen = Bolunen
  12 ÷ 3 = 4 → Kontrol: 4 × 3 = 12 ✓

BASIT BOLME ORNEKLERI:
- 6 ÷ 2 = 3
- 8 ÷ 4 = 2
- 10 ÷ 5 = 2
- 15 ÷ 3 = 5
- 20 ÷ 4 = 5
- 16 ÷ 2 = 8
- 0 ÷ 5 = 0 (Sifir herhangi bir sayiya bolunur, sonuc sifirdir)
- ONEMLI: Bir sayi sifira bolunemez! (tanimsiz)
"""
},

"MAT.2.1.KESIR_GIRISI": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Kesir Kavramina Giris",
    "icerik": """
KESIR NEDIR?
- Bir butunun esit parcalara bolunmesinde her bir parcayi ifade eder
- 2. sinifta yarim ve ceyrek kavramlari ogretilir
- Somut nesnelerle (kek, pizza, elma, kagit) gosterilir

YARIM (1/2):
- Bir butunun 2 esit parcaya bolunmesinde her bir parca
- 1/2 seklinde yazilir (pay: 1, payda: 2)
- Ornekler:
  * Bir elmayi ortadan ikiye bol → her parca yarim elma
  * Bir kagidi ikiye katla → her parca yarım kagit
  * Bir pizzanin yarisi = 1/2 pizza
  * 10'un yarisi = 5
  * 8'in yarisi = 4
  * 1 saat = 60 dakika → yarim saat = 30 dakika

CEYREK (1/4):
- Bir butunun 4 esit parcaya bolunmesinde her bir parca
- 1/4 seklinde yazilir (pay: 1, payda: 4)
- Ornekler:
  * Bir pizzayi 4 esit dilime bol → her dilim ceyrek pizza
  * Bir portakali 4 esit parcaya bol → her parca ceyrek portakal
  * 1 saat = 60 dakika → ceyrek saat = 15 dakika
  * 100'un ceyregi = 25
  * 20'nin ceyregi = 5

YARIM VE CEYREK ILISKISI:
- 1 butun = 2 yarim = 4 ceyrek
- 1 yarim = 2 ceyrek
- 2 yarim = 1 butun
- 4 ceyrek = 1 butun
- 2 ceyrek = 1 yarim

GORSEL MODELLER:
- Daire modeli: Daireyi esit parcalara bol, boyayla goster
- Dikdortgen modeli: Dikdortgeni esit parcalara bol
- Sayi dogrusu: 0 ile 1 arasi yarim ve ceyrekleri goster
  0 --- 1/4 --- 1/2 --- 3/4 --- 1
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: GEOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.2.2.GEOMETRI": {
    "unite": "Geometri",
    "baslik": "Geometrik Cisimler ve Kavramlar",
    "icerik": """
TEMEL GEOMETRIK KAVRAMLAR:

1. KOSE:
   - Tanim: Iki kenar veya yuzun birlestigi nokta
   - Ornek: Bir kutunun 8 kosesi vardir
   - Ucgenin 3 kosesi, karenin 4 kosesi, besgenin 5 kosesi vardir
   - Koseler noktalarla gosterilir

2. KENAR:
   - Tanim: Iki koseyi birlestiren dogru parcasi
   - Ornek: Bir karenin 4 kenari vardir ve hepsi esittir
   - Ucgenin 3 kenari, dikdortgenin 4 kenari, besgenin 5 kenari vardir
   - Kenarlar cizgilerle gosterilir

3. YUZ:
   - Tanim: Geometrik cisimlerin duz yuzey alanlari
   - Ornek: Bir kupun 6 yuzu vardir (hepsi kare)
   - Dikdortgenler prizmasinin 6 yuzu vardir
   - Silindirin 2 duz yuzu (daire), 1 egri yuzu vardir
   - Kurenin yuzu tamamen egridir

GEOMETRIK SEKILLER (2 BOYUTLU):
- Ucgen: 3 kose, 3 kenar
- Kare: 4 kose, 4 esit kenar, 4 dik aci
- Dikdortgen: 4 kose, 4 kenar (karsi kenarlar esit), 4 dik aci
- Daire: Kose ve kenar yoktur, yuvarlak

GEOMETRIK CISIMLER (3 BOYUTLU):
- Kup: 8 kose, 12 kenar, 6 yuz (tum yuzler kare)
- Dikdortgenler prizmasi (kutu): 8 kose, 12 kenar, 6 yuz (dikdortgen yuzler)
- Silindir: Yuvarlak cisim, 2 daire yuz + 1 egri yuz
- Kure: Tamamen yuvarlak, top seklinde
- Koni: Sivri tepeli, 1 daire yuz + 1 egri yuz
- Piramit: Sivri tepeli, taban + ucgen yuzler

ORUNTU (SEKIL ORUNTULERI):
- Tekrar eden sekil oruntuleri: daire, kare, ucgen, daire, kare, ucgen, ...
- Buyuyen sekil oruntuleri: Her adimda bir kare ekleniyor
- Renk oruntuleri: kirmizi, mavi, kirmizi, mavi, ...
- Oruntunun kuralini bulma ve devamini tahmin etme

SAYI ORUNTULERI:
- Ikiser artma: 2, 4, 6, 8, 10, ...
- Beser artma: 5, 10, 15, 20, 25, ...
- Onar artma: 10, 20, 30, 40, 50, ...
- Tekrar eden sayi oruntusu: 1, 3, 5, 1, 3, 5, 1, 3, 5, ...
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: OLCME
# ═══════════════════════════════════════════════════════════════

"MAT.2.3.OLCME": {
    "unite": "Olcme",
    "baslik": "Uzunluk, Tartma, Sivi ve Zaman Olcme",
    "icerik": """
UZUNLUK OLCME:

Birimler:
- Santimetre (cm): Kucuk uzunluklari olcmek icin (kalem, silgi, parmak)
- Metre (m): Buyuk uzunluklari olcmek icin (sinif, koridor, bahce)
- 1 metre = 100 santimetre (1 m = 100 cm)

Araclar:
- Cetvel: cm olcmek icin (genellikle 30 cm)
- Metre: m olcmek icin (serit metre, marangoz metresi)

Tahmin ve Olcme:
- Once tahmin et, sonra olc, tahmininle karsilastir
- "Bu kalem yaklasik kac cm?" → Tahmin: 15 cm → Olc: 17 cm

TARTMA (KUTLE):

Birimler:
- Kilogram (kg): Agir seyleri tartmak icin (insanlar, meyve kasalari)
- Gram (g): Hafif seyleri tartmak icin (mektup, kursun kalem)
- 1 kilogram = 1000 gram (1 kg = 1000 g)

Araclar:
- Terazi: Kutle olcmek icin
- Kantar/baskul: Agir seyleri tartmak icin

Ornekler:
- Bir elma ≈ 150 g
- Bir ekmek ≈ 400 g
- Bir sise su (1,5 L) ≈ 1,5 kg
- Bir cocuk (2. sinif) ≈ 25-30 kg

SIVI OLCME:

Birimler:
- Litre (L): Sivi miktarini olcmek icin
- 1 litre = 1000 mililitre (ml)

Araclar:
- Olcu kabi, olcu bardagi, olcu silindiri

Ornekler:
- Bir bardak su ≈ 200 mL
- Bir sise su = 500 mL veya 1 L
- Bir kova su ≈ 10 L
- Bir banyo kuveti ≈ 150 L

ZAMAN OLCME:

Saat Okuma (5'er dakika okuma):
- Kucuk akrep: Saati gosterir
- Buyuk akrep: Dakikayi gosterir
- Buyuk akrep 12'de → tam saat (3:00 = saat uc)
- Buyuk akrep 6'da → bucuk (3:30 = uc bucuk)
- Buyuk akrep 3'te → ceyrek gecek (3:15 = ucu ceyrek geciyor)
- Buyuk akrep 9'da → ceyrek kala (3:45 = dorde ceyrek var)
- 5'er dakika okuma: Buyuk akrep her rakamda 5 dakika ilerler
  12 = 0 dk, 1 = 5 dk, 2 = 10 dk, 3 = 15 dk, ..., 11 = 55 dk

Takvim:
- 1 yil = 12 ay = 365 gun (artik yil 366 gun)
- Aylar: Ocak, Subat, Mart, Nisan, Mayis, Haziran,
         Temmuz, Agustos, Eylul, Ekim, Kasim, Aralik
- 1 hafta = 7 gun
- Haftanin gunleri: Pazartesi, Sali, Carsamba, Persembe, Cuma, Cumartesi, Pazar
- Mevsimler: Ilkbahar, Yaz, Sonbahar, Kis
- Dun, bugun, yarin kavramlari
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.2.4.VERI": {
    "unite": "Veri Isleme",
    "baslik": "Cetele ve Sutun Grafik",
    "icerik": """
CETELE (TALLY):
- Tanim: Verileri sayarak kaydetme yontemi
- Her bir veri icin bir cizgi (|) cekilir
- 5. cizgi diger dortunu caprazlar: |||| (4) → ||||| (besten sonra yeni basla)
  Aslinda: |||| = 4 → ||||  ile gosterilir (5 = dort cizgi + 1 capraz)
- Cetele tablosu: Kategoriler ve karsilarinda cetele isaretleri

CETELE ORNEGI:
Siniftaki ogrencilerin en sevdigi meyve:
| Meyve  | Cetele       | Sayi |
|--------|-------------|------|
| Elma   | |||| |      | 5    |
| Portakal| |||| ||    | 7    |
| Muz    | |||         | 3    |
| Cilek  | |||| ||||   | 9    |

SUTUN GRAFIK (BAR CHART):
- Tanim: Verileri dikdortgen sutunlarla gosteren grafik
- Yatay eksen (alt): Kategoriler (meyve isimleri)
- Dikey eksen (sol): Sayi/miktar
- Her sutunun yuksekligi degeri gosterir
- Sutunlar arasinda bosluk bulunur
- Grafik basligi yazilir

SUTUN GRAFIK OKUMA:
- En uzun sutun = en fazla olan kategori
- En kisa sutun = en az olan kategori
- Sutunlarin yuksekligini sayarak degerleri oku
- Iki sutun arasindaki farki bul

VERI TOPLAMA:
- Sinifta anket yapma (en sevilen renk, meyve, spor)
- Sayma ve kaydetme
- Once cetele yap, sonra grafik ciz

GRAFIK OLUSTURMA ADIMLARI:
1. Veri topla (anket, gozlem)
2. Cetele tablosu olustur
3. Sayilari bul
4. Grafik kagidina eksenleri ciz
5. Kategorileri yatay eksene yaz
6. Sayilari dikey eksene yaz
7. Her kategori icin uygun yukseklikte sutun ciz
8. Grafige baslik ver

SORULARI CEVAPLAMA:
- "En cok hangisi seviliyor?" → En yuksek sutuna bak
- "En az hangisi secilmis?" → En alçak sutuna bak
- "Kac kisi elma secmis?" → Elma sutununun yuksekligini oku
- "Elma ile muz arasindaki fark kac?" → Elma sayisi - Muz sayisi
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik2_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_2_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik2_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_2_REFERANS.keys())
