"""
Genel Modul Kilavuzu — Tum Moduller Icin Generic Kurumsal PDF Uretici
========================================================================
Tek bir generic PDF uretici. MODUL_REGISTRY'ye gore her modul icin
ayni kalitede kurumsal kilavuz uretir.

Mimari:
- MODUL_REGISTRY: Manuel tanimli modul metadata'lari (zenginlestirilmis)
- _auto_discover(modul_id): Registry'de yoksa AST ile otomatik kesfeder
- generate_pdf(modul_id): Tek modul icin PDF uretir
- generate_zip_all(): Tum modullerin PDF'lerini ZIP'ler

Kullanim:
    from models.genel_modul_kilavuzu import (
        list_moduller, generate_pdf, generate_zip_all
    )
    moduller = list_moduller()  # tum modul ID'leri
    pdf_bytes = generate_pdf("kayit_modulu")  # tek modul
    zip_bytes = generate_zip_all()  # tum moduller (zip)
"""

from __future__ import annotations

import io
import os
import ast
import zipfile
from datetime import date
from typing import Any

# ── Reportlab lazy imports ──
try:
    from reportlab.lib.units import cm as _CM
    from reportlab.platypus import (
        Paragraph, Spacer, PageBreak, Table, TableStyle,
        KeepTogether, HRFlowable, SimpleDocTemplate,
    )
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    _REPORTLAB_OK = True
except ImportError:
    _CM = 28.346
    Paragraph = Spacer = PageBreak = Table = TableStyle = None
    KeepTogether = HRFlowable = SimpleDocTemplate = None
    HexColor = None
    A4 = None
    ParagraphStyle = None
    TA_LEFT = TA_CENTER = TA_JUSTIFY = 0
    _REPORTLAB_OK = False

cm = _CM

# ============================================================
# RENK PALETI — Ultra Premium Diamond
# ============================================================

NAVY       = "#0B1E3F"
NAVY_LIGHT = "#1e293b"
GOLD       = "#C8952E"
GOLD_LT    = "#E6C77A"
GOLD_DARK  = "#8B6514"
WHITE      = "#FFFFFF"
DARK       = "#1E293B"
BODY       = "#334155"
MUTED      = "#64748B"
LIGHT_GRAY = "#F1F5F9"

RED        = "#DC2626"
ORANGE     = "#F97316"
YELLOW     = "#F59E0B"
GREEN      = "#16A34A"
BLUE       = "#3B82F6"
INDIGO     = "#6366F1"
PURPLE     = "#8B5CF6"
PINK       = "#EC4899"
CYAN       = "#06B6D4"


# ============================================================
# MODUL_REGISTRY — Tum Moduller (manuel zenginlestirilmis metadata)
# ============================================================

# Her modul icin: id, ad, emoji, view_dosya, model_dosyalari, aciklama,
# ana_ozellikler, tablar, otomatik_isler, manuel_isler, ipuclari,
# arka_plan_motorlari, veri_dosyalari, kullanim_senaryosu

MODUL_REGISTRY: dict[str, dict] = {
    "kayit_modulu": {
        "ad": "Kayit Modulu",
        "emoji": "🎯",
        "kategori": "KURUM",
        "view_dosya": "views/kayit_modulu.py",
        "model_dosyalari": [
            "models/kayit_modulu.py",
            "models/kayit_otomasyon.py",
            "models/kayit_ai_engine.py",
            "models/kayit_takip_engine.py",
            "models/kayit_sifir_kayip.py",
            "models/kayit_sessiz_red.py",
            "models/kayit_pismanlik_motoru.py",
            "models/kayit_cocuk_sesi.py",
            "models/kayit_korku_yikici.py",
            "models/kayit_gelecek_kitabi.py",
            "models/kayit_kisisel_url.py",
            "models/kayit_5dk_kurali.py",
            "models/kayit_veli_parmak_izi.py",
            "models/kayit_son_mil_gardiyan.py",
            "models/kayit_gelir_optimizasyon.py",
            "models/kayit_kurumsal_kanal.py",
            "models/kayit_ceo_cockpit.py",
        ],
        "aciklama": (
            "Aday/CRM yonetim sistemi. Kampanyadan kesin kayita kadar "
            "tum kayit yasam dongusunu yoneten profesyonel modul. "
            "19 sekme, 16 otomasyon, 7 cron tetikleyici, AI destekli "
            "icerik uretimi, dinamik fiyatlama, B2B kurumsal kanal."
        ),
        "ana_ozellikler": [
            "7 asamali pipeline (aday → kesin kayit)",
            "16 otomasyon + 7 cron-based zaman tetikleyici",
            "AI destekli kapanis silahlari (Gelecegin Mini Kitabi, Korku Yikici)",
            "Dinamik fiyatlama (WTP + LTV + Elastikiyet)",
            "B2B Kurumsal Kanal (sirket pipeline'i)",
            "CEO Command Center (sabah brifingi)",
            "Sessiz Red Dedektoru (72 saat erken uyari)",
            "5 Dakika Kurali (lead yanit savaslari)",
        ],
        "tablar": [
            ("📋 Gunluk", "Bugun yapilmasi gereken oncelikli isler", ["Bekleyen aday listesi", "Kritik eskalasyonlar", "Bugunun aramalari"], ["Aday se", "Aramayi yap", "Sonucu kaydet"]),
            ("🔄 Pipeline", "7 asamali Kanban tahtasi", ["Asama bazli aday sayilari", "Funnel donusum", "Sicak/soguk gostergesi"], ["Asama gecisleri", "Aday detay", "Notlar"]),
            ("➕ Yeni Aday", "Manuel aday kayit formu", ["Otomasyon trigger", "Duplicate kontrol", "XP kazanma"], ["Veli/ogrenci bilgileri", "UTM alanlari", "Profil zenginlestirme"]),
            ("📊 Istatistik", "Genel rakamlar + raporlar", ["Donusum hesabi", "Personel skoru", "Funnel chart"], ["Filtre/zaman secimi", "Export"]),
            ("📣 Kampanya", "AI destekli kampanya planlama", ["40+ hazir kampanya", "AI icerik uretimi", "ROI hesabi"], ["Yeni kampanya", "Sonuc kaydetme", "Referans sistemi"]),
            ("⚡ Otomasyon", "16 otomasyonun kontrol paneli", ["Tetikleyici islemler", "Kuyruk yonetimi", "Log takibi"], ["Aktif/pasif yapma", "Manuel test"]),
            ("🏫 Tur", "Public tur rezervasyonu", ["QR kod URL", "Otomatik onay"], ["QR yazdirma"]),
            ("🎯 Rakip", "Rakip okul istihbarati", ["Fiyat takibi", "Kampanya izleme"], ["Yeni rakip ekleme"]),
            ("🧮 Yerlestirme", "AI sinif optimizasyon", ["Dengeli dagilim", "Kapasite kontrol"], ["Sube tanimi"]),
            ("🏆 Skorboard", "Gamified personel performans", ["Otomatik XP", "Seviye/rozet"], ["Skoru gor"]),
            ("📢 Outreach", "Toplu mesaj gonderim", ["Filtre/grup", "AI sablon"], ["Hedef grup", "Mesaj yazma"]),
            ("🚨 Risk Radar", "Kayip riski olan adaylar", ["Sifir kayip motoru", "Kurtarma plani"], ["Kritik adaya temas"]),
            ("💎 Konusma Madeni", "Notlarin AI analizi", ["Itirazlar", "Persona", "Kapatis kelimeleri"], ["Madenleri inceleme"]),
            ("🎤 Sesli Asistan", "Voice-first not alma", ["Whisper transkript", "AI analiz"], ["Mikrofonu ac"]),
            ("🎪 Etkinlik", "Aile etkinlik merkezi", ["Public RSVP", "Otomatik tesekkur"], ["Etkinlik tanimi"]),
            ("✨ Kapanis Silahlari", "3 premium kapanis araci", ["Gelecegin Mini Kitabi PDF", "Korku Yikici raporu", "Kisisel URL + 24h Hold"], ["Aday sec", "PDF uret", "Veliye gonder"]),
            ("🧠 Zeki Motorlar", "3 gelismis predictive motor", ["Pismanlik Madenciligi", "Cocugun Ic Sesi", "Sessiz Red Dedektoru"], ["Sessiz red kritikler", "Cocuk anketi", "Pismanlik dokunuslari"]),
            ("👑 Ust Duzey", "3 stratejik motor", ["CEO Command Center", "Gelir Optimizasyon", "Kurumsal Kanal B2B"], ["Sabah brifingi", "Optimal fiyat", "Kurum ekleme"]),
            ("🛡️ Kayip Kalkani", "3 savunma motoru", ["5 Dakika Kurali", "Veli Parmak Izi", "Son Mil Gumruk"], ["War Room", "Cakisma kontrol", "Checklist takibi"]),
        ],
        "otomasyonlar": [
            ("👋 Yeni Aday Karsilama", "yeni_aday", "5dk + 2sa + 1gun karsilama mesajlari"),
            ("🤝 Gorusme Sonrasi Tesekkur", "gorusme_tamamlandi", "1sa + 1.5sa tesekkur + brosur"),
            ("📞 Ilk Arama Cevapsiz", "arama_cevapsiz", "2sa WhatsApp + 8sa SMS"),
            ("🎉 Sozlesme Hosgeldin", "sozlesme_imzalandi", "5dk tebrikler + 1sa ders programi"),
            ("💰 Fiyat Anlik Teklif", "fiyat_verildi", "0dk + 1gun + 5gun + 7gun mudur karti"),
            ("📅 Randevu Onay", "randevu_alindi", "Onay + yol tarifi"),
            ("📊 Test Sonucu Rapor", "test_sonucu_kaydedildi", "AI rapor + email"),
            ("🎯 Ihtiyac Analizi Paket", "ihtiyac_analizi_tamamlandi", "Kisisel paket + email"),
            ("🎓 14 Gun Onboarding", "kesin_kayit_yapildi", "Kayit sonrasi 14 gun mikro dokunus"),
            ("⏰ Fiyat 3 Gun Hatirlatma", "fiyat_verildi_3gun", "[CRON] Fiyat verilen ve cevapsiz adaya hatirlatma"),
            ("🔄 Olumsuz 30 Gun", "olumsuz_isaretlendi_30gun", "[CRON] Olumsuz adaya 30 gun sonra geri donus"),
            ("🎂 Dogum Gunu", "dogum_gunu", "[CRON] Bugun dogum gunu olan adaya kutlama"),
            ("❄️ Isi Dustu", "isi_dustu", "[CRON] Isi seviyesi dusen adaya uyari"),
            ("⏰ Randevu Yarin", "randevu_yarin", "[CRON] Randevu -1 gun hatirlatma"),
            ("🔔 Randevu 2sa Once", "randevu_2saat_oncesi", "[CRON] Son hatirlatma + adres"),
            ("🔄 Randevu Kacirildi", "randevu_kacirildi", "[CRON] Veli gelmediyse ozur + yeni randevu"),
        ],
        "arka_plan_motorlari": [
            ("Isi Hesaplama", "kayit_takip_engine.py", "Her aday icin SICAK/ILIK/SOGUK/BUZ seviyesi"),
            ("Gecikme Hesaplama", "kayit_takip_engine.py", "NORMAL/DIKKAT/ACIL/KRITIK gecikme durumu"),
            ("Eskalasyon", "kayit_takip_engine.py", "Mudur uyarisi gereken adaylari belirler"),
            ("Lookalike Motoru", "kayit_lookalike.py", "Yeni aday icin en benzer mevcut veli"),
            ("Forecast", "kayit_forecast.py", "30/60/90/180 gun kayit tahmini"),
            ("Cron Scheduler", "kayit_otomasyon.py → cron_tara()", "4 saatte 1 zaman bazli tarama"),
            ("Otomasyon Kuyrugu", "kayit_otomasyon.py", "Planli gorevlerin sirayla islenmesi"),
            ("Merge Suggestion", "kayit_veli_parmak_izi.py", "Duplicate aday tespiti (Levenshtein)"),
            ("Risk Skorlama", "kayit_sifir_kayip.py + sessiz_red.py", "0-100 skor + 72 saat alarmi"),
            ("AI Katmani", "utils/ai_rules.py", "OpenAI GPT-4o-mini + fallback"),
        ],
        "veri_dosyalari": [
            ("kayit_adaylar.json", "Tum adaylar (KayitAday listesi)"),
            ("otomasyonlar.json", "Hangi otomasyonlar aktif"),
            ("otomasyon_gorevleri.json", "Kuyrukta bekleyen gorevler"),
            ("otomasyon_log.json", "Son 1000 otomasyon olayi"),
            ("cron_meta.json", "Son cron calismasi + istatistik"),
            ("cron_isi_snapshot.json", "Isi seviyesi snapshot"),
            ("pismanlik_kayitlari.json", "Pismanlik motor log"),
            ("cocuk_sesleri.json", "Cocugun Ic Sesi anket kayitlari"),
            ("korku_yikici.json", "Korku Yikici rapor log"),
            ("gelecek_kitaplari.json", "Gelecegin Mini Kitabi log"),
            ("kisisel_urller.json", "Kisisel URL + slug kayitlari"),
            ("sube_kontenjan.json", "Sube kapasite bilgileri"),
            ("fiyat_onerileri.json", "Gelir Optimizasyon log"),
            ("kurum_musterileri.json", "B2B Kurumsal Kanal musteriler"),
            ("lead_response_log.json", "5 Dakika Kurali tracker"),
            ("son_mil_checklists.json", "Son Mil Gumruk checklist"),
        ],
        "senaryo": [
            "Sabah: Gunluk sekmesi → bekleyen adaylari ara",
            "Yeni lead: 5dk icinde yanit ver (Kayip Kalkani War Room)",
            "Randevu: arama_kaydet sonra otomatik 3 hatirlatma cron'la",
            "Gorusme: sonuc se → fiyat asamasina gec",
            "Fiyat: Gelir Optimizasyon ile optimal teklif → 4 dokunus zinciri",
            "Kararsiz: Kapanis Silahlari (Gelecegin Mini Kitabi + Korku Yikici)",
            "Sozlesme: imzala → Son Mil checklist otomatik baslar",
            "Kesin kayit: 14 gun onboarding zinciri otomatik",
        ],
    },

    "akademik_takip": {
        "ad": "Akademik Takip",
        "emoji": "📚",
        "kategori": "AKADEMIK",
        "view_dosya": "views/akademik_takip.py",
        "model_dosyalari": ["models/akademik_takip.py"],
        "aciklama": (
            "Ogrenci akademik yasam dongusunu yoneten ana modul. "
            "Yoklama, not girisi, ders programi, akademik plan, kazanim "
            "isleme takibi, etut kayitlari, odev sistemi."
        ),
        "ana_ozellikler": [
            "5 ana grup (Kadro, Ders/Program, Ogretim/Planlama, Yoklama/Notlar, Raporlar)",
            "Multi-tab yapida 8+ alt sekme",
            "Kazanim isleme ve uygulama takibi",
            "Yillik/aylik/haftalik plan sistemi",
            "Online odev teslim sistemi",
            "Etut/destek/telafi kaydi",
            "Karne raporu, siralama, devamsizlik",
        ],
        "tablar": [
            ("👥 Kadro & Ogrenci", "Akademik kadro + sinif listesi + ogrenci yonetimi", ["Ortak veri kaynagi"], ["Kadro tanimi", "Ogrenci ekleme"]),
            ("📅 Ders & Program", "5 alt sekmeli ders programi + zaman cizelgesi", ["Otomatik conflict check"], ["Ders saati ekleme", "Plan onayi"]),
            ("🎯 Ogretim & Planlama", "Akademik plan + uygulama takibi + ders defteri + odev", ["Kazanim auto-tracking"], ["Yillik plan", "Odev tanimi"]),
            ("📋 Yoklama & Notlar", "Yoklama (7 alt sekme) + not girisi", ["Otomatik istatistik"], ["Yoklama alma", "Not girisi"]),
            ("📊 Raporlar", "Karne, siralama, devamsizlik, ders analizi", ["Otomatik rapor olusturma"], ["Filtre + export"]),
        ],
        "otomasyonlar": [
            ("Devamsizlik Bildirim", "yoklama_alindi", "Veliye SMS/WhatsApp ile devamsizlik bildirim"),
            ("Not Bildirimi", "not_kaydedildi", "Veliye yeni not bildirim"),
            ("Odev Hatirlatma", "odev_son_tarihi", "Tesimat tarihinden 1 gun once veliye hatirlatma"),
            ("Karne Hazir", "donem_sonu", "Karne hazir oldugunda veliye PDF gonderim"),
        ],
        "arka_plan_motorlari": [
            ("Kazanim Tracker", "akademik_takip.py", "Hangi kazanim islendi/islenmedi"),
            ("Devamsizlik Hesaplayici", "akademik_takip.py", "Yarim/tam gun, ozursuz/ozurlu hesabi"),
            ("Not Ortalama Motoru", "akademik_takip.py", "Yazili/sozlu/proje agirlikli ortalama"),
            ("Konu Plan Optimizer", "akademik_takip.py", "Yillik plana gore haftalik konu dagitimi"),
        ],
        "veri_dosyalari": [
            ("students.json", "Ogrenci kayitlari"),
            ("grades.json", "Notlar"),
            ("attendance.json", "Devamsizlik kayitlari"),
            ("schedule.json", "Ders programi"),
            ("teachers.json", "Ogretmenler"),
            ("academic_plans.json", "Yillik/aylik/haftalik planlar"),
            ("kazanim_isleme.json", "Kazanim islenme kaydi"),
            ("olcme_takvim.json", "Olcme takvimi"),
            ("etut_kayitlari.json", "Etut/destek dersleri"),
        ],
        "senaryo": [
            "Sabah: Yoklama al → devamsizlik velilere bildirilir",
            "Ders: Kazanim isleme kaydet → yillik plan ilerlesin",
            "Sinav sonrasi: Not gir → veliye otomatik bildirim",
            "Hafta sonu: Akademik plan kontrol et",
            "Donem sonu: Karne PDF olustur → veliye gonder",
        ],
    },

    "olcme_degerlendirme": {
        "ad": "Olcme ve Degerlendirme",
        "emoji": "📝",
        "kategori": "AKADEMIK",
        "view_dosya": "views/olcme_degerlendirme_v2.py",
        "model_dosyalari": ["models/olcme_degerlendirme.py"],
        "aciklama": (
            "Kazanim → Soru → Sinav → Ogrenci → Sonuc tam yasam dongusu. "
            "AI ile soru uretimi, PDF cikarimi, online sinav, otomatik puanlama, "
            "telafi sistemi, MEB yillik plan import, OSYM/MEB sinav formati."
        ),
        "ana_ozellikler": [
            "6839 MEB yillik plan kaydi (14 ders, 1-12. sinif)",
            "AI destekli soru uretimi (5 adimli wizard)",
            "Sinav blueprint/sablon sistemi",
            "OSYM tarzi PDF uretici (2 sutunlu, profesyonel)",
            "Online sinav (ogrenci girisi, otomatik puanlama)",
            "Stok kontrol (otomatik soru uretimi ile doldurma)",
            "Telafi sistemi (RED/YELLOW/GREEN/BLUE renk bandi)",
            "Adaptif test (CAT, IRT 1-2-3 PL)",
            "QTI 2.1 import/export",
        ],
        "tablar": [
            ("🎯 Kazanim Yonetimi", "Kazanimlarin CRUD + import", [], []),
            ("❓ Soru Olusturma", "5 adim sihirbaz", ["Kalite degerlendirme"], ["Manuel/AI"]),
            ("📚 Soru Bankasi", "Tum sorular + filtre + ay secimi", [], []),
            ("📋 Sinav Sablonu", "Blueprint olusturma", ["20 kademe sablon"], []),
            ("🎓 Sinav Uretici", "Blueprint'ten sinav uretimi", ["Otomatik secim"], []),
            ("🧪 Online Sinav", "Ogrenci sinava girer", ["Otomatik puanlama"], []),
            ("📊 Sonuc Analizi", "Istatistik + zorluk + siralama", [], []),
            ("📄 PDF Sinav Export", "Profesyonel PDF cikar", ["OSYM tarzi"], []),
            ("📥 PDF Soru Cikarma", "PDF'den AI ile soru cikar", [], []),
            ("📅 MEB Yillik Plan", "6839 kayit import", [], []),
            ("🤖 AI Soru Uretimi", "Kazanim bazli", [], []),
            ("📦 Stok Kontrol", "Otomatik doldurma", [], []),
            ("🔄 Telafi", "RED/YELLOW/GREEN/BLUE", ["AutoGrader entegre"], []),
        ],
        "otomasyonlar": [
            ("Sinav Sonucu Velilere", "sinav_tamamlandi", "Sonuc PDF + yorum"),
            ("Telafi Olustur", "dusuk_basari", "Otomatik telafi gorevi"),
            ("Stok Doldur", "stok_dustu", "AI ile yeni soru uretimi"),
        ],
        "arka_plan_motorlari": [
            ("AutoGrader", "olcme_degerlendirme.py", "Otomatik puanlama + telafi tetikleyici"),
            ("DistractorAnalyzer", "olcme_degerlendirme.py", "Celdirici etkinlik analizi"),
            ("CATEngine", "olcme_degerlendirme.py", "Computerized Adaptive Testing"),
            ("IRT 1/2/3 PL", "olcme_degerlendirme.py", "Madde Tepki Kurami modelleri"),
            ("PsikometrikAnaliz", "olcme_degerlendirme.py", "Madde analizi"),
            ("StockController", "olcme_degerlendirme.py", "Soru stogu kontrol + doldurma"),
            ("RemediationEngine", "olcme_degerlendirme.py", "Telafi gorevi olusturucu"),
        ],
        "veri_dosyalari": [
            ("outcomes.json", "Kazanimlar"),
            ("questions.json", "Sorular"),
            ("blueprints.json", "Sinav sablonlari"),
            ("exams.json", "Sinavlar"),
            ("sessions.json", "Sinav oturumlari"),
            ("answers.json", "Ogrenci cevaplari"),
            ("results.json", "Sonuclar"),
            ("annual_plans.json", "6839 MEB yillik plan kaydi"),
            ("telafi_tasks.json", "Telafi gorevleri"),
            ("stok_raporlari.json", "Stok kontrol raporlari"),
        ],
        "senaryo": [
            "Yillik plan import → 6839 MEB kazanimi sisteme yuklenir",
            "Kazanim sec → AI ile 5 adimda soru uret",
            "Sablon olustur → sinav otomatik uretilir",
            "Online sinav → ogrenciler cevaplar",
            "Sonuclar otomatik puanlanir → telafi tetiklenir",
            "Stok dusukse otomatik soru uretimi calisir",
        ],
    },

    "rehberlik": {
        "ad": "Rehberlik",
        "emoji": "🧠",
        "kategori": "AKADEMIK",
        "view_dosya": "views/rehberlik.py",
        "model_dosyalari": ["models/rehberlik.py"],
        "aciklama": "Rehberlik servisi yonetim sistemi — gorusme, test, mudahale, raporlama.",
        "ana_ozellikler": [
            "Bireysel/grup gorusme kayitlari",
            "Test uygulama ve sonuc analizi",
            "Mudahale plani",
            "Raporlama ve PDF cikti",
            "Veli rehberlik gorusmeleri",
        ],
        "tablar": [
            ("👨‍🎓 Ogrenci Listesi", "Tum ogrenciler", [], []),
            ("📋 Gorusme Kayitlari", "Rehberlik gorusmeleri", [], []),
            ("🧪 Test Uygulama", "Psikometrik testler", [], []),
            ("📊 Raporlar", "Detayli raporlar", [], []),
        ],
        "otomasyonlar": [
            ("Gorusme Hatirlatma", "randevu_yaklasiyor", "Ogrenci/veliye hatirlatma"),
        ],
        "arka_plan_motorlari": [
            ("Risk Tespit", "rehberlik.py", "Erken uyari sinyalleri"),
        ],
        "veri_dosyalari": [
            ("rehberlik_gorusmeler.json", "Gorusme kayitlari"),
            ("rehberlik_testler.json", "Test sonuclari"),
        ],
        "senaryo": [
            "Ogrenci sec → gorusme kaydi olustur",
            "Test uygula → sonuclari incele",
            "Mudahale planı olustur",
            "Veliye rapor PDF gonder",
        ],
    },

    "insan_kaynaklari": {
        "ad": "Insan Kaynaklari Yonetimi",
        "emoji": "👥",
        "kategori": "KURUM",
        "view_dosya": "views/insan_kaynaklari.py",
        "model_dosyalari": ["models/insan_kaynaklari.py"],
        "aciklama": "Personel/ogretmen yonetimi — ozluk, izin, performans, bordro, egitim.",
        "ana_ozellikler": [
            "Personel kayit ve ozluk yonetimi",
            "Izin/devamsizlik takibi",
            "Performans degerlendirme",
            "Maas/bordro hesabi",
            "Egitim ve gelisim takibi",
            "Pozisyon ve hiyerarsi",
        ],
        "tablar": [
            ("👤 Personel Listesi", "Tum personeli gor", [], ["Yeni personel ekleme"]),
            ("📋 Ozluk", "Personel ozluk dosyalari", [], ["Belge ekleme"]),
            ("🗓️ Izinler", "Izin yonetimi", [], ["Izin onayi"]),
            ("📊 Performans", "Yillik degerlendirme", [], []),
            ("💰 Bordro", "Maas hesabi", [], []),
            ("🎓 Egitim", "Mesleki gelisim", [], []),
        ],
        "otomasyonlar": [
            ("Dogum Gunu", "personel_dogum_gunu", "Personel dogum gunu kutlama"),
            ("Izin Bitti", "izin_bitis", "Izin biten personele hatirlatma"),
        ],
        "arka_plan_motorlari": [
            ("Bordro Hesaplayici", "insan_kaynaklari.py", "Otomatik maas hesabi"),
        ],
        "veri_dosyalari": [
            ("personel.json", "Personel kayitlari"),
            ("izinler.json", "Izin kayitlari"),
            ("bordro.json", "Maas/bordro"),
        ],
        "senaryo": [
            "Yeni personel ekle → ozluk olusur",
            "Izin talep al → onayla → kayit duser",
            "Ay sonu → bordro otomatik hesaplanir",
        ],
    },

    "randevu_ziyaretci": {
        "ad": "Randevu ve Ziyaretci",
        "emoji": "📅",
        "kategori": "KURUM",
        "view_dosya": "views/randevu_ziyaretci.py",
        "model_dosyalari": ["models/randevu_ziyaretci.py"],
        "aciklama": "Randevu yonetimi + ziyaretci giris/cikis + raporlar. 6 sekmeli kurumsal modul.",
        "ana_ozellikler": [
            "Online randevu sistemi",
            "Ziyaretci giris/cikis kayit",
            "Gorusulecek unvan/kisi yonetimi",
            "Ziyaretci rehberi",
            "Raporlar ve istatistikler",
        ],
        "tablar": [
            ("📊 Dashboard", "Genel durum", [], []),
            ("📋 Randevu Yonetimi", "Randevu CRUD", [], ["Yeni randevu", "Onay/red"]),
            ("🚪 Ziyaretci Giris/Cikis", "Anlik kayit", [], ["Giris yap", "Cikis yap"]),
            ("📖 Ziyaretci Rehberi", "Tum ziyaretciler", [], []),
            ("📊 Raporlar", "Istatistikler", [], []),
            ("⚙️ Ayarlar", "Modul ayarlari", [], []),
        ],
        "otomasyonlar": [
            ("Randevu Hatirlatma", "randevu_yarin", "Ziyaretciye SMS/email"),
        ],
        "arka_plan_motorlari": [
            ("Ziyaretci Profil Eslesme", "randevu_ziyaretci.py", "IK pozisyonlari ile eslestirme"),
        ],
        "veri_dosyalari": [
            ("randevular.json", "Randevu kayitlari"),
            ("ziyaretciler.json", "Ziyaretci giris/cikis"),
        ],
        "senaryo": [
            "Veli randevu talebi -> sistemde olusur",
            "Onayla -> hatirlatma planlanir",
            "Geldiginde -> giris yap",
            "Gittiginde -> cikis yap",
        ],
    },

    "kim_organizational": {
        "ad": "Kurumsal Organizasyon ve Iletisim",
        "emoji": "🏢",
        "kategori": "KURUM",
        "view_dosya": "views/kim_organizational.py",
        "model_dosyalari": ["models/kim_organizational.py"],
        "aciklama": "Kurum profili, organizasyon semasi, iletisim merkezi, sinif listeleri, ortak veri havuzu.",
        "ana_ozellikler": [
            "Kurum profili (ad, adres, logo, telefon)",
            "Organizasyon semasi (departmanlar, hiyerarsi)",
            "Sinif listeleri (TUM modullerin paylasilan kaynagi)",
            "Iletisim merkezi (toplu duyuru)",
            "Veli/ogrenci ortak veritabani",
        ],
        "tablar": [
            ("🏢 Kurum Profili", "Temel bilgiler", [], ["Logo, adres, telefon"]),
            ("🗂️ Organizasyon Semasi", "Departman/hiyerarsi", [], ["Birim ekleme"]),
            ("📋 Sinif Listeleri", "Tum siniflar (MERKEZI)", [], ["Ogrenci ekleme/yer degistirme"]),
            ("📞 Iletisim Merkezi", "Toplu mesaj", [], ["Hedef grup", "Mesaj yazma"]),
        ],
        "otomasyonlar": [
            ("Yeni Donem Hatirlatma", "donem_baslangici", "Tum velilere bilgilendirme"),
        ],
        "arka_plan_motorlari": [
            ("Veri Senkronizasyon", "kim_organizational.py", "Diger modullerin paylasilan veriyi cekmesi"),
        ],
        "veri_dosyalari": [
            ("kurum_profili.json", "Kurum bilgileri"),
            ("siniflar.json", "Tum siniflar/subeler"),
            ("ogrenciler.json", "Tum ogrenciler"),
            ("veliler.json", "Tum veliler"),
        ],
        "senaryo": [
            "Kurum profili doldur",
            "Sinif listelerini ekle (tum modullerin temeli)",
            "Toplu duyuru gonder",
        ],
    },

    "sosyal_medya": {
        "ad": "Sosyal Medya Yonetimi",
        "emoji": "📱",
        "kategori": "KURUM",
        "view_dosya": "views/sosyal_medya.py",
        "model_dosyalari": ["models/sosyal_medya.py"],
        "aciklama": "Sosyal medya icerik planlama, paylasim takvimi, etkilesim takibi, AI icerik uretimi.",
        "ana_ozellikler": [
            "Icerik takvimi (Instagram/Facebook/X/TikTok)",
            "AI ile post metni + hashtag uretimi",
            "Gorsel/video kutuphanesi",
            "Etkilesim metrikleri",
            "Reklam butce takibi",
        ],
        "tablar": [
            ("📅 Takvim", "Aylik icerik plani", [], []),
            ("✏️ Yeni Post", "AI destekli olusturma", [], []),
            ("📊 Etkilesim", "Begeni/yorum/paylasim", [], []),
            ("💰 Reklam", "Butce + ROI", [], []),
        ],
        "otomasyonlar": [
            ("Otomatik Paylasim", "planlanan_zaman", "Zamanli post"),
        ],
        "arka_plan_motorlari": [
            ("AI Hashtag Uretici", "sosyal_medya.py", "Trend hashtagler"),
        ],
        "veri_dosyalari": [
            ("postlar.json", "Tum paylasimlar"),
            ("etkilesim.json", "Metrik kayitlari"),
        ],
        "senaryo": [
            "Aylik plan olustur",
            "AI ile post metni uret",
            "Zamanlanmis paylasim",
            "Etkilesimi izle",
        ],
    },

    "butce_gelir_gider": {
        "ad": "Butce Gelir Gider",
        "emoji": "💰",
        "kategori": "KURUM",
        "view_dosya": "views/butce_gelir_gider.py",
        "model_dosyalari": ["models/butce_gelir_gider.py"],
        "aciklama": "Okul finans yonetimi — butce, gelir, gider, fatura, raporlar, banka entegrasyonu.",
        "ana_ozellikler": [
            "Yillik butce planlama",
            "Gelir/gider kategorileri",
            "Fatura ve makbuz yonetimi",
            "Veli odeme takibi",
            "Raporlar (gelir/gider/karne)",
            "Banka entegrasyon hazirligi",
        ],
        "tablar": [
            ("📊 Dashboard", "Finansal ozet", [], []),
            ("💰 Gelir", "Veli odemeleri + diger gelirler", [], ["Tahsilat girisi"]),
            ("💸 Gider", "Tum giderler", [], ["Gider girisi"]),
            ("📋 Faturalar", "Fatura yonetimi", [], []),
            ("📊 Raporlar", "Aylik/yillik raporlar", [], []),
            ("📅 Butce", "Yillik plan", [], []),
        ],
        "otomasyonlar": [
            ("Odeme Hatirlatma", "vade_yaklasiyor", "Veliye otomatik hatirlatma"),
            ("Gecikmis Odeme", "vade_gecti", "Eskalasyon"),
        ],
        "arka_plan_motorlari": [
            ("Tahsilat Tracker", "butce_gelir_gider.py", "Veli odeme durumu"),
            ("Butce Sapma", "butce_gelir_gider.py", "Plan vs gerceklesen"),
        ],
        "veri_dosyalari": [
            ("gelirler.json", "Gelir kayitlari"),
            ("giderler.json", "Gider kayitlari"),
            ("faturalar.json", "Fatura listesi"),
            ("butce.json", "Yillik butce plani"),
        ],
        "senaryo": [
            "Yillik butce plani olustur",
            "Veli odemelerini kaydet",
            "Gider girisi yap",
            "Aylik rapor olustur",
        ],
    },

    "toplanti_kurullar": {
        "ad": "Toplanti ve Kurullar",
        "emoji": "🤝",
        "kategori": "KURUM",
        "view_dosya": "views/toplanti_kurullar.py",
        "model_dosyalari": ["models/toplanti_kurullar.py"],
        "aciklama": "Kurul/toplanti yonetimi — kararlar, gundem, katilim, tutanak, takip.",
        "ana_ozellikler": [
            "Kurul/komite tanimlama",
            "Gundem hazirlama",
            "Toplanti tutanak ve kararlar",
            "Karar takip ve uygulama",
            "Katilim listesi",
        ],
        "tablar": [
            ("📋 Kurullar", "Kurul listesi", [], []),
            ("📅 Toplantilar", "Toplanti planlama", [], []),
            ("📝 Tutanaklar", "Toplanti tutanaklari", [], []),
            ("✅ Kararlar", "Karar takibi", [], []),
        ],
        "otomasyonlar": [
            ("Toplanti Hatirlatma", "toplanti_yarin", "Katilimcilara"),
        ],
        "arka_plan_motorlari": [
            ("Karar Takip", "toplanti_kurullar.py", "Karar uygulama izleme"),
        ],
        "veri_dosyalari": [
            ("kurullar.json", "Kurul tanimlari"),
            ("toplantilar.json", "Toplanti kayitlari"),
            ("kararlar.json", "Kararlar"),
        ],
        "senaryo": [
            "Kurul olustur → uyeler ekle",
            "Toplanti planla → gundem hazirla",
            "Tutanak yaz → kararlar olustur",
            "Karar takibi → uygulama kontrol",
        ],
    },

    "kurum_hizmetleri": {
        "ad": "Kurum Hizmetleri",
        "emoji": "🏛️",
        "kategori": "KURUM",
        "view_dosya": "views/kurum_hizmetleri.py",
        "model_dosyalari": ["models/kurum_hizmetleri.py"],
        "aciklama": "Servis, yemekhane, kantin, kiyafet gibi yan hizmetlerin yonetimi.",
        "ana_ozellikler": [
            "Servis guzergah ve takip",
            "Yemekhane menu yonetimi",
            "Kantin satis takibi",
            "Kiyafet siparis",
            "Hizmet ucret takibi",
        ],
        "tablar": [
            ("🚌 Servis", "Guzergahlar", [], []),
            ("🍽️ Yemekhane", "Menu + ucret", [], []),
            ("🏪 Kantin", "Satislar", [], []),
            ("👔 Kiyafet", "Siparis", [], []),
        ],
        "otomasyonlar": [
            ("Servis Iptali", "servis_iptal", "Veliye bildirim"),
        ],
        "arka_plan_motorlari": [
            ("Guzergah Optimizer", "kurum_hizmetleri.py", "En kisa rota"),
        ],
        "veri_dosyalari": [
            ("servisler.json", "Servis bilgileri"),
            ("menuler.json", "Yemek menusu"),
            ("kantin.json", "Kantin satislari"),
        ],
        "senaryo": [
            "Servis guzergahi tanimla",
            "Yemek menusu hazirla",
            "Kantin satisi kaydet",
        ],
    },

    "ogrenci_360": {
        "ad": "Ogrenci 360",
        "emoji": "📊",
        "kategori": "AKADEMIK",
        "view_dosya": "views/ogrenci_360.py",
        "model_dosyalari": ["models/ogrenci_360.py"],
        "aciklama": "Ogrenci icin 360 derece tum bilgi ekrani — akademik, sosyal, davranis, saglik, aile.",
        "ana_ozellikler": [
            "Tek ekranda ogrencinin tum profili",
            "Akademik basari grafikleri",
            "Devamsizlik trendi",
            "Davranis kayitlari",
            "Saglik bilgisi",
            "Aile bilgileri",
            "AI ile kisilik analizi",
        ],
        "tablar": [
            ("📋 Profil", "Temel bilgiler", [], []),
            ("📊 Akademik", "Notlar + grafik", [], []),
            ("🎯 Davranis", "Davranis kayitlari", [], []),
            ("🏥 Saglik", "Saglik gecmisi", [], []),
            ("👨‍👩‍👧 Aile", "Veli/aile bilgileri", [], []),
            ("🤖 AI Analiz", "Kisilik + tahmin", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [
            ("Profil Birlestirici", "ogrenci_360.py", "Tum modullerden veri toplama"),
        ],
        "veri_dosyalari": [
            ("ogrenci_360_cache.json", "Cached profile data"),
        ],
        "senaryo": [
            "Ogrenci sec",
            "Tum profili tek ekranda gor",
            "AI analiz al",
        ],
    },

    "okul_oncesi_ilkokul": {
        "ad": "Okul Oncesi - Ilkokul",
        "emoji": "🎨",
        "kategori": "AKADEMIK",
        "view_dosya": "views/okul_oncesi_ilkokul.py",
        "model_dosyalari": [],
        "aciklama": "Okul oncesi ve ilkokul kademesine ozel egitim materyalleri ve oyunlar.",
        "ana_ozellikler": [
            "Yas grubuna ozel egitim icerigi",
            "Etkinlik ve oyun arsivi",
            "Hazirbulunusluk testleri",
            "Veli rehberligi",
        ],
        "tablar": [
            ("🎮 Oyunlar", "Egitsel oyunlar", [], []),
            ("📚 Etkinlikler", "Etkinlik arsivi", [], []),
            ("🧪 Testler", "Hazirbulunusluk", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Yas grubu sec",
            "Etkinlik bul",
            "Sinifa uygula",
        ],
    },

    "akademik_takvim": {
        "ad": "Akademik Takvim",
        "emoji": "📅",
        "kategori": "AKADEMIK",
        "view_dosya": "views/akademik_takvim.py",
        "model_dosyalari": ["models/akademik_takvim.py"],
        "aciklama": "Yillik akademik takvim — tatiller, sinavlar, etkinlikler, donem tarihleri.",
        "ana_ozellikler": [
            "MEB takvimi import",
            "Ozel etkinlikler",
            "Sinav takvimi",
            "Toplanti tarihleri",
            "Tatil donemleri",
        ],
        "tablar": [
            ("📅 Takvim", "Yillik gorunum", [], []),
            ("➕ Etkinlik Ekle", "Yeni etkinlik", [], []),
            ("📋 Liste", "Tum etkinlik listesi", [], []),
        ],
        "otomasyonlar": [
            ("Etkinlik Hatirlatma", "etkinlik_yarin", "Velilere bildirim"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("takvim.json", "Etkinlikler"),
        ],
        "senaryo": [
            "Yillik takvim olustur",
            "Etkinlik ekle",
            "Velilere paylas",
        ],
    },

    "okul_sagligi": {
        "ad": "Okul Sagligi Takip",
        "emoji": "🏥",
        "kategori": "AKADEMIK",
        "view_dosya": "views/okul_sagligi.py",
        "model_dosyalari": ["models/okul_sagligi.py"],
        "aciklama": "Ogrenci saglik bilgisi yonetimi — asilar, alerjiler, ilac, ilkyardim, doktor randevu.",
        "ana_ozellikler": [
            "Ogrenci saglik dosyasi",
            "Asi takibi",
            "Alerji ve kronik hastalik",
            "Ilac kullanim",
            "Ilkyardim olaylari",
            "Doktor randevu kayit",
        ],
        "tablar": [
            ("👤 Saglik Dosyasi", "Ogrenci profili", [], []),
            ("💉 Asi", "Asi takvimi", [], []),
            ("⚠️ Alerji", "Alerji listesi", [], []),
            ("💊 Ilac", "Ilac kullanim", [], []),
            ("🚑 Ilkyardim", "Olay kayitlari", [], []),
        ],
        "otomasyonlar": [
            ("Asi Hatirlatma", "asi_zamani", "Veliye SMS"),
        ],
        "arka_plan_motorlari": [
            ("Asi Tracker", "okul_sagligi.py", "Eksik asi tespit"),
        ],
        "veri_dosyalari": [
            ("saglik.json", "Saglik kayitlari"),
            ("asilar.json", "Asi gecmisi"),
            ("ilkyardim.json", "Olaylar"),
        ],
        "senaryo": [
            "Yeni ogrenci -> saglik dosyasi olustur",
            "Asi zamani gelince hatirlat",
            "Olay yasandiginda kayit",
        ],
    },

    "sosyal_etkinlik": {
        "ad": "Sosyal Etkinlik ve Kulupler",
        "emoji": "🎭",
        "kategori": "AKADEMIK",
        "view_dosya": "views/sosyal_etkinlik.py",
        "model_dosyalari": ["models/sosyal_etkinlik.py"],
        "aciklama": "Kulup ve sosyal etkinlik yonetimi — uyelik, etkinlik plani, devamsizlik.",
        "ana_ozellikler": [
            "Kulup tanimlama (resim, satranc, tiyatro, vs)",
            "Uyelik yonetimi",
            "Etkinlik plani",
            "Devamsizlik takibi",
            "Yil sonu sergi/gosteri",
        ],
        "tablar": [
            ("📋 Kulupler", "Tum kulupler", [], []),
            ("👥 Uyeler", "Kulup uyeleri", [], []),
            ("📅 Etkinlikler", "Etkinlik plani", [], []),
            ("📊 Raporlar", "Katilim raporu", [], []),
        ],
        "otomasyonlar": [
            ("Etkinlik Hatirlatma", "etkinlik_yarin", "Uyelere bildirim"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("kulupler.json", "Kulup listesi"),
            ("uyelikler.json", "Uyelik kayitlari"),
        ],
        "senaryo": [
            "Kulup tanimla",
            "Ogrencileri kayit et",
            "Etkinlik planla",
        ],
    },

    "kutuphane": {
        "ad": "Kutuphane",
        "emoji": "📖",
        "kategori": "AKADEMIK",
        "view_dosya": "views/kutuphane.py",
        "model_dosyalari": ["models/kutuphane.py"],
        "aciklama": "Okul kutuphane yonetimi — kitap envanteri, odunc, iade, gecikme, raporlar.",
        "ana_ozellikler": [
            "Kitap envanteri (ISBN, kategori, raf)",
            "Odunc/iade takibi",
            "Gecikme uyarisi",
            "Cok okuyan ogrenci raporu",
            "Yeni kitap satin alma planlamasi",
        ],
        "tablar": [
            ("📚 Envanter", "Tum kitaplar", [], []),
            ("📤 Odunc Ver", "Odunc islemi", [], []),
            ("📥 Iade Al", "Iade islemi", [], []),
            ("⏰ Gecikme", "Gecikmis kitaplar", [], []),
            ("📊 Raporlar", "Istatistikler", [], []),
        ],
        "otomasyonlar": [
            ("Iade Hatirlatma", "iade_yaklasiyor", "Ogrenciye bildirim"),
            ("Gecikme Uyari", "gecikme_olustu", "Veliye uyari"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("kitaplar.json", "Kitap envanteri"),
            ("odunc.json", "Odunc kayitlari"),
        ],
        "senaryo": [
            "Kitap envantere ekle",
            "Ogrenciye odunc ver",
            "Iade aldiginda guncelle",
            "Gecikme uyarilari otomatik",
        ],
    },

    "dijital_kutuphane": {
        "ad": "Dijital Kutuphane",
        "emoji": "📱",
        "kategori": "AKADEMIK",
        "view_dosya": "views/dijital_kutuphane.py",
        "model_dosyalari": [],
        "aciklama": "PDF/eBook kutuphanesi, AI ozet, kisisellestirilmis oneri, online okuma.",
        "ana_ozellikler": [
            "PDF/EPUB kutuphane",
            "AI kitap ozeti",
            "Kisilestirilmis oneri",
            "Online okuma",
            "Okuma takibi",
        ],
        "tablar": [
            ("📚 Kutuphane", "Tum eBookler", [], []),
            ("🔍 Ara", "AI destekli arama", [], []),
            ("📊 Onerilen", "Sana ozel", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [
            ("AI Oneri Motoru", "dijital_kutuphane.py", "Okuma gecmisinden oneri"),
        ],
        "veri_dosyalari": [
            ("ebooks.json", "Dijital kitaplar"),
        ],
        "senaryo": [
            "eBook ekle",
            "Ogrenciler okuyabilsin",
            "AI oneri al",
        ],
    },

    "ai_bireysel_egitim": {
        "ad": "AI Bireysel Egitim",
        "emoji": "🎓",
        "kategori": "AKADEMIK",
        "view_dosya": "views/ai_bireysel_egitim.py",
        "model_dosyalari": [],
        "aciklama": "Her ogrenci icin AI destekli kisisellestirilmis egitim plani + adaptif sorular.",
        "ana_ozellikler": [
            "Her ogrenci icin oz egitim plani",
            "Adaptif soru sistemi",
            "Zayif konularda yogunlasma",
            "Ilerlemenin gorsel takibi",
            "Veli paylasimi",
        ],
        "tablar": [
            ("👤 Ogrenci Profili", "Egitim profili", [], []),
            ("🎯 Plan", "AI plan", [], []),
            ("❓ Adaptif Sorular", "Akilli sorular", [], []),
            ("📊 Ilerleme", "Grafikler", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [
            ("Adaptif Algoritma", "ai_bireysel_egitim.py", "Soru zorluk ayarlama"),
        ],
        "veri_dosyalari": [
            ("ai_planlar.json", "Egitim planlari"),
        ],
        "senaryo": [
            "Ogrenci sec",
            "AI ile plan olustur",
            "Adaptif sorular cozdur",
            "Ilerlemenin gorsel takibi",
        ],
    },

    "yabanci_dil": {
        "ad": "Yabanci Dil",
        "emoji": "🌍",
        "kategori": "AKADEMIK",
        "view_dosya": "views/yabanci_dil.py",
        "model_dosyalari": [],
        "aciklama": "Yabanci dil egitim modulu — Ingilizce/Almanca/Fransizca/Italyanca/Ispanyolca destekli.",
        "ana_ozellikler": [
            "5 dil destegi",
            "Seviye tespit (CEFR)",
            "Premium AI ile sohbet",
            "Kelime kitapcigi",
            "Dilbilgisi modul",
            "Gunluk pratik",
        ],
        "tablar": [
            ("🌐 Dil Sec", "Calisilacak dil", [], []),
            ("🎯 Seviye Test", "CEFR test", [], []),
            ("💬 AI Sohbet", "Premium chat", [], []),
            ("📚 Kelime", "Kelime calismasi", [], []),
            ("📝 Dilbilgisi", "Gramer", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Dil sec",
            "Seviye testi yap",
            "Gunluk pratik",
            "AI ile sohbet",
        ],
    },

    "kisisel_dil_gelisimi": {
        "ad": "Kisisel Dil Gelisimi",
        "emoji": "🎓",
        "kategori": "AKADEMIK",
        "view_dosya": "views/kisisel_dil_gelisimi.py",
        "model_dosyalari": [],
        "aciklama": "Turkce dil gelisimi — kelime hazinesi, anlam bilgisi, yazim, kompozisyon.",
        "ana_ozellikler": [
            "Kelime hazinesi gelistirme",
            "Anlam bilgisi calismasi",
            "Yazim ve noktalama",
            "Kompozisyon yardimcisi",
            "AI yazim duzeltme",
        ],
        "tablar": [
            ("📖 Kelime", "Kelime havuzu", [], []),
            ("✏️ Yazim", "Yazim kurali", [], []),
            ("📝 Kompozisyon", "AI destekli", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Kelime calismasi",
            "Yazim alistirmasi",
            "AI ile kompozisyon",
        ],
    },

    "erken_uyari": {
        "ad": "Erken Uyari Sistemi",
        "emoji": "🧠",
        "kategori": "AKADEMIK",
        "view_dosya": "views/erken_uyari.py",
        "model_dosyalari": [],
        "aciklama": "Akademik/sosyal/davranissal risk sinyallerini erken tespit eden AI sistemi.",
        "ana_ozellikler": [
            "Devamsizlik riski",
            "Akademik dusus tespiti",
            "Davranis sinyalleri",
            "Sosyal izolasyon uyarisi",
            "Aile sorunlari sezimi",
            "Mudahale onerileri",
        ],
        "tablar": [
            ("🚨 Aktif Uyarilar", "Su anki risk listesi", [], []),
            ("📊 Trend Analizi", "Zaman serisi", [], []),
            ("🛠️ Mudahale", "Onerilen aksiyonlar", [], []),
        ],
        "otomasyonlar": [
            ("Risk Bildirim", "risk_skor_yukseldi", "Rehbere bildirim"),
        ],
        "arka_plan_motorlari": [
            ("Risk Skorlama", "erken_uyari.py", "ML/heuristik bazli skor"),
            ("Trend Tespit", "erken_uyari.py", "Zaman serisi sapma"),
        ],
        "veri_dosyalari": [
            ("uyarilar.json", "Aktif uyarilar"),
            ("mudahaleler.json", "Mudahale kayitlari"),
        ],
        "senaryo": [
            "Sistem otomatik tarar",
            "Risk yuksek aday tespit",
            "Rehbere bildirim",
            "Mudahale baslatilir",
        ],
    },

    "egitim_koclugu": {
        "ad": "Egitim Koclugu",
        "emoji": "🏅",
        "kategori": "AKADEMIK",
        "view_dosya": "views/egitim_koclugu.py",
        "model_dosyalari": [],
        "aciklama": "Bireysel egitim kocluk sistemi — hedef belirleme, plan, takip, basari odulleri.",
        "ana_ozellikler": [
            "Hedef belirleme",
            "Aksiyon plani",
            "Haftalik takip",
            "Basari rozetleri",
            "Veli paylasimi",
        ],
        "tablar": [
            ("🎯 Hedefler", "Yillik hedef", [], []),
            ("📋 Plan", "Haftalik plan", [], []),
            ("📊 Takip", "Ilerleme", [], []),
            ("🏆 Rozetler", "Basarilar", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("kocluk_planlari.json", "Plan kayitlari"),
        ],
        "senaryo": [
            "Hedef belirle",
            "Plan olustur",
            "Haftalik takip yap",
        ],
    },

    "bilgi_treni": {
        "ad": "AI Treni",
        "emoji": "🚂",
        "kategori": "AKADEMIK",
        "view_dosya": "views/bilgi_treni.py",
        "model_dosyalari": [],
        "aciklama": "Cocuklar icin AI destekli interaktif ogrenme treni — egitsel oyunlar, hikayeler, sorular.",
        "ana_ozellikler": [
            "Yas bazli icerik",
            "Interaktif hikayeler",
            "Egitsel oyunlar",
            "Soru-cevap modu",
            "Aile katilimi",
        ],
        "tablar": [
            ("🚂 Tren Yolculugu", "Ana ekran", [], []),
            ("📚 Hikayeler", "Hikaye kutuphanesi", [], []),
            ("🎮 Oyunlar", "Egitsel oyunlar", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Yas grubu sec",
            "Hikaye veya oyun sec",
            "Cocukla beraber yap",
        ],
    },

    "stem_merkezi": {
        "ad": "STEAM Merkezi",
        "emoji": "🔬",
        "kategori": "AKADEMIK",
        "view_dosya": "views/stem_merkezi.py",
        "model_dosyalari": [],
        "aciklama": "Bilim, teknoloji, muhendislik, sanat, matematik (STEAM) merkezi yonetimi.",
        "ana_ozellikler": [
            "Proje katalogu",
            "Atolye plani",
            "Malzeme envanteri",
            "Ogrenci proje takip",
            "Yarisma katilim",
        ],
        "tablar": [
            ("🔬 Projeler", "Proje listesi", [], []),
            ("🛠️ Atolyeler", "Atolye plani", [], []),
            ("📦 Malzeme", "Envanter", [], []),
            ("🏆 Yarismalar", "Katilimlar", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Proje sec",
            "Atolye planla",
            "Malzemeleri hazirla",
        ],
    },

    "tuketim_demirbas": {
        "ad": "Tuketim ve Demirbas",
        "emoji": "🗄️",
        "kategori": "OPERASYON",
        "view_dosya": "views/tuketim_demirbas.py",
        "model_dosyalari": ["models/tuketim_demirbas.py"],
        "aciklama": "Okul demirbas + tuketim malzemeleri envanter ve takip sistemi.",
        "ana_ozellikler": [
            "Demirbas envanteri (sira, masa, bilgisayar)",
            "Tuketim malzemesi (kalem, kagit, temizlik)",
            "Stok takibi",
            "Talep yonetimi",
            "Tedarikci takibi",
            "Zimmet listesi",
        ],
        "tablar": [
            ("📦 Demirbas", "Tum demirbas", [], []),
            ("🛒 Tuketim", "Tuketim malzemesi", [], []),
            ("📋 Talepler", "Talep listesi", [], []),
            ("🏪 Tedarikci", "Tedarikci listesi", [], []),
            ("📊 Raporlar", "Stok raporlari", [], []),
        ],
        "otomasyonlar": [
            ("Stok Az", "stok_dustu", "Yoneticiye uyari"),
        ],
        "arka_plan_motorlari": [
            ("Stok Tracker", "tuketim_demirbas.py", "Min stok altinda olanlari tespit"),
        ],
        "veri_dosyalari": [
            ("demirbas.json", "Demirbas envanteri"),
            ("tuketim.json", "Tuketim envanteri"),
            ("talepler.json", "Talepler"),
        ],
        "senaryo": [
            "Demirbas envantere ekle",
            "Talep al",
            "Stok takibi",
        ],
    },

    "destek_hizmetleri": {
        "ad": "Destek Hizmetleri Takip",
        "emoji": "🔧",
        "kategori": "OPERASYON",
        "view_dosya": "views/destek_hizmetleri.py",
        "model_dosyalari": ["models/destek_hizmetleri.py"],
        "aciklama": "Bakim, onarim, temizlik, guvenlik gibi destek hizmetlerinin takibi.",
        "ana_ozellikler": [
            "Bakim/onarim talep yonetimi",
            "Temizlik takvimi",
            "Guvenlik kayitlari",
            "Personel atama",
            "Tamamlanma takibi",
        ],
        "tablar": [
            ("🔧 Bakim", "Bakim talepleri", [], []),
            ("🧹 Temizlik", "Temizlik plani", [], []),
            ("🛡️ Guvenlik", "Guvenlik olaylari", [], []),
            ("👷 Personel", "Atama", [], []),
        ],
        "otomasyonlar": [
            ("Bakim Vakti", "periyodik_bakim", "Bakim hatirlatma"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("bakimlar.json", "Bakim kayitlari"),
            ("temizlik.json", "Temizlik plani"),
        ],
        "senaryo": [
            "Talep al",
            "Personel ata",
            "Tamamlanmayi takip et",
        ],
    },

    "sivil_savunma_isg": {
        "ad": "Sivil Savunma ve IS Guvenligi",
        "emoji": "⛑️",
        "kategori": "OPERASYON",
        "view_dosya": "views/sivil_savunma_isg.py",
        "model_dosyalari": ["models/sivil_savunma_isg.py"],
        "aciklama": "Iş guvenligi + sivil savunma — risk degerlendirme, tatbikat, egitim, kaza kayit.",
        "ana_ozellikler": [
            "Risk analizi",
            "Acil durum plani",
            "Yangin/deprem tatbikat",
            "Personel egitimi",
            "Iş kazasi kayit",
            "Yasal uyumluluk takibi",
        ],
        "tablar": [
            ("📋 Risk Analizi", "Risk degerlendirme", [], []),
            ("🚨 Acil Durum", "Plan", [], []),
            ("🔥 Tatbikat", "Tatbikat takvimi", [], []),
            ("📚 Egitimler", "Personel egitimi", [], []),
            ("⚠️ Kazalar", "Iş kazasi kayit", [], []),
        ],
        "otomasyonlar": [
            ("Tatbikat Yarin", "tatbikat_yaklasiyor", "Personel hatirlatma"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("riskler.json", "Risk kayitlari"),
            ("kazalar.json", "Kaza kayitlari"),
        ],
        "senaryo": [
            "Risk analizi yap",
            "Tatbikat planla",
            "Personel egit",
        ],
    },

    "alumni_career": {
        "ad": "Mezunlar ve Kariyer Yonetimi",
        "emoji": "🎓",
        "kategori": "OPERASYON",
        "view_dosya": "views/alumni_career.py",
        "model_dosyalari": ["models/alumni_career.py"],
        "aciklama": "Mezun takibi + kariyer destegi + universite yerlestirme + ag yonetimi.",
        "ana_ozellikler": [
            "Mezun veritabani",
            "Universite yerlestirme takibi",
            "Kariyer rehberligi",
            "Mezun ag (network)",
            "Etkinlik ve bulusma",
            "Bagis ve katki",
        ],
        "tablar": [
            ("👥 Mezunlar", "Mezun listesi", [], []),
            ("🎓 Universite", "Yerlestirme", [], []),
            ("💼 Kariyer", "Is gelisimi", [], []),
            ("🤝 Etkinlik", "Bulusmalar", [], []),
        ],
        "otomasyonlar": [
            ("Dogum Gunu", "mezun_dogum_gunu", "Kutlama mesaji"),
            ("Etkinlik Daveti", "etkinlik_planlandi", "Mezun grubuna davet"),
        ],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [
            ("mezunlar.json", "Mezun kayitlari"),
        ],
        "senaryo": [
            "Mezun ekle",
            "Universite kayit",
            "Kariyer takibi",
            "Etkinlik planla",
        ],
    },

    "ai_destek": {
        "ad": "AI Destek",
        "emoji": "🤖",
        "kategori": "SISTEM",
        "view_dosya": "views/ai_destek.py",
        "model_dosyalari": [],
        "aciklama": "Tum sistem icin merkezi AI destek noktasi — soru sor, AI cevaplar, yardim al.",
        "ana_ozellikler": [
            "Genel AI sohbet",
            "Modul rehberi",
            "Sorun giderme",
            "Ozellik onerisi",
            "Hata bildirimi",
        ],
        "tablar": [
            ("💬 Sohbet", "AI ile soru-cevap", [], []),
            ("📚 Rehber", "Modul kilavuzlari", [], []),
            ("🐛 Hata Bildirimi", "Hata gonder", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [
            ("AI Knowledge Base", "ai_destek.py", "Modul bilgi havuzu"),
        ],
        "veri_dosyalari": [],
        "senaryo": [
            "Soru sor",
            "AI'dan cevap al",
            "Yardimci linkleri kullan",
        ],
    },

    "ana_sayfa": {
        "ad": "Ana Sayfa",
        "emoji": "🏠",
        "kategori": "GENEL",
        "view_dosya": "views/ana_sayfa.py",
        "model_dosyalari": [],
        "aciklama": "Sistemin ana giris ekrani — gunluk ozet, hizli erisim, modul navigasyonu.",
        "ana_ozellikler": [
            "Gunluk ozet",
            "Hizli erisim kartlari",
            "Bildirimler",
            "Aktif moduller",
        ],
        "tablar": [
            ("🏠 Ozet", "Gunluk durum", [], []),
            ("⚡ Hizli Erisim", "Onemli moduller", [], []),
            ("🔔 Bildirimler", "Aktif uyarilar", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Sisteme gir",
            "Gunluk ozet bak",
            "Hizli erisim kullan",
        ],
    },

    "yonetim_ekran": {
        "ad": "Yonetim Tek Ekran",
        "emoji": "📊",
        "kategori": "GENEL",
        "view_dosya": "views/yonetim_ekran.py",
        "model_dosyalari": [],
        "aciklama": "Mudur/sahip icin tek ekranda tum sistemin stratejik gorunumu.",
        "ana_ozellikler": [
            "Tum modullerden ozet",
            "KPI metrikleri",
            "Finansal durum",
            "Akademik basari",
            "Personel durumu",
            "Aksiyon onerileri",
        ],
        "tablar": [
            ("📊 Dashboard", "Ana metrikler", [], []),
            ("💰 Finansal", "Gelir/gider", [], []),
            ("📚 Akademik", "Basari", [], []),
            ("👥 Personel", "Durum", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [],
        "veri_dosyalari": [],
        "senaryo": [
            "Sabah aç",
            "5 dakikada tum durumu gor",
            "Stratejik karar al",
        ],
    },

    "kurum_yonetimi": {
        "ad": "Kurum Yonetimi",
        "emoji": "🏛️",
        "kategori": "YONETIM",
        "view_dosya": "views/kurum_yonetimi.py",
        "model_dosyalari": ["models/kurum_yonetimi.py"],
        "aciklama": "Multi-tenant kurum yonetimi — yeni okul ekle, ayarlar, lisans, kullanici izinleri.",
        "ana_ozellikler": [
            "Yeni okul (tenant) ekleme",
            "Lisans yonetimi",
            "Kullanici/rol/izin",
            "Genel ayarlar",
            "Yedekleme",
        ],
        "tablar": [
            ("🏛️ Kurumlar", "Tum kurumlar", [], []),
            ("👥 Kullanicilar", "Yetkili kullanici", [], []),
            ("⚙️ Ayarlar", "Sistem ayarlari", [], []),
            ("💾 Yedekleme", "Veri yedek", [], []),
        ],
        "otomasyonlar": [],
        "arka_plan_motorlari": [
            ("Tenant Router", "kurum_yonetimi.py", "Multi-tenant yonlendirme"),
        ],
        "veri_dosyalari": [
            ("kurumlar.json", "Tum kurumlar"),
            ("kullanicilar.json", "Sistem kullanicilari"),
        ],
        "senaryo": [
            "Yeni kurum ekle",
            "Kullanici tanimla",
            "Izinleri ayarla",
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # YENI MODULLER (2026-04 eklenen)
    # ══════════════════════════════════════════════════════════════

    "odeme_takip": {
        "ad": "Odeme Takip",
        "emoji": "💳",
        "kategori": "KURUM YONETIMI",
        "view_dosya": "views/odeme_takip.py",
        "model_dosyalari": ["models/odeme_takip.py"],
        "aciklama": (
            "Kolej ucret yonetim sistemi. Ogrenci bazli taksit planlari, "
            "odeme kayitlari, geciken odemeler, veli borc durumu, makbuz uretimi. "
            "6 sekmeli Streamlit UI + mobil backend endpoint'leri."
        ),
        "ana_ozellikler": [
            "Otomatik taksit plani olusturma (10 taksit, ay bazli)",
            "Indirim yonetimi (kardes, basari bursu, tam burs)",
            "Geciken odeme takibi + uyari",
            "Veli borc durumu (mobil API)",
            "Ucret kalemleri CRUD (ogretim, yemek, servis, kiyafet)",
            "Sinif bazli tahsilat raporu + CSV export",
        ],
        "tablar": [
            ("Dashboard", "Toplam borc/odenen/kalan metrikleri + grafik", [], []),
            ("Taksit Planlari", "Ogrenci bazli taksit listesi + odeme alma", [], []),
            ("Ucret Kalemleri", "Donem bazli ucret tanimlari", [], []),
            ("Yeni Plan Olustur", "Ogrenci sec + otomatik taksit hesapla", [], []),
            ("Odeme Gecmisi", "Tarih/ogrenci filtreli gecmis + CSV", [], []),
            ("Raporlar", "Sinif bazli tahsilat + geciken + indirim raporu", [], []),
        ],
        "veri_dosyalari": [
            "data/odeme/taksit_planlari.json",
            "data/odeme/odeme_kayitlari.json",
            "data/odeme/ucret_kalemleri.json",
        ],
        "senaryo": [
            "Yeni ogrenci icin taksit plani olustur",
            "Taksit odemesi al (nakit/havale/kredi karti)",
            "Geciken odemeleri raporla",
        ],
    },

    "analitik_dashboard": {
        "ad": "Analitik Dashboard",
        "emoji": "📈",
        "kategori": "GENEL",
        "view_dosya": "views/analitik_dashboard.py",
        "model_dosyalari": [],
        "aciklama": (
            "Okul geneli analitik dashboard. Ogrenci performansi, devamsizlik "
            "analizi, ogretmen metrikleri, sinif karsilastirmasi. Plotly grafikleri."
        ),
        "ana_ozellikler": [
            "Genel bakis (ogrenci/ogretmen/sinif sayilari, cinsiyet dagilimi)",
            "Akademik performans (sinif ortalamasi, top 10, ders bazli)",
            "Devamsizlik analizi (sinif/gun/ay bazli trend)",
            "Ogretmen performans metrikleri",
            "Sinif karsilastirma (A vs B yan yana)",
        ],
        "tablar": [
            ("Genel Bakis", "4 metrik + grafikler", [], []),
            ("Akademik Performans", "Sinif ortalamasi + top 10", [], []),
            ("Devamsizlik Analizi", "Trend + gun bazli pattern", [], []),
            ("Ogretmen Performans", "Brans dagilimi + etkinlik", [], []),
            ("Karsilastirma", "Iki sinif yan yana", [], []),
        ],
        "senaryo": ["Donem sonu performans raporu cikar", "Iki sinifi karsilastir"],
    },

    "veli_ogretmen_gorusme": {
        "ad": "Veli-Ogretmen Gorusme",
        "emoji": "👨‍👩‍👦",
        "kategori": "ILETISIM & RANDEVU",
        "view_dosya": "views/veli_ogretmen_gorusme.py",
        "model_dosyalari": [],
        "aciklama": (
            "Veli-ogretmen gorusme randevu sistemi. Slot bazli randevu, "
            "cakisma kontrolu, gorusme notlari, puanlama, istatistik."
        ),
        "ana_ozellikler": [
            "Haftalik gorusme takvimi",
            "Ogretmen + tarih + saat slot secimi",
            "Cakisma kontrolu (ayni ogretmen ayni saat)",
            "Gorusme sonrasi puanlama (1-5 yildiz)",
            "Konu bazli istatistik (pie chart)",
        ],
        "tablar": [
            ("Gorusme Takvimi", "Bu haftanin gorusmeleri", [], []),
            ("Yeni Talep", "Randevu olusturma formu", [], []),
            ("Gecmis Gorusmeler", "Tamamlanan + notlar + puan", [], []),
            ("Istatistik", "Toplam/ortalama/konu dagilimi", [], []),
        ],
        "senaryo": ["Veli gorusme talebi olustur", "Ogretmen gorusme notu gir"],
    },

    "sertifika_uretici": {
        "ad": "Sertifika Uretici",
        "emoji": "🏆",
        "kategori": "AKADEMIK",
        "view_dosya": "views/sertifika_uretici.py",
        "model_dosyalari": [],
        "aciklama": (
            "Sertifika ve belge uretim sistemi. 7 sablon, HTML onizleme, "
            "ReportLab PDF, toplu uretim + ZIP indirme, arsiv."
        ),
        "ana_ozellikler": [
            "7 sertifika sablonu (Basari, Katilim, Tesekkur, Takdir, 1./2./3.luk)",
            "HTML onizleme + ReportLab PDF uretimi",
            "Toplu sertifika (sinif bazli)",
            "ZIP indirme",
            "Sertifika arsivi + yeniden indirme",
        ],
        "tablar": [
            ("Sertifika Olustur", "Sablon + ogrenci + onizleme + PDF", [], []),
            ("Toplu Sertifika", "Sinif sec + batch uret + ZIP", [], []),
            ("Sertifika Arsivi", "Gecmis sertifikalar + filtre + indirme", [], []),
        ],
        "senaryo": ["Donem sonu basari belgesi uret", "Tum sinifa toplu takdir belgesi"],
    },

    "servis_gps_takip": {
        "ad": "Servis GPS Takip",
        "emoji": "🚌",
        "kategori": "OKUL YASAMI",
        "view_dosya": "views/servis_gps_takip.py",
        "model_dosyalari": [],
        "aciklama": (
            "Okul servisi takip sistemi. Canli harita (st.map), guzergah CRUD, "
            "ogrenci atama, doluluk raporu."
        ),
        "ana_ozellikler": [
            "Canli konum haritasi (st.map + GPS simülasyon)",
            "Guzergah CRUD (plaka, sofor, hostes, kapasite)",
            "Ogrenci-servis atama (checkbox bazli)",
            "Doluluk orani raporu + grafik",
        ],
        "tablar": [
            ("Canli Takip", "Harita + servis kartlari + durum", [], []),
            ("Guzergah Yonetimi", "Ekle/duzenle/sil", [], []),
            ("Ogrenci Atama", "Servise ogrenci ata/cikar", [], []),
            ("Raporlar", "Doluluk + performans", [], []),
        ],
        "veri_dosyalari": ["data/akademik/servis_bilgileri.json"],
        "senaryo": ["Yeni guzergah ekle", "Ogrenci servise ata"],
    },

    "kutuphane_barkod": {
        "ad": "Kutuphane Barkod",
        "emoji": "📚",
        "kategori": "OKUL YASAMI",
        "view_dosya": "views/kutuphane_barkod.py",
        "model_dosyalari": [],
        "aciklama": (
            "Kutuphane barkod/kitap yonetim sistemi. Kitap arama, odunc verme/iade, "
            "envanter, gecikme ucreti, barkod uretici."
        ),
        "ana_ozellikler": [
            "Kitap arama (baslik, yazar, ISBN, kategori)",
            "Odunc verme + iade alma",
            "Gecikme gun + ucret hesaplama (2 TL/gun)",
            "Envanter metrikleri + kategori dagilimi",
            "Barkod etiketi uretici (print-ready)",
        ],
        "tablar": [
            ("Kitap Arama", "Arama + sonuc tablosu", [], []),
            ("Odunc Ver", "Kitap + ogrenci + tarih", [], []),
            ("Iade Al", "Odunc listesi + iade + gecikme", [], []),
            ("Envanter", "Toplam/odunc/mevcut + grafikler", [], []),
            ("Barkod Uretici", "Secilen kitaplara barkod etiketi", [], []),
        ],
        "veri_dosyalari": [
            "data/kutuphane/kitaplar.json",
            "data/kutuphane/odunc_kayitlari.json",
        ],
        "senaryo": ["Kitap odunc ver", "Geciken iadeleri raporla"],
    },

    "yemek_tercihi": {
        "ad": "Yemek Tercihi ve Alerji",
        "emoji": "🍽️",
        "kategori": "OKUL YASAMI",
        "view_dosya": "views/yemek_tercihi.py",
        "model_dosyalari": [],
        "aciklama": (
            "Ogrenci yemek tercihi ve alerji takip sistemi. Diyet turu, 11 alerjen, "
            "haftalik menu planlama, alerji cakisma kontrolu."
        ),
        "ana_ozellikler": [
            "5 diyet turu (normal, vejetaryen, vegan, glutensiz, diger)",
            "11 alerjen takibi (fistik, sut, yumurta, gluten, ...)",
            "Haftalik menu editoru (5 gun x 4 ogel)",
            "Alerji cakisma kontrolu (menu vs ogrenci alerjileri)",
            "Kritik alerji uyari kartlari",
            "CSV + text export",
        ],
        "tablar": [
            ("Tercihler", "Ogrenci listesi + diyet/alerji formu", [], []),
            ("Alerji Raporu", "Alerjen bazli sayilar + uyarilar + export", [], []),
            ("Menu Planlama", "Haftalik menu + cakisma kontrolu", [], []),
            ("Istatistik", "Diyet dagilimi + alerji grafikleri", [], []),
        ],
        "veri_dosyalari": [
            "data/yemek/ogrenci_tercihleri.json",
            "data/akademik/yemek_menusu.json",
        ],
        "senaryo": ["Ogrenci alerjisi kaydet", "Haftalik menu planla + cakisma kontrol"],
    },
}


# ============================================================
# AUTO-DISCOVERY (Registry'de yoksa AST ile cikar)
# ============================================================

def _auto_discover(modul_id: str) -> dict | None:
    """Registry'de yoksa view dosyalarini AST ile tarar."""
    aday_yollar = [
        f"views/{modul_id}.py",
        f"models/{modul_id}.py",
    ]

    bulunan_dosya = None
    for yol in aday_yollar:
        if os.path.exists(yol):
            bulunan_dosya = yol
            break

    if not bulunan_dosya:
        return None

    try:
        with open(bulunan_dosya, encoding="utf-8") as f:
            kaynak = f.read()
        agac = ast.parse(kaynak)
    except Exception:
        return None

    # Modul docstring'i
    docstring = ast.get_docstring(agac) or ""

    # Function ve class isimleri
    fonksiyonlar = [n.name for n in ast.walk(agac) if isinstance(n, ast.FunctionDef)]
    siniflar = [n.name for n in ast.walk(agac) if isinstance(n, ast.ClassDef)]

    return {
        "ad": modul_id.replace("_", " ").title(),
        "emoji": "📦",
        "kategori": "AUTO-DISCOVERED",
        "view_dosya": bulunan_dosya,
        "model_dosyalari": [],
        "aciklama": (docstring[:300] if docstring else "Bu modul icin manuel metadata yok. Auto-discovery ile gorunur."),
        "ana_ozellikler": [f"{len(fonksiyonlar)} fonksiyon", f"{len(siniflar)} sinif"],
        "tablar": [],
        "otomasyonlar": [],
        "arka_plan_motorlari": [(s, bulunan_dosya, "Sinif") for s in siniflar[:6]],
        "veri_dosyalari": [],
        "senaryo": ["Modul ekrani uzerinde kullanilir"],
        "_auto": True,
        "_fonksiyonlar": fonksiyonlar,
        "_siniflar": siniflar,
    }


# ============================================================
# PUBLIC API
# ============================================================

def list_moduller() -> list[tuple[str, str, str]]:
    """Tum moduller (ID, ad, emoji) listesi — registry'de olanlar."""
    sonuc = []
    for mod_id, meta in MODUL_REGISTRY.items():
        sonuc.append((mod_id, meta["ad"], meta.get("emoji", "📦")))
    return sorted(sonuc, key=lambda x: x[1])


def get_modul_meta(modul_id: str) -> dict | None:
    """Bir modul icin metadata dondur (registry oncelikli, sonra auto-discovery)."""
    if modul_id in MODUL_REGISTRY:
        return MODUL_REGISTRY[modul_id]
    return _auto_discover(modul_id)


# ============================================================
# PDF URETICI — TUM MODULLER ICIN GENERIC
# ============================================================

def generate_pdf(modul_id: str, kurum_adi: str = "SmartCampus AI") -> bytes:
    """
    Bir modul icin kurumsal kilavuz PDF uret.
    Returns: PDF bytes (hata durumunda bos)
    """
    if not _REPORTLAB_OK:
        return b""

    meta = get_modul_meta(modul_id)
    if not meta:
        return b""

    try:
        from utils.shared_data import ensure_turkish_pdf_fonts
        fn, fb = ensure_turkish_pdf_fonts()
    except Exception:
        fn, fb = "Helvetica", "Helvetica-Bold"

    styles = _build_styles(fn, fb)
    story = []

    _build_cover(story, styles, meta, kurum_adi, fn, fb)
    story.append(PageBreak())
    _build_section_overview(story, styles, meta)
    story.append(PageBreak())
    _build_section_tablar(story, styles, meta)
    story.append(PageBreak())
    _build_section_otomasyon(story, styles, meta)
    story.append(PageBreak())
    _build_section_motorlar(story, styles, meta)
    story.append(PageBreak())
    _build_section_veri(story, styles, meta)
    story.append(PageBreak())
    _build_section_senaryo(story, styles, meta)
    story.append(PageBreak())
    _build_back_cover(story, styles, meta, kurum_adi, fn, fb)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.2 * cm,
        title=f"{meta['ad']} Kilavuzu",
        author=kurum_adi,
        subject=f"{meta['ad']} Modulu Kullanim Kilavuzu",
    )

    def _on_page(c, d):
        _draw_header_footer(c, d, fn, fb, kurum_adi, meta["ad"])

    try:
        doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    except Exception:
        return b""

    return buf.getvalue()


def generate_zip_all(kurum_adi: str = "SmartCampus AI") -> bytes:
    """Tum modullerin PDF'lerini ZIP olarak dondur."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for mod_id, meta in MODUL_REGISTRY.items():
            try:
                pdf = generate_pdf(mod_id, kurum_adi)
                if pdf:
                    safe_name = "".join(
                        c if c.isalnum() or c in "_-" else "_"
                        for c in meta["ad"]
                    )
                    zf.writestr(f"{safe_name}_Kilavuzu.pdf", pdf)
            except Exception:
                continue
    return buf.getvalue()


# ============================================================
# STILLER
# ============================================================

def _build_styles(fn: str, fb: str):
    if not _REPORTLAB_OK:
        return {}
    styles = {}

    styles["KapakBaslik"] = ParagraphStyle(
        "KapakBaslik", fontName=fb, fontSize=36, leading=42,
        textColor=HexColor(WHITE), alignment=TA_CENTER,
    )
    styles["H1"] = ParagraphStyle(
        "H1", fontName=fb, fontSize=22, leading=28,
        textColor=HexColor(NAVY), alignment=TA_LEFT, spaceAfter=10,
    )
    styles["H2"] = ParagraphStyle(
        "H2", fontName=fb, fontSize=15, leading=20,
        textColor=HexColor(NAVY), spaceBefore=14, spaceAfter=6,
    )
    styles["H3"] = ParagraphStyle(
        "H3", fontName=fb, fontSize=12, leading=15,
        textColor=HexColor(GOLD_DARK), spaceBefore=10, spaceAfter=4,
    )
    styles["Body"] = ParagraphStyle(
        "Body", fontName=fn, fontSize=9.5, leading=13,
        textColor=HexColor(BODY), alignment=TA_JUSTIFY, spaceAfter=4,
    )
    styles["Madde"] = ParagraphStyle(
        "Madde", fontName=fn, fontSize=9, leading=12,
        textColor=HexColor(BODY), leftIndent=16, spaceAfter=1,
    )
    styles["MaddeAlt"] = ParagraphStyle(
        "MaddeAlt", fontName=fn, fontSize=8.5, leading=11,
        textColor=HexColor(MUTED), leftIndent=26, spaceAfter=1,
    )
    styles["KutuMetin"] = ParagraphStyle(
        "KutuMetin", fontName=fn, fontSize=8.5, leading=11,
        textColor=HexColor(BODY), leftIndent=6, rightIndent=6,
    )
    styles["KutuMetinBold"] = ParagraphStyle(
        "KutuMetinBold", fontName=fb, fontSize=8.5, leading=11,
        textColor=HexColor(DARK), leftIndent=6, rightIndent=6,
    )
    styles["TabloH"] = ParagraphStyle(
        "TabloH", fontName=fb, fontSize=9, leading=11,
        textColor=HexColor(WHITE),
    )
    styles["Tablo"] = ParagraphStyle(
        "Tablo", fontName=fn, fontSize=8.5, leading=10.5,
        textColor=HexColor(BODY),
    )
    styles["TabloBold"] = ParagraphStyle(
        "TabloBold", fontName=fb, fontSize=8.5, leading=10.5,
        textColor=HexColor(NAVY),
    )

    return styles


# ============================================================
# HEADER / FOOTER
# ============================================================

def _draw_header_footer(c, doc, fn: str, fb: str, kurum_adi: str, modul_adi: str):
    if not _REPORTLAB_OK:
        return
    W, H = A4

    if doc.page > 1:
        c.setFillColor(HexColor(NAVY))
        c.rect(0, H - 1.5 * cm, W, 1.5 * cm, fill=1, stroke=0)
        c.setStrokeColor(HexColor(GOLD))
        c.setLineWidth(1.2)
        c.line(0, H - 1.5 * cm, W, H - 1.5 * cm)

        c.setFillColor(HexColor(GOLD))
        c.setFont(fb, 7)
        c.drawString(2.2 * cm, H - 1.0 * cm, kurum_adi.upper()[:50])

        c.setFillColor(HexColor(WHITE))
        c.setFont(fb, 8)
        c.drawCentredString(W / 2, H - 1.0 * cm, f"{modul_adi.upper()} - KILAVUZ")

        c.setFillColor(HexColor(GOLD_LT))
        c.setFont(fn, 6.5)
        c.drawRightString(W - 2.2 * cm, H - 1.0 * cm, date.today().isoformat())

    # Footer
    c.setStrokeColor(HexColor(GOLD))
    c.setLineWidth(0.4)
    c.line(2.2 * cm, 1.5 * cm, W - 2.2 * cm, 1.5 * cm)
    c.setFillColor(HexColor(MUTED))
    c.setFont(fn, 7)
    c.drawString(2.2 * cm, 1.0 * cm, f"{kurum_adi}")
    c.setFont(fb, 8)
    c.setFillColor(HexColor(GOLD_DARK))
    c.drawCentredString(W / 2, 1.0 * cm, f"◆ Sayfa {doc.page} ◆")
    c.setFont(fn, 7)
    c.setFillColor(HexColor(MUTED))
    c.drawRightString(W - 2.2 * cm, 1.0 * cm, "Modul Kilavuz v1.0")


# ============================================================
# YARDIMCI FLOWABLE'LAR
# ============================================================

def _gold_rule():
    return HRFlowable(
        width="100%", thickness=1.2, color=HexColor(GOLD),
        spaceBefore=4, spaceAfter=8, hAlign="LEFT",
    )


def _bolum_baslik(story, styles, no, baslik, alt=""):
    data = [[
        Paragraph(f"<font color='{GOLD}' size='30'><b>{no:02d}</b></font>", styles["Body"]),
        Paragraph(
            f"<font color='{NAVY}' size='22'><b>{baslik.upper()}</b></font>"
            + (f"<br/><font color='{GOLD_DARK}' size='9'>{alt}</font>" if alt else ""),
            styles["Body"]
        ),
    ]]
    tbl = Table(data, colWidths=[1.8 * cm, 14.5 * cm])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 1.5, HexColor(GOLD)),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.4 * cm))


def _h2(story, styles, baslik):
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph(f"<b>{baslik}</b>", styles["H2"]))


def _h3(story, styles, baslik):
    story.append(Paragraph(baslik, styles["H3"]))


def _p(story, styles, metin):
    story.append(Paragraph(metin, styles["Body"]))


def _madde(story, styles, metin):
    story.append(Paragraph(f"•  {metin}", styles["Madde"]))


def _alt_madde(story, styles, metin):
    story.append(Paragraph(f"◦  {metin}", styles["MaddeAlt"]))


def _bilgi_kutusu(story, styles, baslik, metin, renk=NAVY, ikon="i"):
    data = [
        [Paragraph(f"<b>{ikon}  {baslik}</b>", styles["KutuMetinBold"])],
        [Paragraph(metin, styles["KutuMetin"])],
    ]
    tbl = Table(data, colWidths=[16.3 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(renk)),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor(WHITE)),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor(LIGHT_GRAY)),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBEFORE", (0, 0), (0, -1), 3, HexColor(renk)),
    ]))
    story.append(Spacer(1, 0.15 * cm))
    story.append(tbl)
    story.append(Spacer(1, 0.2 * cm))


def _tablo(story, styles, basliklar, satirlar, sutun_genislikleri=None, renk=NAVY):
    data = [[Paragraph(b, styles["TabloH"]) for b in basliklar]]
    for satir in satirlar:
        data.append([
            Paragraph(str(h), styles["Tablo"]) if not str(h).startswith("__B__")
            else Paragraph(str(h)[5:], styles["TabloBold"])
            for h in satir
        ])
    if not sutun_genislikleri:
        esit = 16.3 / len(basliklar)
        sutun_genislikleri = [esit * cm] * len(basliklar)
    tbl = Table(data, colWidths=sutun_genislikleri, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor(renk)),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor(WHITE)),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor(MUTED)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor(WHITE), HexColor("#F8FAFC")]),
    ]))
    story.append(Spacer(1, 0.15 * cm))
    story.append(tbl)
    story.append(Spacer(1, 0.25 * cm))


# ============================================================
# BÖLÜMLER
# ============================================================

def _build_cover(story, styles, meta, kurum_adi, fn, fb):
    band = [[Paragraph(
        f"<font color='{GOLD}' size='9'><b>{kurum_adi.upper()}</b></font>",
        styles["Body"]
    )]]
    tbl = Table(band, colWidths=[16.3 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(NAVY)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEABOVE", (0, 0), (-1, 0), 2, HexColor(GOLD)),
        ("LINEBELOW", (0, 0), (-1, 0), 2, HexColor(GOLD)),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 3 * cm))

    # Modul emoji + ad
    emoji = meta.get("emoji", "📦")
    story.append(Paragraph(
        f"<font color='{NAVY}' size='62'>{emoji}</font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.5 * cm))

    # Ad
    story.append(Paragraph(
        f"<font color='{NAVY}' size='30'><b>{meta['ad'].upper()}</b></font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.3 * cm))

    # Diamond
    story.append(Paragraph(
        f"<font color='{GOLD}' size='22'>◆ ◆ ◆</font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.4 * cm))

    # Alt baslik
    story.append(Paragraph(
        f"<font color='{GOLD_DARK}' size='14'><b>KURUMSAL KULLANIM KILAVUZU</b></font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        f"<font color='{MUTED}' size='10'>{meta.get('kategori', 'MODUL')}</font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 1.5 * cm))

    # Istatistik kutulari
    tab_sayisi = len(meta.get("tablar", []))
    otomasyon_sayisi = len(meta.get("otomasyonlar", []))
    motor_sayisi = len(meta.get("arka_plan_motorlari", []))
    veri_sayisi = len(meta.get("veri_dosyalari", []))

    istatistik_data = [[
        Paragraph(f"<font color='{GOLD}' size='22'><b>{tab_sayisi}</b></font><br/>"
                  f"<font color='{MUTED}' size='7'>SEKME</font>", styles["Body"]),
        Paragraph(f"<font color='{GOLD}' size='22'><b>{otomasyon_sayisi}</b></font><br/>"
                  f"<font color='{MUTED}' size='7'>OTOMASYON</font>", styles["Body"]),
        Paragraph(f"<font color='{GOLD}' size='22'><b>{motor_sayisi}</b></font><br/>"
                  f"<font color='{MUTED}' size='7'>ARKA PLAN MOTOR</font>", styles["Body"]),
        Paragraph(f"<font color='{GOLD}' size='22'><b>{veri_sayisi}</b></font><br/>"
                  f"<font color='{MUTED}' size='7'>VERI DOSYASI</font>", styles["Body"]),
    ]]
    tbl_st = Table(istatistik_data, colWidths=[4 * cm] * 4)
    tbl_st.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, HexColor(GOLD)),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, HexColor(GOLD)),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8FAFC")),
    ]))
    story.append(tbl_st)
    story.append(Spacer(1, 2 * cm))

    alt_band = [[Paragraph(
        f"<font color='{GOLD_LT}' size='8'><b>HAZIRLANMA:</b> "
        f"{date.today().strftime('%d %B %Y')}  •  <b>VERSIYON:</b> v1.0  •  "
        f"<b>STATU:</b> URETIM</font>",
        styles["Body"]
    )]]
    tbl_alt = Table(alt_band, colWidths=[16.3 * cm])
    tbl_alt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(NAVY)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEABOVE", (0, 0), (-1, 0), 2, HexColor(GOLD)),
        ("LINEBELOW", (0, 0), (-1, 0), 2, HexColor(GOLD)),
    ]))
    story.append(tbl_alt)


def _build_section_overview(story, styles, meta):
    _bolum_baslik(story, styles, 1, "Modul Tanitimi",
                   meta.get("ad", "") + " - Yonetici Ozeti")

    _p(story, styles, meta.get("aciklama", "Bu modul icin aciklama yok."))

    if meta.get("ana_ozellikler"):
        _h2(story, styles, "1.1 Ana Ozellikler")
        for oz in meta["ana_ozellikler"]:
            _madde(story, styles, oz)

    _h2(story, styles, "1.2 Modul Bilgileri")
    bilgi_data = [
        ["ALAN", "DEGER"],
        ["__B__Modul Adi", meta.get("ad", "-")],
        ["__B__Kategori", meta.get("kategori", "-")],
        ["__B__View Dosyasi", meta.get("view_dosya", "-")],
        ["__B__Model Dosyalari", str(len(meta.get("model_dosyalari", [])))],
        ["__B__Sekme Sayisi", str(len(meta.get("tablar", [])))],
        ["__B__Otomasyon Sayisi", str(len(meta.get("otomasyonlar", [])))],
        ["__B__Arka Plan Motoru", str(len(meta.get("arka_plan_motorlari", [])))],
        ["__B__Veri Dosyasi", str(len(meta.get("veri_dosyalari", [])))],
    ]
    _tablo(story, styles, bilgi_data[0], bilgi_data[1:],
            sutun_genislikleri=[6 * cm, 10.3 * cm])

    if meta.get("model_dosyalari"):
        _h2(story, styles, "1.3 Model Dosyalari")
        for md in meta["model_dosyalari"]:
            _madde(story, styles, f"<b>{md}</b>")


def _build_section_tablar(story, styles, meta):
    _bolum_baslik(story, styles, 2, "Sekmeler ve Kullanim",
                   "Her tabin amaci, otomatik islei, manuel islei")

    tablar = meta.get("tablar", [])
    if not tablar:
        _p(story, styles, "Bu modul icin sekme detayi henuz eklenmedi.")
        return

    for i, tab_data in enumerate(tablar, 1):
        if len(tab_data) >= 4:
            ad, amac, otomatik, manuel = tab_data[0], tab_data[1], tab_data[2], tab_data[3]
        elif len(tab_data) >= 2:
            ad, amac = tab_data[0], tab_data[1]
            otomatik, manuel = [], []
        else:
            continue

        # Baslik
        basl = [[Paragraph(
            f"<font color='{WHITE}' size='11'><b>{i:02d}.  {ad}</b></font>",
            styles["Body"]
        )]]
        tbl_basl = Table(basl, colWidths=[16.3 * cm])
        tbl_basl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor(NAVY)),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBEFORE", (0, 0), (0, -1), 4, HexColor(GOLD)),
        ]))
        bolum_content = [tbl_basl, Spacer(1, 0.1 * cm)]

        bolum_content.append(Paragraph(f"<b>Amac:</b> {amac}", styles["Body"]))

        if otomatik:
            bolum_content.append(Paragraph(
                f"<font color='{GREEN}'><b>Otomatik:</b></font>", styles["Body"]
            ))
            for ot in otomatik:
                bolum_content.append(Paragraph(f"•  {ot}", styles["Madde"]))

        if manuel:
            bolum_content.append(Paragraph(
                f"<font color='{ORANGE}'><b>Manuel:</b></font>", styles["Body"]
            ))
            for mn in manuel:
                bolum_content.append(Paragraph(f"•  {mn}", styles["Madde"]))

        bolum_content.append(Spacer(1, 0.3 * cm))
        story.append(KeepTogether(bolum_content))


def _build_section_otomasyon(story, styles, meta):
    _bolum_baslik(story, styles, 3, "Otomasyon Sistemi",
                   "Otomatik tetiklenen islemler")

    otomasyonlar = meta.get("otomasyonlar", [])
    if not otomasyonlar:
        _p(story, styles, "Bu modulde tanimli otomasyon bulunmuyor.")
        return

    _p(story, styles,
       f"Bu modul {len(otomasyonlar)} otomasyon iceriyor. Her biri belirli bir "
       f"olay (trigger) ile devreye girer.")

    data = [["#", "OTOMASYON", "TRIGGER", "ACIKLAMA"]]
    for i, ot in enumerate(otomasyonlar, 1):
        if len(ot) >= 3:
            ad, trigger, aciklama = ot[0], ot[1], ot[2]
        else:
            ad, trigger, aciklama = ot[0] if ot else "", "", ""
        data.append([str(i), f"__B__{ad}", trigger, aciklama])

    _tablo(story, styles, data[0], data[1:],
            sutun_genislikleri=[0.8 * cm, 5 * cm, 4 * cm, 6.5 * cm])


def _build_section_motorlar(story, styles, meta):
    _bolum_baslik(story, styles, 4, "Arka Plan Motorlari",
                   "Gorunmeyen ama surekli calisan hesaplamalar")

    motorlar = meta.get("arka_plan_motorlari", [])
    if not motorlar:
        _p(story, styles, "Bu modulde arka plan motoru tanimli degil.")
        return

    _p(story, styles,
       f"Bu modul {len(motorlar)} arka plan motoru ile destekleniyor. "
       f"Bu motorlar siz farkinda olmadan calisir ve veri uretir.")

    data = [["#", "MOTOR", "DOSYA", "GOREVI"]]
    for i, m in enumerate(motorlar, 1):
        if len(m) >= 3:
            ad, dosya, gorev = m[0], m[1], m[2]
        else:
            ad, dosya, gorev = m[0] if m else "", "", ""
        data.append([str(i), f"__B__{ad}", dosya, gorev])

    _tablo(story, styles, data[0], data[1:],
            sutun_genislikleri=[0.8 * cm, 4.5 * cm, 4.5 * cm, 6.5 * cm])


def _build_section_veri(story, styles, meta):
    _bolum_baslik(story, styles, 5, "Veri Dosyalari",
                   "Modulun kullandigi JSON depolari")

    dosyalar = meta.get("veri_dosyalari", [])
    if not dosyalar:
        _p(story, styles, "Bu modul ozel veri dosyasi kullanmiyor (paylasilan veri kaynaklari kullanir).")
        return

    _p(story, styles,
       f"Bu modul {len(dosyalar)} JSON dosyasi kullaniyor. Her biri tenant-aware "
       f"olarak data/{{tenant}}/{{modul}}/ altinda saklanir.")

    data = [["#", "DOSYA", "ICERIK"]]
    for i, df in enumerate(dosyalar, 1):
        if len(df) >= 2:
            dosya, icerik = df[0], df[1]
        else:
            dosya, icerik = df[0] if df else "", ""
        data.append([str(i), f"__B__{dosya}", icerik])

    _tablo(story, styles, data[0], data[1:],
            sutun_genislikleri=[0.8 * cm, 6 * cm, 9.5 * cm])


def _build_section_senaryo(story, styles, meta):
    _bolum_baslik(story, styles, 6, "Kullanim Senaryosu",
                   "Pratik adim adim is akisi")

    senaryo = meta.get("senaryo", [])
    if not senaryo:
        _p(story, styles, "Bu modul icin senaryo tanimi yok.")
        return

    _h2(story, styles, "Tipik Kullanim Akisi")
    for i, adim in enumerate(senaryo, 1):
        _madde(story, styles, f"<b>Adim {i}:</b> {adim}")

    _bilgi_kutusu(story, styles, "Pratik Tavsiye",
        "Bu modulu acmadan once mevcut veri kaynaklarinizin (Sinif Listeleri, "
        "Kurum Profili, IK Personel) dolu olduğundan emin olun. Bircok modul "
        "bu paylasilan kaynaklardan veri ceker.",
        renk=NAVY, ikon="*")


def _build_back_cover(story, styles, meta, kurum_adi, fn, fb):
    story.append(Spacer(1, 3 * cm))

    story.append(Paragraph(
        f"<font color='{GOLD}' size='32'>◆</font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(
        f"<font color='{NAVY}' size='22'><b>BU KILAVUZ HAZIRDIR</b></font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(_gold_rule())

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        f"<font color='{BODY}' size='10'>{meta['ad']} modulunun tum ozellikleri, "
        f"sekmeleri, otomasyonlari ve veri yapilari bu kilavuzda detayli olarak "
        f"yer aliyor.</font>",
        styles["Body"]
    ))
    story.append(Spacer(1, 1.5 * cm))

    imza_data = [[
        Paragraph(
            f"<font color='{GOLD}' size='13'><b>{kurum_adi.upper()}</b></font><br/>"
            f"<font color='{GOLD_LT}' size='9'>{meta['ad']} Kilavuz v1.0</font><br/>"
            f"<font color='{MUTED}' size='8'>Hazirlanma: {date.today().strftime('%d %B %Y')}</font>",
            styles["Body"]
        )
    ]]
    tbl = Table(imza_data, colWidths=[16.3 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor(NAVY)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LINEABOVE", (0, 0), (-1, 0), 2, HexColor(GOLD)),
        ("LINEBELOW", (0, 0), (-1, 0), 2, HexColor(GOLD)),
    ]))
    story.append(tbl)
