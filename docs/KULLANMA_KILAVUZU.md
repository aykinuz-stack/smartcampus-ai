# SmartCampusAI - Kullanma Kilavuzu

> **Surum:** 1.0 | **Tarih:** Nisan 2026
> **Platform:** Web (Streamlit) + Mobil (Flutter APK)

---

## Icerik Tablosu

1. [Giris](#1-giris)
2. [Giris Yapma](#2-giris-yapma)
3. [Genel Arayuz](#3-genel-arayuz)
4. [Modul Rehberi](#4-modul-rehberi)
5. [Mobil Uygulama](#5-mobil-uygulama)
6. [Sik Sorulan Sorular (SSS)](#6-sik-sorulan-sorular-sss)
7. [Sorun Giderme](#7-sorun-giderme)
8. [Iletisim ve Destek](#8-iletisim-ve-destek)

---

## 1. Giris

### 1.1 SmartCampusAI Nedir?

SmartCampusAI, Turk ozel okullari icin gelistirilmis **yapay zeka destekli egitim yonetim platformu**dur. Akademik takipten olcme degerlendirmeye, insan kaynaklarindan butce yonetimine, veli iletisiminden servis takibine kadar bir egitim kurumunun tum sureclerini tek catida birlestiren kapsamli bir cozumdur.

**Temel ozellikler:**

- 8 ana grup altinda **30 modul** ile tam kapsamli okul yonetimi
- **Yapay zeka destekli** soru uretimi, ogrenme analitigi ve akilli asistan
- **Multi-tenant** yapi: Birden fazla okul/kampus ayni altyapida bagimsiz calisabilir
- **Rol bazli erisim:** Yonetici, ogretmen, veli, ogrenci ve rehber rolleri
- **Web + Mobil:** Masaustunden tam yonetim, mobil cihazdan hizli erisim
- **Ultra Premium Diamond** tasarim dili: Gold ve navy renk paleti, profesyonel arayuz

### 1.2 Kimler Kullanir?

| Rol | Tipik Kullanicilar | Temel Erisim Alanlari |
|-----|--------------------|-----------------------|
| **Yonetici** | Okul muduru, mudur yardimcisi, genel mudur | Tum moduller, tum veriler |
| **Ogretmen** | Brans ogretmenleri, sinif ogretmenleri | Akademik takip, olcme degerlendirme, ders programi, odev |
| **Veli** | Anne/baba, vasi | Ogrenci bilgileri, not/devamsizlik, yemek, servis, mesajlasma |
| **Ogrenci** | Ilkokul-lise ogrencileri | Online sinav, odev teslimi, dijital ogrenme, AI treni |
| **Rehber** | Psikolojik danisman, rehber ogretmen | Rehberlik modulu, davranissal risk, gorusme kayitlari |

### 1.3 Nasil Erisim Saglanir?

**Web Uygulamasi (Tam Ozellik):**
```
http://localhost:8501
```
Tarayicinizdan (Chrome, Firefox, Edge, Safari) yukaridaki adrese giderek platform arayuzune ulasabilirsiniz. Sunucu farkli bir makinede kuruluysa `localhost` yerine sunucu IP adresini kullanin.

**Mobil Uygulama (APK):**

Flutter tabanli mobil uygulama, Android cihazlarda APK olarak kurulur. Mobil uygulama REST API (FastAPI) uzerinden web ile ayni veri tabanini paylasir. Detaylar icin [Bolum 5: Mobil Uygulama](#5-mobil-uygulama) kismina bakin.

---

## 2. Giris Yapma

### 2.1 Web Uygulamasinda Giris

1. Tarayicinizda `http://localhost:8501` adresini acin.
2. Sol taraftaki **sidebar**'da giris formu gorunecektir.
3. **Kullanici adi** ve **sifre** alanlarini doldurun.
4. **Giris Yap** butonuna basin.
5. Dogrulama basarili olursa sidebar'da modul menusu gorunur.

> **Not:** Ilk kurulumda sistem yoneticisi tarafindan varsayilan hesaplar olusturulur. Guvenlik icin ilk giristen sonra sifrenizi mutlaka degistirin.

### 2.2 Mobil Uygulamada Giris

1. APK'yi yukleyip uygulamayi acin.
2. Giris ekraninda **kullanici adi** ve **sifre** girin.
3. **Giris Yap** butonuna dokunun.
4. Basarili giristen sonra rolunuze uygun ana ekrana yonlendirilirsiniz.

### 2.3 Kullanici Rolleri ve Yetkileri

SmartCampusAI, **Rol Bazli Erisim Kontrolu (RBAC)** kullanir. Her kullanici bir role atanir ve yalnizca o role tanimli modullere erisebilir.

| Rol | Erisim Seviyesi | Ozel Yetkiler |
|-----|-----------------|---------------|
| **SuperAdmin** | Tum sistem | Kullanici yonetimi, tenant ayarlari, sistem yapilandirmasi |
| **Yonetici** | Tum moduller | Personel yonetimi, butce, raporlar, onay islemleri |
| **Ogretmen** | Akademik moduller | Not girisi, devamsizlik, sinav olusturma, odev verme |
| **Calisan** | Atanan moduller | Gorev bazli erisim (idari, destek, vb.) |
| **Ogrenci** | Ogrenci modulleri | Online sinav, odev teslimi, dijital ogrenme |
| **Veli** | Veli modulleri | Cocuk bilgileri (salt okunur), mesajlasma, randevu |

### 2.4 Sifre Guvenligi

- Sifreler **bcrypt** ile hash'lenerek saklanir.
- Legacy SHA-256 hash'ler otomatik olarak bcrypt'e guncellenir.
- Uretim ortaminda sifrelerin ortam degiskenleri ile ayarlanmasi zorunludur.
- Sifre degistirmek icin profil alaninda **Sifre Degistir** sekmesini kullanin.

---

## 3. Genel Arayuz

### 3.1 Ana Ekran Yapisi

SmartCampusAI arayuzu uc ana bolumden olusur:

```
+-------------------+---------------------------------------+
|                   |                                       |
|   SIDEBAR         |        ANA ICERIK ALANI               |
|   (Sol Menu)      |        (Secili modul burada           |
|                   |         goruntulenur)                  |
|   - Kullanici     |                                       |
|     bilgisi       |                                       |
|   - Modul grubu   |                                       |
|     basliklari    |                                       |
|   - Modul         |                                       |
|     butonlari     |                                       |
|   - Tema          |                                       |
|     degistirme    |                                       |
|                   |                                       |
+-------------------+---------------------------------------+
```

### 3.2 Sidebar Menu Yapisi

Sidebar'da moduller **8 grup** halinde duzenlenmistir. Her grubun basligi buyuk harfle ve vurgu rengiyle gosterilir:

| # | Grup Adi | Modul Sayisi |
|---|----------|--------------|
| 1 | GENEL | 3 |
| 2 | KURUM YONETIMI | 6 |
| 3 | ILETISIM & RANDEVU | 3 |
| 4 | AKADEMIK | 7 |
| 5 | DIJITAL OGRENME | 5 |
| 6 | OKUL YASAMI | 3 |
| 7 | OPERASYON | 2 |
| 8 | SISTEM | 1 |
| | **Toplam** | **30** |

Bir modulu acmak icin sidebar'daki ilgili butona tiklamaniz yeterlidir. Aktif modul, sol kenarinda vurgu cizgisi ve koyu arka planla belirginlestirilir.

### 3.3 Tema ve Gorunum

SmartCampusAI varsayilan olarak **koyu (dark) tema** ile gelir:

- **Arka plan:** Koyu lacivert (#0B0F19)
- **Yuzey rengi:** Derin lacivert (#131825)
- **Ana vurgu:** Indigo (#6366F1)
- **Metin:** Acik gri (#E2E8F0)
- **Gold aksan:** Diamond gold (#D4AF37)

Tema ayarlari `.streamlit/config.toml` dosyasindan yonetilir.

### 3.4 Sekmeler ve Alt Navigasyon

Cogu modul ic iceriklerini **sekmeler (tabs)** ile organize eder. Sekmeler ana icerik alaninin ustunde yatay olarak siralanir. Bazi modullerde ic ice sekmeler de bulunur.

**Ornek — Akademik Takip modulu:**
```
Kadro & Ogrenci | Ders & Program | Ogretim & Planlama | Yoklama & Notlar | Raporlar
```

### 3.5 QR Kod ile Hizli Erisim

SmartCampusAI bazi islemler icin QR kod destegi sunar:

- **Online sinav girisi:** QR taratarak dogrudan sinava katilim
- **Etkinlik kayit (RSVP):** QR ile etkinlige kayit
- **Tur rezervasyonu:** Okul turu icin QR ile form doldurma
- **AI muzakere:** Kayit surecinde AI destekli gorusme

Bu QR kodlar login gerektirmeden dogrudan ilgili forma yonlendirir.

---

## 4. Modul Rehberi

### 4.1 GENEL

#### Ana Sayfa (Dashboard)

Sisteme giris yaptiginizda karsiniza cikan ilk ekrandir. Rolunuze gore ozellesmis ozet bilgiler, istatistikler ve hizli erisim kartlari sunar.

- **Yoneticiler icin:** Toplam ogrenci, ogretmen, bugunun devamsizligi, yaklasan sinavlar
- **Ogretmenler icin:** Bugunku dersler, bekleyen odevler, yaklasan sinav tarihleri
- **Veliler icin:** Cocugun devamsizlik durumu, son notlar, yaklasan etkinlikler

#### Yonetim Tek Ekran

Okul yoneticilerine ozel **tek bakista tum okul** gorunumu. Ogrenci sayilari, ogretmen dagilimi, akademik performans ozeti, devamsizlik oranlari ve kritik uyarilar tek bir ekranda sunulur.

#### Analitik Dashboard

Veri odakli grafikler ve interaktif tablolar ile derinlemesine analiz imkani saglar. Plotly tabanli grafiklerle trend analizi, karsilastirma ve raporlama yapabilirsiniz.

---

### 4.2 KURUM YONETIMI

#### Kurumsal Organizasyon ve Iletisim

Okul/kurum bilgilerinin yonetildigi ana moduldul:

- **Kurum Profili:** Okul adi, adres, logo, iletisim bilgileri
- **Sinif Listeleri:** Ogrenci ve veli verilerinin merkezi kaynak noktasi
- **Iletisim dizinleri:** Personel, veli ve ogrenci iletisim bilgileri
- **Duyurular:** Kurum geneli duyuru yonetimi

> **Onemli:** Ogrenci ve veli verileri bu modulde yonetilir. Diger moduller bu veriyi referans olarak kullanir.

#### Insan Kaynaklari Yonetimi

Personel ve kadro yonetimi:

- Calisanlar (yonetim, akademik, idari, destek)
- Pozisyon tanimlari ve gorev atamalari
- Izin takibi ve nobet kayitlari
- Performans degerlendirme
- Belge yonetimi

#### Kayit Modulu

Ogrenci kayit surecinin A'dan Z'ye yonetimi:

- Yeni ogrenci kaydi ve belge toplama
- Kayit durumu takibi (basvuru, kabul, tamamlandi)
- Tur rezervasyonu (QR destekli)
- AI destekli muzakere (veli ile fiyat gorusmesi)
- Diamond kalitesinde kayit raporlari

#### Butce Gelir Gider

Kurumun mali yonetimi:

- Gelir ve gider kalemleri
- Butce planlama ve takip
- Donem bazli karsilastirmalar
- Grafik ve tablo raporlari
- **Odeme Takip sekmesi:** Ogrenci aidat ve odeme sureci, taksit takibi, geciken odeme uyarilari, odeme makbuzu uretimi

> **Not:** Odeme Takip artik ayri bir modul degil, Butce Gelir Gider modulunun bir sekmesidir.

#### Sosyal Medya Yonetimi

Okulun dijital pazarlama ve sosyal medya icerik yonetimi:

- Icerik planlama takvimi
- Platform bazli icerik hazirlama
- Yayinlama durumu takibi

#### Kurum Hizmetleri

Okulun sundugu ek hizmetlerin yonetimi:

- Hizmet tanimlari ve fiyatlandirma
- Hizmet bazli raporlama
- **Yemek Tercihi ve Alerji sekmesi:** Haftalik/aylik menu planlama, ogrenci alerji bilgileri, ozel diyet gereksinimleri
- **Servis GPS Takip sekmesi:** Servis guzergah yonetimi, binis/inis kayitlari, veli bildirim sistemi

> **Not:** Yemek Tercihi ve Servis GPS Takip artik ayri moduller degil, Kurum Hizmetleri modulunun sekmeleridir.

---

### 4.3 ILETISIM & RANDEVU

#### Veli-Ogretmen Gorusme

Veliler ile ogretmenler arasindaki gorusme surecinin yonetimi:

- Gorusme talep olusturma ve onaylama
- Gorusme notlari ve takip
- AI destekli gorusme senaryolari (250+ hazir senaryo)
- WhatsApp entegrasyonu

#### Randevu ve Ziyaretci

Okula gelen ziyaretcilerin ve randevularin yonetimi:

- **Dashboard:** Bugunun randevu ve ziyaretci ozeti
- **Randevu Yonetimi:** Yeni randevu olusturma, onaylama, iptal
- **Ziyaretci Giris/Cikis:** Kimlik kaydi, ziyaret nedeni, giris/cikis saati
- **Ziyaretci Rehberi:** Gorusulecek kisi ve unvan secimi (IK verileriyle entegre)
- **Raporlar:** Ziyaretci istatistikleri ve analizleri
- **Ayarlar:** Modul yapilandirmasi

#### Toplanti ve Kurullar

Okul ici toplanti ve kurul yonetimi:

- Toplanti planlama ve gundemi hazirlama
- Katilimci listesi ve davet gondermesi
- Karar tutanaklari
- Toplanti takvimi

---

### 4.4 AKADEMIK

#### Akademik Takip

Ogrenci akademik surecinin tam yonetimi. **5 ana grup** ve alt sekmelerden olusur:

**1. Kadro & Ogrenci:**
- Akademik Kadro: Ogretmen listesi ve brans bilgileri
- Sinif Listesi: Sinif bazli ogrenci listeleri
- Ogrenci Yonetimi: Detayli ogrenci bilgileri
- Ogretmen Detay: Ogretmen bazli ders ve sinif bilgileri

**2. Ders & Program:**
- Ders Programi (5 alt sekme): Haftalik program gorunumu, cizelge
- Zaman Cizelgesi: Gunluk zaman dilimleri (ders/teneffus/ogle/etut)

**3. Ogretim & Planlama:**
- Akademik Planlama: Yillik/aylik/haftalik plan hazirlama
- Uygulama Takibi: Kazanim islenme durumu
- Ders Defteri: Gunluk ders notlari
- Odev Takip: Odev verme ve teslim durumu

**4. Yoklama & Notlar:**
- Yoklama & Devamsizlik (7 alt sekme): Gunluk yoklama, devamsizlik raporlari
- Not Girisi: Yazili, sozlu, proje, performans notlari

**5. Raporlar:**
- Karne, siralama, devamsizlik ve ders analizi raporlari

#### Olcme ve Degerlendirme

Sinav ve soru bankasi yonetiminin merkezi:

- **Kazanim Yonetimi:** MEB yillik plan kayitlarindan (6839 kayit, 14 ders, 1-12. sinif) otomatik kazanim secimi
- **Soru Bankasi:** Coktan secmeli, dogru/yanlis, bosluk doldurma, eslestirme, siralama, cloze, matematik ifade turleri
- **AI Soru Uretimi:** OpenAI GPT-4o-mini ile kazanim bazli otomatik soru uretimi
- **Sinav Olusturma:** Blueprint/sablon sistemi, LGS/TYT/AYT tarzi bolum yapilari
- **Online Sinav:** Ogrenci girisi, tab guvenlik, heartbeat takibi, QR ile giris
- **Otomatik Puanlama:** Negatif puanlama, rubrik bazli degerlendirme
- **PDF Export:** OSYM tarzi 2 sutunlu profesyonel sinav, optik form, kisisel optik form
- **Telafi Sistemi:** Renk bandli (RED/YELLOW/GREEN/BLUE) otomatik telafi gorevleri
- **Psikometrik Analiz:** IRT modelleri (1-PL, 2-PL, 3-PL), madde analizi
- **Adaptif Test:** ELO tabanli zorluk kalibrasyonu, CAT motoru
- **Stok Kontrol:** Soru bankasini otomatik doldurma ve kalite kontrol
- **QTI Export/Import:** IMS QTI 2.1 standardi ile dis sistemlerle entegrasyon

#### Ogrenci Zeka Merkezi

Ogrencinin bilissel profili ve coklu zeka analizi:

- Zeka turu tespiti ve guclendirme onerileri
- Ogrenme stili analizi
- Kisisellestirilmis gelisim planlari

#### Okul Oncesi - Ilkokul

Okul oncesi ve ilkokul seviyesine ozel moduller:

- Gelisim raporlari (fiziksel, bilissel, sosyal, duygusal)
- Anasinifindan 4. sinifa kadar mufredat takibi
- Oyun bazli ogrenme kayitlari

#### Rehberlik

Rehber ogretmenler icin psikolojik danismanlik ve yonlendirme:

- Ogrenci gorusme kayitlari
- Davranissal risk degerlendirme
- Cerceve planlari
- Psikolojik test ve envanter sonuclari
- Mesleki yonlendirme

#### Sertifika Uretici

Cesitli etkinlik ve basarilar icin profesyonel sertifika uretimi:

- Hazir sertifika sablonlari
- PDF olarak sertifika olusturma ve indirme
- Toplu sertifika uretimi

#### Egitim Koclugu

Ogretmen ve yonetici gelisimi icin kocluk modulu:

- Kocluk oturumu planlama ve takip
- Geri bildirim kayitlari
- Gelisim hedefleri belirleme

---

### 4.5 DIJITAL OGRENME

#### AI Ogrenme Platformu

Yapay zeka destekli kisisellestirilmis ogrenme deneyimi:

- Ogrenci seviyesine uyarlanmis icerik onerileri
- Interaktif ders materyalleri
- Ogrenme analitigi ve ilerleme takibi

#### Yabanci Dil

Yabanci dil ogretimi icin ozel modul:

- CEFR seviyelendirme sinavlari (A1-C2)
- Kelime bankasi ve alisitiirmalar
- Dinleme ve konusma pratiigi

#### Kisisel Dil Gelisimi

Her ogrencinin dil yetkinligini olcen ve gelistiren modul:

- Okuma, yazma, dinleme, konusma becerileri takibi
- Bireysel gelisim planlari

#### AI Treni

Oyunlastirma ile ogrenme motivasyonunu artiran modul:

- Konu bazli sorularla ilerleyen tren metaforu
- Basari rozetleri ve skor tablosu
- Tamamen gomulu — backend gerektirmez

#### STEAM Merkezi

Bilim, Teknoloji, Muhendislik, Sanat ve Matematik projeleri:

- Proje planlama ve takip
- Deney gunlukleri
- Sergi ve yarisma kayitlari

---

### 4.6 OKUL YASAMI

#### Sosyal Etkinlik ve Kulupler

Okul etkinlikleri ve ogrenci kuluplerininn yonetimi:

- Etkinlik olusturma ve takvim
- Kulup uyelik kayitlari
- QR ile etkinlik katilim (RSVP)
- Etkinlik duyurulari

#### Kutuphane

Okul kutuphanesi yonetimi:

- Kitap envanteri ve kataloglama
- Odunc verme/alma takibi
- Ogrenci okuma listeleri
- Barcode/QR ile kitap islemleri

#### Okul Sagligi Takip

Ogrenci saglik bilgilerinin yonetimi:

- Saglik gecmisi ve kronik durumlar
- Alerji kayitlari
- Revir kayitlari
- Asi takibi

> **Not:** Yemek Tercihi ve Alerji ile Servis GPS Takip artik KURUM YONETIMI > Kurum Hizmetleri modulunun sekmeleridir.

---

### 4.7 OPERASYON

#### Sivil Savunma ve IS Guvenligi

Acil durum planlama ve is guvenligi:

- Tahliye planlari
- Tatbikat kayitlari
- IS guvenligi denetimleri
- Acil durum iletisim zincirleri

#### Mezunlar ve Kariyer Yonetimi

Mezun takibi ve kariyer yonlendirme:

- Mezun veri tabani
- Universite ve kariyer takibi
- Mezun etkinlikleri
- Mentorluk programlari

> **Not:** Tesis ve Varlik Yonetimi artik ayri bir modul degil, Destek Hizmetleri > Tesis & Varlik sekmesi olarak erisime aciktir.

---

### 4.8 SISTEM

#### AI Destek

SmartCampusAI'nin gomulu yapay zeka asistani:

- Platform kullanimi hakkinda sorulari yanitlar
- Modul yonlendirmesi yapar
- Sik karsilasilan sorunlara cozum onerir

---

## 5. Mobil Uygulama

### 5.1 Genel Bilgi

SmartCampusAI mobil uygulamasi, Flutter frameworku ile gelistirilmistir. Android cihazlarda APK olarak kurulur. Mobil uygulama, FastAPI tabanli bir REST API uzerinden web uygulamasi ile **ayni veritabanini** paylasir.

### 5.2 APK Indirme ve Kurulum

1. Okul yonetiminden veya IT departmanindan APK dosyasini edinin.
2. Android cihazinizda **Ayarlar > Guvenlik > Bilinmeyen Kaynaklara Izin Ver** secenegini aktif edin.
3. APK dosyasini acin ve **Yukle** butonuna dokunun.
4. Kurulum tamamlandiginda uygulamayi acin.

### 5.3 Mobil Roller ve Erisim

Mobil uygulamada 5 temel rol desteklenir:

| Rol | Erisim Alanlari |
|-----|-----------------|
| **Yonetici** | Tum ogrenci/ogretmen verileri, raporlar, bildirim yonetimi |
| **Ogretmen** | Sinif listeleri, not girisi, yoklama, odev, mesajlasma |
| **Veli** | Cocuk bilgileri, not/devamsizlik, yemek, servis, mesajlasma |
| **Ogrenci** | Online sinav, odevler, dijital ogrenme, AI treni |
| **Rehber** | Gorusme kayitlari, ogrenci profili, risk uyarilari |

### 5.4 Mobil Uygulama Ozellikleri

- **Push Bildirimler:** Onemli duyurular ve uyarilar aninda cihaza ulasir
- **Mesajlasma:** Veli-ogretmen, ogrenci-ogretmen mesajlasma
- **Ruh Hali (Mood) Takibi:** Ogrenciler gunluk ruh halini kaydedebilir
- **Ihbar Sistemi:** Anonim bildirim ve geri bildirim
- **Quiz Koleksiyonu:** Mobil cihazdan hizli sinav ve quiz
- **Odeme Bilgileri:** Aidat durumu ve odeme gecmisi
- **Offline Destek:** Bazi temel bilgiler internet baglantisi olmadan da goruntulenir

### 5.5 Mobil Backend Baglantisi

Mobil uygulama `http://<sunucu-ip>:8000/api/v1` adresindeki REST API'ye baglanir. Baglanti ayarlari uygulama icinden yapilir. Ilk calistirmada sunucu adresi bir kez girilir.

---

## 6. Sik Sorulan Sorular (SSS)

### S1: Sisteme ilk kez nasil giris yapabilirim?
**C:** Okul IT yoneticiniz size bir kullanici adi ve gecici sifre verecektir. Bu bilgilerle giris yapin ve ardindan sifrenizi degistirin.

### S2: Sifremi unuttum, ne yapmaliyim?
**C:** Okul yoneticinize veya IT departmanina basvurun. Yonetici panelindan sifreniz sifirlanabilir. SuperAdmin veya Yonetici rolu bu islemi yapabilir.

### S3: Birden fazla cocugum var, hepsini ayni hesaptan gorebilir miyim?
**C:** Evet. Veli hesabiniz, ayni okuldaki tum cocuklarinizla iliskilendirilir. Giris yaptiktan sonra cocuklariniz arasinda gecis yapabilirsiniz.

### S4: Mobil uygulamada bildirim gelmiyor, ne yapmaliyim?
**C:** Telefonunuzun bildirim ayarlarindan SmartCampusAI uygulamasina bildirim izni verdiginizden emin olun. Ayrica pil tasarrufu modunun uygulamayi kisitlamadagini kontrol edin.

### S5: Verilerim guvenli mi?
**C:** SmartCampusAI tum sifreleri bcrypt ile sifreler. JWT tabanli oturum yonetimi kullanir. Veriler sunucunuzda yerel olarak saklanir; ucuncu taraf sunucularina gonderilmez (AI soru uretimi disinda).

### S6: AI soru uretimi icin internet baglantisi gerekli mi?
**C:** Evet. AI soru uretimi OpenAI API kullanir ve aktif bir internet baglantisi ile gecerli bir API anahtari gerektirir. Diger tum moduller internet gerektirmez.

### S7: Birden fazla okul ayni sistemde calisabilir mi?
**C:** Evet. SmartCampusAI multi-tenant yapiyi destekler. Her okul `data/tenants/<okul_adi>/` altinda kendi verisi ile bagimsiz calisir.

### S8: PDF sinav ciktilarinin kalitesi nasil?
**C:** SmartCampusAI, OSYM standartlarinda 2 sutunlu profesyonel sinav PDF'leri uretir. Gold cap cizgileri, diamond semboller, QR kodlar ve hizalama isaretleri ile kurumsal kalitede optik form destegi vardir.

### S9: Hangi sinav turleri destekleniyor?
**C:** Coktan secmeli (MCQ), dogru/yanlis, bosluk doldurma, eslestirme, siralama, cloze test ve matematik ifadesi turleri desteklenir. LGS, TYT ve AYT formatlarinda sinav olusturulabilir.

### S10: Yedekleme otomatik mi?
**C:** Evet. Sistem her gun otomatik yedekleme yapar ve son 30 yedegi saklar. Ek olarak manuel yedekleme de yapabilirsiniz. Yedekler `backups/` dizininde ZIP formatinda saklanir.

---

## 7. Sorun Giderme

### 7.1 Web Uygulamasi Acilmiyor

**Belirti:** Tarayicida `localhost:8501` acilmiyor veya "connection refused" hatasi veriyor.

**Cozum:**
1. Streamlit sunucusunun calistigini kontrol edin:
   ```bash
   # Terminal'de kontrol edin
   ps aux | grep streamlit
   ```
2. Sunucuyu yeniden baslatin:
   ```bash
   streamlit run app.py
   ```
3. Port 8501'in baska bir uygulama tarafindan kullanilmadigini kontrol edin.

### 7.2 Mobil Backend Baglantiisi Basarisiz

**Belirti:** Mobil uygulama "Baglanti hatasi" veya "Sunucu yanit vermiyor" uyarisi gosteriyor.

**Cozum:**
1. FastAPI backend'in calistigini kontrol edin:
   ```bash
   python -m uvicorn mobile.backend.main:app --host 0.0.0.0 --port 8000
   ```
2. Mobil cihazdaki sunucu IP adresinin dogru oldugundan emin olun.
3. Firewall ayarlarindan 8000 portunu acin.
4. Cihazin sunucu ile ayni aga bagli oldugundan emin olun.

### 7.3 Veriler Gorunmuyor veya Yuklenmiyor

**Belirti:** Modul aciliyor ama tablolar, listeler veya kartlar bos gorunuyor.

**Cozum:**
1. `data/` dizinindeki JSON dosyalarinin mevcut ve bos olmaadigini kontrol edin.
2. Dosya izinlerinin dogru ayarlandigini kontrol edin.
3. Tarayici cache'ini temizleyin (Ctrl+Shift+R).
4. Streamlit sunucusunu yeniden baslatin.

### 7.4 AI Soru Uretimi Calismiyyor

**Belirti:** "API hatasi" veya soru uretilemiyor mesaji.

**Cozum:**
1. `.env` dosyasinda `OPENAI_API_KEY` degerinin dogru ayarlandigini kontrol edin.
2. API anahtarinin aktif ve bakiyesinin yeterli oldugundan emin olun.
3. Internet baglantinizi kontrol edin.
4. OpenAI servis durumunu `status.openai.com` adresinden kontrol edin.

### 7.5 PDF Export Hatasi

**Belirti:** Sinav veya rapor PDF olarak indirilemiyyor.

**Cozum:**
1. `reportlab` ve `PyMuPDF` paketlerinin yuklu oldugundan emin olun:
   ```bash
   pip install reportlab PyMuPDF
   ```
2. Disk alaninin yeterli oldugundan emin olun.
3. Gecici dosyalar icin yazma iznini kontrol edin.

### 7.6 Giris Yapamiyorum

**Belirti:** Dogru bilgilerle bile giris basarili olmuyor.

**Cozum:**
1. Kullanici adi ve sifrenin dogru yazildigindan emin olun (buyuk/kucuk harf duyarli).
2. `data/users.json` dosyasinin mevcut ve gecerli JSON oldugunu kontrol edin.
3. Yoneticiden sifre sifirlama talep edin.
4. Gerekirse SuperAdmin hesabiyla giris yapin.

---

## 8. Iletisim ve Destek

### 8.1 Teknik Destek

SmartCampusAI ile ilgili teknik sorunlar, oneriler veya geri bildirimler icin:

- **E-posta:** destek@smartcampusai.com
- **Dokumantasyon:** `docs/` dizinindeki kilavuzlar
- **Sistem Icii Destek:** AI Destek modulu (sidebar > SISTEM > AI Destek)

### 8.2 Acil Durum

Sistem cokmes veya veri kaybi durumunda:

1. Hemen yedekleme durumunu kontrol edin (`backups/` dizini).
2. Mevcut en son yedegi guvenli bir konuma kopyalayin.
3. IT departmaniniza bildirin.

### 8.3 Geri Bildirim

Platform iyilestirme onerileri icin AI Destek modulundeki geri bildirim formunu kullanabilir veya dogrudan okul yonetiminize iletebilirsiniz.

---

> **SmartCampusAI** — Turkiye'nin en modern, kullanici dostu ve veri odakli egitim yonetim platformu.
>
> *"Dusunmeden akip giden deneyim: Hiz + Tutarlilik + Rol Bazli Netlik"*
