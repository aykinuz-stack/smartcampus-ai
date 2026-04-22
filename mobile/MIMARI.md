# SmartCampusAI Mobile -- Mimari Dokuman

> Son guncelleme: 2026-04-21
> Flutter 3.19+ | FastAPI | 99 Dart dosya | 135 API endpoint | 5 rol

---

## 1. Genel Bakis

SmartCampusAI Mobile, Streamlit web uygulamasinin yaninda calisan, **ayni veri kaynagini**
paylasan native Android uygulamasidir. Hicbir veri migrasyonuna gerek yoktur;
backend JSON dosyalarini direkt okur/yazar.

| Ozellik | Deger |
|---|---|
| Platform | Android (minSdk 23, targetSdk 34) |
| Framework | Flutter 3.19+ / Dart 3.2+ |
| Backend | FastAPI (Python 3.10+) |
| Dart dosya sayisi | 99 |
| API endpoint sayisi | 135 |
| Rol sayisi | 5 (ogrenci, veli, ogretmen, rehber, yonetici) |
| Toplam sayfa | 85+ (24 ogrenci, 13 veli, 7 ogretmen, 13 rehber, 21 yonetici, 6 ortak, 1 auth) |
| Tasarim | Ultra Premium -- dark/light tema, glassmorphism, gradient |
| Offline | Hive cache ile offline-first destegi |
| CI/CD | GitHub Actions -- otomatik APK build + Release |

---

## 2. Teknoloji Stack

### Frontend (Flutter)

| Paket | Versiyon | Kullanim |
|---|---|---|
| flutter_riverpod | ^2.4.9 | State management |
| go_router | ^13.0.0 | Deklaratif routing |
| dio | ^5.4.0 | HTTP client + interceptor |
| hive / hive_flutter | ^2.2.3 | Offline cache (NoSQL) |
| flutter_secure_storage | ^9.0.0 | JWT token saklama |
| google_fonts | ^6.1.0 | Tipografi (Inter, Poppins) |
| fl_chart | ^0.66.0 | Grafik / chart |
| shimmer | ^3.0.0 | Yukleme animasyonu |
| lottie | ^3.0.0 | Lottie animasyonlari |
| cached_network_image | ^3.3.0 | Resim onbellekleme |
| firebase_core | ^2.25.0 | Firebase altyapi |
| firebase_messaging | ^14.7.10 | Push bildirim (FCM) |
| flutter_local_notifications | ^16.3.0 | Lokal bildirim |
| mobile_scanner | ^3.5.5 | QR kod okuma (yoklama, ziyaretci) |
| image_picker | ^1.0.5 | Kamera (odev teslim) |
| speech_to_text | ^6.6.0 | Sesli giris (Smarti) |
| flutter_tts | ^3.8.5 | Text-to-speech |
| local_auth | ^2.1.8 | Biyometrik giris |
| connectivity_plus | ^5.0.2 | Ag durumu izleme |
| url_launcher | ^6.2.4 | Dis baglanti acma |
| intl | ^0.19.0 | Tarih / sayi formatlama |
| jwt_decoder | ^2.0.1 | Token cozumleme |

### Backend (FastAPI)

| Paket | Kullanim |
|---|---|
| fastapi | REST API framework |
| uvicorn | ASGI sunucu |
| python-jose | JWT token olusturma/dogrulama |
| passlib + bcrypt | Sifre hash |
| pydantic-settings | Yapilandirma yonetimi |
| httpx | Async HTTP client (AI entegrasyon) |

---

## 3. Dizin Yapisi

```
mobile/
|-- flutter_app/
|   |-- lib/
|   |   |-- core/
|   |   |   |-- api/
|   |   |   |   |-- api_client.dart         # Dio + JWT interceptor
|   |   |   |   |-- ogrenci_api.dart        # Ogrenci endpoint'leri
|   |   |   |   |-- ogretmen_api.dart       # Ogretmen endpoint'leri
|   |   |   |   |-- rehber_yonetici_api.dart# Rehber + Yonetici
|   |   |   |   +-- veli_api.dart           # Veli endpoint'leri
|   |   |   |-- auth/
|   |   |   |   +-- auth_service.dart       # Login, logout, token yonetimi
|   |   |   |-- services/
|   |   |   |   |-- notification_service.dart   # FCM + lokal bildirim
|   |   |   |   +-- offline_cache_service.dart  # Hive cache-first GET
|   |   |   |-- theme/
|   |   |   |   |-- app_theme.dart          # Renk, gradient, golge, radius, spacing
|   |   |   |   +-- theme_provider.dart     # Dark/Light/System toggle
|   |   |   +-- widgets/
|   |   |       +-- premium_widgets.dart    # GlassCard, GradientButton, KPICard, vb.
|   |   |-- features/
|   |   |   |-- auth/
|   |   |   |   +-- login_page.dart
|   |   |   |-- ogrenci/    (24 sayfa)
|   |   |   |-- veli/       (13 sayfa)
|   |   |   |-- ogretmen/   (7 sayfa)
|   |   |   |-- rehber/     (13 sayfa)
|   |   |   |-- yonetici/   (21 sayfa)
|   |   |   +-- shared/     (6 sayfa)
|   |   |-- shared/
|   |   |   +-- widgets/
|   |   |       +-- ogrenci_secici.dart
|   |   |-- app.dart            # GoRouter + MaterialApp + SplashPage
|   |   +-- main.dart           # Entry point (ProviderScope + Hive init)
|   |-- assets/
|   |   +-- icon/
|   |       |-- app_icon.png
|   |       +-- app_icon_fg.png
|   |-- store/
|   |   |-- play_store_listing.md
|   |   +-- privacy_policy.html
|   +-- pubspec.yaml
|-- backend/
|   |-- core/
|   |   |-- config.py          # Settings (JWT, CORS, DATA_DIR, rate limit)
|   |   |-- data_adapter.py    # JSON dosya okuma/yazma (Streamlit ile paylasimli)
|   |   |-- deps.py            # FastAPI Depends (current_user, data_adapter)
|   |   +-- security.py        # JWT create/verify, password hash
|   |-- routers/
|   |   |-- auth.py            # /auth/login, /auth/register, /auth/refresh, /auth/me
|   |   |-- bildirim.py        # /bildirim/*
|   |   |-- ihbar.py           # /ihbar/*
|   |   |-- messaging.py       # /mesaj/*
|   |   |-- mood.py            # /mood/*
|   |   |-- odeme.py           # /odeme/*
|   |   |-- ogrenci.py         # /ogrenci/*
|   |   |-- ogretmen.py        # /ogretmen/*
|   |   |-- quiz_koleksiyon.py # /quiz-koleksiyon/*
|   |   |-- rehber.py          # /rehber/*
|   |   |-- smarti.py          # /smarti/*
|   |   |-- veli.py            # /veli/*
|   |   +-- yonetici.py        # /yonetici/*
|   |-- schemas/
|   |   |-- auth.py
|   |   |-- ihbar.py
|   |   |-- messaging.py
|   |   |-- mood.py
|   |   |-- ogrenci.py
|   |   |-- ogretmen.py
|   |   |-- rehber.py
|   |   |-- veli.py
|   |   +-- yonetici.py
|   +-- main.py                # FastAPI app, CORS, rate limiting, 135 route
+-- docs/
    |-- MIMARI.md              (bu dosya)
    +-- CALISTIRMA_KILAVUZU.md
```

---

## 4. Sayfa Listesi (Rol Bazli)

### Ogrenci (24 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | ogrenci_home.dart | Ana Sayfa | /ogrenci |
| 2 | mood_checkin_page.dart | Ruh Hali Check-in | /mood |
| 3 | notlar_page.dart | Notlarim | /notes |
| 4 | devamsizlik_page.dart | Devamsizlik | /attendance |
| 5 | odev_page.dart | Odevlerim | /homework |
| 6 | mesaj_page.dart | Mesajlar | /messages |
| 7 | ihbar_page.dart | Ihbar Hatti | /ihbar |
| 8 | smarti_chat_page.dart | Smarti AI Chat | /smarti |
| 9 | dil_gelisimi_page.dart | Dil Gelisimi | /dil-gelisimi |
| 10 | akademik_takvim_page.dart | Akademik Takvim | /takvim |
| 11 | duyuru_yemek_page.dart | Duyuru & Yemek | /duyuru-yemek |
| 12 | ai_treni_page.dart | AI Treni | /ai-treni |
| 13 | online_sinav_page.dart | Online Sinav | /online-sinav |
| 14 | kocluk_page.dart | Kocluk | /kocluk |
| 15 | dijital_kutuphane_page.dart | Dijital Kutuphane | /dijital-kutuphane |
| 16 | gunun_bilgisi_page.dart | Gunun Bilgisi | /gunun-bilgisi |
| 17 | zeka_oyunlari_page.dart | Zeka Oyunlari | /zeka-oyunlari |
| 18 | kdg_premium_page.dart | KDG Premium (CEFR) | /kdg-premium |
| 19 | sinav_sonuclari_page.dart | Sinav Sonuclari | /ogrenci/sinav-sonuclari |
| 20 | kazanim_borclari_page.dart | Kazanim Borclari | /ogrenci/kazanim-borclari |
| 21 | telafi_page.dart | Telafi Gorevleri | /ogrenci/telafi |
| 22 | defterim_page.dart | Defterim | /ogrenci/defterim |
| 23 | sanat_sokagi_page.dart | Sanat Sokagi | /ogrenci/sanat-sokagi |
| 24 | bilisim_vadisi_page.dart | Bilisim Vadisi | /ogrenci/bilisim-vadisi |

### Veli (13 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | veli_home.dart | Ana Sayfa | /veli |
| 2 | cocuk_detay_page.dart | Cocuk Detay | /veli/cocuk-detay |
| 3 | kapsul_page.dart | Kapsul | /veli/kapsul |
| 4 | randevu_page.dart | Randevu | /veli/randevu |
| 5 | belge_page.dart | Belge Talebi | /veli/belge |
| 6 | geri_bildirim_page.dart | Geri Bildirim | /veli/geri-bildirim |
| 7 | servis_takip_page.dart | Servis Takip | /veli/servis |
| 8 | gunluk_bulten_page.dart | Gunluk Bulten | /veli/bulten |
| 9 | basari_duvari_page.dart | Basari Duvari | /veli/basari-duvari |
| 10 | yemek_menusu_page.dart | Yemek Menusu | /veli/yemek-menusu |
| 11 | anket_page.dart | Anket | /veli/anket |
| 12 | saglik_rehberlik_page.dart | Saglik & Rehberlik | /veli/saglik-rehberlik |
| 13 | veli_egitim_page.dart | Veli Egitim | /veli/veli-egitim |

### Ogretmen (7 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | ogretmen_home.dart | Ana Sayfa | /ogretmen |
| 2 | yoklama_page.dart | Yoklama | /ogretmen/yoklama |
| 3 | qr_yoklama_page.dart | QR Yoklama | /ogretmen/qr-yoklama |
| 4 | not_giris_page.dart | Not Girisi | /ogretmen/not |
| 5 | ders_defteri_page.dart | Ders Defteri | /ogretmen/ders-defteri |
| 6 | odev_ata_page.dart | Odev Atama | /ogretmen/odev-ata |
| 7 | sinav_sonuc_page.dart | Sinav Sonuclari | /ogretmen/sinav-sonuclari |

### Rehber (13 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | rehber_home.dart | Ana Sayfa | /rehber |
| 2 | vakalar_page.dart | Vakalar | /rehber/vakalar |
| 3 | gorusme_page.dart | Gorusme Kayitlari | /rehber/gorusme |
| 4 | aile_form_page.dart | Aile Bilgi Formu | /rehber/aile-form |
| 5 | mood_panel_page.dart | Mood Panel | /rehber/mood |
| 6 | ihbar_inceleme_page.dart | Ihbar Inceleme | /rehber/ihbar |
| 7 | risk_degerlendirme_page.dart | Risk Degerlendirme | /rehber/risk |
| 8 | gelisim_dosyasi_page.dart | Gelisim Dosyasi | /rehber/gelisim-dosyasi |
| 9 | yonlendirme_page.dart | Yonlendirme | /rehber/yonlendirme |
| 10 | kriz_mudahale_page.dart | Kriz Mudahale | /rehber/kriz |
| 11 | kariyer_rehberligi_page.dart | Kariyer Rehberligi | /rehber/kariyer |
| 12 | sosyo_duygusal_page.dart | Sosyo-Duygusal | /rehber/sosyo-duygusal |
| 13 | bep_page.dart | BEP (Bireysel Egitim) | /rehber/bep |

### Yonetici (21 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | yonetici_home.dart | Ana Sayfa | /yonetici |
| 2 | erken_uyari_page.dart | Erken Uyari | /yonetici/erken-uyari |
| 3 | onaylar_page.dart | Onaylar | /yonetici/onaylar |
| 4 | bugun_okulda_page.dart | Bugun Okulda | /yonetici/bugun-okulda |
| 5 | butce_page.dart | Butce | /yonetici/butce |
| 6 | randevular_page.dart | Randevular | /yonetici/randevular |
| 7 | gun_raporu_page.dart | Gun Raporu | /yonetici/gun-raporu |
| 8 | kayit_ozet_page.dart | Kayit Ozet | /yonetici/kayit-ozet |
| 9 | ders_programi_page.dart | Ders Programi | /yonetici/ders-programi |
| 10 | nobet_page.dart | Nobet | /yonetici/nobet |
| 11 | zaman_cizelgesi_page.dart | Zaman Cizelgesi | /yonetici/zaman-cizelgesi |
| 12 | calisanlar_page.dart | Calisanlar | /yonetici/calisanlar |
| 13 | sinif_listeleri_page.dart | Sinif Listeleri | /yonetici/sinif-listeleri |
| 14 | tuketim_demirbas_page.dart | Tuketim & Demirbas | /yonetici/tuketim-demirbas |
| 15 | destek_hizmetleri_page.dart | Destek Hizmetleri | /yonetici/destek-hizmetleri |
| 16 | revir_page.dart | Revir | /yonetici/revir |
| 17 | kutuphane_page.dart | Kutuphane | /yonetici/kutuphane |
| 18 | sosyal_etkinlik_page.dart | Sosyal Etkinlik | /yonetici/sosyal-etkinlik |
| 19 | toplanti_kurullar_page.dart | Toplanti & Kurullar | /yonetici/toplanti-kurullar |
| 20 | servis_hizmetleri_page.dart | Servis Hizmetleri | /yonetici/servis-hizmetleri |
| 21 | veli_talepleri_page.dart | Veli Talepleri | /yonetici/veli-talepleri |

### Ortak / Shared (6 sayfa)

| # | Dosya | Sayfa Adi | Rota |
|---|---|---|---|
| 1 | bildirim_page.dart | Bildirimler | /bildirimler |
| 2 | profil_page.dart | Profil | /profile |
| 3 | gunluk_isler_page.dart | Gunluk Isler | /gunluk-isler |
| 4 | bilgi_yarismasi_koleksiyon_page.dart | Bilgi Yarismasi | /bilgi-yarismasi-koleksiyon |
| 5 | matematik_koyu_page.dart | Matematik Koyu | /matematik-koyu |
| 6 | quiz_game_page.dart | Quiz Oyunu | (alt sayfa) |

---

## 5. Tasarim Sistemi

### 5.1 AppColors

```
primary         #6366F1  (Indigo 500)
primaryDark     #4338CA  (Indigo 700)
primaryLight    #818CF8  (Indigo 400)
gold            #F59E0B  (Amber 500)
goldDark        #D97706  (Amber 600)
success         #10B981  (Emerald 500)
warning         #F59E0B  (Amber 500)
danger          #EF4444  (Red 500)
info            #3B82F6  (Blue 500)
surfaceDark     #0F172A  (Slate 900)
surfaceDarker   #020617  (Slate 950)
cardDark        #1E293B  (Slate 800)
surfaceLight    #F8FAFC  (Slate 50)
```

Glassmorphism renkleri: `glassWhite (0.08)`, `glassBorder (0.12)`, `glassWhiteStrong (0.15)`.

### 5.2 AppGradients

| Gradient | Renkler |
|---|---|
| primary | Indigo 500 -> Violet 500 |
| primaryDark | Indigo 700 -> Indigo 500 |
| gold | Amber 500 -> Orange 500 |
| dark | Slate 900 -> Indigo 950 -> Slate 900 |
| darkCard | Slate 800 -> Slate 900 |
| success | Emerald 500 -> Emerald 600 |
| danger | Red 500 -> Red 600 |
| shimmer | Transparan -> Beyaz 20% -> Transparan |

### 5.3 AppShadows

| Seviye | Kullanim |
|---|---|
| soft | Kartlar, hafif yukselme |
| medium | Dialoglar, dropdown |
| strong | Modal, floating button |
| glow(color) | Renk bazli isik efekti |
| none | Golgesiz |

### 5.4 AppRadius

```
xs=6  sm=8  md=12  lg=16  xl=20  xxl=28  full=999
```

Her deger icin hazir `BorderRadius` sabiti: `bXs`, `bSm`, `bMd`, `bLg`, `bXl`, `bXxl`, `bFull`.

### 5.5 AppSpacing

```
xs=4  sm=8  md=12  lg=16  xl=20  xxl=24  xxxl=32
```

### 5.6 Premium Widgets (`premium_widgets.dart`)

| Widget | Aciklama |
|---|---|
| **GlassCard** | Glassmorphism efektli kart. BackdropFilter + blur + yari saydam arka plan. |
| **GradientButton** | Gradient arkaplanli buton. Loading state, ikon destegi. Glow golge. |
| **KPICard** | Istatistik karti. Ikon, deger, etiket. Renk bazli arka plan. |
| **SectionHeader** | Bolum basligi. Ikon + trailing aksyon butonu. |
| **FeatureTile** | Ozellik karti. Ikon, baslik, alt baslik. Tiklama destegi. |

### 5.7 Tema Degisimi

`theme_provider.dart` ile `ThemeMode.light`, `ThemeMode.dark`, `ThemeMode.system` arasinda
gecis yapilir. Kullanici tercihi `Hive` ile saklanir.

---

## 6. API Yapisi

### 6.1 Genel Bilgi

| Ozellik | Deger |
|---|---|
| Base URL | `http://<IP>:8000/api/v1` |
| Auth | JWT Bearer token (HS256) |
| Token suresi | 24 saat access, 30 gun refresh |
| Rate limit | 100 istek/dakika (IP bazli) |
| CORS | localhost:3000, localhost:8501, capacitor://localhost |
| Dokumantasyon | `/docs` (Swagger) , `/redoc` (ReDoc) |

### 6.2 Router Listesi (13 router)

| Router | Prefix | Endpoint Sayisi | Aciklama |
|---|---|---|---|
| auth | /auth | 4 | Login, register, refresh, me |
| mood | /mood | 4 | Check-in, gecmis, istatistik, son |
| ogrenci | /ogrenci | 9 | Profil, notlar, devamsizlik, odev, takvim, telafi |
| messaging | /mesaj | 3 | Gonder, listele, okundu |
| ihbar | /ihbar | 3 | Olustur, listele, durum guncelle |
| smarti | /smarti | 2 | AI sohbet, gecmis |
| veli | /veli | 22 | Cocuk bilgi, kapsul, randevu, belge, anket, odeme |
| ogretmen | /ogretmen | 10 | Yoklama, not giris, ders defteri, odev, sinav |
| rehber | /rehber | 20 | Vakalar, gorusme, mood panel, risk, BEP, kriz |
| yonetici | /yonetici | 22 | Dashboard, onay, butce, calisanlar, nobet, raporlar |
| quiz_koleksiyon | /quiz-koleksiyon | 6 | Koleksiyonlar, quiz baslat, sonuc |
| bildirim | /bildirim | 3 | Listele, okundu, toplu isaretle |
| odeme | /odeme | 6 | Borc listesi, odeme kaydi, gecmis |

### 6.3 Dogrudan main.py Uzerindeki Endpoint'ler

| Endpoint | Metot | Aciklama |
|---|---|---|
| / | GET | Uygulama bilgisi |
| /api/v1/health | GET | Healthcheck |
| /api/v1/dil/dersler | GET | Dil dersleri (5 dil) |
| /api/v1/dil/ders/{ders_no} | GET | Ders detayi |
| /api/v1/dijital-kutuphane/icerik | GET | Kutuphane kategorileri |
| /api/v1/bilgi-yarismasi/{level} | GET | Quiz sorulari |
| /api/v1/gunun-bilgisi | GET | Gunun bilgisi |
| /api/v1/e-dergi | GET | E-dergi listesi |
| /api/v1/zeka-oyunlari | GET | Oyun listesi |
| /api/v1/kdg/{dil} | GET | KDG CEFR seviyeleri |
| /api/v1/kdg/{dil}/{seviye} | GET | KDG seviye detayi |
| /api/v1/kurum/duyurular | GET | Kurum duyurulari |
| /api/v1/kurum/yemek-menusu | GET | Yemek menusu |
| /api/v1/ai-treni/config | GET | AI Treni yapilandirma |
| /api/v1/ai-treni/quiz/{sinif} | GET | Sinif bazli quiz |
| /api/v1/saglik/revir-ozet | GET | Revir ozet |
| /api/v1/kutuphane/ozet | GET | Kutuphane ozet |
| /api/v1/sosyal/ozet | GET | Sosyal etkinlik ozet |
| /api/v1/gunluk-isler | GET | Bugunku yoklama + ogretmen ek |
| /api/v1/qr-handler | GET | QR kod icerik yonlendirme |

---

## 7. Offline Cache + Bildirim

### 7.1 OfflineCacheService

Dosya: `core/services/offline_cache_service.dart`

```
Online akis:
  1. Cache'de var mi + taze mi? (maxAge kontrolu)
  2. Evet -> cache'den don (HIT)
  3. Hayir -> API'den cek -> Hive'a kaydet -> don (FRESH)

Offline akis:
  1. connectivity_plus ile ag durumu kontrol
  2. Offline -> Hive cache'den oku (STALE ama kullanilabilir)
  3. Cache bos -> hata don
```

- Varsayilan `maxAge`: 15 dakika
- Cache key: endpoint path + query parametreleri
- Her kayit `_cached_at` timestamp icerir

### 7.2 NotificationService

Dosya: `core/services/notification_service.dart`

- **Lokal bildirim:** `flutter_local_notifications` ile aninda bildirim
- **Push bildirim:** Firebase Cloud Messaging (FCM)
- Firebase platform dosyalari (`google-services.json`) yoksa sessizce atlanir
- Android kanallar otomatik olusturulur

---

## 8. Kimlik Dogrulama Akisi

```
1. Kullanici login_page'de username + password girer
2. AuthService -> POST /auth/login
3. Backend JWT access_token + refresh_token dondurur
4. Token FlutterSecureStorage'a kaydedilir
5. ApiClient her istekte Authorization: Bearer <token> ekler
6. 401 gelirse refresh_token ile yeni access_token alinir
7. Refresh da basarisiz -> login sayfasina yonlendir
```

Roller: `ogrenci`, `veli`, `ogretmen`, `rehber` (calisan), `yonetici` (mudur, superadmin)

Splash sayfasi acilista token kontrolu yapar ve role gore dogru ana sayfaya yonlendirir.

---

## 9. CI/CD -- GitHub Actions

### Workflow: `.github/workflows/build-apk.yml`

```
Tetikleyici: push -> main/master  VEYA  manuel (workflow_dispatch)

Adimlar:
  1. Checkout kod
  2. Java 17 kur (Temurin)
  3. Flutter 3.19.5 SDK kur (cache acik)
  4. flutter create . --platforms=android  (platform dosyalari olustur)
  5. flutter pub get
  6. App icon olustur (flutter_launcher_icons)
  7. Splash screen olustur (flutter_native_splash)
  8. AndroidManifest.xml'e INTERNET + CAMERA + RECORD_AUDIO izni ekle
  9. build.gradle'da minSdkVersion -> 23
  10. flutter build apk --release
  11. APK'yi artifact olarak yukle (30 gun sakla)
  12. GitHub Release olustur (v{run_number} tag'i ile)
```

Cikti: `app-release.apk` -- GitHub Releases sayfasindan indirilebilir.

---

## 10. Veri Paylasimi

Backend, Streamlit web uygulamasiyla **ayni JSON dosyalarini** kullanir.
Veri yolu: `SmartCampusAI/data/` (config.py'deki `DATA_DIR`).

```
data/
|-- akademik/         # Ogrenci, ogretmen, yoklama, ders programi, notlar
|-- olcme/            # Sorular, sinavlar, kazanimlar, yillik planlar
|-- saglik/           # Revir ziyaretleri
|-- kutuphane/        # Kitaplar, odunc kayitlari
|-- sosyal_etkinlik/  # Kulupler, etkinlikler
|-- fono/             # Ingilizce dil dersleri
|-- fono_almanca_104/ # Almanca dil dersleri
|-- fono_fransizca/   # Fransizca dil dersleri
|-- fono_italyanca/   # Italyanca dil dersleri
|-- fono_ispanyolca/  # Ispanyolca dil dersleri
|-- english/          # CEFR Ingilizce kelime + gramer
|-- german/           # CEFR Almanca kelime + gramer
|-- bilgi_treni/      # AI Treni quiz verileri
+-- users.json        # Kullanici hesaplari
```

Multi-tenant destegi: `DataAdapter` tenant_id parametresi ile farkli kurumlarin
verilerini ayri dizinlerden okuyabilir (varsayilan: `default`).

---

## 11. Guvenlik

| Onlem | Uygulama |
|---|---|
| JWT Token | HS256, 24 saat omur, refresh destegi |
| Sifre saklama | bcrypt hash (passlib) |
| Token saklama | FlutterSecureStorage (Android Keystore) |
| Rate limiting | 100 istek/dakika/IP |
| CORS | Beyaz liste bazli origin kontrolu |
| Global hata | Exception handler -- debug modda detay, production'da gizli |
| Biyometrik | local_auth ile parmak izi / yuz tanima (opsiyonel) |
