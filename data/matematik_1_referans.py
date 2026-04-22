# -*- coding: utf-8 -*-
"""
1. Sinif Matematik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Ogrenme alanlari:
1. Sayilar ve Islemler
2. Geometri
3. Olcme
4. Veri Isleme
"""

MATEMATIK_1_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: SAYILAR VE ISLEMLER
# ═══════════════════════════════════════════════════════════════

"MAT.1.1.DOGAL_SAYILAR": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Dogal Sayilar 0-100",
    "icerik": """
DOGAL SAYILAR (0-100):

1. SAYILARIN OKUNMASI VE YAZILMASI:
   - 0 (sifir) ile 100 (yuz) arasindaki sayilar ogretilir.
   - Ilk olarak 1-20 arasi, sonra 20-100 arasi ogretilir.
   - Her sayinin rakamla ve yaziyla gosterimi:
     * 1: bir, 2: iki, 3: uc, 4: dort, 5: bes
     * 6: alti, 7: yedi, 8: sekiz, 9: dokuz, 10: on
     * 11: on bir, 12: on iki, ... 19: on dokuz
     * 20: yirmi, 30: otuz, 40: kirk, 50: elli
     * 60: altmis, 70: yetmis, 80: seksen, 90: doksan, 100: yuz

2. SAYI KAVRAMI:
   - Sifir (0): Hicbir sey olmadigini gosterir.
   - Nesnelerle birebir eslestirme yapilir.
   - Ornek: 5 elma = ||||| (bes tane)

3. BASAMAK DEGERI (onluk-birlik):
   - Birler basamagi: 0-9 arasi
   - Onlar basamagi: 10, 20, 30, ..., 90
   - Ornek: 45 = 4 onluk + 5 birlik = 40 + 5
   - Cubuklarla gosterim: 4 demet (onluk) + 5 tek cubuk (birlik)

4. SAYMA:
   - Birer birer sayma: 1, 2, 3, 4, 5, ...
   - Geriye dogru sayma: 10, 9, 8, 7, 6, ...
   - Belirli bir sayidan baslatma: 5'ten baslayarak: 5, 6, 7, 8, ...

5. SIRALAMA:
   - Kucukten buyuge: 3, 5, 8, 12, 15
   - Buyukten kucuge: 15, 12, 8, 5, 3
"""
},

"MAT.1.1.RITMIK_SAYMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Ritmik Sayma",
    "icerik": """
RITMIK SAYMA:
Belirli bir kurala gore (esit araliklarla) saymaya ritmik sayma denir.

1. BIRER SAYMA (1'er):
   1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...
   - En temel sayma bicimi.

2. IKISER SAYMA (2'ser):
   2, 4, 6, 8, 10, 12, 14, 16, 18, 20, ...
   - Cift sayilari olusturur.
   - Tekler: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, ...

3. BESER SAYMA (5'er):
   5, 10, 15, 20, 25, 30, 35, 40, 45, 50, ...
   - Para saymada kullanisli (5 kurus, 5 TL).
   - Saat ogreniminde yardimci.

4. ONAR SAYMA (10'ar):
   10, 20, 30, 40, 50, 60, 70, 80, 90, 100
   - Onluk kavramini pekistirir.
   - Para sayma (10 TL'lik banknotlar).

GERIYE DOGRU RITMIK SAYMA:
   - 10'ar geri: 100, 90, 80, 70, 60, 50, 40, 30, 20, 10
   - 5'er geri: 50, 45, 40, 35, 30, 25, 20, 15, 10, 5
   - 2'ser geri: 20, 18, 16, 14, 12, 10, 8, 6, 4, 2

ORUNTU TAMAMLAMA:
   - 3, 6, 9, ?, 15 -> cevap: 12 (3'er sayma)
   - 10, 20, ?, 40, 50 -> cevap: 30 (10'ar sayma)

CIFT VE TEK SAYILAR:
   - Cift sayilar: 2'ye tam bolunen: 0, 2, 4, 6, 8, 10, 12, ...
   - Tek sayilar: 2'ye tam bolunmeyen: 1, 3, 5, 7, 9, 11, 13, ...
"""
},

"MAT.1.1.KARSILASTIRMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Sayi Karsilastirma",
    "icerik": """
SAYI KARSILASTIRMA:

SEMBOLLER:
- < (kucuktur): Sol taraftaki sayi daha kucuk.
  Ornek: 3 < 7 (3, 7'den kucuktur)

- > (buyuktur): Sol taraftaki sayi daha buyuk.
  Ornek: 9 > 4 (9, 4'ten buyuktur)

- = (esittir): Iki sayi birbirine esit.
  Ornek: 5 = 5 (5, 5'e esittir)

KARSILASTIRMA YONTEMI:
1. Basamak sayisina bak:
   - 2 basamakli sayi > 1 basamakli sayi (ornek: 12 > 9)
2. Basamak sayisi ayniysa onlar basamagina bak:
   - 45 ve 32: 4 > 3, o halde 45 > 32
3. Onlar basamagi ayniysa birler basamagina bak:
   - 45 ve 48: Onlar esit (4=4), birler: 5 < 8, o halde 45 < 48

AC AGIZ YONTEMI (Timsah kurali):
- Timsah her zaman buyuk sayiya dogru agzini acar.
- 5 < 8: Timsah 8'e dogru agzini acar.
- 12 > 7: Timsah 12'ye dogru agzini acar.

SIRALAMA:
- Kucukten buyuge siralama (artan siralama):
  Ornek: 8, 3, 15, 1, 10 -> 1, 3, 8, 10, 15
- Buyukten kucuge siralama (azalan siralama):
  Ornek: 8, 3, 15, 1, 10 -> 15, 10, 8, 3, 1

EN BUYUK VE EN KUCUK:
- Bir gruptaki en buyuk sayi: 3, 7, 2, 9 -> En buyuk: 9
- Bir gruptaki en kucuk sayi: 3, 7, 2, 9 -> En kucuk: 2
"""
},

"MAT.1.1.TOPLAMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Toplama Islemi (0-100)",
    "icerik": """
TOPLAMA ISLEMI:

TEMEL KAVRAMLAR:
- Toplama isareti: + (arti)
- Esittir isareti: =
- Toplanan + Toplanan = Toplam
- Ornek: 3 + 5 = 8 (3 ile 5'in toplami 8'dir)

TOPLAMA OZELLIKLERI:
1. Degisme ozelligi: 3 + 5 = 5 + 3 = 8
   (Toplananlarin yeri degistirildiginde toplam degismez)
2. Etkisiz eleman (sifir): 7 + 0 = 7, 0 + 4 = 4
   (Bir sayiya 0 eklendiginde sayi degismez)

ELDESIZ TOPLAMA (toplam 9'u gecmez):
- Birler basamagi toplami 10'dan kucuk.
- Ornekler:
  23 + 14 = 37 (3+4=7 birler, 2+1=3 onlar)
  41 + 25 = 66 (1+5=6 birler, 4+2=6 onlar)

ELDELI TOPLAMA (birler toplami 10 veya fazla):
- Birler basamagi toplami 10 veya uzerinde olursa 1 onluk elde edilir.
- Ornekler:
  27 + 15 = 42
  Birler: 7 + 5 = 12 -> 2 yaz, 1 elde
  Onlar: 2 + 1 + 1(elde) = 4
  Sonuc: 42

PARMAKLA TOPLAMA:
- 10'a kadar toplama islemleri icin parmaklar kullanilir.
- 3 + 4: Bir elde 3 parmak, diger elde 4 parmak ac, toplami say.

SAYI DOGRUSU ILE TOPLAMA:
- Sayi dogrusu uzerinde ilk sayidan baslayarak ikinci sayi kadar ileri say.
- 4 + 3: 4'ten baslayip 3 adim ilerle -> 5, 6, 7 -> sonuc: 7

ON TAMAMLAMA STRATEJISI:
- 8 + 5: Once 8'i 10'a tamamla (8+2=10), kalan 3'u ekle (10+3=13)
- 7 + 6: Once 7'yi 10'a tamamla (7+3=10), kalan 3'u ekle (10+3=13)
"""
},

"MAT.1.1.CIKARMA": {
    "unite": "Sayilar ve Islemler",
    "baslik": "Cikarma Islemi (0-100)",
    "icerik": """
CIKARMA ISLEMI:

TEMEL KAVRAMLAR:
- Cikarma isareti: - (eksi)
- Eksilen - Cikan = Fark (Kalan)
- Ornek: 8 - 3 = 5 (8'den 3 cikarilirsa 5 kalir)

CIKARMA OZELLIKLERI:
1. Degisme ozelligi YOKTUR: 8 - 3 ≠ 3 - 8
   (Cikarma isleminde yer degistirilemez)
2. Kendisinden cikarma: 5 - 5 = 0
   (Bir sayidan kendisi cikarilirsa sifir kalir)
3. Sifir cikarma: 7 - 0 = 7
   (Bir sayidan sifir cikarilirsa sayi degismez)

ONLUK BOZMADAN CIKARMA:
- Birler basamagindaki cikarma mumkunse dogrudan yapilir.
- Ornekler:
  48 - 23 = 25 (8-3=5 birler, 4-2=2 onlar)
  76 - 31 = 45 (6-1=5 birler, 7-3=4 onlar)

ONLUK BOZARAK CIKARMA:
- Birler basamaginda cikarma yapilamazsa onlar basamagindan 1 onluk (10) birler basamagina aktarilir.
- Ornekler:
  42 - 17 = 25
  Birler: 2'den 7 cikilamaz -> Onlardan 1 al: 12 - 7 = 5
  Onlar: 3 (4-1) - 1 = 2
  Sonuc: 25

TOPLAMA-CIKARMA ILISKISI:
- Toplama ve cikarma ters islemlerdir.
- 5 + 3 = 8 ise 8 - 3 = 5 ve 8 - 5 = 3
- Bu iliski islem kontrolunde kullanilir.

PROBLEM COZME:
- "Ali'nin 12 bilye vardi, 5 tanesini kaybetti. Kac bilyesi kaldi?"
  12 - 5 = 7 bilye kaldi.
- "Sepette 8 elma vardi, 6 tane daha koyduk. Kac elma oldu?"
  8 + 6 = 14 elma oldu.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: GEOMETRI
# ═══════════════════════════════════════════════════════════════

"MAT.1.2.GEOMETRIK_SEKILLER": {
    "unite": "Geometri",
    "baslik": "Geometrik Sekiller ve Uzamsal Iliskiler",
    "icerik": """
GEOMETRIK SEKILLER (1. sinif):

1. KARE:
   - 4 kenar, 4 kose
   - Tum kenarlari esit uzunlukta
   - Tum acilari dik aci (90 derece)
   - Gunluk hayat ornekleri: bisko, pencere, karo

2. DIKDORTGEN:
   - 4 kenar, 4 kose
   - Karsi kenarlari esit uzunlukta
   - Tum acilari dik aci (90 derece)
   - Gunluk hayat ornekleri: kapı, kitap, tahta, telefon

3. UCGEN:
   - 3 kenar, 3 kose
   - Farkli turde ucgenler olabilir (1. sinifta tur ayrimina girilmez)
   - Gunluk hayat ornekleri: aci, bayrak sekli, cati

4. DAIRE:
   - Kosesi ve kenari yoktur (egrisel sekil)
   - Bir merkez noktasi vardir
   - Merkezden cevreye olan uzaklik her yerde ayni (yaricap)
   - Gunluk hayat ornekleri: tekerlek, saat, tabak, para

UZAMSAL ILISKILER:

1. SAG - SOL:
   - Sagimiz: Yazi yazdigimiz elimiz (cogu kisi icin)
   - Solumuz: Diger elimiz
   - "Kitap masanin saginda." "Silgi masanin solunda."

2. UST - ALT:
   - Ust: Yukari yonde olan
   - Alt: Asagi yonde olan
   - "Kus dalın ustunde." "Kedi masanin altinda."

3. IC - DIS:
   - Ic: Bir seklin veya cismin icinde
   - Dis: Bir seklin veya cismin disinda
   - "Top kutunun icinde." "Kedi evin disinda."

4. ONDE - ARKADA:
   - "Ali, Ayse'nin onunde oturuyor."
   - "Okul, parkin arkasinda."

5. YAKIN - UZAK:
   - "Okul evimize yakin." "Market evimize uzak."

CISIMLER VE SEKILLER:
- Kup (zar, rubik): Her yuzu kare
- Dikdortgenler prizması (kutu): Her yuzu dikdortgen
- Silindir (konserve kutusu): Yuvarlak tabanli
- Kure (top): Her yonden yuvarlak
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: OLCME
# ═══════════════════════════════════════════════════════════════

"MAT.1.3.OLCME": {
    "unite": "Olcme",
    "baslik": "Uzunluk, Zaman ve Para",
    "icerik": """
UZUNLUK KARSILASTIRMA:

1. DOGRUDAN KARSILASTIRMA:
   - Iki nesneyi yan yana koyarak karsilastirma
   - Kisa - uzun, daha kisa - daha uzun, en kisa - en uzun
   - Ornek: "Kalem silgiden uzun." "Agac evden yuksek."

2. STANDART OLMAYAN OLCME:
   - Karis, adim, karış, parmak gibi birimlerle olcme
   - "Masa 5 karis uzunlugunda." "Sinif 20 adim genisliginde."
   - Not: Bu olcumler kisiden kisiye degisir.

ZAMAN:

1. DUN - BUGUN - YARIN:
   - Dun: Gecen gun (gecmis)
   - Bugun: Bu gun (simdi)
   - Yarin: Gelecek gun (gelecek)

2. HAFTANIN GUNLERI (7 gun):
   Pazartesi, Sali, Carsamba, Persembe, Cuma, Cumartesi, Pazar
   - Hafta ici: Pazartesi - Cuma (5 gun, okul gunleri)
   - Hafta sonu: Cumartesi - Pazar (2 gun, tatil)

3. YILIN AYLARI (12 ay):
   Ocak, Subat, Mart, Nisan, Mayis, Haziran,
   Temmuz, Agustos, Eylul, Ekim, Kasim, Aralik

4. MEVSIMLER:
   - Ilkbahar: Mart, Nisan, Mayis
   - Yaz: Haziran, Temmuz, Agustos
   - Sonbahar: Eylul, Ekim, Kasim
   - Kis: Aralik, Ocak, Subat

5. SAAT OKUMA:
   - Tam saat: Kisa akrep sayinin uzerinde, uzun yelkovan 12'de
     Ornek: Saat 3:00 = "Saat uc"
   - Yarim saat: Uzun yelkovan 6'da
     Ornek: Saat 3:30 = "Ucu yirmi dakika geciyor" degil "Uc bucuk"
   - Akrep: Kisa, kalin -> Saati gosterir
   - Yelkovan: Uzun, ince -> Dakikayi gosterir

PARA:

1. TURK LIRASI (TL) VE KURUS:
   - 1 TL = 100 kurus
   - Madeni paralar: 5 kr, 10 kr, 25 kr, 50 kr, 1 TL
   - Kagit paralar (banknotlar): 5 TL, 10 TL, 20 TL, 50 TL, 100 TL, 200 TL
   - Ataturk resmi tum Turk Lirasi banknotlarinda bulunur.

2. PARA ILE TOPLAMA:
   - 5 TL + 10 TL = 15 TL
   - 25 kr + 25 kr = 50 kr
   - 50 kr + 50 kr = 1 TL (= 100 kr)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: VERI ISLEME
# ═══════════════════════════════════════════════════════════════

"MAT.1.4.VERI": {
    "unite": "Veri Isleme",
    "baslik": "Tablo ve Grafik (Basit Cetele)",
    "icerik": """
VERI TOPLAMA VE GOSTERME:

1. CETELE (SAYIM) TABLOSU:
   - Verileri saymak icin cetele (|) isareti kullanilir.
   - Her bes cetele bir grup olusturur: |||| = 5
   - Ornek:
     Meyve    | Cetele    | Sayi
     ---------|-----------|-----
     Elma     | ||||      |  4
     Armut    | |||       |  3
     Portakal | |||| |    |  6
     Muz      | ||        |  2

2. TABLO OKUMA:
   - Tablodaki verileri okuyarak soruları cevaplama:
     * "En cok hangi meyve var?" -> Portakal (6 tane)
     * "En az hangi meyve var?" -> Muz (2 tane)
     * "Toplam kac meyve var?" -> 4 + 3 + 6 + 2 = 15

3. BASIT GRAFIK (SUTUN GRAFIGI):
   - Cetele tablosundaki veriler sutun grafigine donusturulur.
   - Her sutun bir kategoriyi temsil eder.
   - Sutunun yuksekligi sayiyi gosterir.
   - Ornek: Siniftaki ogrencilerin en sevdigi renk
     Kirmizi: 8 ogrenci -> 8 birim yukseklikte sutun
     Mavi: 12 ogrenci -> 12 birim yukseklikte sutun
     Yesil: 5 ogrenci -> 5 birim yukseklikte sutun

4. GRAFIK YORUMLAMA:
   - "Hangi rengi en cok kisi sevmis?" -> Mavi (12)
   - "Kirmizi ve yesili seven kisi sayisi toplami?" -> 8 + 5 = 13
   - "Mavi ile kirmizi arasindaki fark?" -> 12 - 8 = 4

5. SINIFLANDIRMA:
   - Nesneleri rengine, sekline, boyutuna gore gruplama
   - Ornek: Oyuncaklari buyuk-kucuk, renklerine gore ayirma
   - Canli-cansiz, dogal-yapay gibi siniflama
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_matematik1_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in MATEMATIK_1_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_matematik1_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(MATEMATIK_1_REFERANS.keys())
