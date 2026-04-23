# SmartCampus AI - Yonetici Kullanim Kilavuzu

**Versiyon:** 2.0  
**Son Guncelleme:** Nisan 2026  
**Hedef Kitle:** Okul muduru, mudur yardimcisi, genel mudur, kurum yoneticileri

---

## Icindekiler

1. [Yonetici Paneline Giris](#1-yonetici-paneline-giris)
2. [Gunluk Isler](#2-gunluk-isler)
3. [Kurum Yonetimi](#3-kurum-yonetimi)
4. [Iletisim ve Randevu](#4-iletisim-ve-randevu)
5. [Akademik Izleme](#5-akademik-izleme)
6. [Operasyon Yonetimi](#6-operasyon-yonetimi)
7. [Raporlar ve Ciktilar](#7-raporlar-ve-ciktilar)
8. [Mobil Uygulama](#8-mobil-uygulama)

---

## 1. Yonetici Paneline Giris

### 1.1 Sisteme Erisim

SmartCampus AI web tarayiciniz uzerinden calisir. Herhangi bir kurulum gerekmez.

| Bilgi           | Deger                        |
|-----------------|------------------------------|
| URL             | http://localhost:8501        |
| Kullanici Adi   | `admin`                      |
| Sifre           | `SmartCampus123`             |
| Rol             | Yonetici                     |

> **ONEMLI:** Ilk giriste sistem sizden sifre degistirmenizi isteyecektir.
> Guclu bir sifre belirleyin (en az 8 karakter, harf + rakam).

### 1.2 Giris Adimlari

1. Tarayicinizda sistem adresini acin.
2. Kullanici adi ve sifrenizi girin.
3. **Giris Yap** butonuna basin.
4. Basarili giris sonrasinda Ana Sayfa goruntulenecektir.

### 1.3 Sidebar Navigasyonu

Giris yaptiktan sonra sol tarafta (sidebar) modul gruplari gorunur. Yonetici rolu **tum modullere** erisim hakkina sahiptir. Gruplar:

| Grup                  | Icerik                                                      |
|-----------------------|-------------------------------------------------------------|
| **GENEL**             | Ana Sayfa, Yonetim Tek Ekran, Analitik Dashboard            |
| **KURUM YONETIMI**    | Kurumsal Org., IK, Kayit, Butce Gelir Gider, Sosyal Medya, Kurum Hizmetleri |
| **ILETISIM & RANDEVU**| Veli-Ogretmen Gorusme, Randevu ve Ziyaretci, Toplanti ve Kurullar |
| **AKADEMIK**          | Akademik Takip, Olcme Degerlendirme, Zeka Merkezi, Rehberlik vb. |
| **DIJITAL OGRENME**   | AI Ogrenme Platformu, Yabanci Dil, AI Treni, STEAM Merkezi  |
| **OKUL YASAMI**       | Etkinlikler, Kutuphane, Saglik                               |
| **OPERASYON**         | Sivil Savunma, Mezunlar                                      |
| **SISTEM**            | AI Destek                                                    |

Herhangi bir modulu acmak icin sidebar'daki ilgili butona tiklayin.

### 1.4 Komut Paleti (Hizli Erisim)

Klavyeden **Ctrl+K** (Mac: Cmd+K) tusuna basarak komut paletini acabilirsiniz. Modul adini yazmaya baslayin, listeden secin ve dogrudan o module atlayin.

---

## 2. Gunluk Isler

Her gun sisteme giris yaptiginizda yapmaniz gereken kontroller:

### 2.1 Ana Sayfa Dashboard

Ana Sayfa, kurumunuzun gunluk ozetini sunar:

1. Sidebar'da **Ana Sayfa** butonuna tiklayin.
2. Ekranda su bilgileri goreceksiniz:
   - Toplam ogrenci, ogretmen ve personel sayilari
   - Bugunun yoklama durumu (devamsizlik orani)
   - Yaklasan sinav ve etkinlikler
   - Kritik bildirimler ve uyarilar
   - Odeme/tahsilat ozeti
3. Kartlara tiklayarak ilgili modullere hizlica gecebilirsiniz.

> **IPUCU:** Ana Sayfada gorunen metrik kartlari canli veri gosterir.
> Sayfa her yuklendiginde guncel degerler otomatik hesaplanir.

### 2.2 Yonetim Tek Ekran

Tum kurum verilerini tek sayfada gorun:

1. **GENEL > Yonetim Tek Ekran** butonuna tiklayin.
2. Bu ekranda su bolumler yer alir:
   - **Hizli Bakis:** Toplam kayit, devamsizlik, odeme durumu
   - **Gunluk Ozet:** Bugun islenen dersler, sinav sonuclari
   - **Personel Durumu:** Izinli/gorevde personel sayilari
   - **Kritik Uyarilar:** Geciken odemeler, devamsizlik alarmlari
3. Detay icin ilgili karti tiklayarak alt modullere gecin.

### 2.3 Analitik Dashboard

Trend analizleri ve karsilastirma grafikleri:

1. **GENEL > Analitik Dashboard** butonuna tiklayin.
2. Mevcut gorunum secenekleri:
   - **Sinif Bazli Performans:** Siniflarin not ortalamasi karsilastirmasi
   - **Devamsizlik Trendleri:** Haftalik/aylik devamsizlik grafikleri
   - **Sinav Analizi:** Ders bazli basari dagilimlari
   - **Odeme Durumu:** Tahsilat grafikleri
3. Filtre seceneklerini kullanarak donem, sinif veya ders bazinda daraltma yapabilirsiniz.

> **IPUCU:** Tum grafiklerde fare ile uzerine geldiginizde detay degerler gorunur.
> Grafikleri PNG olarak indirebilirsiniz (sag ust koseteki kamera ikonu).

---

## 3. Kurum Yonetimi

### 3.1 Kurumsal Organizasyon ve Iletisim

Okul profili, departman yapisi ve iletisim bilgilerinin yonetildigi modul.

**Modulu acmak icin:** KURUM YONETIMI > Kurumsal Organizasyon ve Iletisim

#### Kurum Profili

1. **Kurum Profili** sekmesine tiklayin.
2. Su bilgileri duzenleyebilirsiniz:
   - Okul adi, logo, slogan
   - Adres, telefon, e-posta, web sitesi
   - Mudurluk bilgileri
   - Kurum numarasi (MEB kodu)
3. Degisiklikleri **Kaydet** butonuyla onaylayin.

#### Departmanlar

1. **Departmanlar** sekmesine gecin.
2. Mevcut departmanlari goruntuleyebilir, yeni departman ekleyebilirsiniz.
3. Her departmana sorumlu kisi atayabilirsiniz.

#### Iletisim / Sinif Listeleri

1. **Iletisim** sekmesine gidin.
2. **Sinif Listeleri** alt sekmesinde ogrenci ve veli kayitlari yonetilir.
3. Bu ekran sistemdeki **merkezi ogrenci veri tabanidir** - diger tum moduller (Akademik Takip, Yoklama vb.) buradaki verileri kullanir.

> **ONEMLI:** Yeni ogrenci veya veli eklemek icin bu modulu kullanin.
> Ogrenci/veli verileri tek merkezden yonetilir.

### 3.2 Insan Kaynaklari Yonetimi (IK)

Personel islemlerinin tamamini bu modulden yonetirsiniz.

**Modulu acmak icin:** KURUM YONETIMI > Insan Kaynaklari Yonetimi

#### Personel Kayit

1. **Kadro Yonetimi** sekmesinden mevcut personeli goruntuleyebilirsiniz.
2. **Yeni Personel Ekle** butonuyla kayit formu acilir:
   - Ad, soyad, TC kimlik, dogum tarihi
   - Pozisyon (ogretmen, idari personel, destek personeli vb.)
   - Brans (ogretmenler icin)
   - Iletisim bilgileri (telefon, e-posta)
   - Istenme tarihi, sicil numarasi
3. Kaydettikten sonra personele otomatik olarak kullanici hesabi olusturulur.

#### Izin Yonetimi

1. **Izin Yonetimi** sekmesine gecin.
2. Personelden gelen izin taleplerini burada gorursunuz.
3. Her talep icin:
   - **Onayla** veya **Reddet** butonlarini kullanin.
   - Red durumunda gerekce yazin.
4. Onaylanan izinler otomatik olarak takvime islenir.

#### Mulakat

1. **Mulakat** sekmesinden aday mulakat sureclerini yonetin.
2. Yeni mulakat kaydi olusturun, tarih ve saat atayin.
3. Mulakat sonuclarini (puan, notlar) girin.

### 3.3 Kayit Modulu

Ogrenci aday kayit surecinin tamamini yoneten kapsamli modul.

**Modulu acmak icin:** KURUM YONETIMI > Kayit Modulu

Kayit Modulu 34 sekmeden olusur ve 6 ana gruba ayrilir:

| Grup            | Sekmeler                                                          |
|-----------------|-------------------------------------------------------------------|
| **Aday Yonetimi** | Aday listesi, basvuru formu, gorusme kaydi, kayit onay sureci   |
| **Pazarlama**   | Kampanya yonetimi, etkinlik planlama, sosyal medya entegrasyonu   |
| **Otomasyon**   | Otomatik mesaj sablonlari, hatirlatici kuyrugu, toplu SMS/e-posta |
| **Analiz**      | Donusum hunisi, kaynak analizi, kampanya ROI, trend raporlari     |
| **Operasyon**   | Tur planlama, soz yonetimi, evrak takibi                         |
| **Premium**     | AI muzakere, akilli fiyatlandirma, tahmin modeli                  |

#### Temel Islemler

1. **Yeni Aday Kaydi:** Aday Yonetimi grubundan "Yeni Aday" butonunu tiklayin, formu doldurun.
2. **Pipeline Takibi:** Adaylarin hangi asamada oldugunu (basvuru, gorusme, kayit, kesinlesme) goruntuleyebilirsiniz.
3. **Kampanya Olusturma:** Pazarlama grubundan yeni kampanya tanimlayabilir, QR kod ve etkinlik kayit linki uretebilirsiniz.
4. **Otomasyon:** Otomatik hatirlatma mesajlari ve takip aksiyonlari tanimlayabilirsiniz.

### 3.4 Butce Gelir Gider

Kurumun mali takibini yapin.

**Modulu acmak icin:** KURUM YONETIMI > Butce Gelir Gider

1. **Gelir Kaydi:** Ogrenim ucreti, burs, disindan gelirler
2. **Gider Kaydi:** Personel maaslari, faturalar, malzeme alimlari
3. **Butce Plani:** Yillik/aylik butce hedefleri tanimlama
4. **Raporlar:** Gelir-gider karsilastirmasi, butce sapma analizi

#### Yeni Kayit Ekleme

1. **Gelir Ekle** veya **Gider Ekle** butonuna tiklayin.
2. Kategori, tutar, tarih ve aciklama girin.
3. **Kaydet** butonuyla onaylayin.
4. Tum kayitlar otomatik olarak grafiklere ve raporlara yansir.

### 3.5 Odeme Takip

Ogrenci ucretleri ve taksit yonetimi.

**Erisim:** KURUM YONETIMI > Butce Gelir Gider > **Odeme Takip** sekmesi

> **Not:** Odeme Takip artik ayri bir sidebar modulu degil, Butce Gelir Gider modulunun bir sekmesidir.

#### Taksit Plani Olusturma

1. **Taksit Planlari** sekmesine gidin.
2. Ogrenci veya sinif secin.
3. Toplam tutar, taksit sayisi ve baslangic tarihini belirleyin.
4. **Plan Olustur** butonuna basin.
5. Sistem otomatik olarak odeme takvimini olusturur.

#### Odeme Alma

1. **Odeme Girisi** sekmesinden ogrenci secin.
2. Odenecek taksiti isareyleyin.
3. Odeme yontemi (nakit, havale, kredi karti) secin.
4. **Odeme Al** butonuyla kaydedin.
5. Makbuz otomatik olusturulur.

#### Geciken Odemeler

1. **Geciken Odemeler** sekmesinde vadesi gecmis taksitler listelenir.
2. Gecikme gun sayisi, faiz tutari ve toplam borc goruntulenir.
3. Veliye hatirlatma mesaji gonderebilirsiniz (SMS/bildirim).

#### Raporlar

- Aylik tahsilat raporu
- Ogrenci bazli borc durumu
- Gecikme analizi
- CSV/PDF export secenekleri

---

## 4. Iletisim ve Randevu

### 4.1 Veli-Ogretmen Gorusme

Veli gorusme taleplerini yonetin.

**Modulu acmak icin:** ILETISIM & RANDEVU > Veli-Ogretmen Gorusme

1. Velilerden gelen gorusme taleplerini goruntuleyebilirsiniz.
2. Her talep icin:
   - **Onayla:** Gorusme tarih ve saatini belirleyin.
   - **Reddet:** Gerekce yazarak reddedin.
   - **Ertele:** Farkli bir tarih onerin.
3. Onaylanan gorusmeler hem veliye hem ogretmene bildirim olarak iletilir.
4. Gorusme sonrasi notlari sisteme girebilirsiniz.

### 4.2 Randevu ve Ziyaretci

Dis ziyaretci kaydi ve randevu yonetimi.

**Modulu acmak icin:** ILETISIM & RANDEVU > Randevu ve Ziyaretci

| Sekme             | Islem                                               |
|--------------------|-----------------------------------------------------|
| Dashboard          | Gunluk ziyaretci ozeti, bekleyen randevular         |
| Randevu Yonetimi   | Yeni randevu olusturma, takvim gorunumu             |
| Ziyaretci Giris    | Gelen ziyaretcinin kaydini acma, ziyaret baslangici |
| Ziyaretci Cikis    | Ziyaretcinin cikis kaydini olusturma                |
| Ziyaretci Rehberi  | Gorusulecek kisiler ve unvanlar (IK'dan cekilir)    |
| Raporlar           | Ziyaretci istatistikleri, siklik analizi             |
| Ayarlar            | Gorusulecek unvan listesi, varsayilan sureler        |

#### Yeni Randevu Olusturma

1. **Randevu Yonetimi** sekmesine gidin.
2. **Yeni Randevu** butonuna tiklayin.
3. Ziyaretci adi, gorusulecek kisi, tarih/saat ve konu girin.
4. **Kaydet** butonuna basin.

### 4.3 Toplanti ve Kurullar

Ogretmenler kurulu, zumre toplantilari ve diger kurumsal toplantilar.

**Modulu acmak icin:** ILETISIM & RANDEVU > Toplanti ve Kurullar

1. **Yeni Toplanti Olustur:** Toplanti turu secin (Ogretmenler Kurulu, Zumre, Disiplin vb.).
2. Tarih, saat, yer ve katilimci listesini belirleyin.
3. Gundem maddelerini ekleyin.
4. Toplanti sonrasi **tutanak** olusturup kaydedebilirsiniz.
5. Tum katilimcilara bildirim gonderilebilir.

---

## 5. Akademik Izleme

### 5.1 Akademik Takip

Sinif performansini izlemek icin en kapsamli modul.

**Modulu acmak icin:** AKADEMIK > Akademik Takip

Akademik Takip 5 ana grup ve cok sayida alt sekmeden olusur:

| Grup                  | Alt Sekmeler                                              |
|-----------------------|-----------------------------------------------------------|
| Kadro & Ogrenci       | Akademik Kadro, Sinif Listesi, Ogrenci Yonetimi, Ogretmen Detay |
| Ders & Program        | Ders Programi (5 alt sekme), Zaman Cizelgesi              |
| Ogretim & Planlama    | Akademik Planlama, Uygulama Takibi, Ders Defteri, Odev Takip |
| Yoklama & Notlar      | Yoklama & Devamsizlik (7 alt sekme), Not Girisi           |
| Raporlar              | Karne, siralama, devamsizlik analizi, ders analizi        |

#### Sinif Performans Izleme

1. **Raporlar** grubuna gidin.
2. Sinif ve donem secin.
3. Not ortalamasi, basari siralamasi ve devamsizlik oranlarini gorun.
4. Grafikleri PDF olarak indirebilirsiniz.

#### Devamsizlik Kontrolu

1. **Yoklama & Notlar > Yoklama & Devamsizlik** sekmesine gidin.
2. Sinif bazli veya ogrenci bazli devamsizlik raporlarina erisin.
3. Kritik devamsizlik esigine yaklasan ogrenciler otomatik uyarilanir.

### 5.2 Analitik Dashboard ile Karsilastirma

1. **GENEL > Analitik Dashboard** acin.
2. **Sinif Karsilastirmasi** gorunumunu secin.
3. Ayni sinif duzeyindeki subelerin performansini yan yana gorun.
4. Ders bazli ayrinti icin ilgili dersi secin.

### 5.3 Erken Uyari Sistemi

Riskli ogrencileri tespit edin.

Erken Uyari Sistemi, Ogrenci Zeka Merkezi modulunun icinde yer alir:

1. **AKADEMIK > Ogrenci Zeka Merkezi** modulune gidin.
2. **Erken Uyari** sekmesini secin.
3. Sistem su kriterlere gore risk analizi yapar:
   - Not dususu trendi (son 3 sinav ortalamasinda dusus)
   - Devamsizlik artisi
   - Odev teslim orani dususu
   - Davranis puani degisimi
4. Risk seviyeleri: **YUKSEK** (kirmizi), **ORTA** (sari), **DUSUK** (yesil)
5. Yuksek riskli ogrenciler icin aksiyon plani olusturabilirsiniz.

> **IPUCU:** Erken Uyari verilerini haftalik olarak kontrol edin.
> Riskli ogrenciler icin rehberlik servisi ile koordinasyon saglayin.

---

## 6. Operasyon Yonetimi

### 6.1 Servis GPS Takip

Okul servislerinin guzergah ve zaman yonetimi.

**Erisim:** KURUM YONETIMI > Kurum Hizmetleri > **Servis** sekmesi

> **Not:** Servis GPS Takip artik ayri bir sidebar modulu degil, Kurum Hizmetleri modulunun bir sekmesidir.

1. **Guzergah Yonetimi:** Mevcut servis guzergahlarini goruntuleyebilir, yeni guzergah ekleyebilirsiniz.
2. **Durak Tanimlari:** Her guzergahtaki duraklari sirasiyla ekleyin.
3. **Ogrenci Atama:** Hangi ogrencinin hangi servise/duraga atandigini yonetin.
4. **Sofor ve Rehber Atama:** Servis aracina personel atayin.
5. **Hareket Saatleri:** Kalkis ve varis saatlerini tanimlayabilirsiniz.

### 6.2 Yemek Tercihi ve Alerji

Ogrenci beslenme yonetimi.

**Erisim:** KURUM YONETIMI > Kurum Hizmetleri > **Yemek** sekmesi

> **Not:** Yemek Tercihi ve Alerji artik ayri bir sidebar modulu degil, Kurum Hizmetleri modulunun bir sekmesidir.

1. **Haftalik Menu:** Yemek menusunu girin veya guncelleyin.
2. **Alerji Kayitlari:** Ogrenci bazli alerji bilgilerini yonetin.
3. **Alerji Raporu:** Hangi yemekte hangi alerjene maruz kalabilecek ogrenciler listelenir.
4. **Diyet Tercihleri:** Ozel diyet gerektiren ogrencilerin takibi.

> **ONEMLI:** Alerji bilgilerini donem basinda mutlaka guncelleyin.
> Yeni ogrenci kayitlarinda alerji bilgisi zorunlu olarak sorulur.

### 6.3 Kutuphane

Okul kutuphanesi envanter ve odunc yonetimi.

**Modulu acmak icin:** OKUL YASAMI > Kutuphane

1. **Envanter:** Kitap, dergi ve diger materyallerin listesi.
2. **Yeni Materyal Ekle:** Barkod, ISBN, baslik, yazar, kategori bilgilerini girin.
3. **Odunc Verme:** Ogrenci veya personele materyal odunc verin (barkod okutarak hizli islem).
4. **Iade:** Odunc verilen materyallerin iade kaydini olusturun.
5. **Geciken Iadeler:** Suresi gecen odunc raporunu goruntuleyebilirsiniz.

### 6.4 Tesis ve Varlik Yonetimi

Okul binasi, ekipman ve demirbas takibi.

**Erisim:** Destek Hizmetleri > **Tesis & Varlik** sekmesi

> **Not:** Tesis ve Varlik Yonetimi artik ayri bir sidebar modulu degil, Destek Hizmetleri modulunun bir sekmesidir.

1. **Demirbas Kaydi:** Okul demirbaslarini (projektor, bilgisayar, mobilya) sisteme ekleyin.
2. **Tuketim Malzemeleri:** Kirtasiye, temizlik malzemesi gibi tuketim kalemlerinin stok takibi.
3. **Ariza Bildirimi:** Personel veya ogretmenlerden gelen ariza bildirimlerini yonetin.
4. **Bakim Planlama:** Periyodik bakim takvimi olusturun.
5. **Destek Hizmetleri:** Temizlik, guvenlik ve diger destek hizmetlerinin takibi.

### 6.5 Sivil Savunma ve IS Guvenligi

Acil durum planlari ve is guvenligi uyumlulugu.

**Modulu acmak icin:** OPERASYON > Sivil Savunma ve IS Guvenligi

1. **Acil Durum Planlari:** Deprem, yangin ve tahliye planlarini tanimlayabilirsiniz.
2. **Tatbikat Kayitlari:** Yapilan tatbikatlarin tarihi, katilim ve sonuclarini kaydedin.
3. **IS Guvenligi:** Risk degerlendirmeleri, ISG egitim kayitlari.
4. **Ilkyardim:** Ilkyardimci listesi ve sertifika takibi.

---

## 7. Raporlar ve Ciktilar

### 7.1 Sertifika Uretici

Ogrenci ve personel icin profesyonel sertifika/belge uretimi.

**Modulu acmak icin:** AKADEMIK > Sertifika Uretici

1. **Sablon Sec:** Hazir sertifika sablonlarindan birini secin (basari belgesi, katilim belgesi, tesekkur belgesi vb.).
2. **Alici Bilgileri:** Ogrenci veya personel secin (sinif/isim bazli arama).
3. **Icerik Duzenle:** Sertifika metnini ozellestirebilirsiniz.
4. **PDF Olustur:** **Indir** butonuyla PDF ciktisini alin.
5. **Toplu Uretim:** Birden fazla ogrenci icin ayni anda sertifika uretebilirsiniz.

### 7.2 PDF Export

Bircok modulde PDF export ozelligi bulunur:

| Modul                    | Mevcut PDF Ciktilari                                |
|--------------------------|-----------------------------------------------------|
| Olcme ve Degerlendirme   | Sinav kagidi (OSYM formati), optik form, sonuc raporu |
| Akademik Takip           | Karne, devamsizlik raporu, sinif listesi            |
| Butce Gelir Gider > Odeme Takip | Makbuz, borc durumu                           |
| Ogrenci Zeka Merkezi     | Ogrenci 360 raporu                                   |
| Sertifika Uretici        | Basari belgesi, katilim belgesi                      |

PDF indirmek icin ilgili moduldeki **PDF Indir** veya **Rapor Olustur** butonunu kullanin.

### 7.3 CSV Download

Tablo gorunumundeki verileri CSV formatinda indirmek icin:

1. Ilgili moduldeki tablo gorunumune gidin.
2. Tablonun ust kismindaki **CSV Indir** veya **Excel'e Aktar** butonuna tiklayin.
3. Dosya otomatik olarak indirilecektir.

> **IPUCU:** CSV dosyalarini Excel'de acarken karakter kodlamasi icin
> UTF-8 secenegini kullanmaniz Turkce karakterlerin dogru goruntulenmesini saglar.

---

## 8. Mobil Uygulama

### 8.1 Genel Bilgi

SmartCampus AI mobil uygulamasi Flutter ile gelistirilmistir ve Android cihazlarda calismaktadir. Yonetici rolunde **21 sayfa** erisime aciktir.

### 8.2 Mobil Sayfalar (Yonetici Rolu)

| No | Sayfa                  | Aciklama                                          |
|----|------------------------|---------------------------------------------------|
| 1  | Ana Sayfa              | Gunluk ozet dashboard'u                           |
| 2  | Bugun Okulda           | Gunun canli ozeti, yoklama, etkinlik              |
| 3  | Gun Raporu             | Gunun detayli raporu                              |
| 4  | Butce                  | Gelir/gider ozeti                                 |
| 5  | Calisanlar             | Personel listesi ve durumu                        |
| 6  | Ders Programi          | Haftalik ders cizelgesi                           |
| 7  | Destek Hizmetleri      | Ariza ve destek talepleri                         |
| 8  | Erken Uyari            | Risk altindaki ogrenciler                         |
| 9  | Kayit Ozet             | Aday kayit pipeline'i                             |
| 10 | Kutuphane              | Odunc durumu ve envanter                          |
| 11 | Nobet                  | Ogretmen nobet programi                           |
| 12 | Onaylar                | Bekleyen onay talepleri                           |
| 13 | Randevular             | Randevu takvimi                                   |
| 14 | Revir                  | Saglik birimi kayitlari                           |
| 15 | Servis Hizmetleri      | Servis durumu                                     |
| 16 | Sinif Listeleri        | Sinif bazli ogrenci listesi                       |
| 17 | Sosyal Etkinlik        | Etkinlik ve kulup durumu                          |
| 18 | Toplanti ve Kurullar   | Yaklasan toplantilar                              |
| 19 | Tuketim ve Demirbas    | Stok ve demirbas durumu                           |
| 20 | Veli Talepleri         | Veli gelen talepleri                              |
| 21 | Zaman Cizelgesi        | Gunluk program akisi                              |

### 8.3 Mobil Uygulama Kurulumu

1. APK dosyasini okul yonetiminizden veya sistem yoneticinizden temin edin.
2. Android cihazinizda **Ayarlar > Guvenlik > Bilinmeyen Kaynaklara Izin Ver** secenegini acin.
3. APK dosyasini yukleyin ve kurun.
4. Uygulama acildiginda web sistemdeki ayni kullanici adi ve sifreyle giris yapin.

### 8.4 Mobil Kullanim Ipuclari

- Mobil uygulama internet baglantisi gerektirir (cevrimdisi mod yoktur).
- Bildirimler anlık olarak cekilir; push notification sistemi aktiftir.
- Yonetim onaylari (izin, randevu) mobil uzerinden de verilebilir.
- Dashboard grafikleri mobil ekrana uyumlu olarak yeniden boyutlandirilir.

---

## Ek Bilgiler

### Sik Sorulan Sorular

**S: Sifirdan yeni ogretmen hesabi nasil olustururum?**
C: IK Modulunden personel kaydi olusturdugunuzda, sistem otomatik olarak kullanici hesabi uretir. Kullanici adi ve gecici sifre IK ekraninda goruntulenir.

**S: Bir modulu belirli bir ogretmene kapatabilir miyim?**
C: Evet. SISTEM > AI Destek icerisinden veya dogrudan kullanici yonetimi uzerinden, ilgili kullanicinin "Izinli Moduller" listesini duzenleyebilirsiniz.

**S: Yedekleme nasil yapilir?**
C: Sistem her gun otomatik yedekleme yapar (son 30 yedek saklanir). Manuel yedekleme icin sistem yoneticinize basvurun.

**S: Birden fazla kurum (multi-tenant) yonetebilir miyim?**
C: Evet. SuperAdmin hesabiyla tum kurumlari yonetebilirsiniz. Her kurum izole veri alaninda calisir.

### Klavye Kisayollari

| Kisayol     | Islem                              |
|-------------|------------------------------------|
| Ctrl+K      | Komut paleti (hizli modul arama)   |
| Ctrl+Enter  | Form gonderme (bazi ekranlarda)    |

### Destek

Teknik sorun yasadiginizda:

1. Oncelikle **SISTEM > AI Destek** modulunu deneyin; AI asistan genel sorulara yanit verebilir.
2. Cozum bulunamazsa sistem yoneticinize (IT) basvurun.
3. Hata mesajinin ekran goruntusunu almak sorun cozumunu hizlandirir.

---

**SmartCampus AI** - Turkiye'nin en modern egitim yonetim platformu

*Bu kilavuz SmartCampus AI v2.0 icin hazirlanmistir. Sistem guncellendikce kilavuz da guncellenecektir.*
