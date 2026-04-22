# SmartCampusAI - Kurulum Kilavuzu

> **Surum:** 1.0 | **Tarih:** Nisan 2026
> **Hedef Kitle:** Sunucu/IT Yoneticileri, DevOps Muhendisleri

---

## Icerik Tablosu

1. [Gereksinimler](#1-gereksinimler)
2. [Kurulum Adimlari](#2-kurulum-adimlari)
3. [Ortam Degiskenleri](#3-ortam-degiskenleri)
4. [Web Uygulamayi Baslatma](#4-web-uygulamayi-baslatma)
5. [Mobil Backend Baslatma](#5-mobil-backend-baslatma)
6. [Multi-Tenant Yapilandirma](#6-multi-tenant-yapilandirma)
7. [Yedekleme](#7-yedekleme)
8. [Guvenlik Ayarlari](#8-guvenlik-ayarlari)
9. [Guncelleme](#9-guncelleme)
10. [Sorun Giderme](#10-sorun-giderme)

---

## 1. Gereksinimler

### 1.1 Sistem Gereksinimleri

| Gereksinim | Minimum | Onerilen |
|------------|---------|----------|
| **Isletim Sistemi** | Windows 10+, Ubuntu 20.04+, macOS 12+ | Ubuntu 22.04 LTS / Windows 11 |
| **Python** | 3.10 | 3.11 veya 3.12 |
| **RAM** | 4 GB | 8 GB+ |
| **Disk Alani** | 10 GB | 20 GB+ (PDF ve yedekler icin) |
| **CPU** | 2 cekirdek | 4 cekirdek+ |
| **Ag** | Internet (AI icin) | Sabit IP (mobil erisim icin) |

### 1.2 Python Paketleri

Tum bagimliliklar `requirements.txt` dosyasinda tanimlidir. Temel paketler:

| Paket | Isllev |
|-------|--------|
| `streamlit` | Web arayuz framework'u |
| `pandas` | Veri isleme ve tablo yonetimi |
| `openai` | AI soru uretimi (GPT-4o-mini) |
| `reportlab` | PDF sinav ve rapor uretimi |
| `PyMuPDF` (fitz) | PDF okuma ve cikarma |
| `openpyxl` | Excel import/export |
| `plotly` | Interaktif grafik ve dashboard |
| `matplotlib` | Grafik uretimi |
| `numpy` | Sayisal hesaplamalar (IRT, psikometri) |
| `fastapi` | Mobil backend REST API |
| `uvicorn` | ASGI sunucu (FastAPI icin) |
| `pydantic` | Veri modeli validasyonu |
| `pydantic-settings` | Ortam degiskeni yonetimi |
| `bcrypt` | Sifre hashleme |
| `python-jose` | JWT token uretimi ve dogrulama |
| `python-dotenv` | `.env` dosya okuma |
| `pillow` | Goruntu isleme |
| `qrcode` | QR kod uretimi |
| `python-docx` | Word belgesi uretimi |
| `fpdf2` | Ek PDF uretimi |
| `pypdf` | PDF birlestirme |
| `PyPDF2` | PDF ayrma ve birlestirme |
| `pdfplumber` | PDF metin cikarma |
| `requests` | HTTP istemci |
| `opencv-python` | Goruntu isleme (optik form) |
| `edge-tts` | Metin-ses donusumu |
| `anthropic` | Anthropic Claude API |
| `audio-recorder-streamlit` | Ses kayit bileeseni |
| `pytesseract` | OCR (optik karakter tanima) |
| `pyzbar` | Barkod/QR okuma |
| `rarfile` | RAR arsiv destegi |
| `streamlit-drawable-canvas` | Cizim tahtasi bileseni |

### 1.3 Ek Sistem Bagimliliklari

- **Git** — Kaynak kodu yonetimi ve guncelleme icin
- **Tesseract OCR** — `pytesseract` icin (opsiyonel, PDF OCR kullanilacaksa)
- **FFmpeg** — Ses issleme icin (opsiyonel, TTS kullanilacaksa)

---

## 2. Kurulum Adimlari

### 2.1 Kaynak Kodu Klonlama

```bash
git clone https://github.com/aykinuz-stack/smartcampus-ai.git
cd smartcampus-ai
```

### 2.2 Sanal Ortam Olusturma (Onerilen)

Sistem genelindeki Python paketlerini etkilememek icin sanal ortam (virtualenv) kullanmaniz siddeetle onerilir:

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2.3 Bagimliliklari Yukleme

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Not:** Bazi paketler (opencv-python, PyMuPDF) derleme gerektirebilir. Windows'ta sorun yasarsaniz, onceden derlenmiis (prebuilt) paketleri kullanin:
> ```bash
> pip install opencv-python-headless  # GUI gerektirmeyen ortamlar icin
> ```

### 2.4 bcrypt Yukleme (Siifre Hashleme)

`bcrypt` paketi `requirements.txt` icerisinde listelenmiis olmayabilir ancak `utils/auth.py` tarafindan zorunlu olarak kullanilir:

```bash
pip install bcrypt
```

### 2.5 Veri Dizin Yapisini Dogrulama

Kurulumdan sonra `data/` dizininin mevcut ve temel JSON dosyalarini icerdigini dogrulayin:

```bash
ls data/
# Beklenen: akademik/ olcme/ bildirim/ tenants/ users.json ...
```

Bos bir kurulumda bu dizinler ve dosyalar ilk calistirmada otomatik olusturulacaktir.

### 2.6 Streamlit Yapilandirmasi

Proje icerisindeki `.streamlit/config.toml` dosyasi varsayilan Streamlit ayarlarini icerir:

```toml
[server]
enableStaticServing = true

[theme]
base = "dark"
primaryColor = "#6366F1"
backgroundColor = "#0B0F19"
secondaryBackgroundColor = "#131825"
textColor = "#E2E8F0"
font = "sans serif"
```

Bu dosya projeyle birlikte gelir. Sunucu portunu degistirmek icin:

```toml
[server]
enableStaticServing = true
port = 8501
address = "0.0.0.0"
```

---

## 3. Ortam Degiskenleri

Proje kokunde bir `.env` dosyasi olusturun. Bu dosya hassas bilgileri icerir ve **asla versiyon kontrolune eklenmemelidir**.

### 3.1 Ornek .env Dosyasi

```env
# ── AI Ayarlari ──────────────────────────────────────────
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Varsayilan Sifreler (ilk kurulum icin) ───────────────
# Bos birakilirsa kullanicilarin ilk giriste sifre olusturmasi zorunlu olur
SA_DEFAULT_PW=SuperAdmin2026!
ADMIN_DEFAULT_PW=Admin2026!
OGR_DEFAULT_PW=Ogretmen2026!
STU_DEFAULT_PW=Ogrenci2026!
VELI_DEFAULT_PW=Veli2026!

# ── JWT Guvenlik Anahtari (URETIMDE MUTLAKA DEGISTIR!) ──
JWT_SECRET_KEY=change-me-in-production-32-char-random-string

# ── Sunucu Ayarlari ─────────────────────────────────────
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ── Mobil Backend ────────────────────────────────────────
CORS_ORIGINS=["http://localhost:3000","http://localhost:8501"]
RATE_LIMIT_PER_MIN=100
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=30
DEBUG=false
```

### 3.2 Ortam Degiskeni Aciklamalari

| Degisken | Zorunlu | Aciklama |
|----------|---------|----------|
| `OPENAI_API_KEY` | Hayir* | OpenAI API anahtari. AI soru uretimi icin gerekli. Girilmezse AI ozellikleri devre disi kalir. |
| `SA_DEFAULT_PW` | Hayir | SuperAdmin varsayilan sifresi. Bos biirakilirsa ilk giriste sifre olusturma zorunlu. |
| `ADMIN_DEFAULT_PW` | Hayir | Yonetici varsayilan sifresi. |
| `OGR_DEFAULT_PW` | Hayir | Ogretmen varsayilan sifresi. |
| `STU_DEFAULT_PW` | Hayir | Ogrenci varsayilan sifresi. |
| `VELI_DEFAULT_PW` | Hayir | Veli varsayilan sifresi. |
| `JWT_SECRET_KEY` | **Evet** | JWT token imzalama anahtari. En az 32 karakter, rastgele, guclu bir deger kullanin. |
| `STREAMLIT_SERVER_PORT` | Hayir | Web uygulamasi portu. Varsayilan: `8501`. |
| `STREAMLIT_SERVER_ADDRESS` | Hayir | Dinlenecek IP adresi. `0.0.0.0` tum arayuzlerde dinler. |
| `CORS_ORIGINS` | Hayir | Mobil backend icin izin verilen kaynaklar. JSON dizi formati. |
| `RATE_LIMIT_PER_MIN` | Hayir | Mobil API icin dakika basina istek limiti. Varsayilan: `100`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Hayir | JWT erisim token suresi (dakika). Varsayilan: `1440` (24 saat). |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Hayir | JWT yenileme token suresi (gun). Varsayilan: `30`. |
| `DEBUG` | Hayir | Hata ayiklama modu. Uretimde `false` yapin. |

### 3.3 JWT Anahtari Uretme

Guvenli bir JWT anahtari olusturmak icin:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Bu komutun ciktisini `.env` dosyasindaki `JWT_SECRET_KEY` degerine yapisttirin.

---

## 4. Web Uygulamayi Baslatma

### 4.1 Gelistirme Modu

```bash
streamlit run app.py
```

Tarayiciniz otomatik olarak `http://localhost:8501` adresini acacaktir.

### 4.2 Uretim Modu

```bash
streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
```

| Parametre | Aciklama |
|-----------|----------|
| `--server.port` | Dinlenecek port |
| `--server.address` | `0.0.0.0` ile tum arayuzlerde dinler |
| `--server.headless` | Tarayici otomatik acilmasin |
| `--browser.gatherUsageStats` | Telemetri verisi gonderme |

### 4.3 Arka Planda Calistirma (Linux)

**systemd servisi olarak (onerilen):**

`/etc/systemd/system/smartcampus-web.service` dosyasini olusturun:

```ini
[Unit]
Description=SmartCampusAI Web Application
After=network.target

[Service]
Type=simple
User=smartcampus
WorkingDirectory=/opt/smartcampus-ai
ExecStart=/opt/smartcampus-ai/venv/bin/streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
Restart=always
RestartSec=5
EnvironmentFile=/opt/smartcampus-ai/.env

[Install]
WantedBy=multi-user.target
```

Servisi etkinlestirin ve baslatin:

```bash
sudo systemctl daemon-reload
sudo systemctl enable smartcampus-web
sudo systemctl start smartcampus-web
sudo systemctl status smartcampus-web
```

**Windows'ta arka plan (nssm ile):**

```bash
nssm install SmartCampusWeb "C:\smartcampus\venv\Scripts\streamlit.exe" "run app.py --server.headless true"
nssm set SmartCampusWeb AppDirectory "C:\smartcampus"
nssm start SmartCampusWeb
```

---

## 5. Mobil Backend Baslatma

### 5.1 Gelistirme Modu

```bash
python -m uvicorn mobile.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

- `--reload` parametresi dosya degisikliklerinde otomatik yeniden yukleme saglar (yalnizca gelistirme icin).
- API dokumantasyonu: `http://localhost:8000/docs` (Swagger UI)
- Alternatif dokumantasyon: `http://localhost:8000/redoc` (ReDoc)

### 5.2 Uretim Modu

```bash
python -m uvicorn mobile.backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level warning
```

| Parametre | Aciklama |
|-----------|----------|
| `--host 0.0.0.0` | Tum arayuzlerde dinle (mobil erisim icin sart) |
| `--port 8000` | API portu |
| `--workers 4` | Paralel isci sayisi (CPU cekirdek sayisina gore ayarlayin) |
| `--log-level` | Log seviyesi: `debug`, `info`, `warning`, `error` |

### 5.3 Arka Planda Calistirma (Linux systemd)

`/etc/systemd/system/smartcampus-api.service`:

```ini
[Unit]
Description=SmartCampusAI Mobile Backend API
After=network.target

[Service]
Type=simple
User=smartcampus
WorkingDirectory=/opt/smartcampus-ai
ExecStart=/opt/smartcampus-ai/venv/bin/python -m uvicorn \
  mobile.backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level warning
Restart=always
RestartSec=5
EnvironmentFile=/opt/smartcampus-ai/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable smartcampus-api
sudo systemctl start smartcampus-api
```

### 5.4 API Endpointleri

Backend su router'lari icerir:

| Router | Yol Oneki | Aciklama |
|--------|-----------|----------|
| `auth` | `/api/v1/auth` | Giris, token yenileme, sifre degistirme |
| `ogrenci` | `/api/v1/ogrenci` | Ogrenci verileri |
| `ogretmen` | `/api/v1/ogretmen` | Ogretmen verileri |
| `veli` | `/api/v1/veli` | Veli erisim noktaalri |
| `rehber` | `/api/v1/rehber` | Rehberlik verileri |
| `yonetici` | `/api/v1/yonetici` | Yonetici erisim noktaalri |
| `messaging` | `/api/v1/messaging` | Mesajlasma |
| `mood` | `/api/v1/mood` | Ruh hali takibi |
| `ihbar` | `/api/v1/ihbar` | Ihbar sistemi |
| `smarti` | `/api/v1/smarti` | AI asistan |
| `quiz_koleksiyon` | `/api/v1/quiz` | Quiz koleksiyonu |
| `bildirim` | `/api/v1/bildirim` | Push bildirimler |
| `odeme` | `/api/v1/odeme` | Odeme bilgileri |

### 5.5 Rate Limiting

Mobil backend yerlesik IP bazli rate limiting icerir. Varsayilan olarak her IP adresi dakikada en fazla **100 istek** gonderebilir. Bu deger `.env` dosyasindaki `RATE_LIMIT_PER_MIN` degiskeni ile ayarlanabilir.

---

## 6. Multi-Tenant Yapilandirma

### 6.1 Genel Yapi

SmartCampusAI, birden fazla okuluun ayni altyapida bagimsiz calismasini saglayan multi-tenant yapiyi destekler. Her tenant (okul) kendi veri dizinine sahiptir.

```
data/
├── tenants/
│   ├── aykin_koleji/
│   │   ├── settings.json
│   │   ├── question_bank.json
│   │   ├── generation_plan.json
│   │   └── imports/
│   ├── smartcampus_koleji/
│   │   ├── settings.json
│   │   ├── question_bank.json
│   │   └── ...
│   └── uz_koleji/
│       ├── settings.json
│       └── ...
├── akademik/         # Paylasilaan akademik veriler
├── olcme/            # Olcme degerlendirme verileri
├── users.json        # Kullanici hesaplari
└── ...
```

### 6.2 Yeni Okul (Tenant) Ekleme

1. `data/tenants/` altinda yeni bir dizin olusturun:
   ```bash
   mkdir -p data/tenants/yeni_okul
   ```

2. Zorunlu `settings.json` dosyasini olusturun:
   ```json
   {
     "okul_adi": "Yeni Okul",
     "tenant_id": "yeni_okul",
     "aktif": true,
     "olusturma_tarihi": "2026-04-21"
   }
   ```

3. Gerekli alt dizinleri olusturun:
   ```bash
   mkdir -p data/tenants/yeni_okul/imports
   ```

4. Kullanici hesaplarini `data/users.json` dosyasina ekleyin ve tenant bilgisini iliskklendirin.

### 6.3 Tenant Veri Izolasyonu

Her tenant yalnizca kendi `data/tenants/<tenant_id>/` dizinindeki verilere erisebilir. Paylasilaan veriler (MEB yillik planlari, genel mufredat vb.) ana `data/` dizininde tutulur ve tum tenant'lar tarafindan okunabilir.

---

## 7. Yedekleme

### 7.1 Otomatik Yedekleme

SmartCampusAI her gun otomatik yedekleme yapar. Sistem baslatildiginda otomatik yedekleme tetiklenir ve `backups/` dizinine ZIP formatinda kaydedilir.

**Varsayilan ayarlar:**
- Yedekleme dizini: `backups/`
- Saklanan yedek sayisi: Son 30 yedek
- Format: `backup_YYYY-MM-DD_HH-MM-SS.zip`

### 7.2 Manuel Yedekleme

Python konsolu veya script uzerinden:

```python
from utils.backup import create_backup, list_backups

# Yedek olustur
result = create_backup()
print(f"Yedek: {result['path']}, Boyut: {result['size_mb']} MB, Dosya: {result['files']}")

# Yedek listesi
backups = list_backups()
for b in backups:
    print(b)
```

### 7.3 Manuel Yedekleme (Komut Satiri)

`data/` dizinini dogrudan zipleyerek de yedekleyebilirsiniz:

**Linux/macOS:**
```bash
zip -r backups/manual_$(date +%Y%m%d_%H%M%S).zip data/ --exclude="data/__pycache__/*"
```

**Windows:**
```powershell
Compress-Archive -Path data\* -DestinationPath backups\manual_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip
```

### 7.4 Geri Yukleme

```python
from utils.backup import restore_backup

restore_backup("backups/backup_2026-04-20_01-30-00.zip")
```

> **Uyari:** Geri yukleme mevcut `data/` dizininin uzerine yazar. Geri yukleme oncesinde mevcut verilerin yedeegini almaniz onerilir.

### 7.5 Uzak Yedekleme (Onerilen)

Uretim ortaminda `backups/` dizinini duzenli olarak uzak bir konuma kopyalayin:

```bash
# rsync ile uzak sunucuya
rsync -avz backups/ backup-server:/smartcampus-backups/

# AWS S3'e
aws s3 sync backups/ s3://smartcampus-backups/ --delete

# Google Cloud Storage'a
gsutil -m rsync -r backups/ gs://smartcampus-backups/
```

---

## 8. Guvenlik Ayarlari

### 8.1 Sifre Guvenligi

**Uretim ortaminda yapilmasi gerekenler:**

1. `.env` dosyasindaki tum varsayilan sifreleri degistirin.
2. `JWT_SECRET_KEY` icin en az 48 karakter uzunlugunda rastgele bir deger olusturun:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
3. Kullanicilarin ilk giriste sifre degistirmesini zorunlu kilin.
4. Varsayilan sifre degiskenlerini bos birakarak kullanicilarin sifre olusturmasini saglayabilirsiniz.

### 8.2 CORS Yapilandirmasi

Mobil backend'in CORS ayarlarini uretim ortaminda kisitlayin. `.env` veya `mobile/backend/core/config.py` dosyasinda:

```env
CORS_ORIGINS=["https://sizin-domain.com","https://api.sizin-domain.com"]
```

**Asla** uretim ortaminda `allow_origins=["*"]` kullanmayin.

### 8.3 HTTPS Yapilandirmasi

Uretim ortaminda HTTPS kullanimi zorunludur. Nginx reverse proxy ile SSL/TLS yappilandirmasi:

```nginx
server {
    listen 443 ssl;
    server_name campus.sizin-domain.com;

    ssl_certificate /etc/letsencrypt/live/campus.sizin-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/campus.sizin-domain.com/privkey.pem;

    # Streamlit Web
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Mobil API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name campus.sizin-domain.com;
    return 301 https://$host$request_uri;
}
```

Let's Encrypt ile ucretsiz SSL sertifikasi:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d campus.sizin-domain.com
```

### 8.4 Firewall Ayarlari

Yalnizca gerekli portlari acin:

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (HTTPS yonlendirme icin)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

> **Not:** 8501 ve 8000 portlarini dogrudan disa acmayin. Nginx uzerinden proxy yapin.

### 8.5 Dosya Izinleri

```bash
# data/ dizini — uygulama kullanicisi okuyup yazabilmeli
chown -R smartcampus:smartcampus /opt/smartcampus-ai/data
chmod -R 750 /opt/smartcampus-ai/data

# .env dosyasi — yalnizca sahip okuyabilmeli
chmod 600 /opt/smartcampus-ai/.env

# backups/ dizini
chmod -R 750 /opt/smartcampus-ai/backups
```

### 8.6 Guvenlik Kontrol Listesi

| # | Kontrol | Durum |
|---|---------|-------|
| 1 | JWT_SECRET_KEY degistirildi mi? | [ ] |
| 2 | Varsayilan sifreler degistirildi mi? | [ ] |
| 3 | HTTPS aktif mi? | [ ] |
| 4 | CORS kisitlandi mi? | [ ] |
| 5 | Firewall yapilandirildi mi? | [ ] |
| 6 | .env dosyasi versiyon kontrolunde yok mu? | [ ] |
| 7 | Yedekleme otomatik calisiyor mu? | [ ] |
| 8 | Uzak yedekleme ayarlandi mi? | [ ] |
| 9 | DEBUG=false ayarlandi mi? | [ ] |
| 10 | Dosya izinleri kontrol edildi mi? | [ ] |

---

## 9. Guncelleme

### 9.1 Standart Guncelleme Proseduru

```bash
# 1. Mevcut durumu yedekle
cd /opt/smartcampus-ai
python -c "from utils.backup import create_backup; create_backup()"

# 2. En son kodu cek
git pull origin main

# 3. Bagimliliklari guncelle
pip install -r requirements.txt --upgrade

# 4. Servisleri yeniden baslat
sudo systemctl restart smartcampus-web
sudo systemctl restart smartcampus-api
```

### 9.2 Buyuk Guncelleme (Major Update)

Buyuk suruum guncellemelerinde ek adimlar gerekebilir:

```bash
# 1. Tam yedek al
python -c "from utils.backup import create_backup; create_backup()"

# 2. Servisleri durdur
sudo systemctl stop smartcampus-web
sudo systemctl stop smartcampus-api

# 3. Kodu guncelle
git pull origin main

# 4. Sanal ortami yeniden olustur (opsiyonel, buyuk degisikliklerde)
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Veri migrasyonu (gerekiyorsa — CHANGELOG'u kontrol edin)
python migrate.py  # Eger mevcut ise

# 6. Servisleri baslat
sudo systemctl start smartcampus-web
sudo systemctl start smartcampus-api

# 7. Dogrulama
curl -s http://localhost:8501 | head -5
curl -s http://localhost:8000/docs | head -5
```

### 9.3 Geri Alma (Rollback)

Guncelleme sonrasi sorun yasanirsa:

```bash
# 1. Servisleri durdur
sudo systemctl stop smartcampus-web
sudo systemctl stop smartcampus-api

# 2. Onceki surume don
git log --oneline -5     # Onceki commit'i bul
git checkout <commit-hash>

# 3. Bagimliliklari eski surume getir
pip install -r requirements.txt

# 4. Gerekirse veri yedegini geri yukle
python -c "from utils.backup import restore_backup; restore_backup('backups/backup_YYYY-MM-DD_HH-MM-SS.zip')"

# 5. Servisleri baslat
sudo systemctl start smartcampus-web
sudo systemctl start smartcampus-api
```

---

## 10. Sorun Giderme

### 10.1 Port Cakismasi

**Belirti:** `Address already in use` hatasi.

**Tani:**
```bash
# Hangi prosesin portu kullandigini bul
# Linux/macOS:
lsof -i :8501
lsof -i :8000

# Windows:
netstat -ano | findstr :8501
netstat -ano | findstr :8000
```

**Cozum:**
```bash
# Cakisan prosesi sonlandir
kill -9 <PID>        # Linux/macOS
taskkill /PID <PID>  # Windows

# Veya farkli port kullan
streamlit run app.py --server.port 8502
```

### 10.2 Modul Import Hatasi

**Belirti:** `ModuleNotFoundError: No module named 'xxx'` hatasi.

**Cozum:**
```bash
# Eksik paketi yukle
pip install <paket-adi>

# Tum bagimliliklari kontrol et
pip install -r requirements.txt

# Sanal ortamin aktif oldugundan emin ol
which python    # Linux/macOS
where python    # Windows
```

### 10.3 JSON Veri Bozulmasi

**Belirti:** Modul acilirken `json.JSONDecodeError` hatasi.

**Tani:**
```bash
# JSON dosyasini dogrula
python -c "import json; json.load(open('data/akademik/students.json'))"
```

**Cozum:**
1. Bozuk dosyayi yeniden adlandirin:
   ```bash
   mv data/akademik/students.json data/akademik/students.json.bak
   ```
2. Son yedekten geri yukleyin veya bos bir JSON dizisi ile baslatin:
   ```bash
   echo "[]" > data/akademik/students.json
   ```

### 10.4 Streamlit Cache Sorunlari

**Belirti:** Eski veriler goruntuyleniyor, degisiklikler yansimimiyor.

**Cozum:**
```bash
# Streamlit cache'ini temizle
streamlit cache clear

# Veya tarayicida
# URL'ye ?clear_cache=true ekleyin
# veya Ctrl+Shift+R ile hard refresh yapin
```

### 10.5 Bellek Yetersizligi

**Belirti:** Uygulama yavasliyor veya cokuyor; `MemoryError` hatasi.

**Cozum:**
1. Streamlit worker sayisini azaltin:
   ```bash
   streamlit run app.py --server.maxUploadSize 50
   ```
2. Sunucu RAM'ini artirin (minimum 4 GB, onerilen 8 GB).
3. Gereksiz yedekleri temizleyin:
   ```bash
   ls -la backups/ | head -20
   ```

### 10.6 OpenAI API Hatalari

**Belirti:** AI soru uretimi calisimiyor, `AuthenticationError` veya `RateLimitError`.

| Hata | Sebebi | Cozum |
|------|--------|-------|
| `AuthenticationError` | Gecersiz API anahtari | `.env` dosyasindaki `OPENAI_API_KEY` degerini kontrol edin |
| `RateLimitError` | Istek limiti asildi | Birkaac dakika bekleyin, daha kucuk batch'ler kullanin |
| `InsufficientQuotaError` | Bakiye yetersiz | OpenAI hesabiniza bakiye ekleyin |
| `Timeout` | Baglanti zaman asimi | Internet baglantinizi kontrol edin |

### 10.7 Mobil Uygulama Baglanti Sorunlari

**Belirti:** Mobil uygulama API'ye baglanamiyor.

**Kontrol listesi:**

1. Backend calisiiyor mu?
   ```bash
   curl http://localhost:8000/docs
   ```
2. Firewall 8000 portunu engelliyor mu?
   ```bash
   sudo ufw status
   ```
3. Mobil cihaz ayni agda mi?
4. Mobil uygulamadaki sunucu IP adresi dogru mu?
5. CORS ayarlari mobil cihazin origin'ine izin veriyor mu?

### 10.8 Log Dosyalari

Sorun giderme icin log dosyalarini inceleyin:

```bash
# Streamlit loglari
journalctl -u smartcampus-web -f --lines=50

# FastAPI loglari
journalctl -u smartcampus-api -f --lines=50

# Genel Python hatalari
python -m uvicorn mobile.backend.main:app --log-level debug
```

---

## Ek: Hizli Baslangic Kontrol Listesi

Yeni bir kurulum sonrasi asagidaki adimlari sirayla tamamlayin:

```
[ ] 1. Python 3.10+ yuklu
[ ] 2. Repo klonlandi (git clone)
[ ] 3. Sanal ortam olusturuldu ve aktif
[ ] 4. pip install -r requirements.txt basarili
[ ] 5. bcrypt ek olarak yuklendi
[ ] 6. .env dosyasi olusturuldu
[ ] 7. JWT_SECRET_KEY guclu bir degerle ayarlandi
[ ] 8. Varsayilan sifreler degistirildi
[ ] 9. streamlit run app.py calisiyor (localhost:8501)
[ ] 10. Mobil backend calisiyor (localhost:8000)
[ ] 11. Swagger UI aciliyor (localhost:8000/docs)
[ ] 12. Yonetici hesabi ile web giris basarili
[ ] 13. Otomatik yedekleme calisiyor
[ ] 14. (Uretim) HTTPS yapilandirildi
[ ] 15. (Uretim) Firewall ayarlari yapildi
[ ] 16. (Uretim) CORS kisitlandi
[ ] 17. (Uretim) Uzak yedekleme aktif
```

---

> **SmartCampusAI** — Turkiye'nin en modern, kullanici dostu ve veri odakli egitim yonetim platformu.
>
> Kurulum veya yapilandirma ile ilgili sorular icin: destek@smartcampusai.com
