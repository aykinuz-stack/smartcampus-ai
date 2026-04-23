"""
Ogrenci & Veli Paneli
=====================
Veli ve Ogrenci rolleri için ozel giris ekranlari.
- Veli: Ozet kartlar + 16 sekme + tam ozellikli Smarti AI asistan + zengin grafikler
- Ogrenci: Tam bilgi paneli + KYT soru cozme + Smarti AI asistan
"""

import base64
import hashlib
import io
import json
import os
import random
import uuid
import calendar
import streamlit as st
import streamlit.components.v1 as _stc

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("default")
except Exception:
    pass
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

from utils.auth import AuthManager
from models.akademik_takip import (
    AkademikDataStore, get_akademik_store, Student,
    KYTSoru, KYTCevap, VeliMesaj,
    KYT_DERSLER, _get_kademe,
    MESAJ_KATEGORILERI,
    MUDAHALE_TIPLERI, ONERI_KATEGORILERI, ONERI_ONCELIKLERI,
    RISK_SEVERITY_LABELS, RISK_SEVERITY_COLORS,
    DESTEK_PLANI_DURUMLARI,
    OdevTeslim,
    Odev,
    KazanimIsleme,
    KazanimBorc, KazanimBorcEngine,
    BORC_NEDENI_LABELS, KAPANMA_NEDENLERI,
)
from models.olcme_degerlendirme import DataStore as OlcmeDataStore
from models.okul_sagligi import SaglikDataStore
from models.rehberlik import RehberlikDataStore
from models.veli_memnuniyet import (
    VeliAnketDataStore, AnketCevap, AnketYorum,
    ANKET_KATEGORILERI, KATEGORI_IKONLARI, KATEGORI_RENKLER,
    LIKERT_OLCEK,
)
from utils.tenant import get_tenant_dir, get_data_path
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG

# ===================== GRAFIK RENK PALETI (EXCEL SUNBURST STIL) =====================

# Ana palet: Mavi, Altin, Turuncu, Gri + acik tonlari
CHART_COLORS = [
    "#4472C4", "#FFC000", "#ED7D31", "#A5A5A5",
    "#5B9BD5", "#FFD966", "#F4B183", "#BFBFBF",
    "#2F5597", "#BF8F00", "#C55A11", "#7F7F7F",
    "#8FAADC", "#FFE699", "#F7CBAC", "#D9D9D9",
]
CHART_BG = "rgba(0,0,0,0)"
CHART_FONT = dict(family="Segoe UI, sans-serif", color="#333333")
CHART_LAYOUT = dict(
    paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
    font=CHART_FONT, margin=dict(l=20, r=20, t=40, b=20),
    height=380,
)


# ===================== SINAV TÜRÜ GÖRSEL MAPPING =====================
# (label, text_color, bg_color)
EXAM_TYPE_DISPLAY = {
    "1. Donem 1. Yazili": ("Okul Yazılısı", "#1e3a5f", "#e8ecf4"),
    "1. Donem 2. Yazili": ("Okul Yazılısı", "#1e3a5f", "#e8ecf4"),
    "2. Donem 1. Yazili": ("Okul Yazılısı", "#1e3a5f", "#e8ecf4"),
    "2. Donem 2. Yazili": ("Okul Yazılısı", "#1e3a5f", "#e8ecf4"),
    "1. Donem 1. Proje": ("Proje", "#0f766e", "#e0f7f0"),
    "1. Donem 2. Proje": ("Proje", "#0f766e", "#e0f7f0"),
    "2. Donem 1. Proje": ("Proje", "#0f766e", "#e0f7f0"),
    "2. Donem 2. Proje": ("Proje", "#0f766e", "#e0f7f0"),
    "Kazanim Değerlendirme": ("Kazanım Ölçme", "#92400e", "#FFF8E1"),
    "Deneme": ("Deneme Sınavı", "#7c3aed", "#f3e8ff"),
    "LGS": ("LGS", "#dc2626", "#fef2f2"),
    "TYT": ("TYT", "#2563eb", "#eff6ff"),
    "AYT Esit Agirlik": ("AYT-EA", "#059669", "#ecfdf5"),
    "AYT Sayısal": ("AYT-SAY", "#d97706", "#fffbeb"),
    "AYT Sozel": ("AYT-SÖZ", "#9333ea", "#faf5ff"),
    "Quiz": ("Quiz", "#C8952E", "#FFF8E1"),
}


def _exam_type_badge_html(exam_type: str) -> str:
    """Sınav türü için renkli pill HTML badge döndürür."""
    label, color, bg = EXAM_TYPE_DISPLAY.get(exam_type, (exam_type or "Sınav", "#64748b", "#1A2035"))
    return (f'<span style="display:inline-block;background:{bg};color:{color};'
            f'padding:2px 10px;border-radius:10px;font-size:0.72rem;font-weight:700;'
            f'border:1px solid {color}20;margin-left:8px;">{label}</span>')


def _kazanim_breakdown_html(outcome_breakdown: dict, outcome_cache: dict) -> str:
    """Kazanım bazlı doğru/yanlış HTML tablosu döndürür."""
    if not outcome_breakdown:
        return ""
    rows = ""
    idx = 0
    for oid, perf in outcome_breakdown.items():
        total = perf.get("total", 0)
        correct = perf.get("correct", 0)
        wrong = perf.get("wrong", 0)
        pct = round((correct / total) * 100) if total > 0 else 0
        # Renk
        if pct >= 85:
            badge_bg, badge_color = "#eff6ff", "#2563eb"
        elif pct >= 70:
            badge_bg, badge_color = "#ecfdf5", "#059669"
        elif pct >= 50:
            badge_bg, badge_color = "#fffbeb", "#d97706"
        else:
            badge_bg, badge_color = "#fef2f2", "#dc2626"
        # Kazanım metni
        kaz_text = outcome_cache.get(oid, oid)
        if len(kaz_text) > 60:
            kaz_text = kaz_text[:57] + "..."
        # Zebra
        row_bg = "#FFFDF5" if idx % 2 == 0 else "#ffffff"
        rows += f"""<tr style="background:{row_bg};">
            <td style="padding:5px 10px;font-size:0.78rem;color:#475569;border-bottom:1px solid #e2e8f0;
                max-width:280px;word-wrap:break-word;">{kaz_text}</td>
            <td style="padding:5px 8px;text-align:center;font-size:0.82rem;font-weight:700;
                color:#16a34a;border-bottom:1px solid #e2e8f0;">{correct}</td>
            <td style="padding:5px 8px;text-align:center;font-size:0.82rem;font-weight:700;
                color:#dc2626;border-bottom:1px solid #e2e8f0;">{wrong}</td>
            <td style="padding:5px 8px;text-align:center;font-size:0.82rem;color:#64748b;
                border-bottom:1px solid #e2e8f0;">{total}</td>
            <td style="padding:5px 8px;text-align:center;border-bottom:1px solid #e2e8f0;">
                <span style="background:{badge_bg};color:{badge_color};padding:2px 8px;
                    border-radius:8px;font-size:0.72rem;font-weight:700;">%{pct}</span></td>
        </tr>"""
        idx += 1
    th_style = ('padding:6px 10px;text-align:center;font-size:0.7rem;font-weight:700;'
                'color:#475569;text-transform:uppercase;letter-spacing:0.5px;'
                'border-bottom:2px solid #C8952E;background:#FFFDF5;')
    th_left = th_style.replace("text-align:center", "text-align:left")
    return f"""<div style="margin-top:4px;border-top:2px solid #C8952E;border-radius:0 0 8px 8px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;">
            <thead><tr>
                <th style="{th_left}">Kazanım</th>
                <th style="{th_style}">D</th>
                <th style="{th_style}">Y</th>
                <th style="{th_style}">Top</th>
                <th style="{th_style}">Başarı</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def _apply_chart_layout(fig, title: str = "", height: int = 380):
    """Grafiklere ortak layout uygula - Excel sunburst stili."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#94A3B8", family="Segoe UI, sans-serif")),
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        font=CHART_FONT, margin=dict(l=30, r=30, t=55, b=25),
        height=height,
        legend=dict(font=dict(size=11, family="Segoe UI, sans-serif"),
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E0E0", borderwidth=1),
    )
    return fig


# ===================== STİL FONKSİYONLARI =====================

def _inject_panel_tab_css():
    """Tab'larin satirlara sarmasini saglayan CSS."""
    inject_common_css("panel")


def _inject_veli_premium_css():
    """Veli paneli — temiz, okunabilir, sade light tema."""
    if st.session_state.get("_veli_premium_css_injected"):
        return
    st.session_state["_veli_premium_css_injected"] = True

    st.markdown("""
<style>
/* ═══ VELI PANELI — TEMIZ LIGHT TEMA v5 ═══ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Temiz beyaz arka plan */
html, body, .stApp, .main, section.main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}
[data-testid="stHeader"] { background: #f8fafc !important; }

/* Tum yazilar koyu — okunabilir */
.stApp p, .stApp span, .stApp div, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp li, .stApp td, .stApp th { color: #1e293b !important; }

/* Basliklar */
.stApp h1 { font-size: 1.6rem !important; font-weight: 700 !important; color: #0f172a !important; }
.stApp h2 { font-size: 1.3rem !important; font-weight: 700 !important; color: #1e293b !important; }
.stApp h3 { font-size: 1.1rem !important; font-weight: 600 !important; color: #334155 !important; }

/* Butonlar — sade */
.stButton > button {
    background: #ffffff !important; color: #1e293b !important;
    border: 1px solid #e2e8f0 !important; border-radius: 10px !important;
    font-weight: 600 !important; box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
}
.stButton > button:hover { border-color: #6366f1 !important; box-shadow: 0 2px 6px rgba(99,102,241,.12) !important; }
.stButton > button[kind="primary"] { background: #6366f1 !important; color: #fff !important; border: none !important; }
.stButton > button[kind="primary"]:hover { background: #4f46e5 !important; }

/* Input alanlari */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input,
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
    background: #ffffff !important; color: #1e293b !important;
    border: 1px solid #e2e8f0 !important; border-radius: 8px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 2px rgba(99,102,241,.1) !important; }
.stSelectbox label, .stTextInput label, .stTextArea label { color: #475569 !important; font-weight: 600 !important; }

/* Tabs — sade, okunabilir */
div[data-testid="stTabs"] > div:first-child { gap: 4px !important; }
button[data-baseweb="tab"] {
    background: #ffffff !important; color: #475569 !important;
    border: 1px solid #e2e8f0 !important; border-radius: 10px !important;
    font-weight: 600 !important; padding: 8px 16px !important; font-size: 0.85rem !important;
}
button[data-baseweb="tab"]:hover { border-color: #6366f1 !important; color: #4338ca !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    background: #6366f1 !important; color: #ffffff !important;
    border-color: #6366f1 !important; box-shadow: 0 2px 8px rgba(99,102,241,.25) !important;
}
button[data-baseweb="tab"][aria-selected="true"] *, button[data-baseweb="tab"][aria-selected="true"] p { color: #ffffff !important; }
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }

/* Expander — temiz kart */
[data-testid="stExpander"] > details {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; box-shadow: 0 1px 3px rgba(0,0,0,.04) !important;
}
[data-testid="stExpander"] summary { color: #1e293b !important; font-weight: 700 !important; }
[data-testid="stExpander"] > details > div { background: #fafbff !important; color: #1e293b !important; }

/* Metric — temiz kart */
[data-testid="stMetric"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; padding: 16px !important; box-shadow: 0 1px 3px rgba(0,0,0,.04) !important;
}
[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 600 !important; }

/* Tablo — beyaz arka plan */
[data-testid="stDataFrame"], [data-testid="stTable"] { background: #ffffff !important; border-radius: 10px !important; }
.stDataFrame th { background: #f1f5f9 !important; color: #334155 !important; font-weight: 700 !important; }
.stDataFrame td { color: #1e293b !important; }

/* Radio / Checkbox — okunabilir */
.stRadio label, .stCheckbox label { color: #1e293b !important; font-weight: 500 !important; }
.stRadio [data-baseweb="radio"] { color: #6366f1 !important; }

/* Sidebar gizle (veli icin gereksiz) */
section[data-testid="stSidebar"] { display: none !important; }

/* Uyari/info banner'lari */
.stAlert { border-radius: 10px !important; }

/* Veli hero header */
.vp-hero {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 16px; padding: 24px; color: white;
    box-shadow: 0 4px 16px rgba(99,102,241,.2);
}
.vp-hero * { color: white !important; }
.vp-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: rgba(255,255,255,.2); display: flex; align-items: center;
    justify-content: center; font-size: 1.6rem; font-weight: 800; color: white;
    border: 3px solid rgba(255,255,255,.4);
}
.vp-welcome-name { font-size: 1.6rem; font-weight: 800; }
.vp-subtitle { opacity: .8; font-size: .9rem; }
.vp-date-box {
    background: rgba(255,255,255,.15); border-radius: 12px; padding: 8px 14px;
    font-size: .8rem; text-align: center;
}

/* Kart stilleri */
.vp-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,.04); margin-bottom: 12px;
}
.vp-card-title { font-weight: 700; color: #0f172a; font-size: 1rem; margin-bottom: 8px; }
.vp-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: .75rem; font-weight: 700;
}
.vp-badge-green { background: #dcfce7; color: #166534; }
.vp-badge-red { background: #fee2e2; color: #991b1b; }
.vp-badge-yellow { background: #fef3c7; color: #92400e; }
.vp-badge-blue { background: #dbeafe; color: #1e40af; }
.vp-badge-purple { background: #f3e8ff; color: #6b21a8; }

/* Mobile optimize */
@media (max-width: 768px) {
    .vp-hero { padding: 20px 18px; }
    .vp-avatar { width: 56px; height: 56px; font-size: 1.3rem; }
    .vp-welcome-name { font-size: 1.3rem; }
    .vp-date-box { display: none; }
}
</style>
""", unsafe_allow_html=True)


def _render_veli_premium_hero(student, auth_user):
    """Premium veli paneli hero header — \u00f6\u011frenci avatar + ho\u015fgeldin + tarih.

    \u00d6\u011frenci ad-soyad ba\u015f harfleri b\u00fcy\u00fck avatar olarak g\u00f6sterilir,
    veli ad\u0131 ile ki\u015fiselle\u015ftirilmi\u015f selam, sa\u011f\u0131nda canl\u0131 tarih kutusu.
    """
    from datetime import date as _date
    today = _date.today()

    saat = datetime.now().hour
    if saat < 6:
        selamlama = "\u0130yi geceler"
        emoji = "\U0001f319"
    elif saat < 12:
        selamlama = "G\u00fcnayd\u0131n"
        emoji = "\u2600\ufe0f"
    elif saat < 17:
        selamlama = "\u0130yi g\u00fcnler"
        emoji = "\U0001f324\ufe0f"
    elif saat < 21:
        selamlama = "\u0130yi ak\u015famlar"
        emoji = "\U0001f306"
    else:
        selamlama = "\u0130yi geceler"
        emoji = "\U0001f319"

    veli_ad = (auth_user.get("name") or "Sayın Veli").strip()
    initials = ""
    try:
        initials = (student.ad[0] if student.ad else "?") + (student.soyad[0] if student.soyad else "?")
        initials = initials.upper()
    except Exception:
        initials = "??"

    aylar_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    gunler_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    gun_no = today.day
    ay_adi = aylar_tr[today.month - 1]
    gun_adi = gunler_tr[today.weekday()]

    sinif_text = f"{student.sinif}/{student.sube}"
    no_text = student.numara or "—"

    st.markdown(
        f'<div class="vp-hero">'
        f'<div class="vp-hero-inner">'
        f'<div class="vp-avatar">{initials}</div>'
        f'<div class="vp-welcome">'
        f'<div class="vp-welcome-greeting">{emoji} {selamlama}, {veli_ad}</div>'
        f'<div class="vp-welcome-name">{student.ad} {student.soyad}</div>'
        f'<div class="vp-welcome-meta">'
        f'<span class="vp-welcome-meta-item">📚 <b>{sinif_text}</b></span>'
        f'<span class="vp-welcome-meta-item">🎓 No: <b>{no_text}</b></span>'
        f'</div>'
        f'</div>'
        f'<div class="vp-date-box">'
        f'<div class="vp-date-day">{gun_no}</div>'
        f'<div class="vp-date-month">{ay_adi}</div>'
        f'<div class="vp-date-weekday">{gun_adi}</div>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ===================== PREMIUM ÜST KARTLAR (AI Briefing + 360 + Quick Actions) =====================

def _render_veli_ai_briefing(store, student, auth_user, od=None):
    """AI G\u00fcn\u00fcn \u00d6zeti Kart\u0131 — bug\u00fcn icin en \u00f6nemli 4 madde.

    Veli sayfaya girdigi an "bana en \u00f6nemli sey ne?" cevab\u0131n\u0131 al\u0131r.
    Mevcut akademik veriden h\u0131zl\u0131 ozet \u00fcretir (AI kullanmaz, deterministik).
    """
    from datetime import date as _date, timedelta

    veli_ad = (auth_user.get("name") or "Sayın Veli").strip()
    bugun = _date.today()

    # Hizli veri toplama
    bullet_items = []  # (icon, color, text)

    # 1) Devamsizlik
    try:
        attendance = store.get_attendance(student_id=student.id) or []
        bugun_dev = [a for a in attendance if getattr(a, "tarih", "") == bugun.isoformat()]
        if not bugun_dev:
            bullet_items.append(("✅", "#10b981", "Bugün okula tam katıldı, ders performansı iyi"))
        else:
            bullet_items.append(("⚠️", "#f59e0b", f"Bugün {len(bugun_dev)} ders devamsızlık tespit edildi"))
    except Exception:
        bullet_items.append(("✅", "#10b981", "Bugün okula tam katıldı"))

    # 2) Son sinav / not
    try:
        grades = store.get_grades(student_id=student.id) or []
        son_grades = sorted(
            [g for g in grades if getattr(g, "puan", 0) and g.puan > 0],
            key=lambda x: getattr(x, "tarih", "") or "",
            reverse=True,
        )
        if son_grades:
            son = son_grades[0]
            puan = son.puan
            ders = getattr(son, "ders", "Genel")
            # Trend hesabi (varsa)
            ayni_ders = [g for g in son_grades if getattr(g, "ders", "") == ders][:2]
            if len(ayni_ders) >= 2:
                fark = ayni_ders[0].puan - ayni_ders[1].puan
                trend = f" ({'+' if fark >= 0 else ''}{fark:.0f} {'↑' if fark >= 0 else '↓'})"
            else:
                trend = ""
            icon = "🥇" if puan >= 90 else ("📊" if puan >= 70 else "📉")
            color = "#10b981" if puan >= 70 else "#f59e0b"
            bullet_items.append((icon, color, f"{ders} dersinden {puan:.0f} aldı{trend}"))
    except Exception:
        pass

    # 3) Bekleyen odev
    try:
        odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif") or []
        teslimleri = store.get_odev_teslimleri(student_id=student.id) or []
        teslim_ids = {t.odev_id for t in teslimleri if t.durum == "teslim_edildi"}
        bekleyen = [o for o in odevler if o.id not in teslim_ids]
        if bekleyen:
            bullet_items.append(("📝", "#f59e0b",
                f"{len(bekleyen)} bekleyen ödev var (en yakın: {bekleyen[0].baslik})"))
        else:
            bullet_items.append(("📝", "#10b981", "Tüm ödevler güncel, eksik yok"))
    except Exception:
        pass

    # 4) KYT performans
    try:
        akademik_yil = _get_akademik_yil()
        kyt_analiz = store.get_kyt_ogrenci_analizi(
            student_id=student.id, akademik_yil=akademik_yil
        )
        if kyt_analiz and kyt_analiz.get("toplam", 0) > 0:
            basari = kyt_analiz.get("basari_yuzde", 0)
            bullet_items.append(("🎯", "#8b5cf6",
                f"KYT başarı oranı %{basari:.0f} ({kyt_analiz.get('toplam', 0)} test)"))
    except Exception:
        pass

    # En fazla 4 madde
    bullet_items = bullet_items[:4]

    # Render — LIGHT MODERN
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#ffffff 0%,#f0f9ff 50%,#eff6ff 100%);'
        f'border-radius:20px;padding:22px 26px;margin-bottom:14px;'
        f'box-shadow:0 1px 3px rgba(15,23,42,.04),0 8px 24px rgba(59,130,246,.08),'
        f'0 16px 48px rgba(99,102,241,.06);'
        f'border:1px solid rgba(191,219,254,.6);position:relative;overflow:hidden;">'
        f'<div style="position:absolute;top:-80px;right:-60px;width:240px;height:240px;'
        f'background:radial-gradient(circle,rgba(96,165,250,.18) 0%,transparent 70%);'
        f'border-radius:50%;filter:blur(50px);pointer-events:none"></div>'
        f'<div style="position:relative;z-index:1">'
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">'
        f'<div style="width:44px;height:44px;border-radius:14px;'
        f'background:linear-gradient(135deg,#3b82f6,#6366f1);'
        f'display:flex;align-items:center;justify-content:center;'
        f'box-shadow:0 6px 16px rgba(59,130,246,.3),inset 0 1px 0 rgba(255,255,255,.3);'
        f'flex-shrink:0">'
        f'<span style="font-size:1.4rem">🤖</span></div>'
        f'<div>'
        f'<div style="font-size:.72rem;color:#3b82f6;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:1px">AI Günün Özeti</div>'
        f'<div style="font-size:1.05rem;font-weight:800;color:#0f172a;margin-top:1px">'
        f'Sayın {veli_ad}, bugün {student.ad} için</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    if bullet_items:
        for icon, color, text in bullet_items:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;'
                f'background:rgba(255,255,255,.7);border:1px solid rgba(226,232,240,.7);'
                f'border-left:4px solid {color};'
                f'border-radius:0 12px 12px 0;padding:11px 16px;margin-bottom:7px;'
                f'box-shadow:0 1px 3px rgba(15,23,42,.04),0 4px 12px rgba(99,102,241,.04);'
                f'transition:transform .2s,box-shadow .2s">'
                f'<div style="width:34px;height:34px;border-radius:10px;'
                f'background:{color}15;display:flex;align-items:center;'
                f'justify-content:center;flex-shrink:0">'
                f'<span style="font-size:1.1rem">{icon}</span></div>'
                f'<span style="color:#1e293b;font-size:.9rem;font-weight:600;line-height:1.4">{text}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div style="color:#64748b;font-size:.85rem;padding:8px 0">'
            'Bugün için özet bilgi henüz hazır değil. Veriler yüklendikçe burada görünecek.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div></div>', unsafe_allow_html=True)


def _render_veli_360_snapshot(store, student, od=None):
    """\u00c7ocuk 360\u00b0 Snapshot Kart\u0131 — Plotly radar grafik + ba\u015far\u0131lar/uyar\u0131lar.

    6 boyut: Akademik, Sosyal, Sa\u011fl\u0131k, \u00d6dev, Devam, Davran\u0131\u015f
    """
    import plotly.graph_objects as go

    # Boyut hesaplari
    boyutlar = {}

    # 1) Akademik (notlar ortalamasi)
    try:
        grades = store.get_grades(student_id=student.id) or []
        puanlar = [g.puan for g in grades if getattr(g, "puan", 0) > 0]
        boyutlar["Akademik"] = round(sum(puanlar) / len(puanlar), 1) if puanlar else 70
    except Exception:
        boyutlar["Akademik"] = 70

    # 2) Devam (devamsizlik = 0 -> 100, her gunluk -2)
    try:
        attendance = store.get_attendance(student_id=student.id) or []
        boyutlar["Devam"] = max(0, 100 - len(attendance) * 2)
    except Exception:
        boyutlar["Devam"] = 100

    # 3) Odev (teslim oran)
    try:
        odevler = store.get_odevler(sinif=student.sinif, sube=student.sube) or []
        teslimleri = store.get_odev_teslimleri(student_id=student.id) or []
        teslim_edilen = sum(1 for t in teslimleri if getattr(t, "durum", "") == "teslim_edildi")
        toplam_t = len(teslimleri)
        boyutlar["Ödev"] = round(teslim_edilen / toplam_t * 100, 0) if toplam_t > 0 else 80
    except Exception:
        boyutlar["Ödev"] = 80

    # 4) Sosyal (rehberlik vakalar yoksa yuksek)
    try:
        from models.rehberlik import RehberlikDataStore
        rs = RehberlikDataStore()
        vakalar = [v for v in rs.load_list("vaka_kayitlari")
                   if v.get("ogrenci_id") == student.id]
        boyutlar["Sosyal"] = max(50, 100 - len(vakalar) * 10)
    except Exception:
        boyutlar["Sosyal"] = 80

    # 5) Saglik (revir ziyaret yoksa yuksek)
    try:
        sstore = _get_saglik_store()
        ziyaretler = sstore.find_by_field("revir_ziyaretleri", "ogrenci_id", student.id) or []
        boyutlar["Sağlık"] = max(60, 100 - len(ziyaretler) * 5)
    except Exception:
        boyutlar["Sağlık"] = 90

    # 6) Davranis (default 85)
    boyutlar["Davranış"] = 85

    # Genel ortalama
    genel = round(sum(boyutlar.values()) / len(boyutlar), 1)

    # Render — LIGHT MODERN
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#ffffff 0%,#faf5ff 50%,#fdf4ff 100%);'
        f'border-radius:20px;padding:20px 26px;margin-bottom:14px;'
        f'box-shadow:0 1px 3px rgba(15,23,42,.04),0 8px 24px rgba(168,85,247,.08),'
        f'0 16px 48px rgba(124,58,237,.06);'
        f'border:1px solid rgba(216,180,254,.5);position:relative;overflow:hidden">'
        f'<div style="position:absolute;top:-80px;left:-60px;width:240px;height:240px;'
        f'background:radial-gradient(circle,rgba(168,85,247,.15) 0%,transparent 70%);'
        f'border-radius:50%;filter:blur(50px);pointer-events:none"></div>'
        f'<div style="position:relative;z-index:1;display:flex;align-items:center;gap:12px;margin-bottom:6px">'
        f'<div style="width:44px;height:44px;border-radius:14px;'
        f'background:linear-gradient(135deg,#a855f7,#ec4899);'
        f'display:flex;align-items:center;justify-content:center;'
        f'box-shadow:0 6px 16px rgba(168,85,247,.3),inset 0 1px 0 rgba(255,255,255,.3);'
        f'flex-shrink:0">'
        f'<span style="font-size:1.4rem">🎯</span></div>'
        f'<div style="flex:1">'
        f'<div style="font-size:.72rem;color:#a855f7;font-weight:700;'
        f'text-transform:uppercase;letter-spacing:1px">360° Performans</div>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#0f172a;margin-top:1px">'
        f'{student.ad}\'nin Genel Görünümü · '
        f'<span style="background:linear-gradient(120deg,#a855f7,#ec4899);'
        f'-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;'
        f'color:transparent">{genel}/100</span></div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    rc1, rc2 = st.columns([3, 2])
    with rc1:
        # Plotly radar — LIGHT THEME
        kategoriler = list(boyutlar.keys()) + [list(boyutlar.keys())[0]]
        degerler = list(boyutlar.values()) + [list(boyutlar.values())[0]]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=degerler,
            theta=kategoriler,
            fill="toself",
            fillcolor="rgba(168,85,247,0.18)",
            line=dict(color="#a855f7", width=3),
            marker=dict(size=10, color="#ec4899",
                         line=dict(color="#fff", width=2)),
            name=student.ad,
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0)",
                radialaxis=dict(visible=True, range=[0, 100],
                                gridcolor="rgba(168,85,247,0.15)",
                                tickfont=dict(color="#64748b", size=10),
                                tickcolor="rgba(168,85,247,0.2)"),
                angularaxis=dict(gridcolor="rgba(168,85,247,0.18)",
                                  tickfont=dict(color="#1e1b4b", size=12,
                                                family="Inter"))
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20),
            height=290,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with rc2:
        # En yuksek 3 (basari) ve en dusuk 2 (uyari) — LIGHT THEME
        sorted_boyutlar = sorted(boyutlar.items(), key=lambda x: x[1], reverse=True)
        st.markdown(
            '<div style="color:#059669;font-weight:800;font-size:.78rem;margin-bottom:8px;'
            'text-transform:uppercase;letter-spacing:.8px;display:flex;align-items:center;gap:6px">'
            '<span style="font-size:1rem">✨</span> EN GÜÇLÜ ALANLAR</div>',
            unsafe_allow_html=True,
        )
        for boyut, deger in sorted_boyutlar[:3]:
            st.markdown(
                f'<div style="background:linear-gradient(90deg,rgba(16,185,129,.08),rgba(16,185,129,.02));'
                f'border:1px solid rgba(16,185,129,.2);border-left:3px solid #10b981;'
                f'border-radius:0 10px 10px 0;padding:8px 12px;margin-bottom:6px;'
                f'box-shadow:0 1px 3px rgba(16,185,129,.06);'
                f'display:flex;justify-content:space-between;align-items:center">'
                f'<span style="font-size:.85rem;color:#0f172a;font-weight:600">{boyut}</span>'
                f'<span style="font-size:.85rem;color:#059669;font-weight:800">{deger:.0f}/100</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div style="color:#d97706;font-weight:800;font-size:.78rem;margin:12px 0 8px;'
            'text-transform:uppercase;letter-spacing:.8px;display:flex;align-items:center;gap:6px">'
            '<span style="font-size:1rem">⚠️</span> GELİŞTİRİLECEK</div>',
            unsafe_allow_html=True,
        )
        for boyut, deger in sorted_boyutlar[-2:]:
            renk = "#ef4444" if deger < 60 else "#f59e0b"
            bg_grad = (f"linear-gradient(90deg,rgba(239,68,68,.08),rgba(239,68,68,.02))"
                       if deger < 60
                       else "linear-gradient(90deg,rgba(245,158,11,.08),rgba(245,158,11,.02))")
            border_clr = "rgba(239,68,68,.2)" if deger < 60 else "rgba(245,158,11,.2)"
            st.markdown(
                f'<div style="background:{bg_grad};'
                f'border:1px solid {border_clr};border-left:3px solid {renk};'
                f'border-radius:0 10px 10px 0;padding:8px 12px;margin-bottom:6px;'
                f'display:flex;justify-content:space-between;align-items:center">'
                f'<span style="font-size:.85rem;color:#0f172a;font-weight:600">{boyut}</span>'
                f'<span style="font-size:.85rem;color:{renk};font-weight:800">{deger:.0f}/100</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


def _render_veli_quick_actions(store, student, auth_user):
    """Premium Sticky Aksiyon \u00c7ubu\u011fu — 4 h\u0131zl\u0131 eylem butonu + canl\u0131 badge.

    H\u0131zl\u0131 eylem: Mesajlar, Randevu, \u00d6dev, Servis. Her biri sayfan\u0131n ilgili
    sekmesine atlama yerine, anl\u0131k bilgi g\u00f6sterir.
    """
    # Veri toplama
    try:
        okunmamis = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))
    except Exception:
        okunmamis = 0

    try:
        randevular = store.get_randevular(veli_id=auth_user.get("username", "")) if hasattr(store, "get_randevular") else []
        bekleyen_randevu = sum(1 for r in randevular if getattr(r, "durum", "") in ("bekliyor", "talep"))
    except Exception:
        bekleyen_randevu = 0

    try:
        odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif") or []
        teslimleri = store.get_odev_teslimleri(student_id=student.id) or []
        teslim_ids = {t.odev_id for t in teslimleri if t.durum == "teslim_edildi"}
        bekleyen_odev = sum(1 for o in odevler if o.id not in teslim_ids)
    except Exception:
        bekleyen_odev = 0

    qa_data = [
        ("💬", "Mesaj", okunmamis, "yeni", "#3b82f6", "#dbeafe", "#eff6ff"),
        ("📅", "Randevu", bekleyen_randevu, "bekliyor", "#8b5cf6", "#ede9fe", "#f5f3ff"),
        ("📝", "Ödev", bekleyen_odev, "acil" if bekleyen_odev >= 3 else "bekliyor",
         "#ef4444" if bekleyen_odev >= 3 else "#f59e0b",
         "#fee2e2" if bekleyen_odev >= 3 else "#fef3c7",
         "#fef2f2" if bekleyen_odev >= 3 else "#fffbeb"),
        ("🚌", "Servis", "CANLI", "konum", "#10b981", "#d1fae5", "#ecfdf5"),
    ]

    cols = st.columns(4)
    for i, (ikon, label, count, sub, color, bg_icon, bg_card) in enumerate(qa_data):
        with cols[i]:
            count_text = str(count) if isinstance(count, int) else count
            count_size = "1.6rem" if isinstance(count, int) else "1.05rem"
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#ffffff 0%,{bg_card} 100%);'
                f'border:1px solid {color}33;border-left:4px solid {color};'
                f'border-radius:18px;padding:16px 14px;text-align:center;'
                f'box-shadow:0 1px 3px rgba(15,23,42,.04),0 6px 16px {color}1a;'
                f'transition:transform .25s cubic-bezier(.4,0,.2,1),box-shadow .25s;'
                f'cursor:pointer;min-height:120px;'
                f'display:flex;flex-direction:column;justify-content:center;align-items:center">'
                f'<div style="width:48px;height:48px;border-radius:14px;'
                f'background:{bg_icon};display:flex;align-items:center;justify-content:center;'
                f'margin-bottom:8px;box-shadow:0 4px 12px {color}22">'
                f'<span style="font-size:1.5rem;line-height:1">{ikon}</span></div>'
                f'<div style="font-size:{count_size};font-weight:900;color:{color};line-height:1;'
                f'letter-spacing:-.5px">{count_text}</div>'
                f'<div style="font-size:.7rem;color:#475569;font-weight:700;margin-top:4px;'
                f'text-transform:uppercase;letter-spacing:.6px">{label}</div>'
                f'<div style="font-size:.65rem;color:#475569;font-weight:500;margin-top:1px">'
                f'{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ===================== AİLE BAŞARI DUVARI =====================

def _render_aile_basari_duvari(store, student, auth_user):
    """Aile Basari Duvari — cocugun her basarisi bir kart olarak duvarda birikir.

    Veli/ogretmen begenebilir, yorum yazabilir. Otomatik (notlardan) ve
    manuel basarilar desteklenir. Zaman bazli grup gosterimi.
    """
    try:
        from models.aile_basari_duvari import (
            BasariDuvariStore, Achievement, AchievementComment,
            AutoAchievementGenerator, ACHIEVEMENT_KATEGORILER, kategori_meta,
        )
    except Exception as _e:
        styled_info_banner(f"Aile Basari Duvari modulu yuklenemedi: {_e}", "warning")
        return

    bd_store = BasariDuvariStore()

    # ── PREMIUM HEADER ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0b1437 0%,#4338ca 30%,#ec4899 70%,#f59e0b 100%);'
        f'border-radius:18px;padding:22px 28px;margin-bottom:14px;'
        f'box-shadow:0 10px 32px rgba(236,72,153,.3);'
        f'border:1px solid rgba(245,158,11,.3);">'
        f'<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">'
        f'<span style="font-size:2.4rem">🌟</span>'
        f'<div style="flex:1;min-width:200px">'
        f'<div style="font-size:1.45rem;font-weight:900;color:#fff;letter-spacing:-.3px">'
        f'{student.ad}\'nin Başarı Duvarı</div>'
        f'<div style="font-size:.85rem;color:rgba(254,243,199,.9);margin-top:3px">'
        f'Her başarı bir hatıra · Her hatıra bir gurur · Yıl sonunda dijital pasaport</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── OTOMATIK BASARI URET (her render'da kontrol et) ──
    try:
        gen = AutoAchievementGenerator(bd_store)
        gen.generate_all(student, store)
    except Exception:
        pass

    # ── OZET STAT KARTLARI ──
    summary = bd_store.get_summary(student.id)
    styled_stat_row([
        ("Toplam Başarı", str(summary["toplam"]), "#f59e0b", "🌟"),
        ("Bu Hafta", str(summary["bu_hafta"]), "#10b981", "✨"),
        ("Bu Ay", str(summary["bu_ay"]), "#8b5cf6", "📅"),
        ("Toplam Beğeni", str(summary["begeni_toplami"]), "#ec4899", "❤️"),
        ("Yorumlar", str(summary["yorum_toplami"]), "#3b82f6", "💬"),
    ])
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── FILTRE BARI ──
    fc1, fc2 = st.columns([3, 1])
    with fc1:
        kat_options = ["Tümü"] + [k[1] for k in ACHIEVEMENT_KATEGORILER]
        secili_kat = st.selectbox(
            "Kategori filtresi",
            kat_options,
            key=f"basari_kat_filter_{student.id}",
            label_visibility="collapsed",
        )
    with fc2:
        if st.button("➕ Manuel Başarı Ekle", key=f"basari_ekle_btn_{student.id}",
                     use_container_width=True):
            st.session_state[f"basari_ekle_open_{student.id}"] = True

    # ── MANUEL BASARI EKLEME FORMU ──
    if st.session_state.get(f"basari_ekle_open_{student.id}"):
        with st.form(f"basari_ekle_form_{student.id}", clear_on_submit=True):
            st.markdown(
                '<div style="font-size:1rem;font-weight:700;color:#475569;margin-bottom:8px">'
                '➕ Yeni Başarı Ekle</div>',
                unsafe_allow_html=True,
            )
            yc1, yc2 = st.columns(2)
            with yc1:
                y_baslik = st.text_input("Başlık *", placeholder="örn. Sınıf temsilcisi seçildi")
                y_kategori = st.selectbox(
                    "Kategori",
                    [k[0] for k in ACHIEVEMENT_KATEGORILER],
                    format_func=lambda k: f"{kategori_meta(k)[1]} {kategori_meta(k)[0]}",
                )
            with yc2:
                y_tarih = st.date_input("Tarih", value=date.today())
                y_video = st.text_input("Video linki (opsiyonel)", placeholder="https://...")
            y_aciklama = st.text_area("Açıklama", placeholder="Detayları yazın...", height=80)

            sc1, sc2 = st.columns([1, 4])
            with sc1:
                kaydet = st.form_submit_button("✅ Ekle", type="primary",
                                                use_container_width=True)
            with sc2:
                iptal = st.form_submit_button("İptal", use_container_width=False)

            if kaydet:
                if not y_baslik.strip():
                    st.error("Başlık zorunludur.")
                else:
                    new_ach = Achievement(
                        student_id=student.id,
                        student_adi=getattr(student, "tam_ad", f"{student.ad} {student.soyad}"),
                        sinif=str(getattr(student, "sinif", "")),
                        sube=getattr(student, "sube", ""),
                        baslik=y_baslik.strip(),
                        aciklama=y_aciklama.strip(),
                        kategori=y_kategori,
                        video_link=y_video.strip(),
                        kaynak="manuel",
                        ogretmen_adi=auth_user.get("name", ""),
                        tarih=y_tarih.isoformat(),
                    )
                    bd_store.save_achievement(new_ach)
                    st.session_state[f"basari_ekle_open_{student.id}"] = False
                    st.success("✅ Başarı eklendi!")
                    st.balloons()
                    st.rerun()
            if iptal:
                st.session_state[f"basari_ekle_open_{student.id}"] = False
                st.rerun()

    # ── BASARI LISTESI ──
    achs = bd_store.get_achievements(student_id=student.id)
    if secili_kat != "Tümü":
        kat_key = next((k[0] for k in ACHIEVEMENT_KATEGORILER if k[1] == secili_kat), None)
        if kat_key:
            achs = [a for a in achs if a.kategori == kat_key]

    if not achs:
        styled_info_banner(
            f"{student.ad} için henüz başarı kartı yok. Öğretmen başarı eklediğinde veya çocuğunuz "
            "yüksek not, ödev başarısı, kazanım tamamlama vb. yaptığında otomatik kartlar eklenecek. "
            "Manuel olarak da '➕ Manuel Başarı Ekle' butonu ile ekleyebilirsiniz.",
            "info",
        )
        return

    # ── ZAMAN BAZLI GRUPLAMA ──
    from datetime import timedelta
    bugun = date.today()
    dun = bugun - timedelta(days=1)
    hafta_basi = bugun - timedelta(days=bugun.weekday())
    ay_basi = bugun.replace(day=1)

    gruplar: dict[str, list] = {
        "📍 Bugün": [],
        "📅 Dün": [],
        "📆 Bu Hafta": [],
        "🗓️ Bu Ay": [],
        "⏳ Daha Önce": [],
    }
    for a in achs:
        try:
            ad = date.fromisoformat(a.tarih)
        except Exception:
            ad = bugun
        if ad == bugun:
            gruplar["📍 Bugün"].append(a)
        elif ad == dun:
            gruplar["📅 Dün"].append(a)
        elif ad >= hafta_basi:
            gruplar["📆 Bu Hafta"].append(a)
        elif ad >= ay_basi:
            gruplar["🗓️ Bu Ay"].append(a)
        else:
            gruplar["⏳ Daha Önce"].append(a)

    user_id = auth_user.get("username", "veli")

    for grup_adi, grup_achs in gruplar.items():
        if not grup_achs:
            continue
        st.markdown(
            f'<div style="background:linear-gradient(90deg,#1e293b,#0f172a);'
            f'color:#475569;padding:8px 16px;border-radius:10px;'
            f'margin:14px 0 8px;font-weight:700;font-size:.92rem;'
            f'border-left:4px solid #f59e0b">{grup_adi} '
            f'<span style="color:#64748b;font-weight:500;font-size:.78rem">'
            f'· {len(grup_achs)} başarı</span></div>',
            unsafe_allow_html=True,
        )

        for ach in grup_achs:
            kat_label, kat_icon, kat_color = kategori_meta(ach.kategori)
            is_liked = bd_store.is_liked_by(ach.id, user_id)
            heart_icon = "❤️" if is_liked else "🤍"
            ogr_text = f" · {ach.ogretmen_adi}" if ach.ogretmen_adi else ""
            kaynak_badge = ""
            if ach.kaynak == "auto_grade":
                kaynak_badge = '<span style="background:#1e3a8a;color:#bfdbfe;padding:1px 8px;border-radius:8px;font-size:.65rem;font-weight:700;margin-left:6px">AUTO</span>'
            elif ach.kaynak == "auto_kazanim":
                kaynak_badge = '<span style="background:#065f46;color:#a7f3d0;padding:1px 8px;border-radius:8px;font-size:.65rem;font-weight:700;margin-left:6px">AUTO</span>'
            elif ach.kaynak == "auto_odev":
                kaynak_badge = '<span style="background:#92400e;color:#fde68a;padding:1px 8px;border-radius:8px;font-size:.65rem;font-weight:700;margin-left:6px">AUTO</span>'

            video_html = ""
            if ach.video_link:
                video_html = (f'<div style="margin-top:6px"><a href="{ach.video_link}" target="_blank" '
                              f'style="color:#60a5fa;font-size:.78rem;text-decoration:none">'
                              f'🎬 Video İzle →</a></div>')

            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);'
                f'border:1px solid {kat_color}55;border-left:5px solid {kat_color};'
                f'border-radius:14px;padding:16px 20px;margin:8px 0;'
                f'box-shadow:0 4px 14px rgba(0,0,0,.25)">'
                f'<div style="display:flex;align-items:flex-start;gap:14px">'
                f'<div style="font-size:2rem;flex-shrink:0;margin-top:-2px">{ach.ikon}</div>'
                f'<div style="flex:1">'
                f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:4px">'
                f'<span style="font-size:1rem;font-weight:800;color:#0f172a">{ach.baslik}</span>'
                f'<span style="background:{kat_color}22;color:{kat_color};border:1px solid {kat_color}44;'
                f'border-radius:10px;padding:1px 8px;font-size:.68rem;font-weight:700">{kat_label}</span>'
                f'{kaynak_badge}'
                f'</div>'
                f'<div style="font-size:.85rem;color:#0f172a;line-height:1.5">{ach.aciklama or "—"}</div>'
                f'<div style="font-size:.72rem;color:#64748b;margin-top:6px">'
                f'📅 {ach.tarih}{ogr_text}'
                f'</div>'
                f'{video_html}'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Like + Yorum butonları
            bc1, bc2, bc3, _bc4 = st.columns([1, 1, 1, 4])
            with bc1:
                if st.button(f"{heart_icon} {ach.begeni_count}",
                             key=f"basari_like_{ach.id}",
                             use_container_width=True):
                    bd_store.toggle_like(ach.id, user_id)
                    st.rerun()
            with bc2:
                yorum_label = f"💬 {ach.yorum_count}" if ach.yorum_count else "💬 Yorum"
                if st.button(yorum_label, key=f"basari_yorum_btn_{ach.id}",
                             use_container_width=True):
                    st.session_state[f"basari_yorum_open_{ach.id}"] = not st.session_state.get(
                        f"basari_yorum_open_{ach.id}", False
                    )
            with bc3:
                # Sadece manuel kayıt için sil butonu
                if ach.kaynak == "manuel":
                    if st.button("🗑️", key=f"basari_sil_{ach.id}",
                                 help="Bu başarı kartını sil"):
                        bd_store.delete_achievement(ach.id)
                        st.rerun()

            # Yorumlar (açıksa göster)
            if st.session_state.get(f"basari_yorum_open_{ach.id}"):
                comments = bd_store.get_comments(ach.id)
                if comments:
                    for c in comments:
                        rol_renk = {"veli": "#10b981", "ogretmen": "#7c3aed", "ogrenci": "#f59e0b"}.get(
                            c.yazan_rol, "#64748b"
                        )
                        rol_label = {"veli": "👨‍👩 Veli", "ogretmen": "👩‍🏫 Öğretmen", "ogrenci": "🎓 Öğrenci"}.get(
                            c.yazan_rol, "Yorum"
                        )
                        st.markdown(
                            f'<div style="background:#ffffff;border-left:3px solid {rol_renk};'
                            f'border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0 4px 24px">'
                            f'<div style="font-size:.78rem;color:{rol_renk};font-weight:700">'
                            f'{rol_label} · {c.yazan_adi} <span style="color:#64748b;font-weight:400">'
                            f'· {c.tarih[:16].replace("T", " ")}</span></div>'
                            f'<div style="font-size:.85rem;color:#0f172a;margin-top:3px">{c.mesaj}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                # Yeni yorum formu
                with st.form(f"yorum_form_{ach.id}", clear_on_submit=True):
                    yorum_msg = st.text_input(
                        "Yorum yaz",
                        placeholder="Aferin oğlum/kızım, çok gurur duyduk...",
                        label_visibility="collapsed",
                    )
                    if st.form_submit_button("Yorum Gönder", type="primary"):
                        if yorum_msg.strip():
                            new_comment = AchievementComment(
                                achievement_id=ach.id,
                                yazan_id=user_id,
                                yazan_adi=auth_user.get("name", "Sayın Veli"),
                                yazan_rol="veli",
                                mesaj=yorum_msg.strip(),
                            )
                            bd_store.save_comment(new_comment)
                            st.rerun()


# ===================== STEM MERKEZI (STEAM) — VELI/OGRENCI =====================

def _render_stem_merkezi_tab(student, role: str = "veli"):
    """STEM Merkezi sekmesi — ogrenci/veli icin sadelestirilmis goruntuleme.

    Ogrencinin STEM profili, projeler, yarisma katilimlari, XP/seviye ve
    rozetler. Veli icin: cocugun STEAM gelisimi (sadece okuma).
    Ogrenci icin: ek olarak yapabilecegi muhendislik gorevleri kataloglu.
    """
    try:
        from models.stem_merkezi import get_stem_store
    except Exception as _e:
        styled_info_banner(f"STEM Merkezi modulu yuklenemedi: {_e}", "warning")
        return

    stem_store = get_stem_store()

    # ── PREMIUM HEADER ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0b1437 0%,#4338ca 35%,#7c3aed 70%,#22d3ee 100%);'
        f'border-radius:18px;padding:20px 26px;margin-bottom:14px;'
        f'box-shadow:0 10px 32px rgba(124,58,237,.3);'
        f'border:1px solid rgba(34,211,238,.3);">'
        f'<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">'
        f'<span style="font-size:2.2rem">🔬</span>'
        f'<div style="flex:1;min-width:200px">'
        f'<div style="font-size:1.35rem;font-weight:900;color:#fff;letter-spacing:-.3px">'
        f'STEAM Merkezi — {student.ad}</div>'
        f'<div style="font-size:.82rem;color:rgba(186,230,253,.95);margin-top:3px">'
        f'Bilim · Teknoloji · Muhendislik · Sanat · Matematik — projeler, yarismalar, beceri agaci</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── BIRLESIK PROFIL ──
    try:
        birlesik = stem_store.get_birlesik_stem_profil(student.id)
    except Exception:
        birlesik = {}

    stem_profil = (birlesik.get("stem_profil") or {}) if birlesik else {}
    projeler = (birlesik.get("projeler") or []) if birlesik else []
    yarisma_sayisi = int(birlesik.get("yarisma_sayisi", 0)) if birlesik else 0
    tamamlanan_proje = int(birlesik.get("tamamlanan_proje", 0)) if birlesik else 0
    toplam_proje = int(birlesik.get("toplam_proje", len(projeler))) if birlesik else len(projeler)

    # Profil yoksa default
    stem_xp = int(stem_profil.get("stem_xp", 0))
    stem_seviye = int(stem_profil.get("stem_seviye", 1))
    rozetler = stem_profil.get("rozetler", []) or []

    # ── OZET STAT KARTLARI ──
    styled_stat_row([
        ("STEAM Seviye", f"Lv {stem_seviye}", "#7c3aed", "🏅"),
        ("Toplam XP", str(stem_xp), "#22d3ee", "⚡"),
        ("Aktif Proje", str(max(toplam_proje - tamamlanan_proje, 0)), "#f59e0b", "🔬"),
        ("Tamamlanan", str(tamamlanan_proje), "#10b981", "✅"),
        ("Yarisma", str(yarisma_sayisi), "#ec4899", "🏆"),
        ("Rozet", str(len(rozetler)), "#fbbf24", "🥇"),
    ])
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── DAL BAZLI SKORLAR (radar yerine bar) ──
    if stem_profil:
        st.markdown(
            '<div style="font-size:.95rem;font-weight:800;color:#475569;margin:10px 0 6px">'
            '📊 STEAM Dal Skorlari</div>',
            unsafe_allow_html=True,
        )
        dal_skorlar = [
            ("Matematik", float(stem_profil.get("matematik_skoru", 0)), "#3b82f6"),
            ("Fen", float(stem_profil.get("fen_skoru", 0)), "#10b981"),
            ("Teknoloji", float(stem_profil.get("teknoloji_skoru", 0)), "#7c3aed"),
            ("Muhendislik", float(stem_profil.get("muhendislik_skoru", 0)), "#f59e0b"),
        ]
        for ad, skor, renk in dal_skorlar:
            yuzde = max(0, min(100, skor))
            st.markdown(
                f'<div style="margin-bottom:6px">'
                f'<div style="display:flex;justify-content:space-between;font-size:.78rem;'
                f'color:#475569;font-weight:700;margin-bottom:3px">'
                f'<span>{ad}</span><span style="color:{renk}">{yuzde:.0f}/100</span></div>'
                f'<div style="background:#e2e8f0;border-radius:8px;height:8px;overflow:hidden">'
                f'<div style="background:linear-gradient(90deg,{renk},{renk}cc);'
                f'width:{yuzde}%;height:100%;border-radius:8px"></div></div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── ROZETLER ──
    if rozetler:
        st.markdown(
            '<div style="font-size:.95rem;font-weight:800;color:#475569;margin:12px 0 6px">'
            '🥇 Rozetler</div>',
            unsafe_allow_html=True,
        )
        roz_html = ''.join([
            f'<span style="display:inline-block;background:linear-gradient(135deg,#fbbf24,#f59e0b);'
            f'color:#7c2d12;padding:6px 12px;border-radius:20px;font-size:.78rem;font-weight:700;'
            f'margin:3px;box-shadow:0 2px 6px rgba(245,158,11,.3)">🏅 {r}</span>'
            for r in rozetler
        ])
        st.markdown(f'<div>{roz_html}</div>', unsafe_allow_html=True)

    # ── PROJELER ──
    st.markdown(
        '<div style="font-size:.95rem;font-weight:800;color:#475569;margin:14px 0 6px">'
        '🔬 STEAM Projelerim</div>',
        unsafe_allow_html=True,
    )

    # PROJE_DURUMLARI flat list -> human label map
    durum_map = {
        "fikir": "Fikir Asamasi",
        "planlama": "Planlama",
        "gelistirme": "Gelistirme",
        "test": "Test",
        "sunum": "Sunum",
        "tamamlandi": "Tamamlandi",
        "iptal": "Iptal",
    }
    durum_renk = {
        "fikir": "#94a3b8", "planlama": "#3b82f6", "gelistirme": "#f59e0b",
        "test": "#a855f7", "sunum": "#06b6d4", "tamamlandi": "#10b981",
        "iptal": "#ef4444",
    }

    if not projeler:
        styled_info_banner(
            "Henuz STEAM projesi bulunmuyor. Ogretmenin sana yeni proje atayabilir veya "
            "STEAM Merkezi'nde bir muhendislik gorevi secebilirsin.", "info",
        )
    else:
        # Son 5 proje (tarihe gore tersten)
        sirali_proj = sorted(
            projeler,
            key=lambda p: p.get("olusturma_tarihi", ""),
            reverse=True,
        )[:8]
        for p in sirali_proj:
            durum_key = p.get("durum", "fikir")
            durum_lbl = durum_map.get(durum_key, durum_key)
            renk = durum_renk.get(durum_key, "#64748b")
            kategori = p.get("kategori", "-")
            zorluk = p.get("zorluk", "Orta")
            mentor = p.get("mentor_adi", "-") or "-"
            baslangic = p.get("baslangic_tarihi", "")[:10]
            hedef = p.get("hedef_tarih", "")[:10] or "-"
            stem_dallari = ", ".join(p.get("stem_dallari", []) or []) or "-"

            st.markdown(
                f'<div style="background:linear-gradient(135deg,#f8fafc,#eef2ff);'
                f'border:1px solid #c7d2fe;border-left:4px solid {renk};'
                f'border-radius:12px;padding:14px 18px;margin-bottom:10px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'flex-wrap:wrap;gap:8px;margin-bottom:6px">'
                f'<span style="font-size:1rem;font-weight:800;color:#1e293b">'
                f'🔬 {p.get("baslik", "(baslik yok)")}</span>'
                f'<span style="background:{renk};color:#fff;padding:3px 10px;'
                f'border-radius:14px;font-size:.72rem;font-weight:700">{durum_lbl}</span>'
                f'</div>'
                f'<div style="font-size:.78rem;color:#475569;margin-bottom:4px">'
                f'📂 {kategori} · ⚡ {zorluk} · 🧪 {stem_dallari}'
                f'</div>'
                f'<div style="font-size:.75rem;color:#64748b">'
                f'👤 Mentor: {mentor} · 📅 {baslangic} → {hedef}'
                f'</div>'
                + (f'<div style="font-size:.78rem;color:#334155;margin-top:6px">'
                   f'{p.get("aciklama", "")[:200]}</div>' if p.get("aciklama") else '')
                + '</div>',
                unsafe_allow_html=True,
            )

    # ── YARISMALAR ──
    try:
        tum_yarismalar = stem_store.load_list("yarismalar")
        ogrenci_yar = [
            y for y in tum_yarismalar
            if student.id in (y.get("katilimci_ids") or [])
        ]
    except Exception:
        ogrenci_yar = []

    if ogrenci_yar:
        st.markdown(
            '<div style="font-size:.95rem;font-weight:800;color:#475569;margin:14px 0 6px">'
            '🏆 Yarisma Katilimlari</div>',
            unsafe_allow_html=True,
        )
        for y in sorted(ogrenci_yar, key=lambda x: x.get("tarih", ""), reverse=True)[:6]:
            sonuc = y.get("sonuc", "katilim") or "katilim"
            sonuc_renk = "#fbbf24" if sonuc in ("birincilik", "ikincilik", "ucunculuk") else "#64748b"
            st.markdown(
                f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;'
                f'align-items:center;gap:10px">'
                f'<div><div style="font-weight:800;color:#1e293b;font-size:.88rem">'
                f'🏆 {y.get("yarisma_adi", "(adsiz)")}</div>'
                f'<div style="font-size:.72rem;color:#64748b">'
                f'{y.get("organizator", "-")} · 📅 {y.get("tarih", "-")} · {y.get("yer", "-")}</div></div>'
                f'<span style="background:{sonuc_renk};color:#fff;padding:4px 12px;'
                f'border-radius:14px;font-size:.72rem;font-weight:700">{sonuc.upper()}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── OGRENCI ICIN: EVDE YAPILABILECEK GOREV KATALOGU ──
    if role == "ogrenci":
        st.markdown(
            '<div style="font-size:.95rem;font-weight:800;color:#475569;margin:16px 0 6px">'
            '🔧 Sana Ozel Muhendislik Gorevleri</div>',
            unsafe_allow_html=True,
        )
        try:
            tum_gorevler = stem_store.load_list("gorevler")
        except Exception:
            tum_gorevler = []

        # Sinif grubu eslesmesi
        try:
            _sn = int(student.sinif) if str(student.sinif).isdigit() else 0
        except Exception:
            _sn = 0
        if 1 <= _sn <= 4:
            sg = "Ilkokul (1-4)"
        elif 5 <= _sn <= 8:
            sg = "Ortaokul (5-8)"
        else:
            sg = "Lise (9-12)"

        uygun = [g for g in tum_gorevler if g.get("sinif_grubu") == sg]
        if not uygun:
            uygun = tum_gorevler[:6]
        else:
            uygun = uygun[:8]

        if not uygun:
            styled_info_banner("Henuz tanimlanmis muhendislik gorevi yok.", "info")
        else:
            for g in uygun:
                with st.expander(
                    f"🔧 {g.get('baslik', '(adsiz)')} · "
                    f"{g.get('alan', '-')} · ⚡ {g.get('zorluk', 'Orta')} · "
                    f"⏱️ {g.get('sure_dk', 0)} dk",
                    expanded=False,
                ):
                    st.markdown(f"**Aciklama:** {g.get('aciklama', '-')}")
                    malz = g.get("malzemeler", [])
                    if malz:
                        st.markdown("**Malzemeler:** " + ", ".join(malz))
                    kazanim = g.get("kazanimlar", [])
                    if kazanim:
                        st.markdown("**Kazanimlar:** " + ", ".join(kazanim))
                    adimlar = g.get("adimlar", [])
                    if adimlar:
                        st.markdown("**Adimlar:**")
                        for ad in adimlar:
                            st.markdown(
                                f"- **{ad.get('adim_no', '?')}.** {ad.get('aciklama', '')}"
                            )

    # ── VELI ICIN: EVDE DESTEK ONERILERI ──
    if role == "veli":
        st.markdown(
            '<div style="font-size:.85rem;color:#475569;background:#fef3c7;'
            'border:1px solid #fcd34d;border-radius:10px;padding:12px 16px;margin-top:14px">'
            '💡 <b>Veli Onerisi:</b> Cocugunuzun STEAM gelisimini destekleyin: haftada 1 saat '
            'birlikte bir muhendislik gorevi yapin, projelerini sergileyin ve ilgi duydugu alanlari '
            'kesfetmesine alan acin.</div>',
            unsafe_allow_html=True,
        )


# ===================== YARDIMCI FONKSİYONLAR =====================

def _get_akademik_yil() -> str:
    today = date.today()
    if today.month >= 9:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


def _find_student_for_veli(store: AkademikDataStore, auth_user: dict) -> list[Student]:
    """Velinin cocuklarini bul."""
    name = auth_user.get("name", "")
    username = auth_user.get("username", "")
    all_students = store.get_students()
    children = [s for s in all_students
                if s.veli_adi and name.lower() in s.veli_adi.lower()]
    if not children:
        children = [s for s in all_students
                    if s.veli_telefon and username in str(s.veli_telefon)]
    if not children:
        children = [s for s in all_students
                    if s.veli_email and username in str(s.veli_email)]
    return children


def _find_student_for_ogrenci(store: AkademikDataStore, auth_user: dict) -> Student | None:
    """Ogrenci hesabina ait ogrenci kaydini bul."""
    name = auth_user.get("name", "")
    username = auth_user.get("username", "")
    all_students = store.get_students()
    for s in all_students:
        if name.lower() in s.tam_ad.lower():
            return s
    for s in all_students:
        if s.ogrenci_email and username in str(s.ogrenci_email):
            return s
    return None


def _get_not_ortalamasi(grades: list) -> float:
    if not grades:
        return 0.0
    puanlar = [g.puan for g in grades if g.puan is not None and g.puan > 0]
    if not puanlar:
        return 0.0
    return round(sum(puanlar) / len(puanlar), 1)


# ===================== ORTAK SEKMELER (GRAFİKLİ) =====================

def _render_notlar_tab(store: AkademikDataStore, student: Student, readonly: bool = True):
    """Notlar sekmesi - ders bazli tablo + grafikler."""
    grades = store.get_grades(student_id=student.id)
    if not grades:
        styled_info_banner("Henuz not kaydi bulunmuyor.", "info")
        return

    # Ders bazli gruplama
    ders_notlar: dict[str, list] = {}
    for g in grades:
        ders_notlar.setdefault(g.ders, []).append(g)

    # --- GRAFIK: Ders Bazli Ortalama Bar Chart ---
    ders_ort_data = []
    for ders, notlar in sorted(ders_notlar.items()):
        ort = _get_not_ortalamasi(notlar)
        ders_ort_data.append({"Ders": ders, "Ortalama": ort, "Not Sayısı": len(notlar)})

    if ders_ort_data:
        df_ort = pd.DataFrame(ders_ort_data)
        c1, c2 = st.columns(2)

        with c1:
            df_sorted = df_ort.sort_values("Ortalama", ascending=True)
            fig_bar = go.Figure(go.Bar(
                y=df_sorted["Ders"], x=df_sorted["Ortalama"],
                orientation="h", text=[f"{v:.1f}" for v in df_sorted["Ortalama"]],
                textposition="outside",
                marker_color=SC_COLORS[0],
            ))
            sc_bar(fig_bar, horizontal=True)
            fig_bar.update_layout(xaxis=dict(range=[0, 105]), yaxis=dict(automargin=True))
            st.plotly_chart(fig_bar, use_container_width=True, config=SC_CHART_CFG)

        with c2:
            fig_donut = go.Figure(go.Pie(
                labels=df_ort["Ders"], values=df_ort["Not Sayısı"],
                hole=0.55, marker=dict(colors=SC_COLORS[:len(df_ort)],
                                       line=dict(color="#fff", width=2)),
            ))
            sc_pie(fig_donut)
            st.plotly_chart(fig_donut, use_container_width=True, config=SC_CHART_CFG)

    # Tablo detay
    for ders, notlar in sorted(ders_notlar.items()):
        with st.expander(f"📚 {ders} ({len(notlar)} not)", expanded=False):
            rows = []
            for g in notlar:
                rows.append({
                    "Not Turu": g.not_turu, "Sira": g.not_sirasi,
                    "Puan": g.puan, "Donem": g.donem,
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)
            ort = _get_not_ortalamasi(notlar)
            st.caption(f"Ders Ortalaması: **{ort}**")


def _render_devamsizlik_tab(store: AkademikDataStore, student: Student):
    """Devamsizlik sekmesi + grafikler."""
    attendance = store.get_attendance(student_id=student.id)
    if not attendance:
        styled_info_banner("Henuz devamsizlik kaydi bulunmuyor.", "info")
        return

    ozurlu = sum(1 for a in attendance if a.turu == "ozurlu")
    ozursuz = sum(1 for a in attendance if a.turu == "ozursuz")

    styled_stat_row([
        ("Toplam", str(len(attendance)), "#4472C4", "📊"),
        ("Ozurlu", str(ozurlu), "#FFC000", "✅"),
        ("Ozursuz", str(ozursuz), "#ED7D31", "❌"),
    ])

    c1, c2 = st.columns(2)

    # --- GRAFIK: Donut Chart (Ozurlu / Ozursuz) ---
    with c1:
        fig_donut = go.Figure(go.Pie(
            labels=["Ozurlu", "Ozursuz"],
            values=[ozurlu, ozursuz],
            hole=0.55,
            marker=dict(colors=SC_COLORS[:2],
                        line=dict(color="#fff", width=2)),
        ))
        sc_pie(fig_donut)
        st.plotly_chart(fig_donut, use_container_width=True, config=SC_CHART_CFG)

    # --- GRAFIK: Aylik Trend ---
    with c2:
        aylik: dict[str, int] = {}
        for a in attendance:
            ay = a.tarih[:7] if a.tarih else "Bilinmiyor"
            aylik[ay] = aylik.get(ay, 0) + 1
        if aylik:
            df_ay = pd.DataFrame([
                {"Ay": k, "Devamsızlık": v} for k, v in sorted(aylik.items())
            ])
            fig_trend = go.Figure(go.Bar(
                y=df_ay["Ay"], x=df_ay["Devamsızlık"],
                orientation="h", text=df_ay["Devamsızlık"],
                textposition="outside",
                marker_color=SC_COLORS[0],
            ))
            sc_bar(fig_trend, horizontal=True)
            fig_trend.update_layout(yaxis=dict(automargin=True))
            st.plotly_chart(fig_trend, use_container_width=True, config=SC_CHART_CFG)

    # Tablo
    rows = []
    for a in sorted(attendance, key=lambda x: x.tarih, reverse=True):
        rows.append({
            "Tarih": a.tarih, "Ders": getattr(a, 'ders', '-'),
            "Ders Saati": getattr(a, 'ders_saati', '-'), "Turu": a.turu.upper(),
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _get_or_create_kazanim_odevi(
    store: AkademikDataStore, od: OlcmeDataStore, ki: KazanimIsleme
):
    """KazanimIsleme kaydı için soru bankasından ödev bul veya otomatik oluştur."""
    sinif_int = ki.sinif if isinstance(ki.sinif, int) else int(ki.sinif or 0)
    mevcut = store.get_odevler(sinif=sinif_int, sube=ki.sube, ders=ki.ders, durum="aktif")
    for o in mevcut:
        if o.odev_turu == "kazanim_odevi" and o.kazanim_kodu == ki.kazanim_kodu:
            return o

    qs = od.get_questions(grade=sinif_int, subject=ki.ders)
    iyi = [q for q in qs
           if not q.stem.startswith("[")
           and q.correct_choice
           and q.choices.get("A", "").strip()
           and q.choices.get("B", "").strip()]
    if not iyi:
        return None

    secilen = random.sample(iyi, min(3, len(iyi)))
    soru_ids = json.dumps([q.id for q in secilen])

    tarih = ki.tarih or date.today().isoformat()
    try:
        son_tarih = (date.fromisoformat(tarih) + timedelta(days=3)).isoformat()
    except Exception:
        son_tarih = tarih

    odev = Odev(
        sinif=sinif_int,
        sube=ki.sube,
        ders=ki.ders,
        baslik=f"Kazanım Ödevi — {(ki.kazanim_metni or ki.kazanim_kodu)[:60]}",
        aciklama=soru_ids,
        odev_turu="kazanim_odevi",
        verilme_tarihi=tarih,
        son_teslim_tarihi=son_tarih,
        kazanim_kodu=ki.kazanim_kodu,
        online_teslim=True,
        ogrenci_teslim_turu="metin",
        durum="aktif",
    )
    store.save_odev(odev)
    store.odev_teslim_olustur(odev)
    return odev


def _render_kazanim_odevi_coz(
    store: AkademikDataStore, od: OlcmeDataStore,
    student: Student, odev: Odev, teslim, ki: KazanimIsleme
):
    """Tek kazanım ödevini açık göster, cevapla, otomatik değerlendir."""
    today_str = date.today().isoformat()

    # Kazanım bilgi kartı
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#05966910,#05966905);
                border-left:4px solid #059669;border-radius:8px;
                padding:10px 14px;margin-bottom:12px;">
        <div style="font-weight:700;color:#059669;font-size:0.88rem;">🎯 Kazanım</div>
        <div style="font-size:0.82rem;color:#475569;margin-top:3px;">
            {ki.kazanim_metni or ki.kazanim_kodu}
        </div>
        <div style="font-size:0.72rem;color:#64748b;margin-top:4px;">
            📚 {odev.ders} &nbsp;|&nbsp;
            📅 Verilme: {odev.verilme_tarihi} &nbsp;|&nbsp;
            ⏰ Son: {odev.son_teslim_tarihi}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quiz sorularını yükle
    quiz_key = f"kaz_quiz_{odev.id}"
    if quiz_key not in st.session_state:
        quiz_qs = []
        try:
            soru_ids = json.loads(odev.aciklama)
            for qid in soru_ids:
                q = od.get_question(qid)
                if q:
                    quiz_qs.append(q)
        except Exception:
            pass
        # Fallback: bankadan seç
        if not quiz_qs:
            try:
                _s = student.sinif
                sinif_int = _s if isinstance(_s, int) else int(''.join(c for c in str(_s or '0') if c.isdigit()) or '0')
            except (ValueError, TypeError):
                sinif_int = 0
            qs = od.get_questions(grade=sinif_int, subject=odev.ders)
            iyi = [q for q in qs
                   if not q.stem.startswith("[") and q.correct_choice
                   and q.choices.get("A", "").strip() and q.choices.get("B", "").strip()]
            quiz_qs = random.sample(iyi, min(3, len(iyi))) if iyi else []
        st.session_state[quiz_key] = quiz_qs

    quiz_qs = st.session_state.get(quiz_key, [])
    if not quiz_qs:
        styled_info_banner("Bu kazanım için soru bankasında uygun soru bulunamadı.", "warning")
        return

    st.markdown(f"""
    <div style="background:#6366f110;border:1px solid #6366f130;border-radius:10px;
                padding:10px 14px;margin-bottom:14px;">
        <span style="color:#6366f1;font-weight:700;">📝 {len(quiz_qs)} Soru</span>
        <span style="color:#64748b;font-size:0.78rem;margin-left:8px;">
            Tüm soruları yanıtlayıp "Teslim Et" butonuna basın.
        </span>
    </div>
    """, unsafe_allow_html=True)

    cevaplar: dict[str, str] = {}
    for i, q in enumerate(quiz_qs):
        secenekler = [f"{k}) {v}" for k, v in sorted(q.choices.items()) if v.strip()]
        st.markdown(f"**{i + 1}.** {q.stem}")
        secim = st.radio(
            f"ks_{i}", secenekler,
            key=f"kaz_{odev.id}_{q.id}",
            index=None, label_visibility="collapsed",
        )
        if secim:
            cevaplar[q.id] = secim[0]
        st.markdown("")

    cevaplanmis = len(cevaplar)
    btn_label = (
        "✅ Teslim Et & Otomatik Değerlendir"
        if cevaplanmis == len(quiz_qs)
        else f"✅ Teslim Et  ({cevaplanmis}/{len(quiz_qs)} cevaplanmış)"
    )
    if st.button(btn_label, key=f"kaz_submit_{odev.id}",
                 type="primary", use_container_width=True):
        dogru = sum(1 for q in quiz_qs if cevaplar.get(q.id) == q.correct_choice)
        yanlis = cevaplanmis - dogru
        bos = len(quiz_qs) - cevaplanmis
        puan = round((dogru / len(quiz_qs)) * 100)

        metin = (
            f"Kazanım: {ki.kazanim_kodu}\nDers: {odev.ders}\n"
            + "Cevaplar: " + ", ".join(
                f"S{i+1}:{cevaplar.get(q.id, '–')}" for i, q in enumerate(quiz_qs)
            )
            + f"\nDoğru: {dogru}/{len(quiz_qs)}, Puan: {puan}/100"
        )
        _odev_teslim_kaydet(store, odev, teslim, student, float(puan), metin, today_str)

        renk = "#22c55e" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
        st.markdown(f"""
        <div style="background:{renk}15;border:2px solid {renk};border-radius:12px;
                    padding:20px;text-align:center;margin-top:12px;">
            <div style="font-size:2.2rem;font-weight:900;color:{renk};">{puan}</div>
            <div style="color:{renk};font-weight:700;">/ 100 Puan</div>
            <div style="color:#475569;font-size:0.85rem;margin-top:8px;">
                ✅ {dogru} Doğru &nbsp;&nbsp; ❌ {yanlis} Yanlış &nbsp;&nbsp; ⬜ {bos} Boş
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.pop(quiz_key, None)
        st.rerun()


def _render_kazanim_odevi_tab(
    store: AkademikDataStore, od: OlcmeDataStore, student: Student
):
    """Kazanım Ödevi sekmesi: otomatik quiz + sonuç grafikleri."""
    import re as _re

    styled_section("Kazanım Ödevleri", "#059669")
    akademik_yil = _get_akademik_yil()
    try:
        sinif_int = student.sinif if isinstance(student.sinif, int) else int(''.join(c for c in str(student.sinif or '0') if c.isdigit()) or '0')
    except (ValueError, TypeError):
        sinif_int = 0
    today_str = date.today().isoformat()

    # ── İşlenen kazanımları yükle ──
    ki_kayitlar = store.get_kazanim_isleme(
        sinif=sinif_int, sube=student.sube, durum="islendi", akademik_yil=akademik_yil
    )
    if not ki_kayitlar:
        styled_info_banner(
            "Henüz işlenmiş kazanım bulunmuyor. "
            "Öğretmen kazanımları işaretledikçe ödevler otomatik oluşur.", "info"
        )
        return

    # ── Her kazanım için ödev bul / oluştur ──
    teslimler = store.get_odev_teslimleri(student_id=student.id)
    teslim_map = {t.odev_id: t for t in teslimler}

    odev_listesi: list[tuple] = []
    with st.spinner("Kazanım ödevleri hazırlanıyor…"):
        for ki in ki_kayitlar:
            odev = _get_or_create_kazanim_odevi(store, od, ki)
            if odev is None:
                continue
            teslim = teslim_map.get(odev.id)
            odev_listesi.append((ki, odev, teslim))

    if not odev_listesi:
        styled_info_banner("Soru bankasında uygun soru bulunamadı.", "warning")
        return

    bekleyen = [(ki, o, t) for ki, o, t in odev_listesi if not t or t.durum != "teslim_edildi"]
    tamamlanan = [(ki, o, t) for ki, o, t in odev_listesi if t and t.durum == "teslim_edildi"]
    puan_ort = round(sum(t.puan for _, _, t in tamamlanan) / len(tamamlanan)) if tamamlanan else 0

    # ── İstatistik kartları ──
    styled_stat_row([
        ("Toplam Kazanım", str(len(odev_listesi)), "#059669", "🎯"),
        ("Bekleyen", str(len(bekleyen)), "#f59e0b", "⏳"),
        ("Tamamlanan", str(len(tamamlanan)), "#2563eb", "✅"),
        ("Ort. Puan", f"{puan_ort}/100", "#7c3aed", "📊"),
    ])
    st.markdown("---")

    # ── Bekleyen ödevler ──
    if bekleyen:
        styled_section("⏳ Bekleyen Kazanım Ödevleri", "#f59e0b")
        for ki, odev, teslim in bekleyen:
            gecikti = odev.son_teslim_tarihi and odev.son_teslim_tarihi < today_str
            ikon = "🔴" if gecikti else "📋"
            suffix = " — GECİKTİ" if gecikti else f" · Son: {odev.son_teslim_tarihi}"
            label = f"{ikon} {odev.ders} — {(ki.kazanim_metni or ki.kazanim_kodu)[:65]}{suffix}"
            with st.expander(label, expanded=False):
                _render_kazanim_odevi_coz(store, od, student, odev, teslim, ki)

    # ── Sonuçlar & Grafikler ──
    if tamamlanan:
        st.markdown("")
        styled_section("📊 Kazanım Ödevi Sonuçları", "#2563eb")

        rows = []
        for ki, odev, teslim in tamamlanan:
            metin = teslim.teslim_metni or ""
            dogru, toplam_soru = 0, 5
            m = _re.search(r"Doğru:\s*(\d+)/(\d+)", metin)
            if m:
                dogru = int(m.group(1))
                toplam_soru = int(m.group(2))
            rows.append({
                "Ders": odev.ders,
                "Kazanım": (ki.kazanim_metni or ki.kazanim_kodu)[:45],
                "Tarih": teslim.teslim_tarihi or odev.verilme_tarihi,
                "Puan": teslim.puan,
                "Doğru": dogru,
                "Yanlış": toplam_soru - dogru,
                "Toplam": toplam_soru,
            })

        df = pd.DataFrame(rows)

        # Renk paleti (Excel sunburst ile uyumlu)
        _SUNBURST_RENKLER = [
            "#4472C4", "#FFC000", "#ED7D31", "#A5A5A5",
            "#5B9BD5", "#70AD47", "#FF0000", "#264478",
        ]
        _DOGRU_RENK = "#4472C4"
        _YANLIS_RENK = "#ED7D31"

        tab_bugun, tab_toplam, tab_ders, tab_genel = st.tabs([
            "📅 Bugün", "📈 Toplamlı", "📚 Ders Bazında", "🌐 Tüm Dersler",
        ])

        # ── Bugün ──
        with tab_bugun:
            df_b = df[df["Tarih"] == today_str]
            if df_b.empty:
                styled_info_banner("Bugün tamamlanan kazanım ödevi yok.", "info")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Bugün Tamamlanan", str(len(df_b)))
                c2.metric("Doğru", str(int(df_b["Doğru"].sum())))
                c3.metric("Yanlış", str(int(df_b["Yanlış"].sum())))

                col_bar, col_sun = st.columns(2)
                with col_bar:
                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(
                        name="Doğru", x=df_b["Kazanım"], y=df_b["Doğru"],
                        marker_color=SC_COLORS[0], text=df_b["Doğru"], textposition="outside",
                    ))
                    fig_bar.add_trace(go.Bar(
                        name="Yanlış", x=df_b["Kazanım"], y=df_b["Yanlış"],
                        marker_color=SC_COLORS[1], text=df_b["Yanlış"], textposition="outside",
                    ))
                    fig_bar.update_layout(barmode="group", xaxis_tickangle=-20,
                                          legend=dict(orientation="h", y=-0.2))
                    sc_bar(fig_bar, height=360)
                    st.plotly_chart(fig_bar, use_container_width=True, config=SC_CHART_CFG)

                with col_sun:
                    # Sunburst: Kazanım → Doğru/Yanlış
                    ids, labels, parents, values, colors = ["root"], ["Bugün"], [""], [0], ["#ffffff"]
                    for i, row in df_b.iterrows():
                        kaz = row["Kazanım"]
                        ids += [kaz, f"{kaz}_D", f"{kaz}_Y"]
                        labels += [kaz, "Doğru", "Yanlış"]
                        parents += ["root", kaz, kaz]
                        values += [0, int(row["Doğru"]), int(row["Yanlış"])]
                        c_idx = list(df_b.index).index(i) % len(_SUNBURST_RENKLER)
                        colors += [_SUNBURST_RENKLER[c_idx], _DOGRU_RENK, _YANLIS_RENK]
                    fig_sun = go.Figure(go.Sunburst(
                        ids=ids, labels=labels, parents=parents, values=values,
                        branchvalues="remainder",
                        marker=dict(colors=colors, line=dict(color="white", width=2)),
                        textinfo="label+value+percent parent",
                        insidetextorientation="radial",
                    ))
                    fig_sun.update_layout(title="Sunburst — Kazanım Dağılımı",
                                          height=360, margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig_sun, use_container_width=True, config=SC_CHART_CFG)

        # ── Toplamlı ──
        with tab_toplam:
            c1, c2, c3 = st.columns(3)
            c1.metric("Toplam Tamamlanan", str(len(df)))
            c2.metric("Toplam Doğru", str(int(df["Doğru"].sum())))
            c3.metric("Toplam Yanlış", str(int(df["Yanlış"].sum())))

            df_s = df.sort_values("Tarih").copy()
            df_s["Kümülatif Doğru"] = df_s["Doğru"].cumsum()
            df_s["Kümülatif Yanlış"] = df_s["Yanlış"].cumsum()

            col_trend, col_sun2 = st.columns(2)
            with col_trend:
                fig_tr = go.Figure()
                fig_tr.add_trace(go.Scatter(
                    x=df_s["Tarih"], y=df_s["Kümülatif Doğru"], name="Kümülatif Doğru",
                    line=dict(color=_DOGRU_RENK, width=2), fill="tozeroy",
                    fillcolor=f"{_DOGRU_RENK}30",
                ))
                fig_tr.add_trace(go.Scatter(
                    x=df_s["Tarih"], y=df_s["Kümülatif Yanlış"], name="Kümülatif Yanlış",
                    line=dict(color=_YANLIS_RENK, width=2), fill="tozeroy",
                    fillcolor=f"{_YANLIS_RENK}30",
                ))
                fig_tr.update_layout(title="Kümülatif Doğru/Yanlış Trendi", height=360)
                st.plotly_chart(fig_tr, use_container_width=True, config=SC_CHART_CFG)

            with col_sun2:
                # Sunburst: Ders → Kazanım (toplam soru sayısı)
                ids2 = ["root"]
                labels2 = ["Tüm Ödevler"]
                parents2 = [""]
                values2 = [0]
                colors2 = ["#ffffff"]
                for di, ders in enumerate(sorted(df["Ders"].unique())):
                    df_dd = df[df["Ders"] == ders]
                    d_renk = _SUNBURST_RENKLER[di % len(_SUNBURST_RENKLER)]
                    ids2.append(ders)
                    labels2.append(ders)
                    parents2.append("root")
                    values2.append(0)
                    colors2.append(d_renk)
                    for _, row in df_dd.iterrows():
                        kaz_id = f"{ders}_{row['Kazanım']}"
                        ids2.append(kaz_id)
                        labels2.append(row["Kazanım"])
                        parents2.append(ders)
                        values2.append(int(row["Toplam"]))
                        colors2.append(d_renk + "99")
                fig_sun2 = go.Figure(go.Sunburst(
                    ids=ids2, labels=labels2, parents=parents2, values=values2,
                    branchvalues="remainder",
                    marker=dict(colors=colors2, line=dict(color="white", width=2)),
                    textinfo="label+value+percent parent",
                    insidetextorientation="radial",
                ))
                fig_sun2.update_layout(title="Sunburst — Ders → Kazanım Dağılımı",
                                       height=360, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_sun2, use_container_width=True, config=SC_CHART_CFG)

        # ── Ders Bazında ──
        with tab_ders:
            for di, ders in enumerate(sorted(df["Ders"].unique())):
                df_d = df[df["Ders"] == ders]
                d_renk = _SUNBURST_RENKLER[di % len(_SUNBURST_RENKLER)]
                styled_section(f"📚 {ders}", d_renk)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Kazanım Ödevi", str(len(df_d)))
                c2.metric("Toplam Doğru", str(int(df_d["Doğru"].sum())))
                c3.metric("Toplam Yanlış", str(int(df_d["Yanlış"].sum())))
                c4.metric("Ort. Puan", f"{round(df_d['Puan'].mean())}/100")

                col_b, col_s = st.columns(2)
                with col_b:
                    fig_db = go.Figure()
                    fig_db.add_trace(go.Bar(
                        name="Doğru", x=df_d["Kazanım"], y=df_d["Doğru"],
                        marker_color=SC_COLORS[0], text=df_d["Doğru"], textposition="outside",
                    ))
                    fig_db.add_trace(go.Bar(
                        name="Yanlış", x=df_d["Kazanım"], y=df_d["Yanlış"],
                        marker_color=SC_COLORS[1], text=df_d["Yanlış"], textposition="outside",
                    ))
                    fig_db.update_layout(barmode="group", xaxis_tickangle=-15)
                    sc_bar(fig_db, height=300)
                    st.plotly_chart(fig_db, use_container_width=True, config=SC_CHART_CFG)

                with col_s:
                    # Sunburst: Kazanım → Doğru/Yanlış
                    s_ids = ["root"]
                    s_lbl = [ders]
                    s_par = [""]
                    s_val = [0]
                    s_col = [d_renk]
                    for _, row in df_d.iterrows():
                        kaz = row["Kazanım"]
                        s_ids += [kaz, f"{kaz}_D", f"{kaz}_Y"]
                        s_lbl += [kaz, "Doğru", "Yanlış"]
                        s_par += ["root", kaz, kaz]
                        s_val += [0, int(row["Doğru"]), int(row["Yanlış"])]
                        s_col += [d_renk + "cc", _DOGRU_RENK, _YANLIS_RENK]
                    fig_ds = go.Figure(go.Sunburst(
                        ids=s_ids, labels=s_lbl, parents=s_par, values=s_val,
                        branchvalues="remainder",
                        marker=dict(colors=s_col, line=dict(color="white", width=2)),
                        textinfo="label+value+percent parent",
                        insidetextorientation="radial",
                    ))
                    fig_ds.update_layout(title=f"{ders} — Sunburst",
                                         height=300, margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig_ds, use_container_width=True, config=SC_CHART_CFG)
                st.markdown("")

        # ── Tüm Dersler ──
        with tab_genel:
            ozet = (df.groupby("Ders")
                    .agg(Doğru=("Doğru", "sum"), Yanlış=("Yanlış", "sum"),
                         Kazanım=("Ders", "count"), Puan=("Puan", "mean"))
                    .reset_index())
            ozet["Puan"] = ozet["Puan"].round(1)

            # ── Sunburst: Ders → Doğru / Yanlış (ana grafik) ──
            g_ids = ["root"]
            g_lbl = ["Tüm Dersler"]
            g_par = [""]
            g_val = [0]
            g_col = ["#ffffff"]
            for di, row in ozet.iterrows():
                d_renk = _SUNBURST_RENKLER[di % len(_SUNBURST_RENKLER)]
                ders = row["Ders"]
                g_ids += [ders, f"{ders}_D", f"{ders}_Y"]
                g_lbl += [ders, "Doğru", "Yanlış"]
                g_par += ["root", ders, ders]
                g_val += [0, int(row["Doğru"]), int(row["Yanlış"])]
                g_col += [d_renk, _DOGRU_RENK, _YANLIS_RENK]

            fig_main = go.Figure(go.Sunburst(
                ids=g_ids, labels=g_lbl, parents=g_par, values=g_val,
                branchvalues="remainder",
                marker=dict(colors=g_col, line=dict(color="white", width=3)),
                textinfo="label+value+percent parent",
                insidetextorientation="radial",
            ))
            fig_main.update_layout(
                title="Tüm Dersler — Ders › Doğru/Yanlış Sunburst",
                height=480, margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_main, use_container_width=True, config=SC_CHART_CFG)

            # ── Yatay bar (özet) + tablo yan yana ──
            col_h, col_tbl = st.columns([3, 2])
            with col_h:
                fig_h = go.Figure()
                fig_h.add_trace(go.Bar(
                    name="Doğru", y=ozet["Ders"], x=ozet["Doğru"], orientation="h",
                    marker_color=SC_COLORS[0], text=ozet["Doğru"], textposition="outside",
                ))
                fig_h.add_trace(go.Bar(
                    name="Yanlış", y=ozet["Ders"], x=ozet["Yanlış"], orientation="h",
                    marker_color=SC_COLORS[1], text=ozet["Yanlış"], textposition="outside",
                ))
                fig_h.update_layout(barmode="group")
                sc_bar(fig_h, height=max(280, len(ozet) * 55 + 80), horizontal=True)
                st.plotly_chart(fig_h, use_container_width=True, config=SC_CHART_CFG)

            with col_tbl:
                st.dataframe(
                    ozet.rename(columns={
                        "Kazanım": "Kazanım", "Puan": "Ort. Puan",
                        "Doğru": "✅ Doğru", "Yanlış": "❌ Yanlış",
                    }),
                    use_container_width=True, hide_index=True,
                )

    # ── Tamamlanan liste ──
    if tamamlanan:
        st.markdown("")
        styled_section("✅ Tamamlanan Kazanım Ödevleri", "#22c55e")
        for ki, odev, teslim in tamamlanan:
            puan = teslim.puan if teslim else 0.0
            renk = "#22c55e" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(
                f'<div style="background:{renk}10;border-left:4px solid {renk};'
                f'border-radius:8px;padding:8px 14px;margin-bottom:6px;">'
                f'✅ <b>{odev.ders}</b> — '
                f'{(ki.kazanim_metni or ki.kazanim_kodu)[:65]}'
                f' <span style="color:{renk};font-weight:700;">· {puan:.0f}/100</span>'
                f'</div>',
                unsafe_allow_html=True
            )


def _odev_teslim_kaydet(store: AkademikDataStore, odev, teslim,
                        student: Student, puan: float, metin: str, today_str: str):
    """OdevTeslim kaydı oluştur veya güncelle."""
    if teslim is None:
        teslim = OdevTeslim(
            odev_id=odev.id,
            student_id=student.id,
            student_adi=f"{student.ad} {student.soyad}",
        )
    teslim.durum = "teslim_edildi"
    teslim.puan = puan
    teslim.teslim_tarihi = today_str
    teslim.teslim_metni = metin
    store.save_odev_teslim(teslim)


def _render_odev_coz(store: AkademikDataStore, od: OlcmeDataStore,
                     student: Student, odev, teslim):
    """Bekleyen ödevi aç, cevapla ve otomatik değerlendir."""
    today_str = date.today().isoformat()
    gecikti = bool(odev.son_teslim_tarihi and odev.son_teslim_tarihi < today_str)
    try:
        sinif_int = student.sinif if isinstance(student.sinif, int) else int(''.join(c for c in str(student.sinif or '0') if c.isdigit()) or '0')
    except (ValueError, TypeError):
        sinif_int = 0

    # ── Ödev detay bilgisi ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**📚 Ders:** {odev.ders}")
        st.markdown(f"**📅 Verilme:** {odev.verilme_tarihi}")
    with c2:
        son_etiketi = "🔴 GECİKTİ —" if gecikti else "🟡 Son Teslim:"
        st.markdown(f"**{son_etiketi}** {odev.son_teslim_tarihi or '–'}")
        tur_map = {"test": "Test / KYT", "gunluk": "Günlük Ödev", "haftalik": "Haftalık Ödev",
                   "proje": "Proje", "arastirma": "Araştırma", "calisma_kagidi": "Çalışma Kağıdı",
                   "tekrar": "Tekrar / Pekiştirme"}
        st.markdown(f"**📝 Tür:** {tur_map.get(odev.odev_turu, odev.odev_turu)}")

    if odev.aciklama:
        st.info(odev.aciklama)
    if odev.video_link:
        st.markdown(f"📺 [Video İzle]({odev.video_link})")
    if odev.dis_link:
        st.markdown(f"🔗 [Kaynak Aç]({odev.dis_link})")

    st.markdown("---")

    # ── KYT / Test tipi: soru bankasından quiz ──
    is_test = odev.odev_turu == "test"
    quiz_qs = []

    if is_test:
        quiz_key = f"kyt_quiz_{odev.id}"
        if quiz_key not in st.session_state:
            qs = od.get_questions(grade=sinif_int, subject=odev.ders)
            iyi = [q for q in qs
                   if not q.stem.startswith("[")
                   and q.correct_choice
                   and q.choices.get("A", "").strip()
                   and q.choices.get("B", "").strip()]
            if not iyi:
                qs2 = od.get_questions(subject=odev.ders)
                iyi = [q for q in qs2
                       if not q.stem.startswith("[")
                       and q.correct_choice
                       and q.choices.get("A", "").strip()
                       and q.choices.get("B", "").strip()]
            secilen = random.sample(iyi, min(5, len(iyi))) if iyi else []
            st.session_state[quiz_key] = secilen
        quiz_qs = st.session_state.get(quiz_key, [])

    if is_test and quiz_qs:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#6366f115,#6366f108);
                    border:1px solid #6366f130;border-radius:12px;
                    padding:12px 16px;margin-bottom:16px;">
            <div style="font-weight:700;color:#6366f1;font-size:0.95rem;">
                📝 KYT — {len(quiz_qs)} Soru · Otomatik Değerlendirme
            </div>
            <div style="font-size:0.78rem;color:#64748b;margin-top:3px;">
                Her soruyu dikkatle okuyun ve cevabınızı seçin.
                Tüm soruları yanıtladıktan sonra "Teslim Et" butonuna basın.
            </div>
        </div>
        """, unsafe_allow_html=True)

        cevaplar: dict[str, str] = {}
        for i, q in enumerate(quiz_qs):
            secenekler = [f"{k}) {v}" for k, v in sorted(q.choices.items()) if v.strip()]
            st.markdown(f"**{i + 1}.** {q.stem}")
            secim = st.radio(
                f"soru_{i}",
                secenekler,
                key=f"kyt_{odev.id}_{q.id}",
                index=None,
                label_visibility="collapsed",
            )
            if secim:
                cevaplar[q.id] = secim[0]
            st.markdown("")

        cevaplanmis = len(cevaplar)
        teslim_label = (
            "✅ Teslim Et & Otomatik Değerlendir"
            if cevaplanmis == len(quiz_qs)
            else f"✅ Teslim Et  ({cevaplanmis}/{len(quiz_qs)} cevaplanmış)"
        )
        if st.button(teslim_label, key=f"kyt_submit_{odev.id}",
                     type="primary", use_container_width=True):
            dogru = sum(1 for q in quiz_qs if cevaplar.get(q.id) == q.correct_choice)
            yanlis = cevaplanmis - dogru
            bos = len(quiz_qs) - cevaplanmis
            puan = round((dogru / len(quiz_qs)) * 100)

            metin = (
                f"KYT Cevaplar: "
                + ", ".join(f"S{i+1}:{cevaplar.get(q.id, '–')}" for i, q in enumerate(quiz_qs))
                + f"\nSonuç: {dogru}/{len(quiz_qs)} doğru, Puan: {puan}/100"
            )
            _odev_teslim_kaydet(store, odev, teslim, student, float(puan), metin, today_str)

            renk = "#22c55e" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{renk}15,{renk}08);
                        border:2px solid {renk};border-radius:14px;
                        padding:24px;text-align:center;margin-top:12px;">
                <div style="font-size:2.5rem;font-weight:900;color:{renk};">{puan}</div>
                <div style="color:{renk};font-weight:700;font-size:1.1rem;">/ 100 Puan</div>
                <div style="margin-top:10px;color:#475569;font-size:0.88rem;">
                    ✅ {dogru} Doğru &nbsp;&nbsp;
                    ❌ {yanlis} Yanlış &nbsp;&nbsp;
                    ⬜ {bos} Boş
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.success("Ödev teslim edildi ve değerlendirildi!")
            # Quiz session temizle
            st.session_state.pop(f"kyt_quiz_{odev.id}", None)
            st.rerun()

    else:
        # Normal ödev veya soru bulunamadı: metin teslimi
        if is_test:
            styled_info_banner(
                "Bu ders için soru bankasında henüz soru bulunamadı. "
                "Cevabınızı metin olarak yazabilirsiniz.", "warning"
            )
        st.markdown("**Cevabınızı yazın:**")
        metin = st.text_area(
            "cevap",
            placeholder="Cevabınızı buraya yazın...",
            key=f"metin_{odev.id}",
            height=150,
            label_visibility="collapsed",
        )
        if st.button("📤 Teslim Et", key=f"teslim_{odev.id}",
                     type="primary", use_container_width=True):
            if metin.strip():
                _odev_teslim_kaydet(store, odev, teslim, student, 100.0, metin.strip(), today_str)
                st.success("Ödev teslim edildi!")
                st.rerun()
            else:
                st.warning("Lütfen bir cevap yazın.")


def _render_odevler_tab(store: AkademikDataStore, student: Student, od: OlcmeDataStore):
    """Odevler sekmesi + grafikler."""
    odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
    if not odevler:
        styled_info_banner("Bekleyen odev bulunmuyor.", "info")
        return

    teslimler = store.get_odev_teslimleri(student_id=student.id)
    teslim_map = {t.odev_id: t for t in teslimler}

    bekleyen = []
    teslim_edilen = []
    for odev in odevler:
        teslim = teslim_map.get(odev.id)
        if teslim and teslim.durum == "teslim_edildi":
            teslim_edilen.append((odev, teslim))
        else:
            bekleyen.append((odev, teslim))

    styled_stat_row([
        ("Toplam Ödev", str(len(odevler)), "#4472C4", "📝"),
        ("Bekleyen", str(len(bekleyen)), "#FFC000", "⏳"),
        ("Teslim Edilen", str(len(teslim_edilen)), "#ED7D31", "✅"),
    ])

    c1, c2 = st.columns(2)

    # --- GRAFIK: Teslim Durumu Donut ---
    with c1:
        fig_d = go.Figure(go.Pie(
            labels=["Teslim Edilen", "Bekleyen"],
            values=[len(teslim_edilen), len(bekleyen)],
            hole=0.55,
            marker=dict(colors=SC_COLORS[:2],
                        line=dict(color="#fff", width=2)),
        ))
        sc_pie(fig_d)
        st.plotly_chart(fig_d, use_container_width=True, config=SC_CHART_CFG)

    # --- GRAFIK: Ders Bazli Odev Dagilimi ---
    with c2:
        ders_count: dict[str, int] = {}
        for odev in odevler:
            ders_count[odev.ders] = ders_count.get(odev.ders, 0) + 1
        if ders_count:
            df_ders = pd.DataFrame([
                {"Ders": k, "Ödev Sayısı": v} for k, v in sorted(ders_count.items())
            ])
            df_ders_sorted = df_ders.sort_values("Ödev Sayısı", ascending=True)
            fig_ders = go.Figure(go.Bar(
                y=df_ders_sorted["Ders"], x=df_ders_sorted["Ödev Sayısı"],
                orientation="h", text=df_ders_sorted["Ödev Sayısı"],
                textposition="outside",
                marker_color=SC_COLORS[0],
            ))
            sc_bar(fig_ders, horizontal=True)
            fig_ders.update_layout(yaxis=dict(automargin=True))
            st.plotly_chart(fig_ders, use_container_width=True, config=SC_CHART_CFG)

    if bekleyen:
        styled_section("Bekleyen Ödevler", "#f59e0b")
        for odev, teslim in bekleyen:
            today_str = date.today().isoformat()
            gecikti = bool(odev.son_teslim_tarihi and odev.son_teslim_tarihi < today_str)
            ikon = "🔴" if gecikti else "📋"
            etiket = " — GECİKTİ" if gecikti else ""
            with st.expander(f"{ikon} {odev.baslik} ({odev.ders}) — Son: {odev.son_teslim_tarihi or '–'}{etiket}",
                expanded=False,
            ):
                _render_odev_coz(store, od, student, odev, teslim)

    if teslim_edilen:
        styled_section("Teslim Edilen Ödevler", "#22c55e")
        for odev, teslim in teslim_edilen:
            puan_str = f" · {teslim.puan:.0f}/100 puan" if teslim.puan else ""
            st.markdown(
                f"✅ **{odev.baslik}** ({odev.ders})"
                f" — Teslim: {teslim.teslim_tarihi}{puan_str}"
            )


def _render_sinav_sonuclari_tab(od: OlcmeDataStore, student: Student):
    """Sinav sonuclari sekmesi - premium kazanim bazli kartlar + grafikler."""
    results = od.get_results(student_id=student.id)
    if not results:
        styled_info_banner("Henuz sinav sonucu bulunmuyor.", "info")
        return

    # --- Exam ve Outcome cache (N+1 query onleme) ---
    exam_cache = {}
    outcome_cache = {}
    for r in results:
        if r.exam_id and r.exam_id not in exam_cache:
            exam_cache[r.exam_id] = od.get_exam(r.exam_id)
    for o in od.get_outcomes():
        outcome_cache[o.id] = getattr(o, "outcome_text", "") or getattr(o, "outcome_code", "")

    # --- Filtreler ---
    ders_secenekleri = sorted(set(
        exam_cache[r.exam_id].subject for r in results
        if r.exam_id in exam_cache and exam_cache[r.exam_id] and exam_cache[r.exam_id].subject
    ))
    tur_secenekleri = sorted(set(
        exam_cache[r.exam_id].exam_type for r in results
        if r.exam_id in exam_cache and exam_cache[r.exam_id] and exam_cache[r.exam_id].exam_type
    ))

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filtre_ders = st.multiselect("Ders", ders_secenekleri, key=f"vp_ss_ders_{student.id}")
    with fc2:
        filtre_tur = st.multiselect("Sınav Türü", tur_secenekleri, key=f"vp_ss_tur_{student.id}")
    with fc3:
        donem_sec = st.selectbox("Dönem", ["Tümü", "1. Dönem", "2. Dönem", "Son 30 Gün"],
                                  key=f"vp_ss_donem_{student.id}")

    # Filtre uygula
    filtered_results = results
    if filtre_ders:
        filtered_results = [r for r in filtered_results
                            if r.exam_id in exam_cache and exam_cache[r.exam_id]
                            and exam_cache[r.exam_id].subject in filtre_ders]
    if filtre_tur:
        filtered_results = [r for r in filtered_results
                            if r.exam_id in exam_cache and exam_cache[r.exam_id]
                            and exam_cache[r.exam_id].exam_type in filtre_tur]
    if donem_sec == "1. Dönem":
        filtered_results = [r for r in filtered_results
                            if r.exam_id in exam_cache and exam_cache[r.exam_id]
                            and exam_cache[r.exam_id].exam_type
                            and "1. Donem" in exam_cache[r.exam_id].exam_type]
    elif donem_sec == "2. Dönem":
        filtered_results = [r for r in filtered_results
                            if r.exam_id in exam_cache and exam_cache[r.exam_id]
                            and exam_cache[r.exam_id].exam_type
                            and "2. Donem" in exam_cache[r.exam_id].exam_type]
    elif donem_sec == "Son 30 Gün":
        from datetime import timedelta
        _30_gun_once = (datetime.now() - timedelta(days=30)).isoformat()
        filtered_results = [r for r in filtered_results
                            if r.graded_at and r.graded_at >= _30_gun_once]

    if not filtered_results:
        styled_info_banner("Filtrelere uygun sonuç bulunamadı.", "warning")
        return

    results = filtered_results

    # --- Ozet stat kartlari ---
    puanlar = [r.score for r in results if r.score is not None]
    if puanlar:
        ort = round(sum(puanlar) / len(puanlar), 1)
        en_yuksek = max(puanlar)
        toplam_dogru = sum(r.correct_count for r in results)
        toplam_yanlis = sum(r.wrong_count for r in results)
        styled_stat_row([
            ("Sınav Sayısı", str(len(results)), "#4472C4", "📝"),
            ("Ortalama", f"{ort}", "#C8952E", "📊"),
            ("En Yüksek", f"{en_yuksek:.0f}", "#16a34a", "🏆"),
            ("Toplam D/Y", f"{toplam_dogru}/{toplam_yanlis}", "#7c3aed", "🎯"),
        ])

    # --- GRAFIK: Puan Trendi ---
    if puanlar and len(puanlar) >= 2:
        c1, c2 = st.columns(2)

        with c1:
            sinav_labels = []
            for i, r in enumerate(results):
                exam = exam_cache.get(r.exam_id)
                name = exam.name[:18] if exam and exam.name else f"Sınav {i+1}"
                sinav_labels.append(name)
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=sinav_labels, y=puanlar,
                mode="lines+markers+text",
                text=[f"{p:.0f}" for p in puanlar],
                textposition="top center",
                line=dict(color="#4472C4", width=3),
                marker=dict(size=10, color="#4472C4", line=dict(color="#2F5597", width=2)),
                fill="tozeroy", fillcolor="rgba(68,114,196,0.1)",
            ))
            ort_val = sum(puanlar) / len(puanlar)
            fig_line.add_hline(y=ort_val, line_dash="dash", line_color="#FFC000", line_width=2,
                               annotation_text=f"Ort: {ort_val:.1f}",
                               annotation_font_color="#BF8F00")
            _apply_chart_layout(fig_line, "Sınav Puan Trendi")
            st.plotly_chart(fig_line, use_container_width=True, config=SC_CHART_CFG)

        with c2:
            ort = round(sum(puanlar) / len(puanlar), 1)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ort,
                title={"text": "Sınav Ortalaması", "font": {"family": "Segoe UI"}},
                delta={"reference": 70, "increasing": {"color": "#4472C4"}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#4472C4"},
                    "steps": [
                        {"range": [0, 50], "color": "#F7CBAC"},
                        {"range": [50, 70], "color": "#FFE699"},
                        {"range": [70, 85], "color": "#8FAADC"},
                        {"range": [85, 100], "color": "#4472C4"},
                    ],
                },
            ))
            _apply_chart_layout(fig_gauge, "")
            st.plotly_chart(fig_gauge, use_container_width=True, config=SC_CHART_CFG)

    # --- KATEGORİK SINAV SONUCLARI (tur bazli gruplama, en yeniden eskiye) ---
    st.markdown("")

    # Sonuclari ture gore grupla
    tur_gruplari: dict[str, list] = {}
    for r in results:
        exam = exam_cache.get(r.exam_id)
        tur = (exam.exam_type if exam and exam.exam_type else "Diger") if exam else "Diger"
        # Tur normalizasyonu
        if "Yazili" in tur or "Donem" in tur:
            kategori = "🏫 Okul Yazılıları"
        elif tur in ("LGS", "TYT", "AYT Sayısal", "AYT Esit Agirlik", "AYT Sozel"):
            kategori = "📊 LGS / TYT / AYT"
        elif tur == "Deneme":
            kategori = "📝 Deneme Sınavları"
        elif tur == "Quiz":
            kategori = "⚡ Quiz"
        elif "Kazanim" in tur:
            kategori = "🎯 Kazanım Ölçme"
        else:
            kategori = "📋 Diğer Sınavlar"
        tur_gruplari.setdefault(kategori, []).append((r, exam))

    # Kategori sirasi
    kategori_sira = ["🏫 Okul Yazılıları", "📊 LGS / TYT / AYT", "📝 Deneme Sınavları",
                      "🎯 Kazanım Ölçme", "⚡ Quiz", "📋 Diğer Sınavlar"]

    for kategori in kategori_sira:
        items = tur_gruplari.get(kategori, [])
        if not items:
            continue

        # En yeniden eskiye sirala
        items.sort(key=lambda x: x[0].graded_at or "", reverse=True)
        kat_puanlar = [r.score for r, _ in items if r.score is not None]
        kat_ort = round(sum(kat_puanlar) / len(kat_puanlar), 1) if kat_puanlar else 0
        ort_clr = "#22c55e" if kat_ort >= 70 else ("#f59e0b" if kat_ort >= 50 else "#ef4444")

        with st.expander(f"{kategori} — {len(items)} sınav | Ort: {kat_ort}", expanded=True):
            for r, exam in items:
                exam_name = exam.name if exam and exam.name else "Sınav"
                exam_type = exam.exam_type if exam else ""
                exam_subject = exam.subject if exam and exam.subject else ""
                tarih = r.graded_at[:10] if r.graded_at else ""
                tarih_fmt = f"{tarih[8:10]}.{tarih[5:7]}.{tarih[:4]}" if len(tarih) >= 10 else tarih
                puan = r.score if r.score is not None else 0
        # Puan rengi
        if puan >= 85:
            puan_renk = "#2563eb"
        elif puan >= 70:
            puan_renk = "#16a34a"
        elif puan >= 50:
            puan_renk = "#d97706"
        else:
            puan_renk = "#dc2626"
        basari_pct = round((r.correct_count / r.total_questions) * 100) if r.total_questions > 0 else 0
        type_badge = _exam_type_badge_html(exam_type)
        # Kazanim breakdown HTML
        kaz_html = _kazanim_breakdown_html(r.outcome_breakdown, outcome_cache)

        card_html = f"""<div style="border:1px solid #e2e8f0;border-radius:12px;margin-bottom:12px;
                    overflow:hidden;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                        display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;
                        background:linear-gradient(135deg,#111827,#ffffff);">
                <div>
                    <div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;">
                        <span style="font-weight:700;font-size:0.95rem;color:#475569;">{exam_name}</span>
                        {type_badge}
                    </div>
                    <div style="font-size:0.78rem;color:#64748b;margin-top:4px;">
                        {f'{exam_subject} | ' if exam_subject else ''}{tarih_fmt} | {r.total_questions} Soru
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:1.5rem;font-weight:800;color:{puan_renk};">{puan:.0f}</span>
                    <div style="font-size:0.72rem;color:#64748b;">Net: {r.net_score:.1f}</div>
                </div>
            </div>
            <div style="padding:10px 18px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
                <span style="color:#16a34a;font-weight:600;font-size:0.85rem;">✅ {r.correct_count}</span>
                <span style="color:#dc2626;font-weight:600;font-size:0.85rem;">❌ {r.wrong_count}</span>
                <span style="color:#475569;font-weight:600;font-size:0.85rem;">⬜ {r.empty_count}</span>
                <div style="flex:1;min-width:80px;background:#f1f5f9;border-radius:6px;height:8px;">
                    <div style="width:{basari_pct}%;background:linear-gradient(90deg,{puan_renk},
                        {puan_renk}cc);height:100%;border-radius:6px;transition:width 0.3s;"></div>
                </div>
                <span style="font-size:0.75rem;font-weight:700;color:{puan_renk};">%{basari_pct}</span>
            </div>
            {kaz_html}
        </div>"""
        st.markdown(card_html, unsafe_allow_html=True)

        # Sonuc belgesi PDF indirme
        _pdf_key = f"_ogr_sonuc_pdf_{r.id}"
        if st.session_state.get(_pdf_key):
            st.download_button("📄 Sonuç Belgesi İndir", data=st.session_state[_pdf_key],
                               file_name=f"sonuc_{exam_name[:20]}_{student.numara}.pdf",
                               mime="application/pdf", key=f"dl_sb_{r.id}",
                               use_container_width=True)
        else:
            if st.button("📄 Sonuç Belgesi Oluştur", key=f"gen_sb_{r.id}", use_container_width=True):
                try:
                    from views.olcme_degerlendirme_v2 import _generate_sonuc_belgesi_pdf, _load_kurum_ayarlari
                    kurum = _load_kurum_ayarlari()
                    pdf_bytes = _generate_sonuc_belgesi_pdf(r, exam, od, kurum)
                    if pdf_bytes:
                        st.session_state[_pdf_key] = pdf_bytes
                        st.rerun()
                except Exception as _e:
                    st.error(f"PDF oluşturulamadı: {_e}")

    # ═══ KARŞILAŞTIRMALI ANALİZ ═══
    _render_sinav_karsilastirma_analiz(results, exam_cache, outcome_cache, student)


def _render_sinav_karsilastirma_analiz(results, exam_cache, outcome_cache, student):
    """Karsilastirmali sinav analizi — tur bazli trend + kazanim ilerleme + yillik karsilastirma."""
    if len(results) < 2:
        return

    st.markdown("---")
    st.markdown("#### 📈 Karşılaştırmalı Sınav Analizi")

    # Yil bazli gruplama
    yil_results: dict[str, list] = {}
    for r in results:
        tarih = r.graded_at[:4] if r.graded_at and len(r.graded_at) >= 4 else "?"
        yil_results.setdefault(tarih, []).append(r)

    # Yil secimi
    yillar = sorted(yil_results.keys(), reverse=True)
    if len(yillar) > 1:
        yil_sec = st.selectbox("Akademik Yıl", ["Tümü"] + yillar, key=f"ska_yil_{student.id}")
        if yil_sec != "Tümü":
            results = yil_results.get(yil_sec, results)

    # ── TÜR BAZLI TREND — her sinav turunde puan trendi ──
    st.markdown("##### Sınav Türü Bazlı Puan Trendi")
    st.caption("Her sınav türünde puanların nasıl değiştiği — yükseliş mi düşüş mü?")

    tur_puanlar: dict[str, list[tuple]] = {}
    for r in sorted(results, key=lambda x: x.graded_at or ""):
        exam = exam_cache.get(r.exam_id)
        if not exam or r.score is None:
            continue
        tur = exam.exam_type if hasattr(exam, "exam_type") and exam.exam_type else "Diger"
        tarih = r.graded_at[:10] if r.graded_at else "?"
        tur_puanlar.setdefault(tur, []).append((tarih, r.score))

    if tur_puanlar:
        fig_trend = go.Figure()
        color_map = {}
        for i, (tur, puanlar) in enumerate(sorted(tur_puanlar.items())):
            clr = SC_COLORS[i % len(SC_COLORS)]
            color_map[tur] = clr
            tarihler = [p[0] for p in puanlar]
            skorlar = [p[1] for p in puanlar]
            fig_trend.add_trace(go.Scatter(
                x=tarihler, y=skorlar, mode="lines+markers+text",
                name=tur, line=dict(color=clr, width=2),
                marker=dict(size=8, color=clr),
                text=[f"{s:.0f}" for s in skorlar], textposition="top center",
                textfont=dict(size=8),
            ))
        fig_trend.add_hline(y=70, line_dash="dash", line_color="#22c55e40", line_width=1,
                            annotation_text="Başarı Sınırı (70)")
        fig_trend.update_layout(
            height=320, margin=dict(l=40, r=20, t=30, b=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(range=[0, 105], gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
            xaxis=dict(tickfont=dict(color="#94a3b8", size=8), tickangle=-30),
            legend=dict(font=dict(color="#c7d2fe", size=10)),
            font=dict(color="#94a3b8"),
        )
        st.plotly_chart(fig_trend, use_container_width=True, config=SC_CHART_CFG)

        # Trend yorumu — her tur icin
        for tur, puanlar in tur_puanlar.items():
            if len(puanlar) >= 2:
                ilk = puanlar[0][1]
                son = puanlar[-1][1]
                delta = son - ilk
                if delta > 5:
                    st.markdown(f"<span style='color:#22c55e;font-size:.82rem;'>📈 <b>{tur}</b>: "
                                f"+{delta:.0f} puan yükseliş ({ilk:.0f} → {son:.0f})</span>",
                                unsafe_allow_html=True)
                elif delta < -5:
                    st.markdown(f"<span style='color:#ef4444;font-size:.82rem;'>📉 <b>{tur}</b>: "
                                f"{delta:.0f} puan düşüş ({ilk:.0f} → {son:.0f})</span>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color:#475569;font-size:.82rem;'>➡️ <b>{tur}</b>: "
                                f"Stabil ({ilk:.0f} → {son:.0f})</span>",
                                unsafe_allow_html=True)

    # ── KAZANIM İLERLEME ANALİZİ ──
    st.markdown("##### Kazanım Bazlı İlerleme")
    st.caption("Kazanımlardaki doğru oranı nasıl değişiyor — hangi kazanımlar iyileşti, hangileri kötüleşti?")

    # Tum sinavlardan kazanim birlestir
    kazanim_timeline: dict[str, list[tuple]] = {}
    for r in sorted(results, key=lambda x: x.graded_at or ""):
        ob = r.outcome_breakdown if hasattr(r, "outcome_breakdown") and r.outcome_breakdown else {}
        if not isinstance(ob, dict):
            continue
        tarih = r.graded_at[:10] if r.graded_at else "?"
        for oid, data in ob.items():
            if not isinstance(data, dict):
                continue
            total = data.get("total", 0)
            correct = data.get("correct", 0)
            if total > 0:
                pct = round(correct / total * 100)
                text = outcome_cache.get(oid, data.get("text", oid))
                if len(text) > 40:
                    text = text[:37] + "..."
                kazanim_timeline.setdefault(text, []).append((tarih, pct))

    # En cok degisen kazanimlar
    kazanim_delta = []
    for kaz, points in kazanim_timeline.items():
        if len(points) >= 2:
            ilk = points[0][1]
            son = points[-1][1]
            delta = son - ilk
            kazanim_delta.append({"kazanim": kaz, "ilk": ilk, "son": son, "delta": delta})

    if kazanim_delta:
        # Yukselen
        yukselen = sorted([k for k in kazanim_delta if k["delta"] > 0], key=lambda x: -x["delta"])[:5]
        dusen = sorted([k for k in kazanim_delta if k["delta"] < 0], key=lambda x: x["delta"])[:5]

        kc1, kc2 = st.columns(2)
        with kc1:
            if yukselen:
                st.markdown("**📈 En Çok İyileşen Kazanımlar:**")
                for k in yukselen:
                    st.markdown(f"""<div style="background:#052e16;border-radius:6px;padding:6px 10px;
                    margin:2px 0;border-left:3px solid #22c55e;font-size:.78rem;">
                    <span style="color:#86efac;">{k['kazanim']}</span>
                    <span style="color:#22c55e;font-weight:700;float:right;">+{k['delta']}% ({k['ilk']}→{k['son']})</span>
                    </div>""", unsafe_allow_html=True)
        with kc2:
            if dusen:
                st.markdown("**📉 Gerileyen Kazanımlar:**")
                for k in dusen:
                    st.markdown(f"""<div style="background:#1c0505;border-radius:6px;padding:6px 10px;
                    margin:2px 0;border-left:3px solid #ef4444;font-size:.78rem;">
                    <span style="color:#fca5a5;">{k['kazanim']}</span>
                    <span style="color:#ef4444;font-weight:700;float:right;">{k['delta']}% ({k['ilk']}→{k['son']})</span>
                    </div>""", unsafe_allow_html=True)

    # ── YILLIK KARŞILAŞTIRMA ──
    if len(yillar) > 1 and len(yil_results) > 1:
        st.markdown("##### Yıllık Karşılaştırma")
        yil_ort = {}
        for yil, yr in sorted(yil_results.items()):
            puanlar_y = [r.score for r in yr if r.score is not None]
            if puanlar_y:
                yil_ort[yil] = round(sum(puanlar_y) / len(puanlar_y), 1)

        if len(yil_ort) >= 2:
            fig_yil = go.Figure()
            fig_yil.add_trace(go.Bar(
                x=list(yil_ort.keys()), y=list(yil_ort.values()),
                marker_color=[SC_COLORS[i % len(SC_COLORS)] for i in range(len(yil_ort))],
                text=[f"{v}" for v in yil_ort.values()], textposition="auto",
            ))
            fig_yil.update_layout(
                height=260, margin=dict(l=40, r=20, t=20, b=40),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(range=[0, 100], gridcolor="#1e293b", tickfont=dict(color="#94a3b8")),
                xaxis=dict(tickfont=dict(color="#c7d2fe", size=12)),
                font=dict(color="#94a3b8"),
            )
            st.plotly_chart(fig_trend if 'fig_trend' in dir() else fig_yil,
                            use_container_width=True, config=SC_CHART_CFG)

            # Yorum
            yil_list = sorted(yil_ort.items())
            if len(yil_list) >= 2:
                ilk_yil = yil_list[0]
                son_yil = yil_list[-1]
                delta = son_yil[1] - ilk_yil[1]
                if delta > 3:
                    st.success(f"📈 Yıllık ilerleme: {ilk_yil[0]} ({ilk_yil[1]}) → {son_yil[0]} ({son_yil[1]}) — **+{delta:.1f} puan yükseliş**")
                elif delta < -3:
                    st.error(f"📉 Yıllık gerileme: {ilk_yil[0]} ({ilk_yil[1]}) → {son_yil[0]} ({son_yil[1]}) — **{delta:.1f} puan düşüş**")
                else:
                    st.info(f"➡️ Stabil performans: {ilk_yil[0]} ({ilk_yil[1]}) → {son_yil[0]} ({son_yil[1]})")

    # ── GENEL ÖZET YORUM ──
    puanlar_all = [r.score for r in results if r.score is not None]
    if puanlar_all:
        ort = sum(puanlar_all) / len(puanlar_all)
        sinav_sayisi = len(puanlar_all)
        tur_sayisi = len(tur_puanlar) if tur_puanlar else 0
        kaz_iyilesen = len([k for k in kazanim_delta if k["delta"] > 0]) if kazanim_delta else 0
        kaz_gerileyen = len([k for k in kazanim_delta if k["delta"] < 0]) if kazanim_delta else 0

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
        padding:16px 20px;margin:12px 0;border:1px solid rgba(99,102,241,0.2);">
        <div style="font-size:.88rem;font-weight:700;color:#c7d2fe;margin-bottom:6px;">
        📊 Genel Analiz Özeti</div>
        <div style="font-size:.82rem;color:#0f172a;line-height:1.6;">
        • Toplam <b>{sinav_sayisi}</b> sınav, <b>{tur_sayisi}</b> farklı türde<br>
        • Genel ortalama: <b>{ort:.1f}</b> puan<br>
        • İyileşen kazanım: <b>{kaz_iyilesen}</b> | Gerileyen: <b>{kaz_gerileyen}</b><br>
        • {'📈 Genel trend: Yükseliyor' if kaz_iyilesen > kaz_gerileyen else '📉 Dikkat: Bazı alanlarda gerileme var' if kaz_gerileyen > kaz_iyilesen else '➡️ Stabil performans'}
        </div></div>""", unsafe_allow_html=True)


def _render_kyt_performans_tab(store: AkademikDataStore, student: Student):
    """KYT performans sekmesi + grafikler."""
    akademik_yil = _get_akademik_yil()
    analiz = store.get_kyt_ogrenci_analizi(student_id=student.id, akademik_yil=akademik_yil)

    if analiz["toplam"] == 0:
        styled_info_banner("Henuz KYT sorusu cevaplanmamis.", "info")
        return

    styled_stat_row([
        ("Toplam Cevap", str(analiz["toplam"]), "#4472C4", "📊"),
        ("Dogru", str(analiz["dogru"]), "#FFC000", "✅"),
        ("Yanlis", str(analiz["yanlis"]), "#ED7D31", "❌"),
        ("Başarı %", f"%{analiz['basari_yuzde']}", "#A5A5A5", "🎯"),
    ])

    c1, c2 = st.columns(2)

    # --- GRAFIK: Dogru/Yanlis Donut ---
    with c1:
        fig_dy = go.Figure(go.Pie(
            labels=["Dogru", "Yanlis"],
            values=[analiz["dogru"], analiz["yanlis"]],
            hole=0.55,
            marker=dict(colors=SC_COLORS[:2],
                        line=dict(color="#fff", width=2)),
        ))
        sc_pie(fig_dy)
        st.plotly_chart(fig_dy, use_container_width=True, config=SC_CHART_CFG)

    # --- GRAFIK: Ders Bazli Basari Bar ---
    with c2:
        if analiz["ders_performans"]:
            dp_rows = []
            for ders, dp in analiz["ders_performans"].items():
                basari = round((dp["dogru"] / dp["toplam"]) * 100, 1) if dp["toplam"] > 0 else 0
                dp_rows.append({"Ders": ders, "Başarı %": basari, "Toplam": dp["toplam"]})
            df_dp = pd.DataFrame(dp_rows)
            df_dp_sorted = df_dp.sort_values("Başarı %", ascending=True)
            fig_dp = go.Figure(go.Bar(
                y=df_dp_sorted["Ders"], x=df_dp_sorted["Başarı %"],
                orientation="h",
                text=[f"{v:.1f}%" for v in df_dp_sorted["Başarı %"]],
                textposition="outside",
                marker_color=SC_COLORS[0],
            ))
            sc_bar(fig_dp, horizontal=True)
            fig_dp.update_layout(xaxis=dict(range=[0, 110]), yaxis=dict(automargin=True))
            st.plotly_chart(fig_dp, use_container_width=True, config=SC_CHART_CFG)

    # Gunluk trend
    if analiz.get("gunluk_trend"):
        styled_section("Günlük KYT Trendi", "#4472C4")
        trend_data = []
        for entry in analiz["gunluk_trend"]:
            if isinstance(entry, dict):
                trend_data.append(entry)
        if trend_data:
            df_trend = pd.DataFrame(trend_data)
            if "tarih" in df_trend.columns and "dogru" in df_trend.columns:
                fig_t = go.Figure(go.Scatter(
                    x=df_trend["tarih"], y=df_trend["dogru"],
                    mode="lines+markers",
                    line=dict(color="#4472C4", width=3),
                    marker=dict(size=8, color="#FFC000", line=dict(color="#4472C4", width=2)),
                    fill="tozeroy", fillcolor="rgba(68,114,196,0.1)",
                ))
                _apply_chart_layout(fig_t, "Günlük Dogru Cevap Trendi")
                st.plotly_chart(fig_t, use_container_width=True, config=SC_CHART_CFG)

    # Tablo
    if analiz["ders_performans"]:
        styled_section("Detayli Tablo", "#2563eb")
        rows = []
        for ders, dp in analiz["ders_performans"].items():
            basari = round((dp["dogru"] / dp["toplam"]) * 100, 1) if dp["toplam"] > 0 else 0
            rows.append({"Ders": ders, "Toplam": dp["toplam"], "Dogru": dp["dogru"],
                         "Yanlis": dp["toplam"] - dp["dogru"], "Başarı %": basari})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)


def _render_telafi_tab(od: OlcmeDataStore, student: Student):
    """Telafi gorevleri sekmesi + grafikler."""
    telafi = od.get_telafi_tasks(student_id=student.id)
    if not telafi:
        styled_info_banner("Telafi gorevi bulunmuyor.", "info")
        return

    aktif = [t for t in telafi if t.status in ("assigned", "in_progress")]
    tamamlanan = [t for t in telafi if t.status == "completed"]

    styled_stat_row([
        ("Aktif", str(len(aktif)), "#f59e0b", "⏳"),
        ("Tamamlanan", str(len(tamamlanan)), "#22c55e", "✅"),
        ("Toplam", str(len(telafi)), "#2563eb", "📊"),
    ])

    # --- GRAFIK: Renk Bandi Dagilimi ---
    band_counts = {"RED": 0, "YELLOW": 0, "GREEN": 0, "BLUE": 0}
    for t in telafi:
        if t.color_band in band_counts:
            band_counts[t.color_band] += 1

    c1, c2 = st.columns(2)

    with c1:
        fig_band = go.Figure(go.Pie(
            labels=["Kirmizi (0-49)", "Sari (50-69)", "Yesil (70-84)", "Mavi (85-100)"],
            values=[band_counts["RED"], band_counts["YELLOW"],
                    band_counts["GREEN"], band_counts["BLUE"]],
            hole=0.55,
            marker=dict(
                colors=[SC_COLORS[4], SC_COLORS[3], SC_COLORS[7], SC_COLORS[0]],
                line=dict(color="#fff", width=2),
            ),
        ))
        sc_pie(fig_band)
        st.plotly_chart(fig_band, use_container_width=True, config=SC_CHART_CFG)

    with c2:
        fig_durum = go.Figure(go.Pie(
            labels=["Aktif", "Tamamlanan"],
            values=[len(aktif), len(tamamlanan)],
            hole=0.55,
            marker=dict(
                colors=SC_COLORS[:2],
                line=dict(color="#fff", width=2),
            ),
        ))
        sc_pie(fig_durum)
        st.plotly_chart(fig_durum, use_container_width=True, config=SC_CHART_CFG)

    band_icons = {"RED": "🔴", "YELLOW": "🟡", "GREEN": "🟢", "BLUE": "🔵"}
    if aktif:
        styled_section("Aktif Telafi Görevleri", "#f59e0b")
        for t in aktif:
            icon = band_icons.get(t.color_band, "⚪")
            st.write(f"{icon} **{t.outcome_text}** | Bant: {t.color_band} | Durum: {t.status}")


# ===================== KYT SORU COZME (OGRENCI) =====================

def _render_kyt_cozme_tab(store: AkademikDataStore, student: Student):
    """Ogrenci için KYT soru cozme arayuzu."""
    akademik_yil = _get_akademik_yil()
    tarih = st.date_input("Tarih", value=datetime.now().date(), key="panel_kyt_tarih")
    tarih_str = tarih.strftime("%Y-%m-%d")

    sorular = store.get_kyt_sorular(sinif=student.sinif, sube=student.sube, tarih=tarih_str)
    if not sorular:
        styled_info_banner(f"{tarih_str} tarihinde KYT sorusu bulunmuyor.", "info")
        return

    mevcut = store.get_kyt_cevaplar(student_id=student.id, tarih=tarih_str,
                                     sinif=student.sinif, sube=student.sube)
    cevaplanan_ids = {c.soru_id for c in mevcut}
    cevaplanmamis = [s for s in sorular if s.id not in cevaplanan_ids]

    if not cevaplanmamis:
        st.success("Bu tarihteki tum KYT sorulari cevaplanmis!")
        dogru_s = sum(1 for c in mevcut if c.dogru_mu)
        styled_stat_row([
            ("Toplam", str(len(mevcut)), "#2563eb", "📊"),
            ("Dogru", str(dogru_s), "#22c55e", "✅"),
            ("Yanlis", str(len(mevcut) - dogru_s), "#ef4444", "❌"),
        ])
        return

    st.info(f"{len(cevaplanmamis)} cevaplanmamis soru var.")

    with st.form("panel_kyt_form"):
        cevaplar = {}
        for i, soru in enumerate(cevaplanmamis):
            st.markdown(f"**Soru {i+1}** ({soru.ders}): {soru.soru_metni}")
            sec = st.radio(
                "Cevabin:",
                list(soru.secenekler.keys()),
                format_func=lambda x, s=soru: f"{x}) {s.secenekler.get(x, '', key="ogrenci_ve_m1")}",
                key=f"panel_kyt_q_{soru.id}",
                horizontal=True,
            )
            cevaplar[soru.id] = sec
            st.markdown("---")
        submitted = st.form_submit_button("Cevaplari Gonder", type="primary",
                                           use_container_width=True)

    if submitted:
        dogru_c = 0
        soru_map = {s.id: s for s in cevaplanmamis}
        for soru_id, cevap in cevaplar.items():
            soru = soru_map[soru_id]
            dogru_mu = cevap == soru.dogru_cevap
            if dogru_mu:
                dogru_c += 1
            kyt_cevap = KYTCevap(
                soru_id=soru_id, student_id=student.id, student_adi=student.tam_ad,
                sinif=student.sinif, sube=student.sube, ders=soru.ders,
                cevap=cevap, dogru_mu=dogru_mu, tarih=tarih_str, akademik_yil=akademik_yil,
            )
            store.save_kyt_cevap(kyt_cevap)
        st.success(f"Kaydedildi! Dogru: {dogru_c} | Yanlis: {len(cevaplar) - dogru_c}")
        for soru_id, cevap in cevaplar.items():
            soru = soru_map[soru_id]
            if cevap == soru.dogru_cevap:
                st.success(f"✅ {soru.ders}: Dogru!")
            else:
                st.error(f"❌ {soru.ders}: Yanlis (Dogru: {soru.dogru_cevap})")
                st.caption(f"Açıklama: {soru.aciklama}")


# ===================== GUNLUK RAPOR SEKMESİ =====================

def _render_gunluk_rapor_tab(store: AkademikDataStore, student: Student,
                              od: OlcmeDataStore, auth_user: dict):
    """Gunluk rapor - cerceveli, tablo formatinda rapor."""
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    tarih_goster = today.strftime("%d.%m.%Y")
    gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"][today.weekday()]
    akademik_yil = _get_akademik_yil()

    # ── Veri toplama ──
    attendance = store.get_attendance(student_id=student.id)
    bugun_devamsiz = [a for a in attendance if a.tarih == today_str] if attendance else []
    odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
    bugun_odev = [o for o in odevler if o.son_teslim_tarihi == today_str] if odevler else []
    kyt_cevaplar = store.get_kyt_cevaplar(
        student_id=student.id, tarih=today_str, sinif=student.sinif, sube=student.sube)
    kyt_sorular = store.get_kyt_sorular(
        sinif=student.sinif, sube=student.sube, tarih=today_str)
    kyt_dogru = sum(1 for c in kyt_cevaplar if c.dogru_mu)
    tum_ki = store.get_kazanim_isleme(sinif=student.sinif, sube=student.sube)
    bugun_ki = [k for k in tum_ki if k.tarih == today_str and k.durum in ("islendi", "kismen")]
    grades = store.get_grades(student_id=student.id)
    results = od.get_results(student_id=student.id)
    bugun_results = [r for r in results if r.graded_at and r.graded_at[:10] == today_str]
    kyt_analiz = store.get_kyt_ogrenci_analizi(student_id=student.id, akademik_yil=akademik_yil)
    teslimler = store.get_odev_teslimleri(student_id=student.id)
    teslim_ids = {t.odev_id for t in teslimler if t.durum == "teslim_edildi"}
    teslim_orani = round((len(teslim_ids) / len(odevler)) * 100, 1) if odevler else 100
    not_ort = _get_not_ortalamasi(grades) if grades else 0
    sinav_ort = round(sum(r.score for r in results if r.score) / len([r for r in results if r.score]), 1) if results and any(r.score for r in results) else 0
    kyt_basari = kyt_analiz["basari_yuzde"] if kyt_analiz["toplam"] > 0 else 0
    devamsizlik_skoru = max(0, 100 - (len(attendance) * 2 if attendance else 0))
    # ── YD Quiz bekleyen bilgisi ──
    _yd_bekleyen_quiz = 0
    _yd_quiz_names = []
    try:
        from models.yd_assessment import YdAssessmentStore as _YdGR
        _yd_gr = _YdGR()
        _si_gr = int(student.sinif) if student.sinif else 0
        _lvl_gr = f"grade{_si_gr}" if 1 <= _si_gr <= 12 else None
        if _lvl_gr:
            _yqs = _yd_gr.get_exams(level=_lvl_gr, sinif=_si_gr, sube=student.sube, category="quiz", status="started")
            _yqw = _yd_gr.get_exams(level=_lvl_gr, sinif=_si_gr, sube=student.sube, category="quiz", status="sent")
            _ya = _yd_gr.get_student_answers(student_id=student.id)
            _yd_done = {a.exam_id for a in _ya if a.status == "submitted"}
            _yd_pending = [e for e in (_yqs + _yqw) if e.id not in _yd_done]
            _yd_bekleyen_quiz = len(_yd_pending)
            _yd_quiz_names = [e.name for e in _yd_pending[:3]]
    except Exception:
        pass

    menuler = _load_veli_json(YEMEK_MENU_DOSYA)
    bugun_menu = next((m for m in menuler if m.get("tarih") == today_str), None)
    # ── Online ders verisi (rapor için) ──
    _sinif_int = student.sinif if isinstance(student.sinif, int) else int(student.sinif or 0)
    _tum_online_kayit = store.get_online_ders_kayitlari(akademik_yil=akademik_yil)
    _sinif_online_linkler = [
        l for l in store.get_online_ders_links(akademik_yil=akademik_yil)
        if l.sinif == _sinif_int and (not l.sube or l.sube == student.sube) and l.aktif
    ]
    bugun_online = [
        k for k in _tum_online_kayit
        if k.sinif == _sinif_int and (not k.sube or k.sube == student.sube)
        and k.planlanan_tarih == today_str
    ]

    # ── Yemek menusu satirlari (yeni format: kahvalti/ogle/ikindi) ──
    def _menu_tags(items, renk_bg, renk_bord, renk_text):
        return "".join(
            f'<span style="display:inline-block;background:{renk_bg};border:1px solid {renk_bord};'
            f'border-radius:6px;padding:2px 8px;margin:2px 3px 2px 0;font-size:0.78rem;color:{renk_text};">'
            f'{y}</span>' for y in items
        )

    if bugun_menu:
        # Normalize: eski format destegi
        if "kahvalti" not in bugun_menu and "yemekler" in bugun_menu:
            ogun = bugun_menu.get("ogun", "Ogle Yemegi")
            ylist = bugun_menu.get("yemekler", [])
            if "Sabah" in ogun or "Kahvalti" in ogun:
                bugun_menu = {"kahvalti": ylist, "ogle_yemegi": [], "ikindi_ara_ogun": [], "notlar": bugun_menu.get("notlar", "")}
            elif "Ikindi" in ogun:
                bugun_menu = {"kahvalti": [], "ogle_yemegi": [], "ikindi_ara_ogun": ylist, "notlar": bugun_menu.get("notlar", "")}
            else:
                bugun_menu = {"kahvalti": [], "ogle_yemegi": ylist, "ikindi_ara_ogun": [], "notlar": bugun_menu.get("notlar", "")}

        kah  = bugun_menu.get("kahvalti", [])
        ogle = bugun_menu.get("ogle_yemegi", [])
        ik   = bugun_menu.get("ikindi_ara_ogun", [])
        menu_notlar = bugun_menu.get("notlar", "")

        oguns_html = ""
        if kah:
            oguns_html += (f'<div style="margin-bottom:6px;">'
                           f'<span style="font-size:0.72rem;font-weight:700;color:#92400e;">☕ KAHVALTI</span><br>'
                           f'{_menu_tags(kah,"#fff7ed","#fed7aa","#92400e")}</div>')
        if ogle:
            oguns_html += (f'<div style="margin-bottom:6px;">'
                           f'<span style="font-size:0.72rem;font-weight:700;color:#1d4ed8;">🍽️ ÖĞLE YEMEĞİ</span><br>'
                           f'{_menu_tags(ogle,"#eff6ff","#bfdbfe","#1d4ed8")}</div>')
        if ik:
            oguns_html += (f'<div style="margin-bottom:4px;">'
                           f'<span style="font-size:0.72rem;font-weight:700;color:#166534;">🍎 İKİNDİ ARA ÖĞÜN</span><br>'
                           f'{_menu_tags(ik,"#f0fdf4","#bbf7d0","#166534")}</div>')
        if not oguns_html:
            oguns_html = '<span style="color:#475569;font-size:0.82rem;">Yemek bilgisi girilmemiş.</span>'
        if menu_notlar:
            oguns_html += f'<div style="margin-top:4px;"><span style="font-size:0.75rem;color:#78716c;">💡 {menu_notlar}</span></div>'
        menu_html_icerik = oguns_html
    else:
        menu_html_icerik = '<span style="color:#475569;font-size:0.82rem;">Bugüne ait yemek menüsü henüz girilmemiş.</span>'

    # ── Devamsizlik satiri ──
    if bugun_devamsiz:
        dev_text = ", ".join(f"{a.ders} ({a.turu})" for a in bugun_devamsiz)
        dev_renk = "#dc2626"
        dev_ikon = "Var"
    else:
        dev_text = "Devamsizlik yok"
        dev_renk = "#16a34a"
        dev_ikon = "Yok"

    # ── Online ders satirlari ──
    online_satirlar = ""
    _p_ikon_map = {
        "google_classroom": ("🏫", "Google Classroom"),
        "zoom": ("📹", "Zoom"),
        "teams": ("💼", "Teams"),
        "meet": ("🎥", "Google Meet"),
        "eba": ("📚", "EBA"),
    }
    _durum_map_online = {
        "planli": ("🟡", "#f59e0b", "Planlandı"),
        "yapiliyor": ("🟢", "#22c55e", "Yapılıyor"),
        "yapildi": ("✅", "#16a34a", "Tamamlandı"),
        "yapilmadi": ("❌", "#dc2626", "Yapılmadı"),
    }
    if bugun_online:
        for ok in sorted(bugun_online, key=lambda x: x.planlanan_saat):
            p_ikon_r, p_ad_r = _p_ikon_map.get(ok.platform, ("🔗", ok.platform or "–"))
            d_ikon_r, d_renk_r, d_text_r = _durum_map_online.get(ok.durum, ("⬜", "#94a3b8", ok.durum))
            # link bul
            link_r = ""
            if ok.link_id:
                eslesme_r = next((l for l in _sinif_online_linkler if l.id == ok.link_id), None)
                if eslesme_r:
                    link_r = eslesme_r.link
            link_html_r = f'<a href="{link_r}" target="_blank" style="font-size:0.72rem;color:#6366f1;text-decoration:none;">🔗 Bağlantı</a>' if link_r else ""
            online_satirlar += f"""<tr>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;font-weight:600;">{ok.planlanan_saat or "–"}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{ok.ders}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{p_ikon_r} {p_ad_r}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">
                    <span style="color:{d_renk_r};font-weight:600;">{d_ikon_r} {d_text_r}</span>
                </td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{link_html_r}</td>
            </tr>"""
    else:
        online_satirlar = """<tr><td colspan="5" style="padding:8px 12px;color:#94a3af;font-size:0.82rem;
            text-align:center;">Bugün online ders planlanmamış</td></tr>"""

    # ── Odev satirlari ──
    odev_satirlar = ""
    teslim_map_today = {t.odev_id: t for t in teslimler}
    if bugun_odev:
        for o in bugun_odev:
            t = teslim_map_today.get(o.id)
            d_icon = "✅" if (t and t.durum == "teslim_edildi") else "⏳"
            d_text = "Teslim Edildi" if (t and t.durum == "teslim_edildi") else "Bekliyor"
            odev_satirlar += f"""<tr>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{o.baslik}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{o.ders}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{d_icon} {d_text}</td>
            </tr>"""
    else:
        odev_satirlar = """<tr><td colspan="3" style="padding:8px 12px;color:#94a3af;font-size:0.82rem;
            text-align:center;">Bugün son teslim tarihli ödev yok</td></tr>"""

    # ── KYT satiri ──
    if kyt_sorular:
        kyt_text = f"{len(kyt_cevaplar)}/{len(kyt_sorular)} cevaplanmis | Dogru: {kyt_dogru} | Yanlis: {len(kyt_cevaplar) - kyt_dogru}"
        kyt_basari_today = round((kyt_dogru / len(kyt_cevaplar)) * 100) if kyt_cevaplar else 0
    else:
        kyt_text = "Bugün KYT sorusu yok"
        kyt_basari_today = 0

    # ── Kazanim satirlari ──
    kaz_satirlar = ""
    if bugun_ki:
        ders_gruplari: dict[str, list] = {}
        for k in bugun_ki:
            ders_gruplari.setdefault(k.ders, []).append(k)
        for ders, kazanimlar in sorted(ders_gruplari.items()):
            for k in kazanimlar:
                d_icon = "✅" if k.durum == "islendi" else "🟡"
                d_text = "Islendi" if k.durum == "islendi" else "Kismen"
                ogr = k.ogretmen_adi if k.ogretmen_adi else "-"
                kaz_satirlar += f"""<tr>
                    <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{ders}</td>
                    <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{k.kazanim_kodu}</td>
                    <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.78rem;max-width:280px;">{k.kazanim_metni[:80]}{'...' if len(k.kazanim_metni)>80 else ''}</td>
                    <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;">{d_icon} {d_text}</td>
                </tr>"""
    else:
        kaz_satirlar = """<tr><td colspan="4" style="padding:8px 12px;color:#94a3af;font-size:0.82rem;
            text-align:center;">Bugün islenen kazanim kaydi yok</td></tr>"""

    # ── Bugunku sinav sonuclari ──
    sinav_satirlar = ""
    if bugun_results:
        _exam_cache_r = {}
        _outcome_cache_r = {}
        for _o in od.get_outcomes():
            _outcome_cache_r[_o.id] = getattr(_o, "outcome_text", "") or getattr(_o, "outcome_code", "")
        for _r in bugun_results:
            if _r.exam_id not in _exam_cache_r:
                _exam_cache_r[_r.exam_id] = od.get_exam(_r.exam_id)
        for _r in bugun_results:
            _ex = _exam_cache_r.get(_r.exam_id)
            _ex_name = _ex.name[:30] if _ex and _ex.name else "Sinav"
            _ex_type = _ex.exam_type if _ex else ""
            _lbl, _tc, _tbg = EXAM_TYPE_DISPLAY.get(_ex_type, (_ex_type or "Sınav", "#64748b", "#1A2035"))
            _puan = _r.score if _r.score is not None else 0
            _pr = "#16a34a" if _puan >= 70 else ("#d97706" if _puan >= 50 else "#dc2626")
            # En dusuk basarili kazanimlar
            _kaz_ozet = ""
            if _r.outcome_breakdown:
                _sorted_kaz = sorted(_r.outcome_breakdown.items(),
                                     key=lambda x: (x[1].get("correct", 0) / max(x[1].get("total", 1), 1)))
                for _kid, _kp in _sorted_kaz[:3]:
                    _kt = _outcome_cache_r.get(_kid, _kid)[:25]
                    _kpct = round((_kp.get("correct", 0) / max(_kp.get("total", 1), 1)) * 100)
                    _kc = "#dc2626" if _kpct < 50 else ("#d97706" if _kpct < 70 else "#16a34a")
                    _kaz_ozet += (f'<span style="display:inline-block;background:#ffffff;border:1px solid {_kc}30;'
                                  f'border-radius:6px;padding:1px 6px;margin:1px 2px;font-size:0.68rem;color:{_kc};">'
                                  f'{_kt} %{_kpct}</span>')
            sinav_satirlar += f"""<tr>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;font-weight:600;">{_ex_name}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;">
                    <span style="background:{_tbg};color:{_tc};padding:1px 8px;border-radius:8px;
                        font-size:0.7rem;font-weight:700;">{_lbl}</span></td>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;font-weight:700;color:{_pr};
                    text-align:center;font-size:0.85rem;">{_puan:.0f}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;text-align:center;color:#16a34a;
                    font-size:0.82rem;">{_r.correct_count}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;text-align:center;color:#dc2626;
                    font-size:0.82rem;">{_r.wrong_count}</td>
                <td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;text-align:center;color:#475569;
                    font-size:0.82rem;">{_r.empty_count}</td>
            </tr>"""
            if _kaz_ozet:
                sinav_satirlar += f"""<tr><td colspan="6" style="padding:4px 10px 8px 10px;border-bottom:1px solid #e2e8f0;
                    background:#FFFDF5;">{_kaz_ozet}</td></tr>"""
    else:
        sinav_satirlar = """<tr><td colspan="6" style="padding:8px 12px;color:#94a3af;font-size:0.82rem;
            text-align:center;">Bugun degerlendirilen sinav yok</td></tr>"""

    # ── Not ozeti tablosu ──
    not_satirlar = ""
    if grades:
        ders_ort: dict[str, dict] = {}
        for g in grades:
            d = ders_ort.setdefault(g.ders, {"puanlar": [], "son_not": 0, "son_tarih": ""})
            d["puanlar"].append(g.puan)
            if g.tarih >= d["son_tarih"]:
                d["son_tarih"] = g.tarih
                d["son_not"] = g.puan
        for ders, info in sorted(ders_ort.items()):
            valid = [p for p in info["puanlar"] if p and p > 0]
            ort = round(sum(valid) / len(valid), 1) if valid else 0
            renk = "#16a34a" if ort >= 70 else ("#f59e0b" if ort >= 50 else "#dc2626")
            not_satirlar += f"""<tr>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;font-weight:600;">{ders}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;text-align:center;">{len(valid)}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;text-align:center;
                    color:{renk};font-weight:700;">{ort}</td>
                <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;text-align:center;">{info['son_not']:.0f}</td>
            </tr>"""
    else:
        not_satirlar = """<tr><td colspan="4" style="padding:8px 12px;color:#94a3af;font-size:0.82rem;
            text-align:center;">Henuz not kaydi yok</td></tr>"""

    # ── Genel Performans satirlari ──
    perf_items = [
        ("Not Ortalamasi", f"{not_ort}", "#16a34a" if not_ort >= 70 else ("#f59e0b" if not_ort >= 50 else "#dc2626")),
        ("Sinav Ortalamasi", f"{sinav_ort}", "#16a34a" if sinav_ort >= 70 else ("#f59e0b" if sinav_ort >= 50 else "#dc2626")),
        ("KYT Basari", f"%{kyt_basari}", "#16a34a" if kyt_basari >= 70 else ("#f59e0b" if kyt_basari >= 50 else "#dc2626")),
        ("Odev Teslim", f"%{teslim_orani}", "#16a34a" if teslim_orani >= 70 else ("#f59e0b" if teslim_orani >= 50 else "#dc2626")),
        ("Devam Skoru", f"{devamsizlik_skoru}/100", "#16a34a" if devamsizlik_skoru >= 80 else ("#f59e0b" if devamsizlik_skoru >= 60 else "#dc2626")),
        ("Toplam Devamsizlik", f"{len(attendance) if attendance else 0} gun", "#dc2626" if attendance and len(attendance) > 10 else "#64748b"),
    ]
    perf_satirlar = ""
    for label, val, renk in perf_items:
        perf_satirlar += f"""<tr>
            <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.82rem;font-weight:600;color:#475569;">{label}</td>
            <td style="padding:6px 12px;border-bottom:1px solid #e2e8f0;font-size:0.85rem;font-weight:700;
                color:{renk};text-align:right;">{val}</td>
        </tr>"""

    # ════════════════════════════════════════════════════
    #  ANA RAPOR HTML
    # ════════════════════════════════════════════════════
    _tablo_baslik = """<th style="padding:8px 12px;text-align:left;font-size:0.75rem;
        font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.5px;
        border-bottom:2px solid #334155;background:#ffffff;">"""

    # Kurum bilgisi
    try:
        from utils.shared_data import load_kurum_profili as _lkp
        _kr = _lkp()
        _kurum_adi_r = _kr.get("kurum_adi", "Smart Campus") if _kr else "Smart Campus"
    except Exception:
        _kurum_adi_r = "Smart Campus"

    rapor_html = f"""
    <div style="border:none;border-radius:16px;overflow:hidden;
                background:#ffffff;box-shadow:0 4px 24px rgba(0,0,0,0.08),0 1px 4px rgba(0,0,0,0.04);
                margin-bottom:1rem;">

        <!-- KURUMSAL RAPOR BASLIK -->
        <div style="background:linear-gradient(135deg,#0c2461 0%,#1e3a8a 30%,#2563eb 60%,#3b82f6 100%);
                    padding:24px 28px;color:white;position:relative;overflow:hidden;">
            <div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;
                        background:rgba(255,255,255,0.05);border-radius:50%"></div>
            <div style="position:absolute;bottom:-20px;left:-20px;width:80px;height:80px;
                        background:rgba(255,255,255,0.03);border-radius:50%"></div>
            <div style="font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;
                        opacity:0.6;margin-bottom:4px;">{_kurum_adi_r}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <div style="font-size:1.3rem;font-weight:800;letter-spacing:0.3px;">
                        📋 Gunluk Akademik Rapor</div>
                    <div style="font-size:0.85rem;opacity:0.85;margin-top:6px;">
                        {student.tam_ad} | {student.sinif}/{student.sube} | No: {student.numara}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.95rem;font-weight:700;">{tarih_goster}</div>
                    <div style="font-size:0.8rem;opacity:0.8;">{gun_adi}</div>
                </div>
            </div>
        </div>

        <!-- 0. YEMEK MENUSU -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;background:#ffffff;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">🍽️</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Bugunku Yemek Menusu</span>
                {"<span style='background:#f8fafc;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:600;color:#d97706;border:1px solid #fed7aa;'>Girildi</span>" if bugun_menu else "<span style='background:#f1f5f9;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:600;color:#475569;'>Girilmedi</span>"}
            </div>
            <div style="padding:10px 14px;background:#f8fafc;border-radius:8px;border-left:3px solid #f59e0b;">
                {menu_html_icerik}
            </div>
        </div>

        <!-- 1. DEVAMSIZLIK -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:0.9rem;">📅</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Devamsizlik Durumu</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                        background:#ffffff;border-radius:8px;border-left:3px solid {dev_renk};">
                <span style="font-weight:700;color:{dev_renk};font-size:0.85rem;">{dev_ikon}</span>
                <span style="color:#475569;font-size:0.82rem;">{dev_text}</span>
            </div>
        </div>

        <!-- 2. ONLINE DERSLER -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">💻</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Bugunku Online Dersler</span>
                <span style="background:#eef2ff;padding:2px 8px;border-radius:10px;
                      font-size:0.7rem;font-weight:600;color:#6366f1;">{len(bugun_online)} ders</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr>
                    {_tablo_baslik}Saat</th>
                    {_tablo_baslik}Ders</th>
                    {_tablo_baslik}Platform</th>
                    {_tablo_baslik}Durum</th>
                    {_tablo_baslik}Bağlantı</th>
                </tr></thead>
                <tbody>{online_satirlar}</tbody>
            </table>
        </div>

        <!-- 3. BUGUNKU ODEVLER -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">📋</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Bugunku Odevler</span>
                <span style="background:#f1f5f9;padding:2px 8px;border-radius:10px;
                      font-size:0.7rem;font-weight:600;color:#64748b;">{len(bugun_odev)} odev</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr>
                    {_tablo_baslik}Odev</th>
                    {_tablo_baslik}Ders</th>
                    {_tablo_baslik}Durum</th>
                </tr></thead>
                <tbody>{odev_satirlar}</tbody>
            </table>
        </div>

        <!-- 4. KYT SONUCLARI -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:0.9rem;">📝</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">KYT Sonuclari</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                        background:#ffffff;border-radius:8px;border-left:3px solid #7c3aed;">
                <span style="color:#475569;font-size:0.82rem;">{kyt_text}</span>
                {"<span style='margin-left:auto;background:#7c3aed;color:white;padding:2px 10px;border-radius:10px;font-size:0.75rem;font-weight:700;'>%" + str(kyt_basari_today) + "</span>" if kyt_cevaplar else ""}
            </div>
        </div>

        <!-- 4.5 SINAV SONUCLARI -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">📊</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Sinav Sonuclari</span>
                <span style="background:#C8952E;color:white;padding:2px 8px;border-radius:10px;
                      font-size:0.7rem;font-weight:600;">{len(bugun_results)} sonuc</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr>
                    {_tablo_baslik}Sinav</th>
                    {_tablo_baslik}Tur</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">Puan</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">D</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">Y</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">B</th>
                </tr></thead>
                <tbody>{sinav_satirlar}</tbody>
            </table>
        </div>

        <!-- 4b. YD QUIZ BILDIRIMI -->
        {"" if _yd_bekleyen_quiz == 0 else f'''
        <div style="padding:14px 24px;border-bottom:1px solid #1e293b;
            background:linear-gradient(135deg,#1e1b4b10,#4338ca10);">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span style="font-size:0.9rem;">🌍</span>
                <span style="font-weight:700;color:#818cf8;font-size:0.9rem;">Bekleyen Ingilizce Quiz</span>
                <span style="background:#4338ca20;color:#818cf8;padding:2px 8px;border-radius:10px;
                      font-size:0.7rem;font-weight:700;">{_yd_bekleyen_quiz} quiz</span>
            </div>
            {"".join(f'<div style="padding:4px 0;font-size:0.82rem;color:#a5b4fc;">📝 {n}</div>' for n in _yd_quiz_names)}
            <div style="font-size:0.75rem;color:#64748b;margin-top:4px;">
            Yabanci Dil sekmesinden quiz cozebilirsiniz</div>
        </div>
        '''}

        <!-- 5. ISLENEN KAZANIMLAR -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">📚</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Islenen Kazanimlar</span>
                <span style="background:#f1f5f9;padding:2px 8px;border-radius:10px;
                      font-size:0.7rem;font-weight:600;color:#64748b;">{len(bugun_ki)} kazanim</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr>
                    {_tablo_baslik}Ders</th>
                    {_tablo_baslik}Kod</th>
                    {_tablo_baslik}Kazanim</th>
                    {_tablo_baslik}Durum</th>
                </tr></thead>
                <tbody>{kaz_satirlar}</tbody>
            </table>
        </div>

        <!-- 6. NOT OZETI -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">📊</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Ders Bazli Not Ozeti</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <thead><tr>
                    {_tablo_baslik}Ders</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">Not Sayisi</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">Ortalama</th>
                    <th style="padding:8px 12px;text-align:center;font-size:0.75rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.5px;
                        border-bottom:2px solid #334155;background:#ffffff;">Son Not</th>
                </tr></thead>
                <tbody>{not_satirlar}</tbody>
            </table>
        </div>

        <!-- 7. GENEL PERFORMANS -->
        <div style="padding:16px 24px;border-bottom:1px solid #1e293b;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:0.9rem;">🎯</span>
                <span style="font-weight:700;color:#0f172a;font-size:0.9rem;">Genel Performans Ozeti</span>
            </div>
            <table style="width:100%;border-collapse:collapse;">
                <tbody>{perf_satirlar}</tbody>
            </table>
        </div>

        <!-- FOOTER -->
        <div style="padding:12px 24px;text-align:center;background:#ffffff;">
            <div style="font-size:0.7rem;color:#475569;">
                {_kurum_adi_r} — Gunluk Akademik Rapor Sistemi | {tarih_goster}
            </div>
        </div>

    </div>
    """
    # Ders sayisi hesapla (not tablosu icin)
    _ders_sayisi = len(set(g.ders for g in grades)) if grades else 0
    # Yukseklik: baslik + sectionlar + tablolar
    _menu_h = max(80, len(bugun_menu.get("yemekler", [])) * 22 + 70) if bugun_menu else 70
    _online_h = max(60, len(bugun_online) * 40 + 70)
    _rapor_h = 100 + _menu_h + _online_h + 80 + max(80, len(bugun_odev) * 40 + 80) + 80
    _sinav_h = max(80, len(bugun_results) * 60 + 80)  # sinav sonuclari + kazanim ozet satirlari
    _rapor_h += _sinav_h
    _rapor_h += max(80, len(bugun_ki) * 40 + 80)
    _rapor_h += max(100, _ders_sayisi * 40 + 80)
    _rapor_h += len(perf_items) * 40 + 80
    _stc.html(rapor_html, height=_rapor_h, scrolling=False)

    # ── Radar Grafik ──
    st.markdown("")
    fig_radar = go.Figure(go.Scatterpolar(
        r=[not_ort, sinav_ort, kyt_basari, teslim_orani, devamsizlik_skoru],
        theta=["Not Ort", "Sinav Ort", "KYT Basari", "Odev Teslim", "Devam Skoru"],
        fill="toself",
        fillcolor="rgba(68,114,196,0.25)",
        marker=dict(color="#4472C4", size=7),
        line=dict(color="#4472C4", width=2),
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="#E0E0E0", linecolor="#BFBFBF"),
            angularaxis=dict(gridcolor="#E0E0E0", linecolor="#BFBFBF"),
            bgcolor="white",
        ),
        showlegend=False,
    )
    _apply_chart_layout(fig_radar, "Genel Akademik Performans")
    st.plotly_chart(fig_radar, use_container_width=True, config=SC_CHART_CFG)

    # ── KYT Odevi ──
    bugun_islenen = bugun_ki
    _render_kazanim_kyt_odevi(store, student, bugun_islenen, today_str, akademik_yil,
                               auth_user)

    st.markdown("---")
    _render_ai_analiz_section(store, student, od)


# ===================== KAZANIM KYT ÖDEVİ (OTOMATİK) =====================

def _auto_generate_kyt_for_kazanimlar(store: AkademikDataStore, kazanimlar: list,
                                       sinif: int, sube: str, akademik_yil: str,
                                       today_str: str) -> int:
    """Islenen kazanimlar için otomatik 2'ser soru uret ve KYTSoru olarak kaydet.
    Zaten uretilmis kazanimlar için tekrar uretmez. Uretilen soru sayisini dondurur."""
    from views.akademik_takip import _generate_kyt_questions

    # KYT derslerini filtrele (kademeye uygun)
    kademe = _get_kademe(sinif)
    kyt_dersler = KYT_DERSLER.get(kademe, [])

    # Bugun bu sinif/sube için mevcut KYT sorulari
    mevcut_sorular = store.get_kyt_sorular(sinif=sinif, sube=sube, tarih=today_str)
    mevcut_kazanim_kodlari = {s.kazanim_kodu for s in mevcut_sorular}

    # Sadece KYT derslerinde olan ve henuz sorusu uretilmemis kazanimlari sec
    uretilecek = [k for k in kazanimlar
                  if k.ders in kyt_dersler and k.kazanim_kodu not in mevcut_kazanim_kodlari]

    if not uretilecek:
        return 0

    toplam_uretilen = 0
    progress = st.progress(0, text="KYT sorulari uretiliyor...")

    for idx, kaz in enumerate(uretilecek):
        progress.progress((idx + 1) / len(uretilecek),
                          text=f"{kaz.ders}: {kaz.kazanim_kodu} için sorular uretiliyor...")

        sorular = _generate_kyt_questions(kaz.ders, sinif, kaz.kazanim_metni)
        for s in sorular:
            kyt_soru = KYTSoru(
                sinif=sinif,
                sube=sube,
                ders=kaz.ders,
                kazanim_kodu=kaz.kazanim_kodu,
                kazanim_metni=kaz.kazanim_metni,
                soru_metni=s.get("metin", ""),
                secenekler=s.get("secenekler", {}),
                dogru_cevap=s.get("dogru", "A"),
                aciklama=s.get("aciklama", ""),
                tarih=today_str,
                kaynak_kazanim_id=kaz.id,
                akademik_yil=akademik_yil,
            )
            store.save_kyt_soru(kyt_soru)
            toplam_uretilen += 1

    progress.empty()
    return toplam_uretilen


def _render_kazanim_kyt_odevi(store: AkademikDataStore, student: Student,
                               bugun_islenen: list, today_str: str,
                               akademik_yil: str, auth_user: dict):
    """Kazanim KYT odevi: otomatik soru uretimi, online cevaplama, degerlendirme, dashboard."""
    styled_section("Kazanim KYT Ödevi", "#7c3aed")

    if not bugun_islenen:
        styled_info_banner("Bugün islenen kazanim yok, KYT odevi olusturulmadi.", "info")
        return

    # --- 1) Otomatik soru uretimi ---
    mevcut_sorular = store.get_kyt_sorular(sinif=student.sinif, sube=student.sube,
                                            tarih=today_str)

    # Bugun islenen kazanim kodlari
    kademe = _get_kademe(student.sinif)
    kyt_dersler = KYT_DERSLER.get(kademe, [])
    kyt_kazanimlar = [k for k in bugun_islenen if k.ders in kyt_dersler]

    if not kyt_kazanimlar:
        styled_info_banner("Bugün islenen kazanimlar KYT derslerinde degil.", "info")
        return

    # Sorusu uretilmemis kazanimlari kontrol et
    mevcut_kaz_kodlari = {s.kazanim_kodu for s in mevcut_sorular}
    eksik_kazanimlar = [k for k in kyt_kazanimlar if k.kazanim_kodu not in mevcut_kaz_kodlari]

    if eksik_kazanimlar:
        st.info(f"{len(eksik_kazanimlar)} kazanim için soru uretilmesi gerekiyor "
                f"(toplam {len(eksik_kazanimlar) * 2} soru).")
        if st.button("Sorulari Otomatik Uret", key="auto_kyt_generate",
                     type="primary", use_container_width=True):
            uretilen = _auto_generate_kyt_for_kazanimlar(
                store, eksik_kazanimlar, student.sinif, student.sube,
                akademik_yil, today_str
            )
            if uretilen > 0:
                st.success(f"{uretilen} soru basariyla uretildi!")
                st.rerun()
            else:
                st.warning("Soru uretilemedi. API anahtarini kontrol edin.")
            return

    # Sorulari yeniden yükle (uretildiyse)
    sorular = store.get_kyt_sorular(sinif=student.sinif, sube=student.sube, tarih=today_str)
    # Sadece bugunku kazanimlara ait sorulari filtrele
    kaz_kodlari = {k.kazanim_kodu for k in kyt_kazanimlar}
    sorular = [s for s in sorular if s.kazanim_kodu in kaz_kodlari]

    if not sorular:
        styled_info_banner("Bugün için KYT sorusu bulunmuyor.", "info")
        return

    # --- 2) Mevcut cevaplari kontrol et ---
    mevcut_cevaplar = store.get_kyt_cevaplar(student_id=student.id, tarih=today_str)
    cevaplanan_ids = {c.soru_id for c in mevcut_cevaplar}
    cevaplanmamis = [s for s in sorular if s.id not in cevaplanan_ids]
    cevaplanan = [s for s in sorular if s.id in cevaplanan_ids]

    # --- Stat kartlari ---
    toplam_soru = len(sorular)
    cevaplanan_s = len(cevaplanan)
    dogru_s = sum(1 for c in mevcut_cevaplar if c.dogru_mu and c.soru_id in kaz_kodlari or c.soru_id in {s.id for s in sorular})
    dogru_s = sum(1 for c in mevcut_cevaplar if c.dogru_mu)
    yanlis_s = cevaplanan_s - dogru_s
    ders_sayisi = len(set(s.ders for s in sorular))

    styled_stat_row([
        ("Ders", str(ders_sayisi), "#4472C4", "📚"),
        ("Toplam Soru", str(toplam_soru), "#2563eb", "📝"),
        ("Cevaplanan", f"{cevaplanan_s}/{toplam_soru}", "#f59e0b", "✏️"),
        ("Dogru", str(dogru_s), "#22c55e", "✅"),
        ("Yanlis", str(yanlis_s), "#ef4444", "❌"),
    ])

    st.markdown("")

    # --- 3) Online cevaplama formu ---
    if cevaplanmamis:
        with st.expander(f"📝 Cevaplanmamis Sorular ({len(cevaplanmamis)})", expanded=True):
            # Derse gore grupla
            ders_grp: dict[str, list] = {}
            for s in cevaplanmamis:
                ders_grp.setdefault(s.ders, []).append(s)

            with st.form("kazanim_kyt_form", clear_on_submit=False):
                cevaplar: dict[str, str] = {}
                for ders_adi, ders_sorulari in sorted(ders_grp.items()):
                    st.markdown(f"### 📚 {ders_adi}")
                    for i, soru in enumerate(ders_sorulari):
                        st.markdown(f"**Soru {i + 1}** | Kazanim: `{soru.kazanim_kodu}`")
                        st.markdown(f"> {soru.soru_metni}")
                        sec = st.radio(
                            f"Cevabin ({soru.id}):",
                            list(soru.secenekler.keys()),
                            format_func=lambda x, s=soru: f"{x}) {s.secenekler.get(x, '', key="ogrenci_ve_m2")}",
                            key=f"kyt_odev_{soru.id}",
                            horizontal=True,
                        )
                        cevaplar[soru.id] = sec
                        st.markdown("---")

                gonder = st.form_submit_button("Cevaplari Gonder", type="primary",
                                                use_container_width=True)

            if gonder:
                soru_map = {s.id: s for s in cevaplanmamis}
                yeni_dogru = 0
                yeni_yanlis = 0
                for soru_id, cevap in cevaplar.items():
                    soru = soru_map[soru_id]
                    dogru_mu = cevap == soru.dogru_cevap
                    if dogru_mu:
                        yeni_dogru += 1
                    else:
                        yeni_yanlis += 1

                    kyt_cevap = KYTCevap(
                        soru_id=soru_id,
                        student_id=student.id,
                        student_adi=student.tam_ad,
                        sinif=student.sinif,
                        sube=student.sube,
                        ders=soru.ders,
                        cevap=cevap,
                        dogru_mu=dogru_mu,
                        tarih=today_str,
                        akademik_yil=akademik_yil,
                    )
                    store.save_kyt_cevap(kyt_cevap)

                st.success(f"Kaydedildi! ✅ Dogru: {yeni_dogru} | ❌ Yanlis: {yeni_yanlis}")

                # Anlik geri bildirim
                for soru_id, cevap in cevaplar.items():
                    soru = soru_map[soru_id]
                    if cevap == soru.dogru_cevap:
                        st.success(f"✅ {soru.ders} - {soru.kazanim_kodu}: Dogru!")
                    else:
                        st.error(f"❌ {soru.ders} - {soru.kazanim_kodu}: Yanlis "
                                 f"(Dogru cevap: {soru.dogru_cevap})")
                        if soru.aciklama:
                            st.caption(f"Açıklama: {soru.aciklama}")
                st.rerun()
    else:
        styled_info_banner("Tüm sorular cevaplanmis!", "success")

    # --- 4) Ders bazli dashboard + grafikler ---
    if cevaplanan_s > 0:
        styled_section("Ders Bazli Performans", "#4472C4")

        # Ders bazli istatistikleri hesapla
        cevap_map = {c.soru_id: c for c in mevcut_cevaplar}
        ders_stats: dict[str, dict] = {}
        for s in sorular:
            c = cevap_map.get(s.id)
            if not c:
                continue
            ds = ders_stats.setdefault(s.ders, {"kazanim": set(), "soru": 0,
                                                  "dogru": 0, "yanlis": 0})
            ds["kazanim"].add(s.kazanim_kodu)
            ds["soru"] += 1
            if c.dogru_mu:
                ds["dogru"] += 1
            else:
                ds["yanlis"] += 1

        # Tablo
        tablo_rows = []
        for ders_adi, ds in sorted(ders_stats.items()):
            basari = round((ds["dogru"] / ds["soru"]) * 100) if ds["soru"] > 0 else 0
            tablo_rows.append({
                "Ders": ders_adi,
                "Kazanim": len(ds["kazanim"]),
                "Soru": ds["soru"],
                "Dogru": ds["dogru"],
                "Yanlis": ds["yanlis"],
                "Başarı %": basari,
            })

        if tablo_rows:
            st.dataframe(pd.DataFrame(tablo_rows), use_container_width=True, hide_index=True)

        # Grafikler
        gc1, gc2 = st.columns(2)

        with gc1:
            # Ders bazli yatay bar chart - dogru/yanlis
            ders_adlari = [r["Ders"] for r in tablo_rows]
            dogru_vals = [r["Dogru"] for r in tablo_rows]
            yanlis_vals = [r["Yanlis"] for r in tablo_rows]

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=ders_adlari, x=dogru_vals, name="Dogru",
                orientation="h", marker_color=SC_COLORS[0],
                text=dogru_vals, textposition="outside",
            ))
            fig_bar.add_trace(go.Bar(
                y=ders_adlari, x=yanlis_vals, name="Yanlis",
                orientation="h", marker_color=SC_COLORS[1],
                text=yanlis_vals, textposition="outside",
            ))
            fig_bar.update_layout(barmode="stack")
            sc_bar(fig_bar, height=300, horizontal=True)
            st.plotly_chart(fig_bar, use_container_width=True, config=SC_CHART_CFG)

        with gc2:
            # Genel basari donut
            fig_donut = go.Figure(go.Pie(
                labels=["Dogru", "Yanlis"],
                values=[dogru_s, yanlis_s],
                hole=0.55,
                marker=dict(
                    colors=SC_COLORS[:2],
                    line=dict(color="#fff", width=2),
                ),
            ))
            sc_pie(fig_donut)
            st.plotly_chart(fig_donut, use_container_width=True, config=SC_CHART_CFG)

        # Ders bazli basari yuzde bar
        if len(tablo_rows) > 1:
            basari_vals = [r["Başarı %"] for r in tablo_rows]
            renkler = [SC_COLORS[0] if b >= 70 else SC_COLORS[3] if b >= 50
                       else SC_COLORS[4] for b in basari_vals]
            fig_basari = go.Figure(go.Bar(
                y=ders_adlari, x=basari_vals,
                orientation="h",
                marker_color=renkler,
                text=[f"%{b}" for b in basari_vals],
                textposition="outside",
            ))
            sc_bar(fig_basari, height=280, horizontal=True)
            fig_basari.update_xaxes(range=[0, 100])
            st.plotly_chart(fig_basari, use_container_width=True, config=SC_CHART_CFG)

    # --- 5) AI destekli tavsiye ---
    if cevaplanan_s > 0:
        _render_kyt_ai_tavsiye(store, student, sorular, mevcut_cevaplar, tablo_rows
                               if cevaplanan_s > 0 else [])


def _render_kyt_ai_tavsiye(store: AkademikDataStore, student: Student,
                            sorular: list, cevaplar: list,
                            ders_stats_rows: list):
    """KYT sonuclarina gore AI destekli tavsiye ve yonlendirme."""
    with st.expander("🤖 AI Destekli KYT Tavsiyesi", expanded=False):
        st.caption("Yapay zeka bugunun KYT sonuclarini analiz eder ve kisisel tavsiyeler sunar.")

        ss_key = "kyt_ai_tavsiye"
        if ss_key not in st.session_state:
            st.session_state[ss_key] = None

        if st.button("Tavsiye Oluştur", key="kyt_tavsiye_btn", type="primary"):
            try:
                from views.ai_destek import _get_client
                client = _get_client()
                if not client:
                    st.warning("OpenAI API anahtari bulunamadı.")
                    return
            except Exception:
                st.warning("AI servisi kullanilamiyor.")
                return

            # Sonuc ozeti olustur
            soru_map = {s.id: s for s in sorular}
            yanlis_detay = []
            for c in cevaplar:
                if not c.dogru_mu:
                    s = soru_map.get(c.soru_id)
                    if s:
                        yanlis_detay.append(
                            f"- {s.ders} | {s.kazanim_kodu}: {s.kazanim_metni} "
                            f"(Verdigi cevap: {c.cevap}, Dogru: {s.dogru_cevap})"
                        )

            ders_ozet = "\n".join(
                f"- {r['Ders']}: {r['Soru']} soru, {r['Dogru']} dogru, "
                f"{r['Yanlis']} yanlis, %{r['Başarı %']} basari"
                for r in ders_stats_rows
            )

            prompt = (
                f"Öğrenci: {student.tam_ad} ({student.sinif}. sinif {student.sube} subesi)\n\n"
                f"BUGUNUN KYT SONUCLARI:\n{ders_ozet}\n\n"
                f"YANLIS YAPILANLAR:\n" + ("\n".join(yanlis_detay) if yanlis_detay else "Hepsi dogru!") +
                f"\n\nLutfen su basliklar altinda kisa ve net tavsiyeler ver:\n"
                f"1. Genel Değerlendirme (2-3 cumle)\n"
                f"2. Güçlü Yonler\n"
                f"3. Gelistirilmesi Gereken Alanlar\n"
                f"4. Veli İçin Oneriler (evde nasil destek olabilir)\n"
                f"5. Öğrenci İçin Somut Calisma Tavsiyeleri\n"
                f"Turkce yaz, samimi ve motive edici ol."
            )

            with st.spinner("AI tavsiye olusturuyor..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system",
                             "content": "Sen deneyimli bir egitim danismanisin. "
                                        "Öğrenci KYT sonuclarini analiz edip kisisel tavsiyeler veriyorsun. "
                                        "Turkce yaz, kisa ve net ol."},
                            {"role": "user", "content": prompt},
                        ],
                        max_tokens=800,
                        temperature=0.7,
                    )
                    st.session_state[ss_key] = response.choices[0].message.content or ""
                except Exception as e:
                    st.error(f"AI hatasi: {e}")

        if st.session_state[ss_key]:
            st.markdown(st.session_state[ss_key])


def _render_ai_analiz_section(store: AkademikDataStore, student: Student,
                               od: OlcmeDataStore):
    """AI destekli ogrenci analizi."""
    with st.expander("🤖 AI Destekli Akademik Analiz", expanded=False):
        st.caption("Yapay zeka cocugunuzun akademik durumunu analiz eder ve oneriler sunar.")
        if "veli_ai_analiz" not in st.session_state:
            st.session_state.veli_ai_analiz = None
        if st.button("Analiz Oluştur", key="veli_ai_analiz_btn", type="primary"):
            with st.spinner("AI analiz olusturuyor..."):
                analiz_text = _generate_ai_student_analysis(store, student, od)
                st.session_state.veli_ai_analiz = analiz_text
        if st.session_state.veli_ai_analiz:
            st.markdown(st.session_state.veli_ai_analiz)


def _generate_ai_student_analysis(store: AkademikDataStore, student: Student,
                                   od: OlcmeDataStore) -> str:
    """Tum ogrenci verisini topla ve AI ile analiz et."""
    try:
        from views.ai_destek import _get_client
        client = _get_client()
        if not client:
            return "OpenAI API anahtari bulunamadı. Analiz olusturulamadi."
    except Exception:
        return "AI servisi su anda kullanilamiyor."

    grades = store.get_grades(student_id=student.id)
    attendance = store.get_attendance(student_id=student.id)
    results = od.get_results(student_id=student.id)
    akademik_yil = _get_akademik_yil()
    kyt_analiz = store.get_kyt_ogrenci_analizi(student_id=student.id, akademik_yil=akademik_yil)
    telafi = od.get_telafi_tasks(student_id=student.id)
    odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
    teslimler = store.get_odev_teslimleri(student_id=student.id)
    risk_alerts = store.get_risk_alerts(student_id=student.id, status="active")

    ctx = [f"Öğrenci: {student.tam_ad} | Sınıf: {student.sinif}/{student.sube}"]
    if grades:
        ders_ort: dict[str, list] = {}
        for g in grades:
            ders_ort.setdefault(g.ders, []).append(g.puan)
        ctx.append("\nNOTLAR:")
        for ders, puanlar in ders_ort.items():
            valid = [p for p in puanlar if p and p > 0]
            ort = round(sum(valid) / len(valid), 1) if valid else 0
            ctx.append(f"  {ders}: Ortalama {ort} ({len(valid)} not)")
    if attendance:
        ozurlu = sum(1 for a in attendance if a.turu == "ozurlu")
        ozursuz = sum(1 for a in attendance if a.turu == "ozursuz")
        ctx.append(f"\nDEVAMSIZLIK: Toplam {len(attendance)} gun (Ozurlu: {ozurlu}, Ozursuz: {ozursuz})")
    if results:
        puanlar = [r.score for r in results if r.score is not None]
        if puanlar:
            ctx.append(f"\nSINAV: {len(puanlar)} sinav, Ort: {round(sum(puanlar)/len(puanlar),1)}")
    if kyt_analiz["toplam"] > 0:
        ctx.append(f"\nKYT: {kyt_analiz['toplam']} soru, Başarı: %{kyt_analiz['basari_yuzde']}")
    teslim_ids = {t.odev_id for t in teslimler if t.durum == "teslim_edildi"}
    bekleyen = sum(1 for o in odevler if o.id not in teslim_ids)
    ctx.append(f"\nODEV: {len(odevler)} aktif, {bekleyen} bekleyen")
    if telafi:
        aktif_telafi = [t for t in telafi if t.status in ("assigned", "in_progress")]
        ctx.append(f"\nTELAFI: {len(aktif_telafi)} aktif")
    if risk_alerts:
        ctx.append(f"\nRISK: {len(risk_alerts)} aktif uyari")

    prompt = f"""Sen bir egitim danisman yapay zekasin. Asagidaki ogrenci verilerini analiz et
ve veliye yonelik kisa bir rapor olustur. Turkce yaz.

Rapor formati:
1. Genel Degerlendirme (2-3 cumle)
2. Guclu Alanlar (madde isareti)
3. Gelisim Alanlari (madde isareti)
4. Veliye Oneriler (madde isareti)

Ogrenci Verileri:
{chr(10).join(ctx)}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": __import__('utils.ai_rules', fromlist=['inject_rules']).inject_rules(
                    "Sen bir egitim danismanisin. Kisa, net ve yapici analizler yapiyorsun.", short=True)},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024, temperature=0.7,
        )
        return response.choices[0].message.content or "Analiz olusturulamadi."
    except Exception as e:
        return f"AI analiz hatasi: {e}"


# ===================== AKADEMİK YÖNLENDİRME SEKMESİ =====================

def _render_akademik_yonlendirme_tab(store: AkademikDataStore, student: Student):
    """Akademik yonlendirme - salt okunur veli gorunumu."""
    _render_risk_alerts_readonly(store, student)
    _render_destek_planlari_readonly(store, student)
    _render_ogretmen_onerileri_readonly(store, student)
    _render_mudahaleler_readonly(store, student)


def _render_risk_alerts_readonly(store: AkademikDataStore, student: Student):
    styled_section("Risk Uyarilari", "#ef4444")
    alerts = store.get_risk_alerts(student_id=student.id, status="active")
    if not alerts:
        styled_info_banner("Aktif risk uyarisi bulunmuyor.", "success")
        return
    severity_icons = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
    alert_type_labels = {
        "attendance": "Devamsızlık", "grade_decline": "Not Dususu",
        "homework": "Ödev Takibi", "exam_trend": "Sınav Trendi", "composite": "Genel",
    }
    for alert in alerts:
        icon = severity_icons.get(alert.severity, "⚪")
        sev_label = RISK_SEVERITY_LABELS.get(alert.severity, alert.severity)
        type_label = alert_type_labels.get(alert.alert_type, alert.alert_type)
        with st.expander(f"{icon} {type_label} - Seviye: {sev_label}", expanded=False):
            st.write(alert.details or "Detay bilgisi yok")
            st.caption(f"Oluşturma: {alert.created_at[:10] if alert.created_at else '-'}")


def _render_destek_planlari_readonly(store: AkademikDataStore, student: Student):
    styled_section("Destek Planlari", "#7c3aed")
    planlar = store.get_destek_planlari(student_id=student.id, status="active")
    if not planlar:
        styled_info_banner("Aktif destek plani bulunmuyor.", "info")
        return
    for plan in planlar:
        with st.expander(f"📋 {plan.plan_name}", expanded=False):
            st.write(f"**Başlangıç:** {plan.start_date or '-'} | **Bitis:** {plan.end_date or '-'}")
            try:
                goals = json.loads(plan.goals) if isinstance(plan.goals, str) else plan.goals
                if goals:
                    st.write("**Hedefler:**")
                    for g in goals:
                        st.write(f"- {g}")
            except (json.JSONDecodeError, TypeError):
                pass


def _render_ogretmen_onerileri_readonly(store: AkademikDataStore, student: Student):
    styled_section("Öğretmen Gozlemleri", "#2563eb")
    oneriler = store.get_ogretmen_onerileri(student_id=student.id)
    if not oneriler:
        styled_info_banner("Öğretmen gozlemi bulunmuyor.", "info")
        return
    kat_map = dict(ONERI_KATEGORILERI)
    oncelik_icons = {"low": "🔵", "normal": "🟢", "high": "🟡", "urgent": "🔴"}
    for oneri in sorted(oneriler, key=lambda x: x.created_at, reverse=True)[:10]:
        icon = oncelik_icons.get(oneri.priority, "⚪")
        kat_label = kat_map.get(oneri.category, oneri.category)
        with st.expander(f"{icon} {kat_label} - {oneri.teacher_name or 'Öğretmen'} "
            f"({oneri.created_at[:10] if oneri.created_at else '-'})", expanded=False
        ):
            st.write(oneri.note or "Not yok")
            if oneri.follow_up_date:
                st.caption(f"Takip tarihi: {oneri.follow_up_date}")


def _render_mudahaleler_readonly(store: AkademikDataStore, student: Student):
    styled_section("Mudahale Kayıtlari", "#f59e0b")
    mudahaleler = store.get_mudahaleler(student_id=student.id)
    if not mudahaleler:
        styled_info_banner("Mudahale kaydi bulunmuyor.", "info")
        return
    tip_map = dict(MUDAHALE_TIPLERI)
    durum_map = {"planned": "Planli", "in_progress": "Devam Ediyor",
                 "completed": "Tamamlandı", "cancelled": "Iptal"}
    durum_icons = {"planned": "📋", "in_progress": "⏳", "completed": "✅", "cancelled": "❌"}
    for m in sorted(mudahaleler, key=lambda x: x.created_at, reverse=True)[:10]:
        icon = durum_icons.get(m.status, "📋")
        tip_label = tip_map.get(m.mudahale_type, m.mudahale_type)
        durum_label = durum_map.get(m.status, m.status)
        st.write(f"{icon} **{tip_label}** - {durum_label} | Sorumlu: {m.assigned_to_name or '-'}")
        if m.description:
            st.caption(m.description)


# ===================== MESAJLAR SEKMESİ =====================

def _render_mesajlar_tab(store: AkademikDataStore, student: Student, auth_user: dict):
    styled_section("Mesajlaşma", "#6366f1")

    # Premium mode seçici
    _mk = st.session_state.get("veli_mesaj_modu_v2", "gelen")
    _mode_items = [("gelen", "📥 Gelen Kutusu", "#2563eb"), ("giden", "📤 Giden Kutusu", "#7c3aed"), ("yeni", "✏️ Yeni Mesaj", "#059669")]
    _btns_html = ""
    for _mid, _mlabel, _mcol in _mode_items:
        _active = _mk == _mid
        _bg = f"linear-gradient(135deg,{_mcol},{_mcol}dd)" if _active else "#111827"
        _color = "#fff" if _active else "#94A3B8"
        _shadow = f"0 2px 8px {_mcol}40" if _active else "none"
        _btns_html += (f'<span style="display:inline-block;background:{_bg};color:{_color};'
                       f'padding:8px 18px;border-radius:20px;font-size:0.82rem;font-weight:600;'
                       f'box-shadow:{_shadow};border:1px solid {"transparent" if _active else "#e5e7eb"};'
                       f'margin-right:6px;">{_mlabel}</span>')
    st.markdown(f'<div style="margin-bottom:12px;">{_btns_html}</div>', unsafe_allow_html=True)

    mesaj_modu = st.radio(
        "Mesaj modu", ["Gelen Kutusu", "Giden Kutusu", "Yeni Mesaj"],
        horizontal=True, key="veli_mesaj_modu", label_visibility="collapsed"
    )
    if mesaj_modu == "Gelen Kutusu":
        _render_gelen_kutusu(store, auth_user, student)
    elif mesaj_modu == "Giden Kutusu":
        _render_giden_kutusu(store, auth_user)
    else:
        _render_yeni_mesaj_formu(store, student, auth_user)


def _render_gelen_kutusu(store: AkademikDataStore, auth_user: dict, student: Student):
    username = auth_user.get("username", "")
    mesajlar = store.get_panel_gelen_kutusu(receiver_id=username)
    if not mesajlar:
        styled_info_banner("Gelen kutunuz boş.", "info")
        return
    okunmamis = sum(1 for m in mesajlar if not m.okundu)
    toplam = len(mesajlar)
    styled_stat_row([
        ("Toplam", str(toplam), "#6366f1", "📬"),
        ("Okunmamış", str(okunmamis), "#f59e0b" if okunmamis else "#10b981", "📩"),
        ("Okunan", str(toplam - okunmamis), "#10b981", "✅"),
    ])
    kat_map = dict(MESAJ_KATEGORILERI)
    for i, m in enumerate(mesajlar):
        is_grup = getattr(m, "is_group_message", False)
        _unread = not m.okundu
        _bg = "linear-gradient(135deg,#eff6ff,#dbeafe)" if _unread else "linear-gradient(135deg,#111827,#1A2035)"
        _border = "#3b82f6" if _unread else "#e5e7eb"
        _shadow = "0 2px 8px rgba(59,130,246,0.12)" if _unread else "0 1px 3px rgba(0,0,0,0.04)"
        _kat_label = kat_map.get(m.kategori, m.kategori)
        _tarih = m.created_at[:16] if m.created_at else "-"
        _grup_html = '<span style="background:#7c3aed20;color:#7c3aed;padding:2px 8px;border-radius:10px;font-size:0.68rem;font-weight:600;margin-left:6px;">👥 Grup</span>' if is_grup else ""
        _unread_dot = '<span style="display:inline-block;width:8px;height:8px;background:#3b82f6;border-radius:50%;margin-right:6px;"></span>' if _unread else ""

        st.markdown(
            f'<div style="background:{_bg};border:1px solid {_border};border-radius:12px;'
            f'padding:14px 16px;margin-bottom:8px;box-shadow:{_shadow};">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div style="flex:1;">'
            f'<div style="display:flex;align-items:center;gap:4px;">'
            f'{_unread_dot}'
            f'<span style="font-weight:700;color:#0f172a;font-size:0.88rem;">{m.sender_name}</span>'
            f'{_grup_html}</div>'
            f'<div style="color:#0f172a;font-size:0.82rem;margin-top:3px;font-weight:500;">{m.konu or "(Konu yok)"}</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:0.7rem;color:#6b7280;">{_tarih}</div>'
            f'<span style="display:inline-block;margin-top:3px;background:#6366f120;color:#6366f1;'
            f'padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:600;">{_kat_label}</span>'
            f'</div></div></div>',
            unsafe_allow_html=True
        )

        with st.expander(f"{'📩' if _unread else '📧'} {m.sender_name} — detay", expanded=False):
            if _unread:
                if is_grup:
                    store.mark_grup_mesaj_okundu(m.id, username)
                else:
                    store.mark_mesaj_okundu(m.id)
            st.markdown(
                f'<div style="background:#ffffff;border-radius:10px;padding:14px;border:1px solid #e5e7eb;">'
                f'<div style="color:#0f172a;font-size:0.88rem;line-height:1.6;">{m.icerik or "(İçerik yok)"}</div>'
                f'</div>', unsafe_allow_html=True
            )
            if not is_grup:
                reply_key = f"veli_inline_reply_{m.id}"
                if st.button("✏️ Yanıtla", key=f"reply_{m.id}_{i}"):
                    st.session_state[reply_key] = True
                if st.session_state.get(reply_key):
                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);'
                        f'border:1px solid #86efac;border-radius:10px;padding:12px;margin:8px 0;">'
                        f'<span style="font-size:0.82rem;color:#166534;font-weight:600;">'
                        f'↩️ {m.sender_name} kişisine yanıt</span></div>',
                        unsafe_allow_html=True
                    )
                    with st.form(f"veli_inline_reply_form_{m.id}", clear_on_submit=True):
                        reply_konu = st.text_input("Konu", value=f"Re: {m.konu or ''}", key=f"rk_{m.id}")
                        reply_icerik = st.text_area("Mesajınız", height=100, key=f"ri_{m.id}")
                        c1, c2 = st.columns(2)
                        with c1:
                            gonder_btn = st.form_submit_button("📤 Gönder", type="primary", use_container_width=True)
                        with c2:
                            iptal_btn = st.form_submit_button("İptal", use_container_width=True)
                    if gonder_btn:
                        if not reply_icerik.strip():
                            st.error("Mesaj içeriği boş olamaz.")
                        else:
                            yanit = VeliMesaj(
                                sender_type="veli",
                                sender_id=username,
                                sender_name=auth_user.get("name", "Veli"),
                                receiver_type=m.sender_type or "ogretmen",
                                receiver_id=m.sender_id,
                                receiver_name=m.sender_name,
                                student_id=student.id if student else "",
                                konu=reply_konu.strip() or f"Re: {m.konu}",
                                icerik=reply_icerik.strip(),
                                kategori=m.kategori or "genel",
                                parent_message_id=m.id,
                                conversation_id=m.conversation_id or m.id,
                            )
                            store.save_veli_mesaj(yanit)
                            st.session_state.pop(reply_key, None)
                            st.toast("✅ Yanıtınız gönderildi!", icon="✅")
                            st.rerun()
                    if iptal_btn:
                        st.session_state.pop(reply_key, None)
                        st.rerun()


def _render_giden_kutusu(store: AkademikDataStore, auth_user: dict):
    username = auth_user.get("username", "")
    mesajlar = store.get_veli_giden_kutusu(sender_id=username)
    if not mesajlar:
        styled_info_banner("Henüz mesaj göndermemişsiniz.", "info")
        return
    _okundu_cnt = sum(1 for m in mesajlar if m.okundu)
    styled_stat_row([
        ("Gönderilen", str(len(mesajlar)), "#7c3aed", "📤"),
        ("Okunan", str(_okundu_cnt), "#10b981", "✅"),
        ("Bekleyen", str(len(mesajlar) - _okundu_cnt), "#f59e0b", "⏳"),
    ])
    kat_map = dict(MESAJ_KATEGORILERI)
    for m in mesajlar:
        _okundu = m.okundu
        _bg = "linear-gradient(135deg,#f0fdf4,#dcfce7)" if _okundu else "linear-gradient(135deg,#fffbeb,#fef3c7)"
        _border = "#86efac" if _okundu else "#fcd34d"
        _badge_bg = "#16a34a" if _okundu else "#f59e0b"
        _badge_text = "✅ Okundu" if _okundu else "⏳ Bekliyor"
        _tarih = m.created_at[:16] if m.created_at else "-"
        _kat_label = kat_map.get(m.kategori, m.kategori)

        st.markdown(
            f'<div style="background:{_bg};border:1px solid {_border};border-radius:12px;'
            f'padding:14px 16px;margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,0.04);">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            f'<div style="flex:1;">'
            f'<span style="font-weight:700;color:#0f172a;font-size:0.88rem;">📤 {m.receiver_name}</span>'
            f'<div style="color:#0f172a;font-size:0.82rem;margin-top:3px;font-weight:500;">{m.konu or "(Konu yok)"}</div>'
            f'<div style="font-size:0.7rem;color:#6b7280;margin-top:2px;">{_tarih} · {_kat_label}</div>'
            f'</div>'
            f'<span style="background:{_badge_bg};color:#fff;padding:4px 12px;border-radius:20px;'
            f'font-size:0.7rem;font-weight:600;white-space:nowrap;">{_badge_text}</span>'
            f'</div></div>', unsafe_allow_html=True
        )
        with st.expander(f"📤 {m.receiver_name} — detay", expanded=False):
            st.markdown(
                f'<div style="background:#ffffff;border-radius:10px;padding:14px;border:1px solid #e5e7eb;">'
                f'<div style="color:#0f172a;font-size:0.88rem;line-height:1.6;">{m.icerik or "(İçerik yok)"}</div>'
                f'</div>', unsafe_allow_html=True
            )


def _render_yeni_mesaj_formu(store: AkademikDataStore, student: Student,
                              auth_user: dict, reply_to: VeliMesaj = None):
    if reply_to is None:
        reply_to = st.session_state.pop("veli_reply_to", None)
    styled_section("Yeni Mesaj Yaz", "#059669")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1px solid #86efac;'
        'border-radius:12px;padding:12px 16px;margin-bottom:12px;font-size:0.82rem;color:#166534;">'
        '✏️ Aşağıdaki formu doldurarak öğretmen veya yönetime mesaj gönderebilirsiniz.</div>',
        unsafe_allow_html=True
    )

    # Kadro bazlı alıcı kısıtlaması
    kadro = store.get_sinif_kadro_for_student(student)
    alici_listesi = {}
    if kadro:
        teachers = store.get_teachers()
        teacher_map = {t.id: t for t in teachers}
        kadro_ids = set()
        for tid in [kadro.sinif_ogretmeni_id, kadro.sinif_danisman_id,
                     kadro.rehber_ogretmen_id, kadro.mudur_yardimcisi_id, kadro.mudur_id]:
            if tid:
                kadro_ids.add(tid)
        for tid in kadro_ids:
            t = teacher_map.get(tid)
            if t:
                rol = _get_kadro_role_label(kadro, tid)
                alici_listesi[t.id] = f"{t.ad} {t.soyad} ({rol})"
    else:
        teachers = store.get_teachers()
        for t in teachers:
            alici_listesi[t.id] = f"{t.ad} {t.soyad} ({getattr(t, 'brans', '-')})"
        alici_listesi["yonetim"] = "Okul Yönetimi"

    with st.form("veli_yeni_mesaj_form", clear_on_submit=True):
        if reply_to:
            st.info(f"Yanit: {reply_to.sender_name} - {reply_to.konu}")
            alici_id = reply_to.sender_id
            default_konu = f"Re: {reply_to.konu}"
        else:
            alici_secenekler = list(alici_listesi.keys())
            alici_id = st.selectbox(
                "Alici", alici_secenekler,
                format_func=lambda x: alici_listesi.get(x, x), key="veli_mesaj_alici"
            )
            default_konu = ""
        konu = st.text_input("Konu", value=default_konu, key="veli_mesaj_konu")
        kategori = st.selectbox("Kategori", [k for k, _ in MESAJ_KATEGORILERI],
                                format_func=lambda x: dict(MESAJ_KATEGORILERI).get(x, x),
                                key="veli_mesaj_kategori")
        icerik = st.text_area("Mesajiniz", height=150, key="veli_mesaj_icerik")
        gonder = st.form_submit_button("Mesaji Gonder", type="primary", use_container_width=True)

    if gonder:
        if not konu or not icerik:
            st.error("Konu ve mesaj icerigi zorunludur.")
            return
        alici_name = alici_listesi.get(alici_id, "Bilinmiyor")
        mesaj = VeliMesaj(
            sender_type="veli", sender_id=auth_user.get("username", ""),
            sender_name=auth_user.get("name", "Veli"),
            receiver_type="ogretmen" if alici_id != "yonetim" else "yonetici",
            receiver_id=alici_id, receiver_name=alici_name,
            student_id=student.id, konu=konu, icerik=icerik, kategori=kategori,
            parent_message_id=reply_to.id if reply_to else "",
            conversation_id=reply_to.conversation_id if reply_to else "",
        )
        if not mesaj.conversation_id:
            mesaj.conversation_id = mesaj.id
        store.save_veli_mesaj(mesaj)
        st.success(f"Mesaj '{alici_name}' adresine gonderildi!")


# ===================== DİJİTAL ÖĞRENME SEKMESİ =====================

_PLATFORM_IKON = {
    "google_classroom": ("🏫", "#34A853", "Google Classroom"),
    "zoom":             ("📹", "#2D8CFF", "Zoom"),
    "teams":            ("💼", "#6264A7", "Microsoft Teams"),
    "meet":             ("🎥", "#00897B", "Google Meet"),
    "eba":              ("📚", "#e63946", "EBA"),
    "diger":            ("🔗", "#64748b", "Diğer"),
}
_DIJITAL_KAT_IKON = {
    "eba":      ("📚", "#e63946"),
    "video":    ("▶️",  "#ef4444"),
    "interaktif": ("🎮", "#22c55e"),
    "dokuman":  ("📄", "#f59e0b"),
    "oyun_quiz": ("🧩", "#8b5cf6"),
    "diger":    ("🔗", "#64748b"),
}

# ── Dijital Kütüphane / Dijital Öğrenme: Sabit Platform & YouTube verileri ──
_PANEL_DIJITAL_PLATFORMLAR = (
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

# Video konferans ve canlı ders platformları — Türkçe giriş sayfaları
_PANEL_VIDEO_KONFERANS_PLATFORMLAR = (
    ("Zoom", "Türkçe Giriş — Canlı Ders & Toplantı Oluştur", "https://zoom.us/tr/signin", "#2D8CFF", "#1565c0", "#dbeafe"),
    ("Microsoft Teams", "Microsoft 365 — Türkçe Ekip & Ders Platformu", "https://teams.microsoft.com/?culture=tr-tr&country=TR", "#6264A7", "#4f46e5", "#e9d5ff"),
    ("Google Classroom", "Google Sınıf — Türkçe Ödev & Ders Yönetimi", "https://classroom.google.com/?hl=tr", "#34A853", "#1e8e3e", "#d1fae5"),
    ("Google Meet", "Türkçe Google Görüntülü Görüşme & Canlı Ders", "https://meet.google.com/?hl=tr", "#00897B", "#00695c", "#e0f2f1"),
)

_PANEL_DIJITAL_YT_KANALLAR = {
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


def _build_panel_platform_html() -> str:
    parts = ['<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">']
    for ad, aciklama, link, r1, r2, rt in _PANEL_DIJITAL_PLATFORMLAR:
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


def _build_panel_yt_html() -> str:
    parts = []
    for kademe, kanallar in _PANEL_DIJITAL_YT_KANALLAR.items():
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


def _build_panel_video_konferans_html() -> str:
    """Video konferans ve canlı ders platform kartlarını oluşturur — Türkçe giriş linkleri."""
    parts = ['<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:16px;">']
    for ad, aciklama, link, r1, r2, rt in _PANEL_VIDEO_KONFERANS_PLATFORMLAR:
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


_PANEL_PLATFORM_HTML_CACHE = _build_panel_platform_html()
_PANEL_YT_HTML_CACHE = _build_panel_yt_html()
_PANEL_VIDEO_KONFERANS_HTML_CACHE = _build_panel_video_konferans_html()


def _render_dk_embed():
    """Dijital Kütüphane modülünü readonly olarak embed eder (Veli/Öğrenci paneli içinden)."""
    from views.dijital_kutuphane import render_dijital_kutuphane
    render_dijital_kutuphane(readonly=True)


def _render_dijital_ogrenme_tab(store: AkademikDataStore, student: Student):
    """Dijital Ogrenme & Online Ders sekmesi — veli/ogrenci goruntuleme.
    Ana amac: ogretmenin paylastigi online ders linkine tek tiklama ile katilim.
    """
    today_str = date.today().isoformat()
    akademik_yil = _get_akademik_yil()
    try:
        sinif_int = student.sinif if isinstance(student.sinif, int) else int(''.join(c for c in str(student.sinif or '0') if c.isdigit()) or '0')
    except (ValueError, TypeError):
        sinif_int = 0

    # ── Veri yükle ──
    tum_kayitlar = store.get_online_ders_kayitlari(akademik_yil=akademik_yil)
    sinif_kayitlari = [
        k for k in tum_kayitlar
        if k.sinif == sinif_int and (not k.sube or k.sube == student.sube)
    ]
    bugun_kayitlar = sorted(
        [k for k in sinif_kayitlari if k.planlanan_tarih == today_str],
        key=lambda x: x.planlanan_saat
    )
    tamamlanan = [k for k in sinif_kayitlari if k.durum == "yapildi"]

    tum_linkler = store.get_online_ders_links(akademik_yil=akademik_yil)
    sinif_linkleri = [
        l for l in tum_linkler
        if l.sinif == sinif_int and (not l.sube or l.sube == student.sube) and l.aktif
    ]

    tum_dijital = store.get_dijital_ogrenme_links(akademik_yil=akademik_yil)
    sinif_dijital = [
        d for d in tum_dijital
        if d.sinif == sinif_int and (not d.sube or d.sube == student.sube) and d.aktif
    ]

    # ════════════════════════════════════════════════════════════════
    # BİLDİRİM — Bu hafta yaklaşan online dersler
    # ════════════════════════════════════════════════════════════════
    import datetime as _dt
    _yedi_gun = (_dt.date.today() + _dt.timedelta(days=7)).isoformat()
    yaklasan = sorted(
        [k for k in sinif_kayitlari
         if k.planlanan_tarih > today_str
         and k.planlanan_tarih <= _yedi_gun
         and k.durum in ("planli", "yapiliyor")],
        key=lambda x: (x.planlanan_tarih, x.planlanan_saat)
    )
    if yaklasan:
        _bildirim_satirlar = []
        for _yk in yaklasan:
            try:
                _ytarih = _dt.date.fromisoformat(_yk.planlanan_tarih)
                _ygun = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][_ytarih.weekday()]
                _ytarih_str = f"{_ygun} {_ytarih.strftime('%d.%m')}"
            except ValueError:
                _ytarih_str = _yk.planlanan_tarih
            _bildirim_satirlar.append(
                f'<span style="background:rgba(255,255,255,0.25);border-radius:8px;'
                f'padding:2px 10px;margin-right:6px;font-size:0.82rem;white-space:nowrap;">'
                f'📅 {_ytarih_str} · {_yk.planlanan_saat} · <b>{_yk.ders}</b></span>'
            )
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);'
            f'border-radius:14px;padding:14px 18px;margin-bottom:14px;">'
            f'<div style="color:white;font-weight:700;font-size:0.95rem;margin-bottom:8px;">'
            f'🔔 Bu Hafta {len(yaklasan)} Online Ders Planlandı</div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:6px;">{"".join(_bildirim_satirlar)}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 1 — BUGÜNÜN ONLINE DERSLERİ (EN ÜST, HER ZAMAN GÖRÜNÜR)
    # ════════════════════════════════════════════════════════════════
    gun_adi_map = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
                   4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    bugun_dt = _dt.date.today()
    gun_label = f"{gun_adi_map[bugun_dt.weekday()]} {bugun_dt.strftime('%d %B %Y')}"

    canli_var = any(k.durum == "yapiliyor" for k in bugun_kayitlar)

    # Başlık banner
    if canli_var:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#dc2626,#b91c1c);'
            f'border-radius:16px;padding:18px 24px;margin-bottom:16px;'
            f'display:flex;align-items:center;gap:16px;">'
            f'<span style="font-size:2rem;">🔴</span>'
            f'<div>'
            f'<div style="font-size:1.15rem;font-weight:800;color:white;letter-spacing:0.5px;">'
            f'CANLI DERS VAR — {gun_label}</div>'
            f'<div style="color:#fecaca;font-size:0.85rem;margin-top:2px;">'
            f'Şu an devam eden ders için aşağıdaki butona tıklayın</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#4f46e5,#6366f1);'
            f'border-radius:16px;padding:16px 22px;margin-bottom:16px;'
            f'display:flex;align-items:center;gap:14px;">'
            f'<span style="font-size:1.8rem;">📅</span>'
            f'<div>'
            f'<div style="font-size:1.05rem;font-weight:800;color:white;">'
            f'Bugünün Online Dersleri — {gun_label}</div>'
            f'<div style="color:#c7d2fe;font-size:0.82rem;margin-top:2px;">'
            f'Linke tıklayarak derse katılabilirsiniz</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    if bugun_kayitlar:
        for k in bugun_kayitlar:
            p_ikon, p_renk, p_ad = _PLATFORM_IKON.get(k.platform, ("🔗", "#64748b", k.platform or "Link"))
            is_canli = k.durum == "yapiliyor"
            is_planli = k.durum == "planli"
            is_bitti = k.durum == "yapildi"

            # Link bul: önce kayıttaki direkt URL, yoksa link_id lookup
            link_url = k.link if k.link else ""
            if not link_url and k.link_id:
                eslesme = next((l for l in sinif_linkleri if l.id == k.link_id), None)
                if eslesme:
                    link_url = eslesme.link

            # Kart rengi ve durum
            if is_canli:
                kart_bg = "linear-gradient(135deg,#dc262608,#dc262603)"
                kart_border = "#dc2626"
                durum_html = ('<span style="background:#dc2626;color:white;padding:3px 12px;'
                              'border-radius:20px;font-size:0.75rem;font-weight:700;'
                              'animation:pulse 1.5s infinite;">🔴 CANLI</span>')
                btn_label = "🔴  DERSE KATIL"
                btn_color = "#dc2626"
            elif is_planli:
                kart_bg = "linear-gradient(135deg,#6366f108,#6366f103)"
                kart_border = "#6366f1"
                durum_html = ('<span style="background:#6366f1;color:white;padding:3px 12px;'
                              'border-radius:20px;font-size:0.75rem;font-weight:700;">🟡 Planlandı</span>')
                btn_label = "▶  Derse Gir"
                btn_color = "#6366f1"
            elif is_bitti:
                kart_bg = "linear-gradient(135deg,#16a34a08,#16a34a03)"
                kart_border = "#16a34a"
                durum_html = ('<span style="background:#16a34a;color:white;padding:3px 12px;'
                              'border-radius:20px;font-size:0.75rem;font-weight:700;">✅ Tamamlandı</span>')
                btn_label = "Tekrar Aç"
                btn_color = "#16a34a"
            else:
                kart_bg = "#111827"
                kart_border = "#94a3b8"
                durum_html = ('<span style="background:#94a3b8;color:white;padding:3px 12px;'
                              'border-radius:20px;font-size:0.75rem;font-weight:700;">❌ Yapılmadı</span>')
                btn_label = ""
                btn_color = "#94a3b8"

            col_info, col_btn = st.columns([5, 1])
            with col_info:
                st.markdown(
                    f'<div style="background:{kart_bg};border:2px solid {kart_border}40;'
                    f'border-left:5px solid {kart_border};border-radius:14px;'
                    f'padding:16px 20px;margin-bottom:10px;">'
                    f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px;">'
                    f'<span style="font-size:1.5rem;">{p_ikon}</span>'
                    f'<span style="font-size:1.05rem;font-weight:800;color:#0B0F19;">{k.ders}</span>'
                    f'<span style="background:{p_renk}22;color:{p_renk};padding:2px 10px;'
                    f'border-radius:10px;font-size:0.73rem;font-weight:700;">{p_ad}</span>'
                    f'{durum_html}'
                    f'</div>'
                    f'<div style="display:flex;gap:20px;font-size:0.85rem;color:#475569;flex-wrap:wrap;">'
                    f'<span>🕐 <b>{k.planlanan_saat}</b></span>'
                    f'<span>⏱ {k.sure_dk} dakika</span>'
                    f'<span>👨‍🏫 {k.ogretmen_adi or "–"}</span>'
                    f'{f"<span>📝 {k.notlar}</span>" if k.notlar else ""}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with col_btn:
                st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
                if link_url and btn_label:
                    st.markdown(
                        f'<a href="{link_url}" target="_blank" rel="noopener" style="text-decoration:none;">'
                        f'<div class="sc-stat-hover" style="background:{btn_color};color:white;border-radius:12px;'
                        f'padding:14px 10px;text-align:center;font-weight:800;font-size:0.9rem;'
                        f'cursor:pointer;transition:opacity 0.15s;letter-spacing:0.3px;">'
                        f'{btn_label}</div></a>',
                        unsafe_allow_html=True
                    )
                elif btn_label and not link_url:
                    st.markdown(
                        f'<div style="background:#e2e8f0;color:#475569;border-radius:12px;'
                        f'padding:14px 10px;text-align:center;font-size:0.8rem;">'
                        f'Link eklenmemiş</div>',
                        unsafe_allow_html=True
                    )
    else:
        st.markdown(
            '<div style="background:#f1f5f9;border:2px dashed #cbd5e1;border-radius:14px;'
            'padding:32px;text-align:center;margin-bottom:16px;">'
            '<div style="font-size:2.5rem;margin-bottom:10px;">📭</div>'
            '<div style="font-size:1rem;font-weight:700;color:#475569;">Bugün için online ders planlanmamış</div>'
            '<div style="font-size:0.82rem;color:#475569;margin-top:6px;">'
            'Öğretmeniniz ders planladığında burada görünecek</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 2 — SINIF PLATFORM BAĞLANTILARI (öğretmen tarafından eklenen kalıcı linkler)
    # ════════════════════════════════════════════════════════════════
    if sinif_linkleri:
        st.markdown("")
        st.markdown(
            '<div style="background:linear-gradient(90deg,#2563eb15,#2563eb05);'
            'border-left:4px solid #2563eb;padding:10px 16px;border-radius:0 10px 10px 0;'
            'font-weight:700;font-size:0.95rem;color:#1d4ed8;margin-bottom:12px;">'
            '🔗 Sınıf Platform Bağlantıları — Öğretmeninizin Paylaştığı Linkler'
            '</div>',
            unsafe_allow_html=True
        )
        n = len(sinif_linkleri)
        cols = st.columns(min(n, 3))
        for i, l in enumerate(sinif_linkleri):
            p_ikon, p_renk, p_ad = _PLATFORM_IKON.get(l.platform, ("🔗", "#6366f1", l.platform or "Platform"))
            with cols[i % 3]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{p_renk}18,{p_renk}08);'
                    f'border:2px solid {p_renk}50;border-radius:14px;'
                    f'padding:16px;margin-bottom:8px;text-align:center;">'
                    f'<div style="font-size:1.8rem;margin-bottom:6px;">{p_ikon}</div>'
                    f'<div style="font-weight:800;color:#0B0F19;font-size:0.92rem;">{l.ders}</div>'
                    f'<div style="font-size:0.75rem;color:#64748b;margin-top:3px;">{p_ad}</div>'
                    f'{f"<div style=\"font-size:0.72rem;color:#475569;margin-top:2px;\">{l.ogretmen_adi}</div>" if l.ogretmen_adi else ""}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if l.link:
                    st.link_button("Bağlan →", l.link, type="primary", use_container_width=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 3 — DİJİTAL KAYNAKLAR (öğretmen tarafından atanan)
    # ════════════════════════════════════════════════════════════════
    if sinif_dijital:
        with st.expander(f"📖 Öğretmenin Atadığı Dijital Kaynaklar  ({len(sinif_dijital)} kaynak)", expanded=True):
            ders_gruplari: dict[str, list] = {}
            for d in sinif_dijital:
                ders_gruplari.setdefault(d.ders or "Genel", []).append(d)
            for ders_adi, kaynaklar in sorted(ders_gruplari.items()):
                st.markdown(f"**📚 {ders_adi}**")
                for d in kaynaklar:
                    kat = d.kategori.lower() if d.kategori else "diger"
                    k_ikon, k_renk = _DIJITAL_KAT_IKON.get(kat, ("🔗", "#64748b"))
                    col_a, col_b = st.columns([5, 1])
                    with col_a:
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;'
                            f'border-bottom:1px solid #e2e8f0;">'
                            f'<span style="font-size:1.1rem;">{k_ikon}</span>'
                            f'<div>'
                            f'<div style="font-weight:600;color:#0f172a;font-size:0.88rem;">{d.baslik}</div>'
                            f'{f"<div style=\'font-size:0.75rem;color:#64748b;\'>{d.aciklama}</div>" if d.aciklama else ""}'
                            f'<span style="background:{k_renk}22;color:{k_renk};padding:1px 7px;'
                            f'border-radius:8px;font-size:0.68rem;font-weight:600;">'
                            f'{d.kategori.upper() if d.kategori else "KAYNAK"}</span>'
                            f'</div></div>',
                            unsafe_allow_html=True
                        )
                    with col_b:
                        if d.link:
                            st.link_button("Aç →", d.link, use_container_width=True)

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 4 — VIDEO KONFERANS & CANLI DERS PLATFORMLARI
    # ════════════════════════════════════════════════════════════════
    with st.expander("📹 Canlı Ders Platformları (Zoom, Teams, Classroom, Meet)", expanded=True):
        st.markdown(
            '<div style="background:linear-gradient(135deg,#4f46e510,#6366f108);'
            'border-left:4px solid #6366f1;padding:10px 16px;border-radius:0 10px 10px 0;'
            'margin-bottom:14px;font-size:0.82rem;color:#475569;">'
            'Öğretmeniniz canlı ders linki paylaştığında aşağıdaki platformlardan giriş yapabilirsiniz.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_PANEL_VIDEO_KONFERANS_HTML_CACHE, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 5 — GENEL EĞİTİM PLATFORMLARI & YOUTUBE (expander)
    # ════════════════════════════════════════════════════════════════
    with st.expander("🌐 Genel Eğitim Platformları (EBA, Khan Akademi, GeoGebra...)", expanded=True):
        st.markdown(_PANEL_PLATFORM_HTML_CACHE, unsafe_allow_html=True)

    with st.expander("▶ YouTube Eğitim Kanalları", expanded=True):
        st.markdown(_PANEL_YT_HTML_CACHE, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════════
    # BÖLÜM 5 — BU DÖNEM İSTATİSTİK ÖZETİ
    # ════════════════════════════════════════════════════════════════
    planli_sayi = len([k for k in sinif_kayitlari if k.durum in ("planli", "yapiliyor")])
    toplam = len(sinif_kayitlari)
    if toplam > 0:
        st.markdown("")
        oran = round((len(tamamlanan) / toplam) * 100)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Toplam Planlanan", str(toplam))
        with c2:
            st.metric("Tamamlanan", str(len(tamamlanan)))
        with c3:
            st.metric("Bekleyen", str(planli_sayi))
        with c4:
            st.metric("Tamamlanma Oranı", f"%{oran}")


# ===================== İŞLENEN KAZANIMLAR (1-2. SINIF VELİ) =====================

def _render_islenen_kazanimlar_tab(store: AkademikDataStore, student: Student):
    """1-2. sınıf velileri için işlenen kazanımlar görünümü."""
    from utils.shared_data import normalize_sinif

    styled_section("📖 İşlenen Kazanımlar", "#2563eb")
    st.caption("Çocuğunuzun sınıfında bu dönem işlenen kazanımların listesi.")

    sinif_no = normalize_sinif(str(student.sinif))
    try:
        sinif_int = int(sinif_no)
    except (ValueError, TypeError):
        sinif_int = 1

    akademik_yil = _get_akademik_yil()

    # Tüm işlenen kazanımları getir
    records = store.get_kazanim_isleme(
        sinif=sinif_int, sube=student.sube, durum="islendi",
        akademik_yil=akademik_yil,
    )

    if not records:
        styled_info_banner("Henüz işlenmiş kazanım kaydı bulunmuyor.", "info")
        return

    # Derse göre grupla
    ders_grp = {}
    for r in records:
        ders_adi = r.ders or "Diğer"
        if ders_adi not in ders_grp:
            ders_grp[ders_adi] = []
        ders_grp[ders_adi].append(r)

    # Ders ikonları
    ders_ikon = {
        "Türkçe": "📝", "Matematik": "🔢", "Hayat Bilgisi": "🌍",
        "İngilizce": "🌎", "Müzik": "🎵", "Görsel Sanatlar": "🎨",
        "Beden Eğitimi": "⚽", "Fen Bilimleri": "🔬", "Trafik Güvenliği": "🚦",
    }

    # Özet stat kartları
    toplam_kaz = len(records)
    ders_sayisi = len(ders_grp)
    son_hafta = max((r.hafta for r in records), default=0)
    styled_stat_row([
        ("Toplam Kazanım", str(toplam_kaz), "#2563eb", "📖"),
        ("Ders Sayısı", str(ders_sayisi), "#7c3aed", "📚"),
        ("Son Hafta", f"{son_hafta}. hafta", "#059669", "📅"),
    ])

    st.markdown("")

    # Her ders için kart
    for ders_adi in sorted(ders_grp.keys()):
        kaz_list = ders_grp[ders_adi]
        kaz_list.sort(key=lambda r: (r.hafta, r.kazanim_kodu))
        ikon = ders_ikon.get(ders_adi, "📘")

        with st.expander(f"{ikon} {ders_adi} — {len(kaz_list)} kazanım", expanded=False):
            for r in kaz_list:
                tarih_str = r.tarih or ""
                hafta_str = f"{r.hafta}. hafta" if r.hafta else ""
                meta_parts = [x for x in [hafta_str, tarih_str] if x]
                meta = " | ".join(meta_parts)

                st.markdown(
                    f'<div style="border-left:3px solid #22c55e;padding:6px 12px;'
                    f'margin-bottom:6px;background:#f8fafc;border-radius:0 8px 8px 0;">'
                    f'<div style="font-size:0.85rem;color:#0f172a;">'
                    f'<b>{r.kazanim_kodu}</b> — {r.kazanim_metni or "-"}</div>'
                    f'<div style="font-size:0.72rem;color:#64748b;margin-top:2px;">'
                    f'✅ İşlendi{" | " + meta if meta else ""}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )


# ===================== KAZANIM BORÇ BANKASI =====================

def _render_borc_tab(store: AkademikDataStore, student: Student, rol: str = "veli"):
    """Kazanım Borç Bankası — veli ve öğrenci ortak görünümü — premium tasarım."""
    from datetime import date as _date

    # Kurum bilgisi
    try:
        from utils.shared_data import load_kurum_profili
        kurum = load_kurum_profili()
        kurum_adi = kurum.get("kurum_adi", "Smart Campus") if kurum else "Smart Campus"
    except Exception:
        kurum_adi = "Smart Campus"

    # Premium başlık
    st.markdown(
        f"<div style='background:linear-gradient(135deg,#2e1065 0%,#4c1d95 30%,#7c3aed 60%,#8b5cf6 100%);"
        f"color:#fff;padding:20px 24px;border-radius:14px;margin-bottom:16px;position:relative;overflow:hidden'>"
        f"<div style='position:absolute;top:-20px;right:-20px;width:100px;height:100px;"
        f"background:rgba(255,255,255,0.05);border-radius:50%'></div>"
        f"<div style='font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;"
        f"opacity:0.65;margin-bottom:3px'>{kurum_adi}</div>"
        f"<div style='font-size:1.2rem;font-weight:800;letter-spacing:0.3px'>📚 Kazanım Borç Bankası</div>"
        f"<div style='font-size:0.82rem;opacity:0.85;margin-top:4px'>"
        f"{student.tam_ad} · {student.sinif}/{student.sube}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Tanıtım
    if rol == "veli":
        styled_info_banner(
            "Çocuğunuzun devamsızlığı veya ödev eksikliği nedeniyle geride kaldığı kazanımlar "
            "borç olarak kaydedilir. Bu ekrandan tüm borç durumunu ve AI yol haritasını görebilirsiniz.",
            "info"
        )
    else:
        styled_info_banner(
            "Devamsız olduğun veya ödevini yapmadığın / hatalı yaptığın kazanımlar borç olarak görünür. "
            "Borçlarını kapatmak için öğretmeninden telafi ödevi iste veya AI yol haritasını incele.",
            "info"
        )

    akademik_yil_now = f"{__import__('datetime').date.today().year}-{__import__('datetime').date.today().year + 1}"
    if __import__('datetime').date.today().month >= 9:
        pass
    else:
        akademik_yil_now = f"{__import__('datetime').date.today().year - 1}-{__import__('datetime').date.today().year}"

    borclar = store.get_kazanim_borclari(
        student_id=student.id,
        akademik_yil=akademik_yil_now,
    )
    aktif = [b for b in borclar if b.durum == "borc_var"]
    kapali = [b for b in borclar if b.durum == "kapandi"]

    # Premium stat kartlar
    import plotly.express as px

    def _borc_kart(ikon, baslik, deger, renk, bg_from, bg_to, border_color):
        return (
            f"<div style='flex:1;min-width:140px;background:linear-gradient(135deg,{bg_from},{bg_to});"
            f"border-radius:14px;padding:18px 16px;text-align:center;border:1.5px solid {border_color};"
            f"box-shadow:0 2px 8px rgba(0,0,0,0.06)'>"
            f"<div style='font-size:1.5rem'>{ikon}</div>"
            f"<div style='font-size:0.72rem;color:{renk};font-weight:600;margin:4px 0;letter-spacing:0.3px'>"
            f"{baslik}</div>"
            f"<div style='font-size:1.6rem;font-weight:800;color:{renk}'>{deger}</div>"
            f"</div>"
        )

    st.markdown(
        "<div style='display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px'>"
        + _borc_kart("📚", "TOPLAM BORÇ", len(borclar), "#7c3aed", "#faf5ff", "#f3e8ff", "#e9d5ff")
        + _borc_kart("🔴", "AKTİF BORÇ", len(aktif), "#ef4444", "#fef2f2", "#fee2e2", "#fecaca")
        + _borc_kart("✅", "KAPATILAN", len(kapali), "#10b981", "#f0fdf4", "#dcfce7", "#bbf7d0")
        + _borc_kart("📖", "BORÇLU DERS", len({b.ders for b in aktif}), "#f59e0b", "#fffbeb", "#fef3c7", "#fde68a")
        + "</div>",
        unsafe_allow_html=True,
    )

    if not borclar:
        styled_info_banner("Tebrikler! Herhangi bir kazanım borcunuz bulunmamaktadır.", "success")
        return

    # Ders bazlı dağılım grafiği
    if aktif:
        ders_say = {}
        for b in aktif:
            ders_say[b.ders] = ders_say.get(b.ders, 0) + 1
        df_ders = pd.DataFrame(
            sorted(ders_say.items(), key=lambda x: x[1], reverse=True),
            columns=["Ders", "Borç Sayısı"]
        )
        fig = go.Figure(go.Bar(
            x=df_ders["Ders"], y=df_ders["Borç Sayısı"],
            marker_color=SC_COLORS[2],
            text=df_ders["Borç Sayısı"], textposition="outside",
        ))
        sc_bar(fig, height=220)
        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

    # Ders bazlı borç listesi — premium kartlar
    st.markdown(
        "<div style='background:linear-gradient(135deg,#fef2f2,#fff1f2);border-radius:12px;"
        "padding:12px 16px;margin-bottom:12px;border:1.5px solid #fecaca'>"
        "<div style='font-weight:700;color:#be123c;font-size:0.92rem'>📋 Borçlu Kazanımlar (Derse Göre)</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    for ders_adi in sorted({b.ders for b in borclar}):
        ders_borclar = [b for b in borclar if b.ders == ders_adi]
        aktif_count = len([b for b in ders_borclar if b.durum == "borc_var"])
        with st.expander(f"📖 {ders_adi}  ({aktif_count} aktif borç)", expanded=(aktif_count > 0)):
            for b in ders_borclar:
                durum_color = "#ef4444" if b.durum == "borc_var" else "#10b981"
                durum_bg = "#fef2f2" if b.durum == "borc_var" else "#f0fdf4"
                durum_lbl = "🔴 Borçlu" if b.durum == "borc_var" else "✅ Kapandı"
                neden_lbl = BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)
                tarih = b.kazanim_isleme_tarihi[:10] if b.kazanim_isleme_tarihi else "-"
                kapan_info = ""
                if b.durum == "kapandi" and b.kapanma_tarihi:
                    kapan_info = f" | Kapandı: {b.kapanma_tarihi[:10]}"
                st.markdown(
                    f'<div style="border-left:4px solid {durum_color};padding:12px 16px;'
                    f'margin:6px 0;background:{durum_bg};border-radius:0 12px 12px 0;'
                    f'box-shadow:0 1px 4px rgba(0,0,0,0.05)">'
                    f'<div style="font-weight:600;font-size:0.88rem;color:#0f172a;line-height:1.4">'
                    f'{b.kazanim_metni}</div>'
                    f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:6px;align-items:center">'
                    f'<span style="background:{durum_color};color:white;padding:2px 10px;'
                    f'border-radius:10px;font-size:0.72rem;font-weight:600">{durum_lbl}</span>'
                    f'<span style="font-size:0.75rem;color:#64748b">{neden_lbl}</span>'
                    f'<span style="font-size:0.75rem;color:#475569">📅 {tarih}{kapan_info}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

    # AI Yol Haritası
    st.write("")
    styled_section("AI Yol Haritası ve Tavsiyeler", "#7c3aed")
    if aktif:
        btn_key = f"borc_ai_{student.id}_{rol}"
        if st.button("🤖 AI Yol Haritası Oluştur", key=btn_key):
            with st.spinner("AI kişiselleştirilmiş yol haritası hazırlanıyor..."):
                try:
                    import openai
                    import os as _os
                    api_key = _os.environ.get("OPENAI_API_KEY", "")
                    if api_key:
                        borc_listesi = "\n".join([
                            f"- {b.ders} | {b.kazanim_metni} | Neden: {BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)}"
                            for b in aktif[:10]
                        ])
                        prompt_rol = "velisine" if rol == "veli" else "öğrenciye"
                        prompt = (
                            f"Öğrenci: {student.tam_ad}, Sınıf: {student.sinif}/{student.sube}\n\n"
                            f"Borçlu olduğu kazanımlar:\n{borc_listesi}\n\n"
                            f"Bu öğrencinin {prompt_rol} yönelik:\n"
                            "1) Her kazanım için kısa ve net telafi yol haritası\n"
                            "2) Günlük çalışma önerileri\n"
                            "3) Her kazanım için 2 pekiştirme sorusu\n"
                            "Türkçe, motivasyonel ve destekleyici bir dil kullan."
                        )
                        client = openai.OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir eğitim danışmanısın. Türkçe, sıcak ve destekleyici bir dilde rehberlik yapıyorsun."},
                                {"role": "user", "content": prompt},
                            ],
                            max_tokens=1500,
                            temperature=0.7,
                        )
                        rapor = response.choices[0].message.content or ""
                        st.session_state[f"borc_ai_rapor_{student.id}_{rol}"] = rapor
                    else:
                        st.session_state[f"borc_ai_rapor_{student.id}_{rol}"] = "OpenAI API anahtarı bulunamadı."
                except Exception as e:
                    st.session_state[f"borc_ai_rapor_{student.id}_{rol}"] = f"AI analizi alınamadı: {e}"

        ai_key = f"borc_ai_rapor_{student.id}_{rol}"
        if ai_key in st.session_state and st.session_state[ai_key]:
            st.markdown(
                f'<div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:12px;'
                f'padding:16px;line-height:1.7;font-size:0.88rem;color:#475569">'
                f'{st.session_state[ai_key].replace(chr(10), "<br>")}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # PDF indirme
        st.write("")
        styled_section("PDF Rapor", "#7c3aed")
        if st.button("📄 PDF Rapor İndir", key=f"borc_pdf_{student.id}_{rol}"):
            with st.spinner("PDF hazırlanıyor..."):
                try:
                    from io import BytesIO
                    from reportlab.lib import colors as rl_colors
                    from reportlab.lib.pagesizes import A4
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib.units import cm
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.enums import TA_CENTER
                    from reportlab.pdfbase import pdfmetrics
                    from reportlab.pdfbase.ttfonts import TTFont
                    import unicodedata

                    # Font önce yükle — _n() bunu kullanır
                    try:
                        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts", "DejaVuSans.ttf"))
                        if os.path.exists(fp):
                            pdfmetrics.registerFont(TTFont("DejaVuSans", fp))
                            FONT = "DejaVuSans"
                        else:
                            FONT = "Helvetica"
                    except Exception:
                        FONT = "Helvetica"

                    # DejaVuSans tam Unicode destekler; Helvetica için Türkçe harfleri dönüştür
                    if FONT == "DejaVuSans":
                        def _n(t) -> str:
                            return str(t) if t else ""
                    else:
                        _TR2 = str.maketrans("ğşıöüçĞŞİÖÜÇ", "gsioucGSIOUC")
                        def _n(t) -> str:
                            return str(t).translate(_TR2) if t else ""

                    buf = BytesIO()
                    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm,
                                            topMargin=2*cm, bottomMargin=2*cm)

                    styles = getSampleStyleSheet()
                    t_style = ParagraphStyle("T", fontName=FONT, fontSize=16, alignment=TA_CENTER,
                                            textColor=rl_colors.HexColor("#7c3aed"), spaceAfter=8)
                    s_style = ParagraphStyle("S", fontName=FONT, fontSize=11, alignment=TA_CENTER,
                                            textColor=rl_colors.HexColor("#475569"), spaceAfter=16)
                    h_style = ParagraphStyle("H", fontName=FONT, fontSize=12,
                                            textColor=rl_colors.HexColor("#94A3B8"), spaceBefore=12, spaceAfter=6)
                    b_style = ParagraphStyle("B", fontName=FONT, fontSize=9,
                                            textColor=rl_colors.HexColor("#334155"), spaceAfter=4, leading=14)

                    story = []
                    story.append(Paragraph(_n("Kazanım Borç Bankası Raporu"), t_style))
                    story.append(Paragraph(_n(f"{student.tam_ad}  |  {student.sinif}. Sınıf / {student.sube} Şubesi"), s_style))
                    story.append(Paragraph(_n(f"Tarih: {_date.today().strftime('%d.%m.%Y')}"), b_style))
                    story.append(Spacer(1, 10))

                    story.append(Paragraph(_n("Borçlu Kazanımlar"), h_style))
                    if borclar:
                        tbl_data = [[_n("Ders"), _n("Kazanım"), _n("Neden"), _n("Durum"), _n("Tarih")]]
                        for b in borclar:
                            tbl_data.append([
                                _n(b.ders),
                                _n(b.kazanim_metni[:50] + ("..." if len(b.kazanim_metni) > 50 else "")),
                                _n(BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)),
                                _n("Borçlu" if b.durum == "borc_var" else "Kapandı"),
                                _n(b.kazanim_isleme_tarihi[:10] if b.kazanim_isleme_tarihi else "-"),
                            ])
                        tbl = Table(tbl_data, colWidths=[3*cm, 6.5*cm, 4*cm, 2*cm, 2.5*cm])
                        tbl.setStyle(TableStyle([
                            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#7c3aed")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
                            ("FONTNAME", (0, 0), (-1, -1), FONT),
                            ("FONTSIZE", (0, 0), (-1, 0), 9),
                            ("FONTSIZE", (0, 1), (-1, -1), 8),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl_colors.HexColor("#f8f9fa"), rl_colors.white]),
                            ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.HexColor("#e2e8f0")),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("PADDING", (0, 0), (-1, -1), 4),
                        ]))
                        story.append(tbl)
                    else:
                        story.append(Paragraph(_n("Borçlu kazanım bulunmamaktadır."), b_style))

                    ai_key_pdf = f"borc_ai_rapor_{student.id}_{rol}"
                    if ai_key_pdf in st.session_state and st.session_state[ai_key_pdf]:
                        story.append(Spacer(1, 14))
                        story.append(Paragraph(_n("AI Yol Haritası"), h_style))
                        for satir in st.session_state[ai_key_pdf].split("\n"):
                            if satir.strip():
                                story.append(Paragraph(_n(satir.strip()), b_style))

                    doc.build(story)
                    pdf_bytes = buf.getvalue()
                    dosya = f"kazanim_borc_{student.tam_ad.replace(' ', '_')}_{_date.today().strftime('%Y%m%d')}.pdf"
                    st.download_button("⬇️ PDF İndir", data=pdf_bytes, file_name=dosya,
                                       mime="application/pdf", key=f"borc_dl_{student.id}_{rol}")
                    st.success("PDF hazır!")
                except Exception as e:
                    st.error(f"PDF oluşturulamadı: {e}")
    else:
        styled_info_banner("Aktif borç bulunmadığından AI yol haritası ve PDF rapor oluşturulamaz.", "info")


# ===================== VELİ JSON YARDIMCILARI =====================

_VELI_DATA_DIR = get_data_path("akademik")


def _veli_json_path(filename: str) -> str:
    return os.path.join(_VELI_DATA_DIR, filename)


def _load_veli_json(filename: str) -> list[dict]:
    path = _veli_json_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_veli_json(filename: str, data: list[dict]) -> None:
    os.makedirs(_VELI_DATA_DIR, exist_ok=True)
    with open(_veli_json_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── İngilizce Günlük Özet — Veli Raporu Helpers ─────────────────────

_ENG_GUNLUK_OZET_FILE = get_data_path("english", "gunluk_ozet.json")


def _load_eng_daily_summary(tarih: str, sinif, sube: str):
    """Belirli tarih+sinif+sube icin Ingilizce gunluk ozet getir."""
    if not os.path.exists(_ENG_GUNLUK_OZET_FILE):
        return None
    try:
        with open(_ENG_GUNLUK_OZET_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
    except Exception:
        return None
    for r in records:
        if (r.get("tarih") == tarih
                and str(r.get("sinif")) == str(sinif)
                and r.get("sube", "") == (sube or "")):
            return r
    return None


def _build_eng_daily_html(ozet: dict) -> str:
    """Ingilizce gunluk ozet icin premium HTML uret."""
    if not ozet:
        return ""
    theme_tr = ozet.get("theme_tr", "")
    theme = ozet.get("theme", "")
    wn = ozet.get("week_num", "")
    vocab = ozet.get("vocab", [])
    vocab_txt = ", ".join(vocab[:8])
    if len(vocab) > 8:
        vocab_txt += f" +{len(vocab) - 8}"
    structure = ozet.get("structure", "")

    def _acts_html(acts):
        parts = []
        for a in (acts or []):
            icon = a.get("icon", "")
            title = a.get("title", "")
            done = a.get("completed", False)
            mark = "\u2705" if done else "\u2B1C"
            parts.append(f"{mark} {icon} {title}")
        return " &nbsp; ".join(parts) if parts else "\u2014"

    l1_html = _acts_html(ozet.get("lesson_1", []))
    l2_html = _acts_html(ozet.get("lesson_2", []))

    note_html = ""
    if ozet.get("ogretmen_notu"):
        note_html = (
            f'<div style="margin-top:8px;font-size:0.8rem;color:#6d28d9;">'
            f'<b>Not:</b> {ozet["ogretmen_notu"]}</div>')

    structure_html = ""
    if structure:
        structure_html = (
            f'<div style="font-size:0.8rem;color:#475569;margin-bottom:4px;">'
            f'<b>Kalip:</b> {structure}</div>')

    return (
        '<div style="background:linear-gradient(135deg,#ede9fe,#ddd6fe);border-radius:12px;'
        'padding:14px 16px;margin:14px 0;border:1.5px solid #a78bfa">'
        '<div style="font-weight:700;color:#6d28d9;margin-bottom:8px;font-size:0.92rem">'
        f'\U0001F310 Ingilizce Gunluk Ozet \u2014 Hafta {wn}: {theme_tr}'
        + (f' ({theme})' if theme and theme != theme_tr else '') + '</div>'
        f'<div style="font-size:0.82rem;color:#475569;margin-bottom:4px;">'
        f'<b>Kelimeler:</b> {vocab_txt}</div>'
        f'{structure_html}'
        f'<div style="font-size:0.82rem;color:#475569;margin-bottom:4px;">'
        f'<b>1. Ders:</b> {l1_html}</div>'
        f'<div style="font-size:0.82rem;color:#475569;">'
        f'<b>2. Ders:</b> {l2_html}</div>'
        f'{note_html}'
        '</div>'
    )


# ===================== 10. DERS PROGRAMI SEKMESİ =====================


def _render_ders_programi_tab(store: AkademikDataStore, student: Student):
    """Cocugun haftalik ders programi + ogretmen bilgileri — Premium."""
    styled_section("Haftalık Ders Programı", "#2563eb")

    schedule = store.get_schedule(sinif=student.sinif, sube=student.sube)
    if not schedule:
        styled_info_banner("Ders programı henüz oluşturulmamış.", "info")
        return

    gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]
    gun_kisa = {"Pazartesi": "Pzt", "Sali": "Sal", "Carsamba": "Çar", "Persembe": "Per", "Cuma": "Cum"}
    max_saat = max((s.ders_saati for s in schedule), default=8)
    toplam_ders = len(set(s.ders for s in schedule if s.ders))
    ogretmen_set = set(s.ogretmen for s in schedule if s.ogretmen)

    # Bugünün günü
    from datetime import date as _date
    _gun_map = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma"}
    _bugun_gun = _gun_map.get(_date.today().weekday(), "")
    _bugun_ders = sum(1 for s in schedule if s.gun == _bugun_gun and s.ders)

    styled_stat_row([
        ("Toplam Ders", str(toplam_ders), "#2563eb", "📚"),
        ("Öğretmen", str(len(ogretmen_set)), "#7c3aed", "👨‍🏫"),
        ("Bugün", f"{_bugun_ders} ders" if _bugun_ders else "Yok", "#10b981" if _bugun_ders else "#6b7280", "📅"),
    ])

    # Premium HTML tablo
    _hdr_cells = ''.join(
        f'<th style="padding:10px 8px;font-size:0.82rem;font-weight:700;'
        f'color:#0f172a;text-align:center;background:#ffffff;border-bottom:2px solid #6366f1;'
        f'{"background:#eef2ff;" if g == _bugun_gun else ""}'
        f'">{gun_kisa.get(g, g)}</th>'
        for g in gunler
    )
    _rows_html = ""
    for saat in range(1, max_saat + 1):
        _cells = ""
        for g in gunler:
            slot = next((s for s in schedule if s.gun == g and s.ders_saati == saat), None)
            _is_today = g == _bugun_gun
            if slot and slot.ders:
                _ogr_kisa = slot.ogretmen.split()[-1][:8] if slot.ogretmen else ""
                _cell_bg = "#eff6ff" if _is_today else ("#111827" if saat % 2 == 0 else "#fff")
                _cells += (
                    f'<td style="padding:8px 6px;text-align:center;background:{_cell_bg};'
                    f'border-bottom:1px solid #e5e7eb;">'
                    f'<div style="font-weight:600;color:#0f172a;font-size:0.82rem;">{slot.ders}</div>'
                    f'<div style="font-size:0.68rem;color:#6b7280;margin-top:1px;">{_ogr_kisa}</div>'
                    f'</td>'
                )
            else:
                _cell_bg = "#f0f9ff" if _is_today else ("#111827" if saat % 2 == 0 else "#fff")
                _cells += (
                    f'<td style="padding:8px 6px;text-align:center;background:{_cell_bg};'
                    f'border-bottom:1px solid #e5e7eb;color:#d1d5db;">—</td>'
                )
        _rows_html += (
            f'<tr>'
            f'<td style="padding:8px 10px;font-weight:700;color:#0f172a;font-size:0.8rem;'
            f'background:#f1f5f9;border-bottom:1px solid #e5e7eb;white-space:nowrap;">'
            f'{saat}. Ders</td>{_cells}</tr>'
        )

    st.markdown(
        f'<div style="border-radius:12px;overflow:hidden;border:1px solid #dbeafe;'
        f'box-shadow:0 2px 8px rgba(37,99,235,0.08);margin-bottom:16px;">'
        f'<table style="width:100%;border-collapse:collapse;">'
        f'<thead><tr>'
        f'<th style="padding:10px;font-size:0.82rem;font-weight:700;color:#0f172a;'
        f'background:#ffffff;border-bottom:2px solid #6366f1;text-align:left;">Saat</th>'
        f'{_hdr_cells}</tr></thead>'
        f'<tbody>{_rows_html}</tbody></table></div>',
        unsafe_allow_html=True
    )

    # Öğretmen bilgileri — premium kartlar
    styled_section("Öğretmen Bilgileri", "#7c3aed")
    ogretmenler = {}
    for s in schedule:
        if s.ogretmen and s.ders:
            ogretmenler[s.ders] = {"ad": s.ogretmen, "id": s.ogretmen_id}

    if ogretmenler:
        teachers = store.get_teachers()
        teacher_map = {t.id: t for t in teachers}

        cols = st.columns(min(3, len(ogretmenler)))
        for idx, (ders, info) in enumerate(ogretmenler.items()):
            teacher = teacher_map.get(info["id"])
            brans = getattr(teacher, "brans", "-") if teacher else "-"
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);
                            border:1px solid #c4b5fd;border-radius:12px;padding:14px;
                            margin-bottom:8px;text-align:center;
                            box-shadow:0 2px 6px rgba(124,58,237,0.1);">
                    <div style="font-size:1.3rem;margin-bottom:4px;">👨‍🏫</div>
                    <p style="margin:0;font-weight:700;color:#5b21b6;font-size:0.9rem;">{ders}</p>
                    <p style="margin:4px 0 0 0;font-size:0.85rem;color:#0f172a;">{info['ad']}</p>
                    <span style="display:inline-block;margin-top:4px;background:#7c3aed20;color:#7c3aed;
                                 padding:2px 10px;border-radius:20px;font-size:0.72rem;font-weight:600;">
                        {brans}
                    </span>
                </div>
                """, unsafe_allow_html=True)
    else:
        styled_info_banner("Öğretmen bilgisi bulunamadı.", "info")


# ===================== 11. ETKİNLİK & DUYURULAR SEKMESİ =====================

ETKINLIK_DOSYA = "etkinlik_duyurular.json"


def _render_etkinlik_duyuru_tab(student: Student):
    """Okul duyurulari, etkinlik takvimi."""
    styled_section("Duyurular", "#ef4444")

    duyurular = _load_veli_json(ETKINLIK_DOSYA)
    today = date.today()

    # Sadece aktif ve ogrencinin sinif+subesine uygun duyurular
    ogrenci_sinif_sube = f"{student.sinif}/{student.sube}"  # orn: "5/A"
    aktif = []
    for d in duyurular:
        hedef = d.get("hedef_siniflar", [])
        if hedef:
            hedef_lower = [str(h).lower() for h in hedef]
            if "tumu" in hedef_lower:
                pass  # okul geneli, herkese goster
            elif ogrenci_sinif_sube in hedef:
                pass  # "5/A" formatı eslesti
            elif student.sinif in hedef or str(student.sinif) in hedef:
                pass  # eski format: sadece sinif numarasi
            else:
                continue  # bu ogrenciye ait degil
        bitis = d.get("bitis_tarihi", "")
        if bitis:
            try:
                if date.fromisoformat(bitis) < today:
                    continue
            except ValueError:
                pass
        aktif.append(d)

    if not aktif:
        styled_info_banner("Su anda aktif duyuru bulunmuyor.", "info")
    else:
        for d in sorted(aktif, key=lambda x: x.get("tarih", ""), reverse=True):
            tip = d.get("tip", "duyuru")
            tip_icon = {"duyuru": "📢", "etkinlik": "🎉", "toplanti": "📋", "tatil": "🏖️"}.get(tip, "📌")
            tip_renk = {"duyuru": "#3b82f6", "etkinlik": "#8b5cf6", "toplanti": "#f59e0b", "tatil": "#10b981"}.get(tip, "#6b7280")
            onemli = d.get("onemli", False)
            border = f"border-left: 4px solid {tip_renk};"
            if onemli:
                border = f"border: 2px solid #ef4444; border-left: 4px solid #ef4444;"

            with st.expander(f"{tip_icon} {d.get('baslik', 'Duyuru')} {'🔴' if onemli else ''}", expanded=onemli):
                st.markdown(f"""
                <div style="{border} border-radius: 8px; padding: 0.8rem; background: white;">
                    <p style="margin: 0 0 0.5rem 0; font-size: 0.8rem; color: #6b7280;">
                        📅 {d.get('tarih', '-')}
                        {f" | 📍 {d.get('yer', '')}" if d.get('yer') else ""}
                        {f" | 🕐 {d.get('saat', '')}" if d.get('saat') else ""}
                    </p>
                    <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">{d.get('icerik', '')}</p>
                </div>
                """, unsafe_allow_html=True)

    # Etkinlik takvimi - bu ay
    styled_section("Etkinlik Takvimi", "#8b5cf6")
    etkinlikler = [d for d in aktif if d.get("tip") == "etkinlik"]
    if etkinlikler:
        for e in etkinlikler:
            tarih = e.get("tarih", "-")
            yer_text = f" 📍 {e.get('yer', '')}" if e.get("yer") else ""
            st.markdown(f"- **{tarih}** : {e.get('baslik', '')}{yer_text}")
    else:
        styled_info_banner("Bu donemde planli etkinlik yok.", "info")


# ===================== 12. YEMEK MENÜSÜ SEKMESİ =====================

YEMEK_MENU_DOSYA = "yemek_menusu.json"

MONTHS_TR = ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
             "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"]


def _render_gunun_bilgisi_tab():
    """Günün Bilgisi — veliler için günlük bilgi kartı."""
    from datetime import date as _date
    try:
        from models.gunun_bilgisi_kitap import (
            KATEGORILER, get_gunun_bilgisi, get_gecmis_bilgiler, BASLANGIC, BITIS,
        )
    except ImportError:
        st.info("Günün Bilgisi modülü yüklenmemiş.")
        return

    styled_section("Günün Bilgisi", "#6366f1")

    bugun = _date.today()
    bugunun = get_gunun_bilgisi(bugun)

    if not bugunun:
        st.info("Bugün için bilgi henüz eklenmemiş.")
        return

    kat_info = KATEGORILER.get(bugunun["kategori"], {})
    ikon = kat_info.get("icon", "💡")
    baslik_kat = kat_info.get("baslik", "")
    renk = kat_info.get("renk", "#6366f1")

    st.html(f"""
    <div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);border-radius:14px;
        padding:22px 24px;margin-bottom:16px;box-shadow:0 4px 20px rgba(37,99,235,.25)">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
            <span style="font-size:1.5rem">{ikon}</span>
            <span style="font-size:11px;color:rgba(255,255,255,.6);text-transform:uppercase;
                letter-spacing:1px;font-weight:600">{baslik_kat} — {bugun.strftime('%d.%m.%Y')}</span>
        </div>
        <div style="font-size:1.15rem;font-weight:700;color:#fff;margin-bottom:10px;line-height:1.4">
            {bugunun['baslik']}
        </div>
        <div style="font-size:.9rem;color:rgba(255,255,255,.88);line-height:1.8">
            {bugunun['icerik']}
        </div>
    </div>
    """)

    # Son 5 günün bilgisi
    bilgiler = get_gecmis_bilgiler(bugun)
    son_5 = bilgiler[-5:] if len(bilgiler) > 5 else bilgiler
    son_5 = [(d, b) for d, b in son_5 if d != bugun][-4:]

    if son_5:
        st.html('<div style="font-size:.85rem;font-weight:700;color:#475569;margin:12px 0 8px 0">📅 Önceki Günler</div>')
        for tarih, bilgi in reversed(son_5):
            ki = KATEGORILER.get(bilgi["kategori"], {})
            st.html(f"""
            <div style="background:#ffffff;border:1px solid #334155;border-radius:10px;
                padding:12px 16px;margin-bottom:8px;border-left:4px solid {ki.get('renk','#6366f1')}">
                <div style="font-size:.7rem;color:#475569;margin-bottom:3px">
                    {ki.get('icon','')} {ki.get('baslik','')} — {tarih.strftime('%d.%m.%Y')}
                </div>
                <div style="font-size:.85rem;font-weight:600;color:#475569">{bilgi['baslik']}</div>
            </div>
            """)


def _render_yemek_menusu_tab():
    """Aylik yemek menusu goruntuleme — Kahvaltı / Öğle / İkindi."""
    styled_section("Aylık Yemek Menüsü", "#f59e0b")

    menuler_raw = _load_veli_json(YEMEK_MENU_DOSYA)
    today = date.today()

    # Normalize tüm kayıtlar (eski+yeni format)
    def _norm(m):
        if "kahvalti" in m or "ogle_yemegi" in m or "ikindi_ara_ogun" in m:
            return m
        ogun = m.get("ogun", "Ogle Yemegi")
        ylist = m.get("yemekler", [])
        if "Sabah" in ogun or "Kahvalti" in ogun:
            return {**m, "kahvalti": ylist, "ogle_yemegi": [], "ikindi_ara_ogun": []}
        elif "Ikindi" in ogun:
            return {**m, "kahvalti": [], "ogle_yemegi": [], "ikindi_ara_ogun": ylist}
        return {**m, "kahvalti": [], "ogle_yemegi": ylist, "ikindi_ara_ogun": []}

    menuler_map = {m.get("tarih"): _norm(m) for m in menuler_raw if m.get("tarih")}

    # Ay seçici
    ay_col1, ay_col2 = st.columns(2)
    with ay_col1:
        secili_ay = st.selectbox("Ay", list(range(1, 13)),
                                  index=today.month - 1,
                                  format_func=lambda x: MONTHS_TR[x - 1],
                                  key="yemek_ay")
    with ay_col2:
        secili_yil = st.selectbox("Yıl", [today.year - 1, today.year, today.year + 1],
                                   index=1, key="yemek_yil")

    ay_key = f"{secili_yil}-{secili_ay:02d}"
    ay_m = {t: m for t, m in menuler_map.items() if t.startswith(ay_key)}

    if not ay_m:
        styled_info_banner(
            f"{MONTHS_TR[secili_ay - 1]} {secili_yil} için yemek menüsü henüz girilmemiş.", "info")
        return

    st.markdown(f"### 🍽️ {MONTHS_TR[secili_ay - 1]} {secili_yil} Yemek Menüsü")

    # Renk gösterge
    st.markdown(
        '<div style="display:flex;gap:12px;font-size:0.75rem;margin-bottom:8px;">'
        '<span>☕ <b>Kahvaltı</b></span>'
        '<span>🍽️ <b>Öğle</b></span>'
        '<span>🍎 <b>İkindi</b></span>'
        '</div>', unsafe_allow_html=True
    )

    # Takvim başlık satırı
    gunler_tr = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    cols_header = st.columns(7)
    for i, gun in enumerate(gunler_tr):
        with cols_header[i]:
            st.markdown(
                f"<div style='text-align:center;font-weight:700;color:#6b7280;"
                f"font-size:0.8rem;padding-bottom:4px;'>{gun}</div>",
                unsafe_allow_html=True)

    cal = calendar.monthcalendar(secili_yil, secili_ay)

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("")
                    continue
                tarih_str = f"{secili_yil}-{secili_ay:02d}-{day:02d}"
                menu = ay_m.get(tarih_str)
                is_today = (tarih_str == today.isoformat())
                bg     = "#dbeafe" if is_today else ("#fffbeb" if menu else "#111827")
                border = "2px solid #3b82f6" if is_today else "1px solid #e5e7eb"

                if menu:
                    kah  = menu.get("kahvalti", [])
                    ogle = menu.get("ogle_yemegi", [])
                    ik   = menu.get("ikindi_ara_ogun", [])

                    html_ic = f'<strong style="color:#0f172a;">{day}</strong>'
                    if kah:
                        html_ic += (f'<div style="margin-top:2px;">'
                                    f'<span style="color:#92400e;font-size:0.6rem;font-weight:700;">☕</span> '
                                    + "<br>".join(f'<span style="color:#78350f;font-size:0.62rem;">• {y}</span>' for y in kah[:2])
                                    + '</div>')
                    if ogle:
                        html_ic += (f'<div style="margin-top:2px;">'
                                    f'<span style="color:#1d4ed8;font-size:0.6rem;font-weight:700;">🍽️</span> '
                                    + "<br>".join(f'<span style="color:#1e3a8a;font-size:0.62rem;">• {y}</span>' for y in ogle[:3])
                                    + '</div>')
                    if ik:
                        html_ic += (f'<div style="margin-top:2px;">'
                                    f'<span style="color:#166534;font-size:0.6rem;font-weight:700;">🍎</span> '
                                    + "<br>".join(f'<span style="color:#14532d;font-size:0.62rem;">• {y}</span>' for y in ik[:2])
                                    + '</div>')

                    st.markdown(
                        f'<div style="background:{bg};border:{border};border-radius:8px;'
                        f'padding:0.35rem;min-height:90px;margin-bottom:0.3rem;">'
                        f'{html_ic}</div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div style="background:{bg};border:{border};border-radius:8px;'
                        f'padding:0.35rem;min-height:90px;margin-bottom:0.3rem;">'
                        f'<strong style="color:#9ca3af;">{day}</strong></div>',
                        unsafe_allow_html=True)


# ===================== 13. SERVİS TAKİBİ SEKMESİ =====================

SERVIS_DOSYA = "servis_bilgileri.json"


def _render_servis_tab(student: Student):
    """Servis guzergahi ve bilgileri — Premium."""
    styled_section("Servis Takibi", "#10b981")

    servisler = _load_veli_json(SERVIS_DOSYA)

    ogrenci_servis = None
    for s in servisler:
        ogrenci_ids = s.get("ogrenci_ids", [])
        ogrenci_adlari = s.get("ogrenci_adlari", [])
        if student.id in ogrenci_ids or student.tam_ad in ogrenci_adlari:
            ogrenci_servis = s
            break

    if not ogrenci_servis:
        styled_info_banner("Öğrenci için servis kaydı bulunamadı. Servis kullanmıyorsanız bu normaldir.", "info")
        if servisler:
            styled_section("Mevcut Servis Güzergahları", "#64748b")
            for s in servisler:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#111827,#1A2035);border:1px solid #334155;'
                    f'border-radius:10px;padding:10px 14px;margin-bottom:6px;">'
                    f'<span style="font-weight:600;color:#0f172a;">🚌 {s.get("hat_adi", "-")}</span>'
                    f'<span style="margin-left:12px;font-size:0.8rem;color:#6b7280;">Şoför: {s.get("sofor_adi", "-")}</span>'
                    f'</div>', unsafe_allow_html=True)
        return

    # Premium stat row
    styled_stat_row([
        ("Güzergah", ogrenci_servis.get("hat_adi", "-"), "#10b981", "🚌"),
        ("Sabah", ogrenci_servis.get("sabah_saat", "-"), "#2563eb", "🌅"),
        ("Akşam", ogrenci_servis.get("aksam_saat", "-"), "#f59e0b", "🌇"),
    ])

    # Premium servis detay kartları
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;'
            f'border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(16,185,129,0.1);">'
            f'<div style="font-size:1.2rem;margin-bottom:8px;">🚌</div>'
            f'<div style="font-weight:700;color:#166534;font-size:0.95rem;margin-bottom:10px;">Servis Bilgileri</div>'
            f'<table style="width:100%;font-size:0.85rem;border-collapse:collapse;">'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #d1fae5;">Hat</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #d1fae5;">{ogrenci_servis.get("hat_adi", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #d1fae5;">Plaka</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #d1fae5;">{ogrenci_servis.get("plaka", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #d1fae5;">Şoför</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #d1fae5;">{ogrenci_servis.get("sofor_adi", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;">Telefon</td>'
            f'<td style="font-weight:600;padding:5px 0;">{ogrenci_servis.get("sofor_tel", "-")}</td></tr>'
            f'</table></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #93c5fd;'
            f'border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(37,99,235,0.1);">'
            f'<div style="font-size:1.2rem;margin-bottom:8px;">⏰</div>'
            f'<div style="font-weight:700;color:#1d4ed8;font-size:0.95rem;margin-bottom:10px;">Saat & Durak</div>'
            f'<table style="width:100%;font-size:0.85rem;border-collapse:collapse;">'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #bfdbfe;">Sabah Alınma</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #bfdbfe;">{ogrenci_servis.get("sabah_saat", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #bfdbfe;">Akşam Bırakma</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #bfdbfe;">{ogrenci_servis.get("aksam_saat", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;border-bottom:1px solid #bfdbfe;">Durak</td>'
            f'<td style="font-weight:600;padding:5px 0;border-bottom:1px solid #bfdbfe;">{ogrenci_servis.get("durak", "-")}</td></tr>'
            f'<tr><td style="color:#6b7280;padding:5px 0;">Hostes</td>'
            f'<td style="font-weight:600;padding:5px 0;">{ogrenci_servis.get("hostes_adi", "-")}</td></tr>'
            f'</table></div>', unsafe_allow_html=True)

    # Güzergah — Timeline style
    duraklar = ogrenci_servis.get("duraklar", [])
    if duraklar:
        styled_section("Güzergah", "#0ea5e9")
        _timeline_html = ""
        for idx, durak in enumerate(duraklar):
            _is_first = idx == 0
            _is_last = idx == len(duraklar) - 1
            _icon = "🏠" if _is_first else ("🏫" if _is_last else "📍")
            _dot_color = "#10b981" if _is_first else ("#2563eb" if _is_last else "#94a3b8")
            _line = "" if _is_last else f'<div style="width:3px;height:20px;background:#e2e8f0;margin-left:9px;"></div>'
            _timeline_html += (
                f'<div style="display:flex;align-items:center;gap:12px;">'
                f'<div style="width:20px;height:20px;border-radius:50%;background:{_dot_color};'
                f'display:flex;align-items:center;justify-content:center;font-size:0.6rem;color:#fff;'
                f'flex-shrink:0;box-shadow:0 2px 4px {_dot_color}40;">●</div>'
                f'<div style="flex:1;background:linear-gradient(135deg,#111827,#1A2035);'
                f'border:1px solid #334155;border-radius:10px;padding:8px 14px;">'
                f'<span style="font-weight:600;color:#0f172a;font-size:0.85rem;">{_icon} {durak.get("ad", "-")}</span>'
                f'<span style="margin-left:10px;font-size:0.78rem;color:#6b7280;">{durak.get("saat", "-")}</span>'
                f'</div></div>{_line}'
            )
        st.markdown(
            f'<div style="padding:8px 0;">{_timeline_html}</div>',
            unsafe_allow_html=True
        )


# ===================== 14. RANDEVU SİSTEMİ SEKMESİ =====================

RANDEVU_DOSYA = "veli_randevular.json"


def _render_randevu_tab(store: AkademikDataStore, student: Student, auth_user: dict):
    """Veli-ogretmen gorusme randevusu alma — Premium."""
    styled_section("Randevu Yönetimi", "#8b5cf6")

    randevular = _load_veli_json(RANDEVU_DOSYA)
    username = auth_user.get("username", "")
    veli_randevular = [r for r in randevular if r.get("veli_id") == username]
    aktif_randevular = [r for r in veli_randevular
                        if r.get("durum") in ("beklemede", "onaylandi")
                        and r.get("tarih", "") >= date.today().isoformat()]
    _onaylanan = sum(1 for r in aktif_randevular if r.get("durum") == "onaylandi")
    _bekleyen = sum(1 for r in aktif_randevular if r.get("durum") == "beklemede")

    styled_stat_row([
        ("Aktif Randevu", str(len(aktif_randevular)), "#8b5cf6", "📅"),
        ("Onaylanan", str(_onaylanan), "#10b981", "✅"),
        ("Bekleyen", str(_bekleyen), "#f59e0b" if _bekleyen else "#6b7280", "⏳"),
    ])

    if aktif_randevular:
        styled_section("Aktif Randevularınız", "#10b981")
        for r in sorted(aktif_randevular, key=lambda x: x.get("tarih", "")):
            _is_ok = r.get("durum") == "onaylandi"
            _bg = "linear-gradient(135deg,#f0fdf4,#dcfce7)" if _is_ok else "linear-gradient(135deg,#fffbeb,#fef3c7)"
            _border = "#86efac" if _is_ok else "#fcd34d"
            _badge_bg = "#16a34a" if _is_ok else "#f59e0b"
            _badge_text = "✅ Onaylandı" if _is_ok else "⏳ Onay Bekliyor"
            _konu_html = f'<div style="margin-top:6px;font-size:0.78rem;color:#6b7280;">📝 {r.get("konu", "")}</div>' if r.get("konu") else ""
            st.markdown(
                f'<div style="background:{_bg};border:1px solid {_border};border-radius:12px;'
                f'padding:14px 16px;margin-bottom:8px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                f'<div><div style="font-weight:700;color:#0f172a;font-size:0.9rem;">👤 {r.get("ogretmen_adi", "-")}</div>'
                f'<div style="font-size:0.82rem;color:#0f172a;margin-top:3px;">'
                f'📅 {r.get("tarih", "-")} · 🕐 {r.get("saat", "-")} · 📍 {r.get("yer", "Okul")}</div>'
                f'{_konu_html}</div>'
                f'<span style="background:{_badge_bg};color:#fff;padding:4px 14px;border-radius:20px;'
                f'font-size:0.72rem;font-weight:600;white-space:nowrap;">{_badge_text}</span>'
                f'</div></div>', unsafe_allow_html=True)

    # Yeni randevu formu
    styled_section("Yeni Randevu Oluştur", "#3b82f6")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #93c5fd;'
        'border-radius:12px;padding:12px 16px;margin-bottom:10px;font-size:0.82rem;color:#1e40af;">'
        '📅 Öğretmen veya yönetimle görüşme randevusu oluşturun.</div>',
        unsafe_allow_html=True
    )

    teachers = store.get_teachers()
    if not teachers:
        styled_info_banner("Öğretmen listesi yuklenemedi.", "warning")
        return

    ogretmen_map = {t.id: f"{t.ad} {t.soyad} ({getattr(t, 'brans', '-')})" for t in teachers}
    ogretmen_map["yonetim"] = "Okul Yönetimi"
    ogretmen_map["rehberlik"] = "Rehberlik Servisi"

    with st.form("veli_randevu_form", clear_on_submit=True):
        ogretmen_id = st.selectbox(
            "Görüşmek Istediginiz Kisi",
            list(ogretmen_map.keys()),
            format_func=lambda x: ogretmen_map[x],
            key="randevu_ogretmen"
        )

        r_col1, r_col2 = st.columns(2)
        with r_col1:
            randevu_tarihi = st.date_input("Tarih", min_value=date.today(),
                                            value=date.today() + timedelta(days=1),
                                            key="randevu_tarih")
        with r_col2:
            saat_options = [f"{h:02d}:{m:02d}" for h in range(9, 17) for m in (0, 30)]
            randevu_saati = st.selectbox("Saat", saat_options, index=4, key="randevu_saat")

        konu = st.text_input("Görüşme Konusu", key="randevu_konu",
                              placeholder="Ornegin: Matematik dersi hakkinda")
        notlar = st.text_area("Ek Notlar (opsiyonel)", key="randevu_not", height=80)
        yer = st.radio("Görüşme Sekli", ["Yuz Yuze (Okulda)", "Online (Zoom)"],
                       horizontal=True, key="randevu_yer")

        gonder = st.form_submit_button("Randevu Talebi Gonder", type="primary",
                                        use_container_width=True)

    if gonder:
        if not konu:
            st.error("Görüşme konusu zorunludur.")
            return
        yeni_randevu = {
            "id": f"rdv_{uuid.uuid4().hex[:8]}",
            "veli_id": username,
            "veli_adi": auth_user.get("name", ""),
            "ogrenci_id": student.id,
            "ogrenci_adi": student.tam_ad,
            "ogretmen_id": ogretmen_id,
            "ogretmen_adi": ogretmen_map.get(ogretmen_id, "-"),
            "tarih": randevu_tarihi.isoformat(),
            "saat": randevu_saati,
            "konu": konu,
            "notlar": notlar,
            "yer": "Okul" if "Yuz" in yer else "Online",
            "durum": "beklemede",
            "created_at": datetime.now().isoformat(),
        }
        randevular.append(yeni_randevu)
        _save_veli_json(RANDEVU_DOSYA, randevular)
        st.success("Randevu talebiniz gonderildi! Onay sonrasi bilgilendirileceksiniz.")
        st.rerun()

    # Gecmis randevular
    gecmis = [r for r in veli_randevular
              if r.get("tarih", "") < date.today().isoformat() or r.get("durum") == "tamamlandı"]
    if gecmis:
        styled_section("Geçmiş Randevular", "#64748b")
        with st.expander(f"Geçmiş ({len(gecmis)})", expanded=False):
            for r in sorted(gecmis, key=lambda x: x.get("tarih", ""), reverse=True)[:10]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#111827,#1A2035);border:1px solid #334155;'
                    f'border-radius:10px;padding:10px 14px;margin-bottom:6px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-size:0.82rem;color:#0f172a;">'
                    f'📅 {r.get("tarih", "-")} · 👤 {r.get("ogretmen_adi", "-")}</span>'
                    f'<span style="font-size:0.72rem;color:#6b7280;">📝 {r.get("konu", "-")}</span>'
                    f'</div></div>', unsafe_allow_html=True
                )


# ===================== 15. BELGE TALEP SEKMESİ =====================

BELGE_TALEP_DOSYA = "veli_belge_talepleri.json"

BELGE_TURLERI = [
    ("ogrenci_belgesi", "Öğrenci Belgesi"),
    ("transkript", "Transkript / Not Çokumu"),
    ("devamsizlik_belgesi", "Devamsızlık Belgesi"),
    ("nakil_belgesi", "Nakil Belgesi"),
    ("bursluluk_belgesi", "Bursluluk Belgesi"),
    ("ogrenim_belgesi", "Ogrenim Belgesi"),
    ("askerlik_belgesi", "Askerlik Tecil Belgesi"),
    ("disiplin_belgesi", "Disiplin Durumu Belgesi"),
    ("mezuniyet_belgesi", "Mezuniyet Belgesi"),
    ("diger", "Diger"),
]


def _render_belge_talep_tab(student: Student, auth_user: dict):
    """Online belge talebi (ogrenci belgesi, transkript vb.) — Premium."""
    styled_section("Belge Talebi", "#0369a1")

    talepler = _load_veli_json(BELGE_TALEP_DOSYA)
    username = auth_user.get("username", "")
    veli_talepler = [t for t in talepler if t.get("veli_id") == username]
    aktif_talepler = [t for t in veli_talepler if t.get("durum") in ("beklemede", "hazirlaniyor")]
    tamamlanan = [t for t in veli_talepler if t.get("durum") == "tamamlandı"]

    styled_stat_row([
        ("Toplam Talep", str(len(veli_talepler)), "#0369a1", "📄"),
        ("Aktif", str(len(aktif_talepler)), "#f59e0b" if aktif_talepler else "#6b7280", "⏳"),
        ("Tamamlanan", str(len(tamamlanan)), "#10b981", "✅"),
    ])

    if aktif_talepler:
        styled_section("Aktif Talepleriniz", "#f59e0b")
        for t in aktif_talepler:
            durum_map = {"beklemede": ("⏳", "Beklemede", "linear-gradient(135deg,#fffbeb,#fef3c7)", "#92400e", "#fcd34d"),
                         "hazirlaniyor": ("📝", "Hazırlanıyor", "linear-gradient(135deg,#eff6ff,#dbeafe)", "#1e40af", "#93c5fd")}
            icon, text, bg, color, border = durum_map.get(t.get("durum"), ("⏳", "Beklemede", "linear-gradient(135deg,#fffbeb,#fef3c7)", "#92400e", "#fcd34d"))
            belge_label = dict(BELGE_TURLERI).get(t.get("belge_turu", ""), t.get("belge_turu", ""))
            st.markdown(
                f'<div style="background:{bg};border:1px solid {border};border-radius:12px;'
                f'padding:14px 16px;margin-bottom:8px;box-shadow:0 2px 6px {color}10;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div><div style="font-weight:700;color:{color};font-size:0.9rem;">📄 {belge_label}</div>'
                f'<div style="font-size:0.78rem;color:#6b7280;margin-top:3px;">'
                f'Talep: {t.get("created_at", "-")[:10]} · Adet: {t.get("adet", 1)}'
                f'{"  · 🔴 Acil" if t.get("acil") else ""}</div></div>'
                f'<span style="background:{color};color:#fff;padding:4px 14px;border-radius:20px;'
                f'font-size:0.72rem;font-weight:600;">{icon} {text}</span>'
                f'</div></div>', unsafe_allow_html=True)

    # Yeni talep formu
    styled_section("Yeni Belge Talebi", "#3b82f6")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #93c5fd;'
        'border-radius:12px;padding:12px 16px;margin-bottom:10px;font-size:0.82rem;color:#1e40af;">'
        '📋 Aşağıdan belge türünü seçerek talepte bulunabilirsiniz.</div>',
        unsafe_allow_html=True
    )

    with st.form("veli_belge_form", clear_on_submit=True):
        belge_turu = st.selectbox(
            "Belge Türü",
            [k for k, _ in BELGE_TURLERI],
            format_func=lambda x: dict(BELGE_TURLERI).get(x, x),
            key="belge_tur"
        )
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            adet = st.number_input("Adet", min_value=1, max_value=5, value=1, key="belge_adet")
        with b_col2:
            acil = st.checkbox("Acil Talep", key="belge_acil")
        aciklama = st.text_area("Açıklama (opsiyonel)", key="belge_aciklama", height=80,
                                 placeholder="Belge ile ilgili ek bilgi veya not")
        gonder = st.form_submit_button("Belge Talebini Gönder", type="primary",
                                        use_container_width=True)

    if gonder:
        yeni_talep = {
            "id": f"bt_{uuid.uuid4().hex[:8]}",
            "veli_id": username,
            "veli_adi": auth_user.get("name", ""),
            "ogrenci_id": student.id,
            "ogrenci_adi": student.tam_ad,
            "sinif_sube": f"{student.sinif}/{student.sube}",
            "belge_turu": belge_turu,
            "adet": adet,
            "acil": acil,
            "aciklama": aciklama,
            "durum": "beklemede",
            "created_at": datetime.now().isoformat(),
        }
        talepler.append(yeni_talep)
        _save_veli_json(BELGE_TALEP_DOSYA, talepler)
        belge_label = dict(BELGE_TURLERI).get(belge_turu, belge_turu)
        st.success(f"'{belge_label}' talebiniz başarıyla gönderildi!")
        st.rerun()

    # Tamamlanan talepler
    if tamamlanan:
        styled_section("Tamamlanan Talepler", "#10b981")
        with st.expander(f"Geçmiş ({len(tamamlanan)})", expanded=False):
            for t in sorted(tamamlanan, key=lambda x: x.get("created_at", ""), reverse=True):
                belge_label = dict(BELGE_TURLERI).get(t.get("belge_turu", ""), t.get("belge_turu", ""))
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;'
                    f'border-radius:10px;padding:10px 14px;margin-bottom:6px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-weight:600;color:#166534;">✅ {belge_label}</span>'
                    f'<span style="font-size:0.72rem;color:#6b7280;">'
                    f'Talep: {t.get("created_at", "-")[:10]} · Tamamlanma: '
                    f'{t.get("tamamlanma_tarihi", "-")[:10] if t.get("tamamlanma_tarihi") else "-"}'
                    f'</span></div></div>', unsafe_allow_html=True
                )


# ===================== SMARTİ AI ASİSTAN TAB =====================

_SMARTI_MASCOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "assets", "mascot.png")

_SMARTI_PREFIX = "panel_smarti_"


def _smarti_ss(key: str):
    """Panel Smarti için session state key."""
    return f"{_SMARTI_PREFIX}{key}"


def _smarti_hitap(auth_user: dict) -> str:
    """Kullanıcıya uygun hitap şekli: Bey/Hanım veya ad soyad."""
    name = auth_user.get("name", "").strip()
    cinsiyet = auth_user.get("cinsiyet", "").strip().lower()
    if not name:
        return "Sayın Kullanıcı"
    parts = name.split()
    ad = parts[0]
    if cinsiyet in ("erkek", "e", "bay"):
        return f"{ad} Bey"
    elif cinsiyet in ("kadin", "k", "bayan", "kadın"):
        return f"{ad} Hanım"
    else:
        return name


def _render_aktif_sinavlar_banner(student: Student):
    """Ogrenci panelinin en ustunde aktif sinavlari gosterir — tab'lardan once."""
    try:
        from models.olcme_degerlendirme import DataStore as _ODS, ExamSession, StudentAnswer, AutoGrader
        _od = _ODS()
        all_exams = _od.get_exams()
        # Ogrencinin sinifina uygun sinavlar (created + active)
        sinif_sinavlar = all_exams
        try:
            sinif_int = int(student.sinif)
            sinif_uygun = [e for e in all_exams if e.grade == sinif_int and e.status in ("created", "active")]
            if sinif_uygun:
                sinif_sinavlar = sinif_uygun
            else:
                sinif_sinavlar = [e for e in all_exams if e.status in ("created", "active")]
        except (ValueError, TypeError):
            sinif_sinavlar = [e for e in all_exams if e.status in ("created", "active")]

        if not sinif_sinavlar:
            return

        # Bu ogrencinin daha once cozdugu sinavlari bul
        student_id = f"{student.numara}_{student.sube}"
        sessions = _od.get_sessions()
        my_sessions = {s.exam_id: s for s in sessions if s.student_id == student_id}

        # Kategorize: baslatilmis (cozulebilir) vs bekleyen (henuz baslatilmamis)
        baslatilmis = []  # active — ogrenci cozebilir
        bekleyen = []     # created — ogrenci gorebilir ama cozemez
        for e in sinif_sinavlar:
            s = my_sessions.get(e.id)
            if s and s.status == "submitted":
                continue  # zaten cozmis, gosterme
            if e.status == "active":
                baslatilmis.append(e)
            elif e.status == "created":
                bekleyen.append(e)

        if not baslatilmis and not bekleyen:
            return

        # ── BASLATILMIS SINAVLAR — cozulebilir ──
        if baslatilmis:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#7f1d1d 0%,#991b1b 50%,#b91c1c 100%);
            border-radius:16px;padding:18px 24px;margin:10px 0 8px 0;
            border:2px solid rgba(239,68,68,0.4);">
            <style>@keyframes pulse2{{0%,100%{{box-shadow:0 0 8px rgba(239,68,68,0.3)}}50%{{box-shadow:0 0 20px rgba(239,68,68,0.6)}}}}</style>
            <div style="font-size:1.1rem;font-weight:900;color:#fca5a5;">
            🚨 {len(baslatilmis)} Sınav Başladı — Hemen Çöz!</div>
            <div style="font-size:.82rem;color:#fecaca;margin-top:4px;">
            Öğretmenin sınavı başlattı. Süre işliyor!</div>
            </div>""", unsafe_allow_html=True)

            for exam in baslatilmis:
                ec1, ec2 = st.columns([3, 1])
                with ec1:
                    st.markdown(f"""<div style="background:#ffffff;border-radius:10px;padding:12px 16px;
                    margin:4px 0;border-left:4px solid #ef4444;">
                    <div style="font-size:.92rem;font-weight:700;color:#fca5a5;">📝 {exam.name}</div>
                    <div style="font-size:.78rem;color:#475569;">
                    {exam.subject} · {len(exam.question_ids)} soru · {exam.duration_minutes} dk</div>
                    </div>""", unsafe_allow_html=True)
                with ec2:
                    if st.button(f"🚀 Çöz", key=f"ogr_banner_start_{exam.id}",
                                   type="primary", use_container_width=True):
                        st.session_state["_sidebar_secim"] = "Olcme ve Degerlendirme"
                        st.session_state["verified_exam_id"] = exam.id
                        st.session_state["verified_exam_code"] = getattr(exam, "access_code", "")
                        st.rerun()

        # ── BEKLEYEN SINAVLAR — henuz baslatilmamis ──
        if bekleyen:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1c1917 0%,#292524 100%);
            border-radius:14px;padding:14px 20px;margin:8px 0;
            border:1px solid rgba(245,158,11,0.3);">
            <div style="font-size:.9rem;font-weight:700;color:#fcd34d;">
            ⏳ {len(bekleyen)} Sınav Hazırlanıyor</div>
            <div style="font-size:.78rem;color:#d4d4d4;margin-top:3px;">
            Öğretmenin sınavı başlatmasını bekle</div>
            </div>""", unsafe_allow_html=True)

            for exam in bekleyen:
                st.markdown(f"""<div style="background:#ffffff;border-radius:8px;padding:10px 14px;
                margin:3px 0;border-left:3px solid #f59e0b;opacity:0.7;">
                <span style="color:#fcd34d;font-size:.85rem;">⏳ {exam.name}</span>
                <span style="color:#64748b;font-size:.75rem;margin-left:8px;">
                {exam.subject} · {len(exam.question_ids)} soru — beklemede</span>
                </div>""", unsafe_allow_html=True)

    except Exception:
        pass  # OD modulu yuklenemediyse sessizce gec

    # ── CEFR Aktif Sinavlar ──
    try:
        from models.cefr_exam import CEFRPlacementStore
        _cp = CEFRPlacementStore()
        cp_exams = _cp.list_exams()

        # Sinifa uygun + published (baslatilmis)
        cp_aktif = []
        cp_bekleyen = []
        try:
            sinif_int = int(student.sinif)
            for e in cp_exams:
                if e.grade == sinif_int or e.sinif == sinif_int:
                    if e.status == "published":
                        # Daha once cozmis mi?
                        stu_results = _cp.get_student_results(student.id)
                        cozdu = any(r.exam_id == e.id for r in stu_results)
                        if not cozdu:
                            cp_aktif.append(e)
                    elif e.status == "created":
                        cp_bekleyen.append(e)
        except (ValueError, TypeError):
            pass

        if cp_aktif:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#312e81 0%,#4c1d95 100%);
            border-radius:16px;padding:18px 24px;margin:10px 0 8px 0;
            border:2px solid rgba(139,92,246,0.4);">
            <div style="font-size:1.1rem;font-weight:900;color:#c4b5fd;">
            🌍 {len(cp_aktif)} CEFR Seviye Tespit Sinavi Basladi!</div>
            <div style="font-size:.82rem;color:#a5b4fc;margin-top:4px;">
            Ingilizce seviye tespit sinavini hemen coz</div>
            </div>""", unsafe_allow_html=True)

            for exam in cp_aktif:
                period_label = "Sene Basi" if exam.period == "sene_basi" else "Sene Sonu"
                ec1, ec2 = st.columns([3, 1])
                with ec1:
                    st.markdown(f"""<div style="background:#ffffff;border-radius:10px;padding:12px 16px;
                    margin:4px 0;border-left:4px solid #8b5cf6;">
                    <div style="font-size:.92rem;font-weight:700;color:#c4b5fd;">🌍 {exam.name}</div>
                    <div style="font-size:.78rem;color:#475569;">
                    {exam.cefr} · {len(exam.questions)} soru · {exam.duration_min} dk · {period_label}</div>
                    </div>""", unsafe_allow_html=True)
                with ec2:
                    if st.button("🚀 Çöz", key=f"ogr_cefr_start_{exam.id}",
                                   type="primary", use_container_width=True):
                        st.session_state["_sidebar_secim"] = "Yabanci Dil"
                        st.session_state["yd_view"] = "cefr_placement"
                        st.rerun()

        if cp_bekleyen:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1c1917,#292524);
            border-radius:14px;padding:14px 20px;margin:8px 0;
            border:1px solid rgba(139,92,246,0.2);">
            <div style="font-size:.9rem;font-weight:700;color:#a78bfa;">
            ⏳ {len(cp_bekleyen)} CEFR Sinavi Hazirlaniyor</div>
            <div style="font-size:.78rem;color:#d4d4d4;margin-top:3px;">
            Ogretmenin sinavi baslatmasini bekle</div>
            </div>""", unsafe_allow_html=True)
    except Exception:
        pass

    # ── YD Unite Quizleri ──
    try:
        from models.yd_assessment import YdAssessmentStore
        _yd_store = YdAssessmentStore()
        sinif_int = int(student.sinif)
        sube_str = str(student.sube)
        _yd_level = f"grade{sinif_int}" if 1 <= sinif_int <= 12 else None
        if _yd_level:
            yd_started = _yd_store.get_exams(level=_yd_level, sinif=sinif_int, sube=sube_str,
                                              category="quiz", status="started")
            yd_sent = _yd_store.get_exams(level=_yd_level, sinif=sinif_int, sube=sube_str,
                                           category="quiz", status="sent")
            # Ogrencinin cevapladigi quizleri bul
            _stu_id = getattr(student, "id", "") or f"{student.numara}_{student.sube}"
            _yd_answers = _yd_store.get_student_answers(student_id=_stu_id)
            _yd_submitted = {a.exam_id for a in _yd_answers if a.status == "submitted"}

            yd_aktif = [e for e in yd_started if e.id not in _yd_submitted]
            yd_bekleyen = [e for e in yd_sent if e.id not in _yd_submitted]

            # Sure dolmus olanlari filtrele
            from datetime import datetime as _dt_yd
            yd_aktif_valid = []
            for e in yd_aktif:
                if e.deadline:
                    try:
                        if _dt_yd.fromisoformat(e.deadline) > _dt_yd.now():
                            yd_aktif_valid.append(e)
                    except Exception:
                        yd_aktif_valid.append(e)
                else:
                    yd_aktif_valid.append(e)

            if yd_aktif_valid:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1e1b4b 0%,#4338ca 100%);
                border-radius:16px;padding:18px 24px;margin:10px 0 8px 0;
                border:2px solid rgba(99,102,241,0.4);">
                <div style="font-size:1.1rem;font-weight:900;color:#a5b4fc;">
                🌍 {len(yd_aktif_valid)} Ingilizce Quiz Basladi!</div>
                <div style="font-size:.82rem;color:#c7d2fe;margin-top:4px;">
                Unite quiz'ini hemen coz — sure isliyor!</div>
                </div>""", unsafe_allow_html=True)

                for exam in yd_aktif_valid:
                    remaining = ""
                    if exam.deadline:
                        try:
                            rem_sec = (_dt_yd.fromisoformat(exam.deadline) - _dt_yd.now()).total_seconds()
                            rem_min = max(0, int(rem_sec // 60))
                            remaining = f" · ⏱ {rem_min} dk kaldi"
                        except Exception:
                            pass
                    ec1, ec2 = st.columns([3, 1])
                    with ec1:
                        st.markdown(f"""<div style="background:#ffffff;border-radius:10px;padding:12px 16px;
                        margin:4px 0;border-left:4px solid #6366f1;">
                        <div style="font-size:.92rem;font-weight:700;color:#a5b4fc;">🌍 {exam.name}</div>
                        <div style="font-size:.78rem;color:#475569;">
                        {len(exam.questions)} soru · {exam.duration_minutes} dk{remaining}</div>
                        </div>""", unsafe_allow_html=True)
                    with ec2:
                        if st.button("🚀 Coz", key=f"ogr_ydquiz_{exam.id}",
                                       type="primary", use_container_width=True):
                            # Direkt YD Quiz Ogrenci ekrani — auto-fill ile
                            st.session_state["_sidebar_secim"] = "Yabanci Dil"
                            st.session_state["yd_view"] = "yd_quiz"
                            st.session_state["yd_quiz_target_tab"] = "ogrenci"
                            st.session_state["yd_quiz_target_exam_id"] = exam.id
                            st.rerun()

            if yd_bekleyen:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#1c1917,#292524);
                border-radius:14px;padding:14px 20px;margin:8px 0;
                border:1px solid rgba(99,102,241,0.2);">
                <div style="font-size:.9rem;font-weight:700;color:#818cf8;">
                ⏳ {len(yd_bekleyen)} Ingilizce Quiz Hazirlaniyor</div>
                <div style="font-size:.78rem;color:#d4d4d4;margin-top:3px;">
                Ogretmenin quiz'i baslatmasini bekle</div>
                </div>""", unsafe_allow_html=True)
    except Exception:
        pass


def _render_smarti_top_greeting(auth_user: dict, student: Student | None = None):
    """Ust kisimda Smarti karsilama + mini sohbet kutusu."""
    mascot_path = _SMARTI_MASCOT
    if os.path.exists(mascot_path):
        with open(mascot_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        avatar_html = f'<img src="data:image/png;base64,{img_b64}" style="width:56px;height:56px;border-radius:50%;object-fit:cover;border:3px solid #a855f7;" />'
    else:
        avatar_html = '<span style="font-size:2.5rem;">🤖</span>'

    hitap = _smarti_hitap(auth_user)
    saat = datetime.now().hour
    if saat < 6:
        selamlama = "İyi geceler"
        alt_emoji = "🌙"
    elif saat < 12:
        selamlama = "Günaydın"
        alt_emoji = "☀️"
    elif saat < 17:
        selamlama = "İyi günler"
        alt_emoji = "🌤️"
    elif saat < 21:
        selamlama = "İyi akşamlar"
        alt_emoji = "🌆"
    else:
        selamlama = "İyi geceler"
        alt_emoji = "🌙"

    if student:
        alt_mesaj = f"Hadi {student.ad} ile birlikte harika şeyler öğrenelim bugün!"
    else:
        alt_mesaj = "Sana nasıl yardımcı olabilirim? Hadi konuşalım!"

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #94A3B8 0%, #7c3aed 50%, #a855f7 100%);
        border-radius: 16px;
        padding: 18px 24px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 4px 20px rgba(124,58,237,0.25);
    ">
        <div style="flex-shrink:0;">{avatar_html}</div>
        <div>
            <div style="color:white;font-size:1.15rem;font-weight:700;">
                {alt_emoji} {selamlama}, {hitap}!
            </div>
            <div style="color:rgba(255,255,255,0.75);font-size:0.88rem;margin-top:4px;">
                Ben <strong>Smarti</strong>, senin dijital eğitim arkadaşın! {alt_mesaj}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Mini sohbet kutusu ---
    mini_key = "smarti_top_chat"
    hist_key = _smarti_ss("history")
    if hist_key not in st.session_state:
        st.session_state[hist_key] = []

    with st.expander("Smarti'ye yaz, hemen cevaplayayım!", expanded=False):
        try:
            from views.ai_destek import _get_client, SYSTEM_PROMPT, _build_data_context
        except ImportError:
            st.warning("AI Destek modülü yüklenemedi.")
            return

        client = _get_client()
        if not client:
            st.info("OpenAI API anahtarı tanımlanmamış.")
            return

        # Son mesajlar
        for msg in st.session_state[hist_key][-6:]:
            role_label = "Sen" if msg["role"] == "user" else "Smarti"
            bg = "#1A2035" if msg["role"] == "user" else "#ede9fe"
            icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f"""
            <div style="background:{bg};border-radius:10px;padding:8px 14px;margin-bottom:6px;font-size:0.85rem;">
                <strong>{icon} {role_label}:</strong> {msg['content'][:500]}
            </div>""", unsafe_allow_html=True)

        user_input = st.text_input("Mesajını yaz...", key=mini_key,
                                    placeholder="Örnek: Bugün hangi derslerim var?")
        if user_input:
            st.session_state[hist_key].append({"role": "user", "content": user_input})
            data_ctx = _build_data_context(auth_user)
            system_msg = {"role": "system",
                          "content": SYSTEM_PROMPT + "\n\n" + data_ctx}
            messages = [system_msg] + st.session_state[hist_key][-10:]
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.8,
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                answer = f"Bir hata oluştu: {e}"
            st.session_state[hist_key].append({"role": "assistant", "content": answer})
            st.rerun()


def _render_smarti_floating_avatar():
    """Sag alt kosede yuzen Smarti avatar butonu."""
    mascot_path = _SMARTI_MASCOT
    if os.path.exists(mascot_path):
        with open(mascot_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        avatar_img = f'<img src="data:image/png;base64,{img_b64}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" />'
    else:
        avatar_img = '<span style="font-size:2rem;">🤖</span>'

    st.markdown(f"""
    <style>
    .smarti-fab {{
        position: fixed;
        bottom: 28px;
        right: 28px;
        z-index: 99999;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 6px 24px rgba(124, 58, 237, 0.45);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: smarti-fab-bounce 3s ease-in-out infinite;
    }}
    .smarti-fab:hover {{
        transform: scale(1.12);
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.65);
    }}
    @keyframes smarti-fab-bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-6px); }}
    }}
    .smarti-fab-label {{
        position: fixed;
        bottom: 96px;
        right: 20px;
        z-index: 99999;
        background: #94A3B8;
        color: white;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 0.78rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
        white-space: nowrap;
    }}
    .smarti-fab:hover + .smarti-fab-label {{
        opacity: 1;
    }}
    </style>
    <div class="smarti-fab">{avatar_img}</div>
    <div class="smarti-fab-label">Smarti ile konuşun!</div>
    """, unsafe_allow_html=True)


def _inject_smarti_css():
    st.markdown("""<style>
    .smarti-header {
        background: linear-gradient(135deg, #94A3B8 0%, #7c3aed 100%);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.3);
        position: relative; overflow: hidden;
    }
    .smarti-header::before {
        content: ''; position: absolute; top: -30px; right: -30px;
        width: 120px; height: 120px;
        background: rgba(255,255,255,0.05); border-radius: 50%;
    }
    .smarti-header h2 { color: white; margin: 0; font-size: 1.5rem; font-weight: 800; }
    .smarti-header p { color: rgba(255,255,255,0.7); margin: 4px 0 0 0; font-size: 0.85rem; }
    .smarti-voice-banner {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 12px; padding: 16px 24px; margin-bottom: 16px;
        text-align: center; color: white; font-weight: 600; font-size: 1rem;
        animation: smarti-pulse 2s ease-in-out infinite;
    }
    @keyframes smarti-pulse {
        0%, 100% { box-shadow: 0 0 10px rgba(124, 58, 237, 0.3); }
        50% { box-shadow: 0 0 25px rgba(124, 58, 237, 0.6); }
    }
    .smarti-voice-banner .subtitle {
        font-weight: 400; font-size: 0.8rem; opacity: 0.85; margin-top: 4px;
    }
    </style>""", unsafe_allow_html=True)


def _smarti_process_input(client, user_input: str, system_msg: dict,
                          mascot_avatar, tts_fn):
    """Kullanici girdisini isle: gecmise ekle, AI yaniti al, TTS olustur."""
    from views.ai_destek import _get_ai_response

    hist_key = _smarti_ss("history")
    cache_key = _smarti_ss("audio_cache")

    st.session_state[hist_key].append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    messages = [system_msg] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state[hist_key]
    ]

    with st.chat_message("assistant", avatar=mascot_avatar):
        with st.spinner("Smarti düşünüyor..."):
            response_text = _get_ai_response(client, messages)
        st.markdown(response_text)

        if response_text and tts_fn:
            with st.spinner("Ses oluşturuluyor..."):
                audio = tts_fn(client, response_text)
                if audio:
                    msg_idx = len(st.session_state[hist_key])
                    st.session_state[cache_key][f"audio_{msg_idx}"] = audio
                    st.audio(audio, format="audio/mp3", autoplay=True)

    st.session_state[hist_key].append({"role": "assistant", "content": response_text})


def _render_smarti_tab(auth_user: dict, role: str = "Veli"):
    """Tam ozellikli Smarti AI asistan sekmesi (sesli + yazili)."""
    _inject_smarti_css()

    # --- Import AI fonksiyonlari ---
    try:
        from views.ai_destek import (
            _get_client, SYSTEM_PROMPT, _build_data_context,
            _text_to_speech, _speech_to_text, _audio_hash,
        )
    except ImportError:
        st.warning("AI Destek modülü yüklenemedi.")
        return

    client = _get_client()
    if not client:
        st.error("OpenAI API anahtarı bulunamadı. Lütfen .env dosyasında OPENAI_API_KEY tanımlayın.")
        return

    # --- Mascot ---
    mascot_avatar = _SMARTI_MASCOT if os.path.exists(_SMARTI_MASCOT) else "🤖"

    # --- Header ---
    hdr_cols = st.columns([1, 4])
    with hdr_cols[0]:
        if os.path.exists(_SMARTI_MASCOT):
            st.image(_SMARTI_MASCOT, width=140)
    with hdr_cols[1]:
        st.markdown(
            '<div class="smarti-header">'
            '<h2>Smarti</h2>'
            '<p>SmartCampus AI sesli asistanı — size nasıl yardımcı olabilirim?</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    # --- Session state ---
    hist_key = _smarti_ss("history")
    cache_key = _smarti_ss("audio_cache")
    voice_key = _smarti_ss("voice_mode")
    hash_key = _smarti_ss("last_audio_hash")
    greet_key = _smarti_ss("greeted")

    if hist_key not in st.session_state:
        st.session_state[hist_key] = []
    if cache_key not in st.session_state:
        st.session_state[cache_key] = {}
    if voice_key not in st.session_state:
        st.session_state[voice_key] = False
    if hash_key not in st.session_state:
        st.session_state[hash_key] = None
    if greet_key not in st.session_state:
        st.session_state[greet_key] = False

    # --- Kontrol butonlari ---
    ctrl1, ctrl2, ctrl3 = st.columns([1.5, 1.5, 3])
    with ctrl1:
        if st.session_state[voice_key]:
            if st.button("Sesli Konuşmayı Durdur", key="panel_smarti_stop_voice",
                         type="secondary", use_container_width=True):
                st.session_state[voice_key] = False
                st.session_state[hash_key] = None
                st.rerun()
        else:
            if st.button("Sesli Konuşmayı Başlat", key="panel_smarti_start_voice",
                         type="primary", use_container_width=True):
                st.session_state[voice_key] = True
                st.session_state[hash_key] = None
                st.rerun()
    with ctrl2:
        if st.button("Sohbeti Temizle", key="panel_smarti_clear",
                      use_container_width=True):
            st.session_state[hist_key] = []
            st.session_state[cache_key] = {}
            st.session_state[hash_key] = None
            st.session_state[greet_key] = False
            st.rerun()

    st.markdown("---")

    # --- Hitap ve system prompt ---
    kullanici_adi = auth_user.get("name", "Kullanıcı")
    kullanici_rol = role
    kullanici_cinsiyet = auth_user.get("cinsiyet", "")
    ilk_isim = kullanici_adi.split()[0] if kullanici_adi.split() else kullanici_adi

    if kullanici_rol == "Öğrenci":
        hitap = ilk_isim
    elif kullanici_cinsiyet.lower() in ("kadin", "k", "bayan", "kadın"):
        hitap = f"{ilk_isim} Hanım"
    elif kullanici_cinsiyet.lower() in ("erkek", "e", "bay"):
        hitap = f"{ilk_isim} Bey"
    else:
        hitap = kullanici_adi

    try:
        from views.kim_organizational import load_profile
        profile = load_profile()
        kurum_adi = profile.get("name", "SmartCampus AI")
    except Exception:
        kurum_adi = "SmartCampus AI"

    veri_paneli = _build_data_context(auth_user)

    system_msg = {
        "role": "system",
        "content": SYSTEM_PROMPT.format(
            kurum_adi=kurum_adi,
            kullanici_adi=hitap,
            kullanici_rol=kullanici_rol,
            veri_paneli=veri_paneli,
        ),
    }

    # --- Karşılama mesajı ---
    greeting_text = (
        f"Merhaba {hitap}! Ben Smarti, senin dijital eğitim arkadaşın! "
        f"Bugün sana nasıl yardımcı olabilirim?"
    )
    if not st.session_state[hist_key]:
        with st.chat_message("assistant", avatar=mascot_avatar):
            st.markdown(
                f"Merhaba **{hitap}**! Ben **Smarti**, senin dijital eğitim arkadaşın! "
                f"Bugün sana nasıl yardımcı olabilirim?\n\n"
                f"Yazarak veya **sesli konuşmak** için yukarıdaki butona basarak sohbet edebilirsin."
            )
        if not st.session_state[greet_key]:
            st.session_state[greet_key] = True
            with st.spinner("Smarti hazırlanıyor..."):
                greeting_audio = _text_to_speech(client, greeting_text)
            if greeting_audio:
                st.session_state[cache_key]["greeting"] = greeting_audio
                st.audio(greeting_audio, format="audio/mp3", autoplay=True)
        elif "greeting" in st.session_state[cache_key]:
            st.audio(st.session_state[cache_key]["greeting"], format="audio/mp3")

    # --- Gecmis mesajlari goster ---
    for i, msg in enumerate(st.session_state[hist_key]):
        avatar = mascot_avatar if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and not st.session_state[voice_key]:
                audio_k = f"audio_{i}"
                if audio_k in st.session_state[cache_key]:
                    st.audio(st.session_state[cache_key][audio_k], format="audio/mp3")
                else:
                    if st.button("Seslendir", key=f"panel_tts_{i}"):
                        with st.spinner("Ses oluşturuluyor..."):
                            audio = _text_to_speech(client, msg["content"])
                            if audio:
                                st.session_state[cache_key][audio_k] = audio
                                st.audio(audio, format="audio/mp3", autoplay=True)

    # --- SESLİ KONUŞMA MODU ---
    if st.session_state[voice_key]:
        st.markdown(
            '<div class="smarti-voice-banner">'
            'Sesli Konuşma Aktif — Konuşmaya başlayın'
            '<div class="subtitle">Konuşmanız bitince otomatik algılanacak ve Smarti yanıtlayacak</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        try:
            from audio_recorder_streamlit import audio_recorder
            audio_bytes = audio_recorder(
                text="",
                recording_color="#ef4444",
                neutral_color="#7c3aed",
                icon_size="3x",
                pause_threshold=2.5,
                auto_start=True,
                key="panel_smarti_voice_rec",
            )
            if audio_bytes:
                current_hash = _audio_hash(audio_bytes)
                if current_hash != st.session_state[hash_key]:
                    st.session_state[hash_key] = current_hash
                    with st.spinner("Ses tanınıyor..."):
                        voice_text = _speech_to_text(client, audio_bytes)
                    if voice_text:
                        _smarti_process_input(client, voice_text, system_msg,
                                              mascot_avatar, _text_to_speech)
                        st.rerun()
                    else:
                        st.info("Ses anlaşılamadı, lütfen tekrar deneyin.")
        except ImportError:
            st.warning("Sesli konuşma için 'audio_recorder_streamlit' paketi gereklidir.")
            st.code("pip install audio-recorder-streamlit", language="bash")

    # --- YAZI MODU ---
    else:
        text_input = st.chat_input("Smarti'ye sorunuzu yazın...",
                                    key="panel_smarti_chat_input")
        if text_input:
            _smarti_process_input(client, text_input, system_msg,
                                  mascot_avatar, _text_to_speech)


# ===================== MEMNUNİYET ANKETİ SEKMESİ =====================

def _get_veli_anket_store() -> VeliAnketDataStore:
    base = os.path.join(get_tenant_dir(), "veli_anket")
    s = VeliAnketDataStore(base)
    s.seed_defaults()
    return s


def _render_memnuniyet_anketi_tab(student: Student, auth_user: dict):
    """Veli memnuniyet anketi - sadece Veli rolu icin."""
    styled_section("Veli Memnuniyet Anketi", "#8b5cf6")

    store = _get_veli_anket_store()
    aktif = store.get_aktif_donem()

    if not aktif:
        styled_info_banner(
            "Su anda aktif bir anket donemi bulunmamaktadir. "
            "Anket donemi acildiginda burada bilgilendirileceksiniz.",
            "warning",
        )
        return

    styled_info_banner(
        f"<b>{aktif.donem_adi}</b> &nbsp;|&nbsp; "
        f"Son tarih: <b>{aktif.bitis}</b>",
        "info",
    )

    # Anonim token olustur (oturum bazli)
    token_key = "veli_anket_token"
    if token_key not in st.session_state:
        st.session_state[token_key] = uuid.uuid4().hex[:12]
    token = st.session_state[token_key]

    # Daha once katildi mi?
    mevcut = store.katilimci_cevaplari(aktif.id, token)
    if mevcut:
        styled_info_banner(
            f"Bu anket donemi için zaten katilim sagladiniz "
            f"({len(mevcut)} cevap). Katiliminiz için tesekkur ederiz!",
            "success",
        )
        return

    # Ogrenci sinif bilgisi otomatik
    sinif = str(student.sinif)

    st.markdown(
        '<div style="background:#f8fafc;border:1px solid #bae6fd;border-radius:10px;'
        'padding:14px 18px;margin:10px 0;font-size:0.9rem;color:#0369a1;">'
        f'<b>Öğrenci:</b> {student.tam_ad} &nbsp;|&nbsp; '
        f'<b>Sınıf:</b> {sinif}. sinif'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Kategorilere gore sorulari goster
    sorular_by_kat = store.get_sorular_by_kategori()
    cevaplar: dict[str, int] = {}

    for kat in ANKET_KATEGORILERI:
        kat_sorular = sorular_by_kat.get(kat, [])
        if not kat_sorular:
            continue

        ikon = KATEGORI_IKONLARI.get(kat, "")
        renk = KATEGORI_RENKLER.get(kat, "#2563eb")

        st.markdown(
            f'<div style="background:linear-gradient(135deg,{renk}15 0%,{renk}05 100%);'
            f'border-left:4px solid {renk};border-radius:0 12px 12px 0;'
            f'padding:14px 18px;margin:20px 0 10px 0">'
            f'<span style="font-size:1.3rem">{ikon}</span>'
            f'<span style="font-size:1.1rem;font-weight:700;color:{renk};margin-left:8px">{kat}</span>'
            f'<span style="font-size:0.8rem;color:#64748b;margin-left:8px">({len(kat_sorular)} soru)</span>'
            f'</div>', unsafe_allow_html=True,
        )

        for soru in kat_sorular:
            st.markdown(
                f'<div style="font-size:0.9rem;font-weight:500;color:#0f172a;margin:8px 0 4px 8px">'
                f'{soru.sira}. {soru.soru}</div>',
                unsafe_allow_html=True,
            )
            secim = st.radio(
                f"s_{soru.id}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {LIKERT_OLCEK[x]}",
                horizontal=True,
                key=f"vp_anket_q_{soru.id}",
                label_visibility="collapsed",
            )
            cevaplar[soru.id] = secim

    st.markdown("---")
    styled_section("Görüşleriniz (Opsiyonel)", "#64748b")
    genel_yorum = st.text_area(
        "Eklemek istediginiz goruslerinizi yazabilirsiniz:",
        key="vp_anket_genel_yorum",
        placeholder="Okul hakkindaki genel degerlendirmeniz, onerileriniz veya sikayetleriniz...",
        height=100,
    )

    st.markdown("")
    if st.button("Anketi Gonder", type="primary", use_container_width=True,
                  key="vp_anket_gonder_btn"):
        toplam = 0
        for soru_id, puan in cevaplar.items():
            soru_obj = store.get_by_id("sorular", soru_id)
            cevap = AnketCevap(
                donem_id=aktif.id,
                soru_id=soru_id,
                kategori=soru_obj.kategori if soru_obj else "",
                puan=puan,
                anonim_token=token,
                sinif=sinif,
            )
            store.upsert("cevaplar", cevap)
            toplam += 1

        if genel_yorum.strip():
            yorum = AnketYorum(
                donem_id=aktif.id,
                yorum=genel_yorum.strip(),
                anonim_token=token,
                sinif=sinif,
            )
            store.upsert("yorumlar", yorum)

        st.success(
            f"Anketiniz basariyla kaydedildi! ({toplam} cevap) "
            "Katiliminiz için tesekkur ederiz."
        )
        st.balloons()
        st.rerun()


# ===================== GÜNLÜK RAPOR PDF ÜRETİCİ =====================

def _generate_gunluk_rapor_pdf(store: AkademikDataStore, student: Student,
                                od: OlcmeDataStore, rapor_tarihi: date) -> bytes:
    """Belirtilen tarih icin gunluk akademik rapor PDF'i uretir."""
    from utils.report_utils import ReportPDFGenerator, get_institution_info

    tarih_str = rapor_tarihi.strftime("%Y-%m-%d")
    tarih_goster = rapor_tarihi.strftime("%d.%m.%Y")
    gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe",
               "Cuma", "Cumartesi", "Pazar"][rapor_tarihi.weekday()]
    akademik_yil = _get_akademik_yil()

    # Veri toplama
    attendance = store.get_attendance(student_id=student.id)
    bugun_devamsiz = [a for a in attendance if a.tarih == tarih_str] if attendance else []
    odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
    bugun_odev = [o for o in odevler if o.son_teslim_tarihi == tarih_str] if odevler else []
    kyt_cevaplar = store.get_kyt_cevaplar(
        student_id=student.id, tarih=tarih_str,
        sinif=student.sinif, sube=student.sube)
    kyt_sorular = store.get_kyt_sorular(
        sinif=student.sinif, sube=student.sube, tarih=tarih_str)
    kyt_dogru = sum(1 for c in kyt_cevaplar if c.dogru_mu)
    tum_ki = store.get_kazanim_isleme(sinif=student.sinif, sube=student.sube)
    bugun_ki = [k for k in tum_ki if k.tarih == tarih_str and k.durum in ("islendi", "kismen")]
    grades = store.get_grades(student_id=student.id)
    results = od.get_results(student_id=student.id)
    teslimler = store.get_odev_teslimleri(student_id=student.id)
    teslim_ids = {t.odev_id for t in teslimler if t.durum == "teslim_edildi"}
    teslim_orani = round((len(teslim_ids) / len(odevler)) * 100, 1) if odevler else 100
    not_ort = _get_not_ortalamasi(grades) if grades else 0
    sinav_ort = round(sum(r.score for r in results if r.score) / len(
        [r for r in results if r.score]), 1) if results and any(
        r.score for r in results) else 0
    kyt_analiz = store.get_kyt_ogrenci_analizi(
        student_id=student.id, akademik_yil=akademik_yil)
    kyt_basari = kyt_analiz["basari_yuzde"] if kyt_analiz["toplam"] > 0 else 0
    devamsizlik_skoru = max(0, 100 - (len(attendance) * 2 if attendance else 0))
    menuler_pdf = _load_veli_json(YEMEK_MENU_DOSYA)
    bugun_menu_pdf = next((m for m in menuler_pdf if m.get("tarih") == tarih_str), None)
    _sinif_int_pdf = student.sinif if isinstance(student.sinif, int) else int(student.sinif or 0)
    _online_kayit_pdf = store.get_online_ders_kayitlari(akademik_yil=akademik_yil)
    _online_link_pdf = [
        l for l in store.get_online_ders_links(akademik_yil=akademik_yil)
        if l.sinif == _sinif_int_pdf and (not l.sube or l.sube == student.sube) and l.aktif
    ]
    bugun_online_pdf = [
        k for k in _online_kayit_pdf
        if k.sinif == _sinif_int_pdf and (not k.sube or k.sube == student.sube)
        and k.planlanan_tarih == tarih_str
    ]

    # PDF olustur
    info = get_institution_info()
    pdf = ReportPDFGenerator(
        title=f"Gunluk Akademik Rapor - {tarih_goster}",
        subtitle=f"{student.tam_ad} | {student.sinif}/{student.sube} | No: {student.numara} | {gun_adi}",
        orientation="portrait",
    )
    pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))

    # 1. Genel Performans
    pdf.add_section("Genel Performans Ozeti", color="#94A3B8")
    pdf.add_metrics([
        ("Not Ort.", f"{not_ort}", "#2563eb"),
        ("Sinav Ort.", f"{sinav_ort}", "#7c3aed"),
        ("KYT Basari", f"%{kyt_basari}", "#22c55e"),
        ("Odev Teslim", f"%{teslim_orani}", "#f59e0b"),
        ("Devam Skoru", f"{devamsizlik_skoru}/100", "#0891b2"),
    ])

    # 2. Online Dersler
    pdf.add_section("Online Dersler", color="#6366f1")
    if bugun_online_pdf:
        _p_ad_map_pdf = {
            "google_classroom": "Google Classroom", "zoom": "Zoom",
            "teams": "Teams", "meet": "Google Meet", "eba": "EBA",
        }
        _dur_map_pdf = {
            "planli": "Planlandı", "yapiliyor": "Yapılıyor",
            "yapildi": "Tamamlandı", "yapilmadi": "Yapılmadı",
        }
        online_data_pdf = []
        for ok in sorted(bugun_online_pdf, key=lambda x: x.planlanan_saat):
            link_str = ""
            if ok.link_id:
                eslesme = next((l for l in _online_link_pdf if l.id == ok.link_id), None)
                if eslesme and eslesme.link:
                    link_str = eslesme.link[:40] + ("..." if len(eslesme.link) > 40 else "")
            online_data_pdf.append({
                "Saat": ok.planlanan_saat or "–",
                "Ders": ok.ders,
                "Platform": _p_ad_map_pdf.get(ok.platform, ok.platform),
                "Durum": _dur_map_pdf.get(ok.durum, ok.durum),
                "Süre": f"{ok.sure_dk} dk",
            })
        pdf.add_table(pd.DataFrame(online_data_pdf), header_color="#6366f1")
    else:
        pdf.add_text("Bu tarih icin online ders planlanmamistir.")

    # 3. Yemek Menusu
    pdf.add_section("Yemek Menusu", color="#f59e0b")
    if bugun_menu_pdf:
        yemekler_pdf = bugun_menu_pdf.get("yemekler", [])
        ogun_pdf = bugun_menu_pdf.get("ogun", "Ogle Yemegi")
        kalori_pdf = bugun_menu_pdf.get("kalori", "")
        menu_notlar_pdf = bugun_menu_pdf.get("notlar", "")
        menu_satir = f"{ogun_pdf}: " + " | ".join(yemekler_pdf) if yemekler_pdf else ogun_pdf
        if kalori_pdf:
            menu_satir += f"  ({kalori_pdf} kcal)"
        pdf.add_text(menu_satir)
        if menu_notlar_pdf:
            pdf.add_text(f"Not: {menu_notlar_pdf}")
    else:
        pdf.add_text("Bu tarih icin yemek menusu girilmemistir.")

    # 4. Devamsizlik
    pdf.add_section("Devamsizlik Durumu", color="#ef4444")
    if bugun_devamsiz:
        dev_text = ", ".join(f"{a.ders} ({a.turu})" for a in bugun_devamsiz)
        pdf.add_text(f"Devamsizlik VAR: {dev_text}")
    else:
        pdf.add_text("Bu tarihte devamsizlik bulunmamaktadir.")

    # 5. Odevler
    pdf.add_section("Odevler", color="#f59e0b")
    if bugun_odev:
        teslim_map = {t.odev_id: t for t in teslimler}
        odev_data = []
        for o in bugun_odev:
            t = teslim_map.get(o.id)
            durum = "Teslim Edildi" if (t and t.durum == "teslim_edildi") else "Bekliyor"
            odev_data.append({"Odev": o.baslik, "Ders": o.ders, "Durum": durum})
        pdf.add_table(pd.DataFrame(odev_data), header_color="#f59e0b")
    else:
        pdf.add_text("Bu tarihte son teslim tarihli odev bulunmamaktadir.")

    # 6. KYT
    pdf.add_section("KYT Sonuclari", color="#7c3aed")
    if kyt_sorular:
        kyt_basari_today = round(
            (kyt_dogru / len(kyt_cevaplar)) * 100) if kyt_cevaplar else 0
        pdf.add_text(
            f"Cevaplanmis: {len(kyt_cevaplar)}/{len(kyt_sorular)} | "
            f"Dogru: {kyt_dogru} | Yanlis: {len(kyt_cevaplar) - kyt_dogru} | "
            f"Basari: %{kyt_basari_today}")
    else:
        pdf.add_text("Bu tarihte KYT sorusu bulunmamaktadir.")

    # 7. Islenen kazanimlar
    pdf.add_section("Islenen Kazanimlar", color="#059669")
    if bugun_ki:
        kaz_data = []
        for k in bugun_ki:
            kaz_data.append({
                "Ders": k.ders,
                "Kod": k.kazanim_kodu,
                "Kazanim": k.kazanim_metni[:60] + ("..." if len(k.kazanim_metni) > 60 else ""),
                "Durum": "Islendi" if k.durum == "islendi" else "Kismen",
            })
        pdf.add_table(pd.DataFrame(kaz_data), header_color="#059669")
    else:
        pdf.add_text("Bu tarihte islenen kazanim kaydi bulunmamaktadir.")

    # 8. Not ozeti
    pdf.add_section("Ders Bazli Not Ozeti", color="#2563eb")
    if grades:
        ders_ort: dict[str, dict] = {}
        for g in grades:
            d = ders_ort.setdefault(g.ders, {"puanlar": [], "son_not": 0, "son_tarih": ""})
            d["puanlar"].append(g.puan)
            if g.tarih >= d["son_tarih"]:
                d["son_tarih"] = g.tarih
                d["son_not"] = g.puan
        not_data = []
        for ders, info_d in sorted(ders_ort.items()):
            valid = [p for p in info_d["puanlar"] if p and p > 0]
            ort = round(sum(valid) / len(valid), 1) if valid else 0
            not_data.append({
                "Ders": ders,
                "Not Sayisi": len(valid),
                "Ortalama": ort,
                "Son Not": f"{info_d['son_not']:.0f}",
            })
        pdf.add_table(pd.DataFrame(not_data), header_color="#2563eb")
    else:
        pdf.add_text("Henuz not kaydi bulunmamaktadir.")

    return pdf.generate()


# ===================== RAPORLAR SEKMESİ =====================

def _render_raporlar_tab(store: AkademikDataStore, student: Student,
                          od: OlcmeDataStore):
    """Raporlar sekmesi - tarih filtreli gunluk rapor PDF indirme."""
    styled_section("Gunluk Rapor Arsivi", "#94A3B8")

    styled_info_banner(
        "Tarih secerek o gune ait gunluk akademik raporu PDF olarak indirebilirsiniz.",
        "info")

    col1, col2 = st.columns([1, 2])
    with col1:
        secilen_tarih = st.date_input(
            "Rapor Tarihi",
            value=date.today(),
            max_value=date.today(),
            key="vp_rapor_tarih",
        )

    tarih_goster = secilen_tarih.strftime("%d.%m.%Y")
    gun_adi = ["Pazartesi", "Sali", "Carsamba", "Persembe",
               "Cuma", "Cumartesi", "Pazar"][secilen_tarih.weekday()]

    st.markdown(f"""
    <div style="border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;
                margin:12px 0;background:#ffffff;">
        <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.5rem;">📄</span>
            <div>
                <div style="font-weight:700;color:#475569;font-size:1rem;">
                    {tarih_goster} - {gun_adi}</div>
                <div style="color:#64748b;font-size:0.85rem;">
                    {student.tam_ad} | {student.sinif}/{student.sube}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    if st.button("PDF Rapor Olustur", key="vp_rapor_pdf_btn",
                  type="primary"):
        with st.spinner("PDF rapor olusturuluyor..."):
            try:
                pdf_bytes = _generate_gunluk_rapor_pdf(
                    store, student, od, secilen_tarih)
                dosya_adi = (
                    f"Gunluk_Rapor_{student.tam_ad.replace(' ', '_')}_"
                    f"{secilen_tarih.strftime('%Y%m%d')}.pdf"
                )
                st.session_state["_vp_rapor_pdf"] = pdf_bytes
                st.session_state["_vp_rapor_dosya"] = dosya_adi
                st.success("PDF rapor basariyla olusturuldu!")
            except Exception as e:
                st.error(f"PDF olusturulurken hata: {e}")

    # PDF indirme butonu (olusturulduysa)
    if st.session_state.get("_vp_rapor_pdf"):
        st.download_button(
            label="PDF Indir",
            data=st.session_state["_vp_rapor_pdf"],
            file_name=st.session_state.get("_vp_rapor_dosya", "rapor.pdf"),
            mime="application/pdf",
            key="vp_rapor_download",
        )

    # Hizli tarih secimi
    st.markdown("")
    styled_section("Hizli Erisim", "#64748b")
    cols = st.columns(5)
    bugun = date.today()
    for i, col in enumerate(cols):
        gun = bugun - timedelta(days=i)
        gun_str = gun.strftime("%d.%m")
        gun_adi_k = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"][gun.weekday()]
        with col:
            if st.button(f"{gun_str}\n{gun_adi_k}", key=f"vp_hizli_{i}"):
                st.session_state["vp_rapor_tarih"] = gun
                # Temizle eski PDF
                st.session_state.pop("_vp_rapor_pdf", None)
                st.rerun()


# ===================== REVİR KAYITLARI SEKMESİ =====================

def _get_saglik_store() -> SaglikDataStore:
    base = os.path.join(get_tenant_dir(), "saglik")
    return SaglikDataStore(base)


def _get_rehberlik_store() -> RehberlikDataStore:
    base = os.path.join(get_tenant_dir(), "rehberlik")
    return RehberlikDataStore(base)


def _render_revir_kayitlari_tab(student: Student):
    """Revir ziyaret kayitlari - veli gorunumu."""
    styled_section("Revir Kayitlari", "#ef4444")
    sstore = _get_saglik_store()
    ziyaretler = sstore.find_by_field("revir_ziyaretleri", "ogrenci_id", student.id)
    if not ziyaretler:
        styled_info_banner("Revir ziyaret kaydi bulunmuyor.", "info")
        return
    ziyaretler.sort(key=lambda z: getattr(z, "basvuru_tarihi", "") or "", reverse=True)
    styled_info_banner(
        f"Toplam <b>{len(ziyaretler)}</b> revir ziyareti kaydi bulunmaktadir.", "info")
    for z in ziyaretler:
        tarih = getattr(z, "basvuru_tarihi", "") or ""
        saat = getattr(z, "basvuru_saati", "") or ""
        sikayet = getattr(z, "sikayet", "-") or "-"
        kategori = getattr(z, "sikayet_kategorisi", "-") or "-"
        mudahale = getattr(z, "mudahale", "") or "Belirtilmedi"
        uygulayan = getattr(z, "uygulayan", "") or "-"
        sonuc = getattr(z, "sonuc", "-") or "-"
        veli_bilgi = getattr(z, "veli_bilgilendirildi", False)
        takip = getattr(z, "takip_gerekiyor", False)
        takip_notu = getattr(z, "takip_notu", "") or ""
        sonuc_renk = {"Kapandi": "#16a34a", "Mudahale Edildi": "#2563eb",
                       "Veli Bilgilendirildi": "#f59e0b",
                       "Basvuruldu": "#7c3aed"}.get(sonuc, "#64748b")
        veli_ikon = "✅" if veli_bilgi else "❌"
        takip_ikon = "⚠️" if takip else "✅"
        st.markdown(f"""
        <div style="border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;
                    margin-bottom:12px;background:#fff;">
            <div style="display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:10px;">
                <div>
                    <span style="font-weight:700;color:#475569;font-size:0.95rem;">
                        📅 {tarih}</span>
                    <span style="color:#64748b;font-size:0.85rem;margin-left:8px;">
                        {saat}</span>
                </div>
                <span style="background:{sonuc_renk};color:white;padding:3px 12px;
                      border-radius:12px;font-size:0.75rem;font-weight:600;">{sonuc}</span>
            </div>
            <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
                <tr>
                    <td style="padding:4px 0;color:#64748b;width:140px;font-weight:600;">
                        Sikayet</td>
                    <td style="padding:4px 0;color:#475569;">{sikayet}</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;color:#64748b;font-weight:600;">Kategori</td>
                    <td style="padding:4px 0;color:#475569;">{kategori}</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;color:#64748b;font-weight:600;">Mudahale</td>
                    <td style="padding:4px 0;color:#475569;">{mudahale}</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;color:#64748b;font-weight:600;">Uygulayan</td>
                    <td style="padding:4px 0;color:#475569;">{uygulayan}</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;color:#64748b;font-weight:600;">
                        Veli Bilgilendirildi</td>
                    <td style="padding:4px 0;color:#475569;">{veli_ikon}
                        {"Evet" if veli_bilgi else "Hayir"}</td>
                </tr>
                <tr>
                    <td style="padding:4px 0;color:#64748b;font-weight:600;">Takip</td>
                    <td style="padding:4px 0;color:#475569;">{takip_ikon}
                        {"Gerekiyor" if takip else "Gerekmiyor"}
                        {f" - {takip_notu}" if takip_notu else ""}</td>
                </tr>
            </table>
        </div>""", unsafe_allow_html=True)


# ===================== REHBERLİK VAKA KAYITLARI SEKMESİ =====================

def _render_rehberlik_vaka_tab(student: Student):
    """Rehberlik vaka kayitlari ve gorusme gecmisi - veli gorunumu."""
    styled_section("Rehberlik Vaka Kayitlari", "#8b5cf6")
    rstore = _get_rehberlik_store()
    vakalar = rstore.find_by_field("vakalar", "ogrenci_id", student.id)
    gorusmeler = rstore.find_by_field("gorusmeler", "ogrenci_id", student.id)
    if not vakalar and not gorusmeler:
        styled_info_banner("Rehberlik kaydi bulunmuyor.", "info")
        return
    # Vakalar
    if vakalar:
        styled_info_banner(
            f"<b>{len(vakalar)}</b> aktif/gecmis vaka kaydi bulunmaktadir.", "info")
        for v in vakalar:
            durum = getattr(v, "durum", "ACIK") or "ACIK"
            oncelik = getattr(v, "oncelik", "DUSUK") or "DUSUK"
            risk = getattr(v, "risk_seviyesi", "DUSUK") or "DUSUK"
            durum_renk = {"ACIK": "#ef4444", "TAKIPTE": "#f59e0b",
                          "BEKLEMEDE": "#64748b", "KAPANDI": "#16a34a"}.get(durum, "#64748b")
            oncelik_renk = {"ACIL": "#dc2626", "YUKSEK": "#f59e0b",
                            "NORMAL": "#2563eb", "DUSUK": "#16a34a"}.get(oncelik, "#64748b")
            konular = ", ".join(getattr(v, "ilgili_konular", []) or []) or "-"
            rehber = getattr(v, "atanan_rehber", "") or "-"
            vaka_basligi = getattr(v, "vaka_basligi", "-") or "-"
            baslangic = getattr(v, "baslangic_tarihi", "-") or "-"
            gorusme_sayisi = getattr(v, "gorusme_sayisi", 0) or 0
            vaka_aciklama = getattr(v, "vaka_aciklamasi", "") or ""
            st.markdown(f"""
            <div style="border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;
                        margin-bottom:12px;background:#fff;
                        border-left:4px solid {durum_renk};">
                <div style="display:flex;justify-content:space-between;align-items:center;
                            margin-bottom:10px;">
                    <span style="font-weight:700;color:#475569;font-size:0.95rem;">
                        {vaka_basligi}</span>
                    <div>
                        <span style="background:{durum_renk};color:white;padding:2px 10px;
                              border-radius:10px;font-size:0.72rem;font-weight:600;
                              margin-right:4px;">{durum}</span>
                        <span style="background:{oncelik_renk};color:white;padding:2px 10px;
                              border-radius:10px;font-size:0.72rem;font-weight:600;">
                            {oncelik}</span>
                    </div>
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
                    <tr>
                        <td style="padding:4px 0;color:#64748b;width:140px;font-weight:600;">
                            Baslangic</td>
                        <td style="padding:4px 0;color:#475569;">{baslangic}</td>
                    </tr>
                    <tr>
                        <td style="padding:4px 0;color:#64748b;font-weight:600;">
                            Rehber</td>
                        <td style="padding:4px 0;color:#475569;">{rehber}</td>
                    </tr>
                    <tr>
                        <td style="padding:4px 0;color:#64748b;font-weight:600;">
                            Konular</td>
                        <td style="padding:4px 0;color:#475569;">{konular}</td>
                    </tr>
                    <tr>
                        <td style="padding:4px 0;color:#64748b;font-weight:600;">
                            Risk Seviyesi</td>
                        <td style="padding:4px 0;color:#475569;">{risk}</td>
                    </tr>
                    <tr>
                        <td style="padding:4px 0;color:#64748b;font-weight:600;">
                            Gorusme Sayisi</td>
                        <td style="padding:4px 0;color:#475569;">{gorusme_sayisi}</td>
                    </tr>
                </table>
                {"<div style='margin-top:8px;padding:8px 12px;background:#ffffff;border-radius:8px;font-size:0.82rem;color:#475569;'>" + vaka_aciklama + "</div>" if vaka_aciklama else ""}
            </div>""", unsafe_allow_html=True)
    # Gorusmeler
    if gorusmeler:
        st.markdown("")
        styled_section("Gorusme Gecmisi", "#6d28d9")
        gorusmeler.sort(key=lambda g: getattr(g, "tarih", "") or "", reverse=True)
        for g in gorusmeler:
            gizlilik = getattr(g, "gizlilik_seviyesi", "NORMAL") or "NORMAL"
            if gizlilik == "COK_GIZLI":
                g_tarih = getattr(g, "tarih", "") or ""
                st.markdown(f"""
                <div style="border:1px solid #fecaca;border-radius:12px;padding:14px 20px;
                            margin-bottom:10px;background:#fef2f2;">
                    <span style="color:#991b1b;font-size:0.85rem;">
                        🔒 {g_tarih} - Bu gorusme gizlilik kapsamindadir.</span>
                </div>""", unsafe_allow_html=True)
                continue
            tur = getattr(g, "gorusme_turu", "-") or "-"
            konu = getattr(g, "gorusme_konusu", "-") or "-"
            ozet = getattr(g, "gorusme_ozeti", "") or ""
            sonraki = getattr(g, "sonraki_adim", "") or ""
            g_tarih = getattr(g, "tarih", "") or ""
            g_saat_bas = getattr(g, "saat_baslangic", "") or ""
            g_saat_bit = getattr(g, "saat_bitis", "") or ""
            g_gorusen = getattr(g, "gorusen", "-") or "-"
            st.markdown(f"""
            <div style="border:1px solid #e2e8f0;border-radius:12px;padding:14px 20px;
                        margin-bottom:10px;background:#fff;">
                <div style="display:flex;justify-content:space-between;align-items:center;
                            margin-bottom:8px;">
                    <div>
                        <span style="font-weight:700;color:#475569;font-size:0.9rem;">
                            📋 {g_tarih}</span>
                        <span style="color:#64748b;font-size:0.82rem;margin-left:6px;">
                            {g_saat_bas}-{g_saat_bit}</span>
                    </div>
                    <span style="background:#7c3aed;color:white;padding:2px 10px;
                          border-radius:10px;font-size:0.72rem;font-weight:600;">{tur}</span>
                </div>
                <div style="font-size:0.82rem;color:#64748b;margin-bottom:4px;">
                    <b>Konu:</b> {konu} | <b>Gorusen:</b> {g_gorusen}</div>
                {"<div style='padding:8px 12px;background:#ffffff;border-radius:8px;font-size:0.82rem;color:#475569;margin-bottom:6px;'>" + ozet + "</div>" if ozet else ""}
                {"<div style='font-size:0.8rem;color:#2563eb;'><b>Sonraki Adim:</b> " + sonraki + "</div>" if sonraki else ""}
            </div>""", unsafe_allow_html=True)


# ===================== REHBERLİK TEST SONUÇLARI SEKMESİ =====================

def _render_rehberlik_test_tab(student: Student):
    """Rehberlik test sonuclari - veli gorunumu."""
    styled_section("Rehberlik Test Sonuçları", "#0891b2")
    rstore = _get_rehberlik_store()
    oturumlar = rstore.find_by_field("test_oturumlari", "ogrenci_id", student.id)
    if not oturumlar:
        styled_info_banner("Henüz tamamlanmış test bulunmuyor.", "info")
        return
    testler = rstore.load_list("testler")
    test_map = {t["id"]: t for t in testler}
    tamamlanan = [o for o in oturumlar if getattr(o, "durum", "") == "TAMAMLANDI"]
    devam_eden = [o for o in oturumlar if getattr(o, "durum", "") != "TAMAMLANDI"]

    styled_stat_row([
        ("Tamamlanan", str(len(tamamlanan)), "#10b981", "✅"),
        ("Devam Eden", str(len(devam_eden)), "#f59e0b" if devam_eden else "#6b7280", "⏳"),
        ("Toplam Test", str(len(oturumlar)), "#0891b2", "📋"),
    ])
    # Test cevaplarini yukle (olcek bazli skor icin)
    tum_cevaplar = rstore.load_list("test_cevaplari")
    tum_sorular = rstore.load_list("test_sorulari")
    for o in tamamlanan:
        o_test_id = getattr(o, "test_id", "") or ""
        o_bitis = getattr(o, "bitis_zamani", "") or ""
        o_sure = getattr(o, "toplam_sure", 0) or 0
        test_info = test_map.get(o_test_id, {})
        test_adi = test_info.get("test_adi", "Bilinmeyen Test")
        test_kat = test_info.get("test_kategorisi", "-")
        olcekler = test_info.get("olcekler", [])
        tarih = o_bitis[:10] if o_bitis else "-"
        sure = o_sure
        # Olcek bazli skor hesapla
        oturum_cevaplar = [c for c in tum_cevaplar
                           if c.get("oturum_id") == o.id]
        oturum_sorular = [s for s in tum_sorular
                          if s.get("test_id") == o_test_id]
        olcek_skorlari = {}
        if oturum_cevaplar and oturum_sorular:
            soru_map = {s["id"]: s for s in oturum_sorular}
            for c in oturum_cevaplar:
                soru = soru_map.get(c.get("soru_id", ""), {})
                olcek = soru.get("olcek", "Genel")
                puan = c.get("puan", 0)
                olcek_skorlari.setdefault(olcek, []).append(puan)
        kat_ikon = {"Kaygi": "😟", "Kisilik": "🧠", "Ilgi": "🎯",
                    "Yetenek": "⭐", "Dikkat": "🔍", "Depresyon": "💙",
                    "Sosyometri": "👥", "Zeka": "🧩"}.get(
            test_kat.replace("ı", "i").replace("â", "a"), "📝")
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#f0fdfa,#ccfbf1);border:1px solid #99f6e4;'
            f'border-radius:12px;padding:16px 20px;margin-bottom:12px;'
            f'box-shadow:0 2px 6px rgba(8,145,178,0.08);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
            f'<div><span style="font-size:1.3rem;">{kat_ikon}</span>'
            f'<span style="font-weight:700;color:#475569;font-size:0.95rem;margin-left:8px;">{test_adi}</span></div>'
            f'<span style="background:linear-gradient(135deg,#0891b2,#3b82f6);color:#fff;padding:4px 14px;'
            f'border-radius:20px;font-size:0.72rem;font-weight:600;">{test_kat}</span></div>'
            f'<div style="font-size:0.82rem;color:#64748b;">'
            f'📅 {tarih} · ⏱️ {sure} dk · 📝 {len(oturum_cevaplar)} soru</div></div>',
            unsafe_allow_html=True)
        # Olcek bazli sonuclar (varsa)
        if olcek_skorlari:
            cols_data = []
            for olcek_adi in olcekler:
                puanlar = olcek_skorlari.get(olcek_adi, [])
                if puanlar:
                    ort = round(sum(puanlar) / len(puanlar), 1)
                    cols_data.append((olcek_adi, ort))
            if cols_data:
                cols = st.columns(min(len(cols_data), 4))
                for idx, (olcek_adi, ort) in enumerate(cols_data):
                    renk = "#16a34a" if ort >= 3.5 else (
                        "#f59e0b" if ort >= 2.5 else "#ef4444")
                    _pct = min(100, int(ort / 5 * 100))
                    with cols[idx % len(cols)]:
                        st.markdown(
                            f'<div style="text-align:center;padding:12px;background:linear-gradient(135deg,#111827,#1A2035);'
                            f'border:1px solid #e2e8f0;border-radius:12px;margin-bottom:8px;">'
                            f'<div style="font-size:0.75rem;color:#64748b;margin-bottom:6px;font-weight:600;">{olcek_adi}</div>'
                            f'<div style="font-size:1.4rem;font-weight:800;color:{renk};">{ort}</div>'
                            f'<div style="background:#e5e7eb;border-radius:10px;height:6px;margin-top:6px;overflow:hidden;">'
                            f'<div style="background:{renk};height:100%;width:{_pct}%;border-radius:10px;"></div>'
                            f'</div></div>', unsafe_allow_html=True)
        elif olcekler:
            st.markdown(f"""
            <div style="padding:8px 12px;background:#f0f9ff;border-radius:8px;
                        font-size:0.82rem;color:#0369a1;margin-bottom:8px;">
                Olcek alanları: {', '.join(olcekler)}</div>""", unsafe_allow_html=True)
    # Devam eden testler
    if devam_eden:
        st.markdown("")
        styled_info_banner(
            f"<b>{len(devam_eden)}</b> test devam etmektedir.", "warning")


# ===================== VELİ PANELİ =====================

def render_veli_panel():
    """Veli giris ekrani — premium tasarim + 18/9 sekmeli panel + Smarti AI."""
    _inject_panel_tab_css()
    _inject_veli_premium_css()  # Premium veli paneli CSS

    auth_user = AuthManager.get_current_user()
    store = get_akademik_store()
    od = OlcmeDataStore()

    role = auth_user.get("role", "")
    is_preview = role in ("Yonetici", "Öğretmen", "Çalışan", "SuperAdmin")

    if is_preview:
        # Yonetici/Ogretmen onizleme
        all_students = store.get_students()

        styled_info_banner(
            "📋 Önizleme Modu — Velinin gördüğü panelleri kademe kademe inceliyorsunuz. "
            "5 farklı ekran tipi var: Anaokulu / 1-2.sınıf (sade) / 3-4.sınıf (tam) / Ortaokul (LGS) / Lise (YKS).",
            "info",
        )

        # 5 FARKLI EKRAN TIPI — her birinin ozel sinif ornegi var
        _kademe_map = {
            "🎨 Anaokulu (5 yaş)":      ("ana5", "Anasınıfı",  "23 sekme · gelişim odaklı"),
            "📚 İlkokul 1-2. Sınıf":    ("1",    "1.sınıf",     "19 sekme · sade akademik (not yok)"),
            "📗 İlkokul 3-4. Sınıf":    ("3",    "3.sınıf",     "9 ana grup · tam panel"),
            "🔬 Ortaokul (5-8)":        ("6",    "6.sınıf",     "9 ana grup · LGS Hazırlık Modu"),
            "🎓 Lise (9-12)":           ("10",   "10.sınıf",    "9 ana grup · YKS + Üniversite Tercih"),
        }
        _prev_kademe = st.radio(
            "📚 Hangi kademe ekranını görüntülemek istiyorsunuz?",
            list(_kademe_map.keys()),
            horizontal=True,
            key="veli_preview_kademe",
        )
        _prev_sinif, _prev_kademe_label, _prev_aciklama = _kademe_map[_prev_kademe]

        # Aciklama satiri
        st.markdown(
            f'<div style="background:rgba(99,102,241,.08);border-left:3px solid #6366f1;'
            f'border-radius:0 8px 8px 0;padding:8px 14px;margin:6px 0 12px;'
            f'font-size:.84rem;color:#475569">'
            f'<b style="color:#a5b4fc">{_prev_kademe}</b> · '
            f'<span style="color:#0f172a">{_prev_aciklama}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Once gercek o kademede ogrenci var mi bul
        sinif_filtreli = [s for s in all_students if str(s.sinif) == _prev_sinif]

        if not sinif_filtreli:
            # Demo öğrenci oluştur — bu kademede gercek kayit yok
            st.caption(f"ℹ️ Bu kademede gerçek öğrenci kaydı yok. Demo öğrenciyle gösteriliyor.")
            _demo_stu = Student(
                id=f"demo_preview_{_prev_sinif}",
                ad="Demo", soyad="Öğrenci",
                sinif=_prev_sinif, sube="A", numara="001",
                tc_no="00000000000", cinsiyet="Erkek",
                veli_adi="Demo Veli", veli_telefon="05001234567",
            )
            student = _demo_stu
        else:
            # Bu kademede gercek ogrenciler var — secim sun
            stu_map = {s.id: s for s in sinif_filtreli}
            selected_id = st.selectbox(
                f"📋 {_prev_kademe} kademesinden öğrenci seç ({len(sinif_filtreli)} öğrenci)",
                [s.id for s in sinif_filtreli],
                format_func=lambda x: f"{stu_map[x].tam_ad} — {stu_map[x].sinif}/{stu_map[x].sube} (No: {stu_map[x].numara})",
                key=f"preview_student_select_{_prev_sinif}",
            )
            student = stu_map[selected_id]
    else:
        # Kademe-bagimsiz: velinin TUM cocuklarini cek
        children = _find_student_for_veli(store, auth_user)

        if not children:
            styled_info_banner(
                "Kayıtlı çocuğunuz bulunamadı. Lütfen yöneticiyle iletişime geçin "
                "(veli adı, telefon veya e-mail eşleşmesi gerekiyor).",
                "warning",
            )
            return

        # Cok cocuk varsa: KART TABANLI secim (veli isimlere tiklayarak girer)
        if len(children) > 1:
            # Onceden secilen cocuk varsa onu kullan, yoksa secim ekranini goster
            _selected_child_id = st.session_state.get("veli_secili_cocuk_id", "")
            student = next((c for c in children if c.id == _selected_child_id), None)

            if student is None:
                # ── KART TABANLI COCUK SECIM EKRANI ──
                styled_header(
                    "👨‍👩‍👧‍👦 Çocuğunuzu Seçin",
                    f"{auth_user.get('name', 'Sayın Veli')}, sisteme {len(children)} öğrenciniz kayıtlı. "
                    "Görüntülemek istediğiniz çocuğa tıklayın.",
                )

                # Kademe ikonlari
                _kademe_icon_map = {
                    "okul_oncesi": ("🎨", "Anaokulu", "#0d9488"),
                    "ilkokul":     ("📚", "İlkokul",  "#2563eb"),
                    "ortaokul":    ("🔬", "Ortaokul", "#6366f1"),
                    "lise":        ("🎓", "Lise",     "#1e40af"),
                }

                def _kademe_of(stu):
                    try:
                        from utils.shared_data import normalize_sinif
                        ns = normalize_sinif(str(stu.sinif))
                    except Exception:
                        ns = str(stu.sinif)
                    if ns in {"ana4", "ana5", "anahaz"}:
                        return "okul_oncesi"
                    if ns in {"1", "2", "3", "4"}:
                        return "ilkokul"
                    if ns in {"5", "6", "7", "8", "haz"}:
                        return "ortaokul"
                    if ns in {"9", "10", "11", "12"}:
                        return "lise"
                    return "ilkokul"

                # Insan dostu sinif etiketi (ana5 -> "Anaokulu 5 yaş")
                def _sinif_label(stu):
                    try:
                        from utils.shared_data import normalize_sinif
                        ns = normalize_sinif(str(stu.sinif))
                    except Exception:
                        ns = str(stu.sinif)
                    _ana_map = {
                        "ana4": "Anaokulu 4 yaş",
                        "ana5": "Anaokulu 5 yaş",
                        "anahaz": "Anaokulu Hazırlık",
                    }
                    if ns in _ana_map:
                        return _ana_map[ns]
                    if ns == "haz":
                        return "Hazırlık sınıfı"
                    if ns in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}:
                        return f"{ns}. sınıf"
                    return f"{ns}. sınıf"

                # 2 sutun grid — LIGHT TEMA
                _ncols = min(4, len(children))
                _cols = st.columns(_ncols)
                for _ci, _child in enumerate(children):
                    _kk = _kademe_of(_child)
                    _icon, _label, _clr = _kademe_icon_map.get(_kk, ("🎓", "Öğrenci", "#2563eb"))
                    _initials = ((_child.ad[0] if _child.ad else "?") + (_child.soyad[0] if _child.soyad else "?")).upper()
                    _sinif_text = _sinif_label(_child)
                    with _cols[_ci % _ncols]:
                        st.markdown(
                            f'<div style="background:#ffffff;'
                            f'border:1px solid #e2e8f0;border-radius:20px;padding:22px 16px;'
                            f'text-align:center;margin-bottom:10px;'
                            f'box-shadow:0 1px 3px rgba(15,23,42,.04),'
                            f'0 8px 24px rgba(99,102,241,.08),'
                            f'0 16px 48px {_clr}10;'
                            f'transition:transform .25s cubic-bezier(.4,0,.2,1);'
                            f'cursor:pointer;position:relative;overflow:hidden">'
                            # Üst gradient şerit
                            f'<div style="position:absolute;top:0;left:0;right:0;height:5px;'
                            f'background:linear-gradient(90deg,{_clr} 0%,{_clr}aa 100%)"></div>'
                            # Avatar
                            f'<div style="width:74px;height:74px;border-radius:50%;'
                            f'background:linear-gradient(135deg,{_clr} 0%,{_clr}cc 100%);'
                            f'color:#fff;font-weight:900;font-size:1.7rem;letter-spacing:-1px;'
                            f'line-height:74px;margin:8px auto 14px auto;'
                            f'border:3px solid #ffffff;'
                            f'box-shadow:0 8px 20px {_clr}40,'
                            f'inset 0 -3px 6px rgba(0,0,0,.15),'
                            f'inset 0 3px 6px rgba(255,255,255,.25)">'
                            f'{_initials}</div>'
                            # Ad soyad
                            f'<div style="font-size:1.1rem;font-weight:800;color:#0f172a;'
                            f'line-height:1.25;margin-bottom:6px;letter-spacing:-.3px">'
                            f'{_child.ad} {_child.soyad}</div>'
                            # Sinif (insan dostu)
                            f'<div style="font-size:.85rem;color:#475569;font-weight:600;'
                            f'margin-bottom:3px">{_sinif_text}</div>'
                            # Sube + No (kucuk)
                            f'<div style="font-size:.72rem;color:#475569;font-weight:500;'
                            f'margin-bottom:10px">{_child.sube} şubesi · No: {_child.numara or "—"}</div>'
                            # Kademe rozeti
                            f'<div style="display:inline-block;background:{_clr}15;'
                            f'color:{_clr};border:1px solid {_clr}44;'
                            f'border-radius:20px;padding:5px 14px;font-size:.75rem;'
                            f'font-weight:700">{_icon} {_label}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"➜ {_child.ad}'i Görüntüle",
                            key=f"veli_cocuk_sec_{_child.id}",
                            type="primary",
                            use_container_width=True,
                        ):
                            st.session_state["veli_secili_cocuk_id"] = _child.id
                            st.rerun()

                # Tek-cocuk secimini sifirlama uyarisi
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                styled_info_banner(
                    "Çocuk değiştirmek için sayfanın üstündeki '🔄 Çocuk Değiştir' butonuna basabilirsiniz.",
                    "info",
                )
                return  # Cocuk secilmediyse panel acilmasin
        else:
            student = children[0]
            st.session_state["veli_secili_cocuk_id"] = student.id

        # Cok cocuklu velide: cocuk degistirme butonu
        if len(children) > 1:
            _hb1, _hb2 = st.columns([5, 1])
            with _hb2:
                if st.button("🔄 Çocuk Değiştir", key="veli_cocuk_degistir",
                              use_container_width=True):
                    st.session_state.pop("veli_secili_cocuk_id", None)
                    st.rerun()

    # ── KOMPAKT HERO (sadece avatar + selam + tarih) ──
    _render_veli_premium_hero(student, auth_user)
    # NOT: AI briefing + 360 snapshot + Quick actions + kadro kunye + tum widgetlar
    # artik panellerin ICINDE "Ozet" sekmesinde gosteriliyor.
    # Bu sayede sayfa girer girmez sekmeler hemen gozukur, dagilim olmaz.

    # ── YENİ MESAJ UYARI SİSTEMİ — sayfa açılışında otomatik bildirim ──
    _render_yeni_mesaj_uyari(store, student, auth_user)

    # --- Anasınıfı tespiti ---
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR
    _norm_sinif = normalize_sinif(str(student.sinif))
    _is_anaokulu = _norm_sinif in KADEME_SINIFLAR.get("Anaokulu", [])

    # ── BUGÜNÜN AKADEMİK RAPORU — açılışta otomatik göster ──
    _render_acilis_gunluk_rapor(store, od, student, auth_user, _is_anaokulu)

    if _is_anaokulu:
        # ============ ANASINIFI VELİ PANELİ — SADELEŞTIRILMIŞ ============
        _render_veli_anaokulu_panel(store, od, student, auth_user, is_preview)
    else:
        # ============ NORMAL VELİ PANELİ ============
        _render_veli_normal_panel(store, od, student, auth_user, is_preview)

    # Floating Smarti avatar (sag alt kose)
    _render_smarti_floating_avatar()


def _render_yeni_mesaj_uyari(store, student, auth_user):
    """Yeni mesaj uyari sistemi.

    1) Okunmamis mesaj sayisini kontrol eder
    2) Eger varsa: pulse-animasyonlu kirmizi banner gosterir
    3) Onceki render'a gore YENI mesaj geldiyse: st.toast bildirim
    4) Session state ile son sayim takip edilir
    """
    try:
        username = auth_user.get("username", "")
        unread = store.get_okunmamis_mesaj_sayisi(receiver_id=username) or 0
    except Exception:
        unread = 0

    if unread <= 0:
        # Okunmamis yoksa eski sayimi sifirla
        st.session_state[f"_son_unread_{student.id}"] = 0
        return

    # ── YENI MESAJ TESPITI (toast icin) ──
    son_key = f"_son_unread_{student.id}"
    son_sayim = int(st.session_state.get(son_key, 0))
    yeni_geldi = unread > son_sayim
    st.session_state[son_key] = unread

    # ── TOAST: yeni mesaj gelirse ──
    if yeni_geldi:
        try:
            yeni_count = unread - son_sayim
            if son_sayim == 0:
                st.toast(f"💬 {unread} okunmamış mesajınız var", icon="📬")
            else:
                st.toast(f"💬 {yeni_count} yeni mesaj geldi! (Toplam: {unread})", icon="🔔")
        except Exception:
            pass

    # ── PULSE-ANIMASYONLU KIRMIZI UYARI BANNER ──
    # Son gonderen ogretmen bilgisi
    son_gonderen = ""
    son_konu = ""
    try:
        mesajlar = store.get_messages(receiver_id=username) or []
        okunmamis_msj = [m for m in mesajlar if not getattr(m, "okundu", True)]
        if okunmamis_msj:
            okunmamis_msj.sort(key=lambda m: getattr(m, "tarih", ""), reverse=True)
            son = okunmamis_msj[0]
            son_gonderen = getattr(son, "gonderen_adi", "") or "Öğretmen"
            son_konu = (getattr(son, "konu", "") or getattr(son, "icerik", "") or "")[:80]
    except Exception:
        pass

    detay_html = ""
    if son_gonderen:
        detay_html = (
            f'<div style="font-size:.78rem;color:rgba(255,255,255,.92);margin-top:4px">'
            f'📨 Son gönderen: <b>{son_gonderen}</b>'
            + (f' · "{son_konu}{"..." if len(son_konu) >= 80 else ""}"' if son_konu else '')
            + '</div>'
        )

    st.markdown(
        f"""
        <style>
        @keyframes mesajPulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(239,68,68,0.7), 0 12px 32px rgba(239,68,68,0.35); }}
            50%      {{ box-shadow: 0 0 0 12px rgba(239,68,68,0), 0 12px 32px rgba(239,68,68,0.35); }}
        }}
        @keyframes mesajShake {{
            0%, 100% {{ transform: rotate(0deg); }}
            10%, 30%, 50%, 70%, 90% {{ transform: rotate(-12deg); }}
            20%, 40%, 60%, 80% {{ transform: rotate(12deg); }}
        }}
        .veli-mesaj-uyari {{
            background: linear-gradient(135deg,#dc2626 0%,#ef4444 50%,#f97316 100%);
            border-radius: 16px;
            padding: 14px 22px;
            margin: 10px 0 14px 0;
            border: 2px solid rgba(254,202,202,.4);
            animation: mesajPulse 1.8s ease-in-out infinite;
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
        }}
        .veli-mesaj-icon {{
            font-size: 2rem;
            display: inline-block;
            animation: mesajShake 1.5s ease-in-out infinite;
            transform-origin: top center;
        }}
        .veli-mesaj-badge {{
            background: #fff;
            color: #dc2626;
            font-weight: 900;
            font-size: 1.4rem;
            padding: 6px 16px;
            border-radius: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,.2);
            min-width: 50px;
            text-align: center;
        }}
        </style>
        <div class="veli-mesaj-uyari">
            <span class="veli-mesaj-icon">🔔</span>
            <div style="flex:1;min-width:200px">
                <div style="font-size:1.05rem;font-weight:900;color:#fff;letter-spacing:-.3px">
                    Yeni Mesajınız Var!
                </div>
                <div style="font-size:.82rem;color:rgba(255,255,255,.95);margin-top:2px">
                    💬 Mesajlar sekmesinden okuyabilirsiniz
                </div>
                {detay_html}
            </div>
            <div class="veli-mesaj-badge">{unread}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_acilis_gunluk_rapor(store, od, student, auth_user, is_anaokulu: bool):
    """Veli paneli acilisinda BUGUNUN gunluk akademik raporunu otomatik gosterir.

    Banner-style kart: bugun ogrencinin ders/devamsizlik/odev/oncekiler ozeti.
    Anaokulu icin: gunluk bulten ozeti (duygu, beslenme, etkinlik).
    Ilkokul+ icin: gunluk rapor ozeti (devam, katilim, odev, ogretmen notu).
    Hic veri yoksa nazik bilgi mesaji.
    """
    from datetime import date as _date
    bugun = _date.today().strftime("%Y-%m-%d")
    gun_adi = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"][_date.today().weekday()]
    bugun_g = _date.today().strftime("%d.%m.%Y")

    # ── ANAOKULU: GunlukBulten ──
    if is_anaokulu:
        try:
            bultenler = store.get_gunluk_bultenler(student_id=student.id, tarih=bugun) or []
        except Exception:
            bultenler = []

        if bultenler:
            blt = bultenler[0]
            duygu_ikon = {"cok_mutlu": "😄", "mutlu": "🙂", "normal": "😐",
                          "keyifsiz": "😕", "uzgun": "😢"}.get(getattr(blt, "duygu", ""), "✨")
            beslenme_lbl = {"hepsini_yedi": "Hepsini yedi 🍽️",
                            "bir_kismini": "Bir kısmını yedi 🥄",
                            "yemedi": "Yemedi ❌"}.get(getattr(blt, "beslenme", ""), "—")
            etk_count = len(getattr(blt, "etkinlikler", []) or [])
            ogretmen_notu = (getattr(blt, "ogretmen_notu", "") or "").strip()
            bugun_basari = (getattr(blt, "bugun_basari", "") or "").strip()

            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0b1437 0%,#4338ca 35%,#7c3aed 70%,#ec4899 100%);'
                f'border-radius:18px;padding:18px 24px;margin:12px 0 16px 0;'
                f'box-shadow:0 12px 32px rgba(67,56,202,.3);'
                f'border:1px solid rgba(236,72,153,.3);">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'flex-wrap:wrap;gap:10px;margin-bottom:10px">'
                f'<div style="display:flex;align-items:center;gap:12px">'
                f'<span style="font-size:1.8rem">📋</span>'
                f'<div><div style="font-size:1.1rem;font-weight:900;color:#fff">Bugünkü Günlük Bülten</div>'
                f'<div style="font-size:.78rem;color:rgba(254,243,199,.9)">{gun_adi} · {bugun_g}</div></div>'
                f'</div>'
                f'<span style="background:rgba(255,255,255,.18);color:#fff;padding:4px 12px;'
                f'border-radius:14px;font-size:.72rem;font-weight:800;backdrop-filter:blur(6px)">✅ ÖĞRETMEN GİRDİ</span>'
                f'</div>'
                f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));'
                f'gap:10px;margin-top:8px">'
                f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
                f'<div style="font-size:1.6rem">{duygu_ikon}</div>'
                f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">DUYGU</div></div>'
                f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
                f'<div style="font-size:.85rem;color:#fff;font-weight:800">{beslenme_lbl}</div>'
                f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">BESLENME</div></div>'
                f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
                f'<div style="font-size:1.2rem;color:#fff;font-weight:900">{etk_count}</div>'
                f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">ETKİNLİK</div></div>'
                f'</div>'
                + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #fbbf24;'
                   f'border-radius:8px;padding:10px 14px;margin-top:10px;font-size:.82rem;color:#fff">'
                   f'🌟 <b>Bugün başardığı:</b> {bugun_basari}</div>' if bugun_basari else '')
                + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #22d3ee;'
                   f'border-radius:8px;padding:10px 14px;margin-top:8px;font-size:.82rem;color:#fff">'
                   f'👩‍🏫 <b>Öğretmen notu:</b> {ogretmen_notu[:240]}</div>' if ogretmen_notu else '')
                + '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#fef3c7,#fde68a);'
                f'border:1px solid #fcd34d;border-radius:14px;padding:14px 20px;margin:12px 0 16px 0;'
                f'display:flex;align-items:center;gap:14px">'
                f'<span style="font-size:1.8rem">📋</span>'
                f'<div><div style="font-size:.95rem;font-weight:800;color:#92400e">'
                f'Bugün için günlük bülten henüz girilmedi</div>'
                f'<div style="font-size:.78rem;color:#a16207;margin-top:2px">'
                f'{gun_adi} · {bugun_g} — Öğretmeniniz gün içinde bülteni dolduracak.</div></div></div>',
                unsafe_allow_html=True,
            )
        return

    # ── ILKOKUL+ (1-12): IlkokulGunlukRapor ──
    try:
        raporlar = store.get_ilkokul_gunluk_raporlar(student_id=student.id, tarih=bugun) or []
    except Exception:
        raporlar = []

    if raporlar:
        r = raporlar[0]
        devam_lbl = {"tam": "Tam ✅", "gec_kaldi": "Geç kaldı ⏰",
                     "erken_cikti": "Erken çıktı 🚪", "izinli": "İzinli 📝"}.get(
            getattr(r, "devam", ""), "—")
        katilim_lbl = {"cok_iyi": "Çok İyi", "iyi": "İyi",
                       "orta": "Orta", "dusuk": "Düşük"}.get(getattr(r, "katilim", ""), "—")
        odev_lbl = "Var 📚" if getattr(r, "odev_durumu", "") == "verildi" else "Yok"
        ders_count = len(getattr(r, "islenen_dersler", []) or [])
        one_cikan = (getattr(r, "one_cikan_konu", "") or "").strip()
        ogretmen_notu = (getattr(r, "ogretmen_notu", "") or "").strip()
        bugun_basari = (getattr(r, "bugun_basari", "") or "").strip()
        bugun_ogrendigi = (getattr(r, "bugun_ogrendigi", "") or "").strip()

        st.markdown(
            f'<div style="background:linear-gradient(135deg,#0b1437 0%,#1e40af 35%,#0891b2 70%,#10b981 100%);'
            f'border-radius:18px;padding:18px 24px;margin:12px 0 16px 0;'
            f'box-shadow:0 12px 32px rgba(8,145,178,.3);'
            f'border:1px solid rgba(16,185,129,.3);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'flex-wrap:wrap;gap:10px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:center;gap:12px">'
            f'<span style="font-size:1.8rem">📋</span>'
            f'<div><div style="font-size:1.1rem;font-weight:900;color:#fff">Bugünkü Akademik Rapor</div>'
            f'<div style="font-size:.78rem;color:rgba(186,230,253,.95)">{gun_adi} · {bugun_g}</div></div>'
            f'</div>'
            f'<span style="background:rgba(255,255,255,.18);color:#fff;padding:4px 12px;'
            f'border-radius:14px;font-size:.72rem;font-weight:800;backdrop-filter:blur(6px)">✅ ÖĞRETMEN GİRDİ</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));'
            f'gap:10px;margin-top:8px">'
            f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:.88rem;color:#fff;font-weight:800">{devam_lbl}</div>'
            f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">DEVAM</div></div>'
            f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:.88rem;color:#fff;font-weight:800">{katilim_lbl}</div>'
            f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">KATILIM</div></div>'
            f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:1.2rem;color:#fff;font-weight:900">{ders_count}</div>'
            f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">DERS</div></div>'
            f'<div style="background:rgba(255,255,255,.12);border-radius:10px;padding:10px;text-align:center">'
            f'<div style="font-size:.88rem;color:#fff;font-weight:800">{odev_lbl}</div>'
            f'<div style="font-size:.7rem;color:rgba(255,255,255,.85);font-weight:700;margin-top:2px">ÖDEV</div></div>'
            f'</div>'
            + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #22d3ee;'
               f'border-radius:8px;padding:10px 14px;margin-top:10px;font-size:.82rem;color:#fff">'
               f'📖 <b>Öne çıkan konu:</b> {one_cikan}</div>' if one_cikan else '')
            + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #34d399;'
               f'border-radius:8px;padding:10px 14px;margin-top:8px;font-size:.82rem;color:#fff">'
               f'💡 <b>Bugün öğrendiği:</b> {bugun_ogrendigi}</div>' if bugun_ogrendigi else '')
            + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #fbbf24;'
               f'border-radius:8px;padding:10px 14px;margin-top:8px;font-size:.82rem;color:#fff">'
               f'🌟 <b>Bugün başardığı:</b> {bugun_basari}</div>' if bugun_basari else '')
            + (f'<div style="background:rgba(255,255,255,.1);border-left:3px solid #fb7185;'
               f'border-radius:8px;padding:10px 14px;margin-top:8px;font-size:.82rem;color:#fff">'
               f'👩‍🏫 <b>Öğretmen notu:</b> {ogretmen_notu[:240]}</div>' if ogretmen_notu else '')
            + '</div>',
            unsafe_allow_html=True,
        )
    else:
        # Yumusak bilgi banner
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#fef3c7,#fde68a);'
            f'border:1px solid #fcd34d;border-radius:14px;padding:14px 20px;margin:12px 0 16px 0;'
            f'display:flex;align-items:center;gap:14px">'
            f'<span style="font-size:1.8rem">📋</span>'
            f'<div><div style="font-size:.95rem;font-weight:800;color:#92400e">'
            f'Bugün için günlük rapor henüz girilmedi</div>'
            f'<div style="font-size:.78rem;color:#a16207;margin-top:2px">'
            f'{gun_adi} · {bugun_g} — Öğretmen rapor girince burada otomatik görünecek.</div></div></div>',
            unsafe_allow_html=True,
        )


def _render_veli_anaokulu_panel(store, od, student, auth_user, is_preview):
    """Anasınıfı öğrencileri için sadeleştirilmiş veli paneli — modern toplu görünüm.

    Yapı: Sekmeler EN ÜSTTE (hero hemen altında).
    Tüm widget yığını + AI briefing + 360 + Quick Actions + kadro künye
    artık "📊 Özet" sekmesinin İÇİNDE gösteriliyor.
    """
    from datetime import date

    # ── ANAOKULU: 20 sekme (Mesajlar EN BASTA + 3 birlesik + Basari Duvari) ──
    try:
        _unread_ana = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))
    except Exception:
        _unread_ana = 0
    _msg_label_ana = (f"  💬 Mesajlar 🔴 {_unread_ana}  "
                      if _unread_ana > 0 else "  💬 Mesajlar  ")
    (t_mesaj,
     t_ozet_ana,
     t_bulten, t_basari_ana, t_vgb_ana,
     t_saglik_birlesik,
     t_belgeler_birlesik,
     t_etkinlik, t_program_ana, t_yemek,
     t_servis, t_randevu, t_anket_ana, t_dijital_ana,
     t_yabanci_dil_ana, t_gunbilgi_ana,
     t_brans_koyleri,
     t_karne_v, t_veli_egitim_v, t_smarti_ana,
     t_okul_oncesi_dijital_v) = st.tabs([
        _msg_label_ana,
        "  📊 Özet  ",
        "  📋 Günlük Bülten  ",
        "  🌟 Başarı Duvarı  ",
        "  📝 Veli Geri Bildirim  ",
        "  🏥 Sağlık & Rehberlik  ",
        "  📎 Belgeler  ",
        "  🎉 Etkinlik & Duyurular  ",
        "  📅 Ders Programı  ",
        "  🍽️ Yemek Menüsü  ",
        "  🚌 Servis Takibi  ",
        "  📅 Randevu  ",
        "  📊 Memnuniyet Anketi  ",
        "  📚 Dijital Kütüphane  ",
        "  🌐 Yabancı Dil  ",
        "  💡 Günün Bilgisi  ",
        "  🎨 Branş Köyleri  ",
        "  📋 Karne  ",
        "  🎓 Veli Eğitim  ",
        "  🤖 Smarti AI  ",
        "  🧒 Okul Öncesi Dijital  ",
    ])

    # ════════════════════════════════════════════════════════════════
    # 📊 ÖZET SEKMESİ — varsayılan açık (en başta)
    # AI Briefing + 360 Snapshot + Quick Actions + Kadro Künye + Widgets
    # ════════════════════════════════════════════════════════════════
    with t_ozet_ana:
        # 1) Akıllı kartlar (AI briefing + 360 + Quick actions)
        try:
            _render_veli_ai_briefing(store, student, auth_user, od)
        except Exception:
            pass
        try:
            _render_veli_360_snapshot(store, student, od)
        except Exception:
            pass
        try:
            _render_veli_quick_actions(store, student, auth_user)
        except Exception:
            pass

        # 2) Sınıf kadrosu künye (kompakt)
        try:
            _render_sinif_kadro_kunye(store, student)
        except Exception:
            pass

        # 3) Bugünkü özet stat row (anaokulu için)
        bugun = date.today().strftime("%Y-%m-%d")
        bugun_bulten = store.get_gunluk_bultenler(student_id=student.id, tarih=bugun)
        okunmamis = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))
        bulten_durum = "Girildi" if bugun_bulten else "Bekleniyor"
        bulten_renk = "#22c55e" if bugun_bulten else "#f59e0b"
        duygu_map_mini = {"cok_mutlu": "😄", "mutlu": "🙂", "normal": "😐", "keyifsiz": "😕", "uzgun": "😢"}
        duygu_icon = duygu_map_mini.get(bugun_bulten[0].duygu, "⏳") if bugun_bulten else "⏳"
        styled_stat_row([
            ("Günlük Bülten", bulten_durum, bulten_renk, "📋"),
            ("Duygu Durumu", duygu_icon, "#7c3aed", "😊"),
            ("Mesajlar", str(okunmamis) if okunmamis > 0 else "0", "#8b5cf6", "✉️"),
        ])

        # 4) Smarti karşılama
        st.markdown("")
        _render_smarti_top_greeting(auth_user, student)

        # 5) Premium widget yığını — hepsi expander içinde (sade görünüm için)
        with st.expander("✨ Detaylı İstatistikler & Widget'lar", expanded=False):
            try:
                from utils.ui_common import (mutluluk_indeksi, aylik_gelisim_karsilastirmasi,
                                              sinif_siralama_anonim, geri_sayim_sayaci,
                                              odev_hatirlatma_widget, etkinlik_foto_galerisi,
                                              hedef_belirleme_widget)
                import random as _rnd

                _m_skor = _rnd.uniform(6.5, 9.0)
                mutluluk_indeksi(_m_skor, {"akademik": _rnd.randint(6, 9), "sosyal": _rnd.randint(7, 9),
                                            "davranis": _rnd.randint(5, 9), "saglik": _rnd.randint(7, 10)})

                hedef_belirleme_widget([
                    {"hedef": "Sosyal Uyum", "mevcut": 7, "hedef_deger": 10, "birim": "puan"},
                    {"hedef": "El Becerisi", "mevcut": 8, "hedef_deger": 10, "birim": "puan"},
                ])

                _gc1, _gc2 = st.columns(2)
                with _gc1:
                    aylik_gelisim_karsilastirmasi(68.5, 72.3, "Genel")
                with _gc2:
                    sinif_siralama_anonim(_rnd.randint(3, 15), 30)

                geri_sayim_sayaci("2026-06-14", "Yaz Tatili", "🌞")

                odev_hatirlatma_widget([
                    {"ders": "Etkinlik", "baslik": "Boyama ödevi", "son_tarih": "2026-04-08", "teslim": False},
                    {"ders": "Müzik", "baslik": "Şarkı tekrarı", "son_tarih": "2026-04-10", "teslim": False},
                ])

                etkinlik_foto_galerisi()
            except Exception:
                pass

            try:
                from utils.ui_common import (cocugum_bugun_ne_ogrendi, haftalik_animasyonlu_ozet,
                                              acil_durum_butonu, uyku_enerji_takibi,
                                              kisisel_icerik_onerisi, veli_tesekkur_sistemi,
                                              goruntulu_gorusme_randevu)

                haftalik_animasyonlu_ozet()
                try:
                    from utils.ui_common import haftalik_video_widget
                    haftalik_video_widget()
                except Exception:
                    pass

                try:
                    _bugun_str = date.today().isoformat()
                    try:
                        _sinif_int = int(student.sinif) if str(student.sinif).isdigit() else 0
                    except Exception:
                        _sinif_int = 0
                    _bugun_kazanim = []
                    _ki_list = store.get_kazanim_isleme(
                        sinif=_sinif_int, sube=getattr(student, "sube", ""),
                        durum="islendi"
                    ) or []
                    for _ki in _ki_list:
                        _t = getattr(_ki, "tarih", "") or getattr(_ki, "updated_at", "")
                        if _t and str(_t)[:10] == _bugun_str:
                            _bugun_kazanim.append({
                                "ders": getattr(_ki, "ders", "-"),
                                "kazanim": getattr(_ki, "kazanim_metni", "") or getattr(_ki, "kazanim_kodu", "-"),
                            })
                    cocugum_bugun_ne_ogrendi(_bugun_kazanim)
                except Exception:
                    cocugum_bugun_ne_ogrendi()

                acil_durum_butonu()

                from utils.ui_common import (canli_ders_giris_bildirimi, ai_gunluk_motivasyon,
                                              veli_puan_sistemi, gelecek_hafta_plani,
                                              anlik_not_sinif_karsilastirma, ai_hafta_sonu_etkinlik_onerisi,
                                              karne_oncesi_panic_uyari, kardes_karsilastirma_paneli)

                _stu_ad = student.ad if hasattr(student, 'ad') else student.get('ad', '')
                canli_ders_giris_bildirimi()
                ai_gunluk_motivasyon(_stu_ad)
                gelecek_hafta_plani()
                anlik_not_sinif_karsilastirma(75, 72, 68, "Genel")
                veli_puan_sistemi()
                karne_oncesi_panic_uyari(48, 50, 21)
                with st.expander("🎉 Hafta Sonu Etkinlik Önerisi", expanded=False):
                    ai_hafta_sonu_etkinlik_onerisi()
            except Exception:
                pass

    with t_basari_ana:
        _render_aile_basari_duvari(store, student, auth_user)

    with t_bulten:
        _render_veli_gunluk_bulten(store, student, auth_user)
        try:
            from utils.ui_common import uyku_enerji_takibi as _uet_ana
            _uet_ana()
        except Exception:
            pass

    with t_vgb_ana:
        _render_veli_geri_bildirim_tab(store, student, auth_user, kademe="anaokulu")

    with t_mesaj:
        if is_preview:
            styled_info_banner("Önizleme modunda mesajlaşma devre dışı.", "info")
        else:
            _render_mesajlar_tab(store, student, auth_user)
        try:
            from utils.ui_common import veli_tesekkur_sistemi as _vts_ana
            _vts_ana()
        except Exception:
            pass

    # ── BIRLESIM 1: SAGLIK & REHBERLIK (3 alt sekme) ──
    with t_saglik_birlesik:
        _sa1, _sa2, _sa3 = st.tabs([
            "  🏥 Sağlık Kayıtları  ",
            "  🧑‍⚕️ Rehberlik  ",
            "  📋 Test Sonuçları  ",
        ])
        with _sa1:
            _render_revir_kayitlari_tab(student)
        with _sa2:
            _render_rehberlik_vaka_tab(student)
            try:
                from utils.ui_common import toplanti_ozeti_widget
                toplanti_ozeti_widget(
                    ozet="Genel değerlendirme olumlu. Velilerin okul etkinliklerine katılımı teşvik edildi.",
                    tarih="2026-03-28",
                    gundem=["Dönem sonu değerlendirmesi", "Yaz okulu bilgilendirmesi", "Sosyal etkinlik planları"],
                )
            except Exception:
                pass
        with _sa3:
            _render_rehberlik_test_tab(student)
            try:
                from utils.ui_common import ogretmen_degerlendirme_notu
                ogretmen_degerlendirme_notu(
                    yorum="Çocuğunuz sosyal becerilerinde olumlu gelişim göstermektedir. Grup çalışmalarına aktif katılım sağlıyor.",
                    ders="Genel Değerlendirme", donem="2025-2026 / 2. Dönem",
                )
            except Exception:
                pass

    # ── BIRLESIM 2: BELGELER (Gelen + Talep, 2 alt sekme) ──
    with t_belgeler_birlesik:
        _bl1, _bl2 = st.tabs([
            "  📎 Gelen Belgeler & Linkler  ",
            "  📄 Belge Talep  ",
        ])
        with _bl1:
            _render_veli_belgeler_tab(store, student)
        with _bl2:
            if is_preview:
                styled_info_banner("Önizleme modunda belge talebi oluşturulamaz.", "info")
            else:
                _render_belge_talep_tab(student, auth_user)

    with t_etkinlik:
        _render_etkinlik_duyuru_tab(student)
    with t_program_ana:
        _render_ders_programi_tab(store, student)
    with t_yemek:
        _render_yemek_menusu_tab()
    with t_servis:
        _render_servis_tab(student)
    with t_randevu:
        if is_preview:
            styled_info_banner("Önizleme modunda randevu talebi oluşturulamaz.", "info")
        else:
            _render_randevu_tab(store, student, auth_user)
        try:
            from utils.ui_common import goruntulu_gorusme_randevu as _ggr_ana
            _ggr_ana()
        except Exception:
            pass
    with t_anket_ana:
        if is_preview:
            styled_info_banner("Önizleme modunda anket doldurulamaz.", "info")
        else:
            _render_memnuniyet_anketi_tab(student, auth_user)
    with t_dijital_ana:
        _render_dk_embed()
        try:
            from utils.ui_common import kisisel_icerik_onerisi as _kio_ana
            _kio_ana(seviye="Anaokulu")
        except Exception:
            pass
    with t_yabanci_dil_ana:
        from views.yabanci_dil import render_veli_english_tab
        render_veli_english_tab(student.sinif, student.sube)
    with t_gunbilgi_ana:
        _render_gunun_bilgisi_tab()

    # ── BIRLESIM 3: BRANS KOYLERI (Matematik + Sanat + Bilisim + STEAM, 4 alt sekme) ──
    with t_brans_koyleri:
        _bk1, _bk2, _bk3, _bk4 = st.tabs([
            "  🏘️ Matematik Köyü  ",
            "  🎨 Sanat Sokağı  ",
            "  💻 Bilişim Vadisi  ",
            "  🔬 STEAM Merkezi  ",
        ])
        with _bk1:
            try:
                from views.matematik_dunyasi import render_matematik_dunyasi
                render_matematik_dunyasi()
            except Exception as e:
                st.error(f"Matematik Koyu yuklenemedi: {e}")
            with st.expander("Modul Raporu", expanded=False):
                try:
                    from views.modul_rapor_ui import render_veli_ogrenci_rapor
                    render_veli_ogrenci_rapor(
                        ogrenci_id=student.id, ogrenci_adi=student.tam_ad,
                        sinif=f"{student.sinif}/{student.sube}",
                        modul_filter="matematik", key_prefix="vp_mr_mat",
                    )
                except Exception as e:
                    st.error(f"Matematik raporu yuklenemedi: {e}")
        with _bk2:
            try:
                from views.sanat_sokagi import render_sanat_sokagi
                render_sanat_sokagi()
            except Exception as e:
                st.error(f"Sanat Sokagi yuklenemedi: {e}")
            with st.expander("Modul Raporu", expanded=False):
                try:
                    from views.modul_rapor_ui import render_veli_ogrenci_rapor as _veli_rapor_snt
                    _veli_rapor_snt(
                        ogrenci_id=student.id, ogrenci_adi=student.tam_ad,
                        sinif=f"{student.sinif}/{student.sube}",
                        modul_filter="sanat", key_prefix="vp_mr_snt",
                    )
                except Exception as e:
                    st.error(f"Sanat raporu yuklenemedi: {e}")
        with _bk3:
            try:
                from views.bilisim_vadisi import render_bilisim_vadisi
                render_bilisim_vadisi()
            except Exception as e:
                st.error(f"Bilisim Vadisi yuklenemedi: {e}")
            with st.expander("Modul Raporu", expanded=False):
                try:
                    from views.modul_rapor_ui import render_veli_ogrenci_rapor as _veli_rapor_bv
                    _veli_rapor_bv(
                        ogrenci_id=student.id, ogrenci_adi=student.tam_ad,
                        sinif=f"{student.sinif}/{student.sube}",
                        modul_filter="bilisim", key_prefix="vp_mr_bv",
                    )
                except Exception as e:
                    st.error(f"Bilisim raporu yuklenemedi: {e}")
        with _bk4:
            _render_stem_merkezi_tab(student, role="veli")
    # ── DİJİTAL KARNE ──
    with t_karne_v:
        try:
            styled_section("Dijital Karne", "#6366F1")
            from models.akademik_takip import get_akademik_store
            _at = get_akademik_store()
            _donem = st.selectbox("Dönem", ["1. Donem", "2. Donem"], key="veli_karne_donem")
            if st.button("📋 Karne Oluştur", key="veli_karne_btn", use_container_width=True):
                if hasattr(_at, 'karne_olustur'):
                    _karne = _at.karne_olustur(student.get("id", student.id if hasattr(student, "id") else ""), donem=_donem)
                    if _karne and _karne.get("ders_ortalamalari"):
                        st.markdown(f"**Genel Ortalama: {_karne.get('genel_ortalama', 0)}**")
                        for _ders, _ort in _karne.get("ders_ortalamalari", {}).items():
                            _renk = "#10B981" if _ort >= 70 else ("#F59E0B" if _ort >= 50 else "#EF4444")
                            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1E293B">'
                                        f'<span style="color:#0f172a">{_ders}</span>'
                                        f'<span style="color:{_renk};font-weight:700">{_ort}</span></div>',
                                        unsafe_allow_html=True)
                        _dev = _karne.get("devamsizlik", {})
                        st.markdown(f"**Devamsızlık:** {_dev.get('ozurlu',0)} özürlü, {_dev.get('ozursuz',0)} özürsüz")
                        if _karne.get("ai_ogretmen_yorumu"):
                            st.markdown(f"**Öğretmen Yorumu (AI):**\n{_karne['ai_ogretmen_yorumu']}")
                        # PDF indirme
                        try:
                            from utils.ui_common import karne_pdf_link
                            _pdf = karne_pdf_link(_karne)
                            if _pdf:
                                st.download_button("📄 Karne PDF İndir", _pdf, "karne.pdf", "application/pdf", key="veli_karne_pdf")
                        except Exception:
                            pass
                        # Sesli okuma
                        try:
                            from utils.ui_common import sesli_rapor_okuma
                            sesli_rapor_okuma(f"Genel ortalama {_karne.get('genel_ortalama', 0)}. {_karne.get('ai_ogretmen_yorumu', '')[:200]}", "veli_karne_tts")
                        except Exception:
                            pass
                    else:
                        styled_info_banner("Bu dönem için yeterli not kaydı bulunamadı.", "warning")
                else:
                    styled_info_banner("Karne oluşturma özelliği henüz aktif değil.", "info")
        except Exception as _ek:
            st.error(f"Karne hatası: {_ek}")

    # ── VELİ EĞİTİM İÇERİKLERİ ──
    with t_veli_egitim_v:
        try:
            styled_section("Veli Eğitim İçerikleri", "#8B5CF6")
            st.markdown(
                '<div style="background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.2);'
                'border-radius:12px;padding:14px;margin-bottom:12px;color:#A5B4FC;font-size:.85rem">'
                '🎓 Çocuğunuzun gelişimini desteklemek için hazırlanmış eğitim içerikleri</div>',
                unsafe_allow_html=True)
            import json as _json_ve
            _ve_path = None
            try:
                from utils.tenant import get_data_path
                _ve_path = os.path.join(get_data_path(""), "veli_egitim_icerikleri.json")
            except Exception:
                pass
            if not _ve_path or not os.path.exists(_ve_path):
                _ve_path = os.path.join("data", "veli_egitim_icerikleri.json")
            _icerikler = []
            if os.path.exists(_ve_path):
                try:
                    with open(_ve_path, "r", encoding="utf-8") as _vf:
                        _icerikler = _json_ve.load(_vf)
                except Exception:
                    pass
            if _icerikler:
                _kategoriler = sorted(set(ic.get("kategori", "") for ic in _icerikler))
                _sec_kat = st.selectbox("Kategori", ["Tümü"] + _kategoriler, key="veli_egitim_kat")
                for _ic in _icerikler:
                    if _sec_kat != "Tümü" and _ic.get("kategori") != _sec_kat:
                        continue
                    with st.expander(f"📖 {_ic.get('baslik', '')} — {_ic.get('sure_dk', 0)} dk"):
                        st.markdown(f"**Kategori:** {_ic.get('kategori', '')}")
                        st.markdown(f"**Süre:** {_ic.get('sure_dk', 0)} dakika")
                        st.markdown(f"{_ic.get('ozet', '')}")
            else:
                styled_info_banner("Eğitim içerikleri henüz yüklenmedi.", "info")
        except Exception as _eve:
            st.error(f"Veli eğitim hatası: {_eve}")

    with t_smarti_ana:
        _render_smarti_tab(auth_user, role="Veli")
    with t_okul_oncesi_dijital_v:
        try:
            _render_veli_okul_oncesi_dijital()
        except Exception as _e:
            st.info(f"Okul Öncesi Dijital yüklenemedi: {_e}")


def _render_veli_geri_bildirim_tab(store, student, auth_user, kademe="anaokulu"):
    """Veli geri bildirim formu — evdeki durum bildirimi, öğretmene düşer."""
    from datetime import date
    from models.akademik_takip import (
        VeliGeriBildirim, VELI_GB_YEMEK, VELI_GB_UYKU, VELI_GB_RUH_HALI,
        VELI_GB_SAGLIK, VELI_GB_EVDE_ANA, VELI_GB_EVDE_ILKOKUL,
    )

    styled_section("Veli Geri Bildirim — Evde Durum Bildirimi", "#059669")

    # Tarih seçici
    tc1, tc2 = st.columns([1, 3])
    with tc1:
        secili_tarih = st.date_input("Tarih", value=date.today(), key="vgb_tarih")
    tarih_str = secili_tarih.strftime("%Y-%m-%d")

    # Mevcut bildirim var mı kontrol
    mevcut = store.get_veli_geri_bildirimler(student_id=student.id, tarih=tarih_str)
    duzenle = mevcut[0] if mevcut else None

    # Premium stat row
    _vgb_durum = "Gönderildi" if duzenle else "Girilmedi"
    _vgb_okundu = "Okundu" if (duzenle and duzenle.okundu) else ("Bekliyor" if duzenle else "—")
    _vgb_gecmis = store.get_veli_geri_bildirimler(student_id=student.id)
    styled_stat_row([
        ("Bugün", _vgb_durum, "#10b981" if duzenle else "#f59e0b", "📝"),
        ("Öğretmen", _vgb_okundu, "#10b981" if (duzenle and duzenle.okundu) else "#6b7280", "👨‍🏫"),
        ("Toplam", str(len(_vgb_gecmis)), "#6366f1", "📊"),
    ])

    st.markdown(
        '<div style="background:linear-gradient(135deg,#ecfdf5,#d1fae5);border:1px solid #6ee7b7;'
        'border-radius:12px;padding:12px 16px;margin-bottom:14px;font-size:0.82rem;color:#065f46;">'
        '📝 Çocuğunuzun evdeki durumunu öğretmenine bildirin. Bu bilgiler sınıf öğretmenine iletilecektir.</div>',
        unsafe_allow_html=True
    )

    if duzenle and duzenle.okundu:
        _ogr_not_html = ""
        if duzenle.ogretmen_notu:
            _ogr_not_html = (f'<div style="margin-top:6px;font-size:0.85rem;color:#475569;">'
                             f'<b>Öğretmen notu:</b> {duzenle.ogretmen_notu}</div>')
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #86efac;'
            f'border-radius:12px;padding:14px 16px;margin-bottom:14px;'
            f'box-shadow:0 2px 6px rgba(34,197,94,0.1);">'
            f'<span style="font-weight:700;color:#166534;">✅ Öğretmen tarafından okundu</span>'
            f'{_ogr_not_html}'
            f'</div>',
            unsafe_allow_html=True
        )

    yemek_map = dict(VELI_GB_YEMEK)
    uyku_map = dict(VELI_GB_UYKU)
    ruh_map = dict(VELI_GB_RUH_HALI)
    saglik_map = dict(VELI_GB_SAGLIK)
    evde_list = VELI_GB_EVDE_ANA if kademe == "anaokulu" else VELI_GB_EVDE_ILKOKUL

    yemek_keys = [k for k, _ in VELI_GB_YEMEK]
    yemek_labels = [v for _, v in VELI_GB_YEMEK]
    uyku_keys = [k for k, _ in VELI_GB_UYKU]
    uyku_labels = [v for _, v in VELI_GB_UYKU]
    ruh_keys = [k for k, _ in VELI_GB_RUH_HALI]
    ruh_labels = [v for _, v in VELI_GB_RUH_HALI]
    saglik_keys = [k for k, _ in VELI_GB_SAGLIK]
    saglik_labels = [v for _, v in VELI_GB_SAGLIK]

    def _idx(keys, val):
        try:
            return keys.index(val)
        except ValueError:
            return 0

    # ── FORM — Premium Gradient Sections ──
    def _vgb_section(icon, title, color1, color2, border_color):
        st.markdown(
            f'<div style="background:linear-gradient(135deg,{color1},{color2});'
            f'border-left:4px solid {border_color};border-radius:10px;'
            f'padding:10px 14px;margin:14px 0 8px 0;font-size:0.88rem;font-weight:700;color:#475569;">'
            f'{icon} {title}</div>', unsafe_allow_html=True)

    _vgb_section("🍽️", "Akşam Yemeği", "#fffbeb", "#fef3c7", "#f59e0b")
    fc1, fc2 = st.columns(2)
    with fc1:
        aksam_idx = st.selectbox("Durum", range(len(yemek_keys)),
                                  index=_idx(yemek_keys, duzenle.aksam_yemegi) if duzenle else 0,
                                  format_func=lambda i: yemek_labels[i],
                                  key="vgb_aksam")
    with fc2:
        aksam_not = st.text_input("Not (opsiyonel)",
                                   value=duzenle.aksam_yemegi_not if duzenle else "",
                                   key="vgb_aksam_not")

    _vgb_section("☕", "Kahvaltı", "#fff7ed", "#ffedd5", "#f97316")
    fc3, fc4 = st.columns(2)
    with fc3:
        kahv_idx = st.selectbox("Durum", range(len(yemek_keys)),
                                 index=_idx(yemek_keys, duzenle.kahvalti) if duzenle else 0,
                                 format_func=lambda i: yemek_labels[i],
                                 key="vgb_kahv")
    with fc4:
        kahv_not = st.text_input("Not (opsiyonel)",
                                  value=duzenle.kahvalti_not if duzenle else "",
                                  key="vgb_kahv_not")

    _vgb_section("😴", "Gece Uykusu", "#eef2ff", "#e0e7ff", "#6366f1")
    uc1, uc2, uc3 = st.columns(3)
    with uc1:
        uyku_idx = st.selectbox("Uyku Durumu", range(len(uyku_keys)),
                                 index=_idx(uyku_keys, duzenle.gece_uykusu) if duzenle else 0,
                                 format_func=lambda i: uyku_labels[i],
                                 key="vgb_uyku")
    with uc2:
        uyku_saati = st.text_input("Yattığı Saat",
                                    value=duzenle.uyku_saati if duzenle else "21:00",
                                    key="vgb_uyku_saat")
    with uc3:
        uyanma_saati = st.text_input("Kalktığı Saat",
                                      value=duzenle.uyanma_saati if duzenle else "07:00",
                                      key="vgb_uyanma")

    _vgb_section("😊", "Sabah Ruh Hali", "#fdf4ff", "#fae8ff", "#a855f7")
    ruh_idx = st.selectbox("Ruh Hali", range(len(ruh_keys)),
                            index=_idx(ruh_keys, duzenle.sabah_ruh_hali) if duzenle else 0,
                            format_func=lambda i: ruh_labels[i],
                            key="vgb_ruh")

    _vgb_section("🏥", "Sağlık Durumu", "#fef2f2", "#fee2e2", "#ef4444")
    sc1, sc2 = st.columns(2)
    with sc1:
        saglik_idx = st.selectbox("Durum", range(len(saglik_keys)),
                                   index=_idx(saglik_keys, duzenle.saglik_durumu) if duzenle else 0,
                                   format_func=lambda i: saglik_labels[i],
                                   key="vgb_saglik")
    with sc2:
        saglik_not = st.text_input("Açıklama (opsiyonel)",
                                    value=duzenle.saglik_notu if duzenle else "",
                                    key="vgb_saglik_not")

    _vgb_section("🏠", "Evde Yapılanlar", "#f0fdf4", "#dcfce7", "#22c55e")
    evde_keys = [k for k, _ in evde_list]
    evde_labels = [v for _, v in evde_list]
    evde_defaults = duzenle.evde_yapilan if duzenle else []
    default_idxs = [i for i, k in enumerate(evde_keys) if k in evde_defaults]
    secili_evde = st.multiselect("Yapılanları seçin", range(len(evde_keys)),
                                  default=default_idxs,
                                  format_func=lambda i: evde_labels[i],
                                  key="vgb_evde")

    _vgb_section("📝", "Veli Notu", "#111827", "#1A2035", "#64748b")
    veli_notu = st.text_area("Eklemek istediğiniz not",
                              value=duzenle.veli_notu if duzenle else "",
                              height=80, key="vgb_not")

    # ── KAYDET ──
    if st.button("💾 Gönder", type="primary", key="vgb_kaydet"):
        if duzenle:
            gb = duzenle
        else:
            gb = VeliGeriBildirim(
                student_id=student.id,
                student_adi=student.tam_ad,
                tarih=tarih_str,
                sinif=str(student.sinif),
                sube=student.sube,
                veli_id=auth_user.get("username", ""),
                veli_adi=auth_user.get("ad", ""),
            )
        gb.aksam_yemegi = yemek_keys[aksam_idx]
        gb.aksam_yemegi_not = aksam_not
        gb.kahvalti = yemek_keys[kahv_idx]
        gb.kahvalti_not = kahv_not
        gb.gece_uykusu = uyku_keys[uyku_idx]
        gb.uyku_saati = uyku_saati
        gb.uyanma_saati = uyanma_saati
        gb.sabah_ruh_hali = ruh_keys[ruh_idx]
        gb.saglik_durumu = saglik_keys[saglik_idx]
        gb.saglik_notu = saglik_not
        gb.evde_yapilan = [evde_keys[i] for i in secili_evde]
        gb.veli_notu = veli_notu
        store.save_veli_geri_bildirim(gb)
        st.success("✅ Geri bildirim gönderildi! Öğretmeniniz görecektir.")
        st.rerun()

    # ── GEÇMİŞ BİLDİRİMLER ──
    styled_section("Geçmiş Bildirimler", "#64748b")
    with st.expander("📅 Son 10 Bildirim", expanded=False):
        gecmis = store.get_veli_geri_bildirimler(student_id=student.id)
        gecmis.sort(key=lambda b: b.tarih, reverse=True)
        gecmis = [b for b in gecmis if b.tarih != tarih_str][:10]
        if not gecmis:
            styled_info_banner("Geçmiş bildirim bulunamadı.", "info")
        else:
            for gb in gecmis:
                _gb_ok = gb.okundu
                _gb_bg = "linear-gradient(135deg,#f0fdf4,#dcfce7)" if _gb_ok else "linear-gradient(135deg,#fffbeb,#fef3c7)"
                _gb_border = "#86efac" if _gb_ok else "#fcd34d"
                _gb_badge_bg = "#16a34a" if _gb_ok else "#f59e0b"
                _gb_badge = "✅ Okundu" if _gb_ok else "⏳ Bekliyor"
                ruh_lbl = ruh_map.get(gb.sabah_ruh_hali, '-')
                saglik_lbl = saglik_map.get(gb.saglik_durumu, '-')
                _ogr_n = f'<div style="margin-top:4px;font-size:0.78rem;color:#166534;"><b>Öğretmen:</b> {gb.ogretmen_notu}</div>' if gb.ogretmen_notu else ""
                st.markdown(
                    f'<div style="background:{_gb_bg};border:1px solid {_gb_border};border-radius:10px;'
                    f'padding:10px 14px;margin-bottom:6px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<div><span style="font-weight:700;color:#475569;font-size:0.85rem;">📅 {gb.tarih}</span>'
                    f'<span style="margin-left:10px;font-size:0.78rem;color:#475569;">'
                    f'😊 {ruh_lbl} · 🏥 {saglik_lbl}</span></div>'
                    f'<span style="background:{_gb_badge_bg};color:#fff;padding:3px 10px;border-radius:20px;'
                    f'font-size:0.68rem;font-weight:600;">{_gb_badge}</span>'
                    f'</div>{_ogr_n}</div>', unsafe_allow_html=True
                )


def _render_veli_okul_oncesi_dijital():
    """Anasınıfı velisi için Dijital Öğrenme — Okul Öncesi YouTube Kanalları."""
    styled_section("📚 Dijital Kütüphane — Okul Öncesi", "#7c3aed")
    st.caption("Canlı ders platformları ve çocuğunuz için önerilen ücretsiz eğitim kanalları")

    # --- CANLI DERS PLATFORMLARI ---
    with st.expander("📹 Canlı Ders Platformları (Zoom, Teams, Classroom, Meet)", expanded=True):
        st.markdown(
            '<div style="background:linear-gradient(135deg,#4f46e510,#6366f108);'
            'border-left:4px solid #6366f1;padding:10px 16px;border-radius:0 10px 10px 0;'
            'margin-bottom:14px;font-size:0.82rem;color:#475569;">'
            'Öğretmeniniz canlı ders linki paylaştığında aşağıdaki platformlardan giriş yapabilirsiniz.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_PANEL_VIDEO_KONFERANS_HTML_CACHE, unsafe_allow_html=True)

    # --- TÜRKÇE (Çizgi Film / Şarkı / Masal) ---
    st.markdown("#### 🎬 Türkçe — Çizgi Film / Şarkı / Masal")

    _VELİ_YT_TR_CIZGI = (
        ("TRT Çocuk", "TRT Çocuk Resmi Kanalı",
         "https://www.youtube.com/trtcocuk", "#dc2626", "#991b1b", "#fecaca"),
        ("Niloya", "Niloya Çizgi Film",
         "https://www.youtube.com/@niloyatv", "#e11d48", "#be123c", "#fecdd3"),
        ("Kukuli", "Kukuli — Eğlenceli Çizgi Film",
         "https://www.youtube.com/Kukuli", "#ea580c", "#c2410c", "#fed7aa"),
        ("Düşyeri (Pepee vb.)", "Pepee, Leliko ve daha fazlası",
         "https://www.youtube.com/@Dusyeri", "#d97706", "#b45309", "#fef3c7"),
        ("BabyTV Türkçe", "BabyTV Türkçe Çocuk Kanalı",
         "https://www.youtube.com/channel/UCIIxdvCLc0c_iJ8xbtFVPNQ", "#ca8a04", "#a16207", "#fef9c3"),
        ("LooLoo Çocuklar", "LooLoo Çocuk Şarkıları",
         "https://www.youtube.com/@LooLooCocuklar", "#16a34a", "#15803d", "#dcfce7"),
        ("HeyKids Türkçe", "Bebek Şarkıları Türkçe",
         "https://www.youtube.com/channel/UCUwOn6rugJcI6eS-cPUegMA", "#0d9488", "#0f766e", "#ccfbf1"),
        ("Adisebaba Masal", "Masal ve Çocuk Şarkıları",
         "https://www.youtube.com/channel/UCFHuNk4ZyCkWdxKKULyEKKA", "#7c3aed", "#6d28d9", "#ede9fe"),
    )

    cards_html = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
    for ad, aciklama, link, r1, r2, rt in _VELİ_YT_TR_CIZGI:
        cards_html += (
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
            f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
            f'transition:transform 0.15s,box-shadow 0.15s;">'
            f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
            f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
            f'padding:1px 8px;">▶ YouTube</div>'
            f'<div style="font-size:16px;font-weight:800;color:white;'
            f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
            f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
            f'</div></a>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # --- TÜRKÇE (Etkinlik / Öğretmen Kanalları) ---
    st.markdown("#### 👩‍🏫 Türkçe — Etkinlik / Öğretmen Kanalları")

    _VELİ_YT_TR_OGRETMEN = (
        ("Buse Öğretmen", "Okul Öncesi Etkinlikler",
         "https://www.youtube.com/c/BuseDurano%C4%9Flu", "#2563eb", "#1d4ed8", "#bfdbfe"),
        ("Yonca Öğretmen", "Okul Öncesi Eğitim",
         "https://www.youtube.com/channel/UCf1Y0wt9IyqZuvcH5Tw07dg", "#7c3aed", "#6d28d9", "#ede9fe"),
        ("AÇEV", "Anne Çocuk Eğitim Vakfı",
         "https://www.youtube.com/channel/UCknrine7khh3jBWiushNOpw", "#059669", "#047857", "#d1fae5"),
    )

    cards_html2 = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
    for ad, aciklama, link, r1, r2, rt in _VELİ_YT_TR_OGRETMEN:
        cards_html2 += (
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
            f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
            f'transition:transform 0.15s,box-shadow 0.15s;">'
            f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
            f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
            f'padding:1px 8px;">▶ YouTube</div>'
            f'<div style="font-size:16px;font-weight:800;color:white;'
            f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
            f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
            f'</div></a>'
        )
    cards_html2 += '</div>'
    st.markdown(cards_html2, unsafe_allow_html=True)

    # --- İNGİLİZCE (Güçlü Eğitsel Kanallar) ---
    st.markdown("#### 🌍 İngilizce — Eğitsel Kanallar")

    _VELİ_YT_EN = (
        ("Super Simple Songs", "Çocuk Şarkıları & Eğitim",
         "https://www.youtube.com/user/SuperSimpleSongs", "#dc2626", "#991b1b", "#fecaca"),
        ("Sesame Street", "Susam Sokağı Resmi Kanalı",
         "https://www.youtube.com/sesamestreet", "#16a34a", "#15803d", "#dcfce7"),
        ("Numberblocks", "Sayılar ve Matematik",
         "https://www.youtube.com/channel/UCPlwvN0w4qFSP1FllALB92w", "#2563eb", "#1d4ed8", "#bfdbfe"),
        ("Alphablocks", "Harfler ve Okuma",
         "https://www.youtube.com/channel/UC_qs3c0ehDvZkbiEbOj6Drg", "#7c3aed", "#6d28d9", "#ede9fe"),
        ("PBS KIDS", "PBS Çocuk Eğitim",
         "https://www.youtube.com/channel/UCrNnk0wFBnCS1awGjq_ijGQ", "#0d9488", "#0f766e", "#ccfbf1"),
        ("CBeebies", "BBC Çocuk Kanalı",
         "https://www.youtube.com/cbeebies", "#d97706", "#b45309", "#fef3c7"),
        ("Pinkfong", "Baby Shark & Eğitsel İçerikler",
         "https://www.youtube.com/Pinkfong", "#e11d48", "#be123c", "#fecdd3"),
    )

    cards_html3 = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px;margin-bottom:20px;">'
    for ad, aciklama, link, r1, r2, rt in _VELİ_YT_EN:
        cards_html3 += (
            f'<a href="{link}" target="_blank" rel="noopener" style="text-decoration:none;">'
            f'<div class="sc-stat-hover" style="background:linear-gradient(135deg,{r1},{r2});border-radius:14px;'
            f'padding:22px 18px;text-align:center;position:relative;cursor:pointer;'
            f'transition:transform 0.15s,box-shadow 0.15s;">'
            f'<div style="font-size:11px;position:absolute;top:8px;left:12px;'
            f'background:rgba(255,255,255,0.2);color:white;border-radius:8px;'
            f'padding:1px 8px;">▶ YouTube</div>'
            f'<div style="font-size:16px;font-weight:800;color:white;'
            f'letter-spacing:0.5px;margin-top:8px;">{ad}</div>'
            f'<div style="color:{rt};font-size:10px;margin-top:6px;">{aciklama}</div>'
            f'</div></a>'
        )
    cards_html3 += '</div>'
    st.markdown(cards_html3, unsafe_allow_html=True)


def _render_veli_normal_panel(store, od, student, auth_user, is_preview):
    """Normal (ilkokul+) öğrenci veli paneli — modern toplu tasarım.

    Sekmeler EN ÜSTTE. Tüm widget yığını + AI briefing + 360 + Quick Actions
    'Özet' sekmesinin İÇİNDE. Veli sayfaya girer girmez sekmelere ulaşır.
    """
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR, render_egitim_yili_secici

    sinif_no = normalize_sinif(str(student.sinif))
    _is_ilkokul = sinif_no in KADEME_SINIFLAR.get("Ilkokul", [])
    _is_ortaokul = sinif_no in KADEME_SINIFLAR.get("Ortaokul", [])
    _is_lise = sinif_no in KADEME_SINIFLAR.get("Lise", [])
    _is_12 = sinif_no in ("1", "2")  # 1-2. sınıf: akademik değerlendirme yok

    selected_egitim_yili = render_egitim_yili_secici("veli_panel_egitim_yili")

    # Yardimci: Ozet sekmesi icerigi (her panelde ayni sekilde rendere edilecek)
    def _render_ozet_icerik():
        """Ozet sekmesinin tum icerigi: AI briefing + 360 + Quick Actions + widgetlar."""
        from datetime import date as _date
        # 1) Akıllı kartlar
        try:
            _render_veli_ai_briefing(store, student, auth_user, od)
        except Exception:
            pass
        try:
            _render_veli_360_snapshot(store, student, od)
        except Exception:
            pass
        try:
            _render_veli_quick_actions(store, student, auth_user)
        except Exception:
            pass

        # 2) Sınıf kadrosu
        try:
            _render_sinif_kadro_kunye(store, student)
        except Exception:
            pass

        # 3) Ozet stat row (kademeye gore)
        attendance = store.get_attendance(student_id=student.id)
        devamsizlik = len(attendance) if attendance else 0
        okunmamis = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))

        if _is_12:
            odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
            teslimler = store.get_odev_teslimleri(student_id=student.id)
            teslim_ids = {t.odev_id for t in teslimler if t.durum == "teslim_edildi"}
            bekleyen_odev = sum(1 for o in odevler if o.id not in teslim_ids)
            styled_stat_row([
                ("Devamsızlık", str(devamsizlik), "#ef4444", "📅"),
                ("Bekleyen Ödev", str(bekleyen_odev), "#f59e0b", "📋"),
                ("Mesajlar", str(okunmamis) if okunmamis > 0 else "0", "#8b5cf6", "✉️"),
            ])
        else:
            grades = store.get_grades(student_id=student.id)
            results = od.get_results(student_id=student.id)
            odevler = store.get_odevler(sinif=student.sinif, sube=student.sube, durum="aktif")
            teslimler = store.get_odev_teslimleri(student_id=student.id)
            teslim_ids = {t.odev_id for t in teslimler if t.durum == "teslim_edildi"}
            bekleyen_odev = sum(1 for o in odevler if o.id not in teslim_ids)
            akademik_yil = _get_akademik_yil()
            kyt_analiz = store.get_kyt_ogrenci_analizi(student_id=student.id, akademik_yil=akademik_yil)
            not_ort = _get_not_ortalamasi(grades)
            son_sinav = f"{results[-1].score:.0f}" if results and results[-1].score is not None else "-"
            kyt_basari = f"%{kyt_analiz['basari_yuzde']}" if kyt_analiz["toplam"] > 0 else "-"
            stat_items = [
                ("Not Ortalaması", str(not_ort), "#2563eb", "📊"),
                ("Devamsızlık", str(devamsizlik), "#ef4444", "📅"),
                ("Son Sınav", son_sinav, "#7c3aed", "📝"),
                ("Bekleyen Ödev", str(bekleyen_odev), "#f59e0b", "📋"),
                ("KYT Başarı", kyt_basari, "#22c55e", "🎯"),
                ("Mesajlar", str(okunmamis) if okunmamis > 0 else "0", "#8b5cf6", "✉️"),
            ]
            styled_stat_row(stat_items)

        # 4) Smarti karsilama
        st.markdown("")
        _render_smarti_top_greeting(auth_user, student)

        # 5) Kademeye ozel uyari/sayac (rozet gibi)
        from utils.ui_common import geri_sayim_sayaci
        if _is_ilkokul:
            geri_sayim_sayaci("2026-06-20", "Dönem Sonu", "🏫")
        elif _is_ortaokul:
            geri_sayim_sayaci("2026-06-14", "LGS Sınavı", "📝")
            geri_sayim_sayaci("2026-06-20", "Dönem Sonu", "🏫")
            st.markdown(
                '<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);'
                'border-radius:10px;padding:10px 14px;margin:8px 0;display:flex;align-items:center;gap:8px">'
                '<span style="font-size:1.1rem">🎯</span>'
                '<div><div style="color:#1e40af;font-weight:700;font-size:.82rem">LGS Hazırlık Modu Aktif</div>'
                '<div style="color:#475569;font-size:.7rem">Deneme analizi, hedef puan takibi ve kazanım borç bankası</div></div></div>',
                unsafe_allow_html=True)
        elif _is_lise:
            geri_sayim_sayaci("2026-06-21", "TYT Sınavı", "📝")
            geri_sayim_sayaci("2026-06-22", "AYT Sınavı", "📝")
            geri_sayim_sayaci("2026-06-25", "Dönem Sonu", "🏫")
            st.markdown(
                '<div style="background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.2);'
                'border-radius:10px;padding:10px 14px;margin:8px 0;display:flex;align-items:center;gap:8px">'
                '<span style="font-size:1.1rem">🎓</span>'
                '<div><div style="color:#7c3aed;font-weight:700;font-size:.82rem">YKS Hazırlık Modu Aktif</div>'
                '<div style="color:#475569;font-size:.7rem">TYT/AYT deneme analizi, alan seçimi rehberi, üniversite tercih danışmanlığı</div></div></div>',
                unsafe_allow_html=True)

        # 6) Detayli widget yigini — expander icinde sade
        with st.expander("✨ Detaylı İstatistikler & Widget'lar", expanded=False):
            try:
                from utils.ui_common import (mutluluk_indeksi, aylik_gelisim_karsilastirmasi,
                                              sinif_siralama_anonim, geri_sayim_sayaci,
                                              odev_hatirlatma_widget, etkinlik_foto_galerisi,
                                              hedef_belirleme_widget)
                import random as _rnd

                _m_skor = _rnd.uniform(6.5, 9.0)
                mutluluk_indeksi(_m_skor, {"akademik": _rnd.randint(6, 9), "sosyal": _rnd.randint(7, 9),
                                            "davranis": _rnd.randint(5, 9), "saglik": _rnd.randint(7, 10)})

                hedef_belirleme_widget([
                    {"hedef": "Mat 80+", "mevcut": 72, "hedef_deger": 80, "birim": "puan"},
                    {"hedef": "İng 75+", "mevcut": 68, "hedef_deger": 75, "birim": "puan"},
                    {"hedef": "Devamsızlık < 5", "mevcut": 3, "hedef_deger": 5, "birim": "gün"},
                ])

                _gc1, _gc2 = st.columns(2)
                with _gc1:
                    aylik_gelisim_karsilastirmasi(68.5, 72.3, "Genel")
                    aylik_gelisim_karsilastirmasi(65, 71, "Mat")
                    aylik_gelisim_karsilastirmasi(75, 73, "İng")
                with _gc2:
                    sinif_siralama_anonim(_rnd.randint(3, 15), 30)

                odev_hatirlatma_widget([
                    {"ders": "Matematik", "baslik": "Konu tekrar", "son_tarih": "2026-04-08", "teslim": False},
                    {"ders": "Türkçe", "baslik": "Kompozisyon", "son_tarih": "2026-04-10", "teslim": False},
                ])

                etkinlik_foto_galerisi()
            except Exception:
                pass

            try:
                from utils.ui_common import (cocugum_bugun_ne_ogrendi, haftalik_animasyonlu_ozet,
                                              acil_durum_butonu, uyku_enerji_takibi,
                                              kisisel_icerik_onerisi, veli_tesekkur_sistemi,
                                              goruntulu_gorusme_randevu)

                haftalik_animasyonlu_ozet()
                try:
                    from utils.ui_common import haftalik_video_widget
                    haftalik_video_widget()
                except Exception:
                    pass

                try:
                    _bugun_str = _date.today().isoformat()
                    try:
                        _sinif_int = int(student.sinif) if str(student.sinif).isdigit() else 0
                    except Exception:
                        _sinif_int = 0
                    _bugun_kazanim = []
                    _ki_list = store.get_kazanim_isleme(
                        sinif=_sinif_int, sube=getattr(student, "sube", ""),
                        durum="islendi"
                    ) or []
                    for _ki in _ki_list:
                        _t = getattr(_ki, "tarih", "") or getattr(_ki, "updated_at", "")
                        if _t and str(_t)[:10] == _bugun_str:
                            _bugun_kazanim.append({
                                "ders": getattr(_ki, "ders", "-"),
                                "kazanim": getattr(_ki, "kazanim_metni", "") or getattr(_ki, "kazanim_kodu", "-"),
                            })
                    cocugum_bugun_ne_ogrendi(_bugun_kazanim)
                except Exception:
                    cocugum_bugun_ne_ogrendi()

                acil_durum_butonu()

                from utils.ui_common import (canli_ders_giris_bildirimi, ai_gunluk_motivasyon,
                                              veli_puan_sistemi, gelecek_hafta_plani,
                                              anlik_not_sinif_karsilastirma, ai_hafta_sonu_etkinlik_onerisi,
                                              karne_oncesi_panic_uyari, kardes_karsilastirma_paneli)

                _stu_ad = student.ad if hasattr(student, 'ad') else student.get('ad', '')
                canli_ders_giris_bildirimi()
                ai_gunluk_motivasyon(_stu_ad)
                gelecek_hafta_plani()
                anlik_not_sinif_karsilastirma(75, 72, 68, "Genel")
                veli_puan_sistemi()
                karne_oncesi_panic_uyari(48, 50, 21)
                with st.expander("🎉 Hafta Sonu Etkinlik Önerisi", expanded=False):
                    ai_hafta_sonu_etkinlik_onerisi()
            except Exception:
                pass

    # ── 1-2. SINIF: 21 sekme (Mesajlar EN BASTA + Ozet + 2 birlesik + Basari Duvari + STEAM) ──
    if _is_12:
        try:
            _unread_12 = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))
        except Exception:
            _unread_12 = 0
        _msg_label_12 = (f"  💬 Mesajlar 🔴 {_unread_12}  "
                         if _unread_12 > 0 else "  💬 Mesajlar  ")
        (t_mesajlar,
         t_ozet_12,
         t_rapor, t_basari_12, t_vgb, t_kazanim, t_devam, t_odevler,
         t_saglik_birlesik_12,
         t_belgeler_birlesik_12,
         t_program, t_dijital,
         t_yabanci_dil, t_steam_12, t_etkinlik, t_yemek, t_servis, t_randevu,
         t_anket, t_gunbilgi_12, t_smarti,
        ) = st.tabs([
            _msg_label_12,
            "  📊 Özet  ",
            "  📋 Günlük Rapor  ",
            "  🌟 Başarı Duvarı  ",
            "  📝 Veli Geri Bildirim  ",
            "  📖 İşlenen Kazanımlar  ",
            "  📅 Devamsızlık  ",
            "  📝 Ödevler  ",
            "  🏥 Sağlık & Rehberlik  ",
            "  📎 Belgeler  ",
            "  🗓️ Ders Programı  ",
            "  📚 Dijital Kütüphane  ",
            "  🌐 Yabancı Dil  ",
            "  🔬 STEAM Merkezi  ",
            "  🎉 Etkinlik & Duyurular  ",
            "  🍽️ Yemek Menüsü  ",
            "  🚌 Servis Takibi  ",
            "  📅 Randevu  ",
            "  📊 Memnuniyet Anketi  ",
            "  💡 Günün Bilgisi  ",
            "  🤖 Smarti AI  ",
        ])

        with t_ozet_12:
            _render_ozet_icerik()

        with t_basari_12:
            _render_aile_basari_duvari(store, student, auth_user)

        with t_rapor:
            _render_veli_ilkokul_gunluk_rapor(store, student, auth_user)
            try:
                from utils.ui_common import uyku_enerji_takibi as _uet_12
                _uet_12()
            except Exception:
                pass
        with t_vgb:
            _render_veli_geri_bildirim_tab(store, student, auth_user, kademe="ilkokul")
        with t_kazanim:
            _render_islenen_kazanimlar_tab(store, student)
        with t_devam:
            _render_devamsizlik_tab(store, student)
        with t_odevler:
            _render_odevler_tab(store, student, od)
            try:
                from utils.ui_common import odev_yardim_ai
                odev_yardim_ai("1-2. Sınıf Ödevleri")
            except Exception:
                pass

        # ── BIRLESIM 1: SAGLIK & REHBERLIK (3 alt sekme) ──
        with t_saglik_birlesik_12:
            _sa_12_1, _sa_12_2, _sa_12_3 = st.tabs([
                "  🏥 Revir Kayıtları  ",
                "  🧑‍⚕️ Rehberlik  ",
                "  📊 Test Sonuçları  ",
            ])
            with _sa_12_1:
                _render_revir_kayitlari_tab(student)
            with _sa_12_2:
                _render_rehberlik_vaka_tab(student)
                try:
                    from utils.ui_common import toplanti_ozeti_widget
                    toplanti_ozeti_widget(
                        ozet="Genel değerlendirme olumlu. Velilerin okul etkinliklerine katılımı teşvik edildi.",
                        tarih="2026-03-28",
                        gundem=["Dönem sonu değerlendirmesi", "Yaz okulu bilgilendirmesi", "Sosyal etkinlik planları"],
                    )
                except Exception:
                    pass
            with _sa_12_3:
                _render_rehberlik_test_tab(student)
                try:
                    from utils.ui_common import ogretmen_degerlendirme_notu
                    ogretmen_degerlendirme_notu(
                        yorum="Öğrenciniz derslerine düzenli katılım sağlamakta ve gelişim göstermektedir.",
                        ders="Genel Değerlendirme", donem="2025-2026 / 2. Dönem",
                    )
                except Exception:
                    pass

        # ── BIRLESIM 2: BELGELER (Gelen + Talep, 2 alt sekme) ──
        with t_belgeler_birlesik_12:
            _bl_12_1, _bl_12_2 = st.tabs([
                "  📎 Gelen Belgeler & Linkler  ",
                "  📄 Belge Talep  ",
            ])
            with _bl_12_1:
                _render_veli_belgeler_tab(store, student)
            with _bl_12_2:
                if is_preview:
                    styled_info_banner("Önizleme modunda belge talebi oluşturulamaz.", "info")
                else:
                    _render_belge_talep_tab(student, auth_user)

        with t_mesajlar:
            if is_preview:
                styled_info_banner("Önizleme modunda mesajlaşma devre dışı.", "info")
            else:
                _render_mesajlar_tab(store, student, auth_user)
            try:
                from utils.ui_common import veli_tesekkur_sistemi as _vts_12
                _vts_12()
            except Exception:
                pass
        with t_program:
            _render_ders_programi_tab(store, student)
        with t_dijital:
            _render_dk_embed()
            try:
                from utils.ui_common import kisisel_icerik_onerisi as _kio_12
                _kio_12(seviye="İlkokul")
            except Exception:
                pass
        with t_yabanci_dil:
            from views.yabanci_dil import render_veli_english_tab
            render_veli_english_tab(student.sinif, student.sube)
        with t_steam_12:
            _render_stem_merkezi_tab(student, role="veli")
        with t_etkinlik:
            _render_etkinlik_duyuru_tab(student)
        with t_yemek:
            _render_yemek_menusu_tab()
        with t_servis:
            _render_servis_tab(student)
        with t_randevu:
            if is_preview:
                styled_info_banner("Önizleme modunda randevu talebi oluşturulamaz.", "info")
            else:
                _render_randevu_tab(store, student, auth_user)
            try:
                from utils.ui_common import goruntulu_gorusme_randevu as _ggr_12
                _ggr_12()
            except Exception:
                pass
        with t_anket:
            if is_preview:
                styled_info_banner("Önizleme modunda anket doldurulamaz.", "info")
            else:
                _render_memnuniyet_anketi_tab(student, auth_user)
        with t_gunbilgi_12:
            _render_gunun_bilgisi_tab()
        with t_smarti:
            _render_smarti_tab(auth_user, role="Veli")

    # ── 3+ SINIF: 11 ANA GRUP (Mesajlar EN BASTA + Ozet + 9 mevcut) ──
    else:
        try:
            _unread_34 = store.get_okunmamis_mesaj_sayisi(receiver_id=auth_user.get("username", ""))
        except Exception:
            _unread_34 = 0
        _msg_label_34 = (f"  💬 Mesajlar 🔴 {_unread_34}  "
                         if _unread_34 > 0 else "  💬 Mesajlar  ")
        (g_msg_top, g0_ozet, g1_gunluk, g2_akademik, g3_odev, g4_yon, g5_saglik,
         g6_iletisim, g7_program, g8_sosyal, g9_bilgi) = st.tabs([
            _msg_label_34,
            "  📊 Özet  ",
            "  📋 Günlük & Geri Bildirim  ",
            "  📊 Akademik Sonuçlar  ",
            "  📝 Ödev & Kazanım  ",
            "  🎓 Yönlendirme & Defter  ",
            "  🏥 Sağlık & Rehberlik  ",
            "  📎 Belge & Randevu  ",
            "  🗓️ Program & Kaynak  ",
            "  🎉 Sosyal & Hizmet  ",
            "  🤖 Bilgi & AI  ",
        ])

        # ══════════════════════════════════════════════════════════════
        # 💬 MESAJLAR — EN BASTA (top-level)
        # ══════════════════════════════════════════════════════════════
        with g_msg_top:
            if is_preview:
                styled_info_banner("Önizleme modunda mesajlaşma devre dışı.", "info")
            else:
                _render_mesajlar_tab(store, student, auth_user)

        # ══════════════════════════════════════════════════════════════
        # GRUP 0: ÖZET — varsayilan acik sekme
        # ══════════════════════════════════════════════════════════════
        with g0_ozet:
            _render_ozet_icerik()

        # ══════════════════════════════════════════════════════════════
        # GRUP 1: GUNLUK & GERI BILDIRIM (2 alt sekme)
        # ══════════════════════════════════════════════════════════════
        with g1_gunluk:
            _g1_t1, _g1_t2 = st.tabs([
                "  📋 Günlük Rapor  ",
                "  📝 Veli Geri Bildirim  ",
            ])
            with _g1_t1:
                if _is_ilkokul:
                    _render_veli_ilkokul_gunluk_rapor(store, student, auth_user)
                else:
                    _render_gunluk_rapor_tab(store, student, od, auth_user)
                try:
                    from utils.ui_common import uyku_enerji_takibi as _uet_34
                    _uet_34()
                except Exception:
                    pass
            with _g1_t2:
                _kademe_vgb = "ilkokul" if _is_ilkokul else "ortaokul"
                _render_veli_geri_bildirim_tab(store, student, auth_user, kademe=_kademe_vgb)

        # ══════════════════════════════════════════════════════════════
        # GRUP 2: AKADEMIK SONUCLAR (4 alt sekme)
        # ══════════════════════════════════════════════════════════════
        with g2_akademik:
            _g2_t1, _g2_t2, _g2_t3, _g2_t4 = st.tabs([
                "  📝 Notlar  ",
                "  📊 Sınav Sonuçları  ",
                "  📈 KYT Performans  ",
                "  🔄 Telafi Görevleri  ",
            ])
            with _g2_t1:
                _render_notlar_tab(store, student)
            with _g2_t2:
                _render_sinav_sonuclari_tab(od, student)
            with _g2_t3:
                _render_kyt_performans_tab(store, student)
            with _g2_t4:
                _render_telafi_tab(od, student)

        # ══════════════════════════════════════════════════════════════
        # GRUP 3: ODEV & KAZANIM (3 alt sekme)
        # ══════════════════════════════════════════════════════════════
        with g3_odev:
            _g3_t1, _g3_t2, _g3_t3 = st.tabs([
                "  📝 Klasik Ödevler  ",
                "  📖 Kazanım Ödevi  ",
                "  📚 Kazanım Borç Bankası  ",
            ])
            with _g3_t1:
                _render_odevler_tab(store, student, od)
                try:
                    from utils.ui_common import odev_yardim_ai
                    odev_yardim_ai("3+ Sınıf Ödevleri")
                except Exception:
                    pass
            with _g3_t2:
                _render_kazanim_odevi_tab(store, od, student)
            with _g3_t3:
                _render_borc_tab(store, student, rol="veli")

        # ══════════════════════════════════════════════════════════════
        # GRUP 4: YONLENDIRME & DEFTER (4 alt sekme — Basari Duvari eklendi)
        # ══════════════════════════════════════════════════════════════
        with g4_yon:
            _g4_t1, _g4_t2, _g4_t3, _g4_t4 = st.tabs([
                "  🎯 Akademik Yönlendirme  ",
                "  📓 Öğrenci Defteri  ",
                "  📥 Raporlar (PDF)  ",
                "  🌟 Başarı Duvarı  ",
            ])
            with _g4_t1:
                _render_akademik_yonlendirme_tab(store, student)
                # ── Lise icin: Universite Tercih Rehberi (eski ust widget'tan tasindi) ──
                if _is_lise:
                    st.markdown("---")
                    st.markdown(
                        '<div style="background:linear-gradient(135deg,#4c1d95,#7c3aed);'
                        'color:#fff;padding:14px 18px;border-radius:12px;margin-bottom:12px;'
                        'display:flex;align-items:center;gap:10px;'
                        'box-shadow:0 4px 16px rgba(124,58,237,0.25)">'
                        '<span style="font-size:1.5rem">🎓</span>'
                        '<div><div style="font-size:1.05rem;font-weight:800">'
                        'Üniversite Tercih Rehberi</div>'
                        '<div style="font-size:.78rem;opacity:.9;margin-top:2px">'
                        'TYT/AYT puan tahmini · Alan seçimi · Tercih stratejisi · '
                        'Burs imkânları · AI Danışman</div></div></div>',
                        unsafe_allow_html=True,
                    )
                    _ut1, _ut2, _ut3, _ut4 = st.columns(4)
                    with _ut1:
                        st.markdown(
                            '<div style="background:#1e1b4b;border:1px solid #4c1d9544;'
                            'border-radius:10px;padding:12px;text-align:center;height:100%">'
                            '<div style="font-size:1.5rem;margin-bottom:6px">🎯</div>'
                            '<div style="color:#c4b5fd;font-weight:800;font-size:.82rem;'
                            'margin-bottom:4px">Alan Seçimi</div>'
                            '<div style="color:#475569;font-size:.72rem">Çocuğunuzun güçlü '
                            'derslerine göre uygun alan önerisi</div></div>',
                            unsafe_allow_html=True,
                        )
                    with _ut2:
                        st.markdown(
                            '<div style="background:#1e1b4b;border:1px solid #4c1d9544;'
                            'border-radius:10px;padding:12px;text-align:center;height:100%">'
                            '<div style="font-size:1.5rem;margin-bottom:6px">📊</div>'
                            '<div style="color:#c4b5fd;font-weight:800;font-size:.82rem;'
                            'margin-bottom:4px">Puan Hesaplama</div>'
                            '<div style="color:#475569;font-size:.72rem">TYT + AYT puan '
                            'tahmini ve hedef puan analizi</div></div>',
                            unsafe_allow_html=True,
                        )
                    with _ut3:
                        st.markdown(
                            '<div style="background:#1e1b4b;border:1px solid #4c1d9544;'
                            'border-radius:10px;padding:12px;text-align:center;height:100%">'
                            '<div style="font-size:1.5rem;margin-bottom:6px">📋</div>'
                            '<div style="color:#c4b5fd;font-weight:800;font-size:.82rem;'
                            'margin-bottom:4px">Tercih Stratejisi</div>'
                            '<div style="color:#475569;font-size:.72rem">Sıralama, puan ve '
                            'konum bazlı tercih önerileri</div></div>',
                            unsafe_allow_html=True,
                        )
                    with _ut4:
                        st.markdown(
                            '<div style="background:#1e1b4b;border:1px solid #4c1d9544;'
                            'border-radius:10px;padding:12px;text-align:center;height:100%">'
                            '<div style="font-size:1.5rem;margin-bottom:6px">💰</div>'
                            '<div style="color:#c4b5fd;font-weight:800;font-size:.82rem;'
                            'margin-bottom:4px">Burs İmkânları</div>'
                            '<div style="color:#475569;font-size:.72rem">Başarı burslu '
                            'üniversite listesi ve şartları</div></div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
                    if st.button("🤖 AI Tercih Danışmanı'ndan Öneri Al",
                                 key="veli_tercih_ai_g4",
                                 type="primary",
                                 use_container_width=True):
                        try:
                            from openai import OpenAI
                            import os as _os_ut
                            _api_ut = _os_ut.environ.get("OPENAI_API_KEY", "")
                            if _api_ut:
                                with st.spinner("AI Tercih Danışmanı düşünüyor..."):
                                    _cl_ut = OpenAI(api_key=_api_ut)
                                    _resp_ut = _cl_ut.chat.completions.create(
                                        model="gpt-4o-mini",
                                        messages=[
                                            {"role": "system",
                                             "content": "Universite tercih danismanisin. "
                                                        "Turkce, somut, lise ogrencisi velisine "
                                                        "yonelik oneriler ver."},
                                            {"role": "user",
                                             "content": f"{student.sinif}. sinif ogrencisi "
                                                        f"icin universite tercih stratejisi, "
                                                        f"onemli tarihler ve veli olarak "
                                                        f"yapilmasi gerekenler hakkinda "
                                                        f"bilgi ver."},
                                        ],
                                        temperature=0.7, max_tokens=600,
                                    )
                                st.markdown(
                                    f'<div style="background:#1e1b4b;border:1px solid #7c3aed44;'
                                    f'border-radius:10px;padding:14px 18px;margin-top:10px;'
                                    f'color:#0f172a;font-size:.85rem;line-height:1.6">'
                                    f'<div style="font-weight:800;color:#c4b5fd;'
                                    f'margin-bottom:8px;font-size:.95rem">'
                                    f'🤖 AI Tercih Danışmanı</div>'
                                    f'{_resp_ut.choices[0].message.content}</div>',
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.info("Tercih danışmanlığı için OpenAI API anahtarı tanımlı değil.")
                        except Exception as _e_ut:
                            st.warning(f"AI bağlantı hatası: {_e_ut}")

            with _g4_t2:
                from views.ogrenci_defteri import render_ogrenci_defteri_tab
                render_ogrenci_defteri_tab(store, od, student, rol="veli",
                                           akademik_yil=selected_egitim_yili)
            with _g4_t3:
                _render_raporlar_tab(store, student, od)
            with _g4_t4:
                _render_aile_basari_duvari(store, student, auth_user)

        # ══════════════════════════════════════════════════════════════
        # GRUP 5: SAGLIK & REHBERLIK (4 alt sekme — devamsizlik dahil)
        # ══════════════════════════════════════════════════════════════
        with g5_saglik:
            _g5_t1, _g5_t2, _g5_t3, _g5_t4 = st.tabs([
                "  📅 Devamsızlık  ",
                "  🏥 Revir Kayıtları  ",
                "  🧑‍⚕️ Rehberlik  ",
                "  📋 Test Sonuçları  ",
            ])
            with _g5_t1:
                _render_devamsizlik_tab(store, student)
            with _g5_t2:
                _render_revir_kayitlari_tab(student)
            with _g5_t3:
                _render_rehberlik_vaka_tab(student)
                try:
                    from utils.ui_common import toplanti_ozeti_widget
                    toplanti_ozeti_widget(
                        ozet="Genel değerlendirme olumlu. Velilerin okul etkinliklerine katılımı teşvik edildi.",
                        tarih="2026-03-28",
                        gundem=["Dönem sonu değerlendirmesi", "Yaz okulu bilgilendirmesi", "LGS hazırlık planları"],
                    )
                except Exception:
                    pass
            with _g5_t4:
                _render_rehberlik_test_tab(student)
                try:
                    from utils.ui_common import ogretmen_degerlendirme_notu
                    ogretmen_degerlendirme_notu(
                        yorum="Öğrenciniz akademik hedeflerine yönelik olumlu bir performans sergilemektedir. Düzenli çalışma alışkanlığını sürdürmesi önerilir.",
                        ders="Genel Değerlendirme", donem="2025-2026 / 2. Dönem",
                    )
                except Exception:
                    pass

        # ══════════════════════════════════════════════════════════════
        # GRUP 6: BELGE & RANDEVU (3 alt sekme — Mesajlar en uste tasindi)
        # ══════════════════════════════════════════════════════════════
        with g6_iletisim:
            _g6_t2, _g6_t3, _g6_t4 = st.tabs([
                "  📎 Gelen Belgeler  ",
                "  📄 Belge Talep  ",
                "  📅 Randevu  ",
            ])
            with _g6_t2:
                _render_veli_belgeler_tab(store, student)
            with _g6_t3:
                if is_preview:
                    styled_info_banner("Önizleme modunda belge talebi oluşturulamaz. Belge talep yönetimi için Kurum Hizmetleri sekmesini kullanın.", "info")
                else:
                    _render_belge_talep_tab(student, auth_user)
            with _g6_t4:
                if is_preview:
                    styled_info_banner("Önizleme modunda randevu talebi oluşturulamaz. Randevu yönetimi için Kurum Hizmetleri sekmesini kullanın.", "info")
                else:
                    _render_randevu_tab(store, student, auth_user)
                try:
                    from utils.ui_common import goruntulu_gorusme_randevu as _ggr_34
                    _ggr_34()
                except Exception:
                    pass

        # ══════════════════════════════════════════════════════════════
        # GRUP 7: PROGRAM & KAYNAK (4 alt sekme — STEAM eklendi)
        # ══════════════════════════════════════════════════════════════
        with g7_program:
            _g7_t1, _g7_t2, _g7_t3, _g7_t4 = st.tabs([
                "  🗓️ Ders Programı  ",
                "  📚 Dijital Kütüphane  ",
                "  🌐 Yabancı Dil  ",
                "  🔬 STEAM Merkezi  ",
            ])
            with _g7_t1:
                _render_ders_programi_tab(store, student)
            with _g7_t2:
                _render_dk_embed()
                try:
                    from utils.ui_common import kisisel_icerik_onerisi as _kio_34
                    _kio_34(seviye="Ortaokul")
                except Exception:
                    pass
            with _g7_t3:
                from views.yabanci_dil import render_veli_english_tab
                render_veli_english_tab(student.sinif, student.sube)
            with _g7_t4:
                _render_stem_merkezi_tab(student, role="veli")

        # ══════════════════════════════════════════════════════════════
        # GRUP 8: SOSYAL & HIZMET (4 alt sekme)
        # ══════════════════════════════════════════════════════════════
        with g8_sosyal:
            _g8_t1, _g8_t2, _g8_t3, _g8_t4 = st.tabs([
                "  🎉 Etkinlik & Duyurular  ",
                "  🍽️ Yemek Menüsü  ",
                "  🚌 Servis Takibi  ",
                "  📊 Memnuniyet Anketi  ",
            ])
            with _g8_t1:
                _render_etkinlik_duyuru_tab(student)
            with _g8_t2:
                _render_yemek_menusu_tab()
            with _g8_t3:
                _render_servis_tab(student)
            with _g8_t4:
                if is_preview:
                    styled_info_banner("Önizleme modunda anket doldurulamaz. Anket sonuclari için Kurumsal Organizasyon modulundeki Veli Memnuniyet sekmesini kullanin.", "info")
                else:
                    _render_memnuniyet_anketi_tab(student, auth_user)

        # ══════════════════════════════════════════════════════════════
        # GRUP 9: BILGI & AI (3 alt sekme)
        # ══════════════════════════════════════════════════════════════
        with g9_bilgi:
            _g9_t1, _g9_t2, _g9_t3 = st.tabs([
                "  💡 Günün Bilgisi  ",
                "  🤖 Smarti AI  ",
                "  📋 Modül Raporu  ",
            ])
            with _g9_t1:
                _render_gunun_bilgisi_tab()
            with _g9_t2:
                _render_smarti_tab(auth_user, role="Veli")
            with _g9_t3:
                try:
                    from views.modul_gorev_atama import render_veli_modul_raporu
                    render_veli_modul_raporu(student_id=student.id, student_name=student.tam_ad)
                except Exception as _e:
                    st.info(f"Modül Raporu yüklenemedi: {_e}")


# ===================== VELİ — SINIF KADRO KÜNYE =====================

def _render_sinif_kadro_kunye(store, student):
    """Veli panelinde sınıf kadrosu bilgilerini gösterir."""
    from models.akademik_takip import SinifKadro
    from utils.shared_data import normalize_sinif, KADEME_SINIFLAR

    kadro = store.get_sinif_kadro_for_student(student)
    if not kadro:
        return

    sinif_n = normalize_sinif(str(student.sinif))
    is_ilk = sinif_n in (KADEME_SINIFLAR.get("Anaokulu", []) + KADEME_SINIFLAR.get("Ilkokul", []))

    items = []
    if is_ilk:
        if kadro.sinif_ogretmeni_adi:
            items.append(("Sınıf Öğretmeni", kadro.sinif_ogretmeni_adi, "#2563eb", "👩‍🏫"))
    else:
        if kadro.sinif_danisman_adi:
            items.append(("Danışman Öğrt.", kadro.sinif_danisman_adi, "#2563eb", "👩‍🏫"))

    if kadro.rehber_ogretmen_adi:
        items.append(("Rehber Öğrt.", kadro.rehber_ogretmen_adi, "#7c3aed", "🧑‍⚕️"))
    if kadro.mudur_yardimcisi_adi:
        items.append(("Müdür Yrd.", kadro.mudur_yardimcisi_adi, "#f59e0b", "👔"))
    if kadro.mudur_adi:
        items.append(("Müdür", kadro.mudur_adi, "#059669", "🏫"))

    if items:
        styled_stat_row(items)


def _get_kadro_role_label(kadro, teacher_id: str) -> str:
    """Kadrodaki öğretmenin rol etiketini döndür."""
    roles = []
    if teacher_id == kadro.sinif_ogretmeni_id:
        roles.append("Sınıf Öğretmeni")
    if teacher_id == kadro.sinif_danisman_id:
        roles.append("Danışman Öğretmen")
    if teacher_id == kadro.rehber_ogretmen_id:
        roles.append("Rehber Öğretmen")
    if teacher_id == kadro.mudur_yardimcisi_id:
        roles.append("Müdür Yardımcısı")
    if teacher_id == kadro.mudur_id:
        roles.append("Müdür")
    return ", ".join(roles) if roles else "Öğretmen"


# ===================== VELİ — BELGELER & LİNKLER =====================

def _render_veli_belgeler_tab(store, student):
    """Veli panelinde öğretmenin gönderdiği belge ve linkleri göster."""
    import os
    from models.akademik_takip import OgretmenBelge, BELGE_KATEGORILER
    from utils.shared_data import normalize_sinif

    styled_section("Belgeler & Linkler", "#2563eb")

    sinif_n = normalize_sinif(str(student.sinif))
    sube = student.sube or ""

    belgeler = store.get_ogretmen_belgeleri(sinif=sinif_n, sube=sube)
    belgeler.sort(key=lambda b: b.tarih, reverse=True)

    if not belgeler:
        styled_info_banner("Henüz paylaşılan belge veya link bulunmuyor.", "info")
        return

    kat_map = dict(BELGE_KATEGORILER)
    _dosya_cnt = sum(len(b.dosyalar) for b in belgeler if b.dosyalar)
    _link_cnt = sum(len(b.linkler) for b in belgeler if b.linkler)
    _son_tarih = belgeler[0].tarih if belgeler else "-"

    styled_stat_row([
        ("Paylaşım", str(len(belgeler)), "#2563eb", "📎"),
        ("Dosya", str(_dosya_cnt), "#7c3aed", "📄"),
        ("Link", str(_link_cnt), "#0ea5e9", "🔗"),
        ("Son", _son_tarih, "#10b981", "📅"),
    ])

    # Kategori filtresi
    tum_kategoriler = sorted({b.kategori for b in belgeler})
    kat_secenekler = ["Tümü"] + [kat_map.get(k, k) for k in tum_kategoriler]
    secili_kat = st.selectbox("Kategori Filtresi", kat_secenekler, key="veli_belge_kat_filtre")

    if secili_kat != "Tümü":
        ters_kat = {v: k for k, v in kat_map.items()}
        kat_key = ters_kat.get(secili_kat, secili_kat)
        belgeler = [b for b in belgeler if b.kategori == kat_key]

    if not belgeler:
        st.info("Bu kategoride paylaşılan belge yok.")
        return

    st.caption(f"Toplam {len(belgeler)} paylaşım")

    for b in belgeler:
        kat_label = kat_map.get(b.kategori, b.kategori)
        dosya_count = len(b.dosyalar) if b.dosyalar else 0
        link_count = len(b.linkler) if b.linkler else 0

        # Kategori renkleri
        kat_renk = {
            "duyuru": "#dc2626", "bilgi": "#2563eb", "etkinlik": "#7c3aed",
            "odev": "#d97706", "velibilgi": "#059669", "diger": "#6b7280",
        }
        badge_bg = kat_renk.get(b.kategori, "#6b7280")

        st.markdown(
            f'<div style="background:linear-gradient(135deg,#111827,#eef2ff);'
            f'border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin-bottom:12px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
            f'<span style="font-size:1.05rem;font-weight:700;color:#475569;">📌 {b.baslik}</span>'
            f'<span style="background:{badge_bg};color:#fff;padding:2px 10px;border-radius:20px;'
            f'font-size:0.75rem;font-weight:600;">{kat_label}</span>'
            f'</div>'
            f'<div style="font-size:0.82rem;color:#64748b;margin-bottom:6px;">'
            f'📅 {b.tarih}  •  👩‍🏫 {b.ogretmen_adi}  •  📎 {dosya_count} dosya  •  🔗 {link_count} link'
            f'</div>'
            + (f'<div style="font-size:0.9rem;color:#334155;margin-top:6px;">{b.aciklama}</div>' if b.aciklama else '')
            + f'</div>',
            unsafe_allow_html=True,
        )

        # Dosyalar — indirme butonları
        if b.dosyalar:
            cols = st.columns(min(len(b.dosyalar), 4))
            for idx, d in enumerate(b.dosyalar):
                dosya_yolu = d.get("dosya_yolu", "")
                with cols[idx % len(cols)]:
                    if os.path.exists(dosya_yolu):
                        with open(dosya_yolu, "rb") as fp:
                            st.download_button(
                                f"📥 {d['dosya_adi']}",
                                data=fp.read(),
                                file_name=d["dosya_adi"],
                                key=f"vdl_{b.id}_{idx}",
                            )
                    else:
                        st.caption(f"⚠️ {d['dosya_adi']} — dosya bulunamadı")

        # Linkler — tıklanabilir
        if b.linkler:
            for lnk in b.linkler:
                link_baslik = lnk.get("baslik", lnk["url"])
                st.markdown(f"🔗 [{link_baslik}]({lnk['url']})")

        st.markdown("")


# ===================== ANASINIFI VELİ BÜLTEN GÖRÜNÜMÜ =====================

def _render_veli_gunluk_bulten(store, student, auth_user):
    """Veli panelinde anasınıfı günlük bülten görünümü — premium kurumsal tasarım."""
    from datetime import date, timedelta
    from models.akademik_takip import (
        GunlukBulten, BULTEN_ETKINLIKLER, BULTEN_BESLENME,
        BULTEN_DUYGU, BULTEN_ARKADAS, BULTEN_KURALLAR,
        BULTEN_AYRILIK, BULTEN_TUVALET, BULTEN_UYKU,
        BULTEN_TESLIM, BULTEN_EVDE,
    )

    styled_section("📋 Günlük Bülten — Okulumda Bugün", "#7c3aed")

    # Tarih seçici
    tc1, tc2 = st.columns([1, 3])
    with tc1:
        secili_tarih = st.date_input("Tarih", value=date.today(), key="veli_blt_tarih")
    tarih_str = secili_tarih.strftime("%Y-%m-%d")

    bultenler = store.get_gunluk_bultenler(student_id=student.id, tarih=tarih_str)

    if not bultenler:
        gun_adi = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][secili_tarih.weekday()]
        st.warning(f"📋 {secili_tarih.strftime('%d.%m.%Y')} ({gun_adi}) için henüz bülten girilmemiş. "
                   "Öğretmeniniz bülteni girince burada görüntülenecektir.")

        # Son bültenleri göster
        son_7 = store.get_gunluk_bultenler(student_id=student.id)
        son_7.sort(key=lambda b: b.tarih, reverse=True)
        if son_7:
            st.caption(f"Son bülten: {son_7[0].tarih}")
        return

    blt = bultenler[0]
    gun_adi = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][secili_tarih.weekday()]

    # ---- LABEL HELPER'LAR ----
    etk_map = dict(BULTEN_ETKINLIKLER)
    bes_map = dict(BULTEN_BESLENME)
    duygu_map = dict(BULTEN_DUYGU)
    ark_map = dict(BULTEN_ARKADAS)
    kur_map = dict(BULTEN_KURALLAR)
    ayr_map = dict(BULTEN_AYRILIK)
    tuv_map = dict(BULTEN_TUVALET)
    uyku_map = dict(BULTEN_UYKU)
    teslim_map = dict(BULTEN_TESLIM)
    evde_map = dict(BULTEN_EVDE)

    # ---- YEMEK MENÜSÜ (Kurum Hizmetlerinden) ----
    menuler = _load_veli_json(YEMEK_MENU_DOSYA)
    bugun_menu = next((m for m in menuler if m.get("tarih") == tarih_str), None)

    # ---- REVİR KAYITLARI ----
    try:
        sstore = _get_saglik_store()
        revir_ziyaretler = sstore.find_by_field("revir_ziyaretleri", "ogrenci_id", student.id)
        bugun_revir = [z for z in revir_ziyaretler
                       if getattr(z, "basvuru_tarihi", "") == tarih_str]
    except Exception:
        bugun_revir = []

    # ---- KURUM BİLGİSİ ----
    try:
        from utils.shared_data import load_kurum_profili
        kurum = load_kurum_profili()
        kurum_adi = kurum.get("kurum_adi", "Smart Campus") if kurum else "Smart Campus"
    except Exception:
        kurum_adi = "Smart Campus"

    # ---- RENK & İKON HELPER'LAR ----
    def _bes_renk(val):
        if val == "hepsini_yedi": return "#22c55e"
        if val == "bir_kismini": return "#f59e0b"
        if val == "yemedi": return "#ef4444"
        return "#94a3b8"

    def _bes_icon(val):
        if val == "hepsini_yedi": return "✅"
        if val == "bir_kismini": return "🟡"
        if val == "yemedi": return "❌"
        return "⬜"

    def _duygu_renk(val):
        r = {"cok_mutlu":"#22c55e","mutlu":"#4ade80","normal":"#f59e0b","keyifsiz":"#f97316","uzgun":"#ef4444"}
        return r.get(val, "#94a3b8")

    def _sosyal_renk(val):
        r = {"cok_iyi":"#22c55e","iyi":"#4ade80","gelisiyor":"#f59e0b","zorlaniyor":"#ef4444",
             "hatirlatildi":"#f59e0b","zorlandi":"#ef4444","rahat":"#22c55e","kisa_sure":"#f59e0b"}
        return r.get(val, "#94a3b8")

    # Etkinlik ikonları
    etk_ikon_map = {
        "serbest_oyun": "🎲", "bahce_park": "🌳", "drama": "🎭", "kum_su": "🏖️",
        "blok_insa": "🧱", "sanat": "🎨", "muzik": "🎵", "kutuphane": "📚",
        "bilim_deney": "🔬", "degerler": "💝", "ince_motor": "✂️", "kaba_motor": "🤸",
        "turkce_dil": "🗣️", "zeka_oyun": "🧩", "ingilizce": "🌍",
    }
    # Eski key'ler için fallback (geriye uyumluluk)
    _fallback_ikon = {"oyun_saati": "🎲", "matematik": "🔢", "okuma_yazma": "✏️",
                      "kodlama": "🤖", "fen_doga": "🌿", "beden_egitimi": "⚽",
                      "bahce": "🌳", "blok": "🧱", "hikaye": "📚", "deney": "🔬",
                      "dil": "🗣️", "zeka": "🧩"}
    etk_ikon_map.update(_fallback_ikon)

    # ---- ETKİNLİK BADGE'LERİ ----
    etk_badges = ""
    etk_colors = ["#7c3aed", "#2563eb", "#059669", "#d97706", "#dc2626",
                  "#0891b2", "#4f46e5", "#be185d", "#65a30d", "#ea580c",
                  "#7c3aed", "#0284c7", "#c026d3", "#0d9488", "#b91c1c"]
    for idx_e, e in enumerate((blt.etkinlikler or [])):
        lbl = etk_map.get(e, e)
        ikon = etk_ikon_map.get(e, "📌")
        color = etk_colors[idx_e % len(etk_colors)]
        etk_badges += (
            f"<span style='display:inline-block;background:linear-gradient(135deg,{color}11,{color}22);"
            f"color:{color};padding:6px 14px;border-radius:20px;margin:3px 4px;font-size:0.82rem;"
            f"font-weight:600;border:1.5px solid {color}44'>{ikon} {lbl}</span>")
    if not etk_badges:
        etk_badges = "<span style='color:#475569;font-style:italic'>Etkinlik bilgisi girilmemiş</span>"

    # ---- YEMEK MENÜSÜ HTML ----
    menu_html = ""
    if bugun_menu:
        # Yeni format: kahvalti/ogle_yemegi/ikindi_ara_ogun veya eski format: yemekler
        if "kahvalti" in bugun_menu or "ogle_yemegi" in bugun_menu:
            kah_list = bugun_menu.get("kahvalti", [])
            ogle_list = bugun_menu.get("ogle_yemegi", [])
            ik_list = bugun_menu.get("ikindi_ara_ogun", [])
        else:
            kah_list = []
            ogle_list = bugun_menu.get("yemekler", [])
            ik_list = []

        def _menu_items(items, renk, baslik, ikon):
            if not items:
                return ""
            yemek_satirlar = "".join(
                f'<div style="font-size:0.82rem;color:#334155;padding:2px 0">• {y}</div>'
                for y in items)
            return (
                f'<div style="flex:1;min-width:160px;background:#fff;border-radius:10px;'
                f'padding:12px;border-top:3px solid {renk}">'
                f'<div style="font-size:0.75rem;font-weight:700;color:{renk};'
                f'margin-bottom:6px">{ikon} {baslik}</div>'
                f'{yemek_satirlar}</div>')

        menu_parts = []
        if kah_list:
            menu_parts.append(_menu_items(kah_list, "#92400e", "KAHVALTI", "☕"))
        if ogle_list:
            menu_parts.append(_menu_items(ogle_list, "#166534", "ÖĞLE YEMEĞİ", "🍽️"))
        if ik_list:
            menu_parts.append(_menu_items(ik_list, "#9a3412", "İKİNDİ", "🍎"))

        if menu_parts:
            menu_html = (
                '<div style="background:linear-gradient(135deg,#fefce8,#fef9c3);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #fde68a">'
                '<div style="font-weight:700;color:#92400e;margin-bottom:10px;font-size:0.92rem">'
                '🍴 Günün Yemek Menüsü</div>'
                '<div style="display:flex;gap:10px;flex-wrap:wrap">'
                + "".join(menu_parts) +
                '</div></div>')

    # ---- REVİR HTML ----
    revir_html = ""
    if bugun_revir:
        revir_items = ""
        for z in bugun_revir:
            saat = getattr(z, "basvuru_saati", "") or ""
            sikayet = getattr(z, "sikayet", "-") or "-"
            mudahale = getattr(z, "mudahale", "") or "Belirtilmedi"
            sonuc = getattr(z, "sonuc", "-") or "-"
            revir_items += (
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-top:6px;border-left:3px solid #ef4444">'
                f'<div style="font-size:0.82rem;color:#475569">'
                f'<b>Saat:</b> {saat} &nbsp;|&nbsp; <b>Şikâyet:</b> {sikayet}</div>'
                f'<div style="font-size:0.8rem;color:#64748b;margin-top:4px">'
                f'<b>Müdahale:</b> {mudahale} &nbsp;|&nbsp; <b>Sonuç:</b> {sonuc}</div>'
                f'</div>')
        revir_html = (
            '<div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #fca5a5">'
            '<div style="font-weight:700;color:#dc2626;margin-bottom:6px;font-size:0.92rem">'
            '🏥 Revir Kaydı</div>' + revir_items + '</div>')

    # ---- ÖNE ÇIKAN & ÜRÜN ----
    beceri_text = getattr(blt, 'one_cikan_beceri', '') or ''
    urun_text = getattr(blt, 'bugun_urun', '') or ''
    kazanim_html = ""
    if beceri_text or urun_text:
        kparts = ""
        if beceri_text:
            kparts += (
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-bottom:6px;border-left:3px solid #7c3aed">'
                f'<div style="font-size:0.75rem;color:#7c3aed;font-weight:600">⭐ Öne Çıkan Kazanım / Beceri</div>'
                f'<div style="font-size:0.85rem;color:#475569;margin-top:4px">{beceri_text}</div>'
                f'</div>')
        if urun_text:
            kparts += (
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'border-left:3px solid #059669">'
                f'<div style="font-size:0.75rem;color:#059669;font-weight:600">🎨 Bugün Yaptığım Ürün / Çalışma</div>'
                f'<div style="font-size:0.85rem;color:#475569;margin-top:4px">{urun_text}</div>'
                f'</div>')
        kazanim_html = kparts

    # ---- SAĞLIK NOTU HTML ----
    saglik_html = ""
    if blt.saglik_notu:
        saglik_html = (
            f'<div style="margin-top:8px;background:#fff;padding:8px 12px;border-radius:8px;'
            f'font-size:0.82rem;border-left:3px solid #f59e0b">'
            f'<b>Sağlık Notu:</b> {blt.saglik_notu}</div>')
    kaza_html = ""
    if blt.kaza_notu:
        kaza_html = (
            f'<div style="margin-top:6px;background:#fff;padding:8px 12px;border-radius:8px;'
            f'font-size:0.82rem;border-left:3px solid #ef4444">'
            f'<b>Kaza / Yaralanma:</b> {blt.kaza_notu}</div>')

    # ---- ÖĞRETMEN NOTU HTML ----
    ogretmen_html = ""
    if blt.ogretmen_notu:
        ogretmen_html = (
            '<div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #93c5fd">'
            '<div style="font-weight:700;color:#1d4ed8;margin-bottom:8px;font-size:0.92rem">'
            '📝 Öğretmen Notu</div>'
            f'<div style="font-size:0.88rem;color:#475569;line-height:1.6">{blt.ogretmen_notu}</div>'
            '</div>')

    # ── YENI ALANLAR HTML ──
    # Akil & Gelisim
    akademik_html = ""
    _bg_o = getattr(blt, 'bugun_ogrendigi', '') or ''
    _bg_b = getattr(blt, 'bugun_basari', '') or ''
    _yh = getattr(blt, 'yarin_hazirlik', '') or ''
    if _bg_o or _bg_b or _yh:
        _items = []
        if _bg_o:
            _items.append(
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-bottom:6px;border-left:3px solid #0d9488">'
                f'<div style="font-size:0.75rem;color:#0d9488;font-weight:700">'
                f'🎯 Bugün Öğrendiği Yeni Şey</div>'
                f'<div style="font-size:0.85rem;color:#0f172a;margin-top:4px">{_bg_o}</div></div>')
        if _bg_b:
            _items.append(
                f'<div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);'
                f'border-radius:8px;padding:10px 12px;margin-bottom:6px;'
                f'border-left:3px solid #f59e0b">'
                f'<div style="font-size:0.75rem;color:#92400e;font-weight:700">'
                f'🌟 Bugünkü Başarısı</div>'
                f'<div style="font-size:0.88rem;color:#0f172a;margin-top:4px;font-weight:600">{_bg_b}</div>'
                f'<div style="font-size:0.7rem;color:#92400e;margin-top:4px;font-style:italic">'
                f'✨ Aile Başarı Duvarı\'nda kaydedildi</div></div>')
        if _yh:
            _items.append(
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-bottom:6px;border-left:3px solid #2563eb">'
                f'<div style="font-size:0.75rem;color:#2563eb;font-weight:700">'
                f'📚 Yarın için Hazırlık</div>'
                f'<div style="font-size:0.85rem;color:#0f172a;margin-top:4px">{_yh}</div></div>')
        akademik_html = (
            '<div style="background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #6ee7b7">'
            '<div style="font-weight:700;color:#047857;margin-bottom:8px;font-size:0.92rem">'
            '🎯 Akademik & Gelişim</div>' + "".join(_items) + '</div>')

    # Canta kontrolu
    canta_html = ""
    _ck = getattr(blt, 'canta_kontrolu', []) or []
    if _ck:
        try:
            from models.akademik_takip import CANTA_KONTROL
            _ck_map = dict(CANTA_KONTROL)
            _ck_badges = "".join(
                f'<span style="display:inline-block;background:#fff;border:1px solid #cbd5e1;'
                f'border-radius:12px;padding:4px 12px;margin:3px 4px;font-size:0.78rem;'
                f'color:#0f172a;font-weight:600">{_ck_map.get(k, k)}</span>'
                for k in _ck
            )
        except Exception:
            _ck_badges = ""
        if _ck_badges:
            canta_html = (
                '<div style="background:linear-gradient(135deg,#f1f5f9,#e2e8f0);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #cbd5e1">'
                '<div style="font-weight:700;color:#475569;margin-bottom:8px;font-size:0.92rem">'
                '🎒 Çıkış Çanta Kontrolü</div>'
                f'<div>{_ck_badges}</div></div>')

    # Multimedya — fotograf & video
    media_html = ""
    _fotos = getattr(blt, 'foto_yollari', []) or []
    _video = getattr(blt, 'video_yolu', '') or ''
    if _fotos or _video:
        import os as _os_blt_v
        import base64 as _b64_blt
        _media_parts = []
        for _fp in _fotos[:3]:
            if _fp and _os_blt_v.path.exists(_fp):
                try:
                    with open(_fp, "rb") as _ff:
                        _b64 = _b64_blt.b64encode(_ff.read()).decode()
                    _media_parts.append(
                        f'<img src="data:image/jpeg;base64,{_b64}" '
                        f'style="width:32%;max-height:200px;object-fit:cover;'
                        f'border-radius:10px;border:2px solid #fff;'
                        f'box-shadow:0 4px 12px rgba(0,0,0,0.1);margin:2px"/>')
                except Exception:
                    pass
        media_html_inner = "".join(_media_parts)
        video_html = ""
        if _video and _os_blt_v.path.exists(_video):
            try:
                with open(_video, "rb") as _vf:
                    _vb64 = _b64_blt.b64encode(_vf.read()).decode()
                video_html = (
                    f'<video controls style="width:100%;max-height:300px;border-radius:10px;'
                    f'margin-top:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1)">'
                    f'<source src="data:video/mp4;base64,{_vb64}" type="video/mp4"/>'
                    f'</video>')
            except Exception:
                pass
        if media_html_inner or video_html:
            media_html = (
                '<div style="background:linear-gradient(135deg,#fdf4ff,#fae8ff);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #e9d5ff">'
                '<div style="font-weight:700;color:#7c3aed;margin-bottom:8px;font-size:0.92rem">'
                '📷 Bugünden Anlar</div>'
                + (f'<div style="display:flex;flex-wrap:wrap;gap:4px">{media_html_inner}</div>' if media_html_inner else '')
                + video_html
                + '</div>')

    # Acil & kisisel mesaj
    acil_html = ""
    _kisisel = getattr(blt, 'kisisel_mesaj', '') or ''
    _acil = getattr(blt, 'acil_mi', False)
    if _acil or _kisisel:
        if _acil:
            acil_html += (
                '<div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border-radius:12px;'
                'padding:14px 16px;margin-bottom:8px;border:2px solid #ef4444;'
                'box-shadow:0 4px 16px rgba(239,68,68,0.2);animation:pulse 2s ease-in-out infinite">'
                '<div style="font-weight:800;color:#dc2626;font-size:1rem">'
                '🚨 ACİL MESAJ — Lütfen dikkat!</div></div>')
        if _kisisel:
            acil_html += (
                '<div style="background:linear-gradient(135deg,#fdf4ff,#f3e8ff);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #c4b5fd">'
                '<div style="font-weight:700;color:#7c3aed;margin-bottom:6px;font-size:0.92rem">'
                '⭐ Size Özel Mesaj</div>'
                f'<div style="font-size:0.88rem;color:#0f172a;line-height:1.6;font-style:italic">'
                f'"{_kisisel}"</div></div>')

    # ---- İNGİLİZCE GÜNLÜK ÖZET ----
    _eng_oz = _load_eng_daily_summary(tarih_str, blt.sinif, blt.sube)
    eng_daily_html = _build_eng_daily_html(_eng_oz) if _eng_oz else ""

    # ── Avatar baş harfleri ──
    _ogr_initials = (student.ad[0] if student.ad else "?") + (student.soyad[0] if student.soyad else "?")
    _ogr_initials = _ogr_initials.upper()

    # ================ LIGHT MODERN HTML BÜLTEN ================
    html = f"""
    <div style="font-family:'Inter','Plus Jakarta Sans','Segoe UI',system-ui,-apple-system,sans-serif;
                max-width:820px;margin:0 auto;border-radius:24px;overflow:hidden;
                box-shadow:0 1px 3px rgba(15,23,42,.04),0 12px 40px rgba(99,102,241,.10),
                           0 24px 80px rgba(168,85,247,.06);
                background:#ffffff;
                border:1px solid #e2e8f0">

      <!-- LIGHT MODERN HERO HEADER -->
      <div style="background:linear-gradient(135deg,#ffffff 0%,#f5f3ff 40%,#fef3f2 100%);
                  color:#0f172a;padding:28px 32px;position:relative;overflow:hidden;
                  border-bottom:1px solid #e2e8f0">

        <!-- Soft pastel orbs -->
        <div style="position:absolute;top:-80px;right:-50px;width:240px;height:240px;
                    background:radial-gradient(circle,rgba(236,72,153,.18) 0%,transparent 70%);
                    border-radius:50%;filter:blur(50px);pointer-events:none"></div>
        <div style="position:absolute;bottom:-80px;left:-50px;width:280px;height:280px;
                    background:radial-gradient(circle,rgba(99,102,241,.15) 0%,transparent 70%);
                    border-radius:50%;filter:blur(60px);pointer-events:none"></div>

        <!-- Üst rozet + tarih -->
        <div style="position:relative;z-index:2;display:flex;align-items:center;
                    justify-content:space-between;margin-bottom:18px;gap:12px">
          <div style="background:#ffffff;border:1px solid #c7d2fe;
                      box-shadow:0 1px 3px rgba(99,102,241,.08);
                      border-radius:20px;padding:5px 14px;font-size:.7rem;
                      letter-spacing:1.5px;text-transform:uppercase;font-weight:700;
                      color:#4338ca">
            ✨ {kurum_adi}
          </div>
          <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;
                      padding:8px 16px;text-align:center;
                      box-shadow:0 4px 12px rgba(99,102,241,.10)">
            <div style="font-size:1.5rem;font-weight:900;line-height:1;color:#6366f1;
                        letter-spacing:-1px">
              {secili_tarih.strftime('%d')}
            </div>
            <div style="font-size:.62rem;font-weight:700;letter-spacing:.8px;
                        text-transform:uppercase;color:#475569;margin-top:2px">
              {["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"][secili_tarih.month-1]}
            </div>
          </div>
        </div>

        <!-- Ana başlık -->
        <div style="position:relative;z-index:2">
          <div style="font-size:2rem;font-weight:900;letter-spacing:-1px;line-height:1.1;
                      background:linear-gradient(120deg,#1e1b4b 0%,#6366f1 30%,#ec4899 60%,#f59e0b 100%);
                      -webkit-background-clip:text;background-clip:text;
                      -webkit-text-fill-color:transparent;color:transparent;
                      margin-bottom:6px">
            🌟 OKULUMDA BUGÜN
          </div>
          <div style="font-size:.85rem;color:#64748b;letter-spacing:.3px;font-weight:500">
            Günlük Bülten · {gun_adi}, {secili_tarih.strftime('%d %B %Y').replace(secili_tarih.strftime('%B'), {
              'January':'Ocak','February':'Şubat','March':'Mart','April':'Nisan',
              'May':'Mayıs','June':'Haziran','July':'Temmuz','August':'Ağustos',
              'September':'Eylül','October':'Ekim','November':'Kasım','December':'Aralık'
            }.get(secili_tarih.strftime('%B'), secili_tarih.strftime('%B')))}
          </div>
        </div>

        <!-- Öğrenci kartı + öğretmen -->
        <div style="position:relative;z-index:2;display:flex;align-items:center;gap:16px;
                    margin-top:20px;background:#ffffff;
                    border:1px solid #e2e8f0;
                    box-shadow:0 4px 16px rgba(99,102,241,.08);
                    border-radius:18px;padding:16px 20px">

          <!-- Avatar -->
          <div style="width:64px;height:64px;border-radius:50%;flex-shrink:0;
                      background:linear-gradient(135deg,#fbbf24 0%,#f472b6 50%,#a855f7 100%);
                      display:flex;align-items:center;justify-content:center;
                      color:white;font-weight:900;font-size:1.5rem;
                      box-shadow:0 8px 20px rgba(244,114,182,.35),
                                 inset 0 2px 4px rgba(255,255,255,.3);
                      border:3px solid #ffffff">
            {_ogr_initials}
          </div>

          <!-- Bilgi -->
          <div style="flex:1;min-width:0">
            <div style="font-size:1.25rem;font-weight:800;color:#0f172a;line-height:1.2;
                        margin-bottom:2px">
              {student.tam_ad}
            </div>
            <div style="font-size:.78rem;color:#6366f1;font-weight:700;
                        margin-bottom:6px">
              📚 {blt.sinif} / {blt.sube}
            </div>
            <div style="display:flex;align-items:center;gap:6px;
                        background:#f1f5f9;border:1px solid #e2e8f0;border-radius:10px;
                        padding:4px 10px;width:fit-content">
              <span style="font-size:.7rem">👩‍🏫</span>
              <span style="font-size:.74rem;color:#475569;font-weight:600">
                {blt.ogretmen_adi or 'Öğretmen'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div style="padding:24px 28px 8px 28px">

        <!-- GELİŞ / ÇIKIŞ KARTLARI -->
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#f0fdf4,#dcfce7);
                      padding:14px 16px;border-radius:12px;text-align:center;
                      border:1px solid #bbf7d0">
            <div style="font-size:0.7rem;color:#16a34a;font-weight:700;letter-spacing:0.5px">🕐 GELİŞ</div>
            <div style="font-size:1.2rem;font-weight:800;color:#166534;margin-top:4px">{blt.gelis_saati or '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#fef2f2,#fee2e2);
                      padding:14px 16px;border-radius:12px;text-align:center;
                      border:1px solid #fecaca">
            <div style="font-size:0.7rem;color:#dc2626;font-weight:700;letter-spacing:0.5px">🕐 ÇIKIŞ</div>
            <div style="font-size:1.2rem;font-weight:800;color:#991b1b;margin-top:4px">{blt.cikis_saati or '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                      padding:14px 16px;border-radius:12px;text-align:center;
                      border:1px solid #bfdbfe">
            <div style="font-size:0.7rem;color:#2563eb;font-weight:700;letter-spacing:0.5px">🚌 SERVİS</div>
            <div style="font-size:1.2rem;font-weight:800;color:#1e40af;margin-top:4px">{'Var' if blt.servis == 'var' else 'Yok' if blt.servis == 'yok' else '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#fdf4ff,#f3e8ff);
                      padding:14px 16px;border-radius:12px;text-align:center;
                      border:1px solid #e9d5ff">
            <div style="font-size:0.7rem;color:#7c3aed;font-weight:700;letter-spacing:0.5px">👤 TESLİM</div>
            <div style="font-size:1.2rem;font-weight:800;color:#5b21b6;margin-top:4px">{teslim_map.get(blt.teslim_eden, '—')}</div>
          </div>
        </div>

        <!-- YEMEK MENÜSÜ -->
        {menu_html}

        <!-- BESLENME DURUMU -->
        <div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #bbf7d0">
          <div style="font-weight:700;color:#166534;margin-bottom:10px;font-size:0.92rem">
            🍽️ Beslenme Durumu</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:150px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {_bes_renk(blt.kahvalti)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.72rem;color:#64748b;font-weight:600">☕ Kahvaltı</div>
              <div style="font-weight:700;font-size:0.95rem;margin-top:4px">
                {_bes_icon(blt.kahvalti)} {bes_map.get(blt.kahvalti, '—')}</div>
              {'<div style="font-size:0.72rem;color:#64748b;margin-top:3px;font-style:italic">'+blt.kahvalti_not+'</div>' if blt.kahvalti_not else ''}
            </div>
            <div style="flex:1;min-width:150px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {_bes_renk(blt.ogle)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.72rem;color:#64748b;font-weight:600">🍽️ Öğle</div>
              <div style="font-weight:700;font-size:0.95rem;margin-top:4px">
                {_bes_icon(blt.ogle)} {bes_map.get(blt.ogle, '—')}</div>
              {'<div style="font-size:0.72rem;color:#64748b;margin-top:3px;font-style:italic">'+blt.ogle_not+'</div>' if blt.ogle_not else ''}
            </div>
            <div style="flex:1;min-width:150px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {_bes_renk(blt.ikindi)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.72rem;color:#64748b;font-weight:600">🍎 İkindi</div>
              <div style="font-weight:700;font-size:0.95rem;margin-top:4px">
                {_bes_icon(blt.ikindi)} {bes_map.get(blt.ikindi, '—')}</div>
              {'<div style="font-size:0.72rem;color:#64748b;margin-top:3px;font-style:italic">'+blt.ikindi_not+'</div>' if blt.ikindi_not else ''}
            </div>
          </div>
        </div>

        <!-- GÜNLÜK ETKİNLİKLER & ÖĞRENME -->
        <div style="background:linear-gradient(135deg,#fdf4ff,#faf5ff);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #e9d5ff">
          <div style="font-weight:700;color:#7c3aed;margin-bottom:10px;font-size:0.92rem">
            🎨 Günlük Etkinlikler & Öğrenme</div>
          <div style="display:flex;flex-wrap:wrap;gap:2px">{etk_badges}</div>
          {kazanim_html}
        </div>

        <!-- REVİR -->
        {revir_html}

        <!-- DUYGU DURUMU & SOSYAL UYUM -->
        <div style="background:linear-gradient(135deg,#fef2f2,#fff1f2);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #fecaca">
          <div style="font-weight:700;color:#be123c;margin-bottom:10px;font-size:0.92rem">
            😊 Duygu & Sosyal Uyum</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:135px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_duygu_renk(blt.duygu)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Duygu Durumu</div>
              <div style="font-weight:700;margin-top:4px">{duygu_map.get(blt.duygu, '—')}</div>
            </div>
            <div style="flex:1;min-width:135px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_sosyal_renk(blt.arkadas_iliskisi)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Arkadaş İlişkisi</div>
              <div style="font-weight:700;margin-top:4px">{ark_map.get(blt.arkadas_iliskisi, '—')}</div>
            </div>
            <div style="flex:1;min-width:135px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_sosyal_renk(blt.sinif_kurallari)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Sınıf Kuralları</div>
              <div style="font-weight:700;margin-top:4px">{kur_map.get(blt.sinif_kurallari, '—')}</div>
            </div>
            <div style="flex:1;min-width:135px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_sosyal_renk(blt.ayrilik_uyumu)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Ayrılık Uyumu</div>
              <div style="font-weight:700;margin-top:4px">{ayr_map.get(blt.ayrilik_uyumu, '—')}</div>
            </div>
          </div>
        </div>

        <!-- SAĞLIK, UYKU & ÖZ BAKIM -->
        <div style="background:linear-gradient(135deg,#ecfeff,#e0f2fe);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #a5f3fc">
          <div style="font-weight:700;color:#0e7490;margin-bottom:10px;font-size:0.92rem">
            🏥 Sağlık, Uyku & Öz Bakım</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:150px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">🚽 Tuvalet</div>
              <div style="font-weight:700;margin-top:4px">{tuv_map.get(blt.tuvalet, '—')}</div>
            </div>
            <div style="flex:1;min-width:150px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">😴 Uyku</div>
              <div style="font-weight:700;margin-top:4px">{uyku_map.get(blt.uyku_durumu, '—')}</div>
              <div style="font-size:0.75rem;color:#64748b;margin-top:2px">{blt.uyku_suresi} dk {'(' + blt.uyku_baslangic + ' - ' + blt.uyku_bitis + ')' if blt.uyku_baslangic else ''}</div>
            </div>
          </div>
          {saglik_html}
          {kaza_html}
        </div>

        <!-- ACIL & KISISEL MESAJ (YENI - en ust onceliik) -->
        {acil_html}

        <!-- AKADEMIK & GELISIM (YENI) -->
        {akademik_html}

        <!-- MULTIMEDYA - FOTO & VIDEO (YENI) -->
        {media_html}

        <!-- CANTA KONTROLU (YENI) -->
        {canta_html}

        <!-- ÖĞRETMEN NOTU -->
        {ogretmen_html}

        <!-- İNGİLİZCE GÜNLÜK ÖZET -->
        {eng_daily_html}

        <!-- FOOTER -->
        <div style="text-align:center;padding-top:10px;border-top:1px solid #e5e7eb;
                    margin-top:8px">
          <div style="font-size:0.7rem;color:#475569">
            {kurum_adi} — Günlük Bülten Sistemi | {secili_tarih.strftime('%d.%m.%Y')}
          </div>
        </div>

      </div>
    </div>
    """

    st.html(html)

    # ---- EVDE BÖLÜMÜ (Veli doldurur) ----
    st.markdown("---")
    styled_section("🏠 Evde — Veli Geri Bildirimi", "#059669")
    st.caption("Çocuğunuzun evdeki aktivitelerini işaretleyin, öğretmenine iletilecektir.")

    evde_defaults = blt.evde_kontrol or []
    evde_keys = [k for k, _ in BULTEN_EVDE]
    evde_labels = [v for _, v in BULTEN_EVDE]
    default_idxs = [i for i, k in enumerate(evde_keys) if k in evde_defaults]
    secili_evde = st.multiselect("Evde Yapılanlar", range(len(evde_keys)),
                                  default=default_idxs,
                                  format_func=lambda i: evde_labels[i],
                                  key="veli_blt_evde")
    veli_notu = st.text_area("Veli Notu", value=blt.veli_notu, height=60,
                              key="veli_blt_not")

    if st.button("💾 Kaydet", type="primary", key="veli_blt_evde_kaydet"):
        blt.evde_kontrol = [evde_keys[i] for i in secili_evde]
        blt.veli_notu = veli_notu
        store.save_gunluk_bulten(blt)
        st.success("✅ Evde bilgileri kaydedildi!")

    # ---- PDF İNDİR ----
    st.markdown("---")
    pdf_bytes = _generate_bulten_pdf(blt, student)
    st.download_button(
        label="📥 Bülten PDF İndir",
        data=pdf_bytes,
        file_name=f"bulten_{student.numara}_{blt.tarih}.pdf",
        mime="application/pdf",
        key="veli_blt_pdf_dl"
    )

    # ---- GEÇMİŞ BÜLTENLERİ ----
    with st.expander("📅 Geçmiş Bültenler"):
        gecmis = store.get_gunluk_bultenler(student_id=student.id)
        gecmis.sort(key=lambda b: b.tarih, reverse=True)
        gecmis = [b for b in gecmis if b.tarih != tarih_str][:10]
        if not gecmis:
            st.info("Geçmiş bülten bulunamadı.")
        else:
            for gb in gecmis:
                d_map = dict(BULTEN_DUYGU)
                st.markdown(f"**{gb.tarih}** — {d_map.get(gb.duygu, '-')} | "
                           f"Öğretmen: {gb.ogretmen_adi or '-'}")


def _generate_bulten_pdf(blt, student) -> bytes:
    """Anasınıfı günlük bülten PDF oluşturur."""
    try:
        from utils.report_utils import ReportPDFGenerator
    except ImportError:
        return b"ReportPDFGenerator bulunamadi"

    from models.akademik_takip import (
        BULTEN_ETKINLIKLER, BULTEN_BESLENME, BULTEN_DUYGU,
        BULTEN_ARKADAS, BULTEN_KURALLAR, BULTEN_AYRILIK,
        BULTEN_TUVALET, BULTEN_UYKU, BULTEN_TESLIM, BULTEN_EVDE,
    )

    etk_map = dict(BULTEN_ETKINLIKLER)
    bes_map = dict(BULTEN_BESLENME)
    duygu_map = dict(BULTEN_DUYGU)
    ark_map = dict(BULTEN_ARKADAS)
    kur_map = dict(BULTEN_KURALLAR)
    ayr_map = dict(BULTEN_AYRILIK)
    tuv_map = dict(BULTEN_TUVALET)
    uyku_map = dict(BULTEN_UYKU)
    teslim_map = dict(BULTEN_TESLIM)
    evde_map = dict(BULTEN_EVDE)

    pdf = ReportPDFGenerator(f"OKULUMDA BUGUN — {student.tam_ad}")
    pdf.add_header(f"OKULUMDA BUGUN — {student.tam_ad}")
    pdf.add_text(f"Tarih: {blt.tarih} | Sinif: {blt.sinif}/{blt.sube} | Öğretmen: {blt.ogretmen_adi}")
    pdf.add_spacer(0.3)

    # Geliş/Çıkış
    pdf.add_section("Gelis / Cikis Bilgileri", color="#2563eb")
    pdf.add_table(pd.DataFrame([{
        "Gelis": blt.gelis_saati or "-",
        "Cikis": blt.cikis_saati or "-",
        "Servis": "Var" if blt.servis == "var" else ("Yok" if blt.servis == "yok" else "-"),
        "Teslim Eden": teslim_map.get(blt.teslim_eden, "-"),
    }]))

    # Beslenme
    pdf.add_section("Beslenme", color="#059669")
    pdf.add_table(pd.DataFrame([
        {"Ogun": "Kahvalti", "Durum": bes_map.get(blt.kahvalti, "-"), "Not": blt.kahvalti_not or "-"},
        {"Ogun": "Ogle", "Durum": bes_map.get(blt.ogle, "-"), "Not": blt.ogle_not or "-"},
        {"Ogun": "Ikindi", "Durum": bes_map.get(blt.ikindi, "-"), "Not": blt.ikindi_not or "-"},
    ]))

    # Etkinlikler
    pdf.add_section("Oyun & Etkinlikler", color="#d97706")
    etk_str = ", ".join([etk_map.get(e, e) for e in (blt.etkinlikler or [])]) or "-"
    pdf.add_text(f"Yapilan: {etk_str}")
    if blt.one_cikan_beceri:
        pdf.add_text(f"One cikan beceri: {blt.one_cikan_beceri}")
    if getattr(blt, 'bugun_urun', ''):
        pdf.add_text(f"Bugun yaptigim urun / calisma: {blt.bugun_urun}")

    # Duygu
    pdf.add_section("Duygu Durumu & Sosyal Uyum", color="#dc2626")
    pdf.add_table(pd.DataFrame([{
        "Duygu": duygu_map.get(blt.duygu, "-"),
        "Arkadas": ark_map.get(blt.arkadas_iliskisi, "-"),
        "Kurallar": kur_map.get(blt.sinif_kurallari, "-"),
        "Ayrilik": ayr_map.get(blt.ayrilik_uyumu, "-"),
    }]))

    # Sağlık
    pdf.add_section("Sağlık, Uyku & Öz Bakım", color="#0891b2")
    pdf.add_table(pd.DataFrame([{
        "Tuvalet": tuv_map.get(blt.tuvalet, "-"),
        "Uyku": uyku_map.get(blt.uyku_durumu, "-"),
        "Sure (dk)": str(blt.uyku_suresi),
        "Saat": f"{blt.uyku_baslangic}-{blt.uyku_bitis}" if blt.uyku_baslangic else "-",
    }]))
    if blt.saglik_notu:
        pdf.add_text(f"Sağlık: {blt.saglik_notu}")
    if blt.kaza_notu:
        pdf.add_text(f"Kaza: {blt.kaza_notu}")

    # Öğretmen notu
    if blt.ogretmen_notu:
        pdf.add_section("Öğretmen Notu", color="#4338ca")
        pdf.add_text(blt.ogretmen_notu)

    # Evde
    if blt.evde_kontrol:
        pdf.add_section("Evde (Veli Geri Bildirimi)", color="#059669")
        evde_str = ", ".join([evde_map.get(e, e) for e in blt.evde_kontrol])
        pdf.add_text(evde_str)
        if blt.veli_notu:
            pdf.add_text(f"Veli notu: {blt.veli_notu}")

    return pdf.generate()


# ===================== İLKOKUL VELİ GÜNLÜK RAPOR GÖRÜNÜMÜ =====================

def _render_veli_ilkokul_gunluk_rapor(store, student, auth_user):
    """Veli panelinde ilkokul (1-4) günlük rapor görünümü + evde bölümü."""
    from datetime import date
    from models.akademik_takip import (
        IlkokulGunlukRapor, ILKOKUL_DERSLER, ILKOKUL_DEVAM, ILKOKUL_KATILIM,
        ILKOKUL_DIKKAT, ILKOKUL_SORUMLULUK, ILKOKUL_EVDE,
        BULTEN_BESLENME, BULTEN_TESLIM, BULTEN_ARKADAS, BULTEN_KURALLAR,
    )

    styled_section("📋 Günlük Rapor — İlkokul İletişim Formu", "#2563eb")

    # Tarih seçici
    tc1, tc2 = st.columns([1, 3])
    with tc1:
        secili_tarih = st.date_input("Tarih", value=date.today(), key="veli_igr_tarih")
    tarih_str = secili_tarih.strftime("%Y-%m-%d")

    raporlar = store.get_ilkokul_gunluk_raporlar(student_id=student.id, tarih=tarih_str)

    if not raporlar:
        gun_adi = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][secili_tarih.weekday()]
        st.warning(f"📋 {secili_tarih.strftime('%d.%m.%Y')} ({gun_adi}) için henüz rapor girilmemiş. "
                   "Öğretmeniniz raporu girince burada görüntülenecektir.")
        # Son raporları göster
        son = store.get_ilkokul_gunluk_raporlar(student_id=student.id)
        son.sort(key=lambda r: r.tarih, reverse=True)
        if son:
            st.caption(f"Son rapor: {son[0].tarih}")
        return

    rap = raporlar[0]
    gun_adi = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"][secili_tarih.weekday()]

    # ---- LABEL HELPERS ----
    ders_map = dict(ILKOKUL_DERSLER)
    devam_map = dict(ILKOKUL_DEVAM)
    katilim_map = dict(ILKOKUL_KATILIM)
    dikkat_map = dict(ILKOKUL_DIKKAT)
    bes_map = dict(BULTEN_BESLENME)
    teslim_map = dict(BULTEN_TESLIM)
    ark_map = dict(BULTEN_ARKADAS)
    kur_map = dict(BULTEN_KURALLAR)
    sorumluluk_map = dict(ILKOKUL_SORUMLULUK)
    evde_map = dict(ILKOKUL_EVDE)

    # Renk yardımcıları
    def _bes_renk(val):
        if val == "hepsini_yedi": return "#22c55e"
        if val == "bir_kismini": return "#f59e0b"
        if val == "yemedi": return "#ef4444"
        return "#94a3b8"

    def _bes_icon(val):
        if val == "hepsini_yedi": return "✅"
        if val == "bir_kismini": return "🟡"
        if val == "yemedi": return "❌"
        return "⬜"

    def _perf_renk(val):
        r = {"cok_iyi":"#22c55e","iyi":"#4ade80","orta":"#f59e0b","dusuk":"#ef4444",
             "zorlandi":"#ef4444","gelisiyor":"#f59e0b","zorlaniyor":"#ef4444",
             "hatirlatildi":"#f59e0b"}
        return r.get(val, "#94a3b8")

    # İşlenen dersler badges
    ders_badges = ""
    for d in (rap.islenen_dersler or []):
        lbl = ders_map.get(d, d)
        ders_badges += (f"<span style='display:inline-block;background:#eff6ff;color:#2563eb;"
                       f"padding:3px 10px;border-radius:12px;margin:2px 3px;font-size:0.78rem;"
                       f"font-weight:600'>{lbl}</span>")
    if not ders_badges:
        ders_badges = "<span style='color:#475569'>—</span>"

    # Devam durumu ikonu
    devam_icon = {"tam":"✅","gec_kaldi":"⏰","erken_cikti":"🔙","izinli":"📋"}.get(rap.devam, "⬜")
    devam_renk = {"tam":"#22c55e","gec_kaldi":"#f59e0b","erken_cikti":"#f97316","izinli":"#3b82f6"}.get(rap.devam, "#94a3b8")

    # ---- KURUM BİLGİSİ ----
    try:
        from utils.shared_data import load_kurum_profili
        kurum = load_kurum_profili()
        kurum_adi = kurum.get("kurum_adi", "Smart Campus") if kurum else "Smart Campus"
    except Exception:
        kurum_adi = "Smart Campus"

    # ---- YEMEK MENÜSÜ ----
    menuler = _load_veli_json(YEMEK_MENU_DOSYA)
    bugun_menu = next((m for m in menuler if m.get("tarih") == tarih_str), None)
    menu_html = ""
    if bugun_menu:
        if "kahvalti" in bugun_menu or "ogle_yemegi" in bugun_menu:
            ogle_list = bugun_menu.get("ogle_yemegi", [])
        else:
            ogle_list = bugun_menu.get("yemekler", [])
        if ogle_list:
            yemek_items = "".join(
                f'<span style="display:inline-block;background:#fff;border:1px solid #fde68a;'
                f'border-radius:8px;padding:4px 12px;margin:3px 4px;font-size:0.82rem;'
                f'color:#92400e;font-weight:500">🍽️ {y}</span>' for y in ogle_list)
            menu_html = (
                '<div style="background:linear-gradient(135deg,#fefce8,#fef9c3);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #fde68a">'
                '<div style="font-weight:700;color:#92400e;margin-bottom:8px;font-size:0.92rem">'
                '🍴 Günün Yemek Menüsü</div>'
                f'<div style="display:flex;flex-wrap:wrap;gap:2px">{yemek_items}</div>'
                '</div>')

    # ---- REVİR KAYITLARI ----
    try:
        sstore = _get_saglik_store()
        revir_ziyaretler = sstore.find_by_field("revir_ziyaretleri", "ogrenci_id", student.id)
        bugun_revir = [z for z in revir_ziyaretler
                       if getattr(z, "basvuru_tarihi", "") == tarih_str]
    except Exception:
        bugun_revir = []
    revir_html = ""
    if bugun_revir:
        revir_items = ""
        for z in bugun_revir:
            saat = getattr(z, "basvuru_saati", "") or ""
            sikayet = getattr(z, "sikayet", "-") or "-"
            mudahale = getattr(z, "mudahale", "") or "Belirtilmedi"
            sonuc = getattr(z, "sonuc", "-") or "-"
            revir_items += (
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-top:6px;border-left:3px solid #ef4444">'
                f'<div style="font-size:0.82rem;color:#475569">'
                f'<b>Saat:</b> {saat} &nbsp;|&nbsp; <b>Şikâyet:</b> {sikayet}</div>'
                f'<div style="font-size:0.8rem;color:#64748b;margin-top:4px">'
                f'<b>Müdahale:</b> {mudahale} &nbsp;|&nbsp; <b>Sonuç:</b> {sonuc}</div>'
                f'</div>')
        revir_html = (
            '<div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #fca5a5">'
            '<div style="font-weight:700;color:#dc2626;margin-bottom:6px;font-size:0.92rem">'
            '🏥 Revir Kaydı</div>' + revir_items + '</div>')

    # Ders badge'leri (renkli)
    ders_ikon_map = {
        "turkce": "📖", "matematik": "🔢", "hayat_bilgisi": "🌍", "fen_bilimleri": "🔬",
        "sosyal_bilgiler": "🏛️", "ingilizce": "🌐", "din_kulturu": "☪️",
        "beden_egitimi": "⚽", "gorsel_sanatlar": "🎨", "muzik": "🎵",
    }
    ders_renk_map = {
        "turkce": "#2563eb", "matematik": "#7c3aed", "hayat_bilgisi": "#059669",
        "fen_bilimleri": "#0891b2", "sosyal_bilgiler": "#d97706", "ingilizce": "#dc2626",
        "din_kulturu": "#4f46e5", "beden_egitimi": "#16a34a", "gorsel_sanatlar": "#be185d",
        "muzik": "#ea580c",
    }
    ders_badges = ""
    for d in (rap.islenen_dersler or []):
        lbl = ders_map.get(d, d)
        ikon = ders_ikon_map.get(d, "📌")
        color = ders_renk_map.get(d, "#64748b")
        ders_badges += (
            f"<span style='display:inline-block;background:linear-gradient(135deg,{color}11,{color}22);"
            f"color:{color};padding:6px 14px;border-radius:20px;margin:3px 4px;font-size:0.82rem;"
            f"font-weight:600;border:1.5px solid {color}44'>{ikon} {lbl}</span>")
    if not ders_badges:
        ders_badges = "<span style='color:#475569;font-style:italic'>Ders bilgisi girilmemiş</span>"

    # Öne çıkan konu
    konu_html = ""
    if rap.one_cikan_konu:
        konu_html = (
            f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
            f'margin-top:8px;border-left:3px solid #7c3aed">'
            f'<div style="font-size:0.75rem;color:#7c3aed;font-weight:600">⭐ Öne Çıkan Konu</div>'
            f'<div style="font-size:0.85rem;color:#475569;margin-top:4px">{rap.one_cikan_konu}</div>'
            f'</div>')

    # Beslenme notu
    beslenme_not_html = ""
    if rap.beslenme_not:
        beslenme_not_html = (
            f'<div style="margin-top:8px;background:#fff;padding:8px 12px;border-radius:8px;'
            f'font-size:0.82rem;border-left:3px solid #f59e0b">'
            f'<b>Not:</b> {rap.beslenme_not}</div>')

    # Ödev açıklama
    odev_aciklama_html = ""
    if rap.odev_aciklama:
        odev_aciklama_html = (
            f'<div style="margin-top:8px;background:#fff;padding:8px 12px;border-radius:8px;'
            f'font-size:0.82rem;border-left:3px solid #f59e0b">'
            f'<b>Ödev açıklaması:</b> {rap.odev_aciklama}</div>')

    # Davranış notu
    davranis_not_html = ""
    if rap.davranis_notu:
        davranis_not_html = (
            f'<div style="margin-top:8px;background:#fff;padding:8px 12px;border-radius:8px;'
            f'font-size:0.82rem;border-left:3px solid #f59e0b">'
            f'<b>Not:</b> {rap.davranis_notu}</div>')

    # Öğretmen notu
    ogretmen_html = ""
    if rap.ogretmen_notu:
        ogretmen_html = (
            '<div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #93c5fd">'
            '<div style="font-weight:700;color:#1d4ed8;margin-bottom:8px;font-size:0.92rem">'
            '✏️ Öğretmen Notu</div>'
            f'<div style="font-size:0.88rem;color:#475569;line-height:1.6">{rap.ogretmen_notu}</div>'
            '</div>')

    # ── YENI ALANLAR HTML (ilkokul) ──
    # Akademik & Gelisim
    akademik_html = ""
    _bg_o_i = getattr(rap, 'bugun_ogrendigi', '') or ''
    _bg_b_i = getattr(rap, 'bugun_basari', '') or ''
    _yh_i = getattr(rap, 'yarin_hazirlik', '') or ''
    if _bg_o_i or _bg_b_i or _yh_i:
        _items_i = []
        if _bg_o_i:
            _items_i.append(
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-bottom:6px;border-left:3px solid #0d9488">'
                f'<div style="font-size:0.75rem;color:#0d9488;font-weight:700">'
                f'🎯 Bugün Öğrendiği Yeni Şey</div>'
                f'<div style="font-size:0.85rem;color:#0f172a;margin-top:4px">{_bg_o_i}</div></div>')
        if _bg_b_i:
            _items_i.append(
                f'<div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);'
                f'border-radius:8px;padding:10px 12px;margin-bottom:6px;'
                f'border-left:3px solid #f59e0b">'
                f'<div style="font-size:0.75rem;color:#92400e;font-weight:700">'
                f'🌟 Bugünkü Başarısı</div>'
                f'<div style="font-size:0.88rem;color:#0f172a;margin-top:4px;font-weight:600">{_bg_b_i}</div>'
                f'<div style="font-size:0.7rem;color:#92400e;margin-top:4px;font-style:italic">'
                f'✨ Aile Başarı Duvarı\'nda kaydedildi</div></div>')
        if _yh_i:
            _items_i.append(
                f'<div style="background:#fff;border-radius:8px;padding:10px 12px;'
                f'margin-bottom:6px;border-left:3px solid #2563eb">'
                f'<div style="font-size:0.75rem;color:#2563eb;font-weight:700">'
                f'📚 Yarın için Hazırlık</div>'
                f'<div style="font-size:0.85rem;color:#0f172a;margin-top:4px">{_yh_i}</div></div>')
        akademik_html = (
            '<div style="background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-radius:12px;'
            'padding:14px 16px;margin-bottom:14px;border:1.5px solid #6ee7b7">'
            '<div style="font-weight:700;color:#047857;margin-bottom:8px;font-size:0.92rem">'
            '🎯 Akademik & Gelişim</div>' + "".join(_items_i) + '</div>')

    # Canta kontrolu
    canta_html = ""
    _ck_i = getattr(rap, 'canta_kontrolu', []) or []
    if _ck_i:
        try:
            from models.akademik_takip import CANTA_KONTROL
            _ck_map_i = dict(CANTA_KONTROL)
            _ck_badges_i = "".join(
                f'<span style="display:inline-block;background:#fff;border:1px solid #cbd5e1;'
                f'border-radius:12px;padding:4px 12px;margin:3px 4px;font-size:0.78rem;'
                f'color:#0f172a;font-weight:600">{_ck_map_i.get(k, k)}</span>'
                for k in _ck_i
            )
        except Exception:
            _ck_badges_i = ""
        if _ck_badges_i:
            canta_html = (
                '<div style="background:linear-gradient(135deg,#f1f5f9,#e2e8f0);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #cbd5e1">'
                '<div style="font-weight:700;color:#475569;margin-bottom:8px;font-size:0.92rem">'
                '🎒 Çıkış Çanta Kontrolü</div>'
                f'<div>{_ck_badges_i}</div></div>')

    # Multimedya
    media_html = ""
    _fotos_i = getattr(rap, 'foto_yollari', []) or []
    _video_i = getattr(rap, 'video_yolu', '') or ''
    if _fotos_i or _video_i:
        import os as _os_igr_v
        import base64 as _b64_igr
        _media_parts_i = []
        for _fp in _fotos_i[:3]:
            if _fp and _os_igr_v.path.exists(_fp):
                try:
                    with open(_fp, "rb") as _ff:
                        _b64 = _b64_igr.b64encode(_ff.read()).decode()
                    _media_parts_i.append(
                        f'<img src="data:image/jpeg;base64,{_b64}" '
                        f'style="width:32%;max-height:200px;object-fit:cover;'
                        f'border-radius:10px;border:2px solid #fff;'
                        f'box-shadow:0 4px 12px rgba(0,0,0,0.1);margin:2px"/>')
                except Exception:
                    pass
        media_html_inner_i = "".join(_media_parts_i)
        video_html_i = ""
        if _video_i and _os_igr_v.path.exists(_video_i):
            try:
                with open(_video_i, "rb") as _vf:
                    _vb64 = _b64_igr.b64encode(_vf.read()).decode()
                video_html_i = (
                    f'<video controls style="width:100%;max-height:300px;border-radius:10px;'
                    f'margin-top:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1)">'
                    f'<source src="data:video/mp4;base64,{_vb64}" type="video/mp4"/>'
                    f'</video>')
            except Exception:
                pass
        if media_html_inner_i or video_html_i:
            media_html = (
                '<div style="background:linear-gradient(135deg,#fdf4ff,#fae8ff);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #e9d5ff">'
                '<div style="font-weight:700;color:#7c3aed;margin-bottom:8px;font-size:0.92rem">'
                '📷 Bugünden Anlar</div>'
                + (f'<div style="display:flex;flex-wrap:wrap;gap:4px">{media_html_inner_i}</div>' if media_html_inner_i else '')
                + video_html_i
                + '</div>')

    # Acil & kisisel mesaj
    acil_html = ""
    _kisisel_i = getattr(rap, 'kisisel_mesaj', '') or ''
    _acil_i = getattr(rap, 'acil_mi', False)
    if _acil_i or _kisisel_i:
        if _acil_i:
            acil_html += (
                '<div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border-radius:12px;'
                'padding:14px 16px;margin-bottom:8px;border:2px solid #ef4444;'
                'box-shadow:0 4px 16px rgba(239,68,68,0.2)">'
                '<div style="font-weight:800;color:#dc2626;font-size:1rem">'
                '🚨 ACİL MESAJ — Lütfen dikkat!</div></div>')
        if _kisisel_i:
            acil_html += (
                '<div style="background:linear-gradient(135deg,#fdf4ff,#f3e8ff);border-radius:12px;'
                'padding:14px 16px;margin-bottom:14px;border:1.5px solid #c4b5fd">'
                '<div style="font-weight:700;color:#7c3aed;margin-bottom:6px;font-size:0.92rem">'
                '⭐ Size Özel Mesaj</div>'
                f'<div style="font-size:0.88rem;color:#0f172a;line-height:1.6;font-style:italic">'
                f'"{_kisisel_i}"</div></div>')

    # ---- İNGİLİZCE GÜNLÜK ÖZET ----
    _eng_oz_i = _load_eng_daily_summary(tarih_str, rap.sinif, rap.sube)
    eng_daily_html = _build_eng_daily_html(_eng_oz_i) if _eng_oz_i else ""

    html = f"""
    <div style="font-family:'Segoe UI',system-ui,-apple-system,sans-serif;max-width:760px;
                margin:0 auto;border-radius:16px;overflow:hidden;
                box-shadow:0 4px 24px rgba(0,0,0,0.08),0 1px 4px rgba(0,0,0,0.04)">

      <!-- KURUMSAL BAŞLIK -->
      <div style="background:linear-gradient(135deg,#0c2461 0%,#1e3a8a 30%,#2563eb 60%,#3b82f6 100%);
                  color:#fff;padding:24px 28px;position:relative;overflow:hidden">
        <div style="position:absolute;top:-30px;right:-30px;width:120px;height:120px;
                    background:rgba(255,255,255,0.05);border-radius:50%"></div>
        <div style="position:absolute;bottom:-20px;left:-20px;width:80px;height:80px;
                    background:rgba(255,255,255,0.03);border-radius:50%"></div>
        <div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;
                    opacity:0.7;margin-bottom:4px">{kurum_adi}</div>
        <div style="font-size:1.3rem;font-weight:800;letter-spacing:0.5px">📋 İLKOKUL GÜNLÜK RAPOR</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;
                    flex-wrap:wrap;gap:8px">
          <div>
            <div style="font-size:1rem;font-weight:700">{student.tam_ad}</div>
            <div style="font-size:0.82rem;opacity:0.85">Sınıf: {rap.sinif} / {rap.sube}</div>
          </div>
          <div style="text-align:right">
            <div style="font-size:0.95rem;font-weight:700">{secili_tarih.strftime('%d.%m.%Y')}</div>
            <div style="font-size:0.82rem;opacity:0.85">{gun_adi}</div>
          </div>
        </div>
        <div style="margin-top:8px;font-size:0.78rem;opacity:0.7;border-top:1px solid rgba(255,255,255,0.15);
                    padding-top:6px">👩‍🏫 Öğretmen: {rap.ogretmen_adi or '-'}</div>
      </div>

      <div style="background:#ffffff;padding:24px 28px">

        <!-- GELİŞ / ÇIKIŞ -->
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#f0fdf4,#dcfce7);
                      padding:14px 16px;border-radius:12px;text-align:center;border:1px solid #bbf7d0">
            <div style="font-size:0.7rem;color:#16a34a;font-weight:700;letter-spacing:0.5px">🕐 GELİŞ</div>
            <div style="font-size:1.2rem;font-weight:800;color:#166534;margin-top:4px">{rap.gelis_saati or '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#fef2f2,#fee2e2);
                      padding:14px 16px;border-radius:12px;text-align:center;border:1px solid #fecaca">
            <div style="font-size:0.7rem;color:#dc2626;font-weight:700;letter-spacing:0.5px">🕐 ÇIKIŞ</div>
            <div style="font-size:1.2rem;font-weight:800;color:#991b1b;margin-top:4px">{rap.cikis_saati or '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#eff6ff,#dbeafe);
                      padding:14px 16px;border-radius:12px;text-align:center;border:1px solid #bfdbfe">
            <div style="font-size:0.7rem;color:#2563eb;font-weight:700;letter-spacing:0.5px">🚌 SERVİS</div>
            <div style="font-size:1.2rem;font-weight:800;color:#1e40af;margin-top:4px">{'Var' if rap.servis == 'var' else 'Yok' if rap.servis == 'yok' else '—'}</div>
          </div>
          <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#fdf4ff,#f3e8ff);
                      padding:14px 16px;border-radius:12px;text-align:center;border:1px solid #e9d5ff">
            <div style="font-size:0.7rem;color:#7c3aed;font-weight:700;letter-spacing:0.5px">👤 TESLİM</div>
            <div style="font-size:1.2rem;font-weight:800;color:#5b21b6;margin-top:4px">{teslim_map.get(rap.teslim_eden, '—')}</div>
          </div>
        </div>

        <!-- YEMEK MENÜSÜ -->
        {menu_html}

        <!-- DEVAM & KATILIM -->
        <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #bfdbfe">
          <div style="font-weight:700;color:#1d4ed8;margin-bottom:10px;font-size:0.92rem">
            📊 Devam & Ders Katılımı</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {devam_renk};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Devam</div>
              <div style="font-weight:700;margin-top:4px">{devam_icon} {devam_map.get(rap.devam, '—')}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {_perf_renk(rap.katilim)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Katılım</div>
              <div style="font-weight:700;margin-top:4px">{katilim_map.get(rap.katilim, '—')}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {_perf_renk(rap.dikkat)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Dikkat</div>
              <div style="font-weight:700;margin-top:4px">{dikkat_map.get(rap.dikkat, '—')}</div>
            </div>
          </div>
        </div>

        <!-- BESLENME -->
        <div style="background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #bbf7d0">
          <div style="font-weight:700;color:#166534;margin-bottom:10px;font-size:0.92rem">
            🍽️ Beslenme Durumu</div>
          <div style="background:#fff;border-radius:10px;padding:14px;text-align:center;
                      border-left:4px solid {_bes_renk(rap.beslenme)};
                      box-shadow:0 1px 3px rgba(0,0,0,0.05)">
            <div style="font-weight:700;font-size:1.1rem">
              {_bes_icon(rap.beslenme)} {bes_map.get(rap.beslenme, '—')}</div>
          </div>
          {beslenme_not_html}
        </div>

        <!-- İŞLENEN DERSLER -->
        <div style="background:linear-gradient(135deg,#fdf4ff,#faf5ff);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #e9d5ff">
          <div style="font-weight:700;color:#7c3aed;margin-bottom:10px;font-size:0.92rem">
            📚 Bugün İşlenen Dersler</div>
          <div style="display:flex;flex-wrap:wrap;gap:2px">{ders_badges}</div>
          {konu_html}
        </div>

        <!-- REVİR -->
        {revir_html}

        <!-- ÖDEV & OKUMA TAKİBİ -->
        <div style="background:linear-gradient(135deg,#fff7ed,#ffedd5);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #fed7aa">
          <div style="font-weight:700;color:#c2410c;margin-bottom:10px;font-size:0.92rem">
            📝 Ödev & Okuma Takibi</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {'#2563eb' if rap.odev_durumu == 'verildi' else '#94a3b8'};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Ödev Durumu</div>
              <div style="font-weight:700;margin-top:4px">{'📋 Verildi' if rap.odev_durumu == 'verildi' else '— Yok'}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid {'#22c55e' if rap.odev_teslim == 'tam' else '#f59e0b' if rap.odev_teslim == 'eksik' else '#94a3b8'};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Teslim</div>
              <div style="font-weight:700;margin-top:4px">{'✅ Tam' if rap.odev_teslim == 'tam' else '⚠️ Eksik' if rap.odev_teslim == 'eksik' else '—'}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:12px;
                        text-align:center;border-left:4px solid #3b82f6;
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">📖 Okuma</div>
              <div style="font-weight:700;margin-top:4px">{rap.okuma_suresi} dk</div>
              {'<div style="font-size:0.72rem;color:#64748b">'+rap.kitap_adi+'</div>' if rap.kitap_adi else ''}
            </div>
          </div>
          {odev_aciklama_html}
        </div>

        <!-- DAVRANIŞ & SOSYAL GELİŞİM -->
        <div style="background:linear-gradient(135deg,#fef2f2,#fff1f2);border-radius:12px;
                    padding:14px 16px;margin-bottom:14px;border:1.5px solid #fecaca">
          <div style="font-weight:700;color:#be123c;margin-bottom:10px;font-size:0.92rem">
            🤝 Davranış & Sosyal Gelişim</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap">
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_perf_renk(rap.sinif_kurallari)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Sınıf Kuralları</div>
              <div style="font-weight:700;margin-top:4px">{kur_map.get(rap.sinif_kurallari, '—')}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_perf_renk(rap.arkadas_iliskisi)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Arkadaş İlişkisi</div>
              <div style="font-weight:700;margin-top:4px">{ark_map.get(rap.arkadas_iliskisi, '—')}</div>
            </div>
            <div style="flex:1;min-width:140px;background:#fff;border-radius:10px;padding:10px;
                        text-align:center;border-left:4px solid {_perf_renk(rap.sorumluluk)};
                        box-shadow:0 1px 3px rgba(0,0,0,0.05)">
              <div style="font-size:0.7rem;color:#64748b;font-weight:600">Sorumluluk</div>
              <div style="font-weight:700;margin-top:4px">{sorumluluk_map.get(rap.sorumluluk, '—')}</div>
            </div>
          </div>
          {davranis_not_html}
        </div>

        <!-- ACIL & KISISEL MESAJ (YENI) -->
        {acil_html}

        <!-- AKADEMIK & GELISIM (YENI) -->
        {akademik_html}

        <!-- MULTIMEDYA - FOTO & VIDEO (YENI) -->
        {media_html}

        <!-- CANTA KONTROLU (YENI) -->
        {canta_html}

        <!-- ÖĞRETMEN NOTU -->
        {ogretmen_html}

        <!-- İNGİLİZCE GÜNLÜK ÖZET -->
        {eng_daily_html}

        <!-- FOOTER -->
        <div style="text-align:center;padding-top:10px;border-top:1px solid #e5e7eb;margin-top:8px">
          <div style="font-size:0.7rem;color:#475569">
            {kurum_adi} — İlkokul Günlük Rapor Sistemi | {secili_tarih.strftime('%d.%m.%Y')}
          </div>
        </div>

      </div>
    </div>
    """

    st.html(html)

    # ---- 7) EVDE BÖLÜMÜ (Veli doldurur) ----
    st.markdown("---")
    styled_section("🏠 Evde — Veli Geri Bildirimi", "#059669")
    st.caption("Çocuğunuzun evdeki aktivitelerini işaretleyin, öğretmenine iletilecektir.")

    evde_defaults = rap.evde_kontrol or []
    evde_keys = [k for k, _ in ILKOKUL_EVDE]
    evde_labels = [v for _, v in ILKOKUL_EVDE]
    default_idxs = [i for i, k in enumerate(evde_keys) if k in evde_defaults]
    secili_evde = st.multiselect("Evde Yapılanlar", range(len(evde_keys)),
                                  default=default_idxs,
                                  format_func=lambda i: evde_labels[i],
                                  key="veli_igr_evde")
    aile_notu = st.text_area("Aile Notu", value=rap.aile_notu, height=60,
                              key="veli_igr_not")

    if st.button("💾 Kaydet", type="primary", key="veli_igr_evde_kaydet"):
        rap.evde_kontrol = [evde_keys[i] for i in secili_evde]
        rap.aile_notu = aile_notu
        store.save_ilkokul_gunluk_rapor(rap)
        st.success("✅ Evde bilgileri kaydedildi!")

    # ---- PDF İNDİR ----
    st.markdown("---")
    pdf_bytes = _generate_ilkokul_rapor_pdf(rap, student)
    st.download_button(
        label="📥 Rapor PDF İndir",
        data=pdf_bytes,
        file_name=f"ilkokul_rapor_{student.numara}_{rap.tarih}.pdf",
        mime="application/pdf",
        key="veli_igr_pdf_dl"
    )

    # ---- GEÇMİŞ RAPORLAR ----
    with st.expander("📅 Geçmiş Raporlar"):
        gecmis = store.get_ilkokul_gunluk_raporlar(student_id=student.id)
        gecmis.sort(key=lambda r: r.tarih, reverse=True)
        gecmis = [r for r in gecmis if r.tarih != tarih_str][:10]
        if not gecmis:
            st.info("Geçmiş rapor bulunamadı.")
        else:
            for gr in gecmis:
                devam_lbl = devam_map.get(gr.devam, '-')
                katilim_lbl = katilim_map.get(gr.katilim, '-')
                st.markdown(f"**{gr.tarih}** — Devam: {devam_lbl} | Katılım: {katilim_lbl} | "
                           f"Öğretmen: {gr.ogretmen_adi or '-'}")


def _generate_ilkokul_rapor_pdf(rap, student) -> bytes:
    """İlkokul günlük rapor PDF oluşturur."""
    try:
        from utils.report_utils import ReportPDFGenerator
    except ImportError:
        return b"ReportPDFGenerator bulunamadi"

    from models.akademik_takip import (
        ILKOKUL_DERSLER, ILKOKUL_DEVAM, ILKOKUL_KATILIM,
        ILKOKUL_DIKKAT, ILKOKUL_SORUMLULUK, ILKOKUL_EVDE,
        BULTEN_BESLENME, BULTEN_TESLIM, BULTEN_ARKADAS, BULTEN_KURALLAR,
    )

    ders_map = dict(ILKOKUL_DERSLER)
    devam_map = dict(ILKOKUL_DEVAM)
    katilim_map = dict(ILKOKUL_KATILIM)
    dikkat_map = dict(ILKOKUL_DIKKAT)
    bes_map = dict(BULTEN_BESLENME)
    teslim_map = dict(BULTEN_TESLIM)
    ark_map = dict(BULTEN_ARKADAS)
    kur_map = dict(BULTEN_KURALLAR)
    sorumluluk_map = dict(ILKOKUL_SORUMLULUK)
    evde_map = dict(ILKOKUL_EVDE)

    pdf = ReportPDFGenerator(f"ILKOKUL GUNLUK RAPOR — {student.tam_ad}")
    pdf.add_header(f"ILKOKUL GUNLUK RAPOR — {student.tam_ad}")
    pdf.add_text(f"Tarih: {rap.tarih} | Sinif: {rap.sinif}/{rap.sube} | Öğretmen: {rap.ogretmen_adi}")
    pdf.add_spacer(0.3)

    # Geliş/Çıkış
    pdf.add_section("Gelis / Cikis Bilgileri", color="#2563eb")
    pdf.add_table(pd.DataFrame([{
        "Gelis": rap.gelis_saati or "-",
        "Cikis": rap.cikis_saati or "-",
        "Servis": "Var" if rap.servis == "var" else ("Yok" if rap.servis == "yok" else "-"),
        "Teslim Eden": teslim_map.get(rap.teslim_eden, "-"),
    }]))

    # Devam & Katılım
    pdf.add_section("Devam & Ders Katilimi", color="#1d4ed8")
    pdf.add_table(pd.DataFrame([{
        "Devam": devam_map.get(rap.devam, "-"),
        "Katilim": katilim_map.get(rap.katilim, "-"),
        "Dikkat": dikkat_map.get(rap.dikkat, "-"),
    }]))

    # Beslenme
    pdf.add_section("Beslenme", color="#059669")
    pdf.add_table(pd.DataFrame([{
        "Durum": bes_map.get(rap.beslenme, "-"),
        "Not": rap.beslenme_not or "-",
    }]))

    # İşlenen Dersler
    pdf.add_section("Bugun Islenen Dersler", color="#7c3aed")
    ders_str = ", ".join([ders_map.get(d, d) for d in (rap.islenen_dersler or [])]) or "-"
    pdf.add_text(f"Dersler: {ders_str}")
    if rap.one_cikan_konu:
        pdf.add_text(f"One cikan konu: {rap.one_cikan_konu}")

    # Ödev & Okuma
    pdf.add_section("Odev & Okuma Takibi", color="#c2410c")
    pdf.add_table(pd.DataFrame([{
        "Odev": "Verildi" if rap.odev_durumu == "verildi" else "Yok",
        "Teslim": "Tam" if rap.odev_teslim == "tam" else ("Eksik" if rap.odev_teslim == "eksik" else "-"),
        "Aciklama": rap.odev_aciklama or "-",
        "Okuma (dk)": str(rap.okuma_suresi),
        "Kitap": rap.kitap_adi or "-",
    }]))

    # Davranış & Sosyal
    pdf.add_section("Davranis & Sosyal Gelisim", color="#dc2626")
    pdf.add_table(pd.DataFrame([{
        "Sinif Kurallari": kur_map.get(rap.sinif_kurallari, "-"),
        "Arkadas Iliskisi": ark_map.get(rap.arkadas_iliskisi, "-"),
        "Sorumluluk": sorumluluk_map.get(rap.sorumluluk, "-"),
    }]))
    if rap.davranis_notu:
        pdf.add_text(f"Not: {rap.davranis_notu}")

    # Öğretmen notu
    if rap.ogretmen_notu:
        pdf.add_section("Öğretmen Notu", color="#4338ca")
        pdf.add_text(rap.ogretmen_notu)

    # Evde
    if rap.evde_kontrol:
        pdf.add_section("Evde (Veli Geri Bildirimi)", color="#059669")
        evde_str = ", ".join([evde_map.get(e, e) for e in rap.evde_kontrol])
        pdf.add_text(evde_str)
        if rap.aile_notu:
            pdf.add_text(f"Aile notu: {rap.aile_notu}")

    return pdf.generate()


# ===================== ÖĞRENCİ PANELİ =====================

def render_ogrenci_panel():
    """Ogrenci giris ekrani - tam bilgi paneli."""
    _inject_panel_tab_css()
    styled_header("Öğrenci Paneli", "Akademik bilgileriniz ve odevleriniz", icon="🎓")

    auth_user = AuthManager.get_current_user()
    store = get_akademik_store()
    od = OlcmeDataStore()

    _role = auth_user.get("role", "")
    _is_ogr_preview = _role in ("Yonetici", "Ogretmen", "SuperAdmin", "Öğretmen", "Çalışan")

    if _is_ogr_preview:
        # Önizleme modu — kademe seçimli demo
        styled_info_banner("📋 Önizleme Modu — Öğrenci panelinin yapısını ve sekmelerini inceliyorsunuz.", "info")

        _kademe_map_ogr = {
            "Okul Öncesi": ("ana5", "Anasınıfı"),
            "İlkokul": ("3", "İlkokul"),
            "Ortaokul": ("6", "Ortaokul"),
            "Lise": ("10", "Lise"),
        }
        _prev_kademe_ogr = st.radio(
            "📚 Kademe Önizleme",
            list(_kademe_map_ogr.keys()),
            horizontal=True,
            key="ogr_preview_kademe",
        )
        _prev_sinif_ogr, _ = _kademe_map_ogr[_prev_kademe_ogr]

        # Gerçek öğrenci varsa listele, yoksa demo
        all_stu = store.get_students()
        _sinif_stu = [s for s in all_stu if str(s.sinif) == _prev_sinif_ogr] if all_stu else []

        if _sinif_stu:
            stu_map = {s.id: s for s in _sinif_stu}
            sel_id = st.selectbox(
                "Öğrenci Seçin",
                [s.id for s in _sinif_stu],
                format_func=lambda x: f"{stu_map[x].tam_ad} ({stu_map[x].numara})",
                key="ogr_preview_stu",
            )
            student = stu_map[sel_id]
        else:
            st.caption(f"Demo öğrenci ile {_prev_kademe_ogr} kademesi gösteriliyor.")
            student = Student(
                id="demo_ogr_001", ad="Demo", soyad="Öğrenci",
                sinif=_prev_sinif_ogr, sube="A", numara="001",
                tc_no="00000000000", cinsiyet="Erkek",
                veli_adi="Demo Veli", veli_telefon="05001234567",
            )
    else:
        student = _find_student_for_ogrenci(store, auth_user)

    if not student:
        styled_info_banner("Öğrenci kaydiniz bulunamadı. Lutfen yoneticiyle iletisime gecin.", "warning")
        return

    st.markdown(f"### {student.tam_ad}\n**Sınıf:** {student.sinif}/{student.sube} | **Numara:** {student.numara}")

    # ═══ AKTİF SINAVLARIM — en üstte, tab'lardan önce ═══
    _render_aktif_sinavlar_banner(student)

    st.markdown("---")

    # --- Smarti karsilama + mini sohbet ---
    _render_smarti_top_greeting(auth_user, student)

    # --- MOOD CHECK-IN — gunluk ruh hali (5 saniyede) ---
    try:
        with st.expander("😊 Bugünkü Ruh Halin — 5 saniyede işaretle", expanded=False):
            from views._mood_checkin import render_mood_checkin_student
            render_mood_checkin_student(
                student_id=student.id,
                student_name=f"{student.ad} {student.soyad}",
            )
    except Exception as _mood_err:
        # Mood check-in modülü yüklenemedi — sessizce geç
        pass

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("ogrenci_panel_egitim_yili")

    t1, t_borc_ogr, t_defter_ogr, t2, t3, t3k, t4, t5, t6, t7, t_mat_ogr, t_snt_ogr, t_blsm_ogr, t_stem_ogr, t8, t_dijital_ogrenme_ogr = st.tabs([
        "  📝 Notlarım  ",
        "  📚 Kazanım Borçlarım  ",
        "  📓 Öğrenci Defterim  ",
        "  📅 Devamsızlığım  ", "  📝 Ödevlerim  ",
        "  📖 Kazanım Ödevleri  ",
        "  🎯 KYT Sorulari  ", "  📊 Sınav Sonuclarim  ", "  🔄 Telafi Görevlerim  ",
        "  📚 Dijital Kütüphane",
        "  🏘️ Matematik Köyü  ",
        "  🎨 Sanat Sokağı  ",
        "  💻 Bilişim Vadisi  ",
        "  🔬 STEAM Merkezi  ",
        "  🤖 Smarti AI  ",
        "  🖥️ Dijital Öğrenme  ",
    ])

    with t1:
        styled_section("Notlarım", "#2563eb")
        _render_notlar_tab(store, student)
    with t_borc_ogr:
        _render_borc_tab(store, student, rol="ogrenci")
    with t_defter_ogr:
        from views.ogrenci_defteri import render_ogrenci_defteri_tab
        render_ogrenci_defteri_tab(store, od, student, rol="ogrenci",
                                   akademik_yil=selected_egitim_yili)
    with t2:
        styled_section("Devamsızlık Durumum", "#ef4444")
        _render_devamsizlik_tab(store, student)
    with t3:
        styled_section("Ödevlerim", "#f59e0b")
        _render_odevler_tab(store, student, od)
    with t3k:
        _render_kazanim_odevi_tab(store, od, student)
    with t4:
        styled_section("KYT Soru Cozme", "#10b981")
        _render_kyt_cozme_tab(store, student)
    with t5:
        styled_section("Sınav Sonuclarim", "#7c3aed")
        _render_sinav_sonuclari_tab(od, student)
    with t6:
        styled_section("Telafi Görevlerim", "#dc2626")
        _render_telafi_tab(od, student)
    with t7:
        _render_dk_embed()
    with t_mat_ogr:
        try:
            from views.matematik_dunyasi import render_matematik_dunyasi
            render_matematik_dunyasi()
        except Exception as e:
            st.error(f"Matematik Koyu yuklenemedi: {e}")
    with t_snt_ogr:
        try:
            from views.sanat_sokagi import render_sanat_sokagi
            render_sanat_sokagi()
        except Exception as e:
            st.error(f"Sanat Sokagi yuklenemedi: {e}")
    with t_blsm_ogr:
        try:
            from views.bilisim_vadisi import render_bilisim_vadisi
            render_bilisim_vadisi()
        except Exception as e:
            st.error(f"Bilisim Vadisi yuklenemedi: {e}")
    with t_stem_ogr:
        _render_stem_merkezi_tab(student, role="ogrenci")
    with t8:
        _render_smarti_tab(auth_user, role="Öğrenci")
    with t_dijital_ogrenme_ogr:
        try:
            _render_dijital_ogrenme_tab(store, student)
        except Exception as _e:
            st.info(f"Dijital Öğrenme yüklenemedi: {_e}")

    # Floating Smarti avatar (sag alt kose)
    _render_smarti_floating_avatar()
