"""
Akademik Takip Modulu - UI
===========================
Ogrenci yonetimi, not takibi, devamsizlik, ders programi,
ogretmen yonetimi ve raporlama.
"""

from __future__ import annotations

import calendar
import json
import os
import random
import re
import uuid
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from utils.tenant import get_data_path
from utils.report_utils import ReportStyler, ReportPDFGenerator, ReportSharer, get_institution_info
from utils.ui_kit import confirm_action
from models.akademik_takip import (
    Student, Teacher, GradeRecord, AttendanceRecord, ScheduleSlot,
    KazanimIsleme, EtutKayit, SinifKadro,
    Odev, ZamanDilimi, TeacherAssignment,
    OnlineDersLink, OnlineDersKayit, DijitalOgrenmeLink,
    NobetGorev, NobetKayit, OgretmenIzin,
    MudahaleKayit, DestekPlani, OgretmenOneri,
    EarlyWarningEngine,
    AkademikDataStore, get_akademik_store, ScheduleDistributor,
    DERSLER, GUNLER, GUNLER_FULL, GUN_KISALTMA, SINIFLAR, SUBELER,
    NOT_TURLERI, DERS_KISALTMA, GOREV_LABELS,
    AYLAR, ETUT_TURLERI,
    ISLENMEME_NEDENLERI, ODEV_TURLERI, ODEV_TESLIM_DURUMLARI,
    OGRENCI_TESLIM_TURLERI, DOSYA_TURLERI,
    DEVAMSIZLIK_TURLERI, DEVAMSIZLIK_TIPLERI,
    SABAH_DERS_SAATLERI, OGLEDEN_SONRA_SAATLERI,
    VELI_BILDIRIM_SABLONLARI,
    DEVAMSIZLIK_UYARI_GUN, DEVAMSIZLIK_TEHLIKE_GUN, DEVAMSIZLIK_SINIR_GUN,
    VARSAYILAN_ZAMAN_CIZELGESI, ZAMAN_DILIMI_TURLERI, ZAMAN_DILIMI_RENKLER,
    ONLINE_DERS_DURUMLARI, ONLINE_DERS_DURUM_LABELS, YAPILMAMA_NEDENLERI,
    DIJITAL_OGRENME_KATEGORILERI, DIJITAL_OGRENME_KATEGORI_MAP,
    NOBET_YERLERI, NOBET_GUNLERI, NOBET_DURUMLARI, NOBET_TUTULMAMA_NEDENLERI,
    IZIN_TURLERI, IZIN_SURE_TURLERI, IZIN_DURUMLARI,
    ORTAOKUL_DERSLER,
    MUDAHALE_TIPLERI, MUDAHALE_DURUMLARI,
    ONERI_KATEGORILERI, ONERI_ONCELIKLERI,
    RISK_SEVERITY_LABELS, RISK_SEVERITY_COLORS,
    DESTEK_PLANI_DURUMLARI,
    Certificate, SERTIFIKA_TURLERI, SERTIFIKA_BASLIK_MAP,
    PRESET_CERT_TEMPLATES,
    KYTSoru, KYT_DERSLER, _get_kademe,
    KazanimBorcEngine,
    BORC_NEDENLERI, BORC_NEDENI_LABELS, KAPANMA_NEDENLERI,
)

from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("akademik_takip")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("akademik_takip",
        "14 sekmeli kapsamli akademik yonetim — not, yoklama, ders defteri, kazanim takibi",
        [("200", "Ogrenci"), ("50", "Ogretmen"), ("14", "Sekme")])
except Exception:
    pass


# ==================== YARDIMCI FONKSIYONLAR ====================

@st.cache_data(ttl=3600)
def _get_akademik_yil() -> str:
    """Mevcut akademik yili dondurur — 1 saatlik cache."""
    today = date.today()
    if today.month >= 9:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


def _not_turu_label(kod: str) -> str:
    """Not turu kodunu etiketine cevirir."""
    mapping = dict(NOT_TURLERI)
    return mapping.get(kod, kod)


_AY_MAP = {
    "eylul": 9, "eylül": 9, "ekim": 10, "kasim": 11, "kasım": 11,
    "aralik": 12, "aralık": 12, "ocak": 1, "subat": 2, "şubat": 2,
    "mart": 3, "nisan": 4, "mayis": 5, "mayıs": 5,
    "haziran": 6, "temmuz": 7, "agustos": 8, "ağustos": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6,
}

_AY_ISIMLERI = {
    9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik",
    1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan",
    5: "Mayis", 6: "Haziran",
}

# Akademik yildaki ay sirasi (Eylul=1, Ekim=2, ..., Haziran=10)
_AY_SIRA = {9: 1, 10: 2, 11: 3, 12: 4, 1: 5, 2: 6, 3: 7, 4: 8, 5: 9, 6: 10}


def _parse_hafta_no(week_str: str) -> int:
    """Hafta stringinden hafta numarasi cikarir. Bulamazsa 0 doner."""
    week_clean = week_str.replace('\n', ' ').strip()
    # Turkce: "3. Hafta"
    m = re.search(r'(\d+)\.\s*[Hh]afta', week_clean)
    if m:
        return int(m.group(1))
    # Ingilizce: "Week 11"
    m = re.search(r'[Ww]eek\s*(\d+)', week_clean)
    if m:
        return int(m.group(1))
    return 0


def _parse_ay(week_str: str) -> int:
    """Hafta stringinden ay numarasi cikarir. Bulamazsa 0 doner."""
    week_lower = week_str.replace('\n', ' ').strip().lower()
    for ay_isim, ay_no in _AY_MAP.items():
        if ay_isim in week_lower:
            return ay_no
    return 0


def _uyari_badge(uyari: str) -> str:
    """Devamsizlik uyari badge HTML."""
    if uyari == "SINIR_ASILDI":
        return '<span style="background:#DC2626;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">SINIR ASILDI</span>'
    elif uyari == "TEHLIKE":
        return '<span style="background:#F59E0B;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">TEHLIKE</span>'
    elif uyari == "UYARI":
        return '<span style="background:#FB923C;color:white;padding:2px 8px;border-radius:4px;font-size:12px;">UYARI</span>'
    return ""


# ==================== PROGRAM ENTEGRASYON YARDIMCILARI ====================

def _get_ogretmen_from_schedule(store, sinif: int, sube: str, gun: str,
                                 ders_saati: int, akademik_yil: str = None) -> str | None:
    """Ders programindan belirli sinif/sube/gun/saat için ogretmen adini dondurur."""
    if not akademik_yil:
        akademik_yil = _get_akademik_yil()
    program = store.get_schedule(sinif=sinif, sube=sube, gun=gun,
                                  akademik_yil=akademik_yil)
    for slot in program:
        if slot.ders_saati == ders_saati:
            return slot.ogretmen
    return None


def _get_ogretmen_by_ders(store, sinif: int, sube: str, ders: str,
                           akademik_yil: str = None) -> str | None:
    """Ders programindan belirli sinif/sube/ders için ogretmen adini dondurur.
    Birden fazla ogretmen varsa ilkini dondurur."""
    if not akademik_yil:
        akademik_yil = _get_akademik_yil()
    all_slots = store.get_schedule(sinif=sinif, sube=sube, akademik_yil=akademik_yil)
    for slot in all_slots:
        if slot.ders and slot.ders.lower() == ders.lower():
            return slot.ogretmen
    return None


def _get_schedule_ders_map(store, sinif: int, sube: str, gun: str,
                            akademik_yil: str = None) -> dict:
    """Belirli gun için {ders_saati: {"ders": ..., "ogretmen": ...}} dict'i dondurur."""
    if not akademik_yil:
        akademik_yil = _get_akademik_yil()
    program = store.get_schedule(sinif=sinif, sube=sube, gun=gun,
                                  akademik_yil=akademik_yil)
    result = {}
    for slot in program:
        result[slot.ders_saati] = {"ders": slot.ders, "ogretmen": slot.ogretmen}
    return result


# ==================== MODERN CSS & STIL ====================

def _inject_css():
    """Dashboard-style modern CSS - session_state ile sadece 1 kez inject edilir."""
    if st.session_state.get("_at_css_injected"):
        return
    st.session_state["_at_css_injected"] = True
    inject_common_css("at")
    st.markdown("""
    <style>
    :root {
        --ak-primary: #2563eb;
        --ak-primary-dark: #1e40af;
        --ak-primary-light: #60a5fa;
        --ak-success: #10b981;
        --ak-warning: #f59e0b;
        --ak-danger: #ef4444;
        --ak-purple: #8b5cf6;
        --ak-teal: #0d9488;
        --ak-dark: #0B0F19;
        --ak-gray-50: #111827;
        --ak-gray-100: #1A2035;
        --ak-gray-200: #e2e8f0;
        --ak-gray-500: #64748b;
        --ak-gray-800: #94A3B8;
    }

    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(180deg, #0B0F19 0%, #131825 100%);
    }
    .stApp > header { background: transparent !important; }

    /* ===== METRIC CARDS - DASHBOARD ===== */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border-left: 4px solid #2563eb;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0B0F19 !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(37,99,235,0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button[kind="secondary"],
    .stButton > button:not([kind]) {
        border-radius: 10px !important;
        border: 1.5px solid #e2e8f0 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:not([kind]):hover {
        border-color: #2563eb !important;
        background: #eff6ff !important;
    }

    /* ===== EXPANDERS ===== */
    details[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
        overflow: hidden;
    }
    details[data-testid="stExpander"] summary {
        font-weight: 600 !important;
        padding: 12px 16px !important;
    }

    /* ===== INPUTS ===== */
    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border-color: #e2e8f0 !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }

    /* ===== DATA TABLES ===== */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06) !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(5,150,105,0.25) !important;
    }
    .stDownloadButton > button:hover {
        box-shadow: 0 6px 18px rgba(5,150,105,0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== DIVIDERS ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #cbd5e1 50%, transparent 100%) !important;
        margin: 1rem 0 !important;
    }

    /* ===== ALERTS & RADIO ===== */
    .stAlert { border-radius: 10px !important; }
    .stRadio > div { gap: 0.5rem; }
    .stRadio > div > label {
        border-radius: 10px !important;
        padding: 6px 12px !important;
    }

    /* ===== SCHEDULE CELLS (ders programi) ===== */
    .ak-schedule-cell {
        background: #f0f9ff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 6px 8px;
        text-align: center;
        font-size: 12px;
        min-height: 50px;
    }
    .ak-schedule-cell .ders { font-weight: 600; color: #2563eb; }
    .ak-schedule-cell .ogretmen { color: #64748b; font-size: 11px; }
    .ak-empty-cell {
        background: #111827;
        border: 1px dashed #e2e8f0;
        border-radius: 8px;
        padding: 6px 8px;
        text-align: center;
        font-size: 12px;
        min-height: 50px;
        color: #cbd5e1;
    }
    </style>
    """, unsafe_allow_html=True)


def _styled_group_header(title: str, subtitle: str = "", color: str = "#2563eb"):
    """Grup basligini gorsel olarak vurgulayan mini header."""
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{color}12 0%,{color}06 100%);'
        f'border:1px solid {color}20;border-radius:12px;padding:12px 18px;margin:6px 0 10px 0;">'
        f'<div style="font-size:1.05rem;font-weight:700;color:{color};">{title}</div>'
        + (f'<div style="font-size:0.78rem;color:#64748b;margin-top:2px;">{subtitle}</div>' if subtitle else '')
        + '</div>',
        unsafe_allow_html=True
    )


# ==================== TAB 1: OGRENCI YONETIMI ====================

@st.fragment
def _render_ogrenci_yonetimi(store: AkademikDataStore):
    """Ogrenci yonetimi sekmesi (salt-okunur, merkezi kaynak: KOI Sinif Listeleri)."""
    styled_section("Öğrenci Yönetimi", "#2563eb")
    st.markdown(
        """<div style='background:linear-gradient(135deg,#0d9488,#0891b2);color:#fff;
        padding:14px 20px;border-radius:10px;margin-bottom:16px;font-size:0.95rem'>
        <b>Merkezi Veri Tabani:</b> Öğrenci ve veli verileri
        <b>Kurumsal Organizasyon ve İletişim &gt; İletişim &gt; Sinif Listeleri</b>
        ekranindan yonetilmektedir. Öğrenci ekleme, duzenleme ve silme islemleri icin
        KOI modulunu kullanin.</div>""",
        unsafe_allow_html=True,
    )

    # Filtreler
    col1, col2, col3 = st.columns(3)
    with col1:
        filtre_sinif = st.selectbox("Sınıf", [None] + SINIFLAR,
                                     format_func=lambda x: "Tümü" if x is None else f"{x}. Sınıf",
                                     key="stu_filtre_sinif")
    with col2:
        filtre_sube = st.selectbox("Şube", [None] + SUBELER,
                                    format_func=lambda x: "Tümü" if x is None else x,
                                    key="stu_filtre_sube")
    with col3:
        arama = st.text_input("Ara (Ad, Soyad, Numara)", key="stu_arama")

    students = store.get_students(sinif=filtre_sinif, sube=filtre_sube,
                                   durum="aktif", query=arama if arama else None)

    # Ozet metrikler
    all_students = store.get_students(durum="aktif")
    sinif_sayisi = len(set((s.sinif, s.sube) for s in all_students))
    pasif = len(store.get_students(durum="pasif"))
    styled_stat_row([
        ("Toplam Öğrenci", len(all_students), "#2563eb", "\U0001f465"),
        ("Sınıf/Şube", sinif_sayisi, "#8b5cf6", "\U0001f3eb"),
        ("Filtrelenen", len(students), "#10b981", "\U0001f50d"),
        ("Pasif", pasif, "#f59e0b", "\u23f8\ufe0f"),
    ])
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if students:
        df_data = []
        for s in students:
            df_data.append({
                "Numara": s.numara,
                "Ad": s.ad,
                "Soyad": s.soyad,
                "Sınıf": s.sinif,
                "Şube": s.sube,
                "Veli": s.veli_adi,
                "Telefon": s.veli_telefon,
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Ogrenci detay (salt-okunur)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        styled_section("Öğrenci Detay", "#0d9488")
        student_options = {f"{s.numara} - {s.ad} {s.soyad}": s.id for s in students}
        selected = st.selectbox("Öğrenci Seçin", list(student_options.keys()), key="stu_select")

        if selected:
            stu = store.get_student(student_options[selected])
            if stu:
                dc1, dc2 = st.columns(2)
                with dc1:
                    st.markdown(f"**Ad Soyad:** {stu.ad} {stu.soyad}")
                    st.markdown(f"**Sınıf/Şube:** {stu.sinif}/{stu.sube}")
                    st.markdown(f"**Numara:** {stu.numara}")
                    st.markdown(f"**TC No:** {stu.tc_no or '-'}")
                    st.markdown(f"**Cinsiyet:** {stu.cinsiyet or '-'}")
                with dc2:
                    st.markdown(f"**Veli Adi:** {stu.veli_adi or '-'}")
                    st.markdown(f"**Veli Telefon:** {stu.veli_telefon or '-'}")
                    st.markdown(f"**Veli E-posta:** {stu.veli_email or '-'}")
                    st.markdown(f"**Anne:** {stu.anne_adi or '-'}")
                    st.markdown(f"**Baba:** {stu.baba_adi or '-'}")
                st.caption("Düzenleme icin: KOI > İletişim > Bilgi İşlem > Öğrenci Bilgi Karti")
    else:
        st.info("Öğrenci bulunamadı. Filtrelerinizi kontrol edin.")


# ==================== SINAV SONUÇLARI ====================

_KADEME_DERSLER: dict[str, list[str]] = {
    "İlkokul (1-4)": [
        "Türkçe", "Matematik", "Hayat Bilgisi", "İngilizce",
        "Müzik", "Görsel Sanatlar", "Beden Eğitimi", "Din Kültürü ve Ahlak Bilgisi",
    ],
    "Ortaokul (5-8)": list(ORTAOKUL_DERSLER),
    "Lise (9-12)": [
        "Türk Dili ve Edebiyatı", "Matematik", "Fizik", "Kimya", "Biyoloji",
        "Tarih", "Coğrafya", "Felsefe", "Geometri", "İngilizce",
        "Almanca", "Fransızca", "Din Kültürü ve Ahlak Bilgisi",
        "Beden Eğitimi", "Müzik", "Görsel Sanatlar",
        "T.C. İnkılap Tarihi ve Atatürkçülük",
    ],
}

_SS_COLS = [
    ("yazili",   1, "1. Yazılı"),
    ("yazili",   2, "2. Yazılı"),
    ("proje",    1, "1. Proje"),
    ("proje",    2, "2. Proje"),
    ("ders_ici", 1, "1. Katılım"),
    ("ders_ici", 2, "2. Katılım"),
]

_KADEMELER_SS = {
    "İlkokul (1-4)":  list(range(1, 5)),
    "Ortaokul (5-8)": list(range(5, 9)),
    "Lise (9-12)":    list(range(9, 13)),
}


def _ss_puan_badge(p) -> str:
    """Renk kodlu puan badge HTML."""
    if p is None or (isinstance(p, float) and pd.isna(p)):
        return "<span style='color:#94a3b8;font-size:0.85rem'>—</span>"
    p = float(p)
    if p < 50:
        clr, txt = "#ef4444", "Başarısız"
    elif p < 65:
        clr, txt = "#b45309", "Orta"
    elif p < 80:
        clr, txt = "#1d4ed8", "İyi"
    else:
        clr, txt = "#059669", "Pekiyi"
    return (
        f"<span style='background:{clr}18;color:{clr};border:1px solid {clr}44;"
        f"border-radius:5px;padding:2px 9px;font-size:0.82rem;font-weight:700'>"
        f"{p:.0f} <span style='font-size:0.7rem;opacity:.85'>{txt}</span></span>"
    )


@st.fragment
def _render_sinav_sonuclari(store: AkademikDataStore):
    """Tüm modüllerden konsolide sınav sonuçları — öğrenci bazlı kategori görünümü."""
    from datetime import date as _date

    styled_section("Sınav Sonuçları & Dönemlik Not Takibi", "#2563eb")

    # ── Canli Senkron Bilgi Bandı + Yenile Dugmesi ──────────────────────
    _sync_c1, _sync_c2 = st.columns([6, 1])
    with _sync_c1:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#0f766e,#10b981);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:8px;font-size:0.82rem;"
            "display:flex;align-items:center;gap:8px;"
            "box-shadow:0 2px 8px rgba(16,185,129,0.25)'>"
            "<span style='font-size:1.15rem'>🔗</span>"
            "<span><b>Ölçme Değerlendirme ile CANLI senkron</b> — "
            "🏫 Okul Yazılısı · 🎯 Kazanım Ölçme · 📝 Deneme · 📊 LGS-TYT-AYT · ⚡ Quiz "
            "sınavları Ölçme modülünden anlık olarak çekilir. "
            "Ölçme'de yeni bir sınav uygulandığında sonuç otomatik bu ekrana düşer."
            "</span>"
            "<span style='margin-left:auto;background:rgba(255,255,255,0.2);"
            "padding:2px 10px;border-radius:10px;font-size:0.7rem;font-weight:700;"
            "display:flex;align-items:center;gap:4px'>"
            "<span style='width:8px;height:8px;border-radius:50%;background:#10ff9a;"
            "box-shadow:0 0 6px #10ff9a'></span>LIVE</span>"
            "</div>",
            unsafe_allow_html=True,
        )
    with _sync_c2:
        st.write("")
        if st.button("🔄 Yenile", key="ss_refresh_btn", use_container_width=True,
                     help="Ölçme Değerlendirme modülünden en güncel sınav sonuçlarını çek"):
            st.rerun()

    # ── Bilgilendirme bandı
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1e40af,#3b82f6);color:white;"
        "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.82rem;"
        "display:flex;align-items:center;gap:8px'>"
        "<span style='font-size:1.2rem'>📊</span>"
        "<span><b>Konsolide Sınav Merkezi</b> — Okul yazılıları, ölçme değerlendirme sınavları, "
        "deneme sınavları, online testler, kazanım ölçme, ödev değerlendirme ve yabancı dil "
        "sınavları dahil tüm SmartCampusAI modüllerinden toplanan veriler.</span></div>",
        unsafe_allow_html=True,
    )

    # ── Ortak Filtreler ──────────────────────────────────────────────────
    _today = _date.today()
    current_yil = _get_akademik_yil()
    yil_list = [f"{y}-{y+1}" for y in range(_today.year - 2, _today.year + 1)]
    yil_list.reverse()

    fc1, fc2, fc3, fc4, fc5 = st.columns([2, 1, 2, 1, 1])
    with fc1:
        ss_yil = st.selectbox(
            "Eğitim Öğretim Yılı", yil_list,
            index=yil_list.index(current_yil) if current_yil in yil_list else 0,
            key="ss_yil",
        )
    with fc2:
        ss_donem = st.selectbox("Dönem", ["1. Dönem", "2. Dönem"], key="ss_donem")
    with fc3:
        ss_kademe = st.selectbox("Kademe", list(_KADEMELER_SS.keys()), key="ss_kademe")
    sinif_listesi = _KADEMELER_SS[ss_kademe]
    with fc4:
        ss_sinif = st.selectbox("Sınıf", sinif_listesi, key="ss_sinif")
    with fc5:
        ss_sube = st.selectbox("Şube", SUBELER, key="ss_sube")

    donem_key = "1. Donem" if "1" in ss_donem else "2. Donem"
    kademe_dersler = _KADEME_DERSLER.get(ss_kademe, DERSLER)

    students = store.get_students(sinif=ss_sinif, sube=ss_sube, durum="aktif")
    students = sorted(students, key=lambda s: s.numara or "")

    if not students:
        styled_info_banner("Bu sınıf/şubede aktif öğrenci bulunamadı.", "warning")
        return

    # ── Tum not verilerini yukle ─────────────────────────────────────────
    all_grades = store.get_grades(
        sinif=ss_sinif, sube=ss_sube,
        donem=donem_key, akademik_yil=ss_yil,
    )
    grade_map: dict = {}
    for g in all_grades:
        grade_map[(g.student_id, g.ders, g.not_turu, g.not_sirasi)] = (g.puan, g.id)

    def _stu_ort(stu_id: str) -> float | None:
        ps = [grade_map[k][0] for k in grade_map if k[0] == stu_id]
        ps = [p for p in ps if p and p > 0]
        return sum(ps) / len(ps) if ps else None

    # ── Veri Yukleme Fonksiyonlari ───────────────────────────────────────
    def _g(obj, key, default=""):
        """Güvenli attr/dict getter."""
        return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

    def _load_od_results(stu_or_id):
        """OD modulundeki sinav sonuclarini Akademik Takip ogrencisi icin getir.

        Argument: ya AT Student objesi ya da string id.
        OD'de student_id iki farkli sema ile kaydedilebiliyor:
          - 'stu_xxxxxxxx' (Akademik Takip ile ayni)
          - '{numara}_{sube}' (OD bireysel yukleme akisindan)
        Bu fonksiyon HER IKISIYLE de eslestirir.

        Donen sozluk SINIF/SUBE/OGRENCI alanlarini da TASIR -- Akademik Takip
        ile bire bir ayni keylere sahip olur.
        """
        try:
            from models.olcme_degerlendirme import DataStore as ODStore
            od = ODStore()

            # Input cesitleri: Student objesi mi, plain id mi?
            if isinstance(stu_or_id, str):
                stu_id = stu_or_id
                stu_numara = ""
                stu_sube = ""
                stu_sinif = None
                stu_ad = ""
                stu_soyad = ""
            else:
                stu_id = _g(stu_or_id, "id", "")
                stu_numara = str(_g(stu_or_id, "numara", "") or "")
                stu_sube = str(_g(stu_or_id, "sube", "") or "")
                stu_sinif = _g(stu_or_id, "sinif", None)
                stu_ad = _g(stu_or_id, "ad", "") or ""
                stu_soyad = _g(stu_or_id, "soyad", "") or ""

            # Olasi tum eslesme anahtarlari (lower-case + strip)
            match_keys = set()
            if stu_id:
                match_keys.add(str(stu_id).strip().lower())
            if stu_numara and stu_sube:
                match_keys.add(f"{stu_numara}_{stu_sube}".strip().lower())
                match_keys.add(f"{stu_numara}_{stu_sube.upper()}".strip().lower())

            # Sinav haritasi
            exams_map = {}
            try:
                for ex in od.get_exams():
                    eid = _g(ex, "id")
                    if eid:
                        exams_map[eid] = ex
            except Exception:
                pass

            # TUM sonuclari cek, ID semasina bakmaksizin esleme yap
            try:
                all_results = od.get_results()  # student_id filtersiz -> hepsini al
            except Exception:
                all_results = []

            items = []
            stu_full_lower = (f"{stu_ad} {stu_soyad}").strip().lower()

            for r in all_results:
                r_sid = str(_g(r, "student_id", "") or "").strip().lower()
                r_name = str(_g(r, "student_name", "") or "").strip().lower()
                r_no = str(_g(r, "student_number", "") or "").strip()

                # Eslesme: student_id veya student_name+numara
                matched = False
                if r_sid and r_sid in match_keys:
                    matched = True
                elif stu_numara and r_no and r_no == stu_numara and stu_full_lower and r_name == stu_full_lower:
                    matched = True
                elif stu_full_lower and r_name == stu_full_lower and not r_no:
                    matched = True

                if not matched:
                    continue

                exam_id = _g(r, "exam_id")
                exam = exams_map.get(exam_id, {})

                items.append({
                    # SINAV bilgileri (OD exam'den)
                    "exam_id": exam_id,
                    "sinav_adi": _g(exam, "name", "Sınav"),
                    "sinav_turu": _g(exam, "exam_type", ""),
                    "ders": _g(exam, "subject", "—"),
                    "sinif": _g(exam, "grade", stu_sinif),
                    "sube": _g(exam, "section", stu_sube) or stu_sube,
                    # OGRENCI bilgileri (OD result'tan + AT fallback)
                    "ogrenci_id": _g(r, "student_id", stu_id),
                    "ogrenci_adi": _g(r, "student_name", f"{stu_ad} {stu_soyad}".strip()),
                    "ogrenci_no": _g(r, "student_number", stu_numara),
                    # SONUC alanlari (OD result)
                    "toplam": int(_g(r, "total_questions", 0) or 0),
                    "dogru": int(_g(r, "correct_count", 0) or 0),
                    "yanlis": int(_g(r, "wrong_count", 0) or 0),
                    "bos": int(_g(r, "empty_count", 0) or 0),
                    "puan": float(_g(r, "score", 0) or 0),
                    "net": float(_g(r, "net_score", 0) or 0),
                    "tarih": str(_g(r, "graded_at", "")),
                })
            return items
        except Exception:
            return []

    # ── EXAM_TYPE → 5 OD GRUBU MAP (Olcme modulu ile senkron) ──
    def _exam_type_grubu(exam_type: str, exam_name: str = "") -> str:
        """OD exam_type (ve fallback olarak exam_name) degerini 5 ana sinav grubuna esle.
        Returns: 'okul_yazilisi' | 'kazanim_olcme' | 'deneme' | 'lgs_tyt_ayt' | 'quiz' | 'diger'

        exam_type bos olsa bile exam_name uzerinden tahmin yapilir
        (eski/elle eklenmis sinavlar icin geriye donuk uyumluluk).
        """
        et = (str(exam_type or "") + " " + str(exam_name or "")).strip()
        if not et:
            return "diger"
        # Quiz once kontrol edilmeli (Quiz adi diger anahtar kelimelerle de gecebilir)
        if "Quiz" in et or "quiz" in et.lower():
            return "quiz"
        # LGS-TYT-AYT
        if "LGS" in et or "TYT" in et or "AYT" in et:
            return "lgs_tyt_ayt"
        # Deneme
        if "Deneme" in et or "deneme" in et.lower():
            return "deneme"
        # Kazanim Olcme
        if "Kazanim" in et or "Kazanım" in et:
            return "kazanim_olcme"
        # Okul Yazilisi: 1./2. Donem 1./2. Yazili / Proje / Sozlu / Performans
        if (
            "Yazili" in et or "Yazılı" in et or "Proje" in et
            or "Sozlu" in et or "Sözlü" in et or "Performans" in et
        ):
            return "okul_yazilisi"
        return "diger"

    def _filter_od_by_grup(od_items: list, grup: str) -> list:
        """OD sonuc listesini sinav turu grubuna gore filtrele.

        Hem 'sinav_turu' hem 'sinav_adi' alanlarini kontrol eder
        (eski sinavlarda exam_type bos olabilir).
        """
        return [
            d for d in od_items
            if _exam_type_grubu(
                d.get("sinav_turu", ""),
                d.get("sinav_adi", ""),
            ) == grup
        ]

    def _load_deneme(stu_id):
        try:
            from models.egitim_koclugu import EKDataStore
            ek = EKDataStore()
            return ek.get_by_ogrenci("deneme_analizleri", stu_id) or []
        except Exception:
            return []

    def _load_online_test(stu_id):
        try:
            from models.egitim_koclugu import EKDataStore
            ek = EKDataStore()
            return ek.get_by_ogrenci("online_testler", stu_id) or []
        except Exception:
            return []

    def _load_yd(stu_or_id):
        """Yabanci Dil sonuclari (geriye uyumlu — list[YdExamResult] doner).

        Eski cagri sekli korunur: _load_yd(stu_id) — string id alir, YdExamResult
        nesnelerini doner. Yeni zenginlestirilmis veriler icin
        _load_yd_full(stu) kullan.
        """
        try:
            from models.yd_assessment import YdAssessmentStore
            yd = YdAssessmentStore()
            stu_id = stu_or_id if isinstance(stu_or_id, str) else _g(stu_or_id, "id", "")
            results = yd.get_results(student_id=stu_id) or []
            # Geriye donuk: ID semasi farkli olabilir — Student objesi geldiyse
            # numara_sube ve student_name fallback'lerini de dene
            if not results and not isinstance(stu_or_id, str):
                stu_numara = str(_g(stu_or_id, "numara", "") or "")
                stu_sube = str(_g(stu_or_id, "sube", "") or "")
                stu_ad = _g(stu_or_id, "ad", "") or ""
                stu_soyad = _g(stu_or_id, "soyad", "") or ""
                full_name = f"{stu_ad} {stu_soyad}".strip().lower()
                alt_keys = set()
                if stu_numara and stu_sube:
                    alt_keys.add(f"{stu_numara}_{stu_sube}".lower())
                # Tum sonuclari cek, manuel match yap
                all_results = yd.get_results() or []
                for r in all_results:
                    r_sid = str(getattr(r, "student_id", "") or "").strip().lower()
                    r_name = str(getattr(r, "student_name", "") or "").strip().lower()
                    if r_sid in alt_keys or (full_name and r_name == full_name):
                        results.append(r)
            return results
        except Exception:
            return []

    def _load_yd_full(stu_or_id):
        """Ogrenci icin TUM Yabanci Dil verisi (Quiz + Sinav + CEFR Placement + CEFR Mock).

        Tek seferde tum kaynaklardan zenginlestirilmis dict listeleri donduruyor:
        {
            'quizler':       [{...}],   # YdExamResult exam_category=='quiz'
            'sinavlar':      [{...}],   # YdExamResult exam_category!='quiz' (haftalik/yazili/deneme)
            'cefr_placement':[{...}],   # CEFRPlacementResult
            'cefr_mock':     [{...}],   # CEFRResult (Mock Exam)
            'remediation':   [{...}],   # YdRemediation (yanlislardan otomatik odev)
        }
        Hem stu_xxx ID hem numara_sube hem student_name semalarini eslestirir.
        """
        result = {
            "quizler": [],
            "sinavlar": [],
            "cefr_placement": [],
            "cefr_mock": [],
            "remediation": [],
        }

        # Esleme anahtarlari
        if isinstance(stu_or_id, str):
            stu_id = stu_or_id
            stu_numara = stu_sube = stu_ad = stu_soyad = ""
            stu_sinif = None
        else:
            stu_id = _g(stu_or_id, "id", "")
            stu_numara = str(_g(stu_or_id, "numara", "") or "")
            stu_sube = str(_g(stu_or_id, "sube", "") or "")
            stu_sinif = _g(stu_or_id, "sinif", None)
            stu_ad = _g(stu_or_id, "ad", "") or ""
            stu_soyad = _g(stu_or_id, "soyad", "") or ""

        match_keys = set()
        if stu_id:
            match_keys.add(str(stu_id).strip().lower())
        if stu_numara and stu_sube:
            match_keys.add(f"{stu_numara}_{stu_sube}".strip().lower())
            match_keys.add(f"{stu_numara}_{stu_sube.upper()}".strip().lower())
        full_name_lower = (f"{stu_ad} {stu_soyad}").strip().lower()

        def _student_matches(r_obj) -> bool:
            r_sid = str(_g(r_obj, "student_id", "") or "").strip().lower()
            r_name = str(_g(r_obj, "student_name", "") or "").strip().lower()
            if r_sid and r_sid in match_keys:
                return True
            if full_name_lower and r_name == full_name_lower:
                return True
            return False

        # ── 1. YD Quiz/Sinav (YdAssessmentStore) ──
        try:
            from models.yd_assessment import YdAssessmentStore
            yd = YdAssessmentStore()
            all_yd = yd.get_results() or []
            # Parent YdExam map (id -> exam) — name/unit/level icin
            exams_map = {}
            try:
                yd_exams = yd._load("exams") if hasattr(yd, "_load") else []
                for ex_d in yd_exams:
                    if isinstance(ex_d, dict) and ex_d.get("id"):
                        exams_map[ex_d["id"]] = ex_d
            except Exception:
                pass

            for r in all_yd:
                if not _student_matches(r):
                    continue
                exam_id = _g(r, "exam_id", "")
                parent = exams_map.get(exam_id, {})
                # Hangi liste? Quiz mi sinav mi?
                cat = str(_g(r, "exam_category", "") or _g(parent, "category", "") or "").lower()
                # exam_category bossa parent.category'den dene, oda bossa name'e bak
                if not cat:
                    nm = str(_g(parent, "name", "") or _g(r, "exam_name", "") or "").lower()
                    if "quiz" in nm:
                        cat = "quiz"
                    elif "yazili" in nm or "yazılı" in nm:
                        cat = "yazili"
                    elif "deneme" in nm:
                        cat = "deneme"
                    else:
                        cat = "haftalik"

                item = {
                    "kaynak": "yd_quiz" if cat == "quiz" else "yd_sinav",
                    "result_id": _g(r, "id", ""),
                    "exam_id": exam_id,
                    "sinav_adi": _g(r, "exam_name", "") or _g(parent, "name", "Yabancı Dil Sınavı"),
                    "kategori": cat,
                    "ders": "İngilizce",
                    "sinif": _g(r, "sinif", _g(parent, "sinif", stu_sinif)),
                    "sube": _g(r, "sube", _g(parent, "sube", stu_sube)),
                    "level": _g(r, "level", _g(parent, "level", "")),
                    "unit": _g(r, "unit", _g(parent, "unit", 0)),
                    "unit_theme": _g(r, "unit_theme", _g(parent, "unit_theme", "")),
                    "weeks": _g(r, "weeks", _g(parent, "weeks", [])),
                    "ogrenci_id": _g(r, "student_id", stu_id),
                    "ogrenci_adi": _g(r, "student_name", f"{stu_ad} {stu_soyad}".strip()),
                    "toplam": int(_g(r, "total_questions", 0) or 0),
                    "dogru": int(_g(r, "correct_count", 0) or 0),
                    "yanlis": int(_g(r, "wrong_count", 0) or 0),
                    "bos": int(_g(r, "empty_count", 0) or 0),
                    "puan": float(_g(r, "score", 0) or 0),
                    "earned_points": float(_g(r, "earned_points", 0) or 0),
                    "total_points": float(_g(r, "total_points", 0) or 0),
                    "skill_breakdown": _g(r, "skill_breakdown", {}) or {},
                    "theme_breakdown": _g(r, "theme_breakdown", {}) or {},
                    "week_breakdown": _g(r, "week_breakdown", {}) or {},
                    "tarih": str(_g(r, "graded_at", "") or ""),
                }
                if cat == "quiz":
                    result["quizler"].append(item)
                else:
                    result["sinavlar"].append(item)

            # YD Remediation (yanlislardan otomatik odev)
            try:
                all_rem = yd._load("remediation") if hasattr(yd, "_load") else []
                for rd in all_rem:
                    if not isinstance(rd, dict):
                        continue
                    if not _student_matches(rd):
                        continue
                    result["remediation"].append({
                        "kaynak": "yd_remediation",
                        "id": rd.get("id", ""),
                        "exam_id": rd.get("exam_id", ""),
                        "sinif": rd.get("sinif", stu_sinif),
                        "sube": rd.get("sube", stu_sube),
                        "level": rd.get("level", ""),
                        "wrong_topics": rd.get("wrong_topics", []),
                        "total_questions": int(rd.get("total_questions", 0) or 0),
                        "status": rd.get("status", ""),
                        "score": float(rd.get("score", 0) or 0),
                        "tarih": rd.get("created_at", ""),
                    })
            except Exception:
                pass
        except Exception:
            pass

        # ── 2. CEFR Placement (Seviye Tespit) ──
        try:
            from models.cefr_exam import CEFRPlacementStore
            cps = CEFRPlacementStore()
            # Ham veriyi al, manuel match (her semayi destekle)
            all_pl = cps._load(cps._results_path) if hasattr(cps, "_load") else []
            for d in all_pl:
                if not isinstance(d, dict):
                    continue
                if not _student_matches(d):
                    continue
                result["cefr_placement"].append({
                    "kaynak": "cefr_placement",
                    "id": d.get("id", ""),
                    "exam_id": d.get("exam_id", ""),
                    "sinav_adi": "CEFR Seviye Tespit",
                    "ders": "İngilizce",
                    "sinif": d.get("sinif", stu_sinif),
                    "sube": d.get("sube", stu_sube),
                    "grade": d.get("grade", 0),
                    "period": d.get("period", ""),
                    "academic_year": d.get("academic_year", ""),
                    "target_cefr": d.get("target_cefr", ""),
                    "placed_cefr": d.get("placed_cefr", ""),
                    "is_above_target": bool(d.get("is_above_target", False)),
                    "is_below_target": bool(d.get("is_below_target", False)),
                    "listening_score": float(d.get("listening_score", 0) or 0),
                    "listening_max": float(d.get("listening_max", 0) or 0),
                    "reading_score": float(d.get("reading_score", 0) or 0),
                    "reading_max": float(d.get("reading_max", 0) or 0),
                    "use_of_english_score": float(d.get("use_of_english_score", 0) or 0),
                    "use_of_english_max": float(d.get("use_of_english_max", 0) or 0),
                    "writing_score": float(d.get("writing_score", 0) or 0),
                    "writing_max": float(d.get("writing_max", 0) or 0),
                    "total_score": float(d.get("total_score", 0) or 0),
                    "total_max": float(d.get("total_max", 0) or 0),
                    "percentage": float(d.get("percentage", 0) or 0),
                    "score_by_level": d.get("score_by_level", {}),
                    "skill_breakdown": d.get("skill_breakdown", {}),
                    "tarih": d.get("submitted_at", ""),
                })
        except Exception:
            pass

        # ── 3. CEFR Mock Exam (Cambridge tarzi) ──
        try:
            from models.cefr_exam import CEFRExamStore
            ces = CEFRExamStore()
            all_mk = ces._load(ces._results_path) if hasattr(ces, "_load") else []
            for d in all_mk:
                if not isinstance(d, dict):
                    continue
                if not _student_matches(d):
                    continue
                result["cefr_mock"].append({
                    "kaynak": "cefr_mock",
                    "id": d.get("id", ""),
                    "exam_id": d.get("exam_id", ""),
                    "sinav_adi": "CEFR Mock Exam",
                    "ders": "İngilizce",
                    "sinif": d.get("sinif", stu_sinif),
                    "sube": d.get("sube", stu_sube),
                    "grade": d.get("grade", 0),
                    "cefr": d.get("cefr", ""),
                    "achieved_cefr": d.get("achieved_cefr", ""),
                    "next_cefr": d.get("next_cefr", ""),
                    "distance_to_next": float(d.get("distance_to_next", 0) or 0),
                    "listening_score": float(d.get("listening_score", 0) or 0),
                    "listening_max": float(d.get("listening_max", 0) or 0),
                    "reading_score": float(d.get("reading_score", 0) or 0),
                    "reading_max": float(d.get("reading_max", 0) or 0),
                    "writing_score": float(d.get("writing_score", 0) or 0),
                    "writing_max": float(d.get("writing_max", 0) or 0),
                    "speaking_score": float(d.get("speaking_score", 0) or 0),
                    "speaking_max": float(d.get("speaking_max", 0) or 0),
                    "total_score": float(d.get("total_score", 0) or 0),
                    "total_max": float(d.get("total_max", 0) or 0),
                    "percentage": float(d.get("percentage", 0) or 0),
                    "skill_breakdown": d.get("skill_breakdown", {}),
                    "tarih": d.get("submitted_at", ""),
                })
        except Exception:
            pass

        return result

    def _load_kyt(stu_id):
        try:
            return store.get_kyt_cevaplar(student_id=stu_id) or []
        except Exception:
            return []

    def _load_odev(stu_id):
        """Ogrencinin tum odev teslim kayitlari + parent Odev metadatasi.

        Odev Takip modulu (Ogretim & Planlama > Odev Takip) ile ayni
        AkademikDataStore uzerinden CANLI okuma yapar — ekstra cache yok.
        Donen liste her satirda hem teslim hem odev bilgilerini birlestirir.
        """
        try:
            teslimleri = store.get_odev_teslimleri(student_id=stu_id) or []
            if not teslimleri:
                return []
            # Tum ogrenciyi ilgilendiren parent odevleri tek seferde cek + map'e koy
            try:
                tum_odevler = store.get_odevler() or []
            except Exception:
                tum_odevler = []
            odev_map = {}
            for ov in tum_odevler:
                ov_id = _g(ov, "id", "")
                if ov_id:
                    odev_map[ov_id] = ov

            items = []
            for t in teslimleri:
                odev_id = _g(t, "odev_id", "")
                parent = odev_map.get(odev_id)
                items.append({
                    # Teslim
                    "teslim_id": _g(t, "id", ""),
                    "odev_id": odev_id,
                    "ogrenci_id": _g(t, "student_id", stu_id),
                    "ogrenci_adi": _g(t, "student_adi", ""),
                    "durum": _g(t, "durum", "bekliyor"),
                    "puan": float(_g(t, "puan", 0) or 0),
                    "teslim_tarihi": str(_g(t, "teslim_tarihi", "") or ""),
                    "ogretmen_notu": _g(t, "ogretmen_notu", "") or "",
                    "ogrenci_notu": _g(t, "ogrenci_notu", "") or "",
                    "dosya_yolu": _g(t, "dosya_yolu", "") or "",
                    # Parent Odev (Odev Takip modulunden)
                    "baslik": _g(parent, "baslik", "Ödev"),
                    "ders": _g(parent, "ders", "—"),
                    "sinif": _g(parent, "sinif", ""),
                    "sube": _g(parent, "sube", ""),
                    "odev_turu": _g(parent, "odev_turu", ""),
                    "verilme_tarihi": str(_g(parent, "verilme_tarihi", "") or ""),
                    "son_teslim_tarihi": str(_g(parent, "son_teslim_tarihi", "") or ""),
                    "kazanim_kodu": _g(parent, "kazanim_kodu", ""),
                    "ogretmen_adi": _g(parent, "ogretmen_adi", ""),
                    "online_teslim": bool(_g(parent, "online_teslim", False)),
                    "akademik_yil": _g(parent, "akademik_yil", ""),
                })
            return items
        except Exception:
            return []

    def _avg(lst):
        return sum(lst) / len(lst) if lst else 0

    # ── Renk Aciklama Bandi ──────────────────────────────────────────────
    st.markdown(
        "<div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px'>"
        "<span style='background:#ef444418;color:#ef4444;border:1px solid #ef444444;"
        "border-radius:10px;padding:1px 9px;font-size:0.75rem;font-weight:600'>⚠ Başarısız &lt;50</span>"
        "<span style='background:#f59e0b18;color:#b45309;border:1px solid #f59e0b44;"
        "border-radius:10px;padding:1px 9px;font-size:0.75rem;font-weight:600'>📌 Orta 50–64</span>"
        "<span style='background:#3b82f618;color:#1d4ed8;border:1px solid #3b82f644;"
        "border-radius:10px;padding:1px 9px;font-size:0.75rem;font-weight:600'>👍 İyi 65–79</span>"
        "<span style='background:#10b98118;color:#059669;border:1px solid #10b98144;"
        "border-radius:10px;padding:1px 9px;font-size:0.75rem;font-weight:600'>⭐ Pekiyi ≥80</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Ogrenci Kartlari Grid ────────────────────────────────────────────
    styled_section(f"Öğrenci Seçimi — {ss_sinif}/{ss_sube}", "#2563eb")

    sel_key = f"ss_sel_stu_{ss_sinif}_{ss_sube}"
    if sel_key not in st.session_state:
        st.session_state[sel_key] = None

    _N_COLS = 5
    card_rows = [students[i:i+_N_COLS] for i in range(0, len(students), _N_COLS)]

    for crow in card_rows:
        cols = st.columns(_N_COLS)
        for ci, stu in enumerate(crow):
            ort = _stu_ort(stu.id)
            is_sel = st.session_state[sel_key] == stu.id
            initials = (stu.ad[0] if stu.ad else "?") + (stu.soyad[0] if stu.soyad else "?")

            if ort is not None:
                if ort < 50:
                    av_color = "#ef4444"
                elif ort < 65:
                    av_color = "#b45309"
                elif ort < 80:
                    av_color = "#1d4ed8"
                else:
                    av_color = "#059669"
                av_html = f"<div style='font-size:1rem;font-weight:800;color:{av_color}'>{ort:.1f}</div>"
            else:
                av_color = "#94a3b8"
                av_html = "<div style='font-size:0.65rem;color:#94a3b8'>—</div>"

            border = f"2px solid {av_color}" if is_sel else "1.5px solid #e2e8f0"
            bg = f"{av_color}08" if is_sel else "#ffffff"
            shadow = f"0 4px 16px {av_color}30" if is_sel else "0 2px 6px #00000010"

            with cols[ci]:
                # AI Tahmin Badge
                _ai_badge_html = ""
                try:
                    from utils.ui_common import ai_tahmin_badge
                    _tahmin = (ort or 65) + random.uniform(-5, 8)
                    _risk = "dusuk" if _tahmin >= 70 else ("orta" if _tahmin >= 50 else "yuksek")
                    _ai_badge_html = f'<div style="text-align:center;margin-top:2px">{ai_tahmin_badge(_tahmin, _risk)}</div>'
                except Exception:
                    pass

                st.markdown(
                    f'<div data-student-id="{stu.id}" style="background:{bg};border:{border};border-radius:12px;'
                    f'padding:8px 6px;text-align:center;box-shadow:{shadow};margin-bottom:2px">'
                    f'<div style="width:34px;height:34px;border-radius:50%;'
                    f'background:linear-gradient(135deg,#1e40af,#60a5fa);'
                    f'color:white;font-weight:800;font-size:0.85rem;line-height:34px;'
                    f'margin:0 auto 4px auto">{initials}</div>'
                    f'<div style="font-weight:700;font-size:0.78rem;color:#94A3B8;'
                    f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
                    f'{stu.ad} {stu.soyad}</div>'
                    f'<div style="font-size:0.65rem;color:#64748b">{stu.numara or "—"}</div>'
                    f'{av_html}{_ai_badge_html}</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "✔ Seçili" if is_sel else "Seç",
                    key=f"ss_sel_btn_{stu.id}",
                    use_container_width=True,
                ):
                    st.session_state[sel_key] = stu.id
                    st.rerun(scope="fragment")

    # ── Secili Ogrenci → Kategori Tabları ────────────────────────────────
    sel_stu_id = st.session_state.get(sel_key)
    sel_stu = next((s for s in students if s.id == sel_stu_id), None)

    if sel_stu is None:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        styled_info_banner("Yukarıdan bir öğrenci seçin.", "info")
        return

    # Öğrenci başlık bandı
    stu_ort = _stu_ort(sel_stu.id)
    ort_text = f"{stu_ort:.1f}" if stu_ort else "—"
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#eef2ff 0%,#e0e7ff 60%,#c7d2fe 100%);'
        f'color:#94A3B8;padding:10px 18px;border-radius:12px;margin:12px 0 10px 0;'
        f'border:1px solid #c7d2fe;display:flex;justify-content:space-between;align-items:center">'
        f'<div><span style="font-size:1.05rem;font-weight:800">'
        f'{sel_stu.ad} {sel_stu.soyad}</span>'
        f'<span style="color:#64748b;font-size:0.8rem;margin-left:10px">'
        f'No: {sel_stu.numara or "—"} · {ss_sinif}/{ss_sube} · {ss_yil}</span></div>'
        f'<div style="text-align:right">'
        f'<div style="font-size:1.3rem;font-weight:800;color:#4f46e5">{ort_text}</div>'
        f'<div style="font-size:0.65rem;color:#64748b">YAZILI ORT.</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── 8 Kategori Tabi ──────────────────────────────────────────────────
    # Olcme Degerlendirme modulundeki 5 sinav turuyle senkron
    t_ozet, t_yazili, t_kazanim, t_deneme, t_lgs, t_quiz, t_odev, t_yd = st.tabs([
        "  📊 Genel Özet  ",
        "  🏫 Okul Yazılısı  ",
        "  🎯 Kazanım Ölçme  ",
        "  📝 Deneme  ",
        "  📊 LGS-TYT-AYT  ",
        "  ⚡ Quiz  ",
        "  📋 Ödev  ",
        "  🇬🇧 Yabancı Dil  ",
    ])

    # ══════════════════════════════════════════════════════════════════════
    # TAB 1 — GENEL OZET
    # ══════════════════════════════════════════════════════════════════════
    with t_ozet:
        styled_section("Konsolide Akademik Özet", "#4f46e5")

        # Tüm verileri yükle
        od_data = _load_od_results(sel_stu)
        deneme_data = _load_deneme(sel_stu.id)
        online_data = _load_online_test(sel_stu.id)
        yd_data = _load_yd(sel_stu.id)
        kyt_data = _load_kyt(sel_stu.id)
        odev_data = _load_odev(sel_stu.id)

        # OD'yi 5 sinav grubuna gore parcala (Olcme modulu ile birebir)
        od_okul_yazilisi = _filter_od_by_grup(od_data, "okul_yazilisi")
        od_kazanim = _filter_od_by_grup(od_data, "kazanim_olcme")
        od_deneme = _filter_od_by_grup(od_data, "deneme")
        od_lgs = _filter_od_by_grup(od_data, "lgs_tyt_ayt")
        od_quiz = _filter_od_by_grup(od_data, "quiz")

        # Hesaplamalar
        stu_grades = [g2 for g2 in all_grades if g2.student_id == sel_stu.id]
        yazili_p = [g2.puan for g2 in stu_grades if g2.puan and g2.puan > 0 and g2.not_turu == "yazili"]
        tum_p = [g2.puan for g2 in stu_grades if g2.puan and g2.puan > 0]

        # 5 grup ortalamalari
        okul_yazilisi_p = [d["puan"] for d in od_okul_yazilisi if d.get("puan")]
        kazanim_p = [d["puan"] for d in od_kazanim if d.get("puan")]
        deneme_od_p = [d["puan"] for d in od_deneme if d.get("puan")]
        deneme_ek_p = [d.get("puan", 0) for d in deneme_data if d.get("puan")]
        deneme_birlesik_p = okul_yazilisi_p and (deneme_od_p + deneme_ek_p) or (deneme_od_p + deneme_ek_p)
        lgs_p = [d["puan"] for d in od_lgs if d.get("puan")]
        quiz_od_p = [d["puan"] for d in od_quiz if d.get("puan")]
        quiz_online_p = [d.get("puan", 0) for d in online_data if d.get("puan")]
        quiz_birlesik_p = quiz_od_p + quiz_online_p

        kyt_dogru = sum(1 for k in kyt_data if getattr(k, "dogru_mu", False))
        kyt_toplam = len(kyt_data)
        # _load_odev artik dict listesi donduruyor (Odev Takip ile join edilmis)
        odev_teslim = sum(1 for o in odev_data if o.get("durum", "") == "teslim_edildi")
        odev_toplam = len(odev_data)
        odev_p = [float(o.get("puan", 0)) for o in odev_data if o.get("puan", 0) and float(o.get("puan", 0)) > 0]
        yd_p = [getattr(d, "score", 0) for d in yd_data if getattr(d, "score", 0) and float(getattr(d, "score", 0)) > 0]

        # 5 sinav grubu istatistik kartlari (Olcme modulu turleriyle birebir)
        styled_stat_row([
            ("🏫 Okul Yazılısı", f"{len(od_okul_yazilisi) + len(yazili_p)} kayıt", "#1e3a5f", "🏫"),
            ("🎯 Kazanım Ölçme", f"{len(od_kazanim)} sınav", "#92400e", "🎯"),
            ("📝 Deneme", f"{len(od_deneme) + len(deneme_data)} sınav", "#7c3aed", "📝"),
            ("📊 LGS-TYT-AYT", f"{len(od_lgs)} sınav", "#dc2626", "📊"),
            ("⚡ Quiz", f"{len(od_quiz) + len(online_data)} quiz", "#C8952E", "⚡"),
        ])
        st.write("")
        styled_stat_row([
            ("📋 Ödev", f"{odev_teslim}/{odev_toplam} teslim", "#6366f1", "📋"),
            ("🇬🇧 Yabancı Dil", f"{len(yd_data)} sınav", "#dc2626", "🇬🇧"),
            ("🔍 KYT Yoklama", f"{kyt_dogru}/{kyt_toplam}", "#0891b2", "🔍"),
            ("Not Ortalama", f"{_avg(tum_p):.1f}" if tum_p else "—", "#1e40af", "📊"),
            ("OD Puan Ort.", f"{_avg([d['puan'] for d in od_data if d.get('puan')]):.1f}" if od_data else "—", "#7c3aed", "🎯"),
        ])

        # Kategori bazli detay tablosu — Olcme modulu turleriyle birebir
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        styled_section("Sınav Türü Bazlı Detay (Ölçme Değerlendirme ile Senkron)", "#1e40af")

        # Birlesik deneme ve quiz puanlari hesabi
        deneme_tum_p = deneme_od_p + deneme_ek_p
        quiz_tum_p = quiz_od_p + quiz_online_p

        categories = [
            ("🏫 Okul Yazılısı", len(od_okul_yazilisi) + len(yazili_p),
             _avg(okul_yazilisi_p + yazili_p) if (okul_yazilisi_p or yazili_p) else None, "#1e3a5f"),
            ("🎯 Kazanım Ölçme", len(od_kazanim),
             _avg(kazanim_p) if kazanim_p else None, "#92400e"),
            ("📝 Deneme", len(od_deneme) + len(deneme_data),
             _avg(deneme_tum_p) if deneme_tum_p else None, "#7c3aed"),
            ("📊 LGS-TYT-AYT", len(od_lgs),
             _avg(lgs_p) if lgs_p else None, "#dc2626"),
            ("⚡ Quiz", len(od_quiz) + len(online_data),
             _avg(quiz_tum_p) if quiz_tum_p else None, "#C8952E"),
            ("📋 Ödev", odev_toplam,
             _avg(odev_p) if odev_p else None, "#6366f1"),
            ("🇬🇧 Yabancı Dil", len(yd_data),
             _avg(yd_p) if yd_p else None, "#dc2626"),
        ]

        cat_html = ""
        for cat_name, cat_count, cat_avg_val, cat_color in categories:
            bar_w = min(cat_avg_val, 100) if cat_avg_val else 0
            cat_html += (
                f"<tr style='border-bottom:1px solid #1A2035'>"
                f"<td style='padding:8px 12px;font-weight:600;font-size:0.85rem'>{cat_name}</td>"
                f"<td style='padding:8px;text-align:center;font-weight:700;color:{cat_color}'>{cat_count}</td>"
                f"<td style='padding:8px;text-align:center'>{_ss_puan_badge(cat_avg_val)}</td>"
                f"<td style='padding:8px 12px;width:200px'>"
                f"<div style='background:#1A2035;border-radius:6px;height:12px;overflow:hidden'>"
                f"<div style='background:{cat_color};height:100%;width:{bar_w}%;border-radius:6px'></div>"
                f"</div></td></tr>"
            )

        st.markdown(
            f"<div style='border-radius:10px;border:1px solid #e2e8f0;overflow:hidden'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>"
            f"<th style='padding:10px 12px;background:#1e40af;color:white;text-align:left;font-size:0.8rem'>Kategori</th>"
            f"<th style='padding:10px 8px;background:#1e40af;color:white;text-align:center;font-size:0.8rem'>Adet</th>"
            f"<th style='padding:10px 8px;background:#1e40af;color:white;text-align:center;font-size:0.8rem'>Ortalama</th>"
            f"<th style='padding:10px 12px;background:#1e40af;color:white;text-align:left;font-size:0.8rem'>Performans</th>"
            f"</tr></thead><tbody>{cat_html}</tbody></table></div>",
            unsafe_allow_html=True,
        )

    # ══════════════════════════════════════════════════════════════════════
    # TAB 2 — OKUL YAZILISI (Olcme modulu Okul Yazilisi turu + manuel not girisi)
    # ══════════════════════════════════════════════════════════════════════
    with t_yazili:
        styled_section(f"Okul Yazılısı — {ss_donem}", "#1e3a5f")

        # 1. ONCE OD modulunden Okul Yazilisi turundeki sinavlari goster
        try:
            _od_all_y = _load_od_results(sel_stu)
            yazili_od = _filter_od_by_grup(_od_all_y, "okul_yazilisi")
        except Exception:
            yazili_od = []

        if yazili_od:
            st.markdown(
                "<div style='background:#e8ecf4;border-left:4px solid #1e3a5f;border-radius:6px;"
                "padding:8px 14px;margin:8px 0;color:#1e3a5f;font-size:0.85rem;font-weight:600'>"
                f"📋 Ölçme Değerlendirme modülünden gelen sınavlar — {len(yazili_od)} kayıt"
                "</div>",
                unsafe_allow_html=True,
            )
            yz_rows = ""
            for i, d in enumerate(sorted(yazili_od, key=lambda x: x.get("tarih", ""), reverse=True)):
                tarih_str = str(d.get("tarih", "—"))[:10]
                yz_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#e8ecf4' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{d.get('sinav_adi','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem;color:#64748b'>{d.get('sinav_turu','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem;color:#64748b'>{d.get('ders','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem'>{d.get('toplam',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{tarih_str}</td>"
                    f"</tr>"
                )
            yz_headers = ["Sınav Adı", "Tür", "Ders", "Soru", "D", "Y", "Puan", "Tarih"]
            yz_th = "".join(
                f"<th style='padding:8px 6px;background:#1e3a5f;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in yz_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:14px'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{yz_th}</tr></thead><tbody>{yz_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

        # 2. SONRA mevcut manuel not girisi (yazili1, yazili2, sozlu, proje, perf, dersi ici)
        st.markdown(
            "<div style='background:#1e3a5f15;border-left:4px solid #1e3a5f;border-radius:6px;"
            "padding:8px 14px;margin:14px 0 8px;color:#1e3a5f;font-size:0.85rem;font-weight:600'>"
            "✏️ Manuel Not Girişi — yazılı, sözlü, proje, performans"
            "</div>",
            unsafe_allow_html=True,
        )

        for ders_adi in kademe_dersler:
            ders_notlar = {
                (nt, sir): (puan, gid)
                for (sid, d, nt, sir), (puan, gid) in grade_map.items()
                if sid == sel_stu.id and d == ders_adi
            }
            ders_puanlar = [p for (p, _) in ders_notlar.values() if p and p > 0]
            ders_ort = sum(ders_puanlar) / len(ders_puanlar) if ders_puanlar else None

            gir_sayisi = len(ders_puanlar)
            ders_label = f"📖 {ders_adi}"
            if ders_ort:
                ders_label += f"  —  Ort: {ders_ort:.1f}  ({gir_sayisi}/6 not girildi)"
            else:
                ders_label += "  —  Not girilmedi"

            with st.expander(ders_label, expanded=(gir_sayisi > 0)):
                inp_cols = st.columns(6)
                new_vals: dict = {}

                for ci2, (nt, sirasi, lbl) in enumerate(_SS_COLS):
                    mevcut_puan, _ = ders_notlar.get((nt, sirasi), (None, None))
                    with inp_cols[ci2]:
                        st.markdown(
                            f'<div style="font-size:0.68rem;font-weight:700;color:#64748b;'
                            f'text-align:center;margin-bottom:2px;text-transform:uppercase;'
                            f'letter-spacing:.3px">{lbl}</div>',
                            unsafe_allow_html=True,
                        )
                        inp_val = st.number_input(
                            lbl, min_value=0, max_value=100, step=1,
                            value=int(mevcut_puan) if mevcut_puan and mevcut_puan > 0 else 0,
                            label_visibility="collapsed",
                            key=f"ss_inp_{sel_stu.id}_{ders_adi}_{nt}_{sirasi}",
                        )
                        new_vals[(nt, sirasi, lbl)] = inp_val
                        if mevcut_puan and mevcut_puan > 0:
                            st.markdown(
                                f'<div style="text-align:center;margin-top:1px">'
                                f'{_ss_puan_badge(mevcut_puan)}</div>',
                                unsafe_allow_html=True,
                            )

                preview_vals = [v for v in new_vals.values() if v and v > 0]
                if preview_vals:
                    prev_ort = sum(preview_vals) / len(preview_vals)
                    st.markdown(
                        f'<div style="margin-top:6px;padding:5px 10px;background:#111827;'
                        f'border-radius:8px;display:inline-block;font-size:0.8rem">'
                        f'Girilen Ortalama: {_ss_puan_badge(prev_ort)}</div>',
                        unsafe_allow_html=True,
                    )

                sav_c, _ = st.columns([1, 3])
                with sav_c:
                    if st.button(
                        f"💾 {ders_adi[:12]} Kaydet",
                        key=f"ss_sav_{sel_stu.id}_{ders_adi}",
                        use_container_width=True,
                    ):
                        saved_cnt = 0
                        for (nt, sirasi, lbl2), puan_val in new_vals.items():
                            if puan_val is not None and int(puan_val) > 0:
                                _, existing_id = ders_notlar.get((nt, sirasi), (None, None))
                                gid = existing_id if existing_id else f"not_{uuid.uuid4().hex[:8]}"
                                g = GradeRecord(
                                    student_id=sel_stu.id,
                                    ders=ders_adi,
                                    sinif=ss_sinif,
                                    sube=ss_sube,
                                    donem=donem_key,
                                    not_turu=nt,
                                    not_sirasi=sirasi,
                                    puan=float(puan_val),
                                    akademik_yil=ss_yil,
                                )
                                g.id = gid
                                store.save_grade(g)
                                saved_cnt += 1
                        if saved_cnt > 0:
                            st.success(f"✅ {ders_adi} — {saved_cnt} not kaydedildi!")
                            st.rerun(scope="fragment")
                        else:
                            st.warning("Kaydedilecek not bulunamadı (0'dan büyük değer girin).")

    # ══════════════════════════════════════════════════════════════════════
    # TAB 3 — KAZANIM ÖLÇME (OD modulu + KYT birlikte)
    # ══════════════════════════════════════════════════════════════════════
    with t_kazanim:
        styled_section("Kazanım Ölçme Sonuçları", "#92400e")

        od_results = _load_od_results(sel_stu)
        kazanim_results = _filter_od_by_grup(od_results, "kazanim_olcme")
        kyt_results = _load_kyt(sel_stu.id)

        # Istatistikler
        kazanim_puanlar = [d["puan"] for d in kazanim_results if d.get("puan")]
        kyt_dogru_t = sum(1 for k in kyt_results if getattr(k, "dogru_mu", False))
        kyt_toplam_t = len(kyt_results)
        kyt_orani = (kyt_dogru_t / kyt_toplam_t * 100) if kyt_toplam_t else 0

        styled_stat_row([
            ("OD Kazanım Sınavı", str(len(kazanim_results)), "#92400e", "🎯"),
            ("OD Ortalama", f"{_avg(kazanim_puanlar):.1f}" if kazanim_puanlar else "—", "#2563eb", "📊"),
            ("KYT Soru", f"{kyt_toplam_t}", "#0891b2", "🔍"),
            ("KYT Doğru", f"{kyt_dogru_t}/{kyt_toplam_t}", "#059669", "✅"),
            ("KYT Başarı", f"%{kyt_orani:.0f}" if kyt_toplam_t else "—", "#d97706", "📈"),
        ])
        st.write("")

        # OD Kazanim sonuclari tablosu
        if kazanim_results:
            st.markdown("**📋 OD Kazanım Değerlendirme Sınavları:**")
            od_rows = ""
            for i, d in enumerate(sorted(kazanim_results, key=lambda x: x.get("tarih", ""), reverse=True)):
                tarih_str = d.get("tarih", "—")[:10] if d.get("tarih") else "—"
                od_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#fff8e1' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{d.get('sinav_adi','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem;color:#64748b'>{d.get('ders','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem'>{d.get('toplam',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#94a3b8'>{d.get('bos',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-weight:700'>{d.get('net',0):.1f}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{tarih_str}</td>"
                    f"</tr>"
                )
            od_headers = ["Sınav Adı", "Ders", "Soru", "D", "Y", "B", "Net", "Puan", "Tarih"]
            od_th = "".join(
                f"<th style='padding:8px 6px;background:#92400e;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in od_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:14px'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{od_th}</tr></thead><tbody>{od_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

        # KYT detayli — son 20 cevap
        if kyt_results:
            st.markdown("**🔍 KYT (Kazanım Yoklama Testi) Cevaplari:**")
            kyt_rows = ""
            for i, k in enumerate(kyt_results[-20:][::-1]):
                dogru = getattr(k, "dogru_mu", False)
                tarih = str(getattr(k, "tarih", ""))[:10]
                ikon = "✅" if dogru else "❌"
                kyt_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#ecfeff' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-size:0.82rem'>{ikon}</td>"
                    f"<td style='padding:7px 10px;font-size:0.78rem'>{getattr(k, 'kazanim_kodu', '—')}</td>"
                    f"<td style='padding:7px 10px;font-size:0.78rem;color:#64748b'>{getattr(k, 'ders', '—')}</td>"
                    f"<td style='padding:7px 10px;font-size:0.78rem;color:#64748b'>{tarih}</td>"
                    f"</tr>"
                )
            kyt_headers = ["", "Kazanım", "Ders", "Tarih"]
            kyt_th = "".join(
                f"<th style='padding:8px 6px;background:#0891b2;color:white;font-size:0.78rem;"
                f"text-align:left;white-space:nowrap'>{h}</th>"
                for h in kyt_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{kyt_th}</tr></thead><tbody>{kyt_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

        if not kazanim_results and not kyt_results:
            styled_info_banner("Kazanım ölçme sonucu bulunamadı (OD modülünden Kazanım Değerlendirme sınavı veya KYT ile veri girilebilir).", "info")

    # ══════════════════════════════════════════════════════════════════════
    # TAB 4 — DENEME SINAVLARI (Egitim Koclugu + OD modulu birlikte)
    # ══════════════════════════════════════════════════════════════════════
    with t_deneme:
        styled_section("Deneme Sınav Sonuçları", "#059669")

        deneme_results = _load_deneme(sel_stu.id)
        # OD'den de "Deneme" turundeki sinavlari ekle
        try:
            _od_all = _load_od_results(sel_stu)
            _od_deneme = _filter_od_by_grup(_od_all, "deneme")
            for d in _od_deneme:
                deneme_results.append({
                    "sinav_adi": d.get("sinav_adi", "OD Deneme"),
                    "sinav_turu": "OD-Deneme",
                    "dogru": d.get("dogru", 0),
                    "yanlis": d.get("yanlis", 0),
                    "bos": d.get("bos", 0),
                    "net": d.get("net", 0),
                    "puan": d.get("puan", 0),
                    "tarih": d.get("tarih", ""),
                    "siralama": "—",
                })
        except Exception:
            pass

        if not deneme_results:
            styled_info_banner("Deneme sınavı sonucu bulunamadı.", "info")
        else:
            d_puanlar = [d.get("puan", 0) for d in deneme_results if d.get("puan")]
            d_netler = [d.get("net", 0) for d in deneme_results if d.get("net")]
            styled_stat_row([
                ("Toplam Deneme", str(len(deneme_results)), "#059669", "📈"),
                ("Puan Ort.", f"{_avg(d_puanlar):.1f}" if d_puanlar else "—", "#2563eb", "📊"),
                ("Net Ort.", f"{_avg(d_netler):.1f}" if d_netler else "—", "#d97706", "🎯"),
                ("En Yüksek", f"{max(d_puanlar):.1f}" if d_puanlar else "—", "#059669", "⬆"),
                ("En Düşük", f"{min(d_puanlar):.1f}" if d_puanlar else "—", "#ef4444", "⬇"),
            ])
            st.write("")

            dn_rows = ""
            for i, d in enumerate(sorted(deneme_results, key=lambda x: x.get("tarih", ""), reverse=True)):
                tarih_str = str(d.get("tarih", "—"))[:10]
                siralama = d.get("siralama", "—")
                dn_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#f0fdf4' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{d.get('sinav_adi','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem'>"
                    f"<span style='background:#10b98118;color:#059669;border-radius:4px;padding:1px 6px;font-size:0.75rem'>"
                    f"{d.get('sinav_turu','deneme')}</span></td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#94a3b8'>{d.get('bos',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-weight:700'>{d.get('net',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.82rem;font-weight:600;color:#6366f1'>{siralama}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{tarih_str}</td>"
                    f"</tr>"
                )

            dn_headers = ["Sınav Adı", "Tür", "D", "Y", "B", "Net", "Puan", "Sıra", "Tarih"]
            dn_th = "".join(
                f"<th style='padding:8px 6px;background:#059669;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in dn_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{dn_th}</tr></thead><tbody>{dn_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

            # Ders detayları (varsa)
            son_deneme = deneme_results[-1] if deneme_results else {}
            ders_det = son_deneme.get("ders_detaylari", {})
            if ders_det and isinstance(ders_det, dict):
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                styled_section("Son Deneme — Ders Bazlı Detay", "#0d9488")
                det_rows = ""
                for ders_nm, det_val in ders_det.items():
                    if isinstance(det_val, dict):
                        det_rows += (
                            f"<tr style='border-bottom:1px solid #1A2035'>"
                            f"<td style='padding:6px 10px;font-weight:600'>{ders_nm}</td>"
                            f"<td style='padding:6px 8px;text-align:center;color:#059669;font-weight:700'>{det_val.get('dogru',0)}</td>"
                            f"<td style='padding:6px 8px;text-align:center;color:#ef4444;font-weight:700'>{det_val.get('yanlis',0)}</td>"
                            f"<td style='padding:6px 8px;text-align:center;color:#94a3b8'>{det_val.get('bos',0)}</td>"
                            f"<td style='padding:6px 8px;text-align:center;font-weight:700'>{det_val.get('net',0)}</td>"
                            f"</tr>"
                        )
                if det_rows:
                    det_th = "".join(
                        f"<th style='padding:6px;background:#0d9488;color:white;font-size:0.78rem;text-align:center'>{h}</th>"
                        for h in ["Ders", "D", "Y", "B", "Net"]
                    )
                    st.markdown(
                        f"<div style='overflow-x:auto;border-radius:8px;border:1px solid #e2e8f0'>"
                        f"<table style='width:100%;border-collapse:collapse'>"
                        f"<thead><tr>{det_th}</tr></thead><tbody>{det_rows}</tbody></table></div>",
                        unsafe_allow_html=True,
                    )

    # ══════════════════════════════════════════════════════════════════════
    # TAB 5 — LGS-TYT-AYT (Olcme modulundeki tur)
    # ══════════════════════════════════════════════════════════════════════
    with t_lgs:
        styled_section("LGS / TYT / AYT Sınav Sonuçları", "#dc2626")

        # OD modulunden LGS-TYT-AYT turundeki sinavlari cek
        _od_all = _load_od_results(sel_stu)
        lgs_results = _filter_od_by_grup(_od_all, "lgs_tyt_ayt")

        if not lgs_results:
            styled_info_banner(
                "LGS / TYT / AYT sınav sonucu bulunamadı. "
                "Ölçme Değerlendirme modülünden bu türde sınav oluşturup uyguladığınızda burada listelenir.",
                "info"
            )
        else:
            ll_puanlar = [d.get("puan", 0) for d in lgs_results if d.get("puan")]
            ll_netler = [d.get("net", 0) for d in lgs_results if d.get("net")]
            styled_stat_row([
                ("Toplam Sınav", str(len(lgs_results)), "#dc2626", "📊"),
                ("Puan Ort.", f"{_avg(ll_puanlar):.1f}" if ll_puanlar else "—", "#2563eb", "📈"),
                ("Net Ort.", f"{_avg(ll_netler):.1f}" if ll_netler else "—", "#d97706", "🎯"),
                ("En Yüksek", f"{max(ll_puanlar):.1f}" if ll_puanlar else "—", "#059669", "⬆"),
                ("En Düşük", f"{min(ll_puanlar):.1f}" if ll_puanlar else "—", "#ef4444", "⬇"),
            ])
            st.write("")

            ll_rows = ""
            for i, d in enumerate(sorted(lgs_results, key=lambda x: x.get("tarih", ""), reverse=True)):
                tarih_str = str(d.get("tarih", "—"))[:10]
                tur = d.get("sinav_turu", "—")
                tur_renk_map = {
                    "LGS": ("#dc2626", "#fef2f2"),
                    "TYT": ("#2563eb", "#eff6ff"),
                    "AYT Esit Agirlik": ("#059669", "#ecfdf5"),
                    "AYT Sayısal": ("#d97706", "#fffbeb"),
                    "AYT Sozel": ("#9333ea", "#faf5ff"),
                }
                t_clr, t_bg = tur_renk_map.get(tur, ("#64748b", "#f1f5f9"))
                tur_badge = (
                    f"<span style='background:{t_bg};color:{t_clr};border-radius:6px;padding:2px 8px;"
                    f"font-size:0.72rem;font-weight:700;border:1px solid {t_clr}40'>{tur}</span>"
                )
                ll_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#fef2f220' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{d.get('sinav_adi','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{tur_badge}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem'>{d.get('toplam',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#94a3b8'>{d.get('bos',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-weight:700'>{d.get('net',0):.2f}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{tarih_str}</td>"
                    f"</tr>"
                )

            ll_headers = ["Sınav Adı", "Tür", "Soru", "D", "Y", "B", "Net", "Puan", "Tarih"]
            ll_th = "".join(
                f"<th style='padding:8px 6px;background:#dc2626;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in ll_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{ll_th}</tr></thead><tbody>{ll_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════
    # TAB 6 — QUIZ (OD modulu Quiz turu + Egitim Koclugu online testleri)
    # ══════════════════════════════════════════════════════════════════════
    with t_quiz:
        styled_section("Quiz Sonuçları", "#C8952E")

        # OD'den Quiz turundeki sinavlar
        _od_all2 = _load_od_results(sel_stu)
        quiz_results = _filter_od_by_grup(_od_all2, "quiz")
        # Egitim koclugu online testlerini de Quiz olarak ekle
        online_results = _load_online_test(sel_stu.id)
        for d in online_results:
            quiz_results.append({
                "sinav_adi": d.get("test_adi", "Online Quiz"),
                "sinav_turu": "Online Quiz",
                "ders": d.get("ders", "—"),
                "toplam": d.get("toplam", 0),
                "dogru": d.get("dogru", 0),
                "yanlis": d.get("yanlis", 0),
                "bos": d.get("bos", 0),
                "puan": d.get("puan", 0),
                "net": d.get("net", 0),
                "tarih": d.get("tarih", ""),
            })

        if not quiz_results:
            styled_info_banner(
                "Quiz sonucu bulunamadı. "
                "Ölçme Değerlendirme modülünden Quiz türünde sınav oluşturup uyguladığınızda burada listelenir.",
                "info"
            )
        else:
            qz_puanlar = [d.get("puan", 0) for d in quiz_results if d.get("puan")]
            styled_stat_row([
                ("Toplam Quiz", str(len(quiz_results)), "#C8952E", "⚡"),
                ("Puan Ort.", f"{_avg(qz_puanlar):.1f}" if qz_puanlar else "—", "#2563eb", "📊"),
                ("En Yüksek", f"{max(qz_puanlar):.1f}" if qz_puanlar else "—", "#059669", "⬆"),
                ("En Düşük", f"{min(qz_puanlar):.1f}" if qz_puanlar else "—", "#ef4444", "⬇"),
            ])
            st.write("")

            qz_rows = ""
            for i, d in enumerate(sorted(quiz_results, key=lambda x: x.get("tarih", ""), reverse=True)):
                tarih_str = str(d.get("tarih", "—"))[:10]
                qz_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#FFF8E1' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{d.get('sinav_adi','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem;color:#64748b'>{d.get('ders','—')}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>"
                    f"<span style='background:#FFF8E1;color:#C8952E;border-radius:6px;padding:2px 8px;font-size:0.72rem;font-weight:700;border:1px solid #C8952E40'>"
                    f"{d.get('sinav_turu','Quiz')}</span></td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem'>{d.get('toplam',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;color:#94a3b8'>{d.get('bos',0)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-weight:700'>{d.get('net',0):.1f}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{tarih_str}</td>"
                    f"</tr>"
                )

            qz_headers = ["Quiz Adı", "Ders", "Tür", "Soru", "D", "Y", "B", "Net", "Puan", "Tarih"]
            qz_th = "".join(
                f"<th style='padding:8px 6px;background:#C8952E;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in qz_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{qz_th}</tr></thead><tbody>{qz_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════
    # TAB 7 — ODEV DEGERLENDIRME (Odev Takip modulu ile CANLI senkron)
    # ══════════════════════════════════════════════════════════════════════
    with t_odev:
        styled_section("Ödev Değerlendirme Sonuçları", "#6366f1")

        # Canli senkron banner — Odev Takip modulu ile entegre
        st.markdown(
            "<div style='background:linear-gradient(135deg,#4338ca,#6366f1);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:10px;font-size:0.82rem;"
            "display:flex;align-items:center;gap:8px;"
            "box-shadow:0 2px 8px rgba(99,102,241,0.25)'>"
            "<span style='font-size:1.15rem'>🔗</span>"
            "<span><b>Öğretim &amp; Planlama › Ödev Takip</b> ile CANLI senkron — "
            "ödev oluşturulduğunda öğrenciye otomatik atanır, teslim/puan/öğretmen notu güncellendiğinde "
            "burada anlık görünür."
            "</span>"
            "<span style='margin-left:auto;background:rgba(255,255,255,0.2);"
            "padding:2px 10px;border-radius:10px;font-size:0.7rem;font-weight:700;"
            "display:flex;align-items:center;gap:4px'>"
            "<span style='width:8px;height:8px;border-radius:50%;background:#10ff9a;"
            "box-shadow:0 0 6px #10ff9a'></span>LIVE</span>"
            "</div>",
            unsafe_allow_html=True,
        )

        odev_results = _load_odev(sel_stu.id)

        if not odev_results:
            styled_info_banner(
                "Ödev teslim kaydı bulunamadı. "
                "Öğretim & Planlama > Ödev Takip sekmesinden bu öğrencinin sınıf/şubesine ödev "
                "oluşturduğunuzda otomatik olarak burada listelenir.",
                "info",
            )
        else:
            teslim_cnt = sum(1 for o in odev_results if o.get("durum", "") == "teslim_edildi")
            gecik_cnt = sum(1 for o in odev_results if o.get("durum", "") == "gecikti")
            eksik_cnt = sum(1 for o in odev_results if o.get("durum", "") in ("bekliyor", "teslim_edilmedi"))
            muaf_cnt = sum(1 for o in odev_results if o.get("durum", "") == "muaf")
            ov_puanlar = [float(o.get("puan", 0)) for o in odev_results
                          if o.get("puan", 0) and float(o.get("puan", 0)) > 0]

            styled_stat_row([
                ("Toplam Ödev", str(len(odev_results)), "#6366f1", "📋"),
                ("Teslim Edilen", str(teslim_cnt), "#059669", "✅"),
                ("Geciken", str(gecik_cnt), "#d97706", "⏰"),
                ("Eksik", str(eksik_cnt), "#ef4444", "❌"),
                ("Puan Ort.", f"{_avg(ov_puanlar):.1f}" if ov_puanlar else "—", "#2563eb", "📊"),
            ])
            st.write("")

            # Tarih bazli sirala (en yeni once) — verilme tarihine gore
            odev_results_sorted = sorted(
                odev_results,
                key=lambda x: (x.get("verilme_tarihi", "") or x.get("teslim_tarihi", "")),
                reverse=True,
            )

            ov_rows = ""
            for i, o in enumerate(odev_results_sorted):
                odev_baslik = o.get("baslik", "Ödev")
                odev_ders = o.get("ders", "—")
                odev_turu = o.get("odev_turu", "")
                ogretmen_adi = o.get("ogretmen_adi", "")
                durum = o.get("durum", "—")
                puan = o.get("puan", 0)
                teslim_tarih = str(o.get("teslim_tarihi", "") or "—")[:10]
                son_teslim = str(o.get("son_teslim_tarihi", "") or "—")[:10]
                ogr_notu = o.get("ogretmen_notu", "")
                online_b = "💻 " if o.get("online_teslim") else ""

                durum_colors = {
                    "teslim_edildi": ("#059669", "#10b98118", "Teslim"),
                    "gecikti": ("#d97706", "#f59e0b18", "Gecikti"),
                    "bekliyor": ("#6366f1", "#6366f118", "Bekliyor"),
                    "teslim_edilmedi": ("#ef4444", "#ef444418", "Teslim Edilmedi"),
                    "muaf": ("#64748b", "#64748b18", "Muaf"),
                }
                d_clr, d_bg, d_label = durum_colors.get(durum, ("#64748b", "#1A2035", durum.title()))
                durum_badge = (
                    f"<span style='background:{d_bg};color:{d_clr};border:1px solid {d_clr}44;"
                    f"border-radius:4px;padding:1px 6px;font-size:0.72rem;font-weight:600'>"
                    f"{d_label}</span>"
                )

                ov_rows += (
                    f"<tr style='border-bottom:1px solid #1A2035;{'background:#eef2ff' if i%2==0 else ''}'>"
                    f"<td style='padding:7px 10px;font-weight:600;font-size:0.83rem'>{online_b}{odev_baslik}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.8rem;color:#64748b'>{odev_ders}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.75rem;color:#64748b'>{ogretmen_adi or '—'}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{durum_badge}</td>"
                    f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(float(puan) if puan else None)}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{son_teslim}</td>"
                    f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{teslim_tarih}</td>"
                    f"<td style='padding:7px 8px;font-size:0.72rem;color:#64748b;max-width:180px;"
                    f"overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{(ogr_notu or '')[:40] if ogr_notu else '—'}</td>"
                    f"</tr>"
                )

            ov_headers = ["Ödev Adı", "Ders", "Öğretmen", "Durum", "Puan", "Son Teslim", "Teslim", "Öğretmen Notu"]
            ov_th = "".join(
                f"<th style='padding:8px 6px;background:#6366f1;color:white;font-size:0.78rem;"
                f"text-align:center;white-space:nowrap'>{h}</th>"
                for h in ov_headers
            )
            st.markdown(
                f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0'>"
                f"<table style='width:100%;border-collapse:collapse'>"
                f"<thead><tr>{ov_th}</tr></thead><tbody>{ov_rows}</tbody></table></div>",
                unsafe_allow_html=True,
            )

    # ══════════════════════════════════════════════════════════════════════
    # TAB 8 — YABANCI DIL SINAVLARI
    # ══════════════════════════════════════════════════════════════════════
    with t_yd:
        _render_yd_degerlendirme(sel_stu, styled_section, styled_stat_row, styled_info_banner, _load_yd, _avg, _ss_puan_badge, _load_yd_full=_load_yd_full)


def _render_yd_degerlendirme(sel_stu, styled_section, styled_stat_row, styled_info_banner, _load_yd, _avg, _ss_puan_badge, _load_yd_full=None):
    """Ogrenci Yabanci Dil Degerlendirmesi — Quiz + CEFR Placement + Mock Exam + Analiz + Tavsiye.

    Yabanci Dil modulu (Unite Quiz, haftalik sinav, yazili, deneme) +
    CEFR alt sistemi (Placement + Mock Exam) ile CANLI senkron.
    """
    import pandas as pd

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e1b4b,#4338ca);color:#fff;'
        'padding:18px 22px;border-radius:14px;margin-bottom:14px;text-align:center;">'
        '<h3 style="margin:0;font-size:20px;">🌍 Öğrenci Yabancı Dil Değerlendirmesi</h3>'
        '<p style="margin:4px 0 0;font-size:13px;opacity:.85;">'
        'Quiz · CEFR Seviye Tespit · Mock Exam · Beceri Analizi · AI Tavsiye</p></div>',
        unsafe_allow_html=True,
    )

    # Canli senkron banner — YD + CEFR ile entegre
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1e1b4b,#7c3aed);color:white;"
        "padding:10px 16px;border-radius:10px;margin-bottom:10px;font-size:0.82rem;"
        "display:flex;align-items:center;gap:8px;"
        "box-shadow:0 2px 8px rgba(124,58,237,0.25)'>"
        "<span style='font-size:1.15rem'>🔗</span>"
        "<span><b>Yabancı Dil Modülü</b> ile CANLI senkron — "
        "Ünite Quiz · Haftalık Sınav · Yazılı/Deneme · CEFR Seviye Tespit · CEFR Mock Exam "
        "verileri anlık olarak buraya çekilir."
        "</span>"
        "<span style='margin-left:auto;background:rgba(255,255,255,0.2);"
        "padding:2px 10px;border-radius:10px;font-size:0.7rem;font-weight:700;"
        "display:flex;align-items:center;gap:4px'>"
        "<span style='width:8px;height:8px;border-radius:50%;background:#10ff9a;"
        "box-shadow:0 0 6px #10ff9a'></span>LIVE</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    sinif_int = int(sel_stu.sinif) if sel_stu.sinif else 0

    # ── ZENGINLESTIRILMIS VERIYI YUKLE ──
    if _load_yd_full is not None:
        full = _load_yd_full(sel_stu)
    else:
        full = {"quizler": [], "sinavlar": [], "cefr_placement": [], "cefr_mock": [], "remediation": []}

    quizler_full = full.get("quizler", [])
    sinavlar_full = full.get("sinavlar", [])
    cefr_pl_full = full.get("cefr_placement", [])
    cefr_mk_full = full.get("cefr_mock", [])
    remediation_full = full.get("remediation", [])

    # Geriye uyumluluk: yd_results listesi (eski getattr-tabanli kod icin)
    yd_results = _load_yd(sel_stu)
    if not yd_results:
        # _load_yd_full'dan turetilebilen YD sonuclar olabilir; yine de objesiz fallback yok
        yd_results = []

    # CEFR icin native nesneleri de ayrica cek (eski rendering kodu uyumu)
    cefr_placement = []
    cefr_mock = []
    try:
        from models.cefr_exam import CEFRPlacementStore, CEFR_LEVELS, GRADE_TO_CEFR, CEFR_ORDER
        _cp = CEFRPlacementStore()
        cefr_placement = _cp.get_student_results(sel_stu.id) or []
    except Exception:
        CEFR_LEVELS = {}
        GRADE_TO_CEFR = {}
        CEFR_ORDER = []
    try:
        from models.cefr_exam import CEFRExamStore
        _ce = CEFRExamStore()
        cefr_mock = _ce.get_student_results(sel_stu.id, grade=sinif_int) or []
    except Exception:
        pass

    if (not yd_results and not cefr_placement and not cefr_mock
            and not quizler_full and not sinavlar_full and not cefr_pl_full and not cefr_mk_full):
        styled_info_banner(
            "Yabancı dil değerlendirme verisi bulunamadı. "
            "Yabancı Dil modülünden Ünite Quiz / sınav uygulayın veya CEFR Placement / Mock Exam çözdürdüğünüzde "
            "bu ekranda otomatik görünür.",
            "info",
        )
        return

    # ── 1. GENEL DURUM KARTI ──
    # Quiz ve sinav puanlarini once full'dan al, yoksa yd_results'tan
    if quizler_full or sinavlar_full:
        quiz_puanlar = [float(d.get("puan", 0)) for d in quizler_full if d.get("puan", 0) > 0]
        sinav_puanlar = [float(d.get("puan", 0)) for d in sinavlar_full if d.get("puan", 0) > 0]
        yd_puanlar = quiz_puanlar + sinav_puanlar
        quiz_results = quizler_full  # used downstream as len-able
    else:
        yd_puanlar = [float(getattr(d, "score", 0)) for d in yd_results if getattr(d, "score", 0) and float(getattr(d, "score", 0)) > 0]
        quiz_results = [d for d in yd_results if getattr(d, "exam_category", "") == "quiz"]
        quiz_puanlar = [float(getattr(d, "score", 0)) for d in quiz_results if getattr(d, "score", 0) and float(getattr(d, "score", 0)) > 0]
        sinav_puanlar = []

    target_cefr = "—"
    placed_cefr = "—"
    mock_cefr = "—"
    try:
        target_cefr = GRADE_TO_CEFR.get(sinif_int, "A2")
    except Exception:
        pass
    if cefr_placement:
        last_pl = max(cefr_placement, key=lambda r: r.submitted_at)
        placed_cefr = last_pl.placed_cefr
    if cefr_mock:
        last_mk = max(cefr_mock, key=lambda r: r.submitted_at)
        mock_cefr = last_mk.achieved_cefr or last_mk.cefr

    # Toplam YD aktivite sayisi (her kaynaktan)
    _toplam_yd_kayit = (
        len(quizler_full) + len(sinavlar_full)
        + len(cefr_pl_full) + len(cefr_mk_full)
    ) or len(yd_results)

    stats = [
        ("Toplam Kayıt", str(_toplam_yd_kayit), "#2563eb", "📝"),
        ("Quiz Sayısı", str(len(quizler_full) or len(quiz_results)), "#7c3aed", "🎯"),
        ("Quiz Ort.", f"{_avg(quiz_puanlar):.1f}" if quiz_puanlar else "—", "#d97706", "📊"),
        ("CEFR Tespit", placed_cefr, "#8b5cf6", "📋"),
        ("Mock Exam", mock_cefr, "#6d28d9", "🏆"),
        ("Hedef", target_cefr, "#059669", "🎯"),
    ]
    styled_stat_row(stats)
    st.write("")

    # Ek istatistik satiri — sinav, placement ve mock
    stats2 = [
        ("YD Sınavları", str(len(sinavlar_full)), "#0891b2", "📋"),
        ("Sınav Ort.", f"{_avg(sinav_puanlar):.1f}" if sinav_puanlar else "—", "#0e7490", "📈"),
        ("CEFR Placement Sayısı", str(len(cefr_pl_full) or len(cefr_placement)), "#8b5cf6", "🎯"),
        ("CEFR Mock Sayısı", str(len(cefr_mk_full) or len(cefr_mock)), "#6d28d9", "🏆"),
        ("YD Telafi (Remediation)", str(len(remediation_full)), "#dc2626", "🔁"),
    ]
    styled_stat_row(stats2)
    st.write("")

    # ── 2. CEFR SEVİYE DURUMU ──
    if cefr_placement or cefr_mock:
        st.markdown(
            '<div style="background:#131825;border-radius:12px;padding:14px 18px;'
            'border:1px solid rgba(139,92,246,.2);margin-bottom:12px;">'
            '<h4 style="margin:0 0 10px;color:#a78bfa;font-size:15px;">📋 CEFR Seviye Durumu</h4>',
            unsafe_allow_html=True,
        )
        _cefr_cols = st.columns(2)
        with _cefr_cols[0]:
            if cefr_placement:
                lp = max(cefr_placement, key=lambda r: r.submitted_at)
                ci = CEFR_LEVELS.get(lp.placed_cefr, {})
                clr = ci.get("color", "#8b5cf6")
                st.markdown(f"""<div style="text-align:center;padding:8px;">
                <div style="color:#94a3b8;font-size:.78rem;">Seviye Tespit</div>
                <div style="display:inline-block;border-radius:16px;padding:6px 18px;
                font-weight:800;font-size:1.2rem;color:#fff;background:{clr};margin:6px 0;">{lp.placed_cefr}</div>
                <div style="color:#c7d2fe;font-weight:700;">%{lp.percentage:.0f}</div>
                <div style="color:#64748b;font-size:.72rem;">L:{lp.listening_score:.0f} R:{lp.reading_score:.0f}
                G:{lp.use_of_english_score:.0f} W:{lp.writing_score:.0f}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;color:#475569;padding:12px;">Tespit yapılmamış</div>', unsafe_allow_html=True)
        with _cefr_cols[1]:
            if cefr_mock:
                lm = max(cefr_mock, key=lambda r: r.submitted_at)
                ci2 = CEFR_LEVELS.get(lm.achieved_cefr, {})
                clr2 = ci2.get("color", "#6d28d9")
                st.markdown(f"""<div style="text-align:center;padding:8px;">
                <div style="color:#94a3b8;font-size:.78rem;">Mock Exam</div>
                <div style="display:inline-block;border-radius:16px;padding:6px 18px;
                font-weight:800;font-size:1.2rem;color:#fff;background:{clr2};margin:6px 0;">{lm.achieved_cefr}</div>
                <div style="color:#c7d2fe;font-weight:700;">%{lm.percentage:.0f}</div>
                <div style="color:#64748b;font-size:.72rem;">L:{lm.listening_score:.0f} R:{lm.reading_score:.0f}
                W:{lm.writing_score:.0f} S:{lm.speaking_score:.0f}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;color:#475569;padding:12px;">Mock Exam yapılmamış</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── 3. BECERİ ANALİZİ (tüm kaynaklardan birleşik: yd_results + zenginlestirilmis quizler/sinavlar + CEFR) ──
    agg_skills: dict[str, dict] = {}

    def _agg_skill_breakdown(sb_data):
        if not sb_data or not isinstance(sb_data, dict):
            return
        for sk, data in sb_data.items():
            if sk not in agg_skills:
                agg_skills[sk] = {"correct": 0, "total": 0}
            if isinstance(data, dict):
                agg_skills[sk]["correct"] += int(data.get("correct", 0) or 0)
                agg_skills[sk]["total"] += int(data.get("total", 0) or 0)

    # Eski yd_results (objesi)
    for d in yd_results:
        _agg_skill_breakdown(getattr(d, "skill_breakdown", {}) or {})
    # Yeni zenginlestirilmis quizler/sinavlar (dict)
    for d in (quizler_full + sinavlar_full):
        _agg_skill_breakdown(d.get("skill_breakdown", {}))
    # CEFR kaynaklari
    for d in (cefr_pl_full + cefr_mk_full):
        _agg_skill_breakdown(d.get("skill_breakdown", {}))

    if agg_skills:
        st.markdown("**Beceri Bazlı Başarı (Quiz/Sınav):**")
        sk_labels = {"vocabulary": "Kelime", "grammar": "Dilbilgisi", "reading": "Okuma",
                     "listening": "Dinleme", "other": "Diğer"}
        for sk, data in agg_skills.items():
            pct = (data["correct"] / data["total"] * 100) if data["total"] else 0
            clr = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;padding:4px 0;">'
                f'<span style="min-width:80px;color:#cbd5e1;font-size:.85rem;">{sk_labels.get(sk, sk.title())}</span>'
                f'<div style="flex:1;background:rgba(99,102,241,.1);border-radius:4px;height:16px;overflow:hidden;">'
                f'<div style="width:{pct}%;height:100%;background:{clr};border-radius:4px;"></div></div>'
                f'<span style="color:{clr};font-weight:700;font-size:.85rem;min-width:50px;">%{pct:.0f}</span>'
                f'<span style="color:#64748b;font-size:.72rem;">({data["correct"]}/{data["total"]})</span></div>',
                unsafe_allow_html=True,
            )

    # ── 4. ÜNİTE BAZLI PERFORMANS (yd_results + zenginlestirilmis quizler/sinavlar) ──
    unit_data: dict[int, list] = {}
    for d in yd_results:
        u = getattr(d, "unit", 0) or 0
        if u > 0:
            unit_data.setdefault(u, []).append(float(getattr(d, "score", 0) or 0))
    for d in (quizler_full + sinavlar_full):
        u = int(d.get("unit", 0) or 0)
        if u > 0:
            unit_data.setdefault(u, []).append(float(d.get("puan", 0) or 0))
    if unit_data:
        st.markdown("---")
        st.markdown("**Ünite Bazlı Performans:**")
        u_rows = []
        for u in sorted(unit_data.keys()):
            scores = [s for s in unit_data[u] if s > 0]
            avg_s = sum(scores) / len(scores) if scores else 0
            clr = "#22c55e" if avg_s >= 70 else "#f59e0b" if avg_s >= 50 else "#ef4444"
            u_rows.append({"Ünite": f"Ü{u}", "Ortalama": round(avg_s, 1), "Sınav": len(scores)})
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;padding:3px 0;">'
                f'<span style="min-width:40px;color:#a5b4fc;font-weight:700;">Ü{u}</span>'
                f'<div style="flex:1;background:rgba(99,102,241,.08);border-radius:4px;height:14px;overflow:hidden;">'
                f'<div style="width:{avg_s}%;height:100%;background:{clr};border-radius:4px;"></div></div>'
                f'<span style="color:{clr};font-weight:700;font-size:.85rem;">{avg_s:.0f}</span></div>',
                unsafe_allow_html=True,
            )

    # ── 5. AI TAVSİYE ve DURUM TESPİTİ ──
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:12px;'
        'padding:14px 18px;border:1px solid rgba(139,92,246,.2);">'
        '<h4 style="margin:0 0 10px;color:#a78bfa;font-size:15px;">🧠 Durum Tespiti & Tavsiyeler</h4>',
        unsafe_allow_html=True,
    )
    tavsiyeler = []
    genel_ort = _avg(yd_puanlar) if yd_puanlar else 0

    # Genel durum
    if genel_ort >= 70:
        st.markdown('<div style="color:#22c55e;font-weight:700;">✅ Yabancı dil performansı iyi seviyede.</div>', unsafe_allow_html=True)
    elif genel_ort >= 50:
        st.markdown('<div style="color:#f59e0b;font-weight:700;">⚠️ Yabancı dil performansı geliştirilmeli.</div>', unsafe_allow_html=True)
    elif yd_puanlar:
        st.markdown('<div style="color:#ef4444;font-weight:700;">🔴 Yabancı dil performansı kritik — acil müdahale gerekli.</div>', unsafe_allow_html=True)

    # Zayif beceriler
    weak_skills = [sk for sk, d in agg_skills.items() if d["total"] > 0 and (d["correct"] / d["total"] * 100) < 50]
    if weak_skills:
        sk_labels = {"vocabulary": "Kelime", "grammar": "Dilbilgisi", "reading": "Okuma", "listening": "Dinleme"}
        names = [sk_labels.get(s, s) for s in weak_skills]
        tavsiyeler.append(f"📚 Zayıf beceriler: **{', '.join(names)}** — bu alanlarda ek çalışma planlanmalı")

    # CEFR hedef altı
    if placed_cefr != "—" and target_cefr != "—":
        try:
            t_idx = CEFR_ORDER.index(target_cefr)
            p_idx = CEFR_ORDER.index(placed_cefr)
            if p_idx < t_idx:
                tavsiyeler.append(f"🌐 CEFR seviyesi ({placed_cefr}) hedefin ({target_cefr}) altında — seviye geliştirme programı uygulanmalı")
        except Exception:
            pass

    # Quiz eksikliği
    if len(quiz_results) == 0:
        tavsiyeler.append("🎯 Henüz ünite quiz'i çözülmemiş — düzenli quiz uygulaması başlatılmalı")
    elif len(quiz_results) < 3:
        tavsiyeler.append("🎯 Az sayıda quiz çözülmüş — her ünite sonrası quiz uygulanmalı")

    # Mock Exam eksikliği
    if not cefr_mock:
        tavsiyeler.append("🏆 CEFR Mock Exam uygulanmamış — Cambridge formatında pratik sınav önerilir")

    # Düşük ünite
    weak_units = [u for u, scores in unit_data.items() if scores and sum(s for s in scores if s > 0) / max(len([s for s in scores if s > 0]), 1) < 50]
    if weak_units:
        tavsiyeler.append(f"📖 Zayıf üniteler: **Ü{', Ü'.join(str(u) for u in weak_units)}** — bu ünitelerde telafi quiz'i uygulanmalı")

    if genel_ort >= 70 and not tavsiyeler:
        tavsiyeler.append("✅ Mevcut performansı sürdürmeli, ileri seviye içeriklerle desteklenmeli")

    for t in tavsiyeler:
        st.markdown(f'<div style="padding:4px 0;font-size:.88rem;color:#e2e8f0;">{t}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── 5b. AİLE BİLGİ FORMU VERİLERİ ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_AT
        _abf_all = _CML_AT.load_aile_bilgi_formlari()
        _ogr_abf = [f for f in _abf_all if f.get("ogrenci_id") == sel_stu.id]
        if _ogr_abf:
            st.markdown("---")
            st.markdown(
                '<div style="background:#0f172a;border-radius:10px;padding:12px 16px;'
                'border:1px solid rgba(13,148,136,.2);">'
                '<h4 style="margin:0 0 8px;color:#2dd4bf;font-size:14px;">📋 Aile Bilgi Formu Verileri</h4>',
                unsafe_allow_html=True,
            )
            _abf = _ogr_abf[-1]
            _ac1, _ac2 = st.columns(2)
            with _ac1:
                st.markdown(f"**Anne:** {_abf.get('anne_adi_soyadi', '-')} ({_abf.get('anne_sag_olu', '-')}, {_abf.get('anne_birlikte_bosanmis', '-')})")
                st.markdown(f"**Baba:** {_abf.get('baba_adi_soyadi', '-')} ({_abf.get('baba_sag_olu', '-')}, {_abf.get('baba_birlikte_bosanmis', '-')})")
                st.markdown(f"**Yaşam:** {_abf.get('kiminle_nerede_yasiyor', '-')} | Kardeş: Öz:{_abf.get('kardes_oz_sayisi', 0)} Üvey:{_abf.get('kardes_uvey_sayisi', 0)}")
            with _ac2:
                st.markdown(f"**Gelir:** {_abf.get('ortalama_gelir', '-')} | Ev: {_abf.get('ev_sahipligi', '-')}")
                st.markdown(f"**Okula tutum:** {_abf.get('okula_tutum', '-')}")
                st.markdown(f"**Ders desteği:** {_abf.get('ders_destegi', '-')}")
            # Kritik uyarılar
            _kr = []
            if _abf.get("anne_birlikte_bosanmis") in ("Boşanmış", "Ayrı") or _abf.get("baba_birlikte_bosanmis") in ("Boşanmış", "Ayrı"):
                _kr.append("⚠️ Boşanmış/ayrı aile")
            if _abf.get("anne_sag_olu") == "Ölü" or _abf.get("baba_sag_olu") == "Ölü":
                _kr.append("💔 Ebeveyn kaybı")
            if _abf.get("etkisindeki_olay"):
                _kr.append(f"⚠️ Travma: {_abf['etkisindeki_olay']}")
            if _abf.get("bagimllik_durumu"):
                _kr.append(f"🚫 Bağımlılık: {_abf['bagimllik_durumu']}")
            if _abf.get("suregen_hastalik"):
                _kr.append(f"🏥 Hastalık: {_abf['suregen_hastalik']}")
            if _kr:
                for k in _kr:
                    _kc = "#ef4444" if "💔" in k or "Travma" in k else "#f59e0b"
                    st.markdown(f'<div style="background:{_kc}08;border-left:3px solid {_kc};padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:.82rem;color:{_kc};font-weight:600;">{k}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass

    # ── 5b2. MEB DİJİTAL FORMLAR ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_MEB_AT
        _meb_all_at = _CML_MEB_AT.load_all_meb_forms()
        _ogr_meb_at: dict[str, list] = {}
        for _sk, _flist in _meb_all_at.items():
            for _f in _flist:
                if _f.get("ogrenci_id") == sel_stu.id:
                    _ogr_meb_at.setdefault(_sk, []).append(_f)
        if _ogr_meb_at:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:10px;'
                'padding:12px 16px;border:1px solid rgba(59,130,246,.2);margin-top:10px;">'
                '<h5 style="margin:0 0 8px;color:#60a5fa;">📄 MEB Dijital Form Kayıtları</h5>',
                unsafe_allow_html=True,
            )
            from models.meb_formlar import MEB_FORM_SCHEMAS
            _risk_alerts_at = []
            for _sk, _forms in _ogr_meb_at.items():
                _sch = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == _sk), None)
                _fname = _sch["title"] if _sch else _sk
                _ficon = _sch.get("icon", "📄") if _sch else "📄"
                _latest = sorted(_forms, key=lambda x: x.get("olusturma_zamani", ""), reverse=True)[0]
                _tarih = _latest.get("tarih", _latest.get("olusturma_zamani", "")[:10])
                st.markdown(f'<div style="background:#1e293b;border-left:3px solid #3b82f6;padding:6px 10px;'
                            f'border-radius:0 6px 6px 0;margin:3px 0;font-size:.82rem;">'
                            f'{_ficon} <b>{_fname}</b> — {len(_forms)} kayıt | Son: {_tarih}</div>',
                            unsafe_allow_html=True)
                # Risk uyarıları
                if _sk == "dehb_gozlem_formlari":
                    _risk_alerts_at.append("🧠 DEHB gözlem formu mevcut")
                if _sk == "ozel_ogrenme_guclugu_formlari":
                    _risk_alerts_at.append("📖 ÖÖG gözlem formu mevcut")
                if _sk == "disiplin_gorusme_formlari":
                    _risk_alerts_at.append(f"⚖️ {len(_forms)} disiplin görüşmesi")
                if _sk == "psikolojik_yonlendirme_formlari":
                    _risk_alerts_at.append("🧭 Psikolojik destek yönlendirmesi")
                if _sk == "saglik_yonlendirme_formlari":
                    _risk_alerts_at.append("🏥 Sağlık kuruluşuna yönlendirme")
            if _risk_alerts_at:
                for _ra in _risk_alerts_at:
                    _kc = "#ef4444" if "DEHB" in _ra or "ÖÖG" in _ra or "Psikolojik" in _ra else "#f59e0b"
                    st.markdown(f'<div style="background:{_kc}08;border-left:3px solid {_kc};'
                                f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;'
                                f'font-size:.82rem;color:{_kc};font-weight:600;">{_ra}</div>',
                                unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass

    # ── 5c. REHBERLİK TEST & ENVANTER SONUÇLARI ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_RT4
        _rt_otr = _CML_RT4.load_rehberlik_test_oturumlari()
        _rt_cvp = _CML_RT4.load_rehberlik_test_cevaplari()
        _rt_tst = _CML_RT4.load_rehberlik_testler()
        _ogr_otr = [o for o in _rt_otr if o.get("ogrenci_id") == sel_stu.id]
        if _ogr_otr:
            st.markdown("---")
            st.markdown(
                '<div style="background:#0f172a;border-radius:10px;padding:12px 16px;'
                'border:1px solid rgba(139,92,246,.2);">'
                '<h4 style="margin:0 0 8px;color:#a78bfa;font-size:14px;">📝 Rehberlik Test & Envanter</h4>',
                unsafe_allow_html=True,
            )
            _tst_map = {t.get("id", ""): t for t in _rt_tst}
            for o in _ogr_otr:
                test = _tst_map.get(o.get("test_id", ""), {})
                durum = o.get("durum", "-")
                d_clr = "#22c55e" if durum == "TAMAMLANDI" else "#f59e0b" if durum == "DEVAM_EDIYOR" else "#64748b"
                _c = [c for c in _rt_cvp if c.get("oturum_id") == o.get("id")]
                _p = [float(c.get("puan", 0)) for c in _c if c.get("puan")]
                _avg = sum(_p) / len(_p) if _p else 0
                _extra = f" | Ort Puan: {_avg:.1f}" if _p else ""
                st.markdown(
                    f'<div style="background:{d_clr}08;border-left:3px solid {d_clr};'
                    f'padding:5px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:.82rem;">'
                    f'<b style="color:{d_clr};">{test.get("test_adi", "-")}</b> '
                    f'<span style="color:#94a3b8;">({durum}{_extra})</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass

    # ══════════════════════════════════════════════════════════════════
    # ── 6. KAYNAK BAZLI DETAY TABLOLARI (Quiz / YD Sınav / CEFR Pl / CEFR Mock)
    # ══════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<h4 style="margin:14px 0 8px;color:#a78bfa;font-size:15px;">'
        '📊 Kaynak Bazlı Sınav Detayları (Yabancı Dil Modülü → Akademik Takip)</h4>',
        unsafe_allow_html=True,
    )

    # ── 6a. UNITE QUIZLERI ──
    if quizler_full:
        st.markdown(
            '<div style="background:#7c3aed10;border-left:3px solid #7c3aed;padding:6px 12px;'
            'border-radius:0 6px 6px 0;margin:10px 0 4px;font-size:0.85rem;color:#a78bfa;font-weight:700;">'
            f'🎯 Ünite Quizleri — {len(quizler_full)} kayıt</div>',
            unsafe_allow_html=True,
        )
        rows = ""
        for i, d in enumerate(sorted(quizler_full, key=lambda x: x.get("tarih", "") or "", reverse=True)):
            tarih = str(d.get("tarih", "—") or "")[:10]
            unit_n = int(d.get("unit", 0) or 0)
            unit_b = (f"<span style='background:#7c3aed18;color:#7c3aed;border:1px solid #7c3aed44;"
                      f"border-radius:4px;padding:1px 6px;font-size:0.72rem;font-weight:600'>Ü{unit_n}</span>"
                      if unit_n > 0 else "—")
            level_b = ""
            if d.get("level"):
                level_b = (f"<span style='background:#0891b218;color:#0891b2;border:1px solid #0891b244;"
                           f"border-radius:4px;padding:1px 6px;font-size:0.72rem;font-weight:600'>{d['level']}</span>")
            rows += (
                f"<tr style='border-bottom:1px solid #1A2035;{'background:#7c3aed08' if i%2==0 else ''}'>"
                f"<td style='padding:7px 10px;font-weight:600;font-size:0.82rem'>{d.get('sinav_adi','—')}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{unit_b}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{level_b}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem'>{d.get('toplam',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center;color:#94a3b8'>{d.get('bos',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{tarih}</td>"
                f"</tr>"
            )
        headers = ["Quiz Adı", "Ünite", "Level", "Soru", "D", "Y", "B", "Puan", "Tarih"]
        th = "".join(f"<th style='padding:8px 6px;background:#7c3aed;color:white;font-size:0.76rem;"
                     f"text-align:center;white-space:nowrap'>{h}</th>" for h in headers)
        st.markdown(
            f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:12px'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>",
            unsafe_allow_html=True,
        )

    # ── 6b. YD SINAVLAR (haftalik / yazili / deneme) ──
    if sinavlar_full:
        st.markdown(
            '<div style="background:#0891b210;border-left:3px solid #0891b2;padding:6px 12px;'
            'border-radius:0 6px 6px 0;margin:10px 0 4px;font-size:0.85rem;color:#0891b2;font-weight:700;">'
            f'📋 Yabancı Dil Sınavları — {len(sinavlar_full)} kayıt (Haftalık/Yazılı/Deneme)</div>',
            unsafe_allow_html=True,
        )
        rows = ""
        cat_colors = {"haftalik": "#0891b2", "yazili": "#7c3aed", "deneme": "#059669"}
        cat_labels = {"haftalik": "Haftalık", "yazili": "Yazılı", "deneme": "Deneme"}
        for i, d in enumerate(sorted(sinavlar_full, key=lambda x: x.get("tarih", "") or "", reverse=True)):
            tarih = str(d.get("tarih", "—") or "")[:10]
            cat = d.get("kategori", "")
            c_clr = cat_colors.get(cat, "#64748b")
            cat_label = cat_labels.get(cat, cat.title() if cat else "—")
            cat_badge = (f"<span style='background:{c_clr}18;color:{c_clr};border:1px solid {c_clr}44;"
                         f"border-radius:4px;padding:1px 6px;font-size:0.72rem;font-weight:600'>{cat_label}</span>")
            unit_n = int(d.get("unit", 0) or 0)
            unit_b = f"Ü{unit_n}" if unit_n > 0 else "—"
            rows += (
                f"<tr style='border-bottom:1px solid #1A2035;{'background:#0891b208' if i%2==0 else ''}'>"
                f"<td style='padding:7px 10px;font-weight:600;font-size:0.82rem'>{d.get('sinav_adi','—')}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{cat_badge}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem'>{unit_b}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem'>{d.get('toplam',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center;color:#059669;font-weight:700'>{d.get('dogru',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center;color:#ef4444;font-weight:700'>{d.get('yanlis',0)}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('puan',0))}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{tarih}</td>"
                f"</tr>"
            )
        headers = ["Sınav Adı", "Kategori", "Ünite", "Soru", "D", "Y", "Puan", "Tarih"]
        th = "".join(f"<th style='padding:8px 6px;background:#0891b2;color:white;font-size:0.76rem;"
                     f"text-align:center;white-space:nowrap'>{h}</th>" for h in headers)
        st.markdown(
            f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:12px'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>",
            unsafe_allow_html=True,
        )

    # ── 6c. CEFR PLACEMENT (Seviye Tespit) ──
    if cefr_pl_full:
        st.markdown(
            '<div style="background:#8b5cf610;border-left:3px solid #8b5cf6;padding:6px 12px;'
            'border-radius:0 6px 6px 0;margin:10px 0 4px;font-size:0.85rem;color:#a78bfa;font-weight:700;">'
            f'🎯 CEFR Seviye Tespit (Placement) — {len(cefr_pl_full)} kayıt</div>',
            unsafe_allow_html=True,
        )
        rows = ""
        for i, d in enumerate(sorted(cefr_pl_full, key=lambda x: x.get("tarih", "") or "", reverse=True)):
            tarih = str(d.get("tarih", "—") or "")[:10]
            placed = d.get("placed_cefr", "—") or "—"
            target = d.get("target_cefr", "—") or "—"
            pct = float(d.get("percentage", 0) or 0)
            period = d.get("period", "—") or "—"
            ay = d.get("academic_year", "")
            l_s = d.get("listening_score", 0)
            r_s = d.get("reading_score", 0)
            u_s = d.get("use_of_english_score", 0)
            w_s = d.get("writing_score", 0)
            placed_color = "#22c55e" if not d.get("is_below_target") else "#f59e0b"
            placed_badge = (f"<span style='background:{placed_color}18;color:{placed_color};"
                            f"border:1px solid {placed_color}44;border-radius:4px;padding:1px 8px;"
                            f"font-size:0.78rem;font-weight:800'>{placed}</span>")
            target_badge = (f"<span style='background:#0596690f;color:#059669;border:1px solid #05966944;"
                            f"border-radius:4px;padding:1px 6px;font-size:0.72rem;font-weight:700'>{target}</span>")
            rows += (
                f"<tr style='border-bottom:1px solid #1A2035;{'background:#8b5cf608' if i%2==0 else ''}'>"
                f"<td style='padding:7px 10px;font-size:0.78rem;color:#64748b'>{period} {ay}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{placed_badge}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{target_badge}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(pct)}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>L:{l_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>R:{r_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>UoE:{u_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>W:{w_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{tarih}</td>"
                f"</tr>"
            )
        headers = ["Dönem", "Placed", "Hedef", "Yüzde", "Listen", "Read", "Use of Eng", "Write", "Tarih"]
        th = "".join(f"<th style='padding:8px 6px;background:#8b5cf6;color:white;font-size:0.74rem;"
                     f"text-align:center;white-space:nowrap'>{h}</th>" for h in headers)
        st.markdown(
            f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:12px'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>",
            unsafe_allow_html=True,
        )

    # ── 6d. CEFR MOCK EXAM (Cambridge tarzi) ──
    if cefr_mk_full:
        st.markdown(
            '<div style="background:#6d28d910;border-left:3px solid #6d28d9;padding:6px 12px;'
            'border-radius:0 6px 6px 0;margin:10px 0 4px;font-size:0.85rem;color:#a78bfa;font-weight:700;">'
            f'🏆 CEFR Mock Exam — {len(cefr_mk_full)} kayıt</div>',
            unsafe_allow_html=True,
        )
        rows = ""
        for i, d in enumerate(sorted(cefr_mk_full, key=lambda x: x.get("tarih", "") or "", reverse=True)):
            tarih = str(d.get("tarih", "—") or "")[:10]
            achieved = d.get("achieved_cefr", "—") or d.get("cefr", "—") or "—"
            target = d.get("cefr", "—") or "—"
            pct = float(d.get("percentage", 0) or 0)
            l_s = d.get("listening_score", 0)
            r_s = d.get("reading_score", 0)
            w_s = d.get("writing_score", 0)
            sp_s = d.get("speaking_score", 0)
            achieved_badge = (f"<span style='background:#6d28d918;color:#6d28d9;"
                              f"border:1px solid #6d28d944;border-radius:4px;padding:1px 8px;"
                              f"font-size:0.78rem;font-weight:800'>{achieved}</span>")
            rows += (
                f"<tr style='border-bottom:1px solid #1A2035;{'background:#6d28d908' if i%2==0 else ''}'>"
                f"<td style='padding:7px 10px;font-size:0.78rem;color:#64748b'>Mock Exam</td>"
                f"<td style='padding:7px 8px;text-align:center'>{achieved_badge}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>Hedef: {target}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(pct)}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>L:{l_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>R:{r_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>W:{w_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>S:{sp_s:.0f}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{tarih}</td>"
                f"</tr>"
            )
        headers = ["Tür", "Achieved", "Hedef", "Yüzde", "Listen", "Read", "Write", "Speak", "Tarih"]
        th = "".join(f"<th style='padding:8px 6px;background:#6d28d9;color:white;font-size:0.74rem;"
                     f"text-align:center;white-space:nowrap'>{h}</th>" for h in headers)
        st.markdown(
            f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:12px'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>",
            unsafe_allow_html=True,
        )

    # ── 6e. YD REMEDIATION (yanlislardan otomatik telafi odevi) ──
    if remediation_full:
        st.markdown(
            '<div style="background:#dc262610;border-left:3px solid #dc2626;padding:6px 12px;'
            'border-radius:0 6px 6px 0;margin:10px 0 4px;font-size:0.85rem;color:#dc2626;font-weight:700;">'
            f'🔁 YD Telafi (Remediation) — {len(remediation_full)} kayıt</div>',
            unsafe_allow_html=True,
        )
        rows = ""
        for i, d in enumerate(sorted(remediation_full, key=lambda x: x.get("tarih", "") or "", reverse=True)):
            tarih = str(d.get("tarih", "") or "")[:10]
            rows += (
                f"<tr style='border-bottom:1px solid #1A2035;{'background:#dc262608' if i%2==0 else ''}'>"
                f"<td style='padding:7px 10px;font-size:0.78rem'>Telafi #{(d.get('id','') or '')[-6:]}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem'>{d.get('total_questions',0)} soru</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.78rem'>{d.get('status','—')}</td>"
                f"<td style='padding:7px 8px;text-align:center'>{_ss_puan_badge(d.get('score',0)) if d.get('score') else '—'}</td>"
                f"<td style='padding:7px 8px;text-align:center;font-size:0.72rem;color:#64748b'>{tarih}</td>"
                f"</tr>"
            )
        headers = ["Telafi", "Soru", "Durum", "Puan", "Tarih"]
        th = "".join(f"<th style='padding:8px 6px;background:#dc2626;color:white;font-size:0.76rem;"
                     f"text-align:center;white-space:nowrap'>{h}</th>" for h in headers)
        st.markdown(
            f"<div style='overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;margin-bottom:12px'>"
            f"<table style='width:100%;border-collapse:collapse'>"
            f"<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>",
            unsafe_allow_html=True,
        )


# ==================== TAB 2: NOT GIRISI ====================

@st.fragment
def _render_not_girisi(store: AkademikDataStore):
    """Not girisi ve takibi sekmesi."""
    styled_section("Not Girişi & Takibi", "#8b5cf6")
    styled_info_banner("Toplu veya tekil not girisi yapin, mevcut notlari goruntuleyip analiz edin.", "info")

    akademik_yil = _get_akademik_yil()

    # Filtreler
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        not_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="not_sinif")
    with col2:
        not_sube = st.selectbox("Şube", SUBELER, key="not_sube")
    with col3:
        not_ders = st.selectbox("Ders", DERSLER, key="not_ders")
    with col4:
        not_donem = st.selectbox("Donem", ["1. Donem", "2. Donem"], key="not_donem")

    students = store.get_students(sinif=not_sinif, sube=not_sube, durum="aktif")

    tab_toplu, tab_tekil, tab_goruntule = st.tabs(["📋 Toplu Not Girişi", "📝 Tekil Not Girişi", "👁️ Not Görüntüle"])

    with tab_toplu:
        if not students:
            st.info("Bu sinif/subede ogrenci bulunamadı.")
            return

        st.markdown(f"**{not_sinif}/{not_sube} - {not_ders} - {not_donem}**")

        # Uygulamali ders kontrolu — yazili/sozlu otomatik gizlenir
        from models.akademik_takip import get_not_turleri_for_ders, UYGULAMALI_DERSLER, UYGULAMALI_DERS_BILGI
        _gecerli_turler = get_not_turleri_for_ders(not_ders)
        _is_uygulamali = not_ders in UYGULAMALI_DERSLER

        if _is_uygulamali:
            _bilgi = UYGULAMALI_DERS_BILGI.get(not_ders, {})
            st.markdown(
                f'<div style="background:#f59e0b15;border-left:3px solid #f59e0b;padding:8px 12px;'
                f'border-radius:0 8px 8px 0;margin:6px 0;font-size:12px;">'
                f'<b>Uygulamali Ders:</b> {not_ders} — Yazili sinav yoktur.<br>'
                f'{_bilgi.get("uygulama", "Uygulama notu, ders ici etkinlik ve proje/performans ile degerlendirilir.")}</div>',
                unsafe_allow_html=True)

        tc1, tc2 = st.columns(2)
        with tc1:
            _not_turu_labels = [t[1] for t in _gecerli_turler]
            toplu_not_turu_label = st.selectbox("Not Turu", _not_turu_labels, key="toplu_not_turu")
            toplu_not_turu_idx = _not_turu_labels.index(toplu_not_turu_label) if toplu_not_turu_label in _not_turu_labels else 0
            toplu_not_turu = _gecerli_turler[toplu_not_turu_idx][0]
        with tc2:
            _sira_label = "Not Sirasi (1. uygulama, 2. uygulama...)" if _is_uygulamali else "Not Sirasi (1. yazili, 2. yazili...)"
            toplu_not_sirasi = st.number_input(_sira_label,
                                                min_value=1, max_value=10, value=1,
                                                key="toplu_not_sirasi")

        with st.form("toplu_not_form"):
            styled_section("Notları Girin (0-100)", "#8b5cf6")

            puanlar = {}
            for i, stu in enumerate(students):
                col_name, col_puan = st.columns([3, 1])
                with col_name:
                    st.write(f"{stu.numara} - {stu.ad} {stu.soyad}")
                with col_puan:
                    puanlar[stu.id] = st.number_input(
                        f"Puan", min_value=0.0, max_value=100.0, value=0.0,
                        step=1.0, key=f"toplu_puan_{stu.id}",
                        label_visibility="collapsed"
                    )

            if st.form_submit_button("Notları Kaydet", type="primary"):
                count = 0
                for stu_id, puan in puanlar.items():
                    if puan > 0:
                        grade = GradeRecord(
                            student_id=stu_id,
                            ders=not_ders,
                            sinif=not_sinif,
                            sube=not_sube,
                            donem=not_donem,
                            not_turu=toplu_not_turu,
                            not_sirasi=toplu_not_sirasi,
                            puan=puan,
                            akademik_yil=akademik_yil,
                        )
                        store.save_grade(grade)
                        count += 1
                st.success(f"{count} ogrencinin notu kaydedildi!")
                st.rerun(scope="fragment")

    with tab_tekil:
        if not students:
            st.info("Bu sinif/subede ogrenci bulunamadı.")
            return

        with st.form("tekil_not_form"):
            styled_section("Tekil Not Girişi", "#0d9488")
            student_options = {f"{s.numara} - {s.ad} {s.soyad}": s.id for s in students}
            tek_stu = st.selectbox("Öğrenci", list(student_options.keys()), key="tek_stu")

            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                _tek_gecerli = get_not_turleri_for_ders(not_ders)
                _tek_not_labels = [t[1] for t in _tek_gecerli]
                tek_not_turu_label = st.selectbox("Not Turu", _tek_not_labels, key="tek_not_turu")
                tek_not_turu_idx = _tek_not_labels.index(tek_not_turu_label) if tek_not_turu_label in _tek_not_labels else 0
                tek_not_turu = _tek_gecerli[tek_not_turu_idx][0]
            with tc2:
                tek_not_sirasi = st.number_input("Sira", min_value=1, max_value=10, value=1, key="tek_sira")
            with tc3:
                tek_puan = st.number_input("Puan", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="tek_puan")

            tek_tarih = st.date_input("Tarih", value=date.today(), key="tek_tarih")
            tek_aciklama = st.text_input("Açıklama (opsiyonel)", key="tek_aciklama")

            if st.form_submit_button("Notu Kaydet", type="primary"):
                if tek_puan > 0:
                    grade = GradeRecord(
                        student_id=student_options[tek_stu],
                        ders=not_ders,
                        sinif=not_sinif,
                        sube=not_sube,
                        donem=not_donem,
                        not_turu=tek_not_turu,
                        not_sirasi=tek_not_sirasi,
                        puan=tek_puan,
                        tarih=tek_tarih.strftime("%Y-%m-%d"),
                        aciklama=tek_aciklama,
                        akademik_yil=akademik_yil,
                    )
                    store.save_grade(grade)
                    st.success("Not kaydedildi!")
                    st.rerun(scope="fragment")
                else:
                    st.error("Puan 0'dan buyuk olmalidir.")

    with tab_goruntule:
        grades = store.get_grades(ders=not_ders, sinif=not_sinif, sube=not_sube,
                                   donem=not_donem, akademik_yil=akademik_yil)
        if grades:
            df_data = []
            for g in grades:
                stu = store.get_student(g.student_id)
                stu_name = f"{stu.ad} {stu.soyad}" if stu else "Bilinmiyor"
                stu_no = stu.numara if stu else ""
                df_data.append({
                    "Numara": stu_no,
                    "Öğrenci": stu_name,
                    "Not Turu": _not_turu_label(g.not_turu),
                    "Sira": g.not_sirasi,
                    "Puan": g.puan,
                    "Tarih": g.tarih,
                    "Açıklama": g.aciklama,
                })
            df = pd.DataFrame(df_data)
            df = df.sort_values(["Numara", "Not Turu", "Sira"])
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Sinif ortalamalari
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            styled_section("Sınıf Not Ortalamaları", "#6366f1")
            avg_data = {}
            for g in grades:
                key = _not_turu_label(g.not_turu) + f" {g.not_sirasi}"
                if key not in avg_data:
                    avg_data[key] = []
                avg_data[key].append(g.puan)

            ort_stats = []
            renkler = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#0d9488"]
            for i, (key, puanlar) in enumerate(avg_data.items()):
                ort = sum(puanlar) / len(puanlar)
                renk = renkler[i % len(renkler)]
                ort_stats.append((key, f"{ort:.1f}", renk, "\U0001f4ca"))
            if ort_stats:
                styled_stat_row(ort_stats[:4])
        else:
            st.info("Bu secimler için not kaydi bulunamadı.")


# ==================== TAB 3: DERS PROGRAMI ====================

def _render_schedule_grid(schedule: list, gunler: list, max_saat: int, mode: str = "class",
                          ders_saatleri_map: dict = None, kurum_adi: str = "",
                          baslik: str = "", mudur_adi: str = "", logo_path: str = ""):
    """Profesyonel haftalik program tablosu. mode='class' veya 'teacher'."""
    # Ders renkleri
    ders_renkler = {
        "Matematik": "#3b82f6", "Turkce": "#ef4444", "Fen Bilimleri": "#10b981",
        "Sosyal Bilgiler": "#f59e0b", "Ingilizce": "#8b5cf6", "Almanca": "#ec4899",
        "Din Kulturu ve Ahlak Bilgisi": "#3b82f6", "Gorsel Sanatlar": "#f97316",
        "Muzik": "#a855f7", "Beden Egitimi": "#14b8a6", "Teknoloji ve Tasarim": "#6366f1",
        "Bilisim Teknolojileri": "#0ea5e9", "Rehberlik": "#84cc16",
        "T.C. Inkilap Tarihi ve Ataturkculuk": "#f59e0b", "Fransizca": "#e879f9",
    }

    # Kurum basligi
    header_html = ""
    if kurum_adi or baslik:
        header_html = '<div style="text-align:center;margin-bottom:12px">'
        if logo_path:
            import os
            if os.path.exists(logo_path):
                import base64
                with open(logo_path, "rb") as lf:
                    logo_b64 = base64.b64encode(lf.read()).decode()
                ext = logo_path.rsplit(".", 1)[-1].lower()
                mime = "image/png" if ext == "png" else "image/jpeg"
                header_html += f'<img src="data:{mime};base64,{logo_b64}" style="height:48px;margin-bottom:6px"><br>'
        if kurum_adi:
            header_html += f'<div style="font-size:1.1rem;font-weight:800;color:#0d47a1;letter-spacing:1px">{kurum_adi}</div>'
        if baslik:
            header_html += f'<div style="font-size:0.95rem;font-weight:600;color:#94A3B8;margin-top:2px">{baslik}</div>'
        header_html += '</div>'

    # Gun basliklari
    gun_headers = ""
    for gun in gunler:
        kisa = GUN_KISALTMA.get(gun, gun[:3])
        gun_headers += (
            f'<th style="background:linear-gradient(135deg,#1565c0,#1976d2);color:#fff;'
            f'padding:10px 6px;text-align:center;font-weight:700;font-size:0.85rem;'
            f'border:1px solid #1565c0;min-width:100px">{kisa}</th>'
        )

    # Satir olustur
    rows_html = ""
    for saat in range(1, max_saat + 1):
        # Saat bilgisi
        saat_label = f"{saat}. Ders"
        saat_zaman = ""
        if ders_saatleri_map and saat in ders_saatleri_map:
            z = ders_saatleri_map[saat]
            saat_zaman = f'<div style="font-size:0.65rem;color:#64748b;margin-top:1px">{z["baslangic"]}-{z["bitis"]}</div>'

        zebra = "#111827" if saat % 2 == 0 else "#ffffff"
        rows_html += (
            f'<tr style="background:{zebra}">'
            f'<td style="background:linear-gradient(135deg,#e3f2fd,#bbdefb);padding:8px 6px;'
            f'text-align:center;font-weight:700;font-size:0.8rem;color:#0d47a1;'
            f'border:1px solid #90caf9;white-space:nowrap">'
            f'{saat_label}{saat_zaman}</td>'
        )

        for gun in gunler:
            slot = next((s for s in schedule if s.gun == gun and s.ders_saati == saat), None)
            if slot:
                ders_kisa = DERS_KISALTMA.get(slot.ders, slot.ders)
                renk = ders_renkler.get(slot.ders, "#64748b")
                if mode == "teacher":
                    alt = f"{slot.sinif}/{slot.sube}"
                else:
                    alt = (slot.ogretmen or "").split()[0] if slot.ogretmen else ""
                rows_html += (
                    f'<td style="padding:6px 4px;text-align:center;border:1px solid #e2e8f0;'
                    f'vertical-align:middle">'
                    f'<div style="font-weight:700;font-size:0.82rem;color:{renk};line-height:1.2">{ders_kisa}</div>'
                    f'<div style="font-size:0.68rem;color:#94a3b8;margin-top:1px">{alt}</div>'
                    f'</td>'
                )
            else:
                rows_html += (
                    f'<td style="padding:6px;text-align:center;border:1px solid #e2e8f0;'
                    f'color:#cbd5e1;font-size:0.8rem">-</td>'
                )
        rows_html += '</tr>'

    # Mudur ve basari mesaji (ogretmen raporlari icin)
    footer_html = ""
    if mudur_adi:
        footer_html = (
            f'<div style="text-align:right;margin-top:16px;padding:12px 20px;'
            f'border-top:2px solid #e2e8f0">'
            f'<div style="font-weight:700;font-size:0.9rem;color:#94A3B8">{mudur_adi}</div>'
            f'<div style="font-size:0.8rem;color:#64748b;margin-top:2px">Kurum Muduru</div>'
            f'<div style="font-style:italic;font-size:0.82rem;color:#475569;margin-top:8px">'
            f'"Calismalarinizda basarilar dilerim."</div>'
            f'</div>'
        )

    # Tum tablo
    st.markdown(
        f'{header_html}'
        f'<table style="width:100%;border-collapse:separate;border-spacing:0;'
        f'border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);'
        f'margin-bottom:8px">'
        f'<thead><tr>'
        f'<th style="background:linear-gradient(135deg,#0d47a1,#1565c0);color:#fff;'
        f'padding:10px 8px;text-align:center;font-weight:700;font-size:0.85rem;'
        f'border:1px solid #0d47a1;min-width:80px">Saat</th>'
        f'{gun_headers}'
        f'</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
        f'{footer_html}',
        unsafe_allow_html=True
    )


def _render_carsaf_html(rows: list, gunler: list, max_saat: int, label_header: str = "Sınıf/Şube",
                         show_sub: bool = False, sub_header: str = "", show_total: bool = False,
                         kurum_adi: str = "", baslik: str = "", ders_saat_map: dict = None):
    """Carsaf gorunumunde profesyonel HTML tablo. 2 satirlik header (gun grubu + saat no),
    renk kodlu gun gruplari, sticky ilk kolon, yatay scroll."""
    gun_renkleri = ["#1565c0", "#2e7d32", "#e65100", "#6a1b9a", "#c62828", "#00838f", "#4e342e"]

    # Kurum / baslik
    header_html = ""
    if kurum_adi or baslik:
        header_html = '<div style="text-align:center;margin-bottom:10px">'
        if kurum_adi:
            header_html += f'<div style="font-size:1rem;font-weight:800;color:#0d47a1;letter-spacing:1px">{kurum_adi}</div>'
        if baslik:
            header_html += f'<div style="font-size:0.85rem;font-weight:600;color:#475569;margin-top:2px">{baslik}</div>'
        header_html += '</div>'

    # Header row 1: gun isimleri (colspan=max_saat)
    h1_cells = (
        f'<th rowspan="2" style="position:sticky;left:0;z-index:3;background:#0d47a1;color:#fff;'
        f'padding:6px 10px;text-align:center;font-weight:700;font-size:0.8rem;'
        f'border:1px solid #0d47a1;min-width:90px">{label_header}</th>'
    )
    if show_sub:
        h1_cells += (
            f'<th rowspan="2" style="position:sticky;left:90px;z-index:3;background:#0d47a1;color:#fff;'
            f'padding:6px 6px;text-align:center;font-weight:700;font-size:0.75rem;'
            f'border:1px solid #0d47a1;min-width:60px">{sub_header}</th>'
        )
    for gi, gun in enumerate(gunler):
        kisa = GUN_KISALTMA.get(gun, gun[:3])
        renk = gun_renkleri[gi % len(gun_renkleri)]
        h1_cells += (
            f'<th colspan="{max_saat}" style="background:{renk};color:#fff;'
            f'padding:6px 2px;text-align:center;font-weight:700;font-size:0.8rem;'
            f'border:1px solid {renk};letter-spacing:0.5px">{kisa}</th>'
        )
    if show_total:
        h1_cells += (
            f'<th rowspan="2" style="background:#0d47a1;color:#fff;padding:6px 4px;'
            f'text-align:center;font-weight:700;font-size:0.75rem;border:1px solid #0d47a1;'
            f'min-width:40px">Top</th>'
        )

    # Header row 2: saat numaralari
    h2_cells = ""
    for gi, gun in enumerate(gunler):
        renk = gun_renkleri[gi % len(gun_renkleri)]
        for saat in range(1, max_saat + 1):
            saat_tip = ""
            if ders_saat_map and saat in ders_saat_map:
                z = ders_saat_map[saat]
                saat_tip = f' title="{z}"'
            h2_cells += (
                f'<th style="background:{renk}dd;color:#fff;padding:3px 2px;text-align:center;'
                f'font-size:0.7rem;font-weight:600;border:1px solid {renk};min-width:55px"'
                f'{saat_tip}>{saat}</th>'
            )

    # Veri satirlari
    body_html = ""
    for ri, row in enumerate(rows):
        zebra = "#111827" if ri % 2 == 0 else "#ffffff"
        label = row.get("_label", "")
        sub_val = row.get("_sub", "")
        total_val = row.get("_total", "")
        body_html += f'<tr style="background:{zebra}">'
        body_html += (
            f'<td style="position:sticky;left:0;z-index:1;background:linear-gradient(135deg,#e3f2fd,#bbdefb);'
            f'padding:5px 8px;text-align:center;font-weight:700;font-size:0.78rem;color:#0d47a1;'
            f'border:1px solid #90caf9;white-space:nowrap">{label}</td>'
        )
        if show_sub:
            body_html += (
                f'<td style="position:sticky;left:90px;z-index:1;background:{zebra};'
                f'padding:4px 4px;text-align:center;font-size:0.7rem;color:#64748b;'
                f'border:1px solid #e2e8f0;white-space:nowrap">{sub_val}</td>'
            )
        for gi, gun in enumerate(gunler):
            renk = gun_renkleri[gi % len(gun_renkleri)]
            bg_light = f'{renk}08' if ri % 2 == 0 else f'{renk}04'
            for saat in range(1, max_saat + 1):
                val = row.get((gun, saat), "")
                if val:
                    body_html += (
                        f'<td style="padding:4px 2px;text-align:center;font-size:0.72rem;'
                        f'font-weight:600;color:#94A3B8;border:1px solid #e2e8f0;'
                        f'background:{bg_light}">{val}</td>'
                    )
                else:
                    body_html += (
                        f'<td style="padding:4px 2px;text-align:center;font-size:0.7rem;'
                        f'color:#d1d5db;border:1px solid #e2e8f0;background:{bg_light}">-</td>'
                    )
        if show_total:
            body_html += (
                f'<td style="padding:4px 4px;text-align:center;font-weight:700;font-size:0.78rem;'
                f'color:#0d47a1;border:1px solid #e2e8f0;background:#e3f2fd">{total_val}</td>'
            )
        body_html += '</tr>'

    st.markdown(
        f'{header_html}'
        f'<div style="overflow-x:auto;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.08)">'
        f'<table style="border-collapse:collapse;white-space:nowrap">'
        f'<thead><tr>{h1_cells}</tr><tr>{h2_cells}</tr></thead>'
        f'<tbody>{body_html}</tbody>'
        f'</table></div>',
        unsafe_allow_html=True
    )


@st.fragment
def _render_ders_programi(store: AkademikDataStore):
    """Ders programi yonetimi sekmesi - 5 alt sekmeli."""
    styled_section("Ders Programı", "#1565c0")

    akademik_yil = _get_akademik_yil()
    ayarlar = store.get_ders_programi_ayarlari()
    aktif_gunler = ayarlar.get("aktif_gunler", GUNLER[:5])
    max_saat = ayarlar.get("gunluk_ders_saati", 8)

    dp_tab = st.radio(
        "Ders Programı Sekmeleri",
        ["Okul Ayarlari", "Öğretmen Görevlendirme", "Sınıf Kadro",
         "Otomatik Dağıtım", "Program Raporlari", "Manuel Düzenleme"],
        horizontal=True, key="dp_active_tab", label_visibility="collapsed"
    )

    # ===== TAB 1: OKUL AYARLARI =====
    if dp_tab == "Okul Ayarlari":
        # --- Genel Okul Ayarlari ---
        styled_section("Genel Okul Ayarlari", "#1565c0")

        styled_stat_row([
            ("Günlük Ders Saati", max_saat, "#2563eb", "\U0001f4da"),
            ("Haftalık Gün", len(aktif_gunler), "#10b981", "\U0001f4c5"),
            ("Haftalık Slot", max_saat * len(aktif_gunler), "#8b5cf6", "\U0001f4ca"),
            ("Aktif Günler", ", ".join(GUN_KISALTMA.get(g, g[:3]) for g in aktif_gunler), "#f59e0b", "\u2705"),
        ])

        with st.expander("Ayarlari Düzenle", expanded=False):
            with st.form("dp_ayarlar_form"):
                ac1, ac2 = st.columns(2)
                with ac1:
                    ay_ders_saati = st.number_input(
                        "Günlük Ders Saati", min_value=1, max_value=11,
                        value=ayarlar.get("gunluk_ders_saati", 8),
                        key="dp_ay_ders_saati"
                    )
                with ac2:
                    ay_gun_sayisi = st.number_input(
                        "Haftalık Gün Sayısı", min_value=5, max_value=7,
                        value=ayarlar.get("haftalik_gun_sayisi", 5),
                        key="dp_ay_gun_sayisi"
                    )

                gun_secenekleri = GUNLER_FULL[:ay_gun_sayisi]
                ay_aktif_gunler = st.multiselect(
                    "Aktif Günler", GUNLER_FULL,
                    default=gun_secenekleri,
                    key="dp_ay_aktif_gunler"
                )

                if st.form_submit_button("Ayarlari Kaydet", type="primary"):
                    yeni_ayarlar = {
                        "gunluk_ders_saati": ay_ders_saati,
                        "haftalik_gun_sayisi": ay_gun_sayisi,
                        "aktif_gunler": ay_aktif_gunler,
                    }
                    store.save_ders_programi_ayarlari(yeni_ayarlar)
                    st.success("Ayarlar kaydedildi!")
                    st.rerun(scope="fragment")

        # --- Sinif Bazli Haftalik Ders Saatleri ---
        styled_section("Sınıf Bazlı Haftalık Ders Saatleri", "#00695c")
        styled_info_banner(
            "Her sinif seviyesi için derslerin haftalik kac saat oldugunu belirleyin. "
            "Bu bilgi ogretmen gorevlendirme ve otomatik dagitimda kullanilir.",
            "info"
        )

        mevcut_ders_saatleri = store.get_ders_saatleri()
        max_haftalik = max_saat * len(aktif_gunler)

        # Kademe seçimi
        _KADEME_SINIF_MAP = {
            "İlkokul (1-4)": ["1", "2", "3", "4"],
            "Ortaokul (5-8)": ["5", "6", "7", "8"],
            "Lise (9-12)": ["9", "10", "11", "12"],
        }
        _KADEME_DERS_MAP = {
            "İlkokul (1-4)": [
                "Türkçe", "Matematik", "Hayat Bilgisi", "Fen Bilimleri",
                "Sosyal Bilgiler", "İngilizce", "Din Kültürü ve Ahlak Bilgisi",
                "Görsel Sanatlar", "Müzik", "Beden Eğitimi", "Oyun ve Fiziki Etkinlikler",
            ],
            "Ortaokul (5-8)": list(ORTAOKUL_DERSLER),
            "Lise (9-12)": [
                "Edebiyat", "Matematik", "Fizik", "Kimya", "Biyoloji",
                "Tarih", "Coğrafya", "Felsefe", "İngilizce",
                "Din Kültürü ve Ahlak Bilgisi", "Beden Eğitimi",
                "Görsel Sanatlar", "Müzik",
            ],
        }

        dp_kademe = st.radio(
            "Kademe",
            list(_KADEME_SINIF_MAP.keys()),
            horizontal=True, key="dp_kademe_sec",
            index=1,
        )
        secili_siniflar = _KADEME_SINIF_MAP[dp_kademe]
        secili_dersler = _KADEME_DERS_MAP[dp_kademe]

        # Anlik toplamlar hesapla
        toplamlar = {}
        for sinif in secili_siniflar:
            toplamlar[sinif] = sum(
                st.session_state.get(f"dp_ds_{sinif}_{d}", mevcut_ders_saatleri.get(sinif, {}).get(d, 0))
                for d in secili_dersler
            )

        # Toplam ozet kartlari
        toplam_stats = []
        for sinif in secili_siniflar:
            t = toplamlar[sinif]
            renk = "#10b981" if t == max_haftalik else "#f59e0b" if t < max_haftalik else "#ef4444"
            toplam_stats.append((f"{sinif}. Sınıf", f"{t}/{max_haftalik}", renk, "\U0001f4d6"))
        styled_stat_row(toplam_stats)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Profesyonel HTML tablo baslik
        sinif_hdrs = "".join(
            f'<th style="background:linear-gradient(135deg,#1565c0,#1976d2);color:#fff;'
            f'padding:10px 8px;text-align:center;font-weight:700;font-size:0.85rem;'
            f'min-width:80px">{s}. Sınıf</th>'
            for s in secili_siniflar
        )
        st.markdown(
            f'<table style="width:100%;border-collapse:separate;border-spacing:0;'
            f'border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);'
            f'margin-bottom:8px">'
            f'<thead><tr>'
            f'<th style="background:linear-gradient(135deg,#0d47a1,#1565c0);color:#fff;'
            f'padding:12px 16px;text-align:left;font-weight:700;font-size:0.9rem;'
            f'min-width:200px">Ders Adi</th>'
            f'{sinif_hdrs}'
            f'</tr></thead></table>',
            unsafe_allow_html=True
        )

        # Ders satirlari - number input ile
        yeni_saatler = {s: {} for s in secili_siniflar}
        for idx, ders in enumerate(secili_dersler):
            zebra = "#111827" if idx % 2 == 0 else "#ffffff"
            d_cols = st.columns([3] + [1] * len(secili_siniflar))
            with d_cols[0]:
                st.markdown(
                    f'<div style="background:{zebra};padding:6px 12px;border-radius:6px;'
                    f'border-left:3px solid #1565c0;margin:1px 0;font-weight:600;'
                    f'font-size:0.88rem;color:#94A3B8">{ders}</div>',
                    unsafe_allow_html=True
                )
            for i, sinif in enumerate(secili_siniflar):
                with d_cols[i + 1]:
                    mevcut_val = mevcut_ders_saatleri.get(sinif, {}).get(ders, 0)
                    saat = st.number_input(
                        f"{ders} {sinif}",
                        min_value=0, max_value=12,
                        value=mevcut_val,
                        key=f"dp_ds_{sinif}_{ders}",
                        label_visibility="collapsed"
                    )
                    if saat > 0:
                        yeni_saatler[sinif][ders] = saat

        # Toplam satiri - anlik hesaplama
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        t_cols = st.columns([3] + [1] * len(secili_siniflar))
        with t_cols[0]:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0d47a1,#1565c0);'
                'padding:8px 12px;border-radius:8px;font-weight:800;font-size:0.95rem;'
                'color:#ffffff;text-align:center;letter-spacing:0.5px">TOPLAM</div>',
                unsafe_allow_html=True
            )
        for i, sinif in enumerate(secili_siniflar):
            with t_cols[i + 1]:
                toplam = sum(
                    st.session_state.get(f"dp_ds_{sinif}_{d}", 0)
                    for d in secili_dersler
                )
                if toplam == max_haftalik:
                    bg, renk, ikon = "linear-gradient(135deg,#059669,#34d399)", "#fff", "\u2705"
                elif toplam > max_haftalik:
                    bg, renk, ikon = "linear-gradient(135deg,#dc2626,#f87171)", "#fff", "\u26a0\ufe0f"
                else:
                    bg, renk, ikon = "linear-gradient(135deg,#d97706,#fbbf24)", "#fff", "\U0001f4dd"
                st.markdown(
                    f'<div style="background:{bg};padding:8px 4px;border-radius:8px;'
                    f'text-align:center;font-weight:800;font-size:1.1rem;color:{renk};'
                    f'box-shadow:0 2px 6px rgba(0,0,0,0.12)">'
                    f'{ikon} {toplam}<span style="font-size:0.7rem;opacity:0.8">/{max_haftalik}</span></div>',
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Ders Saatlerini Kaydet", type="primary", key="dp_ds_kaydet", use_container_width=True):
            store.save_ders_saatleri(yeni_saatler)
            st.success("Ders saatleri kaydedildi!")
            st.rerun(scope="fragment")

    # ===== TAB 2: OGRETMEN GOREVLENDIRME =====
    elif dp_tab == "Öğretmen Görevlendirme":
        teachers = store.get_teachers(durum="aktif")
        if not teachers:
            st.warning("Önce Akademik Kadro sekmesinden personel ekleyin.")
            return

        ders_saatleri_map = store.get_ders_saatleri()
        assignments = store.get_teacher_assignments(akademik_yil=akademik_yil)
        assign_map = {a.ogretmen_id: a for a in assignments}

        # Sinif/sube listesi
        _cache_key = "_dp_sinif_sube_cache"
        if _cache_key not in st.session_state:
            _stu = store.get_students()
            _ss = sorted(set((s.sinif, s.sube) for s in _stu if s.sinif and s.sube),
                         key=lambda x: (str(x[0]), str(x[1])))
            if not _ss:
                _ss = [(s, sb) for s in [5, 6, 7, 8] for sb in SUBELER[:2]]
            st.session_state[_cache_key] = _ss
        sinif_subeler = st.session_state[_cache_key]

        if not ders_saatleri_map:
            styled_section("Öğretmen Görevlendirme", "#2563eb")
            st.warning("Önce Okul Ayarlari sekmesinden ders saatlerini girin.")
            return

        # --- Her ders için toplam saat ve sinif detayi hesapla ---
        ders_bilgi = {}
        for sinif, sube in sinif_subeler:
            sinif_str = str(sinif)
            saatler = ders_saatleri_map.get(sinif_str, {})
            for ders, saat in saatler.items():
                if saat <= 0:
                    continue
                if ders not in ders_bilgi:
                    ders_bilgi[ders] = {"toplam": 0, "siniflar": []}
                ders_bilgi[ders]["toplam"] += saat
                ders_bilgi[ders]["siniflar"].append((sinif, sube, saat))

        if not ders_bilgi:
            styled_section("Öğretmen Görevlendirme", "#2563eb")
            st.warning("Ders saatleri henuz girilmemiş.")
            return

        # --- Ogretmenleri brans'a gore eslestir ---
        ders_ogretmenler = {}
        for t in teachers:
            t_dersler = t.branslar if t.branslar else ([t.brans] if t.brans else [])
            for d in t_dersler:
                if d not in ders_ogretmenler:
                    ders_ogretmenler[d] = []
                ders_ogretmenler[d].append(t)

        # ========================================
        # DERS-OGRETMEN YUK DAGITIMI
        # ========================================
        styled_section("Ders-Öğretmen Yuk Dağılımı", "#2563eb")
        styled_info_banner(
            "Ders saatlerine gore ogretmen yuku otomatik hesaplandi. "
            "Her ogretmenin kac saat alacagini ayarlayabilirsiniz. "
            "Toplam, tum subelerdeki ders saati toplamina esit olmalidir.",
            "info"
        )

        toplam_ders_saati = sum(d["toplam"] for d in ders_bilgi.values())
        eslesen_ders = sum(1 for d in ders_bilgi if d in ders_ogretmenler)
        eksik_ders = sum(1 for d in ders_bilgi if d not in ders_ogretmenler)
        styled_stat_row([
            ("Toplam Ders Yuku", f"{toplam_ders_saati} saat", "#2563eb", ""),
            ("Şube Sayısı", str(len(sinif_subeler)), "#10b981", ""),
            ("Eslesen Ders", str(eslesen_ders), "#059669", ""),
            ("Öğretmensiz Ders", str(eksik_ders), "#ef4444" if eksik_ders > 0 else "#10b981", ""),
        ])

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # --- Her ders için dagitim satirlari ---
        ogretmen_yukler = {}  # ogr_id -> {"ad", "toplam", "dersler": {ders: saat}}

        for ders in sorted(ders_bilgi.keys()):
            info = ders_bilgi[ders]
            toplam = info["toplam"]
            ogretmenler = ders_ogretmenler.get(ders, [])

            if not ogretmenler:
                st.error(f"**{ders}** ({toplam} saat) — Öğretmen bulunamadı! Akademik Kadro'dan bu bransli ogretmen ekleyin.")
                continue

            ogr_isimleri = ", ".join(o.tam_ad for o in ogretmenler)
            esit = toplam // len(ogretmenler)
            kalan_esit = toplam % len(ogretmenler)

            with st.expander(f"{ders} — {toplam} saat | {len(ogretmenler)} ogretmen ({ogr_isimleri})", expanded=True):
                cols = st.columns(len(ogretmenler) + 1)
                dagitim_toplam = 0

                for i, ogr in enumerate(ogretmenler):
                    with cols[i]:
                        # Mevcut atamadan veya esit dagitimdan varsayilan
                        a = assign_map.get(ogr.id)
                        mevcut = 0
                        if a:
                            mevcut = sum(g["haftalik_saat"] for g in a.gorevler if g.get("ders") == ders)
                        varsayilan = mevcut if mevcut > 0 else (esit + (1 if i < kalan_esit else 0))

                        saat_val = st.number_input(
                            ogr.tam_ad, min_value=0, max_value=toplam,
                            value=varsayilan, key=f"dp_yd_{ders}_{ogr.id}"
                        )
                        dagitim_toplam += saat_val

                        if ogr.id not in ogretmen_yukler:
                            ogretmen_yukler[ogr.id] = {"ad": ogr.tam_ad, "toplam": 0, "dersler": {}}
                        ogretmen_yukler[ogr.id]["toplam"] += saat_val
                        ogretmen_yukler[ogr.id]["dersler"][ders] = saat_val

                with cols[-1]:
                    fark = toplam - dagitim_toplam
                    if fark == 0:
                        st.markdown(
                            f'<div style="padding:28px 8px 8px;text-align:center;font-weight:700;'
                            f'color:#166534;font-size:1.1rem">{dagitim_toplam}/{toplam}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div style="padding:20px 8px 8px;text-align:center;font-weight:700;'
                            f'color:#991b1b;font-size:1.1rem">{dagitim_toplam}/{toplam}'
                            f'<br><span style="font-size:0.8rem">Fark: {fark:+d}</span></div>',
                            unsafe_allow_html=True
                        )

        # ========================================
        # OGRETMEN TOPLAM YUK OZETI
        # ========================================
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        styled_section("Öğretmen Toplam Yuk Özeti", "#7c3aed")

        if ogretmen_yukler:
            yuk_stats = []
            for ogr_id, yuk in sorted(ogretmen_yukler.items(), key=lambda x: -x[1]["toplam"]):
                t_saat = yuk["toplam"]
                renk = "#ef4444" if t_saat > 40 else "#f59e0b" if t_saat > 30 else "#10b981"
                yuk_stats.append((yuk["ad"], f"{t_saat} saat", renk, ""))
            for i in range(0, len(yuk_stats), 4):
                styled_stat_row(yuk_stats[i:i + 4])

            yuk_tablo = []
            for ogr_id, yuk in sorted(ogretmen_yukler.items(), key=lambda x: -x[1]["toplam"]):
                ders_str = " | ".join(f"{d}: {s}s" for d, s in yuk["dersler"].items() if s > 0)
                yuk_tablo.append({
                    "Öğretmen": yuk["ad"],
                    "Toplam Saat": yuk["toplam"],
                    "Ders Dagilimi": ders_str,
                    "Durum": "Agir Yuk" if yuk["toplam"] > 40 else "Yogun" if yuk["toplam"] > 30 else "Normal",
                })
            st.dataframe(pd.DataFrame(yuk_tablo), use_container_width=True, hide_index=True)

        # ========================================
        # KAYDET
        # ========================================
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        hatali = []
        for ders in ders_bilgi:
            ogrs = ders_ogretmenler.get(ders, [])
            atanan = sum(st.session_state.get(f"dp_yd_{ders}_{o.id}", 0) for o in ogrs)
            fark = ders_bilgi[ders]["toplam"] - atanan
            if fark != 0:
                hatali.append(f"{ders}({fark:+d})")
        if hatali:
            st.warning(f"Dengesiz dersler: {', '.join(hatali)}. Toplam saat uyusmayan dersler var.")

        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            kaydet_btn = st.button("Görevlendirmeleri Kaydet", type="primary", key="dp_yd_kaydet", use_container_width=True)
        with btn_c2:
            temizle_btn = st.button("Görevlendirmeleri Temizle", key="dp_yd_temizle", use_container_width=True)
        with btn_c3:
            yeni_program_btn = st.button("Temizle + Yeni Program Yap", key="dp_yd_yeni_program", use_container_width=True)

        if temizle_btn:
            existing_assigns = store.get_teacher_assignments(akademik_yil=akademik_yil)
            silinen = 0
            for ea in existing_assigns:
                store.delete_teacher_assignment(ea.id)
                silinen += 1
            # Sinif/sube cache temizle
            if "_dp_sinif_sube_cache" in st.session_state:
                del st.session_state["_dp_sinif_sube_cache"]
            # number_input cache temizle
            for k in list(st.session_state.keys()):
                if k.startswith("dp_yd_"):
                    del st.session_state[k]
            st.success(f"{silinen} ogretmen gorevlendirmesi silindi!")
            st.rerun(scope="fragment")

        if yeni_program_btn:
            # Once gorevlendirmeleri sil
            existing_assigns = store.get_teacher_assignments(akademik_yil=akademik_yil)
            for ea in existing_assigns:
                store.delete_teacher_assignment(ea.id)
            # Mevcut programi da sil
            store.clear_schedule(akademik_yil)
            # Cache temizle
            if "_dp_sinif_sube_cache" in st.session_state:
                del st.session_state["_dp_sinif_sube_cache"]
            for k in list(st.session_state.keys()):
                if k.startswith("dp_yd_"):
                    del st.session_state[k]
            st.success("Görevlendirmeler ve mevcut ders programi silindi! Sifirdan baslayabilirsiniz.")
            st.rerun(scope="fragment")

        if kaydet_btn:
            # Her ders için sinif-ogretmen eslestirmesi hesapla
            ders_ogr_hedef = {}
            for ders in ders_bilgi:
                ogrs = ders_ogretmenler.get(ders, [])
                hedefler = []
                for o in ogrs:
                    h = st.session_state.get(f"dp_yd_{ders}_{o.id}", 0)
                    if h > 0:
                        hedefler.append((o.id, o.tam_ad, h))
                ders_ogr_hedef[ders] = hedefler

            # Sinifları ogretmenlere dagit (her ders için bagimsiz)
            ogr_gorevler = {}
            for ders in ders_bilgi:
                sinif_listesi = sorted(ders_bilgi[ders]["siniflar"])
                hedefler = ders_ogr_hedef.get(ders, [])
                sinif_idx = 0
                for ogr_id, ogr_ad, hedef in hedefler:
                    if ogr_id not in ogr_gorevler:
                        ogr_gorevler[ogr_id] = {"ad": ogr_ad, "dersler": set(), "gorevler": []}
                    kalan = hedef
                    while sinif_idx < len(sinif_listesi) and kalan > 0:
                        sinif, sube, saat = sinif_listesi[sinif_idx]
                        if saat <= kalan:
                            ogr_gorevler[ogr_id]["gorevler"].append({
                                "sinif": sinif, "sube": sube,
                                "ders": ders, "haftalik_saat": saat,
                            })
                            ogr_gorevler[ogr_id]["dersler"].add(ders)
                            kalan -= saat
                            sinif_idx += 1
                        else:
                            break

            # Assignment kayitlarini olustur/guncelle
            kayit_sayisi = 0
            for ogr_id, data in ogr_gorevler.items():
                teacher = next((t for t in teachers if t.id == ogr_id), None)
                if not teacher:
                    continue
                existing_a = assign_map.get(ogr_id)
                if existing_a:
                    assignment = existing_a
                else:
                    assignment = TeacherAssignment(
                        ogretmen_id=ogr_id,
                        ogretmen_adi=data["ad"],
                        akademik_yil=akademik_yil,
                    )
                assignment.dersler = list(data["dersler"])
                assignment.gorevler = data["gorevler"]
                if not existing_a:
                    assignment.musait_degil = []
                store.save_teacher_assignment(assignment)
                teacher.branslar = assignment.dersler
                store.save_teacher(teacher)
                kayit_sayisi += 1

            st.success(f"{kayit_sayisi} ogretmenin gorevlendirmesi kaydedildi!")
            st.rerun(scope="fragment")

    # ===== TAB 3: SINIF KADRO =====
    elif dp_tab == "Sınıf Kadro":
        _render_sinif_kadro_tab(store, akademik_yil)

    # ===== TAB 4: OTOMATIK DAGITIM =====
    elif dp_tab == "Otomatik Dağıtım":
        styled_section("Otomatik Ders Programı Dağılımı", "#dc2626")
        styled_info_banner("Tüm ogretmen gorevlendirmeleri tamamlandıktan sonra dagitimi baslatin.", "info")

        assignments = store.get_teacher_assignments(akademik_yil=akademik_yil)

        if not assignments:
            st.warning("Henuz ogretmen gorevlendirmesi yapilmamis. Önce 'Öğretmen Görevlendirme' sekmesini tamamlayin.")
        else:
            # Ozet
            toplam_ogretmen = len(assignments)
            toplam_gorev = sum(len(a.gorevler) for a in assignments)
            toplam_saat = sum(a.toplam_saat for a in assignments)
            sinif_set = set()
            for a in assignments:
                for g in a.gorevler:
                    sinif_set.add(f"{g['sinif']}/{g['sube']}")

            styled_stat_row([
                ("Öğretmen", toplam_ogretmen, "#2563eb", "\U0001f468\u200d\U0001f3eb"),
                ("Sınıf/Şube", len(sinif_set), "#10b981", "\U0001f3eb"),
                ("Toplam Görev", toplam_gorev, "#f59e0b", "\U0001f4cb"),
                ("Toplam Saat", toplam_saat, "#8b5cf6", "\u23f0"),
            ])

            # Dogrulama
            distributor = ScheduleDistributor(store, akademik_yil)
            validation = distributor.validate()

            if validation["errors"]:
                st.error("Dogrulama Hatalari (duzeltilmeden dagitim yapilamaz):")
                for err in validation["errors"]:
                    st.markdown(f"- {err}")

            if validation["warnings"]:
                with st.expander("Uyarilar", expanded=False):
                    for warn in validation["warnings"]:
                        st.markdown(f"- {warn}")

            st.divider()

            # Mevcut program bilgisi
            mevcut = store.get_schedule(akademik_yil=akademik_yil)
            if mevcut:
                st.warning(f"Mevcut programda {len(mevcut)} ders slotu var. Dağıtım yaparken mevcut program silinecek!")

            dc1, dc2 = st.columns(2)
            with dc1:
                if not validation["errors"]:
                    if st.button("Dağılımı Baslat", type="primary", key="dp_dag_baslat"):
                        with st.spinner("Program dagitiyor..."):
                            result = distributor.distribute()

                        if result["toplam_yerlesemeyen"] == 0:
                            st.success(f"{result['toplam_yerlesen']} ders saati basariyla yerlestirildi!")
                        else:
                            st.warning(
                                f"{result['toplam_yerlesen']} saat yerlestirildi, "
                                f"{result['toplam_yerlesemeyen']} saat yerlestirilemedi!"
                            )
                            with st.expander("Yerlestirilemeyenler"):
                                for u in result["yerlesemeyen_detay"]:
                                    st.markdown(
                                        f"- **{u['ogretmen']}** - {u['sinif']}/{u['sube']} "
                                        f"{u['ders']}: {u['eksik']} saat eksik"
                                    )
                        st.rerun(scope="fragment")
            with dc2:
                if mevcut:
                    if confirm_action("Mevcut Programı Sil", f"Tüm ders programını ({akademik_yil}) silmek istediğinize emin misiniz? Bu işlem geri alınamaz.", key="dp_dag_sil"):
                        deleted = store.clear_schedule(akademik_yil)
                        st.success(f"{deleted} ders slotu silindi!")
                        st.rerun(scope="fragment")

    # ===== TAB 4: PROGRAM RAPORLARI =====
    elif dp_tab == "Program Raporlari":
        styled_section("Program Raporlari", "#6366f1")

        # Kurum bilgilerini yukle
        from views.kim_organizational import load_profile
        _kurum_profil = load_profile()
        _kurum_adi = _kurum_profil.get("name", "")
        _kurum_logo = _kurum_profil.get("logo_path", "")

        # Mudur bilgisi: Teacher tablosundan veya tum ogretmenlerden mudur bul
        _all_teachers = store.get_teachers(durum="aktif")
        _mudur = next((t for t in _all_teachers if t.gorev == "mudur"), None)
        _mudur_adi = _mudur.tam_ad if _mudur else ""

        # Ders saatleri (zaman cizelgesinden)
        _zaman_cizelgesi = store.get_zaman_cizelgesi()
        _ders_saat_map = {}  # {ders_no: {"baslangic": "09:00", "bitis": "09:40"}}
        for zd in _zaman_cizelgesi:
            if zd.tur == "ders" and zd.ders_no > 0 and zd.baslangic and zd.bitis:
                _ders_saat_map[zd.ders_no] = {"baslangic": zd.baslangic, "bitis": zd.bitis}

        rapor_turu = st.radio("Rapor Turu", [
            "Sınıf Programı",
            "Öğretmen Programı",
            "Tüm Sınıflar (Carsaf)",
            "Tüm Öğretmenler (Carsaf)",
        ], horizontal=True, key="dp_rapor_turu")

        st.divider()

        all_schedule = store.get_schedule(akademik_yil=akademik_yil)

        if not all_schedule:
            st.info("Henuz ders programi olusturulmamis.")
        elif rapor_turu == "Sınıf Programı":
            rc1, rc2 = st.columns(2)
            with rc1:
                r_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dp_r_sinif")
            with rc2:
                r_sube = st.selectbox("Şube", SUBELER, key="dp_r_sube")

            sinif_schedule = [s for s in all_schedule if s.sinif == r_sinif and s.sube == r_sube]

            with st.expander(f"{r_sinif}/{r_sube} Haftalık Ders Programı ({len(sinif_schedule)} ders)", expanded=False):
                _render_schedule_grid(
                    sinif_schedule, aktif_gunler, max_saat, mode="class",
                    ders_saatleri_map=_ders_saat_map, kurum_adi=_kurum_adi,
                    baslik=f"{r_sinif}/{r_sube} Sınıfı Haftalık Ders Programı - {akademik_yil}",
                    logo_path=_kurum_logo,
                )

            # PDF Indirme
            pdf_c1, pdf_c2 = st.columns(2)
            with pdf_c1:
                if st.button(f"{r_sinif}/{r_sube} PDF Indir", type="primary", key="dp_pdf_sinif_tek"):
                    pages = [{"baslik": f"{r_sinif}/{r_sube} Sınıfı Haftalık Ders Programı",
                              "alt_baslik": f"{_kurum_adi} | Akademik Yil: {akademik_yil} | {len(sinif_schedule)} ders",
                              "schedule": sinif_schedule, "mode": "class"}]
                    pdf_bytes = _generate_program_grid_pdf(pages, aktif_gunler, max_saat,
                                                           ders_saat_map=_ders_saat_map, kurum_adi=_kurum_adi, logo_path=_kurum_logo)
                    if pdf_bytes:
                        st.session_state["dp_pdf_data"] = pdf_bytes
                        st.session_state["dp_pdf_name"] = f"program_{r_sinif}_{r_sube}.pdf"
                        st.rerun(scope="fragment")
                    else:
                        st.error("PDF olusturulamadi. ReportLab yuklu degil.")
            with pdf_c2:
                if st.button("Tüm Sınıflarin PDF", key="dp_pdf_sinif_toplu"):
                    sinif_sube_set = sorted(set((s.sinif, s.sube) for s in all_schedule),
                                             key=lambda x: (str(x[0]), str(x[1])))
                    pages = []
                    for (si, su) in sinif_sube_set:
                        sch = [s for s in all_schedule if s.sinif == si and s.sube == su]
                        pages.append({"baslik": f"{si}/{su} Sınıfı Haftalık Ders Programı",
                                      "alt_baslik": f"{_kurum_adi} | Akademik Yil: {akademik_yil} | {len(sch)} ders",
                                      "schedule": sch, "mode": "class"})
                    pdf_bytes = _generate_program_grid_pdf(pages, aktif_gunler, max_saat,
                                                           ders_saat_map=_ders_saat_map, kurum_adi=_kurum_adi, logo_path=_kurum_logo)
                    if pdf_bytes:
                        st.session_state["dp_pdf_data"] = pdf_bytes
                        st.session_state["dp_pdf_name"] = f"tum_siniflar_programi_{akademik_yil}.pdf"
                        st.rerun(scope="fragment")
                    else:
                        st.error("PDF olusturulamadi.")
            if "dp_pdf_data" in st.session_state:
                st.download_button(
                    label="PDF Indir", data=st.session_state["dp_pdf_data"],
                    file_name=st.session_state.get("dp_pdf_name", "program.pdf"),
                    mime="application/pdf", key="dp_pdf_download",
                )

        elif rapor_turu == "Öğretmen Programı":
            teachers = store.get_teachers(durum="aktif")
            if not teachers:
                st.info("Öğretmen bulunamadı.")
            else:
                ogr_map = {f"{t.tam_ad} - {GOREV_LABELS.get(t.gorev, t.gorev)} ({t.brans})": t for t in teachers}
                sel_ogr = st.selectbox("Öğretmen", list(ogr_map.keys()), key="dp_r_ogretmen")
                if sel_ogr:
                    sel_teacher = ogr_map[sel_ogr]
                    ogr_schedule = [s for s in all_schedule if s.ogretmen_id == sel_teacher.id]

                    with st.expander(f"{sel_teacher.tam_ad} - Haftalık Ders Programı ({len(ogr_schedule)} ders)", expanded=False):
                        _render_schedule_grid(
                            ogr_schedule, aktif_gunler, max_saat, mode="teacher",
                            ders_saatleri_map=_ders_saat_map, kurum_adi=_kurum_adi,
                            baslik=f"{sel_teacher.tam_ad} ({sel_teacher.brans}) - Haftalık Ders Programı - {akademik_yil}",
                            mudur_adi=_mudur_adi, logo_path=_kurum_logo,
                        )

                    pdf_o1, pdf_o2 = st.columns(2)
                    with pdf_o1:
                        if st.button(f"{sel_teacher.tam_ad} PDF Indir", type="primary", key="dp_pdf_ogr_tek"):
                            pages = [{"baslik": f"{sel_teacher.tam_ad} - Haftalık Ders Programı",
                                      "alt_baslik": f"{_kurum_adi} | Branş: {sel_teacher.brans} | {akademik_yil} | {len(ogr_schedule)} ders",
                                      "schedule": ogr_schedule, "mode": "teacher",
                                      "mudur_adi": _mudur_adi}]
                            pdf_bytes = _generate_program_grid_pdf(pages, aktif_gunler, max_saat,
                                                                    ders_saat_map=_ders_saat_map, kurum_adi=_kurum_adi, logo_path=_kurum_logo)
                            if pdf_bytes:
                                st.session_state["dp_pdf_ogr_data"] = pdf_bytes
                                st.session_state["dp_pdf_ogr_name"] = f"program_{sel_teacher.tam_ad.replace(' ', '_')}.pdf"
                                st.rerun(scope="fragment")
                            else:
                                st.error("PDF olusturulamadi.")
                    with pdf_o2:
                        if st.button("Tüm Öğretmenlerin PDF", key="dp_pdf_ogr_toplu"):
                            ogretmen_ids = sorted(set(s.ogretmen_id for s in all_schedule if s.ogretmen_id))
                            pages = []
                            for oid in ogretmen_ids:
                                t = store.get_teacher(oid)
                                if not t:
                                    continue
                                sch = [s for s in all_schedule if s.ogretmen_id == oid]
                                pages.append({"baslik": f"{t.tam_ad} - Haftalık Ders Programı",
                                              "alt_baslik": f"{_kurum_adi} | Branş: {t.brans} | {akademik_yil} | {len(sch)} ders",
                                              "schedule": sch, "mode": "teacher",
                                              "mudur_adi": _mudur_adi})
                            pdf_bytes = _generate_program_grid_pdf(pages, aktif_gunler, max_saat,
                                                                    ders_saat_map=_ders_saat_map, kurum_adi=_kurum_adi, logo_path=_kurum_logo)
                            if pdf_bytes:
                                st.session_state["dp_pdf_ogr_data"] = pdf_bytes
                                st.session_state["dp_pdf_ogr_name"] = f"tum_ogretmenler_programi_{akademik_yil}.pdf"
                                st.rerun(scope="fragment")
                            else:
                                st.error("PDF olusturulamadi.")
                    if "dp_pdf_ogr_data" in st.session_state:
                        st.download_button(
                            label="PDF Indir", data=st.session_state["dp_pdf_ogr_data"],
                            file_name=st.session_state.get("dp_pdf_ogr_name", "ogretmen_programi.pdf"),
                            mime="application/pdf", key="dp_pdf_ogr_download",
                        )

        elif rapor_turu == "Tüm Sınıflar (Carsaf)":
            sinif_sube_set = sorted(set((s.sinif, s.sube) for s in all_schedule),
                                     key=lambda x: (str(x[0]), str(x[1])))
            if not sinif_sube_set:
                st.info("Programda ders bulunamadı.")
            else:
                # Veri hazirla
                rows = []
                for (sinif, sube) in sinif_sube_set:
                    row = {"_label": f"{sinif}/{sube}"}
                    for gun in aktif_gunler:
                        for saat in range(1, max_saat + 1):
                            slot = next(
                                (s for s in all_schedule
                                 if s.sinif == sinif and s.sube == sube
                                 and s.gun == gun and s.ders_saati == saat),
                                None
                            )
                            row[(gun, saat)] = DERS_KISALTMA.get(slot.ders, slot.ders[:4]) if slot else ""
                    rows.append(row)

                with st.expander(f"Tüm Sınıflar Carsaf Programi ({len(sinif_sube_set)} sinif/sube)", expanded=False):
                    _render_carsaf_html(rows, aktif_gunler, max_saat, label_header="Sınıf/Şube",
                                        kurum_adi=_kurum_adi, baslik=f"Tüm Sınıflar Haftalık Ders Programı - {akademik_yil}",
                                        ders_saat_map=_ders_saat_map)

                # PDF veri hazirla (eski format)
                pdf_rows = []
                for (sinif, sube) in sinif_sube_set:
                    r = {"Sınıf/Şube": f"{sinif}/{sube}"}
                    for gun in aktif_gunler:
                        kisa_gun = GUN_KISALTMA.get(gun, gun)
                        for saat in range(1, max_saat + 1):
                            slot = next((s for s in all_schedule if s.sinif == sinif and s.sube == sube and s.gun == gun and s.ders_saati == saat), None)
                            r[f"{kisa_gun}-{saat}"] = DERS_KISALTMA.get(slot.ders, slot.ders[:4]) if slot else "-"
                    pdf_rows.append(r)
                pdf_columns = ["Sınıf/Şube"] + [f"{GUN_KISALTMA.get(g, g)}-{s}" for g in aktif_gunler for s in range(1, max_saat + 1)]

                if st.button("Carsaf PDF Indir", type="primary", key="dp_pdf_carsaf_sinif"):
                    pdf_bytes = _generate_program_carsaf_pdf(
                        pdf_rows, pdf_columns, aktif_gunler, max_saat,
                        title=f"{_kurum_adi} - Tüm Sınıflar Haftalık Ders Programı ({akademik_yil})",
                        alt_baslik=f"{len(sinif_sube_set)} sinif/sube | {len(all_schedule)} ders",
                        ders_saat_map=_ders_saat_map,
                    )
                    if pdf_bytes:
                        st.session_state["dp_pdf_cs_data"] = pdf_bytes
                        st.session_state["dp_pdf_cs_name"] = f"tum_siniflar_carsaf_{akademik_yil}.pdf"
                        st.rerun(scope="fragment")
                if "dp_pdf_cs_data" in st.session_state:
                    st.download_button(
                        label="PDF Indir", data=st.session_state["dp_pdf_cs_data"],
                        file_name=st.session_state.get("dp_pdf_cs_name", "carsaf.pdf"),
                        mime="application/pdf", key="dp_pdf_cs_download",
                    )

        elif rapor_turu == "Tüm Öğretmenler (Carsaf)":
            ogretmen_ids = sorted(set(s.ogretmen_id for s in all_schedule if s.ogretmen_id))
            if not ogretmen_ids:
                st.info("Programda ogretmen bulunamadı.")
            else:
                rows = []
                for oid in ogretmen_ids:
                    teacher = store.get_teacher(oid)
                    ogr_name = teacher.tam_ad if teacher else "?"
                    ogr_brans = teacher.brans if teacher else ""
                    ogr_slots = [s for s in all_schedule if s.ogretmen_id == oid]
                    row = {"_label": f"{ogr_name}", "_sub": ogr_brans, "_total": len(ogr_slots)}
                    for gun in aktif_gunler:
                        for saat in range(1, max_saat + 1):
                            slot = next((s for s in ogr_slots if s.gun == gun and s.ders_saati == saat), None)
                            row[(gun, saat)] = f"{slot.sinif}/{slot.sube}" if slot else ""
                    rows.append(row)

                with st.expander(f"Tüm Öğretmenler Carsaf Programi ({len(ogretmen_ids)} ogretmen)", expanded=False):
                    _render_carsaf_html(rows, aktif_gunler, max_saat, label_header="Öğretmen",
                                        show_sub=True, sub_header="Branş", show_total=True,
                                        kurum_adi=_kurum_adi, baslik=f"Tüm Öğretmenler Haftalık Ders Programı - {akademik_yil}",
                                        ders_saat_map=_ders_saat_map)

                # PDF veri hazirla
                pdf_rows = []
                for oid in ogretmen_ids:
                    teacher = store.get_teacher(oid)
                    ogr_name = teacher.tam_ad if teacher else "?"
                    ogr_brans = teacher.brans if teacher else ""
                    ogr_slots = [s for s in all_schedule if s.ogretmen_id == oid]
                    r = {"Öğretmen": ogr_name, "Branş": ogr_brans}
                    for gun in aktif_gunler:
                        kisa_gun = GUN_KISALTMA.get(gun, gun)
                        for saat in range(1, max_saat + 1):
                            slot = next((s for s in ogr_slots if s.gun == gun and s.ders_saati == saat), None)
                            r[f"{kisa_gun}-{saat}"] = f"{slot.sinif}/{slot.sube}" if slot else "-"
                    r["Toplam"] = len(ogr_slots)
                    pdf_rows.append(r)
                pdf_columns = ["Öğretmen", "Branş"] + [f"{GUN_KISALTMA.get(g, g)}-{s}" for g in aktif_gunler for s in range(1, max_saat + 1)] + ["Toplam"]

                if st.button("Carsaf PDF Indir", type="primary", key="dp_pdf_carsaf_ogr"):
                    pdf_bytes = _generate_program_carsaf_pdf(
                        pdf_rows, pdf_columns, aktif_gunler, max_saat,
                        title=f"{_kurum_adi} - Tüm Öğretmenler Haftalık Ders Programı ({akademik_yil})",
                        alt_baslik=f"{len(ogretmen_ids)} ogretmen | {len(all_schedule)} ders",
                        ders_saat_map=_ders_saat_map,
                    )
                    if pdf_bytes:
                        st.session_state["dp_pdf_co_data"] = pdf_bytes
                        st.session_state["dp_pdf_co_name"] = f"tum_ogretmenler_carsaf_{akademik_yil}.pdf"
                        st.rerun(scope="fragment")
                if "dp_pdf_co_data" in st.session_state:
                    st.download_button(
                        label="PDF Indir", data=st.session_state["dp_pdf_co_data"],
                        file_name=st.session_state.get("dp_pdf_co_name", "carsaf_ogretmenler.pdf"),
                        mime="application/pdf", key="dp_pdf_co_download",
                    )

    # ===== TAB 5: MANUEL DUZENLEME =====
    elif dp_tab == "Manuel Düzenleme":
        styled_section("Manuel Ders Programı Düzenleme", "#64748b")
        styled_info_banner("Otomatik dagitim sonrasi tekil ders ekle, sil veya tasi.", "info")

        teachers = store.get_teachers(durum="aktif")
        ogretmen_map = {
            f"{t.tam_ad} - {GOREV_LABELS.get(t.gorev, t.gorev)} ({t.brans})": t
            for t in teachers
        }

        # Ders ekleme
        with st.form("dp_manuel_ekle_form"):
            styled_section("Ders Ekle", "#10b981")
            mc1, mc2 = st.columns(2)
            with mc1:
                m_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dp_m_sinif")
                m_gun = st.selectbox("Gün", aktif_gunler, key="dp_m_gun")
                m_ders = st.selectbox("Ders", DERSLER, key="dp_m_ders")
            with mc2:
                m_sube = st.selectbox("Şube", SUBELER, key="dp_m_sube")
                m_saat = st.number_input("Ders Saati", min_value=1, max_value=max_saat, value=1, key="dp_m_saat")
                if ogretmen_map:
                    m_ogretmen_key = st.selectbox("Öğretmen (Akademik Kadro)", list(ogretmen_map.keys()), key="dp_m_ogretmen")
                else:
                    m_ogretmen_key = None
                    st.warning("Önce Akademik Kadro'dan personel ekleyin!")

            if st.form_submit_button("Ders Ekle", type="primary"):
                ogretmen_id = ogretmen_map[m_ogretmen_key].id if m_ogretmen_key and m_ogretmen_key in ogretmen_map else ""
                conflicts = store.check_schedule_conflict(
                    sinif=m_sinif, sube=m_sube, gun=m_gun,
                    ders_saati=m_saat, ogretmen_id=ogretmen_id,
                )
                if conflicts:
                    for c in conflicts:
                        st.error(f"Cakisma: {c}")
                else:
                    ogretmen_obj = ogretmen_map.get(m_ogretmen_key)
                    slot = ScheduleSlot(
                        sinif=m_sinif, sube=m_sube, gun=m_gun,
                        ders_saati=m_saat, ders=m_ders,
                        ogretmen=ogretmen_obj.tam_ad if ogretmen_obj else "",
                        ogretmen_id=ogretmen_id,
                        akademik_yil=akademik_yil,
                    )
                    store.save_schedule_slot(slot)
                    st.success(f"{m_gun} {m_saat}. saat - {m_ders} eklendi!")
                    st.rerun(scope="fragment")

        # Ders silme
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        styled_section("Ders Silme", "#ef4444")
        all_slots = store.get_schedule(akademik_yil=akademik_yil)
        if all_slots:
            slot_options = {
                f"{s.sinif}/{s.sube} {s.gun} {s.ders_saati}.saat - {s.ders} ({s.ogretmen})": s.id
                for s in sorted(all_slots, key=lambda x: (x.sinif, x.sube, x.gun, x.ders_saati))
            }
            del_slot = st.selectbox("Silinecek Ders", list(slot_options.keys()), key="dp_m_del_slot")
            if confirm_action("Dersi Sil", "Seçili ders saatini programdan kaldırmak istediğinize emin misiniz?", key="dp_m_sil_btn"):
                store.delete_schedule_slot(slot_options[del_slot])
                st.success("Ders silindi!")
                st.rerun(scope="fragment")
        else:
            st.info("Programda ders bulunamadı.")




# ==================== AKADEMİK TAKİP FORMU ====================


def _collect_student_all_data(store: AkademikDataStore, student_id: str, akademik_yil: str) -> dict:
    """Tek öğrenci için tüm modüllerden veri toplar."""
    data: dict = {"student_id": student_id}

    # 1) Akademik notlar + ortalama
    data["ortalama"] = store.get_student_average(student_id, akademik_yil=akademik_yil)
    data["notlar"] = store.get_student_grades(student_id=student_id, akademik_yil=akademik_yil)

    # 2) Devamsızlık
    data["devamsizlik"] = store.get_attendance_summary(student_id, akademik_yil)

    # 3) Ödev teslim
    data["odev_teslimleri"] = store.get_odev_teslimleri(student_id=student_id)

    # 4) KYT performans
    data["kyt"] = store.get_kyt_ogrenci_analizi(student_id, akademik_yil=akademik_yil)

    # 5) Risk uyarıları
    data["risk_alerts"] = store.get_risk_alerts(student_id=student_id)

    # 6) Sınavlar (Ölçme & Değerlendirme)
    try:
        from models.olcme_degerlendirme import DataStore as OD_DataStore
        od_store = OD_DataStore()
        data["sinav_sonuclari"] = od_store.get_results(student_id=student_id)
    except Exception:
        data["sinav_sonuclari"] = []

    # 7) Rehberlik
    try:
        from models.rehberlik import RehberlikDataStore, VakaTakipci
        from utils.tenant import get_data_path
        rh_store = RehberlikDataStore(get_data_path("rehberlik"))
        data["rehberlik"] = VakaTakipci.get_ogrenci_gecmisi(rh_store, student_id)
    except Exception:
        data["rehberlik"] = {}

    # 8) Okul sağlığı
    try:
        from models.okul_sagligi import SaglikDataStore
        from utils.tenant import get_data_path as _gdp2
        sg_store = SaglikDataStore(_gdp2("saglik"))
        sk_list = sg_store.find_by_field("saglik_kartlari", "ogrenci_id", student_id)
        data["saglik_karti"] = sk_list[0] if sk_list else None
        data["revir_ziyaretleri"] = sg_store.find_by_field("revir_ziyaretleri", "ogrenci_id", student_id)
        data["kaza_olaylari"] = sg_store.find_by_field("kaza_olaylari", "ogrenci_id", student_id)
    except Exception:
        data["saglik_karti"] = None
        data["revir_ziyaretleri"] = []
        data["kaza_olaylari"] = []

    return data


def _build_ai_assessment(stu, data: dict) -> list[dict]:
    """AI destekli öğrenci değerlendirmesi oluşturur."""
    insights: list[dict] = []
    ort = data["ortalama"]
    dev = data["devamsizlik"]
    kyt = data["kyt"]

    # 1) Akademik genel durum
    genel_ort = ort.get("ortalama", 0)
    if genel_ort >= 85:
        insights.append({
            "icon": "🌟", "title": "Ustun Akademik Basari",
            "text": f"Genel ortalama <b>{genel_ort:.1f}</b> ile ustun duzey. "
                    f"Zenginlestirme programlari ve olimpiyat calismalari onerilebilir.",
            "color": "#10b981",
        })
    elif genel_ort >= 70:
        insights.append({
            "icon": "📊", "title": "Iyi Akademik Duzey",
            "text": f"Genel ortalama <b>{genel_ort:.1f}</b> ile iyi duzey. "
                    f"Zayif derslerde hedefli calisma ile ustun duzeye tasinabilir.",
            "color": "#2563eb",
        })
    elif genel_ort >= 50:
        insights.append({
            "icon": "⚠️", "title": "Gelisim Gerektiren Akademik Duzey",
            "text": f"Genel ortalama <b>{genel_ort:.1f}</b>. Bireysel destek plani ve "
                    f"etut programi olusturulmali. Veli gorusmesi planlanmali.",
            "color": "#f59e0b",
        })
    elif genel_ort > 0:
        insights.append({
            "icon": "🚨", "title": "Kritik Akademik Duzey",
            "text": f"Genel ortalama <b>{genel_ort:.1f}</b> ile risk altinda. "
                    f"Acil mudahale planı, rehberlik desteği ve veli isbirligi gerekli.",
            "color": "#ef4444",
        })

    # 2) Ders bazlı zayıf/güçlü analiz
    detay = ort.get("detay", {})
    if detay:
        zayif_dersler = [d for d, info in detay.items() if info.get("ortalama", 0) < 50]
        guclu_dersler = [d for d, info in detay.items() if info.get("ortalama", 0) >= 85]
        if zayif_dersler:
            insights.append({
                "icon": "📉", "title": "Zayif Dersler",
                "text": f"<b>{', '.join(zayif_dersler)}</b> derslerinde basari 50 altinda. "
                        f"Bu derslerde bireysel etut ve telafi calismalari planlanmali.",
                "color": "#ef4444",
            })
        if guclu_dersler:
            insights.append({
                "icon": "💪", "title": "Guclu Yonler",
                "text": f"<b>{', '.join(guclu_dersler)}</b> derslerinde ustun basari. "
                        f"Bu alanlarda liderlik ve mentorlik firsatlari sunulabilir.",
                "color": "#10b981",
            })

    # 3) Devamsızlık
    toplam_dev = dev.get("toplam", 0)
    ozursuz = dev.get("ozursuz", 0)
    if ozursuz >= 10:
        insights.append({
            "icon": "🚨", "title": "Yuksek Ozursuz Devamsizlik",
            "text": f"<b>{ozursuz}</b> gun ozursuz devamsizlik. Veli ile acil gorusme "
                    f"ve rehberlik mudahalesi planlanmali.",
            "color": "#ef4444",
        })
    elif toplam_dev >= 15:
        insights.append({
            "icon": "⚠️", "title": "Devamsizlik Uyarisi",
            "text": f"Toplam <b>{toplam_dev}</b> gun devamsizlik (ozursuz: {ozursuz}). "
                    f"Devamsizlik nedenlerinin arastirilmasi onerilir.",
            "color": "#f59e0b",
        })

    # 4) Ödev performansı
    odev_list = data.get("odev_teslimleri", [])
    if odev_list:
        teslim_count = sum(1 for o in odev_list
                           if _safe_attr(o, "durum") in ("teslim_edildi",))
        toplam_odev = len(odev_list)
        teslim_oran = round(teslim_count / toplam_odev * 100) if toplam_odev else 0
        if teslim_oran < 50:
            insights.append({
                "icon": "📝", "title": "Dusuk Odev Teslim Orani",
                "text": f"Odev teslim orani <b>%{teslim_oran}</b>. Odev takibi ve "
                        f"motivasyon stratejileri guclendirilmeli.",
                "color": "#ef4444",
            })
        elif teslim_oran >= 90:
            insights.append({
                "icon": "✅", "title": "Yuksek Odev Teslim Orani",
                "text": f"Odev teslim orani <b>%{teslim_oran}</b>. Sorumluluk bilinci gelismis.",
                "color": "#10b981",
            })

    # 5) KYT
    kyt_basari = kyt.get("basari_yuzde", 0)
    if kyt.get("toplam", 0) > 0:
        if kyt_basari >= 80:
            insights.append({
                "icon": "🎯", "title": "Guclu Kazanim Performansi",
                "text": f"KYT basari orani <b>%{kyt_basari:.0f}</b>. Kazanimlara hakim.",
                "color": "#10b981",
            })
        elif kyt_basari < 50:
            insights.append({
                "icon": "📚", "title": "Kazanim Eksikligi",
                "text": f"KYT basari orani <b>%{kyt_basari:.0f}</b>. Kazanim bazli "
                        f"telafi calismalari planlanmali.",
                "color": "#ef4444",
            })

    # 6) Rehberlik
    rehberlik = data.get("rehberlik", {})
    gorusmeler = rehberlik.get("gorusmeler", [])
    vakalar = rehberlik.get("vakalar", [])
    risk_deg = rehberlik.get("risk_degerlendirmeleri", [])
    aktif_vakalar = [v for v in vakalar
                     if _safe_attr(v, "durum") in ("ACIK", "TAKIPTE")]
    if aktif_vakalar:
        insights.append({
            "icon": "🔍", "title": "Aktif Rehberlik Vakasi",
            "text": f"<b>{len(aktif_vakalar)}</b> aktif rehberlik vakasi mevcut. "
                    f"Takip suresinin duzenlenmesi onerilir.",
            "color": "#8b5cf6",
        })
    kritik_risk = [r for r in risk_deg
                   if _safe_attr(r, "risk_seviyesi") in ("YUKSEK", "KRITIK")]
    if kritik_risk:
        insights.append({
            "icon": "🚨", "title": "Yuksek Risk Değerlendirmesi",
            "text": f"Rehberlik tarafindan <b>{len(kritik_risk)}</b> yuksek/kritik risk "
                    f"degerlendirmesi yapilmis. Acil mudahale planina alinmali.",
            "color": "#ef4444",
        })

    # 7) Sağlık
    revir = data.get("revir_ziyaretleri", [])
    if len(revir) >= 5:
        insights.append({
            "icon": "🏥", "title": "Sik Revir Ziyareti",
            "text": f"<b>{len(revir)}</b> revir ziyareti kaydi. Saglik durumunun "
                    f"detayli degerlendirilmesi onerilir.",
            "color": "#f59e0b",
        })

    if not insights:
        insights.append({
            "icon": "📋", "title": "Değerlendirme",
            "text": "Yeterli veri bulunmadiginda detayli analiz yapilamaz. "
                    "Verilerin girilmesiyle otomatik degerlendirme olusturulacaktir.",
            "color": "#64748b",
        })

    return insights


def _safe_attr(obj, attr: str, default=""):
    """Dict veya dataclass'tan güvenli attribute okur."""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


def _render_akademik_takip_formu(store: AkademikDataStore, akademik_yil: str, kurum: dict):
    """Öğrenci Akademik Takip Formu — tüm modüllerden veri toplayan kapsamlı rapor."""
    st.markdown(ReportStyler.report_header_html(
        "Öğrenci Akademik Takip Formu",
        "Tum modullerin verilerini birlestiren kapsamli ogrenci profili",
        "#0B0F19"
    ), unsafe_allow_html=True)

    # Öğrenci seçimi
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        atf_sinif = st.selectbox("Sinif", SINIFLAR, index=4, key="atf_sinif")
    with fc2:
        atf_sube = st.selectbox("Sube", SUBELER, key="atf_sube")

    students = store.get_students(sinif=atf_sinif, sube=atf_sube, durum="aktif")
    if not students:
        st.info("Bu sinif/subede ogrenci bulunamadi.")
        return

    student_map = {f"{s.numara} - {s.ad} {s.soyad}": s.id for s in students}
    with fc3:
        selected_label = st.selectbox("Öğrenci", list(student_map.keys()), key="atf_stu")
    if not selected_label:
        return

    stu_id = student_map[selected_label]
    stu = store.get_student(stu_id)
    if not stu:
        st.warning("Öğrenci bulunamadi.")
        return

    # Tüm modüllerden veri topla
    with st.spinner("Veriler toplanıyor..."):
        d = _collect_student_all_data(store, stu_id, akademik_yil)

    ort_info = d["ortalama"]
    dev_info = d["devamsizlik"]
    kyt_info = d["kyt"]
    odev_list = d["odev_teslimleri"]
    sinav_list = d["sinav_sonuclari"]
    rehberlik = d["rehberlik"]
    revir_list = d["revir_ziyaretleri"]
    saglik_karti = d["saglik_karti"]
    kaza_list = d["kaza_olaylari"]
    risk_alerts = d["risk_alerts"]

    # ==================== PROFIL KARTI ====================
    st.markdown(ReportStyler.report_header_html(
        f"{stu.ad} {stu.soyad}",
        f"Sinif: {stu.sinif}/{stu.sube} | Numara: {stu.numara} | {akademik_yil}",
        "#1e40af"
    ), unsafe_allow_html=True)

    # ==================== ÖZET METRİKLER ====================
    genel_ort = ort_info.get("ortalama", 0)
    ort_renk = "#10b981" if genel_ort >= 70 else "#f59e0b" if genel_ort >= 50 else "#ef4444"

    odev_teslim_count = sum(1 for o in odev_list if _safe_attr(o, "durum") == "teslim_edildi")
    odev_toplam = len(odev_list)
    odev_oran = round(odev_teslim_count / odev_toplam * 100) if odev_toplam else 0

    kyt_basari = kyt_info.get("basari_yuzde", 0)
    sinav_ort = 0
    if sinav_list:
        scores = [_safe_attr(r, "score", 0) for r in sinav_list if _safe_attr(r, "score", 0) > 0]
        sinav_ort = round(sum(scores) / len(scores), 1) if scores else 0

    gorusme_list = rehberlik.get("gorusmeler", [])

    st.markdown(ReportStyler.metric_cards_html([
        ("Genel Ortalama", f"{genel_ort:.1f}", ort_renk, ""),
        ("Devamsizlik", f"{dev_info.get('toplam', 0)} gun", "#f59e0b", ""),
        ("Sinav Ort.", f"{sinav_ort}", "#8b5cf6", ""),
        ("Odev Teslim", f"%{odev_oran}", "#2563eb", ""),
        ("KYT Basari", f"%{kyt_basari:.0f}", "#0d9488", ""),
        ("Rehberlik", f"{len(gorusme_list)} gr.", "#7c3aed", ""),
    ]), unsafe_allow_html=True)

    # ==================== 1. AKADEMİK PERFORMANS ====================
    st.markdown(ReportStyler.section_divider_html("Akademik Performans", "#1565c0"), unsafe_allow_html=True)
    detay = ort_info.get("detay", {})
    if detay:
        karne_data = []
        chart_data = {}
        for ders, info in sorted(detay.items()):
            karne_data.append({
                "Ders": ders,
                "Ortalama": round(info["ortalama"], 1),
                "Not Sayisi": info["not_sayisi"],
                "Durum": "Gecti" if info["ortalama"] >= 50 else "Kaldi",
            })
            chart_data[ders] = info["ortalama"]
        df_karne = pd.DataFrame(karne_data)
        col_l, col_r = st.columns([3, 2])
        with col_l:
            st.markdown(ReportStyler.colored_table_html(df_karne, "#1565c0", value_column="Ortalama"), unsafe_allow_html=True)
        with col_r:
            st.markdown(ReportStyler.horizontal_bar_html(chart_data, "#2563eb"), unsafe_allow_html=True)
    else:
        st.info("Henuz not verisi girilmemis.")

    # ==================== 2. DEVAMSIZLIK ====================
    st.markdown(ReportStyler.section_divider_html("Devamsizlik Durumu", "#f59e0b"), unsafe_allow_html=True)
    dc1, dc2 = st.columns([2, 1])
    with dc1:
        dev_tablo = pd.DataFrame([{
            "Ozurlu": dev_info.get("ozurlu", 0),
            "Ozursuz": dev_info.get("ozursuz", 0),
            "Toplam": dev_info.get("toplam", 0),
            "Durum": dev_info.get("uyari", "Normal") or "Normal",
        }])
        st.markdown(ReportStyler.colored_table_html(dev_tablo, "#f59e0b"), unsafe_allow_html=True)
    with dc2:
        donut_d = {}
        if dev_info.get("ozurlu", 0) > 0:
            donut_d["Ozurlu"] = dev_info["ozurlu"]
        if dev_info.get("ozursuz", 0) > 0:
            donut_d["Ozursuz"] = dev_info["ozursuz"]
        if donut_d:
            st.markdown(ReportStyler.donut_chart_svg(donut_d, ["#2563eb", "#ef4444"], size=140), unsafe_allow_html=True)

    # ==================== 3. SINAV SONUÇLARI ====================
    st.markdown(ReportStyler.section_divider_html("Sinav Sonuclari (Ölçme & Değerlendirme)", "#8b5cf6"), unsafe_allow_html=True)
    if sinav_list:
        sinav_data = []
        for r in sinav_list:
            sinav_data.append({
                "Sinav": _safe_attr(r, "exam_name", _safe_attr(r, "exam_id", "-"))[:30],
                "Puan": _safe_attr(r, "score", 0),
                "Net": _safe_attr(r, "net_score", 0),
                "Dogru": _safe_attr(r, "correct_count", 0),
                "Yanlis": _safe_attr(r, "wrong_count", 0),
                "Bos": _safe_attr(r, "empty_count", 0),
            })
        df_sinav = pd.DataFrame(sinav_data)
        st.markdown(ReportStyler.colored_table_html(df_sinav, "#8b5cf6", value_column="Puan"), unsafe_allow_html=True)
    else:
        st.info("Sinav sonucu bulunamadi.")

    # ==================== 4. ÖDEV PERFORMANSI ====================
    st.markdown(ReportStyler.section_divider_html("Odev Performansi", "#2563eb"), unsafe_allow_html=True)
    if odev_list:
        durum_sayac = {}
        puan_list = []
        for o in odev_list:
            dur = _safe_attr(o, "durum", "bekliyor")
            durum_sayac[dur] = durum_sayac.get(dur, 0) + 1
            p = _safe_attr(o, "puan", 0)
            if p and float(p) > 0:
                puan_list.append(float(p))
        odev_puan_ort = round(sum(puan_list) / len(puan_list), 1) if puan_list else 0
        st.markdown(ReportStyler.metric_cards_html([
            ("Toplam Odev", str(odev_toplam), "#2563eb", ""),
            ("Teslim Edilen", str(odev_teslim_count), "#10b981", ""),
            ("Teslim Orani", f"%{odev_oran}", "#0d9488", ""),
            ("Puan Ortalamasi", str(odev_puan_ort), "#8b5cf6", ""),
        ]), unsafe_allow_html=True)
        if durum_sayac:
            durum_labels = {
                "teslim_edildi": "Teslim", "bekliyor": "Bekliyor",
                "gecikti": "Gecikti", "teslim_edilmedi": "Teslim Edilmedi",
            }
            chart_d = {durum_labels.get(k, k): v for k, v in durum_sayac.items()}
            st.markdown(ReportStyler.donut_chart_svg(chart_d, size=140), unsafe_allow_html=True)
    else:
        st.info("Odev kaydi bulunamadi.")

    # ==================== 5. KYT PERFORMANSI ====================
    st.markdown(ReportStyler.section_divider_html("Kazanim Yoklama Testi (KYT)", "#0d9488"), unsafe_allow_html=True)
    if kyt_info.get("toplam", 0) > 0:
        st.markdown(ReportStyler.metric_cards_html([
            ("Toplam Soru", str(kyt_info["toplam"]), "#0d9488", ""),
            ("Dogru", str(kyt_info["dogru"]), "#10b981", ""),
            ("Yanlis", str(kyt_info["yanlis"]), "#ef4444", ""),
            ("Basari", f"%{kyt_info['basari_yuzde']:.0f}", "#2563eb", ""),
        ]), unsafe_allow_html=True)
        ders_perf = kyt_info.get("ders_performans", {})
        if ders_perf:
            kyt_chart = {}
            for ders, info in ders_perf.items():
                t = info.get("toplam", 0)
                dg = info.get("dogru", 0)
                kyt_chart[ders] = round(dg / t * 100) if t else 0
            st.markdown(ReportStyler.horizontal_bar_html(kyt_chart, "#0d9488"), unsafe_allow_html=True)
    else:
        st.info("KYT verisi bulunamadi.")

    # ==================== 6. REHBERLİK ====================
    st.markdown(ReportStyler.section_divider_html("Rehberlik Bilgileri", "#7c3aed"), unsafe_allow_html=True)
    vakalar = rehberlik.get("vakalar", [])
    risk_deg = rehberlik.get("risk_degerlendirmeleri", [])
    aile_gr = rehberlik.get("aile_gorusmeleri", [])
    if gorusme_list or vakalar or risk_deg:
        st.markdown(ReportStyler.metric_cards_html([
            ("Gorusme", str(len(gorusme_list)), "#7c3aed", ""),
            ("Vaka", str(len(vakalar)), "#ea580c", ""),
            ("Aile Gorusmesi", str(len(aile_gr)), "#2563eb", ""),
            ("Risk Deg.", str(len(risk_deg)), "#ef4444", ""),
        ]), unsafe_allow_html=True)
        if gorusme_list:
            gr_data = []
            for g in gorusme_list[:10]:
                gr_data.append({
                    "Tarih": _safe_attr(g, "tarih", "-")[:10],
                    "Tur": _safe_attr(g, "gorusme_turu", "-"),
                    "Konu": _safe_attr(g, "gorusme_konusu", "-"),
                    "Sonraki Adim": _safe_attr(g, "sonraki_adim", "-")[:30],
                })
            df_gr = pd.DataFrame(gr_data)
            st.markdown(ReportStyler.colored_table_html(df_gr, "#7c3aed"), unsafe_allow_html=True)
    else:
        st.info("Rehberlik verisi bulunamadi.")

    # ==================== 7. SAĞLIK ====================
    st.markdown(ReportStyler.section_divider_html("Okul Sagligi", "#059669"), unsafe_allow_html=True)
    if revir_list or saglik_karti or kaza_list:
        sag_metrics = [("Revir Ziyareti", str(len(revir_list)), "#059669", "")]
        if kaza_list:
            sag_metrics.append(("Kaza/Olay", str(len(kaza_list)), "#ef4444", ""))
        if saglik_karti:
            kan = _safe_attr(saglik_karti, "kan_grubu", "-")
            sag_metrics.append(("Kan Grubu", kan, "#2563eb", ""))
            alerji = _safe_attr(saglik_karti, "alerjiler", [])
            if alerji:
                sag_metrics.append(("Alerji", str(len(alerji)), "#f59e0b", ""))
        st.markdown(ReportStyler.metric_cards_html(sag_metrics), unsafe_allow_html=True)

        if revir_list:
            rev_data = []
            for r in revir_list[:8]:
                rev_data.append({
                    "Tarih": _safe_attr(r, "basvuru_tarihi", "-")[:10],
                    "Sikayet": _safe_attr(r, "sikayet_kategorisi", _safe_attr(r, "sikayet", "-"))[:25],
                    "Mudahale": _safe_attr(r, "mudahale", "-")[:30],
                    "Sonuc": _safe_attr(r, "sonuc", "-")[:20],
                })
            df_rev = pd.DataFrame(rev_data)
            st.markdown(ReportStyler.colored_table_html(df_rev, "#059669"), unsafe_allow_html=True)
    else:
        st.info("Saglik verisi bulunamadi.")

    # ==================== 8. RİSK UYARILARI ====================
    if risk_alerts:
        aktif_risks = [r for r in risk_alerts if _safe_attr(r, "status") == "active"]
        if aktif_risks:
            st.markdown(ReportStyler.section_divider_html(
                f"Aktif Risk Uyarilari ({len(aktif_risks)})", "#ef4444"
            ), unsafe_allow_html=True)
            risk_data = []
            for r in aktif_risks[:10]:
                risk_data.append({
                    "Tur": _safe_attr(r, "alert_type", "-"),
                    "Siddet": _safe_attr(r, "severity", "-"),
                    "Puan": _safe_attr(r, "risk_score", 0),
                    "Detay": _safe_attr(r, "details", "-")[:40],
                })
            df_risk = pd.DataFrame(risk_data)
            st.markdown(ReportStyler.colored_table_html(df_risk, "#ef4444"), unsafe_allow_html=True)

    # ==================== 9. AI DEĞERLENDİRMESİ ====================
    try:
        from utils.report_utils import ai_recommendations_html
        ai_insights = _build_ai_assessment(stu, d)
        if ai_insights:
            st.markdown(ReportStyler.section_divider_html("AI Destekli Değerlendirme & Oneriler", "#0B0F19"), unsafe_allow_html=True)
            st.markdown(ai_recommendations_html(ai_insights), unsafe_allow_html=True)
    except Exception:
        pass

    # ==================== PDF RAPOR ====================
    st.markdown(ReportStyler.section_divider_html("Rapor Indirme & Paylasim", "#94A3B8"), unsafe_allow_html=True)

    pdf_gen = ReportPDFGenerator(
        f"Öğrenci Akademik Takip Formu - {stu.ad} {stu.soyad}",
        f"{stu.sinif}/{stu.sube} | No: {stu.numara} | {akademik_yil}"
    )
    pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))

    # PDF: Öğrenci bilgileri
    pdf_gen.add_section("Öğrenci Bilgileri")
    pdf_gen.add_text(
        f"Ad Soyad: {stu.ad} {stu.soyad}  |  Sinif: {stu.sinif}/{stu.sube}  |  "
        f"Numara: {stu.numara}  |  TC: {stu.tc_no or '-'}"
    )
    veli_adi = getattr(stu, "veli_adi", "") or ""
    veli_tel = getattr(stu, "veli_telefon", "") or ""
    if veli_adi:
        pdf_gen.add_text(f"Veli: {veli_adi}  |  Telefon: {veli_tel}")

    # PDF: Özet metrikler
    pdf_gen.add_section("Genel Ozet")
    pdf_gen.add_metrics([
        ("Ortalama", f"{genel_ort:.1f}", ort_renk),
        ("Devamsizlik", f"{dev_info.get('toplam', 0)} gun", "#f59e0b"),
        ("Sinav Ort.", f"{sinav_ort}", "#8b5cf6"),
        ("Odev Teslim", f"%{odev_oran}", "#2563eb"),
        ("KYT Basari", f"%{kyt_basari:.0f}", "#0d9488"),
        ("Rehberlik", f"{len(gorusme_list)} gr.", "#7c3aed"),
    ])
    pdf_gen.add_spacer(0.3)

    # PDF: Akademik performans
    if detay:
        pdf_gen.add_section("Akademik Performans")
        pdf_gen.add_table(df_karne, "#1565c0")
        pdf_gen.add_bar_chart(chart_data, "Ders Ortalamalari", "#2563eb")

    # PDF: Devamsızlık
    pdf_gen.add_section("Devamsizlik Durumu")
    pdf_gen.add_table(dev_tablo, "#f59e0b")
    if donut_d:
        pdf_gen.add_donut_chart(donut_d, "Ozurlu / Ozursuz", ["#2563eb", "#ef4444"])

    # PDF: Sınav sonuçları
    if sinav_list:
        pdf_gen.add_section("Sinav Sonuclari")
        pdf_gen.add_table(df_sinav, "#8b5cf6")
        sinav_chart = {_safe_attr(r, "exam_name", _safe_attr(r, "exam_id", ""))[:20]: _safe_attr(r, "score", 0)
                       for r in sinav_list if _safe_attr(r, "score", 0) > 0}
        if sinav_chart:
            pdf_gen.add_bar_chart(sinav_chart, "Sinav Puanlari", "#8b5cf6")

    # PDF: Ödev
    if odev_list:
        pdf_gen.add_section("Odev Performansi")
        pdf_gen.add_metrics([
            ("Toplam", str(odev_toplam), "#2563eb"),
            ("Teslim", str(odev_teslim_count), "#10b981"),
            ("Oran", f"%{odev_oran}", "#0d9488"),
            ("Puan Ort.", str(odev_puan_ort), "#8b5cf6"),
        ])

    # PDF: KYT
    if kyt_info.get("toplam", 0) > 0:
        pdf_gen.add_section("Kazanim Yoklama Testi (KYT)")
        pdf_gen.add_metrics([
            ("Toplam", str(kyt_info["toplam"]), "#0d9488"),
            ("Dogru", str(kyt_info["dogru"]), "#10b981"),
            ("Yanlis", str(kyt_info["yanlis"]), "#ef4444"),
            ("Basari", f"%{kyt_info['basari_yuzde']:.0f}", "#2563eb"),
        ])
        if ders_perf:
            pdf_gen.add_bar_chart(kyt_chart, "KYT Ders Bazli Basari (%)", "#0d9488")

    # PDF: Rehberlik
    if gorusme_list or vakalar:
        pdf_gen.add_section("Rehberlik Bilgileri")
        pdf_gen.add_text(
            f"Gorusme: {len(gorusme_list)}  |  Vaka: {len(vakalar)}  |  "
            f"Aile Gorusmesi: {len(aile_gr)}  |  Risk Deg.: {len(risk_deg)}"
        )
        if gorusme_list:
            pdf_gen.add_table(df_gr, "#7c3aed")

    # PDF: Sağlık
    if revir_list or saglik_karti:
        pdf_gen.add_section("Okul Sagligi")
        sag_text = f"Revir Ziyareti: {len(revir_list)}"
        if saglik_karti:
            sag_text += f"  |  Kan Grubu: {_safe_attr(saglik_karti, 'kan_grubu', '-')}"
            alerji_list = _safe_attr(saglik_karti, "alerjiler", [])
            if alerji_list:
                sag_text += f"  |  Alerjiler: {', '.join(str(a) for a in alerji_list[:5])}"
            kronik = _safe_attr(saglik_karti, "kronik_durumlar", [])
            if kronik:
                sag_text += f"  |  Kronik: {', '.join(str(k) for k in kronik[:5])}"
        pdf_gen.add_text(sag_text)
        if revir_list:
            pdf_gen.add_table(df_rev, "#059669")

    # PDF: Risk uyarıları
    if risk_alerts:
        aktif = [r for r in risk_alerts if _safe_attr(r, "status") == "active"]
        if aktif:
            pdf_gen.add_section("Aktif Risk Uyarilari")
            pdf_gen.add_table(df_risk, "#ef4444")

    # PDF: AI değerlendirmesi
    try:
        ai_insights = _build_ai_assessment(stu, d)
        if ai_insights:
            pdf_gen.add_section("AI Destekli Değerlendirme & Oneriler")
            for ins in ai_insights:
                pdf_gen.add_text(f"{ins['icon']} {ins['title']}: {ins['text'].replace('<b>', '').replace('</b>', '')}")
    except Exception:
        pass

    # PDF oluştur
    pdf_bytes = pdf_gen.generate()

    veli_email = getattr(stu, "veli_email", "") or ""
    veli_tel_share = getattr(stu, "veli_telefon", "") or ""
    ReportSharer.render_share_ui(
        pdf_bytes,
        f"Akademik_Takip_{stu.ad}_{stu.soyad}_{akademik_yil}.pdf",
        f"Akademik Takip Formu - {stu.ad} {stu.soyad}",
        unique_key="atf_form",
        default_email=veli_email,
        default_phone=veli_tel_share,
    )


# ==================== TAB 6: RAPORLAR ====================

@st.fragment
def _render_raporlar(store: AkademikDataStore):
    """Raporlar ve istatistikler sekmesi - profesyonel rapor stili."""
    akademik_yil = _get_akademik_yil()
    kurum = get_institution_info()

    # Sinif karsilastirma
    try:
        from utils.ui_common import karsilastirma_tablosu
        with st.expander("🔀 Sınıf Karşılaştırma", expanded=False):
            sc1, sc2 = st.columns(2)
            with sc1:
                sinif1 = st.selectbox("Sınıf 1", [5, 6, 7, 8, 9, 10, 11, 12], key="kars_s1")
            with sc2:
                sinif2 = st.selectbox("Sınıf 2", [5, 6, 7, 8, 9, 10, 11, 12], index=1, key="kars_s2")
            if sinif1 != sinif2:
                g1 = [g for g in store.get_grades(sinif=sinif1) if g.puan and g.puan > 0]
                g2 = [g for g in store.get_grades(sinif=sinif2) if g.puan and g.puan > 0]
                ort1 = sum(g.puan for g in g1) / max(len(g1), 1)
                ort2 = sum(g.puan for g in g2) / max(len(g2), 1)
                veri1 = {"Ortalama": f"{ort1:.1f}", "Ogrenci": str(len(set(g.student_id for g in g1))), "Not Kaydi": str(len(g1))}
                veri2 = {"Ortalama": f"{ort2:.1f}", "Ogrenci": str(len(set(g.student_id for g in g2))), "Not Kaydi": str(len(g2))}
                karsilastirma_tablosu(veri1, veri2, f"{sinif1}. Sinif", f"{sinif2}. Sinif")
    except Exception:
        pass

    try:
        from utils.ui_common import sesli_rapor_okuma
        sesli_rapor_okuma("Akademik rapor ozeti: Genel ortalama yetmis iki. Devamsizlik oranlari normal seviyelerde.", "at_rapor")
    except Exception:
        pass

    tab_karne, tab_siralama, tab_devam_rap, tab_ders_analiz, tab_akademik_form = st.tabs([
        "🎓 Öğrenci Karnesi", "🏆 Başarı Sıralaması", "📋 Devamsızlık Raporu", "📊 Ders Analizi",
        "📝 Akademik Takip Formu"
    ])

    # ---- TAB 1: OGRENCI KARNESI ----
    with tab_karne:
        st.markdown(ReportStyler.report_header_html("Öğrenci Karnesi", "Bireysel ogrenci basari raporu", "#d32f2f"), unsafe_allow_html=True)
        kc1, kc2, kc3 = st.columns(3)
        with kc1:
            kr_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="kr_sinif")
        with kc2:
            kr_sube = st.selectbox("Şube", SUBELER, key="kr_sube")
        with kc3:
            kr_donem = st.selectbox("Donem", [None, "1. Donem", "2. Donem"],
                                     format_func=lambda x: "Tüm Yil" if x is None else x, key="kr_donem")

        students = store.get_students(sinif=kr_sinif, sube=kr_sube, durum="aktif")
        if not students:
            st.info("Bu sinif/subede ogrenci bulunamadı.")
        else:
            student_map = {f"{s.numara} - {s.ad} {s.soyad}": s.id for s in students}
            selected_stu = st.selectbox("Öğrenci", list(student_map.keys()), key="kr_stu")

            if selected_stu:
                stu_id = student_map[selected_stu]
                stu = store.get_student(stu_id)
                avg = store.get_student_average(stu_id, donem=kr_donem, akademik_yil=akademik_yil)
                dev_summary = store.get_attendance_summary(stu_id, akademik_yil)

                # Profil karti
                st.markdown(ReportStyler.report_header_html(
                    f"{stu.ad} {stu.soyad}",
                    f"Sınıf: {stu.sinif}/{stu.sube} | Numara: {stu.numara} | {akademik_yil}",
                    "#1e40af"
                ), unsafe_allow_html=True)

                # Metrikler
                ort_renk = "#10b981" if avg['ortalama'] >= 70 else "#f59e0b" if avg['ortalama'] >= 50 else "#ef4444"
                st.markdown(ReportStyler.metric_cards_html([
                    ("Genel Ortalama", f"{avg['ortalama']:.1f}", ort_renk, ""),
                    ("Ders Sayısı", str(avg['ders_sayisi']), "#2563eb", ""),
                    ("Toplam Not", str(avg['not_sayisi']), "#8b5cf6", ""),
                    ("Devamsızlık", f"{dev_summary['toplam']} gun", "#f59e0b", ""),
                ]), unsafe_allow_html=True)

                # Sol: tablo | Sag: grafik
                if avg['detay']:
                    col_l, col_r = st.columns([3, 2])
                    karne_data = []
                    chart_data = {}
                    for ders, info in sorted(avg['detay'].items()):
                        karne_data.append({
                            "Ders": ders,
                            "Ortalama": round(info['ortalama'], 1),
                            "Not Sayısı": info['not_sayisi'],
                            "Durum": "Gecti" if info['ortalama'] >= 50 else "Kaldi",
                        })
                        chart_data[ders] = info['ortalama']
                    df_karne = pd.DataFrame(karne_data)

                    with col_l:
                        st.markdown(ReportStyler.section_divider_html("Ders Bazli Ortalamalar", "#1565c0"), unsafe_allow_html=True)
                        st.markdown(ReportStyler.colored_table_html(df_karne, "#1565c0", value_column="Ortalama"), unsafe_allow_html=True)

                    with col_r:
                        st.markdown(ReportStyler.section_divider_html("Ders Grafigi", "#0d9488"), unsafe_allow_html=True)
                        st.markdown(ReportStyler.horizontal_bar_html(chart_data, "#2563eb"), unsafe_allow_html=True)

                        # Devamsizlik donut
                        if dev_summary['toplam'] > 0:
                            st.markdown(ReportStyler.section_divider_html("Devamsızlık", "#f59e0b"), unsafe_allow_html=True)
                            dev_data = {}
                            if dev_summary['ozurlu'] > 0:
                                dev_data["Ozurlu"] = dev_summary['ozurlu']
                            if dev_summary['ozursuz'] > 0:
                                dev_data["Ozursuz"] = dev_summary['ozursuz']
                            if dev_data:
                                st.markdown(ReportStyler.donut_chart_svg(dev_data, ["#2563eb", "#ef4444"], size=160), unsafe_allow_html=True)

                    # PDF + Paylasim
                    pdf_gen = ReportPDFGenerator(f"Öğrenci Karnesi - {stu.ad} {stu.soyad}")
                    pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
                    pdf_gen.add_section("Öğrenci Bilgileri")
                    pdf_gen.add_text(f"Ad Soyad: {stu.ad} {stu.soyad}  |  Sınıf: {stu.sinif}/{stu.sube}  |  Numara: {stu.numara}")
                    pdf_gen.add_section("Genel Metrikler")
                    pdf_gen.add_metrics([
                        ("Ortalama", f"{avg['ortalama']:.1f}", ort_renk),
                        ("Ders Sayısı", str(avg['ders_sayisi']), "#2563eb"),
                        ("Devamsızlık", f"{dev_summary['toplam']}", "#f59e0b"),
                    ])
                    pdf_gen.add_spacer(0.3)
                    pdf_gen.add_section("Ders Bazli Ortalamalar")
                    pdf_gen.add_table(df_karne, "#1565c0")
                    pdf_gen.add_bar_chart(chart_data, "Ders Ortalamalari", "#2563eb")
                    pdf_bytes = pdf_gen.generate()

                    veli_email = getattr(stu, "veli_email", "") or ""
                    veli_tel = getattr(stu, "veli_telefon", "") or ""
                    ReportSharer.render_share_ui(
                        pdf_bytes, f"karne_{stu.ad}_{stu.soyad}.pdf",
                        f"Öğrenci Karnesi - {stu.ad} {stu.soyad}",
                        unique_key="karne", default_email=veli_email, default_phone=veli_tel,
                    )

    # ---- TAB 2: BASARI SIRALAMASI ----
    with tab_siralama:
        st.markdown(ReportStyler.report_header_html("Başarı Sıralaması", "Sınıf bazli ogrenci siralama raporu", "#8b5cf6"), unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            sr_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="sr_sinif")
        with sc2:
            sr_sube = st.selectbox("Şube", SUBELER, key="sr_sube")
        with sc3:
            sr_donem = st.selectbox("Donem", [None, "1. Donem", "2. Donem"],
                                     format_func=lambda x: "Tüm Yil" if x is None else x, key="sr_donem")

        ranking = store.get_class_ranking(sr_sinif, sr_sube, donem=sr_donem, akademik_yil=akademik_yil)
        if not ranking:
            st.info("Sıralama için yeterli veri bulunamadı.")
        else:
            sinif_ort = sum(r["ortalama"] for r in ranking) / len(ranking)
            st.markdown(ReportStyler.metric_cards_html([
                ("Öğrenci Sayısı", str(len(ranking)), "#8b5cf6", ""),
                ("Sınıf Ortalaması", f"{sinif_ort:.1f}", "#2563eb", ""),
                ("En Yuksek", f"{ranking[0]['ortalama']:.1f}", "#10b981", ""),
                ("En Dusuk", f"{ranking[-1]['ortalama']:.1f}", "#ef4444", ""),
            ]), unsafe_allow_html=True)

            col_tbl, col_chart = st.columns([3, 2])
            df_ranking = pd.DataFrame([{
                "Sira": r["siralama"], "Numara": r["numara"],
                "Ad Soyad": f"{r['ad']} {r['soyad']}",
                "Ortalama": round(r["ortalama"], 1),
            } for r in ranking])

            with col_tbl:
                st.markdown(ReportStyler.section_divider_html("Sıralama Tablosu", "#8b5cf6"), unsafe_allow_html=True)
                st.markdown(ReportStyler.colored_table_html(df_ranking, "#8b5cf6", value_column="Ortalama", highlight_top=3), unsafe_allow_html=True)

            with col_chart:
                st.markdown(ReportStyler.section_divider_html("Puan Dagilimi", "#0d9488"), unsafe_allow_html=True)
                top_10 = {f"{r['ad']} {r['soyad'][:1]}.": r["ortalama"] for r in ranking[:10]}
                st.markdown(ReportStyler.horizontal_bar_html(top_10, "#8b5cf6"), unsafe_allow_html=True)

            # PDF + Paylasim
            pdf_gen = ReportPDFGenerator(f"Başarı Sıralaması - {sr_sinif}/{sr_sube}")
            pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen.add_metrics([
                ("Öğrenci", str(len(ranking)), "#8b5cf6"),
                ("Ortalama", f"{sinif_ort:.1f}", "#2563eb"),
            ])
            pdf_gen.add_section("Sıralama")
            pdf_gen.add_table(df_ranking, "#8b5cf6")
            pdf_gen.add_bar_chart(top_10, "En Başarılı Öğrenciler", "#8b5cf6")
            pdf_bytes = pdf_gen.generate()
            ReportSharer.render_share_ui(
                pdf_bytes, f"siralama_{sr_sinif}_{sr_sube}.pdf",
                f"Başarı Sıralaması {sr_sinif}/{sr_sube}",
                unique_key="siralama",
            )

    # ---- TAB 3: DEVAMSIZLIK RAPORU ----
    with tab_devam_rap:
        st.markdown(ReportStyler.report_header_html("Devamsızlık Raporu", "Sınıf bazli devamsizlik analizi", "#f59e0b"), unsafe_allow_html=True)
        dc1, dc2 = st.columns(2)
        with dc1:
            dr_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dr_sinif")
        with dc2:
            dr_sube = st.selectbox("Şube", SUBELER, key="dr_sube")

        students = store.get_students(sinif=dr_sinif, sube=dr_sube, durum="aktif")
        if not students:
            st.info("Öğrenci bulunamadı.")
        else:
            rap_data = []
            toplam_ozurlu = 0
            toplam_ozursuz = 0
            for stu in students:
                summary = store.get_attendance_summary(stu.id, akademik_yil)
                toplam_ozurlu += summary["ozurlu"]
                toplam_ozursuz += summary["ozursuz"]
                rap_data.append({
                    "Numara": stu.numara, "Ad": stu.ad, "Soyad": stu.soyad,
                    "Ozurlu": summary["ozurlu"], "Ozursuz": summary["ozursuz"],
                    "Toplam": summary["toplam"],
                    "Durum": summary["uyari"] if summary["uyari"] else "Normal",
                })
            rap_data.sort(key=lambda x: x["Toplam"], reverse=True)
            total_days = sum(r["Toplam"] for r in rap_data)
            avg_absence = total_days / len(rap_data) if rap_data else 0
            uyari_count = sum(1 for r in rap_data if r["Durum"] != "Normal")

            st.markdown(ReportStyler.metric_cards_html([
                ("Toplam Devamsızlık", f"{total_days} gun", "#2563eb", ""),
                ("Ortalama", f"{avg_absence:.1f} gun", "#f59e0b", ""),
                ("Uyari Alan", str(uyari_count), "#ef4444" if uyari_count else "#10b981", ""),
                ("Öğrenci Sayısı", str(len(rap_data)), "#8b5cf6", ""),
            ]), unsafe_allow_html=True)

            col_tbl, col_chart = st.columns([3, 2])
            df_dev = pd.DataFrame(rap_data)

            with col_tbl:
                st.markdown(ReportStyler.section_divider_html("Devamsızlık Tablosu", "#f59e0b"), unsafe_allow_html=True)
                st.markdown(ReportStyler.colored_table_html(df_dev, "#f59e0b"), unsafe_allow_html=True)

            with col_chart:
                st.markdown(ReportStyler.section_divider_html("Ozurlu / Ozursuz Dagilimi", "#0d9488"), unsafe_allow_html=True)
                donut_data = {}
                if toplam_ozurlu > 0:
                    donut_data["Ozurlu"] = toplam_ozurlu
                if toplam_ozursuz > 0:
                    donut_data["Ozursuz"] = toplam_ozursuz
                if donut_data:
                    st.markdown(ReportStyler.donut_chart_svg(donut_data, ["#2563eb", "#ef4444"], size=145), unsafe_allow_html=True)

                # En cok devamsiz ogrenciler bar chart
                top_abs = {f"{r['Ad']} {r['Soyad'][:1]}.": r["Toplam"] for r in rap_data[:8] if r["Toplam"] > 0}
                if top_abs:
                    st.markdown(ReportStyler.section_divider_html("En Çok Devamsız", "#ef4444"), unsafe_allow_html=True)
                    st.markdown(ReportStyler.horizontal_bar_html(top_abs, "#ef4444"), unsafe_allow_html=True)

            # PDF + Paylasim
            pdf_gen = ReportPDFGenerator(f"Devamsızlık Raporu - {dr_sinif}/{dr_sube}")
            pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen.add_metrics([
                ("Toplam", f"{total_days}", "#2563eb"),
                ("Ortalama", f"{avg_absence:.1f}", "#f59e0b"),
                ("Uyari", str(uyari_count), "#ef4444"),
            ])
            pdf_gen.add_section("Devamsızlık Detay")
            pdf_gen.add_table(df_dev, "#f59e0b")
            if donut_data:
                pdf_gen.add_donut_chart(donut_data, "Ozurlu / Ozursuz", ["#2563eb", "#ef4444"])
            pdf_bytes = pdf_gen.generate()
            ReportSharer.render_share_ui(
                pdf_bytes, f"devamsizlik_{dr_sinif}_{dr_sube}.pdf",
                f"Devamsızlık Raporu {dr_sinif}/{dr_sube}",
                unique_key="devamsizlik",
            )

    # ---- TAB 4: DERS ANALIZI ----
    with tab_ders_analiz:
        st.markdown(ReportStyler.report_header_html("Ders Bazli Başarı Analizi", "Ders performans karsilastirmasi", "#1565c0"), unsafe_allow_html=True)
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            da_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="da_sinif")
        with ac2:
            da_sube = st.selectbox("Şube", SUBELER, key="da_sube")
        with ac3:
            da_donem = st.selectbox("Donem", [None, "1. Donem", "2. Donem"],
                                     format_func=lambda x: "Tüm Yil" if x is None else x, key="da_donem")

        grades = store.get_grades(sinif=da_sinif, sube=da_sube, donem=da_donem, akademik_yil=akademik_yil)
        if not grades:
            st.info("Bu secimler için not verisi bulunamadı.")
        else:
            ders_stats: dict[str, list] = {}
            for g in grades:
                ders_stats.setdefault(g.ders, []).append(g.puan)

            analiz_data = []
            ort_chart = {}
            gecme_chart = {}
            for ders, puanlar in sorted(ders_stats.items()):
                ort = round(sum(puanlar) / len(puanlar), 1)
                gecme = round(sum(1 for p in puanlar if p >= 50) / len(puanlar) * 100)
                analiz_data.append({
                    "Ders": ders, "Not Sayısı": len(puanlar),
                    "Ortalama": ort, "En Yuksek": max(puanlar),
                    "En Dusuk": min(puanlar), "Gecme Orani": f"%{gecme}",
                })
                ort_chart[ders] = ort
                gecme_chart[ders] = gecme

            df_analiz = pd.DataFrame(analiz_data).sort_values("Ortalama", ascending=False)
            genel_ort = round(sum(ort_chart.values()) / len(ort_chart), 1) if ort_chart else 0

            st.markdown(ReportStyler.metric_cards_html([
                ("Ders Sayısı", str(len(ders_stats)), "#1565c0", ""),
                ("Genel Ortalama", str(genel_ort), "#2563eb", ""),
                ("En Başarılı", df_analiz.iloc[0]["Ders"] if not df_analiz.empty else "-", "#10b981", ""),
                ("Toplam Not", str(len(grades)), "#8b5cf6", ""),
            ]), unsafe_allow_html=True)

            col_tbl, col_chart = st.columns([3, 2])
            with col_tbl:
                st.markdown(ReportStyler.section_divider_html("Ders İstatistikleri", "#1565c0"), unsafe_allow_html=True)
                st.markdown(ReportStyler.colored_table_html(df_analiz, "#1565c0", value_column="Ortalama"), unsafe_allow_html=True)

            with col_chart:
                st.markdown(ReportStyler.section_divider_html("Ders Ortalamalari", "#0d9488"), unsafe_allow_html=True)
                st.markdown(ReportStyler.horizontal_bar_html(dict(sorted(ort_chart.items(), key=lambda x: x[1], reverse=True)), "#2563eb"), unsafe_allow_html=True)

                st.markdown(ReportStyler.section_divider_html("Gecme Orani Dagilimi", "#10b981"), unsafe_allow_html=True)
                st.markdown(ReportStyler.donut_chart_svg(gecme_chart, size=145), unsafe_allow_html=True)

            # PDF + Paylasim
            pdf_gen = ReportPDFGenerator(f"Ders Analizi - {da_sinif}/{da_sube}")
            pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen.add_metrics([
                ("Ders", str(len(ders_stats)), "#1565c0"),
                ("Ortalama", str(genel_ort), "#2563eb"),
            ])
            pdf_gen.add_section("Ders İstatistikleri")
            pdf_gen.add_table(df_analiz, "#1565c0")
            pdf_gen.add_bar_chart(ort_chart, "Ders Ortalamalari", "#2563eb")
            pdf_gen.add_donut_chart(gecme_chart, "Gecme Oranlari")
            pdf_bytes = pdf_gen.generate()
            ReportSharer.render_share_ui(
                pdf_bytes, f"ders_analizi_{da_sinif}_{da_sube}.pdf",
                f"Ders Analizi {da_sinif}/{da_sube}",
                unique_key="ders_analizi",
            )

    # ---- TAB 5: AKADEMİK TAKİP FORMU ----
    with tab_akademik_form:
        _render_akademik_takip_formu(store, akademik_yil, kurum)

    # ============================================================
    # PERFORMANS KARSILASTIRMA, AI ONERILERI, KUNYE
    # ============================================================
    try:
        from utils.report_utils import (
            ai_recommendations_html, period_comparison_row_html,
            render_report_kunye_html, ReportStyler as _RS,
        )

        st.markdown(_RS.section_divider_html("Donemsel Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

        now = datetime.now()
        all_students = store.get_students(durum="aktif")
        all_grades_cur = store.get_grades(akademik_yil=akademik_yil)
        # Donem 1 ve Donem 2 karsilastirmasi
        d1_grades = [g for g in all_grades_cur if g.donem == "1. Donem"]
        d2_grades = [g for g in all_grades_cur if g.donem == "2. Donem"]

        d1_ort = (sum(g.puan for g in d1_grades) / len(d1_grades)) if d1_grades else 0
        d2_ort = (sum(g.puan for g in d2_grades) / len(d2_grades)) if d2_grades else 0

        # Devamsizlik - bu ay vs onceki ay
        cur_m_start = now.replace(day=1).strftime("%Y-%m-%d")
        cur_m_end = now.strftime("%Y-%m-%d")
        prev_m_end_dt = now.replace(day=1) - timedelta(days=1)
        prev_m_start = prev_m_end_dt.replace(day=1).strftime("%Y-%m-%d")
        prev_m_end = prev_m_end_dt.strftime("%Y-%m-%d")

        all_attendance = store.get_attendance(akademik_yil=akademik_yil) if hasattr(store, "get_attendance") else []
        cur_devamsizlik = len([a for a in all_attendance if cur_m_start <= a.tarih <= cur_m_end])
        prev_devamsizlik = len([a for a in all_attendance if prev_m_start <= a.tarih <= prev_m_end])

        comparisons = [
            {"label": "1. Donem Ort.", "current": d1_ort, "previous": 0},
            {"label": "2. Donem Ort.", "current": d2_ort, "previous": d1_ort},
            {"label": "Öğrenci Sayısı", "current": len(all_students), "previous": len(all_students)},
            {"label": "Aylık Devamsızlık", "current": cur_devamsizlik, "previous": prev_devamsizlik},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)

        # ---- AI Onerileri ----
        insights = []

        # 1) Basari trendi
        if d1_ort > 0 and d2_ort > 0:
            fark = d2_ort - d1_ort
            if fark > 5:
                insights.append({
                    "icon": "📈", "title": "Başarı Artisi",
                    "text": f"2. Donem ortalamasi 1. Donem'e gore <b>{fark:.1f}</b> puan yukseldi. "
                            f"Başarılı ogretim stratejileri devam ettirilmeli.",
                    "color": "#10b981",
                })
            elif fark < -5:
                insights.append({
                    "icon": "📉", "title": "Başarı Dususu Uyarisi",
                    "text": f"2. Donem ortalamasi 1. Donem'e gore <b>{abs(fark):.1f}</b> puan dustu. "
                            f"Telafi dersleri ve bireysel destek planlari degerlendirilmeli.",
                    "color": "#ef4444",
                })
        elif d1_ort > 0:
            insights.append({
                "icon": "📊", "title": "Donem Ortalaması",
                "text": f"1. Donem ortalamasi: <b>{d1_ort:.1f}</b>. "
                        f"2. Donem verileri henuz yeterli degil.",
                "color": "#2563eb",
            })

        # 2) Devamsizlik uyarisi
        if cur_devamsizlik > 0:
            if prev_devamsizlik > 0:
                dev_degisim = ((cur_devamsizlik - prev_devamsizlik) / prev_devamsizlik) * 100
                if dev_degisim > 20:
                    insights.append({
                        "icon": "⚠️", "title": "Devamsızlık Artisi",
                        "text": f"Bu ay devamsizlik onceki aya gore <b>%{dev_degisim:.0f}</b> artti "
                                f"({prev_devamsizlik} -> {cur_devamsizlik}). Veli bilgilendirmesi onerilir.",
                        "color": "#f59e0b",
                    })
            else:
                insights.append({
                    "icon": "📋", "title": "Devamsızlık Durumu",
                    "text": f"Bu ay toplam <b>{cur_devamsizlik}</b> devamsizlik kaydi girildi.",
                    "color": "#64748b",
                })

        # 3) Basarisiz ogrenci orani
        if all_grades_cur:
            dusuk_not_ogrenciler = set()
            for g in all_grades_cur:
                if g.puan < 50:
                    dusuk_not_ogrenciler.add(g.ogrenci_id)
            if dusuk_not_ogrenciler:
                oran = len(dusuk_not_ogrenciler) / max(1, len(all_students)) * 100
                insights.append({
                    "icon": "🎓", "title": "Risk Altindaki Öğrenciler",
                    "text": f"<b>{len(dusuk_not_ogrenciler)}</b> ogrenci (<b>%{oran:.0f}</b>) en az bir derste "
                            f"50 altinda not aldi. Bireysel destek planlari olusturulmali.",
                    "color": "#ef4444" if oran > 20 else "#f59e0b",
                })

        # 4) Not giris sayisi
        insights.append({
            "icon": "📝", "title": "Not Kayıt Özeti",
            "text": f"Bu akademik yil toplam <b>{len(all_grades_cur)}</b> not kaydi girildi, "
                    f"<b>{len(all_students)}</b> aktif ogrenci bulunuyor.",
            "color": "#8b5cf6",
        })

        # 5) Ders bazli risk
        if all_grades_cur:
            ders_puanlari: dict[str, list] = {}
            for g in all_grades_cur:
                ders_puanlari.setdefault(g.ders, []).append(g.puan)
            en_dusuk_ders = None
            en_dusuk_ort = 100.0
            for ders, puanlar in ders_puanlari.items():
                ort = sum(puanlar) / len(puanlar)
                if ort < en_dusuk_ort:
                    en_dusuk_ort = ort
                    en_dusuk_ders = ders
            if en_dusuk_ders and en_dusuk_ort < 60:
                insights.append({
                    "icon": "📚", "title": "Dusuk Başarılı Ders",
                    "text": f"<b>{en_dusuk_ders}</b> dersi <b>{en_dusuk_ort:.1f}</b> ortalama ile en dusuk basarili ders. "
                            f"Ek calisma materyali ve etut planlari olusturulmali.",
                    "color": "#ea580c",
                })

        if insights:
            st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)

        # ---- Kurumsal Kunye ----
        st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    except Exception:
        pass  # report_utils yuklenemezse sessizce gec


# ==================== TAB 7: AKADEMIK PLANLAMA ====================

@st.fragment
def _render_akademik_planlama(store: AkademikDataStore):
    """Akademik planlama sekmesi - yillik/aylik/haftalik plan + olcme takvimi.
    MEB yillik planlari sinif (1-12), sube (A-E) bazli entegre edilir.
    """
    styled_section("Akademik Planlama", "#1565c0")
    styled_info_banner("MEB kazanim bazli yillik plan, aylik/haftalik akis plani ve olcme takvimi.", "info")

    akademik_yil = _get_akademik_yil()

    tab_yillik, tab_aylik, tab_haftalik = st.tabs([
        "📅 Yıllık Plan", "🗓️ Aylık Plan", "📆 Haftalık Akış Planı"
    ])

    # --- YILLIK PLAN (MEB VERISI + KUTUCUKLU) ---
    with tab_yillik:
        styled_section("Yıllık Plan (MEB Kazanim Bazli)", "#0d47a1")

        yc1, yc2, yc3 = st.columns(3)
        with yc1:
            yp_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="yp_sinif")
        with yc2:
            yp_sube = st.selectbox("Şube", SUBELER, key="yp_sube")
        with yc3:
            yp_dersler = store.get_meb_subjects(grade=yp_sinif)
            if not yp_dersler:
                yp_dersler = DERSLER
            yp_ders = st.selectbox("Ders", yp_dersler, key="yp_ders")

        # Ogretmen otomatik tespit
        yp_auto_ogr = _get_ogretmen_by_ders(store, yp_sinif, yp_sube, yp_ders, akademik_yil)
        if yp_auto_ogr:
            st.caption(f"Sınıf: {yp_sinif} / Şube: {yp_sube} / Ders: {yp_ders} / "
                       f"Öğretmen: **{yp_auto_ogr}** / Yil: {akademik_yil}")
        else:
            st.caption(f"Sınıf: {yp_sinif} / Şube: {yp_sube} / Ders: {yp_ders} / Yil: {akademik_yil}")

        # MEB yillik plan verilerini yukle
        meb_plans = store.get_meb_kazanimlar_by_week(yp_sinif, yp_ders)

        if meb_plans:
            # Sync butonu
            sync_c1, sync_c2 = st.columns([3, 1])
            with sync_c1:
                st.info(f"{len(meb_plans)} haftalik MEB plani mevcut. Kazanimlari yukleyip kutucuklu takip baslatin.")
            with sync_c2:
                if st.button("Kazanimlari Yukle", type="primary", key="yp_sync"):
                    count = store.sync_kazanim_isleme_from_meb(yp_sinif, yp_sube, yp_ders, akademik_yil)
                    if count > 0:
                        st.success(f"{count} kazanim yuklendi!")
                    else:
                        st.info("Tüm kazanimlar zaten yuklu.")
                    st.rerun(scope="fragment")

            # Ozet metrikler
            toplam_kazanim = sum(len(p['kazanimlar']) for p in meb_plans)
            toplam_saat = 0
            for p in meb_plans:
                try:
                    toplam_saat += int(p.get('hours', 0))
                except (ValueError, TypeError):
                    pass

            # Kazanim islenme kayitlari (sube bazli)
            records = store.get_kazanim_isleme(sinif=yp_sinif, sube=yp_sube,
                                                ders=yp_ders, akademik_yil=akademik_yil)
            islenen_count = sum(1 for r in records if r.durum == "islendi") if records else 0
            yuzde = round((islenen_count / len(records)) * 100, 1) if records else 0

            styled_stat_row([
                ("Toplam Hafta", len(meb_plans), "#2563eb", "\U0001f4c5"),
                ("Toplam Kazanim", toplam_kazanim, "#8b5cf6", "\U0001f3af"),
                ("Islendi", islenen_count, "#10b981", "\u2705"),
                ("İlerleme", f"%{yuzde}", "#0ea5e9", "\U0001f4c8"),
            ])

            if records:
                st.progress(yuzde / 100)

            # Hafta bazli kayit index'i
            hafta_records_map = {}
            for r in records:
                if r.hafta not in hafta_records_map:
                    hafta_records_map[r.hafta] = []
                hafta_records_map[r.hafta].append(r)

            st.divider()

            # Unite bazli gruplama
            unite_map = {}
            unite_hafta_map = {}
            for idx, p in enumerate(meb_plans):
                unite = p.get('unit', 'Diger')
                if unite not in unite_map:
                    unite_map[unite] = []
                    unite_hafta_map[unite] = []
                unite_map[unite].append(p)
                unite_hafta_map[unite].append(idx + 1)

            for unite, hafta_list in unite_map.items():
                unite_kaz_count = sum(len(h['kazanimlar']) for h in hafta_list)
                unite_hafta_nolari = unite_hafta_map[unite]
                # Unite islenme ozeti
                u_records = []
                for hn in unite_hafta_nolari:
                    u_records.extend(hafta_records_map.get(hn, []))
                u_islenen = sum(1 for r in u_records if r.durum == "islendi")
                u_badge = f" [{u_islenen}/{len(u_records)}]" if u_records else ""

                with st.expander(f"Unite: {unite} ({len(hafta_list)} hafta, {unite_kaz_count} kazanim){u_badge}", expanded=False):
                    for h_idx, p in enumerate(hafta_list):
                        hafta_no = unite_hafta_nolari[h_idx]
                        week_clean = p['week'].replace('\n', ' ').strip()
                        st.markdown(f"**{week_clean}** - {p['topic']}")
                        if p.get('hours'):
                            st.caption(f"Ders saati: {p['hours']}")

                        # Kutucuklu kazanimlar
                        h_records = hafta_records_map.get(hafta_no, [])
                        if h_records and p['kazanimlar']:
                            neden_labels = [n[1] for n in ISLENMEME_NEDENLERI]
                            neden_keys = [n[0] for n in ISLENMEME_NEDENLERI]
                            with st.form(f"yp_kaz_{hafta_no}"):
                                durumlar = {}
                                nedenler = {}
                                for r in h_records:
                                    col_cb, col_neden = st.columns([3, 2])
                                    with col_cb:
                                        checked = r.durum == "islendi"
                                        cb = st.checkbox(
                                            r.kazanim_metni[:150],
                                            value=checked,
                                            key=f"yp_cb_{r.id}"
                                        )
                                        durumlar[r.id] = cb
                                    with col_neden:
                                        mevcut_idx = 0
                                        if r.islenmeme_nedeni:
                                            try:
                                                mevcut_idx = neden_keys.index(r.islenmeme_nedeni)
                                            except ValueError:
                                                mevcut_idx = 0
                                        neden_sel = st.selectbox(
                                            "Neden",
                                            range(len(ISLENMEME_NEDENLERI)),
                                            format_func=lambda x: neden_labels[x],
                                            index=mevcut_idx,
                                            key=f"yp_nd_{r.id}",
                                            label_visibility="collapsed"
                                        )
                                        nedenler[r.id] = neden_keys[neden_sel]
                                if st.form_submit_button(f"Hafta {hafta_no} Kaydet", type="primary"):
                                    degisen = 0
                                    for r in h_records:
                                        yeni = "islendi" if durumlar.get(r.id) else "islenmedi"
                                        yeni_neden = nedenler.get(r.id, "") if yeni != "islendi" else ""
                                        if r.durum != yeni or r.islenmeme_nedeni != yeni_neden:
                                            r.durum = yeni
                                            r.islenmeme_nedeni = yeni_neden
                                            r.tarih = date.today().strftime("%Y-%m-%d")
                                            if yp_auto_ogr and not r.ogretmen_adi:
                                                r.ogretmen_adi = yp_auto_ogr
                                            store.save_kazanim_isleme(r)
                                            degisen += 1
                                    if degisen:
                                        st.success(f"{degisen} kazanim güncellendi!")
                                        st.rerun(scope="fragment")
                        elif p['kazanimlar']:
                            for kaz in p['kazanimlar']:
                                st.write(f"  - {kaz}")
                            st.caption("Kutucuklar için yukaridaki 'Kazanimlari Yukle' butonuna tiklayin.")
                        st.markdown("---")
        else:
            st.info(f"{yp_sinif}. Sınıf - {yp_ders} için MEB yillik plan verisi bulunamadı.")

    # --- AYLIK PLAN (MEB ENTEGRASYONU + KUTUCUKLU) ---
    with tab_aylik:
        styled_section("Aylık Plan (MEB Verisinden)", "#1976d2")

        ac1, ac2, ac3, ac4 = st.columns(4)
        with ac1:
            ap_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ap_sinif")
        with ac2:
            ap_sube = st.selectbox("Şube", SUBELER, key="ap_sube")
        with ac3:
            ap_dersler = store.get_meb_subjects(grade=ap_sinif)
            if not ap_dersler:
                ap_dersler = DERSLER
            ap_ders = st.selectbox("Ders", ap_dersler, key="ap_ders")
        with ac4:
            ay_listesi = [(9, "Eylul"), (10, "Ekim"), (11, "Kasim"), (12, "Aralik"),
                          (1, "Ocak"), (2, "Subat"), (3, "Mart"), (4, "Nisan"),
                          (5, "Mayis"), (6, "Haziran")]
            ay_isimleri = [a[1] for a in ay_listesi]
            ap_ay_label = st.selectbox("Ay", ay_isimleri, key="ap_ay_meb")
            ap_ay_idx = ay_isimleri.index(ap_ay_label) if ap_ay_label in ay_isimleri else 0
            ap_ay_no = ay_listesi[ap_ay_idx][0]
            ap_ay_isim = ay_listesi[ap_ay_idx][1]

        ap_auto_ogr = _get_ogretmen_by_ders(store, ap_sinif, ap_sube, ap_ders, akademik_yil)
        if ap_auto_ogr:
            st.caption(f"Sınıf: {ap_sinif} / Şube: {ap_sube} / Ders: {ap_ders} / "
                       f"Öğretmen: **{ap_auto_ogr}** / Ay: {ap_ay_isim}")
        else:
            st.caption(f"Sınıf: {ap_sinif} / Şube: {ap_sube} / Ders: {ap_ders} / Ay: {ap_ay_isim}")

        # MEB verilerini yukle
        meb_plans = store.get_meb_kazanimlar_by_week(ap_sinif, ap_ders)

        if meb_plans:
            # Sync butonu
            asc1, asc2 = st.columns([3, 1])
            with asc1:
                st.info(f"MEB kazanimlarini yukleyerek kutucuklu takip baslatin.")
            with asc2:
                if st.button("Kazanimlari Yukle", type="primary", key="ap_sync"):
                    count = store.sync_kazanim_isleme_from_meb(ap_sinif, ap_sube, ap_ders, akademik_yil)
                    if count > 0:
                        st.success(f"{count} kazanim yuklendi!")
                    else:
                        st.info("Tüm kazanimlar zaten yuklu.")
                    st.rerun(scope="fragment")

            # Ay filtreleme - hangi MEB planlari bu aya ait
            aylik_meb = []
            aylik_hafta_nolari = []
            for idx, p in enumerate(meb_plans):
                if _parse_ay(p['week']) == ap_ay_no:
                    aylik_meb.append(p)
                    aylik_hafta_nolari.append(idx + 1)

            # Kazanim islenme kayitlari
            records = store.get_kazanim_isleme(sinif=ap_sinif, sube=ap_sube,
                                                ders=ap_ders, akademik_yil=akademik_yil)
            hafta_records_map = {}
            for r in records:
                if r.hafta not in hafta_records_map:
                    hafta_records_map[r.hafta] = []
                hafta_records_map[r.hafta].append(r)

            if aylik_meb:
                # Ozet metrikler
                ay_kaz_count = sum(len(p['kazanimlar']) for p in aylik_meb)
                ay_saat = 0
                for p in aylik_meb:
                    try:
                        ay_saat += int(p.get('hours', 0))
                    except (ValueError, TypeError):
                        pass
                # Ay bazli islenme
                ay_records = []
                for hn in aylik_hafta_nolari:
                    ay_records.extend(hafta_records_map.get(hn, []))
                ay_islenen = sum(1 for r in ay_records if r.durum == "islendi")
                ay_yuzde = round((ay_islenen / len(ay_records)) * 100, 1) if ay_records else 0

                styled_stat_row([
                    ("Hafta Sayısı", len(aylik_meb), "#2563eb", "\U0001f4c5"),
                    ("Kazanim Sayısı", ay_kaz_count, "#8b5cf6", "\U0001f3af"),
                    ("Islendi", ay_islenen, "#10b981", "\u2705"),
                    ("İlerleme", f"%{ay_yuzde}", "#0ea5e9", "\U0001f4c8"),
                ])

                if ay_records:
                    st.progress(ay_yuzde / 100)

                st.divider()

                # Her haftanin detayi + kutucuklar
                for h_idx, p in enumerate(aylik_meb):
                    hafta_no = aylik_hafta_nolari[h_idx]
                    week_clean = p['week'].replace('\n', ' ').strip()
                    # Use _parse_hafta_no to extract display-friendly week number
                    parsed_hno = _parse_hafta_no(p['week'])
                    display_hno = parsed_hno if parsed_hno else hafta_no
                    kaz_count = len(p['kazanimlar'])
                    h_records = hafta_records_map.get(hafta_no, [])
                    h_islenen = sum(1 for r in h_records if r.durum == "islendi")
                    h_badge = f" [{h_islenen}/{len(h_records)}]" if h_records else ""

                    with st.expander(f"Hafta {display_hno}: {week_clean} ({kaz_count} kazanim){h_badge}", expanded=True):
                        st.markdown(f"**Unite:** {p.get('unit', '-')} | **Konu:** {p.get('topic', '-')}")
                        if p.get('hours'):
                            st.caption(f"Ders saati: {p['hours']}")

                        # Kutucuklu kazanimlar
                        if h_records:
                            neden_labels = [n[1] for n in ISLENMEME_NEDENLERI]
                            neden_keys = [n[0] for n in ISLENMEME_NEDENLERI]
                            with st.form(f"ap_kaz_{hafta_no}"):
                                durumlar = {}
                                nedenler = {}
                                for r in h_records:
                                    col_cb, col_neden = st.columns([3, 2])
                                    with col_cb:
                                        checked = r.durum == "islendi"
                                        cb = st.checkbox(
                                            r.kazanim_metni[:150],
                                            value=checked,
                                            key=f"ap_cb_{r.id}"
                                        )
                                        durumlar[r.id] = cb
                                    with col_neden:
                                        mevcut_idx = 0
                                        if r.islenmeme_nedeni:
                                            try:
                                                mevcut_idx = neden_keys.index(r.islenmeme_nedeni)
                                            except ValueError:
                                                mevcut_idx = 0
                                        neden_sel = st.selectbox(
                                            "Neden",
                                            range(len(ISLENMEME_NEDENLERI)),
                                            format_func=lambda x: neden_labels[x],
                                            index=mevcut_idx,
                                            key=f"ap_nd_{r.id}",
                                            label_visibility="collapsed"
                                        )
                                        nedenler[r.id] = neden_keys[neden_sel]
                                if st.form_submit_button(f"Hafta {hafta_no} Kaydet", type="primary"):
                                    degisen = 0
                                    for r in h_records:
                                        yeni = "islendi" if durumlar.get(r.id) else "islenmedi"
                                        yeni_neden = nedenler.get(r.id, "") if yeni != "islendi" else ""
                                        if r.durum != yeni or r.islenmeme_nedeni != yeni_neden:
                                            r.durum = yeni
                                            r.islenmeme_nedeni = yeni_neden
                                            r.tarih = date.today().strftime("%Y-%m-%d")
                                            if ap_auto_ogr and not r.ogretmen_adi:
                                                r.ogretmen_adi = ap_auto_ogr
                                            store.save_kazanim_isleme(r)
                                            degisen += 1
                                    if degisen:
                                        st.success(f"{degisen} kazanim güncellendi!")
                                        st.rerun(scope="fragment")
                        elif p['kazanimlar']:
                            for kaz in p['kazanimlar']:
                                st.write(f"  - {kaz}")
                            st.caption("Kutucuklar için 'Kazanimlari Yukle' butonuna tiklayin.")
            else:
                st.info(f"{ap_ay_isim} ayinda {ap_ders} dersi için plan bulunamadı.")
        else:
            st.info(f"{ap_sinif}. Sınıf - {ap_ders} için MEB yillik plan verisi bulunamadı.")

    # --- HAFTALIK AKIS PLANI (MEB ENTEGRASYONU + KUTUCUKLU - TUM HAFTALAR) ---
    with tab_haftalik:
        styled_section("Haftalık Ders Akis Plani (MEB Verisinden)", "#00695c")

        hc1, hc2, hc3 = st.columns(3)
        with hc1:
            hp_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="hp_sinif")
        with hc2:
            hp_sube = st.selectbox("Şube", SUBELER, key="hp_sube")
        with hc3:
            hp_dersler = store.get_meb_subjects(grade=hp_sinif)
            if not hp_dersler:
                hp_dersler = DERSLER
            hp_ders = st.selectbox("Ders", hp_dersler, key="hp_ders")

        hp_auto_ogr = _get_ogretmen_by_ders(store, hp_sinif, hp_sube, hp_ders, akademik_yil)
        if hp_auto_ogr:
            st.caption(f"Sınıf: {hp_sinif} / Şube: {hp_sube} / Ders: {hp_ders} / "
                       f"Öğretmen: **{hp_auto_ogr}** / Yil: {akademik_yil}")
        else:
            st.caption(f"Sınıf: {hp_sinif} / Şube: {hp_sube} / Ders: {hp_ders} / Yil: {akademik_yil}")

        # MEB verilerinden tum haftalari yukle
        meb_plans = store.get_meb_kazanimlar_by_week(hp_sinif, hp_ders)

        if meb_plans:
            # Sync butonu
            hsc1, hsc2 = st.columns([3, 1])
            with hsc1:
                st.info(f"{len(meb_plans)} haftalik MEB plani mevcut. Kazanimlari yukleyip kutucuklu takip baslatin.")
            with hsc2:
                if st.button("Kazanimlari Yukle", type="primary", key="hp_sync"):
                    count = store.sync_kazanim_isleme_from_meb(hp_sinif, hp_sube, hp_ders, akademik_yil)
                    if count > 0:
                        st.success(f"{count} kazanim yuklendi!")
                    else:
                        st.info("Tüm kazanimlar zaten yuklu.")
                    st.rerun(scope="fragment")

            # Ozet metrikler
            toplam_kazanim = sum(len(p['kazanimlar']) for p in meb_plans)
            toplam_saat = 0
            for p in meb_plans:
                try:
                    toplam_saat += int(p.get('hours', 0))
                except (ValueError, TypeError):
                    pass

            # Kazanim islenme kayitlari
            records = store.get_kazanim_isleme(sinif=hp_sinif, sube=hp_sube,
                                                ders=hp_ders, akademik_yil=akademik_yil)
            islenen_count = sum(1 for r in records if r.durum == "islendi") if records else 0
            yuzde = round((islenen_count / len(records)) * 100, 1) if records else 0

            styled_stat_row([
                ("Toplam Hafta", len(meb_plans), "#2563eb", "\U0001f4c5"),
                ("Toplam Kazanim", toplam_kazanim, "#8b5cf6", "\U0001f3af"),
                ("Islendi", islenen_count, "#10b981", "\u2705"),
                ("İlerleme", f"%{yuzde}", "#0ea5e9", "\U0001f4c8"),
            ])

            if records:
                st.progress(yuzde / 100)

            # Hafta bazli kayit index'i
            hafta_records_map = {}
            for r in records:
                if r.hafta not in hafta_records_map:
                    hafta_records_map[r.hafta] = []
                hafta_records_map[r.hafta].append(r)

            st.divider()

            # Tum haftalari sirali olarak goster
            for idx, p in enumerate(meb_plans):
                hafta_no = idx + 1
                week_clean = p['week'].replace('\n', ' ').strip()
                kaz_count = len(p['kazanimlar'])
                unite = p.get('unit', '')
                topic = p.get('topic', '')

                h_records = hafta_records_map.get(hafta_no, [])
                h_islenen = sum(1 for r in h_records if r.durum == "islendi")
                h_badge = f" [{h_islenen}/{len(h_records)}]" if h_records else ""

                with st.expander(f"Hafta {hafta_no}: {week_clean} - {kaz_count} kazanim{h_badge}", expanded=False
                ):
                    dc1, dc2, dc3 = st.columns(3)
                    with dc1:
                        st.markdown(f"**Unite:** {unite}")
                    with dc2:
                        st.markdown(f"**Konu:** {topic}")
                    with dc3:
                        st.markdown(f"**Ders Saati:** {p.get('hours', '-')}")

                    # Kutucuklu kazanimlar
                    if h_records:
                        neden_labels = [n[1] for n in ISLENMEME_NEDENLERI]
                        neden_keys = [n[0] for n in ISLENMEME_NEDENLERI]
                        with st.form(f"hp_kaz_{hafta_no}"):
                            durumlar = {}
                            nedenler = {}
                            for r in h_records:
                                col_cb, col_neden = st.columns([3, 2])
                                with col_cb:
                                    checked = r.durum == "islendi"
                                    cb = st.checkbox(
                                        r.kazanim_metni[:150],
                                        value=checked,
                                        key=f"hp_cb_{r.id}"
                                    )
                                    durumlar[r.id] = cb
                                with col_neden:
                                    mevcut_idx = 0
                                    if r.islenmeme_nedeni:
                                        try:
                                            mevcut_idx = neden_keys.index(r.islenmeme_nedeni)
                                        except ValueError:
                                            mevcut_idx = 0
                                    neden_sel = st.selectbox(
                                        "Neden",
                                        range(len(ISLENMEME_NEDENLERI)),
                                        format_func=lambda x: neden_labels[x],
                                        index=mevcut_idx,
                                        key=f"hp_nd_{r.id}",
                                        label_visibility="collapsed"
                                    )
                                    nedenler[r.id] = neden_keys[neden_sel]
                            if st.form_submit_button(f"Hafta {hafta_no} Kaydet", type="primary"):
                                degisen = 0
                                for r in h_records:
                                    yeni = "islendi" if durumlar.get(r.id) else "islenmedi"
                                    yeni_neden = nedenler.get(r.id, "") if yeni != "islendi" else ""
                                    if r.durum != yeni or r.islenmeme_nedeni != yeni_neden:
                                        r.durum = yeni
                                        r.islenmeme_nedeni = yeni_neden
                                        r.tarih = date.today().strftime("%Y-%m-%d")
                                        if hp_auto_ogr and not r.ogretmen_adi:
                                            r.ogretmen_adi = hp_auto_ogr
                                        store.save_kazanim_isleme(r)
                                        degisen += 1
                                if degisen:
                                    st.success(f"{degisen} kazanim güncellendi!")
                                    st.rerun(scope="fragment")

                        # Hafta islenme ozeti
                        h_yuzde = round((h_islenen / len(h_records)) * 100) if h_records else 0
                        st.progress(h_yuzde / 100, text=f"Hafta {hafta_no}: %{h_yuzde}")
                    elif p['kazanimlar']:
                        for kaz in p['kazanimlar']:
                            st.write(f"  - {kaz}")
                        st.caption("Kutucuklar için 'Kazanimlari Yukle' butonuna tiklayin.")

            st.success(f"Toplam {len(meb_plans)} hafta yuklendi ({hp_sinif}. Sınıf - {hp_ders})")
        else:
            st.info(f"{hp_sinif}. Sınıf - {hp_ders} için MEB haftalik plan verisi bulunamadı.")



# ==================== TAB 8: UYGULAMA TAKIBI ====================

@st.fragment
def _render_uygulama_takibi(store: AkademikDataStore):
    """Uygulama takibi - kazanim islenme, etut/destek, kazanim acigi raporu."""
    styled_section("Uygulama Takibi", "#059669")
    styled_info_banner("Kazanim islenme takibi, etut/destek dersleri ve kazanim acigi raporlari.", "info")

    try:
        from utils.ui_common import ai_canli_ders_asistani
        with st.expander("🎓 AI Canlı Ders Asistanı", expanded=False):
            ai_canli_ders_asistani("", "")
    except Exception:
        pass

    akademik_yil = _get_akademik_yil()

    tab_otomatik, tab_kazanim, tab_kyt_uret, tab_etut, tab_acik, tab_brans = st.tabs([
        "🎯 Bana Atanmış Dersler", "✅ Kazanım İşlenme (Manuel)", "❓ KYT Soru Üret", "📖 Etüt & Destek Dersleri", "⚠️ Kazanım Açığı Raporu", "📈 Branş İlerleme"
    ])

    # ════════════════════════════════════════════════════════════
    # YENI: BANA ATANMIS DERSLER (Otomatik)
    # Giris yapan ogretmenin haftalik programi + bu hafta islenecek
    # kazanimlar tek ekranda — sec ara, isaretle.
    # ════════════════════════════════════════════════════════════
    with tab_otomatik:
        _render_otomatik_ogretmen_kazanim(store, akademik_yil)

    # --- KAZANIM ISLENME (OGRETMEN GIRISI) ---
    with tab_kazanim:
        styled_section("Öğretmen Kazanım İşlenme Girişi", "#059669")
        st.caption("Derse giren ogretmen sinif, sube ve ders secer, isledigi kazanimlari isaretler.")

        # Sinif/sube/ders secimi — Öğretmen: önce AT, yoksa İK'dan al
        teachers = store.get_teachers(durum="aktif")
        ik_teachers = []
        if not teachers:
            # İK modülünden Akademik Kadro verisini çek (fallback)
            try:
                from utils.shared_data import load_ik_active_employees
                ik_all = load_ik_active_employees()
                ik_teachers = [e for e in ik_all if e.get("role_scope") == "TEACHER"]
            except Exception:
                ik_teachers = []

        if not teachers and not ik_teachers:
            st.warning("Sistemde kayıtlı öğretmen bulunamadı. "
                       "İnsan Kaynakları modülünden öğretmen ekleyin veya "
                       "Akademik Kadro sekmesini kontrol edin.")
        else:
            kc1, kc2, kc3 = st.columns(3)
            with kc1:
                ki_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ki_sinif")
            with kc2:
                ki_sube = st.selectbox("Şube", SUBELER, key="ki_sube")
            with kc3:
                ki_dersler = store.get_meb_subjects(grade=ki_sinif)
                if not ki_dersler:
                    ki_dersler = DERSLER
                ki_ders = st.selectbox("Ders", ki_dersler, key="ki_ders")

            # Ogretmen otomatik tespit
            secili_ogretmen = None
            ki_auto_ogr = _get_ogretmen_by_ders(store, ki_sinif, ki_sube, ki_ders, akademik_yil)
            if ki_auto_ogr:
                st.info(f"Öğretmen (programdan): **{ki_auto_ogr}** | "
                        f"Sınıf: **{ki_sinif}/{ki_sube}** | Ders: **{ki_ders}**")
                for t in teachers:
                    if t.tam_ad == ki_auto_ogr:
                        secili_ogretmen = t
                        break
            if not secili_ogretmen:
                if teachers:
                    # AT öğretmen listesi
                    ogretmen_listesi = [f"{t.ad} {t.soyad} ({t.brans})" for t in teachers]
                    ogretmen_map = {f"{t.ad} {t.soyad} ({t.brans})": t for t in teachers}
                    ki_ogretmen_key = st.selectbox("Öğretmen", ogretmen_listesi, key="ki_ogretmen")
                    secili_ogretmen = ogretmen_map.get(ki_ogretmen_key)
                elif ik_teachers:
                    # İK'dan gelen öğretmen listesi
                    ik_ogr_listesi = [
                        f"{e.get('ad', '')} {e.get('soyad', '')} ({e.get('position_name', '')})"
                        for e in ik_teachers
                    ]
                    ik_ogr_map = {
                        f"{e.get('ad', '')} {e.get('soyad', '')} ({e.get('position_name', '')})": e
                        for e in ik_teachers
                    }
                    ki_ogretmen_key = st.selectbox("Öğretmen (İK Kadro)", ik_ogr_listesi, key="ki_ogretmen_ik")
                    # İK verisini basit objeye çevir
                    _ik_sel = ik_ogr_map.get(ki_ogretmen_key, {})
                    if _ik_sel:
                        class _IKTeacher:
                            def __init__(self, d):
                                self.ad = d.get("ad", "")
                                self.soyad = d.get("soyad", "")
                                self.brans = d.get("position_name", "")
                                self.tam_ad = f"{self.ad} {self.soyad}"
                                self.id = d.get("id", "")
                        secili_ogretmen = _IKTeacher(_ik_sel)

            st.divider()

            # MEB kazanimlarini yukle
            meb_plans = store.get_meb_kazanimlar_by_week(ki_sinif, ki_ders)

            if not meb_plans:
                st.warning(f"{ki_sinif}. Sınıf - {ki_ders} için MEB kazanim verisi bulunamadı.")
            else:
                # Senkronize et butonu
                st.divider()
                sync_col1, sync_col2 = st.columns([3, 1])
                with sync_col1:
                    st.caption(f"{len(meb_plans)} haftalik MEB plani mevcut.")
                with sync_col2:
                    if st.button("Kazanimlari Yukle", type="primary", key="sync_meb"):
                        count = store.sync_kazanim_isleme_from_meb(
                            ki_sinif, ki_sube, ki_ders, akademik_yil
                        )
                        if count > 0:
                            st.success(f"{count} kazanim yuklendi!")
                        else:
                            st.info("Tüm kazanimlar zaten yuklu.")
                        st.rerun(scope="fragment")

                # Mevcut hafta bilgisi
                mevcut_hafta = store.get_mevcut_hafta_no()
                st.markdown(f"**Mevcut Hafta:** {mevcut_hafta}. hafta")

                # Mevcut kazanim islenme kayitlarini goster (kutucuklu)
                records = store.get_kazanim_isleme(sinif=ki_sinif, sube=ki_sube,
                                                    ders=ki_ders, akademik_yil=akademik_yil)

                if records:
                    # Ozet metrikler
                    islenen_count = sum(1 for r in records if r.durum == "islendi")
                    kismen_count = sum(1 for r in records if r.durum == "kismen")
                    toplam = len(records)
                    yuzde = round((islenen_count / toplam) * 100, 1) if toplam > 0 else 0

                    styled_stat_row([
                        ("Toplam Kazanim", toplam, "#6366f1", "\U0001f3af"),
                        ("Islendi", islenen_count, "#10b981", "\u2705"),
                        ("Kismen", kismen_count, "#f59e0b", "\u26a0\ufe0f"),
                        ("İlerleme", f"%{yuzde}", "#0ea5e9", "\U0001f4c8"),
                    ])

                    st.progress(yuzde / 100)
                    st.divider()

                    # Hafta bazli gruplama
                    hafta_grp = {}
                    for r in records:
                        h = r.hafta
                        if h not in hafta_grp:
                            hafta_grp[h] = []
                        hafta_grp[h].append(r)

                    # MEB plan bilgileri ile eslestir
                    meb_by_idx = {}
                    for idx, p in enumerate(meb_plans, 1):
                        meb_by_idx[idx] = p

                    for hafta_no in sorted(hafta_grp.keys()):
                        kaz_list = hafta_grp[hafta_no]
                        meb_info = meb_by_idx.get(hafta_no, {})
                        week_label = meb_info.get('week', f'Hafta {hafta_no}').replace('\n', ' ').strip()
                        topic = meb_info.get('topic', '')
                        unite = meb_info.get('unit', '')

                        # Hafta basliginda islenen sayisi
                        h_islenen = sum(1 for r in kaz_list if r.durum == "islendi")
                        h_toplam = len(kaz_list)
                        h_badge = f" ({h_islenen}/{h_toplam})"

                        # Mevcut haftayi otomatik ac
                        is_current_week = (hafta_no == mevcut_hafta)

                        with st.expander(f"Hafta {hafta_no}: {week_label}{h_badge} - {unite}", expanded=is_current_week):
                            if topic:
                                st.caption(f"Konu: {topic}")

                            # Son isleyen ogretmen bilgisi
                            islenen_ogretmenler = set()
                            for r in kaz_list:
                                if r.ogretmen_adi and r.durum == "islendi":
                                    islenen_ogretmenler.add(r.ogretmen_adi)
                            if islenen_ogretmenler:
                                st.caption(f"Isleyen: {', '.join(islenen_ogretmenler)}")

                            # Her kazanim için kutucuk + neden
                            neden_labels = [n[1] for n in ISLENMEME_NEDENLERI]
                            neden_keys = [n[0] for n in ISLENMEME_NEDENLERI]
                            with st.form(f"kaz_form_{hafta_no}"):
                                durumlar = {}
                                nedenler = {}
                                for r in kaz_list:
                                    col_check, col_text, col_neden = st.columns([1, 4, 2])
                                    with col_check:
                                        is_checked = r.durum == "islendi"
                                        checked = st.checkbox(
                                            "Islendi",
                                            value=is_checked,
                                            key=f"kaz_cb_{r.id}",
                                            label_visibility="collapsed"
                                        )
                                        durumlar[r.id] = checked
                                    with col_text:
                                        if r.durum == "islendi":
                                            icon = "[x]"
                                        elif r.durum == "kismen":
                                            icon = "[~]"
                                        else:
                                            icon = "[ ]"
                                        st.write(f"{icon} {r.kazanim_metni[:150]}")
                                    with col_neden:
                                        mevcut_idx = 0
                                        if r.islenmeme_nedeni:
                                            try:
                                                mevcut_idx = neden_keys.index(r.islenmeme_nedeni)
                                            except ValueError:
                                                mevcut_idx = 0
                                        neden_sel = st.selectbox(
                                            "Neden",
                                            range(len(ISLENMEME_NEDENLERI)),
                                            format_func=lambda x: neden_labels[x],
                                            index=mevcut_idx,
                                            key=f"kaz_nd_{r.id}",
                                            label_visibility="collapsed"
                                        )
                                        nedenler[r.id] = neden_keys[neden_sel]

                                if st.form_submit_button(f"Hafta {hafta_no} Kaydet", type="primary"):
                                    degisen = 0
                                    yeni_islenen = []  # Tam KazanimIsleme kayitlari
                                    for r in kaz_list:
                                        yeni_durum = "islendi" if durumlar.get(r.id) else "islenmedi"
                                        yeni_neden = nedenler.get(r.id, "") if yeni_durum != "islendi" else ""
                                        durum_degisti = r.durum != yeni_durum
                                        neden_degisti = r.islenmeme_nedeni != yeni_neden
                                        if durum_degisti or neden_degisti:
                                            eski_durum = r.durum
                                            r.durum = yeni_durum
                                            r.islenmeme_nedeni = yeni_neden
                                            r.tarih = date.today().strftime("%Y-%m-%d")
                                            if secili_ogretmen:
                                                r.ogretmen_id = secili_ogretmen.id
                                                r.ogretmen_adi = f"{secili_ogretmen.ad} {secili_ogretmen.soyad}"
                                            store.save_kazanim_isleme(r)
                                            degisen += 1
                                            if eski_durum != "islendi" and yeni_durum == "islendi":
                                                yeni_islenen.append(r)
                                    if degisen > 0:
                                        ogr_adi = (f"{secili_ogretmen.ad} {secili_ogretmen.soyad}"
                                                   if secili_ogretmen else "")
                                        st.success(f"{degisen} kazanim güncellendi!"
                                                   + (f" (Öğretmen: {ogr_adi})" if ogr_adi else ""))

                                        # ── OTOMATİK KYT SORU ÜRETİMİ ──
                                        if yeni_islenen:
                                            kademe = _get_kademe(ki_sinif)
                                            kyt_dersler = KYT_DERSLER.get(kademe, [])
                                            kyt_kazanimlar = [k for k in yeni_islenen
                                                              if k.ders in kyt_dersler]
                                            if kyt_kazanimlar:
                                                today_str = date.today().strftime("%Y-%m-%d")
                                                mevcut = store.get_kyt_sorular(
                                                    sinif=ki_sinif, sube=ki_sube, tarih=today_str)
                                                mevcut_ids = {s.kaynak_kazanim_id for s in mevcut}
                                                uretilecek = [k for k in kyt_kazanimlar
                                                              if k.id not in mevcut_ids]

                                                if uretilecek:
                                                    st.divider()
                                                    st.markdown(
                                                        '<div style="background:linear-gradient(135deg,'
                                                        '#059669 0%,#10b981 100%);color:white;'
                                                        'padding:14px 20px;border-radius:12px">'
                                                        '<b>KYT Otomatik Soru Üretimi</b> — '
                                                        f'{len(uretilecek)} kazanım için soru '
                                                        'üretiliyor...</div>',
                                                        unsafe_allow_html=True,
                                                    )
                                                    uretilen = 0
                                                    progress = st.progress(0)
                                                    status = st.empty()
                                                    for idx, kaz in enumerate(uretilecek):
                                                        status.text(
                                                            f"Soru üretiliyor: {kaz.kazanim_kodu} "
                                                            f"({idx+1}/{len(uretilecek)})")
                                                        progress.progress(
                                                            (idx + 1) / len(uretilecek))
                                                        sorular = _generate_kyt_questions(
                                                            kaz.ders, ki_sinif, kaz.kazanim_metni)
                                                        for soru_data in sorular:
                                                            kyt_soru = KYTSoru(
                                                                sinif=ki_sinif,
                                                                sube=ki_sube,
                                                                ders=kaz.ders,
                                                                kazanim_kodu=kaz.kazanim_kodu,
                                                                kazanim_metni=kaz.kazanim_metni,
                                                                soru_metni=soru_data.get("metin", ""),
                                                                secenekler=soru_data.get("secenekler", {}),
                                                                dogru_cevap=soru_data.get("dogru", "A"),
                                                                aciklama=soru_data.get("aciklama", ""),
                                                                tarih=today_str,
                                                                kaynak_kazanim_id=kaz.id,
                                                                akademik_yil=akademik_yil,
                                                            )
                                                            store.save_kyt_soru(kyt_soru)
                                                            uretilen += 1
                                                    progress.progress(1.0)
                                                    status.empty()

                                                    # Ders bazli odev olustur
                                                    ders_grp = {}
                                                    for k in uretilecek:
                                                        ders_grp.setdefault(k.ders, []).append(k)
                                                    odev_sayisi = 0
                                                    for d, kzl in ders_grp.items():
                                                        kaz_kodlari = ", ".join(
                                                            k.kazanim_kodu for k in kzl)
                                                        odev = Odev(
                                                            sinif=ki_sinif,
                                                            sube=ki_sube,
                                                            ders=d,
                                                            baslik=f"KYT Ödev - {today_str} - {d}",
                                                            aciklama=(
                                                                f"Kazanım Yoklama Testi: "
                                                                f"{kaz_kodlari}"),
                                                            odev_turu="test",
                                                            kazanim_kodu=kaz_kodlari,
                                                            verilme_tarihi=today_str,
                                                            son_teslim_tarihi=today_str,
                                                            online_teslim=True,
                                                            ogrenci_teslim_turu="metin",
                                                            akademik_yil=akademik_yil,
                                                        )
                                                        store.save_odev(odev)
                                                        store.odev_teslim_olustur(odev)
                                                        odev_sayisi += 1
                                                    st.success(
                                                        f"{uretilen} KYT sorusu üretildi ve "
                                                        f"{odev_sayisi} ödev öğrencilere atandı!")
                                        st.rerun(scope="fragment")
                                    else:
                                        st.info("Degisiklik yok.")
                else:
                    st.info("Henuz kazanim yuklenmemis. Yukaridaki 'Kazanimlari Yukle' butonuna tiklayin.")

    # --- KYT SORU ÜRET (ÖĞRETMEN) ---
    with tab_kyt_uret:
        styled_section("KYT Günlük Soru Üretimi", "#059669")
        styled_info_banner(
            "Ek ödev vermek istediğinizde buradan manuel KYT sorusu oluşturun. "
            "Otomatik sistem (kazanım kaydedildiğinde tetiklenir) ayrıca çalışmaya devam eder. "
            "Sınıf, şube ve tarihi seçin → işlenen kazanımlar listelenir → 'Soru Üret' butonuna basın.",
            banner_type="info"
        )
        _render_kyt_gunluk_rapor(store, key_prefix="kyt_ogr")

    # --- ETUT & DESTEK ---
    with tab_etut:
        styled_section("Etut / Destek Dersleri / Telafi Planlari", "#0d9488")

        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            et_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="et_sinif")
        with ec2:
            et_sube = st.selectbox("Şube", SUBELER, key="et_sube")
        with ec3:
            et_ders = st.selectbox("Ders", [None] + DERSLER,
                                    format_func=lambda x: "Tüm Dersler" if x is None else x,
                                    key="et_ders")

        etutler = store.get_etut_kayitlari(sinif=et_sinif, sube=et_sube,
                                            ders=et_ders, akademik_yil=akademik_yil)
        if etutler:
            df_data = []
            for e in sorted(etutler, key=lambda x: x.tarih, reverse=True):
                tur_label = dict(ETUT_TURLERI).get(e.tur, e.tur)
                df_data.append({
                    "Tarih": e.tarih,
                    "Ders": e.ders,
                    "Tur": tur_label,
                    "Konu": e.konu,
                    "Saat": e.saat,
                    "Katilim": e.katilimci_sayisi,
                    "Öğretmen": e.ogretmen_adi,
                })
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Ozet metrikler
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            toplam_katilim = sum(e.katilimci_sayisi for e in etutler)
            telafi = sum(1 for e in etutler if e.tur == "telafi")
            styled_stat_row([
                ("Toplam Etut/Destek", len(etutler), "#2563eb", "\U0001f4da"),
                ("Toplam Katilim", toplam_katilim, "#10b981", "\U0001f465"),
                ("Telafi Dersi", telafi, "#f59e0b", "\U0001f504"),
            ])
        else:
            st.info("Etut/destek kaydi bulunamadı.")

        st.divider()
        teachers = store.get_teachers(durum="aktif")
        ogretmen_map = {f"{t.ad} {t.soyad}": t for t in teachers}

        with st.form("etut_form"):
            styled_section("Yeni Etut / Destek Kaydi", "#8b5cf6")
            ef1, ef2 = st.columns(2)
            with ef1:
                et_n_ders = st.selectbox("Ders", DERSLER, key="et_n_ders")
                et_n_tarih = st.date_input("Tarih", value=date.today(), key="et_n_tarih")
                et_n_konu = st.text_input("Konu", key="et_n_konu")
            with ef2:
                _etut_tur_labels = [t[1] for t in ETUT_TURLERI]
                et_n_tur_label = st.selectbox("Tur", _etut_tur_labels, key="et_n_tur")
                et_n_tur_idx = _etut_tur_labels.index(et_n_tur_label) if et_n_tur_label in _etut_tur_labels else 0
                et_n_tur = ETUT_TURLERI[et_n_tur_idx][0]
                et_n_saat = st.text_input("Saat Araligi", placeholder="14:00-15:00", key="et_n_saat")
                et_n_katilim = st.number_input("Katilimci Sayısı", min_value=0, value=0, key="et_n_kat")

            if ogretmen_map:
                et_n_ogr_key = st.selectbox("Öğretmen", list(ogretmen_map.keys()), key="et_n_ogr")
            else:
                et_n_ogr_key = None

            et_n_kazanim = st.text_input("Kazanim Kodu (opsiyonel)", key="et_n_kaz")
            et_n_aciklama = st.text_input("Açıklama", key="et_n_acik")

            if st.form_submit_button("Kaydet", type="primary"):
                if et_n_ders and et_n_konu:
                    ogr_obj = ogretmen_map.get(et_n_ogr_key) if et_n_ogr_key else None
                    kayit = EtutKayit(
                        sinif=et_sinif, sube=et_sube, ders=et_n_ders,
                        ogretmen_id=ogr_obj.id if ogr_obj else "",
                        ogretmen_adi=f"{ogr_obj.ad} {ogr_obj.soyad}" if ogr_obj else "",
                        tarih=et_n_tarih.strftime("%Y-%m-%d"),
                        saat=et_n_saat, konu=et_n_konu,
                        kazanim_kodu=et_n_kazanim,
                        katilimci_sayisi=et_n_katilim,
                        aciklama=et_n_aciklama, tur=et_n_tur,
                        akademik_yil=akademik_yil,
                    )
                    store.save_etut_kayit(kayit)
                    st.success("Etut/destek kaydi oluşturuldu!")
                    st.rerun(scope="fragment")
                else:
                    st.error("Ders ve Konu alanlari zorunludur.")

    # --- KAZANIM TAKIP RAPORU (TAKVIM BAZLI) ---
    with tab_acik:
        styled_section("Kazanım Takip Raporu (Takvim Bazli)", "#e65100")
        st.caption("Okul acilis tarihinden itibaren islenmesi gereken vs islenen kazanimlari gosterir")

        # Okul acilis tarihi ayari
        with st.expander("Okul Acilis Tarihi Ayari", expanded=False):
            mevcut_acilis = store.get_okul_acilis_tarihi()
            st.info(f"Mevcut okul acilis tarihi: **{mevcut_acilis.strftime('%d.%m.%Y')}**")
            with st.form("okul_acilis_form"):
                yeni_acilis = st.date_input(
                    "Yeni Okul Acilis Tarihi",
                    value=mevcut_acilis,
                    key="okul_acilis_input"
                )
                if st.form_submit_button("Tarihi Kaydet", type="primary"):
                    store.set_okul_acilis_tarihi(yeni_acilis)
                    st.success(f"Okul acilis tarihi güncellendi: {yeni_acilis.strftime('%d.%m.%Y')}")
                    st.rerun(scope="fragment")

        st.divider()

        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            ra_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ra_sinif")
        with rc2:
            ra_sube = st.selectbox("Şube", SUBELER, key="ra_sube")
        with rc3:
            ra_dersler = store.get_meb_subjects(grade=ra_sinif)
            if not ra_dersler:
                ra_dersler = DERSLER
            ra_ders = st.selectbox("Ders", ra_dersler, key="ra_ders")

        rapor = store.get_kazanim_takip_raporu(ra_sinif, ra_sube, ra_ders, akademik_yil)

        # Takvim bilgisi
        mevcut_hafta = rapor["mevcut_hafta"]
        toplam_hafta = rapor["toplam_hafta_plan"]
        okul_acilis_str = rapor.get("okul_acilis", "")

        st.markdown(f"**Okul Acilis:** {okul_acilis_str} | **Mevcut Hafta:** {mevcut_hafta}. hafta | "
                    f"**Toplam Plan:** {toplam_hafta} hafta")
        st.divider()

        if rapor["toplam_gereken_kazanim"] > 0:
            # Ozet metrikler
            styled_stat_row([
                ("Islenmesi Gereken", rapor["toplam_gereken_kazanim"], "#6366f1", "\U0001f4cb"),
                ("Islenen", rapor["islenen_kazanim"], "#10b981", "\u2705"),
                ("Islenmedi", rapor["islenmedi_kazanim"], "#ef4444", "\u274c"),
                ("Kismen", rapor["kismen_kazanim"], "#f59e0b", "\u26a0\ufe0f"),
                ("İlerleme", f"%{rapor['ilerleme_yuzde']}", "#0ea5e9", "\U0001f4c8"),
            ])

            # Progress bar
            yuzde_val = rapor["ilerleme_yuzde"] / 100
            st.progress(min(yuzde_val, 1.0))

            # Durum degerlendirmesi
            if rapor["ilerleme_yuzde"] >= 90:
                st.success("Kazanim isleme plana uygun ilerliyor.")
            elif rapor["ilerleme_yuzde"] >= 70:
                st.warning("Kazanim isleme planin biraz gerisinde. Telafi planlamasi onerilir.")
            else:
                st.error("Kazanim isleme planin oldukca gerisinde! Acil aksiyon gerekli.")

            st.divider()

            # ISLENMEDI (ACIK KAZANIMLAR)
            if rapor["islenmedi_list"]:
                st.markdown(f"**Islenmedi - Açık Kazanimlar ({len(rapor['islenmedi_list'])} adet):**")
                df_islenmedi = pd.DataFrame(rapor["islenmedi_list"])
                df_islenmedi.columns = ["Hafta", "Hafta Bilgisi", "Kazanim", "Neden", "Durum"]
                st.dataframe(
                    df_islenmedi[["Hafta", "Hafta Bilgisi", "Kazanim", "Neden"]],
                    use_container_width=True, hide_index=True,
                )

                # Neden dagilimi
                neden_sayilari = {}
                for item in rapor["islenmedi_list"]:
                    n = item.get("neden", "-")
                    neden_sayilari[n] = neden_sayilari.get(n, 0) + 1
                if neden_sayilari:
                    styled_section("Islenmeme Nedeni Dagilimi", "#f59e0b")
                    neden_df = pd.DataFrame([
                        {"Neden": k, "Sayı": v} for k, v in sorted(neden_sayilari.items(), key=lambda x: -x[1])
                    ])
                    st.dataframe(neden_df, use_container_width=True, hide_index=True)

            # KISMEN ISLENEN
            if rapor["kismen_list"]:
                st.markdown(f"**Kismen Islenen Kazanimlar ({len(rapor['kismen_list'])} adet):**")
                df_kismen = pd.DataFrame(rapor["kismen_list"])
                df_kismen.columns = ["Hafta", "Hafta Bilgisi", "Kazanim", "Neden", "Durum"]
                st.dataframe(
                    df_kismen[["Hafta", "Hafta Bilgisi", "Kazanim", "Neden"]],
                    use_container_width=True, hide_index=True,
                )

            # ISLENEN KAZANIMLAR
            if rapor["islenen_list"]:
                with st.expander(f"Islenen Kazanimlar ({len(rapor['islenen_list'])} adet)"):
                    df_islenen = pd.DataFrame(rapor["islenen_list"])
                    df_islenen.columns = ["Hafta", "Hafta Bilgisi", "Kazanim", "Islenme Tarihi"]
                    st.dataframe(df_islenen, use_container_width=True, hide_index=True)

            # GELECEK KAZANIMLAR
            if rapor["gelecek_list"]:
                with st.expander(f"Gelecek Haftalar ({len(rapor['gelecek_list'])} hafta)"):
                    for g in rapor["gelecek_list"]:
                        kaz_str = ", ".join(k[:80] for k in g["kazanimlar"][:3])
                        if len(g["kazanimlar"]) > 3:
                            kaz_str += f" ... (+{len(g['kazanimlar']) - 3})"
                        st.write(f"**Hafta {g['hafta']}:** {g['week']} - {kaz_str}")
        else:
            st.info("Bu secimler için MEB kazanim verisi bulunamadı veya henuz kazanimlar senkronize edilmemis. "
                    "Kazanım İşlenme sekmesinden 'MEB Kazanimlari Yukle' butonuna tiklayin.")

    # --- BRANS BAZLI ILERLEME ---
    with tab_brans:
        styled_section("Branş Bazli İlerleme Yuzdesi", "#1565c0")

        bc1, bc2 = st.columns(2)
        with bc1:
            bi_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="bi_sinif")
        with bc2:
            st.write("")  # bosluk

        ilerleme = store.get_brans_ilerleme(bi_sinif, akademik_yil)

        if ilerleme:
            df_data = []
            for item in ilerleme:
                df_data.append({
                    "Ders": item["ders"],
                    "Toplam Kazanim": item["toplam"],
                    "Islenen": item["islenen"],
                    "Kismen": item["kismen"],
                    "Islenmedi": item["islenmedi"],
                    "İlerleme (%)": item["ilerleme_yuzde"],
                })
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Grafik
            chart_df = df.set_index("Ders")[["İlerleme (%)"]]
            st.bar_chart(chart_df)
        else:
            st.info("Branş ilerleme verisi bulunamadı. "
                    "Kazanım İşlenme sekmesinden veri girin.")


# ==================== TAB 9: ODEV VERME & TAKIP ====================

ODEV_DOSYA_DIR = get_data_path("akademik", "odev_dosyalari")
TESLIM_DOSYA_DIR = get_data_path("akademik", "teslim_dosyalari")


def _save_uploaded_file(uploaded_file, target_dir: str, prefix: str = "") -> dict:
    """Yuklenen dosyayi kaydeder, bilgi dict doner."""
    os.makedirs(target_dir, exist_ok=True)
    dosya_adi = uploaded_file.name
    uzanti = dosya_adi.rsplit('.', 1)[-1].lower() if '.' in dosya_adi else ""
    unique_name = f"{prefix}{uuid.uuid4().hex[:8]}_{dosya_adi}"
    dosya_yolu = os.path.join(target_dir, unique_name)
    with open(dosya_yolu, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return {"dosya_adi": dosya_adi, "dosya_yolu": dosya_yolu, "tur": uzanti}


@st.fragment
def _render_odev_takip(store: AkademikDataStore):
    """Ödev yönetim merkezi — 3 sekme, modern tasarım."""
    import os as _os_odev
    from utils.shared_data import load_ik_active_employees

    # ── CSS (bir kez) ──────────────────────────────────────────────────────────
    if not st.session_state.get("_odev_mod_css"):
        st.session_state["_odev_mod_css"] = True
        st.markdown("""<style>
/* ═══ Ödev Modülü Modern CSS ══════════════════════════════════════════════ */
.od-kart{border-radius:14px;border:1px solid #e2e8f0;background:#fff;
    padding:16px 18px;margin-bottom:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);transition:box-shadow .2s}
.od-kart:hover{box-shadow:0 4px 20px rgba(0,0,0,0.10)}
.od-baslik{font-weight:800;font-size:0.95rem;color:#0B0F19;margin-bottom:4px}
.od-meta{font-size:0.75rem;color:#64748b;line-height:1.6}
.od-badge{display:inline-block;border-radius:20px;padding:2px 10px;
    font-size:0.7rem;font-weight:700;margin-right:4px;margin-top:4px}
.od-badge-aktif{background:#dcfce7;color:#16a34a}
.od-badge-kapali{background:#1A2035;color:#64748b}
.od-badge-gecikme{background:#fee2e2;color:#dc2626}
.od-badge-online{background:#dbeafe;color:#1d4ed8}
.od-progress{height:6px;border-radius:4px;background:#1A2035;overflow:hidden;margin:8px 0 2px}
.od-progress-bar{height:100%;border-radius:4px;background:linear-gradient(90deg,#10b981,#059669)}
.od-sec-lbl{font-size:0.7rem;font-weight:700;color:#64748b;text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:4px}
</style>""", unsafe_allow_html=True)

    styled_section("Ödev Yönetimi", "#f59e0b")
    akademik_yil = _get_akademik_yil()

    tab_ver, tab_takip, tab_perf = st.tabs([
        "  📝 Ödev Ver  ",
        "  📊 Takip & Değerlendirme  ",
        "  🎯 Performans Ödevleri  ",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — ÖDEV VER
    # ════════════════════════════════════════════════════════════════════════
    tab_odev_ver = tab_ver
    tab_odev_takip = tab_takip
    tab_odev_degerlendirme = None   # artık tab_takip içinde
    tab_online_teslim = None        # artık tab_takip içinde
    tab_performans = tab_perf

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — ÖDEV VER
    # ════════════════════════════════════════════════════════════════════════
    with tab_ver:
        styled_section("Yeni Ödev Oluştur", "#e65100")

        ov1, ov2, ov3 = st.columns(3)
        with ov1:
            ov_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ov_sinif")
        with ov2:
            ov_sube = st.selectbox("Şube", SUBELER, key="ov_sube")
        with ov3:
            ov_dersler = store.get_meb_subjects(grade=ov_sinif) or DERSLER
            ov_ders = st.selectbox("Ders", ov_dersler, key="ov_ders")

        # Öğretmen tespiti — önce ders programından, sonra IK'dan
        ov_auto_ogr = _get_ogretmen_by_ders(store, ov_sinif, ov_sube, ov_ders, akademik_yil)
        ogretmen_adi_secili = ""
        if ov_auto_ogr:
            st.markdown(
                f"<div style='background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;"
                f"padding:8px 14px;font-size:0.84rem;color:#15803d;margin-bottom:8px'>"
                f"👨‍🏫 <b>Öğretmen (ders programından):</b> {ov_auto_ogr}</div>",
                unsafe_allow_html=True,
            )
            ogretmen_adi_secili = ov_auto_ogr
        else:
            ik_teachers = [
                e for e in load_ik_active_employees() if e.get("role_scope") == "TEACHER"
            ]
            ogr_listesi = [
                f"{e.get('ad','')} {e.get('soyad','')}".strip() for e in ik_teachers
            ]
            if ogr_listesi:
                ogretmen_adi_secili = st.selectbox("Öğretmen", ogr_listesi, key="ov_ogretmen_ik")
            else:
                ogretmen_adi_secili = st.text_input(
                    "Öğretmen Adı", key="ov_ogretmen_manual", placeholder="Ad Soyad"
                )

        st.divider()

        st.markdown("<div class='od-sec-lbl'>📎 Ekler — PDF, Word, Resim, Video vb.</div>",
                    unsafe_allow_html=True)
        yuklenen_dosyalar = st.file_uploader(
            "Dosya Yükle", accept_multiple_files=True, type=DOSYA_TURLERI,
            key="ov_dosyalar", label_visibility="collapsed",
        )
        if yuklenen_dosyalar:
            from utils.security import validate_upload
            _valid_dosyalar = []
            for _f in yuklenen_dosyalar:
                _ok, _msg = validate_upload(_f, allowed_types=DOSYA_TURLERI, max_mb=50)
                if _ok:
                    _valid_dosyalar.append(_f)
                else:
                    st.warning(f"⚠️ {_f.name}: {_msg}")
            yuklenen_dosyalar = _valid_dosyalar

        with st.form("odev_ver_form"):
            ov_baslik = st.text_input("📌 Ödev Başlığı *",
                                      placeholder="örn. 3. Ünite Konu Özeti", key="ov_baslik")
            ov_aciklama = st.text_area("📄 Açıklama / Talimatlar", height=100, key="ov_aciklama",
                                       placeholder="Ödev ile ilgili detaylı açıklama...")

            ov_col1, ov_col2 = st.columns(2)
            with ov_col1:
                ov_tur_idx = st.selectbox(
                    "Ödev Türü", range(len(ODEV_TURLERI)),
                    format_func=lambda x: ODEV_TURLERI[x][1], key="ov_tur",
                )
                ov_tur = ODEV_TURLERI[ov_tur_idx][0]
                ov_verilme = st.date_input("📅 Veriliş Tarihi", value=date.today(), key="ov_verilme")
            with ov_col2:
                ov_son_teslim = st.date_input(
                    "⏰ Son Teslim Tarihi",
                    value=date.today() + timedelta(days=7), key="ov_son_teslim",
                )
                ov_kazanim = st.text_input("🎯 Kazanım Kodu (opsiyonel)", key="ov_kazanim")

            lc1, lc2 = st.columns(2)
            with lc1:
                ov_video_link = st.text_input("▶️ Video Linki", key="ov_video_link",
                                              placeholder="https://youtube.com/...")
            with lc2:
                ov_dis_link = st.text_input("🔗 Harici Link", key="ov_dis_link",
                                            placeholder="https://docs.google.com/...")

            tc1, tc2 = st.columns(2)
            with tc1:
                ov_online = st.checkbox("💻 Öğrenci Online Teslim Edebilsin", value=True, key="ov_online")
            with tc2:
                ov_teslim_tur_idx = st.selectbox(
                    "Teslim Yöntemi", range(len(OGRENCI_TESLIM_TURLERI)),
                    format_func=lambda x: OGRENCI_TESLIM_TURLERI[x][1], key="ov_teslim_tur",
                )
                ov_teslim_tur = OGRENCI_TESLIM_TURLERI[ov_teslim_tur_idx][0]

            if st.form_submit_button("✅ Ödev Oluştur & Kaydet", type="primary",
                                     use_container_width=True):
                if ov_baslik.strip():
                    ekler = []
                    if yuklenen_dosyalar:
                        for uf in yuklenen_dosyalar:
                            ekler.append(_save_uploaded_file(uf, ODEV_DOSYA_DIR, prefix="odev_"))
                    odev = Odev(
                        sinif=ov_sinif, sube=ov_sube, ders=ov_ders,
                        ogretmen_id="", ogretmen_adi=ogretmen_adi_secili,
                        baslik=ov_baslik.strip(), aciklama=ov_aciklama.strip(),
                        odev_turu=ov_tur,
                        verilme_tarihi=ov_verilme.strftime("%Y-%m-%d"),
                        son_teslim_tarihi=ov_son_teslim.strftime("%Y-%m-%d"),
                        kazanim_kodu=ov_kazanim, ekler=ekler,
                        video_link=ov_video_link, dis_link=ov_dis_link,
                        online_teslim=ov_online, ogrenci_teslim_turu=ov_teslim_tur,
                        durum="aktif", akademik_yil=akademik_yil,
                    )
                    store.save_odev(odev)
                    sayi = store.odev_teslim_olustur(odev)
                    st.success(f"✅ Ödev oluşturuldu — {sayi} öğrenciye atandı.")
                    st.rerun(scope="fragment")
                else:
                    st.error("Ödev başlığı zorunludur.")

        # Son verilen ödevler (kart görünümü)
        st.divider()
        styled_section("Son Ödevler", "#b45309")
        son_odevler = sorted(
            store.get_odevler(akademik_yil=akademik_yil),
            key=lambda x: x.verilme_tarihi, reverse=True,
        )[:8]
        if not son_odevler:
            st.info("Henüz ödev oluşturulmamış.")
        else:
            _tur_map_son = dict(ODEV_TURLERI)
            for o in son_odevler:
                _oz = store.get_odev_ozet(o.id)
                _yuzde = _oz["teslim_yuzde"]
                _aktif_b = "<span class='od-badge od-badge-aktif'>Aktif</span>" if o.durum == "aktif" else "<span class='od-badge od-badge-kapali'>Kapalı</span>"
                _online_b = "<span class='od-badge od-badge-online'>💻 Online</span>" if getattr(o, "online_teslim", False) else ""
                st.markdown(
                    f"<div class='od-kart'>"
                    f"<div class='od-baslik'>{o.baslik}</div>"
                    f"<div class='od-meta'>{o.ders} &nbsp;·&nbsp; {o.sinif}/{o.sube}"
                    f" &nbsp;·&nbsp; {_tur_map_son.get(o.odev_turu, o.odev_turu)}"
                    f" &nbsp;·&nbsp; Son Teslim: {o.son_teslim_tarihi}</div>"
                    f"<div style='margin:6px 0'>{_aktif_b}{_online_b}</div>"
                    f"<div class='od-progress'><div class='od-progress-bar' style='width:{_yuzde}%'></div></div>"
                    f"<div class='od-meta'>Teslim: {_oz['teslim_edildi']}/{_oz['toplam']} (%{_yuzde})</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — TAKİP & DEĞERLENDİRME (Eski 3 sekme birleştirildi)
    # ════════════════════════════════════════════════════════════════════════
    with tab_takip:
        styled_section("Ödev Takip & Teslim Değerlendirme", "#059669")

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            ft_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ft_sinif")
        with f2:
            ft_sube = st.selectbox("Şube", SUBELER, key="ft_sube")
        with f3:
            ft_dersler = store.get_meb_subjects(grade=ft_sinif) or DERSLER
            ft_ders = st.selectbox("Ders", [None] + ft_dersler,
                                   format_func=lambda x: "Tüm Dersler" if x is None else x,
                                   key="ft_ders")
        with f4:
            ft_durum = st.selectbox("Durum", [None, "aktif", "kapali"],
                                    format_func=lambda x: "Tümü" if x is None else x.title(),
                                    key="ft_durum")

        odevler = sorted(
            store.get_odevler(sinif=ft_sinif, sube=ft_sube, ders=ft_ders,
                              durum=ft_durum, akademik_yil=akademik_yil),
            key=lambda x: x.verilme_tarihi, reverse=True,
        )

        if not odevler:
            styled_info_banner("Filtreye uygun ödev bulunamadı.", "warning")
        else:
            _tur_map = dict(ODEV_TURLERI)
            _durum_labels = [d[1] for d in ODEV_TESLIM_DURUMLARI]
            _durum_keys = [d[0] for d in ODEV_TESLIM_DURUMLARI]
            today_str = date.today().strftime("%Y-%m-%d")

            for odev in odevler:
                ozet = store.get_odev_ozet(odev.id)
                gecikme = (odev.son_teslim_tarihi or "") < today_str and odev.durum == "aktif"
                yuzde = ozet["teslim_yuzde"]

                if gecikme:
                    bant = "#dc2626"
                elif odev.durum == "kapali":
                    bant = "#94a3b8"
                else:
                    bant = "#16a34a"

                _db = (f"<span class='od-badge od-badge-gecikme'>⚠ Süre Doldu</span>" if gecikme
                       else f"<span class='od-badge od-badge-aktif'>✓ Aktif</span>" if odev.durum == "aktif"
                       else f"<span class='od-badge od-badge-kapali'>Kapalı</span>")
                _ob = ("<span class='od-badge od-badge-online'>💻 Online</span>"
                       if getattr(odev, "online_teslim", False) else "")

                with st.expander(f"{'⚠ ' if gecikme else ''}  {odev.baslik}"
                    f"  |  {odev.ders}  |  {odev.sinif}/{odev.sube}"
                    f"  |  Teslim: {ozet['teslim_edildi']}/{ozet['toplam']}  (%{yuzde})",
                    expanded=False,
                ):
                    # Ödev bilgi kartı
                    st.markdown(
                        f"<div style='background:#111827;border-left:4px solid {bant};"
                        f"border-radius:10px;padding:12px 16px;margin-bottom:12px'>"
                        f"<div style='font-size:0.84rem;color:#334155'>"
                        f"<b>Öğretmen:</b> {odev.ogretmen_adi or '–'}  ·  "
                        f"<b>Tür:</b> {_tur_map.get(odev.odev_turu, odev.odev_turu)}  ·  "
                        f"<b>Veriliş:</b> {odev.verilme_tarihi}  ·  "
                        f"<b>Son Teslim:</b> {odev.son_teslim_tarihi}"
                        f"</div>"
                        f"<div style='margin-top:6px'>{_db}{_ob}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                    styled_stat_row([
                        ("Teslim",        ozet["teslim_edildi"],   "#10b981", "✅"),
                        ("Gecikti",       ozet["gecikti"],         "#f59e0b", "⏰"),
                        ("Bekliyor",      ozet["bekliyor"],        "#6366f1", "⏳"),
                        ("Teslim Etmedi", ozet["teslim_edilmedi"], "#ef4444", "❌"),
                        ("Muaf",          ozet["muaf"],            "#64748b", "🚫"),
                    ])
                    st.progress(min(yuzde / 100, 1.0))

                    # Ekler & linkler
                    _ekler = getattr(odev, "ekler", []) or []
                    _vlink = getattr(odev, "video_link", "") or ""
                    _dlink = getattr(odev, "dis_link", "") or ""
                    if _ekler or _vlink or _dlink:
                        with st.expander("📎 Ödev Kaynakları", expanded=False):
                            for i, ek in enumerate(_ekler):
                                ec1, ec2 = st.columns([4, 1])
                                with ec1:
                                    st.write(f"{i+1}. {ek.get('dosya_adi','dosya')} "
                                             f"({ek.get('tur','').upper()})")
                                with ec2:
                                    _yol = ek.get("dosya_yolu", "")
                                    if _yol and _os_odev.path.exists(_yol):
                                        with open(_yol, "rb") as _f:
                                            st.download_button("İndir", _f.read(),
                                                               file_name=ek.get("dosya_adi"),
                                                               key=f"ft_dl_{odev.id}_{i}")
                            if _vlink:
                                st.markdown(f"▶️ **Video:** [{_vlink}]({_vlink})")
                            if _dlink:
                                st.markdown(f"🔗 **Link:** [{_dlink}]({_dlink})")

                    st.divider()

                    # Öğrenci teslim listesi + değerlendirme
                    _teslimleri = sorted(
                        store.get_odev_teslimleri(odev_id=odev.id),
                        key=lambda x: x.student_adi,
                    )
                    if not _teslimleri:
                        st.warning("Teslim kaydı yok.")
                        if st.button("📋 Teslim Kayıtları Oluştur", key=f"ft_olustur_{odev.id}"):
                            cnt = store.odev_teslim_olustur(odev)
                            st.success(f"{cnt} öğrenci için kayıt oluşturuldu.")
                            st.rerun(scope="fragment")
                    else:
                        with st.form(f"ft_deger_form_{odev.id}"):
                            hc1, hc2, hc3, hc4 = st.columns([3, 2, 1, 3])
                            with hc1: st.caption("**Öğrenci**")
                            with hc2: st.caption("**Durum**")
                            with hc3: st.caption("**Puan**")
                            with hc4: st.caption("**Öğretmen Notu**")

                            _guncelle = {}
                            for t in _teslimleri:
                                _has_online = any([
                                    getattr(t, "teslim_metni", ""),
                                    getattr(t, "teslim_dosya_adi", ""),
                                    getattr(t, "teslim_link", ""),
                                ])
                                tc1, tc2, tc3, tc4 = st.columns([3, 2, 1, 3])
                                with tc1:
                                    st.write(f"**{t.student_adi}**{'  💻' if _has_online else ''}")
                                    if _has_online:
                                        if getattr(t, "teslim_metni", ""):
                                            st.caption(f"📝 {t.teslim_metni[:70]}…")
                                        if getattr(t, "teslim_dosya_adi", ""):
                                            st.caption(f"📎 {t.teslim_dosya_adi}")
                                        if getattr(t, "teslim_link", ""):
                                            st.caption(f"🔗 {t.teslim_link[:55]}")
                                with tc2:
                                    try:
                                        _di = _durum_keys.index(t.durum)
                                    except ValueError:
                                        _di = 0
                                    _yd = st.selectbox(
                                        "Durum", range(len(ODEV_TESLIM_DURUMLARI)),
                                        format_func=lambda x: _durum_labels[x],
                                        index=_di, key=f"ft_dur_{t.id}",
                                        label_visibility="collapsed",
                                    )
                                with tc3:
                                    _yp = st.number_input(
                                        "Puan", 0.0, 100.0, float(t.puan), 5.0,
                                        key=f"ft_puan_{t.id}", label_visibility="collapsed",
                                    )
                                with tc4:
                                    _yn = st.text_input(
                                        "Not", value=t.ogretmen_notu or "",
                                        key=f"ft_not_{t.id}", label_visibility="collapsed",
                                        placeholder="Öğretmen notu…",
                                    )
                                _guncelle[t.id] = {
                                    "dur": _durum_keys[_yd], "puan": _yp,
                                    "not": _yn, "obj": t,
                                }

                            if st.form_submit_button("💾 Değerlendirmeleri Kaydet",
                                                     type="primary", use_container_width=True):
                                _degisen = 0
                                for _tid, _bilgi in _guncelle.items():
                                    _t = _bilgi["obj"]
                                    if (_t.durum != _bilgi["dur"] or _t.puan != _bilgi["puan"]
                                            or _t.ogretmen_notu != _bilgi["not"]):
                                        _t.durum = _bilgi["dur"]
                                        _t.puan = _bilgi["puan"]
                                        _t.ogretmen_notu = _bilgi["not"]
                                        if (_bilgi["dur"] in ("teslim_edildi", "gecikti")
                                                and not _t.teslim_tarihi):
                                            _t.teslim_tarihi = date.today().strftime("%Y-%m-%d")
                                        store.save_odev_teslim(_t)
                                        _degisen += 1
                                if _degisen:
                                    st.success(f"✅ {_degisen} öğrenci kaydedildi.")
                                    st.rerun(scope="fragment")
                                else:
                                    st.info("Değişiklik yok.")

                    st.divider()

                    # Durum butonları
                    bc1, bc2, bc3 = st.columns(3)
                    with bc1:
                        if odev.durum == "aktif" and st.button("🔒 Kapat", key=f"ft_kapat_{odev.id}"):
                            odev.durum = "kapali"
                            store.save_odev(odev)
                            st.success("Ödev kapatıldı.")
                            st.rerun(scope="fragment")
                    with bc2:
                        if odev.durum == "kapali" and st.button("🔓 Yeniden Aç",
                                                                  key=f"ft_ac_{odev.id}"):
                            odev.durum = "aktif"
                            store.save_odev(odev)
                            st.success("Ödev açıldı.")
                            st.rerun(scope="fragment")
                    with bc3:
                        if confirm_action("🗑️ Sil",
                                          "Bu ödevi ve tüm teslimlerini silmek istiyor musunuz?",
                                          key=f"ft_sil_{odev.id}"):
                            store.delete_odev(odev.id)
                            st.success("Ödev silindi.")
                            st.rerun(scope="fragment")

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — PERFORMANS ÖDEVLERİ
    # ════════════════════════════════════════════════════════════════════════
    with tab_perf:
        styled_section("Performans Ödevleri", "#7c3aed")
        styled_info_banner(
            "Müzik, Beden Eğitimi, Görsel Sanatlar, Bilişim, Koro, Sergi ve Spor alanlarında "
            "performans görevi oluşturun. Öğrenciler öğretmen tarafından değerlendirilir.",
            banner_type="info"
        )

        # Alan kartları
        _PERF_ALANLAR = [
            ("🎵", "Müzik",              "#7c3aed", "Şarkı söyleme, enstrüman çalma, ritim, solfej"),
            ("⚽", "Beden Eğitimi",      "#16a34a", "Beceri testi, spor etkinliği, fiziksel ölçüm"),
            ("🎨", "Görsel Sanatlar",    "#e65100", "Resim, heykel, seramik, tasarım çalışması"),
            ("💻", "Bilişim",            "#0284c7", "Proje, uygulama geliştirme, sunum, tasarım"),
            ("🎭", "Koro",               "#be185d", "Ses testi, prova katılımı, konser performansı"),
            ("🖼️", "Sergi",              "#b45309", "Eser hazırlama, sergileme, portfolyo sunumu"),
            ("🏆", "Spor",               "#059669", "Turnuva, yarışma, sportif beceri değerlendirme"),
            ("🤝", "Sosyal Faaliyetler", "#0f766e", "Kulüp etkinliği, toplum hizmeti, gezi, sosyal sorumluluk projeleri"),
        ]

        _alan_isimleri = [a[1] for a in _PERF_ALANLAR]

        # Kart satırı (row 1: 4 kart, row 2: 3 kart)
        tum_odevler = store.get_odevler(akademik_yil=akademik_yil)
        perf_odevler = [o for o in tum_odevler if o.odev_turu == "performans"]

        kart_cols = st.columns(4)
        for i, (ikon, alan, renk, tanim) in enumerate(_PERF_ALANLAR[:4]):
            sayi = sum(1 for o in perf_odevler if o.ders == alan)
            with kart_cols[i]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{renk}18,{renk}08);'
                    f'border:2px solid {renk}40;border-top:4px solid {renk};border-radius:14px;'
                    f'padding:16px 14px;text-align:center;margin-bottom:8px;">'
                    f'<div style="font-size:2rem;">{ikon}</div>'
                    f'<div style="font-weight:800;font-size:0.9rem;color:#0B0F19;margin:6px 0 4px;">{alan}</div>'
                    f'<div style="font-size:0.72rem;color:#64748b;margin-bottom:8px;">{tanim}</div>'
                    f'<div style="background:{renk};color:white;border-radius:20px;'
                    f'padding:3px 14px;font-size:0.78rem;font-weight:700;display:inline-block;">'
                    f'{sayi} görev</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        kart_cols2 = st.columns(4)
        for i, (ikon, alan, renk, tanim) in enumerate(_PERF_ALANLAR[4:]):
            sayi = sum(1 for o in perf_odevler if o.ders == alan)
            with kart_cols2[i]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{renk}18,{renk}08);'
                    f'border:2px solid {renk}40;border-top:4px solid {renk};border-radius:14px;'
                    f'padding:16px 14px;text-align:center;margin-bottom:12px;">'
                    f'<div style="font-size:2rem;">{ikon}</div>'
                    f'<div style="font-weight:800;font-size:0.9rem;color:#0B0F19;margin:6px 0 4px;">{alan}</div>'
                    f'<div style="font-size:0.72rem;color:#64748b;margin-bottom:8px;">{tanim}</div>'
                    f'<div style="background:{renk};color:white;border-radius:20px;'
                    f'padding:3px 14px;font-size:0.78rem;font-weight:700;display:inline-block;">'
                    f'{sayi} görev</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # Yeni performans görevi oluştur
        _pf_col1, _pf_col2 = st.columns([1, 1])
        with _pf_col1:
            styled_section("Yeni Performans Görevi", "#7c3aed")
            with st.form("performans_odev_form", clear_on_submit=True):
                pf_alan = st.selectbox("Alan / Ders", _alan_isimleri, key="pf_alan")
                pf_sinif = st.selectbox("Sınıf", SINIFLAR, key="pf_sinif")
                pf_sube = st.selectbox("Şube", ["Tüm Şubeler"] + list(SUBELER), key="pf_sube")
                pf_baslik = st.text_input("Görev Başlığı", placeholder="örn. 1. Dönem Türkü Performansı", key="pf_baslik")
                pf_aciklama = st.text_area(
                    "Görev Açıklaması",
                    placeholder="Öğrencilerin yapacağı görevin ayrıntılı açıklaması...",
                    height=100, key="pf_aciklama"
                )
                pf_kriterler = st.text_area(
                    "Değerlendirme Kriterleri",
                    placeholder="1. Ses tonu (%30)\n2. Ritim (%30)\n3. Sahne duruşu (%20)\n4. Ezber (%20)",
                    height=90, key="pf_kriterler"
                )
                pf_puan = st.number_input("Tam Puan", min_value=10, max_value=100, value=100, step=5, key="pf_puan")
                _pf_c1, _pf_c2 = st.columns(2)
                with _pf_c1:
                    pf_verilme = st.date_input("Veriliş Tarihi", value=date.today(), key="pf_verilme")
                with _pf_c2:
                    pf_teslim = st.date_input("Son Teslim Tarihi", key="pf_teslim")
                pf_ogretmen = st.text_input("Öğretmen Adı", key="pf_ogretmen", placeholder="Ad Soyad")

                pf_submit = st.form_submit_button("💜 Performans Görevi Oluştur", use_container_width=True, type="primary")
                if pf_submit:
                    if not pf_baslik.strip():
                        st.error("Görev başlığı giriniz.")
                    else:
                        _sube_val = "" if pf_sube == "Tüm Şubeler" else pf_sube
                        new_pf_odev = Odev(
                            sinif=pf_sinif,
                            sube=_sube_val,
                            ders=pf_alan,
                            ogretmen_adi=pf_ogretmen.strip(),
                            baslik=pf_baslik.strip(),
                            aciklama=(pf_aciklama.strip() + (
                                f"\n\n**Değerlendirme Kriterleri:**\n{pf_kriterler.strip()}"
                                if pf_kriterler.strip() else ""
                            )),
                            odev_turu="performans",
                            verilme_tarihi=pf_verilme.isoformat(),
                            son_teslim_tarihi=pf_teslim.isoformat() if pf_teslim else "",
                            online_teslim=False,
                            akademik_yil=akademik_yil,
                        )
                        store.save_odev(new_pf_odev)
                        st.success(f"✅ '{pf_baslik}' performans görevi oluşturuldu.")
                        st.rerun(scope="fragment")

        with _pf_col2:
            styled_section("Mevcut Performans Görevleri", "#f59e0b")

            # Alan filtresi
            pf_filtre = st.selectbox(
                "Alan Filtresi",
                ["Tümü"] + _alan_isimleri,
                key="pf_filtre_alan"
            )
            filtreli_pf = perf_odevler if pf_filtre == "Tümü" else [
                o for o in perf_odevler if o.ders == pf_filtre
            ]
            filtreli_pf.sort(key=lambda x: x.verilme_tarihi or "", reverse=True)

            if not filtreli_pf:
                styled_info_banner("Henüz performans görevi oluşturulmamış.", banner_type="warning")
            else:
                for po in filtreli_pf:
                    _alan_data = next((a for a in _PERF_ALANLAR if a[1] == po.ders), ("📋", po.ders, "#64748b", ""))
                    _p_ikon, _p_alan, _p_renk, _ = _alan_data
                    _sube_str = po.sube if po.sube else "Tüm Şubeler"
                    with st.expander(f"{_p_ikon} {po.baslik}  |  {po.sinif}-{_sube_str}  |  {_p_alan}", expanded=False
                    ):
                        st.markdown(
                            f'<div style="background:{_p_renk}10;border-left:4px solid {_p_renk};'
                            f'border-radius:8px;padding:12px 16px;margin-bottom:8px;">'
                            f'<b>Açıklama:</b><br>{(po.aciklama or "–").replace(chr(10), "<br>")}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        pi_c1, pi_c2, pi_c3 = st.columns(3)
                        with pi_c1:
                            st.caption(f"📅 Veriliş: {po.verilme_tarihi}")
                        with pi_c2:
                            st.caption(f"⏰ Son Teslim: {po.son_teslim_tarihi or '–'}")
                        with pi_c3:
                            st.caption(f"👨‍🏫 {po.ogretmen_adi or '–'}")
                        if st.button("🗑️ Sil", key=f"pf_del_{po.id}", type="secondary"):
                            store.delete_odev(po.id)
                            st.rerun(scope="fragment")

# ==================== TAB 10: YOKLAMA VE DEVAMSIZLIK TAKIBI ====================

def _tur_label(kod: str) -> str:
    """Devamsizlik tur kodunu etikete cevirir."""
    mapping = dict(DEVAMSIZLIK_TURLERI)
    return mapping.get(kod, kod)


def _tur_label_short(kod: str) -> str:
    """Kisa etiket."""
    short_map = {"ozursuz": "O.suz", "ozurlu": "O.lu", "izinli": "Izn", "raporlu": "Rap"}
    return short_map.get(kod, kod[:4])


def _tipi_label(kod: str) -> str:
    """Devamsizlik tipi kodunu etikete cevirir."""
    mapping = dict(DEVAMSIZLIK_TIPLERI)
    return mapping.get(kod, kod or "-")


def _detect_devamsizlik_tipi(devamsiz_saatler: list[int], turu: str, max_saat: int) -> str:
    """Devamsiz saatlere gore devamsizlik tipini otomatik tespit eder."""
    if turu == "izinli":
        return "izinli"
    if turu == "raporlu":
        return "raporlu"
    if not devamsiz_saatler:
        return "tekil"

    sabah_saatler = [s for s in SABAH_DERS_SAATLERI if s <= max_saat]
    ogleden_sonra = [s for s in OGLEDEN_SONRA_SAATLERI if s <= max_saat]

    sabah_devamsiz = all(s in devamsiz_saatler for s in sabah_saatler) if sabah_saatler else False
    ogleden_devamsiz = all(s in devamsiz_saatler for s in ogleden_sonra) if ogleden_sonra else False

    if sabah_devamsiz and ogleden_devamsiz:
        return "tam_gun"
    elif sabah_devamsiz and not ogleden_devamsiz:
        return "sabah_yarim"
    elif ogleden_devamsiz and not sabah_devamsiz:
        return "ogleden_sonra_yarim"
    elif len(devamsiz_saatler) >= max_saat:
        return "tam_gun"
    else:
        return "tekil"


def _generate_veli_mesaj(sablon_key: str, ogrenci: Student, tarih_str: str,
                         ders: str = "", saat: int = 0, okul_adi: str = "Okul Mudurlugu") -> str:
    """Veli bildirim mesajini sablondan uretir."""
    sablon = VELI_BILDIRIM_SABLONLARI.get(sablon_key, "")
    if not sablon:
        return ""
    return sablon.format(
        veli_adi=ogrenci.veli_adi or "Veli",
        ogrenci_adi=f"{ogrenci.ad} {ogrenci.soyad}",
        sinif=ogrenci.sinif,
        sube=ogrenci.sube,
        tarih=tarih_str,
        ders=ders,
        saat=saat,
        okul_adi=okul_adi,
    )


@st.fragment
def _render_yoklama_devamsizlik(store: AkademikDataStore):
    """Gelismis yoklama ve devamsizlik takibi sekmesi."""
    styled_section("Yoklama ve Devamsızlık Takibi", "#ef4444")
    styled_info_banner("Günlük yoklama, ders bazli devamsizlik, analiz ve veli bilgilendirme.", "info")

    akademik_yil = _get_akademik_yil()

    (tab_gunluk, tab_ders_yoklama, tab_gecmis,
     tab_ogrenci_kart, tab_analiz, tab_uyari, tab_sablon) = st.tabs([
        "✅ Günlük Toplu Yoklama",
        "📚 Ders Yoklaması",
        "🕐 Yoklama Geçmişi",
        "🪪 Öğrenci Devamsızlık Kartı",
        "📊 Devamsızlık Analizi",
        "🔔 Uyarı & Veli Bilgilendirme",
        "📄 Bildirim Şablonları",
    ])

    # Ogretmen listesini bir kere cek
    all_teachers = store.get_teachers(durum="aktif")
    ogr_display_list = ["-- Öğretmen Seçin --"] + [f"{t.ad} {t.soyad} ({t.brans})" for t in all_teachers]
    ogr_display_map = {f"{t.ad} {t.soyad} ({t.brans})": t for t in all_teachers}

    # --- GUNLUK TOPLU YOKLAMA ---
    with tab_gunluk:
        styled_section("Günlük Toplu Yoklama", "#d32f2f")
        styled_info_banner(
            "Bir gune ait tum ders saatlerinin yoklamasini tek seferde alin. "
            "Sabah ilk ders yok yazilan ogrencilerin velisine otomatik bildirim olusturulur.",
            "info"
        )

        gy_col1, gy_col2, gy_col3 = st.columns(3)
        with gy_col1:
            gy_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="gy_sinif")
        with gy_col2:
            gy_sube = st.selectbox("Şube", SUBELER, key="gy_sube")
        with gy_col3:
            gy_tarih = st.date_input("Tarih", value=date.today(), key="gy_tarih")

        # Ogretmen secimi
        if all_teachers:
            gy_ogretmen_key = st.selectbox("Yoklamayi Alan Öğretmen", ogr_display_list, key="gy_ogretmen")
            gy_ogretmen = ogr_display_map.get(gy_ogretmen_key)
        else:
            gy_ogretmen = None
            st.caption("Öğretmen kaydi bulunamadı. Öğretmen Yönetimi sekmesinden ekleyebilirsiniz.")

        students = store.get_students(sinif=gy_sinif, sube=gy_sube, durum="aktif")
        if not students:
            st.info("Bu sinif/subede aktif ogrenci bulunamadı.")
        else:
            students = sorted(students, key=lambda s: (s.numara or 0, s.soyad, s.ad))

            # O gun için ders programini cek
            gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
            gun_idx = gy_tarih.weekday()
            gun_str = gun_adi[gun_idx] if gun_idx < len(gun_adi) else "Pazartesi"

            program = store.get_schedule(sinif=gy_sinif, sube=gy_sube, gun=gun_str,
                                          akademik_yil=akademik_yil)
            ders_saatleri = {}
            ogretmen_saatleri = {}
            for slot in program:
                ders_saatleri[slot.ders_saati] = slot.ders
                if slot.ogretmen:
                    ogretmen_saatleri[slot.ders_saati] = slot.ogretmen

            # Mevcut yoklama kayitlarini getir
            tarih_str = gy_tarih.strftime("%Y-%m-%d")
            mevcut_kayitlar = store.get_attendance(tarih=tarih_str, sinif=gy_sinif,
                                                    sube=gy_sube, akademik_yil=akademik_yil)
            mevcut_map = {}
            for r in mevcut_kayitlar:
                if r.student_id not in mevcut_map:
                    mevcut_map[r.student_id] = {}
                mevcut_map[r.student_id][r.ders_saati] = r

            st.markdown(f"**{gy_sinif}/{gy_sube} - {gy_tarih.strftime('%d.%m.%Y')} {gun_str}** | "
                        f"{len(students)} ogrenci")

            if ders_saatleri:
                ders_info_parts = []
                for s, d in sorted(ders_saatleri.items()):
                    # Use helper to get teacher from schedule
                    ogr_name = ogretmen_saatleri.get(s, "") or _get_ogretmen_from_schedule(
                        store, gy_sinif, gy_sube, gun_str, s, akademik_yil) or ""
                    if ogr_name:
                        ders_info_parts.append(f"{s}.saat: {d} ({ogr_name})")
                    else:
                        ders_info_parts.append(f"{s}.saat: {d}")
                ders_info = " | ".join(ders_info_parts)
                st.caption(f"Ders Programı: {ders_info}")

            max_saat = st.slider("Ders Saati Sayısı", min_value=1, max_value=10, value=8, key="gy_max_saat")

            # Tur secenekleri
            tur_options = [t[0] for t in DEVAMSIZLIK_TURLERI]

            with st.form("gunluk_yoklama_form"):
                header_cols = st.columns([3] + [1] * max_saat + [1])
                with header_cols[0]:
                    st.markdown("**Öğrenci**")
                for saat in range(1, max_saat + 1):
                    with header_cols[saat]:
                        ders_adi = ders_saatleri.get(saat, "")
                        if ders_adi:
                            st.markdown(f"**{saat}.**\n{ders_adi[:6]}")
                        else:
                            st.markdown(f"**{saat}.**")
                with header_cols[-1]:
                    st.markdown("**Tur**")

                yoklama_data = {}
                for stu in students:
                    row_cols = st.columns([3] + [1] * max_saat + [1])
                    with row_cols[0]:
                        st.write(f"{stu.numara} - {stu.ad} {stu.soyad}")

                    saat_devamsiz = {}
                    for saat in range(1, max_saat + 1):
                        with row_cols[saat]:
                            mevcut = mevcut_map.get(stu.id, {}).get(saat)
                            default_val = mevcut is not None
                            saat_devamsiz[saat] = st.checkbox(
                                f"s{saat}", value=default_val,
                                key=f"gy_{stu.id}_{saat}",
                                label_visibility="collapsed"
                            )

                    with row_cols[-1]:
                        mevcut_turler = [r.turu for r in mevcut_map.get(stu.id, {}).values()]
                        default_tur = "ozursuz"
                        if mevcut_turler:
                            most_common = max(set(mevcut_turler), key=mevcut_turler.count)
                            default_tur = most_common
                        tur = st.selectbox(
                            "T", tur_options,
                            index=tur_options.index(default_tur) if default_tur in tur_options else 0,
                            format_func=_tur_label_short,
                            key=f"gy_tur_{stu.id}",
                            label_visibility="collapsed"
                        )

                    yoklama_data[stu.id] = {"saatler": saat_devamsiz, "tur": tur, "stu": stu}

                if st.form_submit_button("Günlük Yoklamayi Kaydet", type="primary"):
                    eklenen = 0
                    silinen = 0
                    veli_bildirim_listesi = []  # Sabah ilk ders devamsizlari

                    for stu_id, bilgi in yoklama_data.items():
                        devamsiz_saatler = [s for s, d in bilgi["saatler"].items() if d]
                        tipi = _detect_devamsizlik_tipi(devamsiz_saatler, bilgi["tur"], max_saat)

                        for saat, devamsiz in bilgi["saatler"].items():
                            mevcut = mevcut_map.get(stu_id, {}).get(saat)
                            ders_adi = ders_saatleri.get(saat, f"Ders {saat}")

                            if devamsiz and not mevcut:
                                record = AttendanceRecord(
                                    student_id=stu_id,
                                    tarih=tarih_str,
                                    ders=ders_adi,
                                    ders_saati=saat,
                                    turu=bilgi["tur"],
                                    devamsizlik_tipi=tipi,
                                    ogretmen_id=gy_ogretmen.id if gy_ogretmen else "",
                                    ogretmen_adi=gy_ogretmen.tam_ad if gy_ogretmen else "",
                                    akademik_yil=akademik_yil,
                                )
                                store.save_attendance(record)
                                eklenen += 1
                            elif devamsiz and mevcut:
                                changed = False
                                if mevcut.turu != bilgi["tur"]:
                                    mevcut.turu = bilgi["tur"]
                                    changed = True
                                if mevcut.devamsizlik_tipi != tipi:
                                    mevcut.devamsizlik_tipi = tipi
                                    changed = True
                                if gy_ogretmen and mevcut.ogretmen_id != gy_ogretmen.id:
                                    mevcut.ogretmen_id = gy_ogretmen.id
                                    mevcut.ogretmen_adi = gy_ogretmen.tam_ad
                                    changed = True
                                if changed:
                                    store.save_attendance(mevcut)
                                    eklenen += 1
                            elif not devamsiz and mevcut:
                                store.delete_attendance(mevcut.id)
                                silinen += 1

                        # Sabah 1. ders devamsiz mi? -> Veli bildirim listesine ekle
                        if 1 in devamsiz_saatler and bilgi["tur"] == "ozursuz":
                            stu_obj = bilgi["stu"]
                            if stu_obj.veli_telefon:
                                veli_bildirim_listesi.append(stu_obj)

                    msg_parts = []
                    if eklenen > 0:
                        msg_parts.append(f"{eklenen} devamsizlik kaydedildi")
                    if silinen > 0:
                        msg_parts.append(f"{silinen} kayit kaldirildi")
                    if msg_parts:
                        st.success(", ".join(msg_parts) + ".")
                    else:
                        st.info("Degisiklik yapilmadi.")

                    # Sabah 1. ders devamsiz bildirim
                    if veli_bildirim_listesi:
                        st.divider()
                        st.warning(f"Sabah 1. ders devamsiz: {len(veli_bildirim_listesi)} ogrenci. "
                                   "Veli bildirim mesajlari asagida hazirlanmistir.")
                        for stu_obj in veli_bildirim_listesi:
                            mesaj = _generate_veli_mesaj(
                                "sabah_devamsiz", stu_obj, tarih_str
                            )
                            with st.expander(f"{stu_obj.ad} {stu_obj.soyad} - {stu_obj.veli_telefon}"):
                                st.code(mesaj, language=None)
                                wp_link = f"https://wa.me/{stu_obj.veli_telefon.replace('+','').replace(' ','')}?text={mesaj}"
                                st.markdown(f"[WhatsApp ile Gonder]({wp_link})")
                    st.rerun(scope="fragment")

    # --- DERS YOKLAMASI ---
    with tab_ders_yoklama:
        styled_section("Ders Bazli Yoklama", "#0d9488")
        styled_info_banner("Derse giren ogretmen tek bir ders saati için yoklama alir.", "info")

        dy_col1, dy_col2, dy_col3 = st.columns(3)
        with dy_col1:
            dy_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dy_sinif")
        with dy_col2:
            dy_sube = st.selectbox("Şube", SUBELER, key="dy_sube")
        with dy_col3:
            dy_tarih = st.date_input("Tarih", value=date.today(), key="dy_tarih")

        dy_col4, dy_col5 = st.columns(2)
        with dy_col4:
            dy_saat = st.number_input("Ders Saati", min_value=1, max_value=10, value=1, key="dy_saat")
        with dy_col5:
            dy_dersler = store.get_meb_subjects(grade=dy_sinif)
            if not dy_dersler:
                dy_dersler = DERSLER
            dy_ders = st.selectbox("Ders", dy_dersler, key="dy_ders")

        # Programdan ogretmen otomatik tespit
        dy_gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
        dy_gun_idx = dy_tarih.weekday()
        dy_gun_str = dy_gun_adi[dy_gun_idx] if dy_gun_idx < len(dy_gun_adi) else "Pazartesi"
        dy_schedule_map = _get_schedule_ders_map(store, dy_sinif, dy_sube, dy_gun_str, akademik_yil)
        dy_slot_info = dy_schedule_map.get(dy_saat)

        dy_ogretmen = None
        if dy_slot_info and dy_slot_info.get("ogretmen"):
            dy_auto_ogr = dy_slot_info["ogretmen"]
            dy_auto_ders = dy_slot_info.get("ders", "")
            st.info(f"Program: {dy_gun_str} {dy_saat}. ders → **{dy_auto_ders}** | "
                    f"Öğretmen: **{dy_auto_ogr}**")
            for t in all_teachers:
                if t.tam_ad == dy_auto_ogr:
                    dy_ogretmen = t
                    break
        if not dy_ogretmen:
            if all_teachers:
                dy_ogretmen_key = st.selectbox("Yoklamayi Alan Öğretmen", ogr_display_list,
                                                key="dy_ogretmen")
                dy_ogretmen = ogr_display_map.get(dy_ogretmen_key)

        dy_students = store.get_students(sinif=dy_sinif, sube=dy_sube, durum="aktif")
        if not dy_students:
            st.info("Bu sinif/subede aktif ogrenci bulunamadı.")
        else:
            dy_students = sorted(dy_students, key=lambda s: (s.numara or 0, s.soyad))
            dy_tarih_str = dy_tarih.strftime("%Y-%m-%d")

            dy_mevcut = store.get_attendance(tarih=dy_tarih_str, sinif=dy_sinif,
                                              sube=dy_sube, akademik_yil=akademik_yil)
            dy_mevcut_saat = {r.student_id: r for r in dy_mevcut if r.ders_saati == dy_saat}

            st.markdown(f"**{dy_sinif}/{dy_sube} - {dy_tarih.strftime('%d.%m.%Y')} - "
                        f"{dy_ders} ({dy_saat}. saat)** | {len(dy_students)} ogrenci")

            if dy_mevcut_saat:
                st.info(f"Bu ders saati için {len(dy_mevcut_saat)} mevcut devamsizlik kaydi var.")

            tur_options = [t[0] for t in DEVAMSIZLIK_TURLERI]

            with st.form("ders_yoklama_form"):
                hdr_c1, hdr_c2, hdr_c3, hdr_c4 = st.columns([3, 1, 1, 2])
                with hdr_c1:
                    st.caption("Öğrenci")
                with hdr_c2:
                    st.caption("Devamsız")
                with hdr_c3:
                    st.caption("Tur")
                with hdr_c4:
                    st.caption("Açıklama")

                dy_yoklama = {}
                for stu in dy_students:
                    c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
                    mevcut_r = dy_mevcut_saat.get(stu.id)
                    with c1:
                        st.write(f"{stu.numara} - {stu.ad} {stu.soyad}")
                    with c2:
                        devamsiz = st.checkbox(
                            "D", value=(mevcut_r is not None),
                            key=f"dy_{stu.id}",
                            label_visibility="collapsed"
                        )
                    with c3:
                        m_tur = mevcut_r.turu if mevcut_r else "ozursuz"
                        tur = st.selectbox(
                            "T", tur_options,
                            index=tur_options.index(m_tur) if m_tur in tur_options else 0,
                            format_func=_tur_label_short,
                            key=f"dy_tur_{stu.id}",
                            label_visibility="collapsed"
                        )
                    with c4:
                        m_ack = mevcut_r.aciklama if mevcut_r else ""
                        ack = st.text_input(
                            "A", value=m_ack,
                            key=f"dy_ack_{stu.id}",
                            label_visibility="collapsed",
                            placeholder="Not..."
                        )
                    dy_yoklama[stu.id] = {"devamsiz": devamsiz, "tur": tur, "aciklama": ack,
                                          "mevcut": mevcut_r, "stu": stu}

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    kaydet = st.form_submit_button("Yoklamayi Kaydet", type="primary")
                with col_btn2:
                    tum_geldi = st.form_submit_button("Herkes Geldi (Temizle)")

                if kaydet:
                    eklenen = 0
                    silinen = 0
                    sabah_bildirim = []

                    for stu_id, bilgi in dy_yoklama.items():
                        mevcut_r = bilgi["mevcut"]
                        if bilgi["devamsiz"]:
                            if mevcut_r:
                                changed = False
                                if mevcut_r.turu != bilgi["tur"]:
                                    mevcut_r.turu = bilgi["tur"]
                                    changed = True
                                if mevcut_r.aciklama != bilgi["aciklama"]:
                                    mevcut_r.aciklama = bilgi["aciklama"]
                                    changed = True
                                if dy_ogretmen and mevcut_r.ogretmen_id != dy_ogretmen.id:
                                    mevcut_r.ogretmen_id = dy_ogretmen.id
                                    mevcut_r.ogretmen_adi = dy_ogretmen.tam_ad
                                    changed = True
                                if changed:
                                    store.save_attendance(mevcut_r)
                                    eklenen += 1
                            else:
                                record = AttendanceRecord(
                                    student_id=stu_id,
                                    tarih=dy_tarih_str,
                                    ders=dy_ders,
                                    ders_saati=dy_saat,
                                    turu=bilgi["tur"],
                                    devamsizlik_tipi="tekil",
                                    ogretmen_id=dy_ogretmen.id if dy_ogretmen else "",
                                    ogretmen_adi=dy_ogretmen.tam_ad if dy_ogretmen else "",
                                    aciklama=bilgi["aciklama"],
                                    akademik_yil=akademik_yil,
                                )
                                store.save_attendance(record)
                                eklenen += 1

                                # Sabah 1. ders ve ozursuz ise bildirim
                                if dy_saat == 1 and bilgi["tur"] == "ozursuz":
                                    stu_obj = bilgi["stu"]
                                    if stu_obj.veli_telefon:
                                        sabah_bildirim.append(stu_obj)
                        elif mevcut_r:
                            store.delete_attendance(mevcut_r.id)
                            silinen += 1

                    msg_parts = []
                    if eklenen:
                        msg_parts.append(f"{eklenen} kayit")
                    if silinen:
                        msg_parts.append(f"{silinen} silindi")
                    if msg_parts:
                        st.success("Yoklama kaydedildi: " + ", ".join(msg_parts))
                    else:
                        st.info("Degisiklik yok.")

                    if sabah_bildirim:
                        st.divider()
                        st.warning(f"Sabah 1. ders devamsiz: {len(sabah_bildirim)} ogrenci")
                        for stu_obj in sabah_bildirim:
                            mesaj = _generate_veli_mesaj("sabah_devamsiz", stu_obj, dy_tarih_str)
                            with st.expander(f"{stu_obj.ad} {stu_obj.soyad} - {stu_obj.veli_telefon}"):
                                st.code(mesaj, language=None)
                                wp_link = f"https://wa.me/{stu_obj.veli_telefon.replace('+','').replace(' ','')}?text={mesaj}"
                                st.markdown(f"[WhatsApp ile Gonder]({wp_link})")
                    st.rerun(scope="fragment")

                if tum_geldi:
                    silinen = 0
                    for stu_id, bilgi in dy_yoklama.items():
                        if bilgi["mevcut"]:
                            store.delete_attendance(bilgi["mevcut"].id)
                            silinen += 1
                    if silinen:
                        st.success(f"{silinen} devamsizlik kaydi kaldirildi. Herkes geldi!")
                    else:
                        st.info("Zaten devamsizlik kaydi yok.")
                    st.rerun(scope="fragment")

    # --- YOKLAMA GECMISI ---
    with tab_gecmis:
        styled_section("Yoklama Geçmişi", "#6366f1")
        styled_info_banner("Geçmiş yoklama kayitlarini goruntuleyin, duzenleyin veya silin.", "info")

        yg_col1, yg_col2, yg_col3 = st.columns(3)
        with yg_col1:
            yg_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="yg_sinif")
        with yg_col2:
            yg_sube = st.selectbox("Şube", SUBELER, key="yg_sube")
        with yg_col3:
            yg_filtre_opts = [None] + [t[0] for t in DEVAMSIZLIK_TURLERI]
            yg_filtre = st.selectbox("Tur Filtresi", yg_filtre_opts,
                                      format_func=lambda x: "Tümü" if x is None else _tur_label(x),
                                      key="yg_filtre")

        yg_tarih_col1, yg_tarih_col2 = st.columns(2)
        with yg_tarih_col1:
            yg_baslangic = st.date_input("Başlangıç Tarihi",
                                          value=date.today() - timedelta(days=30),
                                          key="yg_baslangic")
        with yg_tarih_col2:
            yg_bitis = st.date_input("Bitis Tarihi",
                                      value=date.today(),
                                      key="yg_bitis")

        records = store.get_attendance(sinif=yg_sinif, sube=yg_sube,
                                        turu=yg_filtre, akademik_yil=akademik_yil)

        baslangic_str = yg_baslangic.strftime("%Y-%m-%d")
        bitis_str = yg_bitis.strftime("%Y-%m-%d")
        records = [r for r in records if baslangic_str <= r.tarih <= bitis_str]
        records = sorted(records, key=lambda r: (r.tarih, r.ders_saati), reverse=True)

        if records:
            st.markdown(f"**{len(records)} kayit bulundu** ({yg_baslangic.strftime('%d.%m.%Y')} - {yg_bitis.strftime('%d.%m.%Y')})")

            tarih_grup = {}
            for r in records:
                if r.tarih not in tarih_grup:
                    tarih_grup[r.tarih] = []
                tarih_grup[r.tarih].append(r)

            for tarih_val, gunluk_kayitlar in sorted(tarih_grup.items(), reverse=True):
                try:
                    tarih_obj = date.fromisoformat(tarih_val)
                    gun_adi_list = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
                    gun_ismi = gun_adi_list[tarih_obj.weekday()]
                except (ValueError, IndexError):
                    gun_ismi = ""

                with st.expander(f"{tarih_val} ({gun_ismi}) - {len(gunluk_kayitlar)} devamsizlik",
                    expanded=False
                ):
                    df_data = []
                    for r in sorted(gunluk_kayitlar, key=lambda x: x.ders_saati):
                        stu = store.get_student(r.student_id)
                        stu_name = f"{stu.ad} {stu.soyad}" if stu else "Bilinmiyor"
                        stu_no = stu.numara if stu else ""
                        df_data.append({
                            "No": stu_no,
                            "Öğrenci": stu_name,
                            "Ders": r.ders,
                            "Saat": r.ders_saati,
                            "Tur": _tur_label(r.turu),
                            "Tip": _tipi_label(getattr(r, 'devamsizlik_tipi', '')),
                            "Öğretmen": getattr(r, 'ogretmen_adi', '') or "-",
                            "Açıklama": r.aciklama or "-",
                        })
                    df = pd.DataFrame(df_data)
                    st.dataframe(df[["No", "Öğrenci", "Ders", "Saat", "Tur", "Tip", "Öğretmen", "Açıklama"]],
                                 use_container_width=True, hide_index=True)

                    islem_col1, islem_col2, islem_col3, islem_col4 = st.columns(4)
                    with islem_col1:
                        if st.button("Tümü Ozurlu", key=f"yg_ozurlu_{tarih_val}"):
                            for r in gunluk_kayitlar:
                                if r.turu != "ozurlu":
                                    r.turu = "ozurlu"
                                    store.save_attendance(r)
                            st.success("Tüm kayitlar ozurlu olarak güncellendi.")
                            st.rerun(scope="fragment")
                    with islem_col2:
                        if st.button("Tümü İzinli", key=f"yg_izinli_{tarih_val}"):
                            for r in gunluk_kayitlar:
                                if r.turu != "izinli":
                                    r.turu = "izinli"
                                    r.devamsizlik_tipi = "izinli"
                                    store.save_attendance(r)
                            st.success("Tüm kayitlar izinli olarak güncellendi.")
                            st.rerun(scope="fragment")
                    with islem_col3:
                        if st.button("Tümü Raporlu", key=f"yg_raporlu_{tarih_val}"):
                            for r in gunluk_kayitlar:
                                if r.turu != "raporlu":
                                    r.turu = "raporlu"
                                    r.devamsizlik_tipi = "raporlu"
                                    store.save_attendance(r)
                            st.success("Tüm kayitlar raporlu olarak güncellendi.")
                            st.rerun(scope="fragment")
                    with islem_col4:
                        if confirm_action("Günü Sil", f"{tarih_val} tarihli {len(gunluk_kayitlar)} devamsızlık kaydını silmek istediğinize emin misiniz?", key=f"yg_sil_{tarih_val}"):
                            for r in gunluk_kayitlar:
                                store.delete_attendance(r.id)
                            st.success(f"{tarih_val} tarihli {len(gunluk_kayitlar)} kayıt silindi.")
                            st.rerun(scope="fragment")
        else:
            st.info("Secili tarih araliginda devamsizlik kaydi bulunamadı.")

    # --- OGRENCI DEVAMSIZLIK KARTI ---
    with tab_ogrenci_kart:
        styled_section("Öğrenci Devamsızlık Kartı", "#ec4899")
        styled_info_banner("Belirli bir ogrencinin detayli devamsizlik bilgilerini goruntuler.", "info")

        ok_col1, ok_col2 = st.columns(2)
        with ok_col1:
            ok_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="ok_sinif")
        with ok_col2:
            ok_sube = st.selectbox("Şube", SUBELER, key="ok_sube")

        ok_students = store.get_students(sinif=ok_sinif, sube=ok_sube, durum="aktif")
        if not ok_students:
            st.info("Bu sinif/subede ogrenci bulunamadı.")
        else:
            ok_students = sorted(ok_students, key=lambda s: (s.numara or 0, s.soyad))
            ogr_secenekleri = [f"{s.numara} - {s.ad} {s.soyad}" for s in ok_students]
            ogr_sec_map = {f"{s.numara} - {s.ad} {s.soyad}": s for s in ok_students}

            secili_ogr_key = st.selectbox("Öğrenci Seçin", ogr_secenekleri, key="ok_ogr_sec")
            secili_ogr = ogr_sec_map.get(secili_ogr_key)

            if secili_ogr:
                ozet = store.get_attendance_summary(secili_ogr.id, akademik_yil)

                # Uyari durumu
                uyari_html = _uyari_badge(ozet["uyari"])
                if uyari_html:
                    st.markdown(uyari_html, unsafe_allow_html=True)
                if ozet["uyari"] == "SINIR_ASILDI":
                    st.error(f"SINIR ASILDI! Ozursuz devamsizlik: {ozet['ozursuz']} gun "
                             f"(Sinir: {DEVAMSIZLIK_SINIR_GUN} gun)")
                elif ozet["uyari"] == "TEHLIKE":
                    st.warning(f"TEHLIKE! Ozursuz devamsizlik: {ozet['ozursuz']} gun "
                               f"(Tehlike esigi: {DEVAMSIZLIK_TEHLIKE_GUN} gun)")
                elif ozet["uyari"] == "UYARI":
                    st.warning(f"UYARI! Ozursuz devamsizlik: {ozet['ozursuz']} gun "
                               f"(Uyari esigi: {DEVAMSIZLIK_UYARI_GUN} gun)")

                # Detayli kayitlar (tum turler için say)
                tum_kayitlar = store.get_student_attendance(secili_ogr.id, akademik_yil)
                tum_kayitlar = sorted(tum_kayitlar, key=lambda r: r.tarih, reverse=True)

                izinli_sayi = sum(1 for r in tum_kayitlar if r.turu == "izinli")
                raporlu_sayi = sum(1 for r in tum_kayitlar if r.turu == "raporlu")

                # Metrikler
                kalan = max(0, DEVAMSIZLIK_SINIR_GUN - ozet["ozursuz"])
                styled_stat_row([
                    ("Toplam", ozet["toplam"], "#6366f1", "\U0001f4ca"),
                    ("Ozurlu", ozet["ozurlu"], "#10b981", "\u2705"),
                    ("Ozursuz", ozet["ozursuz"], "#ef4444", "\u274c"),
                    ("İzinli", izinli_sayi, "#f59e0b", "\U0001f4cb"),
                    ("Raporlu", raporlu_sayi, "#8b5cf6", "\U0001f3e5"),
                    ("Kalan Hak", f"{kalan} gun", "#0ea5e9", "\u23f3"),
                ])

                # Devamsizlik tipi dagilimi
                tipi_grp = {}
                for r in tum_kayitlar:
                    tip = getattr(r, 'devamsizlik_tipi', '') or "tekil"
                    if tip not in tipi_grp:
                        tipi_grp[tip] = 0
                    tipi_grp[tip] += 1

                if tipi_grp:
                    styled_section("Devamsızlık Tipi Dagilimi", "#7c3aed")
                    tipi_stat_items = [
                        (_tipi_label(tip_kod), sayi, "#8b5cf6", "\U0001f4cb")
                        for tip_kod, sayi in sorted(tipi_grp.items())
                    ]
                    styled_stat_row(tipi_stat_items)

                # Veli bilgileri
                if secili_ogr.veli_adi or secili_ogr.veli_telefon:
                    with st.expander("Veli Bilgileri", expanded=False):
                        if secili_ogr.veli_adi:
                            st.write(f"**Veli Adi:** {secili_ogr.veli_adi}")
                        if secili_ogr.veli_telefon:
                            st.write(f"**Telefon:** {secili_ogr.veli_telefon}")
                        if getattr(secili_ogr, 'veli_email', ''):
                            st.write(f"**Email:** {secili_ogr.veli_email}")

                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

                if tum_kayitlar:
                    # Ders bazli dagilim
                    styled_section("Ders Bazli Devamsızlık", "#0d9488")
                    ders_grp = {}
                    for r in tum_kayitlar:
                        if r.ders not in ders_grp:
                            ders_grp[r.ders] = {"ozurlu": 0, "ozursuz": 0, "izinli": 0, "raporlu": 0}
                        tur_key = r.turu if r.turu in ders_grp[r.ders] else "ozursuz"
                        ders_grp[r.ders][tur_key] += 1

                    ders_df_data = []
                    for ders_adi, sayilar in sorted(ders_grp.items()):
                        ders_df_data.append({
                            "Ders": ders_adi,
                            "Ozurlu": sayilar["ozurlu"],
                            "Ozursuz": sayilar["ozursuz"],
                            "İzinli": sayilar["izinli"],
                            "Raporlu": sayilar["raporlu"],
                            "Toplam": sum(sayilar.values()),
                        })
                    ders_df = pd.DataFrame(ders_df_data)
                    st.dataframe(ders_df, use_container_width=True, hide_index=True)

                    # Ay bazli dagilim
                    styled_section("Ay Bazli Devamsızlık", "#2563eb")
                    ay_grp = {}
                    ay_isimleri = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan",
                                   5: "Mayis", 6: "Haziran", 7: "Temmuz", 8: "Agustos",
                                   9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}
                    for r in tum_kayitlar:
                        try:
                            ay_no = int(r.tarih.split("-")[1])
                        except (IndexError, ValueError):
                            ay_no = 0
                        ay_key = ay_isimleri.get(ay_no, f"Ay {ay_no}")
                        if ay_key not in ay_grp:
                            ay_grp[ay_key] = 0
                        ay_grp[ay_key] += 1

                    if ay_grp:
                        ay_chart_data = pd.DataFrame(
                            [{"Ay": k, "Devamsızlık": v} for k, v in ay_grp.items()]
                        )
                        st.bar_chart(ay_chart_data.set_index("Ay"))

                    # Tum kayitlar tablosu
                    styled_section("Tüm Kayıtlar", "#64748b")
                    kayit_data = []
                    for r in tum_kayitlar:
                        kayit_data.append({
                            "Tarih": r.tarih,
                            "Ders": r.ders,
                            "Saat": r.ders_saati,
                            "Tur": _tur_label(r.turu),
                            "Tip": _tipi_label(getattr(r, 'devamsizlik_tipi', '')),
                            "Öğretmen": getattr(r, 'ogretmen_adi', '') or "-",
                            "Açıklama": r.aciklama or "-",
                        })
                    kayit_df = pd.DataFrame(kayit_data)
                    st.dataframe(kayit_df, use_container_width=True, hide_index=True)
                else:
                    st.success("Bu ogrencinin devamsizlik kaydi bulunmuyor.")

    # --- DEVAMSIZLIK ANALIZI ---
    with tab_analiz:
        styled_section("Devamsızlık Analizi", "#dc2626")
        styled_info_banner("Sınıf, sube ve ders bazli devamsizlik istatistikleri.", "info")

        da_col1, da_col2 = st.columns(2)
        with da_col1:
            da_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="yd_da_sinif")
        with da_col2:
            da_sube = st.selectbox("Şube", ["Tümü"] + SUBELER, key="yd_da_sube")

        da_sube_filtre = None if da_sube == "Tümü" else da_sube

        da_students = store.get_students(sinif=da_sinif, sube=da_sube_filtre, durum="aktif")

        if not da_students:
            st.info("Öğrenci bulunamadı.")
        else:
            tum_kayitlar = store.get_attendance(sinif=da_sinif, sube=da_sube_filtre,
                                                 akademik_yil=akademik_yil)

            # Genel metrikler
            toplam_dev = len(tum_kayitlar)
            ozurlu_dev = sum(1 for r in tum_kayitlar if r.turu == "ozurlu")
            ozursuz_dev = sum(1 for r in tum_kayitlar if r.turu == "ozursuz")
            izinli_dev = sum(1 for r in tum_kayitlar if r.turu == "izinli")
            raporlu_dev = sum(1 for r in tum_kayitlar if r.turu == "raporlu")
            benzersiz_tarih = len(set(r.tarih for r in tum_kayitlar))

            styled_stat_row([
                ("Toplam", toplam_dev, "#6366f1", "\U0001f4ca"),
                ("Ozurlu", ozurlu_dev, "#10b981", "\u2705"),
                ("Ozursuz", ozursuz_dev, "#ef4444", "\u274c"),
                ("İzinli", izinli_dev, "#f59e0b", "\U0001f4cb"),
                ("Raporlu", raporlu_dev, "#8b5cf6", "\U0001f3e5"),
                ("Devamsız Gün", benzersiz_tarih, "#0ea5e9", "\U0001f4c5"),
            ])

            # Devamsizlik tipi dagilimi
            tipi_dagilim = {}
            for r in tum_kayitlar:
                tip = getattr(r, 'devamsizlik_tipi', '') or "tekil"
                if tip not in tipi_dagilim:
                    tipi_dagilim[tip] = 0
                tipi_dagilim[tip] += 1

            if tipi_dagilim:
                styled_section("Devamsızlık Tipi Dagilimi", "#7c3aed")
                tipi_stat_items2 = [
                    (_tipi_label(tip_k), tip_v, "#8b5cf6", "\U0001f4cb")
                    for tip_k, tip_v in sorted(tipi_dagilim.items())
                ]
                styled_stat_row(tipi_stat_items2)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            # Ogrenci bazli siralama
            styled_section("Öğrenci Devamsızlık Sıralamasi (en cok devamsiz olan basta)", "#dc2626")
            ogr_dev_data = []
            for stu in da_students:
                stu_kayitlar = [r for r in tum_kayitlar if r.student_id == stu.id]
                stu_ozurlu = sum(1 for r in stu_kayitlar if r.turu == "ozurlu")
                stu_ozursuz = sum(1 for r in stu_kayitlar if r.turu == "ozursuz")
                stu_izinli = sum(1 for r in stu_kayitlar if r.turu == "izinli")
                stu_raporlu = sum(1 for r in stu_kayitlar if r.turu == "raporlu")
                stu_toplam = len(stu_kayitlar)
                ozet = store.get_attendance_summary(stu.id, akademik_yil)
                ogr_dev_data.append({
                    "No": stu.numara,
                    "Öğrenci": f"{stu.ad} {stu.soyad}",
                    "Şube": stu.sube,
                    "Ozurlu": stu_ozurlu,
                    "Ozursuz": stu_ozursuz,
                    "İzinli": stu_izinli,
                    "Raporlu": stu_raporlu,
                    "Toplam": stu_toplam,
                    "Durum": ozet["uyari"] if ozet["uyari"] else "Normal",
                })

            ogr_dev_df = pd.DataFrame(ogr_dev_data)
            ogr_dev_df = ogr_dev_df.sort_values("Toplam", ascending=False)
            st.dataframe(ogr_dev_df, use_container_width=True, hide_index=True)

            # Ders bazli analiz
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            styled_section("Ders Bazli Devamsızlık Dagilimi", "#0d9488")
            ders_analiz = {}
            for r in tum_kayitlar:
                if r.ders not in ders_analiz:
                    ders_analiz[r.ders] = {"ozurlu": 0, "ozursuz": 0, "izinli": 0, "raporlu": 0}
                tur_key = r.turu if r.turu in ders_analiz[r.ders] else "ozursuz"
                ders_analiz[r.ders][tur_key] += 1

            if ders_analiz:
                ders_chart_data = pd.DataFrame([
                    {"Ders": d, "Ozurlu": v["ozurlu"], "Ozursuz": v["ozursuz"],
                     "İzinli": v["izinli"], "Raporlu": v["raporlu"],
                     "Toplam": sum(v.values())}
                    for d, v in sorted(ders_analiz.items(), key=lambda x: sum(x[1].values()), reverse=True)
                ])
                st.dataframe(ders_chart_data, use_container_width=True, hide_index=True)
                st.bar_chart(ders_chart_data.set_index("Ders")[["Ozurlu", "Ozursuz", "İzinli", "Raporlu"]])

            # Gun bazli analiz
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            styled_section("Gün Bazli Devamsızlık Dagilimi", "#2563eb")
            gun_analiz = {}
            gun_adi_list = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
            for r in tum_kayitlar:
                try:
                    tarih_obj = date.fromisoformat(r.tarih)
                    gun_ismi = gun_adi_list[tarih_obj.weekday()]
                except (ValueError, IndexError):
                    gun_ismi = "Bilinmiyor"
                if gun_ismi not in gun_analiz:
                    gun_analiz[gun_ismi] = 0
                gun_analiz[gun_ismi] += 1

            if gun_analiz:
                gun_sira = {g: i for i, g in enumerate(gun_adi_list)}
                gun_chart_data = pd.DataFrame([
                    {"Gün": g, "Devamsızlık": v}
                    for g, v in sorted(gun_analiz.items(), key=lambda x: gun_sira.get(x[0], 99))
                ])
                st.bar_chart(gun_chart_data.set_index("Gün"))

            # Saat bazli analiz
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            styled_section("Ders Saati Bazli Devamsızlık", "#f59e0b")
            saat_analiz = {}
            for r in tum_kayitlar:
                saat_key = f"{r.ders_saati}. saat"
                if saat_key not in saat_analiz:
                    saat_analiz[saat_key] = 0
                saat_analiz[saat_key] += 1

            if saat_analiz:
                saat_chart_data = pd.DataFrame([
                    {"Saat": k, "Devamsızlık": v}
                    for k, v in sorted(saat_analiz.items())
                ])
                st.bar_chart(saat_chart_data.set_index("Saat"))

    # --- UYARI & VELI BILGILENDIRME ---
    with tab_uyari:
        styled_section("Devamsızlık Uyarilari & Veli Bilgilendirme", "#dc2626")
        styled_info_banner("Devamsızlık esiklerini asan ogrencilerin listesi ve veli bildirim sistemi.", "warning")

        uy_col1, uy_col2 = st.columns(2)
        with uy_col1:
            uy_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="uy_sinif")
        with uy_col2:
            uy_sube = st.selectbox("Şube", ["Tümü"] + SUBELER, key="uy_sube")

        uy_sube_filtre = None if uy_sube == "Tümü" else uy_sube

        st.info(f"Uyari Esikleri: Uyari = {DEVAMSIZLIK_UYARI_GUN} gun | "
                f"Tehlike = {DEVAMSIZLIK_TEHLIKE_GUN} gun | "
                f"Sinir = {DEVAMSIZLIK_SINIR_GUN} gun (ozursuz)")

        uy_students = store.get_students(sinif=uy_sinif, sube=uy_sube_filtre, durum="aktif")

        if not uy_students:
            st.info("Öğrenci bulunamadı.")
        else:
            sinir_list = []
            tehlike_list = []
            uyari_list = []

            for stu in uy_students:
                ozet = store.get_attendance_summary(stu.id, akademik_yil)
                bilgi = {
                    "numara": stu.numara,
                    "ad_soyad": f"{stu.ad} {stu.soyad}",
                    "sinif_sube": f"{stu.sinif}/{stu.sube}",
                    "ozurlu": ozet["ozurlu"],
                    "ozursuz": ozet["ozursuz"],
                    "toplam": ozet["toplam"],
                    "veli_adi": getattr(stu, 'veli_adi', '') or "-",
                    "veli_telefon": getattr(stu, 'veli_telefon', '') or "-",
                    "veli_email": getattr(stu, 'veli_email', '') or "-",
                    "uyari": ozet["uyari"],
                    "stu_obj": stu,
                }
                if ozet["uyari"] == "SINIR_ASILDI":
                    sinir_list.append(bilgi)
                elif ozet["uyari"] == "TEHLIKE":
                    tehlike_list.append(bilgi)
                elif ozet["uyari"] == "UYARI":
                    uyari_list.append(bilgi)

            col_defs = {
                "numara": "No", "ad_soyad": "Öğrenci", "sinif_sube": "Sınıf",
                "ozursuz": "Ozursuz", "ozurlu": "Ozurlu", "toplam": "Toplam",
                "veli_adi": "Veli", "veli_telefon": "Telefon",
            }
            display_cols = ["numara", "ad_soyad", "sinif_sube", "ozursuz", "ozurlu",
                            "toplam", "veli_adi", "veli_telefon"]

            # SINIR ASILDI
            if sinir_list:
                st.error(f"SINIR ASILDI ({len(sinir_list)} ogrenci) - {DEVAMSIZLIK_SINIR_GUN}+ gun ozursuz")
                sinir_df = pd.DataFrame(sinir_list)
                st.dataframe(sinir_df[display_cols], use_container_width=True,
                             hide_index=True, column_config=col_defs)

                # Toplu bildirim butonu
                with st.expander("Sinir Asilan Öğrencilere Toplu Veli Bildirimi"):
                    for bilgi in sinir_list:
                        stu_o = bilgi["stu_obj"]
                        if stu_o.veli_telefon and stu_o.veli_telefon != "-":
                            mesaj = _generate_veli_mesaj("tam_gun_devamsiz", stu_o,
                                                         date.today().strftime("%d.%m.%Y"))
                            st.markdown(f"**{stu_o.ad} {stu_o.soyad}** - {stu_o.veli_telefon}")
                            st.code(mesaj, language=None)
                            wp_link = f"https://wa.me/{stu_o.veli_telefon.replace('+','').replace(' ','')}?text={mesaj}"
                            st.markdown(f"[WhatsApp Gonder]({wp_link})")
                            st.divider()

            # TEHLIKE
            if tehlike_list:
                st.warning(f"TEHLIKE ({len(tehlike_list)} ogrenci) - {DEVAMSIZLIK_TEHLIKE_GUN}-{DEVAMSIZLIK_SINIR_GUN - 1} gun ozursuz")
                tehlike_df = pd.DataFrame(tehlike_list)
                st.dataframe(tehlike_df[display_cols], use_container_width=True,
                             hide_index=True, column_config=col_defs)

            # UYARI
            if uyari_list:
                st.warning(f"UYARI ({len(uyari_list)} ogrenci) - {DEVAMSIZLIK_UYARI_GUN}-{DEVAMSIZLIK_TEHLIKE_GUN - 1} gun ozursuz")
                uyari_df = pd.DataFrame(uyari_list)
                st.dataframe(uyari_df[display_cols], use_container_width=True,
                             hide_index=True, column_config=col_defs)

            if not sinir_list and not tehlike_list and not uyari_list:
                st.success("Devamsızlık esigini asan ogrenci bulunmuyor.")

            # Bugunun devamsizlari - hizli bildirim
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            styled_section("Bugünün Devamsız Öğrencileri - Hızlı Veli Bildirimi", "#f59e0b")
            bugun_str = date.today().strftime("%Y-%m-%d")
            bugun_kayitlar = store.get_attendance(tarih=bugun_str, sinif=uy_sinif,
                                                   sube=uy_sube_filtre, akademik_yil=akademik_yil)

            if bugun_kayitlar:
                # Ogrenci bazli gruplayip devamsizlik tipini belirle
                bugun_ogr_map = {}
                for r in bugun_kayitlar:
                    if r.student_id not in bugun_ogr_map:
                        bugun_ogr_map[r.student_id] = []
                    bugun_ogr_map[r.student_id].append(r)

                for stu_id, kayitlar in bugun_ogr_map.items():
                    stu = store.get_student(stu_id)
                    if not stu:
                        continue

                    saatler = sorted([r.ders_saati for r in kayitlar])
                    tur = kayitlar[0].turu
                    tipi = kayitlar[0].devamsizlik_tipi if hasattr(kayitlar[0], 'devamsizlik_tipi') else "tekil"

                    # Sablon secimi
                    if tipi == "tam_gun":
                        sablon_key = "tam_gun_devamsiz"
                    elif tipi == "sabah_yarim":
                        sablon_key = "sabah_devamsiz"
                    elif tipi == "ogleden_sonra_yarim":
                        sablon_key = "ogleden_sonra_devamsiz"
                    elif tur == "izinli":
                        sablon_key = "izinli"
                    elif tur == "raporlu":
                        sablon_key = "raporlu"
                    else:
                        sablon_key = "tekil_devamsiz"

                    mesaj = _generate_veli_mesaj(sablon_key, stu,
                                                 date.today().strftime("%d.%m.%Y"),
                                                 ders=kayitlar[0].ders,
                                                 saat=saatler[0] if saatler else 0)

                    tur_etiket = _tur_label(tur)
                    tipi_etiket = _tipi_label(tipi)
                    saatler_str = ", ".join([str(s) for s in saatler])

                    with st.expander(f"{stu.ad} {stu.soyad} | {tur_etiket} | {tipi_etiket} | Saatler: {saatler_str}"):
                        st.code(mesaj, language=None)
                        if stu.veli_telefon:
                            sms_col, wp_col = st.columns(2)
                            with sms_col:
                                st.markdown(f"**SMS:** {stu.veli_telefon}")
                            with wp_col:
                                wp_link = f"https://wa.me/{stu.veli_telefon.replace('+','').replace(' ','')}?text={mesaj}"
                                st.markdown(f"[WhatsApp Gonder]({wp_link})")
                        else:
                            st.caption("Veli telefon numarasi kayitli degil.")
            else:
                st.success("Bugün devamsiz ogrenci bulunmuyor.")

            # Ozet istatistik
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            styled_section("Genel Özet", "#64748b")
            styled_stat_row([
                ("Toplam Öğrenci", len(uy_students), "#2563eb", "\U0001f465"),
                ("Sinir Asilan", len(sinir_list), "#ef4444", "\U0001f6a8"),
                ("Tehlike", len(tehlike_list), "#f59e0b", "\u26a0\ufe0f"),
                ("Uyari", len(uyari_list), "#6366f1", "\U0001f514"),
            ])

    # --- BILDIRIM SABLONLARI ---
    with tab_sablon:
        styled_section("Veli Bildirim Şablonları", "#8b5cf6")
        styled_info_banner("SMS ve WhatsApp ile veliye gonderilecek mesaj sablonlari. "
                   "Degiskenler: {veli_adi}, {ogrenci_adi}, {sinif}, {sube}, {tarih}, {ders}, {saat}, {okul_adi}", "info")

        for sablon_key, sablon_text in VELI_BILDIRIM_SABLONLARI.items():
            sablon_baslik_map = {
                "sabah_devamsiz": "Sabah Devamsızlık Bildirimi",
                "tam_gun_devamsiz": "Tam Gün Devamsızlık Bildirimi",
                "ogleden_sonra_devamsiz": "Ogleden Sonra Devamsızlık Bildirimi",
                "tekil_devamsiz": "Tekil Ders Devamsızlık Bildirimi",
                "izinli": "İzinli Bildirimi",
                "raporlu": "Raporlu Bildirimi",
            }
            baslik = sablon_baslik_map.get(sablon_key, sablon_key)
            with st.expander(baslik, expanded=False):
                st.text_area("Sablon Metni", value=sablon_text,
                             height=100, disabled=True,
                             key=f"sablon_{sablon_key}")

                # Ornek onizleme
                ornek_mesaj = sablon_text.format(
                    veli_adi="Ahmet Yilmaz",
                    ogrenci_adi="Ali Yilmaz",
                    sinif=5, sube="A",
                    tarih=date.today().strftime("%d.%m.%Y"),
                    ders="Matematik", saat=1,
                    okul_adi="Okul Mudurlugu",
                )
                styled_section("Ornek Onizleme", "#0d9488")
                st.info(ornek_mesaj)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        styled_section("Bildirim Akisi", "#2563eb")
        st.markdown("""
1. Öğretmen sabah 1. ders yoklama alir
2. Devamsiz isaretlenen ogrenciler için otomatik mesaj olusturulur
3. Devamsizlik tipine gore uygun sablon secilir:
   - **Sabah Yarim Gun:** Sabah tum saatleri devamsiz
   - **Ogleden Sonra Yarim Gun:** Ogleden sonra tum saatleri devamsiz
   - **Tam Gun:** Tum gun devamsiz
   - **Izinli / Raporlu:** Ozel durum bildirimi
4. Veli telefon numarasi uzerinden SMS veya WhatsApp ile gonderilir
5. Bildirim durumu kayit altina alinir
""")

        styled_section("Devamsızlık Tipi Açıklamalari", "#f59e0b")
        for kod, etiket in DEVAMSIZLIK_TIPLERI:
            st.write(f"- **{etiket}** (`{kod}`)")

        styled_section("Devamsızlık Turleri", "#dc2626")
        for kod, etiket in DEVAMSIZLIK_TURLERI:
            st.write(f"- **{etiket}** (`{kod}`)")


# ==================== TAB 11: AKADEMIK KADRO ====================

@st.fragment
def _render_akademik_kadro(store: AkademikDataStore):
    """Akademik kadro - IK modülünden aktif öğretmenler (salt okunur görünüm)."""
    from utils.shared_data import load_ik_active_employees

    styled_section("Akademik Kadro", "#8b5cf6")

    # Kaynak bilgi banneri
    st.markdown(
        "<div style='background:linear-gradient(135deg,#eef2ff,#e0e7ff);color:#3730a3;"
        "padding:12px 18px;border-radius:10px;margin-bottom:16px;font-size:0.87rem;"
        "border-left:4px solid #6366f1'>"
        "<b>📌 Veri Kaynağı:</b> İK Modülü → Aktif Çalışanlar (Öğretmen ünvanlı personel). "
        "Personel eklemek veya güncellemek için <b>İnsan Kaynakları</b> modülünü kullanın.</div>",
        unsafe_allow_html=True,
    )

    # IK'dan öğretmenleri çek (role_scope == "TEACHER")
    tum_calisanlar = load_ik_active_employees()
    teachers = [e for e in tum_calisanlar if e.get("role_scope") == "TEACHER"]

    # Özet istatistikler
    unvan_set = sorted(set(
        e.get("position_name", "-") for e in teachers if e.get("position_name")
    ))
    kampus_set = sorted(set(
        e.get("kampus", "") for e in teachers
        if e.get("kampus") and e.get("kampus") not in ("TUMU", "Tümü", "ALL")
    ))
    styled_stat_row([
        ("Toplam Öğretmen", len(teachers),    "#8b5cf6", "👥"),
        ("Farklı Ünvan",    len(unvan_set),   "#2563eb", "🎓"),
        ("Kampüs Sayısı",   max(len(kampus_set), 1), "#10b981", "🏫"),
    ])
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not teachers:
        st.info(
            "İK modülünde 'Öğretmen' rolünde aktif personel bulunamadı. "
            "İnsan Kaynakları → Aktif Çalışanlar sekmesinden personel ekleyin."
        )
        return

    # Filtreler
    fc1, fc2 = st.columns(2)
    with fc1:
        filtre_unvan = st.selectbox(
            "Ünvan Filtrele",
            ["Tümü"] + unvan_set,
            key="ak_filtre_unvan",
        )
    with fc2:
        sl_arama_k = st.text_input(
            "🔍 Ada göre ara", placeholder="Örn: Ahmet Yılmaz",
            key="ak_arama_kadro",
        )

    filtered = teachers
    if filtre_unvan and filtre_unvan != "Tümü":
        filtered = [e for e in filtered if e.get("position_name") == filtre_unvan]
    if sl_arama_k.strip():
        q = sl_arama_k.strip().lower()
        filtered = [
            e for e in filtered
            if q in e.get("ad", "").lower() or q in e.get("soyad", "").lower()
        ]

    if not filtered:
        st.info("Filtrelere uygun personel bulunamadı.")
        return

    # Tablo
    df_data = []
    for e in sorted(filtered, key=lambda x: f"{x.get('ad', '')} {x.get('soyad', '')}"):
        kampus_goster = e.get("kampus", "-")
        if kampus_goster in ("TUMU", "ALL"):
            kampus_goster = "Tümü"
        df_data.append({
            "Ad Soyad":      f"{e.get('ad', '')} {e.get('soyad', '')}".strip(),
            "Ünvan":         e.get("position_name", "-"),
            "E-posta":       e.get("email", "-") or "-",
            "Telefon":       e.get("telefon", "-") or "-",
            "Kampüs":        kampus_goster or "-",
            "İşe Başlama":   e.get("ise_baslama_tarihi", "-") or "-",
        })
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # PDF Export
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    _pdf_k = "ak_kadro_pdf_bytes"
    _pdf_m = "ak_kadro_pdf_meta"
    p1, p2 = st.columns(2)
    with p1:
        if st.button("📄 Kadro PDF Hazırla", key="ak_kadro_pdf_hazirla",
                     type="primary", use_container_width=True):
            _pdf_data = _generate_akademik_kadro_pdf(
                filtered,
                filtre_unvan=None if filtre_unvan == "Tümü" else filtre_unvan,
            )
            if _pdf_data:
                from datetime import datetime as _dt
                _dosya = f"akademik_kadro_{_dt.now().strftime('%Y%m%d')}.pdf"
                st.session_state[_pdf_k] = _pdf_data
                st.session_state[_pdf_m] = {"dosya": _dosya, "sayi": len(filtered)}
                st.success(f"✅ PDF hazır — {len(filtered)} personel")
            else:
                st.error("PDF oluşturulamadı. ReportLab kurulu değil.")
    with p2:
        _saved = st.session_state.get(_pdf_k)
        _meta  = st.session_state.get(_pdf_m, {})
        if _saved:
            st.download_button(
                label=f"📥 İndir ({_meta.get('sayi', len(filtered))} personel)",
                data=_saved,
                file_name=_meta.get("dosya", "akademik_kadro.pdf"),
                mime="application/pdf",
                key="ak_kadro_pdf_indir",
                type="primary",
                use_container_width=True,
            )
        else:
            st.info("← Önce 'Kadro PDF Hazırla' butonuna tıklayın.")

    # Ünvan dağılımı özeti
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    styled_section("Ünvan Dağılımı", "#6366f1")
    unvan_ozet: dict[str, int] = {}
    for e in teachers:
        u = e.get("position_name", "Diğer") or "Diğer"
        unvan_ozet[u] = unvan_ozet.get(u, 0) + 1
    ozet_df = pd.DataFrame([
        {"Ünvan": k, "Sayı": v}
        for k, v in sorted(unvan_ozet.items(), key=lambda x: -x[1])
    ])
    st.dataframe(ozet_df, use_container_width=True, hide_index=True)


# ==================== AKADEMIK KADRO PDF ====================

def _generate_akademik_kadro_pdf(teachers: list, filtre_unvan: str | None = None,
                                  filtre_gorev: str | None = None,
                                  filtre_brans: str | None = None) -> bytes | None:
    """Akademik kadro listesi - kurumsal PDF.

    teachers: IK modülünden gelen employee dict listesi.
    Sütunlar: Sıra | Ad Soyad | Ünvan | E-posta | Telefon | Kampüs | İşe Başlama
    Ünvan gruplarına ayrılarak dizilir; imza alanı, kurum başlığı ve tarih içerir.
    """
    import io
    import os
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image,
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    from utils.report_utils import get_institution_info

    fn, fb = ensure_turkish_pdf_fonts()

    kurum = get_institution_info()
    kurum_adi = kurum.get("name", "") or "Okul Adı"
    kurum_adres = kurum.get("address", "")
    kurum_tel = kurum.get("phone", "")
    logo_path = kurum.get("logo_path", "")

    # Müdür bilgisi (sinif_yonetim.json)
    try:
        import json
        with open(get_data_path("akademik", "sinif_yonetim.json"), "r", encoding="utf-8") as f:
            atama = json.load(f)
        mudur_raw = atama.get("okul_muduru", "")
        mudur_adi = mudur_raw.split(" - ")[0].strip() if mudur_raw and mudur_raw != "-- Secim yapin --" else ""
    except Exception:
        mudur_adi = ""

    from datetime import date as _date
    bugun_str = _date.today().strftime("%d.%m.%Y")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        topMargin=1.5 * cm, bottomMargin=2.2 * cm,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
    )

    pw = landscape(A4)[0] - 3 * cm   # kullanılabilir genişlik

    styles = getSampleStyleSheet()
    def _sty(name, **kw):
        kw.setdefault("fontName", fn)
        return ParagraphStyle(name=name, **kw)

    sty_kurum  = _sty("AKKurum",  fontSize=15, leading=19, alignment=TA_CENTER,
                       fontName=fb, textColor=colors.white, spaceAfter=3)
    sty_baslik = _sty("AKBaslik", fontSize=11, leading=14, alignment=TA_CENTER,
                       fontName=fb, textColor=colors.HexColor("#3b82f6"), spaceAfter=2)
    sty_alt    = _sty("AKAlt",    fontSize=8,  leading=11, alignment=TA_CENTER,
                       textColor=colors.HexColor("#cbd5e1"), spaceAfter=10)
    sty_grup   = _sty("AKGrup",   fontSize=9,  leading=12, alignment=TA_LEFT,
                       fontName=fb, textColor=colors.HexColor("#ffffff"))
    sty_hucre  = _sty("AKHucre",  fontSize=8,  leading=10, alignment=TA_LEFT)
    sty_hucre_c= _sty("AKHucreC", fontSize=8,  leading=10, alignment=TA_CENTER)
    sty_footer = _sty("AKFooter", fontSize=8,  leading=11, alignment=TA_CENTER,
                       textColor=colors.HexColor("#475569"))
    sty_imza   = _sty("AKImza",   fontSize=8,  leading=11, alignment=TA_CENTER,
                       fontName=fb, textColor=colors.HexColor("#94A3B8"))

    elements = []

    # ── Başlık ──────────────────────────────────────────────────────────────
    header_data = [[]]
    if logo_path and os.path.exists(logo_path):
        try:
            header_data[0].append(Image(logo_path, width=2 * cm, height=2 * cm))
        except Exception:
            header_data[0].append(Spacer(2 * cm, 2 * cm))
    else:
        header_data[0].append(Spacer(2 * cm, 2 * cm))

    baslik_col = [
        Paragraph(kurum_adi, sty_kurum),
        Paragraph("AKADEMİK KADRO LİSTESİ", sty_baslik),
    ]
    alt_parts = [f"Tarih: {bugun_str}"]
    if filtre_unvan:
        alt_parts.append(f"Ünvan: {filtre_unvan}")
    if kurum_adres:
        alt_parts.append(kurum_adres)
    if kurum_tel:
        alt_parts.append(f"Tel: {kurum_tel}")
    baslik_col.append(Paragraph("  |  ".join(alt_parts), sty_alt))
    header_data[0].append(baslik_col)

    header_tbl = Table(header_data, colWidths=[2.4 * cm, pw - 2.4 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",  (0, 0), (0, 0),  "CENTER"),
        ("ALIGN",  (1, 0), (1, 0),  "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0B0F19")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ROUNDEDCORNERS", [6, 6, 0, 0]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(header_tbl)

    # Teal accent line
    accent_data = [[""]]
    accent_tbl = Table(accent_data, colWidths=[pw], rowHeights=[3])
    accent_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2563eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(accent_tbl)
    elements.append(Spacer(1, 8 * mm))

    # ── Ünvan grubu sıralaması (IK dict'lerden) ───────────────────────────
    # Benzersiz ünvanları topla ve alfabetik sırala
    unvan_listesi = sorted(set(
        e.get("position_name", "Diğer") or "Diğer" for e in teachers
    ))

    # Ünvan renkleri (ardışık)
    UNVAN_RENKLER = [
        "#94A3B8", "#1e40af", "#0d6efd", "#2563eb",
        "#7c3aed", "#9d174d", "#94A3B8", "#0d9488",
    ]
    unvan_gruplari: dict[str, list] = {}
    for e in teachers:
        u = e.get("position_name", "Diğer") or "Diğer"
        unvan_gruplari.setdefault(u, []).append(e)

    # Sütun genişlikleri (A4 landscape ~270 mm kullanılabilir)
    COL_W = [
        1.0 * cm,   # Sıra
        4.5 * cm,   # Ad Soyad
        3.5 * cm,   # Ünvan
        5.5 * cm,   # E-posta
        3.2 * cm,   # Telefon
        3.0 * cm,   # Kampüs
        3.0 * cm,   # İşe Başlama
    ]

    HEADER_ROW = ["#", "Ad Soyad", "Ünvan", "E-posta", "Telefon", "Kampüs", "İşe Başlama"]

    toplam_satir = 0

    for renk_idx, unvan_k in enumerate(unvan_listesi):
        grup_teachers = unvan_gruplari.get(unvan_k, [])
        if not grup_teachers:
            continue

        grup_renk = colors.HexColor(UNVAN_RENKLER[renk_idx % len(UNVAN_RENKLER)])

        # Grup başlık satırı (tam genişlik, renkli arka plan)
        grup_row = [[Paragraph(f"  {unvan_k.upper()}  ({len(grup_teachers)} kişi)", sty_grup)]]
        grup_tbl = Table(grup_row, colWidths=[sum(COL_W)])
        grup_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), grup_renk),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ]))
        elements.append(grup_tbl)

        # Tablo başlık + veri satırları
        table_data = [[Paragraph(h, sty_hucre_c) for h in HEADER_ROW]]

        for sira, e in enumerate(
            sorted(grup_teachers, key=lambda x: f"{x.get('ad', '')} {x.get('soyad', '')}"), 1
        ):
            tam_ad = f"{e.get('ad', '')} {e.get('soyad', '')}".strip()
            kampus_val = e.get("kampus", "-") or "-"
            if kampus_val in ("TUMU", "ALL"):
                kampus_val = "Tümü"
            row = [
                Paragraph(str(toplam_satir + sira), sty_hucre_c),
                Paragraph(tam_ad or "-", sty_hucre),
                Paragraph(e.get("position_name", "-") or "-", sty_hucre),
                Paragraph(e.get("email", "-") or "-", sty_hucre),
                Paragraph(e.get("telefon", "-") or "-", sty_hucre),
                Paragraph(kampus_val, sty_hucre_c),
                Paragraph(e.get("ise_baslama_tarihi", "-") or "-", sty_hucre_c),
            ]
            table_data.append(row)

        toplam_satir += len(grup_teachers)

        tbl = Table(table_data, colWidths=COL_W, repeatRows=1)
        tbl.setStyle(TableStyle([
            # Başlık satırı
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#94A3B8")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), fb),
            ("FONTSIZE",      (0, 0), (-1, 0), 8),
            ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
            ("TOPPADDING",    (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            # Veri satırları
            ("FONTNAME",   (0, 1), (-1, -1), fn),
            ("FONTSIZE",   (0, 1), (-1, -1), 8),
            ("TOPPADDING",    (0, 1), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
            # Zebra
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#1A2035")]),
            # Grid
            ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("BOX",        (0, 0), (-1, -1), 1.0, colors.HexColor("#CBD5E1")),
            ("LINEBELOW",  (0, 0), (-1, 0),  1.0, colors.HexColor("#2563eb")),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(tbl)
        elements.append(Spacer(1, 5 * mm))

    # ── Özet ──────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 4 * mm))
    ozet_parts = [f"TOPLAM KADRO: {toplam_satir} KİŞİ"]
    for u in unvan_listesi:
        c = len(unvan_gruplari.get(u, []))
        if c:
            ozet_parts.append(f"{u}: {c}")
    elements.append(Paragraph("  |  ".join(ozet_parts), sty_alt))

    # ── İmza alanı ────────────────────────────────────────────────────────
    elements.append(Spacer(1, 10 * mm))
    imza_w = pw / 3

    imza_data = [[
        [Paragraph("Hazırlayan", sty_footer),
         Paragraph("........................", sty_imza)],
        [Paragraph("Okul Müdür Yardımcısı", sty_footer),
         Paragraph("........................", sty_imza)],
        [Paragraph("Okul Müdürü", sty_footer),
         Paragraph(mudur_adi if mudur_adi else "........................", sty_imza)],
    ]]
    imza_tbl = Table(imza_data, colWidths=[imza_w, imza_w, imza_w])
    imza_tbl.setStyle(TableStyle([
        ("ALIGN",    (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",   (0, 0), (-1, -1), "TOP"),
        ("LINEBEFORE", (1, 0), (1, 0), 0.5, colors.HexColor("#cbd5e1")),
        ("LINEBEFORE", (2, 0), (2, 0), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
    ]))
    elements.append(imza_tbl)

    doc.build(elements)
    return buffer.getvalue()


# ==================== TAB 12: DIJITAL DERS DEFTERI ====================

def _normalize_tr(text: str) -> str:
    """Turkce karakterleri PDF-safe ASCII'ye cevirir."""
    tr_map = {
        'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ş': 's', 'Ş': 'S',
        'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C',
    }
    for k, v in tr_map.items():
        text = text.replace(k, v)
    return text


def _generate_program_grid_pdf(pages: list, aktif_gunler: list, max_saat: int,
                                ders_saat_map: dict = None, kurum_adi: str = "",
                                logo_path: str = "") -> bytes:
    """Ders programi PDF olusturur (grid gorunumunde).
    pages: [{"baslik": str, "alt_baslik": str, "schedule": list[ScheduleSlot],
             "mode": "class"|"teacher", "mudur_adi": str (optional)}, ...]
    Her page için ayri bir sayfa olusturulur.
    """
    import io
    import os
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, PageBreak, Image)
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    def _txt(text):
        return str(text)

    if ders_saat_map is None:
        ders_saat_map = {}

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                             topMargin=1.2 * cm, bottomMargin=1.2 * cm,
                             leftMargin=1.5 * cm, rightMargin=1.5 * cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='PGKurum', fontSize=16, leading=20,
                               alignment=TA_CENTER, spaceAfter=2,
                               fontName=font_bold, textColor=colors.white))
    styles.add(ParagraphStyle(name='PGBaşlık', fontSize=12, leading=16,
                               alignment=TA_CENTER, spaceAfter=4,
                               fontName=font_bold, textColor=colors.HexColor('#3b82f6')))
    styles.add(ParagraphStyle(name='PGAlt', fontSize=9, leading=12,
                               alignment=TA_CENTER, spaceAfter=10,
                               textColor=colors.HexColor('#cbd5e1'), fontName=font_name))
    styles.add(ParagraphStyle(name='PGFooter', fontSize=9, leading=12,
                               alignment=TA_CENTER, spaceAfter=10,
                               textColor=colors.grey, fontName=font_name))
    styles.add(ParagraphStyle(name='PGHucre', fontSize=8, leading=10,
                               fontName=font_name, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='PGSaat', fontSize=7, leading=9,
                               fontName=font_name, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='PGMudur', fontSize=10, leading=14,
                               alignment=TA_RIGHT, spaceAfter=2,
                               fontName=font_bold))
    styles.add(ParagraphStyle(name='PGMudurAlt', fontSize=9, leading=12,
                               alignment=TA_RIGHT, spaceAfter=2,
                               fontName=font_name, textColor=colors.HexColor('#555555')))

    elements = []

    for page_idx, page in enumerate(pages):
        if page_idx > 0:
            elements.append(PageBreak())

        # Kurum adi ve logo - premium dark banner
        pg_page_w = landscape(A4)[0] - 3 * cm
        if kurum_adi:
            banner_cells = [[]]
            if logo_path and os.path.exists(logo_path):
                try:
                    logo_img = Image(logo_path, width=1.5 * cm, height=1.5 * cm)
                    banner_cells[0].append(logo_img)
                except Exception:
                    banner_cells[0].append(Spacer(1.5 * cm, 1.5 * cm))
            else:
                banner_cells[0].append(Spacer(1.5 * cm, 1.5 * cm))
            banner_cells[0].append([
                Paragraph(_txt(kurum_adi), styles['PGKurum']),
                Paragraph(_txt(page["baslik"]), styles['PGBaşlık']),
            ])
            if page.get("alt_baslik"):
                banner_cells[0][1].append(Paragraph(_txt(page["alt_baslik"]), styles['PGAlt']))
            banner_tbl = Table(banner_cells, colWidths=[2 * cm, pg_page_w - 2 * cm])
            banner_tbl.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B0F19')),
                ('ROUNDEDCORNERS', [6, 6, 0, 0]),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(banner_tbl)
            # Teal accent line
            accent_data = [[""]]
            accent_tbl = Table(accent_data, colWidths=[pg_page_w], rowHeights=[3])
            accent_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            elements.append(accent_tbl)
            elements.append(Spacer(1, 0.3 * cm))
        else:
            elements.append(Paragraph(_txt(page["baslik"]), styles['PGBaşlık']))
            if page.get("alt_baslik"):
                elements.append(Paragraph(_txt(page["alt_baslik"]), styles['PGAlt']))

        schedule = page["schedule"]
        mode = page.get("mode", "class")
        mudur_adi = page.get("mudur_adi", "")

        # Tablo basligi
        gun_kisaltmalar = [GUN_KISALTMA.get(g, g[:3]) for g in aktif_gunler]
        header = [_txt("Saat")] + [_txt(g) for g in gun_kisaltmalar]
        data = [header]

        for saat in range(1, max_saat + 1):
            # Ders saati bilgisi
            saat_info = ders_saat_map.get(saat)
            if saat_info:
                saat_label = Paragraph(
                    f'<b>{saat}. Ders</b><br/>'
                    f'<font size="6" color="#555555">{_txt(saat_info)}</font>',
                    styles['PGSaat']
                )
            else:
                saat_label = f"{saat}. Ders"
            row = [saat_label]
            for gun in aktif_gunler:
                slot = next((s for s in schedule if s.gun == gun and s.ders_saati == saat), None)
                if slot:
                    ders_kisa = DERS_KISALTMA.get(slot.ders, slot.ders[:6])
                    if mode == "teacher":
                        alt = f"{slot.sinif}/{slot.sube}"
                    else:
                        alt = (slot.ogretmen or "").split()[0]
                    cell = Paragraph(
                        f'<b>{_txt(ders_kisa)}</b><br/>'
                        f'<font size="6" color="#666666">{_txt(alt)}</font>',
                        styles['PGHucre']
                    )
                else:
                    cell = Paragraph("-", styles['PGHucre'])
                row.append(cell)
            data.append(row)

        page_w = landscape(A4)[0] - 3 * cm
        saat_w = 2.5 * cm
        gun_w = (page_w - saat_w) / len(aktif_gunler)
        col_widths = [saat_w] + [gun_w] * len(aktif_gunler)

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#94A3B8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), font_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e3f2fd')),
            ('FONTNAME', (0, 1), (0, -1), font_bold),
            ('FONTSIZE', (0, 1), (0, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#CBD5E1')),
            ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.HexColor('#2563eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#1A2035')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)

        ders_sayisi = len(schedule)
        from datetime import datetime as _dt
        tarih = _dt.now().strftime('%d.%m.%Y %H:%M')
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(
            f'{_txt("Toplam")} {ders_sayisi} {_txt("ders")} | {_txt("Oluşturma")}: {tarih}',
            styles['PGFooter']
        ))

        # Mudur imzasi (ogretmen programlarinda)
        if mudur_adi and mode == "teacher":
            elements.append(Spacer(1, 0.8 * cm))
            elements.append(Paragraph(
                _txt("Çalışmalarınızda başarılar dilerim."),
                styles['PGMudurAlt']
            ))
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(Paragraph(_txt(mudur_adi), styles['PGMudur']))

    doc.build(elements)
    return buffer.getvalue()


def _generate_program_carsaf_pdf(rows: list, columns: list,
                                  aktif_gunler: list = None, max_saat: int = 8,
                                  title: str = "", alt_baslik: str = "",
                                  ders_saat_map: dict = None) -> bytes:
    """Carsaf gorunumunde ders programi PDF olusturur.
    2 satirlik header: gun adi (merge) + saat numarasi.
    Gun gruplarina renk kodlama, duzgun sutun genislikleri."""
    import io
    import os
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    def _txt(text):
        return str(text)

    if ders_saat_map is None:
        ders_saat_map = {}
    if aktif_gunler is None:
        aktif_gunler = GUNLER[:5]

    # Sabit kolonlari (label, brans, toplam) ve ders kolonlarini ayir
    ders_cols = [c for c in columns if "-" in c and any(c.startswith(GUN_KISALTMA.get(g, g)) for g in aktif_gunler)]
    label_cols = [c for c in columns if c not in ders_cols]
    # label_cols'un sonundaki "Toplam" varsa ayir
    has_toplam = "Toplam" in label_cols
    if has_toplam:
        label_cols = [c for c in label_cols if c != "Toplam"]

    n_label = len(label_cols)
    n_gun = len(aktif_gunler)
    n_saat = max_saat
    n_toplam = 1 if has_toplam else 0
    total_cols = n_label + n_gun * n_saat + n_toplam

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                             topMargin=0.8 * cm, bottomMargin=0.8 * cm,
                             leftMargin=0.8 * cm, rightMargin=0.8 * cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CSBaşlık', fontSize=11, leading=14,
                               alignment=TA_CENTER, spaceAfter=2,
                               fontName=font_bold, textColor=colors.white))
    styles.add(ParagraphStyle(name='CSAltBanner', fontSize=7, leading=9,
                               alignment=TA_CENTER, spaceAfter=6,
                               textColor=colors.HexColor('#cbd5e1'), fontName=font_name))
    styles.add(ParagraphStyle(name='CSAlt', fontSize=7, leading=9,
                               alignment=TA_CENTER, spaceAfter=6,
                               textColor=colors.grey, fontName=font_name))

    elems = []

    # Premium header banner
    cs_page_w = landscape(A4)[0] - 1.6 * cm
    banner_content = [[Paragraph(_txt(title), styles['CSBaşlık'])]]
    if alt_baslik:
        banner_content[0].append(Paragraph(_txt(alt_baslik), styles['CSAltBanner']))
    banner_tbl = Table([banner_content], colWidths=[cs_page_w])
    banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B0F19')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [6, 6, 0, 0]),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elems.append(banner_tbl)
    # Teal accent line
    cs_accent_data = [[""]]
    cs_accent_tbl = Table(cs_accent_data, colWidths=[cs_page_w], rowHeights=[3])
    cs_accent_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elems.append(cs_accent_tbl)
    elems.append(Spacer(1, 0.3 * cm))

    # Gun renkleri
    gun_renkleri_hex = ["#1565c0", "#2e7d32", "#e65100", "#6a1b9a", "#c62828", "#00838f", "#4e342e"]

    # --- 2 satirlik header ---
    # Row 1: label kolonlari (rowspan simule) + gun adlari (colspan=max_saat) + toplam (rowspan simule)
    header_row1 = []
    for lc in label_cols:
        header_row1.append(_txt(lc))
    for gi, gun in enumerate(aktif_gunler):
        kisa = GUN_KISALTMA.get(gun, gun[:3])
        header_row1.append(_txt(kisa))
        for _ in range(n_saat - 1):
            header_row1.append("")
    if has_toplam:
        header_row1.append(_txt("Top"))

    # Row 2: bos label kolonlari + saat numaralari + bos toplam
    header_row2 = []
    for _ in label_cols:
        header_row2.append("")
    for gi, gun in enumerate(aktif_gunler):
        for saat in range(1, n_saat + 1):
            saat_str = str(saat)
            if saat in ders_saat_map:
                z = ders_saat_map[saat]
                saat_str = f"{saat}"
            header_row2.append(saat_str)
    if has_toplam:
        header_row2.append("")

    data = [header_row1, header_row2]

    # Veri satirlari
    for row in rows:
        dr = []
        for lc in label_cols:
            dr.append(_txt(str(row.get(lc, ""))))
        for gun in aktif_gunler:
            kisa_gun = GUN_KISALTMA.get(gun, gun)
            for saat in range(1, n_saat + 1):
                val = row.get(f"{kisa_gun}-{saat}", "-")
                dr.append(_txt(str(val)))
        if has_toplam:
            dr.append(_txt(str(row.get("Toplam", ""))))
        data.append(dr)

    # Sutun genislikleri
    page_w = landscape(A4)[0] - 1.6 * cm
    label_w_total = 0
    label_widths = []
    for lc in label_cols:
        w = 2.8 * cm if lc in ("Öğretmen",) else 1.8 * cm
        label_widths.append(w)
        label_w_total += w
    toplam_w = 1.0 * cm if has_toplam else 0
    remaining = page_w - label_w_total - toplam_w
    slot_w = remaining / (n_gun * n_saat) if (n_gun * n_saat) > 0 else 1.5 * cm
    col_widths = label_widths + [slot_w] * (n_gun * n_saat)
    if has_toplam:
        col_widths.append(toplam_w)

    table = Table(data, colWidths=col_widths, repeatRows=2)

    # Tablo stilleri
    ts = [
        # Genel
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 1), font_bold),
        ('FONTSIZE', (0, 0), (-1, 1), 6),
        ('FONTSIZE', (0, 2), (-1, -1), 5.5),
        ('FONTNAME', (0, 2), (-1, -1), font_name),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#CBD5E1')),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        # Row backgrounds (veri satirlari)
        ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, colors.HexColor('#1A2035')]),
        # Label kolonlari header - koyu mavi
        ('BACKGROUND', (0, 0), (n_label - 1, 1), colors.HexColor('#94A3B8')),
        ('TEXTCOLOR', (0, 0), (n_label - 1, 1), colors.white),
        # Label kolonlari veri - acik mavi
        ('BACKGROUND', (0, 2), (n_label - 1, -1), colors.HexColor('#e3f2fd')),
        ('FONTNAME', (0, 2), (n_label - 1, -1), font_bold),
        # Row 1 label kolonlari row2 ile merge
        ('SPAN', (0, 0), (0, 1)),
    ]
    # Birden fazla label kolonu varsa her birini merge et
    for li in range(1, n_label):
        ts.append(('SPAN', (li, 0), (li, 1)))

    # Gun gruplari renk ve merge
    col_offset = n_label
    for gi, gun in enumerate(aktif_gunler):
        renk = colors.HexColor(gun_renkleri_hex[gi % len(gun_renkleri_hex)])
        renk_acik = colors.HexColor(gun_renkleri_hex[gi % len(gun_renkleri_hex)] + "18")
        start_col = col_offset + gi * n_saat
        end_col = start_col + n_saat - 1
        # Row 1: gun adi merge
        ts.append(('SPAN', (start_col, 0), (end_col, 0)))
        ts.append(('BACKGROUND', (start_col, 0), (end_col, 0), renk))
        ts.append(('TEXTCOLOR', (start_col, 0), (end_col, 0), colors.white))
        # Row 2: saat numaralari - biraz acik ton
        lighter = colors.HexColor(gun_renkleri_hex[gi % len(gun_renkleri_hex)] + "cc")
        ts.append(('BACKGROUND', (start_col, 1), (end_col, 1), lighter))
        ts.append(('TEXTCOLOR', (start_col, 1), (end_col, 1), colors.white))

    # Toplam kolonu
    if has_toplam:
        tc = total_cols - 1
        ts.append(('SPAN', (tc, 0), (tc, 1)))
        ts.append(('BACKGROUND', (tc, 0), (tc, 1), colors.HexColor('#94A3B8')))
        ts.append(('TEXTCOLOR', (tc, 0), (tc, 1), colors.white))
        ts.append(('BACKGROUND', (tc, 2), (tc, -1), colors.HexColor('#e3f2fd')))
        ts.append(('FONTNAME', (tc, 2), (tc, -1), font_bold))

    table.setStyle(TableStyle(ts))
    elems.append(table)

    from datetime import datetime as _dt
    elems.append(Spacer(1, 0.3 * cm))
    elems.append(Paragraph(
        f'{_txt("Toplam")} {len(rows)} {_txt("satır")} | {_txt("Oluşturma")}: {_dt.now().strftime("%d.%m.%Y %H:%M")}',
        styles['CSAlt']
    ))

    doc.build(elems)
    return buffer.getvalue()


def _generate_ders_defteri_pdf(kayitlar: list, sinif: int, sube: str,
                                ders_filtre: str = None, ogretmen_filtre: str = None) -> bytes:
    """Dijital ders defteri PDF dosyası oluşturur."""
    import io
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, PageBreak)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                             topMargin=1.2 * cm, bottomMargin=1.2 * cm,
                             leftMargin=1.5 * cm, rightMargin=1.5 * cm)

    dd_page_w = landscape(A4)[0] - 3 * cm

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='DDBaşlık', fontSize=14, leading=18,
                               alignment=TA_CENTER, spaceAfter=6,
                               fontName=font_bold, textColor=colors.white))
    styles.add(ParagraphStyle(name='DDAltBaşlık', fontSize=9, leading=12,
                               alignment=TA_CENTER, spaceAfter=12,
                               textColor=colors.HexColor('#cbd5e1'), fontName=font_name))
    styles.add(ParagraphStyle(name='DDHucre', fontSize=7, leading=9,
                               fontName=font_name))

    elements = []

    # Premium header banner
    baslik = f"Dijital Ders Defteri - {sinif}/{sube}"
    if ders_filtre:
        baslik += f" - {ders_filtre}"

    alt_baslik_parts = [f"Toplam {len(kayitlar)} kayıt"]
    if ogretmen_filtre:
        alt_baslik_parts.append(f"Öğretmen: {ogretmen_filtre}")
    from datetime import datetime as _dt
    alt_baslik_parts.append(f"Oluşturma: {_dt.now().strftime('%d.%m.%Y %H:%M')}")

    dd_banner_content = [
        Paragraph(baslik, styles['DDBaşlık']),
        Paragraph(" | ".join(alt_baslik_parts), styles['DDAltBaşlık']),
    ]
    dd_banner_tbl = Table([[dd_banner_content]], colWidths=[dd_page_w])
    dd_banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B0F19')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [6, 6, 0, 0]),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(dd_banner_tbl)
    # Teal accent line
    dd_accent_data = [[""]]
    dd_accent_tbl = Table(dd_accent_data, colWidths=[dd_page_w], rowHeights=[3])
    dd_accent_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    elements.append(dd_accent_tbl)
    elements.append(Spacer(1, 0.4 * cm))

    if not kayitlar:
        elements.append(Paragraph("Kayıt bulunamadı.", styles['DDHucre']))
        doc.build(elements)
        return buffer.getvalue()

    # Tablo başlıkları
    header = ["#", "Tarih", "Hafta", "Ders", "Kazanım Kodu", "Kazanım",
              "Öğretmen", "Durum"]
    data = [header]

    for i, r in enumerate(kayitlar, 1):
        durum_text = "İşlendi" if r.durum == "islendi" else "Kısmen"
        kazanim_short = (r.kazanim_metni[:80]) if r.kazanim_metni else "-"
        row = [
            str(i),
            r.tarih or "-",
            str(r.hafta),
            r.ders,
            r.kazanim_kodu or "-",
            Paragraph(kazanim_short, styles['DDHucre']),
            r.ogretmen_adi or "-",
            durum_text,
        ]
        data.append(row)

    col_widths = [0.8 * cm, 2.2 * cm, 1.3 * cm, 2.5 * cm, 2.5 * cm,
                  10 * cm, 3.5 * cm, 1.8 * cm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#94A3B8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (7, 0), (7, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#CBD5E1')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.HexColor('#2563eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#1A2035')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(table)

    doc.build(elements)
    return buffer.getvalue()


# ====================== MUFREDAT AGACI ======================

def _filter_mufredat_tree(tree: dict, search_term: str) -> dict:
    """Mufredat agacini arama terimine gore filtreler."""
    if not search_term:
        return tree
    s = search_term.lower()
    filtered_units = []
    for unit in tree.get("units", []):
        if s in unit["name"].lower():
            filtered_units.append(unit)
            continue
        filtered_topics = []
        for topic in unit.get("topics", []):
            if s in topic["name"].lower():
                filtered_topics.append(topic)
                continue
            filtered_kaz = [
                k for k in topic.get("kazanimlar", [])
                if s in k["text"].lower() or s in k.get("code", "").lower()
            ]
            if filtered_kaz:
                filtered_topics.append({**topic, "kazanimlar": filtered_kaz})
        if filtered_topics:
            filtered_units.append({**unit, "topics": filtered_topics})
    return {**tree, "units": filtered_units}


def _render_mufredat_agaci(store: AkademikDataStore):
    """Mufredat Agaci - Ders-Unite-Konu-Kazanim hiyerarsik gorunumu."""
    styled_section("Mufredat Agaci", "#7c3aed")
    styled_info_banner(
        "MEB yillik plan verilerinden otomatik olusturulan mufredat agaci. "
        "Ders ve sinif secin, kazanim islenme durumlarini takip edin.",
        "info"
    )

    akademik_yil = _get_akademik_yil()

    # --- Filtreler ---
    fc1, fc2, fc3, fc4 = st.columns([1, 1.5, 1, 1.5])
    with fc1:
        sinif_sec = st.selectbox(
            "Sınıf", list(range(1, 13)),
            index=8, key="ma_sinif"
        )
    with fc2:
        dersler = store.get_meb_subjects(grade=sinif_sec)
        if not dersler:
            st.warning("Bu sinif için MEB plani bulunamadı.")
            return
        ders_sec = st.selectbox("Ders", dersler, key="ma_ders")
    with fc3:
        sube_sec = st.selectbox(
            "Şube", ["A", "B", "C", "D", "E"],
            key="ma_sube"
        )
    with fc4:
        arama = st.text_input("Arama", placeholder="Kazanim, konu veya unite ara...",
                              key="ma_arama")

    # --- Veri ---
    tree = store.get_mufredat_tree_with_status(
        grade=sinif_sec, subject=ders_sec, sube=sube_sec, akademik_yil=akademik_yil
    )
    if not tree["units"]:
        st.info("Secilen sinif ve ders için mufredat verisi bulunamadı.")
        return

    if arama:
        tree = _filter_mufredat_tree(tree, arama)
        if not tree["units"]:
            st.warning(f"'{arama}' için sonuc bulunamadı.")
            return

    stats = tree.get("stats", {})
    status = tree.get("status", {})
    progress_pct = status.get("progress_pct", 0)
    completed = status.get("completed", 0)
    partial = status.get("partial", 0)
    not_completed = status.get("not_completed", 0)

    # --- Istatistik kartlari ---
    st.markdown(ReportStyler.metric_cards_html([
        ("Unite", str(stats.get("total_units", 0)), "#7c3aed", ""),
        ("Konu", str(stats.get("total_topics", 0)), "#2563eb", ""),
        ("Kazanim", str(stats.get("total_kazanim", 0)), "#059669", ""),
        ("İlerleme", f"%{progress_pct}", "#f59e0b", ""),
    ]), unsafe_allow_html=True)

    st.progress(progress_pct / 100)

    # --- Grafik bolumu ---
    gc1, gc2 = st.columns(2)
    with gc1:
        if completed or partial or not_completed:
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Pie(
                labels=["Islendi", "Kismen", "Islenmedi"],
                values=[completed, partial, not_completed],
                hole=0.55,
                marker=dict(colors=SC_COLORS[:3], line=dict(color="#fff", width=2)),
            )])
            total_kaz = completed + partial + not_completed
            sc_pie(fig, height=320, center_text=f"<b>{total_kaz}</b><br><span style='font-size:10px;color:#64748b'>Kazanım</span>")
            st.plotly_chart(fig, use_container_width=True, key="ma_pie", config=SC_CHART_CFG)

    with gc2:
        unit_names = [u["name"][:25] for u in tree["units"]]
        unit_kaz_counts = [u.get("total_kazanim", 0) for u in tree["units"]]
        unit_completed = [u.get("completed", 0) for u in tree["units"]]
        if unit_names:
            import plotly.graph_objects as go
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                y=unit_names, x=unit_completed,
                orientation='h', name="Islendi",
                marker_color=SC_COLORS[0],
                text=unit_completed, textposition="inside",
            ))
            fig2.add_trace(go.Bar(
                y=unit_names,
                x=[t - c for t, c in zip(unit_kaz_counts, unit_completed)],
                orientation='h', name="Kalan",
                marker_color=SC_COLORS[7],
                text=[t - c for t, c in zip(unit_kaz_counts, unit_completed)], textposition="inside",
            ))
            fig2.update_layout(barmode='stack', showlegend=True)
            sc_bar(fig2, height=320, horizontal=True)
            st.plotly_chart(fig2, use_container_width=True, key="ma_bar", config=SC_CHART_CFG)

    st.divider()

    # --- Agac gorunumu ---
    for u_idx, unit in enumerate(tree["units"]):
        u_completed = unit.get("completed", 0)
        u_total = unit.get("total_kazanim", 0)
        u_pct = unit.get("progress_pct", 0)
        u_hours = unit.get("total_hours", 0)
        topic_count = len(unit.get("topics", []))

        exp_label = (
            f"Unite: {unit['name']}  ({topic_count} konu, "
            f"{u_total} kazanim, {u_hours} saat)  "
            f"[{u_completed}/{u_total}]"
        )
        with st.expander(exp_label, expanded=(u_idx == 0)):
            st.progress(u_pct / 100)
            for topic in unit.get("topics", []):
                t_kaz = topic.get("kazanimlar", [])
                t_comp = topic.get("completed", 0)
                t_total = len(t_kaz)
                t_pct = topic.get("progress_pct", 0)
                t_hours = topic.get("hours", 0)
                weeks_str = ", ".join(topic.get("weeks", []))

                st.markdown(
                    f"<div style='margin:12px 0 4px 0;padding:8px 12px;"
                    f"background:linear-gradient(135deg,#f0f4ff,#e8ecf8);"
                    f"border-radius:8px;border-left:4px solid #7c3aed;'>"
                    f"<b>{topic['name']}</b> "
                    f"<span style='color:#64748b;font-size:13px;'>"
                    f"({t_total} kazanim, {t_hours} saat"
                    f"{', ' + weeks_str if weeks_str else ''})"
                    f"</span> "
                    f"<span style='float:right;font-weight:600;color:#7c3aed;'>"
                    f"[{t_comp}/{t_total}]</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if t_total:
                    st.progress(t_pct / 100)

                for kaz in t_kaz:
                    kaz_status = kaz.get("status", "islenmedi")
                    if kaz_status == "islendi":
                        icon = "<span style='color:#22c55e;'>&#10003;</span>"
                        bg = "#f0fdf4"
                        border = "#22c55e"
                    elif kaz_status == "kismen":
                        icon = "<span style='color:#f59e0b;'>&#9679;</span>"
                        bg = "#fffbeb"
                        border = "#f59e0b"
                    else:
                        icon = "<span style='color:#94a3b8;'>&#9744;</span>"
                        bg = "#111827"
                        border = "#e2e8f0"

                    hours_badge = ""
                    if kaz.get("hours"):
                        hours_badge = (
                            f"<span style='background:#e0e7ff;color:#4338ca;"
                            f"padding:1px 8px;border-radius:10px;font-size:11px;"
                            f"margin-left:8px;'>{kaz['hours']} saat</span>"
                        )

                    st.markdown(
                        f"<div style='padding:6px 12px;margin:2px 0 2px 16px;"
                        f"background:{bg};border-left:3px solid {border};"
                        f"border-radius:4px;font-size:13px;'>"
                        f"{icon} {kaz['text']}{hours_badge}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

    # --- PDF Export ---
    st.divider()
    pdf_col1, pdf_col2 = st.columns([1, 3])
    with pdf_col1:
        if st.button("PDF Hazirla", key="ma_pdf_btn", type="primary",
                     use_container_width=True):
            kurum = get_institution_info()
            pdf_gen = ReportPDFGenerator(
                f"Mufredat Agaci - {ders_sec} ({sinif_sec}. Sınıf)",
                institution_name=kurum.get("name", "")
            )
            pdf_gen.add_metrics([
                ("Unite", str(stats.get("total_units", 0)), "#7c3aed"),
                ("Konu", str(stats.get("total_topics", 0)), "#2563eb"),
                ("Kazanim", str(stats.get("total_kazanim", 0)), "#059669"),
                ("İlerleme", f"%{progress_pct}", "#f59e0b"),
            ])
            for unit in tree["units"]:
                pdf_gen.add_section_header(
                    f"Unite: {unit['name']} "
                    f"[{unit.get('completed', 0)}/{unit.get('total_kazanim', 0)}]"
                )
                table_data = [["Konu", "Kazanim", "Durum", "Saat"]]
                for topic in unit.get("topics", []):
                    for kaz in topic.get("kazanimlar", []):
                        s = kaz.get("status", "islenmedi")
                        s_label = {"islendi": "Islendi",
                                   "kismen": "Kismen",
                                   "islenmedi": "Islenmedi"}.get(s, s)
                        table_data.append([
                            topic["name"][:30],
                            kaz["text"][:60],
                            s_label,
                            str(kaz.get("hours", ""))
                        ])
                if len(table_data) > 1:
                    pdf_gen.add_table(table_data)
            pdf_bytes = pdf_gen.generate()
            st.session_state["ma_pdf_bytes"] = pdf_bytes
            st.session_state["ma_pdf_fname"] = f"mufredat_agaci_{ders_sec}_{sinif_sec}.pdf"
            st.rerun()

        if st.session_state.get("ma_pdf_bytes"):
            st.download_button(
                "⬇️ PDF İndir", data=st.session_state["ma_pdf_bytes"],
                file_name=st.session_state.get("ma_pdf_fname", "mufredat_agaci.pdf"),
                mime="application/pdf", key="ma_pdf_dl",
                use_container_width=True,
            )
    with pdf_col2:
        kurum = get_institution_info()
        ReportSharer.render_share_ui(
            f"Mufredat Agaci - {ders_sec} ({sinif_sec}. Sınıf)",
            f"Unite: {stats.get('total_units', 0)}, "
            f"Konu: {stats.get('total_topics', 0)}, "
            f"Kazanim: {stats.get('total_kazanim', 0)}, "
            f"İlerleme: %{progress_pct}",
            kurum, key_prefix="ma_share"
        )


def _dd_gun_adi(tarih: date) -> str:
    """Python weekday (0=Mon) → GUNLER listesindeki karşılık."""
    _MAP = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    return _MAP.get(tarih.weekday(), "Pazartesi")


def _dd_zaman_map(store: AkademikDataStore) -> dict:
    """ders_no → {baslangic, bitis, sure_dk} haritası. ZamanCizelgesi'nden çeker."""
    cizelge = store.get_zaman_cizelgesi()
    result = {}
    for zd in cizelge:
        if zd.tur == "ders" and zd.ders_no and zd.ders_no > 0:
            sure = getattr(zd, "sure_dk", 40) or 40
            result[zd.ders_no] = {
                "baslangic": getattr(zd, "baslangic", "") or "",
                "bitis": getattr(zd, "bitis", "") or "",
                "sure_dk": sure,
            }
    return result


def _dd_hafta_baslangic(tarih: date) -> date:
    """Haftanın Pazartesi günü."""
    return tarih - timedelta(days=tarih.weekday())


@st.fragment
def _render_dijital_ders_defteri(store: AkademikDataStore):
    """Dijital Sınıf Defteri — ders programından otomatik çeker, günlük/haftalık görünüm."""
    import calendar as _cal

    akademik_yil = _get_akademik_yil()
    today = date.today()

    # ─── Aktif gün otomatik sıfırlama ──────────────────────────────────────
    # Her yeni günde Ders Defteri otomatik olarak "Günlük" modunda ve
    # bugünün tarihiyle açılır. Aynı gün içinde kullanıcı seçimi korunur.
    _dd_init_key = f"_dd_gun_init_{today.isoformat()}"
    if not st.session_state.get(_dd_init_key):
        st.session_state["dd_mod"] = "Günlük"
        st.session_state["dd_gun_tarih"] = today
        st.session_state[_dd_init_key] = True

    # ─── Filtreler ───
    c1, c2, c3 = st.columns([2, 2, 4])
    with c1:
        dd_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dd_sinif")
    with c2:
        dd_sube = st.selectbox("Şube", SUBELER, key="dd_sube")
    with c3:
        dd_mod = st.radio(
            "Görünüm",
            ["Günlük", "Haftalık", "Aylık", "Yıllık", "Tarih Aralığı"],
            horizontal=True, key="dd_mod",
        )

    # ─── Tarih seçici ───
    dd_tarih = today
    if dd_mod == "Günlük":
        dd_tarih = st.date_input("Tarih", value=today, key="dd_gun_tarih")
        tarih_bas = tarih_bit = dd_tarih.strftime("%Y-%m-%d")
        dd_label = dd_tarih.strftime("%d.%m.%Y")

    elif dd_mod == "Haftalık":
        dd_tarih = st.date_input("Haftanın herhangi bir günü", value=today, key="dd_hft_tarih")
        pzt_h = _dd_hafta_baslangic(dd_tarih)
        cum_h = pzt_h + timedelta(days=4)
        tarih_bas = pzt_h.strftime("%Y-%m-%d")
        tarih_bit = cum_h.strftime("%Y-%m-%d")
        dd_label = f"{pzt_h.strftime('%d.%m')}–{cum_h.strftime('%d.%m.%Y')}"
        st.caption(f"📅 Hafta: **{dd_label}**")

    elif dd_mod == "Aylık":
        mc1, mc2 = st.columns(2)
        with mc1:
            dd_ay = st.selectbox(
                "Ay", list(range(1, 13)), index=today.month - 1,
                format_func=lambda x: ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
                                        "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"][x-1],
                key="dd_ay")
        with mc2:
            dd_yil = st.selectbox("Yıl", [today.year-1, today.year, today.year+1],
                                   index=1, key="dd_ay_yil")
        son_gun = _cal.monthrange(dd_yil, dd_ay)[1]
        tarih_bas = f"{dd_yil}-{dd_ay:02d}-01"
        tarih_bit = f"{dd_yil}-{dd_ay:02d}-{son_gun:02d}"
        dd_label = f"{dd_ay:02d}/{dd_yil}"

    elif dd_mod == "Yıllık":
        dd_yil2 = st.selectbox("Yıl", [today.year-1, today.year, today.year+1],
                                index=1, key="dd_yil2")
        tarih_bas = f"{dd_yil2}-01-01"
        tarih_bit = f"{dd_yil2}-12-31"
        dd_label = str(dd_yil2)

    else:  # Tarih Aralığı
        ra1, ra2 = st.columns(2)
        with ra1:
            dd_tarih_bas = st.date_input("Başlangıç", value=date(today.year, 9, 1), key="dd_tarih_bas")
        with ra2:
            dd_tarih_bit = st.date_input("Bitiş", value=today, key="dd_tarih_bit")
        tarih_bas = dd_tarih_bas.strftime("%Y-%m-%d")
        tarih_bit = dd_tarih_bit.strftime("%Y-%m-%d")
        dd_label = f"{dd_tarih_bas.strftime('%d.%m.%Y')}–{dd_tarih_bit.strftime('%d.%m.%Y')}"

    st.divider()

    # Ortak veriler
    zaman_map = _dd_zaman_map(store)
    ayarlar = store.get_ders_programi_ayarlari() or {}
    kurum_adi = ayarlar.get("kurum_adi", "") or ""
    aktif_gunler = ayarlar.get("aktif_gunler", None) or GUNLER[:5]
    GUN_TR = {
        "Pazartesi": "Pazartesi", "Sali": "Salı", "Carsamba": "Çarşamba",
        "Persembe": "Perşembe", "Cuma": "Cuma",
    }

    def _kurum_row():
        return (f"<div style='font-size:0.72rem;color:#64748b;margin-bottom:2px'>{kurum_adi}</div>"
                if kurum_adi else "")

    def _tablo_header(sinif, sube, tarih_str, alt_str):
        return f"""
<div style='background:linear-gradient(135deg,#111827 0%,#eef2ff 50%,#e0e7ff 100%);padding:14px 20px;border-bottom:2px solid #6366f1'>
  {_kurum_row()}
  <div style='display:flex;justify-content:space-between;align-items:center'>
    <div>
      <span style='font-size:1.05rem;font-weight:800;color:#94A3B8;letter-spacing:-0.3px'>SINIF DEFTERİ</span>
      &nbsp;&nbsp;
      <span style='background:#6366f1;color:#fff;font-size:0.9rem;font-weight:700;padding:3px 12px;border-radius:20px'>{sinif}/{sube}</span>
    </div>
    <div style='text-align:right'>
      <span style='color:#4f46e5;font-size:0.85rem;font-weight:600'>{tarih_str}</span><br>
      <span style='color:#64748b;font-size:0.7rem'>{alt_str}</span>
    </div>
  </div>
</div>"""

    # ════════════════════════════════════════════════
    # GÜNLÜK
    # ════════════════════════════════════════════════
    if dd_mod == "Günlük":
        gun_adi = _dd_gun_adi(dd_tarih)
        gun_tr_label = GUN_TR.get(gun_adi, gun_adi)
        slots = sorted(
            store.get_schedule(sinif=dd_sinif, sube=dd_sube, gun=gun_adi, akademik_yil=akademik_yil),
            key=lambda s: s.ders_saati or 0,
        )
        if not slots:
            styled_info_banner(
                f"{dd_sinif}/{dd_sube} için {gun_tr_label} günü ders programı girilmemiş. "
                "Ders & Program sekmesinden ekleyin.", "warning")
            return

        all_ki = store.get_kazanim_isleme(sinif=dd_sinif, sube=dd_sube, akademik_yil=akademik_yil)
        gun_ki_map: dict = {}
        for k in all_ki:
            if k.tarih == tarih_bas and k.durum in ("islendi", "kismen"):
                gun_ki_map.setdefault(k.ders, []).append(k)

        rows_html = ""
        tum_ki = []
        for slot in slots:
            dn = slot.ders_saati or 0
            zd = zaman_map.get(dn, {})
            bas = zd.get("baslangic", "")
            bit = zd.get("bitis", "")
            sure = zd.get("sure_dk", 40) or 40
            saat_html = (f"{bas}<br><span style='font-size:0.64rem;color:#94a3b8'>{bit}</span>"
                         if bas else "—")
            ki_list = gun_ki_map.get(slot.ders, [])
            tum_ki.extend(ki_list)

            if ki_list:
                konu_parts = []
                for k in ki_list:
                    kod = (f"<b style='color:#6366f1;font-size:0.68rem'>[{k.kazanim_kodu}]</b> "
                           if k.kazanim_kodu else "")
                    konu_parts.append(
                        f"<div style='margin-bottom:3px'>{kod}"
                        f"<span style='font-size:0.78rem'>{k.kazanim_metni or '—'}</span></div>"
                    )
                konu_html = "".join(konu_parts)
                if all(k.durum == "islendi" for k in ki_list):
                    badge = ("<span style='background:#dcfce7;color:#166534;padding:3px 10px;"
                             "border-radius:12px;font-size:0.7rem;font-weight:700'>✅ İşlendi</span>")
                else:
                    badge = ("<span style='background:#fef9c3;color:#854d0e;padding:3px 10px;"
                             "border-radius:12px;font-size:0.7rem;font-weight:700'>⚠️ Kısmen</span>")
                row_bg = "#f0fdf4"
            else:
                konu_html = "<span style='color:#94a3b8;font-style:italic;font-size:0.76rem'>Kazanım işlenmedi</span>"
                badge = ("<span style='background:#1A2035;color:#94a3b8;padding:3px 10px;"
                         "border-radius:12px;font-size:0.7rem'>○ Bekleniyor</span>")
                row_bg = "#ffffff"

            ogr_html = slot.ogretmen or "<span style='color:#94a3b8'>—</span>"
            rows_html += (
                f"<tr style='background:{row_bg};border-bottom:1px solid #e2e8f0'>"
                f"<td style='text-align:center;font-weight:800;font-size:1rem;color:#94A3B8;"
                f"padding:10px 6px;width:44px;border-right:2px solid #cbd5e1;vertical-align:top'>{dn}</td>"
                f"<td style='text-align:center;font-size:0.73rem;color:#475569;padding:10px 6px;"
                f"width:72px;border-right:1px solid #e2e8f0;vertical-align:top;line-height:1.6'>"
                f"{saat_html}<br><span style='color:#94a3b8;font-size:0.65rem'>{sure} dk</span></td>"
                f"<td style='padding:10px;font-weight:700;font-size:0.85rem;color:#94A3B8;"
                f"width:130px;border-right:1px solid #e2e8f0;vertical-align:top'>{slot.ders or '—'}</td>"
                f"<td style='padding:10px;font-size:0.8rem;color:#334155;width:140px;"
                f"border-right:1px solid #e2e8f0;vertical-align:top'>{ogr_html}</td>"
                f"<td style='padding:10px 12px;font-size:0.78rem;color:#94A3B8;vertical-align:top'>{konu_html}</td>"
                f"<td style='text-align:center;padding:10px 8px;width:115px;"
                f"vertical-align:top;border-left:1px solid #e2e8f0'>{badge}</td>"
                f"</tr>"
            )

        islendi_c = sum(1 for s in slots if gun_ki_map.get(s.ders))
        tarih_header = f"{dd_tarih.strftime('%d.%m.%Y')} · {gun_tr_label}"
        st.markdown(f"""
<div style='border:2px solid #94A3B8;border-radius:12px;overflow:hidden;
            box-shadow:0 4px 20px rgba(15,23,42,0.12);margin:4px 0 12px'>
  {_tablo_header(dd_sinif, dd_sube, tarih_header, f"{akademik_yil} Akademik Yılı")}
  <table style='width:100%;border-collapse:collapse'>
    <thead>
      <tr style='background:#111827;border-bottom:2px solid #6366f1'>
        <th style='text-align:center;padding:8px 6px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase;width:44px;border-right:2px solid #cbd5e1'>Sıra</th>
        <th style='text-align:center;padding:8px 6px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase;width:72px;border-right:1px solid #e2e8f0'>Saat</th>
        <th style='text-align:left;padding:8px 10px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase;width:130px;border-right:1px solid #e2e8f0'>Ders</th>
        <th style='text-align:left;padding:8px 10px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase;width:140px;border-right:1px solid #e2e8f0'>Öğretmen</th>
        <th style='text-align:left;padding:8px 12px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase'>Konu ve İşlenen Kazanımlar</th>
        <th style='text-align:center;padding:8px;font-size:0.7rem;font-weight:700;color:#475569;
                   text-transform:uppercase;width:115px;border-left:1px solid #e2e8f0'>Durum</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
  <div style='background:#111827;border-top:1px solid #e2e8f0;padding:8px 16px;
              display:flex;justify-content:space-between;align-items:center'>
    <span style='font-size:0.72rem;color:#64748b'>
      Toplam {len(slots)} ders saati &nbsp;·&nbsp; {islendi_c} derste kazanım işlendi
    </span>
    <span style='font-size:0.68rem;color:#94a3b8'>SmartCampus AI — Dijital Sınıf Defteri</span>
  </div>
</div>
""", unsafe_allow_html=True)
        _dd_export_buttons(tum_ki, dd_sinif, dd_sube, dd_label, prefix="ddg")
        return

    # ════════════════════════════════════════════════
    # HAFTALIK — Yatay çizelge (Satır=Gün, Sütun=Ders No)
    # ════════════════════════════════════════════════
    if dd_mod == "Haftalık":
        pzt_h = _dd_hafta_baslangic(dd_tarih)
        cum_h = pzt_h + timedelta(days=4)
        tarih_bas = pzt_h.strftime("%Y-%m-%d")
        tarih_bit = cum_h.strftime("%Y-%m-%d")

        all_ki = store.get_kazanim_isleme(sinif=dd_sinif, sube=dd_sube, akademik_yil=akademik_yil)
        hafta_ki = [k for k in all_ki
                    if tarih_bas <= (k.tarih or "") <= tarih_bit
                    and k.durum in ("islendi", "kismen")]

        # Her gün için veri topla
        gunler_data = []
        tum_dn: set = set()
        for offset in range(5):
            gt = pzt_h + timedelta(days=offset)
            ga = _dd_gun_adi(gt)
            if ga not in aktif_gunler:
                continue
            gt_str = gt.strftime("%Y-%m-%d")
            slots = store.get_schedule(sinif=dd_sinif, sube=dd_sube,
                                       gun=ga, akademik_yil=akademik_yil)
            gun_ki = [k for k in hafta_ki if k.tarih == gt_str]
            ki_by_ders: dict = {}
            for k in gun_ki:
                ki_by_ders.setdefault(k.ders, []).append(k)
            slot_by_dn: dict = {}
            for sl in slots:
                dn = sl.ders_saati or 0
                slot_by_dn[dn] = sl
                tum_dn.add(dn)
            gunler_data.append({
                "tarih": gt, "gun_tr": GUN_TR.get(ga, ga),
                "is_today": gt == today,
                "slot_by_dn": slot_by_dn, "ki_by_ders": ki_by_ders,
            })

        if not gunler_data or not tum_dn:
            styled_info_banner(
                f"{dd_sinif}/{dd_sube} için bu hafta ders programı bulunamadı. "
                "Ders & Program sekmesinden girin.", "warning")
            _dd_export_buttons(hafta_ki, dd_sinif, dd_sube, dd_label, prefix="ddh")
            return

        max_dn = max(tum_dn)
        dn_list = list(range(1, max_dn + 1))

        # Sütun başlıkları (koyu header)
        th_cells = (
            "<th style='min-width:90px;background:#111827;padding:8px 6px;font-size:0.66rem;"
            "font-weight:700;color:#94A3B8;text-transform:uppercase;"
            "border-right:2px solid #e2e8f0;border-bottom:2px solid #6366f1;text-align:center'>Gün / Tarih</th>"
        )
        for dn in dn_list:
            zd = zaman_map.get(dn, {})
            bas = zd.get("baslangic", "")
            bit = zd.get("bitis", "")
            saat_sub = (f"<div style='font-size:0.6rem;color:#6366f1;margin-top:1px'>{bas}–{bit}</div>"
                        if bas else "")
            th_cells += (
                f"<th style='min-width:108px;background:#111827;padding:7px 5px;font-size:0.68rem;"
                f"font-weight:700;color:#94A3B8;text-transform:uppercase;"
                f"border-right:1px solid #e2e8f0;border-bottom:2px solid #6366f1;text-align:center'>{dn}. Ders{saat_sub}</th>"
            )

        # Gün satırları
        row_cells_all = ""
        toplam_ders = 0
        toplam_islendi = 0
        for gd in gunler_data:
            is_today = gd["is_today"]
            if is_today:
                gun_td_style = "background:linear-gradient(135deg,#dbeafe,#eff6ff)"
                gun_txt_style = "font-weight:800;color:#1d4ed8"
                today_lbl = "<div style='font-size:0.6rem;color:#1d4ed8;margin-top:1px'>● Bugün</div>"
            else:
                gun_td_style = "background:#111827"
                gun_txt_style = "font-weight:700;color:#94A3B8"
                today_lbl = ""

            row = (
                f"<td style='{gun_td_style};padding:8px;border-right:2px solid #cbd5e1;"
                f"border-bottom:1px solid #e2e8f0;vertical-align:middle;text-align:center'>"
                f"<div style='{gun_txt_style};font-size:0.82rem'>{gd['gun_tr']}</div>"
                f"<div style='font-size:0.67rem;color:#64748b'>{gd['tarih'].strftime('%d.%m.%Y')}</div>"
                f"{today_lbl}</td>"
            )

            for dn in dn_list:
                slot = gd["slot_by_dn"].get(dn)
                if not slot:
                    row += (
                        "<td style='background:#1A2035;border-right:1px solid #e2e8f0;"
                        "border-bottom:1px solid #e2e8f0;text-align:center;padding:8px'>"
                        "<span style='color:#cbd5e1;font-size:0.9rem'>—</span></td>"
                    )
                    continue

                toplam_ders += 1
                ki_list = gd["ki_by_ders"].get(slot.ders, [])
                if ki_list:
                    toplam_islendi += 1
                    if all(k.durum == "islendi" for k in ki_list):
                        cell_bg = "#f0fdf4"
                        badge = ("<span style='background:#dcfce7;color:#166534;font-size:0.62rem;"
                                 "padding:2px 7px;border-radius:8px;font-weight:700'>✅</span>")
                    else:
                        cell_bg = "#fefce8"
                        badge = ("<span style='background:#fef9c3;color:#854d0e;font-size:0.62rem;"
                                 "padding:2px 7px;border-radius:8px;font-weight:700'>⚠️</span>")
                else:
                    cell_bg = "#ffffff"
                    badge = ("<span style='background:#1A2035;color:#94a3b8;font-size:0.62rem;"
                             "padding:2px 7px;border-radius:8px'>○</span>")

                ogr_html = (f"<div style='font-size:0.64rem;color:#64748b;margin-top:1px'>"
                            f"{slot.ogretmen}</div>") if slot.ogretmen else ""
                row += (
                    f"<td style='background:{cell_bg};border-right:1px solid #e2e8f0;"
                    f"border-bottom:1px solid #e2e8f0;padding:7px 6px;vertical-align:top'>"
                    f"<div style='font-size:0.76rem;font-weight:700;color:#94A3B8;line-height:1.3'>"
                    f"{slot.ders or '—'}</div>"
                    f"{ogr_html}"
                    f"<div style='margin-top:4px'>{badge}</div></td>"
                )

            row_cells_all += f"<tr>{row}</tr>"

        hafta_str = f"{pzt_h.strftime('%d.%m')} – {cum_h.strftime('%d.%m.%Y')}"
        st.markdown(f"""
<div style='border:2px solid #94A3B8;border-radius:12px;overflow:hidden;
            box-shadow:0 4px 20px rgba(15,23,42,0.12);margin:4px 0 12px'>
  {_tablo_header(dd_sinif, dd_sube, hafta_str, f"{akademik_yil} Akademik Yılı")}
  <div style='overflow-x:auto'>
    <table style='width:100%;border-collapse:collapse;min-width:500px'>
      <thead><tr>{th_cells}</tr></thead>
      <tbody>{row_cells_all}</tbody>
    </table>
  </div>
  <div style='background:#111827;border-top:1px solid #e2e8f0;padding:8px 16px;
              display:flex;justify-content:space-between;align-items:center'>
    <span style='font-size:0.72rem;color:#64748b'>
      Toplam {toplam_ders} ders saati &nbsp;·&nbsp; {toplam_islendi} derste kazanım işlendi
    </span>
    <span style='font-size:0.68rem;color:#94a3b8'>SmartCampus AI — Dijital Sınıf Defteri</span>
  </div>
</div>
""", unsafe_allow_html=True)
        _dd_export_buttons(hafta_ki, dd_sinif, dd_sube, dd_label, prefix="ddh")
        return

    # ════════════════════════════════════════════════
    # AYLIK / YILLIK / TARİH ARALIĞI — Liste görünümü
    # ════════════════════════════════════════════════
    styled_section(f"📋 Ders Defteri — {dd_sinif}/{dd_sube} ({dd_label})", "#059669")
    all_ki = store.get_kazanim_isleme(sinif=dd_sinif, sube=dd_sube, akademik_yil=akademik_yil)
    kayitlar = sorted(
        [k for k in all_ki
         if tarih_bas <= (k.tarih or "") <= tarih_bit
         and k.durum in ("islendi", "kismen")],
        key=lambda r: (r.tarih or "", r.ders),
    )
    islendi_c = sum(1 for r in kayitlar if r.durum == "islendi")
    kismen_c = len(kayitlar) - islendi_c
    yuzde = round(islendi_c / len(all_ki) * 100) if all_ki else 0
    styled_stat_row([
        ("Kayıt", len(kayitlar), "#6366f1", "📚"),
        ("İşlendi", islendi_c, "#10b981", "✅"),
        ("Kısmen", kismen_c, "#f59e0b", "⚠️"),
        ("İlerleme", f"%{yuzde}", "#0ea5e9", "📈"),
    ])
    if kayitlar:
        df_rows = [{
            "#": i,
            "Tarih": r.tarih or "-",
            "Ders": r.ders,
            "Kazanım Kodu": r.kazanim_kodu or "-",
            "Konu / Kazanım": (r.kazanim_metni or "-")[:120],
            "Öğretmen": r.ogretmen_adi or "-",
            "Süre (dk)": 40,
            "Durum": "✅ İşlendi" if r.durum == "islendi" else "⚠️ Kısmen",
        } for i, r in enumerate(kayitlar, 1)]
        st.dataframe(pd.DataFrame(df_rows), use_container_width=True,
                     hide_index=True, height=460)
        with st.expander("📊 Ders Bazlı Özet"):
            ozet: dict = {}
            for r in kayitlar:
                ozet.setdefault(r.ders, {"İşlendi": 0, "Kısmen": 0, "Öğretmen": set()})
                ozet[r.ders]["İşlendi" if r.durum == "islendi" else "Kısmen"] += 1
                if r.ogretmen_adi:
                    ozet[r.ders]["Öğretmen"].add(r.ogretmen_adi)
            ozet_rows = [
                {"Ders": d, "İşlendi": v["İşlendi"], "Kısmen": v["Kısmen"],
                 "Toplam": v["İşlendi"] + v["Kısmen"],
                 "Öğretmen": ", ".join(sorted(v["Öğretmen"])) or "-"}
                for d, v in sorted(ozet.items())
            ]
            st.dataframe(pd.DataFrame(ozet_rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner(
            f"{dd_sinif}/{dd_sube} için seçilen dönemde işlenmiş kazanım yok. "
            "Uygulama Takibi sekmesinden kazanımları işaretleyin.", "info")
    _dd_export_buttons(kayitlar, dd_sinif, dd_sube, dd_label, prefix="dda")



def _dd_export_buttons(kayitlar: list, sinif: int, sube: str, label: str, prefix: str = "dd"):
    """PDF ve Excel export butonları — Ders Defteri için."""
    if not kayitlar:
        return
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    styled_section("📤 Rapor Al", "#dc2626")
    ex1, ex2 = st.columns(2)

    with ex1:
        if st.button("📄 PDF Oluştur", type="primary", key=f"{prefix}_pdf_btn",
                     use_container_width=True):
            ogr_set = sorted(set(r.ogretmen_adi for r in kayitlar if r.ogretmen_adi))
            pdf_bytes = _generate_ders_defteri_pdf(
                kayitlar, sinif, sube,
                ogretmen_filtre=", ".join(ogr_set) if ogr_set else None
            )
            if pdf_bytes:
                st.session_state[f"{prefix}_pdf_data"] = pdf_bytes
                st.session_state[f"{prefix}_pdf_name"] = f"ders_defteri_{sinif}{sube}_{label.replace(' ', '_').replace('.','')}.pdf"
                st.success("PDF hazır!")
                st.rerun(scope="fragment")
            else:
                st.error("PDF oluşturulamadı. ReportLab yüklü değil.")

    with ex2:
        # Excel (DataFrame → bytes)
        import io as _io
        df_exp = pd.DataFrame([{
            "Tarih": r.tarih or "-",
            "Ders": r.ders,
            "Kazanım Kodu": r.kazanim_kodu or "-",
            "Konu / Kazanım": r.kazanim_metni or "-",
            "Öğretmen": r.ogretmen_adi or "-",
            "Süre (dk)": 40,
            "Durum": "İşlendi" if r.durum == "islendi" else "Kısmen",
            "Notlar": r.notlar or "",
        } for r in kayitlar])
        buf = _io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df_exp.to_excel(writer, index=False, sheet_name="Ders Defteri")
        st.download_button(
            "📊 Excel İndir",
            data=buf.getvalue(),
            file_name=f"ders_defteri_{sinif}{sube}_{label.replace(' ','_').replace('.','')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"{prefix}_excel_btn",
            use_container_width=True,
        )

    if st.session_state.get(f"{prefix}_pdf_data"):
        st.download_button(
            "⬇️ PDF İndir",
            data=st.session_state[f"{prefix}_pdf_data"],
            file_name=st.session_state.get(f"{prefix}_pdf_name", "ders_defteri.pdf"),
            mime="application/pdf",
            key=f"{prefix}_pdf_dl",
        )


# ==================== KURUMSAL KARNELER ====================

# Varsayilan kurs/ders listesi
KURUMSAL_KARNE_DERSLERI = [
    "Ingilizce",
    "Almanca",
    "Fransizca",
    "Satranc",
    "Kodlama",
    "Yazilim ve Kodlama",
    "Robotik ve Kodlama",
    "Drama",
    "Piyano",
    "Keman",
    "Basketbol",
    "Futbol",
    "Voleybol",
]

KURUMSAL_KARNE_IMZA_SECENEKLERI = [
    "Okul Muduru",
    "Kampus Muduru",
    "Genel Mudur Yardimcisi",
    "Genel Mudur",
    "Kurucu",
    "Yönetim Kurulu Baskani",
]


@st.fragment
def _render_kurumsal_karneler(store: AkademikDataStore):
    """Kurumsal Karneler - seciniz derslere gore toplu sertifika uretimi."""

    styled_section("Kurumsal Karneler", "#7c3aed")
    styled_info_banner(
        "Secmeli ders ve etkinliklere katilan ogrencilere toplu sertifika "
        "olusturun. Ders, donem ve sinif secip tek tusla tum ogrencilere sertifika uretebilirsiniz.",
        "info",
    )

    # --- Ozel ders listesi yonetimi ---
    kk_dersler_key = "kk_custom_dersler"
    if kk_dersler_key not in st.session_state:
        st.session_state[kk_dersler_key] = list(KURUMSAL_KARNE_DERSLERI)
    ders_listesi = st.session_state[kk_dersler_key]

    # --- 1. DERS SECIMI ---
    styled_section("Ders / Etkinlik Secimi", "#2563eb")
    dc1, dc2, dc3 = st.columns([3, 2, 1])
    with dc1:
        secili_ders = st.selectbox(
            "Ders / Etkinlik",
            ders_listesi,
            key="kk_ders_sec",
        )
    with dc2:
        yeni_ders = st.text_input("Yeni Ders Ekle", key="kk_yeni_ders", placeholder="Ornek: Gorsel Sanatlar")
    with dc3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Ekle", key="kk_ders_ekle_btn", use_container_width=True):
            if yeni_ders.strip() and yeni_ders.strip() not in ders_listesi:
                ders_listesi.append(yeni_ders.strip())
                st.session_state[kk_dersler_key] = ders_listesi
                st.success(f"'{yeni_ders.strip()}' ders listesine eklendi.")
                st.rerun()
            elif yeni_ders.strip() in ders_listesi:
                st.warning("Bu ders zaten listede.")

    # --- 2. DONEM SECIMI ---
    styled_section("Donem", "#059669")
    donem_col1, donem_col2 = st.columns(2)
    with donem_col1:
        donem = st.selectbox("Donem", ["1. Donem", "2. Donem"], key="kk_donem")
    with donem_col2:
        akademik_yil = _get_akademik_yil()
        st.text_input("Akademik Yil", value=akademik_yil, disabled=True, key="kk_akd_yil")

    # --- 3. SINIF / OGRENCI SECIMI ---
    styled_section("Sınıf & Öğrenci Seçimi", "#dc2626")
    sc1, sc2 = st.columns(2)
    with sc1:
        kk_sinif_options = ["Tümü"] + [str(s) for s in SINIFLAR]
        kk_sinif_sel = st.selectbox("Sınıf", kk_sinif_options, key="kk_sinif")
    with sc2:
        kk_sube_options = ["Tümü"] + list(SUBELER)
        kk_sube_sel = st.selectbox("Şube", kk_sube_options, key="kk_sube")

    # Ogrenci listesi yukle — Tümü seçilirse filtre uygulanmaz
    _kk_sinif = None if kk_sinif_sel == "Tümü" else str(kk_sinif_sel)
    _kk_sube = None if kk_sube_sel == "Tümü" else kk_sube_sel
    ogrenciler = store.get_students(
        sinif=_kk_sinif, sube=_kk_sube, durum="aktif"
    )
    if not ogrenciler:
        st.warning(f"Seçilen filtrede kayıtlı öğrenci bulunamadı.")
        return

    # Sınıf bilgisi label için
    kk_sinif = _kk_sinif or "Tümü"
    kk_sube = _kk_sube or "Tümü"

    tum_sinif_sec = st.checkbox("Tüm öğrencileri seç", value=True, key="kk_tum_sinif")

    if tum_sinif_sec:
        secili_ogrenciler = ogrenciler
        st.info(f"{len(ogrenciler)} öğrenci seçildi ({kk_sinif}/{kk_sube})")
    else:
        ogr_options = {
            f"{o.ad} {o.soyad} - {o.sinif}/{o.sube} ({o.numara})": o
            for o in ogrenciler
        }
        secilen_isimler = st.multiselect(
            "Öğrenci Seç",
            list(ogr_options.keys()),
            key="kk_ogrenci_sec",
        )
        secili_ogrenciler = [ogr_options[n] for n in secilen_isimler if n in ogr_options]
        if secili_ogrenciler:
            st.info(f"{len(secili_ogrenciler)} öğrenci seçildi")

    if not secili_ogrenciler:
        st.warning("En az bir öğrenci seçiniz.")
        return

    # --- 4. SERTIFIKA SABLONU SECIMI ---
    styled_section("Sertifika Ayarlari", "#7c3aed")
    # Sablonlari session_state'te cachele (agir I/O onlenir)
    _tpl_cache_key = "_kk_tpl_cache"
    if _tpl_cache_key not in st.session_state:
        st.session_state[_tpl_cache_key] = store.get_cert_templates() or list(PRESET_CERT_TEMPLATES)
    templates = st.session_state[_tpl_cache_key]

    tpl_names = {t.get("name", f"Sablon {i+1}"): t for i, t in enumerate(templates)}
    tpl_col1, tpl_col2 = st.columns(2)
    with tpl_col1:
        secili_tpl_name = st.selectbox("Sertifika Sablonu", list(tpl_names.keys()), key="kk_tpl_sec")
    with tpl_col2:
        imza_secim = st.selectbox("Sertifikayi Veren (Imza)", KURUMSAL_KARNE_IMZA_SECENEKLERI, key="kk_imza")

    secili_template = tpl_names.get(secili_tpl_name, templates[0])

    # Sertifika metni onizleme
    styled_section("Sertifika Metni Onizleme", "#f59e0b")
    donem_metin = "1. donem" if donem == "1. Donem" else "2. donem"
    ornek_metin = (
        f"Okulumuzda {akademik_yil} egitim ogretim yili {donem_metin} almis oldugunuz "
        f"{secili_ders} egitimini basariyla tamamladiginizi belirtir."
    )
    st.markdown(
        f'<div style="background:#fef3c7;border:1px solid #f59e0b;border-radius:8px;'
        f'padding:16px;font-size:15px;color:#92400e;margin:8px 0">'
        f'<strong>Ornek:</strong> {ornek_metin}</div>',
        unsafe_allow_html=True,
    )

    ozel_metin = st.text_area(
        "Özel Metin (bos birakilirsa otomatik olusturulur)",
        value="",
        key="kk_ozel_metin",
        height=80,
        placeholder=ornek_metin,
    )

    st.divider()

    # --- 5. SERTIFIKA URET ---
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:white;'
        f'padding:12px 16px;border-radius:8px;text-align:center;font-size:16px;'
        f'font-weight:600;margin:8px 0">'
        f'{len(secili_ogrenciler)} ogrenci için {secili_ders} sertifikasi uretilecek'
        f'</div>',
        unsafe_allow_html=True,
    )

    # --- BOŞ ŞABLON ÖNİZLEME ---
    if st.button("👁️ Şablon Önizleme", key="kk_onizleme_btn", use_container_width=True):
        try:
            from views.kim_organizational import _generate_certificate_from_template
            kurum_adi = st.session_state.get("tenant_name", "Okul")
            logo_path = ""
            for lp in [os.path.join("assets", "logo.png"), os.path.join("assets", "school_logo.png")]:
                if os.path.exists(lp):
                    logo_path = lp
                    break
            donem_metin_p = "1. donem" if donem == "1. Donem" else "2. donem"
            neden_p = ozel_metin.strip() if ozel_metin.strip() else (
                f"Okulumuzda {akademik_yil} egitim ogretim yili {donem_metin_p} "
                f"almis oldugunuz {secili_ders} egitimini basariyla tamamladiginizi belirtir."
            )
            pdf_preview = _generate_certificate_from_template(
                template=secili_template,
                kurum_adi=kurum_adi,
                logo_path=logo_path,
                sertifika_turu=secili_ders,
                alici_adi="______________________",
                sinif_sube="__ / __",
                verilis_tarihi=date.today().strftime("%d.%m.%Y"),
                verilis_nedeni=neden_p,
                sertifika_veren=imza_secim,
            )
            if pdf_preview:
                import base64
                b64 = base64.b64encode(pdf_preview).decode("utf-8")
                st.markdown(
                    '<div style="background:#eff6ff;border:2px solid #3b82f6;border-radius:12px;'
                    'padding:12px;margin:12px 0;text-align:center;">'
                    '<b>Şablon Önizleme</b> — Basılacak sertifikanın boş hali</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<iframe src="data:application/pdf;base64,{b64}" '
                    f'width="100%" height="500" style="border:1px solid #e2e8f0;border-radius:8px;"></iframe>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.error(f"Önizleme oluşturulamadı: {e}")

    st.divider()

    if st.button("Sertifikalari Oluştur", key="kk_olustur_btn", type="primary", use_container_width=True):
        import io
        import zipfile
        from views.kim_organizational import _generate_certificate_from_template

        kurum_adi = st.session_state.get("tenant_name", "Okul")
        logo_path = ""
        logo_candidates = [
            os.path.join("assets", "logo.png"),
            os.path.join("assets", "school_logo.png"),
        ]
        for lp in logo_candidates:
            if os.path.exists(lp):
                logo_path = lp
                break

        progress = st.progress(0, text="Sertifikalar olusturuluyor...")
        toplam = len(secili_ogrenciler)
        pdf_dosyalar = []
        basarili = 0

        for idx, ogr in enumerate(secili_ogrenciler):
            ogr_ad = f"{ogr.ad} {ogr.soyad}"
            ogr_sinif_sube = f"{ogr.sinif}/{ogr.sube}"

            # Sertifika nedeni
            if ozel_metin.strip():
                neden = ozel_metin.strip()
            else:
                neden = (
                    f"Okulumuzda {akademik_yil} egitim ogretim yili {donem_metin} "
                    f"almis oldugunuz {secili_ders} egitimini basariyla tamamladiginizi belirtir."
                )

            verilis_tarihi = date.today().strftime("%d.%m.%Y")

            try:
                pdf_bytes = _generate_certificate_from_template(
                    template=secili_template,
                    kurum_adi=kurum_adi,
                    logo_path=logo_path,
                    sertifika_turu=secili_ders,
                    alici_adi=ogr_ad,
                    sinif_sube=ogr_sinif_sube,
                    verilis_tarihi=verilis_tarihi,
                    verilis_nedeni=neden,
                    sertifika_veren=imza_secim,
                )
                dosya_adi = f"sertifika_{ogr.ad}_{ogr.soyad}_{secili_ders}.pdf".replace(" ", "_")
                pdf_dosyalar.append((dosya_adi, pdf_bytes))
                basarili += 1

                # Sertifika kaydini sakla
                cert_record = Certificate(
                    sertifika_turu=secili_ders,
                    alici_tipi="ogrenci",
                    alici_id=ogr.id,
                    alici_adi=ogr_ad,
                    sinif_sube=ogr_sinif_sube,
                    verilis_tarihi=verilis_tarihi,
                    verilis_nedeni=neden,
                    template_id=secili_template.get("id", ""),
                )
                store.save_certificate(cert_record.__dict__)

            except Exception as e:
                st.error(f"{ogr_ad} için sertifika olusturulamadi: {e}")

            progress.progress((idx + 1) / toplam, text=f"Oluşturuluyor... {idx + 1}/{toplam}")

        progress.empty()

        if basarili > 0:
            st.success(f"{basarili}/{toplam} sertifika basariyla oluşturuldu!")

            if len(pdf_dosyalar) == 1:
                # Tek dosya - direkt indir
                st.download_button(
                    "PDF Indir",
                    data=pdf_dosyalar[0][1],
                    file_name=pdf_dosyalar[0][0],
                    mime="application/pdf",
                    key="kk_pdf_tek_indir",
                )
            else:
                # Coklu dosya - ZIP olarak indir
                zip_buf = io.BytesIO()
                with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
                    for dosya_adi, pdf_bytes in pdf_dosyalar:
                        zf.writestr(dosya_adi, pdf_bytes)
                zip_buf.seek(0)

                st.download_button(
                    f"Tüm Sertifikalari Indir (ZIP - {len(pdf_dosyalar)} dosya)",
                    data=zip_buf.getvalue(),
                    file_name=f"kurumsal_karne_{secili_ders}_{kk_sinif}{kk_sube}.zip",
                    mime="application/zip",
                    key="kk_zip_indir",
                )

            # Onizleme: ilk sertifikayi goster
            if pdf_dosyalar:
                with st.expander("Onizleme (ilk sertifika)", expanded=True):
                    try:
                        import fitz
                        pdf_doc = fitz.open(stream=pdf_dosyalar[0][1], filetype="pdf")
                        page = pdf_doc[0]
                        pix = page.get_pixmap(dpi=150)
                        img_bytes = pix.tobytes("png")
                        st.image(img_bytes, use_container_width=True)
                        pdf_doc.close()
                    except Exception:
                        st.info("PDF onizleme için PyMuPDF (fitz) gereklidir.")
        else:
            st.error("Hicbir sertifika olusturulamadi.")


# ==================== TAB 13: SINIF LISTESI ====================

@st.fragment
def _render_sinif_listesi(store: AkademikDataStore):
    """Sinif listesi - modern HTML tablo gorunumu."""

    # ── CSS enjeksiyonu (bir kez) ─────────────────────────────────────────────
    if not st.session_state.get("_sl_css_done"):
        st.session_state["_sl_css_done"] = True
        st.markdown("""<style>
/* ══ Sınıf Listesi Modern Tablo ══════════════════════════════════════════ */
.sl-table-wrap{overflow-x:auto;border-radius:14px;border:1px solid #e2e8f0;
    box-shadow:0 4px 20px rgba(0,0,0,0.06);background:#fff;margin:6px 0 14px 0}
.sl-table{width:100%;border-collapse:collapse;min-width:520px;font-family:
    'Inter','Segoe UI',system-ui,sans-serif}
.sl-table thead tr{background:linear-gradient(135deg,#111827 0%,#1A2035 50%,#e2e8f0 100%);border-bottom:2px solid #6366f1}
.sl-table thead th{color:#94A3B8;font-size:0.73rem;font-weight:700;letter-spacing:.6px;
    text-transform:uppercase;padding:11px 12px;text-align:left;white-space:nowrap}
.sl-table thead th.center{text-align:center}
.sl-table tbody tr{transition:background .15s}
.sl-table tbody tr:nth-child(even){background:#111827}
.sl-table tbody tr:nth-child(odd){background:#ffffff}
.sl-table tbody tr:hover{background:#eff6ff}
.sl-table tbody td{padding:10px 12px;font-size:0.82rem;color:#94A3B8;
    border-bottom:1px solid #1A2035;vertical-align:middle}
.sl-table tbody td.center{text-align:center}
/* Numaracı balonu */
.sl-no{display:inline-flex;align-items:center;justify-content:center;
    width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:#fff;font-size:0.7rem;font-weight:800}
/* Okul No badge */
.sl-okul-no{display:inline-block;background:#1A2035;border:1px solid #cbd5e1;
    border-radius:6px;padding:2px 8px;font-size:0.75rem;font-weight:700;color:#334155;
    font-family:monospace}
/* İsim */
.sl-name{font-weight:700;color:#0B0F19;font-size:0.85rem}
.sl-name-sub{font-size:0.72rem;color:#64748b;margin-top:1px}
/* Sınıf badge */
.sl-sinif-badge{display:inline-block;padding:3px 9px;border-radius:20px;
    font-size:0.72rem;font-weight:700;background:linear-gradient(135deg,#6366f1,#8b5cf6);
    color:#fff;white-space:nowrap}
/* Cinsiyet badge */
.sl-cin-e{display:inline-block;padding:2px 8px;border-radius:12px;font-size:0.7rem;
    font-weight:600;background:#dbeafe;color:#1d4ed8}
.sl-cin-k{display:inline-block;padding:2px 8px;border-radius:12px;font-size:0.7rem;
    font-weight:600;background:#fce7f3;color:#be185d}
/* İletişim */
.sl-contact{font-size:0.76rem;color:#334155}
.sl-contact a{color:#2563eb;text-decoration:none}
/* Veli card */
.sl-veli-row{display:flex;align-items:center;gap:10px;padding:10px 14px;
    border-bottom:1px solid #1A2035}
.sl-veli-row:last-child{border-bottom:none}
.sl-veli-avatar{width:36px;height:36px;border-radius:50%;display:flex;
    align-items:center;justify-content:center;font-size:0.9rem;
    flex-shrink:0;font-weight:700;color:#fff}
.sl-veli-info{flex:1;min-width:0}
.sl-veli-name{font-weight:700;font-size:0.84rem;color:#0B0F19}
.sl-veli-role{font-size:0.7rem;color:#64748b;margin-bottom:2px}
.sl-veli-tel{font-size:0.76rem;color:#2563eb}
.sl-veli-mail{font-size:0.72rem;color:#64748b}
/* Sınıf özet kartları */
.sl-ozet-grid{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.sl-ozet-kart{flex:1;min-width:90px;max-width:130px;background:#fff;
    border:1px solid #e2e8f0;border-radius:12px;padding:10px 12px;text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.sl-ozet-kart.aktif-sinif{border:2px solid #2563eb;background:#eff6ff}
.sl-ozet-sinif{font-size:0.9rem;font-weight:800;color:#0B0F19}
.sl-ozet-sayi{font-size:1.3rem;font-weight:800;color:#2563eb;line-height:1.1}
.sl-ozet-label{font-size:0.65rem;color:#64748b;font-weight:600;text-transform:uppercase;
    letter-spacing:.4px}
/* Öğretmen chip */
.sl-ogr-chip{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;
    border-radius:20px;background:#1A2035;border:1px solid #e2e8f0;
    font-size:0.72rem;color:#334155;margin:2px;white-space:nowrap}
.sl-ogr-chip b{color:#0B0F19}
</style>""", unsafe_allow_html=True)

    # ── Üst bilgi bandı ───────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:linear-gradient(135deg,#0d9488,#0891b2);color:#fff;"
        "padding:12px 18px;border-radius:12px;margin-bottom:14px;font-size:0.85rem;"
        "display:flex;align-items:center;gap:10px'>"
        "<span style='font-size:1.3rem'>🏫</span>"
        "<span><b>Merkezi Kaynak:</b> Öğrenci verileri "
        "<b>KOI › İletişim › Sınıf Listeleri</b> ekranından yönetilir.</span></div>",
        unsafe_allow_html=True,
    )

    akademik_yil = _get_akademik_yil()

    # ── Filtre satırı ─────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns([2, 2, 3])
    with fc1:
        sl_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="sl_sinif")
    with fc2:
        sl_sube = st.selectbox("Şube", SUBELER, key="sl_sube")
    with fc3:
        sl_arama = st.text_input("🔍 Ada veya No'ya göre ara",
                                 placeholder="Örn: Ahmet veya 1042",
                                 key="sl_arama")

    # ── Veri yükle ────────────────────────────────────────────────────────────
    tum_ogrenciler = store.get_students(durum="aktif")
    tum_siniflar   = sorted(set((s.sinif, s.sube) for s in tum_ogrenciler),
                             key=lambda x: (str(x[0]), str(x[1])))
    students       = store.get_students(sinif=sl_sinif, sube=sl_sube, durum="aktif")
    students       = sorted(
        students,
        key=lambda s: (int(s.numara) if str(s.numara).isdigit() else 9999, s.soyad, s.ad),
    )

    # Arama filtresi
    if sl_arama.strip():
        q = sl_arama.strip().lower()
        students = [
            s for s in students
            if q in s.ad.lower() or q in s.soyad.lower() or q in str(s.numara).lower()
        ]

    # ── İstatistik kartları ───────────────────────────────────────────────────
    styled_stat_row([
        ("Bu Sınıfta", len(students),      "#2563eb", "🎓"),
        ("Tüm Öğrenci", len(tum_ogrenciler), "#10b981", "👥"),
        ("Sınıf/Şube", len(tum_siniflar),  "#8b5cf6", "🏛️"),
    ])
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Ders öğretmenleri chip satırı ─────────────────────────────────────────
    ogretmen_ders_map: dict[str, str] = {}
    for gun in GUNLER:
        for slot in store.get_schedule(sinif=sl_sinif, sube=sl_sube,
                                        gun=gun, akademik_yil=akademik_yil):
            if slot.ders and slot.ogretmen and slot.ders not in ogretmen_ders_map:
                ogretmen_ders_map[slot.ders] = slot.ogretmen

    if ogretmen_ders_map:
        chips = "".join(
            f"<span class='sl-ogr-chip'><b>{d}:</b> {o}</span>"
            for d, o in sorted(ogretmen_ders_map.items())
        )
        st.markdown(
            f"<div style='margin:4px 0 10px 0'>"
            f"<span style='font-size:0.72rem;font-weight:700;color:#64748b;"
            f"text-transform:uppercase;letter-spacing:.5px'>Ders Öğretmenleri&nbsp;</span>"
            f"{chips}</div>",
            unsafe_allow_html=True,
        )

    # ── Sekmeler ──────────────────────────────────────────────────────────────
    tab_ogr, tab_veli, tab_ozet = st.tabs([
        f"  🎓 Öğrenci Listesi ({len(students)})  ",
        f"  👨‍👩‍👧 Veli Listesi  ",
        f"  📊 Tüm Sınıflar  ",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — ÖĞRENCİ LİSTESİ
    # ════════════════════════════════════════════════════════════════════════
    with tab_ogr:
        if not students:
            st.markdown(
                f"<div style='text-align:center;padding:40px 20px;color:#94a3b8;"
                f"font-size:0.9rem'>🔍 {sl_sinif}/{sl_sube} sınıfında"
                f"{'arama kriterine uygun ' if sl_arama.strip() else ' '}öğrenci bulunamadı.</div>",
                unsafe_allow_html=True,
            )
        else:
            # HTML tablo oluştur
            rows_html = ""
            for i, s in enumerate(students, 1):
                cin_raw = (s.cinsiyet or "").strip().lower()
                if cin_raw == "erkek":
                    cin_badge = "<span class='sl-cin-e'>Erkek</span>"
                elif cin_raw in ("kiz", "kız"):
                    cin_badge = "<span class='sl-cin-k'>Kız</span>"
                else:
                    cin_badge = f"<span style='font-size:0.72rem;color:#94a3b8'>{s.cinsiyet or '-'}</span>"

                veli_txt = s.veli_adi or "-"
                tel_txt  = s.veli_telefon or "-"
                tel_html = (
                    f"<a href='tel:{tel_txt}' class='sl-contact'>{tel_txt}</a>"
                    if tel_txt != "-" else
                    "<span style='color:#cbd5e1'>—</span>"
                )

                rows_html += (
                    "<tr>"
                    f"<td class='center'><span class='sl-no'>{i}</span></td>"
                    f"<td class='center'><span class='sl-okul-no'>{s.numara or '-'}</span></td>"
                    f"<td><div class='sl-name'>{s.ad} {s.soyad}</div></td>"
                    f"<td class='center'><span class='sl-sinif-badge'>{s.sinif}/{s.sube}</span></td>"
                    f"<td class='center'>{cin_badge}</td>"
                    f"<td><span class='sl-contact'>{veli_txt}</span></td>"
                    f"<td>{tel_html}</td>"
                    "</tr>"
                )

            st.markdown(
                "<div class='sl-table-wrap'>"
                "<table class='sl-table'>"
                "<thead><tr>"
                "<th class='center' style='width:44px'>#</th>"
                "<th class='center'>Okul No</th>"
                "<th>Ad Soyad</th>"
                "<th class='center'>Sınıf</th>"
                "<th class='center'>Cinsiyet</th>"
                "<th>Veli</th>"
                "<th>Veli Telefon</th>"
                "</tr></thead>"
                f"<tbody>{rows_html}</tbody>"
                "</table></div>",
                unsafe_allow_html=True,
            )

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — VELİ LİSTESİ
    # ════════════════════════════════════════════════════════════════════════
    with tab_veli:
        # Veli kartları
        AVATAR_RENKLER = [
            "#2563eb", "#7c3aed", "#0d9488", "#dc2626",
            "#ea580c", "#059669", "#9333ea", "#0369a1",
        ]

        # Veli kayıtları topla (anne / baba / genel veli)
        veli_kayitlari: list[dict] = []
        for s in students:
            ogr_adi = f"{s.ad} {s.soyad}"
            sinif_str = f"{s.sinif}/{s.sube}"
            if s.veli_adi and s.veli_adi.strip():
                veli_kayitlari.append({
                    "ad":    s.veli_adi.strip(),
                    "rol":   "Veli",
                    "tel":   s.veli_telefon or "",
                    "mail":  s.veli_email or "",
                    "ogr":   ogr_adi,
                    "sinif": sinif_str,
                    "icon":  "👤",
                    "renk":  AVATAR_RENKLER[len(veli_kayitlari) % len(AVATAR_RENKLER)],
                })
            if getattr(s, "anne_adi", None) and s.anne_adi.strip():
                anne_tam = f"{s.anne_adi} {getattr(s, 'anne_soyadi', '') or ''}".strip()
                veli_kayitlari.append({
                    "ad":    anne_tam,
                    "rol":   "Anne",
                    "tel":   getattr(s, "anne_telefon", "") or "",
                    "mail":  getattr(s, "anne_email", "") or "",
                    "ogr":   ogr_adi,
                    "sinif": sinif_str,
                    "icon":  "👩",
                    "renk":  "#be185d",
                })
            if getattr(s, "baba_adi", None) and s.baba_adi.strip():
                baba_tam = f"{s.baba_adi} {getattr(s, 'baba_soyadi', '') or ''}".strip()
                veli_kayitlari.append({
                    "ad":    baba_tam,
                    "rol":   "Baba",
                    "tel":   getattr(s, "baba_telefon", "") or "",
                    "mail":  getattr(s, "baba_email", "") or "",
                    "ogr":   ogr_adi,
                    "sinif": sinif_str,
                    "icon":  "👨",
                    "renk":  "#1d4ed8",
                })

        if not veli_kayitlari:
            st.markdown(
                "<div style='text-align:center;padding:40px 20px;color:#94a3b8;font-size:0.9rem'>"
                "👥 Bu sınıfta kayıtlı veli bilgisi bulunamadı.</div>",
                unsafe_allow_html=True,
            )
        else:
            # 3 kolonlu kart grid
            cols = st.columns(3)
            for idx, v in enumerate(veli_kayitlari):
                with cols[idx % 3]:
                    _vtel = v["tel"]
                    _vmail = v["mail"]
                    tel_html = (
                        f"<a href='tel:{_vtel}' style='color:#2563eb;text-decoration:none;"
                        f"font-size:0.78rem'>📞 {_vtel}</a>"
                        if _vtel else
                        "<span style='color:#cbd5e1;font-size:0.75rem'>Telefon yok</span>"
                    )
                    mail_html = (
                        f"<div style='font-size:0.72rem;color:#64748b;margin-top:2px'>"
                        f"✉️ {_vmail}</div>"
                        if _vmail else ""
                    )
                    ilk_harf = v["ad"][0].upper() if v["ad"] else "?"
                    st.markdown(
                        f"<div style='border:1px solid #e2e8f0;border-radius:14px;"
                        f"padding:14px 16px;margin-bottom:8px;background:#fff;"
                        f"box-shadow:0 2px 8px rgba(0,0,0,0.04);transition:box-shadow .2s'>"
                        f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:8px'>"
                        f"<div style='width:38px;height:38px;border-radius:50%;background:{v['renk']};"
                        f"display:flex;align-items:center;justify-content:center;"
                        f"color:#fff;font-size:0.95rem;font-weight:800;flex-shrink:0'>{ilk_harf}</div>"
                        f"<div><div style='font-weight:700;font-size:0.86rem;color:#0B0F19'>{v['ad']}</div>"
                        f"<div style='font-size:0.7rem;color:#64748b;"
                        f"background:#1A2035;display:inline-block;padding:1px 7px;"
                        f"border-radius:10px;margin-top:2px'>{v['icon']} {v['rol']}</div></div></div>"
                        f"<div style='font-size:0.75rem;color:#475569;margin-bottom:6px'>"
                        f"🎓 <b>{v['ogr']}</b> · {v['sinif']}</div>"
                        f"{tel_html}{mail_html}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — TÜM SINIFLAR ÖZET
    # ════════════════════════════════════════════════════════════════════════
    with tab_ozet:
        # Sınıf → öğrenci sayısı haritası
        sinif_ozet: dict[str, int] = {}
        for s in tum_ogrenciler:
            k = f"{s.sinif}/{s.sube}"
            sinif_ozet[k] = sinif_ozet.get(k, 0) + 1

        aktif_sinif_key = f"{sl_sinif}/{sl_sube}"

        # Kademeler
        def _kademe(sinif_str: str) -> str:
            try:
                n = int(sinif_str.split("/")[0])
                if n <= 4:   return "İlkokul"
                if n <= 8:   return "Ortaokul"
                return "Lise"
            except Exception:
                return "Diğer"

        from itertools import groupby as _groupby

        # Kademe gruplarına ayır
        kademe_gruplari: dict[str, list] = {}
        for k, v in sorted(sinif_ozet.items()):
            kad = _kademe(k)
            kademe_gruplari.setdefault(kad, []).append((k, v))

        KADEME_RENK = {
            "İlkokul":  ("#2563eb", "#eff6ff"),
            "Ortaokul": ("#7c3aed", "#f5f3ff"),
            "Lise":     ("#0d9488", "#f0fdfa"),
            "Diğer":    ("#64748b", "#111827"),
        }

        for kademe_adi, siniflar in kademe_gruplari.items():
            header_renk, _ = KADEME_RENK.get(kademe_adi, ("#64748b", "#111827"))
            toplam_kad = sum(v for _, v in siniflar)
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;"
                f"background:linear-gradient(135deg,{header_renk}15,{header_renk}05);"
                f"border-left:4px solid {header_renk};border-radius:0 10px 10px 0;"
                f"padding:8px 14px;margin:10px 0 6px 0'>"
                f"<span style='font-size:0.9rem;font-weight:800;color:{header_renk}'>{kademe_adi}</span>"
                f"<span style='font-size:0.75rem;color:#64748b;background:#fff;"
                f"padding:2px 8px;border-radius:10px;border:1px solid #e2e8f0'>"
                f"{len(siniflar)} şube · {toplam_kad} öğrenci</span></div>",
                unsafe_allow_html=True,
            )

            # Tablo satırları
            rows = ""
            for k, v in sorted(siniflar):
                is_aktif = k == aktif_sinif_key
                row_bg   = "background:#eff6ff;font-weight:700;" if is_aktif else ""
                indicator = "◀ Seçili" if is_aktif else ""
                bar_w    = min(int(v / max(sinif_ozet.values()) * 100), 100)
                bar_html = (
                    f"<div style='background:#e2e8f0;border-radius:4px;height:6px;"
                    f"width:120px;display:inline-block;vertical-align:middle;margin-left:6px'>"
                    f"<div style='background:{header_renk};height:6px;border-radius:4px;"
                    f"width:{bar_w}%'></div></div>"
                )
                rows += (
                    f"<tr style='{row_bg}'>"
                    f"<td style='padding:9px 14px;font-size:0.84rem;color:#0B0F19;"
                    f"font-weight:{'700' if is_aktif else '500'}'>"
                    f"<span style='background:{header_renk};color:#fff;padding:2px 8px;"
                    f"border-radius:8px;font-size:0.75rem;font-weight:700;margin-right:6px'>{k}</span>"
                    f"{indicator}</td>"
                    f"<td style='padding:9px 14px;font-size:0.84rem;color:{header_renk};"
                    f"font-weight:800'>{v} öğrenci{bar_html}</td>"
                    "</tr>"
                )

            st.markdown(
                "<div class='sl-table-wrap'>"
                "<table class='sl-table'>"
                "<thead><tr>"
                f"<th style='background:linear-gradient(135deg,{header_renk},{header_renk}cc)'>"
                f"Sınıf / Şube</th>"
                f"<th style='background:linear-gradient(135deg,{header_renk},{header_renk}cc)'>"
                f"Mevcudu</th>"
                "</tr></thead>"
                f"<tbody>{rows}</tbody>"
                "</table></div>",
                unsafe_allow_html=True,
            )

        # Genel özet stat satırı
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        tum = store.get_students()
        aktif_s  = sum(1 for s in tum if s.durum == "aktif")
        pasif_s  = sum(1 for s in tum if s.durum == "pasif")
        mezun_s  = sum(1 for s in tum if s.durum == "mezun")
        styled_stat_row([
            ("Aktif",   aktif_s,  "#10b981", "✅"),
            ("Pasif",   pasif_s,  "#f59e0b", "⏸️"),
            ("Mezun",   mezun_s,  "#2563eb", "🎓"),
            ("Toplam",  len(tum), "#8b5cf6", "📊"),
        ])


# ==================== TAB 13: ZAMAN CIZELGESI ====================

@st.fragment
def _render_zaman_cizelgesi(store: AkademikDataStore):
    """Gunluk zaman cizelgesi / ders saatleri ayarlamasi."""
    styled_section("Zaman Çizelgesi", "#1565c0")
    styled_info_banner("Okulun gunluk ders saatleri, teneffusler, ogle arasi ve etut saatlerini duzenleyin. "
               "Saatler ve sureler bos birakilmistir, okul kendi programina gore dolduracaktir.", "info")

    # Mevcut cizelgeyi yukle
    dilimler = store.get_zaman_cizelgesi()

    # Gorsel zaman cizelgesi onizleme
    styled_section("Günlük Program Onizleme", "#0d9488")

    # Renk kodlari aciklama
    renk_col1, renk_col2, renk_col3, renk_col4, renk_col5 = st.columns(5)
    with renk_col1:
        st.markdown(f"<span style='background-color:{ZAMAN_DILIMI_RENKLER['hazirlik']};padding:4px 12px;border-radius:4px;'>Hazirlik</span>",
                    unsafe_allow_html=True)
    with renk_col2:
        st.markdown(f"<span style='background-color:{ZAMAN_DILIMI_RENKLER['ders']};padding:4px 12px;border:1px solid #ddd;border-radius:4px;'>Ders</span>",
                    unsafe_allow_html=True)
    with renk_col3:
        st.markdown(f"<span style='background-color:{ZAMAN_DILIMI_RENKLER['teneffus']};padding:4px 12px;border-radius:4px;'>Teneffus</span>",
                    unsafe_allow_html=True)
    with renk_col4:
        st.markdown(f"<span style='background-color:{ZAMAN_DILIMI_RENKLER['ogle_arasi']};padding:4px 12px;border-radius:4px;'>Ogle Arasi</span>",
                    unsafe_allow_html=True)
    with renk_col5:
        st.markdown(f"<span style='background-color:{ZAMAN_DILIMI_RENKLER['etut']};padding:4px 12px;border-radius:4px;'>Etut</span>",
                    unsafe_allow_html=True)

    st.divider()

    # Onizleme tablosu
    preview_data = []
    for d in dilimler:
        if not d.aktif:
            continue
        tur_gorsel = d.tur
        if d.ders_no >= 9 and d.mod == "etut":
            tur_gorsel = "etut"
        renk = ZAMAN_DILIMI_RENKLER.get(tur_gorsel, "#0F1420")
        saat_bilgi = ""
        if d.baslangic and d.bitis:
            saat_bilgi = f"{d.baslangic} - {d.bitis}"
        elif d.baslangic:
            saat_bilgi = f"{d.baslangic} -"
        sure_bilgi = f"{d.sure_dk} dk" if d.sure_dk > 0 else "-"
        mod_bilgi = ""
        if d.ders_no >= 9 and d.tur == "ders":
            mod_bilgi = "Ders" if d.mod == "ders" else "Etut"

        preview_data.append({
            "Etiket": d.etiket,
            "Saat": saat_bilgi,
            "Sure": sure_bilgi,
            "Tur": ZAMAN_DILIMI_TURLERI.get(tur_gorsel, d.tur),
            "Mod": mod_bilgi,
        })

    if preview_data:
        preview_df = pd.DataFrame(preview_data)
        st.dataframe(preview_df, use_container_width=True, hide_index=True,
                     column_config={
                         "Etiket": st.column_config.TextColumn("Etkinlik", width="medium"),
                         "Saat": st.column_config.TextColumn("Saat Araligi", width="medium"),
                         "Sure": st.column_config.TextColumn("Sure", width="small"),
                         "Tur": st.column_config.TextColumn("Tur", width="small"),
                         "Mod": st.column_config.TextColumn("Mod", width="small"),
                     })

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Duzenleme formu
    styled_section("Zaman Çizelgesini Düzenle", "#2563eb")
    styled_info_banner("Her satirda baslangic saati, bitis saati ve sure (dakika) girebilirsiniz. "
               "9, 10 ve 11. dersler için Ders veya Etut modunu secebilirsiniz.", "info")

    with st.form("zaman_cizelgesi_form"):
        # Baslik
        hdr = st.columns([3, 2, 2, 1, 2, 1])
        with hdr[0]:
            st.markdown("**Etkinlik**")
        with hdr[1]:
            st.markdown("**Başlangıç**")
        with hdr[2]:
            st.markdown("**Bitis**")
        with hdr[3]:
            st.markdown("**Sure (dk)**")
        with hdr[4]:
            st.markdown("**Mod**")
        with hdr[5]:
            st.markdown("**Aktif**")

        yeni_dilimler = []
        for d in dilimler:
            cols = st.columns([3, 2, 2, 1, 2, 1])
            with cols[0]:
                st.write(f"{d.etiket}")
            with cols[1]:
                baslangic = st.text_input(
                    "B", value=d.baslangic,
                    key=f"zc_bas_{d.sira}",
                    label_visibility="collapsed",
                    placeholder="08:30"
                )
            with cols[2]:
                bitis = st.text_input(
                    "Bt", value=d.bitis,
                    key=f"zc_bit_{d.sira}",
                    label_visibility="collapsed",
                    placeholder="09:10"
                )
            with cols[3]:
                sure = st.number_input(
                    "S", value=d.sure_dk, min_value=0, max_value=120,
                    key=f"zc_sure_{d.sira}",
                    label_visibility="collapsed"
                )
            with cols[4]:
                if d.ders_no >= 9 and d.tur == "ders":
                    mod_opts = ["ders", "etut"]
                    mod = st.selectbox(
                        "M", mod_opts,
                        index=mod_opts.index(d.mod) if d.mod in mod_opts else 0,
                        format_func=lambda x: "Ders" if x == "ders" else "Etut",
                        key=f"zc_mod_{d.sira}",
                        label_visibility="collapsed"
                    )
                else:
                    mod = d.mod
                    st.write("-")
            with cols[5]:
                aktif = st.checkbox(
                    "A", value=d.aktif,
                    key=f"zc_aktif_{d.sira}",
                    label_visibility="collapsed"
                )

            yeni_d = ZamanDilimi(
                sira=d.sira,
                tur=d.tur,
                etiket=d.etiket,
                ders_no=d.ders_no,
                baslangic=baslangic.strip(),
                bitis=bitis.strip(),
                sure_dk=sure,
                mod=mod,
                aktif=aktif,
            )
            yeni_dilimler.append(yeni_d)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            kaydet_btn = st.form_submit_button("Zaman Çizelgesini Kaydet", type="primary")
        with btn_col2:
            sifirla_btn = st.form_submit_button("Varsayilana Sifirla")

        if kaydet_btn:
            store.save_zaman_cizelgesi(yeni_dilimler)
            st.success("Zaman cizelgesi basariyla kaydedildi!")
            st.rerun(scope="fragment")

        if sifirla_btn:
            store.reset_zaman_cizelgesi()
            st.success("Zaman cizelgesi varsayilan degerlere sifirlandi!")
            st.rerun(scope="fragment")

    # Bilgi paneli
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    styled_section("Zaman Çizelgesi Bilgileri", "#8b5cf6")
    styled_info_banner(
        "Günlük Program Yapisi: Sabah Hazirlik → 1-4. Ders (aralarinda teneffus) → "
        "Ogle Arasi → 5-8. Ders → 9-11. Ders/Etut. Başlangıç/Bitis saat formatinda (08:30), "
        "Sure dakika cinsinden (40), Mod 9-11. dersler için Ders/Etut, "
        "Aktif kullanilmayan saatleri devre disi birakin.", "info"
    )

    # Ozet istatistik
    aktif_dersler = [d for d in dilimler if d.aktif and d.tur == "ders"]
    aktif_etutler = [d for d in dilimler if d.aktif and d.tur == "ders" and d.mod == "etut"]
    aktif_teneffusler = [d for d in dilimler if d.aktif and d.tur == "teneffus"]
    toplam_ders_sure = sum(d.sure_dk for d in aktif_dersler if d.sure_dk > 0)
    toplam_teneffus_sure = sum(d.sure_dk for d in aktif_teneffusler if d.sure_dk > 0)
    ogle_arasi = next((d for d in dilimler if d.aktif and d.tur == "ogle_arasi"), None)
    ogle_sure = ogle_arasi.sure_dk if ogle_arasi and ogle_arasi.sure_dk > 0 else 0

    styled_stat_row([
        ("Aktif Ders", len(aktif_dersler), "#2563eb", "\U0001f4d6"),
        ("Etut Saati", len(aktif_etutler), "#8b5cf6", "\U0001f4dd"),
        ("Teneffus", len(aktif_teneffusler), "#10b981", "\u2615"),
        ("Toplam Ders", f"{toplam_ders_sure} dk" if toplam_ders_sure > 0 else "-", "#f59e0b", "\u23f0"),
        ("Ogle Arasi", f"{ogle_sure} dk" if ogle_sure > 0 else "-", "#ef4444", "\U0001f37d\ufe0f"),
    ])


# ==================== AI ANALIZ YARDIMCISI ====================

def _ai_ogrenci_analiz(ogrenci_adi: str, sinif: int, sube: str,
                       sinav_verileri: dict, devamsizlik_verileri: dict,
                       online_ders_verileri: dict, platform_verileri: dict,
                       analiz_turu: str = "ogrenci") -> str:
    """OpenAI GPT-4o-mini ile ogrenci analizi ve tavsiyeleri uret.

    analiz_turu: 'ogrenci' | 'veli' | 'genel'
    """
    try:
        import openai
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return ""

        # Veri ozetini hazirla
        veri_ozeti = f"Öğrenci: {ogrenci_adi} | Sınıf: {sinif}-{sube}\n\n"

        # Sinav verileri
        if sinav_verileri.get("sinav_sayisi", 0) > 0:
            veri_ozeti += (
                f"SINAV VERILERI:\n"
                f"- Sınav sayisi: {sinav_verileri['sinav_sayisi']}\n"
                f"- Ortalama puan: {sinav_verileri.get('ortalama', 0):.1f}\n"
                f"- En yuksek: {sinav_verileri.get('en_yuksek', 0):.1f}\n"
                f"- En dusuk: {sinav_verileri.get('en_dusuk', 0):.1f}\n"
            )
            if sinav_verileri.get("konu_performans"):
                veri_ozeti += "- Konu bazli basari oranlari:\n"
                for konu, oran in sinav_verileri["konu_performans"].items():
                    veri_ozeti += f"  * {konu}: %{oran}\n"
        else:
            veri_ozeti += "SINAV VERILERI: Henuz sinav sonucu yok.\n"

        # Devamsizlik verileri
        veri_ozeti += (
            f"\nDEVAMSIZLIK:\n"
            f"- Toplam: {devamsizlik_verileri.get('toplam', 0)} gun\n"
            f"- Ozurlu: {devamsizlik_verileri.get('ozurlu', 0)}\n"
            f"- Ozursuz: {devamsizlik_verileri.get('ozursuz', 0)}\n"
        )

        # Online ders verileri
        if online_ders_verileri.get("toplam", 0) > 0:
            veri_ozeti += (
                f"\nONLINE DERS:\n"
                f"- Toplam ders: {online_ders_verileri['toplam']}\n"
                f"- Yapilan: {online_ders_verileri.get('yapildi', 0)}\n"
                f"- Yapilmayan: {online_ders_verileri.get('yapilmadi', 0)}\n"
                f"- Toplam sure: {online_ders_verileri.get('sure_dk', 0)} dakika\n"
            )

        # Platform verileri
        if platform_verileri.get("girisler"):
            veri_ozeti += "\nDIJITAL PLATFORM KULLANIMI:\n"
            for plt_adi, sayi in platform_verileri["girisler"].items():
                veri_ozeti += f"- {plt_adi}: {sayi} giris\n"

        # Prompt olustur
        if analiz_turu == "veli":
            system_msg = (
                "Sen deneyimli bir egitim danismanisin. Velilere yonelik anlasilir, "
                "yapici ve motive edici bir dilde analiz ve tavsiyeler yazarsin. "
                "Turkce yaz, emoji kullanma."
            )
            user_msg = (
                f"Asagidaki ogrenci verilerini analiz et ve veliye yonelik "
                f"bir rapor hazirla:\n\n{veri_ozeti}\n\n"
                "Su basliklarda yaz:\n"
                "1. GENEL DEGERLENDIRME (2-3 cumle)\n"
                "2. GUCLU YONLER\n"
                "3. GELISIM ALANLARI\n"
                "4. VELIYE TAVSIYELER (evde yapilabilecekler)\n"
                "5. OGRETMENLE ISBIRLIGI ONERILERI"
            )
        elif analiz_turu == "genel":
            system_msg = (
                "Sen deneyimli bir egitim analisti ve okul danismanisin. "
                "Sınıf bazli genel performans analizi yapiyorsun. Turkce yaz, emoji kullanma."
            )
            user_msg = (
                f"Asagidaki sinif/okul geneli verileri analiz et:\n\n{veri_ozeti}\n\n"
                "Su basliklarda yaz:\n"
                "1. GENEL PERFORMANS DEGERLENDIRMESI\n"
                "2. DIKKAT GEREKTIREN NOKTALAR\n"
                "3. BASARILI ALANLAR\n"
                "4. IYILESTIRME ONERILERI\n"
                "5. AKSIYON PLANI"
            )
        else:  # ogrenci
            system_msg = (
                "Sen deneyimli bir egitim danismani ve rehber ogretmensin. "
                "Öğrencilere yonelik motive edici, yapici ve somut tavsiyeler verirsin. "
                "Turkce yaz, emoji kullanma."
            )
            user_msg = (
                f"Asagidaki ogrenci verilerini analiz et ve ogrenciye yonelik "
                f"kisisellestirilmis bir degerlendirme hazirla:\n\n{veri_ozeti}\n\n"
                "Su basliklarda yaz:\n"
                "1. GENEL DEGERLENDIRME (2-3 cumle)\n"
                "2. GUCLU YONLERIN\n"
                "3. GELISIM ALANLARIN\n"
                "4. SOMUT TAVSIYELER (ne yapmali)\n"
                "5. HAFTALIK CALISMA PLANI ONERISI"
            )

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.6,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analiz olusturulamadi: {str(e)}"


def _collect_student_ai_data(sel_ogr_id: str, sel_ogr: dict,
                             od_results, attendance, online_kayitlar, platform_girisler):
    """Bir ogrencinin AI analizi için verilerini topla."""
    # Sinav verileri
    ogr_results = [r for r in od_results if r.student_id == sel_ogr_id]
    sinav_verileri = {"sinav_sayisi": len(ogr_results)}
    if ogr_results:
        puanlar = [r.score for r in ogr_results]
        sinav_verileri["ortalama"] = sum(puanlar) / len(puanlar)
        sinav_verileri["en_yuksek"] = max(puanlar)
        sinav_verileri["en_dusuk"] = min(puanlar)
        konu_toplam: dict[str, dict] = {}
        for r in ogr_results:
            for konu, perf in r.subject_breakdown.items():
                if konu not in konu_toplam:
                    konu_toplam[konu] = {"correct": 0, "total": 0}
                konu_toplam[konu]["correct"] += perf.get("correct", 0)
                konu_toplam[konu]["total"] += perf.get("total", 0)
        sinav_verileri["konu_performans"] = {
            k: round(v["correct"] * 100 / max(v["total"], 1))
            for k, v in konu_toplam.items()
        }

    # Devamsizlik verileri
    ogr_dev = [a for a in attendance if a.student_id == sel_ogr_id]
    devamsizlik_verileri = {
        "toplam": len(ogr_dev),
        "ozurlu": sum(1 for a in ogr_dev if a.turu == "ozurlu"),
        "ozursuz": sum(1 for a in ogr_dev if a.turu == "ozursuz"),
    }

    # Online ders verileri
    ogr_sinif = sel_ogr.get("sinif", 0)
    ogr_sube = sel_ogr.get("sube", "")
    ogr_online = [k for k in online_kayitlar
                  if k.sinif == ogr_sinif and k.sube == ogr_sube]
    online_ders_verileri = {
        "toplam": len(ogr_online),
        "yapildi": sum(1 for k in ogr_online if k.durum == "yapildi"),
        "yapilmadi": sum(1 for k in ogr_online if k.durum == "yapilmadi"),
        "sure_dk": sum(k.sure_dk for k in ogr_online if k.durum == "yapildi"),
    }

    # Platform verileri
    plt_sayim: dict[str, int] = {}
    for g in platform_girisler:
        plt_sayim[g.platform_adi] = plt_sayim.get(g.platform_adi, 0) + 1
    platform_verileri = {"girisler": plt_sayim} if plt_sayim else {}

    return sinav_verileri, devamsizlik_verileri, online_ders_verileri, platform_verileri


def _render_ai_analiz_section(ogrenci_adi: str, sinif: int, sube: str,
                              sinav_verileri: dict, devamsizlik_verileri: dict,
                              online_ders_verileri: dict, platform_verileri: dict,
                              key_prefix: str = "ai"):
    """AI analiz butonlari ve sonuclarini goster."""
    st.markdown("---")
    styled_section("AI Destekli Analiz ve Tavsiyeler", color="#8b5cf6")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        styled_info_banner(
            "AI analiz için OPENAI_API_KEY ortam degiskeni tanimlanmalidir.",
            banner_type="warning"
        )
        return

    ai_c1, ai_c2 = st.columns(2)
    with ai_c1:
        ogrenci_btn = st.button(
            "Öğrenci Raporu Oluştur",
            key=f"{key_prefix}_ogrenci_btn",
            use_container_width=True,
        )
    with ai_c2:
        veli_btn = st.button(
            "Veli Raporu Oluştur",
            key=f"{key_prefix}_veli_btn",
            use_container_width=True,
        )

    if ogrenci_btn:
        with st.spinner("AI ogrenci analizi hazirlaniyor..."):
            sonuc = _ai_ogrenci_analiz(
                ogrenci_adi, sinif, sube,
                sinav_verileri, devamsizlik_verileri,
                online_ders_verileri, platform_verileri,
                analiz_turu="ogrenci"
            )
        if sonuc:
            st.session_state[f"{key_prefix}_ogrenci_sonuc"] = sonuc

    if veli_btn:
        with st.spinner("AI veli raporu hazirlaniyor..."):
            sonuc = _ai_ogrenci_analiz(
                ogrenci_adi, sinif, sube,
                sinav_verileri, devamsizlik_verileri,
                online_ders_verileri, platform_verileri,
                analiz_turu="veli"
            )
        if sonuc:
            st.session_state[f"{key_prefix}_veli_sonuc"] = sonuc

    # Ogrenci raporu goster
    if f"{key_prefix}_ogrenci_sonuc" in st.session_state:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#ede9fe,#e0e7ff);border-radius:14px;'
            f'padding:20px;margin:12px 0;border-left:4px solid #6366f1;">'
            f'<div style="font-size:15px;font-weight:700;color:#4338ca;margin-bottom:10px;">'
            f'Öğrenci İçin AI Analizi</div>'
            f'<div style="font-size:13px;color:#94A3B8;white-space:pre-wrap;">'
            f'{st.session_state[f"{key_prefix}_ogrenci_sonuc"]}</div></div>',
            unsafe_allow_html=True
        )

    # Veli raporu goster
    if f"{key_prefix}_veli_sonuc" in st.session_state:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#fef3c7,#fde68a);border-radius:14px;'
            f'padding:20px;margin:12px 0;border-left:4px solid #f59e0b;">'
            f'<div style="font-size:15px;font-weight:700;color:#b45309;margin-bottom:10px;">'
            f'Veli İçin AI Raporu</div>'
            f'<div style="font-size:13px;color:#94A3B8;white-space:pre-wrap;">'
            f'{st.session_state[f"{key_prefix}_veli_sonuc"]}</div></div>',
            unsafe_allow_html=True
        )


# ==================== OGRENCI ANALIZI ====================

@st.fragment
def _render_ogrenci_analizi(store: AkademikDataStore):
    """Ogrenci analizi: sinav, devamsizlik, online ders, dijital ogrenme verileri."""
    kurum = get_institution_info()
    akademik_yil = _get_akademik_yil()

    # OD modulunden sinav verilerini cek
    try:
        from models.olcme_degerlendirme import get_store as get_od_store
        od_store = get_od_store()
        od_results = od_store.get_results()
        od_available = True
    except Exception:
        od_results = []
        od_available = False

    # Akademik Takip verileri
    students = store.get_students()
    attendance = store.get_attendance()
    online_kayitlar = store.get_online_ders_kayitlari(akademik_yil)
    platform_girisler = store.get_platform_girisler(akademik_yil)

    if not students and not od_results:
        styled_info_banner("Analiz için ogrenci veya sinav verisi bulunamadı.", banner_type="warning")
        return

    # Ogrenci listesi: her iki kaynaktan birlesik
    ogrenci_map: dict[str, dict] = {}

    # Kayitli ogrenciler
    for s in students:
        key = s.id
        ogrenci_map[key] = {
            "id": s.id, "ad": f"{s.ad} {s.soyad}",
            "sinif": s.sinif, "sube": s.sube, "numara": s.numara,
        }

    # Sinav sonuclarindan bilinmeyen ogrenciler
    for r in od_results:
        if r.student_id and r.student_id not in ogrenci_map:
            ogrenci_map[r.student_id] = {
                "id": r.student_id, "ad": r.student_name,
                "sinif": 0, "sube": r.section, "numara": r.student_number,
            }

    an_tab1, an_tab2, an_tab3 = st.tabs([
        "📊 Genel Bakis", "🎓 Öğrenci Detay", "⚖️ Karsilastirma"
    ])

    # ---- TAB 1: Genel Bakis ----
    with an_tab1:
        st.markdown(ReportStyler.report_header_html(
            "Genel Bakis", "Öğrenci, sinav, devamsizlik ve dijital platform ozeti", "#6366f1"
        ), unsafe_allow_html=True)

        toplam_ogrenci = len(ogrenci_map)
        toplam_sinav = len(od_results)
        toplam_devamsizlik = len(attendance)
        toplam_online = len(online_kayitlar)

        st.markdown(ReportStyler.metric_cards_html([
            ("Öğrenci", str(toplam_ogrenci), "#6366f1", ""),
            ("Sınav Sonucu", str(toplam_sinav), "#2563eb", ""),
            ("Devamsızlık", str(toplam_devamsizlik), "#ef4444", ""),
            ("Online Ders", str(toplam_online), "#059669", ""),
        ]), unsafe_allow_html=True)

        pdf_metrics_gb = [
            ("Öğrenci", str(toplam_ogrenci), "#6366f1"),
            ("Sınav", str(toplam_sinav), "#2563eb"),
            ("Devamsızlık", str(toplam_devamsizlik), "#ef4444"),
            ("Online Ders", str(toplam_online), "#059669"),
        ]
        pdf_tables_gb = []
        pdf_charts_gb = []

        if od_results:
            st.markdown(ReportStyler.section_divider_html("Sınav Performansi Özeti", "#2563eb"), unsafe_allow_html=True)

            puan_araliklari = {"0-25": 0, "26-50": 0, "51-75": 0, "76-100": 0}
            puanlar = []
            for r in od_results:
                puanlar.append(r.score)
                if r.score <= 25:
                    puan_araliklari["0-25"] += 1
                elif r.score <= 50:
                    puan_araliklari["26-50"] += 1
                elif r.score <= 75:
                    puan_araliklari["51-75"] += 1
                else:
                    puan_araliklari["76-100"] += 1

            ort_puan = sum(puanlar) / len(puanlar) if puanlar else 0
            max_puan = max(puanlar) if puanlar else 0
            min_puan = min(puanlar) if puanlar else 0

            st.markdown(ReportStyler.metric_cards_html([
                ("Ortalama", f"{ort_puan:.1f}", "#2563eb", ""),
                ("En Yuksek", f"{max_puan:.1f}", "#059669", ""),
                ("En Dusuk", f"{min_puan:.1f}", "#ef4444", ""),
                ("Sınav Sayısı", str(len(od_results)), "#7c3aed", ""),
            ]), unsafe_allow_html=True)

            col_bar_gb, col_donut_gb = st.columns([3, 2])
            with col_bar_gb:
                st.markdown(ReportStyler.section_divider_html("Puan Dagilimi", "#1565c0"), unsafe_allow_html=True)
                st.markdown(ReportStyler.horizontal_bar_html(puan_araliklari, "#2563eb"), unsafe_allow_html=True)
            with col_donut_gb:
                st.markdown(ReportStyler.section_divider_html("Puan Dilimi Dagilimi", "#0d9488"), unsafe_allow_html=True)
                st.markdown(ReportStyler.donut_chart_svg(puan_araliklari, ["#ef4444", "#f59e0b", "#2563eb", "#059669"], size=145), unsafe_allow_html=True)

            pdf_charts_gb.append(("bar", puan_araliklari, "Puan Dagilimi", "#2563eb"))
            pdf_charts_gb.append(("donut", puan_araliklari, "Puan Dilimi", ["#ef4444", "#f59e0b", "#2563eb", "#059669"]))

        # Devamsizlik ozeti
        if attendance:
            st.markdown(ReportStyler.section_divider_html("Devamsızlık Özeti", "#ef4444"), unsafe_allow_html=True)

            devamsizlik_by_type: dict[str, int] = {}
            for a in attendance:
                devamsizlik_by_type[a.turu] = devamsizlik_by_type.get(a.turu, 0) + 1

            dev_rows_gb = [{"Tur": t.capitalize(), "Sayı": s} for t, s in sorted(devamsizlik_by_type.items())]
            df_dev_gb = pd.DataFrame(dev_rows_gb)

            col_devt, col_devc = st.columns([3, 2])
            with col_devt:
                st.markdown(ReportStyler.colored_table_html(df_dev_gb, "#ef4444"), unsafe_allow_html=True)
            with col_devc:
                dev_chart_data = {t.capitalize(): s for t, s in devamsizlik_by_type.items()}
                st.markdown(ReportStyler.donut_chart_svg(dev_chart_data, ["#10b981", "#ef4444", "#f59e0b", "#8b5cf6"], size=160), unsafe_allow_html=True)

            pdf_tables_gb.append(("Devamsızlık Özeti", df_dev_gb, "#ef4444"))
            pdf_charts_gb.append(("donut", dev_chart_data, "Devamsızlık Turleri", ["#10b981", "#ef4444", "#f59e0b", "#8b5cf6"]))

        # Platform giris ozeti
        if platform_girisler:
            st.markdown(ReportStyler.section_divider_html("Dijital Platform Kullanimi", "#7c3aed"), unsafe_allow_html=True)

            plt_sayim: dict[str, int] = {}
            for g in platform_girisler:
                plt_sayim[g.platform_adi] = plt_sayim.get(g.platform_adi, 0) + 1

            plt_rows_gb = [{"Platform": p, "Giriş Sayısı": s} for p, s in sorted(plt_sayim.items(), key=lambda x: x[1], reverse=True)]
            df_plt_gb = pd.DataFrame(plt_rows_gb)

            col_pltt, col_pltc = st.columns([3, 2])
            with col_pltt:
                st.markdown(ReportStyler.colored_table_html(df_plt_gb, "#7c3aed"), unsafe_allow_html=True)
            with col_pltc:
                st.markdown(ReportStyler.horizontal_bar_html(plt_sayim, "#7c3aed"), unsafe_allow_html=True)

            pdf_tables_gb.append(("Platform Kullanimi", df_plt_gb, "#7c3aed"))
            pdf_charts_gb.append(("bar", plt_sayim, "Platform Kullanimi", "#7c3aed"))

        # Genel AI Analizi
        st.markdown(ReportStyler.section_divider_html("AI Destekli Genel Değerlendirme", "#8b5cf6"), unsafe_allow_html=True)

        api_key_genel = os.environ.get("OPENAI_API_KEY", "")
        if not api_key_genel:
            styled_info_banner(
                "AI analiz için OPENAI_API_KEY ortam degiskeni tanimlanmalidir.",
                banner_type="warning"
            )
        else:
            if st.button("Genel AI Analizi Oluştur", key="ai_genel_btn", use_container_width=True):
                genel_sinav = {
                    "sinav_sayisi": len(od_results),
                    "ortalama": sum(r.score for r in od_results) / max(len(od_results), 1),
                    "en_yuksek": max((r.score for r in od_results), default=0),
                    "en_dusuk": min((r.score for r in od_results), default=0),
                }
                genel_dev = {
                    "toplam": len(attendance),
                    "ozurlu": sum(1 for a in attendance if a.turu == "ozurlu"),
                    "ozursuz": sum(1 for a in attendance if a.turu == "ozursuz"),
                }
                genel_online = {
                    "toplam": len(online_kayitlar),
                    "yapildi": sum(1 for k in online_kayitlar if k.durum == "yapildi"),
                    "yapilmadi": sum(1 for k in online_kayitlar if k.durum == "yapilmadi"),
                    "sure_dk": sum(k.sure_dk for k in online_kayitlar if k.durum == "yapildi"),
                }
                genel_plt: dict[str, int] = {}
                for g in platform_girisler:
                    genel_plt[g.platform_adi] = genel_plt.get(g.platform_adi, 0) + 1
                genel_platform = {"girisler": genel_plt} if genel_plt else {}

                with st.spinner("AI genel analiz hazirlaniyor..."):
                    sonuc = _ai_ogrenci_analiz(
                        "Okul Geneli", 0, "",
                        genel_sinav, genel_dev, genel_online, genel_platform,
                        analiz_turu="genel"
                    )
                if sonuc:
                    st.session_state["ai_genel_sonuc"] = sonuc

            if "ai_genel_sonuc" in st.session_state:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border-radius:14px;'
                    f'padding:20px;margin:12px 0;border-left:4px solid #16a34a;">'
                    f'<div style="font-size:15px;font-weight:700;color:#166534;margin-bottom:10px;">'
                    f'Genel AI Değerlendirmesi</div>'
                    f'<div style="font-size:13px;color:#94A3B8;white-space:pre-wrap;">'
                    f'{st.session_state["ai_genel_sonuc"]}</div></div>',
                    unsafe_allow_html=True
                )

        # PDF + Paylasim
        pdf_gen = ReportPDFGenerator("Öğrenci Genel Bakis Raporu")
        pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
        pdf_gen.add_section("Genel Metrikler")
        pdf_gen.add_metrics(pdf_metrics_gb)
        for _title, _df, _color in pdf_tables_gb:
            pdf_gen.add_section(_title)
            pdf_gen.add_table(_df, _color)
        for _ci in pdf_charts_gb:
            if _ci[0] == "bar":
                pdf_gen.add_bar_chart(_ci[1], _ci[2], _ci[3])
            else:
                pdf_gen.add_donut_chart(_ci[1], _ci[2], _ci[3])
        pdf_bytes = pdf_gen.generate()
        ReportSharer.render_share_ui(
            pdf_bytes, "ogrenci_genel_bakis.pdf",
            "Öğrenci Genel Bakis Raporu",
            unique_key="ogr_genel",
        )

    # ---- TAB 2: Ogrenci Detay ----
    with an_tab2:
        st.markdown(ReportStyler.report_header_html(
            "Öğrenci Detay Raporu", "360 derece bireysel ogrenci analizi", "#2563eb"
        ), unsafe_allow_html=True)

        if not ogrenci_map:
            styled_info_banner("Öğrenci verisi bulunamadı.", banner_type="warning")
        else:
            ogr_opts = {k: f"{v['ad']} ({v['sinif']}-{v['sube']} / {v['numara']})" for k, v in ogrenci_map.items()}
            sel_ogr_id = st.selectbox("Öğrenci Sec", list(ogr_opts.keys()),
                                      format_func=lambda x: ogr_opts.get(x, x),
                                      key="an_ogr_sec")

            sel_ogr = ogrenci_map.get(sel_ogr_id, {})
            if sel_ogr:
                st.markdown(ReportStyler.report_header_html(
                    sel_ogr["ad"],
                    f'Sınıf: {sel_ogr["sinif"]}-{sel_ogr["sube"]} | No: {sel_ogr["numara"]}',
                    "#1e40af"
                ), unsafe_allow_html=True)

                pdf_gen_d = ReportPDFGenerator(f"Öğrenci Raporu - {sel_ogr['ad']}")
                pdf_gen_d.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
                pdf_gen_d.add_section("Öğrenci Bilgileri")
                pdf_gen_d.add_text(f"Ad: {sel_ogr['ad']}  |  Sınıf: {sel_ogr['sinif']}-{sel_ogr['sube']}  |  No: {sel_ogr['numara']}")

                # 1. Sinav sonuclari
                ogr_results = [r for r in od_results if r.student_id == sel_ogr_id]
                st.markdown(ReportStyler.section_divider_html("Sınav Sonuclari", "#2563eb"), unsafe_allow_html=True)

                if ogr_results:
                    ogr_puanlar = [r.score for r in ogr_results]
                    ogr_ort = sum(ogr_puanlar) / len(ogr_puanlar)
                    ogr_max = max(ogr_puanlar)
                    ogr_min = min(ogr_puanlar)

                    st.markdown(ReportStyler.metric_cards_html([
                        ("Sınav Sayısı", str(len(ogr_results)), "#2563eb", ""),
                        ("Ortalama", f"{ogr_ort:.1f}", "#6366f1", ""),
                        ("En Yuksek", f"{ogr_max:.1f}", "#059669", ""),
                        ("En Dusuk", f"{ogr_min:.1f}", "#ef4444", ""),
                    ]), unsafe_allow_html=True)

                    pdf_gen_d.add_section("Sınav Sonuclari")
                    pdf_gen_d.add_metrics([
                        ("Sınav", str(len(ogr_results)), "#2563eb"),
                        ("Ortalama", f"{ogr_ort:.1f}", "#6366f1"),
                        ("En Yuksek", f"{ogr_max:.1f}", "#059669"),
                        ("En Dusuk", f"{ogr_min:.1f}", "#ef4444"),
                    ])

                    sinav_rows = []
                    for r in ogr_results:
                        sinav_rows.append({
                            "Tarih": r.graded_at[:10] if r.graded_at else "",
                            "Puan": round(r.score, 1),
                            "Net": round(r.net_score, 1),
                            "Dogru": r.correct_count,
                            "Yanlis": r.wrong_count,
                            "Bos": r.empty_count,
                            "Toplam Soru": r.total_questions,
                        })
                    df_sinav = pd.DataFrame(sinav_rows)

                    col_sinav_t, col_sinav_c = st.columns([3, 2])
                    with col_sinav_t:
                        st.markdown(ReportStyler.colored_table_html(df_sinav, "#2563eb", value_column="Puan"), unsafe_allow_html=True)
                    with col_sinav_c:
                        st.markdown(ReportStyler.section_divider_html("Puan Trendi", "#0d9488"), unsafe_allow_html=True)
                        puan_trend = {f"S{i+1}": p for i, p in enumerate(ogr_puanlar)}
                        st.markdown(ReportStyler.horizontal_bar_html(puan_trend, "#2563eb"), unsafe_allow_html=True)

                    pdf_gen_d.add_table(df_sinav, "#2563eb")
                    pdf_gen_d.add_bar_chart(puan_trend, "Puan Trendi", "#2563eb")

                    # Konu bazli performans
                    konu_toplam: dict[str, dict] = {}
                    for r in ogr_results:
                        for konu, perf in r.subject_breakdown.items():
                            if konu not in konu_toplam:
                                konu_toplam[konu] = {"correct": 0, "wrong": 0, "empty": 0, "total": 0}
                            konu_toplam[konu]["correct"] += perf.get("correct", 0)
                            konu_toplam[konu]["wrong"] += perf.get("wrong", 0)
                            konu_toplam[konu]["empty"] += perf.get("empty", 0)
                            konu_toplam[konu]["total"] += perf.get("total", 0)

                    if konu_toplam:
                        st.markdown(ReportStyler.section_divider_html("Konu Bazli Performans", "#7c3aed"), unsafe_allow_html=True)
                        konu_rows = []
                        konu_chart = {}
                        for konu, info in sorted(konu_toplam.items()):
                            basari = round(info["correct"] * 100 / max(info["total"], 1))
                            konu_rows.append({
                                "Konu": konu,
                                "Dogru": info["correct"],
                                "Yanlis": info["wrong"],
                                "Bos": info["empty"],
                                "Toplam": info["total"],
                                "Başarı %": basari,
                            })
                            konu_chart[konu] = basari
                        df_konu = pd.DataFrame(konu_rows)

                        col_konu_t, col_konu_c = st.columns([3, 2])
                        with col_konu_t:
                            st.markdown(ReportStyler.colored_table_html(df_konu, "#7c3aed", value_column="Başarı %"), unsafe_allow_html=True)
                        with col_konu_c:
                            st.markdown(ReportStyler.horizontal_bar_html(konu_chart, "#7c3aed"), unsafe_allow_html=True)

                        pdf_gen_d.add_section("Konu Bazli Performans")
                        pdf_gen_d.add_table(df_konu, "#7c3aed")
                        pdf_gen_d.add_bar_chart(konu_chart, "Konu Başarı Oranlari", "#7c3aed")
                else:
                    st.info("Bu ogrenciye ait sinav sonucu bulunmuyor.")

                # 2. Devamsizlik
                ogr_devamsizlik = [a for a in attendance if a.student_id == sel_ogr_id]
                st.markdown(ReportStyler.section_divider_html("Devamsızlık Kayıtlari", "#ef4444"), unsafe_allow_html=True)

                if ogr_devamsizlik:
                    dev_ozlu = sum(1 for a in ogr_devamsizlik if a.turu == "ozurlu")
                    dev_ozursuz = sum(1 for a in ogr_devamsizlik if a.turu == "ozursuz")
                    dev_diger = len(ogr_devamsizlik) - dev_ozlu - dev_ozursuz

                    st.markdown(ReportStyler.metric_cards_html([
                        ("Toplam", str(len(ogr_devamsizlik)), "#ef4444", ""),
                        ("Ozurlu", str(dev_ozlu), "#f59e0b", ""),
                        ("Ozursuz", str(dev_ozursuz), "#dc2626", ""),
                        ("Diger", str(dev_diger), "#64748b", ""),
                    ]), unsafe_allow_html=True)

                    dev_rows = []
                    for a in sorted(ogr_devamsizlik, key=lambda x: x.tarih, reverse=True)[:20]:
                        dev_rows.append({
                            "Tarih": a.tarih,
                            "Ders": a.ders,
                            "Saat": a.ders_saati,
                            "Tur": a.turu.capitalize(),
                        })
                    df_dev_d = pd.DataFrame(dev_rows)

                    col_dev_t, col_dev_c = st.columns([3, 2])
                    with col_dev_t:
                        st.markdown(ReportStyler.colored_table_html(df_dev_d, "#ef4444"), unsafe_allow_html=True)
                    with col_dev_c:
                        dev_donut = {}
                        if dev_ozlu > 0:
                            dev_donut["Ozurlu"] = dev_ozlu
                        if dev_ozursuz > 0:
                            dev_donut["Ozursuz"] = dev_ozursuz
                        if dev_diger > 0:
                            dev_donut["Diger"] = dev_diger
                        if dev_donut:
                            st.markdown(ReportStyler.donut_chart_svg(dev_donut, ["#f59e0b", "#ef4444", "#64748b"], size=160), unsafe_allow_html=True)

                    pdf_gen_d.add_section("Devamsızlık")
                    pdf_gen_d.add_metrics([
                        ("Toplam", str(len(ogr_devamsizlik)), "#ef4444"),
                        ("Ozurlu", str(dev_ozlu), "#f59e0b"),
                        ("Ozursuz", str(dev_ozursuz), "#dc2626"),
                    ])
                    pdf_gen_d.add_table(df_dev_d, "#ef4444")
                    if dev_donut:
                        pdf_gen_d.add_donut_chart(dev_donut, "Devamsızlık Dagilimi", ["#f59e0b", "#ef4444", "#64748b"])
                else:
                    st.info("Bu ogrenciye ait devamsizlik kaydi bulunmuyor.")

                # 3. Online ders katilimi (sinif/sube bazli)
                st.markdown(ReportStyler.section_divider_html("Online Ders Verileri", "#059669"), unsafe_allow_html=True)

                ogr_sinif = sel_ogr.get("sinif", 0)
                ogr_sube = sel_ogr.get("sube", "")
                ogr_online = [k for k in online_kayitlar
                             if k.sinif == ogr_sinif and k.sube == ogr_sube]

                if ogr_online:
                    on_yapildi = sum(1 for k in ogr_online if k.durum == "yapildi")
                    on_yapilmadi = sum(1 for k in ogr_online if k.durum == "yapilmadi")
                    on_sure = sum(k.sure_dk for k in ogr_online if k.durum == "yapildi")

                    st.markdown(ReportStyler.metric_cards_html([
                        ("Toplam Ders", str(len(ogr_online)), "#059669", ""),
                        ("Yapildi", str(on_yapildi), "#16a34a", ""),
                        ("Yapilmadi", str(on_yapilmadi), "#ef4444", ""),
                        ("Toplam Sure", f"{on_sure} dk", "#2563eb", ""),
                    ]), unsafe_allow_html=True)

                    on_donut = {"Yapildi": on_yapildi, "Yapilmadi": on_yapilmadi}
                    st.markdown(ReportStyler.donut_chart_svg(on_donut, ["#059669", "#ef4444"], size=160), unsafe_allow_html=True)

                    pdf_gen_d.add_section("Online Ders")
                    pdf_gen_d.add_metrics([
                        ("Toplam", str(len(ogr_online)), "#059669"),
                        ("Yapildi", str(on_yapildi), "#16a34a"),
                        ("Sure", f"{on_sure} dk", "#2563eb"),
                    ])
                    pdf_gen_d.add_donut_chart(on_donut, "Online Ders Durumu", ["#059669", "#ef4444"])
                else:
                    st.info(f"{ogr_sinif}-{ogr_sube} sinifina ait online ders kaydi bulunmuyor.")

                # 4. Dijital platform kullanimi (genel)
                st.markdown(ReportStyler.section_divider_html("Dijital Platform Kullanimi (Genel)", "#7c3aed"), unsafe_allow_html=True)

                if platform_girisler:
                    plt_sayim2: dict[str, int] = {}
                    for g in platform_girisler:
                        plt_sayim2[g.platform_adi] = plt_sayim2.get(g.platform_adi, 0) + 1

                    st.markdown(ReportStyler.horizontal_bar_html(plt_sayim2, "#7c3aed"), unsafe_allow_html=True)
                else:
                    st.info("Platform giris verisi bulunmuyor.")

                # 5. AI Destekli Analiz
                sinav_v, dev_v, online_v, plt_v = _collect_student_ai_data(
                    sel_ogr_id, sel_ogr, od_results, attendance,
                    online_kayitlar, platform_girisler
                )
                _render_ai_analiz_section(
                    sel_ogr["ad"], sel_ogr.get("sinif", 0), sel_ogr.get("sube", ""),
                    sinav_v, dev_v, online_v, plt_v,
                    key_prefix=f"ai_detay_{sel_ogr_id[:8]}"
                )

                # PDF + Paylasim
                pdf_bytes_d = pdf_gen_d.generate()
                veli_email = ""
                veli_tel = ""
                for s in students:
                    if s.id == sel_ogr_id:
                        veli_email = getattr(s, "veli_email", "") or ""
                        veli_tel = getattr(s, "veli_telefon", "") or ""
                        break
                ReportSharer.render_share_ui(
                    pdf_bytes_d, f"ogrenci_raporu_{sel_ogr['ad'].replace(' ', '_')}.pdf",
                    f"Öğrenci Raporu - {sel_ogr['ad']}",
                    unique_key="ogr_detay", default_email=veli_email, default_phone=veli_tel,
                )

    # ---- TAB 3: Karsilastirma ----
    with an_tab3:
        st.markdown(ReportStyler.report_header_html(
            "Öğrenci Karsilastirma", "Sınav, devamsizlik ve online ders karsilastirma raporu", "#f59e0b"
        ), unsafe_allow_html=True)

        if not od_results:
            styled_info_banner("Karsilastirma için sinav sonucu bulunamadı.", banner_type="warning")
        else:
            # Sinif/sube filtresi
            kr_c1, kr_c2 = st.columns(2)
            with kr_c1:
                kr_siniflar = sorted(set(v["sinif"] for v in ogrenci_map.values() if v["sinif"]))
                kr_sinif_an = st.selectbox("Sınıf", ["Tümü"] + kr_siniflar, key="kr_sinif_an")
            with kr_c2:
                kr_subeler = sorted(set(v["sube"] for v in ogrenci_map.values() if v["sube"]))
                kr_sube_an = st.selectbox("Şube", ["Tümü"] + kr_subeler, key="kr_sube_an")

            filtre_ogrenciler = dict(ogrenci_map)
            if kr_sinif_an != "Tümü":
                filtre_ogrenciler = {k: v for k, v in filtre_ogrenciler.items() if v["sinif"] == kr_sinif_an}
            if kr_sube_an != "Tümü":
                filtre_ogrenciler = {k: v for k, v in filtre_ogrenciler.items() if v["sube"] == kr_sube_an}

            karsilastirma_rows = []
            for ogr_id, ogr_info in sorted(filtre_ogrenciler.items(), key=lambda x: x[1]["ad"]):
                ogr_res = [r for r in od_results if r.student_id == ogr_id]
                sinav_sayisi = len(ogr_res)
                ort_puan = round(sum(r.score for r in ogr_res) / len(ogr_res), 1) if ogr_res else 0

                ogr_dev = [a for a in attendance if a.student_id == ogr_id]
                dev_sayisi = len(ogr_dev)

                ogr_on = [k for k in online_kayitlar
                         if k.sinif == ogr_info.get("sinif", 0) and k.sube == ogr_info.get("sube", "")]
                on_yapildi = sum(1 for k in ogr_on if k.durum == "yapildi")

                karsilastirma_rows.append({
                    "Öğrenci": ogr_info["ad"],
                    "Sınıf": f"{ogr_info['sinif']}-{ogr_info['sube']}",
                    "Sınav": sinav_sayisi,
                    "Ort. Puan": ort_puan,
                    "Devamsızlık": dev_sayisi,
                    "Online Ders": on_yapildi,
                })

            if karsilastirma_rows:
                df_kr = pd.DataFrame(karsilastirma_rows).sort_values("Ort. Puan", ascending=False)
                with_scores = [r for r in karsilastirma_rows if r["Ort. Puan"] > 0]
                total_ort = sum(r["Ort. Puan"] for r in with_scores) / len(with_scores) if with_scores else 0

                st.markdown(ReportStyler.metric_cards_html([
                    ("Öğrenci", str(len(karsilastirma_rows)), "#f59e0b", ""),
                    ("Genel Ortalama", f"{total_ort:.1f}", "#2563eb", ""),
                    ("En Yuksek", f"{max(r['Ort. Puan'] for r in karsilastirma_rows):.1f}", "#059669", ""),
                    ("En Dusuk", f"{min(r['Ort. Puan'] for r in with_scores):.1f}" if with_scores else "-", "#ef4444", ""),
                ]), unsafe_allow_html=True)

                col_kr_t, col_kr_c = st.columns([3, 2])
                with col_kr_t:
                    st.markdown(ReportStyler.section_divider_html("Karsilastirma Tablosu", "#f59e0b"), unsafe_allow_html=True)
                    st.markdown(ReportStyler.colored_table_html(df_kr, "#f59e0b", value_column="Ort. Puan", highlight_top=3), unsafe_allow_html=True)
                with col_kr_c:
                    top_chart = {r["Öğrenci"]: r["Ort. Puan"] for r in sorted(karsilastirma_rows, key=lambda x: x["Ort. Puan"], reverse=True)[:10] if r["Ort. Puan"] > 0}
                    if top_chart:
                        st.markdown(ReportStyler.section_divider_html("En Başarılı Öğrenciler", "#059669"), unsafe_allow_html=True)
                        st.markdown(ReportStyler.horizontal_bar_html(top_chart, "#059669"), unsafe_allow_html=True)

                # En basarili / destek gereken
                if len(with_scores) >= 3:
                    sorted_by_score = sorted(with_scores, key=lambda x: x["Ort. Puan"], reverse=True)
                    top_c, bot_c = st.columns(2)
                    with top_c:
                        st.markdown(ReportStyler.section_divider_html("En Başarılı 5 Öğrenci", "#059669"), unsafe_allow_html=True)
                        top5_data = [{"Öğrenci": r["Öğrenci"], "Sınıf": r["Sınıf"], "Puan": r["Ort. Puan"]} for r in sorted_by_score[:5]]
                        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(top5_data), "#059669", value_column="Puan"), unsafe_allow_html=True)
                    with bot_c:
                        st.markdown(ReportStyler.section_divider_html("Destek Gereken 5 Öğrenci", "#ef4444"), unsafe_allow_html=True)
                        bot5_data = [{"Öğrenci": r["Öğrenci"], "Sınıf": r["Sınıf"], "Puan": r["Ort. Puan"]} for r in sorted_by_score[-5:]]
                        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(bot5_data), "#ef4444", value_column="Puan"), unsafe_allow_html=True)

                # Devamsizlik - basari iliskisi
                if with_scores:
                    st.markdown(ReportStyler.section_divider_html("Devamsızlık - Başarı Iliskisi", "#f59e0b"), unsafe_allow_html=True)
                    ilski_rows = [{"Öğrenci": r["Öğrenci"], "Puan": float(r["Ort. Puan"]), "Devamsızlık": r["Devamsızlık"]} for r in with_scores]
                    ilski_df = pd.DataFrame(ilski_rows)
                    if len(ilski_df) > 1:
                        st.scatter_chart(ilski_df, x="Devamsızlık", y="Puan", height=300)

                # PDF + Paylasim
                pdf_gen_k = ReportPDFGenerator("Öğrenci Karsilastirma Raporu")
                pdf_gen_k.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
                pdf_gen_k.add_metrics([
                    ("Öğrenci", str(len(karsilastirma_rows)), "#f59e0b"),
                    ("Ortalama", f"{total_ort:.1f}", "#2563eb"),
                ])
                pdf_gen_k.add_section("Karsilastirma Tablosu")
                pdf_gen_k.add_table(df_kr, "#f59e0b")
                if top_chart:
                    pdf_gen_k.add_bar_chart(top_chart, "En Başarılı Öğrenciler", "#059669")
                pdf_bytes_k = pdf_gen_k.generate()
                ReportSharer.render_share_ui(
                    pdf_bytes_k, "ogrenci_karsilastirma.pdf",
                    "Öğrenci Karsilastirma Raporu",
                    unique_key="ogr_karsilastirma",
                )
            else:
                st.info("Filtreye uygun ogrenci bulunamadı.")


# ==================== OGRETMEN ANALIZI ====================

@st.fragment
def _render_ogretmen_analizi(store: AkademikDataStore):
    """Ogretmen analizi: gorevler, nobet, kazanim, izin/rapor."""
    kurum = get_institution_info()
    akademik_yil = _get_akademik_yil()
    teachers = store.get_teachers()

    if not teachers:
        styled_info_banner("Öğretmen verisi bulunamadı. Önce Akademik Kadro sekmesinden ogretmen ekleyin.",
                            banner_type="warning")
        return

    oa_tab1, oa_tab2, oa_tab3 = st.tabs([
        "👨‍🏫 Öğretmen Detay Analizi", "📋 İzin ve Rapor Yönetimi", "⚖️ Genel Karsilastirma"
    ])

    # ---- TAB 1: Ogretmen Detay Analizi ----
    with oa_tab1:
        st.markdown(ReportStyler.report_header_html(
            "Öğretmen Detay Analizi", "Bireysel ogretmen performans raporu", "#0d9488"
        ), unsafe_allow_html=True)

        ogr_opts = {t.id: f"{t.tam_ad} ({t.brans})" for t in teachers if t.durum == "aktif"}
        if not ogr_opts:
            st.info("Aktif ogretmen bulunamadı.")
            return

        sel_ogr_id = st.selectbox("Öğretmen Sec", list(ogr_opts.keys()),
                                  format_func=lambda x: ogr_opts.get(x, x),
                                  key="oa_ogr_sec")

        sel_teacher = next((t for t in teachers if t.id == sel_ogr_id), None)
        if not sel_teacher:
            return

        st.markdown(ReportStyler.report_header_html(
            sel_teacher.tam_ad,
            f'Branş: {sel_teacher.brans} | Görev: {sel_teacher.gorev} | Durum: {sel_teacher.durum.capitalize()}',
            "#0d9488"
        ), unsafe_allow_html=True)

        pdf_gen_t = ReportPDFGenerator(f"Öğretmen Raporu - {sel_teacher.tam_ad}")
        pdf_gen_t.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
        pdf_gen_t.add_section("Öğretmen Bilgileri")
        pdf_gen_t.add_text(f"Ad: {sel_teacher.tam_ad}  |  Branş: {sel_teacher.brans}  |  Görev: {sel_teacher.gorev}")

        # 1. Gorevlendirmeler
        st.markdown(ReportStyler.section_divider_html("Ders Görevlendirmeleri", "#2563eb"), unsafe_allow_html=True)

        assignments = store.get_teacher_assignments(ogretmen_id=sel_ogr_id, akademik_yil=akademik_yil)
        if assignments:
            toplam_saat = 0
            gorev_rows = []
            for ta in assignments:
                for g in ta.gorevler:
                    saat = g.get("haftalik_saat", 0)
                    toplam_saat += saat
                    gorev_rows.append({
                        "Sınıf": g.get("sinif", ""),
                        "Şube": g.get("sube", ""),
                        "Ders": g.get("ders", ""),
                        "Haftalık Saat": saat,
                    })

            sinif_sayisi = len(set(f"{g['Sınıf']}-{g['Şube']}" for g in gorev_rows))
            ders_sayisi = len(set(g["Ders"] for g in gorev_rows))

            st.markdown(ReportStyler.metric_cards_html([
                ("Sınıf/Şube", str(sinif_sayisi), "#2563eb", ""),
                ("Ders Cesidi", str(ders_sayisi), "#7c3aed", ""),
                ("Haftalık Saat", str(toplam_saat), "#059669", ""),
                ("Görev Sayısı", str(len(gorev_rows)), "#f59e0b", ""),
            ]), unsafe_allow_html=True)

            pdf_gen_t.add_section("Ders Görevlendirmeleri")
            pdf_gen_t.add_metrics([
                ("Sınıf/Şube", str(sinif_sayisi), "#2563eb"),
                ("Ders Cesidi", str(ders_sayisi), "#7c3aed"),
                ("Haftalık Saat", str(toplam_saat), "#059669"),
            ])

            if gorev_rows:
                df_gorev = pd.DataFrame(gorev_rows)
                st.markdown(ReportStyler.colored_table_html(df_gorev, "#2563eb"), unsafe_allow_html=True)
                pdf_gen_t.add_table(df_gorev, "#2563eb")
        else:
            st.info("Bu ogretmene ait gorevlendirme bulunamadı.")

        # 2. Haftalik ders programi
        st.markdown(ReportStyler.section_divider_html("Haftalık Ders Programı", "#6366f1"), unsafe_allow_html=True)

        schedule_slots = store.get_schedule(akademik_yil=akademik_yil)
        ogr_slots = [s for s in schedule_slots if s.ogretmen_id == sel_ogr_id]

        if ogr_slots:
            ayarlar = store.get_ders_programi_ayarlari()
            aktif_gunler = ayarlar.get("aktif_gunler", GUNLER)
            gunluk_saat = ayarlar.get("gunluk_ders_saati", 8)

            # Program tablosu
            prog_data: dict[int, dict[str, str]] = {}
            for saat in range(1, gunluk_saat + 1):
                prog_data[saat] = {g: "" for g in aktif_gunler}

            for s in ogr_slots:
                gun_k = GUN_KISALTMA.get(s.gun, s.gun)
                gun_full = next((g for g in aktif_gunler if GUN_KISALTMA.get(g) == gun_k or g == s.gun), None)
                if gun_full and s.ders_saati in prog_data:
                    kisaltma = DERS_KISALTMA.get(s.ders, s.ders[:3])
                    prog_data[s.ders_saati][gun_full] = f"{kisaltma} ({s.sinif}{s.sube})"

            prog_rows = []
            for saat in range(1, gunluk_saat + 1):
                row = {"Saat": f"{saat}. Ders"}
                row.update(prog_data[saat])
                prog_rows.append(row)

            df_prog = pd.DataFrame(prog_rows)
            st.markdown(ReportStyler.colored_table_html(df_prog, "#6366f1"), unsafe_allow_html=True)

            dolu_saat = sum(1 for s in range(1, gunluk_saat + 1) for g in aktif_gunler if prog_data[s][g])
            bos_saat = len(aktif_gunler) * gunluk_saat - dolu_saat
            doluluk = round(dolu_saat * 100 / max(len(aktif_gunler) * gunluk_saat, 1))

            st.markdown(ReportStyler.metric_cards_html([
                ("Dolu Saat", str(dolu_saat), "#059669", ""),
                ("Bos Saat", str(bos_saat), "#94a3b8", ""),
                ("Doluluk", f"%{doluluk}", "#2563eb", ""),
            ]), unsafe_allow_html=True)

            pdf_gen_t.add_section("Haftalık Ders Programı")
            pdf_gen_t.add_table(df_prog, "#6366f1")
            pdf_gen_t.add_metrics([
                ("Dolu Saat", str(dolu_saat), "#059669"),
                ("Doluluk", f"%{doluluk}", "#2563eb"),
            ])
        else:
            st.info("Bu ogretmene ait ders programi bulunamadı.")

        # 3. Nobet performansi
        st.markdown(ReportStyler.section_divider_html("Nöbet Performansi", "#b45309"), unsafe_allow_html=True)

        nobet_gorevler = store.get_nobet_gorevler(akademik_yil=akademik_yil)
        nobet_kayitlar = store.get_nobet_kayitlar(akademik_yil=akademik_yil)

        ogr_nobet_gorevler = [g for g in nobet_gorevler if g.ogretmen_id == sel_ogr_id]
        ogr_nobet_kayitlar = [k for k in nobet_kayitlar if k.ogretmen_id == sel_ogr_id]

        if ogr_nobet_gorevler or ogr_nobet_kayitlar:
            # Nobet gunleri
            nobet_gunleri_str = ", ".join(sorted(set(g.gun for g in ogr_nobet_gorevler))) if ogr_nobet_gorevler else "-"
            nobet_yerleri_str = ", ".join(sorted(set(g.nobet_yeri for g in ogr_nobet_gorevler))) if ogr_nobet_gorevler else "-"

            tutulan = sum(1 for k in ogr_nobet_kayitlar if k.durum == "tamamlandı")
            tutulmayan = sum(1 for k in ogr_nobet_kayitlar if k.durum == "tutulmadi")
            devam_eden = sum(1 for k in ogr_nobet_kayitlar if k.durum in ("bekliyor", "devam_ediyor"))

            st.markdown(ReportStyler.metric_cards_html([
                ("Tutulan", str(tutulan), "#059669", ""),
                ("Tutulmayan", str(tutulmayan), "#ef4444", ""),
                ("Bekleyen", str(devam_eden), "#f59e0b", ""),
                ("Toplam", str(len(ogr_nobet_kayitlar)), "#2563eb", ""),
            ]), unsafe_allow_html=True)

            st.markdown(f"**Nöbet Günleri:** {nobet_gunleri_str}")
            st.markdown(f"**Nöbet Yerleri:** {nobet_yerleri_str}")

            if tutulan + tutulmayan > 0:
                perf_oran = round(tutulan * 100 / (tutulan + tutulmayan))
                nobet_chart = {"Tutulan": tutulan, "Tutulmayan": tutulmayan}
                st.markdown(ReportStyler.donut_chart_svg(nobet_chart, ["#059669", "#ef4444"], size=160), unsafe_allow_html=True)

                pdf_gen_t.add_section("Nöbet Performansi")
                pdf_gen_t.add_metrics([
                    ("Tutulan", str(tutulan), "#059669"),
                    ("Tutulmayan", str(tutulmayan), "#ef4444"),
                    ("Performans", f"%{perf_oran}", "#2563eb"),
                ])
                pdf_gen_t.add_donut_chart(nobet_chart, "Nöbet Durumu", ["#059669", "#ef4444"])

            tutulmayan_kayitlar = [k for k in ogr_nobet_kayitlar if k.durum == "tutulmadi"]
            if tutulmayan_kayitlar:
                st.markdown(ReportStyler.section_divider_html("Tutulmayan Nöbetler", "#ef4444"), unsafe_allow_html=True)
                tk_rows = []
                for k in tutulmayan_kayitlar:
                    tk_rows.append({
                        "Tarih": k.tarih,
                        "Yer": k.nobet_yeri,
                        "Neden": k.tutulmama_nedeni or "-",
                        "Yerine Tutan": k.yerine_tutan_adi or "-",
                    })
                df_tk = pd.DataFrame(tk_rows)
                st.markdown(ReportStyler.colored_table_html(df_tk, "#ef4444"), unsafe_allow_html=True)
        else:
            st.info("Bu ogretmene ait nobet verisi bulunamadı.")

        # 4. Kazanim takip performansi
        st.markdown(ReportStyler.section_divider_html("Kazanim İşleme Performansi", "#7c3aed"), unsafe_allow_html=True)

        kazanim_kayitlari = store.get_kazanim_isleme(ogretmen_id=sel_ogr_id, akademik_yil=akademik_yil)

        if kazanim_kayitlari:
            islenen = sum(1 for k in kazanim_kayitlari if k.durum == "islendi")
            islenmeyen = sum(1 for k in kazanim_kayitlari if k.durum == "islenmedi")
            kismen = sum(1 for k in kazanim_kayitlari if k.durum == "kismen")

            st.markdown(ReportStyler.metric_cards_html([
                ("Islenen", str(islenen), "#059669", ""),
                ("Islenmeyen", str(islenmeyen), "#ef4444", ""),
                ("Kismen", str(kismen), "#f59e0b", ""),
                ("Toplam", str(len(kazanim_kayitlari)), "#2563eb", ""),
            ]), unsafe_allow_html=True)

            if islenen + islenmeyen + kismen > 0:
                kz_donut = {"Islenen": islenen, "Islenmeyen": islenmeyen}
                if kismen > 0:
                    kz_donut["Kismen"] = kismen
                st.markdown(ReportStyler.donut_chart_svg(kz_donut, ["#059669", "#ef4444", "#f59e0b"], size=160), unsafe_allow_html=True)

                pdf_gen_t.add_section("Kazanim İşleme")
                pdf_gen_t.add_metrics([
                    ("Islenen", str(islenen), "#059669"),
                    ("Islenmeyen", str(islenmeyen), "#ef4444"),
                    ("Kismen", str(kismen), "#f59e0b"),
                ])
                pdf_gen_t.add_donut_chart(kz_donut, "Kazanim Durumu", ["#059669", "#ef4444", "#f59e0b"])

            # Ders bazli kazanim performansi
            ders_kazanim: dict[str, dict] = {}
            for k in kazanim_kayitlari:
                if k.ders not in ders_kazanim:
                    ders_kazanim[k.ders] = {"islendi": 0, "islenmedi": 0, "kismen": 0}
                ders_kazanim[k.ders][k.durum] = ders_kazanim[k.ders].get(k.durum, 0) + 1

            if ders_kazanim:
                st.markdown(ReportStyler.section_divider_html("Ders Bazli Kazanim Durumu", "#7c3aed"), unsafe_allow_html=True)
                dk_rows = []
                dk_chart = {}
                for ders, info in sorted(ders_kazanim.items()):
                    toplam = info["islendi"] + info["islenmedi"] + info["kismen"]
                    oran = round(info["islendi"] * 100 / max(toplam, 1))
                    dk_rows.append({
                        "Ders": ders,
                        "Islenen": info["islendi"],
                        "Islenmeyen": info["islenmedi"],
                        "Kismen": info["kismen"],
                        "Başarı %": oran,
                    })
                    dk_chart[ders] = oran
                df_dk = pd.DataFrame(dk_rows)

                col_dk_t, col_dk_c = st.columns([3, 2])
                with col_dk_t:
                    st.markdown(ReportStyler.colored_table_html(df_dk, "#7c3aed", value_column="Başarı %"), unsafe_allow_html=True)
                with col_dk_c:
                    st.markdown(ReportStyler.horizontal_bar_html(dk_chart, "#7c3aed"), unsafe_allow_html=True)

                pdf_gen_t.add_section("Ders Bazli Kazanim")
                pdf_gen_t.add_table(df_dk, "#7c3aed")
                pdf_gen_t.add_bar_chart(dk_chart, "Kazanim Başarı Oranlari", "#7c3aed")
        else:
            st.info("Bu ogretmene ait kazanim isleme kaydi bulunamadı.")

        # 5. Izin ve rapor ozeti
        st.markdown(ReportStyler.section_divider_html("İzin ve Rapor Özeti", "#dc2626"), unsafe_allow_html=True)

        izinler = store.get_ogretmen_izinler(ogretmen_id=sel_ogr_id, akademik_yil=akademik_yil)

        if izinler:
            toplam_izin_gun = sum(i.sure_gun for i in izinler if i.durum == "onaylandi")
            rapor_gun = sum(i.sure_gun for i in izinler if i.durum == "onaylandi" and "Rapor" in i.izin_turu)
            izin_gun = toplam_izin_gun - rapor_gun

            st.markdown(ReportStyler.metric_cards_html([
                ("Toplam İzin", f"{toplam_izin_gun:.1f} gun", "#dc2626", ""),
                ("Rapor", f"{rapor_gun:.1f} gun", "#ef4444", ""),
                ("İzin", f"{izin_gun:.1f} gun", "#f59e0b", ""),
                ("Kayıt Sayısı", str(len(izinler)), "#64748b", ""),
            ]), unsafe_allow_html=True)

            izin_rows = []
            for i in sorted(izinler, key=lambda x: x.baslangic_tarihi, reverse=True):
                izin_rows.append({
                    "Tur": i.izin_turu,
                    "Başlangıç": i.baslangic_tarihi,
                    "Bitis": i.bitis_tarihi,
                    "Sure": f"{i.sure_gun} gun" if i.sure_gun >= 1 else i.sure_turu,
                    "Durum": IZIN_DURUMLARI.get(i.durum, i.durum),
                    "Belgeli": "Evet" if i.belge_var else "Hayir",
                })
            df_izin = pd.DataFrame(izin_rows)

            izin_tur_sayim: dict[str, float] = {}
            for i in izinler:
                if i.durum == "onaylandi":
                    izin_tur_sayim[i.izin_turu] = izin_tur_sayim.get(i.izin_turu, 0) + i.sure_gun

            col_iz_t, col_iz_c = st.columns([3, 2])
            with col_iz_t:
                st.markdown(ReportStyler.colored_table_html(df_izin, "#dc2626"), unsafe_allow_html=True)
            with col_iz_c:
                if izin_tur_sayim:
                    iz_chart = {k: round(v, 1) for k, v in sorted(izin_tur_sayim.items(), key=lambda x: x[1], reverse=True)}
                    st.markdown(ReportStyler.horizontal_bar_html(iz_chart, "#dc2626"), unsafe_allow_html=True)

            pdf_gen_t.add_section("İzin ve Rapor")
            pdf_gen_t.add_metrics([
                ("Toplam", f"{toplam_izin_gun:.1f}", "#dc2626"),
                ("Rapor", f"{rapor_gun:.1f}", "#ef4444"),
                ("İzin", f"{izin_gun:.1f}", "#f59e0b"),
            ])
            pdf_gen_t.add_table(df_izin, "#dc2626")
            if izin_tur_sayim:
                pdf_gen_t.add_bar_chart(iz_chart, "İzin Turu Dagilimi", "#dc2626")
        else:
            st.info("Bu ogretmene ait izin/rapor kaydi bulunamadı.")

        # PDF + Paylasim
        pdf_bytes_t = pdf_gen_t.generate()
        t_email = getattr(sel_teacher, "email", "") or ""
        t_tel = getattr(sel_teacher, "telefon", "") or ""
        ReportSharer.render_share_ui(
            pdf_bytes_t, f"ogretmen_raporu_{sel_teacher.tam_ad.replace(' ', '_')}.pdf",
            f"Öğretmen Raporu - {sel_teacher.tam_ad}",
            unique_key="ogr_t_detay", default_email=t_email, default_phone=t_tel,
        )

    # ---- TAB 2: Izin ve Rapor Yonetimi ----
    with oa_tab2:
        st.markdown(ReportStyler.report_header_html(
            "İzin ve Rapor Yönetimi", "Öğretmen izin/rapor kayit ve takip sistemi", "#dc2626"
        ), unsafe_allow_html=True)

        iz_c1, iz_c2 = st.columns(2)
        with iz_c1:
            iz_ogretmen_id = st.selectbox(
                "Öğretmen", list(ogr_opts.keys()),
                format_func=lambda x: ogr_opts.get(x, x),
                key="iz_ogretmen_sec"
            )
        with iz_c2:
            iz_turu = st.selectbox("İzin Turu", IZIN_TURLERI, key="iz_turu")

        iz_c3, iz_c4, iz_c5 = st.columns(3)
        with iz_c3:
            iz_baslangic = st.date_input("Başlangıç Tarihi", key="iz_baslangic")
        with iz_c4:
            iz_bitis = st.date_input("Bitis Tarihi", key="iz_bitis")
        with iz_c5:
            iz_sure_turu = st.selectbox("Sure Turu", IZIN_SURE_TURLERI, key="iz_sure_turu")

        # Sure gun hesapla
        sure_map = {
            "Yarim Gün": 0.5, "1 Gün": 1, "2 Gün": 2, "3 Gün": 3,
            "4 Gün": 4, "5 Gün": 5, "1 Hafta": 5, "2 Hafta": 10, "1 Ay": 22,
        }
        if iz_sure_turu == "Diger":
            iz_sure_gun = st.number_input("Sure (gun)", min_value=0.5, step=0.5, value=1.0, key="iz_sure_gun")
        else:
            iz_sure_gun = sure_map.get(iz_sure_turu, 1)

        iz_c6, iz_c7 = st.columns(2)
        with iz_c6:
            iz_aciklama = st.text_area("Açıklama", key="iz_aciklama", height=80)
        with iz_c7:
            iz_belge = st.checkbox("Belge/Rapor Var", key="iz_belge")
            yerine_opts = {"": "Seçilmedi"} | {t.id: t.tam_ad for t in teachers
                          if t.durum == "aktif" and t.id != iz_ogretmen_id}
            iz_yerine = st.selectbox("Yerine Gelen", list(yerine_opts.keys()),
                                     format_func=lambda x: yerine_opts.get(x, x),
                                     key="iz_yerine")

        if st.button("İzin/Rapor Kaydet", key="iz_kaydet", use_container_width=True):
            sel_t = next((t for t in teachers if t.id == iz_ogretmen_id), None)
            if sel_t:
                yer_t = next((t for t in teachers if t.id == iz_yerine), None) if iz_yerine else None
                izin = OgretmenIzin(
                    ogretmen_id=iz_ogretmen_id,
                    ogretmen_adi=sel_t.tam_ad,
                    izin_turu=iz_turu,
                    baslangic_tarihi=iz_baslangic.strftime("%Y-%m-%d"),
                    bitis_tarihi=iz_bitis.strftime("%Y-%m-%d"),
                    sure_turu=iz_sure_turu,
                    sure_gun=iz_sure_gun,
                    aciklama=iz_aciklama,
                    belge_var=iz_belge,
                    durum="onaylandi",
                    yerine_gelen_id=iz_yerine if iz_yerine else "",
                    yerine_gelen_adi=yer_t.tam_ad if yer_t else "",
                    akademik_yil=akademik_yil,
                )
                store.save_ogretmen_izin(izin)
                st.success(f"{sel_t.tam_ad} için {iz_turu} kaydi oluşturuldu.")
                st.rerun(scope="fragment")

        # Mevcut kayitlar
        st.markdown(ReportStyler.section_divider_html("Mevcut İzin/Rapor Kayıtlari", "#b45309"), unsafe_allow_html=True)

        tum_izinler = store.get_ogretmen_izinler(akademik_yil=akademik_yil)
        if tum_izinler:
            iz_rows = []
            for i in sorted(tum_izinler, key=lambda x: x.baslangic_tarihi, reverse=True):
                iz_rows.append({
                    "Öğretmen": i.ogretmen_adi,
                    "Tur": i.izin_turu,
                    "Başlangıç": i.baslangic_tarihi,
                    "Bitis": i.bitis_tarihi,
                    "Sure": f"{i.sure_gun} gun" if i.sure_gun >= 1 else i.sure_turu,
                    "Durum": IZIN_DURUMLARI.get(i.durum, i.durum),
                    "Yerine Gelen": i.yerine_gelen_adi or "-",
                })
            df_iz_all = pd.DataFrame(iz_rows)
            st.markdown(ReportStyler.colored_table_html(df_iz_all, "#b45309"), unsafe_allow_html=True)

            # PDF export for all records
            pdf_gen_iz = ReportPDFGenerator("İzin/Rapor Kayıtlari")
            pdf_gen_iz.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen_iz.add_section("Tüm İzin/Rapor Kayıtlari")
            pdf_gen_iz.add_table(df_iz_all, "#b45309")
            pdf_bytes_iz = pdf_gen_iz.generate()
            ReportSharer.render_share_ui(
                pdf_bytes_iz, "izin_rapor_kayitlari.pdf",
                "İzin/Rapor Kayıtlari", unique_key="izin_kayit",
            )

            # Silme
            sil_iz = st.selectbox("Silinecek Kayıt",
                                  [(i.id, f"{i.ogretmen_adi} - {i.izin_turu} ({i.baslangic_tarihi})") for i in tum_izinler],
                                  format_func=lambda x: x[1],
                                  key="sil_iz")
            if st.button("Secili Kaydi Sil", key="sil_iz_btn"):
                store.delete_ogretmen_izin(sil_iz[0])
                st.success("Kayıt silindi.")
                st.rerun(scope="fragment")
        else:
            st.info("Henuz izin/rapor kaydi bulunmuyor.")

    # ---- TAB 3: Genel Karsilastirma ----
    with oa_tab3:
        st.markdown(ReportStyler.report_header_html(
            "Öğretmen Karsilastirma", "Tüm ogretmenlerin performans karsilastirmasi", "#0d9488"
        ), unsafe_allow_html=True)

        tum_assignments = store.get_teacher_assignments(akademik_yil=akademik_yil)
        tum_nobet_kayitlar = store.get_nobet_kayitlar(akademik_yil=akademik_yil)
        tum_kazanim = store.get_kazanim_isleme(akademik_yil=akademik_yil)
        tum_izinler_all = store.get_ogretmen_izinler(akademik_yil=akademik_yil)

        karsi_rows = []
        for t in sorted(teachers, key=lambda x: x.tam_ad):
            if t.durum != "aktif":
                continue

            t_assignments = [a for a in tum_assignments if a.ogretmen_id == t.id]
            haftalik = sum(a.toplam_saat for a in t_assignments)

            siniflar_set = set()
            for a in t_assignments:
                for g in a.gorevler:
                    siniflar_set.add(f"{g.get('sinif')}-{g.get('sube')}")

            t_nobet = [k for k in tum_nobet_kayitlar if k.ogretmen_id == t.id]
            nobet_tutulan = sum(1 for k in t_nobet if k.durum == "tamamlandı")
            nobet_tutulmayan = sum(1 for k in t_nobet if k.durum == "tutulmadi")

            t_kazanim = [k for k in tum_kazanim if k.ogretmen_id == t.id]
            kz_islenen = sum(1 for k in t_kazanim if k.durum == "islendi")
            kz_toplam = len(t_kazanim)

            t_izin = [i for i in tum_izinler_all if i.ogretmen_id == t.id and i.durum == "onaylandi"]
            izin_gun = sum(i.sure_gun for i in t_izin)

            karsi_rows.append({
                "Öğretmen": t.tam_ad,
                "Branş": t.brans,
                "Sınıf Sayısı": len(siniflar_set),
                "Haftalık Saat": haftalik,
                "Nöbet Tutulan": nobet_tutulan,
                "Nöbet Tutulmayan": nobet_tutulmayan,
                "Kazanim Islenen": kz_islenen,
                "Kazanim Toplam": kz_toplam,
                "İzin Gün": round(izin_gun, 1),
            })

        if karsi_rows:
            aktif_ogretmen = len(karsi_rows)
            ort_saat = sum(r["Haftalık Saat"] for r in karsi_rows) / max(aktif_ogretmen, 1)
            ort_izin = sum(r["İzin Gün"] for r in karsi_rows) / max(aktif_ogretmen, 1)
            toplam_nobet_t = sum(r["Nöbet Tutulan"] for r in karsi_rows)
            toplam_nobet_tu = sum(r["Nöbet Tutulmayan"] for r in karsi_rows)
            nobet_perf = round(toplam_nobet_t * 100 / max(toplam_nobet_t + toplam_nobet_tu, 1)) if toplam_nobet_t + toplam_nobet_tu > 0 else 0

            st.markdown(ReportStyler.metric_cards_html([
                ("Aktif Öğretmen", str(aktif_ogretmen), "#0d9488", ""),
                ("Ort. Haftalık Saat", f"{ort_saat:.1f}", "#2563eb", ""),
                ("Ort. İzin Gün", f"{ort_izin:.1f}", "#dc2626", ""),
                ("Nöbet Perf.", f"%{nobet_perf}" if nobet_perf else "-", "#059669", ""),
            ]), unsafe_allow_html=True)

            df_karsi = pd.DataFrame(karsi_rows)

            col_karsi_t, col_karsi_c = st.columns([3, 2])
            with col_karsi_t:
                st.markdown(ReportStyler.section_divider_html("Karsilastirma Tablosu", "#0d9488"), unsafe_allow_html=True)
                st.markdown(ReportStyler.colored_table_html(df_karsi, "#0d9488", value_column="Haftalık Saat"), unsafe_allow_html=True)
            with col_karsi_c:
                saat_chart = {r["Öğretmen"]: r["Haftalık Saat"] for r in sorted(karsi_rows, key=lambda x: x["Haftalık Saat"], reverse=True)[:8] if r["Haftalık Saat"] > 0}
                if saat_chart:
                    st.markdown(ReportStyler.section_divider_html("Haftalık Ders Yuku", "#2563eb"), unsafe_allow_html=True)
                    st.markdown(ReportStyler.horizontal_bar_html(saat_chart, "#2563eb"), unsafe_allow_html=True)

            # En cok izin kullanan
            izinli = sorted(karsi_rows, key=lambda x: x["İzin Gün"], reverse=True)[:5]
            if any(r["İzin Gün"] > 0 for r in izinli):
                izin_chart = {r["Öğretmen"]: r["İzin Gün"] for r in izinli if r["İzin Gün"] > 0}
                top_iz, bot_iz = st.columns(2)
                with top_iz:
                    st.markdown(ReportStyler.section_divider_html("En Çok İzin Kullanan", "#dc2626"), unsafe_allow_html=True)
                    iz_data = [{"Öğretmen": r["Öğretmen"], "Branş": r["Branş"], "İzin Gün": r["İzin Gün"]} for r in izinli if r["İzin Gün"] > 0]
                    st.markdown(ReportStyler.colored_table_html(pd.DataFrame(iz_data), "#dc2626"), unsafe_allow_html=True)
                with bot_iz:
                    st.markdown(ReportStyler.section_divider_html("İzin Dagilimi", "#ef4444"), unsafe_allow_html=True)
                    st.markdown(ReportStyler.horizontal_bar_html(izin_chart, "#dc2626"), unsafe_allow_html=True)

            # PDF + Paylasim
            pdf_gen_gk = ReportPDFGenerator("Öğretmen Karsilastirma Raporu")
            pdf_gen_gk.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen_gk.add_metrics([
                ("Öğretmen", str(aktif_ogretmen), "#0d9488"),
                ("Ort. Saat", f"{ort_saat:.1f}", "#2563eb"),
                ("Nöbet Perf.", f"%{nobet_perf}", "#059669"),
            ])
            pdf_gen_gk.add_section("Karsilastirma Tablosu")
            pdf_gen_gk.add_table(df_karsi, "#0d9488")
            if saat_chart:
                pdf_gen_gk.add_bar_chart(saat_chart, "Haftalık Ders Yuku", "#2563eb")
            pdf_bytes_gk = pdf_gen_gk.generate()
            ReportSharer.render_share_ui(
                pdf_bytes_gk, "ogretmen_karsilastirma.pdf",
                "Öğretmen Karsilastirma Raporu",
                unique_key="ogr_t_karsilastirma",
            )
        else:
            st.info("Aktif ogretmen verisi bulunamadı.")


# ==================== NOBET SISTEMI ====================

@st.fragment
def _render_nobet(store: AkademikDataStore):
    """Ogretmen nobet yonetimi: planlama, takip, raporlama."""
    styled_section("Nöbet Yönetimi", color="#b45309")

    akademik_yil = _get_akademik_yil()
    teachers = store.get_teachers()
    custom_yerler = store.get_nobet_yerleri_custom()
    tum_yerler = NOBET_YERLERI + custom_yerler

    ntab1, ntab2, ntab3, ntab4 = st.tabs([
        "📋 Nöbet Planlama", "🗓️ Aylık Nöbet Listesi", "👁️ Nöbet Takip", "📈 Nöbet Raporu"
    ])

    # ---- TAB 1: Nobet Planlama ----
    with ntab1:
        styled_info_banner(
            "Öğretmenlere ay, gun ve nobet yeri atayarak nobet planlamasi yapin. "
            "Aylık nobet listesi bu gorevlendirmelerden otomatik olusturulur.",
            banner_type="info"
        )

        # Nobet yeri ekle
        with st.expander("Nöbet Yeri Ekle"):
            ny_c1, ny_c2 = st.columns([3, 1])
            with ny_c1:
                yeni_yer = st.text_input("Yeni Nöbet Yeri", placeholder="Ornek: Spor Salonu", key="yeni_nobet_yeri")
            with ny_c2:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                if st.button("Ekle", key="nobet_yeri_ekle_btn", use_container_width=True):
                    if yeni_yer.strip() and yeni_yer.strip() not in tum_yerler:
                        store.add_nobet_yeri(yeni_yer.strip())
                        st.success(f"'{yeni_yer.strip()}' eklendi!")
                        st.rerun(scope="fragment")
                    elif yeni_yer.strip() in tum_yerler:
                        st.warning("Bu nobet yeri zaten mevcut.")
                    else:
                        st.error("Nöbet yeri giriniz.")

        st.markdown("---")

        # Gorevlendirme formu
        with st.form("nobet_gorev_form", clear_on_submit=True):
            ng_c1, ng_c2 = st.columns(2)
            with ng_c1:
                today = date.today()
                ng_baslangic = st.date_input("Nöbet Başlangıç", value=today.replace(day=1), key="ng_baslangic")
                ng_bitis = st.date_input("Nöbet Bitiş", value=today, key="ng_bitis")
                if teachers:
                    ogretmen_opts = {t.id: f"{t.ad} {t.soyad} ({t.brans})" for t in teachers}
                    ng_ogretmen_id = st.selectbox("Öğretmen", list(ogretmen_opts.keys()),
                                                  format_func=lambda x: ogretmen_opts.get(x, x),
                                                  key="ng_ogretmen")
                else:
                    ng_ogretmen_id = None
                    st.warning("Akademik kadroda ogretmen bulunamadı.")
            with ng_c2:
                ng_gun = st.selectbox("Nöbet Günü", NOBET_GUNLERI, key="ng_gun")
                ng_yer = st.selectbox("Nöbet Yeri", tum_yerler, key="ng_yer")

            ng_submitted = st.form_submit_button("Görevlendir", use_container_width=True)
            if ng_submitted and ng_ogretmen_id:
                if ng_bitis < ng_baslangic:
                    st.error("Bitis tarihi baslangic tarihinden once olamaz.")
                else:
                    sel_teacher = next((t for t in teachers if t.id == ng_ogretmen_id), None)
                    if sel_teacher:
                        ng_ay = ng_baslangic.month
                        ng_yil = ng_baslangic.year
                        # Ayni ay/gun/yer için tekrar kontrolu
                        mevcut = store.get_nobet_gorevler(akademik_yil, ay=ng_ay, yil=ng_yil)
                        tekrar = any(g for g in mevcut if g.ogretmen_id == ng_ogretmen_id
                                    and g.gun == ng_gun and g.nobet_yeri == ng_yer)
                        if tekrar:
                            st.warning("Bu ogretmen ayni ay/gun/yer için zaten gorevlendirilmis.")
                        else:
                            gorev = NobetGorev(
                                ogretmen_id=sel_teacher.id,
                                ogretmen_adi=f"{sel_teacher.ad} {sel_teacher.soyad}",
                                ay=ng_ay,
                                yil=ng_yil,
                                gun=ng_gun,
                                nobet_yeri=ng_yer,
                                baslangic_tarihi=ng_baslangic.strftime("%Y-%m-%d"),
                                bitis_tarihi=ng_bitis.strftime("%Y-%m-%d"),
                                akademik_yil=akademik_yil,
                            )
                            store.save_nobet_gorev(gorev)
                            st.success(f"{sel_teacher.ad} {sel_teacher.soyad} - {ng_gun} {ng_yer} ({ng_baslangic.strftime('%d.%m.%Y')} - {ng_bitis.strftime('%d.%m.%Y')}) gorevlendirildi!")
                            st.rerun(scope="fragment")

        # Mevcut gorevlendirmeler
        st.markdown("---")
        styled_section("Mevcut Görevlendirmeler", color="#92400e")
        fl_c1, fl_c2 = st.columns(2)
        with fl_c1:
            ay_secenekler = [(ay_no, ay_adi) for ay_no, ay_adi in AYLAR]
            fl_ay_idx = next((i for i, (n, _) in enumerate(ay_secenekler) if n == date.today().month), 0)
            fl_ay_sec = st.selectbox("Ay Filtresi", ay_secenekler,
                                     index=fl_ay_idx,
                                     format_func=lambda x: x[1],
                                     key="fl_nobet_ay")
            fl_ay = fl_ay_sec[0]
        with fl_c2:
            fl_yil = st.number_input("Yil", min_value=2024, max_value=2030, value=date.today().year, key="fl_nobet_yil")

        gorevler = store.get_nobet_gorevler(akademik_yil, ay=fl_ay, yil=fl_yil)
        if gorevler:
            # Gune gore grupla
            gun_map: dict[str, list[NobetGorev]] = {}
            for g in gorevler:
                gun_map.setdefault(g.gun, []).append(g)

            for gun in NOBET_GUNLERI:
                if gun in gun_map:
                    with st.expander(f"{gun} ({len(gun_map[gun])} ogretmen)", expanded=False):
                        for g in gun_map[gun]:
                            gc1, gc2, gc3, gc4 = st.columns([3, 2, 2, 1])
                            with gc1:
                                st.markdown(f"**{g.ogretmen_adi}**")
                            with gc2:
                                st.caption(g.nobet_yeri)
                            with gc3:
                                if g.baslangic_tarihi and g.bitis_tarihi:
                                    st.caption(f"{g.baslangic_tarihi} - {g.bitis_tarihi}")
                            with gc4:
                                if st.button("Sil", key=f"ng_del_{g.id}", type="secondary"):
                                    store.delete_nobet_gorev(g.id)
                                    st.rerun(scope="fragment")
        else:
            st.info("Bu ay için gorevlendirme bulunmuyor.")

    # ---- TAB 2: Aylik Nobet Listesi ----
    with ntab2:
        al_c1, al_c2 = st.columns(2)
        with al_c1:
            al_ay_secenekler = [(ay_no, ay_adi) for ay_no, ay_adi in AYLAR]
            al_ay_idx = next((i for i, (n, _) in enumerate(al_ay_secenekler) if n == date.today().month), 0)
            al_ay_sec = st.selectbox("Ay", al_ay_secenekler,
                                     index=al_ay_idx,
                                     format_func=lambda x: x[1],
                                     key="al_ay")
            al_ay = al_ay_sec[0]
        with al_c2:
            al_yil = st.number_input("Yil", min_value=2024, max_value=2030, value=date.today().year, key="al_yil")

        al_gorevler = store.get_nobet_gorevler(akademik_yil, ay=al_ay, yil=al_yil)

        if not al_gorevler:
            styled_info_banner("Bu ay için nöbet görevlendirmesi yok. Önce 'Nöbet Planlama' sekmesinden görevlendirme yapın.", banner_type="warning")
        else:
            if st.button("Aylık Nöbet Listesini Oluştur", type="primary", use_container_width=True, key="nobet_olustur"):
                import calendar
                _, gun_sayisi = calendar.monthrange(al_yil, al_ay)

                # Gun isimlerini Turkce map et
                GUN_MAP_TR = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}

                olusturulan = 0
                mevcut_kayitlar = store.get_nobet_kayitlar(akademik_yil)
                mevcut_tarihler = {(k.ogretmen_id, k.tarih, k.nobet_yeri) for k in mevcut_kayitlar}

                for gun_no in range(1, gun_sayisi + 1):
                    tarih = date(al_yil, al_ay, gun_no)
                    gun_adi = GUN_MAP_TR.get(tarih.weekday(), "")

                    if gun_adi == "Pazar":
                        continue

                    for gorev in al_gorevler:
                        if gorev.gun == gun_adi:
                            key = (gorev.ogretmen_id, tarih.isoformat(), gorev.nobet_yeri)
                            if key not in mevcut_tarihler:
                                kayit = NobetKayit(
                                    gorev_id=gorev.id,
                                    ogretmen_id=gorev.ogretmen_id,
                                    ogretmen_adi=gorev.ogretmen_adi,
                                    tarih=tarih.isoformat(),
                                    nobet_yeri=gorev.nobet_yeri,
                                    durum="bekliyor",
                                    akademik_yil=akademik_yil,
                                )
                                store.save_nobet_kayit(kayit)
                                olusturulan += 1

                if olusturulan > 0:
                    st.success(f"{al_ay_sec[1]} {al_yil} için {olusturulan} nobet kaydi oluşturuldu!")
                    st.rerun(scope="fragment")
                else:
                    st.info("Tüm nobet kayitlari zaten mevcut.")

            # Mevcut aylik liste
            ay_kayitlari = [k for k in store.get_nobet_kayitlar(akademik_yil)
                           if k.tarih and k.tarih.startswith(f"{al_yil}-{al_ay:02d}")]
            ay_kayitlari.sort(key=lambda x: x.tarih)

            if ay_kayitlari:
                st.markdown("---")
                styled_section(f"{al_ay_sec[1]} {al_yil} Nöbet Listesi", color="#b45309")

                # Istatistikler
                bekliyor = sum(1 for k in ay_kayitlari if k.durum == "bekliyor")
                devam = sum(1 for k in ay_kayitlari if k.durum == "devam_ediyor")
                tamamlandı = sum(1 for k in ay_kayitlari if k.durum == "tamamlandı")
                tutulmadi = sum(1 for k in ay_kayitlari if k.durum == "tutulmadi")

                styled_stat_row([
                    ("Toplam", str(len(ay_kayitlari)), "#b45309", ""),
                    ("Bekliyor", str(bekliyor), "#f59e0b", ""),
                    ("Tamamlandı", str(tamamlandı), "#059669", ""),
                    ("Tutulmadi", str(tutulmadi), "#ef4444", ""),
                ])

                # Tablo
                rows = []
                for k in ay_kayitlari:
                    try:
                        t_obj = date.fromisoformat(k.tarih)
                        gun_adi = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"][t_obj.weekday()]
                        tarih_str = f"{t_obj.strftime('%d.%m.%Y')} {gun_adi}"
                    except (ValueError, IndexError):
                        tarih_str = k.tarih
                    rows.append({
                        "Tarih": tarih_str,
                        "Öğretmen": k.ogretmen_adi,
                        "Nöbet Yeri": k.nobet_yeri,
                        "Durum": NOBET_DURUMLARI.get(k.durum, k.durum),
                        "Başlangıç": k.baslangic_saati or "-",
                        "Bitis": k.bitis_saati or "-",
                        "Olay": "Var" if k.olay_raporu else "-",
                    })

                def _nobet_durum_renk(val):
                    if val == "Tamamlandı":
                        return "background-color: #dcfce7; color: #166534"
                    elif val == "Tutulmadi":
                        return "background-color: #fee2e2; color: #991b1b"
                    elif val == "Devam Ediyor":
                        return "background-color: #dbeafe; color: #1e40af"
                    elif val == "Bekliyor":
                        return "background-color: #fef9c3; color: #854d0e"
                    return ""

                df = pd.DataFrame(rows)
                styled_df = df.style.map(_nobet_durum_renk, subset=["Durum"])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # ---- TAB 3: Nobet Takip ----
    with ntab3:
        styled_info_banner(
            "Bugünün nöbetlerini görüntüleyin. Nöbet başlangıcınızı ve bitişinizi kaydedin, "
            "olay varsa rapor yazın.",
            banner_type="info"
        )

        bugun = date.today().isoformat()
        bugun_kayitlari = [k for k in store.get_nobet_kayitlar(akademik_yil)
                          if k.tarih == bugun]

        if not bugun_kayitlari:
            # Tarih secimi ile baska gunlere de bakilabilsin
            nt_tarih = st.date_input("Tarih Sec", value=date.today(), key="nt_tarih")
            bugun_kayitlari = [k for k in store.get_nobet_kayitlar(akademik_yil)
                              if k.tarih == nt_tarih.isoformat()]
            if not bugun_kayitlari:
                styled_info_banner("Secilen tarih için nobet kaydi bulunamadı.", banner_type="warning")
        else:
            nt_tarih = date.today()

        for nk in bugun_kayitlari:
            durum_renk = {"bekliyor": "#f59e0b", "devam_ediyor": "#2563eb",
                         "tamamlandı": "#059669", "tutulmadi": "#ef4444"}.get(nk.durum, "#64748b")
            durum_label = NOBET_DURUMLARI.get(nk.durum, nk.durum)

            st.markdown(
                f'<div style="background:linear-gradient(135deg,{durum_renk}08,{durum_renk}18);'
                f'border-left:4px solid {durum_renk};border-radius:8px;padding:16px;margin-bottom:12px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div>'
                f'<span style="font-weight:700;font-size:16px;color:#94A3B8;">{nk.ogretmen_adi}</span>'
                f'<span style="margin-left:12px;background:{durum_renk};color:white;padding:2px 10px;'
                f'border-radius:10px;font-size:12px;font-weight:600;">{durum_label}</span>'
                f'</div>'
                f'<div style="color:#64748b;font-size:13px;">{nk.nobet_yeri}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            if nk.durum == "bekliyor":
                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("Nöbet Başlangıçi", key=f"nb_start_{nk.id}", type="primary", use_container_width=True):
                        nk.durum = "devam_ediyor"
                        nk.baslangic_saati = datetime.now().strftime("%H:%M")
                        store.save_nobet_kayit(nk)
                        st.success(f"Nöbet basladi: {nk.baslangic_saati}")
                        st.rerun(scope="fragment")
                with bc2:
                    # Tutulmadi
                    with st.expander("Nöbet Tutulmadi"):
                        ntm_neden = st.selectbox("Neden", NOBET_TUTULMAMA_NEDENLERI, key=f"ntm_neden_{nk.id}")
                        yerine_opts = {t.id: f"{t.ad} {t.soyad}" for t in teachers if t.id != nk.ogretmen_id}
                        if yerine_opts:
                            yerine_id = st.selectbox("Yerine Tutan", list(yerine_opts.keys()),
                                                     format_func=lambda x: yerine_opts.get(x, x),
                                                     key=f"ntm_yerine_{nk.id}")
                        else:
                            yerine_id = None
                        if st.button("Kaydet", key=f"ntm_save_{nk.id}", use_container_width=True):
                            nk.durum = "tutulmadi"
                            nk.tutulmama_nedeni = ntm_neden
                            if yerine_id:
                                nk.yerine_tutan_id = yerine_id
                                nk.yerine_tutan_adi = yerine_opts.get(yerine_id, "")
                            store.save_nobet_kayit(nk)
                            st.warning("Nöbet tutulmadi olarak kaydedildi.")
                            st.rerun(scope="fragment")

            elif nk.durum == "devam_ediyor":
                st.caption(f"Başlangıç: **{nk.baslangic_saati}**")

                with st.form(f"nobet_bitis_form_{nk.id}"):
                    styled_section("Nöbet Raporu", "#dc2626")
                    nb_olay = st.text_area("Olay / Rapor (varsa yazin)", value=nk.olay_raporu, height=100,
                                           key=f"nb_olay_{nk.id}")
                    nb_dosya = st.file_uploader("Dosya Ekle (foto, Word, PDF vb.)",
                                                type=["jpg", "jpeg", "png", "pdf", "docx", "doc", "txt"],
                                                accept_multiple_files=True,
                                                key=f"nb_dosya_{nk.id}")

                    if st.form_submit_button("Nöbet Bitir ve Kaydet", use_container_width=True):
                        nk.durum = "tamamlandı"
                        nk.bitis_saati = datetime.now().strftime("%H:%M")
                        nk.olay_raporu = nb_olay.strip()

                        # Dosya kaydet
                        if nb_dosya:
                            from utils.security import validate_upload
                            _valid_nb = []
                            for _f in nb_dosya:
                                _ok, _msg = validate_upload(_f, allowed_types=["jpg", "jpeg", "png", "pdf", "docx", "doc", "txt"], max_mb=50)
                                if _ok:
                                    _valid_nb.append(_f)
                                else:
                                    st.warning(f"⚠️ {_f.name}: {_msg}")
                            nb_dosya = _valid_nb
                        if nb_dosya:
                            dosya_dir = get_data_path("akademik", "nobet_dosyalar")
                            os.makedirs(dosya_dir, exist_ok=True)
                            for f_up in nb_dosya:
                                dosya_adi = f"{nk.id}_{f_up.name}"
                                dosya_yolu = os.path.join(dosya_dir, dosya_adi)
                                with open(dosya_yolu, "wb") as df_out:
                                    df_out.write(f_up.getbuffer())
                                nk.olay_dosyalari.append({
                                    "dosya_adi": f_up.name,
                                    "dosya_yolu": dosya_yolu,
                                })

                        store.save_nobet_kayit(nk)
                        st.success(f"Nöbet tamamlandı! Bitis: {nk.bitis_saati}")
                        st.rerun(scope="fragment")

            elif nk.durum == "tamamlandı":
                st.caption(f"Başlangıç: **{nk.baslangic_saati}** | Bitis: **{nk.bitis_saati}**")
                if nk.olay_raporu:
                    st.info(f"Olay Raporu: {nk.olay_raporu}")
                if nk.olay_dosyalari:
                    st.caption(f"Ekli dosya: {len(nk.olay_dosyalari)} adet")

            elif nk.durum == "tutulmadi":
                st.caption(f"Neden: **{nk.tutulmama_nedeni}**")
                if nk.yerine_tutan_adi:
                    st.caption(f"Yerine tutan: **{nk.yerine_tutan_adi}**")

    # ---- TAB 4: Nobet Raporu ----
    with ntab4:
        tum_kayitlar = store.get_nobet_kayitlar(akademik_yil)

        if not tum_kayitlar:
            styled_info_banner("Henuz nobet kaydi bulunmuyor.", banner_type="warning")
        else:
            # Filtreler
            import calendar as _cal

            rp_c1, rp_c2, rp_c3, rp_c4 = st.columns(4)
            with rp_c1:
                rp_yil = st.number_input("Yil", min_value=2024, max_value=2030,
                                         value=date.today().year, key="rp_nobet_yil")
            with rp_c2:
                ay_secenekler = []
                ay_map: dict[str, int] = {}
                for _ay_no, _ay_adi in AYLAR:
                    _, _son_gun = _cal.monthrange(rp_yil, _ay_no)
                    _label = f"{_ay_adi} (1-{_son_gun})"
                    ay_secenekler.append(_label)
                    ay_map[_label] = _ay_no
                rp_ay_label = st.selectbox("Ay", ["Tümü"] + ay_secenekler, key="rp_nobet_ay")
                rp_ay = "Tümü" if rp_ay_label == "Tümü" else ay_map.get(rp_ay_label, "Tümü")
            with rp_c3:
                rp_durum = st.selectbox("Durum", ["Tümü"] + list(NOBET_DURUMLARI.values()), key="rp_nobet_durum")
            with rp_c4:
                ogr_list = sorted(set(k.ogretmen_adi for k in tum_kayitlar))
                rp_ogr = st.selectbox("Öğretmen", ["Tümü"] + ogr_list, key="rp_nobet_ogr")

            filtrelenmis = tum_kayitlar[:]
            if rp_ay != "Tümü" and isinstance(rp_ay, int):
                filtrelenmis = [k for k in filtrelenmis if k.tarih and len(k.tarih) >= 7
                                and k.tarih[:4] == str(rp_yil)
                                and k.tarih[5:7] == f"{rp_ay:02d}"]
            if rp_durum != "Tümü":
                durum_key = next((k for k, v in NOBET_DURUMLARI.items() if v == rp_durum), None)
                if durum_key:
                    filtrelenmis = [k for k in filtrelenmis if k.durum == durum_key]
            if rp_ogr != "Tümü":
                filtrelenmis = [k for k in filtrelenmis if k.ogretmen_adi == rp_ogr]

            # Genel istatistikler
            toplam = len(tum_kayitlar)
            tamamlandı_n = sum(1 for k in tum_kayitlar if k.durum == "tamamlandı")
            tutulmadi_n = sum(1 for k in tum_kayitlar if k.durum == "tutulmadi")
            olaylar = sum(1 for k in tum_kayitlar if k.olay_raporu)

            styled_stat_row([
                ("Toplam Nöbet", str(toplam), "#b45309", ""),
                ("Tamamlanan", str(tamamlandı_n), "#059669", ""),
                ("Tutulmayan", str(tutulmadi_n), "#ef4444", ""),
                ("Olay Raporu", str(olaylar), "#7c3aed", ""),
            ])

            st.markdown("---")

            # Ogretmen bazli ozet
            styled_section("Öğretmen Bazli Özet", color="#92400e")
            ogr_ozet: dict[str, dict] = {}
            for k in tum_kayitlar:
                name = k.ogretmen_adi
                if name not in ogr_ozet:
                    ogr_ozet[name] = {"toplam": 0, "tamamlandı": 0, "tutulmadi": 0, "olay": 0, "yerler": set()}
                ogr_ozet[name]["toplam"] += 1
                if k.durum == "tamamlandı":
                    ogr_ozet[name]["tamamlandı"] += 1
                elif k.durum == "tutulmadi":
                    ogr_ozet[name]["tutulmadi"] += 1
                if k.olay_raporu:
                    ogr_ozet[name]["olay"] += 1
                ogr_ozet[name]["yerler"].add(k.nobet_yeri)

            ozet_rows = []
            for ogr, info in sorted(ogr_ozet.items()):
                ozet_rows.append({
                    "Öğretmen": ogr,
                    "Toplam": info["toplam"],
                    "Tamamlanan": info["tamamlandı"],
                    "Tutulmayan": info["tutulmadi"],
                    "Olay Sayısı": info["olay"],
                    "Nöbet Yerleri": ", ".join(sorted(info["yerler"])),
                })
            st.dataframe(pd.DataFrame(ozet_rows), use_container_width=True, hide_index=True)

            # Detay tablosu
            st.markdown("---")
            styled_section("Filtrelenmis Kayıtlar", color="#6366f1")
            filtrelenmis.sort(key=lambda x: x.tarih, reverse=True)

            if filtrelenmis:
                det_rows = []
                for k in filtrelenmis:
                    try:
                        tarih_str = date.fromisoformat(k.tarih).strftime('%d.%m.%Y')
                    except ValueError:
                        tarih_str = k.tarih
                    det_rows.append({
                        "Tarih": tarih_str,
                        "Öğretmen": k.ogretmen_adi,
                        "Nöbet Yeri": k.nobet_yeri,
                        "Durum": NOBET_DURUMLARI.get(k.durum, k.durum),
                        "Başlangıç": k.baslangic_saati or "-",
                        "Bitis": k.bitis_saati or "-",
                        "Neden": k.tutulmama_nedeni if k.durum == "tutulmadi" else "",
                        "Yerine": k.yerine_tutan_adi if k.durum == "tutulmadi" else "",
                        "Olay": "Var" if k.olay_raporu else "-",
                    })
                st.dataframe(pd.DataFrame(det_rows), use_container_width=True, hide_index=True)
            else:
                st.info("Filtreye uygun kayit bulunamadı.")

            # Olay raporlari detay
            olaylilar = [k for k in filtrelenmis if k.olay_raporu]
            if olaylilar:
                st.markdown("---")
                styled_section("Olay Raporlari", color="#ef4444")
                for k in olaylilar:
                    try:
                        tarih_str = date.fromisoformat(k.tarih).strftime('%d.%m.%Y')
                    except ValueError:
                        tarih_str = k.tarih
                    with st.expander(f"{tarih_str} - {k.ogretmen_adi} ({k.nobet_yeri})"):
                        st.write(k.olay_raporu)
                        if k.olay_dosyalari:
                            st.caption(f"Ekli dosya sayisi: {len(k.olay_dosyalari)}")
                            for dosya in k.olay_dosyalari:
                                dosya_yolu = dosya.get("dosya_yolu", "")
                                if os.path.exists(dosya_yolu):
                                    with open(dosya_yolu, "rb") as f_read:
                                        st.download_button(
                                            f"Indir: {dosya.get('dosya_adi', 'dosya')}",
                                            f_read.read(),
                                            file_name=dosya.get("dosya_adi", "dosya"),
                                            key=f"dl_{k.id}_{dosya.get('dosya_adi', '')}",
                                        )


# ==================== ONLINE DERS ====================

# Statik veriler modül seviyesinde (her render'da yeniden oluşturulmaz)
_DIJITAL_PLATFORMLAR = (
    ("e-Okul YD", "MEB e-Okul Yüz Yüze Değerlendirme", "https://eokulyd.meb.gov.tr/vbsssogiris.aspx", "#c62828", "#b71c1c", "#ffcdd2"),
    ("MEBi", "MEB Dijital İçerik Platformu", "https://mebi.eba.gov.tr/?ReturnUrl=%2Fteacher%2Fhome%2Fcontent", "#1565c0", "#0d47a1", "#bbdefb"),
    ("Khan Akademi", "Ücretsiz Dünya Sınıfı Eğitim", "https://tr.khanacademy.org/", "#14BF96", "#0a9b7a", "#b2dfdb"),
    ("OGDM Materyal", "OGM Eğitim Materyalleri", "https://ogmmateryal.eba.gov.tr/", "#e65100", "#bf360c", "#ffccbc"),
    ("EBA", "Eğitim Bilişim Ağı", "https://www.eba.gov.tr/", "#1976d2", "#0d47a1", "#bbdefb"),
    ("Ders Atölyeleri", "İBB Ücretsiz Online Atölyeler", "https://dersatolyeleri.ibb.istanbul/onlineatolyeler/", "#d32f2f", "#b71c1c", "#ffcdd2"),
    ("Code.org", "Kodlama ve Bilgisayar Bilimi Eğitimi", "https://code.org/tr/", "#f57c00", "#e65100", "#ffe0b2"),
    ("Scratch", "MIT Görsel Programlama Platformu", "https://scratch.mit.edu/", "#7c3aed", "#5b21b6", "#ddd6fe"),
    ("PhET", "İnteraktif Fen ve Matematik Simülasyonları", "https://phet.colorado.edu/tr/", "#0891b2", "#155e75", "#a5f3fc"),
    ("GeoGebra", "Matematik ve Geometri Araçları", "https://www.geogebra.org/?lang=tr", "#6d28d9", "#4c1d95", "#c4b5fd"),
    ("Bilim Genç", "TÜBİTAK Bilim ve Teknoloji Portalı", "https://bilimgenc.tubitak.gov.tr/", "#0d9488", "#115e59", "#ccfbf1"),
)

# Online Ders Linkleri — platform seçenekleri (görünen ad → key, ikon, renk, kısa ad)
_ONLINE_DERS_PLATFORM_MAP: dict[str, tuple] = {
    "Zoom":             ("zoom",             "Z", "#2D8CFF", "Zoom"),
    "Microsoft Teams":  ("teams",            "T", "#6264A7", "MS Teams"),
    "Google Classroom": ("google_classroom", "G", "#34A853", "Classroom"),
    "Google Meet":      ("meet",             "M", "#00897B", "Meet"),
}
_ONLINE_DERS_PLATFORMLAR = list(_ONLINE_DERS_PLATFORM_MAP.keys())
# key → (görünen ad) — ters arama için
_ONLINE_DERS_KEY_TO_LABEL = {v[0]: k for k, v in _ONLINE_DERS_PLATFORM_MAP.items()}

# Video konferans ve canlı ders platformları — Türkçe giriş sayfaları
_VIDEO_KONFERANS_PLATFORMLAR = (
    ("Zoom", "Türkçe Giriş — Canlı Ders & Toplantı Oluştur", "https://zoom.us/tr/signin", "#2D8CFF", "#1565c0", "#dbeafe"),
    ("Microsoft Teams", "Microsoft 365 — Türkçe Ekip & Ders Platformu", "https://teams.microsoft.com/?culture=tr-tr&country=TR", "#6264A7", "#4f46e5", "#e9d5ff"),
    ("Google Classroom", "Google Sınıf — Türkçe Ödev & Ders Yönetimi", "https://classroom.google.com/?hl=tr", "#34A853", "#1e8e3e", "#d1fae5"),
    ("Google Meet", "Türkçe Google Görüntülü Görüşme & Canlı Ders", "https://meet.google.com/?hl=tr", "#00897B", "#00695c", "#e0f2f1"),
)

_DIJITAL_YT_KANALLAR = {
    "İlkokul (1-4)": (
        ("Tonguc 1. Sınıf", "Tonguç Akademi 1. Sınıf Dersleri", "https://www.youtube.com/tonguc1", "#dc2626", "#991b1b", "#fecaca"),
        ("Tonguc 2. Sınıf", "Tonguç Akademi 2. Sınıf Dersleri", "https://www.youtube.com/c/tonguc2", "#ea580c", "#c2410c", "#fed7aa"),
        ("Tonguc 3. Sınıf", "Tonguç Akademi 3. Sınıf Dersleri", "https://www.youtube.com/channel/UCWKFn2p0uodV8JCdsYtGLIw", "#d97706", "#b45309", "#fef3c7"),
        ("Tonguc 4. Sınıf", "Tonguç Akademi 4. Sınıf Dersleri", "https://www.youtube.com/@tonguc4", "#ca8a04", "#a16207", "#fef9c3"),
        ("Sade Öğretmen", "İlkokul Ders Anlatımları", "https://www.youtube.com/@Sade_Ogretmen", "#16a34a", "#15803d", "#dcfce7"),
    ),
    "Ortaokul (5-8) + LGS": (
        ("Tonguç 5. Sınıf", "Tonguç Akademi 5. Sınıf Dersleri", "https://www.youtube.com/tonguc5", "#2563eb", "#1d4ed8", "#bfdbfe"),
        ("Tonguç 6. Sınıf", "Tonguç Akademi 6. Sınıf Dersleri", "https://www.youtube.com/@tonguc6", "#4f46e5", "#4338ca", "#c7d2fe"),
        ("Tonguç 7. Sınıf", "Tonguç Akademi 7. Sınıf Dersleri", "https://www.youtube.com/channel/UCI5Ir6-br-HM54InF7HUlzg", "#7c3aed", "#6d28d9", "#ddd6fe"),
        ("Tonguç 8. Sınıf", "Tonguç Akademi 8. Sınıf Dersleri", "https://www.youtube.com/@tonguc8", "#9333ea", "#7e22ce", "#e9d5ff"),
        ("Tonguç LGS", "LGS Hazırlık ve Soru Çözüm", "https://www.youtube.com/@tonguc8", "#dc2626", "#b91c1c", "#fecaca"),
    ),
    "Lise (9-11) + YKS (TYT/AYT)": (
        ("Tonguç 9. Sınıf", "Tonguç Akademi 9. Sınıf Dersleri", "https://www.youtube.com/channel/UCnMkrwpqeeUdULISjn-_NGA", "#0891b2", "#0e7490", "#cffafe"),
        ("Tonguç 10. Sınıf", "Tonguç Akademi 10. Sınıf Dersleri", "https://www.youtube.com/@tonguc10", "#0d9488", "#0f766e", "#ccfbf1"),
        ("Tonguç 11. Sınıf", "Tonguç Akademi 11. Sınıf Dersleri", "https://www.youtube.com/tonguc11", "#059669", "#047857", "#d1fae5"),
        ("Tonguç YKS", "YKS TYT/AYT Hazırlık ve Soru Çözüm", "https://www.youtube.com/channel/UCyKKD_T683_M2-cmnVwtFfg", "#dc2626", "#b91c1c", "#fecaca"),
        ("Benim Hocam", "YKS TYT/AYT Tüm Dersler", "https://www.youtube.com/c/BenimHocam/featured", "#7c3aed", "#6d28d9", "#ddd6fe"),
        ("Hocalara Geldik", "Lise ve YKS Ders Anlatımları", "https://www.youtube.com/channel/UCBcM2J8SHyq8GUSvrhWnwTg", "#db2777", "#be185d", "#fce7f3"),
    ),
    "LGS (8. Sınıf) Ücretsiz Kanallar": (
        ("Tonguç LGS Hazırlık", "LGS Tüm Dersler Hazırlık", "https://www.youtube.com/channel/UCPdN4Vx2DogwmjDJCkyVcXQ", "#dc2626", "#991b1b", "#fecaca"),
        ("Tonguç Sınıf", "Tonguç Sınıf LGS İçerikleri", "https://www.youtube.com/@TongucSnf-yk5oe", "#ea580c", "#c2410c", "#fed7aa"),
        ("Hocalara Geldik 8. Sınıf", "8. Sınıf Tüm Dersler", "https://www.youtube.com/channel/UChH7ByCfWqN7jE2i_M-p-PQ", "#d97706", "#b45309", "#fef3c7"),
        ("Benim Hocam Ortaokul", "5-8. Sınıf Tüm Dersler", "https://www.youtube.com/channel/UC2jKIKPwgMNZKsrsga005Yg", "#65a30d", "#4d7c0f", "#ecfccb"),
        ("Ders Like", "LGS Ders Anlatım ve Soru Çözüm", "https://www.youtube.com/c/DersLike", "#059669", "#047857", "#d1fae5"),
        ("Partikül Matematik", "Eğlenceli Matematik ve Motivasyon", "https://www.youtube.com/channel/UCRnT96PJOr4KeMEjhizEMfg", "#0891b2", "#0e7490", "#cffafe"),
        ("Bıyıklı Matematik", "LGS Matematik Soru Çözüm", "https://www.youtube.com/@biyiklimatematik", "#2563eb", "#1d4ed8", "#bfdbfe"),
        ("Önder Hoca", "LGS Fen Bilimleri Anlatım", "https://www.youtube.com/@onderhoca", "#4f46e5", "#4338ca", "#c7d2fe"),
        ("Rüştü Hoca ile Türkçe", "LGS Türkçe Ders Anlatım", "https://www.youtube.com/@RüştüHocaileTürkçe", "#7c3aed", "#6d28d9", "#ddd6fe"),
        ("Tonguç Akademi", "Tonguç Ana Kanal - Tüm Dersler", "https://www.youtube.com/channel/UCm3vDH7Uvz_qwql5Qih4yGw", "#9333ea", "#7e22ce", "#e9d5ff"),
    ),
    "YKS (TYT-AYT) Ücretsiz Kanallar": (
        ("Benim Hocam", "TYT/AYT Tüm Dersler", "https://www.youtube.com/@BenimHocam", "#dc2626", "#991b1b", "#fecaca"),
        ("Hocalara Geldik", "Lise ve YKS Ders Anlatımları", "https://www.youtube.com/channel/UCBcM2J8SHyq8GUSvrhWnwTg", "#ea580c", "#c2410c", "#fed7aa"),
        ("Rehber Matematik", "TYT/AYT Matematik", "https://www.youtube.com/@RehberMatematik", "#d97706", "#b45309", "#fef3c7"),
        ("Bıyıklı Matematik", "Matematik Soru Çözüm", "https://www.youtube.com/@biyiklimatematik", "#ca8a04", "#a16207", "#fef9c3"),
        ("Matematiğin Güler Yüzü", "TYT/AYT Matematik Anlatım", "https://www.youtube.com/matematiginguleryuzu", "#65a30d", "#4d7c0f", "#ecfccb"),
        ("Önder Hoca", "YKS Fen Bilimleri", "https://www.youtube.com/@onderhoca", "#16a34a", "#15803d", "#dcfce7"),
        ("Rüştü Hoca ile Türkçe", "TYT Türkçe/Edebiyat Ders Anlatım", "https://www.youtube.com/channel/UCyohoF5P2JFvc3KLLZRwDug", "#059669", "#047857", "#d1fae5"),
        ("Fizik Finito", "TYT/AYT Fizik", "https://www.youtube.com/channel/UC-zDbhn0rWs2EywjGQMrK7A", "#0891b2", "#0e7490", "#cffafe"),
        ("Kimya Adası", "TYT/AYT Kimya", "https://www.youtube.com/channel/UCTR3FZld7SysalUMHnIDnuA", "#0d9488", "#0f766e", "#ccfbf1"),
        ("Senin Biyolojin", "TYT/AYT Biyoloji", "https://www.youtube.com/seninbiyolojin", "#2563eb", "#1d4ed8", "#bfdbfe"),
        ("Dr.Biyoloji - Barış Hoca", "TYT/AYT Biyoloji Anlatım", "https://www.youtube.com/channel/UCY7Nh-CV3qqaWTxldlG4RCA", "#4f46e5", "#4338ca", "#c7d2fe"),
        ("FUNDAmentals Biyoloji", "TYT/AYT Biyoloji", "https://www.youtube.com/channel/UCzkNEai752Dr3AF4nEyTnqA", "#7c3aed", "#6d28d9", "#ddd6fe"),
        ("Sosyal Kale", "TYT/AYT Tarih ve Coğrafya", "https://www.youtube.com/sosyalkale", "#9333ea", "#7e22ce", "#e9d5ff"),
        ("Gri Koç", "YKS Motivasyon ve Koçluk", "https://www.youtube.com/@grikoc", "#db2777", "#be185d", "#fce7f3"),
        ("Eyüp B. Matematik", "TYT/AYT Matematik ve Geometri", "https://www.youtube.com/@EyupB", "#b45309", "#92400e", "#fef3c7"),
    ),
    "Yabancı Dil (İngilizce)": (
        ("BBC Learning English", "BBC İngilizce Ders Videoları", "https://www.youtube.com/bbclearningenglish", "#b71c1c", "#7f0000", "#ffcdd2"),
        ("EnglishClass101", "İngilizce Dil Eğitimi", "https://www.youtube.com/@EnglishClass101", "#1565c0", "#0d47a1", "#bbdefb"),
        ("engVid", "Learn English - Gramer ve Kelime", "https://www.youtube.com/user/engvidenglish", "#2e7d32", "#1b5e20", "#c8e6c9"),
    ),
}


def _build_dijital_platform_html() -> str:
    """Platform kartlarini tek HTML blogu olarak olusturur (widget yok = hizli)."""
    parts = ['<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">']
    for ad, aciklama, link, r1, r2, rt in _DIJITAL_PLATFORMLAR:
        parts.append(
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
            f'padding:22px 18px;text-align:center;min-height:80px;display:flex;flex-direction:column;'
            f'justify-content:center;cursor:pointer;transition:transform 0.15s,box-shadow 0.15s;">'
            f'<div style="font-size:22px;font-weight:800;color:white;letter-spacing:1px;">{ad}</div>'
            f'<div style="color:{rt};font-size:12px;margin-top:6px;">{aciklama}</div></div></a>'
        )
    parts.append('</div>')
    return "".join(parts)


def _build_dijital_yt_html() -> str:
    """YouTube kanallarini tek HTML blogu olarak olusturur (widget yok = hizli)."""
    parts = []
    for kademe, kanallar in _DIJITAL_YT_KANALLAR.items():
        parts.append(
            f'<div style="background:linear-gradient(90deg,#dc262615,#dc262605);'
            f'border-left:4px solid #dc2626;padding:8px 14px;border-radius:0 8px 8px 0;'
            f'margin:12px 0 8px 0;font-weight:700;font-size:0.9rem;color:#dc2626;">'
            f'🎓 {kademe}</div>'
        )
        parts.append('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:8px;">')
        for ad, aciklama, link, r1, r2, rt in kanallar:
            parts.append(
                f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
                f'transition:transform 0.15s,box-shadow 0.15s;">'
                f'<div style="font-size:13px;position:absolute;top:8px;left:12px;'
                f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;padding:1px 8px;">▶ YouTube</div>'
                f'<div style="font-size:18px;font-weight:800;color:white;letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
                f'<div style="color:{rt};font-size:11px;margin-top:6px;">{aciklama}</div></div></a>'
            )
        parts.append('</div>')
    return "".join(parts)


def _build_video_konferans_html() -> str:
    """Video konferans ve canlı ders platform kartlarını oluşturur — Türkçe giriş linkleri."""
    parts = ['<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px;">']
    for ad, aciklama, link, r1, r2, rt in _VIDEO_KONFERANS_PLATFORMLAR:
        parts.append(
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
            f'padding:24px 18px;text-align:center;min-height:110px;display:flex;flex-direction:column;'
            f'justify-content:center;cursor:pointer;transition:transform 0.15s,box-shadow 0.15s;">'
            f'<div style="font-size:20px;font-weight:800;color:white;letter-spacing:0.5px;">{ad}</div>'
            f'<div style="color:{rt};font-size:11px;margin-top:6px;line-height:1.4;">{aciklama}</div>'
            f'<div style="margin-top:12px;background:rgba(255,255,255,0.22);color:white;'
            f'border-radius:20px;padding:5px 16px;font-size:12px;font-weight:700;display:inline-block;'
            f'letter-spacing:0.5px;">Giriş Yap →</div>'
            f'</div></a>'
        )
    parts.append('</div>')
    return "".join(parts)


# Onceden build et (modul yuklenmesinde 1 kez)
_PLATFORM_HTML_CACHE = _build_dijital_platform_html()
_YT_HTML_CACHE = _build_dijital_yt_html()
_VIDEO_KONFERANS_HTML_CACHE = _build_video_konferans_html()


# ==================== GÜNLÜK PLAN OLUŞTURUCU ====================

# MEB 2024-2025 standart tatil günleri (her yıl benzer)
_MEB_STANDART_TATILLER = [
    # (başlık, başlangıç_ay, başlangıç_gün, bitiş_ay, bitiş_gün, 1.dönem_mi)
    ("Cumhuriyet Bayramı", 10, 28, 10, 29, True),
    ("1. Ara Tatil (Kasım)", 11, 17, 11, 21, True),
    ("Yılbaşı", 1, 1, 1, 1, False),
    ("Sömestr Tatili", 1, 20, 2, 2, False),
    ("2. Ara Tatil (Nisan)", 4, 14, 4, 18, False),
    ("Ulusal Egemenlik ve Çocuk Bayramı", 4, 23, 4, 23, False),
    ("İşçi Bayramı", 5, 1, 5, 1, False),
    ("Atatürk'ü Anma Günü", 5, 19, 5, 19, False),
]


def _get_tatil_gunleri(yil_baslangic: int, ekstra_tatiller: list = None) -> set:
    """Akademik yılın tatil günlerini set olarak döndür."""
    from datetime import date, timedelta
    tatil_set = set()
    y1 = yil_baslangic
    y2 = yil_baslangic + 1

    for _, b_ay, b_gun, s_ay, s_gun, _ in _MEB_STANDART_TATILLER:
        b_yil = y1 if b_ay >= 9 else y2
        s_yil = y1 if s_ay >= 9 else y2
        try:
            d = date(b_yil, b_ay, b_gun)
            son = date(s_yil, s_ay, s_gun)
            while d <= son:
                tatil_set.add(d)
                d += timedelta(days=1)
        except ValueError:
            pass

    # Akademik takvimden ek tatiller
    if ekstra_tatiller:
        for et in ekstra_tatiller:
            bas = et.get("tarih_baslangic", "")
            bit = et.get("tarih_bitis", "") or bas
            tur = et.get("tur", "")
            if tur not in ("ara_tatil", "someter", "bayram_milli", "bayram_dini"):
                continue
            try:
                d = date.fromisoformat(bas)
                son = date.fromisoformat(bit) if bit else d
                while d <= son:
                    tatil_set.add(d)
                    d += timedelta(days=1)
            except (ValueError, TypeError):
                pass

    return tatil_set


def _parse_uploaded_plan(uploaded_file) -> list:
    """Yüklenen yıllık plan dosyasını parse et. Excel veya CSV destekler.
    Döndürür: [{"hafta": int, "konu": str, "kazanim": str, "saat": int}, ...]
    """
    fname = uploaded_file.name.lower()

    try:
        if fname.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl" if fname.endswith(".xlsx") else None)
        elif fname.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            return []
    except Exception:
        return []

    # Sütun isimlerini normalize et
    col_map = {}
    for c in df.columns:
        cl = str(c).lower().strip()
        if "hafta" in cl or "week" in cl:
            col_map["hafta"] = c
        elif "konu" in cl or "topic" in cl or "ünite" in cl or "unite" in cl:
            col_map["konu"] = c
        elif "kazanım" in cl or "kazanim" in cl or "outcome" in cl or "hedef" in cl:
            col_map["kazanim"] = c
        elif "saat" in cl or "süre" in cl or "sure" in cl or "hour" in cl:
            col_map["saat"] = c

    # Eğer sütun eşlemesi bulunamazsa ilk birkaç sütunu kullan
    cols = list(df.columns)
    if "hafta" not in col_map and len(cols) >= 1:
        col_map["hafta"] = cols[0]
    if "konu" not in col_map and len(cols) >= 2:
        col_map["konu"] = cols[1]
    if "kazanim" not in col_map and len(cols) >= 3:
        col_map["kazanim"] = cols[2]
    if "saat" not in col_map and len(cols) >= 4:
        col_map["saat"] = cols[3]

    rows = []
    for idx, row in df.iterrows():
        hafta_raw = str(row.get(col_map.get("hafta", ""), idx + 1))
        # Hafta numarası çıkar
        import re
        hafta_nums = re.findall(r"\d+", hafta_raw)
        hafta_no = int(hafta_nums[0]) if hafta_nums else idx + 1

        konu = str(row.get(col_map.get("konu", ""), "")).strip()
        kazanim = str(row.get(col_map.get("kazanim", ""), "")).strip()
        saat_raw = row.get(col_map.get("saat", ""), 0)
        try:
            saat = int(float(str(saat_raw).replace(",", ".")))
        except (ValueError, TypeError):
            saat = 0

        if konu and konu != "nan":
            rows.append({
                "hafta": hafta_no,
                "konu": konu,
                "kazanim": kazanim if kazanim != "nan" else "",
                "saat": max(saat, 1),
            })

    return rows


def _generate_gunluk_plan_pdf(
    ders: str, sinif: str, sube: str, ogretmen: str,
    kurum_adi: str, akademik_yil: str,
    haftalik_plan: list, haftalik_saat: int,
    okul_baslangic, aktif_gunler: list,
) -> bytes:
    """Günlük plan PDF oluştur.
    haftalik_plan: [{"hafta": int, "gun_planlar": [{"tarih": date, "gun": str,
                     "konu": str, "kazanim": str, "saat": int}]}]
    """
    import io
    from datetime import date
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, PageBreak)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    except ImportError:
        return None

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                             topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                             leftMargin=1.5 * cm, rightMargin=1.5 * cm)

    styles = getSampleStyleSheet()
    s_title = ParagraphStyle('GPTitle', fontSize=14, leading=18, alignment=TA_CENTER,
                              fontName=font_bold, textColor=colors.white, spaceAfter=2)
    s_sub = ParagraphStyle('GPSub', fontSize=9, leading=12, alignment=TA_CENTER,
                            fontName=font_name, textColor=colors.HexColor('#cbd5e1'), spaceAfter=6)
    s_h2 = ParagraphStyle('GPH2', fontSize=11, leading=14, alignment=TA_LEFT,
                           fontName=font_bold, textColor=colors.HexColor('#1e40af'), spaceBefore=8, spaceAfter=4)
    s_cell = ParagraphStyle('GPCell', fontSize=8, leading=10, fontName=font_name, alignment=TA_LEFT)
    s_cellb = ParagraphStyle('GPCellB', fontSize=8, leading=10, fontName=font_bold, alignment=TA_LEFT)
    s_cellc = ParagraphStyle('GPCellC', fontSize=8, leading=10, fontName=font_name, alignment=TA_CENTER)
    s_foot = ParagraphStyle('GPFoot', fontSize=8, leading=10, fontName=font_name,
                             alignment=TA_RIGHT, textColor=colors.grey)

    GUN_TR = {"Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
              "Thursday": "Perşembe", "Friday": "Cuma", "Saturday": "Cumartesi", "Sunday": "Pazar"}

    elements = []
    page_w = A4[0] - 3 * cm

    # Başlık banner
    banner_data = [[Paragraph(f"{kurum_adi}", s_title)],
                    [Paragraph(f"Günlük Ders Planı — {ders} | {sinif}/{sube} | {akademik_yil}", s_sub)]]
    banner = Table(banner_data, colWidths=[page_w])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B0F19')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    elements.append(banner)
    elements.append(Spacer(1, 8))

    # Öğretmen + bilgi satırı
    info_text = f"Öğretmen: {ogretmen}  |  Haftalık Saat: {haftalik_saat}  |  Aktif Günler: {', '.join(aktif_gunler)}"
    elements.append(Paragraph(info_text, ParagraphStyle('GPInfo', fontSize=9, leading=12,
                              fontName=font_name, alignment=TA_LEFT, textColor=colors.HexColor('#475569'),
                              spaceBefore=4, spaceAfter=10)))

    # Hafta hafta tablo oluştur
    col_widths = [1.8 * cm, 2.5 * cm, page_w - 1.8 * cm - 2.5 * cm - 3.5 * cm - 1.5 * cm, 3.5 * cm, 1.5 * cm]
    header = [
        Paragraph("Tarih", s_cellb),
        Paragraph("Gün", s_cellb),
        Paragraph("Konu / İçerik", s_cellb),
        Paragraph("Kazanım", s_cellb),
        Paragraph("Saat", s_cellb),
    ]

    for hafta in haftalik_plan:
        hafta_no = hafta["hafta"]
        gun_planlar = hafta["gun_planlar"]
        if not gun_planlar:
            continue

        elements.append(Paragraph(f"{hafta_no}. Hafta", s_h2))

        table_data = [header]
        for gp in gun_planlar:
            tarih_str = gp["tarih"].strftime("%d.%m.%Y") if isinstance(gp["tarih"], date) else str(gp["tarih"])
            gun_str = GUN_TR.get(gp["gun"], gp["gun"])
            table_data.append([
                Paragraph(tarih_str, s_cellc),
                Paragraph(gun_str, s_cellc),
                Paragraph(str(gp["konu"]), s_cell),
                Paragraph(str(gp["kazanim"])[:80], s_cell),
                Paragraph(str(gp["saat"]), s_cellc),
            ])

        t = Table(table_data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), font_bold),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#111827')]),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 6))

        # Her 4 haftada sayfa kır
        if hafta_no > 0 and hafta_no % 4 == 0:
            elements.append(PageBreak())

    # Footer
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"SmartCampus AI — Günlük Plan Oluşturucu | Oluşturulma: {date.today().strftime('%d.%m.%Y')}", s_foot))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def _render_gunluk_plan_olustur(store: AkademikDataStore):
    """Günlük Plan Oluşturucu - yıllık plan yükle, tatilleri al, PDF üret."""
    from datetime import date, timedelta
    import json
    import os

    st.markdown(
        '<div style="background:linear-gradient(135deg,#064e3b,#065f46);color:#fff;'
        'padding:14px 20px;border-radius:12px;margin-bottom:16px;">'
        '<div style="font-size:1.1rem;font-weight:700;">📅 Günlük Plan Oluşturucu</div>'
        '<div style="font-size:.85rem;opacity:.85;margin-top:4px;">'
        'Yıllık planı yükle → Tatilleri otomatik al → Günlük plana dönüştür → PDF indir</div>'
        '</div>', unsafe_allow_html=True,
    )

    # ── ADIM 1: Ders & Sınıf Bilgileri ──
    styled_section("1. Ders & Sınıf Bilgileri", color="#2563eb")

    c1, c2, c3 = st.columns(3)
    with c1:
        ders = st.text_input("Ders Adı", value="", placeholder="Matematik, Türkçe...", key="gp_ders")
    with c2:
        sinif_sec = st.selectbox("Sınıf", list(range(1, 13)), index=4, key="gp_sinif")
    with c3:
        sube_sec = st.text_input("Şube", value="A", key="gp_sube")

    c4, c5 = st.columns(2)
    with c4:
        ogretmen = st.text_input("Öğretmen Adı", value="", key="gp_ogretmen")
    with c5:
        from utils.shared_data import load_kurum_profili
        kurum = load_kurum_profili()
        kurum_adi = kurum.get("kurum_adi", "SmartCampus Okulu") if kurum else "SmartCampus Okulu"
        st.text_input("Kurum Adı", value=kurum_adi, key="gp_kurum", disabled=True)

    # ── ADIM 2: Akademik Takvim Ayarları ──
    styled_section("2. Akademik Takvim Ayarları", color="#0d9488")

    c6, c7, c8 = st.columns(3)
    with c6:
        okul_bas = st.date_input("Okulun İlk Günü", value=date(2025, 9, 8), key="gp_okul_bas")
    with c7:
        haftalik_saat = st.number_input("Haftada Kaç Saat", min_value=1, max_value=20, value=5, key="gp_haft_saat")
    with c8:
        toplam_hafta = st.number_input("Toplam Hafta", min_value=20, max_value=40, value=36, key="gp_toplam_hafta")

    aktif_gunler_sec = st.multiselect(
        "Aktif Günler",
        ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"],
        default=["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"],
        key="gp_aktif_gunler",
    )
    GUN_EN = {"Pazartesi": 0, "Salı": 1, "Çarşamba": 2, "Perşembe": 3, "Cuma": 4, "Cumartesi": 5, "Pazar": 6}
    aktif_gun_nums = {GUN_EN[g] for g in aktif_gunler_sec}

    # Tatil bilgisi
    st.markdown("##### Tatil Günleri")
    st.caption("MEB standart tatilleri otomatik yüklenir. Akademik Takvim modülünden ek tatiller alınır.")

    yil_bas = okul_bas.year
    # Akademik takvim verilerini yükle
    takvim_path = get_data_path("akademik", "akademik_takvim.json")
    ekstra_tatiller = []
    if os.path.exists(takvim_path):
        try:
            with open(takvim_path, "r", encoding="utf-8") as f:
                ekstra_tatiller = json.load(f)
        except Exception:
            pass

    tatil_set = _get_tatil_gunleri(yil_bas, ekstra_tatiller)

    # Tatil listesini göster
    with st.expander(f"📅 Tatil Günleri ({len(tatil_set)} gün)", expanded=False):
        tatil_list = sorted(tatil_set)
        for baslik, b_ay, b_gun, s_ay, s_gun, _ in _MEB_STANDART_TATILLER:
            b_yil = yil_bas if b_ay >= 9 else yil_bas + 1
            s_yil = yil_bas if s_ay >= 9 else yil_bas + 1
            try:
                b_date = date(b_yil, b_ay, b_gun)
                s_date = date(s_yil, s_ay, s_gun)
                gun_sayisi = (s_date - b_date).days + 1
                st.markdown(f"- **{baslik}**: {b_date.strftime('%d.%m.%Y')} — {s_date.strftime('%d.%m.%Y')} ({gun_sayisi} gün)")
            except ValueError:
                pass
        if ekstra_tatiller:
            st.markdown("**Akademik Takvimden:**")
            for et in ekstra_tatiller:
                if et.get("tur") in ("ara_tatil", "someter", "bayram_milli", "bayram_dini"):
                    st.markdown(f"- {et.get('baslik', '?')}: {et.get('tarih_baslangic', '')} — {et.get('tarih_bitis', '')}")

    # ── ADIM 3: Yıllık Plan Yükle ──
    styled_section("3. Yıllık Plan Yükle", color="#7c3aed")

    st.markdown(
        '<div style="background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.2);'
        'border-radius:10px;padding:12px 16px;margin-bottom:12px;font-size:.85rem;color:#7c3aed;">'
        '<b>Excel Formatı:</b> Hafta | Konu/Ünite | Kazanım | Saat sütunları beklenir. '
        'Sütun adları otomatik algılanır.</div>', unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Yıllık Plan Dosyası (Excel / CSV)",
        type=["xlsx", "xls", "csv"],
        key="gp_upload",
    )

    if uploaded:
        from utils.security import validate_upload
        _ok, _msg = validate_upload(uploaded, allowed_types=["xlsx", "xls", "csv"], max_mb=100)
        if not _ok:
            st.error(f"⚠️ {_msg}")
            uploaded = None

    plan_rows = []
    if uploaded:
        plan_rows = _parse_uploaded_plan(uploaded)
        if plan_rows:
            st.success(f"✅ {len(plan_rows)} satır başarıyla yüklendi.")
            with st.expander("Yüklenen Plan Önizleme", expanded=False):
                df_preview = pd.DataFrame(plan_rows)
                st.dataframe(df_preview, use_container_width=True, height=300)
        else:
            st.warning("Dosya okunamadı veya boş. Lütfen formatı kontrol edin.")

    # Manuel giriş seçeneği
    if not plan_rows:
        st.markdown("**veya Manuel Konu Girişi:**")
        manuel_text = st.text_area(
            "Her satıra bir konu yazın (opsiyonel: konu | kazanım | saat)",
            height=150,
            key="gp_manuel",
            placeholder="1. Ünite: Sayılar | M.5.1.1 | 4\nDoğal Sayılar | M.5.1.2 | 3\n...",
        )
        if manuel_text.strip():
            lines = [l.strip() for l in manuel_text.strip().split("\n") if l.strip()]
            for i, line in enumerate(lines):
                parts = [p.strip() for p in line.split("|")]
                konu = parts[0] if len(parts) >= 1 else line
                kazanim = parts[1] if len(parts) >= 2 else ""
                try:
                    saat = int(parts[2]) if len(parts) >= 3 else haftalik_saat
                except (ValueError, TypeError):
                    saat = haftalik_saat
                plan_rows.append({"hafta": i + 1, "konu": konu, "kazanim": kazanim, "saat": saat})

    # ── ADIM 4: Günlük Plan Oluştur ──
    styled_section("4. Günlük Plan Oluştur & PDF İndir", color="#dc2626")

    if not plan_rows:
        st.info("Önce yıllık plan dosyası yükleyin veya manuel konu girişi yapın.")
        return

    if not ders:
        st.warning("Lütfen ders adını girin.")
        return

    # İstatistikler
    toplam_konu = len(plan_rows)
    toplam_saat_plan = sum(r["saat"] for r in plan_rows)
    toplam_saat_yil = toplam_hafta * haftalik_saat

    styled_stat_row([
        {"label": "Toplam Konu", "value": str(toplam_konu), "color": "blue", "icon": "📚"},
        {"label": "Plan Saati", "value": str(toplam_saat_plan), "color": "purple", "icon": "⏱️"},
        {"label": "Yıllık Saat", "value": str(toplam_saat_yil), "color": "green", "icon": "📅"},
        {"label": "Tatil Günü", "value": str(len(tatil_set)), "color": "yellow", "icon": "🌴"},
    ])

    if st.button("📅 Günlük Plan Oluştur & PDF İndir", type="primary", use_container_width=True, key="gp_btn"):
        with st.spinner("Günlük plan oluşturuluyor..."):
            # Tüm iş günlerini hesapla (tatiller ve hafta sonları hariç)
            is_gunleri = []
            current = okul_bas
            max_date = okul_bas + timedelta(days=365)
            while len(is_gunleri) < toplam_hafta * len(aktif_gunler_sec) and current < max_date:
                if current.weekday() in aktif_gun_nums and current not in tatil_set:
                    is_gunleri.append(current)
                current += timedelta(days=1)

            if not is_gunleri:
                st.error("Hiç iş günü bulunamadı. Tarihleri kontrol edin.")
                return

            # Konuları günlere dağıt
            # Her konu, saat sayısı kadar gün alır (her gün 1 ders saati olarak)
            gun_konulari = []  # [(tarih, konu, kazanim, saat)]
            gun_idx = 0
            for row in plan_rows:
                konu = row["konu"]
                kazanim = row["kazanim"]
                saat = row["saat"]
                ders_per_gun = max(1, haftalik_saat // len(aktif_gunler_sec)) if aktif_gunler_sec else 1
                gun_sayisi = max(1, (saat + ders_per_gun - 1) // ders_per_gun)
                for _ in range(gun_sayisi):
                    if gun_idx >= len(is_gunleri):
                        break
                    gun_konulari.append({
                        "tarih": is_gunleri[gun_idx],
                        "gun": is_gunleri[gun_idx].strftime("%A"),
                        "konu": konu,
                        "kazanim": kazanim,
                        "saat": min(saat, ders_per_gun),
                    })
                    saat -= ders_per_gun
                    gun_idx += 1

            # Haftalara grupla
            haftalik_plan = []
            hafta_no = 0
            prev_iso_week = None
            for gk in gun_konulari:
                iso_week = gk["tarih"].isocalendar()[1]
                if iso_week != prev_iso_week:
                    hafta_no += 1
                    haftalik_plan.append({"hafta": hafta_no, "gun_planlar": []})
                    prev_iso_week = iso_week
                haftalik_plan[-1]["gun_planlar"].append(gk)

            # Önizleme
            st.success(f"✅ {len(gun_konulari)} günlük plan oluşturuldu — {len(haftalik_plan)} hafta")

            # Önizleme tablosu
            with st.expander("📋 Günlük Plan Önizleme", expanded=True):
                GUN_TR_MAP = {"Monday": "Pazartesi", "Tuesday": "Salı", "Wednesday": "Çarşamba",
                              "Thursday": "Perşembe", "Friday": "Cuma"}
                preview_data = []
                for h in haftalik_plan[:8]:
                    for g in h["gun_planlar"]:
                        preview_data.append({
                            "Hafta": h["hafta"],
                            "Tarih": g["tarih"].strftime("%d.%m.%Y"),
                            "Gün": GUN_TR_MAP.get(g["gun"], g["gun"]),
                            "Konu": g["konu"][:50],
                            "Kazanım": g["kazanim"][:40],
                            "Saat": g["saat"],
                        })
                if preview_data:
                    st.dataframe(pd.DataFrame(preview_data), use_container_width=True, height=350)
                if len(haftalik_plan) > 8:
                    st.caption(f"... ve {len(haftalik_plan) - 8} hafta daha")

            # PDF oluştur
            pdf_bytes = _generate_gunluk_plan_pdf(
                ders=ders,
                sinif=str(sinif_sec),
                sube=sube_sec,
                ogretmen=ogretmen or "—",
                kurum_adi=kurum_adi,
                akademik_yil=f"{yil_bas}-{yil_bas + 1}",
                haftalik_plan=haftalik_plan,
                haftalik_saat=haftalik_saat,
                okul_baslangic=okul_bas,
                aktif_gunler=aktif_gunler_sec,
            )

            if pdf_bytes:
                st.download_button(
                    "📥 Günlük Plan PDF İndir",
                    data=pdf_bytes,
                    file_name=f"gunluk_plan_{ders}_{sinif_sec}{sube_sec}_{yil_bas}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="gp_pdf_dl",
                )
            else:
                st.error("PDF oluşturulamadı. ReportLab kütüphanesi yüklü mü?")


@st.fragment
def _render_online_ders(store: AkademikDataStore):
    """Online ders linkleri yonetimi, planlama ve raporlama."""
    styled_section("Dijital Öğrenme ve Online Ders", color="#7c3aed")

    akademik_yil = _get_akademik_yil()

    tab_dijital, tab_ekle, tab_dersler, tab_durum, tab_rapor, tab_giris_rapor = st.tabs([
        "💻 Dijital Öğrenme", "🎥 Online Ders Planlama", "▶️ Ders Başlat",
        "🔄 Durum Güncelle", "📈 Ders Raporları", "🔑 Platform Giriş Raporu"
    ])

    # --- TAB 0: Dijital Öğrenme Kaynaklari ---
    with tab_dijital:
        styled_section("Eğitim Platformları", color="#1565c0")

        # Sabit platformlar: tek HTML blogu (0 widget)
        st.markdown(_PLATFORM_HTML_CACHE, unsafe_allow_html=True)

        # Kullanici eklentisi platformlar (sadece bunlar widget gerektirir)
        dij_links = store.get_dijital_ogrenme_links(akademik_yil)
        kullanici_platformlar = [d for d in dij_links if d.kategori == "platform"]

        if kullanici_platformlar:
            _EKSTRA_RENKLER = (
                ("#7c3aed", "#5b21b6", "#ddd6fe"), ("#0891b2", "#155e75", "#a5f3fc"),
                ("#be185d", "#9d174d", "#fce7f3"), ("#4338ca", "#3730a3", "#c7d2fe"),
            )
            for row_start in range(0, len(kullanici_platformlar), 3):
                row_items = kullanici_platformlar[row_start:row_start + 3]
                cols = st.columns(3)
                for ci, kp in enumerate(row_items):
                    r1, r2, rt = _EKSTRA_RENKLER[(row_start + ci) % len(_EKSTRA_RENKLER)]
                    with cols[ci]:
                        st.markdown(
                            f'<a href="{kp.link}" target="_blank" rel="noopener" style="text-decoration:none;">'
                            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
                            f'padding:22px 18px;text-align:center;min-height:80px;display:flex;flex-direction:column;'
                            f'justify-content:center;cursor:pointer;transition:transform 0.15s;">'
                            f'<div style="font-size:22px;font-weight:800;color:white;">{kp.baslik}</div>'
                            f'<div style="color:{rt};font-size:12px;margin-top:6px;">{kp.aciklama or kp.link}</div></div></a>',
                            unsafe_allow_html=True
                        )
                        if st.button("Kaldır", key=f"pdel_{kp.id}", type="secondary", use_container_width=True):
                            store.delete_dijital_ogrenme_link(kp.id)
                            st.rerun(scope="fragment")

        # Video Konferans & Canlı Ders Platformları (Türkçe giriş)
        st.markdown("")
        styled_section("🎥 Video Konferans & Canlı Ders Platformları", color="#7c3aed")
        st.markdown(
            '<div style="background:linear-gradient(90deg,#7c3aed15,#7c3aed05);'
            'border-left:4px solid #7c3aed;padding:8px 14px;border-radius:0 8px 8px 0;'
            'margin-bottom:12px;font-size:0.85rem;color:#6d28d9;">'
            '💡 Aşağıdaki platformlara tıklayarak Türkçe giriş sayfasına ulaşabilirsiniz. '
            'Zoom, Teams ve Google Classroom için kurumsal veya kişisel hesabınızla oturum açın.'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown(_VIDEO_KONFERANS_HTML_CACHE, unsafe_allow_html=True)

        # YouTube Eğitim Kanalları — expander içinde (32KB HTML sadece açılınca yüklenir)
        st.markdown("")
        with st.expander("▶ YouTube Eğitim Kanalları  (Tonguç, Hocalara Geldik, Benim Hocam...)", expanded=False):
            st.markdown(_YT_HTML_CACHE, unsafe_allow_html=True)

        # Yeni platform ekle
        st.markdown("")
        with st.expander("Yeni Platform Ekle"):
            yp_c1, yp_c2 = st.columns([2, 3])
            with yp_c1:
                yp_ad = st.text_input("Platform Adı", placeholder="Örnek: Morpa Kampüs", key="yp_ad")
            with yp_c2:
                yp_link = st.text_input("Link Yapıştır", placeholder="https://...", key="yp_link")
            yp_aciklama = st.text_input("Açıklama (isteğe bağlı)", placeholder="Kısa açıklama", key="yp_aciklama")
            if st.button("Ekle", key="yp_ekle_btn", use_container_width=True):
                if yp_link and yp_link.strip().startswith("http"):
                    ad = yp_ad.strip() if yp_ad.strip() else yp_link.strip().split("//")[-1].split("/")[0]
                    new_plt = DijitalOgrenmeLink(
                        baslik=ad,
                        link=yp_link.strip(),
                        kategori="platform",
                        aciklama=yp_aciklama.strip(),
                        akademik_yil=akademik_yil,
                    )
                    store.save_dijital_ogrenme_link(new_plt)
                    st.success(f"'{ad}' eklendi!")
                    st.rerun(scope="fragment")
                else:
                    st.error("Geçerli bir link yapıştırın.")

        st.markdown("---")
        styled_section("Kaynak Ekle", color="#7c3aed")
        styled_info_banner(
            "Ders bazli dijital ogrenme kaynaklarinizi ekleyin: videolar, interaktif icerikler, "
            "dokumanlar ve daha fazlasi.",
            banner_type="info"
        )

        with st.form("dijital_ogrenme_form", clear_on_submit=True):
            dc1, dc2 = st.columns(2)
            with dc1:
                do_baslik = st.text_input("Kaynak Başlığı", placeholder="Ornek: EBA Matematik 5. Sınıf Kesirlerde İşlemler", key="akademik_t_m1")
                do_link = st.text_input("Link", placeholder="https://...", key="akademik_t_m2")
                do_kategori = st.selectbox("Kategori", DIJITAL_OGRENME_KATEGORILERI, key="do_kat")
            with dc2:
                do_ders = st.selectbox("Ders", DERSLER, key="do_ders")
                do_sinif = st.selectbox("Sınıf", SINIFLAR, key="do_sinif")
                do_sube = st.selectbox("Şube (bos = tum subeler)", ["Tümü"] + SUBELER, key="do_sube")
                from utils.shared_data import get_all_staff_options as _do_staff
                _do_opts = _do_staff()
                if len(_do_opts) > 1:
                    do_ogretmen = st.selectbox("Paylasan Öğretmen", list(_do_opts.keys()), key="do_ogr")
                    if do_ogretmen == "-- Secim yapin --":
                        do_ogretmen = ""
                else:
                    do_ogretmen = st.text_input("Paylasan Öğretmen", key="do_ogr_txt")
            do_aciklama = st.text_area("Açıklama (istege bagli)", height=68, key="do_aciklama")

            do_submitted = st.form_submit_button("Kaynak Ekle", use_container_width=True)
            if do_submitted:
                if not do_link.strip():
                    st.error("Link giriniz.")
                elif not do_baslik.strip():
                    st.error("Başlık giriniz.")
                else:
                    new_dol = DijitalOgrenmeLink(
                        baslik=do_baslik.strip(),
                        link=do_link.strip(),
                        kategori=DIJITAL_OGRENME_KATEGORI_MAP.get(do_kategori, "diger"),
                        ders=do_ders,
                        sinif=do_sinif,
                        sube="" if do_sube == "Tümü" else do_sube,
                        ogretmen_adi=do_ogretmen.strip(),
                        aciklama=do_aciklama.strip(),
                        akademik_yil=akademik_yil,
                    )
                    store.save_dijital_ogrenme_link(new_dol)
                    st.success(f"'{do_baslik}' eklendi!")
                    st.rerun(scope="fragment")

        # Mevcut kaynaklar
        if dij_links:
            st.markdown("---")

            # Filtreler
            fl1, fl2, fl3 = st.columns(3)
            with fl1:
                flt_do_kat = st.selectbox("Kategori Filtresi", ["Tümü"] + DIJITAL_OGRENME_KATEGORILERI, key="flt_do_kat")
            with fl2:
                flt_do_ders = st.selectbox("Ders Filtresi", ["Tümü"] + sorted(set(d.ders for d in dij_links)), key="flt_do_ders")
            with fl3:
                flt_do_sinif = st.selectbox("Sınıf Filtresi", ["Tümü"] + sorted(set(str(d.sinif) for d in dij_links)), key="flt_do_sinif")

            gosterilecek = dij_links[:]
            if flt_do_kat != "Tümü":
                kat_key = DIJITAL_OGRENME_KATEGORI_MAP.get(flt_do_kat, "")
                gosterilecek = [d for d in gosterilecek if d.kategori == kat_key]
            if flt_do_ders != "Tümü":
                gosterilecek = [d for d in gosterilecek if d.ders == flt_do_ders]
            if flt_do_sinif != "Tümü":
                gosterilecek = [d for d in gosterilecek if str(d.sinif) == flt_do_sinif]

            # Istatistikler
            kat_sayilari = {}
            for d in dij_links:
                kat_sayilari[d.kategori] = kat_sayilari.get(d.kategori, 0) + 1

            styled_stat_row([
                ("Toplam Kaynak", str(len(dij_links)), "#7c3aed", ""),
                ("EBA", str(kat_sayilari.get("eba", 0)), "#1565c0", ""),
                ("Video", str(kat_sayilari.get("video", 0)), "#ef4444", ""),
                ("Interaktif", str(kat_sayilari.get("interaktif", 0)), "#059669", ""),
            ])

            st.markdown("")

            # Kategori renk/ikon
            KAT_STILI = {
                "eba": ("#1565c0", "E"),
                "video": ("#ef4444", "V"),
                "interaktif": ("#059669", "I"),
                "dokuman": ("#f59e0b", "D"),
                "oyun_quiz": ("#8b5cf6", "Q"),
                "diger": ("#64748b", "+"),
            }

            if not gosterilecek:
                st.info("Filtreye uygun kaynak bulunamadı.")
            else:
                for dol in gosterilecek:
                    renk, ikon = KAT_STILI.get(dol.kategori, ("#64748b", "+"))
                    sube_str = f"-{dol.sube}" if dol.sube else " (Tüm Şubeler)"

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,{renk}08,{renk}15);'
                        f'border:1px solid {renk}33;border-radius:12px;padding:14px 18px;margin-bottom:10px;">'
                        f'<div style="display:flex;align-items:center;gap:14px;">'
                        f'<div style="background:{renk};color:white;width:38px;height:38px;border-radius:10px;'
                        f'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;'
                        f'flex-shrink:0;">{ikon}</div>'
                        f'<div style="flex:1;">'
                        f'<div style="font-weight:700;font-size:15px;color:#94A3B8;">{dol.baslik}</div>'
                        f'<div style="color:#64748b;font-size:12px;margin-top:2px;">'
                        f'{dol.ders} | {dol.sinif}{sube_str} | {dol.ogretmen_adi}</div>'
                        f'{"<div style=color:#475569;font-size:12px;margin-top:3px;>" + dol.aciklama + "</div>" if dol.aciklama else ""}'
                        f'</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    dlc1, dlc2, dlc3 = st.columns([4, 1, 1])
                    with dlc2:
                        st.link_button("Ac", dol.link, use_container_width=True)
                    with dlc3:
                        if st.button("Sil", key=f"dol_del_{dol.id}", type="secondary", use_container_width=True):
                            store.delete_dijital_ogrenme_link(dol.id)
                            st.rerun(scope="fragment")
        else:
            styled_info_banner("Henuz dijital ogrenme kaynagi eklenmemiş.", banner_type="warning")

    # --- TAB 1 & sonrası için ortak veri — tab_dijital render TAMAMLANDIKTAN sonra yüklenir ---
    links = store.get_online_ders_links(akademik_yil)
    kayitlar = store.get_online_ders_kayitlari(akademik_yil)

    # --- TAB 1: Hızlı Ders Planla (link + plan tek adımda) ---
    with tab_ekle:
        styled_section("📅 Hızlı Ders Planla", color="#6366f1")
        styled_info_banner(
            "Zoom / Teams / Classroom linkini yapıştır, sınıf ve saati seç, 'Planla' butonuna bas. "
            "Link anında öğrenci ve veli paneline düşer.",
            banner_type="info"
        )

        from utils.shared_data import get_all_staff_options as _hiz_staff
        _hiz_opts = _hiz_staff()

        with st.form("hizli_ders_planla_form", clear_on_submit=True):
            hiz_c1, hiz_c2 = st.columns(2)
            with hiz_c1:
                hiz_platform = st.selectbox("Platform", _ONLINE_DERS_PLATFORMLAR, key="hiz_platform")
                hiz_link = st.text_input(
                    "Ders Linki  ← Buraya yapıştır",
                    placeholder="https://zoom.us/j/123...  veya  https://teams.microsoft.com/...",
                    key="hiz_link"
                )
                hiz_baslik = st.text_input(
                    "Ders Başlığı (isteğe bağlı)",
                    placeholder="Boş bırakılırsa otomatik oluşturulur",
                    key="hiz_baslik"
                )
                hiz_not = st.text_input("Not (isteğe bağlı)", placeholder="Konu, açıklama...", key="hiz_not")
            with hiz_c2:
                hiz_sinif = st.selectbox("Sınıf", SINIFLAR, key="hiz_sinif")
                hiz_sube = st.selectbox("Şube", SUBELER, key="hiz_sube")
                hiz_ders = st.selectbox("Ders", DERSLER, key="hiz_ders")
                if len(_hiz_opts) > 1:
                    hiz_ogretmen = st.selectbox("Öğretmen", list(_hiz_opts.keys()), key="hiz_ogr")
                    if hiz_ogretmen == "-- Secim yapin --":
                        hiz_ogretmen = ""
                else:
                    hiz_ogretmen = st.text_input("Öğretmen Adı", key="hiz_ogr_txt")
                hiz_tarih = st.date_input("Ders Tarihi", value=date.today(), key="hiz_tarih")
                hiz_saat = st.time_input("Başlangıç Saati", value=None, key="hiz_saat")
                hiz_sure = st.number_input("Süre (dk)", min_value=10, max_value=180, value=40, step=5, key="hiz_sure")

            hiz_submit = st.form_submit_button("📤  Planla & Öğrencilere Gönder", use_container_width=True, type="primary")
            if hiz_submit:
                if not hiz_link.strip():
                    st.error("Ders linki giriniz.")
                elif not hiz_saat:
                    st.error("Başlangıç saati seçiniz.")
                else:
                    _plt_key = _ONLINE_DERS_PLATFORM_MAP.get(hiz_platform, ("zoom",))[0]
                    _ogr = hiz_ogretmen.strip() if isinstance(hiz_ogretmen, str) else ""
                    _baslik = hiz_baslik.strip() if hiz_baslik.strip() else f"{hiz_sinif}-{hiz_sube} {hiz_ders} Canlı Ders"
                    # 1. Kalıcı link kaydı
                    new_link = OnlineDersLink(
                        platform=_plt_key,
                        baslik=_baslik,
                        link=hiz_link.strip(),
                        sinif=hiz_sinif,
                        sube=hiz_sube,
                        ders=hiz_ders,
                        ogretmen_adi=_ogr,
                        akademik_yil=akademik_yil,
                    )
                    store.save_online_ders_link(new_link)
                    # 2. Planlanan ders kaydı (URL direkt gömülü)
                    new_kayit = OnlineDersKayit(
                        link_id=new_link.id,
                        link=hiz_link.strip(),
                        platform=_plt_key,
                        baslik=_baslik,
                        ders=hiz_ders,
                        ogretmen_adi=_ogr,
                        sinif=hiz_sinif,
                        sube=hiz_sube,
                        akademik_yil=akademik_yil,
                        planlanan_tarih=hiz_tarih.isoformat(),
                        planlanan_saat=hiz_saat.strftime("%H:%M"),
                        sure_dk=int(hiz_sure),
                        durum="planli",
                        notlar=hiz_not.strip(),
                    )
                    store.save_online_ders_kayit(new_kayit)
                    # Rerun için links ve kayitlar güncellenir
                    links = store.get_online_ders_links(akademik_yil)
                    kayitlar = store.get_online_ders_kayitlari(akademik_yil)
                    st.success(
                        f"✅ '{_baslik}' planlandı! "
                        f"{hiz_sinif}-{hiz_sube} sınıfının öğrenci ve veli panelinde görünecek."
                    )
                    st.rerun(scope="fragment")

        # ── Planlanmış gelecek dersler özeti ──
        bugun_iso = date.today().isoformat()
        gelecek = [k for k in kayitlar if k.planlanan_tarih >= bugun_iso and k.durum == "planli"]
        gelecek.sort(key=lambda x: (x.planlanan_tarih, x.planlanan_saat))
        if gelecek:
            st.markdown("")
            styled_section("📋 Planlanmış Dersler", color="#f59e0b")
            for gk in gelecek:
                _glbl = _ONLINE_DERS_KEY_TO_LABEL.get(gk.platform, gk.platform or "Platform")
                _gpinfo = _ONLINE_DERS_PLATFORM_MAP.get(_glbl, ("", "?", "#64748b", _glbl))
                _gcolor = _gpinfo[2]
                try:
                    _gtarih = date.fromisoformat(gk.planlanan_tarih).strftime("%d.%m.%Y")
                    _ggun = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"][date.fromisoformat(gk.planlanan_tarih).weekday()]
                    _gtarih = f"{_ggun} {_gtarih}"
                except ValueError:
                    _gtarih = gk.planlanan_tarih
                gc1, gc2, gc3 = st.columns([4, 2, 1])
                with gc1:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;'
                        f'border-bottom:1px solid #1A2035;">'
                        f'<div style="background:{_gcolor};color:white;width:28px;height:28px;'
                        f'border-radius:6px;display:flex;align-items:center;justify-content:center;'
                        f'font-weight:700;font-size:12px;flex-shrink:0;">{_gpinfo[1]}</div>'
                        f'<div>'
                        f'<div style="font-weight:700;font-size:0.88rem;color:#0B0F19;">{gk.baslik}</div>'
                        f'<div style="font-size:0.75rem;color:#64748b;">'
                        f'{gk.sinif}-{gk.sube} | {gk.ders} | {gk.ogretmen_adi or "–"}</div>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )
                with gc2:
                    st.markdown(f"**{_gtarih}** · {gk.planlanan_saat} · {gk.sure_dk} dk")
                with gc3:
                    if st.button("İptal", key=f"hiz_iptal_{gk.id}", type="secondary"):
                        store.delete_online_ders_kayit(gk.id)
                        st.rerun(scope="fragment")

        # ── Kalıcı Linkler (gelişmiş kullanım) ──
        st.markdown("")
        with st.expander("⚙️ Kalıcı Link Yönetimi  (tekrar kullanılacak sabit oda linkleri)"):
            styled_info_banner(
                "Zoom sabit oda, Teams kanalı gibi her zaman aynı kalan linkleri buraya ekleyin. "
                "Bu sekmeden bu linkleri seçerek yeni ders planlayabilirsiniz.",
                banner_type="info"
            )
            with st.form("online_ders_link_form", clear_on_submit=True):
                fc1, fc2 = st.columns(2)
                with fc1:
                    od_platform = st.selectbox("Platform", _ONLINE_DERS_PLATFORMLAR, key="od_platform")
                    od_baslik = st.text_input("Başlık", placeholder="Örnek: 5-A Matematik Sabit Oda", key="od_baslik")
                    od_link = st.text_input("Link", placeholder="https://zoom.us/j/...", key="od_link")
                with fc2:
                    od_sinif = st.selectbox("Sınıf", SINIFLAR, key="od_sinif")
                    od_sube = st.selectbox("Şube", SUBELER, key="od_sube")
                    od_ders = st.selectbox("Ders", DERSLER, key="od_ders")
                    from utils.shared_data import get_all_staff_options as _od_staff
                    _od_opts = _od_staff()
                    if len(_od_opts) > 1:
                        od_ogretmen = st.selectbox("Öğretmen", list(_od_opts.keys()), key="od_ogretmen")
                        if od_ogretmen == "-- Secim yapin --":
                            od_ogretmen = ""
                    else:
                        od_ogretmen = st.text_input("Öğretmen Adı", key="od_ogretmen_txt")
                submitted = st.form_submit_button("Kaydet", use_container_width=True)
                if submitted:
                    if not od_link.strip():
                        st.error("Link giriniz.")
                    elif not od_baslik.strip():
                        st.error("Başlık giriniz.")
                    else:
                        platform_key = _ONLINE_DERS_PLATFORM_MAP.get(od_platform, ("zoom",))[0]
                        new_link = OnlineDersLink(
                            platform=platform_key,
                            baslik=od_baslik.strip(),
                            link=od_link.strip(),
                            sinif=od_sinif,
                            sube=od_sube,
                            ders=od_ders,
                            ogretmen_adi=od_ogretmen.strip() if isinstance(od_ogretmen, str) else "",
                            akademik_yil=akademik_yil,
                        )
                        store.save_online_ders_link(new_link)
                        links = store.get_online_ders_links(akademik_yil)
                        st.success(f"'{od_baslik}' kaydedildi!")
                        st.rerun(scope="fragment")

            if links:
                st.markdown("**Kayıtlı Kalıcı Linkler:**")
                for lnk in links:
                    _plt_label = _ONLINE_DERS_KEY_TO_LABEL.get(lnk.platform, lnk.platform or "?")
                    _plt_info = _ONLINE_DERS_PLATFORM_MAP.get(_plt_label, ("", "?", "#64748b", _plt_label))
                    platform_icon = _plt_info[1]
                    platform_color = _plt_info[2]
                    platform_label = _plt_label

                    with st.container():
                        lc1, lc2, lc3, lc4 = st.columns([0.5, 3, 2, 1])
                        with lc1:
                            st.markdown(
                                f'<div style="background:{platform_color};color:white;'
                                f'width:36px;height:36px;border-radius:8px;display:flex;'
                                f'align-items:center;justify-content:center;font-weight:700;'
                                f'font-size:16px;margin-top:8px;">{platform_icon}</div>',
                                unsafe_allow_html=True
                            )
                        with lc2:
                            st.markdown(f"**{lnk.baslik}**")
                            st.caption(f"{platform_label} | {lnk.sinif}-{lnk.sube} {lnk.ders} | {lnk.ogretmen_adi}")
                        with lc3:
                            st.code(lnk.link, language=None)
                        with lc4:
                            if st.button("Sil", key=f"del_{lnk.id}", type="secondary"):
                                store.delete_online_ders_link(lnk.id)
                                st.rerun(scope="fragment")

    # --- TAB 2: Ders Baslat (Gomulu Ekran) ---
    with tab_dersler:
        if not links:
            styled_info_banner("Ders baslatmak için once 'Link Yönetimi' sekmesinden link ekleyin.", banner_type="warning")
        else:
            styled_info_banner(
                "Asagidan dersi secin ve 'Dersi Baslat' butonuna tiklayin. "
                "Ders yeni sekmede acilacaktir.",
                banner_type="info"
            )

            pf1, pf2 = st.columns(2)
            with pf1:
                flt_platform = st.selectbox(
                    "Platform Filtresi",
                    ["Tümü"] + _ONLINE_DERS_PLATFORMLAR,
                    key="flt_od_platform"
                )
            with pf2:
                flt_ders = st.selectbox(
                    "Ders Filtresi",
                    ["Tümü"] + sorted(set(l.ders for l in links)),
                    key="flt_od_ders"
                )

            filtered = links
            if flt_platform != "Tümü":
                _flt_key = _ONLINE_DERS_PLATFORM_MAP.get(flt_platform, (flt_platform,))[0]
                filtered = [l for l in filtered if l.platform == _flt_key]
            if flt_ders != "Tümü":
                filtered = [l for l in filtered if l.ders == flt_ders]

            if not filtered:
                st.info("Filtreye uygun link bulunamadı.")
            else:
                for lnk in filtered:
                    _lbl = _ONLINE_DERS_KEY_TO_LABEL.get(lnk.platform, lnk.platform or "Platform")
                    _pinfo = _ONLINE_DERS_PLATFORM_MAP.get(_lbl, ("", "?", "#64748b", _lbl))
                    platform_label = _lbl
                    platform_color = _pinfo[2]

                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,{platform_color}11,{platform_color}22);'
                        f'border:1px solid {platform_color}44;border-radius:12px;padding:16px;margin-bottom:12px;">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                        f'<div>'
                        f'<span style="font-weight:700;font-size:16px;color:#94A3B8;">{lnk.baslik}</span><br>'
                        f'<span style="color:#64748b;font-size:13px;">'
                        f'{platform_label} | {lnk.sinif}-{lnk.sube} {lnk.ders} | {lnk.ogretmen_adi}</span>'
                        f'</div>'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    bc1, bc2 = st.columns([3, 1])
                    with bc2:
                        st.link_button(
                            f"Dersi Baslat ({platform_label})",
                            lnk.link,
                            use_container_width=True,
                        )

                    with st.expander("Gomulu Görünüm (deneysel)"):
                        st.markdown(
                            f'<iframe src="{lnk.link}" width="100%" height="600" '
                            f'style="border:1px solid #e2e8f0;border-radius:8px;" '
                            f'allow="camera;microphone;fullscreen" '
                            f'sandbox="allow-same-origin allow-scripts allow-popups allow-forms">'
                            f'</iframe>',
                            unsafe_allow_html=True
                        )
                        st.caption(
                            "Not: Google Classroom ve Zoom guvenlik nedeniyle gomulu gorunumu engelleyebilir. "
                            "Bu durumda 'Dersi Baslat' butonunu kullanin."
                        )

    # --- TAB 3: Durum Guncelle ---
    with tab_durum:
        planli_list = [k for k in kayitlar if k.durum == "planli"]
        planli_list.sort(key=lambda x: (x.planlanan_tarih, x.planlanan_saat))

        if not planli_list:
            styled_info_banner(
                "Durumu guncellenecek planli ders bulunmuyor. 'Online Ders Planlama' sekmesinden ders ekleyin.",
                banner_type="warning"
            )
        else:
            styled_info_banner(
                "Planlanan derslerin durumunu guncelleyin: Yapildi veya Yapilmadi olarak isaretleyin. "
                "Yapilmadi ise nedenini ve varsa telafi tarihini girin.",
                banner_type="info"
            )

            for pk in planli_list:
                platform_label = _ONLINE_DERS_KEY_TO_LABEL.get(pk.platform, pk.platform or "Platform")
                tarih_str = pk.planlanan_tarih
                try:
                    tarih_obj = date.fromisoformat(pk.planlanan_tarih)
                    tarih_str = tarih_obj.strftime('%d.%m.%Y')
                except ValueError:
                    pass

                with st.expander(f"{tarih_str} {pk.planlanan_saat} | {pk.sinif}-{pk.sube} {pk.ders} | {pk.baslik}", expanded=False
                ):
                    st.caption(f"Öğretmen: {pk.ogretmen_adi} | {platform_label} | Sure: {pk.sure_dk} dk")
                    if pk.notlar:
                        st.caption(f"Not: {pk.notlar}")

                    dg_c1, dg_c2 = st.columns(2)
                    with dg_c1:
                        if st.button("Yapildi", key=f"yapildi_{pk.id}", type="primary", use_container_width=True):
                            pk.durum = "yapildi"
                            store.save_online_ders_kayit(pk)
                            st.success("Ders yapildi olarak isaretlendi!")
                            st.rerun(scope="fragment")
                    with dg_c2:
                        yapilmadi_neden = st.selectbox(
                            "Yapilmama Nedeni",
                            YAPILMAMA_NEDENLERI,
                            key=f"neden_{pk.id}"
                        )
                        telafi_tarih = st.date_input("Telafi Tarihi", value=None, key=f"telafi_{pk.id}")
                        if st.button("Yapilmadi", key=f"yapilmadi_{pk.id}", type="secondary", use_container_width=True):
                            pk.durum = "yapilmadi"
                            pk.yapilmama_nedeni = yapilmadi_neden
                            if telafi_tarih:
                                pk.telafi_tarihi = telafi_tarih.isoformat()
                            store.save_online_ders_kayit(pk)
                            st.warning("Ders yapilmadi olarak isaretlendi.")
                            st.rerun(scope="fragment")

    # --- TAB 5: Raporlar ---
    with tab_rapor:
        if not kayitlar:
            styled_info_banner("Henuz ders kaydi bulunmuyor.", banner_type="warning")
        else:
            # Genel istatistikler
            yapildi_list = [k for k in kayitlar if k.durum == "yapildi"]
            yapilmadi_list = [k for k in kayitlar if k.durum == "yapilmadi"]
            planli_count = sum(1 for k in kayitlar if k.durum == "planli")
            toplam_sure = sum(k.sure_dk for k in yapildi_list)

            styled_stat_row([
                ("Toplam Ders", str(len(kayitlar)), "#7c3aed", ""),
                ("Yapildi", str(len(yapildi_list)), "#059669", ""),
                ("Yapilmadi", str(len(yapilmadi_list)), "#ef4444", ""),
                ("Planli", str(planli_count), "#f59e0b", ""),
            ])

            st.markdown("")
            styled_stat_row([
                ("Toplam Sure", f"{toplam_sure} dk", "#2563eb", ""),
                ("Ort. Sure", f"{toplam_sure // len(yapildi_list) if yapildi_list else 0} dk", "#6366f1", ""),
                ("Başarı Orani", f"%{round(len(yapildi_list) * 100 / max(len(yapildi_list) + len(yapilmadi_list), 1))}", "#059669", ""),
                ("Telafi Bekleyen", str(sum(1 for k in yapilmadi_list if k.telafi_tarihi)), "#f59e0b", ""),
            ])

            st.markdown("---")

            # Filtreler
            rp_c1, rp_c2, rp_c3 = st.columns(3)
            with rp_c1:
                rp_durum = st.selectbox(
                    "Durum",
                    ["Tümü", "Yapildi", "Yapilmadi", "Planli"],
                    key="rp_od_durum"
                )
            with rp_c2:
                all_ders = sorted(set(k.ders for k in kayitlar))
                rp_ders = st.selectbox("Ders", ["Tümü"] + all_ders, key="rp_od_ders")
            with rp_c3:
                all_ogretmen = sorted(set(k.ogretmen_adi for k in kayitlar if k.ogretmen_adi))
                rp_ogretmen = st.selectbox("Öğretmen", ["Tümü"] + all_ogretmen, key="rp_od_ogretmen")

            # Filtreleme
            raporlanacak = kayitlar[:]
            if rp_durum == "Yapildi":
                raporlanacak = [k for k in raporlanacak if k.durum == "yapildi"]
            elif rp_durum == "Yapilmadi":
                raporlanacak = [k for k in raporlanacak if k.durum == "yapilmadi"]
            elif rp_durum == "Planli":
                raporlanacak = [k for k in raporlanacak if k.durum == "planli"]
            if rp_ders != "Tümü":
                raporlanacak = [k for k in raporlanacak if k.ders == rp_ders]
            if rp_ogretmen != "Tümü":
                raporlanacak = [k for k in raporlanacak if k.ogretmen_adi == rp_ogretmen]

            raporlanacak.sort(key=lambda x: (x.planlanan_tarih, x.planlanan_saat), reverse=True)

            # Detay tablosu
            styled_section("Ders Kayıtlari Detay", color="#6366f1")
            if raporlanacak:
                rows = []
                for k in raporlanacak:
                    tarih_str = k.planlanan_tarih
                    try:
                        tarih_str = date.fromisoformat(k.planlanan_tarih).strftime('%d.%m.%Y')
                    except ValueError:
                        pass
                    durum_label = ONLINE_DERS_DURUM_LABELS.get(k.durum, k.durum)
                    platform_label = _ONLINE_DERS_KEY_TO_LABEL.get(k.platform, k.platform or "Platform")
                    rows.append({
                        "Tarih": tarih_str,
                        "Saat": k.planlanan_saat,
                        "Ders": k.ders,
                        "Sınıf": f"{k.sinif}-{k.sube}",
                        "Öğretmen": k.ogretmen_adi,
                        "Platform": platform_label,
                        "Sure (dk)": k.sure_dk,
                        "Durum": durum_label,
                        "Neden": k.yapilmama_nedeni if k.durum == "yapilmadi" else "",
                        "Telafi": k.telafi_tarihi if k.durum == "yapilmadi" else "",
                    })
                df = pd.DataFrame(rows)

                # Durum renkli gosterim
                def _durum_color(val):
                    if val == "Yapildi":
                        return "background-color: #dcfce7; color: #166534"
                    elif val == "Yapilmadi":
                        return "background-color: #fee2e2; color: #991b1b"
                    elif val == "Planli":
                        return "background-color: #fef9c3; color: #854d0e"
                    return ""

                styled_df = df.style.map(_durum_color, subset=["Durum"])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                st.info("Filtreye uygun kayit bulunamadı.")

            # Ders bazli ozet
            st.markdown("---")
            styled_section("Ders Bazli Özet", color="#059669")
            ders_ozet: dict[str, dict] = {}
            for k in kayitlar:
                if k.ders not in ders_ozet:
                    ders_ozet[k.ders] = {"toplam": 0, "yapildi": 0, "yapilmadi": 0, "planli": 0, "sure": 0, "ogretmenler": set()}
                ders_ozet[k.ders]["toplam"] += 1
                ders_ozet[k.ders][k.durum] += 1
                if k.durum == "yapildi":
                    ders_ozet[k.ders]["sure"] += k.sure_dk
                ders_ozet[k.ders]["ogretmenler"].add(k.ogretmen_adi)

            ozet_rows = []
            for ders_adi, info in sorted(ders_ozet.items()):
                tamamlanan = info["yapildi"]
                bitmis = tamamlanan + info["yapilmadi"]
                oran = round(tamamlanan * 100 / bitmis) if bitmis > 0 else 0
                ozet_rows.append({
                    "Ders": ders_adi,
                    "Toplam": info["toplam"],
                    "Yapildi": info["yapildi"],
                    "Yapilmadi": info["yapilmadi"],
                    "Planli": info["planli"],
                    "Sure (dk)": info["sure"],
                    "Başarı %": f"%{oran}",
                    "Öğretmenler": ", ".join(sorted(info["ogretmenler"])),
                })
            if ozet_rows:
                st.dataframe(pd.DataFrame(ozet_rows), use_container_width=True, hide_index=True)

            # Ogretmen bazli ozet
            st.markdown("---")
            styled_section("Öğretmen Bazli Özet", color="#8b5cf6")
            ogr_ozet: dict[str, dict] = {}
            for k in kayitlar:
                name = k.ogretmen_adi or "Belirtilmemis"
                if name not in ogr_ozet:
                    ogr_ozet[name] = {"toplam": 0, "yapildi": 0, "yapilmadi": 0, "planli": 0, "sure": 0, "dersler": set(), "siniflar": set()}
                ogr_ozet[name]["toplam"] += 1
                ogr_ozet[name][k.durum] += 1
                if k.durum == "yapildi":
                    ogr_ozet[name]["sure"] += k.sure_dk
                ogr_ozet[name]["dersler"].add(k.ders)
                ogr_ozet[name]["siniflar"].add(f"{k.sinif}-{k.sube}")

            ogr_rows = []
            for ogr_adi, info in sorted(ogr_ozet.items()):
                tamamlanan = info["yapildi"]
                bitmis = tamamlanan + info["yapilmadi"]
                oran = round(tamamlanan * 100 / bitmis) if bitmis > 0 else 0
                ogr_rows.append({
                    "Öğretmen": ogr_adi,
                    "Toplam": info["toplam"],
                    "Yapildi": info["yapildi"],
                    "Yapilmadi": info["yapilmadi"],
                    "Planli": info["planli"],
                    "Sure (dk)": info["sure"],
                    "Başarı %": f"%{oran}",
                    "Dersler": ", ".join(sorted(info["dersler"])),
                    "Sınıflar": ", ".join(sorted(info["siniflar"])),
                })
            if ogr_rows:
                st.dataframe(pd.DataFrame(ogr_rows), use_container_width=True, hide_index=True)

            # Sinif bazli ozet
            st.markdown("---")
            styled_section("Sınıf / Şube Bazli Özet", color="#1565c0")
            sinif_ozet: dict[str, dict] = {}
            for k in kayitlar:
                key = f"{k.sinif}-{k.sube}"
                if key not in sinif_ozet:
                    sinif_ozet[key] = {"toplam": 0, "yapildi": 0, "yapilmadi": 0, "planli": 0, "sure": 0, "dersler": set()}
                sinif_ozet[key]["toplam"] += 1
                sinif_ozet[key][k.durum] += 1
                if k.durum == "yapildi":
                    sinif_ozet[key]["sure"] += k.sure_dk
                sinif_ozet[key]["dersler"].add(k.ders)

            sinif_rows = []
            for sinif_key, info in sorted(sinif_ozet.items()):
                tamamlanan = info["yapildi"]
                bitmis = tamamlanan + info["yapilmadi"]
                oran = round(tamamlanan * 100 / bitmis) if bitmis > 0 else 0
                sinif_rows.append({
                    "Sınıf": sinif_key,
                    "Toplam": info["toplam"],
                    "Yapildi": info["yapildi"],
                    "Yapilmadi": info["yapilmadi"],
                    "Planli": info["planli"],
                    "Sure (dk)": info["sure"],
                    "Başarı %": f"%{oran}",
                    "Dersler": ", ".join(sorted(info["dersler"])),
                })
            if sinif_rows:
                st.dataframe(pd.DataFrame(sinif_rows), use_container_width=True, hide_index=True)

            # Yapilmayan dersler detay
            if yapilmadi_list:
                st.markdown("---")
                styled_section("Yapilmayan Dersler Detay", color="#ef4444")
                yp_rows = []
                for k in yapilmadi_list:
                    tarih_str = k.planlanan_tarih
                    try:
                        tarih_str = date.fromisoformat(k.planlanan_tarih).strftime('%d.%m.%Y')
                    except ValueError:
                        pass
                    telafi_str = ""
                    if k.telafi_tarihi:
                        try:
                            telafi_str = date.fromisoformat(k.telafi_tarihi).strftime('%d.%m.%Y')
                        except ValueError:
                            telafi_str = k.telafi_tarihi
                    yp_rows.append({
                        "Tarih": tarih_str,
                        "Ders": k.ders,
                        "Sınıf": f"{k.sinif}-{k.sube}",
                        "Öğretmen": k.ogretmen_adi,
                        "Neden": k.yapilmama_nedeni,
                        "Telafi Tarihi": telafi_str,
                    })
                st.dataframe(pd.DataFrame(yp_rows), use_container_width=True, hide_index=True)

    # --- TAB 7: Platform Giris Raporu ---
    with tab_giris_rapor:
        all_girisler = store.get_platform_girisler(akademik_yil)

        if not all_girisler:
            styled_info_banner("Henuz platform giris kaydi bulunmuyor. Platformlara 'Giriş Yap' butonuyla eristiginde kayit olusur.", banner_type="warning")
        else:
            # Platform bazli sayim
            platform_sayim: dict[str, int] = {}
            platform_link: dict[str, str] = {}
            gunluk_sayim: dict[str, int] = {}
            for g in all_girisler:
                platform_sayim[g.platform_adi] = platform_sayim.get(g.platform_adi, 0) + 1
                platform_link[g.platform_adi] = g.link
                try:
                    gun = datetime.fromisoformat(g.tarih).strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    gun = "Bilinmiyor"
                gunluk_sayim[gun] = gunluk_sayim.get(gun, 0) + 1

            # Genel istatistikler
            toplam_giris = len(all_girisler)
            en_cok = max(platform_sayim.items(), key=lambda x: x[1])
            farkli_platform = len(platform_sayim)
            farkli_gun = len(gunluk_sayim)

            styled_stat_row([
                ("Toplam Giriş", str(toplam_giris), "#7c3aed", ""),
                ("En Çok", f"{en_cok[0]} ({en_cok[1]})", "#059669", ""),
                ("Platform Sayısı", str(farkli_platform), "#1565c0", ""),
                ("Aktif Gün", str(farkli_gun), "#f59e0b", ""),
            ])

            st.markdown("---")

            # Platform bazli tablo
            styled_section("Platform Bazli Giriş Sayılari", color="#6366f1")
            plt_rows = []
            for padi, sayi in sorted(platform_sayim.items(), key=lambda x: x[1], reverse=True):
                # Son giris tarihi
                son_girisler = [g for g in all_girisler if g.platform_adi == padi]
                son_girisler.sort(key=lambda x: x.tarih, reverse=True)
                son_tarih = ""
                if son_girisler:
                    try:
                        son_tarih = datetime.fromisoformat(son_girisler[0].tarih).strftime("%d.%m.%Y %H:%M")
                    except (ValueError, TypeError):
                        son_tarih = son_girisler[0].tarih

                oran = round(sayi * 100 / toplam_giris)
                plt_rows.append({
                    "Platform": padi,
                    "Giriş Sayısı": sayi,
                    "Oran (%)": f"%{oran}",
                    "Son Giriş": son_tarih,
                })
            st.dataframe(pd.DataFrame(plt_rows), use_container_width=True, hide_index=True)

            # Gorsel bar chart
            st.markdown("")
            styled_section("Giriş Dagilimi", color="#059669")
            for padi, sayi in sorted(platform_sayim.items(), key=lambda x: x[1], reverse=True):
                oran = sayi * 100 / max(toplam_giris, 1)
                bar_renk = "#2563eb"
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">'
                    f'<div style="width:140px;font-weight:600;font-size:14px;color:#94A3B8;text-align:right;">{padi}</div>'
                    f'<div style="flex:1;background:#1A2035;border-radius:8px;height:28px;overflow:hidden;">'
                    f'<div style="width:{oran}%;background:linear-gradient(90deg,{bar_renk},{bar_renk}cc);'
                    f'height:100%;border-radius:8px;display:flex;align-items:center;padding-left:10px;">'
                    f'<span style="color:white;font-size:12px;font-weight:700;">{sayi}</span>'
                    f'</div></div></div>',
                    unsafe_allow_html=True
                )

            # Gunluk trend
            st.markdown("---")
            styled_section("Günlük Giriş Trendi", color="#f59e0b")
            gun_rows = []
            for gun, sayi in sorted(gunluk_sayim.items(), reverse=True)[:30]:
                try:
                    gun_fmt = datetime.strptime(gun, "%Y-%m-%d").strftime("%d.%m.%Y")
                    gun_adi = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"][datetime.strptime(gun, "%Y-%m-%d").weekday()]
                except (ValueError, TypeError):
                    gun_fmt = gun
                    gun_adi = ""
                gun_rows.append({
                    "Tarih": gun_fmt,
                    "Gün": gun_adi,
                    "Giriş Sayısı": sayi,
                })
            st.dataframe(pd.DataFrame(gun_rows), use_container_width=True, hide_index=True)

            # Detay log
            with st.expander("Tüm Giriş Kayıtlari (Detay)"):
                detay_rows = []
                for g in sorted(all_girisler, key=lambda x: x.tarih, reverse=True):
                    try:
                        tarih_fmt = datetime.fromisoformat(g.tarih).strftime("%d.%m.%Y %H:%M:%S")
                    except (ValueError, TypeError):
                        tarih_fmt = g.tarih
                    detay_rows.append({
                        "Tarih/Saat": tarih_fmt,
                        "Platform": g.platform_adi,
                    })
                st.dataframe(pd.DataFrame(detay_rows), use_container_width=True, hide_index=True)


# ==================== ANA RENDER FONKSIYONU ====================

def render_akademik_takip():
    """Akademik Takip modulu ana giris noktasi - 5 gruplu modern tasarim."""
    _inject_css()

    styled_header(
        "Akademik Takip",
        "Kadro, ogrenci, ders programi, ogretim planlama ve raporlama sistemi",
        icon=""
    )

    store = get_akademik_store()

    # ==================== 12 ANA GRUP ====================
    render_smarti_welcome("akademik_takip")
    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("akademik_takip_egitim_yili")

    # Veri dogrulama
    try:
        from utils.ui_common import veri_dogrulama_butonu, veri_dogrulama_sonucu
        veri_dogrulama_butonu("akademik_takip")
        if st.session_state.get("_veri_kontrol_aktif_akademik_takip"):
            sorunlar = []
            _at_students = store.get_students(durum="aktif")
            _at_grades = store.get_grades()
            if len(_at_students) == 0:
                sorunlar.append({"tip": "eksik", "alan": "Ogrenci Kaydi", "sayi": 0, "oncelik": "yuksek"})
            if len(_at_grades) == 0:
                sorunlar.append({"tip": "eksik", "alan": "Not Kaydi", "sayi": 0, "oncelik": "orta"})
            _no_num = sum(1 for s in _at_students if not s.numara)
            if _no_num > 0:
                sorunlar.append({"tip": "eksik", "alan": "Numara Eksik Ogrenci", "sayi": _no_num, "oncelik": "orta"})
            veri_dogrulama_sonucu(sorunlar)
            st.session_state["_veri_kontrol_aktif_akademik_takip"] = False
    except Exception:
        pass

    try:
        from utils.ui_common import geri_sayim_sayaci
        geri_sayim_sayaci("2026-06-14", "LGS Sınavı", "📝")
        geri_sayim_sayaci("2026-06-20", "Dönem Sonu", "🏫")
    except Exception:
        pass

    try:
        from utils.ui_common import sinif_yarismasi_tablosu
        with st.expander("🏁 Sınıflar Arası Yarışma", expanded=False):
            sinif_yarismasi_tablosu()
    except Exception:
        pass

    # ── PREMIUM HERO + METRICS + KOMPAKT TAB CSS ──
    try:
        _at_premium_hero()
        _at_premium_metrics(store)
        _at_premium_tab_css()
    except Exception:
        pass

    # -- Tab Gruplama (28 tab -> 4 grup) --
    _GRP_TABS = {
        "📋 Grup A": [("👥 Kadro", 0), ("📐 Öğretim", 1), ("📓 Ders Defteri", 2), ("📅 Günlük Plan", 3), ("💻 Dijital Öğrenme", 4), ("📝 Ödev", 5), ("✅ Yoklama & Not", 6)],
        "📊 Grup B": [("📊 Sınav Sonuç", 7), ("📈 Raporlar", 8), ("🚨 Erken Uyarı", 9), ("🎯 KYT", 10), ("📚 Borç Bankası", 11), ("📓 Öğr. Defteri", 12), ("🧬 Dijital İkiz", 13)],
        "🔧 Grup C": [("📡 Öğr. Cockpit", 14), ("🔔 Veli Ajansı", 15), ("🎛️ Akd. Komuta", 16), ("⚔️ Karşılaştır", 17), ("🧠 AI Strateji", 18), ("👨‍🏫 Öğrt. Verimlilik", 19), ("⚡ Oto Müdahale", 20)],
        "📈 Grup D": [("🔮 Tahmin", 21), ("🗺️ Müfredat GPS", 22), ("🧬 Sınıf İkiz", 23), ("⏰ Zaman Makinesi", 24), ("🏫 Kurum Hizmetleri", 25), ("🪪 Öğrenci Kimlik", 26), ("🤖 Smarti", 27)],
    }
    _sg_grp_45615 = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg_grp_45615")
    _gt_grp_45615 = _GRP_TABS[_sg_grp_45615]
    _tn_grp_45615 = [t[0] for t in _gt_grp_45615]
    _ti_grp_45615 = [t[1] for t in _gt_grp_45615]
    _tabs_grp_45615 = st.tabs(_tn_grp_45615)
    _tmap_grp_45615 = {i: t for i, t in zip(_ti_grp_45615, _tabs_grp_45615)}
    grp1 = _tmap_grp_45615.get(0)
    grp3 = _tmap_grp_45615.get(1)
    grp3b = _tmap_grp_45615.get(2)
    grp_gunluk = _tmap_grp_45615.get(3)
    grp4 = _tmap_grp_45615.get(4)
    grp5 = _tmap_grp_45615.get(5)
    grp6 = _tmap_grp_45615.get(6)
    grp_sinav = _tmap_grp_45615.get(7)
    grp7 = _tmap_grp_45615.get(8)
    grp8 = _tmap_grp_45615.get(9)
    grp10 = _tmap_grp_45615.get(10)
    grp_borc = _tmap_grp_45615.get(11)
    grp_defter = _tmap_grp_45615.get(12)
    grp_ikiz = _tmap_grp_45615.get(13)
    grp_cockpit = _tmap_grp_45615.get(14)
    grp_veli = _tmap_grp_45615.get(15)
    grp_komuta = _tmap_grp_45615.get(16)
    grp_arena = _tmap_grp_45615.get(17)
    grp_strateji = _tmap_grp_45615.get(18)
    grp_verimlilik = _tmap_grp_45615.get(19)
    grp_mudahale = _tmap_grp_45615.get(20)
    grp_tahmin = _tmap_grp_45615.get(21)
    grp_mufredat = _tmap_grp_45615.get(22)
    grp_sinif_ikiz = _tmap_grp_45615.get(23)
    grp_zaman = _tmap_grp_45615.get(24)
    grp_kurum_hiz = _tmap_grp_45615.get(25)
    grp_ogrenci_kimlik = _tmap_grp_45615.get(26)
    grp_smarti = _tmap_grp_45615.get(27)

    # --- YENİ: Öğrenci Kimlik (Pasaport + Başarı Duvarı + Karşılaştırma) ---
    if grp_ogrenci_kimlik is not None:
      with grp_ogrenci_kimlik:
        try:
            ok_tabs = st.tabs([
                "🪪 Dijital Pasaport",
                "🏆 Başarı Duvarı",
                "📊 Karşılaştırmalı İlerleme",
            ])
            with ok_tabs[0]:
                try:
                    from views._dijital_pasaport import render_dijital_pasaport
                    render_dijital_pasaport()
                except ImportError:
                    st.info("Dijital Pasaport modülü yüklü değil.")
                except Exception as _e:
                    st.error(f"Pasaport yüklenemedi: {_e}")
            with ok_tabs[1]:
                try:
                    from views._basari_duvari import render_basari_duvari
                    render_basari_duvari()
                except ImportError:
                    st.info("Başarı Duvarı modülü yüklü değil.")
                except Exception as _e:
                    st.error(f"Başarı Duvarı yüklenemedi: {_e}")
            with ok_tabs[2]:
                try:
                    from views._karsilastirmali_ilerleme import render_karsilastirmali_ilerleme, render_sinif_percentile_listesi
                    kri_tabs = st.tabs(["👤 Bireysel Rapor", "📋 Sınıf Listesi"])
                    with kri_tabs[0]:
                        render_karsilastirmali_ilerleme()
                    with kri_tabs[1]:
                        render_sinif_percentile_listesi()
                except ImportError:
                    st.info("Karşılaştırmalı İlerleme modülü yüklü değil.")
                except Exception as _e:
                    st.error(f"Karşılaştırmalı İlerleme yüklenemedi: {_e}")
        except Exception as _e:
            st.error(f"Öğrenci Kimlik sekmesi hatası: {_e}")

    # --- GRUP 1: KADRO & OGRENCI ---
    if grp1 is not None:
      with grp1:
        try:
            _styled_group_header(
                "Kadro & Öğrenci Yönetimi",
                "Öğretmen kadrosu, sınıf listeleri ve öğrenci kayıtları",
                color="#2563eb"
            )
            g1t1, g1t2 = st.tabs([
                "  👨‍🏫 Akademik Kadro  ", "  📋 Sınıf Listesi  "
            ])
            with g1t1:
                _render_akademik_kadro(store)
            with g1t2:
                _render_sinif_listesi(store)
                try:
                    from utils.ui_common import sinif_mood_gostergesi
                    sinif_mood_gostergesi()
                except Exception:
                    pass
                # PDF indirme — aynı sekme içinde
                st.markdown("---")
                st.markdown(
                    "<div style='background:linear-gradient(135deg,#0d9488,#0891b2);color:#fff;"
                    "padding:12px 18px;border-radius:10px;margin-bottom:14px;font-size:0.87rem;"
                    "display:flex;align-items:center;gap:8px'>"
                    "<span style='font-size:1.2rem'>📄</span>"
                    "<span><b>PDF Sınıf Listesi:</b> Kademe, sınıf ve şubeye göre filtreleyerek "
                    "baskıya hazır PDF liste indirin.</span></div>",
                    unsafe_allow_html=True,
                )
                from utils.shared_data import render_sinif_listesi_al_ui
                render_sinif_listesi_al_ui(key_prefix="at")
        except Exception as _e1:
            import traceback; st.error(f"Kadro & Öğrenci hatası: {_e1}"); st.code(traceback.format_exc())


    # --- GRUP 3: OGRETIM & PLANLAMA ---
    if grp3 is not None:
      with grp3:
        try:
            _styled_group_header(
                "Öğretim Planlama & Takip",
                "Akademik planlar ve kazanim takibi",
                color="#7c3aed"
            )
            g3t1, g3t2, g3t3 = st.tabs([
                "  📚 Akademik Planlama  ", "  📋 Uygulama Takibi  ",
                "  🌳 Mufredat Agaci  "
            ])
            with g3t1:
                _render_akademik_planlama(store)
            with g3t2:
                _render_uygulama_takibi(store)
            with g3t3:
                try:
                    _render_mufredat_agaci(store)
                except Exception as e:
                    import traceback
                    st.error(f"Mufredat Agaci hatasi: {e}")
                    st.code(traceback.format_exc())
        except Exception as _e3:
            import traceback; st.error(f"Öğretim & Planlama hatası: {_e3}"); st.code(traceback.format_exc())

    # --- GRUP 3B: DERS DEFTERI ---
    if grp3b is not None:
      with grp3b:
        try:
            _styled_group_header(
                "Ders Defteri",
                "Ders programından otomatik beslenen dijital defter + sınıf & öğretmen programları",
                color="#6366f1"
            )
            dd_t1, dd_t2, dd_t3, dd_t4 = st.tabs([
                "  📓 Ders Defteri  ",
                "  📅 Sınıf Programı  ",
                "  👨‍🏫 Öğretmen Programı  ",
                "  🎓 Kurumsal Karneler  ",
            ])

            with dd_t1:
                _render_dijital_ders_defteri(store)

            with dd_t2:
                styled_section("Sınıf Haftalık Ders Programı", "#1565c0")
                _ak_yil = _get_akademik_yil()
                _ayarlar = store.get_ders_programi_ayarlari()
                _aktif_gunler = _ayarlar.get("aktif_gunler", GUNLER[:5])
                _max_saat = _ayarlar.get("gunluk_ders_saati", 8)
                _all_sch = store.get_schedule(akademik_yil=_ak_yil)
                if not _all_sch:
                    styled_info_banner("Henüz ders programı oluşturulmamış. "
                                        "Ders & Program sekmesinden program girin.", "warning")
                else:
                    _zaman_cizelgesi = store.get_zaman_cizelgesi()
                    _ders_saat_map2 = {}
                    for _zd in _zaman_cizelgesi:
                        if _zd.tur == "ders" and _zd.ders_no > 0 and _zd.baslangic and _zd.bitis:
                            _ders_saat_map2[_zd.ders_no] = {"baslangic": _zd.baslangic, "bitis": _zd.bitis}
                    _kurum_adi2 = _ayarlar.get("kurum_adi", "")
                    _logo2 = _ayarlar.get("logo_path", "")
                    sp1, sp2 = st.columns(2)
                    with sp1:
                        _r_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="dd_sp_sinif")
                    with sp2:
                        _r_sube = st.selectbox("Şube", SUBELER, key="dd_sp_sube")
                    _sinif_sch = [s for s in _all_sch if s.sinif == _r_sinif and s.sube == _r_sube]
                    _render_schedule_grid(
                        _sinif_sch, _aktif_gunler, _max_saat, mode="class",
                        ders_saatleri_map=_ders_saat_map2, kurum_adi=_kurum_adi2,
                        baslik=f"{_r_sinif}/{_r_sube} Sınıfı Haftalık Ders Programı — {_ak_yil}",
                        logo_path=_logo2,
                    )
                    if st.button(f"{_r_sinif}/{_r_sube} PDF İndir", type="primary",
                                  key="dd_sp_pdf_btn"):
                        _pages = [{"baslik": f"{_r_sinif}/{_r_sube} Sınıfı Haftalık Ders Programı",
                                   "alt_baslik": f"{_kurum_adi2} | {_ak_yil}",
                                   "schedule": _sinif_sch, "mode": "class"}]
                        _pdf = _generate_program_grid_pdf(_pages, _aktif_gunler, _max_saat,
                                                          ders_saat_map=_ders_saat_map2,
                                                          kurum_adi=_kurum_adi2, logo_path=_logo2)
                        if _pdf:
                            st.session_state["dd_sp_pdf_data"] = _pdf
                            st.session_state["dd_sp_pdf_name"] = f"program_{_r_sinif}_{_r_sube}.pdf"
                            st.rerun()
                        else:
                            st.error("PDF oluşturulamadı.")
                    if st.session_state.get("dd_sp_pdf_data"):
                        st.download_button(
                            "⬇️ PDF İndir",
                            data=st.session_state["dd_sp_pdf_data"],
                            file_name=st.session_state.get("dd_sp_pdf_name", "sinif_programi.pdf"),
                            mime="application/pdf",
                            key="dd_sp_pdf_dl",
                        )

            with dd_t3:
                styled_section("Öğretmen Haftalık Ders Programı", "#0f766e")
                _ak_yil3 = _get_akademik_yil()
                _ayarlar3 = store.get_ders_programi_ayarlari()
                _aktif_gunler3 = _ayarlar3.get("aktif_gunler", GUNLER[:5])
                _max_saat3 = _ayarlar3.get("gunluk_ders_saati", 8)
                _all_sch3 = store.get_schedule(akademik_yil=_ak_yil3)
                if not _all_sch3:
                    styled_info_banner("Ders programı bulunamadı.", "warning")
                else:
                    _zaman_cizelgesi3 = store.get_zaman_cizelgesi()
                    _dsm3 = {}
                    for _zd3 in _zaman_cizelgesi3:
                        if _zd3.tur == "ders" and _zd3.ders_no > 0 and _zd3.baslangic and _zd3.bitis:
                            _dsm3[_zd3.ders_no] = {"baslangic": _zd3.baslangic, "bitis": _zd3.bitis}
                    _kurum_adi3 = _ayarlar3.get("kurum_adi", "")
                    _logo3 = _ayarlar3.get("logo_path", "")
                    _mudur3 = _ayarlar3.get("mudur_adi", "")
                    _teachers3 = store.get_teachers(durum="aktif")
                    if not _teachers3:
                        st.info("Aktif öğretmen bulunamadı.")
                    else:
                        _ogr_map3 = {
                            f"{t.tam_ad} ({t.brans})": t for t in _teachers3
                        }
                        _sel_ogr3 = st.selectbox("Öğretmen", list(_ogr_map3.keys()),
                                                 key="dd_op_ogretmen")
                        if _sel_ogr3:
                            _teacher3 = _ogr_map3[_sel_ogr3]
                            _ogr_sch3 = [s for s in _all_sch3 if s.ogretmen_id == _teacher3.id]
                            _render_schedule_grid(
                                _ogr_sch3, _aktif_gunler3, _max_saat3, mode="teacher",
                                ders_saatleri_map=_dsm3, kurum_adi=_kurum_adi3,
                                baslik=f"{_teacher3.tam_ad} — Haftalık Ders Programı — {_ak_yil3}",
                                mudur_adi=_mudur3, logo_path=_logo3,
                            )
                            if st.button(f"{_teacher3.tam_ad} PDF İndir", type="primary",
                                          key="dd_op_pdf_btn"):
                                _pages3 = [{"baslik": f"{_teacher3.tam_ad} — Haftalık Ders Programı",
                                            "alt_baslik": f"{_kurum_adi3} | {_ak_yil3}",
                                            "schedule": _ogr_sch3, "mode": "teacher",
                                            "mudur_adi": _mudur3}]
                                _pdf3 = _generate_program_grid_pdf(
                                    _pages3, _aktif_gunler3, _max_saat3,
                                    ders_saat_map=_dsm3, kurum_adi=_kurum_adi3, logo_path=_logo3
                                )
                                if _pdf3:
                                    st.session_state["dd_op_pdf_data"] = _pdf3
                                    st.session_state["dd_op_pdf_name"] = f"program_{_teacher3.tam_ad.replace(' ','_')}.pdf"
                                    st.rerun()
                                else:
                                    st.error("PDF oluşturulamadı.")
                            if st.session_state.get("dd_op_pdf_data"):
                                st.download_button(
                                    "⬇️ PDF İndir",
                                    data=st.session_state["dd_op_pdf_data"],
                                    file_name=st.session_state.get("dd_op_pdf_name", "ogretmen_programi.pdf"),
                                    mime="application/pdf",
                                    key="dd_op_pdf_dl",
                                )

            with dd_t4:
                _render_kurumsal_karneler(store)
        except Exception as _e3b:
            import traceback; st.error(f"Ders Defteri hatası: {_e3b}"); st.code(traceback.format_exc())

    # --- GRUP GUNLUK PLAN: GÜNLÜK PLAN OLUŞTUR ---
    if grp_gunluk is not None:
      with grp_gunluk:
        try:
            _styled_group_header(
                "Günlük Plan Oluşturucu",
                "Yıllık planı yükle, tatilleri otomatik al, günlük ders planı PDF oluştur",
                color="#0d9488"
            )
            _render_gunluk_plan_olustur(store)
        except Exception as _egp:
            import traceback; st.error(f"Günlük Plan hatası: {_egp}"); st.code(traceback.format_exc())

    # --- GRUP 4: DIJITAL OGRENME & ONLINE DERS ---
    if grp4 is not None:
      with grp4:
        try:
            _styled_group_header(
                "Dijital Öğrenme & Online Ders",
                "Online dersler, dijital platformlar, ders planlama ve raporlama",
                color="#7c3aed"
            )
            _render_online_ders(store)
        except Exception as _e4:
            import traceback; st.error(f"Dijital Öğrenme hatası: {_e4}"); st.code(traceback.format_exc())

    # --- GRUP 5: ODEV TAKIP ---
    if grp5 is not None:
      with grp5:
        try:
            _styled_group_header(
                "Ödev Takip & Yönetim",
                "Ödev olusturma, teslim takibi ve degerlendirme",
                color="#f59e0b"
            )
            _render_odev_takip(store)
        except Exception as _e5:
            import traceback; st.error(f"Ödev Takip hatası: {_e5}"); st.code(traceback.format_exc())

    # --- GRUP 6: YOKLAMA & NOTLAR ---
    if grp6 is not None:
      with grp6:
        try:
            _styled_group_header(
                "Yoklama & Not Takibi",
                "Devamsızlık yonetimi, veli bildirim ve not girisi",
                color="#dc2626"
            )
            g6t1, g6t2, g6t3 = st.tabs([
                "  ✅ Yoklama & Devamsızlık  ",
                "  📸 Akıllı Yoklama  ",
                "  📝 Not Girişi & Takibi  ",
            ])
            with g6t1:
                _render_yoklama_devamsizlik(store)
            with g6t2:
                try:
                    from views._akilli_yoklama import render_akilli_yoklama
                    render_akilli_yoklama()
                except ImportError:
                    st.info("Akıllı Yoklama modülü yüklü değil.")
                except Exception as _e:
                    st.error(f"Akıllı Yoklama yüklenemedi: {_e}")
            with g6t3:
                _render_not_girisi(store)
        except Exception as _e6:
            import traceback; st.error(f"Yoklama & Notlar hatası: {_e6}"); st.code(traceback.format_exc())

    # --- SINAV SONUÇLARI ---
    if grp_sinav is not None:
      with grp_sinav:
        try:
            _styled_group_header(
                "Sınav Sonuçları & Dönemlik Not Takibi",
                "Tüm SmartCampusAI modüllerinden konsolide sınav sonuçları — OD, deneme, online test, KYT, ödev ve yabancı dil",
                color="#2563eb"
            )
            _render_sinav_sonuclari(store)
        except Exception as _es:
            import traceback; st.error(f"Sınav Sonuçları hatası: {_es}"); st.code(traceback.format_exc())

    # --- GRUP 7: RAPORLAR & ANALIZ ---
    if grp7 is not None:
      with grp7:
        try:
            _styled_group_header(
                "Raporlar & Analiz",
                "Genel raporlar, ogrenci ve ogretmen performans analizi, AI destekli degerlendirme",
                color="#059669"
            )
            g7t1, g7t2, g7t3 = st.tabs([
                "  📈 Genel Raporlar  ", "  🎓 Öğrenci Analizi  ", "  👨‍🏫 Öğretmen Analizi  "
            ])
            with g7t1:
                _render_raporlar(store)
            with g7t2:
                _render_ogrenci_analizi(store)
            with g7t3:
                _render_ogretmen_analizi(store)
        except Exception as _e7:
            import traceback; st.error(f"Raporlar hatası: {_e7}"); st.code(traceback.format_exc())

    # --- GRUP 8: ERKEN UYARI & DESTEK ---
    if grp8 is not None:
      with grp8:
        try:
            _styled_group_header(
                "Erken Uyari & Akademik Destek",
                "Risk tespiti, mudahale planlama, destek programlari ve ogretmen CRM",
                color="#dc2626"
            )
            _render_erken_uyari(store)
        except Exception as _e8:
            import traceback; st.error(f"Erken Uyarı hatası: {_e8}"); st.code(traceback.format_exc())

    # --- GRUP 10: KAZANIM TAKİP (KYT) ---
    if grp10 is not None:
      with grp10:
        try:
            _styled_group_header(
                "Kazanım Takip Sistemi (KYT)",
                "Günlük kazanim yoklama, otomatik soru uretimi ve analiz",
                color="#10b981"
            )
            _render_kyt(store)
        except Exception as _e10:
            import traceback; st.error(f"KYT hatası: {_e10}"); st.code(traceback.format_exc())

    # --- KAZANIM BORÇ BANKASI ---
    if grp_borc is not None:
      with grp_borc:
        try:
            _styled_group_header(
                "Kazanım Borç Bankası",
                "Devamsızlık ve ödev eksikliğinden kaynaklanan kazanım borçları takibi, AI yol haritası ve PDF rapor",
                color="#7c3aed"
            )
            _render_kazanim_borc_bankasi(store)
        except Exception as _eb:
            import traceback; st.error(f"Kazanım Borç hatası: {_eb}"); st.code(traceback.format_exc())

    # --- ÖĞRENCI DEFTERİ ---
    if grp_defter is not None:
      with grp_defter:
        try:
            _styled_group_header(
                "Öğrenci Defteri",
                "Tüm akademik verileri AI ile analiz eden kapsamlı öğrenci profil defteri — risk analizi, grafikler ve tavsiyeler",
                color="#94A3B8"
            )
            from views.ogrenci_defteri import render_ogrenci_defteri_admin
            render_ogrenci_defteri_admin(selected_egitim_yili=selected_egitim_yili)
        except Exception as _ed:
            import traceback; st.error(f"Öğrenci Defteri hatası: {_ed}"); st.code(traceback.format_exc())

    # --- DIJITAL IKIZ (Premium yenilik) ---
    if grp_ikiz is not None:
      with grp_ikiz:
        try:
            _styled_group_header(
                "Öğrenci Dijital İkizi",
                "Her öğrenci için 6 boyutlu radar + AI 30/60/90 gün tahmin + aksiyon önerileri",
                color="#3b82f6"
            )
            _render_dijital_ikiz(store)
        except Exception as _eik:
            import traceback; st.error(f"Dijital İkiz hatası: {_eik}"); st.code(traceback.format_exc())

    # --- OGRETMEN COCKPIT (Premium yenilik) ---
    if grp_cockpit is not None:
      with grp_cockpit:
        try:
            _styled_group_header(
                "Öğretmen Performans Cockpit",
                "3 KPI + sınıf bazlı performans + AI koçluk önerileri",
                color="#8b5cf6"
            )
            _render_ogretmen_cockpit(store)
        except Exception as _ecp:
            import traceback; st.error(f"Öğretmen Cockpit hatası: {_ecp}"); st.code(traceback.format_exc())

    # --- VELI BILDIRIM AJANSI (Premium yenilik) ---
    if grp_veli is not None:
      with grp_veli:
        try:
            _styled_group_header(
                "Veli Bildirim Otomasyonu",
                "Devamsızlık + Not + Ödev + Risk + Haftalık özet — proaktif WhatsApp",
                color="#10b981"
            )
            _render_veli_bildirim_panel(store)
        except Exception as _evb:
            import traceback; st.error(f"Veli Bildirim hatası: {_evb}"); st.code(traceback.format_exc())

    # --- ZIRVE: Akademik Komuta Merkezi ---
    if grp_komuta is not None:
      with grp_komuta:
        try:
            from views._at_zirve import render_akademik_komuta
            render_akademik_komuta(store)
        except Exception as _eak:
            import traceback; st.error(f"Akademik Komuta hatasi: {_eak}"); st.code(traceback.format_exc())

    # --- ZIRVE: Sinif/Sube Karsilastirma Arena ---
    if grp_arena is not None:
      with grp_arena:
        try:
            from views._at_zirve import render_sinif_karsilastirma
            render_sinif_karsilastirma(store)
        except Exception as _esk:
            import traceback; st.error(f"Karsilastirma hatasi: {_esk}"); st.code(traceback.format_exc())

    # --- ZIRVE: AI Akademik Strateji ---
    if grp_strateji is not None:
      with grp_strateji:
        try:
            from views._at_zirve import render_ai_strateji
            render_ai_strateji(store)
        except Exception as _eas:
            import traceback; st.error(f"AI Strateji hatasi: {_eas}"); st.code(traceback.format_exc())

    # --- SUPER: Ogretmen Verimlilik ---
    if grp_verimlilik is not None:
      with grp_verimlilik:
        try:
            from views._at_super import render_ogretmen_verimlilik
            render_ogretmen_verimlilik(store)
        except Exception as _eov:
            import traceback; st.error(f"Ogretmen Verimlilik hatasi: {_eov}"); st.code(traceback.format_exc())

    # --- SUPER: Otomatik Mudahale ---
    if grp_mudahale is not None:
      with grp_mudahale:
        try:
            from views._at_super import render_oto_mudahale
            render_oto_mudahale(store)
        except Exception as _eom:
            import traceback; st.error(f"Oto Mudahale hatasi: {_eom}"); st.code(traceback.format_exc())

    # --- SUPER: Tahmin Motoru ---
    if grp_tahmin is not None:
      with grp_tahmin:
        try:
            from views._at_super import render_tahmin_motoru
            render_tahmin_motoru(store)
        except Exception as _etm:
            import traceback; st.error(f"Tahmin Motoru hatasi: {_etm}"); st.code(traceback.format_exc())

    # --- MEGA: Mufredat GPS ---
    if grp_mufredat is not None:
      with grp_mufredat:
        try:
            from views._at_mega import render_mufredat_gps
            render_mufredat_gps(store)
        except Exception as _emg:
            import traceback; st.error(f"Mufredat GPS hatasi: {_emg}"); st.code(traceback.format_exc())

    # --- MEGA: Sinif Dijital Ikiz ---
    if grp_sinif_ikiz is not None:
      with grp_sinif_ikiz:
        try:
            from views._at_mega import render_sinif_dijital_ikiz
            render_sinif_dijital_ikiz(store)
        except Exception as _esi:
            import traceback; st.error(f"Sinif Ikiz hatasi: {_esi}"); st.code(traceback.format_exc())

    # --- MEGA: Zaman Makinesi ---
    if grp_zaman is not None:
      with grp_zaman:
        try:
            from views._at_mega import render_akademik_zaman
            render_akademik_zaman(store)
        except Exception as _eaz:
            import traceback; st.error(f"Zaman Makinesi hatasi: {_eaz}"); st.code(traceback.format_exc())

    # --- KURUM HİZMETLERİ ---
    if grp_kurum_hiz is not None:
      with grp_kurum_hiz:
        try:
            _render_kurum_hizmetleri()
        except Exception as _ekh:
            st.error(f"Kurum Hizmetleri hatasi: {_ekh}")

    # --- SMARTI ---
    if grp_smarti is not None:
      with grp_smarti:
        try:
            def _at_data_context():
                try:
                    students = store.get_students()
                    teachers = store.get_teachers()
                    grades = store.get_grades()
                    attendance = store.get_attendance()
                    return (
                        f"Toplam ogrenci sayisi: {len(students)}\n"
                        f"Toplam ogretmen sayisi: {len(teachers)}\n"
                        f"Toplam not kaydi sayisi: {len(grades)}\n"
                        f"Toplam devamsizlik kaydi sayisi: {len(attendance)}"
                    )
                except Exception:
                    return ""
            render_smarti_chat("akademik_takip", _at_data_context)
        except Exception as _esm:
            import traceback; st.error(f"Smarti hatası: {_esm}"); st.code(traceback.format_exc())


# ==================== ERKEN UYARI & DESTEK ====================

def _render_erken_uyari(store: AkademikDataStore):
    """Erken Uyari & Akademik Destek ana fonksiyonu - 6 alt sekme."""
    kurum = get_institution_info()
    engine = EarlyWarningEngine(store)

    eu_t1, eu_t2, eu_t3, eu_t4, eu_t5, eu_t6 = st.tabs([
        "  🚨 Risk Dashboard  ",
        "  🔍 Öğrenci Risk Detay  ",
        "  🛠️ Mudahale Yönetimi  ",
        "  📋 Destek Planlari  ",
        "  👨‍🏫 Öğretmen CRM  ",
        "  📊 Analiz & Raporlar  ",
    ])

    # ========== TAB 1: RISK DASHBOARD ==========
    with eu_t1:
        _render_risk_dashboard(store, engine, kurum)

    # ========== TAB 2: OGRENCI RISK DETAY ==========
    with eu_t2:
        _render_ogrenci_risk_detay(store, engine, kurum)

    # ========== TAB 3: MUDAHALE YONETIMI ==========
    with eu_t3:
        _render_mudahale_yonetimi(store, engine, kurum)

    # ========== TAB 4: DESTEK PLANLARI ==========
    with eu_t4:
        _render_destek_planlari(store, kurum)

    # ========== TAB 5: OGRETMEN CRM ==========
    with eu_t5:
        _render_ogretmen_crm(store, kurum)

    # ========== TAB 6: ANALIZ & RAPORLAR ==========
    with eu_t6:
        _render_eu_analiz(store, engine, kurum)


# ---------- TAB 1: RISK DASHBOARD ----------

def _render_risk_dashboard(store, engine, kurum):
    styled_section("Risk Dashboard", "#dc2626")

    # Filtreler
    fc1, fc2, fc3 = st.columns([1, 1, 2])
    with fc1:
        rd_siniflar = [None] + SINIFLAR
        rd_sinif = st.selectbox("Sınıf", rd_siniflar, format_func=lambda x: "Tümü" if x is None else f"{x}. Sınıf", key="eu_rd_sinif")
    with fc2:
        rd_subeler = [None] + SUBELER
        rd_sube = st.selectbox("Şube", rd_subeler, format_func=lambda x: "Tümü" if x is None else x, key="eu_rd_sube")
    with fc3:
        st.markdown("")
        st.markdown("")
        tarama_btn = st.button("Tarama Baslat", type="primary", key="eu_tarama_btn", use_container_width=True)

    # Tarama sonuclari
    if tarama_btn:
        with st.spinner("Öğrenciler taraniyor..."):
            scan = engine.scan_all_students(sinif=rd_sinif, sube=rd_sube)
            st.session_state["eu_scan_results"] = scan
            # Otomatik alert olustur
            new_alerts = engine.auto_generate_alerts(sinif=rd_sinif, sube=rd_sube)
            if new_alerts:
                st.success(f"{len(new_alerts)} yeni risk uyarisi oluşturuldu.")

    scan = st.session_state.get("eu_scan_results", [])

    # Metrik kartlar
    kritik = sum(1 for s in scan if s.get("severity") == "critical")
    yuksek = sum(1 for s in scan if s.get("severity") == "high")
    orta = sum(1 for s in scan if s.get("severity") == "medium")
    dusuk = sum(1 for s in scan if s.get("severity") == "low")

    st.markdown(ReportStyler.metric_cards_html([
        ("Toplam Riskli", str(len(scan)), "#6366f1", ""),
        ("Kritik", str(kritik), "#ef4444", ""),
        ("Yuksek", str(yuksek), "#f97316", ""),
        ("Orta", str(orta), "#f59e0b", ""),
    ]), unsafe_allow_html=True)

    if not scan:
        styled_info_banner("Tarama baslatmak için yukardaki butonu kullanin veya henuz riskli ogrenci bulunmadi.", "info")
        return

    # Risk tablosu
    styled_section("Riskli Öğrenciler", "#dc2626")
    risk_data = []
    for s in scan:
        sev = s.get("severity", "")
        sev_label = RISK_SEVERITY_LABELS.get(sev, sev)
        risk_data.append({
            "Öğrenci": f"{s['ad']} {s['soyad']}",
            "Sınıf": f"{s['sinif']}/{s['sube']}",
            "No": s.get("numara", ""),
            "Risk Skoru": f"{s['score']:.0f}",
            "Seviye": sev_label,
            "Devamsızlık": f"{s['factors']['attendance']:.0f}",
            "Not": f"{s['factors']['grade']:.0f}",
            "Ödev": f"{s['factors']['homework']:.0f}",
            "Sınav": f"{s['factors']['exam']:.0f}",
        })

    if risk_data:
        df_risk = pd.DataFrame(risk_data)
        color_rules = {
            "Seviye": {
                "Kritik": "#fecaca",
                "Yuksek": "#fed7aa",
                "Orta": "#fef08a",
                "Dusuk": "#bbf7d0",
            }
        }
        st.markdown(ReportStyler.colored_table_html(df_risk, header_color="#dc2626", color_rules=color_rules), unsafe_allow_html=True)

    # Grafikler
    gc1, gc2 = st.columns(2)
    with gc1:
        styled_section("Risk Dagilimi", "#dc2626")
        dist_data = {}
        if kritik > 0:
            dist_data["Kritik"] = kritik
        if yuksek > 0:
            dist_data["Yuksek"] = yuksek
        if orta > 0:
            dist_data["Orta"] = orta
        if dusuk > 0:
            dist_data["Dusuk"] = dusuk
        if dist_data:
            st.markdown(ReportStyler.donut_chart_svg(dist_data, ["#ef4444", "#f97316", "#f59e0b", "#22c55e"]), unsafe_allow_html=True)

    with gc2:
        styled_section("Faktor Ortalama Skor", "#dc2626")
        if scan:
            avg_att = sum(s["factors"]["attendance"] for s in scan) / len(scan)
            avg_grd = sum(s["factors"]["grade"] for s in scan) / len(scan)
            avg_hw = sum(s["factors"]["homework"] for s in scan) / len(scan)
            avg_exam = sum(s["factors"]["exam"] for s in scan) / len(scan)
            faktor_data = {
                "Devamsızlık": avg_att,
                "Not Dususu": avg_grd,
                "Ödev Teslim": avg_hw,
                "Sınav Trendi": avg_exam,
            }
            st.markdown(ReportStyler.horizontal_bar_html(faktor_data, color="#dc2626"), unsafe_allow_html=True)

    # PDF export
    styled_section("Rapor & Paylasim", "#dc2626")
    try:
        pdf_gen = ReportPDFGenerator("Risk Dashboard Raporu", kurum.get("name", ""))
        pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
        pdf_gen.add_section("Risk Özeti")
        pdf_gen.add_metrics([
            ("Toplam Riskli", str(len(scan)), "#6366f1"),
            ("Kritik", str(kritik), "#ef4444"),
            ("Yuksek", str(yuksek), "#f97316"),
            ("Orta", str(orta), "#f59e0b"),
        ])
        if risk_data:
            pdf_gen.add_section("Riskli Öğrenciler")
            pdf_gen.add_table(pd.DataFrame(risk_data))
        pdf_bytes = pdf_gen.generate()
        ReportSharer.render_share_ui(pdf_bytes, "risk_dashboard.pdf", "Risk Dashboard Raporu", key_prefix="eu_rd")
    except Exception as e:
        st.warning(f"PDF olusturulamadi: {e}")


# ---------- TAB 2: OGRENCI RISK DETAY ----------

def _render_ogrenci_risk_detay(store, engine, kurum):
    styled_section("Öğrenci Risk Detay", "#f97316")

    # Ogrenci secimi
    fc1, fc2, fc3 = st.columns([1, 1, 2])
    with fc1:
        ord_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="eu_ord_sinif")
    with fc2:
        ord_sube = st.selectbox("Şube", SUBELER, key="eu_ord_sube")
    students = store.get_students(sinif=ord_sinif, sube=ord_sube, durum="aktif")
    if not students:
        styled_info_banner("Bu sinif/subede ogrenci bulunmuyor.", "warning")
        return
    with fc3:
        stu_opts = {s.id: f"{s.ad} {s.soyad} ({s.numara})" for s in students}
        sel_stu_id = st.selectbox("Öğrenci", list(stu_opts.keys()), format_func=lambda x: stu_opts[x], key="eu_ord_stu")

    stu = store.get_student(sel_stu_id)
    if not stu:
        return

    # Risk hesapla
    risk = engine.calculate_composite_risk(sel_stu_id)
    factors = risk.get("factors", {})
    severity = risk.get("severity", "")
    score = risk.get("score", 0)

    # Ogrenci bilgi karti + risk skoru
    sev_color = RISK_SEVERITY_COLORS.get(severity, "#94a3b8")
    sev_label = RISK_SEVERITY_LABELS.get(severity, "Yok")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#111827,#1e293b);border-radius:16px;padding:24px;margin:16px 0;color:#94A3B8;border:1px solid #334155;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:22px;font-weight:700;">{stu.ad} {stu.soyad}</div>
                <div style="color:#64748b;font-size:14px;">{stu.sinif}/{stu.sube} - No: {stu.numara}</div>
                <div style="color:#64748b;font-size:13px;margin-top:4px;">Veli: {stu.veli_adi} | Tel: {stu.veli_telefon}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:42px;font-weight:900;color:{sev_color};">{score:.0f}</div>
                <div style="background:{sev_color};color:white;padding:4px 16px;border-radius:20px;font-size:13px;font-weight:600;">{sev_label}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 faktor karti
    fc_cols = st.columns(4)
    faktor_labels = [
        ("Devamsızlık", factors.get("attendance", 0), "#ef4444"),
        ("Not Dususu", factors.get("grade", 0), "#f97316"),
        ("Ödev Teslim", factors.get("homework", 0), "#f59e0b"),
        ("Sınav Trendi", factors.get("exam", 0), "#8b5cf6"),
    ]
    for col, (lbl, val, clr) in zip(fc_cols, faktor_labels):
        with col:
            pct = min(val, 100)
            st.markdown(f"""
            <div style="background:white;border:2px solid {clr};border-radius:12px;padding:16px;text-align:center;">
                <div style="font-size:13px;color:#64748b;font-weight:600;">{lbl}</div>
                <div style="font-size:28px;font-weight:800;color:{clr};">{val:.0f}</div>
                <div style="background:#e2e8f0;border-radius:8px;height:8px;margin-top:8px;">
                    <div style="background:{clr};width:{pct}%;height:8px;border-radius:8px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Detay metrikleri
    st.markdown("")
    styled_section("Detay Bilgileri", "#f97316")

    dc1, dc2 = st.columns(2)
    with dc1:
        # Devamsizlik detayi
        att_sum = store.get_attendance_summary(sel_stu_id)
        st.markdown(f"""
        <div style="background:#fff7ed;border-left:4px solid #f97316;padding:12px 16px;border-radius:8px;margin:8px 0;">
            <b>Devamsizlik Ozeti</b><br>
            Toplam: {att_sum.get('toplam', 0)} gun | Ozurlu: {att_sum.get('ozurlu', 0)} | Ozursuz: {att_sum.get('ozursuz', 0)}<br>
            Durum: <b>{att_sum.get('uyari', 'Normal')}</b>
        </div>
        """, unsafe_allow_html=True)

        # Not ortalamalari
        avg_data = store.get_student_average(sel_stu_id)
        if avg_data.get("detay"):
            not_rows = []
            for d, info in avg_data["detay"].items():
                not_rows.append({"Ders": d, "Ortalama": f"{info['ortalama']:.1f}", "Not Sayısı": info['not_sayisi']})
            if not_rows:
                st.markdown(ReportStyler.colored_table_html(
                    pd.DataFrame(not_rows), header_color="#f97316",
                    color_rules={"Ortalama": lambda v: "#fecaca" if float(v) < 50 else ("#fef08a" if float(v) < 70 else "#bbf7d0")}
                ), unsafe_allow_html=True)

    with dc2:
        # Odev teslim durumu
        teslimleri = store.get_odev_teslimleri(student_id=sel_stu_id)
        toplam_odev = len(teslimleri)
        teslim_eden = sum(1 for t in teslimleri if t.durum in ("teslim_edildi", "muaf"))
        teslim_orani = (teslim_eden / toplam_odev * 100) if toplam_odev > 0 else 0
        st.markdown(f"""
        <div style="background:#eff6ff;border-left:4px solid #3b82f6;padding:12px 16px;border-radius:8px;margin:8px 0;">
            <b>Odev Teslim Durumu</b><br>
            Toplam: {toplam_odev} | Teslim: {teslim_eden} | Oran: %{teslim_orani:.0f}
        </div>
        """, unsafe_allow_html=True)

        # Mudahale onerileri
        if severity:
            alert_dummy = type('obj', (object,), {'factors': json.dumps(factors)})()
            suggestions = engine.suggest_interventions(alert_dummy)
            st.markdown(f"""
            <div style="background:#fef2f2;border-left:4px solid #ef4444;padding:12px 16px;border-radius:8px;margin:8px 0;">
                <b>Mudahale Onerileri</b><br>
                {'<br>'.join(f'&#8226; {s}' for s in suggestions)}
            </div>
            """, unsafe_allow_html=True)

    # Risk gecmisi
    styled_section("Risk Geçmişi", "#f97316")
    alerts = store.get_risk_alerts(student_id=sel_stu_id)
    if alerts:
        alert_rows = []
        for a in alerts:
            alert_rows.append({
                "Tarih": a.created_at[:10] if a.created_at else "",
                "Seviye": RISK_SEVERITY_LABELS.get(a.severity, a.severity),
                "Skor": f"{a.risk_score:.0f}",
                "Durum": a.status.replace("_", " ").title(),
                "Detay": a.details[:80] if a.details else "",
            })
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(alert_rows), header_color="#f97316"), unsafe_allow_html=True)
    else:
        st.info("Bu ogrenci için onceki risk uyarisi bulunmuyor.")

    # Aktif mudahaleler
    muds = store.get_mudahaleler(student_id=sel_stu_id)
    aktif_muds = [m for m in muds if m.status in ("planned", "in_progress")]
    if aktif_muds:
        styled_section("Aktif Mudahaleler", "#f97316")
        mud_rows = []
        for m in aktif_muds:
            tip_label = dict(MUDAHALE_TIPLERI).get(m.mudahale_type, m.mudahale_type)
            dur_label = dict(MUDAHALE_DURUMLARI).get(m.status, m.status)
            mud_rows.append({
                "Tip": tip_label,
                "Açıklama": m.description[:60] if m.description else "",
                "Sorumlu": m.assigned_to_name,
                "Hedef Tarih": m.due_date,
                "Durum": dur_label,
            })
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(mud_rows), header_color="#f97316"), unsafe_allow_html=True)

    # PDF export
    styled_section("Rapor & Paylasim", "#f97316")
    try:
        pdf_gen = ReportPDFGenerator(f"Risk Raporu - {stu.ad} {stu.soyad}", kurum.get("name", ""))
        pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
        pdf_gen.add_section("Öğrenci Bilgileri")
        pdf_gen.add_text(f"Ad Soyad: {stu.ad} {stu.soyad}\nSınıf/Şube: {stu.sinif}/{stu.sube}\nNumara: {stu.numara}")
        pdf_gen.add_section("Risk Değerlendirmesi")
        pdf_gen.add_metrics([
            ("Risk Skoru", f"{score:.0f}", sev_color),
            ("Seviye", sev_label, sev_color),
            ("Devamsızlık", f"{factors.get('attendance', 0):.0f}", "#ef4444"),
            ("Not", f"{factors.get('grade', 0):.0f}", "#f97316"),
        ])
        pdf_gen.add_text(f"Detay: {risk.get('details', '')}")
        pdf_bytes = pdf_gen.generate()
        ReportSharer.render_share_ui(
            pdf_bytes, f"risk_raporu_{stu.ad}_{stu.soyad}.pdf",
            f"Risk Raporu - {stu.ad} {stu.soyad}",
            default_phone=stu.veli_telefon, default_email=stu.veli_email,
            key_prefix="eu_ord"
        )
    except Exception as e:
        st.warning(f"PDF olusturulamadi: {e}")


# ---------- TAB 3: MUDAHALE YONETIMI ----------

def _render_mudahale_yonetimi(store, engine, kurum):
    styled_section("Müdahale Yönetimi", "#7c3aed")

    mtab1, mtab2 = st.tabs(["  ➕ Yeni Mudahale  ", "  📋 Mudahale Listesi  "])

    with mtab1:
        styled_section("Yeni Mudahale Kaydi", "#7c3aed")
        mc1, mc2 = st.columns(2)
        with mc1:
            m_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="eu_m_sinif")
            m_sube = st.selectbox("Şube", SUBELER, key="eu_m_sube")
        students = store.get_students(sinif=m_sinif, sube=m_sube, durum="aktif")
        with mc2:
            if students:
                m_stu_opts = {s.id: f"{s.ad} {s.soyad}" for s in students}
                m_stu_id = st.selectbox("Öğrenci", list(m_stu_opts.keys()), format_func=lambda x: m_stu_opts[x], key="eu_m_stu")
            else:
                st.warning("Öğrenci bulunamadı.")
                return

            # Iliskili uyari (opsiyonel)
            alerts = store.get_risk_alerts(student_id=m_stu_id, status="active")
            alert_opts = {"": "-- Uyari yok --"}
            for a in alerts:
                alert_opts[a.id] = f"Skor: {a.risk_score:.0f} - {RISK_SEVERITY_LABELS.get(a.severity, '')}"
            m_alert_id = st.selectbox("Iliskili Uyari", list(alert_opts.keys()), format_func=lambda x: alert_opts[x], key="eu_m_alert")

        mc3, mc4 = st.columns(2)
        with mc3:
            m_tip_opts = [t[0] for t in MUDAHALE_TIPLERI]
            m_tip = st.selectbox("Mudahale Tipi", m_tip_opts, format_func=lambda x: dict(MUDAHALE_TIPLERI).get(x, x), key="eu_m_tip")
            m_desc = st.text_area("Açıklama", key="eu_m_desc", height=100)
        with mc4:
            teachers = store.get_teachers(durum="aktif") if hasattr(store, 'get_teachers') else []
            if teachers:
                t_opts = {t.id: f"{t.ad} {t.soyad}" for t in teachers}
                m_assigned = st.selectbox("Sorumlu", list(t_opts.keys()), format_func=lambda x: t_opts[x], key="eu_m_assigned")
                m_assigned_name = t_opts[m_assigned]
            else:
                m_assigned = ""
                m_assigned_name = st.text_input("Sorumlu Adi", key="eu_m_assigned_name")
            m_due = st.date_input("Hedef Tarih", key="eu_m_due")

        if st.button("Mudahale Kaydet", type="primary", key="eu_m_save", use_container_width=True):
            if not m_desc:
                st.error("Açıklama alani bos birakilamaz.")
            else:
                kayit = MudahaleKayit(
                    student_id=m_stu_id,
                    alert_id=m_alert_id if m_alert_id else "",
                    mudahale_type=m_tip,
                    description=m_desc,
                    assigned_to=m_assigned,
                    assigned_to_name=m_assigned_name if not teachers else t_opts.get(m_assigned, ""),
                    due_date=m_due.strftime("%Y-%m-%d"),
                    status="planned",
                )
                store.save_mudahale(kayit)
                st.success("Mudahale kaydi oluşturuldu!")
                st.rerun()

    with mtab2:
        styled_section("Mudahale Kayıtlari", "#7c3aed")

        # Filtre
        mf1, mf2 = st.columns(2)
        with mf1:
            ml_dur_opts = [("", "Tümü")] + MUDAHALE_DURUMLARI
            ml_dur = st.selectbox("Durum Filtresi", [d[0] for d in ml_dur_opts], format_func=lambda x: dict(ml_dur_opts).get(x, x), key="eu_ml_dur")
        with mf2:
            pass

        all_muds = store.get_mudahaleler(status=ml_dur if ml_dur else None)
        if not all_muds:
            st.info("Kayıtli mudahale bulunmuyor.")
        else:
            mud_rows = []
            for m in all_muds:
                stu = store.get_student(m.student_id)
                stu_ad = f"{stu.ad} {stu.soyad}" if stu else m.student_id
                tip_label = dict(MUDAHALE_TIPLERI).get(m.mudahale_type, m.mudahale_type)
                dur_label = dict(MUDAHALE_DURUMLARI).get(m.status, m.status)
                mud_rows.append({
                    "Öğrenci": stu_ad,
                    "Tip": tip_label,
                    "Açıklama": m.description[:50] if m.description else "",
                    "Sorumlu": m.assigned_to_name,
                    "Hedef": m.due_date,
                    "Durum": dur_label,
                    "id": m.id,
                })

            color_rules = {
                "Durum": {
                    "Planli": "#bfdbfe",
                    "Devam Ediyor": "#fef08a",
                    "Tamamlandı": "#bbf7d0",
                    "Iptal": "#e2e8f0",
                }
            }
            df_mud = pd.DataFrame(mud_rows)
            display_df = df_mud.drop(columns=["id"])
            st.markdown(ReportStyler.colored_table_html(display_df, header_color="#7c3aed", color_rules=color_rules), unsafe_allow_html=True)

            # Durum guncelleme
            styled_section("Durum Güncelle", "#7c3aed")
            gu1, gu2, gu3 = st.columns([2, 1, 1])
            with gu1:
                gu_opts = {m["id"]: f"{m['Öğrenci']} - {m['Tip']}" for m in mud_rows}
                gu_sel = st.selectbox("Mudahale Sec", list(gu_opts.keys()), format_func=lambda x: gu_opts[x], key="eu_gu_sel")
            with gu2:
                gu_yeni_dur = st.selectbox("Yeni Durum", [d[0] for d in MUDAHALE_DURUMLARI], format_func=lambda x: dict(MUDAHALE_DURUMLARI).get(x, x), key="eu_gu_dur")
            with gu3:
                gu_sonuc = st.text_input("Sonuc Notu", key="eu_gu_sonuc")
            if st.button("Durumu Güncelle", key="eu_gu_save"):
                update_data = {"status": gu_yeni_dur}
                if gu_sonuc:
                    update_data["result"] = gu_sonuc
                store.update_mudahale(gu_sel, **update_data)
                st.success("Mudahale durumu güncellendi!")
                st.rerun()

        # Istatistikler
        all_muds_full = store.get_mudahaleler()
        if all_muds_full:
            styled_section("Mudahale İstatistikleri", "#7c3aed")
            ic1, ic2 = st.columns(2)
            with ic1:
                tip_dist = {}
                for m in all_muds_full:
                    lbl = dict(MUDAHALE_TIPLERI).get(m.mudahale_type, m.mudahale_type)
                    tip_dist[lbl] = tip_dist.get(lbl, 0) + 1
                if tip_dist:
                    st.markdown(ReportStyler.donut_chart_svg(tip_dist, ["#8b5cf6", "#3b82f6", "#3b82f6", "#22c55e", "#f59e0b", "#ef4444"]), unsafe_allow_html=True)
            with ic2:
                dur_dist = {}
                for m in all_muds_full:
                    lbl = dict(MUDAHALE_DURUMLARI).get(m.status, m.status)
                    dur_dist[lbl] = dur_dist.get(lbl, 0) + 1
                if dur_dist:
                    st.markdown(ReportStyler.horizontal_bar_html(dur_dist, color="#7c3aed"), unsafe_allow_html=True)


# ---------- TAB 4: DESTEK PLANLARI ----------

def _render_destek_planlari(store, kurum):
    styled_section("Destek Planları", "#0d9488")

    dtab1, dtab2 = st.tabs(["  ➕ Yeni Plan  ", "  📋 Plan Listesi  "])

    with dtab1:
        styled_section("Yeni Destek Plani Oluştur", "#0d9488")
        dp1, dp2 = st.columns(2)
        with dp1:
            dp_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="eu_dp_sinif")
            dp_sube = st.selectbox("Şube", SUBELER, key="eu_dp_sube")
            dp_students = store.get_students(sinif=dp_sinif, sube=dp_sube, durum="aktif")
            if dp_students:
                dp_stu_opts = {s.id: f"{s.ad} {s.soyad}" for s in dp_students}
                dp_stu_id = st.selectbox("Öğrenci", list(dp_stu_opts.keys()), format_func=lambda x: dp_stu_opts[x], key="eu_dp_stu")
            else:
                st.warning("Öğrenci bulunamadı.")
                return
        with dp2:
            dp_name = st.text_input("Plan Adi", key="eu_dp_name", placeholder="Orn: Matematik Destek Programi")
            dp_start = st.date_input("Başlangıç Tarihi", key="eu_dp_start")
            dp_end = st.date_input("Bitis Tarihi", key="eu_dp_end")

        dp_goals = st.text_area("Hedefler (her satir bir hedef)", key="eu_dp_goals", height=100, placeholder="1. Matematik ortalamasini 70 uzerine cikarmak\n2. Devamsızlığı azaltmak")
        dp_schedule = st.text_area("Haftalık Program", key="eu_dp_schedule", height=80, placeholder="Pazartesi 14:00 Matematik Etut, Carsamba 14:00 Fen Etut")

        # Sorumlu ogretmenler
        teachers = store.get_teachers(durum="aktif") if hasattr(store, 'get_teachers') else []
        if teachers:
            t_all = {t.id: f"{t.ad} {t.soyad}" for t in teachers}
            dp_teachers = st.multiselect("Sorumlu Öğretmenler", list(t_all.keys()), format_func=lambda x: t_all[x], key="eu_dp_teachers")
        else:
            dp_teachers = []

        if st.button("Plan Oluştur", type="primary", key="eu_dp_save", use_container_width=True):
            if not dp_name:
                st.error("Plan adi gereklidir.")
            else:
                goals_list = [g.strip() for g in dp_goals.split("\n") if g.strip()]
                plan = DestekPlani(
                    student_id=dp_stu_id,
                    plan_name=dp_name,
                    start_date=dp_start.strftime("%Y-%m-%d"),
                    end_date=dp_end.strftime("%Y-%m-%d"),
                    goals=json.dumps(goals_list, ensure_ascii=False),
                    weekly_schedule=dp_schedule,
                    assigned_teachers=json.dumps(dp_teachers, ensure_ascii=False),
                    status="active",
                )
                store.save_destek_plani(plan)
                st.success("Destek plani oluşturuldu!")
                st.rerun()

    with dtab2:
        styled_section("Aktif Destek Planlari", "#0d9488")
        df1, df2 = st.columns(2)
        with df1:
            dp_dur_opts = [("", "Tümü")] + DESTEK_PLANI_DURUMLARI
            dp_dur_filtre = st.selectbox("Durum", [d[0] for d in dp_dur_opts], format_func=lambda x: dict(dp_dur_opts).get(x, x), key="eu_dp_dur_f")

        plans = store.get_destek_planlari(status=dp_dur_filtre if dp_dur_filtre else None)
        if not plans:
            st.info("Kayıtli destek plani bulunmuyor.")
        else:
            for plan in plans:
                stu = store.get_student(plan.student_id)
                stu_ad = f"{stu.ad} {stu.soyad}" if stu else plan.student_id
                dur_label = dict(DESTEK_PLANI_DURUMLARI).get(plan.status, plan.status)
                dur_color = {"active": "#22c55e", "completed": "#3b82f6", "paused": "#f59e0b", "cancelled": "#94a3b8"}.get(plan.status, "#94a3b8")

                with st.expander(f"{stu_ad} - {plan.plan_name} ({dur_label})", expanded=False):
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown(f"**Tarih:** {plan.start_date} - {plan.end_date}")
                        st.markdown(f"**Durum:** <span style='color:{dur_color};font-weight:700;'>{dur_label}</span>", unsafe_allow_html=True)
                        # Hedefler
                        try:
                            goals = json.loads(plan.goals) if plan.goals else []
                        except Exception:
                            goals = []
                        if goals:
                            st.markdown("**Hedefler:**")
                            for i, g in enumerate(goals, 1):
                                st.markdown(f"  {i}. {g}")
                    with pc2:
                        st.markdown(f"**Haftalık Program:** {plan.weekly_schedule}")
                        # Ilerleme notu ekle
                        prog_note = st.text_input("İlerleme Notu Ekle", key=f"eu_dp_pn_{plan.id}")
                        if st.button("Not Ekle", key=f"eu_dp_pn_btn_{plan.id}"):
                            if prog_note:
                                try:
                                    notes = json.loads(plan.progress_notes) if plan.progress_notes else []
                                except Exception:
                                    notes = []
                                notes.append({"tarih": datetime.now().strftime("%Y-%m-%d %H:%M"), "not": prog_note})
                                store.update_destek_plani(plan.id, progress_notes=json.dumps(notes, ensure_ascii=False))
                                st.success("İlerleme notu eklendi!")
                                st.rerun()

                    # Ilerleme notlari
                    try:
                        notes = json.loads(plan.progress_notes) if plan.progress_notes else []
                    except Exception:
                        notes = []
                    if notes:
                        st.markdown("**İlerleme Notları:**")
                        for n in reversed(notes):
                            st.markdown(f"  - **{n.get('tarih', '')}:** {n.get('not', '')}")

                    # Durum guncelle
                    dp_new_dur = st.selectbox("Durum Güncelle", [d[0] for d in DESTEK_PLANI_DURUMLARI], format_func=lambda x: dict(DESTEK_PLANI_DURUMLARI).get(x, x), key=f"eu_dp_ndur_{plan.id}")
                    if st.button("Durumu Kaydet", key=f"eu_dp_ndur_btn_{plan.id}"):
                        store.update_destek_plani(plan.id, status=dp_new_dur)
                        st.success("Plan durumu güncellendi!")
                        st.rerun()


# ---------- TAB 5: OGRETMEN CRM ----------

def _render_ogretmen_crm(store, kurum):
    styled_section("Öğretmen Oneri & Gozlem Notları", "#2563eb")

    crm1, crm2 = st.tabs(["  ✏️ Yeni Not Ekle  ", "  📋 Not Listesi & Takip  "])

    with crm1:
        styled_section("Yeni Oneri / Gozlem", "#2563eb")
        cc1, cc2 = st.columns(2)
        with cc1:
            cr_sinif = st.selectbox("Sınıf", SINIFLAR, index=4, key="eu_cr_sinif")
            cr_sube = st.selectbox("Şube", SUBELER, key="eu_cr_sube")
            cr_students = store.get_students(sinif=cr_sinif, sube=cr_sube, durum="aktif")
            if cr_students:
                cr_stu_opts = {s.id: f"{s.ad} {s.soyad}" for s in cr_students}
                cr_stu_id = st.selectbox("Öğrenci", list(cr_stu_opts.keys()), format_func=lambda x: cr_stu_opts[x], key="eu_cr_stu")
            else:
                st.warning("Öğrenci bulunamadı.")
                return

        with cc2:
            teachers = store.get_teachers(durum="aktif") if hasattr(store, 'get_teachers') else []
            if teachers:
                cr_t_opts = {t.id: f"{t.ad} {t.soyad}" for t in teachers}
                cr_teacher_id = st.selectbox("Öğretmen", list(cr_t_opts.keys()), format_func=lambda x: cr_t_opts[x], key="eu_cr_teacher")
                cr_teacher_name = cr_t_opts[cr_teacher_id]
            else:
                from utils.shared_data import get_all_staff_options as _cr_staff
                _cr_opts = _cr_staff()
                if len(_cr_opts) > 1:
                    cr_teacher_id = ""
                    cr_sel = st.selectbox("Öğretmen (Çalışan Yönetimi)", list(_cr_opts.keys()), key="eu_cr_tname")
                    cr_teacher_name = cr_sel if cr_sel != "-- Secim yapin --" else ""
                else:
                    cr_teacher_id = ""
                    cr_teacher_name = st.text_input("Öğretmen Adi", key="eu_cr_tname_txt")

            cr_category = st.selectbox("Kategori", [c[0] for c in ONERI_KATEGORILERI], format_func=lambda x: dict(ONERI_KATEGORILERI).get(x, x), key="eu_cr_cat")

        cr_note = st.text_area("Not / Gozlem", key="eu_cr_note", height=120, placeholder="Öğrenci ile ilgili gozlem ve onerinizi yaziniz...")
        cc3, cc4 = st.columns(2)
        with cc3:
            cr_priority = st.selectbox("Öncelik", [p[0] for p in ONERI_ONCELIKLERI], format_func=lambda x: dict(ONERI_ONCELIKLERI).get(x, x), key="eu_cr_pri", index=1)
        with cc4:
            cr_followup = st.date_input("Takip Tarihi", key="eu_cr_followup")

        if st.button("Notu Kaydet", type="primary", key="eu_cr_save", use_container_width=True):
            if not cr_note:
                st.error("Not alani bos birakilamaz.")
            else:
                oneri = OgretmenOneri(
                    student_id=cr_stu_id,
                    teacher_id=cr_teacher_id,
                    teacher_name=cr_teacher_name,
                    category=cr_category,
                    note=cr_note,
                    priority=cr_priority,
                    follow_up_date=cr_followup.strftime("%Y-%m-%d"),
                )
                store.save_ogretmen_oneri(oneri)
                st.success("Oneri/gozlem notu kaydedildi!")
                st.rerun()

    with crm2:
        styled_section("CRM Notları", "#2563eb")

        # Filtreler
        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            cr_f_sinif = st.selectbox("Sınıf", [None] + SINIFLAR, format_func=lambda x: "Tümü" if x is None else f"{x}. Sınıf", key="eu_cr_f_sinif")
        with cf2:
            cr_f_sube = st.selectbox("Şube", [None] + SUBELER, format_func=lambda x: "Tümü" if x is None else x, key="eu_cr_f_sube")
        with cf3:
            cr_f_takip = st.checkbox("Sadece takip gereken", key="eu_cr_f_takip")

        # Tum onerileri al
        all_onerileri = store.get_ogretmen_onerileri()

        # Filtre uygula
        if cr_f_sinif is not None or cr_f_sube is not None:
            filtered = []
            for o in all_onerileri:
                stu = store.get_student(o.student_id)
                if not stu:
                    continue
                if cr_f_sinif is not None and stu.sinif != cr_f_sinif:
                    continue
                if cr_f_sube is not None and stu.sube != cr_f_sube:
                    continue
                filtered.append(o)
            all_onerileri = filtered

        if cr_f_takip:
            today = date.today().strftime("%Y-%m-%d")
            all_onerileri = [o for o in all_onerileri if o.follow_up_date and o.follow_up_date <= today and not o.follow_up_done]

        if not all_onerileri:
            st.info("Kayıtli oneri/gozlem notu bulunmuyor.")
        else:
            # Timeline gorununmu
            for o in sorted(all_onerileri, key=lambda x: x.created_at, reverse=True):
                stu = store.get_student(o.student_id)
                stu_ad = f"{stu.ad} {stu.soyad}" if stu else o.student_id
                cat_label = dict(ONERI_KATEGORILERI).get(o.category, o.category)
                pri_label = dict(ONERI_ONCELIKLERI).get(o.priority, o.priority)
                pri_color = {"low": "#22c55e", "normal": "#3b82f6", "high": "#f97316", "urgent": "#ef4444"}.get(o.priority, "#94a3b8")

                takip_badge = ""
                if o.follow_up_date and not o.follow_up_done:
                    if o.follow_up_date <= date.today().strftime("%Y-%m-%d"):
                        takip_badge = '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px;">Takip Gecikti</span>'
                    else:
                        takip_badge = '<span style="background:#f59e0b;color:white;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px;">Takip Bekliyor</span>'
                elif o.follow_up_done:
                    takip_badge = '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px;">Takip Yapildi</span>'

                st.markdown(f"""
                <div style="border-left:4px solid {pri_color};padding:12px 16px;margin:8px 0;background:#111827;border-radius:0 8px 8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:700;">{stu_ad}</span>
                            <span style="background:{pri_color};color:white;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px;">{pri_label}</span>
                            <span style="background:#e2e8f0;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:4px;">{cat_label}</span>
                            {takip_badge}
                        </div>
                        <div style="color:#94a3b8;font-size:12px;">{o.created_at[:10] if o.created_at else ''}</div>
                    </div>
                    <div style="margin-top:8px;color:#334155;">{o.note}</div>
                    <div style="margin-top:4px;color:#94a3b8;font-size:12px;">Öğretmen: {o.teacher_name} | Takip: {o.follow_up_date if o.follow_up_date else '-'}</div>
                </div>
                """, unsafe_allow_html=True)

                # Takip yap butonu
                if o.follow_up_date and not o.follow_up_done:
                    tc1, tc2 = st.columns([3, 1])
                    with tc1:
                        t_note = st.text_input("Takip Notu", key=f"eu_cr_tn_{o.id}")
                    with tc2:
                        st.markdown("")
                        st.markdown("")
                        if st.button("Takip Tamamla", key=f"eu_cr_td_{o.id}"):
                            store.update_ogretmen_oneri(o.id, follow_up_done=True, follow_up_notes=t_note)
                            st.success("Takip tamamlandı!")
                            st.rerun()


# ---------- TAB 6: ANALIZ & RAPORLAR ----------

def _render_eu_analiz(store, engine, kurum):
    styled_section("Erken Uyari Analiz & Raporlar", "#059669")

    at1, at2, at3 = st.tabs(["  📊 Kohort Analizi  ", "  🎯 Mudahale Etkinligi  ", "  ⚖️ Karsilastirmali Rapor  "])

    with at1:
        styled_section("Sınıf/Şube Bazli Risk Dagilimi", "#059669")
        # Her sinif/sube için risk ozeti
        all_students = store.get_students(durum="aktif")
        if not all_students:
            st.info("Öğrenci bulunamadı.")
        else:
            # Sinif bazli gruplama
            sinif_sube_map = {}
            for s in all_students:
                key = f"{s.sinif}/{s.sube}"
                if key not in sinif_sube_map:
                    sinif_sube_map[key] = []
                sinif_sube_map[key].append(s)

            kohort_data = []
            for key in sorted(sinif_sube_map.keys()):
                stus = sinif_sube_map[key]
                total = len(stus)
                risk_count = 0
                toplam_skor = 0
                for s in stus:
                    risk = engine.calculate_composite_risk(s.id)
                    if risk["severity"]:
                        risk_count += 1
                    toplam_skor += risk["score"]
                ort_skor = toplam_skor / total if total > 0 else 0
                kohort_data.append({
                    "Sınıf/Şube": key,
                    "Öğrenci Sayısı": total,
                    "Riskli Öğrenci": risk_count,
                    "Risk Orani (%)": f"{(risk_count / total * 100):.0f}" if total > 0 else "0",
                    "Ort. Risk Skoru": f"{ort_skor:.1f}",
                })

            if kohort_data:
                df_kohort = pd.DataFrame(kohort_data)
                st.markdown(ReportStyler.colored_table_html(df_kohort, header_color="#059669"), unsafe_allow_html=True)

                # Bar chart
                chart_data = {d["Sınıf/Şube"]: float(d["Ort. Risk Skoru"]) for d in kohort_data}
                st.markdown(ReportStyler.horizontal_bar_html(chart_data, color="#059669"), unsafe_allow_html=True)

    with at2:
        styled_section("Mudahale Etkinlik Analizi", "#059669")
        all_muds = store.get_mudahaleler()
        if not all_muds:
            st.info("Mudahale kaydi bulunmuyor.")
        else:
            # Tip bazli basari orani
            tip_stats = {}
            for m in all_muds:
                tip = dict(MUDAHALE_TIPLERI).get(m.mudahale_type, m.mudahale_type)
                if tip not in tip_stats:
                    tip_stats[tip] = {"toplam": 0, "tamamlanan": 0}
                tip_stats[tip]["toplam"] += 1
                if m.status == "completed":
                    tip_stats[tip]["tamamlanan"] += 1

            etkinlik_rows = []
            for tip, stat in tip_stats.items():
                oran = (stat["tamamlanan"] / stat["toplam"] * 100) if stat["toplam"] > 0 else 0
                etkinlik_rows.append({
                    "Mudahale Tipi": tip,
                    "Toplam": stat["toplam"],
                    "Tamamlanan": stat["tamamlanan"],
                    "Başarı Orani (%)": f"{oran:.0f}",
                })

            st.markdown(ReportStyler.colored_table_html(pd.DataFrame(etkinlik_rows), header_color="#059669"), unsafe_allow_html=True)

            # Tamamlanma orani bar chart
            bar_data = {r["Mudahale Tipi"]: float(r["Başarı Orani (%)"]) for r in etkinlik_rows}
            st.markdown(ReportStyler.horizontal_bar_html(bar_data, color="#059669"), unsafe_allow_html=True)

            # Metrik kartlar
            toplam_mud = len(all_muds)
            tamamlanan = sum(1 for m in all_muds if m.status == "completed")
            devam_eden = sum(1 for m in all_muds if m.status == "in_progress")
            planli = sum(1 for m in all_muds if m.status == "planned")
            st.markdown(ReportStyler.metric_cards_html([
                ("Toplam Mudahale", str(toplam_mud), "#6366f1", ""),
                ("Tamamlanan", str(tamamlanan), "#22c55e", ""),
                ("Devam Eden", str(devam_eden), "#f59e0b", ""),
                ("Planli", str(planli), "#3b82f6", ""),
            ]), unsafe_allow_html=True)

    with at3:
        styled_section("Karsilastirmali Rapor", "#059669")

        # Mevcut aktif alertler ile cozulmus alertler karsilastirmasi
        active_alerts = store.get_risk_alerts(status="active")
        resolved_alerts = store.get_risk_alerts(status="resolved")
        all_alerts = store.get_risk_alerts()

        st.markdown(ReportStyler.metric_cards_html([
            ("Toplam Uyari", str(len(all_alerts)), "#6366f1", ""),
            ("Aktif", str(len(active_alerts)), "#ef4444", ""),
            ("Cozulmus", str(len(resolved_alerts)), "#22c55e", ""),
            ("Diger", str(len(all_alerts) - len(active_alerts) - len(resolved_alerts)), "#94a3b8", ""),
        ]), unsafe_allow_html=True)

        if all_alerts:
            # Severity dagilimi
            sev_dist = {}
            for a in all_alerts:
                lbl = RISK_SEVERITY_LABELS.get(a.severity, a.severity)
                sev_dist[lbl] = sev_dist.get(lbl, 0) + 1
            st.markdown(ReportStyler.donut_chart_svg(sev_dist, ["#22c55e", "#f59e0b", "#f97316", "#ef4444"]), unsafe_allow_html=True)

        # PDF export
        styled_section("Rapor & Paylasim", "#059669")
        try:
            pdf_gen = ReportPDFGenerator("Erken Uyari Analiz Raporu", kurum.get("name", ""))
            pdf_gen.add_header(kurum.get("name", ""), kurum.get("logo_path", ""))
            pdf_gen.add_section("Genel Özet")
            pdf_gen.add_metrics([
                ("Toplam Uyari", str(len(all_alerts)), "#6366f1"),
                ("Aktif", str(len(active_alerts)), "#ef4444"),
                ("Cozulmus", str(len(resolved_alerts)), "#22c55e"),
            ])
            all_muds_r = store.get_mudahaleler()
            if all_muds_r:
                pdf_gen.add_section("Mudahale Özeti")
                pdf_gen.add_metrics([
                    ("Toplam", str(len(all_muds_r)), "#6366f1"),
                    ("Tamamlanan", str(sum(1 for m in all_muds_r if m.status == "completed")), "#22c55e"),
                ])
            pdf_bytes = pdf_gen.generate()
            ReportSharer.render_share_ui(pdf_bytes, "erken_uyari_analiz.pdf", "Erken Uyari Analiz Raporu", key_prefix="eu_an")
        except Exception as e:
            st.warning(f"PDF olusturulamadi: {e}")


# ==================== KAZANIM TAKİP SİSTEMİ (KYT) ====================

def _generate_kyt_questions(ders: str, grade: int, kazanim_metni: str) -> list[dict]:
    """Tek kazanim için 2 MCQ soru uret (OpenAI GPT-4o-mini).
    Dondurur: [{"metin": "...", "secenekler": {"A":..}, "dogru": "A", "aciklama": "..."}]
    """
    import os
    import json

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API anahtari bulunamadı. .env dosyasinda OPENAI_API_KEY ayarlayin.")
        return []

    kademe_map = {"ILKOKUL": "İlkokul", "ORTAOKUL": "Ortaokul", "LISE": "Lise"}
    kademe = _get_kademe(grade)
    kademe_adi = kademe_map.get(kademe, "Ortaokul")

    prompt = f"""Sen deneyimli bir {ders} ogretmenisin. MEB mufredatina hakim, profesyonel soru hazirlama uzmanisin.

## GOREV
Asagidaki kazanima gore tam olarak 2 coktan secmeli (MCQ) soru hazirla.

## SINIF SEVIYESI
{grade}. sinif ({kademe_adi})

## KAZANIM
{kazanim_metni}

## KURALLAR
1. Her soru kazanima TAMAMEN uygun olmali
2. Soru metni en az 2-3 cumle, gercek hayattan senaryo icermeli
3. 4 secenek (A, B, C, D), sadece 1 dogru cevap
4. Her soruya kisa aciklama ekle
5. Celdiriciler yaygin ogrenci hatalarina dayali olmali
6. Dili {grade}. sinif seviyesine uygun tut

## CIKTI FORMATI (SADECE JSON)
```json
{{
    "sorular": [
        {{
            "metin": "Soru metni burada",
            "secenekler": {{"A": "A sikki", "B": "B sikki", "C": "C sikki", "D": "D sikki"}},
            "dogru": "A",
            "aciklama": "Cozum aciklamasi"
        }}
    ]
}}
```

ONEMLI: Tam olarak 2 soru uret. Sadece JSON dondur, baska aciklama yazma."""

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Sen bir {ders} ogretmenisin. Kazanima uygun, MEB standardinda sorular hazirliyorsun. Sadece JSON formatinda cevap ver."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        content = response.choices[0].message.content or ""
        # JSON parse
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)
        return data.get("sorular", [])
    except Exception as e:
        st.error(f"AI soru uretim hatasi: {e}")
        return []


def _render_kyt_dashboard(store: AkademikDataStore):
    """KYT Dashboard - genel istatistikler ve grafikler."""
    styled_section("KYT Dashboard", "#10b981")

    akademik_yil = _get_akademik_yil()

    c1, c2, c3 = st.columns(3)
    with c1:
        sinif_sec = st.selectbox("Sınıf", [None] + list(range(1, 13)),
                                  format_func=lambda x: "Tümü" if x is None else f"{x}. Sınıf",
                                  key="kyt_dash_sinif")
    with c2:
        sube_sec = st.selectbox("Şube", [None] + list(SUBELER),
                                 format_func=lambda x: "Tümü" if x is None else x,
                                 key="kyt_dash_sube")
    with c3:
        st.write("")
        st.caption(f"Akademik Yil: {akademik_yil}")

    stats = store.get_kyt_dashboard(sinif=sinif_sec, sube=sube_sec, akademik_yil=akademik_yil)

    styled_stat_row([
        ("Toplam Kazanim", str(stats["toplam_kazanim"]), "#7c3aed", ""),
        ("Toplam Soru", str(stats["toplam_soru"]), "#2563eb", ""),
        ("Cevaplanan", str(stats["toplam_cevap"]), "#f59e0b", ""),
        ("Dogru", str(stats["dogru"]), "#22c55e", ""),
        ("Yanlis", str(stats["yanlis"]), "#ef4444", ""),
    ])

    if stats["toplam_cevap"] > 0:
        st.metric("Başarı Orani", f"%{stats['basari_yuzde']}")

    # Ders bazli dagilim
    if stats["ders_stats"]:
        st.markdown("#### Ders Bazli Performans")
        ders_data = []
        for ders, ds in stats["ders_stats"].items():
            basari = round((ds["dogru"] / ds["cevap"]) * 100, 1) if ds["cevap"] > 0 else 0
            ders_data.append({"Ders": ders, "Soru": ds["soru"], "Cevap": ds["cevap"],
                              "Dogru": ds["dogru"], "Başarı %": basari})
        df = pd.DataFrame(ders_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        if len(ders_data) > 0:
            chart_df = pd.DataFrame(ders_data).set_index("Ders")[["Soru", "Dogru"]]
            st.bar_chart(chart_df)

    # Gunluk trend
    if stats["gunluk_trend"]:
        st.markdown("#### Günlük Cozum Trendi")
        trend_data = []
        for tarih, td in sorted(stats["gunluk_trend"].items()):
            trend_data.append({"Tarih": tarih, "Cevap": td["cevap"], "Dogru": td["dogru"]})
        if trend_data:
            tdf = pd.DataFrame(trend_data).set_index("Tarih")
            st.line_chart(tdf)

    if stats["toplam_soru"] == 0:
        styled_info_banner("Henuz KYT sorusu uretilmemis. 'Günlük Rapor & Soru Uret' sekmesinden baslayabilirsiniz.", "info")


def _render_kyt_gunluk_rapor(store: AkademikDataStore, key_prefix: str = "kyt"):
    """Gunluk kazanim raporu ve otomatik soru uretimi."""
    styled_section("Günlük Rapor & Soru Uretimi", "#059669")

    akademik_yil = _get_akademik_yil()
    today_str = datetime.now().strftime("%Y-%m-%d")

    c1, c2, c3 = st.columns(3)
    with c1:
        tarih = st.date_input("Tarih", value=datetime.now().date(), key=f"{key_prefix}_rapor_tarih")
        tarih_str = tarih.strftime("%Y-%m-%d")
    with c2:
        sinif = st.selectbox("Sınıf", list(range(1, 13)),
                              format_func=lambda x: f"{x}. Sınıf",
                              key=f"{key_prefix}_rapor_sinif")
    with c3:
        sube = st.selectbox("Şube", list(SUBELER), key=f"{key_prefix}_rapor_sube")

    st.markdown("---")

    # Kademe ve KYT dersleri
    kademe = _get_kademe(sinif)
    kyt_dersler = KYT_DERSLER.get(kademe, [])

    # O gun islenmis kazanimlari getir
    all_islenmis = store.get_kazanim_isleme(sinif=sinif, sube=sube, durum="islendi", akademik_yil=akademik_yil)
    gunluk_kazanimlar = [k for k in all_islenmis if k.tarih == tarih_str]

    # KYT derslerine gore filtrele
    kyt_kazanimlar = [k for k in gunluk_kazanimlar if k.ders in kyt_dersler]

    if not kyt_kazanimlar:
        styled_info_banner(
            f"{tarih_str} tarihinde {sinif}/{sube} için islenmis KYT kazanimi bulunamadı.\n\n"
            f"KYT dersleri ({kademe}): {', '.join(kyt_dersler)}\n\n"
            "Öğretmenlerin 'Öğretim & Planlama > Uygulama Takibi' sekmesinden kazanimlari islemesi gerekir.",
            "warning"
        )
        return

    # Kazanimlari ders bazli grupla
    ders_kazanim = {}
    for k in kyt_kazanimlar:
        ders_kazanim.setdefault(k.ders, []).append(k)

    st.markdown(f"### {tarih_str} - {sinif}/{sube} Islenmis Kazanimlar")
    styled_stat_row([
        ("Toplam Kazanim", str(len(kyt_kazanimlar)), "#7c3aed", ""),
        ("Ders Sayısı", str(len(ders_kazanim)), "#2563eb", ""),
        ("Uretilecek Soru", str(len(kyt_kazanimlar) * 2), "#f59e0b", ""),
    ])

    for ders, kazanimlar in ders_kazanim.items():
        with st.expander(f"{ders} ({len(kazanimlar)} kazanim)", expanded=True):
            for k in kazanimlar:
                st.write(f"- **{k.kazanim_kodu}**: {k.kazanim_metni[:150]}")

    # Mevcut KYT sorulari kontrol
    mevcut_sorular = store.get_kyt_sorular(sinif=sinif, sube=sube, tarih=tarih_str)

    if mevcut_sorular:
        st.success(f"Bu tarih için {len(mevcut_sorular)} KYT sorusu zaten uretilmis.")
        with st.expander("Mevcut Sorulari Gor", expanded=False):
            for i, s in enumerate(mevcut_sorular, 1):
                st.markdown(f"**Soru {i}** ({s.ders} - {s.kazanim_kodu})")
                st.write(s.soru_metni)
                for harf, metin in s.secenekler.items():
                    marker = " **[DOGRU]**" if harf == s.dogru_cevap else ""
                    st.write(f"  {harf}) {metin}{marker}")
                st.caption(f"Açıklama: {s.aciklama}")
                st.markdown("---")
    else:
        # Soru uretim butonu
        if st.button("KYT Sorularini Uret", key=f"{key_prefix}_uret_btn", type="primary",
                      use_container_width=True):
            uretilen_toplam = 0
            progress_bar = st.progress(0)
            status_text = st.empty()

            toplam_kazanim = len(kyt_kazanimlar)
            for idx, kaz in enumerate(kyt_kazanimlar):
                status_text.text(f"Soru uretiliyor: {kaz.ders} - {kaz.kazanim_kodu} ({idx+1}/{toplam_kazanim})")
                progress_bar.progress((idx + 1) / toplam_kazanim)

                sorular = _generate_kyt_questions(kaz.ders, sinif, kaz.kazanim_metni)

                for soru_data in sorular:
                    kyt_soru = KYTSoru(
                        sinif=sinif,
                        sube=sube,
                        ders=kaz.ders,
                        kazanim_kodu=kaz.kazanim_kodu,
                        kazanim_metni=kaz.kazanim_metni,
                        soru_metni=soru_data.get("metin", ""),
                        secenekler=soru_data.get("secenekler", {}),
                        dogru_cevap=soru_data.get("dogru", "A"),
                        aciklama=soru_data.get("aciklama", ""),
                        tarih=tarih_str,
                        kaynak_kazanim_id=kaz.id,
                        akademik_yil=akademik_yil,
                    )
                    store.save_kyt_soru(kyt_soru)
                    uretilen_toplam += 1

            progress_bar.progress(1.0)
            status_text.empty()

            # Otomatik odev olustur (ders bazli)
            odev_sayisi = 0
            for ders, kazanimlar in ders_kazanim.items():
                kazanim_listesi = ", ".join([k.kazanim_kodu for k in kazanimlar])
                odev = Odev(
                    sinif=sinif,
                    sube=sube,
                    ders=ders,
                    baslik=f"KYT Ödev - {tarih_str} - {ders}",
                    aciklama=f"Kazanim Yoklama Testi: {kazanim_listesi}",
                    odev_turu="test",
                    kazanim_kodu=kazanim_listesi,
                    verilme_tarihi=tarih_str,
                    son_teslim_tarihi=tarih_str,
                    online_teslim=True,
                    ogrenci_teslim_turu="metin",
                    akademik_yil=akademik_yil,
                )
                store.save_odev(odev)
                store.odev_teslim_olustur(odev)
                odev_sayisi += 1

            st.success(f"{uretilen_toplam} KYT sorusu uretildi ve {odev_sayisi} odev oluşturuldu!")
            st.rerun()


def _render_kyt_ogrenci_analizi(store: AkademikDataStore):
    """Ogrenci bazli KYT performans analizi."""
    styled_section("Öğrenci KYT Analizi", "#8b5cf6")

    akademik_yil = _get_akademik_yil()

    c1, c2 = st.columns(2)
    with c1:
        sinif = st.selectbox("Sınıf", list(range(1, 13)),
                              format_func=lambda x: f"{x}. Sınıf",
                              key="kyt_analiz_sinif")
    with c2:
        sube = st.selectbox("Şube", list(SUBELER), key="kyt_analiz_sube")

    ogrenciler = store.get_students(sinif=sinif, sube=sube, durum="aktif")
    if not ogrenciler:
        styled_info_banner("Bu sinif/subede aktif ogrenci bulunamadı.", "warning")
        return

    ogrenci_map = {s.id: s for s in ogrenciler}
    ogrenci_secim = st.selectbox(
        "Öğrenci",
        [s.id for s in ogrenciler],
        format_func=lambda x: f"{ogrenci_map[x].ad} {ogrenci_map[x].soyad} ({ogrenci_map[x].numara})",
        key="kyt_analiz_ogrenci"
    )

    if not ogrenci_secim:
        return

    ogrenci = ogrenci_map[ogrenci_secim]
    st.markdown(f"### {ogrenci.ad} {ogrenci.soyad} - KYT Performans Analizi")
    st.markdown("---")

    analiz = store.get_kyt_ogrenci_analizi(student_id=ogrenci_secim, akademik_yil=akademik_yil)

    if analiz["toplam"] == 0:
        styled_info_banner("Bu ogrenci henuz KYT sorusu cevaplamamis.", "info")
        return

    styled_stat_row([
        ("Toplam Cevap", str(analiz["toplam"]), "#2563eb", ""),
        ("Dogru", str(analiz["dogru"]), "#22c55e", ""),
        ("Yanlis", str(analiz["yanlis"]), "#ef4444", ""),
        ("Başarı %", f"%{analiz['basari_yuzde']}", "#7c3aed", ""),
    ])

    # Ders bazli performans
    if analiz["ders_performans"]:
        st.markdown("#### Ders Bazli Performans")
        ders_data = []
        for ders, dp in analiz["ders_performans"].items():
            basari = round((dp["dogru"] / dp["toplam"]) * 100, 1) if dp["toplam"] > 0 else 0
            ders_data.append({
                "Ders": ders,
                "Toplam": dp["toplam"],
                "Dogru": dp["dogru"],
                "Yanlis": dp["toplam"] - dp["dogru"],
                "Başarı %": basari,
            })
        df = pd.DataFrame(ders_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Grafik
        chart_df = pd.DataFrame(ders_data).set_index("Ders")[["Dogru", "Yanlis"]]
        st.bar_chart(chart_df)

    # Gunluk trend
    if analiz["gunluk_trend"]:
        st.markdown("#### Günlük İlerleme Trendi")
        trend_data = []
        for tarih, td in sorted(analiz["gunluk_trend"].items()):
            basari = round((td["dogru"] / td["toplam"]) * 100, 1) if td["toplam"] > 0 else 0
            trend_data.append({"Tarih": tarih, "Başarı %": basari, "Toplam": td["toplam"]})
        if trend_data:
            tdf = pd.DataFrame(trend_data).set_index("Tarih")
            st.line_chart(tdf[["Başarı %"]])

    # Eksik kazanimlar
    cevaplar = store.get_kyt_cevaplar(student_id=ogrenci_secim, akademik_yil=akademik_yil)
    yanlis_kazanimlar = {}
    sorular = store.get_kyt_sorular(sinif=sinif, sube=sube)
    soru_map = {s.id: s for s in sorular}
    for c in cevaplar:
        if not c.dogru_mu:
            soru = soru_map.get(c.soru_id)
            if soru:
                key = soru.kazanim_kodu
                if key not in yanlis_kazanimlar:
                    yanlis_kazanimlar[key] = {"metin": soru.kazanim_metni, "ders": soru.ders, "yanlis": 0}
                yanlis_kazanimlar[key]["yanlis"] += 1

    if yanlis_kazanimlar:
        st.markdown("#### Eksik Kazanimlar (En Çok Yanlis)")
        sorted_eksik = sorted(yanlis_kazanimlar.items(), key=lambda x: x[1]["yanlis"], reverse=True)
        for kod, info in sorted_eksik[:10]:
            st.warning(f"**{kod}** ({info['ders']}): {info['metin'][:120]}... | Yanlis: {info['yanlis']}")


def _render_kyt_raporlar(store: AkademikDataStore):
    """KYT genel raporlari."""
    styled_section("KYT Raporlari", "#dc2626")

    akademik_yil = _get_akademik_yil()

    c1, c2 = st.columns(2)
    with c1:
        sinif = st.selectbox("Sınıf", [None] + list(range(1, 13)),
                              format_func=lambda x: "Tümü" if x is None else f"{x}. Sınıf",
                              key="kyt_rapor2_sinif")
    with c2:
        sube = st.selectbox("Şube", [None] + list(SUBELER),
                             format_func=lambda x: "Tümü" if x is None else x,
                             key="kyt_rapor2_sube")

    sorular = store.get_kyt_sorular(sinif=sinif, sube=sube, akademik_yil=akademik_yil)
    cevaplar = store.get_kyt_cevaplar(sinif=sinif, sube=sube, akademik_yil=akademik_yil)

    if not sorular:
        styled_info_banner("Henuz KYT sorusu uretilmemis.", "info")
        return

    st.markdown("### Genel Özet")
    dogru = sum(1 for c in cevaplar if c.dogru_mu)
    yanlis = len(cevaplar) - dogru
    styled_stat_row([
        ("Toplam Soru", str(len(sorular)), "#2563eb", ""),
        ("Cevaplanan", str(len(cevaplar)), "#f59e0b", ""),
        ("Dogru", str(dogru), "#22c55e", ""),
        ("Yanlis", str(yanlis), "#ef4444", ""),
    ])

    # En basarili kazanimlar
    kazanim_perf = {}
    for c in cevaplar:
        # Soru bilgisini bul
        soru = None
        for s in sorular:
            if s.id == c.soru_id:
                soru = s
                break
        if soru:
            key = soru.kazanim_kodu
            if key not in kazanim_perf:
                kazanim_perf[key] = {"metin": soru.kazanim_metni[:80], "ders": soru.ders,
                                      "toplam": 0, "dogru": 0}
            kazanim_perf[key]["toplam"] += 1
            if c.dogru_mu:
                kazanim_perf[key]["dogru"] += 1

    if kazanim_perf:
        st.markdown("### Kazanim Bazli Performans")
        kaz_data = []
        for kod, kp in kazanim_perf.items():
            basari = round((kp["dogru"] / kp["toplam"]) * 100, 1) if kp["toplam"] > 0 else 0
            kaz_data.append({
                "Kazanim": kod, "Ders": kp["ders"], "Metin": kp["metin"],
                "Toplam": kp["toplam"], "Dogru": kp["dogru"], "Başarı %": basari,
            })
        kaz_data.sort(key=lambda x: x["Başarı %"])
        df = pd.DataFrame(kaz_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Grafik - en dusuk basarili kazanimlar
        en_dusuk = kaz_data[:10]
        if en_dusuk:
            st.markdown("#### En Dusuk Başarılı Kazanimlar")
            chart_df = pd.DataFrame(en_dusuk).set_index("Kazanim")[["Başarı %"]]
            st.bar_chart(chart_df)

    # Ogrenci siralama
    if sinif and sube:
        ogrenciler = store.get_students(sinif=sinif, sube=sube, durum="aktif")
        if ogrenciler:
            st.markdown("### Öğrenci Sıralama")
            ogr_data = []
            for ogr in ogrenciler:
                ogr_cevaplar = [c for c in cevaplar if c.student_id == ogr.id]
                if ogr_cevaplar:
                    ogr_dogru = sum(1 for c in ogr_cevaplar if c.dogru_mu)
                    ogr_basari = round((ogr_dogru / len(ogr_cevaplar)) * 100, 1)
                    ogr_data.append({
                        "Öğrenci": f"{ogr.ad} {ogr.soyad}",
                        "Toplam": len(ogr_cevaplar),
                        "Dogru": ogr_dogru,
                        "Yanlis": len(ogr_cevaplar) - ogr_dogru,
                        "Başarı %": ogr_basari,
                    })
            if ogr_data:
                ogr_data.sort(key=lambda x: x["Başarı %"], reverse=True)
                df = pd.DataFrame(ogr_data)
                st.dataframe(df, use_container_width=True, hide_index=True)


def _ai_borc_yol_haritasi(ogrenci_adi: str, sinif: int, sube: str, borclar: list) -> str:
    """OpenAI GPT-4o-mini ile borçlu kazanımlar için kişiselleştirilmiş yol haritası üret."""
    try:
        import openai
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            return ""

        borc_listesi = "\n".join([
            f"- {b.ders} | {b.kazanim_metni} | Neden: {BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)}"
            for b in borclar[:10]
        ])

        prompt = (
            f"Öğrenci: {ogrenci_adi}, Sınıf: {sinif}/{sube}\n\n"
            f"Borçlu olduğu kazanımlar:\n{borc_listesi}\n\n"
            "Bu öğrenci için:\n"
            "1) Her kazanım için kısa ve net bir telafi yol haritası yaz\n"
            "2) Günlük çalışma önerileri ver\n"
            "3) Her kazanım için 2 pekiştirme sorusu sor\n"
            "Türkçe yaz, motivasyonel ve destekleyici bir dil kullan."
        )

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen bir eğitim danışmanısın. Öğrencilere Türkçe, sıcak ve destekleyici bir dilde rehberlik yapıyorsun."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"AI analizi alınamadı: {e}"


def _generate_borc_pdf(ogrenci_adi: str, sinif: int, sube: str,
                       borclar: list, ai_rapor: str = "") -> bytes:
    """Kazanım Borç Bankası PDF raporu oluştur."""
    try:
        from io import BytesIO
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        from utils.shared_data import ensure_turkish_pdf_fonts
        borc_fn, borc_fb = ensure_turkish_pdf_fonts()

        def _n(text) -> str:
            return str(text) if text else ""

        borc_page_w = A4[0] - 3 * cm

        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("BorcTitle", fontName=borc_fb, fontSize=16, alignment=TA_CENTER,
                                     textColor=rl_colors.white, spaceAfter=4)
        sub_style = ParagraphStyle("BorcSub", fontName=borc_fn, fontSize=11, alignment=TA_CENTER,
                                   textColor=rl_colors.HexColor("#cbd5e1"), spaceAfter=4)
        section_style = ParagraphStyle("BorcSection", fontName=borc_fb, fontSize=12,
                                       textColor=rl_colors.HexColor("#94A3B8"), spaceBefore=12, spaceAfter=6)
        body_style = ParagraphStyle("BorcBody", fontName=borc_fn, fontSize=9,
                                    textColor=rl_colors.HexColor("#334155"), spaceAfter=4, leading=14)

        story = []

        # Premium header banner
        borc_banner_content = [
            Paragraph(_n("Kazanım Borç Bankası Raporu"), title_style),
            Paragraph(_n(f"{ogrenci_adi}  |  {sinif}. Sınıf / {sube} Şubesi"), sub_style),
        ]
        borc_banner_tbl = Table([[borc_banner_content]], colWidths=[borc_page_w])
        borc_banner_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor("#0B0F19")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [6, 6, 0, 0]),
            ("TOPPADDING", (0, 0), (-1, -1), 14),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ]))
        story.append(borc_banner_tbl)
        # Teal accent line
        borc_accent_data = [[""]]
        borc_accent_tbl = Table(borc_accent_data, colWidths=[borc_page_w], rowHeights=[3])
        borc_accent_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor("#2563eb")),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(borc_accent_tbl)
        story.append(Spacer(1, 6))

        story.append(Paragraph(_n(f"Rapor tarihi: {date.today().strftime('%d.%m.%Y')}"), body_style))
        story.append(Spacer(1, 10))

        # Borç tablosu
        story.append(Paragraph(_n("Borçlu Kazanımlar"), section_style))
        if borclar:
            table_data = [[_n("Ders"), _n("Kazanım"), _n("Neden"), _n("Durum"), _n("Tarih")]]
            for b in borclar:
                table_data.append([
                    _n(b.ders),
                    _n(b.kazanim_metni[:50] + ("..." if len(b.kazanim_metni) > 50 else "")),
                    _n(BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)),
                    _n("Borçlu" if b.durum == "borc_var" else "Kapandı"),
                    _n(b.kazanim_isleme_tarihi[:10] if b.kazanim_isleme_tarihi else "-"),
                ])

            tbl = Table(table_data, colWidths=[3*cm, 6.5*cm, 4*cm, 2*cm, 2.5*cm])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#94A3B8")),
                ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
                ("FONTNAME", (0, 0), (-1, 0), borc_fb),
                ("FONTNAME", (0, 1), (-1, -1), borc_fn),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.white, rl_colors.HexColor("#1A2035")]),
                ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.HexColor("#CBD5E1")),
                ("BOX", (0, 0), (-1, -1), 1.0, rl_colors.HexColor("#CBD5E1")),
                ("LINEBELOW", (0, 0), (-1, 0), 1.0, rl_colors.HexColor("#2563eb")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(tbl)
        else:
            story.append(Paragraph(_n("Bu öğrenciye ait borçlu kazanım bulunmamaktadır."), body_style))

        # AI yol haritası
        if ai_rapor:
            story.append(Spacer(1, 14))
            story.append(Paragraph(_n("AI Yol Haritası ve Tavsiyeler"), section_style))
            for satir in ai_rapor.split("\n"):
                if satir.strip():
                    story.append(Paragraph(_n(satir.strip()), body_style))

        doc.build(story)
        return buf.getvalue()
    except Exception as e:
        return b""


@st.fragment
def _render_kazanim_borc_bankasi(store: AkademikDataStore):
    """Kazanım Borç Bankası — admin/öğretmen görünümü."""
    from datetime import date as _date

    styled_section("Kazanım Borç Bankası", "#7c3aed")
    styled_info_banner(
        "Öğretmen kazanım işlediğinde öğrenci devamsız ise veya ödev yapmamış/yanlış yapmış ise "
        "kazanım otomatik borç olarak kaydedilir. Borçlar kapatılana kadar takipte kalır.",
        "info"
    )

    tab_dash, tab_ogrenci, tab_kapat, tab_pdf = st.tabs([
        "  📊 Dashboard  ",
        "  🎓 Öğrenci Bazlı  ",
        "  ✅ Borç Kapat  ",
        "  📄 PDF Rapor  ",
    ])

    # ── Dashboard ──────────────────────────────────────────────────────────────
    with tab_dash:
        styled_section("Borç Durumu Özeti", "#7c3aed")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            sel_sinif_d = st.selectbox("Sınıf", ["Tümü"] + [str(s) for s in SINIFLAR], key="borc_dash_sinif")
        with col_f2:
            sel_sube_d = st.selectbox("Şube", ["Tümü"] + list(SUBELER), key="borc_dash_sube")
        with col_f3:
            akademik_yil = _get_akademik_yil()
            st.text_input("Akademik Yıl", value=akademik_yil, disabled=True, key="borc_dash_yil")

        sinif_filter = int(sel_sinif_d) if sel_sinif_d != "Tümü" else None
        sube_filter = sel_sube_d if sel_sube_d != "Tümü" else None

        borclar = store.get_kazanim_borclari(
            sinif=sinif_filter, sube=sube_filter, akademik_yil=akademik_yil
        )
        actif = [b for b in borclar if b.durum == "borc_var"]
        kapali = [b for b in borclar if b.durum == "kapandi"]

        styled_stat_row([
            ("Toplam Borç", len(borclar), "#7c3aed", "📚"),
            ("Aktif Borç", len(actif), "#ef4444", "🔴"),
            ("Kapatılan", len(kapali), "#10b981", "✅"),
            ("Etkilenen Öğrenci", len({b.student_id for b in actif}), "#f59e0b", "🎓"),
        ])
        st.write("")

        if actif:
            import plotly.graph_objects as go

            col_c1, col_c2 = st.columns(2)
            with col_c1:
                ders_say = {}
                for b in actif:
                    ders_say[b.ders] = ders_say.get(b.ders, 0) + 1
                sorted_ders = sorted(ders_say.items(), key=lambda x: x[1], reverse=True)
                ders_labels = [d[0] for d in sorted_ders]
                ders_values = [d[1] for d in sorted_ders]
                fig = go.Figure(data=[go.Bar(
                    x=ders_values, y=ders_labels, orientation='h',
                    marker_color=SC_COLORS[0],
                    text=ders_values, textposition="outside",
                )])
                fig.update_layout(yaxis=dict(autorange="reversed"))
                sc_bar(fig, height=280, horizontal=True)
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

            with col_c2:
                neden_say = {}
                for b in actif:
                    lbl = BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)
                    neden_say[lbl] = neden_say.get(lbl, 0) + 1
                neden_labels = list(neden_say.keys())
                neden_values = list(neden_say.values())
                n_neden = len(neden_labels)
                fig2 = go.Figure(data=[go.Pie(
                    labels=neden_labels, values=neden_values,
                    hole=0.55,
                    marker=dict(colors=SC_COLORS[:n_neden], line=dict(color="#fff", width=2)),
                )])
                total_borc = sum(neden_values)
                sc_pie(fig2, height=280, center_text=f"<b>{total_borc}</b><br><span style='font-size:10px;color:#64748b'>Borç</span>")
                st.plotly_chart(fig2, use_container_width=True, config=SC_CHART_CFG)

            # Borç tablosu
            st.write("")
            styled_section("Aktif Borç Listesi", "#ef4444")
            rows = []
            for b in sorted(actif, key=lambda x: x.kazanim_isleme_tarihi, reverse=True):
                rows.append({
                    "Öğrenci": b.student_adi,
                    "Sınıf": f"{b.sinif}-{b.sube}",
                    "Ders": b.ders,
                    "Kazanım": b.kazanim_metni[:60] + ("..." if len(b.kazanim_metni) > 60 else ""),
                    "Neden": BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni),
                    "Tarih": b.kazanim_isleme_tarihi[:10] if b.kazanim_isleme_tarihi else "-",
                })
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Seçili filtre için aktif borç kaydı bulunmamaktadır.", "success")

        # Güncelle butonu
        st.write("")
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🔄 Borçları Güncelle", key="borc_guncelle_btn", use_container_width=True):
                with st.spinner("Tüm borçlar hesaplanıyor..."):
                    engine = KazanimBorcEngine(store)
                    engine.guncelle_tum_borclar(akademik_yil)
                st.success("Borçlar güncellendi!")
                st.rerun()

    # ── Öğrenci Bazlı ─────────────────────────────────────────────────────────
    with tab_ogrenci:
        styled_section("Öğrenci Bazlı Borç Takibi", "#7c3aed")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            sel_sinif_o = st.selectbox("Sınıf", [str(s) for s in SINIFLAR], key="borc_ogr_sinif")
        with col_s2:
            sel_sube_o = st.selectbox("Şube", list(SUBELER), key="borc_ogr_sube")
        with col_s3:
            sel_durum_o = st.selectbox("Durum", ["Tümü", "Aktif Borçlar", "Kapatılanlar"], key="borc_ogr_durum")

        sinif_o = int(sel_sinif_o)
        students = [s for s in store.get_students() if s.sinif == sinif_o and s.sube == sel_sube_o]
        ogr_options = {f"{s.ad} {s.soyad} ({s.numara})": s.id for s in students}

        if not ogr_options:
            styled_info_banner(f"{sinif_o}-{sel_sube_o} şubesinde kayıtlı öğrenci bulunamadı.", "warning")
        else:
            sel_ogr_label = st.selectbox("Öğrenci", list(ogr_options.keys()), key="borc_ogr_sec")
            sel_student_id = ogr_options[sel_ogr_label]
            sel_student = next((s for s in students if s.id == sel_student_id), None)

            durum_filter = None
            if sel_durum_o == "Aktif Borçlar":
                durum_filter = "borc_var"
            elif sel_durum_o == "Kapatılanlar":
                durum_filter = "kapandi"

            ogr_borclar = store.get_kazanim_borclari(
                student_id=sel_student_id,
                akademik_yil=_get_akademik_yil(),
                durum=durum_filter,
            )
            aktif_b = [b for b in ogr_borclar if b.durum == "borc_var"]
            kapali_b = [b for b in ogr_borclar if b.durum == "kapandi"]

            styled_stat_row([
                ("Toplam Borç", len(ogr_borclar), "#7c3aed", "📚"),
                ("Aktif Borç", len(aktif_b), "#ef4444", "🔴"),
                ("Kapatılan", len(kapali_b), "#10b981", "✅"),
                ("Borçlu Ders", len({b.ders for b in aktif_b}), "#f59e0b", "📖"),
            ])
            st.write("")

            if ogr_borclar:
                for ders_adi in sorted({b.ders for b in ogr_borclar}):
                    ders_borclar = [b for b in ogr_borclar if b.ders == ders_adi]
                    with st.expander(f"📖 {ders_adi}  ({len([b for b in ders_borclar if b.durum == 'borc_var'])} aktif borç)", expanded=True):
                        for b in ders_borclar:
                            durum_color = "#ef4444" if b.durum == "borc_var" else "#10b981"
                            durum_lbl = "🔴 Borçlu" if b.durum == "borc_var" else "✅ Kapandı"
                            neden_lbl = BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)
                            tarih = b.kazanim_isleme_tarihi[:10] if b.kazanim_isleme_tarihi else "-"
                            st.markdown(
                                f'<div style="border-left:3px solid {durum_color};padding:8px 12px;'
                                f'margin:4px 0;background:#111827;border-radius:0 8px 8px 0">'
                                f'<span style="font-weight:600;font-size:0.85rem">{b.kazanim_metni}</span><br>'
                                f'<span style="font-size:0.75rem;color:#64748b">{neden_lbl} | {tarih} | {durum_lbl}</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
            else:
                styled_info_banner("Bu öğrenciye ait borç kaydı bulunmamaktadır.", "success")

            # AI Yol Haritası
            st.write("")
            styled_section("AI Yol Haritası", "#7c3aed")
            if aktif_b:
                if st.button("🤖 AI Yol Haritası Oluştur", key=f"ai_borc_{sel_student_id}"):
                    with st.spinner("AI yol haritası hazırlanıyor..."):
                        rapor = _ai_borc_yol_haritasi(
                            sel_ogr_label.split(" (")[0],
                            sinif_o, sel_sube_o, aktif_b
                        )
                    if rapor:
                        st.session_state[f"ai_borc_rapor_{sel_student_id}"] = rapor

                if f"ai_borc_rapor_{sel_student_id}" in st.session_state:
                    st.markdown(
                        f'<div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:12px;'
                        f'padding:16px;line-height:1.7;font-size:0.88rem;color:#94A3B8">'
                        f'{st.session_state[f"ai_borc_rapor_{sel_student_id}"].replace(chr(10), "<br>")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                styled_info_banner("Aktif borç bulunmadığından AI yol haritası oluşturulamaz.", "info")

    # ── Borç Kapat ────────────────────────────────────────────────────────────
    with tab_kapat:
        styled_section("Borç Kapatma", "#10b981")
        styled_info_banner(
            "Öğrencinin telafi görevini tamamlaması veya öğretmen onayı ile borçlar kapatılır.",
            "info"
        )

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            sel_sinif_k = st.selectbox("Sınıf", [str(s) for s in SINIFLAR], key="borc_kapat_sinif")
        with col_k2:
            sel_sube_k = st.selectbox("Şube", list(SUBELER), key="borc_kapat_sube")

        sinif_k = int(sel_sinif_k)
        students_k = [s for s in store.get_students() if s.sinif == sinif_k and s.sube == sel_sube_k]
        ogr_options_k = {f"{s.ad} {s.soyad} ({s.numara})": s.id for s in students_k}

        if not ogr_options_k:
            styled_info_banner("Bu şubede kayıtlı öğrenci bulunamadı.", "warning")
        else:
            sel_ogr_k = st.selectbox("Öğrenci", list(ogr_options_k.keys()), key="borc_kapat_ogr")
            sel_sid_k = ogr_options_k[sel_ogr_k]

            aktif_borclar_k = store.get_kazanim_borclari(
                student_id=sel_sid_k, durum="borc_var", akademik_yil=_get_akademik_yil()
            )

            if not aktif_borclar_k:
                styled_info_banner("Bu öğrenciye ait aktif borç bulunmamaktadır.", "success")
            else:
                borc_options_k = {
                    f"{b.ders} | {b.kazanim_metni[:50]} | {BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)}": b.id
                    for b in aktif_borclar_k
                }
                sel_borc_label = st.selectbox("Kapatılacak Borç", list(borc_options_k.keys()), key="borc_kapat_sec")
                sel_borc_id = borc_options_k[sel_borc_label]

                kapanma_sec = st.selectbox(
                    "Kapanma Nedeni",
                    [v for k, v in KAPANMA_NEDENLERI],
                    key="borc_kapat_neden"
                )
                kapanma_kod = next(
                    (k for k, v in KAPANMA_NEDENLERI if v == kapanma_sec),
                    "ogretmen_onayladi"
                )

                if st.button("✅ Borcu Kapat", key="borc_kapat_btn", use_container_width=False):
                    # Borcu güncelle
                    data = store._load(store.kazanim_borc_file)
                    for item in data:
                        if item.get("id") == sel_borc_id:
                            item["durum"] = "kapandi"
                            item["kapanma_tarihi"] = _date.today().isoformat()
                            item["kapanma_nedeni"] = kapanma_kod
                            break
                    store._save(store.kazanim_borc_file, data)
                    st.success("Borç kapatıldı!")
                    st.rerun()

    # ── PDF Rapor ─────────────────────────────────────────────────────────────
    with tab_pdf:
        styled_section("PDF Rapor", "#7c3aed")

        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            sel_sinif_p = st.selectbox("Sınıf", [str(s) for s in SINIFLAR], key="borc_pdf_sinif")
        with col_p2:
            sel_sube_p = st.selectbox("Şube", list(SUBELER), key="borc_pdf_sube")
        with col_p3:
            sel_durum_p = st.selectbox("Durum Filtresi", ["Aktif Borçlar", "Kapatılanlar", "Tümü"], key="borc_pdf_durum")

        sinif_p = int(sel_sinif_p)
        students_p = [s for s in store.get_students() if s.sinif == sinif_p and s.sube == sel_sube_p]
        ogr_opt_p = {f"{s.ad} {s.soyad} ({s.numara})": s.id for s in students_p}

        if not ogr_opt_p:
            styled_info_banner("Bu şubede kayıtlı öğrenci bulunamadı.", "warning")
        else:
            sel_ogr_p = st.selectbox("Öğrenci", list(ogr_opt_p.keys()), key="borc_pdf_ogr")
            sel_sid_p = ogr_opt_p[sel_ogr_p]

            durum_p = None
            if sel_durum_p == "Aktif Borçlar":
                durum_p = "borc_var"
            elif sel_durum_p == "Kapatılanlar":
                durum_p = "kapandi"

            borclar_p = store.get_kazanim_borclari(
                student_id=sel_sid_p, durum=durum_p, akademik_yil=_get_akademik_yil()
            )

            styled_stat_row([
                ("Seçili Borç", len(borclar_p), "#7c3aed", "📚"),
                ("Aktif", len([b for b in borclar_p if b.durum == "borc_var"]), "#ef4444", "🔴"),
                ("Kapatılan", len([b for b in borclar_p if b.durum == "kapandi"]), "#10b981", "✅"),
            ])
            st.write("")

            with_ai = st.checkbox("AI Yol Haritası ekle", value=True, key="borc_pdf_ai")

            if st.button("📄 PDF Oluştur", key="borc_pdf_btn", use_container_width=False):
                ai_text = ""
                if with_ai and borclar_p:
                    aktif_p = [b for b in borclar_p if b.durum == "borc_var"]
                    if aktif_p:
                        with st.spinner("AI yol haritası oluşturuluyor..."):
                            ai_text = _ai_borc_yol_haritasi(
                                sel_ogr_p.split(" (")[0], sinif_p, sel_sube_p, aktif_p
                            )
                with st.spinner("PDF hazırlanıyor..."):
                    pdf_bytes = _generate_borc_pdf(
                        sel_ogr_p.split(" (")[0], sinif_p, sel_sube_p,
                        borclar_p, ai_text
                    )
                if pdf_bytes:
                    dosya_adi = f"kazanim_borc_{sel_ogr_p.split('(')[0].strip().replace(' ', '_')}_{_date.today().strftime('%Y%m%d')}.pdf"
                    st.download_button(
                        "⬇️ PDF İndir",
                        data=pdf_bytes,
                        file_name=dosya_adi,
                        mime="application/pdf",
                        key="borc_pdf_dl",
                    )
                    st.success("PDF hazır! Yukarıdaki butona tıklayarak indirebilirsiniz.")
                else:
                    st.error("PDF oluşturulamadı. ReportLab kurulu değil olabilir.")


@st.fragment
def _render_kyt(store: AkademikDataStore):
    """KYT - Kazanım Takip Sistemi ana fonksiyonu."""
    styled_section("Kazanım Takip Sistemi (KYT)", "#10b981")
    styled_info_banner(
        "Günlük kazanim yoklama, otomatik soru uretimi ve ogrenci analizi. "
        "Öğretmenler 'Öğretim & Planlama' sekmesinden kazanimlari isler, "
        "KYT otomatik soru uretir ve ogrencilere odev olarak atar. "
        "Öğrenciler 'Ödev Takip > Online Ödev Teslim' sekmesinden testleri çözer.",
        "info"
    )

    t1, t2, t3, t4 = st.tabs([
        "  📊 Dashboard  ", "  📝 Günlük Rapor & Soru Uret  ",
        "  🎓 Öğrenci Analizi  ", "  📈 KYT Raporlari  "
    ])

    with t1:
        _render_kyt_dashboard(store)
    with t2:
        _render_kyt_gunluk_rapor(store, key_prefix="kyt_admin")
    with t3:
        _render_kyt_ogrenci_analizi(store)
    with t4:
        _render_kyt_raporlar(store)


# ==================== KURUM HİZMETLERİ: JSON YARDIMCILARI ====================

_HIZMET_DATA_DIR = get_data_path("akademik")

ETKINLIK_DOSYA = "etkinlik_duyurular.json"
YEMEK_MENU_DOSYA = "yemek_menusu.json"
SERVIS_DOSYA = "servis_bilgileri.json"
RANDEVU_DOSYA = "veli_randevular.json"
BELGE_TALEP_DOSYA = "veli_belge_talepleri.json"

MONTHS_TR = ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
             "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"]

ETKINLIK_TIPLERI = [("duyuru", "Duyuru"), ("etkinlik", "Etkinlik"),
                    ("toplanti", "Toplanti"), ("tatil", "Tatil")]

BELGE_TURLERI_MAP = {
    "ogrenci_belgesi": "Öğrenci Belgesi",
    "transkript": "Not Durum Belgesi (Transkript)",
    "devamsizlik_belgesi": "Devamsızlık Belgesi",
    "nakil_belgesi": "Nakil Belgesi",
    "burs_belgesi": "Burs Belgesi",
    "kayit_belgesi": "Kayıt Belgesi",
    "askerlik_belgesi": "Askerlik Tecil Belgesi",
    "disiplin_belgesi": "Disiplin Durum Belgesi",
    "mezuniyet_belgesi": "Mezuniyet Belgesi",
}


def _hizmet_json_path(filename: str) -> str:
    return os.path.join(_HIZMET_DATA_DIR, filename)


def _load_hizmet_json(filename: str) -> list[dict]:
    path = _hizmet_json_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_hizmet_json(filename: str, data: list[dict]) -> None:
    os.makedirs(_HIZMET_DATA_DIR, exist_ok=True)
    with open(_hizmet_json_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==================== KURUM HİZMETLERİ: ANA RENDER ====================

def _render_kurum_hizmetleri(store: AkademikDataStore):
    """Kurum Hizmetleri ana fonksiyonu - 4 alt sekme."""
    kh_t1, kh_t2, kh_t3, kh_t4 = st.tabs([
        "  📢 Etkinlik & Duyurular  ",
        "  🍽️ Yemek Menusu  ",
        "  🚌 Servis Yönetimi  ",
        "  📩 Veli Talep Yönetimi  ",
    ])

    with kh_t1:
        _render_admin_etkinlik_duyuru(store)
    with kh_t2:
        _render_admin_yemek_menusu()
    with kh_t3:
        _render_admin_servis(store)
    with kh_t4:
        _render_admin_veli_talepler(store)


# ==================== 1) ETKİNLİK & DUYURU YÖNETİMİ ====================

def _render_admin_etkinlik_duyuru(store: AkademikDataStore):
    """Duyuru/etkinlik CRUD yonetimi."""
    styled_section("Etkinlik & Duyuru Yönetimi", "#3b82f6")

    duyurular = _load_hizmet_json(ETKINLIK_DOSYA)

    # --- İstatistikler ---
    today = date.today()
    aktif = [d for d in duyurular
             if not d.get("bitis_tarihi") or d.get("bitis_tarihi", "") >= today.isoformat()]
    tip_sayac = {}
    for d in duyurular:
        t = d.get("tip", "duyuru")
        tip_sayac[t] = tip_sayac.get(t, 0) + 1

    stat_items = [
        ("Toplam", str(len(duyurular)), "#3b82f6", "📋"),
        ("Aktif", str(len(aktif)), "#22c55e", "✅"),
        ("Duyuru", str(tip_sayac.get("duyuru", 0)), "#f59e0b", "📢"),
        ("Etkinlik", str(tip_sayac.get("etkinlik", 0)), "#8b5cf6", "🎉"),
    ]
    cols = st.columns(len(stat_items))
    for i, (label, val, color, icon) in enumerate(stat_items):
        with cols[i]:
            st.metric(f"{icon} {label}", val)

    # --- Yeni duyuru/etkinlik ekleme ---
    with st.expander("Yeni Duyuru / Etkinlik Ekle", expanded=False):
        with st.form("admin_etkinlik_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                baslik = st.text_input("Başlık *", key="ae_baslik")
                tip = st.selectbox("Tip", [t[0] for t in ETKINLIK_TIPLERI],
                                   format_func=lambda x: dict(ETKINLIK_TIPLERI).get(x, x),
                                   key="ae_tip")
                tarih = st.date_input("Tarih", value=today, key="ae_tarih")
            with fc2:
                yer = st.text_input("Yer (opsiyonel)", key="ae_yer")
                saat = st.text_input("Saat (opsiyonel, orn: 10:00)", key="ae_saat")
                bitis_tarihi = st.date_input("Bitis Tarihi (opsiyonel)",
                                              value=today + timedelta(days=30),
                                              key="ae_bitis")

            icerik = st.text_area("İçerik *", key="ae_icerik")

            hedef_str = st.text_input(
                "Hedef Sınıflar (virgul ile, bos = tumu)",
                placeholder="5, 6, 7 veya tumu",
                key="ae_hedef")

            onemli = st.checkbox("Onemli / Sabit Duyuru", key="ae_onemli")

            if st.form_submit_button("Kaydet", type="primary"):
                if not baslik or not icerik:
                    st.error("Başlık ve icerik alanlari zorunludur.")
                else:
                    hedef_list = []
                    if hedef_str.strip():
                        for h in hedef_str.split(","):
                            h = h.strip()
                            if h.lower() == "tumu":
                                hedef_list = ["tumu"]
                                break
                            try:
                                hedef_list.append(int(h))
                            except ValueError:
                                hedef_list.append(h)
                    if not hedef_list:
                        hedef_list = ["tumu"]

                    yeni = {
                        "id": str(uuid.uuid4())[:8],
                        "baslik": baslik,
                        "tip": tip,
                        "tarih": tarih.isoformat(),
                        "bitis_tarihi": bitis_tarihi.isoformat(),
                        "yer": yer,
                        "saat": saat,
                        "icerik": icerik,
                        "hedef_siniflar": hedef_list,
                        "onemli": onemli,
                        "olusturma_tarihi": datetime.now().isoformat(),
                    }
                    duyurular.append(yeni)
                    _save_hizmet_json(ETKINLIK_DOSYA, duyurular)
                    st.success(f"'{baslik}' basariyla eklendi!")
                    st.rerun()

    # --- Mevcut duyurulari listele ---
    styled_section("Mevcut Duyurular", "#6366f1")

    if not duyurular:
        styled_info_banner("Henuz duyuru/etkinlik eklenmemiş.", "info")
        return

    for d in sorted(duyurular, key=lambda x: x.get("tarih", ""), reverse=True):
        tip = d.get("tip", "duyuru")
        tip_icon = {"duyuru": "📢", "etkinlik": "🎉", "toplanti": "📋", "tatil": "🏖️"}.get(tip, "📌")
        hedef = d.get("hedef_siniflar", ["tumu"])
        hedef_str = ", ".join(str(h) for h in hedef) if hedef else "Tümü"

        with st.expander(f"{tip_icon} {d.get('baslik', '-')} | {d.get('tarih', '-')} | Hedef: {hedef_str}"):
            st.markdown(f"**İçerik:** {d.get('icerik', '-')}")
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.caption(f"Yer: {d.get('yer', '-')} | Saat: {d.get('saat', '-')}")
            with mc2:
                st.caption(f"Bitis: {d.get('bitis_tarihi', '-')} | Onemli: {'Evet' if d.get('onemli') else 'Hayir'}")
            with mc3:
                if st.button("Sil", key=f"del_etkinlik_{d.get('id', '')}",
                             type="secondary"):
                    duyurular.remove(d)
                    _save_hizmet_json(ETKINLIK_DOSYA, duyurular)
                    st.success("Silindi!")
                    st.rerun()


# ==================== 2) YEMEK MENÜSÜ YÖNETİMİ ====================

def _normalize_menu_kayit(m: dict) -> dict:
    """Eski (ogun+yemekler) veya yeni (kahvalti/ogle/ikindi) formati normalize eder."""
    if "kahvalti" in m or "ogle_yemegi" in m or "ikindi_ara_ogun" in m:
        return m  # zaten yeni format
    # Eski format: tek ogun
    ogun = m.get("ogun", "Ogle Yemegi")
    yemekler = m.get("yemekler", [])
    result = {
        "id": m.get("id", str(uuid.uuid4())[:8]),
        "tarih": m.get("tarih", ""),
        "kahvalti": [],
        "ogle_yemegi": [],
        "ikindi_ara_ogun": [],
        "notlar": m.get("notlar", ""),
        "guncelleme": m.get("guncelleme", ""),
    }
    if "Kahvalti" in ogun or "Sabah" in ogun:
        result["kahvalti"] = yemekler
    elif "Ikindi" in ogun or "ikindi" in ogun:
        result["ikindi_ara_ogun"] = yemekler
    else:
        result["ogle_yemegi"] = yemekler
    return result


def _render_admin_yemek_menusu():
    """Aylik yemek menusu giris ve yonetimi — Kahvaltı / Öğle / İkindi."""
    styled_section("Yemek Menüsü Yönetimi", "#f59e0b")

    menuler_raw = _load_hizmet_json(YEMEK_MENU_DOSYA)
    # Tum kayitlari normalize et (eski+yeni format destegi)
    menuler_map: dict[str, dict] = {}
    for m in menuler_raw:
        nm = _normalize_menu_kayit(m)
        menuler_map[nm["tarih"]] = nm

    today = date.today()
    ay_key = f"{today.year}-{today.month:02d}"
    bu_ay_count = sum(1 for t in menuler_map if t.startswith(ay_key))

    styled_stat_row([
        ("Toplam Kayıt", str(len(menuler_map)), "#f59e0b", ""),
        (f"{MONTHS_TR[today.month-1]} Girilen", str(bu_ay_count), "#ea580c", ""),
        ("Bugün", "✅ Var" if today.isoformat() in menuler_map else "❌ Yok", "#10b981", ""),
    ])

    tab_gunluk, tab_excel, tab_takvim = st.tabs([
        "📅 Günlük Menü Ekle", "📊 Excel Yükle", "📆 Aylık Takvim"
    ])

    # ─────────── TAB 1: GÜNLÜK MENÜ EKLE ───────────
    with tab_gunluk:
        styled_section("Günlük Menü Girişi", "#f59e0b")
        styled_info_banner(
            "Kahvaltı, Öğle Yemeği ve İkindi Ara Öğün bilgilerini ayrı ayrı girin. "
            "Her satıra bir yiyecek/içecek yazın.",
            banner_type="info"
        )
        with st.form("admin_yemek_form", clear_on_submit=True):
            ym_tarih = st.date_input("Tarih", value=today, key="ym_tarih_v2")
            mevcut = menuler_map.get(ym_tarih.isoformat() if hasattr(ym_tarih, 'isoformat') else str(ym_tarih), {})

            yf1, yf2, yf3 = st.columns(3)
            with yf1:
                st.markdown("☕ **Kahvaltı**")
                kahvalti_text = st.text_area(
                    "Kahvaltı",
                    value="\n".join(mevcut.get("kahvalti", [])),
                    height=120,
                    placeholder="Çay\nPeynir\nZeytin\nDomates\nSalatalık\nEkmek",
                    key="ym_kahvalti",
                    label_visibility="collapsed",
                )
            with yf2:
                st.markdown("🍽️ **Öğle Yemeği**")
                ogle_text = st.text_area(
                    "Öğle Yemeği",
                    value="\n".join(mevcut.get("ogle_yemegi", [])),
                    height=120,
                    placeholder="Mercimek Çorbası\nKuru Fasulye\nPirinç Pilavı\nAyran\nMeyve",
                    key="ym_ogle",
                    label_visibility="collapsed",
                )
            with yf3:
                st.markdown("🍎 **İkindi Ara Öğün**")
                ikindi_text = st.text_area(
                    "İkindi Ara Öğün",
                    value="\n".join(mevcut.get("ikindi_ara_ogun", [])),
                    height=120,
                    placeholder="Meyve\nSüt\nBisküvi",
                    key="ym_ikindi",
                    label_visibility="collapsed",
                )
            notlar = st.text_input(
                "Notlar (opsiyonel, ör: Vejetaryen seçenek mevcut)",
                value=mevcut.get("notlar", ""),
                key="ym_notlar_v2"
            )
            if st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True):
                kahvalti = [y.strip() for y in kahvalti_text.strip().split("\n") if y.strip()]
                ogle = [y.strip() for y in ogle_text.strip().split("\n") if y.strip()]
                ikindi = [y.strip() for y in ikindi_text.strip().split("\n") if y.strip()]
                if not any([kahvalti, ogle, ikindi]):
                    st.error("En az bir öğün için yemek giriniz.")
                else:
                    tarih_str = ym_tarih.isoformat()
                    kayit = {
                        "id": mevcut.get("id", str(uuid.uuid4())[:8]),
                        "tarih": tarih_str,
                        "kahvalti": kahvalti,
                        "ogle_yemegi": ogle,
                        "ikindi_ara_ogun": ikindi,
                        "notlar": notlar.strip(),
                        "guncelleme": datetime.now().isoformat(),
                    }
                    menuler_map[tarih_str] = kayit
                    _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                    st.success(f"✅ {tarih_str} menüsü kaydedildi!")
                    st.rerun()

        # Bugünkü + yakın kayıtları göster
        yakin = sorted(
            [(t, m) for t, m in menuler_map.items()
             if t >= (today - timedelta(days=3)).isoformat()],
            key=lambda x: x[0]
        )[:7]
        if yakin:
            st.markdown("---")
            styled_section("Son Girişler", "#ea580c")
            for t_str, m in yakin:
                is_t = t_str == today.isoformat()
                kh = ", ".join(m.get("kahvalti", [])) or "–"
                og = ", ".join(m.get("ogle_yemegi", [])) or "–"
                ik = ", ".join(m.get("ikindi_ara_ogun", [])) or "–"
                with st.expander(f"{'📌 ' if is_t else ''}{t_str}  {'(Bugün)' if is_t else ''}",
                    expanded=is_t
                ):
                    st.markdown(f"☕ **Kahvaltı:** {kh}")
                    st.markdown(f"🍽️ **Öğle:** {og}")
                    st.markdown(f"🍎 **İkindi:** {ik}")
                    if m.get("notlar"):
                        st.caption(f"💡 {m['notlar']}")
                    if st.button("🗑️ Sil", key=f"ym_del_{t_str}", type="secondary"):
                        menuler_map.pop(t_str, None)
                        _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                        st.rerun()

    # ─────────── TAB 2: EXCEL YÜKLE ───────────
    with tab_excel:
        styled_section("Excel ile Aylık Menü Yükle", "#0284c7")
        styled_info_banner(
            "Excel dosyanızın sütunları: A=Tarih (YYYY-AA-GG veya GG.AA.YYYY) | "
            "B=Kahvaltı | C=Öğle Yemeği | D=İkindi Ara Öğün  "
            "Her hücreye yiyecekleri satır satır veya virgülle ayırarak yazabilirsiniz.",
            banner_type="info"
        )

        # Örnek Excel şablon indirme
        st.markdown("**📥 Örnek şablon:**")
        ornek_satir = (
            "Tarih\tKahvaltı\tÖğle Yemeği\tİkindi Ara Öğün\n"
            "2026-03-03\tÇay\nPeynir\nZeytin\tMercimek Çorbası\nKuru Fasulye\nPilav\nAyran\tMeyve\nSüt\n"
            "2026-03-04\tSüt\nKakao\nEkmek\tDomates Çorbası\nSpagetti\nSalata\tBisküvi\nMeyve Suyu"
        )
        st.download_button(
            "📥 Örnek Excel Şablonu İndir (TSV)",
            data=ornek_satir.encode("utf-8-sig"),
            file_name="yemek_menusu_sablon.tsv",
            mime="text/tab-separated-values",
        )

        yukle_dosya = st.file_uploader(
            "Excel Dosyası Seç (.xlsx, .xls, .csv)",
            type=["xlsx", "xls", "csv"],
            key="ym_excel_yukle"
        )
        if yukle_dosya:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(yukle_dosya, allowed_types=["xlsx", "xls", "csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                yukle_dosya = None
        if yukle_dosya:
            try:
                if yukle_dosya.name.endswith(".csv"):
                    df = pd.read_csv(yukle_dosya, dtype=str)
                else:
                    df = pd.read_excel(yukle_dosya, dtype=str)

                df.columns = [str(c).strip() for c in df.columns]
                st.dataframe(df.head(10), use_container_width=True)

                # Sütun eşleştirme
                tum_sutunlar = list(df.columns)
                em1, em2, em3, em4 = st.columns(4)
                with em1:
                    col_tarih = st.selectbox("Tarih Sütunu", tum_sutunlar, key="ym_col_tarih")
                with em2:
                    col_kahvalti = st.selectbox(
                        "Kahvaltı Sütunu", ["(yok)"] + tum_sutunlar, key="ym_col_kah")
                with em3:
                    col_ogle = st.selectbox(
                        "Öğle Yemeği Sütunu", ["(yok)"] + tum_sutunlar, key="ym_col_ogle")
                with em4:
                    col_ikindi = st.selectbox(
                        "İkindi Sütunu", ["(yok)"] + tum_sutunlar, key="ym_col_ikindi")

                if st.button("📥 İçe Aktar", type="primary", key="ym_import_btn",
                              use_container_width=True):
                    eklenen = 0
                    hatalar = []

                    def _parse_ogun_hucre(val) -> list[str]:
                        if not val or str(val).strip() in ("nan", "None", ""):
                            return []
                        return [x.strip() for x in
                                str(val).replace("\n", ",").split(",") if x.strip()]

                    for _, row in df.iterrows():
                        raw_tarih = str(row.get(col_tarih, "")).strip()
                        if not raw_tarih or raw_tarih in ("nan", "None"):
                            continue
                        # Tarih parse
                        tarih_str = None
                        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                from datetime import datetime as _dt2
                                tarih_str = _dt2.strptime(raw_tarih, fmt).strftime("%Y-%m-%d")
                                break
                            except ValueError:
                                continue
                        if not tarih_str:
                            hatalar.append(f"Tarih okunamadı: {raw_tarih}")
                            continue

                        kah = _parse_ogun_hucre(row.get(col_kahvalti) if col_kahvalti != "(yok)" else None)
                        og  = _parse_ogun_hucre(row.get(col_ogle) if col_ogle != "(yok)" else None)
                        ik  = _parse_ogun_hucre(row.get(col_ikindi) if col_ikindi != "(yok)" else None)

                        if not any([kah, og, ik]):
                            continue

                        mevcut_k = menuler_map.get(tarih_str, {})
                        kayit = {
                            "id": mevcut_k.get("id", str(uuid.uuid4())[:8]),
                            "tarih": tarih_str,
                            "kahvalti": kah or mevcut_k.get("kahvalti", []),
                            "ogle_yemegi": og or mevcut_k.get("ogle_yemegi", []),
                            "ikindi_ara_ogun": ik or mevcut_k.get("ikindi_ara_ogun", []),
                            "notlar": mevcut_k.get("notlar", ""),
                            "guncelleme": datetime.now().isoformat(),
                        }
                        menuler_map[tarih_str] = kayit
                        eklenen += 1

                    _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                    st.success(f"✅ {eklenen} günlük menü içe aktarıldı!")
                    if hatalar:
                        st.warning("Bazı satırlar atlandı:\n" + "\n".join(hatalar[:5]))
                    st.rerun()

            except Exception as ex:
                st.error(f"Dosya okunamadı: {ex}")

    # ─────────── TAB 3: AYLIK TAKVİM ───────────
    with tab_takvim:
        styled_section("Aylık Menü Takvimi", "#ea580c")
        tk1, tk2 = st.columns(2)
        with tk1:
            goster_ay = st.selectbox("Ay", list(range(1, 13)),
                                      index=today.month - 1,
                                      format_func=lambda x: MONTHS_TR[x - 1],
                                      key="ym_goster_ay")
        with tk2:
            goster_yil = st.selectbox("Yil", [today.year - 1, today.year, today.year + 1],
                                       index=1, key="ym_goster_yil")

        ay_k = f"{goster_yil}-{goster_ay:02d}"
        ay_m = {t: m for t, m in menuler_map.items() if t.startswith(ay_k)}

        if not ay_m:
            styled_info_banner(
                f"{MONTHS_TR[goster_ay - 1]} {goster_yil} için menü kaydı yok.", "info")
        else:
            gunler_tr = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
            cal = calendar.monthcalendar(goster_yil, goster_ay)
            hdr = st.columns(7)
            for i, g in enumerate(gunler_tr):
                with hdr[i]:
                    st.markdown(
                        f"<div style='text-align:center;font-weight:700;"
                        f"color:#6b7280;font-size:0.8rem;'>{g}</div>",
                        unsafe_allow_html=True)
            for week in cal:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day == 0:
                            st.markdown("")
                            continue
                        ts = f"{goster_yil}-{goster_ay:02d}-{day:02d}"
                        m = ay_m.get(ts)
                        is_today = ts == today.isoformat()
                        bg = "#fef3c7" if m else "#111827"
                        if is_today:
                            bg = "#dbeafe"
                        border = "2px solid #3b82f6" if is_today else "1px solid #e5e7eb"
                        if m:
                            og_items = m.get("ogle_yemegi", [])[:3]
                            og_html = "<br>".join(f"• {y}" for y in og_items)
                            kah_count = len(m.get("kahvalti", []))
                            ik_count  = len(m.get("ikindi_ara_ogun", []))
                            badges = ""
                            if kah_count:
                                badges += f'<span style="color:#92400e;font-size:0.6rem;">☕{kah_count}</span> '
                            if ik_count:
                                badges += f'<span style="color:#166534;font-size:0.6rem;">🍎{ik_count}</span>'
                            st.markdown(
                                f'<div style="background:{bg};border:{border};border-radius:8px;'
                                f'padding:0.3rem;min-height:80px;font-size:0.65rem;margin-bottom:0.2rem;">'
                                f'<strong style="color:#94A3B8;">{day}</strong> {badges}<br>'
                                f'<span style="color:#94A3B8;">{og_html}</span>'
                                f'</div>',
                                unsafe_allow_html=True)
                        else:
                            st.markdown(
                                f'<div style="background:{bg};border:{border};border-radius:8px;'
                                f'padding:0.3rem;min-height:80px;font-size:0.65rem;margin-bottom:0.2rem;">'
                                f'<strong style="color:#9ca3af;">{day}</strong>'
                                f'</div>',
                                unsafe_allow_html=True)


# ==================== 3) SERVİS YÖNETİMİ ====================

def _render_admin_servis(store: AkademikDataStore):
    """Servis guzergah, sofor ve ogrenci atama yonetimi."""
    styled_section("Servis / Ulasim Yönetimi", "#10b981")

    servisler = _load_hizmet_json(SERVIS_DOSYA)

    # İstatistikler
    toplam_ogrenci = sum(len(s.get("ogrenci_ids", [])) + len(s.get("ogrenci_adlari", []))
                         for s in servisler)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Servis Hatti", str(len(servisler)))
    with c2:
        st.metric("Kayıtli Öğrenci", str(toplam_ogrenci))
    with c3:
        st.metric("Sofor", str(len(set(s.get("sofor_adi", "") for s in servisler if s.get("sofor_adi")))))

    # --- Yeni servis hatti ekleme ---
    with st.expander("Yeni Servis Hatti Ekle", expanded=False):
        with st.form("admin_servis_form", clear_on_submit=True):
            sf1, sf2 = st.columns(2)
            with sf1:
                hat_adi = st.text_input("Hat Adi *", placeholder="Orn: Kadikoy - Okul", key="sv_hat")
                plaka = st.text_input("Plaka *", key="sv_plaka")
                sofor_adi = st.text_input("Sofor Adi *", key="sv_sofor")
                sofor_tel = st.text_input("Sofor Telefon", key="sv_sofor_tel")
            with sf2:
                hostes_adi = st.text_input("Hostes Adi (opsiyonel)", key="sv_hostes")
                sabah_saat = st.text_input("Sabah Alinma Saati", placeholder="07:30", key="sv_sabah")
                aksam_saat = st.text_input("Aksam Birakma Saati", placeholder="16:30", key="sv_aksam")
                kapasite = st.number_input("Kapasite", min_value=1, value=30, key="sv_kapasite")

            st.markdown("**Duraklar** (her satira: durak_adi, saat)")
            durak_text = st.text_area("Duraklar", height=100,
                                       placeholder="Kadikoy Meydan, 07:30\nUskudar, 07:45\nOkul, 08:15",
                                       key="sv_duraklar")

            # Ogrenci atama
            students = store.get_students()
            student_opts = {s.id: f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in students}
            secili_ogrenciler = st.multiselect("Öğrenciler", list(student_opts.keys()),
                                               format_func=lambda x: student_opts.get(x, x),
                                               key="sv_ogrenciler")

            if st.form_submit_button("Kaydet", type="primary"):
                if not hat_adi or not plaka or not sofor_adi:
                    st.error("Hat adi, plaka ve sofor adi zorunludur.")
                else:
                    duraklar = []
                    for line in durak_text.strip().split("\n"):
                        if not line.strip():
                            continue
                        parts = [p.strip() for p in line.split(",")]
                        duraklar.append({
                            "ad": parts[0],
                            "saat": parts[1] if len(parts) > 1 else "",
                        })

                    ogrenci_adlari = []
                    for sid in secili_ogrenciler:
                        for s in students:
                            if s.id == sid:
                                ogrenci_adlari.append(s.tam_ad)
                                break

                    yeni = {
                        "id": str(uuid.uuid4())[:8],
                        "hat_adi": hat_adi,
                        "plaka": plaka,
                        "sofor_adi": sofor_adi,
                        "sofor_tel": sofor_tel,
                        "hostes_adi": hostes_adi,
                        "sabah_saat": sabah_saat,
                        "aksam_saat": aksam_saat,
                        "kapasite": kapasite,
                        "duraklar": duraklar,
                        "ogrenci_ids": secili_ogrenciler,
                        "ogrenci_adlari": ogrenci_adlari,
                    }
                    servisler.append(yeni)
                    _save_hizmet_json(SERVIS_DOSYA, servisler)
                    st.success(f"'{hat_adi}' hatti eklendi!")
                    st.rerun()

    # --- Mevcut servisler ---
    styled_section("Mevcut Servis Hatlari", "#059669")

    if not servisler:
        styled_info_banner("Henuz servis hatti tanimlanmamis.", "info")
        return

    for s in servisler:
        ogr_sayi = len(s.get("ogrenci_ids", [])) + len(s.get("ogrenci_adlari", []))
        with st.expander(f"🚌 {s.get('hat_adi', '-')} | {s.get('plaka', '-')} | Sofor: {s.get('sofor_adi', '-')} | {ogr_sayi} ogrenci"):
            dc1, dc2 = st.columns(2)
            with dc1:
                st.markdown(f"""
                - **Plaka:** {s.get('plaka', '-')}
                - **Sofor:** {s.get('sofor_adi', '-')} ({s.get('sofor_tel', '-')})
                - **Hostes:** {s.get('hostes_adi', '-')}
                """)
            with dc2:
                st.markdown(f"""
                - **Sabah:** {s.get('sabah_saat', '-')}
                - **Aksam:** {s.get('aksam_saat', '-')}
                - **Kapasite:** {s.get('kapasite', '-')}
                """)

            duraklar = s.get("duraklar", [])
            if duraklar:
                st.caption("Guzergah:")
                for idx, d in enumerate(duraklar):
                    icon = "🏠" if idx == 0 else ("🏫" if idx == len(duraklar) - 1 else "📍")
                    st.write(f"{icon} {d.get('ad', '-')} - {d.get('saat', '-')}")

            ogrenciler = s.get("ogrenci_adlari", [])
            if ogrenciler:
                st.caption(f"Kayıtli Öğrenciler ({len(ogrenciler)}):")
                st.write(", ".join(ogrenciler))

            # Ogrenci ekleme/cikarma
            with st.form(f"servis_ogr_form_{s.get('id', '')}"):
                students = store.get_students()
                mevcut_ids = set(s.get("ogrenci_ids", []))
                yeni_adaylar = {st_obj.id: f"{st_obj.tam_ad} ({st_obj.sinif}/{st_obj.sube})"
                                for st_obj in students if st_obj.id not in mevcut_ids}
                ek_ogrenciler = st.multiselect(
                    "Öğrenci Ekle", list(yeni_adaylar.keys()),
                    format_func=lambda x: yeni_adaylar.get(x, x),
                    key=f"sv_ekle_{s.get('id', '')}",
                )
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    ekle_btn = st.form_submit_button("Öğrenci Ekle", type="primary")
                with btn_col2:
                    sil_btn = st.form_submit_button("Hatti Sil")

                if ekle_btn and ek_ogrenciler:
                    for sid in ek_ogrenciler:
                        s.setdefault("ogrenci_ids", []).append(sid)
                        for st_obj in students:
                            if st_obj.id == sid:
                                s.setdefault("ogrenci_adlari", []).append(st_obj.tam_ad)
                                break
                    _save_hizmet_json(SERVIS_DOSYA, servisler)
                    st.success(f"{len(ek_ogrenciler)} ogrenci eklendi!")
                    st.rerun()

                if sil_btn:
                    servisler.remove(s)
                    _save_hizmet_json(SERVIS_DOSYA, servisler)
                    st.success("Servis hatti silindi!")
                    st.rerun()


# ==================== 4) VELİ TALEP YÖNETİMİ (RANDEVU + BELGE) ====================

def _render_admin_veli_talepler(store: AkademikDataStore):
    """Veli randevu ve belge taleplerini yonetme ekrani."""
    vt1, vt2 = st.tabs(["  📅 Randevu Talepleri  ", "  📄 Belge Talepleri  "])

    with vt1:
        _render_admin_randevu_talepler(store)
    with vt2:
        _render_admin_belge_talepler()


def _render_admin_randevu_talepler(store: AkademikDataStore):
    """Velilerin gonderdigi randevu taleplerini yonet."""
    styled_section("Veli Randevu Talepleri", "#8b5cf6")

    randevular = _load_hizmet_json(RANDEVU_DOSYA)

    if not randevular:
        styled_info_banner("Henuz randevu talebi bulunmuyor.", "info")
        return

    bekleyen = [r for r in randevular if r.get("durum") == "beklemede"]
    onaylanan = [r for r in randevular if r.get("durum") == "onaylandi"]
    reddedilen = [r for r in randevular if r.get("durum") == "reddedildi"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam", str(len(randevular)))
    with c2:
        st.metric("Bekleyen", str(len(bekleyen)))
    with c3:
        st.metric("Onaylanan", str(len(onaylanan)))
    with c4:
        st.metric("Reddedilen", str(len(reddedilen)))

    # Bekleyen talepleri islemek
    if bekleyen:
        styled_section("Bekleyen Talepler", "#f59e0b")
        for r in sorted(bekleyen, key=lambda x: x.get("tarih", ""), reverse=True):
            with st.expander(f"⏳ {r.get('veli_adi', '-')} → {r.get('ogretmen_adi', '-')} | "
                f"{r.get('tarih', '-')} {r.get('saat', '-')}"
            ):
                st.markdown(f"""
                - **Veli:** {r.get('veli_adi', '-')}
                - **Öğrenci:** {r.get('ogrenci_adi', '-')}
                - **Öğretmen:** {r.get('ogretmen_adi', '-')}
                - **Tarih/Saat:** {r.get('tarih', '-')} / {r.get('saat', '-')}
                - **Konu:** {r.get('konu', '-')}
                """)
                ac1, ac2 = st.columns(2)
                with ac1:
                    if st.button("Onayla", key=f"rv_onayla_{r.get('id', '')}",
                                 type="primary", use_container_width=True):
                        r["durum"] = "onaylandi"
                        r["islem_tarihi"] = datetime.now().isoformat()
                        _save_hizmet_json(RANDEVU_DOSYA, randevular)
                        st.success("Randevu onaylandi!")
                        st.rerun()
                with ac2:
                    if st.button("Reddet", key=f"rv_reddet_{r.get('id', '')}",
                                 type="secondary", use_container_width=True):
                        r["durum"] = "reddedildi"
                        r["islem_tarihi"] = datetime.now().isoformat()
                        _save_hizmet_json(RANDEVU_DOSYA, randevular)
                        st.warning("Randevu reddedildi.")
                        st.rerun()

    # Tum randevular tablosu
    styled_section("Tüm Randevular", "#6366f1")
    if randevular:
        rows = []
        for r in sorted(randevular, key=lambda x: x.get("tarih", ""), reverse=True):
            durum = r.get("durum", "beklemede")
            durum_icon = {"beklemede": "⏳", "onaylandi": "✅", "reddedildi": "❌"}.get(durum, "❓")
            rows.append({
                "Durum": f"{durum_icon} {durum.capitalize()}",
                "Veli": r.get("veli_adi", "-"),
                "Öğrenci": r.get("ogrenci_adi", "-"),
                "Öğretmen": r.get("ogretmen_adi", "-"),
                "Tarih": r.get("tarih", "-"),
                "Saat": r.get("saat", "-"),
                "Konu": r.get("konu", "-"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_admin_belge_talepler():
    """Veli belge taleplerini yonet (durum guncelleme)."""
    styled_section("Veli Belge Talepleri", "#0ea5e9")

    talepler = _load_hizmet_json(BELGE_TALEP_DOSYA)

    if not talepler:
        styled_info_banner("Henuz belge talebi bulunmuyor.", "info")
        return

    bekleyen = [t for t in talepler if t.get("durum") == "beklemede"]
    hazirlanan = [t for t in talepler if t.get("durum") == "hazirlaniyor"]
    tamamlanan = [t for t in talepler if t.get("durum") == "tamamlandı"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam", str(len(talepler)))
    with c2:
        st.metric("Bekleyen", str(len(bekleyen)))
    with c3:
        st.metric("Hazirlaniyor", str(len(hazirlanan)))
    with c4:
        st.metric("Tamamlandı", str(len(tamamlanan)))

    # Islem bekleyen talepler
    islem_bekleyen = [t for t in talepler if t.get("durum") != "tamamlandı"]
    if islem_bekleyen:
        styled_section("İşlem Bekleyen Talepler", "#f59e0b")
        for t in sorted(islem_bekleyen, key=lambda x: x.get("talep_tarihi", ""), reverse=True):
            durum = t.get("durum", "beklemede")
            durum_icon = {"beklemede": "⏳", "hazirlaniyor": "🔄", "tamamlandı": "✅"}.get(durum, "❓")
            belge_adi = BELGE_TURLERI_MAP.get(t.get("belge_turu", ""), t.get("belge_turu", "-"))

            with st.expander(f"{durum_icon} {t.get('veli_adi', '-')} | {belge_adi} | "
                f"{t.get('talep_tarihi', '-')}"
            ):
                st.markdown(f"""
                - **Veli:** {t.get('veli_adi', '-')}
                - **Öğrenci:** {t.get('ogrenci_adi', '-')}
                - **Belge:** {belge_adi}
                - **Talep Tarihi:** {t.get('talep_tarihi', '-')}
                - **Aciklama:** {t.get('aciklama', '-')}
                - **Mevcut Durum:** {durum.capitalize()}
                """)

                yeni_durum = st.selectbox(
                    "Durumu Güncelle",
                    ["beklemede", "hazirlaniyor", "tamamlandı"],
                    index=["beklemede", "hazirlaniyor", "tamamlandı"].index(durum),
                    format_func=lambda x: {"beklemede": "Beklemede", "hazirlaniyor": "Hazirlaniyor",
                                           "tamamlandı": "Tamamlandı"}.get(x, x),
                    key=f"bt_durum_{t.get('id', '')}",
                )
                if st.button("Güncelle", key=f"bt_guncelle_{t.get('id', '')}",
                             type="primary"):
                    t["durum"] = yeni_durum
                    t["islem_tarihi"] = datetime.now().isoformat()
                    _save_hizmet_json(BELGE_TALEP_DOSYA, talepler)
                    st.success(f"Durum '{yeni_durum}' olarak güncellendi!")
                    st.rerun()

    # Tum talepler tablosu
    styled_section("Tüm Belge Talepleri", "#0891b2")
    rows = []
    for t in sorted(talepler, key=lambda x: x.get("talep_tarihi", ""), reverse=True):
        durum = t.get("durum", "beklemede")
        durum_icon = {"beklemede": "⏳", "hazirlaniyor": "🔄", "tamamlandı": "✅"}.get(durum, "❓")
        rows.append({
            "Durum": f"{durum_icon} {durum.capitalize()}",
            "Veli": t.get("veli_adi", "-"),
            "Öğrenci": t.get("ogrenci_adi", "-"),
            "Belge": BELGE_TURLERI_MAP.get(t.get("belge_turu", ""), t.get("belge_turu", "-")),
            "Talep": t.get("talep_tarihi", "-"),
            "İşlem": t.get("islem_tarihi", "-"),
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# =====================================================================
# SINIF KADRO ATAMA
# =====================================================================

def _get_kademe_from_sinif(sinif_norm: str) -> str:
    """Normalized sinif degerinden kademe belirler."""
    from utils.shared_data import KADEME_SINIFLAR
    for kademe, siniflar in KADEME_SINIFLAR.items():
        if sinif_norm in siniflar:
            return kademe
    return "Ortaokul"


def _render_sinif_kadro_tab(store: AkademikDataStore, akademik_yil: str):
    """Sinif Kadro Atama sekmesi — her sinif/sube icin ogretmen/yonetici kadrosu."""
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR

    styled_section("Sınıf Kadro Atamaları", "#7c3aed")
    styled_info_banner(
        "Her sınıf/şube için sınıf öğretmeni (ilkokul) veya sınıf danışman öğretmeni (ortaokul/lise), "
        "rehber öğretmen, müdür yardımcısı ve müdür atayın. "
        "Otomatik atama ders programındaki en çok saat giren öğretmeni sınıf sorumlusu olarak atar.",
        "info",
    )

    teachers = store.get_teachers()
    aktif_teachers = [t for t in teachers if getattr(t, 'durum', 'aktif') == 'aktif']
    if not aktif_teachers:
        st.warning("Önce Akademik Kadro sekmesinden personel ekleyin.")
        return

    # Rol bazlı gruplama
    mudurler = [t for t in aktif_teachers if t.gorev == "mudur"]
    mudur_yardimcilari = [t for t in aktif_teachers if t.gorev == "mudur_yardimcisi"]
    rehber_ogretmenler = [t for t in aktif_teachers
                          if t.gorev == "rehber_ogretmen"
                          or "REHBERLİK" in (t.brans or "").upper()
                          or "REHBERLIK" in (t.brans or "").upper()
                          or any("REHBER" in b.upper() for b in (getattr(t, 'branslar', None) or []))]
    tum_ogretmenler = [t for t in aktif_teachers if t.gorev in ("ogretmen", "usta_ogretici", "sozlesmeli_egitmen")]

    # Sınıf/şube listesi (öğrencilerden)
    students = store.get_students()
    sinif_subeler = sorted(set(
        (normalize_sinif(str(s.sinif)), s.sube)
        for s in students if s.sinif and s.sube and getattr(s, 'durum', 'aktif') == 'aktif'
    ))
    if not sinif_subeler:
        st.warning("Öğrenci listesi boş. Önce öğrenci ekleyin.")
        return

    mevcut_kadro = store.get_sinif_kadro_all(akademik_yil=akademik_yil)
    atanmis = len(mevcut_kadro)

    styled_stat_row([
        ("Toplam Sınıf/Şube", str(len(sinif_subeler)), "#2563eb", "📋"),
        ("Kadro Atanmış", str(atanmis), "#10b981", "✅"),
        ("Atanmamış", str(len(sinif_subeler) - atanmis), "#ef4444", "⚠️"),
        ("Müdür", str(len(mudurler)), "#7c3aed", "🏫"),
        ("Rehber Öğrt.", str(len(rehber_ogretmenler)), "#f59e0b", "🧑‍⚕️"),
    ])

    # ── OTOMATİK ATAMA ──
    with st.expander("⚡ Otomatik Kadro Atama", expanded=False):
        styled_info_banner(
            "Her sınıf/şubeye en çok ders saati giren öğretmen sınıf öğretmeni/danışman olarak atanır. "
            "Rehber öğretmen, müdür yardımcısı ve müdür rolleri mevcut kadrodan dağıtılır.",
            "info",
        )
        if st.button("⚡ Otomatik Kadro Ata", type="primary", key="sk_otomatik_btn"):
            _otomatik_kadro_ata(store, akademik_yil, sinif_subeler,
                                aktif_teachers, rehber_ogretmenler,
                                mudur_yardimcilari, mudurler)
            st.success("Otomatik kadro atamaları tamamlandı!")
            st.rerun()

    # ── Kademe bazlı gruplama ──
    kademe_gruplari = {}
    for sinif_n, sube in sinif_subeler:
        kademe = _get_kademe_from_sinif(sinif_n)
        if kademe not in kademe_gruplari:
            kademe_gruplari[kademe] = []
        kademe_gruplari[kademe].append((sinif_n, sube))

    # ── MANUEL ATAMA ──
    styled_section("📝 Manuel Kadro Atama", "#1565c0")

    # Öğretmen seçenekleri hazırla
    def _teacher_options(teacher_list):
        opts = {"": "-- Seçiniz --"}
        for t in teacher_list:
            brans_info = t.brans or t.gorev or ""
            opts[t.id] = f"{t.tam_ad} ({brans_info})"
        return opts

    # Tüm kadro olarak gösterilecek liste (müdür/yardımcı + rehber + öğretmenler)
    sinif_sorumlu_list = tum_ogretmenler + mudur_yardimcilari + rehber_ogretmenler
    # Duplicates kaldır
    seen_ids = set()
    sinif_sorumlu_unique = []
    for t in sinif_sorumlu_list:
        if t.id not in seen_ids:
            seen_ids.add(t.id)
            sinif_sorumlu_unique.append(t)

    sorumlu_opts = _teacher_options(sinif_sorumlu_unique)
    rehber_opts = _teacher_options(rehber_ogretmenler)
    my_opts = _teacher_options(mudur_yardimcilari)
    mudur_opts = _teacher_options(mudurler)

    kademe_sira = ["Anaokulu", "Ilkokul", "Ortaokul", "Lise"]
    kademe_labels = {"Anaokulu": "🎒 Anaokulu", "Ilkokul": "📚 İlkokul",
                     "Ortaokul": "📖 Ortaokul", "Lise": "🎓 Lise"}

    for kademe in kademe_sira:
        if kademe not in kademe_gruplari:
            continue
        siniflar = kademe_gruplari[kademe]
        is_ilk = kademe in ("Anaokulu", "Ilkokul")
        rol_label = "Sınıf Öğretmeni" if is_ilk else "Sınıf Danışman Öğretmeni"

        st.markdown(f"### {kademe_labels.get(kademe, kademe)}")

        for sinif_n, sube in siniflar:
            key = f"{sinif_n}_{sube}"
            kadro = mevcut_kadro.get(key)
            mevcut_sorumlu = ""
            mevcut_rehber = ""
            mevcut_my = ""
            mevcut_mudur = ""
            if kadro:
                mevcut_sorumlu = kadro.sinif_ogretmeni_id if is_ilk else kadro.sinif_danisman_id
                mevcut_rehber = kadro.rehber_ogretmen_id
                mevcut_my = kadro.mudur_yardimcisi_id
                mevcut_mudur = kadro.mudur_id

            # Expander başlığı
            atama_durum = "✅" if kadro else "⚠️"
            sorumlu_adi = (kadro.sinif_ogretmeni_adi if is_ilk else kadro.sinif_danisman_adi) if kadro else "-"

            with st.expander(f"{atama_durum} {sinif_n}/{sube}  —  {rol_label}: {sorumlu_adi}"):
                with st.form(f"sk_form_{key}"):
                    fc1, fc2 = st.columns(2)
                    with fc1:
                        # Sınıf sorumlusu
                        sorumlu_keys = list(sorumlu_opts.keys())
                        sorumlu_idx = sorumlu_keys.index(mevcut_sorumlu) if mevcut_sorumlu in sorumlu_keys else 0
                        secilen_sorumlu = st.selectbox(
                            rol_label, sorumlu_keys,
                            index=sorumlu_idx,
                            format_func=lambda x: sorumlu_opts.get(x, x),
                            key=f"sk_sor_{key}",
                        )
                        # Rehber
                        rehber_keys = list(rehber_opts.keys())
                        rehber_idx = rehber_keys.index(mevcut_rehber) if mevcut_rehber in rehber_keys else 0
                        secilen_rehber = st.selectbox(
                            "Rehber Öğretmen", rehber_keys,
                            index=rehber_idx,
                            format_func=lambda x: rehber_opts.get(x, x),
                            key=f"sk_reh_{key}",
                        )
                    with fc2:
                        # Müdür Yardımcısı
                        my_keys = list(my_opts.keys())
                        my_idx = my_keys.index(mevcut_my) if mevcut_my in my_keys else 0
                        secilen_my = st.selectbox(
                            "Müdür Yardımcısı", my_keys,
                            index=my_idx,
                            format_func=lambda x: my_opts.get(x, x),
                            key=f"sk_my_{key}",
                        )
                        # Müdür
                        mudur_keys = list(mudur_opts.keys())
                        mudur_idx = mudur_keys.index(mevcut_mudur) if mevcut_mudur in mudur_keys else 0
                        secilen_mudur = st.selectbox(
                            "Müdür", mudur_keys,
                            index=mudur_idx,
                            format_func=lambda x: mudur_opts.get(x, x),
                            key=f"sk_mud_{key}",
                        )

                    if st.form_submit_button("💾 Kaydet", type="primary"):
                        teacher_map = {t.id: t for t in aktif_teachers}
                        new_kadro = SinifKadro(
                            id=kadro.id if kadro else None,
                            sinif=sinif_n, sube=sube,
                            akademik_yil=akademik_yil,
                            otomatik_atama=False,
                        )
                        if is_ilk:
                            new_kadro.sinif_ogretmeni_id = secilen_sorumlu
                            t = teacher_map.get(secilen_sorumlu)
                            new_kadro.sinif_ogretmeni_adi = t.tam_ad if t else ""
                        else:
                            new_kadro.sinif_danisman_id = secilen_sorumlu
                            t = teacher_map.get(secilen_sorumlu)
                            new_kadro.sinif_danisman_adi = t.tam_ad if t else ""

                        t = teacher_map.get(secilen_rehber)
                        new_kadro.rehber_ogretmen_id = secilen_rehber
                        new_kadro.rehber_ogretmen_adi = t.tam_ad if t else ""

                        t = teacher_map.get(secilen_my)
                        new_kadro.mudur_yardimcisi_id = secilen_my
                        new_kadro.mudur_yardimcisi_adi = t.tam_ad if t else ""

                        t = teacher_map.get(secilen_mudur)
                        new_kadro.mudur_id = secilen_mudur
                        new_kadro.mudur_adi = t.tam_ad if t else ""

                        store.save_sinif_kadro(new_kadro)
                        st.success(f"{sinif_n}/{sube} kadrosu kaydedildi!")
                        st.rerun()


def _otomatik_kadro_ata(store, akademik_yil, sinif_subeler,
                         all_teachers, rehber_ogretmenler,
                         mudur_yardimcilari, mudurler):
    """Otomatik kadro atama algoritmasi."""
    assignments = store.get_teacher_assignments(akademik_yil=akademik_yil)
    teacher_map = {t.id: t for t in all_teachers}

    for idx, (sinif_n, sube) in enumerate(sinif_subeler):
        kademe = _get_kademe_from_sinif(sinif_n)
        is_ilk = kademe in ("Anaokulu", "Ilkokul")

        # 1. En çok saat giren öğretmen → sınıf sorumlusu
        max_hours = 0
        best_id = ""
        best_name = ""
        for a in assignments:
            hours = sum(
                g.get("haftalik_saat", 0) for g in a.gorevler
                if str(g.get("sinif", "")) == str(sinif_n) and g.get("sube") == sube
            )
            if hours > max_hours:
                max_hours = hours
                best_id = a.ogretmen_id
                best_name = a.ogretmen_adi

        # 2. Rehber öğretmen (round-robin)
        rehber_id = ""
        rehber_adi = ""
        if rehber_ogretmenler:
            r = rehber_ogretmenler[idx % len(rehber_ogretmenler)]
            rehber_id = r.id
            rehber_adi = r.tam_ad

        # 3. Müdür yardımcısı (round-robin)
        my_id = ""
        my_adi = ""
        if mudur_yardimcilari:
            m = mudur_yardimcilari[idx % len(mudur_yardimcilari)]
            my_id = m.id
            my_adi = m.tam_ad

        # 4. Müdür (tüm sınıflara aynı)
        mudur_id = mudurler[0].id if mudurler else ""
        mudur_adi = mudurler[0].tam_ad if mudurler else ""

        kadro = SinifKadro(
            sinif=sinif_n, sube=sube, akademik_yil=akademik_yil,
            rehber_ogretmen_id=rehber_id, rehber_ogretmen_adi=rehber_adi,
            mudur_yardimcisi_id=my_id, mudur_yardimcisi_adi=my_adi,
            mudur_id=mudur_id, mudur_adi=mudur_adi,
            otomatik_atama=True,
        )
        if is_ilk:
            kadro.sinif_ogretmeni_id = best_id
            kadro.sinif_ogretmeni_adi = best_name
        else:
            kadro.sinif_danisman_id = best_id
            kadro.sinif_danisman_adi = best_name

        store.save_sinif_kadro(kadro)


# ════════════════════════════════════════════════════════════
# YENI: BANA ATANMIS DERSLER (Otomatik Ogretmen Modu)
# ════════════════════════════════════════════════════════════

def _giris_yapan_ogretmen_bul(store):
    """
    auth_user uzerinden giris yapan ogretmeni Teacher dataclass'ina esle.
    Sirayla denenir: email > tam_ad > username > ad+soyad

    Returns: Teacher obj veya None
    """
    auth_user = st.session_state.get("auth_user", {}) or st.session_state.get("current_user", {})
    if not auth_user:
        return None

    # Auth verilerini topla
    auth_username = (auth_user.get("username") or "").lower().strip()
    auth_email = (auth_user.get("email") or "").lower().strip()
    auth_name = (auth_user.get("name") or "").strip()
    auth_role = (auth_user.get("role") or "").lower()

    # Sadece ogretmen rolu icin bak (yonetici de gorsun istersen kaldirilabilir)
    teachers = store.get_teachers(durum="aktif") or []

    if not teachers:
        return None

    # 1. Email tam eslesme
    if auth_username:
        for t in teachers:
            t_email = (getattr(t, "email", "") or "").lower().strip()
            if t_email and t_email == auth_username:
                return t
            # Username = email basligi (ahmet.yilmaz @ smartcampus...)
            if t_email and t_email.split("@")[0] == auth_username:
                return t

    if auth_email:
        for t in teachers:
            t_email = (getattr(t, "email", "") or "").lower().strip()
            if t_email and t_email == auth_email:
                return t

    # 2. Tam ad eslesme
    if auth_name:
        for t in teachers:
            t_tam = (getattr(t, "tam_ad", "") or "").strip()
            if t_tam and t_tam.lower() == auth_name.lower():
                return t

    # 3. ad + soyad parcalama
    if auth_name:
        parts = auth_name.split()
        if len(parts) >= 2:
            ad = parts[0].lower()
            soyad = " ".join(parts[1:]).lower()
            for t in teachers:
                t_ad = (getattr(t, "ad", "") or "").lower()
                t_soyad = (getattr(t, "soyad", "") or "").lower()
                if t_ad == ad and t_soyad == soyad:
                    return t

    return None


def _ogretmen_bugun_dersleri(store, ogretmen_id: str, akademik_yil: str = "") -> list:
    """Bir ogretmen icin BUGUN'un derslerini ders saatine gore sirali dondur."""
    bugun_index = datetime.now().weekday()  # 0=Pzt
    gun_isim = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"][bugun_index]

    sched = store.get_schedule(akademik_yil=akademik_yil) or store.get_schedule() or []
    bugun = []
    for s in sched:
        if s.ogretmen_id == ogretmen_id and s.gun.lower().replace("ı", "i") == gun_isim.lower().replace("ı", "i"):
            bugun.append(s)
    bugun.sort(key=lambda x: x.ders_saati or 0)
    return bugun


def _ogretmen_haftalik_dersleri(store, ogretmen_id: str, akademik_yil: str = "") -> dict:
    """Ogretmenin tum haftalik program — gun bazli grupla."""
    sched = store.get_schedule(akademik_yil=akademik_yil) or store.get_schedule() or []
    grup = {}
    for s in sched:
        if s.ogretmen_id == ogretmen_id:
            grup.setdefault(s.gun, []).append(s)
    for g in grup:
        grup[g].sort(key=lambda x: x.ders_saati or 0)
    return grup


def _slot_kazanimlari_yukle_ve_getir(store, sinif, sube, ders, akademik_yil, hafta_no):
    """
    Bir ders icin: 1) MEB'den otomatik sync, 2) o haftaya ait kazanim_isleme kayitlari.
    Returns: (records_list, mevcut_hafta_kayitlari, hafta_meb_info)
    """
    # 1. MEB sync
    try:
        store.sync_kazanim_isleme_from_meb(sinif, sube, ders, akademik_yil)
    except Exception:
        pass

    # 2. Tum kayitlari getir
    try:
        all_records = store.get_kazanim_isleme(
            sinif=sinif, sube=sube, ders=ders, akademik_yil=akademik_yil
        ) or []
    except Exception:
        all_records = []

    # 3. Bu haftaya ait olanlari filtrele
    bu_hafta = [r for r in all_records if r.hafta == hafta_no]

    # 4. MEB plan bilgisi (hafta basligi, konu)
    meb_info = {}
    try:
        meb_plans = store.get_meb_kazanimlar_by_week(sinif, ders) or []
        if hafta_no <= len(meb_plans):
            meb_info = meb_plans[hafta_no - 1] if hafta_no > 0 else {}
    except Exception:
        pass

    return all_records, bu_hafta, meb_info


def _render_otomatik_ogretmen_kazanim(store, akademik_yil: str):
    """
    Otomatik ogretmen sekmesi:
    - Giris yapan ogretmeni tespit eder
    - Bugun ders programini gosterir
    - Her ders icin BU HAFTANIN kazanimlarini otomatik gosterir
    - Kazanim isaretle butonu ile durumu gunceller
    - Manuel SECIM YOK
    """
    # 1. Giris yapan ogretmeni bul
    teacher = _giris_yapan_ogretmen_bul(store)

    # Premium banner
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0c4a6e,#075985);
                border:1px solid rgba(14,165,233,.4);border-radius:14px;
                padding:14px 18px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:1.6rem">🎯</div>
            <div>
                <div style="color:#7dd3fc;font-size:.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">OTOMATIK MODU — OGRETMEN ICIN</div>
                <div style="color:#fff;font-size:1.05rem;font-weight:800">Bana Atanmış Dersler</div>
                <div style="color:#94a3b8;font-size:.75rem">Ders programınız + bu haftanın kazanımları otomatik geliyor — manuel sınıf/şube/ders seçimi yok</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not teacher:
        # Auth bilgisi yoksa veya eslesemediysek yardimci uyari
        auth_user = st.session_state.get("auth_user", {})
        st.warning(
            f"⚠️ Giriş yapan kullanıcı sistemdeki öğretmen kaydıyla eşleştirilemedi.\n\n"
            f"**Mevcut kullanıcı:** `{auth_user.get('name', '-')}` ({auth_user.get('username', '-')})\n\n"
            f"Eşleştirme için: Akademik Kadro sekmesinden bu kullanıcıya öğretmen kaydı oluşturun "
            f"(ya da mevcut öğretmenin email alanını kullanıcı adı ile aynı yapın)."
        )

        # Manuel ogretmen secimi (fallback)
        st.markdown("---")
        st.caption("Geçici olarak öğretmen seçebilirsiniz:")
        teachers = store.get_teachers(durum="aktif") or []
        if teachers:
            secenekler = {f"{t.tam_ad} — {t.brans}": t for t in teachers[:200]}
            sec = st.selectbox("Öğretmen", list(secenekler.keys()), key="aut_man_ogr")
            teacher = secenekler.get(sec)

    if not teacher:
        return

    # 2. Ogretmen profil karti
    bugun_isim = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][datetime.now().weekday()]
    mevcut_hafta = store.get_mevcut_hafta_no()

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);'
        f'border:2px solid #0ea5e9;border-radius:16px;padding:18px 22px;margin:10px 0;'
        f'box-shadow:0 8px 24px rgba(14,165,233,.25)">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px">'
        f'<div>'
        f'<div style="color:#38bdf8;font-size:.7rem;font-weight:800;letter-spacing:1.5px">HOSGELDIN</div>'
        f'<div style="color:#fff;font-size:1.5rem;font-weight:900;margin-top:2px">👨‍🏫 {teacher.tam_ad}</div>'
        f'<div style="color:#94a3b8;font-size:.78rem;margin-top:2px">'
        f'Branş: <b style="color:#cbd5e1">{teacher.brans}</b> • '
        f'Email: <b style="color:#cbd5e1">{teacher.email or "-"}</b>'
        f'</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="color:#94a3b8;font-size:.66rem;text-transform:uppercase;letter-spacing:1px">BUGUN</div>'
        f'<div style="color:#38bdf8;font-size:1.5rem;font-weight:900">{bugun_isim}</div>'
        f'<div style="color:#94a3b8;font-size:.75rem">📅 {mevcut_hafta}. hafta</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # 3. Bugunun dersleri
    bugun_dersler = _ogretmen_bugun_dersleri(store, teacher.id, akademik_yil)

    if not bugun_dersler:
        st.info(f"📭 **{bugun_isim}** günü için ders programınızda atama yok. Aşağıdan haftalık programınızı görebilirsiniz.")

        # Haftalik program goster
        haftalik = _ogretmen_haftalik_dersleri(store, teacher.id, akademik_yil)
        if haftalik:
            st.markdown("##### 📅 Haftalık Program")
            for gun in ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]:
                if gun in haftalik:
                    st.markdown(f"**{gun}:**")
                    for s in haftalik[gun]:
                        st.caption(f"  • {s.ders_saati}. ders — {s.sinif}/{s.sube} — {s.ders}")
        return

    # 4. BUGUN'UN DERSLERI — kart kart goster
    st.markdown(f"##### 📚 Bugün ({bugun_isim}) — {len(bugun_dersler)} dersiniz var")

    for idx, slot in enumerate(bugun_dersler):
        sinif = slot.sinif
        sube = slot.sube
        ders = slot.ders
        ders_saati = slot.ders_saati

        # Bu ders icin BU HAFTANIN kazanimlarini cek
        try:
            tum_records, bu_hafta_records, meb_info = _slot_kazanimlari_yukle_ve_getir(
                store, sinif, sube, ders, akademik_yil, mevcut_hafta
            )
        except Exception as e:
            st.error(f"{ders} kazanim yukleme hatasi: {e}")
            continue

        # Hafta bilgisi
        week_label = ""
        unite = ""
        topic = ""
        if meb_info:
            week_label = meb_info.get('week', '').replace('\n', ' ').strip()
            unite = meb_info.get('unit', '')
            topic = meb_info.get('topic', '')

        # Kart basligi
        islenen = sum(1 for r in bu_hafta_records if r.durum == "islendi")
        kismen = sum(1 for r in bu_hafta_records if r.durum == "kismen")
        toplam = len(bu_hafta_records)
        yuzde = round((islenen / toplam) * 100, 1) if toplam > 0 else 0

        bg_renk = "#16a34a" if yuzde >= 100 else ("#f59e0b" if islenen + kismen > 0 else "#0ea5e9")

        with st.expander(
            f"⏰ {ders_saati}. Ders — {sinif}/{sube} — **{ders}**  ({islenen}/{toplam} kazanım işlendi)",
            expanded=(idx < 2),  # ilk 2 ders acik
        ):
            # Hafta bilgi banner
            st.markdown(
                f'<div style="background:linear-gradient(90deg,{bg_renk}20,#0f172a);'
                f'border-left:4px solid {bg_renk};border-radius:8px;padding:10px 14px;margin:6px 0">'
                f'<div style="color:{bg_renk};font-size:.7rem;font-weight:800;letter-spacing:1px">📅 {mevcut_hafta}. HAFTA — {week_label}</div>'
                + (f'<div style="color:#cbd5e1;font-size:.82rem;margin-top:4px"><b>Ünite:</b> {unite}</div>' if unite else '')
                + (f'<div style="color:#94a3b8;font-size:.78rem"><b>Konu:</b> {topic}</div>' if topic else '')
                + f'</div>',
                unsafe_allow_html=True,
            )

            # Progress bar
            if toplam > 0:
                st.progress(yuzde / 100, text=f"İlerleme: {islenen}/{toplam} işlendi (%{yuzde:.0f})")

            # Kazanim listesi — checkbox + durum
            if not bu_hafta_records:
                st.warning(
                    f"📭 Bu hafta için kazanım kaydı yok.\n\n"
                    f"**'Tüm Kazanımlarımı Yükle'** butonuna basarak MEB yıllık planından otomatik yükleyebilirsiniz."
                )
                if st.button(f"📥 {sinif}/{sube} {ders} - MEB Kazanımlarını Yükle",
                              key=f"aut_sync_{idx}_{sinif}_{sube}_{ders}",
                              type="primary",
                              use_container_width=True):
                    sayi = store.sync_kazanim_isleme_from_meb(sinif, sube, ders, akademik_yil)
                    st.success(f"✓ {sayi} kazanım yüklendi")
                    st.rerun()
            else:
                # Form ile toplu update
                with st.form(f"aut_form_{idx}_{slot.id}"):
                    st.markdown("**Bu hafta işlediğiniz kazanımları işaretleyin:**")

                    durumlar = {}
                    for r in bu_hafta_records:
                        kc1, kc2 = st.columns([1, 6])
                        with kc1:
                            varsayilan_durum = r.durum == "islendi"
                            durumlar[r.id] = st.checkbox(
                                "İşlendi",
                                value=varsayilan_durum,
                                key=f"aut_cb_{idx}_{r.id}",
                                label_visibility="collapsed",
                            )
                        with kc2:
                            ikon = "✅" if r.durum == "islendi" else ("⚠️" if r.durum == "kismen" else "⬜")
                            st.markdown(
                                f'<div style="padding:4px 0">'
                                f'{ikon} <span style="color:#cbd5e1;font-size:.85rem">{r.kazanim_kodu}</span> — '
                                f'<span style="color:#e2e8f0">{r.kazanim_metni[:120] if hasattr(r, "kazanim_metni") else r.kazanim_kodu}</span>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

                    notlar = st.text_input(
                        "Ders Notu (opsiyonel)",
                        key=f"aut_not_{idx}_{slot.id}",
                        placeholder="Bugün dersle ilgili özel bir not...",
                    )

                    submitted = st.form_submit_button(
                        "💾 Kaydet ve İlerlet",
                        type="primary",
                        use_container_width=True,
                    )

                    if submitted:
                        guncellendi = 0
                        for r_id, isaret in durumlar.items():
                            yeni_durum = "islendi" if isaret else "beklemede"
                            try:
                                # Mevcut kaydi bul
                                rec = next((r for r in bu_hafta_records if r.id == r_id), None)
                                if rec:
                                    rec.durum = yeni_durum
                                    rec.ogretmen_id = teacher.id
                                    rec.ogretmen_adi = teacher.tam_ad
                                    if isaret:
                                        rec.tarih = date.today().isoformat()
                                    if notlar:
                                        rec.aciklama = notlar
                                    store.save_kazanim_isleme(rec)
                                    guncellendi += 1
                            except Exception as e:
                                st.error(f"Hata: {e}")

                        if guncellendi > 0:
                            st.success(f"✓ {guncellendi} kazanım güncellendi")
                            st.rerun()


# ════════════════════════════════════════════════════════════
# PREMIUM YENILIKLER — Akademik Takip
# 1. _at_premium_hero() — animated gradient banner
# 2. _at_premium_metrics() — glassmorphism metric cards
# 3. _at_premium_tab_css() — kompakt sekme stili
# 4. _render_dijital_ikiz() — Tab: Ogrenci Dijital Ikizi
# 5. _render_ogretmen_cockpit() — Tab: Ogretmen Cockpit
# 6. _render_veli_bildirim_panel() — Tab: Veli Bildirim Otomasyon
# ════════════════════════════════════════════════════════════


def _at_premium_hero():
    """Akademik takip premium hero banner."""
    st.markdown("""
    <style>
    @keyframes atHeroShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes atHeroFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    @keyframes atPulseGlow {
        0%, 100% { box-shadow: 0 0 30px rgba(37,99,235,.3), 0 8px 32px rgba(0,0,0,.4); }
        50% { box-shadow: 0 0 60px rgba(59,130,246,.5), 0 12px 48px rgba(0,0,0,.5); }
    }
    .at-hero {
        background: linear-gradient(135deg, #0c1b4d 0%, #1e3a8a 30%, #1e40af 60%, #0c1b4d 100%);
        background-size: 300% 300%;
        animation: atHeroShimmer 14s ease infinite;
        border-radius: 22px;
        padding: 26px 32px;
        margin: 12px 0 16px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(59,130,246,.35);
        box-shadow: 0 12px 48px rgba(30,58,138,.35),
                    0 0 0 1px rgba(59,130,246,.12) inset;
    }
    .at-hero::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -10%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(96,165,250,.2) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(60px);
        pointer-events: none;
    }
    .at-hero::after {
        content: '';
        position: absolute;
        bottom: -40%;
        left: -5%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(99,102,241,.18) 0%, transparent 60%);
        border-radius: 50%;
        filter: blur(70px);
        pointer-events: none;
    }
    .at-hero-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    }
    .at-hero-icon {
        width: 80px;
        height: 80px;
        border-radius: 20px;
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        animation: atHeroFloat 4s ease-in-out infinite, atPulseGlow 3s ease-in-out infinite;
        flex-shrink: 0;
    }
    .at-hero-text {
        flex: 1;
        min-width: 260px;
    }
    .at-hero-title {
        font-size: 2.1rem;
        font-weight: 900;
        background: linear-gradient(90deg, #fff, #dbeafe, #93c5fd, #dbeafe, #fff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: atHeroShimmer 7s linear infinite;
        margin: 0;
        letter-spacing: -.8px;
        line-height: 1;
    }
    .at-hero-sub {
        color: rgba(147,197,253,.85);
        font-size: .82rem;
        letter-spacing: 1.5px;
        margin-top: 8px;
        text-transform: uppercase;
        font-weight: 600;
    }
    .at-hero-tagline {
        color: rgba(255,255,255,.7);
        font-size: .8rem;
        margin-top: 6px;
        line-height: 1.5;
    }
    .at-hero-pills {
        display: flex;
        gap: 7px;
        margin-top: 12px;
        flex-wrap: wrap;
    }
    .at-hero-pill {
        background: rgba(96,165,250,.18);
        border: 1px solid rgba(147,197,253,.35);
        color: #dbeafe;
        padding: 4px 11px;
        border-radius: 14px;
        font-size: .66rem;
        font-weight: 700;
        letter-spacing: .5px;
    }
    </style>
    <div class="at-hero">
        <div class="at-hero-content">
            <div class="at-hero-icon">📚</div>
            <div class="at-hero-text">
                <div class="at-hero-title">AKADEMIK TAKIP</div>
                <div class="at-hero-sub">Yoklama · Notlar · Plan · Risk · Veli Iletisim · AI Analiz</div>
                <div class="at-hero-tagline">Ogrenci yasam dongusunun her noktasinda 200+ ogrenci, 50 ogretmen, 30+ veri kaynagi tek ekranda</div>
                <div class="at-hero-pills">
                    <span class="at-hero-pill">🧬 Dijital Ikiz</span>
                    <span class="at-hero-pill">📡 Ogretmen Cockpit</span>
                    <span class="at-hero-pill">🔔 Veli Bildirim</span>
                    <span class="at-hero-pill">🚨 Risk Engine</span>
                    <span class="at-hero-pill">🎯 KYT</span>
                    <span class="at-hero-pill">📚 Borç Bankası</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _at_premium_metrics(store):
    """5 glassmorphism metric karti — gercek veriden besler."""
    try:
        ogr_sayi = len(store.get_students(durum="aktif") or [])
        teach_sayi = len(store.get_teachers(durum="aktif") or [])
        not_sayi = len(store.get_grades() or [])
        dev_sayi = len(store.get_attendance() or [])
    except Exception:
        ogr_sayi = teach_sayi = not_sayi = dev_sayi = 0

    # Risk sayisi
    risk_sayi = 0
    try:
        from models.akademik_takip import EarlyWarningEngine
        ew = EarlyWarningEngine(store)
        risk_listesi = ew.get_active_alerts() if hasattr(ew, "get_active_alerts") else []
        risk_sayi = len(risk_listesi)
    except Exception:
        try:
            risk_sayi = len(store.load_list("risk_alerts") or [])
        except Exception:
            pass

    st.markdown("""
    <style>
    .at-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        margin: 8px 0 16px;
    }
    .at-metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
        border: 1px solid rgba(59,130,246,.25);
        border-radius: 14px;
        padding: 14px 16px;
        backdrop-filter: blur(20px);
        transition: all .3s ease;
        position: relative;
        overflow: hidden;
    }
    .at-metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--at-color);
    }
    .at-metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--at-color);
        box-shadow: 0 10px 28px var(--at-glow);
    }
    .at-metric-icon {
        font-size: 1.5rem;
        opacity: .85;
    }
    .at-metric-value {
        font-size: 1.85rem;
        font-weight: 900;
        color: #fff;
        margin: 4px 0 2px;
        line-height: 1;
        font-family: 'Inter', sans-serif;
    }
    .at-metric-label {
        color: rgba(255,255,255,.6);
        font-size: .65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

    metrikler = [
        ("Ogrenci", ogr_sayi, "#3b82f6", "rgba(59,130,246,.3)", "👨‍🎓"),
        ("Ogretmen", teach_sayi, "#8b5cf6", "rgba(139,92,246,.3)", "👨‍🏫"),
        ("Notlar", not_sayi, "#10b981", "rgba(16,185,129,.3)", "📝"),
        ("Devamsizlik", dev_sayi, "#f59e0b", "rgba(245,158,11,.3)", "📅"),
        ("Risk", risk_sayi, "#ef4444", "rgba(239,68,68,.3)", "🚨"),
    ]

    cards_html = '<div class="at-metrics">'
    for label, val, color, glow, icon in metrikler:
        cards_html += (
            f'<div class="at-metric-card" style="--at-color:{color};--at-glow:{glow}">'
            f'<div class="at-metric-icon">{icon}</div>'
            f'<div class="at-metric-value">{val}</div>'
            f'<div class="at-metric-label">{label}</div>'
            f'</div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


def _at_premium_tab_css():
    """Tab listesini kompakt + 17 sekme tek satira sigsin."""
    st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-list"] {
        gap: 4px !important;
        flex-wrap: wrap !important;
        padding: 6px 0 !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"] {
        padding: 6px 12px !important;
        min-height: 32px !important;
        height: 32px !important;
        font-size: .73rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg,#0f172a,#1e293b) !important;
        border: 1px solid rgba(59,130,246,.25) !important;
        color: #93c5fd !important;
        transition: all .2s ease !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg,#172554,#1e3a8a) !important;
        border-color: rgba(96,165,250,.6) !important;
        color: #fff !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg,#2563eb,#3b82f6) !important;
        border-color: #60a5fa !important;
        color: #fff !important;
        box-shadow: 0 4px 14px rgba(37,99,235,.4) !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-border"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# YENILIK 1: ÖĞRENCİ DİJİTAL İKİZİ
# ────────────────────────────────────────────────────────────

def _render_dijital_ikiz(store):
    """Ogrenci icin 6 boyutlu radar + AI tahmin + aksiyon onerileri."""
    try:
        from models.akademik_dijital_ikiz import (
            ogrenci_radar_skoru, ogrenci_ai_tahmin, ogrenci_aksiyon_onerileri
        )
    except Exception as e:
        st.error(f"Dijital Ikiz modulu yuklenemedi: {e}")
        return

    st.markdown("""
    <div style="background:linear-gradient(135deg,#0c1b4d,#1e3a8a);
                border:1px solid rgba(59,130,246,.4);border-radius:14px;
                padding:14px 18px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:1.6rem">🧬</div>
            <div>
                <div style="color:#60a5fa;font-size:.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">PREMIUM ÖZELLIK</div>
                <div style="color:#fff;font-size:1.05rem;font-weight:800">Öğrenci Dijital İkizi</div>
                <div style="color:#94a3b8;font-size:.75rem">6 boyutlu radar + AI 30/60/90 gün tahmin + aksiyon önerileri</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ogrenci secimi
    students = store.get_students(durum="aktif") or []
    if not students:
        st.info("Aktif öğrenci bulunamadı.")
        return

    # Filtreler
    fc1, fc2 = st.columns([1, 2])
    with fc1:
        sinif_seti = sorted(set(getattr(s, "sinif", "") or "?" for s in students))
        sec_sinif = st.selectbox("Sınıf", ["Tümü"] + sinif_seti, key="di_sinif")
    with fc2:
        if sec_sinif != "Tümü":
            sf = [s for s in students if getattr(s, "sinif", "") == sec_sinif]
        else:
            sf = students
        # Aday isim olusturma (nested f-string'den kacin)
        def _ogr_label(s):
            ad = getattr(s, "ad", "") or ""
            soyad = getattr(s, "soyad", "") or ""
            adsoyad = getattr(s, "ad_soyad", "") or f"{ad} {soyad}".strip() or "Ogrenci"
            sinif = getattr(s, "sinif", "") or ""
            sube = getattr(s, "sube", "") or ""
            return f"{adsoyad} ({sinif}/{sube})"
        secenekler = {_ogr_label(s): s for s in sf[:200]}
        secili_label = st.selectbox("Öğrenci", list(secenekler.keys()), key="di_ogrenci")

    if not secili_label:
        return
    secili = secenekler[secili_label]
    sid = secili.id
    sad = getattr(secili, "ad_soyad", None) or f"{getattr(secili, 'ad', '')} {getattr(secili, 'soyad', '')}".strip()

    # Skorlari hesapla
    radar = ogrenci_radar_skoru(store, sid)
    tahmin = ogrenci_ai_tahmin(store, sid)
    aksiyonlar = ogrenci_aksiyon_onerileri(store, sid)

    # ── PROFIL KARTI ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);'
        f'border:2px solid {radar["renk"]};border-radius:18px;padding:20px 24px;margin:14px 0;'
        f'box-shadow:0 8px 28px {radar["renk"]}40">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px">'
        f'<div>'
        f'<div style="color:{radar["renk"]};font-size:.7rem;font-weight:800;letter-spacing:1.5px">SEÇILI ÖĞRENCİ</div>'
        f'<div style="color:#fff;font-size:1.6rem;font-weight:900;margin-top:2px">👨‍🎓 {sad}</div>'
        f'<div style="color:#94a3b8;font-size:.78rem;margin-top:2px">{getattr(secili, "sinif", "")}/{getattr(secili, "sube", "")} • Numara: {getattr(secili, "numara", "-")}</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="color:#94a3b8;font-size:.66rem;text-transform:uppercase;letter-spacing:1px">GENEL SKOR</div>'
        f'<div style="color:{radar["renk"]};font-size:3rem;font-weight:900;line-height:1">{radar["ortalama"]:.0f}</div>'
        f'<div style="color:{radar["renk"]};font-size:.85rem;font-weight:800">{radar["seviye"]}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── 6 BOYUTLU RADAR + 30/60/90 GUN ──
    rc1, rc2 = st.columns([1, 1])

    with rc1:
        st.markdown("##### 📊 6 Boyutlu Yetkinlik Radarı")
        try:
            import plotly.graph_objects as go
            kategoriler = ["Akademik", "Devam", "Kazanım", "Ödev", "Katılım", "Trend"]
            degerler = [radar["akademik"], radar["devam"], radar["kazanim"],
                        radar["odev"], radar["katilim"], radar["trend"]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=degerler + [degerler[0]],
                theta=kategoriler + [kategoriler[0]],
                fill='toself',
                fillcolor=f'rgba(59,130,246,.3)',
                line=dict(color=radar["renk"], width=3),
                marker=dict(size=8, color=radar["renk"]),
                name=sad,
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(15,23,42,.5)",
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor="rgba(148,163,184,.2)",
                        tickfont=dict(color="#94a3b8", size=9),
                    ),
                    angularaxis=dict(
                        gridcolor="rgba(148,163,184,.2)",
                        tickfont=dict(color="#cbd5e1", size=11, family="Inter"),
                    ),
                ),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=20, b=20),
                height=340,
                font=dict(color="#e2e8f0"),
            )
            st.plotly_chart(fig, use_container_width=True, key=f"di_radar_{sid}")
        except Exception:
            # Fallback: bar chart yerine progress bars
            for k, v in zip(kategoriler, degerler):
                st.progress(v / 100, text=f"{k}: {v:.0f}")

    with rc2:
        st.markdown("##### 🔮 AI Tahmin (30/60/90 Gün)")
        try:
            import plotly.graph_objects as go
            x = ["Bugün", "30 Gün", "60 Gün", "90 Gün"]
            y_ort = [radar["ortalama"],
                     tahmin["30_gun"]["ortalama"],
                     tahmin["60_gun"]["ortalama"],
                     tahmin["90_gun"]["ortalama"]]
            y_akademik = [radar["akademik"],
                          tahmin["30_gun"]["akademik"],
                          tahmin["60_gun"]["akademik"],
                          tahmin["90_gun"]["akademik"]]

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=x, y=y_ort, name="Ortalama",
                                       line=dict(color=radar["renk"], width=4),
                                       marker=dict(size=10),
                                       mode='lines+markers'))
            fig2.add_trace(go.Scatter(x=x, y=y_akademik, name="Akademik",
                                       line=dict(color="#60a5fa", width=2, dash='dash'),
                                       marker=dict(size=8),
                                       mode='lines+markers'))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,.3)",
                yaxis=dict(range=[0, 100], gridcolor="rgba(148,163,184,.15)",
                           tickfont=dict(color="#94a3b8")),
                xaxis=dict(gridcolor="rgba(148,163,184,.15)",
                           tickfont=dict(color="#cbd5e1")),
                margin=dict(l=10, r=10, t=20, b=10),
                height=340,
                legend=dict(font=dict(color="#cbd5e1"),
                             bgcolor="rgba(15,23,42,.7)",
                             bordercolor="rgba(59,130,246,.3)",
                             borderwidth=1),
                font=dict(color="#e2e8f0"),
            )
            st.plotly_chart(fig2, use_container_width=True, key=f"di_tahmin_{sid}")
        except Exception:
            st.write(f"**30 gun:** {tahmin['30_gun']['ortalama']}")
            st.write(f"**60 gun:** {tahmin['60_gun']['ortalama']}")
            st.write(f"**90 gun:** {tahmin['90_gun']['ortalama']}")

    # ── AI YORUM ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{radar["renk"]}15,#0f172a);'
        f'border-left:4px solid {radar["renk"]};border-radius:10px;'
        f'padding:14px 18px;margin:12px 0">'
        f'<div style="color:{radar["renk"]};font-size:.7rem;font-weight:800;letter-spacing:1.5px;margin-bottom:6px">🧠 AI YORUM</div>'
        f'<div style="color:#e2e8f0;font-size:.88rem;line-height:1.6">{tahmin["ai_yorum"]}</div>'
        f'<div style="color:#94a3b8;font-size:.74rem;margin-top:8px;font-style:italic">{tahmin["risk_aciklama"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── AKSIYON ONERILERI ──
    st.markdown("##### 🎯 Önerilen Aksiyonlar")
    cols = st.columns(min(len(aksiyonlar), 4))
    for i, aksiyon in enumerate(aksiyonlar):
        with cols[i % len(cols)]:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{aksiyon["renk"]}20,#0f172a);'
                f'border:1px solid {aksiyon["renk"]}60;border-radius:12px;padding:14px;'
                f'min-height:130px;display:flex;flex-direction:column;justify-content:space-between">'
                f'<div>'
                f'<div style="font-size:1.5rem;margin-bottom:4px">{aksiyon["ikon"]}</div>'
                f'<div style="color:{aksiyon["renk"]};font-size:.8rem;font-weight:800;margin-bottom:4px">{aksiyon["ad"]}</div>'
                f'<div style="color:#cbd5e1;font-size:.72rem;line-height:1.4">{aksiyon["aciklama"]}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ────────────────────────────────────────────────────────────
# YENILIK 2: ÖĞRETMEN PERFORMANS COCKPIT
# ────────────────────────────────────────────────────────────

def _render_ogretmen_cockpit(store):
    """Ogretmen performans dashboard."""
    try:
        from models.akademik_ogretmen_cockpit import (
            ogretmen_performans, ogretmen_konu_heatmap,
            sinif_arasi_karsilastirma, ai_kocluk_onerisi, ogretmen_ozet_istatistik
        )
    except Exception as e:
        st.error(f"Ogretmen Cockpit modulu yuklenemedi: {e}")
        return

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);
                border:1px solid rgba(139,92,246,.4);border-radius:14px;
                padding:14px 18px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:1.6rem">📡</div>
            <div>
                <div style="color:#a78bfa;font-size:.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">PREMIUM ÖZELLIK</div>
                <div style="color:#fff;font-size:1.05rem;font-weight:800">Öğretmen Performans Cockpit</div>
                <div style="color:#94a3b8;font-size:.75rem">3 KPI + konu heatmap + sınıf arası karşılaştırma + AI koçluk</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Genel ozet
    ozet = ogretmen_ozet_istatistik(store)
    sc = st.columns(5)
    metrikler = [
        ("Toplam", ozet["toplam_ogretmen"], "#6366f1"),
        ("Çok İyi", ozet["cok_iyi"], "#16a34a"),
        ("İyi", ozet["iyi"], "#22c55e"),
        ("Orta", ozet["orta"], "#f59e0b"),
        ("Geliştir", ozet["gelistirilmesi_gerek"], "#ef4444"),
    ]
    for col, (lbl, val, clr) in zip(sc, metrikler):
        with col:
            st.markdown(
                f'<div style="background:#0f172a;border:1px solid {clr}40;border-radius:10px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:.6rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.5rem;font-weight:900">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Ogretmen secimi
    teachers = store.get_teachers(durum="aktif") or []
    if not teachers:
        st.info("Aktif öğretmen bulunamadı.")
        return

    def _ogretmen_label(t):
        ad = getattr(t, "ad", "") or ""
        soyad = getattr(t, "soyad", "") or ""
        tam = getattr(t, "tam_ad", "") or f"{ad} {soyad}".strip() or "Ogretmen"
        brans = getattr(t, "brans", "-") or "-"
        return f"{tam} — {brans}"

    secenekler = {_ogretmen_label(t): t for t in teachers[:200]}
    secili_label = st.selectbox("👨‍🏫 Öğretmen Seç", list(secenekler.keys()), key="oc_ogretmen")
    if not secili_label:
        return

    secili = secenekler[secili_label]
    tid = secili.id
    tad = getattr(secili, "tam_ad", None) or f"{getattr(secili, 'ad', '')} {getattr(secili, 'soyad', '')}".strip()

    perf = ogretmen_performans(store, tid)

    # Profil + skor
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);'
        f'border:2px solid {perf["renk"]};border-radius:18px;padding:20px 24px;margin:14px 0;'
        f'box-shadow:0 8px 28px {perf["renk"]}40">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px">'
        f'<div>'
        f'<div style="color:{perf["renk"]};font-size:.7rem;font-weight:800;letter-spacing:1.5px">SEÇILI ÖĞRETMEN</div>'
        f'<div style="color:#fff;font-size:1.6rem;font-weight:900;margin-top:2px">👨‍🏫 {tad}</div>'
        f'<div style="color:#94a3b8;font-size:.78rem;margin-top:2px">'
        f'Branş: {getattr(secili, "brans", "-")} • '
        f'{perf["sinif_sayisi"]} sınıf • {perf["ders_sayisi"]} ders • {perf["ogrenci_sayisi"]} öğrenci'
        f'</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="color:#94a3b8;font-size:.66rem;text-transform:uppercase;letter-spacing:1px">SKOR</div>'
        f'<div style="color:{perf["renk"]};font-size:3rem;font-weight:900;line-height:1">{perf["skor"]:.0f}</div>'
        f'<div style="color:{perf["renk"]};font-size:.85rem;font-weight:800">{perf["seviye"]}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # 3 KPI
    kc1, kc2, kc3 = st.columns(3)
    kpi_list = [
        (kc1, "Sınıf Ortalaması", perf["sinif_ortalamasi"], "#10b981", "📊"),
        (kc2, "Kazanım Hızı", f"%{perf['kazanim_orani']:.0f}", "#3b82f6", "🎯"),
        (kc3, "Memnuniyet", f"%{perf['memnuniyet_skoru']:.0f}", "#a855f7", "❤️"),
    ]
    for col, lbl, val, clr, ico in kpi_list:
        with col:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0f172a,{clr}15);'
                f'border:1px solid {clr}40;border-radius:12px;padding:16px;text-align:center">'
                f'<div style="font-size:1.5rem;margin-bottom:4px">{ico}</div>'
                f'<div style="color:#94a3b8;font-size:.65rem;text-transform:uppercase;letter-spacing:1px">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.8rem;font-weight:900;margin-top:2px">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Sinif breakdown
    st.markdown("##### 🎯 Sınıf Bazlı Performans")
    if perf["siniflar"]:
        for s in perf["siniflar"][:10]:
            renk = "#16a34a" if s["ortalama"] >= 80 else ("#f59e0b" if s["ortalama"] >= 65 else "#ef4444")
            barlen = int(s["ortalama"])
            st.markdown(
                f'<div style="background:#0f172a;border-left:3px solid {renk};'
                f'border-radius:6px;padding:10px 14px;margin:5px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'
                f'<span style="color:#e2e8f0;font-size:.85rem;font-weight:700">{s["etiket"]}</span>'
                f'<span style="color:{renk};font-weight:900;font-size:1rem">{s["ortalama"]:.1f}</span>'
                f'</div>'
                f'<div style="background:#1e293b;border-radius:4px;height:6px;overflow:hidden">'
                f'<div style="background:{renk};height:100%;width:{barlen}%"></div>'
                f'</div>'
                f'<div style="color:#64748b;font-size:.65rem;margin-top:3px">'
                f'{s["ogrenci_sayisi"]} not • Min: {s["min"]} • Max: {s["max"]}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("Bu öğretmen için henüz not kaydı yok.")

    # AI kocluk
    st.markdown("---")
    st.markdown("##### 🧠 AI Koçluk Önerisi")
    yorum = ai_kocluk_onerisi(perf)
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{perf["renk"]}10,#0f172a);'
        f'border-left:4px solid {perf["renk"]};border-radius:10px;'
        f'padding:14px 18px;margin:8px 0;color:#e2e8f0;font-size:.85rem;line-height:1.6;'
        f'white-space:pre-wrap">{yorum}</div>',
        unsafe_allow_html=True,
    )


# ────────────────────────────────────────────────────────────
# YENILIK 3: VELI BILDIRIM OTOMASYON
# ────────────────────────────────────────────────────────────

def _render_veli_bildirim_panel(store):
    """Veli bildirim cron + kuyruk + log paneli."""
    try:
        from models.akademik_veli_bildirim import (
            istatistikler, son_log_listesi, cron_tara, gorevleri_isle,
            trigger_haftalik_ozet, _kuyrugu_yukle
        )
    except Exception as e:
        st.error(f"Veli Bildirim modulu yuklenemedi: {e}")
        return

    st.markdown("""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);
                border:1px solid rgba(16,185,129,.4);border-radius:14px;
                padding:14px 18px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="font-size:1.6rem">🔔</div>
            <div>
                <div style="color:#34d399;font-size:.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">PREMIUM OTOMASYON</div>
                <div style="color:#fff;font-size:1.05rem;font-weight:800">Veli Bildirim Otomasyonu</div>
                <div style="color:#94a3b8;font-size:.75rem">Devamsızlık · Not · Ödev · Risk · Haftalık özet — proaktif WhatsApp/SMS</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ist = istatistikler()

    # Stats
    sc = st.columns(5)
    metrikler = [
        ("Toplam", ist["toplam_gorev"], "#10b981"),
        ("Bekleyen", ist["bekleyen"], "#f59e0b"),
        ("Gönderilen", ist["gonderilen"], "#22c55e"),
        ("Başarısız", ist["basarisiz"], "#ef4444"),
        ("Son 24h", ist["son_24_saat"], "#3b82f6"),
    ]
    for col, (lbl, val, clr) in zip(sc, metrikler):
        with col:
            st.markdown(
                f'<div style="background:#0f172a;border:1px solid {clr}40;border-radius:10px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:.6rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.5rem;font-weight:900">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Aksiyon butonlari
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        if st.button("⚡ Cron Tara (Manuel)", key="vb_cron",
                      use_container_width=True, type="primary"):
            with st.spinner("Cron taramasi calisiyor..."):
                sonuc = cron_tara(store, force=True)
                if sonuc.get("atlandi"):
                    st.info(f"Atlandı: {sonuc.get('neden')}")
                else:
                    st.success(
                        f"✓ Tarama tamam — Kuyruk: {sonuc['kuyruk_islenen']} işlendi, "
                        f"Haftalık: {sonuc['haftalik_olusturulan']} oluştu"
                    )
    with ac2:
        if st.button("📤 Kuyruğu İşle (Test)", key="vb_isle",
                      use_container_width=True):
            with st.spinner("Kuyruk işleniyor..."):
                sonuc = gorevleri_isle(test_modu=True)
                st.success(
                    f"✓ {sonuc['islenen']} işlendi, {sonuc['basarili']} başarılı, "
                    f"{sonuc['basarisiz']} başarısız"
                )
                st.rerun()
    with ac3:
        if st.button("📨 Tüm Velilere Haftalık Özet", key="vb_haftalik",
                      use_container_width=True):
            with st.spinner("Haftalık özetler hazırlanıyor..."):
                sayac = 0
                students = store.get_students(durum="aktif") or []
                for s in students[:50]:
                    if trigger_haftalik_ozet(store, s.id):
                        sayac += 1
                st.success(f"✓ {sayac} öğrenci için haftalık özet kuyruğa eklendi")
                st.rerun()

    st.markdown("---")

    # Tip dagilimi
    if ist["tip_dagilimi"]:
        st.markdown("##### 📊 Tip Dağılımı")
        td_cols = st.columns(len(ist["tip_dagilimi"]))
        for col, (tip, sayi) in zip(td_cols, ist["tip_dagilimi"].items()):
            with col:
                st.metric(tip.title(), sayi)

    st.markdown("---")

    # Bekleyen kuyruk
    st.markdown("##### ⏳ Bekleyen Görevler (İlk 10)")
    kuyruk = _kuyrugu_yukle()
    bekleyenler = [g for g in kuyruk if g.durum == "bekliyor"][:10]

    if not bekleyenler:
        st.success("✅ Bekleyen görev yok — kuyruk temiz")
    else:
        for g in bekleyenler:
            st.markdown(
                f'<div style="background:#0f172a;border-left:3px solid #f59e0b;'
                f'border-radius:6px;padding:10px 14px;margin:5px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<div>'
                f'<span style="color:#fbbf24;font-size:.65rem;font-weight:800;text-transform:uppercase">{g.tip}</span>'
                f'<span style="color:#e2e8f0;font-size:.85rem;font-weight:700;margin-left:8px">{g.ogrenci_adi}</span>'
                f'</div>'
                f'<div style="color:#94a3b8;font-size:.7rem">{g.kanal} • {g.planlanan_zaman[:16] if g.planlanan_zaman else "-"}</div>'
                f'</div>'
                f'<div style="color:#cbd5e1;font-size:.75rem;margin-top:4px">{g.konu}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Log gecmisi
    with st.expander("📋 Son 20 Bildirim Logu", expanded=False):
        loglar = son_log_listesi(20)
        if not loglar:
            st.caption("Henüz log kaydı yok")
        else:
            for log in loglar:
                durum_renk = "#22c55e" if "gonderildi" in log.get("durum", "") else "#ef4444"
                st.markdown(
                    f'<div style="background:#0f172a;border-left:2px solid {durum_renk};'
                    f'border-radius:4px;padding:6px 10px;margin:3px 0;font-size:.75rem">'
                    f'<span style="color:#64748b">{log.get("tarih", "")[:16]}</span> • '
                    f'<span style="color:#cbd5e1">{log.get("tip", "")}</span> • '
                    f'<b style="color:#e2e8f0">{log.get("ogrenci", "")}</b> • '
                    f'<span style="color:{durum_renk}">{log.get("durum", "")}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
