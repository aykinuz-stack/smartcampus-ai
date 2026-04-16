# SmartCampusAI Mobile — Çalıştırma Kılavuzu

Bu iskelet **çalışır durumda** ama eksik parçalar var (Firebase config, Android SDK ayarı,
diğer modüller). Aşağıdaki adımlarla geliştirme ortamını kurabilirsin.

## İçindekiler
1. [Gereksinimler](#1-gereksinimler)
2. [Backend Kurulumu](#2-backend-kurulumu-fastapi)
3. [Flutter Kurulumu](#3-flutter-kurulumu)
4. [İlk Çalıştırma](#4-ilk-calistirma)
5. [Android Cihazda Test](#5-android-cihazda-test)
6. [Production Build](#6-production-build)
7. [Eksik Parçalar (yapılacaklar)](#7-eksik-parçalar)

---

## 1. Gereksinimler

| Araç | Versiyon | Amaç |
|---|---|---|
| Python | 3.12+ | Backend |
| Flutter SDK | 3.16+ | Mobil frontend |
| Android Studio | 2023.1+ | Android SDK + Emulator |
| VS Code | son | Flutter extension için |
| Java | JDK 17 | Android build |
| Firebase CLI | son | Push notification (opsiyonel) |

### Kurulum komutları

**Flutter** (Windows):
```bash
# https://docs.flutter.dev/get-started/install/windows adresinden indir
flutter --version  # 3.16+ olmalı
flutter doctor     # Her şey yeşil olmalı
```

**Android Studio:**
- [developer.android.com/studio](https://developer.android.com/studio)
- SDK Manager → Android SDK 33+ yükle
- AVD Manager → Pixel 6 emulator oluştur

---

## 2. Backend Kurulumu (FastAPI)

### Virtual environment + bağımlılıklar

```bash
cd c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI\mobile\backend

# Python venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Paketleri yükle
pip install -r requirements.txt
```

### Backend'i başlat

```bash
cd c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI
python -m mobile.backend.main
```

Başarılı çıktı:
```
[BACKEND] SmartCampusAI Mobile Backend v1.0.0
[BACKEND] DATA_DIR: c:\...\SmartCampusAI\data
[BACKEND] API Prefix: /api/v1
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Backend'i test et

Tarayıcıda aç: **http://localhost:8000/docs**

FastAPI Swagger UI görürsün — tüm endpointleri buradan test edebilirsin.

**Login testi:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{\"username\":\"admin\",\"password\":\"sifre\",\"tenant_id\":\"default\"}'
```

---

## 3. Flutter Kurulumu

### Bağımlılıklar

```bash
cd c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI\mobile\flutter_app

flutter pub get
```

### Android platform dosyalarını oluştur

İlk kurulumda sadece `lib/` + `pubspec.yaml` var. Android+iOS platform dosyalarını üret:

```bash
flutter create . --platforms=android,ios --org=com.smartcampus.ai
```

### Icon + Splash screen (opsiyonel ilk sürüm için)

```bash
# flutter_launcher_icons paketi + assets/icons/icon.png ile icon
# flutter_native_splash paketi + assets/images/splash.png ile splash
```

---

## 4. İlk Çalıştırma

### Emulator'ı başlat

Android Studio → AVD Manager → Pixel 6 → ▶️ Play

**Önemli:** Emulator açıkken backend'de `10.0.2.2` adresi host makinenin localhost'udur.
Bu zaten `api_client.dart` içinde ayarlı.

### Flutter'ı çalıştır

```bash
cd c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI\mobile\flutter_app

flutter run
```

İlk derleme 3-5 dakika sürer. Sonra her değişiklikte **hot reload** (r tuşu) kullanılır.

### Beklenen akış

1. Splash screen (600ms)
2. Login sayfası
3. `admin` / `admin123` (örnek data'da bu olabilir — `data/users.json`'a bak)
4. Rol bazlı home (öğrenci rolüyle → `OgrenciHomePage`)
5. **Mood Check-in** kartına tıkla
6. Emoji seç → "KAYDET" → toast başarılı mesaj
7. Backend tarafında `data/mood_checkin/checkins.json` dosyasına eklendi
8. **Streamlit'te aynı veri görünür** (Rehberlik > Mood Paneli veya Öğrenci Paneli'nde)

---

## 5. Android Cihazda Test

### USB bağlantı

1. Telefonda **Ayarlar > Geliştirici Seçenekleri > USB Hata Ayıklama** aç
2. USB ile bilgisayara bağla
3. `flutter devices` → cihaz listede mi?
4. `flutter run -d <device_id>` → cihaza yükle

### Bilgisayar IP'si üzerinden backend

Telefon emulator değil gerçek cihazsa `10.0.2.2` çalışmaz.
`lib/core/api/api_client.dart` içinde:

```dart
static const String baseUrl = 'http://192.168.1.5:8000/api/v1';
// Bilgisayarın local IP'si — ipconfig ile bul
```

Windows Defender Firewall'da 8000 portunu aç.

---

## 6. Production Build

### Android APK

```bash
flutter build apk --release
# Çıktı: build/app/outputs/flutter-apk/app-release.apk
```

### Google Play Store için .aab

```bash
flutter build appbundle --release
# Çıktı: build/app/outputs/bundle/release/app-release.aab
```

### Backend Production

- HTTPS zorunlu (Let's Encrypt sertifika)
- `JWT_SECRET_KEY` güvenli bir string (32+ karakter)
- `DEBUG=False` (core/config.py)
- Uvicorn + Gunicorn (process manager)
- Nginx reverse proxy (önerilir)
- Log rotation + monitoring (Sentry, Prometheus)

```bash
# Production uvicorn komutu
gunicorn -k uvicorn.workers.UvicornWorker \
  -w 4 -b 0.0.0.0:8000 \
  mobile.backend.main:app
```

---

## 7. Eksik Parçalar (Yapılacaklar)

Şu anki iskelette **çalışan:**
- ✅ Backend FastAPI (auth + mood + health)
- ✅ JWT auth flow
- ✅ JSON data adapter (Streamlit ile ortak veri)
- ✅ Flutter login → role-based routing
- ✅ Öğrenci home page
- ✅ Mood check-in (tam end-to-end)

**Henüz yapılmamış (sprint bazlı):**

### Sprint 1 — Öğrenci Core (2 hafta)
- Backend: `routers/ogrenci.py` — notlar, devamsızlık, ödev endpoint'leri
- Flutter: NotlarPage, DevamsizlikPage, OdevlerPage
- Push bildirim altyapısı (Firebase setup)

### Sprint 2 — Veli App
- Backend: `routers/veli.py` — günlük kapsül, çocuk listesi
- Flutter: VeliHome, KapsulPage, CocukProfilPage

### Sprint 3 — Öğretmen App
- Backend: `routers/ogretmen.py` — QR yoklama, not girişi
- Flutter: QR tarayıcı (mobile_scanner), NotGirisPage

### Sprint 4 — Rehber App
- Backend: `routers/rehber.py` — vaka, görüşme, aile formu
- Flutter: VakaPage, GorusmePage, AileFormPage

### Sprint 5 — Yönetim
- Backend: `routers/erken_uyari.py` — risk skorları + protokol
- Flutter: YoneticiDashboard, RiskKategoriPage

### Sprint 6 — Polish + Store
- Dark/Light tema geçişi (Ayarlar)
- Onboarding animasyonları
- Performance optimization
- Play Store + App Store submission

### Ek geliştirmeler
- **WebSocket**: Smarti chat için real-time
- **Firebase FCM**: Push bildirim (fcm_token alma + backend send)
- **Biometric login**: `local_auth` ile parmak izi
- **Offline mode**: Hive queue ile mood offline kaydet
- **i18n**: Çoklu dil (Türkçe/İngilizce)
- **Deep links**: Bildirimden direkt sayfa açılması

---

## Dosya Yapısı Referansı

```
mobile/
├── MIMARI.md                    # Bu dosyayı önce oku
├── CALISTIRMA_KILAVUZU.md       # Bu dosya
├── backend/
│   ├── requirements.txt
│   ├── main.py                  # uvicorn entry
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py          # JWT + bcrypt
│   │   ├── deps.py              # FastAPI dependencies
│   │   └── data_adapter.py      # JSON dosya köprüsü
│   ├── routers/
│   │   ├── auth.py              # login, refresh, me
│   │   └── mood.py              # mood check-in + summary
│   └── schemas/
│       ├── auth.py
│       └── mood.py
└── flutter_app/
    ├── pubspec.yaml
    └── lib/
        ├── main.dart
        ├── app.dart              # MaterialApp + Router
        ├── core/
        │   ├── theme/app_theme.dart
        │   ├── api/api_client.dart
        │   └── auth/auth_service.dart
        └── features/
            ├── auth/login_page.dart
            └── ogrenci/
                ├── ogrenci_home.dart
                └── mood_checkin_page.dart
```

---

## Sorun Giderme

| Problem | Çözüm |
|---|---|
| `flutter pub get` hata veriyor | `flutter clean && flutter pub get` |
| Emulator bağlantı reddediyor | `http://10.0.2.2:8000` doğru mu? Backend çalışıyor mu? |
| Gerçek cihazdan bağlanamıyor | Bilgisayar IP'si `api_client.dart`'a yazıldı mı? Firewall? |
| Login 500 hatası | Backend logda ne yazıyor? `data/users.json` var mı? |
| JWT token expired | Otomatik refresh olmalı — refresh_token varsa sessizce yenilenir |
| Mood kaydetti ama Streamlit görmüyor | Aynı klasör mü? `DATA_DIR` path config doğru mu? |

---

## Next Steps

1. **Bu iskelet üzerinden çalışarak** ilk modülü (Öğrenci Notları) ekle
2. Her sprint'te 3-5 endpoint + Flutter sayfası ekleniyor
3. 12 hafta sonunda production-ready 4 native app
4. Google Play Store + App Store yayın

**İlk sprint'e hazır mısın? "Sprint 1 başla" de, Öğrenci Notları modülünü hemen ekleyeyim.**
