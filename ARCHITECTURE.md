# SmartCampus AI - Sistem Mimarisi Dokumantasyonu

> Son guncelleme: 2026-04-21 | Versiyon: 3.0

---

## Icerik

1. [Genel Bakis](#1-genel-bakis)
2. [Teknoloji Stack](#2-teknoloji-stack)
3. [Dizin Yapisi](#3-dizin-yapisi)
4. [Modul Listesi (34 Modul)](#4-modul-listesi-34-modul)
5. [Mobil Uygulama Mimarisi](#5-mobil-uygulama-mimarisi)
6. [Backend API Yapisi](#6-backend-api-yapisi)
7. [Veri Modeli](#7-veri-modeli)
8. [Guvenlik](#8-guvenlik)
9. [CI/CD](#9-cicd)
10. [Kurulum ve Calistirma](#10-kurulum-ve-calistirma)

---

## 1. Genel Bakis

**SmartCampus AI**, Turk ozel okullari icin gelistirilmis, uctan uca egitim yonetim
platformudur. Sistem uc ana bilesenden olusur:

| Bilesen           | Teknoloji       | Aciklama                                       |
|-------------------|-----------------|-------------------------------------------------|
| Web Uygulamasi    | Streamlit       | 34 modul, 291 Python view dosyasi               |
| Mobil Uygulama    | Flutter (Dart)  | 99 Dart dosyasi, 5 rol, 78 sayfa                |
| Mobil Backend     | FastAPI          | 138 route, 13 router, JWT kimlik dogrulama       |

Temel prensipler:
- **Multi-tenant mimari**: Her okul kendi veri alaninda calisir (`data/tenants/`)
- **Tek veri kaynagi**: Streamlit ve FastAPI ayni JSON dosyalarini paylasir
- **Rol tabanli erisim (RBAC)**: SuperAdmin, Yonetici, Ogretmen, Calisan, Ogrenci, Veli
- **Dark tema + Gold aksan**: Tum ekranlarda tutarli kurumsal tasarim dili
- **Sifir placeholder**: Hem web hem mobil — tum sayfalar gercek islevsellik icerir

---

## 2. Teknoloji Stack

### 2.1 Web Uygulamasi (Streamlit)

| Katman        | Teknoloji             | Aciklama                              |
|---------------|-----------------------|---------------------------------------|
| UI Framework  | Streamlit 1.x         | Python tabanli web arayuzu            |
| AI Motoru     | OpenAI GPT-4o-mini    | Soru uretimi, PDF cikarma, analiz     |
| PDF Islem     | PyMuPDF (fitz)        | PDF render, sayfa gorsellestirme      |
| PDF Uretim    | ReportLab             | Sinav PDF, optik form, sertifika      |
| Veri Islem    | Pandas, OpenPyXL      | Excel/CSV okuma-yazma                 |
| Grafik        | Plotly, Matplotlib    | Dashboard grafikleri, analitik        |
| QR Kod        | qrcode, Pillow        | QR uretimi, gorsel isleme             |
| Barkod        | python-barcode        | Kutuphane barkod sistemi              |
| Harita        | st.map (Streamlit)    | Servis GPS takip                      |
| Parola        | bcrypt                | Sifre hashleme (12 round salt)        |

### 2.2 Mobil Uygulama (Flutter)

| Katman        | Teknoloji             | Aciklama                              |
|---------------|-----------------------|---------------------------------------|
| Framework     | Flutter 3.19.5        | Cross-platform mobil gelistirme       |
| Dil           | Dart                  | Tip guvenli programlama               |
| HTTP          | http / dio            | API istemcisi                         |
| Yerel Cache   | SharedPreferences     | Offline veri onbellegi                |
| Bildirim      | firebase_messaging    | Push notification                     |
| Tema          | Material 3            | Glassmorphism + gradient tasarim      |
| Ikon          | flutter_launcher_icons| Uygulamaya ozel launcher ikonu        |
| Splash        | flutter_native_splash | Animasyonlu acilis ekrani             |

### 2.3 Backend API (FastAPI)

| Katman        | Teknoloji             | Aciklama                              |
|---------------|-----------------------|---------------------------------------|
| Framework     | FastAPI               | Asenkron REST API                     |
| ASGI Server   | Uvicorn               | Production-grade Python sunucu        |
| JWT           | python-jose           | Token uretim ve dogrulama             |
| Sifre         | passlib + bcrypt      | Parola hashleme                       |
| Validasyon    | Pydantic v2           | Veri modeli ve ayar yonetimi          |
| Rate Limit    | Ozel middleware        | IP bazli istek sinirlandirma          |
| Veri          | JSON dosya            | Streamlit ile paylasimli DataAdapter  |

---

## 3. Dizin Yapisi

```
SmartCampusAI/
|
|-- app.py                          # Ana giris noktasi (Streamlit)
|-- config.py                       # Tema, sayfa ayarlari, session state
|-- requirements.txt                # Python paket bagimliliklar
|-- .env                            # Ortam degiskenleri (API anahtarlari, sifreler)
|
|-- views/                          # Streamlit UI modulleri (291 dosya)
|   |-- __init__.py
|   |-- olcme_degerlendirme_v2.py   # Olcme & Degerlendirme ana UI
|   |-- akademik_takip.py           # Akademik Takip ana UI
|   |-- question_builder/           # Soru olusturma paketi
|   |-- halkla_iliskiler/           # Halkla iliskiler paketi
|   |-- _aibe_*.py                  # AI Ogrenme Platformu ek modulleri
|   |-- _at_*.py                    # Akademik Takip ek modulleri
|   |-- _akt_*.py                   # Akademik ek islevler
|   |-- _eu_*.py                    # Erken Uyari ek modulleri
|   |-- _destek_*.py                # Destek hizmetleri ek modulleri
|   |-- _dk_*.py                    # Dijital Kutuphane ek modulleri
|   |-- _ek_*.py                    # Egitim Koclugu ek modulleri
|   |-- _bt_*.py                    # Butce Gelir Gider ek modulleri
|   |-- _kh_*.py                    # Kurum Hizmetleri ek modulleri
|   |-- _kim_*.py                   # Kurumsal Organizasyon ek modulleri
|   |-- _ik_*.py                    # Insan Kaynaklari ek modulleri
|   |-- _kayit_*.py                 # Kayit Modulu ek modulleri
|   `-- ...                         # Diger view dosyalari
|
|-- models/                         # Veri modelleri ve is mantigi (~100 dosya)
|   |-- olcme_degerlendirme.py      # OD veri modelleri + DataStore
|   |-- akademik_takip.py           # Akademik Takip modelleri
|   |-- kayit_modulu.py             # Kayit modulu modelleri
|   |-- insan_kaynaklari.py         # IK modelleri
|   |-- butce_gelir_gider.py        # Butce modelleri
|   |-- odeme_takip.py              # Odeme Takip modelleri
|   |-- rehberlik.py                # Rehberlik modelleri
|   |-- kutuphane.py                # Kutuphane modelleri
|   |-- okul_sagligi.py             # Okul Sagligi modelleri
|   |-- servis_yonetimi.py          # Servis GPS modelleri
|   |-- sosyal_etkinlik.py          # Sosyal Etkinlik modelleri
|   |-- toplanti_kurullar.py        # Toplanti & Kurullar modelleri
|   |-- randevu_ziyaretci.py        # Randevu & Ziyaretci modelleri
|   |-- sivil_savunma_isg.py        # Sivil Savunma & ISG modelleri
|   |-- erken_uyari.py              # Erken Uyari sistemi
|   |-- gamification.py             # Oyunlastirma motoru
|   |-- adaptive_learning.py        # Adaptif ogrenme motoru
|   `-- ...                         # Diger model dosyalari
|
|-- services/                       # Is mantigi servisleri
|   `-- question_generation.py      # OpenAI soru uretim servisi
|
|-- utils/                          # Yardimci fonksiyonlar
|   |-- auth.py                     # Kimlik dogrulama + RBAC
|   |-- tenant.py                   # Multi-tenant yonetim
|   |-- shared_data.py              # Merkezi veri kaynaklari (moduller arasi)
|   |-- backup.py                   # Otomatik gunluk yedekleme
|   |-- chart_utils.py              # Plotly gold tema sablonu
|   |-- bildirim_servisi.py         # SMS/Email bildirim soyutlamasi
|   |-- database.py                 # Veritabani yardimcilari
|   |-- cache.py                    # Onbellek yardimcilari
|   |-- learning_outcomes.py        # Excel kazanim okuyucu
|   |-- pdf_pipeline.py             # PDF isleme pipeline
|   |-- kayit_*.py                  # Kayit modulu yardimcilari (~15 dosya)
|   `-- ...                         # Diger util dosyalari
|
|-- data/                           # Veri depolama (683 JSON dosyasi)
|   |-- users.json                  # Kullanici veritabani
|   |-- question_bank.json          # Global soru bankasi
|   |-- akademik/                   # Akademik Takip verileri
|   |-- olcme/                      # Olcme & Degerlendirme verileri
|   |-- odeme/                      # Odeme Takip verileri
|   |-- bildirim/                   # Bildirim servisi verileri
|   |-- kutuphane/                  # Kutuphane verileri
|   |-- yemek/                      # Yemek tercihi verileri
|   |-- saglik/                     # Okul sagligi verileri
|   |-- rehberlik/                  # Rehberlik verileri
|   |-- sosyal_etkinlik/            # Sosyal etkinlik verileri
|   |-- sosyal_medya/               # Sosyal medya verileri
|   |-- kayit_modulu/               # Kayit modulu verileri
|   |-- kurumsal/                   # Kurumsal organizasyon
|   |-- toplanti/                   # Toplanti & Kurullar
|   |-- mezunlar/                   # Mezunlar & Kariyer
|   |-- ihbar_hatti/                # Ihbar hatti verileri
|   |-- mood_checkin/               # Ruh hali takibi
|   |-- erken_uyari/                # Erken uyari verileri
|   |-- fono/                       # Ingilizce dil dersleri
|   |-- fono_almanca/               # Almanca dil dersleri
|   |-- fono_fransizca/             # Fransizca dil dersleri
|   |-- fono_ispanyolca/            # Ispanyolca dil dersleri
|   |-- fono_italyanca/             # Italyanca dil dersleri
|   |-- bilgi_treni/                # AI Treni verileri
|   |-- stem/                       # STEAM Merkezi verileri
|   `-- tenants/                    # Tenant-spesifik veriler
|       |-- uz_koleji/
|       |-- aykin_koleji/
|       |-- ayk_n_koleji/
|       `-- smartcampus_koleji/
|
|-- mobile/                         # Mobil uygulama (Flutter + FastAPI)
|   |-- flutter_app/                # Flutter uygulamasi
|   |   |-- lib/
|   |   |   |-- main.dart           # Uygulama giris noktasi
|   |   |   |-- app.dart            # MaterialApp yapilandirmasi
|   |   |   |-- core/               # Cekirdek: API, auth, tema, widget
|   |   |   |-- features/           # Rol bazli sayfalar
|   |   |   |   |-- auth/           # Giris sayfasi
|   |   |   |   |-- ogrenci/        # Ogrenci sayfalari (24)
|   |   |   |   |-- veli/           # Veli sayfalari (13)
|   |   |   |   |-- ogretmen/       # Ogretmen sayfalari (7)
|   |   |   |   |-- rehber/         # Rehber sayfalari (13)
|   |   |   |   |-- yonetici/       # Yonetici sayfalari (21)
|   |   |   |   `-- shared/         # Paylasilan sayfalar (5)
|   |   |   `-- shared/             # Paylasilan widget'lar
|   |   |-- pubspec.yaml            # Flutter bagimliliklar
|   |   `-- assets/                 # Gorseller, ikonlar
|   |
|   `-- backend/                    # FastAPI backend
|       |-- main.py                 # FastAPI giris noktasi
|       |-- core/
|       |   |-- config.py           # Ayarlar (pydantic-settings)
|       |   |-- security.py         # JWT + bcrypt islemleri
|       |   |-- data_adapter.py     # JSON veri adaptoru
|       |   `-- deps.py             # FastAPI bagimliliklari
|       |-- routers/                # API router'lari (13 adet)
|       |   |-- auth.py             # Kimlik dogrulama
|       |   |-- ogrenci.py          # Ogrenci islemleri
|       |   |-- veli.py             # Veli islemleri
|       |   |-- ogretmen.py         # Ogretmen islemleri
|       |   |-- rehber.py           # Rehber islemleri
|       |   |-- yonetici.py         # Yonetici islemleri
|       |   |-- messaging.py        # Mesajlasma
|       |   |-- mood.py             # Ruh hali takibi
|       |   |-- ihbar.py            # Ihbar hatti
|       |   |-- smarti.py           # AI asistan
|       |   |-- quiz_koleksiyon.py  # Bilgi yarismasi
|       |   |-- bildirim.py         # Bildirim servisi
|       |   `-- odeme.py            # Odeme islemleri
|       `-- schemas/                # Pydantic sema dosyalari
|
|-- .github/
|   `-- workflows/
|       `-- build-apk.yml           # GitHub Actions — otomatik APK build
|
`-- assets/                         # Statik dosyalar (logo, gorsel)
```

---

## 4. Modul Listesi (34 Modul)

Web uygulamasi 8 sidebar grubunda toplam 34 modul icerir:

### 4.1 GENEL (3 modul)

| # | Modul Adi             | Aciklama                                              |
|---|-----------------------|-------------------------------------------------------|
| 1 | Ana Sayfa             | Hosgeldin ekrani, hizli erisim kartlari, ozet bilgiler |
| 2 | Yonetim Tek Ekran     | Tum okul verilerinin tek ekranda ozet gorunumu         |
| 3 | Analitik Dashboard    | 5 sekmeli analitik panel (Plotly grafikleri)            |

### 4.2 KURUM YONETIMI (7 modul)

| # | Modul Adi                         | Aciklama                                              |
|---|-----------------------------------|-------------------------------------------------------|
| 4 | Kurumsal Organizasyon ve Iletisim | Okul profili, org semasi, iletisim, sinif listeleri   |
| 5 | Insan Kaynaklari Yonetimi         | Personel CRUD, izin takibi, ozluk, pozisyon yonetimi  |
| 6 | Kayit Modulu                      | Aday takip (CRM), kampanya, gorusme, kesin kayit      |
| 7 | Butce Gelir Gider                 | Gelir/gider takibi, butce planlama, raporlar           |
| 8 | Odeme Takip                       | Taksit planlari, makbuz, veli odeme portali            |
| 9 | Sosyal Medya Yonetimi             | Icerik planlama, performans takibi, takvim             |
|10 | Kurum Hizmetleri                  | Destek hizmetleri, form yonetimi, MEB formlar          |

### 4.3 ILETISIM & RANDEVU (3 modul)

| # | Modul Adi               | Aciklama                                              |
|---|-------------------------|-------------------------------------------------------|
|11 | Veli-Ogretmen Gorusme   | Gorusme zamanlama, randevu olusturma, takip            |
|12 | Randevu ve Ziyaretci    | Ziyaretci giris/cikis, randevu yonetimi, rehber       |
|13 | Toplanti ve Kurullar    | Toplanti planlama, katilimci takibi, tutanak           |

### 4.4 AKADEMIK (7 modul)

| # | Modul Adi                 | Aciklama                                              |
|---|---------------------------|-------------------------------------------------------|
|14 | Akademik Takip            | Not girisi, devamsizlik, ders programi, yillik plan   |
|15 | Olcme ve Degerlendirme    | Soru bankasi, sinav olusturma, online sinav, analiz   |
|16 | Ogrenci Zeka Merkezi      | Oyunlastirma, zeka oyunlari, matematik, bilisim       |
|17 | Okul Oncesi - Ilkokul     | Okul oncesi + ilkokul mufredati, etkinlik planlama    |
|18 | Rehberlik                 | Vaka takibi, BEP, psikolojik test, kriz mudahale      |
|19 | Sertifika Uretici         | 7 sablon, PDF uretim, toplu ZIP, ozel tasarim          |
|20 | Egitim Koclugu            | Bireylestirmis destek, hedef takibi, ilerleme raporu   |

### 4.5 DIJITAL OGRENME (5 modul)

| # | Modul Adi               | Aciklama                                              |
|---|-------------------------|-------------------------------------------------------|
|21 | AI Ogrenme Platformu    | GPT destekli icerik, adaptif ogrenme, dijital pasaport|
|22 | Yabanci Dil             | 5 dil (EN/DE/FR/ES/IT), CEFR bazli, konusma pratiği  |
|23 | Kisisel Dil Gelisimi    | Bireysel dil ilerleme takibi, kelime defteri           |
|24 | AI Treni                | Oyunlastirilmis bilgi yarismasi (gomulu, backend yok) |
|25 | STEAM Merkezi           | Bilim, teknoloji, muhendislik, sanat, matematik       |

### 4.6 OKUL YASAMI (5 modul)

| # | Modul Adi               | Aciklama                                              |
|---|-------------------------|-------------------------------------------------------|
|26 | Sosyal Etkinlik ve Kulupler | Kulup yonetimi, etkinlik planlama, katilimci takip |
|27 | Kutuphane               | Barkod sistemi, odunc takibi, 20 ornek kitap          |
|28 | Okul Sagligi Takip      | Revir kayitlari, saglik formlari, alerji takibi        |
|29 | Yemek Tercihi ve Alerji | 11 alerjen, menu catisma kontrolu, diyet tercihleri    |
|30 | Servis GPS Takip        | Otobus rota takibi (st.map), ogrenci binis listesi    |

### 4.7 OPERASYON (3 modul)

| # | Modul Adi                       | Aciklama                                              |
|---|---------------------------------|-------------------------------------------------------|
|31 | Tesis ve Varlik Yonetimi        | Demirbas, tuketim malzemesi, bakim planlama            |
|32 | Sivil Savunma ve IS Guvenligi   | Tatbikat planlama, risk degerlendirme, egitim takibi   |
|33 | Mezunlar ve Kariyer Yonetimi    | Mezun veritabani, mentorluk, etkinlik, is takibi       |

### 4.8 SISTEM (1 modul)

| # | Modul Adi | Aciklama                                              |
|---|-----------|-------------------------------------------------------|
|34 | AI Destek | Yapay zeka destekli sistem yardimcisi                  |

---

## 5. Mobil Uygulama Mimarisi

### 5.1 Genel Yapi

Mobil uygulama Flutter ile gelistirilmistir. Toplam 99 Dart dosyasi, 5 kullanici
rolu icin 78 gercek sayfa icerir. Hicbir placeholder sayfa yoktur.

```
mobile/flutter_app/lib/
|-- main.dart               # Uygulama giris noktasi
|-- app.dart                # MaterialApp, route yapisi, tema
|-- core/
|   |-- api/
|   |   |-- api_client.dart         # HTTP istemci (base URL, token yonetimi)
|   |   |-- ogrenci_api.dart        # Ogrenci API cagrilari
|   |   |-- ogretmen_api.dart       # Ogretmen API cagrilari
|   |   |-- rehber_yonetici_api.dart# Rehber+Yonetici API cagrilari
|   |   `-- veli_api.dart           # Veli API cagrilari
|   |-- auth/
|   |   `-- auth_service.dart       # JWT saklama, giris/cikis, token yenileme
|   |-- services/
|   |   |-- notification_service.dart   # Push bildirim yonetimi
|   |   `-- offline_cache_service.dart  # Cevrimdisi veri onbellegi
|   |-- theme/
|   |   |-- app_theme.dart          # Renk paleti, tipografi, gradient tanimlari
|   |   `-- theme_provider.dart     # Dark/Light tema gecisi
|   `-- widgets/
|       `-- premium_widgets.dart    # Glassmorphism kartlar, animasyonlu bilesenler
|-- features/
|   |-- auth/
|   |   `-- login_page.dart         # Animasyonlu giris ekrani
|   |-- ogrenci/ (24 sayfa)
|   |-- veli/ (13 sayfa)
|   |-- ogretmen/ (7 sayfa)
|   |-- rehber/ (13 sayfa)
|   |-- yonetici/ (21 sayfa)
|   `-- shared/ (5 sayfa)
`-- shared/
    `-- widgets/
        `-- ogrenci_secici.dart     # Paylasilan ogrenci secim widget'i
```

### 5.2 Rol Bazli Sayfalar

#### Ogrenci (24 sayfa)
| Sayfa | Islem |
|-------|-------|
| ogrenci_home | Ana ekran, hizli erisim kartlari |
| notlar_page | Not goruntuleme |
| devamsizlik_page | Devamsizlik kayitlari |
| odev_page | Odev listesi ve teslim |
| online_sinav_page | Online sinav cozme |
| sinav_sonuclari_page | Sinav sonuc analizi |
| telafi_page | Telafi gorevleri |
| kazanim_borclari_page | Kazanim borc takibi |
| mood_checkin_page | Gunluk ruh hali girisi |
| mesaj_page | Ogretmenle mesajlasma |
| smarti_chat_page | AI asistan sohbet |
| dil_gelisimi_page | Yabanci dil dersleri |
| kdg_premium_page | Kisisel dil gelisimi |
| dijital_kutuphane_page | E-kitap ve kaynak erisimi |
| ai_treni_page | Bilgi yarismasi (oyun) |
| akademik_takvim_page | Akademik takvim goruntuleme |
| defterim_page | Kisisel not defteri |
| duyuru_yemek_page | Duyuru ve yemek menusu |
| gunun_bilgisi_page | Gunun bilgisi/ipucu |
| ihbar_page | Anonim ihbar |
| bilisim_vadisi_page | Bilisim egitimi |
| kocluk_page | Egitim koclugu |
| sanat_sokagi_page | Sanat etkinlikleri |
| zeka_oyunlari_page | Zeka oyunlari |

#### Veli (13 sayfa)
| Sayfa | Islem |
|-------|-------|
| veli_home | Ana ekran, cocuk secimleri |
| cocuk_detay_page | Cocugun akademik detay |
| randevu_page | Ogretmen randevu talebi |
| servis_takip_page | Okul servisi canli takip |
| yemek_menusu_page | Haftalik menu goruntuleme |
| gunluk_bulten_page | Gunluk okul bulteni |
| saglik_rehberlik_page | Saglik ve rehberlik bilgileri |
| belge_page | Belge talep ve indirme |
| anket_page | Memnuniyet anketleri |
| geri_bildirim_page | Geri bildirim gonderme |
| basari_duvari_page | Cocugun basari duvari |
| veli_egitim_page | Veli egitim icerikleri |
| kapsul_page | Gunluk bilgi kapsulleri |

#### Ogretmen (7 sayfa)
| Sayfa | Islem |
|-------|-------|
| ogretmen_home | Ana ekran, sinif ozeti |
| yoklama_page | Yoklama girisi |
| qr_yoklama_page | QR kodlu hizli yoklama |
| not_giris_page | Not girisi |
| ders_defteri_page | Ders defteri kayitlari |
| odev_ata_page | Odev atama |
| sinav_sonuc_page | Sinav sonuc analizi |

#### Rehber (13 sayfa)
| Sayfa | Islem |
|-------|-------|
| rehber_home | Ana ekran, risk ozeti |
| mood_panel_page | Ruh hali takip paneli |
| gorusme_page | Gorusme kayitlari |
| vakalar_page | Aktif vaka yonetimi |
| risk_degerlendirme_page | Risk degerlendirme formu |
| gelisim_dosyasi_page | Ogrenci gelisim dosyasi |
| bep_page | Bireysel egitim programi |
| sosyo_duygusal_page | Sosyo-duygusal tarama |
| kriz_mudahale_page | Kriz mudahale protokolu |
| kariyer_rehberligi_page | Kariyer rehberligi |
| aile_form_page | Aile bilgi formlari |
| ihbar_inceleme_page | Ihbar inceleme |
| yonlendirme_page | Kurum disi yonlendirme |

#### Yonetici (21 sayfa)
| Sayfa | Islem |
|-------|-------|
| yonetici_home | Ana ekran, kurumsal ozet |
| bugun_okulda_page | Bugunun okul durumu |
| gun_raporu_page | Gunluk rapor |
| calisanlar_page | Calisan yonetimi |
| sinif_listeleri_page | Sinif listesi goruntuleme |
| ders_programi_page | Ders programi yonetimi |
| zaman_cizelgesi_page | Zaman cizelgesi |
| butce_page | Butce ozeti |
| kayit_ozet_page | Kayit durumu ozeti |
| onaylar_page | Onay bekleyen islemler |
| nobet_page | Nobet listesi |
| randevular_page | Randevu takibi |
| toplanti_kurullar_page | Toplanti/kurul plani |
| kutuphane_page | Kutuphane yonetimi |
| revir_page | Revir kayitlari |
| erken_uyari_page | Erken uyari paneli |
| servis_hizmetleri_page | Servis yonetimi |
| destek_hizmetleri_page | Destek hizmetleri |
| sosyal_etkinlik_page | Etkinlik yonetimi |
| tuketim_demirbas_page | Demirbas/tuketim |
| veli_talepleri_page | Veli talep yonetimi |

#### Paylasilan (5 sayfa)
| Sayfa | Islem |
|-------|-------|
| bildirim_page | Bildirim merkezi |
| profil_page | Kullanici profil ayarlari |
| gunluk_isler_page | Gunluk gorevler/isler |
| quiz_game_page | Bilgi yarismasi |
| matematik_koyu_page | Matematik alistirmalari |
| bilgi_yarismasi_koleksiyon_page | Quiz koleksiyonlari |

### 5.3 Tasarim Sistemi

Mobil uygulamada ultra premium tasarim dili kullanilir:
- **Glassmorphism**: Yarim saydam kartlar, blur efekti
- **Gradient arka planlar**: Deep navy -> mavi/mor gecisler
- **Animasyonlu splash**: Ozel acilis animasyonu (native splash)
- **Dark/Light tema**: ThemeProvider ile dinamik gecis
- **Gold aksan rengi**: Web uygulamayla tutarli marka dili

---

## 6. Backend API Yapisi

### 6.1 Genel Bilgi

| Ozellik | Deger |
|---------|-------|
| Framework | FastAPI |
| API Prefix | `/api/v1` |
| Toplam Route | ~138 |
| Toplam Router | 13 |
| Dokumantasyon | `/docs` (Swagger), `/redoc` (ReDoc) |
| Rate Limit | 100 istek/dakika/IP |

### 6.2 Router Detaylari

| Router | Prefix | Route Sayisi | Aciklama |
|--------|--------|:------------:|----------|
| auth | `/auth` | 4 | Giris, kayit, token yenileme, profil |
| ogrenci | `/ogrenci` | 9 | Not, devamsizlik, odev, sinav, takvim |
| veli | `/veli` | 22 | Cocuk bilgileri, randevu, menu, belge, servis |
| ogretmen | `/ogretmen` | 10 | Yoklama, not girisi, odev atama, ders defteri |
| rehber | `/rehber` | 20 | Vaka, gorusme, mood, risk, BEP, yonlendirme |
| yonetici | `/yonetici` | 22 | Calisan, butce, kayit, onay, rapor, nobet |
| messaging | `/messaging` | 3 | Mesaj gonderme/alma/listeleme |
| mood | `/mood` | 4 | Ruh hali kaydederme, gecmis, istatistik |
| ihbar | `/ihbar` | 4 | Anonim ihbar olusturma/takip |
| smarti | `/smarti` | 2 | AI asistan sohbet |
| quiz_koleksiyon | `/quiz` | 6 | Bilgi yarismasi koleksiyonlari |
| bildirim | `/bildirim` | 3 | Push bildirim gonderme/listeleme |
| odeme | `/odeme` | 6 | Taksit listesi, makbuz, odeme durumu |

Ek olarak `main.py` icerisinde dogrudan tanimli ~20 route bulunur (dil dersleri,
kurum hizmetleri vb.).

### 6.3 Akis Semasi

```
Flutter App
    |
    v
[HTTP Request + JWT Bearer Token]
    |
    v
FastAPI (Uvicorn)
    |-- Rate Limit Middleware (100 req/min/IP)
    |-- CORS Middleware
    |-- Exception Handler
    |
    v
Router --> Deps (get_current_user) --> Security (decode_token)
    |
    v
DataAdapter --> JSON dosyalari (data/ dizini)
    |             ^
    |             |
    `--- Ayni JSON dosyalari <--- Streamlit Web App
```

### 6.4 DataAdapter

`core/data_adapter.py` hem Streamlit hem FastAPI tarafindan kullanilan veriyi
okur/yazar. Paylasilan JSON dosya yollari:

| Veri | Dosya Yolu |
|------|------------|
| Kullanicilar | `data/users.json` |
| Ogrenciler | `data/akademik/students.json` |
| Notlar | `data/akademik/grades.json` |
| Devamsizlik | `data/akademik/attendance.json` |
| Ders Programi | `data/akademik/schedule.json` |
| Ogretmenler | `data/akademik/teachers.json` |
| Mood Check-in | `data/mood_checkin/` |
| Ihbar | `data/ihbar_hatti/` |
| Odeme | `data/odeme/` |
| Bildirim | `data/bildirim/` |

---

## 7. Veri Modeli

### 7.1 Depolama Stratejisi

Sistem JSON dosya tabanli depolama kullanir. Her modul kendi dizininde
bagimsiz JSON dosyalari tutar. Bu yaklasim:
- Kurulum kolayligi saglar (veritabani sunucusu gerekmez)
- Streamlit ve FastAPI dogrudan ayni dosyalari okur/yazar
- Tenant izolasyonu dizin bazli uygulanir
- SQLite/PostgreSQL gecisine hazirliktir

### 7.2 Veri Dizin Dagilimlari

| Dizin | JSON Dosya Sayisi | Icerik |
|-------|:-----------------:|--------|
| `data/akademik/` | ~30 | Ogrenci, not, devamsizlik, plan, etut |
| `data/olcme/` | ~10 | Soru bankasi, sinav, sonuc, kazanim |
| `data/tenants/` | 4 dizin | Tenant-spesifik tum veriler |
| `data/odeme/` | ~5 | Taksit, makbuz, odeme plani |
| `data/bildirim/` | ~5 | SMS/email sablonlari, gonderim logu |
| `data/kutuphane/` | ~5 | Kitap envanteri, odunc kayitlari |
| `data/yemek/` | ~3 | Menu, alerji, tercih |
| `data/saglik/` | ~5 | Revir kayitlari, saglik formlari |
| `data/fono*/` | ~10 | 5 dilde dil egitimi icerik |
| Diger | ~600+ | Kayit, IK, sosyal, rehberlik, vb. |
| **Toplam** | **~683** | |

### 7.3 Temel Veri Yapilari

#### Kullanici (users.json)
```
{
  "username": "string",
  "password_hash": "$2b$12...",       # bcrypt hash
  "name": "string",
  "role": "Yonetici|Ogretmen|Calisan|Ogrenci|Veli|SuperAdmin",
  "active": true,
  "created_at": "2026-01-15T10:00:00"
}
```

#### Soru (olcme/questions.json)
```
{
  "id": "uuid",
  "text": "Soru metni",
  "options": ["A", "B", "C", "D"],
  "answer": "A",
  "subject": "Matematik",
  "grade": 9,
  "difficulty": "easy|medium|hard",
  "question_type": "MCQ|true_false|fill_blank|matching|ordering|cloze|math_expr",
  "bloom": "bilgi|kavrama|uygulama|analiz|sentez|degerlendirme",
  "outcome_code": "M.9.1.1.1",
  "quality_score": 85,
  "status": "draft|in_review|approved",
  "created_at": "2026-01-31T23:00:00"
}
```

#### Ogrenci (akademik/students.json)
```
{
  "id": "stu_uuid",
  "ad": "string",
  "soyad": "string",
  "sinif": "9",
  "sube": "A",
  "numara": "1234",
  "veli_ad": "string",
  "veli_tel": "05xx..."
}
```

#### Not Kaydi (akademik/grades.json)
```
{
  "id": "not_uuid",
  "ogrenci_id": "stu_uuid",
  "ders": "Matematik",
  "donem": 1,
  "not_turu": "yazili_1|sozlu|performans|proje",
  "puan": 85.5,
  "tarih": "2026-03-15"
}
```

#### Sinav (olcme/exams.json)
```
{
  "id": "uuid",
  "baslik": "Sinav adi",
  "blueprint_id": "uuid",
  "sorular": ["q_id_1", "q_id_2", ...],
  "sure_dk": 60,
  "shuffle": true,
  "negatif_puanlama": false,
  "tab_guvenlik": true,
  "erisim_kodu": "ABC123",
  "baslangic": "2026-04-01T09:00:00",
  "bitis": "2026-04-01T10:00:00"
}
```

### 7.4 Multi-Tenant Veri Izolasyonu

```
data/tenants/
|-- uz_koleji/
|   |-- question_bank.json
|   |-- measure_eval/
|   |-- pr01_kampanya_plani.json
|   `-- ...
|-- smartcampus_koleji/
|   |-- question_bank.json
|   `-- ...
|-- aykin_koleji/
`-- ayk_n_koleji/
```

Her tenant kendi alt dizinine sahiptir. `utils/tenant.py` modulu tenant
secimi, dizin olusturma ve veri okuma/yazma islemlerini yonetir:

| Fonksiyon | Imza | Aciklama |
|-----------|------|----------|
| `tenant_key(value)` | `str -> str` | Ismi dosya sistemi guvenligi anahtara cevirir |
| `get_current_tenant()` | `-> str` | Session state'den aktif tenant'i alir |
| `get_tenant_dir(name)` | `str -> str` | Tenant dizin yolunu dondurur |
| `ensure_tenant_dir(name)` | `str -> str` | Dizini olusturup yolunu dondurur |
| `load_json_list(path)` | `str -> list` | JSON dosya yukler |
| `save_json_list(path, items)` | `str, list -> None` | JSON dosya yazar |

---

## 8. Guvenlik

### 8.1 Kimlik Dogrulama

| Katman | Mekanizma | Detay |
|--------|-----------|-------|
| Web (Streamlit) | Session bazli | `utils/auth.py` — AuthManager sinifi |
| Mobil (Flutter) | JWT Bearer | `core/security.py` — python-jose |
| Parola depolama | bcrypt | 12 round salt, `$2b$` prefix |
| Legacy destek | SHA-256 fallback | Eski hash'ler icin geriye uyumluluk |
| Otomatik guncelleme | Rehash | SHA-256 hash'ler giris sirasinda bcrypt'e cevrılır |

### 8.2 JWT Token Yapisi

| Token Tipi | Gecerlilik Suresi | Algoritma |
|------------|:-----------------:|-----------|
| Access Token | 24 saat (1440 dk) | HS256 |
| Refresh Token | 30 gun | HS256 |

Token payload:
```
{
  "sub": "username",
  "role": "Ogrenci",
  "exp": 1744156800,
  "type": "access|refresh"
}
```

### 8.3 Rol Bazli Erisim Kontrolu (RBAC)

| Rol | Web Erisim | Mobil Erisim |
|-----|------------|--------------|
| SuperAdmin | Tum moduller | - |
| Yonetici | Tum moduller | Yonetici sayfalari (21) |
| Ogretmen | Akademik moduller | Ogretmen sayfalari (7) |
| Calisan | Sinirli moduller | - |
| Ogrenci | Ogrenci modulleri | Ogrenci sayfalari (24) |
| Veli | Veli modulleri | Veli sayfalari (13) |

`utils/auth.py` icindeki `get_user_modules()` fonksiyonu her rol icin
erisilebilir modul listesini dondurur.

### 8.4 Rate Limiting

| Parametre | Deger |
|-----------|-------|
| Limit | 100 istek/dakika/IP |
| Pencere | 60 saniye (sliding window) |
| HTTP Durum | 429 Too Many Requests |
| Uygulama | FastAPI middleware (`main.py`) |

### 8.5 Sifre Yonetimi

Varsayilan sifreler ortam degiskenleri uzerinden yapilir:

| Degisken | Aciklama |
|----------|----------|
| `SA_DEFAULT_PW` | SuperAdmin varsayilan sifre |
| `ADMIN_DEFAULT_PW` | Yonetici varsayilan sifre |
| `OGR_DEFAULT_PW` | Ogretmen varsayilan sifre |
| `STU_DEFAULT_PW` | Ogrenci varsayilan sifre |
| `VELI_DEFAULT_PW` | Veli varsayilan sifre |

> UYARI: Production ortaminda bu ortam degiskenleri MUTLAKA ayarlanmalidir.
> Ayarlanmazsa kullanicinin ilk giriste sifre olusturmasi zorunlu olur.

### 8.6 CORS Yapilandirmasi

Izin verilen origin'ler (`core/config.py`):
```
http://localhost:3000
http://localhost:8501      # Streamlit
http://127.0.0.1:8501
capacitor://localhost      # Flutter WebView
http://localhost
```

> Production'da bu liste kisitlanmalidir.

---

## 9. CI/CD

### 9.1 GitHub Actions - Otomatik APK Build

Dosya: `.github/workflows/build-apk.yml`

| Ozellik | Deger |
|---------|-------|
| Tetikleyici | `push` (main/master) + Manuel (`workflow_dispatch`) |
| Runner | `ubuntu-latest` |
| Java | Temurin 17 |
| Flutter | 3.19.5 (stable) |
| Cikti | `app-release.apk` |
| Dagitim | GitHub Releases (otomatik) |

### 9.2 Build Adimlari

```
1. Checkout kod
2. Java 17 kur (Temurin)
3. Flutter SDK kur (3.19.5, stable, cache aktif)
4. Flutter dogrulama
5. Platform dosyalari olustur (android/)
6. Dependencies yukle (flutter pub get)
7. App Icon olustur (flutter_launcher_icons)
8. Splash Screen olustur (flutter_native_splash)
9. AndroidManifest.xml izinleri ekle (INTERNET, CAMERA, RECORD_AUDIO)
10. build.gradle — minSdkVersion 23'e yukselt
11. APK build (flutter build apk --release)
12. APK'yi GitHub Release olarak yayinla
```

### 9.3 Mobil Izinler

APK build sirasinda eklenen Android izinleri:
- `android.permission.INTERNET` — API erisimi
- `android.permission.CAMERA` — QR okuma, proctoring
- `android.permission.RECORD_AUDIO` — Sesli asistan

---

## 10. Kurulum ve Calistirma

### 10.1 Gereksinimler

| Bilesen | Minimum Versiyon |
|---------|-----------------|
| Python | 3.10+ |
| pip | 21.0+ |
| Flutter | 3.19.5 (yalnizca mobil icin) |
| Java | 17 (yalnizca Android build icin) |
| Git | 2.x |

### 10.2 Web Uygulamasi (Streamlit)

```bash
# 1. Repoyu klonla
git clone https://github.com/smartcampus/SmartCampusAI.git
cd SmartCampusAI

# 2. Sanal ortam olustur
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Bagimliiklari yukle
pip install -r requirements.txt

# 4. Ortam degiskenlerini ayarla
# .env dosyasi olustur:
#   OPENAI_API_KEY=sk-...
#   SA_DEFAULT_PW=guclu_sifre_123

# 5. Uygulamayi baslat
streamlit run app.py
```

Uygulama varsayilan olarak `http://localhost:8501` adresinde acilir.

### 10.3 Mobil Backend (FastAPI)

```bash
# 1. Proje kokunden baslayarak
cd mobile/backend

# 2. Ek bagimliiklari yukle (requirements henuz ayri dosyada degil)
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic-settings

# 3. Backend'i baslat
uvicorn mobile.backend.main:app --host 0.0.0.0 --port 8000 --reload

# 4. API dokumantasyonuna eris
# Swagger UI: http://localhost:8000/docs
# ReDoc:      http://localhost:8000/redoc
```

### 10.4 Flutter Mobil Uygulama

```bash
# 1. Flutter app dizinine gec
cd mobile/flutter_app

# 2. Bagimliiklari yukle
flutter pub get

# 3. App icon ve splash olustur
dart run flutter_launcher_icons
dart run flutter_native_splash:create

# 4. Debug modda calistir
flutter run

# 5. Release APK olustur
flutter build apk --release
# Cikti: build/app/outputs/flutter-apk/app-release.apk
```

### 10.5 Ortam Degiskenleri

| Degisken | Zorunlu | Varsayilan | Aciklama |
|----------|:-------:|------------|----------|
| `OPENAI_API_KEY` | Evet | - | OpenAI API anahtari |
| `OPENAI_MODEL` | Hayir | `gpt-4o-mini` | Kullanilacak AI modeli |
| `SA_DEFAULT_PW` | Onerilir | - | SuperAdmin sifresi |
| `ADMIN_DEFAULT_PW` | Onerilir | - | Yonetici sifresi |
| `OGR_DEFAULT_PW` | Onerilir | - | Ogretmen sifresi |
| `STU_DEFAULT_PW` | Onerilir | - | Ogrenci sifresi |
| `VELI_DEFAULT_PW` | Onerilir | - | Veli sifresi |
| `JWT_SECRET_KEY` | Onerilir | Sabit deger | JWT imzalama anahtari (production icin degistir) |

### 10.6 Yedekleme

Sistem otomatik gunluk yedekleme yapar (`utils/backup.py`):
- Her gun ilk erisimde tetiklenir (`app.py` lifespan)
- Son 30 yedek saklanir (`max_backups=30`)
- JSON veri dizini tamamen yedeklenir

---

## Ek: Temel Python Bagimliiklari

```
streamlit           # Web UI framework
fastapi             # REST API framework
uvicorn             # ASGI server
openai              # GPT API istemcisi
pandas              # Veri isleme
openpyxl            # Excel okuma/yazma
matplotlib          # Grafik olusturma
plotly              # Interaktif grafikler
reportlab           # PDF olusturma
pymupdf (fitz)      # PDF okuma/render
pypdf               # PDF birlestirme
qrcode              # QR kod uretimi
python-barcode      # Barkod uretimi
pillow              # Gorsel isleme
bcrypt              # Sifre hashleme
python-jose         # JWT token islemleri
passlib             # Sifre dogrulama
pydantic            # Veri modelleme
pydantic-settings   # Ayar yonetimi
numpy               # Sayisal islemler
```

---

## Ek: Notlar

1. **JSON -> SQL gecisi**: Sistem su an JSON dosya tabanli calismaktadir.
   Olceklendirme gerektiginde SQLite veya PostgreSQL'e gecis icin `DataAdapter`
   katmani hazirdir.

2. **Moduler yapi**: Her view modulu bagimsiz calisabilir. `models/` katmani
   is mantigi, `views/` katmani sunum, `utils/` katmani yardimci fonksiyonlari
   icerir.

3. **Merkezi veri kaynaklari**: `utils/shared_data.py` moduller arasi veri
   paylasimini saglar (IK personel, ogrenci, veli listesi vb.).

4. **QR kod entegrasyonu**: Sinav, etkinlik, tur rezervasyonu gibi islemler
   icin QR kod uzerinden dogrudan erisim (login gerektirmez).

5. **SMS/Email bildirim**: `utils/bildirim_servisi.py` NetGSM, Twilio ve
   SMTP saglayicilari icin soyutlama katmani sunar.

6. **Otomatik yedekleme**: `utils/backup.py` gunluk otomatik JSON yedekleme
   yapar (son 30 yedek saklanir).
