#!/usr/bin/env python3
"""
SmartCampusAI — PREMIUM TAM KULLANIM KILAVUZU PDF URETICI
============================================================
Tum moduller, sekmeler, alt sekmeler, roller, fonksiyonlar.
Yonetici, Ogretmen, Rehber, Veli, Ogrenci acisindan adim adim.
Her ekran, her buton, her islem detayli anlatilir.

Cikti: SmartCampusAI_Tam_Kullanim_Kilavuzu.pdf
"""
import os
import textwrap
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Output ──
BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, "SmartCampusAI_Tam_Kullanim_Kilavuzu.pdf")

W, H = A4  # 595, 842

# ── Renkler ──
NAVY = HexColor("#0F172A")
NAVY_LIGHT = HexColor("#1E293B")
GOLD = HexColor("#C8952E")
GOLD_LIGHT = HexColor("#E6C77A")
INDIGO = HexColor("#6366F1")
PURPLE = HexColor("#8B5CF6")
GREEN = HexColor("#10B981")
RED = HexColor("#EF4444")
BLUE = HexColor("#3B82F6")
ORANGE = HexColor("#F97316")
CYAN = HexColor("#06B6D4")
PINK = HexColor("#EC4899")
BODY_CLR = HexColor("#334155")
MUTED = HexColor("#64748B")
LIGHT_BG = HexColor("#F8FAFC")
CREAM = HexColor("#FFFDF7")

# ── Fontlar ──
def _register_fonts():
    for name in ["Calibri", "CalibriBold"]:
        try:
            pdfmetrics.getFont(name)
        except:
            try:
                if "Bold" in name:
                    pdfmetrics.registerFont(TTFont(name, "calibrib.ttf"))
                else:
                    pdfmetrics.registerFont(TTFont(name, "calibri.ttf"))
            except:
                pass
    for name in ["Georgia", "GeorgiaBold"]:
        try:
            pdfmetrics.getFont(name)
        except:
            try:
                if "Bold" in name:
                    pdfmetrics.registerFont(TTFont(name, "georgiab.ttf"))
                else:
                    pdfmetrics.registerFont(TTFont(name, "georgia.ttf"))
            except:
                pass

_register_fonts()

# ── Yardimci ──
def _font(bold=False, serif=False):
    if serif:
        return "GeorgiaBold" if bold else "Georgia"
    return "CalibriBold" if bold else "Calibri"

def _text(c, text, x, y, font="Calibri", size=10, color=BODY_CLR, max_w=None):
    c.setFont(font, size)
    c.setFillColor(color)
    if max_w:
        lines = textwrap.wrap(text, width=int(max_w / (size * 0.45)))
        for line in lines:
            c.drawString(x, y, line)
            y -= size + 3
        return y
    else:
        c.drawString(x, y, text)
        return y - size - 3

def _rect(c, x, y, w, h, fill=None, stroke=None, radius=0):
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.5)
    if radius:
        c.roundRect(x, y, w, h, radius, fill=1 if fill else 0, stroke=1 if stroke else 0)
    else:
        c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)

def _line(c, x1, y1, x2, y2, color=GOLD, width=1):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def new_page(c, page_no):
    # Ust bar
    _rect(c, 0, H - 25, W, 25, fill=NAVY)
    c.setFont(_font(True), 8)
    c.setFillColor(GOLD)
    c.drawString(30, H - 18, "SmartCampus AI — Tam Kullanim Kilavuzu")
    c.setFillColor(white)
    c.drawRightString(W - 30, H - 18, f"Sayfa {page_no}")
    # Alt bar
    _rect(c, 0, 0, W, 15, fill=NAVY)
    c.setFont(_font(), 7)
    c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 4, f"SmartCampus AI v25 | {date.today().strftime('%d.%m.%Y')} | Gizlidir")
    # Gold accent
    _line(c, 0, H - 25, W, H - 25, GOLD, 1.5)


# ══════════════════════════════════════════════════
# ROL TANIMLARI
# ══════════════════════════════════════════════════

ROLLER = [
    {
        "ad": "Yonetici / Mudur",
        "ikon": "Y",
        "renk": INDIGO,
        "aciklama": "Okul genelini yonetir. Tum modullere erisim. Butce, kayit, personel, analitik, onay islemleri.",
        "erisim": "Tum moduller (35 modul)",
        "gunluk": [
            "Ana Sayfa dashboard'dan KPI'lari kontrol et",
            "Analitik Dashboard'dan sinif performanslarini karsilastir",
            "Odeme Takip'ten geciken odemeleri incele",
            "Kayit Modulu'nden yeni aday pipeline'ini yonet",
            "Veli taleplerini onayla/reddet",
            "Vekil ogretmen atamasi yap",
        ],
    },
    {
        "ad": "Ogretmen",
        "ikon": "O",
        "renk": GREEN,
        "aciklama": "Sinifini yonetir. Yoklama, not girisi, odev atama, sinav olusturma, ders defteri.",
        "erisim": "Akademik moduller + mesajlasma",
        "gunluk": [
            "Yoklama al (manuel veya QR)",
            "Not girisi yap",
            "Odev ata, teslim takibi",
            "Ders defterine kayit gir",
            "Sinav sonuclarini analiz et",
            "Veli mesajlarini cevapla",
        ],
    },
    {
        "ad": "Rehber Ogretmen",
        "ikon": "R",
        "renk": PURPLE,
        "aciklama": "Ogrenci psikolojik destegi. Vakalar, gorusmeler, risk degerlendirme, BEP, kriz mudahale.",
        "erisim": "Rehberlik + Erken Uyari + Akademik Takip",
        "gunluk": [
            "Mood check-in sonuclarini incele",
            "Risk degerlendirme dashboard'u kontrol et",
            "Gorusme notu yaz",
            "Kriz mudahale kaydi olustur",
            "BEP planlarini guncelle",
            "Ihbar hatti bildirimlerini incele",
        ],
    },
    {
        "ad": "Veli",
        "ikon": "V",
        "renk": ORANGE,
        "aciklama": "Cocugunun akademik durumunu takip eder. Notlar, devamsizlik, odevler, randevu, servis.",
        "erisim": "Cocuk detay + veli modulleri (13 sayfa)",
        "gunluk": [
            "Gunluk Kapsul'den gun ozetini oku",
            "Cocugun notlarini/devamsizligini kontrol et",
            "Bekleyen odevleri gor",
            "Ogretmenle gorusme talebi olustur",
            "Servis durumunu takip et",
            "Yemek menusunu incele",
        ],
    },
    {
        "ad": "Ogrenci",
        "ikon": "S",
        "renk": CYAN,
        "aciklama": "Kendi akademik durumunu takip eder. Notlar, odevler, sinav, defterim, AI asistan.",
        "erisim": "Ogrenci modulleri (24 sayfa)",
        "gunluk": [
            "Dashboard'dan KPI'larini gor (ortalama, devamsizlik, odev)",
            "Yaklasan sinavlari kontrol et",
            "Odevlerini teslim et",
            "Smarti AI'a soru sor",
            "Mood check-in yap",
            "Defterime not ekle",
        ],
    },
]


# ══════════════════════════════════════════════════
# PDF URETIM
# ══════════════════════════════════════════════════

def build_pdf():
    from modul_veri import MODULLER

    c = Canvas(OUTPUT, pagesize=A4)
    page_no = [0]

    def np():
        if page_no[0] > 0:
            c.showPage()
        page_no[0] += 1
        new_page(c, page_no[0])
        return H - 50

    # ════════════════════════════════════
    # KAPAK
    # ════════════════════════════════════
    _rect(c, 0, 0, W, H, fill=NAVY)
    # Gold cerceve
    _rect(c, 15, 15, W - 30, H - 30, stroke=GOLD)
    _rect(c, 20, 20, W - 40, H - 40, stroke=GOLD_LIGHT)
    # Logo alani
    _rect(c, W/2 - 50, H - 200, 100, 100, fill=INDIGO)
    c.setFont(_font(True), 48)
    c.setFillColor(white)
    c.drawCentredString(W/2, H - 170, "SC")
    c.setFont(_font(), 14)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, H - 190, "AI")
    # Baslik
    c.setFont(_font(True, True), 32)
    c.setFillColor(white)
    c.drawCentredString(W/2, H - 260, "SmartCampus AI")
    _line(c, W/2 - 120, H - 270, W/2 + 120, H - 270, GOLD, 2)
    c.setFont(_font(True), 20)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, H - 300, "TAM KULLANIM KILAVUZU")
    c.setFont(_font(), 14)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W/2, H - 330, "Modul Modul · Sekme Sekme · Rol Rol")
    # Alt bilgi
    c.setFont(_font(), 12)
    c.setFillColor(MUTED)
    c.drawCentredString(W/2, 120, f"Versiyon: v25 | {date.today().strftime('%d %B %Y')}")
    c.drawCentredString(W/2, 100, "35 Modul | 40 Kayitli Modul | 390+ Sekme | 5 Rol")
    c.drawCentredString(W/2, 80, "99 Mobil Sayfa | 143 API Endpoint")
    c.setFont(_font(True), 11)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, 50, "GIZLI — Sadece yetkili personel icin")
    page_no[0] = 1

    # ════════════════════════════════════
    # ICINDEKILER
    # ════════════════════════════════════
    y = np()
    c.setFont(_font(True, True), 24)
    c.setFillColor(NAVY)
    c.drawString(40, y, "ICINDEKILER")
    _line(c, 40, y - 5, 200, y - 5, GOLD, 2)
    y -= 30

    sections = [
        "BOLUM 1: SISTEM TANITIMI",
        "BOLUM 2: ROLLER VE ERISIM",
        "BOLUM 3: GIRIS VE ARAYUZ",
    ]
    # Modul gruplari
    grup_sira = ["GENEL", "KURUM", "KURUM YONETIMI", "ILETISIM & RANDEVU",
                 "AKADEMIK", "OKUL YASAMI", "OPERASYON", "SISTEM"]
    modul_no = 4
    for g in grup_sira:
        g_moduls = [m for m in MODULLER if m.get("grup", "").upper().startswith(g.split()[0])]
        if g_moduls:
            sections.append(f"BOLUM {modul_no}: {g}")
            modul_no += 1

    sections.append(f"BOLUM {modul_no}: MOBIL UYGULAMA")
    sections.append(f"BOLUM {modul_no+1}: SORUN GIDERME VE SSS")

    for i, s in enumerate(sections):
        c.setFont(_font(True), 11)
        c.setFillColor(NAVY if "BOLUM" in s else BODY_CLR)
        c.drawString(50, y, s)
        y -= 16
        if y < 60:
            y = np()

    # ════════════════════════════════════
    # BOLUM 1: SISTEM TANITIMI
    # ════════════════════════════════════
    y = np()
    c.setFont(_font(True, True), 26)
    c.setFillColor(NAVY)
    c.drawString(40, y, "BOLUM 1")
    c.setFont(_font(True, True), 20)
    c.setFillColor(INDIGO)
    c.drawString(130, y, "SISTEM TANITIMI")
    _line(c, 40, y - 8, W - 40, y - 8, GOLD, 1.5)
    y -= 30

    tanitim = [
        "SmartCampus AI, Turkiye'nin en kapsamli egitim yonetim platformudur.",
        "",
        "Platform 3 ana bilesenden olusur:",
        "  1. Web Uygulamasi (Streamlit) — 35 modul, 390+ sekme",
        "  2. Mobil Uygulama (Flutter) — 99 sayfa, Android APK",
        "  3. Backend API (FastAPI) — 143 endpoint, JWT guvenlik",
        "",
        "Desteklenen Roller:",
        "  - Yonetici / Mudur: Tum sisteme erisim",
        "  - Ogretmen: Akademik islemler (yoklama, not, odev, sinav)",
        "  - Rehber Ogretmen: Psikolojik destek, risk takibi",
        "  - Veli: Cocuk takibi, randevu, odeme (anaokulundan liseye)",
        "  - Ogrenci: Kendi akademik durumu, AI asistan, oyunlar",
        "",
        "Onemli Ozellikler:",
        "  - Multi-tenant: Birden fazla okul/kampus destegi",
        "  - AI Destekli: GPT-4o-mini ile soru uretimi, Smarti asistan",
        "  - Offline Mobil: Internet yokken cache'den calisir",
        "  - Dark/Light Tema: Kullanici tercihine gore",
        "  - Otomatik APK Build: GitHub Actions ile CI/CD",
        "  - SMS/Email Bildirim: Devamsizlik, not, odeme hatirlatma",
        "  - Rate Limiting: Dakikada 100 istek siniri (guvenlik)",
    ]
    for line in tanitim:
        if not line:
            y -= 8
            continue
        bold = line.startswith("  -") or line.startswith("  1") or line.startswith("  2") or line.startswith("  3")
        c.setFont(_font(bold), 10.5)
        c.setFillColor(BODY_CLR)
        c.drawString(50, y, line)
        y -= 14
        if y < 60:
            y = np()

    # ════════════════════════════════════
    # BOLUM 2: ROLLER
    # ════════════════════════════════════
    y = np()
    c.setFont(_font(True, True), 26)
    c.setFillColor(NAVY)
    c.drawString(40, y, "BOLUM 2")
    c.setFont(_font(True, True), 20)
    c.setFillColor(INDIGO)
    c.drawString(130, y, "ROLLER VE ERISIM HAKLARI")
    _line(c, 40, y - 8, W - 40, y - 8, GOLD, 1.5)
    y -= 35

    for rol in ROLLER:
        if y < 200:
            y = np()
        # Rol basligi
        _rect(c, 40, y - 5, W - 80, 22, fill=rol["renk"])
        c.setFont(_font(True), 13)
        c.setFillColor(white)
        c.drawString(50, y, f"{rol['ikon']}  {rol['ad']}")
        y -= 30
        # Aciklama
        c.setFont(_font(), 10)
        c.setFillColor(BODY_CLR)
        c.drawString(50, y, rol["aciklama"])
        y -= 15
        c.setFont(_font(True), 9)
        c.setFillColor(INDIGO)
        c.drawString(50, y, f"Erisim: {rol['erisim']}")
        y -= 18
        # Gunluk isler
        c.setFont(_font(True), 10)
        c.setFillColor(NAVY)
        c.drawString(50, y, "Gunluk Is Akisi:")
        y -= 14
        for i, iş in enumerate(rol["gunluk"], 1):
            c.setFont(_font(), 9.5)
            c.setFillColor(BODY_CLR)
            c.drawString(60, y, f"{i}. {iş}")
            y -= 13
        y -= 15

    # ════════════════════════════════════
    # BOLUM 3: GIRIS VE ARAYUZ
    # ════════════════════════════════════
    y = np()
    c.setFont(_font(True, True), 26)
    c.setFillColor(NAVY)
    c.drawString(40, y, "BOLUM 3")
    c.setFont(_font(True, True), 20)
    c.setFillColor(INDIGO)
    c.drawString(130, y, "GIRIS VE ARAYUZ REHBERI")
    _line(c, 40, y - 8, W - 40, y - 8, GOLD, 1.5)
    y -= 30

    giris_bilgi = [
        ("Web Giris:", "Tarayicida localhost:8501 adresine git. Sol tarafta sidebar'da kullanici adi + sifre gir."),
        ("Mobil Giris:", "APK'yi telefonuna yukle. Login ekraninda kullanici adi + sifre gir."),
        ("", ""),
        ("Giris Bilgileri:", ""),
        ("  Yonetici:", "admin / SmartCampus123"),
        ("  Ogretmen:", "ogretmen / SmartCampus123"),
        ("  Rehber:", "screhber / SmartCampus123"),
        ("  Veli:", "veli / SmartCampus123"),
        ("  Ogrenci:", "ogrenci / SmartCampus123"),
        ("", ""),
        ("Sidebar Yapisi:", "8 ana grup, 35 modul. Her grup acilir-kapanir."),
        ("Tema:", "Koyu tema (varsayilan). Ayarlar'dan degistirilebilir."),
        ("Arama:", "Sidebar'da modul ismi yazarak filtrele."),
    ]
    for label, val in giris_bilgi:
        if not label and not val:
            y -= 8
            continue
        c.setFont(_font(True), 10)
        c.setFillColor(NAVY)
        c.drawString(50, y, label)
        c.setFont(_font(), 10)
        c.setFillColor(BODY_CLR)
        c.drawString(50 + len(label) * 5.5, y, val)
        y -= 14

    # ════════════════════════════════════
    # MODULLER — Her biri detayli
    # ════════════════════════════════════

    # Renk paleti — gruplara gore
    GRUP_RENK = {
        "GENEL": INDIGO, "KURUM": BLUE, "KURUM YONETIMI": BLUE,
        "AKADEMIK": GREEN, "ILETISIM & RANDEVU": PURPLE,
        "OKUL YASAMI": CYAN, "OPERASYON": ORANGE, "SISTEM": PINK,
    }

    bolum_no = 4
    onceki_grup = ""

    for mi, m in enumerate(MODULLER):
        grup = m.get("grup", "DIGER")
        accent = m.get("accent", GRUP_RENK.get(grup, INDIGO))

        # Yeni grup basligi
        if grup != onceki_grup:
            y = np()
            c.setFont(_font(True, True), 26)
            c.setFillColor(NAVY)
            c.drawString(40, y, f"BOLUM {bolum_no}")
            c.setFont(_font(True, True), 18)
            c.setFillColor(accent)
            c.drawString(140, y, grup.upper())
            _line(c, 40, y - 8, W - 40, y - 8, GOLD, 2)
            bolum_no += 1
            onceki_grup = grup
            y -= 40

        # ── Modul Basligi ──
        if y < 250:
            y = np()

        # Modul no + ad
        _rect(c, 35, y - 8, W - 70, 28, fill=accent)
        c.setFont(_font(True), 14)
        c.setFillColor(white)
        c.drawString(45, y - 2, f"{m['section_no']:02d}  {m['ad'].upper()}")
        yeni_badge = m.get("yeni", False)
        if yeni_badge:
            c.setFont(_font(True), 9)
            c.drawRightString(W - 45, y - 2, "YENI")
        y -= 35

        # Amac
        c.setFont(_font(True), 11)
        c.setFillColor(NAVY)
        c.drawString(45, y, "AMAC")
        _line(c, 45, y - 3, 85, y - 3, accent, 1)
        y -= 15
        amac = m.get("amac", "")
        y = _text(c, amac, 50, y, _font(), 9.5, BODY_CLR, max_w=490)
        y -= 8

        # Kim kullanir
        kim = m.get("kim", [])
        if kim:
            c.setFont(_font(True), 11)
            c.setFillColor(NAVY)
            c.drawString(45, y, "KIM KULLANIR")
            _line(c, 45, y - 3, 140, y - 3, accent, 1)
            y -= 15
            for rol_name, rol_desc in kim:
                c.setFont(_font(True), 9)
                c.setFillColor(accent)
                c.drawString(55, y, f"{rol_name}:")
                c.setFont(_font(), 9)
                c.setFillColor(BODY_CLR)
                c.drawString(55 + len(rol_name) * 5 + 10, y, rol_desc)
                y -= 13
            y -= 5

        # Ana ozellikler
        ozellikler = m.get("ana_ozellikler", [])
        if ozellikler:
            if y < 120:
                y = np()
            c.setFont(_font(True), 11)
            c.setFillColor(NAVY)
            c.drawString(45, y, "ANA OZELLIKLER")
            _line(c, 45, y - 3, 160, y - 3, accent, 1)
            y -= 15
            for oz in ozellikler:
                c.setFont(_font(), 9)
                c.setFillColor(BODY_CLR)
                c.drawString(55, y, f"• {oz}")
                y -= 12
                if y < 50:
                    y = np()
            y -= 5

        # ── SEKMELER ── (en onemli kisim)
        sekmeler = m.get("sekmeler", [])
        if sekmeler:
            if y < 150:
                y = np()
            c.setFont(_font(True), 12)
            c.setFillColor(NAVY)
            c.drawString(45, y, f"SEKMELER ({len(sekmeler)} adet)")
            _line(c, 45, y - 3, 200, y - 3, accent, 1.5)
            y -= 18

            for si, sekme in enumerate(sekmeler, 1):
                if y < 80:
                    y = np()

                # Sekme adi + aciklama
                if isinstance(sekme, tuple) and len(sekme) >= 2:
                    s_ad = sekme[0]
                    s_aciklama = sekme[1]
                    s_kullanim = sekme[2] if len(sekme) > 2 else []
                elif isinstance(sekme, dict):
                    s_ad = sekme.get("ad", "")
                    s_aciklama = sekme.get("aciklama", "")
                    s_kullanim = sekme.get("kullanim", [])
                else:
                    continue

                # Sekme basligi
                _rect(c, 50, y - 4, 490, 17, fill=HexColor("#F1F5F9"), stroke=accent)
                c.setFont(_font(True), 9.5)
                c.setFillColor(accent)
                c.drawString(55, y, f"Sekme {si}: {s_ad}")
                y -= 20

                # Aciklama
                if s_aciklama:
                    y = _text(c, s_aciklama, 60, y, _font(), 9, BODY_CLR, max_w=470)
                    y -= 3

                # Kullanim adimlari
                if isinstance(s_kullanim, list) and s_kullanim:
                    for k in s_kullanim:
                        c.setFont(_font(), 8.5)
                        c.setFillColor(MUTED)
                        c.drawString(65, y, f"  → {k}")
                        y -= 11
                        if y < 50:
                            y = np()

                y -= 5

        # Is akisi
        is_akisi = m.get("is_akisi", [])
        if is_akisi:
            if y < 100:
                y = np()
            c.setFont(_font(True), 11)
            c.setFillColor(NAVY)
            c.drawString(45, y, "IS AKISI (ADIM ADIM)")
            _line(c, 45, y - 3, 200, y - 3, accent, 1)
            y -= 15
            for adim in is_akisi:
                c.setFont(_font(), 9)
                c.setFillColor(BODY_CLR)
                c.drawString(55, y, adim)
                y -= 12
                if y < 50:
                    y = np()
            y -= 5

        # Ipuclari
        ipuclari = m.get("ipuclari", [])
        if ipuclari:
            if y < 80:
                y = np()
            c.setFont(_font(True), 10)
            c.setFillColor(GOLD)
            c.drawString(45, y, "IPUCLARI")
            y -= 14
            for ip in ipuclari:
                c.setFont(_font(), 8.5)
                c.setFillColor(MUTED)
                y = _text(c, f"💡 {ip}", 55, y, _font(), 8.5, MUTED, max_w=480)
                y -= 3
                if y < 50:
                    y = np()
            y -= 5

        # SSS
        sss = m.get("sss", [])
        if sss:
            if y < 80:
                y = np()
            c.setFont(_font(True), 10)
            c.setFillColor(NAVY)
            c.drawString(45, y, "SIK SORULAN SORULAR")
            y -= 14
            for soru, cevap in sss:
                c.setFont(_font(True), 9)
                c.setFillColor(NAVY)
                c.drawString(55, y, f"S: {soru}")
                y -= 12
                c.setFont(_font(), 9)
                c.setFillColor(BODY_CLR)
                y = _text(c, f"C: {cevap}", 55, y, _font(), 9, BODY_CLR, max_w=480)
                y -= 8
                if y < 50:
                    y = np()

        print(f"  [{mi+1:02d}/{len(MODULLER)}] {m['ad']} ... OK")

    # ════════════════════════════════════
    # MOBIL UYGULAMA
    # ════════════════════════════════════
    y = np()
    c.setFont(_font(True, True), 26)
    c.setFillColor(NAVY)
    c.drawString(40, y, f"BOLUM {bolum_no}")
    c.setFont(_font(True, True), 20)
    c.setFillColor(INDIGO)
    c.drawString(140, y, "MOBIL UYGULAMA")
    _line(c, 40, y - 8, W - 40, y - 8, GOLD, 2)
    y -= 35

    mobil_bilgi = [
        "SmartCampus AI mobil uygulamasi Flutter ile gelistirilmistir.",
        "99 Dart dosyasi, 5 rol, ultra premium tasarim.",
        "",
        "Roller ve Sayfa Sayilari:",
        "  Ogrenci: 24 sayfa (notlar, odevler, sinav, defterim, AI, oyunlar...)",
        "  Veli: 13 sayfa (cocuk detay, kapsul, servis, yemek, gorusme...)",
        "  Ogretmen: 7 sayfa (yoklama, QR, not girisi, odev, ders defteri)",
        "  Rehber: 13 sayfa (vakalar, gorusme, risk, BEP, kriz...)",
        "  Yonetici: 21 sayfa (bugun okulda, butce, onaylar, erken uyari...)",
        "",
        "Ortak Ozellikler:",
        "  - Bildirim sayfasi (tum roller)",
        "  - Dark/Light tema toggle",
        "  - Profil sayfasi + sifre degistirme",
        "  - Offline cache (internet yokken calisir)",
        "  - Smarti AI asistan (GPT destekli)",
        "",
        "APK Indirme:",
        "  https://github.com/aykinuz-stack/smartcampus-ai/releases",
        "",
        "Giris Bilgileri (mobil):",
        "  admin / SmartCampus123 (Yonetici)",
        "  ogrenci / SmartCampus123",
        "  veli / SmartCampus123",
        "  ogretmen / SmartCampus123",
        "  screhber / SmartCampus123 (Rehber)",
    ]
    for line in mobil_bilgi:
        if not line:
            y -= 8
            continue
        bold = line.endswith(":") or line.startswith("  -")
        c.setFont(_font(bold), 10)
        c.setFillColor(BODY_CLR)
        c.drawString(50, y, line)
        y -= 14
        if y < 50:
            y = np()

    # ════════════════════════════════════
    # ARKA KAPAK
    # ════════════════════════════════════
    c.showPage()
    _rect(c, 0, 0, W, H, fill=NAVY)
    _rect(c, 15, 15, W - 30, H - 30, stroke=GOLD)
    c.setFont(_font(True, True), 28)
    c.setFillColor(white)
    c.drawCentredString(W/2, H/2 + 40, "SmartCampus AI")
    _line(c, W/2 - 100, H/2 + 30, W/2 + 100, H/2 + 30, GOLD, 2)
    c.setFont(_font(), 14)
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, H/2, "Egitimin Gelecegi")
    c.setFont(_font(), 11)
    c.setFillColor(MUTED)
    c.drawCentredString(W/2, H/2 - 40, "35 Modul | 390+ Sekme | 5 Rol")
    c.drawCentredString(W/2, H/2 - 60, "99 Mobil Sayfa | 143 API Endpoint")
    c.drawCentredString(W/2, H/2 - 80, f"{date.today().year} SmartCampus")

    c.save()

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"\n{'='*60}")
    print(f"TAMAMLANDI: {OUTPUT}")
    print(f"Toplam sayfa: {page_no[0] + 1}")
    print(f"Dosya boyutu: {size_kb:.0f} KB")
    print(f"{'='*60}")


if __name__ == "__main__":
    build_pdf()
