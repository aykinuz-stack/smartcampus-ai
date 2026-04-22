# SmartCampus Mobile APK — Otomatik Build Kilavuzu

**Son guncelleme:** 2026-04-22 | **Mevcut:** 99 Dart dosya, 138 backend route, ultra premium tasarim

Bu rehberi izleyerek **hicbir sey kurmadan** Android APK uretebilir ve
WhatsApp ile paylasabilirsin. GitHub Actions her seyi bulutta yapar.

---

## 🎯 Genel Akış

```
1. GitHub hesap aç + repo oluştur   (5 dk — bir defa)
2. Kodunu GitHub'a gönder           (5 dk — bir defa)
3. 10-15 dk bekle                   (Actions otomatik çalışır)
4. APK'yı indir                     (10 saniye)
5. WhatsApp'la paylaş               (30 saniye)
```

**Toplam ilk kurulum: ~25-30 dk.**
**Sonraki her kod değişikliği sonrası:** push yaparsın → 15 dk sonra yeni APK hazır.

---

## 📋 Adım Adım Yol Haritası

### 1️⃣ GitHub Hesabı Aç (yoksa)

1. https://github.com/signup adresine git
2. Email + şifre + kullanıcı adı seç
3. Email doğrula
4. Ücretsiz planda kal (public repo + Actions bedava)

### 2️⃣ Yeni Boş Repo Oluştur

1. https://github.com/new adresine git
2. **Repository name:** `smartcampus-ai` (veya istediğin isim)
3. **Description:** (opsiyonel) `Akıllı Kampüs Yönetim Sistemi`
4. **Public** seç (GitHub Actions ücretsiz için)
5. **"Add a README file"** → İŞARETLEME (sen zaten kod göndereceksin)
6. **"Create repository"** tıkla

### 3️⃣ Git Kurulu mu?

Terminal aç, yaz:
```bash
git --version
```

- Versiyon çıkarsa (örn: `git version 2.43.0`) → 4. adıma geç
- "command not found" derse → https://git-scm.com/download/win indir + kur

### 4️⃣ Bilgisayarda İlk Git Ayarları (bir defa)

Terminal aç (yeni proje klasöründe değil, herhangi bir yerde):
```bash
git config --global user.name "Ad Soyad"
git config --global user.email "email@ornek.com"
```

### 5️⃣ Kodu GitHub'a Gönder

SmartCampusAI klasörüne git:
```bash
cd "c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI"

# İlk seferde:
git init
git branch -M main
git add .
git commit -m "Ilk commit — SmartCampus AI + Mobile App"

# Remote ekle (repo URL'ini değiştir — GitHub'da oluşturduğun repo URL'si):
git remote add origin https://github.com/KULLANICI_ADIN/smartcampus-ai.git

# Push:
git push -u origin main
```

**Önemli:** Push sırasında GitHub kullanıcı adın + **Personal Access Token** (şifre değil!) sorar.

**Token nasıl alınır?**
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Note: `apk build`
4. Expiration: 90 days
5. Scopes: ☑ `repo` (hepsi)
6. "Generate token" → **Çıkan stringi kopyala, kaybetme**
7. Git push'ta şifre yerine bu tokeni yapıştır

### 6️⃣ GitHub Actions Otomatik Çalışır

Push biter bitmez:
1. GitHub repo sayfasına git
2. Üst barda **"Actions"** sekmesine tıkla
3. "Build Android APK" workflow'u çalışmaya başlar (sarı nokta)
4. Yaklaşık 10-15 dakika sürer

### 7️⃣ APK'yı İndir

**Yol A — Release'ten (önerilir):**
1. Repo ana sayfasında sağ taraftan **"Releases"** (veya `v1`, `v2` numarası)
2. En son sürümde **`app-release.apk`** linkine tıkla
3. İndir

**Yol B — Actions artifact'tan:**
1. Actions sekmesi → son başarılı çalışma
2. En altta **"smartcampus-app-release"** → tıkla + indir (zip içinde)

### 8️⃣ WhatsApp'la Paylaş

**Yöntem A: Direkt link paylaş (kolay)**
1. GitHub Release sayfasında APK URL'sini kopyala
2. WhatsApp'a yapıştır → gönder
3. Alıcı linke tıklar → APK indirilir

**Yöntem B: APK dosyasını direkt gönder**
1. APK'yı bilgisayarına indir (~25-30 MB)
2. WhatsApp Web'den dosya olarak gönder

### 9️⃣ Alıcı Telefona Nasıl Yükler?

1. APK'yı indir (tarayıcı veya WhatsApp üzerinden)
2. Telefon Ayarlar → Güvenlik → **"Bilinmeyen kaynaklara izin ver"** aç (Chrome için)
3. İndirilenlere git → APK'ya tıkla
4. **"Yükle"** → **"Aç"**

**Uyarı:** Android "Zararlı olabilir" diyebilir → **"Yine de yükle"**. Uygulama imzalı değil (development keystore), güvenli ama Google Play doğrulaması yok.

---

## 🔄 Kod Güncellendiğinde

Kod değiştirdikten sonra yeni APK için sadece push:

```bash
cd "c:\Users\safir\OneDrive\Masaüstü\SmartCampusAI"
git add .
git commit -m "Guncelleme: [ne degisti]"
git push
```

→ 15 dk sonra yeni APK hazır.

---

## 🌐 Backend Sorunu (ÖNEMLİ)

APK telefona yüklendi, login ekranı açıldı — **ama backend nerede?**

APK'da `http://BILGISAYAR_IP:8000` yazılı. Eğer:
- **Sadece sen aynı Wi-Fi'desen:** Çalışır
- **Başkaları farklı ağda:** Çalışmaz, login yapamaz

### Çözüm: Ngrok (Backend'i Public Yap)

Ngrok bilgisayarındaki backend'i internete açar:

1. https://ngrok.com/download → indir
2. Hesap aç (bedava), auth token al
3. Backend çalışırken terminalden:
   ```bash
   ngrok http 8000
   ```
4. Çıktıda: `Forwarding https://abc-123.ngrok-free.app -> http://localhost:8000`
5. Bu URL'i [mobile/flutter_app/lib/core/api/api_client.dart](mobile/flutter_app/lib/core/api/api_client.dart) dosyasındaki `baseUrl`'e yaz:
   ```dart
   static const String baseUrl = 'https://abc-123.ngrok-free.app/api/v1';
   ```
6. Tekrar `git push` → yeni APK otomatik oluşur

Artık kim APK'yı yüklerse backend'e ulaşabilir.

### Kalıcı Çözüm: Cloud Deploy

Backend'i bir sunucuya koy (ücretsiz seçenekler):
- **Render.com** — ücretsiz tier, Python FastAPI
- **Railway.app** — ücretsiz tier
- **Fly.io** — ücretsiz tier

Kalıcı URL olur, bilgisayarı kapatsan da çalışır.

---

## ❓ Sorun Çözme

### "Push permission denied" hatası
→ Personal Access Token kullan (şifre değil). Yukarıda yazdığım token oluşturma adımını takip et.

### Actions'ta workflow görünmedi
→ Kodda `.github/workflows/build-apk.yml` var mı kontrol et. GitHub yeşil onay vermesi lazım.

### Build hatası: "Flutter SDK not found"
→ GitHub Actions workflow otomatik kurar. Eğer hata verirse Actions loglarına bak, sebebi göster bana çözeyim.

### APK yüklenmiyor ("Uygulama yüklü değil")
→ Daha eski APK var mı? Kaldır sonra yükle.

### Telefonda açılınca "internet yok" hatası
→ Backend çalışmıyor / backend URL yanlış / Firewall. Ngrok yapılandırılmış mı?

---

## 🎁 Özet

**İlk seferinde:** 25-30 dk (GitHub hesap, git setup, push)
**Sonraki her seferde:** 15 dk (sadece push + bekle)

Bir kere setup yaparsan hayat kolaylaşır — her APK ihtiyacında bir komut yeter.

**Sorunları bana söyle, adım adım çözerim.**
