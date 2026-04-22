"""
Ana Sayfa - Modül Kartları Paneli
==================================
4 sütunlu kart grid, arama, kullanıcıya özel karşılama,
modüle tek tıkla geçiş.
"""

from __future__ import annotations

import os
import streamlit as st
from datetime import datetime, date
from utils.auth import AuthManager, get_user_modules
from utils.tenant import get_tenant_dir, load_json_list, get_data_path


# ── OTOMATİK MODÜL KART LİSTESİ (app.py'den otomatik oluşturulur) ────────────

def _build_modul_kartlari() -> list[dict]:
    """app.py'deki _MODUL_GRUPLARI'ndan otomatik modül kartları oluşturur.
    Yeni modül eklendiğinde ana sayfa otomatik güncellenir."""
    try:
        from app import _MODUL_GRUPLARI
    except ImportError:
        return []

    # Her modül için renk paleti (döngüsel)
    _RENK_PALETI = [
        "#0d9488", "#2563eb", "#059669", "#7c3aed", "#0e9aa7",
        "#dc2626", "#8b5cf6", "#ea580c", "#6366f1", "#4472C4",
        "#0891b2", "#b91c1c", "#4f46e5", "#e11d48", "#0B0F19",
        "#0369a1", "#7e22ce", "#f59e0b", "#0d9488", "#6366f1",
    ]

    # "Ana Sayfa" hariç tüm modüller
    kartlar = []
    renk_idx = 0
    for grup in _MODUL_GRUPLARI:
        for ad, ikon in grup["moduller"]:
            if ad == "Ana Sayfa":
                continue
            kartlar.append({
                "key": ad,
                "baslik": ad,
                "ikon": ikon,
                "renk": _RENK_PALETI[renk_idx % len(_RENK_PALETI)],
                "menuler": [],  # Sekmeler modül içinden belirlenir
            })
            renk_idx += 1
    return kartlar


def _get_modul_kartlari() -> list[dict]:
    """Modül kartlarını her seferinde güncel oluştur."""
    st.session_state["_ana_sayfa_kartlar"] = _build_modul_kartlari()
    return st.session_state["_ana_sayfa_kartlar"]

# ── CSS ───────────────────────────────────────────────────────────────────────

_DARK_BG     = "#0B0F19"
_DARK_MID    = "#e8ecf1"
_DARK_BOT    = "#e2e8f0"
_DARK_CARD   = "#ffffff"
_DARK_BORDER = "rgba(0,0,0,.08)"


def _css() -> None:
    st.markdown(
        f"""
        <style>
        /* ── SAYFA KOYU ARKA PLAN OVERRIDE ── */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {{
            background: {_DARK_BG} !important;
        }}
        [data-testid="stAppViewContainer"] > .main > .block-container {{
            background: linear-gradient(160deg, {_DARK_BG} 0%, {_DARK_MID} 50%, {_DARK_BOT} 100%) !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            margin: 0 !important;
            max-width: 100% !important;
            padding-top: 1.5rem !important;
        }}
        [data-testid="stHeader"] {{
            background: {_DARK_BG} !important;
        }}

        /* ── STREAMLIT FORMLARI KOYU TEMA ── */
        [data-testid="stTextInput"] input {{
            background: rgba(255,255,255,.06) !important;
            border: 1px solid rgba(37,99,235,.2) !important;
            color: #e2e8f0 !important;
            border-radius: 10px !important;
        }}
        [data-testid="stTextInput"] input::placeholder {{
            color: #64748b !important;
        }}
        [data-testid="stTextInput"] input:focus {{
            border-color: rgba(37,99,235,.5) !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,.15) !important;
        }}
        .stButton > button[kind="secondary"] {{
            background: rgba(37,99,235,.1) !important;
            color: #93c5fd !important;
            border: 1px solid rgba(37,99,235,.2) !important;
        }}
        .stButton > button[kind="secondary"]:hover {{
            background: rgba(37,99,235,.2) !important;
            color: #e2e8f0 !important;
        }}

        /* ── KARŞILAMA BANNER ── */
        .as-welcome {{
            background: linear-gradient(135deg, #131825 0%, #1a2035 50%, #1e2642 100%);
            border-radius: 16px;
            padding: 26px 32px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(37,99,235,.15);
            box-shadow: 0 2px 12px rgba(0,0,0,.2);
        }}
        .as-welcome::before {{
            content: '';
            position: absolute;
            top: -30px; right: -30px;
            width: 120px; height: 120px;
            background: radial-gradient(circle, rgba(37,99,235,.1) 0%, transparent 70%);
            border-radius: 50%;
        }}
        .as-welcome-left   {{ display: flex; align-items: center; gap: 16px; z-index: 1; }}
        .as-welcome-emoji  {{
            font-size: 2.2rem; line-height: 1;
            background: rgba(37,99,235,.15);
            width: 52px; height: 52px;
            border-radius: 14px;
            display: flex; align-items: center; justify-content: center;
        }}
        .as-welcome-title  {{ font-size: 1.4rem; font-weight: 700; color: #f1f5f9; margin: 0; }}
        .as-welcome-sub    {{ font-size: .82rem; color: #94a3b8; margin: 4px 0 0 0; }}
        .as-welcome-date   {{ font-size: .78rem; color: #94a3b8; text-align: right; line-height: 1.6; z-index: 1; }}
        .as-date-day       {{ font-size: 1.1rem; font-weight: 700; color: #e2e8f0; display: block; }}

        /* ── KPI STAT BAR ── */
        .as-kpi-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 18px;
        }}
        .as-kpi-card {{
            flex: 1;
            min-width: 140px;
            background: linear-gradient(135deg, #131825, #1a2035);
            border: 1px solid rgba(37,99,235,.12);
            border-radius: 12px;
            padding: 14px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: transform .18s, box-shadow .18s;
        }}
        .as-kpi-card:hover {{
            transform: translateY(-2px);
            background: linear-gradient(135deg, #1a2035, #1e2642);
            box-shadow: 0 4px 16px rgba(37,99,235,.12);
            border-color: rgba(37,99,235,.25);
        }}
        .as-kpi-icon {{
            width: 40px; height: 40px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
            background: rgba(37,99,235,.12);
        }}
        .as-kpi-value {{ font-size: 1.25rem; font-weight: 800; color: #e2e8f0; line-height: 1; }}
        .as-kpi-label {{ font-size: .68rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: .04em; margin-top: 2px; }}

        /* ── HIZLI ERİŞİM LABEL ── */
        .as-section-label {{
            font-size: .7rem;
            font-weight: 700;
            letter-spacing: .08em;
            color: #94a3b8;
            text-transform: uppercase;
            margin: 4px 0 12px 2px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .as-section-label::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, rgba(148,163,184,.2), transparent);
        }}

        /* ── MODUL KARTI ── */
        .mk-card {{
            background: linear-gradient(135deg, #131825, #1a2035);
            border: 1px solid rgba(37,99,235,.1);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,.2);
            transition: box-shadow .2s ease, transform .2s ease;
        }}
        .mk-card:hover {{
            box-shadow: 0 4px 16px rgba(37,99,235,.15);
            transform: translateY(-3px);
            border-color: rgba(37,99,235,.25);
        }}
        .mk-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 13px 16px 11px 16px;
            position: relative;
        }}
        .mk-icon-box {{
            width: 32px; height: 32px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1rem;
        }}
        .mk-icon  {{ font-size: 1rem; line-height: 1; }}
        .mk-title {{
            font-size: .84rem;
            font-weight: 700;
            letter-spacing: .01em;
            color: #e2e8f0;
            flex: 1;
        }}
        .mk-count {{
            font-size: .62rem;
            background: rgba(37,99,235,.15);
            color: #93c5fd;
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: 600;
        }}
        .mk-divider {{ height: 1px; background: linear-gradient(90deg, transparent, rgba(148,163,184,.15), transparent); margin: 0; }}
        .mk-menu    {{ padding: 5px 0 7px 0; }}
        .mk-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 5px 16px;
            font-size: .78rem;
            color: #94a3b8;
            transition: all .15s ease;
        }}
        .mk-item:hover {{
            background: linear-gradient(90deg, rgba(37,99,235,.08), transparent);
            color: #e2e8f0;
            padding-left: 20px;
        }}
        .mk-chevron {{ color: #64748b; font-size: .6rem; transition: color .15s; }}
        .mk-item:hover .mk-chevron {{ color: #93c5fd; }}
        .mk-more {{
            padding: 3px 16px 5px 16px;
            font-size: .7rem;
            color: #64748b;
            font-style: italic;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ── YARDIMCI ─────────────────────────────────────────────────────────────────

def _tarih_str() -> tuple[str, str]:
    """(gün_adı_tarih, saat) döndürür."""
    gun = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    ay  = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
           "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    now = datetime.now()
    tarih = f"{gun[now.weekday()]}, {now.day} {ay[now.month]} {now.year}"
    saat  = now.strftime("%H:%M")
    return tarih, saat


def _render_kart(kart: dict) -> None:
    """Tek modül kartı — premium HTML liste + Streamlit geçiş butonu."""
    key    = kart["key"]
    baslik = kart["baslik"]
    ikon   = kart["ikon"]
    renk   = kart["renk"]
    menuler = kart["menuler"]

    goruntule = menuler[:6]
    kalan     = len(menuler) - len(goruntule)

    item_html = "".join(
        f'<div class="mk-item"><span>{m}</span><span class="mk-chevron">›</span></div>'
        for m in goruntule
    )
    kalan_html = (
        f'<div class="mk-more">+{kalan} daha...</div>' if kalan > 0 else ""
    )

    st.markdown(
        f"""
        <div class="mk-card">
          <div class="mk-header" style="border-bottom:3px solid {renk};">
            <div class="mk-icon-box" style="background:{renk}15;">
              <span class="mk-icon">{ikon}</span>
            </div>
            <span class="mk-title" style="color:{renk};">{baslik}</span>
            <span class="mk-count">{len(menuler)} sekme</span>
          </div>
          <div class="mk-divider"></div>
          <div class="mk-menu">{item_html}{kalan_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"Modüle Git",
        key=f"as_btn_{key}",
        use_container_width=True,
        type="secondary",
    ):
        st.session_state["_ana_sayfa_git"]  = key
        st.session_state["_sidebar_secim"] = key
        st.rerun()


# ── CANLI VERİ TOPLAMA (TÜM MODÜLLERDEN SENKRON) ─────────────────────────────

def _count_json(path: str) -> int:
    """JSON dosyasındaki kayıt sayısını döndür."""
    items = load_json_list(path)
    return len(items)


def _collect_live_stats() -> dict[str, dict]:
    """Tüm modüllerden anlık istatistikleri topla."""
    td = get_tenant_dir()
    today_str = date.today().isoformat()

    stats: dict[str, dict] = {}

    # --- AKADEMİK TAKİP ---
    stats["Akademik Takip"] = {
        "icon": "📚", "renk": "#2563eb",
        "metrikler": [
            ("Öğrenci", _count_json(get_data_path("akademik", "students.json")), "👨‍🎓"),
            ("Öğretmen", _count_json(get_data_path("akademik", "teachers.json")), "👩‍🏫"),
            ("Not Kaydı", _count_json(get_data_path("akademik", "grades.json")), "📊"),
            ("Devamsızlık", _count_json(get_data_path("akademik", "attendance.json")), "📋"),
            ("Ödev", _count_json(get_data_path("akademik", "odevler.json")), "📝"),
        ],
    }

    # --- ÖLÇME DEĞERLENDİRME ---
    stats["Ölçme Değerlendirme"] = {
        "icon": "📝", "renk": "#b91c1c",
        "metrikler": [
            ("Soru", _count_json(get_data_path("olcme", "questions.json")), "❓"),
            ("Kazanım", _count_json(get_data_path("olcme", "outcomes.json")), "🎯"),
            ("Sınav", _count_json(get_data_path("olcme", "exams.json")), "📄"),
            ("Sonuç", _count_json(get_data_path("olcme", "results.json")), "📊"),
            ("MEB Plan", _count_json(get_data_path("olcme", "annual_plans.json")), "📅"),
        ],
    }

    # --- İNSAN KAYNAKLARI ---
    ik_dir = os.path.join(td, "ik")
    stats["İnsan Kaynakları"] = {
        "icon": "👥", "renk": "#0e9aa7",
        "metrikler": [
            ("Çalışan", _count_json(os.path.join(ik_dir, "employees.json")), "👔"),
            ("Pozisyon", _count_json(os.path.join(ik_dir, "positions.json")), "🏷️"),
            ("Aday", _count_json(os.path.join(ik_dir, "candidates.json")), "📋"),
            ("İzin", _count_json(os.path.join(ik_dir, "izinler.json")), "🏖️"),
            ("Performans", _count_json(os.path.join(ik_dir, "performance_reviews.json")), "⭐"),
        ],
    }

    # --- REHBERLİK ---
    reh_dir = os.path.join(td, "rehberlik")
    stats["Rehberlik"] = {
        "icon": "🧠", "renk": "#7c3aed",
        "metrikler": [
            ("Görüşme", _count_json(os.path.join(reh_dir, "gorusme_kayitlari.json")), "💬"),
            ("Vaka", _count_json(os.path.join(reh_dir, "vaka_kayitlari.json")), "📁"),
            ("Aile Görüşme", _count_json(os.path.join(reh_dir, "aile_gorusmeleri.json")), "👨‍👩‍👧"),
            ("Yönlendirme", _count_json(os.path.join(reh_dir, "yonlendirmeler.json")), "🔀"),
            ("BEP", _count_json(os.path.join(reh_dir, "bep_kayitlari.json")), "📑"),
        ],
    }

    # --- OKUL SAĞLIĞI ---
    sag_dir = os.path.join(td, "saglik")
    stats["Okul Sağlığı"] = {
        "icon": "🏥", "renk": "#dc2626",
        "metrikler": [
            ("Sağlık Kartı", _count_json(os.path.join(sag_dir, "saglik_kartlari.json")), "💳"),
            ("Revir Ziyareti", _count_json(os.path.join(sag_dir, "revir_ziyaretleri.json")), "🏥"),
            ("İlaç Uygulama", _count_json(os.path.join(sag_dir, "ilac_uygulamalari.json")), "💊"),
            ("Kaza/Olay", _count_json(os.path.join(sag_dir, "kaza_olaylari.json")), "⚠️"),
            ("Seminer", _count_json(os.path.join(sag_dir, "seminerler.json")), "🎓"),
        ],
    }

    # --- RANDEVU & ZİYARETÇİ ---
    rnd_dir = os.path.join(td, "randevu")
    stats["Randevu & Ziyaretçi"] = {
        "icon": "📅", "renk": "#8b5cf6",
        "metrikler": [
            ("Randevu", _count_json(os.path.join(rnd_dir, "randevular.json")), "📅"),
            ("Ziyaretçi", _count_json(os.path.join(rnd_dir, "ziyaretciler.json")), "🚶"),
            ("Ziyaret Kaydı", _count_json(os.path.join(rnd_dir, "ziyaret_kayitlari.json")), "📋"),
            ("Görüşme Notu", _count_json(os.path.join(rnd_dir, "gorusme_notlari.json")), "📝"),
        ],
    }

    # --- TOPLANTI & KURULLAR ---
    top_dir = os.path.join(td, "toplanti")
    stats["Toplantı & Kurullar"] = {
        "icon": "🤝", "renk": "#059669",
        "metrikler": [
            ("Toplantı", _count_json(os.path.join(top_dir, "meetings.json")), "🤝"),
            ("Karar", _count_json(os.path.join(top_dir, "decisions.json")), "✅"),
            ("Görev", _count_json(os.path.join(top_dir, "gorevler.json")), "📌"),
            ("Kurul", _count_json(os.path.join(top_dir, "kurullar.json")), "🏛️"),
        ],
    }

    # --- SOSYAL ETKİNLİK ---
    se_dir = os.path.join(td, "sosyal_etkinlik")
    stats["Sosyal Etkinlik"] = {
        "icon": "🎭", "renk": "#ea580c",
        "metrikler": [
            ("Kulüp", _count_json(os.path.join(se_dir, "kulupler.json")), "🎭"),
            ("Etkinlik", _count_json(os.path.join(se_dir, "etkinlikler.json")), "🎉"),
            ("Faaliyet", _count_json(os.path.join(se_dir, "kulup_faaliyetler.json")), "📋"),
        ],
    }

    # --- KÜTÜPHANE ---
    kut_dir = os.path.join(td, "kutuphane")
    stats["Kütüphane"] = {
        "icon": "📖", "renk": "#0891b2",
        "metrikler": [
            ("Materyal", _count_json(os.path.join(kut_dir, "materyaller.json")), "📚"),
            ("Ödünç İşlem", _count_json(os.path.join(kut_dir, "odunc_islemleri.json")), "🔄"),
        ],
    }

    # --- BÜTÇE GELİR GİDER ---
    but_dir = os.path.join(td, "butce")
    stats["Bütçe Gelir Gider"] = {
        "icon": "💰", "renk": "#4472C4",
        "metrikler": [
            ("Gelir Kaydı", _count_json(os.path.join(but_dir, "gelir_kayitlari.json")), "📈"),
            ("Gider Kaydı", _count_json(os.path.join(but_dir, "gider_kayitlari.json")), "📉"),
            ("Bütçe Planı", _count_json(os.path.join(but_dir, "butce_planlari.json")), "📊"),
        ],
    }

    # --- TÜKETİM & DEMİRBAŞ ---
    tdm_dir = os.path.join(td, "tdm")
    stats["Tüketim & Demirbaş"] = {
        "icon": "📦", "renk": "#ea580c",
        "metrikler": [
            ("Demirbaş", _count_json(os.path.join(tdm_dir, "demirbaslar.json")), "🗄️"),
            ("Tüketim Ürün", _count_json(os.path.join(tdm_dir, "tuketim_urunleri.json")), "📦"),
            ("Zimmet", _count_json(os.path.join(tdm_dir, "zimmet_kayitlari.json")), "📋"),
            ("Satın Alma", _count_json(os.path.join(tdm_dir, "satin_alma_talepleri.json")), "🛒"),
        ],
    }

    # --- DESTEK HİZMETLERİ ---
    des_dir = os.path.join(td, "destek")
    stats["Destek Hizmetleri"] = {
        "icon": "🔧", "renk": "#6366f1",
        "metrikler": [
            ("Talep (Ticket)", _count_json(os.path.join(des_dir, "tickets.json")), "🎫"),
            ("Periyodik Görev", _count_json(os.path.join(des_dir, "periyodik_gorevler.json")), "🔄"),
            ("Denetim", _count_json(os.path.join(des_dir, "denetimler.json")), "🔍"),
            ("Bakım Kaydı", _count_json(os.path.join(des_dir, "bakim_kayitlari.json")), "🔧"),
        ],
    }

    # --- SİVİL SAVUNMA & İSG ---
    ssg_dir = os.path.join(td, "ssg")
    stats["Sivil Savunma & İSG"] = {
        "icon": "⛑️", "renk": "#b91c1c",
        "metrikler": [
            ("Risk Kaydı", _count_json(os.path.join(ssg_dir, "risk_kayitlari.json")), "⚠️"),
            ("Tatbikat", _count_json(os.path.join(ssg_dir, "tatbikat_kayitlari.json")), "🚨"),
            ("Olay Kaydı", _count_json(os.path.join(ssg_dir, "olay_kayitlari.json")), "📋"),
            ("Denetim", _count_json(os.path.join(ssg_dir, "denetim_kayitlari.json")), "🔍"),
        ],
    }

    # --- SWOT ANALİZİ ---
    swot_dir = os.path.join(td, "swot")
    stats["SWOT Analizi"] = {
        "icon": "📊", "renk": "#7e22ce",
        "metrikler": [
            ("Ölçüm", _count_json(os.path.join(swot_dir, "olcumler.json")), "📐"),
            ("Madde", _count_json(os.path.join(swot_dir, "maddeler.json")), "📝"),
            ("Aksiyon", _count_json(os.path.join(swot_dir, "aksiyonlar.json")), "🎯"),
        ],
    }

    # --- VELİ MEMNUNİYET ---
    va_dir = os.path.join(td, "veli_anket")
    stats["Veli Memnuniyet"] = {
        "icon": "📝", "renk": "#059669",
        "metrikler": [
            ("Anket Sorusu", _count_json(os.path.join(va_dir, "sorular.json")), "❓"),
            ("Cevap", _count_json(os.path.join(va_dir, "cevaplar.json")), "✅"),
            ("Yorum", _count_json(os.path.join(va_dir, "yorumlar.json")), "💬"),
        ],
    }

    # --- MEZUNLAR & KARİYER ---
    stats["Mezunlar & Kariyer"] = {
        "icon": "🎓", "renk": "#6366f1",
        "metrikler": [
            ("Mezun", _count_json(os.path.join(td, "mezunlar.json")), "🎓"),
            ("Etkinlik", _count_json(os.path.join(td, "mezun_etkinlikleri.json")), "🎉"),
            ("Mentorluk", _count_json(os.path.join(td, "mezun_mentorluk.json")), "🤝"),
        ],
    }

    # --- HALKLA İLİŞKİLER ---
    stats["Halkla İlişkiler"] = {
        "icon": "📢", "renk": "#059669",
        "metrikler": [
            ("Kayıt Adayı", _count_json(os.path.join(td, "pr01_kayit_adaylari.json")), "📋"),
            ("Sözleşme", _count_json(os.path.join(td, "sozlesmeler.json")), "📄"),
            ("Görüşme Kaydı", _count_json(os.path.join(td, "pr01_gorusme_kayitlari.json")), "💬"),
        ],
    }

    # --- KURUMSAL ORGANİZASYON ---
    stats["Kurumsal Organizasyon"] = {
        "icon": "🏢", "renk": "#0d9488",
        "metrikler": [
            ("Personel", _count_json(os.path.join(td, "kim01_staff.json")), "👥"),
            ("Şikayet/Öneri", _count_json(os.path.join(td, "kim01_sikayet_oneri.json")), "📩"),
        ],
    }

    # --- YÖNETİM TEK EKRAN ---
    yte_dir = os.path.join(td, "yte")
    stats["Yönetim Tek Ekran"] = {
        "icon": "📊", "renk": "#0B0F19",
        "metrikler": [
            ("Görev", _count_json(os.path.join(yte_dir, "gorevler.json")), "📌"),
            ("Rapor", _count_json(os.path.join(yte_dir, "raporlar.json")), "📄"),
        ],
    }

    return stats


def _render_live_dashboard(stats: dict[str, dict]) -> None:
    """Tüm modüllerden toplanan canlı verileri dashboard kartları olarak göster."""
    # Genel toplam hesapla
    toplam_kayit = sum(
        sum(v for _, v, _ in modul["metrikler"])
        for modul in stats.values()
    )
    aktif_modul = sum(1 for m in stats.values() if any(v > 0 for _, v, _ in m["metrikler"]))

    # Üst KPI bar
    _kpi_html = (
        '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">'
        '<div style="flex:1;min-width:160px;background:linear-gradient(135deg,#1e3a8a,#2563eb);'
        'border-radius:12px;padding:14px 18px;text-align:center;box-shadow:0 4px 16px rgba(37,99,235,.25)">'
        f'<div style="font-size:1.8rem;font-weight:800;color:#fff">{toplam_kayit:,}</div>'
        '<div style="font-size:.72rem;color:#93c5fd;font-weight:600">Toplam Kayıt</div></div>'
        '<div style="flex:1;min-width:160px;background:linear-gradient(135deg,#059669,#34d399);'
        'border-radius:12px;padding:14px 18px;text-align:center;box-shadow:0 4px 16px rgba(5,150,105,.25)">'
        f'<div style="font-size:1.8rem;font-weight:800;color:#fff">{aktif_modul}</div>'
        '<div style="font-size:.72rem;color:#a7f3d0;font-weight:600">Aktif Veri Modülü</div></div>'
        '<div style="flex:1;min-width:160px;background:linear-gradient(135deg,#7c3aed,#a78bfa);'
        'border-radius:12px;padding:14px 18px;text-align:center;box-shadow:0 4px 16px rgba(124,58,237,.25)">'
        f'<div style="font-size:1.8rem;font-weight:800;color:#fff">{len(stats)}</div>'
        '<div style="font-size:.72rem;color:#ddd6fe;font-weight:600">İzlenen Modül</div></div>'
        '<div style="flex:1;min-width:160px;background:linear-gradient(135deg,#0891b2,#67e8f9);'
        'border-radius:12px;padding:14px 18px;text-align:center;box-shadow:0 4px 16px rgba(8,145,178,.25)">'
        '<div style="font-size:1.8rem;font-weight:800;color:#fff">⚡ Canlı</div>'
        '<div style="font-size:.72rem;color:#a5f3fc;font-weight:600">Anlık Senkron</div></div></div>'
    )
    st.markdown(_kpi_html, unsafe_allow_html=True)

    # Modül kartları — 3 sütun grid
    sorted_stats = sorted(stats.items(), key=lambda x: -sum(v for _, v, _ in x[1]["metrikler"]))
    cols = st.columns(3)
    for idx, (modul_adi, modul) in enumerate(sorted_stats):
        with cols[idx % 3]:
            renk = modul["renk"]
            ikon = modul["icon"]
            metrikler = modul["metrikler"]
            toplam = sum(v for _, v, _ in metrikler)

            metrik_parts = []
            for label, value, m_icon in metrikler:
                bar_w = min(value / max(toplam, 1) * 100, 100) if toplam > 0 else 0
                metrik_parts.append(
                    f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">'
                    f'<span style="font-size:.85rem;width:20px;text-align:center">{m_icon}</span>'
                    f'<div style="flex:1">'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:2px">'
                    f'<span style="font-size:.72rem;color:#94a3b8">{label}</span>'
                    f'<span style="font-size:.75rem;font-weight:700;color:#e2e8f0">{value:,}</span>'
                    f'</div>'
                    f'<div style="height:4px;background:rgba(148,163,184,.2);border-radius:2px;overflow:hidden">'
                    f'<div style="width:{bar_w}%;height:100%;background:{renk};border-radius:2px;transition:width .5s ease"></div>'
                    f'</div></div></div>'
                )

            metrik_html = "".join(metrik_parts)
            card_html = (
                f'<div style="background:linear-gradient(160deg,#111827,#1A2035);'
                f'border:1px solid rgba(37,99,235,.1);border-radius:14px;'
                f'padding:16px;margin-bottom:12px;'
                f'box-shadow:0 2px 8px rgba(0,0,0,.06);'
                f'border-top:3px solid {renk}">'
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">'
                f'<span style="font-size:1.3rem">{ikon}</span>'
                f'<span style="font-size:.88rem;font-weight:700;color:#e2e8f0">{modul_adi}</span>'
                f'<span style="margin-left:auto;background:{renk}22;color:{renk};'
                f'padding:2px 8px;border-radius:6px;font-size:.68rem;font-weight:700">'
                f'{toplam:,} kayıt</span>'
                f'</div>{metrik_html}</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


def _render_dk_usage_panel() -> None:
    """Dijital Kütüphane rol bazlı kullanım oranları paneli."""
    try:
        from models.dijital_kutuphane import DijitalKutuphaneDataStore
        dk_store = DijitalKutuphaneDataStore(os.path.join(get_tenant_dir(), "dijital_kutuphane"))
        usage = dk_store.get_usage_stats()
    except Exception:
        usage = {"toplam": 0, "bugun": 0, "roller": {}, "sekmeler": {}, "gunluk_trend": {}, "benzersiz_kullanici": 0}

    toplam = usage["toplam"]
    bugun = usage["bugun"]
    benzersiz = usage["benzersiz_kullanici"]
    roller = usage["roller"]
    sekmeler = usage["sekmeler"]
    gunluk = usage["gunluk_trend"]

    # Rol renk ve ikon haritası
    _ROL_BILGI = {
        "Yonetici": {"renk": "#2563eb", "ikon": "👨‍💼", "label": "Yönetici"},
        "Ogretmen": {"renk": "#059669", "ikon": "👩‍🏫", "label": "Öğretmen"},
        "Ogrenci":  {"renk": "#f59e0b", "ikon": "👨‍🎓", "label": "Öğrenci"},
        "Veli":     {"renk": "#7c3aed", "ikon": "👨‍👩‍👧", "label": "Veli"},
        "Bilinmiyor": {"renk": "#64748b", "ikon": "❓", "label": "Diğer"},
    }

    # Üst KPI kartları
    st.markdown(f"""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px">
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#4f46e5,#818cf8);
            border-radius:12px;padding:14px 16px;text-align:center;
            box-shadow:0 4px 16px rgba(79,70,229,.25)">
            <div style="font-size:1.6rem;font-weight:800;color:#fff">{toplam:,}</div>
            <div style="font-size:.68rem;color:#c7d2fe;font-weight:600">Toplam Kullanım</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#0891b2,#67e8f9);
            border-radius:12px;padding:14px 16px;text-align:center;
            box-shadow:0 4px 16px rgba(8,145,178,.25)">
            <div style="font-size:1.6rem;font-weight:800;color:#fff">{bugun}</div>
            <div style="font-size:.68rem;color:#a5f3fc;font-weight:600">Bugün</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#059669,#34d399);
            border-radius:12px;padding:14px 16px;text-align:center;
            box-shadow:0 4px 16px rgba(5,150,105,.25)">
            <div style="font-size:1.6rem;font-weight:800;color:#fff">{benzersiz}</div>
            <div style="font-size:.68rem;color:#a7f3d0;font-weight:600">Benzersiz Kullanıcı</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#f59e0b,#fbbf24);
            border-radius:12px;padding:14px 16px;text-align:center;
            box-shadow:0 4px 16px rgba(245,158,11,.25)">
            <div style="font-size:1.6rem;font-weight:800;color:#fff">{len(gunluk)}</div>
            <div style="font-size:.68rem;color:#fef3c7;font-weight:600">Aktif Gün</div>
        </div>
    </div>""", unsafe_allow_html=True)

    if toplam == 0:
        st.markdown("""
        <div style="background:rgba(37,99,235,.05);border:1px solid rgba(37,99,235,.12);
            border-radius:12px;padding:20px;text-align:center;margin-bottom:12px">
            <div style="font-size:1.5rem;margin-bottom:6px">📱</div>
            <div style="font-size:.85rem;color:#94a3b8">Henüz kullanım verisi yok.
            Dijital Kütüphane kullanıldıkça veriler burada anlık görünecek.</div>
        </div>""", unsafe_allow_html=True)
        return

    # İki sütun: Rol bazlı dağılım + Sekme bazlı popülerlik
    c1, c2 = st.columns(2)

    with c1:
        # Rol bazlı kullanım oranları
        rol_html = ""
        for rol, sayi in sorted(roller.items(), key=lambda x: -x[1]):
            bilgi = _ROL_BILGI.get(rol, _ROL_BILGI["Bilinmiyor"])
            oran = round(sayi / toplam * 100, 1) if toplam > 0 else 0
            rol_html += (
                f'<div style="margin-bottom:10px">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
                f'<span style="font-size:.78rem;color:#94a3b8">{bilgi["ikon"]} {bilgi["label"]}</span>'
                f'<span style="font-size:.75rem;font-weight:700;color:{bilgi["renk"]}">{sayi}'
                f' <span style="font-size:.65rem;color:#94a3b8">(%{oran})</span></span>'
                f'</div>'
                f'<div style="height:8px;background:rgba(148,163,184,.2);border-radius:4px;overflow:hidden">'
                f'<div style="width:{oran}%;height:100%;background:{bilgi["renk"]};border-radius:4px"></div>'
                f'</div></div>'
            )
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#131825,#1a2035);border:1px solid rgba(37,99,235,.1);border-radius:12px;padding:16px;margin-bottom:8px">'
            f'<div style="font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:12px">👥 Rol Bazlı Kullanım Oranları</div>'
            f'{rol_html}</div>',
            unsafe_allow_html=True,
        )

    with c2:
        # En popüler sekmeler
        sekme_sorted = sorted(sekmeler.items(), key=lambda x: -x[1])[:8]
        max_sekme = sekme_sorted[0][1] if sekme_sorted else 1
        sekme_html = ""
        _sekme_renk = ["#2563eb", "#7c3aed", "#059669", "#f59e0b", "#dc2626", "#0891b2", "#ea580c", "#6366f1"]
        for i, (sekme, sayi) in enumerate(sekme_sorted):
            bar_w = round(sayi / max_sekme * 100, 1)
            renk = _sekme_renk[i % len(_sekme_renk)]
            sekme_html += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'
                f'<span style="font-size:.72rem;color:#94a3b8;min-width:100px;text-align:right">{sekme}</span>'
                f'<div style="flex:1;height:6px;background:rgba(148,163,184,.2);border-radius:3px;overflow:hidden">'
                f'<div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px"></div></div>'
                f'<span style="font-size:.7rem;font-weight:700;color:#94A3B8;min-width:28px">{sayi}</span>'
                f'</div>'
            )
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#131825,#1a2035);border:1px solid rgba(37,99,235,.1);border-radius:12px;padding:16px;margin-bottom:8px">'
            f'<div style="font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:12px">🔥 En Popüler Sekmeler</div>'
            f'{sekme_html}</div>',
            unsafe_allow_html=True,
        )

    # Son 7 gün trendi
    if len(gunluk) > 1:
        son_gunler = sorted(gunluk.items(), key=lambda x: x[0])[-7:]
        max_gun = max(v for _, v in son_gunler)
        trend_html = ""
        for tarih, sayi in son_gunler:
            bar_h = max(round(sayi / max_gun * 60, 0), 4) if max_gun > 0 else 4
            gun_label = tarih[-5:]  # MM-DD
            trend_html += (
                f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1">'
                f'<span style="font-size:.68rem;font-weight:700;color:#e2e8f0">{sayi}</span>'
                f'<div style="width:100%;max-width:32px;height:{bar_h}px;'
                f'background:linear-gradient(180deg,#2563eb,#60a5fa);border-radius:4px"></div>'
                f'<span style="font-size:.6rem;color:#94a3b8">{gun_label}</span>'
                f'</div>'
            )
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#131825,#1a2035);border:1px solid rgba(37,99,235,.1);border-radius:12px;padding:16px;margin-top:4px">'
            f'<div style="font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:12px">📈 Son 7 Gün Kullanım Trendi</div>'
            f'<div style="display:flex;align-items:flex-end;gap:6px;min-height:80px">{trend_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── ANA RENDER ────────────────────────────────────────────────────────────────

def render_ana_sayfa() -> None:
    """Ana sayfa — karşılama + arama + 4 sütunlu modül kartları."""
    _css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("ana_sayfa")
    except Exception:
        pass

    auth_user = AuthManager.get_current_user()
    user_name = auth_user.get("name", "Kullanıcı")
    tarih, saat = _tarih_str()

    # ── Karşılama banner
    st.markdown(
        f"""
        <div class="as-welcome">
            <div class="as-welcome-left">
                <span class="as-welcome-emoji">👋</span>
                <div>
                    <p class="as-welcome-title">Hoş geldiniz, {user_name}</p>
                    <p class="as-welcome-sub">SmartCampus AI — Akademik Yönetim Platformu</p>
                </div>
            </div>
            <div class="as-welcome-date">
                <span class="as-date-day">{tarih}</span>
                {saat}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Canlı veri toplama (tek seferde — sayfa boyunca paylaşılır)
    _MODUL_KARTLARI = _get_modul_kartlari()
    toplam_modul = len(_MODUL_KARTLARI)
    live_stats = _collect_live_stats()
    _toplam_kayit = sum(sum(v for _, v, _ in m["metrikler"]) for m in live_stats.values())
    _aktif_modul = sum(1 for m in live_stats.values() if any(v > 0 for _, v, _ in m["metrikler"]))

    st.markdown(
        f"""
        <div class="as-kpi-bar">
            <div class="as-kpi-card">
                <div class="as-kpi-icon">📦</div>
                <div>
                    <div class="as-kpi-value">{toplam_modul}</div>
                    <div class="as-kpi-label">Toplam Modül</div>
                </div>
            </div>
            <div class="as-kpi-card">
                <div class="as-kpi-icon">📊</div>
                <div>
                    <div class="as-kpi-value">{_toplam_kayit:,}</div>
                    <div class="as-kpi-label">Toplam Kayıt</div>
                </div>
            </div>
            <div class="as-kpi-card">
                <div class="as-kpi-icon">✅</div>
                <div>
                    <div class="as-kpi-value">{_aktif_modul}</div>
                    <div class="as-kpi-label">Aktif Modül</div>
                </div>
            </div>
            <div class="as-kpi-card">
                <div class="as-kpi-icon">🤖</div>
                <div>
                    <div class="as-kpi-value">AI</div>
                    <div class="as-kpi-label">Asistan Hazır</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Arama
    col_s, _ = st.columns([2, 3])
    with col_s:
        search_q = st.text_input(
            "",
            placeholder="Modül veya sekme ara...",
            key="as_search",
            label_visibility="collapsed",
        )

    # ── Yetki filtresi
    izinli = get_user_modules(auth_user.get("username", ""))
    kartlar = _MODUL_KARTLARI[:]
    if izinli:
        kartlar = [k for k in kartlar if k["key"] in izinli]

    # ── Arama filtresi
    if search_q:
        sq = search_q.strip().lower()
        sonuc = []
        for k in kartlar:
            if sq in k["baslik"].lower() or sq in k["key"].lower():
                sonuc.append(k)
            else:
                eslesen = [m for m in k["menuler"] if sq in m.lower()]
                if eslesen:
                    kk = dict(k)
                    kk["menuler"] = eslesen
                    sonuc.append(kk)
        kartlar = sonuc

    # ── Etiket
    etiket = f"{len(kartlar)} modül" + (f' — "{search_q}" araması' if search_q else "")
    st.markdown(f'<div class="as-section-label">Hızlı Erişim · {etiket}</div>', unsafe_allow_html=True)

    if not kartlar:
        st.info("Aramanızla eşleşen modül bulunamadı.")
        return

    # ── 4 sütunlu grid
    cols = st.columns(4)
    for idx, kart in enumerate(kartlar):
        with cols[idx % 4]:
            _render_kart(kart)

    # ── DİJİTAL KÜTÜPHANE KULLANIM ORANLARI ──
    st.markdown("""<div style="height:2px;background:linear-gradient(90deg,transparent,
        rgba(0,0,0,.08),transparent);margin:24px 0 8px 0"></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="as-section-label">📱 Dijital Kütüphane Kullanım Oranları · Rol Bazlı Anlık Takip</div>""",
                unsafe_allow_html=True)
    _render_dk_usage_panel()

    # ── CANLI MODÜL RAPORLARI (Tüm modüllerden senkronize) ──
    st.markdown("""<div style="height:2px;background:linear-gradient(90deg,transparent,
        rgba(0,0,0,.08),transparent);margin:24px 0 8px 0"></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="as-section-label">📊 Canlı Modül Raporları · Anlık Veri Senkronizasyonu</div>""",
                unsafe_allow_html=True)
    _render_live_dashboard(live_stats)
