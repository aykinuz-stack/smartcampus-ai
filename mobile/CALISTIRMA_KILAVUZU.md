# SmartCampusAI Mobile -- Calistirma Kilavuzu

> Son guncelleme: 2026-04-21

Bu kilavuz, SmartCampusAI mobil uygulamasinin backend'ini calistirmayi, APK yuklemeyi
ve gelistirme ortamini kurmayia adim adim anlatir.

---

## Icindekiler

1. [Gereksinimler](#1-gereksinimler)
2. [Backend Calistirma](#2-backend-calistirma)
3. [APK Yukleme (Kullanicilar Icin)](#3-apk-yukleme)
4. [Giris Bilgileri](#4-giris-bilgileri)
5. [Sorun Giderme](#5-sorun-giderme)
6. [Gelistirici Notu (Flutter Build)](#6-gelistirici-notu)
7. [API Dokumantasyonu](#7-api-dokumantasyonu)

---

## 1. Gereksinimler

### Backend icin (zorunlu)

| Gereksinim | Minimum | Aciklama |
|---|---|---|
| Python | 3.10+ | 3.12 onerilir |
| pip | guncel | Paket yonetimi |
| Isletim sistemi | Windows / macOS / Linux | Herhangi biri |

### Mobil uygulama icin

| Gereksinim | Aciklama |
|---|---|
| Android telefon | Android 6.0+ (API 23+) |
| Wi-Fi | Backend ile ayni ag uzerinde olmali |

### Gelistirme icin (opsiyonel)

| Gereksinim | Minimum | Aciklama |
|---|---|---|
| Flutter SDK | 3.19+ | CI zaten build yapar; lokal gelistirme icin |
| Dart SDK | 3.2+ | Flutter ile birlikte gelir |
| Android Studio | guncel | Android SDK + emulator |
| Java | 17 | Android build icin (Temurin onerilir) |

> **Not:** Normal kullanim icin Flutter kurmaya gerek yoktur.
> GitHub Actions CI/CD otomatik olarak APK olusturur.
> Sadece backend'i calistirip APK'yi telefonunuza yukleyin.

---

## 2. Backend Calistirma

### Adim 1: Bagimliliklari yukleyin

```bash
cd SmartCampusAI
pip install fastapi uvicorn python-jose passlib bcrypt httpx pydantic-settings
```

### Adim 2: Backend'i baslatin

```bash
python -m uvicorn mobile.backend.main:app --host 0.0.0.0 --port 8000
```

Basarili cikti:

```
[BACKEND] SmartCampusAI Mobile Backend v1.0.0
[BACKEND] DATA_DIR: C:\...\SmartCampusAI\data
[BACKEND] API Prefix: /api/v1
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Adim 3: Dogrulayin

Tarayicinizda su adresleri acin:

| Adres | Beklenen |
|---|---|
| http://localhost:8000 | `{"app": "SmartCampusAI Mobile Backend", ...}` |
| http://localhost:8000/docs | Swagger API dokumantasyonu |
| http://localhost:8000/api/v1/health | `{"status": "healthy", ...}` |

### IP Adresi Notu

Mobil uygulama backend'e baglanirken bilgisayarinizin **yerel IP adresini** kullanir.
IP adresinizi ogrenmek icin:

```bash
# Windows
ipconfig

# macOS / Linux
ifconfig
# veya
ip addr show
```

Ornek: `192.168.1.103` -- Bu IP adresi `api_client.dart` icindeki `baseUrl` ile eslesmelidir.

---

## 3. APK Yukleme

### GitHub Releases'ten indirme

1. GitHub reponuzun **Releases** sayfasina gidin
2. En son surumdeki `app-release.apk` dosyasini indirin
3. APK dosyasini telefonunuza aktarin (USB, e-posta, bulut depolama, vb.)

### Telefona yukleme

1. **Ayarlar > Guvenlik > Bilinmeyen kaynaklara izin ver** secenegini acin
   (Android 8+: dosya yoneticisi icin ayri izin gerekebilir)
2. `app-release.apk` dosyasina dokunun
3. **Yukle** butonuna basin
4. Yukleme tamamlaninca **Ac** butonuna basin
5. Backend'in calistigini ve ayni Wi-Fi aginda oldugunuzu dogrulayin

### CI/CD ile otomatik APK

Her `main` branch'e push yapildiginda GitHub Actions otomatik olarak:
- APK build eder
- GitHub Release olusturur (v{build_number} tag'i ile)
- APK'yi Release'e ekler

Manuel build tetiklemek icin: GitHub > Actions > Build Android APK > Run workflow

---

## 4. Giris Bilgileri

Asagidaki test hesaplari varsayilan olarak tanimlidir:

| Kullanici Adi | Sifre | Rol | Aciklama |
|---|---|---|---|
| `admin` | `SmartCampus123` | Yonetici | Mudur / superadmin |
| `ogrenci` | `SmartCampus123` | Ogrenci | Ornek ogrenci hesabi |
| `veli` | `SmartCampus123` | Veli | Ornek veli hesabi |
| `ogretmen` | `SmartCampus123` | Ogretmen | Ornek ogretmen hesabi |
| `screhber` | `SmartCampus123` | Rehber | Psikolojik danismanluk / rehber ogretmen |

### Giris Akisi

1. Uygulamayi acin -- Splash ekrani belirir
2. Token gecerli degilse login sayfasina yonlendirilirsiniz
3. Kullanici adi ve sifre girin
4. Role gore ana sayfaya otomatik yonlendirilirsiniz:
   - `ogrenci` -> Ogrenci Ana Sayfa
   - `veli` -> Veli Ana Sayfa
   - `ogretmen` -> Ogretmen Ana Sayfa
   - `screhber` -> Rehber Ana Sayfa
   - `admin` -> Yonetici Ana Sayfa

---

## 5. Sorun Giderme

### 5.1 Backend Baglanti Hatasi

**Belirti:** Uygulama "Baglanti hatasi" veya "Sunucu bulunamadi" gosteriyor.

**Cozum:**

1. Backend'in calistigini dogrulayin:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. Telefonun ve bilgisayarin **ayni Wi-Fi aginda** oldugunu kontrol edin

3. `api_client.dart` icindeki `baseUrl` degerinin bilgisayar IP'si ile eslestigini dogrulayin:
   ```dart
   static const String baseUrl = 'http://192.168.1.103:8000/api/v1';
   ```

4. Bilgisayar guvenllik duvari (firewall) 8000 portuna izin veriyor mu kontrol edin:
   ```bash
   # Windows — gelen baglantilara izin ver
   netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
   ```

### 5.2 Wi-Fi Aglari Farkli

**Belirti:** Tarayicida `localhost:8000` calisiyor ama telefondan erisilemiyyor.

**Cozum:**
- Telefon ve bilgisayar ayni router'a bagli olmali
- Bazi kurumsal aglar cihazlar arasi trafigi engelleyebilir; "guest" ag deneyin
- Alternatif: USB tethering ile dogrudan baglanin

### 5.3 CORS Hatasi

**Belirti:** Backend loglarinda `CORS` hata mesajlari.

**Cozum:**
`mobile/backend/core/config.py` icindeki `CORS_ORIGINS` listesine telefonun eristigi URL'yi ekleyin:

```python
CORS_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "capacitor://localhost",
    "http://localhost",
    # Gerekirse ekleyin:
    # "http://192.168.1.100:8000",
]
```

### 5.4 "Module not found" Hatasi

**Belirti:** `ModuleNotFoundError: No module named 'fastapi'`

**Cozum:**
```bash
pip install fastapi uvicorn python-jose passlib bcrypt httpx pydantic-settings
```

Sanal ortam kullaniyorsaniz aktif oldugundan emin olun:
```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 5.5 JWT Token Suresi Dolmus

**Belirti:** Uygulama aniden login sayfasina donuyor.

**Cozum:**
- Access token suresi 24 saat, refresh token 30 gun
- Refresh otomatik olarak `_AuthInterceptor` tarafindan yapilir
- Sorun devam ederse uygulamadan cikis yapip tekrar giris yapin

### 5.6 Veri Gorunmuyor

**Belirti:** Sayfalar bos veya "Veri bulunamadi" gosteriyor.

**Cozum:**
- `SmartCampusAI/data/` dizininde ilgili JSON dosyalarinin var oldugundan emin olun
- Backend loglarinda (terminal) hata mesajlarini kontrol edin
- Streamlit uygulamasindan veri girisi yaparak JSON dosyalarini doldurun

---

## 6. Gelistirici Notu

> Bu bolum sadece Flutter kodunu degistirmek / lokal build yapmak isteyenler icindir.

### Flutter ortami kurma

```bash
# Flutter SDK'yi kurun (https://docs.flutter.dev/get-started/install)
# Java 17 kurulu olmali

# Proje dizinine gidin
cd SmartCampusAI/mobile/flutter_app

# Platform dosyalarini olusturun (ilk seferlik)
flutter create . --platforms=android --org=com.smartcampus.ai --project-name=smartcampus_mobile

# Bagimliliklari yukleyin
flutter pub get

# App ikonunu olusturun
dart run flutter_launcher_icons

# Splash screen olusturun
dart run flutter_native_splash:create
```

### Debug build

```bash
# Emulator veya bagli cihazda calistirin
flutter run

# Veya debug APK olusturun
flutter build apk --debug
```

### Release build

```bash
flutter build apk --release
# Cikti: build/app/outputs/flutter-apk/app-release.apk
```

### Kod uretimi (Freezed, Riverpod Generator, vb.)

```bash
dart run build_runner build --delete-conflicting-outputs
```

### baseUrl degistirme

`lib/core/api/api_client.dart` dosyasindaki IP adresini guncelleyin:

```dart
// Kendi bilgisayar IP'nizi yazin
static const String baseUrl = 'http://192.168.1.XXX:8000/api/v1';
```

### Onemli dosyalar

| Dosya | Aciklama |
|---|---|
| `lib/main.dart` | Entry point -- Hive init + ProviderScope |
| `lib/app.dart` | GoRouter tanimlamalari + SplashPage |
| `lib/core/api/api_client.dart` | Backend IP adresi burada |
| `lib/core/auth/auth_service.dart` | JWT login/logout/refresh |
| `lib/core/theme/app_theme.dart` | Tum renk, gradient, golge tanimlari |
| `lib/core/widgets/premium_widgets.dart` | GlassCard, GradientButton, KPICard |
| `pubspec.yaml` | Tum bagimliliklar + icon/splash ayarlari |

---

## 7. API Dokumantasyonu

Backend calisirken Swagger UI ile tum endpoint'leri interaktif olarak test edebilirsiniz.

| Arayuz | Adres | Aciklama |
|---|---|---|
| **Swagger UI** | http://localhost:8000/docs | Interaktif API test arayuzu |
| **ReDoc** | http://localhost:8000/redoc | Okunabilir API dokumantasyonu |
| **Root** | http://localhost:8000/ | Uygulama bilgisi |
| **Health** | http://localhost:8000/api/v1/health | Saglik kontrolu |

### Swagger ile test

1. http://localhost:8000/docs adresini acin
2. **Authorize** butonuna tiklayin
3. Oncelikle `/api/v1/auth/login` endpoint'ini kullanarak token alin:
   ```json
   {
     "username": "admin",
     "password": "SmartCampus123"
   }
   ```
4. Donen `access_token` degerini kopyalayin
5. **Authorize** butonuna tekrar tiklayin, `Bearer <token>` yazin
6. Artik korunmali endpoint'leri test edebilirsiniz

### Ornek API cagrilari (curl)

```bash
# Giris yap
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ogrenci", "password": "SmartCampus123"}'

# Ogrenci profili (token gerekli)
curl http://localhost:8000/api/v1/ogrenci/profil \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Gunluk isler (token gerekli)
curl http://localhost:8000/api/v1/gunluk-isler \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Saglik kontrolu (token gerektirmez)
curl http://localhost:8000/api/v1/health

# Dil dersleri (token gerektirmez)
curl http://localhost:8000/api/v1/dil/dersler?dil=ingilizce

# Bilgi yarismasi (token gerektirmez)
curl http://localhost:8000/api/v1/bilgi-yarismasi/ilkokul
```

---

## Hizli Baslangiic Ozeti

```bash
# 1. Bagimliliklari yukle
pip install fastapi uvicorn python-jose passlib bcrypt httpx pydantic-settings

# 2. Backend'i baslat
python -m uvicorn mobile.backend.main:app --host 0.0.0.0 --port 8000

# 3. Dogrula
# Tarayicide: http://localhost:8000/docs

# 4. APK'yi GitHub Releases'ten indirip telefona yukle

# 5. Ayni Wi-Fi'de telefondan giris yap
#    Kullanici: ogrenci / Sifre: SmartCampus123
```
