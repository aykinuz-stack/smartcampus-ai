# SmartCampusAI Mobile — Mimari Doküman

**Hedef:** Streamlit web uygulamasının yanında çalışan, tam entegre native mobil uygulaması.
Veri kaynağı aynı — hiç migrasyon yok.

## Teknoloji Seçimleri

| Katman | Teknoloji | Sebep |
|---|---|---|
| **Backend API** | **FastAPI** (Python 3.12+) | Streamlit ile aynı dil, JSON dosyalarını direkt kullanır, async destekli, otomatik OpenAPI docs |
| **Frontend** | **Flutter 3.x** (Dart) | Tek kodbase = Android + iOS, native performans, geniş widget kitaplığı |
| **Auth** | **JWT + bcrypt** | Mevcut `utils/auth.py` ile uyumlu, stateless |
| **Push Bildirim** | **Firebase Cloud Messaging** | Ücretsiz, Android+iOS |
| **Offline Cache** | **Hive** (Flutter) | Küçük+hızlı, JSON uyumlu |
| **State Management** | **Riverpod** | Modern Flutter standart |
| **HTTP Client** | **dio** | Interceptor + retry destekli |
| **Real-time** | **WebSocket** (FastAPI native) | Mood/bildirim anlık |

## Dizin Yapısı

```
mobile/
├── MIMARI.md                  (bu dosya)
├── YOL_HARITASI.md            (adım adım teslim planı)
├── backend/                   (FastAPI REST API)
│   ├── main.py                (uvicorn entry)
│   ├── requirements.txt
│   ├── core/
│   │   ├── config.py          (env, secrets)
│   │   ├── security.py        (JWT + bcrypt)
│   │   ├── deps.py            (FastAPI dependencies)
│   │   └── data_adapter.py    (JSON dosya köprüsü)
│   ├── routers/
│   │   ├── auth.py            (login, refresh, logout)
│   │   ├── ogrenci.py         (mood, notlar, odev...)
│   │   ├── ogretmen.py        (yoklama, not girisi...)
│   │   ├── rehber.py          (vaka, gorusme, aile...)
│   │   ├── saglik.py          (revir, ilac...)
│   │   ├── sosyal.py          (kulup, etkinlik...)
│   │   ├── erken_uyari.py     (risk score, mudahale...)
│   │   └── smarti.py          (AI chat + 26 ozellik)
│   └── schemas/               (Pydantic models)
│       ├── auth.py
│       ├── mood.py
│       ├── ogrenci.py
│       └── ...
│
├── flutter_app/               (Android + iOS)
│   ├── pubspec.yaml           (dependencies)
│   ├── android/               (Android config + Firebase)
│   ├── ios/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── app.dart           (MaterialApp root)
│   │   ├── core/
│   │   │   ├── api/           (dio client + interceptors)
│   │   │   ├── auth/          (token yonetimi)
│   │   │   ├── theme/         (design system)
│   │   │   └── storage/       (Hive adapter)
│   │   ├── features/
│   │   │   ├── auth/          (login, splash)
│   │   │   ├── home/          (rol bazli home)
│   │   │   ├── ogrenci/       (mood, notlar, odev)
│   │   │   ├── ogretmen/      (yoklama, not)
│   │   │   ├── veli/          (kapsul, mesaj, talep)
│   │   │   ├── rehber/        (vaka, gorusme)
│   │   │   └── erken_uyari/   (dashboard, liste, protokol)
│   │   └── shared/
│   │       ├── widgets/       (card, button, dialog)
│   │       └── utils/
│   └── test/
│
└── docs/
    ├── api_ornekleri.md
    └── endpoint_listesi.md
```

## Veri Akışı

```
┌─────────────────────────────────────────────────────────────┐
│                     MOBIL UYGULAMA                            │
│  Flutter (Dart)  ──────►  dio HTTP client                    │
└─────────────────────────────────────────────────────────────┘
                          │ HTTPS + JWT
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                           │
│  uvicorn (async)  ──►  routers  ──►  services  ──►  adapters │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              MEVCUT JSON VERİ DOSYALARI                       │
│  data/akademik/*.json, data/rehberlik/*.json, vb.            │
│  (Streamlit ile ORTAK — hiç migrasyon yok)                  │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────────────────────────────────────────┐
│              STREAMLIT WEB APP (mevcut)                       │
│  Aynı JSON dosyalarını okur/yazar                            │
└─────────────────────────────────────────────────────────────┘
```

**Kilit mimari kural:** Backend ve Streamlit **AYNI JSON** dosyalarını kullanır.
Mobilden gönderilen mood check-in direk Streamlit'teki rehber panelinde görünür.
Rehberin Streamlit'te açtığı vaka mobilden görünür. **Tek kaynak doğruluğu.**

## Auth Modeli

1. **Kullanıcı login POST**: `{username, password, tenant_id}`
2. **Backend doğrular** (mevcut `utils/auth.py` hash'leri)
3. **JWT oluşturur** (30 dakikalık access + 7 günlük refresh)
4. **Response**: `{access_token, refresh_token, user: {id, role, name, ...}}`
5. Tüm sonraki istekler: `Authorization: Bearer <access_token>`
6. **Rol bazlı endpoint koruması**: `@requires_role("rehber")`

## Rol Matrisi → Mobil Erişim

| Rol | Mobil App Özelliği |
|---|---|
| **Öğrenci** | Mood, notlar, ödev, devamsızlık, mesajlaşma, ihbar |
| **Veli** | Günlük Kapsül, çocuğun notu, mesaj, randevu |
| **Öğretmen** | QR yoklama, not girişi, ders defteri, ödev atama |
| **Rehber** | Vaka, görüşme, aile formu, risk uyarıları |
| **Hemşire** | Revir ziyareti, ilaç, olay kaydı |
| **Müdür / Yardımcı** | Dashboard, Erken Uyarı, onay, mesaj |
| **Koç** | Koçluk öğrencileri, görüşme, hedef |
| **SSG Sorumlusu** | İhbar hattı, tatbikat, olay |

## API Güvenlik Katmanları

1. **HTTPS zorunlu** (production)
2. **JWT imza** (HS256 + secret rotation)
3. **Rate limiting** (100 req/dk, kritik endpoint için 10 req/dk)
4. **Audit logging** (hassas veri erişimleri — KVKK gereği)
5. **CORS whitelist** (sadece Android + iOS app ID'leri)
6. **Input validation** (Pydantic — SQL/command injection koruması)

## Offline Strateji

| Veri | Offline |
|---|---|
| **Mood Check-in** | ✅ Hive'da kuyrukta bekler, bağlantı gelince senkron |
| **Yoklama** | ✅ Günün listesi cache'e alınır, offline girilir |
| **Notlar / Devamsızlık görüntüleme** | ✅ Son senkronizasyon cached |
| **Mesajlaşma** | ⚠️ Görüntüleme cached, gönderim online gerekir |
| **Ödev teslim (dosya upload)** | ❌ Online gerekir (dosya büyük) |
| **Canlı ders / Smarti chat** | ❌ Online gerekir |
| **Erken Uyarı dashboard** | ✅ Son snapshot cached |

## Push Bildirim Senaryoları

| Senaryo | Hedef | Örnek |
|---|---|---|
| Yeni not girildi | Öğrenci + Veli | "Matematik: 85 (yeni)" |
| Veli Günlük Kapsül | Veli | 18:00'de kapsül hazır |
| Ödev yaklaşıyor | Öğrenci | "Yarın teslim: Türkçe kompozisyon" |
| Devamsızlık | Veli | "Ahmet bugün 1. ders'te yoktu" |
| Mood kritik (7+ negatif) | Rehber | "Fatma 7 gün negatif mood — gorusme oner" |
| Risk kritik oluştu | Rehber + Müdür | "Emre zorbalık skoru 72 — protokol acildi" |
| Yeni mesaj | Alıcı | "Öğretmen yeni mesaj: ..." |
| Randevu yaklaşıyor | Ziyaretçi + Ev sahibi | "Randevunuz 1 saat sonra" |

## Tahmini Teslim Takvimi (Sprint bazlı)

### Sprint 0 — Temel Altyapı (bu oturum)
- [x] Mimari dokümanı
- [ ] FastAPI backend iskelet
- [ ] Auth endpoint + JWT
- [ ] İlk endpoint (Mood Check-in — POC)
- [ ] Flutter app iskelet
- [ ] Flutter login + mood sayfası

### Sprint 1 — Öğrenci Core (2 hafta)
- [ ] Ögrenci notları, devamsızlık
- [ ] Ödev listesi + teslim
- [ ] Mesajlaşma (öğretmen ↔ öğrenci)
- [ ] İhbar hattı
- [ ] Push notification altyapısı

### Sprint 2 — Veli App (2 hafta)
- [ ] Veli Günlük Kapsül (18:00 otomatik)
- [ ] Çocuk seçim + tam profil
- [ ] Randevu alma
- [ ] Mesajlaşma + belge talebi

### Sprint 3 — Öğretmen App (3 hafta)
- [ ] QR Yoklama (native kamera entegre)
- [ ] Not girişi
- [ ] Ders defteri
- [ ] Kazanım işaretleme
- [ ] Öğrenci listesi + filtre

### Sprint 4 — Rehber App (2 hafta)
- [ ] Vaka + görüşme kaydı
- [ ] Aile formu
- [ ] Mood paneli
- [ ] İhbar inceleme

### Sprint 5 — Yönetim Dashboard (2 hafta)
- [ ] Erken Uyarı özet
- [ ] Bütüncül Risk kategori liste
- [ ] Onay akışı
- [ ] Smarti chat

### Sprint 6 — Polish + Store (1 hafta)
- [ ] Tema, animasyon, onboarding
- [ ] Play Store yayın (+App Store)
- [ ] Beta test

**Toplam: ~12 hafta (3 ay) ile production-ready native mobile.**
