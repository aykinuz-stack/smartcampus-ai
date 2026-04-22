# SmartCampus AI - Ogretmen Kullanim Kilavuzu

**Versiyon:** 2.0  
**Son Guncelleme:** Nisan 2026  
**Hedef Kitle:** Sinif ogretmenleri, brans ogretmenleri, rehber ogretmenler

---

## Icindekiler

1. [Sisteme Giris](#1-sisteme-giris)
2. [Yoklama Alma](#2-yoklama-alma)
3. [Not Girisi](#3-not-girisi)
4. [Odev Atama](#4-odev-atama)
5. [Ders Defteri](#5-ders-defteri)
6. [Sinav Sonuclari](#6-sinav-sonuclari)
7. [Akademik Takip](#7-akademik-takip)
8. [Olcme ve Degerlendirme](#8-olcme-ve-degerlendirme)
9. [Mesajlasma](#9-mesajlasma)
10. [Mobil Uygulama](#10-mobil-uygulama)
11. [Ipuclari ve En Iyi Uygulamalar](#11-ipuclari-ve-en-iyi-uygulamalar)

---

## 1. Sisteme Giris

### 1.1 Giris Bilgileri

| Bilgi           | Deger                        |
|-----------------|------------------------------|
| URL             | http://localhost:8501        |
| Kullanici Adi   | `ogretmen`                   |
| Sifre           | `SmartCampus123`             |
| Rol             | Ogretmen                     |

> **NOT:** Her ogretmenin kendi kullanici adi vardir (orn. `ali.yilmaz`).
> Yukaridaki bilgiler demo hesabi icindir. IK tarafindan size ozel
> kullanici adi ve gecici sifre verilecektir.

### 1.2 Giris Adimlari

1. Tarayicinizda sistem adresini acin.
2. Kullanici adinizi ve sifrenizi girin.
3. **Giris Yap** butonuna basin.
4. Ilk giristeyseniz sifre degistirmeniz istenecektir.

### 1.3 Sidebar Navigasyonu

Giris yaptiktan sonra sol tarafta erisebileceginiz moduller listelenir. Ogretmen rolunde su moduller gorunur:

| Modul                        | Aciklama                                    |
|------------------------------|---------------------------------------------|
| Ana Sayfa                    | Gunluk ozet ve bildirimler                  |
| Ogrenci Zeka Merkezi         | Ogrenci 360 gorunumu, erken uyari           |
| Akademik Takip               | Yoklama, not, odev, ders defteri            |
| Olcme ve Degerlendirme       | Soru bankasi, sinav olusturma               |
| Okul Oncesi - Ilkokul        | Ilkokul kazanim ve materyal yonetimi        |
| Rehberlik                    | Rehberlik hizmetleri                        |
| Sosyal Etkinlik ve Kulupler  | Kulup ve etkinlik yonetimi                  |
| Kutuphane                    | Kutuphane erisimi                           |
| AI Ogrenme Platformu         | Dijital icerik ve bireysel egitim           |
| Yabanci Dil                  | Dil ogretim araclari                        |
| Kisisel Dil Gelisimi         | Ogrenci dil gelisim takibi                  |
| Egitim Koclugu               | Mesleki gelisim araclari                    |
| AI Treni                     | Interaktif AI ogrenme oyunlari              |
| AI Destek                    | Yapay zeka destekli yardim                  |

---

## 2. Yoklama Alma

Yoklama alma, ogretmenin en sik kullanacagi islevlerden biridir. SmartCampus AI'da birkac farkli yoklama yontemi vardir.

### 2.1 Manuel Yoklama

**Yol:** Akademik Takip > Yoklama & Notlar > Yoklama & Devamsizlik

1. **Sinif secin:** Acilir menuden sinif/subenizi secin (orn. "5-A").
2. **Tarih secin:** Varsayilan bugunun tarihidir. Gerekirse degistirebilirsiniz.
3. **Ders saati secin:** Hangi ders saati icin yoklama aliyorsunuz.
4. Ogrenci listesi goruntulenecektir.
5. Her ogrenci icin durumu secin:

| Durum      | Anlami                                 | Renk   |
|------------|----------------------------------------|--------|
| Devam      | Ogrenci derstedir                      | Yesil  |
| Devamsiz   | Ogrenci yoktur (ozursuz)               | Kirmizi|
| Gec        | Ogrenci derse gec gelmistir            | Turuncu|
| Izinli     | Ogrenci izinlidir (ozurlu devamsizlik) | Mavi   |

6. **Kaydet** butonuna basin.

### 2.2 Toplu Islem

Tum sinifi tek seferde isaretlemek icin:

- **"Hepsi Devam"** butonu: Tum ogrencileri "Devam" olarak isaretle. Sonra sadece devamsiz olanlari tek tek degistirin.
- **"Hepsi Yok"** butonu: Tum ogrencileri "Devamsiz" olarak isaretle. Sonra gelenleri "Devam" olarak guncelleyin.

> **IPUCU:** Cogunluk dersteyse "Hepsi Devam" butonuyla baslayip
> sadece gelmeyenleri degistirmek en hizli yontemdir.

### 2.3 Swipe (Kaydirma) ile Yoklama

Mobil uyumlu arayuzde veya dokunmatik ekranlarda:

- **Sola kaydir** = Devamsiz olarak isaretle
- **Saga kaydir** = Gec olarak isaretle
- Varsayilan durum "Devam"dir; kaydirma yapmadiginiz ogrenciler devam sayilir.

### 2.4 QR Yoklama

Sinifta fiziksel QR kod kullanarak yoklama:

1. **Akademik Takip** icerisinde veya mobil uygulamada **QR Yoklama** sekmesine gidin.
2. **Kamera Ac** butonuna basin.
3. Ogrencinin kimlik kartindaki veya telefonundaki QR kodunu kameraya tutturun.
4. Sistem ogrenciyi otomatik taniyip "Devam" olarak kaydeder.
5. Her basarili okumada onay sesi ve yesil tik gorunur.
6. Tum ogrenciler tarandiktan sonra **Kaydet** ile yoklamayi sonlandirin.

> **NOT:** QR yoklama icin cihazinizin kamerasina tarayici erisimine izin vermeniz gerekir.
> Tarayici izin istediginde "Izin Ver" secin.

---

## 3. Not Girisi

Yazili sinav, sozlu, proje ve performans notlarini girin.

**Yol:** Akademik Takip > Yoklama & Notlar > Not Girisi

### 3.1 Not Girisi Adimlari

1. **Sinif secin:** Acilir menuden sinif/subeyi secin.
2. **Ders secin:** Acilir menuden dersinizi secin.
3. **Donem secin:** 1. Donem veya 2. Donem.
4. **Not Turu secin:** Yazili, sozlu, performans, proje, portfolyo vb.
5. **Ogrenci listesi** goruntulenir, her ogrencinin yaninda puan giris alani vardir.
6. Puanlari girin (0-100 arasi).
7. **Kaydet** butonuna basin.

### 3.2 Not Duzenleme

Daha once girdiginiz notlari duzenlemek icin:

1. Ayni filtrelerle (sinif, ders, donem, not turu) secim yapin.
2. Mevcut notlar otomatik yuklenir.
3. Degistirmek istediginiz puanlari guncelleyin.
4. **Kaydet** butonuna basin.

> **ONEMLI:** Not kayitlari degisiklik gecmisini tutar. Hangi degisikligi
> ne zaman yaptiginiz sistem tarafindan kayit altindadir.

### 3.3 Not Hesaplama

Sistem, girilen notlara gore su hesaplamalari otomatik yapar:

- Ders ortalamasi (agirliklara gore)
- Sinif siralamasi
- Donem ortalamasi
- Yilsonu ortalamasi

---

## 4. Odev Atama

Ogrencilerinize odev tanimlayin ve teslim surecini takip edin.

**Yol:** Akademik Takip > Ogretim & Planlama > Odev Takip

### 4.1 Yeni Odev Olusturma

1. **Yeni Odev** butonuna tiklayin.
2. Su bilgileri doldurun:

| Alan             | Aciklama                                       |
|------------------|-------------------------------------------------|
| Sinif            | Odevin atanacagi sinif/sube                     |
| Ders             | Ilgili ders                                      |
| Baslik           | Odevin kisa adi (orn. "5. Unite Calisma Kagidi")|
| Aciklama         | Detayli odev talimatlari                         |
| Teslim Tarihi    | Son teslim tarih ve saati                        |
| Odev Turu        | Dosya/link/video/QR                              |

3. Isterseniz ek dosya yukleyin (PDF, gorsel, video linki).
4. **Kaydet** butonuna basin.
5. Odev otomatik olarak ilgili siniftaki ogrenci ve velilere bildirim olarak iletilir.

### 4.2 Teslim Takibi

1. Atanmis odevlerin listesinden bir odev secin.
2. Her ogrenci icin teslim durumunu gorun:
   - **Teslim Edildi** (yesil): Ogrenci odevi yukledi
   - **Bekliyor** (sari): Henuz teslim edilmedi, sure devam ediyor
   - **Gecikti** (kirmizi): Teslim tarihi gecti, odev yuklenmedi
3. Teslim edilen odevleri inceleyebilir, puan ve yorum ekleyebilirsiniz.

---

## 5. Ders Defteri

Gunluk ders kayitlarinizi tutun.

**Yol:** Akademik Takip > Ogretim & Planlama > Ders Defteri

### 5.1 Gunluk Kayit Olusturma

1. **Tarih** secin (varsayilan bugun).
2. **Sinif** ve **Ders** secin.
3. **Ders Saati** secin.
4. Su bilgileri girin:

| Alan              | Aciklama                                     |
|-------------------|----------------------------------------------|
| Islenen Konu      | Derste islenen ana konu                      |
| Kazanimlar        | Hedeflenen MEB kazanimlari                   |
| Yapilan Etkinlik  | Ders icerisinde yapilan aktiviteler          |
| Odev/Gorev        | Verilen odevler veya gorevler                |
| Notlar            | Ek aciklamalar, gozlemler                    |

5. **Kaydet** butonuna basin.

### 5.2 Gecmis Kayitlar

1. Tarih araligini secin.
2. Gecmis ders kayitlarinizi goruntuleyebilir, duzenleyebilirsiniz.
3. Hangi kazanimlarin islenip islenmedigini takip edebilirsiniz.

> **IPUCU:** Ders defterini her ders sonrasinda hemen doldurmak
> en dogru ve eksiksiz kayit tutmayi saglar.

---

## 6. Sinav Sonuclari

Yazili sinavlar ve deneme sinavlarinin sonuc analizini yapin.

**Yol:** Akademik Takip > Raporlar (veya Olcme ve Degerlendirme > Sonuclar)

### 6.1 Yazili Sinav Analizi

1. **Sinif**, **Ders** ve **Sinav** secin.
2. Goruntulenecek bilgiler:
   - Sinif ortalamasi
   - En yuksek / en dusuk puan
   - Standart sapma
   - Puan dagilim grafigi (histogram)
   - Soru bazli basari oranlari
3. Basarisiz ogrencilerin listesini gorebilirsiniz.

### 6.2 Deneme Sinavi Sonuclari

1. Deneme sinavi sonuclarini yukleyin veya online sinav sonuclarini goruntuleyebilirsiniz.
2. Net sayisi analizi (dogru, yanlis, bos).
3. Konu bazli basari dagilimi.
4. Ogrencinin zaman icerisindeki gelisim grafigi.

### 6.3 Karsilastirmali Analiz

- Farkli sinavlar arasinda ogrenci gelisimini karsilastirin.
- Sinif ortalamasinin zaman icerisindeki degisimini izleyin.
- Konu/kazanim bazli zayif noktalari tespit edin.

---

## 7. Akademik Takip

Siniflariniz ve ogrencileriniz hakkinda butuncul bir gorunum elde edin.

**Yol:** Akademik Takip

### 7.1 Siniflarim

1. **Kadro & Ogrenci** grubundan sinif listesine erisin.
2. Sorumlu oldugunuz siniflari goruntuleyebilirsiniz.
3. Her sinif icin:
   - Ogrenci sayisi
   - Sinif ortalamasi
   - Devamsizlik orani
   - Son sinav sonuclari

### 7.2 Ogrenci Performans Izleme

1. **Ogrenci Yonetimi** veya **Ogrenci Zeka Merkezi** modulunden bir ogrenci secin.
2. Ogrencinin 360 derece profili goruntulenir:
   - **Not Gecmisi:** Tum derslerden alinan notlar ve trend
   - **Devamsizlik:** Yoklama durumu ve devamsizlik sayisi
   - **Sinav Performansi:** Sinav bazli puan degisimi
   - **Odev Durumu:** Teslim edilen/edilmeyen odevler
   - **Davranis:** Davranis kayitlari (varsa)

### 7.3 Akademik Planlama

1. **Ogretim & Planlama > Akademik Planlama** sekmesine gidin.
2. MEB yillik plani otomatik olarak yuklenir (6839+ kazanim kaydi).
3. Haftalik/aylik plan gorunumunde hangi kazanimlari isleyeceginizi gorun.
4. Plan uzerinde ilerlemenizi guncelleyebilirsiniz.

### 7.4 Kazanim Isleme Takibi

1. **Ogretim & Planlama > Uygulama Takibi** sekmesinden kazanim islenme durumunu isaretleyin.
2. Her kazanim icin durum:
   - **Islendi** (yesil)
   - **Kismen Islendi** (sari)
   - **Islenmedi** (kirmizi)
3. Islenme oranini grafik olarak takip edebilirsiniz.

---

## 8. Olcme ve Degerlendirme

Soru bankasi ve sinav olusturma araclari.

**Yol:** Olcme ve Degerlendirme

### 8.1 Soru Bankasi

1. **Soru Bankasi** sekmesine gidin.
2. Mevcut sorulari kategorilere gore goruntuleyebilirsiniz:
   - **Kazanim Bankasi:** MEB kazanimlarina bagli sorular
   - **Disardan Yuklenen:** PDF'den import edilen sorular
3. Filtreleme secenekleri: sinif, ders, konu, zorluk, soru tipi, ay

### 8.2 Soru Olusturma Sihirbazi

Yeni soru olusturmak icin 5 adimli sihirbazi kullanin:

1. **Adim 1 - Temel Bilgi:** Ders, sinif, kazanim secin.
2. **Adim 2 - Soru Tipi:** Coktan secmeli (MCQ), dogru/yanlis, bosulk doldurma, eslestirme, siralama, cloze veya matematik ifadesi.
3. **Adim 3 - Soru Metni:** Soruyu ve secenekleri yazin. Dogru cevabi isaretleyin.
4. **Adim 4 - Kalite:** Bloom taksonomisi seviyesi, zorluk, rubrik bilgileri.
5. **Adim 5 - Onizleme:** Soruyu kontrol edin ve **Kaydet** butonuyla onaylayin.

### 8.3 AI ile Soru Uretimi

Yapay zeka destekli otomatik soru uretimi:

1. **AI Soru Uretimi** sekmesine gidin.
2. **Ders** ve **Sinif** secin.
3. **Kazanim** secin (MEB yillik planindaki kazanimlar otomatik listelenir).
4. **Soru sayisi**, **zorluk** ve **Bloom seviyesi** belirleyin.
5. **Uret** butonuna basin.
6. AI tarafindan uretilen sorulari inceleyin.
7. Uygun gordugunuz sorulari **Onayla** ile soru bankasina ekleyin.
8. Gerekiyorsa soruyu duzenleyip tekrar kaydedin.

> **NOT:** AI soru uretimi OpenAI GPT-4o-mini kullanir.
> Uretilen sorulari mutlaka kontrol edin; icerik dogrulugu sizin sorumlulugunuzdadir.

### 8.4 Sinav Olusturma

1. **Blueprint (Sablon)** olusturun:
   - Sinav adi, ders, sinif
   - Soru sayisi ve dagilimi (kazanim, zorluk, Bloom)
   - Puan dagilimi
2. **Sinav Uret** butonuyla soru bankasindan otomatik soru secimi yapilir.
3. Secilen sorulari inceleyin, gerekirse degistirin.
4. Sinav ayarlarini yapin:
   - Sure
   - Soru/sik karistirma (deterministik seed ile)
   - Negatif puanlama (varsa)
   - Tab guvenlik (online sinav icin)
5. **Kaydet** ile sinavi olusturun.

### 8.5 PDF Sinav Ciktisi

1. Olusturdugunuz sinavi secin.
2. **PDF Indir** butonuna tiklayin.
3. Mevcut PDF formatlari:
   - **OSYM Formati:** 2 sutunlu, profesyonel kapak sayfasi, bolum basliklari
   - **Standart Format:** Tek sutunlu, basit tasarim
4. Optik form da ayri olarak indirilebilir (ogrenci bilgileri, baloncuklu cevap alani).

### 8.6 Online Sinav

1. Sinav ayarlarindan **Online Sinav** modunu aktif edin.
2. Ogrencilere sinav erisim kodu veya QR kod dagitilir.
3. Ogrenciler web uzerinden sinava girerler.
4. Sinav bitiminde sistem **otomatik puanlama** yapar (AutoGrader).
5. Sonuclar aninda goruntulenebilir.

---

## 9. Mesajlasma

Veli ve yonetimle iletisim.

### 9.1 Veli ile Iletisim

1. **Veli-Ogretmen Gorusme** modulune gidin (ILETISIM & RANDEVU grubunda).
2. Gelen gorusme taleplerini goruntuleyebilirsiniz.
3. Talepleri onaylayabilir veya farkli tarih onerebilirsiniz.
4. Gorusme sonrasi notlarinizi sisteme girebilirsiniz.

### 9.2 Bildirim Gonderme

- Odev atadiginizda ilgili sinifa otomatik bildirim gider.
- Sinav sonuclari girildiginde velilere bildirim iletilir.
- Devamsizlik kaydi olusturdugunuzda veliye aninda bilgi gider.

---

## 10. Mobil Uygulama

### 10.1 Genel Bilgi

SmartCampus AI mobil uygulamasi ogretmen rolunde **7 sayfa** sunar.

### 10.2 Mobil Sayfalar (Ogretmen Rolu)

| No | Sayfa           | Aciklama                                        |
|----|-----------------|--------------------------------------------------|
| 1  | Ana Sayfa       | Gunluk ozet, siniflarim, bildirimler             |
| 2  | Yoklama         | Sinif secip yoklama alma (toggle liste)          |
| 3  | QR Yoklama      | Kamera ile QR okutarak yoklama                   |
| 4  | Not Girisi      | Sinif/ders secip puan girisi                     |
| 5  | Odev Ata        | Yeni odev olusturma ve teslim takibi             |
| 6  | Ders Defteri    | Gunluk ders kaydi olusturma                      |
| 7  | Sinav Sonuc     | Sinav sonuc goruntuleyebilirsiniz ve analizi      |

### 10.3 Kurulum

1. APK dosyasini okul yonetiminden temin edin.
2. Android cihaziniza yukleyin.
3. Web sistemdeki kullanici adiniz ve sifrenizle giris yapin.

### 10.4 Mobilde Yoklama Alma

Mobil uygulamada yoklama almak en sik kullanilan islevdir:

1. Ana Sayfadan **Yoklama** kartina dokunun.
2. Sinif ve ders saatini secin.
3. Ogrenci listesi gorunur; her ismin yaninda toggle (devam/devamsiz) bulunur.
4. Devamsiz ogrencileri isaretleyin.
5. **Kaydet** butonuna dokunun.

> **IPUCU:** Mobilde QR Yoklama da kullanabilirsiniz.
> Telefonunuzun kamerasini acip ogrenci QR kodlarini sirayla okutun.

---

## 11. Ipuclari ve En Iyi Uygulamalar

### 11.1 Zaman Tasarrufu

- **Toplu Islemler:** Yoklamada "Hepsi Devam" butonuyla baslayip sadece devamsizlari degistirin.
- **Komut Paleti:** Ctrl+K ile modullere hizlica atlayin, menulerde gezinmek yerine.
- **Sablonlar:** Sinav blueprint'lerini kaydedin, her seferinde tekrar olusturmak yerine sablondan uretin.
- **AI Soru Uretimi:** Rutin sorulari AI'a urettirip, yaratici/ozel sorulari kendiniz yazin.

### 11.2 Veri Kalitesi

- Yoklamayi her ders basinda alin; geri donuk yoklama hataya aciktir.
- Not girisini sinav kagitlarini okur okumaz yapin.
- Ders defterini gun sonunda degil, ders bitiminde doldurun.
- Kazanim isleme takibini haftalik olarak guncelleyin.

### 11.3 Ogrenci Takibi

- Haftada bir **Ogrenci Zeka Merkezi** > **Erken Uyari** sekmesini kontrol edin.
- Not dususu veya devamsizlik artisi gosteren ogrenciler icin rehberlik servisiyle gorusun.
- Odev teslim orani dusuk ogrencilerle bireysel gorusme yapin.

### 11.4 Sinav Hazirlama

- Soru bankasini duzenli olarak zenginlestirin (her sinav sonrasi yeni sorular ekleyin).
- AI uretimli sorulari mutlaka icerik ve zorluk acisindan kontrol edin.
- Blueprint'lerde Bloom taksonomisi dagilimini dengeli tutun (sadece bilgi duzeyinde kalmak yerine analiz ve degerlendirme duzeyi de ekleyin).
- Online sinav kullaniyorsaniz, sinav oncesi tab guvenlik ayarlarini kontrol edin.

### 11.5 Iletisim

- Veli gorusme taleplerini 24 saat icinde yanitlayin.
- Odev ve sinav bildirimlerini en az 3 gun oncesinden gonderin.
- Ogrenci hakkinda olumsuz bildirimde bulunurken mutlaka olumlu bir noktayi da belirtin.

---

## Sik Sorulan Sorular

**S: Yanlis girdigim yoklamayi nasil duzeltirim?**
C: Ayni sinif, ayni tarih ve ayni ders saatini tekrar secin. Mevcut yoklama kaydi yuklenir, degisikligi yapip tekrar kaydedin.

**S: Gecmis bir tarihe not girebilir miyim?**
C: Evet, tarih secimini degistirerek gecmis tarihe not girebilirsiniz. Ancak donem kapanmis ise yonetici onayi gerekebilir.

**S: Soru bankasindaki sorulari baska ogretmenler de gorebilir mi?**
C: Evet, soru bankasi kurumsal paylasimlidir. Tum ogretmenler ayni soru havuzuna erisir. Ancak soru olusturucusu bilgisi kayitlidir.

**S: PDF'den soru yukleyebilir miyim?**
C: Evet. Olcme ve Degerlendirme modulunde **PDF Soru Cikarma** ozelligi vardir. PDF yuklediginizde AI soruları otomatik tanir ve soru bankasina ekler. Sinif, ders ve ay bilgilerini secmeniz zorunludur.

**S: Mobil uygulamadan sinav olusturabilir miyim?**
C: Mobil uygulama sinav sonuclarini goruntuleme icin tasarlanmistir. Sinav olusturma ve soru bankasi islemleri web arayuzunden yapilmalidir.

**S: Sifremi unuttum, ne yapmaliyim?**
C: Okul yoneticinize veya IT sorumlunuza basvurun. Hesabiniz icin yeni gecici sifre olusturulabilir.

---

**SmartCampus AI** - Turkiye'nin en modern egitim yonetim platformu

*Bu kilavuz SmartCampus AI v2.0 icin hazirlanmistir. Sistem guncellendikce kilavuz da guncellenecektir.*
