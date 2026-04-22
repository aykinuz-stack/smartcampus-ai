"""
Kisisel Dil Gelisimi — Premium Diamond Edition
10 alt modul: Ingilizce, Almanca, Fransizca, Italyanca, Ispanyolca,
KDG Ingilizce, KDG Almanca, Pratik Dil, Dil Treni
"""
from __future__ import annotations
import streamlit as st

_PREFIX = "kdg_hub_"
_VIEW_KEY = f"{_PREFIX}view"

# Alt modul tanimlari — tumu gold/diamond tema
_SUBMODULES = [
    {
        "id": "fono_en",
        "icon": "🇬🇧",
        "title": "İngilizce",
        "desc": "104 Ders | Kendi Kendine Hızlı İngilizce",
        "badge": "A1 → B1",
    },
    {
        "id": "fono_de",
        "icon": "🇩🇪",
        "title": "Almanca",
        "desc": "104 Ders | Kendi Kendine Hızlı Almanca",
        "badge": "A1 → B1",
    },
    {
        "id": "fono_fr",
        "icon": "🇫🇷",
        "title": "Fransızca",
        "desc": "104 Ders | Kendi Kendine Hızlı Fransızca",
        "badge": "A1 → B1",
    },
    {
        "id": "fono_it",
        "icon": "🇮🇹",
        "title": "İtalyanca",
        "desc": "104 Ders | Kendi Kendine Hızlı İtalyanca",
        "badge": "A1 → B1",
    },
    {
        "id": "fono_es",
        "icon": "🇪🇸",
        "title": "İspanyolca",
        "desc": "104 Ders | Kendi Kendine Hızlı İspanyolca",
        "badge": "A1 → B1",
    },
    {
        "id": "kdg_en",
        "icon": "🌟",
        "title": "KDG İngilizce",
        "desc": "CEFR Uyumlu Diamond Premium İngilizce",
        "badge": "CEFR",
    },
    {
        "id": "kdg_de",
        "icon": "🇩🇪",
        "title": "KDG Almanca",
        "desc": "CEFR Uyumlu Diamond Premium Almanca",
        "badge": "CEFR",
    },
    {
        "id": "pratik_dil",
        "icon": "💎",
        "title": "Pratik Dil",
        "desc": "5 Dil | 770 Kelime & 600 Cümle | Sesli Telaffuz",
        "badge": "PREMIUM",
    },
    {
        "id": "dil_treni",
        "icon": "🚂",
        "title": "Dil Treni",
        "desc": "10 Dil | 400 Kelime | Tren & Flashcard",
        "badge": "YENİ",
    },
]


def _inject_css():
    st.markdown("""
    <style>
    /* ═══ PREMIUM DIAMOND GOLD+NAVY THEME ═══ */
    @keyframes kdg-shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes kdg-glow-pulse {
        0%, 100% { box-shadow: 0 0 15px rgba(212,175,55,0.15), 0 4px 20px rgba(0,0,0,0.3); }
        50% { box-shadow: 0 0 25px rgba(212,175,55,0.3), 0 4px 30px rgba(0,0,0,0.4); }
    }
    @keyframes kdg-diamond-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* ─── HEADER ─── */
    .kdg-hub-header {
        background: linear-gradient(135deg, #0B0F19 0%, #141440 40%, #232B3E 100%);
        padding: 32px 36px;
        border-radius: 18px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(212,175,55,0.25);
    }
    .kdg-hub-header::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
        animation: kdg-shimmer 4s infinite;
    }
    .kdg-hub-header::after {
        content: '◆';
        position: absolute;
        top: 12px; right: 20px;
        font-size: 2.2rem;
        color: rgba(212,175,55,0.12);
        animation: kdg-diamond-spin 12s linear infinite;
    }
    .kdg-hub-header h1 {
        font-size: 1.7rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 1.5px;
        background: linear-gradient(135deg, #6366F1, #6366F1, #6366F1);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: kdg-shimmer 3s linear infinite;
    }
    .kdg-hub-header p {
        color: #94A3B8;
        font-size: 0.9rem;
        margin: 8px 0 0 0;
        letter-spacing: 0.3px;
    }
    .kdg-hub-header .kdg-diamond-line {
        width: 80px; height: 2px;
        background: linear-gradient(90deg, transparent, #6366F1, transparent);
        margin: 10px 0 0 0;
        border-radius: 2px;
    }

    /* ─── CARDS ─── */
    .kdg-card {
        background: linear-gradient(145deg, rgba(20,20,60,0.95), rgba(10,10,46,0.98));
        border-radius: 16px;
        padding: 26px 18px;
        text-align: center;
        min-height: 210px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border: 1px solid rgba(212,175,55,0.2);
        position: relative;
        overflow: hidden;
        animation: kdg-glow-pulse 4s ease-in-out infinite;
    }
    .kdg-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.04), transparent);
        animation: kdg-shimmer 5s infinite;
    }
    .kdg-card::after {
        content: '';
        position: absolute;
        top: -1px; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 10%, #6366F1 50%, transparent 90%);
    }
    .kdg-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(212,175,55,0.5);
        box-shadow: 0 0 35px rgba(212,175,55,0.25), 0 8px 32px rgba(0,0,0,0.5);
    }
    .kdg-card-icon {
        font-size: 2.8rem;
        margin-bottom: 12px;
        filter: drop-shadow(0 2px 6px rgba(212,175,55,0.3));
    }
    .kdg-card-title {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 6px;
        background: linear-gradient(135deg, #6366F1, #6366F1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.5px;
    }
    .kdg-card-desc {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .kdg-card-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 1px;
        background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(244,208,63,0.08));
        color: #6366F1;
        border: 1px solid rgba(212,175,55,0.3);
    }

    /* ─── INFO BOXES ─── */
    .kdg-info-box {
        background: linear-gradient(135deg, rgba(20,20,60,0.9), rgba(10,10,46,0.95));
        padding: 18px 22px;
        border-radius: 14px;
        margin-top: 22px;
        border: 1px solid rgba(212,175,55,0.15);
        position: relative;
        overflow: hidden;
    }
    .kdg-info-box::before {
        content: '';
        position: absolute;
        top: -1px; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 5%, #6366F1 50%, transparent 95%);
    }
    .kdg-info-box b {
        color: #6366F1;
    }
    .kdg-info-box .kdg-info-text {
        font-size: 0.85rem;
        color: #CBD5E1;
        line-height: 1.7;
    }
    .kdg-section-header {
        background: linear-gradient(135deg, #0B0F19, #232B3E);
        padding: 22px 26px;
        border-radius: 16px;
        margin-top: 26px;
        border: 1px solid rgba(212,175,55,0.2);
        position: relative;
        overflow: hidden;
    }
    .kdg-section-header::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.05), transparent);
        animation: kdg-shimmer 4s infinite;
    }
    .kdg-section-header h2 {
        font-size: 1.15rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #6366F1, #6366F1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kdg-section-header p {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 4px 0 0 0;
    }

    /* ─── BUTTONS ─── */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #232B3E, #0B0F19) !important;
        color: #6366F1 !important;
        border: 1px solid rgba(212,175,55,0.35) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #6366F1, #A5B4FC) !important;
        color: #0B0F19 !important;
        border-color: #6366F1 !important;
        box-shadow: 0 0 20px rgba(212,175,55,0.3) !important;
    }

    /* ─── SELECTBOX ─── */
    div[data-testid="stSelectbox"] label {
        color: #6366F1 !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: linear-gradient(135deg, #141440, #0B0F19) !important;
        border: 1px solid rgba(212,175,55,0.25) !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
    }

    /* ─── BACK BUTTON BAR ─── */
    .kdg-back-bar {
        background: linear-gradient(135deg, #0B0F19, #141440);
        padding: 10px 18px;
        border-radius: 12px;
        border: 1px solid rgba(212,175,55,0.15);
        margin-bottom: 12px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .kdg-back-bar .kdg-mod-label {
        font-size: 1.05rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1, #6366F1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
    """, unsafe_allow_html=True)


def _render_hub():
    """Ana ekran — Premium Diamond hub."""
    st.markdown("""
    <div class="kdg-hub-header">
        <h1>◆ Kişisel Dil Gelişimi</h1>
        <div class="kdg-diamond-line"></div>
        <p>Kendi Kendine Öğrenme & CEFR Uyumlu KDG Platformları — Diamond Premium Edition</p>
    </div>
    """, unsafe_allow_html=True)

    # Ust sira: 5 dil modulu
    cols1 = st.columns(5)
    for i, mod in enumerate(_SUBMODULES[:5]):
        with cols1[i]:
            st.markdown(f"""
            <div class="kdg-card">
                <div class="kdg-card-icon">{mod['icon']}</div>
                <div class="kdg-card-title">{mod['title']}</div>
                <div class="kdg-card-desc">{mod['desc']}</div>
                <div class="kdg-card-badge">{mod['badge']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(
                f"◆ {mod['title']}",
                key=f"{_PREFIX}go_{mod['id']}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state[_VIEW_KEY] = mod["id"]
                st.rerun()

    # Alt sira: KDG, Pratik Dil, Dil Treni + diger moduller
    remaining = _SUBMODULES[5:]
    cols2 = st.columns(len(remaining))
    for i, mod in enumerate(remaining):
        with cols2[i]:
            st.markdown(f"""
            <div class="kdg-card">
                <div class="kdg-card-icon">{mod['icon']}</div>
                <div class="kdg-card-title">{mod['title']}</div>
                <div class="kdg-card-desc">{mod['desc']}</div>
                <div class="kdg-card-badge">{mod['badge']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(
                f"◆ {mod['title']}",
                key=f"{_PREFIX}go_{mod['id']}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state[_VIEW_KEY] = mod["id"]
                st.rerun()

    # Alt bilgi — diamond
    st.markdown("""
    <div class="kdg-info-box">
        <div class="kdg-info-text">
            <b>◆ Dil Modülleri (5 Dil):</b> İngilizce, Almanca, Fransızca, İtalyanca, İspanyolca — Her biri 104 ders, interaktif alıştırmalı, sesli telaffuz<br>
            <b>◆ KDG Modülleri:</b> CEFR uyumlu, adaptif, Diamond Premium öğrenim platformu<br>
            <b>◆ Pratik Dil:</b> 4 dilde 200 kelime & cümle, sesli telaffuz, flashcard pratik<br>
            <b>◆ Dil Treni:</b> 10 dilde 400 kelime, tren vagonu metaforu, sesli telaffuz & flashcard
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── İnteraktif Çalışmalar — diamond ──
    st.markdown("""
    <div class="kdg-section-header">
        <h2>◆ İnteraktif Çalışmalar</h2>
        <p>Kelime, oyun, şarkı, diyalog, okuma, yazma, dilbilgisi, sesler ve dinleme</p>
    </div>
    """, unsafe_allow_html=True)

    _CEFR_LEVELS = {
        "Pre-A1 (Okul Öncesi)": "preschool",
        "A1 Başlangıç (1. Sınıf)": "grade1",
        "A1 (2. Sınıf)": "grade2",
        "A1+ (3. Sınıf)": "grade3",
        "A2 Temel (4. Sınıf)": "grade4",
        "A2 (5. Sınıf)": "grade5",
        "A2+ (6. Sınıf)": "grade6",
        "B1 Orta (7. Sınıf)": "grade7",
        "B1 (8. Sınıf)": "grade8",
        "B1+ (9. Sınıf)": "grade9",
        "B2 Orta Üstü (10. Sınıf)": "grade10",
        "B2 (11. Sınıf)": "grade11",
        "B2+ / C1 (12. Sınıf)": "grade12",
    }
    _level_names = list(_CEFR_LEVELS.keys())
    _sel_idx = st.selectbox(
        "Seviye Seç:",
        range(len(_level_names)),
        index=1,
        format_func=lambda i: _level_names[i],
        key=f"{_PREFIX}ia_level",
    )
    _sel_level = _CEFR_LEVELS[_level_names[_sel_idx]]
    _kp = f"kdg_hub_ia_{_sel_level}"

    from views.kdg_interaktif import render_interaktif_calisma
    render_interaktif_calisma(level=_sel_level, key_prefix=_kp)


def render_kisisel_dil_gelisimi():
    """Ana giris noktasi — Kisisel Dil Gelisimi hub."""
    _inject_css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("kisisel_dil_gelisimi")
    except Exception:
        pass

    if _VIEW_KEY not in st.session_state:
        st.session_state[_VIEW_KEY] = "hub"

    view = st.session_state[_VIEW_KEY]

    # Geri butonu (alt moduldeyken) — diamond
    if view != "hub":
        mod_info = next((m for m in _SUBMODULES if m["id"] == view), None)
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("◆ Ana Ekrana Dön", key=f"{_PREFIX}back", type="secondary"):
                st.session_state[_VIEW_KEY] = "hub"
                st.rerun()
        with c2:
            if mod_info:
                st.markdown(
                    f'<div class="kdg-back-bar">'
                    f'<span class="kdg-mod-label">{mod_info["icon"]} {mod_info["title"]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # Routing
    if view == "hub":
        _render_hub()

    elif view == "fono_en":
        from views.fono_ingilizce import render_fono_ingilizce
        render_fono_ingilizce()

    elif view == "fono_de":
        from views.fono_almanca_104 import render_fono_almanca_104
        render_fono_almanca_104()

    elif view == "fono_fr":
        from views.fono_fransizca import render_fono_fransizca
        render_fono_fransizca()

    elif view == "fono_it":
        from views.fono_italyanca import render_fono_italyanca
        render_fono_italyanca()

    elif view == "fono_es":
        from views.fono_ispanyolca import render_fono_ispanyolca
        render_fono_ispanyolca()

    elif view == "kdg_en":
        from views.yd_tools import _render_kdg_tab
        _render_kdg_tab()

    elif view == "kdg_de":
        from views.yd_tools import _render_kdg_german_tab
        _render_kdg_german_tab()

    elif view == "pratik_dil":
        from views.pratik_dil_premium import render_pratik_dil
        render_pratik_dil()

    elif view == "dil_treni":
        from views.dil_treni_tab import render_dil_treni
        render_dil_treni()

    else:
        st.session_state[_VIEW_KEY] = "hub"
        st.rerun()
