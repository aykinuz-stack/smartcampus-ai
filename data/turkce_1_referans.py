# -*- coding: utf-8 -*-
"""
1. Sinif Turkce dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Bu dosya, AI ders anlatiminda dogru bilgi kullanilmasini saglamak icin
1. sinif Turkce mufredatina gore organize edilmis referans icerik barindirir.

Konular:
1. Ses ve Harf Ogretimi
2. Hece Olusturma
3. Kelime Okuma ve Yazma
4. Cumle Olusturma
5. Noktalama ve Buyuk Harf
6. Dinleme ve Anlama
7. 5N1K Sorulari
8. Tekerlemeler, Ninniler, Siirler
9. Alfabe Sirasi
"""

TURKCE_1_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. SES VE HARF OGRETIMI
# ═══════════════════════════════════════════════════════════════

"T1.1.SESLI_HARFLER": {
    "unite": "Ses ve Harf Ogretimi",
    "baslik": "Sesli (Unlu) Harfler",
    "icerik": """
SESLI HARFLER (8 ADET):
Turk alfabesinde 8 sesli (unlu) harf bulunur: a, e, i, i, o, o, u, u

SINIFLANDIRMA:

1. KALIN UNLULER: a, i, o, u
   - Soylenis sirasinda dil arkaya cekilir.
   - Ornekler: araba, balik, orman, uzum

2. INCE UNLULER: e, i, o, u
   - Soylenis sirasinda dil one gelir.
   - Ornekler: elma, igne, ordek, uzum

3. DUZ UNLULER: a, e, i, i
   - Dudaklar duz (yayvan) konumdadir.
   - Ornekler: anne, ekmek, incir, irmak

4. YUVARLAK UNLULER: o, o, u, u
   - Dudaklar yuvarlak konumdadir.
   - Ornekler: okul, ogretmen, uzum, utu

OGRETIM SIRASI (MEB oneri):
- Ilk ogretilen sesli harfler: e, a, i
- Daha sonra: o, u, u, i, o
- Her harf ses olarak tanitilir, sonra yazimi ogretilir.

TEMEL KURALLAR:
- Her hecede mutlaka bir sesli harf bulunur.
- Sesli harf tek basina hece olusturabilir: a-ri, e-rik, o-kul
- Turkcede iki sesli harf yan yana gelmez (yabanci kokenli sozcukler haric).
"""
},

"T1.1.SESSIZ_HARFLER": {
    "unite": "Ses ve Harf Ogretimi",
    "baslik": "Sessiz (Unsuz) Harfler",
    "icerik": """
SESSIZ HARFLER (21 ADET):
Turk alfabesinde 21 sessiz (unsuz) harf bulunur:
b, c, c, d, f, g, g, h, j, k, l, m, n, p, r, s, s, t, v, y, z

OGRETIM SIRASI (MEB oneri):
- Kolay sesler once ogretilir: l, n, r, m, t, k, s
- Zor sesler sonra ogretilir: g, j, h, v
- Benzer sesler ayri zamanlarda ogretilir (b-d, m-n, s-z gibi)

SINIFLANDIRMA:

1. SERT UNSUZLER: c, f, h, k, p, s, s, t
   - "Fistarik sePetCi HaSan" cumlesiyle hatirlama
   - Ses tellerinin titresimi olmadan cikan sesler

2. YUMUSAK UNSUZLER: b, c, d, g, g, j, l, m, n, r, v, y, z
   - Ses tellerinin titremesiyle cikan sesler

SESSIZ HARF OGRETIM YONTEMI:
- Harf sesi ogretilir (harf adi degil): "be" degil "b", "ke" degil "k"
- Sesli harfle birlestirilerek hece olusturulur: l + a = la, l + e = le
- Goruntuler ve nesnelerle iliskilendirilir: "b" = balik, "m" = masa

ONEMLI UYARI:
- "g" harfi tek basina soylenemez, sadece hece icinde soylenir.
- "g" kelime basinda bulunmaz (Turkce kelimelerde).
"""
},

"T1.1.SES_OGRETIM_YONTEMI": {
    "unite": "Ses ve Harf Ogretimi",
    "baslik": "Ses Tabanli Cumle Yontemi",
    "icerik": """
SES TABANLI CUMLE YONTEMI (MEB 2025):
1. sinifta okuma-yazma ogretiminde "Ses Tabanli Cumle Yontemi" kullanilir.

ASAMALAR:

1. SESI HISSETME VE TANIMA:
   - Ses, bir nesne veya gorsel ile tanitilir.
   - Ogrenci sesi isitir, tekrar eder.
   - Ornek: Arinin sesi "vvv", ruzgarin sesi "sss"

2. SESI OKUMA VE YAZMA:
   - Sesin yazili karsiligi (harf) ogretilir.
   - Buyuk ve kucuk harf birlikte ogretilir: A-a, E-e
   - Dik temel yazi kullanilir (el yazisindan once).

3. SESTEN HECEYE:
   - Ogrenilen sesler birlestirilerek hece olusturulur.
   - Ilk olarak acik heceler: a-la, e-le, a-li
   - Sonra kapali heceler: el, al, an

4. HECEDEN KELIMEYE:
   - Heceler birlestirilerek anlamli kelimeler olusturulur.
   - Ornek: a + la = ala, e + le = ele

5. KELIMEDEN CUMLEYE:
   - Kelimeler bir araya getirilerek cumleler olusturulur.
   - Ornek: "Ali ata." "Ela elma aldi."

HARF GRUPLARI (Ogretim Sirasi):
- 1. Grup: e, l, a, t (ilk ogretilen harfler)
- 2. Grup: i, n, o, r, m
- 3. Grup: u, k, i, s, d, y
- 4. Grup: b, u, s, z, c, g, p
- 5. Grup: h, g, v, c, o, f, j
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. HECE OLUSTURMA
# ═══════════════════════════════════════════════════════════════

"T1.2.HECE": {
    "unite": "Hece Olusturma",
    "baslik": "Hece Yapisi ve Cesitleri",
    "icerik": """
HECE TANIMI:
Agzimizi her acip kapadigimizda bir hece soyleriz.
Her hecede mutlaka bir sesli harf bulunur.

HECE CESITLERI:

1. ACIK HECE:
   - Sesli harf ile biten hece.
   - Ornekler: a-ri, ka-pi, de-ni, ba-ba, su-la-ma
   - En sik gorilen hece turudur.

2. KAPALI HECE:
   - Sessiz harf ile biten hece.
   - Ornekler: el, kar, top, bal-kon, yor-gan

3. TEK SESLI HECE:
   - Sadece bir sesli harften olusan hece.
   - Ornekler: a-ci, o-da, u-cak (ilk heceleri tek sesli)

HECE BOLME KURALLARI:
- Iki sesli harf arasindaki sessiz harf, sonraki heceye gider: a-ra-ba (a-ra-ba)
- Yan yana iki sessiz varsa: ilki onceki heceye, ikincisi sonrakine: bas-kal
- Satir sonunda kelime bolunemiyorsa, kelime bir sonraki satira tasinir.

HECE SAYISI BELIRLEME:
- Kelimede kac sesli harf varsa o kadar hece vardir.
  * "ev" -> 1 hece (1 sesli: e)
  * "araba" -> 3 hece (3 sesli: a-a-a)
  * "okul" -> 2 hece (2 sesli: o-u)

UYGULAMA ORNEKLERI:
- anne -> an-ne (2 hece)
- elma -> el-ma (2 hece)
- kalem -> ka-lem (2 hece)
- televizyon -> te-le-viz-yon (4 hece)
- kitap -> ki-tap (2 hece)
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. KELIME OKUMA VE YAZMA
# ═══════════════════════════════════════════════════════════════

"T1.3.KELIME": {
    "unite": "Kelime Okuma ve Yazma",
    "baslik": "Kelime Olusturma ve Okuma",
    "icerik": """
KELIME OKUMA SURECI:

1. HARFLERDEN HECEYE:
   - Ogrenilen harfler birlestirilerek hece olusturulur.
   - Ornek: e + l = el, a + l = al, a + t = at

2. HECELERDEN KELIMEYE:
   - Heceler birlestirilerek anlamli kelimeler elde edilir.
   - Ornek: a + la = ala, a + ta = ata, el + ma = elma

ILK OKUNAN KELIMELER (ogretim sirasina gore):
- 1. Grup (e, l, a, t): ele, ata, et, al, ela, tel, tale
- 2. Grup (+i, n, o, r, m): anne, nine, mini, tren, limon
- 3. Grup (+u, k, i, s, d, y): kutu, disk, yildiz, simit
- 4. Grup (+b, u, s, z, c, g, p): buzul, sucuk, copse
- 5. Grup (+h, g, v, c, o, f, j): havuz, ceviz, jeton

YAZMA BECERILERI:
- Dik temel yazi (1. sinif): Harfler dumduz ve ayrik yazilir.
- Satir araligi: Ogrenci defterleri genis cizgilidir.
- Harfler arasi bosluk: Her harf birbirinden ayri yazilir.
- Kelimeler arasi bosluk: Bir parmak kadar bosluk birakilir.

SIK KULLANILAN KELIMELER (gorme sozcukleri):
- "ve", "bir", "bu", "o", "ben", "sen", "biz", "de", "da"
- "ile", "icin", "gibi", "ama", "var", "yok", "ne", "her"
- Bu kelimeler sikca karsilasildigi icin ezbere taninir.

KELIME HAZINESI GELISTIRME:
- Resimli sozluk calismalari
- Nesne-kelime eslestirme
- Kelime kartlari (flash card)
- Gunluk hayattan kelimeler: okul, ev, aile, yemek, hayvan
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. CUMLE OLUSTURMA
# ═══════════════════════════════════════════════════════════════

"T1.4.CUMLE": {
    "unite": "Cumle Olusturma",
    "baslik": "Basit Cumle Yapisi ve Kurma",
    "icerik": """
CUMLE TANIMI:
Bir dusunceyi, duyguyu veya istegi tam olarak anlatan soz dizisine cumle denir.
Cumle buyuk harfle baslar ve noktalama isaretiyle biter.

BASIT CUMLE YAPISI:
Turkce cumle yapisi: Ozne + Tümleç + Yüklem (fiil sonda gelir)

ORNEKLER:
- "Ali kosuyor." (Ozne + Yuklem)
- "Kedi sutu icti." (Ozne + Nesne + Yuklem)
- "Anne eve geldi." (Ozne + Yer + Yuklem)

CUMLE TIPLERI (1. sinif duzeyi):

1. OLUMLU CUMLE:
   - Bir isi, durumu veya olusi bildirir.
   - Ornek: "Kus ucuyor." "Ben okula gidiyorum."

2. OLUMSUZ CUMLE:
   - Isin yapilmadigini bildirir. "degil", "-ma/-me" kullanilir.
   - Ornek: "Kus ucmuyor." "Ben hasta degilim."

3. SORU CUMLESI:
   - Soru sorar. Soru isaretiyle biter.
   - Ornek: "Sen nereye gidiyorsun?" "Bu ne?"

4. UNLEM CUMLESI:
   - Saskinlik, sevinc, korku gibi duygulari ifade eder.
   - Ornek: "Ne guzel!" "Dikkat et!"

CUMLE YAZMA ADIMI:
1. Dusunceni belirle (Ne soylemek istiyorsun?)
2. Kelimeleri sirayla yaz
3. Buyuk harfle basla
4. Sonuna noktalama isareti koy
5. Cumleyi tekrar oku ve kontrol et

ORNEK CUMLELER (1. sinif duzeyi):
- "Ben Ali." / "Benim adim Ela."
- "Annem beni seviyor."
- "Bugün hava güzel."
- "Topu bahceye attim."
- "Kedimizin adi Pamuk."
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. NOKTALAMA VE BUYUK HARF
# ═══════════════════════════════════════════════════════════════

"T1.5.NOKTALAMA": {
    "unite": "Noktalama ve Buyuk Harf",
    "baslik": "Noktalama Isaretleri",
    "icerik": """
1. SINIFTA OGRETILEN NOKTALAMA ISARETLERI:

1. NOKTA (.):
   - Cumle sonuna konur.
   - Cumlenin bittigi yeri gosterir.
   - Ornek: "Bugün okula gittim."
   - Kisaltmalarin sonuna konur: Dr. Prof. vb.

2. SORU ISARETI (?):
   - Soru cumlelerinin sonuna konur.
   - Soru kelimesi iceren cumlelerde kullanilir.
   - Ornek: "Adin ne?" "Nereye gidiyorsun?" "Bu senin mi?"

BUYUK HARF KULLANIMI:

1. CUMLE BASI:
   - Her cumle buyuk harfle baslar.
   - Ornek: "Okula gittim. Ders calistim."

2. OZEL ISIMLER:
   - Kisi adlari: Ali, Ayse, Mehmet, Zeynep
   - Soyadi: Yilmaz, Demir, Kaya
   - Sehir adlari: Ankara, Istanbul, Izmir
   - Ulke adlari: Turkiye, Almanya
   - Nehir, dag, deniz: Kizilirmak, Agri Dagi, Karadeniz
   - Hayvan adlari (ozel ad): Pamuk, Karabas, Tekir

3. SATIR BASI:
   - Siir satirlari buyuk harfle baslar.

YAYGIN HATALAR:
- "ali" degil "Ali" (kisi adi buyuk harfle baslar)
- "turkiye" degil "Turkiye" (ulke adi buyuk harfle baslar)
- Cumle basinda kucuk harf kullanmak yanlistir.
- Cumle sonunda nokta unutmak yanlistir.
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. DINLEME VE ANLAMA
# ═══════════════════════════════════════════════════════════════

"T1.6.DINLEME": {
    "unite": "Dinleme ve Anlama",
    "baslik": "Dinleme Becerileri ve Anlama Stratejileri",
    "icerik": """
DINLEME BECERILERI (1. sinif):

1. DINLEME KURALLARI:
   - Konusani dikkatle dinle, goz temasi kur.
   - Konusan kisinin sozunu kesme.
   - Dinlerken sessiz ol.
   - Anlam bilmedigin kelimeyi sor.
   - Dinlediklerini hatirlamaya calis.

2. DINLEME TURLERI:
   a) Hikaye dinleme: Ogretmenin okudugu hikayeyi dinleme
   b) Siir dinleme: Ritim ve kafiyeye dikkat ederek dinleme
   c) Yonerge dinleme: Verilen talimati anlama ve uygulama
   d) Muzik dinleme: Sarki sozlerini takip etme

3. ANLAMA STRATEJILERI:
   - Baslik ve resimlere bakarak tahmin etme
   - Dinlerken zihninde canlandirma (gorsellestirme)
   - Dinledikten sonra ozetleme
   - Sorulara cevap verme
   - Siralama: Olaylari oluslarina gore siralama

4. KONUSMA BECERILERI:
   - Parmak kaldirarak soz isteme
   - Duygu ve dusuncelerini ifade etme
   - Anlasilir bir ses tonuyla konusma
   - Sira ile konusma
   - "Lutfen", "tesekkur ederim", "ozur dilerim" kaliplari

5. DINLEME SONRASI ETKINLIKLER:
   - Dinledigi hikayeyi kendi kelimeleriyle anlatma
   - Resimleri olaya gore siralama
   - Ana karakteri ve olaylari belirleme
   - "Bu hikayede ne oldu?" sorusuna cevap verme
"""
},

# ═══════════════════════════════════════════════════════════════
# 7. 5N1K SORULARI
# ═══════════════════════════════════════════════════════════════

"T1.7.5N1K": {
    "unite": "5N1K Sorulari",
    "baslik": "5N1K Soru Kelimeleri ve Kullanimi",
    "icerik": """
5N1K SORU KELIMELERI:

1. NE? (What?)
   - Bir seyin ne oldugunu sorar.
   - Ornek: "Bu ne?" -> "Bu bir kalem."
   - "Ne yapiyorsun?" -> "Resim ciziyorum."

2. NEREDE? (Where?)
   - Yeri, konumu sorar.
   - Ornek: "Kitap nerede?" -> "Kitap masanin ustunde."
   - "Nerede oturuyorsun?" -> "Ankara'da oturuyorum."

3. NE ZAMAN? (When?)
   - Zamani sorar.
   - Ornek: "Ne zaman geldin?" -> "Dun geldim."
   - "Okul ne zaman basliyor?" -> "Eylulde basliyor."

4. KIM? (Who?)
   - Kisiyi sorar.
   - Ornek: "Bunu kim yapti?" -> "Ali yapti."
   - "Ogretmenin kim?" -> "Ogretmenim Ayse hanim."

5. NEDEN / NICIN? (Why?)
   - Sebebi, nedeni sorar.
   - Ornek: "Neden agliyorsun?" -> "Dizim acidiyor."
   - "Nicin okula gidiyoruz?" -> "Ogrenmeye gidiyoruz."

6. NASIL? (How?)
   - Sekli, durumu sorar.
   - Ornek: "Bugün nasilsin?" -> "Iyiyim, tesekkurler."
   - "Okula nasil gidiyorsun?" -> "Otobus ile gidiyorum."

5N1K ILE METIN ANLAMA:
- Bir hikaye okuduktan sonra 5N1K sorulariyla metin analiz edilir:
  * Kim? -> Hikayenin kahramanlari
  * Ne? -> Hikayedeki olaylar
  * Nerede? -> Olaylarin gectigi yer
  * Ne zaman? -> Olaylarin zamani
  * Neden? -> Olaylarin sebebi
  * Nasil? -> Olaylarin gelisimi
"""
},

# ═══════════════════════════════════════════════════════════════
# 8. TEKERLEMELER, NINNILER, SIIRLER
# ═══════════════════════════════════════════════════════════════

"T1.8.SOZEL_KULTUR": {
    "unite": "Tekerlemeler, Ninniler, Siirler",
    "baslik": "Sozlu Kultur ve Edebiyat Turleri",
    "icerik": """
1. TEKERLEMELER:
Hizli soylendiginde dil becerisi gelistiren, eglenceli soz dizileridir.

Ornekler:
- "Bir berber bir berbere gel beraber bir berber dukkanı acalim demis."
- "Sak sak sakaci, sakinin kosesi, kosede karga, karganin yuvasi."
- "Dal sarkar kartal kalkar, kartal kalkar dal sarkar."
- "Pirasa sarmasik, sarmasik pirasa."

Amaci: Dogru ve akici telaffuz, dikkat, dil becerisi gelistirme.

2. NINNILER:
Annelerin cocuklarina soyledigi melodik sozlerdir.

Ornekler:
- "Dandini dandini dastana, danalar girdi bostana..."
- "Uyusun da buyusun, ninni..."
- "Hu hu huu, bebesini uyutuyor anasi..."

Amaci: Dil gelisimi, ritim duygusu, kulturel aktarim.

3. SIIRLER (1. sinif duzeyi):
Olculu ve kafiyeli sozler iceren edebi metinlerdir.

Siir Ozellikleri:
- Dize (misra): Siirin her bir satiri
- Kafiye (uyak): Dize sonlarindaki ses benzerligi
- Ritim: Siirin ahenkli okunmasi
- Kita (bend): Dize gruplari

1. Sinifta Siir Calismalari:
- Siir dinleme ve ezberleme
- Ritimli okuma (el cirparak, tempo tutarak)
- Siirdeki kelimeleri anlama
- Siirde gecen duygulari ifade etme

4. BILMECELER:
- "Yesil basli, kirmizi donlu, suda yuzer. (Ordek)"
- "Beyaz inek otlagi yalar. (Dil)"
- "Annem serer, babam toplar. (Yatak/Yorgan)"

5. MANILER:
Dort satirlik, kafiyeli halk siiri turudur.
Turk kulturunun onemli bir parcasidir.
"""
},

# ═══════════════════════════════════════════════════════════════
# 9. ALFABE SIRASI
# ═══════════════════════════════════════════════════════════════

"T1.9.ALFABE": {
    "unite": "Alfabe Sirasi",
    "baslik": "Turk Alfabesi ve Siralama",
    "icerik": """
TURK ALFABESI (29 HARF):

Sira | Buyuk | Kucuk | Tur
-----|-------|-------|--------
 1   |   A   |   a   | Sesli
 2   |   B   |   b   | Sessiz
 3   |   C   |   c   | Sessiz
 4   |   C   |   c   | Sessiz
 5   |   D   |   d   | Sessiz
 6   |   E   |   e   | Sesli
 7   |   F   |   f   | Sessiz
 8   |   G   |   g   | Sessiz
 9   |   G   |   g   | Sessiz
10   |   H   |   h   | Sessiz
11   |   I   |   i   | Sesli
12   |   I   |   i   | Sesli
13   |   J   |   j   | Sessiz
14   |   K   |   k   | Sessiz
15   |   L   |   l   | Sessiz
16   |   M   |   m   | Sessiz
17   |   N   |   n   | Sessiz
18   |   O   |   o   | Sesli
19   |   O   |   o   | Sesli
20   |   P   |   p   | Sessiz
21   |   R   |   r   | Sessiz
22   |   S   |   s   | Sessiz
23   |   S   |   s   | Sessiz
24   |   T   |   t   | Sessiz
25   |   U   |   u   | Sesli
26   |   U   |   u   | Sesli
27   |   V   |   v   | Sessiz
28   |   Y   |   y   | Sessiz
29   |   Z   |   z   | Sessiz

ONEMLI BILGILER:
- Turk alfabesi Latin harflerine dayanir (1 Kasim 1928, Harf Devrimi).
- Ingiliz alfabesinden farkli olarak Q, W, X harfleri yoktur.
- Turk alfabesine ozgu harfler: C, G, I, O, S, U
- "I" ve "I" harfleri farklidir:
  * I (buyuk) -> i (kucuk): Noktalı i
  * I (buyuk) -> i (kucuk): Noktasiz i
- Toplam: 8 sesli + 21 sessiz = 29 harf

ALFABE SIRASI ILE SIRALAMA:
- Sozcukleri sozlukte bulmak icin alfabe sirasini bilmek gerekir.
- Ilk harf ayni ise ikinci harfe bakilir.
- Ornek siralama: araba, balik, canta, cicek, defter, elma
"""
},

}

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSIYONLAR
# ═══════════════════════════════════════════════════════════════

def get_turkce1_reference(topic: str) -> list:
    """Verilen konuya en uygun referans iceriklerini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in TURKCE_1_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]


def get_all_turkce1_keys() -> list:
    """Tum referans anahtarlarini listeler."""
    return list(TURKCE_1_REFERANS.keys())
